from nicegui import ui
from obasan.stores import (
    chat_messages,
    phase
)
from ._stab import do_translate

def translate_button():
    """
    状態確認ボタンコンポーネント
    """
    async def on_click():
        phase.update("start")
        await chat_messages.sent_message_stream("ファイルを翻訳してくれ!")
        await chat_messages.reply_message_stream("かしこまりました。少々お待ちください…。")
        phase.update("pending")
        # TODO: 翻訳なり
        await do_translate()

    ui.button(
        text="翻訳",
        icon="sym_o_translate",
        color="positive",
        on_click=lambda: on_click()
    ).props('size=sm outline')

