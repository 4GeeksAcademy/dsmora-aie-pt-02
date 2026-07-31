# Resumen de la clase 36

Este resumen está basado en el contenido de los JSON del scraper para la clase 36 y está pensado para usarlo como guía de clase.

## Objetivo de la clase

Introducir la mentalidad de testing y mostrar cómo las pruebas ayudan a prevenir errores, validar comportamiento y mejorar la calidad del software.

## Cómo desarrollar la clase

1. Explicar por qué los errores cuestan más cuando aparecen tarde y por qué las pruebas son una inversión.
2. Diferenciar entre pruebas unitarias, de integración, funcionales y de rendimiento.
3. Mostrar cómo identificar casos normales, casos límite y casos de error.
4. Introducir el ciclo TDD: rojo, verde y refactorización.
5. Explicar cómo aplicar pruebas en TypeScript y en FastAPI, incluyendo el uso de frameworks y TestClient.
6. Cerrar con la importancia de planificar pruebas y evitar anti-patrones.

## Ejemplo práctico para explicar

Un ejemplo útil es empezar con una función de validación o un endpoint simple, escribir una prueba que falle, implementar la solución y luego refactorizarla.

## Puntos clave para enfatizar

- Las pruebas no solo detectan errores, también ayudan a diseñar mejor el código.
- El TDD obliga a pensar primero en el comportamiento esperado.
- No todas las pruebas sirven para lo mismo: cada tipo cubre un nivel distinto del sistema.
- En FastAPI es importante probar endpoints y operaciones CRUD, mientras que en TypeScript conviene pensar en pruebas unitarias con marcos como Jest, Vitest o Mocha/Chai.

## Ejemplo de código

El material del JSON muestra este ejemplo de prueba con FastAPI y TestClient:

```python
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

@app.get("/hello")
async def say_hello():
    return {"message": "¡Hola, FastAPI!"}

client = TestClient(app)
```

## Cierre sugerido

Pedir a los estudiantes que propongan una prueba mínima para una funcionalidad sencilla antes de escribir el código.
