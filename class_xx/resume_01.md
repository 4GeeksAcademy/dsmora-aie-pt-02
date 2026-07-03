# Guía Docente Completa: Class 19 - Fundamentos de Python y Condicionales

Clase online para 60-75 minutos.
Documento para profesor: incluye guion literal, comandos exactos y ejemplos completos. El profesor puede saltarse bloques sin perder continuidad.

## 1) Objetivo de la clase

Al finalizar, el estudiante podrá:

- Declarar variables con nombres descriptivos y reasignar valores correctamente en Python.
- Diferenciar tipos de datos frecuentes: bool, int, float, str, list, dict y None.
- Escribir funciones simples con parametros y retorno.
- Tomar decisiones con if, elif, else y combinar condiciones con and, or, not.

## 2) Agenda sugerida (60-75 min)

Ruta base de 65 minutos:

- Apertura y contexto: 5 min
- Bloque A (variables y tipos): 12 min
- Bloque B (operaciones y funciones): 15 min
- Bloque C (logica y condicionales): 12 min
- Bloque D (bucles y mini reto integrador): 16 min
- Cierre + checklist + Q&A: 5 min

Si tienes 75 min:

- Anade 10 min de practica guiada con un ejercicio extra de clasificacion de edades.

Si tienes 60 min:

- Recorta 5 min del bloque D (deja solo while) y 5 min de Q&A.

## 3) Preparación docente (antes de clase)

Checklist técnico:

- Tener Python 3 disponible en terminal.
- Tener carpeta de trabajo para crear scripts de ejemplo.
- Tener editor abierto para mostrar cambios en vivo.

Comandos de verificación previa:

```bash
python3 --version
mkdir -p class_19/live && cd class_19/live
python3 -c "print('Entorno listo para clase 19')"
```

## 4) Guion docente detallado (con texto literal)

## Apertura (5 min)

Qué decir (literal):

"Hoy vamos a construir una base solida en Python: datos, funciones y decisiones."

"Si al final puedes modelar una decision real con if/elif/else, cumplimos el objetivo de la clase."

## Bloque A - Variables y tipos de datos (12 min)

### A1. Concepto rapido (3 min)

Qué decir (literal):

"Una variable es una etiqueta que apunta a un valor. El nombre debe explicar la intencion, no solo guardar algo."

### A2. Demo guiada (4 min)

Ejecuta:

```bash
cat > variables_tipos.py <<'PY'
edad = 24
nombre = "Ana"
es_estudiante = True
promedio = 18.5
datos_extra = ["Python", 101, None]
perfil = {"pais": "VE", "activo": True}

print(type(edad), edad)
print(type(nombre), nombre)
print(type(es_estudiante), es_estudiante)
print(type(promedio), promedio)
print(type(datos_extra), datos_extra)
print(type(perfil), perfil)
PY
python3 variables_tipos.py
```

Qué decir (literal):

"Fijense que Python infiere el tipo automaticamente, pero nosotros debemos mantener claridad con nombres y estructura."

### A3. Mini práctica (5 min)

Prompt exacto sugerido:

```text
Actua como tutor de programacion. Dame 5 ejercicios cortos para practicar variables en Python.
Condiciones:
1) incluir al menos un bool, un float y un string,
2) pedir reasignacion de valor,
3) mostrar salida esperada,
4) nivel principiante.
```

## Bloque B - Operaciones y funciones (15 min)

### B1. Concepto y riesgos (5 min)

Qué decir (literal):

"Las operaciones cambian o combinan datos. El riesgo principal en principiantes es mezclar tipos sin validar."

"Una funcion encapsula logica reutilizable: entrada, proceso y salida."

### B2. Ejemplo práctico (5 min)

Ejecuta:

```bash
cat > funciones.py <<'PY'
def multiplicar(a, b):
    return a * b

def saludar(nombre):
    return f"Hola, {nombre}"

print(multiplicar(6, 7))
print(saludar("Camila"))
PY
python3 funciones.py
```

Qué decir (literal):

"Si una funcion tiene un nombre claro y devuelve un valor concreto, ya es facil de probar y reutilizar."

### B3. Validación (5 min)

Checklist:

- La funcion tiene verbo en el nombre (por ejemplo, multiplicar, validar, calcular).
- Los parametros tienen significado (evitar x, y si no aportan contexto).
- El return devuelve exactamente lo que promete el nombre de la funcion.

## Bloque C - Logica y condicionales (12 min)

Ejecuta:

```bash
cat > condicionales.py <<'PY'
edad = 17
tiene_permiso = True

if edad >= 18:
    print("Puede entrar")
elif tiene_permiso and edad >= 16:
    print("Puede entrar con permiso")
else:
    print("No puede entrar")
PY
python3 condicionales.py
```

Prompt exacto sugerido:

```text
Explicame paso a paso este bloque de Python para un principiante:
if, elif, else, and, or, not.
Luego dame 3 variaciones del ejemplo de "acceso por edad" con salida esperada.
```

## Bloque D - Bucles y mini reto integrador (16 min)

Ejecuta:

```bash
cat > bucles_reto.py <<'PY'
numeros = [3, 8, 12, 19, 21]
pares = 0
impares = 0

for n in numeros:
    if n % 2 == 0:
        pares += 1
    else:
        impares += 1

print("pares:", pares)
print("impares:", impares)

contador = 1
suma = 0
while contador <= 5:
    suma += contador
    contador += 1

print("suma 1..5:", suma)
PY
python3 bucles_reto.py
```

Prompt exacto sugerido:

```text
Genera un reto integrador en Python para principiantes que combine:
1) variables,
2) una funcion,
3) condicionales,
4) un bucle for.
Incluye solucion comentada y 2 errores tipicos que debo evitar.
```

Qué decir (literal):

"Cuando juntas bucles con condicionales, ya puedes resolver problemas reales pequenos sin repetir codigo manualmente."

## 5) Cierre (5 min)

Qué decir (literal):

"Hoy no solo escribimos sintaxis: construimos una forma de pensar en pasos y decisiones."

"El proximo salto es practicar mas casos, porque programar se aprende haciendo y corrigiendo."

Checklist final en vivo:

```bash
ls -1
python3 condicionales.py
python3 bucles_reto.py
```

## 6) Preguntas de chequeo rápidas

- Que diferencia hay entre asignar (`=`) y comparar (`==`) en Python?
- Cuando usarias `elif` en lugar de varios `if` separados?
- Que ventaja te da poner una operacion dentro de una funcion?
- Como evitas un bucle infinito en `while`?

## 7) Plan de contingencia

Si falla la demo principal:

```bash
python3 - <<'PY'
valor = 14
if valor < 10:
    print("unidad")
elif valor < 100:
    print("decena")
else:
    print("centena o mas")
PY
```

Si falla integración externa:

- Cambiar a explicacion en pizarra con pseudocodigo.
- Ejecutar ejemplos minimos en una sola linea con `python3 -c`.
- Cerrar con ejercicio oral de trazado de condiciones (sin depender de herramientas).