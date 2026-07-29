# Guía Docente Completa: Class 30 - Working with Files in Python

Clase online para 60-75 minutos.
Documento para profesor: incluye guion literal, comandos exactos y prompts completos. El profesor puede saltarse bloques sin perder continuidad.

## 1) Objetivo de la clase

Al finalizar, el estudiante podrá:

- Comprender qué es un archivo, cómo se representa en disco y por qué necesita una ruta.
- Abrir, leer, crear y escribir archivos de texto con `open()` y `with`.
- Manejar errores comunes al escribir archivos y aplicar buenas prácticas de codificación con `encoding="utf-8"`.
- Leer y procesar archivos CSV de forma práctica, incluyendo transformación a diccionarios.

## 2) Agenda sugerida (60-75 min)

Ruta base de 65 minutos:

- Apertura y contexto: 5 min
- Bloque A: Qué es un archivo y rutas: 12 min
- Bloque B: Abrir, leer y escribir: 15 min
- Bloque C: Errores al escribir y validación: 12 min
- Bloque D: CSV y procesamiento estructurado: 16 min
- Cierre + checklist + Q&A: 5 min

Si tienes 75 min:

- Añade 10 min de práctica guiada con un segundo archivo CSV o un mini ejercicio de escritura.

Si tienes 60 min:

- Recorta el bloque D a una demo más breve y deja la parte de diccionarios como ejemplo del profesor.

## 3) Preparación docente (antes de clase)

Checklist técnico:

- Python 3.10+ disponible.
- Terminal abierta con acceso a la carpeta del proyecto.
- `cat`, `python3` y `curl` disponibles.

Comandos de verificación previa:

```bash
python3 --version
python3 -m pip --version
```

Carpeta demo sugerida:

```bash
mkdir -p class_30/demo_files
cd class_30/demo_files
```

## 4) Guion docente detallado (con texto literal)

## Apertura (5 min)

Qué decir (literal):

"Hoy vamos a trabajar con una de las habilidades más útiles en backend: guardar y recuperar información de forma persistente."

"No se trata solo de leer texto; se trata de construir programas que recuerden datos entre ejecuciones."

## Bloque A - Qué es un archivo y cómo se ubica (12 min)

### A1. Concepto rápido (4 min)

Qué decir (literal):

"Un archivo es un contenedor de bytes con un nombre, una extensión y una ubicación. Python necesita saber dónde está para poder interactuar con él."

"La ruta puede ser absoluta o relativa. Una absoluta apunta siempre al mismo lugar; una relativa depende del directorio desde el que ejecutas el script."

### A2. Demo guiada (4 min)

Ejecuta:

```bash
pwd
mkdir -p demo_data
python3 - <<'PY'
from pathlib import Path
p = Path('demo_data/example.txt')
print('exists before:', p.exists())
print('absolute path:', p.resolve())
PY
```

Qué decir (literal):

"Cuando ejecutamos un script, Python resuelve rutas desde el directorio actual. Por eso conviene ser explícitos y, en muchos casos, usar `Path` para hacerlo más claro."

### A3. Mini práctica (4 min)

Prompt exacto sugerido:

```text
Actúa como profesor de Python. Explícame con un ejemplo sencillo la diferencia entre una ruta absoluta y una ruta relativa, y cómo se vería en un proyecto real con una carpeta data y un archivo users.txt.
```

## Bloque B - Abrir, leer y escribir archivos (15 min)

### B1. Concepto y riesgos (5 min)

Qué decir (literal):

"La forma más segura y recomendada de trabajar con archivos es usando `with open(...) as f:`. Así, Python se encarga de cerrar el archivo aunque ocurra un error."

"Para leer texto, usamos `"r"`; para crear o sobrescribir, `"w"`; para añadir, `"a"`."

### B2. Ejemplo práctico (7 min)

Ejecuta:

```bash
python3 - <<'PY'
from pathlib import Path

path = Path('demo_data/notes.txt')
path.parent.mkdir(parents=True, exist_ok=True)

with open(path, 'w', encoding='utf-8') as f:
    f.write('Hola desde Python\n')
    f.write('Segundo renglón\n')

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()
    print(content)
PY
```

Qué decir (literal):

"Fíjense que el archivo se crea con `w` y luego se lee con `r`. El `encoding="utf-8"` evita problemas con acentos y caracteres especiales."

### B3. Validación (3 min)

Checklist:

- El archivo existe en la carpeta `demo_data`.
- El contenido se imprime correctamente.
- Se usa `encoding="utf-8"` al abrir el archivo.

## Bloque C - Errores al escribir y buenas prácticas (12 min)

Ejecuta:

```bash
python3 - <<'PY'
from pathlib import Path

path = Path('demo_data/unsafe.txt')
path.parent.mkdir(parents=True, exist_ok=True)

try:
    with open(path, 'w', encoding='utf-8') as f:
        f.write('Texto nuevo\n')
except Exception as e:
    print('Error:', e)
else:
    print('Archivo escrito correctamente')
PY
```

Prompt exacto sugerido:

```text
Quiero un ejemplo en Python que cree un archivo llamado report.txt, lo abra en modo escritura, agregue una línea y luego lo lea de vuelta. Usa with open y encoding utf-8.
```

Qué decir (literal):

"Los errores de escritura suelen estar relacionados con rutas inválidas, permisos o codificaciones. El patrón `try/except` ayuda a identificar el problema de forma clara."

## Bloque D - CSV y transformación a diccionarios (16 min)

Ejecuta:

```bash
python3 - <<'PY'
import csv
from pathlib import Path

path = Path('demo_data/users.csv')
path.parent.mkdir(parents=True, exist_ok=True)

with open(path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['name', 'email'])
    writer.writerow(['Ana', 'ana@example.com'])
    writer.writerow(['Luis', 'luis@example.com'])

with open(path, 'r', encoding='utf-8', newline='') as f:
    rows = list(csv.DictReader(f))
    print(rows)
PY
```

Prompt exacto sugerido:

```text
Actúa como senior Python teacher. Muéstrame cómo leer un archivo CSV en Python usando csv.DictReader y convertir cada fila en un diccionario con claves y valores claros.
```

Qué decir (literal):

"El CSV es una forma muy común de guardar datos tabulares. Con `csv.DictReader` podemos trabajar con cada fila como un diccionario, lo que resulta mucho más legible que manipular listas de strings."

## Bloque E (opcional, 8 min) - Enviar archivos a una API y procesarlos

Objetivo rápido:

- Mostrar cómo un cliente envía un archivo con `multipart/form-data`.
- Guardar temporalmente el archivo en backend y devolver metadatos útiles.

Ejecuta:

```bash
mkdir -p api_upload_demo && cd api_upload_demo
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi "uvicorn[standard]" python-multipart

cat > main.py << 'PY'
from pathlib import Path
from fastapi import FastAPI, UploadFile, File

app = FastAPI(title="Upload API Demo")
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
        target = UPLOAD_DIR / file.filename
        content = await file.read()
        target.write_bytes(content)

        return {
                "filename": file.filename,
                "content_type": file.content_type,
                "size_bytes": len(content),
                "saved_to": str(target),
        }
PY

uvicorn main:app --reload --port 8002
```

En otra terminal, prueba el envío:

```bash
cd class_30/demo_files
echo "archivo de prueba" > sample.txt
curl -s -X POST http://127.0.0.1:8002/upload \
    -F "file=@sample.txt"
```

Qué decir (literal):

"Aquí el cliente manda el archivo como `multipart/form-data`, no como JSON. En FastAPI, `UploadFile` nos da nombre, tipo de contenido y el stream de bytes."

"Este patrón se usa para adjuntos, importación de CSV y carga de imágenes. Después de guardar el archivo, lo normal es validar tipo/tamaño y procesarlo en un job asíncrono si pesa mucho."

## 5) Cierre (5 min)

Qué decir (literal):

"Lo importante hoy no es solo saber abrir un archivo, sino entender que los archivos permiten que un programa conserve información entre ejecuciones."

"En backend, esto es clave para logs, reportes, almacenamiento de usuarios y procesamiento de datos."

Checklist final en vivo:

```bash
ls demo_data
python3 - <<'PY'
from pathlib import Path
print(Path('demo_data/notes.txt').exists())
print(Path('demo_data/users.csv').exists())
PY
```

## 6) Preguntas de chequeo rápidas

- ¿Cuál es la diferencia entre una ruta absoluta y una ruta relativa?
- ¿Por qué conviene usar `with open(...)`?
- ¿Qué significa `encoding="utf-8"`?
- ¿Qué ventaja tiene usar `csv.DictReader` frente a leer el CSV como texto plano?

## 7) Plan de contingencia

Si falla la demo principal:

```bash
python3 - <<'PY'
from pathlib import Path
Path('demo_data').mkdir(exist_ok=True)
Path('demo_data/notes.txt').write_text('fallback demo\n', encoding='utf-8')
print(Path('demo_data/notes.txt').read_text(encoding='utf-8'))
PY
```

Si falla la parte de CSV:

- Mostrar un ejemplo de archivo CSV en texto simple.
- Explicar la estructura de filas y columnas antes de introducir la librería `csv`.
- Usar un ejemplo muy simple con solo 2 columnas.
