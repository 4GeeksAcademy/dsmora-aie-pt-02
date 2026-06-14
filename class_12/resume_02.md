# Guia Docente: Visual to Spec - Translate Designs for AI

Este documento adapta el modulo de traduccion visual a especificacion.
El foco es convertir disenos o ideas UI en prompts tecnicos claros
que una IA pueda transformar en codigo frontend consistente.

## 1. Objetivos de aprendizaje

Al finalizar la clase, el estudiante deberia poder:

- Leer una interfaz visual con metodo, no por intuicion.
  Como explicarlo: aplicar lectura en tres pasos (estructura, componentes, detalle).
- Traducir una idea visual a especificacion textual accionable.
  Como explicarlo: describir layout, componentes, contenido y estados en orden.
- Construir prompts UI con rol, stack y restricciones claras.
  Como explicarlo: fijar tecnologia objetivo, reglas de estilo y criterios de aceptacion.
- Describir layout usando caja, filas, columnas y grillas.
  Como explicarlo: mapear la pantalla por secciones antes de hablar de colores.
- Evitar anti patrones que generan interfaces inconsistentes.
  Como explicarlo: detectar ambiguedades tipicas y reemplazarlas por lenguaje concreto.
- Usar vocabulario semantico y HTML correcto en la especificacion.
  Como explicarlo: nombrar componentes con etiquetas y roles reales de accesibilidad.

## 2. Mapa del modulo (17 lecciones)

1. 0 Bienvenido a convertir ideas visuales en especificaciones ai
2. 1 Entendiendo la mentalidad de vision a especificacion
3. 1.1 Leyendo un diseno con el metodo de tres pasos
4. 1.2 Traduciendo imagenes mentales a especificaciones
5. 1.3 Practica tu primera traduccion de especificacion
6. 2 Anatomia de un prompt ui
7. 2.1 Definiendo rol y pila en prompts
8. 2.2 Creando restricciones y contenido
9. 2.3 Construyendo prompts ui completos
10. 3 Marco mental del modelo de caja
11. 3.1 Describiendo filas columnas y cuadriculas
12. 3.2 Evitando anti patrones comunes
13. 3.3 Descomponiendo interfaces en especificaciones
14. 4 Usando html semantico en especificaciones
15. 4.1 Vocabulario de componentes y disposicion
16. 5 Desafio final de captura de pantalla a especificacion
17. 5.1 Prueba tus habilidades de especificacion visual

## 3. Guion sugerido para clase online (35 minutos)

### Bloque A (8 min): Mentalidad vision -> especificacion

- La IA no "adivina" diseno, ejecuta instrucciones.
  Como explicarlo: mostrar fallos cuando se describe una UI de forma abstracta.
- Metodo de tres pasos para leer diseno.
  Como explicarlo: 1) estructura macro, 2) componentes, 3) detalle de contenido y estilo.

### Bloque B (10 min): Anatomia de prompt UI

- Rol y stack tecnologico.
  Como explicarlo: incluir si se espera HTML/CSS, React o TypeScript y por que.
- Restricciones de contenido y layout.
  Como explicarlo: definir jerarquia, espaciados, responsive y comportamiento esperado.
- Prompt completo.
  Como explicarlo: construir una plantilla reutilizable para tareas de frontend.

### Bloque C (9 min): Modelo de caja y descomposicion

- Filas, columnas y grillas.
  Como explicarlo: dibujar primero bloques de alto nivel antes de microdetalles.
- Anti patrones comunes.
  Como explicarlo: evitar pedidos ambiguos como "que se vea moderno" sin criterios.
- Descomposicion de interfaz.
  Como explicarlo: dividir pantalla en header, hero, cards, footer con responsabilidades.

### Bloque D (8 min): Semantica y desafio final

- HTML semantico y vocabulario de componentes.
  Como explicarlo: usar main, section, article, nav, button segun funcion real.
- Desafio screenshot -> especificacion.
  Como explicarlo: convertir una referencia visual en prompt ejecutable y evaluable.

## 4. Errores frecuentes y correccion

- Error: describir solo estetica, sin estructura.
  Correccion: comenzar por layout y jerarquia antes de color/tipografia.
- Error: omitir stack o formato de salida.
  Correccion: exigir tecnologia, alcance y entregable exacto desde el inicio.
- Error: usar lenguaje subjetivo (bonito, pro).
  Correccion: reemplazar por reglas concretas de espaciado, tipografia y componentes.
- Error: no considerar semantica/accesibilidad.
  Correccion: incorporar etiquetas semanticas y roles en la especificacion.

## 5. Cierre para sesion

- Mensaje clave: traducir visual a especificacion reduce retrabajo y acelera desarrollo.
- Resultado esperado: estudiante capaz de generar prompts UI claros, medibles y reutilizables.
- Siguiente paso: implementar la UI con enfoque iterativo y fases de construccion (resume_03).
