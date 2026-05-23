# ─────────────────────────────────────────────────────────────
# pages/analytics.py — Smart Analytics Page
# Implements:
#   • Hash Table  → instant product lookup display
#   • Binary Search → fast product search
#   • Merge Sort  → ranked sales leaderboard
#   • Min-Heap PQ → restock priority queue
#   • Dijkstra    → optimal supplier finder
# ─────────────────────────────────────────────────────────────

import tkinter as tk
from tkinter import ttk, messagebox

from base_page import BasePage
from config import (
    BG, WHITE, SIDEBAR, SIDEBAR_H, ACCENT,
    TEXT_DARK, TEXT_GRAY,
    FONT_TITLE, FONT_HEADER, FONT_BODY, FONT_SMALL, FONT_BTN,
)
from algorithms import (
    HashTable, binary_search, merge_sort, MinHeap, SupplierGraph,
)


class AnalyticsPage(BasePage):

    def build(self):
        self.section_label("🧠  Smart Analytics (DSA Engine)")

        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=14, pady=8)

        # ── Tab containers ────────────────────────────────────
        t1 = tk.Frame(nb, bg=BG);  nb.add(t1, text="  🔍 Product Search  ")
        t2 = tk.Frame(nb, bg=BG);  nb.add(t2, text="  🏆 Sales Ranking  ")
        t3 = tk.Frame(nb, bg=BG);  nb.add(t3, text="  ⚠️ Restock Queue  ")
        t4 = tk.Frame(nb, bg=BG);  nb.add(t4, text="  🗺️ Supplier Optimizer  ")
        t5 = tk.Frame(nb, bg=BG);  nb.add(t5, text="  🗂️ Hash Table View  ")

        self._build_search_tab(t1)
        self._build_ranking_tab(t2)
        self._build_restock_tab(t3)
        self._build_supplier_tab(t4)
        self._build_hashtable_tab(t5)

    # ══════════════════════════════════════════════════════════
    # TAB 1 — Binary Search (Product Lookup)
    # ══════════════════════════════════════════════════════════

    def _build_search_tab(self, parent):
        tk.Label(parent,
                 text="Binary Search — O(log n)  |  Type a product name prefix",
                 font=FONT_HEADER, bg=BG, fg=SIDEBAR).pack(anchor="w", padx=10, pady=8)

        tk.Label(parent,
                 text="Products are sorted alphabetically and searched with binary search "
                      "(no linear scan). Complexity: O(log n) to locate, O(k) for k results.",
                 font=FONT_SMALL, bg=BG, fg=TEXT_GRAY, wraplength=780,
                 justify="left").pack(anchor="w", padx=10)

        # Search bar
        bar = tk.Frame(parent, bg=BG)
        bar.pack(fill="x", padx=10, pady=(8, 4))
        tk.Label(bar, text="Search:", font=FONT_BODY,
                 bg=BG, fg=TEXT_DARK).pack(side="left")
        self._v_search = tk.StringVar()
        self._v_search.trace_add("write", lambda *_: self._run_search())
        tk.Entry(bar, textvariable=self._v_search, width=30,
                 font=FONT_BODY, relief="solid", bd=1).pack(side="left", padx=6)
        self._lbl_search_info = tk.Label(bar, text="", font=FONT_SMALL,
                                         bg=BG, fg=ACCENT)
        self._lbl_search_info.pack(side="left", padx=8)

        # Results table
        cols   = ("ID", "Product", "Category", "Unit", "Price", "Stock", "Reorder")
        widths = (45, 180, 120, 70, 80, 70, 70)
        self._search_tree = self.make_table(parent, cols, widths, height=14)

        # Load sorted name list & hash table for fast lookup
        self._load_product_data()

    def _load_product_data(self):
        rows = self.db.fetch("""
            SELECT p.product_id, p.product_name, c.category_name,
                   p.unit, p.price, p.reorder_level,
                   COALESCE(SUM(sb.quantity),0)
                     - COALESCE((SELECT SUM(s.quantity_sold) FROM sales s
                                 WHERE s.product_id = p.product_id),0) AS stock_qty
            FROM product p
            JOIN category c ON p.category_id = c.category_id
            LEFT JOIN stock_batch sb ON sb.product_id = p.product_id
            GROUP BY p.product_id, p.product_name, c.category_name,
                     p.unit, p.price, p.reorder_level
            ORDER BY p.product_name
        """)
        # Hash Table
        self._ht = HashTable()
        self._ht.load_products(rows)
        # Sorted list for binary search
        self._sorted_names = [r["product_name"] for r in rows]
        self._run_search()

    def _run_search(self):
        q = self._v_search.get().strip()
        if q:
            import time
            t0 = time.perf_counter()
            matches = binary_search(self._sorted_names, q)
            elapsed = (time.perf_counter() - t0) * 1_000_000  # µs
            self._lbl_search_info.config(
                text=f"{len(matches)} result(s) — {elapsed:.1f} µs  [Binary Search]")
            rows = [self._ht.get(name) for name in matches if self._ht.get(name)]
        else:
            rows = self._ht.all_values()
            self._lbl_search_info.config(
                text=f"{len(rows)} total products loaded in Hash Table")

        low_ids = {r["product_id"] for r in
                   self.db.fetch("SELECT product_id FROM vw_low_stock")}
        self._search_tree.delete(*self._search_tree.get_children())
        for i, r in enumerate(rows):
            vals = (r["product_id"], r["product_name"], r["category_name"],
                    r["unit"], f"₱{float(r['price']):.2f}",
                    int(r.get("stock_qty", 0)), r["reorder_level"])
            tag = "low" if r["product_id"] in low_ids else ("odd" if i % 2 else "even")
            self._search_tree.insert("", "end", values=vals, tags=(tag,))

    # ══════════════════════════════════════════════════════════
    # TAB 2 — Merge Sort (Sales Ranking)
    # ══════════════════════════════════════════════════════════

    def _build_ranking_tab(self, parent):
        tk.Label(parent, text="Merge Sort — O(n log n)  |  Best-Selling Products",
                 font=FONT_HEADER, bg=BG, fg=SIDEBAR).pack(anchor="w", padx=10, pady=8)
        tk.Label(parent,
                 text="All sales records are sorted using Merge Sort. "
                      "No built-in sort() is used. Complexity: O(n log n), stable.",
                 font=FONT_SMALL, bg=BG, fg=TEXT_GRAY,
                 wraplength=780, justify="left").pack(anchor="w", padx=10)

        ctrl = tk.Frame(parent, bg=BG)
        ctrl.pack(fill="x", padx=10, pady=6)
        tk.Label(ctrl, text="Sort by:", font=FONT_BODY,
                 bg=BG, fg=TEXT_DARK).pack(side="left")
        self._v_sort_key = tk.StringVar(value="Total Revenue")
        ttk.Combobox(ctrl, textvariable=self._v_sort_key,
                     values=["Total Revenue", "Units Sold", "Avg Price"],
                     state="readonly", width=18).pack(side="left", padx=6)
        self.red_btn(ctrl, "Sort  ▶", self._run_ranking).pack(side="left", padx=4)
        self._lbl_sort_info = tk.Label(ctrl, text="", font=FONT_SMALL,
                                       bg=BG, fg=ACCENT)
        self._lbl_sort_info.pack(side="left", padx=8)

        cols   = ("Rank", "Product", "Category", "Units Sold",
                  "Avg Price", "Total Revenue")
        widths = (50, 190, 130, 90, 100, 120)
        self._rank_tree = self.make_table(parent, cols, widths, height=14)
        self._run_ranking()

    def _run_ranking(self):
        import time
        rows = self.db.fetch("""
            SELECT p.product_name, c.category_name,
                   SUM(s.quantity_sold) AS units_sold,
                   AVG(s.selling_price) AS avg_price,
                   SUM(s.quantity_sold * s.selling_price) AS revenue
            FROM sales s
            JOIN product p ON s.product_id = p.product_id
            JOIN category c ON p.category_id = c.category_id
            GROUP BY p.product_id, p.product_name, c.category_name
        """)
        if not rows:
            self._lbl_sort_info.config(text="No sales data yet.")
            return

        key_map = {
            "Total Revenue": lambda r: float(r["revenue"] or 0),
            "Units Sold":    lambda r: int(r["units_sold"] or 0),
            "Avg Price":     lambda r: float(r["avg_price"] or 0),
        }
        key_fn = key_map.get(self._v_sort_key.get(),
                             key_map["Total Revenue"])

        t0 = time.perf_counter()
        sorted_rows = merge_sort(rows, key=key_fn, reverse=True)
        elapsed = (time.perf_counter() - t0) * 1_000_000

        self._lbl_sort_info.config(
            text=f"{len(sorted_rows)} products — {elapsed:.1f} µs  [Merge Sort]")

        self._rank_tree.delete(*self._rank_tree.get_children())
        for rank, r in enumerate(sorted_rows, 1):
            medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(rank, f"#{rank}")
            vals = (
                medal,
                r["product_name"],
                r["category_name"],
                int(r["units_sold"] or 0),
                f"₱{float(r['avg_price'] or 0):.2f}",
                f"₱{float(r['revenue'] or 0):,.2f}",
            )
            self._rank_tree.insert("", "end", values=vals,
                                   tags=("odd" if rank % 2 else "even",))

    # ══════════════════════════════════════════════════════════
    # TAB 3 — Priority Queue / Min-Heap (Restock)
    # ══════════════════════════════════════════════════════════

    def _build_restock_tab(self, parent):
        tk.Label(parent,
                 text="Min-Heap Priority Queue — O(log n)  |  Restock Priority",
                 font=FONT_HEADER, bg=BG, fg=SIDEBAR).pack(anchor="w", padx=10, pady=8)
        tk.Label(parent,
                 text="Products are heapified by urgency ratio (stock ÷ reorder level). "
                      "Lower ratio = higher urgency. Pop operations: O(log n).",
                 font=FONT_SMALL, bg=BG, fg=TEXT_GRAY,
                 wraplength=780, justify="left").pack(anchor="w", padx=10)

        ctrl = tk.Frame(parent, bg=BG)
        ctrl.pack(fill="x", padx=10, pady=6)
        self.red_btn(ctrl, "🔄  Build Heap", self._run_restock).pack(side="left", padx=4)
        self._lbl_heap_info = tk.Label(ctrl, text="", font=FONT_SMALL,
                                       bg=BG, fg=ACCENT)
        self._lbl_heap_info.pack(side="left", padx=8)

        cols   = ("Priority", "Product", "Category", "Stock", "Reorder", "Urgency Ratio", "Status")
        widths = (70, 180, 120, 70, 80, 110, 90)
        self._heap_tree = self.make_table(parent, cols, widths, height=14)
        self._run_restock()

    def _run_restock(self):
        import time
        rows = self.db.fetch("""
            SELECT p.product_id, p.product_name, c.category_name,
                   p.reorder_level,
                   COALESCE(SUM(sb.quantity),0)
                     - COALESCE((SELECT SUM(s.quantity_sold) FROM sales s
                                 WHERE s.product_id = p.product_id),0) AS stock_qty
            FROM product p
            JOIN category c ON p.category_id = c.category_id
            LEFT JOIN stock_batch sb ON sb.product_id = p.product_id
            GROUP BY p.product_id, p.product_name, c.category_name, p.reorder_level
        """)
        if not rows:
            self._lbl_heap_info.config(text="No products found.")
            return

        t0 = time.perf_counter()
        heap = MinHeap.build_restock_queue(rows)
        sorted_items = heap.to_sorted_list()
        elapsed = (time.perf_counter() - t0) * 1_000_000

        self._lbl_heap_info.config(
            text=f"{len(sorted_items)} items heapified — {elapsed:.1f} µs  [Min-Heap]")

        self._heap_tree.delete(*self._heap_tree.get_children())
        for rank, item in enumerate(sorted_items, 1):
            stock   = int(item.get("stock_qty", 0))
            reorder = max(int(item.get("reorder_level", 1)), 1)
            ratio   = stock / reorder
            if stock == 0:
                status = "🔴 OUT"
            elif ratio <= 0.5:
                status = "🟠 URGENT"
            elif ratio <= 1.0:
                status = "🟡 LOW"
            else:
                status = "🟢 OK"
            tag = "low" if ratio <= 1.0 else ("odd" if rank % 2 else "even")
            vals = (
                f"#{rank}", item["product_name"], item["category_name"],
                stock, reorder, f"{ratio:.2f}", status,
            )
            self._heap_tree.insert("", "end", values=vals, tags=(tag,))

    # ══════════════════════════════════════════════════════════
    # TAB 4 — Dijkstra (Supplier Optimizer)
    # ══════════════════════════════════════════════════════════

    def _build_supplier_tab(self, parent):
        tk.Label(parent,
                 text="Dijkstra's Algorithm — O((V+E) log V)  |  Optimal Supplier",
                 font=FONT_HEADER, bg=BG, fg=SIDEBAR).pack(anchor="w", padx=10, pady=8)
        tk.Label(parent,
                 text="Suppliers are modelled as graph nodes. Edge weights combine "
                      "distance (km) and price index. Dijkstra finds the lowest-cost "
                      "path from the store to every supplier.",
                 font=FONT_SMALL, bg=BG, fg=TEXT_GRAY,
                 wraplength=780, justify="left").pack(anchor="w", padx=10)

        # Supplier metadata form
        meta_frame = tk.LabelFrame(parent, text=" Set Supplier Metrics ",
                                   font=FONT_SMALL, bg=WHITE, fg=SIDEBAR)
        meta_frame.pack(fill="x", padx=10, pady=6)

        tk.Label(meta_frame,
                 text="Enter Distance (km) and Price Index (1–10) for each supplier, "
                      "then click Run Dijkstra.",
                 font=FONT_SMALL, bg=WHITE, fg=TEXT_GRAY).pack(
            anchor="w", padx=8, pady=(4, 2))

        self._sup_meta_frame = tk.Frame(meta_frame, bg=WHITE)
        self._sup_meta_frame.pack(fill="x", padx=8, pady=4)

        ctrl = tk.Frame(parent, bg=BG)
        ctrl.pack(fill="x", padx=10, pady=4)
        self.red_btn(ctrl, "▶  Run Dijkstra", self._run_dijkstra).pack(side="left", padx=4)
        self._lbl_dijk_info = tk.Label(ctrl, text="", font=FONT_SMALL,
                                       bg=BG, fg=ACCENT)
        self._lbl_dijk_info.pack(side="left", padx=8)

        cols   = ("Rank", "Supplier", "Distance km", "Price Index", "Score", "Verdict")
        widths = (60, 200, 110, 110, 90, 120)
        self._dijk_tree = self.make_table(parent, cols, widths, height=10)

        self._load_supplier_meta()

    def _load_supplier_meta(self):
        """Build per-supplier distance + price_index input rows."""
        for w in self._sup_meta_frame.winfo_children():
            w.destroy()

        sups = self.db.fetch("SELECT supplier_id, supplier_name FROM supplier ORDER BY supplier_name")
        self._sup_meta: list[dict] = []

        headers = ["Supplier", "Distance (km)", "Price Index (1–10)"]
        for col, h in enumerate(headers):
            tk.Label(self._sup_meta_frame, text=h, font=FONT_SMALL,
                     bg=WHITE, fg=TEXT_GRAY, width=20, anchor="w").grid(
                row=0, column=col, padx=4, pady=2)

        for row_idx, s in enumerate(sups, 1):
            tk.Label(self._sup_meta_frame, text=s["supplier_name"],
                     font=FONT_BODY, bg=WHITE, fg=TEXT_DARK, anchor="w",
                     width=22).grid(row=row_idx, column=0, padx=4, pady=2)

            v_dist = tk.StringVar(value="5")
            tk.Entry(self._sup_meta_frame, textvariable=v_dist,
                     width=10, font=FONT_BODY, relief="solid", bd=1).grid(
                row=row_idx, column=1, padx=4, pady=2)

            v_pi = tk.StringVar(value="5")
            tk.Entry(self._sup_meta_frame, textvariable=v_pi,
                     width=10, font=FONT_BODY, relief="solid", bd=1).grid(
                row=row_idx, column=2, padx=4, pady=2)

            self._sup_meta.append({
                "supplier_name": s["supplier_name"],
                "v_dist": v_dist,
                "v_pi":   v_pi,
            })

    def _run_dijkstra(self):
        import time
        if not self._sup_meta:
            messagebox.showwarning("No Suppliers", "Add suppliers first.")
            return

        sup_list = []
        for s in self._sup_meta:
            try:
                dist = float(s["v_dist"].get())
                pi   = float(s["v_pi"].get())
                if not (1 <= pi <= 10):
                    raise ValueError
            except ValueError:
                messagebox.showerror("Invalid",
                                     f"Invalid distance/price index for '{s['supplier_name']}'.")
                return
            sup_list.append({
                "supplier_name": s["supplier_name"],
                "distance_km":   dist,
                "price_index":   pi,
            })

        t0 = time.perf_counter()
        graph   = SupplierGraph.build_from_suppliers(sup_list)
        ranked  = graph.best_supplier("Store", [s["supplier_name"] for s in sup_list])
        elapsed = (time.perf_counter() - t0) * 1_000_000

        self._lbl_dijk_info.config(
            text=f"{len(ranked)} suppliers ranked — {elapsed:.1f} µs  [Dijkstra]")

        meta_lookup = {s["supplier_name"]: s for s in sup_list}
        self._dijk_tree.delete(*self._dijk_tree.get_children())
        for rank, (name, score) in enumerate(ranked, 1):
            m = meta_lookup[name]
            medal   = {1: "🥇 Best", 2: "🥈", 3: "🥉"}.get(rank, f"#{rank}")
            verdict = "✅ Recommended" if rank == 1 else ("👍 Good" if rank == 2 else "")
            vals = (
                medal, name,
                f"{m['distance_km']:.1f} km",
                f"{m['price_index']:.0f} / 10",
                f"{score:.3f}",
                verdict,
            )
            tag = "odd" if rank % 2 else "even"
            self._dijk_tree.insert("", "end", values=vals, tags=(tag,))

    # ══════════════════════════════════════════════════════════
    # TAB 5 — Hash Table Inspector
    # ══════════════════════════════════════════════════════════

    def _build_hashtable_tab(self, parent):
        tk.Label(parent,
                 text="Hash Table — O(1) average lookup  |  Product Index",
                 font=FONT_HEADER, bg=BG, fg=SIDEBAR).pack(anchor="w", padx=10, pady=8)
        tk.Label(parent,
                 text="All products are stored in a custom separate-chaining hash table. "
                      "Lookup time: O(1) average.  Visualised below bucket-by-bucket.",
                 font=FONT_SMALL, bg=BG, fg=TEXT_GRAY,
                 wraplength=780, justify="left").pack(anchor="w", padx=10)

        ctrl = tk.Frame(parent, bg=BG)
        ctrl.pack(fill="x", padx=10, pady=6)

        tk.Label(ctrl, text="Lookup key:", font=FONT_BODY,
                 bg=BG, fg=TEXT_DARK).pack(side="left")
        self._v_ht_key = tk.StringVar()
        tk.Entry(ctrl, textvariable=self._v_ht_key, width=26,
                 font=FONT_BODY, relief="solid", bd=1).pack(side="left", padx=6)
        self.red_btn(ctrl, "Lookup O(1)", self._ht_lookup).pack(side="left", padx=4)
        self.grey_btn(ctrl, "🔄 Reload", self._ht_reload).pack(side="left", padx=4)
        self._lbl_ht_info = tk.Label(ctrl, text="", font=FONT_SMALL,
                                     bg=BG, fg=ACCENT)
        self._lbl_ht_info.pack(side="left", padx=8)

        cols   = ("Bucket #", "Product Name", "Category", "Stock", "Price")
        widths = (70, 200, 140, 70, 90)
        self._ht_tree = self.make_table(parent, cols, widths, height=14)
        self._ht_reload()

    def _ht_reload(self):
        if not hasattr(self, "_ht"):
            self._load_product_data()
        self._ht_tree.delete(*self._ht_tree.get_children())
        for bucket_idx, bucket in enumerate(self._ht._buckets):
            for key, val in bucket:
                vals = (
                    f"#{bucket_idx}",
                    val["product_name"],
                    val.get("category_name", "—"),
                    int(val.get("stock_qty", 0)),
                    f"₱{float(val['price']):.2f}",
                )
                self._ht_tree.insert("", "end", values=vals,
                                     tags=("odd" if bucket_idx % 2 else "even",))
        self._lbl_ht_info.config(
            text=f"{len(self._ht)} products, 64 buckets")

    def _ht_lookup(self):
        import time
        key = self._v_ht_key.get().strip()
        if not key:
            return
        t0  = time.perf_counter()
        val = self._ht.get(key)
        elapsed = (time.perf_counter() - t0) * 1_000_000
        if val:
            messagebox.showinfo(
                "Hash Table Lookup — O(1)",
                f"Key: \"{key}\"\n\n"
                f"Product ID : {val['product_id']}\n"
                f"Category   : {val.get('category_name','—')}\n"
                f"Price      : ₱{float(val['price']):.2f}\n"
                f"Stock      : {int(val.get('stock_qty',0))}\n\n"
                f"⏱  Lookup time: {elapsed:.2f} µs  [Hash Table]"
            )
        else:
            messagebox.showwarning(
                "Not Found",
                f'"{key}" not found in hash table.\n'
                f"⏱  {elapsed:.2f} µs — checked 1 bucket."
            )
