from llama_index.core import set_global_handler
from llama_index.core.workflow import (
    Workflow,
    step
)
from llama_index.core.workflow.events import (
    StopEvent
)
from logging import getLogger
from .events import (
    ActionEvent,
    UrlInputEvent,
    InspectionEvent,
    TranslationEvent,
    ActionNameEnum
)
from obasan.stores import (
    chat_messages,
    phase,
    markdown,
    input_url,
    PhaseEnum
)
from .agents import (
    inspection_run,
    valid_url_run,
    translation_run
)

logger = getLogger(__name__)

class AppWorkflow(Workflow):
    """
    翻訳アプリの統合ワークフロー
    """

    @step
    async def routing(self, ev: ActionEvent) -> UrlInputEvent|TranslationEvent|StopEvent:
        """
        現在の状況を判断しルーティングを行う
        """
        # 処理開始
        match ev.action_name:
            # ファイル検証
            case ActionNameEnum.INSPECT:
                return UrlInputEvent(
                    action_name=ev.action_name,
                    url=ev.url
                )

            # 翻訳
            case ActionNameEnum.TRANSLATE:
                return UrlInputEvent(
                    action_name=ev.action_name,
                    url=ev.url
                )

            case _:
                return StopEvent()

    @step
    async def validate(self, ev: UrlInputEvent) -> InspectionEvent|TranslationEvent|StopEvent:
        """
        入力されたURLの正当性をLLMに検証させる
        """
        # 処理中に変更
        phase.update(PhaseEnum.PENDING)
        try:
            output = await valid_url_run(ev.url)
            # 検証エラー
            if not output.is_valid:
                await chat_messages.reply_message_stream(output.reason)
                return StopEvent()

            # 次のステップへ
            match ev.action_name:
                # ファイル検証へ
                case ActionNameEnum.INSPECT:
                    return InspectionEvent(path=output.path)

                # 翻訳実行へ
                case ActionNameEnum.TRANSLATE:
                    return TranslationEvent(path=output.path)

                case _:
                    return StopEvent()

        except Exception as e:
            # LLM問い合わせでエラー発生(主に構造化データが不正な場合)
            await chat_messages.reply_message_stream("予期せぬエラーが発生しました。")
            logger.error(e)
            return StopEvent()

    @step
    async def inspect(self, ev: InspectionEvent) -> StopEvent:
        """
        PATH を元にファイルの状態を検査するツールをLLMに実行させる
        """
        try:
            output = await inspection_run(path=ev.path)
            phase.update(PhaseEnum.INSPECTED)
            await markdown.render_stream(output.markdown)
            await chat_messages.reply_message_stream(output.comment)

            return StopEvent()
        except Exception as e:
            await chat_messages.reply_message_stream("[inspect] 予期せぬエラーが発生しました。")
            logger.error(e)
            return StopEvent()

    @step
    async def translate(self, ev: TranslationEvent) -> StopEvent:
        """
        PATH を元にファイルを翻訳するツールをLLMに実行させる
        TODO: ほぼほぼ同じ処理であり、イベントやフェーズのステートが違うくらい？
        """
        try:
            output = await translation_run(path=ev.path)
            phase.update(PhaseEnum.TRANSLATED)
            await markdown.render_stream(output.markdown)
            await chat_messages.reply_message_stream(output.comment)

            return StopEvent()
        except Exception as e:
            await chat_messages.reply_message_stream("[translate] 予期せぬエラーが発生しました。")
            logger.error(e)
            return StopEvent()

async def run_workflow(action_name: str) -> None:
    """
    Workflow Run
    """
    set_global_handler("simple")
    phase.update(PhaseEnum.START)
    workflow = AppWorkflow(timeout=360.0)
    await workflow.run(
        start_event=ActionEvent(
            action_name=action_name,
            url=input_url.url
        )
    )
