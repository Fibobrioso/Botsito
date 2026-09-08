# F08 · evidence-retrieval

**Rama:** `feature/F08-evidence-retrieval` · **Fase:** 1 (cierra la base de conocimiento) ·
**Depende de:** F07 (`stable/F07`), y a traves de F07 de F04 (crudas) y F05 (fotogramas)

## Objetivo
Busqueda de DESARROLLO sobre la base de conocimiento: por texto (`kb find "break even"`) y por
instante (`kb at --video v4 --t 0:44:56`). Toda respuesta lleva fuente (id `ev-*`, `tr-*/n` de
segmento o `fr-*/<t_ms>` de fotograma), la busqueda es determinista y el indice se regenera desde
`knowledge/` + `data/` sin ficheros intermedios. Sirve al desarrollador (y al brief de F10) para
responder "que dijo el trader sobre X" y "que pasa en este instante" sin releer las crudas.
Lexica, sin embeddings (MASTER_PLAN, nota de F08): si la busqueda lexica demuestra ser
insuficiente, la decision de anadir otra cosa se registra en un ADR, no aqui.

## Hechos de partida (lo que hay al abrir la rama)
- 341 items de evidencia (`knowledge/evidence/<v>/ev-*.yaml`, F07): `cita_literal`, `afirmacion`,
  `tema`, `valor`, `notas`, `t0`/`t1`, `transcripcion` (`tr-*`, 337; todos citan las 5 activas),
  `fotogramas` (`fr-*/t_ms`, 7), `provenance: bot-v2` (42). `_contradicciones.yaml` (1 abierta).
  `_temas.yaml` (19 raices). Ningun item con `supersede` todavia (F09 creara los primeros).
- 5 crudas activas en `data/transcripciones/<v>/<motor>-<hash8>/cruda.jsonl` (segmentos con
  `palabras`, `senales`) y la capa `corregida.jsonl` + `correcciones.jsonl` (glosario v2, con
  `dudas` en la cabecera: v2 8, v3 13, v4 4). 3 936 segmentos (405 + 806 + 1020 + 1625 + 80).
- 5 manifiestos de fotogramas activos (1 fps completo; `index.jsonl` en
  `data/fotogramas/<v>/<carpeta>/`; `Fotogramas.referencias()` da las regulares existentes sin
  leer el indice; `corpus.fotogramas.mas_cercanos` es "menor |pts - t|").
- Tokenizacion canonica de F07 (`evidence.verificacion.tokens`: NFC, casefold, acentos
  CONSERVADOS, numeros con separador interior como un token, guiones y apostrofes como espacio,
  `...` fuera) y localizacion por trozos (`localizar_cita`, comodin `[...]`, minimos de 4 tokens
  y 3 por trozo, una sola localizacion dentro de una ventana).
- Medido por la revision de diseno sobre las 5 crudas: `0,75` 0 segmentos frente a `0.75` 71;
  `0.50` 26 frente a `0.5` 6; 10 % de los tokens con tilde o enie (`límite` 33 / `limite` 0,
  `operación` 15 / `operacion` 0); `1:3` 0 (la cruda escribe `1.3`, 23); `breakeven` 5 frente
  a `break` + `even` 70; `m15` 112 (`m` + `15` 13/20); `spread` 2 en cruda / 5 en corregida;
  `gann` 0 / 3. Carga: 5 crudas + 5 corregidas 0,29 s; 341 YAML de evidencia 0,39 s;
  tokenizar todo 0,08 s; arranque de la CLI 0,65 s.
- `evidence list --video --tema` y `corpus frames show` / `corpus transcript show` no cruzan
  evidencia con cruda ni con fotogramas, ni buscan por texto. `frames show` imprime rutas
  absolutas (`cli.py`), y `_segmento_en` mezcla avisos `#` en stdout.
- Deuda que F08 absorbe (PROJECT_STATE, F04 iii): las `palabras` de la cruda quedan bajo un
  texto corregido sin marcar.

## Decisiones de diseno (cerradas tras la revision del 2026-09-08)
1. **Paquete nuevo `botsito.retrieval`** (`indice.py`, `consultas.py`, `salida.py`) en el
   contrato de capas ENTRE `spec` y `feedback`: `cli -> validation -> viewer | mql5bridge ->
   engine -> cases -> spec -> retrieval -> feedback -> evidence | corpus | data | config -> comun
   -> domain`. Asi `cases` (F10) y `spec` (F11) pueden usarlo y `kb` podra buscar `fb-*` cuando
   F09 tenga registros sin cambiar el contrato. `retrieval` no importa `validation`, `cli`,
   `engine`, `viewer` ni `mql5bridge` (import-linter + `test_import_contracts`). Se tocan tambien
   MASTER_PLAN tabla B (lista de paquetes), ADR-0006 (nota), `test_tree.PACKAGES` y el comentario
   del contrato en `pyproject.toml`. ADR-0010 registra la capa, la decision lexica y la fuente
   obligatoria, y ENMIENDA ADR-0009 §3: "validation y retrieval componen evidencia y corpus".
2. **Lo que es del corpus vive en `corpus`**: `pipeline_transcripcion.dudas_de(carpeta)` y
   `cargar_capas(carpeta) -> Capas(cruda, corregida | None, dudas)`; `validation/contexto_evidencia`
   deja de tener su `_dudas_de` privada y usa eso. `retrieval` no duplica composicion.
3. **Indice en memoria, construido en cada ejecucion** desde `knowledge/evidence` (TODOS los
   items, los `supersede` marcados `[superseded por ev-…]`), las transcripciones ACTIVAS
   (cruda + corregida si existe; las reemplazadas no se indexan: 0 items las citan) y los
   manifiestos de fotogramas activos. Sin fichero de indice ni cache. Determinismo: dos
   ejecuciones del mismo comando sobre el mismo repo + `data/` = mismos bytes (test).
4. **Token de busqueda (`retrieval.indice.token_de_busqueda`)** = `tokens()` de F07 + plegado de
   acentos (NFD sin marcas combinantes; `ñ` -> `n`) + numeros con `,`/`.` normalizados via
   `Decimal` (como `contradicciones.normalizar_valor`: `0,75` = `0.75` = `0.750`; `0.50` = `0.5`).
   Se aplica al indice y a la consulta; `tokens()` de F07 NO cambia (las citas siguen siendo
   fieles). `1:3` -> `1`, `3` y `breakeven` siguen sin casar con `1.3` / `break even`: son fallos
   lexicos conocidos que el informe mide y propone al glosario (no se toca el glosario en F08:
   cambiar `vocabulario` obliga a retranscribir).
5. **Documentos**: (a) item de evidencia, con campos separados `cita_literal`, `afirmacion`,
   `tema` (puntos como espacio), `valor`, `notas`; el AND se evalua sobre la union de campos, la
   frase campo a campo (nunca cruzando cita -> afirmacion); (b) segmento de cruda activa: texto
   cruda + texto corregida del mismo `n` (AND POR SEGMENTO: los segmentos de Whisper son de 5-15
   s); la corregida se muestra solo cuando difiere, marcada `[corregida]`, SIN tiempos propios
   (los tiempos son de la cruda: deuda F04 iii, dicho en la cabecera de la salida); `dudas` de
   la cabecera de `correcciones.jsonl` salen como marca `<duda glosario>` y las `senales` del
   segmento como `<no_habla>` etc.
6. **`kb find <texto>`**: AND de tokens de busqueda por documento (por defecto); `--frase`
   exige la secuencia con comodines `[...]` usando `evidence.verificacion.buscar_secuencia(flujo,
   trozos) -> [(inicio, fin)]`, funcion NUEVA que devuelve TODAS las apariciones y no impone
   minimos de tokens (solo trozos no vacios); `localizar_cita` pasa a usarla (mismo resultado que
   hoy: sus minimos y la ventana se quedan en `localizar_cita`). En la cruda la frase se busca
   sobre el flujo de tokens de toda la transcripcion (cruda Y corregida) y puede cruzar hasta 3
   segmentos consecutivos (`MAX_SEGMENTOS_FRASE`; un salto mayor no es la misma frase); se listan
   los segmentos tocados, fuente `tr-*/n0-n1`; en los items, por campo. `--prefijo`: cada termino
   casa con los tokens que empiezan por el; no se combina con `--frase`. Sin sinonimos ni stemming.
   (Ajustes de la auditoria de cierre I1/I2/M1.)
7. **Filtros**: `--video`, `--tema` (raiz o tema completo; implica `--solo evidencia`: los
   segmentos no tienen tema), `--desde`/`--hasta` (exigen `--video`; `--desde` > `--hasta` es
   error), `--solo evidencia|cruda`, `--top N` (sin limite por defecto; `N < 1` es error).
   Orden fijo: (video, t0_ms, tipo: evidencia antes que segmento, id); `--top` corta por ese
   orden. Sin puntuacion de relevancia.
8. **`kb at --video <v> --t <h:mm:ss[.d]> [--margen-s 10]`** (misma convencion que `frames
   show`; `parse_ms` estricto; margen 0-120 s): en este orden y con fuente: items cuyo
   `[t0 - m, t1 + m]` contiene `t` (por t0); segmentos de la cruda activa que tocan `[t - m,
   t + m]` (por n, via `texto_entre`); el fotograma de referencia en `t`; contradicciones abiertas
   (`contradicciones.detectar(items)`, no el YAML) que involucran a alguno de esos items, una
   linea por contradiccion citando los `ev-*` implicados. `no_consta` de las propuestas queda
   FUERA de F08 (fuente `pr-*` de tramos de 5-15 min, no del instante; leerlas exige validar
   sellos).
9. **Fotograma de referencia** (una sola regla, en `corpus.manifiestos_fotogramas.referencia_en(
   fotogramas, t_ms) -> str | None`): el mayor instante regular `<= t_ms` que exista
   (`Fotogramas.referencias()`, saltando `ausentes_ms`), es decir, "lo que ya estaba en pantalla
   en t"; sin leer `index.jsonl`. Los extras solo aparecen via el campo `fotogramas` del item.
   `frames show` sigue siendo "el mas cercano por pts" (ADR-0010 lo anota). Si `data/fotogramas`
   esta en la maquina se anade la ruta; si no, solo la referencia.
10. **Rutas**: siempre POSIX relativas al repo (`data/fotogramas/v4/png-1fps/002696000.png`); si
    `[rutas].data` cae fuera del repo, `ruta: null` y aviso en stderr. Test: ninguna linea de la
    salida casa `^[A-Za-z]:/|/home/|/Users/`.
11. **Toda linea de resultado lleva fuente** (`ev-`, `tr-…/n`, `fr-…/t`, o `contradiccion` con
    sus `ev-*`); test sobre la salida real. Avisos por stderr, nunca en stdout; `--json` imprime
    SOLO el JSON (lista, `[]` si no hay resultados, codigo 0), claves ordenadas, `ensure_ascii`
    falso. stdout y stderr reconfigurados a UTF-8 en `main()`.
12. **Esquema JSON** (una entrada por resultado): `fuente` (str), `tipo`
    (`evidencia|segmento|fotograma|contradiccion`), `video` (str), `t0_ms`, `t1_ms` (int),
    `texto` (str: cita o texto de la cruda), `fotograma` (`{referencia, ruta | null}` o null),
    y `extra` (dict por tipo: evidencia -> `afirmacion, tema, valor, tipo_item, confianza,
    modalidad, transcripcion, provenance, fotogramas, supersede`; segmento -> `n, transcripcion,
    texto_corregido | null, senales, duda_glosario`; contradiccion -> `tema, valores, items`).
13. **Medicion del informe**: `tests/golden/f08_consultas_referencia.yaml` con 15 consultas
    (tabla de la revision: `break even`, `0,75`, `1:3`, `cartuchos`, `tres cartuchos`,
    `liquidez de m15`, `spread`, `utc`, `cuadro de gann`, `equal`, `3 pm`, `0.50`, `0.80`,
    `segundo esquema`, `orden limite`) con el `ev-*` esperado y, opcionalmente, un minimo de
    segmentos esperados. El golden `test_golden_consultas_f08` corre SIEMPRE: sin `data/`
    construye el indice solo con evidencia y exige el `ev-*`; con `data/` exige ademas los
    segmentos. El informe registra cuales necesitan `--prefijo` o la corregida y cuales fallan
    por la lexica (`1:3`, `breakeven`).
14. **Rendimiento**: `Measure-Command { uv run --no-sync botsito kb find "break even" }` de pared,
    interprete incluido, < 2 s en esta maquina; el coste dominante es cargar los YAML de
    evidencia (~1,1 ms/item), no tokenizar. Sin cache en F08.
15. **Sin escritura**: F08 no crea ni modifica nada en `knowledge/` ni `data/`. Sin
    dependencias nuevas. Nombre `kb` (MASTER_PLAN.html; `evidence find` seria falso porque
    tambien busca en el corpus).
16. **Errores**: video fuera de `fuentes.yaml` = error; video sin transcripcion activa =
    evidencia sola + aviso; cruda ausente en `data/` = aviso y resultados solo de evidencia
    (`--solo cruda` entonces da 0 resultados, codigo 0); fotogramas ausentes = referencia sin
    ruta; tiempo invalido, `--frase` mal formada, `--top < 1`, margen fuera de 0-120 = error sin
    traceback.

## Alcance cerrado (que SI)
- `corpus.pipeline_transcripcion.{dudas_de, cargar_capas}`; `validation.contexto_evidencia` usa
  `dudas_de`. `corpus.manifiestos_fotogramas.referencia_en`.
  `evidence.verificacion.buscar_secuencia` (y `localizar_cita` sobre ella).
- `botsito.retrieval`: `indice.py` (`token_de_busqueda`, `Documento`, `Indice`,
  `construir_indice(repo, carpeta_datos)`), `consultas.py` (`buscar`, `en_instante`),
  `salida.py` (tabla y JSON deterministas, rutas relativas).
- CLI `kb find` / `kb at` con las opciones de las decisiones 6-8; stderr UTF-8.
- ADR-0010 + indice; enmiendas en ADR-0006 y ADR-0009 (notas).
- Contratos: `pyproject.toml` layers, `test_import_contracts` (`retrieval`), `test_tree`.
- Tests: `tests/unit/test_retrieval.py` con fixture propia (crudas y corregidas escritas a mano
  con `a_jsonl`, manifiestos por dict, `index.jsonl` sin PNG, items con `escribir_item`,
  contradiccion con dos valores): token de busqueda (acentos, coma/punto), determinismo, AND por
  segmento, frase cruzando segmentos, prefijo, filtros y errores, orden y `--top`, instante con
  margen, fotograma de referencia con y sin `data/`, corregida marcada sin tiempos, dudas y
  senales, superseded, cruda ausente, rutas relativas, JSON y stdout/stderr; `test_cli.py` (kb);
  `test_verificacion.py` (`buscar_secuencia`); `test_fotogramas.py` (`referencia_en`); golden
  de 15 consultas.
- Informe `docs/validation/F08-evidence-retrieval.md` (medicion 13 y 14).
- Docs: `knowledge/README.md`, HANDOFF, PROJECT_STATE, MASTER_PLAN (tabla A fila F08, tabla B,
  Change Log).

## Fuera de alcance (que NO)
- Embeddings, ranking por relevancia, sinonimos, stemming, corrector de la consulta.
- `no_consta` de propuestas, propuestas rechazadas, feedback (0 registros; la capa lo permite
  en el futuro), spec (F11).
- Indice persistente, servidor, interfaz web (F25). Cambios en el glosario.
- Escribir evidencia, feedback o propuestas desde `kb`. Diarizacion.

## Entradas
`knowledge/evidence/**`, `knowledge/corpus/{fuentes,manifest}.yaml`,
`knowledge/corpus/transcripciones/*.yaml`, `knowledge/corpus/fotogramas/*.yaml`,
`data/transcripciones/**/{cruda,corregida,correcciones}.jsonl`, `data/fotogramas/**/index.jsonl`,
`config/ajustes` (carpeta de datos). Codigo reutilizado: `evidence.verificacion.tokens`,
`evidence.modelo.cargar_evidencia`, `evidence.contradicciones.{detectar,normalizar_valor}`,
`corpus.pipeline_transcripcion.{cargar_cruda,cargar_corregida}`,
`corpus.manifiestos_transcripcion.{cargar_todos,activos,carpeta_de}`,
`corpus.manifiestos_fotogramas.{cargar_todos,activos,carpeta_de,Fotogramas.referencias}`,
`corpus.fotogramas.{cargar_indice,nombre_fichero,referencia}`,
`corpus.transcripcion.{parse_ms,formato_ms,texto_entre}`, `corpus.inventario.cargar_fuentes`.

## Salidas (ficheros)
`src/botsito/retrieval/{__init__,indice,consultas,salida}.py`; `src/botsito/cli.py` (`kb`);
`src/botsito/corpus/{pipeline_transcripcion,manifiestos_fotogramas}.py`,
`src/botsito/evidence/verificacion.py`, `src/botsito/validation/contexto_evidencia.py`;
`pyproject.toml`; `tests/unit/{test_retrieval,test_cli,test_verificacion,test_fotogramas,test_tree}.py`,
`tests/contract/{test_import_contracts,test_golden_consultas_f08}.py`,
`tests/golden/f08_consultas_referencia.yaml`; `docs/adr/0010-*.md` + indice, notas en 0006/0009;
`docs/validation/F08-evidence-retrieval.md`; `knowledge/README.md`; PROJECT_STATE, HANDOFF,
MASTER_PLAN.

## Tests
Ver "Alcance cerrado". Casos negativos obligatorios: consulta vacia; sin resultados (tabla "0
resultados" / JSON `[]`, codigo 0); `--frase` con comodin al borde; video inexistente; video sin
transcripcion activa; tiempo `0:99:99`; `--desde` sin `--video`; `--desde` > `--hasta`; `--top 0`;
margen 121; cruda ausente (aviso en stderr); fotogramas ausentes (referencia sin ruta); `--json`
sin rutas absolutas, claves ordenadas y nada mas en stdout; `--tema` descarta segmentos.

## Criterio de aceptacion
`make check` verde; contrato de capas con `retrieval`; `kb find` y `kb at` deterministas (test
de bytes); 100 % de las lineas de resultado con fuente (test sobre la salida real); golden de 15
consultas en verde con y sin `data/` (el informe explica los fallos lexicos conocidos); `kb find`
< 2 s de pared sobre los 5 videos; nada escrito en `knowledge/` ni `data/`.

## Riesgos
- Errores del ASR que el glosario no corrige (`1.3`, `breakeven`, `m 15`): medidos en el golden y
  propuestos al glosario en el informe; no se cambia el glosario en F08.
- Segmentos con `no_habla` o `dudas`: marcados en la salida para que el lector desconfie.
- `kb at` con margen grande devuelve muchos segmentos: por defecto 10 s, maximo 120 s.
- Tentacion de meter ranking: fuera de alcance; el orden temporal es la unica ordenacion.
- Con ~1 000 items (F11) la carga de YAML sube a ~1,2 s: el cache queda como decision futura
  (ADR) si el limite de 2 s se supera.

## Revision de diseno (agente, 2026-09-08, antes de programar)
Aceptados (todos con cambio en el brief): B1 token de busqueda con acentos plegados y numeros
normalizados (decision 4; `0,75` daba 0 segmentos frente a 71, `limite` 0 frente a 33); B2
`--frase` no puede ir por `localizar_cita` (minimos de 4/3 tokens, una ventana, una
localizacion): `buscar_secuencia` nueva y AND por segmento (5-6); B3 `no_consta` fuera y
contradicciones por `detectar` con `ev-*` (8, 11); I1 capa `retrieval` entre `spec` y
`feedback`, `dudas_de`/`cargar_capas` en `corpus`, enmienda de ADR-0009 §3, tabla B, ADR-0006,
`test_tree` (1, 2); I2 una sola regla de fotograma de referencia en `corpus` (9); I3 rutas
relativas POSIX y test (10); I4 golden con y sin `data/` (13); I5 fixture a mano sin ffmpeg
(Tests); I6 todos los items con `supersede` marcado, `--tema` implica evidencia, `--desde`
exige `--video`, frase por campo, evidencia antes que segmento (3, 5, 7); I7 esquema JSON
(12); I8 corregida sin tiempos propios y `<duda glosario>` desde `correcciones.jsonl` (5); I9
metodo de medida y coste dominante (14); M1 `--video/--t/--margen-s` (8); M2 `--top` sin limite
por defecto (7); M3 nombre `kb` (15); M4 stderr UTF-8 (11); M5/M6 fallos lexicos medidos y
documentados (4, 13); M7 `provenance` en vez de `marca_heredada` (Hechos, 12); M8 orden en
`at` (8); M9 errores (16). Descartados: ninguno.

## Que habilita
F10 (kit de elicitacion: preguntas desde UNKNOWN con la evidencia y el instante a mano), F11
(escribir reglas citando `ev-*` encontrados por tema), y cierra la fase 1 (F03-F08).
