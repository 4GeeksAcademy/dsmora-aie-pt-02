# Guia Docente Completa: Class 24 - APIs para Agentes y Gestion Segura de Secretos en OpenClaw

Clase online para 60-75 minutos.
Documento para profesor: incluye guion literal, comandos exactos y prompts completos para demos en vivo.

## 1) Objetivos de aprendizaje

Al finalizar, el estudiante podra:

- Explicar por que un agente necesita APIs para actuar sobre sistemas externos, no solo generar texto.
- Identificar componentes clave de una integracion API para agentes: endpoint, metodo, autenticacion y formato JSON.
- Aplicar el marco de pensamiento del agente: datos requeridos, acciones, evaluacion y limites de activacion.
- Redactar pasos replicables y evaluaciones verificables para una skill.
- Configurar secretos con `.env` y mapearlos en `openclaw.json` sin exponer credenciales.
- Auditar proyecto e historial Git para detectar fugas de secretos.

## 2) Agenda sugerida (60-75 min)

Ruta base de 66 minutos:

- Apertura y contexto: 5 min
- Bloque A - APIs vistas por el agente: 14 min
- Bloque B - De API a skill replicable: 16 min
- Bloque C - Secretos y variables de entorno en OpenClaw: 16 min
- Bloque D - Verificacion de seguridad en vivo: 10 min
- Cierre y chequeo de comprension: 5 min

Version corta (60 min):

- Recortar 3 min del Bloque B (hacer solo un ejemplo de paso atomico).
- Recortar 3 min del Bloque D (mostrar solo auditoria en codigo, sin historial Git).

Version extendida (75 min):

- Agregar 5 min de laboratorio guiado: estudiantes redactan su propia evaluacion de skill.
- Agregar 4 min de debate de casos reales de fuga de secretos y mitigaciones.

## 3) Preparacion docente (antes de clase)

Checklist tecnico:

- VS Code abierto en la raiz del repo.
- Terminal bash funcional.
- Proyecto con `.gitignore` editable.
- OpenClaw disponible en el entorno.

Comandos de verificacion previa:

```bash
pwd
ls -la
git status -s
openclaw --help || true
```

## 4) Guion docente detallado (con texto literal)

## Apertura (5 min)

Que decir (literal):

"Hoy pasamos de un agente que solo conversa a un agente que opera sobre sistemas reales con control y seguridad."

"La meta no es solo conectar APIs, sino hacerlo de forma replicable y sin filtrar secretos."

---

## Bloque A - APIs vistas por el agente (14 min)

### A1. Por que ir mas alla del texto (4 min)

Que decir (literal):

"Un agente sin APIs es un analista; un agente con APIs puede ejecutar acciones: leer tareas, enviar mensajes o crear eventos."

"Las APIs son la interfaz universal para que el agente salga del chat y entre en sistemas reales."

### A2. Anatomia minima de una llamada API (6 min)

Que decir (literal):

"Para el agente, una API se resume en 4 piezas: endpoint, metodo, autenticacion y JSON de respuesta."

"Si una de esas 4 piezas no esta clara, la skill se vuelve fragil."

Comando de apoyo en vivo:

```bash
echo "GET https://api.example.com/resource + Authorization: Bearer TOKEN + JSON"
```

Prompt exacto sugerido (OpenClaw):

```text
Explica para principiantes la diferencia entre endpoint, metodo HTTP, autenticacion y respuesta JSON.
Usa una tabla con 4 filas y un ejemplo de cada uno orientado a un agente de IA.
```

### A3. Marco de pensamiento del agente (4 min)

Que decir (literal):

"Antes de implementar, el agente necesita un marco: que datos requiere, que acciones ejecuta, como verificamos y cuando NO debe activarse."

"Este marco evita prompts ambiguos y comportamientos no reproducibles."

---

## Bloque B - De API a skill replicable (16 min)

### B1. Disenar acciones atomicas (6 min)

Que decir (literal):

"Una instruccion buena no dice 'revisa tareas'. Dice exactamente que endpoint consultar, con que header y que filtro aplicar."

"Si un paso no es observable, no es evaluable; y si no es evaluable, no es confiable."

Prompt exacto sugerido (OpenClaw):

```text
Convierte esta instruccion vaga en pasos atomicos y verificables:
"Obten las tareas pendientes del estudiante y guardalas en un archivo".
Devuelve:
1) Pasos numerados
2) Entradas requeridas
3) Salida esperada verificable
Formato breve y tecnico.
```

### B2. Construir estructura minima de skill (6 min)

Comandos exactos para demo:

```bash
mkdir -p .github/skills/assignment-pending-check
cat > .github/skills/assignment-pending-check/SKILL.md << 'EOF'
---
name: assignment-pending-check
description: Consulta tareas pendientes por API y genera salida markdown verificable.
---

# Skill: assignment-pending-check

## Cuando usar
Cuando el usuario pida estado de tareas pendientes.

## Datos requeridos
- API_BASE_URL
- STUDENT_ID
- GEEKS_TOKEN

## Procedimiento
1. Leer token del entorno.
2. Ejecutar GET autenticado al endpoint de tareas.
3. Filtrar estado pending.
4. Guardar salida en pending_assignments.md.

## Salida esperada
Archivo markdown con tareas pendientes y total de elementos.
EOF

sed -n '1,220p' .github/skills/assignment-pending-check/SKILL.md
```

Que decir (literal):

"Fijense que la descripcion define activacion; el procedimiento define ejecucion; y la salida esperada define evaluacion."

### B3. Evaluacion replicable (4 min)

Que decir (literal):

"Evaluar no es 'me parece bien'. Evaluar es comprobar una evidencia concreta y repetible."

Prompt exacto sugerido (OpenClaw):

```text
Actua como revisor de calidad de skills.
Evalua si estos pasos son replicables y sugiere mejoras.
Criterios: especificidad, observabilidad, atomicidad y salida verificable.
Responde con: Aprobado/No aprobado + 3 mejoras concretas.
```

---

## Bloque C - Secretos y variables de entorno en OpenClaw (16 min)

### C1. Riesgo de hardcodear secretos (4 min)

Que decir (literal):

"Si un secreto entra al codigo, tarde o temprano termina expuesto en repo, logs o historial."

"Aunque borres una clave despues, Git conserva historia. Por eso la prevencion es primero."

### C2. Regla de oro: `.env` + `.gitignore` (6 min)

Comandos exactos para demo:

```bash
touch .env
printf "\n.env\n" >> .gitignore
grep -n "^\.env$" .gitignore || true
```

Que decir (literal):

"El valor real vive en `.env` local; el repositorio solo ve placeholders o mapeos."

"Sin `.gitignore`, la boveda queda abierta."

### C3. Mapeo explicito en `openclaw.json` (6 min)

Prompt exacto sugerido (OpenClaw):

```text
Genera un ejemplo minimo de configuracion de una skill en openclaw.json
que mapee dos variables de entorno:
- GEEKS_TOKEN
- API_BASE_URL
Usa sintaxis de interpolacion ${VARIABLE_NAME} y agrega una breve explicacion de por que el mapeo explicito mejora seguridad.
```

Que decir (literal):

"OpenClaw no inyecta todo el entorno por defecto: eso reduce superficie de ataque."

"Mapear explicito es una decision de seguridad y de mantenibilidad."

---

## Bloque D - Verificacion de seguridad en vivo (10 min)

### D1. Buscar exposicion en base de codigo (5 min)

Que decir (literal):

"Seguridad sin auditoria es fe. Vamos a verificar que el secreto no aparezca fuera de `.env`."

Comando exacto para demo (usar placeholder):

```bash
grep -R "abc123" ./
```

Nota para explicar en vivo:

- Reemplazar `abc123` por un patron controlado, nunca proyectar una clave real en pantalla.

### D2. Revisar historial Git por fugas antiguas (5 min)

Comandos exactos para demo:

```bash
git log -p -- . ':!*.png' ':!*.jpg' | grep -n "abc123" || true
```

Que decir (literal):

"La auditoria debe incluir historia, porque un secreto viejo sigue siendo util para un atacante."

"Si detectan exposicion, deben rotar credenciales y limpiar historia con un plan formal."

---

## Cierre y chequeo de comprension (5 min)

Que decir (literal):

"Hoy conectamos 2 mundos: ejecucion por API y seguridad operativa. Sin ambos, un agente en produccion es inestable o riesgoso."

"Si pueden definir pasos verificables y proteger secretos, ya pueden construir skills mas profesionales."

Preguntas de chequeo:

- Cual es la diferencia entre una accion del agente y su evaluacion?
- Por que el mapeo explicito de variables mejora seguridad?
- Que evidencia minima confirma que una skill es replicable?

## 5) Plan de contingencia docente

Si falla OpenClaw o internet:

- Continuar con diseno en pizarra de pasos atomicos y evaluaciones.
- Ejecutar solo comandos locales de seguridad (`grep`, `git`, `.gitignore`).
- Pedir a estudiantes redactar en parejas un `SKILL.md` minimamente verificable.

Si falta tiempo:

- Priorizar Bloques A, B y C.
- Dejar Bloque D como tarea guiada con checklist de auditoria.

## 6) Material de apoyo para el profesor

Prompts de refuerzo (opcionales):

```text
Actua como auditor de seguridad para un proyecto con OpenClaw.
Genera un checklist de 10 puntos para evitar fugas de secretos,
incluyendo .env, .gitignore, historial Git, logs y rotacion de claves.
```

```text
Tengo una skill que consulta una API externa.
Ayudame a definir una evaluacion automatizable en 5 criterios,
con formato de rubrica (criterio, evidencia esperada, fallo comun).
```

Resultado esperado de la clase:

- Estudiantes entienden como convertir una API en una skill accionable.
- Estudiantes aplican patron seguro para secretos en OpenClaw.
- Profesor cuenta con una secuencia replicable para 60-75 min.