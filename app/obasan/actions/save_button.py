from nicegui import ui
from obasan.stores import phase

def save_button():
    """
    状態確認ボタンコンポーネント
    """
    ui.button(
        text="保存",
        icon="sym_o_save",
        color="positive",
    ).props(
        'size=sm outline'
    ).bind_visibility_from(
        target_object=phase,
        target_name="is_translated"
    )

