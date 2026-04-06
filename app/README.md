# NiceGUI

- [NiceGUI](https://nicegui.io/)

## Environment

```bash
cd app
# uv update
uv self update
# 初期化
uv init
# パッケージのインストール
uv add nicegui \
  pydantic \
  llama-index \
  llama-index-llms-google-genai \
  llama-index-tools-mcp \
  fastmcp
# パッケージの更新
uv pip list --outdated
uv sync --upgrade
```

```bash
uv run app.py
```