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

def register_file_inspector_tool(mcp: FastMCP):
    """
    fileinfo tool を登録します。
    """
    @mcp.tool(
        name="FileInspector",
        tags={"documentation"},
        timeout=10.0,
        version="1.0.0"
    )
    async def file_inspector(
        path: Annotated[str, Field(description="FastMCPのドキュメントファイルの識別子となる PATH。例) /path/to/file")],
        context: Context,
        config: RootConfig = Depends(get_config)
    ) -> DocumentFileInfo:
        """
        指定されたPATHに関連するFastMCPのドキュメントファイルのメタデータ(更新日時やサイズなど)を取得できます。
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