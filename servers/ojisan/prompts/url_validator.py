from fastmcp import FastMCP

def register_url_validator(mcp: FastMCP):
    """
    URL検証用プロンプトを登録
    """
    @mcp.prompt(
        version="1.0.0",
    )
    def url_validator_prompt(url: str):
        """
        URL検証で利用するプロンプトを返す
        """
        return f"""
あなたはURL Parserです。
- 入力されたURLが許可されているかどうかを判定してください。
- 不許可の場合のその理由も説明してください。
- 入力されたURLからパス部分のみを抽出し、指定されたJSONスキーマに従って出力してください。
- パスが不明な場合は "/" を返してください。
- 回答にはJSON以外のテキスト（挨拶や説明文など）を一切含めず、純粋なJSONのみを返してください。

許可ホスト:
- gofastmcp.com
- localhost

対象URL: {url}
"""
