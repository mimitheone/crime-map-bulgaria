import os
import requests
from datetime import datetime, timedelta

# Настройка
output_dir = "data/bulletins"
os.makedirs(output_dir, exist_ok=True)

# Публични URL адреси за МВР бюлетини (примерни, HTML)
BASE_URLS = {
    "varna": "https://varna.mvr.bg",
    "burgas": "https://burgas.mvr.bg",
    "plovdiv": "https://plovdiv.mvr.bg"
}

# Това е просто демонстрация. Истинският скрипт ще иска повече логика и парсване.
# Тук ще запишем фиктивни страници (примерни) в HTML
for region, base_url in BASE_URLS.items():
    try:
        response = requests.get(base_url, timeout=10)
        if response.status_code == 200:
            filename = f"{region}_{datetime.today().strftime('%Y-%m-%d')}.html"
            filepath = os.path.join(output_dir, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(response.text)
            print(f"[✔] Saved {filename}")
        else:
            print(f"[!] Failed to fetch {region} – status code {response.status_code}")
    except Exception as e:
        print(f"[✘] Error fetching {region}: {e}")
