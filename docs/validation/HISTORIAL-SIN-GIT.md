# FUNCTIONALITY VALIDATION REPORT · Sin historial evaluado, no se dice «intacto»

Rama `trabajo/historial-sin-git`, abierta el 2026-10-03 desde `main` `48ccbd2` (commit de estado
sobre el merge `c76aaf6`, tag `stable/F36t-reabrir-y-fuente-documental`; comprobado antes de abrir).
Encargo, copiado tal cual: `docs/encargos/trabajo-historial-sin-git.md`.

Objetivo: que ninguna comprobación de `knowledge validate` afirme lo que no evaluó. Paga la deuda
de Technical Debt que apunta a `docs/validation/REABRIR-Y-FUENTE-DOCUMENTAL.md` §4.2. No cambia el
motor, la spec, `knowledge/`, ninguna cifra ni ninguna ambigüedad.

## 0. Fase 0 · Inventario, sin tocar nada

### 0.1 Cómo se midió

Un guion de la carpeta de trabajo (fuera del repositorio) llama a `validar` en cuatro montajes:

| Montaje | Qué es | Código |
|---|---|---|
| `repo` | el repositorio real, con git y `data/` | 0 |
| `copia` | la copia sin `.git` de `test_kit.py` (`knowledge/`, `docs/`, `config/`, sin `holdout/{1,2,3}`) | 1 |
| `copia_m` | la misma copia más `data/manifests/` | 0 |
| `subdir` | `copia_m` dentro de un subdirectorio de un repositorio git nuevo con un commit: hay git y `historial_evaluable()` dice «el proyecto no es la raiz del repositorio git» | 1 |

La copia de `test_kit.py` tal cual sale con 1 en el kit (`datasets` cita manifiestos de
`data/manifests/`, que la copia no lleva) y **no llega** a las líneas de feedback ni de evidencia;
por eso se mide también `copia_m`, que llega al final. Los avisos de `data/` ausente (crudas,
índices de fotogramas) se filtran: son iguales en todos los montajes sin `data/`.

**El clon superficial no se montó**: un `git clone --depth 1` del repositorio copia el holdout
(`knowledge/cases/holdout/{1,2,3}`), y copiar es leer (`test_kit.py`, `_sin_holdout`). Pasa por la
misma rama del código que `subdir` (`historial_evaluable()` distinto de None), y
`tests/contract/test_feedback_history.py` ya prueba con un repo sintético que en un clon superficial
`modificaciones_en_historial` y `commits_sin_fuente` dan None.

### 0.2 Las comprobaciones que dependen de `con_git` o de `historial_evaluable`

`validar` (`src/botsito/validation/knowledge.py`) calcula `con_git = hay_git(repo)` y
`no_evaluable = historial_evaluable(repo) if con_git else None` (l. 555-556). Sin git,
`modificaciones_en_historial` y `commits_sin_fuente` devuelven None (llaman a `_git`, que falla), y
`historial_evaluable` devuelve None (no puede preguntar a git: «evaluable»).

| # | Comprobación | Dónde | Con git (repo, medido) | Sin git (copia_m, medido) | Git, historial no evaluable (subdir) |
|---|---|---|---|---|---|
| 1 | Libros solo-añadir (ADR-0039) | `corpus/libros.py:156` (`historial_evaluable`; y `versiones_del_fichero` None sin git); OK en `knowledge.py:480` | `OK: 3 libros declarados con formato y huso, solo-anadir intacto, cruzados con cobertura_material` | **la misma línea**, sin haber comparado ninguna versión | **la misma línea** (medido): `problemas_de_libros` sale antes del solo-añadir |
| 2 | Días retirados solo-añadir (ADR-0041) | `cases/holdout.py:508`; OK en `knowledge.py:494` | `OK: 1 dias retirados del holdout, cada uno de un reservado, solo-anadir intacto` | **la misma línea** | **la misma línea** (medido) |
| 3 | Evidencia inmutable | `modificaciones_en_historial(repo)`, `knowledge.py:557` | `OK: 437 items de evidencia, 0 contradicciones abiertas, historial intacto; 25 propuestas (0 items pendientes)` | **la misma línea** | `ERROR: la guardia de historial de evidencia no se pudo evaluar (el proyecto no es la raiz del repositorio git (…))`, código 1 (medido) |
| 4 | Feedback solo-añadir | `knowledge.py:670` | `OK: 150 registros de feedback, historial intacto, commits con Fuente` | **la misma línea** | ERROR «no se pudo evaluar» (código; no se llega: sale en la 3) |
| 5 | Trailers `Fuente:` y su ancla de trazabilidad | `resolver`, `ancla_desviada`, `commits_sin_fuente` con `con_git`, `knowledge.py:677-691` | el «commits con Fuente» de la línea de la 4 | **la misma línea**: sin git `ancla` es None, no se evalúa nada y no hay error | ERROR (código; no se llega) |
| 6 | Manifiestos de datos inmutables | `knowledge.py:722` | `OK: 8 manifiestos de datos validos, historial intacto` | **la misma línea** | ERROR (código; no se llega) |
| 7 | Manifiestos de transcripción inmutables | `knowledge.py:749` | `OK: 14 transcripciones registradas, historial intacto` | **la misma línea** | ERROR (código; no se llega) |
| 8 | Manifiestos de fotogramas inmutables | `knowledge.py:778` | `OK: 9 extracciones de fotogramas registradas, obligatorios presentes, historial intacto` | **la misma línea** | ERROR (código; no se llega) |
| 9 | Fuentes documentales commiteadas | `problemas_fuentes_documentales(…, con_git)` y `aviso_sin_git`, `knowledge.py:194-232, 626-630` | nada (ni OK ni aviso) | `AVISO: ambiguedades: sin git, NO se comprobo que el documento de las 6 fuentes documentales este commiteado (…)` | (código; no se llega) con `con_git` verdadero comprobaría `HEAD:<ruta>` con la ruta relativa al proyecto, y en un subdirectorio daría un falso «no esta commiteado» |

Las siete de §4.2 son la 1, 2, 3, 4, 6, 7 y 8. La 5 y la 9 son las otras dos que dependen de
`con_git`; la 5 va dentro de la línea de feedback («commits con Fuente») y tampoco se evaluaba sin git.

### 0.3 ¿Alguna cambia algo más que un mensaje? No

- **Sin git** (copia_m: código 0 en `main`): ninguna de las nueve cambia el código de salida;
  todas dejan de evaluar lo que depende del historial -igual que hasta hoy, la garantía es la CI- y
  las 1-8 lo tapan con un OK que lo afirma. Lo que no depende del historial se sigue comprobando
  (forma, cruce con `cobertura_material`, que cada retirada sea de un reservado, la ruta, el
  encabezado, la fila y el literal de las fuentes documentales).
- **Con git y el historial no evaluable** (subdir: código 1): la 3 da ERROR y `validar` sale con 1
  siempre (`historial is None and con_git`, sin otra salida), así que lo que las 1 y 2 afirman de
  más va en una ejecución que falla. Las 4-9 no se llegan a ejecutar. Solo mensaje.

Ninguna deja pasar un error que hoy se cace: no hay parada.

### 0.4 Lo que depende de git por otra vía (fuera del inventario del encargo)

No pasan por `con_git` ni por `historial_evaluable`, pero leen git. Leído en el código; lo único
medido es que la copia sin `.git` (copia_m) pasa sin quejarse de ninguna:

| Comprobación | Dónde | Sin git |
|---|---|---|
| Anclas de paquetes del kit, artefactos de fidelidad y repartos dev-visto (ADR-0035) | `cases/paquete.py:989` `problemas_de_ancla` (3 llamadas) | `blob_en_head` None → `continue`: el ancla **no se compara**, en silencio. Ninguna línea OK lo afirma («paquetes de sesion validos» no nombra el ancla). |
| `spec_version` subida si la spec cambió respecto a HEAD | `spec/manifiesto.py:209` `version_sin_subir` | `contenido_en_head` None → None, en silencio. La línea OK dice «hash del manifiesto al dia», que se calcula sin git. |
| Anterioridad del reparto respecto al `LABEL_CASE` | `cases/anterioridad.py:90`, `cases/paquete.py:1257` | falla CERRADO («no esta commiteado»). Hoy no hay ningún `LABEL_CASE`: no corre. |
| Autorizaciones del holdout (pre-registro commiteado) | `cases/holdout.py:126, 205` | falla CERRADO. |

Las dos primeras callan sin git pero no afirman nada que no evalúen: no entran en la regla del
encargo («no imprime intacto»), y tocarlas es tocar `src/botsito/cases/` y `src/botsito/spec/`, que
el contrato protege. Se anotan para el consultor (§ final), no se cambian aquí.

## 1. Fase 1 · El cambio

### 1.1 Una función común: `Historial`

Todo en `src/botsito/validation/knowledge.py`; `libros.py` y `holdout.py` no se tocan.

- **`Historial`** es la ÚNICA puerta por la que una línea de `validar` afirma algo que solo sabe el
  historial de git. `Historial.de(repo)` calcula UNA vez el motivo por el que el historial no se
  evalúa: `"sin git"` si `hay_git` es falso, si no lo que diga `historial_evaluable` (clon
  superficial, proyecto que no es la raíz), o None si se evalúa. Es la misma condición que ya
  usaban las nueve comprobaciones (§0.2), ahora en un solo sitio.
- **`ok(con, sin, (ambito, que)…, motivo=None)`**: con el historial evaluado devuelve `con` -la
  línea de hoy, carácter a carácter- y la apunta en `afirmadas`; si no, un
  `AVISO: <ambito>: <motivo>, NO se comprobo <que>` por cada comprobación y `sin`, que dice solo lo
  que sí se comprobó.
- **`aviso(ambito, que)`**: el aviso solo, para la comprobación que no tiene línea OK propia (las
  fuentes documentales). Sustituye a `aviso_sin_git`, con el MISMO texto sin git
  (`AVISO: ambiguedades: sin git, NO se comprobo que el documento de las 6 fuentes documentales
  este commiteado (…)`, que `test_kit.py` sigue exigiendo sin cambiar).
- **`sin_versiones(repo, ruta)`**: la causa que quedaba suelta. Libros y retirados saltan el
  solo-añadir también si `versiones_del_fichero` da None con el historial evaluable (git falló en
  esa pregunta); entonces el motivo es `git no dio las versiones de <ruta>` y sale como aviso, no
  como «intacto». Las otras siete ya daban ERROR en ese caso con git, y siguen igual.

**Niega por defecto**, en dos capas:
1. En ejecución: `validar` es ahora un envoltorio de `_validar`; al acabar, `afirmaciones_sueltas`
   busca líneas `OK:` que contengan una de `AFIRMACIONES_DE_HISTORIAL` («intacto», «commits con
   Fuente») y que no hayan salido de `ok`. Si hay alguna, `validar` sale con 1 y una línea
   `ERROR: validar: '<línea>' afirma lo que solo sabe el historial de git sin pasar por
   Historial.ok`. Una comprobación nueva que escriba «intacto» a mano no pasa `make check`.
2. En el código: un test recorre el AST de todo `src/botsito/` y falla si un literal con una de esas
   afirmaciones no va dentro de una llamada a `.ok(…)` (los docstrings y la propia tupla
   `AFIRMACIONES_DE_HISTORIAL` no cuentan).

**Su límite (lo señaló el revisor, b1):** las dos capas reconocen la afirmación por sus PALABRAS
(«intacto», «commits con Fuente»), no por el hecho de depender del historial. Una comprobación nueva
que afirme el historial con otra palabra («integro», «sin modificar») no la caza ninguna de las dos.
Cubre lo que el encargo nombra -que nada imprima «intacto» sin pasar por la puerta- y no más; una
afirmación nueva con otra palabra se añade a `AFIRMACIONES_DE_HISTORIAL` en la rama que la traiga.
*(Segunda orden del consultor, 2026-10-03: la guardia pasa a nombrar la condición -quién lee git-,
y las palabras quedan como segunda red. §6.1.)*

**El nombre `puerta`**: dentro de `_validar` ya había una variable `historial` (el resultado de
`modificaciones_en_historial` para la evidencia, l. 557 en `main`); llamar `historial` al
parámetro la habría sombreado y las líneas OK de después habrían llamado `.ok` sobre una lista.
Lo cazó mypy (`"Historial" has no attribute "__iter__"`) antes de ejecutar nada; el parámetro se
llama `puerta`.

### 1.2 Lo que dice cada una ahora sin el historial evaluado

| # | Línea OK (sin historial) | AVISO |
|---|---|---|
| 1 | `OK: 3 libros declarados con formato y huso, cruzados con cobertura_material` | `libros: <motivo>, NO se comprobo contra el historial que knowledge/corpus/libros.yaml sea solo-anadir` |
| 2 | `OK: 1 dias retirados del holdout, cada uno de un reservado` | `retirados: …, NO se comprobo contra el historial que knowledge/cases/retirados.yaml sea solo-anadir` |
| 3 | `OK: 437 items de evidencia, 0 contradicciones abiertas; 25 propuestas (0 items pendientes)` | `evidencia: …, NO se comprobo contra el historial que ningun fichero de knowledge/evidence/ se haya modificado, borrado o renombrado` |
| 4 y 5 | `OK: 150 registros de feedback` | `feedback: …` (igual, `knowledge/feedback/`) y `trailers Fuente: …, NO se comprobo que los commits que tocan knowledge/spec/ y knowledge/cases/ lleven un trailer `Fuente:` con ids que existen, ni el ancla de trazabilidad stable/F06` |
| 6 | `OK: 8 manifiestos de datos validos` | `manifiestos de datos: …` (`data/manifests/`) |
| 7 | `OK: 14 transcripciones registradas` | `transcripciones: …` (`knowledge/corpus/transcripciones/`) |
| 8 | `OK: 9 extracciones de fotogramas registradas, obligatorios presentes` | `fotogramas: …` (`knowledge/corpus/fotogramas/`) |
| 9 | (sin línea OK) | `ambiguedades: …, NO se comprobo que el documento de las 6 fuentes documentales este commiteado (…)`; y `problemas_fuentes_documentales` recibe `puerta.motivo is None` en vez de `con_git` |

Los ERROR de hoy con git y el historial no evaluable («la guardia de historial de … no se pudo
evaluar») no cambian: con git siguen siendo ERROR, como manda el encargo.

### 1.3 Medido: la salida antes y después, en los cuatro montajes

El mismo guion de §0.1, sobre el árbol de la rama, comparado línea a línea con lo medido en `main`:

- **`repo` (con git): idéntica y código 0**, salvo `OK: 304 documentos` → `OK: 305 documentos`: es
  el informe de esta rama (`docs/validation/HISTORIAL-SIN-GIT.md`), un documento más que mira la
  comprobación de ids citados, no el código.
- **`copia_m` (sin git): código 0 en las dos.** Las ocho líneas OK pierden «intacto» / «commits con
  Fuente» y llevan delante sus nueve avisos (el de ambigüedades ya estaba y no cambia). Ninguna
  línea contiene «intacto».
- **`copia` (la de `test_kit.py`, sin git): código 1 en las dos** (el kit, por `data/manifests/`);
  cambian las cinco que se alcanzan (libros, retirados, transcripciones, fotogramas, manifiestos).
- **`subdir` (git, historial no evaluable): código 1 en las dos.** Libros y retirados pasan de
  «solo-anadir intacto» a su aviso con el motivo `el proyecto no es la raiz del repositorio git
  (…)`; el ERROR de la evidencia, igual (cambia solo la ruta temporal).

En los documentos: 302 → 303 en las dos copias, por lo mismo.

### 1.4 Los tests, cada uno roto a propósito

`tests/unit/test_historial_sin_git.py`, seis funciones (siete tras §6.1, 1246) (1239 → 1245 en `PROJECT_STATE`; siete y
1246 tras la segunda orden, §6.1). Cada rotura
la hizo un guion de la carpeta de trabajo que muta `knowledge.py`, corre ese test y restaura el
fichero comprobando su sha256 (`bfa378919a92…` antes y después).

| Test | Qué comprueba | Rotura | Resultado |
|---|---|---|---|
| 1 `test_sin_git_ninguna_linea_dice_intacto_y_cada_comprobacion_avisa` | copia sin `.git` + `data/manifests/`: ninguna línea con «intacto» ni «commits con Fuente», exactamente un aviso «sin git, NO se comprobo» por cada uno de los nueve ámbitos, la línea OK de lo que sí se comprobó, y código 0 | libros vuelve a su OK de antes (`salida.append(…solo-anadir intacto…)`) | FALLA en la aserción de «intacto» (l. 82) |
| 2a `test_una_afirmacion_de_historial_que_no_pasa_por_historial_hace_fallar_validar` | una comprobación falsa (monkeypatch de `_validar`) añade `OK: 3 ficheros nuevos, historial intacto`: `validar` sale con 1 y el ERROR la nombra | `validar` deja de negar (`if True: return codigo, salida`) | FALLA: `assert 0 == 1` (l. 107) |
| 2c `test_afirmaciones_sueltas` | la función de la puerta: la línea afirmada pasa, la suelta no, un AVISO o un ERROR no afirman | (la cubre la rotura 2a) | — |
| 2b `test_ningun_literal_de_src_afirma_historial_fuera_de_historial_ok` | AST de `src/botsito/`: ningún literal con la afirmación fuera de `.ok(…)`; y el detector ve una falsa escrita a mano y deja pasar una que va por `ok` | una comprobación falsa en `knowledge.py`: `salida.append(f"OK: {len(items)} ficheros nuevos, historial intacto")` | FALLA: el diccionario de sueltos no está vacío (l. 157) |
| 3 `test_con_git_las_lineas_ok_son_las_de_main` | `validar` sobre el repositorio real con git: código 0, las doce líneas OK en orden y casando con las de `main` (recuentos como `\d+`), y ningún «NO se comprobo» | `transcripciones registradas, historial intacto` → `historial integro` | FALLA: `('OK: 14 transcripciones registradas, historial integro', …)` (l. 175) |
| 4 `test_con_git_y_el_proyecto_fuera_de_la_raiz_tampoco_dice_intacto` | la copia dentro de un subdirectorio de un repo git con un commit: código 1, el ERROR de la evidencia, ninguna línea con «intacto», y el aviso de libros y retirados con el motivo «el proyecto no es la raiz del repositorio git» | retirados vuelve a su OK de antes | FALLA en la aserción de «intacto» (l. 195) |

Sin rotura, los seis pasan (siete tras §6.1, 1246). El test 3 tarda ~70 s en esta máquina (verifica las citas contra las
crudas de `data/`; en la CI, sin `data/`, menos). El de historial no evaluable se montó con el
proyecto fuera de la raíz; el clon superficial no (§0.1).

`tests/unit/test_reabrir_y_fuente_documental.py`: el test de `aviso_sin_git` pasa a probar
`que_fuentes_documentales` y `Historial.aviso` con el mismo texto exacto de antes; por eso entra en
el contrato (`contrato.yaml` ampliado en el commit de la Fase 1).

### 1.5 PROJECT_STATE

Sale la línea de Technical Debt que apuntaba a `REABRIR-Y-FUENTE-DOCUMENTAL.md` §4.2 (la paga esta
rama; su registro irá a HISTORIA al cerrar, RITUAL.md) y «Tests Currently Passing» pasa de 1239 a
1245, que `make check` exige. Nada más.

## 2. La CI de Linux y `make check`

**`make check` sellado** sobre el commit de la Fase 1 (`5740220`): exit 0, ningún `failed`,
`1909 passed in 804.51s`, `SELLO: make check en verde sobre el arbol 28f92433762eb79830ce68c63c3b250a0776b4dc`,
`PICO DE MEMORIA de make check: 288 MiB`.

**CI de Linux: run 201** (id 37170620167), el push `git push origin
trabajo/historial-sin-git:refs/heads/fix/historial-sin-git` de `5740220` (el nombre que manda
`docs/runbooks/RITUAL.md`, «Antes del merge: la CI de Linux», leído antes de empujar).
`conclusion: failure` con **un solo fallo, el esperado**:
`FAILED tests/unit/test_cli.py::test_state_check_ok_on_real_repo` por `ERROR: PROJECT_STATE declara
la rama 'trabajo/historial-sin-git'; la rama actual es 'fix/historial-sin-git'`. Resumen:
`1 failed, 1900 passed, 8 skipped`. El run 199 de la rama anterior daba `1 failed, 1894 passed,
8 skipped`: seis más, los seis de `test_historial_sin_git.py`, que corrieron en Linux sin saltarse
(el test 3, con el `.git` del checkout de la CI, `fetch-depth: 0`). `make` para en `test`, así que
en la CI `knowledge validate` como paso suelto no llegó a correr; `validar` sobre el repositorio
con git sí, dentro del test 3.

## 3. Para el consultor: lo que depende de git por otra vía

§0.4: las anclas de los paquetes del kit, de los artefactos de fidelidad y de los repartos dev-visto
(`problemas_de_ancla`) y la subida de `spec_version` (`version_sin_subir`) **callan sin git**: no
se comparan y nada lo dice. No afirman nada que no evalúen, así que no entran en la regla de este
encargo, y están en `src/botsito/cases/` y `src/botsito/spec/`, fuera del contrato. Si se quiere que
también avisen, es otra rama (y el ancla, a diferencia del historial, se podría comprobar contra el
árbol sin git, calculando el blob en Python). No se anota en `PROJECT_STATE` porque el encargo lo
prohíbe; queda aquí. *(Segunda orden del consultor, 2026-10-03: aceptado, no se tocan en esta
rama, y van a Technical Debt con una línea que apunta aquí. §6.2.)*

## 4. Lo que encontró el revisor, y qué se hizo

Ninguno bloquea.
- **a1 (importa)**, el informe sin la CI, el sello ni el revisor: rellenado (§2, §5 y el estado).
- **a2 (menor)**, la numeración de los tests: el de `afirmaciones_sueltas` pasa a «2c» en §1.4.
- **b1 (importa)**, la puerta reconoce la afirmación por sus palabras: declarado en §1.1, «Su
  límite». No se amplía la lista: el encargo nombra «intacto», y añadir palabras que hoy nadie
  imprime no caza nada que exista.
- **b2 (menor)**, el test 3 compara con patrones y no con una salida de `main`: los patrones son
  las doce líneas OK medidas en `main` (§0.1, montaje `repo`) con los recuentos como `\d+`, para que
  el test no se rompa cada vez que entra un item; la comparación línea a línea con la salida real de
  `main`, recuentos incluidos, es la de §1.3 (idéntica salvo el documento de más).

## 5. Informe del revisor

## Informe del revisor · trabajo/historial-sin-git · 2026-10-03

### Eje (a) · Reglas de la casa
Resumen: 0 bloquea, 1 importa, 1 menor.
| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| a1 | importa | El informe de la rama aun no esta cerrado: §2 dice «PENDIENTE» (CI de Linux y `make check`) y `## Estado` dice «EN CURSO. Falta la CI de Linux, el sello de make check y el revisor». Hay que rellenar el run 201 (id 37170620167), el sello `28f92433…` (1909 passed, PICO 288 MiB) y pegar este informe, y cambiar el estado al final. | `docs/validation/HISTORIAL-SIN-GIT.md` §2 y ultima seccion |
| a2 | menor | El informe afirma «seis funciones» de test y 1239 a 1245. Es coherente con `PROJECT_STATE.md`, pero la tabla §1.4 usa la numeracion «2», «2a», «2b». Las 6 son: 1, 2a, 2, 2b, 3, 4. Solo forma. | `docs/validation/HISTORIAL-SIN-GIT.md` §1.4 |

Comprobado sin hallazgos:
- Contrato: `uv run python scripts/contrato_rama.py` da `CONTRATO: 8 ficheros dentro del contrato de trabajo/historial-sin-git (riesgo medio, …, 4 comprobaciones para el revisor)`. Los 8 ficheros del diff estan en `rutas_permitidas`. No se toca nada de `rutas_protegidas`: engine, domain, cases, corpus, knowledge y manifests no aparecen en `git diff --name-status`.
- `uv run botsito state check`: `OK: rama 'trabajo/historial-sin-git' - funcionalidad actual: …`.
- `uv run pytest tests/unit/test_historial_sin_git.py tests/unit/test_reabrir_y_fuente_documental.py -q -p no:cacheprovider`: todos los puntos en verde (46 tests, `[100%]`).
- `make check` (no ejecutado): `make-check.log` trae `1909 passed in 804.51s`, `All checks passed!`, `SELLO: make check en verde sobre el arbol 28f92433762eb79830ce68c63c3b250a0776b4dc` y `PICO DE MEMORIA … 288 MiB`. No comprobe que ese arbol sea el de 5740220 (`git write-tree` escribe).
- `knowledge validate` con git sobre el repo real: exit 0. Las lineas OK son las de siempre: libros «solo-anadir intacto», retirados «solo-anadir intacto», transcripciones, fotogramas y manifiestos «historial intacto», feedback «historial intacto, commits con Fuente», evidencia «historial intacto; …». Ningun «NO se comprobo». Salvo `304 → 305 documentos`, que el informe declara (el propio informe de la rama).
- Trailers `Fuente:`: ningun commit de la rama toca `knowledge/spec` ni `knowledge/cases` (`git log … -- knowledge` vacio). No aplica.
- Holdout y material: no se toca ni se cita. La rama no declara haber abierto libros, imagenes, fotogramas ni transcripciones, y mide con copias sin holdout. No hacia falta fila en `HOLDOUT-EXPOSICIONES`.
- Regimenes: `evidence`, `feedback`, `manifests`, `transcripciones`, `fotogramas` y `libros.yaml` no cambian. `HISTORIA.md` solo se amplia (`git diff` con 0 lineas borradas, Archivo 11 al final). `PROJECT_STATE.md`: solo presente, sin «Lo anterior:».
- Ambiguedades y ADR: no cambian `ambiguedades.yaml` ni ADR. No aplica.
- Informes cerrados: el diff no toca ningun `docs/validation/*.md` previo.
- Tres guardias de `cita`: la rama no anade ningun sitio con `cita`.
- Cifras: no se anade ninguna cifra a la forma ejecutable.
- Ensayos: el informe dice que las mediciones se hicieron con un guion en la carpeta de trabajo, sobre copias de `test_kit.py` y un repo git nuevo, no sobre el repo real.
- Citas del informe contrastadas con la fuente. (1) §0.2, la linea 1 con git (3 libros, 1 retirado, 14 transcripciones, 9 fotogramas, 8 manifiestos, 150 feedback, 437 evidencia, 25 propuestas): coincide con mi ejecucion. (2) El diff sustituye `aviso_sin_git` por `Historial.aviso` con el mismo texto. (3) La variable `puerta` no sombrea a `historial`: en el diff aparece `puerta.ok`, y la evidencia sigue usando `historial`.

### Eje (b) · Encargo
Resumen: 0 bloquea, 1 importa, 1 menor. Requisitos: 11 hechos, 1 parcial, 0 no hechos.
| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 1 | Fase 0: inventario de TODAS las comprobaciones que dependen de `con_git`/`historial_evaluable`, con salida con git, sin git y con historial no evaluable | Hecho | §0.2: 9 filas (las 7 de §4.2 mas trailers `Fuente`/ancla y fuentes documentales). §0.4 anade las que leen git por otra via. Contraste con el codigo: los usos de `con_git`/`historial_evaluable`/`hay_git` en `knowledge.py` quedan cubiertos. Una grep de «intacto» fuera de `knowledge.py` solo da `intacto_desde` (anterioridad/paquete, fallan cerradas), docstrings y un comentario. No encontre una que falte. |
| 2 | Medir sobre la copia sin `.git` y sobre una con historial no evaluable, o decir que no se puede | Hecho | §0.1: 4 montajes (`repo`, `copia`, `copia_m`, `subdir`). El clon superficial no se monto y se explica (copiaria el holdout). Cubierto por `test_feedback_history.py`. |
| 3 | Parar si alguna cambia algo mas que un mensaje | Hecho | §0.3 concluye «Solo mensaje». Con `subdir` la evidencia da ERROR, exit 1, antes y despues. No hay parada que justificar. |
| 4 | Regla: sin historial evaluado (sin git o `historial_evaluable` no) no se imprime «intacto», se imprime AVISO con «NO se comprobo» y el motivo | Hecho | `Historial.de`: `"sin git"` si no hay git, si no `historial_evaluable`. `ok()` emite `AVISO: <ambito>: <motivo>, NO se comprobo <que>`. Libros y retirados cubren ademas el caso `versiones_del_fichero` None (`sin_versiones`). |
| 5 | Mecanismo comun que niega por defecto | Hecho | Clase `Historial` mas `afirmaciones_sueltas`: `validar` da exit 1 y `ERROR: validar: … sin pasar por Historial.ok` si una linea OK con «intacto»/«commits con Fuente» no salio de `ok`. Ademas, un test AST sobre `src/botsito/`. Limite: lo detecta por texto («intacto», «commits con Fuente»), no por el hecho de depender del historial. Una comprobacion nueva con otra palabra no la caza (ver b1). |
| 6 | Fase 1: cada comprobacion sin historial emite su aviso y su OK deja de decir «intacto» | Hecho | Diff: 7 llamadas a `puerta.ok` (libros, retirados, transcripciones, fotogramas, manifiestos, feedback+trailers, evidencia) mas el aviso de fuentes documentales. Todas con su linea `sin`. |
| 7 | Con git, nada cambia: salida y codigo de `knowledge validate` | Hecho | Mi ejecucion: exit 0, las lineas OK textuales de `main`. Las cadenas `con` son las de antes caracter a caracter en el diff. Diferencia declarada: 304 → 305 documentos (el propio informe). |
| 8 | Sin git, el codigo de salida no cambia | Hecho | §1.3: `copia_m` 0 en las dos, `copia` 1 en las dos. Test 1 afirma exit 0. En el diff, `ok()` solo cambia las lineas, no los codigos; el unico `return 1` nuevo es el de `afirmaciones_sueltas`. |
| 9 | Test 1: copia sin `.git`, ninguna linea con «intacto», un aviso por comprobacion; roto devolviendo un OK | Hecho | §1.4, test 1, rotura documentada con su fallo (l. 82). Tras mis ejecuciones, los 46 pasan sin la rotura. La rotura la hizo el autor y no la repeti: no escribo. |
| 10 | Test 2: comprobacion falsa que imprime «intacto» sin pasar por el mecanismo hace fallar un test | Hecho | Tests 2a (monkeypatch de `_validar`, `validar` sale con 1) y 2b (AST de `src/`), cada uno con rotura documentada. |
| 11 | Test 3: con git, salida igual a main; roto cambiando una palabra de un OK | Hecho | Test 3 compara las 12 lineas OK con patrones y exige 0 «NO se comprobo»; rotura «historial integro» documentada. Observacion: contra patrones escritos en el test, no contra una salida de `main` real (ver b2). |
| 12 | Test 4: historial no evaluable con su rotura, o decir que no se monto | Hecho | Test 4 (proyecto en un subdirectorio de un repo git): exit 1, ERROR de evidencia, avisos con el motivo de la raiz. Rotura: retirados vuelve a su OK. Clon superficial no montado, dicho. |
| 13 | CI de Linux: push `fix/historial-sin-git`, dar run | Parcial | Run 201, id 37170620167. `gh run view` a los pocos minutos: `* fix/historial-sin-git ci · 37170620167 … Triggered via push about 2 minutes ago`, job `python` sin terminar. El informe aun dice PENDIENTE (a1). No puedo confirmar el «solo el fallo esperado de state check por el nombre fix/». |
| 14 | Quitar la linea de Technical Debt de §4.2 y nada mas en PROJECT_STATE | Hecho | `git diff` de `PROJECT_STATE.md`: sale solo esa linea de Technical Debt. Los demas cambios son los propios de abrir la rama: Current Branch, Current Feature, tests 1239 → 1245 (que `make check` exige) y «ninguna desde el Archivo 11». No se anade ninguna linea de deuda ni de estado nueva. |
| 15 | Informe en `docs/validation/HISTORIAL-SIN-GIT.md` con inventario, cambio, tests con rotura, run de CI y make check sellado; revisor pegado al final | Parcial | Inventario, cambio y tests: presentes. Run de CI y make check sellado: no estan en el informe (a1). El revisor lo pega quien llama, no yo. |

Hallazgos:
| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| b1 | importa | La puerta «niega por defecto» solo por los literales «intacto» y «commits con Fuente». Una linea OK nueva que dependa del historial y use otra palabra («integro», «sin modificar», «solo-anadir» a secas) no la caza ni `validar` ni el test AST. Esto es mas debil que «una comprobacion de historial nueva no puede imprimir intacto sin pasar por el mismo mecanismo», y el informe lo presenta como cubierta en dos capas sin decir ese limite. No hay que arreglarlo necesariamente, pero conviene declararlo. | `src/botsito/validation/knowledge.py:195` `AFIRMACIONES_DE_HISTORIAL = ("intacto", "commits con Fuente")`; `afirmaciones_sueltas` filtra con `any(a in x …)`; informe §1.1 «Niega por defecto, en dos capas». |
| b2 | menor | El test 3 («con git, igual que main») compara contra patrones escritos a mano en el propio test, no contra una salida real de `main`. Es suficiente como regresion de texto, pero el nombre promete mas. | informe §1.4, test 3 (`recuentos como \d+`). |

Fuera de encargo (cada cosa): (1) `sin_versiones` / caso `versiones_del_fichero` None con historial evaluable: justificado en §1.1 como «la causa que quedaba suelta» (la regla dice «por la causa que sea»). (2) Cambio en `tests/unit/test_reabrir_y_fuente_documental.py` y su entrada al contrato: justificado en §1.4. (3) `_validar` como envoltorio: justificado. No hay cambio fuera de las rutas permitidas. No se tocan las rutas que el encargo prohibe (motor, spec, knowledge, cifras, ambiguedades).

### Lo que no pude comprobar
- Resultado de la CI de Linux (run 37170620167): seguia en curso cuando mire; el job `python` no habia terminado. Mirar de nuevo con `gh run view 37170620167`.
- Que el arbol sellado `28f92433…` sea exactamente el de 5740220: `git write-tree` escribe en la base de objetos.
- Las roturas de los tests: no las repeti (modificar `knowledge.py` es escribir). Me baso en lo que cuenta el informe y en que los tests pasan sin rotura.
- Montaje `subdir` y salidas «sin git»: no las reproduje (requieren copiar y escribir fuera del repo). Me baso en el informe y en el diff.
- Lo que los tests de `test_kit.py` exigen del aviso sin git: no los ejecute (el contrato los lista, pero no estaban en los comandos que me diste). `make check` (1909 passed) los incluye.

### Comandos ejecutados
1. `git log --format='%h %s' main..HEAD`, `git diff --stat main...HEAD`, `git status --short`, lectura del encargo y de `contrato.yaml`.
2. `git diff main...HEAD -- src/botsito/validation/knowledge.py PROJECT_STATE.md tests/unit/test_reabrir_y_fuente_documental.py` y `git diff --name-status main...HEAD`.
3. Lectura de `docs/validation/HISTORIAL-SIN-GIT.md`.
4. `uv run python scripts/contrato_rama.py`; `uv run botsito state check`; lectura de `make-check.log` (SELLO, PICO, passed); recuento de lineas borradas en HISTORIA; `git log … -- knowledge`.
5. `uv run pytest tests/unit/test_historial_sin_git.py tests/unit/test_reabrir_y_fuente_documental.py -q -p no:cacheprovider` (46 passed); `gh run view 37170620167` (en curso).
6. `uv run botsito knowledge validate` (exit 0, lineas OK identicas a las de siempre); grep de «intacto» en `src/botsito`; `git diff main...HEAD -- docs/state/HISTORIA.md | head`.

## 6. Segunda orden: respuesta del consultor (2026-10-03)

Copiada tal cual (también al final del encargo):

> Modelo: Opus · Esfuerzo: alto
>
> Respuesta del consultor a trabajo/historial-sin-git (2026-10-03). Cópiala con su fecha al informe y al final del encargo.
>
> 1. La guardia nombra la condición, no las palabras. Hoy Historial reconoce la afirmación por su texto («intacto», «commits con Fuente»), y una comprobación nueva que diga «íntegro» se escaparía: lo dejaste escrito como límite y lo vio el revisor. La condición real es «esta comprobación lee el historial de git». Mide primero si las primitivas que leen git en src/botsito/validation/ (las que sean: hay_git, historial_evaluable, contenido_en_head, resolver, ancla_desviada y las que encuentres) están centralizadas. Si lo están, añade un test que recorra src/botsito/validation/ con ast y falle si alguna de esas primitivas se llama fuera de Historial (o de una lista explícita de excepciones, cada una con su porqué en un comentario). Rómpelo a propósito con una comprobación falsa que llame a una primitiva directamente. La comprobación por palabras se queda como segunda red. Si las primitivas NO están centralizadas y hacerlo exige tocar más que validation/, no lo hagas: para, dímelo con lo medido y añade una línea a Technical Debt que apunte al informe.
> 2. Las dos comprobaciones que callan sin git (las anclas de paquetes, fidelidad y dev-visto, y la subida de spec_version): aceptado, no se tocan en esta rama. No afirman nada, pero el encargo de la rama anterior pedía que sin git nada saliera en silencio. Una línea corta en Technical Debt que apunte a §3 de tu informe. PROJECT_STATE tiene que seguir por debajo de 25 KB: di su tamaño.
> 3. El push: empuja todo, el informe incluido, a fix/historial-sin-git (git push origin trabajo/historial-sin-git:refs/heads/fix/historial-sin-git). CI de Linux con solo el fallo esperado de state check; dame el número de run. La CI revisa también documentos, así que un commit de solo documentación no se queda fuera.
> 4. El revisor revisó un informe a medias. Pasada corta del revisor sobre el informe ya completo y sobre lo que cambie por los puntos 1 y 2, con su informe pegado al final. Para el cierre, la lección que irá a la fila de ERRORES-RECURRENTES de esta rama: el revisor se lanza con el informe terminado, nunca antes.
> 5. El clon superficial no montado para no copiar el holdout: aceptado, con ese motivo escrito en el informe, como ya está.
>
> make check sellado antes de cada commit.
>
> Rama lista para revisión, NO cerrada.

### 6.1 La condición: quién lee git (punto 1)

**Medido antes de tocar nada** (grep e imports de `src/botsito/validation/`, sobre `ac08b5a`):

- Los tres ficheros de `validation/`: solo `knowledge.py` lee git. `ids_citados.py` y
  `contexto_evidencia.py` no importan nada de `botsito.comun.historial` ni `subprocess`.
- Todas las primitivas que lee `knowledge.py` salen de UN módulo, `botsito.comun.historial`. Son
  ocho: `hay_git`, `historial_evaluable`, `versiones_del_fichero`, `contenido_en_head`,
  `modificaciones_en_historial` (cinco llamadas: evidencia, feedback, manifiestos, transcripciones,
  fotogramas), `resolver`, `ancla_desviada` y `commits_sin_fuente`.
- **No estaban centralizadas en `Historial`**: de catorce llamadas, tres iban dentro de la clase
  (`hay_git`, `historial_evaluable` y `versiones_del_fichero`) y once fuera: `contenido_en_head` en
  `problemas_fuentes_documentales`, y en `_validar` `hay_git`, `historial_evaluable`, las cinco de
  `modificaciones_en_historial`, `resolver`, `ancla_desviada` y `commits_sin_fuente`.
- **Centralizarlas solo exige tocar `knowledge.py`**: las once están en `validation/`. Así que no
  hay parada por este lado, y se hizo.
- **Lo que NO se centraliza sin tocar más que `validation/`**: `validar` llama a siete funciones de
  otros módulos que leen git por su cuenta (todos importan `botsito.comun.historial`):
  `problemas_de_libros` (`corpus/libros.py`), `problemas_de_retirados` (`cases/holdout.py`),
  `validar_paquetes` (`cases/paquete.py`: anclas y `LABEL_CASE`), `problemas_de_anterioridad`
  (`cases/anterioridad.py`), `validar_artefactos` (`cases/fidelidad.py`: anclas),
  `camino_visto.problemas` (`cases/visto.py`: anclas) y `comprobar_manifiesto_spec`
  (`spec/manifiesto.py`: `spec_version`). Libros y retirados ya dicen su línea por `Historial.ok`
  con el motivo de `Historial` (§1.1); las anclas y `spec_version` callan sin git (§3); anterioridad
  y `LABEL_CASE` fallan cerrado. Meterlas en `Historial` es tocar `cases/`, `corpus/` y `spec/`:
  no se hace, y va a Technical Debt (§6.2).

**El cambio** (`knowledge.py`): `Historial` gana cinco envoltorios -`en_head`, `modificaciones`,
`resolver`, `ancla_desviada`, `commits_sin_fuente`- y guarda `con_git` y `no_evaluable` al
construirse, con el mismo cálculo que hacía `_validar` (`SIN_GIT = "sin git"` es el motivo cuando no
hay git). `_validar` y `problemas_fuentes_documentales` ya no importan ninguna función de
`botsito.comun.historial`: fuera de la clase solo se importan sus constantes (`DIRECTORIO_*`,
`ANCLA_FUENTE`, `DIRECTORIOS_CON_FUENTE`). Las comprobaciones son las mismas, con los mismos
argumentos y en el mismo orden; los ERROR de hoy con git, iguales.

**El test** (`test_en_validation_solo_historial_lee_git`, el séptimo de
`tests/unit/test_historial_sin_git.py`; 1245 → 1246): recorre con `ast` cada `.py` de
`src/botsito/validation/` y falla si, FUERA del cuerpo de la clase `Historial`, se importa una
función de `botsito.comun.historial` (un nombre que no sea de constante, en MAYÚSCULAS), el módulo
entero (`import botsito.comun.historial`, `from botsito.comun import historial`) o `subprocess`
(git a mano). Mira las importaciones, no las llamadas: para llamar a una primitiva hay que
importarla, y así tampoco se escapa la que se pasa como argumento sin llamarla. **Lo que no ve**
(lo señaló el revisor en la pasada corta, a2): una importación dinámica (`__import__`,
`importlib`) y un subpaquete futuro de `validation/`, porque recorre solo sus `*.py` de primer
nivel (`glob`, no `rglob`); hoy `validation/` son tres ficheros planos y ninguno importa así. La lista de
excepciones existe (`EXCEPCIONES`, cada entrada `(fichero, nombre)` con su porqué en un comentario)
y hoy está vacía. Se autoprueba: ve una comprobación falsa con
`from botsito.comun.historial import DIRECTORIO_FEEDBACK, modificaciones_en_historial` (solo
señala la función, no la constante), ve `import subprocess`, y deja pasar la misma importación
dentro de `class Historial`.

**Rotura** (el guion de §1.4, ahora con siete casos; sha256 de `knowledge.py` igual antes y después,
`90687b1ea1e8…`): una comprobación falsa al final de `_validar` que importa
`modificaciones_en_historial` y escribe `OK: N ficheros integros`.

| Test | Resultado |
|---|---|
| `test_en_validation_solo_historial_lee_git` | FALLA: `Left contains one more item: 'knowledge.py:1071: modificaciones_en_historial'` (l. 245) |
| contraprueba: la misma rotura contra `test_ningun_literal_de_src_afirma_historial_fuera_de_historial_ok` | PASA (exit 0): la red de palabras no la ve, porque dice «integros». Es el hueco que señaló el revisor (b1), y ahora lo cierra el test de la condición. |

Las cinco roturas de §1.4 se repitieron sobre el código nuevo: las cinco FALLAN igual que antes
(mismas líneas, 82, 107, 157, 175 y 195). La red de palabras se queda como segunda red.

### 6.2 Technical Debt y el tamaño de PROJECT_STATE (punto 2)

Una línea nueva en Technical Debt: «Sin git callan, sin aviso, las comprobaciones que leen git
fuera de validation/ y no pasan por Historial: las anclas de paquetes, fidelidad y dev-visto y la
subida de spec_version (docs/validation/HISTORIAL-SIN-GIT.md §3 y §6.1)». Recoge en una sola línea
lo del punto 2 y lo del punto 1 que exige tocar más que `validation/`, porque son las mismas
lecturas. Y «Tests Currently Passing», 1245 → 1246. **`PROJECT_STATE.md`: 23.421 bytes**
(`wc -c`), por debajo del tope de 25.000 de `tests/unit/test_project_state.py`.

### 6.3 El push y la CI (punto 3)

`make check` sellado sobre el commit de la segunda orden (`7c5737b`): exit 0, ningún `failed`,
`1910 passed in 819.53s`, `SELLO: make check en verde sobre el arbol df37bb1d0be7a87fe5ed8e3e545c9f2f1988e1ca`,
`PICO DE MEMORIA de make check: 289 MiB`.

Empujado con `git push origin trabajo/historial-sin-git:refs/heads/fix/historial-sin-git`, que
lleva también `ac08b5a` (el informe de la primera vuelta, que no se había empujado).
**CI de Linux: run 202** (id 37173283083), sobre `7c5737b`: `conclusion: failure` con un solo
fallo, el esperado -`FAILED tests/unit/test_cli.py::test_state_check_ok_on_real_repo` por
`ERROR: PROJECT_STATE declara la rama 'trabajo/historial-sin-git'; la rama actual es
'fix/historial-sin-git'`-. Resumen: `1 failed, 1901 passed, 8 skipped`, uno más que el run 201: el
test de la condición, que corrió en Linux.

El commit que pega el informe del revisor (§7) se empuja igual, después: su run va en la respuesta
al consultor, porque un informe no puede llevar el run de su propio commit.

### 6.4 El revisor (punto 4)

Pasada corta lanzada con este informe terminado -§6.1 a §6.3, CI incluida- sobre `7c5737b` y el
informe en el árbol; su informe, entero, en §7. La lección para la fila de ERRORES-RECURRENTES de
esta rama, al cerrar: el revisor se lanza con el informe terminado, nunca antes.

Lo que encontró (0 bloquea, 0 importa, 3 menores), y qué se hizo:
- **a1**, «seis funciones» en §1.4 sin decir que tras la segunda orden son siete: anotado en §1.4.
- **a2**, el test de la condición no ve una importación dinámica ni un subpaquete futuro de
  `validation/`: declarado en §6.1, «Lo que no ve». No se amplía: hoy no hay ninguna de las dos.
- **b1**, mira importaciones y no llamadas: ya estaba declarado y justificado en §6.1.

### 6.5 El clon superficial (punto 5)

Sin cambios: el motivo -copiaría el holdout- ya está en §0.1.

## 7. Informe del revisor, pasada corta de la segunda orden

## Informe del revisor · trabajo/historial-sin-git · 2026-10-03 (pasada corta, segunda orden)

### Eje (a) · Reglas de la casa
Resumen: 0 bloquea, 0 importa, 2 menor.
| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| a1 | menor | El informe sigue diciendo «seis funciones» (1239 → 1245) en §1.4 y «Sin rotura, los seis pasan». Es cierto para la primera vuelta, y §6.1 aclara que el nuevo es el séptimo (1246). Una nota «(siete tras §6.1)» evitaría la confusión. | `docs/validation/HISTORIAL-SIN-GIT.md` l. 170 y l. 183, frente a l. 363 |
| a2 | menor | El test nuevo solo mira IMPORTACIONES y solo los `*.py` de primer nivel de `validation/`. No ve `__import__`, `importlib`, ni un subpaquete futuro (`glob("*.py")`). El informe lo dice para las importaciones (§6.1) pero no menciona los otros dos huecos. Hoy `validation/` son tres ficheros planos. | `tests/unit/test_historial_sin_git.py`, `VALIDATION.glob("*.py")` y `_lecturas_de_git_fuera_de_historial` |

Comprobado sin hallazgos:
- Contrato: `uv run python scripts/contrato_rama.py` da `CONTRATO: 8 ficheros dentro del contrato de trabajo/historial-sin-git (riesgo medio, …, 4 comprobaciones para el revisor)`. El diff `main...HEAD` solo toca ficheros de `rutas_permitidas` y nada de `rutas_protegidas`.
- `uv run botsito state check`: OK, rama 'trabajo/historial-sin-git'.
- `uv run pytest tests/unit/test_historial_sin_git.py -q -p no:cacheprovider`: `.......` 7 tests, `[100%]`. `grep -c "def test_"` da 7, y `git diff main...HEAD -- tests` añade 7 `def test_` (coherente con 1239 → 1246: 1245 más el nuevo).
- `make-check.log`: `1910 passed in 819.53s`, `All checks passed!`, `SELLO: … df37bb1d0be7a87fe5ed8e3e545c9f2f1988e1ca`, `PICO DE MEMORIA … 289 MiB`. Coincide con §6.3. No comprobé que ese árbol sea el de 7c5737b, porque `git write-tree` escribe en la base de objetos.
- CI: `gh run view 37173283083 --json headSha,conclusion` da `failure` sobre `7c5737b01418…`, que es el HEAD. `--log-failed`: solo `FAILED tests/unit/test_cli.py::test_state_check_ok_on_real_repo` con `ERROR: PROJECT_STATE declara la rama 'trabajo/historial-sin-git'; la rama actual es 'fix/historial-sin-git'`, y `1 failed, 1901 passed, 8 skipped`. Coincide con §6.3.
- PROJECT_STATE: `wc -c` da 23421 bytes, tanto en el disco como en `git show 7c5737b:PROJECT_STATE.md`, por debajo de 25.000. `git diff HEAD~1 HEAD -- PROJECT_STATE.md` muestra solo 1245 → 1246 y UNA línea nueva en Technical Debt (la de anclas y `spec_version`, que apunta a §3 y §6.1). La línea no lleva «Lo anterior:».
- `uv run botsito knowledge validate`: exit 0. Las líneas OK son las de siempre («solo-anadir intacto» en libros y retirados, «historial intacto» en transcripciones, fotogramas, manifiestos, feedback con «commits con Fuente» y evidencia). Ninguna «NO se comprobo». Las cifras coinciden con §0.2 (3 libros, 1 retirado, 14, 9, 8, 150, 437, 25), salvo 305 documentos, que el informe ya declara.
- Medición de §6.1 contra `git show ac08b5a:src/botsito/validation/knowledge.py`. Dentro de `Historial` había 3 llamadas (l. 218-227: `hay_git`, `historial_evaluable`, `versiones_del_fichero`). Fuera había 11: `contenido_en_head` (l. 297), `hay_git` y `historial_evaluable` (l. 646-647), `modificaciones_en_historial` ×5 (l. 648, 762, 814, 841, 870), `resolver` (770), `ancla_desviada` (776) y `commits_sin_fuente` (779). Son 14 en total y 8 primitivas, como dice el informe. `grep` sobre `src/botsito/validation/` no halla `comun.historial` ni `subprocess` fuera de `knowledge.py` (`ids_citados.py` y `contexto_evidencia.py` limpios).
- El estado nuevo de `knowledge.py`: las primitivas solo se importan dentro de métodos de `Historial` (l. 228-267). Fuera de la clase solo se importan constantes (`DIRECTORIO_EVIDENCIA`, `ANCLA_FUENTE`, `DIRECTORIO_FEEDBACK`, `DIRECTORIOS_CON_FUENTE`, `DIRECTORIO_TRANSCRIPCIONES`, `DIRECTORIO_FOTOGRAMAS`), y las llamadas pasan a `puerta.resolver`, `puerta.ancla_desviada` y `puerta.commits_sin_fuente` (l. 800-809). Las cinco comprobaciones y su orden se mantienen.
- Trailers `Fuente:`, holdout y material, regímenes de cambio, ambigüedades, ADR e informes cerrados: la rama no toca `knowledge/spec`, `knowledge/cases` ni ningún ADR o informe de `main`, y no abre material. No aplican. No se añade ningún sitio con `cita` ni ninguna cifra.
- Informe: no hay un §7 todavía. Es el hueco previsto para pegar este informe, y el Estado lo dice («falta pegar la pasada corta del revisor (§7)»). Lo pega quien llama.

### Eje (b) · Encargo (segunda orden)
Resumen: 0 bloquea, 0 importa, 1 menor. Requisitos: 8 hechos, 0 parciales, 0 no hechos (un requisito, el 4, queda a medias por quien me llama; ver su fila).
| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 1 | P1: medir si las primitivas que leen git en `validation/` están centralizadas | Hecho | §6.1 y la medición de `ac08b5a` (arriba): 14 llamadas, 3 dentro, 11 fuera. Esto es cierto. Incluye las del encargo (`hay_git`, `historial_evaluable`, `contenido_en_head`, `resolver`, `ancla_desviada`) y las que encontró (`versiones_del_fichero`, `modificaciones_en_historial`, `commits_sin_fuente`). |
| 2 | P1: si lo están (o se puede con solo `validation/`), test con `ast` que falle si se llaman fuera de `Historial`, con lista de excepciones comentada | Hecho | La centralización solo toca `knowledge.py`. `test_en_validation_solo_historial_lee_git`, `EXCEPCIONES` con su comentario (vacía). Variante: mira importaciones en lugar de llamadas, y el informe lo declara y lo justifica (§6.1, «para llamar hay que importarla»). Es «hecho de otra forma» declarada. |
| 3 | P1: romperlo con una comprobación falsa que llame a una primitiva directamente | Hecho | §6.1: rotura con `modificaciones_en_historial` y «ficheros integros», falla con `knowledge.py:1071`. Contraprueba: la red de palabras no la ve. Además el test se autoprueba con una falsa, un `import subprocess` y la misma importación dentro de `class Historial`. La rotura la hizo el autor y no la repetí: modificar `knowledge.py` es escribir. |
| 4 | P1: la red de palabras se queda como segunda red | Hecho | `AFIRMACIONES_DE_HISTORIAL` y `afirmaciones_sueltas` siguen en `knowledge.py`. Los tests 2a y 2b pasan. |
| 5 | P2: no tocar anclas ni `spec_version`; una línea corta en Technical Debt que apunte a §3 | Hecho | La línea nueva de PROJECT_STATE nombra §3 y §6.1. No hay cambios en `cases/` ni en `spec/` (`git diff --name-only main...HEAD`). Hay una sola línea, no varias. |
| 6 | P2: PROJECT_STATE por debajo de 25 KB y decir su tamaño | Hecho | 23.421 bytes (`wc -c`), dicho en §6.2. |
| 7 | P3: empujar todo, informe incluido, a `fix/historial-sin-git`, CI con solo el fallo esperado y el número de run | Hecho | Run 202, id 37173283083, solo el fallo de `state check` por el nombre `fix/`. El informe dice que lleva también `ac08b5a`. El commit del informe actual (§6.3/§6.4 y Estado, sin commitear en el disco) y el del revisor se empujan después; el informe lo dice (§6.3, último párrafo). |
| 8 | P4 y P5: pasada corta con el informe completo, su informe pegado al final; lección «el revisor se lanza con el informe terminado» anotada; clon superficial no montado con su motivo | Hecho / pendiente de quien llama | §6.4 y §6.5 contienen la lección y el motivo (§0.1, l. 29-33). Pegar este informe en §7 lo hace quien llama. `make check` sellado antes de cada commit: el SELLO es de 7c5737b. |

Hallazgos:
| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| b1 | menor | La segunda orden pedía «una lista explícita de excepciones» sobre llamadas. El test usa importaciones, lo cual es más estricto y no deja pasar una primitiva pasada como argumento. Está declarado y justificado, así que solo lo anoto como diferencia de forma. | `tests/unit/test_historial_sin_git.py`, docstring de `_lecturas_de_git_fuera_de_historial`; informe §6.1 |

Fuera de encargo: no hay nada. El cambio de `knowledge.py` (cinco envoltorios, `SIN_GIT`, `Historial` guarda `con_git` y `no_evaluable`) es el medio de P1. No se tocó nada de lo prohibido (spec, motor, `cases/`, `corpus/`, `knowledge/`).

### Lo que no pude comprobar
- Las roturas de §6.1 (una comprobación falsa en `knowledge.py`, sha256 `90687b1e…`): modificar el fichero es escribir. Me baso en lo que cuenta el informe y en que el test se autoprueba con el detector ante una falsa y pasa sin rotura.
- Que el árbol sellado `df37bb1d…` sea el de 7c5737b (`git write-tree` escribe).
- Las líneas de `knowledge validate` sin git y con proyecto fuera de la raíz: no las reproduje (requieren copias fuera del repositorio). Sí corrió la rama de git completo.
- La afirmación de §6.1 de que las cinco roturas de la primera vuelta se repitieron sobre el código nuevo con las mismas líneas: no la repetí.

### Comandos ejecutados
1. `git show 7c5737b --stat`, lectura del encargo y `git status --short`.
2. Lectura de `docs/validation/HISTORIAL-SIN-GIT.md`.
3. Un intento de volcar `git show ac08b5a:…` a un fichero temporal, bloqueado por el hook de solo lectura (no escribió nada).
4. `git show ac08b5a:src/botsito/validation/knowledge.py | grep -nE …`; `grep -rnE "comun.historial|subprocess|import historial" src/botsito/validation/`; `grep -nE …` sobre el `knowledge.py` actual.
5. `git diff HEAD~1 HEAD -- PROJECT_STATE.md`; `wc -c PROJECT_STATE.md`; `git show 7c5737b:PROJECT_STATE.md | wc -c`; `git show 7c5737b -- tests/unit/test_historial_sin_git.py`; `git diff --name-only main...HEAD`; lectura de `contrato.yaml`.
6. `uv run python scripts/contrato_rama.py`; `uv run botsito state check`; `uv run botsito knowledge validate` (exit 0); `gh run view 37173283083`.
7. `gh run view 37173283083 --log-failed | grep …`; `gh run view … --json headSha,conclusion`; `git rev-parse HEAD`; `sed -n 685,700p` de `knowledge.py`; `grep` de SELLO, passed y PICO en `make-check.log`; `git diff HEAD -- docs/validation/HISTORIAL-SIN-GIT.md`.
8. `uv run pytest tests/unit/test_historial_sin_git.py -q -p no:cacheprovider` (7 passed); `grep -c "def test_"`; `git diff main --stat -- tests`.

## 8. Orden de cierre del consultor (2026-10-03)

Copiada tal cual (también al final del encargo):

> Modelo: Opus · Esfuerzo: medio
>
> Orden de cierre de trabajo/historial-sin-git (consultor, 2026-10-03). Cópiala con su fecha al informe y al final del encargo. Se ejecuta cuando Aleks escriba /cerrar-rama trabajo/historial-sin-git; hasta entonces no hagas nada más.
>
> Tag: stable/F36u-historial-sin-git. Antes de usarlo, comprueba en HISTORIA que la última letra cerrada es la t; si no lo es, usa la siguiente libre y dilo.
>
> En el commit que saca el contrato, además de lo que manda RITUAL.md:
> 1. Informe, hallazgo a1 del revisor: en §1.4, donde dice «seis funciones» y «los seis pasan», añade «(siete tras §6.1, 1246)». No reescribas nada más.
> 2. Informe, hallazgo a2: en §6.1, junto al límite ya declarado, añade que el test tampoco ve __import__ ni importlib, y que solo recorre los *.py de primer nivel de validation/ (glob, no rglob). No se cambia código: es límite declarado.
> 3. Fila de la rama en ERRORES-RECURRENTES, con los hallazgos del consultor que el revisor no vio:
>    - importa: en la primera vuelta, el commit del informe (ac08b5a) se quedó sin push a fix/ y sin CI, y el revisor no lo señaló. Lección para el revisor: comprobar que el último commit de la rama, el que se va a fusionar, tiene su run de CI, no solo el commit del código.
>    - menor: el revisor se lanzó la primera vez con el informe sin terminar. Lección (§6.4): el revisor se lanza con el informe terminado, nunca antes.
>    - menor: la guardia de la primera vuelta reconocía palabras («intacto») en vez de la condición (leer git). Lo vio el revisor; se apunta como un caso más del patrón «nombra la condición, no los casos».
> 4. El registro del cierre en HISTORIA, con la deuda de §4.2 de REABRIR-Y-FUENTE-DOCUMENTAL.md como pagada.
>
> Después, el ritual completo: merge --no-ff, tag, commit de estado que solo sustituye Current Branch, Current Feature, Stable Main State y Last Stable Commit (Next Action no cambia), state check, make check sellado, push atómico de main y el tag, CI de main en verde y, solo entonces, borrar la rama local y fix/historial-sin-git de origin.
>
> Informe final: sha de main, tag, run de la CI de main, ramas que quedan en local y en remoto, y tamaño de PROJECT_STATE.

Hecho en el commit que saca el contrato (`chore(cierre)`):
- Letra: la última cerrada en HISTORIA es la `t` (`stable/F36t-reabrir-y-fuente-documental`), y
  `stable/F36u-historial-sin-git` no existía ni en local ni en `origin`: se usa ese tag.
- Punto 1 (a1): «(siete tras §6.1, 1246)» añadido en §1.4 tras «seis funciones» y tras «los seis
  pasan». Junto a «seis funciones» ya iba, desde la segunda orden, «siete y 1246 tras la segunda
  orden, §6.1»; no se reescribe.
- Punto 2 (a2): en §6.1 ya se declaraban `__import__`, `importlib` y los `*.py` de primer nivel
  desde la pasada corta; se añade «(`glob`, no `rglob`)». No cambia código.
- Puntos 3 y 4: la fila de la rama en `docs/runbooks/ERRORES-RECURRENTES.md` y el registro del
  cierre al final de `docs/state/HISTORIA.md`, con la deuda de
  `REABRIR-Y-FUENTE-DOCUMENTAL.md` §4.2 como pagada.

## Estado

CERRÁNDOSE por la orden de cierre del consultor del 2026-10-03 (§8), como
`stable/F36u-historial-sin-git`. Fases 0 y 1 y la segunda orden hechas: en `validation/` solo
`Historial` lee git, con su test por `ast` roto a propósito, y las palabras como segunda red.
`make check` sellado antes de cada commit; CI de Linux runs 201, 202 y 203 (este último sobre
`cab9eb1`, el informe con el revisor), los tres con solo el fallo esperado de `state check` por el
nombre `fix/`. Revisor: pasada completa (§5) y pasada corta con el informe terminado (§7), sin
bloqueos. El merge, el tag y la CI de `main`, en el registro de HISTORIA y en `PROJECT_STATE.md`.
