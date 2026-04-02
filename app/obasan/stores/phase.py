from pydantic import BaseModel, Field
from typing import Literal

class Phase(BaseModel):
    """
    翻訳処理のフェーズを管理するモデル
    """
    state: Literal["standby", "start", "pending", "translated", "information"] = Field(description="現在の状態を示す文字列", default="standby")

    def update(self, state: Literal["standby", "start", "pending", "translated", "information"]) -> None:
        """
        ステート変更
        """
        self.state = state

    @property
    def is_standby(self) -> bool:
        """
        処理開始準備
        """
        return self.state == "standby"

    @property
    def is_start(self) -> bool:
        """
        処理開始
        """
        return self.state == "start"

    @property
    def is_pending(self) -> bool:
        """
        MCP問い合わせ中
        """
        return self.state == "pending"

    @property
    def is_translated(self) -> bool:
        """
        翻訳完了
        """
        return self.state == "translated"

    @property
    def is_information(self) -> bool:
        """
        情報取得
        """
        return self.state == "information"

    @property
    def state_message(self) -> str:
        """
        現在のステートをメッセージで返す
        """
        return f"Phase: {self.state}"

    @property
    def view_content_card(self) -> bool:
        """
        コンテンツ表示状態の制御
        """
        return self.state in ["pending", "translated", "information"]

# singleton
phase = Phase()