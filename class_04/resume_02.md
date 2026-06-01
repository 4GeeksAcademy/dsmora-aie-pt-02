# Guia Docente: Fundamentos de la Linea de Comandos (CLI)

Este documento organiza el contenido del modulo como guia para clase online.
El objetivo es pasar de comandos sueltos a una mentalidad de trabajo profesional.

## 1. Objetivos de aprendizaje

Al finalizar la clase, el estudiante deberia poder:

- Navegar por directorios con seguridad usando `pwd`, `ls` y `cd`.
    Como explicarlo: establece rutina fija de ubicacion antes de cualquier operacion sensible.
- Ejecutar operaciones CRUD de archivos y carpetas desde terminal.
    Como explicarlo: practica crear, mover, copiar y borrar en un entorno de prueba controlado.
- Consultar y filtrar contenido con `cat`, `less`, `head`, `tail` y `grep`.
    Como explicarlo: asigna un comando segun objetivo (lectura rapida, paginada, busqueda puntual).
- Aprovechar historial, autocompletado y comodines para productividad.
    Como explicarlo: demuestra ahorro de tiempo real con TAB, flechas y patrones `*`.
- Editar archivos rapidos con `nano` y entender lo minimo de `vim`.
    Como explicarlo: enseña solo atajos de supervivencia para editar y salir sin bloqueo.

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
    Como explicarlo: compara misma tarea en GUI y CLI midiendo pasos y tiempo.
- Casos reales donde CLI resuelve tareas complejas en segundos.
    Como explicarlo: muestra comandos encadenados para procesar multiples archivos rapidamente.

### Bloque B (20 min): Navegacion segura

- Practica guiada: `pwd`, `ls -la`, `cd`, `cd ..`, `cd ~`.
    Como explicarlo: recorre rutas reales y confirma siempre ubicacion actual.
- Regla de oro: confirmar ubicacion antes de borrar o mover.
    Como explicarlo: institucionaliza doble verificacion para prevenir perdida de datos.

### Bloque C (20 min): CRUD en vivo

- Crear: `mkdir`, `touch`.
    Como explicarlo: parte de estructura vacia y construye proyecto desde cero.
- Copiar/mover: `cp`, `mv`.
    Como explicarlo: diferencia duplicar vs trasladar para evitar sobrescrituras accidentales.
- Eliminar: `rm` con foco en seguridad.
    Como explicarlo: acota rutas y valida con `ls` antes de ejecutar borrado.

```bash
mkdir -p demo/src
touch demo/src/app.js
cp demo/src/app.js demo/src/app.backup.js
mv demo/src/app.backup.js demo/src/app.v1.js
```

### Bloque D (20 min): Lectura y busqueda

- Mostrar diferencias entre `cat` y `less`.
    Como explicarlo: usa archivo largo para justificar lectura paginada.
- Usar `tail -n` para logs.
    Como explicarlo: sigue eventos recientes sin abrir archivos completos.
- Buscar con `grep -r` e `-i` en un mini proyecto.
    Como explicarlo: filtra resultados por carpeta para evitar ruido innecesario.

### Bloque E (15 min): Productividad y edicion

- TAB, historial, wildcard `*`.
    Como explicarlo: repite el mismo flujo primero manual y luego con atajos.
- Edicion express con `nano`.
    Como explicarlo: cubre abrir, editar, guardar y salir en menos de un minuto.
- Introduccion breve a `vim` para no bloquearse.
    Como explicarlo: ensena entrar en insercion, guardar y salir sin profundizar mas.

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
