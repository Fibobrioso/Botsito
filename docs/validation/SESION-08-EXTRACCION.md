# Sesión 7b con el trader: la extracción por pregunta y por sesión del bloque de días

> **PLANTILLA mientras la rama está EN CURSO**: la tabla final entra con la extracción.

> **Borrador para el consultor. Esta rama NO resuelve nada**: no hay `feedback apply`, ni
> ambigüedades cerradas, ni cambios en la spec, en el motor, en los casos, en las cifras, en
> `SESION_EN_CURSO` ni en la hoja de ruta (R4.3 sigue ABIERTA); de `PREGUNTAS-7B.md` solo cambia el
> recuadro de la hoja usada. Cada «resuelve» de abajo es una propuesta sobre lo que dijo el trader;
> el destino de cada respuesta lo decide el consultor en la rama de activación de la 7b (encargo del
> 2026-11-21, `docs/encargos/trabajo-sesion-08.md`).

Rama `trabajo/sesion-08`, abierta el 2026-11-21 desde `main` en `5ae7c482` (commit de estado sobre
el merge `c6d5a9c2`, tag `stable/F39i-guardia-enlaces`). Tramo R4 de la hoja de ruta (R4.3, NA:F,
paso (2)). Skill `ingerir-sesion`, de principio a fin, y ADR-0093 §2. Plantilla:
`SESION-07-EXTRACCION.md`. Tag de cierre previsto: `stable/F39j-sesion-08` (no existe ni en local
ni en origin: `git tag -l 'stable/F39j*'` y `git ls-remote --tags origin 'stable/F39j*'` vacíos).

## Base comprobada al abrir

- `git fetch --prune`; en `main`, `git status --short` vacío.
- `git rev-parse main origin/main` da dos veces `5ae7c482f6dd4ef00f333dbc307ac23466f3dee0`.
- El último `- Tag: ` de `docs/state/HISTORIA.md` es `stable/F39i-guardia-enlaces`;
  `git rev-parse "stable/F39i-guardia-enlaces^{commit}"` = `git rev-parse main^1` =
  `c6d5a9c2cf39c6e1922f7721aa6b7f0448437ee5`; `git ls-remote --tags origin` da
  `9fb6345d… refs/tags/stable/F39i-guardia-enlaces` (el objeto del tag anotado) y su `^{}`,
  `c6d5a9c2…`. Es también el primero de `git tag -l 'stable/*' --sort=-creatordate`.
- CI de `main` sobre su HEAD, una consulta suelta de `gh run view 44871267577`: `completed`,
  `success`, `headSha` `5ae7c482f6dd4ef00f333dbc307ac23466f3dee0`, rama `main`.
- `git branch -a` solo da `main` y `origin/main`; `git ls-remote --heads origin` solo da
  `refs/heads/main` (ningún `fix/*`).
- `scripts/transcribir_sesion.py` de `main`: `"08": {` en la línea 260 de
  `CODIGOS_DE_SESION_TEXTO`, con 7 textos, S-1 a S-7; `"08": ORDEN_SESION_08` en `HOJAS` (línea
  278); `SESION_EN_CURSO = "08"` (línea 283).
- `PROJECT_STATE.md`: 24.576 bytes en `main` y 24.614 tras abrir (`wc -c`), por debajo de 24.900.
- **El corpus no es un enlace de unión**: `fsutil reparsepoint query corpus` da «Error 4390: El
  archivo o directorio no es un punto de análisis repetido» (exit 1): es una carpeta normal.

## Decisiones de proceso de la rama

- Al comprobar qué vídeos del primer nivel faltan en `fuentes.yaml`, la guardia negó (solo lectura)
  un bucle `for f in ...; do b=$(basename "$f"); grep -qF "$b" ...` («`basename` recibe un argumento
  que se construye al ejecutarse»); seguí su forma (guion con Write, ejecutado en otra llamada), y
  ese guion lo negó también («el codigo nombra la carpeta C:\Users\USER\Desktop\Bot v3, que contiene
  material protegido»); seguí la forma que propone su segundo mensaje, «rutas LITERALES»: un solo
  `grep -o -F -e "<nombre>" ...` con los 17 nombres del listado escritos tal cual sobre
  `knowledge/corpus/fuentes.yaml` (`docs/runbooks/DECISIONES-DE-PROCESO.md`).
- La guardia negó las dos líneas de «Antes», paso 1, en un solo comando («antes, en el mismo
  comando, va `uv run python -c ...`»); seguí su forma: una llamada por ejecutable.

## 0. Lo primero

### 0.1 Los días, antes de registrar

La línea de `SESION-DE-PREGUNTAS.md` («Antes», paso 1), que imprime solo `True` o `False`:
- `2026-11-20`: `False`.
- `2026-11-21`: `False`.

### 0.2 Los vídeos

Son los dos únicos vídeos del primer nivel de `corpus/Estrategia del trader/` que no estaban en
`fuentes.yaml` (los otros 15 vídeos de ese nivel salen una vez cada uno):
- `Grabación de pantalla 2026-11-20 182155.mp4`, 4.878.875.346 bytes (v20, el primer día);
- `Grabación de pantalla 2026-11-21 104411.mp4`, 8.440.884.009 bytes (v21, el segundo día).

El id de la sesión es `2026-11-20-sesion-08` (el del primer día; encargo, OBJETIVO).

### 0.3 Lo que contestó Aleks en el terminal (2026-11-21), antes del registro

Las preguntas del encargo («ENTRADAS», la última), con sus palabras resumidas; Aleks pidió después
que se compruebe TODO en la filtrada, «no me recuerdo bien del todo». Lo que la filtrada confirma o
no, en §3 y §4.
1. **Los días no se comprobaron antes de grabar.** **Desviación del paso 1, declarada** (y en
   `HOLDOUT-EXPOSICIONES.md`, 2026-11-21); se comprobaron hoy, después (0.1). Precedente: la 7a
   (`SESION-07-EXTRACCION.md` §0.1).
2. Las frases de «Para confirmar al final» se leyeron «de la mayoría».
3. Los códigos de voz, «pregunta ese uno» … «fin de pregunta», «en la mayoría». **Desviación nueva,
   declarada**: Aleks no estuvo en toda la reunión (exámenes) y **el trader dirigió las preguntas**
   («dejé al trader al mando»). ADR-0093 §2 y `PREGUNTAS-7B.md` §1 dan a Aleks el papel de hacer las
   preguntas y la de cada corrección; quién leyó qué se comprueba en la filtrada.
4. En el bloque técnico el trader abrió su gráfico, «con los días permitidos entre 1 al 17 de
   julio». Si lo dijo en voz alta no lo contestó: lo decide la filtrada, con la regla de la PARADA
   condicional del encargo.
5. El replay de cada sesión **no** se abrió antes de compartir pantalla: «todo ha sido directo con
   él, no ha "preverificado" nada». **Desviación del paso 2 de `PREGUNTAS-7B.md` §1, declarada.**
6. El de la sesión 2, «todo limpio».
7. La fecha: «Todo lo que ha trazado se ve en vivo […] son con las fechas acordadas». Si la dijo al
   abrir el gráfico y otra vez con el replay abierto, en la filtrada, sesión por sesión.
8. «En algunos casos sí y en otros lo fue comparando a medida que avanzaba el tiempo»: en unas
   sesiones operó entera la sesión antes de ver las láminas y en otras no. **Desviación del paso 4
   de `PREGUNTAS-7B.md` §1, declarada**; cuáles, en la filtrada.

Quién enseñaba las láminas cuando Aleks no estaba lo pregunté y queda por comprobar en la filtrada
(el encargo dice «Las láminas las enseñé yo»).

## 1. El registro y el audio

### 1.1 Metadatos y audio

Con las formas exactas del paso 2 de la skill (`ffprobe -v error -show_format -show_streams`,
`silencedetect=noise=-50dB:d=30`, `volumedetect`), el 2026-11-21:

| Vídeo | Duración | Imagen | Audio | volumedetect (media / máximo) | Silencios de 30 s o más |
|---|---|---|---|---|---|
| v20 | 1:13:04 (4384,9 s) | 1920x1080, 30 fps | AAC estéreo, 48 kHz | -24,2 dB / -0,2 dB | 6 |
| v21 | 2:06:25 (7585,5 s) | 1920x1080, 30 fps | AAC estéreo, 48 kHz | -24,3 dB / -0,1 dB | 9 |

Los cortes, en `h:mm:ss` (inicio hacia abajo y fin hacia arriba, como en v18 y v19), cada uno en
`tramos_no_citables.yaml` con motivo «SIN AUDIO»:
- **v20**: 0:16:18-0:25:01 (522,8 s: casi nueve minutos), 0:25:01-0:25:34, 0:40:19-0:41:44,
  0:49:36-0:52:05, 1:04:55-1:06:48 y 1:12:28-1:13:05 (hasta el final).
- **v21**: 0:48:45-0:49:39, 1:20:21-1:21:00, 1:27:44-1:28:27, 1:29:43-1:30:30, 1:31:24-1:32:11,
  1:33:37-1:34:57, 1:52:59-1:54:13, 2:03:41-2:04:47 y 2:04:47-2:05:30.

La causa de cada silencio no la sabe la sesión (Aleks no estuvo en toda la reunión); va así en su
`motivo`. El audio de cada vídeo, extraído con la forma de la skill a
`C:\Users\USER\Desktop\sesion-08-audio\sesion-08-v20.wav` y `sesion-08-v21.wav` (mono, 16 kHz),
fuera del repositorio. No hay audio de respaldo.

### 1.2 Los tests rotos a propósito

Con v20 y v21 ya en `fuentes.yaml` y ANTES de añadirlos a `SESIONES_EN_CUARENTENA`:
`uv run pytest tests/unit/test_cuarentena.py "tests/unit/test_guardia_claude.py::test_la_guardia_y_el_modulo_dicen_la_misma_cuarentena" "tests/unit/test_guardia_claude.py::test_contra_el_repo_real_ve_lo_mismo_que_el_codigo" --tb=no -p no:randomly`:

```
FAILED tests/unit/test_cuarentena.py::test_la_lista_cuadra_con_fuentes - Asse...
FAILED tests/unit/test_guardia_claude.py::test_la_guardia_y_el_modulo_dicen_la_misma_cuarentena
FAILED tests/unit/test_guardia_claude.py::test_contra_el_repo_real_ve_lo_mismo_que_el_codigo
3 failed, 39 passed in 7.16s
```

(el primero, «'v20: es una sesion (drive_id null) y no esta en SESIONES_EN_CUARENTENA ni en
EXCEPCIONES'» y lo mismo de v21; los otros dos, «Extra items in the left set: 'v20' 'v21'»).
Después: v20 y v21 en `SESIONES_EN_CUARENTENA` (`src/botsito/corpus/cuarentena.py`), en el
conjunto literal de `test_contra_el_repo_real_ve_lo_mismo_que_el_codigo` (el sintético de
`{"v7", "v9"}` no se toca) y en el dict `reales` de `test_la_comprobacion_de_la_lista_no_es_decorativa`, cuya sonda
«sesión sin listar» pasa de v20 a v22. Los mismos, más `tests/unit/test_inventario.py`
(`range(1, 22)`), tras `corpus inventory`: `55 passed in 10.85s`.

### 1.3 Inventario y hashes

`uv run botsito corpus inventory`: «OK: manifiesto escrito · […] video_original: 21 ficheros,
98,507,386,788 bytes»; en `manifest.yaml` solo entran v20 (`sha256` `b63eedfc…`) y v21
(`59a972a4…`) y cambia el total de `video_original` (de 19 a 21 ficheros). `uv run botsito corpus check
--hashes`: «OK: el corpus coincide con el manifiesto (hashes)».

Sellado y commiteado en `7fcc7990` (PICO DE MEMORIA del sello: 322 MiB en `test`; el de la apertura,
`5fc0f9fd`, 318 MiB).

## 2. Transcripción y cuarentena

### 2.1 v20: transcripción, cuarentena y puerta del ASR

Con el «listo» de Aleks antes de cada una (programas cerrados), una cada vez y ninguna junto a un
`make check`.

- **Transcripción del corpus**: `uv run botsito corpus transcribe --video v20` →
  `tr-v20-large-v3-int8-float16-2d93201d`, **685 segmentos** (sin medir su pico de memoria).
  `corpus transcript check`: `OK: 27 transcripciones coherentes con el disco y el glosario`.
- **El guion de `main`** (`git diff --quiet main -- scripts/transcribir_sesion.py`: exit 0,
  idéntico), con un segundo «listo»: `--audio C:/Users/USER/Desktop/sesion-08-audio/sesion-08-v20.wav
  --sesion 08 --video v20`, medido con `scripts/pico_memoria.py ejecutar`: PICO DE MEMORIA **5531
  MiB** (el mayor, 5480 MiB). El registro (`sesion-08-v20.registro.txt`, fuera del repositorio) dice:
  - hoja: la de la sesión 08; tramos no citables del vídeo: 6 (los silencios);
  - audio comprobado: el sha256 de su WAV (`2c7f326258cb…`) es el de la transcripción del corpus de v20;
  - ASR de 667,7 s (factor 0,15), en cuda; **685 segmentos**, los mismos que la del corpus;
  - **segmentos en cuarentena: 0 en 0 bloques**; tapados solo por meses 0, solo por tramos 4, por
    ambos 0; bloques `[NO CITABLE]`: 3;
  - códigos detectados: S-3 38:05 y S-4 49:25; sin código detectado, S-1, S-2, S-5, S-6 y S-7 (cómo
    se localizan, §3).
- **Ningún bloque de cuarentena**, así que ningún tramo de cuarentena que añadir a
  `tramos_no_citables.yaml` para v20: el commit propio de v20 lleva su manifiesto de transcripción,
  este apartado y su fila de `HOLDOUT-EXPOSICIONES.md`.
- **La puerta del ASR de los seis silencios**, por los bloques `[NO CITABLE]` (marca = principio del
  primer segmento y fin del último, al segundo; un segmento que solapa un tramo sale tapado, así que
  uno con `t1` dentro de un corte saldría en un bloque):
  - `[41:43–42:33]`: empieza en el último segundo del silencio 0:40:19–0:41:43,6 (2503,63 s) y acaba
    en 42:33, fuera. Pasa.
  - `[52:04–52:34]`: empieza en el último segundo del silencio 0:49:36–0:52:04,6 (3124,60 s) y acaba
    en 52:34, fuera. Pasa.
  - `[66:47–66:48]`: un segmento de un segundo que empieza al final del silencio 1:04:55–1:06:47,6
    (4007,60 s); su `t1` cae en el segundo 66:48, después del final del silencio. Pasa.
  - Los silencios 0:16:18–0:25:01 y 0:25:01–0:25:34 y el del final, 1:12:28–1:13:05: ningún segmento
    los toca (ningún bloque; la línea siguiente al primero es `[25:35]`). Pasa.
  Los cuatro segmentos tapados no se citan.

### 2.2 v20: el barrido, antes de leer

Con `scripts/barrido_dias.py` de `main`, antes de leer una sola línea de la filtrada de v20:
- **Del 1 al 31: 49 líneas** con un entero suelto: números de pregunta, de dibujo y de esquema, el
  1 de la caja, horas y temporalidades («[N] horas», «m [N]»), cantidades y recuentos. Una sola
  lleva mes: `[66:50]`, «el dia dice [N] de julio», en S-7.
- **Rango por defecto (18 a 31): 0 líneas.** Así que el día de `[66:50]` cae del 1 al 17 de julio,
  de construcción.

**Sin PARADA por el barrido.** En sus 49 líneas no sale ningún otro mes; lo que se diga de un
mes sin número lo ve la lectura (§3).

Sellado y commiteado en `66ea16bd` (PICO DE MEMORIA del sello: 321 MiB en `test`).

### 2.3 v20: fotogramas

`uv run botsito corpus frames extract --video v20` → `fr-v20-c29e6481`, «4385 fotogramas, 0
extra», fuera de git en `data/fotogramas/v20/png-1fps/`. `uv run botsito corpus frames check`:
«OK: 20 extracciones coherentes con el disco; 3 obligatorios presentes». **Ningún fotograma de
v20 se ha abierto**: los únicos tramos con gráfico real en que la voz dice el día son los de S-7
(10 de julio), y lo que se cita de ellos no pide imagen.

Sellado y commiteado, con los tramos de precaución de v20 y el §3, en `ca547e77` (PICO DE MEMORIA
del sello: 320 MiB en `test`).

### 2.4 v21: transcripción, cuarentena, puerta del ASR y barrido

Con un «listo» de Aleks antes de cada una, solas y sin ningún `make check` a la vez.

- **Transcripción del corpus**: `uv run botsito corpus transcribe --video v21` (medida con
  `scripts/pico_memoria.py ejecutar`) → `tr-v21-large-v3-int8-float16-9a52aac1`, **1140 segmentos**;
  PICO DE MEMORIA **5531 MiB** (el mayor, 5479 MiB). `corpus transcript check`: `OK: 28
  transcripciones coherentes con el disco y el glosario`.
- **El guion de `main`** (idéntico) con `--audio C:/Users/USER/Desktop/sesion-08-audio/sesion-08-v21.wav
  --sesion 08 --video v21`; PICO DE MEMORIA **5531 MiB** (el mayor, 5480 MiB). El registro dice: hoja
  de la sesión 08; tramos no citables del vídeo: 9 (los silencios); el sha256 del WAV (`59d09925237d…`)
  es el de la transcripción del corpus; ASR de 1140,9 s (factor 0,15); **1140 segmentos**; **9 en
  cuarentena en 3 bloques** (solo por meses 9, solo por tramos 5, ambos 0; bloques `[NO CITABLE]`: 5;
  motivos «fecha numérica» 3 y «vecino» 6); **ningún código detectado**, como se esperaba (v21 no
  lleva preguntas técnicas).
- **La puerta del ASR de los nueve silencios**, por los bloques `[NO CITABLE]`:
  - `[80:07–81:53]` cubre el silencio 1:20:21–1:21:00 y acaba fuera. Pasa.
  - `[87:34–89:15]` cubre el silencio 1:27:44–1:28:27 y acaba fuera (antes del siguiente). Pasa.
  - `[90:29–91:11]`: empieza en el último segundo del silencio 1:29:43–1:30:29,9 (5429,94 s) y acaba en
    91:11, fuera. Pasa.
  - `[93:12–95:28]` cubre el silencio 1:33:37–1:34:57 y acaba fuera. Pasa.
  - `[112:47–114:14]` cubre el silencio 1:52:59–1:54:12,9 (6852,88 s) y acaba en 114:14, fuera. Pasa.
  - Los silencios 0:48:45–0:49:39, 1:31:24–1:32:11, 2:03:41–2:04:47 y 2:04:47–2:05:30: ningún segmento
    (ningún bloque). Pasa.
- **Los tres bloques de cuarentena, a `tramos_no_citables.yaml`**, sin contenido y en el commit propio
  de v21, con el fin de cada uno más un segundo: **0:03:54–0:04:02**, **0:36:43–0:36:52** y
  **1:12:12–1:13:32**. El segundo de margen toca la primera línea visible tras los dos primeros
  (`[04:01]` y `[36:51]`), que por eso tampoco se citan; tras el tercero, la siguiente es `[73:33]`.
- **El barrido**, antes de leer:
  - del 1 al 31, **160 líneas**;
  - **con el rango por defecto (18 a 31), 22 líneas**. Nueve llevan mes: «de abril» en `[71:35]`,
    `[73:33]` y `[87:23]`, y «de enero» en `[87:23]`, `[104:41]`, `[112:11]`, `[112:19]`, `[123:16]`,
    `[125:32]` y `[125:57]`. Hay además «fecha [N]» sin mes en `[00:24]`. Los días del bloque son el
    24 y el 27 de abril y el 19 y el 21 de enero, todos en ese rango y todos de construcción (enero del
    2 al 30 y abril del 1 al 29).
  - Para ver si alguna es un día fuera de construcción, **con `--desde 30 --hasta 31`, 1 línea**,
    `[63:46]` «2 y [N].», sin mes, que no es un día. **Con `--desde 1 --hasta 1`**, ninguna línea con
    el 1 nombra un mes. Esa pasada deja ver los demás números de sus líneas, y lo que dejó ver son
    días de construcción («27 de abril finalizado continuo con 19 19 de», `[87:23]`).
  - **Sin PARADA por el barrido**: ningún día fuera de construcción del mes que nombra.

## 3. El bloque técnico (v20), por pregunta

La filtrada de v20 leída entera, fuera de sus bloques tapados (fila de `HOLDOUT-EXPOSICIONES.md` del
2026-11-21, declarada antes). Cada literal es de la FILTRADA, con su `mm:ss`; ninguno cae en un tramo
de `tramos_no_citables.yaml` (§3.0). Cada «resuelve» es una propuesta: lo decide el consultor.

### 3.0 Lo que la filtrada dice de la sesión, contra lo que contestó Aleks

- **El trader dirigió las preguntas, y Aleks no estuvo todo el rato** (respuesta 3): el trader lee
  cada pregunta del PDF en voz, con «Lo que nos has dicho» y «Lo que todavía no sabemos» (S-1 en
  `[00:07]`, S-2 en `[14:57]`, S-3 en `[38:12]`), y lee también «Alex te dice cuál» (`[64:32]`) de S-7.
  Pregunta «¿Estás allí?» en `[16:02]` y en `[64:36]`. Antes de S-4 dice «me voy a dar un brillo un
  minuto» (`[49:28]`). En S-7 hay dos voces (`[67:03]`–`[67:14]`).
- **El silencio de casi nueve minutos (0:16:18–0:25:01)**: justo antes, «Bro ahora vengo ¿vale?»
  (`[16:00]`), y después «Vale, volví.» (`[25:35]`). Fue una pausa en mitad de S-2.
- **Los códigos de voz** (respuesta 3, «en la mayoría»): no son exactamente los de la hoja. S-1 se abre
  con «S1, la mecha de un minuto…» (`[00:07]`) y se cierra con «continúo verdad bro» (`[14:49]`). S-2
  se abre con «S2, tus zonas de control» (`[14:57]`) y se cierra con «ese 2 terminado, pregunta ese 3»
  (`[38:05]`). S-3 se cierra con «pregunta S3 finalizada» (`[49:23]`). S-4 se abre con «pregunta S4»
  (`[49:25]`) y se cierra con «ese 4 finalizado» (`[58:37]`). S-5 se abre con «ese 5» (`[58:40]`) y se
  cierra con «ese 5 finalizado» (`[61:35]`). S-6 se abre en esa misma línea y se cierra con «S6
  finalizado» (`[64:07]`–`[64:12]`). S-7 se abre con «S7» (`[64:13]`) y se cierra con «ese 7, pues,
  cerrado» (`[72:21]`). Por eso el guion solo detectó S-3 y S-4: localizadas a mano, todas en el orden
  de la hoja (respuesta b), S-1 a S-6 y S-7 al final.
- **«Para confirmar al final»** (respuesta 2, «de la mayoría»): **se leyeron las seis**, cada una al
  final de su pregunta: S-1 `[13:25]`, S-2 `[37:39]`, S-3 `[48:33]`, S-4 `[57:52]`, S-5 `[61:23]` (a
  medias: «cuando la roja» y «lo descarto», `[61:35]`) y S-6 `[63:44]`. S-7 no lleva.
- **El gráfico real** (respuesta 4): el trader pasa a un gráfico real en S-1 («lo vamos a ir al el
  mercado real», `[03:27]`), en S-2 (`[28:00]` y `[32:09]`) y en S-3 («evaluar en nuestro gráfico»,
  `[39:21]`, y «lo voy a mostrar en el gráfico», `[48:40]`). **En ninguno dice el día en voz.**
  Según Aleks eran días de julio del 1 al 17, pero la voz no lo confirma. Por la regla de la PARADA
  condicional, cada uno es un tramo no citable, y la pregunta se queda con lo citable de fuera. Son
  cinco tramos: **0:03:27–0:14:49, 0:28:00–0:30:14, 0:32:09–0:37:39, 0:39:21–0:44:06 y
  0:48:40–0:49:18**. Sus límites salen de la voz y van por precaución hacia afuera (sin abrir
  fotogramas: ninguno antes de que la voz sitúe el tramo en un día). En S-1 nombra además el desenlace
  de una operación de ese gráfico; no se copia aquí.
- **El vídeo de mapeo**: el trader lo nombra en S-1 y dos veces en S-2, siempre dentro de esos tramos.
  Hay una mención más del «mapeo de estructura», en `[15:46]`, mientras lee «Lo que nos has dicho» de
  S-2; va también a `tramos_no_citables.yaml` (**0:15:46–0:15:51**), porque no se puede saber si
  habla del vídeo.
- **S-7**: el trader abre el replay del **10 de julio**. El día se dice en voz en `[66:50]` («El día
  dice 10 de julio.») y es de construcción (`casos_ocultos`: `False`). Por la misma regla, ese tramo
  (`[66:48]`–`[69:55]`) es citable. Sus operaciones y cómo acabaron no se escriben aquí (encargo, S-7).
- **Los esquemas**: S-4, S-5 y S-6 se contestan sobre los esquemas del PDF («Dibujo 1»,
  «Dibujo 2», `[52:59]`, `[54:51]`; «me gusta como lo [has] trazado», `[63:37]`). En S-5, «voy a usar
  este» (`[60:15]`) no dice qué; no hay palabra de gráfico ni de mercado.

### 3.1 S-1 (A-35, la única bloqueante): la mecha de un minuto que pasa tu alto de M15 y vuelve

Vídeo v20, `[00:07]`–`[14:43]`. Lo citable está en `[00:07]`–`[03:27]`; de `[03:27]` a `[14:49]` el
trader trabaja en su gráfico real, y ese tramo no es citable.

- **Lo que dice, sobre el esquema:** «Tiene que cerrar, al menos cuando hay la toma de liquidez de
  M15, la regla es que rompa con cuerpo y cierre con cuerpo por arriba.» (`[01:38]`), «Si no, esto no
  se llegaría a considerar, o sea, se llegaría a considerar liquidez de M1.» (`[01:45]`); «Nosotros no
  lo tomaríamos en cuenta porque tiene que romper con un cuerpo cuando es la toma de liquidez de M15
  para poderlo validar, recién validar esto de aquí.» (`[02:37]`); «Entonces, si lo hace con Mecha,
  simplemente yo esperaría y trazaría esto como una zona lineal de liquidez de M1 y esperaría que el
  precio rompa, ¿vale?» (`[02:51]`).
- **La opción (a, b u «otra»)**: la dice en `[10:44]`, dentro del tramo del gráfico real: **no
  citable**. Lo citable no elige entre A y B. Dice que la mecha de una M1 que pasa el alto de M15 no
  es una toma de liquidez de M15: la trata como liquidez de M1 y espera la ruptura con cuerpo.
  **No dice dónde queda su alto de M15.**
- **Varias velas seguidas**: contestada en `[10:49]`, dentro del tramo: no citable.
- **El bajo, al revés**: contestada en `[13:13]`, dentro del tramo: no citable.
- **«Para confirmar al final»**: se leyó (`[13:25]`), dentro del tramo: no citable.
- **En qué valor de `liquidez_m15_mecha_que_vuelve` cae** (`parametros.yaml:595`, opciones
  `no_mueve`, `solo_la_contraria` y `cualquier_mecha`; hoy `solo_la_contraria`, DEFAULT_AMBIGUOUS).
  Según el «Para Aleks» de `PREGUNTAS-7B.md`, (a) → `solo_la_contraria`, (b) → `cualquier_mecha` y
  «otra» → A-35 sigue abierta. **Lo citable no cae en ninguno de forma literal: lo decide Aleks.** Lo
  que sí dice toca otra cosa, qué cuenta como toma de M15: ruptura y cierre con cuerpo
  (`liquidez_m15_criterio_toma`, ADR-0062). Que la mecha nueva no sea una toma de M15 no dice si
  mueve el nivel.
- **Propuesta: no resuelve** A-35 con lo citable. Regla general: sí, para la toma («la regla es»).
  «creo»: no, en lo citable. Alto y bajo: lo citable habla del alto; lo del bajo cae en el tramo.

### 3.2 S-2 (RN-009 y A-13): tus zonas de control y el momento del break even

Vídeo v20, `[14:57]`–`[38:04]`, con la pausa 0:16:18–0:25:34 en medio. Lo citable está en
`[14:57]`–`[16:02]` (la lectura, menos `[15:46]`–`[15:51]`), `[25:35]`–`[27:54]`,
`[30:14]`–`[32:07]` y `[37:39]`–`[38:04]`. Los dos gráficos reales (0:28:00–0:30:14 y
0:32:09–0:37:39) no son citables.

**Pregunta 1, las zonas de control (RN-009):**
- Sobre el dibujo 1: «vale, la A» (`[26:14]`), «si sería una zona» (`[26:18]`), «de control válida,
  la B también, la C también» (`[26:20]`), «y la D» (`[26:22]`), «punto breaker» (`[26:24]`).
- Al leer la pregunta: «La C también valdría como una zona de control.» (`[30:23]`), «Se forman antes
  de romper el punto y pueden formarse también después de romperlo.» (`[30:28]`). Después: «y antes
  que genere rompimiento el posible punto breaker, pues no solo nos deja una zona de control y rompe,
  no nos genera otras más» (`[30:49]`), «si hay más de uno, simplemente se invalida este posible punto
  breaker y no se opera, vale, esperaríamos a que el precio rompiera por debajo» (`[30:58]`).
- La opción: «pues la respuesta sería» (`[31:29]`), «la letra T» (`[31:30]`). Es una transcripción
  dudosa, y no se abre ningún fotograma para ver la letra (§3.0). Con `[30:28]`, lo dicho es la (b),
  «también después de romperlo».
- **Contradicción, dicha sin decidir (R4.6):** en `[26:20]` y `[30:23]` A, B y C le valen como zonas
  de control. En `[30:58]`, «si hay más de uno», se invalida el punto, que es lo fijado en A-20
  (RESUELTA: una sola zona; con dos se descarta, `zonas_control_max_por_esquema` = 1). En la 7a dijo
  «solo a y b» (`ev-v18-002115-bf40ec0b`). A-20 no se vuelve a preguntar (ADR-0093 §1): va como
  contradicción con lo fijado. Lo que dice de D (formado tras la ruptura) es solo «y la D», «punto
  breaker»: no dice si es zona de control.
- **«El bajo que deja la propia toma, ¿cuenta como zona de control?»** (fila propia): lo lee en
  `[37:06]` y lo contesta en `[37:19]`–`[37:37]`, dentro del tramo 0:32:09–0:37:39, porque señala
  algo en pantalla que puede ser el gráfico real. **No citable: no resuelve.**
- **Propuesta: en parte** (b) para «antes o después», con la contradicción de cuántas zonas.

**Pregunta 2, el margen del break even (A-13):**
- Sobre el dibujo 2: «si está demasiado extendido el precio, vale, no llega, o sea, a estar en medio
  de» (`[26:30]`), «de nuestra zona de entrada, bastaría con cuerpo, o sea, que rompa con poco cuerpo y
  cierre,» (`[27:00]`), «para poder nosotros, pues, poner en break-even la entrada, o inclusive con
  mecha.» (`[27:07]`); «aquí entonces está en medio cuando está en medio y tendría que romper con
  cuerpo y cerrar con cuerpo» (`[27:37]`), «rompimiento aquí ya te genera la zona de control basaría
  sólo con una mecha porque hay una» (`[27:49]`).
- La opción: «y la respuesta sería C, otra cual» (`[31:51]`), «porque ya dije, o sea, la diferencia»
  (`[31:55]`), «de las zonas de control» (`[31:57]`), «para puesta en break-even, enfocado»
  (`[32:00]`).
- **Basta cerrar por encima o pide margen**: «otra». **Depende de la distancia** entre la zona de
  control y el nivel de entrada. Si la zona queda «en medio» del nivel de entrada, rompe y cierra con
  cuerpo. Si el precio está «demasiado extendido», basta con poco cuerpo, «o inclusive con mecha».
  **Cifra: ninguna. Unidad: ninguna. Siempre el mismo: no** (depende del escenario).
- «Para confirmar al final» (`[37:39]`): «Bueno, mi zona de control, pues, es la condicional para
  poder pasar a break even.» (`[37:49]`), «La vela tiene que estar por encima del alto de la zona de
  control.» (`[37:53]`), «Eso, pues, específicamente es solo en casos, pues, para poder poner en break
  even.» (`[37:57]`).
- **Ejemplo, en el replay del 10 de julio (S-7, citable)**: «para poder poner un break even se va a
  dar después de la entrada entonces aquí» (`[68:49]`), «ocurre el retroceso después de haber activado
  la entrada» (`[68:52]`). Es lo que la 7a dejó en duda (la zona del break even se forma después de la
  entrada: `ev-v19-011640-1fdc33a7`).
- **Propuesta: en parte**: no hay margen fijo. Con «depende», A-13 sigue abierta (el «Para Aleks» de
  `PREGUNTAS-7B.md`). Regla general: sí, con su condición. «creo»: no. Compra y venta: lo dice para
  la compra del dibujo 2 y no habla de la venta.

### 3.3 S-3 (A-48): dónde pones el 0 de tu caja

Vídeo v20, `[38:05]`–`[49:24]`. Lo citable está en `[38:05]`–`[39:21]`, `[44:06]`–`[48:40]` y
`[49:18]`–`[49:24]`. Los gráficos reales (0:39:21–0:44:06 y 0:48:40–0:49:18) no son citables.

- Sobre el esquema («vale estamos estamos aquí explicando el lo que sería este gráfico este esquema
  inventado vale», `[44:46]`): «pero ojo el punto 1 está bien planteado pero aquí hay una rata que
  sería» (`[46:10]`), «el 0 aquí en el a no iría vale tampoco iría pues aquí tampoco iría en la vela
  pues de la toma y no» (`[46:17]`), «quería a este nivel de aquí pero cambio iría a este nivel aquí es
  la vela pues queda retrocedido» (`[46:28]`), … «esta zona de control» (`[46:45]`), «su punto más
  bajo sería este de aquí» (`[46:48]`), «entonces allí iría el 0» (`[46:51]`).
- La opción: «La respuesta sería C, en otro sitio, ¿cuál? Con lo explicado, pues, anteriormente,
  ¿vale?» (`[47:50]`).
- **Dónde va el 0: «otra»**: ni en A (el último pivote de M1) ni en B (la vela de la toma). Va en el
  punto más bajo de la zona de control que se forma tras el retroceso y valida la ruptura (en la
  venta del esquema), que es su punto de entrada: «El cero, por lo general, va en una compra, el punto
  de entrada, ¿vale?» (`[48:13]`), «En el posible punto breaker y al revés, pues sería también al nivel
  de entrada, ¿vale?» (`[48:20]`).
- **La compra, por separado**: «Ahora, para precisar, ¿lo haces igual en una compra? Exacto, lo hago
  igual en una compra.» (`[48:03]`).
- «Para confirmar al final»: «Ahora, para confirmar al final, mi cero es, tu cero es tu punto de
  entrada.» (`[48:33]`).
- **Propuesta: en parte.** Elige «otra», el punto más bajo de la zona de control que valida, que
  llama su punto de entrada. Si eso es `ultimo_pivote_m1` o `referencia_de_la_toma`
  (`parametros.yaml:702`) lo decide el consultor: el trader descarta A y B tal como están dibujados.
  Regla general: sí («por lo general»). «creo»: no en la respuesta. Compra y venta: sí.

### 3.4 S-4 (A-58): tu rango de 4 horas después de una ruptura

Vídeo v20, `[49:25]`–`[58:37]`, con la pausa 0:49:36–0:52:05. Todo sobre los dos dibujos del PDF
(«Dibujo 1, ¿qué me sirve con explicarlo en este dibujo?», `[52:59]`).

- **Dibujo 1** (cierra de su color): «pero la actualización de rango» (`[54:29]`), «como sería,
  nuestro rango pasa» (`[54:31]`), «de aquí» (`[54:33]`), «a aquí, ese sería» (`[54:35]`), «nuestro
  rango a trabajar» (`[54:38]`), «para nosotros vale o sea esto pasaría a este bajo y esto esté alto
  aquí vale ahora» (`[54:40]`). Antes: «y como digo, no sé» (`[54:23]`), «si es indiferente de saber
  este rango con mecha por encima» (`[54:25]`), «o con cuerpo, vale» (`[54:27]`). Las palabras no
  dicen de qué vela son «este bajo» y «este alto», y no se abre ningún fotograma para verlo.
- **Dibujo 2** (cierra del color contrario): «es roto por encima pero los tierra una vela de color
  contrario entonces nosotros lo que» (`[55:20]`), «que haríamos sería seguir buscando pues operativas
  alcistas vale nuestro rango pues estaría definido» (`[55:28]`), «en el mismo en el mismo nivel vale
  no lo actualizamos sino que lo no que lo definimos» (`[55:35]`), «el mismo nivel lo dejamos hasta
  que puede romper con una vela pues de acorde a esto» (`[55:41]`). Después: «no voy a actualizar a
  esa vela verde» (`[56:05]`), «en mi rango, sino que respeto» (`[56:07]`), «respeto el rango»
  (`[56:19]`).
- La opción, de los dos: «vale en el dibujo 1 del alto bajo el alto al bajo de esa vela a esas
  preguntas la respuesta sería la» (`[56:53]`), «c otra cual con lo explicado pues anteriormente y
  para el número 2 también sería hacer otra cual con» (`[57:12]`). Formalmente, «otra» en los dos. Lo
  explicado en el dibujo 2 es lo que la (a) dice: «sigue siendo el mismo».
- **La ruptura por abajo**: «la hace es igual cuando la ruptura» (`[57:42]`), «es por abajo o al
  revés» (`[57:44]`), «yo» (`[57:47]`), «considero que» (`[57:48]`), «o sea, la hace su color»
  (`[57:49]`), «es igual» (`[57:50]`).
- **«¿Marcas tu rango siempre en el gráfico de 4 horas, o a veces en otro?»** (fila propia): «siempre
  marco mi rango» (`[57:23]`), «que es mi temporalidad mayor» (`[57:33]`), «está definida como mi
  temporalidad mayor» (`[57:35]`), «H4» (`[57:39]`). Siempre en H4.
- «Para confirmar al final»: «mi nuevo rango es pues la continuación y cierra el color contrario mi
  rango es pues» (`[58:07]`), «dependiendo o sea basándonos en estos ejemplos ambos serían de
  continuación vale porque para» (`[58:15]`), «yo poder cambiar mi rango a bajista tendría que haber
  un rompimiento pues en este caso por aquí» (`[58:21]`).
- **Propuesta: en parte.** El dibujo 2 queda contestado (el rango sigue el mismo) y siempre en H4. En
  el dibujo 1 el rango pasa «a este bajo y esto este alto», sin decir de qué vela: no se puede decir
  si es la (a). Con «otra» en los dos, el «Para Aleks» manda `otra` (regla nueva con ADR), salvo que
  el consultor lea el dibujo 2 como (a). Regla general: sí («siempre», «considero que … es igual»).
  «creo»: no, pero «no sé» en `[54:23]` (si la ruptura es con mecha o con cuerpo). Alto y bajo: sí
  («es igual»).

### 3.5 S-5 (S-22): para que el máximo de la verde sea tu punto, qué tiene que hacer la roja

Vídeo v20, `[58:40]`–`[61:35]`, sobre el esquema.

- **La pregunta**: «El máximo de la última verde es tu punto.» (`[59:38]`), «Si vas a compasar el
  mínimo de la última con verde.» (`[59:42]`), «No, tiene que pasar el mínimo de toda la racha.»
  (`[59:46]`), «Vale.» (`[59:50]`), «Creo que...» (`[59:52]`), «A ver, no tiene que pasar el mínimo
  de la racha.» (`[59:54]`). Después: «A ver, es que me he inventado...» (`[59:58]`), «Vale, pero el
  problema es que no me está diciendo...» (`[60:00]`), «mayor planteamiento en el esquema inventado»
  (`[60:07]`). Y al final: «O sea, de mínimo de la última vela verde, que no tiene nada que ver,
  siempre se va a trazar, o sea, si lo vemos de esa manera, una vela roja, una vela verde, o al revés,
  allí se traza un punto, vale, …» (`[60:49]`).
- **Para precisar 1, «si la roja no pasa ningún mínimo, ¿vale el punto de antes o no hay punto?»**
  (fila propia): «si no pasa, pues no hay ningún punto, vale,» (`[60:49]`, en la misma línea).
- **Para precisar 2, «¿basta con que lo pase con la mecha?»** (fila propia): «basta con lo que pase
  con la mecha, que lo pase con mecha, si, basta con lo que pase con la mecha,» (`[60:49]`).
- «Para confirmar al final»: «el máximo de la verde es mi punto cuando la lar la roja cuando la roja»
  (`[61:23]`), y «vale lo descarto» (`[61:35]`): a medias.
- **Propuesta: no resuelve** la pregunta. Lee la (a) y la (b), dice «Creo que...» y «no tiene que
  pasar el mínimo de la racha», pide más planteamiento en el esquema y acaba en «una vela roja, una
  vela verde, o al revés, allí se traza un punto». Es lo que el bot hace hoy (ADR-0085 §3, que no se
  toca aquí). Las dos de «Para precisar» sí tienen respuesta: sin pasar ningún mínimo no hay punto, y
  basta la mecha. Regla general: no clara. «creo»: sí (`[59:52]`). Compra y venta: «o al revés»
  (`[60:49]`).

### 3.6 S-6 (S-19): el precio ya está más allá del 0 cuando se forma la caja

Vídeo v20, `[61:35]`–`[64:12]`, sobre el esquema («Aquí se forma la caja vale perfecto me gusta
esto», `[62:16]`).

- **Cuál de las cinco**: «inclinaría más que nada que espero que el cero quede al lado bueno y
  entonces la pongo bueno» (`[62:43]`), «no así está bien este es el punto de entrada es el punto de
  entrada es igual a nivel 0 de la caja» (`[62:56]`), «y si o sea para hacerlo de manera más detallada
  y no liarnos vale la respuesta va a ser la hay» (`[63:03]`), «otra cual con lo explicado pues
  anteriormente y aquí también vale ahora han explicado aquí pero» (`[63:10]`). Se inclina por la (b)
  («espero que el cero quede al lado bueno») y contesta «otra», con que el punto de entrada es el
  nivel 0 de la caja.
- **«¿Y si el precio vuelve por debajo del 0 antes de que pongas la orden?»**: «orden pues la orden no
  se tiene que ir nosotros tenemos tiempo de sobra para anticipar por ejemplo» (`[63:23]`); «ya o sea
  para adelante si el precio ya está más allá del cero o sea siempre como tiene que estar» (`[63:44]`),
  «a nivel, o sea, la orden tiene que estar a nivel» (`[63:54]`), «entonces, si sube o retrocede»
  (`[63:55]`), «solo toca esperar, o sea, la activaría» (`[63:58]`), «la orden, retrocedería y
  continuaría su» (`[63:59]`).
- «Para confirmar al final»: es la de `[63:44]` («si el precio ya está más allá del cero o sea siempre
  como tiene que estar»), sin completar.
- **Propuesta: en parte.** Se inclina por la (b), esperar a que el 0 quede del lado bueno, y contesta
  «otra». Si el precio vuelve, la orden sigue en el nivel y «solo toca esperar». Regla general: no
  clara. «creo»: «me inclinaría» (`[62:36]`–`[62:43]`). Compra y venta: no lo dice.

### 3.7 S-7 (material): una tarde que no está en el vídeo

Vídeo v20, `[64:13]`–`[72:21]`. El trader lee la pregunta («Alex te dice cuál.», `[64:32]`), y
después del silencio se dice el día: «El día dice 10 de julio.» (`[66:50]`). El trader abre el
replay de ese día y lo deja correr (`[67:28]`–`[69:55]`). Sus operaciones y cómo acabaron no se
escriben aquí.
- **Si esa tarde se grabó en otra parte y dónde**: «Que si es que no se llega a mostrar, simplemente,
  o sea, la B no se grabó, no se grabó y eso.» (`[72:13]`). La (b): no se grabó; no dice ninguna otra
  parte.
- **Propuesta: resuelve** la pregunta de material: esa tarde no se grabó.

## Estado

EN CURSO.
