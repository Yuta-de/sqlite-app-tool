# sqlite-app-tool

売上ExcelファイルをDBに取り込み、集計結果をExcelファイルでエクスポートするツールです。  
CLIとGUI（Tkinter）の両方で実行できます。
業務でExcel集計を行っている人向けに作成したツールです。

---

## 特徴

- Excelファイルの取り込み
- pandasによるExcel書き込み
- DB保存(SQLite)
- CLI / GUI 両対応
- config.ini による設定管理
- loggingによるログ出力（ファイル / GUI / コンソール）

---
## セットアップ

```bash
pip install -r requirements.txt
```

---
## 設定ファイル
`config.ini`を編集してください。

```ini
[excel]
sheet_store = store
sheet_date = date
sheet_category = category
sheet_product = product

[paths]
default_input = input/sales.xlsx
default_output = output/report.xlsx

[log]
log_file = logs/app.log
log_level = INFO
```

---
## 入力ファイル形式

以下の列を持つExcelファイルを想定しています：

- date
- store
- product
- category
- amount
---
## 出力内容

集計結果を以下のシートで出力します：

- store（店舗別）
- date（日付別）
- category（カテゴリ別）
- product（商品別）
---
## 実行方法

### CLI

```bash
python run.py --input input/sales.xlsx --output output/report.xlsx
```

### GUI

```bash
python run.py --gui
```

---

## フォルダ構成

```text
sqlite_app/
├─ core/
│   ├─ config_loader.py
│   ├─ db.py
│   ├─ logger_setup.py
│   ├─ repository.py
│   └─ service.py
│
├─ gui/
│   └─ gui_app.py
│
├─ run.py
├─ config.ini
└─ requirements.txt
```

---

## 設計ポイント

- 責務分離
  - `core/db.py`: DBの接続管理
  - `core/repository.py`: SQL
  - `core/service.py`: 業務ロジック(GUI/CLIで共通化し、再利用性を高めた)
  - `gui/gui_app.py`：UI
  - `run.py`：アプリの入り口(GUI/CLI分岐)
- 設定の外部化（config.ini）
- Tkinterのメインスレッド/ワーカースレッド分離し、UIフリーズを防止
- loggingのHandlerを分離し、GUIにもログを出力できるようにした

---

## 使用技術
- Python
- pandas/openpyxl
- sqlite3
- tkinter
- logging
- configparser
- argparse

---

## 今後の改善予定
- GUIのエラーダイアログ実装
- スレッド状態管理（多重実行防止の強化）
- DBトランザクション
- Web連携（Seleniumなど）