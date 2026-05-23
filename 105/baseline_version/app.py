# ─────────────────────────────────────────────
# app.py — Main Application Window
# ─────────────────────────────────────────────

import tkinter as tk
from tkinter import ttk

from config import (
    BG, SIDEBAR, SIDEBAR_H, WHITE,
    FONT_BTN, DB_CONFIG
)
from database import Database
from dashboard  import DashboardPage
from products   import ProductsPage
from stock_in   import StockInPage
from suppliers  import SuppliersPage
from low_stock  import LowStockPage



class SariSariApp(tk.Tk):
    """Root window — owns the sidebar and content area."""

    PAGES = [
        ("🏠  Dashboard",   DashboardPage),
        ("🛒  Products",    ProductsPage),
        ("📥  Stock-In",    StockInPage),
        ("🏪  Suppliers",   SuppliersPage),
        ("⚠️  Low Stock",   LowStockPage),
    ]

    def __init__(self):
        super().__init__()
        self.title("Nanay Sari-Sari Store — Baseline Version")
        self.geometry("980x640")
        self.minsize(860, 560)
        self.configure(bg=BG)
        self.db = Database(DB_CONFIG)
        self._build_layout()
        self._show(DashboardPage, "🏠  Dashboard")

    def _build_layout(self):
        sidebar = tk.Frame(self, bg=SIDEBAR, width=190)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="🏪", font=("Helvetica", 30),
                 bg=SIDEBAR, fg=WHITE).pack(pady=(24, 0))
        tk.Label(sidebar, text="Nanay\nSari-Sari Store",
                 font=("Georgia", 12, "bold"), bg=SIDEBAR,
                 fg=WHITE, justify="center").pack(pady=(4, 20))
        tk.Frame(sidebar, bg=SIDEBAR_H, height=1).pack(fill="x", padx=14)

        self._content = tk.Frame(self, bg=BG)
        self._content.pack(side="left", fill="both", expand=True)

        self._nav_btns = []
        for label, page_cls in self.PAGES:
            btn = tk.Button(
                sidebar, text=label, font=FONT_BTN,
                bg=SIDEBAR, fg=WHITE, relief="flat",
                anchor="w", padx=18, pady=10,
                activebackground=SIDEBAR_H, activeforeground=WHITE,
                cursor="hand2",
                command=lambda cls=page_cls, lbl=label: self._show(cls, lbl))
            btn.pack(fill="x")
            self._nav_btns.append((btn, label))

        tk.Label(sidebar,
                 text="IT6L  •  Dela Cerna\nFundamentals of DB Systems",
                 font=("Helvetica", 8), bg=SIDEBAR,
                 fg="#E8A8A4", justify="center").pack(side="bottom", pady=14)

    def _show(self, page_cls, active_label: str):
        for btn, lbl in self._nav_btns:
            btn.config(bg=SIDEBAR_H if lbl == active_label else SIDEBAR)

        for w in self._content.winfo_children():
            w.destroy()

        canvas = tk.Canvas(self._content, bg=BG, highlightthickness=0)
        sb     = ttk.Scrollbar(self._content, orient="vertical",
                               command=canvas.yview)
        canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        inner  = tk.Frame(canvas, bg=BG)
        win_id = canvas.create_window((0, 0), window=inner, anchor="nw")

        canvas.bind("<Configure>",
                    lambda e: canvas.itemconfig(win_id, width=e.width))
        inner.bind("<Configure>",
                   lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind_all("<MouseWheel>",
                        lambda e: canvas.yview_scroll(
                            int(-1 * (e.delta / 120)), "units"))

        page_cls(inner, self.db)


if __name__ == "__main__":
    app = SariSariApp()
    app.mainloop()
