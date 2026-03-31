from nicegui import ui
from obasan.stores import chat_messages

@ui.refreshable
def sent_message():
    """
    発信メッセージの表示
    """
    ui.chat_message(
        text=chat_messages.sent,
        name="Obasan",
        avatar="https://robohash.org/obasan?set=set3",
    ).props("sent")