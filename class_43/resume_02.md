# Clase 43 — Guía práctica: cómo explicar ejemplos y diferenciar stream vs batch

## Nota de alcance

Este documento complementa a [resume_01.md](resume_01.md). No agrega casos nuevos ni datos que no estén en los tres JSON de la carpeta (`introduction_to_telemetry.json`, `telemetry_architecture.json`, `most_representative_cases_in_telemetry.json`) ni en el proyecto asociado (`ai-eng-telemetry-plan`). Su objetivo es dar al profesor un método reutilizable para **explicar los ejemplos con rigor técnico** y para que el grupo **distinga con seguridad procesamiento en flujo (stream) de procesamiento por lotes (batch)**, incluyendo los errores de comprensión más comunes al enseñar este tema.

## 1. Método para explicar cualquier ejemplo de telemetría

Un error frecuente al enseñar telemetría es contar el ejemplo como anécdota de empresa ("Netflix sabe todo de vos") en lugar de como decisión de ingeniería. Para evitarlo, cada ejemplo debe descomponerse siempre en tres partes, en este orden:

1. **Evento observable:** el dato concreto que se captura, no una interpretación. Debe ser algo que un sistema puede registrar sin ambigüedad (un clic, una pausa, un timestamp, un código de respuesta).
2. **Hipótesis:** la pregunta de negocio o de producto que ese evento intenta responder. Si no se puede formular una hipótesis, el evento no debería capturarse (mentalidad de "hipótesis primero", bloque 2 de resume_01).
3. **Decisión habilitada:** qué acción concreta se toma con esa evidencia. Sin esta parte, el ejemplo queda incompleto y suena a "vigilancia" en lugar de a ingeniería con propósito.

Esto coincide exactamente con la plantilla que el proyecto exige para el catálogo de eventos:

> *"Capturamos `[event_type]` porque necesitamos saber `[hipótesis]`, lo que nos permite tomar la decisión `[decisión]`."*

Recomendación práctica: pedirle al grupo que complete esa frase en voz alta para cada ejemplo del material antes de seguir. Si a alguien le cuesta completarla, es señal de que el ejemplo se explicó como dato suelto y no como caso de uso.

### 1.1 Ejemplos del material, descompuestos con el método de 3 partes

| Empresa | Evento observable | Hipótesis | Decisión habilitada |
|---|---|---|---|
| Netflix | `episode_paused` con timestamp exacto dentro del episodio | Si muchos usuarios pausan en el mismo punto, algo en esa escena no funciona | Ajustar ritmo narrativo o decidir renovar/cancelar la serie |
| Spotify | `track_skipped` con el segundo exacto del salto | Un salto temprano indica que la recomendación no encajó con el gusto del usuario | Reentrenar el algoritmo de recomendación sin depender de calificaciones explícitas |
| Cloudflare | Volumen y origen de solicitudes HTTP por segundo | Un pico anómalo de tráfico desde pocas IPs indica un ataque DDoS en curso | Activar mitigación automática en tiempo real |
| Tesla | Métricas de batería/motor procesadas localmente, solo se envían resúmenes y anomalías | Si más del 0.1% de la flota muestra el mismo patrón anómalo, hay un problema sistémico, no un caso aislado | Disparar una actualización OTA que ajuste la gestión de batería antes de la falla |
| DHL | Temperatura de un paquete en tránsito | Superar 30°C indica riesgo de daño a la mercadería | Disparar alerta para intervención humana antes de la entrega |

Usar esta tabla como guion en el aula: leer la fila completa en voz alta transmite mejor la lógica que solo nombrar la empresa.

### 1.2 Error común a corregir en clase

> "Spotify sabe todo lo que escuchás" no es una explicación técnica, es una afirmación de marketing.

La versión correcta, que hay que modelar frente al grupo:

> "Spotify captura el evento `track_skipped` con el segundo exacto del salto porque necesita saber si la recomendación falló temprano (antes del estribillo) o tarde (canción ya escuchada varias veces), lo que le permite decidir qué peso darle a esa señal en el algoritmo de recomendación."

## 2. Cómo diferenciar stream (tiempo real) de batch sin ambigüedad

### 2.1 La pregunta guía

Antes de cualquier definición técnica, plantear siempre la misma pregunta de negocio:

> **¿Alguien tiene que actuar sobre este dato en segundos o minutos, o puede esperar horas o días sin que eso cause un problema?**

- Si la acción es urgente (bloquear una transacción, alertar a un conductor que excede velocidad, mitigar un ataque DDoS) → **stream**.
- Si la acción puede esperar (revisar un informe semanal, analizar una tendencia mensual) → **batch**.

Esta pregunta evita que el grupo memorice la tabla de compensación de resume_01 sin entender por qué existe. La tabla es la consecuencia de la pregunta, no el punto de partida:

| Aspecto | Procesamiento en flujo (stream) | Procesamiento por lotes (batch) |
|---|---|---|
| Latencia | Baja (tiempo real) | Alta (retrasada) |
| Costo | Alto (sistemas siempre activos) | Bajo (procesamiento periódico) |
| Formato de datos | Eventos individuales | Arreglos de eventos en lotes |
| Pregunta que lo justifica | "¿Hay que actuar ya?" | "¿Puede esperar?" |

### 2.2 El error de confusión más común: modelo de procesamiento vs mecanismo de transporte

Este es el punto donde más se confunden los desarrolladores nuevos en telemetría, y conviene aclararlo explícitamente en clase:

> **Stream vs batch responde "¿cuándo proceso este dato?". HTTP POST, WebSockets o `sendBeacon` responden "¿cómo lo envío?". Son decisiones independientes.**

Ejemplo para desarmar la confusión en el aula:

- Se puede enviar cada evento por separado vía HTTP POST (mecanismo de transporte discreto) y aun así **acumularlos en el servidor y procesarlos juntos cada hora** (modelo de procesamiento batch).
- Se puede mantener una conexión WebSocket abierta (mecanismo de transporte persistente) y **procesar cada evento apenas llega** (modelo de procesamiento stream).

Es decir: el transporte es el "cómo viaja el dato" y el modelo de procesamiento es el "cuándo se analiza". Confundirlos lleva a errores de diseño típicos, como asumir que "usar WebSockets" ya implica que el sistema es de procesamiento en flujo, cuando en realidad depende de qué hace el backend con esos eventos al recibirlos.

### 2.3 Checklist de dos pasos para decidir en clase (y en el proyecto)

Para cualquier evento nuevo que el grupo proponga, aplicar este checklist en orden:

1. **¿Este evento se dispara con demasiada frecuencia?** (cada tecla, cada scroll, cada movimiento del mouse). Si sí, primero hay que resolver la frecuencia de envío con **debounce**, **throttle/rate limiting** o **sampling**, antes de pensar en stream o batch. Enviar sin limitar satura cualquiera de los dos modelos.
2. **¿La decisión que habilita este evento tolera minutos/horas de retraso, o necesita segundos?** Esta pregunta, y no una preferencia técnica del equipo, es la que determina si el evento va por stream o por batch.

Este checklist reproduce en miniatura las cuatro decisiones arquitectónicas del bloque 4 de resume_01 (dónde procesar, cómo transportar, con qué frecuencia, qué modelo), aplicadas evento por evento, que es exactamente lo que el proyecto `ai-eng-telemetry-plan` pide justificar en su fase 3 ("Estrategia de entrega").

### 2.4 Ejercicio guiado con el caso del buscador (para reforzar el checklist)

Retomar el ejemplo del cuadro de búsqueda (bloque 2 de resume_01) y resolverlo en vivo con el checklist de 2.3:

> Un usuario escribe "fastapi tutorial" (16 caracteres) en un buscador. Cada tecla dispara un evento `search_input_changed`.

- **Paso 1 (frecuencia):** 16 eventos por una sola búsqueda es demasiado. Aplicar **debounce**: esperar a que el usuario deje de escribir por ~300-500ms y enviar un solo evento con la consulta final.
- **Paso 2 (urgencia de la decisión):** una vez resuelta la frecuencia, ¿el análisis de qué buscan los usuarios necesita segundos o puede esperar? En este caso, casi siempre **batch** (informe de términos más buscados), salvo que el negocio use la búsqueda para autocompletado en vivo, en cuyo caso sí requeriría **stream**.

Esto muestra al grupo que ambos pasos son necesarios y en ese orden: limitar frecuencia primero, elegir modelo de procesamiento después.

## 3. Guion ampliado por dominio (para usar tal cual en el aula)

### 3.1 Telemetría de producto

> "Cuando hablamos de telemetría de producto, la pregunta no es '¿qué hizo el usuario?' sino '¿qué patrón de comportamiento, repetido en miles de usuarios, revela algo que ninguno de ellos reportaría en una encuesta?'. Netflix no le pregunta a nadie por qué abandonó un episodio: lo infiere del punto exacto donde se detuvo la reproducción."

Frase de cierre útil para conectar con la mentalidad de hipótesis primero:

> "Si un evento de producto no cambia una decisión de diseño, contenido o priorización, es ruido, no telemetría."

### 3.2 Telemetría de sistemas y seguridad

> "Acá el volumen cambia de escala: la telemetría de sistemas puede ser de 10 a 100 veces el volumen de la de producto, y se genera automáticamente en cada request, no por una acción deliberada del usuario. Por eso Cloudflare, procesando 50 millones de solicitudes por segundo, necesita analizar patrones de ataque en tiempo real, no en un informe semanal."

Para diferenciar SIEM de EDR frente al grupo, usar esta comparación directa:

> "SIEM correlaciona eventos entre múltiples fuentes — firewall, servidores, red — para detectar un patrón de ataque distribuido, como un login fallido seguido de un escaneo de puertos desde la misma IP. EDR, en cambio, mira un solo endpoint en detalle: qué proceso se ejecutó, qué archivo se escribió, qué conexión de red se abrió. Uno busca el patrón amplio, el otro la evidencia fina en un punto."

### 3.3 Telemetría del mundo físico

> "Acá el edge processing no es una optimización opcional, es una necesidad física: Waymo genera terabytes de datos de sensores por hora, y sería imposible (y carísimo) mandar todo eso a la nube sin analizar nada localmente. Por eso Tesla procesa batería y motor a bordo, y solo sube a la nube resúmenes comprimidos y anomalías."

Pregunta de cierre para conectar con mantenimiento predictivo:

> "Si DHL solo revisara la temperatura de un paquete al llegar a destino, ¿qué tipo de decisión perderían la posibilidad de tomar?" (Respuesta esperada: la de intervenir a tiempo, antes de que el daño ya esté hecho — la diferencia entre mantenimiento predictivo y constatar el daño después).

## 4. Rúbrica rápida para autoevaluar la explicación en clase

Antes de pasar al siguiente bloque de la agenda, el profesor puede chequear en 10 segundos si la explicación de un ejemplo fue completa:

- [ ] ¿Se nombró el evento observable de forma concreta (no una generalidad tipo "mide el comportamiento")?
- [ ] ¿Se formuló la hipótesis como pregunta, no como afirmación?
- [ ] ¿Se explicitó la decisión que ese dato habilita?
- [ ] Si el ejemplo involucra stream/batch, ¿se justificó con la pregunta de urgencia de la decisión, y no con "porque es más rápido"?
- [ ] Si el evento es de alta frecuencia, ¿se mencionó primero cómo limitarlo (debounce/throttle/sampling) antes de discutir el modelo de procesamiento?

Si alguna casilla queda sin marcar, es la señal de volver sobre ese ejemplo antes de avanzar con la agenda de resume_01.
