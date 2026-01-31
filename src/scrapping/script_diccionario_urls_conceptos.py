from ddgs import DDGS
import pandas as pd
import time

SEARCH_TERMS = [
    "Lean Manufacturing definicion",
    "Lean Manufacturing conceptos",
    "ISO 9001 definicion",
    "ISO 9001 conceptos",
    "Statistical Process Control SPC",
    "SPC definicion",
    "SPC conceptos",
    "Six Sigma definicion",
    "Six Sigma conceptos",
]

results = []

with DDGS() as ddgs:
    for term in SEARCH_TERMS:
        print(f"Buscando: {term}")

        search_results = ddgs.text(
            term,
            max_results=15,
            safesearch="moderate"
        )

        for r in search_results:
            results.append({
                "search_term": term,
                "title": r.get("title"),
                "url": r.get("href"),
                "snippet": r.get("body")
            })

        time.sleep(1)

df = pd.DataFrame(results)
df.dropna(subset=["url"], inplace=True)
df.drop_duplicates(subset=["url"], inplace=True)

output_path = "./urls_duckduckgo_raw.csv"
df.to_csv(output_path, index=False, encoding="utf-8")

print(f"\nURLs obtenidas: {len(df)}")
print(f"Archivo generado: {output_path}")