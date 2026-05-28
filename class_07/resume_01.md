# Guia Docente: JavaScript and TypeScript Fundamentals

Este documento esta pensado como guia para impartir una clase online del modulo.
Se basa en el contenido extraido del curso y reorganizado para facilitar explicacion,
practica y evaluacion en vivo.

## 1. Objetivos de aprendizaje

Al finalizar la clase, el estudiante deberia poder:

- Explicar la diferencia entre JavaScript y TypeScript.
- Describir el flujo TypeScript -> transpilacion -> JavaScript.
- Escribir codigo basico con sintaxis correcta en TypeScript.
- Usar `console.log` para depurar de forma intencional.
- Declarar variables con tipos explicitos y aprovechar inferencia de tipos.
- Reconocer buenas practicas y anti patrones comunes al trabajar con variables.

## 2. Mapa del modulo (14 lecciones)

1. 0 De algoritmos a codigo
2. 1 Que es javascript
3. 1.1 Que es typescript y por que usarlo
4. 1.2 Como funciona typescript
5. 2 Entendiendo la sintaxis
6. 2.1 Reglas esenciales de typescript
7. 2.2 Depurando con console.log
8. 2.3 Configurando tu primer programa
9. 3 Variables en typescript
10. 3.1 Declarando variables con tipos
11. 3.2 Inferencia de tipos
12. 3.3 Mejores practicas para variables
13. 3.4 Anti patrones de variables
14. 5 Evaluacion fundamentos js y ts

## 3. Guion sugerido para clase online (90 minutos)

### Bloque A (15 min): Contexto y motivacion

- Conectar con la idea de algoritmo: instrucciones claras y secuenciales.
- Relacionar con problemas reales: errores en produccion por tipos incorrectos.
- Presentar objetivo: escribir codigo mas seguro sin perder velocidad.

### Bloque B (20 min): JavaScript vs TypeScript

- JavaScript: lenguaje de ejecucion en navegador y Node.js.
- TypeScript: superconjunto de JavaScript con sistema de tipos.
- Beneficio central: errores detectados antes de ejecutar.

Ejemplo para mostrar en vivo:

```ts
// JavaScript valida tarde (en runtime)
function greet(name) {
	return "Hola " + name.toUpperCase();
}

// TypeScript valida antes (en development)
function greetTs(name: string): string {
	return "Hola " + name.toUpperCase();
}
```

### Bloque C (20 min): Flujo de trabajo TypeScript

- Archivo fuente `.ts`.
- Compilacion/transpilacion a `.js`.
- Ejecucion del JavaScript generado.
- Rol del compilador: verificar tipos, no cambiar la logica del negocio.

Comando de referencia:

```bash
tsc app.ts
node app.js
```

### Bloque D (20 min): Sintaxis y depuracion con console.log

- Reglas basicas: declaraciones claras, nombres expresivos, bloques legibles.
- Depuracion: usar `console.log` con contexto, no solo valores sueltos.

Patron recomendado:

```ts
const total = 125;
console.log("[checkout] total calculado:", total);
```

### Bloque E (15 min): Variables, tipos, inferencia y calidad

- Tipado explicito cuando aporta claridad de dominio.
- Inferencia cuando el valor inicial es obvio.
- Buenas practicas: nombres semanticos, consistencia y alcance controlado.
- Anti patrones: nombres ambiguos, `any` innecesario, reasignaciones confusas.

## 4. Checklist didactico por tema

Antes de cerrar cada tema, validar:

- El estudiante puede explicarlo con sus palabras.
- Puede escribir un ejemplo minimo funcional.
- Puede detectar un error tipico y corregirlo.

## 5. Actividades practicas para la clase

### Actividad 1 (parejas, 10 min)

Refactorizar codigo JS a TS agregando tipos a parametros y retorno.

### Actividad 2 (individual, 10 min)

Detectar 3 anti patrones en un snippet y proponer mejora.

### Actividad 3 (cierre, 5 min)

Escribir una regla personal de estilo para variables y justificarla.

## 6. Preguntas de comprobacion rapida

- Que problema principal resuelve TypeScript frente a JavaScript puro?
- Cuando conviene declarar tipo explicito y cuando conviene inferencia?
- Que diferencia hay entre depurar con logs aleatorios y logs con contexto?
- Que riesgo trae abusar de `any` en un proyecto real?

## 7. Errores frecuentes y como corregirlos

- Error: usar nombres genericos como `data` o `temp` en todo.
	Correccion: usar nombres orientados a dominio (`userEmail`, `cartTotal`).
- Error: asumir que TypeScript evita todos los errores de ejecucion.
	Correccion: recordar que TS ayuda en tipos, no reemplaza pruebas.
- Error: llenar el codigo de logs sin estructura.
	Correccion: agregar prefijos por contexto y retirar logs al finalizar.

## 8. Cierre para la sesion

- Resumen de valor: TypeScript mejora mantenibilidad y confianza del equipo.
- Puente al siguiente modulo: control de flujo y toma de decisiones con tipos.
- Tarea sugerida: convertir un script JS corto a TS aplicando 3 buenas practicas.

## 9. Nota de calidad del scraping

El JSON contiene las 14 lecciones del indice del modulo.
Se detectaron algunos bloques de contenido repetidos entre lecciones consecutivas,
por lo que esta guia prioriza estructura docente y conceptos nucleares del programa.