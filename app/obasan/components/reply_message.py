from nicegui import ui
from obasan.stores import chat_messages

def reply_message_task(text):
    return text

def reply_message():
    """
    返答メッセージの表示
    """
    with ui.chat_message(
        name="Ojisan",
        avatar="https://robohash.org/ojisan?set=set1",
    ) :
        ui.label().bind_text(
            target_object=chat_messages,
            target_name="reply",
        )

