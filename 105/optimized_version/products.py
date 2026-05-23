# ─────────────────────────────────────────────
# pages/products.py — Products Page
# ─────────────────────────────────────────────

import tkinter as tk
from tkinter import messagebox

from base_page import BasePage
from config import WHITE, SIDEBAR, TEXT_GRAY, FONT_HEADER, FONT_SMALL


class ProductsPage(BasePage):

    def build(self):
        self.section_label("🛒  Products")
        self._edit_id = None

        form = tk.Frame(self, bg=WHITE, bd=1, relief="solid")
        form.pack(fill="x", padx=14, pady=10)

        self._form_title = tk.Label(form, text="Add New Product",
                                    font=FONT_HEADER, bg=WHITE, fg=SIDEBAR)
        self._form_title.grid(row=0, column=0, columnspan=4,
                              sticky="w", padx=8, pady=6)

        cats = self.db.fetch(
            "SELECT category_id, category_name FROM category ORDER BY category_name")
        self._cat_map = {c["category_name"]: c["category_id"] for c in cats}

        self._v_name  = self.labeled_entry(form, "Product Name",  1)
        self._v_unit  = self.labeled_entry(form, "Unit",           2)
        self._v_price = self.labeled_entry(form, "Price (₱)",      3)
        self._v_reord = self.labeled_entry(form, "Reorder Level",  4)
        self._v_cat, _ = self.labeled_combo(
            form, "Category", 1, list(self._cat_map.keys()), col=2)

        cols   = ("ID", "Product", "Category", "Unit", "Price", "Stock Qty", "Reorder")
        widths = (40, 170, 120, 70, 80, 80, 80)
        self._tree = self.make_table(self, cols, widths)
        self._tree.bind("<<TreeviewSelect>>", self._on_select)

        btn_frame = tk.Frame(form, bg=WHITE)
        btn_frame.grid(row=5, column=0, columnspan=4, pady=8, padx=6, sticky="w")

        self._btn_save = self.red_btn(btn_frame, "➕  Add Product", self._save)
        self._btn_save.pack(side="left", padx=4)

        self._btn_cancel = self.grey_btn(btn_frame, "✖  Cancel Edit", self._clear_form)

        self.purple_btn(btn_frame, "🗑  Delete Selected", self._delete).pack(
            side="left", padx=4)
        self.red_btn(btn_frame, "🔄  Refresh", self._refresh).pack(
            side="left", padx=4)

        tk.Label(form, text="💡 Click a row to edit it.", font=FONT_SMALL,
                 bg=WHITE, fg=TEXT_GRAY).grid(row=6, column=0, columnspan=4,
                                              sticky="w", padx=8, pady=(0, 6))
        self._refresh()

    def _refresh(self):
        rows = self.db.fetch("""
            SELECT
                p.product_id,
                p.product_name,
                c.category_name,
                p.unit,
                p.price,
                p.reorder_level,
                COALESCE(SUM(sb.quantity), 0)
                  - COALESCE((SELECT SUM(s.quantity_sold)
                              FROM sales s
                              WHERE s.product_id = p.product_id), 0)
                AS stock_qty
            FROM product p
            JOIN category c ON p.category_id = c.category_id
            LEFT JOIN stock_batch sb ON sb.product_id = p.product_id
            GROUP BY p.product_id, p.product_name, c.category_name,
                     p.unit, p.price, p.reorder_level
            ORDER BY c.category_name, p.product_name
        """)
        low_ids = {r["product_id"] for r in
                   self.db.fetch("SELECT product_id FROM vw_low_stock")}
        self._tree.delete(*self._tree.get_children())
        for i, r in enumerate(rows):
            vals = (r["product_id"], r["product_name"], r["category_name"],
                    r["unit"], f"₱{float(r['price']):.2f}",
                    int(r["stock_qty"]), r["reorder_level"])
            tag = "low" if r["product_id"] in low_ids else ("odd" if i % 2 else "even")
            self._tree.insert("", "end", values=vals, tags=(tag,))

    def _clear_form(self):
        for v in (self._v_name, self._v_unit, self._v_price, self._v_reord):
            v.set("")
        self._v_cat.set("")
        self._edit_id = None
        self._form_title.config(text="Add New Product")
        self._btn_save.config(text="➕  Add Product")
        self._btn_cancel.pack_forget()

    def _on_select(self, _event):
        sel = self._tree.selection()
        if not sel:
            return
        vals = self._tree.item(sel[0], "values")
        self._edit_id = int(vals[0])
        self._v_name.set(vals[1])
        self._v_cat.set(vals[2])
        self._v_unit.set(vals[3])
        self._v_price.set(vals[4].replace("₱", ""))
        self._v_reord.set(vals[6])
        self._form_title.config(text=f"✏️  Editing: {vals[1]}")
        self._btn_save.config(text="💾  Save Changes")
        self._btn_cancel.pack(side="left", padx=4)

    def _save(self):
        if not self._v_name.get() or not self._v_cat.get() or not self._v_price.get():
            messagebox.showwarning("Missing", "Fill in Name, Category and Price.")
            return
        try:
            price  = float(self._v_price.get())
            reord  = int(self._v_reord.get() or 5)
            unit   = self._v_unit.get() or "piece"
            cat_id = self._cat_map[self._v_cat.get()]
        except (ValueError, KeyError):
            messagebox.showerror("Error", "Invalid price, reorder level, or category.")
            return

        if self._edit_id is None:
            self.db.execute(
                "INSERT INTO product (category_id, product_name, unit, price, reorder_level)"
                " VALUES (%s,%s,%s,%s,%s)",
                (cat_id, self._v_name.get(), unit, price, reord))
            messagebox.showinfo("Success", f"Product '{self._v_name.get()}' added.")
        else:
            self.db.execute(
                "UPDATE product SET category_id=%s, product_name=%s, unit=%s,"
                " price=%s, reorder_level=%s WHERE product_id=%s",
                (cat_id, self._v_name.get(), unit, price, reord, self._edit_id))
            messagebox.showinfo("Updated", f"Product '{self._v_name.get()}' updated.")

        self._clear_form()
        self._refresh()

    def _delete(self):
        sel = self._tree.selection()
        if not sel:
            messagebox.showwarning("No Selection", "Please click a product row first.")
            return
        vals = self._tree.item(sel[0], "values")
        pid, pname = int(vals[0]), vals[1]
        if not messagebox.askyesno("Confirm Delete",
                                   f"Delete '{pname}'?\n\nThis cannot be undone."):
            return
        if self.db.execute("DELETE FROM product WHERE product_id=%s", (pid,)) is not None:
            messagebox.showinfo("Deleted", f"'{pname}' deleted.")
            self._clear_form()
            self._refresh()
