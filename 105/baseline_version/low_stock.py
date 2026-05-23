# ─────────────────────────────────────────────
# pages/low_stock.py — Low Stock Alerts Page
# ─────────────────────────────────────────────

import tkinter as tk

from base_page import BasePage
from config import BG, ACCENT, TEXT_GRAY, FONT_HEADER, FONT_SMALL


class LowStockPage(BasePage):

    def build(self):
        self.section_label("⚠️  Low Stock Alerts")

        tk.Label(self,
                 text="Products at or below their reorder level are listed below.",
                 font=FONT_SMALL, bg=BG, fg=TEXT_GRAY).pack(anchor="w", padx=14)

        self._lbl_count = tk.Label(self, text="", font=FONT_HEADER,
                                   bg=BG, fg=ACCENT)
        self._lbl_count.pack(anchor="w", padx=14, pady=(0, 4))

        cols   = ("ID", "Product", "Category", "Stock Qty", "Reorder Level")
        widths = (50, 220, 140, 90, 110)
        self._tree = self.make_table(self, cols, widths)

        self.red_btn(self, "🔄  Refresh Alerts", self._refresh).pack(
            anchor="w", padx=14, pady=4)
        self._refresh()

    def _refresh(self):
        rows = self.db.fetch("SELECT * FROM vw_low_stock ORDER BY stock_qty ASC")
        self._tree.delete(*self._tree.get_children())
        for r in rows:
            vals = (r["product_id"], r["product_name"],
                    r["category_name"], r["stock_qty"], r["reorder_level"])
            self._tree.insert("", "end", values=vals, tags=("low",))
        self._lbl_count.config(text=f"{len(rows)} item(s) need restocking")
