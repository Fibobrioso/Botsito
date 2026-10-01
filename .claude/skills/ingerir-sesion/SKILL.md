---
name: ingerir-sesion
description: Ingiere una grabacion de una sesion de Bot v3 con el trader (v7, v8, v9...) - registro en el corpus, comprobacion de audio, transcripcion con cuarentena, fotogramas, extraccion por pregunta y evidencia - hasta el informe de extraccion, sin resolver ninguna ambiguedad. Usala cuando Aleks deja una grabacion nueva de una sesion en el corpus.
argument-hint: "<fichero de video en corpus/> <AAAA-MM-DD> <sesion-NN>"
---

# ingerir-sesion

El camino que siguieron v7, v8 y v9 (`docs/validation/SESION-02-VIDEO.md`,
`docs/validation/SESION-02-VIDEO-V8.md`, `docs/validation/SESION-03-EXTRACCION.md`), en orden. Las
reglas viven en `CLAUDE.md`, `docs/runbooks/SESION-DE-PREGUNTAS.md` («Después (Aleks y la sesión)») y
`docs/runbooks/MIRAR-EL-MATERIAL.md`; aqui solo el recorrido, las puertas y las trampas medidas.

## Entradas

| Entrada | De donde sale |
|---|---|
| El video, ya copiado por Aleks en `corpus/Estrategia del trader/` | Aleks |
| Fecha de la sesion y su numero (`AAAA-MM-DD-sesion-NN`) | Aleks |
| La hoja de preguntas que se llevo (orden y codigos) | `scripts/hoja_preguntas.py`, `ORDEN_SESION_NN` en `scripts/transcribir_sesion.py` |
| Audio de respaldo, si lo hay | Aleks |

## Limites

- **La cruda de una sesion NO LA LEE NADIE: ninguna persona ni ningun modelo** (cuarentena,
  `scripts/transcribir_sesion.py`). Se lee solo `<stem>.filtrada.md`. La guardia bloquea las crudas
  de v7 en adelante y los tramos no citables de cualquier video: **no se rodea**.
- Un fotograma se abre solo por instante LOCALIZADO en la filtrada (ADR-0038), nunca la pestana
  Analytics ni el tramo sin audio; de 25 en 25 como mucho, anotando cada lote antes del siguiente.
- `corpus frames show`, `kb find --solo cruda`, `kb at` y `corpus transcript show` IMPRIMEN texto
  crudo: cerca de un tramo en cuarentena revelan lo que la cuarentena tapa. No se usan alli
  (Next Action I de `PROJECT_STATE.md`: la CLI todavia no respeta la cuarentena).
- Si algo trae un dia reservado o un agregado, se declara en
  `docs/validation/HOLDOUT-EXPOSICIONES.md` el MISMO dia.
- **Esta rama NO resuelve nada**: propone. Los registros de feedback y el cierre de ambiguedades van
  en OTRA rama, tras la revision del consultor (`docs/validation/ACTIVAR-SESION-03.md`), con
  `docs/runbooks/AMBIGUEDADES.md`.
- Nada escribe en el repositorio mientras corre `make check`: la transcripcion y la extraccion de
  fotogramas tampoco (rompen la huella del sello).

## Herramientas

Bash (`uv run botsito corpus ...`, `uv run python scripts/transcribir_sesion.py`, `ffmpeg`),
Read de la filtrada y de fotogramas localizados, Write/Edit para `fuentes.yaml`,
`tramos_no_citables.yaml` y el informe. Los comandos largos van a segundo plano y se espera su aviso.

## El recorrido

1. **Registro.** Entrada nueva en `knowledge/corpus/fuentes.yaml` (siguiente `video_id`,
   `drive_id: null`, `fecha_grabacion`, y una `naturaleza` que empiece por «sesion»; la procedencia,
   en un comentario encima: el esquema no tiene notas). Ampliar `v1..vN` en
   `tests/unit/test_inventario.py`. `uv run botsito corpus inventory` (hashea todo: minutos) y
   `uv run botsito corpus check --hashes`.
2. **Audio.** No hay comando del repo: se mide con `ffmpeg -af silencedetect` (en v8, -50 dB y 30 s
   minimo; `SESION-02-VIDEO-V8.md`). Un corte de audio entra en
   `knowledge/corpus/tramos_no_citables.yaml` con motivo «SIN AUDIO», en `naturaleza` y en el
   comentario de `fuentes.yaml`, y la respuesta afectada se marca «respuesta incompleta por audio».
   Puerta: tras la transcripcion, ningun segmento con `t1` dentro del corte (alucinacion del ASR).
   Si hay audio de respaldo, el procedimiento de `SESION-03-EXTRACCION.md` (registrarlo, desfase por
   correlacion, ventanas en un `git worktree`), decidiendo ANTES si es un video nuevo o una
   transcripcion complementaria: `evidence new` solo cita la transcripcion ACTIVA.
3. **Transcripcion.** `uv run botsito corpus transcribe --video <vN>` (large-v3, ADR-0007; no
   imprime texto). Escribe el manifiesto inmutable `knowledge/corpus/transcripciones/tr-<vN>-...yaml`
   y el texto en `data/transcripciones/<vN>/`. Puerta: `uv run botsito corpus transcript check`.
4. **Cuarentena.** `uv run python scripts/transcribir_sesion.py --audio <carpeta FUERA del repo>`
   (o `--solo-filtrar` sobre una cruda ya hecha): escribe `<stem>.cruda-NO-LEER.*`,
   `<stem>.filtrada.md` (lo UNICO que se lee) y `<stem>.registro.txt`. Los bloques en cuarentena
   entran en `tramos_no_citables.yaml` con `motivo` y `acordado`, SIN contenido, en un commit propio
   (v7: `3718889`). Desde ese commit `evidence propose --check` y `evidence new` rechazan citarlos.
5. **Fotogramas.** `uv run botsito corpus frames extract --video <vN>`; puerta:
   `uv run botsito corpus frames check` (0 huecos, 0 extra).
6. **Extraccion por pregunta.** La deteccion automatica («pregunta» + codigo ... «fin de pregunta»)
   dio 0 en v7 y en v9, y no se afloja (`SESION-DE-PREGUNTAS.md`). Se localiza a mano en la
   filtrada, por los codigos sueltos o el texto leido de la pregunta; la cita es el literal de la
   filtrada con su `mm:ss`, y el hablante se atribuye por contexto y se declara en `revisado_por`.
   Por cada codigo: resuelve / en parte / no resuelve, con la cita.
7. **Evidencia.** `uv run botsito evidence new --video <vN> --t0 ... --t1 ... --cita "..."` con su
   tipo, tema y confianza (o la via `evidence propose` / `--check` / `accept`, que no admite
   `supersede`); la cita se comprueba contra la cruda, asi que copiarla de la filtrada funciona
   fuera de los bloques en cuarentena. Despues `uv run botsito evidence contradictions`.
8. **Sello y commits**: estadiar → `make check > make-check.log 2>&1` → commit, por fase.

## Artefacto

`docs/validation/SESION-NN-EXTRACCION.md` -cortes de audio, cuarentena (cuantos segmentos y bloques,
sin contenido), por cada codigo de la hoja su propuesta con cita, y la tabla final- mas la entrada
de `fuentes.yaml`, los manifiestos de transcripcion y fotogramas, los tramos no citables y los
items de evidencia nuevos.

## Verificacion

- `uv run botsito corpus check --hashes`, `corpus transcript check` y `corpus frames check` en verde.
- `uv run botsito knowledge validate > knowledge-validate.log 2>&1` en verde (ids, tramos, citas).
- `git diff --name-status main...HEAD -- knowledge/evidence knowledge/corpus/transcripciones
  knowledge/corpus/fotogramas data/manifests`: solo `A`.
- Ninguna cita del informe ni de la evidencia cae en un tramo de `tramos_no_citables.yaml`.
- `make check` sellado y el revisor pasado antes de declarar la rama lista.
