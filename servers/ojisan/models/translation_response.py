from .response import SimpleResponse
from pydantic import Field
from typing import Annotated

class TranslationResponse(SimpleResponse):
    translated_text: Annotated[str, Field(description="翻訳結果")] = ""