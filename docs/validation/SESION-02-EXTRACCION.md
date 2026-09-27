# Sesión 02 con el trader: extracción de respuestas (PLANTILLA)

> **Borrador. Nada se resuelve sin revisión del consultor.**

Rama `trabajo/sesion-02`. Plantilla SIN contenido: se rellena después de la sesión, y solo desde la versión FILTRADA que produce `scripts/transcribir_sesion.py` (`<audio>.filtrada.md`, fuera del repositorio). La cruda (`<audio>.cruda-NO-LEER.*`) no se abre, no se cita y no entra en el repositorio, igual que el audio. Un tramo `[CUARENTENA mm:ss–mm:ss]` no se reconstruye, no se escucha y no se pregunta: si una respuesta cae dentro, la pregunta queda NO RESPONDIDA y se dice que cayó en cuarentena.

Cómo se rellena cada pregunta:

- **Cita:** el literal de la versión filtrada, entre comillas, con su `mm:ss` (minutos desde el inicio del audio). Si hay varias, una por línea. Nada parafraseado.
- **Lectura:** cuál de las lecturas documentadas elige (las opciones cerradas del registro están debajo de cada pregunta), o «NUEVA» con una frase que la describa. Una lectura nueva PARA (`docs/runbooks/ACTIVAR-A35-A44.md` §4): no se fuerza en la más cercana.
- **Claridad:** CLARA (responde la pregunta, en un sentido) · PARCIAL (responde a medias, con un ejemplo o en dos sentidos) · NO RESPONDIDA (no se preguntó, no contestó, o cayó en cuarentena).
- **Notas:** lo que el consultor tiene que saber para decidir (repreguntas hechas, dudas del ASR, si el código de la pregunta no se detectó y la respuesta se localizó a mano).

El orden es el de la hoja de la sesión 02 (`hoja-sesion-02.docx`, generada por `scripts/hoja_preguntas.py`) con A-46 justo después de A-21, que en la hoja impresa va escrita a mano. Las lecturas de A-35 y A-44 están en `docs/validation/PREPARACION-A35-A44.md`; las de A-21, en `docs/validation/PREPARACION-A21.md` y ADR-0055.

## Lo primero

### A-35 · cuándo un pivote de M15 está formado

Opciones del registro: `liquidez_m15_pivote_formado` (UNKNOWN): `inicio_vela_contraria` · `cierre_vela_contraria`.

- **Cita:** —
- **Lectura:** —
- **Claridad:** —
- **Notas:** —

### A-45 · en qué granularidad se evalúa «cierra con cuerpo» en la toma de liquidez de RN-004

Opciones del registro: `liquidez_m15_criterio_toma` (CONFIRMED): `cuerpo` · `mecha`.

- **Cita:** —
- **Lectura:** —
- **Claridad:** —
- **Notas:** —

### A-21 · que es una zona de control limpia, sin ruido

Opciones del registro: `zona_control_limpia` (UNKNOWN): `solo_una_zona_de_control` · `sin_mecha_mas_alla_del_extremo`.

- **Cita:** —
- **Lectura:** —
- **Claridad:** —
- **Notas:** —

### A-46 · si una toma de liquidez de una sesion anterior del mismo dia sigue valiendo en la siguiente

Opciones del registro: sin parámetro en el registro: lectura libre; si responde, se lleva al consultor.

- **Cita:** —
- **Lectura:** —
- **Claridad:** —
- **Notas:** —

### A-44 · magnitud y corte del tope de pérdida propio del trader (perdida_dia, perdida_semana)

Opciones del registro: `perdida_maxima_diaria` (CONFIRMED, porcentaje); `base_calculo_perdida_diaria` (CONFIRMED): `saldo_actual` · `saldo_inicial_dia`; `perdida_maxima_semanal` (CONFIRMED, porcentaje); `base_calculo_perdida_semanal` (CONFIRMED): `saldo_actual` · `saldo_inicial_semana` · `saldo_inicial_dia`; `perdida_trader_alcance` (UNKNOWN): `sin_tope` · `dia` · `semana` · `ambos`; `perdida_trader_magnitud` (UNKNOWN): `saldo` · `equity`; `perdida_trader_unidad` (UNKNOWN): `porcentaje` · `usd`; `perdida_trader_dia_usd` (UNKNOWN, decimal); `perdida_trader_semana_usd` (UNKNOWN, decimal); `perdida_trader_reinicio_huso` (UNKNOWN, texto).

- **Cita:** —
- **Lectura:** —
- **Claridad:** —
- **Notas:** —

### A-43 · si una liquidez de M15 tomada antes de las 7 cuenta para operar después

Opciones del registro: sin parámetro en el registro: lectura libre; si responde, se lleva al consultor.

- **Cita:** —
- **Lectura:** —
- **Claridad:** —
- **Notas:** —

### A-24 · que hace que marques un pivote de M15 y no otro

Opciones del registro: sin parámetro en el registro: lectura libre; si responde, se lleva al consultor.

- **Cita:** —
- **Lectura:** —
- **Claridad:** —
- **Notas:** —

### A-42 · con qué reloj cuenta el trader su horario de operar de 07:00 a 15:00

Opciones del registro: `huso_operativa` (CONFIRMED, texto).

- **Cita:** —
- **Lectura:** —
- **Claridad:** —
- **Notas:** —

## La liquidez de M15

### A-26 · el flujo de M15 cuando va contra el sesgo de H4

Opciones del registro: sin parámetro en el registro: lectura libre; si responde, se lleva al consultor.

- **Cita:** —
- **Lectura:** —
- **Claridad:** —
- **Notas:** —

### A-25 · la vida de la marca de liquidez de M15

Opciones del registro: `cartuchos_reinicio` (CONFIRMED): `siguiente_liquidez_m15` · `fin_de_dia` · `nunca`.

- **Cita:** —
- **Lectura:** —
- **Claridad:** —
- **Notas:** —

### A-32 · el nivel que al romperse con mecha invalida la entrada

Opciones del registro: `breaker_m1_criterio_ruptura` (CONFIRMED): `mecha` · `cuerpo`.

- **Cita:** —
- **Lectura:** —
- **Claridad:** —
- **Notas:** —

## La orden y el stop

### A-36 · en qué punto de la mecha va la orden límite

Opciones del registro: sin parámetro en el registro: lectura libre; si responde, se lleva al consultor.

- **Cita:** —
- **Lectura:** —
- **Claridad:** —
- **Notas:** —

### A-37 · en qué temporalidad se busca la vela contraria de la que sale el stop

Opciones del registro: sin parámetro en el registro: lectura libre; si responde, se lleva al consultor.

- **Cita:** —
- **Lectura:** —
- **Claridad:** —
- **Notas:** —

### A-29 · cuando nace la orden limite

Opciones del registro: `orden_limite_nace` (DEFAULT_AMBIGUOUS): `al_darse_el_esquema` · `al_tomarse_la_liquidez`.

- **Cita:** —
- **Lectura:** —
- **Claridad:** —
- **Notas:** —

### A-30 · la orden limite pendiente al llegar el fin de la ventana

Opciones del registro: sin parámetro en el registro: lectura libre; si responde, se lleva al consultor.

- **Cita:** —
- **Lectura:** —
- **Claridad:** —
- **Notas:** —

### A-38 · cuándo se da por anulada una orden límite que el precio deja sin llenar

Opciones del registro: sin parámetro en el registro: lectura libre; si responde, se lleva al consultor.

- **Cita:** —
- **Lectura:** —
- **Claridad:** —
- **Notas:** —

## La gestión de la operación

### A-18 · base sobre la que se mide el objetivo 1:3

Opciones del registro: `base_calculo_objetivo` (CONFIRMED): `caja_completa` · `riesgo_real`; `objetivo_rr` (CONFIRMED, decimal).

- **Cita:** —
- **Lectura:** —
- **Claridad:** —
- **Notas:** —

### A-13 · break even al toque o con cuerpo

Opciones del registro: `break_even_criterio_ruptura` (DEFAULT_AMBIGUOUS): `mecha` · `cuerpo`.

- **Cita:** —
- **Lectura:** —
- **Claridad:** —
- **Notas:** —

### A-31 · el stop entero de una entrada que se activo sin ruptura

Opciones del registro: sin parámetro en el registro: lectura libre; si responde, se lleva al consultor.

- **Cita:** —
- **Lectura:** —
- **Claridad:** —
- **Notas:** —

### A-40 · qué se hace con el stop después del break even

Opciones del registro: sin parámetro en el registro: lectura libre; si responde, se lleva al consultor.

- **Cita:** —
- **Lectura:** —
- **Claridad:** —
- **Notas:** —

### A-33 · tres ganadoras que cierran por debajo de 3R

Opciones del registro: `parciales` (CONFIRMED): `si` · `no`; `objetivo_rr` (CONFIRMED, decimal).

- **Cita:** —
- **Lectura:** —
- **Claridad:** —
- **Notas:** —

## Para terminar

### A-34 · vela H4 previa que rompe ambos extremos

Opciones del registro: sin parámetro en el registro: lectura libre; si responde, se lleva al consultor.

- **Cita:** —
- **Lectura:** —
- **Claridad:** —
- **Notas:** —

### A-41 · si hay un tope de entradas por día, aparte de los cartuchos

Opciones del registro: sin parámetro en el registro: lectura libre; si responde, se lleva al consultor.

- **Cita:** —
- **Lectura:** —
- **Claridad:** —
- **Notas:** —

### A-39 · qué pasa con lo que viene de la primera sesión cuando la segunda cambia el sesgo

Opciones del registro: sin parámetro en el registro: lectura libre; si responde, se lleva al consultor.

- **Cita:** —
- **Lectura:** —
- **Claridad:** —
- **Notas:** —

## SIN PREGUNTA

Lo que el trader diga fuera de un código y sea relevante para alguna ambigüedad o regla: cita con `mm:ss` y a qué pregunta o regla apunta. Sin contenido todavía.

## Cómo se ejecuta mañana

1. Grabar la sesión con el permiso del trader dicho EN la grabación (regla 1 de la hoja).
   **Protocolo de voz, obligatorio: es lo único que el script entiende.**
   - Para ABRIR cada pregunta, decir en voz alta **«Pregunta A …»** con el código: «Pregunta A treinta y cinco», «Pregunta A cuarenta y seis». Sin la palabra «pregunta» delante, el código NO abre nada: un «A-35» suelto, o un «llega a treinta» del trader, no cambian de pregunta.
   - Para CERRAR, decir **«fin de pregunta»** al acabar cada una. Lo que se hable desde ahí hasta la siguiente «Pregunta A …» queda como SIN PREGUNTA.
   - Si se olvida abrir, la respuesta cae en la pregunta anterior (o en SIN PREGUNTA si se cerró): se localiza a mano en la filtrada (paso 5).
2. Copiar el audio (un solo fichero: m4a, mp3, wav, ogg, opus, mp4...) a `C:\Users\USER\Desktop\reunion-a35-a44\sesion-02-audio\`. La carpeta NO está dentro del repositorio, y así tiene que seguir.
3. Desde la raíz del repositorio, en la terminal:

   ```
   uv run python scripts/transcribir_sesion.py
   ```

   Sin argumentos procesa todos los audios de esa carpeta; con `--audio <fichero>` solo uno. Tarda del orden de 0,4 veces la duración del audio en la GPU de esta máquina (medido: 3 minutos en 65 s, con la carga del modelo; unos 45 minutos para 2 horas). No descarga nada: usa el modelo que ya está en la caché. Si la GPU falla, `--dispositivo cpu` (mucho más lento).
4. Abrir SOLO `<audio>.registro.txt` y `<audio>.filtrada.md`. El registro dice cuántos segmentos fueron a cuarentena, qué códigos se detectaron (con su primer `mm:ss`) y qué preguntas de la hoja no tienen código. No abrir `<audio>.cruda-NO-LEER.*`.
5. Si una pregunta no se abrió (el registro la lista en «preguntas de la hoja SIN codigo detectado»), su respuesta queda en la pregunta anterior o en SIN PREGUNTA: se localiza a mano DENTRO de la versión filtrada y se anota en «Notas».
6. Si hace falta ajustar el filtro (por ejemplo, una grafía nueva de un mes), se ajusta el script y se rehace la filtrada sin volver a transcribir: `uv run python scripts/transcribir_sesion.py --solo-filtrar`.
7. Rellenar esta plantilla en una rama, citando la filtrada. Registrar cada respuesta como feedback (`docs/runbooks/ACTIVAR-A35-A44.md` §1) solo después de la revisión del consultor.
