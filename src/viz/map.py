import folium
from folium.plugins import FastMarkerCluster
from src.access.get_measurements import get_site_codes

def parse_coordinates(site_code):
    lat = int(site_code[0:6]) / 10000.0
    lon = -int(site_code[7:14]) / 10000.0
    return [lat, lon]

def get_all_coords():
    site_codes = get_site_codes()
    coords = []
    for site_code in site_codes:
        coords.append(parse_coordinates(site_code))
    return coords

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
    marker_cluster = FastMarkerCluster(get_all_coords()).add_to(m)
    m.save('map.html')

if __name__ == "__main__":
    draw_map()