# Las filtradas de sesión con los tramos no citables

Rama `trabajo/filtradas-con-tramos`, abierta el 2026-10-05 desde `main` en `0bf71a2` (commit de
estado sobre el merge `5e486dc`, tag `stable/F36x-filtradas-escenario-b`). Encargo:
`docs/encargos/trabajo-filtradas-con-tramos.md`, una tarea autónoma del consultor. Es el punto Q de
la Next Action.

En toda la rama no se lee ninguna cruda ni ninguna filtrada real. Todo se prueba con texto y
segmentos sintéticos, y el guion nuevo no se ejecuta sobre material real.

## 0. Fase 0

Todo se midió leyendo código y documentos del repositorio.

### 0.1 Dónde aplica hoy el guion la cuarentena

`scripts/transcribir_sesion.py`:
- **`procesar`:**
  1. lee los segmentos: de la cruda que ya existe, con `--solo-filtrar`, o del ASR, que la escribe
     antes;
  2. llama a `lineas_filtradas(segmentos, validos, meses_libres_del_repo())`;
  3. escribe la filtrada con `version_filtrada` y el registro con `registro_filtro`.

  Es la única función que escribe la filtrada (`_escribir(salidas["filtrada"], …)`).
- **`lineas_filtradas`:** aplica `botsito.corpus.cuarentena.en_cuarentena`, la regla por meses, y
  funde en una línea `[CUARENTENA mm:ss–mm:ss]` los segmentos seguidos en cuarentena de la misma
  pregunta.

**No aplica ningún tramo no citable.** Es el hueco de `FILTRADAS-ESCENARIO-B.md` §0.4.

### 0.2 Los segmentos: inicio y fin en milisegundos

- **`Seg(t0_ms, t1_ms, texto)`:** con ASR, sale de `fusionar(...).segmentos` del corpus; con
  `--solo-filtrar`, de las claves `t0_ms` y `t1_ms` de la cruda `.jsonl`. Son enteros en ms.
- **Reloj:** el audio que se pasa es el del vídeo, extraído sin recodificar.
  - En la sesión 4, la transcripción del guion dio «1914 segmentos, los mismos que la
    transcripción del corpus» (`SESION-04-EXTRACCION.md` §1.1).
  - En v9, el último segmento del bloque de 0:34:44 dio los mismos milisegundos en la cruda del
    guion y en la del corpus (`FILTRADAS-ESCENARIO-B.md` §4.1).
  - Así que los ms de los segmentos están en el reloj del vídeo, el mismo con el que se escriben
    los tramos (`t0`, `t1`, «h:mm:ss del video»).

**No salta la parada de «ms no fiables».**

### 0.3 Cómo se identifica el vídeo de cada sesión

- **El guion no lo sabe hoy.** Solo recibe `--audio` y `--sesion 02/03/04`, que elige la hoja de
  preguntas.
- **`--sesion` no basta, porque es ambiguo.** La sesión 02 tiene dos vídeos, v7 y v8, que se
  filtran los dos con `--sesion 02`. Los nombres de los audios (`sesion-02-v7`, `sesion-03`…) no
  son canónicos, y el manifiesto del corpus guarda el `.mp4` y no el `.m4a`.
- **La lista canónica de vídeos de sesión** está en la librería: `SESIONES_EN_CUARENTENA` (v7-v10)
  y `EXCEPCIONES` (v6), en `botsito.corpus.cuarentena`. `tests/unit/test_cuarentena.py` las vigila
  contra el manifiesto (toda sesión con `drive_id` nulo está en una o en otra).

**Decisión de diseño de esta rama, para la revisión del consultor:** el vídeo se identifica por
**declaración obligatoria**, `--video vN`, y el guion lo comprueba:
- `vN` tiene que ser un vídeo de sesión (`SESIONES_EN_CUARENTENA` o `EXCEPCIONES`);
- `--audio` tiene que dar **un solo** audio, porque un `--video` no puede valer para varios. Por
  ejemplo, la carpeta de la sesión 3 tiene además dos `.mp4` de WhatsApp, que el guion también
  tomaría por audios;
- sin `--video`, o con uno que no cumple esto, no escribe nada y sale con error.

Con eso la identificación no es ambigua. Si el consultor no lo considera suficiente, es la parada del
encargo («el vídeo de una sesión no se puede identificar sin ambigüedad»).

**Riesgo que queda:** declarar un vídeo equivocado que también sea una sesión. Un mismo audio no se
puede comprobar contra el manifiesto sin leer material: la duración del `.m4a` saldría de ffprobe
sobre el audio real, y en esta rama no se toca.

### 0.4 Cómo se leen los tramos

- **Fichero:** `knowledge/corpus/tramos_no_citables.yaml`, con una única clave `tramos`. Cada tramo
  lleva `video_id`, `t0`, `t1` (h:mm:ss, hasta tres decimales), `motivo` y `acordado`.
- **Función de la librería:** `botsito.corpus.cuarentena.cargar_tramos_no_citables(repo)`, que
  devuelve `video_id -> ((t0_ms, t1_ms, motivo), …)`, ordenados.
  - Valida la clave única, que la lista sea una lista y los cinco campos de cada tramo, que los
    tiempos se lean con `parse_ms` y que `t1 > t0`.
  - Lanza `TramosNoCitablesError` si no.
  - **Si el fichero no existe, devuelve `{}`, sin error.** El fallo cerrado lo tiene que poner el
    guion.
- **Ya existe una función que da los tramos de un vídeo:**
  `filtro_de(repo, video_id).tramos`, que es `cargar_tramos_no_citables(repo).get(video_id, ())`.
  El guion usa `cargar_tramos_no_citables`, la misma función que usan `knowledge validate`, la CLI y
  `filtro_de`; no lee el yaml por su cuenta.
- **La condición de «más de 0 ms» ya está escrita en la librería**, en `Filtro.motivos`:
  `s.t1_ms > a and s.t0_ms < b`, la misma que `tramo_no_citable` para los ítems.
  - `Filtro` no sirve tal cual: para un vídeo de `SESIONES_EN_CUARENTENA` tapa la sesión entera
    (`MOTIVO_SESION`), y no distingue meses de tramos.
  - El guion aplica esa misma condición y lo dice en su código.
  - No se añade una función pública a `corpus.cuarentena`, porque el encargo deja intacto ese
    módulo.

### 0.5 Paradas

Ninguna salta:
- los segmentos tienen ms fiables y en el reloj del vídeo;
- el vídeo se identifica sin ambigüedad con la declaración obligatoria (§0.3);
- no hace falta tocar `.claude/`, la guardia ni la regla de meses, ni leer material real.

## Estado

EN CURSO. Fase 0 hecha; sin paradas. Rama NO cerrada.
