# pages/suppliers.py - Suppliers Page

import time
import tkinter as tk
from tkinter import messagebox

from base_page import BasePage
from config import BG, WHITE, SIDEBAR, TEXT_DARK, TEXT_GRAY, FONT_HEADER, FONT_SMALL, FONT_BODY
from algorithms import SupplierGraph


class SuppliersPage(BasePage):

    def build(self):
        self.section_label("Suppliers")
        self._edit_id = None
        self._all_rows = []
        self._metric_vars = []

        form = tk.Frame(self, bg=WHITE, bd=1, relief="solid")
        form.pack(fill="x", padx=14, pady=10)

        self._form_title = tk.Label(form, text="Add Supplier",
                                    font=FONT_HEADER, bg=WHITE, fg=SIDEBAR)
        self._form_title.grid(row=0, column=0, columnspan=4,
                              sticky="w", padx=8, pady=6)

        self._v_name = self.labeled_entry(form, "Supplier Name", 1)
        self._v_contact = self.labeled_entry(form, "Contact No.", 2)
        self._v_address = self.labeled_entry(form, "Address", 1, col=2, width=28)

        btn_frame = tk.Frame(form, bg=WHITE)
        btn_frame.grid(row=3, column=0, columnspan=4, pady=8, padx=6, sticky="w")

        self._btn_save = self.red_btn(btn_frame, "Add Supplier", self._save)
        self._btn_save.pack(side="left", padx=4)
        self._btn_cancel = self.grey_btn(btn_frame, "Cancel Edit", self._clear_form)
        self.purple_btn(btn_frame, "Delete Selected", self._delete).pack(side="left", padx=4)
        self.red_btn(btn_frame, "Refresh", self._refresh).pack(side="left", padx=4)

        tk.Label(form, text="Click a row to edit it.", font=FONT_SMALL,
                 bg=WHITE, fg=TEXT_GRAY).grid(row=4, column=0, columnspan=4,
                                              sticky="w", padx=8, pady=(0, 6))

        search_bar = tk.Frame(self, bg=BG)
        search_bar.pack(fill="x", padx=14, pady=(4, 0))

        tk.Label(search_bar, text="Search:", font=FONT_SMALL,
                 bg=BG, fg=TEXT_DARK).pack(side="left")
        self._v_search = tk.StringVar()
        self._v_search.trace_add("write", lambda *_: self._apply_search())
        tk.Entry(search_bar, textvariable=self._v_search, width=30,
                 font=FONT_BODY, relief="solid", bd=1).pack(side="left", padx=6)
        self.grey_btn(search_bar, "Clear", self._clear_search).pack(side="left")

        cols = ("ID", "Supplier Name", "Contact No.", "Address", "Added On")
        widths = (40, 180, 110, 220, 110)
        self._tree = self.make_table(self, cols, widths)
        self._tree.bind("<<TreeviewSelect>>", self._on_select)

        self._build_recommendation_panel()
        self._refresh()

    def _build_recommendation_panel(self):
        panel = tk.LabelFrame(self, text=" Supplier Recommendation ",
                              font=FONT_HEADER, bg=WHITE, fg=SIDEBAR,
                              bd=1, relief="solid")
        panel.pack(fill="x", padx=14, pady=10)

        tk.Label(panel,
                 text="Enter distance and price index, then recommend the lowest combined score.",
                 font=FONT_SMALL, bg=WHITE, fg=TEXT_GRAY).pack(anchor="w", padx=8, pady=(6, 2))

        self._metric_frame = tk.Frame(panel, bg=WHITE)
        self._metric_frame.pack(fill="x", padx=8, pady=4)

        ctrl = tk.Frame(panel, bg=WHITE)
        ctrl.pack(fill="x", padx=8, pady=4)
        self.red_btn(ctrl, "Recommend Supplier", self._recommend_supplier).pack(side="left", padx=4)
        self._lbl_recommend = tk.Label(ctrl, text="",
                                       font=FONT_SMALL, bg=WHITE, fg=SIDEBAR)
        self._lbl_recommend.pack(side="left", padx=8)

        rank_cols = ("Rank", "Supplier", "Distance km", "Price Index", "Score")
        rank_widths = (60, 200, 100, 100, 90)
        self._recommend_tree = self.make_table(panel, rank_cols, rank_widths, height=6)

    def _reload_metric_inputs(self):
        for w in self._metric_frame.winfo_children():
            w.destroy()
        self._metric_vars = []

        headers = ("Supplier", "Distance (km)", "Price Index")
        for col, header in enumerate(headers):
            tk.Label(self._metric_frame, text=header, font=FONT_SMALL,
                     bg=WHITE, fg=TEXT_GRAY, width=20, anchor="w").grid(
                row=0, column=col, padx=4, pady=2)

        for row, supplier in enumerate(self._all_rows, 1):
            tk.Label(self._metric_frame, text=supplier["supplier_name"],
                     font=FONT_BODY, bg=WHITE, fg=TEXT_DARK,
                     width=22, anchor="w").grid(row=row, column=0, padx=4, pady=2)
            v_dist = tk.StringVar(value="5")
            v_price = tk.StringVar(value="5")
            tk.Entry(self._metric_frame, textvariable=v_dist, width=10,
                     font=FONT_BODY, relief="solid", bd=1).grid(row=row, column=1, padx=4, pady=2)
            tk.Entry(self._metric_frame, textvariable=v_price, width=10,
                     font=FONT_BODY, relief="solid", bd=1).grid(row=row, column=2, padx=4, pady=2)
            self._metric_vars.append({
                "supplier_name": supplier["supplier_name"],
                "distance": v_dist,
                "price_index": v_price,
            })

    def _recommend_supplier(self):
        if not self._metric_vars:
            messagebox.showwarning("No Suppliers", "Add suppliers first.")
            return

        suppliers = []
        for row in self._metric_vars:
            try:
                distance = float(row["distance"].get())
                price_index = float(row["price_index"].get())
                if distance < 0 or price_index < 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Invalid Metrics",
                                     f"Invalid metrics for {row['supplier_name']}.")
                return
            suppliers.append({
                "supplier_name": row["supplier_name"],
                "distance_km": distance,
                "price_index": price_index,
            })

        start = time.perf_counter()
        # SuppliersPage = Dijkstra supplier ranking by combined distance + price score.
        graph = SupplierGraph.build_from_suppliers(suppliers)
        ranked = graph.best_supplier("Store", [s["supplier_name"] for s in suppliers])
        elapsed = (time.perf_counter() - start) * 1_000_000

        lookup = {s["supplier_name"]: s for s in suppliers}
        self._recommend_tree.delete(*self._recommend_tree.get_children())
        for rank, (name, score) in enumerate(ranked, 1):
            meta = lookup[name]
            vals = (rank, name, f"{meta['distance_km']:.1f}",
                    f"{meta['price_index']:.1f}", f"{score:.3f}")
            self._recommend_tree.insert("", "end", values=vals,
                                        tags=("odd" if rank % 2 else "even",))

        if ranked:
            self._lbl_recommend.config(
                text=f"Recommended: {ranked[0][0]} - Dijkstra {elapsed:.1f} µs")

    def _apply_search(self):
        q = self._v_search.get().strip().lower()
        self._tree.delete(*self._tree.get_children())
        for i, r in enumerate(self._all_rows):
            if q in r["supplier_name"].lower() \
            or q in (r["contact_no"] or "").lower() \
            or q in (r["address"] or "").lower():
                self._tree.insert("", "end", tags=("odd" if i % 2 else "even",),
                                  values=(r["supplier_id"], r["supplier_name"],
                                          r["contact_no"], r["address"],
                                          str(r["created_at"])[:10]))

    def _clear_search(self):
        self._v_search.set("")

    def _refresh(self):
        self._all_rows = self.db.fetch("SELECT * FROM supplier ORDER BY supplier_name")
        self._apply_search()
        self._reload_metric_inputs()

    def _clear_form(self):
        for v in (self._v_name, self._v_contact, self._v_address):
            v.set("")
        self._edit_id = None
        self._form_title.config(text="Add Supplier")
        self._btn_save.config(text="Add Supplier")
        self._btn_cancel.pack_forget()

    def _on_select(self, _event):
        sel = self._tree.selection()
        if not sel:
            return
        v = self._tree.item(sel[0], "values")
        self._edit_id = int(v[0])
        self._v_name.set(v[1])
        self._v_contact.set(v[2])
        self._v_address.set(v[3])
        self._form_title.config(text=f"Editing: {v[1]}")
        self._btn_save.config(text="Save Changes")
        self._btn_cancel.pack(side="left", padx=4)

    def _save(self):
        if not self._v_name.get():
            messagebox.showwarning("Missing", "Supplier name is required.")
            return
        if self._edit_id is None:
            self.db.execute(
                "INSERT INTO supplier (supplier_name, contact_no, address) VALUES (%s,%s,%s)",
                (self._v_name.get(), self._v_contact.get(), self._v_address.get()))
            messagebox.showinfo("Success", f"Supplier '{self._v_name.get()}' added.")
        else:
            self.db.execute(
                "UPDATE supplier SET supplier_name=%s, contact_no=%s, address=%s"
                " WHERE supplier_id=%s",
                (self._v_name.get(), self._v_contact.get(),
                 self._v_address.get(), self._edit_id))
            messagebox.showinfo("Updated", f"Supplier '{self._v_name.get()}' updated.")
        self._clear_form()
        self._refresh()

    def _delete(self):
        sel = self._tree.selection()
        if not sel:
            messagebox.showwarning("No Selection", "Please click a supplier row first.")
            return
        v = self._tree.item(sel[0], "values")
        sid, sname = int(v[0]), v[1]
        if not messagebox.askyesno("Confirm Delete",
                                   f"Delete '{sname}'?\n\nThis cannot be undone."):
            return
        if self.db.execute("DELETE FROM supplier WHERE supplier_id=%s", (sid,)) is not None:
            messagebox.showinfo("Deleted", f"'{sname}' deleted.")
            self._clear_form()
            self._refresh()
