# ─────────────────────────────────────────────
# pages/stock_in.py — Stock-In Page (With Reference Number)
# ─────────────────────────────────────────────

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime

from base_page import BasePage
from config import (
    WHITE, SIDEBAR, SIDEBAR_H, ACCENT, BG,
    TEXT_DARK, TEXT_GRAY,
    FONT_TITLE, FONT_HEADER, FONT_BODY, FONT_SMALL, FONT_BTN,
    ROW_ODD, ROW_EVEN
)


class StockInPage(BasePage):

    def build(self):
        self.section_label("📥  Stock-In")
        self._items: list[dict] = []

        # ── 1. Delivery Header ─────────────────────────
        hdr = tk.LabelFrame(self, text=" 📋  Delivery Header ",
                            font=FONT_HEADER, bg=WHITE, fg=SIDEBAR,
                            bd=1, relief="solid")
        hdr.pack(fill="x", padx=14, pady=(8, 4))

        sups = self.db.fetch(
            "SELECT supplier_id, supplier_name FROM supplier ORDER BY supplier_name")
        emps = self.db.fetch(
            "SELECT employee_id, full_name FROM employee ORDER BY full_name")

        self._sup_map = {s["supplier_name"]: s["supplier_id"] for s in sups}
        self._emp_map = {e["full_name"]: e["employee_id"] for e in emps}

        # Supplier
        tk.Label(hdr, text="Supplier", font=FONT_SMALL,
                 bg=WHITE, fg=TEXT_GRAY).grid(row=0, column=0, padx=8, pady=4, sticky="w")
        self._v_sup = tk.StringVar()
        ttk.Combobox(hdr, textvariable=self._v_sup,
                     values=list(self._sup_map.keys()),
                     state="readonly", width=26).grid(row=0, column=1)

        # Date
        tk.Label(hdr, text="Date", font=FONT_SMALL,
                 bg=WHITE, fg=TEXT_GRAY).grid(row=0, column=2, padx=8, pady=4, sticky="w")
        self._v_date = tk.StringVar(value=str(date.today()))
        tk.Entry(hdr, textvariable=self._v_date, width=14).grid(row=0, column=3)

        # Employee
        tk.Label(hdr, text="Received By", font=FONT_SMALL,
                 bg=WHITE, fg=TEXT_GRAY).grid(row=1, column=0, padx=8, pady=4, sticky="w")
        self._v_emp = tk.StringVar()
        ttk.Combobox(hdr, textvariable=self._v_emp,
                     values=list(self._emp_map.keys()),
                     state="readonly", width=26).grid(row=1, column=1)

        # ✅ Reference Number (AUTO GENERATED)
        tk.Label(hdr, text="Reference No.", font=FONT_SMALL,
                 bg=WHITE, fg=TEXT_GRAY).grid(row=2, column=0, padx=8, pady=4, sticky="w")

        self._v_ref = tk.StringVar(
            value="REF-" + datetime.now().strftime("%Y%m%d%H%M%S")
        )
        tk.Entry(hdr, textvariable=self._v_ref, width=20).grid(row=2, column=1)

        # ── 2. Add Item ────────────────────────────────
        item_frame = tk.LabelFrame(self, text=" ➕ Add Item ",
                                   font=FONT_HEADER, bg=WHITE, fg=SIDEBAR)
        item_frame.pack(fill="x", padx=14, pady=4)

        prods = self.db.fetch(
            "SELECT product_id, product_name FROM product ORDER BY product_name")
        self._prod_map = {p["product_name"]: p["product_id"] for p in prods}

        # ── Labels row ──
        tk.Label(item_frame, text="Product", font=FONT_SMALL,
                 bg=WHITE, fg=TEXT_GRAY).grid(row=0, column=0, padx=8, pady=(6,0), sticky="w")
        tk.Label(item_frame, text="Quantity", font=FONT_SMALL,
                 bg=WHITE, fg=TEXT_GRAY).grid(row=0, column=1, padx=8, pady=(6,0), sticky="w")
        tk.Label(item_frame, text="Cost / Unit (₱)", font=FONT_SMALL,
                 bg=WHITE, fg=TEXT_GRAY).grid(row=0, column=2, padx=8, pady=(6,0), sticky="w")

        # ── Input row ──
        self._v_prod = tk.StringVar()
        ttk.Combobox(item_frame, textvariable=self._v_prod,
                     values=list(self._prod_map.keys()),
                     state="readonly", width=26).grid(row=1, column=0, padx=8, pady=(0,8), sticky="w")

        self._v_qty = tk.StringVar()
        tk.Entry(item_frame, textvariable=self._v_qty, width=12,
                 font=FONT_BODY, relief="solid", bd=1).grid(row=1, column=1, padx=8, pady=(0,8), sticky="w")

        self._v_cost = tk.StringVar()
        tk.Entry(item_frame, textvariable=self._v_cost, width=12,
                 font=FONT_BODY, relief="solid", bd=1).grid(row=1, column=2, padx=8, pady=(0,8), sticky="w")

        self.red_btn(item_frame, "➕  Add Item", self._add_item).grid(
            row=1, column=3, padx=8, pady=(0,8), sticky="w")

        # ── 3. Table ──────────────────────────────────
        self._stage_tree = ttk.Treeview(self, columns=("Product", "Qty", "Cost", "Total"),
                                       show="headings", height=5)
        for col in ("Product", "Qty", "Cost", "Total"):
            self._stage_tree.heading(col, text=col)
        self._stage_tree.pack(fill="x", padx=14, pady=6)

        self._lbl_total = tk.Label(self, text="Total: ₱0.00")
        self._lbl_total.pack()

        self.red_btn(self, "Post Delivery", self._post_delivery).pack(pady=10)

    # ── Add Item ─────────────────────────────────────
    def _add_item(self):
        try:
            item = {
                "product_name": self._v_prod.get(),
                "product_id": self._prod_map[self._v_prod.get()],
                "qty": int(self._v_qty.get()),
                "cost": float(self._v_cost.get())
            }
        except:
            messagebox.showerror("Error", "Invalid input")
            return

        self._items.append(item)
        self._redraw()

    def _redraw(self):
        self._stage_tree.delete(*self._stage_tree.get_children())
        total = 0
        for item in self._items:
            line = item["qty"] * item["cost"]
            total += line
            self._stage_tree.insert("", "end",
                values=(item["product_name"], item["qty"], item["cost"], line))
        self._lbl_total.config(text=f"Total: ₱{total:.2f}")

    # ── Post Delivery ────────────────────────────────
    def _post_delivery(self):

        sup = self._v_sup.get()
        emp = self._v_emp.get()
        d   = self._v_date.get()
        ref = self._v_ref.get()

        if not sup or not emp or not d or not ref:
            messagebox.showwarning("Missing", "Fill all fields")
            return

        if not self._items:
            messagebox.showwarning("Empty", "No items")
            return

        sup_id = self._sup_map[sup]
        emp_id = self._emp_map[emp]

        for item in self._items:
            self.db.execute(
                "INSERT INTO stock_batch "
                "(reference_number, supplier_id, employee_id, product_id, quantity, cost_per_unit, stockin_date) "
                "VALUES (%s,%s,%s,%s,%s,%s,%s)",
                (ref, sup_id, emp_id,
                 item["product_id"], item["qty"], item["cost"], d)
            )

        messagebox.showinfo("Success", f"Delivery {ref} saved!")

        # Reset
        self._items.clear()
        self._redraw()
        self._v_ref.set("REF-" + datetime.now().strftime("%Y%m%d%H%M%S"))