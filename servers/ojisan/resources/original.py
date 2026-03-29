import aiofiles
from fastmcp import (
    FastMCP,
    Context,
)
from fastmcp.dependencies import Depends
from fastmcp.resources import (
    ResourceContent,
    ResourceResult,
)
from pathlib import Path
from ojisan.configs import (
    get_config,
    RootConfig
)

def register_original_resource(mcp: FastMCP):
    """
    オリジナル版のドキュメント情報を取り扱うリソースを登録します。
    """
    @mcp.resource(
        uri="resource://original/{path}",
        name="OriginalResource",
        description="FastMCP Original Documentation",
        mime_type="text/markdown",
        tags={"documentation"},
        version="1.0.0"
    )
    async def get_original_resource(
            path: str,
            context: Context,
            config: RootConfig = Depends(get_config)
    ) -> ResourceResult:
        """
        オリジナル版のドキュメント情報を検索して返す。
        """
        file_path: Path | None = None
        # 拡張子を付けてファイルを探す。
        for ext in config.docs.ext:
            _path = (config.docs.original / f"{path.strip('/')}.{ext}").resolve()
            await context.debug(f"Searching original resource: {_path}")
            if _path.exists():
                file_path = _path
                break

        # ファイルが見つからない
        if file_path is None:
            raise FileNotFoundError(
                f"Original resource not found: {file_path}"
            )

        # ファイルが規定のディレクトリに含まれているかどうかを確認する。
        if not file_path.is_relative_to(config.docs.original):
            raise ValueError(
                f"Original resource path is not within the original directory: {path}"
            )

        #
        await context.info(f"Loading original resource: {file_path}")
        async with aiofiles.open(file_path, "r") as f:
            content = await f.read()
            return ResourceResult(
                contents=[
                    ResourceContent(content=content,mime_type="text/markdown")
                ]
            )