import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# ✅ Пълен списък с 28 ODMVR поддомейна
regions = [
    "blagoevgrad", "burgas", "varna", "veliko-tarnovo", "vidin", "vratsa", "gabrovo",
    "dobrich", "kardzhali", "kyustendil", "lovech", "montana", "pazardzhik",
    "pernik", "pleven", "plovdiv", "razgrad", "ruse", "silistra", "sliven", "smolyan",
    "sofia", "sofia-oblast", "stara-zagora", "targovishte", "haskovo", "shumen", "yambol"
]

# 🔍 User-Agent за избягване на 403 грешки
headers = {
    "User-Agent": "Mozilla/5.0 (compatible; crime-map-bulgaria-bot/1.0)"
}

# 📁 Къде ще запишем свалените HTML бюлетини
output_dir = "data/bulletins"
os.makedirs(output_dir, exist_ok=True)

today = datetime.today().strftime("%Y-%m-%d")
new_bulletins_found = False

for region in regions:
    try:
        print(f"🌐 Проверка на {region}...")
        base_url = f"https://{region}.mvr.bg"
        bulletin_url = f"{base_url}/press/"

        resp = requests.get(bulletin_url, headers=headers, timeout=10)
        if resp.status_code == 403:
            print(f"[!] Достъп забранен (403) за {region}")
            continue
        elif resp.status_code != 200:
            print(f"[!] Грешка при {region}: HTTP {resp.status_code}")
            continue

        soup = BeautifulSoup(resp.text, "html.parser")
        links = soup.find_all("a", href=True)

        for link in links:
            href = link['href']
            if "bulletin" in href or "presscenter" in href:
                full_url = href if href.startswith("http") else base_url + href
                filename = f"{region}_{today}.html"
                filepath = os.path.join(output_dir, filename)

                if os.path.exists(filepath):
                    print(f"[✓] Вече имаме: {filename}")
                    continue

                b_resp = requests.get(full_url, headers=headers, timeout=10)
                if b_resp.status_code == 200:
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(b_resp.text)
                    print(f"[+] Записан нов бюлетин: {filename}")
                    new_bulletins_found = True
                else:
                    print(f"[✘] Неуспешно сваляне на {full_url}")

    except Exception as e:
        print(f"[‼] Грешка при {region}: {e}")

if not new_bulletins_found:
    print("🚫 Няма нови бюлетини за днес.")
