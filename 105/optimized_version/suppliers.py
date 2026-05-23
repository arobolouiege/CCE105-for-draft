# ─────────────────────────────────────────────
# pages/suppliers.py — Suppliers Page
# ─────────────────────────────────────────────

import tkinter as tk
from tkinter import messagebox

from base_page import BasePage
from config import BG, WHITE, SIDEBAR, TEXT_DARK, TEXT_GRAY, FONT_HEADER, FONT_SMALL, FONT_BODY


class SuppliersPage(BasePage):

    def build(self):
        self.section_label("🏪  Suppliers")
        self._edit_id  = None
        self._all_rows = []   # cache for search filtering

        # ── Form ─────────────────────────────────────────────
        form = tk.Frame(self, bg=WHITE, bd=1, relief="solid")
        form.pack(fill="x", padx=14, pady=10)

        self._form_title = tk.Label(form, text="Add Supplier",
                                    font=FONT_HEADER, bg=WHITE, fg=SIDEBAR)
        self._form_title.grid(row=0, column=0, columnspan=4,
                              sticky="w", padx=8, pady=6)

        self._v_name    = self.labeled_entry(form, "Supplier Name", 1)
        self._v_contact = self.labeled_entry(form, "Contact No.",   2)
        self._v_address = self.labeled_entry(form, "Address",       1, col=2, width=28)

        btn_frame = tk.Frame(form, bg=WHITE)
        btn_frame.grid(row=3, column=0, columnspan=4, pady=8, padx=6, sticky="w")

        self._btn_save = self.red_btn(btn_frame, "➕  Add Supplier", self._save)
        self._btn_save.pack(side="left", padx=4)
        self._btn_cancel = self.grey_btn(btn_frame, "✖  Cancel Edit", self._clear_form)
        self.purple_btn(btn_frame, "🗑  Delete Selected", self._delete).pack(side="left", padx=4)
        self.red_btn(btn_frame, "🔄  Refresh", self._refresh).pack(side="left", padx=4)

        tk.Label(form, text="💡 Click a row to edit it.", font=FONT_SMALL,
                 bg=WHITE, fg=TEXT_GRAY).grid(row=4, column=0, columnspan=4,
                                              sticky="w", padx=8, pady=(0, 6))

        # ── Search bar ───────────────────────────────────────
        search_bar = tk.Frame(self, bg=BG)
        search_bar.pack(fill="x", padx=14, pady=(4, 0))

        tk.Label(search_bar, text="🔍 Search:", font=FONT_SMALL,
                 bg=BG, fg=TEXT_DARK).pack(side="left")
        self._v_search = tk.StringVar()
        self._v_search.trace_add("write", lambda *_: self._apply_search())
        tk.Entry(search_bar, textvariable=self._v_search, width=30,
                 font=FONT_BODY, relief="solid", bd=1).pack(side="left", padx=6)
        self.grey_btn(search_bar, "✖  Clear", self._clear_search).pack(side="left")

        # ── Table ────────────────────────────────────────────
        cols   = ("ID", "Supplier Name", "Contact No.", "Address", "Added On")
        widths = (40, 180, 110, 220, 110)
        self._tree = self.make_table(self, cols, widths)
        self._tree.bind("<<TreeviewSelect>>", self._on_select)

        self._refresh()

    # ── Search ────────────────────────────────────────────────

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

    # ── CRUD ──────────────────────────────────────────────────

    def _refresh(self):
        self._all_rows = self.db.fetch("SELECT * FROM supplier ORDER BY supplier_name")
        self._apply_search()

    def _clear_form(self):
        for v in (self._v_name, self._v_contact, self._v_address):
            v.set("")
        self._edit_id = None
        self._form_title.config(text="Add Supplier")
        self._btn_save.config(text="➕  Add Supplier")
        self._btn_cancel.pack_forget()

    def _on_select(self, _event):
        sel = self._tree.selection()
        if not sel:
            return
        v = self._tree.item(sel[0], "values")
        self._edit_id = int(v[0])
        self._v_name.set(v[1]); self._v_contact.set(v[2]); self._v_address.set(v[3])
        self._form_title.config(text=f"✏️  Editing: {v[1]}")
        self._btn_save.config(text="💾  Save Changes")
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
        self._clear_form(); self._refresh()

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
            self._clear_form(); self._refresh()
