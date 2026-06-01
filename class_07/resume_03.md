# Guia Docente: Data Types in TypeScript

Este documento convierte el modulo en guia para clase online.
El foco es consolidar tipos de datos y operadores para construir expresiones
seguras, predecibles y faciles de mantener.

## 1. Objetivos de aprendizaje

Al finalizar la clase, el estudiante deberia poder:

- Diferenciar tipos primitivos en TypeScript y su uso correcto.
  Como explicarlo: compara datos reales del aula (edad, nombre, aprobado) y pregunta que tipo evita errores en cada caso.
- Explicar el impacto de `null` y `undefined` en la seguridad de tipos.
  Como explicarlo: muestra un fallo comun al acceder a propiedades vacias y luego corrige con validacion temprana.
- Aplicar operadores aritmeticos, de asignacion, comparacion y logicos.
  Como explicarlo: transforma reglas de negocio en expresiones (por ejemplo, aprobar si nota >= 60 y asistencia > 80).
- Evitar coerciones peligrosas y validar tipos con `typeof`.
  Como explicarlo: contrasta una suma incorrecta por coercion con una conversion explicita antes de operar.
- Detectar errores comunes al combinar operadores.
  Como explicarlo: analiza expresiones ambiguas en voz alta y reescribelas con parentesis para hacer la intencion clara.

## 2. Mapa del modulo (18 lecciones)

1. 0 Introduccion a los fundamentos de typescript
2. 1 Entendiendo los tipos de datos primitivos
3. 1.1 Trabajando con numeros y booleanos
4. 1.2 Cadenas y simbolos explicados
5. 1.3 Null undefined y seguridad de tipos
6. 2 Operadores aritmeticos en typescript
7. 2.1 Operadores de asignacion y atajos
8. 2.2 Practica de operaciones matematicas
9. 3 Operadores de comparacion tomando decisiones
10. 3.1 Operadores logicos y o no
11. 3.2 Combinando operadores efectivamente
12. 3.3 Errores comunes con operadores
13. 4 Identificando tipos de datos
14. 4.1 Conversion y coercion de tipos
15. 4.2 Trabajando con el operador typeof
16. 5 Desafio de tipos de datos y operadores
17. 5.1 Verificacion de conocimientos tipos y operadores
18. 6 Tu fundamento en datos de typescript

## 3. Guion sugerido para clase online (90 minutos)

### Bloque A (20 min): Tipos primitivos

- `number`, `string`, `boolean`, `symbol`.
  Como explicarlo: asigna un ejemplo cotidiano a cada tipo y valida si se puede operar sin conversion.
- Diferencia entre valor y tipo.
  Como explicarlo: separa "que dato tengo" (valor) de "que reglas aplica" (tipo) en una tabla rapida.
- Casos de uso reales por tipo.
  Como explicarlo: modela un formulario simple y decide el tipo correcto campo por campo.

### Bloque B (20 min): Null, undefined y seguridad

- Significado semantico de ausencia de valor.
  Como explicarlo: usa dos ejemplos, dato aun no cargado (`undefined`) y dato intencionalmente vacio (`null`).
- Riesgos al no validar nulos.
  Como explicarlo: reproduce un error de runtime y enseguida aplica guard clause para evitarlo.
- Buenas practicas con checks explicitos.
  Como explicarlo: estandariza validaciones con `=== null` o `=== undefined` antes de usar el dato.

Ejemplo:

```ts
function printName(name: string | null) {
  if (name === null) {
    console.log("sin nombre");
    return;
  }
  console.log(name.toUpperCase());
}
```

### Bloque C (20 min): Operadores

- Aritmeticos y asignacion abreviada.
  Como explicarlo: resuelve una cuenta paso a paso y luego muestra la version abreviada equivalente.
- Comparacion estricta vs no estricta.
  Como explicarlo: compara resultados de `==` y `===` con distintos tipos para evidenciar diferencias.
- Logicos para combinar reglas.
  Como explicarlo: construye reglas de acceso con `&&`, `||` y `!` usando un caso de login.

### Bloque D (15 min): Coercion y typeof

- Coercion implicita: cuando ocurre y por que puede ser peligrosa.
  Como explicarlo: muestra una operacion que parece valida pero cambia de significado por conversion automatica.
- Conversion explicita: estrategia recomendada.
  Como explicarlo: aplica `Number()` o `String()` antes de operar y verifica que el resultado sea predecible.
- `typeof` para decisiones seguras en runtime.
  Como explicarlo: ramifica flujo segun `typeof` para tratar entradas externas sin romper la ejecucion.

### Bloque E (15 min): Integracion practica

- Resolver ejercicio que combine tipos, operadores y validaciones.
  Como explicarlo: divide el ejercicio en tres pasos (tipar, operar, validar) y revisa errores en cada etapa.

## 4. Actividades practicas para la clase

### Actividad 1 (individual, 10 min)

Clasificar variables por tipo y justificar su eleccion.

### Actividad 2 (parejas, 12 min)

Corregir expresiones con comparaciones ambiguas (`==`) y coercion involuntaria.

### Actividad 3 (individual, 8 min)

Implementar validacion con `typeof` antes de operar con un dato externo.

## 5. Preguntas de comprobacion rapida

- Por que `===` suele ser preferible a `==`?
- Que diferencia conceptual existe entre `null` y `undefined`?
- Que riesgo aparece al sumar string y number sin control?
- En que casos `typeof` evita errores de ejecucion?

## 6. Errores frecuentes y como corregirlos

- Error: depender de coercion implicita sin darse cuenta.
  Correccion: convertir explicitamente tipos antes de operar.
- Error: comparar valores con `==` en logica sensible.
  Correccion: usar `===` y `!==` por defecto.
- Error: no contemplar `null/undefined` en entradas externas.
  Correccion: validar temprano y usar retornos anticipados.

## 7. Cierre para la sesion

- Mensaje clave: tipar bien y operar bien reduce bugs y acelera mantenimiento.
- Resultado esperado: expresiones confiables y decisiones logicas robustas.
- Tarea sugerida: crear un mini validador de formulario usando tipos y operadores en TypeScript.
