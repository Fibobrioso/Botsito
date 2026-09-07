# FUNCTIONALITY VALIDATION REPORT

**Funcionalidad:** F07 · evidence-extraction (ronda 1 de 2)
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
  pantalla) y `tests/contract/test_golden_citas_f07.py` (se salta mientras no hay evidencia;
  en la ronda 2 exige un item activo por referencia a <= 30 s).
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
`tests/contract/test_golden_citas_f07.py`, `docs/validation/anexos/F07-evidence-extraction/{hoja_revision.py,revision.html}`.

## Archivos modificados
`src/botsito/evidence/modelo.py`, `src/botsito/validation/knowledge.py`, `src/botsito/cli.py`,
`src/botsito/comun/ids.py`, `knowledge/{README,evidence/README}.md`, `docs/adr/README.md`,
`tests/unit/{test_evidence,test_cli,test_tree}.py`, `tests/contract/test_import_contracts.py`,
`PROJECT_STATE.md`, `docs/HANDOFF.md`, `docs/plan/MASTER_PLAN.md`.

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
validate` recomputa el sello de las 20 propuestas; `evidence propose --check` sobre cualquiera
de ellas vuelve a localizar cada cita.

## Tests ejecutados
`make check` verde: 309 funciones de test, 454 casos (antes 307 / 452 en `stable/F05-previos-F07`, mas los de F07 anadidos en la rama). Nuevos: localizacion por tokens (numeros, elipsis del ASR, guiones,
orden estricto, coincidencias multiples, ventana en tiempo, sin palabras, tolerancia),
referencias de pantalla (modalidades, otro video, fuera de tramo, material solo con `fr-*`),
modelo (`transcripcion`, reglas de modalidad, contexto, colision), propuestas (esqueleto, sello,
guardias, duplicados, solapes, temas buscados, cita ya en evidencia o rechazada, aceptar/rechazar,
carga estricta, `validar_propuestas`), CLI con una cruda real del motor falso (`new` de audio
exige cita localizada; `propose`/`--check`/`accept`/`reject` de punta a punta; sello violado
detectado por `knowledge validate`), contrato `evidence` no importa `corpus`, golden bien formado.

## Resultados

### Propuestas (ronda 1)
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

### Golden (lista cerrada antes de proponer)
Las 40 referencias de `tests/golden/f07_citas_referencia.yaml` tienen propuesta (comprobado con la
misma regla del test sobre las propuestas: fragmento contenido en la cita y `t0` a <= 30 s; para
las 3 de pantalla, la referencia `fr-*` esta en `fotogramas`). El test de contrato se salta en
esta ronda (0 items) y sera el golden real en la ronda 2 tras las decisiones del usuario; lo que
el usuario rechace se marcara `descartada: <motivo>` en la fixture.

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
| Aceptadas / rechazadas por el usuario | ronda 2 |
| Frases citables que el usuario echa en falta (recall humano) | ronda 2 (hoja) |

Limitacion declarada: proponente, autor de la lista de referencia y primer filtro son la misma
sesion (`claude-fable-5-1`); la cobertura mide que la sesion no omitio lo que ya sabia, no que
no omitiera lo que no sabia. El control independiente es el usuario (aceptados, rechazados y
frases anadidas en la hoja). Dos de las 7 referencias son preguntas del consultor, no
afirmaciones del trader (estan propuestas como `UNKNOWN` con `notas: habla el consultor`).

## Que deberia observar el usuario
`knowledge validate` en verde con 20 propuestas y 341 items pendientes; la hoja de revision
abierta en el navegador; `evidence propose --check` sobre una propuesta cualquiera devolviendo
"OK: N items... salida sellada" y una linea "localizado en h:mm:ss-h:mm:ss" por item.

## Que casos funcionan
Todo el alcance de la ronda 1 del brief. Ningun item de evidencia existe todavia (por diseno).

## Que casos todavia no funcionan
- Ronda 2 pendiente: `accept`/`reject` item a item, `evidence contradictions`, golden real,
  hechos de PROJECT_STATE convertidos en ids, auditoria de cierre con dos agentes, ritual.
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
Pendiente: se hace en la ronda 2, cuando exista la evidencia (decision I5 de la revision de
diseno).

## Que debe decidir el usuario
1. **La hoja de revision** (`docs/validation/anexos/F07-evidence-extraction/revision.html`):
   por cada propuesta, aceptar (la afirmacion, el tema y el valor no dicen mas que la cita),
   rechazar con motivo, y para los 7 items de pantalla/ambas marcar `fotograma visto` (abrir la
   ruta local indicada). Respuesta por lotes valida: "acepto todos salvo pr-... item n
   (motivo)". Los aceptados se crearan con `revisado_por: "Aleks · hoja F07 <fecha> · cruda
   leida"` (o `fotograma visto`).
2. **Recall humano** sobre V4 0:05:00-0:15:00: frases citables del tramo que falten en la
   propuesta `pr-v4-000500-001500-*` (o "ninguna").
3. **Tag de cierre** `stable/F07` (funcionalidad con numero propio, §F sin cambios).
4. Confirmar que el golden H4 sobre F15 pasa a F10 (ningun fotograma muestra la hora de apertura
   de una H4; ya anotado en H.2).

## Que puede comprobar sin recursos especiales
`make check`; `uv run botsito knowledge validate`; abrir la hoja; `uv run botsito evidence
propose --check knowledge/_proposals/<cualquiera>.yaml`; `git diff stable/F05-previos-F07..HEAD
--stat`; `uv run --no-sync pytest -q tests/contract/test_golden_citas_f07.py` (se salta hasta la
ronda 2).

## Estado
WAITING_FOR_USER_VALIDATION (ronda 1: hoja de revision)
