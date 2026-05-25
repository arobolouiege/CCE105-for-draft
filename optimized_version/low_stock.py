# pages/low_stock.py - Low Stock Alerts Page

import tkinter as tk

from base_page import BasePage
from config import BG, ACCENT, TEXT_GRAY, FONT_HEADER, FONT_SMALL
from algorithms import MinHeap


class LowStockPage(BasePage):

    def build(self):
        self.section_label("Low Stock Alerts")

        tk.Label(self,
                 text="Restock priority is ordered by urgency ratio.",
                 font=FONT_SMALL, bg=BG, fg=TEXT_GRAY).pack(anchor="w", padx=14)

        self._lbl_count = tk.Label(self, text="", font=FONT_HEADER,
                                   bg=BG, fg=ACCENT)
        self._lbl_count.pack(anchor="w", padx=14, pady=(0, 4))

        cols = ("ID", "Product", "Category", "Stock Qty", "Reorder Level", "Ratio", "Status")
        widths = (50, 200, 130, 90, 110, 70, 90)
        self._tree = self.make_table(self, cols, widths)

        self.red_btn(self, "Refresh Alerts", self._refresh).pack(
            anchor="w", padx=14, pady=4)
        self._refresh()

    def _refresh(self):
        rows = self.db.fetch("""
            SELECT p.product_id, p.product_name, c.category_name,
                   p.reorder_level,
                   COALESCE(SUM(sb.quantity), 0)
                     - COALESCE((SELECT SUM(s.quantity_sold)
                                 FROM sales s
                                 WHERE s.product_id = p.product_id), 0) AS stock_qty
            FROM product p
            JOIN category c ON p.category_id = c.category_id
            LEFT JOIN stock_batch sb ON sb.product_id = p.product_id
            GROUP BY p.product_id, p.product_name, c.category_name, p.reorder_level
        """)
        # LowStockPage = MinHeap restock prioritization by stock/reorder ratio.
        queue = MinHeap.build_restock_queue(rows)
        prioritized = queue.to_sorted_list()

        self._tree.delete(*self._tree.get_children())
        needs_restock = 0
        for i, r in enumerate(prioritized):
            stock = int(r.get("stock_qty", 0))
            reorder = max(int(r.get("reorder_level", 1)), 1)
            ratio = stock / reorder
            if stock == 0:
                status = "OUT"
            elif ratio <= 0.5:
                status = "URGENT"
            elif ratio <= 1.0:
                status = "LOW"
            else:
                status = "OK"

            if ratio <= 1.0:
                needs_restock += 1
            tag = "low" if ratio <= 1.0 else ("odd" if i % 2 else "even")
            vals = (r["product_id"], r["product_name"], r["category_name"],
                    stock, reorder, f"{ratio:.2f}", status)
            self._tree.insert("", "end", values=vals, tags=(tag,))

        self._lbl_count.config(
            text=f"{needs_restock} item(s) need restocking - ordered using MinHeap")
