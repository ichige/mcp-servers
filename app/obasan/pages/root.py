from nicegui import ui
from obasan.layouts import base_layout
from obasan.actions import (
    state_button,
    save_button,
    translate_button,
    reset_button
)
from obasan.components import (
    reply_message,
    sent_message,
    server_notification,
    markdown_content,
    input_url_component
)
from obasan.stores import phase

def register_root_page():
    """
    root page の登録
    """

    @ui.page("/")
    def root_page():
        # Input and Chat Message
        with ui.grid(columns=2).classes("w-full"):
            # Input Card
            with ui.card().classes(""):
                # w-full を指定しないと幅が狭まる
                with ui.card_section().classes("w-full"):
                    # URL Input
                    input_url_component()

                ui.separator()
                # Actions w-full を指定しないと幅が狭まる
                with ui.card_actions().props("align=right").classes("w-full"):
                    # 情報
                    state_button()
                    # 翻訳
                    translate_button()

            # Chat Message Card
            with ui.card().classes(""):
                with ui.card_section().classes("w-full"):
                    # Obasan(ユーザ)からの指令
                    sent_message()
                    # Ojisan(LLM/MCP)からの返答
                    reply_message()
                    # server status
                    server_notification()

        # マークダウンコンテンツ表示
        with ui.card().classes("") as content_card:

            content_card.bind_visibility_from(
                target_object=phase,
                target_name="view_content_card"
            )

            with ui.card_section().classes("w-full"):
                markdown_content()
            ui.separator()
            with ui.card_actions().classes("w-full"):
                # 保存
                save_button()
                # リセット
                reset_button()

        # 共通レイアウト
        base_layout()