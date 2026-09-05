---
status: ACTIVE
date: 2026-09-05
phase: F05
---

# 0008 · Fotogramas: cobertura completa a 1 fps sin perdida, regla de seleccion por `pts` y manifiesto inmutable

## Decision
1. **Cobertura completa, no "tramos con decision".** Cada video del corpus se extrae entero a un
   fotograma por segundo. El plan (tabla A, H.2) preveia extraer solo tramos densos derivados
   de la transcripcion; se midio sobre las cuatro crudas `tr-*` que cualquier regla razonable de
   palabras clave marca entre el 46 % y el 99 % de cada video (ponderado por duracion, el ahorro
   de disco de filtrar seria del 7 % al 29 %) y que el unico tramo "sin decision" claro es la
   musica y el audio malo de V2 que F04 ya detecta. Instruccion del usuario (2026-09-05): maxima
   fidelidad sin restriccion de tiempo ni recursos.
2. **Sin perdida y bit a bit reproducible.** PNG con `-fflags +bitexact -flags +bitexact` (sin
   la etiqueta `Lavc`: el hash no depende de la version del codificador; si del decodificador
   H.264 de la build de ffmpeg, que se anota en el manifiesto). Medido en V3: 26 MiB por minuto
   de video, unos 7 GiB y 10 minutos estimados para los cuatro videos (real: 8,9 GiB y ~11 min);
   dos extracciones dan el mismo sha256.
3. **Regla unica de seleccion: "primer fotograma fuente con `t >= instante`".** Regulares en una
   pasada con `select='isnan(prev_selected_t)+gte(floor(t),floor(prev_selected_t)+1)'` y
   `-fps_mode passthrough`, que conserva el `pts` original; `showinfo` DESPUES de `select` da el
   `pts_ms` real de cada fotograma. Obligatorios con fraccion de segundo con `-ss <t> -copyts`
   (misma regla; sin `-copyts` el `pts` sale 0). Un obligatorio en segundo entero ES el regular
   (misma imagen, mismo hash). `fps=1` queda descartado: elige el fotograma en `n + 0,47 s`,
   reescribe el `pts` a `0, 1, 2...` y duplica fotogramas para rellenar saltos de la fuente,
   con lo que ni el `pts` ni los huecos serian verificables (medido en la revision de diseno).
4. **Indice y manifiesto.** `data/fotogramas/<video>/png-1fps[-<huella8>]/{<t_ms>.png,
   index.jsonl}` fuera de git (`n`, `t_ms` nominal, `pts_ms` real, fichero, sha256, bytes,
   origen). Manifiesto INMUTABLE `knowledge/corpus/fotogramas/fr-<video>-<hash8 del sha256 de
   index.jsonl>.yaml` (patron de F04/F15: hook, guardia de historial, `reemplaza_a`), con
   resolucion, build de ffmpeg, parametros, `ultimo_pts_ms`, `huecos` sobre `pts` consecutivos
   (> 2 s; el esquema los acepta como hecho medido, la aceptacion de F05 exige `[]`), `extra`
   (instantes con fraccion) y `sha256_index`. Exactamente una extraccion activa por video:
   extraer a otra carpeta (otros obligatorios, otra build) exige `reemplaza_a` = la activa; la
   huella de la carpeta lleva la build y los instantes extra, asi que una re-extraccion nunca
   pisa la anterior. `knowledge validate` lee `index.jsonl` (~2,5 MB en total), nunca hashea
   los 16 000 PNG; `corpus frames check` verifica por hash los extra y una muestra de 20.
5. **Obligatorios en lista mutable.** `knowledge/corpus/fotogramas_obligatorios.yaml`
   (`video_id`, `t`, `motivo`, `marca_heredada`) se valida contra el indice de la extraccion
   activa: anadir un instante en segundo entero no toca ningun manifiesto; uno con fraccion
   exige re-extraer con `reemplaza_a`. Contenido inicial: las tres marcas de F04 no
   verificables por audio (V3 0:28:56, V2 0:33:21, V4 0:12:30).
6. **Referencia citable** (F07): `fr-<id>/<t_ms>` (`t_ms` nominal, tiempo de video).
   `referencias_conocidas` = referencias de TODOS los manifiestos (activos o reemplazados: un
   item que cito uno reemplazado sigue siendo valido, el manifiesto es inmutable y no se borra)
   mas las rutas del corpus con papel `material_adicional`; lo heredado de Bot v2
   (`heredado_v2`) queda fuera. Hecho que sostiene la comparacion con `t0/t1` de la evidencia:
   `start_time = 0` en video y audio de los cuatro MP4, tasa constante (`r_frame_rate =
   avg_frame_rate`), `nb_frames` coherente con la duracion; el `t` del video y el `t_ms` de la
   cruda comparten origen. `evidence` y `corpus` son hermanos independientes en el contrato de
   capas: F07 anade el parametro a `validar_contra_manifiesto` y al `comprobar` de `evidence
   new`, alimentado desde `validation/knowledge.py`.

## Problema que resuelve
F07 necesita citar lo que se ve en pantalla (Excel, herramienta de posicion, caja, configuracion
del grafico para A-9) con la misma precision con la que F04 cita lo que se oye. Los fotogramas
heredados (29+118+78+113 con huecos de hasta 11 min) no cubren el corpus y no se citan. "Tramo
con decision" no tenia quien lo declarara (H.2) y la medida muestra que no filtra nada.

## Alternativas consideradas
1. Tramos densos por regla de palabras clave mas huecos heredados (el plan original).
2. Deteccion de escenas mas 1 fps en tramos (HTML original).
3. JPEG q=2 (legible, 159 KiB por fotograma) en lugar de PNG.
4. Filtro `fps=1` de ffmpeg.
5. Obligatorios dentro del manifiesto inmutable.

## Por que elegimos esta opcion
La cobertura completa elimina una frontera discutible por un coste medido pequeno; el PNG
elimina toda duda sobre cifras pequenas; la regla `select` es la unica que da `pts` reales y
huecos verificables; el manifiesto por fichero reutiliza las guardias que ya existen.

## Por que descartamos las demas
(1) y (2) ahorran 7-29 % y arriesgan que la evidencia caiga fuera del tramo. (3) Legible, pero
el usuario pidio maxima fidelidad sin restriccion de recursos. (4) Medido: fotograma equivocado y
`pts` reescrito. (5) Anadir un obligatorio en segundo entero obligaria a un manifiesto nuevo sin
que cambie ningun fotograma.

## Impacto
`src/botsito/corpus/{fotogramas,manifiestos_fotogramas}.py`, `src/botsito/cli.py` (`corpus
frames extract|check|show`), `src/botsito/validation/knowledge.py`, `src/botsito/comun/{ids,
historial}.py`, hook, `knowledge/corpus/{fotogramas_obligatorios.yaml,fotogramas/,README.md}`,
`tests/integration/` (estrenado). Cambio de plan: tabla A fila F05 y H.2 fila F05 en MASTER_PLAN.

## Fecha / fase
2026-09-05 · F05

## Estado
ACTIVE
