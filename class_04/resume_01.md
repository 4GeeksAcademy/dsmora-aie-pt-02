# Resumen Detallado: Fundamentos del Sistema de Archivos

Este resumen profundiza en la organización, jerarquía y gestión de archivos, conceptos críticos para cualquier desarrollador web.

## 📂 1. Conceptos Fundamentales: Contenido vs. Ubicación

Un archivo no es solo la información que contiene (bytes), sino también su contexto dentro de una estructura.
*   **Contenido:** El código HTML, las reglas CSS o los assets.
*   **Ubicación:** La "dirección" exacta que permite al sistema o al navegador encontrar ese contenido. Sin una ubicación correcta, el contenido es inaccesible.

## 🌳 2. Jerarquía y Estructura de "Árbol"

Los sistemas de archivos modernos utilizan una estructura de árbol invertido.

```mermaid
graph TD
    Root[/] --> Home[home/]
    Root --> Etc[etc/]
    Home --> User[usuario/]
    User --> Projects[projects/]
    Projects --> Portfolio[portfolio/]
    Portfolio --> Index[index.html]
    Portfolio --> CSS[css/]
    Portfolio --> Assets[assets/]
    CSS --> Style[style.css]
    Assets --> Logo[logo.png]
```

### Relaciones Clave:
*   **Carpeta Raíz (Root):** El nivel superior. En Linux/macOS es `/`, en Windows suele ser `C:\`.
*   **Padre (Parent):** Directorio que contiene otros elementos. `portfolio` es padre de `index.html`.
*   **Hijo (Child):** Elemento contenido en otro. `style.css` es hijo de `css`.
*   **Hermanos (Siblings):** Elementos en el mismo nivel. `index.html`, `css/` y `assets/` son hermanos.

## 📍 3. Rutas: El Mapa del Desarrollador

### A. Rutas Absolutas
Definen la ubicación desde la raíz absoluta del sistema.
*   **Ejemplo:** `/home/user/project/index.html`
*   **Uso:** Raro en desarrollo web local, ya que las rutas cambian al subir el sitio a un servidor.

### B. Rutas Relativas (El estándar de oro)
Definen la ubicación partiendo de donde está el archivo actual.
*   `archivo.html`: El archivo está en la misma carpeta.
*   `carpeta/archivo.html`: Entra en una subcarpeta.
*   `../`: Sube un nivel hacia el padre.

| Situación | Ruta Ejemplo |
| :--- | :--- |
| Mismo nivel | `archivo.txt` |
| Dentro de una carpeta | `img/foto.jpg` |
| Subir un nivel | `../otro_archivo.html` |
| Subir y entrar en otra | `../css/styles.css` |

## 🚀 4. Punto de Entrada y Buenas Prácticas

*   **index.html:** Es el nombre reservado. Los servidores web buscan este archivo automáticamente cuando entras en un directorio.
*   **Nivel de Anidación:** Mantén tu estructura simple. Evita `proyecto/web/src/assets/images/icons/social/fb.png` si puedes simplificarlo.
*   **Case Sensitivity:** En servidores Linux, `Imagen.png` e `imagen.png` son archivos distintos. Usa siempre minúsculas para evitar errores.
*   **Caracteres Prohibidos:** Evita espacios y tildes en nombres de archivos (ej. usa `mi-archivo.js` en lugar de `mi archivo.js`).

## 🛠️ Ejercicio de Verificación
Si estás en `css/style.css` y quieres usar una imagen en `assets/bg.jpg`, ¿cuál es la ruta correcta?
*   **Respuesta:** `../assets/bg.jpg` (Sales de `css` y entras en `assets`).

---
*Este conocimiento es la base para que tus hojas de estilo, scripts e imágenes funcionen siempre, sin importar dónde despliegues tu código.*

