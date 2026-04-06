from fastmcp import FastMCP

def register_file_inspect(mcp: FastMCP):
    """
    ファイル検証用プロンプト
    """
    @mcp.prompt(
        version="1.0.0",
    )
    def file_inspect_prompt(path: str):
        """
        ファイル検証で利用するプロンプトを返す
        """
        return f"""
以下のPATHに関連するFast MCPのドキュメントのメタデータ(更新日時やサイズなど)を取得してください。
- 検査結果の内容(メタデータ)を分かりやすくマークダウンのテーブル形式で報告してください。
- UNIX TIMESTAMP形式の項目は、日本時間に修正してください。例) 2026/04/4 12:00:00
- ファイルサイズは理解しやすいように適切な単位に変換して下さい。例) KB
- マークダウン形式の回答およびツール実行報告のコメントは、指定されたJSONスキーマに従って出力してください。
- 更新系のツールの利用は禁止します。

PATH: {path}
"""
