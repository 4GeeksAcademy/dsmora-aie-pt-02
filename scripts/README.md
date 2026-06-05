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

El script no usa valores por defecto. Siempre debes indicar objetivos con este formato:

`class_x:url1,url2`

Ejemplo para una clase con dos enlaces:

```bash
python3 scraper.py --target "class_13:https://url1.com,https://url2.com"
```

Ejemplo con multiples clases:

```bash
python3 scraper.py \
  --target "class_13:https://url1.com,https://url2.com" \
  --target "class_14:https://url3.com"
```

Reglas:

- `class_x` debe cumplir `class_N` (por ejemplo: `class_13`).
- Puedes pasar varias URLs separadas por coma para la misma clase.
- Puedes repetir `--target` para varias clases.

## Salidas

Los JSON se escriben en la carpeta de clase indicada en cada `--target`.
El nombre de archivo se deriva automaticamente del subdominio de la URL.

## Características

- **Gestión de Modales:** Inyecta JavaScript para eliminar pop-ups que bloquean la interacción.
- **Navegación Automática:** Abre el menú lateral, identifica las lecciones y hace clic en cada una.
- **Saltos de Bloqueo:** Detecta y hace clic en botones como "Continue anyway" para acceder al contenido protegido.
- **Extracción de Texto:** Limpia el DOM para extraer únicamente el texto relevante de las lecciones.
- **Entrada Explícita:** Obliga a definir clase y URLs en cada ejecución con `--target`.
