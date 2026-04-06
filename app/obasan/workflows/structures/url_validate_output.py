from pydantic import BaseModel, Field
from typing import Optional

class UrlValidateOutput(BaseModel):
    """
    URL検証出力構造
    """
    path: str = Field(description="URLのパス。例) /path/to/file")
    is_valid: bool = Field(description="許可されたURLかどうかの判定値")
    reason: Optional[str] = Field(description="不許可の説明文", default=None)
