from llama_index.core import set_global_handler
from llama_index.core.workflow import (
    Workflow,
    step
)
from llama_index.core.workflow.events import (
    StartEvent,
    StopEvent
)
from .events import (
    UrlInputEvent
)
from obasan.stores import (
    phase
)
from .agents import valid_url_run

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
    async def validate(self, ev: UrlInputEvent) -> StopEvent:
        """
        入力されたURLの正当性をLLMに検証させる
        """
        try:
            output = await valid_url_run(ev.url)
            # TODO: 次のステップへ(ファイル情報取得tool)
            return StopEvent(result=output.model_dump())
        except Exception as e:
            return StopEvent(result=str(e))
