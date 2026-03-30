from fastmcp import (
    FastMCP,
    Context,
)
from fastmcp.dependencies import Depends
from ojisan.configs import (
    get_config,
    RootConfig
)
from ojisan.models import SimpleResponse
from ojisan.utils import (
    GitHelper
)

def register_update_docs(mcp: FastMCP) -> None:
    """
    update_docs tool を登録します。
    """
    @mcp.tool(
        name="UpdateDocs",
        tags={"documentation"},
        timeout=30.0,
        version="1.0.0"
    )
    def update_docs(
        context: Context,
        config: RootConfig = Depends(get_config)
    ) -> SimpleResponse:
        """
        Updates the local documentation repository by pulling the latest changes from the remote server.
        """
        res = GitHelper.update_repository(config.docs.original_repo)
        if not res:
            return SimpleResponse(message="Failed to update docs")

        return SimpleResponse(
            success=True,
            message=f"Docs updated successfully: {res}"
        )
