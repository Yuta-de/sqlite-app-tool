# ====================
#  メインの実行ファイルになる場所
# ====================
from pathlib import Path
import argparse

from core.db import init_db
from core.repository import (
    get_sales_summary_by_store,
    delete_all_sales,
    get_sales_summary_by_date,
    get_sales_summary_by_category,
    get_sales_summary_by_product
)
from core.service import import_sales_from_excel,export_report_to_excel
from core.config_loader import (
    EXCEL_SHEET_DATE,
    EXCEL_SHEET_STORE,
    EXCEL_SHEET_CATEGORY,
    EXCEL_SHEET_PRODUCT,
    DEFAULT_INPUT,
    DEFAULT_OUTPUT
)

def parse_args():
    parser = argparse.ArgumentParser(description="Sales Excel Import/Export tool")

    parser.add_argument("--input", help="入力Excelファイルのパス")
    parser.add_argument("--output", help="出力Excelファイルのパス")

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    input_file_path = Path(args.input or DEFAULT_INPUT)
    output_file_path = Path(args.output or DEFAULT_OUTPUT)

    if not input_file_path.exists():
        raise FileNotFoundError(f"入力ファイルが存在しません：{input_file_path}")

    init_db()
    print("データベースの初期化が完了しました。")

    # salesのデータ削除
    delete_all_sales()

    import_sales_from_excel(str(input_file_path))

    print("Excel出力中...")

    reports_list = [
        {"sales_summary": get_sales_summary_by_store(), "sheet_name": EXCEL_SHEET_STORE},
        {"sales_summary": get_sales_summary_by_date(), "sheet_name": EXCEL_SHEET_DATE},
        {"sales_summary": get_sales_summary_by_category(), "sheet_name": EXCEL_SHEET_CATEGORY},
        {"sales_summary": get_sales_summary_by_product(), "sheet_name": EXCEL_SHEET_PRODUCT}
    ]
    export_report_to_excel(str(output_file_path), reports_list)
    print("完了しました。")


if __name__ == "__main__":
    main()