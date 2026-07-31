# Guia Docente Completa: Class 35 - Error Handling y Aplicaciones Resilientes

Clase online para 60-75 minutos.
Documento para profesor: incluye guion literal, comandos exactos y prompts completos para demos en vivo.

## 1) Objetivos de aprendizaje

Al finalizar, el estudiante podra:

- Identificar puntos de fallo comunes en apps frontend y backend.
- Aplicar try/catch/finally en flujos sincronos y asincronos.
- Implementar manejo defensivo de datos con ?, ?? y valores por defecto.
- Traducir errores tecnicos a mensajes claros para usuario final.
- Disenar una experiencia resiliente con estados de carga, error y reintento.

## 2) Agenda sugerida (60-75 min)

Ruta base de 66 minutos:

- Apertura y contexto: 6 min
- Bloque A - Anatomia de fallos y mentalidad defensiva: 12 min
- Bloque B - try/catch/finally + async error handling: 16 min
- Bloque C - Fallbacks y acceso seguro a datos: 14 min
- Bloque D - Mensajes amigables y componente de error: 12 min
- Cierre y chequeo: 6 min

Version corta (60 min):

- Recortar 3 min del Bloque C (dejar una sola tecnica: ? + ??).
- Recortar 3 min del Bloque D (explicar componente sin codificar variante).

Version extendida (75 min):

- Agregar 9 min de practica guiada para refactor de una vista fragil a resiliente.

## 3) Preparacion docente (antes de clase)

Checklist tecnico:

- VS Code abierto en la raiz del repo.
- Terminal bash disponible.
- Node.js instalado para ejecutar snippets de demo.
- Conexion a internet para prompts de OpenClaw.

Comandos de verificacion previa:

```bash
pwd
ls -la
node --version
npm --version
```

Carpeta de trabajo sugerida para demo:

```bash
mkdir -p class_35/workshop
cd class_35/workshop
```

## 4) Guion docente detallado (con texto literal)

## Apertura (6 min)

Que decir (literal):

"Hoy no vamos a aprender solo a capturar errores; vamos a disenar software que sigue funcionando cuando algo falla. Esa diferencia separa una app demo de una app profesional." 

"La meta de esta clase es que ustedes puedan anticipar fallos de red, de datos y de usuario, y responder con codigo y UI claros." 

---

## Bloque A - Anatomia de fallos y mentalidad defensiva (12 min)

### A1. Tipos de fallo comunes (5 min)

Que decir (literal):

"Los fallos mas frecuentes vienen de tres fuentes: red inestable, datos incompletos y entradas de usuario inesperadas. Si no modelamos esos escenarios, la app se rompe en produccion." 

"Programacion defensiva significa asumir que algo puede salir mal y escribir el flujo de recuperacion antes del incidente." 

### A2. Mini demo de propagacion de error (4 min)

Ejecuta:

```bash
cat > failure-anatomy.js << 'EOF'
function parseUser(raw) {
  return JSON.parse(raw);
}

try {
  const user = parseUser('{ bad json }');
  console.log(user.name);
} catch (error) {
  console.log('[capturado]', error.name, '-', error.message);
}
EOF

node failure-anatomy.js
```

Que decir (literal):

"Sin try/catch, este mismo error puede tumbar toda la ejecucion. Con manejo explicito, controlamos impacto y mensaje." 

### A3. Prompt de diagnostico (3 min)

Prompt exacto sugerido:

```text
Actua como reviewer de resiliencia en frontend.
Dame una lista de 8 fallos comunes en apps web modernas.
Para cada fallo incluye:
1) sintoma visible
2) causa probable
3) defensa recomendada en codigo
Formato: tabla corta en espanol.
```

---

## Bloque B - try/catch/finally + async error handling (16 min)

### B1. Sintaxis y criterio de uso (5 min)

Que decir (literal):

"No usamos try/catch en todo. Lo usamos alrededor de operaciones riesgosas: parseo, IO, red y transformaciones fragiles." 

"finally no es para logica de negocio; es para limpieza que debe ocurrir siempre, como apagar loading." 

### B2. Demo sincronica y asincrona (8 min)

Ejecuta:

```bash
cat > safe-fetch.js << 'EOF'
async function fetchUser(userId) {
  let loading = true;
  let error = null;

  try {
    if (!userId) throw new Error('userId requerido');

    const response = await fetch('https://jsonplaceholder.typicode.com/users/' + userId);
    if (!response.ok) {
      throw new Error('HTTP ' + response.status);
    }

    const data = await response.json();
    return { loading: false, error: null, data };
  } catch (err) {
    error = err.message;
    return { loading: false, error, data: null };
  } finally {
    loading = false;
    console.log('[finally] loading =', loading);
  }
}

fetchUser(1).then((result) => console.log('[ok]', result.error ? result.error : result.data.name));
fetchUser(null).then((result) => console.log('[error]', result.error));
EOF

node safe-fetch.js
```

Que decir (literal):

"Aqui vemos dos capas: errores de validacion local y errores HTTP remotos. Ambos terminan en un contrato estable: { loading, error, data }." 

### B3. Prompt de mejora de codigo (3 min)

Prompt exacto sugerido:

```text
Refactoriza esta funcion async para hacerla resiliente:
- Debe validar parametros
- Debe manejar response.ok
- Debe devolver contrato estable { loading, error, data }
- Debe traducir errores tecnicos a mensajes utiles
Entrega solo codigo JavaScript y una explicacion de 6 lineas maximo.
```

---

## Bloque C - Fallbacks y acceso seguro a datos (14 min)

### C1. ? vs || vs ?? (5 min)

Que decir (literal):

"El operador || reemplaza cualquier valor falsy, incluso 0 o cadena vacia. En cambio ?? solo reemplaza null o undefined. Esa diferencia evita bugs silenciosos." 

"Combinamos optional chaining con nullish coalescing para leer estructuras profundas sin romper render." 

### C2. Demo de renderizado seguro (6 min)

Ejecuta:

```bash
cat > safe-render.js << 'EOF'
function mapProfile(user) {
  return {
    name: user?.profile?.name ?? 'Usuario anonimo',
    email: user?.email ?? 'Correo no disponible',
    plan: user?.subscription?.plan ?? 'free',
    alerts: user?.preferences?.alerts ?? true,
  };
}

console.log(mapProfile({ profile: { name: 'Ada' }, email: '' }));
console.log(mapProfile({}));
console.log(mapProfile(null));
EOF

node safe-render.js
```

Que decir (literal):

"Si aqui usaramos || para email, una cadena vacia se pisaria aunque fuera intencional. Con ?? solo cubrimos ausencia real de dato." 

### C3. Prompt de practica (3 min)

Prompt exacto sugerido:

```text
Quiero endurecer un componente React que rompe cuando faltan campos en `user`.
Genera una version robusta usando:
- optional chaining
- nullish coalescing
- valores por defecto semanticos
Incluye tambien 4 casos de prueba de entrada/salida en texto.
```

---

## Bloque D - Mensajes amigables y componente de error (12 min)

### D1. Traduccion de errores tecnicos (4 min)

Que decir (literal):

"El usuario no necesita ver stack traces ni codigos crudos. Necesita entender que paso y que puede hacer ahora." 

"Un buen mensaje de error tiene tres piezas: contexto, tranquilidad y accion sugerida." 

### D2. Demo de mapeo de errores + UI reusable (6 min)

Ejecuta:

```bash
cat > error-message-map.js << 'EOF'
function getErrorMessage(errorText) {
  if (!errorText) return null;
  const e = errorText.toLowerCase();

  if (e.includes('network') || e.includes('fetch')) {
    return 'No pudimos conectar. Revisa tu internet e intenta de nuevo.';
  }
  if (e.includes('404')) {
    return 'No encontramos ese recurso. Verifica el identificador.';
  }
  if (e.includes('500')) {
    return 'Tuvimos un problema interno. Intenta nuevamente en unos minutos.';
  }
  return 'Ocurrio un error inesperado. Vuelve a intentarlo.';
}

['NetworkError: failed to fetch', 'HTTP 404', 'HTTP 500', 'TypeError raro'].forEach((sample) => {
  console.log(sample, '=>', getErrorMessage(sample));
});
EOF

node error-message-map.js
```

Que decir (literal):

"Mismo error tecnico, distinto impacto de producto segun como lo comuniquemos. Este mapeo debe ser consistente en toda la app." 

### D3. Prompt para componente React (2 min)

Prompt exacto sugerido:

```text
Crea un componente React `ErrorMessage` reutilizable con:
- prop `error`
- prop opcional `onRetry`
- `role="alert"` para accesibilidad
- mapeo de error tecnico a mensaje amigable
Devuelve codigo completo y ejemplo de uso en una vista con fetch.
```

---

## 5) Plan de contingencia docente

Si falla internet durante clase:

- Mantener demos con los archivos locales `*.js` ya creados en [class_35/workshop](class_35/workshop).
- Simular respuestas HTTP con objetos locales y estados manuales.
- Sustituir prompts por discusion guiada con checklist de decisiones.

Si falta tiempo:

- Priorizar Bloques B y C.
- Explicar Bloque D solo con ejemplo de mapeo y una pregunta de reflexion.

Si sobra tiempo:

- Mini reto: implementar politicas distintas para 401, 403, 404 y 500.

## 6) Cierre y preguntas de chequeo (6 min)

Que decir (literal):

"Una app resiliente no es la que nunca falla; es la que falla con control, informa bien y se recupera rapido." 

"Si hoy se llevan una regla, que sea esta: cada operacion riesgosa necesita estrategia de fallo, no solo estrategia de exito." 

Preguntas de chequeo:

- Cuando conviene usar try/catch y cuando no?
- Que problema evita combinar ? con ?? en datos anidados?
- Cual es la diferencia practica entre || y ?? en formularios?
- Como cambia la UX cuando traduces errores tecnicos a mensajes accionables?

## 7) Resultado esperado al finalizar la clase

El estudiante deberia poder:

- Implementar una funcion async resiliente con contrato estable de estado.
- Proteger renderizado ante datos incompletos sin romper UI.
- Disenar un mapeo central de errores tecnicos a mensajes de producto.
- Defender decisiones de manejo de errores con criterio de UX y mantenibilidad.