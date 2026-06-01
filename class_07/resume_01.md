# Guia Docente: JavaScript and TypeScript Fundamentals

Este documento esta pensado como guia para impartir una clase online del modulo.
Se basa en el contenido extraido del curso y reorganizado para facilitar explicacion,
practica y evaluacion en vivo.

## 1. Objetivos de aprendizaje

Al finalizar la clase, el estudiante deberia poder:

- Explicar la diferencia entre JavaScript y TypeScript.
	Como explicarlo: compara un mismo ejemplo sin tipos y con tipos para visualizar cuando TypeScript previene errores.
- Describir el flujo TypeScript -> transpilacion -> JavaScript.
	Como explicarlo: muestra el recorrido archivo fuente, compilador y salida ejecutable, indicando que paso valida tipos.
- Escribir codigo basico con sintaxis correcta en TypeScript.
	Como explicarlo: construye snippets cortos y revisa en vivo errores de sintaxis frecuentes.
- Usar `console.log` para depurar de forma intencional.
	Como explicarlo: estandariza logs con contexto de modulo para que el alumno entienda que observar y por que.
- Declarar variables con tipos explicitos y aprovechar inferencia de tipos.
	Como explicarlo: decide explicitamente cuando el dominio requiere claridad adicional y cuando inferencia es suficiente.
- Reconocer buenas practicas y anti patrones comunes al trabajar con variables.
	Como explicarlo: contrasta pares "mala version vs buena version" con impacto en mantenibilidad.

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
	Como explicarlo: retoma un algoritmo cotidiano y traduce cada paso a una instruccion programable.
- Relacionar con problemas reales: errores en produccion por tipos incorrectos.
	Como explicarlo: presenta un bug realista por tipo inesperado y analiza su costo.
- Presentar objetivo: escribir codigo mas seguro sin perder velocidad.
	Como explicarlo: enfatiza que tipos tempranos reducen retrabajo sin frenar desarrollo.

### Bloque B (20 min): JavaScript vs TypeScript

- JavaScript: lenguaje de ejecucion en navegador y Node.js.
	Como explicarlo: ubica donde corre JS en cada entorno y que responsabilidades tiene.
- TypeScript: superconjunto de JavaScript con sistema de tipos.
	Como explicarlo: recalca que TS agrega chequeos, pero el codigo final sigue siendo JavaScript.
- Beneficio central: errores detectados antes de ejecutar.
	Como explicarlo: muestra un error atrapado por el compilador antes de llegar a runtime.

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
	Como explicarlo: crea un archivo minimo y resalta que aqui se define la intencion de tipos.
- Compilacion/transpilacion a `.js`.
	Como explicarlo: ejecuta compilacion y compara linea equivalente entre TS y JS generado.
- Ejecucion del JavaScript generado.
	Como explicarlo: corre el archivo resultante para evidenciar que quien ejecuta es JS.
- Rol del compilador: verificar tipos, no cambiar la logica del negocio.
	Como explicarlo: muestra que un cambio de tipos no altera reglas funcionales ya definidas.

Comando de referencia:

```bash
tsc app.ts
node app.js
```

### Bloque D (20 min): Sintaxis y depuracion con console.log

- Reglas basicas: declaraciones claras, nombres expresivos, bloques legibles.
	Como explicarlo: aplica una checklist rapida de legibilidad a un snippet antes de ejecutarlo.
- Depuracion: usar `console.log` con contexto, no solo valores sueltos.
	Como explicarlo: imprime etiqueta + variable para seguir el flujo y eliminar ruido de logs.

Patron recomendado:

```ts
const total = 125;
console.log("[checkout] total calculado:", total);
```

### Bloque E (15 min): Variables, tipos, inferencia y calidad

- Tipado explicito cuando aporta claridad de dominio.
	Como explicarlo: tipa explicitamente datos criticos (monto, estado, rol) para evitar ambiguedad.
- Inferencia cuando el valor inicial es obvio.
	Como explicarlo: deja que TS infiera en constantes claras y evita redundancia visual.
- Buenas practicas: nombres semanticos, consistencia y alcance controlado.
	Como explicarlo: revisa ejemplos de nombres y alcance para mejorar lectura en equipo.
- Anti patrones: nombres ambiguos, `any` innecesario, reasignaciones confusas.
	Como explicarlo: detecta anti patrones en un fragmento y refactoriza con criterio de mantenimiento.

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
