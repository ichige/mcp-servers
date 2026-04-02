import asyncio
from pydantic import BaseModel, Field

class ChatMessages(BaseModel):
    """
    電信的なチャットメッセージ
    """
    sent: str = Field(description="発信メッセージ", default="...")
    reply: str = Field(description="応答メッセージ", default="...")

    def sent_message(self, message: str):
        """
        発信メッセージ
        """
        self.sent = message

    async def sent_message_stream(self, message: str):
        """
        発信メッセージ 疑似Stream版
        """
        self.sent = ""
        for char in message:
            current = self.sent + char
            await asyncio.sleep(0.05)
            self.sent_message(current)

    def reply_message(self, message: str):
        """
        応答メッセージ
        """
        self.reply = message

    async def reply_message_stream(self, message: str):
        """
        応答メッセージ 疑似Stream版
        """
        self.reply = ""
        for char in message:
            current = self.reply + char
            await asyncio.sleep(0.05)
            self.reply_message(current)


# Singleton
chat_messages = ChatMessages()

