import folium
from folium.plugins import MarkerCluster
from src.access.get_measurements import get_site_codes
from src.compute.site_stats import compute_site_stats, classify
import datetime
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "groundwater.db"
INDEX_PATH = Path(__file__).resolve().parents[2] / "docs/index.html"
MAP_PATH = Path(__file__).resolve().parents[2] / "docs/map.html"


def parse_coordinates(site_code):
    lat = int(site_code[0:6]) / 10000.0
    lon = -int(site_code[7:14]) / 10000.0
    return [lat, lon]


def get_limited_site_codes():
    site_codes = get_site_codes()
    valid_site_codes = []

    for site_code in site_codes:
        site_stats = compute_site_stats(site_code)

        if site_stats is None:
            continue

        valid_site_codes.append(site_code)

    return valid_site_codes


def get_marker_msg(site_code, site_stats, trend):
    if site_stats is None:
        return f"Site: {site_code}<br>Insufficient data"

    return (
        f"Site: {site_code}<br>"
        f"Status: {trend}<br>"
        f"Change: {site_stats['change']:.2f} ft<br>"
        f"P-value: {site_stats['p_value']:.3f}"
    )


def add_site_marker(marker_cluster, site_code):
    coords = parse_coordinates(site_code)

    site_stats = compute_site_stats(site_code)
    if site_stats is None:
        return

    trend = classify(site_stats["change"], site_stats["p_value"])
    popup_text = get_marker_msg(site_code, site_stats, trend)

    folium.Marker(
        location=coords,
        popup=folium.Popup(popup_text, max_width=300),
    ).add_to(marker_cluster)


def draw_map():
    min_lat, max_lat = 32.5121 - 5, 42.0126 + 5
    min_lon, max_lon = -124.6509 - 5, -114.1315 + 5

    m = folium.Map(
        max_bounds=True,
        location=[37.4277, -122.1701],
        zoom_start=6,
        min_lat=min_lat,
        max_lat=max_lat,
        min_lon=min_lon,
        max_lon=max_lon,
    )

    marker_cluster = MarkerCluster().add_to(m)

    for site_code in get_limited_site_codes():
        add_site_marker(marker_cluster, site_code)

    m.save(MAP_PATH)


def update_index_html():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    latest_date = cur.execute("""
        SELECT value
        FROM metadata
        WHERE key = 'latest_date'
    """).fetchone()

    if latest_date is None or latest_date[0] is None:
        updated_text = "Update unavailable"
    else:
        latest_dt = datetime.datetime.fromisoformat(latest_date[0])
        now = datetime.datetime.now()
        delta = (now.date() - latest_dt.date()).days

        if delta == 0:
            updated_text = "Updated today"
        elif delta == 1:
            updated_text = "Updated yesterday"
        else:
            updated_text = f"Updated {delta} days ago"

    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        html = f.read()

    html = html.replace("LAST_UPDATED_PLACEHOLDER", updated_text)

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(html)

    conn.close()


def main():
    draw_map()
    update_index_html()


if __name__ == "__main__":
    main()