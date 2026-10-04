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

EN CURSO.

## Estado

EN CURSO. Fase 0 terminada (este inventario); Fase 1 sin empezar.
