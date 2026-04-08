from llama_index.core.agent.workflow import FunctionAgent, AgentOutput
from obasan.workflows.llms import flash_lite_model
from obasan.workflows.mcp_client import get_prompt, get_tools
from obasan.workflows.structures import MarkdownOutput
from pydantic import BaseModel
from typing import Any, Optional

async def tools_agent() -> FunctionAgent:
    """
    prompt に応じた tool 実行を行わせるエージェント
    """
    tools = await get_tools()
    workflow = FunctionAgent(
        tools=tools,
        name="With Tools Agent",
        llm=flash_lite_model(
            temperature=0.0,
            deep_thinking=True
        ),
        output_cls=MarkdownOutput
    )

    return workflow

async def agent_run[T: BaseModel](
        prompt: str,
        model: type[T],
        arguments: Optional[dict[str, Any]] = None) -> T:

    """
    prompt に応じたツールを実行させる
    """
    # 要求 prompt を MCPサーバから取得
    request = await get_prompt(prompt, arguments)
    # agent prompt をMCPから取得する。
    user_msg = await get_prompt("tool_agent_prompt", {"request": request})

    # ツール実行エージェント
    workflow = await tools_agent()
    response: AgentOutput = await workflow.run(user_msg=user_msg)
    # Pydantic Model を生成できない場合は None になる模様。
    output = response.get_pydantic_model(model)
    if isinstance(output, model):
        return output
    else:
        # LLM の精度次第で、構造化されずに返ってくる場合がある。
        raise ValueError(f"Failed to parse output by {model.__name__}: {response}")
