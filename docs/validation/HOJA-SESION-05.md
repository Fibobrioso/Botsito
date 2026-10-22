# HOJA-SESION-05 · La hoja de la sesión 5 en el guion de transcripción, antes de grabar (R4.1)

Rama `trabajo/hoja-sesion-05`, abierta el 2026-10-22 desde `main` en 7e6dec2 (commit de estado
sobre el merge e4563db, tag `stable/F37y-previa-sesion-5`). Encargo:
`docs/encargos/trabajo-hoja-sesion-05.md`. Tramo: R4 (R4.1 de `docs/plan/HOJA-DE-RUTA.md`; V de
la Next Action). Modelo de la sesión: `claude-opus-5-5`, con esfuerzo medio (`/effort` de Aleks).

## 0 · La base, comprobada al abrir

| Comprobación | Comando | Salida |
|---|---|---|
| `main` es 7e6dec2 y es `origin/main` | `git rev-parse main`; `git rev-parse origin/main` | dos veces `7e6dec2b686049b344e06422a6afd583e8f47e79` |
| El tag apunta al merge bajo `main` | `git rev-parse main^1`; `git rev-parse "stable/F37y-previa-sesion-5^{commit}"` | dos veces `e4563db76fc3fcb5102dba557b34cc478010107d` |
| La CI de `main` sobre su HEAD | `gh run view 39727304930 --json status,conclusion,headSha`, a mano y una vez | `{"conclusion":"success","headSha":"7e6dec2b686049b344e06422a6afd583e8f47e79","status":"completed"}` |
| Ninguna otra rama | `git branch --list`; `git ls-remote --heads origin "fix/*"` | `* main`; vacío |

`make check` del commit de apertura (adcc76b): exit 0, `2729 passed in 948.10s`, ningún `failed`,
`SELLO: make check en verde sobre el arbol e01e52eabdb39b38c2078255b35b483462182dbd`,
`PICO DE MEMORIA de make check: 295 MiB en `test` (suma de sus procesos, memoria comprometida, Windows; el mayor proceso, 285 MiB)`.

## 1 · Fase 0: lo medido (sin escribir código)

Las líneas son las de `main` (7e6dec2), antes de tocar nada. Esta rama no leyó ningún material del
punto 3 de `CLAUDE.md`, ni transcripciones, ni fotogramas: solo el guion, sus tests, la skill, los
runbooks y `docs/sesion-5/PREGUNTAS.md`, que es un documento de la rama anterior.

**a) Cómo se usan los códigos en `scripts/transcribir_sesion.py`:**
- `CODIGOS_DE_SESION_TEXTO` (`:124-161`): un diccionario por sesión. Sus CLAVES son los códigos de
  sesión válidos de esa sesión, y sus valores, el texto de cada uno.
- `codigos_validos(sesion)` (`:631-641`): las ambigüedades ABIERTA o DECIDIDA de
  `ambiguedades.yaml` más `tuple(CODIGOS_DE_SESION_TEXTO[sesion])`. Así que un código de sesión
  solo abre una pregunta si tiene texto en la hoja de esa sesión.
- `codigo_en(texto, validos)` (`:203-214`): el último «pregunta <letra> <número>» cuyo código está
  entre los válidos. El número va por `numeros_a_cifras` (`botsito.corpus.cuarentena`) y el patrón
  admite una o dos cifras (`_RE_CODIGO`, `:195-199`), así que S-25 cabe. Medido sin leer material:
  `numeros_a_cifras(normalizar("pregunta ese veinticinco"))` da `pregunta ese 25`.
- `HOJAS` (`:163-167`): el orden de cada sesión, con el que se agrupa la filtrada; `SESION_EN_CURSO`
  (`:168`) es `"04"`.
- `orden_de_preguntas(presentes, hoja)` (`:307-314`): primero los presentes en el orden de la hoja,
  después los demás por letra y número, y SIN PREGUNTA al final.
- `registro_filtro(..., validos, hoja, ...)` (`:344-387`): lista los detectados en el orden de la
  hoja y los de la hoja sin detectar (`no_detectados`, `:366`, la línea «SIN codigo detectado»).
- `procesar` (`:607-613`): `codigos_validos(sesion)` y `HOJAS[sesion]` para la filtrada y el
  registro.
- La opción `--sesion` (`:653-658`): `default=SESION_EN_CURSO`, `choices=tuple(HOJAS)`.

Lo que pide la hoja 05, entonces: `ORDEN_SESION_05`, `CODIGOS_DE_SESION_TEXTO["05"]` (sin él, S-25
no abre nada), `HOJAS["05"]` (sin él, `--sesion 05` no se acepta) y `SESION_EN_CURSO = "05"`. Nada
más del guion cambia.

**b) Los tests que fijan la sesión en curso o la hoja 04**, en `tests/unit/test_transcribir_sesion.py`:
- `test_el_orden_es_el_de_la_hoja_de_la_sesion_04` (`:398-405`): el orden de la 04, su texto y
  `assert m.SESION_EN_CURSO == "04"` (`:403`), como dice el encargo;
- `test_s1_tiene_un_texto_por_sesion_y_la_hoja_03_no_cambia` (`:408-416`),
  `test_los_codigos_validos_son_los_de_la_hoja_de_cada_sesion` (`:419-425`),
  `test_la_sesion_04_abre_con_ese_y_el_numero` (`:438-439`) y
  `test_la_filtrada_de_la_04_agrupa_con_su_hoja` (`:442-448`): fijan la 03 y la 04, pero nombrando
  la sesión, así que no dependen de la sesión en curso y no cambian.

**c) Los documentos que nombran la sesión en curso o el `--sesion` por defecto del guion:**
- `.claude/skills/ingerir-sesion/SKILL.md:69`: `transcribir_sesion.py --audio … --video <vN>` sin
  `--sesion`. Para la sesión 5 sigue siendo cierto: con la hoja por defecto en 05, la sesión que se
  ingiere es la de la hoja por defecto. **No queda falso.**
- `.claude/skills/ingerir-sesion/SKILL.md:20`: la hoja es `ORDEN_SESION_NN` en el guion. Sigue cierto.
- `docs/runbooks/SESION-DE-PREGUNTAS.md` y `docs/runbooks/MIRAR-EL-MATERIAL.md`: no nombran el
  `--sesion` del guion ni la sesión en curso. Los `--sesion` de SESION-DE-PREGUNTAS.md (`:157`) y de
  otros runbooks son de `botsito feedback`, y `ORDEN_SESION_02` (`:69`) es de
  `scripts/hoja_preguntas.py`. Medido con un Grep de `--sesion|SESION_EN_CURSO|sesion en curso|ORDEN_SESION_0|HOJAS\[|CODIGOS_DE_SESION_TEXTO`
  sobre `.claude/skills`, `docs/runbooks`, `CLAUDE.md`, `docs/plan` y `PROJECT_STATE.md`.
- El único que queda falso es el propio docstring del guion (`:48-52`): su ejemplo
  `--video v10 --solo-filtrar`, sin `--sesion`, con la hoja por defecto en 05 agruparía v10 con la
  hoja 05. Se corrige en la fase 1, como pide el encargo.

Nada de esto pide más de lo que dice el encargo: **sin PARADA**.

**d) El orden de PREGUNTAS.md es el numérico:** `grep -n '^\*\*S-[0-9]*\.'` da S-1 a S-25 en orden
creciente de línea (de `:74` a `:779`, en el fichero de `main`).

**Una observación que no cambia nada:** `numeros_a_cifras` pasa «veinte y cinco», en tres palabras,
a `20 y 5`, y entonces «pregunta ese veinte y cinco» abriría S-20 y no S-25. Ya pasaba con S-21 a
S-24 en la sesión 04, y el ASR escribe «veinticinco», en una palabra, o la cifra. Se deja dicho
para quien lea la filtrada de la 05; no es de esta rama.

## 2 · Fase 1: la hoja 05

En `scripts/transcribir_sesion.py`:
- **El docstring** (`:47-54`): el primer ejemplo es la sesión nueva (`--video v15`, sin `--sesion`)
  y el de `--solo-filtrar` lleva `--video v10 --sesion 04`. Dice además que una re-filtrada de una
  sesión anterior lleva SIEMPRE su `--sesion`: **v9 se filtra con `--sesion 03` y v10 con
  `--sesion 04`**; sin ella, se agruparía sin aviso con la hoja de la sesión en curso. (v15 es el id
  que el encargo da a la sesión 5, que entra con la ingesta: aquí solo es el ejemplo.)
- **`ORDEN_SESION_05`** (`:127-131`): S-1 a S-25 en el orden de la hoja, con el comentario que pide
  el encargo encima (`:121-126`).
- **`CODIGOS_DE_SESION_TEXTO["05"]`** (`:176-206`): el título de cada pregunta de
  `docs/sesion-5/PREGUNTAS.md`, sin «S-n. » ni lo que va detrás de la negrita (en S-1, las dos líneas
  de la negrita, unidas), con la primera letra en minúscula; S-7 y S-12, el «Título» de su recuadro
  de corrección del 2026-10-21. El comentario de encima del diccionario (`:132-138`) lo dice.
- **`HOJAS["05"] = ORDEN_SESION_05`** (`:212`) y **`SESION_EN_CURSO = "05"`** (`:214`).
- Las hojas 02, 03 y 04 no cambian.

En `tests/unit/test_transcribir_sesion.py`:
- `test_el_orden_es_el_de_la_hoja_de_la_sesion_04` (`:399`) pierde `SESION_EN_CURSO == "04"`; el
  orden de la 04 se queda.
- Cinco tests nuevos (`:452-515`):
  - `test_la_hoja_05_tiene_los_25_codigos_con_su_texto`: S-1 a S-25 en orden numérico, y el texto de
    cada uno igual al título que **lee de `docs/sesion-5/PREGUNTAS.md`**: si la hoja o el guion
    cambian uno sin el otro, falla;
  - `test_la_sesion_en_curso_es_la_05`: `SESION_EN_CURSO == "05"` y `HOJAS["05"] is ORDEN_SESION_05`;
  - `test_s25_vale_en_la_05_y_no_en_la_04`: con `codigos_validos` y con «pregunta ese veinticinco»;
  - `test_la_03_y_la_04_no_cambian`: las hojas de la 03 y la 04, dos textos y la filtrada de la 04;
  - `test_la_filtrada_de_la_05_agrupa_con_su_hoja` (de más: no lo pide el encargo): con la hoja 05,
    S-7 va antes que S-22, al revés que en la 04, y S-25 abre su pregunta.

**Los tests, rotos a propósito en los dos sentidos.** Con
`docs/validation/anexos/HOJA-SESION-05/romper_tests.py <raiz>`: carga el guion y los tests, y corre
cada test tal cual y con mutaciones en memoria, al menos una por sentido, deshaciendo cada una antes
de la siguiente; no escribe nada (tampoco en PREGUNTAS.md: la mutación del lado de la hoja cambia lo
que el test LEE, no el fichero). Tras la revisión (b2 y b3, §10) lleva tres mutaciones más: el lado
de la hoja en el test de los textos, y dos que llegan al orden y al agrupado de la 04. Salida
(`PYTHONUTF8=1 uv run python … .`):

```
test_la_hoja_05_tiene_los_25_codigos_con_su_texto: tal cual -> pasa
  roto (S-7 con el titulo del cuerpo y no el del recuadro) -> FALLA en test_transcribir_sesion.py:478: assert m.CODIGOS_DE_SESION_TEXTO["05"] == titulos
  roto (sin S-25 (la hoja de 24 codigos)) -> FALLA en test_transcribir_sesion.py:478: assert m.CODIGOS_DE_SESION_TEXTO["05"] == titulos
  roto (del lado de la hoja: el titulo de S-9 cambiado en lo que se lee de PREGUNTAS.md) -> FALLA en test_transcribir_sesion.py:478: assert m.CODIGOS_DE_SESION_TEXTO["05"] == titulos
  de nuevo tal cual -> pasa
test_s25_vale_en_la_05_y_no_en_la_04: tal cual -> pasa
  roto (S-25 tambien en la 04) -> FALLA en test_transcribir_sesion.py:490: assert "S-25" not in v04
  roto (S-25 fuera de la 05) -> FALLA en test_transcribir_sesion.py:489: assert "S-25" in v05
  de nuevo tal cual -> pasa
test_la_03_y_la_04_no_cambian: tal cual -> pasa
  roto (la hoja 04 con S-1 y S-2 cambiados de sitio) -> FALLA en test_transcribir_sesion.py:498: assert m.HOJAS["04"] is m.ORDEN_SESION_04
  roto (el texto de S-1 de la 03 cambiado) -> FALLA en test_transcribir_sesion.py:501: assert m.CODIGOS_DE_SESION_TEXTO["03"]["S-1"] == "cómo decide el sesgo del día"
  roto (la hoja 04 reordenada en su sitio (ORDEN_SESION_04 y HOJAS['04'] a la vez)) -> FALLA en test_transcribir_sesion.py:499: assert list(m.ORDEN_SESION_04) == ORDEN_04
  roto (la hoja 04 con S-22 al final (lo agrupa despues de S-7)) -> FALLA en test_transcribir_sesion.py:499: assert list(m.ORDEN_SESION_04) == ORDEN_04
  roto (las hojas intactas y el agrupado sin mirar la hoja (por letra y numero)) -> FALLA en test_transcribir_sesion.py:505: assert texto.index("## S-1\n") < texto.index("## S-22") < texto.index("## S-7")
  de nuevo tal cual -> pasa
test_la_sesion_en_curso_es_la_05: tal cual -> pasa
  roto (SESION_EN_CURSO = 04 (lo de main)) -> FALLA en test_transcribir_sesion.py:483: assert m.SESION_EN_CURSO == "05"
  roto (HOJAS['05'] con la hoja de la 04) -> FALLA en test_transcribir_sesion.py:484: assert m.HOJAS["05"] is m.ORDEN_SESION_05
  de nuevo tal cual -> pasa
todo como se espera
```

Cada fallo cae en la aserción de lo que se rompe. La mutación «SESION_EN_CURSO = 04» es justo el
guion de `main`. `uv run pytest -q tests/unit/test_transcribir_sesion.py`: todos pasan; `ruff check`
y `ruff format --check` en verde sobre los tres ficheros de Python. `Tests Currently Passing` pasa
de 1642 a 1647 funciones (`state check` lo pidió).

**Ningún documento de la fase 0 quedó falso**, salvo el docstring, corregido arriba. No hay
recuadros. **Pero la fase 0 no miró `docs/sesion-5/`, y allí hay uno que sí** (revisor, b1, §10):
`docs/sesion-5/PREGUNTAS.md:22-24` dice que los textos de los códigos «entran en ese script con la
ingesta de la sesión (`CODIGOS_DE_SESION_TEXTO["05"]`), no aquí», y sus recuadros de S-7, S-12 y
S-13 (`:246`, `:415`, `:483`) dicen que su texto va a `CODIGOS_DE_SESION_TEXTO["05"]` «con la
ingesta». Desde esta rama entran antes, aquí. **No lo corrijo**: el encargo dice que PREGUNTAS.md
no se toca. Lo que sigue siendo cierto es lo que importa para la sesión: el texto que vale es el de
los recuadros, y es el que lleva el guion. Propuesta para el consultor, en §6.

## 3 · Fase 2: la regla del 2026-10-21

En `docs/runbooks/DECISIONES-DE-PROCESO.md`, «Decisions and Rationale», una entrada con el formato
de las de 2026-09-04 (fecha · decisión. Problema. Alternativas. Estado: ACTIVE), con fecha
2026-10-21. Dice que **nace aquí** (`trabajo/hoja-sesion-05`) y no viene de la mudanza de
PROJECT_STATE. Lleva las dos frases del encargo, literales, cada una con su origen, verificado:

| Frase | Origen | Verificado en |
|---|---|---|
| «Si la guardia o el clasificador niegan un comando, PARADA, salvo seguir la forma que la propia guardia propone en su mensaje, declarándolo en el informe.» | el encargo de `trabajo/previa-sesion-5`, «0. Apertura» | `docs/encargos/trabajo-previa-sesion-5.md:13` («Regla del consultor desde el 2026-10-21: si la guardia o el clasificador niegan un comando, PARADA, salvo seguir la forma que la propia guardia propone en su mensaje, declarándolo en el informe») |
| | `PREVIA-SESION-5.md`, que la aplicó | `docs/validation/PREVIA-SESION-5.md:28` («regla del consultor del 2026-10-21: PARADA salvo seguir la forma que propone la guardia, declarándolo») |
| | el antecedente de EA-CONEXION | `docs/validation/EA-CONEXION.md:1076`, §12, fila 3g («PARADA, sin cambiar de vía ni reescribirlo»), que la orden de cierre de esa rama corrigió a la forma de hoy (registro de cierre de `trabajo/ea-conexion` en `docs/state/HISTORIA.md`, punto 3) |
| «Ninguna consulta de la CI con un guion ni con un bucle.» | EA-CONEXION.md §13 y su fila de hallazgos | `EA-CONEXION.md:1077`, §12, fila 0/7 («el guion de espera de §13»); y la fila de `trabajo/ea-conexion` en `docs/runbooks/ERRORES-RECURRENTES.md` |
| | la orden de cierre de SESGO-H4-COLOR | `docs/validation/SESGO-H4-COLOR.md:1301`, en §10 («Orden de cierre del consultor», `:1269`): «cambiar de vía tras una negativa es rodearla». **Matiz:** la frase es de la orden de cierre de `trabajo/sesgo-h4-color`, pero el hallazgo que la lleva es sobre el cierre de `trabajo/corrida-construccion`; la entrada lo dice |
| | la línea de Technical Debt sobre el guion que espera a la CI | `PROJECT_STATE.md:104` («La guardia no niega un guion que espera a la CI en bucle…»), que sigue abierta para el carril de guardias |

Ningún test exige que esto viva en otro sitio: `grep -rn 'DECISIONES-DE-PROCESO\|Decisions and
Rationale'` sobre `tests/`, `src/` y `scripts/` solo da el comentario de
`tests/contract/test_tramos_fuente.py:5`, que ya está en Technical Debt. **Sin PARADA.** La
cabecera del runbook dice ahora que, desde el 2026-10-22, también lleva entradas que nacen allí.

## 4 · Exposiciones

Ninguna. La rama no leyó transcripciones, fotogramas, libros, casos ni nada reservado; ni
consultó `casos_ocultos`. La única lectura de un texto del trader son los títulos de
`docs/sesion-5/PREGUNTAS.md`, que son preguntas nuestras.

## 5 · Lo que NO cambia

`git diff main --stat` (abajo, en la entrega): `scripts/transcribir_sesion.py`,
`tests/unit/test_transcribir_sesion.py`, `docs/runbooks/DECISIONES-DE-PROCESO.md`, el anexo
`romper_tests.py`, el informe, el encargo, `contrato.yaml`, `PROJECT_STATE.md` y
`docs/state/HISTORIA.md`. Nada del motor, la spec, las ambigüedades, el feedback, los casos, el
corpus, `fuentes.yaml` ni la cuarentena (`src/botsito/corpus/cuarentena.py` sin tocar); y
`docs/sesion-5/PREGUNTAS.md` intacto (`docs/sesion-5/` está protegido en el contrato).

## 6 · Líneas preparadas para el commit del contrato de la orden de cierre

- **PROJECT_STATE, V:** tras «…con los recuadros de corrección de S-7, S-12, S-13 y S-15
  (trabajo/previa-sesion-5): la primera parte de S-12 decide si RN-005 sigue o se reabre
  (PREVIA-SESION-5.md §1).», añadir: «La hoja 05 está en `scripts/transcribir_sesion.py`, por
  defecto (trabajo/hoja-sesion-05); v9 y v10 se re-filtran con `--sesion 03` y `--sesion 04`.»
  (unos 160 bytes; PROJECT_STATE quedaría hacia 22.560).
- Ninguna letra pasa a HECHA (V se cumple con la sesión y su activación); la hoja de ruta no
  cambia.
- **Para decidir el consultor (revisor, b1):** `docs/sesion-5/PREGUNTAS.md:22-24` y sus recuadros
  de S-7, S-12 y S-13 dicen que los textos entran en `CODIGOS_DE_SESION_TEXTO["05"]` «con la
  ingesta», y entran en esta rama. Opciones: (a) un recuadro de corrección en PREGUNTAS.md, junto a
  `:22-24`, en el commit del contrato de la orden de cierre (habría que ampliar el contrato a
  `docs/sesion-5/PREGUNTAS.md`), que diga: «Desde `trabajo/hoja-sesion-05` (2026-10-22) los textos
  de los códigos ya están en `scripts/transcribir_sesion.py`, `CODIGOS_DE_SESION_TEXTO["05"]`,
  antes de grabar: S-7 y S-12 con el título de su recuadro, y los demás con el suyo. Lo que dicen
  los recuadros sobre «con la ingesta» vale ahora para esta rama»; (b) dejarlo para la rama de la
  ingesta, que escribe `docs/sesion-5/HOJA-USADA.md`. Recomiendo (a): es una línea, y quien abra la
  ingesta lee PREGUNTAS.md antes que nada.

## 7 · El encargo, punto por punto

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 0 | Base: 7e6dec2, `origin/main`, el tag sobre e4563db, ninguna otra rama; abrir con `abrir-rama` y el encargo tal cual con la fecha | Hecho | §0; adcc76b |
| R1 | Guardia o clasificador: PARADA salvo la forma que proponen | Hecho | ninguna negativa en esta rama |
| R2 | La CI con un `gh run view` suelto cada vez | Hecho | §8 |
| F0.1 | Uso de `codigos_validos`, `HOJAS`, `CODIGOS_DE_SESION_TEXTO`, `orden_de_preguntas`, `registro_filtro`, `--sesion` | Hecho | §1.a |
| F0.2 | Tests que fijan la sesión en curso o la 04 | Hecho | §1.b |
| F0.3 | Documentos que nombran la sesión en curso o el `--sesion` por defecto | Hecho | §1.c: solo el docstring queda falso |
| F1.1 | `ORDEN_SESION_05` S-1..S-25 en el orden de la hoja (numérico, verificado), con su comentario | Hecho | §1.d, §2 |
| F1.2 | `CODIGOS_DE_SESION_TEXTO["05"]` con los títulos; S-7 y S-12 del recuadro; S-13 y S-15 con el suyo | Hecho | §2; el test los compara con PREGUNTAS.md |
| F1.3 | `HOJAS["05"]` y `SESION_EN_CURSO = "05"` | Hecho | §2 |
| F1.4 | La 03 y la 04 agrupan igual | Hecho | `test_la_03_y_la_04_no_cambian` y los tests de la 04, sin cambios |
| F1.5 | El docstring: v9 con `--sesion 03`, v10 con `--sesion 04` | Hecho | §2 |
| F1.6 | El test de `SESION_EN_CURSO` se parte | Hecho | §2 |
| F1.7 | Tests rotos en los dos sentidos, con las dos salidas | Hecho | §2, `romper_tests.py` |
| F1.8 | Documentos falsos corregidos | Parcial, declarado | §1.c: el docstring, corregido; `docs/sesion-5/PREGUNTAS.md:22-24` y tres recuadros (revisor, b1) no se tocan porque el encargo lo prohíbe: §2 y la propuesta de §6 |
| F2 | La entrada del 2026-10-21 en DECISIONES-DE-PROCESO.md, con las dos frases y sus orígenes verificados | Hecho, con un matiz | §3 (la frase de SESGO-H4-COLOR va sobre el cierre de corrida-construccion) |
| NC | Lo que no cambia | Hecho | §5 |
| C | Informe, `make check`, `fix/hoja-sesion-05` con solo el fallo de `state check`, revisor | Hecho | §8; el revisor, pegado en §9, y sus hallazgos, en §10 |

**Desviaciones declaradas:**
1. Un test de más, `test_la_filtrada_de_la_05_agrupa_con_su_hoja`, que el encargo no pide (§2).
2. El test de los textos de la 05 no copia los títulos: los LEE de `docs/sesion-5/PREGUNTAS.md`.
   Así, si la hoja cambia (un recuadro nuevo) y el guion no, falla.
3. El contrato se amplió a `docs/validation/anexos/HOJA-SESION-05/`, por el guion de las roturas.

## 8 · `make check` y CI de Linux

- `make check` del commit aab4df3 (fases 1 y 2): exit 0, `2734 passed in 922.37s`, ningún `failed`,
  `SELLO: make check en verde sobre el arbol fd941e16279f0909424082ff0c2264d1cb6b5db0`,
  `PICO DE MEMORIA de make check: 297 MiB en `test` (suma de sus procesos, memoria comprometida, Windows; el mayor proceso, 287 MiB)`.
- CI de Linux: `git push origin trabajo/hoja-sesion-05:refs/heads/fix/hoja-sesion-05`. **Run
  39738216803** sobre `aab4df336da311abb8f1b95f3f6128e5f81ed74e`: `1 failed, 2723 passed, 10
  skipped`; el único fallo es el esperado, `FAILED tests/unit/test_cli.py::test_state_check_ok_on_real_repo`
  (PROJECT_STATE declara `trabajo/hoja-sesion-05` y la rama es `fix/hoja-sesion-05`). Consultada
  con `gh run list --branch fix/hoja-sesion-05` y `gh run view 39738216803 --log-failed`, a mano,
  una vez cada uno, tras una espera en segundo plano sin consulta. Una primera llamada,
  `gh run list --commit aab4df3`, antes de la espera, dio `[]`: el run aún no existía.

## 9 · Informe del revisor, entero

El subagente `revisor` (opus), 2026-10-22, sobre aab4df3 más el informe estadiado (§8 y el
Estado). Pegado tal cual (sin la sangría que añade el entorno); no cita ningún tramo no citable.

> ## Informe del revisor · trabajo/hoja-sesion-05 · 2026-10-22
>
> Base `main` 7e6dec2. Commits adcc76b y aab4df3, más el informe con un cambio estadiado (§8 y el Estado).
>
> ### Eje (a) · Reglas de la casa
> Resumen: 0 bloquea, 0 importa, 0 menor. **Sin hallazgos.**
>
> Lo que comprobé:
> 1. **Contrato.** `uv run python scripts/contrato_rama.py` dice: `CONTRATO: 9 ficheros dentro del contrato de trabajo/hoja-sesion-05 (riesgo medio, artefacto docs/validation/HOJA-SESION-05.md, tramo 'R4', 3 comprobaciones para el revisor)` y sale con exit=0.
>    - `uv run pytest tests/unit/test_transcribir_sesion.py`: `112 passed in 38.16s`.
>    - `make check` no lo ejecuté. `make-check.log` (fechado a las 02:05 del 22-10) trae `2734 passed in 922.37s`, `SELLO: make check en verde sobre el arbol fd941e16279f0909424082ff0c2264d1cb6b5db0` y `PICO DE MEMORIA … 297 MiB … el mayor proceso, 287 MiB`.
>    - `git rev-parse aab4df3^{tree}` da `fd941e16…`: el sello es el árbol de aab4df3. El de adcc76b es `e01e52ea…`, que es el que cita §0.
> 2. **Trailers `Fuente:`.** No hacen falta: ningún commit toca `knowledge/spec/` ni `knowledge/cases/`.
> 3. **Holdout y material.** No se toca nada de holdout, transcripciones, fotogramas ni libros. La única lectura es `docs/sesion-5/PREGUNTAS.md`, un documento nuestro. No hace falta ninguna fila en HOLDOUT-EXPOSICIONES.
> 4. **Regímenes de cambio.** El diff no toca evidence, feedback, manifests ni corpus. `docs/state/HISTORIA.md` tiene solo líneas añadidas (`git diff --numstat`: `167 0`), con `# Archivo 42 · PROJECT_STATE.md de main en 7e6dec2`.
> 5. **Ambigüedades y ADR.** Ninguno cambia.
> 6. **Informes cerrados.** Ninguno cambia: solo es nuevo `HOJA-SESION-05.md` y su anexo.
> 7. **Las tres guardias de una `cita`.** No se aplica.
> 8. **Cifras de negocio en el motor.** No hay: el cambio es en `scripts/` y en tests.
> 9. **`PROJECT_STATE.md`.** Cambia lo de abrir-rama, el recuento de 1642 a 1647 (son 5 funciones `def test_` nuevas) y Archivo 41 a 42.
> 10. **El informe.** Existe y acaba en «Rama lista para revisión, NO cerrada».
> 11. **Citas del informe (más de tres) contra su fuente, todas exactas:**
>     - `docs/encargos/trabajo-previa-sesion-5.md:13`
>     - `PREVIA-SESION-5.md:28`
>     - `EA-CONEXION.md:1076` (fila 3g) y `:1077` (fila 0/7)
>     - `SESGO-H4-COLOR.md:1269` (§10) y `:1301` (con el matiz de corrida-construccion, bien declarado)
>     - `PROJECT_STATE.md:104` (la línea de Technical Debt)
>     - HISTORIA, registro de cierre de ea-conexion, punto 3 (`HISTORIA.md:11139-11141`)
> 12. **Evidencia nueva.** No hay.
>
> ### Eje (b) · Encargo
> Resumen: 0 bloquea, 1 importa, 3 menor. Requisitos: 20 hechos, 2 parciales, 0 no hechos.
>
> | # | Requisito | Estado | Evidencia |
> |---|---|---|---|
> | 1 | Base 7e6dec2, tag sobre e4563db, ninguna otra rama | Hecho | informe §0; mensaje de adcc76b |
> | 2 | Abrir con abrir-rama: encargo tal cual con fecha, contrato y Archivo en HISTORIA | Hecho | `docs/encargos/trabajo-hoja-sesion-05.md:3`; `contrato.yaml`; HISTORIA Archivo 42 |
> | 3 | R1 · guardia o clasificador: PARADA salvo la forma propuesta | Hecho (declarado) | informe:198, «ninguna negativa» |
> | 4 | R2 · CI sin guion ni bucle | Hecho (declarado) | informe §8:230-232 |
> | 5 | F0.1 · usos de los códigos y de `--sesion` | Hecho | `git show main:scripts/transcribir_sesion.py`: 124, 163, 168, 195, 203, 307, 344, 366, 607-608, 631, 654-656, todas como dice §1.a |
> | 6 | F0.2 · tests que fijan la 04 o la sesión en curso | Hecho | main `test_transcribir_sesion.py:398`, `:403 assert m.SESION_EN_CURSO == "04"`, 408, 419, 438 y 442; ningún test llama a `main()` sin `--sesion` salvo `:293` (solo `--audio`) |
> | 7 | F0.3 · skill, SESION-DE-PREGUNTAS y MIRAR-EL-MATERIAL | Hecho | `SKILL.md:20,69-70` siguen ciertos para la sesión 5. `SESION-DE-PREGUNTAS.md:69` es de `hoja_preguntas` y `:157` de `feedback new --sesion`; MIRAR-EL-MATERIAL no los nombra |
> | 8 | F1.1 · `ORDEN_SESION_05` S-1..S-25 con su comentario; el orden de PREGUNTAS es el numérico | Hecho | `transcribir_sesion.py:121-131`; Grep `^\*\*S-` en PREGUNTAS.md da las líneas 74 a 779, crecientes |
> | 9 | F1.2 · textos de la 05: título sin «S-n. », sin lo de detrás de la negrita, S-1 en dos líneas, minúscula; S-7 y S-12 del recuadro; S-13 y S-15 con el suyo | Hecho | Los 25 comparados uno a uno con PREGUNTAS.md (74-75, 94, 120, …, 779). S-7 viene de `:248` y S-12 de `:417`. Los recuadros de S-13 (`:479-485`) y S-15 (`:538-546`) no traen «Título», y el guion conserva `:487` y `:548` |
> | 10 | F1.3 · `HOJAS["05"]` y `SESION_EN_CURSO = "05"` | Hecho | `transcribir_sesion.py:212,214` |
> | 11 | F1.4 · la 03 y la 04 agrupan igual; 02, 03 y 04 sin cambios | Hecho | `git diff main...HEAD -- scripts/transcribir_sesion.py` solo añade; ni una línea de las hojas ni de los textos 02, 03 y 04 cambia |
> | 12 | F1.5 · docstring: v9 con `--sesion 03`, v10 con `--sesion 04`, ningún ejemplo de re-filtrada sin `--sesion` | Hecho | `transcribir_sesion.py:47-54`. El único `--solo-filtrar` del docstring lleva `--sesion 04` (`:49-50`) |
> | 13 | F1.6 · se parte el test de `SESION_EN_CURSO` | Hecho | `test_transcribir_sesion.py:399-406` sin la aserción; `:481-484` es `test_la_sesion_en_curso_es_la_05` |
> | 14 | F1.7 · cuatro tests rotos en los dos sentidos, con sus salidas | Hecho | `PYTHONUTF8=1 uv run python docs/validation/anexos/HOJA-SESION-05/romper_tests.py .` reproduce línea a línea la salida del informe (`:120-136`), acaba en «todo como se espera» y sale con exit=0 |
> | 15 | F1.8 · un documento que queda falso se corrige en la rama | Parcial | hallazgo b1 |
> | 16 | F2 · entrada del 2026-10-21 en «Decisions and Rationale», con el formato de la sección y «nace aquí» | Hecho | `DECISIONES-DE-PROCESO.md:28`: formato fecha · decisión · Problema · Alternativas · Estado: ACTIVE, como las del 2026-09-04; «NACE AQUI… no viene de la mudanza» |
> | 17 | F2 · las dos frases literales, con sus orígenes verificados | Hecho | Las dos frases coinciden carácter a carácter con el encargo (`:42-43`). Orígenes comprobados en el eje (a), punto 11 |
> | 18 | F2 · PARADA si un test exige otro sitio | Hecho | informe §3:163-165; sin PARADA |
> | 19 | Lo que NO cambia (motor, spec, ambigüedades, feedback, casos, corpus, fuentes.yaml, cuarentena, PREGUNTAS.md) | Hecho | `git diff --stat main...HEAD`: 9 ficheros, ninguno de esas rutas; `contrato_rama.py` en verde con `docs/sesion-5/` protegido |
> | 20 | Informe y make check sellado | Hecho | eje (a), punto 1 (aab4df3). El cambio estadiado del informe todavía no tiene sello propio |
> | 21 | Push a `fix/hoja-sesion-05` y CI de Linux con solo el fallo de state check | Hecho (en parte por declaración) | `gh run view 39738216803 --json conclusion,headSha` da `{"conclusion":"failure","headSha":"aab4df336da311abb8f1b95f3f6128e5f81ed74e"}`: el run es sobre aab4df3 y falla. Que el único fallo sea `test_state_check_ok_on_real_repo` lo dice el informe (§8:227-229); no lo comprobé (ver abajo) |
> | 22 | El revisor, lanzado con el informe terminado, pegado al final | Parcial | pendiente de pegar este informe (informe:237, «El revisor, abajo») |
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | b1 | importa | **Un documento dice que los textos de la 05 entran con la ingesta, y ahora entran en esta rama.** El informe lo da por cierto y no lo declara: «Ningún documento de la fase 0 quedó falso, salvo el docstring» (informe:144) y §1.c. `docs/sesion-5/PREGUNTAS.md:22-24` dice: «Los textos de estos códigos entran en ese script con la ingesta de la sesión (`CODIGOS_DE_SESION_TEXTO["05"]`), no aquí». Lo repiten sus recuadros en `:246`, `:415` y `:483` («a `CODIGOS_DE_SESION_TEXTO["05"]` con la ingesta»). Tras aab4df3 entran en esta rama, antes de la ingesta. El Grep de la fase 0 buscaba `CODIGOS_DE_SESION_TEXTO`, pero no sobre `docs/sesion-5/`. PREGUNTAS.md no se toca por el encargo (`:17`), así que lo que tocaba era declararlo en el informe o subirlo al consultor (PARADA con propuesta, `:28`), no callarlo. | `git grep -n 'CODIGOS_DE_SESION_TEXTO\["05"\]'` da `docs/sesion-5/PREGUNTAS.md:23`, `:246`, `:415` y `:483`. También `PREVIA-SESION-5.md:83` y `:482`, informe cerrado que cuenta lo que entonces decía PREGUNTAS |
> | b2 | menor | **La rotura del test de los textos de la 05 solo prueba el lado del guion.** El informe dice que «si la hoja o el guion cambian uno sin el otro, falla» (informe:106-107; desviación 2, :217-218). Las dos mutaciones del anexo cambian el guion. Ninguna cambia el texto leído de PREGUNTAS.md (por ejemplo, sustituyendo `PREGUNTAS_05` en memoria). Por construcción la igualdad falla en los dos casos, pero ese lado no está demostrado. | `romper_tests.py:77-80` |
> | b3 | menor | **La rotura de `test_la_03_y_la_04_no_cambian` cae en la identidad, no en el agrupado.** La mutación «la hoja 04 con S-1 y S-2 cambiados» sustituye `HOJAS["04"]` por una tupla nueva y cae en la comprobación de identidad (`:498 assert m.HOJAS["04"] is m.ORDEN_SESION_04`). Ninguna mutación llega a la aserción del orden (`:499`) ni al agrupado de la filtrada (`:503-506`), que es lo que el encargo pide fijar («agrupando exactamente igual»). | `romper_tests.py:70,95-96`; salida «FALLA en test_transcribir_sesion.py:498» |
> | b4 | menor | **La tabla del informe marca el revisor como «Hecho» antes de pegarlo.** La fila C de §7 dice «Hecho» e incluye al revisor, cuyo informe aún no está pegado. | informe:213 |
>
> ### Lo que no pude comprobar
> - **El sello del árbol estadiado.** `git write-tree` escribe en la base de objetos y no lo ejecuté. El cambio estadiado (§8 y el Estado del informe) no está cubierto por el sello `fd941e16…`, que es el árbol de aab4df3. Su commit necesitará otro `make check`.
> - **Que el único fallo del run 39738216803 sea `test_state_check_ok_on_real_repo`.** Hice la única consulta permitida (`--json conclusion,headSha`): da `failure` sobre aab4df3. El detalle del fallo descansa en lo que dice el informe (§8).
> - **La primera pasada de pytest.** Un segundo pytest encadenado en el mismo comando lo negó la guardia (regla de `trabajo/guion-mismo-comando`). Lo relancé solo, en su propia llamada, y dio `112 passed`.
> - **`ruff check` y `ruff format --check`.** No los relancé; los cubre el `make check` de aab4df3.
> - **R1 y R2** (ninguna negativa de la guardia en la rama; la CI sin bucle). Solo tengo la declaración del informe.
>
> ### Comandos ejecutados
> 1. `git branch --show-current && git merge-base main HEAD && git log --format='%h %s' main..HEAD && git diff --stat main...HEAD && git status --short && git diff --cached --stat`
> 2. Read de `docs/encargos/trabajo-hoja-sesion-05.md`, `contrato.yaml` y `docs/validation/HOJA-SESION-05.md`
> 3. `git diff main...HEAD -- scripts/transcribir_sesion.py tests/unit/test_transcribir_sesion.py docs/runbooks/DECISIONES-DE-PROCESO.md PROJECT_STATE.md`
> 4. Grep `^\*\*S-[0-9]+\.|Título:|^> .*2026-10-21` en `docs/sesion-5/PREGUNTAS.md`
> 5. `uv run python scripts/contrato_rama.py`
> 6. `uv run pytest -q tests/unit/test_transcribir_sesion.py`
> 7. `PYTHONUTF8=1 uv run python docs/validation/anexos/HOJA-SESION-05/romper_tests.py .`
> 8. `gh run view 39738216803 --json conclusion,headSha` (una vez)
> 9. Un pytest con `echo exit` y un segundo pytest en el mismo comando: lo negó la guardia
> 10. `uv run pytest -q tests/unit/test_transcribir_sesion.py -p no:cacheprovider | grep …` y `uv run pytest tests/unit/test_transcribir_sesion.py -p no:cacheprovider -rN | tail -3`
> 11. Read de `romper_tests.py`
> 12. `git diff --cached`; `git grep -n -e solo-filtrar -e SESION_EN_CURSO -e "sesion en curso" -- scripts .claude/skills docs/runbooks CLAUDE.md`
> 13. `git grep -n transcribir_sesion -- .claude docs/runbooks CLAUDE.md docs/plan PROJECT_STATE.md docs/HANDOFF.md docs/sesion-5`
> 14. Read de `SKILL.md:14-78`, `PREGUNTAS.md:15-29`, `:239-250`, `:479-487` y `:538-547`
> 15. `git grep -n` de `CODIGOS_DE_SESION_TEXTO["05"]`, `ORDEN_SESION_05` y `HOJAS["05"]` fuera de los ficheros de la rama
> 16. `git show main:scripts/transcribir_sesion.py | grep -n …` y `git show main:tests/unit/test_transcribir_sesion.py | grep -n …`; `git grep -n SESION_EN_CURSO -- tests src`
> 17. Grep de `main(|parse_args|--sesion|procesar(` en el test
> 18. `sed -n` de `trabajo-previa-sesion-5.md:13`, `PREVIA-SESION-5.md:26-29`, `EA-CONEXION.md:1074-1078`, `SESGO-H4-COLOR.md:1269,1299-1302` y `PROJECT_STATE.md:104`
> 19. `grep` de los encabezados de PREVIA, de ea-conexion en HISTORIA y de su fila en ERRORES-RECURRENTES; Read de `HISTORIA.md:11133-11144`
> 20. `git diff main...HEAD --numstat -- docs/state/HISTORIA.md` y cabecera del diff
> 21. `ls -la make-check.log`; `grep` de SELLO, PICO, passed y failed; `git log -1 --format='%h %ci' aab4df3`
> 22. `git rev-parse aab4df3^{tree} adcc76b^{tree}`; `git log --format='%h%n%B---' main..HEAD`
> 23. `sed -n '69p;157p' docs/runbooks/SESION-DE-PREGUNTAS.md`; grep de «sesión en curso» y `--sesion` en MIRAR-EL-MATERIAL y SESION-DE-PREGUNTAS
> 24. `git grep -n -i -e "con la ingesta" -e "hoja 05" -e ORDEN_SESION_NN -- docs/runbooks .claude/skills docs/plan PROJECT_STATE.md`

## 10 · Lo que se hizo con los hallazgos del revisor

| # | Gravedad | Qué se hizo |
|---|---|---|
| b1 | importa | **Declarado, sin tocar PREGUNTAS.md**, que el encargo prohíbe tocar: §2 dice que `docs/sesion-5/PREGUNTAS.md:22-24` y los recuadros de S-7, S-12 y S-13 (`:246`, `:415`, `:483`) quedan desfasados («con la ingesta»), §7 (F1.8) pasa a «Parcial, declarado», y §6 propone al consultor un recuadro en la orden de cierre, con su texto. La fase 0 no buscó en `docs/sesion-5/`: es lo que se le escapó. |
| b2 | menor | Arreglado: `romper_tests.py` tiene una mutación del lado de la hoja (cambia en memoria lo que el test lee de PREGUNTAS.md, el título de S-9, sin escribir el fichero), y falla en `:478` (§2). |
| b3 | menor | Arreglado: dos mutaciones reordenan la hoja 04 en su sitio (`ORDEN_SESION_04` y `HOJAS["04"]` a la vez) y caen en el orden (`:499`); una tercera deja las hojas intactas y rompe solo el agrupado (`orden_de_preguntas` sin mirar la hoja) y cae en la filtrada de la 04 (`:505`) (§2). |
| b4 | menor | Arreglado: la fila C de §7 remite a §9 y §10. |

Lo que el revisor no pudo comprobar del run 39738216803 (que el único fallo sea el esperado) lo
dice §8 con su salida: `gh run view 39738216803 --log-failed`, «1 failed, 2723 passed, 10 skipped»
y `FAILED tests/unit/test_cli.py::test_state_check_ok_on_real_repo`. Tras los arreglos, el último
commit lleva su propio `make check` y su propia CI (§11).

## 11 · El último commit, con los arreglos del revisor

Su `make check` y su CI de Linux por `fix/hoja-sesion-05` no pueden ir dentro del árbol que
sellan: el resultado del `make check` va en el mensaje de su commit, y el número del run de la CI,
en el mensaje final a Aleks. La CI se consulta igual que en §8: una espera en segundo plano sin
consulta y después un `gh run list` y un `gh run view` sueltos.

## Estado

Rama lista para revisión, NO cerrada. Fases 0, 1 y 2 hechas (§7), con tres desviaciones declaradas
y un documento desfasado que el encargo no deja tocar (b1: `docs/sesion-5/PREGUNTAS.md:22-24`, con
la propuesta de §6). CI de Linux de aab4df3 con solo el fallo esperado (run 39738216803). El
revisor (§9) no encontró nada que bloquee; su «importa» está declarado y sus tres «menor»,
arreglados (§10).
