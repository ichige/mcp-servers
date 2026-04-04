from pydantic import BaseModel, Field
from enum import Enum

class PhaseEnum(str, Enum):
    # 準備OK
    STANDBY = "standby"
    # 処理開始
    START = "start"
    # 処理中
    PENDING = "pending"
    # 翻訳完了
    TRANSLATED = "translated"
    # 検査完了
    INSPECTED = "inspected"


class Phase(BaseModel):
    """
    翻訳処理のフェーズを管理するモデル
    """
    state: PhaseEnum = Field(description="現在の状態を示す文字列", default="standby")

    def update(self, state: PhaseEnum) -> None:
        """
        ステート変更
        """
        self.state = state

    @property
    def is_standby(self) -> bool:
        """
        処理開始準備
        """
        return self.state == PhaseEnum.STANDBY

    @property
    def is_start(self) -> bool:
        """
        処理開始
        """
        return self.state == PhaseEnum.START

    @property
    def is_pending(self) -> bool:
        """
        MCP問い合わせ中
        """
        return self.state == PhaseEnum.PENDING

    @property
    def is_translated(self) -> bool:
        """
        翻訳完了
        """
        return self.state == PhaseEnum.TRANSLATED

    @property
    def is_inspected(self) -> bool:
        """
        情報取得
        """
        return self.state == PhaseEnum.INSPECTED

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
        return self.state in [PhaseEnum.TRANSLATED, PhaseEnum.INSPECTED]

# singleton
phase = Phase()