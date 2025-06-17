import pandas as pd
import folium
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import os

# Зареждаме данните
df = pd.read_csv("data/cases.csv")

# Създаваме координати, ако липсват
geolocator = Nominatim(user_agent="crime-map-bulgaria")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

def resolve_coordinates(region):
    try:
        location = geocode(f"{region}, Bulgaria")
        return location.latitude, location.longitude if location else (None, None)
    except:
        return (None, None)

# Добавяме координати
df["lat"] = None
df["lng"] = None

for i, row in df.iterrows():
    latlng = resolve_coordinates(row["region"])
    if latlng:
        df.at[i, "lat"], df.at[i, "lng"] = latlng

# Създаваме карта
m = folium.Map(location=[42.7, 25.3], zoom_start=7)

for _, row in df.iterrows():
    if pd.notnull(row["lat"]) and pd.notnull(row["lng"]):
        folium.Marker(
            location=[row["lat"], row["lng"]],
            popup=f"{row['date']} – {row['region']}<br>{row['context']}",
            icon=folium.Icon(color="red", icon="info-sign")
        ).add_to(m)

# Запазваме
os.makedirs("map", exist_ok=True)
m.save("map/interactive_map.html")
print("[✔] Map generated at map/interactive_map.html")
