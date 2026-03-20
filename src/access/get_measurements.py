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