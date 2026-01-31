# ---------------------------------------------
# Script: 01_data_cleaning.R
# Descripción: Limpieza e integración de datasets conceptuales Lean / ISO
# ---------------------------------------------

# Librerías esenciales
library(tidyverse)
library(stringr)
library(janitor)

# ---------------------------------------------
# 1. Normalización de datasets base
# ---------------------------------------------

dataset_conceptual_limpia <- dataset_conceptual_iso_lean_raw %>%
  clean_names() %>%
  rename(text = description)

# ---------------------------------------------
# 2. Limpieza del scraping (idiomas no objetivo)
# ---------------------------------------------

dataset_conceptual_scrapping_limpia <- dataset_conceptual_scrapping_diccionario %>%
  clean_names() %>%
  filter(!grepl("www.zhihu.com", url, fixed = TRUE))

# ---------------------------------------------
# 3. Unificación de datasets (repositorio central)
# ---------------------------------------------

df_iso <- dataset_conceptual_iso_lean_raw %>%
  clean_names() %>%
  rename(text = description) %>%
  select(text)

df_scrapping <- dataset_conceptual_scrapping_limpia %>%
  select(text)

df_fuentes <- dataset_definiciones_lean_diversas_fuentes %>%
  clean_names() %>%
  select(text)

dataset_total <- bind_rows(df_iso, df_scrapping, df_fuentes) %>%
  filter(!is.na(text))

# ---------------------------------------------
# 4. Clasificación educativa y dificultad
# ---------------------------------------------

dataset_final_limpio <- dataset_total %>%
  mutate(
    stage = case_when(
      str_detect(text, "(?i)filosofía|origen japonés|desperdicio|muda") ~ "1. Fundamentos",
      str_detect(text, "(?i)5S|estandarización|normativa|iso 9001") ~ "2. Operativo",
      str_detect(text, "(?i)Kanban|Pull|Kaizen|estadística|poka-yoke") ~ "3. Especialista",
      str_detect(text, "(?i)estrategia|cultura|cadena de suministro|supply chain") ~ "4. Estratégico",
      TRUE ~ "Introductorio / Otros"
    ),
    nivel_dificultad = case_when(
      stage == "1. Fundamentos" ~ 1,
      stage == "2. Operativo" ~ 2,
      stage == "3. Especialista" ~ 3,
      stage == "4. Estratégico" ~ 4,
      TRUE ~ 0
    ),
    text_length = nchar(text)
  ) %>%
  filter(nivel_dificultad > 0)

# ---------------------------------------------
# 5. Guardar dataset limpio final
# ---------------------------------------------

write_csv(dataset_final_limpio, "data/processed/dataset_final_limpio.csv")