from llama_index.core.agent.workflow import FunctionAgent, AgentOutput
from obasan.workflows.llms import flash_lite_model
from obasan.workflows.structures import UrlValidateOutput
from obasan.workflows.mcp_client import get_prompt
from pydantic import BaseModel
from typing import Optional, Any

def simple_agent() -> FunctionAgent:
    """
    URLの検証を行うエージェント
    """
    workflow = FunctionAgent(
        name="Simple Agent",
        llm=flash_lite_model(
            temperature=0.0,
            deep_thinking=True
        ),
        output_cls=UrlValidateOutput,
    )

    return workflow

async def simple_agent_run[T: BaseModel](
    prompt: str,
    model: type[T],
    arguments: Optional[dict[str, Any]] = None
) -> T:
    """
    エージェントの実行
    """
    # prompt を MCPサーバから取得
    user_msg = await get_prompt(prompt, arguments)

    # エージェントを実行
    workflow = simple_agent()
    response: AgentOutput = await workflow.run(user_msg=user_msg)
    # Pydantic Model を生成できない場合は None になる模様。
    output = response.get_pydantic_model(model)
    if isinstance(output, model):
        return output
    else:
        # LLM の精度次第で、構造化されずに返ってくる場合がある。
        raise ValueError(f"Failed to parse output by {model.__name__}: {response}")