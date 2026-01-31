import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# -------- CONFIGURACIÓN --------
INPUT_URLS = "./urls_duckduckgo_raw.csv"
OUTPUT_DATASET = "./dataset_conceptual_scrapping_diccionario.csv"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (AcademicScraper/1.0)"
}

MIN_TEXT_LENGTH = 120   # filtro de calidad
TIME_DELAY = 2          # pausa ética entre requests
# --------------------------------

# Cargar URLs
df_urls = pd.read_csv(INPUT_URLS)
urls = df_urls["url"].dropna().unique()

data = []

print(f"URLs a procesar: {len(urls)}\n")

for i, url in enumerate(urls, start=1):
    print(f"[{i}/{len(urls)}] Scraping: {url}")

    try:
        response = requests.get(url, headers=HEADERS, timeout=15)

        if response.status_code != 200:
            print("  ⚠️ No accesible")
            continue

        soup = BeautifulSoup(response.text, "lxml")

        # Extraer encabezados (definiciones clave)
        for header in soup.find_all(["h1", "h2", "h3"]):
            text = header.get_text(strip=True)
            if len(text) >= MIN_TEXT_LENGTH:
                data.append({
                    "url": url,
                    "content_type": "header",
                    "text": text
                })

        # Extraer párrafos (explicaciones)
        for p in soup.find_all("p"):
            text = p.get_text(strip=True)
            if len(text) >= MIN_TEXT_LENGTH:
                data.append({
                    "url": url,
                    "content_type": "paragraph",
                    "text": text
                })

        time.sleep(TIME_DELAY)

    except Exception as e:
        print(f"  ❌ Error: {e}")

# Crear DataFrame
df_data = pd.DataFrame(data)
df_data.drop_duplicates(subset=["url", "text"], inplace=True)

# Guardar dataset
df_data.to_csv(OUTPUT_DATASET, index=False, encoding="utf-8")

print("\nScraping finalizado")
print(f"Registros obtenidos: {len(df_data)}")
print(f"Archivo generado: {OUTPUT_DATASET}")