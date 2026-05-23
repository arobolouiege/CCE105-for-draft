# ─────────────────────────────────────────────
# database.py — Database Handler
# ─────────────────────────────────────────────

import tkinter.messagebox as messagebox
import mysql.connector
from mysql.connector import Error


class Database:
    """Handles all MySQL operations."""

    def __init__(self, config: dict):
        self.config = config

    def _connect(self):
        return mysql.connector.connect(**self.config)

    def fetch(self, sql: str, params: tuple = ()) -> list:
        try:
            conn = self._connect()
            cur  = conn.cursor(dictionary=True)
            cur.execute(sql, params)
            rows = cur.fetchall()
            conn.close()
            return rows
        except Error as e:
            messagebox.showerror("DB Error", str(e))
            return []

    def execute(self, sql: str, params: tuple = ()):
        try:
            conn = self._connect()
            cur  = conn.cursor()
            cur.execute(sql, params)
            conn.commit()
            lid = cur.lastrowid
            conn.close()
            return lid
        except Error as e:
            messagebox.showerror("DB Error", str(e))
            return None
