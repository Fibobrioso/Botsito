# FUNCTIONALITY VALIDATION REPORT

**Funcionalidad:** F08 · evidence-retrieval
**Rama:** `feature/F08-evidence-retrieval`
**Objetivo:** busqueda de DESARROLLO sobre la base de conocimiento: por texto (`kb find`) y por
instante (`kb at`), lexica y determinista, con fuente en cada linea (`ev-*`, `tr-*/n`,
`fr-*/t_ms`) y un indice regenerado desde `knowledge/` + `data/` en cada ejecucion. Cierra la
fase 1 (F03-F08). Metodo supervisado: brief -> revision de diseno por agente (3 bloqueantes, 9
importantes y 9 menores, todos aplicados al brief) -> construccion -> auditoria de cierre con dos
agentes -> este informe.

## Que se construyo
- **Paquete `botsito.retrieval`** (ADR-0010), capa nueva entre `spec` y `feedback` en el contrato
  de capas (ADR-0006 enmendado): `indice.py` (token de busqueda, documentos, `construir_indice`),
  `consultas.py` (`buscar`, `en_instante`), `salida.py` (tabla y JSON deterministas). No importa
  `validation` ni `cli` (import-linter + `test_import_contracts`).
- **Token de busqueda** = `tokens()` de F07 + acentos plegados + numeros con separador
  normalizados por `Decimal`: `0,75` = `0.75`; `limite` = `límite`. `tokens()` de F07 no cambia
  (las citas siguen siendo fieles a la cruda).
- **Indice en memoria** (~0,75 s): 341 items (todos; `supersede` marcado) + 3 936 segmentos de
  las 5 crudas activas con su corregida y las `dudas` del glosario; fotograma de referencia por
  resultado (`corpus.manifiestos_fotogramas.referencia_en`: el regular anterior existente).
- **`kb find <texto>`**: AND de tokens por documento (por campo en los items, por segmento en la
  cruda); `--frase` (secuencia con comodin `[...]` via `evidence.verificacion.buscar_secuencia`,
  todas las apariciones, cruzando segmentos); `--prefijo`; `--video`, `--tema` (implica
  evidencia), `--desde/--hasta` (exigen `--video`), `--solo evidencia|cruda`, `--top`,
  `--contexto`, `--json`. Orden fijo (video, t0, evidencia antes que segmento, fuente).
- **`kb at --video --t [--margen-s 10]`**: items cuyo tramo ampliado contiene el instante,
  segmentos que lo tocan, fotograma de referencia y contradicciones abiertas de esos items
  (`contradicciones.detectar`), por bloques.
- **Compartido con `validation`**: `corpus.pipeline_transcripcion.{dudas_de, cargar_capas}`;
  `evidence.verificacion.buscar_secuencia` como base de `localizar_cita` (mismo resultado).
- Salida: toda linea de resultado con fuente; rutas POSIX relativas al repo; avisos por stderr;
  `--json` con claves ordenadas y `[]` sin resultados; stdout y stderr en UTF-8.
- Golden `tests/golden/f08_consultas_referencia.yaml` (15 consultas cerradas en la revision de
  diseno ANTES de programar) y `tests/contract/test_golden_consultas_f08.py` (corre siempre: sin
  `data/` exige el `ev-*`; con `data/` exige ademas los segmentos).

## Archivos creados
`src/botsito/retrieval/{__init__,indice,consultas,salida}.py`,
`docs/adr/0010-busqueda-de-desarrollo-lexica-con-fuente.md`, `docs/plan/features/F08-evidence-retrieval.md`,
`tests/unit/test_retrieval.py`, `tests/golden/f08_consultas_referencia.yaml`,
`tests/contract/test_golden_consultas_f08.py`.

## Archivos modificados
`src/botsito/cli.py` (`kb find | at`, stderr UTF-8), `src/botsito/corpus/pipeline_transcripcion.py`
(`dudas_de`, `Capas`, `cargar_capas`), `src/botsito/corpus/manifiestos_fotogramas.py` (`referencia_en`),
`src/botsito/evidence/verificacion.py` (`buscar_secuencia`), `src/botsito/validation/contexto_evidencia.py`,
`pyproject.toml` (capa `retrieval`), `tests/unit/{test_verificacion,test_fotogramas,test_tree}.py`,
`tests/contract/test_import_contracts.py`, `docs/adr/{README,0006-*,0009-*}.md`,
`docs/plan/MASTER_PLAN.md`, `knowledge/README.md`, `PROJECT_STATE.md`, `docs/HANDOFF.md`.

## Decisiones tomadas
Las 16 del brief (cerradas tras la revision de diseno del 2026-09-08). Destacan: capa
`retrieval` entre `spec` y `feedback` (para que F10 y F11 la usen y `fb-*` entre sin cambiar el
contrato); indice en memoria sin cache; token de busqueda distinto del token de cita; `--frase`
sin los minimos de `localizar_cita`; `no_consta` de propuestas fuera; una sola regla de
fotograma de referencia; sin ranking, sinonimos ni embeddings (fallos lexicos medidos y
propuestos al glosario, que no se toca en F08).

## Como ejecutarlo
```
uv run botsito kb find "break even" --top 10
uv run botsito kb find "0,75" --video v4 --desde 0:05:00 --hasta 0:15:00 --contexto
uv run botsito kb find "no hay entrada [...] porque cae" --frase
uv run botsito kb find "cartucho" --prefijo --solo evidencia --json
uv run botsito kb at --video v4 --t 0:44:56 --margen-s 5 --contexto
```

## Como probarlo
`make check` (lint, mypy strict, 471 casos, 4 contratos con la capa `retrieval`, state/config/
knowledge validate). Sin `data/`: `uv run --no-sync pytest -q tests/unit/test_retrieval.py
tests/contract/test_golden_consultas_f08.py` (fixture a mano, sin ffmpeg ni GPU; el golden exige
solo el `ev-*`). Con `data/`: el golden exige ademas `segmentos_min` por consulta.

## Tests ejecutados
`make check` verde: 326 funciones de test, 471 casos (antes 311 / 456 en `stable/F07`). Nuevos:
token de busqueda (acentos, coma/punto, `1:3`), indice determinista (dos construcciones = misma
salida), AND por segmento, frase por campo y cruzando segmentos (dos apariciones), prefijo,
filtros y errores (`--video` desconocido, `--desde` sin video, `--desde` > `--hasta`, `--top 0`,
`--solo` invalido, corchetes, trozo vacio, consulta sin tokens), orden y `--top`, corregida
marcada sin tiempos, `dudas` y `senales`, fotograma de referencia (floor, ausentes, sin fichero,
fuera del video), `kb at` (bloques, margen 0 y 60 s, contradiccion), sin `data/` (avisos, solo
evidencia), toda linea con fuente y sin rutas absolutas, JSON con claves ordenadas y `[]`, CLI
(`find`, `at`, errores por stderr, avisos por stderr, `--json` puro), `buscar_secuencia` (todas
las apariciones, cortes, trozo vacio), `referencia_en` (floor, ausente, extra ignorado, fuera).

## Resultados

### Golden de 15 consultas (sobre los 341 items y las 5 crudas activas)
| Consulta | Item esperado | Sale | Items | Segmentos | Con `--prefijo` |
|---|---|---|---|---|---|
| break even | ev-v4-004447-bc2e74ee | si | 36 | 70 | 112 |
| 0,75 | ev-v1-000448-346d6d90 | si | 50 | 68 | 118 |
| 1:3 | ev-v1-000414-825d71a4 | si | 14 | 0 | 14 |
| cartuchos | ev-v3-004817-f2dfb955 | si | 26 | 3 | 29 |
| tres cartuchos | ev-v4-002333-8bf96363 | si | 5 | 1 | 6 |
| liquidez de m15 | ev-v1-000321-e3a35fe7 | si | 43 | 27 | 72 |
| spread | ev-v4-001221-1e66b5fd | si | 9 | 5 | 14 |
| utc | ev-v3-000136-6160fcea | si | 4 | 5 | 9 |
| cuadro de gann | ev-v1-000448-346d6d90 | si | 2 | 3 | 5 |
| equal | ev-v5-000246-17eff9e1 | si | 5 | 1 | 6 |
| 3 pm | ev-v4-011514-fe34ac7e | si | 2 | 4 | 6 |
| 0.50 | ev-v1-001643-47673889 | si | 24 | 31 | 56 |
| 0.80 | ev-v5-000312-f5062062 | si | 3 | 2 | 5 |
| segundo esquema | ev-v3-004329-a16d379b | si | 11 | 14 | 25 |
| orden limite | ev-v1-001358-a2b8ec0d | si | 12 | 15 | 27 |

15 de 15 devuelven su item. Lo que la normalizacion arregla: `0,75` pasaba de 0 segmentos a 68
(la cruda escribe `0.75`); `orden limite` de 0 a 15 (`límite`); `0.50` une `0.50` y `0.5`;
`spread` y `cuadro de gann` salen por la capa corregida (2 -> 5 y 0 -> 3 segmentos). Fallos
lexicos conocidos: `1:3` no casa con el `1.3` que escribe el ASR (0 segmentos; sale por la
afirmacion); `breakeven` (5 segmentos) solo con `--prefijo break`. Candidatos al glosario (no se
toca en F08): `1.3` -> `1:3` y `breakeven` -> `break even`.

### Rendimiento (pared, PowerShell `Measure-Command`, interprete incluido)
| Comando | ms |
|---|---|
| `kb find "break even"` | 1 040 |
| `kb at --video v4 --t 0:44:56` | 983 |
| `evidence list --video v5` (referencia) | 538 |

Construir el indice 0,75 s (4 277 documentos); cada consulta 9-48 ms. Bajo el limite de 2 s del
brief; sin cache.

### Determinismo y fuente
Dos ejecuciones = mismos bytes (test); toda linea de resultado con fuente (test sobre la salida
real); ninguna ruta absoluta; `kb at v4 0:44:56` devuelve `ev-v4-004447` (A-4), los segmentos
768-773, `fr-v4-9ad0ebb8/2696000` con su ruta y ninguna contradiccion (ninguno de esos items la
tiene).

## Que deberia observar el usuario
`uv run botsito kb find "break even" --top 10` imprime la cabecera `# tiempos de la cruda ...`,
diez lineas que empiezan por `ev-` o `tr-`, cada una con su `fr-*` de referencia, y `10
resultados`. `kb at --video v4 --t 0:44:56 --contexto` muestra items, segmentos, el fotograma
con su ruta `data/fotogramas/v4/png-1fps/002696000.png` y las afirmaciones. `--json` imprime solo
JSON. Sin `data/`, un `AVISO:` por stderr y resultados solo de evidencia.

## Que casos funcionan
Todo el alcance del brief.

## Que casos todavia no funcionan
- Sinonimos, stemming, ranking por relevancia, embeddings: fuera de alcance por decision del
  plan; el golden es la medida para reabrirlo con un ADR.
- `no_consta` de las propuestas y feedback (`fb-*`, 0 registros) no se indexan; la capa lo
  permite mas adelante.

## Limitaciones
- Lexica: lo que el ASR escribe distinto no se encuentra (`1.3`, `breakeven`, `m 15`); medido.
- La corregida se muestra sin tiempos propios (los tiempos son de la cruda): la cabecera lo dice
  (deuda F04 iii cerrada por declaracion).
- Con ~1 000 items (F11) la carga de YAML de evidencia sube a ~1,2 s; el cache queda como decision
  futura si se supera el limite de 2 s.

## Riesgos
Confundir "no aparece" con "no lo dijo": la busqueda es lexica y el aviso de cruda ausente
distingue el caso; `kb at` con margen grande devuelve muchos segmentos (maximo 120 s).

## Impacto sobre funcionalidades anteriores
`localizar_cita` (F07) se apoya en `buscar_secuencia`: mismo resultado (tests de F07 intactos,
341 items siguen localizados). `validation/contexto_evidencia.py` usa `dudas_de` de `corpus`
(sin cambio de comportamiento). El contrato de capas gana `retrieval`; ningun id ni fichero de
`knowledge/` cambia; F08 no escribe.

## Auditoria de cierre (dos agentes: codigo/tests y docs/proceso)
Hecha el 2026-09-08. El agente de docs/proceso se corto por el limite de sesion antes de
informar; esa revision la hizo la sesion siguiendo su guion (brief frente a codigo, ADR e
indice, MASTER_PLAN, PROJECT_STATE, HANDOFF, commits, ritual).

**Codigo y tests** (0 bloqueantes, 5 importantes, 6 menores; todo aplicado):
- I1 el comodin de `--frase` no acotaba el salto: `vale [...] vale` en v4 daba un resultado de
  740 s y 9 911 caracteres. Ahora una frase cruza como maximo 3 segmentos consecutivos
  (`MAX_SEGMENTOS_FRASE`); la misma consulta da 16 resultados de hasta 47 s.
- I2 la frase se buscaba en la corregida O en la cruda por segmento: `cuadro de gam` (literal
  de la cruda) daba 0 con `--frase`. Ahora se busca en los dos flujos y se unen las
  apariciones (`cuadro de gam` 1, `split` 5 como el AND).
- I3 `[corregida]` falsa en frases que cruzaban segmentos sin diferencias: ahora solo si algun
  segmento difiere; test.
- I4 `kb at --margen-s inf` daba traceback (`OverflowError`): ahora error de dominio.
- I5 `dudas` no enteras en `correcciones.jsonl` daban traceback (tambien en `knowledge
  validate`): ahora se ignoran.
- M1 `--frase` con `--prefijo` (se ignoraba) y `--tema` con `--solo cruda` (siempre 0) son
  errores. M2 `--tema` se valida contra `_temas.yaml`. M3 `t0/t1` de la contradiccion son los
  de sus items y los del fotograma los de su referencia. M4 anotado en ADR-0010: `10,000` y
  `10.000` -> `10` (miles y decimales no se distinguen). M5 corregida ilegible = aviso y se
  indexa solo la cruda; cruda sin segmentos = aviso. M6 tests anadidos: determinismo de la
  CLI real (dos ejecuciones, mismos bytes), `supersede`, carpeta de datos fuera del repo,
  `--frase` con `--desde`, regex de rutas Windows con barra invertida.
- Sin problema: token de busqueda en casos raros (`1.2.3`, `0,75r`, `40%`, `don't`, `ß`,
  `Decimal('10.0')` -> `10` sin notacion cientifica), AND por segmento y por union de campos,
  frase por campo, frase repetida en un segmento (un resultado), frase cruzando segmentos
  verificada a mano en v3, determinismo de `find` y `at --json`, golden 15/15 con y sin
  `data/` (corre en CI), `referencia_en` contra los 5 manifiestos reales, rutas siempre
  relativas, `kb at` por bloques, transcripciones reemplazadas fuera del indice, errores de
  fichero capturados (fuentes, manifiestos, cruda corrupta, evidencia rota, ajustes rotos),
  UTF-8 con stdout en pipe, contrato de capas (`retrieval` solo importa `corpus`, `evidence`,
  `comun`), rendimiento (`construir_indice` 0,71 s; `buscar('de')` 1 171 resultados en 0,49 s).

**Docs y proceso** (revision de la sesion): las 16 decisiones del brief estan en codigo, tests
y datos (decision 6 ajustada por I1/I2/M1 y anotada en el brief); ADR-0010 e indice, enmiendas
en ADR-0006 y ADR-0009 coherentes con `pyproject.toml`; MASTER_PLAN tabla B con `retrieval` y
Change Log con la entrada de F08; PROJECT_STATE (Current Feature, Waiting, componentes,
326 funciones / 471 casos, deuda F04 iii cerrada por declaracion, Next Feature F10, Next
Action = validar y ritual, Change Log); HANDOFF reescrito (estado, siguiente, lecciones de
F08); `knowledge/README.md` con el parrafo "Consultar". Commits de la rama con trailers;
ninguno toca `knowledge/spec` ni `knowledge/cases`. `state check` pasara tras el merge con el
`docs(state)` previsto (Completed Features exige este informe; Last Stable Commit = merge).


## Que debe decidir el usuario
1. Validar F08 y confirmar el cierre: merge `--no-ff` a `main` con tag `stable/F08` (cierra la
   fase 1: F03-F08).
2. Los dos candidatos al glosario (`1.3` -> `1:3`, `breakeven` -> `break even`): quedan anotados
   en Technical Debt; aplicarlos exige `corpus glossary apply` (sustituciones, sin retranscribir)
   y se decide al abrir la siguiente ronda de evidencia, no ahora.
3. Siguiente funcionalidad: F10 elicitation-kit (orden E), cuyo brief consumira `kb find` y `kb
   at` para las preguntas desde UNKNOWN.

## Que puede comprobar sin recursos especiales
`make check`; `uv run botsito kb find "0,75" --top 5`; `uv run botsito kb at --video v3 --t
0:01:36 --contexto` (reloj UTC+2, A-9); `uv run --no-sync pytest -q
tests/contract/test_golden_consultas_f08.py`; `git diff stable/F07..HEAD --stat`.

## Estado
WAITING_FOR_USER_VALIDATION
