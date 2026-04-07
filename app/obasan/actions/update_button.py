from nicegui import ui
from obasan.stores import chat_messages, input_url
from obasan.workflows import run_workflow, ActionNameEnum

def update_button():
    """
    リポジトリ更新ボタンコンポーネント
    """
    async def on_click():

        await chat_messages.sent_message_stream("FastMCPのリポジトリを最新化して!")
        await chat_messages.reply_message_stream("かしこまりました。少々お待ちください…。")
        # 最新化を実行
        await run_workflow(action_name=ActionNameEnum.UPDATE)

    ui.button(
        text="最新化",
        icon="sym_o_autorenew",
        color="accent",
        on_click=lambda: on_click()
    ).props(
        "size=sm outline"
    )
