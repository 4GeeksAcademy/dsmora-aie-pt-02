# Ejercicios Rapidos - Class 07

Este archivo contiene 4 variantes alineadas con JavaScript/TypeScript: tipos, decisiones, control de flujo y validacion.

## Variante 1 (facil): Usuario activo o inactivo

**Objetivo:** variables tipadas + decision simple.

**Enunciado:**
- Declarar `userName: string` y `isActive: boolean`.
- Si `isActive` es `true`, mostrar "usuario activo".
- Si no, mostrar "usuario inactivo".

**Ejemplo TypeScript:**
```ts
const userName: string = "Ana";
const isActive: boolean = true;

if (isActive) {
  console.log(userName + " esta activo");
} else {
  console.log(userName + " esta inactivo");
}
```

**Tiempo estimado:** 5 minutos.

## Variante 2 (facil-media): Validador de edad con parseo

**Objetivo:** string a number + decision.

**Enunciado:**
- Recibir edad como texto.
- Convertir a numero.
- Si no es numero valido, mostrar error.
- Si edad >= 18, "Mayor de edad"; si no, "Menor de edad".

**Ejemplo TypeScript:**
```ts
const ageInput: string = "21";
const age: number = Number(ageInput);

if (Number.isNaN(age)) {
  console.log("Edad invalida");
} else if (age >= 18) {
  console.log("Mayor de edad");
} else {
  console.log("Menor de edad");
}
```

**Tiempo estimado:** 7 minutos.

## Variante 3 (media): Recuento de aprobados en arreglo

**Objetivo:** arreglo + bucle + decision.

**Enunciado:**
- Dado un arreglo de notas, contar cuantas son >= 60.
- Mostrar total de aprobados.

**Ejemplo TypeScript:**
```ts
const grades: number[] = [55, 71, 90, 48, 60];
let approvedCount: number = 0;

for (let i = 0; i < grades.length; i++) {
  if (grades[i] >= 60) {
    approvedCount++;
  }
}

console.log("Aprobados:", approvedCount);
```

**Tiempo estimado:** 9 minutos.

## Variante 4 (mas larga, max 15 min): Mini validador de registro (HTML, CSS y JavaScript)

**Objetivo:** integrar interfaz, validaciones y decisiones con datos del formulario.

**Enunciado:**
1. Crear formulario con nombre y edad.
2. Validar:
   - nombre minimo 3 caracteres
   - edad entre 18 y 120
3. Mostrar mensaje de exito o error en pantalla.
4. Cambiar color del resultado segun estado.

**Starter sugerido:**
```html
<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Validador de Registro</title>
    <style>
      body {
        margin: 0;
        min-height: 100vh;
        display: grid;
        place-items: center;
        background: linear-gradient(160deg, #f4f1de, #e0fbfc);
        font-family: "Segoe UI", Tahoma, sans-serif;
      }

      .panel {
        width: min(92vw, 380px);
        background: #fff;
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.12);
      }

      input,
      button {
        width: 100%;
        margin-top: 8px;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #c6c6c6;
      }

      button {
        border: none;
        background: #006d77;
        color: #fff;
        font-weight: 700;
        cursor: pointer;
      }

      #msg {
        margin-top: 12px;
        border-radius: 8px;
        padding: 10px;
        font-weight: 700;
        background: #f1f1f1;
      }

      .ok {
        background: #d8f3dc;
        color: #1b5e20;
      }

      .error {
        background: #ffd6d6;
        color: #8b1e1e;
      }
    </style>
  </head>
  <body>
    <div class="panel">
      <h1>Registro</h1>
      <label for="name">Nombre</label>
      <input id="name" type="text" />

      <label for="age">Edad</label>
      <input id="age" type="number" />

      <button id="checkBtn">Validar</button>
      <div id="msg">Esperando datos...</div>
    </div>

    <script>
      const nameInput = document.getElementById("name");
      const ageInput = document.getElementById("age");
      const checkBtn = document.getElementById("checkBtn");
      const msg = document.getElementById("msg");

      checkBtn.addEventListener("click", () => {
        const name = nameInput.value.trim();
        const age = Number(ageInput.value);

        msg.className = "";

        if (name.length < 3) {
          msg.textContent = "Nombre invalido (minimo 3 caracteres)";
          msg.classList.add("error");
          return;
        }

        if (Number.isNaN(age) || age < 18 || age > 120) {
          msg.textContent = "Edad invalida (18 a 120)";
          msg.classList.add("error");
          return;
        }

        msg.textContent = "Registro valido";
        msg.classList.add("ok");
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
