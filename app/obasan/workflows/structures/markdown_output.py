from pydantic import BaseModel, Field

class MarkdownOutput(BaseModel):
    """
    マークダウン出力構造
    """
    markdown: str = Field(description="マークダウン形式の回答")
    comment: str = Field(description="ツール実行結果の報告。例) 回答お待たせしました。")
