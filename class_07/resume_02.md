# Guia Docente: Control Flow in TypeScript

Este documento adapta el modulo a una guia de clase online.
El objetivo es que el estudiante domine decisiones, bucles y control de ejecucion
con criterio de legibilidad y seguridad.

## 1. Objetivos de aprendizaje

Al finalizar la clase, el estudiante deberia poder:

- Construir logica condicional con `if`, `else if`, `else` y `switch`.
  Como explicarlo: parte de reglas reales (roles, notas, estados) y mapea cada una a la estructura condicional mas clara.
- Usar bucles `for` y `while` segun el problema.
  Como explicarlo: distingue entre "cantidad conocida" (`for`) y "condicion dinamica" (`while`) con ejemplos comparados.
- Aplicar `break` y `continue` de forma intencional.
  Como explicarlo: demuestra en consola como cambia la salida cuando cortas el ciclo o saltas una iteracion.
- Evitar codigo flecha y bucles infinitos.
  Como explicarlo: refactoriza un bloque anidado a guard clauses y verifica siempre condicion de salida.
- Resolver ejercicios combinando condicionales y bucles.
  Como explicarlo: guia la solucion por etapas: decision principal, repeticion y regla de corte.

## 2. Mapa del modulo (18 lecciones)

1. 0 Bienvenido al flujo de control en typescript
2. 1 Entendiendo las declaraciones if
3. 1.1 Practicando else y else if
4. 1.2 Dominando las declaraciones switch
5. 2 Introduccion a los bucles en typescript
6. 2.1 Trabajando con bucles for
7. 2.2 Explorando bucles while
8. 2.3 Variantes avanzadas de bucles
9. 3 Teoria de break y continue
10. 3.1 Practicando break y continue
11. 3.2 Bucles anidados en accion
12. 4 Evitando codigo flecha
13. 4.1 Previniendo bucles infinitos
14. 5 Practica de logica condicional
15. 5.1 Practica de ejecucion de bucles
16. 5.2 Ejercicios combinados de flujo de control
17. 5.3 Evaluacion de conocimientos de flujo de control
18. 6 Conclusion del curso y proximos pasos

## 3. Guion sugerido para clase online (90 minutos)

### Bloque A (20 min): Condicionales

- `if/else` para casos binarios.
  Como explicarlo: usa preguntas de si/no para que identifiquen rapidamente cuando esta estructura basta.
- `else if` para reglas multiples.
  Como explicarlo: ordena condiciones de mayor a menor prioridad y evalua por que ese orden importa.
- `switch` para decisiones por valor discreto.
  Como explicarlo: convierte un `else if` repetitivo a `switch` cuando comparas una sola variable.

Ejemplo:

```ts
const role: string = "student";

if (role === "admin") {
  console.log("acceso total");
} else if (role === "student") {
  console.log("acceso parcial");
} else {
  console.log("acceso limitado");
}
```

### Bloque B (20 min): Bucles

- `for`: cuando conoces rango o cantidad.
  Como explicarlo: recorre una lista de longitud conocida y muestra contador, inicio y fin.
- `while`: cuando depende de condicion dinamica.
  Como explicarlo: modela un proceso que termina al cumplirse una condicion externa.
- Diferenciar contador controlado vs condicion de salida.
  Como explicarlo: subraya que todo bucle necesita actualizacion de estado y criterio de corte verificable.

### Bloque C (20 min): Break, continue y anidamiento

- `break` para cortar flujo.
  Como explicarlo: simula una busqueda y detente al primer match para evidenciar ahorro de iteraciones.
- `continue` para saltar iteracion.
  Como explicarlo: filtra elementos invalidos sin detener todo el proceso.
- Riesgos de anidar demasiado y como simplificar.
  Como explicarlo: extrae reglas a funciones pequenas y compara legibilidad antes/despues.

### Bloque D (15 min): Calidad de control de flujo

- Reducir complejidad ciclomatica.
  Como explicarlo: mide ramas de decision y elimina condiciones redundantes para bajar complejidad.
- Evitar codigo flecha con retornos tempranos.
  Como explicarlo: reescribe una funcion anidada con guard clauses y valida que el resultado no cambie.
- Prevencion de bucles infinitos con condiciones verificables.
  Como explicarlo: agrega trazas de contador y criterio maximo de seguridad durante pruebas.

### Bloque E (15 min): Practica guiada y mini evaluacion

- Resolver un problema que combine validaciones y recorrido de datos.
  Como explicarlo: separa el problema en validacion de entrada, iteracion de datos y decision final.

## 4. Actividades practicas para la clase

### Actividad 1 (parejas, 12 min)

Convertir un `if/else if` largo en `switch` cuando corresponda.

### Actividad 2 (individual, 10 min)

Detectar y corregir un bucle infinito en un snippet dado.

### Actividad 3 (parejas, 10 min)

Refactorizar una funcion con codigo flecha usando guard clauses.

## 5. Preguntas de comprobacion rapida

- Cuando prefieres `switch` sobre `if/else if`?
- Que diferencia practica hay entre `break` y `continue`?
- Que pistas te alertan de un posible bucle infinito?
- Como disminuyes complejidad en un bloque condicional grande?

## 6. Errores frecuentes y como corregirlos

- Error: condiciones demasiado anidadas.
  Correccion: usar guard clauses y funciones auxiliares.
- Error: olvidar actualizar contador en `while`.
  Correccion: validar condicion de salida y mutaciones del estado.
- Error: usar `switch` sin `default`.
  Correccion: agregar caso por defecto para estados inesperados.

## 7. Cierre para la sesion

- Mensaje clave: controlar el flujo es controlar el comportamiento del programa.
- Resultado esperado: decisiones claras, bucles seguros y codigo legible.
- Tarea sugerida: resolver 3 ejercicios donde se combine `if`, `for`, `break` y `continue`.
