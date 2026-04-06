import os
from dotenv import load_dotenv
from fastmcp import FastMCP
from fastmcp.client.sampling.handlers.google_genai import GoogleGenaiSamplingHandler
from ojisan.resources import register_resources
from ojisan.tools import register_tools
from ojisan.prompts import register_prompts

load_dotenv()

mcp = FastMCP(
    name="FastMCP Server",
    # 保険的な設定なので、LLMの細かい制御が出来ない。
    sampling_handler=GoogleGenaiSamplingHandler(
        default_model=os.getenv("MODEL_PREFERENCE", "gemini-3.1-flash-lite-preview")
    ),
    # fallback に指定すると、非対応クライアントであれば、自前のLLMを使う。
    sampling_handler_behavior="fallback",
)

# Resources
register_resources(mcp)
# Tools
register_tools(mcp)
# Prompts
register_prompts(mcp)

@mcp.tool
def great(name: str) -> str:
    """
    Greets the user
    """
    return f"Hello {name}!"
