# Resumen Ampliado: Fundamentos de la Línea de Comandos (CLI)

La terminal no es solo una pantalla negra con texto; es la herramienta más poderosa para automatizar tareas y gestionar sistemas de forma profesional.

## 0. Filosofía de la Terminal
*   **Eficiencia:** Realizar tareas repetitivas en segundos.
*   **Automatización:** Escribir scripts que hagan el trabajo por ti.
*   **Control Total:** Acceder a funciones que las interfaces gráficas (GUI) ocultan.

## 1. Navegación y Ubicación
Para dominar la terminal, primero debes saber dónde estás y cómo moverte.

| Comando | Descripción | Ejemplo / Tip |
| :--- | :--- | :--- |
| `pwd` | *Print Working Directory*. Muestra la ruta actual. | Úsalo antes de borrar archivos. |
| `ls` | *List*. Lista el contenido de la carpeta. | `ls -la` (detallado y ocultos). |
| `cd` | *Change Directory*. Navega entre carpetas. | `cd ..` (subir), `cd ~` (home). |
| `clear` | Limpia la pantalla de la terminal. | Atajo: `Ctrl + L`. |

## 2. Gestión de Archivos y Carpetas (CRUD)

| Operación | Comando | Notas Pro |
| :--- | :--- | :--- |
| **Crear Carpeta** | `mkdir [nombre]` | `mkdir -p a/b/c` crea toda la ruta. |
| **Crear Archivo** | `touch [archivo]` | También sirve para actualizar la fecha del archivo. |
| **Copiar** | `cp [origen] [destino]` | Usa `cp -r` para carpetas completas. |
| **Mover / Renombrar** | `mv [origen] [destino]` | Si el destino es un nombre nuevo, lo renombra. |
| **Eliminar** | `rm [archivo]` | **¡PELIGRO!** No hay papelera. Usa `rm -rf` con extrema precaución. |

## 3. Visualización y Búsqueda de Contenido

*   **`cat`**: Muestra todo el texto de una vez. Ideal para archivos cortos.
*   **`less`**: Permite navegar por archivos largos (usa `q` para salir).
*   **`head` / `tail`**: Muestra las primeras o últimas líneas (ej. `tail -n 20 error.log`).
*   **`grep`**: El buscador maestro.
    *   `grep "token" config.json` -> Busca la palabra "token".
    *   `grep -i "error" server.log` -> Ignora mayúsculas/minúsculas.
    *   `grep -r "TODO" .` -> Busca recursivamente en todos los archivos de la carpeta actual.
    *   `grep -ir "db_password" .` -> **Combinado:** Busca "db_password" de forma recursiva ignorando mayúsculas/minúsculas en todo el proyecto.

## 4. Superpoderes y Atajos de Productividad

1.  **Tabulador (TAB):** Empieza a escribir y presiona TAB. La terminal autocompletará el nombre por ti. ¡Es la clave para no cometer errores!
2.  **Flechas Arriba/Abajo:** Navega por tu historial de comandos anteriores.
3.  **`history`**: Muestra una lista numerada de todo lo que has ejecutado.
4.  **Wildcards (*):** El asterisco representa "cualquier cosa".
    *   `rm *.png` -> Borra todos los archivos PNG.
    *   `ls project_*` -> Lista todo lo que empiece por "project_".

## 5. El Flujo de Trabajo Profesional
Un desarrollador rara vez usa la terminal aislada. El flujo típico es:
1.  `cd` al proyecto.
2.  `ls -la` para revisar el estado.
3.  `touch` o `mkdir` para preparar la estructura.
4.  Ejecutar comandos de herramientas como **Git**, **npm** o **Python**.

---
*Dominar estos comandos te sacará del grupo de "usuarios" y te pondrá en el de "desarrolladores". La memoria muscular es clave: ¡Practica cada comando al menos 10 veces!*


## 6. Editores de Texto en la Terminal (Nano y Vim)

Cuando trabajas en la terminal, a menudo necesitas editar archivos rápidamente sin salir de ella.

### Nano: La Simplicidad por Defecto
Ideal para principiantes. Muestra los comandos en la parte inferior.
*   **Abrir:** `nano archivo.txt`
*   **Guardar:** `Ctrl + O` (Enter para confirmar).
*   **Salir:** `Ctrl + X`.

### Vim: El Editor del Poder
Funciona por modos (Normal, Insertar, Comando).
*   **Escribir:** Presiona `i` (Modo Insertar).
*   **Volver:** Presiona `Esc` (Modo Normal).
*   **Guardar y Salir:** Escribe `:wq` y `Enter`.
*   **Salir sin guardar:** Escribe `:q!` y `Enter`.
