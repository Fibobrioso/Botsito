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

## 1. Las decisiones del consultor sobre §0.3

Copiadas tal cual en `docs/encargos/trabajo-cuarentena-por-defecto.md`, «Segunda orden». En corto:
(1) `src/botsito/corpus/cuarentena.py` con una LISTA EXPLICITA de sesiones en cuarentena y la
excepcion de v6 con su motivo; la deduccion por `drive_id: null` pasa a test cruzado; (2) la regla
por segmento `en_cuarentena` se muda a `src/` y se aplica a todos los videos, con el recuento por
video en el informe; (3) `evidence propose` filtra, y se auditan las propuestas existentes sin
tocarlas; (4) el filtro va EN LAS FUNCIONES, con `crudo=True` solo para la verificacion de citas,
`scripts/transcribir_sesion.py` y los tests, un test que lo vigila y la guardia que lo bloquea.

## 2. Lo que se construyo

**`src/botsito/corpus/cuarentena.py`, la UNICA fuente** de las tres reglas:
- (a) `SESIONES_EN_CUARENTENA = {v7, v8, v9}` y `EXCEPCIONES = {v6: motivo}`;
  `problemas_de_la_lista` la cruza con `fuentes.yaml` (`test_la_lista_cuadra_con_fuentes`, contra el
  repositorio real, y `test_la_comprobacion_de_la_lista_no_es_decorativa`). La guardia guarda su
  copia -la deduce de `fuentes.yaml`- y `test_la_guardia_y_el_modulo_dicen_la_misma_cuarentena`
  comprueba que dicen lo mismo sobre el repositorio real.
- (b) `cargar_tramos_no_citables`, que BAJA aqui desde `validation/contexto_evidencia.py` (que lo
  sigue exportando con los mismos nombres) para que `retrieval` y la CLI lo lean de la misma fuente.
  Lee los tiempos con `corpus.transcripcion.parse_ms` y no con `evidence.modelo.parse_tiempo`,
  porque `corpus` no importa `evidence` (capas hermanas): el formato es el mismo salvo que admite
  hasta tres decimales, y el fichero real no usa ninguno.
- (c) `normalizar`, `numeros_a_cifras`, `MESES_FILTRADOS`, `motivos_cuarentena` y `en_cuarentena`,
  MUDADOS TAL CUAL desde `scripts/transcribir_sesion.py` por un guion (117 lineas), que ahora los
  importa de aqui; sus tests van tambien a la fuente nueva.
- `Filtro`, uno por video, con prioridad a > b > c: aplica las reglas y anota lo que oculta
  (`Oculto`: video, numero, tiempos y motivo, NUNCA texto); `resumen` lo dice en una linea, solo con
  numeros y motivos.

**Las funciones filtran por defecto, y sin filtro fallan** (en vez de devolver el crudo):
`cargar_cruda`, `cargar_corregida` y `cargar_capas` (`corpus/pipeline_transcripcion.py`, con la regla
sobre la cruda Y la corregida: un segmento se oculta en las dos capas si lo pide cualquiera; una
corregida ilegible no impide filtrar con la cruda), `texto_entre` (`corpus/transcripcion.py`),
`construir_indice`, `buscar` y `en_instante` (`retrieval/`: el indice se construye filtrado salvo con
`crudo=True`, la consulta exige el mismo modo, y `Respuesta.ocultos` dice que segmentos del alcance
de la consulta quedaron fuera). La evidencia NO se filtra: un item ya paso la guardia de tramos y la
revision del consultor, y los de la sesion 3 (v9) son citas de su version filtrada.

**La CLI**: `kb find`, `kb at`, `corpus transcript show` y `corpus frames show` ganan `--crudo` y
terminan con la linea `OCULTOS: N segmentos: ... (a|b|c)` cuando ocultan algo (en `--json`, por
stderr). `evidence propose` filtra SIEMPRE, sin `--crudo`, porque escribe en el repositorio.

**La guardia** (`R_CRUDO`): bloquea cualquier comando Bash o PowerShell -y el codigo de `python -c`,
de un heredoc o de un guion nuevo- que lleve `--crudo` (o su abreviatura hasta `--cr`, que argparse
aceptaria) o `crudo=` con un valor que no sea `False` (o la clave `"crudo"` de un dict). Deja pasar
`make check` (solo con su redireccion a un fichero) y `pytest` sin argumentos.

> **CORRECCION (2026-10-01, misma rama, tercera orden del consultor).** Este parrafo decia que las
> reglas viejas -bloquear `kb find` sin `--video`, los videos en cuarentena y los intervalos que
> pisan un tramo- se quedaban como estaban. La tercera orden quito la primera y mantuvo las otras
> dos como segunda capa: lo vigente esta en §9.5.

### 2.1 Los llamadores que piden el contenido sin filtrar

| Llamador | Como | Por que |
|---|---|---|
> **CORRECCION (2026-10-01, misma rama, tercera orden del consultor).** La primera version de
> esta tabla ponia `corpus glossary apply` con una funcion interna que leia la cruda sin
> `crudo=True` (`regenerar_corregida`). El consultor no la acepto: era una via que el test de
> autorizados no veia. Ya no existe; la tabla de abajo es la vigente, y §9 cuenta el cambio.

`AUTORIZADOS`, en `tests/unit/test_cuarentena.py`, por (fichero, funcion) y con su motivo:

| Llamador | Como | Por que |
|---|---|---|
| La verificacion de citas (`validation/contexto_evidencia.py`, `crudas`) | `cargar_cruda(..., crudo=True)` | compara la cita con la cruda entera; no devuelve su texto |
| `corpus glossary apply` (`cli.py`, `corpus_glossary_apply`) | `cargar_cruda(..., crudo=True)` | la corregida se recalcula desde la cruda ENTERA (ADR-0007): filtrada, se corromperia. Por orden del consultor |
| `corpus transcript check` (`corpus/manifiestos_transcripcion.py`, `comprobar`) | `cargar_cruda(..., crudo=True)`, y lee la corregida para compararla con cruda + glosario | la integridad recalcula los recuentos del manifiesto sobre la cruda entera. **Anadido en esta rama con su motivo: lo decide el consultor (§9)** |
| `scripts/transcribir_sesion.py` (el fichero) | autorizado; hoy no lo necesita (lee su propia cruda fuera del repositorio) | es la cuarentena de una sesion nueva |
| Los tests | `crudo=True` en sus llamadas directas | datos sinteticos |

El sha de la cruda se calcula con `pipeline_transcripcion.sha256_de_cruda`: hashear no es leer su
contenido (CLAUDE.md). `make check` no necesita nada sin filtrar fuera de los tests. Los vigilan
dos tests sobre `src/` y `scripts/`: `test_crudo_true_solo_en_los_llamadores_autorizados` (un
`crudo=` que no sea `False` ni el reenvio de un parametro o de un atributo, salvo `True` en una
funcion autorizada) y `test_nadie_lee_la_cruda_sin_pasar_por_las_funciones_que_filtran` (construir
la ruta de la cruda o de la corregida para algo que no sea preguntar si existe, o parsearla con el
`desde_jsonl` de las transcripciones, fuera del modulo que implementa las funciones y de los
autorizados). `test_los_recorridos_no_son_decorativos` rompe los dos a proposito.

### 2.2 Cambios que no estaban en el encargo, declarados

- El texto del motor de ASR falso de los tests (`corpus/transcripcion.py`, `MotorFalso`) pasa de
  «texto falso 0-1 de …» a «texto falso 0 a 1 de …»: «0-1» es una fecha numerica para la regla (c) y
  ocultaba el unico segmento de dos tests del pipeline. Ningun test dependia del formato.
- `contrato.yaml` gano `src/botsito/validation/contexto_evidencia.py` (la reexportacion y el
  `crudo=True` de la verificacion) y `docs/validation/anexos/CUARENTENA-POR-DEFECTO/` (el recuento).
- `CLAUDE.md` y la skill `ingerir-sesion` dicen ya que la CLI filtra; la skill gana el paso «anadir
  el video a la lista de cuarentena».

## 3. La tabla de la Fase 0, despues

| Comando | (a) cuarentena v7+ | (b) tramos de v6 | (c) reservado | Con `--crudo` |
|---|---|---|---|---|
| `kb find` | **si**, por defecto (`buscar`, indice filtrado) | **si** | **si**, en los segmentos | lo muestra (solo Aleks) |
| `kb at` | **si** (`en_instante`) | **si** | **si** | lo muestra |
| `corpus transcript show` | **si** (`cargar_cruda`/`cargar_corregida` y `texto_entre`) | **si** | **si** | lo muestra |
| `corpus frames show` | **si**, el segmento (`_segmento_en`) | **si** | **si** | lo muestra |
| `evidence propose` | **si**, siempre | **si**, siempre | **si**, siempre | no tiene: escribe en el repositorio |
| `feedback trace`, `motor visor`, `motor arnes`, `kit`, `fidelidad`, `casos` | como antes | como antes | **si**, como antes | — |

Todas leen las listas de `botsito.corpus.cuarentena`; ninguna las copia.

## 4. Cuanto oculta, por video

Medido con `docs/validation/anexos/CUARENTENA-POR-DEFECTO/recuento.py`, que lee por las mismas
funciones filtradas y solo cuenta (2026-10-01; segmentos de la cruda activa):

| Video | Segmentos | (a) | (b) | (c) | Ocultos | % |
|---|---|---|---|---|---|---|
| v1 | 405 | 0 | 0 | 0 | 0 | 0.0 % |
| v2 | 806 | 0 | 0 | 3 | 3 | 0.4 % |
| v3 | 1020 | 0 | 0 | 3 | 3 | 0.3 % |
| v4 | 1625 | 0 | 0 | 26 | 26 | 1.6 % |
| v5 | 80 | 0 | 0 | 0 | 0 | 0.0 % |
| v6 | 2146 | 0 | 118 | 69 | 187 | 8.7 % |
| v7 | 602 | 602 | 0 | 0 | 602 | 100.0 % |
| v8 | 229 | 229 | 0 | 0 | 229 | 100.0 % |
| v9 | 1664 | 1664 | 0 | 0 | 1664 | 100.0 % |

Cada segmento cuenta una vez, por el primer motivo (a > b > c); la (c) incluye el segmento anterior
y el siguiente de cada uno que dispara la regla, como en las sesiones.

## 5. La auditoria de `knowledge/_proposals/`

25 ficheros. **10 tienen segmentos que hoy caerian en (b) o (c); ninguno en (a).** No se han
borrado ni editado. Solo cuentas y nombres:

| Fichero | Segmentos | (a) | (b) | (c) |
|---|---|---|---|---|
| pr-v2-002400-003830-e923632f.yaml | 153 | 0 | 0 | 3 |
| pr-v3-001300-002600-7f79833c.yaml | 141 | 0 | 0 | 3 |
| pr-v4-000000-000500-28a0de27.yaml | 51 | 0 | 0 | 6 |
| pr-v4-003000-004500-c2b977e5.yaml | 272 | 0 | 0 | 5 |
| pr-v4-004500-010000-c2b977e5.yaml | 215 | 0 | 0 | 6 |
| pr-v4-010000-011500-fee495dc.yaml | 298 | 0 | 0 | 3 |
| pr-v4-011500-013336-fee495dc.yaml | 341 | 0 | 0 | 6 |
| pr-v6-005000-010000-216cbc85.yaml | 194 | 0 | 7 | 3 |
| pr-v6-010800-011030-cc689b83.yaml | 43 | 0 | 0 | 3 |
| pr-v6-014500-014700-e29045ea.yaml | 35 | 0 | 0 | 3 |

**Orden del consultor: «si hay alguno, para y avísame».** La rama se para aqui (§8).

## 6. Tests

`tests/unit/test_cuarentena.py` (25 casos, todo sintetico): la lista contra `fuentes.yaml` y su
version rota; el filtro con las tres reglas y su prioridad; el aviso sin contenido (el propio aviso
no dispara la regla c); las funciones que fallan sin filtro; y, para cada comando del inventario, que
por defecto oculta un segmento de cada tipo y que `--crudo` lo muestra (`evidence propose`, que no
tiene `--crudo`, solo lo primero). La (a) se prueba poniendo v1 en la lista con `monkeypatch`; la
(c), con un segmento que nombra un mes SIN dia. `tests/unit/test_guardia_claude.py`: la guardia
bloquea `--crudo` al principio, al final, con `=`, con un valor, abreviado, en `python -c`, en un
heredoc, por diccionario, en un guion nuevo y en PowerShell, y deja pasar los mismos comandos sin la
opcion, `make check` y `pytest`. Ajustados para pedir `crudo=True` (son llamadores autorizados):
`test_transcripcion`, `test_pipeline_transcripcion` y `test_cli`; y `test_transcribir_sesion` mira
la regla en su fuente nueva.

## 7. Lo que debe decidir el consultor

1. **Los 9 items de evidencia de §9.3**, que citan un segmento que hoy se oculta por (c). No se ha
   tocado nada de `knowledge/`.
2. **`corpus transcript check` en `AUTORIZADOS`** (§2.1 y §9.1): se anadio con su motivo porque la
   integridad necesita la cruda entera; si no se acepta, hay que decidir como comprueba el
   manifiesto.
3. **`scripts/a18_buscar.py` filtrado** (§9.1): con el filtro, las cuatro salidas commiteadas de
   las busquedas de A-18, A-24, A-35 y la sesion 02 ya no se reproducen byte a byte (mismos
   pasajes, menos lineas). La alternativa es autorizarlo con `crudo=True`.

## La skill `abrir-rama`, en su primer uso

Abrio esta rama y se quedo corta en un punto: no decia que el artefacto del contrato tiene que
estar estadiado ya en el primer commit, y `make check` lo exige (`contrato_rama.py`: «falta el
artefacto»). Corregido en la propia skill, pasos 4 y 7. Lo demas -base, encargo, contrato, Archivo 2
de `PROJECT_STATE.md` en HISTORIA y `state check` antes de sellar- fue tal cual. Tambien se apunto en
HISTORIA, como pedia el encargo, lo que quedo fuera del cierre de F36k (el «1 skipped» de
`make check` en `main`).

## 8. Estado

**PARADA, por orden del consultor, antes de declarar la rama lista**: la auditoria de §9.3 encontro
9 items de evidencia vivos que citan un segmento que hoy se oculta por (c). El resto de la tercera
orden esta hecho y sellado; la CI de Linux y el revisor, en §10 y §11.

## 9. La tercera orden del consultor (2026-10-01)

Copiada tal cual en `docs/encargos/trabajo-cuarentena-por-defecto.md`, «Tercera orden».

### 9.1 Punto 0: ninguna lectura de la cruda sin pasar por `crudo=True`

- **`corpus glossary apply`** pasa a `cargar_cruda(carpeta, crudo=True)` y entra en `AUTORIZADOS`
  con su motivo. La funcion interna `regenerar_corregida` ya no existe.
- **Comprobado en todo `src/` y `scripts/`** con la busqueda de `cruda.jsonl`, `FICHERO_CRUDA` y
  `desde_jsonl`. Habia dos lecturas mas sin pasar por `cargar_cruda`:
  - `corpus transcript check` (`manifiestos_transcripcion.comprobar`) leia los bytes de la cruda
    para el sha y los parseaba para recalcular el manifiesto. Ahora hashea con `sha256_de_cruda` y
    lee con `cargar_cruda(carpeta, crudo=True)`; entra en `AUTORIZADOS` con su motivo, y queda a
    decision del consultor (§7).
  - `scripts/a18_buscar.py`, `leer` (que usa tambien `scripts/buscar_ambiguedades.py`), abria
    `cruda.jsonl` y lo parseaba a mano. Ahora hashea con `sha256_de_cruda` y lee FILTRADO, con
    `cargar_cruda(carpeta, filtro_de(...))`; no se anade a `AUTORIZADOS`. Medido con sha256, sin
    leer contenido: antes del cambio las cuatro salidas se reproducian byte a byte (A-18, A-24,
    A-35 y sesion 02); despues, ninguna. Tienen los MISMOS bloques -42, 44, 10 y 47 pasajes- y 50,
    9, 9 y 11 lineas menos: los segmentos que ahora se ocultan dentro de los pasajes. Decision
    del consultor (§7).
- **Lo vigila un test nuevo**, `test_nadie_lee_la_cruda_sin_pasar_por_las_funciones_que_filtran`
  (§2.1), y la lista de autorizados pasa a ser por (fichero, funcion) en vez de por fichero.

### 9.2 Punto 1: las propuestas con segmentos ocultos no se leen

- `cuarentena.propuestas_con_ocultos` CALCULA la lista; `scripts/propuestas_con_ocultos.py
  --escribir` la vuelca a `.claude/hooks/propuestas_con_ocultos.txt`, que lee la guardia (no
  importa `botsito`); `test_la_lista_de_la_guardia_es_la_que_se_calcula` falla si no coincide. Hoy:
  las mismas 10 de §5. La guardia las bloquea con `R_PROPUESTA_OCULTA`
  (`test_una_propuesta_con_segmentos_ocultos_no_se_lee`, sintetico), y mantiene como segunda capa
  su calculo propio de lo que pisa un tramo. No se ha borrado ni editado ninguna propuesta.

### 9.3 Punto 1: la auditoria de knowledge/

`docs/validation/anexos/CUARENTENA-POR-DEFECTO/auditoria_knowledge.py`: un item de evidencia cita
los segmentos de SU transcripcion que pisan su intervalo; sale si alguno lo oculta hoy el filtro
por (b) o (c). Una regla de la spec o un termino del glosario salen si su `cita` es uno de esos
items. Solo ids, video y motivo:

| Item | Video | Motivo | Vivo |
|---|---|---|---|
| ev-v2-002604-041288d7 | v2 | (c) | si |
| ev-v3-001952-a3276d86 | v3 | (c) | si |
| ev-v3-002026-fa5295fa | v3 | (c) | si |
| ev-v4-000016-8f6862dd | v4 | (c) | si |
| ev-v4-000052-61cf22a9 | v4 | (c) | si |
| ev-v4-000353-9ea3ce94 | v4 | (c) | si |
| ev-v4-004533-14f2b226 | v4 | (c) | si |
| ev-v4-012049-04c922c5 | v4 | (c) | si |
| ev-v6-014702-2d7096db | v6 | (c) | si |

9 de 437 items, ninguno por (b). **Ninguna regla de `strategy_spec.yaml` ni ningun termino de
`glossary.yaml` los cita** (0 de 44), y una busqueda de los nueve ids en `knowledge/spec/` no
devuelve nada. **Orden del consultor: «si sale algun caso, para y avísame antes de declarar la rama
lista».**

### 9.4 Un bloqueo de la guardia nueva, tal como se pidio

La guardia bloqueo un `cat >> docs/encargos/... <<'EOF'` que copiaba esta orden: su texto lleva
literalmente el parametro con `True`, y la orden pide bloquear los heredocs que lo contengan. No
se rodeo: el encargo se completo con la herramienta Edit, que escribe un documento y no ejecuta
nada. Es el coste conocido de buscar el texto en todo el comando: tampoco pasa un `git commit -m`
que lo nombre. Si el consultor quiere afinarla (solo en el codigo que va a Python), es una linea.

### 9.5 Punto 2: las reglas viejas de la guardia

- `kb find` SIN `--video` pasa: el indice que consulta sale filtrado.
- Siguen como segunda capa: `kb find --video v7` (una sesion en cuarentena), `kb at`,
  `transcript show` y `frames show` de una sesion en cuarentena, y los intervalos que pisan un tramo
  de v6. Lo comprueban `test_la_cli_pasa_salvo_lo_que_imprime_una_cruda` (con `kb find stop` ya en
  «pasa» y `kb find stop --video v7` en «bloquea») y los casos de v6 de siempre.

## 10. La CI de Linux

Regla de `RITUAL.md` (la rama toca un hook): empujada como `fix/cuarentena-por-defecto`.

| Commit | Run | Resultado |
|---|---|---|
| `e30765c` (tercera orden) | `36936326358` | 1 failed, 1768 passed, 8 skipped: solo el fallo esperado, `test_state_check_ok_on_real_repo` por el nombre `fix/` frente a `trabajo/` |

El run del commit que trae los arreglos del revisor (§11) se apunta en la respuesta: escribirlo
aqui exigiria otro commit y otro run.

## 11. Informe del revisor

Subagente `revisor`, sobre `e30765c`. Los hallazgos (A1, A2, B1 a B4), tal cual; la tabla de
requisitos del eje (b), lo comprobado sin hallazgos y la lista de comandos, resumidos.

> ## Informe del revisor · trabajo/cuarentena-por-defecto · 2026-10-01
>
> HEAD e30765c, base main c95ab8b, 3 commits. El árbol del commit es 687043c0…26 y coincide con `.git/botsito-sello`. No existe `make-check.log` en el árbol de trabajo, así que no vi la línea SELLO ni el PICO. Los 1777 passed y los 285 MiB los doy solo como declarados por quien encarga.
>
> ### Eje (a) · Reglas de la casa
> Resumen: 0 bloquea, 1 importa, 1 menor.
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | A1 | importa | El informe se contradice. §2 (el párrafo de «La guardia») dice que las reglas viejas de `kb find` sin `--video` «se quedan como estaban: el encargo no pide quitarlas, y relajarlas lo decide el consultor (§7)». La tercera orden, punto 2, ordena quitar esa regla, §9.5 dice que se quitó, y el código la quita. Un lector que se quede en §2 cree que la regla sigue. | `docs/validation/CUARENTENA-POR-DEFECTO.md` líneas 109-114 frente a 312-318; `.claude/hooks/guardia.py` (diff: `video is not None and video.lower() in cuarentena`) |
> | A2 | menor | La lista `SIN_MIRAR_CRUDO` deja pasar un `make check` con argumentos extra, porque `make\s+check\b[^;&|]*` admite la opción de crudo. Es solo lectura del regex. Quise ejecutar `exigir_sin_crudo` y la propia guardia me bloqueó el comando, así que no pude comprobarlo. No lo rodeé. El caso es inofensivo, pero la orden decía «make check y pytest sin argumentos extra»: `pytest` está bien, `make check` no. | `.claude/hooks/guardia.py` (definición de `SIN_MIRAR_CRUDO`) |
>
> Comprobado sin hallazgos: el contrato (29 ficheros, nada en `rutas_protegidas`); `pytest` de `test_guardia_claude.py` y `test_cuarentena.py` en verde; `state check` OK; `knowledge/` intacto; `HISTORIA.md` solo con lineas anadidas; el informe sin contenido de transcripciones ni fechas de dias reservados; los tres anexos reproducen §4, §5 y §9.3; la regla (c) movida linea a linea desde `scripts/transcribir_sesion.py`; la guardia bloquea la opcion de crudo en todas las formas pedidas, deja pasar `make check` y `pytest`, bloquea la propuesta oculta, deja pasar `kb find` sin `--video` y bloquea `--video v7`; tres citas del informe contra su fuente.
>
> ### Eje (b) · Encargo
> Resumen: 0 bloquea, 2 importa, 2 menor. Requisitos: 19 hechos, 1 parcial, 0 no hechos.
>
> | # | Requisito | Estado | Evidencia |
> |---|---|---|---|
> | 1-6, 8-15, 17-20 | Fase 0 a 3 y las ordenes segunda y tercera | Hecho | (ver el informe del revisor; resumido aqui por longitud) |
> | 7 | Empujar como `fix/` y esperar la CI de Linux | Pendiente | se anade despues |
> | 16 | Segunda orden 4: un test falla ante el parametro fuera de la lista; la guardia lo bloquea | Parcial | Ver B2 |
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | B1 | importa | **`evidence propose` filtra solo el tramo copiado, no la cruda entera**, y puede copiar a `knowledge/_proposals/` un segmento que la CLI oculta por «vecino». `evidence_propose` hace `filtro.aplicar([s for s in segmentos if tramo])`. La regla (c) arrastra al segmento anterior y al siguiente, y esa vecindad solo se calcula dentro del recorte. Si un segmento del borde del intervalo es vecino de uno que menciona un mes y este queda fuera, se copia. Con `cargar_cruda` (filtrado global) ese mismo segmento sale oculto. Lo ejecuté con dos segmentos: `aplicar([s0, s1])` da `[]` y `aplicar([s0])` da `[0]`. Además `test_evidence_propose_copia_solo_lo_que_se_puede_ensenar` usa el intervalo entero 0:00:00-0:00:40, así que no ejercita el borde. | `src/botsito/cli.py` (líneas ~1120-1129 de la rama); `tests/unit/test_cuarentena.py:248` |
> | B2 | importa | **El test `test_nadie_lee_la_cruda_sin_pasar_por_las_funciones_que_filtran` es sintáctico y no cubre lo que el encargo pide vigilar**. Solo detecta `X / FICHERO_CRUDA` o `X / "cruda.jsonl"` (BinOp `Div`) y el import de `desde_jsonl` desde `transcripcion`. No ve `joinpath("cruda.jsonl")`, `open(f"{c}/cruda.jsonl")`, `glob("cruda*")`, ni `cruda.txt` / `parciales/*.json`. Hoy no hay ningún caso real (mi barrido en `src/` y `scripts/` es limpio), pero el informe presenta el test como cierre de la vía. Además `scripts/transcribir_sesion.py` está autorizado por fichero entero (`(…, None)`) aunque «hoy no lo necesita» (§2.1). Cualquier uso nuevo en ese script pasaría el test. | `tests/unit/test_cuarentena.py:278`, `:340-375` |
> | B3 | menor | La evidencia entra entera en `kb find`, `kb at` e índice. Los 9 items de §9.3, que citan segmentos que hoy se ocultan por (c), se muestran con su cita. Está declarado en §2 y §9.3 y en §7.1 espera la decisión del consultor. | Informe §2 y §9.3; `indice.py` |
> | B4 | menor | `scripts/a18_buscar.py` pasa a leer filtrado y las cuatro salidas commiteadas ya no se reproducen byte a byte (declarado, §7.3 y §9.1). La afirmación la hizo la rama midiendo sha256, y no la puedo reproducir sin escribir. Es una decisión del consultor, no un fallo. | Informe §9.1 |
>
> ### Lo que no pude comprobar
> `make check` (solo el sello contra el arbol del commit, que coincide); `knowledge validate` (escribe); `make check` con la opcion de crudo (la guardia lo bloqueo y no la rodeo); la CI de Linux; la medicion de sha256 de las salidas de A-18, A-24, A-35 y sesion 02; evasiones por construccion de cadenas en shell o en Python.

**Respuesta de la sesion, hallazgo a hallazgo:**
- **A1, arreglado**: recuadro de correccion en §2 que apunta a §9.5.
- **A2, arreglado**: `SIN_MIRAR_CRUDO` deja pasar `make check` solo con su redireccion a un fichero;
  `make check` con la opcion de crudo y redireccion se bloquea (caso nuevo en
  `test_la_guardia_bloquea_el_corpus_sin_filtrar`).
- **B1, arreglado**: `evidence propose` filtra la cruda ENTERA y despues recorta, como
  `cargar_cruda`; el aviso cuenta solo los ocultos del intervalo.
  `test_evidence_propose_oculta_el_vecino_aunque_el_que_dispara_quede_fuera` ejercita el borde
  (intervalo 0:00:20-0:00:21: solo el vecino, con el que dispara fuera).
- **B2, arreglado en lo que se puede medir**: `lecturas_en_bruto` ve ahora tambien el nombre del
  texto de una transcripcion (`cruda*`, `corregida*`, `parciales`, en literales y f-strings, y las
  constantes del pipeline) pasado a `open`, `Path`, `joinpath`, `glob`, `rglob`, `iglob` o
  `read_text`, ademas de detras de una `/`; cuatro casos nuevos en
  `test_los_recorridos_no_son_decorativos`. Sigue siendo un recorrido del codigo, no una prueba de
  que no exista otra via (una ruta armada en tiempo de ejecucion no se ve): se dice asi. Sobre el
  proyecto da cero casos; el primer intento con «parcial» cazo un `.parcial` de una descarga de
  ticks y se estrecho a `parciales`. La autorizacion de `scripts/transcribir_sesion.py` por
  fichero entero es la de la lista del consultor; si la quiere por funcion, no hay hoy ninguna que
  la use.
- **B3 y B4**: declarados; son decisiones del consultor (§7).
