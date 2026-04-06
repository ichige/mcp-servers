from fastmcp import FastMCP

def register_file_translation(mcp: FastMCP):
    """
    ファイル翻訳用プロンプト
    """
    @mcp.prompt(
        version="1.0.0",
    )
    def file_translation_prompt(path: str):
        """
        ファイル翻訳で利用するプロンプトを返す
        """
        return f"""
以下のPATHに関連するFast MCPのドキュメントを日本語に翻訳してください。
- ツール実行に成功した場合は、翻訳結果(マークダウン形式)を加工せずにそのまま返してください。
- 翻訳結果のマークダウンおよびツール実行報告のコメントは、指定されたJSONスキーマに従って出力してください。
- 更新系のツールおよび非推奨のツールの利用は禁止します。

PATH: {path}
"""
