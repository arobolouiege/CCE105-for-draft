# ─────────────────────────────────────────────
# database.py — Database Handler
# ─────────────────────────────────────────────

import tkinter.messagebox as messagebox
import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta


CREATE_SALES_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS sales (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    quantity_sold INT NOT NULL,
    selling_price DECIMAL(10,2) NOT NULL,
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_sales_product
        FOREIGN KEY (product_id) REFERENCES product(product_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
)
"""


class Database:
    """Handles all MySQL operations."""

    def __init__(self, config: dict):
        self.config = config
        self._ensure_sales_table()
        self._ensure_product_seed_count()
        self._ensure_sales_seed_count()

    def _connect(self):
        return mysql.connector.connect(**self.config)

    def _ensure_sales_table(self):
        try:
            conn = self._connect()
            cur = conn.cursor()
            cur.execute(CREATE_SALES_TABLE_SQL)
            conn.commit()
            conn.close()
        except Error as e:
            messagebox.showerror("DB Error", str(e))

    def _ensure_product_seed_count(self, target_count: int = 500):
        try:
            conn = self._connect()
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT COUNT(*) AS n FROM product")
            current_count = cur.fetchone()["n"]
            if current_count >= target_count:
                conn.close()
                return

            cur.execute("SELECT category_id, category_name FROM category ORDER BY category_id")
            categories = cur.fetchall()
            if not categories:
                conn.close()
                return

            units = ["can", "bottle", "pack", "pack", "piece"]
            n = 1
            while current_count < target_count:
                category = categories[n % len(categories)]
                product_name = f"Store Product {n:03d}"
                cur.execute(
                    "SELECT 1 FROM product WHERE product_name=%s LIMIT 1",
                    (product_name,))
                if cur.fetchone() is None:
                    cur.execute(
                        "INSERT INTO product "
                        "(category_id, product_name, unit, price, reorder_level) "
                        "VALUES (%s,%s,%s,%s,%s)",
                        (
                            category["category_id"],
                            product_name,
                            units[n % len(units)],
                            10.00 + (n * 7 % 95),
                            5 + (n % 21),
                        ))
                    current_count += 1
                n += 1

            conn.commit()
            conn.close()
        except Error as e:
            messagebox.showerror("DB Error", str(e))

    def _ensure_sales_seed_count(self, target_count: int = 68):
        try:
            conn = self._connect()
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT COUNT(*) AS n FROM sales")
            current_count = cur.fetchone()["n"]
            if current_count >= target_count:
                conn.close()
                return

            cur.execute("""
                SELECT product_id, price
                FROM product
                ORDER BY product_id
                LIMIT %s
            """, (target_count,))
            products = cur.fetchall()
            if not products:
                conn.close()
                return

            needed = target_count - current_count
            now = datetime.now()
            for i in range(needed):
                product = products[(current_count + i) % len(products)]
                qty = 1 + ((current_count + i) % 5)
                sale_date = now - timedelta(hours=i)
                cur.execute(
                    "INSERT INTO sales "
                    "(product_id, quantity_sold, selling_price, sale_date) "
                    "VALUES (%s,%s,%s,%s)",
                    (product["product_id"], qty, product["price"], sale_date)
                )

            conn.commit()
            conn.close()
        except Error as e:
            messagebox.showerror("DB Error", str(e))

    def fetch(self, sql: str, params: tuple = ()) -> list:
        try:
            conn = self._connect()
            cur  = conn.cursor(dictionary=True)
            cur.execute(sql, params)
            rows = cur.fetchall()
            conn.close()
            return rows
        except Error as e:
            messagebox.showerror("DB Error", str(e))
            return []

    def execute(self, sql: str, params: tuple = ()):
        try:
            conn = self._connect()
            cur  = conn.cursor()
            cur.execute(sql, params)
            conn.commit()
            lid = cur.lastrowid
            conn.close()
            return lid
        except Error as e:
            messagebox.showerror("DB Error", str(e))
            return None
