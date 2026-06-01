# Guia Docente: Functions in JavaScript and TypeScript

Este documento adapta el modulo a una guia para clase online.
El foco es que el estudiante use funciones para organizar logica,
reducir duplicacion y escribir codigo mas mantenible.

## 1. Objetivos de aprendizaje

Al finalizar la clase, el estudiante deberia poder:

- Explicar por que una funcion mejora organizacion y reutilizacion de codigo.
  Como explicarlo: compara codigo duplicado vs codigo encapsulado en funcion y mide legibilidad.
- Declarar e invocar funciones en TypeScript con sintaxis correcta.
  Como explicarlo: construye ejemplos pequenos donde se vea nombre, parametros y retorno.
- Definir parametros y tipos de entrada segun el dominio del problema.
  Como explicarlo: parte de un caso real y decide que datos debe recibir cada funcion.
- Devolver valores con tipos de retorno claros y distinguirlos de efectos secundarios.
  Como explicarlo: contrasta una funcion que calcula y retorna con otra que solo imprime en consola.
- Diferenciar funciones y metodos al resolver tareas con strings y numeros.
  Como explicarlo: muestra cuando usar una funcion utilitaria y cuando un metodo de objeto.
- Aplicar principios DRY, responsabilidad unica y retorno temprano.
  Como explicarlo: refactoriza una funcion larga a piezas pequenas con guard clauses.

## 2. Mapa del modulo (25 lecciones)

1. 0 Bienvenido aprendiendo a organizar y reutilizar codigo
2. 1 Que es un bloque de codigo
3. 1.1 De bloques a funciones dando nombre a tu codigo
4. 1.2 Tu primera declaracion e invocacion de funcion
5. 2 Sintaxis de declaracion de funciones en typescript
6. 2.1 Nombrando funciones haciendo el codigo autoexplicativo
7. 2.2 Expresiones de funcion y funciones flecha
8. 2.3 Practica escribiendo funciones en diferentes estilos
9. 3 Entendiendo parametros dando datos a funciones
10. 3.1 Trabajando con multiples parametros
11. 3.2 Anotaciones de tipo para parametros en typescript
12. 3.3 Practica construyendo funciones que aceptan entrada
13. 4 Como las funciones retornan valores
14. 4.1 Anotaciones de tipo de retorno en typescript
15. 4.2 Funciones vs procedimientos retorno vs efectos secundarios
16. 4.3 Practica funciones que calculan y retornan
17. 5 Entendiendo metodos vs funciones
18. 5.1 Metodos de cadenas manipulando texto
19. 5.2 Metodos de numeros y funciones matematicas
20. 6 Principio dry y funciones puras
21. 6.1 Responsabilidad unica y patron de retorno temprano
22. 6.2 Antipatrones funciones dios y dependencias globales
23. 7 Desafio completo de practica de funciones
24. 7.1 Verificacion de conocimientos sobre funciones
25. 8 Tu viaje con las funciones continua

## 3. Guion sugerido para clase online (95 minutos)

### Bloque A (15 min): De bloques a funciones

- Reforzar el problema: codigo repetido y dificil de mantener.
  Como explicarlo: toma un bloque duplicado en dos lugares y muestra costo de cambiarlo.
- Definir funcion como unidad con nombre, entrada y salida.
  Como explicarlo: usa una plantilla mental simple (input -> proceso -> output).
- Mostrar primera declaracion e invocacion.
  Como explicarlo: ejecutar en vivo con un ejemplo minimo y salida verificable.

### Bloque B (20 min): Sintaxis y estilos de funcion

- Declaracion clasica de funcion en TypeScript.
  Como explicarlo: explicar orden nombre, parametros tipados y tipo de retorno.
- Expresiones de funcion y funciones flecha.
  Como explicarlo: comparar legibilidad y casos donde cada estilo aporta claridad.
- Criterio de nombres autoexplicativos.
  Como explicarlo: renombrar funciones ambiguas a nombres orientados a accion.

Ejemplo para mostrar en vivo:

```ts
function calcularSubtotal(precio: number, cantidad: number): number {
  return precio * cantidad;
}

const calcularImpuesto = (subtotal: number, tasa: number): number => {
  return subtotal * tasa;
};
```

### Bloque C (20 min): Parametros y tipos de entrada

- Parametros como contrato de entrada.
  Como explicarlo: listar que datos necesita cada funcion antes de codificar.
- Multiples parametros y orden semantico.
  Como explicarlo: ordenar parametros por significado para evitar errores de uso.
- Tipado de parametros en TypeScript.
  Como explicarlo: mostrar error temprano cuando se envia tipo incorrecto.

### Bloque D (20 min): Retorno, procedimientos y metodos

- Diferenciar retorno de efectos secundarios.
  Como explicarlo: comparar una funcion pura con un procedimiento que escribe en consola.
- Tipado de retorno para contratos claros.
  Como explicarlo: explicar por que el retorno esperado ayuda a componer funciones.
- Metodos de string/number vs funciones utilitarias.
  Como explicarlo: resolver el mismo problema con metodo nativo y con funcion propia.

Ejemplo corto:

```ts
function formatearNombre(nombre: string): string {
  return nombre.trim().toUpperCase();
}

function notificar(nombre: string): void {
  console.log("Usuario procesado:", nombre);
}
```

### Bloque E (20 min): Calidad de diseno con funciones

- DRY para eliminar duplicacion.
  Como explicarlo: extraer logica repetida en una sola funcion reutilizable.
- Responsabilidad unica por funcion.
  Como explicarlo: dividir una funcion grande en funciones pequenas enfocadas.
- Retorno temprano para reducir anidacion.
  Como explicarlo: usar guard clauses para manejar casos invalidos al inicio.
- Antipatrones: funcion dios y dependencias globales.
  Como explicarlo: identificar sintomas y refactorizar hacia parametros y retornos explicitos.

## 4. Actividades practicas para la clase

### Actividad 1 (parejas, 12 min)

Refactorizar un bloque duplicado de validacion en una funcion reutilizable.

### Actividad 2 (individual, 12 min)

Escribir 3 funciones tipadas: una con un parametro, otra con multiples parametros y otra que retorne `void`.

### Actividad 3 (parejas, 12 min)

Tomar una funcion con anidaciones y aplicar retorno temprano manteniendo el mismo comportamiento.

## 5. Preguntas de comprobacion rapida

- Que ganamos al extraer un bloque repetido a una funcion?
- Que diferencia practica hay entre una funcion que retorna y una que solo produce efectos secundarios?
- Como decides si usar metodo nativo o crear una funcion propia?
- Que riesgo tiene una funcion que hace demasiadas cosas?

## 6. Errores frecuentes y como corregirlos

- Error: nombres de funciones vagos (`doThing`, `processData`).
  Correccion: usar verbos y contexto del dominio (`calcularTotalCompra`, `validarCorreo`).
- Error: parametros sin tipo o tipo demasiado laxo.
  Correccion: declarar tipos explicitos y evitar contratos ambiguos.
- Error: mezclar calculo, validacion y salida en una sola funcion.
  Correccion: separar por responsabilidad y componer funciones pequenas.
- Error: depender de variables globales ocultas.
  Correccion: pasar datos por parametros y retornar resultado sin efectos colaterales innecesarios.

## 7. Cierre para la sesion

- Mensaje clave: buenas funciones hacen el codigo mas legible, reusable y testeable.
- Resultado esperado: estudiante capaz de disenar funciones claras con entradas y salidas bien definidas.
- Tarea sugerida: resolver un mini problema de negocio usando al menos 4 funciones pequenas y una composicion final.

## 8. Nota de calidad del scraping

El scraping completo las 25 lecciones del modulo y genero el JSON final sin errores.
Durante la ejecucion aparecieron pantallas intermedias de confirmacion ("Continue anyway"),
pero el contenido se proceso y guardo correctamente.
