import aiofiles
import logging
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
        # 拡張子を付けてファイルを探す。
        for item in ext:
            _path = (base_path / f"{path.strip('/')}.{item}").resolve()
            logger.debug(f"docs path resolved: {_path}")
            if _path.exists():
                return _path

        return None

    @staticmethod
    def create_docs_path(
        base_path: Annotated[Path, "ドキュメントが配置されているベースのパス"],
        path: Annotated[str, "ドキュメントのファイル名となるパス名"],
        ext: Annotated[str, "拡張子"] = "mdx"
    ) -> Path | None:
        """
        指定された条件でパスを生成する。
        生成したパスがベースパスに含まれない場合は None を返す。
        """
        _path = (base_path / f"{path.strip('/')}.{ext}").resolve()
        if _path.is_relative_to(base_path):
            return _path

        return None

    @staticmethod
    async def save_docs(path: Path, content: str) -> bool:
        """
        指定されたファイルパスに非同期でデータを保存する
        """
        try:
            # ディレクトリを作ってから保存を試みる。
            path.parent.mkdir(parents=True, exist_ok=True)
            async with aiofiles.open(path, "w") as f:
                await f.write(content)
        except Exception as e:
            logger.error(f"Failed to save docs: {e}")
            return False

        return True
