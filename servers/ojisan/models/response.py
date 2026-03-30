from pydantic import (
    BaseModel,
    Field
)

class SimpleResponse(BaseModel):
    """
    汎用的な tool 実行結果
    """
    success: bool = Field(description="Whether the tool execution was successful (true) or failed (false).", default=False)
    message: str = Field(description="A descriptive message indicating the result or error details.", default="")