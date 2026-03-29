from pydantic import BaseModel
from .docs import DocsConfig

class RootConfig(BaseModel):
    """
    設定ファイルのルート
    """
    docs: DocsConfig
