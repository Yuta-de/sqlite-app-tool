# ====================
# 業務ロジックを書く場所
# ====================

from pathlib import Path
import pandas as pd

from core.repository import add_sale

def import_sales_from_excel(file_path: str) -> None:
    excel_path = Path(file_path)

    df = pd.read_excel(excel_path)

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

def export_report_to_excel(file_path: str, reports_list: list[dict]) -> None:
    report_path = Path(file_path)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    with pd.ExcelWriter(report_path, engine="openpyxl") as writer:
        for report in reports_list:
            sheet_name = report["sheet_name"]
            df = pd.DataFrame(
                report["sales_summary"],
                columns=[sheet_name, "total_amount"]
            )
            df.to_excel(writer, sheet_name=report["sheet_name"], index=False)

