# Prompt para completar el Hito de Data Pipelines (Partes 1, 2 y 3)

Este prompt está pensado para pegarlo completo en tu asistente de IA (OpenClaw, Copilot Chat, etc.) dentro de **tu copia del monorepo** de la compañía asignada, para completar de punta a punta el hito de Telemetría y Data Pipelines: diseño (Parte 1), implementación resiliente (Parte 2) y refactor a producción (Parte 3).

No reemplaza tu criterio: antes de ejecutarlo, ten a mano tu `CONTEXT-company.md` del contexto de data pipelines (KPIs a medir, tabla de destino, audiencia, frecuencia) y tu `CONTEXT-company.md` de telemetría (campos de evento obligatorios). El asistente debe usar los nombres exactos de esos documentos, nunca inventar KPIs, tablas o campos genéricos.

---

## Prompt completo

```text
Eres mi copiloto de ingeniería para completar un hito de tres partes en mi copia del
monorepo de la compañía asignada en el curso. NO estamos creando un repositorio nuevo:
todo el trabajo va sobre el monorepo existente.

Antes de escribir código o documentos, lee y usa como única fuente de verdad:
1. Mi CONTEXT-company.md del contexto de data pipelines (sección "KPIs a medir",
   audiencia, frecuencia, tabla de destino).
2. Mi CONTEXT-company.md de telemetría (campos de evento obligatorios que alimentan
   esos KPIs).
3. La carpeta data/ del monorepo (raw/, process/, pipelines/, eval/) y services/
   (donde ya vive services/telemetry/analysis.py y el endpoint GET /telemetry/report,
   que NO se deben modificar).

Regla no negociable en las tres partes: telemetry_events es siempre la FUENTE, nunca
el destino de este pipeline nuevo. services/telemetry/analysis.py y GET /telemetry/report
quedan intactos. Todo lo nuevo vive en data/pipelines/, data/process/ y
services/reporting/ (separado de services/telemetry/). Los nombres de KPIs, tablas,
campos, flows, tasks y tests deben coincidir con el vocabulario de dominio real de mi
compañía en CONTEXT-company.md — nunca genéricos tipo "extract_data" o
"reporting.business_metrics".

===========================================================
PARTE 1 — Diseño del pipeline (documento, sin código de orquestación)
===========================================================

Objetivo: producir data/pipelines/PIPELINE_DESIGN.md con estas secciones:

1. Estado actual: qué eventos de telemetría ya se capturan, dónde se almacenan, y qué
   responde hoy el reporte técnico existente para ingeniería.
2. Brecha de negocio: qué pregunta de mi CONTEXT-company.md sigue sin respuesta y
   requiere este pipeline nuevo.
3. Propósito del pipeline en una frase: qué entregable de negocio produce, qué KPI(s)
   de la sección "KPIs a medir" calcula, y de qué métrica(s) obligatoria(s) de
   telemetría depende.
4. Formato y frecuencia de extracción desde telemetry_events (y otras tablas de
   dominio si aplica).
5. Diagrama de flujo (texto o Mermaid) con al menos 3 etapas: extracción,
   transformación, carga.
6. Estrategia para manejar actualizaciones de registros existentes sin duplicar datos.
7. Tabla(s) de destino nueva(s) bajo el esquema "reporting", usando EXACTAMENTE el
   nombre de la sección "Destination table" de mi CONTEXT-company.md, y los
   endpoints nuevos previstos en services/reporting/ (estado, disparo manual,
   consulta de KPIs) — separados de servicios de telemetría.
8. Estrategia de idempotencia: qué pasa si el pipeline falla en la carga y se
   reejecuta.
9. Diseño del log de ejecución: campos mínimos por corrida (inicio, fin, registros
   procesados, estado, errores) y por qué cada uno importa.
10. Mapeo a conceptos de Prefect: al menos un flow principal y al menos tres tasks
    (extracción, transformación, carga), y qué states (Running, Completed, Failed)
    son relevantes. Indica qué configuración manejarías como Prefect blocks.
11. Esbozo de los tres endpoints de servicios/reporting/ (consulta de estado, disparo
    manual, consulta de KPIs) y qué función/flow de data/pipelines/ llama cada uno.

Antes de redactar el documento, respóndeme por escrito (borrador) cómo resolverías,
para MI compañía concreta, los siguientes casos: duplicados en el origen, reintento
tras un fallo con carga parcial, eventos tardíos, silencio vs. ausencia real de
actividad, trazabilidad evento→reporte, crecimiento vs. pérdida de datos, caída de
base de datos a mitad de pipeline, y si tiene sentido un buffer offline en el
frontend. No avances a la Parte 2 hasta que este documento esté commiteado.

===========================================================
PARTE 2 — Implementación resiliente (código funcional)
===========================================================

Punto de partida: PIPELINE_DESIGN.md aprobado en la Parte 1. Implementa exactamente
lo que ahí se diseñó — no reinventes el diseño en código.

Objetivo: crear data/pipelines/pipeline.py (punto de entrada principal) más los
módulos de soporte en data/process/, con:

1. Uno o más flows (@flow) de Prefect que sigan las etapas del diseño: extracción,
   transformación, carga como mínimo, cada una como task (@task) independiente con
   inputs/outputs explícitos.
2. Al menos un paso opcional/no crítico (notificación, exportación secundaria,
   snapshot de eval) invocado con return_state=True, para que su fallo no tumbe el
   flow principal.
3. retries y retry_delay_seconds en cada task que toque un servicio externo (base de
   datos, API), con un comentario que justifique el número de reintentos elegido.
4. Al menos un fallo de task manejado explícitamente con return_state=True en vez de
   dejarlo propagar.
5. Caché (cache_key_fn, cache_expiration) en al menos una task de transformación
   costosa, con un comentario que explique la clave de caché y su validez.
6. Carga idempotente en la tabla de destino nombrada en mi CONTEXT-company.md,
   apoyada en el constraint único de mi esquema — reejecutar el pipeline sobre los
   mismos datos no debe duplicar filas.
7. Registro de metadata de cada corrida (inicio, fin, registros procesados, estado,
   errores) en base de datos o en un log estructurado.
8. Un bloque `if __name__ == "__main__"` que permita ejecutar
   `python data/pipelines/pipeline.py` de punta a punta sin errores.
9. Tres endpoints nuevos en services/reporting/ (separados de services/telemetry/):
   (a) estado y metadata de la última corrida, (b) disparo manual del flow,
   (c) consulta de las filas de KPIs de la tabla de destino — este último es lo que
   consumirá el dashboard de la Parte 3. Los endpoints deben importar flows/funciones
   desde data/pipelines/, sin duplicar lógica, y seguir las convenciones de
   autenticación y respuesta del resto de mi API.

Instala Prefect 3 si no está: uv add "prefect>=3". Verifica que
`python data/pipelines/pipeline.py` corre sin errores antes de dar la Parte 2 por
terminada. No avances a la Parte 3 hasta confirmar esto.

===========================================================
PARTE 3 — Refactor a producción: subflows, tests y dashboard
===========================================================

Punto de partida: data/pipelines/pipeline.py de la Parte 2, ya funcional. No lo
reescribas desde cero — refactorízalo.

Objetivo:

1. Divide el flow principal en al menos tres subflows (@flow) que correspondan a las
   etapas reales de mi diseño (extracción desde telemetry_events y otras tablas de
   dominio, transformación, carga en la tabla de destino de mi CONTEXT-company.md).
   El flow principal los invoca en secuencia. Cada subflow tiene inputs y outputs
   explícitos — sin variables globales compartidas entre subflows. Si hay pasos
   opcionales, extráelos también como subflows invocados con return_state=True.
2. Crea tests/pipelines/test_pipeline.py con al menos tres tests unitarios para las
   tasks de transformación que calculan mis KPIs. Cada test debe:
   - Ejecutarse aislado, con datos de prueba en memoria con la forma de mis eventos
     de telemetría (sin base de datos real ni APIs externas). Llama a la task con
     `.fn(...)` para evitar el runtime de Prefect.
   - Incluir al menos un caso de input inválido o malformado (comportamiento
     defensivo).
   - Incluir al menos un caso que valide el valor calculado de un KPI contra la
     definición de mi CONTEXT-company.md, con un input conocido calculado a mano.
   `python -m pytest tests/pipelines/test_pipeline.py` debe pasar sin errores.
3. Verifica que, tras el refactor a subflows, `python data/pipelines/pipeline.py`
   sigue ejecutando el ETL completo sin errores, preservando el entrypoint
   `__main__` y el comando documentado en la Parte 2 — no lo reconstruyas.
4. Construye un dashboard en uis/backoffice/ (por ejemplo /reporting) que consuma mi
   endpoint de consulta de KPIs de services/reporting/ y muestre cada KPI de la
   sección "KPIs a medir" de mi CONTEXT-company.md (un gráfico o tabla por KPI),
   etiquetado con el mismo nombre que en el CONTEXT y mostrando el período (semana o
   mes) que cubren los datos. Debe ser legible para el stakeholder de negocio
   nombrado en mi CONTEXT-company.md (ej. CEO o gerente de departamento), sin pulido
   visual obligatorio — solo funcional y correctamente etiquetado.
5. (Opcional) Si al responder las preguntas de diseño de la Parte 1 identifiqué
   mejoras de resiliencia u observabilidad que no cubrí en las Fases 1-3 (heartbeat de
   silencio, lock de concurrencia, patrón Idempotency-Key), impleméntalas ahora y
   anota en PIPELINE_DESIGN.md qué pregunta responden y por qué las prioricé. No
   inventes una mejora solo para marcar la casilla.

Antes de terminar, confirma conmigo este checklist final de las tres partes:
- [ ] PIPELINE_DESIGN.md commiteado con las 11 secciones de la Parte 1.
- [ ] data/pipelines/pipeline.py con flow(s)/tasks resilientes (retries, caché,
      return_state) y carga idempotente en la tabla de destino de mi CONTEXT.
- [ ] Tres endpoints en services/reporting/ (estado, disparo manual, consulta de
      KPIs), separados de services/telemetry/.
- [ ] Flow principal dividido en al menos tres subflows con inputs/outputs
      explícitos.
- [ ] tests/pipelines/test_pipeline.py con al menos tres tests unitarios, incluyendo
      un caso de input inválido y un caso de validación de KPI contra el CONTEXT.
- [ ] `python -m pytest tests/pipelines/test_pipeline.py` y
      `python data/pipelines/pipeline.py` pasan sin errores.
- [ ] Dashboard en uis/backoffice/ mostrando cada KPI, etiquetado y con período,
      alimentado desde services/reporting/.
- [ ] telemetry_events y services/telemetry/analysis.py sin modificar en todo el
      proceso.

Al terminar cada parte, dime qué archivos creaste o modificaste y qué falta
verificar antes de hacer commit. Usa el mensaje de commit sugerido de cada parte:
Parte 2 -> "feat: implement resilient business performance pipeline"
Parte 3 -> "feat: refactor business performance pipeline into subflows, add unit
tests, and add reporting dashboard"
```

---

## Notas de uso

- Ejecuta el prompt una parte a la vez si prefieres revisar cada entrega antes de continuar; el texto ya está dividido en tres bloques (`PARTE 1`, `PARTE 2`, `PARTE 3`) para poder copiar solo el bloque que necesitas.
- Sustituye cualquier referencia a `CONTEXT-company.md` por el nombre real de archivo si tu equipo lo llama distinto.
- Fuentes usadas para construir este prompt: `class_48/ai-eng-data-pipeline-design_project_README.es.md` (Parte 1), `class_49/ai-eng-data-pipeline-build_project_README.es.md` (Parte 2), `class_50/ai-eng-milestone-data-pipeline-enhancement_project_README.es.md` (Parte 3).
