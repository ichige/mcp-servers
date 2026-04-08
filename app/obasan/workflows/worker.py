from llama_index.core import set_global_handler
from llama_index.core.workflow import Workflow,step
from llama_index.core.workflow.events import StopEvent
from logging import getLogger
from .events import (
    ActionEvent,
    UrlInputEvent,
    SaveEvent,
    UpdateRepoEvent,
    InspectionEvent,
    TranslationEvent,
    ActionNameEnum
)
from obasan.stores import (
    phase,
    chat_messages,
    markdown,
    input_url,
    PhaseEnum
)

from .agents import agent_run, simple_agent_run
from .structures import MarkdownOutput, UrlValidateOutput
from .mcp_client import direct_call_tool

logger = getLogger(__name__)

class AppWorkflow(Workflow):
    """
    翻訳アプリの統合ワークフロー
    各ステップをMixinで登録
    """

    @step
    async def routing(self, ev: ActionEvent) -> (
        UrlInputEvent |
        StopEvent |
        SaveEvent |
        UpdateRepoEvent
    ):
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

            # 保存
            case ActionNameEnum.SAVE:
                return SaveEvent(
                    path=input_url.path,
                    content=markdown.text
                )

            # リポジトリ更新
            case ActionNameEnum.UPDATE:
                return UpdateRepoEvent(
                    action_name=ev.action_name,
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
            output = await simple_agent_run(
                prompt=ev.prompt,
                arguments=ev.arguments(),
                model=UrlValidateOutput
            )
            # 検証エラー
            if not output.is_valid:
                await chat_messages.reply_message_stream(output.reason)
                return StopEvent()

            # path を設定
            input_url.path = output.path

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
            output = await agent_run(
                prompt=ev.prompt,
                arguments=ev.arguments(),
                model=MarkdownOutput
            )
            phase.update(PhaseEnum.INSPECTED)
            await markdown.render_stream(output.markdown)
            await chat_messages.reply_message_stream(output.comment)

            return StopEvent()
        except Exception as e:
            await chat_messages.reply_message_stream("[inspect] 予期せぬエラーが発生しました。")
            logger.error(e)
            return StopEvent()

    @step
    async def save(self, ev: SaveEvent) -> StopEvent:
        """
        翻訳結果を保存する
        翻訳結果をLLMに渡してツールを実行すると、意味もなくトークンを無駄使いするため、ここでは直接ツール実行を行う。
        """
        try:

            result = await direct_call_tool(
                name="FileSave",
                arguments={
                    "path": ev.path,
                    "content": ev.content
                }
            )
            phase.update(PhaseEnum.SAVED)
            # 成功・失敗に関わらずメッセージを表示。
            await chat_messages.reply_message_stream(result.get("message", "unknown"))

        except Exception as e:
            await chat_messages.reply_message_stream(f"[{self.save.__name__}] 予期せぬエラーが発生しました。")
            logger.error(e)

        return StopEvent()

    @step
    async def translate(self, ev: TranslationEvent) -> StopEvent:
        """
        PATH を元にファイルを翻訳するツールをLLMに実行させる
        """
        try:
            output = await agent_run(
                prompt=ev.prompt,
                arguments=ev.arguments(),
                model=MarkdownOutput
            )
            phase.update(PhaseEnum.TRANSLATED)
            # 長文で Stream 描画は重いので、一撃描画で。
            markdown.render(output.markdown)
            await chat_messages.reply_message_stream(output.comment)

            return StopEvent()
        except Exception as e:
            await chat_messages.reply_message_stream("[translate] 予期せぬエラーが発生しました。")
            logger.error(e)
            return StopEvent()

    @step
    async def update(self, ev: UpdateRepoEvent) -> StopEvent:
        """
        FastMCP のローカルリポジトリを更新させる
        """
        try:
            output = await agent_run(
                prompt=ev.prompt,
                model=MarkdownOutput
            )
            phase.update(PhaseEnum.UPDATED)
            await markdown.render_stream(output.markdown)
            await chat_messages.reply_message_stream(output.comment)

            return StopEvent()
        except Exception as e:
            await chat_messages.reply_message_stream(f"[{self.update.__name__}] 予期せぬエラーが発生しました。")
            logger.error(e)
            return StopEvent()

async def run_workflow(action_name: ActionNameEnum) -> None:
    """
    Workflow Run
    """
    set_global_handler("simple")
    phase.update(PhaseEnum.START)
    workflow = AppWorkflow(timeout=600.0)

    await workflow.run(
        start_event=ActionEvent(
            action_name=action_name,
            url=input_url.url
        ),

    )
