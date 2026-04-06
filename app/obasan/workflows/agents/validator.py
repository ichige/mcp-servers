from llama_index.core.agent.workflow import FunctionAgent, AgentOutput
from obasan.workflows.llms import flash_lite_model
from obasan.workflows.structures import UrlValidateOutput
from obasan.workflows.mcp_client import get_prompt

def validator_agent() -> FunctionAgent:
    """
    URLの検証を行うエージェント
    """
    workflow = FunctionAgent(
        name="URL Validator",
        llm=flash_lite_model(
            temperature=0.0,
            deep_thinking=True
        ),
        output_cls=UrlValidateOutput,
    )

    return workflow

async def valid_url_run(url: str) -> UrlValidateOutput:
    """
    URL検証の実行
    """
    # prompt を MCPサーバから取得
    user_msg = await get_prompt("url_validator_prompt", {"url": url})

    # URL検証実行
    workflow = validator_agent()
    response: AgentOutput = await workflow.run(user_msg=user_msg)
    # Pydantic Model を生成できない場合は None になる模様。
    output = response.get_pydantic_model(UrlValidateOutput)
    if isinstance(output, UrlValidateOutput):
        return output
    else:
        # LLM の精度次第で、構造化されずに返ってくる場合がある。
        raise ValueError(f"Failed to parse output by valid url: {response}")