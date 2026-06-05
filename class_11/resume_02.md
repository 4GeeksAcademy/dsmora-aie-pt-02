# Guia Docente: Mutabilidad en TypeScript

Este documento adapta el tutorial mutability_in_typescript para clase online.
El foco es que el estudiante comprenda como se comporta la memoria
y pueda prevenir bugs de estado por referencias compartidas.

## 1. Objetivos de aprendizaje

Al finalizar la clase, el estudiante deberia poder:

- Distinguir datos mutables e inmutables en escenarios reales.
  Como explicarlo: usar analogias simples (cuaderno editable vs libro cerrado).
- Explicar paso por valor y paso por referencia.
  Como explicarlo: comparar primitivas y objetos en llamadas a funciones.
- Detectar trampas de mutacion en objetos y arreglos.
  Como explicarlo: reproducir bugs de aliasing y rastrear el origen.
- Aplicar copia defensiva segun profundidad de datos.
  Como explicarlo: decidir entre spread, map y estrategias mas profundas.
- Definir practicas de inmutabilidad para codigo mantenible.
  Como explicarlo: transformar actualizaciones mutables en patrones predecibles.

## 2. Mapa del modulo (17 lecciones)

1. 0 Bienvenido a la mutabilidad en typescript
2. 1 Entendiendo datos mutables vs inmutables
3. 1.1 La analogia del libro vs cuaderno
4. 1.2 Explorando la mutabilidad en la practica
5. 1.3 Por que la mutabilidad importa
6. 2 Entendiendo tipos por valor
7. 2.1 Entendiendo tipos por referencia
8. 2.2 Comparando comportamiento por valor y por referencia
9. 2.3 Trampas comunes con referencias
10. 3 Tipos primitivos y paso por valor
11. 3.1 Objetos y arreglos paso por referencia
12. 3.2 Estrategias de copia defensiva
13. 3.3 Antipatrones comunes de mutacion
14. 3.4 Mejores practicas de inmutabilidad
15. 4 Ejercicios desafio de mutacion
16. 4.1 Verificacion de conocimientos sobre mutaciones
17. 5 Dominando la mutacion y la memoria

## 3. Guion sugerido para clase online (85 minutos)

### Bloque A (15 min): Marco conceptual

- Mutabilidad vs inmutabilidad.
  Como explicarlo: definir impacto en depuracion y colaboracion de equipo.
- Por que importa.
  Como explicarlo: conectar con bugs reales de UI y estado compartido.

### Bloque B (20 min): Valor vs referencia

- Tipos primitivos por valor.
  Como explicarlo: mostrar copias independientes en operaciones simples.
- Objetos y arreglos por referencia.
  Como explicarlo: demostrar cambio lateral al modificar alias.

### Bloque C (20 min): Trampas y defensas

- Trampas comunes con referencias.
  Como explicarlo: reproducir 2 errores frecuentes y analizarlos paso a paso.
- Copia defensiva.
  Como explicarlo: elegir tecnica segun nivel de anidamiento.

### Bloque D (20 min): Buenas practicas

- Antipatrones de mutacion.
  Como explicarlo: detectar where/when muta estado sin control.
- Practicas de inmutabilidad.
  Como explicarlo: actualizar estado con transformaciones puras.

### Bloque E (10 min): Reto y cierre

- Ejercicio de mutacion controlada.
  Como explicarlo: pedir prediccion antes de ejecutar el codigo.
- Verificacion final.
  Como explicarlo: checklist rapido de decisiones correctas.

## 4. Errores frecuentes y correccion

- Error: asumir que asignar objeto crea copia.
  Correccion: explicar alias de referencia y validar con logs.
- Error: usar spread en objeto profundo y creer que todo queda aislado.
  Correccion: aclarar copia superficial y copiar niveles internos necesarios.
- Error: mutar parametros recibidos en funciones.
  Correccion: trabajar sobre copia o retornar nuevo objeto.
- Error: mezclar mutacion e inmutabilidad sin criterio.
  Correccion: definir una convencion de equipo para estado compartido.

## 5. Cierre para sesion

- Mensaje clave: dominar referencia y copia evita bugs silenciosos costosos.
- Resultado esperado: estudiante capaz de elegir estrategia segura de actualizacion.
- Siguiente paso: aplicar estos principios en gestion de estado de apps.
