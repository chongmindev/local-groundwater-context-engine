import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "groundwater.db"

def get_measurements_by_site(site_code):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT msmt_date, gwe 
        FROM measurements 
        WHERE site_code = ?
        ORDER BY msmt_date
    """, (site_code,))
    rows = cur.fetchall()
    conn.close()
    return rows

def get_site_codes():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT DISTINCT site_code
        FROM measurements
    """)
    rows = cur.fetchall()
    site_codes = [site_code[0] for site_code in rows]
    conn.close()
    return site_codes