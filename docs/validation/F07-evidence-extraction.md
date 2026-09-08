# FUNCTIONALITY VALIDATION REPORT

**Funcionalidad:** F07 · evidence-extraction (rondas 1 y 2)
**Rama:** `feature/F07-evidence-extraction`
**Objetivo:** poblar `knowledge/evidence/` con items cuya cita sea verificable por maquina (audio
localizado en la cruda `tr-*` activa; pantalla anclada a un fotograma `fr-*` real), con toda
propuesta registrada en `knowledge/_proposals/` (prompt, modelo, salida y decision humana) y sin
que el proponente escriba nunca en `knowledge/evidence/`. Metodo supervisado: brief con revision
de diseno por agente (6 bloqueantes y 8 importantes aplicados), construccion, y dos rondas: esta
(herramientas + propuestas + hoja de revision) y la segunda (aceptacion item a item por decision
del usuario, evidencia, contradicciones, auditoria de cierre con dos agentes, informe final).

## Que se construyo
- **Verificacion mecanica de citas** (`src/botsito/evidence/verificacion.py`, ADR-0009): la
  `cita_literal` se localiza POR TOKENS en los segmentos de la cruda que tocan
  `[t0 - 2 s, t1 + 2 s]` (NFC, `casefold`, numeros con separador interior como un token, guiones
  y apostrofes como espacio, acentos conservados, `...` del ASR eliminados; `3` no casa en `33`
  ni `1.3` en `11.3`; `0.75` y `0,75` son distintos a proposito), con el comodin `[...]` (maximo
  2; trozos >= 3 tokens; cita >= 4 tokens) y tiempo real por `palabras` (alineadas por caracteres
  sin espacios): la cita queda atada al tiempo, no solo al texto. `evidence` NO importa `corpus`
  (protocolo estructural `SegmentoCitable`; el contexto lo compone
  `validation/contexto_evidencia.py`; contrato nuevo en `test_import_contracts`).
- **Modelo** (`evidence/modelo.py`): campo opcional `transcripcion` (id `tr-*`, obligatorio en
  `audio`/`ambas`, prohibido en `pantalla`; debe ser la activa del video al crear el item);
  `pantalla`/`ambas` exigen al menos una referencia `fr-<id>/<t_ms>` del mismo video dentro de
  `[t0 - 1 s, t1 + 1 s]` conocida por `referencias_conocidas` (ADR-0008 §6); `audio` no admite
  `fotogramas`; `material_adicional` solo acompanado de un `fr-*` del tramo;
  `validar_contra_manifiesto(items, manifiesto, contexto)` (sin referencias conocidas, un item con
  `fotogramas` es error: se acabo aceptar rutas heredadas); `verificar_citas` (verifica SIEMPRE
  contra la cruda citada; sin `data/`, aviso agregado; transcripcion reemplazada, aviso agregado
  con cuantos items se localizan tambien en la nueva); colision de hash distinguida de "mismo
  contenido".
- **Propuestas trazables** (`evidence/propuestas.py`, `knowledge/_proposals/`): id
  `pr-<video>-<t0>-<t1>-<hash8>`; esqueleto con contexto de la cruda (sin `palabras`), referencias
  del tramo compactas, prompt canonico (`PROMPT.md` v1) y `temas_buscados`; `--check` con las
  guardias (cita localizada, >= 4 tokens, tema con raiz en `knowledge/evidence/_temas.yaml`,
  `valor` presente en la cita o cerrado, misma cita en dos items o en la evidencia = error, mismo
  tema con localizaciones solapadas = error, senal del ASR o duda del glosario => confianza no
  `alta`, cada `tema_buscado` en `items` o en `no_consta`, cita rechazada antes = aviso) y sello
  `salida_sha256` (solo los campos de decision pueden cambiar despues; `knowledge validate` lo
  recomputa y exige que todo `evidence_id` anotado exista).
- **CLI**: `evidence new --transcripcion`, `evidence propose [--video --t0 --t1 | --check]`,
  `evidence accept --propuesta --item --revisado-por --metodo cruda_leida|audio_oido|fotograma_visto`
  (pantalla exige `fotograma_visto`; `provenance: bot-v2` solo con `marca_heredada`),
  `evidence reject`, `evidence list`.
- **Golden de la tabla A** cerrado ANTES de proponer: `tests/golden/f07_citas_referencia.yaml`
  (40 referencias: 23 citas del informe de investigacion + marcas de F04 que coinciden + 3 de
  pantalla) y `tests/contract/test_golden_citas_f07.py` (exige un item activo por referencia a
  <= 30 s; se salto en la ronda 1 y pasa 40/40 en la ronda 2).
- **Propuestas para los 5 videos**: 20 propuestas (tramos de 5 a 15 min; v2 sin el tramo de
  musica 0:38:30-0:56:00), todas con `--check` en verde y selladas, generadas por esta sesion
  (`modelo: claude-fable-5-1`, `proponente: llm`) leyendo la cruda completa de cada video.
  Hoja de revision `docs/validation/anexos/F07-evidence-extraction/revision.html` generada por
  `hoja_revision.py` (cruda, no corregida; contexto del tramo; ruta local del fotograma).
- Docs: ADR-0009, `knowledge/_proposals/{README,PROMPT}.md`, `knowledge/README.md`,
  `knowledge/evidence/README.md` (campo `transcripcion`, referencias, regla de la cita,
  `revisado_por` redefinido), `_temas.yaml`.

## Archivos creados
`src/botsito/evidence/{verificacion,propuestas}.py`, `src/botsito/validation/contexto_evidencia.py`,
`knowledge/evidence/_temas.yaml`, `knowledge/_proposals/{README.md,PROMPT.md,pr-*.yaml}` (20),
`docs/adr/0009-verificacion-de-citas-y-propuestas-trazables.md`, `docs/plan/features/F07-evidence-extraction.md`,
`tests/unit/{test_verificacion,test_propuestas}.py`, `tests/golden/f07_citas_referencia.yaml`,
`tests/contract/test_golden_citas_f07.py`, `docs/validation/anexos/F07-evidence-extraction/{hoja_revision.py,revision.html}`,
`knowledge/evidence/<video>/ev-*.yaml` (341, ronda 2, commit ff13e7a).

## Archivos modificados
`src/botsito/evidence/modelo.py`, `src/botsito/validation/knowledge.py`, `src/botsito/cli.py`,
`src/botsito/comun/ids.py`, `knowledge/{README,evidence/README}.md`, `docs/adr/README.md`,
`tests/unit/{test_evidence,test_cli,test_tree}.py`, `tests/contract/test_import_contracts.py`,
`knowledge/evidence/_contradicciones.yaml` (regenerado), `knowledge/_proposals/pr-*.yaml` (decisiones y
re-sellado), `docs/adr/0001-*.md` (nota del quinto regimen), `PROJECT_STATE.md`, `docs/HANDOFF.md`,
`docs/plan/MASTER_PLAN.md`.

## Decisiones tomadas
Las 16 del brief (seccion "Decisiones de diseno"), tras la revision de agente. Destacan: la cita
se verifica contra la cruda citada, no contra la activa del momento; `hotwords` no interviene
(previos); `no_consta` es una lista por tramo con `temas_buscados`; ningun item se escribe antes
de la decision del usuario; `revisado_por` = quien acepto y con que metodo; `provenance: bot-v2`
solo con `marca_heredada`; golden H4 sobre F15 fuera de alcance (ningun fotograma muestra la
hora de apertura de una H4) y trasladado a F10.

## Como ejecutarlo
```
uv run botsito evidence propose --video v4 --t0 0:05:00 --t1 0:15:00 --modelo <quien> --tema-buscado stop ...
uv run botsito evidence propose --check knowledge/_proposals/pr-v4-000500-001500-<hash>.yaml
uv run botsito evidence accept --propuesta <fichero> --item 7 --revisado-por "Aleks · hoja F07 2026-09-0X · cruda leida" --metodo cruda_leida
uv run botsito evidence reject --propuesta <fichero> --item 4 --motivo "..." --decidido-por Aleks
uv run python docs/validation/anexos/F07-evidence-extraction/hoja_revision.py
uv run botsito knowledge validate
```

## Como probarlo
`make check` (lint, mypy strict, tests, 4 contratos + el nuevo `evidence -> corpus`,
state/config/knowledge validate). Sin GPU ni datos: `uv run --no-sync pytest -q
tests/unit/test_verificacion.py tests/unit/test_propuestas.py`. Con `data/`: `knowledge
validate` recomputa el sello de las 20 propuestas, localiza las 334 citas de audio en su cruda y
cruza cada decision con su item; `evidence propose --check` sobre cualquiera de ellas vuelve a
localizar cada cita; `pytest tests/contract/test_golden_citas_f07.py` pasa 40/40.

## Tests ejecutados
`make check` verde: 311 funciones de test, 456 casos (antes 307 / 452 en `stable/F05-previos-F07`). Nuevos: localizacion por tokens (numeros, elipsis del ASR, guiones,
orden estricto, coincidencias multiples, ventana en tiempo, sin palabras, tolerancia),
referencias de pantalla (modalidades, otro video, fuera de tramo, material solo con `fr-*`),
modelo (`transcripcion`, reglas de modalidad, contexto, colision), propuestas (esqueleto, sello,
guardias, duplicados, solapes, temas buscados, cita ya en evidencia o rechazada, aceptar/rechazar,
carga estricta, `validar_propuestas`), CLI con una cruda real del motor falso (`new` de audio
exige cita localizada; `propose`/`--check`/`accept`/`reject` de punta a punta; sello violado
detectado por `knowledge validate`), contrato `evidence` no importa `corpus`, golden bien formado.
Ronda 2 (auditoria): frase repetida antes de la ventana, hueco entre trozos, palabras parciales,
coherencia decision-evidencia (campo distinto, id repetido, rechazado con id, llm sin propuesta,
metodo incoherente), cabecera con tiempo invalido, sello sobre la cabecera, directorio real con
contexto y sin el.

## Resultados

### Propuestas (ronda 1) y evidencia (ronda 2)
| Video | Propuestas | Items | `no_consta` |
|---|---|---|---|
| v1 | 2 | 45 | 5 |
| v2 | 4 | 53 | 26 |
| v3 | 6 | 101 | 25 |
| v4 | 7 | 130 | 31 |
| v5 | 1 | 12 | 4 |
| **total** | **20** | **341** | **91** |

Modalidad: audio 334, pantalla 4, ambas 3. Tipo: RULE_STATEMENT 172, UNKNOWN 89, MANAGEMENT 37, PARAMETER 16, NO_TRADE 14, EXAMPLE_TRADE 13. Confianza: alta 247, media 94, baja 0. Todas las propuestas con `--check` en verde y `salida_sha256`.

Marcas heredadas re-citadas (`marca_heredada`, saldran con `provenance: bot-v2`): 42. Los 91
`no_consta` documentan, tramo a tramo, los temas buscados que no aparecen (por ejemplo, la
charla final de v2 sin contenido operativo, o el sesgo H4 en los tramos donde no se habla de el).
Las 25 `dudas` del glosario (boss/voz/blog/split fuera de los 6 segmentos verificados) fuerzan
`confianza: media` en los items que caen en esos segmentos; la nota de cada item lo dice.

Ronda 2 (2026-09-07): el usuario acepto los 341 items sin modificaciones y rechazo 0; los 7 de
pantalla/ambas con `fotograma visto`; recall humano de V4 0:05-0:15: ninguna frase faltaba.
`evidence accept` x341 sin fallos (10 min): 341 items en `knowledge/evidence/` (commit ff13e7a),
`revisado_por` "Aleks · hoja F07 2026-09-07 · cruda leida" (334) o "· fotograma visto" (7),
`extractor: llm`, 42 con `provenance: bot-v2`; las 20 propuestas anotan `decision`, `decidido_el`,
`metodo_revision` y `evidence_id` (0 pendientes). `evidence contradictions`: 1 abierta,
`stop.nivel` 0,75 (`ev-v1-000448-346d6d90`, `ev-v2-003142-beb4ad3c`) frente a 0,8
(`ev-v5-000312-f5062062`) = A-10; el recuento depende de la granularidad de `tema` elegida por el
proponente (el mismo parametro vive bajo `stop.075_suficiente`, `stop.introducido_en_operacion_075`,
etc.): F11 decide que temas comparten parametro. `knowledge validate`: 341 items, 0 problemas,
1 aviso (una cita con tiempos parciales, `ev-v3-000058-7b5ce480`); 41 items tienen un comodin
que salta entre 15 y 44 s (aceptados por el usuario; desde la auditoria `--check` lo avisa).

### Golden (lista cerrada antes de proponer)
Las 40 referencias de `tests/golden/f07_citas_referencia.yaml` tienen propuesta (ronda 1) y, tras
la aceptacion, item de evidencia (ronda 2): `test_golden_citas_f07` pasa 40/40 (fragmento contenido
en la cita, `t0` a <= 30 s; para las 3 de pantalla, la referencia `fr-*` esta en `fotogramas`).
Ninguna referencia quedo `descartada`.

### Medicion del proponente (V4 0:05:00-0:15:00, 10 min)
Lista de referencia cerrada antes de proponer (marcas de F04, informe de investigacion y hechos de
PROJECT_STATE en el tramo): 7 referencias: 0:05:42 "mas de 250", 0:06:06 pregunta del spread,
0:08:27 spread (ejemplo del glosario), 0:08:39-0:08:56 respiro 0,75 -> 0,80, 0:09:09 spread
aumenta, 0:12:13-0:12:41 stop en 0,75 y spread del momento, 0:12:30 caja 1,19537 (pantalla).

| Medida | Recuento |
|---|---|
| Referencias cerradas | 7 |
| Cubiertas por una propuesta (mismo tema raiz, solape con `[t0 - 5 s, t1 + 5 s]`) | 7 |
| Propuestas en el tramo | 22 items, 6 `no_consta` |
| `--check` en verde (mecanico) | 22 de 22 |
| Aceptadas / rechazadas por el usuario | 22 / 0 |
| Frases citables que el usuario echa en falta (recall humano) | 0 ("ninguna") |

Limitacion declarada: proponente, autor de la lista de referencia y primer filtro son la misma
sesion (`claude-fable-5-1`); la cobertura mide que la sesion no omitio lo que ya sabia, no que
no omitiera lo que no sabia. El control independiente es el usuario (aceptados, rechazados y
frases anadidas en la hoja). Dos de las 7 referencias son preguntas del consultor, no
afirmaciones del trader (estan propuestas como `UNKNOWN` con `notas: habla el consultor`).

## Que deberia observar el usuario
`knowledge validate` en verde: "OK: 341 items de evidencia, 1 contradicciones abiertas, historial
intacto; 20 propuestas (0 items pendientes)" con 1 aviso de tiempos parciales; `evidence list`
con 341 filas; la hoja de revision muestra "aceptado" en cada item; `evidence propose --check`
sobre una propuesta cualquiera devolviendo "OK: N items... salida sellada" y una linea "localizado
en h:mm:ss-h:mm:ss" por item (mas los avisos de hueco largo).

## Que casos funcionan
Todo el alcance del brief (rondas 1 y 2): 341 items verificables por maquina y trazables a su
propuesta, decision y metodo; contradicciones regeneradas; golden 40/40; hechos y ambiguedades de
PROJECT_STATE enlazados a ids.

## Que casos todavia no funcionan
- Sin cliente de API de LLM (no hay clave): el proponente fue esta sesion; el formato de
  propuesta es la interfaz para cualquier otro proponente.
- `evidence list` es una tabla; la busqueda por texto y tiempo es F08.

## Limitaciones
- La cita copia la CRUDA con sus errores del ASR (`m 15`, `breakeven`, `1.3` por "uno a tres",
  repeticiones en los bordes de segmento como "tiene tiene", "no no"); `afirmacion` y `valor`
  normalizan y `notas` explica. Un ASR distinto daria otra cruda y otros ids `tr-*`; los items
  seguirian verificandose contra la cruda que citan.
- Sin diarizacion: cuando habla el consultor la nota lo dice; en 0:09:33 no queda claro quien
  habla.
- Los items de `pantalla` (4) y `ambas` (3) solo estan garantizados por maquina en "el fotograma
  existe y esta en el tramo"; lo que dicen lo confirma el usuario con `fotograma visto`.
- La hoja referencia rutas locales `data/fotogramas/...` (no incrusta 8,9 GiB).

## Riesgos
Sesgo del proponente hacia lo que ya creia saber (mitigado por `no_consta`, la lista cerrada,
las guardias de duplicados y la revision del usuario). Volumen de revision (341 items):
mitigado con la aceptacion por lotes. Si el usuario rechaza muchos, la ronda 2 puede quedar por
debajo de 80 items: entonces se reabren propuestas, no se relajan las guardias.

## Impacto sobre funcionalidades anteriores
`validar_contra_manifiesto` ya no acepta rutas heredadas como `fotogramas` (F06 no tenia items).
`knowledge validate` suma la capa de propuestas y los avisos de citas. `_temas.yaml` y
`_proposals/` entran en `test_tree`. Nada anterior cambia de resultado.

## Auditoria de cierre (dos agentes: codigo/tests y docs/proceso)
Hecha el 2026-09-07 sobre la evidencia aceptada (decision I5 de la revision de diseno); todo lo
que sigue esta aplicado en la rama.

**Codigo y tests** (1 bloqueante, 6 importantes, 6 menores):
- B1 `test_directorio_real_valida` llamaba a `validar_contra_manifiesto` sin contexto y rompio al
  entrar los 7 items de pantalla (la suite estaba en rojo). Ahora construye el contexto real y
  ademas exige que sin referencias conocidas esos items sean error.
- I1 `localizar_cita` tomaba la primera aparicion del primer trozo y luego miraba la ventana: una
  frase repetida antes, en un segmento que solo tocaba la ventana, hacia fallar una cita
  verdadera. Ahora prueba todas las apariciones y toma la primera completa que cabe;
  `coincidencias` cuenta las que caben.
- I2 el sello no cubria `transcripcion` ni `proponente` (editarlos no se detectaba). Ampliado a
  la cabecera (`video_id`, `transcripcion`, `t0`, `t1`, `proponente`); las 20 propuestas
  re-selladas por script (decisiones y `comprobado_el` intactos).
- I3 `knowledge validate` solo comprobaba que el `evidence_id` existiera: un id apuntando a otro
  item, `fotograma_visto` en audio o un aceptado vuelto a rechazado pasaban. Ahora cruza cada
  decision con la evidencia (campos, `extractor`, `transcripcion`, `provenance`, metodo, id unico;
  rechazado con id = error; llm sin propuesta = aviso). Los 341 reales son coherentes.
- I4 cabecera de propuesta con `t0: abc` daba traceback en `--check`, `reject` y `validate`:
  ahora `PropuestaError`.
- I5 el comodin `[...]` no tenia tope de salto. Se mide `hueco_ms` y `--check` avisa a partir de
  15 s; no es error (41 items aceptados lo superan, maximo 44 s: el usuario leyo el tramo).
- I6 la contradiccion mecanica depende de la granularidad de `tema`: anotado en ADR-0009 y en
  Technical Debt para F11; no se cambia el codigo de F07.
- M1 los avisos de localizacion se descartaban y un segmento con la ultima palabra ausente en
  `palabras` perdia toda la alineacion: ahora se alinea el prefijo, el resto lleva el tramo final
  del segmento y `validate` imprime el recuento (1 item).
- M2 `accept` no era atomico: si fallaba anotar la decision quedaba un item huerfano; ahora se
  retira. M3 audio ya no admite `fotograma_visto`. M4 `accept` re-evalua tambien los problemas
  de solape que mencionan el item. M5 sin `manifest.yaml` las referencias de pantalla se
  comprueban igual. M6 tests anadidos para I1, I3, I4, M1, M3 y la cabecera del sello.
- Sin problema: tokenizacion (`3`/`33`, `1.3`/`11.3`, `0,75`/`0.75`, elipsis, guiones,
  acentos), reglas del comodin, ventana con tolerancia, 341/341 localizados en su cruda con 0
  coincidencias multiples y 0 citas repetidas, sello sobre items/contexto/temas/prompt, doble
  aceptacion y rechazo cruzado, `provenance` con `marca_heredada`, transcripcion reemplazada y
  cruda ausente (avisos agregados), YAML sexagesimal rechazado, UTF-8/CRLF, ids por regex,
  contrato `evidence` sin `corpus`.

**Docs y proceso** (2 bloqueantes, 6 importantes, 4 menores): HANDOFF y PROJECT_STATE describian
la ronda 1 (reescritos: Current Feature, Waiting, Tests, Next Action, Change Log); ADR-0009
faltaba en el indice de PROJECT_STATE; MASTER_PLAN decia que el golden H4 se anadia en F07 (fila
H.2 y tabla A corregidas: pasa a F10), filas H "Propuestas de LLM" y "Cita contra la CRUDA" sin
marcar como hechas, fila H.2 "Previos y entradas" sin cerrar, tabla B sin `knowledge/_proposals`
(todo corregido, con `revisado_por` en vez de `reviewed_by`); deuda tecnica de F07 cerrada o con
dueno (referencias conocidas, hallazgo V4 1:28:20, regla de cita, `dudas`, obligatorios de F05,
`palabras` bajo corregida -> F08, proponente = filtro, hook local); el hook instalado en esta
maquina no protegia `knowledge/corpus/fotogramas` (reinstalado con `make hooks`; la garantia real
son los tests de historial en CI); READMEs de evidencia y propuestas (valor con coma, `n` al
final, `decidido_el` en UTC), nota en ADR-0001 (quinto regimen), brief con las salidas marcadas.
Trazabilidad y commits correctos (341 `revisado_por` completos, 341 `evidence_id` unicos y
existentes, trailers presentes, ningun commit toca spec/cases). Ritual §F compatible con `state
check` y los hooks.

## Que debe decidir el usuario
Decidido el 2026-09-07 (ronda 1): (1) hoja de revision: acepto los 341 items sin modificaciones,
`fotograma visto` en los 7 de pantalla/ambas; (2) recall humano V4 0:05-0:15: "ninguna"; (3) tag
`stable/F07`; (4) golden H4 sobre F15 pasa a F10.

Pendiente (parada corta de la ronda 2): confirmar el cierre tras la auditoria, es decir, el merge
`--no-ff` a `main` con tag `stable/F07`. Si prefiere revisar antes alguna correccion de la
auditoria (por ejemplo el aviso de huecos largos o la contradiccion por granularidad de `tema`),
indicarlo; ninguna cambia la evidencia aceptada.

## Que puede comprobar sin recursos especiales
`make check`; `uv run botsito knowledge validate`; `uv run botsito evidence list`; abrir la
hoja; `uv run botsito evidence propose --check knowledge/_proposals/<cualquiera>.yaml`; `git diff
stable/F05-previos-F07..HEAD --stat`; `uv run --no-sync pytest -q
tests/contract/test_golden_citas_f07.py` (40/40); `git log --format=%s knowledge/evidence` (solo
adiciones).

## Estado
WAITING_FOR_USER_VALIDATION (ronda 2: confirmacion de cierre, merge + tag `stable/F07`)
