# ====================
#  メインの実行ファイルになる場所
# ====================

from core.db import init_db
from core.repository import (
    get_all_sales, 
    get_sales,
    get_sales_summary_by_store,
    delete_all_sales,
    get_sales_summary_by_date
)
from core.service import import_sales_from_excel,export_report_to_excel

from pathlib import Path

def main() -> None:
    init_db()
    print("データベースの初期化が完了しました。")

    # salesのデータ削除
    delete_all_sales()

    input_file_path = "input/sales.xlsx"
    import_sales_from_excel(input_file_path)

    print("----- 東京店かつ2026-04-01で取得 -----")
    sales_tokyo = get_sales("東京店", "2026-04-01")
    for row in sales_tokyo:
        print(row)

    print("----- 全件取得 -----")
    sales = get_all_sales()
    for row in sales:
        print(row)

    print("-----店別集計-----")
    sales_summary_store = get_sales_summary_by_store()
    for store, total in sales_summary_store:
        print(f"{store}: {total}円")
    
    print("-----日別集計-----")
    sales_summary_date = get_sales_summary_by_date()
    for date, total in sales_summary_date:
        print(f"{date}: {total}円")

    print("Excel出力")
    output_file_path = "output/report.xlsx"
    reports_list = [
        {"sales_summary": sales_summary_store, "sheet_name": "store"},
        {"sales_summary": sales_summary_date, "sheet_name": "date"}
    ]
    export_report_to_excel(output_file_path, reports_list)


if __name__ == "__main__":
    main()