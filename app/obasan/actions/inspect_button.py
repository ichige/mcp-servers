from nicegui import ui
from obasan.stores import chat_messages, input_url
from obasan.workflows import run_workflow, ActionNameEnum

def inspect_button():
    """
    ファイル検証ボタンコンポーネント
    """
    async def on_click():

        await chat_messages.sent_message_stream("ファイルの状態を教えてくれ!")
        await chat_messages.reply_message_stream("かしこまりました。少々お待ちください…。")
        # ファイルの検証を実行
        await run_workflow(action_name=ActionNameEnum.INSPECT)

    ui.button(
        text="状態",
        icon="sym_o_info",
        color="info",
        on_click=lambda: on_click()
    ).props(
        "size=sm outline"
    ).bind_enabled_from(
        target_object=input_url,
        target_name="url"
    )

