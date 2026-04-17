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


# --- GUI本体 ---
def gui_main():
    # 関数
    def get_setting_info() -> Dict[str, Path]:
        import_path = Path(import_var.get())
        export_path = Path(export_folder_var.get()) / (export_file_var.get() + ".xlsx")
        return {"import_path" : import_path, "export_path": export_path}
    
    def worker():
        try:
            setting = get_setting_info()
            input_file_path = setting.get("import_path") or Path(DEFAULT_INPUT)
            output_file_path = setting.get("export_path") or Path(DEFAULT_OUTPUT)
            process_sales_report(input_file_path, output_file_path)
        except Exception as e:
            print("Unexpected error occurred:", str(e))

    root = tk.Tk()
    root.title("売上レポート管理ツール")

    # 入力ファイル
    import_label = tk.Label(root, text="インポートファイル").grid(row=0, column=0)
    import_var = tk.StringVar()
    import_entry = tk.Entry(root, textvariable=import_var, width=50)
    import_entry.grid(row=0, column=1)
    import_button = tk.Button(root, text="選択", command=lambda:(import_var.set(filedialog.askopenfilename()))).grid(row=0, column=2)

    # 出力フォルダ
    export_folder_label = tk.Label(root, text="エクスポートフォルダ").grid(row=1, column=0)
    export_folder_var = tk.StringVar()
    export_folder_entry = tk.Entry(root, textvariable=export_folder_var, width=50)
    export_folder_entry.grid(row=1, column=1)
    export_button = tk.Button(root, text="選択", command=lambda:(export_folder_var.set(filedialog.askdirectory())))
    export_button.grid(row=1, column=2)


    # 出力ファイル名
    export_file_label = tk.Label(root, text="エクスポートファイル名").grid(row=2, column=0)
    export_file_var = tk.StringVar()
    export_file_entry = tk.Entry(root, textvariable=export_file_var, width=50)
    export_file_entry.grid(row=2, column=1)
    export_file_extention = tk.Label(root, text=".xlsx").grid(row=2,column=2 )

    # 実行ボタン
    run_button = tk.Button(root, text="実行", command=worker).grid(row=3, column=1)

    # ログ表示ボックス
    log_box = ScrolledText(root, width=80, height=10)
    log_box.grid(row=4, column=0, columnspan=3)

    # ウィンドウを表示する
    root.mainloop()

if __name__ == "__main__":
    gui_main()