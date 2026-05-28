# Guia Docente: Data Types in TypeScript

Este documento convierte el modulo en guia para clase online.
El foco es consolidar tipos de datos y operadores para construir expresiones
seguras, predecibles y faciles de mantener.

## 1. Objetivos de aprendizaje

Al finalizar la clase, el estudiante deberia poder:

- Diferenciar tipos primitivos en TypeScript y su uso correcto.
- Explicar el impacto de `null` y `undefined` en la seguridad de tipos.
- Aplicar operadores aritmeticos, de asignacion, comparacion y logicos.
- Evitar coerciones peligrosas y validar tipos con `typeof`.
- Detectar errores comunes al combinar operadores.

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
- Diferencia entre valor y tipo.
- Casos de uso reales por tipo.

### Bloque B (20 min): Null, undefined y seguridad

- Significado semantico de ausencia de valor.
- Riesgos al no validar nulos.
- Buenas practicas con checks explicitos.

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
- Comparacion estricta vs no estricta.
- Logicos para combinar reglas.

### Bloque D (15 min): Coercion y typeof

- Coercion implicita: cuando ocurre y por que puede ser peligrosa.
- Conversion explicita: estrategia recomendada.
- `typeof` para decisiones seguras en runtime.

### Bloque E (15 min): Integracion practica

- Resolver ejercicio que combine tipos, operadores y validaciones.

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
