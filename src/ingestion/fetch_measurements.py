import requests
import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).resolve().parents[2] / "groundwater.db"
url = 'https://data.cnra.ca.gov/api/3/action/datastore_search?resource_id=bfa9f262-24a1-45bd-8dc8-138bc8107266&limit=5'  
response = requests.get(url)
data = response.json()["result"]["records"]

print("Writing to:", DB_PATH)
print("Records pulled:", len(data))

conn = sqlite3.connect("groundwater.db")
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS measurements (
        site_code TEXT,
        msmt_date TEXT,
        gwe REAL,
        wlm_qa_desc TEXT,
        UNIQUE(site_code, msmt_date)
    )
    """)

for row in data:
    cur.execute("""
        INSERT OR IGNORE INTO measurements (site_code, msmt_date, gwe, wlm_qa_desc) 
        VALUES (?, ?, ?, ?)
    """, (row["site_code"], row["msmt_date"], row["gwe"], row["wlm_qa_desc"]))

conn.commit()
conn.close()
