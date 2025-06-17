import os
import re
import csv
from bs4 import BeautifulSoup

bulletin_dir = "data/bulletins"
output_file = "data/cases.csv"

keywords = {
    "Убийство": ["убит", "убита", "убиха", "труп", "смърт", "прострелян", "удушен", "наръган", "умъртвен"],
    "Насилие": ["побой", "ударен", "бит", "нападение", "пребит", "нанесени удари", "физическа разправа"],
    "Изнасилване": ["изнасили", "изнасилване", "сексуално насилие", "изнасилена"],
    "Кражба/Грабеж": ["обир", "грабеж", "взлом", "откраднал", "открадната", "изчезнали пари", "влязъл с взлом"],
    "Палеж": ["палеж", "запалил", "пожар", "подпалил", "горял"],
    "Наркотици": ["наркотик", "дрога", "канабис", "амфетамин", "хероин", "наркотици"],
    "Измама": ["измама", "измамил", "подправен", "фалшив", "нелегален", "фалшифициран"],
    "Оръжие": ["оръжие", "пистолет", "нож", "взрив", "взривно устройство"]
}

def extract_snippet(text, word):
    pattern = re.compile(r'([^.]*?\b' + re.escape(word) + r'\b[^.]*\.)', re.IGNORECASE)
    match = pattern.search(text)
    return match.group(1).strip() if match else ""

def analyze_file(filepath):
    results = []
    with open(filepath, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
        text = soup.get_text(separator=" ", strip=True).lower()

        for category, words in keywords.items():
            for word in words:
                if word in text:
                    snippet = extract_snippet(text, word)
                    results.append((os.path.basename(filepath), category, word, snippet))
                    break  # само първото съвпадение от категорията
    return results

def extract_all_cases():
    all_results = []

    for filename in os.listdir(bulletin_dir):
        if filename.endswith(".html"):
            path = os.path.join(bulletin_dir, filename)
            all_results.extend(analyze_file(path))

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["source_file", "crime_type", "matched_word", "context_snippet"])
        writer.writerows(all_results)

    print(f"[✔] Extracted {len(all_results)} crime cases into {output_file}")

if __name__ == "__main__":
    extract_all_cases()
