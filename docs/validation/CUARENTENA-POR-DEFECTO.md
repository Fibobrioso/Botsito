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
`make check` y `pytest` sin argumentos. Las reglas que ya tenia para estos comandos -bloquear
`kb find` sin `--video`, los videos en cuarentena y los intervalos que pisan un tramo- **se quedan
como estaban**: el encargo no pide quitarlas, y relajarlas lo decide el consultor (§7).

### 2.1 Los llamadores que piden el contenido sin filtrar

| Llamador | Como | Por que |
|---|---|---|
| La verificacion de citas (`validation/contexto_evidencia.py`, `crudas`) | `cargar_cruda(..., crudo=True)` | compara la cita con la cruda entera; no devuelve su texto |
| `scripts/transcribir_sesion.py` | autorizado; hoy no lo necesita (lee su propia cruda fuera del repositorio) | es la cuarentena de una sesion nueva |
| Los tests | `crudo=True` en sus llamadas directas | datos sinteticos |
| `corpus glossary apply` | `regenerar_corregida`, que lee la cruda dentro del pipeline sin devolverla | la corregida se recalcula desde la cruda ENTERA (ADR-0007): filtrada, se corromperia. **No es un `crudo=True` y no esta en la lista del consultor: se declara aqui** |

`make check` no necesita nada sin filtrar fuera de los tests. `test_crudo_true_solo_en_los_llamadores_autorizados`
recorre `src/` y `scripts/` y falla ante un `crudo=` que no sea `False`, el reenvio de un parametro
(`crudo=crudo`) o de un atributo (`crudo=args.crudo`, `crudo=indice.crudo`), salvo `True` en los dos
ficheros autorizados; `test_el_recorrido_de_crudo_no_es_decorativo` lo rompe a proposito.

Fuera de estas funciones leen la cruda directamente, abriendo `cruda.jsonl`,
`scripts/a18_buscar.py` y `scripts/buscar_ambiguedades.py`: guiones de medicion de ramas cerradas,
que la guardia trata como codigo revisado mientras sean identicos a los de `main`. No se tocan.

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

1. **Las 10 propuestas** de §5: que se hace con ellas (no se han tocado).
2. **Las reglas viejas de la guardia** para `kb find`, `kb at`, `transcript show` y `frames show`
   (bloquear sin `--video`, los videos en cuarentena y los intervalos que pisan un tramo): con el
   filtro en el codigo son redundantes, y siguen. Quitarlas haria que la sesion pudiera usar esos
   comandos filtrados sobre cualquier video.

## La skill `abrir-rama`, en su primer uso

Abrio esta rama y se quedo corta en un punto: no decia que el artefacto del contrato tiene que
estar estadiado ya en el primer commit, y `make check` lo exige (`contrato_rama.py`: «falta el
artefacto»). Corregido en la propia skill, pasos 4 y 7. Lo demas -base, encargo, contrato, Archivo 2
de `PROJECT_STATE.md` en HISTORIA y `state check` antes de sellar- fue tal cual. Tambien se apunto en
HISTORIA, como pedia el encargo, lo que quedo fuera del cierre de F36k (el «1 skipped» de
`make check` en `main`).

## 8. Estado

**PARADA por la auditoria de propuestas (§5), como manda la segunda orden.** El codigo, la guardia y
los tests de las fases 1 a 3 estan hechos y sellados en la rama. Falta, tras la respuesta del
consultor: empujar como `fix/cuarentena-por-defecto` y esperar la CI de Linux (regla de `RITUAL.md`:
toca un hook), pasar el revisor y pegar su informe. NO lista para revision.
