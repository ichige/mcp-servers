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
  pydantic
```

デバッグは MCP Inspector を使う。

- [MCP Inspector](https://github.com/modelcontextprotocol/inspector)

```bash
cd servers
npx @modelcontextprotocol/inspector uv run fastmcp run starter.py:mcp
```

### FastMCP Docs の構築

まずは本家のコード(ドキュメント)を clone します。

```bash
mkdir .resources
cd .resources
git clone --depth 1 https://github.com/PrefectHQ/fastmcp.git
```

続いて、doc ディレクトリ配下をプロジェクトルートへコピーします。

```bash
cp -R .resources/fastmcp/docs .
```

続いてビルドツールとなる minify をインストールします。

```bash
cd docs
# node のバージョンを固定
node -v > .node-version
# corepack を有効化
corepack enable
# pnpm を有効化
corepack prepare pnpm@latest --activate
# packege の初期化
pnpm init
# mintlify を導入
pnpm add mintlify --save-dev
# build が必要な package の対応
pnpm approve-builds
```

package.json に以下を追記します。

```json
"scripts": {
  "dev": "mintlify dev",
  "build": "mintlify build"
}
```

ローカルプレビューできます。  
時々一部のファイル(mdx)でパースエラーが発生する場合があるが、その場合は自力で修正します。

```bash
pnpm run dev
```

翻訳結果は docs 内の mdx を直接更新します。  
以前との差分は、.resources の中身の履歴を確認する予定です。

## Run

```bash
cd servers
uv run fastmcp run starter.py:mcp
uv run fastmcp run starter.py:mcp --transport http --port 8000
```