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
  - En v9, las dos crudas no son iguales byte a byte (sha256 distinto), pero el bloque de 0:34:44
    son los segmentos 609-612 en las dos. Los milisegundos de la del corpus (fin del 612 en
    2.096.900; el 613 empieza en 2.098.060) casan **al segundo** con las marcas de la filtrada del
    guion (`34:56`, `[34:58]`) (`FILTRADAS-ESCENARIO-B.md` §3 y §4.1). Es coherencia al segundo, no
    igualdad de milisegundos: esta línea decía antes «los mismos milisegundos», y la cita no lo
    sostiene (revisor, A1).
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

**Riesgo que queda:** declarar un vídeo equivocado que también sea una sesión. Entonces se aplican los
tramos de otro vídeo, y un test lo documenta (`test_main_con_el_video_equivocado_no_tapa_el_tramo_ajeno`).

> **Corrección (revisor, B2).** Este párrafo decía que comprobar la declaración contra el manifiesto
> exigía leer la duración del `.m4a` con ffprobe. No es así: el manifiesto trae `duracion_s` de cada
> vídeo, y el guion tiene el `t1_ms` del último segmento sin leer ningún texto.
> - Esa comprobación es una opción para el consultor, y esta rama no la añade.
> - Solo cogería un vídeo declarado **más corto** que el audio.
> - Un límite inferior no sirve, porque v8 no tiene audio desde 40:00 y su último segmento queda
>   lejos del final.



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

**El recuento que pide Q** («el informe de Q da su recuento» de los segmentos visibles del segundo de
margen que la regla de más de 0 ms tapa):
- Lo medido hoy, por marcas, son **12 tramos** con una línea visible en su segundo de margen: 9 de
  tramos anteriores y 3 de la rama `trabajo/filtradas-escenario-b` (`FILTRADAS-ESCENARIO-B.md`
  §5.2).
- El recuento sobre las filtradas rehechas con este guion no se puede dar en esta rama, porque no
  se ejecuta sobre material real. Va en la fase 0 de la activación, que es la comprobación de
  arriba.
- Lo pidió el revisor (B1): la primera versión de este informe no lo daba.

Con el guion de esta rama hará falta `--video` en cada uno: `--video v7`, `v8`, `v9` y `v10`, con
`--sesion 02`, `02`, `03` y `04`.

## 6. Lo que se hizo con los hallazgos del revisor

| # | Gravedad | Qué se hizo |
|---|---|---|
| A1 | importa | **Arreglado.** El §0.2 decía que en v9 el último segmento del bloque dio «los mismos milisegundos» en las dos crudas. La cita no lo sostiene: las crudas difieren en sha256, y lo que casa son los índices 609-612 y los segundos de las marcas. Corregido. La parada de «ms no fiables» sigue sin saltar: los segmentos traen ms enteros, el audio es el del vídeo sin recodificar, en la sesión 4 salen los mismos 1914 segmentos que en el corpus, y en v9 casan los índices y los segundos. |
| A2 | menor | **Declarado.** «segmentos en cuarentena: N en M bloques» cuenta en N los de «ambos», y en M solo los bloques `[CUARENTENA]`. Se dejó así para no cambiar la línea de siempre; la línea nueva del desglose y la de «bloques [NO CITABLE]» lo completan (§1). |
| A3 | menor | **Declarado.** `lineas_filtradas` y `registro_filtro` tienen tramos vacíos por defecto, para que los tests de siempre no cambien. Las dos son puras y no escriben. La única que escribe, `procesar`, exige los tramos y falla cerrado. |
| A4 | menor | **Arreglado.** Los tests que borran o estropean el fichero de tramos lo piden a `_tramos_de_juguete`, que comprueba que `RAIZ` está parcheada y se para si no. Así nunca tocan el real. Los 27 casos siguen pasando. |
| B1 | importa | **Arreglado.** El §5 da el recuento que pide Q: 12 tramos, medidos por marcas, y la medida con el guion nuevo, en la activación. |
| B2 | importa | **Corregido y para el consultor.** El §0.3 decía que comprobar `--video` exigía ffprobe sobre el audio real. No es así: el manifiesto trae `duracion_s`. La comprobación queda como opción del consultor, con su límite (solo coge un vídeo declarado más corto). |
| B3 | menor | **Arreglado.** El Estado lleva la CI de Linux con su número de run. |
| (g) | opinión | **Para el consultor.** El revisor no ve el `--video` obligatorio como «sin ambigüedad lo que pide el encargo», sino como una decisión de diseño no pedida que trataría como parada parcial. El consultor elige: aceptar la declaración tal cual, añadir la comprobación de duración (B2) u otra identificación (§4.1). |
| (b) | dato | **Para el consultor.** Un fichero de tramos válido que no lista el vídeo declarado da 0 tramos y escribe la filtrada sin ninguno. Es lo correcto para v8, que no tiene tramos, y el registro lo dice («tramos no citables del video: 0»), pero en tiempo de ejecución no se distingue de un fichero al que le falta un vídeo. |

Tras el arreglo de A4 no se repitieron las roturas. El guion no cambió (su sha256 sigue siendo
`364c79e0…`), y los nombres de los tests, tampoco.

## Estado

**Lista para revisión, NO cerrada.**
- Fase 0 sin paradas (§0).
- La regla, en el guion (§1); 17 tests sintéticos con sus negativos (§2) y cuatro roturas a
  propósito, que caen y se restauran (§3).
- Decisiones para el consultor (§4, y el §6 con la opinión del revisor sobre `--video`); lo que
  queda para después del merge, con el recuento de Q (§5).
- El revisor y lo que se hizo con sus hallazgos (§6, «Informe del revisor»).
- Ningún material real leído ni ejecutado.

**CI de Linux** (`fix/filtradas-con-tramos`): run **216** (`37309388222`) sobre `bece406`. Falla
solo `tests/unit/test_cli.py::test_state_check_ok_on_real_repo`, el aceptado por el nombre `fix/`;
2004 pasan y 8 se saltan. La del commit de este informe va en la respuesta al consultor.

**Sellos:** `e9ce879` con `77a60a01…`; `bece406` con `6fa06dd6…` (2013 passed, pico 289 MiB).

**`PROJECT_STATE.md`:** 24.649 bytes, por debajo del tope de 25.000 (margen de 351 bytes: el cierre
tiene que sustituir, no añadir).

La fila de ERRORES-RECURRENTES va al cerrar, con los hallazgos del consultor.

## Informe del revisor

Subagente `revisor` (`.claude/agents/revisor.md`), lanzado con el informe terminado sobre `bece406`,
con las tres preguntas expresas del encargo y cinco más de la sesión. Pegado tal cual.

> ## Informe del revisor · trabajo/filtradas-con-tramos · 2026-10-05
>
> Rama `trabajo/filtradas-con-tramos` (HEAD `bece406`, base `0bf71a2` = `main`; el tag `stable/F36x-filtradas-escenario-b` apunta a `5e486dc`, `git rev-parse 'stable/F36x-filtradas-escenario-b^{commit}'`). Árbol limpio. Solo he leído código, tests, yaml del repo e informes; no he ejecutado el guion ni leído material real.
>
> ### Eje (a) · Reglas de la casa
>
> Resumen: 0 bloquea, 1 importa, 3 menor.
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | A1 | importa | La cita que sostiene «los ms de los segmentos son fiables» no dice lo que el informe le hace decir. El informe (§0.2, 2.º punto) afirma que en v9 el último segmento del bloque de 0:34:44 «dio los mismos milisegundos en la cruda del guion y en la del corpus (FILTRADAS-ESCENARIO-B.md §4.1)». Ese §4.1 dice lo contrario sobre las crudas: NO son iguales byte a byte (sha256 `dcd6e5bd…` frente a `d7464d30…`), el bloque se buscó «por sus marcas y no por su índice» y solo coincide el rango de índices 609-612; los 2.096.900 ms son de la cruda de `data/` que lee validate, no de la del guion, de la que solo hay marcas a segundo. Lo que sí se sostiene es el recuento (1914 segmentos «los mismos», `SESION-04-EXTRACCION.md:83`). Con eso se descartó la parada de «ms no fiables» (§0.2: «No salta la parada»): el hecho puede ser cierto, pero la evidencia citada no lo prueba. | `docs/validation/FILTRADAS-ESCENARIO-B.md:519-521` («tienen sha256 distinto»; «Las dos vías dan 609-612»), `:505-512` (los ms salen de `contexto.crudas`, la cruda de `data/`); `docs/validation/FILTRADAS-CON-TRAMOS.md` §0.2 |
> | A2 | menor | La línea del registro «segmentos en cuarentena: N en M bloques» deja de ser comparable con las de antes: N cuenta los segmentos de la regla de meses, «ambos» incluidos, pero M solo los bloques `[CUARENTENA]` (los de «ambos» están en bloques `[NO CITABLE]`). En el test: 3 segmentos «en 2 bloques» con uno en un tercer bloque. Está declarado (§1) y el test lo fija, pero un lector que lo compare con «45 segmentos en 12 bloques» (`SESION-04-EXTRACCION.md:84`) puede confundirse. | `scripts/transcribir_sesion.py` (`registro_filtro`, `bloques = … marca == CUARENTENA`); `tests/unit/test_filtradas_con_tramos.py:124`; informe §1 «El registro» |
> | A3 | menor | `lineas_filtradas(…, tramos=())` y `registro_filtro(…, no_citables=frozenset())` tienen valores por defecto «sin tramos» silenciosos. Hace falta para no tocar los tests existentes, y solo `procesar` escribe (y exige tramos), pero un llamador futuro de esas funciones no recibiría aviso. | `scripts/transcribir_sesion.py` (firmas de `lineas_filtradas` y `registro_filtro`); `_escribir` solo se llama en `procesar` (Grep: líneas 521, 532, 547, 556) |
> | A4 | menor | Los tests que borran/reescriben `m.RAIZ/knowledge/corpus/tramos_no_citables.yaml` (`unlink` en el test de `main_sin_tramos`, `write_text`/`unlink` en el parametrizado de fallo cerrado) solo son seguros porque el fixture `sesion` hace `monkeypatch.setattr(m, "RAIZ", repo)`. Funciona hoy (RAIZ es el repo de juguete de `tmp_path`), pero si ese fixture se rompiera, borrarían el yaml real. | `tests/unit/test_filtradas_con_tramos.py:221`, `:287-293`, `:314` |
>
> Comprobado sin hallazgos:
> - Contrato: `uv run python scripts/contrato_rama.py` → «CONTRATO: 9 ficheros dentro del contrato … 2 comprobaciones», exit 0. Los 9 ficheros del diff están en `rutas_permitidas`; ninguno en `rutas_protegidas` (`src/`, `knowledge/`, `.claude/` y los 4 tests existentes intactos). `pytest test_filtradas_con_tramos + test_transcribir_sesion + test_cuarentena -q`: todo en verde (sin ningún `F`); también pasan `test_cuarentena_por_condicion`, `test_tramos_de_sesion`, `test_project_state`, `test_historia`.
> - Sello de `make check`: `make-check.log` → `SELLO: … arbol 6fa06dd6e96623a575f909f29c2d2310a66c5a2c`, exit=0, `PICO DE MEMORIA … 289 MiB`; `git rev-parse 'HEAD^{tree}'` = `6fa06dd6…`: coincide. `uv run botsito state check` → OK.
> - Regímenes de cambio: `git diff --name-status main...HEAD`: solo `A` salvo `PROJECT_STATE.md`, `HISTORIA.md` y el guion (`M`). `HISTORIA.md`: 214 líneas añadidas, 0 borradas (`--numstat`). No se toca `knowledge/` → no hay trailer `Fuente:` que exigir, ni ambigüedades, ADR, informes cerrados ni citas con tres guardias.
> - Cifras: el guion no lleva cifras de negocio. Cuenta de tests de `PROJECT_STATE` 1278 → 1295 = 1278 + 17 funciones nuevas (`grep -c "^def test_"` = 17); `state check` lo confirma.
> - Informe existe, acaba en `## Estado`, y no declara ninguna lectura de material (así que no hace falta fila en `HOLDOUT-EXPOSICIONES`).
> - Citas del informe contra su fuente: 1914 segmentos (`SESION-04-EXTRACCION.md:83`) ✓; 612 termina en 2.096.900, 613 empieza en 2.098.060, tramo termina en 2.096.000 (`FILTRADAS-ESCENARIO-B.md:511-512`) ✓ (números del test coinciden); `filtro_de` = `cargar_tramos_no_citables(repo).get(video_id, ())` (`cuarentena.py:460-461`) ✓; `cargar_tramos_no_citables` devuelve `{}` sin fichero y valida lo que dice el informe (`cuarentena.py:128-158`) ✓.
> - Anexo de roturas: el sha256 `364c79e0…` de la salida es el del guion commiteado (`git show HEAD:scripts/transcribir_sesion.py | sha256sum`) ✓; las 4 listas de tests caídos y el recuento (4/3/7/3) coinciden con el informe §3; el anexo se niega a correr sobre el repo (`AQUI`).
> - `.git/worktrees` no tiene restos de esta rama (solo `wt-ci`, del 29-sep).
> - Commits: los dos llevan el cuerpo del mensaje; ninguna fila de `ERRORES-RECURRENTES` (aceptado: va al cerrar).
> - CI: run `37309388222` sobre `bece406` (HEAD): `1 failed, 2004 passed, 8 skipped`; el único fallo es `tests/unit/test_cli.py::test_state_check_ok_on_real_repo` (el aceptado, por el nombre `fix/`).
>
> ### Eje (b) · Encargo
>
> Resumen: 0 bloquea, 2 importa, 1 menor. Requisitos: 15 hechos, 1 parcial, 1 no hecho (más 1 «hecho de otra forma» declarado y 1 no comprobable).
>
> | # | Requisito | Estado | Evidencia |
> |---|---|---|---|
> | R1 | Comprobar `main` en `0bf71a2` y el tag en `5e486dc` | Hecho | `git rev-parse main` = `0bf71a26…`; tag^{commit} = `5e486dcd…` |
> | R2 | Rama abierta con la skill: encargo copiado, `contrato.yaml`, Archivo 15 de HISTORIA | Hecho | `docs/encargos/trabajo-filtradas-con-tramos.md`, `contrato.yaml`, `HISTORIA.md` +214/-0 |
> | R3 | Fase 0: dónde se aplica la cuarentena, ms de los segmentos, identificación del vídeo, lectura de tramos | Hecho | informe §0.1-§0.4 (con la debilidad de evidencia de A1 en «ms fiables») |
> | R4 | Fase 0: usar la función de la librería si existe, no una paralela | Hecho de otra forma, declarado | Carga con `cargar_tramos_no_citables` (no relee el yaml); la condición de solape se reescribe en `tapados_por_tramos` porque `Filtro` tapa la sesión entera en v7-v10 y no distingue meses de tramos (declarado en informe §0.4 y en el guion) |
> | R5 | Se tapa un segmento si se solapa >0 ms con un tramo de SU vídeo; el que empieza justo en el fin queda visible | Hecho | `tapados_por_tramos`: `s.t1_ms > a and s.t0_ms < b`; tests `:48-80` |
> | R6 | Marca `[NO CITABLE mm:ss–mm:ss]` sin clase ni motivo; bloques contiguos se funden | Hecho | `NO_CITABLE`, `Linea.marca`; test `:86-104` (con negativo) |
> | R7 | Falla cerrado: fichero ausente/ilegible/inválido → no escribe, sale con error | Hecho | `tramos_del_video` (`is_file` + `TramosNoCitablesError` → `SesionError`) y `procesar` lo llama lo primero; `main` → 2. Tests `:178-198`, `:268-299`, `:302-319` |
> | R8 | Registro con recuentos por separado: por meses, por tramos y por ambos, sin texto | Hecho | `registro_filtro`: «solo por meses X, solo por tramos Y, por ambos Z»; tests `:107-145` |
> | R9 | Test: solape de 1 ms tapa; empieza en el fin del tramo visible; termina en el inicio visible; cada uno con su negativo | Hecho | `:48-64` |
> | R10 | Test: un tramo de otro vídeo no tapa nada (con negativo) | Hecho | `:169-175`, `:259-265` |
> | R11 | Test: tapado por meses y por tramo cuenta en «ambos» y sale en un solo bloque | Hecho | `:107-134` |
> | R12 | Test: fichero ausente o corrupto → nada escrito y código ≠ 0 | Hecho | `:268-299` (compara el listado de la carpeta antes/después) |
> | R13 | Rotura a propósito, documentada y restaurada | Hecho (no reproducida por mí) | Anexo `roturas.py` + `roturas-SALIDA.txt`: 4 roturas, todas hacen caer tests y el sha vuelve. Mi Bash bloquea `git worktree` (solo lectura), así que no la reproduje; por lectura, la rotura 1 cubre `lineas_filtradas`, y quitar el paso de `tramos` desde `procesar` lo atraparía `test_main_aplica_los_tramos_del_video` (`:244-256`, `SECRETO` solo lo oculta el tramo) |
> | R14 | Los tests existentes de cuarentena por meses siguen pasando sin cambiarse | Hecho | `git diff main --stat -- tests` solo muestra el fichero nuevo; los 3 ficheros del contrato pasan |
> | R15 | Qué NO cambia: cuarentena por meses, `cases.holdout`, motor, spec, knowledge, tramos registrados, `.claude/`, hooks | Hecho | `git diff main --stat -- src tests .claude knowledge` → solo `tests/unit/test_filtradas_con_tramos.py` |
> | R16 | Informe: fase 0, regla, tests con roturas, desviaciones, tamaño de PS; lo que queda tras el merge, sin hacerlo | Hecho | `FILTRADAS-CON-TRAMOS.md` §0-§5 + Estado (24.649 bytes); §5 copia el texto del encargo |
> | R17 | Q: «el informe de Q da su recuento» de los casos del segundo de margen | No hecho | `grep recuento` en el informe: sin resultados; §5 solo repite «los 12 casos» como comprobación de después del merge |
> | R18 | Cierre: commit, push como `fix/`, CI con su número de run | Parcial | Commits y push hechos, CI de Linux medida (ver eje a); el informe aún no lleva el número de run (Estado dice «falta la CI»): `37309388222`, único fallo el aceptado |
> | R19 | Revisor con su informe pegado | Pendiente en el llamador | este documento; no lo pego yo |
> | R20 | Paso previo: tabla de minutos de Actions, fuera del repo | No comprobable | pertenece a la respuesta del agente; el diff no contiene nada de eso (correcto) |
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | B1 | importa | Q pide expresamente «el informe de Q da su recuento» de los casos en que la regla de >0 ms tapa el segmento visible del segundo de margen. El informe no da ningún recuento ni dice por qué no lo da. Sin material real no se puede medir ahora, pero sí se podía citar el de `FILTRADAS-ESCENARIO-B.md` (12 = 9 + 3, `:839`, `:861`) y declarar que la medición queda para la fase 0 de la activación (el §5 ya lo prevé, sin presentarlo como ese recuento). | `PROJECT_STATE.md:32` (texto de Q); `FILTRADAS-CON-TRAMOS.md` sin la palabra «recuento»; `FILTRADAS-ESCENARIO-B.md:839`, `:861` |
> | B2 | importa | La justificación de por qué no se puede verificar el `--video` declarado no se sostiene. El informe (§0.3, «Riesgo que queda») dice que comprobarlo contra el manifiesto exigiría ffprobe sobre el audio real. Pero el manifiesto trae `duracion_s` por vídeo (v7 4413,1; v8 7248,4; v9 6273,9; v10 7656,2 s; v6 8824,0) y el guion ya tiene `t1_ms` del último segmento, sin leer contenido. Eso no está descartado en el informe (ver opinión de (g)). Hoy un `--video` equivocado pero válido escribe una filtrada sin los tramos correctos (`test_main_con_el_video_equivocado…`, `:259-265`), que es justo lo que el encargo pide evitar («nunca escribe una filtrada sin aplicar los tramos»). | `knowledge/corpus/manifest.yaml` (`duracion_s` de v6-v10, leído con yaml); informe §0.3; test `:259-265` |
> | B3 | menor | El Estado del informe dice «falta la CI y el revisor» sin el número de run que pide el encargo. Se rellena con el run `37309388222` y el informe del revisor. | informe, `## Estado` |
>
> ### Respuestas a las preguntas expresas
>
> **(a) ¿La regla de >0 ms es la de Q y la de la librería?** Sí.
> - Q (`PROJECT_STATE.md:32`): «tapa un segmento solo si se solapa con el tramo más de 0 ms: un segmento que empieza exactamente donde termina un tramo queda visible».
> - Guion: `tapados_por_tramos` → `s.t1_ms > a and s.t0_ms < b`.
> - Librería: `Filtro.motivos` (`cuarentena.py:432`) usa literalmente `s.t1_ms > a and s.t0_ms < b`; `tramo_no_citable` (`verificacion.py:367`) usa `t0_ms < fin_ms and inicio_ms < t1_ms`. Es la misma desigualdad estricta en los dos sentidos: un extremo que toca el otro no solapa.
> - Matiz: `Filtro.motivos` solo llega a esa línea para vídeos fuera de `SESIONES_EN_CUARENTENA` (v6); para v7-v10 devuelve antes `MOTIVO_SESION` (`:428-429`). Por eso el guion repite la condición en vez de llamar a `Filtro` (declarado en §0.4).
> - Borde de v9 0:34:56: `test_el_caso_de_borde_de_v9_0_34_56` (`:67-80`) usa los ms de `FILTRADAS-ESCENARIO-B.md:511-512`: el segmento 2.090.000–2.096.900 solapa el tramo 2.084.000–2.096.000 y se tapa (`[NO CITABLE 34:50–34:56]`); el 2.098.060–2.100.240 queda visible (`[34:58] …`); un segmento que empieza justo en 2.096.000 no se tapa (negativo). Con tiempos exactos de la rotura 3 (`>=`/`<=`) caen 7 tests, incluidos los de borde.
>
> **(b) ¿Hay algún camino que escriba una filtrada sin aplicar los tramos?** No encontré ninguno que escriba sin haber cargado un fichero de tramos válido.
> - Único punto de escritura de salida: `_escribir`, llamado solo en `procesar` (cruda, cruda_txt, filtrada, registro). Grep sobre el guion (`write_text|write_bytes|open(|mkdir|unlink|replace|rename`): ninguna otra ruta de escritura. Ningún otro script ni `src/` importa o llama a `procesar`/`_escribir`; solo `tests/` lo cargan.
> - `procesar` hace `tramos = tramos_del_video(video, RAIZ)` en la primera línea ejecutable, antes de `salidas_de`, `mkdir` del trabajo, ASR y cualquier `_escribir`. Cubre modo ASR (no se escribe ni la cruda: `test_main_sin_tramos_no_transcribe_ni_escribe_la_cruda`) y `--solo-filtrar`.
> - `video=None` (por defecto de `procesar` y de `--video`) → `SesionError` (tests `test_procesar_sin_video_falla_cerrado`, `main[sin_video]`). `--video` fuera de `SESIONES_EN_CUARENTENA | EXCEPCIONES` → `SesionError` (`v99`, `v1`).
> - Fichero ausente: `cargar_tramos_no_citables` devolvería `{}`, pero `tramos_del_video` lo comprueba antes con `is_file()` → `SesionError` (la rotura 2, quitar esa comprobación, hace caer 3 tests). Corrupto / otra clave / `t1 <= t0` → `TramosNoCitablesError` → `SesionError`. Cualquier otra excepción (p. ej. `UnicodeDecodeError` es `ValueError`) sube a `main`, que la captura o aborta, con nada escrito todavía.
> - Carpeta con varios audios o sin audios: `main` lanza `SesionError` si `len(audios) != 1`; `audios_de` falla si no hay ninguno. `main` → 2 ante `SesionError`, `ValueError`, `RuntimeError`.
> - Casos que SÍ escriben una filtrada con 0 tramos o con otros (no son «sin cargar un fichero válido», pero conviene saberlos): (1) un fichero válido que no lista ese vídeo (p. ej. `tramos: []`, o un yaml truncado en un límite de tramo) → `.get(video, ())` = `()` → se escribe con 0 tramos; lo único que lo delata es la línea del registro «tramos no citables del video: 0» (para v9/v10 el repo real tiene 20 y 22, y un test, `:203-210`, lo exige, pero no es una comprobación de tiempo de ejecución); (2) un `--video` equivocado pero válido aplica los tramos de otro vídeo (documentado en el test `:259-265`; ver B2).
> - Comprobado por lectura y por los tests, no ejecutando el guion sobre material real.
>
> **(c) ¿Algún test lee material real?** No.
> - El módulo se carga con `importlib` desde `scripts/transcribir_sesion.py` (código, no datos).
> - Todos los tests puros (`:48-175`, `:178-199`) usan segmentos escritos en el test o un repo de juguete en `tmp_path`.
> - Fixture `sesion` (`:216-237`): repo de juguete, `m.RAIZ` parcheado a él, `codigos_validos` y `meses_libres_del_repo` parcheados (así no lee ni `knowledge/spec/ambiguedades.yaml` ni la partición reservada), y una cruda sintética + un `.m4a` vacío en `tmp_path/audio`. Los tests `main_*` y `procesar_*` solo tocan eso.
> - Único fichero real que toca algún test: `knowledge/corpus/tramos_no_citables.yaml`, en `test_el_repo_real_da_los_tramos_de_sus_sesiones` (`:203-210`, vía `RAIZ` real). Solo lee los tramos; ninguna cruda, filtrada, holdout ni fotograma. Las rutas `Path(` del test son solo `RAIZ` (línea 20). Los números del test del borde de v9 salen del informe `FILTRADAS-ESCENARIO-B.md`, no de la cruda.
> - Reserva: A4 (los `unlink`/`write_text` sobre `m.RAIZ` dependen del parche del fixture).
>
> **(d) ¿Los tests de cuarentena por meses cambian y pasan?** No cambian: `git diff main --stat -- tests` solo lista `tests/unit/test_filtradas_con_tramos.py` (+337). Pasan `test_transcribir_sesion`, `test_cuarentena` y los dos que el informe nombra de más (`test_cuarentena_por_condicion`, `test_tramos_de_sesion`).
>
> **(e) ¿La regla de meses (`src/`, `cases.holdout`) cambia?** No. `git diff main --stat -- src …` no muestra ningún fichero de `src/`; `git diff main --stat` completo: 9 ficheros, ninguno de `src/`, `knowledge/` ni `.claude/`.
>
> **(f) ¿Se sostienen las afirmaciones del informe (§0-§5)?** Sí, salvo la cita de «mismos milisegundos» en §0.2 (A1). Rutas, funciones (`tapados_por_tramos`, `tramos_del_video`, `Linea.marca`, `registro_filtro`, `procesar`), la marca, el recuento «17 funciones, 27 casos» (27 puntos de `pytest`) y las cuatro roturas (4/3/7/3, sha igual) coinciden con el código y con `roturas-SALIDA.txt`. No pude comprobar por mí mismo que la carpeta de la sesión 3 tenga dos `.mp4` de WhatsApp (§0.3, §4.2): listar esa carpeta es material real.
>
> **(g) Opinión sobre `--video` obligatorio.** No es «sin ambigüedad lo que pide el encargo», es una decisión de diseño razonable pero no pedida, y yo la trataría como parada parcial a decidir por el consultor:
> - El encargo dice «tramos de SU vídeo» y pide en la fase 0 «cómo se identifica el vídeo de cada sesión», con la parada «el vídeo de una sesión no se puede identificar sin ambigüedad». El propio informe concluye que con las entradas actuales NO se puede (`--sesion 02` son v7 y v8): la condición literal de parada se cumple para el guion tal como estaba, y el informe la resuelve añadiendo una entrada nueva, no con lo que ya hay.
> - El encargo no menciona `--video` ni «un audio por ejecución». La decisión la toma una sesión autónoma sin el consultor; está declarada (§0.3, §4.1-§4.2) con sus razones, no oculta. Efectos colaterales, también declarados: el comando de la skill `ingerir-sesion` (`.claude/skills/ingerir-sesion/SKILL.md:69`) falla cerrado hasta que se le añada `--video`, y `--audio <carpeta>` con varios audios deja de funcionar.
> - Lo que queda sin resolver es la VERIFICACIÓN de la declaración, y ahí hay una comprobación mecánica que el informe descarta con una premisa que no se sostiene (B2): el `t1_ms` del último segmento frente a `duracion_s` del manifiesto del vídeo declarado (las duraciones de v6-v10 difieren en más de 1000 s entre sí). Ojo: v8 (sin audio desde 40:00) podría no llegar a su duración, así que la tolerancia no es trivial; es una opción, no lo decido.
> - Con cualquiera de las dos vías, el consultor debería poder elegir entre: (i) aceptar la declaración tal cual, con el riesgo declarado; (ii) añadir esa comprobación; (iii) otra identificación (p. ej. el nombre del audio). No se tocó la skill (correcto: `.claude/` es intocable en esta rama).
>
> **(h) Tamaño de `PROJECT_STATE.md`.** `wc -c` = 24.649 bytes < 25.000 (tope de `tests/unit/test_project_state.py`, que pasa). Margen: 351 bytes. El cierre reescribe «Current Feature», «Stable Main State» y el registro: conviene vigilarlo, 351 bytes es poco para un cierre que tiene que sustituir (no añadir) lo anterior.
>
> ### Veredicto
>
> Sin hallazgos que bloqueen. El guion cumple la regla de Q (condición idéntica a la de la librería, marca distinta, fusión, recuentos por separado), falla cerrado en todos los caminos de escritura que recorrí, los tests no leen material real y los de la cuarentena por meses no cambian. Contrato OK, sello de `make check` = `HEAD^{tree}`, CI de Linux con el único fallo aceptado (run `37309388222`).
>
> Antes de declararla lista conviene corregir o declarar: (1) A1, reescribir la afirmación de §0.2 sobre «los mismos milisegundos» (la cita dice que las crudas difieren en sha256) o aportar la medida que la sostenga; (2) B1, dar el recuento que Q pide (citar los 12 de `FILTRADAS-ESCENARIO-B.md` y decir que la medición real queda para la activación); (3) B2/(g), corregir la premisa de §0.3 sobre el manifiesto y dejar al consultor la decisión sobre `--video` y su posible verificación; (4) rellenar en el Estado el número de run y pegar este informe.
>
> ### Lo que no pude comprobar
> - Las roturas no las reproduje: el anexo escribe en el guion y mi Bash bloquea `git worktree` (solo lectura); lo comprobé leyendo `roturas.py`, su salida commiteada y los tests.
> - No ejecuté el guion sobre ninguna cruda ni audio (regla de lectura): el fallo cerrado está comprobado por tests sintéticos y por lectura de código, no de punta a punta con material real.
> - La afirmación de que la carpeta de la sesión 3 contiene dos `.mp4` de WhatsApp (informe §0.3, §4.2): es una lista de un directorio con material real.
> - La tabla de minutos de Actions (paso previo del encargo): fuera del repo y de mi alcance.
> - Que el sha256 `364c79e0…` fuera el del guion en el clon de la ejecución original: solo puedo comprobar que coincide con el commiteado en HEAD.
>
> ### Comandos ejecutados
> 1. `git branch --show-current`; `git merge-base main HEAD`; `git log --format='%h %s' main..HEAD`; `git diff --stat main...HEAD`; `git status --short`; `git diff --name-status main...HEAD`
> 2. `cat docs/encargos/trabajo-filtradas-con-tramos.md`; `cat contrato.yaml`
> 3. `uv run python scripts/contrato_rama.py`
> 4. `git diff main -- scripts/transcribir_sesion.py`; `git diff main -- PROJECT_STATE.md`; `wc -c PROJECT_STATE.md`; `tail -5 make-check.log`; `git rev-parse 'HEAD^{tree}'`
> 5. Lecturas: `docs/validation/FILTRADAS-CON-TRAMOS.md`, `tests/unit/test_filtradas_con_tramos.py`, `scripts/transcribir_sesion.py` (380-630), `src/botsito/corpus/cuarentena.py` y `src/botsito/evidence/verificacion.py` (Grep), `FILTRADAS-ESCENARIO-B.md`, `SESION-04-EXTRACCION.md`, anexos `roturas.py` y `roturas-SALIDA.txt`
> 6. `uv run pytest tests/unit/test_filtradas_con_tramos.py tests/unit/test_transcribir_sesion.py tests/unit/test_cuarentena.py -q`; `git diff main --stat -- src tests .claude knowledge`; `git diff main --stat`
> 7. `grep -c "^def test_" tests/unit/test_filtradas_con_tramos.py`; `uv run pytest` sobre los tests nuevos y `test_cuarentena_por_condicion`, `test_tramos_de_sesion`, `test_project_state`, `test_historia`
> 8. Grep sobre el guion, `src/`, `tests/`, `scripts/`, `.claude/`, `docs/runbooks/` y `PROJECT_STATE.md` para las rutas de escritura y los llamadores
> 9. `git diff --numstat main...HEAD -- docs/state/HISTORIA.md`; `uv run botsito state check`
> 10. `git show HEAD:scripts/transcribir_sesion.py | sha256sum`; `git log -3 --format=…`
> 11. `uv run python` con `cargar_tramos_no_citables` (recuento de tramos por vídeo: v6 4, v7 1, v9 20, v10 22) y con `yaml` sobre `manifest.yaml` (duraciones v6-v10)
> 12. `git rev-parse 'stable/F36x-filtradas-escenario-b^{commit}' main`; `ls .git/worktrees`; `cat .git/worktrees/wt-ci/gitdir`
> 13. `gh run list --branch fix/filtradas-con-tramos --limit 3 --json …`; `gh run watch 37309388222`; `gh run view 37309388222 --log-failed`
> 14. Bloqueados (no los rodeé): `git worktree add` y `git worktree list` (hook de solo lectura del revisor); un `grep -r .` y un bucle con `$VAR` (guardia de Claude Code)
