from nicegui import ui
from obasan.stores import (
    chat_messages,
    input_url,
    markdown,
    phase,
    PhaseEnum
)

def reset_button():
    """
    リセットボタン
    """
    def on_click():
        phase.update(PhaseEnum.STANDBY)
        chat_messages.sent_message("...")
        chat_messages.reply_message("...")
        markdown.render("")
        input_url.reset()

    ui.button(
        text="リセット",
        icon="sym_o_reset_focus",
        color="danger",
        on_click=lambda: on_click()
    ).props('size=sm outline')