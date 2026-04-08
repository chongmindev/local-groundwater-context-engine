import requests
import sqlite3
from pathlib import Path
from urllib.parse import quote_plus
from datetime import datetime

DB_PATH = Path(__file__).resolve().parents[2] / "groundwater.db"

def ingest_measurements():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    OFFSET_LIMIT = 10000
    offset = 0
    latest_date = cur.execute("""
            SELECT value FROM metadata WHERE key = 'latest_date'
        """).fetchone()
    if latest_date is None:
        latest_date = ('1888-01-01',)
    while True:
        print(offset)
        sql = f"SELECT * FROM \"bfa9f262-24a1-45bd-8dc8-138bc8107266\" WHERE msmt_date > '{latest_date[0]}' LIMIT {OFFSET_LIMIT} OFFSET {offset}"
        url = f"https://data.cnra.ca.gov/api/3/action/datastore_search_sql?sql={quote_plus(sql)}"
        response = requests.get(url)
        data = response.json()["result"]["records"]
        batch = [(d["site_code"], d["msmt_date"], d["gwe"], d["wlm_qa_desc"]) for d in data]
        if len(data) == 0:
            break

        cur.executemany("""
            INSERT INTO measurements (site_code, msmt_date, gwe, wlm_qa_desc) 
            VALUES (?, ?, ?, ?)
            ON CONFLICT (site_code, msmt_date) 
            DO NOTHING
        """, batch)
        offset += OFFSET_LIMIT
    cur.execute("""
        SELECT MAX(msmt_date) FROM measurements
    """)

    cur.execute("""
        INSERT OR REPLACE INTO metadata (key, value) 
        VALUES ('latest_date', ?)
    """, (cur.fetchone()[0],))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    ingest_measurements()
