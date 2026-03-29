from pathlib import Path
from pydantic import (
    BaseModel,
    Field
)

# FastMCPの本家ドキュメント
_ORIGINAL_DOCS_DIR = Path("../.resources/fastmcp/docs").resolve()
# FastMCPの本家のリポジトリ
_ORIGINAL_REPO_DIR = Path("../.resources/fastmcp").resolve()
# FastMCPの翻訳後ドキュメント
_DOCS_DIR = Path("../docs").resolve()
# 翻訳対象の拡張子
_EXT = ["mdx"]

class DocsConfig(BaseModel):
    """
    FastMCP ドキュメントの設定
    """
    model_config = {"frozen": True}
    original: Path = Field(
        description="FastMCPの本家ドキュメント",
        default=_ORIGINAL_DOCS_DIR
    )
    original_repo: Path = Field(
        description="FastMCPの本家リポジトリ",
        default=_ORIGINAL_REPO_DIR
    )
    transrated: Path = Field(
        description="FastMCPの翻訳後ドキュメント",
        default=_DOCS_DIR
    )
    ext: list[str] = Field(
        description="翻訳対象の拡張子(mdxだけ?)",
        default=_EXT
    )
