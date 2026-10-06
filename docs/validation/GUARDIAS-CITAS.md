# Guardias de citas: G1 (evidencia supersedida) y G2 (Fuente: en los tramos)

Rama `trabajo/guardias-citas`, abierta el 2026-10-05 desde `main` en `442a948`. Ese es el commit de
estado de `stable/F37a-respuestas-ftmo`, y su CI de `main` (run 37411332514) estaba en verde,
comprobado antes de abrir. Encargo: `docs/encargos/trabajo-guardias-citas.md`. Paga dos líneas de
Technical Debt de `PROJECT_STATE.md`.

**Estado (2026-10-06, tras la respuesta a las paradas, §8): G2 hecha; G1 escrita, probada y SIN
CONECTAR; PARADA en A-11 (§8.1). El comentario de A-41 ya pasa (§8.2).** Lo de abajo es la historia
de la primera parada (§6):
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

## Estado

PARADA (2026-10-06) en A-11 (§8.1): la cita de `ev-v1-000620-0f7dea14` no sostiene por sí sola el
stop al armar la operación.
- **Hecho:** G2, G1 escrita y probada, A-10 y A-18 con su ítem vigente, y el comentario de A-41.
- **Sin conectar:** G1, porque daría 1 fallo.
- **Falta:**
  - la decisión sobre A-11;
  - conectar G1;
  - la línea de Technical Debt de G1;
  - la CI de Linux;
  - el revisor.

Rama NO lista para revisión.
