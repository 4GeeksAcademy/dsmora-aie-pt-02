# Guia Docente Completa: Class 26 - Listas, Diccionarios y Algoritmos Basicos en Python

Clase online para 60-75 minutos.
Documento para profesor: incluye guion literal, comandos exactos y ejemplos completos. El profesor puede saltarse bloques sin perder continuidad.

## 1) Objetivo de la clase

Al finalizar, el estudiante podra:

- Declarar y manipular listas en Python usando indices, append, insert, pop y remove.
- Explicar la diferencia entre listas y diccionarios y elegir la estructura adecuada para cada caso.
- Acceder, actualizar, agregar y eliminar datos dentro de un diccionario.
- Entender cuando conviene aplicar busqueda lineal, busqueda binaria y ordenamientos simples sobre listas.

## 2) Agenda sugerida (60-75 min)

Ruta base de 70 minutos:

- Apertura y contexto: 5 min
- Bloque A - Listas e indices: 14 min
- Bloque B - Operaciones sobre listas y recorrido: 16 min
- Bloque C - Diccionarios en Python: 16 min
- Bloque D - Busqueda y ordenamiento basico: 14 min
- Cierre + checklist + Q&A: 5 min

Si tienes 75 min:

- Anade 5 min de practica guiada para comparar una solucion con lista y otra con diccionario.

Si tienes 60 min:

- Recorta 5 min del Bloque D y deja solo busqueda lineal mas una comparacion conceptual con busqueda binaria.
- Recorta 5 min del Bloque B y muestra insert y del solo como demo del profesor.

## 3) Preparacion docente (antes de clase)

Checklist tecnico:

- Tener Python 3 disponible en terminal.
- Tener una carpeta de trabajo limpia para demos en vivo.
- Tener editor abierto para ejecutar y corregir ejemplos rapidamente.

Comandos de verificacion previa:

```bash
python3 --version
mkdir -p class_26/live && cd class_26/live
python3 -c "print('Entorno listo para class 26')"
```

## 4) Guion docente detallado (con texto literal)

## Apertura (5 min)

Que decir (literal):

"La clase pasada modelamos decisiones con variables, funciones y condicionales. Hoy damos el siguiente paso: manejar colecciones completas de datos."

"Si al final puedes guardar datos, recorrerlos y encontrar informacion dentro de ellos, ya tienes una base real para resolver problemas pequenos de programacion."

## Bloque A - Listas e indices (14 min)

### A1. Concepto rapido (4 min)

Que decir (literal):

"Una lista es una coleccion ordenada de valores. Lo importante no es solo guardarlos, sino entender que cada elemento tiene una posicion."

"En Python las posiciones empiezan en cero. Ese detalle pequeno explica muchos errores de principiantes."

### A2. Demo guiada (5 min)

Ejecuta:

```bash
cat > listas_base.py <<'PY'
fruits = ["apple", "pear", "grape"]

print("full list:", fruits)
print("first item:", fruits[0])
print("last item:", fruits[2])

fruits[1] = "mango"
print("updated list:", fruits)
PY
python3 listas_base.py
```

Que decir (literal):

"Aqui aparecen las tres operaciones base: ver la lista completa, entrar por indice y reemplazar un valor en una posicion concreta."

### A3. Mini practica guiada (5 min)

Ejercicio en vivo:

- Pide al grupo crear una lista llamada cities con 4 valores.
- Pide mostrar el primer y el ultimo elemento.
- Pide reemplazar el segundo elemento por otra ciudad.
- Cierra preguntando que error aparece si intentan leer una posicion que no existe.

## Bloque B - Operaciones sobre listas y recorrido (16 min)

### B1. Concepto y riesgos (5 min)

Que decir (literal):

"Cuando una lista cambia, normalmente hacemos una de cuatro cosas: agregar, quitar, recorrer o buscar."

"El error tipico no es de sintaxis, es de modelo mental: confundir posicion con valor o asumir que insert siempre es la mejor opcion."

### B2. Ejemplo practico (6 min)

Ejecuta:

```bash
cat > listas_operaciones.py <<'PY'
numbers = [10, 20, 30]

numbers.append(40)
numbers.insert(1, 15)
print("after insertions:", numbers)

last_item = numbers.pop()
numbers.remove(20)
print("removed item:", last_item)
print("final list:", numbers)

for value in numbers:
    print("value:", value)

for index in range(len(numbers)):
    print(index, numbers[index])
PY
python3 listas_operaciones.py
```

Que decir (literal):

"append agrega al final y suele ser la opcion natural. insert sirve, pero mueve elementos y por eso conviene usarlo con criterio."

### B3. Validacion (5 min)

Checklist:

- El estudiante distingue cuando usar un indice y cuando usar el valor del elemento.
- El estudiante reconoce que append agrega al final y pop devuelve lo que elimino.
- El estudiante puede recorrer la lista tanto por valor directo como por posicion con range.

## Bloque C - Diccionarios en Python (16 min)

Ejecuta:

```bash
cat > diccionarios.py <<'PY'
student = {
    "name": "Luisa",
    "age": 22,
    "active": True
}

print(student["name"])
print(student.get("city"))

student["age"] = 23
student["city"] = "Bogota"
student.update({"course": "Python", "level": "basic"})

removed_value = student.pop("active")
print("removed value:", removed_value)

for key, value in student.items():
    print(key, "=>", value)
PY
python3 diccionarios.py
```

Actividad guiada:

- Escribe en la pizarra dos casos: lista de asistencia y ficha de un estudiante.
- Pregunta al grupo cual conviene modelar con lista y cual con diccionario.
- Cierra haciendo que un estudiante explique por que name, age y active funcionan mejor como pares key-value.

## Bloque D - Busqueda y ordenamiento basico (14 min)

Ejecuta:

```bash
cat > algoritmos_basicos.py <<'PY'
def linear_search(items, target):
    # Recorremos la lista completa de izquierda a derecha.
    for index, value in enumerate(items):
        # Si el valor actual coincide con lo que buscamos,
        # devolvemos la posicion y terminamos.
        if value == target:
            return index
    # Si terminamos el recorrido sin encontrarlo, devolvemos -1.
    return -1

def bubble_sort(items):
    # Hacemos una copia para no modificar la lista original.
    data = items[:]

    # Cada pasada mueve el valor mas grande hacia el final.
    for limit in range(len(data)):
        # En cada comparacion miramos pares contiguos.
        for index in range(0, len(data) - 1 - limit):
            # Si el elemento actual es mayor que el siguiente,
            # los intercambiamos de posicion.
            if data[index] > data[index + 1]:
                data[index], data[index + 1] = data[index + 1], data[index]

    # Devolvemos una nueva lista ya ordenada.
    return data

def binary_search(items, target):
    # Empezamos buscando dentro de todo el rango disponible.
    left = 0
    right = len(items) - 1

    # Mientras el rango siga siendo valido, seguimos partiendo la lista.
    while left <= right:
        # Calculamos la posicion del medio.
        middle = (left + right) // 2

        # Si el elemento del medio es el objetivo, terminamos.
        if items[middle] == target:
            return middle

        # Si el valor central es menor que el objetivo,
        # descartamos la mitad izquierda.
        if items[middle] < target:
            left = middle + 1
        else:
            # Si el valor central es mayor, descartamos la mitad derecha.
            right = middle - 1

    # Si el rango se cierra, significa que el valor no estaba en la lista.
    return -1

# Lista original desordenada.
values = [39, 12, 5, 27, 18]

# Ordenamos primero para luego poder aplicar binary search.
sorted_values = bubble_sort(values)

# Mostramos la lista original para compararla con la ordenada.
print("original:", values)
# Mostramos el resultado del ordenamiento.
print("sorted:", sorted_values)
# Binary search funciona sobre la lista ordenada.
print("index of 27 in sorted list:", binary_search(sorted_values, 27))
# Linear search funciona aunque la lista siga desordenada.
print("index of 18 in original list:", linear_search(values, 18))
PY
python3 algoritmos_basicos.py
```

Que remarcar durante la demo:

- linear search sirve aunque los datos esten desordenados, pero puede tardar mas porque revisa elemento por elemento.
- bubble sort se usa aqui como puente pedagogico para mostrar por que el orden importa antes de aplicar binary search.
- binary search no revisa toda la lista: va descartando mitades, por eso depende de que los datos ya esten ordenados.

Caso funcional real para la explicacion:

- Usa el ejemplo de una bandeja de tickets de soporte.
- Si los tickets llegan desordenados y quieres encontrar el ticket 1048, puedes hacer linear search.
- Si primero ordenas los tickets por numero o prioridad, ya puedes introducir la idea de binary search.
- Explica que un sistema con IA puede clasificar o resumir tickets, pero sigue necesitando algoritmos clasicos para ordenarlos, priorizarlos y encontrarlos rapido.

Que decir (literal):

"No buscamos memorizar algoritmos complejos hoy. Buscamos entender el criterio: si los datos no estan ordenados, primero pienso como recorrer; si estan ordenados, ya puedo buscar mejor."

"Un asistente con IA en soporte no deja de depender de esto: alguien tiene que ordenar tickets, localizar uno por ID y decidir cual atender primero. La IA se monta sobre esa base, no la sustituye."

## 5) Cierre (5 min)

Que decir (literal):

"Hoy pasamos de variables sueltas a estructuras que guardan muchos datos y a tecnicas para trabajar con ellos."

"Ese salto cambia la calidad de los programas: ya no solo responden, tambien organizan informacion y toman decisiones sobre colecciones completas."

Checklist final en vivo:

```bash
ls -1
python3 diccionarios.py
python3 algoritmos_basicos.py
```

## 6) Preguntas de chequeo rapidas

- Que diferencia practica hay entre usar lista y usar diccionario?
- Cuando prefieres student["key"] y cuando prefieres student.get("key")?
- Por que binary search no sirve directamente sobre una lista desordenada?
- Que ventaja tiene recorrer una lista con for value in items frente a recorrerla por indice?

## 7) Plan de contingencia

Si falla la demo principal:

```bash
python3 - <<'PY'
data = [3, 1, 2]
data.append(4)
print(data)

person = {"name": "Ana", "age": 20}
print(person.get("name"))
PY
```

Si falla integracion externa:

- Haz toda la clase con ejemplos locales en terminal sin depender de videos ni enlaces.
- Sustituye cualquier apoyo externo por preguntas orales y pide que el grupo compare lista vs diccionario.
- Cierra con un mini reto en vivo: guardar 3 productos en una lista y luego modelar uno de ellos con un diccionario.