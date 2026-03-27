# Fast MCP Servers

- [Fast MCP V3](https://gofastmcp.com/getting-started/welcome)

## アプリケーションの仕様

FastMCP ドキュメントの日本語翻訳を自動化する際に、あえて MCP を導入してみる。  
MCP 導入におけるメリットの1つが、エージェント別に使いまわせる「再利用性」だが、今回はあくまで MCP の導入が目的になるので、そこは無視しておく。

### UI

- 「○○の更新対象はある？」
    - 更新対象があればリスト表示
- リストに並んだドキュメントの翻訳ボタンを押す
    - 翻訳結果をUIに表示
- 保存ボタンを押す
    - 翻訳内容を所定の場所へ保存する。 

今回は LlamaIndex だけ対応。  
そのうち他のやつもやるかも？

### ザックリ設計

以下必要なツールやコンポーネントの設計。

- 更新対象一覧を返すツール
    - 構造化データで返す。
    - 保存先も決めておく。
    - リソースのURLを含めても良い。
- ドキュメントを返すリソース
    - URL を指定することで、ドキュメントを返せるようなURL設計をする。
- 翻訳ツール
    - Sampling 機能を使って、翻訳する。  
    - User Elicitation で、最終確認を促す。
- 保存機能ツール
    - 保存先を指定して翻訳内容を保存する機能。

エージェント側はあくまで翻訳させるまでのステート管理に徹する。  
翻訳機能などは全てMCPに任せる形にする。

第1弾はここまで対応したい。

## Environment

### python 環境の構築

```bash
# 初期化
uv init
# venv の作成
uv venv --python 3.14
# パッケージのインストール
uv sync
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
uv run fastmcp run servers/main.py:mcp --transport http --port 8000
```