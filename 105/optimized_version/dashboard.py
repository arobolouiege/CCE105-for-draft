# ─────────────────────────────────────────────
# pages/dashboard.py — Dashboard Page
# ─────────────────────────────────────────────

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime

from base_page import BasePage
from config import BG, WHITE, SIDEBAR, ACCENT, FONT_HEADER, FONT_SMALL, FONT_BODY, TEXT_DARK, TEXT_GRAY


class DashboardPage(BasePage):

    def build(self):
        self.section_label("📦  Dashboard")

        # ── Stat Cards ───────────────────────────────────────────────────
        self._stats_frame = tk.Frame(self, bg=BG)
        self._stats_frame.pack(fill="x", padx=14, pady=10)
        self._draw_stats()

        # ── Record a Sale (1-to-many cart) ───────────────────────────────
        tk.Label(self, text="🛍️  Record a Sale",
                 font=FONT_HEADER, bg=BG, fg=TEXT_DARK).pack(
            anchor="w", padx=14, pady=(14, 2))

        sale_outer = tk.LabelFrame(self, text=" 🛒  Sale Transaction ",
                                   font=FONT_HEADER, bg=WHITE, fg=SIDEBAR,
                                   bd=1, relief="solid")
        sale_outer.pack(fill="x", padx=14, pady=(0, 8))

        # ── Add-item row ─────────────────────────────────────────────────
        add_row = tk.Frame(sale_outer, bg=WHITE)
        add_row.pack(fill="x", padx=8, pady=(8, 4))

        # Product label + combo
        tk.Label(add_row, text="Product", font=FONT_SMALL,
                 bg=WHITE, fg=TEXT_GRAY).grid(row=0, column=0, sticky="w", padx=(0, 4))
        self._v_prod = tk.StringVar()
        self._v_prod.trace_add("write", self._on_product_select)
        self._prod_combo = ttk.Combobox(add_row, textvariable=self._v_prod,
                                        state="readonly", width=28)
        self._prod_combo.grid(row=1, column=0, padx=(0, 8), sticky="w")

        # Qty label + entry
        tk.Label(add_row, text="Quantity", font=FONT_SMALL,
                 bg=WHITE, fg=TEXT_GRAY).grid(row=0, column=1, sticky="w")
        self._v_qty = tk.StringVar()
        tk.Entry(add_row, textvariable=self._v_qty, width=8,
                 font=FONT_BODY, relief="solid", bd=1).grid(
            row=1, column=1, padx=(0, 8), sticky="w")

        # Price label + entry
        tk.Label(add_row, text="Selling Price (₱)", font=FONT_SMALL,
                 bg=WHITE, fg=TEXT_GRAY).grid(row=0, column=2, sticky="w")
        self._v_price = tk.StringVar()
        tk.Entry(add_row, textvariable=self._v_price, width=10,
                 font=FONT_BODY, relief="solid", bd=1).grid(
            row=1, column=2, padx=(0, 8), sticky="w")

        # Stock hint
        self._lbl_stock = tk.Label(add_row, text="Stock: —",
                                   font=FONT_SMALL, bg=WHITE, fg=ACCENT)
        self._lbl_stock.grid(row=0, column=3, sticky="w", padx=(0, 8))

        # ➕ Add to cart
        self.red_btn(add_row, "➕  Add Item", self._add_item).grid(
            row=1, column=3, padx=(0, 8), sticky="w")

        # ── Cart staging table ───────────────────────────────────────────
        cart_frame = tk.Frame(sale_outer, bg=WHITE)
        cart_frame.pack(fill="x", padx=8, pady=4)

        self._cart_tree = ttk.Treeview(
            cart_frame,
            columns=("Product", "Qty", "Price", "Line Total"),
            show="headings", height=5
        )
        col_cfg = [("Product", 230), ("Qty", 60), ("Price", 100), ("Line Total", 100)]
        for col, w in col_cfg:
            self._cart_tree.heading(col, text=col)
            self._cart_tree.column(col, width=w, anchor="w")
        self._cart_tree.pack(side="left", fill="x", expand=True)

        vsb = ttk.Scrollbar(cart_frame, orient="vertical",
                            command=self._cart_tree.yview)
        self._cart_tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")

        # ── Cart footer: total + action buttons ──────────────────────────
        footer = tk.Frame(sale_outer, bg=WHITE)
        footer.pack(fill="x", padx=8, pady=(4, 10))

        self._lbl_cart_total = tk.Label(
            footer, text="Cart Total:  ₱0.00",
            font=("Georgia", 12, "bold"), bg=WHITE, fg=SIDEBAR)
        self._lbl_cart_total.pack(side="left", padx=8)

        self.red_btn(footer, "💰  Post Sale", self._post_sale).pack(
            side="right", padx=4)
        self.grey_btn(footer, "🗑  Remove Selected", self._remove_item).pack(
            side="right", padx=4)
        self.grey_btn(footer, "✖  Clear Cart", self._clear_cart).pack(
            side="right", padx=4)

        # Internal cart state: list of dicts
        self._cart: list[dict] = []

        # Load product list
        self._reload_products()

        # ── Recent Sales Table ───────────────────────────────────────────
        tk.Label(self, text="📋  Recent Sales",
                 font=FONT_HEADER, bg=BG, fg=TEXT_DARK).pack(
            anchor="w", padx=14, pady=(10, 2))

        sale_cols   = ("Date & Time", "Product", "Qty Sold", "Selling Price", "Total")
        sale_widths = (140, 220, 80, 110, 100)
        self._sale_tree = self.make_table(self, sale_cols, sale_widths, height=8)

        self.red_btn(self, "🔄  Refresh Sales", self._refresh_sales).pack(
            anchor="w", padx=14, pady=(0, 8))

        # ── Recent Stock-In Table ────────────────────────────────────────
        tk.Label(self, text="📥  Recent Stock-In Transactions",
                 font=FONT_HEADER, bg=BG, fg=TEXT_DARK).pack(
            anchor="w", padx=14, pady=(10, 2))

        si_cols   = ("Date", "Product", "Supplier", "Received By", "Qty", "Cost/Unit", "Total")
        si_widths = (90, 160, 130, 130, 60, 80, 80)
        self._si_tree = self.make_table(self, si_cols, si_widths, height=8)

        self._refresh_sales()
        self._refresh_stockin()

    # ── Product loader ───────────────────────────────────────────────────

    def _reload_products(self):
        """Fetch products with computed stock (stock_batch - sales)."""
        rows = self.db.fetch("""
            SELECT
                p.product_id,
                p.product_name,
                p.price,
                COALESCE(SUM(sb.quantity), 0)
                  - COALESCE((SELECT SUM(s.quantity_sold)
                              FROM sales s
                              WHERE s.product_id = p.product_id), 0)
                AS stock_qty
            FROM product p
            LEFT JOIN stock_batch sb ON sb.product_id = p.product_id
            GROUP BY p.product_id, p.product_name, p.price
            ORDER BY p.product_name
        """)
        self._prod_map = {
            r["product_name"]: {
                "id":    r["product_id"],
                "price": float(r["price"]),
                "stock": int(r["stock_qty"]),
            }
            for r in rows
        }
        self._prod_combo["values"] = list(self._prod_map.keys())

    # ── Stat Cards ───────────────────────────────────────────────────────

    def _draw_stats(self):
        for w in self._stats_frame.winfo_children():
            w.destroy()

        total    = self.db.fetch("SELECT COUNT(*) AS n FROM product")[0]["n"]
        low      = self.db.fetch("SELECT COUNT(*) AS n FROM vw_low_stock")[0]["n"]
        sup      = self.db.fetch("SELECT COUNT(*) AS n FROM supplier")[0]["n"]
        today_si = self.db.fetch(
            "SELECT COUNT(*) AS n FROM stock_batch WHERE stockin_date = %s",
            (date.today(),))[0]["n"]
        today_rev = self.db.fetch(
            "SELECT COALESCE(SUM(quantity_sold * selling_price), 0) AS rev "
            "FROM sales WHERE DATE(sale_date) = %s",
            (date.today(),))[0]["rev"]

        for title, val, color in [
            ("Total Products",   total,                "#C0392B"),
            ("Low Stock Alerts", low,                  "#E67E22"),
            ("Suppliers",        sup,                  "#27AE60"),
            ("Stock-Ins Today",  today_si,             "#2980B9"),
            ("Revenue Today",    f"₱{today_rev:,.2f}", "#8E44AD"),
        ]:
            self._stat_card(self._stats_frame, title, val, color)

    def _stat_card(self, parent, title: str, val, color: str):
        card = tk.Frame(parent, bg=color, width=160, height=80)
        card.pack_propagate(False)
        card.pack(side="left", padx=8)
        tk.Label(card, text=val,   font=("Georgia", 16, "bold"),
                 bg=color, fg=WHITE).pack(pady=(12, 0))
        tk.Label(card, text=title, font=FONT_SMALL,
                 bg=color, fg=WHITE).pack()

    # ── Product selection ─────────────────────────────────────────────────

    def _on_product_select(self, *_):
        name = self._v_prod.get()
        if name not in self._prod_map:
            return
        info = self._prod_map[name]
        self._v_price.set(f"{info['price']:.2f}")
        stock = info["stock"]
        self._lbl_stock.config(
            text=f"Stock: {stock}",
            fg=ACCENT if stock <= 5 else "#27AE60"
        )

    # ── Cart helpers ──────────────────────────────────────────────────────

    def _add_item(self):
        """Validate and stage one item into the cart."""
        prod_name = self._v_prod.get()
        if not prod_name or prod_name not in self._prod_map:
            messagebox.showwarning("Missing", "Please select a product.")
            return

        try:
            qty   = int(self._v_qty.get())
            price = float(self._v_price.get())
            if qty <= 0 or price < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid", "Enter a valid quantity and selling price.")
            return

        prod = self._prod_map[prod_name]

        # Check available stock minus what's already in the cart for this product
        already_in_cart = sum(
            item["qty"] for item in self._cart
            if item["product_id"] == prod["id"]
        )
        available = prod["stock"] - already_in_cart

        if qty > available:
            messagebox.showerror(
                "Insufficient Stock",
                f"Only {available} unit(s) of '{prod_name}' available "
                f"(stock: {prod['stock']}, already in cart: {already_in_cart})."
            )
            return

        # Check if product already in cart — merge quantities
        for item in self._cart:
            if item["product_id"] == prod["id"] and item["price"] == price:
                item["qty"] += qty
                self._redraw_cart()
                self._clear_item_inputs()
                return

        # New cart line
        self._cart.append({
            "product_name": prod_name,
            "product_id":   prod["id"],
            "qty":          qty,
            "price":        price,
        })
        self._redraw_cart()
        self._clear_item_inputs()

    def _remove_item(self):
        """Remove the selected row from the cart."""
        sel = self._cart_tree.selection()
        if not sel:
            messagebox.showwarning("No Selection", "Click a cart row to remove it.")
            return
        idx = self._cart_tree.index(sel[0])
        del self._cart[idx]
        self._redraw_cart()

    def _clear_cart(self):
        self._cart.clear()
        self._redraw_cart()

    def _redraw_cart(self):
        """Refresh the cart treeview and update the running total."""
        self._cart_tree.delete(*self._cart_tree.get_children())
        grand_total = 0.0
        for i, item in enumerate(self._cart):
            line = item["qty"] * item["price"]
            grand_total += line
            self._cart_tree.insert(
                "", "end",
                values=(
                    item["product_name"],
                    item["qty"],
                    f"₱{item['price']:.2f}",
                    f"₱{line:,.2f}",
                ),
                tags=("odd" if i % 2 else "even",)
            )
        self._lbl_cart_total.config(text=f"Cart Total:  ₱{grand_total:,.2f}")

    def _clear_item_inputs(self):
        """Reset the add-item row without touching the cart."""
        self._v_prod.set("")
        self._v_qty.set("")
        self._v_price.set("")
        self._lbl_stock.config(text="Stock: —", fg=ACCENT)

    # ── Post Sale (commits whole cart) ───────────────────────────────────

    def _post_sale(self):
        if not self._cart:
            messagebox.showwarning("Empty Cart", "Add at least one item before posting.")
            return

        # Final stock check for every item (in case stock changed)
        self._reload_products()
        cart_usage: dict[int, int] = {}
        for item in self._cart:
            cart_usage[item["product_id"]] = (
                cart_usage.get(item["product_id"], 0) + item["qty"]
            )

        for pid, total_qty in cart_usage.items():
            prod_name = next(
                (n for n, d in self._prod_map.items() if d["id"] == pid), str(pid)
            )
            if total_qty > self._prod_map[prod_name]["stock"]:
                messagebox.showerror(
                    "Insufficient Stock",
                    f"Not enough stock for '{prod_name}'. "
                    f"Available: {self._prod_map[prod_name]['stock']}, "
                    f"needed: {total_qty}."
                )
                return

        # Commit every cart line to the sales table
        for item in self._cart:
            self.db.execute(
                "INSERT INTO sales (product_id, quantity_sold, selling_price) "
                "VALUES (%s, %s, %s)",
                (item["product_id"], item["qty"], item["price"])
            )

        lines     = len(self._cart)
        grand     = sum(i["qty"] * i["price"] for i in self._cart)
        summary   = "\n".join(
            f"  • {i['product_name']}  ×{i['qty']}  @ ₱{i['price']:.2f}"
            for i in self._cart
        )

        messagebox.showinfo(
            "Sale Posted ✅",
            f"{lines} item(s) recorded:\n{summary}\n\n"
            f"Grand Total: ₱{grand:,.2f}"
        )

        # Reset cart and inputs
        self._cart.clear()
        self._redraw_cart()
        self._clear_item_inputs()

        # Refresh everything
        self._reload_products()
        self._refresh_sales()
        self._refresh_stockin()
        self._draw_stats()

    # ── Table refreshes ──────────────────────────────────────────────────

    def _refresh_sales(self):
        rows = self.db.fetch("""
            SELECT s.sale_date, p.product_name,
                   s.quantity_sold, s.selling_price,
                   (s.quantity_sold * s.selling_price) AS total
            FROM sales s
            JOIN product p ON s.product_id = p.product_id
            ORDER BY s.sale_date DESC
            LIMIT 30
        """)
        self._sale_tree.delete(*self._sale_tree.get_children())
        for i, r in enumerate(rows):
            vals = (
                str(r["sale_date"]),
                r["product_name"],
                r["quantity_sold"],
                f"₱{float(r['selling_price']):.2f}",
                f"₱{float(r['total']):.2f}",
            )
            self._sale_tree.insert("", "end", values=vals,
                                   tags=("odd" if i % 2 else "even",))

    def _refresh_stockin(self):
        rows = self.db.fetch("""
            SELECT stockin_date, product_name, supplier_name,
                   received_by, quantity, cost_per_unit, total_cost
            FROM vw_daily_stockin
            ORDER BY stockin_date DESC
            LIMIT 20
        """)
        self._si_tree.delete(*self._si_tree.get_children())
        for i, r in enumerate(rows):
            vals = (
                r["stockin_date"], r["product_name"], r["supplier_name"],
                r["received_by"], r["quantity"],
                f"₱{float(r['cost_per_unit']):.2f}",
                f"₱{float(r['total_cost']):.2f}",
            )
            self._si_tree.insert("", "end", values=vals,
                                  tags=("odd" if i % 2 else "even",))
