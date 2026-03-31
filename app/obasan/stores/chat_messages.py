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

    def reply_message(self, message: str):
        """
        応答メッセージ
        """
        self.reply = message

# Singleton
chat_messages = ChatMessages()

