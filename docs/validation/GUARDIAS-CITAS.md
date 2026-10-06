# Guardias de citas: G1 (evidencia supersedida) y G2 (Fuente: en los tramos)

Rama `trabajo/guardias-citas`, abierta el 2026-10-05 desde `main` en `442a948`. Ese es el commit de
estado de `stable/F37a-respuestas-ftmo`, y su CI de `main` (run 37411332514) estaba en verde,
comprobado antes de abrir. Encargo: `docs/encargos/trabajo-guardias-citas.md`. Paga dos líneas de
Technical Debt de `PROJECT_STATE.md`.

**Estado (2026-10-06): lista para revisión, NO cerrada. G1 y G2 hechas y conectadas; A-11 con UNA
excepción por par en G1 (§9.1); comprobaciones finales y CI de Linux en §10; revisor en §11.** El
informe sigue el orden en que pasó: fase 0 y primera parada (§0-§7), segunda (§8) y tercera (§9).
Lo de abajo es la historia de la primera parada:
- La fase 0 paró porque el recuento de G1 no era cero (§0.a), y el consultor respondió (§1.1).
- Tres de las cuatro citas pasan a su sustituto (§2).
- A-11 se para: su sustituto no sostiene lo que la ambigüedad cita.
- El comentario de A-41 no cumple la condición de G1: nombra a su sustituto en la línea de
  comentario siguiente, no en la misma.

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

### 1.1 La respuesta del consultor a la fase 0 (2026-10-05), copiada tal cual

Llegó el 2026-10-06, en un segundo pegado: el primero llegó cortado y no se aplicó. Está también
al final del encargo.

> Modelo: Opus · Esfuerzo: alto
>
> Respuesta del consultor a la fase 0 de trabajo/guardias-citas (2026-10-05). Cópiala tal cual al encargo y al informe.
>
> 1. Las 4 citas de A-10 (dos), A-11 y A-18: SE SUSTITUYEN por su sustituto, como A-46 en VENTANA-EV-V9.md. Antes de sustituir, compara para cada par (viejo → sustituto) la cita y la afirmación tal como están en los ítems, con la CLI filtrada o leyendo los campos del ítem, nunca transcripciones. Si en algún par el sustituto ya no sostiene lo que la ambigüedad cita (por ejemplo, porque recortó esa parte), para con ese par y dímelo; los demás siguen. Las ambigüedades no cambian de estado. Commit con Fuente:, spec docs --escribir en el mismo commit y el procedimiento de AMBIGUEDADES.md. El contrato se amplía con ambiguedades.yaml y docs/spec/, declarado.
>    Porqué: la spec cita el ítem vigente; un supersedido solo se nombra para contar la sustitución.
>
> 2. Condición de G1, ni A ni B: «En todo fichero versionado bajo knowledge/spec/, un id ev-* supersedido solo puede aparecer dentro del mismo valor escalar de YAML, o de la misma línea de comentario, que nombra su sustituto. Cualquier otra aparición falla.» Se escanea el texto entero, comentarios incluidos, sin lista de campos. Lista de excluidos visible en el código y vacía. docs/spec/ fuera por ser generado, como propones.
>    Comprueba con la medida que, tras el punto 1, el recuento da 0 y que las 5 menciones en prosa (RN-034 y el comentario de A-41) pasan. Si alguna no nombra a su sustituto en el mismo valor o comentario, para: no se toca strategy_spec.yaml sin decisión.
>    Tests que rompen la guardia: un supersedido en el campo evidencia: (falla); el mismo id en una nota sin su sustituto (falla); con su sustituto en la misma nota (pasa); en un fichero nuevo bajo knowledge/spec/ (falla).
>    Porqué: nombrar la condición y negar por defecto; enumerar campos deja escapar el que nadie pensó.
>
> 3. commits_sin_fuente: SÍ al parámetro opcional que solo cambia el texto del mensaje. Con el valor por defecto, el mensaje tiene que ser byte a byte el actual: añade un test que lo compruebe, y los tests existentes no se tocan. Nada de un bucle propio en el test.
>    Porqué: un bucle paralelo que repite la guardia es una segunda vía que puede divergir.
>
> 4. Ancla de G2: aceptado c489685, fijado como sha en el test y que el test falle si no existe en la historia. Los tres commits que deja fuera (cfec50b, c489685 y f443eee) se listan en el informe.
>
> 5. Las dos líneas de Technical Debt salen de PROJECT_STATE.md cuando las guardias existan, en esta rama, y pasan literales a HISTORIA. El saldo final de bytes tiene que ser menor o igual que cero.
>
> Sigue con el encargo: make check y uv run botsito state check en verde, fix/guardias-citas con la CI de Linux y su número de run, y el revisor con su informe pegado al final.
>
> Rama lista para revisión, NO cerrada.

## 2. Punto 1: los cuatro pares, comparados en el ítem

Se leyeron los campos `cita_literal`, `afirmacion`, `tema` y `valor` de los ocho ítems (Read del
YAML de cada uno; ninguna transcripción). La pregunta, por par, es si el sustituto sigue
sosteniendo lo que la ambigüedad cita.

| Ambigüedad | Viejo → sustituto | El viejo dice | El sustituto dice | ¿Lo sostiene? |
|---|---|---|---|---|
| A-10 («stop a 0,8: fijo o 0,75 + spread»), RESUELTA | `ev-v1-000448-346d6d90` → `ev-v6-013508-b4c88d87` | tema `stop.nivel`, valor 0,75: «cubrir hasta un 0.75» | mismo tema, valor 0,80: «hay que hablar de 0,80 [...] ya no 0,75» | **Sí.** Es el nivel del stop, la pregunta de A-10, con el valor vigente; nombra el 0,75 que sustituye |
| A-10, RESUELTA | `ev-v2-003142-beb4ad3c` → `ev-v6-021939-1c7cad28` | tema `stop.nivel`, 0,75: «lo suelo poner en 0.75» | mismo tema, 0,80: «Ahora es a 0.8 No a 0.75» | **Sí**, por lo mismo |
| A-11 («SL en la orden o tras el llenado»), RESUELTA | `ev-v4-001207-0c4ffd4b` → `ev-v6-021939-b430a110` | tema `stop.introducido_en_operacion_075`. La cita dice cuándo y dónde va el stop: «se arma un trade y el stop loss se pone [...] el stop loss como tal que se va a introducir en la operación es hasta el 0.75»; nota «A-11: el consultor pregunta y el trader responde» | mismo tema, pero la cita es la del par anterior: «Es 0.80 Ya a 0.75 Acá nada más Ahora es a 0.8 No a 0.75». Solo trae el NIVEL | **No: PARADA.** Lo que A-11 cita, el stop que se introduce al armar el trade, está solo en la `afirmacion` del sustituto, no en su cita |
| A-18 (base de cálculo del objetivo), ABIERTA | `ev-v4-011951-5fb49e03` → `ev-v6-014702-2d7096db` | tema `objetivo.rr_13_margen_tres_perdidas`: mantiene 1:3 porque con pérdidas consecutivas la tercera se cubre | mismo tema: con 0,75 tres perdedores cuestan 2,25 y el cuarto deja 0,75 % de margen; con 0,80, 0,60. Su nota: «el 1:3 se mide sobre la CAJA COMPLETA (A-18)» | **Sí**, y con la cuenta que A-18 pregunta |

**Hecho:** `knowledge/spec/ambiguedades.yaml:159`, `:160` y `:363` citan ahora
`ev-v6-013508-b4c88d87`, `ev-v6-021939-1c7cad28` y `ev-v6-014702-2d7096db`:
- ninguna ambigüedad cambia de estado ni de otro campo;
- el commit lleva `Fuente:` con los tres sustitutos;
- `botsito spec docs --escribir` corrió en el mismo commit y no cambia ningún fichero, porque
  `docs/spec/ambiguedades.md` no pinta la evidencia;
- con ese cambio pasan `knowledge validate` (rc 0), `test_kit`, `test_hoja_preguntas`,
  `test_spec_docs_generados` y `test_reabrir_y_fuente_documental`.

Como pide la respuesta, el contrato se amplió con `knowledge/spec/ambiguedades.yaml` y `docs/spec/`,
con un comentario que lo declara, y protege nombrándolos los otros cuatro ficheros de
`knowledge/spec/`.

**A-11 no se toca (PARADA 1, §6).**

## 3. G1: la condición del consultor, escrita

- **Dónde:** `src/botsito/validation/citas_supersedidas.py`.
- **Qué mira:** el TEXTO entero de todo fichero bajo `knowledge/spec/`, recursivo, también uno
  nuevo, menos `EXCLUIDOS`, que es una tupla vacía a la vista.
- **La regla:** un id ev-* supersedido pasa solo si su sustituto está en el mismo valor escalar de
  YAML o en la misma línea de comentario.
  - Los escalares se localizan por posición con `yaml.compose_all`; un `>-` de varias líneas es UN
    valor.
  - Un comentario va desde el primer `#` de la línea que no está dentro de un escalar hasta el final
    de la línea.
  - Un fichero que no es YAML, o que no se lee como YAML, no tiene escalares: toda aparición falla.
  - El sustituto vale si es cualquiera de su cadena. El mensaje da el id, su sustituto, el vigente si
    hay cadena, el fichero y la línea.
- **Qué no lee:** recorre el sistema de ficheros, no git, porque en `validation/` solo `Historial` lee
  git, y `test_historial_sin_git` sigue en verde. Solo lee ids y `supersede`.
- **`docs/spec/` queda fuera** por ser generado.

**La medida pedida** (anexo `medir_g1.py`, salida `medir_g1-SALIDA.txt`):
- se miran 6 ficheros;
- tras el punto 1 quedan 4 apariciones de supersedidos en ellos (antes eran 7);
- las DOS menciones de RN-034 (`strategy_spec.yaml:1620`) PASAN, porque las dos están en el mismo
  valor `notas` que sus sustitutos;
- fallan dos:
  - `ambiguedades.yaml:179`, A-11, es la PARADA 1;
  - `ambiguedades.yaml:1100`, el comentario de A-41, es la **PARADA 2**: el id viejo está en la línea
    de comentario 1100 y su sustituto en la 1101.
- **El recuento NO da 0.**

Sobre las «5 menciones en prosa» de la respuesta: en la fuente hay 3 (las dos de RN-034 y la de
A-41). Las otras dos son la copia generada de RN-034 en `docs/spec/reglas.md:1208`, que G1 no mira.

**G1 NO está conectada a `knowledge validate`.** Con las dos paradas abiertas daría ERROR y
`make check` saldría en rojo, y para ponerla en verde habría que tocar A-11 o el comentario sin
decisión. Conectarla es un cambio de pocas líneas en `_validar`, junto a las comprobaciones de
citas: va en cuanto el consultor decida. La línea de Technical Debt de G1 sigue en
`PROJECT_STATE.md` hasta entonces (punto 5: sale cuando la guardia existe, y sin conectar no
vigila nada).

**Tests (`tests/unit/test_citas_supersedidas.py`, 14, todos en `tmp_path`)**:
- los cuatro de la respuesta:
  - un supersedido en `evidencia:` falla;
  - el mismo id en una nota sin su sustituto falla;
  - con su sustituto en la misma nota pasa;
  - en un fichero nuevo bajo `knowledge/spec/` falla;
- y además:
  - en una subcarpeta nueva falla;
  - en un `.md` falla aunque nombre al sustituto;
  - en un YAML ilegible falla;
  - en la misma línea de comentario pasa;
  - en un comentario con el sustituto en la línea siguiente falla;
  - con el sustituto en OTRO valor falla;
  - lo vigente pasa;
  - una cadena de dos supersedes da el vigente en el mensaje;
  - `EXCLUIDOS == ()`;
  - sin `knowledge/spec/` no hay nada que mirar.

## 4. G2: hecha

**`commits_sin_fuente`** (`src/botsito/comun/historial.py`) gana el parámetro opcional
`que: str = "spec/cases"`, que solo nombra las rutas en el mensaje de un commit sin trailer.
- Ninguna comprobación cambia.
- Con el valor por defecto, el mensaje es el de antes byte a byte, y lo comprueba
  `test_el_mensaje_por_defecto_es_el_de_siempre`.
- Los tests existentes (`tests/contract/test_feedback_history.py`) no se tocan y pasan.

**`tests/contract/test_tramos_fuente.py`:**
- **Ancla:** `ANCLA_TRAMOS = "c489685f9ef5d1e126f2e3e81872c1f1c5a644fd"`, un sha completo;
  `test_el_ancla_es_un_sha_completo` lo exige, sin tag ni fecha.
- **El helper `problemas_tramos`:** convierte en FALLO un ancla que no existe o un historial que no
  se puede evaluar (`None`). La lectura del trailer es la de `commits_sin_fuente`, sin bucle propio.
- **`test_repositorio_real`:** pasa sobre el repo real con los ids que existen (`ids_de_fuente`).
- **Los que rompen la guardia, en repos temporales:**
  - un commit tras el ancla sin `Fuente:` falla;
  - con `Fuente:` pasa;
  - con una `Fuente:` que no existe falla;
  - el commit del ancla y los anteriores no se miran;
  - un ancla inexistente falla;
  - un commit que no toca los tramos no se mira;
  - y el del mensaje por defecto.
- 9 tests nuevos en total.

**Los commits anteriores al ancla, que no se tocan:**
- **sin `Fuente:`:** `cfec50b` (2026-10-04 12:29) y `c489685` (2026-10-04 13:22);
- **con una ruta en vez de un id:** `f443eee` (2026-10-01 22:06);
- **con `Fuente:` válida, también anteriores:** `b9e7e8a`, `0e3ca88`, `3718889` y `ed25392`.

La línea de Technical Debt de G2 salió de `PROJECT_STATE.md` y pasó literal a HISTORIA
(«# Technical Debt PAGADA · ...»).

## 5. Encargo frente a lo hecho

| Encargo / respuesta | Hecho | Dónde |
|---|---|---|
| Base `442a948`, CI 37411332514; abrir con `abrir-rama` | Comprobado; rama, encargo, contrato y Archivo 18 | `2c22b15` |
| Fase 0 a)-d) antes de código | §0, con dos medidas; PARADA | `2c22b15` |
| Respuesta, copiada al encargo y al informe | §1.1 y el final del encargo | — |
| R1: sustituir las 4 citas, comparando cada par | 3 sustituidas; **A-11 PARADA** | §2 |
| R2: G1 con la condición del consultor, texto entero, excluidos vacíos | Escrita y probada; **sin conectar** | §3 |
| R2: medida tras el punto 1 = 0, y las menciones en prosa pasan | **No da 0**: queda A-11 y falla el comentario de A-41; RN-034 pasa | §3 |
| R2: los cuatro tests que la rompen | Hechos, más diez | §3 |
| R3: parámetro opcional y test del mensaje byte a byte | Hecho | §4 |
| R4: ancla `c489685` como sha; el test falla si no existe; los tres listados | Hecho | §4 |
| R5 / decisión 4: las dos líneas de Technical Debt a HISTORIA, saldo ≤ 0 | La de G2 hecha; la de G1, al conectarla | §4, §7 |
| make check y state check, `fix/guardias-citas` con la CI de Linux, revisor | Pendiente de las paradas | §7 |

**Desviaciones declaradas:**
- G1 está escrita y no conectada (§3).
- `spec docs --escribir` no cambió ningún fichero (§2).

## 6. PARADAS: dos decisiones del consultor

**PARADA 1 · A-11** (`knowledge/spec/ambiguedades.yaml:179`). Hoy cita `ev-v4-001207-0c4ffd4b`,
supersedido por `ev-v6-021939-b430a110`, cuya cita no sostiene lo que A-11 cita (§2). Opciones:
- **(a)** Quitar el id supersedido de la `evidencia:` de A-11 sin poner nada en su lugar. A-11 sigue
  citando `ev-v1-000620-0f7dea14`, sigue RESUELTA y la respuesta del trader del 2026-09-10 está en su
  `pregunta` y en el feedback. Es la recomendada: la spec no cita lo que ya no es vigente ni lo que no
  lo sostiene.
- **(b)** Sustituirlo de todas formas por `ev-v6-021939-b430a110`, aceptando que solo su `afirmacion`,
  y no su cita, dice lo del stop introducido en la operación.
- **(c)** Mantenerlo, con una excepción por id declarada en el código y con motivo. G1 no tiene ese
  mecanismo, y habría que diseñarlo.

**PARADA 2 · el comentario de A-41** (`knowledge/spec/ambiguedades.yaml:1100-1101`). Nombra
`ev-v3-002714-742f2589` en una línea y «supersedido por `ev-v6-000732-f9c41d5e`» en la siguiente.
Opciones:
- **(a)** Reajustar el corte de ese comentario para que el id viejo y su sustituto queden en la MISMA
  línea. Es un comentario de YAML: no cambia ningún valor, ni `docs/spec/`, ni el texto de la
  ambigüedad. Es la recomendada: la condición se queda como la escribió el consultor.
- **(b)** Leer «línea de comentario» como bloque de líneas de comentario seguidas. Ensancha la
  condición, y un bloque largo podría nombrar al sustituto lejos del viejo.

Con las dos respuestas:
1. se aplica el cambio en `ambiguedades.yaml`, con `Fuente:` si toca la evidencia;
2. G1 se conecta a `knowledge validate`;
3. la línea de Technical Debt de G1 sale a HISTORIA;
4. `make check`, `fix/guardias-citas` con la CI de Linux y el revisor.

## 7. Comprobaciones y bytes

**Antes del commit, sobre lo que entra:**
- `ruff check`, `ruff format --check` y `mypy` de los ficheros nuevos y cambiados, sin problemas;
- los tests nuevos (14 + 9) y `test_feedback_history.py` (sin tocar) pasan;
- `knowledge validate` da rc 0;
- el `make check` del commit va en su mensaje y en la sección siguiente de este informe cuando
  exista.

**Bytes de `PROJECT_STATE.md`:** 23.307 en `main` y 23.431 aquí, un saldo de **+124**.
- La Current Feature es más larga que «NINGUNA ABIERTA».
- La línea de G2 restó.
- Al sacar la de G1 (unos 150 bytes) el saldo queda por debajo de cero.

## 8. Respuesta del consultor a las paradas 1 y 2 (2026-10-06), y lo hecho

Copiada tal cual (también al final del encargo):

> Modelo: Opus · Esfuerzo: alto
>
> Respuesta del consultor a las paradas 1 y 2 de trabajo/guardias-citas (2026-10-06). Cópiala tal cual al encargo y al informe.
>
> 1. A-11: opción (a), CON CONDICIÓN. Antes de quitar el id supersedido, comprueba leyendo solo los campos del ítem (sin transcripciones) que la cita de ev-v1-000620-0f7dea14 sostiene por sí sola lo que A-11 cita: el stop que se introduce al armar la operación.
>    - Si lo sostiene: quita el id supersedido, A-11 sigue RESUELTA y cita solo ev-v1-000620-0f7dea14. Commit con Fuente:, spec docs --escribir y el procedimiento de AMBIGUEDADES.md.
>    - Si no lo sostiene: para. A-11 no se queda sin respaldo.
>    Ni (b), porque el sustituto no lo dice en su cita, ni (c), porque mantenerlo es lo que G1 prohíbe.
>    HALLAZGO para el informe, sin arreglarlo aquí: la afirmación de ev-v6-021939-b430a110 dice algo (el stop al armar) que su cita no contiene. Choca con «sin inferencias en evidence/». Mide si hay más ítems activos cuya afirmación vaya más allá de su cita solo si existe ya una comprobación que lo haga; si no existe, dilo y no la construyas. Lo decide el consultor en otra rama.
>
> 2. Comentario de A-41: opción (a). Reescribe el comentario para que el id viejo y su sustituto queden en la misma línea, sin cambiar lo que dice. Es un comentario de YAML: no cambia ningún valor ni docs/spec/. La (b) no: la condición no se ensancha para que pase un caso.
>
> Con eso, el recuento de G1 tiene que dar 0. Conecta G1 a knowledge validate, saca su línea de Technical Debt a HISTORIA y sigue: make check y uv run botsito state check en verde, push de fix/guardias-citas con la CI de Linux y su número de run, y el revisor con su informe pegado al final. Saldo de bytes de PROJECT_STATE menor o igual que cero.
>
> Rama lista para revisión, NO cerrada.

### 8.1 A-11: la condición NO se cumple, PARADA

Campos de `ev-v1-000620-0f7dea14`, leídos con Read del YAML, sin transcripción:
- tipo `MANAGEMENT`;
- tema `stop.proteger_al_entrar`;
- valor 0,75;
- `cita_literal`: «no olvidarse de poner el cuadro, bueno el cuadro de GAN [...] en 0.75 proteger el
  trade, a inicio apenas se genere la entrada»;
- `afirmacion`: «con el cuadro de Gann, proteger el trade en 0,75 apenas se genere la entrada»;
- ningún ítem lo supersede.

Su cita dice que el trade se protege en 0,75 «a inicio apenas se genere la entrada». **No dice que
el stop se introduzca al ARMAR la operación.** «Apenas se genere la entrada» admite las dos lecturas
que A-11 enfrenta: con la orden pendiente, o en cuanto la entrada se llena. Esa es la duda misma de
A-11, que su `pregunta` dice que se cerró con la respuesta del trader del 2026-09-10 y no con este
ítem.

Por sí sola no sostiene lo que A-11 cita, así que **el id supersedido no se quita y A-11 no se
toca**. Por eso G1 sigue dando 1 fallo (`knowledge/spec/ambiguedades.yaml:179`) y **no se conecta**.

Para el consultor quedan tres salidas, sin recomendación porque las tres son de contenido:
- buscar en el corpus un ítem activo cuya cita diga lo del stop al armar;
- citar el registro del trader del 2026-09-10 por la vía que admita la spec;
- o decidir otra cosa.

### 8.2 El comentario de A-41: hecho

El corte del comentario (`knowledge/spec/ambiguedades.yaml:1100-1102`) se movió para que
`(ev-v3-002714-742f2589 esta supersedido por ev-v6-000732-f9c41d5e)` quede en UNA línea. Medido
contra `HEAD`:
- las palabras del fichero entero, uniendo las líneas de comentario, son las mismas;
- el valor YAML cargado es idéntico;
- `spec docs --escribir` no cambia ningún fichero.

G1 lo deja pasar.

### 8.3 HALLAZGO, sin arreglarlo aquí

La `afirmacion` de `ev-v6-021939-b430a110` («el stop que se introduce en la operacion es 0,80, ya no
0,75») dice algo, el stop que se introduce en la operación, que su `cita_literal` («Es 0.80 Ya a 0.75
Acá nada más Ahora es a 0.8 No a 0.75») no contiene. Choca con «sin inferencias en evidence/».

**No existe ninguna comprobación que mida si una afirmación va más allá de su cita.** La única
relación que se vigila es la LONGITUD: `src/botsito/evidence/modelo.py:224` rechaza una afirmación
de más de 2 × la cita + 40 caracteres, y este ítem la cumple. Como pide la respuesta, no se mide
nada más ni se construye la comprobación. Lo decide el consultor en otra rama.

### 8.4 Medida de G1 tras las dos respuestas

`medir_g1.py`, con su salida en `medir_g1-SALIDA2.txt`:
- 4 apariciones de supersedidos en los 6 ficheros vigilados;
- **pasan 3**: las dos de RN-034 y la de A-41;
- **falla 1**: A-11.
- **El recuento no da 0.**

## 9. Respuesta del consultor a la parada de A-11 (2026-10-06), y lo hecho

Copiada tal cual (también al final del encargo):

> Modelo: Opus · Esfuerzo: alto
>
> Respuesta del consultor a la parada de A-11 en trabajo/guardias-citas (2026-10-06). Cópiala tal cual al encargo y al informe.
>
> CAMBIO DE DECISIÓN, declarado: la condición del punto 1 de la respuesta anterior no se cumplió. Quitar el id dejaría A-11 RESUELTA sin respaldo citable, y sustituirlo tampoco sirve, porque el sustituto no lo dice en su cita. Qué respalda A-11 es una decisión de contenido y no entra en esta rama.
>
> 1. G1 se conecta YA con UNA excepción visible en el código: A-11 + el id supersedido que cita hoy, con el motivo «respaldo de A-11 pendiente de decisión del consultor, GUARDIAS-CITAS.md §8; 2026-10-06». Tests:
>    - la guardia pasa con esa excepción y falla con cualquier otro supersedido;
>    - el test falla si la excepción ya no hace falta (A-11 deja de citar ese id), para que no quede viva sin uso;
>    - la lista de excluidos de ficheros sigue vacía.
>    La excepción es por par (ambigüedad, id), no por fichero ni por campo.
>
> 2. Búsqueda SOLO DE LECTURA para el informe (§8, «Candidatos para A-11»): con la CLI filtrada (uv run botsito kb find / kb at), busca ítems ACTIVOS cuya cita diga cuándo se pone el stop (al colocar la orden o al llenarse). Material citable solamente: nada de transcripciones en cuarentena ni de tramos no citables. Lista cada candidato con id, vídeo, minuto y su cita literal tal como está en el ítem. No cambies nada con ellos y no elijas ninguno.
>    Di también, sin opinar, qué dice hoy el repo sobre citar en la spec un registro escrito del trader (busca «fuente documental» en docs/validation/REABRIR-Y-FUENTE-DOCUMENTAL.md y en CLAUDE.md), y si existe en el repo un registro del trader del 2026-09-10 y dónde.
>
> 3. Technical Debt, una línea nueva que apunte a GUARDIAS-CITAS.md §8: «A-11 RESUELTA cita un ítem supersedido; su respaldo citable no dice el momento del stop; excepción en G1 hasta que decida el consultor.» Sale a la vez la línea de G1. El saldo de bytes de PROJECT_STATE tiene que seguir siendo menor o igual que cero; si no, para y dímelo.
>
> 4. El hallazgo §8.3 queda tal cual: no hay comprobación de afirmación frente a cita, y no se construye aquí.
>
> Sigue con el encargo: make check y uv run botsito state check en verde, push de fix/guardias-citas con la CI de Linux y su número de run, y el revisor con su informe pegado al final. Que el revisor compruebe aparte que la excepción es exactamente un par y que su test de caducidad falla cuando debe.
>
> Rama lista para revisión, NO cerrada.

### 9.1 G1, conectada, con UNA excepción por par

`src/botsito/validation/citas_supersedidas.py`:
- **`EXCEPCIONES`** es una tupla de `Excepcion(ambiguedad, id, motivo)` y hoy lleva un solo par:
  - `("A-11", "ev-v4-001207-0c4ffd4b", "respaldo de A-11 pendiente de decisión del consultor,
    GUARDIAS-CITAS.md §8; 2026-10-06")`.
- **Qué cubre:** la aparición pasa solo si está en un VALOR cuyo objeto más cercano con `id` es
  A-11. No cubre un comentario, otra ambigüedad, otro fichero ni otro supersedido.
- **Caducidad:** una excepción que no cubre ninguna aparición es un FALLO de la guardia («excepcion
  de G1 sin uso: A-11 ya no cita ...; se quita de EXCEPCIONES»). Si A-11 deja de citar el id,
  `knowledge validate` falla hasta que se quite.
- **`EXCLUIDOS`** (ficheros) sigue vacía.

**Conexión:** `src/botsito/validation/knowledge.py`, en `_validar`, justo después de la capa spec:
- un fallo de G1 es `ERROR: spec: ...` y corta con rc 1;
- en verde NO escribe una línea `OK:` propia, igual que `ventana_no_citable`.

**Desviación declarada:** la primera versión sí escribía una línea `OK:`, y rompió
`tests/unit/test_historial_sin_git.py::test_con_git_las_lineas_ok_son_las_de_main`. Esa guardia
congela la lista exacta de líneas OK de `knowledge validate`, y ampliarla sería tocar una guardia
existente (decisión 5), así que la línea se quitó. Que G1 corre y falla cuando debe lo prueba
`test_knowledge_validate_lleva_g1`.

**Medida final** (`medir_g1-SALIDA3.txt`):
- 4 apariciones en los 6 ficheros vigilados, **0 fallos**;
- pasan las dos de RN-034 y la de A-41 por la regla, y la de A-11 por la excepción.

**Tests nuevos de esta respuesta** (`tests/unit/test_citas_supersedidas.py`; diez, sobre los 14
de antes):
- `test_la_excepcion_es_exactamente_un_par`: `EXCEPCIONES == (ese par,)`, con su motivo literal;
- `test_la_excepcion_deja_pasar_su_par`;
- `test_la_excepcion_no_cubre_otro_supersedido_de_a11`;
- `test_la_excepcion_no_cubre_el_mismo_id_en_otra_ambiguedad`;
- `test_la_excepcion_no_cubre_el_par_en_otro_fichero_sin_objeto_a11`;
- `test_la_excepcion_no_cubre_un_comentario`;
- `test_caducidad_la_excepcion_sin_uso_falla`: en `tmp_path`, A-11 sin el id da el fallo de
  excepción sin uso;
- `test_caducidad_en_el_repositorio_real`: G1 sobre el repo real da `[]`, y falla en cuanto A-11
  deje de citar el id;
- `test_knowledge_validate_lleva_g1`: con la guardia forzada a fallar (`monkeypatch`),
  `knowledge.validar` sale con rc 1 y el ERROR;
- `test_sin_el_item_supersedido_la_excepcion_no_tiene_a_que_aplicarse`.

**Ajuste medido, sin tocar tests existentes.** El primer `make check` con G1 conectada salió en
rojo con 3 fallos:
- `test_cli.py::test_feedback_new_valida_contra_el_contexto_antes_de_escribir`;
- `test_pipeline_transcripcion.py::test_cli_transcribe_glossary_check_show`;
- `test_fotogramas_ffmpeg.py::test_cli_extract_check_show_y_knowledge_validate`.

Los tres montan un `knowledge/` mínimo, sin evidencia y sin A-11, y G1 daba la excepción por «sin
uso». En un repo donde el id ni siquiera está supersedido, la excepción no tiene a qué aplicarse.
Ahora solo puede quedar sin uso si su id está supersedido en ese repo. En el real lo está, así que
la caducidad sigue cortando en cuanto A-11 deje de citarlo (los dos tests de caducidad). Con el
ajuste pasan los tres sin cambiarlos.

La lista de ficheros excluidos la sigue vigilando `test_la_lista_de_excluidos_esta_vacia`. Los tests
anteriores pasan `excepciones=()` a sus fixtures, que no tienen A-11.

### 9.2 Candidatos para A-11 (solo lectura; ninguno elegido, nada cambiado)

**Cómo se buscó:**
- con la CLI filtrada, `uv run botsito kb find ... --solo evidencia`:
  - por tema (`--tema stop`);
  - por las palabras `limite`, `pendiente`, `orden`, `activa`, `apertura`, `inmediatamente` y
    `apenas`, con `--prefijo`;
- la cita entera, con `--video --desde --hasta --contexto`.

`kb at` no se usó: la guardia lo bloquea porque imprime la cruda.

**Lo que oculta la CLI:** la búsqueda por tema avisó «OCULTOS: 2 items de evidencia: 2 por tramo no
citable (b)», y no se ven. Solo se listan ítems ACTIVOS: ninguno lo supersede otro.

**Ítems activos cuya cita habla de cuándo se pone o se protege el stop:**

| Id | Vídeo | Minuto | Cita literal tal como está en el ítem |
|---|---|---|---|
| `ev-v1-000620-0f7dea14` | v1 | 0:06:20 | «no olvidarse de poner el cuadro, bueno el cuadro de GAN [...] en 0.75 proteger el trade, a inicio apenas se genere la entrada» |
| `ev-v3-004527-0e4f4834` | v3 | 0:45:27 | «si tú ya proteges inmediatamente, que es lo que yo también haría en esta entrada, ya tienes 0.25 explícitamente, pues estás guardando» |
| `ev-v3-010054-27f55634` | v3 | 1:00:54 | «Stop loss va a estar predefinido aquí [...] cuando el precio ya esté desarrollando a veces con 0.50 lo más probable es ir bajando o sea el stop loss» |
| `ev-v4-000530-c44e3210` | v4 | 0:05:30 | «había comentado a decir en algunos momentos proteger a 0.50 la entrada o sea apenas se dé» |
| `ev-v4-001221-1e66b5fd` | v4 | 0:12:21 | «la opción que yo te de aquí es que se abra la operación pero que este 0.75 se desplace lo suficiente como para que esté de acuerdo al split del momento [...] con ese porcentaje que igual va a ser el 0.75, ya ahí se calcule el lotaje para arriesgar el porcentaje de la cuenta» |
| `ev-v5-000312-f5062062` | v5 | 0:03:12 | «me activa la entrada y si yo protejo a 0.80, que es el SL por defecto» |
| `ev-v10-003559-211855b7` | v10 | 0:35:59 | «O sea, ya cuando tú pones el stop Para calcular el lotaje y todo Sería directamente a 0.8» |
| `ev-v10-003706-5b7055a2` | v10 | 0:37:06 | «Es que el stop se actualizaría O sea, se actualizaría a 0.8 No estaría en el 1 Se usa el 1 al comienzo Pero no de ejecución, sino como planteamiento» |

**Mirados y no listados**, porque su cita no habla del momento del stop:
- `ev-v3-002511-b12d67be`: la orden límite predefinida, sin stop;
- `ev-v4-010759-514b5d7d`: cerrar tras un equal;
- `ev-v10-010228-868271ee`: el spread al poner la orden;
- `ev-v3-004329-a16d379b`: dónde se define el stop, no cuándo.

### 9.3 Qué dice hoy el repo sobre citar un registro escrito del trader (sin opinar)

**El campo `evidencia:` de una ambigüedad:**
- solo admite ids de evidencia `ev-*` (`src/botsito/cases/ambiguedades.py:204-206`: «no es un id de
  evidencia»);
- `knowledge validate` exige que existan (`:256-258`).

**Fuente documental:**
- es el campo `fuentes_documentales`, y se admite solo en ambigüedades de `clase: medicion`;
- en una `pregunta` se niega («la evidencia de una pregunta es lo que dijo el trader, no un
  documento», `ambiguedades.py:197`);
- su `documento` tiene que estar dentro de `docs/` y commiteado, con `ancla` y `literal`;
- la evidencia puede ir vacía solo si hay al menos una fuente documental;
- fuentes: `docs/runbooks/AMBIGUEDADES.md`, «Una fuente documental en vez de evidencia»;
  `docs/validation/REABRIR-Y-FUENTE-DOCUMENTAL.md` §1.3 y la decisión 3 de su respuesta; y
  `CLAUDE.md`, «Ambiguedades» («una `medicion` puede citar una fuente documental en vez de
  evidencia»).
- A-11 no tiene `clase` en el YAML.

**Un registro de feedback (`fb-*`)** es cita válida en otros sitios:
- la `cita` de una regla de `strategy_spec.yaml`;
- la `fuente` de un parámetro;
- el trailer `Fuente:` (`CLAUDE.md`, «El trailer Fuente:»).

**El registro del trader del 2026-09-10 existe:**
- **dónde:** `knowledge/feedback/2026-09-09-sesion-01/fb-2026-09-09-sesion-01-76fd91ba.yaml`,
  `medio: escrito`, `fecha: '2026-09-09'`;
- **qué registra:** `registrado_por: «Aleks · respuesta del trader del 2026-09-10, REFERIDA por el
  consultor (no es transcripcion)»`;
- **sobre qué:** objetivo `parametro/stop_en_orden_pendiente`, `accion: CONFIRM`,
  `valor_resultante: en_la_orden`;
- **qué dice:** `respuesta_literal: «el SL se pone junto a la orden limite, no cuando se apertura
  recien»`;
- su nota avisa de que la frase es la del consultor refiriendo la respuesta, no las palabras exactas
  del trader.
- Ya lo citan `knowledge/spec/parametros.yaml:794` (la `fuente` de `stop_en_orden_pendiente`) y
  `knowledge/spec/strategy_spec.yaml:1298` (la `cita` de una regla).
- A-11 no lo cita: su `evidencia:` no admite `fb-*`, y su `pregunta` lo menciona en prosa.

### 9.4 Technical Debt y bytes

- **Sale**, literal a HISTORIA («# Technical Debt PAGADA · ...», segundo bloque de esta rama): «Nada
  avisa cuando la spec o las ambiguedades citan un item ev-* supersedido ...».
- **Entra:** «A-11 RESUELTA cita un ítem supersedido; su respaldo citable no dice el momento del
  stop; excepción en G1 hasta que decida el consultor (docs/validation/GUARDIAS-CITAS.md §8).»
- **El hallazgo §8.3** queda tal cual.

**Bytes de `PROJECT_STATE.md`:** 23.307 en `main` y 23.285 en la rama: un saldo de **−22**.
- Con las dos líneas cambiadas el saldo daba +135, porque la línea nueva es más larga.
- La Current Feature de la rama se acortó a «G1 (evidencia supersedida) y G2 (Fuente: en los
  tramos), hechas. Informe ...».
- `Tests Currently Passing` pasa de 1309 a 1342 funciones.

## 10. Comprobaciones finales (2026-10-06)

Corrigen lo que §5 y §7 dejaron pendiente o desfasado (hallazgos a1 y b1 del revisor). Esas dos
secciones se dejan como estaban, como historia de la primera parada.

**`make check > make-check.log 2>&1`**, sobre el árbol de `d69aabd` con todo estadiado:
- `exit=0`, ninguna línea con `failed`;
- `CONTRATO: 20 ficheros dentro del contrato de trabajo/guardias-citas (riesgo medio, ...)`;
- `2060 passed in 900.18s (0:15:00)`;
- `SELLO: make check en verde sobre el arbol faafa09c2e59374ccf24b8d1ab5fa26b67df78f3`;
- `PICO DE MEMORIA de make check: 291 MiB en `test``.

El commit de los arreglos del revisor (abajo) pasa por su propio `make check` antes de commitearse,
porque el hook no deja commitear sin sello, y su salida no puede ir dentro del mismo commit.

**`uv run botsito state check`**, rc 0:
`OK: rama 'trabajo/guardias-citas' - funcionalidad actual: `trabajo/guardias-citas` EN CURSO
(2026-10-05): G1 (evidencia supersedida) y G2 (Fuente: en los tramos), hechas. Informe
docs/validation/GUARDIAS-CITAS.md.`

**CI de Linux:** la rama se empujó como `fix/guardias-citas`.
- Run **37481648537**, sobre `d69aabd`, `conclusion: failure` con **un solo fallo, el aceptado**:
  - `FAILED tests/unit/test_cli.py::test_state_check_ok_on_real_repo`;
  - con `ERROR: PROJECT_STATE declara la rama 'trabajo/guardias-citas'; la rama actual es
    'fix/guardias-citas'`;
  - `1 failed, 2051 passed, 8 skipped in 291.37s`.
- G2 corrió en Linux sobre la historia completa (`fetch-depth: 0`) y pasó.

**Bytes de `PROJECT_STATE.md`:** 23.307 en `main` y 23.285 en la rama, un saldo de **−22** (§9.4).

**Tests nuevos de la rama:** 33 funciones.
- 24 en `tests/unit/test_citas_supersedidas.py`;
- 9 en `tests/contract/test_tramos_fuente.py`;
- `Tests Currently Passing` pasa de 1309 a 1342;
- no se tocó ningún test existente.

## 11. Informe del revisor

Lanzado con el informe terminado hasta §9 y la CI de `d69aabd` hecha. Se pega tal cual.

## Informe del revisor · trabajo/guardias-citas · 2026-10-06

**Veredicto: lista para la orden del consultor, sin bloqueos.** Ningún hallazgo bloquea. Hay 2 de importancia y 2 menores, todos de forma del informe y no de código. Las cinco comprobaciones aparte salen bien. La base es main en 442a948, la rama lleva 4 commits y HEAD es d69aabd. Ese es el mismo sha de la CI `fix/guardias-citas` (run 37481648537).

### Eje (a) · Reglas de la casa
Resumen: 0 bloquea, 1 importa, 1 menor.

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| a1 | importa | El informe está desfasado respecto al estado real. §5 dice «la de G1, al conectarla» y «Pendiente de las paradas» para make check y CI. §7 da +124 bytes, y el saldo real es -22. §7 cuenta «14 + 9» tests. El `## Estado` final dice que «faltan el make check, la CI y el revisor». No consta el run 37481648537, ni la línea `SELLO`, ni los 2060 tests. El consultor puede leer el informe y creer que G1 no está conectada. | `docs/validation/GUARDIAS-CITAS.md:405-466` y `:713-717`. `grep -n "37481648537\|SELLO\|PICO\|2060"` sobre el informe no da ninguna línea. El saldo real está en la sección de PROJECT_STATE más abajo. |
| a2 | menor | `make-check.log` no existe en el árbol de trabajo. No pude verificar localmente el verde de 2060 tests ni la línea `PICO DE MEMORIA`. Lo que sí consta es la CI: 1 failed, 2051 passed, 8 skipped (suman 2060). | `ls make-check.log` da «No such file». `gh run view 37481648537 --log-failed` da `FAILED tests/unit/test_cli.py::test_state_check_ok_on_real_repo` y `1 failed, 2051 passed, 8 skipped`. |

Comprobado sin hallazgos:
- **Contrato.** `uv run python scripts/contrato_rama.py` da «20 ficheros dentro del contrato». Ningún fichero cae en `rutas_protegidas`. No cambian `strategy_spec.yaml`, `parametros.yaml` ni `knowledge/evidence`, `corpus`, `feedback` o `cases`. `git diff main --stat` sobre `strategy_spec.yaml` sale vacío.
- **Tests y estado.** Cinco ficheros de test dan 56 pasados: los dos nuevos, `test_historial_sin_git`, `test_feedback_history` y `test_spec_docs_generados`. `uv run botsito state check` da OK con la funcionalidad actual de la rama.
- **Trailer Fuente:.** Solo `f48e912` y `44f4336` tocan `knowledge/spec`, y ambos llevan `Fuente:` en el cuerpo.
  - `f48e912` cita `ev-v6-013508-b4c88d87`, `ev-v6-021939-1c7cad28` y `ev-v6-014702-2d7096db`.
  - `44f4336` cita `ev-v6-000732-f9c41d5e`.
  - Los cuatro ids existen en `knowledge/evidence/v6/`.
  - Los pares viejo→nuevo coinciden con el campo `supersede` de cada ítem:
    - `ev-v1-000448-346d6d90` → `ev-v6-013508-b4c88d87`
    - `ev-v2-003142-beb4ad3c` → `ev-v6-021939-1c7cad28`
    - `ev-v4-011951-5fb49e03` → `ev-v6-014702-2d7096db`
- **Cambios en `ambiguedades.yaml`.** El diff muestra 3 ids sustituidos en `evidencia:` (A-10 dos, A-18 uno) y el comentario de A-41 recortado en otra línea con las mismas palabras. No cambia ningún valor, y `docs/spec/` no cambia.
- **Citas vigentes.** A-11 sigue citando `ev-v4-001207-0c4ffd4b`, supersedido por `ev-v6-021939-b430a110`, cubierto por la excepción.
- **Regímenes de cambio.** Solo hay `A` en tests, informe y anexos. No se tocan evidence, feedback, manifests, corpus ni libros. No hay ADR nuevo y no hay informes cerrados modificados. La rama no añade ninguna `cita` a la spec, así que las tres guardias de `modelo.py` no aplican. No se tocó ningún test existente: `git diff main...HEAD -- tests` da 0 líneas eliminadas y solo `A` para los dos ficheros nuevos.
- **Holdout y material.** No se leyó material protegido. La guardia trabaja con ids.
- **PROJECT_STATE.**
  - Pesa 23.307 bytes en main y 23.285 en la rama: saldo **-22**, menor o igual que cero.
  - Salen las dos líneas de Technical Debt y entra la línea de A-11. Los bytes cuadran con el informe §9.4.
  - Las dos líneas están LITERALES en `docs/state/HISTORIA.md`, dentro del Archivo 18 (que empieza en la línea 5068), en las líneas 5287 y 5298 («Nada avisa…») y 5287 («Falta un test…» en la línea 5287). HISTORIA solo se amplía: `git diff main...HEAD` no tiene líneas `-`, y hay 1 `# Archivo` nuevo.
- **Ensayos.** Ningún ensayo de un script que escribe se hizo sobre copias sueltas.

### Eje (b) · Encargo
Resumen: 0 bloquea, 1 importa, 1 menor. Requisitos: 12 hechos, 0 parciales, 0 no hechos (los dos de verificación externa están hechos con salvedad, ver b1).

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 1 | Fase 0 a-d entregada antes de código | Hecho | Informe §0; commit `2c22b15` anterior al código. |
| 2 | Sustituir las 4 citas por su sustituto (resp. 1) | Hecho de otra forma, declarado | Se sustituyen 3. A-11 se deja con excepción por orden del consultor (resp. 3). El informe §8 y §9 lo declaran. |
| 3 | G1 con la condición del consultor, texto entero, excluidos vacíos (resp. 1, punto 2) | Hecho | `citas_supersedidas.py:46` `EXCLUIDOS = ()`; `:83-92` rglob recursivo. |
| 4 | Tests que rompen G1 (campo evidencia, nota sin sustituto, con sustituto, fichero nuevo) | Hecho | `test_citas_supersedidas.py:51,64,72,82`, más 10 de bordes. |
| 5 | G1 en `knowledge validate` con id, sustituto, fichero y línea | Hecho | `knowledge.py:1068-1079`. Mensaje `fichero:línea: nombra X, supersedido por Y`. Test `test_knowledge_validate_lleva_g1`. |
| 6 | Parada de A-11: UNA excepción por par y su test de caducidad | Hecho | `citas_supersedidas.py:47-53`; tests `test_la_excepcion_*` y `test_caducidad_*`. |
| 7 | Comentario de A-41 en una línea (resp. 2, punto 2) | Hecho | El diff de `ambiguedades.yaml` junta el id viejo y su sustituto en una línea. |
| 8 | `commits_sin_fuente` con parámetro `que`; mensaje por defecto byte a byte; los tests existentes no se tocan | Hecho | `historial.py` (diff): solo el f-string cambia a `toca {que} sin trailer`. Test `test_el_mensaje_por_defecto_es_el_de_siempre`. `test_feedback_history.py` sin diff (0 bytes). |
| 9 | G2 como test en CI con ancla sha `c489685`; falla si no existe; los tres commits listados | Hecho | `test_tramos_fuente.py:35`, `:41-42`. Los tres commits están listados en el docstring (`cfec50b`, `c489685`, `f443eee`). |
| 10 | Las dos líneas de Technical Debt a HISTORIA, línea de A-11 nueva, saldo ≤ 0 | Hecho | Ver el eje (a). |
| 11 | §8 «Candidatos para A-11» y el registro del trader (resp. 3, punto 2) | Hecho | Informe §9.2 y §9.3. No leí transcripciones. Sí consta que los candidatos son material citable. |
| 12 | `make check` y `state check` en verde con su salida en el informe; CI de Linux y su run; revisor al final | Parcial | `state check` OK (lo reejecuté). CI: ver b1. El informe aún no contiene la salida ni el run (hallazgo a1). |
| 13 | Hallazgo §8.3 sin construir la comprobación | Hecho | §8.3. No hay código nuevo para eso. |

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| b1 | importa | El número de run de la CI y la salida de `make check` no están en el informe, que es lo que el encargo pide («da el número de run», «con su salida en el informe»). El revisor no puede cerrar ese requisito por sí solo: solo puede confirmarlo por `gh`. | Ver a1. Confirmado: run 37481648537 sobre d69aabd, rama `fix/guardias-citas`, único fallo `test_state_check_ok_on_real_repo` (el fallo aceptado). |
| b2 | menor | `test_caducidad_en_el_repositorio_real` se llama «caducidad» pero solo comprueba que G1 no da fallos en el repo real. La caducidad la prueba de verdad `test_caducidad_la_excepcion_sin_uso_falla`, y la del repo real se activa por efecto, no por una aserción propia. Es una prueba que dice un poco más de lo que prueba. | `test_citas_supersedidas.py`, final del fichero. |

No hay trabajo fuera del encargo sin declarar. Lo único añadido es el parámetro `que`, que el consultor pidió, y los anexos de medida, que están en `rutas_permitidas`. No se tocaron los protegidos ni `strategy_spec.yaml`.

### Las cinco comprobaciones aparte
1. **Niega ficheros nuevos de `knowledge/spec/`, también en subcarpeta, y `EXCLUIDOS` vacía: BIEN.**
   - `citas_supersedidas.py:46` es `EXCLUIDOS: tuple[str, ...] = ()`. `ficheros_vigilados` usa `raiz.rglob("*")`, así que es recursivo.
   - Los tests pasan: `test_en_un_fichero_nuevo_bajo_knowledge_spec_falla`, `test_un_fichero_nuevo_en_una_subcarpeta_tambien_se_vigila` y `test_la_lista_de_excluidos_esta_vacia`.
   - Un fichero que no es YAML falla incluso si nombra al sustituto: `test_un_fichero_que_no_es_yaml_…`.
2. **El ancla de G2 es un sha completo y el test falla si no existe: BIEN.**
   - `ANCLA_TRAMOS = "c489685f9ef5d1e126f2e3e81872c1f1c5a644fd"`, 40 caracteres hexadecimales, y `test_el_ancla_es_un_sha_completo` lo exige.
   - `git cat-file -t c489685f…` da `commit`.
   - `problemas_tramos` devuelve un fallo si `resolver(repo, ancla)` es None. `test_un_ancla_inexistente_falla` lo prueba con `"0"*40`. Tampoco se salta en un clon superficial: devuelve un fallo.
   - Los tres commits posteriores al ancla que tocan el fichero (`809117b`, `f50b680`, `7120217`) pasan el test del repo real.
3. **Ningún test nuevo escribe en el repo real: BIEN.**
   - `grep` de `write_text|mkdir|open|unlink|touch…` sobre los dos ficheros da seis resultados, y todos escriben bajo `tmp_path`:
     - `test_citas_supersedidas.py:34-35`, helper `_spec(tmp_path, …)`.
     - `test_tramos_fuente.py:55-56`, `:64`, `:137`, helper `_repo(tmp_path)`.
   - Los helpers hacen `git init` dentro de `tmp_path`, y `_git` corre con `cwd=repo`, que es `tmp_path`.
   - Los dos tests que tocan el repo real (`test_repositorio_real` y `test_caducidad_en_el_repositorio_real`) solo leen.
4. **La excepción es EXACTAMENTE un par (A-11, ev-v4-001207-0c4ffd4b): BIEN.**
   - `EXCEPCIONES` tiene una sola `Excepcion("A-11", "ev-v4-001207-0c4ffd4b", "respaldo de A-11 pendiente de decisión del consultor, GUARDIAS-CITAS.md §8; 2026-10-06")`. El test `test_la_excepcion_es_exactamente_un_par` fija `EXCEPCIONES == (esperada,)`.
   - Se aplica por par: la clave es `(dueno, viejo)`, donde `dueno` es el `id` del objeto YAML que contiene el escalar. No es por fichero ni por campo.
   - Quedan fuera, y los tests lo prueban:
     - otro supersedido de A-11 (`test_la_excepcion_no_cubre_otro_supersedido_de_a11`);
     - el mismo id en A-12 (`test_la_excepcion_no_cubre_el_mismo_id_en_otra_ambiguedad`);
     - el par en otro fichero sin objeto A-11;
     - un comentario.
   - Matiz: la excepción cubre cualquier escalar dentro del objeto A-11 que nombre ese id, no solo el campo `evidencia:`. Es coherente con «por par, no por campo», y la guardia sigue sin enumerar campos.
5. **El test de caducidad falla cuando debe: BIEN.**
   - `test_caducidad_la_excepcion_sin_uso_falla` construye en `tmp_path` un A-11 que cita solo `OTRO`. La guardia devuelve exactamente `excepcion de G1 sin uso: A-11 ya no cita ev-v4-001207-0c4ffd4b; se quita de EXCEPCIONES (src/botsito/validation/citas_supersedidas.py)`.
   - En el repo real, `test_caducidad_en_el_repositorio_real` pasa hoy porque A-11 aún cita el id (G1 sin fallos). Si A-11 lo deja de citar, `citas_a_supersedidos` añade el problema de excepción sin uso y ese test falla, y también `knowledge validate`.
   - No repetí el caso por separado en un directorio temporal: la propia función de G1 ya se ejecuta sobre `tmp_path`, y los 56 tests pasan.

### Lo que no pude comprobar
- **`make check` completo.** No ejecuto cosas que escriben y no hay `make-check.log` en el árbol. Solo cuento con la CI (2051 + 1 fallo aceptado + 8 skipped) y con lo que diga el consultor.
- **`uv run botsito spec docs --check`.** Esa opción no existe (`unrecognized arguments: --check`). Lo cubrí con `tests/contract/test_spec_docs_generados.py`, que pasa. Que `spec docs --escribir` no cambie nada lo afirma el informe §2.
- **Si la afirmación de un ítem sostiene su cita (§8.3).** Es el hallazgo del propio informe y no hay comprobación mecánica. No leí citas ni transcripciones.
- **Las 3 citas del informe contra su fuente.** No comprobé tres citas del informe contra su fuente por esa razón. Solo contrasté los ids y los `supersede`.

### Comandos ejecutados
- `git branch --show-current`, `git status --short`, `git log --format='%h %s' main..HEAD`, `git diff --stat main...HEAD`
- `cat contrato.yaml`, lectura del encargo, `uv run python scripts/contrato_rama.py`
- Lectura de `citas_supersedidas.py`, `test_citas_supersedidas.py` y `test_tramos_fuente.py`
- `git diff main...HEAD -- src/botsito/comun/historial.py src/botsito/validation/knowledge.py knowledge/spec/ambiguedades.yaml`
- `git diff --name-status main...HEAD`
- `git diff main -- tests/contract/test_feedback_history.py | wc -c` (0)
- `git log --format='%h%n%B---' main..HEAD -- knowledge/spec`
- `git diff main --stat -- knowledge/spec/strategy_spec.yaml tests/contract/test_feedback_history.py tests/unit/test_historial_sin_git.py` (vacío)
- `git diff --name-status main...HEAD -- tests`
- Grep de `id|supersede` sobre `knowledge/evidence` para los ocho ids
- `uv run pytest tests/unit/test_citas_supersedidas.py tests/contract/test_tramos_fuente.py tests/unit/test_historial_sin_git.py tests/contract/test_feedback_history.py tests/contract/test_spec_docs_generados.py -q` (56 pasados), `uv run botsito state check` (OK), `uv run botsito spec docs --check` (opción inexistente)
- `wc -c PROJECT_STATE.md` y `git show main:PROJECT_STATE.md | wc -c`; `git diff main -- PROJECT_STATE.md`
- `grep` de las dos líneas literales en `docs/state/HISTORIA.md` y de `^# Archivo`
- `git cat-file -t c489685f…`; `git log c489685..HEAD -- knowledge/corpus/tramos_no_citables.yaml`
- `git diff main...HEAD -- tests | grep -c '^-[^-]'` (0)
- Grep de escrituras sobre los dos ficheros de test nuevos
- `gh run view 37481648537`, `gh run view 37481648537 --log-failed`, `gh run view 37481648537 --json headSha,headBranch` y `git rev-parse HEAD`
- Dos comandos con `$i` en la ruta fueron bloqueados por la guardia y los reescribí con rutas literales.

### 11.1 Lo hecho con cada hallazgo

- **a1 (importa), arreglado.** Este §10 trae el estado final: la salida de `make check`, el run de la
  CI, los bytes y los tests. La cabecera y el `## Estado` se actualizaron. §5 y §7 se quedan como
  historia de la primera parada, y lo dice el principio de §10.
- **b1 (importa), arreglado.** Igual que a1: el run 37481648537 y la salida de `make check` están en
  §10.
- **a2 (menor), sin cambio.** `make-check.log` se borra antes de cada commit por la regla del ritual;
  sus líneas están copiadas en §10.
- **b2 (menor), arreglado.** `test_caducidad_en_el_repositorio_real` tiene ahora su propia aserción
  de caducidad. Sin la excepción, G1 da exactamente un fallo en el repo real, el de A-11 en
  `ambiguedades.yaml` con `ev-v4-001207-0c4ffd4b`. El día que A-11 deje de citarlo, esa aserción falla.
- **El matiz de la comprobación 4** (la excepción cubre cualquier escalar del objeto A-11 que nombre
  ese id, no solo `evidencia:`) es lo que pide «por par, no por campo». Queda dicho en §9.1.

## Estado

**Lista para revisión, NO cerrada (2026-10-06).**
- **G1:** conectada a `knowledge validate`, con UNA excepción por par para A-11 y su caducidad.
- **G2:** test de CI con ancla `c489685`.
- **Las citas:** A-10 y A-18 citan el ítem vigente, y el comentario de A-41 está en una línea.
- **Technical Debt:** las dos líneas pasaron a HISTORIA y entró la de A-11.
- **Comprobaciones:** saldo de bytes −22; `make check` y `state check` en verde; CI de Linux
  37481648537 con solo el fallo aceptado.
- **El revisor:** pasado, con 0 bloquea, 2 importa y 2 menores, y lo hecho con cada hallazgo en
  §11.1.
- **Para el consultor:**
  - qué respalda A-11 (§9.2 y §9.3);
  - el hallazgo §8.3 (afirmación frente a cita), en otra rama.
