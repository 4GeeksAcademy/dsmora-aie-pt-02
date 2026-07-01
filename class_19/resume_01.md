Aprendiendo a programar con Python
----------------------------------

Volver arriba

[¿Por qué python?](#por-que-python)

[Variables](#variables)

[Asignándole un valor a las variables](#asignandole-un-valor-a-las-variables)

[Tipos de datos](#tipos-de-datos)

[Operaciones](#operaciones)

[Funciones](#funciones)

[Declarar una Función](#declarar-una-funcion)

[Parámetros y alcance de la Función](#parametros-y-alcance-de-la-funcion)

*   [Variables Locales](#variables-locales)
    
*   [Variables Globales](#variables-globales)
    

[Operaciones lógicas](#operaciones-logicas)

[Controla el Flujo de Tú Código](#controla-el-flujo-de-tu-codigo)

[Switch](#switch)

[While](#while)

[For loop](#for-loop)

[For..in](#forin)

[Entonces ... dime, ¿te gustó la programción?](#entonces-dime-te-gusto-la-programcion)

[](#por-que-python)¿Por qué python?
-----------------------------------

[](#python-es-el-primer-lenguaje-que-debieras-aprender)Python es el primer lenguaje que debieras aprender, pero evidentente no el único.

*   MIT decidió enseñar python como primer lenguaje porque su sintaxis previene muchos errores, especialmente porque tiene identación y no puntos y comas.

[](#variables)Variables
-----------------------

[Haz clic aquí para abrir la demo en otra ventana](https://www.youtube.com/embed/Q-eob0WBKs0)

[](#las-variables-no-son-un-concepto-nuevo-cualquier-q)Las variables no son un concepto nuevo, cualquier que sepa matemáticas está familiriarizado con el condepto de variables.

[](#1edad-24)

`1edad = 24`

[](#que-es-python)![qué es python](https://raw.githubusercontent.com/breatheco-de/content/master/src/assets/images/ecb49b67-f513-49b3-bd4a-dd7cc44e9bce.gif?raw=true)

[](#casi-con-cualquier-lenguaje-de-programacion-puedes)Casi con cualquier lenguaje de programación puedes crear tantas variables como quieras o necesites. Para empezar, en python debes **declarar el nombre de esa variable** con un nombre _único_ (relativo al valor o lo que reciba).

[](#el-nombre-de-la-variable-es-la-manera-mas-efectiva)El **nombre de la variable** es la manera más efectiva de describir el contenido de una variable, úsalo con sabiduría. Es importante escoger un nombre que claramente te indique (a ti y a otros programadores) sobre los datos que están siendo almacenados en la variable. Si escogemos un nombre malo o ambigüo, nuestro código será casi imposible de entender, ergo se vuelve inutilizable. Por ejemplo digamos que le cambiamos el nombre a nuestra variable "edad" a "a":

[](#1a-24)

`1a = 24`

[](#como-puedes-ver-el-nuevo-nombre-de-la-variable-no-)Como puedes ver, el nuevo nombre de la variable no nos dice nada sobre el dato que está siendo almacenado y por qué lo están usando.

[](#escoger-el-nombre-de-tu-variable-es-muy-importante)Escoger el nombre de tu variable es muy importante, así que por favor no uses nombres genéricos ¡Sé descriptivo! Un nombre vago hará difìcil de comprender el propósito de la variable, especialmente para otros programadores (incluyéndote a ti).

[](#asignandole-un-valor-a-las-variables)Asignándole un valor a las variables
-----------------------------------------------------------------------------

[](#como-desarrolladores-podemos-establecer-el-valor-d)Como desarrolladores, podemos establecer el valor de una variable usando el operador `=`. No tienes que establecer el valor de una variable cuando la declaras por primera vez. Puedes establecer o re-establecer (sobreescribir) el valor tantas veces como quieras y cuando quieras. El valor siempre el último que estableciste. A continuación hay algunos ejemplos sobre cómo establecer valores a las variables:

[](#1a-24-2a-25-3a-80)

`1a = 24 2a = 25 3a = 80`

[](#los-valores-de-las-variables-estan-sujetos-a-cambi)Los valores de las variables están sujetos a cambio a largo del tiempo. Para recuperar el valor de una variables puedes imprimir su valor en la pantalla en cualquier momento. Cada lenguaje tiene sus propios métodos para imprimir. En python usamos `print`.

[](#pythonejecutarloading-consola)

Python

Ejecutar

1

2

3

4

5

6

edad = 24

print(edad)

# podemos actualizar el valor de la variable "edad" en cualquier momento

edad = 30

print(edad)

Consola

[](#tipos-de-datos)Tipos de datos
---------------------------------

[](#las-variables-pueden-tener-diferentes-tipos-de-val)Las variables pueden tener diferentes tipos de valores:

**Tipos-de-Datos**

**Posibles Valores**

**Descripción**

Booleano

Verdadero | Falso

Los booleanos están destinados para operaciones lógicas. Si le preguntas a una computadora algo como: "¿X es igual a 3?" Responderá con un booleano (verdadero o falso).

String

Cualquier serie de caracteres

Los strings son la única forma en que tenemos que almacenar palabras (series de caracteres). Nota: los strings deben estar encerradas entre comillas.

Número

Solo números

Números enteros, números negativos, números decimales, decimales, etc. Todos los tipos posibles de números.  

Indefinido

El vacío

Cuando una variable no tiene un valor asignado, queda indefinida.

Arreglo

Una lista con cualquier tipo de valores.

Una sucesión de cualquier tipo de valores. Pueden ser tipos mixtos de valores; por ejemplo: \[2, 3, ‘Word’, 2, 1, null, 232, 5, 3, 23, 234, 5, ‘hello’\].

Objetos

Cualquier objeto

Puedes crear tus propios tipos de datos con operaciones más complejas. Hablaremos más sobre esto más adelante.

Nulo

Sólo nulo

Se utiliza para especificar cuándo la base de datos o cualquier otra función no devuelve nada.

[](#pythonejecutarloading-consola-1)

Python

Ejecutar

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

# Variables y sus tipos

miPrimerBooleano = True  # Booleano

miPrimerEntero = 35  # Entero

miPrimerFlotante = 2323.4545  # Flotante (número con decimales)

miPrimeraCadena = 'Hola Mundo'  # Cadena

miPrimerObjeto = {'name': 'Ramon', 'Age': 32}  # Diccionario con 2 pares clave-valor

miPrimerArreglo = \[23, 'Hola', 8.54, None, 544\]  # Lista de 5 elementos de diferentes tipos

miPrimerNulo = None  # NoneType representa nulo en Python

miPrimerIndefinido = None  # Python utiliza None para representar valores indefinidos o nulos

# Imprimiendo las variables en la consola

print(miPrimerBooleano)

print(miPrimerEntero)

print(miPrimerFlotante)

print(miPrimerFlotante + miPrimerEntero)  # Operación aritmética

Consola

[](#operaciones)Operaciones
---------------------------

[](#que-operaciones-puedo-hacer-con-las-variables-depe)¿Qué operaciones puedo hacer con las variables? Dependiendo del tipo de datos tienes algunas posibilidades diferentes:

*   Los números son fáciles - puedes hacer cualquier operación matemática que desees.
*   Las cadenas se pueden concatenar (fusionar), dividir, convertir a mayúsculas o minúsculas, etc.
*   No se puede hacer mucho con los tipos de datos nulos, booleanose indefinidos.
*   Hablaremos de Arreglos y Objetos en una otra sección. Requieren de mucha más atención.

[](#funciones)Funciones
-----------------------

[](#las-funciones-son-pedazos-de-codigo-que-se-pueden-)Las funciones son pedazos de código que se pueden reutilizar varias veces durante el tiempo de ejecución, independiente de su posición en el código. Hay cientos de razones para usar funciones, pero aquí están las 2 más importantes:

*   Divide y conquista: siempre es más fácil dividir tus problemas en varios problemas más pequeños. Esto se convertirá en tu mayor desafío a la hora de resolver problemas complejos. Las funciones serán tus mejores herramientas para la abstracción.
*   Reutilización: cualquier desarrollo normal tomará al menos 5,000 líneas de código. Es redundante e ineficiente seguir escribiendo el mismo código una y otra vez.

[](#declarar-una-funcion)Declarar una Función
---------------------------------------------

[](#para-declarar-una-funcion-en-python-comienzas-con-)Para declarar una función en Python, comienzas con la palabra clave `def`, seguida del nombre que deseas darle a la función.

[](#luego-especificas-los-parametros-entradas-que-la-f)Luego, especificas los parámetros (entradas) que la función aceptará dentro de paréntesis.

[](#a-continuacion-comienzas-un-nuevo-bloque-de-codigo)A continuación, comienzas un nuevo bloque de código con sangría, donde escribes el código que la función debe ejecutar. Una vez que hayas terminado el código de la función, simplemente detienes la sangría.

[](#nota-para-devolver-un-valor-desde-la-funcion-utili)**Nota:** Para devolver un valor desde la función, utilizas la palabra clave `return`, seguida del valor que deseas retornar. Puedes colocar la sentencia `return` en cualquier parte dentro del bloque de código de la función, y esta se ejecutará, finalizando la función y devolviendo el valor especificado.

> [](#aqui-tienes-un-ejemplo)Aquí tienes un ejemplo:

[](#1def-multiplicar-param1-param2-2-resultado-param1-param2-3-retur)

`1def multiplicar(param1, param2): 2    resultado = param1 * param2 3    return resultado  # Así es como se devuelve un valor desde la función`

[](#parametros-y-alcance-de-la-funcion)Parámetros y alcance de la Función
-------------------------------------------------------------------------

[](#el-alcance-de-una-variable-determina-donde-esta-di)El alcance de una variable determina dónde está disponible esa variable para ser utilizada. Hay dos tipos principales de alcances:

### [](#variables-locales)Variables Locales

[](#una-variable-local-solo-esta-disponible-dentro-del)Una variable local sólo está disponible dentro del alcance de las llaves más cercanas. Por ejemplo, las variables que se pasan como parámetros a funciones, solo están disponibles dentro del contenido de esa función en particular.

### [](#variables-globales)Variables Globales

[](#si-declaras-una-variable-al-comienzo-de-tu-codigo-)Si declaras una variable al comienzo de tu código, estará disponible lo largo de todo el código, incluso durante el contenido de cualquier función en particular.

[](#pythonejecutarloading-consola-2)

Python

Ejecutar

1

2

3

4

5

6

7

8

# Definir la variable global

message = "Hello"

def print\_message():

    # Esta funcion utiliz la variable global "message"

    print(message)

print\_message()  # Salida: Hello

Consola

[](#operaciones-logicas)Operaciones lógicas
-------------------------------------------

[](#las-computadoras-piensan-todo-en-blanco-o-negro-to)Las computadoras piensan todo en blanco o negro. Todo es verdadero o falso. Todas las decisiones en una computadora se reducen a un simple **booleano**. Puedes preparar una computadora para resolver problemas particulares si escribes un código que haga las preguntas adecuadas para resolver ese problema.

[](#por-ejemplo-si-quiero-una-computadora-para-dar-dul)Por ejemplo, si quiero una computadora para dar dulces sólo a niños mayores de 13 años de edad, puedo indicarle a la computadora que pregunte:

[](#la-edad-de-este-nino-es-mayor-de-13-anos-si-o-no)**¿La edad de este niño es mayor de 13 años? ¿Sí o no?**

[](#en-python-puedes-indicarle-a-la-computadora-que-re)**En python, puedes indicarle a la computadora que realice las siguientes operaciones lógicas:**

**Operación**

**Sintaxis**

**Ejemplos**

Igual a

\==

Es 5 == 5? True!  
Es 5 == 4? False!  
Es 5 == '5'? True!

No Igual a

!=

Es 5 != 5? False!  
Es 5 != '5'? False!  
Es 1 != 'Hello' True!

Mayor que

\>

Es 5 > 5? False!  
Es 6 > 3? True!

Menos que

<

Es 6 < 12? True

Mayor o igual

\>=

Es 6 <= 6? True  
Es 3 <= 6? True

Menor o igual

<=

Tienes la idea 🙂

[](#para-crear-operaciones-realmente-utiles-puedes-com)Para crear operaciones realmente útiles, puedes combinar varias operaciones en la misma pregunta usando AND, OR y NOT (y, o o no respectivamente).

[](#puedes-agrupar-las-operaciones-logicas-entre-paren)Puedes agrupar las operaciones lógicas entre paréntesis y también usar paréntesis anidados para realizar varias operaciones al mismo tiempo.

**Operación**

**Sintaxis**

**Ejemplos**

AND

`and`

Con AND, ambos lados TIENEN QUE SER TRUE para que todo se convierta en verdadero.  
Es (5 == 5 and 3 > 1) ? True!  
Es ('Ramon' == 'Pedro' and 2 == 2) ? False!

OR

`or`

Es ('Oscar' != 'Maria' or 2 != 2)? True!  
Es (5 == '5' and 'Ramon' != 'Pedro') or (2 == 2)? True!

NOT

`not`

NOT será exactamente lo contrario del resultado del operador lógico:  
Es not (5 > 5)? True!  
Is not (True)? False!

[](#controla-el-flujo-de-tu-codigo)Controla el Flujo de Tú Código
-----------------------------------------------------------------

[](#bien-ahora-es-cuando-todo-empieza-a-ponerse-divert)Bien, ahora es cuando todo empieza a ponerse divertido! Para controlar el flujo de tu aplicación, tienes varias opciones y las utilizarás cada día. Por lo tanto, debes sentirte cómodo usándolas.

### [](#ifelse)If…else…

[](#la-primera-herramienta-que-tienes-es-el-condiciona)La primera herramienta que tienes es el condicional `if ... else`. Es muy fácil. Puedes decirle a la computadora que omita cualquier parte de tu código dependiendo del valor actual de tus variables.

[](#la-instruccion-if-te-permite-ejecutar-un-fragmento)La instrucción `if` te permite ejecutar un fragmento de código si se cumplen ciertas condiciones (o si son verdaderas). La declaración "else" ejecutará un fragmento de código alternativo en caso de que la condición sea falsa.

[](#1if-number-18-2-print-hello-3else-4-print-good-bye)

`1if number < 18: 2     print("Hello"); 3else: 4     print("Good bye!")`

[](#switch)Switch
-----------------

[](#python-no-cuenta-con-la-capacidad-de-hacer-switch-)Python no cuenta con la capacidad de hacer `switch` como otros lenguajes (js, c#, etc.)

[](#while)While
---------------

[](#es-posible-hacer-un-bucle-de-un-segmento-de-su-cod)Es posible hacer un bucle de un segmento de su código tantas veces como deseeso necesites Los bucles son una de las herramientas más importantes para los desarrolladores en estos días.

[](#imagina-que-estas-dentro-de-un-ascensor-el-ascenso)Imagina que estás dentro de un ascensor: el ascensor debe girar en bucle por los pisos hasta que alcance el piso específico que deseas.

[](#un-bucle-while-ejecutara-un-bloque-de-codigo-siemp)Un bucle `while` ejecutará un bloque de código siempre que una condición sea verdadera. Una vez que la condición sea falsa, el bucle dejará de ejecutar el bloque de código.

[](#pythonejecutarloading-consola-3)

Python

Ejecutar

1

2

3

4

5

6

7

sum = 0;

number = 1;

while number <= 50:

  sum += number

  number += 1

print("Sum = " + sum)

Consola

[](#for-loop)For loop
---------------------

[](#for-es-similar-a-while-con-la-unica-diferencia-de-)`For` es similar a `while,` con la única diferencia de que debes especificar la condición para que se detenga desde un principio. Por esa razón, `for` es un poco más organizado y más fácil de entender.

[](#nota-cuando-realices-un-bucle-asegurate-de-que-la-)Nota: cuando realices un bucle, asegúrate de que la declaración finalmente devuelva falso para evitar un bucle infinito. En un bucle infinito, el código se ejecuta indefinidamente y hará que tu navegador se bloquee.

[Haz clic aquí para abrir el video en una nueva ventana](https://www.youtube.com/embed/TSMzvFwpE_A)

[](#1for-i-in-range-10-2-print-this-is-number-i-3)

`1for i in range(10): 2  print("This is number" + " " + i) 3`

[](#forin)For..in
-----------------

[](#los-bucles-for-in-pueden-usarse-para-recorrer-con-)Los bucles `For… in` pueden usarse para recorrer con un bucle las propiedades de un objeto. Dentro de los paréntesis, puedes establecer cualquier nombre para representar la información dentro del objeto, y luego incluir el nombre del objeto:

[](#1for-variable-in-object-br-2bloque-de-código-a-ejecutarse-3)

`1for (variable in object)<br> { 2bloque de código a ejecutarse 3}`

[](#pythonejecutarloading-consola-4)

Python

Ejecutar

1

2

3

4

5

6

7

8

9

perro = {

  "especie": "Gran Danés",

  "tamaño": "Extra Grande",

  "edad": 3,

  "nombre": "Rocky"

}

for items in perro:

  print(perro\[items\])

Consola

[](#entonces-dime-te-gusto-la-programcion)Entonces ... dime, ¿te gustó la programción?
--------------------------------------------------------------------------------------

[](#la-programacion-es-como-taco-bell-siempre-se-usan-)La programación es como Taco Bell: siempre se usan los mismos ingredientes pero se mezclan de diferentes maneras. Sabes cómo escribir código, pero ... ¿sabes cómo resolver problemas reales?

[](https://github.com/breatheco-de/content/blob/master/src/content/lesson/learning-to-code-in-python.es.md)

Condicionales en la programación en Python
------------------------------------------

Volver arriba

[Introducción a los condicionales en Python](#introduccion-a-los-condicionales-en-python)

[Primero veamos ¿qué es una expresión lógica en Python?](#primero-veamos-que-es-una-expresion-logica-en-python)

[¿Qué tipo de condiciones/preguntas podemos usar/hacer?](#que-tipo-de-condicionespreguntas-podemos-usarhacer)

[Operadores lógicos en Python](#operadores-logicos-en-python)

[Operadores `AND` y `OR` en Python](#operadores-and-y-or-en-python)

[If...else en Python](#ifelse-en-python)

[El `switch` en Python](#el-switch-en-python)

[Conclusión](#conclusion)

[](#introduccion-a-los-condicionales-en-python)Introducción a los condicionales en Python
-----------------------------------------------------------------------------------------

[](#dominar-el-uso-de-las-condiciones-es-una-de-las-5-)Dominar el uso de las condiciones es una de las 5 habilidades fundamentales para construir algoritmos:

1.  Variables.
2.  Condicionales.
3.  Listas.
4.  Bucles (Loops).
5.  Funciones.

[](#el-uso-de-condicionales-es-la-unica-forma-en-que-l)El uso de _condicionales_ es la única forma en que los desarrolladores tienen para decirle a la computadora cómo tomar decisiones en tiempo real.

[](#digamos-que-estamos-construyendo-un-programa-para-)Digamos que estamos construyendo un programa para ayudarnos a elegir qué ponernos y odiamos el color azul, podemos decirle a la computadora que evite el azul usando una condición como esta:

[](#1if-color-blue-2-haz-algo-3else-4-haz-otra-cosa)

`1if color == 'blue': 2    # Haz algo 3else: 4    # Haz otra cosa`

[](#condicionales)![Condicionales](https://raw.githubusercontent.com/breatheco-de/content/master/src/assets/images/e73b673e-d744-45a7-a1ed-61a1dae49560.png?raw=true)

> [](#el-uso-de-switch-no-esta-disponible-en-python)👉 El uso de `switch` no está disponible en Python

[](#primero-veamos-que-es-una-expresion-logica-en-python)Primero veamos ¿qué es una expresión lógica en Python?
---------------------------------------------------------------------------------------------------------------

[](#la-forma-mas-facil-de-entender-expresiones-logicas)La forma más fácil de entender expresiones lógicas (al menos para esta lectura en particular), es pensar en ellas como en preguntas que le puedes hacer al computador sobre nuestras variables, por ejemplo:

1.  `if user_age > 21:`
2.  `if day == "tuesday":`
3.  `if car_model == "toyota" and number_of_tires == 6:`

[](#para-hacer-una-pregunta-o-excusar-condicionalmente)Para hacer una pregunta, o excusar condicionalmente un conjunto particular de líneas, primero necesitas tener datos (información) almacenados en variables útiles, arriba tenemos las variables `user_age`, `day`, `car_model` y `number_of_tires`.

[](#si-no-tenemos-la-informacion-prealmacenada-en-vari)Si no tenemos la información prealmacenada en variables no podemos hacer ninguna pregunta, ¡todo es cuestión de estrategia y planificación!

[](#por-ejemplo-si-tenemos-la-edad-del-usuario-almacen)Por ejemplo, si tenemos la edad del usuario almacenada en una variable `edad` entonces, y solo entonces, podremos codificar algo como:

[](#1-se-utiliza-dos-veces-igual-cuando-quieres-comparar-en-lugar-de)

`1# Se utiliza dos veces igual (==) cuando quieres comparar en lugar de asignar el valor 2if edad == 25: 3    print("¡Eres mayor de edad!")`

[](#que-tipo-de-condicionespreguntas-podemos-usarhacer)¿Qué tipo de condiciones/preguntas podemos usar/hacer?
-------------------------------------------------------------------------------------------------------------

[](#el-ejemplo-anterior-era-una-condicion-simple-pero-)El ejemplo anterior era una condición simple, pero en la vida real elegir qué ponerse implica una combinación de varias condiciones para tomar la decisión final, por ejemplo: Veamos este algoritmo que te dice si tienes gripe.

[](#algoritmo-de-la-gripe)![Algoritmo de la gripe](https://raw.githubusercontent.com/breatheco-de/content/master/src/assets/images/03ed6b76-0ee0-4b04-bd45-0fb58ae6f800.jpeg?raw=true)

[](#si-desea-representar-este-algoritmo-en-python-se-v)Si desea representar este algoritmo en Python, se verá así:

[](#pythonejecutarloading-consola)

Python

Ejecutar

1

2

3

4

5

6

7

8

9

10

siento\_que\_me\_atropello\_un\_tren = True

me\_atropello\_un\_tren = False

if siento\_que\_me\_atropello\_un\_tren == True:

    if me\_atropello\_un\_tren == True:

        print("No tienes gripe")

    else:

        print("Tienes gripe")

else:

    print("No tienes gripe")

Consola

[](#basicamente-este-algoritmo-tiene-dos-variables-a-c)Básicamente, este algoritmo tiene dos variables a considerar: `siento_que_me_atropello_un_tren` y `me_atropello_un_tren`. Nuestro trabajo como desarrolladores es sentarnos y tratar de preparar una estrategia para llegar a un algoritmo que resuelva un problema.

[](#operadores-logicos-en-python)Operadores lógicos en Python
-------------------------------------------------------------

[](#para-hacer-una-pregunta-tenemos-las-siguientes-com)Para hacer una pregunta, tenemos las siguientes comparaciones: `==`, `>`, `<`, `!=`, `is None`, `is not None`, `in`:

Operador

Ejemplo

Descripción

`==`

`if a == b`

Si el valor de la variable `a` es **igual** a `b`

`<`

`if a < b`

Si el valor de `a` es **menor** que `b`

`>`

`if a > b`

Si el valor de `a` es **mayor** que `b`

`!=`

`if a != b`

Si el valor de `a` es **diferente** de `b`

`is not None`

`if a is not None`

Si `a` es diferente de `None`

`is None`

`if a is None`

Si el valor de `a` es igual a `None`

`in`

`if name in ['bob','maria','nancy']`

Si el valor de `name` está contenido dentro de la lista de nombres

[](#operadores-and-y-or-en-python)Operadores `AND` y `OR` en Python
-------------------------------------------------------------------

[](#otra-forma-de-escribir-el-algoritmo-es-combinar-pr)Otra forma de escribir el algoritmo es combinar preguntas en la misma condición utilizando los operadores `AND` y `OR`:

[](#pythonejecutarloading-consola-1)

Python

Ejecutar

1

2

3

4

5

6

7

siento\_que\_me\_atropello\_un\_tren = True

me\_atropello\_un\_tren = False

if siento\_que\_me\_atropello\_un\_tren and me\_atropello\_un\_tren:

    print("No tienes gripe")

elif siento\_que\_me\_atropello\_un\_tren:

    print("Tienes gripe")

Consola

[](#como-puedes-ver-usamos-elif-por-primera-vez-para-c)Como puedes ver, usamos `elif` por primera vez, para codificar más rápido. Otro truco que puedes usar es el siguiente:

Original

Equivalente

En lugar de `if siento_que_me_atropello_un_tren == true`

escribes `if siento_que_me_atropello_un_tren`

En lugar de `if me_atropello_un_tren == false`

escribes `if not me_atropello_un_tren`

[](#ifelse-en-python)If...else en Python
----------------------------------------

[](#tambien-puedes-usar-la-expresion-else-para-referir)También puedes usar la expresión `else` para referirte a la negación de la primera condición:

[](#1if-color-azul-2-descarta-esta-prenda-de-vestir-3else-4-guárdala)

`1if color "azul": 2    # Descarta esta prenda de vestir 3else: 4    # Guárdala en mi armario 5   6edad = 12 7if (edad > 18): 8    print("Es mayor de edad") 9else: 10    print("No es mayor de edad")`

[](#tambien-puedes-anidar-condiciones-ifelse-una-sobre)También puedes anidar condiciones if...else una sobre la otra, de esta forma:

[](#1if-edad-16-2-no-puedes-hacer-nada-3elif-age-18-4-a-estas-altura)

`1if edad < 16:  2    # No puedes hacer nada 3elif age < 18: 4    # A estas alturas, ya sabemos que es mayor de 15 porque si no, no hubiese ingresado a la primera condición 5elif age < 21: 6    # Si el algoritmo ingresa aquí, sabemos que es mayor de 17 7else: 8    # Si el algoritmo ingresa aquí, sabemos que es mayor de 20`

[](#aqui-hay-otro-ejemplo-que-ejecuta-un-algoritmo-par)Aquí hay otro ejemplo que ejecuta un algoritmo para saber si un número tiene centenas:

[](#pythonejecutarloading-consola-2)

Python

Ejecutar

1

2

3

4

5

6

7

8

9

10

11

12

valor = 14

if valor < 10:

    print("El valor es una unidad")

elif valor < 100:

    print("El valor es una decena")

elif valor < 1000:

    print("El valor es una centena")

elif valor < 10000:

    print("El valor es una unidad de mil")

else:

    print("El valor es un número más allá de los miles")

Consola

> [](#cambia-el-valor-de-la-variable-valor-para-que-veas)Cambia el valor de la variable `valor` para que veas como funciona con los diferentes valores.

[](#el-switch-en-python)El `switch` en Python
---------------------------------------------

[](#python-no-tiene-una-sentencia-switch-como-otros-le)Python no tiene una sentencia `switch` como otros lenguajes de programación.

[](#conclusion)Conclusión
-------------------------

[](#hay-que-saber-que-preguntas-hacer-el-ejemplo-anter)Hay que saber qué preguntas hacer. El ejemplo anterior era una condición simple, pero en la vida real, elegir qué hacer implica una combinación de varias condiciones para tomar la decisión final, por ejemplo:

[](#veamos-este-algoritmo-que-le-dice-a-una-computador)Veamos este algoritmo que le dice a una computadora cómo decidir qué ponerse durante el día de San Valentín:

[](#que-ponerme-en-san-valentin)![Qué ponerme en San Valentín](https://raw.githubusercontent.com/breatheco-de/content/refs/heads/master/src/assets/images/87f2be86-32c3-4bfc-8db4-dbd0d979e4d3.jpeg)

[](#1if-voy_a_salir-2-if-puedo_comprar_hamburguesa-3-if-venden_vino)

`1if voy_a_salir: 2    if puedo_comprar_hamburguesa: 3        if venden_vino: 4            # Haz algo 5    else: 6        if blazers > 3: 7            # Haz algo 8        else: 9            # Haz algo 10    elif usa_pantalones: 11        # Haz algo 12    else: 13        # Haz algo 14else: 15    if desnudo_al_llegar: 16        # Haz algo 17    elif blazers > 3: 18        # Haz algo 19    else: 20        # Haz algo` 

[](https://github.com/breatheco-de/content/blob/master/src/content/lesson/conditionals-in-programing-python.es.md)