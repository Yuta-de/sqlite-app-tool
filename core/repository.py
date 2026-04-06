# ====================
#  SQLを書く場所(DBの種類が変わってもここだけ直せばいい)
# ====================

from core.db import get_connection


def add_sale(date: str, store: str, product: str, category: str, amount:int) -> None:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO sales (date, store, product, category, amount)
    VALUES (?, ?, ?, ?, ?)
    """, (date, store, product, category, amount))

    conn.commit()
    conn.close()

def get_all_sales():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM sales ORDER BY date")
    rows = cursor.fetchall()

    conn.close()
    return rows

def get_sales(store: str, date: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
            SELECT * FROM sales 
            WHERE store = ? AND date = ?
            """,(store,date))
    rows = cursor.fetchall()

    conn.close()
    return rows

def get_sales_summary_by_store():
    conn = get_connection()
    cursor = conn.cursor()

    query = """
            SELECT store, SUM(amount)
            FROM sales
            GROUP BY store
            ORDER BY SUM(amount) DESC            
            """
    cursor.execute(query)
    rows = cursor.fetchall()

    conn.close()
    return rows

def get_sales_summary_by_date():
    conn = get_connection()
    cursor = conn.cursor()

    query = """
            SELECT date, SUM(amount)
            FROM sales
            GROUP BY date
            ORDER BY SUM(amount) DESC            
            """
    cursor.execute(query)
    rows = cursor.fetchall()

    conn.close()
    return rows

def delete_all_sales():
    conn = get_connection()
    cursor = conn.cursor()

    query = "DELETE FROM sales"
    cursor.execute(query)

    conn.commit()
    conn.close()
