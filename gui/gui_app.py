# ====================
# Tkinter GUI (GUI専用)
# ====================

import tkinter as tk
from pathlib import Path
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog
from typing import Dict
from core.service import process_sales_report
from core.config_loader import DEFAULT_INPUT, DEFAULT_OUTPUT

import queue
import logging
from logging import getLogger
from core.logger_setup import setup_logger
import threading


# ログのキュー
log_queue = queue.Queue()

# GUI用のハンドラー
class QueueLogHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        msg = self.format(record)
        log_queue.put(msg + "\n")


# --- GUI本体 ---
def gui_main():
    root = tk.Tk()
    root.title("売上レポート管理ツール")

    # GUI用のログ設定変更
    gui_handler = QueueLogHandler()
    setup_logger([gui_handler])
    logger = getLogger(__name__)

    # --- 関数 ---
    # 入力情報取得
    def get_setting_info() -> Dict[str, Path]:
        import_path = Path(import_var.get() or DEFAULT_INPUT)
        export_folder = export_folder_var.get()
        export_file_name = export_file_var.get()
        if export_folder and export_file_name:
            export_path = Path(export_folder) / (export_file_name + ".xlsx")
        elif export_folder:
            export_path = Path(export_folder).joinpath(Path(DEFAULT_OUTPUT).name)
        else:
            export_path = Path(DEFAULT_OUTPUT)
        return {"import_path" : import_path, "export_path": export_path}
    
    # 実行
    def worker(input_file_path: Path, output_file_path: Path):
        try:
            logger.info("Application started")
            process_sales_report(input_file_path, output_file_path)
            logger.info("Application finished")
        except Exception:
            logger.exception("Unexpected error occurred")
        finally:
            root.after(0, lambda: run_button.config(state="normal"))

    def start_worker():
        run_button.config(state="disabled")
        setting = get_setting_info()
        input_file_path = setting["import_path"]
        output_file_path = setting["export_path"]
        worker_thread = threading.Thread(
            target=worker,
            args=(input_file_path, output_file_path),
            daemon=True
        )
        worker_thread.start()

    # ログの更新
    def log_update():
        while not log_queue.empty():
            msg = log_queue.get()
            log_box.insert(tk.END, msg)
            log_box.see(tk.END)
        root.after(100, log_update)
    

    # 入力ファイル
    import_label = tk.Label(root, text="インポートファイル")
    import_label.grid(row=0, column=0)
    import_var = tk.StringVar()
    import_entry = tk.Entry(root, textvariable=import_var, width=50)
    import_entry.grid(row=0, column=1)
    import_button = tk.Button(root, text="選択", command=lambda:(import_var.set(filedialog.askopenfilename())))
    import_button.grid(row=0, column=2)

    # 出力フォルダ
    export_folder_label = tk.Label(root, text="エクスポートフォルダ")
    export_folder_label.grid(row=1, column=0)
    export_folder_var = tk.StringVar()
    export_folder_entry = tk.Entry(root, textvariable=export_folder_var, width=50)
    export_folder_entry.grid(row=1, column=1)
    export_button = tk.Button(root, text="選択", command=lambda:(export_folder_var.set(filedialog.askdirectory())))
    export_button.grid(row=1, column=2)


    # 出力ファイル名
    export_file_label = tk.Label(root, text="エクスポートファイル名")
    export_file_label.grid(row=2, column=0)
    export_file_var = tk.StringVar()
    export_file_entry = tk.Entry(root, textvariable=export_file_var, width=50)
    export_file_entry.grid(row=2, column=1)
    export_file_extention = tk.Label(root, text=".xlsx")
    export_file_extention.grid(row=2,column=2 )

    # 実行ボタン
    run_button = tk.Button(root, text="実行", command=start_worker)
    run_button.grid(row=3, column=1)

    # ログ表示ボックス
    log_box = ScrolledText(root, width=80, height=10)
    log_box.grid(row=4, column=0, columnspan=3)

    # ログの更新
    log_update()

    # ウィンドウを表示する
    root.mainloop()

if __name__ == "__main__":
    gui_main()