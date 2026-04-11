from configparser import ConfigParser
from pathlib import Path

config = ConfigParser()

config_path = Path(__file__).resolve().parent.parent / "config.ini"
config.read(config_path, encoding="utf-8")

EXCEL_SHEET_STORE = config.get("excel", "sheet_store", fallback="store")
EXCEL_SHEET_DATE = config.get("excel", "sheet_date", fallback="date")
EXCEL_SHEET_CATEGORY = config.get("excel", "sheet_category", fallback="category")
EXCEL_SHEET_PRODUCT = config.get("excel", "sheet_product", fallback="product")

DEFAULT_INPUT = config.get("paths", "default_input", fallback="input/sales.xlsx")
DEFAULT_OUTPUT = config.get("paths", "default_output", fallback="output/report.xlsx")