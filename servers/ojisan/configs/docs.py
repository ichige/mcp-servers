from pathlib import Path
from pydantic import BaseModel

# FastMCPの本家ドキュメント
_ORIGINAL_DOCS_DIR = Path("../.resources/fastmcp/docs").resolve()
# FastMCPの翻訳後ドキュメント
_DOCS_DIR = Path("../docs").resolve()
# 翻訳対象の拡張子
_EXT = ["mdx"]

class DocsConfig(BaseModel):
    """
    FastMCP ドキュメントの設定
    """
    original: Path = _ORIGINAL_DOCS_DIR
    docs: Path = _DOCS_DIR
    ext: list[str] = _EXT
