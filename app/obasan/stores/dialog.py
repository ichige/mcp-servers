from pydantic import BaseModel, Field

class Dialog(BaseModel):
    """
    User Elicitation 実行時のダイアログメッセージ管理
    """
    message: str = Field(description="ダイアログのラベルメッセージ", default="実行しますか？")

# singleton
dialog = Dialog()