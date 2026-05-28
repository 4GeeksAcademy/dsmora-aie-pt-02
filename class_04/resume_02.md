# Guia Docente: Fundamentos de la Linea de Comandos (CLI)

Este documento organiza el contenido del modulo como guia para clase online.
El objetivo es pasar de comandos sueltos a una mentalidad de trabajo profesional.

## 1. Objetivos de aprendizaje

Al finalizar la clase, el estudiante deberia poder:

- Navegar por directorios con seguridad usando `pwd`, `ls` y `cd`.
- Ejecutar operaciones CRUD de archivos y carpetas desde terminal.
- Consultar y filtrar contenido con `cat`, `less`, `head`, `tail` y `grep`.
- Aprovechar historial, autocompletado y comodines para productividad.
- Editar archivos rapidos con `nano` y entender lo minimo de `vim`.

## 2. Mapa tematico de la sesion

1. Filosofia de la terminal: eficiencia, automatizacion y control.
2. Navegacion basica del sistema.
3. Gestion de archivos y carpetas.
4. Lectura y busqueda de informacion.
5. Atajos de productividad.
6. Editores de texto en terminal.

## 3. Guion sugerido para clase online (90 minutos)

### Bloque A (15 min): Por que CLI sigue siendo clave

- Diferencia entre GUI y CLI en velocidad y repetibilidad.
- Casos reales donde CLI resuelve tareas complejas en segundos.

### Bloque B (20 min): Navegacion segura

- Practica guiada: `pwd`, `ls -la`, `cd`, `cd ..`, `cd ~`.
- Regla de oro: confirmar ubicacion antes de borrar o mover.

### Bloque C (20 min): CRUD en vivo

- Crear: `mkdir`, `touch`.
- Copiar/mover: `cp`, `mv`.
- Eliminar: `rm` con foco en seguridad.

```bash
mkdir -p demo/src
touch demo/src/app.js
cp demo/src/app.js demo/src/app.backup.js
mv demo/src/app.backup.js demo/src/app.v1.js
```

### Bloque D (20 min): Lectura y busqueda

- Mostrar diferencias entre `cat` y `less`.
- Usar `tail -n` para logs.
- Buscar con `grep -r` e `-i` en un mini proyecto.

### Bloque E (15 min): Productividad y edicion

- TAB, historial, wildcard `*`.
- Edicion express con `nano`.
- Introduccion breve a `vim` para no bloquearse.

## 4. Checklist didactico por tema

- El estudiante navega sin perderse en carpetas.
- Ejecuta CRUD basico sin interfaz grafica.
- Encuentra una cadena en multiples archivos.
- Aplica al menos dos atajos de productividad.

## 5. Actividades practicas para clase

### Actividad 1 (parejas, 10 min)

Crear estructura de proyecto y agregar 3 archivos desde terminal.

### Actividad 2 (individual, 10 min)

Buscar la palabra `TODO` en un directorio y reportar archivo + linea.

### Actividad 3 (cierre, 5 min)

Editar un archivo con `nano`, guardar y verificar cambios con `cat`.

## 6. Preguntas de comprobacion rapida

- Cual es la diferencia entre `cp` y `mv`?
- Para que sirve `cd ..`?
- Que riesgo tiene `rm -rf` y como mitigarlo?
- Cuando usar `less` en lugar de `cat`?

## 7. Errores frecuentes y como corregirlos

- Error: borrar sin confirmar ubicacion.
    Correccion: ejecutar siempre `pwd` + `ls` antes de `rm`.
- Error: no usar comillas en rutas con espacios.
    Correccion: usar rutas sin espacios o entre comillas.
- Error: hacer busquedas demasiado amplias en raiz.
    Correccion: acotar `grep` al directorio del proyecto.

## 8. Cierre para la sesion

- Mensaje clave: CLI multiplica velocidad y reduce friccion tecnica.
- Puente: estos comandos se conectan con Git, despliegue y automatizacion.
- Tarea: recrear un mini flujo local completo solo desde terminal.
