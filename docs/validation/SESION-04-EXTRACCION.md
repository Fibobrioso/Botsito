# Sesión 4 con el trader (v10): la extracción por pregunta

> **Borrador para el consultor. Esta rama NO resuelve nada**: no hay `feedback apply`, ni
> ambigüedades cerradas, ni cambios en la spec o en el motor. Cada «resuelve» de abajo es una
> propuesta sobre lo que dijo el trader; el destino de cada respuesta lo decide el consultor en otra
> rama (encargo del 2026-10-04, `docs/encargos/trabajo-sesion-04.md`).

Rama `trabajo/sesion-04`, abierta el 2026-10-04 desde `main` en `48f9701`
(`stable/F36u-historial-sin-git`). Skill `ingerir-sesion`, de principio a fin. Plantilla:
`SESION-03-EXTRACCION.md`.

## 0. Lo primero

**El día.** La línea de `SESION-DE-PREGUNTAS.md` («Antes», paso 1) con `2026-10-04` imprimió
`False`: el día de la grabación no es reservado.

**Los tramos que declaró Aleks.** Antes de transcribir se le preguntó en el terminal si el trader
habló de operaciones concretas de septiembre o de marzo, o si dio cifras en la pregunta de las
capturas de marzo. Respuesta: **«No, en ningún momento»**. No hubo tramos que declarar por ese
motivo antes de leer.

**El vídeo.** v10, `Grabación de pantalla 2026-10-04 105617.mp4`, 8.001.960.041 bytes, sha256
`12dff899…2e474b6b`, 2:07:36 (7656,2 s), 1918×1014 a 30 fps, con audio AAC estéreo a 48 kHz.
Registrado en `fuentes.yaml` con `drive_id: null` y `fecha_grabacion: "2026-10-04"`, e inventariado
(`manifest.yaml`; `corpus check --hashes` en verde). Está en `SESIONES_EN_CUARENTENA`.
- Transcripción `tr-v10-large-v3-int8-float16-85e8af79`: 1914 segmentos, mismo motor que los demás
  vídeos (ADR-0007). `corpus transcript check`: 15 transcripciones coherentes.
- Fotogramas `fr-v10-69219820`: 7657 a 1 fps, 0 extra. `corpus frames check`: 10 extracciones
  coherentes.

**El protocolo de voz SÍ se siguió esta vez.** Cada pregunta se abrió con «pregunta S…» y se cerró
con «S… cerrada». Pero la filtrada se agrupó con la hoja de la sesión 3, porque la guardia solo deja
ejecutar sobre una cruda el guion idéntico al de `main` (§1.2). Por eso la detección solo vio S-1
(a las 20:00, en realidad el cierre de S-1) y «A-18» (110:26, que es S-18 dicho sin la S). La
localización se hizo a mano por esos marcadores de voz, que están todos en la filtrada.

**Preguntas hechas: las 24, en el orden de la hoja** (S-1 … S-22, S-7 … S-21, S-23, S-24, S-19).
Ninguna se quedó sin preguntar. El resumen está en la tabla del §5.

**Los cinco hallazgos que más cambian el bot:**

1. **S-7, el reloj de invierno (A-42).** Desde el 25 de octubre: primera sesión de 6 a 10 y segunda
   de 10 a 2, en su reloj. Lo dijo después de mirarlo en su gráfico. La frase sigue en un bloque de
   cuarentena, y dos bloques de cuarentena rodean la respuesta (§2.1).
2. **S-24, el break even (A-13): no confirma lo que el bot hace.**
   - Confirma el stop exactamente en la entrada.
   - En su ejemplo lo pone cuando la vela **cierra** más allá del nivel, «si lo hace con cuerpo
     mucho mejor». Y el nivel sigue el criterio de validar un punto de breaker: esperar a que
     cierre por debajo del bajo más bajo.
   - Eso contradice el «apenas toca» de v6 0:57:01 y v9 0:55:43. La subpregunta de si después lo
     mueve cae en cuarentena.
3. **S-16: el backtest de agosto que vale es el GRABADO, el del vídeo** (E-1). El primero no
   incluía los break even. La premisa de la hoja («el completo es el original») era la contraria.
4. **S-14, la vela casi plana (RN-007): se contradice.**
   - Primero elige la (b): casi plana con 1 o 2 puntos de cuerpo o menos.
   - Al repetírsela, dice que con 1 o 2 puntos ya hay cuerpo «que se podría tomar en cuenta».
   - Lo único firme: la vela que abre y cierra en el mismo precio no cuenta.
5. **S-3 y S-4, la vida de la orden (A-18, A-49).**
   - El stop se pone ya en el 0,8; el 1 solo sirve «como planteamiento» del RR.
   - El objetivo es 3 veces la distancia del 0 al 1.
   - Con la orden sin llenar, el 1 de la caja se expande con cada máximo nuevo, mientras no se
     forme otro punto de breaker.

**Holdout.** Hay **21 tramos de v10** en `tramos_no_citables.yaml`:
- 4 sin audio;
- 12 de la cuarentena mecánica;
- 3 de precaución;
- 1 de conversación personal;
- 1 de precaución por un mes con días ocultos que la cuarentena mecánica no cubre (revisión del
  consultor, punto 2).

El trader enseñó en pantalla **su propio replay** (§2.3), y apareció un **hueco del filtro**: junio
de 2026 tiene días ocultos y la cuarentena mecánica no filtra «junio» (§2.4). Declarado en
`HOLDOUT-EXPOSICIONES.md` el mismo día. **Ningún fotograma de v10 se abrió** (§2.5).

## 1. Cómo se leyó

### 1.1 La transcripción y la filtrada

- `scripts/transcribir_sesion.py --audio` sobre el audio extraído sin recodificar a
  `C:\Users\USER\Desktop\sesion-04-audio\sesion-04.m4a`, fuera del repositorio. ASR de 1665 s
  (factor 0,22). Salen 1914 segmentos, los mismos que la transcripción del corpus.
- La cuarentena mecánica dio **45 segmentos en 12 bloques**: fecha numérica 2, mes 16, vecino 27.
  Solo se leyó la versión FILTRADA. La cruda no la abrió nadie.
- Citas: el literal de la filtrada, con su `mm:ss` (minutos totales) desde el inicio del audio.
- **La transcripción no separa voces.** El hablante se atribuye por contexto: la pregunta la lee
  el consultor y la respuesta es del trader. Donde una línea mezcla a los dos, se dice. Varias
  respuestas se dan leyendo en voz alta la pregunta con sus opciones («la B no…»), así que la línea
  trae las dos cosas.
- **Ítems de evidencia: 64**, todos `ev-v10-*`, creados con `botsito evidence new` (voz, extractor
  `llm`). Ninguno cae en un tramo no citable: el check los aceptó contra los 20 tramos ya escritos
  y, tras el punto 2 del consultor, otra vez contra los 21 (`knowledge validate`, §2.4).
  Uno se rehízo porque la cita llevaba tres comodines `[...]` y el máximo es dos.
  `botsito evidence contradictions`: 0 abiertas, porque ningún ítem lleva `valor`. Las
  contradicciones de sentido son las del §4.
- **Sin registros de feedback**, por el encargo.

### 1.2 La hoja de la sesión 4 en el guion, y por qué la filtrada se hizo con el de `main`

**Lo que se midió antes de tocar nada:**
- `codigos_validos()` devolvía las ambigüedades ABIERTA o DECIDIDA más `CODIGOS_DE_SESION`, que era
  `tuple(CODIGOS_DE_SESION_TEXTO)`: un único diccionario de la sesión 3.
- `orden_de_preguntas` y `registro_filtro` usaban la global `ORDEN_SESION = ORDEN_SESION_03`.
- Añadir S-1 … S-24 a ese diccionario habría pisado el S-1 de la sesión 3 («cómo decide el sesgo
  del día»). Habría dejado además E-1, E-2, E-3 y G-1..G-3 como válidos en la sesión 4.

**El cambio** (`scripts/transcribir_sesion.py`):
- `ORDEN_SESION_04`, con el orden del encargo.
- `CODIGOS_DE_SESION_TEXTO` POR SESIÓN (`"02"`, `"03"`, `"04"`): los títulos de la 04 son los de
  `PREGUNTAS.md` y los dos del encargo.
- `HOJAS` (sesión → orden) y `SESION_EN_CURSO = "04"`.
- `codigos_validos(sesion)`, y `orden_de_preguntas`, `version_filtrada` y `registro_filtro` reciben
  la hoja.
- Opción `--sesion {02,03,04}`, por defecto la en curso; el registro dice con qué hoja se agrupó.

**Tests** (`tests/unit/test_transcribir_sesion.py`):
- los de la 03 pasan su hoja explícita;
- 5 nuevos: el orden de la 04; S-1 con un texto por sesión; los válidos de cada sesión; «pregunta
  ese siete», «pregunta S veintidós», etc.; la filtrada de la 04 agrupada con su hoja.

**Roto a propósito.** Se añadió al módulo
`CODIGOS_DE_SESION_TEXTO["03"].update(CODIGOS_DE_SESION_TEXTO["04"])`, que es justo el diccionario
que se pisa. Caen 3 tests:
- `test_el_orden_es_el_de_la_hoja_de_la_sesion_03`;
- `test_s1_tiene_un_texto_por_sesion_y_la_hoja_03_no_cambia`;
- `test_los_codigos_validos_son_los_de_la_hoja_de_cada_sesion`.

Se restauró el fichero (sha256 `a0228b49…` antes y después) y vuelven a verde.

**La guardia bloqueó usar el guion nuevo sobre una cruda**, y es correcto que lo haga. Lo escribo
aquí porque cambia cómo se hizo la filtrada:
- `guardia.py` solo da por revisado un guion idéntico al blob de `main` (decisión del consultor
  del 2026-10-01). El cambiado nombra `.cruda-NO-LEER.jsonl`, y al ejecutarlo la guardia lo
  bloqueó: «el codigo nombra .cruda-NO-LEER.jsonl».
- No se rodeó. La transcripción y la filtrada de v10 se hicieron con el guion **de `main`** (código
  revisado): se apartó el cambio un momento con `git restore --source=main --worktree`, se comprobó
  `git diff --quiet main`, y se restauró la copia (mismo sha `a0228b49…`).
- La cuarentena es la misma, porque vive en `botsito.corpus.cuarentena`. Lo único que cambia es la
  agrupación, con la hoja de la 03.

**La comparación real con la sesión 3 queda PENDIENTE** hasta que el guion nuevo esté en `main`:
- Hoy hay una línea base: la filtrada de v9 rehecha con el guion de `main` tiene sha256
  `f7529459…a027b`, idéntica a la del 2026-09-29.
- Con el guion nuevo y `--sesion 03` debe salir la misma. No se pudo ejecutar aquí: la guardia lo
  bloquea.
- Lo que sí lo cubre aquí son los tests, con texto sintético.
- Al cerrar la rama, o en la siguiente: `--solo-filtrar --sesion 03` sobre v9 (sha esperado
  `f7529459…`) y `--solo-filtrar --sesion 04` sobre v10, que agrupará por S-n.

### 1.3 Los tests: no han bajado (revisión del consultor, punto 5)

Las dos cifras del informe miden cosas distintas.
- **1251** es el campo `Tests Currently Passing` de `PROJECT_STATE.md`, que cuenta **funciones de
  test** (`state check` lo compara con el recuento de funciones; antes de la rama, 1246).
- **1901 passed y 8 skipped** es la salida de **pytest** en la CI de Linux, que cuenta **casos**
  (las parametrizaciones, una a una) y salta los que necesitan `data/`.

**Las cifras, sacadas de su salida:**

| Ejecución | passed | skipped | deselected | failed |
|---|---|---|---|---|
| `make check` sellado de la rama (Windows, con `data/`; `make-check.log`, línea 64: «1919 passed in 661.94s») | 1919 | 0 | 0 | 0 |
| último `make check` de `main` (`48f9701`) | no se conserva: el log de esa máquina se sobrescribe en cada ejecución | | | |
| último run de CI de `main` que consta en HISTORIA (run 203, `cab9eb1`, Linux, sin `data/`) | 1901 | 8 | 0 | 1 (state check) |

Como el log local de `main` no se conserva, la suite de `main` se **recogió** (`pytest
--collect-only`) en un `git worktree` desechable de `48f9701`, y la de la rama en el árbol de
trabajo:
- **`main`: 1910 casos**, que son exactamente 1901 + 8 + 1 de la CI.
- **La rama: 1919 casos**, 9 más. Son las 5 funciones nuevas de `test_transcribir_sesion.py`, una
  de ellas parametrizada con 5 casos: 4 + 5 = 9.
- En funciones, 1246 → 1251 (+5).

**No ha bajado nada.** En local no hay skipped porque `data/` está en la máquina. La CI de esta rama
debe dar 1910 passed, 8 skipped y 1 failed (state check); va en el informe con su número de run.

## 2. Audio, cuarentena y holdout

### 2.1 Los cuatro cortes de audio

Medidos con `ffmpeg silencedetect` (-50 dB, 30 s) y `volumedetect`: los cuatro son **cero digital**
(-91 dB). Fuera de ellos no hay ningún silencio de más de 30 s.

| Corte | Qué hay alrededor | ¿Tapa una respuesta? |
|---|---|---|
| **45:05–46:41** (2705,8–2800,5 s) | 44:42 «Pro, ahora vengo, un minuto»; 44:44 «pregunta S3, cerrada»; 46:40 «Vale, continuamos» | No: cae entre S-3, ya cerrada, y S-4 |
| **1:30:51–1:35:48** (5451,6–5747,7 s) | 90:49 «Ahora vengo, bro, voy a tomar, calentarme.» en mitad de S-13 | Cae en una pausa anunciada; la respuesta de S-13 se da entera al volver (100:05) |
| **1:36:37–1:38:58** (5797,8–5937,6 s) | dentro de la misma pausa | No se puede saber si se dijo algo |
| **1:39:08–1:39:42** (5948,9–5981,6 s) | 99:41 «Volví.» | No |

- **Puerta del ASR:** entre 1:30:49 y 1:39:41 no hay ningún segmento. Tres marcas caen en el borde
  de un corte:
  - 46:40, en el último medio segundo del primero;
  - 46:41, ya fuera;
  - 99:41, en el último medio segundo del cuarto.

  Son el audio que vuelve, no texto inventado dentro del silencio. Se comprobó imprimiendo solo
  marcas de tiempo.
- Los cuatro están en `tramos_no_citables.yaml` con motivo «SIN AUDIO», y en la `naturaleza` y el
  comentario de v10 en `fuentes.yaml`.
- Hay además un corte **de la llamada, no de la grabación** (29:10–31:19, durante S-3): «estás
  callado hace un minuto», y el trader repite la respuesta. Y otro (33:11–34:55), un problema de
  micrófono. Lo dicho en ellos sí está grabado.

### 2.2 La cuarentena mecánica

Son 12 bloques: 00:58–01:12, 01:27–01:36, 40:08–40:19, 63:24–63:38, 64:56–65:28, 86:34–86:40,
86:44–86:50, 115:09–115:20, 115:58–116:02, 116:04–116:07, 126:42–127:02 y 127:04–127:11.

Están en `tramos_no_citables.yaml` con t1 un segundo después, para cubrir el último segmento. Llevan
los motivos agregados, porque sacarlos por bloque exigía un guion nuevo sobre la cruda, y la guardia
lo bloquea (§1.2). No se describe su contenido.

**Tres caen dentro de una respuesta:**
- **63:24–63:38 y 64:56–65:28, en S-7.** El arranque de la respuesta y el final de la frase «la
  segunda sesión y el cierre también sería…».
- **126:42–127:02**: el final de S-24 («para precisar o si después de ponerlo en la entrada lo
  vuelves a…») y el arranque de S-19.

### 2.3 El replay del trader en pantalla

**Lo que se enseñó.** Los cuatro esquemas inventados de la hoja se enseñaron (S-2, S-4, S-11 y S-13;
el trader los comenta: «el ejemplo está bien / pero pasa que no me da más estructura», 23:09). Pero,
para responder, **el trader compartió su pantalla y su replay** de FX Replay, con operaciones
concretas comentadas en voz («aquí esta entrada yo la tomé … es un loss», 09:59). El encargo dice
«no hubo ningún gráfico de un día real»: eso vale para lo que enseñó Aleks, no para lo que enseñó
el trader.

**Los meses que nombra en voz:**
- agosto (01:18, «ah, agosto también lo tengo»);
- julio (26:36, 57:08, 108:58);
- enero (40:43, «me voy a enero»; 74:42, «este es enero»);
- diciembre (114:15).

`casos_ocultos` (2026-10-04): ningún día de 2025-12, 2026-01, 2026-07 ni 2026-08. No se abrió ningún
fotograma para fechar los ejemplos.

**Los tres tramos de precaución (ADR-0021 §2),** marcados al leerlos y declarados:
- **0:40:20–0:40:42**: «estos datos / es usando lo que te había comentado / solo a 20 días» y
  «aumenta el número de trades». Es un agregado de una cuenta suya, sin cifra, por el contexto de
  enero.
- **1:27:44–1:28:19**: el R de operaciones concretas de sus libros, leído en voz. El trader lo usa
  para explicar que FX Replay redondea el objetivo. Periodo no identificado.
- **1:56:07–1:56:19**: **el máximo de operaciones en un día de un libro suyo: 7**. Periodo no
  identificado, entre bloques de cuarentena. Las cifras están listadas en
  `HOLDOUT-EXPOSICIONES.md` y ninguna se usa.

  **Por decisión del consultor (2026-10-04, punto 3), este agregado se trata como EXPUESTO:**
  posible exposición de junio, un agregado de periodo no identificado. El consultor no lee la
  cuarentena: la cruda solo la lee Aleks. **La cifra no se usa en nada**: ni en un parámetro, ni en
  una estimación de mensajes a FTMO, ni en la resolución de S-20.

**El tramo de conversación personal.** 1:43:42–1:44:21 es una conversación ajena a la operativa,
con una persona de su casa y con el consultor. Va como no citable, sin describirla.

### 2.4 Un hueco del filtro: junio

- `casos_ocultos` da **True para 2026-06**: junio tiene días ocultos.
- La cuarentena mecánica (`MESES_FILTRADOS`) filtra septiembre, marzo, mayo y febrero, **no junio**.
- Si el trader hubiera dado cifras de junio, la filtrada las habría dejado a la vista. El máximo de
  7 de 116:07 se trata como expuesto (§2.3, punto 3 del consultor).

**La medida (revisión del consultor, punto 2), con la definición exacta.** Son los segmentos de la
filtrada de v10, fuera de los tramos ya ocultos, que nombran un mes con días en `casos_ocultos` que
no esté en `MESES_FILTRADOS`.
- **Cómo se midió:**
  - los meses con días ocultos salen de las fechas de `casos_ocultos`;
  - un mes cuenta como cubierto si `_RE_MES` (el patrón de `MESES_FILTRADOS`) casa con su nombre en
    español y en inglés;
  - cada línea de la filtrada se normaliza con `cuarentena.normalizar` y se busca el mes por su
    nombre en español, en inglés y por su abreviatura de tres letras.
- **Lo que imprime:** solo recuentos y marcas de tiempo, sin texto ni qué mes.
- **Resultado:** 3 meses con días ocultos, 2 cubiertos y **1 sin cubrir**. Aparece en **un solo
  segmento** de la filtrada fuera de los tramos: **1:55:29** (la línea siguiente empieza a 1:55:32).
- **Ese segmento:**
  - va a `tramos_no_citables.yaml` (1:55:29–1:55:32) con el motivo «precaución: mes con días
    ocultos que la cuarentena mecánica no cubre»;
  - su texto se quitó de este informe y de `HOLDOUT-EXPOSICIONES.md`;
  - al repetir la medida después, sale «YA OCULTO».
- **Evidencia:** ningún ítem `ev-v10-*` cae en él (el más cercano acaba a 1:55:04 y el siguiente
  empieza a 1:56:40), así que no hay nada que retirar.
- **El check de evidencia contra los tramos nuevos:** `knowledge validate` en verde, 501 ítems.
  La verificación de citas carga los tramos (`validation/contexto_evidencia.py`) y rechaza cualquier
  cita que caiga dentro.

**Lo que sigue:** una rama de cuarentena que oculte todo mes con días en `casos_ocultos` nombrando la
condición, no una lista (§6, pendiente a). Esta rama no toca `cuarentena.py` ni la guardia.

### 2.5 Fotogramas: ninguno

No se abrió ningún fotograma de v10.
- El único instante que habría servido es S-7, 64:09–64:34: el trader mira la vela de 4 horas «del
  25» para responder.
- Está entre dos bloques de cuarentena, y en v9 el trader asoció el cambio de hora al backtest de
  marzo, que está sin abrir. Abrir ese fotograma podría enseñar un gráfico de un mes sin sortear.
- Las demás respuestas se entienden por la voz.

**Decisión del consultor (2026-10-04, punto 4): el fotograma de S-7 no se abre.** Lo que hace falta
para A-42 va en el §4, punto 11.

## 3. Por pregunta

Formato: **Tramo** · **Citas** (literal de la filtrada) · **Regla general o ejemplo** · **«creo»** ·
**Compra y venta** · **Propuesta**. S-7 va la primera por el cambio de hora del 25 de octubre;
después, el orden de la sesión.

### 3.1 S-7 · Con qué reloj empiezas a las 7 en invierno (A-42)

- **Tramo:** 62:56 («S7 / pregunta S7») – 65:29 («S7 cerrado»). Cuarentena dentro: 63:24–63:38 y
  64:56–65:28.
- **Citas:**
  - 63:42–63:43 (consultor) «Tu primera sesión a qué hora empieza? / Necesitamos la respuesta segura
    no aproximada.»
  - 63:46–63:48 «Pues hasta, desde el 25 de octubre. / A ver, me voy a ir al InVube.»
  - 64:29–64:34 «sería de 6 a 10 / en lugar de 7 pasaría / de 6 a 10, después del día 25»
    (`ev-v10-010429-0c93f24a`)
  - 64:38–64:54 «claro, sería de aquí / a 10 y de 10 / a 2, ya no sería a 3 / sino a 2 / la segunda
    sesión / y el cierre también sería 10» (`ev-v10-010438-0d4e6798`)
- **Regla o ejemplo:** regla, con fecha de inicio (el 25 de octubre). La sacó mirando su gráfico
  (63:48–64:22) y no de memoria.
- **«creo»:** no en lo legible. Lo que va antes de 63:38 está en cuarentena.
- **Compra y venta:** no aplica (horario).
- **Propuesta: resuelve.** Opción (b), y la segunda parte también: desde el 25 de octubre,
  primera sesión de 6 a 10 y segunda de 10 a 2, en su reloj. Queda por leer en cuarentena el
  final de «…y el cierre también sería 10…». Coincide con lo de v9 («En invierno empieza», 1:07:40;
  «Sí» a las 6, 1:07:53).

### 3.2 S-1 · Cuándo pones la orden, una vez formado el mínimo (o máximo) en M1 (A-49)

- **Tramo:** 00:09 («Empezamos con S1») – 20:00 («pregunta S1 cerrada»). Cuarentena dentro:
  00:58–01:12 y 01:27–01:36.
- **Citas:**
  - 02:31–02:45 «un higher low / cuando cierre / o sea, me tire por debajo con mecho / con cuerpo /
    su lower low / bajo más bajo / entonces / ahí se validaría esto» (`ev-v10-000231-1a17fccd`)
  - 03:20–03:23 «Aquí no se podría actualizar porque no ha cerrado todavía por debajo / con mecha o
    con cuerpo, en M1.» (`ev-v10-000320-6f8ed151`)
  - 07:42 «Ahora, siempre el punto breaker va a ser el más reciente, el que genere, pues, la
    ruptura.» (`ev-v10-000742-cd9d76b1`)
  - 10:53 (consultor) «entonces esperas a que cierre una vela como tal.» / 10:59 «y yo espero que es
    a que se mitigue pues en caso bajista el lower low y en caso alcista el higher high el mismo
    comportamiento en compra que en venta exacto y ya» (`ev-v10-001059-18a772a5`; la línea mezcla
    la pregunta del consultor y el «exacto» del trader)
  - 11:52–11:56 «no existe algo que lo invalide, o sea, lo único / que invalidaría sería / Por
    ejemplo, en un caso del system no me llega a tomar el higher high y en un caso bajista no me
    llega a tomar el lower low.» (`ev-v10-001152-96076e60`)
- **Subpregunta (A-49), la caja con la vela cerrada o en formación:**
  - 13:17–13:31 «la caja iría desde aquí hasta aquí vale pero conforme se va a desarrollar una /
    vez me valide por ejemplo el alto más alto y cierre la vela ya puedo ir actualizando desde /
    este punto hasta este punto» (`ev-v10-001317-75e433f0`)
  - 16:28–16:33 «esperamos a que cierre la vela / esa vela / y lo trazamos desde allí»
    (`ev-v10-001628-59a9a476`)
  - 19:35–19:45 «tu cuadro de ganas estaría / trazado aquí, o si quieres, pues lo puedes /
    actualizar, porque obviamente se ve / el precio, o sea, como avanza lento / puedes actualizarlo
    / desde ese punto» (`ev-v10-001935-d0f4ce50`)
- **Regla o ejemplo:** la regla («siempre», «el mismo comportamiento en compra que en venta»),
  explicada con ejemplos de su replay (agosto, por el contexto).
- **«creo»:** solo sobre la pregunta (00:39) y sobre un ejemplo (06:42), no sobre la regla.
- **Compra y venta:** sí (05:11 «En el caso del cista, sería mitigar el alto más alto.»; 10:59).
- **Propuesta: resuelve en parte.**
  - Firme: no espera nada más que la validación del punto. La orden va en el punto en cuanto una
    vela de M1 cierra más allá del extremo anterior (el bajo más bajo en una venta), con mecha o
    con cuerpo. Lo único que impide ponerla es que no se tome ese extremo.
  - Subpregunta: la caja se traza con la vela **cerrada**, pero añade que «si quieres» se puede ir
    actualizando mientras avanza.
  - El «cierre con mecha o con cuerpo» de M1 hay que leerlo junto a S-2 y S-23.

### 3.3 S-2 · Cuándo un mínimo de M1 se convierte en tu punto de breaker (A-49) · esquema inventado

- **Tramo:** 20:04 («Pregunta S2») – 28:22 («pregunta S2 cerrada»).
- **Citas:**
  - 22:35–22:40 «la B no, porque puede ser de ambos colores / O sea, la otra es de ambos colores /
    Tiene que ver la mecha» (`ev-v10-002235-c99c53f3`)
  - 22:53–23:00 «El momento es en que se tome / En un flujo alcista / Se tome el higher high / Se
    marca»
  - 24:31–24:44 «entonces en qué momento pones aquí la orden pues pongo la orden aquí mismo cuando
    el precio pues / tome liquidez o sea en este higher high de aquí en m1 se complete … pero que me
    tome con mecha o» (`ev-v10-002431-b07d5a36`)
  - 26:06–26:12 «se llega a tomar el lower load más reciente en M1, como sea, que lo haga, / y
    luego, pues, para poder validar este máximo aquí.» (`ev-v10-002606-b18f1c77`)
- **Regla o ejemplo:** la regla, sobre el esquema inventado. Dice que al esquema «le falta
  estructura» (23:09–23:15) y añade un ejemplo de su replay (26:41–28:00, una operación suya
  perdedora).
- **«creo»:** no.
- **Compra y venta:** sí (25:47 «en una compra si sería lo mismo»).
- **Propuesta: resuelve en parte.** «Otra»: descarta la (b), porque no importa el color de la vela
  siguiente; descarta también la (c). El mínimo pasa a ser el punto donde se pone la orden cuando
  el precio toma en M1 el alto más alto anterior (venta), aunque sea con mecha. Coincide con S-1.

### 3.4 S-3 · El stop al poner la orden: ¿en el 1 o en el 0,8? (A-18)

- **Tramo:** 28:26 («pregunta S3») – 44:44 («pregunta S3, cerrada»). Hay un corte de la llamada,
  29:10–31:19 (el trader repite), y un bloque de cuarentena, 40:08–40:19.
- **Citas:**
  - 35:59–36:03 «O sea, ya cuando tú pones el stop / Para calcular el lotaje y todo / Sería
    directamente a 0.8» (`ev-v10-003559-211855b7`)
  - 37:06–37:21 «Es que el stop se actualizaría / O sea, se actualizaría a 0.8 / No estaría en el 1
    / Se usa el 1 al comienzo / Pero no de ejecución, sino como planteamiento / … Plantear el RR /
    Sería de un 1 a 3» (`ev-v10-003706-5b7055a2`)
  - 37:27–37:32 «si uno mueve el stop / Pues va a cambiar el lote / Pero como lo manejamos a 0.8 /
    O sea de 0 a 0.8»
- **Subpregunta (A-18), el objetivo sobre 0→1 o 0→0,8:**
  - 39:27–39:38 «se usa de 0 a 1 / para el cálculo de 1 a 3 / pero para / el cálculo ya de / para
    la toma de la operativa / se usa de 0 a 0,8» (`ev-v10-003927-2f6d9f48`)
  - 39:48–39:57 confirmación: «trazas por ejemplo el stop, el stop se mide / desde el 0 al 1 y de
    ahí trazas / el 1-3, ¿no?» «Sí, claro.»
  - En un ejemplo de enero, 42:28–42:36 «para poder ubicar el tp … me apoyo desde el nivel / del 0
    a 1 y lo ubico a 3» (`ev-v10-004228-53e84fd4`)
- **Regla o ejemplo:** la regla, repetida tres veces, y un ejemplo de enero (desarrollo).
- **«creo»:** no sobre la regla. 44:14 «esto creo que ya lo olvidaría» va sobre otra cosa de su
  cuenta.
- **Compra y venta:** no lo distingue (no hace falta).
- **Propuesta: resuelve.** Opción (a): el stop va ya en el 0,8 al poner la orden. El 1 solo sirve
  para plantear el RR. El objetivo es 3 veces la distancia 0→1 y el lote se calcula 0→0,8. Coincide
  con v9 1:02:32 y 1:03:11, y con v7 0:06:07 («primer cálculo … desde el punto 1»).

### 3.5 S-4 · Si el precio sube más antes de llenarse, ¿se mueve el 1 de la caja? (A-49) · esquema inventado

- **Tramo:** 46:41 («Pregunta S4») – 51:42 («S4 cerrada»).
- **Citas:**
  - 48:10 «la respuesta es otra tal cual»
  - 49:28–49:36 «Número 1, validamos el punto breaker / Sigue trazo de la caja / Entonces,
    trazaríamos la caja desde aquí / Y claro, al máximo nuevo»
  - 49:45–50:03 «Ahora, si ocurre una vela verde, otra vela verde / Pues simplemente lo vamos
    actualizando la caja / Mientras no se desarrolle otro punto breaker / … nosotros vamos
    actualizando o sea expandiendo pues el 1 conforme vaya subiendo / y aquí en este caso pues
    mantendríamos nuestro punto breaker aquí y nuestro 0 aquí» (`ev-v10-004945-59ebac47`)
  - 50:56 «si el máximo nuevo queda muy lejos cambia algo es no es indiferente si el máximo es /
    demasiado lejos o no» (`ev-v10-005056-1a55d5b4`)
  - 51:16–51:25 «Ahora, ¿en una compra es lo mismo con un nuevo mínimo? / Sí, es lo mismo /
    aplicando, eso sí, / las condiciones que expliqué aquí.» (`ev-v10-005116-2a9ff066`)
- **Regla o ejemplo:** la regla («simplemente lo vamos actualizando»), sobre el esquema inventado,
  que según él estaba «mal trazado» (48:23).
- **«creo»:** solo sobre la conexión (48:36).
- **Compra y venta:** sí.
- **Propuesta: resuelve.** Elige «otra», pero lo que describe es la (a): con la orden sin llenar,
  el 1 se expande al máximo nuevo mientras no se forme otro punto de breaker. El 0 y el punto se
  quedan, y la distancia no importa.
  - Que **el stop y el lote** se recalculen con el 1 no lo dice en S-4. Lo dice en S-3, de forma
    general (37:27).
  - Contradice la decisión 5 del ADR de F35 (`caja_se_fija`).

### 3.6 S-5 · La orden sin llenar al acabar la sesión o la ventana (A-30, A-39)

- **Tramo:** 51:45 («S5») – 56:18 («S5 cerrada»).
- **Citas:**
  - 54:27–54:48 «a ver si a las 11 / tienes la orden puesta que no se ha llenado … claro, se quita
    … sí, se quita, porque siempre se va a ir actualizando / la orden, como te digo / o sea, no va a
    haber órdenes / que a lo mejor se pueden tomar a las 3 o fuera / de horario, ¿no? Entonces se
    quita tanto a las 11 / como a las 3, perfecto. Exacto.» (`ev-v10-005427-1a0867af`; la última
    frase es del consultor y el «Exacto» del trader)
  - 54:51–55:10 (consultor) «Si la quitas / es un minuto antes, como la operación / abierta o justo
    a la hora.» … «un minuto antes, lo habíamos / dicho un minuto antes, sí.»; 55:49 «Se cierra, sí,
    un minuto antes»
- **Subpregunta (A-39):** 56:03–56:11 «Si a las 11 el sesgo de 4 horas cambia / ¿Qué haces con la
  orden que traes en la primera sesión? / Se quita, ¿verdad? / … / Sí, se quita»
  (`ev-v10-005603-6a62fca7`)
- **Regla o ejemplo:** la regla.
- **«creo»:** 52:58 y 53:22 «creo yo», pero sobre otra cosa: que no le han pasado dos órdenes
  cruzadas.
- **Compra y venta:** no aplica.
- **Propuesta: resuelve.** Opción (a): la orden sin llenar se quita a las 11 y a las 3. Si a las 11
  cambia el sesgo de H4, también se quita.
  - «Un minuto antes» es dudoso: es la frase del consultor y el «sí» puede ser de cualquiera de los
    dos, así que no se propone.
- **Aparte, no es regla:** 55:12–55:46 «esa vez que me planteaste de si dejar la operativa abierta
  para la siguiente sesión … creo que influye … hay muchos trades a favor de nosotros si dejamos el
  trade abierto … Eso ya lo veremos luego / Te lo comento así por comentar». Es una idea, y en sus
  libros siempre cerró.

### 3.7 S-6 · «Lo mínimo posible» al redondear el stop: ¿un punto o un pip entero? (ADR-0061 §2)

- **Tramo:** 56:21 («S6») – 61:52 («S6 cerrada»).
- **Citas:**
  - 56:59 «vale, yo diría otra cual / porque va a variar siempre»
  - 57:34–57:45 «Por más que uno intente trazar a 0.8 / O tienes, o te bota más abajo / O te bota
    más arriba / O sea, a un pip / O sea, es justo a un pip / Siempre se va a manejar a un pip»
  - 58:47–59:08 «A 0.8 no llega exacto / Tira para abajo / … O sea, siempre es a un pip, se va a
    manejar a un pip / pero siempre tirando por debajo / o sea, por debajo si buscamos una
    operativa / alcista y por arriba si buscamos una operativa / bajista»
    (`ev-v10-005847-b4097030`)
  - 61:10–61:29 «¿Cuántos pips tiene eso? / 1.3 / O sea, tiene 1.3 pips / Sí / Por eso, si
    pusiera 1 arriba, sería 2.3 pips / Ah, vale, no, no, sí, sería 0.1, sí / Un punto, por eso /
    Sí, un punto, un punto» (`ev-v10-010110-8d6830a9`)
  - 61:41–61:46 «entonces, un punto, ¿no? o sea, tomando este ejemplo / un punto, un punto, sí /
    sería del 0.37 al 0.38 / sí, un punto, sí» (mezcla)
- **Regla o ejemplo:** la regla (hacia fuera), con un ejemplo de su replay (julio, 57:08).
- **«creo»:** no.
- **Compra y venta:** sí (por debajo en compra, por arriba en venta).
- **Propuesta: resuelve en parte.**
  - La dirección es firme: hacia fuera.
  - La cantidad: dice «un pip» varias veces y, cuando el consultor le hace la cuenta con un stop de
    1,3 pips, corrige a **un punto** (0,1 pip). Es la opción (a), pero llegó tras una corrección;
    el consultor decide si basta.

### 3.8 S-22 · Dónde va la orden de entrada frente al 0 de la caja (A-36)

- **Tramo:** 61:54 («S22») – 62:54 («S22 cerrada»).
- **Citas:**
  - 62:14–62:26 «exactamente en el 0 contando / la mecha / Exactamente, sí / Para precisar, si va
    más allá son siempre los mismos puntos / O depende de algo / No depende de nada, siempre es la
    mecha / O sea, de mecha a mecha siempre va a ir» (`ev-v10-010214-23a7fc0c`)
  - 62:28–62:33 «¿Tienes en cuenta el split al ponerla? / No, no tengo en cuenta el split al
    ponerla» (`ev-v10-010228-868271ee`)
  - 62:40–62:48 «La orden va en / … / Exactamente, cero / o sea, me echa del cero de la caja»
- **Regla o ejemplo:** la regla («siempre», «no depende de nada»).
- **«creo»:** no.
- **Compra y venta:** no lo distingue («siempre»).
- **Propuesta: resuelve.** Opción (a): la orden va exactamente en el 0 de la caja, contando la
  mecha, y sin tener en cuenta el spread. C6 (la orden puesta unos puntos más allá en pantalla,
  `DISENO-ENTRADA-RUPTURA.md` §2.8) queda sin explicar.

### 3.9 S-8 · Qué corta la racha de 9 pérdidas y cuándo vuelves a operar (A-51)

- **Tramo:** 65:32 («Pregunta S8») – 68:18 («s 8 cerrada»).
- **Citas:**
  - 65:49–66:04 «estas 9 pérdidas / No tenemos como condicional por el hecho de que / … La racha
    de pérdidas más extensa que hemos tenido / no sabemos a lo mejor posteriormente pues puede
    haber una de 10»
  - 66:53–67:05 «como máximo una racha de pérdidas, una racha de nueve pérdidas, como máximo. /
    Esto es por la condicional que nos da la cuenta de fondeo.» (`ev-v10-010653-81316808`)
  - 67:15–67:36 «un break even no se cuenta como cartucho como lo habíamos comentado con
    anterioridad … vamos por el séptimo trade en pérdida / luego nos sigue un break even no corta
    la racha como tal … después de break even es una pérdida pues ahí nuevamente lo contamos como
    otra» (`ev-v10-010715-fae17215`)
  - 68:04–68:18 «sería el día siguiente operaría / ya es al día siguiente aunque las rachas sigue de
    un día a otro y una semana otra la racha sigue de / un día a otro» (`ev-v10-010804-5b6ad1a3`;
    la línea mezcla lectura y respuesta)
- **Regla o ejemplo:** la regla, con un ejemplo (la séptima pérdida).
- **«creo»:** no.
- **Compra y venta:** no aplica.
- **Propuesta: resuelve.** Opción (a) en la primera parte: un break even no corta la racha. Opción
  (a) en la segunda: tras la novena, vuelve al día siguiente. La racha sigue contando de un día a
  otro.
  - **Para el consultor:** las 9 son la racha más larga que ha tenido y vienen de «la condicional
    de la cuenta de fondeo» con un 0,5 % por operación. Dice que con 0,3 o 0,2 % «podríamos
    extender» (66:19–66:24).

### 3.10 S-9 · El tope de pérdida: ¿porcentaje o 9 seguidas? (A-44)

- **Tramo:** 68:18 («pregunta s 9») – 70:44 («S9 cerrado»).
- **Citas:**
  - 68:35–68:50 «es que se complementa podría decirlo por si manejamos a / a un 0.5 la cuenta / y
    tenemos nuestro / tope límite, como digo, 9 / rachas sería 4.5, como máximo / perder»
  - 69:13–69:18 «Ah, no, aquí hay un error / No sería un 9% a la semana / Sería un 4,5% de pérdida
    en el día» (`ev-v10-010913-c4949417`)
  - 69:23 «No recuerdo muy bien eso, pero 9% a la semana»; 69:33–69:37 «Más que nada nos enfocamos
    en la pérdida diaria / Que sería a 4,5»
  - 69:50–69:57 «para parar en un día pues con perder el / 4.5 paramos / Hasta el día siguiente.
    Ahora, las dos cosas, lo que llegué antes, bueno, o sea, la respuesta es la, vamos a marcar la
    D, pero con la condicional de eso, de perder un 4.5 en un día.» (`ev-v10-010950-7e5543df`)
  - 70:21–70:36 «la semana del 9% de pérdida contempla de lunes a viernes. / o desde que empezó la
    racha de pérdidas / bueno, sería desde que empezó / la racha de pérdidas, ¿no?»
    (`ev-v10-011021-02f5dcf3`, confianza baja)
- **Regla o ejemplo:** la regla, pero con dudas («No recuerdo muy bien eso»).
- **«creo»:** no; sí «No recuerdo muy bien».
- **Compra y venta:** no aplica.
- **Propuesta: resuelve en parte.**
  - Las 9 seguidas y el 4,5 % se complementan: 9 × 0,5 % = 4,5 %. Para el día con perder el 4,5 %,
    hasta el día siguiente. Marca «las dos cosas, lo que llegue antes», que es la (c), aunque dice
    «D».
  - Lo del 9 % semanal de la sesión 1 lo llama «un error», pero luego no lo recuerda.
  - Desde cuándo cuenta la semana: dudoso, con un «¿no?».

### 3.11 S-10 · Zona limpia (A-21)

- **Tramo:** 70:47 («pregunta S10») – 81:49 («pregunta s 10 cerrada»).
- **Citas:**
  - 77:25–77:30 «¿una zona se limpia si hay velas verdes y rojas o terrenos rojos? / ¿Es solo eso?
    / Claro, exacto.» (`ev-v10-011725-3741e266`)
  - 77:34–77:39 «Para precisar, en el esquema 2, ¿cuántas velas puede tener como máximo el
    retroceso? / ¿Una, dos, tres, no importa, u otra? / Eso es indiferente, no importa»
    (`ev-v10-011734-fedd3f8e`)
  - 77:42–77:46 «¿Tú ves las seguidas de colores distintos y ensucian la zona? / Sí»
  - 79:57 «se alterna de una vela verde a una vela roja, entonces ya allí ya quedaría invalidado
    ya, o sea quedaría invalidado porque lo está haciendo antes de la ruptura del posible punto de
    breaker» (`ev-v10-011957-7ebb3453`)
  - 77:08–77:12 «¿cómo se ha desarrollado el rompimiento dentro del posible punto breaker? / Pues
    quedaría invalidado, porque no es igual a los esquemas que tenemos planteados.»
- **Regla o ejemplo:** la regla, explicada con los dos esquemas de entrada dibujados y con ejemplos
  de su replay (enero, 74:42).
- **«creo»:** solo sobre los ejemplos (80:37) y «creo que ya queda claro» (81:37).
- **Compra y venta:** sí (80:27 «y lo mismo sería para de alcista bajista»).
- **Propuesta: resuelve.**
  - Pregunta 1: opción (a). Una zona está limpia si no hay velas verdes y rojas alternándose, y es
    solo eso. Si se alternan antes de la ruptura del posible punto de breaker, la entrada queda
    invalidada aunque luego rompa.
  - Pregunta 2: opción (c). El número de velas del retroceso del esquema 2 no importa.

### 3.12 S-11 · El alto de M15 que el precio supera un poco (A-35) · esquema inventado

- **Tramo:** 81:49 – 85:40. El trader dice «pregunta s12 cerrada»; el ASR o el trader confunden el
  número.
- **Citas:**
  - 82:49–82:51 «¿Sigo usando el mismo alto? / Marco, depende / No» (lectura entrecortada)
  - 83:58–84:06 «Esta toma de aquí / No nos dice nada / Porque sabemos que / La regla es que tiene
    que ser / Con cuerpo / O sea, con cuerpo, tomar con cuerpo» (`ev-v10-012358-df6b36d2`)
  - 84:56–85:00 «marcas un alto en m15 después el precio lo pasa por poco con la mecha y / vuelve
    que haces pues no tiene la regla es que lo tiene que pasar con cuerpo no con mecha»
    (`ev-v10-012456-9dc1d221`)
  - 85:09–85:17 «ya actualizaría obviamente mi nuevo alto estaría por allí»
  - 85:26–85:33 «y si lo pasa con cuerpo / es que lo tiene que pasar con cuerpo es una verdad
    absoluta es lo mismo como un bajo de m15» (`ev-v10-012526-15de61b8`)
- **Regla o ejemplo:** la regla («verdad absoluta»), sobre el esquema inventado, que según él
  «está erróneo».
- **«creo»:** no.
- **Compra y venta:** sí (un bajo de M15, «al revés»).
- **Propuesta: resuelve en parte.** Elige «otra». Una superación del alto de M15 con mecha no
  cuenta; tiene que ser con cuerpo, y con cuerpo actualiza al alto nuevo. **Qué alto sigue valiendo
  tras la mecha** solo se deduce: no dice literalmente «sigo usando el mismo». Es la (a) por
  descarte, pero no lo dijo.

### 3.13 S-12 · Las salidas por encima de 3 R (G-2, A-33)

- **Tramo:** 85:40 – 89:21 («pregunta ese 12 cerrado»). Cuarentena dentro: 86:34–86:40 y
  86:44–86:50; tramo de precaución 87:44–88:19.
- **Citas:**
  - 85:55–86:09 «si nunca, el objetivo es fijo, como bien / sabemos, bro, ahora no lo gestionamos
    / es fijo»
  - 86:40–86:42 «Eso creo que es un planteamiento / O sea, algo que yo he añadido pero a futuro»
  - 86:54 «Claro, esto lo dije en los primeros videos»
  - 87:04–87:32 «incrementar tu take profit pero qué pasa después lo hemos dejado así o sea no no
    vamos a tratar / de maximizar porque hay alguien a veces o no tenemos una regla objetiva para
    poder decidir … pues no no vamos a dejar correr nada por ahora» (`ev-v10-012704-d3facd31`)
  - 89:02–89:15 «todo es 13 o sea fijo es 13 la regla es esa … es un / modo 3 tomando en cuenta que
    es de respecto al 1 de la caja no no no no exacto exacto exacto» (`ev-v10-012902-257afe4b`;
    la confirmación del trader a la frase del consultor)
- **Regla o ejemplo:** la regla. Las salidas por encima de 3 R de sus libros las atribuye a cómo
  redondea FX Replay (tramo de precaución, sin citar).
- **«creo»:** 86:40, sobre lo que dijo antes, que llama «un planteamiento … a futuro».
- **Compra y venta:** no aplica.
- **Propuesta: resuelve.** Opción (a): nunca deja correr. El objetivo es fijo, 3 veces respecto al 1
  de la caja. Lo de los primeros vídeos lo deja de lado («por ahora»). Coincide con v9 1:00:53.

### 3.14 S-13 · La vela de 4 horas que rompe por los dos lados y cierra sin cuerpo (ADR-0060 §2) · esquema inventado

- **Tramo:** 89:29 («pregunta ese 13») – 101:49 («Pregunta S13 cerrada»). Pausa 90:49–99:41, con
  los tres cortes de audio.
- **Citas:**
  - 89:57 «en forex hasta ahora no lo he vuelto a ver»
  - 100:05–100:40 «si esta es una vela neutra, no tiene ningún color, / nosotros seguiríamos
    operando alcistas esto es con la única condición con la condicional de si / éste es una vela
    neutra o sea no tiene color» (`ev-v10-014005-7e2228f4`)
  - 100:40–100:53 «ahora si es una vela roja entonces nuestro sesgo / sería bajista a la siguiente
    … si esta / vela termina en color verde entonces nuestro sesgo sería alcista»
    (`ev-v10-014040-fb7a153b`)
  - 101:01–101:29 «y si tiene un cuerpo muy / pequeño, de uno o dos puntos / … si termina en
    verde, pues / continuidad alcista, si termina en roja / … este sería / el sesgo bajista»
- **Regla o ejemplo:** la regla («con la única condición»), dicha sobre un sesgo previo alcista y
  «suponiendo que … no haya otro rango mayor».
- **«creo»:** 89:37, sobre lo raro que es («creo hasta ahora no nos ha tocado»), no sobre la regla.
- **Compra y venta:** solo dicho con un sesgo previo alcista. El caso bajista se deduce.
- **Propuesta: resuelve.** Opción (c): una vela de H4 neutra, sin color, mantiene el sesgo que
  había. Con un cuerpo de 1 o 2 puntos ya cuenta su color.

### 3.15 S-14 · El umbral de la vela casi plana (RN-007)

- **Tramo:** 101:49 – 105:50 («Pregunta S14 cerrada»). Tramo no citable 103:42–104:21
  (conversación personal).
- **Citas:**
  - 103:10–103:29 «Bueno, ahí sería plana, o sea, si abre y cierra en el mismo precio es plana, o
    sea, es una vela neutra y doji. / Es casi plana con 1 o 2 puntos, bueno, sí, podría
    considerarse casi, entre comillas, casi plana con 1 o 2 puntos del cuerpo o menos. / Sí, la B.
    Bueno, todas están correctas. / la A no está correcta» (`ev-v10-014310-2296423b`)
  - 104:38–104:54 «si abre y cierra en / el mismo precio no se toma en cuenta esa vela usar es como
    si no existiera ahora si es casi / plana con 12 puntos ahí sí habría un pequeño cuerpo sea el
    sista bajista que se podría tomar / en cuenta» (`ev-v10-014438-95464201`)
  - 105:39–105:47 «¿solo cuerpo o también las mechas? / Depende del contexto, pero por lo general
    es de mecha a mecha. / Aguarda, depende, ¿no? / Ah, no, sí, sí, sí.»
- **Regla o ejemplo:** la regla, pero dicha dos veces de forma distinta.
- **«creo»:** no, pero «entre comillas», «todas están correctas» y «podría».
- **Compra y venta:** no aplica.
- **Propuesta: resuelve en parte, con contradicción.**
  - Firme: la vela que abre y cierra en el mismo precio no cuenta.
  - Sobre 1 o 2 puntos se contradice: primero (b), casi plana; luego, que con 1 o 2 puntos «hay un
    pequeño cuerpo … que se podría tomar en cuenta».
  - Relacionado (102:39): «yo estoy usando / los datos de Oanda». El color de una vela casi plana
    puede cambiar de un proveedor a otro (A-16).

### 3.16 S-15 · Una liquidez tomada antes de las 7 (A-43)

- **Tramo:** 105:51 («Pregunta S15») – 108:05.
- **Citas:**
  - 106:13–106:19 «si el precio toma ese liquidez antes de tu horario, ¿lo usas para operar a
    partir de las 7? / Sí.» (`ev-v10-014613-6cf002b2`)
  - 106:37–106:39 «Vale, siempre la liquidez se va a ir actualizando / Vamos a tratar de tomar la
    más reciente» (`ev-v10-014637-70d27645`)
  - 107:05–107:15 «La liquidez aquí / Es a las 6 y / Iniciamos a atrasarlo / Desde las 6 y media /
    Pero la operativa / Como digo / Se tiene que dar / Dentro de la zona horaria / O sea, a partir
    de las 7» (`ev-v10-014705-718c5f4e`)
- **Regla o ejemplo:** la regla y un ejemplo de su replay entre sesiones.
- **«creo»:** no.
- **Compra y venta:** no lo distingue.
- **Propuesta: resuelve en parte.**
  - Pregunta 1: opción (a). Una liquidez tomada antes de las 7 sí la usa, siempre que la operación
    se dé desde las 7.
  - Segunda parte (la toma de las 6:45 y la de las 7:20): no elige entre (a) y (b). Contesta que la
    liquidez se va actualizando y se toma «la más reciente». Hoy el motor hace (b), PROVISIONAL
    (ADR-0066).

### 3.17 S-16 · Cuál de tus dos backtests de agosto vale (E-1)

- **Tramo:** 108:05 («pregunta ese 16») – 109:08 («pregunta S16 cerrada»).
- **Citas:**
  - 108:23–108:31 «el último bates e incluyó los break even como mencioné entonces sería el bates
    ideal porque / porque en el otro, en el otro, en el primer mes de agosto no lo incluía,»
    (`ev-v10-014823-64248489`)
  - 108:36–108:46 «a veces visualmente cuando uno ya se acostumbra a ver, … si sé que me va a dar
    break even, pues lo dejo correr y ya está, / o sea, sé que es un B, pongo B, pero claro, no lo
    tomo a la entrada»
  - 108:53 «pero sí, el último, como lo hemos grabado tal cual, lo hemos hecho en vivo, sería el
    último.» (`ev-v10-014853-76602fb4`)
  - 108:58–109:06 «igual este julio / pues también llega a tomar los / los break even y demás /
    porque está grabado / en video también»
- **Regla o ejemplo:** decisión sobre el material.
- **«creo»:** no.
- **Compra y venta:** no aplica.
- **Propuesta: resuelve.** Opción (b): vale el del vídeo, el grabado en vivo, porque incluye los
  break even.
  - **Contradice la premisa de la hoja.** `PREGUNTAS.md` decía que el del vídeo «se saltó
    operaciones de break even» y que el completo era el original. El trader dice lo contrario: el
    primero de agosto no incluía los break even, porque los apuntaba sin tomarlos a la entrada.
  - Dice lo mismo de un backtest de julio grabado en vídeo, que no está en el corpus.

### 3.18 S-17 · Si solo el 0 de la caja cuenta frente al nivel tomado (A-50)

- **Tramo:** 109:10 («pregunta S17») – 110:19.
- **Citas:**
  - 109:32–109:49 no entiende «a caballo» («No sé qué es caballo», «No he escuchado eso nunca»).
  - 110:03–110:19 «si la caja queda a nivel de la liquidez que se tomó, ¿descartas la entrada? /
    Eso creo que entonces a lo mejor tiene que ver con el igual, … / y no me da igual la respuesta
    es la ve no me da igual» (`ev-v10-015003-dd8ab1bf`, confianza baja)
- **Regla o ejemplo:** ninguna de las dos: respuesta corta a una pregunta reformulada.
- **«creo»:** sí («Eso creo que … a lo mejor»).
- **Compra y venta:** no lo distingue.
- **Propuesta: resuelve en parte.** Opción (b), no la descarta, pero sobre la pregunta reformulada
  por el consultor: «a nivel» en vez de «a caballo». Lo relaciona con «el igual» y dice «creo». Que
  no filtra queda como confirmación débil de v9 0:51:08.

### 3.19 S-18 · Los intentos: ¿por marca o por toma? (A-25)

- **Tramo:** 110:26 («pregunta 18», dicho sin la S) – 114:36 («S18 cerrada»).
- **Citas:**
  - 111:52–112:02 «ya la tercera como hemos dicho pues paramos y esperamos el desarrollo / rollo de
    otra zona de liquidez o la toma de otra zona de liquidez para nuevamente pues reiniciar / los
    tres intentos» (`ev-v10-015152-6dad6eb3`)
  - 112:02–112:25 «yo me iría por una / cuarta … hasta un cuarto pues podría ser válido hasta un
    cuarto»; 112:27–112:43 «pero claro / lo ha definido con 3 / bueno, hay que dejarlo así con 3 …
    pérdida 1, pérdida 2 / pérdida 3, detenemos / esperamos la siguiente toma de liquidez y
    nuevamente / operamos allí» (`ev-v10-015227-b360ebf1`)
- **Subpregunta (A-25), la marca del alto viejo:** 113:15–113:40 «luego actualizamos a este / que
  sería el más reciente este ya queda descartado … siempre lo que se va desarrollando va a ser / el
  más reciente»; 114:21–114:30 «Y si el alto se va descartando / O sea, el más reciente es lo que
  importa / … Y si la marca del alto viejo la sigues usando / Paso al nuevo»
  (`ev-v10-015421-44b43053`)
- **Regla o ejemplo:** la regla y un ejemplo supuesto.
- **«creo»:** no. Sí la duda propia del cuarto intento.
- **Compra y venta:** sí: el ejemplo de 113:49 es bajista y el de 113:07, de altos.
- **Propuesta: resuelve.** Opción (a): la toma de otra liquidez reinicia los tres intentos. La marca
  del alto viejo se descarta y pasa al nuevo. **Para el consultor:** el trader dice que él «se iría
  por una cuarta», pero lo deja en 3.

### 3.20 S-20 · Cuántos escenarios puede haber en una sesión como máximo (A-52)

- **Tramo:** 114:37 («Pasamos a S20») – 116:45 («preguntas de 20 cerrada»). Cuarentena 115:09–115:20,
  115:58–116:02 y 116:04–116:07; tramo de precaución 116:07–116:19.
- **Citas:**
  - 114:49–115:02 «Sí, o sea, en una sesión como digo / Mientras se cumplen / Los criterios para
    detener / O sea, de pérdida en general / Que sería una pérdida de 4,5 / O sea, 9 rachas / De
    pérdida, pues normal» (`ev-v10-015449-8a41513d`)
  - 116:20–116:27 «tratamos de / de tomarlo todo / o sea / todo lo que hay en una sesión /
    obviamente cumpliendo / pues los criterios / de entrada y salida»
  - 116:40–116:45 «pues tomamos / todas las entradas ganadoras o perdidas que se puedan dar en una
    sesión» (`ev-v10-015640-d35c5552`)
- **Regla o ejemplo:** la regla. El ejemplo de su libro (el máximo de un día) es el tramo de
  precaución 116:07–116:19. **Por decisión del consultor (2026-10-04, punto 3) se trata como
  expuesto (posible exposición de junio), y la cifra no se usa en nada**: ni en un parámetro, ni en
  una estimación de mensajes a FTMO, ni en esta resolución. La propuesta de abajo sale solo de las
  citas de 114:49 y 116:20–116:45.
- **«creo»:** no.
- **Compra y venta:** no aplica.
- **Propuesta: resuelve.** Opción (a): sin máximo de escenarios. Busca entrada cada vez que se dan
  los criterios, hasta que salta el tope de pérdida (4,5 % o 9 pérdidas). Las «dos entradas por
  día» de v4 se descartan.

### 3.21 S-21 · La orden puesta cuando el precio toma otra liquidez (A-53)

- **Tramo:** 116:55 («pasamos a ese 21») – 121:23 («Pregunta S21 cerrada»).
- **Citas:**
  - 117:16–117:26 «sigue vivo hasta que se desarrolle / otro posible punto de breaker / claro, como
    digo, nuestro punto de breaker / siempre va a ir en actualización / entonces no vamos a dejar /
    en un punto de breaker antiguo» (`ev-v10-015716-5ea2575f`)
  - 118:31 «La A es verdadera, o sea, si tengo que elegir alguna opción, la dejo y la muevo cuando
    aparezca el nuevo punto de liquidez, … ya la acabé, la dejo y la muevo cuando aparezca el nuevo
    punto de liquidez nueva, vale, eso no tiene que ver con el punto de breaker, sino cuando, a
    veces cuando se llegan a topar» (`ev-v10-015831-fb95edf0`, confianza baja)
  - 121:14–121:20 «Mientras no aparece el punto nuevo / Se presiona la orden vieja / ¿La operación
    vale? / Sí, vale / Mientras no aparece un punto nuevo» (`ev-v10-020114-55bdf502`)
- **Regla o ejemplo:** la regla y ejemplos de su replay.
- **«creo»:** no.
- **Compra y venta:** no lo distingue.
- **Propuesta: resuelve en parte.** Lo que describe es la (b): deja la orden y la mueve cuando
  aparece el punto de la liquidez nueva, y mientras tanto, si se llena la vieja, la operación vale.
  Es lo que hace hoy el motor (`se_mueve`, ADR-0066). Pero en la misma frase dice «La A es
  verdadera»; el consultor decide si basta.

### 3.22 S-23 · El nivel que, roto con mecha, anula la entrada (A-32)

- **Tramo:** 121:25 («Pregunta S23») – 123:43 («S23 cerrada»).
- **Citas:**
  - 121:42–121:56 «Cuando, o sea, un nivel en M15, o sea, de liquidez en M15, si es roto con mecha,
    se anula la entrada, o sea, no hay entrada. / Pero en M1, si tratamos de seguir el flujo en M1,
    es válido con mecha y cuerpo.» (`ev-v10-020142-30fd2569`)
  - 122:38–122:43 «tiene que ser con cuerpo la toma de liquidez en M15. / Ahora, si nosotros
    buscamos el flujo en M1, no importa si es con mecha o no.»
  - 123:08–123:25 «eso tiene que ver con el contexto en el que estamos analizando. / si es en / M15
    / la mecha / si es una toma de liquidez con mecha / invalida, pero si es en M1 / se toma en
    cuenta» (`ev-v10-020308-75b88d40`)
- **Regla o ejemplo:** la regla.
- **«creo»:** no.
- **Compra y venta:** no lo distingue.
- **Propuesta: resuelve en parte.** Da la regla (en M15, una toma con mecha invalida; en M1, la
  mecha cuenta), que ya estaba en v9 0:42:17. **No identifica la línea de v4 0:53:10**, que es lo
  que preguntaba A-32. A-32 sigue sin respuesta a su pregunta concreta.

### 3.23 S-24 · Confirmar el break even tapado por el corte de audio de v9 (A-13)

- **Tramo:** 123:45 («pregunta S24») – 126:42. El final cae en la cuarentena 126:42–127:02.
- **Citas:**
  - 123:59–124:08 (lee) «Para el break-even / En cuanto el precio toca el nivel / Que rompe la zona
    de control / Mirando en M1 / Y sin esperar a que se cierre la vela / Pones el stop exactamente
    en la entrada / Después, o ya no la mueves»
  - 124:10–124:16 «Pues siempre pongo exactamente en la entrada / El stop, o sea / cuando llega a
    cumplirse los criterios / que hemos planteado» (`ev-v10-020410-e06f9581`)
  - 124:53–125:00 «cae ya apenas cierra por debajo estoy si lo hace con cuerpo mucho mejor entonces
    nosotros la entrada / ya la pondríamos en break even» (`ev-v10-020453-2d41dd25`)
  - 125:20–125:43 «el nivel que tiene que tocar es más o menos como que seguir el criterio para
    validar un posible punto breaker, ¿vale? … esperaríamos a que se cierre por debajo, o sea, en
    este caso, de un lower low, un bajo más bajo. / Ahora, en un caso alcista, esperaríamos a que
    cierre por encima de un higher high.» (`ev-v10-020520-7bdf02b3`)
  - 126:35 «para precisar o si después de ponerlo en la entrada lo vuelves a» → cuarentena.
- **Regla o ejemplo:** la regla («siempre pongo exactamente en la entrada»), y el disparador
  explicado con un ejemplo y un dibujo.
- **«creo»:** no.
- **Compra y venta:** sí.
- **Propuesta: resuelve en parte, con contradicción.**
  - Confirma el stop exactamente en la entrada.
  - **No confirma «sin esperar a que se cierre la vela»**: en su ejemplo espera a que la vela
    cierre más allá del nivel («apenas cierra por debajo», mejor con cuerpo). Contradice el «apenas
    toca» de v6 0:57:01 y v9 0:55:43.
  - Si después mueve el stop: sin respuesta legible.
  - El bot hoy lo pone al tick (ADR-0065).

### 3.24 S-19 · Las 7 capturas que venían con el backtest de marzo

- **Tramo:** 126:42 (en cuarentena) – 127:29 («se ha acabado el Q&A»). Cuarentena 126:42–127:02 y
  127:04–127:11.
- **Citas:**
  - 127:02 «queremos saber que son antes de decidir que hacer con ellas» (lectura)
  - 127:15–127:26 «o sea, cuantas operativas se hizo al día / o sea, son los stats / o sea,
    estadísticas de / los trades y demás / Así como nos enviabas fotos de las estadísticas / Claro»
    (`ev-v10-020715-7852af76`)
- **Regla o ejemplo:** no aplica.
- **«creo»:** no.
- **Compra y venta:** no aplica.
- **Propuesta: resuelve.** Las 7 capturas son estadísticas de las operaciones («stats»,
  «cuántas operativas se hizo al día»): AGREGADOS de marzo. Según CLAUDE.md no se abren nunca. En lo
  legible no hay ninguna cifra; el arranque de la respuesta está en cuarentena.

## 4. Contradicciones y cosas que el consultor tiene que mirar

1. **El break even al cierre o al toque (S-24).** v6 0:57:01 y v9 0:55:43 dicen «apenas toca»; en
   v10 espera al cierre de la vela más allá del nivel. ADR-0065 lo pone al tick.
2. **La vela casi plana (S-14).** Opción (b) a las 103:17, y lo contrario a las 104:44.
3. **El backtest de agosto que vale (S-16).** Al revés de la premisa de `PREGUNTAS.md`.
4. **S-4 contra `caja_se_fija`** (decisión 5 del ADR de F35): el 1 se expande hasta llenar.
5. **S-21:** «La A es verdadera» y describe la (b).
6. **S-6:** «un pip» y, tras la cuenta, «un punto».
7. **S-9:** «es un error» el 9 % semanal, y después «No recuerdo muy bien eso».
8. **Las 9 pérdidas (S-8)** vienen de la cuenta de fondeo con un 0,5 %, y podría extenderlas con
   menos riesgo.
9. **Junio y la cuarentena mecánica** (§2.4).
10. **La guardia y el guion nuevo** (§1.2): la comparación real de la sesión 3 queda pendiente.
11. **S-7 se respondió en el reloj del trader** (añadido por el consultor el 2026-10-04, punto 4).
    - La rama que active A-42 fija en UTC las dos sesiones de invierno y comprueba que son las mismas
      horas UTC que 07–15 de verano.
    - Mide también dónde caen los cortes de H4 en el reloj del bróker entre el 25 de octubre y el 1
      de noviembre, cuando Europa ya ha cambiado la hora y EE. UU. todavía no.
    - Si la filtrada no deja claro el reloj, el consultor se lo pregunta al trader por mensaje antes
      del 25.

## 5. Tabla final

| Código | Ambigüedad | Tramo | Propuesta | Regla general | «creo» | Compra y venta |
|---|---|---|---|---|---|---|
| **S-7** | A-42 | 62:56–65:29 | **resuelve**: 6–10 y 10–2 desde el 25-10 | sí | no | n/a |
| S-1 | A-49 | 00:09–20:00 | en parte | sí | no (sí sobre ejemplos) | sí |
| S-2 | A-49 | 20:04–28:22 | en parte | sí | no | sí |
| S-3 | A-18 | 28:26–44:44 | **resuelve**: stop en el 0,8; objetivo 0→1 | sí | no | n/a |
| S-4 | A-49 | 46:41–51:42 | **resuelve**: el 1 se expande | sí | no | sí |
| S-5 | A-30, A-39 | 51:45–56:18 | **resuelve**: se quita a las 11 y a las 3 | sí | no | n/a |
| S-6 | ADR-0061 §2 | 56:21–61:52 | en parte: hacia fuera, un punto tras corregir | sí | no | sí |
| S-22 | A-36 | 61:54–62:54 | **resuelve**: en el 0 con mecha, sin spread | sí | no | no lo distingue |
| S-8 | A-51 | 65:32–68:18 | **resuelve**: el BE no corta; vuelve al día siguiente | sí | no | n/a |
| S-9 | A-44 | 68:18–70:44 | en parte | sí, con dudas | no | n/a |
| S-10 | A-21 | 70:47–81:49 | **resuelve**: (a) y retroceso sin tope | sí | no | sí |
| S-11 | A-35 | 81:49–85:40 | en parte | sí | no | sí |
| S-12 | G-2, A-33 | 85:40–89:21 | **resuelve**: fijo, 3 × (0→1) | sí | sobre lo de antes | n/a |
| S-13 | ADR-0060 §2 | 89:29–101:49 | **resuelve**: neutra = mantiene el sesgo | sí | no | solo alcista |
| S-14 | RN-007 | 101:49–105:50 | en parte, contradictoria | sí, dos versiones | no | n/a |
| S-15 | A-43 | 105:51–108:05 | en parte | sí | no | no lo distingue |
| S-16 | E-1 | 108:05–109:08 | **resuelve**: el del vídeo | n/a | no | n/a |
| S-17 | A-50 | 109:10–110:19 | en parte (pregunta reformulada) | no | **sí** | no lo distingue |
| S-18 | A-25 | 110:26–114:36 | **resuelve**: reinicia con 3; pasa al alto nuevo | sí | no | sí |
| S-20 | A-52 | 114:37–116:45 | **resuelve**: sin máximo | sí | no | n/a |
| S-21 | A-53 | 116:55–121:23 | en parte | sí | no | no lo distingue |
| S-23 | A-32 | 121:25–123:43 | en parte: regla sí, la línea de v4 no | sí | no | no lo distingue |
| S-24 | A-13 | 123:45–126:42 | en parte, contradice el «apenas toca» | sí | no | sí |
| S-19 | marzo | 126:42–127:29 | **resuelve**: son estadísticas | n/a | no | n/a |

Resuelve: 13. En parte: 11. No resuelve: ninguna, aunque A-32 en su pregunta concreta y la
subpregunta de S-24 quedan sin respuesta.

## 6. Lo que deja la rama

- `knowledge/corpus/fuentes.yaml` (v10), `manifest.yaml`, la transcripción
  `tr-v10-large-v3-int8-float16-85e8af79` y los fotogramas `fr-v10-69219820`.
- `knowledge/corpus/tramos_no_citables.yaml`: 21 tramos de v10 (4 sin audio, 12 de cuarentena, 3
  de precaución, 1 personal y 1 de un mes con días ocultos que la cuarentena no cubre).
- 64 ítems `knowledge/evidence/v10/ev-v10-*`.
- `src/botsito/corpus/cuarentena.py`: v10 en `SESIONES_EN_CUARENTENA`. Y sus tests:
  `test_inventario`, `test_cuarentena` (el ejemplo de sesión sin listar pasa de v10 a v11) y
  `test_guardia_claude`.
- `scripts/transcribir_sesion.py`, la hoja por sesión, y `tests/unit/test_transcribir_sesion.py`.
- `docs/sesion-4/HOJA-USADA.md`, la tabla código → título → número de `PREGUNTAS.md` →
  ambigüedad.
- `docs/validation/HOLDOUT-EXPOSICIONES.md`: la fila del 2026-10-04.

**Pendientes que deja la rama** (revisión del consultor del 2026-10-04, punto 6). No se hacen
aquí; se apuntan:

- **(a) Una rama de cuarentena.**
  - El filtro oculta todo mes con días en `casos_ocultos`, nombrando la condición y no una lista.
  - Incluye la copia de la guardia, un test roto a propósito con junio, volver a filtrar v7–v10 y
    cruzar la evidencia y los informes commiteados con el filtro nuevo.
  - **Va antes de activar la sesión 4.**
- **(b) Con el guion nuevo ya en `main`:** `--solo-filtrar --sesion 03` sobre v9 (sha esperado
  `f7529459…`) y `--sesion 04` sobre v10.

## Revisión del consultor (2026-10-04)

Decisiones del consultor del 2026-10-04 sobre esta rama, copiadas tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Revisión del consultor de trabajo/sesion-04 (2026-10-04). Copia estas decisiones al final del informe SESION-04-EXTRACCION.md, en una sección «Revisión del consultor (2026-10-04)», con su fecha.
>
> 1. Commit y push. Aleks ha salido del modo automático: vuelve a pedir el commit y el push y él los aprueba a la vista. No añadas reglas de permiso ni toques /permissions. Primero haz los puntos 2 a 5, vuelve a sellar make check y rehaz msg3.txt para que describa el árbol final.
>
> 2. Junio, en esta rama, sin tocar cuarentena.py ni la guardia. Mide la propiedad con su definición exacta: qué segmentos de la filtrada de v10, fuera de los tramos ya ocultos, nombran un mes que tenga días en casos_ocultos y no esté en MESES_FILTRADOS. Lista solo los tiempos, sin texto. Cada uno va a tramos_no_citables.yaml con el motivo «precaución: mes con días ocultos que la cuarentena mecánica no cubre». Después:
>    - quita del informe toda cita de esos segmentos, incluida la de 115:29, y descríbelos sin texto;
>    - comprueba si algún ítem ev-v10-* cae en ellos. Si cae alguno, se retira por el procedimiento de evidencia del repo (la evidencia no se edita). Si no hay procedimiento, para y avísame;
>    - vuelve a pasar el check de evidencia contra los tramos nuevos.
>
> 3. El agregado de 116:07 (máximo de 7 operaciones en un día). El consultor no lee la cuarentena: la cruda solo la lee Aleks. Corrige hoy la fila del 2026-10-04 de HOLDOUT-EXPOSICIONES.md: «posible exposición de junio, un agregado de periodo no identificado; se trata como expuesto». Esa cifra no se usa en nada: ni en un parámetro, ni en una estimación de mensajes a FTMO, ni en la resolución de S-20. Escríbelo así en el §2.3 y el §3.20.
>
> 4. Fotograma de S-7: no se abre. Añade al §4 un punto 11: «S-7 se respondió en el reloj del trader. La rama que active A-42 fija en UTC las dos sesiones de invierno y comprueba que son las mismas horas UTC que 07–15 de verano. Mide también dónde caen los cortes de H4 en el reloj del bróker entre el 25 de octubre y el 1 de noviembre, cuando Europa ya ha cambiado la hora y EE. UU. todavía no. Si la filtrada no deja claro el reloj, el consultor se lo pregunta al trader por mensaje antes del 25».
>
> 5. Tests. Da passed/skipped/deselected del make check sellado de la rama y del último de main, sacados de su salida. El último cierre que consta en HISTORIA da 1901 passed y 8 skipped, y tu informe dice «los tests en 1251». Si son la misma cifra y han bajado, encuentra el porqué antes del commit y escríbelo en el informe.
>
> 6. Pendientes que deja la rama (§6): no se hacen aquí, se apuntan.
>    (a) Una rama de cuarentena: el filtro oculta todo mes con días en casos_ocultos, nombrando la condición y no una lista. Incluye la copia de la guardia, un test roto a propósito con junio, volver a filtrar v7–v10 y cruzar la evidencia y los informes commiteados con el filtro nuevo. Va antes de activar la sesión 4.
>    (b) Con el guion nuevo ya en main: --solo-filtrar --sesion 03 sobre v9 (sha esperado f7529459…) y --sesion 04 sobre v10.
>
> 7. Después: push a fix/sesion-04 (git push origin trabajo/sesion-04:refs/heads/fix/sesion-04) y CI de Linux, en la que el único fallo aceptado es el de state check. Dame el número de run. Luego lanza el revisor con el informe YA TERMINADO y pega su informe al final. Pídele expresamente que busque copias de material oculto fuera de su sitio (informes, evidencia, HOLDOUT-EXPOSICIONES) y meses con días ocultos que el filtro no cubra.
>
> Rama lista para revisión, NO cerrada.

**Qué se hizo con cada punto:**
1. Sin reglas de permiso. Commit y push se piden de nuevo para que Aleks los apruebe a la vista,
   después de los puntos 2 a 5, con `make check` sellado otra vez y `msg3.txt` rehecho.
2. §2.4. Un segmento (1:55:29), ya no citable, sin texto. Ningún ítem cae en él y el check de
   evidencia está en verde.
3. §2.3, §3.20 y la fila del 2026-10-04 de `HOLDOUT-EXPOSICIONES.md`.
4. §2.5 y §4, punto 11.
5. §1.3: no han bajado. 1251 cuenta funciones; 1901 + 8 cuenta casos. La rama recoge 1919 casos y
   `main`, 1910.
6. §6, pendientes (a) y (b).
7. La CI y el revisor, abajo.

## Estado

EXTRACCIÓN HECHA, rama **lista para revisión, NO cerrada**. Nada se resuelve sin el consultor. La CI
y el informe del revisor van abajo.
