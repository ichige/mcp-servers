from pydantic import (
    BaseModel,
    Field
)

class DocumentFileInfo(BaseModel):
    """
    FastMCP ドキュメントファイルのメタ情報
    """
    exists: bool = Field(description="ファイルの存在", default=False)
    outdated: bool = Field(description="更新対象可否", default=False)
    last_modified: int = Field(description="最終更新日時", default="")
    size: int = Field(description="ファイルサイズ(bytes)", default=0)
    committed_date: int = Field(description="最終コミット日時", default=0)
