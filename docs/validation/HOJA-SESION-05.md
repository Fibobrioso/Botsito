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
cada test tal cual y con dos mutaciones en memoria, una por sentido, deshaciendo cada una antes de
la siguiente; no escribe nada. Salida (`PYTHONUTF8=1 uv run python … .`):

```
test_la_hoja_05_tiene_los_25_codigos_con_su_texto: tal cual -> pasa
  roto (S-7 con el titulo del cuerpo y no el del recuadro) -> FALLA en test_transcribir_sesion.py:478: assert m.CODIGOS_DE_SESION_TEXTO["05"] == titulos
  roto (sin S-25 (la hoja de 24 codigos)) -> FALLA en test_transcribir_sesion.py:478: assert m.CODIGOS_DE_SESION_TEXTO["05"] == titulos
  de nuevo tal cual -> pasa
test_s25_vale_en_la_05_y_no_en_la_04: tal cual -> pasa
  roto (S-25 tambien en la 04) -> FALLA en test_transcribir_sesion.py:490: assert "S-25" not in v04
  roto (S-25 fuera de la 05) -> FALLA en test_transcribir_sesion.py:489: assert "S-25" in v05
  de nuevo tal cual -> pasa
test_la_03_y_la_04_no_cambian: tal cual -> pasa
  roto (la hoja 04 con S-1 y S-2 cambiados de sitio) -> FALLA en test_transcribir_sesion.py:498: assert m.HOJAS["04"] is m.ORDEN_SESION_04
  roto (el texto de S-1 de la 03 cambiado) -> FALLA en test_transcribir_sesion.py:501: assert m.CODIGOS_DE_SESION_TEXTO["03"]["S-1"] == "cómo decide el sesgo del día"
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
recuadros.

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
| F1.8 | Documentos falsos corregidos | Hecho | §1.c: solo el docstring |
| F2 | La entrada del 2026-10-21 en DECISIONES-DE-PROCESO.md, con las dos frases y sus orígenes verificados | Hecho, con un matiz | §3 (la frase de SESGO-H4-COLOR va sobre el cierre de corrida-construccion) |
| NC | Lo que no cambia | Hecho | §5 |
| C | Informe, `make check`, `fix/hoja-sesion-05` con solo el fallo de `state check`, revisor | Hecho | §8 y el revisor, abajo |

**Desviaciones declaradas:**
1. Un test de más, `test_la_filtrada_de_la_05_agrupa_con_su_hoja`, que el encargo no pide (§2).
2. El test de los textos de la 05 no copia los títulos: los LEE de `docs/sesion-5/PREGUNTAS.md`.
   Así, si la hoja cambia (un recuadro nuevo) y el guion no, falla.
3. El contrato se amplió a `docs/validation/anexos/HOJA-SESION-05/`, por el guion de las roturas.

## Estado

EN CURSO: falta el `make check` de la entrega, la CI de Linux y el revisor.
