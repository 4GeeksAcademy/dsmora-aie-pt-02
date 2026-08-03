# Guía Docente Completa: Clase 35 - Manejo de Errores

Clase online para 60-75 minutos.
Documento para profesor: incluye objetivo, agenda, guion literal y ejemplos para enseñar programación defensiva, manejo de errores síncronos y asíncronos, renderizado seguro y mensajes de error útiles.

## 1) Objetivo de la clase

Al finalizar, el estudiante podrá:

- Identificar los puntos comunes de fallo en una aplicación.
- Diferenciar errores síncronos de asíncronos.
- Usar try/catch/finally con intención.
- Diseñar llamadas API seguras con estados de carga, error y datos.
- Aplicar valores por defecto, coalescencia nula y encadenamiento opcional.
- Traducir errores técnicos en mensajes claros para usuarios.

## 2) Agenda sugerida (60-75 min)

Ruta base de 65 minutos:

- Apertura y mentalidad defensiva: 8 min
- Bloque A: puntos de fallo y anatomía del error: 12 min
- Bloque B: try/catch/finally y errores async: 14 min
- Bloque C: acceso seguro a datos y fallbacks: 12 min
- Bloque D: mensajes de error y componentes reutilizables: 12 min
- Cierre y preguntas: 7 min

Si tienes 75 min:

- Añade práctica guiada con un componente ErrorMessage y un fetch con reintento.

Si tienes 60 min:

- Resume el bloque de componentes reutilizables y dedica más tiempo a fetch seguro y optional chaining.

## 3) Preparación docente

Checklist:

- Tener un ejemplo de JSON inválido.
- Tener un ejemplo de fetch fallido.
- Poder mostrar datos incompletos para explicar optional chaining.

## 4) Guion docente detallado

## Apertura (8 min)

Qué decir (literal):

"Toda aplicación falla en algún punto. La diferencia entre una app frágil y una app profesional no es que una nunca falle; es cómo responde cuando algo sale mal."

"Hoy vamos a enseñar al sistema a fallar mejor: capturar, contener, comunicar y seguir funcionando cuando sea posible."

## Bloque A - Puntos de fallo y anatomía del error (12 min)

### A1. Dónde suelen fallar las apps (6 min)

Puntos del material:

- Fallos de red.
- Datos faltantes o mal formados.
- Entradas inválidas de usuario.
- Errores del servidor.

Qué decir (literal):

"El error no aparece por sorpresa absoluta. Muchas veces aparece en lugares previsibles: red, parsing, campos nulos, respuestas inesperadas."

### A2. Error síncrono vs asíncrono (6 min)

Ejemplo síncrono:

```javascript
function parseUserData(json) {
  return JSON.parse(json);
}

try {
  const user = parseUserData('invalid json');
  console.log(user.name);
} catch (error) {
  console.error('Error sincrónico capturado:', error.message);
}
```

Qué decir (literal):

"Los errores síncronos suben por la pila de llamadas. Los asíncronos requieren otra atención porque ocurren fuera de ese flujo directo."

## Bloque B - try/catch/finally y errores async (14 min)

### B1. Estructura de try/catch/finally (6 min)

Código base:

```javascript
try {
  // código riesgoso
} catch (error) {
  console.log(error.message);
} finally {
  console.log('limpieza');
}
```

Explica:

- try: envuelve la zona de riesgo.
- catch: toma decisiones sobre el fallo.
- finally: limpia recursos o estado visual.

### B2. Llamadas API seguras (8 min)

Qué decir (literal):

"Cuando una API falla, la UI no debería colapsar ni quedarse muda. Debe saber si está cargando, si falló y qué puede mostrar mientras tanto."

Patrón a enseñar:

- loading
- error
- data

## Bloque C - Acceso seguro a datos y fallbacks (12 min)

### C1. Valores por defecto y operadores de respaldo (5 min)

Ejemplos:

```javascript
function saludar(nombre = 'Invitado') {
  console.log(`¡Hola, ${nombre}!`);
}

const nombreUsuario = entradaUsuario || 'Anónimo';
const titulo = libro?.titulo ?? 'Sin título';
```

Qué decir (literal):

"No todo dato ausente debe romper la interfaz. Muchas veces conviene degradar con gracia y ofrecer un valor alternativo útil."

### C2. Encadenamiento opcional en React (7 min)

Ejemplo:

```javascript
function UserProfile({ user }) {
  const userName = user?.profile?.name ?? 'Usuario Anónimo';
  const userEmail = user?.email ?? 'Correo no proporcionado';
  const userAvatar = user?.profile?.avatar ?? '/default-avatar.png';

  return (
    <div>
      <h2>{userName}</h2>
      <p>{userEmail}</p>
      <img src={userAvatar} alt={userName} />
    </div>
  );
}
```

Punto docente:

- Evitar Cannot read property of undefined.
- Mantener la UI estable aun con datos incompletos.

## Bloque D - Mensajes de error y componentes reutilizables (12 min)

### D1. Traducir errores técnicos (5 min)

Qué decir (literal):

"El usuario no necesita un stack trace. Necesita una explicación breve, clara y accionable."

Comparaciones:

- Error 500: Internal Server Error
- Algo salió mal de nuestro lado. Intenta de nuevo más tarde.

- NetworkError: Failed to fetch
- Estamos teniendo problemas para conectarnos. Revisa tu internet e intenta de nuevo.

### D2. Componente reutilizable de error (7 min)

Ejemplo:

```javascript
const getErrorMessage = (error) => {
  if (!error) return null;
  const lowerError = error.toLowerCase();

  if (lowerError.includes('network') || lowerError.includes('fetch')) {
    return 'Estamos teniendo problemas para conectarnos. Por favor, verifica tu internet e intenta de nuevo.';
  }

  return 'Algo salió mal. Intenta nuevamente en un momento.';
};
```

Qué decir (literal):

"Un componente de error reutilizable reduce duplicación y mantiene consistencia de tono, accesibilidad y acciones disponibles."

## 5) Demo sugerida

1. Intentar parsear JSON inválido.
2. Hacer un fetch que falle.
3. Mostrar loading, error y fallback.
4. Renderizar un perfil con datos incompletos usando optional chaining.

## 6) Preguntas de chequeo

- ¿Qué diferencia hay entre capturar un error y manejarlo bien?
- ¿Cuándo conviene usar finally?
- ¿Por qué optional chaining mejora resiliencia en UI?
- ¿Qué información mínima debe tener un buen mensaje de error?
- ¿Por qué una app no debería mostrar el error técnico crudo al usuario?

## 7) Cierre sugerido

Qué decir (literal):

"El manejo de errores no es una capa decorativa al final del proyecto. Es parte del diseño de una experiencia confiable."

"Una aplicación robusta no es la que nunca falla, sino la que falla con control, claridad y capacidad de recuperación."
