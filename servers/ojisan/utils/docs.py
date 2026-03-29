import logging
from fastmcp.dependencies import CurrentContext
from pathlib import Path
from typing import Annotated

logger = logging.getLogger(__name__)

class DocsHelper:
    """
    FastMCP document を取り扱う共通ヘルパー
    """
    @staticmethod
    def get_docs_path(
        base_path: Annotated[Path, "ドキュメントが配置されているベースのパス"],
        path: Annotated[str, "ドキュメントのファイル名となるパス名"],
        ext: Annotated[list[str], "拡張子のリスト"]
    ) -> Path | None:
        """
        指定された条件で拡張子を持つファイルを1つ見つけて返す。
        存在しない場合は None を返す。
        """
        ctx = CurrentContext()
        # 拡張子を付けてファイルを探す。
        for item in ext:
            _path = (base_path / f"{path.strip('/')}.{item}").resolve()
            logger.debug(f"docs path resolved: {_path}")
            if _path.exists():
                return _path

        return None