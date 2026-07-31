# Guia Docente: Class 36 - Introduccion al Testing + Unit Testing en FastAPI y TypeScript

Este resumen integra:
- introduction_to_testing.json
- unit_testing_with_fastapi.json
- unit_testing_in_typescript.json

Objetivo docente: impartir una clase de 60-75 minutos centrada en mentalidad de testing, diseno de casos (normal, limite, error), TDD (rojo-verde-refactor) y una demo practica en Python/FastAPI y TypeScript.

## 1. Objetivos de aprendizaje

Al finalizar la sesion, el estudiante deberia poder:

- Explicar por que testear reduce costo de errores y acelera cambios seguros.
- Diferenciar pruebas unitarias, integracion y funcionales con ejemplos reales.
- Disenar casos de prueba representativos (normal, borde, error).
- Aplicar el ciclo TDD en una funcionalidad pequena.
- Ejecutar pruebas unitarias basicas en FastAPI con pytest/TestClient.
- Ejecutar pruebas unitarias basicas en TypeScript con Vitest siguiendo AAA.

## 2. Agenda sugerida (60-75 min)

- Bloque A - Contexto y valor del testing: 8 min
- Bloque B - Tipos de pruebas + diseno de casos: 12 min
- Bloque C - TDD rojo-verde-refactor (mini ejercicio guiado): 12 min
- Bloque D - Demo FastAPI con pytest/TestClient: 16 min
- Bloque E - Demo TypeScript con Vitest + cierre: 12 min

Total base: 60 min

Extension a 75 min:
- +8 min en Bloque D para agregar caso CRUD negativo adicional.
- +7 min en Bloque E para agregar tabla de casos limite y cobertura.

## 3. Checklist de preparacion (antes de la clase)

- Confirmar Python 3 y Node instalados.
- Confirmar internet para instalar dependencias.
- Tener terminal limpia en la raiz del repo.
- Tener editor listo para abrir dos carpetas de demo:
  - tmp/class36_fastapi_demo
  - tmp/class36_ts_demo

Comandos de verificacion rapida:

```bash
python3 --version
node --version
npm --version
```

## 4. Guion docente detallado

## Bloque A (8 min): Por que testing importa

Que decir (literal):

"Hoy no vamos a ver testing como burocracia, sino como acelerador. Sin pruebas, cada cambio es una apuesta. Con pruebas, cada cambio tiene red de seguridad. El objetivo no es 100% de cobertura ciega, es confianza para evolucionar codigo sin romper lo que ya funciona."

"Un bug detectado en produccion cuesta mucho mas que uno detectado en local. Testing es ahorro de tiempo futuro y mejor comunicacion de comportamiento esperado."

Accion en vivo:
- Mostrar un ejemplo breve de funcion simple y preguntar: "como demostramos que realmente funciona para entradas raras?"

## Bloque B (12 min): Tipos de pruebas y casos

Que decir (literal):

"Prueba unitaria: valida una pieza pequena aislada. Integracion: valida que piezas colaboren bien. Funcional: valida flujo desde perspectiva del usuario."

"Si solo probamos camino feliz, dejamos agujeros. Minimo debemos cubrir tres grupos: caso normal, caso borde y caso de error."

Ejemplo verbal rapido:
- Funcion validate_user(name, age, email)
- Normal: datos validos.
- Borde: edad 0 y 150.
- Error: email sin arroba.

Prompt exacto para OpenClaw (conceptual):

```text
Actua como instructor tecnico. Dame 9 casos de prueba para una funcion validate_user(name, age, email), separados en 3 categorias: normales, limite y error. Para cada caso incluye: entrada, salida esperada y justificacion corta.
```

## Bloque C (12 min): TDD rojo-verde-refactor

Que decir (literal):

"TDD no significa escribir miles de tests primero. Significa dar pasos pequenos: primero una prueba que falla (rojo), luego codigo minimo para pasar (verde), luego mejorar estructura sin cambiar comportamiento (refactor)."

"Si el refactor rompe algo, el test te lo grita de inmediato. Esa es la ventaja real."

Mini dinamica guiada:
- Elegir funcion add_task(description).
- Escribir primero test que espera ID incremental y validacion de texto vacio.
- Implementar minimo.
- Refactorizar nombres/estructura.

Prompt exacto para OpenClaw (TDD):

```text
Genera una kata TDD minima en Python para una clase TaskManager con metodo add_task(description). Quiero 3 pruebas en orden pedagogico: 1) agrega tarea valida, 2) rechaza descripcion vacia, 3) ids incrementales. Devuelve codigo en archivos task_manager.py y test_task_manager.py.
```

## Bloque D (16 min): Demo FastAPI con pytest/TestClient

Objetivo:
- Probar endpoint GET y POST con validacion basica.

Comandos exactos (copiar/pegar):

```bash
mkdir -p tmp/class36_fastapi_demo
cd tmp/class36_fastapi_demo
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install fastapi pytest httpx
```

Crear app:

```bash
cat > app.py << 'PY'
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
items = []

class Item(BaseModel):
    name: str

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/items")
def create_item(item: Item):
    if len(item.name.strip()) == 0:
        raise HTTPException(status_code=422, detail="name cannot be empty")
    items.append(item.name)
    return {"count": len(items), "name": item.name}
PY
```

Crear pruebas:

```bash
cat > test_app.py << 'PY'
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_health_ok():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"ok": True}

def test_create_item_ok():
    r = client.post("/items", json={"name": "Notebook"})
    assert r.status_code == 200
    body = r.json()
    assert body["name"] == "Notebook"
    assert body["count"] >= 1

def test_create_item_empty_name():
    r = client.post("/items", json={"name": "   "})
    assert r.status_code == 422
    assert r.json()["detail"] == "name cannot be empty"
PY
```

Ejecutar:

```bash
pytest -q
```

Que decir (literal):

"Aqui vemos dos cosas: validar respuestas felices y validar comportamiento de error. Un test util no solo confirma que funciona, tambien confirma que falla bien cuando debe fallar."

Extension opcional (+8 min):
- Agregar test para campo faltante en POST y discutir diferencia entre error de negocio y error de esquema.

Prompt exacto para OpenClaw (FastAPI):

```text
Tengo una API FastAPI con endpoint POST /items que recibe {name: string}. Genera 6 pruebas pytest con TestClient: 2 de exito, 2 de validacion de esquema y 2 de reglas de negocio. Incluye nombres de test claros y patron Arrange-Act-Assert.
```

## Bloque E (12 min): Demo TypeScript con Vitest + cierre

Objetivo:
- Aplicar AAA en TypeScript con casos normales y bordes.

Comandos exactos (copiar/pegar):

```bash
cd /workspaces/dsmora-aie-pt-02
mkdir -p tmp/class36_ts_demo
cd tmp/class36_ts_demo
npm init -y
npm i -D typescript vitest @types/node
npx tsc --init
npm pkg set scripts.test="vitest run"
```

Crear codigo:

```bash
cat > math.ts << 'TS'
export function divide(a: number, b: number): number {
  if (b === 0) throw new Error("division by zero");
  return a / b;
}
TS
```

Crear pruebas:

```bash
cat > math.test.ts << 'TS'
import { describe, it, expect } from "vitest";
import { divide } from "./math";

describe("divide", () => {
  it("retorna cociente correcto", () => {
    // Arrange
    const a = 10;
    const b = 2;

    // Act
    const result = divide(a, b);

    // Assert
    expect(result).toBe(5);
  });

  it("lanza error en division por cero", () => {
    expect(() => divide(10, 0)).toThrow("division by zero");
  });

  it("maneja negativos", () => {
    expect(divide(-9, 3)).toBe(-3);
  });
});
TS
```

Ejecutar:

```bash
npm test
```

Que decir (literal):

"TypeScript ayuda antes de ejecutar, pero no reemplaza tests de comportamiento. El tipo te dice que algo puede compilar; el test te confirma que hace lo correcto."

Prompt exacto para OpenClaw (TypeScript):

```text
Genera una suite Vitest para una funcion calculateDiscount(price, percent, isMember) con minimo 8 tests: normales, bordes y errores. Usa nombres descriptivos y patron AAA.
```

## 5. Version recortada (60 min exactos)

- Reducir Bloque B de 12 a 8 min (explicar solo 1 ejemplo de cada tipo de prueba).
- Reducir Bloque D a 12 min (solo test de health y un POST exitoso).
- Mantener Bloque C y E completos para no perder practica.

## 6. Version extendida (75 min)

- Agregar pair-debugging de un test fallando (5 min).
- Agregar cobertura con reporte rapido (5 min):

```bash
# Python
pip install pytest-cov
pytest --cov=. -q

# TypeScript (opcional)
npm i -D @vitest/coverage-v8
npx vitest run --coverage
```

- Agregar retro final de anti-patrones (5 min):
  - tests fragiles por acoplamiento a implementacion interna
  - tests sin nombres descriptivos
  - solo camino feliz

## 7. Plan de contingencia

Si falla instalacion de dependencias:
- Usar modo solo lectura: revisar tests ya escritos y analizar resultados esperados.
- Pedir a estudiantes que hagan prediccion de resultado por cada test antes de ejecutar.

Si falla internet:
- Ejecutar unicamente la parte conceptual + pseudocodigo de pruebas.

Si falta tiempo:
- Priorizar Bloque C (TDD) y una sola demo (FastAPI o TypeScript), no ambas.

## 8. Preguntas de chequeo para cierre (5 min)

- Cual es la diferencia practica entre unit test e integration test?
- Dame un ejemplo de caso limite y uno de error para una funcion de login.
- En TDD, que ganas al escribir primero la prueba que falla?
- Por que una cobertura alta no garantiza calidad de pruebas?

## 9. Entregable esperado por estudiante

Al final de la clase, cada estudiante deberia tener:
- Al menos 1 funcion con 3-5 pruebas (normal, borde, error).
- Ejecucion local de pruebas sin errores.
- Capacidad de explicar en voz alta por que cada test existe.
