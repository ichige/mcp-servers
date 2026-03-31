from nicegui import ui
from obasan.stores import chat_messages
from .sent_message import sent_message

def state_button():
    """
    状態確認ボタンコンポーネント
    """
    def on_click():
        chat_messages.sent_message("ファイルの状態を教えて!")
        sent_message.refresh()

    ui.button(
        text="状態",
        icon="sym_o_info",
        color="info",
        on_click=lambda: on_click()
    ).props('size=sm outline')

