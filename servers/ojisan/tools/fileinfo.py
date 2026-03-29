from fastmcp import (
    FastMCP,
    Context,
)
from fastmcp.dependencies import Depends
from pydantic import Field
from typing import Annotated
from ojisan.configs import (
    get_config,
    RootConfig
)
from ojisan.models import DocumentFileInfo
from ojisan.utils import (
    DocsHelper,
    GitHelper
)

def register_fileinfo_tool(mcp: FastMCP):
    """
    fileinfo tool を登録します。
    """
    @mcp.tool(
        name="Fileinfo",
        tags={"documentation"},
        timeout=10.0,
        version="1.0.0"
    )
    async def fileinfo(
        path: Annotated[str, Field(description="The path segment of the tool identifier (e.g., 'servers/tools'). Do not provide the full URL; include only the portion after the base domain.")],
        context: Context,
        config: RootConfig = Depends(get_config)
    ) -> DocumentFileInfo:
        """
        Get metadata (size, last modified time, status) for a document file by its relative path.
        Checks both original and translated versions if applicable.
        """
        # 拡張子を付けてファイルを探す。
        original_path = DocsHelper.get_docs_path(config.docs.original, path, config.docs.ext)
        # 翻訳版は存在しない場合もある。
        translated_path = DocsHelper.get_docs_path(config.docs.transrated, path, config.docs.ext)
        info = DocumentFileInfo()

        # 英語版
        if original_path is not None:
            stat_o = original_path.stat()
            info.exists = True
            info.outdated = True
            info.last_modified = int(stat_o.st_mtime)
            info.size = stat_o.st_size
            info.committed_date = GitHelper.get_last_commit_time(config.docs.original_repo, original_path)
            # TODO: 英語版の最終更新日時(Git)が日本語版より新しい場合は、outdated を更新する。
            if translated_path is not None:
                stat_t = translated_path.stat()
                info.outdated = stat_o.st_mtime > stat_t.st_mtime

        return info