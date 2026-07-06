# Guia Docente Completa: Class 22 - Prompting Fundamentals + Spec-Driven Design

Clase online para 60-75 minutos.
Documento para profesor: incluye guion literal, comandos exactos y prompts completos para demos en vivo.

## 1) Objetivo de la clase

Al finalizar, el estudiante podra:

- Diferenciar prompts vagos vs prompts claros usando contexto y especificidad.
- Escribir prompts efectivos con criterio de calidad verificable.
- Transformar una necesidad de producto en una especificacion accionable para IA.
- Redactar criterios de aceptacion en formato Dado-Cuando-Entonces.
- Aplicar el patron Matrioshka para dividir una tarea grande en subespecificaciones.

## 2) Agenda sugerida (60-75 min)

Ruta base de 65 minutos:

- Apertura y contexto: 5 min
- Bloque A - Fundamentos de prompting efectivo: 12 min
- Bloque B - De prompt a especificacion: 15 min
- Bloque C - Criterios de aceptacion y evaluacion: 15 min
- Bloque D - Patron Matrioshka y anti-patrones comunes: 13 min
- Cierre + checklist + Q&A: 5 min

Si tienes 75 min:

- Anade 10 min de practica guiada para que el grupo convierta una especificacion debil en fuerte.

Si tienes 60 min:

- Recorta 5 min del Bloque C y 5 min del Bloque D, dejando la practica evaluativa como tarea.

## 3) Preparacion docente (antes de clase)

Checklist tecnico:

- VS Code abierto en la raiz del repo.
- Terminal bash operativa.
- Asistente de IA disponible (OpenClaw/Copilot Chat o equivalente).
- Carpeta de clase con permisos de escritura.

Comandos de verificacion previa:

```bash
cd /workspaces/dsmora-aie-pt-02
pwd
ls -la class_22
python3 --version
```

## 4) Guion docente detallado (con texto literal)

## Apertura (5 min)

Que decir (literal):

"Hoy vamos a conectar dos habilidades clave: pedir bien y especificar bien. Prompting te ayuda a iniciar; especificacion te ayuda a terminar con calidad."

"Si solo dices lo que quieres de forma vaga, la IA adivina. Si defines objetivo, alcance y criterios, la IA ejecuta con precision."

## Bloque A - Fundamentos de prompting efectivo (12 min)

### A1. Concepto rapido (4 min)

Que decir (literal):

"Un prompt fuerte tiene tres cosas: claridad, especificidad y contexto. Sin esas tres, la respuesta se vuelve generica."

"No buscamos prompts largos, buscamos prompts utiles y comprobables."

### A2. Demo guiada (4 min)

Ejecuta:

```bash
mkdir -p class_22/workshop
cat > class_22/workshop/prompt_vago.txt << 'EOF'
Crea una pantalla de login moderna.
EOF

cat > class_22/workshop/prompt_mejorado.md << 'EOF'
Objetivo:
Construir pantalla de login para una app web.

Alcance:
- Campos email y password
- Boton de enviar
- Mensajes de error por validacion

Restricciones:
- React con componentes funcionales
- Sin librerias nuevas

Criterios de aceptacion:
- Dado email invalido, cuando el usuario envia, entonces muestra mensaje de error.
- Dado password vacio, cuando el usuario envia, entonces bloquea envio.
EOF

cat class_22/workshop/prompt_vago.txt
cat class_22/workshop/prompt_mejorado.md
```

Que decir (literal):

"El primer prompt pide algo bonito. El segundo describe resultado, limites y validacion. Esto reduce ambiguedad y retrabajo."

### A3. Mini practica (4 min)

Prompt exacto sugerido (OpenClaw):

```text
Evalua estos dos prompts (vago vs mejorado) en una tabla con columnas: Claridad, Especificidad, Contexto, Riesgo de mala interpretacion.
Asigna puntaje de 1 a 5 y propone una mejora concreta por cada prompt.
```

## Bloque B - De prompt a especificacion (15 min)

### B1. Concepto y riesgos (5 min)

Que decir (literal):

"Una especificacion no es una explicacion larga; es un contrato ejecutable entre persona y agente."

"Los 5 bloques minimos son: objetivo, alcance, restricciones, criterios de aceptacion y contexto."

Riesgos a enfatizar:

- Pedir demasiado en una sola especificacion.
- Mezclar objetivos con detalles irrelevantes.
- No declarar restricciones tecnicas.

### B2. Ejemplo practico (6 min)

Ejecuta:

```bash
cat > class_22/workshop/spec_login_v1.md << 'EOF'
# Especificacion: Login Basico

## Objetivo
Implementar un componente LoginForm funcional.

## Alcance
- UI de login (email/password)
- Validaciones basicas de cliente
- Envio de formulario simulado

## Fuera de alcance
- Integracion real con backend
- Recuperacion de password

## Restricciones
- Usar React funcional con hooks
- No usar librerias nuevas
- Modificar solo archivos en src/components/

## Criterios de aceptacion
- Dado email invalido, cuando se presiona enviar, entonces aparece error de email.
- Dado password vacio, cuando se presiona enviar, entonces aparece error de password.
- Dado ambos campos validos, cuando se presiona enviar, entonces se ejecuta onSubmit con payload.
EOF

sed -n '1,220p' class_22/workshop/spec_login_v1.md
```

Que decir (literal):

"Fijate en la seccion fuera de alcance: eso evita scope creep. La IA no debe inventar extras fuera del contrato."

### B3. Validacion (4 min)

Checklist:

- El objetivo se puede verificar en una frase.
- El alcance y fuera de alcance no se contradicen.
- Las restricciones son concretas (tecnologia, carpetas, dependencias).
- Los criterios de aceptacion se pueden probar.

Prompt exacto sugerido (OpenClaw):

```text
Revisa esta especificacion y detecta 5 mejoras concretas.
Responde en formato:
1) Problema
2) Riesgo
3) Cambio sugerido
4) Como validarlo
```

## Bloque C - Criterios de aceptacion y evaluacion (15 min)

### C1. Contrato Dado-Cuando-Entonces (5 min)

Que decir (literal):

"Si no puedes verificarlo, no esta especificado. Dado-Cuando-Entonces convierte ideas en pruebas."

"Un criterio fuerte elimina palabras ambiguas como rapido, bonito o robusto sin metrica."

### C2. Demo guiada (5 min)

Ejecuta:

```bash
cat > class_22/workshop/acceptance_criteria.md << 'EOF'
# Criterios de Aceptacion - Login

1) Dado que el email no contiene '@',
cuando el usuario presiona enviar,
entonces el formulario muestra "Email invalido" y no envia datos.

2) Dado que la password tiene menos de 8 caracteres,
cuando el usuario presiona enviar,
entonces el formulario muestra "Password minima: 8 caracteres".

3) Dado que ambos campos son validos,
cuando el usuario presiona enviar,
entonces se muestra "Login enviado" y se limpia el formulario.
EOF

cat class_22/workshop/acceptance_criteria.md
```

Prompt exacto sugerido (OpenClaw):

```text
Convierte estos criterios en casos de prueba manual con columnas: ID, Precondicion, Paso, Resultado esperado.
Incluye al menos 6 casos (3 positivos y 3 negativos).
```

### C3. Mini evaluacion (5 min)

Que decir (literal):

"Evaluar especificaciones temprano cuesta minutos; corregir implementaciones tarde cuesta horas."

Checklist de evaluacion rapida:

- Hay criterios para caso feliz y casos limite.
- No hay lenguaje ambiguo.
- Cada criterio tiene resultado observable.

## Bloque D - Patron Matrioshka y anti-patrones comunes (13 min)

### D1. Patron Matrioshka (5 min)

Que decir (literal):

"No pidas una app completa en un solo tiro. Divide de contenedor a componente: de afuera hacia adentro."

Ejecuta:

```bash
cat > class_22/workshop/matrioshka_plan.md << 'EOF'
# Matrioshka - Login Feature

1. Contenedor: AuthPage
2. Seccion: LoginCard
3. Componente: LoginForm
4. Elemento: EmailInput
5. Elemento: PasswordInput
6. Elemento: SubmitButton
EOF

cat class_22/workshop/matrioshka_plan.md
```

### D2. Anti-patrones comunes (4 min)

Que decir (literal):

"Los 4 anti-patrones que mas rompen resultados: especificacion gigante, asumir memoria de la IA, mezclar declarativo con microgestion, y criterios no verificables."

Prompt exacto sugerido (OpenClaw):

```text
Analiza esta especificacion y marca anti-patrones:
- Especificacion demasiado grande
- Falta de restricciones
- Criterios ambiguos
- Dependencia de contexto no incluido
Devuelve una version corregida y mas pequena (maximo 180 palabras).
```

### D3. Cierre tecnico del bloque (4 min)

Que decir (literal):

"Primero define QUE construir y COMO validar; luego dejas que la IA decida el COMO implementar dentro de restricciones claras."

## 5) Cierre (5 min)

Que decir (literal):

"Prompting y specification-driven design no compiten: se complementan. Uno abre la conversacion y el otro cierra el contrato de calidad."

"Tu ventaja no es escribir prompts largos; tu ventaja es escribir instrucciones comprobables."

Checklist final en vivo:

```bash
ls -la class_22/workshop
sed -n '1,220p' class_22/workshop/spec_login_v1.md
sed -n '1,220p' class_22/workshop/acceptance_criteria.md
```

## 6) Preguntas de chequeo rapidas

- Que diferencia hay entre un prompt claro y una especificacion completa?
- Por que los criterios de aceptacion se consideran un contrato?
- Que problema evita declarar "fuera de alcance"?
- Cuando conviene usar el patron Matrioshka?

## 7) Plan de contingencia

Si falla la demo principal:

```bash
mkdir -p class_22/workshop
printf "Fallback demo activa\n" > class_22/workshop/fallback.txt
cat class_22/workshop/fallback.txt
```

Si falla la integracion con IA:

- Haz la dinamica en pizarra: convertir prompt vago a especificacion en 5 bloques.
- Pide a estudiantes evaluar una especificacion debil con el checklist.
- Cierra con ejercicio oral de Dado-Cuando-Entonces por parejas.
