from nicegui import ui
from obasan.stores import input_url

def input_url_component():
    """
    URL入力コンポーネント
    """
    # URL Input
    component = ui.input(
        label="URL",
        placeholder="https://gofastmcp.com/getting-started/welcome",
        on_change=lambda e: input_url.update(e.value)
    ).props("clearable outlined dense hint=FastMCPのURLを入力").classes("")
    # icon
    with component.add_slot('before'):
        ui.icon(
            name='sym_o_search',
            size='xs',
            color='accent'
        )