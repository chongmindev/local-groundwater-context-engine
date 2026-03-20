import folium
from folium.plugins import MarkerCluster
from src.access.get_measurements import get_site_codes
from src.compute.site_stats import compute_site_stats
import random

SEED_RANDOM = 42
MAX_MARKERS = 4000

def parse_coordinates(site_code):
    lat = int(site_code[0:6]) / 10000.0
    lon = -int(site_code[7:14]) / 10000.0
    return [lat, lon]

def get_limited_site_codes(limit=MAX_MARKERS):
    site_codes = get_site_codes()
    random.seed(SEED_RANDOM)
    random.shuffle(site_codes)
    valid_site_codes = []

    for site_code in site_codes:
        site_score, site_confidence = compute_site_stats(site_code)

        if site_score is None or site_confidence is None:
            continue

        valid_site_codes.append(site_code)

        if len(valid_site_codes) >= limit:
            break

    return valid_site_codes

def add_site_marker(marker_cluster, site_code):
    coords = parse_coordinates(site_code)

    site_score, site_confidence = compute_site_stats(site_code)

    popup_text = f"Site code: {site_code}\n"

    if site_score is not None and site_confidence is not None:
        popup_text += f"Score: {site_score:.2f}\n"
        popup_text += f"Confidence: {site_confidence:.2f}"
    else:
        popup_text += "Score: N/A\nConfidence: N/A"

    folium.Marker(
        location=coords,
        popup=popup_text
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

    m.save("map.html")

if __name__ == "__main__":
    draw_map()