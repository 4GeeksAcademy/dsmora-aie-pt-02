# Guia Docente Practica: Clase 33 (version enfocada en JWT + FastAPI)

Clase online para 60-75 minutos.
Basada en el ejemplo de [example.md](example.md).
Objetivo: que el estudiante entienda teoria clave y luego construya por fases una API protegida con JWT usando apoyo de un agente de IA.

---

## 1) Resumen de teoria (12-15 min)

### 1.1 Diferencias entre JWT, Bearer y Basic

No son exactamente "el mismo tipo" de token; estan en capas distintas:

- Basic:
  - Es un esquema de autenticacion HTTP.
  - Envia credenciales del usuario en cada request.
  - Riesgo alto si se usa mal. Hoy casi nunca se recomienda para apps modernas con frontend.

- Bearer:
  - Tambien es un esquema HTTP (`Authorization: Bearer <token>`).
  - "Bearer" significa: quien posee ese token, accede.
  - No define formato interno del token; solo como se transporta.

- JWT:
  - Es un formato de token (header.payload.signature).
  - Normalmente se envia usando esquema Bearer.
  - Puede contener claims como `sub`, `exp`, `role`.

Frase literal para clase:

"Bearer es el sobre de envio, JWT es la carta que va dentro. Basic es otro protocolo distinto que manda credenciales, no un JWT."

### 1.2 LocalStorage vs Cookies (httpOnly + Secure + SameSite)

- LocalStorage:
  - Ventaja: simple de implementar.
  - Desventaja mayor: si hay XSS, el token puede ser robado por JavaScript malicioso.
  - Suele usarse en demos, pero no es la opcion mas segura para sesion en navegador.

- Cookies httpOnly:
  - `httpOnly`: JavaScript no puede leer la cookie.
  - `Secure`: solo via HTTPS.
  - `SameSite`: ayuda contra CSRF.
  - Riesgo: debes disenar proteccion CSRF correctamente cuando aplica.

Regla practica para clase:

- Si es app web en navegador y quieres mayor seguridad: preferir cookie httpOnly + Secure + SameSite.
- Si es cliente movil o integracion server-to-server: Bearer token en header suele ser natural.

### 1.3 401 vs 403 (muy preguntado)

- 401 Unauthorized:
  - Falta token o token invalido/expirado.
  - Problema de autenticacion.

- 403 Forbidden:
  - Usuario autenticado, pero no tiene permiso.
  - Problema de autorizacion.

---

## 2) Plan de clase por fases usando IA (45-55 min)

Base: [example.md](example.md)
Meta: construir la API por capas, validar en /docs y reforzar conceptos al final de cada fase.

### Fase 0 - Preparar entorno (5 min)

Comandos:

```bash
uv venv
source .venv/bin/activate
uv add fastapi uvicorn tinydb python-dotenv "python-jose[cryptography]" "passlib[bcrypt]"
```

Ejecutar:

```bash
uv run uvicorn app:app --reload
```

Prompt para agente IA:

```text
Actua como asistente tecnico para clase en vivo. Dame un checklist minimo para arrancar FastAPI con uv, TinyDB, python-jose y passlib[bcrypt], incluyendo comando de run y estructura inicial de archivos.
```

### Fase 1 - Esquemas y modelo de datos (8 min)

Objetivo:
- Crear modelos Pydantic para:
  - UserCreate, UserLogin, UserOut
  - ProfileUpdate, ProfileOut
- Separar almacenamiento en TinyDB:
  - tabla users
  - tabla profiles

Punto docente:
- Explicar por que `users` y `profiles` van separados.

Prompt para agente IA:

```text
Genera modelos Pydantic para FastAPI en una API de intercambio de plantas con autenticacion. Necesito UserCreate, UserLogin, UserOut (sin password), ProfileUpdate y ProfileOut. Agrega validaciones basicas de email y campos opcionales de perfil.
```

### Fase 2 - Registro seguro de usuarios (8 min)

Objetivo:
- Implementar `POST /users` publico.
- Hashear password con bcrypt antes de guardar.
- Crear perfil vinculado al crear usuario.

Punto docente:
- "Passwords no se cifran para login; se hashean para no poder recuperarlas en texto plano".

Prompt para agente IA:

```text
Escribe el endpoint POST /users para FastAPI con TinyDB: validar email unico, hashear password con passlib/bcrypt, guardar user y profile inicial, y devolver UserOut sin hashed_password.
```

### Fase 3 - Login + emision JWT (10 min)

Objetivo:
- Implementar `POST /auth/login`.
- Validar credenciales.
- Emitir access token JWT con `sub` y `exp`.
- Configurar `SECRET_KEY` y `ACCESS_TOKEN_EXPIRE_MINUTES` en `.env`.

Punto docente:
- JWT no es secreto: cualquiera puede decodificar payload.
- Lo seguro es la firma + expiracion + secreto robusto.

Prompt para agente IA:

```text
Implementa login JWT en FastAPI con python-jose. Quiero funcion create_access_token(data, expires_delta), lectura de SECRET_KEY y ACCESS_TOKEN_EXPIRE_MINUTES desde .env, validacion de password con bcrypt, y respuesta con access_token + token_type=bearer.
```

### Fase 4 - Dependencia get_current_user (8 min)

Objetivo:
- `OAuth2PasswordBearer(tokenUrl="/auth/login")`
- Dependencia que:
  1) lee Bearer token,
  2) decodifica JWT,
  3) busca usuario en TinyDB,
  4) responde 401 si falla.

Prompt para agente IA:

```text
Crea dependencia get_current_user para FastAPI usando OAuth2PasswordBearer y python-jose. Debe validar firma y expiracion del JWT, extraer sub como email o user_id, buscar usuario en TinyDB y lanzar HTTPException 401 si token falta, es invalido, expiro o usuario no existe.
```

### Fase 5 - Rutas protegidas y autorizacion (10 min)

Objetivo:
- Proteger:
  - `GET /users`
  - `GET /users/{id}`
  - `PUT /users/{id}` solo propio usuario
  - `DELETE /users/{id}` solo propio usuario
  - `GET /profiles/me`
  - `PUT /profiles/me`
  - `GET /auth/me`

Punto docente:
- Caso clasico: token valido pero quiere editar otro usuario -> 403.

Prompt para agente IA:

```text
Implementa rutas protegidas de usuarios y perfiles en FastAPI con Depends(get_current_user). Necesito reglas: 401 si no hay token valido y 403 si un usuario intenta editar o eliminar a otro. Incluye respuesta clara de error.
```

### Fase 6 - Pruebas manuales en /docs (6 min)

Checklist (igual al ejemplo):
- Registrar usuario.
- Login y copiar token.
- Authorize en /docs y probar `GET /auth/me`.
- Probar `GET /users` sin token -> 401.
- Forzar expiracion corta y reprobar ruta protegida -> 401.
- Intentar modificar otro usuario autenticado -> 403.

Prompt para agente IA:

```text
Dame un plan de pruebas manual en /docs para una API JWT en FastAPI que cubra casos felices y errores 401/403. Formato checklist rapido para clase.
```

---

## 3) Mini guion literal (para hablar mientras codeas)

- "Primero validamos identidad: eso es autenticacion."
- "Luego validamos permisos: eso es autorizacion."
- "Bearer no es el token; es la forma de enviarlo en el header."
- "JWT tiene tres partes y el payload no se considera secreto."
- "Si el token falta o expira: 401."
- "Si el usuario esta autenticado pero no puede hacer esa accion: 403."
- "Guardamos password hasheado, nunca texto plano."
- "Separar users y profiles nos da mejor seguridad y arquitectura."

---

## 4) Diferencias clave que te conviene remarcar al cierre

1. Basic vs Bearer:
   - Basic reenvia credenciales.
   - Bearer reenvia token temporal.

2. Bearer vs JWT:
   - Bearer es esquema HTTP.
   - JWT es formato de token.

3. LocalStorage vs Cookie httpOnly:
   - LocalStorage es simple, pero mas expuesto a XSS.
   - Cookie httpOnly reduce robo por JS; requiere buen manejo de CSRF.

4. Seguridad real:
   - No depende de "usar JWT" solamente.
   - Depende de expiracion, secretos, validacion server-side, y control de permisos.

---

## 5) Si te queda tiempo (5 min extra)

Debate rapido:

1. "Que cambiarias para que solo admin vea GET /users?"
2. "Como implementarias refresh token?"
3. "Que pasa si alguien roba un access token valido?"

Esto conecta directo con el proyecto evaluado y deja el puente para clase siguiente.
