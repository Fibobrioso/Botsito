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

`tests/unit/test_historial_sin_git.py`, seis funciones (1239 → 1245 en `PROJECT_STATE`). Cada rotura
la hizo un guion de la carpeta de trabajo que muta `knowledge.py`, corre ese test y restaura el
fichero comprobando su sha256 (`bfa378919a92…` antes y después).

| Test | Qué comprueba | Rotura | Resultado |
|---|---|---|---|
| 1 `test_sin_git_ninguna_linea_dice_intacto_y_cada_comprobacion_avisa` | copia sin `.git` + `data/manifests/`: ninguna línea con «intacto» ni «commits con Fuente», exactamente un aviso «sin git, NO se comprobo» por cada uno de los nueve ámbitos, la línea OK de lo que sí se comprobó, y código 0 | libros vuelve a su OK de antes (`salida.append(…solo-anadir intacto…)`) | FALLA en la aserción de «intacto» (l. 82) |
| 2a `test_una_afirmacion_de_historial_que_no_pasa_por_historial_hace_fallar_validar` | una comprobación falsa (monkeypatch de `_validar`) añade `OK: 3 ficheros nuevos, historial intacto`: `validar` sale con 1 y el ERROR la nombra | `validar` deja de negar (`if True: return codigo, salida`) | FALLA: `assert 0 == 1` (l. 107) |
| 2 `test_afirmaciones_sueltas` | la función de la puerta: la línea afirmada pasa, la suelta no, un AVISO o un ERROR no afirman | (la cubre la rotura 2a) | — |
| 2b `test_ningun_literal_de_src_afirma_historial_fuera_de_historial_ok` | AST de `src/botsito/`: ningún literal con la afirmación fuera de `.ok(…)`; y el detector ve una falsa escrita a mano y deja pasar una que va por `ok` | una comprobación falsa en `knowledge.py`: `salida.append(f"OK: {len(items)} ficheros nuevos, historial intacto")` | FALLA: el diccionario de sueltos no está vacío (l. 157) |
| 3 `test_con_git_las_lineas_ok_son_las_de_main` | `validar` sobre el repositorio real con git: código 0, las doce líneas OK en orden y casando con las de `main` (recuentos como `\d+`), y ningún «NO se comprobo» | `transcripciones registradas, historial intacto` → `historial integro` | FALLA: `('OK: 14 transcripciones registradas, historial integro', …)` (l. 175) |
| 4 `test_con_git_y_el_proyecto_fuera_de_la_raiz_tampoco_dice_intacto` | la copia dentro de un subdirectorio de un repo git con un commit: código 1, el ERROR de la evidencia, ninguna línea con «intacto», y el aviso de libros y retirados con el motivo «el proyecto no es la raiz del repositorio git» | retirados vuelve a su OK de antes | FALLA en la aserción de «intacto» (l. 195) |

Sin rotura, los seis pasan. El test 3 tarda ~70 s en esta máquina (verifica las citas contra las
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

PENDIENTE.

## 3. Para el consultor: lo que depende de git por otra vía

§0.4: las anclas de los paquetes del kit, de los artefactos de fidelidad y de los repartos dev-visto
(`problemas_de_ancla`) y la subida de `spec_version` (`version_sin_subir`) **callan sin git**: no
se comparan y nada lo dice. No afirman nada que no evalúen, así que no entran en la regla de este
encargo, y están en `src/botsito/cases/` y `src/botsito/spec/`, fuera del contrato. Si se quiere que
también avisen, es otra rama (y el ancla, a diferencia del historial, se podría comprobar contra el
árbol sin git, calculando el blob en Python). No se anota en `PROJECT_STATE` porque el encargo lo
prohíbe; queda aquí.

## Estado

EN CURSO. Fases 0 y 1 hechas; falta la CI de Linux, el sello de `make check` y el revisor.
