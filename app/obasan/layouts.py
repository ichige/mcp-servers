from nicegui import ui

def base_layout():
    """
    共通レイアウト
    """
    # dark mode
    ui.dark_mode().enable()

    # header
    with ui.header():
        ui.button(
            icon="sym_o_menu",
            on_click=lambda: left_drawer.toggle()
        ).props('size=sm flat text-color=white')
        with ui.avatar(size='md', color='black'):
            ui.image('https://robohash.org/obasan?set=set3')
        ui.label("Obasan Translator").classes('text-xl font-bold')

    # left drawer
    with ui.left_drawer() as left_drawer:
        with ui.row().classes('items-center gap-2'):
            ui.icon('sym_o_settings')
            ui.label("settings").classes('text-lg')