# FUNCTIONALITY VALIDATION REPORT · La cuarentena por defecto en la CLI

**Funcionalidad:** el I del Next Action: los comandos que ensenan contenido del corpus respetan por
defecto la cuarentena, los tramos no citables y el material reservado; el crudo, solo con `--crudo`,
que la guardia bloquea para Claude.
**Rama:** `trabajo/cuarentena-por-defecto`, desde `main` en `c95ab8b` (`stable/F36k-dieta-y-skills`).
**Encargo:** `docs/encargos/trabajo-cuarentena-por-defecto.md`. **Contrato:** `contrato.yaml`, riesgo
medio. No cambia motor, spec, knowledge, datos ni ninguna cifra.

## 0. Fase 0 · Inventario, ANTES de tocar codigo

Medido leyendo `src/botsito/cli.py`, `src/botsito/retrieval/`, `src/botsito/evidence/`,
`src/botsito/cases/holdout.py`, `scripts/transcribir_sesion.py` y `.claude/hooks/guardia.py`, sin
ejecutar ningun comando que imprima el corpus.

### 0.1 Las tres listas: de donde salen hoy

| Lista | Fuente en `src/` | Otras copias |
|---|---|---|
| (a) Sesiones en cuarentena (v7 en adelante) | **NINGUNA.** Ningun modulo de `src/` sabe que video esta en cuarentena | `.claude/hooks/guardia.py`, `Politica.sesiones_en_cuarentena`: los videos de `knowledge/corpus/fuentes.yaml` con `drive_id: null`, menos `SESIONES_SIN_CUARENTENA = {"v6"}` (constante del hook). Y la cuarentena POR SEGMENTO de `scripts/transcribir_sesion.py`, `en_cuarentena` (meses `MESES_FILTRADOS`, fechas, dia y numero, «backtest» con mes), que se aplica a la cruda de una sesion ANTES de escribir su version filtrada |
| (b) Tramos no citables | `knowledge/corpus/tramos_no_citables.yaml`, leido por `validation/contexto_evidencia.py:cargar_tramos_no_citables` y consultado por `evidence/verificacion.py:tramo_no_citable` | la guardia lo relee con su propio lector (`Politica.tramos`) |
| (c) Material reservado | `cases/holdout.py`: `casos_reservados(repo)` (los repartos commiteados) y `casos_ocultos(repo)` (reservados mas retirados) | la guardia: `Politica.reservados`, `meses_reservados` y `meses_legibles` (`MESES_DE_DESARROLLO` = 2026-01, 04 y 08, menos los que tengan un dia reservado); `tests/unit/test_guardia_claude.py` comprueba que ve lo mismo que `casos_reservados` |

### 0.2 Los comandos que ensenan contenido, y que filtran hoy

«Guardia» = lo para el hook de Claude Code antes de ejecutarse; el COMANDO no filtra nada. Para Aleks
en su terminal, sin hook, sale todo.

| Comando | Que imprime | (a) cuarentena v7+ | (b) tramos de v6 | (c) reservado | De donde sale el filtro |
|---|---|---|---|---|---|
| `kb find` | items de evidencia y segmentos de las crudas activas (y corregida y dudas) de TODOS los videos | **no** (guardia: bloquea sin `--video` o con `--video` en cuarentena) | **no** (guardia: bloquea si el intervalo pisa un tramo o no esta acotado) | **no**: un segmento que nombre un dia o un mes reservado sale | — |
| `kb at` | evidencia, cruda, fotograma y contradicciones alrededor de un instante | **no** (guardia) | **no** (guardia) | **no** | — |
| `corpus transcript show` | la cita literal de la cruda o la corregida entre `--t0` y `--t1` | **no** (guardia) | **no** (guardia) | **no** | — |
| `corpus frames show` | rutas de PNG y el segmento CRUDO que cubre el instante (`_segmento_en`) | **no** (guardia) | **no** (guardia) | **no** | — |
| `evidence propose --video --t0 --t1` | NO imprime: ESCRIBE en `knowledge/_proposals/` un esqueleto con los segmentos crudos del intervalo | **no**, y la guardia **tampoco** lo para: no esta en `CLI_QUE_IMPRIME_CRUDA` | **no** al escribir el esqueleto; `--check` rechaza solo el ITEM que cite un tramo | **no** | — |
| `feedback trace` | la cadena de registros de un objeto | n/a | n/a | **si**: oculta los casos reservados | `casos_ocultos` (`cli.py:1874-1883`) |
| `feedback pending` | id, accion, objetivo y motivo de los registros pendientes (sin el texto de la respuesta) | n/a | n/a | **no** filtra, pero no imprime el valor de ninguna etiqueta; hoy hay 0 `LABEL_CASE` | — |
| `motor visor` | una pagina HTML por dia (velas, trader, bot) en una carpeta ignorada | n/a | n/a | **si**: compuerta de construccion, codigo 3 si un dia esta oculto | `engine/arnes.py` con `casos_ocultos` |
| `motor arnes`, `kit *`, `fidelidad *`, `casos *` | informes y paquetes | n/a | n/a | **si**: la puerta de ADR-0033 y la compuerta del arnes | `cases/holdout.py` |
| `evidence list` | id, video, tiempos, modalidad, tipo y tema (sin cita) | n/a | n/a | n/a | — |

### 0.3 Lo que hay que decidir antes de escribir codigo

1. **La fuente de (a).** No hay ninguna en `src/`. Propuesta: un modulo nuevo
   `src/botsito/corpus/cuarentena.py` que la deduzca como la guardia (`drive_id: null` en
   `fuentes.yaml`, menos v6) y declare alli la excepcion de v6. La guardia corre con el Python del
   sistema y no puede importar `botsito`, asi que conserva su copia y un test comprueba que ve lo
   mismo, como ya se hace con `casos_reservados`. La alternativa -un campo en `fuentes.yaml`- toca
   `knowledge/`, que el encargo protege.
2. **Que es (c) en un texto.** El corpus no trae etiquetas por caso: lo reservado aparece como un
   segmento que nombra un mes o un dia. Propuesta: la MISMA regla por segmento que ya protege las
   sesiones, `en_cuarentena` de `scripts/transcribir_sesion.py`, movida a
   `src/botsito/corpus/cuarentena.py` para que el script y la CLI usen la misma (una sola fuente), y
   aplicada a todos los videos. Coste: ocultara tambien segmentos de v1 a v5 que nombren septiembre,
   marzo, mayo o febrero, aunque hablen de otra cosa. Se mide el recuento por video antes de
   decidir. La alternativa -calcular los meses no legibles desde `casos_reservados`- no tiene las
   grafias del ASR que `MESES_FILTRADOS` ya mide.
3. **`evidence propose`.** No imprime, pero copia segmentos crudos a un fichero del repositorio, y
   hoy nada lo para. Propuesta: el esqueleto se filtra igual que los comandos que imprimen.
4. **Lo que NO se filtra, por la funcion de Python.** `retrieval.consultas.buscar` y `en_instante`,
   `corpus.transcripcion.texto_entre`, `corpus.pipeline_transcripcion.cargar_cruda`, la verificacion
   de citas (`evidence/verificacion.py`, que tiene que ver la cruda para comprobar una cita),
   `scripts/transcribir_sesion.py` (la cuarentena de una sesion nueva) y los tests. El filtro va en
   la CLI; las funciones quedan como estan.

## Estado

FASE 0 ENTREGADA. Pendiente de la decision del consultor sobre §0.3 antes de escribir codigo.

## La skill `abrir-rama`, en su primer uso

Abrio esta rama y se quedo corta en un punto: no decia que el artefacto del contrato tiene que
estar estadiado ya en el primer commit, y `make check` lo exige (`contrato_rama.py`: «falta el
artefacto»). Corregido en la propia skill, pasos 4 y 7. Lo demas -base, encargo, contrato, Archivo 2
de `PROJECT_STATE.md` en HISTORIA y `state check` antes de sellar- fue tal cual. Tambien se apunto en
HISTORIA, como pedia el encargo, lo que quedo fuera del cierre de F36k (el «1 skipped» de
`make check` en `main`).
