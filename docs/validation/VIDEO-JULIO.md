# FUNCTIONALITY VALIDATION REPORT

**Funcionalidad:** T · el vídeo de julio (v11-v14): transcripción, fotogramas, cobertura por día y comparación con el libro (R2.4)
**Rama:** trabajo/video-julio
**Objetivo:** oír al trader sobre julio: transcribir v11 a v14, comprobar qué días cubre cada vídeo, comparar el vídeo con los casos del libro de julio (días 1 a 17) y preparar la clasificación de las 81 filas «sin clase hasta T» y el inventario de los días 20 a 31 (encargo en `docs/encargos/trabajo-video-julio.md`).

## Base (comprobada con git al abrir, 2026-11-08)

- `git rev-parse main origin/main`: `5a54b468a4de3a0f36124cdac0da481d4abf2ed4` las dos veces.
- Último `- Tag:` de HISTORIA: `stable/F38t-recorrida-construccion-2`; `git rev-parse "stable/F38t-recorrida-construccion-2^{commit}"` = `git rev-parse main^1` = `86f306a0dc577eb78de673b45f923d5ef89a434b`; en origin (`git ls-remote --tags`: `4e20ad1…` refs/tags/stable/F38t-recorrida-construccion-2).
- CI de main sobre `5a54b468a4de3a0f36124cdac0da481d4abf2ed4` (check-runs): `Python completed success`, run 42550658681.
- `git branch --list`: solo `main`; `git ls-remote --heads origin`: solo `refs/heads/main`.

## 0. Fase 0 (2026-11-08)

Leída sin escribir en el repo salvo la apertura. El encargo dice «si todo cuadra, NO pares»: se
pararon cuatro preguntas (abajo, «Lo que necesito que decidas»), contestadas el mismo día; la
respuesta va copiada tal cual en su sección y aplicada en §0.9.

### 0.1 La base y lo de julio

- La base, arriba («Base»): las cuatro comprobaciones de `abrir-rama`, en verde.
- Los cuatro `.mkv` (`sha256sum` y `stat -c %s` en `corpus/Estrategia del trader/Material adicional de su operativa/Backtest Julio 2026/`, sin abrir nada): coinciden con ENTRADA-JULIO.md §0.d.

| Vídeo | Fichero | Bytes | sha256 |
|---|---|---|---|
| v11 | `2026-10-02 20-18-00.mkv` | 419918585 | `5732fe44…ba299f` |
| v12 | `2026-10-02 20-53-08.mkv` | 739623714 | `a045ec0b…43f01a3` |
| v13 | `2026-10-04 09-45-43.mkv` | 815725885 | `8dc7efa1…62b0c1ff` |
| v14 | `2026-10-04 12-40-14.mkv` | 1194821502 | `e13e4e4d…203961d6` |

- Julio ENTERO, del 1 al 31, por recuento y sin imprimir ids (guion de la carpeta de trabajo,
  `recuento_julio.py`, copiado en `anexos/VIDEO-JULIO/`):
  ```
  casos_reservados: 34 en total; de 2026-07: 0
  casos_ocultos: 34 en total; de 2026-07: 0
  dias de julio 1-31 sin ninguno:  31
  meses_libres: [1, 4, 7, 8, 10, 11]; 7 dentro: True
  ```
  Los meses no libres son 2, 3, 5, 6, 9 y 12, como dice el encargo.

### 0.2 Qué da cada herramienta y cada salida (medido)

- **`corpus transcribe --video <v>`** (`cli.py:266-325`): imprime un `fragmento N: M segmentos` por
  fragmento y, al final, `OK: <transcripcion_id> (<n> segmentos)`, la ruta de la cruda y la del
  manifiesto (INMUTABLE). Por defecto: faster-whisper `large-v3`, `cuda`, `int8_float16`, con el
  glosario como prompt inicial. **No aplica cuarentena al escribir**: la cruda es entera; el filtro
  se aplica al leer. Medido sobre v11 en §1.
- **`corpus transcript show --video <v> --t0 --t1 [--margen-s] [--capa]`** (`cli.py:414-457`):
  una cabecera `# <id> · capa · t0-t1`, el texto legible con marcas `[h:mm:ss.mmm]` de la capa
  corregida (por defecto), FILTRADO, y al final el resumen de ocultos de la ventana pedida
  (`cuarentena.resumen`): cuántos y con los motivos **a, b o c** (`cuarentena.py:87-96`). La
  cuarentena por condición sale siempre como «c»: el submotivo (mes, fecha, día de la semana,
  «backtest», vecino) no lo da (respuesta del consultor, punto 4).
- **`corpus frames extract --video <v>`** (`cli.py:466-505`): cobertura completa a 1 fps sin
  pérdida más los obligatorios (v11-v14 no tienen ninguno en `fotogramas_obligatorios.yaml`);
  imprime `OK: <fotogramas_id> (<n> fotogramas, <k> extra)`, el índice y el manifiesto. Extraer
  no es abrir (ADR-0038 regula abrir).
- **`corpus frames show --video <v> --t h:mm:ss [--n N]`** (`cli.py:537-567`): por fotograma, una
  línea `fr-<id>/<t_ms>` TAB `pts` TAB `origen` TAB ruta del PNG; y el segmento FILTRADO de la
  transcripción que cubre el instante (o el aviso de oculto).
- **Los casos de julio** (`knowledge/cases/dev/caso-eurusd-2026-07-*.yaml`, 13): `dia`, `fuente`
  (fichero, sha256 del libro, tipo), `id` y `operaciones`, cada una con `direccion`, `entrada`,
  `stop`, `instante_utc` (el llenado) y `sesion` (`07-11` u `11-15`, rótulo en hora de Madrid:
  `2026-07-02T09:34:25+00:00` va en `11-15`). Sin objetivo, sin resultado.
- **`para-clasificar.txt`** (`anexos/RECORRIDA-CONSTRUCCION-2/`): dos tablas. «Operaciones del
  trader» (`:19`): día, sesión, lado, instante UTC, entrada, escalón y orden de la corrida 1
  (id, estado, «llenada a N min del trader»), patrón, **primer hecho que falta** con los
  **frenos** pegados («frenos producidos: …»), escalón y patrón de la corrida 2, vídeo, hora
  perdida. «Órdenes del bot sin operación del trader» (`:220`): día, sesión, dirección, orden,
  resultado, R neto, desenlace, stop movido, patrón; **sin primer hecho ni frenos**. Verificado lo
  del auditor del consultor: **no trae la regla que explica una orden del bot**; y tampoco el bot
  más cercano, Δentrada ni Δinstante (`grep -c "mas cercano\|Δ"` da 0).
- **`patrones-cuenta-por-mes.txt`**: la tabla de patrones por mes y, por fila (`-- filas`), el
  patrón con su subtipo, quién (trader o bot), día, sesión, lado, instante UTC, entrada y: para
  una fila del trader, el **bot más cercano** en la sesión (lado, instante, entrada), **Δentrada**,
  **Δinstante**, el primer hecho que faltó y los frenos; para una del bot, el trader más cercano
  con sus Δ, o «ninguna operación del trader en la sesión/día».
- **`visor-sesiones.txt`**: solo nueve sesiones (cinco de julio: 07-02, 07-06, 07-07, 07-14 y
  07-15), en horas de pared de Madrid: el sesgo anotado por el motor y el color de la H4 que
  decide, la primera liquidez tomada, las acciones bloqueadas, zonas y órdenes (zona de la que
  nace, ¿primera desde la toma?) y, por operación del trader, si había zona del bot de su lado.

Por eso F4 sale de DOS ficheros (respuesta del consultor, punto 3): el bot más cercano y los Δ, de
`patrones-cuenta-por-mes.txt`; la orden, el primer hecho y los frenos, de `para-clasificar.txt`; las
39 filas P5 y P6 (órdenes del bot) van sin primer hecho ni frenos.

### 0.3 Qué cambia al registrar cuatro transcripciones y cuatro extracciones

- Ningún test enumera los manifiestos REALES de transcripciones o fotogramas por número: los que
  los nombran usan ids sintéticos (`tr-v1-falso-…`, `fr-v1-…`) o una lista fija de otras
  transcripciones (`test_a18_buscar.py:49`, `ALCANCE` de 5; `test_filtradas_con_tramos.py:338`,
  los sha de v7-v10). Los que listan VÍDEOS (`test_inventario.py`, v1 a v17; `test_guardia_claude.py:152`,
  las sesiones en cuarentena) no cambian: v11-v14 ya están en `fuentes.yaml` desde
  `trabajo/entrada-julio` y no son sesiones.
- `test_guardia_claude.py::test_la_lista_de_la_guardia_es_la_que_se_calcula`: la lista de ficheros
  con texto oculto se recalcula desde los `docs/` que copian pasajes con formato de salida de
  medición; el informe cita solo texto filtrado, así que no debería entrar ninguno. Se comprueba
  en cada `make check`.
- `knowledge validate` comprueba el historial de los manifiestos (inmutables, `Fuente:` donde
  toque) y `corpus transcript check` / `frames check` su coherencia con el disco.
- **`corpus inventory` al cambiar una naturaleza**: `manifest.yaml` no guarda `naturaleza`
  (`manifest.yaml:2391-2434`, campos de fichero, sha, duración y audio); se ejecuta en F5 tras el
  cambio y se dice su diff.

### 0.4 Quién lee `material_sin_video` y qué rompe cada salida de F5

- `cargar_criterio` → `_material_sin_video` (`criterio_fidelidad.py:354-388`): el bloque existe;
  meses, provisionales y meses de los días son de construcción; todo día con vídeo cae en `meses`;
  ningún mes a la vez en `meses` y en provisionales. `sin_video(dia)` (`:348-351`) solo mira
  `meses` y `dias_con_video`.
- La línea de la salida (`cableado.py:1403-1408`): «libros sin video: …, salvo …; cuentan como
  CON video, provisionales hasta que T lo compruebe: … (fuente: …)».
- **Salida 1** (2026-07 sale de provisionales): carga (la lista vacía vale); `test_metodo_adr0092.py:445`
  **sigue pasando** (julio no está en `meses`); **rompen los tres goldens**
  `tests/golden/metodo_adr0092/main-{hueco,stop,viva}.txt:18`, que copian esa línea con el valor y
  la `fuente` viejos y que `test_cuenta_por_mes.py:277-284` compara byte a byte con el criterio
  REAL.
- **Salida 2** (2026-07 a `meses` y sus días a `dias_con_video`): carga; `:445` pasa solo si
  07-08 está entre los días; rompen los tres goldens y, además,
  `test_criterio_campos_adr0092.py:104` (`("dias_con_video", '["2026-07-01"]')` espera el error
  «fuera de meses», que deja de saltar).
- `test_criterio_campos_adr0092.py:94-112` (bloque ausente o mal formado) no depende del valor real.

### 0.5 Herencias

Búsqueda de «video-julio», «rama del vídeo», «rama que transcriba», «lo comprueba la rama» y
«hasta T» en `PROJECT_STATE.md`, el final de HISTORIA, `docs/validation/`, `docs/adr/`,
`fuentes.yaml` y `knowledge/cases/*.yaml`. Lo que se deja a esta rama, y dónde entra:

| Herencia | Dónde | Entra en |
|---|---|---|
| Transcribir v11-v14, cobertura por día, vídeo frente al xlsx, horas del replay frente al libro | ENTRADA-JULIO.md §5 (:629-636) y §8 | F1, F2, F3 |
| «con el guion de main y su cuarentena», un error | ENTRADA-JULIO.md:629-630 | recuadro de corrección (§8 de este informe) |
| El libro en Europe/Madrid, «dato para la rama del vídeo» | ENTRADA-JULIO.md:508-509 | F3 |
| Qué se hace con los días 20 a 31, después de transcribir | ADR-0078 §3 (:30-32) | F6, para que el consultor decida U |
| «lo comprueba la rama que los transcriba» (comentario y cuatro naturalezas) | fuentes.yaml:116-118, 124-155 | F5 |
| Julio provisional «hasta que T lo compruebe» | ADR-0092 §11 (:259-260); criterio_fidelidad.yaml:59-64 | F5 |
| 81 filas «sin clase hasta T» | RECORRIDA-CONSTRUCCION-2.md §8 (:1320-1330, :1360-1361) | F4 |
| La pendiente con dueño de 07-02 y 07-14 (y 04-13) | RECORRIDA-CONSTRUCCION-2.md:1355-1358 | solo la voz del trader en F4; el motor, la rama de trazas (R4.4) |
| S-25: el Excel y los tres primeros vídeos, «todo está grabado» | SESION-05-EXTRACCION.md:1052-1057, :1228 | F2 y F3 |
| «hasta que T lo compruebe» en `src/` | cableado.py:1408; criterio_fidelidad.py:341 | NO entra: `src/` está protegido; propuesta para la orden de cierre / deuda |
| Punteros a «qué libro viene de vídeo» en ACTIVAR-SESION-05.md §0.b.7 | PROJECT_STATE.md:36 (G) y :122; ACTIVAR-SESION-05.md:76, 296, 311, 1083; METODO-FIDELIDAD-RENTABILIDAD.md:216; BARRIDO-SESION-6.md:120 | propuesta para la orden de cierre (G apunta a este informe); los informes cerrados no se tocan |

### 0.6 Tiempo esperado y memoria

- Duraciones (`manifest.yaml`): v11 1260,9 s, v12 2220,8 s, v13 2449,3 s, v14 3587,5 s; 9518,5 s
  en total (2 h 38 min). Con los factores de las sesiones (0,20 de v17 y 0,32 de v16, medidos con
  el ASR del guion de sesión, el mismo modelo), **de 32 a 51 min** de transcripción para los cuatro
  (v14 sola, de 12 a 19 min); la GPU es una GTX 1650 de 4 GB. Los tiempos reales, en §1.
- PICO DE MEMORIA del último `make check` (el de la apertura, en esta rama): **307 MiB** en `test`.

### 0.7 El encargo frente al repo (auditor-encargo)

48 afirmaciones: 33 correctas, 13 con matiz, 2 incorrectas; 7 cosas que el repo pide y el encargo
no dice. Lo que cambia el trabajo:

- **INCORRECTA (#38):** F4 pide a `para-clasificar.txt` el bot más cercano, Δentrada y Δinstante;
  están en `patrones-cuenta-por-mes.txt`. Pregunta 3; resuelta.
- **INCORRECTA en lo que nombra (#45):** el test que fija el valor viejo no es
  `test_metodo_adr0092.py:445`, son los tres goldens; con la salida 2, además
  `test_criterio_campos_adr0092.py:104`. Pregunta 2; resuelta.
- **MATIZ (#15, y lo que pide el repo #4):** la decisión 1 de la PARADA de v16 («el número no se
  escribe en ningún sitio») chocaba con F2 y F6 «por día». Pregunta 1; resuelta.
- **MATIZ (#21):** los ocultos solo salen por motivo a/b/c. Pregunta 4; resuelta.
- **MATIZ (#20):** «NO tapa un día de julio dicho con palabras» es cierto del mes, pero un día de
  la semana con número («lunes 20») o una fecha numérica («20/7») caen por condición, con sus dos
  vecinos. Si eso tapa los días 20 a 31 en v14, PARADA (encargo).
- **MATIZ (#30):** S-25: «todo está grabado» es literal; que el Excel exporte los tres primeros
  vídeos lo dijo de palabra a Aleks (ENTRADA-JULIO §0.d) y en la sesión 5 solo «está en orden»
  (SESION-05-EXTRACCION.md:1054-1057).
- **MATIZ (#33):** el 3 de las tolerancias se justificó por leer «en otra serie (A-16)»
  (criterio_fidelidad.yaml:18-19); aquí se reutiliza por decisión del encargo.
- **MATIZ (#42):** de las tres horas de ticks perdidas, solo 07-10 05h y 07-16 11h tocan filas del
  trader; la de 07-14 12h no toca ninguna. Se verifica en F4.
- **MATIZ (#8):** el comentario de `fuentes.yaml` empieza en :112; las frases son las de :116-118.
- **MATIZ (#2):** RUMBO-2026-11.md no nombra T; el orden «(1) T» está en F (PROJECT_STATE.md:28).
- Lo que pide el repo #7: ENTRADA-JULIO §5 dice también «extraer fotogramas SOLO por instantes
  localizados»; `frames extract` extrae la cobertura completa y ADR-0038 regula abrir. El
  recuadro lo precisa.

### 0.8 Lo que no pude medir

- El sha de los ficheros de `data/transcripciones/v11..v14`: no existen hasta F1.

### Lo que necesito que decidas (fase 0)

0. La decisión 1 de la PARADA de v16 frente a F2/F6 «por día». (a) levantada para lo medido en v14
   como fuente propia; (b) el último día se enmascara. Recomendé (a), con PARADA parcial.
1. F5: los tres goldens fijan el valor viejo; se ponen al día en el commit de F5. Con la salida 2,
   `test_criterio_campos_adr0092.py:104` rompe: PARADA.
2. F4 de dos ficheros; las 39 filas P5/P6 sin primer hecho ni frenos.
3. Los ocultos, solo por motivo a/b/c.

## Respuesta del consultor a la fase 0 (2026-11-08)

Copiada tal cual:

> Respuesta del consultor a las cuatro preguntas de la fase 0 de trabajo/video-julio (2026-11-08). Cópiala tal cual en el informe, en su sección, y aplícala. No pares la rama: sigue con todo.
>
> 1. La decisión 1 de la PARADA de v16: opción (a), con este alcance.
>    - Sigue en pie para su objeto. El tramo v16 0:30:41-0:31:37 sigue siendo no citable. Su número no se escribe en ningún sitio como dato de v16, ni se compara con lo que dé v14 (y la decisión 5 tampoco cambia).
>    - No alcanza a v14. La decisión 1 se tomó bajo la cautela de «julio del 18 en adelante», que este encargo levanta para v11-v14 por ADR-0078 §3 y porque julio no tiene días en ninguna partición. Lo que v14 enseñe, días incluidos, se mide en v14 como fuente propia y se escribe en el informe (F2 y F6).
>    - La fila de HOLDOUT-EXPOSICIONES sigue diciendo solo «20 a 31», como manda el encargo.
>    - No hace falta la PARADA parcial: sigue con F1 a F7.
>
> 2. F5: de acuerdo con los goldens, y la segunda vía tampoco para.
>    - Los tres tests/golden/metodo_adr0092/main-*.txt fijan en su línea 18 el valor viejo («provisionales hasta que T lo compruebe: 2026-07»). Se regeneran en el commit de F5 por el procedimiento documentado (test_cuenta_por_mes.py:10, test_el_volcado_de_los_escenarios con -s), nunca a mano. El diff tiene que ser solo esa línea; si cambia cualquier otra, PARADA. Amplía el contrato a esos tres ficheros.
>    - Si F5 sale por la segunda vía, test_criterio_campos_adr0092.py:104 no fija el valor viejo: comprueba la regla «un día con vídeo cuyo mes no está en meses» y usa julio de ejemplo. Con julio en meses ya no queda ningún mes de construcción fuera de meses, así que se rehace ese caso para que siga probando la MISMA regla: la copia del criterio lleva meses sin un mes de construcción y dias_con_video con un día de ese mes. Antes de commitear, demuestra que el caso rehecho falla si se quita esa comprobación de cargar_criterio (en un clon desechable con git worktree add, como manda CLAUDE.md) y pega la salida en el informe. Amplía el contrato a ese test. PARADA solo si rompe cualquier otra cosa.
>
> 3. F4 de dos ficheros: de acuerdo. Las 39 filas P5 y P6 van sin primer hecho ni frenos, y el informe lo dice.
>
> 4. Los ocultos, por motivo a, b o c: de acuerdo. Nada sin filtrar.

### 0.9 Cómo se aplica, punto por punto

1. F2 y F6 escriben los días que enseñe v14, medidos en v14. El número de v16 no se escribe ni se
   compara. La fila de exposiciones dice solo «20 a 31». Sin PARADA parcial.
2. Contrato ampliado a los tres goldens y a `test_criterio_campos_adr0092.py` (commit de la fase 0).
   Los goldens, en F5, por `test_el_volcado_de_los_escenarios -s` y `partir_volcado.py`, con diff de
   una sola línea; la salida 2, con el caso rehecho y su prueba de rotura en un worktree.
3. F4 de dos ficheros (§0.2).
4. Ocultos por a/b/c (§1).

## 1. F1 · Transcripción y fotogramas (2026-11-08)

Uno a uno, en segundo plano (Claude Code arrancado con `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1`,
comprobado con `env`), sin ningún `make check` a la vez; GPU GTX 1650 de 4 GB.

| Vídeo | Transcripción | Segmentos | Ocultos por la CLI (a/b/c) | Audio no silencioso (`ms_con_habla`) | Huecos sin texto > 30 s | Palabras (CLI filtrada) | Fotogramas |
|---|---|---|---|---|---|---|---|
| v11 | `tr-v11-large-v3-int8-float16-d5da10be` | 120 | 0 | 1158 s de 1261 s | 0 | 1525 | `fr-v11-b83d5164`, 1261 |
| v12 | `tr-v12-large-v3-int8-float16-cb502503` | 111 | 0 | 1712 s de 2221 s | 4 | 1138 | `fr-v12-3eeb8cf9`, 2221 |
| v13 | `tr-v13-large-v3-int8-float16-1aeb45d5` | 31 | 0 | 1696 s de 2449 s | 4 | 645 | `fr-v13-8c1e06fb`, 2450 |
| v14 | `tr-v14-large-v3-int8-float16-2253ec10` | 29 | 0 | 1365 s de 3588 s | 5 (2195 s) | 565 | `fr-v14-5688e08b`, 3588 |

- **Ocultos: ninguno en los cuatro vídeos.** `transcript show` sobre cada vídeo entero no imprime
  ningún aviso de ocultos (motivos a, b ni c). Ni una fecha numérica, ni un mes no libre, ni un día
  de la semana con número: los días se dicen como «el 10 de julio», «el día 17», «el día 20», que
  la cuarentena por condición no tapa (mes libre). **Nada tapa los días 20 a 31 en v14.**
- `uv run botsito corpus transcript check`: `OK: 22 transcripciones coherentes con el disco y el
  glosario`. `uv run botsito corpus frames check`: `OK: 17 extracciones coherentes con el disco;
  3 obligatorios presentes`.
- **Tiempo** (de la creación de la carpeta del vídeo en `data/transcripciones/` a la cruda escrita;
  metadatos de fichero, sin leer contenido): v11 unos 3 min, v12 138 s, v13 unos 94 s, v14 unos
  91 s; en total **unos 9 minutos**, frente a los 32-51 estimados en §0.6 (factor 0,06 en vez de
  0,20-0,32). La extracción de fotogramas, unos minutos por vídeo.
- **HALLAZGO (importa): poco texto en v13 y v14.** Palabras por minuto de audio no silencioso: v11
  79, v12 40, v13 23, v14 25; segmentos por minuto: v11 6,2, v14 1,3, frente a 17 de la sesión v16
  (526 segmentos en 1823 s) con el mismo motor. `ms_con_habla` sale de `silencedetect` (umbral
  −35 dB), no de un detector de voz: cuenta también música o ruido, así que no prueba que se haya
  perdido habla. Pero el tiempo de GPU (unos 90 s para una hora) y los segmentos de varios minutos
  con una línea de texto (v14 0:00:22.730, el siguiente es 0:17:39) son compatibles con que
  faster-whisper (`vad_filter: true`) se haya saltado habla. Ver PARADA 1, punto 1.
- **Fuera de git, para Aleks:** `SHA256SUMS-v11-v14.txt`, 64 líneas (ruta y sha256 de cada fichero
  de `data/transcripciones/v11..v14`), en
  `C:\Users\USER\AppData\Local\Temp\claude\d82effbe86c6c5d6\bbf57367-ba2b-448c-8dc7-164f862fb2f7\scratchpad\SHA256SUMS-v11-v14.txt`
  (carpeta temporal de la sesión: conviene copiarlo antes de subirlo a «botsito copia a4»).
- **Los manifiestos nuevos** (cuatro de transcripción en `knowledge/corpus/transcripciones/`,
  cuatro de fotogramas en `knowledge/corpus/fotogramas/`), sin editar, en el commit de la fase 0 y
  F1. **Desviación:** el encargo los quiere en su commit; van con la fase 0 porque `make check` no
  sella con ficheros sin estadiar, y la fase 0 ya estaba escrita cuando acabó F1; el commit lo dice.

## 2. F2 · Qué cubre cada vídeo, por la voz (parcial: los fotogramas esperan la PARADA 1)

| Vídeo | Lo que dice la voz sobre los días | Instante |
|---|---|---|
| v11 | «vamos a hacer un backtesting del mes de julio, año 2026» (ningún día dicho); dos cierres de sesión y de día: «tenemos finalizado estos dos días» y «estas dos sesiones ya finalizaron, continuamos con la siguiente» | 0:00:01, 0:09:28, 0:16:25-0:19:26 |
| v12 | «continuamos con el video» (ningún día dicho); «continuamos con la siguiente sesión» | 0:00:00, 0:20:05 |
| v13 | «La última vez nos quedamos en el 10 de julio creo [...] vamos a darle continuidad»; termina «luego más tarde continuaré con, bueno, trataré de finalizarlo» | 0:00:06, 0:40:37 |
| v14 | «Nos quedamos en el día 17. Continuamos con el día 20.»; «continuamos con el siguiente día»; termina «eso es todo, de todo Julio» | 0:00:00, 0:23:16, 0:59:36 |

- Lo que la voz sostiene: v11 y v12 son el principio de julio (sin días); v13 empieza tras el 10;
  v14 empieza el 20 y llega al final del mes. **Que v13 llegue al 17 no lo dice la voz** (termina
  con «trataré de finalizarlo») y que v14 empiece en el 20 lo dice el trader. Los días exactos de
  v11, v12 y el final de v13, y los de v14, por fotogramas, tras la PARADA 1.
**Lo que añaden los fotogramas (localizados, §3.1):**

| Vídeo | Instante | Fotograma | Día en el eje |
|---|---|---|---|
| v11 | 0:10:05 (empieza el día 2) | `fr-v11-b83d5164/605000` | M15 al cierre del miércoles 1 de julio (15:00) |
| v11 | 0:14:50-0:19:20 | `…/890000` a `…/1160000` | jueves 2 de julio |
| v11 | 0:19:40 (empieza otro día) | `…/1180000` | H4; la reproducción llega al viernes (3 de julio) |
| v12 | 0:00:20 | `fr-v12-3eeb8cf9/20000` | no se lee (ventana de OBS delante) |
| v12 | 0:10:15 | `…/615000` | no se lee |
| v12 | 0:22:10 (sesión 11-15) | `…/1330000` | miércoles 8 de julio |
| v12 | 0:33:20 | `…/2000000` | viernes 10 de julio |

- v11 empieza el 1 de julio y llega al 3; v12 llega al 10 (la voz de v13, «nos quedamos en el 10
  de julio», lo confirma). Qué días cubre v12 al empezar (6 o 7) no se ha leído todavía.
- **Fotogramas abiertos hasta aquí: 12** (8 de v11, 4 de v12), uno de ellos el de la PARADA 1.

- **Cifras de resultados dichas en voz** (no se copian ni se usan, encargo): v11 0:03:06 y
  0:09:31, v13 0:19:11.

## 3. F3 · El vídeo frente al libro, días 1 a 17

### 3.0 El criterio (del consultor, escrito antes de abrir nada)

- La unidad son las operaciones de los 13 casos dev de julio. Para cada una: ¿aparece en el
  vídeo? Si aparece: día, dirección, entrada y stop leídos en pantalla, y la hora del gráfico.
- «Coincide» = mismo día y misma dirección; entrada y stop a 3 puntos o menos
  (`tolerancia_entrada_puntos` y `tolerancia_stop_puntos` de `criterio_fidelidad.yaml`; toda
  diferencia se apunta con su cifra, porque el libro y el gráfico son la misma serie de FX
  Replay); la hora del gráfico, en Europe/Madrid (UTC+2 en julio, ADR-0069), en el mismo minuto
  que `instante_utc` + 2 h (`instante_utc` es el llenado).
- Las operaciones que el vídeo enseña y no están en los casos, y las de los casos que no se ven,
  se listan aparte, sin resolverlas.
- Con lo medido se confirma o refuta que el libro está en Europe/Madrid (ENTRADA-JULIO.md §3.b).
- Primero un piloto con tres operaciones de 2026-07-02 11-15: si se localizan al menos dos con
  fecha, entrada y stop legibles, sigue el mes entero; si no, PARADA.
- Cómo se localiza un instante: por la transcripción filtrada (una entrada, un «0.80», un «loss»,
  un «break even» dichos en voz), y antes de abrir se comprueba que no hay ningún segmento oculto
  a ±30 s (en v11-v14 no hay ninguno en todo el vídeo, §1).

### 3.1 El piloto: 2026-07-02, sesión 11-15, en v11 (2026-11-08)

**Dónde está el día.** v11 0:10:01 «continuamos en M15, bueno nos adelantamos a H4» abre un día
nuevo; el fotograma `fr-v11-b83d5164/605000` (M15) tiene el cursor al final del miércoles 1 de julio
(«Wed 01 Jul '26 15:00» en el eje) y los separadores de sesión a las 07:00, 11:00 y 15:00. Las
entradas del 2 de julio en 11-15 caen entre 0:12:56 y 0:19:26 (un segmento del ASR, de 0:16:25 a
0:19:26, cubre tres minutos: «estas dos sesiones ya finalizaron»).

Los seis fotogramas del piloto (ningún segmento oculto en v11):

| Fotograma | Localizado en | Lo que se lee |
|---|---|---|
| `fr-v11-b83d5164/890000` (0:14:50) | 0:14:22 «si nos vamos a 5 segundos» | gráfico de 5 s, «Thu 02 Jul '26 11:28:30» en el eje; ninguna cifra de orden |
| `fr-v11-b83d5164/905000` (0:15:05) | el mismo segmento | 5 s; aviso «Order Added · Take profit added!», sin cifras; la caja de la posición a la derecha |
| `fr-v11-b83d5164/920000` (0:15:20) | 0:15:22 «trazar el punto correcto» | M1, «Thu 02 Jul '26 11:00» en el eje; aviso **«Closed your open position on EURUSD · Buy 100000 at 1.14102 · 100000 closed from avg entry 1.14102 · now flat»**; caja larga (verde sobre rojo) desde hacia las 11:34 |
| `fr-v11-b83d5164/930000` (0:15:30) | 0:15:26 «tenemos un win» | M1, el cursor en «Thu 02 Jul '26 11:32»; la misma caja, que empieza hacia las 11:34 |
| `fr-v11-b83d5164/1160000` (0:19:20) | 0:16:25 «estas dos sesiones ya finalizaron» | M1, «Thu 02 Jul '26 15:00»; dos marcas «be» del trader hacia las 12:25-12:31, una zona tachada hacia las 14:00 y una caja larga con niveles 0,25/0,5/0,8 hacia las 14:15-14:35 |

Frente al caso `caso-eurusd-2026-07-02` (seis compras en 11-15, en Madrid 11:34, 12:25, 12:45,
13:59, 14:10 y 14:23):

- **La primera (09:34:25 UTC = 11:34:25 Madrid, compra, entrada 1.14102, stop 1.1409): día,
  dirección y entrada COINCIDEN** (1.14102 en el aviso de cierre, Δ 0 puntos); la caja empieza en
  el minuto 11:34 del eje de M1, leído a ojo de la posición de la caja (no hay etiqueta de hora en
  la caja). **El stop no se lee.**
- Las otras cinco: hay marcas del trader en las horas de cuatro de ellas (dos «be» hacia las
  12:25-12:31, la zona tachada hacia las 14:00, la caja hacia las 14:15-14:35), pero **ni la
  entrada ni el stop se leen**: la grabación no enseña el eje de precios (el gráfico llega al
  borde derecho de la captura) y los avisos de FX Replay dicen la entrada solo al CERRAR una
  posición, sin el stop ni el precio de salida.
- **La hora del libro.** El eje del gráfico va en la hora de pared del replay (separadores de
  sesión a las 07:00, 11:00 y 15:00, que son las sesiones de Madrid), y la caja de la primera
  compra empieza a las 11:34 de ese eje, con el llenado del libro a las 09:34:25 UTC. Eso
  **confirma Europe/Madrid** (UTC+2 en julio) para el libro en esta operación; una sola
  operación con hora de caja leída a ojo.

**Fuera del piloto, en F2 (v12 0:33:20, `fr-v12-3eeb8cf9/2000000`, junto al segmento 0:33:17
«nos salta en B»):** M1, «Fri 10 Jul '26 10:00» en el eje; aviso **«Closed your open position on
EURUSD · Buy 100000 at 1.14378 · 100000 closed from avg entry 1.14378 · now flat»**. En
`caso-eurusd-2026-07-10`, la sexta compra: entrada 1.14378 (Δ 0 puntos), llenado 08:01:25 UTC =
10:01:25 Madrid; la vela de la entrada está junto a las 10:00 del eje. **Día, dirección y entrada
coinciden; hora compatible con Europe/Madrid (con UTC estaría a las 08:01, dos horas antes del
cursor). El stop (1.14354) no se lee.**

**Resultado del piloto: 1 operación de 3 con fecha y entrada legibles; 0 con el stop legible**
(y una más fuera del piloto, la del 10 de julio, igual: entrada sí, stop no). El
umbral del encargo («al menos dos con fecha, entrada y stop legibles») no se cumple: **PARADA 3**.

### Lo que necesito que decidas (PARADA 3)

0. Cómo sigue F3 sin el stop en pantalla. Opciones: (a) F3 compara por día, dirección, hora del
   eje (al minuto, cuando la caja o una marca lo permiten) y la entrada SOLO cuando un aviso de
   cierre la trae; el stop se apunta «no legible» en todas; «coincide» queda en lo que se puede
   leer, y el informe dice cuántas operaciones tienen cada campo; (b) se buscan más instantes por
   operación (los avisos de cierre de cada posición, segundos después de que el trader diga
   «loss», «win» o «break even») para subir el número de entradas leídas, con el mismo stop
   «no legible»; (c) F3 se queda en el piloto y el resto espera a otra fuente (que el trader grabe
   con el eje de precios a la vista, o una exportación con el stop). Recomiendo (a)+(b): el día, la
   dirección, la hora y la entrada cuando sale son lo que el vídeo da, y bastan para F2, para la
   hora del libro y para saber qué operaciones del libro se ven; el stop lo da el libro, no el vídeo.
   Coste de (c): F3 y F5 quedan sin medir.
1. F5 depende de «coincide». Con el stop no legible, ninguna operación puede cumplir el criterio
   completo del encargo. Opciones: (a) F5 usa «coincide» sin el stop (día, dirección, hora y la
   entrada cuando se lee) y el informe lo dice; (b) F5 no cambia el bloque hasta que haya una
   fuente con el stop, y `material_sin_video` se queda como está. Recomiendo (a), con la regla
   escrita en el informe ANTES de contar: lo que ADR-0092 §11 quiere saber es si el libro está
   grabado en vídeo, y eso lo dicen el día, la dirección y la hora.

### 3.3 F3 en los días de v11 y v12 (PARCIAL, 2026-11-09)

**CORRECCIÓN de lo que dijo la PARADA 3 («el stop no se lee en ninguna»), medida después del
piloto:** el stop SÍ sale en pantalla en dos formas. (1) Como PRECIO, en el aviso «Order Updated ·
Stop loss moved to X» o «Position Updated · Stop loss moved to X» cuando el trader lo coloca o lo
mueve: 7 de julio #3, «Stop loss moved to 1.14284» = el stop del libro (Δ 0). (2) Como DISTANCIA,
en las etiquetas de la herramienta de posición cuando el trader la selecciona («Stop: 0.00018
(0.016%)»): 3 de julio #1, 18 puntos = libro; 3 de julio #3, 19 puntos = libro. No sale en todas,
y el eje de precios sigue sin verse. Las cantidades en dinero de esas etiquetas no se copian.

**Una precisión del criterio (desviación para el consultor):** el borde izquierdo de la caja de
posición es cuándo la DIBUJÓ el trader, no cuándo se llenó (3 de julio #3: caja desde las 11:54,
llenado 12:02). El minuto del llenado solo se lee si el aviso de ejecución sale con la vela de la
entrada bajo el cursor. Cuando la entrada coincide y el llenado cae dentro de la caja pero el
minuto no se lee, la tabla dice «COINCIDE (minuto no legible)».

Fuente de las operaciones: `anexos/VIDEO-JULIO/operaciones-julio.txt` (`operaciones_julio.py`,
13 casos, 67 operaciones). Fotogramas: `fr-v11-b83d5164/<ms>` y `fr-v12-3eeb8cf9/<ms>`.

| Día | # | Madrid | Libro | Categoría | En el vídeo |
|---|---|---|---|---|---|
| 07-01 | 1 | 08:15:55 | compra 1.14042 | **COINCIDE** | v11/125000: «Stop order executed · Buy 100000 at 1.14042», vela de las 08:15 |
| 07-01 | 2 | 09:33:05 | compra 1.13958 | APARECE | v11/215000-235000: caja de Gann desde 09:17, el precio la atraviesa hacia 09:31; voz «tenemos otro loss» (0:03:06); aviso «Entry price moved to 1.13978» (v11/195000) |
| 07-01 | 3 | 12:59:05 | **venta** 1.13984 | APARECE | v11/525000: caja de VENTA proyectada desde ~13:05 con el cursor en ~12:58; la voz de la sesión dice «trades alcistas» (0:05:44) |
| 07-02 | 1 | 11:34:25 | compra 1.14102 | **COINCIDE** | v11/920000-930000: «Closed [...] Buy 100000 at 1.14102», caja desde 11:34 |
| 07-02 | 2 | 12:25:50 | compra 1.14069 | APARECE | v11/1010000: marca «be» del trader en ~12:25 |
| 07-02 | 3 | 12:45:20 | compra 1.14068 | APARECE | v11/1010000-1020000: «Order Added · Stop loss added!» (~12:43) y «Take profit moved to 1.14175» (~12:45); 107 puntos al objetivo frente a 36 al stop del libro, 1:3 |
| 07-02 | 4 | 13:59:30 | compra 1.14039 | APARECE (débil) | v11/1080000: solo trazos del trader sobre 13:52-14:03; sin caja ni aviso |
| 07-02 | 5 | 14:10:00 | compra 1.13996 | APARECE | v11/1080000-1110000: «Order Added · Take profit added!» (~14:06) y caja de Gann 14:05-14:15 |
| 07-02 | 6 | 14:23:05 | compra 1.13976 | APARECE | v11/1160000: caja larga ~14:16-14:38 |
| 07-03 | 1 | 09:24:00 | compra 1.14528 | **COINCIDE** | v12/100000-134000: «Closed [...] Buy 100000 at 1.14528», caja desde ~09:24, cursor 09:23; «Stop: 0.00018» = 18 puntos, el stop del libro |
| 07-03 | 2 | 09:43:00 | compra 1.14502 | APARECE | v12/190000: caja larga desde ~09:42-09:43 |
| 07-03 | 3 | 12:02:00 | compra 1.14423 | **COINCIDE (minuto no legible)** | v12/320000: «Closed [...] Buy 100000 at 1.14423»; «Stop: 0.00019» = 19 puntos, el stop del libro; caja 11:54-12:05 |
| 07-06 | 1-3 | 08:22-08:34 | compras | sin buscar: **no localizable** | su tramo de v12 (481-610 s) es un hueco del ASR: ningún segmento lo cubre y no se abre (ADR-0038) |
| 07-06 | 4 | 10:51:10 | compra 1.14172 | APARECE | v12/615000 y 690000: caja larga ~10:50-11:00 |
| 07-06 | 5 | 12:11:25 | compra 1.1413 | APARECE | v12/690000: «Position Updated · Stop loss moved to 1.1413» (~12:15): el break even a la entrada del libro |
| 07-07 | 1-2 | 07:02, 07:17 | compras | APARECE (débil) | v12/840000: trazos del trader sobre ~07:00-07:21 |
| 07-07 | 3 | 07:50:00 | compra 1.14293 | **COINCIDE** | v12/840000: «Stop order executed · Buy 100000 at 1.14293», vela ~07:50; «Stop loss moved to 1.14284» = el stop del libro |
| 07-07 | 4 | 08:14:00 | compra 1.14262 | APARECE | v12/900000-915000: caja larga (orden pendiente) colocada con el cursor en ~08:13 |
| 07-07 | 5-6 | 12:01, 12:08 | compras | APARECE | v12/1199000: caja larga ~11:53-12:11 |
| 07-07 | 7-8 | 13:51, 13:57 | compras | APARECE (débil) | v12/1199000: trazos del trader ~13:46-13:51 |
| 07-08 | 1 | 09:19:15 | compra 1.14203 | APARECE | v12/1330000: caja larga ~09:18-09:27 |
| 07-08 | 2 | 13:43:35 | compra 1.14039 | APARECE | v12/1442000: «Order Added · Stop loss added!» con el cursor en ~13:41 |
| 07-09 | 1 | 09:59:00 | compra 1.14338 | **COINCIDE (minuto no legible)** | v12/1590000: «Closed [...] Buy 100000 at 1.14338» con el cursor en ~10:06; v12/1658000: caja larga ~09:45-10:00 |
| 07-09 | 2 | 13:02:05 | compra 1.1424 | **no localizable** | su tramo de v12 (1661-1746 s) es un hueco del ASR; v12/1658000 (0:27:38) está aún en las 11:00 |
| 07-10 | 1-2 | 07:36:35, 07:45:20 | compras | APARECE | v12/1870000-1896000: caja larga cuyo borde izquierdo está en la marca «07:36» del eje, hasta ~07:51, y trazos del flujo del trader |
| 07-10 | 3-5 | 09:10-09:50 | compras | sin ver | v12/1960000 (0:32:40): trazos del trader, pero la captura no enseña el eje de horas |
| 07-10 | 6 | 10:01:25 | compra 1.14378 | **COINCIDE** | v12/2000000: «Closed [...] Buy 100000 at 1.14378», cursor 10:00 |
| 07-10 | 7-11 | 10:28-12:58 | 2 compras, 3 ventas | en v13 | espera la PARADA 4 |

**Recuento parcial (35 operaciones de los días 1 a 10 en v11/v12, sin las cinco del 10 que están
en v13):** COINCIDE 7 (dos con el minuto no legible); APARECE 21 (5 de ellas débiles, solo
trazos); CONTRADICE 0; no localizables 4 (tres del 6 y una del 9, en huecos del ASR de v12); sin
ver 3 (el 10, de 09:10 a 09:50). **Ninguna operación contradice al libro.**
El stop legible coincide en las tres en que sale (Δ 0).

**En el vídeo y no en el libro** (sin resolver): 8 de julio, caja larga ~11:05-11:25
(v12/1428000).

**La hora del libro:** en las 6 COINCIDE el eje de pared del replay (sesiones a las 07:00, 11:00 y
15:00) cae en `instante_utc` + 2 h. **El libro de julio está en Europe/Madrid**, como dijo
ENTRADA-JULIO.md §3.b por las velas.

**En v12, los huecos del ASR tapan operaciones del libro**: 481-610 s (las tres del 6 de julio de
08:22 a 08:34) y 1661-1746 s (la del 9 a las 13:02). Que el ASR calle justo donde el trader opera
es otro indicio, con los de §1.6, de que se saltó voz.

**Lo que falta de F3:** las tres del 10 de 09:10 a 09:50 (sin eje en el único instante localizado
de ese tramo), y los días 10 (tarde) a 17 en v13, que esperan la PARADA 4. Fotogramas abiertos
hasta aquí: **42** (12 del día 2026-11-08 y 30 del 2026-11-09: 10 de v11 y 20 de v12), todos por instante localizado; ninguno
con el cursor fuera de julio, marcas sobre otro mes ni panel de operaciones o de estadística.

## 4. F4 · Las 81 filas (reproducidas; la clasificación espera F2 y F3)

`anexos/VIDEO-JULIO/filas_hasta_t.py` (lee `patrones-cuenta-por-mes.txt` y la tabla «Operaciones
del trader» de `para-clasificar.txt`; sale con 1 si no son 81) → `anexos/VIDEO-JULIO/filas-hasta-t.txt`:
`OK: 81 filas en 22 sesiones`, por patrón `{'P1': 20, 'P2': 7, 'P3': 15, 'P5': 37, 'P6': 2}`
(P2 con |Δentrada| > 10 puntos: hay 8 con 10 o más y una con exactamente 10), en 13 días. Cada
fila lleva su hora de Madrid para buscarla en el vídeo. Cuatro filas llevan la marca «posible M»
de una hora de ticks perdida (07-10 05h y 07-16 11h UTC); la de 07-14 12h no toca ninguna fila.

### 4.1 Los días 1 a 10 (52 filas en 14 sesiones; los días 13 a 17, 29 filas en 8 sesiones, esperan la PARADA 4)

Lo del bot sale de `filas-hasta-t.txt` (bot o trader más cercano, Δentrada y Δinstante de
`patrones-cuenta-por-mes.txt`; orden, primer hecho y frenos de `para-clasificar.txt`; las filas P5
y P6 son órdenes del bot y van sin primer hecho ni frenos). La voz, de la transcripción filtrada
(v11 `tr-v11-…d5da10be`, v12 `tr-v12-…cb502503`). Las clases son PROPUESTAS (RUMBO §1 e); las
decide el consultor. Marcas: **[1-jul]** filas del 1 de julio (RUMBO §1 b: no van a la sesión 7);
**[hora perdida]** sesión con una hora de ticks perdida que toca la fila.

| Sesión | Filas | La voz del trader (vídeo, h:mm:ss) | Lo que hizo el bot | Clase propuesta | Por qué |
|---|---|---|---|---|---|
| 07-01 07-11 **[1-jul]** | P1 ×2 (sus compras 08:15, 09:33); P5 otro lado ×3 (ventas del bot 07:00-07:11) | v11 0:00:38-0:00:53: «A ver, este es nuestro rango / Por lo general, como no ha sido mitigado / Ni por debajo por una vela bajista / Ni por arriba por una vela alcista / Para actualizar el rango / Entonces nosotros nos enfocamos en buscar / Traits alcistas» | sesgo bajista; vende a 42-43 puntos y 64-76 min de sus compras; frenos: `detenido_por_cartuchos` | **regla desconocida** | el trader fija el lado por un RANGO de H4 que dura mientras no lo rompa una vela del color contrario; el bot, por la ruptura de la H4 anterior (RN-003) |
| 07-01 11-15 **[1-jul]** | P5 mismo lado ×1 (venta del bot 12:58:16) | v11 0:05:44-0:06:09: «Como todavía no se ha roto nuestro rango, entonces nosotros todavía nos planteamos traer alcistas [...] nos enfocamos en buscar 3 alcistas»; y el trader VENDE a las 12:59 (caja de venta en v11/525000, F3) | venta a 7 puntos y 48 s de la del trader | **sin clase** | casi pareja (7 puntos, fuera de 3); la voz dice compras y la pantalla una venta: a preguntar solo si se repite (es el 1 de julio) |
| 07-02 07-11 | P6 ×2 (compras del bot 07:37, 07:40; el trader no opera) | v11 0:10:52-0:11:18: «Y después tenemos esta, pero que el precio no llegó a romper por debajo en M1 [...] No hay entrada por el hecho de que no nos genera ninguno de los esquemas [...] y como esto de aquí no es ninguno de los esquemas, no se tradea» | dos compras donde el trader no ve entrada | **regla desconocida** | el trader descarta por «ninguno de los dos esquemas»; el bot entra |
| 07-02 11-15 | P3 ×3 (11:34, 12:25, 12:45) y P5 ×2 (11:13, 12:07) | v11 0:12:03-0:12:22: «este flujo de órdenes invalida el segundo esquema y el primer esquema, Entonces no hay entrada, No se toma este trade»; 0:13:58-0:14:16: «esta es una zona de punto breaker válida vale pero se actualiza»; 0:15:22-0:15:26: «lo ideal es esto, o sea, trazar el punto correcto» | compras en otras zonas, a 26-35 puntos y 18-38 min; órdenes o9 y o14 canceladas; frenos `detenido_por_cartuchos` | **sin clase** (a la rama de trazas) | la voz dice que la zona buena es el punto breaker «que se actualiza»; qué zona usó el bot solo lo dicen las trazas (07-02 es día de la rama de trazas, RUMBO §2) |
| 07-02 11-15 | P2 Δ43 (14:10) y P3 (14:23) | v11 0:16:06-0:16:25: «este es un break-even perdón, encontramos aquí, yo activa, retrocede, sube, break-even»; la voz no habla de un tope de intentos | bot detenido por RN-016 (`detenido_por_cartuchos`) desde las 14:08, tras tres pérdidas | **regla desconocida** | el trader sigue entrando tras tres pérdidas en el barrido; el bot no (cartuchos). Pendiente con dueño de §8: el motor lo mide la rama de trazas |
| 07-02 11-15 | P5 ×2 (14:02, 14:05) | (la misma) | compras a 0 puntos (14:02, frente a la del trader de 13:59) y a 43 | **sin clase** | la de 14:02 es casi pareja (Δ0, 2 min 39 s); la de 14:05, de más |
| 07-03 07-11 | P2 Δ17 (09:24) y P5 ×4 (08:02, 08:03, 09:24, 09:35) | v12 0:00:15-0:00:58: «aquí no había entrada porque es con mecha, sabemos que tiene que ser con cuerpo [...] aquí sí que tenemos una entrada vale porque nos genera un breaker con cuerpo y aquí está la zona de liquidez» | compras 80 min antes y a 15-30 puntos; una a 17 puntos y 42 s de la del trader (o3 cancelada) | **error nuestro (sospecha)** | la voz exige la ruptura del breaker en M1 CON CUERPO; si el bot entra con mecha, la pieza sospechosa es la que valida esa ruptura. Lo mide la rama de trazas |
| 07-03 11-15 | P5 (11:13) y P3 (12:02) | v12 0:03:19-0:04:35: «todavía no ha sido roto el breaker, entonces nos enfocamos [...] nosotros igual si se desarrolla el precio pues vamos actualizando, o sea empieza aquí, no rompe, actualiza aquí» | compra 48 min antes y 72 puntos más arriba (o17 cancelada) | **sin clase** (a la rama de trazas) | el trader «va actualizando» la zona; el bot se queda en la primera |
| 07-06 07-11 | P1 ×4 (08:22, 08:29, 08:33, 10:51) | v12 0:06:27-0:06:47: «como no ha sido roto hasta ahora por debajo para buscar operativos bajistas con una vela roja con mechago en cuerpo entonces ni por arriba con una vela verde para poder actualizar rango alcista nuevamente entonces nosotros como está dentro del rango alcista nos enfocamos todavía en buscar operativas alcistas» (las tres de las 08:22-08:33 caen en un hueco del ASR de v12) | sesgo bajista; ninguna operación; `orden_dimensionada[productoras sin cumplirse]` | **regla desconocida** | el rango de H4 (como el 1 de julio) |
| 07-06 11-15 | P1 (12:11) | v12 0:10:10: «no se rompe el rango todavía, entonces, nos enfocamos en 3 alcistas» | igual | **regla desconocida** | el rango de H4 |
| 07-07 07-11 y 11-15 | P1 ×8 (sus ocho compras: 07:02, 07:17, 07:50, 08:14, 12:01, 12:08, 13:51, 13:57) y P5 otro lado ×6 (ventas del bot 10:26-14:35) | v12 0:10:49 y 0:17:25-0:17:38 (un segmento del ASR que cruza del 6 al 7: el fotograma de 0:11:30 aún es el 6): «El CISA [alcista], ok, porque, mira, no sé cuantos días, tres días, dos días creo que lo / han mantenido, primera vez que veo esto, interesante, entonces, nos enfocamos ahí / en tres alcistas» | sesgo bajista; ventas a 18-67 puntos | **regla desconocida** | el rango de H4 que dura días |
| 07-08 07-11 | P5 (10:25) | v12 0:20:05: «aquí liquidez, liquidez, no tenemos entrada, no hay punto breaker de ruptura aquí, pero igual con este desarrollo de este order flow, invalidaría» | compra 66 min después y 86 puntos más abajo | **regla desconocida** | sin punto breaker de ruptura no hay entrada |
| 07-09 07-11 | P5 ×2 (09:52 Δ4, 10:45) | v12 0:25:24-0:27:32: «nos enfocamos en alcistas [...] el enfoque es alcista todavía» | compras a 4 puntos y 7 min antes de la del trader, y otra de más | **sin clase** | la primera es casi pareja; la segunda, de más |
| 07-09 11-15 | P5 (12:59) y P2 Δ13 (13:02) | — (su tramo, 1661-1746 s de v12, es un hueco del ASR) | compra a 13 puntos y 3 min antes (o16 cancelada) | **sin clase** | sin voz del trader en ese tramo |
| 07-10 07-11 **[hora perdida]** | P3 misma entrada otra hora (07:45, «posible M»), P5 (09:59 Δ4), P3 ×2 (10:28, 10:42) | v12 0:30:49: «la condición o sea aquí cuando se completa esta zona de aquí o sea por encima cierra esto esta zona de control se desarrolla se pone en break even la entrada»; las de 10:28 y 10:42 están en v13 (espera la PARADA 4) | compra a 3 puntos y 17 min antes (07:45); compra a 4 puntos y 2 min antes (09:59); o12 cancelada | 07:45: **material incompleto**; 09:59: **sin clase**; 10:28 y 10:42: **hasta la PARADA 4** | la de 07:45 cae junto a la hora perdida de las 05h UTC (respaldo M1); la de 09:59 es casi pareja |

**Las preguntas para el trader (si el consultor confirma «regla desconocida»), en su idioma:**

1. **El rango de H4** (24 filas: las del 1, 6 y 7 de julio): «Cuando dices que el rango de H4 no ha
   sido mitigado y sigues buscando compras, ¿qué vela marca ese rango? ¿Una vela roja que rompe
   solo la vela anterior, pero no el mínimo del rango, te cambia el lado? ¿Cuántos días puede
   durar un rango?» (RUMBO §1 a: es la que más filas mueve.)
2. **Los dos esquemas** (3 filas: 07-02 07-11 y 07-08): «Cuando dices que no hay entrada porque no se
   forma ninguno de los dos esquemas, ¿qué tiene que tener la zona para que valga? ¿Y sin un punto
   breaker de ruptura, nunca hay entrada?»
3. **Seguir tras tres pérdidas** (2 filas, 07-02 14:10 y 14:23): «El 2 de julio seguiste entrando
   en la misma sesión después de tres pérdidas. ¿Hay un número de intentos por barrido de
   liquidez, o depende de algo?»

**«Error nuestro» (sospecha), para la rama de trazas (R4.4):** 07-03 07-11, la validación de la
ruptura del breaker en M1 con cuerpo y no con mecha. No se toca nada aquí.

**Recuento de los días 1 a 10 (52 filas):** regla desconocida 29 (rango de H4 24, esquemas 3,
intentos 2); error nuestro (sospecha) 5; material incompleto 1; sin clase 15; hasta la PARADA 4,
2.

## 7. F7 · Candidatas a evidencia (no se crea ningún ítem)

De la transcripción filtrada; v13 y v14, de las versiones viejas (`tr-v13-…1aeb45d5`,
`tr-v14-…2253ec10`), citables por su id con `--transcripcion` (PARADA 4).

| # | Vídeo, h:mm:ss | Lo que dice | Lo que sostendría |
|---|---|---|---|
| 1 | v11 0:00:38-0:00:53 | «este es nuestro rango / Por lo general, como no ha sido mitigado / Ni por debajo por una vela bajista / Ni por arriba por una vela alcista / Para actualizar el rango / Entonces nosotros nos enfocamos en buscar / Traits alcistas» | el sesgo por un rango de H4 no mitigado (24 filas de F4) |
| 2 | v11 0:05:44-0:06:09 | «Si en caso esta vela roja hubiera roto con mecha o con cuerpo por debajo de esta vela, hubiéramos trazado nuestro rango bajista y esta operativa sería bajista» | qué rompe el rango: mecha o cuerpo |
| 3 | v12 0:06:27-0:07:13 | «...como está dentro del rango alcista nos enfocamos todavía en buscar operativas alcistas / es que es muy pero muy pero muy importante y es lo principal yo diría que un 70% o sea que uno defina bien el rango el / el bias» | el peso del sesgo en el método |
| 4 | v11 0:02:16-0:02:48 | «este punto de aquí nos queda invalidado por el hecho de que aquí hay un breaker o sea bueno este retroceso complejo no debería de darse [...] la zona de control dentro de esto tiene que ser limpia si no no es válido» | el descarte de una zona por un retroceso complejo |
| 5 | v11 0:11:03-0:11:18 | «No hay entrada por el hecho de que no nos genera ninguno de los esquemas [...] como esto de aquí no es ninguno de los esquemas, no se tradea» | el porqué de un descarte: los dos esquemas |
| 6 | v12 0:00:15-0:00:58 | «aquí no había entrada porque es con mecha, sabemos que tiene que ser con cuerpo [...] aquí sí que tenemos una entrada vale porque nos genera un breaker con cuerpo» | la ruptura del breaker en M1, con cuerpo |
| 7 | v12 0:17:55-0:18:47 | «se ve roto, vale, pero nos saca, unicuel, si es unicuel, podemos reentrar [...] Como es un equal, aquí se valida / Este punto de liquidez / Este punto de breaker, mejor dicho» | la reentrada tras un stop en un mínimo igual (cartuchos, RN-016) |
| 8 | v12 0:30:49 y v13 0:00:29-0:05:28 (vieja) | «cuando se completa esta zona de aquí [...] esta zona de control se desarrolla se pone en break even la entrada»; «apenas se desarrolla la zona de control nosotros tomamos en break even, que yo no lo haga no significa que no se deba hacer [...] es una de las condiciones más importantes, o sea el break even» | cuándo se pasa a break even, y que en el backtest no siempre lo hace |
| 9 | v14 0:20:10 (vieja) | «el break even se termina por encima, entonces ahí ubicas el punto de break even, si lo tomas por aquí no te va a dar para que pongas break even [...] se termina con cuerpo por encima, es una validación para que puedas poner break even» | la condición del break even: cierre con cuerpo por encima |
| 10 | v14 0:42:02 (vieja) | «aquí hay una entrada que no le voy a tomar para no afectar al mostreo» | **que el trader deja de tomar entradas válidas en el backtest a propósito**: afecta a la lectura de las operaciones de más del bot (P5) |
| 11 | v13 0:17:34-0:17:57 (vieja) | «el rr 13 lo calculamos [...] para calcular el lotaje y todo eso pues claramente [...] se efectúa desde 0.8 y aquí ya para tener ese 0.75 de beneficio adicional» | el 0,8 y el lotaje (lineamiento del stop 0,8) |

**Cifras de resultados dichas en voz** (no se copian ni se usan): v11 0:03:06 y 0:09:31, v13
0:19:11.

## PARADA 1 · un fotograma de julio enseña velas de meses anteriores (2026-11-08)

**Qué pasó.** El primer fotograma abierto de la rama, `fr-v11-b83d5164/5000` (v11 0:00:05),
localizado en el segmento 0:00:01.880 («vamos a hacer un backtesting del mes de julio, año 2026»;
v11 no tiene ningún segmento oculto), es el gráfico H4 del replay de FX Replay. A la izquierda del
cursor de reproducción enseña las velas de las semanas anteriores a julio de 2026, de meses que no
son libres. El encargo manda: «Si enseña un gráfico de un mes que no sea julio de 2026, se cierra,
no se describe, y PARADA con el vídeo y el instante». Cerrado, no se describe, ningún otro
fotograma abierto; declarado el mismo día en `HOLDOUT-EXPOSICIONES.md`.

**Por qué importa para toda la rama.** Es lo que hace un replay: el gráfico enseña siempre la
historia anterior al cursor, y el trader mira H4 al empezar cada día («nos vamos a H4 para ver el
bias», v13 0:00:06). Los días del principio de julio en H4 enseñarán casi siempre velas de junio, y
cualquier H4 algunas semanas atrás. Con la regla al pie de la letra, F2 (cuando la voz no basta) y
F3 (fecha, entrada, stop y hora en pantalla) solo podrían abrir fotogramas en M1 o M15 con el
gráfico entero dentro de julio, y no se puede saber antes de abrirlo (ADR-0038).

**Lo que dicen los ADR.** Las velas no son holdout: «LAS VELAS DE `data/` SE LEEN para recalcular
ventanas, y eso NO es abrir un holdout» (CLAUDE.md, punto 2; ADR-0021 §1). Lo prohibido es la
etiqueta, el detalle por operación del trader de un día reservado, un agregado o Analytics
(ADR-0037). Un gráfico de precio de FX Replay con velas de junio no trae ninguna de esas cosas,
salvo que el trader haya dibujado o comentado operaciones de esos días.

### Lo que necesito que decidas (PARADA 1)

0. Qué es «un gráfico de un mes que no sea julio». Opciones: (a) un gráfico cuyo CURSOR DE REPLAY
   no está en julio de 2026, o en el que el trader enseña, marca o comenta operaciones, posiciones
   o resultados de otro mes; las velas de contexto a la izquierda de un replay de julio se pueden
   ver, no se describen más allá de lo que el informe necesita (día, hora y precios de julio) y se
   declaran una vez en HOLDOUT-EXPOSICIONES («los fotogramas de H4 enseñan velas de contexto de
   semanas anteriores»); (b) la regla al pie de la letra: cualquier vela de otro mes cierra el
   fotograma, y F2/F3 se hacen solo con fotogramas de M1/M15 que caigan enteros en julio,
   aceptando una PARADA por cada uno que no. Recomiendo (a): las velas no son holdout (ADR-0021
   §1), y (b) hace F3 casi imposible sin ganar nada que proteja una etiqueta. Coste de (b): muchas
   PARADAS y un F3 con pocas operaciones legibles.
1. El poco texto de v13 y v14 (§1, HALLAZGO). Opciones: (a) Aleks escucha un tramo de un hueco
   (por ejemplo v14 de 0:06:00 a 0:17:00, o un minuto suelto dentro) y dice si el trader habla; si
   habla, se retranscribe v13 y v14 con `--reemplaza-a` (manifiesto nuevo, el viejo queda) y
   fragmentos más cortos (`--objetivo-s`, `--min-s`, `--max-s` de `corpus transcribe`), y se mide
   otra vez; (b) se trabaja con lo que hay y el informe dice, en F2 a F7, que la voz de v13 y v14
   puede estar incompleta. Recomiendo (a): un minuto de escucha decide, y la retranscripción
   cuesta unos minutos de GPU. Coste de (b): F4 y F7 pueden perder la voz del trader justo en las
   filas de julio de v13 (días 13 a 17).

**Mientras tanto** (no abre nada): sigue F1 (la extracción de fotogramas de v12, v13 y v14 y las
comprobaciones), y se sellan y commitean la fase 0 y F1. F2 por la VOZ queda leída (abajo); F3,
F6 y la parte de F4 que necesita pantalla esperan la respuesta.

## Respuesta del consultor a la PARADA 1 (2026-11-08)

Copiada tal cual:

> Respuesta del consultor a la PARADA 1 de trabajo/video-julio (2026-11-08). Cópiala tal cual en el informe, en su sección, y aplícala. Desviación aceptada: los ocho manifiestos de F1 van en el commit de la fase 0 (c87cff5).
>
> 0. Qué cuenta como «un gráfico de un mes que no sea julio». Opción (a), precisada:
>    - Las velas de contexto de otros meses, a la izquierda de un gráfico de julio, se pueden ver. Las velas no son holdout (ADR-0021 §1; CLAUDE.md, «Que se puede mirar y que no», punto 2). No se describen, no se comparan con nada y no se usan. Se declaran una vez en la fila del día de HOLDOUT-EXPOSICIONES («fotogramas de v11-v14 con velas de contexto de meses anteriores a julio, sin marcas del trader»).
>    - Lo que NO se mira de otro mes:
>      · el cursor del replay situado fuera de julio de 2026;
>      · las marcas del trader (cajas, niveles, líneas, órdenes o posiciones) sobre velas de un día que no sea de julio de 2026;
>      · cualquier panel de operaciones o de estadística.
>      Si un fotograma lo trae, se cierra, no se describe, se apunta vídeo e instante y se declara el mismo día. No es PARADA: sigue con el siguiente instante localizado.
>    - PARADA solo si el trader opera o comenta en voz operaciones de otro mes. Es un tramo que podría tener que ir a tramos_no_citables.yaml, y eso lo decide el consultor.
>
> 1. El poco texto de v13 y v14: ni (a) ni (b). Primero se mide, sin que Aleks escuche nada:
>    1.1 Con ffmpeg (las formas de GUARDIA-FFMPEG.md: volumedetect y silencedetect=noise=-50dB:d=30), sobre v11 como control y sobre v13 y v14:
>        - el volumen medio del vídeo entero;
>        - los silencios de 30 s o más;
>        - el volumen medio de cada hueco sin texto de 5 minutos o más (con -ss y -t sobre el hueco).
>        Si la guardia niega el comando, PARADA con el comando exacto y lo lanza Aleks con «!».
>    1.2 Regla de decisión, escrita en el informe ANTES de medir:
>        - si los huecos de v13 o v14 no son silencio (menos de la mitad de su duración cae en un silencio de silencedetect y su volumen medio está a menos de 10 dB del de v11), el ASR se saltó voz;
>        - si son silencio, el texto es el que hay, y el informe dice dónde no habla el trader.
>    1.3 Si el ASR se saltó voz: retranscribe v13 y v14 con uv run botsito corpus transcribe --video v13 --reemplaza-a <su tr-id> --objetivo-s 300 --min-s 180 --max-s 420 (y lo mismo con v14). Uno a uno, nunca mientras corre un make check.
>        - Se queda la transcripción que cubra con texto más minutos de los huecos.
>        - Si la nueva tampoco los cubre, PARADA con lo medido: entonces Aleks escucha un minuto.
>        - Los manifiestos nuevos, en su commit, sin editar los anteriores.
>        - transcript check en verde, y el número de segmentos y de ocultos por motivo de las dos versiones, en el informe.
>    1.4 Haz 1.1 a 1.3 antes de F2 y F4 de los días de v13 y v14. El piloto de F3 (2026-07-02, en v11) y lo de v11 y v12 no esperan.
>
> 2. El SHA256SUMS:
>    - Regenéralo al final de F1 o de 1.3, con las transcripciones que queden activas y también las reemplazadas.
>    - Escríbelo en C:\Users\USER\Desktop\SHA256SUMS-v11-v14.txt (fuera del repo y de la carpeta temporal).
>    - El informe dice cuántas líneas tiene.
>
> Sigue sin parar hasta la PARADA final: F2, F3 con el piloto, F4 a F7 y el revisor.

### 1.5 Los huecos de v13 y v14: la regla, escrita ANTES de medir (respuesta a la PARADA 1, punto 1.2)

Un **hueco** es un tramo sin texto de 5 minutos o más del manifiesto de transcripción (`huecos`,
`hueco_transcripcion_s: 30`). Para cada hueco de v13 y v14:

- **cubierto por silencio** = la suma de su intersección con los silencios de
  `silencedetect=noise=-50dB:d=30` sobre el vídeo entero, dividida por su duración;
- **volumen del hueco** = `mean_volume` de `volumedetect` sobre el hueco (`-ss` inicio, `-t`
  duración);
- **referencia** = `mean_volume` de `volumedetect` sobre v11 entero (el control, el vídeo con más
  texto por minuto).

**El hueco NO es silencio (el ASR se saltó voz) si cubierto por silencio < 0,5 Y
|volumen del hueco − referencia| < 10 dB.** Si algún hueco de v13 o v14 lo cumple, se retranscribe
ese vídeo (1.3). Si no, el hueco es silencio: el texto es el que hay y F2 dice dónde no habla el
trader.

### 1.6 Lo medido (1.1), y la PARADA 2: el volumen de cada hueco lo lanza Aleks

Las formas de la lista cerrada de la guardia, sobre los `.mkv` (desde su carpeta, rutas literales):

| Vídeo | `mean_volume` (vídeo entero) | `max_volume` | Silencios ≥ 30 s a −50 dB |
|---|---|---|---|
| v11 (control) | −39,0 dB | −4,9 dB | ninguno |
| v13 | −41,8 dB | −7,9 dB | ninguno |
| v14 | −40,0 dB | −1,4 dB | ninguno |

- **Cubierto por silencio = 0 en todos los huecos** (no hay ningún silencio de 30 s o más en ningún
  vídeo): la primera condición de la regla (< 0,5) se cumple en todos. La decisión depende solo del
  volumen de cada hueco.
- **Huecos de 5 minutos o más** (manifiesto de transcripción): **v13, ninguno** (sus cuatro
  huecos duran 44, 279, 108 y 291 s), así que la regla no se aplica a v13 y su texto es el que
  hay. **v14, cuatro**: 340,460 s (718,6 s), 1403,718 s (573,3 s), 1985,272 s (536,8 s) y
  2669,988 s (322,8 s); el de 1226,108 s dura 44 s.
- **El volumen de cada hueco necesita `-ss`/`-t`, y la guardia lo niega** («`ffmpeg -ss` antes
  de `-i`: solo las opciones generales»; GUARDIA-FFMPEG.md §1, punto 2). No se rodea (respuesta,
  1.1): **PARADA 2**. Los cuatro comandos, para que Aleks los lance con «!»:

```
! ffmpeg -hide_banner -nostdin -ss 340.460 -t 718.647 -i "C:/Users/USER/Desktop/Bot v3/corpus/Estrategia del trader/Material adicional de su operativa/Backtest Julio 2026/2026-10-04 12-40-14.mkv" -vn -sn -dn -af volumedetect -f null - 2>&1 | grep mean_volume
! ffmpeg -hide_banner -nostdin -ss 1403.718 -t 573.284 -i "C:/Users/USER/Desktop/Bot v3/corpus/Estrategia del trader/Material adicional de su operativa/Backtest Julio 2026/2026-10-04 12-40-14.mkv" -vn -sn -dn -af volumedetect -f null - 2>&1 | grep mean_volume
! ffmpeg -hide_banner -nostdin -ss 1985.272 -t 536.786 -i "C:/Users/USER/Desktop/Bot v3/corpus/Estrategia del trader/Material adicional de su operativa/Backtest Julio 2026/2026-10-04 12-40-14.mkv" -vn -sn -dn -af volumedetect -f null - 2>&1 | grep mean_volume
! ffmpeg -hide_banner -nostdin -ss 2669.988 -t 322.817 -i "C:/Users/USER/Desktop/Bot v3/corpus/Estrategia del trader/Material adicional de su operativa/Backtest Julio 2026/2026-10-04 12-40-14.mkv" -vn -sn -dn -af volumedetect -f null - 2>&1 | grep mean_volume
```

- Con la referencia de v11 (−39,0 dB), un hueco con `mean_volume` por encima de −49,0 dB es «no
  silencio» y v14 se retranscribe (1.3). Mientras, sigue lo que no espera (1.4): el piloto de F3 y
  v11/v12.
- Propuesta para la deuda del carril de guardias: la forma de medida de ffmpeg no admite `-ss` y
  `-t` sobre un tramo, que la medida de un hueco necesita.

**Respuesta a la PARADA 2 (2026-11-09):** Aleks lanzó con «!» el primero de los cuatro comandos:
`mean_volume: -38.6 dB` para el hueco de v14 de 340,460 s (718,6 s). Cubierto por silencio 0 y
|−38,6 − (−39,0)| = 0,4 dB < 10 dB: **el hueco NO es silencio; el ASR se saltó voz en v14.** Con
un hueco basta (la regla: «si algún hueco [...] lo cumple, se retranscribe ese vídeo»). Después
Aleks lanzó el segundo: `mean_volume: -41.4 dB` para el hueco de 1403,718 s (573,3 s); |−41,4 −
(−39,0)| = 2,4 dB < 10 dB: tampoco es silencio. El tercero: `mean_volume: -41.5 dB` para el hueco
de 1985,272 s (536,8 s); 2,5 dB: tampoco. El cuarto: `mean_volume: -42.1 dB` para el hueco de
2669,988 s (322,8 s); 3,1 dB: tampoco. **Los cuatro huecos de v14 de 5 minutos o más tienen un
volumen medio a menos de 3,1 dB del de v11 y ningún silencio de 30 s: ninguno es silencio.** Se aplica 1.3: v14 y también v13 (la respuesta nombra los dos; v13 no tiene
huecos de 5 minutos, pero su texto por minuto es igual de bajo, §1), uno a uno, con
`--objetivo-s 300 --min-s 180 --max-s 420`, y se queda la versión que cubra con texto más minutos
de los huecos.

### 1.7 La retranscripción (1.3) y la PARADA 4 (2026-11-09)

`uv run botsito corpus transcribe --video <v> --reemplaza-a <tr-id> --objetivo-s 300 --min-s 180 --max-s 420`,
v14 y luego v13, uno a uno, sin `make check` a la vez:

| Vídeo | Versión | Segmentos | Fragmentos (con 0 segmentos) | Palabras (CLI filtrada) | Ocultos (a/b/c) | Huecos > 30 s |
|---|---|---|---|---|---|---|
| v13 | `tr-v13-large-v3-int8-float16-1aeb45d5` (vieja) | 31 | 4 | 645 | 0 | 4 (44+279+108+291 s) |
| v13 | `tr-v13-large-v3-int8-float16-7f5333a0` (nueva, activa) | 24 | 8 (0) | 926 | 0 | 6 (267+245+193+109+203+273 s) |
| v14 | `tr-v14-large-v3-int8-float16-2253ec10` (vieja) | 29 | 6 | 565 | 0 | 5 (719+44+573+537+323 s) |
| v14 | `tr-v14-large-v3-int8-float16-1d289df6` (nueva, activa) | 47 | 12 (5) | 584 | 0 | 7 (310+567+44+573+537+317+36 s) |

- **Cuánto de los huecos viejos cubre la nueva con texto:** v13, unos 96 s de 722 s (44 del
  primero, 34 del segundo, 0 del tercero, 18 del cuarto); v14, en los cuatro huecos de 5 minutos o
  más, unos 163 s de 2151 s (158 del primero, 0 del segundo y del tercero, 5 del cuarto). **A
  cambio, la nueva pierde texto donde la vieja lo tenía**: v13, de 29 a 296 s, de 703 a 896 s y de
  1305 a 1508 s; v14, de 24 a 334 s.
- `uv run botsito corpus transcript check`: `OK: 24 transcripciones coherentes con el disco y el
  glosario`. Los dos manifiestos nuevos, sin editar los anteriores, en su commit.
- **SHA256SUMS** (respuesta, punto 2): `C:\Users\USER\Desktop\SHA256SUMS-v11-v14.txt`, **116
  líneas**, las transcripciones activas y las reemplazadas de v11 a v14 (las dos carpetas de v13 y
  de v14) y el audio de cada vídeo.
- **La regla de 1.3:** «Se queda la transcripción que cubra con texto más minutos de los huecos»
  da la nueva en los dos (96 s y 163 s frente a 0); «Si la nueva tampoco los cubre, PARADA con lo
  medido: entonces Aleks escucha un minuto» se cumple también: la nueva cubre un 13 % (v13) y un
  8 % (v14) de los huecos. **PARADA 4.**

### Lo que necesito que decidas (PARADA 4)

0. Que Aleks escuche un minuto (respuesta a la PARADA 1, 1.3). Propuesta: v14 de 0:10:00 a
   0:11:00 (dentro del hueco de 340-1059 s en las dos versiones y del de 335-902 s de la nueva) y
   decir si el trader habla. Si habla, el problema es del ASR con este audio (faster-whisper con
   `vad_filter`, el VAD de Silero), no de los parámetros de corte, y la siguiente prueba sería otra
   configuración del motor, que `corpus transcribe` no expone (`src/` protegido): rama propia.
1. Qué versión queda activa. La nueva lo es por `--reemplaza-a`; la regla la elige por los huecos,
   pero pierde texto que la vieja tenía. Opciones: (a) se queda la nueva como activa (la regla
   literal) y, para los tramos que solo tiene la vieja, se cita la vieja por su id
   (`transcript show --transcripcion <id>`, `cli.py:2964`); (b) la vieja es la de referencia en F2 a
   F7, citada siempre por su id, y la nueva solo para los tramos que añade (un manifiesto
   reemplazado no se puede volver a activar sin otra retranscripción). Recomiendo (a): las dos
   versiones quedan en el repo, la CLI filtrada lee cualquiera, y cada cita dice de cuál sale.

**Mientras tanto** sigue lo que no depende de esto (respuesta, 1.4): v11 y v12. F3 espera la
PARADA 3.

## Respuesta del consultor a las PARADAS 2 y 3 (2026-11-09)

Copiada tal cual:

> Respuesta del consultor a las PARADAS 2 y 3 de trabajo/video-julio (2026-11-09). Cópiala tal cual en el informe, en su sección, y aplícala.
>
> PARADA 2. Aleks acaba de lanzar con «!» los cuatro comandos de §1.6, y sus líneas mean_volume están arriba en esta conversación. Cópialas al informe y aplica la regla de decisión escrita antes de medir: el umbral es -49,0 dB, a 10 dB del -39,0 de v11.
> - Si algún hueco de v14 da más de -49,0 dB, retranscribe v14 con el punto 1.3 de la respuesta a la PARADA 1 (--reemplaza-a, --objetivo-s 300, --min-s 180, --max-s 420), con su manifiesto en su commit. Se queda la transcripción que cubra con texto más minutos de los huecos. Si la nueva tampoco los cubre, PARADA con lo medido.
> - Si ninguno pasa de -49,0 dB, el texto es el que hay, y el informe dice dónde no habla el trader.
> - El volumen no distingue voz de música. El informe lo dice al lado de la decisión, sin cambiar la regla.
> - La negativa de la guardia a ffmpeg con -ss/-t sobre un vídeo del corpus es un falso positivo de la lista cerrada de GUARDIA-FFMPEG. Va como línea de Technical Debt del carril de guardias en las propuestas para la orden de cierre. Aquí no se toca la guardia.
>
> PARADA 3. La grabación no enseña el eje de precios y el stop nunca se ve: es un límite del instrumento, medido en el piloto, no un resultado. F3 sigue con (a) más (b), y este criterio se escribe en el informe ANTES de comparar el resto:
> - Tres categorías por operación de los 13 casos:
>   · COINCIDE: día, dirección y hora en Europe/Madrid (el mismo minuto que instante_utc + 2 h), con la entrada leída en el aviso de cierre a 3 puntos o menos;
>   · APARECE SIN ENTRADA LEGIBLE: día, dirección y hora por la marca del trader o por su voz, sin cifra de entrada (para cada operación busca antes su aviso de cierre);
>   · NO APARECE.
>   Además, CONTRADICE: aparece con otra dirección, a otra hora, o con la entrada a más de 3 puntos.
> - El stop va como «no legible» en todas, y el informe dice que el vídeo no sirve para el stop: la caja dispersa (A-48) se le pregunta al trader en directo en la sesión 7.
> - Las operaciones del vídeo que no están en los casos se listan aparte, como dice el encargo.
> - F5 cuenta así:
>   · primera vía (julio sale de provisionales_con_video): las operaciones de los 13 días están todas en COINCIDE o en APARECE, ninguna CONTRADICE y ninguna está en NO APARECE;
>   · si no, segunda vía, y dias_con_video lleva los días en que se cumple eso.
>   Es lo que pregunta material_sin_video (S-14): si las sesiones del libro están grabadas. El stop no cambia esa respuesta.
> - El piloto vale con dos COINCIDE (2 y 10 de julio, Δ 0) y la confirmación de que el libro está en Europe/Madrid.
>
> Sigue sin parar hasta la PARADA final: lo que quede de F2, F3 con este criterio, F4 a F7, el SHA256SUMS en el Escritorio y el revisor.

### Cómo se aplica

- **PARADA 2:** las cuatro líneas `mean_volume` de Aleks están en §1.6 (−38,6, −41,4, −41,5 y
  −42,1 dB). Las cuatro pasan de −49,0 dB: v14 se retranscribió ya (§1.7, antes de esta
  respuesta, por la regla escrita) y la nueva tampoco cubre los huecos: es la **PARADA 4** (§1.7),
  que sigue abierta. **El volumen no distingue voz de música**: la decisión «el ASR se saltó voz»
  es la de la regla escrita, y lo que suena en los huecos puede ser música o ruido de fondo; por
  eso la PARADA 4 pide escuchar un minuto. La negativa de la guardia a `-ss`/`-t`, a las propuestas
  para la orden de cierre (Technical Debt, carril de guardias).
- **PARADA 3:** el criterio, abajo (§3.2), escrito antes de comparar el resto. El piloto vale
  (dos COINCIDE, el libro en Europe/Madrid).
- **Orden:** por 1.4 de la respuesta a la PARADA 1, F2 y F4 de los días de v13 y v14 esperan la
  PARADA 4; F3 empieza por los días de v11 y v12 (1, 2, 3, 6, 7, 8, 9 y 10).

### 3.2 El criterio de F3 (respuesta a la PARADA 3), escrito ANTES de comparar el resto

Para cada operación de los 13 casos dev de julio (`instante_utc` es el llenado; Madrid = UTC+2):

- **COINCIDE**: el mismo día, la misma dirección y la hora en el mismo minuto que `instante_utc`
  + 2 h, leída en el eje del gráfico junto a la caja o la marca del trader; y la entrada leída en el
  aviso de cierre de FX Replay a 3 puntos o menos del libro.
- **APARECE SIN ENTRADA LEGIBLE**: día, dirección y hora por la marca del trader (caja de posición,
  «be», niveles) o por su voz, sin cifra de entrada; antes se busca su aviso de cierre en los
  segundos siguientes a que el trader diga «loss», «win», «B» o «break even».
- **NO APARECE**: la sesión del día se ve en el vídeo y la operación no tiene ni caja, ni marca, ni
  voz a su hora; o el día no se ve.
- **CONTRADICE**: aparece con otra dirección, a otra hora (otro minuto) o con la entrada a más de
  3 puntos.
- **El stop: «no legible» en todas.** El vídeo no sirve para el stop: la grabación no enseña el
  eje de precios y los avisos no lo traen; la caja dispersa (A-48) se le pregunta al trader en
  directo en la sesión 7.
- La hora a ojo: la posición de la caja en el eje se lee al minuto solo si el eje de M1 o de 5 s
  tiene marcas cada pocos minutos; si no, se dice «hora compatible» y la operación no puede ir a
  COINCIDE.
- Las operaciones del vídeo que no están en los casos, aparte, sin resolverlas.
- **F5:** primera vía si las operaciones de los 13 días están todas en COINCIDE o APARECE, ninguna
  CONTRADICE y ninguna NO APARECE; si no, segunda vía, con `dias_con_video` = los días en que se
  cumple.

## Estado
EN CURSO · PARADA 2 (los cuatro comandos de §1.6, para Aleks) y PARADA 3 (el piloto de F3, §3.1)
