from llama_index.core.agent.workflow import FunctionAgent, AgentOutput
from .llms import flash_lite_model
from .structures import UrlValidateOutput
from .mcp_client import get_client, GetPromptResult

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
    user_msg = ""
    async with get_client() as client:
        prompts: GetPromptResult = await client.get_prompt("url_validator_prompt", {"url": url})
        for message in prompts.messages:
            user_msg = getattr(message.content, "text", "")

    # URL検証実行
    workflow = validator_agent()
    response: AgentOutput = await workflow.run(user_msg=user_msg)
    # Pydantic Model を生成できない場合は None になる模様。
    output = response.get_pydantic_model(UrlValidateOutput)
    if isinstance(output, UrlValidateOutput):
        return output
    else:
        # LLM の精度次第で、構造化されずに返ってくる場合がある。
        raise ValueError(f"Failed to parse output: {response}")