---
status: ACTIVE
date: 2026-09-08
phase: F08
---

# 0010 · Busqueda de desarrollo: capa `retrieval`, indice en memoria, lexica y con fuente

## Decision
1. **Paquete `botsito.retrieval`** entre `spec` y `feedback` en el contrato de capas (ADR-0006
   enmendado): `cli -> validation -> viewer | mql5bridge -> engine -> cases -> spec -> retrieval
   -> feedback -> evidence | corpus | data | config -> comun -> domain`. Junta evidencia, crudas y
   fotogramas (cosa que hasta F07 solo hacia `validation`, ADR-0009 §3, enmendado: "validation y
   retrieval componen"); `cases` (F10) y `spec` (F11) pueden usarlo; podra buscar `fb-*` cuando
   F09 tenga registros sin cambiar el contrato. No importa `validation`, `cli`, `engine`, `viewer`
   ni `mql5bridge` (import-linter y `test_import_contracts`).
2. **Indice en memoria, regenerado en cada ejecucion** desde `knowledge/evidence` (todos los
   items; los reemplazados por `supersede` se marcan), las transcripciones ACTIVAS (cruda +
   corregida si existe; las reemplazadas no se indexan) y los manifiestos de fotogramas
   activos. Sin fichero de indice ni cache: 341 items + 3 936 segmentos se cargan en ~0,75 s y
   "regenerable" es trivialmente cierto. Determinismo: mismo repo + mismo `data/` = mismos bytes.
3. **Token de busqueda** = `evidence.verificacion.tokens` (F07) + acentos plegados (NFD sin marcas
   combinantes) + numeros con separador normalizados por `Decimal` (como
   `contradicciones.normalizar_valor`): `0,75` = `0.75` = `0.750`, `límite` = `limite`. Se
   aplica al indice y a la consulta; `tokens()` de F07 NO cambia (las citas siguen siendo fieles a
   la cruda). Fallos lexicos conocidos y medidos: `1:3` es un token que no casa con el `1.3` que
   escribe el ASR; `breakeven` no casa con `break even`. No se cambia el glosario aqui (cambiar
   `vocabulario` obliga a retranscribir).
4. **Consultas**: `kb find` = AND de tokens por documento (por campo en los items: cita,
   afirmacion, tema, valor, notas; por segmento en la cruda, con la corregida del mismo `n`);
   `--frase` = secuencia con comodin `[...]` via `evidence.verificacion.buscar_secuencia` (todas
   las apariciones, sin minimos de tokens; por campo en los items, sobre toda la cruda en los
   segmentos, cruzando segmentos); `--prefijo` = cada termino casa por inicio. Orden fijo
   (video, t0, evidencia antes que segmento, fuente); `--top` corta por ese orden; SIN puntuacion
   de relevancia, sinonimos, stemming ni embeddings (MASTER_PLAN, nota de F08: solo si la lexica
   demuestra ser insuficiente, y con otro ADR).
5. **`kb at`**: items cuyo `[t0 - m, t1 + m]` contiene el instante, segmentos de la cruda activa
   que tocan `[t - m, t + m]`, el fotograma de referencia y las contradicciones abiertas de esos
   items (`contradicciones.detectar`, no el YAML). Por bloques y, dentro, por tiempo. `no_consta`
   de las propuestas queda fuera (fuente de tramo, no de instante).
6. **Fotograma de referencia** (`corpus.manifiestos_fotogramas.referencia_en`): el mayor instante
   regular `<= t` que exista, saltando `segundos_ausentes_ms`, sin leer `index.jsonl`: "lo que ya
   estaba en pantalla en t". `corpus frames show` sigue siendo "el mas cercano por pts": son dos
   preguntas distintas y las dos quedan escritas.
7. **Toda linea de resultado lleva fuente** (`ev-*`, `tr-*/n` o `tr-*/n0-n1`, `fr-*/t_ms`,
   `contradiccion <tema>` con sus `ev-*`); rutas POSIX relativas al repo (nunca absolutas); avisos
   por stderr; `--json` con claves ordenadas y `[]` sin resultados. La corregida se muestra sin
   tiempos propios (los tiempos son de la cruda; deuda F04 iii cerrada por declaracion).
8. **Lo del corpus vive en `corpus`**: `pipeline_transcripcion.dudas_de` y `cargar_capas`
   (cruda, corregida, dudas) los usan `validation` y `retrieval`; nada se duplica.

## Problema que resuelve
Con 341 items y 3 936 segmentos, responder "que dijo el trader sobre X" o "que pasa en este
instante" exigia releer crudas y YAML a mano; el brief de F10 y las reglas de F11 necesitan
encontrar `ev-*` por tema y por instante con la fuente delante.

## Alternativas consideradas
(1) Busqueda dentro de `validation` o de la CLI. (2) Indice persistente (SQLite/JSON en `data/`).
(3) Embeddings o ranking BM25. (4) Aplicar las sustituciones del glosario a la consulta.

## Por que elegimos esta opcion
Una capa propia mantiene `validation` como conductor de validaciones y deja que `cases`/`spec`
consulten sin depender de `validation`. El indice en memoria cuesta menos de un segundo y no
puede caducar. La lexica con acentos y numeros normalizados devuelve el item esperado en las 15
consultas de referencia (golden), y los fallos que quedan son del ASR, medidos y propuestos al
glosario. La fuente obligatoria es la regla del proyecto (toda afirmacion trazable).

## Por que descartamos las demas
(1) `validation` conduce motor y validaciones; meter busqueda ahi mezcla responsabilidades y
obliga a `cases` a importar `validation` (prohibido). (2) Un indice persistente anade un fichero
que puede desincronizarse con `knowledge/` y `data/` sin ganar nada a este tamano. (3) El plan lo
prohibe salvo evidencia de insuficiencia; el golden es esa medida. (4) La corregida ya esta
indexada; reescribir la consulta ocultaria lo que el glosario no cubre.

## Impacto
`src/botsito/retrieval/{indice,consultas,salida}.py`, `src/botsito/cli.py` (`kb find | at`;
stderr en UTF-8), `src/botsito/corpus/{pipeline_transcripcion,manifiestos_fotogramas}.py`,
`src/botsito/evidence/verificacion.py` (`buscar_secuencia`; `localizar_cita` la usa),
`src/botsito/validation/contexto_evidencia.py`, `pyproject.toml` (capa), tests (unit, contrato,
golden `tests/golden/f08_consultas_referencia.yaml`), MASTER_PLAN tabla B, ADR-0006 y ADR-0009
(notas). Ningun id ni fichero de `knowledge/` cambia; F08 no escribe.

## Fecha / fase
2026-09-08 · F08

## Estado
ACTIVE
