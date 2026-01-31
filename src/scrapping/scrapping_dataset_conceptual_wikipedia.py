import requests
from bs4 import BeautifulSoup
import pandas as pd

# Páginas a scrapear
SOURCES = {
    "Lean Manufacturing": "https://es.wikipedia.org/wiki/Lean_manufacturing",
    "Statistical Process Control": "https://es.wikipedia.org/wiki/Control_estad%C3%ADstico_de_procesos",
    "Six Sigma": "https://es.wikipedia.org/wiki/Seis_Sigma",
    "ISO 9001": "https://es.wikipedia.org/wiki/ISO_9001"
}

rows = []
concept_id = 1

for standard, url in SOURCES.items():
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "lxml")

    paragraphs = soup.select("p")

    for p in paragraphs:
        text = p.get_text(strip=True)

        # Filtro para evitar párrafos vacíos o irrelevantes
        if len(text) > 120 and not text.lower().startswith("this article"):
            rows.append({
                "concept_id": concept_id,
                "standard": standard,
                "concept": standard,
                "description": text,
                "source_url": url
            })
            concept_id += 1

df = pd.DataFrame(rows)

print(f"Registros encontrados: {len(df)}")

df.to_csv("./dataset1_conceptual_iso_lean_raw.csv", index=False)