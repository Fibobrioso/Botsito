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

> **CORRECCION (2026-10-01, misma rama, cuarta y quinta orden).** Las tres preguntas que habia aqui
> estan DECIDIDAS: los 9 items, `corpus transcript check` y `scripts/a18_buscar.py` (§12). Queda
> una sola cosa para el consultor, que nace de la quinta orden: §13.4.

## La skill `abrir-rama`, en su primer uso

Abrio esta rama y se quedo corta en un punto: no decia que el artefacto del contrato tiene que
estar estadiado ya en el primer commit, y `make check` lo exige (`contrato_rama.py`: «falta el
artefacto»). Corregido en la propia skill, pasos 4 y 7. Lo demas -base, encargo, contrato, Archivo 2
de `PROJECT_STATE.md` en HISTORIA y `state check` antes de sellar- fue tal cual. Tambien se apunto en
HISTORIA, como pedia el encargo, lo que quedo fuera del cierre de F36k (el «1 skipped» de
`make check` en `main`).

## 8. Estado

> **CORRECCION (2026-10-01, misma rama).** Este estado era el de la tercera orden. El vigente es el
> del final del informe, §15.

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

> **CORRECCION (2026-10-01, misma rama, cuarta orden).** Los nombres de este punto cambiaron: la
> lista es ahora `.claude/hooks/ficheros_con_ocultos.txt`, la escribe
> `scripts/ficheros_con_ocultos.py`, va por rutas relativas y la guardia la mira en
> `motivo_fichero` con `R_FICHERO_OCULTO`, para propuestas y para salidas de medicion (§12.3).

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
| `a4d37e8` (hallazgos del revisor, §11) | `36938253913` | 1 failed, 1770 passed, 8 skipped: el mismo fallo esperado y ningun otro |
| `bc77e2b` (cuarta y quinta orden) | `36944773639` | 1 failed, 1779 passed, 8 skipped: el mismo fallo esperado y ningun otro |
| `14bb92c` (revisor, segunda pasada) | `36946258608` | 1 failed, 1779 passed, 8 skipped: el mismo fallo esperado y ningun otro |
| `0faa9ae` (sexta orden) | `36949045836` | 1 failed, 1784 passed, 8 skipped: el mismo fallo esperado y ningun otro |

El run del commit de documentacion que escribe esta fila se apunta en la respuesta: escribirlo aqui
exigiria otro commit y otro run.

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

## 12. La cuarta orden del consultor (2026-10-01)

Copiada tal cual en `docs/encargos/trabajo-cuarentena-por-defecto.md`, «Cuarta orden».

### 12.1 Punto 1a: ¿el segmento que cita cada uno de los 9 items trae un dia reservado?

`docs/validation/anexos/CUARENTENA-POR-DEFECTO/exposicion_items.py`: lo comprueba el propio filtro
al ocultar (`Filtro.dias`, con los dias de `casos_ocultos`, y `Oculto.fecha_vigilada`), leyendo la
cruda FILTRADA; del texto solo sale un booleano. Se imprimio solo el id y True o False:

| Item | Fecha de un dia de `casos_ocultos` |
|---|---|
| ev-v2-002604-041288d7 | False |
| ev-v3-001952-a3276d86 | False |
| ev-v3-002026-fa5295fa | False |
| ev-v4-000016-8f6862dd | False |
| ev-v4-000052-61cf22a9 | False |
| ev-v4-000353-9ea3ce94 | False |
| ev-v4-004533-14f2b226 | False |
| ev-v4-012049-04c922c5 | False |
| ev-v6-014702-2d7096db | False |

Ninguno da True: no hay exposicion que declarar. La deteccion de fechas (`cuarentena.fechas_en`:
«N de MES», «MES N», «N/M», tambien con el numero en letras) tiene su control positivo sintetico en
`test_fechas_en_dice_dia_y_mes_y_nada_mas`, que exige True para una fecha vigilada y False para el
resto.

### 12.2 Punto 1b: kb oculta la evidencia cuya cita cae en un segmento oculto

> **CORRECCION (2026-10-01, misma rama, sexta orden).** Este criterio ya no es el vigente: la
> evidencia tiene el suyo (§16), y hoy `kb` oculta 1 de 437 items, no 79.

`construir_indice` (`src/botsito/retrieval/indice.py`) quita del indice, salvo con la opcion de
crudo, el item cuyo intervalo pisa un segmento que el filtro oculta (`cuarentena.items_ocultos`, con
el motivo de mas prioridad de los que pisa). `kb find` y `kb at` lo cuentan en el aviso
(«N items de evidencia: … por …»), sin id ni texto; `kb at` cuenta solo los de su ventana.
Test sintetico: `test_kb_oculta_la_evidencia_cuya_cita_cae_en_un_segmento_oculto`.

**Consecuencia que conviene ver: no son solo los 9.** El mismo criterio oculta toda la evidencia de
las sesiones en cuarentena, porque su cita cae en una sesion entera oculta por (a). Medido con
`anexos/CUARENTENA-POR-DEFECTO/kb_ocultos.py` (solo cuentas):

| Video | Motivo | Via | Items |
|---|---|---|---|
| v2 | (c) | cita | 1 |
| v3 | (c) | cita | 2 |
| v4 | (c) | cita | 5 |
| v6 | (c) | cita | 1 |
| v6 | (b) | copia | 1 |
| v7 | (a) | cita | 5 |
| v8 | (a) | cita | 2 |
| v9 | (a) | cita | 62 |

79 de 437 items salen ocultos por defecto: los 9 de (c), los 69 de v7, v8 y v9 por (a), y uno de v6
por (b) que entra por la quinta orden (§13.3). Los de (a) son coherentes con la cuarentena -su cita
es texto de una sesion que no se lee-, pero hasta hoy `kb find` los ensenaba.

### 12.3 Punto 3: `scripts/a18_buscar.py` y sus cuatro salidas

- **Filtrado y sin autorizar**, como estaba. La cabecera del script dice desde hoy que lee la cruda
  filtrada, que su salida de hoy no reproduce la commiteada, y que lo mismo vale para
  `buscar_ambiguedades.py`, que importa de el.
- **Las cuatro salidas, en la lista que bloquea la guardia**, junto a las 10 propuestas: la lista
  pasa a llamarse `.claude/hooks/ficheros_con_ocultos.txt` (14 rutas relativas), la escribe
  `scripts/ficheros_con_ocultos.py --escribir`, y la guardia la mira en `motivo_fichero`
  (`R_FICHERO_OCULTO`): Read, Grep, Glob y los lectores de Bash. Test sintetico:
  `test_un_fichero_con_texto_oculto_no_se_lee` (una propuesta y una salida bloqueadas, sus vecinas
  no). `test_la_lista_de_la_guardia_es_la_que_se_calcula` exige que el fichero sea lo calculado.
- **Que una salida entre se CALCULA, no se supone**: una salida entra si trae alguna linea
  `[h:mm:ss-h:mm:ss] #n texto` cuyo segmento `n`, de la transcripcion de su pasaje, esta oculto hoy.
  La primera version comparaba el sha de la salida de hoy con el de la commiteada, y eso no mide lo
  mismo (§13.1). Con la definicion exacta, las cuatro entran:

| Salida | Lineas de segmentos ocultos hoy | Lineas que hoy ya no salen (la cuenta vieja) |
|---|---|---|
| `A18-TRANSCRIPCIONES-SALIDA.txt` | 27 | 50 |
| `A24-A21-A26-A34-SALIDA.txt` | 9 | 9 |
| `A35-PIVOTE-FORMADO-SALIDA.txt` | 9 | 9 |
| `SESION-02-BUSQUEDA-SALIDA.txt` | 11 | 11 |

- **Recuadros de correccion** en los 9 informes cerrados que nombran una de esas salidas (los
  `*-CRITERIO.md` y `*-CLASIFICACION.md` de A-18, A-24, A-35 y sesion 02, y
  `A18-TRANSCRIPCIONES.md`), justo debajo del titulo, con el cuerpo intacto. Los puso
  `anexos/CUARENTENA-POR-DEFECTO/recuadros.py`, una vez, fuera de `make check`; el diff de cada uno
  son 9 lineas anadidas y ninguna quitada.

### 12.4 Puntos 2 y 4: la lista de autorizados

- **`corpus transcript check`** (`manifiestos_transcripcion.comprobar`), autorizado con su motivo.
  Solo imprime el resultado (OK o el fallo) y el fichero: el error de forma ya no arrastra el
  detalle de la excepcion, que podia traer texto. Test: `test_transcript_check_no_imprime_contenido`,
  con la cruda sana y con una rota cuyo sha casa; ni el texto del segmento ni la palabra que rompe
  la forma salen.
- **`scripts/transcribir_sesion.py`** no usa la opcion de crudo: ya no esta autorizado como fichero
  entero. Quedan dos funciones concretas, `salidas_de` y `transcribir`, porque arman y escriben las
  rutas de la cruda de una sesion NUEVA fuera del repositorio (la tuberia de cuarentena), y sin
  ellas `test_nadie_lee_la_cruda_sin_pasar_por_las_funciones_que_filtran` falla. Es la lectura de
  «se autoriza cuando una funcion concreta lo necesite»; si el consultor las quiere fuera, hay que
  cambiar el script. `_autorizado` ya no acepta una entrada por fichero entero, y un test exige que
  ninguna lo sea.

### 12.5 Punto 5: la trampa en CLAUDE.md

Anadida a «Trampas medidas»: un texto con la opcion o el parametro literal se escribe con Write o
Edit, y el mensaje de commit con `git commit -F` y un fichero escrito con Write. Este commit se hizo
asi.

## 13. La quinta orden del consultor, y una medicion que conto mal

Las dos preguntas y sus respuestas, tal cual, en el encargo («Quinta orden»).

### 13.1 El error

Al hacer el punto 3 medi que ficheros seguidos copian lineas de las cuatro salidas que hoy se
ocultan, y defini «linea oculta» como **la linea que esta en la salida commiteada y no en la de
hoy**. Esa definicion **cuenta de mas**: si el termino de un pasaje cae en un segmento oculto, el
pasaje ENTERO deja de salir, con sus vecinos VISIBLES. Con ella salieron 19 ficheros, y con el
criterio estricto (la mitad o mas de las ventanas) dos informes cerrados -los `*-CLASIFICACION.md`
de A-24 (3) y de A-35 (4)- y seis items, dos de ellos fuera de los 9: `ev-v3-002130-8617c40b` y
`ev-v4-003451-d750e553`. **Con esas cifras se hicieron las dos preguntas.**

Al implementar la segunda respuesta, el criterio por contenido no oculto ninguno de esos dos items.
Buscando por que, se midio (solo numeros y booleanos) que los 8 segmentos que casaban (v3 #241, #243
y #244; v4 #596 a #600) **no estan ocultos hoy**: eran vecinos visibles de pasajes que desaparecen.
Las transcripciones eran las mismas (`tr-v3-…-270a4851`, `tr-v4-…-a8d1bccc`).

### 13.2 La medicion corregida

`anexos/CUARENTENA-POR-DEFECTO/citas_de_salidas.py`, reescrito con la definicion EXACTA (una linea
es oculta si su segmento lo esta) y con la vieja al lado:

- **Ningun informe** copia una linea oculta: los dos `*-CLASIFICACION.md` casaban lineas visibles.
- **Cuatro items** copian alguna, y los cuatro estan ya entre los 9 de §9.3 (ocultos en kb por su
  cita): `ev-v2-002604-041288d7`, `ev-v4-000016-8f6862dd`, `ev-v4-000353-9ea3ce94` y
  `ev-v4-012049-04c922c5`.
- Control: las lineas VISIBLES de las mismas salidas se encuentran copiadas en 54 a 241 ficheros
  segun la salida, asi que el metodo encuentra copias cuando las hay.

### 13.3 Lo que se hizo con las dos respuestas

Las dos decisiones son un MECANISMO calculado («el generador los calcula con el mismo metodo y el
mismo umbral»; «kb oculta el item cuyo texto copia la mitad o mas de una linea oculta»), y se
implementaron tal cual, con la definicion corregida:

- **Informes**: `scripts/ficheros_con_ocultos.py` anade a la lista los ficheros de `docs/` que copian
  una linea oculta de una salida (`cuarentena.copia`, ventanas de 30 caracteres cada 10, la mitad o
  mas). **Hoy no entra ninguno**; la lista sigue en 14 rutas. Test de la definicion:
  `test_una_linea_es_oculta_si_su_segmento_lo_esta` (un `#1` oculto en una transcripcion y visible
  en otra). Los 9 recuadros de §12.3 se pusieron igual: lo que corrigen es la salida, no la copia.
- **Items**: `construir_indice` oculta tambien el item cuyo texto (cita, afirmacion, valor y notas)
  copia un segmento que el filtro oculta en SU video, aunque su cita no lo pise. Lo hace
  `indice._evidencia_que_copia`, AUTORIZADA a leer la cruda entera con su motivo (nueva entrada de
  `AUTORIZADOS`): compara y devuelve ids y motivos, nunca texto. Tests:
  `test_kb_oculta_la_evidencia_que_copia_un_segmento_oculto` (`kb find` y `kb at`, y la opcion de
  crudo lo muestra) y `test_copia_pide_la_mitad_de_las_ventanas`. **Sobre el repositorio real oculta
  uno**, que no es ninguno de los dos de la pregunta: `ev-v6-010927-50b8d873`, motivo (b) -copia el
  texto de un segmento de un tramo no citable de v6 sin que su cita (1:09:27) caiga en el tramo-.
- **La 1a repetida** (`anexos/CUARENTENA-POR-DEFECTO/copias_items.py`, id, motivo y True/False):
  `ev-v6-010927-50b8d873 | b | False`. Los dos items de la pregunta no copian ningun segmento
  oculto, asi que no hay segmento sobre el que repetirla.

### 13.4 Lo que debe decidir el consultor

1. **Las dos respuestas se dieron sobre cifras que estaban mal** (§13.1). Lo implementado es el
   mecanismo que se decidio, con la definicion corregida, y hoy no bloquea ningun informe ni oculta
   los dos items nombrados. Si el consultor queria otra cosa -por ejemplo, bloquear los dos
   `*-CLASIFICACION.md` aunque no copien nada oculto-, es un cambio de una linea en la lista
   calculada.
2. **`ev-v6-010927-50b8d873`** copia texto de un tramo no citable de v6 desde una cita fuera del
   tramo. `knowledge/` no se ha tocado; kb lo oculta por defecto. Puede ser una frase que el trader
   repite (no se ha abierto); si no lo es, el item cita algo que no deberia.

## 14. Informe del revisor, segunda pasada (solo `a4d37e8..bc77e2b`)

Subagente `revisor`, sobre `bc77e2b`. Los hallazgos, tal cual; la tabla de requisitos, lo
comprobado sin hallazgos y los comandos, resumidos.

> ## Informe del revisor · trabajo/cuarentena-por-defecto (solo a4d37e8..bc77e2b) · 2026-10-01
>
> ### Eje (a) · Reglas de la casa
> Resumen: 0 bloquea, 2 importa, 2 menor.
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | A1 | importa | El informe no acaba en su estado vigente. El «Estado» de la tercera orden (§8, línea 242) remite a «el del final del informe, §15», y esa sección no existe. El informe termina en §13.4. Regla: «el informe de la rama existe y acaba en su estado». | `grep -n "§15\|## 14\|## 15"` solo da la línea 242 |
> | A2 | importa | El punto 6 de la cuarta orden pide anotar el run 36938253913 «y el run nuevo». El 36938253913 está en §10, pero el run de `bc77e2b` queda diferido a «la respuesta». Mientras no se escriba, el informe queda incompleto en ese punto. | `CUARENTENA-POR-DEFECTO.md:335-336` |
> | A3 | menor | La primera línea de los recuadros de los 9 informes no está reajustada al ancho del resto. | `git diff a4d37e8 bc77e2b -- docs/validation/A24-A21-A26-A34-CLASIFICACION.md` |
> | A4 | menor | En la CI (sin `data/`), `test_la_lista_de_la_guardia_es_la_que_se_calcula` solo comprueba que las rutas no-propuesta empiezan por `docs/`, y la lista commiteada se da por buena. Es una comprobación débil, aunque no falla y está declarada en la docstring. | `tests/unit/test_guardia_claude.py`; `scripts/ficheros_con_ocultos.py`, rama `otros is None` |
>
> Comprobado sin hallazgos: el contrato; los tests de `test_cuarentena.py` y `test_guardia_claude.py` y `state check`; la lista calculada coincide con la commiteada (14 rutas); la guardia mira la lista por `rel` en `motivo_fichero` y el test cubre Read, `cat` y Grep; ninguna autorización por fichero entero; `transcribir_sesion.py` sin `crudo=True` en ninguna línea; `corpus transcript check` sin el detalle de la excepción; en los 9 recuadros, 0 líneas eliminadas; la trampa en `CLAUDE.md`; `knowledge/` intacto.
>
> ### Eje (b) · Encargo
> Resumen: 0 bloquea, 1 importa, 1 menor. Requisitos: 9 hechos, 1 parcial (el 6, ver A2), 0 no hechos; Q1, Q2 y el punto 4, «hechos de otra forma», declarados.
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | B1 | importa | Las dos respuestas del consultor se dieron sobre una medición que contaba de más, y la implementación aplica el MECANISMO («mismo método y mismo umbral», «mitad o más») con la definición corregida. El resultado práctico es distinto de lo que el consultor creyó decidir: los dos informes no se bloquean y los dos ítems nombrados no se ocultan. Es defendible -las respuestas son mecanismos calculados, y el informe declara el error, la causa, la cuenta corregida y un control-, pero es una reinterpretación unilateral del sentido de «Se añaden a la lista». Recomendación: que el consultor confirme esta lectura antes del cierre, y no tratar la respuesta Q1 como cumplida a la letra. | Informe §13.1, §13.3, §13.4; encargo, «Quinta orden» |
> | B2 | importa | La quinta orden oculta por defecto un ítem que el consultor no nombró, `ev-v6-010927-50b8d873`; y según §12.2 79 de 437 ítems salen ocultos en kb (69 de v7, v8 y v9 por (a)). Está declarado y es coherente con 1b («cuya cita cae en un segmento oculto» cubre la sesión en cuarentena), pero es un cambio grande de comportamiento de `kb find` que el consultor debe ver. | Informe §12.2 y §13.3 |
> | B3 | menor | El calculador solo barre ficheros de `docs/` seguidos por git; `knowledge/` no se barre por copias. Es consistente con el encargo («ficheros de docs/»). | `scripts/ficheros_con_ocultos.py`, `_que_copian` |
>
> ### Lo que no pude comprobar
> La guardia con lectores de Bash distintos de `cat` y con Glob (la propia guardia bloqueó el arnés, y no se rodeó); las cuentas 27, 9, 9 y 11 y los recuentos «79 de 437» (no se ejecutaron los anexos, que leen la cruda); la CI de Linux de `bc77e2b` y el log de `make check` de ese commit.

**Respuesta de la sesion, hallazgo a hallazgo:**
- **A1, arreglado**: §15, abajo.
- **A2, arreglado**: el run de `bc77e2b`, en §10. El de este commit de documentacion se apunta en la
  respuesta: escribirlo aqui pediria otro commit y otro run.
- **A3**: no se toca. Los recuadros los escribio un guion idempotente, y reajustarlos ahora seria
  otro diff en 9 informes cerrados sin cambiar lo que dicen.
- **A4**: declarado. En la CI no hay cruda con la que recalcular, y la comprobacion completa corre
  en `make check` en la maquina, donde si la hay.
- **B1 y B2**: no se arreglan en la rama; son decisiones del consultor, ya en §13.4, y van a §15.
- **B3**: es el alcance que se decidio.

## 15. Estado

> **CORRECCION (2026-10-01, misma rama, sexta orden).** Las cuatro cosas de esta lista las decidio
> el consultor (§16). El estado vigente es el del final del informe, §18.

**Rama lista para revisión, NO cerrada.** La cuarta y la quinta orden estan hechas, selladas y con la
CI de Linux (§10). Quedan para el consultor, sin las que la rama no debe cerrarse:
1. **Confirmar la lectura de la quinta orden** (§13.4.1 y B1): las dos respuestas se aplicaron como
   mecanismo con la definicion corregida, y hoy no bloquean los dos `*-CLASIFICACION.md` ni ocultan
   los dos items nombrados.
2. **`ev-v6-010927-50b8d873`** (§13.4.2): kb lo oculta porque copia texto de un tramo no citable
   de v6; `knowledge/` no se ha tocado.
3. **Lo que kb oculta por defecto** (§12.2 y B2): 79 de 437 items, 69 de ellos de v7, v8 y v9.
4. **Las dos funciones de `scripts/transcribir_sesion.py` en `AUTORIZADOS`** (§12.4): si las quiere
   fuera, hay que cambiar el script.

## 16. La sexta orden del consultor (2026-10-01)

Copiada tal cual en `docs/encargos/trabajo-cuarentena-por-defecto.md`, «Sexta orden». Decide los
cuatro puntos de §15: la lectura de la quinta orden, aceptada (1); el criterio de la evidencia,
cambiado (2); las dos funciones de `scripts/transcribir_sesion.py`, autorizadas (3, y su motivo
en `AUTORIZADOS` lo cita); A3 y A4 de §14, declarados (4).

### 16.1 Por que la evidencia y la cruda tienen criterios distintos

Las tres reglas de la cuarentena -sesion en cuarentena (a), tramo no citable (b) y mes reservado o
sin sortear (c)- se escribieron para la **transcripcion cruda**, que es texto SIN REVISAR: nadie ha
mirado que dice cada segmento, asi que se oculta por lo que podria decir. Un **item de evidencia
aceptado** es otra cosa: un extracto que alguien leyo, recorto y reviso, con su cita literal, y
cuyos ficheros de `knowledge/evidence/` se leen directamente con Read. Ocultarlo en `kb find` por
(a) o por (c) tiene coste -la sesion pierde evidencia revisada al buscar- y no protege nada, porque
el mismo texto esta a un Read de distancia.

Lo que si sigue ocultando un item son las dos cosas que no dependen de que el texto este revisado:
- **(b), un tramo no citable**: es un acuerdo sobre el CONTENIDO -esos minutos no se citan-, y un
  item que los cita, o que copia su texto, lo rompe igual que la cruda;
- **un dia de `casos_ocultos`**: es la exposicion que el holdout prohibe, la diga la cruda o la diga
  un extracto revisado.

El criterio de los SEGMENTOS no cambia: siguen ocultos por (a), (b) y (c).

### 16.2 La comprobacion 1a sobre los 79, antes de cambiar nada

`anexos/CUARENTENA-POR-DEFECTO/exposicion_79.py`, ejecutado con el codigo de `bc77e2b`. True si el
item trae una fecha (dia y mes) que es un dia de `casos_ocultos`, mirada en tres sitios: los
segmentos OCULTOS que su cita pisa o que su texto copia (el filtro lo anota al ocultar, y solo sale
el booleano), los segmentos VISIBLES que su cita pisa, y el texto del propio item. Es la 1a de la
cuarta orden ampliada a lo visible y al item, para no dejar fuera una fecha que el filtro no oculto.

**Los 79 dan False.** Control positivo, con la misma via y TODOS los dias del año como si fueran
reservados (`--control`, solo el total): 5 de los 79 traen alguna fecha, asi que la via encuentra
fechas cuando las hay, y ninguna de esas 5 es un dia de `casos_ocultos`. Solo id, motivo y booleano:

| Item | Motivo actual | Dia de `casos_ocultos` |
|---|---|---|
| ev-v2-002604-041288d7 | (c) | False |
| ev-v3-001952-a3276d86 | (c) | False |
| ev-v3-002026-fa5295fa | (c) | False |
| ev-v4-000016-8f6862dd | (c) | False |
| ev-v4-000052-61cf22a9 | (c) | False |
| ev-v4-000353-9ea3ce94 | (c) | False |
| ev-v4-004533-14f2b226 | (c) | False |
| ev-v4-012049-04c922c5 | (c) | False |
| ev-v6-010927-50b8d873 | (b) | False |
| ev-v6-014702-2d7096db | (c) | False |
| ev-v7-000423-01b2c18a | (a) | False |
| ev-v7-001457-1fe7fdfe | (a) | False |
| ev-v7-001550-82e5cffc | (a) | False |
| ev-v7-002201-2b2f20aa | (a) | False |
| ev-v7-002403-8344331d | (a) | False |
| ev-v8-003620-12670f0e | (a) | False |
| ev-v8-003935-0a0b3f8e | (a) | False |
| ev-v9-000124-d2afa992 | (a) | False |
| ev-v9-000143-214aacde | (a) | False |
| ev-v9-000538-4bbf1c16 | (a) | False |
| ev-v9-000651-6a11b3a1 | (a) | False |
| ev-v9-000902-25db5bf5 | (a) | False |
| ev-v9-001312-19e45e4a | (a) | False |
| ev-v9-001504-72aa462a | (a) | False |
| ev-v9-001522-8b8c4942 | (a) | False |
| ev-v9-001529-ac28bb40 | (a) | False |
| ev-v9-001617-4b47e01a | (a) | False |
| ev-v9-001915-d03d1565 | (a) | False |
| ev-v9-002526-6a6579e6 | (a) | False |
| ev-v9-002735-472432b8 | (a) | False |
| ev-v9-002807-16d5946b | (a) | False |
| ev-v9-003026-0445965d | (a) | False |
| ev-v9-003253-2ac6060a | (a) | False |
| ev-v9-003303-818a0796 | (a) | False |
| ev-v9-003318-c0503fe5 | (a) | False |
| ev-v9-003456-9ef48fb5 | (a) | False |
| ev-v9-003621-f65f51a0 | (a) | False |
| ev-v9-003826-740c4d95 | (a) | False |
| ev-v9-004037-ca58e486 | (a) | False |
| ev-v9-004217-c014bfdc | (a) | False |
| ev-v9-004533-d075b080 | (a) | False |
| ev-v9-004721-2e023ac6 | (a) | False |
| ev-v9-004919-c6bfb3ee | (a) | False |
| ev-v9-005219-3b98f54f | (a) | False |
| ev-v9-005543-1b52290e | (a) | False |
| ev-v9-005619-27ae7cd3 | (a) | False |
| ev-v9-005631-c3b42381 | (a) | False |
| ev-v9-005850-8aae8764 | (a) | False |
| ev-v9-005916-d6a15b43 | (a) | False |
| ev-v9-010053-e521e833 | (a) | False |
| ev-v9-010232-4b049a1e | (a) | False |
| ev-v9-010311-a13b0a41 | (a) | False |
| ev-v9-010416-eb674c2f | (a) | False |
| ev-v9-010541-0c80d5cf | (a) | False |
| ev-v9-010620-ac899dd8 | (a) | False |
| ev-v9-010753-063c8cb7 | (a) | False |
| ev-v9-010809-68e4ea44 | (a) | False |
| ev-v9-011128-a267338b | (a) | False |
| ev-v9-011139-a26a5b11 | (a) | False |
| ev-v9-011206-148fc7f9 | (a) | False |
| ev-v9-011555-81ec8beb | (a) | False |
| ev-v9-011655-c20a1c2d | (a) | False |
| ev-v9-011704-b5ddc3e3 | (a) | False |
| ev-v9-011714-08536830 | (a) | False |
| ev-v9-011957-4250c2b4 | (a) | False |
| ev-v9-012347-eef7627f | (a) | False |
| ev-v9-012401-3fefa768 | (a) | False |
| ev-v9-012514-b5b6c84f | (a) | False |
| ev-v9-012612-d9db2ee8 | (a) | False |
| ev-v9-012809-4c13a3f4 | (a) | False |
| ev-v9-013021-ea0db73a | (a) | False |
| ev-v9-013054-d49a544e | (a) | False |
| ev-v9-013117-c683f9b5 | (a) | False |
| ev-v9-013205-85840dcc | (a) | False |
| ev-v9-013437-ffdd9c87 | (a) | False |
| ev-v9-013736-463282d5 | (a) | False |
| ev-v9-013757-e4c639db | (a) | False |
| ev-v9-013914-9fb86553 | (a) | False |
| ev-v9-013923-0912f06b | (a) | False |

### 16.3 El criterio nuevo, en el codigo

- **`cuarentena.evidencia_a_ocultar`** (pura): oculta un item solo si su cita pisa un tramo no
  citable o un segmento oculto por el (b), o si trae un dia de `filtro.dias` en su texto, en un
  segmento visible que cita o en uno oculto que pisa (motivo c, «material reservado o sin sortear»).
  Devuelve ids, motivos y el booleano; nunca texto ni la fecha.
- **La copia** (quinta orden) se queda, con el alcance de la sexta: `items_que_copian` acepta
  `motivos`, y el indice solo le pasa `{"b"}`. `indice._evidencia_que_copia` ni lee la cruda si el
  video no tiene ningun segmento oculto por (b).
- **Los dias**: `retrieval` no puede importar `cases`, asi que `construir_indice` recibe `dias` de
  quien lo llama; `kb` se los da con `cli._dias_ocultos` (los de `casos_ocultos`). Sin la opcion de
  crudo, el filtro de cada video los lleva y anota el booleano. `kit build`
  (`cases/paquete.py`) construye el indice sin `dias`, pero de el solo usa `fotograma_en`, que no
  depende de lo oculto.
- **Un video sin transcripcion en la maquina** tambien pasa por el criterio: su fecha se mira en el
  texto del item.
- **El recuento y el motivo**, como antes: el aviso dice «N items de evidencia: N por …».

**Medido sobre el repositorio real** (`anexos/CUARENTENA-POR-DEFECTO/kb_ocultos.py --cuarta`): `kb`
oculta **1 de 437 items**, `ev-v6-010927-50b8d873`, por (b) y por copia. Con el criterio de la
cuarta orden eran 78 por la cita, mas ese por la copia: los 79 de §16.2.

### 16.4 Tests

Los tres de la orden, sinteticos, con `kb find` y `kb at`:
- `test_kb_ensena_la_evidencia_de_una_sesion_en_cuarentena_sin_dia_reservado`: v1, puesta en la
  cuarentena con la fixture, hace de v7; el item del boss SALE, y el aviso cuenta segmentos (a) y
  ninguna evidencia.
- `test_kb_oculta_la_evidencia_de_un_tramo_no_citable`: v1 con un tramo sintetico hace de v6; un
  item que copia el segmento del tramo, y otro cuya cita cae en el, se ocultan por (b), y la opcion
  de crudo los muestra.
- `test_kb_oculta_la_evidencia_con_un_dia_reservado`: un item con «31/02» se ve; con ese dia
  imposible puesto como reservado (sustituyendo `cli._dias_ocultos`) se oculta por (c), el aviso no
  lo nombra, y la opcion de crudo lo muestra.

Y uno de la funcion pura, `test_evidencia_a_ocultar_solo_por_tramo_o_dia` (pisar (c) no oculta; el
tramo, el dia en el texto y el dia en el segmento visible citado, si; sin dias, solo el tramo).
`test_las_funciones_filtran_por_defecto_y_sin_filtro_fallan` cambia su asercion: el item que pisa
un segmento de (c) ya no cuenta como oculto. Los dos tests de la cuarta y la quinta orden sobre la
evidencia se sustituyen por estos.

## 17. Informe del revisor, tercera pasada (solo `14bb92c..0faa9ae`)

Subagente `revisor`, sobre `0faa9ae`. Los hallazgos, tal cual; lo comprobado sin hallazgos y la
tabla de requisitos, resumidos.

> ## Informe del revisor · trabajo/cuarentena-por-defecto · 2026-10-01 (solo `14bb92c..HEAD`, commit 0faa9ae)
>
> ### Eje (a) · Reglas de la casa
> Resumen: 0 bloquea, 2 importa, 2 menor.
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | A1 | importa | El informe no acaba en su estado. El recuadro de §15 remite a «el estado vigente es el del final del informe, §18», pero §18 no existe. El último encabezado es `### 16.4 Tests`, sin «Estado», sin «Rama lista para revisión, NO cerrada» y sin el informe del revisor pegado. Puede ser que se añadan después de esta pasada, pero hoy la remisión apunta a nada. | `grep -n "^## "` → último `## 16.`; recuadro de §15 |
> | A2 | importa | La comprobación 1a sobre los 79 no se puede reproducir con el código actual. `exposicion_79.py` importa `indice._evidencia_que_copia`, que este mismo commit restringe a `{b}`. El docstring lo declara («se ejecutó con el código de `bc77e2b`»), pero el anexo queda roto como evidencia reejecutable. Que se corrió ANTES del cambio solo consta por la palabra del informe (§16.2): el commit es único y yo no puedo ejecutar el anexo porque lee la cruda. | `exposicion_79.py:15-17,33,56`; `indice.py` (diff) |
> | A3 | menor | El test del día reservado solo cubre el día en el texto del propio ítem y, en el test puro, el día en el segmento visible. No hay test del camino «segmento OCULTO que pisa con `fecha_vigilada`», que es el que importa en sesiones en cuarentena (a). La aserción `"31" not in línea OCULTOS` es débil como prueba de no fuga. | `test_kb_oculta_la_evidencia_con_un_dia_reservado` y `test_evidencia_a_ocultar_solo_por_tramo_o_dia` |
> | A4 | menor | En `kb_ocultos.py` la «vía» de un ítem con día y tramo a la vez sale «dia» (el booleano manda sobre `en_tramo`). Es solo etiqueta de recuento. | `kb_ocultos.py` (diff) |
>
> Comprobado sin hallazgos: el contrato; los tests de cuarentena, retrieval y guardia y `state check`; el recuento 1147 → 1149; las capas de import (`retrieval` no importa `cases`; `cli._dias_ocultos` lo hace desde la capa superior); `CLAUDE.md` coherente con el código; el criterio de los SEGMENTOS no cambia; el de la evidencia es el de la orden (solo (b) o un día de `filtro.dias`, en tres sitios; la copia solo con `{b}`; los vídeos sin cruda también; con la opción de crudo no se oculta nada; `cases/paquete.py` sin `dias`, declarado); los tres tests de la orden prueban lo que dicen; el recuento y el motivo se mantienen; §16.1 explica por qué evidencia y cruda difieren; §16.2 imprime solo id, motivo y booleano.
>
> ### Eje (b) · Encargo (Sexta orden)
> Resumen: 0 bloquea, 1 importa, 0 menor. Requisitos: 8 hechos, 1 parcial (el cierre: estado, revisor pegado, CI), 0 no hechos; el 3 (la 1a antes del cambio), «hecho por declaración».
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | B1 | importa | Falta el cierre que la orden pide al final (estado «lista para revisión, NO cerrada», informe del revisor pegado). Es el mismo hecho que A1, visto como requisito del encargo; en el informe es pendiente natural hasta que pase esta revisión. | Encargo, línea final de la Sexta orden; informe sin §17/§18 |
>
> ### Lo que no pude comprobar
> Que la 1a sobre los 79 se corrió antes del cambio y que da False (lee la cruda, y el commit es único); la cifra «1 de 437» y «78 + 1»; `make check`, `knowledge validate`, `lint-imports`, el push y la CI de Linux.

**Respuesta de la sesion, hallazgo a hallazgo:**
- **A1 y B1, arreglados**: esta seccion y §18.
- **A2, medido**: el anexo SI se reproduce con el codigo de `0faa9ae`. El unico de los 79 que entraba
  por copia es de (b), asi que restringir la copia a (b) no cambia nada: la salida de hoy es
  identica byte a byte a la de antes del cambio (`cmp`). Anotado en el docstring del anexo. Que se
  corrio antes del cambio sigue constando por la sesion: la salida se guardo antes de editar el
  codigo, y la de hoy es la misma.
- **A3, arreglado**: `test_evidencia_a_ocultar_solo_por_tramo_o_dia` cubre ahora el dia en un
  segmento OCULTO de una sesion en cuarentena (v9, todo oculto por (a)): el item que lo pisa se
  oculta por (c) y su vecino sin dia, no. La asercion sobre «31» se queda como esta: la prueba de
  no fuga es `_sin_fuga` (ningun mes ni texto del segmento), y el «31» es un añadido.
- **A4**: declarado; es la etiqueta de un recuento, y hoy no hay ningun item con dia y tramo a la
  vez.

## 18. Estado

**Rama lista para revisión, NO cerrada.** Las seis ordenes del consultor estan hechas, selladas y
con la CI de Linux (§10; el run del commit que escribe esta seccion, en la respuesta). Ninguna
decision queda abierta: las de §15 las tomo la sexta orden (§16). Lo que la rama deja:
- la CLI ensena el corpus filtrado por defecto, con el recuento y el motivo de lo oculto, y la
  opcion que lo ensena todo, solo para Aleks;
- la evidencia, con su propio criterio: `kb` oculta hoy 1 de 437 items;
- la guardia bloquea la opcion y su equivalente en Python, y 14 ficheros que copian texto oculto;
- `AUTORIZADOS`, por funcion y con motivo, vigilado por tests.
