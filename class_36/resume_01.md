# Guía Docente Completa: Clase 36 - Introducción a las Pruebas

Clase online para 60-75 minutos.
Documento para profesor: incluye objetivo, agenda, guion literal y ejemplos para presentar la mentalidad de testing, TDD, pruebas unitarias en TypeScript y pruebas de endpoints en FastAPI.

## 1) Objetivo de la clase

Al finalizar, el estudiante podrá:

- Explicar por qué las pruebas reducen costo y riesgo en desarrollo.
- Diferenciar pruebas unitarias, de integración, funcionales y de rendimiento.
- Identificar casos normales, límite y de error.
- Entender el ciclo TDD: rojo, verde, refactorizar.
- Reconocer frameworks comunes de pruebas en TypeScript y Python/FastAPI.
- Relacionar pruebas unitarias con calidad, refactorización y confianza técnica.

## 2) Agenda sugerida (60-75 min)

Ruta base de 70 minutos:

- Apertura y costo de errores: 8 min
- Bloque A: tipos de pruebas y casos de prueba: 12 min
- Bloque B: primera mentalidad TDD: 12 min
- Bloque C: pruebas unitarias en TypeScript: 15 min
- Bloque D: pruebas en FastAPI con TestClient: 15 min
- Cierre y preguntas: 8 min

Si tienes 75 min:

- Añade una práctica comparando un test de TypeScript con uno de FastAPI.

Si tienes 60 min:

- Presenta TypeScript y FastAPI como dos ejemplos paralelos sin entrar tanto en frameworks alternativos.

## 3) Preparación docente

Checklist:

- Tener listo un ejemplo de función pequeña para probar.
- Tener claro el patrón AAA.
- Poder mostrar un endpoint FastAPI con TestClient.

## 4) Guion docente detallado

## Apertura (8 min)

Qué decir (literal):

"Las pruebas no son un castigo ni una burocracia. Son una forma de reducir miedo al cambio."

"Cuando no hay pruebas, cada cambio pequeño puede sentirse como una apuesta. Cuando sí las hay, el código se vuelve más confiable y más fácil de evolucionar."

## Bloque A - Tipos de pruebas y casos de prueba (12 min)

### A1. El costo de los errores (4 min)

Qué decir (literal):

"Un error detectado tarde cuesta más. No solo por la corrección, sino por soporte, confianza y tiempo de depuración."

Caso del material:

- Errores en producción cuestan más que errores detectados temprano.

### A2. Tipos principales de pruebas (5 min)

Explica:

- Unitarias: una función o unidad aislada.
- Integración: varias piezas trabajando juntas.
- Funcionales: comportamiento completo desde la mirada del usuario.
- Rendimiento: velocidad, carga y estabilidad.

Qué decir (literal):

"No todas las pruebas hacen lo mismo. La clave es entender qué cubre cada nivel y cuándo conviene usarlo."

### A3. Casos normales, límite y error (3 min)

Qué decir (literal):

"Probar solo el camino feliz deja huecos. Una suite mínima útil piensa también en bordes y fallos esperables."

## Bloque B - Primera mentalidad TDD (12 min)

### B1. Ciclo rojo, verde, refactorizar (6 min)

Qué decir (literal):

"En TDD primero escribes una prueba que falla. Luego haces lo mínimo para que pase. Después limpias el diseño sin cambiar el comportamiento."

### B2. Ejemplo de TDD con TaskManager (6 min)

Código tomado del material:

```python
import pytest


class TaskManager:
        def __init__(self):
                self.tasks = []

        def add_task(self, description):
                pass


def test_add_task():
        tm = TaskManager()
        task_id = tm.add_task("Escribir pruebas unitarias")
        assert task_id == 1
        assert len(tm.tasks) == 1
        assert tm.tasks[0]["description"] == "Escribir pruebas unitarias"
        assert tm.tasks[0]["completed"] is False
```

Punto docente:

- La prueba define comportamiento antes de la implementación.

## Bloque C - Pruebas unitarias en TypeScript (15 min)

### C1. Frameworks comunes (4 min)

Comparativa del material:

- Jest: solución todo en uno.
- Mocha/Chai: modular y flexible.
- Vitest: rápido y alineado con tooling moderno.

### C2. Patrón AAA (4 min)

Qué decir (literal):

"Una buena prueba suele tener tres actos: preparar, ejecutar y verificar. Eso mantiene intención y legibilidad."

### C3. Ejemplo de función en TypeScript (7 min)

```typescript
export interface Shape {
    type: 'circle' | 'rectangle' | 'triangle';
    dimensions: number[];
}

export function calculateArea(shape: Shape): number {
    switch (shape.type) {
        case 'circle':
            return Math.PI * Math.pow(shape.dimensions[0], 2);
        case 'rectangle':
            return shape.dimensions[0] * shape.dimensions[1];
        case 'triangle':
            return 0.5 * shape.dimensions[0] * shape.dimensions[1];
        default:
            throw new Error('Tipo de figura desconocido');
    }
}
```

Qué decir (literal):

"TypeScript ayuda con tipos, pero los tipos no reemplazan el comportamiento en runtime. Por eso igual necesitamos pruebas."

## Bloque D - Pruebas en FastAPI con TestClient (15 min)

### D1. Frameworks de Python (4 min)

Panorama del material:

- unittest
- pytest
- doctest

### D2. TestClient y endpoints (5 min)

Ejemplo:

```python
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


@app.get('/hello')
async def say_hello():
        return {'message': '¡Hola, FastAPI!'}


client = TestClient(app)
```

Qué decir (literal):

"TestClient permite probar el ciclo de request/response sin levantar un servidor real. Eso hace las pruebas más rápidas y prácticas."

### D3. CRUD y casos de error (6 min)

Qué enfatizar:

- Probar POST con payload válido e inválido.
- Probar GET de recurso existente e inexistente.
- Probar update y delete.
- Verificar códigos 404, 422 y respuestas esperadas.

Qué decir (literal):

"Una API no está bien probada solo porque responde 200 una vez. Hay que verificar validación, errores y comportamiento en cada operación principal."

## 5) Ejemplo de validación completa

Caso tomado del material:

```python
def validate_user(name, age, email):
        if not isinstance(name, str) or len(name.strip()) == 0:
                raise ValueError('Name must be a non-empty string')
        if not isinstance(age, int) or age < 0 or age > 150:
                raise ValueError('Age must be between 0 and 150')
        if not isinstance(email, str) or '@' not in email or '.' not in email:
                raise ValueError('Email must contain @ and .')
        return {'name': name.strip(), 'age': age, 'email': email.lower()}
```

Úsalo para explicar:

- caso normal
- caso límite
- caso de error

## 6) Mejores prácticas para remarcar

- Nombres descriptivos de tests.
- Un comportamiento por prueba cuando sea posible.
- AAA para claridad.
- Cobertura útil, no solo cobertura alta.
- Aislamiento entre pruebas.
- Evitar pruebas frágiles o demasiado acopladas a implementación interna.

## 7) Preguntas de chequeo

- ¿Por qué las pruebas reducen el costo de cambio?
- ¿Qué diferencia hay entre una prueba unitaria y una de integración?
- ¿Qué significa la fase roja en TDD?
- ¿Qué aporta TestClient en FastAPI?
- ¿Por qué una alta cobertura no garantiza una buena suite de pruebas?

## 8) Cierre sugerido

Qué decir (literal):

"Las pruebas no solo detectan errores: también obligan a pensar mejor el comportamiento esperado del sistema."

"Cuando un equipo prueba bien, refactoriza con más seguridad, documenta mejor el código y reduce el miedo a tocar piezas importantes."
