# Clase 55: guía de debate — los datos también forman parte del modelo

> **Trazabilidad:** las preguntas siguientes son material del instructor. Se basan en las lecciones scrapeadas de los dos módulos, pero no son una transcripción literal de los JSON. El vínculo con WeLoveReviews es una actividad de continuidad con la clase 54.

## Propósito

Esta guía acompaña `resume_01.md` con preguntas socráticas para que el grupo deje de entender la preparación de datos como una lista mecánica de comandos. La meta es que puedan defender cada transformación: qué problema resuelve, qué información conserva, qué riesgo introduce y cómo se valida.

## Checkpoint

Cada estudiante debe poder presentar una mini-especificación de datos con:

- pregunta y target;
- columnas de entrada y momento en que están disponibles;
- reglas para nulos, duplicados, tipos y categorías;
- estrategia de split;
- riesgo de leakage;
- criterio de éxito y plan de auditoría.

## Apertura

Un modelo da 99% de accuracy. Después se descubre que una columna llamada `closed_at` se generó después del resultado que se quería predecir. ¿El modelo era bueno?

**Respuesta orientativa:** no necesariamente. La métrica puede ser artificial porque la entrada contiene información del futuro. Antes de discutir el algoritmo hay que auditar el contrato temporal de cada columna.

## Aprender: vocabulario y contrato de datos

Preguntas:

1. Si `review_text` es una característica y `human_stars` es una etiqueta, ¿qué sucede cuando `human_stars` se incluye accidentalmente en el texto enviado al modelo?
2. ¿Por qué una columna puede ser numérica en pandas y aun así no ser una buena característica?
3. ¿Qué diferencia hay entre que falte el target y que falte una feature?
4. ¿Cuándo es más importante un split temporal que uno aleatorio?

Sondeos:

- Si responden «solo hay que eliminar nulos», pedir que expliquen cuántas filas se perderían y si la ausencia tiene significado.
- Si responden «todo número es una feature», pedir que analicen un ID, un timestamp de auditoría y una variable posterior al evento.

## Reflexionar: limpieza y sesgo

Caso: las reseñas con 1 estrella tienen más textos vacíos que las reseñas con 5 estrellas.

Preguntas:

1. Si eliminamos todos los vacíos, ¿qué distribución queda?
2. ¿La limpieza puede cambiar el problema que estamos midiendo?
3. ¿Cómo comunicarías al cliente que la salida solo representa reseñas con texto?
4. ¿Qué diferencia hay entre corregir un error y eliminar un caso incómodo?

Idea clave:

> La ausencia de datos también puede ser una señal. No siempre se imputa ni siempre se elimina.

## Tener en cuenta: transformaciones aprendidas

Preguntas:

1. ¿Por qué el promedio para imputar un nulo debe calcularse sobre train?
2. ¿Por qué el vocabulario de un vectorizador no debe aprenderse con el test?
3. ¿Qué pasa si codificamos `bajo`, `medio`, `alto` como 1, 2, 3? ¿Cuándo sería válido y cuándo inventaría una relación?
4. ¿Cómo tratarías una categoría que solo aparece en test?

Respuesta esperada: usar transformaciones ajustadas en train, definir comportamiento para categorías desconocidas y distinguir variables ordinales de variables nominales.

## Hacer: diseñar una preparación

Entregar a los grupos esta tabla:

| columna | ejemplo | pregunta |
| --- | --- | --- |
| `income` | `"45,000"` | ¿separador decimal/miles? |
| `city` | `Madrid`, `madrid` | ¿misma categoría? |
| `age` | `-4` | ¿valor imposible? |
| `created_at` | `2026-09-23` | ¿disponible antes de predecir? |
| `approved` | `yes/no` | ¿target o feature? |
| `decision_date` | fecha posterior | ¿leakage? |

Deben devolver:

```text
columna -> problema -> transformación -> validación
```

Ejemplo:

```text
income -> texto con separador -> convertir a numérico -> contar conversiones fallidas y revisar rango
```

## Evitar: antipatrones

- Eliminar nulos sin medirlos.
- Imputar con la media global antes de dividir.
- Normalizar categorías con reglas que borran diferencias reales.
- Usar IDs como señal predictiva sin entenderlos.
- Ver el test después de cada cambio y llamarlo «validación».
- Eliminar outliers solo porque empeoran la métrica.
- Mezclar la etiqueta humana con la entrada del modelo.
- Cambiar el texto para que el modelo produzca la respuesta esperada.
- Reportar únicamente accuracy cuando las clases están desequilibradas.

Pregunta final del debate:

> ¿Qué evidencia necesitas para afirmar que una transformación mejora el sistema y no solo la métrica?

Respuesta orientativa: una comparación reproducible en datos no vistos, un baseline, una métrica adecuada al problema, revisión de casos y una explicación de los trade-offs.

## Cierre

Cada estudiante completa:

> «Antes de entrenar o ejecutar un modelo, voy a comprobar ______ porque ______. Si encuentro un problema, lo validaré mediante ______ y lo documentaré en ______.»

La respuesta debe incluir al menos una comprobación de calidad y una de leakage.
