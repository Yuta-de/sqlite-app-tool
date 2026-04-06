# ====================
# 業務ロジックを書く場所
# ====================

from pathlib import Path
import pandas as pd

from core.repository import add_sale

def import_sales_from_excel(file_path: str) -> None:
    excel_path = Path(file_path)

    df = pd.read_excel(excel_path)

    for row in df.itertuples(index=False):
        add_sale(
            date=str(row.date).split(" ")[0],
            store=str(row.store),
            product=str(row.product),
            category=str(row.category),
            amount=int(row.amount) # type: ignore[attr-defined]
        )

def export_report_to_excel(file_path: str, reports_list: list[dict]) -> None:
    report_path = Path(file_path)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    with pd.ExcelWriter(report_path, engine="openpyxl") as writer:
        for report in reports_list:
            df = pd.DataFrame(
                report["sales_summary"],
                columns=[report["sheet_name"], "total_amount"]
            )
            df.to_excel(writer, sheet_name=report["sheet_name"], index=False)

