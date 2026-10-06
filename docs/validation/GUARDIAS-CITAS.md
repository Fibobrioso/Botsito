# Guardias de citas: G1 (evidencia supersedida) y G2 (Fuente: en los tramos)

Rama `trabajo/guardias-citas`, abierta el 2026-10-05 desde `main` en `442a948`. Ese es el commit de
estado de `stable/F37a-respuestas-ftmo`, y su CI de `main` (run 37411332514) estaba en verde,
comprobado antes de abrir. Encargo: `docs/encargos/trabajo-guardias-citas.md`. Paga dos líneas de
Technical Debt de `PROJECT_STATE.md`.

**Estado: PARADA en la fase 0, sin código.** El recuento de G1 no es cero (§0.a). Además, la
fase 0 deja tres preguntas para el consultor (§1).

## 0. Fase 0: inventario sin tocar nada

Las dos medidas son guiones de esta rama y su salida va al lado:
- `docs/validation/anexos/GUARDIAS-CITAS/medir_citas_supersedidas.py` (`-SALIDA.txt`). Solo carga los
  ids y el campo `supersede` de la evidencia (`cargar_evidencia`). No imprime ni una cita ni un texto.
- `docs/validation/anexos/GUARDIAS-CITAS/medir_tramos_sin_fuente.py` (`-SALIDA.txt`). Solo lee
  metadatos de git: sha, fecha, padres, asunto y los ids del trailer. No lee el contenido de
  `tramos_no_citables.yaml`.

### 0.a G1: qué es un supersedido, quién cita ev-* y el recuento actual

**Cómo se sabe hoy que un ítem está supersedido.** Por el campo `supersede` del ítem NUEVO, en
`knowledge/evidence/<video>/<id>.yaml`. Un ítem X está supersedido si otro ítem lleva
`supersede: X`. El campo es `EvidenceItem.supersede` (`src/botsito/evidence/modelo.py:137`):
- su formato se valida al cargar (`:236`);
- `validar_contra_manifiesto` comprueba que exista, que no se apunte a sí mismo, que sea del mismo
  tema y que no haya ciclos (`:355-364`).

Ya lo leen dos funciones:
- `botsito.comun.documentos.activos` (`src/botsito/comun/documentos.py:103-106`);
- `ventanas_no_citables` de `knowledge validate` (`src/botsito/validation/knowledge.py:116`).

**La evidencia solo la supersede otra evidencia.** Los 49 `supersede:` de `knowledge/feedback/`
apuntan todos a `fb-*`.

**La guardia que ya existe y no cubre esto.** `comprobar_citas_revocadas`
(`src/botsito/spec/modelo.py:859-887`) mira reglas, glosario y vocabulario, y
`knowledge validate` (`:1016-1035`) mira la fuente de cada parámetro. Pero las dos solo conocen los
registros de FEEDBACK revocados: `revocados` se construye con `registros_fb` (`knowledge.py:440` y
`:1021`). Nada mira la evidencia supersedida, y nada mira el campo `evidencia:` de las ambigüedades.
Ese es el hueco que nombra la línea de Technical Debt.

**Supersedidos hoy.** Hay 13 de 503 ítems, cada uno con su sustituto, y ninguno forma cadena: ningún
sustituto está supersedido a su vez. La lista está en la salida del primer guion.

**Ficheros versionados que nombran algún id ev-\***, contando líneas con un id:

| Fichero | Líneas con ev-* |
|---|---|
| `knowledge/spec/ambiguedades.yaml` | 210 |
| `knowledge/spec/strategy_spec.yaml` | 41 |
| `knowledge/spec/parametros.yaml` | 27 |
| `knowledge/spec/glossary.yaml` | 5 |
| `knowledge/spec/README.md`, `spec_manifest.yaml` | 0 |
| `docs/spec/reglas.md` (generado) | 28 |
| `docs/spec/parametros.md` (generado) | 22 |
| `docs/spec/glosario.md` (generado) | 5 |
| `docs/spec/ambiguedades.md` (generado) | 0: la tabla generada no lleva la evidencia |

Fuera de la spec también nombran ids ev-*:
- `knowledge/evidence/`, `knowledge/feedback/`, `knowledge/_proposals/` y `knowledge/cases/kit/`;
- `knowledge/corpus/tramos_no_citables.yaml`;
- `docs/validation/` y sus anexos, `docs/adr/`, `docs/encargos/`, `docs/state/HISTORIA.md` y
  `docs/HANDOFF.md`;
- los tests.

El primer guion da el recuento por fichero.

**Recuento ACTUAL de citas a supersedidos en la spec: 9 líneas, 7 de ellas en la fuente.**

| # | Fichero:línea | Id supersedido | Sustituto | Dónde está |
|---|---|---|---|---|
| 1 | `knowledge/spec/ambiguedades.yaml:159` | `ev-v1-000448-346d6d90` | `ev-v6-013508-b4c88d87` | A-10 (RESUELTA), campo `evidencia:` |
| 2 | `knowledge/spec/ambiguedades.yaml:160` | `ev-v2-003142-beb4ad3c` | `ev-v6-021939-1c7cad28` | A-10 (RESUELTA), campo `evidencia:` |
| 3 | `knowledge/spec/ambiguedades.yaml:179` | `ev-v4-001207-0c4ffd4b` | `ev-v6-021939-b430a110` | A-11 (RESUELTA), campo `evidencia:` |
| 4 | `knowledge/spec/ambiguedades.yaml:363` | `ev-v4-011951-5fb49e03` | `ev-v6-014702-2d7096db` | A-18 (ABIERTA), campo `evidencia:` |
| 5 | `knowledge/spec/ambiguedades.yaml:1100` | `ev-v3-002714-742f2589` | `ev-v6-000732-f9c41d5e` | A-41, comentario YAML: «está supersedido por» su sustituto, en la línea siguiente |
| 6 | `knowledge/spec/strategy_spec.yaml:1620` | `ev-v4-011351-74b8bb39` | `ev-v6-000732-f7189541` | RN-034, `notas`: «los sustituyen» sus sustitutos, en la línea siguiente |
| 7 | `knowledge/spec/strategy_spec.yaml:1620` | `ev-v1-000959-b82650ad` | `ev-v6-000732-5945fd87` | la misma frase de RN-034 |
| 8-9 | `docs/spec/reglas.md:1208` | los dos de RN-034 | — | la copia generada de las `notas` de RN-034 |

Las filas 1 a 4 son CITAS: un id en el campo `evidencia:` de la ambigüedad. Los cuatro sustitutos
entraron el 2026-09-12 en `2003e61` («fix(evidence,spec): la deuda de conocimiento, ...»), y las
ambigüedades siguieron citando el ítem viejo desde entonces.

Las filas 5 a 9 son MENCIONES en prosa que cuentan la sustitución y nombran al sustituto.
`parametros.yaml` y `glossary.yaml` no citan ningún supersedido, y tampoco lo hace el campo `cita`
de ninguna regla.

**El recuento no es cero: PARA** (§1). Ninguna se toca sin la decisión del consultor.

### 0.b G1: qué queda fuera, y la condición en positivo

**Propuesta: se vigila todo fichero VERSIONADO bajo `knowledge/spec/`** (`git ls-files
knowledge/spec/`), y la lista de excluidos es una constante del código, visible y hoy VACÍA:
- un fichero nuevo bajo `knowledge/spec/` entra solo, sin que nadie se acuerde de añadirlo;
- `README.md` y `spec_manifest.yaml` no nombran ningún ev-*, así que no hace falta excluirlos;
- un test vigila que la lista de excluidos solo cambie a la vista.

**Fuera, y por qué:**
- `docs/spec/`: es GENERADO desde `knowledge/spec/`, y `tests/contract/test_spec_docs_generados.py`
  falla si no reproduce la fuente. Vigilar los dos repetiría cada error y señalaría una línea que
  nadie edita a mano.
- `knowledge/evidence/`: la cita de un id viejo es el propio `supersede` del ítem nuevo, y además es
  INMUTABLE.
- `knowledge/feedback/`: es SOLO AÑADIR; un registro de la sesión 1 (`fb-...-9deda56d`) nombra un
  supersedido y no se puede editar.
- `knowledge/_proposals/`: propuestas históricas, ya aceptadas o descartadas.
- `knowledge/cases/kit/`: el cuestionario y el contexto de la sesión 1 y `vistos.yaml` son registro
  de lo que se preguntó entonces.
- `knowledge/corpus/tramos_no_citables.yaml`: el motivo de un tramo nombra un id; el encargo prohíbe
  tocar su contenido.
- `docs/validation/`, `docs/state/HISTORIA.md`, `docs/encargos/`, `docs/adr/`, `docs/plan/`,
  `docs/HANDOFF.md`, los anexos y los tests: citan ids viejos legítimamente, como historia o como
  fixture.

**Lo que la condición NO decide sola** (pregunta 2 del §1): si dentro de un fichero vigilado cuenta
toda aparición del id o solo las CITAS. Las menciones de las filas 5 a 7 ya nombran al sustituto en
la línea siguiente, y la 6 y la 7 están en `strategy_spec.yaml`, que el encargo dice que no cambia.

### 0.c G2: cómo se exige hoy Fuente:, los commits y el ancla

**Cómo se exige hoy:**
- La función es `commits_sin_fuente` (`src/botsito/comun/historial.py:288-325`).
- Mira las rutas `DIRECTORIOS_CON_FUENTE = ("knowledge/spec/", "knowledge/cases/")` (`:33`).
- Exige desde `ANCLA_FUENTE = ("stable/F06", "b6b82f2f...")` (`:37`). Ese es el sha que manda: si el
  tag existe y no coincide, es error.
- Solo cuenta el CUERPO del mensaje (`fuentes_de_mensaje`, `:276-285`). Cada id tiene que tener
  formato `ev-*`, `fb-*` o `ADR-NNNN` y existir.
- La corren dos sitios:
  - `knowledge validate` (`src/botsito/validation/knowledge.py:874-889`, a través de
    `Historial.commits_sin_fuente`, `:293`), y por tanto `make check`;
  - el test de contrato `test_repositorio_real` (`tests/contract/test_feedback_history.py:170-180`),
    que FALLA si el ancla no se resuelve.
- Ningún hook mira el trailer: `grep Fuente scripts/git-hooks/` sale vacío.

**Commits que tocan `knowledge/corpus/tramos_no_citables.yaml`:** 10 sin contar los merges. En el
`git log` sin `-m`, el que usa la guardia de spec y cases, salen:

| Sha | Fecha | Fuente: |
|---|---|---|
| `809117b` | 2026-10-05 15:30 | `ev-v9-003457-3e28e325` |
| `f50b680` | 2026-10-04 22:20 | `ADR-0021` |
| `7120217` | 2026-10-04 18:36 | `ADR-0021, ADR-0038` |
| `c489685` | 2026-10-04 13:22 | **SIN Fuente:** |
| `cfec50b` | 2026-10-04 12:29 | **SIN Fuente:** |
| `f443eee` | 2026-10-01 22:06 | **`docs/validation/CUARENTENA-POR-DEFECTO.md`: no es un id** (`commits_sin_fuente` lo da como «fuente con formato invalido») |
| `b9e7e8a` | 2026-09-29 19:10 | `ev-v9-010753-063c8cb7, ev-v9-010809-68e4ea44, ADR-0021, ADR-0038` |
| `0e3ca88` | 2026-09-29 18:18 | `ADR-0011, ADR-0021, ADR-0038` |
| `3718889` | 2026-09-27 12:56 | `ADR-0038` |
| `ed25392` | 2026-09-09 16:50 | `ADR-0009` |

Hay **2 sin Fuente:** y **1 con una Fuente: que no es un id**.

Con `git log -m --full-history` salen además 8 merges, y ninguno lleva Fuente: (`f8b291c`,
`5e486dc`, `44f461d`, `eec79a0`, `1591737`, `00fcced`, `408b609` y `1475956`). La guardia de spec y
cases no mira los merges (`git log` sin `-m`), y lo que se propone es lo mismo para G2. Su límite es
el mismo: un cambio ESCONDIDO dentro de un merge no se ve. Las guardias de inmutabilidad sí miran con
`-m`, porque comparan blobs y no trailers.

**El ancla propuesta es `c489685`, el último commit sin Fuente:,** fijada como sha completo en una
constante, sin tag y sin fecha:
- `cfec50b` y `f443eee` son ancestros suyos (`git merge-base --is-ancestor`), así que el rango
  `c489685..HEAD` deja fuera justo los tres malos;
- y sigue vigilando los tres posteriores: `7120217`, `f50b680` y `809117b`;
- medido: `commits_sin_fuente(repo, "c489685", rutas=(tramos,))` da `[]`, y con `desde=None` da los
  tres de arriba.

La alternativa es anclar en `442a948` (`main` al abrir), que también da `[]`, pero deja sin vigilar
los tres commits buenos.

El test FALLA, y no se salta, si el ancla no se resuelve como commit, igual que
`test_repositorio_real` con `ANCLA_FUENTE`.

**Los commits anteriores al ancla, que no se tocan:** `c489685`, `cfec50b` y `f443eee` (arriba),
más `b9e7e8a`, `0e3ca88`, `3718889` y `ed25392`, que sí llevan Fuente:.

**Cómo se reutiliza:** `commits_sin_fuente` ya acepta `rutas`. Lo único que no encaja es su mensaje,
que dice «toca spec/cases» (`historial.py:318`). Ver la pregunta 3 del §1.

### 0.d Lo que depende de la plataforma

- **Codificación y `core.quotepath`:** `_git` ya lanza `git -c core.quotepath=false` y decodifica
  UTF-8 con `errors="replace"` (`historial.py:51-60`). La ruta es ASCII y toda en minúsculas.
- **Finales de línea:** los mensajes se leen con `%B`, y el trailer con `^Fuente:\s*(.+?)\s*$` en
  modo multilínea. `\s*` absorbe un `\r` final. Ninguno de los 10 mensajes lleva `\r` (medido con
  `git log --no-walk --format=%B ... | grep -c $'\r'`: 0).
- **Mayúsculas en la ruta:** en esta máquina `core.ignorecase=true`. El pathspec de `git log` distingue
  mayúsculas igual en Windows y en Linux, y la ruta se escribe literal.
- **Clon superficial en la CI:**
  - `.github/workflows/ci.yml:22` hace `fetch-depth: 0`;
  - `historial_evaluable` detecta un clon superficial (`historial.py:139-141`), y entonces
    `commits_sin_fuente` devuelve `None`;
  - el test tiene que FALLAR con `None` si hay git, no saltarse.
  - El ancla es un sha, así que no necesita tags.
- **Repos temporales en los tests:** necesitan identidad y `core.autocrlf=false` en el propio repo
  temporal, como `_repo` de `tests/contract/test_feedback_history.py:30-34`. Nada se escribe en el
  repositorio real.
- Aun así, G2 lee la historia y la rama se empujará como `fix/guardias-citas` para la CI de Linux,
  como pide el encargo.

## 1. Para el consultor: la PARADA

**1. Las cuatro citas del campo `evidencia:` (filas 1 a 4 del §0.a): ¿se sustituyen o se mantienen?**

| Ambigüedad | Estado | Cita hoy | Sustituto |
|---|---|---|---|
| A-10 | RESUELTA | `ev-v1-000448-346d6d90` | `ev-v6-013508-b4c88d87` |
| A-10 | RESUELTA | `ev-v2-003142-beb4ad3c` | `ev-v6-021939-1c7cad28` |
| A-11 | RESUELTA | `ev-v4-001207-0c4ffd4b` | `ev-v6-021939-b430a110` |
| A-18 | ABIERTA | `ev-v4-011951-5fb49e03` | `ev-v6-014702-2d7096db` |

- **Si se sustituyen:**
  - el contrato se amplía en un commit con `knowledge/spec/ambiguedades.yaml` y `docs/spec/`;
  - el commit lleva `Fuente:` con los cuatro sustitutos;
  - se sigue `docs/runbooks/AMBIGUEDADES.md`, con `botsito spec docs --escribir` en el mismo commit;
  - ninguna se abre ni se cierra; solo cambia la lista `evidencia:`.
- **Si alguna se mantiene:** G1 necesita una excepción declarada, con id, ambigüedad y motivo, en una
  lista visible del código, y la guardia la comprueba. Si no, no pasaría.
- Ninguna de las dos cosas es de esta sesión.

**2. ¿G1 mira solo las CITAS o toda aparición del id?** La recomendación es la opción A.
- **A:**
  - en los ficheros que se conocen, G1 lee los CAMPOS de cita:
    - el `evidencia:` de cada ambigüedad;
    - la `cita` de reglas, glosario y vocabulario;
    - la `fuente.id` de cada parámetro;
  - en cualquier otro fichero bajo `knowledge/spec/`, hoy ninguno, lee el TEXTO entero, línea a
    línea, comentarios incluidos: un fichero nuevo entra sin campos conocidos y se niega por defecto;
  - las menciones en prosa de las filas 5 a 7 pasan;
  - no hay que tocar `strategy_spec.yaml`, que el encargo dice que no cambia.
- **B:**
  - G1 lee el texto de todo fichero vigilado;
  - las tres menciones de las filas 5 a 7 tendrían que declararse en su fichero, como hace
    `ids_citados`;
  - eso edita `strategy_spec.yaml` (las `notas` de RN-034) y `ambiguedades.yaml`, y la primera
    edición contradice el encargo.

**3. ¿Puede G2 reutilizar `commits_sin_fuente` añadiéndole un parámetro?** El parámetro sería
opcional y solo cambiaría el texto del mensaje: por defecto seguiría diciendo «toca spec/cases», y
para G2 diría «toca tramos_no_citables.yaml». Ninguna comprobación cambia, pero es código de una
guardia que ya existe (decisión 5).
- Sin permiso, G2 se escribe en su test con su propio bucle sobre `fuentes_de_mensaje`, y no toca
  nada de `historial.py`.

Con las tres respuestas, el resto de las decisiones se aplica tal cual:
- G1 en `knowledge validate`;
- G2 como test de contrato en la CI, con el ancla en un sha;
- los tests que las rompen en repos temporales;
- las dos líneas de Technical Debt a HISTORIA;
- `fix/guardias-citas` con su run de la CI de Linux.

## Estado

PARADA en la fase 0 (2026-10-05). Hay rama, encargo, contrato y el Archivo 18 de `PROJECT_STATE.md`
en HISTORIA, y las dos medidas con su salida. No hay código, y no se ha tocado `knowledge/` ni
`docs/spec/`. Las dos líneas de Technical Debt siguen en `PROJECT_STATE.md` hasta que existan las
guardias. Espera las tres respuestas del §1.
