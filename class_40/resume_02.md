# Class 40 - Puntos Clave: Contenedores, Docker y Docker Compose

## 1. El problema fundamental: "Funciona en mi máquina"

- Tu aplicación depende del **entorno completo** (SO, runtime, librerías, configuración).
- `requirements.txt` y entornos virtuales **no son suficientes** porque no incluyen dependencias del sistema.
- **Solución real**: empaquetar la aplicación **junto con todo su entorno** en una unidad portátil → el **contenedor**.

---

## 2. Conceptos clave de Contenedores

| Concepto | Definición |
|---|---|
| **Contenedor** | Unidad autónoma y aislada que agrupa app + entorno (runtime, librerías, config). Ligero y portátil. |
| **Imagen** | Plano de **solo lectura**. Como una **clase** en programación. |
| **Contenedor (ejecución)** | Instancia viva de una imagen. Como un **objeto**. Escribible, aislado y **efímero** (los cambios se pierden al detenerse). |
| **Capas** | Las imágenes se construyen por capas: base → dependencias → código. Esto hace las compilaciones **eficientes** (cache). |

**Analogía del contenedor de envío**: un contenedor guarda mercancías de forma segura y las protege del entorno externo. Puede cargarse en cualquier barco, camión o tren y el contenido permanece igual.

---

## 3. Contenedores vs Máquinas Virtuales (diferencia CLAVE)

| Aspecto | VM | Contenedor |
|---|---|---|
| **Tamaño** | Gigabytes (SO completo) | Megabytes (app + deps) |
| **Inicio** | Minutos | Segundos / milisegundos |
| **Kernel** | Cada VM tiene su propio kernel | **Comparten el kernel del host** |
| **Aislamiento** | Fuerte (hipervisor + SO invitado) | Moderado (namespaces / cgroups) |

- **Usa VMs** cuando necesites aislamiento completo de SO o seguridad multi-inquilino.
- **Usa contenedores** para desarrollo diario, apps que escalan horizontalmente, despliegues rápidos.

**Error común**: NO trates un contenedor como una VM. Cada contenedor ejecuta **UN solo proceso principal**. Si necesitas web + base de datos + worker, son **tres contenedores**.

---

## 4. Docker: la herramienta que hace práctico el concepto

**Ecosistema Docker** (4 piezas):

1. **Dockerfile** → la receta
2. **Imagen** → el plano
3. **Contenedor** → la instancia
4. **Docker Hub** → el registro (como npm pero para imágenes)

### Comandos esenciales

```bash
# Gestión de imágenes
docker pull python:3.11-slim   # descargar
docker images                   # listar locales
docker rmi python:3.11-slim   # eliminar

# Gestión de contenedores
docker run python:3.11-slim                     # primer plano
docker run -it python:3.11-slim bash            # interactivo
docker run -d -p 5432:5432 postgres:16         # background + puertos
docker ps / docker ps -a                        # listar
docker stop <id> / docker rm <id>               # detener / eliminar
docker exec -it <id> bash                       # shell dentro del contenedor

# Construir
docker build -t myapp:1.0 .                     # construir imagen
```

### Dockerfile: las 5 instrucciones básicas

```dockerfile
FROM python:3.11-slim   # imagen base (SIEMPRE primera línea)
WORKDIR /app            # directorio de trabajo
COPY requirements.txt . # copiar archivos
RUN pip install -r requirements.txt  # ejecutar en build
COPY . .                # copiar código
CMD ["python", "main.py"]  # comando al arrancar
```

**Mejores prácticas**: usa etiquetas específicas (no `latest`), minimiza capas con `&&`, usa `.dockerignore`, ordena capas de menos a más cambiantes.

---

## 5. Docker Compose: orquestación multi-contenedor

**¿Qué problema resuelve?** Gestionar múltiples contenedores manualmente es un desastre. Compose te permite definirlos **todos en un solo archivo YAML**.

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

volumes:
  db_data:
```

### Conceptos clave de Compose

- **Servicios**: cada uno = un contenedor
- **Puertos**: `"host:contenedor"`
- **Redes**: los servicios se comunican por **nombre del servicio** (NO `localhost`)
- **Variables de entorno**: usa `${VAR}` y un archivo `.env` para secretos
- **Volúmenes**: para persistir datos más allá del ciclo de vida del contenedor
- **`depends_on`**: controla orden de inicio (pero no garantiza que el servicio esté listo)

**Comando mágico**: `docker compose up` → levanta todo. `docker compose down` → lo detiene todo.

---

## 6. Proyecto del módulo: Monorepo Containerization

Se aplica todo lo anterior a un monorepo real con:
- **`/uis/`** → frontend (Next.js) → su Dockerfile
- **`/services/`** → backend (FastAPI) → su Dockerfile
- **`docker-compose.yml`** con **bind mounts** para recarga en caliente (hot reload)

---

## 🔥 Resumen en 3 frases

1. **Contenedores** = empaquetar app + entorno para que funcione igual en todos lados.
2. **Docker** = la herramienta para crear, compartir y ejecutar contenedores (imágenes, Dockerfiles, Docker Hub).
3. **Docker Compose** = orquestar múltiples contenedores (web + DB + etc.) con un solo archivo YAML y un solo comando.