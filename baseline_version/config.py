# ─────────────────────────────────────────────
# config.py — App Configuration
# ─────────────────────────────────────────────

# ── Database connection (edit these to match your MySQL/MariaDB setup) ──
DB_CONFIG = {
    "host":     "127.0.0.1",
    "port":     3306,
    "user":     "root",        # ← your MySQL username
    "password": "",            # ← your MySQL password
    "database": "sari_sari_store",
}

# ── Colour palette ──────────────────────────────────────────────────────
BG        = "#F5F0EB"
WHITE     = "#FFFFFF"
SIDEBAR   = "#8B2635"
SIDEBAR_H = "#A63245"
ACCENT    = "#C0392B"
TEXT_DARK = "#2C2C2C"
TEXT_GRAY = "#7F8C8D"
ROW_ODD   = "#FDF6F0"
ROW_EVEN  = "#FFFFFF"
ROW_LOW   = "#FDECEA"
ROW_LOW   = "#FDECEA"

# ── Fonts ───────────────────────────────────────────────────────────────
FONT_TITLE  = ("Georgia",    16, "bold")
FONT_HEADER = ("Georgia",    13, "bold")
FONT_BODY   = ("Helvetica",  11)
FONT_SMALL  = ("Helvetica",  10)
FONT_BTN    = ("Helvetica",  11, "bold")
