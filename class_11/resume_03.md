# Guia Docente Integrada: Objetos y Mutabilidad en TypeScript

Este resumen integra los contenidos de `resume_01.md` (Objetos en TypeScript) y `resume_02.md` (Mutabilidad en TypeScript) para impartir una clase completa, coherente y accionable.
El enfoque es que el estudiante no solo modele datos correctamente, sino que tambien los actualice sin introducir bugs por referencias compartidas.

## 1. Objetivo general de la clase

Que el estudiante pueda disenar objetos tipados, acceder y operar sobre sus propiedades, y aplicar estrategias de mutacion controlada e inmutabilidad para construir codigo mantenible.

## 2. Objetivos de aprendizaje integrados

Al finalizar la sesion, el estudiante deberia poder:

- Modelar datos con interfaces y objetos literales tipados.
  Como explicarlo: construir contratos claros y mostrar como TypeScript evita errores de forma anticipada.
- Acceder a propiedades de forma segura (punto, corchetes, optional chaining y nullish coalescing).
  Como explicarlo: comparar acceso directo inseguro vs patrones seguros en propiedades opcionales.
- Implementar metodos con `this` correctamente en objetos.
  Como explicarlo: diferenciar propiedades (estado) de metodos (comportamiento) en casos reales.
- Trabajar con objetos anidados y arreglos de objetos.
  Como explicarlo: modelar un dominio real (pedido, carrito, usuario) en multiples niveles.
- Distinguir paso por valor y paso por referencia.
  Como explicarlo: contrastar primitivas con objetos para explicar por que aparecen efectos colaterales.
- Aplicar copia defensiva segun profundidad (superficial vs por niveles).
  Como explicarlo: demostrar limites de spread y cuando copiar niveles internos.
- Actualizar colecciones de forma inmutable.
  Como explicarlo: usar transformaciones puras (`map`, spread) para estado predecible.

## 3. Mapa tematico unificado

1. Fundamentos de objetos tipados
2. Acceso seguro a propiedades
3. Metodos y uso de `this`
4. Modelado de datos complejos (anidamiento y colecciones)
5. Mutabilidad e inmutabilidad
6. Valor vs referencia
7. Trampas comunes de mutacion
8. Copia defensiva y actualizaciones inmutables
9. Verificacion y reto integrador

## 4. Guion sugerido para clase completa (120 minutos)

### Bloque A (20 min): Modelado base con objetos e interfaces

- Que se enseña: interfaces, objetos literales, propiedades obligatorias y opcionales.
- Como explicarlo: levantar una interfaz de `Task` y corregir errores de tipado en vivo.
- Resultado esperado: el estudiante entiende contrato de datos y tipado estructural.

### Bloque B (20 min): Acceso seguro y lectura de datos

- Que se enseña: notacion punto vs corchetes, `?.` y `??`.
- Como explicarlo: usar un objeto de perfil con ramas opcionales y resolver `undefined` sin romper flujo.
- Resultado esperado: el estudiante puede leer datos sin errores de acceso.

### Bloque C (20 min): Metodos, `this` y comportamiento

- Que se enseña: metodos en objetos, diferencia con arrow functions cuando depende de `this`.
- Como explicarlo: construir un carrito con `add`, `total` y discutir por que ciertas implementaciones fallan.
- Resultado esperado: el estudiante separa estado y logica de negocio correctamente.

### Bloque D (20 min): Objetos anidados y colecciones

- Que se enseña: estructuras profundas y arreglos de objetos.
- Como explicarlo: modelar un pedido (`customer`, `address`, `items`) y calcular total.
- Resultado esperado: el estudiante puede navegar y transformar datos complejos.

### Bloque E (20 min): Mutabilidad, referencias y copia defensiva

- Que se enseña: valor vs referencia, aliasing, copia superficial.
- Como explicarlo: comparar casos de primitives, objetos alias y spread en datos anidados.
- Resultado esperado: el estudiante identifica efectos colaterales antes de que ocurran.

### Bloque F (20 min): Patrones inmutables y cierre evaluable

- Que se enseña: actualizacion inmutable de arreglos/objetos y practicas de equipo.
- Como explicarlo: transformar una lista de tareas con `map` sin mutar el original.
- Resultado esperado: el estudiante aplica un patron seguro de actualizacion de estado.

## 5. Secuencia didactica recomendada (en vivo)

1. Apertura diagnostica (5 min)
- Pregunta disparadora: "Que bug te ha pasado por cambiar un objeto sin querer?"

2. Demostracion guiada (35 min)
- Ejemplos de modelado, acceso seguro y `this`.
- Antes de ejecutar, pedir prediccion para activar razonamiento.

3. Practica por parejas (30 min)
- Reto 1: convertir acceso inseguro a acceso seguro.
- Reto 2: refactorizar metodo que usa `this` de forma incorrecta.

4. Laboratorio de mutabilidad (30 min)
- Reproducir bug por referencia compartida.
- Corregir con copia por niveles y actualizacion inmutable.

5. Cierre evaluable (20 min)
- Ticket de salida con 3 preguntas: tipado, referencia, copia defensiva.
- Mini rubrica: correcto, parcialmente correcto, necesita refuerzo.

## 6. Errores frecuentes (integrados) y correccion

- Error: pensar que asignar un objeto crea una copia.
  Correccion: mostrar alias compartido y validar con logs comparativos.
- Error: usar spread en objeto anidado y asumir copia profunda.
  Correccion: copiar explicitamente cada nivel que se va a modificar.
- Error: acceso directo a propiedades opcionales.
  Correccion: aplicar `?.` y `??` para rutas no garantizadas.
- Error: usar arrow function para metodo que depende de `this`.
  Correccion: usar sintaxis de metodo o `function` dentro del objeto.
- Error: mutar parametros o estado compartido sin criterio.
  Correccion: definir convencion de inmutabilidad para datos compartidos.

## 7. Reto integrador final (15-20 min)

Escenario: mini sistema de pedidos.

- Parte 1: definir interfaces (`Customer`, `Address`, `OrderItem`, `Order`).
- Parte 2: implementar metodo `calculateTotal()`.
- Parte 3: actualizar un item (`qty`) sin mutar pedido original.
- Parte 4: leer `customer.address?.city ?? "Sin ciudad"`.

Criterios de logro:
- Tipado correcto sin `any`.
- Sin mutacion accidental del objeto original.
- Uso correcto de acceso seguro.
- Codigo legible con decisiones justificadas.

## 8. Mensajes clave para cerrar la clase

- Modelar bien objetos reduce errores desde el diseno.
- Entender referencia y copia evita bugs silenciosos de estado.
- Inmutabilidad no es moda: es una estrategia de mantenibilidad.
- TypeScript + buenas practicas de actualizacion = codigo mas predecible y facil de depurar.

## 9. Siguiente paso sugerido

Conectar estos conceptos con gestion de estado en frontend (React/Redux/Zustand) para que el estudiante vea su impacto directo en aplicaciones reales.
