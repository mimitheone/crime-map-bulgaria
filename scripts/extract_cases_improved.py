import os
import re
import csv
from datetime import datetime

INPUT_DIR = "data/bulletins"
OUTPUT_FILE = "data/cases.csv"

KEYWORDS = [
    "убийство", "убит", "убита", "убити", "убитият", "смърт",
    "труп", "умъртвяване", "намерен мъртъв", "починал", "смъртта"
]

def extract_cases_from_html(html):
    cases = []
    # Вадим всички параграфи, заглавия и текстови блокове
    paragraphs = re.findall(r'>([^<>]{15,500})<', html)
    for para in paragraphs:
        if any(kw in para.lower() for kw in KEYWORDS):
            context = para.strip().replace('\n', ' ')
            date_match = re.search(r'(\d{1,2}[\.\-/]\d{1,2}[\.\-/]\d{2,4})', html)
            date = date_match.group(1) if date_match else datetime.today().strftime('%Y-%m-%d')
            cases.append({
                "date": date,
                "context": context[:300] + ("..." if len(context) > 300 else "")
            })
    return cases

all_cases = []
for filename in os.listdir(INPUT_DIR):
    if filename.endswith(".html"):
        with open(os.path.join(INPUT_DIR, filename), encoding="utf-8") as f:
            html = f.read()
            region = filename.split("_")[0]
            cases = extract_cases_from_html(html)
            for case in cases:
                case["region"] = region
            all_cases.extend(cases)

# Запис в CSV
os.makedirs("data", exist_ok=True)
with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["date", "region", "context"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for case in all_cases:
        writer.writerow(case)

print(f"[✔] Extracted {len(all_cases)} cases.")
