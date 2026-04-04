from nicegui import ui
from obasan.stores import (
    chat_messages,
    input_url,
    phase,
    PhaseEnum
)
from obasan.workflows.inspection import InspectionWorkflow

def state_button():
    """
    状態確認ボタンコンポーネント
    """
    async def on_click():
        phase.update(PhaseEnum.START)
        await chat_messages.sent_message_stream("ファイルの状態を教えてくれ!")
        await chat_messages.reply_message_stream("かしこまりました。少々お待ちください…。")

        workflow = InspectionWorkflow()
        await workflow.run(url=input_url.url)

    ui.button(
        text="状態",
        icon="sym_o_info",
        color="info",
        on_click=lambda: on_click()
    ).props('size=sm outline')

