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

class TranslationEvent(Event):
    """
    翻訳実行フェーズのイベント
    """
    path: Annotated[str, "翻訳対象となるドキュメントのPATH"]