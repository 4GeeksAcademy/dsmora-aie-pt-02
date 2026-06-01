# Guia Docente: Git y el Ciclo de Vida del Desarrollo

Este documento transforma el resumen del modulo en una guia para clase online.
El objetivo es que el estudiante domine el flujo real de trabajo con Git,
desde cambios locales hasta colaboracion con repositorios remotos.

## 1. Objetivos de aprendizaje

Al finalizar la clase, el estudiante deberia poder:

- Explicar el modelo de tres estados: working directory, staging area y repository.
  Como explicarlo: representa el flujo en tres cajas y mueve un cambio de una a otra con comandos reales.
- Usar correctamente `git add`, `git commit`, `git push` y `git pull`.
  Como explicarlo: practica la secuencia minima diaria y explica que aporta cada comando al flujo.
- Interpretar `git status` y `git log` para diagnosticar el estado del proyecto.
  Como explicarlo: lee ejemplos de salida y pregunta que accion segura tomarian antes de continuar.
- Crear historiales de commits claros, atomicos y trazables.
  Como explicarlo: separa cambios por intencion para que cada commit responda a un unico objetivo.
- Resolver situaciones basicas de conflicto sin perder trabajo.
  Como explicarlo: simula conflicto controlado y guia resolucion paso a paso hasta cerrar merge.

## 2. Mapa tematico de la sesion

1. Modelo mental de Git y estados del archivo.
2. Comandos esenciales de configuracion y flujo diario.
3. Buenas practicas de commits y mensajes.
4. Ramas basicas para aislar cambios.
5. Sincronizacion con remoto y manejo inicial de conflictos.

## 3. Guion sugerido para clase online (90 minutos)

### Bloque A (15 min): Modelo mental

- Explicar Git como sistema de snapshots, no como "guardar versiones sueltas".
  Como explicarlo: compara carpeta de copias manuales vs historial de snapshots enlazados.
- Mostrar los 3 estados y el movimiento de cambios entre estados.
  Como explicarlo: ejecuta comandos en vivo y mapea cada paso al estado correspondiente.

Diagrama para explicar en vivo:

```mermaid
graph LR
    WD[Working Directory] -->|git add| ST[Staging Area]
    ST -->|git commit| LR[Local Repository]
    LR -->|git push| RR[Remote Repository]
    RR -->|git pull| LR
```

### Bloque B (20 min): Flujo minimo diario

- `git status` para leer contexto antes de actuar.
  Como explicarlo: establece la regla "primero mirar, luego cambiar" para evitar errores.
- `git add` selectivo para construir commits atomicos.
  Como explicarlo: agrega solo archivos relacionados y justifica por que mejora trazabilidad.
- `git commit` con mensaje descriptivo y orientado a cambio.
  Como explicarlo: usa formato de mensaje que indique que se hizo y para que.

Secuencia base:

```bash
git status
git add src/auth/login.js
git commit -m "feat(auth): validar formato de email"
```

### Bloque C (20 min): Historial y trazabilidad

- Usar `git log --oneline --graph` para entender historia del repo.
  Como explicarlo: interpreta ramas y merges en el grafo para reconstruir decisiones del equipo.
- Relacionar cada commit con una intencion concreta.
  Como explicarlo: vincula commit con issue o tarea para mantener contexto de negocio.
- Diferenciar commit de trabajo vs commit de entrega.
  Como explicarlo: muestra que no todo avance parcial debe publicarse sin limpiar.

### Bloque D (20 min): Remoto y colaboracion basica

- `git push` y `git pull` como sincronizacion entre local y remoto.
  Como explicarlo: usa dos clones para visualizar ida y vuelta de cambios entre repositorios.
- Caso comun: rechazo en push por cambios remotos.
  Como explicarlo: provoca rechazo intencional y analiza el mensaje antes de resolver.
- Estrategia segura: `git pull --rebase` (si el equipo lo permite) o merge clasico.
  Como explicarlo: compara ambos enfoques y decide segun politica del equipo.

### Bloque E (15 min): Conflictos iniciales

- Identificar marcas de conflicto en archivo.
  Como explicarlo: localiza marcadores y separa claramente ambas versiones antes de editar.
- Resolver manualmente y completar el ciclo con commit.
  Como explicarlo: valida resultado final, ejecuta pruebas y registra resolucion con mensaje claro.

## 4. Actividades practicas para la clase

### Actividad 1 (parejas, 12 min)

Crear 3 commits atomicos sobre un mini proyecto:

- `feat`: nueva funcionalidad pequena.
- `fix`: corregir bug puntual.
- `docs`: actualizar README.

### Actividad 2 (parejas, 10 min)

Simular conflicto en el mismo archivo entre dos ramas y resolverlo.

### Actividad 3 (individual, 8 min)

Reescribir mensajes de commit pobres a mensajes profesionales.

## 5. Preguntas de comprobacion rapida

- Que diferencia hay entre `git add .` y `git add archivo_especifico`?
- Que riesgo tiene crear commits gigantes con multiples cambios no relacionados?
- Cuando un `push` falla por divergir el remoto, cual es el siguiente paso correcto?
- Por que `git status` deberia ejecutarse antes de casi cualquier accion?

## 6. Errores frecuentes y como corregirlos

- Error: commitear archivos temporales o secretos.
  Correccion: usar `.gitignore` y revisar staging antes de commitear.
- Error: mensajes de commit vagos como "cambios".
  Correccion: usar formato con intencion (`feat`, `fix`, `refactor`, `docs`).
- Error: mezclar cambios de multiples temas en un solo commit.
  Correccion: hacer commits pequenos por unidad funcional.

## 7. Cierre para la sesion

- Mensaje clave: Git no solo guarda codigo, documenta decisiones tecnicas.
- Resultado esperado: historial legible y colaboracion mas segura.
- Tarea sugerida: crear una rama personal y entregar 5 commits atomicos en un ejercicio guiado.
