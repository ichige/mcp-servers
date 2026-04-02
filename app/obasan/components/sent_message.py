from nicegui import ui
from obasan.stores import chat_messages

@ui.refreshable
def sent_message():
    """
    発信メッセージの表示
    """
    with ui.chat_message(
        name="Obasan",
        avatar="https://robohash.org/obasan?set=set3",
    ).props("sent"):
        ui.label().bind_text(
            target_object=chat_messages,
            target_name="sent",
        )