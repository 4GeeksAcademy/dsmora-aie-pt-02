# Guia Docente: Object Modeling Diagrams

Este documento adapta el modulo a una guia para clase online.
El foco es traducir ideas de dominio a diagramas de clases,
representar relaciones correctas y preparar una base para codificar.
Este resume corresponde a la segunda mitad de la misma clase integrada iniciada con resume_01.

## 1. Objetivos de aprendizaje

Al finalizar la clase, el estudiante deberia poder:

- Explicar para que sirve un diagrama de clases en el proceso de diseno.
  Como explicarlo: ubica el diagrama como puente entre requerimientos y codigo.
- Leer notacion UML basica para clases, propiedades y tipos.
  Como explicarlo: descomponer un diagrama existente en piezas minimas y su significado.
- Pasar de descripciones del mundo real a clases modeladas.
  Como explicarlo: extraer sustantivos como clases candidatas y validar su utilidad.
- Definir relaciones entre objetos (uno a uno, uno a muchos, muchos a muchos).
  Como explicarlo: usar ejemplos de negocio y justificar cardinalidad por regla concreta.
- Aplicar enfoque top-down para construir modelos completos y consistentes.
  Como explicarlo: iniciar en alto nivel y refinar iterativamente sin perder coherencia.
- Detectar patrones problematicos en diagramas (circularidad, sobreconexion).
  Como explicarlo: revisar sintomas de modelo "copo de nieve" y proponer simplificaciones.

## 2. Mapa del modulo (18 lecciones)

1. 0 Introduccion al modelado visual de objetos
2. 1 Que son los diagramas de clases
3. 1.1 Conceptos basicos de notacion uml
4. 1.2 Leyendo diagramas de clases existentes
5. 2 De mundo real a modelos visuales
6. 2.1 Definiendo clases y propiedades
7. 2.2 Agregando tipos de datos a propiedades
8. 2.3 Creando tu primer modelo de clase
9. 3 Entendiendo asociaciones de objetos
10. 3.1 Relaciones uno a uno y uno a muchos
11. 3.2 Relaciones muchos a muchos
12. 3.3 Modelando objetos conectados
13. 4 Comenzando general enfoque de arriba hacia abajo
14. 4.1 Evitando objetos copo de nieve y relaciones circulares
15. 4.2 Refinando tus modelos
16. 5 Construyendo un modelo de objetos completo
17. 5.1 Evaluacion de conocimientos de modelado de objetos
18. 6 De diagramas a codigo

## 3. Guion sugerido para clase integrada (Parte 2 de 2, 55 minutos)

### Bloque A (10 min): Arranque desde lo modelado en resume_01

- Reusar entidades definidas en la primera parte.
  Como explicarlo: tomar los objetos creados (producto, alumno, carrito) y convertirlos a clases candidatas.
- Definir alcance del diagrama de la sesion.
  Como explicarlo: elegir un dominio pequeno para completar de punta a punta en clase.

### Bloque B (10 min): Introduccion y lectura de diagramas

- Rol del modelado visual en desarrollo de software.
  Como explicarlo: mostrar como un diagrama reduce ambiguedad antes de programar.
- Elementos basicos de diagrama de clases.
  Como explicarlo: identificar clase, atributos y tipos con un ejemplo guiado.
- Lectura de diagramas existentes.
  Como explicarlo: interpretar relaciones y validar si reflejan reglas del dominio.

### Bloque C (10 min): De dominio real a clases

- Extraer clases desde requerimientos.
  Como explicarlo: seleccionar entidades clave y descartar conceptos irrelevantes.
- Definir propiedades y tipos.
  Como explicarlo: convertir reglas de negocio en atributos concretos y tipados.
- Construir primer modelo de clase.
  Como explicarlo: dibujar iterativamente y revisar claridad de nombres.

Ejemplo para mostrar en vivo:

```ts
class Curso {
  id: number;
  titulo: string;
  cupoMaximo: number;

  constructor(id: number, titulo: string, cupoMaximo: number) {
    this.id = id;
    this.titulo = titulo;
    this.cupoMaximo = cupoMaximo;
  }
}
```

### Bloque D (10 min): Asociaciones y cardinalidades

- Relaciones uno a uno y uno a muchos.
  Como explicarlo: usar casos de perfil-usuario y curso-estudiantes para fijar criterio.
- Relaciones muchos a muchos.
  Como explicarlo: introducir entidad intermedia cuando la relacion necesita datos propios.
- Objetos conectados con sentido de negocio.
  Como explicarlo: evitar enlaces por intuicion y exigir justificacion funcional.

### Bloque E (10 min): Enfoque top-down y refinamiento

- Diseñar primero macroestructura del sistema.
  Como explicarlo: establecer clases nucleo y luego completar detalles.
- Evitar copo de nieve y circularidad.
  Como explicarlo: reducir dependencias cruzadas y simplificar navegacion entre clases.
- Refinar modelo para implementacion.
  Como explicarlo: revisar consistencia de nombres, tipos y relaciones antes de codificar.

Ejemplo adicional para mostrar en vivo: muchos a muchos con entidad intermedia

```ts
class Estudiante {
  id: number;
  nombre: string;
  constructor(id: number, nombre: string) {
    this.id = id;
    this.nombre = nombre;
  }
}

class Curso {
  id: number;
  titulo: string;
  constructor(id: number, titulo: string) {
    this.id = id;
    this.titulo = titulo;
  }
}

class Inscripcion {
  estudianteId: number;
  cursoId: number;
  fecha: string;
  constructor(estudianteId: number, cursoId: number, fecha: string) {
    this.estudianteId = estudianteId;
    this.cursoId = cursoId;
    this.fecha = fecha;
  }
}
```

### Bloque F (5 min): Integracion y cierre

- Construir un modelo completo en equipo.
  Como explicarlo: dividir por subdominios y unificar criterios de notacion.
- Paso de diagrama a codigo.
  Como explicarlo: mapear clases y relaciones UML a estructuras TypeScript.

## 4. Actividades practicas para la clase

### Actividad 1 (individual, 8 min)

Leer un diagrama simple e identificar clases, atributos y dos relaciones.

### Actividad 2 (parejas, 12 min)

Modelar un dominio pequeno (biblioteca o ecommerce) con al menos 4 clases y cardinalidades justificadas.

### Actividad 3 (individual, 8 min)

Refinar un diagrama con sobreconexion, eliminando circularidades y mejorando claridad.

## 5. Preguntas de comprobacion rapida

- Que ventaja aporta un diagrama de clases antes de codificar?
- Como distingues uno a muchos de muchos a muchos?
- Que problema genera una relacion circular innecesaria?
- Que pasos sigues para pasar de diagrama a codigo TypeScript?

## 6. Errores frecuentes y como corregirlos

- Error: modelar clases sin limite de responsabilidad.
  Correccion: separar entidades por rol y comportamiento principal.
- Error: cardinalidades definidas por intuicion.
  Correccion: validarlas contra reglas reales del dominio.
- Error: diagrama con demasiadas conexiones cruzadas.
  Correccion: aplicar enfoque top-down y simplificar dependencias.
- Error: tipos de atributos ambiguos.
  Correccion: declarar tipos explicitos para facilitar implementacion posterior.

## 7. Cierre para la sesion

- Mensaje clave: un buen diagrama de clases acelera diseno, comunicacion y calidad de implementacion.
- Resultado esperado: estudiante capaz de leer, crear y refinar modelos visuales utiles.
- Tarea sugerida: convertir el diagrama final de esta segunda parte en codigo TypeScript reutilizando el trabajo del resume_01.

## 8. Nota de calidad del scraping

El scraping completo las 18 lecciones del modulo y genero el JSON final sin errores.
Se valido presencia de class_10/object_modeling_diagrams.json con contenido no vacio.
