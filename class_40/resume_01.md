# Guia Docente Completa: Class 40
## Contenedores, Docker y Docker Compose + Proyecto Monorepo Containerization

Duracion objetivo: 60-75 minutos.

Fuentes usadas para esta guia:
- class_40/containers_without_docker_a_conceptual_guide.json
- class_40/docker_essentials_building_a_conceptual_foundati.json
- class_40/docker_compose_orchestrating_multi_container_app.json
- class_40/ai-eng-contenedor-monorepo-compania_project_README.es.md

---

## 1) Objetivos de aprendizaje

Al cerrar la clase, el estudiante deberia poder:
- Explicar el problema de consistencia del entorno ("funciona en mi maquina") y por que las soluciones tradicionales no lo resuelven.
- Distinguir entre imagen de contenedor (plano solo lectura) y contenedor (instancia en ejecucion) usando la analogia clase/objeto.
- Diferenciar contenedores de maquinas virtuales a nivel arquitectonico (kernel compartido vs hipervisor + SO invitado completo).
- Ejecutar comandos Docker esenciales: pull, images, run, ps, exec, stop, rm, rmi, build.
- Escribir un Dockerfile basico con FROM, WORKDIR, COPY, RUN, CMD y aplicar mejores practicas (capas minimas, etiquetas especificas, .dockerignore).
- Explicar que problema resuelve Docker Compose (orquestacion multi-contenedor).
- Leer y escribir un docker-compose.yml con servicios, puertos, redes, variables de entorno y volumenes.
- Conectar lo anterior con el proyecto de contenerizacion del monorepo: Dockerfiles para `/uis/` y `/services/`, docker-compose.yml con bind mounts y recarga en caliente.

---

## 2) Agenda recomendada (70 min)

- Apertura y contexto: 5 min
- Bloque A. El problema del entorno y la idea de los contenedores: 15 min
- Bloque B. Docker: imagenes, comandos esenciales y Dockerfiles: 20 min
- Bloque C. Docker Compose: orquestacion multi-servicio: 15 min
- Bloque D. Puente directo al proyecto del modulo: 12 min
- Cierre y chequeo: 3 min

Recorte a 60 min:
- Reducir 5 min del Bloque B (saltar mejores practicas de Dockerfile, solo mostrar estructura basica).
- Reducir 5 min del Bloque C (no hacer demo de variables de entorno, solo nombrarlas).

Extension a 75 min:
- Sumar 5 min en Bloque B para comparar docker run vs docker compose paso a paso.
- Sumar 5 min en Bloque D para revisar el docker-compose.yml completo del proyecto y detectar errores comunes.

---

## 3) Guion docente detallado

## Apertura (5 min)

Que decir (literal):

"Hoy vamos a entender tres capas que resuelven el problema mas antiguo del desarrollo: que funcione igual en todas las maquinas. Primero, el concepto de contenedor. Segundo, Docker como la herramienta que lo hace practico. Tercero, Docker Compose para orquestar multiples servicios."

"Todo esto lo aplicamos directamente en el proyecto de contenerizar el monorepo de la empresa."

Prompt de arranque para OpenClaw:

```text
Resumen en 5 bullets del objetivo de esta clase:
1) entender contenedores como empaquetado de app + entorno,
2) diferenciar imagen de contenedor,
3) comandos Docker esenciales y Dockerfiles,
4) orquestacion multi-contenedor con Docker Compose,
5) dockerizar un monorepo real con Next.js y FastAPI.
Usa lenguaje corto y tecnico.
```

---

## Bloque A. El problema del entorno y la idea de los contenedores (15 min)

Lecciones base:
- 0 Bienvenido a contenedores
- 1 El problema de consistencia del entorno
- 2 Que es un contenedor
- 2.1 La idea central de los contenedores
- 3 Imagenes de contenedores explicadas
- 3.1 De imagen a contenedor
- 3.2 Aislamiento de contenedores
- 3.4 Concepto equivocado comun contenedores vs vms
- 4 Arquitectura de maquinas virtuales
- 4.1 Contenedores vs vms diferencias clave
- 4.2 Cuando usar vms vs contenedores

Que decir (literal):

"El problema central: tu app funciona en tu maquina porque tienes las versiones exactas de Python, las librerias, el sistema operativo. Tu companero tiene otras versiones y falla. Eso es el problema de 'funciona en mi maquina'."

"Requirements.txt y entornos virtuales ayudan, pero no incluyen dependencias a nivel de sistema. No resuelven todo."

"Un contenedor empaqueta la aplicacion junto con TODO su entorno: runtime, librerias, configuracion, sistema de archivos. Es una unidad autonoma y portatil."

Analogia del contenedor de envio:
- "Un contenedor de envio guarda mercancias de forma segura y las protege del entorno externo."
- "Puede cargarse en cualquier barco, camion o tren, y el contenido permanece igual."
- "Un contenedor de software hace lo mismo: tu app se ejecuta identicamente en cualquier maquina."

"Imagen vs contenedor: la imagen es el plano de solo lectura (como una clase en Python). El contenedor es la instancia en ejecucion (como un objeto). Puedes crear muchos contenedores desde una misma imagen."

"Las imagenes se construyen por capas: capa base (OS minimo o runtime), capa de dependencias (pip install), capa de aplicacion (codigo). Esto hace las compilaciones eficientes."

"El runtime de contenedor anade una capa escribible encima de las capas de solo lectura de la imagen. Ahi escribe logs, cache, archivos temporales."

"Una confusion comun: NO trates un contenedor como una VM ejecutando multiples procesos. Cada contenedor ejecuta UN solo proceso principal. Si necesitas base de datos + web + worker, son tres contenedores."

Tabla comparativa (del JSON, leccion 4.1):
- VMs: Gigabytes, minutos de inicio, aislamiento fuerte (kernel separado), recursos fijos.
- Contenedores: Megabytes, segundos o milisegundos, aislamiento moderado (kernel compartido), recursos dinamicos.

"Cuando usar VMs: cuando necesitas aislamiento completo de SO, ejecutar diferentes SOs en el mismo host, o seguridad multi-inquilino (ej: AWS)."

"Cuando usar contenedores: despliegue rapido y liviano de aplicaciones, apps que escalan horizontalmente, desarrollo diario."

Pregunta de chequeo:
- "Cual es la diferencia clave entre una imagen de contenedor y un contenedor en ejecucion? Usen la analogia clase/objeto."

---

## Bloque B. Docker: imagenes, comandos esenciales y Dockerfiles (20 min)

Lecciones base:
- 1 Que es docker
- 1.1 Docker vs contenedores
- 2 Resumen del ecosistema docker
- 3 Introduccion a docker hub
- 4 Comandos esenciales de docker
- 4.1 Manejo de imagenes con comandos
- 4.2 Ejecutando y manejando contenedores
- 4.3 Mapeo de puertos y comandos de depuracion
- 5 Que es un dockerfile
- 5.1 Instrucciones basicas de dockerfile
- 5.2 Construyendo imagenes desde dockerfiles
- 5.3 Mejores practicas de dockerfile

Que decir (literal):

"Docker es la herramienta que hizo practica la contenerizacion. No es el unico runtime de contenedores, pero es el mas popular. Estandariza como construir, compartir y ejecutar contenedores."

"El ecosistema Docker tiene cuatro piezas: Dockerfile (la receta), Imagen (el plano), Contenedor (la instancia), y Docker Hub (el registro donde se comparten imagenes)."

"En Docker Hub hay imagenes oficiales (python, nginx, postgres), verificadas (de empresas), y comunitarias (con precaucion)."

Demo de comandos esenciales (tal como aparecen en las lecciones):

```bash
# Gestion de imagenes
docker pull python:3.11-slim
docker images
docker rmi python:3.11-slim
```

```bash
# Ejecucion de contenedores
docker run python:3.11-slim          # primer plano
docker run -it python:3.11-slim bash # interactivo
docker run -d -p 5432:5432 postgres:16  # segundo plano (detached)
```

```bash
# Gestion de contenedores
docker ps          # en ejecucion
docker ps -a       # todos (incluidos detenidos)
docker stop <id>   # detener
docker rm <id>     # eliminar
```

```bash
# Depuracion y mapeo de puertos
docker exec -it <id> bash           # shell dentro del contenedor
docker run -d -p 5432:5432 postgres:16  # mapeo puerto_host:puerto_contenedor
```

```bash
# Construccion de imagenes desde Dockerfile
docker build -t myapp:1.0 .
```

Que decir (literal):

"Un Dockerfile es un archivo de texto plano con instrucciones para construir una imagen. Las cinco instrucciones esenciales son:"

```dockerfile
FROM python:3.11-slim   # Imagen base (SIEMPRE primera linea)
WORKDIR /app            # Directorio de trabajo
COPY requirements.txt . # Copiar archivos
RUN pip install -r requirements.txt  # Ejecutar comandos en construccion
COPY . .                # Copiar codigo
CMD ["python", "main.py"]  # Comando al arrancar el contenedor
```

Mejores practicas del JSON (leccion 5.3):
- "Usa etiquetas especificas: FROM python:3.11-slim, NO FROM python:latest."
- "Minimiza capas: combina RUN con &&."
- "Usa .dockerignore para excluir node_modules, __pycache__, .env."
- "Ordena las capas de menos a mas cambiante: las dependencias antes que el codigo para aprovechar cache."

Prompt para OpenClaw (codigo de apoyo):

```text
Genera un Dockerfile minimal para una API FastAPI con estas reglas:
- Imagen base python:3.11-slim.
- WORKDIR /app.
- Copiar requirements.txt y hacer pip install primero.
- Copiar el resto del codigo despues.
- CMD con uvicorn para arrancar con --reload.
- Incluir un .dockerignore que excluya __pycache__, *.pyc, .env y .git.
```

---

## Bloque C. Docker Compose: orquestacion multi-servicio (15 min)

Lecciones base:
- 0 Bienvenido a docker compose
- 1 Fundamentos de docker compose
- 1.1 Servicios puertos y redes
- 1.2 Variables de entorno
- 2 Escribiendo docker compose.yml
- 2.1 Configurando un proyecto multi servicio
- 2.2 Desafio de aplicacion multi servicio
- 3 Arquitectura del proyecto con compose
- 3.1 Un proyecto dockerizado completo

Que decir (literal):

"Con Docker solo gestionas contenedores individuales. Pero las aplicaciones reales tienen web + base de datos + cache. Ahi aparece Docker Compose."

"Docker Compose permite definir toda la pila en un solo archivo YAML y arrancar todo con un comando: docker compose up."

"El archivo docker-compose.yml tiene tres secciones principales: services, networks y volumes."

Demo del docker-compose.yml (basado en el JSON, leccion 2.1 y 3.1):

```yaml
services:
  web:
    build: .
    ports:
      - "3000:3000"
    depends_on:
      - db
    environment:
      - DATABASE_URL=postgres://postgres:${DB_PASSWORD}@db:5432/appdb

  db:
    image: postgres:15-alpine
    volumes:
      - db_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=appdb

volumes:
  db_data:
```

Que decir (literal):

"Los servicios se comunican por nombre de servicio (db, web), NO por localhost. 'localhost' dentro de un contenedor se refiere a si mismo."

"Las variables de entorno van en un archivo .env separado. Nunca pongas secretos en docker-compose.yml."

"depends_on controla orden de inicio de contenedores, pero NO espera a que el servicio este listo. La aplicacion debe tener logica de reintento."

"Los volumenes nombrados persisten datos fuera del ciclo de vida del contenedor. Esencial para bases de datos."

"El proyecto dockerizado completo tiene cuatro archivos: Dockerfile, docker-compose.yml, .env, .dockerignore."

Prompt para OpenClaw:

```text
Genera un docker-compose.yml minimo con dos servicios:
1) web: construido desde Dockerfile local, puerto 3000:3000, depende de db, variable DATABASE_URL usando .env.
2) db: imagen postgres:15-alpine, volumen db_data, usa variable POSTGRES_PASSWORD desde .env.
Incluye el volume nombrado. NO incluyas secretos hardcodeados.
```

---

## Bloque D. Puente directo al proyecto del modulo (12 min)

Fuente de proyecto:
- ai-eng-contenedor-monorepo-compania_project_README.es.md

Que decir (literal):

"Este proyecto cierra el circulo. Ya sabemos que es un contenedor, como construir imagenes con Docker, y como orquestar multiples servicios con Compose. Ahora aplicamos todo al monorepo de la empresa."

"El problema real: cada vez que un nuevo desarrollador se incorpora, la puesta en marcha tarda horas. Conflictos de versiones de Node, Python, dependencias globales distintas, configuracion manual."

"La solucion: entorno de desarrollo definido en codigo, versionado junto al proyecto, ejecutable con un solo comando."

Resumen de requisitos clave del proyecto:

**Dockerfile de interfaces (`/uis/Dockerfile`):**
- Basado en imagen oficial de Node (Alpine).
- Instalar dependencias de `/uis/website` y `/uis/backoffice` por separado.
- CMD invoca `start.sh` que arranca ambas apps Next.js en puertos distintos (3000 y 3001).
- `.dockerignore` excluye node_modules, .next, .env*, *.log.

**Dockerfile del backend (`/services/Dockerfile`):**
- Basado en imagen oficial de Python.
- Instalar `uv`, luego `uv pip install -r requirements.txt`.
- Arrancar Uvicorn con `--reload`.
- `.dockerignore` excluye __pycache__, *.pyc, .env*, tests/, *.log.

**Docker Compose (`docker-compose.yml`):**
- Dos servicios: interfaces (build desde `/uis/`) y backend (build desde `/services/`).
- Bind mounts sobre el codigo fuente para recarga en caliente.
- Puertos correctos: website 3000, backoffice 3001, backend segun corresponda.
- Red Docker con nombre definido. URLs de conexion por nombre de servicio, NO por localhost.
- Variables de entorno desde `.env`. `.env` en `.gitignore`.

**Criterios de evaluacion del proyecto:**
- `docker compose up` desde la raiz levanta la plataforma completa sin errores ni pasos adicionales.
- Cambios en codigo host se reflejan en navegador sin reconstruir imagen (bind mounts).
- Unico contenedor de interfaces arranca ambas apps Next.js en puertos distintos.
- Servicios se comunican por nombre de servicio Docker.
- No hay secretos hardcodeados en Dockerfile ni docker-compose.yml.
- Archivos `.dockerignore` existen en `/uis/` y `/services/`.

Mini plan en pseudocodigo para explicar al grupo:

```text
1. Crear Dockerfile en /uis/:
   - FROM node:20-alpine
   - COPY package.json de website y backoffice
   - RUN npm install en cada uno
   - COPY codigo fuente
   - Crear start.sh que ejecute next dev en :3000 y :3001
   - Crear .dockerignore

2. Crear Dockerfile en /services/:
   - FROM python:3.11-slim
   - RUN pip install uv
   - COPY requirements.txt
   - RUN uv pip install -r requirements.txt
   - COPY codigo fuente
   - CMD uvicorn main:app --reload --host 0.0.0.0
   - Crear .dockerignore

3. Crear docker-compose.yml en raiz:
   - services.uis: build /uis/, ports 3000:3000 y 3001:3001,
     volumes con bind mount, depends_on services.api
   - services.api: build /services/, ports 8000:8000,
     volumes con bind mount, env desde .env
   - networks con nombre explicito

4. Crear .env en raiz (en .gitignore)
5. Ejecutar: docker compose up
6. Verificar hot reload: cambiar codigo -> ver cambio sin rebuild
```

---

## 4) Comandos de clase listos para copiar

Herramientas necesarias segun el contenido de esta clase:
- Docker Engine + Docker Compose CLI v2 (Docker Desktop o instalacion manual).
- Editor de texto para Dockerfiles y docker-compose.yml.

```bash
# Verificar instalacion de Docker
docker --version
docker compose version
```

```bash
# Comandos esenciales de Docker (del Bloque B)
docker pull python:3.11-slim
docker images
docker run -it python:3.11-slim bash
docker run -d -p 5432:5432 postgres:16
docker ps
docker ps -a
docker exec -it <id> bash
docker stop <id>
docker rm <id>
docker rmi python:3.11-slim
```

```bash
# Construir imagen desde Dockerfile
docker build -t myapp:1.0 .
```

```bash
# Comandos de Docker Compose (del Bloque C)
docker compose up          # Levantar todos los servicios
docker compose up -d       # En segundo plano
docker compose down        # Detener y eliminar contenedores/redes
docker compose ps          # Estado de servicios
docker compose logs -f     # Logs en vivo
```

```bash
# Flujo del proyecto (paso final)
cd /ruta/al/monorepo
docker compose up
# Ver website en http://localhost:3000
# Ver backoffice en http://localhost:3001
```

---

## 5) Checklist de preparacion docente

Antes de clase:
- Confirmar que existen los 3 JSON de contenidos en class_40.
- Confirmar que existe el asset y README del proyecto en class_40.
- Tener Docker instalado y funcional para demos en vivo.
- Preparar terminal dividida: una para comandos Docker, otra para YAML.
- Tener a mano el docker-compose.yml del proyecto para mostrarlo completo.

Durante clase:
- Verificar que el grupo distingue imagen de contenedor antes de pasar a Docker.
- Hacer que ejecuten al menos docker pull y docker run -it frente a ellos.
- En Compose, senalar explicitamente: los servicios NO se comunican por localhost, se comunican por nombre de servicio.
- Proyecto: enfatizar que los bind mounts son esenciales para hot reload.

Contingencia (si falla demo en vivo):
- Leer y analizar los Dockerfiles del proyecto en pantalla sin ejecutar Docker.
- Mostrar capturas de docker compose ps y docker compose logs.
- Convertir la practica en pseudocodigo y revision por pares.

---

## 6) Preguntas de comprobacion final

- Cual es el problema que resuelven los contenedores? ("Funciona en mi maquina")
- Que diferencia hay entre docker pull y docker run?
- En un Dockerfile, para que sirve WORKDIR y que pasa si no lo usas?
- Por que los servicios en Docker Compose NO deben usar localhost para conectarse entre si?
- Que hace depends_on en docker-compose.yml y que NO garantiza?
- Que archivos debe crear el proyecto de contenerizacion del monorepo?
- Donde se ponen las variables de entorno con secretos? (en .env, no en docker-compose.yml)

---

## 7) Cierre sugerido (literal)

"Los contenedores no son una moda: resuelven un problema real que vas a encontrar en cualquier equipo de desarrollo. Docker estandariza como crear y ejecutar esos contenedores. Docker Compose organiza multiples contenedores como un sistema."

"El proyecto de contenerizar el monorepo es exactamente lo que harias en tu primer semana en un equipo nuevo: definir el entorno en codigo para que cualquiera pueda clonar, ejecutar docker compose up y tener todo funcionando."

"Si entiendes estos tres niveles —concepto, herramienta, orquestacion— puedes dockerizar cualquier aplicacion."