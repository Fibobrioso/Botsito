# F08 · evidence-retrieval

**Rama:** `feature/F08-evidence-retrieval` · **Fase:** 1 (cierra la base de conocimiento) ·
**Depende de:** F07 (`stable/F07`), y a traves de F07 de F04 (crudas) y F05 (fotogramas)

## Objetivo
Busqueda de DESARROLLO sobre la base de conocimiento: por texto (`kb find "break even"`) y por
instante (`kb at v4 0:44:56`). Toda respuesta lleva fuente (id `ev-*`, `tr-*/n` de segmento o
`fr-*/<t_ms>` de fotograma), la busqueda es determinista y el indice se regenera desde
`knowledge/` + `data/` sin ficheros intermedios. Sirve al desarrollador (y al brief de F10) para
responder "que dijo el trader sobre X" y "que pasa en este instante" sin releer las crudas.
Lexica, sin embeddings (MASTER_PLAN, nota de F08): si la busqueda lexica demuestra ser
insuficiente, la decision de anadir otra cosa se registra en un ADR, no aqui.

## Hechos de partida (lo que hay al abrir la rama)
- 341 items de evidencia (`knowledge/evidence/<v>/ev-*.yaml`, F07): `cita_literal`, `afirmacion`,
  `tema`, `valor`, `notas`, `t0`/`t1`, `transcripcion` (`tr-*`, 337), `fotogramas` (`fr-*/t_ms`,
  7), `marca_heredada` (42). `_contradicciones.yaml` (1 abierta). `_temas.yaml` (19 raices).
- 5 crudas activas en `data/transcripciones/<v>/<motor>-<hash8>/cruda.jsonl` (segmentos con
  `palabras`, `senales`) y la capa `corregida.jsonl` + `correcciones.jsonl` (glosario v2, con
  `dudas` en la cabecera). 3 936 segmentos en total (405 + 806 + 1020 + 1625 + 80).
- 5 manifiestos de fotogramas activos (1 fps completo; `index.jsonl` en
  `data/fotogramas/<v>/<carpeta>/`; `corpus.fotogramas.mas_cercanos` y `referencia`).
- Ya existe la tokenizacion canonica de F07 (`evidence.verificacion.tokens`: NFC, casefold,
  numeros con separador interior como un token, guiones y apostrofes como espacio, `...` fuera) y
  la localizacion por trozos (`localizar_cita`, comodin `[...]`).
- `evidence list --video --tema` (tabla) y `corpus frames show` / `corpus transcript show`
  (lectura por instante o tramo) son las unicas consultas hoy: no cruzan evidencia con cruda ni
  con fotogramas, ni buscan por texto.
- Deuda que F08 absorbe (PROJECT_STATE, F04 iii): las `palabras` de la cruda quedan bajo un
  texto corregido sin marcar; cualquier salida que muestre la corregida con tiempos debe decir
  que los tiempos son de la cruda.

## Decisiones de diseno (propuestas; se cierran tras la revision de diseno)
1. **Paquete nuevo `botsito.retrieval`** (modulos `indice.py`, `consultas.py`, `salida.py`),
   hermano de `feedback` en el contrato de capas: `... -> spec -> feedback | retrieval ->
   evidence | corpus | data | config -> comun -> domain`. Junta evidencia + crudas + fotogramas
   (cosa que hoy solo puede hacer `validation`) sin meter busqueda en `validation` (que conduce
   motor y validaciones) ni en la CLI. `cases` (F10) podra importarlo. ADR-0010 registra la capa
   y la decision lexica. `test_import_contracts` gana la regla "retrieval no importa validation
   ni cli" y el contrato de import-linter se actualiza.
2. **Indice en memoria, construido en cada ejecucion** desde `knowledge/evidence`, los manifiestos
   activos y `data/`. Sin fichero de indice: 341 items + ~4 000 segmentos se indexan en < 1 s y
   asi "regenerable" es trivialmente cierto y no hay cache que caduque. Determinismo: mismo
   repo + mismo `data/` = misma salida byte a byte (orden fijo, sin hora ni rutas absolutas en la
   salida; `--json` ordena claves).
3. **Unidades indexadas (documentos)**: (a) item de evidencia: texto = `cita_literal` +
   `afirmacion` + `tema` (con puntos como espacio) + `valor` + `notas`; (b) segmento de cruda
   activa: texto = cruda y, si existe, corregida del mismo `n` (se busca en ambas capas; se
   muestra la cruda y, cuando difiere, la corregida marcada `[corregida]`); los segmentos de
   transcripciones reemplazadas NO se indexan (solo las activas; los items que citan una
   reemplazada siguen saliendo por su propio texto y su aviso). Los fotogramas no tienen texto:
   entran como "fotograma mas cercano" de cada resultado.
4. **Consulta por texto (`kb find`)**: tokens de la consulta con la MISMA `tokens()` de F07; por
   defecto todos los tokens deben aparecer en el documento (AND, sin orden); `--frase` exige la
   secuencia (con los mismos comodines `[...]` y reglas de F07, via `localizar_cita` sobre los
   segmentos y una busqueda de subsecuencia sobre los items); `--prefijo` casa `break` con
   `breakeven` (tokens que empiezan por el termino). Sin sinonimos ni stemming: lo que el
   glosario no corrige no se encuentra, y el informe lo mide (lista de consultas de referencia).
5. **Orden y limites**: resultados ordenados por (video, t0, tipo de documento, id); `--top N`
   corta por ese orden, no por relevancia. Sin puntuacion de relevancia en F08 (lexico de
   desarrollo: el usuario acota con `--video`, `--tema`, `--desde/--hasta`, `--solo
   evidencia|cruda`).
6. **Consulta por instante (`kb at <video> <h:mm:ss> [--margen 10s]`)**: devuelve, en este
   orden y con fuente: items de evidencia cuyo `[t0, t1]` ampliado por el margen contiene el
   instante; segmentos de la cruda activa que tocan `[t - margen, t + margen]`; el fotograma mas
   cercano (`fr-*/t_ms`, ruta local si existe); contradicciones abiertas que involucran a alguno
   de esos items; si el instante cae en una propuesta con `no_consta`, se listan los temas que
   NO constan en ese tramo (para no volver a buscarlos).
7. **Fotograma mas cercano de cada resultado**: `fr-<activo>/<t_ms>` con `t_ms` = el mayor
   instante regular <= t0 del resultado que exista en el manifiesto (o el extra mas cercano si
   hay); si los fotogramas no estan en la maquina se imprime la referencia igualmente (es
   citable) y la ruta se omite.
8. **Toda linea de resultado lleva fuente** y un test lo exige sobre la salida real: cada linea
   de resultado empieza por `ev-`, `tr-…/n` o `fr-…/t`; no existe modo "solo texto".
9. **Salida**: tabla legible por defecto (una linea por resultado + contexto opcional
   `--contexto` que imprime la cita/segmento completo) y `--json` (lista de objetos con
   `fuente`, `video`, `t0_ms`, `t1_ms`, `tipo`, `texto`, `fotograma`, `extra`) para el kit de F10.
10. **Sin escritura**: F08 no crea ni modifica nada en `knowledge/` ni `data/`; el hook y los
    tests de historial no cambian. Sin dependencias nuevas.
11. **Medicion del informe**: lista cerrada de 15 consultas de referencia (frases del informe de
    investigacion y de las ambiguedades A-1..A-12, p. ej. "break even", "0,75", "cartuchos",
    "liquidez de m15", "spread", "utc") con el resultado esperado (al menos un `ev-*` conocido);
    se mide cuantas devuelven el item esperado y cuantas necesitan `--prefijo` o la capa
    corregida. Es la evidencia de "la lexica basta / no basta".
12. **Rendimiento**: `kb find` sobre los 5 videos < 2 s en esta maquina (medido en el informe);
    si no, se anade un cache opcional en `data/indice/` en un ADR, no antes.

## Alcance cerrado (que SI)
- `botsito.retrieval`: `indice.py` (documentos, tokens, construccion desde repo + carpeta de
  datos; segmentos de activas con capa corregida si existe), `consultas.py` (`buscar(indice,
  consulta, opciones)`, `en_instante(indice, video, t_ms, margen_ms)`), `salida.py` (tabla y
  JSON, ambas deterministas).
- CLI: `botsito kb find <texto> [--video] [--tema] [--desde --hasta] [--solo evidencia|cruda]
  [--frase] [--prefijo] [--top N] [--contexto] [--json]` y `botsito kb at <video> <t>
  [--margen 10s] [--json]`. Errores de dominio sin traceback (video desconocido, tiempo
  invalido, `--frase` mal formada, cruda ausente = aviso y resultados solo de evidencia).
- ADR-0010 (capa `retrieval`, indice en memoria, lexico sin embeddings, fuente obligatoria).
- Contratos: import-linter y `test_import_contracts` (`retrieval` no importa `validation`, `cli`,
  `engine`, `viewer`, `mql5bridge`); `test_tree` conoce el paquete.
- Tests unitarios con un repo temporal (fixture reutilizando `_knowledge_con_cruda` del F07 en
  `test_cli.py` o una fixture propia): indice determinista (dos construcciones = misma salida),
  AND/frase/prefijo, filtros, orden, `--top`, instante con margen, fotograma mas cercano con y
  sin `index.jsonl`, contradicciones en `at`, `no_consta` en `at`, cruda ausente, transcripcion
  reemplazada no indexada, cada linea con fuente, JSON con claves ordenadas y sin rutas
  absolutas; test sobre el repo real (si hay `data/`): las 15 consultas de referencia
  (`tests/golden/f08_consultas_referencia.yaml`) devuelven su `ev-*` esperado.
- Informe `docs/validation/F08-evidence-retrieval.md` con la medicion (decision 11 y 12).
- Docs: `knowledge/README.md` (como consultar), `docs/HANDOFF.md`, PROJECT_STATE, MASTER_PLAN
  (tabla A fila F08 hecha; fila H.2 si aplica; Change Log).

## Fuera de alcance (que NO)
- Embeddings, ranking por relevancia, sinonimos, stemming, corrector ortografico de la consulta.
- Busqueda sobre propuestas rechazadas, feedback (F09: 0 registros) o spec (F11).
- Indice persistente, servidor, interfaz web (el viewer es F25).
- Escribir evidencia, feedback o propuestas desde `kb` (eso es `evidence propose/accept`).
- Diarizacion o atribucion de voz.

## Entradas
`knowledge/evidence/**`, `knowledge/evidence/_contradicciones.yaml`, `knowledge/_proposals/pr-*.yaml`
(solo `no_consta` y tramos), `knowledge/corpus/transcripciones/*.yaml` y
`knowledge/corpus/fotogramas/*.yaml` (activos), `data/transcripciones/**/{cruda,corregida}.jsonl`,
`data/fotogramas/**/index.jsonl`, `config/ajustes` (carpeta de datos). Codigo reutilizado:
`evidence.verificacion.tokens/localizar_cita`, `evidence.modelo.cargar_evidencia`,
`evidence.contradicciones.detectar`, `corpus.pipeline_transcripcion.cargar_cruda` (+ corregida),
`corpus.manifiestos_transcripcion.{cargar_todos,activos,carpeta_de}`,
`corpus.manifiestos_fotogramas.{cargar_todos,activa_de,carpeta_de}`, `corpus.fotogramas.{cargar_indice,
mas_cercanos,referencia}`, `corpus.transcripcion.{parse_ms,formato_ms}`.

## Salidas (ficheros)
`src/botsito/retrieval/{__init__,indice,consultas,salida}.py`; `src/botsito/cli.py` (subcomando
`kb`); `pyproject.toml` (contrato de capas); `tests/unit/test_retrieval.py`, `tests/unit/test_cli.py`
(kb), `tests/contract/test_import_contracts.py`, `tests/golden/f08_consultas_referencia.yaml`,
`tests/contract/test_golden_consultas_f08.py`; `docs/adr/0010-*.md` + indice;
`docs/validation/F08-evidence-retrieval.md`; `knowledge/README.md`; PROJECT_STATE, HANDOFF,
MASTER_PLAN.

## Tests
Ver "Alcance cerrado". Casos negativos obligatorios: consulta vacia; consulta cuyos tokens no
aparecen (0 resultados, salida "0 resultados", codigo 0); `--frase` con comodin al borde; video
inexistente; tiempo `0:99:99`; `--desde` > `--hasta`; `--top 0`; cruda ausente en `data/`
(aviso, no error); fotogramas ausentes (referencia sin ruta); item que cita una transcripcion
reemplazada (sale por su texto, con aviso); `--json` sin rutas absolutas y con claves ordenadas.

## Criterio de aceptacion
`make check` verde; contrato de capas con `retrieval`; `kb find` y `kb at` deterministas
(mismo comando dos veces = misma salida byte a byte, test); 100 % de las lineas de resultado con
fuente (test sobre la salida real); las 15 consultas de referencia devuelven su item esperado
(o el informe explica cuales no y por que); `kb find` < 2 s sobre los 5 videos; nada escrito en
`knowledge/` ni `data/`.

## Riesgos
- La cruda tiene errores del ASR que el glosario no corrige (`m 15`, `1.3`): una consulta
  "M15" o "1:3" no encontraria "m 15" ni "1.3". Mitigacion: la consulta se tokeniza igual que la
  cruda (`m15` -> `m15`, no casa con `m 15`; documentado) y las 15 consultas de referencia lo
  miden; el informe propone terminos al glosario si hace falta (no se cambia el glosario en F08:
  cambiar `vocabulario` obliga a retranscribir).
- Segmentos con `no_habla` o `dudas`: se muestran con su senal para que el lector desconfie.
- Un margen grande en `kb at` devuelve muchos segmentos: por defecto 10 s, maximo 120 s.
- Tentacion de meter ranking: fuera de alcance; el orden temporal es la unica ordenacion.

## Revision de diseno (agente, antes de programar)
Pendiente: se rellena con los hallazgos aceptados y descartados (con motivo).

## Que habilita
F10 (kit de elicitacion: preguntas desde UNKNOWN con la evidencia y el instante a mano), F11
(escribir reglas citando `ev-*` encontrados por tema), y cierra la fase 1 (F03-F08).
