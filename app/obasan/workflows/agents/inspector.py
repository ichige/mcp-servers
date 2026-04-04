from llama_index.core.agent.workflow import FunctionAgent, AgentOutput
from obasan.workflows.llms import flash_lite_model
from obasan.workflows.mcp_client import get_prompt, get_tools
from obasan.workflows.structures import MarkdownOutput

async def inspector_agent() -> FunctionAgent:
    """
    URLの検証を行うエージェント
    """
    tools = await get_tools()
    workflow = FunctionAgent(
        tools=tools,
        name="Inspector",
        llm=flash_lite_model(
            temperature=0.0,
            deep_thinking=True
        ),
        output_cls=MarkdownOutput,
    )

    return workflow

async def inspection_run(path: str) -> MarkdownOutput:
    """
    PATHに関連するドキュメントの検査実行
    """
    # 要求 prompt を MCPサーバから取得
    request = await get_prompt("file_inspect_prompt", {"path": path})
    # agent prompt をMCPから取得する。
    user_msg = await get_prompt("tool_agent_prompt", {"request": request})

    # URL検証実行
    workflow = await inspector_agent()
    response: AgentOutput = await workflow.run(user_msg=user_msg)
    # Pydantic Model を生成できない場合は None になる模様。
    output = response.get_pydantic_model(MarkdownOutput)
    if isinstance(output, MarkdownOutput):
        return output
    else:
        # LLM の精度次第で、構造化されずに返ってくる場合がある。
        raise ValueError(f"Failed to parse output by inspection: {response}")
