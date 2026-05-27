# Scripts de Scraping para LearnPack

Este directorio contiene las herramientas utilizadas para extraer el contenido de los tutoriales de la plataforma LearnPack (4Geeks Academy).

## Contenido

- `scraper.py`: Script principal basado en Playwright para navegar por los tutoriales, saltar modales de bloqueo y extraer el texto de las lecciones de forma automatizada.

## Requisitos

Es necesario tener instalado Python 3 y las siguientes dependencias:

```bash
pip install playwright
playwright install chromium
```

## Uso

El script actual ya incluye dos tutoriales configurados y los procesa en una sola ejecución:

- Introduction to Programming (Mastering the Art of K)
- Programming Fundamentals

Para ejecutar el scraper:

```bash
python3 scraper.py
```

Los resultados se guardan de forma incremental en `../class_06/` para evitar pérdida de datos:

- `../class_06/introduction_to_programming.json`
- `../class_06/programming_fundamentals.json`

## Características

- **Gestión de Modales:** Inyecta JavaScript para eliminar pop-ups que bloquean la interacción.
- **Navegación Automática:** Abre el menú lateral, identifica las lecciones y hace clic en cada una.
- **Saltos de Bloqueo:** Detecta y hace clic en botones como "Continue anyway" para acceder al contenido protegido.
- **Extracción de Texto:** Limpia el DOM para extraer únicamente el texto relevante de las lecciones.
