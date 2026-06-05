# Guia Docente: Objetos en TypeScript de Basico a Avanzado

Este documento adapta el tutorial objects_in_typescript para una clase online.
El foco es llevar al estudiante desde la sintaxis basica de objetos
hasta patrones seguros de acceso, metodos, composicion y validacion.

## 1. Objetivos de aprendizaje

Al finalizar la clase, el estudiante deberia poder:

- Crear interfaces y objetos literales con tipos correctos.
  Como explicarlo: mostrar errores de tipado comunes y como TypeScript los previene.
- Acceder a propiedades con notacion punto, corchetes y encadenamiento opcional.
  Como explicarlo: resolver casos con campos dinamicos y propiedades opcionales.
- Implementar metodos en objetos usando this de forma segura.
  Como explicarlo: construir objetos interactivos con estado y acciones.
- Modelar estructuras anidadas y arreglos de objetos.
  Como explicarlo: trabajar con catalogos y pedidos con multiples niveles.
- Entender mutabilidad, referencia y trampas de actualizacion.
  Como explicarlo: comparar paso por valor vs paso por referencia en ejemplos cortos.

## 2. Mapa del modulo (25 lecciones)

1. 0 Bienvenido a objetos typescript
2. 1 Interfaces vs objetos literales
3. 1.1 Creando y definiendo objetos
4. 1.2 Propiedades y valores
5. 1.3 Creando y usando objetos typescript con interfaces
6. 1.4 Construyendo tus primeros objetos typescript
7. 2 Notacion punto vs corchetes
8. 2.1 El operador de encadenamiento opcional
9. 2.2 Practica patrones de acceso a propiedades
10. 2.3 Errores comunes de acceso
11. 2.4 Practica acceso seguro a propiedades
12. 3 Entendiendo metodos en objetos
13. 3.1 Implementando metodos de objetos
14. 3.2 Practica construyendo objetos interactivos
15. 4 Trabajando con objetos anidados
16. 4.1 Arreglos de objetos
17. 4.2 Practica manejando datos complejos
18. 4.3 Patrones de composicion de objetos
19. 4.4 Practica trabajando con colecciones de productos
20. 5 Entendiendo la mutabilidad
21. 5.1 Paso por referencia vs valor
22. 5.2 Practica comportamiento de referencia
23. 5.3 Evitando trampas de mutacion
24. 6 Verificacion de conocimientos
25. 7 Tu viaje con objetos typescript

## 3. Guion sugerido para clase online (100 minutos)

### Bloque A (20 min): Interfaces y objetos literales

- Definir contratos claros con interfaces.
  Como explicarlo: levantar una interfaz de Task y validarla con ejemplos.
- Crear instancias tipadas y corregir errores.
  Como explicarlo: mostrar incompatibilidades reales de tipos.

### Bloque B (20 min): Acceso seguro a propiedades

- Punto vs corchetes.
  Como explicarlo: elegir por contexto fijo vs dinamico.
- Encadenamiento opcional y coalescencia nula.
  Como explicarlo: evitar fallos por undefined con patrones seguros.

### Bloque C (20 min): Metodos y estado

- Metodos con this.
  Como explicarlo: objeto carrito con add/remove/total.
- Diferencia entre leer datos y ejecutar comportamiento.
  Como explicarlo: propiedades para estado, metodos para reglas.

### Bloque D (20 min): Datos complejos

- Objetos anidados y arreglos.
  Como explicarlo: modelar pedido con cliente, items y direccion.
- Composicion de objetos.
  Como explicarlo: separar subestructuras reutilizables por dominio.

### Bloque E (20 min): Mutabilidad y cierre

- Referencia vs valor.
  Como explicarlo: demostrar efecto colateral al compartir objetos.
- Trampas de mutacion y defensas.
  Como explicarlo: usar copia superficial/profunda segun el caso.

## 4. Errores frecuentes y correccion

- Error: definir interfaces laxas o incompletas.
  Correccion: modelar campos obligatorios, opcionales y tipos exactos.
- Error: acceso directo a propiedades opcionales.
  Correccion: usar optional chaining y valores por defecto.
- Error: usar arrow function en metodos que dependen de this.
  Correccion: preferir sintaxis de metodo o function en objeto literal.
- Error: mutar objetos compartidos sin control.
  Correccion: aplicar copia defensiva antes de actualizar.

## 5. Cierre para sesion

- Mensaje clave: tipado + modelado correcto mejora seguridad y velocidad de desarrollo.
- Resultado esperado: estudiante capaz de construir objetos robustos en TypeScript.
- Siguiente paso: profundizar inmutabilidad y diseno de estado.
