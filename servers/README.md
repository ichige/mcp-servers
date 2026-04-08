# MCP Server

## Environment

### python 環境の構築

現時点での最新版である python 3.14 を利用しました。

```bash
cd servers
# 初期化
uv init
# パッケージのインストール
uv add fastmcp \
  aiofiles \
  GitPython \
  pydantic \
  google-genai
```

デバッグは MCP Inspector を使う。

- [MCP Inspector](https://github.com/modelcontextprotocol/inspector)

```bash
cd servers
npx @modelcontextprotocol/inspector uv run fastmcp run starter.py:mcp
```

## Run

```bash
cd servers
uv run fastmcp run starter.py:mcp
uv run fastmcp run starter.py:mcp --transport http --port 8000
```