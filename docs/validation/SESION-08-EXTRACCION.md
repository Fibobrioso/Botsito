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

## Estado

EN CURSO.
