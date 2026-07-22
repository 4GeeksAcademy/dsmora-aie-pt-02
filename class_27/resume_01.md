# Guia Docente Completa: Class 27 - Funciones en Python y Buenas Practicas

Clase online para 60-75 minutos.
Documento para profesor: incluye guion literal, comandos exactos y prompts completos para demo con IA.

## 1) Objetivo de la clase

Al finalizar, el estudiante podra:

- Definir y llamar funciones correctamente en Python, diferenciando claramente declaracion vs ejecucion.
- Usar parametros y return para construir funciones reutilizables.
- Explicar alcance (scope), uso basico de lambda y llamadas anidadas.
- Aplicar funciones sobre colecciones con metodos de lista/array y funciones de alto orden simples.
- Aplicar buenas practicas: nombrado, responsabilidad unica, control de longitud y parametros.
- Mejorar legibilidad evitando if/else innecesario, globales y manejo fragil de errores.
- Implementar manejo basico de excepciones, excepciones personalizadas y manejo de recursos con `with`.

## 2) Agenda sugerida (60-75 min)

Ruta base de 70 minutos:

- Apertura y objetivos: 5 min
- Bloque A - Funciones: concepto y definicion vs llamada: 14 min
- Bloque B - Parametros, return y alcance: 12 min
- Bloque C - Lambda, llamadas anidadas y mini practica: 10 min
- Bloque D - Buenas practicas de funciones: 13 min
- Bloque E - Evitando if/else complejos y evitando globales: 8 min
- Bloque F - Excepciones y manejo de recursos: 8 min
- Cierre + checklist + Q&A: 5 min

Si tienes 75 min:

- Anade 5 min para ejercicio extra de refactor de una funcion larga en 3 funciones pequenas.

Si tienes 60 min:

- Recorta 5 min del Bloque C (deja solo 1 ejemplo de lambda).
- Recorta 5 min del Bloque D (manten solo nombrado + responsabilidad unica).

## 3) Preparacion docente (antes de clase)

Checklist tecnico:

- Tener Python 3 disponible en terminal.
- Tener carpeta limpia para demos en vivo.
- Tener editor listo para alternar rapido entre ejemplo "malo" y ejemplo "mejorado".

Comandos de verificacion previa:

```bash
python3 --version
mkdir -p class_27/live && cd class_27/live
python3 -c "print('Entorno listo para class 27')"
```

## 4) Guion docente detallado (con texto literal)

## Apertura (5 min)

Que decir (literal):

"Hasta ahora ya vimos variables, condicionales, listas y bucles. Hoy damos el salto a escribir codigo reusable y mantenible con funciones."

"La meta no es solo que funcione; la meta es que se entienda y se pueda mantener sin dolor."

Micro-nota de repaso (clases 25 y 26):

- Variables, condicionales y listas ya se practicaron; no re-explicar teoria completa.
- Recordatorio rapido: las funciones usaran esas mismas piezas como bloques internos.

## Bloque A - Funciones: concepto y definicion vs llamada (14 min)

### A1. Que es una funcion (4 min)

Que decir (literal):

"Una funcion es un bloque de codigo con un objetivo concreto. Definirla es escribirla; llamarla es ejecutarla."

"Cuando separas problemas en funciones, aplicas dividir y conquistar."

### A2. Demo: definir y luego llamar (6 min)

Ejecuta:

```bash
cat > funciones_base.py <<'PY'
def multiplicar(a, b):
    return a * b

resultado_1 = multiplicar(2, 6)
resultado_2 = multiplicar(5, 2)

print("resultado_1:", resultado_1)
print("resultado_2:", resultado_2)
PY
python3 funciones_base.py
```

Que decir (literal):

"Aqui no copiamos logica dos veces; llamamos la misma funcion con entradas distintas."

### A3. Mini chequeo en vivo (4 min)

- Pregunta: "Que pasaria si escribo solo `multiplicar` sin parentesis?"
- Respuesta esperada: referencia a la funcion, no ejecucion.

## Bloque B - Parametros, return y alcance (12 min)

### B1. Parametros y retorno util (6 min)

Ejecuta:

```bash
cat > parametros_return.py <<'PY'
def calcular_costo_fiesta(invitados):
    costo = invitados * 10
    if invitados > 200:
        costo = costo * 0.9
    return costo

print("150 invitados:", calcular_costo_fiesta(150))
print("250 invitados:", calcular_costo_fiesta(250))
PY
python3 parametros_return.py
```

Que decir (literal):

"El parametro define la entrada, return define la salida. Si la salida es clara, la funcion es facil de probar."

### B2. Alcance y efecto de return (6 min)

Ejecuta:

```bash
cat > alcance_return.py <<'PY'
def demo_scope(a, b):
    mensaje = "solo existe dentro"
    return a * b
    # Este print nunca corre por estar despues de return
    # print("nunca se imprime")

print(demo_scope(3, 4))

try:
    print(mensaje)
except NameError as error:
    print("NameError controlado:", error)
PY
python3 alcance_return.py
```

Que remarcar:

- Variables definidas dentro de la funcion no viven fuera.
- Todo codigo despues de `return` en la misma rama no se ejecuta.

## Bloque C - Lambda, llamadas anidadas y array methods (10 min)

### C1. Lambda en casos pequenos (5 min)

Ejecuta:

```bash
cat > lambda_demo.py <<'PY'
sumar = lambda a, b: a + b
doble = lambda x: x * 2

print("sumar(3, 9):", sumar(3, 9))
print("doble(8):", doble(8))
PY
python3 lambda_demo.py
```

Que decir (literal):

"Lambda no reemplaza todas las funciones; sirve cuando la logica cabe en una sola linea y mejora fluidez."

### C2. Llamadas anidadas y funciones pequenas (5 min)

Ejecuta:

```bash
cat > llamadas_anidadas.py <<'PY'
def get_average(values):
    return sum(values) / len(values)

def get_youngest(values):
    return min(values)

def get_person_info(name, ages):
    return {
        "name": name,
        "average_age": get_average(ages),
        "youngest_age": get_youngest(ages),
    }

print(get_person_info("Luisa", [20, 31, 18, 24]))
PY
python3 llamadas_anidadas.py
```

### C3. Array methods con funciones (2 min dentro del bloque)

Ejecuta:

```bash
cat > array_methods.py <<'PY'
numeros = [1, 2, 3, 4, 5]

cuadrados = list(map(lambda n: n * n, numeros))
pares = list(filter(lambda n: n % 2 == 0, numeros))

print("cuadrados:", cuadrados)
print("pares:", pares)
PY
python3 array_methods.py
```

Que decir (literal):

"Las funciones tambien viven dentro del trabajo con colecciones: map transforma y filter selecciona."

## Bloque D - Buenas practicas de funciones (13 min)

Temas a cubrir (sin omitir):

- Nombrado de variables.
- Nombres significativos.
- Nombrado consistente.
- Convenciones de nombrado.
- Organizacion de funciones.
- Responsabilidad unica.
- Longitud de funcion.
- Manejo de parametros.

Ejecuta (antes/despues):

```bash
cat > buenas_practicas.py <<'PY'
def c(x, y, z, t):
    if t == "normal":
        return x * y + z
    return (x * y + z) * 1.16

def calcular_total_con_impuesto(precio_unitario, cantidad, envio, aplicar_impuesto):
    subtotal = precio_unitario * cantidad + envio
    if not aplicar_impuesto:
        return subtotal
    return subtotal * 1.16

print(c(10, 3, 5, "normal"))
print(calcular_total_con_impuesto(10, 3, 5, True))
PY
python3 buenas_practicas.py
```

Que decir (literal):

"Ambas funciones resuelven algo parecido, pero solo una comunica intencion. Legibilidad tambien es funcionalidad."

Micro-nota de repaso (clase 26):

- Se reutiliza la idea de listas y diccionarios para entradas/salidas de funciones.
- No profundizar de nuevo en operaciones de lista; solo usarlo como contexto.

## Bloque E - Evitando if/else complejos y evitando globales (8 min)

Temas a cubrir:

- Evitando if else.
- Retornos tempranos.
- Busqueda en diccionario.
- Evitando globales.
- Identificando globales.
- Estado adecuado.
- Inyeccion de dependencias.

Ejecuta:

```bash
cat > control_estado.py <<'PY'
def estado_pedido_bad(code):
    if code == 1:
        return "creado"
    elif code == 2:
        return "pagado"
    elif code == 3:
        return "enviado"
    else:
        return "desconocido"

def estado_pedido(code):
    estados = {
        1: "creado",
        2: "pagado",
        3: "enviado",
    }
    return estados.get(code, "desconocido")

def calcular_descuento(total, porcentaje, redondeador):
    # Inyeccion de dependencias: redondeador entra por parametro.
    return redondeador(total * porcentaje)

print(estado_pedido_bad(2))
print(estado_pedido(2))
print(calcular_descuento(105.7, 0.1, round))
PY
python3 control_estado.py
```

Que decir (literal):

"No es prohibir if/else; es evitar arboles largos cuando una estructura de datos comunica mejor la regla."

## Bloque F - Excepciones y manejo de recursos (8 min)

Temas a cubrir:

- Manejo de excepciones.
- Manejo basico de excepciones.
- Excepciones personalizadas.
- Manejo de recursos.

Ejecuta:

```bash
cat > excepciones_recursos.py <<'PY'
class EdadInvalidaError(Exception):
    pass

def validar_edad(edad):
    if edad < 0:
        raise EdadInvalidaError("La edad no puede ser negativa")
    return True

def dividir_seguro(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "No se puede dividir por cero"

print(dividir_seguro(10, 2))
print(dividir_seguro(10, 0))

try:
    validar_edad(-5)
except EdadInvalidaError as error:
    print("Error personalizado:", error)

with open("demo_recursos.txt", "w", encoding="utf-8") as f:
    f.write("manejo de recursos con with")

with open("demo_recursos.txt", "r", encoding="utf-8") as f:
    print(f.read())
PY
python3 excepciones_recursos.py
```

## 5) Prompts exactos para demo con IA

Prompt 1 (refactor de funcion):

```text
Actua como mentor de Python. Refactoriza esta funcion para mejorar:
1) nombres de variables,
2) responsabilidad unica,
3) retornos tempranos,
4) legibilidad.

Devuelveme:
- version original comentada en 3 fallos,
- version mejorada,
- explicacion corta para principiante.
```

Prompt 2 (practica guiada):

```text
Genera 4 ejercicios progresivos de funciones en Python para principiantes.
Condiciones:
1) incluir parametros y return,
2) al menos un ejercicio con lambda,
3) al menos uno con try/except,
4) incluir solucion y salida esperada.
```

Prompt 3 (debugging de alcance):

```text
Te voy a pasar codigo Python con errores de alcance y return.
Identifica:
1) variables fuera de scope,
2) codigo muerto despues de return,
3) correccion minima posible.
Explica paso a paso para nivel principiante.
```

## 6) Cierre (5 min)

Que decir (literal):

"Hoy no solo aprendimos a crear funciones; aprendimos a escribir funciones que otra persona puede entender y mantener."

"En proyectos reales, buenas practicas y manejo de errores son parte del producto, no un extra."

Checklist final en vivo:

```bash
ls -1
python3 funciones_base.py
python3 control_estado.py
python3 excepciones_recursos.py
```

## 7) Preguntas de chequeo rapidas

- Cual es la diferencia exacta entre definir y llamar una funcion?
- Por que return temprano puede mejorar legibilidad?
- Cuando conviene usar diccionario en lugar de cadena larga de if/elif?
- Que problema evita `with open(...)` en manejo de archivos?
- Que ventaja tiene pasar dependencias por parametro en lugar de usar globales?

## 8) Plan de contingencia

Si falla la demo principal:

```bash
python3 - <<'PY'
def area_rectangulo(base, altura):
    if base <= 0 or altura <= 0:
        return "datos invalidos"
    return base * altura

print(area_rectangulo(5, 3))
print(area_rectangulo(-1, 3))
PY
```

Si falla integracion externa:

- Continuar con ejercicios locales y correccion en vivo de funciones pequenas.
- Pedir al grupo convertir un if/elif largo en diccionario con `.get()`.
- Cerrar con reto oral: identificar 2 mejoras de legibilidad en una funcion dada.