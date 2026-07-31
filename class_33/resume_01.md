# Guia Docente Completa: Class 33 - Fundamentos de Autenticacion, Contrasenas Seguras y JWT con FastAPI

Clase online para 60-75 minutos.
Documento para profesor: incluye guion literal, comandos exactos y prompts completos. El profesor puede recortar o extender sin romper continuidad.

## 1) Objetivo de la clase

Al finalizar, el estudiante podra:

- Diferenciar autenticacion vs autorizacion y explicar por que importa en APIs reales.
- Aplicar practicas de contrasenas seguras (fuerza, passphrases, gestores, MFA).
- Entender el flujo JWT de punta a punta: emision, uso, expiracion y revocacion.
- Implementar autenticacion JWT basica en FastAPI con rutas protegidas.

## 2) Agenda sugerida (60-75 min)

Ruta base de 65 minutos:

- Apertura y contexto: 5 min
- Bloque A: fundamentos de autenticacion: 12 min
- Bloque B: contrasenas seguras y MFA: 14 min
- Bloque C: estructura y ciclo JWT: 14 min
- Bloque D: implementacion JWT en FastAPI: 15 min
- Cierre + chequeo + Q&A: 5 min

Si tienes 75 min:

- Agrega 10 min de practica guiada para que cada estudiante agregue una ruta protegida nueva y pruebe expiracion de token.

Si tienes 60 min:

- Recorta la parte de revocacion avanzada y deja solo expiracion + middleware en demo del profesor.

## 3) Preparacion docente (antes de clase)

Checklist tecnico:

- Python 3.10+ disponible.
- Entorno virtual operativo (pipenv o venv).
- Terminal en la raiz del repo.

Comandos de verificacion previa:

```bash
python3 --version
mkdir -p class_33/demo_jwt && cd class_33/demo_jwt
python3 -m venv .venv && source .venv/bin/activate
pip install fastapi "uvicorn[standard]" "python-jose[cryptography]" "passlib[bcrypt]" python-multipart
```

## 4) Guion docente detallado (con texto literal)

## Apertura (5 min)

Que decir (literal):

"Hoy no solo vamos a iniciar sesion, vamos a disenar una autenticacion que resista errores comunes y ataques basicos."

"Vamos a unir tres capas: fundamentos, higiene de contrasenas y JWT implementado en FastAPI."

## Bloque A - Fundamentos de autenticacion (12 min)

Lecciones base: autenticacion vs autorizacion, metodos, tokens, rutas protegidas, anti patrones.

### A1. Concepto rapido (4 min)

Que decir (literal):

"Autenticacion responde quien eres. Autorizacion responde que puedes hacer. Si mezclas ambas, rompes seguridad y mantenimiento."

"Un sistema robusto primero valida identidad y despues aplica permisos por recurso."

### A2. Demo guiada: decision de acceso (4 min)

Ejecuta:

```bash
cd class_33/demo_jwt
cat > auth_vs_authz.py <<'PY'
def autenticar(usuario, password):
    return usuario == 'ana' and password == 'secreto123'

def autorizar(usuario, recurso):
    permisos = {'ana': ['perfil', 'facturas'], 'luis': ['perfil']}
    return recurso in permisos.get(usuario, [])

ok = autenticar('ana', 'secreto123')
print('Autenticada:', ok)
print('Acceso a facturas:', autorizar('ana', 'facturas'))
print('Acceso a admin:', autorizar('ana', 'admin'))
PY
python auth_vs_authz.py
```

Que decir (literal):

"Noten que estar autenticado no implica acceso total. Ese es el error mas comun en apps junior."

### A3. Mini practica (4 min)

Prompt exacto sugerido:

```text
Actua como instructor de ciberseguridad para developers junior. Dame 3 ejemplos concretos donde autenticacion y autorizacion se confunden en una API, y como corregir cada caso.
```

## Bloque B - Contrasenas seguras y MFA (14 min)

Lecciones base: fuerza de contrasena, passphrases, gestor de contrasenas, MFA, habitos diarios.

### B1. Concepto y riesgos (5 min)

Que decir (literal):

"La mayoria de incidentes no empiezan por un zero-day, empiezan por credenciales debiles o reutilizadas."

"Una passphrase larga y unica mas MFA reduce drasticamente riesgo en cuentas reales."

### B2. Ejemplo practico: hash de contrasena (5 min)

Ejecuta:

```bash
cd class_33/demo_jwt
cat > password_hash_demo.py <<'PY'
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

password = 'mi frase super segura 2026'
hashed = pwd_context.hash(password)
print('Hash generado:', hashed)
print('Verificacion correcta:', pwd_context.verify(password, hashed))
print('Verificacion incorrecta:', pwd_context.verify('otra-clave', hashed))
PY
python password_hash_demo.py
```

Que decir (literal):

"Nunca almacenamos password plano. Solo hash con algoritmo resistente como bcrypt."

"Si se filtra la base, hashes robustos frenan ataques offline."

### B3. Validacion (4 min)

Checklist:

- El hash cambia aunque la password sea parecida.
- La verificacion verdadera funciona solo con la clave correcta.
- Queda claro para el grupo que MFA complementa, no reemplaza, buenas contrasenas.

## Bloque C - JWT: estructura, flujo y seguridad (14 min)

Lecciones base: estructura del token, almacenamiento frontend, expiracion, revocacion, mejores practicas.

### C1. Flujo JWT explicado (5 min)

Que decir (literal):

"JWT no es sesion en servidor por defecto: el cliente porta el token y el backend valida firma y expiracion en cada request."

"Header, payload y signature tienen roles distintos: metadata, claims y prueba criptografica."

### C2. Demo de emision y validacion (5 min)

Ejecuta:

```bash
cd class_33/demo_jwt
cat > jwt_parts_demo.py <<'PY'
from datetime import datetime, timedelta, timezone
from jose import jwt

SECRET_KEY = 'dev-secret-change-me'
ALGORITHM = 'HS256'

payload = {
    'sub': 'ana',
    'scope': 'student',
    'exp': datetime.now(timezone.utc) + timedelta(minutes=5)
}

token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
print('JWT:', token)

decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
print('Payload decodificado:', decoded)
PY
python jwt_parts_demo.py
```

### C3. Prompt de refuerzo (4 min)

Prompt exacto sugerido:

```text
Explica para una clase de bootcamp cuando conviene guardar JWT en memoria, localStorage o cookies httpOnly. Incluye riesgos de XSS y CSRF en lenguaje simple.
```

## Bloque D - Implementacion JWT en FastAPI (15 min)

Lecciones base: infraestructura JWT en FastAPI, endpoint de login, rutas protegidas con dependencia/middleware.

### D1. Construccion guiada (10 min)

Ejecuta:

```bash
cd class_33/demo_jwt
cat > main.py <<'PY'
from datetime import datetime, timedelta, timezone
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = 'dev-secret-change-me'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 20

app = FastAPI(title='Class 33 JWT Demo')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# Simulacion de usuario persistido
fake_user_db = {
    'ana': {
        'username': 'ana',
        'hashed_password': pwd_context.hash('secreto123'),
        'role': 'student'
    }
}

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str):
    user = fake_user_db.get(username)
    if not user:
        return None
    if not verify_password(password, user['hashed_password']):
        return None
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='No se pudo validar credenciales',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get('sub')
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = fake_user_db.get(username)
    if user is None:
        raise credentials_exception
    return user

@app.post('/login')
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail='Credenciales invalidas')
    access_token = create_access_token(
        data={'sub': user['username'], 'role': user['role']},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {'access_token': access_token, 'token_type': 'bearer'}

@app.get('/profile')
def profile(current_user: dict = Depends(get_current_user)):
    return {
        'message': 'Ruta protegida OK',
        'user': current_user['username'],
        'role': current_user['role']
    }
PY

uvicorn main:app --reload --port 8010
```

En otra terminal para probar:

```bash
curl -s -X POST 'http://127.0.0.1:8010/login' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=ana&password=secreto123'

# Copia el access_token devuelto y pegalo en TOKEN
TOKEN='PEGA_AQUI_EL_TOKEN'
curl -s 'http://127.0.0.1:8010/profile' -H "Authorization: Bearer $TOKEN"
```

Que decir (literal):

"Este flujo cubre lo esencial: login valida password hasheada, emite JWT con expiracion y protege rutas por dependencia."

"En produccion, cambiaremos secreto, moveremos usuarios a DB real y agregaremos refresh/revocacion."

### D2. Prompt exacto para extension (5 min)

```text
Actua como senior backend. Sobre este main.py de FastAPI, agrega endpoint /admin que solo responda si el claim role es admin. Si no, devolver 403. Explica cada cambio en 5 puntos maximo.
```

## 5) Cierre (5 min)

Que decir (literal):

"Si solo recuerdan una idea: seguridad no es un endpoint, es una cadena de decisiones coherentes desde la password hasta la ruta protegida."

"Hoy conectamos teoria y practica: fundamentos, higiene de credenciales y JWT real funcionando."

Checklist final en vivo:

```bash
cd class_33/demo_jwt
python auth_vs_authz.py
python password_hash_demo.py
python jwt_parts_demo.py
```

## 6) Preguntas de chequeo rapidas

- Cual es la diferencia exacta entre autenticacion y autorizacion?
- Por que no debemos guardar passwords en texto plano?
- Que validaciones minimas debes hacer al recibir un JWT?
- Que cambia entre un prototipo JWT local y una implementacion productiva?

## 7) Plan de contingencia

Si falla la demo principal de FastAPI:

```bash
cd class_33/demo_jwt
python jwt_parts_demo.py
python password_hash_demo.py
```

Si falla la instalacion de dependencias:

```bash
cd class_33/demo_jwt
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install fastapi "uvicorn[standard]" "python-jose[cryptography]" "passlib[bcrypt]" python-multipart
```

Si hay dudas sobre OAuth/login social durante clase:

- Explicar el flujo en 4 pasos: redireccion al proveedor, consentimiento, callback con codigo, intercambio por token en backend.
- Aclarar que no se confia en datos del cliente sin verificar firma/tokens del proveedor.
- Dejar integracion completa (Google/GitHub) como practica posterior para no romper el ritmo de la sesion.