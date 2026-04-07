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

def register_update_local_repository(mcp: FastMCP) -> None:
    """
    update_docs tool を登録します。
    """
    @mcp.tool(
        name="UpdateLocalRepository",
        tags={"documentation"},
        timeout=30.0,
        version="1.0.0"
    )
    async def update_local_repository(
        context: Context,
        config: RootConfig = Depends(get_config)
    ) -> SimpleResponse:
        """
        FastMCPのローカルリポジトリの最新化を行うツールです。
        """
        # ユーザに最新化の最終確認する。
        response = await context.elicit(
            message=f"Repo: {config.docs.original_repo} を最新化しますか？",
            response_type=None,
        )

        # キャンセル
        if response.action != "accept":
            return SimpleResponse(success=False, message="Update cancelled")

        res = GitHelper.update_repository(config.docs.original_repo)
        if not res:
            return SimpleResponse(message="Failed to update docs")

        return SimpleResponse(
            success=True,
            message=f"{res}"
        )
