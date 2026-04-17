# ====================
#  メインの実行ファイルになる場所
# ====================
from pathlib import Path
import argparse

from core.service import process_sales_report
from core.config_loader import DEFAULT_INPUT, DEFAULT_OUTPUT
import core.logger_setup # 読み込むだけ
from logging import getLogger

logger = getLogger(__name__)

def parse_args():
    parser = argparse.ArgumentParser(description="Sales Excel Import/Export tool")

    #入出力用
    parser.add_argument("--input", help="入力Excelファイルのパス")
    parser.add_argument("--output", help="出力Excelファイルのパス")

    #GUI用
    parser.add_argument("--gui", help="GUI用の引数", action="store_true")

    return parser.parse_args()

def gui_main() -> None:
    from gui.gui_app import gui_main
    gui_main()


def cli_main() -> None:
    try:
        logger.info("Application started")
        args = parse_args()

        # 入出力を引数から取得
        input_file_path = Path(args.input or DEFAULT_INPUT)
        output_file_path = Path(args.output or DEFAULT_OUTPUT)

        if not input_file_path.exists():
            raise FileNotFoundError(f"入力ファイルが存在しません：{input_file_path}")
        
        # 業務ロジック実行
        process_sales_report(input_file_path, output_file_path)

        logger.info("Application finished")
    
    except Exception as e:
        logger.exception("Unexpected error occurred")
        raise

if __name__ == "__main__":
    args = parse_args()
    if args.gui:
        gui_main()
    else:
        cli_main()