# ====================
# 業務ロジックを書く場所
# ====================

from pathlib import Path
import pandas as pd

from core.db import init_db
from core.repository import (
    delete_all_sales,
    add_sale,
    get_sales_summary_by_store,
    get_sales_summary_by_date,
    get_sales_summary_by_category,
    get_sales_summary_by_product
)

from core.config_loader import (
    EXCEL_SHEET_DATE,
    EXCEL_SHEET_STORE,
    EXCEL_SHEET_CATEGORY,
    EXCEL_SHEET_PRODUCT
)

from logging import getLogger

logger = getLogger(__name__)

def import_sales_from_excel(file_path: str) -> None:
    excel_path = Path(file_path)

    logger.info(f"Import start: {file_path}")
    df = pd.read_excel(excel_path)
    logger.info(f"Excel loaded: {len(df)} rows")

    # 列名バリデーション
    required_cols = ["date", "store", "product", "category", "amount"]
    missing_cols = [col for col in required_cols if col not in df.columns]

    if missing_cols:
        raise ValueError(
            "Excelの列名が不足しています\n"
            f"不足列名：{', '.join(missing_cols)}\n"
            f"必須列名：{', '.join(required_cols)}"
        )

    for row in df.itertuples(index=False):
        add_sale(
            date=str(row.date).split(" ")[0],
            store=str(row.store),
            product=str(row.product),
            category=str(row.category),
            amount=int(row.amount) # type: ignore[attr-defined]
        )
    logger.info(f"{len(df)} rows inserted")
    logger.info("Import completed")

def export_report_to_excel(file_path: str, reports_list: list[dict]) -> None:
    report_path = Path(file_path)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    logger.info(f"Export start: {file_path}")

    with pd.ExcelWriter(report_path, engine="openpyxl") as writer:
        for report in reports_list:
            sheet_name = report["sheet_name"]
            df = pd.DataFrame(
                report["sales_summary"],
                columns=[sheet_name, "total_amount"]
            )
            df.to_excel(writer, sheet_name=report["sheet_name"], index=False)
    
    logger.info("Export completed")

def process_sales_report(input_file_path: Path, output_file_path: Path) -> None:
    
    # DB初期化
    init_db()

    # salesのデータ削除
    delete_all_sales()

    # excelのデータをDBに取り込み
    import_sales_from_excel(str(input_file_path))

    reports_list = [
        {"sales_summary": get_sales_summary_by_store(), "sheet_name": EXCEL_SHEET_STORE},
        {"sales_summary": get_sales_summary_by_date(), "sheet_name": EXCEL_SHEET_DATE},
        {"sales_summary": get_sales_summary_by_category(), "sheet_name": EXCEL_SHEET_CATEGORY},
        {"sales_summary": get_sales_summary_by_product(), "sheet_name": EXCEL_SHEET_PRODUCT}
    ]

    # エクスポート処理
    export_report_to_excel(str(output_file_path), reports_list)

