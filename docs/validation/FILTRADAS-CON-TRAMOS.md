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

## 1. La regla, como quedó en el guion

`scripts/transcribir_sesion.py`; las funciones nuevas o cambiadas se nombran en cada punto:

- **Qué se tapa** (`tapados_por_tramos`): un segmento se tapa si se solapa **más de 0 ms** con algún
  tramo de **su** vídeo, es decir, si `s.t1_ms > t0 y s.t0_ms < t1`.
  - Es la condición de `Filtro.motivos` y de `tramo_no_citable` en la librería.
  - Un segmento que empieza justo donde termina un tramo, o que termina justo donde empieza, queda
    visible. Es el caso de borde de v9, 0:34:56, que es lo que pide el texto de Q.
- **La marca:** `[NO CITABLE mm:ss–mm:ss]`, distinta de `[CUARENTENA mm:ss–mm:ss]`, sin la clase ni
  el motivo del tramo.
  - Los tapados seguidos de la misma pregunta **y la misma marca** se funden en un bloque
    (`lineas_filtradas`, `Linea.marca`).
  - Un segmento que tapan las dos reglas va al bloque `[NO CITABLE]`, una sola vez, y cuenta en
    «ambos».
  - Un bloque de meses y uno de tramos seguidos quedan como dos bloques, cada uno con su marca.
- **De qué vídeo** (`tramos_del_video`, `--video`):
  - los tramos son los de `--video vN`, cargados con `cargar_tramos_no_citables`, la función de la
    librería;
  - `vN` tiene que ser una sesión (`SESIONES_EN_CUARENTENA` o `EXCEPCIONES`);
  - `--audio` tiene que dar un solo audio (§0.3).
- **Falla cerrado.** Sin `--video`, con un vídeo que no es una sesión, con más de un audio, o si
  `knowledge/corpus/tramos_no_citables.yaml` falta, no se puede leer o no valida, el guion **no
  escribe nada** y sale con 2.
  - No escribe ni la cruda: los tramos se cargan lo primero en `procesar`, antes del ASR.
  - `procesar` es la única función que escribe la filtrada, y su `video` por defecto es `None`,
    que falla.
- **El registro** (`registro_filtro`), sin texto:
  - «video: vN; tramos no citables del video: K»;
  - «segmentos tapados: solo por meses X, solo por tramos Y, por ambos Z»;
  - «bloques [NO CITABLE]: B»;
  - la línea de siempre, «segmentos en cuarentena: N en M bloques», que cuenta los segmentos de la
    regla de meses (los de «ambos» incluidos) y los bloques `[CUARENTENA]`.
- **Compatibilidad:**
  - `lineas_filtradas` y `registro_filtro` conservan sus argumentos de antes; los tramos entran
    por un argumento nuevo con valor por defecto, y sin él se comportan como antes;
  - los tests existentes de la cuarentena por meses (`test_transcribir_sesion.py`,
    `test_cuarentena.py`, `test_cuarentena_por_condicion.py`) pasan **sin cambiarse**, y el
    contrato los protege;
  - la regla de meses, `corpus.cuarentena` y `cases.holdout` no cambian.

## 2. Los tests

`tests/unit/test_filtradas_con_tramos.py`: 17 funciones, 27 casos, todo sintético. Los segmentos
los escribe el test. El fichero de tramos es el de un repositorio de juguete en `tmp_path`, salvo
un test que comprueba que el guion carga el del repositorio con la librería (solo tramos, ninguna
cruda). Cada uno con su negativo:

| Lo que pide el encargo | Test | El negativo dentro del test |
|---|---|---|
| solape de 1 ms: se tapa | `test_un_solape_de_1_ms_tapa` | — (es el propio negativo de los dos siguientes) |
| empieza justo en el fin del tramo: visible | `test_empieza_justo_en_el_fin_del_tramo_queda_visible` | el tramo 1 ms más largo sí lo tapa |
| termina justo en el inicio del tramo: visible | `test_termina_justo_en_el_inicio_del_tramo_queda_visible` | el tramo 1 ms antes sí lo tapa |
| el caso de borde de v9 (Q) | `test_el_caso_de_borde_de_v9_0_34_56` | el segmento oculto sí se tapa |
| la marca, sin texto, clase ni motivo; los contiguos se funden | `test_la_marca_no_lleva_texto_ni_clase_ni_motivo_y_los_contiguos_se_funden` | sin tramos, el texto sale |
| un tramo de otro vídeo no tapa nada | `test_un_tramo_de_otro_video_no_tapa_nada`, `test_main_con_el_video_equivocado_no_tapa_el_tramo_ajeno` | el mismo tramo, en su vídeo, sí tapa |
| tapado por meses y por tramo: «ambos», un solo bloque | `test_un_segmento_de_las_dos_reglas_cuenta_en_ambos_y_sale_una_vez` | con el tramo lejos del mes, «ambos» es 0 |
| el registro sin texto | `test_el_registro_no_trae_texto_ni_motivo` | — |
| fichero ausente, corrupto o que no valida; sin vídeo o con uno que no es sesión | `test_tramos_del_video_falla_cerrado` (7 casos), `test_main_falla_cerrado_y_no_escribe_nada` (5 casos: código distinto de 0 y la carpeta igual que antes) | `test_main_aplica_los_tramos_del_video`: con el fichero bueno, sí escribe |
| sin tramos no se transcribe ni se escribe la cruda | `test_main_sin_tramos_no_transcribe_ni_escribe_la_cruda` | — |
| un audio por ejecución | `test_main_se_niega_con_varios_audios` | — |
| ningún camino escribe sin tramos | `test_procesar_sin_video_falla_cerrado` | — |
| un vídeo de sesión sin tramos (v8) da una tupla vacía | `test_un_video_de_sesion_sin_tramos_da_una_tupla_vacia` | — |
| el guion usa la función de la librería | `test_el_repo_real_da_los_tramos_de_sus_sesiones` | — |

Los tests existentes de la cuarentena por meses pasan sin tocarse: los ejecutó la rama con
`tests/unit/test_transcribir_sesion.py`, `test_cuarentena.py`, `test_cuarentena_por_condicion.py`
y `test_tramos_de_sesion.py`.

## 3. Las roturas a propósito

Anexo: `docs/validation/anexos/FILTRADAS-CON-TRAMOS/roturas.py`, con la salida en
`roturas-SALIDA.txt`.
- Como escribe en el guion, se ejecutó en un **clon desechable** (`git worktree add`, con los dos
  ficheros sin commitear copiados), con la raíz por argumento y negándose a correr sobre el
  repositorio (`CLAUDE.md`, «Ensayos aislados»).
- Cada rotura cambia una línea, corre los tests nuevos, apunta los que caen y restaura el guion,
  comprobando su sha256 (`364c79e0…`, el del repositorio).
- El clon se quitó después.

| Rotura | Caen |
|---|---|
| 1. no se aplican los tramos | 4 (el borde de v9, la marca, `main`, «ambos») |
| 2. sin fichero de tramos se sigue | 3 (los dos `sin_fichero` y «sin tramos no transcribe») |
| 3. el borde se tapa (`>=` en lugar de `>`) | 7 (los dos bordes, el de v9, el registro, `main`, «ambos», el de otro vídeo) |
| 4. sin `--video` se sigue sin tramos | 3 (los dos `sin_video` y `procesar` sin vídeo) |

Restaurado, los 27 casos pasan, y el sha256 del guion es el de antes en las cuatro.

## 4. Decisiones y desviaciones, para la revisión del consultor

1. **El vídeo, por declaración obligatoria (`--video`)** (§0.3). El encargo pedía parar si el vídeo
   de una sesión no se podía identificar sin ambigüedad.
   - Con `--sesion` no se puede: la 02 son v7 y v8.
   - Con `--video`, comprobado contra la lista de sesiones de la librería y con un solo audio por
     ejecución, sí.
   - Lo decidió la sesión autónoma, sin el consultor.
   - Lo que queda abierto es declarar un vídeo de sesión equivocado. Un test documenta que entonces
     no se aplica el tramo ajeno.
2. **Un audio por ejecución.** Antes, `--audio <carpeta>` procesaba todos los audios de la carpeta.
   Ahora se niega si hay más de uno, porque cada audio lleva los tramos de su vídeo. La carpeta de
   la sesión 3 tiene, además del `.m4a`, dos `.mp4` de WhatsApp que el guion habría tomado por
   audios.
3. **Un segmento de las dos reglas va al bloque `[NO CITABLE]`.** El encargo pide que salga en un
   solo bloque, sin decir con qué marca. Se elige la de los tramos.
4. **La skill `ingerir-sesion`** (`.claude/skills/ingerir-sesion/SKILL.md`, paso 4) da el comando
   sin `--video`. Está en `.claude/`, que esta rama no toca: hay que añadirle `--video <vN>` en
   otra rama, o que lo haga Aleks. Hasta entonces, ese comando falla cerrado con «falta --video», y
   no escribe nada.

## 5. Lo que queda para después del merge, sin hacerlo

«En la fase 0 de la rama de activación de la sesión 4, rehacer con --solo-filtrar las filtradas de
v7–v10 y comprobar contra FILTRADAS-ESCENARIO-B.md que lo tapado es B más los tramos, que nada se
destapa frente a A dentro de un tramo y que los 12 casos del segundo de margen quedan tapados.»

Con el guion de esta rama hará falta `--video` en cada uno: `--video v7`, `v8`, `v9` y `v10`, con
`--sesion 02`, `02`, `03` y `04`.

## Estado

**Hecho el trabajo; falta la CI y el revisor.**
- Fase 0 sin paradas (§0).
- La regla, en el guion (§1); 17 tests sintéticos con sus negativos (§2) y cuatro roturas a
  propósito, que caen y se restauran (§3).
- Decisiones para el consultor (§4) y lo que queda para después del merge (§5).
- Ningún material real leído ni ejecutado.

**`PROJECT_STATE.md`:** 24.649 bytes, por debajo del tope de 25.000.

Rama NO cerrada.
