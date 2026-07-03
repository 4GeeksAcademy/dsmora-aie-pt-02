# Guia Docente Completa: Class 20 - Context Engineering Operativo (Prompts, Reglas y Memory Bank)

Clase online para 60-75 minutos.
Documento para profesor: incluye guion literal, comandos exactos y prompts completos para demos en vivo.

## 1) Objetivo de la clase

Al finalizar, el estudiante podra:

- Diagnosticar por que un prompt falla: vaguedad, ruido o falta de contexto.
- Diseñar prompts con 3 capas: contexto del proyecto, de la tarea y de salida.
- Configurar reglas de codificacion AI con alcance correcto (usuario vs proyecto).
- Crear un memory-bank util para colaboracion persistente con IA.
- Convertir pedidos imperativos en planes declarativos de implementacion.

## 2) Agenda sugerida (60-75 min)

Ruta base de 65 minutos:

- Apertura y mapa mental: 5 min
- Bloque A - Prompting profesional y eficiencia de tokens: 12 min
- Bloque B - Reglas AI y scopes (user/project): 15 min
- Bloque C - Memory bank minimo viable: 14 min
- Bloque D - Plan dinamico + iteracion con IA: 14 min
- Cierre + preguntas de chequeo: 5 min

Si tienes 75 min:

- Agrega 10 min de laboratorio adicional en Bloque D (segunda iteracion completa).

Si tienes 60 min:

- Recorta 5 min del Bloque C y 5 min del Bloque D, dejando la segunda iteracion como tarea.

## 3) Preparacion docente (antes de clase)

Checklist tecnico:

- VS Code abierto en la raiz del proyecto.
- Terminal funcional con `bash`.
- Un asistente AI disponible (Copilot Chat o equivalente).
- Permisos de escritura en la carpeta de trabajo del taller.

Comandos de verificacion previa:

```bash
pwd
ls -la
code --version
```

## 4) Guion docente detallado (con texto literal)

## Apertura (5 min)

Que decir (literal):

"Hoy no vamos a aprender a hablar mas con la IA; vamos a aprender a hablar mejor. La diferencia esta en el contexto: que informacion damos, en que orden y con que precision."

"Si mejoramos contexto, mejoramos calidad, reducimos retrabajo y evitamos respuestas aleatorias."

## Bloque A - Prompting profesional y eficiencia de tokens (12 min)

### A1. Concepto rapido (4 min)

Que decir (literal):

"Tres fallos explican casi todas las malas salidas: vaguedad, ruido y falta de contexto. Nuestro objetivo es aumentar senal y bajar ruido."

"Un prompt profesional separa: proyecto, tarea y salida esperada."

### A2. Demo guiada: de prompt vago a prompt estructurado (4 min)

Ejecuta:

```bash
mkdir -p class_20/workshop
cat > class_20/workshop/prompt_vago.txt << 'EOF'
Haz un login bonito para mi app.
EOF

cat > class_20/workshop/prompt_estructurado.md << 'EOF'
## Contexto del Proyecto
- React 18 + TypeScript + Tailwind CSS v3
- Existe src/components/LoginForm.tsx
- Convencion: componentes funcionales con hooks

## Contexto de la Tarea
- Implementar formulario de login en LoginForm.tsx
- Campos: email y password
- Validar email requerido y password minimo 8 caracteres
- No agregar librerias externas

## Contexto de la Salida
- Entregar solo codigo TypeScript del componente
- Mantener estilo con clases Tailwind
- Incluir manejo de errores de validacion en UI
EOF
```

Que decir (literal):

"Mismo objetivo, dos resultados distintos. El primero obliga a adivinar; el segundo reduce ambiguedad y define calidad."

### A3. Mini practica guiada (4 min)

Prompt exacto sugerido:

```text
Tengo dos prompts para la misma tarea (uno vago y uno estructurado). Evalualos con una tabla de 3 filas: Vaguedad, Ruido, Falta de contexto. Para cada fila asigna puntaje de 1 a 5 y propone una mejora concreta.
```

## Bloque B - Reglas AI y scopes user/project (15 min)

### B1. Concepto y riesgos (5 min)

Que decir (literal):

"Las reglas de codificacion AI son contexto persistente. Si todo lo pones en prompt, repites trabajo. Si todo lo pones en reglas globales, rompes flexibilidad."

"Scope de usuario para preferencias personales. Scope de proyecto para acuerdos del equipo."

Riesgos a enfatizar en vivo:

- Regla vaga: produce comportamiento impredecible.
- Regla demasiado global: impone preferencias personales a todo el repo.
- Globs superpuestos: conflicto de instrucciones.

### B2. Ejemplo practico (6 min)

Ejecuta:

```bash
mkdir -p class_20/workshop/rules
cat > class_20/workshop/rules/user-regex-comments.md << 'EOF'
---
title: "Regex con comentarios explicativos"
description: "Cuando propongas regex, explica cada parte de forma breve."
scope: user
alwaysApply: true
---

Si generas un patron regex, agrega una explicacion corta linea por linea.
EOF

cat > class_20/workshop/rules/project-react-components.md << 'EOF'
---
title: "Estandar de componentes React"
description: "En componentes de React usar TypeScript estricto, props tipadas y sin estilos inline."
scope: project
globs:
  - "src/components/**/*.tsx"
alwaysApply: false
---

Para archivos que coincidan con el glob, preferir componentes funcionales y props tipadas.
EOF

ls -la class_20/workshop/rules
```

Que decir (literal):

"Acabamos de separar preferencia personal y estandar de equipo. Esta separacion evita guerras de estilo y mejora consistencia."

### B3. Validacion (4 min)

Checklist:

- Cada regla tiene un solo objetivo claro.
- La descripcion es especifica y comprobable.
- El scope corresponde al impacto real de la regla.
- Los globs apuntan solo a los archivos necesarios.

Prompt exacto sugerido:

```text
Revisa estas dos reglas y detecta 3 problemas potenciales: ambiguedad, alcance incorrecto o glob conflictivo. Devuelve una version corregida de cada regla y explica en una frase por que cambiaste cada campo.
```

## Bloque C - Memory bank minimo viable (14 min)

### C1. Concepto (4 min)

Que decir (literal):

"Sin memoria, la IA empieza de cero en cada sesion. Con memory bank, mantenemos decisiones y contexto vivo sin reexplicar todo."

"No queremos documentos largos; queremos contexto recuperable."

### C2. Demo guiada (6 min)

Ejecuta:

```bash
mkdir -p class_20/workshop/memory-bank
cat > class_20/workshop/memory-bank/product-context.md << 'EOF'
# Product Context
- Producto: TaskFlow Lite
- Usuario objetivo: freelancers con multiples proyectos
- Objetivo: priorizar tareas y deadlines sin friccion
- Stack: React + TypeScript + Tailwind + FastAPI
EOF

cat > class_20/workshop/memory-bank/conventions.md << 'EOF'
# Conventions
- TypeScript strict habilitado
- Componentes funcionales con hooks
- Sin estilos inline; usar Tailwind
- Nombres de variables descriptivos
EOF

cat > class_20/workshop/memory-bank/implementation-plan.md << 'EOF'
# Implementation Plan
- [ ] Crear formulario de login
- [ ] Validar email/password en cliente
- [ ] Mostrar errores de validacion en UI
- [ ] Agregar prueba basica del componente
EOF

find class_20/workshop/memory-bank -maxdepth 1 -type f | sort
```

Que decir (literal):

"Esto ya permite continuidad entre sesiones: producto, convenciones y plan en archivos separados y pequenos."

### C3. Mini practica (4 min)

Prompt exacto sugerido:

```text
Con base en estos tres archivos de memory-bank, propon 5 preguntas de aclaracion que una IA deberia hacer antes de implementar login, y luego actualiza implementation-plan.md con dos riesgos tecnicos y su mitigacion.
```

## Bloque D - Plan dinamico e iteracion con IA (14 min)

### D1. Cambio de requisito en vivo (4 min)

Que decir (literal):

"Ahora simulamos vida real: cambia el requisito y el plan no se borra, se versiona. Lo obsoleto se marca y lo nuevo se agrega."

Ejecuta:

```bash
cat > class_20/workshop/memory-bank/implementation-plan.md << 'EOF'
# Implementation Plan
- [x] Definir alcance de autenticacion
- [ ] ~~Login con password tradicional~~ (obsoleto por cambio de producto)
- [ ] Login con magic link
- [ ] Rate limiting para solicitud de enlaces
- [ ] Telemetria de conversion login
EOF

cat class_20/workshop/memory-bank/implementation-plan.md
```

### D2. Prompt de ejecucion declarativa (6 min)

Prompt exacto sugerido:

```text
Actua como engineering assistant y usa exclusivamente el contexto de memory-bank.
Objetivo: proponer la implementacion de login con magic link para React + FastAPI.
Formato de salida:
1) Supuestos
2) Plan tecnico en 6 pasos maximo
3) Riesgos y mitigaciones
4) Criterios de aceptacion verificables
No des codigo aun.
```

Que decir (literal):

"Primero pedimos plan, luego codigo. Separar plan de implementacion reduce errores y evita cambios impulsivos."

### D3. Segunda iteracion (opcional si hay 75 min) (4 min)

Prompt exacto sugerido:

```text
Con el plan anterior, genera solo los archivos que cambiarias y explica por que cada cambio respeta conventions.md. Si falta informacion, pregunta antes de escribir codigo.
```

## 5) Cierre (5 min)

Que decir (literal):

"Lo que mejora resultados no es pedir mas fuerte, es dar mejor contexto."

"Si aplican 3 capas + reglas claras + memory-bank minimo, la IA deja de improvisar y empieza a colaborar."

Checklist final en vivo:

```bash
tree class_20/workshop -a
echo "Class 20 checklist completed"
```

## 6) Preguntas de chequeo rapidas

- Cual es la diferencia operativa entre ruido y contexto util?
- Cuando una regla debe ir en scope `user` y no en `project`?
- Que archivo del memory-bank cambiarias primero si cambia el objetivo del producto?
- Por que conviene pedir plan antes de pedir codigo?
- Que indicador te dice que tu prompt sigue siendo demasiado vago?

## 7) Plan de contingencia

Si falla la demo principal (asistente AI no responde):

```bash
echo "Fallback: analisis manual de prompts"
cat class_20/workshop/prompt_vago.txt
cat class_20/workshop/prompt_estructurado.md
```

Si falla la practica de reglas:

```bash
echo "Fallback: usar plantilla minima de regla"
cat > class_20/workshop/rules/template-rule.md << 'EOF'
---
title: "Template rule"
description: "Regla de ejemplo con objetivo unico"
scope: project
alwaysApply: false
---

Instruccion concreta y medible.
EOF
```

Si el tiempo se acorta a 60 min:

- Saltar D3 completo.
- Hacer D2 como demostracion del profesor y dejar la implementacion para tarea.
- Cerrar con 3 preguntas de chequeo en lugar de 5.
