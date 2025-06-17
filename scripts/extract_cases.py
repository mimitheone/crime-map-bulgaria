import os
import re
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

input_dir = "data/bulletins"
output_file = "data/cases.csv"

case_list = []

# Ключови думи, по които ще търсим
keywords = ["убийство", "убит", "умъртвяване", "прострелян", "намушкан", "труп", "смърт"]

# Минаваме през всички HTML файлове
for filename in os.listdir(input_dir):
    if filename.endswith(".html"):
        filepath = os.path.join(input_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
            text = soup.get_text(separator=" ").lower()

            for keyword in keywords:
                if keyword in text:
                    # Извличаме дата от името на файла
                    date_str = filename.split("_")[-1].replace(".html", "")
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d")

                    case = {
                        "date": date_obj.strftime("%Y-%m-%d"),
                        "region": filename.split("_")[0],
                        "summary": f"Case related to '{keyword}' found in {filename}",
                        "keyword": keyword
                    }
                    case_list.append(case)
                    break  # Не добавяме няколко пъти едно и също

# Записваме в CSV
df = pd.DataFrame(case_list)
df.to_csv(output_file, index=False)
print(f"[✔] Extracted {len(df)} cases to {output_file}")
