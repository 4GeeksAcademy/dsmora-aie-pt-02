# Guia Docente: Introduction to Programming

Este documento convierte el modulo en una guia para clase online.
El enfoque es ayudar a estudiantes principiantes a pasar de instrucciones cotidianas
al pensamiento computacional basico con pseudocodigo, variables y control de flujo.

## 1. Objetivos de aprendizaje

Al finalizar la clase, el estudiante deberia poder:

- Explicar que es programar usando la idea de instrucciones precisas.
  Como explicarlo: compara una instruccion ambigua con otra precisa para evidenciar por que la maquina necesita detalle.
- Escribir pasos ordenados para resolver una tarea simple.
  Como explicarlo: pide ordenar una tarea cotidiana y validar si otra persona puede ejecutarla sin dudas.
- Convertir instrucciones cotidianas a pseudocodigo basico.
  Como explicarlo: traduce verbos de accion a pasos secuenciales con inicio y fin.
- Comprender el rol de variables y tipos de informacion.
  Como explicarlo: usa la metafora de cajas etiquetadas para guardar datos con significado.
- Aplicar decisiones con condicionales y repeticion con bucles.
  Como explicarlo: presenta situaciones de eleccion y repeticion para decidir si usar `if` o bucle.

## 2. Mapa del modulo (19 lecciones)

1. 0 Bienvenido a la programacion
2. 1 Que es la programacion
3. 1.1 Crea tu primera instruccion
4. 2 Que es el pseudocodigo
5. 2.1 Disena un plan simple con pseudocodigo
6. 2.2 Ayuda al robot a encontrar su camino
7. 3 Almacenando ideas con variables
8. 3.1 Nombra tu primera caja de almacenamiento
9. 3.2 Cambia lo que hay en tu caja
10. 4 Diferentes tipos de informacion
11. 4.1 Clasifica los elementos por tipo
12. 5 Tomando decisiones con condicionales
13. 5.1 Planifica un camino de eleccion
14. 5.2 Prueba tu plan de decision
15. 6 Repetir tareas con bucles
16. 6.1 Planifica una accion repetida
17. 6.2 Detener un bucle a tiempo
18. 7 Verifica tus bases
19. 7.1 Revisa tu viaje

## 3. Guion sugerido para clase online (90 minutos)

### Bloque A (15 min): Que es programar

- Presentar programacion como comunicacion precisa con una maquina.
  Como explicarlo: enfatiza que la computadora no infiere intenciones, solo ejecuta reglas exactas.
- Comparar instrucciones vagas vs instrucciones detalladas.
  Como explicarlo: ejecuta un mini reto donde una instruccion vaga falla y una detallada funciona.
- Conectar con ejemplos del dia a dia (recetas, mapas, pasos).
  Como explicarlo: reutiliza experiencias conocidas para bajar barrera de entrada conceptual.

### Bloque B (20 min): Pseudocodigo

- Definir pseudocodigo como puente entre idea y codigo real.
  Como explicarlo: muestra que permite pensar logica sin bloquearse por sintaxis.
- Practicar estructura secuencial con pasos claros.
  Como explicarlo: revisa si cada paso tiene accion concreta y orden verificable.
- Usar mini ejercicios de robot en grilla para reforzar orden.
  Como explicarlo: visualiza movimiento paso a paso para detectar errores de secuencia.

Ejemplo base:

```text
START
  MOVE RIGHT
  MOVE RIGHT
  MOVE DOWN
END
```

### Bloque C (20 min): Variables y tipos

- Explicar variable como caja con nombre y valor.
  Como explicarlo: cambia el valor de una misma variable para mostrar estado mutable.
- Enfatizar nombres descriptivos y consistencia.
  Como explicarlo: compara nombres genericos frente a nombres con contexto del problema.
- Diferenciar numero, texto y booleano con ejemplos simples.
  Como explicarlo: clasifica datos cotidianos y pregunta que operaciones permite cada tipo.

### Bloque D (20 min): Condicionales y bucles

- Mostrar como tomar decisiones con `if/else`.
  Como explicarlo: formula una regla de negocio y conviertela a condicion legible.
- Explicar repeticion con `for` o `while` segun contexto.
  Como explicarlo: decide el tipo de bucle segun si conoces o no la cantidad de iteraciones.
- Reforzar condiciones de salida para evitar bucles infinitos.
  Como explicarlo: valida siempre contador o criterio de corte antes de ejecutar.

### Bloque E (15 min): Integracion y cierre

- Resolver un problema corto que combine secuencia, variable y decision.
  Como explicarlo: separa la solucion en entrada, proceso y salida para ordenar la logica.
- Hacer repaso rapido de conceptos troncales del modulo.
  Como explicarlo: cierra con preguntas de verificacion para confirmar comprension minima.

## 4. Actividades practicas para la clase

### Actividad 1 (parejas, 10 min)

Describir en pseudocodigo como preparar una merienda en 8 pasos maximo.

### Actividad 2 (individual, 12 min)

Declarar 5 variables de una app escolar y elegir tipo correcto para cada una.

### Actividad 3 (parejas, 10 min)

Resolver un ejercicio con una condicion y un bucle corto, explicando la salida.

## 5. Preguntas de comprobacion rapida

- Por que una instruccion vaga genera errores en programacion?
- Que diferencia hay entre pseudocodigo y codigo ejecutable?
- Que hace que un nombre de variable sea bueno?
- Como decides entre usar condicional o bucle?

## 6. Errores frecuentes y como corregirlos

- Error: instrucciones ambiguas o incompletas.
  Correccion: dividir tareas en pasos pequenos y verificables.
- Error: nombres de variables genericos (`x`, `dato`, `tmp`).
  Correccion: usar nombres con contexto (`edadAlumno`, `estadoPago`).
- Error: bucles sin condicion de salida clara.
  Correccion: validar siempre contador o condicion de corte.

## 7. Cierre para la sesion

- Mensaje clave: programar es pensar con orden, precision y claridad.
- Resultado esperado: estudiante capaz de planear y expresar logica basica.
- Tarea sugerida: crear un pseudocodigo de una rutina diaria con variables y una decision.
