from workflows.events import Event
from typing import Annotated

class UrlInputEvent(Event):
    """
    翻訳または情報参照を求められた場合のイベント
    """
    url: Annotated[str, "翻訳対象となるドキュメントのURL"]
