from nicegui import ui
from nicegui.elements.dialog import Dialog
from obasan.stores import dialog as dialog_store

_dialog = Dialog

def elicitation_dialog_component():
    """
    Dialog Component
    """
    global _dialog
    with ui.dialog() as dialog, ui.card():
        ui.label().bind_text_from(
            target_object=dialog_store,
            target_name="message"
        )
        with ui.row():
            ui.button(text="Yes", on_click=lambda: dialog.submit("Yes"))
            ui.button(text="No", on_click=lambda: dialog.submit("No"))
    _dialog = dialog

async def show_dialog(message: str):
    """
    ダイアログを表示して回答を待つ
    """
    global _dialog
    dialog_store.message = message

    return await _dialog # type: ignore
