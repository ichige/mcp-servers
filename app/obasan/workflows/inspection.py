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
    InspectionEvent
)
from obasan.stores import (
    chat_messages,
    phase,
    markdown,
    PhaseEnum
)
from .agents import (
    inspection_run,
    valid_url_run
)

logger = getLogger(__name__)

class InspectionWorkflow(Workflow):
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
    async def validate(self, ev: UrlInputEvent) -> InspectionEvent | StopEvent:
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
            return InspectionEvent(path=output.path)

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
            print(f"inspect: {ev.path}")
            output = await inspection_run(path=ev.path)
            phase.update(PhaseEnum.INSPECTED)
            await markdown.render_stream(output.markdown)
            await chat_messages.reply_message_stream(output.comment)

            return StopEvent()
        except Exception as e:
            await chat_messages.reply_message_stream("[inspect] 予期せぬエラーが発生しました。")
            logger.error(e)
            return StopEvent()

