# ─────────────────────────────────────────────
# base_page.py — Base Page Class
# ─────────────────────────────────────────────

import tkinter as tk
from tkinter import ttk

from config import (
    BG, WHITE, SIDEBAR, SIDEBAR_H, ACCENT, TEXT_DARK, TEXT_GRAY,
    ROW_ODD, ROW_EVEN, ROW_LOW,
    FONT_TITLE, FONT_HEADER, FONT_BODY, FONT_SMALL, FONT_BTN,
)


class BasePage(tk.Frame):
    """
    All page classes inherit from this.
    Provides:
      - section_label()  — big page heading
      - labeled_entry()  — label + Entry in a grid form
      - labeled_combo()  — label + Combobox in a grid form
      - make_table()     — styled Treeview with scrollbar
      - red_btn()        — primary action button
      - grey_btn()       — secondary / cancel button
      - purple_btn()     — danger / destructive button
    """

    def __init__(self, parent, db):
        super().__init__(parent, bg=BG)
        self.pack(fill="both", expand=True)
        self.db = db
        self.build()

    # ── Override in subclass ─────────────────────────────────────────────
    def build(self):
        pass

    # ── Helpers ──────────────────────────────────────────────────────────

    def section_label(self, text: str):
        tk.Label(self, text=text, font=FONT_TITLE,
                 bg=BG, fg=SIDEBAR).pack(anchor="w", padx=14, pady=(14, 2))
        tk.Frame(self, bg=ACCENT, height=2).pack(fill="x", padx=14, pady=(0, 6))

    def labeled_entry(self, parent, label: str, row: int,
                      col: int = 0, width: int = 22) -> tk.StringVar:
        tk.Label(parent, text=label, font=FONT_SMALL,
                 bg=WHITE, fg=TEXT_GRAY).grid(
            row=row, column=col * 2, padx=(8, 2), pady=4, sticky="w")
        var = tk.StringVar()
        tk.Entry(parent, textvariable=var, width=width,
                 font=FONT_BODY, relief="solid", bd=1).grid(
            row=row, column=col * 2 + 1, padx=(0, 8), pady=4, sticky="w")
        return var

    def labeled_combo(self, parent, label: str, row: int,
                      values: list, col: int = 0,
                      width: int = 20) -> tuple[tk.StringVar, ttk.Combobox]:
        tk.Label(parent, text=label, font=FONT_SMALL,
                 bg=WHITE, fg=TEXT_GRAY).grid(
            row=row, column=col * 2, padx=(8, 2), pady=4, sticky="w")
        var = tk.StringVar()
        combo = ttk.Combobox(parent, textvariable=var,
                             values=values, state="readonly", width=width)
        combo.grid(row=row, column=col * 2 + 1,
                   padx=(0, 8), pady=4, sticky="w")
        return var, combo

    def make_table(self, parent, columns: tuple,
                   widths: tuple, height: int = 12) -> ttk.Treeview:
        frame = tk.Frame(parent, bg=BG)
        frame.pack(fill="both", expand=True, padx=14, pady=6)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background=WHITE, fieldbackground=WHITE,
                        foreground=TEXT_DARK, rowheight=26,
                        font=FONT_BODY)
        style.configure("Treeview.Heading",
                        background=SIDEBAR, foreground=WHITE,
                        font=("Helvetica", 10, "bold"))
        style.map("Treeview", background=[("selected", SIDEBAR_H)])

        tree = ttk.Treeview(frame, columns=columns,
                            show="headings", height=height)
        for col, w in zip(columns, widths):
            tree.heading(col, text=col)
            tree.column(col, width=w, minwidth=w // 2, anchor="w")

        # Row colour tags
        tree.tag_configure("odd",  background=ROW_ODD)
        tree.tag_configure("even", background=ROW_EVEN)
        tree.tag_configure("low",  background=ROW_LOW,
                           foreground="#C0392B")

        vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        tree.pack(side="left", fill="both", expand=True)
        return tree

    # ── Button factory ───────────────────────────────────────────────────

    def _make_btn(self, parent, text: str, cmd,
                  bg: str, fg: str = WHITE) -> tk.Button:
        return tk.Button(parent, text=text, font=FONT_BTN,
                         bg=bg, fg=fg, relief="flat",
                         padx=10, pady=5, cursor="hand2",
                         activebackground=bg, activeforeground=fg,
                         command=cmd)

    def red_btn(self, parent, text: str, cmd) -> tk.Button:
        return self._make_btn(parent, text, cmd, ACCENT)

    def grey_btn(self, parent, text: str, cmd) -> tk.Button:
        return self._make_btn(parent, text, cmd, "#95A5A6")

    def purple_btn(self, parent, text: str, cmd) -> tk.Button:
        return self._make_btn(parent, text, cmd, "#8E44AD")
