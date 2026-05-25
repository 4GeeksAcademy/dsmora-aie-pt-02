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

Para ejecutar el scraper, asegúrate de configurar la URL del tutorial deseado dentro del archivo `scraper.py` y luego ejecuta:

```bash
python3 scraper.py
```

El script generará un archivo `.json` con el contenido extraído de forma incremental para evitar pérdida de datos.

## Características

- **Gestión de Modales:** Inyecta JavaScript para eliminar pop-ups que bloquean la interacción.
- **Navegación Automática:** Abre el menú lateral, identifica las lecciones y hace clic en cada una.
- **Saltos de Bloqueo:** Detecta y hace clic en botones como "Continue anyway" para acceder al contenido protegido.
- **Extracción de Texto:** Limpia el DOM para extraer únicamente el texto relevante de las lecciones.
