from fastmcp import FastMCP

def register_update_local_repository(mcp: FastMCP):
    """
    URL検証用プロンプトを登録
    """
    @mcp.prompt(
        version="1.0.0",
    )
    def update_local_repository_prompt():
        """
        FastMCPのローカルリポジトリの最新化で利用するプロンプトを返す
        """
        return f"""
FastMCPのローカルリポジトリを最新化をしてください。
- ツール実行に成功した場合は、実行結果(message)をマークダウンのコードブロック形式にして返してください。
- コードブロックの開始記号"```"の直後と、終了記号"```"の手前に必ず改行を入れてください。
- 実行結果のマークダウンおよびツール実行報告のコメントは、指定されたJSONスキーマに従って出力してください。
"""
