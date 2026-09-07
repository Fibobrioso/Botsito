# F07 · evidence-extraction

**Rama:** `feature/F07-evidence-extraction` · **Fase:** 1 · **Depende de:** F04, F05, F06 (y de
los previos `stable/F05-previos-F07`: glosario v2, 5 videos retranscritos, copia en Drive)

## Objetivo
Poblar `knowledge/evidence/` con items cuya cita sea verificable por maquina: lo que se oye,
localizado en la CRUDA de la transcripcion activa del video (`tr-*`, ADR-0007 §7); lo que se ve,
anclado a un fotograma real (`fr-<id>/<t_ms>`, ADR-0008 §6) o a un fichero `material_adicional`
del corpus. Toda propuesta de item queda registrada en `knowledge/_proposals/` con su prompt,
modelo, salida y decision humana (MASTER_PLAN H, fila "Propuestas de LLM"); el proponente
nunca escribe en `knowledge/evidence/`. Objetivo del plan (tabla A): >= 80 items, 100 % de
citas verificadas, precision y recall del proponente medidos sobre un tramo de 10 min y
reportados como informacion (sin umbral).

## Hechos de partida (lo que hay al abrir la rama)
- Transcripciones activas (glosario v2, `initial_prompt`): `tr-v1-...-bbd8a931` (405 seg),
  `tr-v2-...-28391c2c` (806), `tr-v3-...-270a4851` (1020), `tr-v4-...-a8d1bccc` (1625),
  `tr-v5-...-3c6fbb57` (80). Crudas en `data/transcripciones/<v>/<carpeta>/cruda.jsonl` (esta
  maquina y Drive). Las `palabras` con tiempo por palabra existen en la cruda; la corregida solo
  es ayuda de lectura (cambia con el glosario bajo el mismo id): la cita se verifica contra la
  cruda.
- Fotogramas activos `fr-v1-5a2a42c3`, `fr-v2-c5a09508`, `fr-v3-982da728`, `fr-v4-9ad0ebb8`,
  `fr-v5-718ecabb` (1 fps completo + obligatorios); `manifiestos_fotogramas.referencias_conocidas`
  ya devuelve el conjunto citable (`fr-<id>/<t_ms>` de cada fotograma que existe + rutas
  `material_adicional`; `heredado_v2` excluido). Hoy `evidence.validar_contra_manifiesto` acepta
  rutas heredadas de `manifest.ficheros`: F07 lo cambia.
- Modelo F06: `EvidenceItem` con 12 campos obligatorios y `fotogramas`, `valor`, `supersede`,
  `notas` opcionales; id = hash del contenido; 0 items reales; `evidence new` comprueba contra
  el manifiesto antes de escribir.
- Material citable ya leido (PROJECT_STATE "Lineamientos ... y hechos del corpus pendientes de
  evidencia", informes F04 y F05): 33 marcas heredadas revisadas sobre large-v3 (28 coinciden),
  23 citas del informe de investigacion del 2026-09-03, obligatorios de F05 (Excel V3 0:28:56
  `2,83 / -0,75 / 3,3`; ratios 4,08 / 3,94 V2 0:33:21; caja 0,75 = 1,19537 V4 0:12:30), relojes
  UTC+2 (candidatos A-9), ficha de reglas en Word (`fr-v3-982da728/101000`, 12 filas con
  respuesta del trader), v5 (0,8 "SL por defecto", reentrada tras equal, RR sobre 1 %, 1:3 con
  1:4), backtest de abril (xlsx + 6 capturas), V4 1:28:20 (riesgo por operacion).
- Las 30 reglas RN de Bot v2 (`Operativa_Cerrada.md`) NO estan en el repositorio ni en Drive: lo
  importable de Bot v2 es lo que cita el informe de investigacion y la ficha del Word; entra con
  `provenance: bot-v2` solo si se re-cita sobre large-v3 o un fotograma; si no, UNKNOWN (H).
- No hay clave de API de ningun proveedor de LLM en la maquina ni en la configuracion; el
  proponente disponible es esta sesion de Claude Code (modelo `claude-fable-5-1`).

## Decisiones de diseno (tras la revision de diseno del 2026-09-07)
1. **Campo opcional `transcripcion`** (id `tr-*`) en `EvidenceItem`; entra en el contenido
   canonico (no hay items previos). `modalidad: audio` o `ambas` lo exige y debe ser la
   transcripcion ACTIVA del `video_id` al crear el item (`evidence new`/`accept` lo comprueban);
   `modalidad: pantalla` lo prohibe. `knowledge validate` verifica SIEMPRE contra la cruda
   citada (inmutable, en disco y en Drive), nunca contra "la activa del momento": una
   retranscripcion no invalida items que nadie edito. Si una transcripcion citada queda
   reemplazada, `validate` emite UN aviso agregado por transcripcion ("N items citan `tr-...`,
   reemplazada por `tr-...`; M se localizan tambien en la nueva") para que F08/F11 decidan
   re-citar; comprueba ademas que el id exista y sea del `video_id`.
2. **Localizacion de la cita de audio por tokens** (`evidence/verificacion.py`, puro, SIN
   importar `corpus`: recibe segmentos por un `Protocol` estructural `SegmentoCitable` con
   `n`, `t0_ms`, `t1_ms`, `texto`, `senales`, `palabras`; los `Segmento` reales lo cumplen y los
   entrega `validation/knowledge.py` o la CLI, que si pueden componer ambas capas). Regla:
   cruda y cita se normalizan igual (NFC, `casefold`, tokens `\w+` conservando `.`/`,`/`:`
   interiores de digitos: `0.75`, `16,5`, `1:3`; guiones y apostrofes = espacio; acentos
   conservados; los `...`/`…` del ASR se eliminan) y se comparan POR TOKENS (`3` no casa en
   `33`, `1.3` no en `11.3`). Comodin `[...]` (corchetes; la cruda nunca lo escribe): maximo 2
   por cita, cada trozo >= 3 tokens, cita total >= 4 tokens; los trozos se buscan en orden
   estricto y sin solape dentro de los tokens de los segmentos que tocan `[t0 - TOL, t1 + TOL]`.
   Sin otro comodin. `Localizacion` devuelve el numero de coincidencias del primer trozo en la
   ventana (mas de una no es error: el informe lo lista).
3. **Tiempo real de la cita por `palabras`.** Tras localizar por tokens sobre `texto`, los
   tokens se alinean con `palabras` por offsets de caracteres sin espacios (la concatenacion de
   `palabras` sin espacios reproduce `texto` sin espacios; con espacios no: `9` + `.65`) y
   `Localizacion` lleva `t0_ms`/`t1_ms` de la primera y la ultima palabra y los segmentos `n`.
   Regla: ese tramo debe caer dentro de `[t0 - TOL, t1 + TOL]` con `TOL = 2 s` (constante
   tecnica); si no, error "la cita esta en h:mm:ss.mmm-h:mm:ss.mmm: ajusta t0/t1". Un segmento
   sin `palabras` cae al `[t0_ms, t1_ms]` del segmento con aviso. F08 hereda tiempos de palabra
   sin tocar el esquema (los `n` NO se guardan en el item: cambian entre transcripciones).
4. **Cita de pantalla**: `modalidad: pantalla` o `ambas` exige al menos una referencia
   `fr-<id>/<t_ms>` del `video_id` del item con `t_ms` en `[t0 - 1 s, t1 + 1 s]`, existente en
   `referencias_conocidas`; `modalidad: audio` no admite `fotogramas`. Una ruta
   `material_adicional` solo se cita ACOMPANADA de un `fr-*` del mismo tramo que muestra o
   comenta ese fichero (v5 con la pantalla de Analytics); un item con solo `material_adicional`
   es error. Las cifras del xlsx que no aparecen en ningun video no son evidencia del trader en
   F07 (quedan como golden de F26 en PROJECT_STATE). Lo que dice una cita de pantalla lo afirma
   la persona que la acepta (`fotograma visto`); la maquina garantiza referencia y tramo.
5. **`validar_contra_manifiesto(items, manifiesto, contexto)`**: `ContextoEvidencia`
   (`referencias`, `crudas: Callable[[tid], Sequence[SegmentoCitable] | None]`, transcripciones
   conocidas con su video, activas y reemplazos, taxonomia de temas). Si algun item lleva
   `fotogramas` y no hay `referencias`, error "faltan referencias conocidas" (se acabo aceptar
   rutas heredadas de `manifest.ficheros`). Sin cruda en la maquina: AVISO agregado "citas de
   audio no verificables aqui". `evidence new` y `accept` construyen siempre el contexto.
6. **Propuestas trazables** en `knowledge/_proposals/<id>.yaml`, con
   `propuesta_id = pr-<video>-<t0hhmmss>-<t1hhmmss>-<hash8 de prompt_sha256 + modelo +
   generado_el>` (formato en `comun/ids.py`). Regimen: manual y versionado; editable SOLO en
   los campos de decision. Contenido: `video_id`, `transcripcion`, `t0`, `t1`, `prompt` integro
   y `prompt_sha256`, `modelo`, `proponente` (`llm` | `humano`), `generado_el`, `contexto`
   (segmentos del tramo con `n`, `t0_ms`, `t1_ms`, `texto`, `senales`; sin `palabras`; y las
   referencias `fr-*` del tramo), `temas_buscados` (lista cerrada del esqueleto), `items`
   (cada uno con cita) y `no_consta: [{tema, motivo}]` (lo que se busco y no consta). Tras
   `--check`, `salida_sha256` = hash canonico de `items` + `no_consta` + `prompt_sha256` +
   `modelo` + `contexto`; `accept`/`reject`/`validate` lo recomputan y rechazan una salida
   cambiada despues del check ("crea otra propuesta"). Fuera del hash solo `decision`,
   `decidido_por`, `decidido_el`, `metodo_revision`, `motivo`, `evidence_id`.
7. **Guardias mecanicas de calidad** en `--check` y en `accept`: cita >= 4 tokens; `tema` con
   raiz en la taxonomia (`knowledge/evidence/temas.yaml`, manual y versionado; cerrada para F07,
   F11 la hara normativa); `valor` solo si su normalizacion coincide con un token numerico de
   la cita o con el vocabulario cerrado del fichero de temas (`cuerpo`, `cierre`, `toque`,
   `mecha`, `si`, `no`); dos items (en propuestas o evidencia) con la misma cita normalizada =
   error; dos items del mismo `tema` con localizaciones solapadas = error salvo modalidad
   distinta; cita localizada en un segmento con `senales` o listado en `dudas` de
   `correcciones.jsonl` fuerza `confianza != alta` y lo anota en `notas`; cada `tema_buscado`
   debe aparecer en `items` o en `no_consta`; una cita normalizada ya rechazada en otra
   propuesta = AVISO.
8. **CLI** (`botsito evidence ...`): `propose --video --t0 --t1` (esqueleto: contexto de la cruda
   activa, referencias del tramo, prompt canonico de `knowledge/_proposals/PROMPT.md` con
   version en cabecera, `temas_buscados`, `items: []`, `no_consta: []`; no llama a ningun
   modelo); `propose --check <fichero>` (esquema, regla 2-4, guardias 7, `salida_sha256`);
   `accept --propuesta --item n --revisado-por --metodo cruda_leida|audio_oido|fotograma_visto`
   (crea el item con todas las comprobaciones de `new`; anota la decision); `reject --item
   --motivo`; `new --transcripcion`; `list` (tabla estable: id, video, t0, tipo, tema).
9. **Quien propone y quien revisa.** Sin API, el proponente es esta sesion de Claude Code
   (`modelo: claude-fable-5-1`, `proponente: llm`, `extractor: llm`). El revisor es el usuario,
   sobre una hoja HTML generada por script versionado
   (`docs/validation/anexos/F07-evidence-extraction/hoja_revision.py`) que muestra SIEMPRE la
   cruda (no la corregida), el contexto y la ruta local del fotograma (no incrusta PNG). Valor
   exacto de `revisado_por` al aceptar: `"<persona> · hoja F07 <fecha> · cruda leida"` (audio)
   o `"... · fotograma visto"` (pantalla/ambas; obligatorio para aceptar). El README de
   evidencia redefine `revisado_por`: quien acepto el item y con que metodo; la cita de audio la
   verifica la maquina contra la cruda `transcripcion`; la persona revisa que `afirmacion`,
   `tema` y `valor` no digan mas que la cita. `provenance: bot-v2` solo cuando la propuesta
   declara `marca_heredada` (tabla de F04 / informe de investigacion); si no, `botsito`.
10. **Dos rondas dentro de la rama.** Ronda 1: herramientas, propuestas para los 5 videos
    (todas con `--check` en verde), hoja de revision, lista de referencia cerrada y golden
    (decision 12), informe `WAITING_FOR_USER_VALIDATION` cuyo "Que debe decidir el usuario" es
    la hoja (aceptar por lotes "todos salvo n, m", rechazar con motivo, marcar `fotograma
    visto`, anotar frases citables que faltan en el tramo de medicion). Ningun item se commitea
    antes. Ronda 2: `accept`/`reject`, commit de la evidencia (inmutable desde entonces),
    `evidence contradictions`, PROJECT_STATE (hechos -> ids), AUDITORIA DE CIERRE con dos
    agentes (despues de la ronda 2, no antes), informe actualizado en la misma ruta con lo
    aplicado, parada corta para que el usuario confirme, ritual §F.
11. **Medicion del proponente** sobre V4 0:05:00-0:15:00 (referencias conocidas en el tramo:
    0:05:42 "mas de 250", 0:06:06 spread, 0:08:27, 0:08:39-0:08:56 respiro 0,75->0,80, 0:09:09,
    0:12:13-0:12:41 stop 0,75 y spread del momento, 0:12:30 caja 1,19537 pantalla): se reporta
    con RECUENTOS, no porcentajes: referencias N, cubiertas (item aceptado cuyo tramo de
    palabras solapa `[t0 - 5 s, t1 + 5 s]` de la referencia con el mismo tema de primer
    nivel), propuestas, `--check` en verde (ronda 1), aceptadas/rechazadas por el usuario y
    frases citables que el usuario echa en falta (recall humano; ronda 2). Se declara que
    proponente, autor de la lista y primer filtro son la misma sesion; el control independiente
    es el usuario.
12. **Golden de la tabla A** materializado: `tests/golden/f07_citas_referencia.yaml`, lista
    CERRADA antes de proponer (23 citas del informe de investigacion + 28 marcas de F04 que
    coinciden, con `video_id`, `t0` heredado, `fragmento` de 4-8 tokens, `modalidad`; las 3
    marcas "era fotograma" como `pantalla`); test de contrato que, si hay >= 1 item, exige por
    cada entrada no `descartada` un item activo cuya cita normalizada contenga el fragmento (o
    cuyos `fotogramas` citen el instante) con tramo localizado a <= 30 s del `t0` heredado.
    Ronda 1: se salta (0 items). Lo que el usuario rechace se marca `descartada: motivo`.
13. **Taxonomia de `tema`** en `knowledge/evidence/temas.yaml` (raices: `ventana`, `sesgo`,
    `liquidez`, `mapeo`, `entrada`, `zona_control`, `stop`, `objetivo`, `break_even`,
    `cartuchos`, `parciales`, `riesgo`, `lotaje`, `herramientas`, `reloj`, `backtest`,
    `no_trade`, `reentrada`, `meta`) con el vocabulario cerrado de `valor`. `valor` solo cuando
    la cita da una cifra o una eleccion cerrada.
14. **Prioridad de extraccion** (>= 80 items): (a) 33 marcas y 23 citas de la investigacion
    re-citadas literalmente; (b) obligatorios de F05 y ficha del Word (`pantalla`,
    `fr-v3-982da728/101000`; la hoja decide fila a fila, no "12 filas = 12 items" a ciegas);
    (c) hechos de v5 (y el backtest de abril solo desde el tramo de v5 que lo muestra); (d) las
    12 ambiguedades A-1..A-12 con las formulaciones en conflicto; (e) ejemplos de no operar y
    de operar. Lo que no se localiza entra en `no_consta`, nunca como item. La cita copia la
    CRUDA aunque tenga errores del ASR (`m 15`, `breakeven`, `1.3` por "uno a tres");
    `afirmacion`/`valor` normalizan (`1:3`) y `notas` explica.
15. **Golden H4 del trader sobre F15** (MASTER_PLAN H "anclaje H4"): NO hay ningun fotograma
    que muestre la hora de apertura de una H4 con el reloj del grafico (informe F05: el grafico
    en UTC+2 no dice a que hora abre su H4); F07 registra los candidatos A-9 como evidencia de
    `reloj.*` y el test de regresion sobre F15 pasa a F10 (captura en la sesion 1). Se anota en
    H.2.
16. **Colision de hash** (Known Issues): `escribir_item` compara el contenido canonico con el
    fichero existente y distingue "mismo item" (error `ya existe`) de "colision" (error
    distinto, imposible en la practica pero explicito).

## Alcance cerrado (que SI)
- `src/botsito/evidence/verificacion.py` (sin importar `corpus`): `tokens`, `localizar_cita`
  (tokens, comodin `[...]`, tiempo por `palabras`, `TOL`), `comprobar_referencias`,
  `ContextoEvidencia`, `SegmentoCitable`/`PalabraCitable` (Protocol).
- `src/botsito/evidence/modelo.py`: campo `transcripcion`; reglas de modalidad; validacion
  extendida; `validar_contra_manifiesto(items, manifiesto, contexto=None)`.
- `src/botsito/evidence/propuestas.py`: esquema, carga estricta, `esqueleto()`, `comprobar()`
  (guardias, `salida_sha256`), `aceptar()`, `rechazar()`, ids `pr-*` (`comun/ids.py`);
  `knowledge/evidence/temas.yaml` (taxonomia y vocabulario de `valor`).
- `src/botsito/validation/knowledge.py`: capa de evidencia con contexto (crudas, referencias,
  activas; avisos sin `data/`); `knowledge/_proposals/` validado (esquema y coherencia con la
  evidencia: un `evidence_id` anotado debe existir).
- CLI: `evidence new --transcripcion`, `propose`, `propose --check`, `accept`, `reject`, `list`.
- `knowledge/_proposals/README.md` y `PROMPT.md` (prompt canonico versionado; su sha256 va en
  cada propuesta); `knowledge/README.md` (regimen); `knowledge/evidence/README.md` (campo
  `transcripcion`, referencias `fr-*`, elipsis, taxonomia); ADR-0009 (verificacion de citas y
  propuestas trazables); hook y `test_evidence_history` sin cambios (las propuestas no son
  inmutables y `_proposals` no esta en la lista del hook).
- Propuestas para los 5 videos (>= 80 items propuestos, todos `--check` en verde), hoja de
  revision HTML por script, golden cerrado (`tests/golden/f07_citas_referencia.yaml`), informe
  con la medicion (decision 11) y la hoja como decision del usuario.
- Tests: unit (`test_verificacion.py`: normalizacion, elipsis, orden, limites de ventana, numeros;
  `test_evidence.py` ampliado: `transcripcion`, modalidades, referencias, contexto ausente;
  `test_propuestas.py`: esqueleto, check, accept/reject, id, doble aceptacion), CLI
  (`test_cli.py`: `propose`/`accept` con `MotorFalso` y fixtures), contrato (`knowledge validate`
  real en verde; `_proposals` en `test_tree`), integridad del repo.

## Fuera de alcance (que NO)
- Busqueda por texto/tiempo y "que hay en V4 0:44:56" (F08).
- Cliente de API de un LLM (no hay clave; el formato de propuesta es la interfaz; si llega una
  clave, un `evidence propose --modelo` rellenaria el esqueleto sin cambiar nada mas).
- Diarizacion (quien habla): atribucion por contexto en `notas` cuando importe.
- Resolver ambiguedades o escribir reglas (F10, F11); lineamientos del usuario como evidencia
  (no son del trader: siguen en PROJECT_STATE hasta que el trader los confirme en F10).
- Re-citar lo heredado de Whisper tiny o de `_procesado/` (decision F04 confirmada).

## Entradas
Crudas activas (`data/transcripciones`), manifiestos `tr-*` y `fr-*`, `manifest.yaml`
(`material_adicional`), `fotogramas_obligatorios.yaml`, PROJECT_STATE (hechos, ambiguedades),
informes F04/F05, informe de investigacion (citas), `Ficha_del_trader_transcrita.md` (solo como
guia de que buscar en el fotograma `fr-v3-982da728/101000`, no como fuente citable).

## Salidas (ficheros)
Codigo y tests citados; `knowledge/_proposals/{README.md,PROMPT.md,pr-*.yaml}`;
`knowledge/evidence/<v>/ev-*.yaml` (ronda 2); `knowledge/evidence/_contradicciones.yaml`
regenerado; `docs/adr/0009-*.md`; `docs/validation/F07-evidence-extraction.md` y
`docs/validation/anexos/F07-evidence-extraction/revision.html`; PROJECT_STATE (hechos
convertidos en ids de evidencia; ambiguedades con ids), HANDOFF, MASTER_PLAN (H.2 fila F07
hecha, Change Log).

## Tests
Ver "Alcance cerrado". Casos negativos obligatorios: cita no localizable; cita con parafrasis;
`audio` con `fotogramas`; `pantalla` sin `fotogramas`; referencia de otro video o fuera de
`[t0-1, t1+1]`; referencia heredada (`_procesado/...`); `transcripcion` no activa o de otro
video; propuesta con item `no_consta: true` y cita; aceptar item rechazado; aceptar dos veces;
`evidence_id` anotado que no existe; propuesta con `prompt_sha256` distinto del `PROMPT.md`
actual (AVISO, no error: el prompt evoluciona).

## Criterio de aceptacion
`make check` verde; `knowledge validate` verde con >= 80 items (ronda 2) y 0 propuestas
`pendiente`; 100 % de items de audio localizados en la cruda por maquina y 100 % de items de
pantalla con fotograma existente y revisados por el usuario; medicion del tramo de 10 min en el
informe; contradicciones regeneradas y listadas; hechos de PROJECT_STATE convertidos en ids.

## Riesgos
- `no_habla` marca el 28 % de los segmentos de v4 y el 42 % de v2: parte de lo citable cae en
  segmentos con senal (confianza `media`/`baja` por regla 7). El trader repite la misma regla
  en varios tramos: sin la guardia de duplicados la cifra 80 se alcanzaria con repeticiones. Un
  `reject` no impide re-proponer lo mismo (aviso en `--check`). La hoja HTML referencia rutas
  locales `data/fotogramas/...` (no incrusta 8,9 GiB).
- Cita "literal" que la cruda escribe distinto (numeros "0,75" frente a "0.75", "un" frente a
  "1"): la normalizacion no lo cubre a proposito; se cita como esta en la cruda y `notas`
  aclara. Riesgo de sesgo del proponente hacia lo que ya cree saber (mitigado por `no_consta`,
  por la revision del usuario y por reportar precision/recall).
- Volumen: 80 items x revision humana. Mitigado por la hoja de revision con contexto y por
  aceptar por lotes ("todos salvo n, m").
- Items de pantalla: la maquina solo garantiza que el fotograma existe y esta en el tramo.

## Revision de diseno (agente, 2026-09-07, antes de programar)
Aceptados (todos los bloqueantes): B1 `evidence` no importa `corpus` (`|` = capas
independientes en import-linter): `Protocol` estructural, composicion en `validation`/CLI,
prohibicion explicita en `test_import_contracts` (decisiones 2 y 5). B2 comodin `[...]` (la
cruda ya contiene `...` del ASR), comparacion por tokens, limites de trozos y de cita
(decision 2). B3 tiempo real por `palabras` con `TOL = 2 s` (decision 3). B4
`material_adicional` solo desde un tramo de video que lo muestra (decision 4). B5 `revisado_por`
redefinido y valor exacto con metodo; `provenance: bot-v2` solo con `marca_heredada` (decision
9). B6 `salida_sha256` e id `pr-*` con hash (decision 6). Importantes: I1 (verificar contra la
cruda citada; aviso agregado), I2 (`no_consta` como lista por tramo con `temas_buscados`), I3
(guardias de calidad, `dudas` y `senales` fuerzan confianza), I4 (medicion con recuentos y
recall humano; tramo V4 0:05-0:15 con 6-7 referencias en vez de 0:40-0:50 con 3), I5
(auditoria de cierre tras la ronda 2; contenido de cada informe), I6 (golden como fixture
cerrada + test), I7 (golden H4: fuera de alcance con motivo, a F10), I8 (`referencias`
obligatorio si hay `fotogramas`). Menores M1-M8 aceptados (README y `test_tree` con
`_proposals`, contexto sin `palabras`, colision de hash, cita copia la cruda, salida estable y
hoja por script, `PROMPT.md` versionado, sin `n` en el item, riesgos anadidos).
Descartado: ninguno.

## Que habilita
F08 (busqueda con fuente: cada item ya trae `transcripcion` y segmentos localizables), F10
(preguntas de la sesion 1 con la evidencia de cada ambiguedad), F11 (reglas que citan ids),
F21 (goldens 4,08 / 3,94 y 1,19537 como evidencia).
