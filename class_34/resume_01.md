# Guia Docente Completa: Class 34 - Frontend Session Management y Session Lifecycle Implementation

Clase online para 60-75 minutos.
Documento para profesor: incluye guion literal, comandos exactos y prompts completos para demos en vivo.

## 1) Objetivos de aprendizaje

Al finalizar, el estudiante podra:

- Explicar el ciclo de vida de una sesion frontend: inicializacion, continuidad y destruccion.
- Distinguir mecanismo de autenticacion vs estrategia de almacenamiento.
- Implementar un flujo base de autenticacion con estados claros: no autenticado, autenticando, autenticado, expirado.
- Construir proteccion de rutas con un patron tipo `PrivateRoute`.
- Aplicar hidratacion de sesion al iniciar la app y manejar expiracion con cierre de sesion automatico.
- Identificar riesgos de seguridad comunes (token en cliente, UI-only guards, falta de validacion backend).

## 2) Agenda sugerida (60-75 min)

Ruta base de 66 minutos:

- Apertura y contexto: 5 min
- Bloque A - Fundamentos de sesion en frontend: 12 min
- Bloque B - Estados de autenticacion y route guards: 15 min
- Bloque C - Hidratacion de sesion al iniciar app: 13 min
- Bloque D - Expiracion de token y logout automatico: 12 min
- Cierre y chequeo de comprension: 9 min

Version corta (60 min):

- Recortar 3 min del Bloque C (omitir variacion con retries).
- Recortar 3 min del Bloque D (explicar sin codificar segundo caso).

Version extendida (75 min):

- Agregar 9 min de laboratorio guiado: refactor de `PrivateRoute` + manejo de loading y redireccion.

## 3) Preparacion docente (antes de clase)

Checklist tecnico:

- VS Code abierto en la raiz del repo.
- Terminal `bash` disponible.
- Node.js y npm disponibles para ejemplos locales (si se desea ejecutar snippets React).
- Conexion a internet para consultas y demo de prompts.

Comandos de verificacion previa:

```bash
pwd
ls -la
node --version
npm --version
```

Carpeta de trabajo sugerida:

```bash
mkdir -p class_34/workshop
cd class_34/workshop
```

## 4) Guion docente detallado (con texto literal)

## Apertura (5 min)

Que decir (literal):

"Hoy vamos a tratar autenticacion como sistema de estado, no como pantalla de login. Si pensamos en estados y ciclo de vida, desaparecen muchos bugs de sesion." 

"La meta no es solo que funcione en feliz camino; la meta es que sobreviva refresh, cambio de pestana, token expirado y rutas protegidas." 

---

## Bloque A - Fundamentos de sesion en frontend (12 min)

### A1. Marco mental: HTTP sin estado + sesion como continuidad (5 min)

Que decir (literal):

"HTTP no recuerda nada entre requests. La sesion es la estrategia para crear continuidad sin romper seguridad." 

"Sesion no es lo mismo que autenticacion: autenticacion dice quien eres; sesion mantiene tu estado durante la interaccion." 

### A2. Mecanismo vs almacenamiento (4 min)

Que decir (literal):

"JWT, Basic u OAuth son mecanismos. LocalStorage, SessionStorage o cookie httpOnly son estrategias de almacenamiento. Son decisiones relacionadas, pero no son la misma decision." 

Comando de apoyo en vivo:

```bash
echo "Mecanismo = como te identifico | Almacenamiento = donde persisto el estado"
```

### A3. Prompt de diagnostico conceptual (3 min)

Prompt exacto sugerido:

```text
Actua como instructor de frontend.
Explica en una tabla de 2 columnas la diferencia entre:
1) mecanismo de autenticacion
2) estrategia de almacenamiento de sesion
Incluye 3 ejemplos por fila y un error comun por cada concepto.
Respuesta corta, en espanol tecnico simple.
```

---

## Bloque B - Estados de autenticacion y route guards (15 min)

### B1. Estados canonicos (4 min)

Que decir (literal):

"Vamos a modelar cuatro estados: no autenticado, autenticando, autenticado y expirado. Con esto evitamos decisiones ambiguas en UI." 

### B2. Demo guiada de `PrivateRoute` (8 min)

Ejecuta:

```bash
cat > auth-flow-demo.js << 'EOF'
const authState = {
  status: 'authenticating', // una de: unauthenticated | authenticating | authenticated | expired
  token: null,
  user: null
};

function canAccessProtectedRoute(state) {
  return state.status === 'authenticated' && Boolean(state.token);
}

console.log('[canAccessProtectedRoute]', canAccessProtectedRoute(authState));
EOF

node auth-flow-demo.js
```

Que decir (literal):

"Un guard real no solo revisa que exista token. Debe considerar estado de verificacion para no renderizar contenido protegido antes de tiempo." 

"Ocultar botones no protege rutas. La proteccion debe ocurrir antes del render de la vista sensible." 

### B3. Prompt de refactor guiado (3 min)

Prompt exacto sugerido:

```text
Tengo esta regla de acceso: permitir si existe token.
Mejorala para contemplar estados de autenticacion y fase de carga.
Devuelve pseudocodigo de un componente PrivateRoute con:
- loading seguro
- redireccion a /login
- validacion asincrona del token
- limpieza de token invalido
```

---

## Bloque C - Hidratacion de sesion al iniciar app (13 min)

### C1. Concepto operativo (4 min)

Que decir (literal):

"Hidratar sesion es restaurar estado al iniciar la app. Si hay token, no confiamos ciegamente: validamos contra backend antes de declarar autenticado." 

### C2. Demo de flujo de hidratacion (7 min)

Ejecuta:

```bash
cat > hydration-demo.js << 'EOF'
async function hydrateSession(storageToken) {
  console.log('[hydrate] start');

  if (!storageToken) {
    return { status: 'unauthenticated', token: null, user: null };
  }

  // Simulacion de validacion backend
  const isValid = storageToken === 'valid-token';

  if (!isValid) {
    return { status: 'expired', token: null, user: null };
  }

  return {
    status: 'authenticated',
    token: storageToken,
    user: { id: 1, name: 'Ada' }
  };
}

hydrateSession('valid-token').then((state) => console.log('[state]', state));
hydrateSession('old-token').then((state) => console.log('[state]', state));
EOF

node hydration-demo.js
```

Que decir (literal):

"Persistencia sin validacion es riesgo. Validacion sin persistencia rompe UX. Necesitamos ambas, en ese orden." 

### C3. Prompt de mejora de arquitectura (2 min)

Prompt exacto sugerido:

```text
Disena una estrategia de hidratacion para React usando Context + useEffect.
Incluye:
- estado inicial
- transiciones de estado
- llamada a /api/me o /api/verify-token
- manejo de token invalido
- salida esperada en UI durante loading
```

---

## Bloque D - Expiracion de token y logout automatico (12 min)

### D1. Manejo de 401 centralizado (6 min)

Que decir (literal):

"El 401 no se maneja pantalla por pantalla. Se maneja de forma centralizada en el cliente API para limpiar estado y redirigir en un solo lugar." 

Ejecuta:

```bash
cat > api-client-demo.js << 'EOF'
function handleApiResponse(status, state) {
  if (status === 401) {
    return {
      ...state,
      status: 'expired',
      token: null,
      user: null,
      redirectTo: '/login?reason=expired'
    };
  }

  return state;
}

const currentState = { status: 'authenticated', token: 'abc', user: { id: 7 } };
console.log('[after-200]', handleApiResponse(200, currentState));
console.log('[after-401]', handleApiResponse(401, currentState));
EOF

node api-client-demo.js
```

### D2. Checklist de seguridad minima (3 min)

Checklist:

- Verificar token en backend, no solo en cliente.
- Limpiar token y estado al detectar 401.
- Evitar guardar secretos sensibles en LocalStorage.
- Usar guards de ruta y no solo ocultamiento de UI.

### D3. Prompt de hardening (3 min)

Prompt exacto sugerido:

```text
Actua como security reviewer frontend.
Te paso un flujo de sesion con JWT en LocalStorage.
Devuelveme:
1) 5 riesgos principales
2) mitigacion concreta por riesgo
3) que moverias a cookie httpOnly y por que
Formato: lista numerada, maximo 14 lineas.
```

---

## 5) Plan de contingencia docente

Si falla internet o no se puede usar herramientas AI:

- Continuar con los scripts locales de `*.js` ya creados en `class_34/workshop`.
- Simular respuestas API con estados fijos (200 y 401) para mantener la narrativa.
- Cambiar prompts por discusion guiada usando las preguntas de cierre.

Si falta tiempo:

- Priorizar Bloques B y C (son el nucleo de implementacion).
- Dejar Bloque D como lectura guiada + checklist.

Si sobra tiempo:

- Agregar mini reto: incluir estado `refreshing` y reintento de validacion una sola vez.

## 6) Cierre y preguntas de chequeo (9 min)

Que decir (literal):

"Si ustedes pueden explicar estados, hidratacion y expiracion, ya tienen la base para una autenticacion frontend profesional." 

"Recuerden: un token encontrado no es una sesion valida; una sesion valida requiere verificacion." 

Preguntas de chequeo:

- Cual es la diferencia practica entre mecanismo de autenticacion y almacenamiento?
- En que momento exacto debe ejecutarse la hidratacion de sesion?
- Por que ocultar botones no equivale a proteger rutas?
- Que pasos ejecutas cuando recibes 401 en una llamada API?
- Que estado de autenticacion mostrarias en UI mientras validas token?

## 7) Resultado esperado al finalizar la clase

El estudiante deberia poder implementar un flujo base con:

- `PrivateRoute` o guard equivalente.
- Hidratacion inicial con validacion backend.
- Manejo centralizado de expiracion y cierre de sesion.
- Decisiones argumentadas de almacenamiento y seguridad.
