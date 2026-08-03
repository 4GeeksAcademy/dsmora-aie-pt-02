# Guía Docente Completa: Clase 33 - Fundamentos de Autenticación

Clase online para 60-75 minutos.
Documento para profesor: incluye objetivo, agenda, guion literal, ejemplos de código y una ruta clara para explicar autenticación, contraseñas seguras, JWT y protección de rutas.

## 1) Objetivo de la clase

Al finalizar, el estudiante podrá:

- Explicar la diferencia entre autenticación y autorización.
- Identificar por qué una contraseña débil compromete un sistema.
- Comparar autenticación básica, autenticación por token, OAuth y MFA.
- Entender la estructura de un JWT y sus implicaciones de seguridad.
- Reconocer anti-patrones comunes en flujos de autenticación.
- Relacionar autenticación backend con protección efectiva de rutas y recursos.

## 2) Agenda sugerida (60-75 min)

Ruta base de 70 minutos:

- Apertura y problema de seguridad: 8 min
- Bloque A: autenticación vs autorización: 10 min
- Bloque B: contraseñas seguras y hábitos básicos: 10 min
- Bloque C: métodos de autenticación y JWT: 18 min
- Bloque D: seguridad JWT, OAuth, MFA y rutas protegidas: 16 min
- Cierre y preguntas de chequeo: 8 min

Si tienes 75 min:

- Añade una comparación guiada entre guardar un token en localStorage y usar cookies httpOnly.

Si tienes 60 min:

- Resume OAuth y MFA como panorama y dedica más tiempo a JWT y rutas protegidas.

## 3) Preparación docente

Checklist:

- Tener claro un ejemplo simple de login y recurso protegido.
- Mostrar un header Authorization y un JWT como texto separado por puntos.
- Tener lista una mini demo en Python o pseudo backend para emisión de token.

Comando opcional para demo local:

```bash
python3 --version
```

## 4) Guion docente detallado

## Apertura (8 min)

Qué decir (literal):

"Cuando una aplicación no valida bien quién entra, no importa que funcione bonito: queda expuesta. La autenticación es una de las capas mínimas para que un sistema sea confiable."

"Hoy vamos a separar ideas que suelen mezclarse: identidad, permisos, contraseñas, tokens y protección de rutas."

Pregunta inicial:

- ¿Qué diferencia hay entre demostrar quién eres y decidir qué puedes hacer?

## Bloque A - Autenticación vs autorización (10 min)

### A1. Qué es autenticación (4 min)

Qué decir (literal):

"Autenticación responde a la pregunta quién eres. El sistema verifica tu identidad antes de darte acceso."

Ejemplo docente:

- Login con usuario y contraseña.
- Validación con token.
- Verificación biométrica.

### A2. Qué es autorización (3 min)

Qué decir (literal):

"Autorización responde a otra pregunta: ahora que sé quién eres, qué te permito hacer."

Caso para explicar:

- Un usuario normal entra al sistema.
- Un administrador entra al mismo sistema.
- Ambos están autenticados, pero no tienen los mismos permisos.

### A3. Error común (3 min)

Qué decir (literal):

"Ocultar un botón en el frontend no es autorización real. La autorización importante siempre debe existir también en el servidor."

## Bloque B - Contraseñas seguras y hábitos básicos (10 min)

### B1. Por qué importan las contraseñas (4 min)

Qué decir (literal):

"La contraseña sigue siendo una llave crítica. Si es débil, todo el sistema queda más vulnerable aunque el resto esté bien hecho."

Puntos a enfatizar:

- Contraseñas comunes son fáciles de adivinar.
- Reutilizar contraseñas amplifica el daño.
- Una contraseña fuerte reduce accesos no autorizados.

### B2. Frases de paso y hábitos seguros (3 min)

Qué decir (literal):

"Una frase de paso larga y memorable suele ser mejor que una contraseña corta y complicada pero predecible."

Ejemplo didáctico:

- Una clave débil: 123456
- Una frase de paso mejor: CafeGuitarra2024Atardecer

### B3. MFA como última barrera (3 min)

Qué decir (literal):

"Si la contraseña cae, MFA añade una segunda barrera. No arregla todo, pero reduce mucho el riesgo."

## Bloque C - Métodos de autenticación y JWT (18 min)

### C1. Panorama de métodos (5 min)

Explica:

- Basic Auth.
- Autenticación basada en token.
- OAuth e inicio de sesión social.
- MFA.

Qué decir (literal):

"No todos los métodos ofrecen el mismo equilibrio entre simplicidad, seguridad y escalabilidad. Por eso hay que entender el contexto antes de elegir."

### C2. Mecánica de Basic Auth (4 min)

Ejemplo para mostrar:

```javascript
const credentials = 'alice:secret123';
const encodedCredentials = btoa(credentials);

fetch('/api/data', {
	headers: {
		Authorization: `Basic ${encodedCredentials}`
	}
});
```

Punto docente:

- Base64 no es cifrado.
- Sin HTTPS, este enfoque es insuficiente.

### C3. Flujo de autenticación por token (4 min)

Qué decir (literal):

"En autenticación por token, el usuario entrega credenciales una vez. Si son válidas, recibe un token y usa ese token en las solicitudes siguientes."

Formato importante:

```http
Authorization: Bearer <token>
```

### C4. Estructura de JWT (5 min)

Qué decir (literal):

"Un JWT tiene tres partes: header, payload y signature. La carga útil se puede decodificar; no debe contener secretos. La firma sirve para verificar integridad y autenticidad."

Ejemplo visual:

```text
xxxxx.yyyyy.zzzzz
```

Ejemplo de payload:

```json
{
	"sub": "johndoe",
	"exp": 1688648000
}
```

## Bloque D - Seguridad JWT, OAuth, MFA y rutas protegidas (16 min)

### D1. Crear un token JWT en Python (5 min)

Código de referencia:

```python
from datetime import datetime, timedelta
import jwt


def create_access_token(data: dict, secret_key: str, expires_delta: timedelta):
		to_encode = data.copy()
		expire = datetime.utcnow() + expires_delta
		to_encode.update({"exp": expire})
		return jwt.encode(to_encode, secret_key, algorithm="HS256")
```

Qué decir (literal):

"El token no solo identifica al usuario; también debe expirar. Un token sin caducidad es un riesgo innecesario."

### D2. Mejores prácticas de seguridad (4 min)

Puntos clave:

- Secretos fuertes y fuera del código fuente.
- Algoritmo especificado explícitamente.
- Tokens con expiración corta.
- No guardar datos sensibles dentro del payload.
- Cuidado con XSS si el token queda expuesto al JavaScript del cliente.

### D3. OAuth y MFA como evolución del sistema (3 min)

Qué decir (literal):

"OAuth delega identidad a terceros confiables y MFA añade una segunda prueba de identidad. Son capas distintas, no reemplazos mágicos."

### D4. Anti-patrones y rutas protegidas (4 min)

Anti-patrones del material:

- Verificación de roles solo en el cliente.
- Guardar tokens sin criterio de seguridad.
- Mensajes de error demasiado específicos en login.
- No validar autorización del lado servidor.

Caso para explicar:

- El frontend oculta el panel admin.
- El usuario escribe la URL manualmente.
- Si el servidor no valida permisos, el sistema sigue expuesto.

## 5) Demo corta sugerida

Secuencia sugerida:

1. Mostrar login conceptual.
2. Generar token.
3. Enviar token en header Bearer.
4. Explicar ruta protegida.

Ejemplo mínimo:

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get('/private')
def private_route(token: str | None = None):
		if not token:
				raise HTTPException(status_code=401, detail='Unauthorized')
		return {'message': 'Protected content'}
```

## 6) Preguntas de chequeo

- ¿Qué diferencia concreta hay entre autenticación y autorización?
- ¿Por qué Base64 no hace segura una contraseña?
- ¿Por qué un JWT no debe guardar información sensible?
- ¿Qué riesgo hay si el frontend controla permisos sin respaldo del servidor?
- ¿Qué añade MFA aunque una contraseña ya exista?

## 7) Cierre sugerido

Qué decir (literal):

"La autenticación no consiste solo en dejar entrar a alguien. Consiste en verificar identidad, limitar exposición, proteger credenciales y controlar acceso de forma coherente."

"JWT, MFA y OAuth no son adornos modernos; son respuestas a problemas reales de seguridad y escala."
