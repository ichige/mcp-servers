from nicegui import ui
from obasan.stores import phase, chat_messages
from obasan.workflows import run_workflow, ActionNameEnum

def save_button():
    """
    保存ボタンコンポーネント
    """
    async def on_click():
        await chat_messages.sent_message_stream("ファイルを保存してくれ!")
        await chat_messages.reply_message_stream("かしこまりました。少々お待ちください…。")
        # ファイルの翻訳を実行
        await run_workflow(action_name=ActionNameEnum.SAVE)

    ui.button(
        text="保存",
        icon="sym_o_save",
        color="positive",
        on_click=lambda: on_click()
    ).props(
        'size=sm outline'
    ).bind_visibility_from(
        target_object=phase,
        target_name="is_translated"
    )

