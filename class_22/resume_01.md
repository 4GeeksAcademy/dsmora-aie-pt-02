# Guia Docente Completa: Class 21 - Creacion de Agent Skills con SKILL.md

Clase online para 60-75 minutos.
Documento para profesor: incluye guion literal, comandos exactos y prompts completos para demos en vivo.

## 1) Objetivo de la clase

Al finalizar, el estudiante podra:

- Explicar que es una agent skill y cuando conviene crearla.
- Diseñar una skill con alcance claro (una tarea repetible, una salida verificable).
- Escribir un archivo `SKILL.md` con frontmatter valido e instrucciones accionables.
- Registrar la skill en la ruta correcta para su agente (proyecto o personal).
- Probar e iterar la skill usando un ciclo de calidad simple y repetible.

## 2) Agenda sugerida (60-75 min)

Ruta base de 66 minutos:

- Apertura y contexto: 5 min
- Bloque A - Que son las skills y como funcionan: 12 min
- Bloque B - Anatomia de `SKILL.md` + alcance correcto: 15 min
- Bloque C - Construccion guiada de una skill real: 17 min
- Bloque D - Testing, debugging y mejora iterativa: 12 min
- Cierre + chequeo + Q&A: 5 min

Si tienes 75 min:

- Agrega 9 min de laboratorio libre para que cada estudiante cree una segunda skill corta.

Si tienes 60 min:

- Recorta 6 min del Bloque C (deja solo una demo del profesor) y elimina el laboratorio libre.

## 3) Preparacion docente (antes de clase)

Checklist tecnico:

- VS Code abierto en la raiz del repo.
- Terminal bash funcional.
- Extension/agente de IA habilitado (Copilot o equivalente).
- Carpeta del repo con permisos de escritura.

Comandos de verificacion previa:

```bash
pwd
ls -la
rg --files .github/skills || true
```

## 4) Guion docente detallado (con texto literal)

## Apertura (5 min)

Que decir (literal):

"Hoy no vamos a pedirle cosas sueltas a la IA. Vamos a ensenarle una capacidad nueva, portable y reutilizable. Eso es una skill."

"La meta no es un prompt bonito; la meta es un comportamiento consistente que podamos probar, mejorar y compartir."

## Bloque A - Que son las skills y como funcionan (12 min)

### A1. Concepto rapido (4 min)

Que decir (literal):

"Una skill no es memoria ni una regla global. Una skill ensena procedimiento: pasos, decisiones y formato de salida para una tarea concreta."

"Si una tarea es repetible, medible y aparece seguido, es candidata ideal para skill."

### A2. Demo guiada (4 min)

Ejecuta:

```bash
mkdir -p class_21/workshop
cat > class_21/workshop/decision_matrix.md << 'EOF'
# Matriz rapida: Rule vs Memory vs Skill
- Rule: comportamiento siempre activo.
- Memory: hechos persistentes de proyecto.
- Skill: flujo de trabajo reusable para una tarea.
EOF
cat class_21/workshop/decision_matrix.md
```

Que decir (literal):

"Si necesito una preferencia permanente, uso regla. Si necesito recordar contexto, uso memoria. Si necesito ejecutar una receta, uso skill."

### A3. Mini practica (4 min)

Prompt exacto sugerido (OpenClaw):

```text
Analiza estas 3 solicitudes y clasificalas en Rule, Memory o Skill. Responde en tabla con columnas: Solicitud, Tipo recomendado, Justificacion (1 frase), Riesgo si se implementa en el tipo equivocado.
Solicitudes:
1) "Siempre escribe commits en formato Conventional Commits"
2) "El producto usa React + TypeScript strict"
3) "Cuando pidan README, genera secciones estandar y checklist final"
```

## Bloque B - Anatomia de SKILL.md y alcance correcto (15 min)

### B1. Concepto y riesgos (5 min)

Que decir (literal):

"Toda skill vive en un directorio y su corazon es `SKILL.md`: frontmatter YAML arriba, instrucciones markdown abajo."

"El error comun es disenar una skill gigante que hace todo. Si no puedes describir la tarea en una frase, el alcance esta mal definido."

Riesgos a enfatizar:

- Disparadores demasiado amplios: la skill se activa donde no debe.
- Instrucciones ambiguas: salida inconsistente.
- Una sola skill con multiples responsabilidades: mantenimiento dificil.

### B2. Ejemplo practico (6 min)

Ejecuta:

```bash
mkdir -p .github/skills/readme-generator
cat > .github/skills/readme-generator/SKILL.md << 'EOF'
---
name: readme-generator
description: Genera README.md estructurado para proyectos de software. Usar cuando pidan crear o rehacer documentacion principal del proyecto.
---

# Objetivo
Generar un README claro, breve y accionable.

# Flujo de trabajo
1. Inspecciona archivos clave del proyecto (package.json, README existente, carpeta src).
2. Extrae nombre del proyecto, stack y comandos de ejecucion.
3. Genera README.md con secciones: Descripcion, Requisitos, Instalacion, Uso, Scripts, Estructura, Contribucion.
4. Si falta informacion critica, marca supuestos explicitamente.

# Criterios de calidad
- No inventar comandos inexistentes.
- Mantener secciones en orden logico.
- Usar lenguaje tecnico claro.
EOF

sed -n '1,220p' .github/skills/readme-generator/SKILL.md
```

Que decir (literal):

"Observa que la descripcion dice cuando activar, y el cuerpo define como ejecutar. Esa separacion mejora precision y testabilidad."

### B3. Validacion (4 min)

Checklist:

- `name` es unico y concreto.
- `description` describe disparadores reales de activacion.
- El flujo tiene pasos imperativos y verificables.
- Hay criterios de calidad para revisar salida.

Prompt exacto sugerido (OpenClaw):

```text
Revisa el SKILL.md mostrado y detecta 5 mejoras concretas.
Devuelve:
1) Problema
2) Riesgo
3) Cambio sugerido (linea exacta a reemplazar)
4) Beneficio esperado
```

## Bloque C - Construccion guiada de una skill real (17 min)

### C1. Planificacion: entradas/salidas/disparadores (5 min)

Que decir (literal):

"Antes de escribir, planificamos. Entradas: que necesita. Salidas: que produce. Disparadores: cuando se activa."

"Si no definimos estos tres elementos, la skill parece funcionar, pero falla en casos borde."

Ejecuta:

```bash
cat > class_21/workshop/plan_readme_skill.md << 'EOF'
# Plan de skill: readme-generator

## Entradas
- Archivos del proyecto en directorio actual.
- README existente (opcional).

## Salidas
- README.md actualizado con secciones estandar.

## Disparadores
- "genera readme"
- "crear documentacion principal"
- "rehacer README"
EOF

cat class_21/workshop/plan_readme_skill.md
```

### C2. Registro por agente (6 min)

Que decir (literal):

"La misma skill cambia de ubicacion segun el agente. Si se registra en ruta incorrecta, no existe para el agente."

Ejecuta:

```bash
cat > class_21/workshop/skill_paths.md << 'EOF'
# Rutas de registro por agente
- GitHub Copilot (proyecto): .github/skills/<skill>/SKILL.md
- Cursor (proyecto): .cursor/skills/<skill>/SKILL.md
- Claude (proyecto): .claude/skills/<skill>/SKILL.md
- Claude (personal): ~/.claude/skills/<skill>/SKILL.md
- Codex/agents (proyecto): .agents/skills/<skill>/SKILL.md
EOF

cat class_21/workshop/skill_paths.md
```

### C3. Mini practica (6 min)

Prompt exacto sugerido (OpenClaw):

```text
Crea una skill llamada test-case-generator para proyectos TypeScript.
Requisitos:
- Frontmatter con name y description.
- Instrucciones en pasos numerados.
- Criterios de calidad verificables.
- No mezclar responsabilidades fuera de testing.
Devuelve solo el contenido final de SKILL.md listo para guardar.
```

## Bloque D - Testing, debugging y mejora iterativa (12 min)

### D1. Ciclo de prueba (5 min)

Que decir (literal):

"Una skill buena no nace perfecta. Se pule con ciclo corto: activar, observar, evaluar y ajustar."

Ejecuta:

```bash
cat > class_21/workshop/test_protocol.md << 'EOF'
# Protocolo de test de skills
1. Activar skill con 3 frases positivas esperadas.
2. Verificar 2 frases negativas (no debe activar).
3. Evaluar formato y completitud de la salida.
4. Ajustar description o pasos en SKILL.md.
5. Repetir 2-3 iteraciones.
EOF

cat class_21/workshop/test_protocol.md
```

### D2. Diagnostico de fallos comunes (4 min)

Prompt exacto sugerido (OpenClaw):

```text
Tengo este problema: mi skill se activa cuando pido "documentacion de API", pero solo quiero que se active para README general.
Propone:
1) 3 causas probables
2) 3 cambios concretos al campo description
3) 2 pruebas negativas para validar que ya no se active por error
Responde en formato checklist.
```

### D3. Cierre tecnico del bloque (3 min)

Que decir (literal):

"No evaluamos una skill por lo bonita que se vea, sino por su comportamiento bajo prueba y su facilidad de mantenimiento."

## 5) Cierre (5 min)

Que decir (literal):

"Hoy diste el salto de usuario de prompts a disenador de capacidades. Eso cambia por completo la productividad con IA en equipos reales."

"Si puedes definir alcance, registrar bien y testear en ciclos cortos, puedes crear skills confiables para casi cualquier flujo repetible."

Checklist final en vivo:

```bash
ls -la .github/skills/readme-generator
sed -n '1,220p' .github/skills/readme-generator/SKILL.md
cat class_21/workshop/test_protocol.md
```

## 6) Preguntas de chequeo rapidas

- Cual es la diferencia practica entre Rule, Memory y Skill en un caso real de proyecto?
- Que senal indica que una skill tiene alcance demasiado grande?
- Que parte del frontmatter controla mejor la activacion de la skill?
- Que pruebas negativas haria para asegurar que una skill NO se active fuera de contexto?

## 7) Plan de contingencia

Si falla la demo principal:

```bash
mkdir -p class_21/fallback
cat > class_21/fallback/SKILL.md << 'EOF'
---
name: changelog-generator
description: Genera CHANGELOG.md desde commits recientes cuando pidan documentar cambios de release.
---

1. Lee commits recientes.
2. Agrupa por tipo (feat, fix, chore).
3. Genera resumen por version.
EOF
cat class_21/fallback/SKILL.md
```

Si falla la integracion con el agente:

- Mover la explicacion a modo conceptual (anatomia y alcance) mientras se valida ruta de registro.
- Ejecutar revision manual del `SKILL.md` con checklist de calidad.
- Mostrar una iteracion de mejora solo editando description y pruebas negativas.
