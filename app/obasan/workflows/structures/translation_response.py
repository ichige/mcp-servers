from pydantic import BaseModel, Field
from typing import Annotated

class TranslationResponse(BaseModel):
    success: bool = Field(description="Whether the tool execution was successful (true) or failed (false).", default=False)
    message: str = Field(description="A descriptive message indicating the result or error details.", default="")
    translated_text: Annotated[str, Field(description="翻訳結果")] = ""