# Clase 12 - Guia Unica de 60 Minutos (Solo Scroll)
## Comunicacion con IA + Visual to Spec + Iteracion Frontend

Usa este documento como teleprompter de clase.
No necesitas cambiar de archivo durante la explicacion.

## 0) Como usar esta guia

- Todo lo que esta en bloques de codigo lo puedes copiar y pegar.
- Todo lo que esta en "Di exactamente" es texto sugerido para decir en vivo.
- Todo lo que esta en "Check rapido" es validacion inmediata antes de avanzar.

## 1) Resultado de aprendizaje (lo que deben lograr en 60 min)

Al final, cada estudiante debe poder:
- escribir un prompt claro y verificable,
- convertir una referencia visual en una especificacion tecnica,
- construir una UI por fases sin retrabajo masivo,
- pedir mejoras con feedback tecnico medible.

## 2) Agenda cerrada (minuto a minuto)

- 00:00-15:00 Bloque A. De prompt vago a prompt profesional.
- 15:00-35:00 Bloque B. De visual a especificacion tecnica.
- 35:00-55:00 Bloque C. Implementacion iterativa en 3 fases.
- 55:00-60:00 Bloque D. Cierre, evaluacion y errores comunes.

---

## 3) Bloque A (00:00-15:00)
## De prompt vago a prompt profesional

### 3.1 Objetivo del bloque

Que entiendan que la calidad de salida depende de la calidad de instruccion.

### 3.2 Di exactamente (apertura, 60-90 segundos)

"Hoy no vamos a improvisar prompts. Vamos a usar una estructura minima que casi siempre mejora resultados: rol, objetivo, restricciones y salida esperada. Si falta una de estas piezas, aparecen ambiguedades y retrabajo."

### 3.3 Demostracion 1: prompt malo vs bueno (min 01-07)

Prompt vago (malo):

```text
Haz una landing moderna para un curso de IA.
```

Explica por que falla:
- no define stack,
- no define contenido minimo,
- no define restricciones,
- no define formato de salida.

Prompt estructurado (bueno):

```text
Actua como frontend developer senior.
Objetivo: crear una landing responsive para un curso de IA aplicada.
Stack: HTML + CSS vanilla.
Contenido minimo: header, hero con CTA, 3 cards de beneficios, footer.
Restricciones:
- usar HTML semantico
- mobile first
- sin librerias externas
- codigo en un solo bloque
Salida esperada:
- HTML y CSS completos
- explicacion breve (max 6 lineas)
```

### 3.4 Ejercicio guiado (min 07-12)

Pide al grupo reescribir este prompt defectuoso:

```text
Quiero una pagina bonita para vender mi curso. Haz algo profesional.
```

Version objetivo esperada (muestra despues de 2 minutos):

```text
Actua como desarrollador frontend.
Objetivo: crear una landing para vender un curso de automatizacion con IA.
Audiencia: principiantes que quieren mejorar productividad.
Stack: HTML + CSS vanilla.
Secciones requeridas: header, hero, beneficios (3 cards), testimonios (2), footer.
Restricciones: semantica HTML5, responsive mobile-first, contraste accesible, sin frameworks.
Salida: codigo completo y checklist de validacion responsive.
```

### 3.5 Check rapido antes de pasar al Bloque B (min 12-15)

Si alguna respuesta es "no", no avances:
- Tiene rol claro?
- Tiene objetivo concreto?
- Tiene restricciones tecnicas?
- Tiene formato de salida?

---

## 4) Bloque B (15:00-35:00)
## De referencia visual a especificacion tecnica

### 4.1 Objetivo del bloque

Que dejen de describir interfaces con adjetivos y empiecen a describirlas con estructura.

### 4.2 Di exactamente (entrada del bloque)

"La IA no construye intenciones; construye instrucciones. Si decimos 'elegante' o 'moderno' sin estructura, cada intento sale distinto. Ahora vamos a especificar layout, componentes, semantica y responsive."

### 4.3 Metodo de lectura visual en 3 pasos (min 15-20)

Paso 1. Estructura macro:
- header
- main
- footer

Paso 2. Componentes:
- hero
- cards
- CTA
- menu

Paso 3. Detalle funcional:
- jerarquia de titulos
- espaciado
- comportamiento responsive

### 4.4 Especificacion completa de ejemplo (min 20-30)

Copia y usa este ejemplo tal cual:

```md
# Especificacion UI - Landing Curso IA

## Layout
- Header horizontal con logo a la izquierda y navegacion a la derecha.
- Hero principal con titulo, subtitulo y boton CTA.
- Seccion de beneficios con 3 cards en grid.
- Footer con enlaces secundarios.

## Componentes
- Header: logo textual + menu (Inicio, Temario, Precio, Contacto).
- Hero: H1, parrafo corto, boton "Empezar ahora".
- Card beneficio: icono simple, titulo corto, texto de 2 lineas.
- Footer: enlaces y texto legal.

## Semantica HTML requerida
- usar: header, nav, main, section, article, footer, button.
- evitar: div sin rol cuando exista etiqueta semantica.

## Responsive
- Mobile (<768px): menu compacto, cards en 1 columna.
- Desktop (>=768px): nav horizontal, cards en 3 columnas.

## Criterios de aceptacion
- Se entiende la jerarquia visual en 5 segundos.
- CTA principal visible sin scroll en desktop.
- Contraste suficiente entre texto y fondo.
- Layout estable sin saltos raros en mobile.
```

### 4.5 Mini ejercicio de correccion (min 30-35)

Muestra esta especificacion mala:

```text
Haz una landing limpia y moderna para curso IA con buen estilo.
```

Pide convertirla a formato tecnico usando 5 campos obligatorios:
- layout,
- componentes,
- semantica,
- responsive,
- criterios de aceptacion.

---

## 5) Bloque C (35:00-55:00)
## Implementacion iterativa en 3 fases

### 5.1 Objetivo del bloque

Que vivan el proceso real: primero estructura, luego contenido, luego estilo.

### 5.2 Di exactamente (inicio del bloque)

"No buscamos perfeccion al primer intento. Buscamos control. Si separas estructura, contenido y estilo, detectas errores antes y corriges mas rapido."

### 5.3 Fase 1 - Estructura (min 35-41)

Pide este prompt:

```text
Genera solo la estructura HTML semantica de una landing con header, hero, 3 cards y footer.
No agregues estilos decorativos, solo estructura y clases base.
```

Salida minima esperada:

```html
<header>
  <nav>...</nav>
</header>
<main>
  <section class="hero">...</section>
  <section class="benefits">
    <article>...</article>
    <article>...</article>
    <article>...</article>
  </section>
</main>
<footer>...</footer>
```

Check rapido Fase 1:
- Hay semantica real?
- Se entiende el layout sin CSS final?

### 5.4 Fase 2 - Contenido (min 41-47)

Pide este prompt:

```text
Sobre la estructura anterior, agrega contenido real:
- H1 orientado a resultado
- subtitulo de valor
- CTA claro
- 3 beneficios concretos
Mantener la estructura sin redisenar.
```

Copy ejemplo para usar en vivo:

```text
H1: Aprende IA aplicada con proyectos reales.
Subtitulo: En 8 semanas dominaras prompts, automatizacion y frontend asistido por IA.
CTA: Quiero mi cupo.
Beneficio 1: Metodo paso a paso sin humo.
Beneficio 2: Proyectos listos para portafolio.
Beneficio 3: Feedback tecnico para mejorar rapido.
```

Check rapido Fase 2:
- El mensaje principal se entiende en 5 segundos?
- El CTA es unico y claro?

### 5.5 Fase 3 - Estilo (min 47-53)

Pide este prompt:

```text
Ahora aplica estilos CSS manteniendo la estructura y contenido.
Requisitos:
- mobile first
- tipografia legible
- contraste alto en CTA
- grid de 3 columnas en desktop y 1 en mobile
- hover visible en boton
```

Fragmento CSS de referencia para explicar:

```css
.cards {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
}

@media (min-width: 768px) {
  .cards {
    grid-template-columns: repeat(3, 1fr);
  }
}

.cta {
  background: #14532d;
  color: #ffffff;
  border-radius: 10px;
  padding: 12px 18px;
}

.cta:hover {
  background: #0f3f23;
}
```

Check rapido Fase 3:
- El texto se lee bien en mobile?
- El boton destaca sin romper armonia?
- El grid cambia correctamente en desktop?

### 5.6 Iteracion de feedback tecnico (min 53-55)

En vez de decir "mejoralo", pide esto:

```text
Ajustes solicitados:
1) Aumenta el padding vertical del hero a 40px.
2) Limita el ancho maximo a 1100px.
3) Sube contraste del CTA.
4) En mobile, deja gap de 16px entre cards.
No cambies estructura ni copy.
```

---

## 6) Bloque D (55:00-60:00)
## Cierre, evaluacion y consolidacion

### 6.1 Autoevaluacion final (si/no)

- El prompt inicial tuvo rol, objetivo, restricciones y salida?
- La especificacion incluyo layout, semantica y responsive?
- Se trabajo en 3 fases separadas?
- Se aplico feedback tecnico medible?

### 6.2 Rubrica rapida (10 puntos)

- 3 puntos: calidad del prompt.
- 3 puntos: calidad de la especificacion.
- 2 puntos: disciplina de iteracion por fases.
- 2 puntos: calidad del feedback tecnico.

### 6.3 Di exactamente (cierre de clase)

"La habilidad no es pedirle todo a la IA en un prompt gigante. La habilidad es dirigir: contexto claro, especificacion precisa, iteracion por fases y correcciones medibles. Ese proceso es lo que vuelve repetible la calidad."

---

## 7) FAQ rapido para contingencias en vivo

Si el grupo dice "la IA me devolvio algo raro":
- revisa si faltan restricciones,
- revisa si pidieron demasiadas cosas a la vez,
- divide en fase actual y fase siguiente.

Si el grupo se atrasa en Bloque C:
- recorta estilos avanzados,
- prioriza que terminen Fase 1 y Fase 2,
- deja Fase 3 como tarea guiada.

Si una salida rompe responsive:
- pedir "no cambies HTML, solo corrige CSS responsive",
- validar primero mobile,
- luego desktop.

## 8) Entregable minimo que deben mostrar al final

- Prompt final estructurado.
- Especificacion tecnica completa.
- Evidencia de 3 fases (estructura, contenido, estilo).
- Un ajuste aplicado por feedback tecnico.

## 9) Orden real del contenido segun los JSON

Los JSON de class_12 no imponen nombres de archivos spec concretos.
Lo que si marcan es este orden de trabajo:

1. Vision a especificacion.
2. Metodo de tres pasos.
3. Traducir imagen mental o screenshot a especificacion.
4. Construir prompt UI completo.
5. Describir layout con filas, columnas, rejillas y pilas.
6. Descomponer interfaces en especificaciones.
7. Usar HTML semantico y vocabulario de componentes.
8. Cerrar con desafio screenshot -> especificacion.

Traducido a artefactos de clase, el orden correcto no es por nombres fijos sino por contenido:

1. Estructura general.
2. Secciones principales.
3. Componente detallado.
4. Responsive.
5. Prompt UI final con Rol + Stack + Restricciones + Contenido.

## 10) Objetivo aplicado de esta clase (caso Biblioteca)

El resultado esperado de esta sesion es que el estudiante pueda ejecutar un flujo spec-first como el ejemplo de Panel de Administracion de Biblioteca:

1. Escribir primero SPECS.md antes de tocar HTML.
2. Definir stack y restricciones exactas: HTML + Tailwind por CDN + JS vanilla.
3. Especificar por seccion (Catalogo, Prestamos, Socios): componente, contenido y comportamiento.
4. Definir componentes reutilizables: sidebar, fila de tabla, dropdown, modal, badge, toggle dark mode.
5. Fijar criterios de aceptacion verificables para modales, dropdowns, sidebar activa y modo oscuro.
6. Implementar luego index.html como prototipo unico siguiendo la especificacion.

Guion breve para decir en clase:

"Primero escribimos la especificacion completa del panel en SPECS.md. Cuando esa especificacion esta clara y verificable, recien pasamos a index.html para implementar tablas, dropdowns, modales, sidebar persistente y toggle de modo oscuro con JavaScript vanilla."
