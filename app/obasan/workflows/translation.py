from llama_index.core import set_global_handler
from llama_index.core.workflow import (
    Workflow,
    step
)
from llama_index.core.workflow.events import (
    StartEvent,
    StopEvent
)
from logging import getLogger
from .events import (
    UrlInputEvent,
    TranslationEvent
)
from obasan.stores import (
    chat_messages,
    phase,
    markdown,
    PhaseEnum
)
from .agents import (
    translation_run,
    valid_url_run
)

logger = getLogger(__name__)

class TranslationWorkflow(Workflow):
    """
    ローカルのリソースファイルの状況から、
    翻訳対象になるかどうかを判断するワークフロー
    """

    @step
    async def routing(self, ev: StartEvent) -> UrlInputEvent|StopEvent:
        """
        現在の状況を判断しルーティングを行う
        """
        set_global_handler("simple")
        # 処理開始
        if phase.is_start:
            return UrlInputEvent(
                url=ev.url
            )

        return StopEvent()

    @step
    async def validate(self, ev: UrlInputEvent) -> TranslationEvent | StopEvent:
        """
        入力されたURLの正当性をLLMに検証させる
        TODO: ここの処理なんか同じやん。
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
            return TranslationEvent(path=output.path)

        except Exception as e:
            # LLM問い合わせでエラー発生(主に構造化データが不正な場合)
            await chat_messages.reply_message_stream("予期せぬエラーが発生しました。")
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
