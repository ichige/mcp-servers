from dotenv import load_dotenv
from nicegui import ui
from obasan.bootstrap import bootstrap

# load .env
load_dotenv()
# App の準備
bootstrap()
# 起動
ui.run()
