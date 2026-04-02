import asyncio
from nicegui.elements.markdown import Markdown as NiceMarkdown
from pydantic import BaseModel, Field, PrivateAttr

class Markdown(BaseModel):
    """
    Markdown コンテンツ
    """
    text: str = Field(description="マークダウン本文", default="")
    _ui: NiceMarkdown = PrivateAttr(default=None)

    def subscribe(self, ui: NiceMarkdown):
        self._ui = ui

    def render(self, text: str):
        """
        markdown コンテンツを描画(更新)
        """
        self.text = text
        if self._ui:
            self._ui.set_content(text)

    async def render_stream(self, text: str):
        """
        markdown コンテンツを描画(更新) 疑似Stream版
        """
        self.text = ""
        for line in text.splitlines():
            current = self.text + line + "\n"
            await asyncio.sleep(0.1)
            self.render(current)

# singleton
markdown = Markdown()