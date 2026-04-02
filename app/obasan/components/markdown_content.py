from nicegui import ui
from obasan.stores import markdown

def markdown_content():
    """
    マークダウン描コンポーネント
    """
    component = ui.markdown()
    markdown.subscribe(component)
