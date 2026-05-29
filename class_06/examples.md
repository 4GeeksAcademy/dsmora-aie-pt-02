# Ejercicios Rapidos - Class 06

Este archivo contiene 4 variantes para practicar fundamentos: secuencia, variables, decisiones y validacion basica.

## Variante 1 (facil): Control de acceso por edad

**Objetivo:** secuencia + variable + decision.

**Enunciado:**
- Pedir nombre y edad.
- Si edad >= 18, mostrar "Puede ingresar".
- Si no, mostrar "Acceso denegado".

**Entradas:**
- `nombre` (texto)
- `edad` (numero)

**Salida:**
- Mensaje final con nombre y resultado.

**Pseudocodigo:**
```
INICIO
  leer nombre
  leer edad

  si edad >= 18 entonces
    mostrar nombre + ": puede ingresar"
  si no
    mostrar nombre + ": acceso denegado"
  fin si
FIN
```

**Tiempo estimado:** 5 minutos.

## Variante 2 (facil-media): Descuento de tienda

**Objetivo:** secuencia + variable + decision + operadores.

**Enunciado:**
- Pedir total de compra.
- Si total >= 100, aplicar 10% de descuento.
- Si no, mantener total.
- Mostrar total final.

**Entradas:**
- `totalCompra` (numero)

**Salida:**
- `totalFinal` (numero)

**Pseudocodigo:**
```
INICIO
  leer totalCompra
  descuento = 0

  si totalCompra >= 100 entonces
    descuento = totalCompra * 0.10
  fin si

  totalFinal = totalCompra - descuento
  mostrar totalFinal
FIN
```

**Tiempo estimado:** 7 minutos.

## Variante 3 (media): Estado de bateria

**Objetivo:** secuencia + variable + decision con validacion de rango.

**Enunciado:**
- Pedir porcentaje de bateria (0 a 100).
- Si bateria < 0 o > 100: "Valor invalido".
- Si bateria < 20: "Conecta cargador".
- Si bateria >= 20: "Bateria suficiente".

**Entradas:**
- `bateria` (numero)

**Salida:**
- Mensaje de estado.

**Pseudocodigo:**
```
INICIO
  leer bateria

  si bateria < 0 o bateria > 100 entonces
    mostrar "Valor invalido"
  si no
    si bateria < 20 entonces
      mostrar "Conecta cargador"
    si no
      mostrar "Bateria suficiente"
    fin si
  fin si
FIN
```

**Tiempo estimado:** 8 minutos.

## Variante 4 (mas larga, max 15 min): Mini validador de nota con HTML, CSS y JavaScript

**Objetivo:** integrar estructura visual y logica condicional en una sola pagina.

**Enunciado:**
1. Crear una interfaz con un input de nota (0 a 100), un boton y un area de resultado.
2. Si nota < 0 o > 100, mostrar "Nota invalida".
3. Si nota >= 60, mostrar "Aprobado".
4. Si nota < 60, mostrar "Reprobado".
5. Usar estilos para diferenciar estados (verde, rojo, naranja).

**Starter sugerido (resolver/completar):**
```html
<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Validador de Nota</title>
    <style>
      body {
        margin: 0;
        min-height: 100vh;
        display: grid;
        place-items: center;
        font-family: "Trebuchet MS", Verdana, sans-serif;
        background: linear-gradient(135deg, #f7f3e8, #d9eef2);
      }

      .card {
        width: min(92vw, 360px);
        background: #ffffff;
        border-radius: 14px;
        padding: 18px;
        box-shadow: 0 10px 24px rgba(0, 0, 0, 0.12);
      }

      input,
      button {
        width: 100%;
        padding: 10px;
        margin-top: 8px;
        border-radius: 8px;
        border: 1px solid #c7c7c7;
      }

      button {
        border: none;
        cursor: pointer;
        background: #1f6f8b;
        color: #fff;
        font-weight: 700;
      }

      #resultado {
        margin-top: 12px;
        padding: 10px;
        border-radius: 8px;
        background: #f3f3f3;
        font-weight: 700;
      }

      .ok {
        background: #d8f3dc;
        color: #1b5e20;
      }

      .fail {
        background: #ffd6d6;
        color: #8b1e1e;
      }

      .warn {
        background: #ffe8cc;
        color: #9a4d00;
      }
    </style>
  </head>
  <body>
    <div class="card">
      <h1>Validador de Nota</h1>
      <label for="nota">Ingresa nota (0-100)</label>
      <input id="nota" type="number" />
      <button id="btn">Evaluar</button>
      <div id="resultado">Esperando evaluacion...</div>
    </div>

    <script>
      const notaInput = document.getElementById("nota");
      const btn = document.getElementById("btn");
      const resultado = document.getElementById("resultado");

      btn.addEventListener("click", () => {
        const nota = Number(notaInput.value);
        resultado.className = "";

        if (Number.isNaN(nota) || nota < 0 || nota > 100) {
          resultado.textContent = "Nota invalida";
          resultado.classList.add("warn");
          return;
        }

        if (nota >= 60) {
          resultado.textContent = "Aprobado";
          resultado.classList.add("ok");
        } else {
          resultado.textContent = "Reprobado";
          resultado.classList.add("fail");
        }
      });
    </script>
  </body>
</html>
```

**Tiempo estimado sugerido:**
- HTML: 4 min
- CSS: 4 min
- JavaScript: 6 min
- Prueba final: 1 min
