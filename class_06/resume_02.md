# Guia Docente: Programming Fundamentals

Este documento adapta el modulo a una guia para clase online.
El objetivo es consolidar logica de programacion desde algoritmos y pseudocodigo
hasta operaciones, flujo de control, estado y funciones basicas.

## 1. Objetivos de aprendizaje

Al finalizar la clase, el estudiante deberia poder:

- Diseñar algoritmos claros para problemas cotidianos.
  Como explicarlo: convierte un problema real en pasos finitos y verifica que otro estudiante pueda reproducirlos.
- Traducir instrucciones a pseudocodigo estructurado.
  Como explicarlo: usa una plantilla simple (inicio, pasos, fin) para ordenar la solucion.
- Usar variables, tipos y operadores de forma correcta.
  Como explicarlo: relaciona tipo de dato con operador valido para evitar combinaciones incorrectas.
- Aplicar condicionales y bucles segun el comportamiento esperado.
  Como explicarlo: decide primero si el problema requiere decision unica o repeticion controlada.
- Entender alcance de variables y nociones iniciales de funciones.
  Como explicarlo: muestra con ejemplos donde una variable existe y cuando deja de estar disponible.

## 2. Mapa del modulo (26 lecciones)

1. 0 Bienvenido a la programacion
2. 1 Programas como instrucciones paso a paso
3. 1.1 Tu primer algoritmo haciendo un sandwich
4. 1.2 De instrucciones diarias a pseudocodigo
5. 1.3 Identificando casos limite en instrucciones
6. 2 Variables dando nombres a valores
7. 2.1 Practicando con variables y valores
8. 2.2 Tipos de datos numeros texto y verdadero falso
9. 2.3 Como los computadores recuerdan una mirada breve a la memoria
10. 3 Operaciones basicas matematicas y asignacion
11. 3.1 Comparando valores y creando logica
12. 3.2 Construyendo expresiones operadores en accion
13. 4 Flujo de control eligiendo diferentes caminos
14. 4.1 Declaraciones if else tomando decisiones
15. 4.2 Multiples condiciones else if y logica compleja
16. 4.3 Errores comunes al tomar decisiones
17. 5 Entendiendo el estado como cambian los valores
18. 5.1 Bucles for contando y repitiendo
19. 5.2 Bucles while repitiendo hasta terminar
20. 5.3 Previniendo bucles infinitos y estrategias de salida
21. 6 Alcance donde viven las variables
22. 6.1 Estructuras anidadas bucles dentro de condicionales
23. 6.2 Instrucciones reutilizables introduccion a funciones
24. 7 El patron ipo juntandolo todo
25. 7.1 Evaluacion de fundamentos de programacion
26. 8 De la logica al codigo que sigue

## 3. Guion sugerido para clase online (100 minutos)

### Bloque A (20 min): Algoritmos y pseudocodigo

- Reforzar secuencia logica y orden de pasos.
  Como explicarlo: intercambia dos pasos y analiza por que el resultado final cambia.
- Analizar por que cambiar el orden altera el resultado.
  Como explicarlo: usa un ejemplo corto de calculo donde el orden incorrecto rompe la solucion.
- Practicar conversion de tareas diarias a pseudocodigo.
  Como explicarlo: pide verbos concretos y elimina ambiguedades del lenguaje natural.

### Bloque B (20 min): Variables y tipos de datos

- Diferenciar nombre de variable y valor almacenado.
  Como explicarlo: reasigna varios valores a la misma variable para distinguir etiqueta y contenido.
- Introducir tipos basicos: entero, decimal, texto, booleano.
  Como explicarlo: clasifica datos de un caso real y justifica el tipo elegido.
- Explicar cambios de estado al reasignar valores.
  Como explicarlo: traza el valor antes/despues de cada operacion en una tabla.

### Bloque C (20 min): Operadores y expresiones

- Operadores aritmeticos y asignacion.
  Como explicarlo: resuelve una formula y luego reescribela con operadores de asignacion abreviada.
- Comparaciones y operadores logicos.
  Como explicarlo: construye condiciones con dos reglas y verifica tablas verdadero/falso.
- Construir expresiones para reglas concretas.
  Como explicarlo: parte de una regla verbal y transformala a expresion evaluable.

### Bloque D (20 min): Flujo de control y bucles

- `if/else` y `else if` para decisiones.
  Como explicarlo: ordena condiciones por prioridad para evitar ramas inalcanzables.
- `for` y `while` para repeticion.
  Como explicarlo: compara ambos sobre el mismo problema y discute cual aporta mas claridad.
- Prevenir bucles infinitos y reducir anidamiento.
  Como explicarlo: valida salida en cada iteracion y extrae bloques complejos a funciones.

### Bloque E (20 min): Alcance, funciones e integracion IPO

- Alcance de variables en bloques.
  Como explicarlo: dibuja limites de bloque para mostrar donde una variable es visible.
- Introduccion a funciones como unidades reutilizables.
  Como explicarlo: encapsula una logica repetida y demuestra reutilizacion con parametros.
- Patron IPO (input-process-output) para estructurar soluciones.
  Como explicarlo: obliga a identificar entrada, proceso y salida antes de codificar.

## 4. Actividades practicas para la clase

### Actividad 1 (parejas, 12 min)

Escribir un algoritmo para registrar una nota final con validacion de rango.

### Actividad 2 (individual, 12 min)

Crear variables de un escenario de tienda y calcular total con operadores.

### Actividad 3 (parejas, 15 min)

Resolver ejercicio con condicional y bucle; luego refactorizar a una funcion.

## 5. Preguntas de comprobacion rapida

- Que diferencia hay entre asignacion (`=`) y comparacion de igualdad?
- Como identificas que un problema requiere bucle en lugar de condicion unica?
- Que riesgo existe al no definir bien el alcance de una variable?
- Como ayuda el patron IPO a organizar una solucion?

## 6. Errores frecuentes y como corregirlos

- Error: mezclar tipos de datos sin control en operaciones.
  Correccion: definir tipos esperados y validar entradas.
- Error: condicionales muy complejas y dificiles de leer.
  Correccion: dividir reglas y usar funciones auxiliares.
- Error: reutilizar variables globales para todo.
  Correccion: limitar alcance y usar parametros/retornos en funciones.

## 7. Cierre para la sesion

- Mensaje clave: dominar fundamentos reduce errores en modulos avanzados.
- Resultado esperado: estudiante puede modelar, implementar y explicar logica basica.
- Tarea sugerida: construir un mini programa con IPO, una condicion y un bucle controlado.
