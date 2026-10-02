# FUNCTIONALITY VALIDATION REPORT · Ajustes tras el cierre de F36l

Rama `trabajo/ajustes-cierre`, abierta el 2026-10-01 desde `main` `72d0d20` (tag
`stable/F36l-cuarentena-por-defecto`). Encargo, copiado tal cual:
`docs/encargos/trabajo-ajustes-cierre.md`. Solo documentacion y la skill `cerrar-rama`: no cambia
codigo, spec, cifras ni datos (`git diff --stat main` no toca `src/`, `tests/`, `scripts/`,
`.claude/hooks/`, `knowledge/spec/`, `knowledge/evidence/` ni `data/`).

## 1. `knowledge/corpus/tramos_no_citables.yaml`

**El regimen, comprobado antes de tocarlo.** `CLAUDE.md` («Regimenes de cambio») no nombra este
fichero: no es INMUTABLE (el hook `pre-commit` solo lo es para `knowledge/evidence`,
`knowledge/feedback`, `data/manifests`, `knowledge/corpus/transcripciones` y
`knowledge/corpus/fotogramas`), no es SOLO ANADIR (eso es `knowledge/corpus/libros.yaml`) y la
guardia mecanica del trailer `Fuente:` no lo cubre (`comun/historial.py`,
`DIRECTORIOS_CON_FUENTE = ("knowledge/spec/", "knowledge/cases/")`). Se puede editar. Lo que si
pide `Fuente:` es su propia cabecera («Manual, versionado; cada commit cita `Fuente:`»), y por eso
el commit lo lleva, con el informe que el encargo nombra: `docs/validation/CUARENTENA-POR-DEFECTO.md`.
No hay ningun ADR de la cuarentena por defecto: la rama la gobernaron las seis ordenes del
consultor, copiadas en `docs/encargos/trabajo-cuarentena-por-defecto.md`.

**El cambio.** Solo el comentario de cabecera; los tramos no se tocan. Decia «el tramo sigue en la
cruda y se puede leer y buscar con `kb find`». Ahora dice que el tramo sigue en la cruda, sin tocar,
y que desde F36l tampoco se ENSENA por defecto: `kb find`, `kb at`, `corpus transcript show`,
`corpus frames show` y `evidence propose` ocultan sus segmentos y dicen cuantos y por que; `kb`
oculta tambien la evidencia cuya cita cae en un tramo o que lo copia (y, por otro motivo, la que
trae un dia de `casos_ocultos`: anadido por el revisor, A3); la opcion que lo ensena todo
es solo de Aleks en su terminal, y la guardia la bloquea. `knowledge validate` en verde despues.

## 2. La skill `cerrar-rama` y `RITUAL.md`: lo que todo cierre lleva

**`docs/runbooks/RITUAL.md`, «Antes del merge: el contrato sale de la rama».** Antes, el registro en
HISTORIA iba «si la orden de cierre pide» uno. Ahora el apartado dice que TODO cierre lleva, en el
mismo commit que saca el contrato y aunque la orden no lo repita:
1. el registro del cierre al final de `docs/state/HISTORIA.md` (`# Registro de cierre · <rama>
   (<fecha>)`), con el tag y el merge como `git rev-parse "stable/<tag>^{commit}"`, los commits de
   la rama y los runs de la CI con su resultado (los de Linux por `fix/<rama>`, o que no hubo);
2. la fila de la rama en la tabla de `docs/runbooks/ERRORES-RECURRENTES.md`, con los hallazgos del
   revisor y los del consultor, y lo que se le escapo al revisor. Si la orden no trae los del
   consultor, la sesion los pregunta antes del commit, y no deja la columna en «se apunta al
   cerrar».
El commit se llama siempre `chore(cierre): sale el contrato y entra el registro en HISTORIA`; el
bloque de comandos estadia los dos ficheros, y la puerta exige ver las tres lineas en
`git status --short`.

**`RITUAL.md`, la edicion de `PROJECT_STATE.md`.** Antes: «Completed Features gana una línea y
Change Log una entrada». Ahora: solo las lineas de cabecera (Current Branch, Current Feature, Stable
Main State, Next Action y Last Stable Commit), y **en el commit de estado no se añade NADA a Change
Log ni a Completed Features**, aunque la orden no lo repita. La frase vieja se nombra en el propio
parrafo, con la fecha del cambio.

**`.claude/skills/cerrar-rama/SKILL.md`.** Lo mismo, en sus palabras: la `description`; tres filas
nuevas en «Entradas» (commits y runs, hallazgos del revisor, y hallazgos del CONSULTOR, que «se
preguntan ANTES del commit del contrato»); «Herramientas» (Edit de HISTORIA y ERRORES-RECURRENTES,
en la rama); el paso 3 (las dos cosas, SIEMPRE); el paso 5 (solo cabecera, nada a Change Log ni a
Completed Features); «Artefacto»; y dos lineas de «Verificacion» (el ultimo commit de la rama es el
`chore(cierre)` con las tres cosas, y el commit de estado solo toca `PROJECT_STATE.md` sin tocar
esas dos secciones).

**Ampliacion del contrato, declarada.** `docs/state/README.md` decia que `PROJECT_STATE.md` lleva
«lo cerrado desde el ultimo archivo (Completed Features y Change Log)», lo contrario de lo que pide
el punto 2. Se corrigio en el mismo commit -las dos secciones siguen, pero el cierre no les anade
nada; lo cerrado va al registro de HISTORIA- y el contrato se amplio a ese fichero con su motivo en
un comentario. Por el revisor (A1), tambien las dos lineas de introduccion de `Completed Features`
y `Change Log` en `PROJECT_STATE.md` dicen ya que el cierre no les anade nada.

**Lo que queda, y por que.** El comentario de `SECCIONES_EXENTAS` en
`tests/contract/test_documentos_vivos.py` sigue diciendo que `Completed Features` lleva «una linea
por rama cerrada». Es un comentario de un test, y `tests/` esta en `rutas_protegidas` porque el
encargo dice que la rama no cambia codigo: no se toca aqui. No cambia lo que el test comprueba (la
seccion sigue exenta, haya lineas o no). Queda para la rama siguiente que toque ese test.

## 3. Otras frases sobre la CLI y la cruda: lo que se busco y lo que se cambio

Buscado en `CLAUDE.md`, `docs/runbooks/` y `.claude/skills/` (y en `.claude/agents/` y
`docs/state/README.md`): `kb find`, `kb at`, `transcript show`, `frames show`, «sin filtrar»,
«cruda entera», «imprime/enseña/muestra la cruda» y frases que juntan tramos con leer o buscar.

| Fichero | Que decia | Que hace ahora |
|---|---|---|
| `knowledge/corpus/tramos_no_citables.yaml` | un tramo «se puede leer y buscar con `kb find`» | §1 |
| `docs/runbooks/MIRAR-EL-MATERIAL.md` | las propuestas de `knowledge/_proposals/` son «la via mas rapida» para ver el tramo, sin decir que 10 de ellas ya no se leen; y no nombraba la CLI filtrada | dice que las que copian segmentos ocultos no se leen (lista calculada, la guardia), y un recuadro: desde F36l la via para LEER es la CLI, que ensena filtrado, con la opcion entera solo para Aleks; los ficheros de `data/transcripciones/` no pasan por ese filtro (crudas de v7 en adelante bloqueadas; v6 por trozos) |
| `docs/runbooks/SESION-DE-PREGUNTAS.md` («Despues», paso 5) | la cita de un registro de feedback se copia de la «transcripción CRUDA (`.../cruda.txt`)» de la sesion | se copia de la FILTRADA (`<stem>.filtrada.md`), que fuera de los bloques en cuarentena es literal de la cruda; la cruda de una sesion no la lee nadie mas que Aleks, y la guardia la bloquea desde v7. El hueco del comando pasa a `"<literal de la filtrada>"` |
| `docs/runbooks/ACTIVAR-A35-A44.md` (§1, el paso 2 de la lectura nueva y el bloque de A-44) | lo mismo que la fila anterior, en tres sitios | lo mismo: «la cita de la filtrada» en los tres, y los cuatro huecos `"<literal de la cruda>"` pasan a `"<literal de la filtrada>"` |

**Las dos ultimas filas no son la letra del punto 3** -no dicen que la CLI ensene la cruda, sino que
se copie de la cruda de una sesion-, pero es el mismo defecto: un procedimiento vivo que manda leer
lo que la cuarentena dice que no lee nadie, y que la skill `ingerir-sesion` (paso 6) ya resolvia
con la filtrada. Se declaran por eso.

**Ya estaban bien, y no se tocaron:** `CLAUDE.md` («Las guardias de Claude Code»: «La CLI ensena el
corpus filtrado»; `MIRAR-EL-MATERIAL.md` por puntero) y `.claude/skills/ingerir-sesion/SKILL.md`
(«Limites»: la CLI ensena el corpus FILTRADO por defecto). Ninguna frase de `.claude/agents/` ni de
las demas skills habla de la CLI y la cruda.

## 4. Comprobaciones

- `uv run botsito state check`: OK.
- `uv run botsito knowledge validate > knowledge-validate.log 2>&1`: exit 0 (144 registros de
  feedback, 437 items de evidencia, historial intacto; `tramos_no_citables.yaml` se sigue leyendo).
- Los tests que leen estos ficheros, en verde: `test_push_atomico.py` (los bloques de `RITUAL.md`),
  `test_hooks_utf8.py`, `test_cuarentena.py` (la lista de tramos), `test_historia.py`,
  `test_project_state.py` y `test_documentos_vivos.py`.
- `make check` sellado antes de cada commit; la rama no toca hooks ni la plataforma, asi que no se
  empujo a `fix/` (lo dice el encargo).

## 5. Informe del revisor

Subagente `revisor`, sobre el trabajo ESTADIADO antes del sello (para que su informe entre en el
mismo commit). Los hallazgos, tal cual; lo comprobado sin hallazgos y la tabla de requisitos,
resumidos.

> ## Informe del revisor · trabajo/ajustes-cierre · 2026-10-01
>
> Revisado sobre `git diff --cached` y `git diff --cached main`. El trabajo está estadiado y sin commitear: solo existe el commit de apertura `5cdbddf`.
>
> ### Eje (a) · Reglas de la casa
> Resumen: 0 bloquea, 2 importa, 3 menor.
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | A1 | importa | Queda un documento vivo que contradice el punto 2. `PROJECT_STATE.md` dice que Completed Features y Change Log llevan «las cerradas / las entradas desde el ultimo archivo», y el comentario de `tests/contract/test_documentos_vivos.py` dice «lo cerrado desde el ultimo archivo» y «una linea por rama cerrada». Ni el informe ni el contrato lo mencionan. `PROJECT_STATE.md` está en `rutas_permitidas`; los tests están protegidos y no se pueden tocar. | `PROJECT_STATE.md:192-199`; `tests/contract/test_documentos_vivos.py:54-64` |
> | A2 | importa | Corrección incompleta en `docs/runbooks/ACTIVAR-A35-A44.md`. Se cambió la cita a «la filtrada» en §1 y en los 4 huecos `--respuesta`, pero siguen mandando copiar de la cruda la línea 168 («la cita de la cruda y el tramo») y la 218 («con la cita de la CRUDA:»). La 218 introduce justo el bloque cuyos huecos sí se cambiaron, así que el documento queda incoherente. Además el informe dice «cinco huecos» y el diff cambia cuatro. | `ACTIVAR-A35-A44.md:168`, `:218`; informe §3, fila 4 |
> | A3 | menor | El comentario nuevo de `tramos_no_citables.yaml` no es del todo exacto respecto a lo que oculta `kb`. Dice «cuya cita cae en un tramo o cuyo texto lo copia». El código también oculta la evidencia que trae un día de `casos_ocultos`. Es cierto en lo que afirma pero incompleto, y el punto 1 pide «EXACTAMENTE». | `cuarentena.py:507-525`; `CLAUDE.md:239-241` |
> | A4 | menor | El trailer `Fuente:` del commit de trabajo aún no existe. El informe declara que el commit citará `docs/validation/CUARENTENA-POR-DEFECTO.md`, que no es un id válido (`ev-*`, `fb-*` o `ADR-NNNN`). La guardia mecánica no cubre este fichero, y el encargo permite nombrar el informe, así que no bloquea. Conviene que el mensaje lo cite en el cuerpo, no en el asunto. | informe §1 |
> | A5 | menor | El informe afirma «`make check` sellado antes de cada commit» y «10 de ellas (propuestas) ya no se leen» sin una evidencia que yo pueda ver: no hay `make-check.log` y no leí la lista de propuestas. | informe §3 y §4 |
>
> Comprobado sin hallazgos: el alcance (solo documentación, la skill, el yaml, el contrato y los ficheros de apertura); el contrato y la ampliación a `docs/state/README.md`; el régimen del yaml; el comentario frente al código (`--crudo` en los cuatro comandos, `evidence propose` filtra siempre, `indice.py` oculta la evidencia solo sin la opción); en el punto 3 no queda ninguna frase que diga que la CLI enseña la cruda sin filtrar o que `kb find` muestra tramos no citables; `MIRAR-EL-MATERIAL.md` y `SESION-DE-PREGUNTAS.md` coherentes con `CLAUDE.md` y con `ingerir-sesion`; ningún ADR ni informe cerrado tocado.
>
> ### Eje (b) · Encargo
> Resumen: 0 bloquea, 0 importa, 1 menor. Requisitos: 8 hechos, 1 parcial (el trailer `Fuente:`, pendiente del commit), 0 no hechos.
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | B1 | menor | Dos correcciones fuera de la letra del punto 3 (`SESION-DE-PREGUNTAS.md` y `ACTIVAR-A35-A44.md`) están bien declaradas en el informe y son de la misma familia. La de `ACTIVAR` quedó incompleta (ver A2). La ampliación del contrato a `docs/state/README.md` está declarada y justificada. | informe §2 y §3 |
>
> ### Lo que no pude comprobar
> El trailer `Fuente:` y el sello de `make check` (no hay commit ni log); el contrato con `scripts/contrato_rama.py` (va dentro de `make check`); el detalle de las propuestas y salidas con segmentos ocultos (no las leí, por restricción).

**Respuesta de la sesion, hallazgo a hallazgo:**
- **A1, arreglado en lo que la rama puede tocar**: las dos introducciones de `Completed Features` y
  `Change Log` en `PROJECT_STATE.md`. El comentario del test se queda, declarado en §2: `tests/` esta
  protegida y el comentario no cambia lo que el test comprueba.
- **A2, arreglado**: las lineas 168 y 218 dicen ya «la filtrada»; `grep -i cruda` en el fichero solo
  da la frase que explica que la cruda no la lee nadie mas que Aleks. El informe dice «cuatro»
  huecos.
- **A3, arreglado**: el comentario nombra tambien el dia de `casos_ocultos`, como otro motivo.
- **A4**: el commit lleva `Fuente: docs/validation/CUARENTENA-POR-DEFECTO.md` en el CUERPO, que es
  lo que el encargo permite; no es un id de la guardia, y la guardia no cubre este fichero.
- **A5, medido**: `.claude/hooks/ficheros_con_ocultos.txt` lista 10 rutas de `knowledge/_proposals/`
  (`grep -c`); el sello de `make check` es el del commit (el hook `pre-commit` lo exige).
- **B1**: declarado; A2 lo completa.

## Estado

**Rama lista para revisión, NO cerrada.** Los tres puntos del encargo estan hechos, con el revisor
pasado y sus hallazgos atendidos. Sin CI de Linux por `fix/`: la rama no toca hooks ni la
plataforma (lo dice el encargo).
