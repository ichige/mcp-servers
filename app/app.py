import logging
from dotenv import load_dotenv
from nicegui import ui
from obasan.bootstrap import bootstrap

# load .env
load_dotenv()
# logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(message)s"
)
# App の準備
bootstrap()
# 起動
ui.run()
