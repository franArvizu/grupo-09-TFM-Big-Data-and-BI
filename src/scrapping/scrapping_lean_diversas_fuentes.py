import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Lista de páginas a scrapear
URLS = [
    ("InstitutoLean", "https://www.institutolean.org/que-es-lean"),
    ("APD", "https://www.apd.es/metodologia-lean-que-es/"),
    ("Atlassian", "https://www.atlassian.com/es/agile/project-management/lean-methodology"),
    ("LeanOrgExplorar", "https://www.lean.org/explore-lean/what-is-lean/"),
    ("BBVA", "https://www.bbva.com/es/innovacion/que-es-el-metodo-lean-startup-y-por-que-es-efectivo/"),
    ("Mecalux", "https://www.mecalux.com.mx/blog/metodologia-lean"),
    ("KaizenInsights", "https://kaizen.com/es/insights-es/comprender-lean-manufacturing-guia/"),
    ("ENAEBlog", "https://www.enae.es/blog/metodologia-lean"),
    ("Ideatec", "https://www.ideatec.es/blog/desarrollo-sostenible-es/metodo-lean/"),
    ("IEP", "https://iep.edu.es/filosofia-lean/")
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; AcademicScraper/1.0)"
}

data = []

for source, url in URLS:
    print(f"Scraping: {source} | {url}")
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(response.text, "lxml")

        # Extraer texto de párrafos
        for p in soup.find_all("p"):
            text = p.get_text(strip=True)
            if len(text) > 80:  # filtro de texto mínimo útil
                data.append({
                    "source": source,
                    "url": url,
                    "text": text
                })

        # Extraer encabezados que contienen definiciones
        for header in soup.find_all(["h1", "h2", "h3"]):
            text = header.get_text(strip=True)
            if len(text) > 40:
                data.append({
                    "source": source,
                    "url": url,
                    "text": text
                })

        time.sleep(1)  # pausa ética
    except Exception as e:
        print(f"Error al scrapear {url}: {e}")

# Crear DataSet y guardar CSV
df = pd.DataFrame(data)
df.drop_duplicates(inplace=True)

output_path = "./conceptos_lean_diversas_fuentes.csv"
df.to_csv(output_path, index=False, encoding="utf-8")

print(f"\nRegistros obtenidos: {len(df)}")
print(f"CSV generado en: {output_path}")
