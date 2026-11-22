# Sesión 7b con el trader: la extracción por pregunta y por sesión del bloque de días

> **Nació como PLANTILLA mientras la rama estaba EN CURSO** («la tabla final entra con la
> extracción»); la tabla final ya está, en §6.

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

### 0.2b Lo que el encargo manda verificar (escrito tras el revisor, b1)

Verificado el 2026-11-21 en el repo, antes de escribir la extracción:
- **`cobertura_material`** de `knowledge/cases/kit/config.yaml`: «2026-01» del `2026-01-02` al
  `2026-01-30`, «2026-04» del `2026-04-01` al `2026-04-29`, «2026-07» del `2026-07-01` al `2026-07-17`
  y «2026-08» del `2026-08-03` al `2026-08-31` (`grep` de `desde`/`hasta` en el fichero). Los cuatro
  tramos de construcción de la entrada a) cuadran.
- **Las ambigüedades de la tabla** (`knowledge/spec/ambiguedades.yaml`, leído con `yaml.safe_load`):
  A-13, A-35, A-48 y A-58, `ABIERTA`; A-16, `ABIERTA`; A-20, `RESUELTA`.
- **`liquidez_m15_mecha_que_vuelve`** (`parametros.yaml:595`): opciones `no_mueve`,
  `solo_la_contraria` y `cualquier_mecha`; `valor: solo_la_contraria`, `estado: DEFAULT_AMBIGUOUS`.

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
    `[125:32]` y `[125:57]`. Hay además una línea con un día sin mes en `[00:24]`, dentro del tramo no
    citable de la sesión 1 (§4.1). Los días del bloque son el
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
- **El gráfico real** (respuesta 4): el trader anuncia en voz que pasa a su gráfico o al mercado real
  en S-1 (desde `[03:27]`), en S-2 (desde `[28:00]`, y el tramo desde `[27:19]`, §14; y desde
  `[32:09]`) y en S-3 (desde `[39:21]` y
  desde `[48:40]`). Esas líneas abren los tramos y no se citan. **En ninguno dice el día en voz.**
  Según Aleks eran días de julio del 1 al 17, pero la voz no lo confirma. Por la regla de la PARADA
  condicional, cada uno es un tramo no citable, y la pregunta se queda con lo citable de fuera. Son
  cinco tramos: **0:03:27–0:14:49, 0:28:00–0:30:14 (desde la respuesta del consultor a la PARADA final,
  0:27:19–0:30:14, §14), 0:32:09–0:37:39, 0:39:21–0:44:06 y 0:48:40–0:49:18**. Sus límites salen de la voz y van por precaución hacia afuera (sin abrir
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
  «Dibujo 2», `[52:59]`, `[54:51]`; en S-6, «Aquí se forma la caja vale perfecto me gusta esto»,
  `[62:16]`). En S-5, «voy a usar
  este» (`[60:15]`) no dice qué; no hay palabra de gráfico ni de mercado.

### 3.1 S-1 (A-35, la única bloqueante): la mecha de un minuto que pasa tu alto de M15 y vuelve

Vídeo v20, `[00:07]`–`[14:43]`. Lo citable está en `[00:07]`–`[03:23]`; de `[03:27]` a `[14:49]` el
trader trabaja en su gráfico real, y ese tramo no es citable (la línea `[03:24]` lo solapa y sale tapada
en la filtrada regenerada, §14).

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
`[14:57]`–`[16:02]` (la lectura, menos `[15:46]`–`[15:51]`), `[25:35]`–`[27:13]`,
`[30:14]`–`[32:06]` y `[37:39]`–`[38:04]`. Los dos gráficos reales (0:27:19–0:30:14, adelantado desde
0:28:00 por la respuesta del consultor a la PARADA final, punto 7; y 0:32:09–0:37:39) no son citables,
y la línea `[32:07]` solapa el segundo y sale tapada en la filtrada regenerada (§14).

**Pregunta 1, las zonas de control (RN-009):**
- Sobre el dibujo 1: «vale, la A» (`[26:14]`), «si sería una zona» (`[26:18]`), «de control válida,
  la B también, la C también» (`[26:20]`), «y la D» (`[26:22]`), «punto breaker» (`[26:24]`).
- Al leer la pregunta: «La C también valdría como una zona de control.» (`[30:23]`). La línea siguiente,
  `[30:28]`, repite el enunciado de la pregunta: es el trader leyéndola, no su respuesta (revisor, a1).
  Después: «y antes que genere rompimiento el posible punto breaker, pues no solo nos deja una zona de
  control y rompe, no nos genera otras más» (`[30:49]`), «si hay más de uno, simplemente se invalida
  este posible punto breaker y no se opera, vale, esperaríamos a que el precio rompiera por debajo»
  (`[30:58]`).
- La opción: «pues la respuesta sería» (`[31:29]`), «la letra T» (`[31:30]`), «como lo he explicado
  anteriormente en el gráfico» (`[31:31]`; `ev-v20-003129-47928a18`, que supersede a
  `ev-v20-003028-0f59ea11`). Es una transcripción dudosa, no se abre ningún fotograma para ver la
  letra (§3.0), y lo explicado en el gráfico cae en el tramo no citable 0:27:19–0:30:14. **Si se forman
  antes o también después de romper el punto no tiene respuesta citable.**
- **Contradicción, dicha sin decidir (R4.6):** en `[26:20]` y `[30:23]` A, B y C le valen como zonas
  de control. En `[30:58]`, «si hay más de uno», se invalida el punto, que es lo fijado en A-20
  (RESUELTA: una sola zona; con dos se descarta, `zonas_control_max_por_esquema` = 1). En la 7a dijo
  «solo a y b» (`ev-v18-002115-bf40ec0b`). A-20 no se vuelve a preguntar (ADR-0093 §1): va como
  contradicción con lo fijado. Lo que dice de D (formado tras la ruptura) es solo «y la D», «punto
  breaker»: no dice si es zona de control.
- **«El bajo que deja la propia toma, ¿cuenta como zona de control?»** (fila propia): lo lee en
  `[37:06]` y lo contesta en `[37:19]`–`[37:37]`, dentro del tramo 0:32:09–0:37:39, porque señala
  algo en pantalla que puede ser el gráfico real. **No citable: no resuelve.**
- **Propuesta: no resuelve** «antes o después» (la letra es dudosa y remite al gráfico no citable). Lo
  citable deja la contradicción de cuántas zonas.

**Pregunta 2, el margen del break even (A-13):**
- Sobre el dibujo 2: «si está demasiado extendido el precio, vale, no llega, o sea, a estar en medio
  de» (`[26:30]`), «de nuestra zona de entrada, bastaría con cuerpo, o sea, que rompa con poco cuerpo y
  cierre,» (`[27:00]`), «para poder nosotros, pues, poner en break-even la entrada, o inclusive con
  mecha.» (`[27:07]`; `ev-v20-002630-6271f57e` y `ev-v20-002700-955a2dc8`). Lo que dice después, de
  `[27:19]` a `[27:54]`, cae desde la respuesta del consultor en el tramo no citable 0:27:19–0:30:14, y
  no se cita ni se resume: sus dos
  ítems, `ev-v20-002737-353f9542` y `ev-v20-002744-e0555bb6`, quedan supersedados (§14).
- La opción: «y la respuesta sería C, otra cual» (`[31:51]`), «porque ya dije, o sea, la diferencia»
  (`[31:55]`), «de las zonas de control» (`[31:57]`), «para puesta en break-even, enfocado»
  (`[32:00]`), «a la puesta de break-even» (`[32:02]`), «pues existe» (`[32:04]`), «el contexto»
  (`[32:06]`; `ev-v20-003151-ac4eb016`).
- **Basta cerrar por encima o pide margen**: «otra», por «la diferencia de las zonas de control para
  puesta en break-even» y porque «existe el contexto». Lo único citable que dice de qué depende es lo de
  `[26:30]`–`[27:13]`: si el precio está «demasiado extendido» y no llega a estar en medio de la zona de
  entrada, basta con poco cuerpo, «o inclusive con mecha». El otro caso (la zona en medio) cae en el
  tramo. **Cifra: ninguna. Unidad: ninguna. Siempre el mismo: no** (depende del contexto).
- «Para confirmar al final» (`[37:39]`): «Bueno, mi zona de control, pues, es la condicional para
  poder pasar a break even.» (`[37:49]`), «La vela tiene que estar por encima del alto de la zona de
  control.» (`[37:53]`), «Eso, pues, específicamente es solo en casos, pues, para poder poner en break
  even.» (`[37:57]`).
- **Ejemplo, en el replay del 10 de julio (S-7, citable)**: «para poder poner un break even se va a
  dar después de la entrada entonces aquí» (`[68:49]`), «ocurre el retroceso después de haber activado
  la entrada» (`[68:52]`). Es lo que la 7a dejó en duda (la zona del break even se forma después de la
  entrada: `ev-v19-011640-1fdc33a7`).
- **Propuesta: en parte**: «otra», sin margen fijo; lo citable da un solo caso (el precio extendido:
  poco cuerpo o mecha). Con «depende», A-13 sigue abierta (el «Para Aleks» de `PREGUNTAS-7B.md`). Regla
  general: sí, con su condición. «creo»: no. Compra y venta: lo dice para la compra del dibujo 2 y no
  habla de la venta.

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
  (`orden_stop_punto`, `parametros.yaml:753`; `PREGUNTAS-7B.md` daba la 702, revisor a5) lo decide el
  consultor: el trader descarta A y B tal como están dibujados.
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

## 4. El bloque de días (v21)

La filtrada de v21 leída entera, fuera de sus bloques tapados (fila de `HOLDOUT-EXPOSICIONES.md` del
2026-11-21, declarada antes). Las sesiones, en el orden de la respuesta b), que la filtrada confirma:
la 1, la 2, la 3, la 4 y la primera reserva. **Ningún fotograma de v21 se ha abierto**
(`fr-v21-de54adc8`, 7586 fotogramas, 0 extra). Sin resultados de operaciones en R ni en dinero. Las
láminas no se describen ni se cuentan: cada corrección va por su minuto, con las palabras del trader.

### 4.0 Lo que la filtrada dice del bloque, contra lo que contestó Aleks

- **Aleks, a ratos**: fuera del tramo no citable de la sesión 1, el trader le habla al final («Bro, ya
  finalicé hasta el 21 de enero, ¿vale?», `[125:32]`); lo de dentro de ese tramo no se cita.
- **Las láminas las abrió el trader** (lo pregunté a Aleks, y el encargo dice «Las láminas las enseñé
  yo»): «voy a abrir las» (`[55:33]`) «las láminas» (`[55:40]`); «Vale, entonces vamos a ver qué es lo
  que hizo, pues, qué se hizo en las láminas.» (`[100:10]`). **Contradice el encargo; a la PARADA
  final.** Lo que leyó en voz de cada lámina no se copia aquí.
- **Nadie hizo la pregunta de cada corrección.** «¿siempre, solo en este caso, o de qué depende?» no
  sale en la filtrada (`grep` de «siempre», «depende», «solo en este caso» y «solo aquí»: solo dos
  líneas del trader en la sesión 1, en el tramo no citable). **Toda corrección cuenta como ejemplo,
  salvo que generalice por su cuenta** (encargo, EXTRACCIÓN), y se dice en cada una.
- **El replay antes de compartir pantalla** (respuesta 5, «no»): la filtrada no lo contradice; el
  trader lo abre en directo («Vale, a ver, voy a abrirlo.», `[49:56]`).
- **La sesión 2, «todo limpio»** (respuesta 6): la voz no lo dice, y no se abre ningún fotograma para
  verlo.
- **La fecha en voz, al abrir y otra vez con el replay abierto** (respuesta 7): se cumple en las sesiones
  2, 3 y 4 y en la reserva (abajo). **En la 1, no** (§4.1).
- **Operó la sesión entera antes de ver ninguna lámina** (respuesta 8): sí en la 3, en la 4 y en la
  reserva. **En la 2, no**: operó primero la sesión de 7 a 11 y, al abrir las láminas, vio que eran de
  la de 11 a 15, que operó después (§4.2).

### 4.1 Sesión 1 · 2026-04-24, de 07 a 11 · sirve a S-3 (cociente 0,62 con el stop fuera) (v21, `[00:00]`–`[47:39]`) · no citable

La voz dice el día al empezar solo con su número, sin mes. La única fecha con número del arranque cae en
el bloque de cuarentena 0:03:54–0:04:02, y la voz no vuelve a decir el día ni el mes de forma visible
hasta `[47:39]`, donde empieza la sesión 2. Sin el mes, la voz no sitúa la sesión en un día de
construcción: el mismo número en julio no lo es. **Por la regla de la PARADA condicional, la sesión
entera es no citable y sin extraer** (tramo **0:00:00–0:47:39** en `tramos_no_citables.yaml`), y **el
2026-04-24 de 07 a 11, el día previsto por la respuesta b), queda gastado**. En ese tramo el trader
opera también la sesión de 11 a 15 del mismo día, que queda igual. A la PARADA final, por si Aleks la
levanta con la respuesta b).

### 4.2 Sesión 2 · 2026-04-15, de 11 a 15 · sirve a «el trader no opera y el bot sí (S-6 de la 7a); S-3» (v21, `[47:39]`–`[71:35]`)

- **El día, visible**: «Ahora, voy a 15 de abril, vale, vamos a plantear lo de 15 de abril.» (`[47:39]`,
  antes de abrir) y, tras «Vale, a ver, voy a abrirlo.» (`[49:56]`), «15 de abril, 15 de abril, 15
  desde el 14, vale, bueno, está bien, creo que 14, luego sigo al 15, confirmo que es 15, sí, 15 de
  abril, vale, lo que me gustó,» (`[50:00]`). Entre los dos, el silencio 0:48:45–0:49:39.
- **Primero opera la sesión de 7 a 11** (`[50:56]`–`[55:33]`), que no es la de la tabla:
  - sesgo y rango de H4: «el rango pues en este caso sería» (`[51:39]`) «bajista, vale» (`[51:42]`); «la
    actualización de nuestro» … «rango sería este nivel aquí» (`[51:58]`–`[52:03]`);
  - la toma de M15: «primero comenzamos con mecha, no es válido todavía ningún trick ese de allí, luego
    lo hace con cuerpo,» (`[52:46]`); «entonces aquí no habría ningún trade porque fue con mecha, tiene
    que ser con cuerpo por encima, aquí también fue con mecha,» (`[55:04]`, `ev-v21-005504-e34f514d`);
  - la entrada: «desarrollo de esquema 2, vale, solo el desarrollo de una zona de control, entonces aquí
    habría una entrada,» (`[53:00]`); el punto de dos velas del mismo color: «habíamos dicho que estos
    equals, pues, para nosotros eran validados, o sea, que la vela 1 y la vela 2, pues, tenía de igual o
    más abajo su mecha, nosotros lo validábamos, ¿vale?» (`[53:51]`);
  - el descarte: «porque apenas me genera la segunda zona de control yo descarto porque sé que no
    cumple» (`[55:28]`, `ev-v21-005523-e4941a17`).
- **Al abrir las láminas** (`[55:33]`) ve que son de la sesión de 11 a 15: «la sesión está claro está
  analizando la sesión de 11 a vale perfecto sí sí muy bien lo voy a» (`[56:49]`), «hacer ahora la
  sesión de 11 a 3» (`[56:58]`), «pensé que iba a ser» (`[57:02]`) «la sesión de 7 a 9» (`[57:03]`).
  **Desviación del paso 4**: la de 11 a 15 la opera después de haber abierto sus láminas.
- **La sesión de 11 a 15** (`[57:07]`–`[58:43]`): «rompimiento» (`[57:07]`) «de rango del salsista en
  ese caso» (`[57:09]`) «entonces buscamos operaciones salsistas» (`[57:11]`), que por el contexto
  es «alcista»; «ruptura de zona de línea de liquidez» (`[57:36]`) «de M15 con cuerpo» (`[57:38]`);
  «perfecto, no hay ninguna entrada, no llega a mitigar» (`[57:40]`); «aquí tendríamos una entrada que
  nos terminaría» (`[57:43]`). La caja, el 0 y el 0,8 no los dice en voz. **Para su «Sirve a»**: aquí
  el trader sí ve entradas en la sesión de 11 a 15.
- **Las correcciones** (ninguna preguntada; todas, ejemplo):
  - `[59:41]`–`[59:54]`: no corrige el trazo de la liquidez: «Es válido, me gusta el trazo» (`[59:46]`),
    «O sea, según hay aquellos datos» (`[59:52]`). Sirve a la liquidez, no a S-3.
  - `[62:57]`: «aquí es algo erróneo, vale, no se tiene por qué marcar algo allí». Ejemplo.
  - `[63:42]`–`[64:56]`, **sirve a S-3**: «Este planteamiento está erróneo.» (`[63:42]`), «No, sería
    desde aquí.» (`[64:17]`), «… esta es la zona desde la zona de control interna de toda» (`[64:35]`),
    «esta zona de aquí me genera el rompimiento aquí sería el nivel allí el trazo desde allí no desde»
    (`[64:48]`). Ejemplo.
  - `[66:23]`–`[67:31]`: primero «por ejemplo este de aquí está mal» (`[66:23]`), «esto de aquí, aquí no
    hay entrada» (`[66:25]`), «no, estamos buscando operaciones» (`[66:29]`) «operaciones alcistas»
    (`[66:32]`); después se corrige él: «Aquí hay una corrección.» (`[67:19]`), «El planteamiento de esta
    liquidez de aquí.» (`[67:20]`), «Es correcta.» (`[67:24]`), «Porque, claro, todo esto sería parte de
    M15, ¿vale?» (`[67:31]`). Ejemplo, con la liquidez del bot dada por buena.
  - `[70:10]`–`[71:04]`: «nuestro posible punto raker allí ubicado» (`[70:52]`) «pero vemos que»
    (`[70:54]`) «me genera zona de control» (`[70:56]`) «que invalidaría en este posible punto»
    (`[70:58]`), «ninguna entrada allí para tomar» (`[71:02]`). Ejemplo.
  - Y, de toda la sesión: «aquí el error que ha habido es más o menos» (`[71:11]`) «en la interpretación
    y algunos trazos de Gant» (`[71:14]`).
- **Contra su respuesta técnica**: en `[55:28]` descarta el punto con la segunda zona de control, y
  en S-2 (v20 `[30:23]`) dijo que la C también le valdría (§5.1, punto 1).

### 4.3 Sesión 3 · 2026-04-27, de 11 a 15 · sirve a S-3 (cociente 0,62 con el stop fuera) (v21, `[71:35]`–`[87:23]`)

- **El día, visible**: «15 de abril finalizado, continúo con 27 de abril» (`[71:35]`, antes) y, tras el
  bloque de cuarentena 1:12:12–1:13:32, «Entonces, me dirijo aquí, voy a 4 horas, 27 de abril, tenemos
  definido un rango alcista en H4, nos dirigimos a M15,» (`[73:33]`). Las horas de la sesión no las dice
  en voz.
- **Lo que marca y opera, antes de las láminas** (`[73:33]`–`[79:03]`): sesgo de H4 alcista
  (`[73:33]`); «marcamos la liquidez, dejamos marcada toda la liquidez necesaria» (`[74:47]`); en M1,
  «rompimiento» (`[77:06]`) «de la zona lineal del liquidez de M15» (`[77:06]`), «posible punto breaker
  más reciente» (`[77:10]`) «estaría ubicado aquí» (`[77:12]`), «llegara, pues me lo hizo con varias
  zonas de control» (`[77:18]`) «lo cual invalidaría este posible punto breaker» (`[77:20]`); y «llega,
  nos desarrolla una zona de control» (`[78:13]`) «y rompe, que es válido, entramos en el trade»
  (`[78:15]`). La caja, el 0 y el 0,8 no los dice en voz.
- **Las correcciones** (ninguna preguntada):
  - `[81:54]`: «aquí habría otro nivel, perfecto, sí, que me olvidé de trazar inclusive yo». Da la razón
    al bot. Ejemplo.
  - `[83:30]`–`[83:59]`, **sirve a S-3**: «punto aquí toma toma en cuenta la mecha verde pero no tiene
    que tomarlo desde desde las desde» (`[83:30]`), «porque eso forma parte de misión de control así lo
    mapeo sería así así entonces ahí hay un error» (`[83:48]`), «a ver continuando aquí esto aquí tendría
    que estar marcado el nivel 0 allí en ese alto de allí vale» (`[83:59]`; `ev-v21-012348-0582ea84`).
    Ejemplo.
  - `[84:43]`–`[85:11]`, la reentrada (B-11 de `PREGUNTAS-7B.md` §3, no S-3): «y luego si me»
    (`[84:55]`) «saca, pues tendría que esperar aquí» (`[84:57]`) «rompimiento de este nivel aquí en M1»
    (`[84:59]`) «y validarlo» (`[85:02]`) … «y plantear mi posible punto de breque para reentrar»
    (`[85:06]`), «pero esto está de más, eso es un error» (`[85:09]`; `ev-v21-012455-6eb57ef2`). Ejemplo.
  - `[86:06]`–`[87:20]`, las zonas de control (RN-009): «Cuando todas las velas son verdes, no existe
    zona de control.» (`[86:23]`), «Tiene que haber una vela roja contraria al impulso que se está dando
    para yo poder validarlo.» (`[86:28]`), «Entonces, todas son verdes es considerado un impulso.»
    (`[86:38]`; `ev-v21-012623-bbdaf48a`). **Regla general, por su cuenta** (lo dice en general, sin que
    se le pregunte). Y pide una sesión para esto: «y es necesario pues poder» (`[86:52]`) «explayarme
    más en esto» (`[86:54]`) «que me haga preguntas» (`[86:56]`).

### 4.4 Sesión 4 · 2026-01-19, de 11 a 15 · sirve a S-3 (cociente 1,78 en la entrada) (v21, `[87:23]`–`[112:11]`)

- **El día, visible**: antes de abrir, «27 de abril finalizado continuó con 19 19 de» (`[87:23]`; lo que
  sigue cae en el silencio) y «Bueno, ¿me puedo ir más atrás? ¿O sí? ¿Será que me puedo ir hasta
  enero?» (`[89:15]`); con el replay abierto, «de consenso de 19 o sea de enero 19 o sea desde»
  (`[104:41]`), y al cerrar, «Entonces, fecha 19 de enero cerrada.» (`[112:11]`).
- **Lo que marca y opera, antes de las láminas** (`[95:29]`–`[100:10]`): «separo la sesión de 11 a 3»
  (`[95:29]`); «11 a 3 la sesión, pues nos encontraríamos» (`[96:06]`) «en un rango alcista» (`[96:09]`)
  «según lo planteaba en H4» (`[96:11]`); «trazamos, vamos a M15» (`[96:14]`); en M1, «tendremos que
  esperar la ruptura de esto» (`[97:05]`) «con cuerpo, rompe con cuerpo» (`[97:07]`) «y recién nosotros
  habilitaríamos este punto» (`[97:09]`); el break even: «Entonces aquí ya al caer, estoy cerrado con
  cuerpo por debajo» (`[97:35]`) «Ya estaría yo, ya pondría un break even la entrada» (`[97:38]`;
  `ev-v21-013735-a127e031`); el objetivo, «a 1.3» (`[98:39]`).
- **Las correcciones** (ninguna preguntada):
  - `[101:50]`–`[101:56]`: «hizo bien su trabajo porque hay algo que» (`[101:50]`) «no me estaba dando
    cuenta, vale» (`[101:52]`) «era marcar este nivel aquí de M15» (`[101:54]`). Da la razón al bot.
  - `[103:25]`–`[105:12]`, el sesgo: corrige al bot por el rango y después se retira: «me corrijo yo
    mismo estoy buscando operaciones bajistas cuando el sesgo es alcista tú lo planteas a el bol lo
    plantea bien» (`[104:54]`–`[105:02]`; `ev-v21-014454-7eb03316`). **Contradicción, dicha**: su propia
    operación de la sesión iba contra el sesgo que dio en `[96:09]`, y el bot tenía razón.
  - `[108:14]`–`[108:55]`, **sirve a S-3**: «Porque vemos que si esta vela» (`[108:35]`) «Pues la otra
    vela» (`[108:37]`) «Tiene la mecha anterior y mucho más grande» (`[108:38]`) «Que esta de aquí»
    (`[108:41]`) «Entonces por lo cual» (`[108:43]`) «Trazaríamos nuestra caja hasta allí» (`[108:44]`;
    `ev-v21-014835-7e7bcd41`), y «Este es un error» (`[108:23]`). Ejemplo.
  - `[109:47]`: «vale esto está mal, o sea aquí hay un trazo luego de la toma, o sea aquí no habría
    entrada». Ejemplo.
  - `[111:04]`–`[111:23]`: «que ya no puede haber más o sea en m15 que tenemos las zonas lineales de m15
    están trazados» (`[111:04]`) «correctamente vale pero en m1 todavía hay errores en errores algunos
    errores» (`[111:23]`). Y vuelve a pedir una sesión sobre las zonas de control: «bueno si es necesario
    armar una sesión pues en cuanto a la explicación mucho más profunda de la» (`[110:27]`).
  - `[111:38]`–`[112:03]`, el lado de la liquidez: «Estamos buscando operaciones alcistas.» (`[111:48]`),
    «No nos importa la liquidez por arriba.» (`[111:49]`), «Nos importa la liquidez en M15 que está
    formado por debajo.» (`[111:51]`; `ev-v21-015148-54dd1a0c`). Ejemplo.

### 4.5 La reserva · 2026-01-21, de 07 a 11 · sirve a S-3 (cociente 0,50 en la entrada) (v21, `[112:19]`–`[123:16]`)

- **El día, visible**: «21 de enero» (`[112:19]`, antes de abrir: «voy a descargar primero»,
  `[112:22]`), y al acabar, con el replay abierto, «de la fecha» (`[123:13]`) «21 de enero»
  (`[123:16]`); después, «Bro, ya finalicé hasta el 21 de enero, ¿vale?» (`[125:32]`). La sesión: «7 a
  11» (`[115:13]`).
- **Lo que marca y opera, antes de las láminas** (`[114:14]`–`[117:14]`): el rango de H4, «nosotros
  teníamos un rango pues alcista» (`[114:18]`) «pero esta vela lo mitiga» (`[114:20]`) «entonces
  actualizaríamos un rango abajista» (`[114:22]`), y «entonces actualizaríamos y tendríamos un rango»
  (`[114:59]`) «bajista, entonces para la 7» (`[115:02]`); en M1, «rompe con mecha, necesitaremos romper»
  (`[115:52]`) «un cuerpo, aquí ya lo hace» (`[115:54]`) «habilitaríamos eso como el posible punto»
  (`[115:57]`); «la entrada sería desde este nivel» (`[116:15]`) «de aquí, hasta ese nivel de allí»
  (`[116:18]`) «por 1.3» (`[116:22]`). Las láminas, desde 1:57:19.
- **Las correcciones** (ninguna preguntada):
  - `[119:11]`–`[119:42]`, **sirve a S-3**: «está mal trazada la caja aquí en ese nivel en tal caso pues
    se» (`[119:21]`), «trazaría desde aquí hasta aquí vale desde ese nivel hasta ese nivel después si
    quiero» (`[119:27]`), «actualizar pues tendría que haber una zona en el desarrollo de una zona control
    variada» (`[119:33]`) «para ello poder actualizar el posible punto breaker que es el más reciente
    sería ese allí» (`[119:37]`; `ev-v21-015933-c05aad41`). Ejemplo.
  - `[120:14]`–`[120:24]`: «aquí esto no, porque» (`[120:14]`) «como dije, no habría entrada antes de
    eso» (`[120:21]`). Ejemplo.
  - `[121:25]`–`[121:52]`, **sirve a S-3**: «este nivel porque eso es estructura interna o sea de la zona
    de control que aquí no nos sirve» (`[121:34]`) «o sea nos sirve trazarlo desde este nivel desde aquí
    que es el punto breaker más reciente sería» (`[121:39]`) «mi nivel 0 a este aquí porque esto todo eso
    es el desarrollo de la zona de control completa y» (`[121:45]`; `ev-v21-020134-6ddd7cd6`). Ejemplo.
  - `[122:20]`–`[122:54]`: «Pero está mal» (`[122:20]`), «Porque yo tengo mi zona de control más
    reciente» (`[122:29]`), «O sea, valido mi ruptura con cuerpo» (`[122:32]`), «Entonces me fijo cuál
    es mi zona de control más reciente» (`[122:37]`). Ejemplo.
  - Al final, de todas: «cosas que destaco ya está corrigiendo pero todavía en m1 el trazo de cuadro»
    (`[126:10]`) «llegan y de entradas ahí está como que un poco pero si ha mejorado ha mejorado y dale»
    (`[126:14]`).
- **Con su respuesta técnica**: lo de `[121:34]`–`[121:45]` (el 0 en el punto breaker más reciente, sin
  la estructura interna de la zona de control) va con su respuesta a S-3 (§3.3).

### 4.6 Las reservas del 2026-01-22 (de 11 a 15) y del 2026-07-16 (de 07 a 11): no se hicieron

v21 acaba en 2:06:25 tras la del 21 de enero. El trader propone seguir más tarde («si tienes tiempo
pues podemos podemos avanzar una más», `[125:57]`), fuera del vídeo. La del 22 de enero era la que
tocaba A-16, el sesgo de H4 por una ruptura de 2 puntos (`PREGUNTAS-7B.md` §1): A-16 queda como
estaba, sin nada nuevo de esta sesión.

## 5. Contradicciones, cobertura y lo que el consultor tiene que mirar

### 5.1 Contradicciones y cosas que mirar (sin decidir, R4.6)

1. **Cuántas zonas de control.** En S-2, A, B y C le valen (v20 `[26:20]`, `[30:23]`;
   `ev-v20-003023-32448478`), y «si hay más de uno» el punto se invalida (v20 `[30:58]`;
   `ev-v20-003058-8518a5ff`). En el bloque descarta con la segunda (v21 `[55:28]`) y con «varias»
   (`[77:18]`). Lo fijado es una sola (`zonas_control_max_por_esquema` = 1, ambigüedad resuelta). En
   la 7a dijo «solo a y b». Es una contradicción con lo fijado y consigo mismo; no se decide aquí.
2. **Qué es una zona de control**: «Cuando todas las velas son verdes, no existe zona de control»
   (v21 `[86:23]`). Regla general por su cuenta, que corrige una lámina del bot. Y pide dos veces
   una sesión para explicarlo (`[86:52]`, `[110:27]`).
3. **El margen del break even**: en la 7a, «un par de puntos o un pip» (`ev-v19-011529-8ae8b581`); en
   la 7b, «otra», según «el contexto», sin cifra; lo citable da solo el caso del precio extendido (§3.2).
4. **El sesgo de la sesión 4**: opera contra el sesgo que dice y se corrige él mismo (§4.4).
5. **Los datos**: atribuye una diferencia con el bot a los datos («por los datos no coinciden», v21
   `[69:26]`).
6. **S-1 y S-3, sin contradicción** con el bloque: la toma de M15 con cuerpo (v21 `[52:46]`, `[55:04]`,
   `[115:52]`), y el 0 en el punto breaker más reciente, sin la estructura interna de la zona de control
   (v21 `[83:48]`, `[121:34]`).
7. **El gráfico real del bloque técnico, sin día en voz**: S-1 se queda sin su opción citable (§3.1), y
   la pregunta del bajo de la toma de S-2 tampoco tiene respuesta citable (§3.2).

### 5.2 Cobertura de lo que la 7b tenía que cubrir

| Qué | Ambigüedad o fuente | Cubierto |
|---|---|---|
| S-1, la mecha de un minuto que vuelve | A-35 | **no**: la opción, varias velas, el bajo y la frase caen en el tramo del gráfico real; lo citable no dice dónde queda el alto |
| S-2, las zonas de control | RN-009 | **no**: «antes o después», sin respuesta citable; contradicción en cuántas; el bajo de la toma, no citable |
| S-2, el margen del break even | A-13 | **en parte**: «otra», depende del contexto; lo citable da solo el caso del precio extendido; sin cifra |
| S-3, el 0 de la caja | A-48 | **en parte**: «otra», el punto más bajo de la zona de control que valida, su punto de entrada; la compra, sí |
| S-4, el rango de 4 horas tras una ruptura | A-58 | **en parte**: el dibujo 2, la ruptura por abajo y «siempre en H4», sí; el dibujo 1, sin decir de qué vela |
| S-5, el punto y la roja | S-22 | **no** la pregunta; las dos de «Para precisar», sí |
| S-6, el precio más allá del 0 | S-19 | **en parte**: «otra», inclinado a esperar; si vuelve, la orden a nivel |
| S-7, la tarde que no está en el vídeo | `VIDEO-JULIO.md` | **sí**: no se grabó |
| Sesión 1 (04-24), sirve a S-3 | — | **no**: la voz no la sitúa; sin extraer; el día queda gastado |
| Sesión 2 (04-15), sirve a «el trader no opera y el bot sí»; S-3 | — | **en parte**: ve entradas en la de 11 a 15; una corrección sobre la caja; desviación del paso 4 |
| Sesión 3 (04-27), sirve a S-3 | — | **sí**: el 0 en ese alto; y qué es una zona de control |
| Sesión 4 (01-19), sirve a S-3 | — | **sí**: la caja por la mecha mayor; el sesgo, retirado |
| Reserva (01-21), sirve a S-3 | — | **sí**: la caja desde el punto breaker más reciente |
| Reservas (01-22 y 07-16) | — | no se hicieron |

## 6. Tabla final

| Código | Ambigüedad | Vídeo | Tramo | Propuesta | Regla general | «creo» | Compra y venta |
|---|---|---|---|---|---|---|---|
| **S-1** | A-35 | v20 | 00:07–14:43 | no resuelve: la opción cae en el tramo del gráfico real; lo citable dice que la mecha de una M1 no es toma de M15 sino liquidez de M1, sin decir dónde queda su alto; no cae en ningún valor | sí, para la toma | no | lo citable, el alto |
| S-1, varias velas seguidas | A-35 | v20 | 10:49 | no resuelve: dentro del tramo no citable | n/a | n/a | n/a |
| S-1, el bajo al revés | A-35 | v20 | 13:13 | no resuelve: dentro del tramo no citable | n/a | n/a | n/a |
| **S-2, pregunta 1** | RN-009 | v20 | 25:35–31:34 | no resuelve: la letra sale como «T» y remite al gráfico no citable; contradicción: A, B y C le valen y «si hay más de uno» se invalida | sí, la de «más de uno» | no | no lo dice |
| S-2, el bajo de la propia toma | RN-009 | v20 | 37:06–37:37 | no resuelve: la respuesta cae en el tramo no citable 0:32:09–0:37:39 | n/a | n/a | n/a |
| **S-2, pregunta 2** | A-13 | v20 | 26:30–27:13; 31:51–32:06 | en parte: «otra», por la diferencia de las zonas de control y «el contexto»; lo citable da un caso: si el precio está demasiado extendido, poco cuerpo o mecha; sin cifra ni unidad | sí, con su condición | no | habla de la compra |
| **S-3** | A-48 | v20 | 44:06–48:40 | en parte: «otra», el 0 en el punto más bajo de la zona de control que valida, que llama su punto de entrada; ni A ni B | sí | no | sí |
| S-3, la compra | A-48 | v20 | 48:03–48:09 | resuelve: igual en una compra | sí | no | sí |
| **S-4, dibujo 1** | A-58 | v20 | 52:59–54:51; 56:53–57:12 | en parte: «otra»; el rango pasa «a este bajo y esto este alto», sin decir de qué vela | no claro | «no sé» (54:23) | n/a |
| **S-4, dibujo 2** | A-58 | v20 | 54:51–56:22; 57:12 | en parte: formalmente «otra»; lo explicado, que el rango sigue en el mismo nivel hasta que rompa una vela de su color | sí | no | n/a |
| S-4, la ruptura por abajo | A-58 | v20 | 57:42–57:50 | resuelve: igual, por el color | sí («considero que») | no | sí |
| S-4, ¿siempre en 4 horas? | A-58 | v20 | 57:17–57:39 | resuelve: siempre en H4, su temporalidad mayor | sí | no | n/a |
| **S-5** | S-22 | v20 | 58:40–61:35 | no resuelve: lee (a) y (b), dice «Creo que...» y pide más planteamiento; acaba en «una vela roja, una vela verde, o al revés, allí se traza un punto» | no | sí | «o al revés» |
| S-5, sin pasar ningún mínimo | S-22 | v20 | 60:49 | resuelve: no hay punto | sí | no | n/a |
| S-5, con la mecha | S-22 | v20 | 60:49 | resuelve: basta con la mecha | sí | no | n/a |
| **S-6** | S-19 | v20 | 61:35–64:12 | en parte: «otra»; se inclina por la (b), esperar a que el 0 quede del lado bueno | no claro | «me inclinaría» | no lo dice |
| S-6, si el precio vuelve antes | S-19 | v20 | 63:18–64:02 | en parte: la orden tiene que estar a nivel y solo toca esperar | no claro | no | no lo dice |
| **S-7** | VIDEO-JULIO.md | v20 | 64:13–72:21 | resuelve: (b), esa tarde no se grabó | n/a | no | n/a |
| Sesión 1 del bloque (2026-04-24, de 07 a 11) | — | v21 | 00:00–47:39 | **no citable**: la voz no la sitúa; sin extraer; el día queda gastado | — | — | — |
| Sesión 2 del bloque (2026-04-15, de 11 a 15) | — | v21 | 47:39–71:35 | ve entradas en la de 11 a 15; corrige la caja desde la zona de control (63:42–64:56); opera tras abrir las láminas | ejemplo | no | compras |
| Sesión 3 del bloque (2026-04-27) | — | v21 | 71:35–87:23 | el 0 «en ese alto» (83:59); la reentrada; sin velas rojas no hay zona de control (86:23) | la de 86:23 | no | compras |
| Sesión 4 del bloque (2026-01-19, de 11 a 15) | — | v21 | 87:23–112:11 | la caja por la mecha mayor (108:35); el lado de la liquidez; su sesgo, retirado | ejemplo | no | compras |
| Reserva del bloque (2026-01-21, de 07 a 11) | — | v21 | 112:19–123:16 | la caja desde el punto breaker más reciente, sin la estructura interna (121:34) | ejemplo | no | ventas |

Por códigos de la hoja (7): se hicieron los 7, en v20 y en el orden de la hoja. En filas: **resuelve**
7 (S-3 la compra, S-4 la ruptura por abajo, S-4 siempre en H4, las dos de S-5 de «Para precisar»,
y S-7); **en parte** 6 (S-2 pregunta 2, S-3, S-4 dibujo 1, S-4 dibujo 2, S-6 y S-6 si el precio
vuelve); **no resuelve** 6 (S-1, S-1 varias velas, S-1 el bajo, S-2 pregunta 1, S-2 el bajo de la toma
y S-5). Del bloque, 4 sesiones extraídas y 1 no citable (sin extraer); dos reservas no se hicieron.

## 7. PARADAS, desviaciones y negativas de la guardia

### 7.1 PARADA final (lo que no cuadra con las reglas del encargo o no lo prevén)

> Respondida por el consultor el 2026-11-21 (§13) y aplicada (§14): 1, 3, 5 y 8, como están; 2 y 4, no
> se levantan; 6, las filtradas regeneradas; 7, el tramo de S-2 desde 0:27:19.

1. **Las láminas las abrió el trader**, no Aleks (§4.0): el encargo dice «Las láminas las enseñé yo».
   ¿Tuvo el trader la carpeta `laminas-sesion-7b-v1`, o una copia? Si es así, conviene decidir si la
   clave (qué carpeta es qué sesión) sigue sin salir de Aleks, y si eso cambia algo para la 7c.
2. **La sesión 1 (2026-04-24, de 07 a 11), no citable** (§4.1): la voz dice el día solo con su número,
   y el mes no sale de forma visible. ¿Basta el número con la respuesta b) para levantarla, como se
   levantó el tramo de S-1 de la 7a? Mientras tanto, entera no citable y el día gastado.
3. **El bloque técnico lo dirigió el trader**, con Aleks fuera a ratos (§3.0): ADR-0093 §2 y
   `PREGUNTAS-7B.md` §1 dan a Aleks hacer las preguntas y la de cada corrección. **Nadie preguntó
   «¿siempre, solo en este caso, o de qué depende?»**, así que el bloque no da ninguna regla general
   salvo la de `[86:23]`, que generaliza él solo. R4.6 pide esa pregunta en cada corrección.
4. **S-1 (A-35, la única bloqueante) sin respuesta citable**: la dio sobre su gráfico real, sin decir el
   día. Si Aleks sabe de qué día era (según él, de julio del 1 al 17), puede decidir levantar ese
   tramo; aquí no se levanta.
5. **La sesión 2, operada después de abrir sus láminas** (desviación del paso 4): la de 11 a 15 la operó
   tras ver que las láminas eran de esa sesión. Sus correcciones se dan, pero no como sesión operada
   a ciegas.
6. **Las filtradas no tapan los tramos de precaución** (revisor, «Lo que no pude comprobar»): se
   generaron antes de añadirlos (los seis de v20 y el de la sesión 1 de v21), y la de v20 no va en orden
   cronológico (empieza por S-3 y S-4). Quien las lea ahora ve ese texto sin tapar: le pasó al revisor
   (a3). Volver a pasar el guion de `main` con `--solo-filtrar` los taparía. No lo hago: reescribe
   ficheros de la copia de seguridad y lo decide el consultor.
7. **`[27:19]`–`[27:54]` de v20, ¿esquema o gráfico real?** (revisor): lo que dice en `[27:19]` no deja
   saber si dibuja sobre el esquema o sobre su gráfico, y el gráfico real lo anuncia en 0:28:00. Lo leí
   como el esquema dibujado; sin fotograma no se puede asegurar. De ahí salen `ev-v20-002737-353f9542` y
   `ev-v20-002744-e0555bb6`. Si fuera el gráfico, el tramo empezaría en 0:27:19. (Respondido: empieza en
   0:27:19, §14; la frase que aquí se citaba cae ahora dentro y se quitó.)
8. **La clave de las láminas, fuera de git** (revisor): el informe da el minuto en que empieza cada repaso
   de láminas, como pide el encargo. Si en pantalla se viera el nombre de la carpeta, esos fotogramas
   (fuera de git, en esta máquina) dejarían deducir la clave. No lo sé, porque no se abren.

### 7.2 Desviaciones y negativas de la guardia

- **Desviaciones de la sesión** (según Aleks y contrastadas con la filtrada): los días de grabación,
  sin comprobar antes de grabar (§0.1; declarado); el trader dirigió las preguntas; el replay, abierto
  en directo; la sesión 2, operada tras abrir sus láminas; las láminas, abiertas por el trader; ninguna
  pregunta de «¿siempre…?».
- **Negativas de la guardia, todas de solo lectura, con la forma que propone su mensaje**: el bucle con
  `basename` y el guion que nombraba la raíz del repo («Decisiones de proceso»); dos `python -c` en un
  comando, y un `git add` seguido de `knowledge validate`, y otro seguido de `date`, en el mismo comando
  (una llamada por ejecutable); un `cat "knowledge/evidence/v18/$(ls …)"` para ver la forma de un ítem («rutas
  LITERALES»; seguí con `ls` y Read del fichero nombrado).
- **El barrido con `--desde 1 --hasta 1`** deja ver los demás números de sus líneas (§2.4); lo que dejó
  ver son días de construcción.
- **Ítems de evidencia rehechos antes de commitear**: uno cuyas notas corregí a mano después de crearlo
  (el id depende del contenido y `evidence new` rechazó el siguiente: «id … no coincide con el
  contenido»), y doce cuya afirmación decía más que su cita (una fecha, una sesión o un paréntesis de
  contexto). Los borré sin commitear y los rehice con `evidence new`, cuando hacía falta con la cita
  ampliada a los segmentos seguidos. Ninguno llegó a un commit.
- **La transcripción del corpus de v20**, sin su pico de memoria medido (la de v21 y los dos guiones, sí).
- **Seis ítems commiteados, supersedados** tras el revisor (a1 y a2), con `evidence new --supersede` y el
  mismo tema (§12).

## 8. Lo que deja la rama

- `knowledge/corpus/fuentes.yaml` y `manifest.yaml`: v20 y v21.
- `knowledge/corpus/transcripciones/`: `tr-v20-large-v3-int8-float16-2d93201d` (685 segmentos) y
  `tr-v21-large-v3-int8-float16-9a52aac1` (1140).
- `knowledge/corpus/fotogramas/`: `fr-v20-c29e6481` (4385 fotogramas, 0 extra) y `fr-v21-de54adc8`
  (7586, 0 extra). `corpus frames check`: «OK: 21 extracciones coherentes con el disco; 3 obligatorios
  presentes». Ninguno abierto.
- `knowledge/corpus/tramos_no_citables.yaml`: 15 «SIN AUDIO» (6 de v20 y 9 de v21), 3 de cuarentena (de
  v21) y 7 de precaución (6 de v20 y 1 de v21).
- `knowledge/evidence/v20/` (32 ítems: 24 y 8 que supersedan a otros tantos, §12 y §14) y
  `knowledge/evidence/v21/` (11). `evidence contradictions`:
  «OK: knowledge/evidence/_contradicciones.yaml con 0 contradicciones abiertas».
- v20 y v21 en `SESIONES_EN_CUARENTENA` y sus tests.
- `docs/sesion-7/HOJA-USADA-7B.md` y el recuadro de `PREGUNTAS-7B.md`.
- Las filas del 2026-11-21 en `HOLDOUT-EXPOSICIONES.md`.

## 9. Para la orden de cierre (preparado, sin aplicar)

- **La F nueva** de la Next Action (hoy, la línea 28 de `PROJECT_STATE.md`, **1169 bytes** con su fin
  de línea, `sed -n 28p | wc -c`); la propuesta, **1005 bytes** (`wc -c` del texto con su fin de línea):

  > F. La sesión 7, en dos días con el método de ADR-0093 (R4.3; pivote en
  > docs/plan/PIVOTES-SESION-7.yaml; línea base, RECORRIDA-CONSTRUCCION-2.md). La 7a (id
  > 2026-11-16-sesion-07) está ingerida (SESION-07-EXTRACCION.md) y ACTIVADA (ACTIVAR-SESION-07.md,
  > F39e: sesgo de H4 por el rango vigente, ADR-0094, con A-58 abierta; break even al cierre y con
  > cuerpo, A-13 abierta solo por el margen). La 7b (id 2026-11-20-sesion-08, v20 y v21, grabada el
  > 2026-11-20 y el 2026-11-21) está ingerida (SESION-08-EXTRACCION.md, F39j); la dirigió el trader y
  > la sesión 1 del bloque quedó no citable. Siguiente, en este orden: (2) activar la 7b, con la rama de
  > S-22 y S-19; (3) la corrida de ADR-0070 §3 y la lectura del pivote (ADR-0093 §6), con su
  > contingencia sin retocarla (decisión de Aleks del 2026-11-19; R4.3). El vídeo de mapeo (recibido el
  > 2026-11-18): SIN ABRIR y fuera del repo, no se ingiere; octubre y noviembre de 2026, reservados. C y
  > R6a en los huecos; R5.7 después de (3), sobre esa corrida.

  (en una sola línea, como la de hoy).
- **R4.3**, la línea de Estado (hoy **266 bytes**; la nueva, **290**): `- **Estado:** ABIERTA (la 7a,
  ingerida en trabajo/sesion-07 y activada en trabajo/activar-sesion-07, ACTIVAR-SESION-07.md; la 7b,
  grabada el 2026-11-20 y el 2026-11-21 e ingerida en trabajo/sesion-08, SESION-08-EXTRACCION.md; falta
  activarla, con la rama de S-22 y S-19, y leer el pivote).`
- **La copia de seguridad** en Technical Debt de `PROJECT_STATE.md` (línea 138; hoy **111 bytes**):
  `- Copia de seguridad de las crudas y los WAV … falta v18, v19, v20 y v21 (entera en HISTORIA,
  Technical Debt ACORTADA)` (**121 bytes**).
- **Lo nuevo fuera de git, para la copia de seguridad**:
  - los vídeos: `corpus/Estrategia del trader/Grabación de pantalla 2026-11-20 182155.mp4` y
    `Grabación de pantalla 2026-11-21 104411.mp4`;
  - `C:\Users\USER\Desktop\sesion-08-audio\`: `sesion-08-v20.wav` y `sesion-08-v21.wav`, las crudas
    (`sesion-08-v20.cruda-NO-LEER.jsonl` y `.txt`, y las de v21), **las filtradas regeneradas el
    2026-11-21** (`sesion-08-v20.filtrada.md`, sha256 `952dd3620bdf…`, y `sesion-08-v21.filtrada.md`,
    `9886c64a558d…`; §14; si ya se copiaron las de antes, se sustituyen), los registros
    (`.registro.txt`, reescritos con ellas) y las carpetas `sesion-08-v20-trabajo` y
    `sesion-08-v21-trabajo`;
  - `data/transcripciones/v20/` (270 MB) y `data/transcripciones/v21/` (466 MB);
  - `data/fotogramas/v20/` (1,9 GB) y `data/fotogramas/v21/` (3,9 GB).
- **Para la activación de la 7b**: el **2026-04-24 de 07 a 11 queda gastado** (§4.1; la PARADA 2 no lo
  levanta, §13); y las reservas del 2026-01-22 y del 2026-07-16 siguen sin usar.
- **A-35 en Technical Debt** (respuesta del consultor, «Además»): `- A-35 sigue ABIERTA y bloqueante
  tras la 7b: su respuesta cayó en un tramo no citable (SESION-08-EXTRACCION.md §3.1); va al trader por
  WhatsApp con el esquema del PDF y entra por «Mensajes del trader».` (**207 bytes** con su fin de
  línea). **Cabe en PROJECT_STATE**: hoy 24.576 bytes en `main`; con la F (−164), la copia de seguridad
  (+10) y esta línea (+207), unos 24.629, por debajo de 25.000. Sin medir: lo que el cierre cambie en
  Current Branch, Current Feature, Stable Main State y Last Stable Commit; el margen que queda, unos 370
  bytes, se comprueba con `wc -c` al cerrar.
- **Las lecciones para la orden de cierre** (respuesta del consultor, puntos 1, 3 y 6), tal cual:
  - «Las láminas las enseña Aleks desde su pantalla; nunca se le pasa al trader la carpeta ni el ZIP».
  - «Una sesión del bloque de días solo cuenta como ciclo de R4.6 si Aleks está presente de principio a
    fin y hace la pregunta de cada corrección; si no puede estar, se cambia el día».
  - «Un tramo de precaución que se añade después de generar la filtrada obliga a regenerarla antes de
    que nadie más la lea».

## 10. El cierre de la rama: sellos, push y CI

Los sellos de la rama, con su PICO DE MEMORIA (todos 3593 passed, 6 xfailed, exit 0):
- apertura (`5fc0f9fd`): sello sobre `e387514a`, **318 MiB**;
- registro de v20 y v21 (`7fcc7990`): sello sobre `341106dd`, **322 MiB**;
- v20 transcrita (`66ea16bd`): sello sobre `f3c45a0b`, **321 MiB**;
- extracción de v20 (`ca547e77`): sello sobre `ed57f829`, **320 MiB**;
- v21 transcrita, con su cuarentena (`565ea236`): sello sobre `331dc5be`, **318 MiB**;
- extracción de v21, evidencia y hoja usada (`69ccd8a2`): sello sobre `ae14ead2`, **317 MiB**;
- el de los hallazgos del revisor (§12): su línea, en el resumen final a Aleks (un informe no puede llevar
  el sello del árbol que lo contiene).

Antes del sello de `69ccd8a2`, con todo estadiado:
- `uv run pytest tests/unit/test_en_parte_no_se_cierra.py tests/unit/test_hoja_de_ruta.py
  tests/unit/test_transcribir_sesion.py tests/unit/test_hoja_preguntas.py`: `168 passed`; y lo que
  sus lectores sacan de la tabla final: A-35 «no resuelve», A-13 «en parte», A-48 y A-58 «en parte» y
  «resuelve»;
- `test_guardia_claude.py -k "lista_de_la_guardia or tramos_del_repo_real or misma_cuarentena"`:
  `3 passed`;
- `knowledge validate` (log fuera del repo): sin ERROR, «OK: 745 items de evidencia, 0 contradicciones
  abiertas, historial intacto»;
- `scripts/contrato_rama.py`: «CONTRATO: 54 ficheros dentro del contrato» y la línea `G2:`.

**La verificación final de la skill**, tras el commit `69ccd8a2`: `git diff --name-status main...HEAD --
knowledge/evidence knowledge/corpus/transcripciones knowledge/corpus/fotogramas data/manifests`: **39
`A`** y nada más (35 ítems, 2 transcripciones, 2 extracciones de fotogramas). Con los 6 que supersedan
(§12), 45 `A`; con los 2 de la respuesta del consultor (§14), 47.

**Push y CI**: `git push origin trabajo/sesion-08:refs/heads/fix/sesion-08` (con `69ccd8a2`), sin
negativa. La CI de Linux es el **run 44957773501**: `completed`, `failure`, `headSha` `69ccd8a2…`, con
**un solo fallo, el esperado**: `FAILED tests/unit/test_cli.py::test_state_check_ok_on_real_repo`
(«PROJECT_STATE declara la rama 'trabajo/sesion-08'; la rama actual es 'fix/sesion-08'»); «1 failed,
3497 passed, 101 skipped in 462.52s». Consultada con un `gh run view` suelto cada vez.

## 11. El encargo, punto por punto

| Punto del encargo | Hecho |
|---|---|
| Base (main, origin, tag, CI, ramas, hoja 08) y tag de cierre libre | sí («Base comprobada al abrir») |
| abrir-rama con la fila del día estadiada antes de comprobar | sí (`5fc0f9fd`; `G2:` en cada sello) |
| El corpus no es una unión | sí: carpeta normal (`fsutil`, «Base») |
| Los dos días de grabación, `False` | sí (§0.1); sin comprobar antes de grabar: desviación declarada |
| Los dos únicos vídeos sin registrar; v20 y v21 con su fecha y `drive_id` null | sí (§0.2, §1) |
| Las preguntas a Aleks antes del registro | sí (§0.3), contrastadas con la filtrada (§3.0, §4.0) |
| Registro, `test_inventario` a v1..v21, inventory y `check --hashes` | sí (§1) |
| Tests rotos a propósito, y verdes tras el alta | sí (§1.2) |
| Audio con las formas exactas; cortes SIN AUDIO; puerta del ASR | sí (§1.1, §2.1, §2.4) |
| Transcripción con «listo» antes de cada una; cuarentena con el guion de `main` | sí, cuatro «listo» (§2.1, §2.4) |
| Un commit propio por vídeo con la cuarentena, «Fuente: ADR-0093» | sí: `66ea16bd` (v20, sin bloques) y `565ea236` (v21, 3 bloques) |
| Fotogramas: extract y check | sí (§2.3, §8); ninguno abierto |
| Barrido de 1 a 31 y por defecto antes de leer | sí (§2.2, §2.4), sin PARADA |
| S-1 a S-7 con sus filas separadas | sí (§3.1 a §3.7) |
| El bloque de días, por sesión y por corrección | sí (§4.1 a §4.6) |
| Cobertura en `###` antes de la tabla; tabla final en el último `##` con «Tabla» | sí (§5.2, §6) |
| Los dos tests de la tabla antes del primer sello del informe | sí (§10) |
| Verificar `cobertura_material` y las ABIERTA | sí (§0.2b) |
| Evidencia con `evidence new`, fuera de los tramos; contradictions y validate | sí (§8; 35 ítems) |
| `HOJA-USADA-7B.md` y el recuadro de `PREGUNTAS-7B.md` | sí |
| Exposiciones del día, con «Escrita tarde» para el 20 | sí (filas del 2026-11-21) |
| Cierre preparado (F, R4.3, copia de seguridad, ficheros fuera de git) | sí (§9) |
| PROJECT_STATE por debajo de 24.900 tras abrir | sí: 24.614 |
| Verificación final: solo `A` en los cuatro directorios | sí (§10): 39 `A`, y 45 con los que supersedan |
| Push a `fix/sesion-08`, CI y revisor con su alcance | sí: run 44957773501, solo el fallo esperado (§10); el revisor, al pie, y lo hecho con sus hallazgos, §12 |

## 12. Lo que se hizo con los hallazgos del revisor

- **a1** (importa): la línea `[30:28]` de S-2, pregunta 1, es el trader leyendo la pregunta. Hecho:
  `ev-v20-003129-47928a18` supersede a `ev-v20-003028-0f59ea11` (mismo tema); §3.2, §5.2 y la fila de
  §6 pasan a «no resuelve».
- **a2** (importa): cinco afirmaciones que decían más que su cita. Hecho: `ev-v20-002737-353f9542`,
  `ev-v20-004813-a28c4443`, `ev-v20-004750-864a8f1e`, `ev-v20-003023-32448478` y
  `ev-v20-000138-584fefb5` supersedan a `ev-v20-002737-ffbdf9b1`, `ev-v20-004813-fa0027de`,
  `ev-v20-004750-2733677c`, `ev-v20-003023-18b67392` y `ev-v20-000138-fe33bb73`, con la afirmación
  ceñida a la cita. `evidence contradictions`: 0 abiertas.
- **a3** (importa): la fila del revisor en `HOLDOUT-EXPOSICIONES.md`, ampliada el mismo día con sus
  consultas en memoria, los barridos (cuyas salidas enmascaradas imprimen líneas que ahora caen en
  tramos, también los de la sesión), su lectura por error de `[39:21]`–`[43:57]` de v20 y lo demás que
  ejecutó.
- **a4** (menor): el «literal» de `[63:37]` sustituido por uno literal de S-6 (`[62:16]`).
- **a5** (menor): `parametros.yaml:753` (`orden_stop_punto`).
- **a6** (menor): fuera el «fecha [N]» de §2.4; §4.1 sigue describiendo el tramo sin citarlo, como la v19
  de la 7a.
- **b1** (importa): §0.2b, con la verificación de `cobertura_material` y de las ABIERTA.
- **b2** y **b3** (menores): §10, con los tests, la verificación de solo `A`, el pico del sello de
  `69ccd8a2` y la CI.
- «Lo que no pude comprobar»: las filtradas sin tapar, la duda de `[27:19]`–`[27:54]` y la clave fuera de
  git, a la PARADA final (§7.1, puntos 6 a 8).

## 13. Respuesta del consultor a la PARADA final

Dada por Aleks (consultor) el 2026-11-21, en un solo mensaje. Copiada tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA final de trabajo/sesion-08 (§7.1 de SESION-08-EXTRACCION.md), 2026-11-21. Cópiala tal cual al informe, en una sección «Respuesta del consultor a la PARADA final». Si pasas de medianoche, la fila de HOLDOUT-EXPOSICIONES del 2026-11-22 va antes del primer make check de ese día (G2).
>
> 1. Las láminas las abrió el trader: se declara como desviación, sin más en esta rama. Todos los días del bloque son de construcción (casos_ocultos False), así que no hay exposición de holdout. La clave solo protege que el trader no sepa qué sesión es cada carpeta antes de operarla, y eso ya lo recoge el punto 5. Lo que haya pasado con la carpeta lo contesta Aleks fuera de la rama; si cambia algo, entra en la preparación de la 7c. Para la orden de cierre, la lección: «Las láminas las enseña Aleks desde su pantalla; nunca se le pasa al trader la carpeta ni el ZIP».
>
> 2. La sesión 1 (el 24 de abril, de 07 a 11): NO se levanta. «24» sin mes no sitúa el día: el mismo número cae en meses que no son de construcción, y la respuesta b) de Aleks dice lo previsto, no lo que se abrió (respuesta del consultor a la PARADA 2 de la 7a). Se queda entera no citable, sin extraer y con el día gastado, como está. No se abre ningún fotograma para comprobarlo.
>
> 3. Sin regla general en el bloque: se acepta tal cual. Toda corrección cuenta como ejemplo, salvo la de [86:23], que generaliza el trader por su cuenta. Lección para la orden de cierre: «Una sesión del bloque de días solo cuenta como ciclo de R4.6 si Aleks está presente de principio a fin y hace la pregunta de cada corrección; si no puede estar, se cambia el día».
>
> 4. El tramo de S-1: NO se levanta. Que Aleks recuerde que eran días de julio del 1 al 17 no sustituye a la voz, y él mismo dijo que no lo recuerda del todo. A-35 sigue ABIERTA y bloqueante. La pregunta va al trader por WhatsApp, con el esquema del PDF, fuera de esta rama; su respuesta entrará por la vía de «Mensajes del trader».
>
> 5. La sesión 2, operada después de abrir sus láminas: sus correcciones se quedan como ejemplos y se marca que no fue a ciegas, como ya está escrito. No cuenta como sesión operada a ciegas para el Marcador ni para R4.6.
>
> 6. Las filtradas: SÍ, se regeneran en esta rama con el guion de main y --solo-filtrar, una por vídeo, para que tapen los tramos de precaución (los seis de v20 y el de la sesión 1 de v21). Antes:
>    a) Comprueba que la filtrada no está en ningún manifiesto inmutable (knowledge/corpus/transcripciones/, data/manifests/). Si lo está, PARADA.
>    b) Comprueba que --solo-filtrar lee tramos_no_citables.yaml del árbol actual y no transcribe de nuevo.
>    Después: el hash de cada filtrada antes y después, en el informe; cuántos segmentos tapa ahora cada una; y que ningún ítem de evidencia de la rama cita una línea que quede tapada (la puerta de la skill, otra vez).
>    Lo que leyó el revisor dentro de un tramo de precaución (a3) se declara en HOLDOUT-EXPOSICIONES.md como exposición posible, con el tramo y sin contenido, si no está ya declarado así. Para la orden de cierre, la lección: «Un tramo de precaución que se añade después de generar la filtrada obliga a regenerarla antes de que nadie más la lea».
>
> 7. [27:19]–[27:54] de v20: por precaución, el tramo no citable de S-2 empieza en 0:27:19. «Linealmente, si lo planteamos usando un gráfico alcista» no deja saber si es el esquema o su gráfico, y lo que no se sabe se niega. Los dos ítems ev-v20-002737-353f9542 y ev-v20-002744-e0555bb6 citan dentro: aplica el régimen de la evidencia que corresponda (supersede si el régimen lo admite para retirar una cita que cae en un tramo no citable, o lo que diga la puerta de la skill). Si ningún régimen lo permite sin romper la inmutabilidad, PARADA con las opciones. Rehaz la fila de S-2, pregunta 2, de la tabla final y la cobertura con lo que quede citable (31:51–32:07 y lo de fuera).
>
> 8. Los fotogramas de los repasos de láminas: no se abren, como hasta ahora. No hace falta nada más: están fuera de git y el informe no da ni el número de láminas ni la carpeta.
>
> Además, para la orden de cierre:
> - Deja preparada en §9 una línea de Technical Debt sobre A-35 (sigue ABIERTA y bloqueante tras la 7b, pendiente de la respuesta por WhatsApp), si cabe en el tope de PROJECT_STATE; si no cabe, va en R4.3, en la hoja de ruta.
> - Para la copia de seguridad, la lista de §9 se actualiza con las filtradas regeneradas.
>
> Lo que sigue: un commit con 6, 7 y esta respuesta en el informe (make check sellado antes); push a fix/sesion-08 y CI de Linux, con el número del run de 097f04c9 y del commit nuevo; revisor con alcance en lo nuevo (las filtradas regeneradas contra tramos_no_citables.yaml, la evidencia retirada o supersedida y la tabla final), y su informe pegado al final.
>
> Rama lista para revisión, NO cerrada.

## 14. La respuesta del consultor, aplicada (2026-11-21)

- **1, 3 y 5**: se quedan como están en §4 y §7 (desviaciones declaradas; toda corrección, ejemplo,
  salvo `[86:23]`; la sesión 2, no a ciegas). En `HOJA-USADA-7B.md` §5 se añade que las láminas las
  abrió el trader. Las lecciones, en §9.
- **2 y 4**: no se levanta ni la sesión 1 ni el tramo de S-1. A-35 sigue ABIERTA y bloqueante; su línea de
  Technical Debt, en §9.
- **6, antes**: (a) ningún manifiesto nombra una filtrada: `grep -rln -i filtrada data/manifests
  knowledge/corpus/transcripciones` no devuelve nada (exit 0, sin líneas); (b) en
  `scripts/transcribir_sesion.py` de `main` (`git diff --quiet main`: exit 0), `procesar` lee los tramos
  con `tramos_del_video(video, RAIZ)`, es decir, `tramos_no_citables.yaml` del árbol actual, y con
  `--solo-filtrar` relee la cruda que ya existe sin transcribir (registra «modo: solo filtrar (la cruda
  ya existia; ASR no ejecutado)»), y escribe la filtrada y el registro fuera del repositorio.
- **6, la regeneración**, con el tramo de S-2 ya en 0:27:19 (punto 7), una llamada por vídeo:
  `uv run python scripts/transcribir_sesion.py --audio C:/Users/USER/Desktop/sesion-08-audio/sesion-08-v20.wav --sesion 08 --video v20 --solo-filtrar`, y lo mismo con v21.

  | Filtrada | sha256 antes | sha256 después | Segmentos tapados ahora | Bloques |
  |---|---|---|---|---|
  | `sesion-08-v20.filtrada.md` | `928445e1ad80…` | `952dd3620bdf…` | 293, por tramos (de 685; antes, 4) | 8 `[NO CITABLE]` |
  | `sesion-08-v21.filtrada.md` | `2f6d07382049…` | `9886c64a558d…` | 440: 431 por tramos y 9 por tramos y cuarentena a la vez (de 1140; antes, 14) | 7 `[NO CITABLE]` |

  Las crudas no cambian (sha256 igual antes y después: `b5db174809c7…` y `b2577d1181d4…`). Los bloques
  nuevos: v20 `[39:21–44:05]`, `[48:40–49:18]`, `[03:24–14:45]`, `[15:46–15:50]`, `[27:19–30:08]` y
  `[32:07–37:38]`, además de los dos de los silencios que ya estaban; v21 `[00:00–47:33]`, que se come el
  bloque de cuarentena 0:03:54 y el de 0:36:43; el de 1:12:12 pasa a `[NO CITABLE]`. Dos bloques
  empiezan un segmento antes que su tramo porque ese segmento lo solapa: `[03:24]` (tramo 0:03:27) y
  `[32:07]` (tramo 0:32:09). Ninguna de las dos líneas se cita (§3.1 y §3.2 dicen ahora hasta `[03:23]`
  y hasta `[32:06]`).
- **6, la puerta**: `uv run botsito knowledge validate` (log fuera del repo) da «OK: 753 items de
  evidencia, 0 contradicciones abiertas, historial intacto» y ningún ERROR. Su comprobación
  `ventanas_no_citables` (`validation/knowledge.py:102-129`) rechaza todo ítem activo cuya ventana
  solape un tramo o un segmento de la cruda que solape un tramo, que es lo que la filtrada tapa.
  `evidence contradictions`: 0 abiertas.
- **6, la lectura del revisor**: declarada como exposición posible en `HOLDOUT-EXPOSICIONES.md`, con el
  tramo y sin contenido (fila nueva del 2026-11-21).
- **7**: el tramo de S-2 empieza en **0:27:19** (antes 0:28:00), con su motivo y su `acordado`. El régimen
  que vale es el de la evidencia: `knowledge validate` solo comprueba contra los tramos los ítems
  activos, y un ítem supersedado «no cuenta: no se cita» (`validation/knowledge.py:103-107`). Así que
  se supersede, sin romper la inmutabilidad: `ev-v20-002630-6271f57e` (`[26:30]`–`[27:13]`, el precio
  extendido) supersede a `ev-v20-002744-e0555bb6`, y `ev-v20-003151-ac4eb016` (`[31:51]`–`[32:04]`, la
  opción) supersede a `ev-v20-002737-353f9542`, con el mismo tema
  (`break_even.margen_segun_distancia`). `ev-v20-002737-ffbdf9b1` ya estaba supersedado (§12). §3.2, la
  fila de §6 y la de §5.2 se rehacen con lo que queda citable: `[26:30]`–`[27:13]` y
  `[31:51]`–`[32:06]`.
- **8**: ningún fotograma abierto.
- **El texto de dentro del tramo nuevo**: con el tramo desde 0:27:19, tres sitios del informe quedaban con
  texto de dentro: el resumen de `[27:19]`–`[27:54]` en §3.2, la frase de `[27:19]` en §7.1 (punto 7) y la
  misma frase en el informe del revisor. Se quitaron, y en el del revisor queda la marca de lo quitado.
  La respuesta del consultor (§13) la cita también y se deja: se copia tal cual.
- **La CI**: el run de `097f04c9` es el **44962532780** (`completed`, `failure`; un solo fallo, el esperado,
  `test_state_check_ok_on_real_repo`; «1 failed, 3497 passed, 101 skipped»). El del commit de esta
  respuesta, y el revisor de lo nuevo, al pie.

## Estado

Rama lista para revisión, NO cerrada. La PARADA final (§7.1), respondida por el consultor (§13) y
aplicada (§14).

## Informe del revisor

Subagente `revisor`, lanzado el 2026-11-21 con el informe ya terminado (`69ccd8a2`) y el alcance que pide
el encargo («CIERRE DE LA RAMA», (1) a (3)). Pegado tal cual, con dos excepciones: en a6 copiaba un
fragmento de la línea `[00:24]` de v21, que cae en el tramo no citable 0:00:00–0:47:39; y en «Lo que no
pude comprobar», la frase de `[27:19]` de v20, que cae desde §14 en el tramo 0:27:19–0:30:14. Se
quitaron, y queda la marca «[fragmento de un tramo no citable, quitado al pegar]». Lo que se hizo con
cada hallazgo, en §12.

### Informe del revisor · trabajo/sesion-08 · 2026-11-21

#### Eje (a) · Reglas de la casa
Resumen: 0 bloquea, 3 importa, 3 menor.

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| a1 | importa | **La «(b)» de S-2, pregunta 1, sale de una línea que casi seguro es el trader leyendo la pregunta, y no su respuesta.** `ev-v20-003028-0f59ea11` (RULE_STATEMENT: «las zonas de control se forman antes de romper el punto y pueden formarse tambien despues») cita `[30:28]`. Esa línea va justo después de la lectura de la pregunta y repite su enunciado; el trader lo vuelve a leer como pregunta en `[31:24]` y contesta «la letra T … como lo he explicado anteriormente en el gráfico», es decir, en el tramo no citable 0:28:00–0:30:14. El informe se apoya en esa línea («Con `[30:28]`, lo dicho es la (b)», §3.2) y la arrastra a §5.2 y a la fila «S-2, pregunta 1» de §6. Lo citable de la respuesta es solo «la letra T» (dudosa) más una remisión al gráfico. | Filtrada v20, l. 566: `[30:14] Abujo A1. A y B te valen como zona de control y C no.`; l. 568: `[30:28] Se forman antes de romper el punto y pueden formarse también después de romperlo.`; l. 577-581: `[31:24] ¿se forman antes de romper el punto` / `[31:26] o pueden formarse también después de romperlo?` / `[31:29] pues la respuesta sería` / `[31:30] la letra T` / `[31:31] como lo he explicado anteriormente en el gráfico`. Enunciado: `docs/sesion-7/PREGUNTAS-7B.md:179-180`. Informe: `SESION-08-EXTRACCION.md:344-346`, `:735`, `:756` |
| a2 | importa | **Hay afirmaciones que dicen más que su cita: meten el contexto de la pregunta o quitan una condición.** (1) `ev-v20-002737-ffbdf9b1`. Cita: «aquí entonces está en medio cuando está en medio y tendría que romper con cuerpo y cerrar con cuerpo». Afirmación: «cuando la zona de control queda en medio del nivel de entrada, para el break even tiene que romper…». «Zona de control», «nivel de entrada» y «break even» no están en la cita. (2) `ev-v20-004813-fa0027de`. Cita: «El cero, por lo general, va en una compra, el punto de entrada». Afirmación: «el 0, por lo general, va en el punto de entrada». Quita «en una compra». (3) `ev-v20-004750-2733677c`. Afirmación: «el explicado sobre el esquema». La cita dice solo «Con lo explicado, pues, anteriormente», y la línea siguiente dice «tanto en el gráfico como en el propio esquema» (`[47:57]`), y el gráfico es el tramo no citable. (4) `ev-v20-003023-18b67392`. Afirmación: «sobre el dibujo 1». La cita no lo dice, y el propio informe pone esa línea en «Al leer la pregunta», no en «Sobre el dibujo 1» (§3.2, :339). (5) `ev-v20-000138-fe33bb73`. Cita: «al menos cuando hay la toma». Afirmación: «para que haya toma». Cambia el sentido de la condición. Ninguno está commiteado como corregido: un ítem commiteado no se edita, se supersede (`evidence new --supersede`). | Los cinco ficheros en `knowledge/evidence/v20/`, leídos con `cat`. Filtrada v20, l. 57-58 y 538 |
| a3 | importa | **La fila del revisor en `HOLDOUT-EXPOSICIONES.md` (estadiada) se queda corta. Viene de esta revisión y hay que ampliarla el mismo día antes del siguiente `make check`.** No declara: (i) `casos_ocultos` y `cargar_meses_reservados` en memoria, solo recuentos: 34 fechas, 5 meses, 0 líneas; (ii) los barridos `scripts/barrido_dias.py` sobre las dos filtradas. Su salida enmascarada imprime líneas dentro de tramos no citables: 14 de las 49 de v20 (1-31) caen en los tramos de precaución, y 7 de las 22 de v21 (18-31) en 0:00:00–0:47:39; el 1-31 de v21 lo vi filtrado a las líneas con mes; (iii) **una lectura mía, por error, dentro de un tramo**: las líneas 10-22 de la filtrada de v20 (`[39:21]`–`[43:57]`, tramo 0:39:21–0:44:06). La filtrada empieza por la sección S-3 y no por el minuto 0, y yo esperaba orden cronológico. No traen día ni precio, y aquí no se copia nada; (iv) un `grep` de `cobertura_material` en `knowledge/cases/kit/config.yaml`, `gh run view 44957773501`, `knowledge validate`, `corpus transcript check`, `corpus frames check` y dos `pytest`. | `git diff --cached -- docs/validation/HOLDOUT-EXPOSICIONES.md` (la fila del revisor solo nombra commits, documentos, filtradas, registros y CI) |
| a4 | menor | **Un «literal» que no es literal.** §3.0 cita «me gusta como lo [has] trazado» (`[63:37]`). La filtrada dice «es me gusta como el atrasado el punto cero…». El informe avisa de que «cada literal es de la FILTRADA». | Filtrada v20, l. 238; `SESION-08-EXTRACCION.md:297` |
| a5 | menor | **Línea de parámetro desfasada**: `parametros.yaml:702` para `ultimo_pivote_m1`/`referencia_de_la_toma`. `orden_stop_punto` está en la 753, en `main` y en la rama. La cifra viene copiada de `PREGUNTAS-7B.md:234`. | `grep -n "nombre: orden_stop_punto"` → `753:` (también en `git show main:`); `SESION-08-EXTRACCION.md:408` |
| a6 | menor | **Un fragmento literal de dentro de un tramo no citable.** §2.4 copia [fragmento de un tramo no citable, quitado al pegar] de `[00:24]`, que cae en 0:00:00–0:47:39 (salida enmascarada del barrido). Y §4.1 y la fila de HOLDOUT describen lo que pasa dentro de ese tramo («opera también la sesión de 11 a 15»). Hay precedente en `main` (la v19 en `fuentes.yaml`), pero ese fragmento sobra. | `SESION-08-EXTRACCION.md:244`, `:547-548`; barrido por defecto de v21: [fragmento de un tramo no citable, quitado al pegar] |

Comprobado sin hallazgos:
- **Contrato**: `uv run python scripts/contrato_rama.py` → «CONTRATO: 54 ficheros dentro del contrato de trabajo/sesion-08 (riesgo medio, artefacto docs/validation/SESION-08-EXTRACCION.md, tramo 'R4', 9 comprobaciones para el revisor)» / «G2: fila de HOLDOUT-EXPOSICIONES del 2026-11-21 para trabajo/sesion-08, estadiada», exit 0.
- **Comprobaciones del contrato que ejecuté**: `corpus transcript check` → «OK: 28 transcripciones coherentes»; `corpus frames check` → «OK: 21 extracciones coherentes con el disco; 3 obligatorios presentes»; `knowledge validate` → «OK: 745 items de evidencia, 0 contradicciones abiertas, historial intacto» y «203 registros de feedback, historial intacto, commits con Fuente»; `git diff --name-status … knowledge/evidence knowledge/corpus/transcripciones knowledge/corpus/fotogramas data/manifests` → 39 `A` y nada más; `pytest test_en_parte_no_se_cierra.py test_hoja_de_ruta.py` → 27 puntos, ningún F; `wc -c PROJECT_STATE.md` → 24614 (en `main`, 24576).
- **`make check`**: no lo lancé. `make-check.log` trae «3593 passed, 6 xfailed», «SELLO: make check en verde sobre el arbol ae14ead2…», que es `HEAD^{tree}`, y «PICO DE MEMORIA … 317 MiB». La fila estadiada del revisor cambia el árbol, así que el próximo commit necesita su propio sello.
- **Trailers `Fuente:`**: los cuatro commits que tocan `tramos_no_citables.yaml` llevan `Fuente:` en el cuerpo (ADR-0021 en 7fcc7990; ADR-0093 en ca547e77, 565ea236 y 69ccd8a2). 66ea16bd también lleva ADR-0093. Nada toca `knowledge/spec` ni `knowledge/cases`.
- **Holdout**: nada en `knowledge/cases/holdout/`. Hay filas del 2026-11-21 con «Escrita tarde para el 2026-11-20 (v20)». La consulta de `casos_ocultos` del 10 de julio está declarada.
- **Regímenes de cambio**: evidencia, transcripciones y fotogramas solo `A`. `HOLDOUT-EXPOSICIONES.md` solo con líneas añadidas. Sin cambios en feedback, `libros.yaml`, spec, ADR, hoja de ruta, motor, domain ni `scripts/`.
- **Ni ambigüedades, ni ADR, ni sitios con `cita`.** No se corrige ningún informe cerrado.
- **Resultados**: ningún resultado en R ni en dinero en el informe ni en `HOJA-USADA-7B.md`. Grep de win/loss/positivo/negativo/sacando/R/euros/pips: solo la cita de la 7a «un par de puntos o un pip». Cada línea de la filtrada que el informe corta deja fuera los precios, los desenlaces y lo que el trader lee de las láminas (comprobado en `[57:43]`, `[62:57]`, `[64:35]`, `[83:30]`–`[83:48]`, `[109:47]`, `[120:14]`–`[120:21]`).
- **Citas del informe contra la filtrada, más de 60, literales salvo a4**: S-1 `[01:38]` `[01:45]` `[02:37]` `[02:51]`; S-2 `[26:14]`–`[27:49]` `[30:49]` `[30:58]` `[31:51]`–`[32:00]` `[37:49]`–`[37:57]`; S-3 `[46:10]`–`[48:33]`; S-4 `[54:23]`–`[58:21]`; S-5 y S-6 `[59:38]`–`[63:59]`; S-7 `[66:50]` `[72:13]`; v21 `[47:39]` `[50:00]` `[52:46]` `[53:51]` `[55:04]` `[55:28]` `[56:49]`–`[57:43]` `[59:46]` `[63:42]`–`[64:48]` `[66:23]`–`[67:31]` `[70:52]`–`[71:14]` `[73:33]` `[77:06]`–`[78:15]` `[81:54]` `[83:30]`–`[83:59]` `[84:55]`–`[85:09]` `[86:23]`–`[86:56]` `[87:23]` `[89:15]` `[95:29]`–`[98:39]` `[101:50]`–`[101:54]` `[104:54]`–`[105:02]` `[108:23]`–`[108:44]` `[110:27]`–`[112:11]` `[112:19]` `[114:18]`–`[116:22]` `[119:21]`–`[119:37]` `[121:34]`–`[121:45]` `[122:20]`–`[122:37]` `[123:16]` `[125:32]` `[125:57]` `[126:10]` `[126:14]`.
- **Cifras del cierre**: la línea 28 de `PROJECT_STATE.md` tiene 1169 bytes y la F propuesta 1005 (1004 sin el fin de línea); la línea 138, 111 bytes. `parametros.yaml:595` es `liquidez_m15_mecha_que_vuelve` con las tres opciones y hoy `solo_la_contraria` DEFAULT_AMBIGUOUS.

**Lo que el encargo pidió además:**
1. **Fechas reservadas en cada commit** (en memoria, sin imprimir ninguna): 2562 líneas examinadas (las añadidas de `git log -p main..HEAD`, los mensajes y lo estadiado). **0 líneas** con una fecha AAAA-MM-DD de un caso oculto. **0 líneas** con una fecha de un mes reservado distinto de octubre y noviembre de 2026. Las de octubre y noviembre son fechas de trabajo del proyecto, ninguna oculta. Los días escritos en palabras («15 de abril», «19 de enero»…), pasados a fecha: 0 ocultos y 0 de mes reservado. **La clave de las láminas**: nada de lo commiteado dice qué carpeta es qué sesión, ni cuántas láminas hubo, ni su numeración. Lo que el trader lee de las láminas no se copia. Juntando pasajes: el número de correcciones por sesión del informe no coincide de forma sistemática con el de láminas que nombra la voz (lo comprobé sin escribir ninguna cifra). Que en la sesión 2 las láminas «son de la sesión de 11 a 15» es la fila de la tabla de `PREGUNTAS-7B.md` §1, no la clave. Riesgo que queda, en «Lo que no pude comprobar».
2. **Búsquedas sobre las filtradas**: las reproduje todas. Barrido v20 1-31: 49 líneas; por defecto: 0. Barrido v21 1-31: 160; por defecto: 22, de ellas 9 con mes en los minutos que da el informe. Todas las líneas con mes de v21 son de `[47:39]` en adelante, fuera de 0:00:00–0:47:39, y todos los días son de construcción. `grep` de «siempre|depende|solo en este caso|solo aquí» en v21 (solo número de línea y marca): 2 líneas, `[25:29]` y `[25:39]`, las dos dentro de 0:00:00–0:47:39, como dice el informe; las variantes con tilde dan 0. Las marcas `[CUARENTENA]` y `[NO CITABLE]` cuadran con §2.1 y §2.4. Ninguna cita del informe ni de la evidencia cae en un tramo. Las líneas de borde que se citan (`[14:49]`, `[30:14]`, `[37:39]`, `[44:06]`, `[49:18]` de v20, y `[47:39]` y `[73:33]` de v21) empiezan en el t1 del tramo o después, y con la regla de solape estricto (`evidence/verificacion.py:366-368`) no solapan. `[04:01]` y `[36:51]` no se citan. Las marcas `[10:44]`, `[10:49]`, `[13:13]`, `[13:25]`, `[37:06]`–`[37:37]` y `[25:29]` son referencias, no citas.
3. **Las 35 afirmaciones contra su cita** (24 de v20 y 11 de v21): las 30 que no salen en a1 y a2 dicen lo que dice su cita. Ninguna cita cae en un tramo (`knowledge validate` OK, y los t0-t1 a mano). Temas y tipos razonables. Los RULE_STATEMENT de correcciones que el informe marca como ejemplo siguen el precedente de la 7a (los 9 de `v19` del bloque).

#### Eje (b) · Encargo
Resumen: 0 bloquea, 1 importa, 2 menor. Requisitos: 31 hechos, 2 parciales, 0 no hechos.

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 1 | Base: main, origin, tag, CI, ninguna otra rama, hoja 08 | Hecho | Informe, «Base comprobada al abrir» |
| 2 | abrir-rama, encargo copiado, fila de HOLDOUT estadiada antes, tag libre | Hecho | 5fc0f9fd; G2 en cada sello |
| 3 | El corpus no es una unión (fsutil) | Hecho | :36-37 |
| 4 | Los días de grabación, `False`; desviación declarada | Hecho | §0.1, §0.3.1 |
| 5 | Los dos únicos vídeos sin registrar | Hecho | §0.2 |
| 6 | Las preguntas a Aleks antes del registro | Hecho | §0.3 |
| 7 | Contrastar a) y b) con la filtrada | Hecho | §3.0, §4.0; PARADA 1 (láminas abiertas por el trader: filtrada `[55:33]`, `[100:10]`) |
| 8 | `fuentes.yaml`: drive_id null, fecha, «sesion…», sin láminas ni carpetas | Hecho | diff de `fuentes.yaml` |
| 9 | `test_inventario` a v1..v21, inventory, `check --hashes` | Hecho | `range(1, 22)`; §1.3 (`check --hashes` no lo repetí) |
| 10 | Tests rotos a propósito y luego verdes; `reales` y sonda v22; el sintético intacto | Hecho | diff de tests; 55 puntos al repetirlos |
| 11 | Audio con las formas exactas, WAV fuera, cortes SIN AUDIO, puerta del ASR | Hecho | 15 tramos SIN AUDIO; §2.1, §2.4 |
| 12 | Transcripción con «listo»; cuarentena con el guion de `main`; commit propio por vídeo con `Fuente: ADR-0093` | Hecho | 66ea16bd y 565ea236 |
| 13 | Fotogramas: extract y check | Hecho | frames check OK (21) |
| 14 | Verificación final: solo `A` | Hecho | 39 `A` (el informe lo deja «en el resumen final») |
| 15 | Barrido de 1 a 31 y por defecto antes de leer | Hecho | reproducido |
| 16 | S-1 a S-7 con sus filas separadas | Hecho | §3.1-§3.7 (S-2, pregunta 1: ver a1) |
| 17 | S-1: el valor de `parametros.yaml` hacia :595 | Hecho | :319-322 |
| 18 | El bloque de días por sesión: día visible, lo marcado, correcciones con «Sirve a» y «¿siempre…?» | Hecho | §4.1-§4.6 |
| 19 | Cobertura en `###` sin «Tabla», antes de la tabla | Hecho | §5.2 |
| 20 | Tabla final: columnas, «Ambigüedad», A-16 fuera, veredicto lo primero, ningún `##` posterior con «Tabla» | Hecho | §6; las filas del bloque sin veredicto, como la 7a (`SESION-07-EXTRACCION.md:780-784`) |
| 21 | Verificar los cuatro tramos de `cobertura_material` y las ABIERTA en `ambiguedades.yaml` | Parcial | no consta en el informe (b1) |
| 22 | Los dos tests antes del primer sello del informe | Hecho | pasan (27 puntos); el informe remite al «resumen final» (b2) |
| 23 | Evidencia con `evidence new`, fuera de los tramos; contradictions y validate | Hecho | validate OK |
| 24 | `HOJA-USADA-7B.md`: la forma pedida, sin citas ni clave | Hecho | fichero leído entero |
| 25 | Recuadro de `PREGUNTAS-7B.md`, único cambio, ninguna línea con «**S-» | Hecho | diff: 5 líneas añadidas, que empiezan por «>» |
| 26 | Exposiciones: fila del primer día con «Escrita tarde» para el 20, y las del día | Hecho | diff de HOLDOUT |
| 27 | Cierre preparado: F (bytes), R4.3, copia de seguridad (bytes), ficheros fuera de git | Hecho | §9; 1169→1005 y 111, medidos |
| 28 | `PROJECT_STATE` < 24.900 y nada más que abrir-rama | Hecho | 24614; el diff es solo de abrir-rama |
| 29 | Push a `fix/sesion-08`, CI con solo el fallo esperado, número de run | Hecho | run 44957773501: único FAILED `test_state_check_ok_on_real_repo` («PROJECT_STATE declara la rama 'trabajo/sesion-08'; la rama actual es 'fix/sesion-08'») |
| 30 | Cada sello con su PICO DE MEMORIA en el informe | Parcial | falta el último (b3) |
| 31 | No se tocan spec, feedback, casos, motor, cifras, `SESION_EN_CURSO`, hoja de ruta ni `transcribir_sesion.py` | Hecho | diff vacío sobre esas rutas |
| 32 | Ningún fotograma abierto antes de situar el tramo | Hecho | según el informe; no verificable |
| 33 | PARADA final con lo que no cuadra | Hecho | §7.1 |

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| b1 | importa | El encargo pide «verifica los cuatro en el fichero» (`cobertura_material` de `knowledge/cases/kit/config.yaml`) y «verifícalo» (las ABIERTA de `ambiguedades.yaml`). El informe no registra ninguna de las dos verificaciones, y §11 no las lista. Las cuatro ambigüedades sí están abiertas: filas de A-13, A-35, A-48 y A-58 en Known Ambiguities de `PROJECT_STATE.md`, que `test_kit` ata a las abiertas. | `grep -n -E "cobertura_material\|config.yaml\|ambiguedades.yaml" SESION-08-EXTRACCION.md` → nada; `encargo:39`, `:72` |
| b2 | menor | Dos puntos de §11 dejan la evidencia «en el resumen final», fuera del informe: los dos tests de la tabla y la verificación de solo `A`. Los repetí: pasan, y salen 39 `A`. | `SESION-08-EXTRACCION.md:910`, `:916` |
| b3 | menor | El PICO DE MEMORIA del sello de 69ccd8a2 (árbol `ae14ead2…`, 317 MiB, `make-check.log`) no está en el informe. Cabe en el commit que pegue este informe. | `SESION-08-EXTRACCION.md:884-885`; `make-check.log` |

Lo que la rama hace sin que el encargo lo pida: la columna «Empieza (situada por la voz)» en `HOJA-USADA-7B.md` §5 y un guion fuera del repo que compara marcas con tramos. Los dos están declarados (este último en la fila de HOLDOUT, punto 5) y no pasan de ahí. Lo que el encargo dice que no se toca está intacto (fila 31).

#### Lo que no pude comprobar
- **Si `[27:19]`–`[27:54]` de v20 es todavía el esquema o ya un gráfico real.** De ahí salen `ev-v20-002737` y `ev-v20-002744`. La voz dice [fragmento de un tramo no citable, quitado al pegar], y el anuncio del gráfico real es en 0:28:00. Para decidirlo haría falta un fotograma, y no se abre ninguno.
- **El riesgo que queda con la clave**: el informe da el minuto en que empieza cada repaso de láminas (`[55:33]`, el final de `[79:03]`, `[100:10]`, 1:57:19). Lo commiteado no dice qué carpeta es qué sesión, pero esos instantes señalan fotogramas que están en esta máquina, fuera de git. No sé si en pantalla se ve el nombre de la carpeta: no abro fotogramas. Tampoco miré si la columna «Filas» de `PREGUNTAS-7B.md` §1, que está en `main` desde antes, tiene relación con el número de láminas; no es de esta rama.
- **La filtrada de v20 no tapa los siete tramos de precaución** (se añadieron después de generarla) y no va en orden cronológico: empieza por S-3 y S-4 y deja «SIN PREGUNTA» desde la l. 299. Quien la lea ahora ve el texto de los tramos sin tapar. Por eso me pasó lo de a3 (iii). Regenerarla con el guion de `main` los taparía; lo decide el consultor.
- Lo que hay dentro de los tramos no citables (las menciones del vídeo de mapeo, el desenlace de S-1, la sesión 1 entera): no lo leí, salvo lo de a3.
- `corpus check --hashes` (relee todos los vídeos, unos 98 GB) y `evidence contradictions` (escribe `_contradicciones.yaml`): no los lancé. Las sustituyen el informe §1.3 y §8 y la línea de `knowledge validate` «0 contradicciones abiertas».
- Que no se abriera ningún fotograma y que hubiera un «listo» antes de cada transcripción: no hay registro que consultar.
- Las crudas: no las leí.

#### Comandos ejecutados
1. `git branch --show-current`, `git merge-base main HEAD`, `git log --format='%h %s' main..HEAD`, `git diff --stat main...HEAD`, `git status --short`
2. Read: `docs/encargos/trabajo-sesion-08.md`, `contrato.yaml`, `docs/validation/SESION-08-EXTRACCION.md` (entero), `docs/sesion-7/HOJA-USADA-7B.md`, `docs/sesion-7/PREGUNTAS-7B.md:70-89,160-334`, `knowledge/spec/parametros.yaml:595-614`, `src/botsito/evidence/verificacion.py:340-399`
3. `git diff main...HEAD -- PREGUNTAS-7B.md HOLDOUT-EXPOSICIONES.md fuentes.yaml`; `git diff --cached -- HOLDOUT-EXPOSICIONES.md`; `git diff main...HEAD -- tramos_no_citables.yaml`; `git diff main...HEAD -- tests/ src/`; `git diff main...HEAD -- PROJECT_STATE.md`
4. `git diff --quiet main -- scripts/barrido_dias.py` (igual a `main`); grep de escrituras en el guion
5. `uv run python scripts/barrido_dias.py <v20 filtrada> --desde 1 --hasta 31`, y sin rango; lo mismo con v21 (la de 1 a 31, filtrada con `grep` a las líneas con mes)
6. `uv run python -c …` en memoria: `casos_ocultos` y `cargar_meses_reservados` contra `git log -p main..HEAD` y `git diff --cached` (fechas AAAA-MM-DD y días en palabras; solo recuentos)
7. `git log -p main..HEAD | grep` de láminas y carpeta; `git diff … | grep` de numeración de láminas
8. Grep `-o -n` de las marcas y las secciones de las dos filtradas; Read de la filtrada v20, l. 1-40 (las l. 10-22 caen en un tramo, por error: a3), 23-64, 80-297, 298-349, 489-512, 515-541, 566-599 y 689-696; de la filtrada v21, l. 435-1140
9. `grep -n -i -E "siempre|depende|solo en este caso|solo aqu"` sobre la filtrada v21, solo número de línea y marca; variante con tildes
10. `cat knowledge/evidence/v20/*.yaml`, `cat knowledge/evidence/v21/*.yaml`; grep del tema `punto_breaker_sin_vela_contraria`; recuento de `tipo` en `v19/ev-v19-01*`
11. `uv run python scripts/contrato_rama.py`
12. `git diff --name-status` sobre los regímenes de cambio y las rutas protegidas
13. `git log --format=… --stat main..HEAD | grep` de `Fuente:` y de tramos
14. `wc -c PROJECT_STATE.md`, `git show main:PROJECT_STATE.md | wc -c`, `sed -n 28p` y `138p | wc -c`, bytes de la F propuesta
15. `uv run pytest tests/unit/test_en_parte_no_se_cierra.py tests/unit/test_hoja_de_ruta.py -p no:cacheprovider -q`; `uv run pytest tests/unit/test_cuarentena.py tests/unit/test_inventario.py <los dos de test_guardia_claude> -p no:cacheprovider -q`
16. `uv run botsito corpus transcript check`; `uv run botsito corpus frames check`; `uv run botsito knowledge validate`
17. `grep` de SELLO, PICO, passed y G2 en `make-check.log`; `git rev-parse HEAD^{tree}`
18. `gh run view 44957773501 --json …`; `gh run view 44957773501 --log-failed | grep …`
19. Grep de `cobertura_material` en `knowledge/cases/kit/config.yaml`; grep de A-13, A-16, A-35, A-48, A-58 y A-20 en la tabla de `PROJECT_STATE.md`; grep de `orden_stop_punto` en `parametros.yaml` (rama y `main`); grep de A-16 en `PREGUNTAS-7B.md`
20. Negados por la guardia, no reescritos para esquivarla: un bucle `for c in $(git log …)` (sustituido por un único `git log --stat | grep`), un `awk` (sustituido por la tabla de `PROJECT_STATE.md`), un `xargs grep` y dos `pytest` en un mismo comando (una llamada por ejecutable, que es la forma que propone la guardia).
