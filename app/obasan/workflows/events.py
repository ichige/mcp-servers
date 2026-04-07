from workflows.events import Event, StartEvent
from enum import Enum
from typing import Annotated

class ActionNameEnum(str, Enum):
    """
    Action Name
    """
    # ファイルの状態確認
    INSPECT = "inspect"
    # ファイルの翻訳
    TRANSLATE = "translate"
    # ファイルの保存
    SAVE = "save"
    # Git リポジトリの更新
    UPDATE = "update"

class ActionEvent(StartEvent):
    """
    カスタム StartEvent
    """
    action_name: Annotated[ActionNameEnum, "アクション(ボタン)名"]
    url: Annotated[str, "翻訳対象となるドキュメントのURL"]

class UrlInputEvent(Event):
    """
    翻訳または情報参照を求められた場合のイベント
    """
    action_name: Annotated[ActionNameEnum, "アクション(ボタン)名"]
    url: Annotated[str, "翻訳対象となるドキュメントのURL"]

class InspectionEvent(Event):
    """
    検査実行フェーズのイベント
    """
    path: Annotated[str, "検査対象となるドキュメントのPATH"]
    prompt: Annotated[str, "検査実行用プロンプト名"] = "file_inspect_prompt"

    def arguments(self) -> dict[str, str]:
        """
        エージェント実行引数
        """
        return {
            "path": self.path
        }

class TranslationEvent(Event):
    """
    翻訳実行フェーズのイベント
    """
    path: Annotated[str, "翻訳対象となるドキュメントのPATH"]

class SaveEvent(Event):
    """
    翻訳結果の保存イベント
    """
    path: Annotated[str, "翻訳対象となるドキュメントのPATH"]
    content: Annotated[str, "翻訳結果のドキュメント"]
    ext: Annotated[str, "ファイルの拡張子"] = "mdx"

class UpdateRepoEvent(Event):
    """
    FastMCPリポジトリの更新を求めらた場合のイベント
    """
    action_name: Annotated[ActionNameEnum, "アクション(ボタン)名"]
    prompt: Annotated[str, "リポジトリ更新用プロンプト名"] = "update_local_repository_prompt"
