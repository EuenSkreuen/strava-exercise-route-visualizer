import json
import os
import polyline
import folium
import webbrowser

DATA_DIR = "data"
OUTPUT_MAP = "routes_map.html"

# Create a map centered roughly at some default location
m = folium.Map(location=[60.0, 25.0], zoom_start=6)

for filename in os.listdir(DATA_DIR):
    if not filename.endswith(".json"):
        continue

    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'r') as f:
        activities = json.load(f)

    for activity in activities:
        poly = activity.get("map", {}).get("summary_polyline")
        if not poly:
            continue

        try:
            coords = polyline.decode(poly)  # List of (lat, lon)
            folium.PolyLine(coords, weight=3, opacity=0.7).add_to(m)
        except Exception as e:
            print(f"Failed to decode polyline in {filename}: {e}")

# Save the map
m.save(OUTPUT_MAP)
print(f"Map saved to {OUTPUT_MAP}")

# Open in browser
webbrowser.open(OUTPUT_MAP)
