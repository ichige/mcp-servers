from pydantic import (
    BaseModel,
    Field
)
from typing import Optional

class DocumentFileInfo(BaseModel):
    """
    FastMCP ドキュメントファイルのメタ情報
    """
    exists: bool = Field(description="ファイルの存在", default=False)
    outdated: bool = Field(description="ファイルの更新対象可否", default=False)
    last_modified: int = Field(description="最終更新日時(UNIX TIMESTAMP)", default=0)
    size: int = Field(description="ファイルサイズ(bytes)", default=0)
    committed_date: Optional[int] = Field(description="最終コミット日時(UNIX TIMESTAMP)", default=None)
