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

## 6. Ejemplos guiados para clase

### Ejemplo A: Interface + objeto literal (Objetivo 1, Bloque A)

```ts
interface Task {
  id: number;
  title: string;
  done: boolean;
  dueDate?: string;
}

const homework: Task = {
  id: 1,
  title: "Repasar objetos",
  done: false,
};

// Error tipico para mostrar en vivo:
// const invalidTask: Task = { id: "1", title: "x", done: false };
```

Como usarlo en clase:
- Primero pedir al grupo que detecte por que el tipo de `id` debe ser `number`.
- Luego agregar `dueDate` para mostrar propiedad opcional.

### Ejemplo B: Acceso seguro a propiedades (Objetivo 2, Bloque B)

```ts
interface UserProfile {
  username: string;
  settings?: {
    language?: string;
  };
}

const user: UserProfile = { username: "ana" };

const language = user.settings?.language ?? "es";
console.log(language); // "es"
```

Como usarlo en clase:
- Comparar acceso inseguro (`user.settings.language`) vs acceso seguro (`?.`).
- Mostrar por que `??` evita valores `undefined` en UI.

### Ejemplo C: Metodos y this (Objetivo 3, Bloque C)

```ts
type CartItem = { name: string; price: number };

type CartWithMethods = {
  items: CartItem[];
  add(item: CartItem): void;
  total(): number;
};

// Caso 1: metodo abreviado (recomendado)
const cart1: CartWithMethods = {
  items: [],
  add(item: CartItem): void {
    this.items.push(item);
  },
  total(): number {
    return this.items.reduce((sum, item) => sum + item.price, 0);
  },
};

// Caso 2: key explicita + function (equivalente)
const cart2: CartWithMethods = {
  items: [],
  add: function (item: CartItem): void {
    this.items.push(item);
  },
  total: function (): number {
    return this.items.reduce((sum, item) => sum + item.price, 0);
  },
};

cart1.add({ name: "Teclado", price: 45 });
cart1.add({ name: "Mouse", price: 20 });
console.log(cart1.total()); // 65

cart2.add({ name: "Teclado", price: 45 });
cart2.add({ name: "Mouse", price: 20 });
console.log(cart2.total()); // 65

// Caso 3: arrow function en objeto (no recomendado si usas this)
const cart3 = {
  items: [] as CartItem[],
  add: (item: CartItem): void => {
    // this no apunta a cart3; en un modulo suele ser undefined
    // this.items.push(item); // provocaria error en runtime
    console.log("No usar arrow con this en metodos de objeto", item.name);
  },
};

cart3.add({ name: "Monitor", price: 120 });
```

Como usarlo en clase:
- Comparar en vivo caso 1 y caso 2: ambos permiten usar `this` del objeto.
- Explicar que en arrow `this` es lexico: se hereda del scope externo, no del objeto.
- Pedir una mejora: metodo `removeByName(name)` en `cart1`.

### Ejemplo D: Objeto anidado + arreglo (Objetivo 4, Bloque D)

```ts
interface Order {
  id: string;
  customer: {
    name: string;
    address: {
      city: string;
      zip: string;
    };
  };
  items: { sku: string; qty: number; price: number }[];
}

const order: Order = {
  id: "ORD-100",
  customer: {
    name: "Carlos",
    address: { city: "Madrid", zip: "28001" },
  },
  items: [
    { sku: "A1", qty: 2, price: 10 },
    { sku: "B5", qty: 1, price: 25 },
  ],
};

const total = order.items.reduce((sum, item) => sum + item.qty * item.price, 0);
console.log(total); // 45
```

Como usarlo en clase:
- Pedir al estudiante extraer una funcion `calculateTotal(order)`.
- Conectar con composicion: `customer`, `address`, `items` como submodelos.

### Ejemplo E: Referencia y mutacion (Objetivo 5, Bloque E)

```ts
const original = { theme: "light", notifications: true };
const alias = original;

alias.theme = "dark";
console.log(original.theme); // "dark" (efecto colateral)

const copy = { ...original };
copy.theme = "light";
console.log(original.theme); // "dark" (sin cambio lateral)
```

Como usarlo en clase:
- Mostrar en pantalla dos variables apuntando al mismo objeto.
- Cerrar con regla practica: "si compartes referencia, compartes cambios".

## 7. Formato sugerido de clase en vivo

1. Apertura (5 min)
- Activar contexto con una pregunta: "Que bug de objetos te ha pasado?".

2. Microdemo por bloque (40 min)
- Ejecutar ejemplos A y B con predicciones del grupo antes del resultado.

3. Practica guiada (25 min)
- Pares resuelven mejoras sobre ejemplos C y D.
- Checkpoint rapido: cada pareja explica una decision de tipado.

4. Reto final (20 min)
- Usar ejemplo E para corregir un bug por referencia compartida.

5. Cierre evaluable (10 min)
- Ticket de salida: 3 preguntas cortas (tipado, acceso seguro, mutacion).
- Mini-rubrica: correcto, parcialmente correcto, necesita refuerzo.
