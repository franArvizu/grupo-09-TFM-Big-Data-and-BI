
# src/scrape_wikipedia_concepts.py
# %%
import time
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; OmarA5Bot/1.0)"}

# Semillas (puedes ampliar)
SEEDS = [
    ("Lean Manufacturing", "https://es.wikipedia.org/wiki/Lean_manufacturing"),
    ("Lean Manufacturing", "https://en.wikipedia.org/wiki/Lean_manufacturing"),
    ("Six Sigma",          "https://en.wikipedia.org/wiki/Six_Sigma"),
    ("SPC",                "https://en.wikipedia.org/wiki/Statistical_process_control"),
]

def clean_text(t: str) -> str:
    if not t:
        return ""
    # quita citas [1], [2]..., espacios y saltos
    t = re.sub(r"\[\d+\]", "", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t

def extract_concepts(url: str, standard: str) -> list[dict]:
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "lxml")

    # Lead (primeros párrafos)
    lead_paras = soup.select("div.mw-parser-output > p")
    concepts = []

    # Descripción general del estándar
    desc_chunks = []
    for p in lead_paras[:4]:
        txt = clean_text(p.get_text())
        if len(txt) > 60:
            desc_chunks.append(txt)
    if desc_chunks:
        concepts.append({
            "standard": standard,
            "concept": standard,
            "description": " ".join(desc_chunks),
            "source_url": url
        })

    # Buscar listas de conceptos/herramientas
    sections = soup.select("h2, h3")
    keywords = ["Tools", "Concepts", "Principles", "Herramientas", "Conceptos", "Principios"]
    for sec in sections:
        title = clean_text(sec.get_text())
        if any(k.lower() in title.lower() for k in keywords):
            ul = sec.find_next("ul")
            if ul:
                for li in ul.select("li"):
                    txt = clean_text(li.get_text())
                    if len(txt) > 3:
                        if ":" in txt:
                            name, desc = txt.split(":", 1)
                        else:
                            parts = txt.split(" ")
                            name = parts[0].strip()
                            desc = txt
                        concepts.append({
                            "standard": standard,
                            "concept": clean_text(name),
                            "description": clean_text(desc),
                            "source_url": url
                        })
    time.sleep(1)  # Pausa de cortesía
    return concepts

def main():
    rows = []
    for standard, url in SEEDS:
        try:
            rows.extend(extract_concepts(url, standard))
        except Exception as e:
            print(f"[WARN] {standard} - {url}: {e}")

    df = pd.DataFrame(rows).drop_duplicates(subset=["standard","concept","source_url"])
    df.insert(0, "concept_id", range(1, len(df) + 1))
    # Reordenamos columnas al esquema pedido
    df = df[["concept_id", "standard", "concept", "description", "source_url"]]
    df.to_csv("data/raw/wikipedia_concepts.csv", index=False, encoding="utf-8")
    print(f"OK: data/raw/wikipedia_concepts.csv ({len(df)} filas)")

if __name__ == "__main__":
    main()

