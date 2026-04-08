import os
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
from datetime import datetime, timedelta, timezone

def register_date_convertor_by_unix_tool(mcp: FastMCP):
    """
    fileinfo tool を登録します。
    """
    @mcp.tool(
        name="DateConvertorByUnix",
        tags={"documentation"},
        timeout=600.0,
        version="1.0.0"
    )
    async def file_inspector(
        timestamp: Annotated[float, Field(description="UNIX Timestamp")],
        context: Context,
        config: RootConfig = Depends(get_config)
    ) -> SimpleResponse:
        """
        UNIX Timestamp を日本時間 YYYY/mm/dd HH:MM:SS 形式に変換します。
        """
        JST = timezone(timedelta(hours=9), "JST")
        dt_jst = datetime.fromtimestamp(timestamp, tz=JST)
        return SimpleResponse(success=True, message=dt_jst.strftime('%Y-%m-%d %H:%M:%S'))

