# Guia Docente Completa: Class 28 - Arquitectura Backend, Organizacion Python, FastAPI y Entornos Virtuales

Clase online para 60-75 minutos.
Documento para profesor: incluye guion literal, comandos exactos y prompts completos para demo con IA.

## 1) Objetivo de la clase

Al finalizar, el estudiante podra:

- Explicar por que la arquitectura backend importa y comparar MVC, arquitectura en capas y enfoque hexagonal a nivel introductorio.
- Detectar problemas de separacion de responsabilidades en proyectos Python (estilo, modulos, imports, responsabilidades por archivo).
- Levantar una API minima con FastAPI y entender endpoints, parametros y validacion con Pydantic.
- Crear y gestionar un entorno virtual reproducible para equipo usando `uv`.
- Relacionar decisiones de arquitectura con mantenibilidad, escalabilidad y colaboracion real.

## 2) Agenda sugerida (60-75 min)

Ruta base de 70 minutos:

- Apertura y objetivos: 5 min
- Bloque A - Arquitecturas backend (MVC, capas, hexagonal, serverless): 16 min
- Bloque B - Separacion de responsabilidades en Python: 12 min
- Bloque C - FastAPI desde cero (app, endpoints, params, Pydantic): 18 min
- Bloque D - Entornos virtuales y flujo profesional con `uv`: 12 min
- Cierre + chequeo + Q&A: 7 min

Si tienes 75 min:

- Anade 5 min con mini-ejercicio de analisis: "dado un endpoint mezclado con SQL, como lo separarias en capas?"

Si tienes 60 min:

- Recorta 5 min del Bloque A (deja MVC + capas, menciona hexagonal/serverless sin demo).
- Recorta 5 min del Bloque D (deja solo `uv init`, `uv add`, `uv sync`).

## 3) Preparacion docente (antes de clase)

Checklist tecnico:

- Tener Python 3.11+ disponible.
- Tener `uv` instalado o listo para instalar.
- Abrir una carpeta limpia para demos en vivo.
- Confirmar que terminal y editor comparten la misma carpeta de trabajo.

Comandos de verificacion previa:

```bash
python3 --version
uv --version
mkdir -p class_28/live && cd class_28/live
python3 -c "print('Entorno listo para class 28')"
```

Si `uv` no existe:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source "$HOME/.cargo/env"
uv --version
```

## 4) Guion docente detallado (con texto literal)

## Apertura (5 min)

Que decir (literal):

"Hoy vamos a conectar cuatro piezas que en el mundo real van juntas: arquitectura backend, organizacion del codigo Python, FastAPI y gestion profesional del entorno."

"La meta no es memorizar terminos; la meta es poder tomar decisiones tecnicas con criterio cuando construyan una API en equipo."

Puente con clases previas:

- Venimos de fundamentos de Python; ahora subimos a decisiones de estructura y despliegue de trabajo colaborativo.

## Bloque A - Arquitecturas backend (16 min)

### A1. Por que arquitectura importa (4 min)

Que decir (literal):

"Dos apps pueden tener las mismas funcionalidades y resultados, pero una puede ser mantenible y la otra un caos. La diferencia suele ser arquitectura."

"Arquitectura es como el plano del edificio: no es decoracion, define estabilidad y costo de cambios futuros."

### A2. MVC, capas y hexagonal en 1 mapa mental (8 min)

Dibujo rapido en pizarra o editor:

- MVC: Controlador recibe peticion, Modelo procesa datos, Vista responde.
- Capas: Presentacion -> Logica de negocio -> Acceso a datos.
- Hexagonal: Core de negocio al centro; puertos y adaptadores afuera.

Que decir (literal):

"Si mezclas acceso a datos en rutas HTTP, cada cambio de base de datos duele en toda la aplicacion."

"Con capas o puertos/adaptadores, la tecnologia externa se vuelve reemplazable y la logica de negocio queda protegida."

### A3. Serverless y trade-offs (4 min)

Que decir (literal):

"Serverless no significa sin servidores; significa que no los gestionas directamente."

"El beneficio es velocidad y elasticidad; el costo puede ser complejidad operativa, cold starts y dependencia del proveedor."

## Bloque B - Separacion de responsabilidades en Python (12 min)

### B1. Problema comun: todo en un solo archivo (4 min)

Que decir (literal):

"Cuando todo vive en un unico archivo, no hay limites claros: crece la friccion para leer, testear y cambiar."

"Separar por responsabilidad reduce acoplamiento y aumenta claridad de equipo."

### B2. Demo corta: estructura por modulos + imports limpios (8 min)

Ejecuta:

```bash
mkdir -p backend_demo/app
cd backend_demo
cat > app/__init__.py <<'PY'
# paquete principal
PY

cat > app/services.py <<'PY'
def calculate_total(price: float, quantity: int) -> float:
    return price * quantity
PY

cat > app/routes.py <<'PY'
from app.services import calculate_total


def checkout_route(price: float, quantity: int) -> dict:
    total = calculate_total(price, quantity)
    return {"total": total}
PY

cat > main.py <<'PY'
from app.routes import checkout_route


print(checkout_route(9.99, 3))
PY

python3 main.py
```

Puntos de refuerzo:

- Nombres consistentes (`snake_case`, claridad semantica).
- Imports explicitos; evitar `from module import *`.
- Cada archivo con una responsabilidad principal.

## Bloque C - FastAPI desde cero (18 min)

### C1. Crear proyecto y dependencias (5 min)

Ejecuta:

```bash
cd ..
uv init fastapi_live
cd fastapi_live
uv add fastapi uvicorn
```

Que decir (literal):

"FastAPI nos da enrutamiento, validacion y documentacion automatica. Nosotros nos enfocamos en logica de negocio."

### C2. App minima + endpoint GET (4 min)

Ejecuta:

```bash
cat > main.py <<'PY'
from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "ok"}
PY

uv run uvicorn main:app --reload
```

Con servidor corriendo, probar en otra terminal:

```bash
curl http://127.0.0.1:8000/health
```

### C3. Parametros de ruta y query (4 min)

Editar `main.py` con:

```python
@app.get("/users/{user_id}")
def get_user(user_id: int, active: bool = True):
    return {"user_id": user_id, "active": active}
```

Probar:

```bash
curl "http://127.0.0.1:8000/users/7?active=false"
```

### C4. Modelo Pydantic para POST (5 min)

Agregar a `main.py`:

```python
from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str
    age: int


@app.post("/users")
def create_user(payload: UserCreate):
    return {"message": "user created", "user": payload.model_dump()}
```

Probar:

```bash
curl -X POST "http://127.0.0.1:8000/users" \
  -H "Content-Type: application/json" \
  -d '{"name":"Ana","email":"ana@example.com","age":24}'
```

Que decir (literal):

"Pydantic convierte tipos y valida estructura automaticamente. Si el dato entra mal, FastAPI responde error de validacion sin escribir codigo extra."

## Bloque D - Entornos virtuales y flujo profesional con uv (12 min)

### D1. Flujo minimo reproducible de equipo (7 min)

Que decir (literal):

"En equipo no alcanza con que funcione en tu laptop; tiene que funcionar igual en todas las maquinas."

Ejecuta:

```bash
cd ..
uv init env_workflow_demo
cd env_workflow_demo
uv add requests
uv add "fastapi>=0.110"
ls -la
```

Explicar:

- `pyproject.toml`: dependencias declaradas.
- `uv.lock`: versiones exactas resueltas.
- `.venv/`: entorno local (no versionar).

### D2. Regla de oro para git y onboarding (5 min)

Ejecuta:

```bash
cat > .gitignore <<'TXT'
.venv/
__pycache__/
TXT

uv sync
```

Que decir (literal):

"En git subimos `pyproject.toml` y `uv.lock`; nunca `.venv/`."

"Con `uv sync`, cualquier companero recrea el entorno exacto en minutos."

## 5) Prompts exactos para demo con OpenClaw

Usa estos prompts tal cual, en bloques separados.

Prompt 1 - Arquitectura (analisis):

```text
Actua como arquitecto backend senior y explica en espanol, de forma didactica y breve, cuando conviene usar MVC, arquitectura en capas y arquitectura hexagonal en una API Python. Incluye 1 ejemplo concreto por patron y 2 trade-offs reales por cada uno.
```

Prompt 2 - Refactor de responsabilidades:

```text
Tengo un archivo FastAPI donde las rutas hacen consultas SQL directas y validan negocio inline. Propon una refactorizacion paso a paso para separar en capas (routes, services, repositories), con estructura de carpetas y responsabilidades por archivo.
```

Prompt 3 - FastAPI + Pydantic:

```text
Genera un ejemplo minimo de FastAPI con endpoints GET /health, GET /users/{user_id} y POST /users usando Pydantic. El codigo debe estar en un solo archivo main.py y debe incluir tipos correctos.
```

Prompt 4 - uv workflow para equipos:

```text
Explica un flujo profesional con uv para proyectos Python colaborativos: init, add, lock, sync, que archivos versionar, que ignorar y errores comunes que evitan conflictos de dependencias.
```

## 6) Errores comunes a provocar y corregir en vivo

- Error 1: mezclar logica de negocio en la ruta.
  - Correccion: mover calculo a `services.py`.
- Error 2: usar nombres ambiguos (`x`, `temp`, `data2`) en codigo de negocio.
  - Correccion: nombres expresivos y consistentes.
- Error 3: no usar entorno virtual y romper dependencias globales.
  - Correccion: `uv init` + `uv add` + `uv sync`.
- Error 4: enviar payload invalido a Pydantic.
  - Correccion: revisar tipos y schema esperado.

## 7) Plan de contingencia (si algo falla)

- Si `uv` falla por instalacion/red:
  - Alternativa rapida:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn
```

- Si el puerto 8000 esta ocupado:

```bash
uv run uvicorn main:app --reload --port 8001
```

- Si no puedes abrir Swagger UI:
  - Validar endpoints con `curl` para no frenar la clase.

## 8) Cierre (7 min)

Que decir (literal):

"Hoy unimos arquitectura y ejecucion real: no solo discutimos patrones, tambien levantamos API y flujo de entorno reproducible."

"Si una API crece, sobrevivira no por suerte, sino por decisiones de separacion y disciplina en el entorno."

Preguntas de chequeo final:

- "Que problema evita separar rutas, servicios y repositorios?"
- "Por que `uv.lock` es clave para trabajo en equipo?"
- "Cuando preferirias un enfoque en capas frente a uno hexagonal?"
- "Que te aporta Pydantic que antes hacias a mano?"

Tarea sugerida (post-clase):

- Crear una mini API de productos con `GET /products`, `GET /products/{id}` y `POST /products`.
- Aplicar separacion por capas minima.
- Gestionar dependencias con `uv` y compartir repo con `pyproject.toml` + `uv.lock`.

## 9) Checklist rapido de exito docente

Marca si se logro en clase:

- Se explicaron y compararon MVC, capas y hexagonal con al menos 1 caso cada una.
- Se mostro separacion de responsabilidades en Python con modulos.
- Se ejecuto FastAPI con al menos 2 endpoints probados.
- Se ejecuto validacion con Pydantic en un POST.
- Se demostro flujo `uv` con archivos de reproducibilidad.
- Hubo cierre con preguntas de comprobacion.# Guia Docente Completa: Class 28 - Arquitectura Backend + FastAPI + Entornos Virtuales

Clase online para 60-75 minutos.
Documento para profesor: incluye guion literal, comandos exactos y prompts completos para demo con IA.

## 1) Objetivo de la clase

Al finalizar, el estudiante podra:

- Explicar por que la arquitectura backend importa y comparar MVC, capas y enfoque hexagonal a nivel inicial.
- Identificar separacion de responsabilidades y anti-patrones comunes en proyectos Python.
- Levantar una API minima con FastAPI usando endpoints, parametros y un modelo Pydantic.
- Crear un entorno virtual reproducible para trabajo individual y en equipo.
- Conectar decisiones de arquitectura con decisiones practicas de implementacion.

## 2) Agenda sugerida (60-75 min)

Ruta base de 70 minutos:

- Apertura y objetivos: 5 min
- Bloque A - Arquitecturas backend (MVC, capas, hexagonal, serverless): 14 min
- Bloque B - Separacion de responsabilidades en Python: 12 min
- Bloque C - Entornos virtuales y flujo uv: 12 min
- Bloque D - FastAPI minimo funcional (endpoints + validacion): 18 min
- Bloque E - Cierre, chequeo de comprension y Q&A: 9 min

Si tienes 75 min:

- Anade 5 min de practica guiada para refactorizar una ruta mezclada (controller + DB) hacia una version con responsabilidades separadas.

Si tienes 60 min:

- Recorta 5 min del Bloque A (deja solo MVC vs capas y una mencion rapida de hexagonal/serverless).
- Recorta 5 min del Bloque E (deja solo 3 preguntas de chequeo y siguiente paso).

## 3) Preparacion docente (antes de clase)

Checklist tecnico:

- Tener Python 3.11+ disponible en terminal.
- Tener `uv` instalado para demo de entorno moderno (si no, usar `venv` como plan B).
- Tener `curl` disponible para probar endpoints.

Comandos de verificacion previa:

```bash
python3 --version
uv --version || echo "uv no instalado, usaremos venv"
mkdir -p class_28/live && cd class_28/live
python3 -c "print('Entorno listo para class 28')"
```

## 4) Guion docente detallado (con texto literal)

## Apertura (5 min)

Que decir (literal):

"Hoy vamos a unir cuatro piezas que normalmente se ensenan separadas: arquitectura, organizacion del codigo, entorno de trabajo y API real." 

"La meta es que salgan con una forma profesional de empezar backend en Python: pensar estructura, crear entorno limpio y exponer endpoints con validacion." 

## Bloque A - Arquitecturas backend (14 min)

### A1. Por que la arquitectura importa (4 min)

Que decir (literal):

"La arquitectura no es decoracion. Es lo que evita que cada cambio rompa tres cosas distintas." 

"Si el codigo crece sin limites claros, el costo de mantenimiento se dispara." 

### A2. Comparacion rapida: MVC, capas, hexagonal y serverless (7 min)

Pizarra verbal sugerida:

- MVC: separa Modelo, Vista, Controlador.
- Capas: presentacion, negocio, datos.
- Hexagonal: puertos y adaptadores para aislar core de dependencias externas.
- Serverless: ejecucion por eventos sin gestionar servidores.

Que decir (literal):

"No hay arquitectura perfecta. Elegimos segun contexto, equipo y tipo de producto." 

"Para proyectos iniciales, MVC o capas suele dar claridad rapida; hexagonal es util cuando quieres fuerte desacople." 

### A3. Mini caso de decision (3 min)

Pregunta al grupo:

- "Si quiero cambiar de PostgreSQL a Mongo sin tocar reglas de negocio, que enfoque me ayuda mas y por que?"

Respuesta esperada:

- Capas bien hechas o hexagonal con adaptadores.

## Bloque B - Separacion de responsabilidades en Python (12 min)

### B1. Detectar anti-patron comun (6 min)

Ejecuta:

```bash
cat > anti_patron.py <<'PY'
def create_user_route(payload):
    # Mezcla validacion, negocio y persistencia en un mismo lugar
    if 'email' not in payload:
        return {"error": "email requerido"}, 400
    if '@' not in payload['email']:
        return {"error": "email invalido"}, 400

    # Simulacion de acceso a BD directo desde "ruta"
    fake_db = []
    fake_db.append(payload)
    return {"ok": True, "users": fake_db}, 201

print(create_user_route({"email": "ana@example.com"}))
PY
python3 anti_patron.py
```

Que decir (literal):

"Este codigo funciona, pero escala mal: la ruta decide todo y queda acoplada a demasiadas responsabilidades." 

### B2. Version separada por responsabilidades (6 min)

Ejecuta:

```bash
cat > separacion_responsabilidades.py <<'PY'
def validate_user(payload):
    if 'email' not in payload:
        return "email requerido"
    if '@' not in payload['email']:
        return "email invalido"
    return None

def save_user(repo, payload):
    repo.append(payload)
    return payload

def create_user_controller(repo, payload):
    error = validate_user(payload)
    if error:
        return {"error": error}, 400
    user = save_user(repo, payload)
    return {"ok": True, "user": user}, 201

repo = []
print(create_user_controller(repo, {"email": "ana@example.com"}))
print(create_user_controller(repo, {"email": "correo-invalido"}))
PY
python3 separacion_responsabilidades.py
```

Que decir (literal):

"Separar responsabilidad no es para escribir mas lineas; es para poder cambiar una parte sin romper todo lo demas." 

## Bloque C - Entornos virtuales y flujo uv (12 min)

### C1. Por que aislar dependencias (3 min)

Que decir (literal):

"Si dos proyectos usan versiones distintas del mismo paquete, sin entorno virtual tienes conflicto seguro." 

### C2. Demo con `uv` (6 min)

Ejecuta:

```bash
mkdir -p fastapi_demo && cd fastapi_demo
uv init
uv add fastapi uvicorn
uv run python -c "import fastapi; print('FastAPI OK:', fastapi.__version__)"
```

Si `uv` no esta disponible, plan B inmediato:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn
python -c "import fastapi; print('FastAPI OK:', fastapi.__version__)"
```

### C3. Reproducibilidad en equipo (3 min)

Que decir (literal):

"La regla de oro: compartimos manifest y lockfile, no compartimos la carpeta del entorno virtual." 

Checklist verbal:

- Versionar `pyproject.toml` y `uv.lock`.
- Ignorar `.venv/`.

## Bloque D - FastAPI minimo funcional (18 min)

### D1. Crear app base y endpoint de salud (6 min)

Ejecuta:

```bash
cat > main.py <<'PY'
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class UserCreate(BaseModel):
    name: str
    email: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/users/{user_id}")
def get_user(user_id: int, active: bool = True):
    return {"user_id": user_id, "active": active}

@app.post("/users")
def create_user(payload: UserCreate):
    return {"message": "usuario creado", "data": payload.model_dump()}
PY
```

### D2. Correr servidor y probar (7 min)

Ejecuta en terminal 1:

```bash
uv run uvicorn main:app --reload
```

Ejecuta en terminal 2:

```bash
curl -s http://127.0.0.1:8000/health
curl -s "http://127.0.0.1:8000/users/42?active=false"
curl -s -X POST http://127.0.0.1:8000/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Ana","email":"ana@example.com"}'
```

Que decir (literal):

"Ya tenemos entrada (request), validacion (Pydantic) y salida (response) en menos de 30 lineas." 

### D3. Mostrar validacion fallida (5 min)

Ejecuta:

```bash
curl -s -X POST http://127.0.0.1:8000/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Ana","email":123}'
```

Que decir (literal):

"FastAPI valida automaticamente y responde con error claro. Eso reduce bugs y trabajo manual de validacion." 

## Bloque E - Cierre y chequeo de comprension (9 min)

Preguntas de chequeo:

- "Que diferencia practica hay entre separar por capas y no separar?"
- "Que archivo permite reproducir exactamente dependencias en flujo con uv?"
- "Que ventaja te da Pydantic en FastAPI sin escribir validadores manuales?"

Que decir (literal):

"Si hoy se llevan una idea, que sea esta: backend profesional = decisiones de arquitectura + habitos de entorno + contratos claros de API." 

## 5) Prompts exactos para demo con OpenClaw

Prompt 1 - Refactor de responsabilidades:

```text
Actua como senior backend en Python.
Tengo este codigo donde una ruta mezcla validacion, logica de negocio y acceso a datos.
Quiero que lo refactorices separando en funciones o capas con nombres claros.
Requisitos:
1) Mantener funcionalidad.
2) Devolver codigo completo ejecutable.
3) Explicar en 5 bullets por que mejora mantenibilidad.
4) Evitar frameworks; solo Python puro.
```

Prompt 2 - Comparacion de arquitectura:

```text
Explica con una tabla breve cuando usar MVC, arquitectura en capas, hexagonal y serverless en un backend pequeno/mediano.
Incluye: ventaja principal, riesgo principal y una senal de que no conviene usarla.
Mantenerlo en espanol, maximo 220 palabras.
```

Prompt 3 - Mejora de API FastAPI:

```text
Tengo una API FastAPI minima con endpoints GET y POST.
Propon 3 mejoras de nivel junior-intermedio aplicables hoy mismo:
- una de estructura de carpetas,
- una de validacion/errores,
- una de pruebas.
Incluye snippets cortos y comandos para ejecutarlas.
```

## 6) Plan de contingencia

Si falla `uv`:

- Cambiar inmediatamente a flujo `venv + pip` y continuar demo sin detener clase.

Si falla el puerto 8000:

```bash
uv run uvicorn main:app --reload --port 8001
```

Si no responde `curl`:

- Abrir `http://127.0.0.1:8000/docs` y probar desde Swagger UI para mostrar que el servidor esta vivo.

## 7) Checklist final para el profesor

- Se explicaron las 4 piezas: arquitectura, responsabilidades, entorno y FastAPI.
- Se ejecuto al menos 1 refactor de responsabilidades en vivo.
- Se levanto FastAPI y se probaron endpoints GET y POST.
- Se mostro al menos 1 error de validacion real.
- Se cerro con preguntas de chequeo y siguiente paso.

## 8) Siguiente paso sugerido para class_29

Mini proyecto guiado: API de tareas con estructura por capas (`routers/`, `services/`, `repositories/`, `schemas/`), usando `uv`, validacion Pydantic y persistencia simulada en memoria.