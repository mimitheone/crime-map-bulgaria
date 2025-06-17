import os
import pandas as pd
import folium
from geopy.geocoders import Nominatim
from time import sleep

INPUT_FILE = "data/cases.csv"
OUTPUT_MAP = "map/interactive_map.html"

# Създаваме папка, ако липсва
os.makedirs("map", exist_ok=True)

# Зареждаме CSV с извлечените случаи
df = pd.read_csv(INPUT_FILE)

# Инициализираме геокодера (със забавяне за да не ни блокират)
geolocator = Nominatim(user_agent="crime-map-bulgaria")

# Добавяме координати за всеки ред, ако липсват
def get_coords(region):
    try:
        location = geolocator.geocode(f"{region}, Bulgaria", timeout=10)
        sleep(1)  # лека пауза между заявките
        if location:
            return location.latitude, location.longitude
    except:
        return None, None
    return None, None

if "lat" not in df.columns or "lng" not in df.columns:
    df["lat"], df["lng"] = zip(*df["region"].apply(get_coords))
    df.to_csv(INPUT_FILE, index=False)
else:
    print("[ℹ️] Coordinates already present.")

# Генерираме картата
m = folium.Map(location=[42.7, 25.4], zoom_start=7)

for _, row in df.iterrows():
    if pd.notnull(row["lat"]) and pd.notnull(row["lng"]):
        popup_text = f"{row['date']} – {row['region']}<br>{row['summary']}"
        folium.Marker(
            location=[row["lat"], row["lng"]],
            popup=popup_text,
            icon=folium.Icon(color="red", icon="info-sign")
        ).add_to(m)

m.save(OUTPUT_MAP)
print(f"[🗺] Map saved to {OUTPUT_MAP}")
