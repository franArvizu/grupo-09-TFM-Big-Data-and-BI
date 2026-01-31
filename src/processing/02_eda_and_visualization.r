# ---------------------------------------------
# Script: 02_eda_and_visualization.R
# Descripción: Análisis Exploratorio y Visualización
# ---------------------------------------------

# Librerías
library(tidyverse)

# ---------------------------------------------
# 1. Cargar dataset limpio
# ---------------------------------------------

dataset_final_limpio <- read_csv("data/processed/dataset_final_limpio.csv")

# ---------------------------------------------
# 2. Distribución por Etapa Educativa
# ---------------------------------------------

ggplot(dataset_final_limpio, aes(x = stage, fill = stage)) +
  geom_bar(show.legend = FALSE) +
  geom_text(stat = "count", aes(label = after_stat(count)),
            vjust = -0.5, fontface = "bold") +
  theme_minimal() +
  labs(
    title = "Disponibilidad de Material por Etapa Educativa",
    x = "Etapa Educativa",
    y = "Cantidad de Conceptos"
  )

# ---------------------------------------------
# 3. Mapa de Dificultad
# ---------------------------------------------

ggplot(dataset_final_limpio,
       aes(x = reorder(stage, nivel_dificultad),
           fill = nivel_dificultad)) +
  geom_bar(width = 0.7) +
  scale_fill_gradient(low = "#56B4E9", high = "#D55E00") +
  theme_minimal() +
  labs(
    title = "Mapa de Ruta: Niveles de Dificultad",
    x = "Etapa del Programa",
    y = "Cantidad de Contenido"
  )

# ---------------------------------------------
# 4. Segmentación de Marketing
# ---------------------------------------------

dataset_marketing <- dataset_final_limpio %>%
  mutate(marketing_tier = case_when(
    str_detect(text, "(?i)black belt|gerente|director|mba|estratégico") ~ "PRÉMIUM",
    str_detect(text, "(?i)green belt|especialista|auditor|analista") ~ "AVANZADO",
    str_detect(text, "(?i)white belt|yellow belt|5s|fundamentos|muda") ~ "BÁSICO",
    TRUE ~ NA_character_
  )) %>%
  filter(!is.na(marketing_tier)) %>%
  mutate(marketing_tier = factor(
    marketing_tier,
    levels = c("BÁSICO", "AVANZADO", "PRÉMIUM")
  ))

ggplot(dataset_marketing, aes(x = marketing_tier, fill = marketing_tier)) +
  geom_bar(width = 0.6) +
  geom_text(stat = "count", aes(label = after_stat(count)),
            vjust = -0.5, fontface = "bold") +
  theme_minimal() +
  labs(
    title = "Estructura del Portafolio: Plan de Mercadeo",
    x = "Nivel de Certificación",
    y = "Cantidad de Contenido"
  )