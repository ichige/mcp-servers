import os
from fastmcp import (
    FastMCP,
    Context,
)
from fastmcp.dependencies import Depends
from pydantic import Field
from typing import Annotated
from ojisan.configs import (
    get_config,
    RootConfig
)
from ojisan.models import TranslationResponse
from ojisan.utils import (
    DocsHelper
)

def register_document_translator_tool(mcp: FastMCP):
    """
    fileinfo tool を登録します。
    """
    @mcp.tool(
        name="DocumentTranslator",
        tags={"documentation"},
        timeout=600.0,
        version="1.0.0"
    )
    async def file_inspector(
        path: Annotated[str, Field(description="FastMCPのドキュメントファイルの識別子となる PATH。例) /path/to/file")],
        context: Context,
        config: RootConfig = Depends(get_config)
    ) -> TranslationResponse:
        """
        指定されたPATHに関連するFastMCPのドキュメントファイルを英語から日本語に翻訳します。
        """
        # 拡張子を付けてファイルを探す。
        original_path = DocsHelper.get_docs_path(config.docs.original, path, config.docs.ext)

        # 英語版が存在しない場合はエラー
        if original_path is None:
            return TranslationResponse(success=False, message="Original document not found")

        system_prompt = """
あなたは、Model Context Protocol (MCP) および Python フレームワーク「FastMCP」に精通した、シニア・テクニカル・ライター兼フルスタックエンジニアです。
ユーザーが提供する MDX 形式の技術ドキュメントを、以下のガイドラインに従って正確かつ自然な日本語に翻訳してください。

### 1. MDX 構造の完全保護
- **Frontmatter**: `---` で囲まれたメタデータ部分の「キー」は変更しないでください。`title` や `description` の「値」のみを翻訳してください。
- **JSX/React Components**: `<Component />`、`<Steps>`、`<Tabs>` などのタグ名、およびそのプロパティ名（例: `header="Title"` の `header` 部分）は一切変更せず、タグで囲まれたコンテンツのみを翻訳してください。
- **Import 文**: ファイル冒頭の `import` 文は一切変更せず、そのまま残してください。

### 2. 技術用語の取り扱い
- **未翻訳維持**: 以下の用語は、文脈上必要な場合を除き、英語のまま（またはカタカナ表記）で維持してください。
  - FastMCP, MCP, Model Context Protocol
  - Tool, Resource, Prompt
  - Server, Client, Transport (SSE, STDIO)
  - Decorator, Argument, Return type
- **コード内**: コードブロック内のロジック、変数名、関数名は一切変更しないでください。コメント部分のみを日本語に翻訳してください。

### 3. スタイル・トーン
- **文体**: 丁寧な技術ドキュメントの口調（「〜です」「〜ます」）を採用してください。
- **明瞭性**: エンジニアが直感的に理解できるよう、冗長な表現を避け、簡潔で正確な表現を選んでください。

### 4. 特殊記法の維持
- `:::tip` や `:::info` などのアドモニション（注釈）記法、および Markdown のリンク形式 `[text](url)` の URL 部分は変更しないでください。

### 5. 禁止事項
- 翻訳結果全体を ```mdx や ``` などのコードブロックで囲わないでください。
        """

        text = await DocsHelper.read_docs(original_path)
        message = f"""
下記の[START]から[END]までのドキュメントを翻訳して下さい。
[START]

{text}

[END]
                """
        try:
            result = await context.sample(
                messages=[message],
                model_preferences=[os.environ.get("MODEL_PREFERENCE", "gemini-3.1-flash-lite-preview")],
                system_prompt=system_prompt,
                temperature=0.1,
                max_tokens=100000,
            )

            return TranslationResponse(success=True, message="OK", translated_text=str(result.text))
        except Exception as e:
            return TranslationResponse(success=False, message=str(e))

