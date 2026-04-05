from llama_index.core.tools import FunctionTool
from obasan.workflows.mcp_client import get_mcp_client
from obasan.workflows.structures import TranslationResponse
from typing import Annotated
from pydantic import Field


async def document_translator_tool(
        path: Annotated[str, Field(description="FastMCPのドキュメントファイルの識別子となる PATH。例) /path/to/file")],
    ) -> TranslationResponse:
    """
    FastMCP が提供している _DocumentTranslator をラップしたツール。
    Google GenAI が sampling に未対応なため、FastMCP Clientで代替します。
    レスポンス型は _DocumentTranslator と合わせる必要があるので、ややメンテナンスが面倒かもしれない。
    """
    async with get_mcp_client() as client:
        response = await client.call_tool("_DocumentTranslator", {"path": path })
        return response.data

def document_translator_tool_spec():
    return FunctionTool.from_defaults(
        fn=document_translator_tool,
        name="document_translator",
        description="指定されたPATHに関連するFastMCPのドキュメントファイルを英語から日本語に翻訳します。"
    )