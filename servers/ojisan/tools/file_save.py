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
from ojisan.models import SimpleResponse
from ojisan.utils import (
    DocsHelper
)

def register_file_save(mcp: FastMCP) -> None:
    """
    file_save tool を登録します。
    """
    @mcp.tool(
        name="FileSave",
        tags={"documentation"},
        timeout=10.0,
        version="1.0.0"
    )
    async def file_save(
            path: Annotated[str, Field(description="The relative path to save the document (e.g., 'guides/getting-started')")],
            content: Annotated[str, Field(description="The content of the document to be saved")],
            ext: Annotated[str, Field(description="The file extension (default: 'mdx')", default="mdx")],
            context: Context,
            config: RootConfig = Depends(get_config)
    ) -> SimpleResponse:
        """
        Saves the translated content to the specified path.
        Automatically creates the necessary directories if they do not exist.
        """
        # 拡張子を付けてファイルを探す。
        original_path = DocsHelper.get_docs_path(config.docs.original, path, config.docs.ext)
        # 翻訳元が見つからない場合は、保存対象としない。
        if original_path is None:
            return SimpleResponse(success=False, message="Original document not found")

        # 保存先パスを生成
        save_path = DocsHelper.create_docs_path(config.docs.transrated, path, ext)
        # 保存先が不正なら保存対象としない。
        if save_path is None:
            return SimpleResponse(success=False, message="Invalid save path")
        # ファイルを非同期で保存する。
        res = await DocsHelper.save_docs(save_path, content)
        if not res:
            return SimpleResponse(success=False, message="Failed to save file")

        # 保存成功
        return SimpleResponse(success=True, message="File saved successfully")