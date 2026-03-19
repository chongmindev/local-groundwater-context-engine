import requests
import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).resolve().parents[2] / "groundwater.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

OFFSET_LIMIT = 1000
offset = 0
while True:
    print(offset)
    url = f'https://data.cnra.ca.gov/api/3/action/datastore_search?resource_id=bfa9f262-24a1-45bd-8dc8-138bc8107266&limit={OFFSET_LIMIT}&offset={offset}'
    response = requests.get(url)
    data = response.json()["result"]["records"]
    batch = [(d["site_code"], d["msmt_date"], d["gwe"], d["wlm_qa_desc"]) for d in data]
    if len(data) == 0:
        break

    cur.executemany("""
        INSERT OR IGNORE INTO measurements (site_code, msmt_date, gwe, wlm_qa_desc) 
        VALUES (?, ?, ?, ?)
    """, batch)
    offset += OFFSET_LIMIT


conn.commit()
conn.close()
