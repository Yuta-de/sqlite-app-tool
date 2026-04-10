from configparser import ConfigParser
from pathlib import Path

config = ConfigParser()

config_path = Path(__file__).resolve().parent.parent / "config.ini"
config.read(config_path, encoding="utf-8")

EXCEL_SHEET_STORE = config.get("excel", "sheet_store", fallback="store")
EXCEL_SHEET_DATE = config.get("excel", "sheet_date", fallback="date")