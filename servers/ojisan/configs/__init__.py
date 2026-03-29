from .root import RootConfig
from .docs import DocsConfig

_root = RootConfig(
    docs=DocsConfig()
)

def get_config() -> RootConfig:
    """
    グローバル設定クラスを返す
    """
    return _root
