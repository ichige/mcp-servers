from nicegui import ui
from obasan.stores import (
    chat_messages,
    input_url,
    phase,
    PhaseEnum
)
from obasan.workflows import TranslationWorkflow

def translate_button():
    """
    状態確認ボタンコンポーネント
    """
    async def on_click():
        phase.update(PhaseEnum.START)
        await chat_messages.sent_message_stream("ファイルを翻訳してくれ!")
        await chat_messages.reply_message_stream("かしこまりました。少々お待ちください…。")

        workflow = TranslationWorkflow(timeout=360.0)
        await workflow.run(url=input_url.url)

    ui.button(
        text="翻訳",
        icon="sym_o_translate",
        color="positive",
        on_click=lambda: on_click()
    ).props('size=sm outline')

