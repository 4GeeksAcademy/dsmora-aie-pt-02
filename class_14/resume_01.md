# Guia Docente: Class 14 - Fundamentos React/Next y Depuracion Frontend

Este resumen integra los JSON de class_14 para una clase online de 60 minutos maximo.
El foco es consolidar props, hooks y renderizado, y sumar un metodo de depuracion
basado en evidencia para alumnos en etapa de aprendizaje.

## 1. Objetivos de aprendizaje

Al finalizar la clase, el estudiante deberia poder:

- Explicar como fluye la informacion con props y children.
  Como explicarlo: pasar datos de un componente padre a uno hijo con ejemplos reales.
- Entender que resuelven los hooks y cuando usar useState/useEffect.
  Como explicarlo: mostrar un contador y una carga de datos simple.
- Diferenciar CSR y SSR a nivel inicial.
  Como explicarlo: escoger estrategia segun interactividad y SEO.
- Aplicar modularizacion basica en un proyecto React/Next.
  Como explicarlo: separar componente, hook y utilidad en archivos distintos.
- Depurar errores usando evidencia en DevTools.
  Como explicarlo: elegir panel correcto segun tipo de error (Elementos, Consola, Red, React DevTools).

## 2. Conceptos clave explicados en palabras simples

- Props: parametros de entrada para personalizar componentes.
- Children: contenido JSX que se inserta dentro de un componente contenedor.
- Hook: funcion especial que agrega estado o efectos a componentes funcionales.
- Renderizado CSR/SSR: donde se genera la UI, cliente o servidor.
- Evidencia sobre suposicion: primero observar datos del error, luego corregir.

## 3. Guion sugerido para clase online (60 minutos)

### Bloque A (12 min): Props y children

- Flujo de datos de padre a hijo.
- Ejemplo de componente contenedor usando children.

### Bloque B (12 min): Hooks esenciales

- useState para estado local.
- useEffect para efectos controlados en casos simples.

### Bloque C (10 min): Renderizado y modularizacion

- Diferencia basica entre CSR y SSR.
- Estructura minima de archivos para evitar monolitos.

### Bloque D (8 min): Depuracion por evidencia

- Identificar categoria del error.
- Elegir panel correcto de DevTools antes de cambiar codigo.

### Bloque E (18 min): Mini ejercicio final (maximo 20 min)

- Objetivo: construir un componente de lista interactiva y depurarlo.
- Requisitos:
  - Componente TaskList con props initialTasks.
  - Input + boton para agregar una tarea.
  - Estado local con useState.
  - Simular un bug pequeno (por ejemplo, no agregar tareas vacias) y resolverlo con Consola.
- Criterio de exito:
  - La lista renderiza tareas iniciales.
  - Se agregan nuevas tareas validas.
  - El estudiante explica que evidencia uso para encontrar el bug.

## 4. Ejemplos para mostrar en vivo

### Ejemplo 1: Props + children

```tsx
type PanelProps = {
  title: string;
  children: React.ReactNode;
};

export function Panel({ title, children }: PanelProps) {
  return (
    <section>
      <h2>{title}</h2>
      {children}
    </section>
  );
}
```

### Ejemplo 2: Hook de estado

```tsx
import { useState } from "react";

export function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(count + 1)}>Clicks: {count}</button>;
}
```

### Ejemplo 3: Elegir panel de depuracion

```text
No funciona un click -> Consola.
Layout roto -> Elementos.
Datos no cargan -> Red.
Props/estado inesperado en React -> React DevTools.
```

## 5. Errores frecuentes y correccion

- Error: prop drilling excesivo para datos simples.
  Correccion: reorganizar arbol de componentes y evaluar contexto mas adelante.
- Error: usar useEffect para todo.
  Correccion: usarlo solo cuando hay efecto secundario real.
- Error: editar codigo sin investigar el error.
  Correccion: recolectar evidencia en DevTools y formular hipotesis primero.
- Error: mezclar UI, estado y logica en un archivo gigante.
  Correccion: extraer modulos pequenos y con nombre claro.

## 6. Cierre para sesion

- Mensaje clave: construir bien y depurar bien son dos caras del mismo trabajo frontend.
- Resultado esperado: estudiante capaz de crear interactividad basica y resolver errores comunes con metodo.
- Siguiente paso: practicar con ejercicios pequenos de refactor + debugging guiado.
