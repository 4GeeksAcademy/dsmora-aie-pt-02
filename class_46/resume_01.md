# Clase 46: NumPy y Pandas para trabajar con arrays y datos tabulares

## Hilo con las dos clases anteriores

Esta clase no empieza desde cero. Continúa el trabajo de telemetría de las dos clases anteriores y cambia el foco: antes diseñamos y capturamos los eventos; ahora aprendemos a trabajar con los datos que esos eventos producen.

### Lo que viene de la clase 43

En la clase 43 se establecieron los fundamentos:

- La telemetría recoge señales observables para tomar decisiones basadas en evidencia.
- Cada evento debe responder a una pregunta o decisión concreta.
- El `event envelope` organiza los campos base del evento y sus `properties`.
- Hay que elegir cómo procesar los datos: en flujo cuando importa la inmediatez o por lotes cuando se pueden acumular.
- El transporte debe ser viable y la carga útil debe ser pequeña, consistente y estable.

**Frase de enlace para decir en clase**

> En la clase 43 decidimos qué señales queríamos recoger, cómo describir cada evento y cuándo convenía procesarlo en flujo o por lotes. Hoy vamos a centrarnos en cómo trabajar con conjuntos de datos numéricos y tabulares, que es la forma concreta que necesitamos para analizarlos y prepararlos.

### Lo que viene de la clase 45

En la clase 45 se llevó ese diseño al frontend:

- Se distinguieron identidad, sesión, contexto, uso del producto, rendimiento y calidad.
- Se definió un contrato de evento con campos base y propiedades.
- Se trabajó con batching, debounce, `sendBeacon` y reintentos.
- Se ubicaron los puntos de captura en Next.js.
- Se aplicaron consentimiento, limpieza, allowlist, muestreo y separación de entornos.
- El proyecto anterior dejó un `TelemetryService` que envía lotes al backend.

**Frase de enlace para decir en clase**

> En la clase 45 los eventos ya se capturaban en el frontend y se enviaban de forma agrupada, con controles para no enviar datos inadecuados. Hoy damos el siguiente paso: cuando esos eventos llegan, necesitamos tratarlos como datos organizados, poder seleccionar valores, calcular resultados y prepararlos para su almacenamiento.

### Qué añade esta clase

La progresión completa queda así:

```text
class_43: decidir qué observar y cómo transportar los eventos
    ↓
class_45: capturar, proteger y enviar eventos desde el frontend
    ↓
class_46: organizar y transformar los datos con NumPy y Pandas
    ↓
proyecto: validar y guardar los eventos en telemetry_events
```

NumPy aporta la base numérica: arrays, matrices, operaciones y funciones estadísticas. Pandas organiza esos valores en Series y DataFrames. El proyecto de esta clase utiliza la misma idea con eventos de telemetría: validar cada evento, mapear sus campos a columnas y conservar propiedades adicionales en `tags`.

**Pregunta de transición**

> Si `class_43` nos enseñó a definir el evento y `class_45` a capturarlo y enviarlo, ¿qué necesitamos hacer ahora para convertir muchos eventos recibidos en información que podamos revisar y almacenar?

**Respuesta esperada**

> Necesitamos estructurarlos, seleccionar sus campos, transformarlos y resumirlos. Eso es lo que practicaremos con arrays, Series y DataFrames.

## Por qué y para qué de esta lección

### Idea principal para el profesor

Esta lección enseña a pasar de datos numéricos sueltos a estructuras que se pueden organizar, transformar y analizar. NumPy sirve para trabajar con arrays y operaciones numéricas; Pandas se apoya en esas capacidades para representar datos tabulares mediante Series y DataFrames.

La secuencia tiene este sentido:

1. Primero se construyen arrays con NumPy.
2. Después se accede a sus posiciones, se modifican valores y se aplican operaciones a todos sus elementos.
3. Luego esos datos se organizan con Series y DataFrames de Pandas.
4. Finalmente se filtran, ordenan, actualizan y transforman con funciones.
5. El proyecto aplica esa forma de trabajar a eventos de telemetría que deben validarse y almacenarse.

### Por qué importa

En programación y análisis de datos, los valores rara vez llegan perfectamente preparados. Pueden estar en una lista, en varias dimensiones o distribuidos en filas y columnas. Estas herramientas permiten trabajar con conjuntos completos de datos de forma estructurada, en lugar de tratar cada valor de manera aislada.

El material presenta NumPy como una librería para tareas matemáticas eficientes y arrays multidimensionales. Presenta Pandas como una librería para manejar y analizar datos tabulares, con estructuras parecidas a una secuencia etiquetada y a una tabla.

### Para qué se puede utilizar

- NumPy: representar mediciones numéricas, vectores, matrices y conjuntos de valores; calcular sumas, medias, mínimos, máximos y otras transformaciones.
- Pandas Series: trabajar con una secuencia de valores que necesita etiquetas o posiciones identificables.
- Pandas DataFrame: organizar datos relacionados en filas y columnas, como una tabla de datos.
- Funciones y `apply`: repetir una transformación sobre una columna, una fila o cada elemento.
- El proyecto: convertir eventos recibidos en registros organizados, validar cada evento y guardar los datos válidos en `telemetry_events`.

### Ejemplos de vida real que puedes usar al explicarla

Estos ejemplos sirven para dar contexto verbal; la práctica técnica debe seguir los ejemplos y ejercicios incluidos en este resumen:

| Concepto | Ejemplo de vida real | Pregunta para conectar con la clase |
|---|---|---|
| Array 1D | Las temperaturas registradas durante varios días | ¿Cómo guardarías todos los valores y calcularías la media? |
| Array 2D | Una tabla de mediciones de varios sensores en varias horas | ¿Qué representan las filas y las columnas? |
| `np.mean`, `np.min`, `np.max` | Resumir las temperaturas mínima, media y máxima | ¿Necesitamos revisar cada medición manualmente? |
| `np.argmax` y `np.argmin` | Encontrar cuándo se produjo la medición más alta o más baja | ¿Queremos el valor o la posición donde aparece? |
| Series | Las ventas de un producto identificadas por fecha | ¿Qué aporta la etiqueta de cada valor? |
| DataFrame | Un registro de productos con nombre, precio y stock | ¿Qué sería una fila y qué sería una columna? |
| Filtrado y ordenación | Localizar productos con poco stock y ordenarlos por cantidad | ¿Qué datos necesitamos seleccionar antes de actuar? |
| Función personalizada | Aplicar una regla de clasificación a todos los registros | ¿Qué transformación debe repetirse en cada fila? |
| Telemetría | Guardar eventos de una aplicación con tipo, fecha y propiedades | ¿Qué columnas son fijas y qué información puede ir en `tags`? |

Una forma sencilla de presentar la utilidad general es:

> NumPy nos ayuda a operar con conjuntos de números; Pandas nos ayuda a darles una forma de tabla; y el proyecto nos pide aplicar esa organización a datos que llegan desde una aplicación.

## Nota de alcance

Esta guía se basa exclusivamente en los tres notebooks enlazados por los HTML de esta carpeta:

- `intro_to_numpy.json`: arrays 1D y N-dimensionales, operaciones, funciones y 15 ejercicios.
- `intro_to_python_pandas.json`: Series, DataFrames, funciones personalizadas y 8 ejercicios.
- `pandas_exercises_and_solutions.json`: soluciones de los ejercicios de creación, filtrado y actualización.

También se incorporó el proyecto `ai-eng-telemetry-storage` mediante `ai-eng-telemetry-storage_project_asset.json` y `ai-eng-telemetry-storage_project_README.es.md`.

Los HTML originales enlazan con notebooks de Colab, pero esta guía es autosuficiente: el profesor puede impartir la clase leyendo únicamente este archivo. Los bloques de código incluidos aquí proceden de los notebooks; las preguntas, tiempos y orden son estructura docente.

## Por qué usar NumPy y Pandas en lugar de listas y bucles clásicos

**Qué decir (literal)**

> Todo esto podríamos hacerlo con una lista de Python y un bucle `for`. La razón para usar NumPy y Pandas es la que da el propio material: NumPy permite realizar operaciones matemáticas en arrays completos sin necesidad de bucles explícitos en el código, lo que lo hace mucho más rápido y eficiente que la misma funcionalidad implementada directamente sobre Python nativo. Pandas hereda esa misma ventaja: todas sus operaciones y funciones se aplican de forma vectorizada, para mejorar el rendimiento frente a los bucles tradicionales y los iteradores de Python.

**Comparación para mostrar en clase**

Con una lista clásica, sumar 10 a cada elemento exige recorrerla uno por uno:

```python
lista = [1, 2, 3, 4, 5]
resultado = []
for valor in lista:
    resultado.append(valor + 10)
```

Con un array de NumPy, la misma operación se aplica al conjunto completo en una sola línea, sin bucle explícito:

```python
array = np.array([1, 2, 3, 4, 5])
array += 10
```

**Qué preguntar**

> ¿Qué pasaría con el bucle `for` si la lista tuviera un millón de elementos en lugar de cinco?

**Por qué importa para el resto de la clase**

Esta misma ventaja —operar sobre el conjunto completo sin escribir un bucle— es la que usaremos después para calcular estadísticas (`np.mean`, `np.sum`, etc.), transformar columnas enteras de un DataFrame y aplicar funciones sobre filas o columnas con `apply`.

## Objetivos

Al terminar, el grupo podrá:

- Crear arrays de NumPy unidimensionales y multidimensionales.
- Acceder, modificar y operar sobre elementos de un array.
- Aplicar funciones aritméticas, estadísticas, logarítmicas y de redondeo.
- Crear Series y DataFrames de Pandas desde listas, arrays, diccionarios y tuplas.
- Seleccionar y actualizar datos de Series y DataFrames.
- Aplicar funciones a columnas, filas y elementos.
- Resolver ejercicios de creación, filtrado, ordenación y actualización.
- Relacionar el trabajo con datos tabulares con el almacenamiento de eventos de telemetría del proyecto.

## Preparación del profesor

- Tener este resumen abierto como único material principal de la clase.
- Preparar un entorno Python con NumPy y Pandas, o ejecutar los bloques en Colab.
- Usar las soluciones incluidas más abajo después de que el grupo intente los ejercicios.
- Tener a la vista `ai-eng-telemetry-storage_project_README.es.md` para el bloque final.

## Agenda de 75 minutos

| Tiempo | Bloque |
|---|---|
| 0-5 min | Contexto y creación de un array NumPy |
| 5-20 min | Arrays 1D y N-dimensionales |
| 20-30 min | Funciones de NumPy |
| 30-45 min | Series y DataFrames de Pandas |
| 45-55 min | Funciones personalizadas y aplicación sobre datos |
| 55-65 min | Ejercicios de Pandas y contraste con soluciones |
| 65-75 min | Proyecto de almacenamiento de telemetría |

Para 60 minutos, reducir los ejercicios de NumPy a los ejercicios 01, 03, 05, 06 y 15, y los de Pandas a los ejercicios 01, 02, 04 y 06. Mantener el bloque de proyecto en cinco minutos.

## Desarrollo para el profesor

### 1. Entrada a NumPy y arrays 1D (5 minutos)

**Qué decir (literal)**

> Vamos a empezar representando datos numéricos como arrays. Primero crearemos un array unidimensional a partir de una lista y después veremos cómo acceder a sus posiciones, modificar valores y aplicar operaciones al conjunto.

Mostrar este ejemplo:

```python
import numpy as np

array = np.array([1, 2, 3, 4, 5])
array
```

Preguntar:

> ¿Qué posición debemos usar para acceder al tercer elemento?

La práctica del material usa `array[2]`, cambia el segundo elemento con `array[1] = 7`, suma 10 con `array += 10` y calcula el total con `np.sum(array)`.

### 2. Arrays N-dimensionales y operaciones (15 minutos)

**Qué decir (literal)**

> Un array también puede tener más de una dimensión. La dimensión se refleja en la estructura de listas que pasamos a `np.array`; después podemos trabajar con sus valores y con su forma.

Mostrar estos ejemplos de arrays 2D y 3D y pedir al grupo que describa la estructura antes de ejecutarlos:

```python
array_2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
array_2d
```

```python
array_3d = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
array_3d
```

#### Funciones de NumPy, explicadas para la clase

Usar este bloque completo. La variable `arr` contiene `[1, 2, 3, 4, 5]` y permite observar el resultado de cada operación:

```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])

# Operaciones aritméticas elemento a elemento
print("Suma:", np.add(arr, 5))
print("Producto:", np.multiply(arr, 3))

# Transformaciones matemáticas elemento a elemento
print("Logaritmo natural:", np.log(arr))
print("Exponencial:", np.exp(arr))

# Resumen estadístico del array
print("Media:", np.mean(arr))
print("Mediana:", np.median(arr))
print("Desviación estándar:", np.std(arr))
print("Varianza:", np.var(arr))
print("Máximo valor:", np.max(arr))
print("Índice del máximo valor:", np.argmax(arr))
print("Mínimo valor:", np.min(arr))
print("Índice del mínimo valor:", np.argmin(arr))
print("Suma de todos los elementos:", np.sum(arr))
```

**Qué explicar, función por función**

- `np.add(arr, 5)` suma 5 a cada elemento y devuelve un nuevo array.
- `np.multiply(arr, 3)` multiplica cada elemento por 3 y devuelve un nuevo array.
- `np.log(arr)` calcula el logaritmo natural de cada elemento.
- `np.exp(arr)` calcula la exponencial de cada elemento.
- `np.mean(arr)` calcula la media aritmética.
- `np.median(arr)` devuelve la mediana, el valor central al ordenar los datos.
- `np.std(arr)` calcula la desviación estándar, que resume cuánto se separan los valores de la media.
- `np.var(arr)` calcula la varianza, relacionada con la dispersión al cuadrado.
- `np.max(arr)` devuelve el valor más grande.
- `np.argmax(arr)` devuelve el índice donde aparece el valor más grande.
- `np.min(arr)` devuelve el valor más pequeño.
- `np.argmin(arr)` devuelve el índice donde aparece el valor más pequeño.
- `np.sum(arr)` suma todos los elementos.

Para redondear resultados decimales, el material también incluye funciones de redondeo de NumPy. Explicar la diferencia práctica: una función de redondeo cambia la representación numérica del resultado, mientras que las funciones estadísticas resumen los valores del array.

**Qué preguntar**

> ¿Qué diferencia hay entre obtener el máximo con `np.max(arr)` y obtener su posición con `np.argmax(arr)`?

Cerrar con los ejercicios de NumPy 01-08, seleccionando dos o tres según el ritmo: vector nulo, vector de unos, `linspace`, arrays aleatorios, matriz identidad, mínimos y máximos, media, y conversión de listas o tuplas. Para `linspace`, indicar que el ejercicio pide investigar y crear un array de 10 elementos espaciados.

### 3. Operaciones entre arrays (10 minutos)

**Qué decir (literal)**

> Ahora aplicaremos operaciones a arrays completos y cambiaremos su organización. El objetivo es practicar inversión, cambio de tamaño, búsqueda de índices, filtrado, ordenación y operaciones entre dos vectores.

Estos son los ejercicios 09-15 del material, cada uno con la función que el propio material sugiere revisar:

- **Ejercicio 09**: invertir el vector del ejercicio anterior. Función sugerida: `np.flip`.
- **Ejercicio 10**: cambiar un array aleatorio de dimensiones 5x12 a 12x5. Función sugerida: `np.reshape`.
- **Ejercicio 11**: convertir `[1, 2, 0, 0, 4, 0]` en un array y obtener el índice de los elementos distintos de cero. Función sugerida: `np.where`.
- **Ejercicio 12**: convertir `[0, 5, -1, 3, 15]` en un array, multiplicar sus valores por `-2` y obtener los elementos pares.
- **Ejercicio 13**: crear un vector aleatorio de 10 elementos y ordenarlo de menor a mayor. Función sugerida: `np.sort`.
- **Ejercicio 14**: generar dos vectores aleatorios de 8 elementos y aplicar suma, resta y multiplicación entre ellos.
- **Ejercicio 15**: convertir la lista `[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]` en un array y transformarlo en una matriz con filas de 3 columnas.

**Cómo se usan las funciones sugeridas** (demostración con un vector de ejemplo, sin depender de ningún archivo externo):

```python
vector = np.array([1, 2, 3, 4, 5])

print(np.flip(vector))             # invierte el orden de los elementos
print(np.reshape(vector, (5, 1)))  # cambia la forma sin cambiar los datos
print(np.where(vector == 0))       # devuelve los índices que cumplen una condición
print(np.sort(vector))             # ordena los elementos de menor a mayor
```

**Qué preguntar**

> ¿Qué diferencia hay entre invertir un array con `np.flip` y ordenarlo con `np.sort`?

### 4. Series y DataFrames (15 minutos)

**Qué decir (literal)**

> Pandas añade estructuras etiquetadas para trabajar con datos. Una Series es una estructura unidimensional; un DataFrame organiza datos en dos dimensiones, con filas y columnas.

Mostrar la creación de una Series:

```python
import pandas as pd

serie = pd.Series([1, 2, 3, 4, 5])
serie
```

Luego explicar el acceso por etiqueta y posición, la actualización del segundo valor, la suma de 10 y la suma total:

```python
serie = pd.Series([1, 2, 3, 4, 5], index = ["a", "b", "c", "d", "e"])

print(serie["c"])  # acceso por etiqueta
print(serie[2])     # acceso por posición
serie["b"] = 7
serie += 10
print(serie)
print(serie.sum())
```

Para DataFrame, enseñar la construcción desde un diccionario:

```python
data = {
    "col A": [1, 2, 3],
    "col B": [4, 5, 6],
    "col C": [7, 8, 9]
}

dataframe = pd.DataFrame(data, index = ["a", "b", "c"])
dataframe
```

Recorrer las operaciones del material con este ejemplo:

```python
print(dataframe["col A"])       # todos los datos de una columna
print(dataframe.loc["a"])       # todos los datos de una fila
print(dataframe.loc["a", "col A"])  # un elemento concreto

dataframe["col D"] = [10, 11, 12]    # nueva columna
dataframe.loc["d"] = [13, 14, 15, 16]  # nueva fila
dataframe["col A"] *= 10             # operar sobre una columna
print(dataframe.sum())                # suma por columna
```

Explicar que `loc` selecciona mediante etiquetas, que una columna se obtiene con su nombre entre corchetes y que las operaciones vectorizadas se aplican al conjunto de valores sin escribir un bucle explícito.

**Qué preguntar**

> ¿Qué estructura usarías para una sola secuencia etiquetada y cuál para varias columnas relacionadas?

### 5. Funciones personalizadas y `apply` (10 minutos)

**Qué decir (literal)**

> Además de las funciones incluidas en Pandas, podemos definir una función y aplicarla a una columna, una fila o a todos los elementos. Una función personalizada permite expresar una transformación que no viene preparada como operación estándar.

Usar este ejemplo autosuficiente, que resume los tres usos incluidos en el material:

```python
def duplicar(valor):
    return valor * 2

dataframe["col A"] = dataframe["col A"].apply(duplicar)  # sobre una columna
totales_por_fila = dataframe.apply(sum, axis=1)            # sobre cada fila
valores_transformados = dataframe.applymap(duplicar)       # sobre cada elemento
```

Explicar `apply(duplicar)` como una aplicación a cada valor de una Series, `axis=1` como recorrido fila a fila de un DataFrame y `applymap(duplicar)` como aplicación elemento a elemento. La versión anónima equivalente para una transformación simple es:

```python
dataframe["col B"] = dataframe["col B"].apply(lambda valor: valor * 2)
```

Una función `lambda` es una función anónima escrita en una sola expresión. Preguntar qué forma usarían si necesitaran reutilizar la transformación varias veces: la función con nombre `duplicar`.

### 6. Ejercicios y soluciones (10 minutos)

Pedir que el grupo resuelva primero estos ejercicios, y comparar después con la solución de cada uno (ya incluida aquí, no hace falta abrir ningún archivo aparte). Todas las soluciones fijan la aleatoriedad con `np.random.seed(42)` al inicio:

```python
import numpy as np
import pandas as pd

np.random.seed(42)
```

**Ejercicio 01: crear una Series desde una lista, un array de NumPy y un diccionario**

```python
l = [1, 2, 3, 4, 5, 6]
serie = pd.Series(l)

array = np.array([1, 2, 3, 4, 5, 6])
serie = pd.Series(array)

d = {"A": 1, "B": 2, "C": 3}
serie = pd.Series(d)
```

**Ejercicio 02: crear un DataFrame desde un array de NumPy, un diccionario y una lista de tuplas**

```python
array = np.random.randint(1, 10, size = (5, 5))
dataframe = pd.DataFrame(array)

d = {
    "A": np.random.randint(10, 100, size = 5),
    "B": np.linspace(1, 10, 5),
    "C": np.random.randn(5)
}
dataframe = pd.DataFrame(d)

t = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
dataframe = pd.DataFrame(t)
```

**Ejercicio 03: construir un DataFrame a partir de dos Series**

```python
s1 = pd.Series([1, 2, 3, 4, 5])
s2 = pd.Series([4, 5, 6, 7, 8])

# Método 1
dataframe = pd.DataFrame({"ser1": s1, "ser2": s2})

# Método 2
dataframe = pd.concat([s1, s2], axis = 1)

# Método 3
s1.name = "ser1"
s2.name = "ser2"
dataframe = s1.to_frame().join(s2)
```

**Ejercicio 04: seleccionar las posiciones de la primera serie que están en la segunda**

```python
# Con Pandas
filtering_results = s1.isin(s2)
indices = s1[filtering_results].index

# Con NumPy
indices = np.where(s1.isin(s2))
```

**Ejercicio 05: listar los elementos no comunes entre ambas series**

```python
unique_s1 = s1[~s1.isin(s2)]
unique_s2 = s2[~s2.isin(s1)]
unique_elements = np.concatenate([unique_s1, unique_s2])
```

**Ejercicio 06: crear un DataFrame aleatorio de 5 columnas y 10 filas, y ordenar una columna**

```python
df = pd.DataFrame(np.random.rand(10, 5) * 10, columns = [f"Col {i}" for i in range(5)])
df.sort_values("Col 0")
```

**Ejercicio 07: renombrar las 5 columnas con el formato `N_column`**

```python
df.columns = [f"{i}_column" for i in range(5)]
```

**Ejercicio 08: modificar el índice de las filas del DataFrame anterior**

```python
df.index = [f"{i}_row" for i in range(10)]
```

**Qué preguntar**

> En el ejercicio 04, ¿qué diferencia hay entre resolverlo con `isin` de Pandas y con `np.where`?

### 7. Proyecto: almacenamiento de telemetría (10 minutos)

**Resumen del brief**

El proyecto parte de un `TelemetryService` que ya envía lotes a un stub. El objetivo es reemplazarlo en el backend por un endpoint real que valide eventos individualmente con `TelemetryEvent`, persista los válidos en Supabase mediante una sola operación bulk y devuelva `received`, `stored` y `rejected`. El frontend no debe cambiar.

La tabla `telemetry_events` tiene ocho columnas: `id`, `timestamp`, `service`, `event_type`, `level`, `value`, `message` y `tags`. El proyecto pide índices para `timestamp` y `event_type`, además de un índice GIN para `tags`, y exige que los eventos sean inmutables.

**Cómo conectar la clase con el proyecto**

> En NumPy y Pandas hemos trabajado con arrays, filas, columnas, filtros y valores numéricos. En el proyecto, los eventos forman un conjunto de datos que debe validarse, transformarse y consultarse de manera consistente. La tabla final organiza cada evento en columnas fijas y conserva propiedades adicionales en `tags`.

**Mini plan en pseudocódigo**

```text
leer un lote con events
para cada evento del lote:
    validar el evento individualmente con TelemetryEvent
    si es válido:
        mapearlo a una fila de telemetry_events
    si es inválido:
        aumentar rejected y continuar
insertar todas las filas válidas en una sola operación
devolver received, stored y rejected
verificar eventos técnicos y de negocio en Supabase
```

Preguntas de cierre del proyecto:

- ¿Por qué un evento inválido no debe cancelar todo el lote?
- ¿Qué datos se guardan en `tags`?
- ¿Qué diferencia hay entre un insert por evento y un bulk insert?
- ¿Por qué el frontend debe permanecer sin cambios?

## Recorte y extensión

### Versión de 60 minutos

- NumPy: explicación breve de arrays 1D y 2D, funciones principales y cinco ejercicios seleccionados.
- Pandas: Series, DataFrame y cuatro ejercicios seleccionados.
- Soluciones: comparar solo los ejercicios realizados.
- Proyecto: presentar el flujo de validación individual y bulk insert.

### Versión de 75 minutos

- Ejecutar ejemplos de arrays 1D, 2D y 3D.
- Resolver ejercicios de NumPy 09-15 sobre operaciones entre arrays.
- Resolver los ocho ejercicios de Pandas antes de abrir las soluciones.
- Dedicar los diez minutos completos al mapeo del proyecto y sus criterios de evaluación.

## Checklist de cierre

- [ ] Se creó y modificó un array NumPy.
- [ ] Se practicaron arrays de más de una dimensión.
- [ ] Se aplicaron funciones aritméticas y estadísticas.
- [ ] Se creó una Series y un DataFrame desde distintas fuentes.
- [ ] Se practicó filtrado, ordenación y actualización.
- [ ] Se compararon ejercicios con sus soluciones.
- [ ] Se explicó la validación parcial y el bulk insert del proyecto.

## Cierre sugerido

> Hoy pasamos de arrays numéricos a estructuras tabulares con Series y DataFrames. La práctica final conecta esas operaciones con un caso real: recibir eventos, validar cada registro, conservar los válidos y almacenarlos en una tabla consultable sin modificar el frontend.