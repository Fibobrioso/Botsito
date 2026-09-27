# La tubería de transcripción con cuarentena de la sesión 02

Rama `trabajo/sesion-02`, 2026-09-27, sesión autónoma sobre `main` en `stable/F25-preparar-a21`.
Sin merge, sin tag, sin push. Esta noche NO se transcribe la reunión: la reunión es mañana. El
audio y la transcripción cruda nunca entran en el repositorio. La plantilla de extracción está en
`SESION-02-EXTRACCION.md`, vacía.

## 1. Fase 0 · El arreglo de los predicados puros está CUBIERTO

ADR-0055 §1 dice que el arreglo lo cubre el test de punta a punta de RN-011. Medido: con el árbol
limpio se reinstaló en el árbol de trabajo, sin commit, la versión de un solo disparo de
`toca_colocar_orden_limite` (`engine/zonas.py`: marca `toca_emitido` en la memoria del día y da
NO a partir de la primera evaluación con esquema). Con ella caen **4 de los 9 tests** de
`tests/unit/test_preparar_a21.py`, todos porque RN-011 deja de disparar:

| test | mensaje |
|---|---|
| `test_el_primer_esquema_forma_la_zona_y_rn011_la_liga_en_el_cierre_del_breaker` | `assert {'RN-004', 'RN-011', 'RN-015'} <= {'RN-003', 'RN-004', 'RN-008'}` |
| `test_el_segundo_esquema_y_las_dos_zonas` | `assert ('RN-011' in {'RN-003', 'RN-004', 'RN-008'})` |
| `test_las_dos_lecturas_de_a21_dejan_trazas_distintas_por_el_arnes_real` | `assert ('RN-011' in {'RN-003', 'RN-004', 'RN-008'})` |
| `test_por_el_cableado_la_zona_llega_al_broker_como_una_orden_limite` | `assert {'RN-004', 'RN-011', 'RN-015'} <= {'RN-003', 'RN-004', 'RN-008'}` |

El resto de los tests del motor (`test_estructura_m1`, `test_cableado`, `test_preparar_a35`,
`test_preparar_a44`, `test_huecos_motor`, `test_arnes_motor`, `test_visor`, `test_rutas_windows`)
pasa igual con o sin el arreglo. Después se deshizo la reversión con `git checkout --` sobre ese
fichero: `git status` vacío y `git diff --stat main` vacío.

## 2. Fase 1 · Lo que ya existía

- **La sesión 01 se transcribió** como el vídeo `v6` del corpus, con la tubería de siempre (`botsito
  corpus transcribe`, F04, ADR-0007): manifiesto `knowledge/corpus/transcripciones/tr-v6-large-v3-int8-float16-7718b3f4.yaml`,
  texto en `data/transcripciones/v6/large-v3-int8-float16/` (cruda, corregida, correcciones).
  Motor: faster-whisper 1.2.1, `large-v3`, `int8_float16`, CUDA, `beam_size=5`, `temperature=0`,
  `vad_filter`, `condition_on_previous_text=False`, `word_timestamps`, el vocabulario de
  `knowledge/corpus/glosario_asr.yaml` como `initial_prompt` (96 tokens). No hubo cuarentena: la
  sesión 01 entró al corpus entera.
- **La sesión 02 reutiliza ese ASR y ese corte**, pero NO su pipeline de alto nivel:
  `transcribir_video` escribe el manifiesto dentro del repo, y aquí nada puede entrar. El script
  compone las mismas piezas (`corpus/audio.py`, `corpus/transcripcion.py`,
  `corpus/motor_whisper.py`) y escribe todo fuera.
- **Dispositivo y velocidad:** NVIDIA GeForce GTX 1650 (4 GB), CUDA, con el modelo `large-v3` ya en
  la caché local (no se descarga nada: el script corre con `HF_HUB_OFFLINE=1`). Medido con un
  extracto de 3 minutos del audio de la sesión 01, escrito fuera del repo y sin leer su texto:
  **65 s, factor 0,36 del tiempo real con la carga del modelo incluida; unos 44 minutos para 2
  horas de audio**.
- **La hoja de la sesión 02** (`hoja-sesion-02.docx`, generada por `scripts/hoja_preguntas.py`,
  leída del propio .docx): 23 preguntas en cinco bloques, idénticas a `ORDEN_SESION_02`. Con A-46
  justo después de A-21 son 24; el generador no se toca, porque en la hoja impresa A-46 va a mano.

## 3. Fase 2 y 3 · El script y sus tests

`scripts/transcribir_sesion.py` y `tests/unit/test_transcribir_sesion.py`. Lo medido que decidió el
filtro, en las crudas de v1-v6 (recuentos de palabras, sin leer el texto):

- El ASR escribe «mayo», «septiembre» y «marzo» bien escritos; no aparece ninguna otra grafía.
  «mayo» es prefijo de «mayor» (23 veces) y «mayoría» (13), así que todo va por **palabra
  entera**. Las grafías típicas de ASR (setiembre, marso, maio, febreo, abreviaturas, inglés) se
  filtran igual, por si acaso.
- **«marco» NO se filtra.** Es el verbo del trader («lo marco») y el sustantivo de «marco de
  operativa»; no hay ni un «marco» por «marzo». Los tests lo destaparon: la primera versión
  mandaba «yo lo marco cuando cierra» a cuarentena.
- Una fecha numérica con punto y dos partes casa 190 veces, y son **precios** («1.17»): solo cuentan
  «/», «-» o tres partes con punto. «N del M» y «el mes N» sí van a cuarentena.
- Aplicado a la cruda completa de la sesión 01, el filtro manda a cuarentena **69 de 2146
  segmentos (3,2 %; 3,6 % del habla) en 20 bloques**: 13 por mes, 12 por fecha numérica y 44
  vecinos. Es el orden de magnitud que cabe esperar mañana.
- **Detección de códigos:** con los códigos que se preguntan mañana (ABIERTA o DECIDIDA, del 13 en
  adelante), **cero falsos positivos** en las dos horas y media de la sesión 01. Con los números
  bajos sí hay ruido: «a 1», «a 3», «a 11» casan 17 veces. Por eso solo cuentan los códigos que se
  preguntan, y por eso la forma recomendada es «pregunta A treinta y cinco».

## 4. Fase 4 · La prueba con el audio de Aleks: NO HECHA, el audio no está

La carpeta `C:\Users\USER\Desktop\reunion-a35-a44\sesion-02-audio\` **no existe**, y no hay ningún
`prueba.*` de audio en el Escritorio, Descargas, Música ni Documentos (hay un `prueba.txt` y un
`prueba.png` de otros proyectos). La fase se detiene aquí, como pide el brief. Lo que sí está
probado de punta a punta es la tubería con el extracto de la sesión 01 (§2): extracción, corte,
ASR en GPU, fusión, cuarentena, versión filtrada, registro y `--solo-filtrar`, sin escribir nada
en el repositorio. Faltan por medir con audio de verdad los códigos dichos en voz alta y las
menciones de los meses que Aleks dice haber leído.

## 5. Riesgos y dudas para el consultor

1. **Sin prueba con audio de la reunión**: la detección de códigos dichos en voz alta no se ha
   medido sobre habla real con códigos. La sesión 01 no los usaba.
2. **Falsos positivos del «a N» desnudo**: «llega a 30» abriría la pregunta A-30. Mitigado por la
   lista de códigos válidos y por las unidades («a 30 pips» no cuenta), no eliminado. El registro
   lista cada código con su primer `mm:ss` para revisarlo.
3. **La cuarentena se pasa de frenada a propósito**: «2 de 3 operaciones» o una proporción «1-3»
   van a cuarentena como fecha numérica. Ante la duda, cuarentena; si una respuesta cae dentro, la
   pregunta queda NO RESPONDIDA y se repregunta otro día.
4. **La cruda existe en disco** (`<audio>.cruda-NO-LEER.*`, fuera del repo). Nadie la lee, pero
   existe; si el consultor prefiere que se borre tras filtrar, es una línea en el script.
5. **Un código dicho dentro de un tramo en cuarentena** sigue cambiando de pregunta: el código no
   dice nada del contenido, pero el encabezado lo delata.

## 6. Estado

Rama lista para revisión, NO cerrada.
