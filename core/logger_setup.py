import logging

from pathlib import Path
from core.config_loader import config

# config.iniから取得
LOG_FILE = config.get("log", "log_file", fallback="app.log")
LOG_LEVEL = config.get("log", "log_level", fallback="INFO").upper()

# ログディレクトリ作成
log_dir = Path(LOG_FILE).parent
log_dir.mkdir(parents=True, exist_ok=True)

# loggingの二重登録を防止
root_logger = logging.getLogger()
if root_logger.handlers:
    root_logger.handlers.clear()

#ハンドラー
handlers=[
    logging.FileHandler(LOG_FILE, encoding="utf-8"),
    logging.StreamHandler()
]

# ロガー設定
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=handlers
)