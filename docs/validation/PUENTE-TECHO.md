# PUENTE-TECHO · El puente del techo pieza a pieza, pre-registrado antes de correr (R4.7, entrada F)

> PLANTILLA hasta la fase 0: el inventario lo escribe la fase 0 (skill fase-cero) en su commit.

Rama `trabajo/puente-techo`, abierta el 2026-11-23 desde `main` en 8a10590b (commit de estado sobre
el merge 88f678f7 del tag `stable/F39l-recorrida-construccion-3`). Encargo:
`docs/encargos/trabajo-puente-techo.md`. Tramo: R4 (R4.7 de `docs/plan/HOJA-DE-RUTA.md`, lo que la
salida C de ADR-0098 pide antes de seguir; la F de la Next Action). El ADR del puente lo escribe la
fase P, a partir del borrador del ADR que trae Aleks. Tag previsto: `stable/F39m-puente-techo` (no
existe ni en local ni en origin: `git tag -l "stable/F39m*"` y `git ls-remote --tags origin
"stable/F39m*"` vacíos).

## Base comprobada (abrir-rama, paso 1)

- `git rev-parse main origin/main`: `8a10590b485ee3867426bf6dce6d08601e22d13b` dos veces; `git status --short` vacío.
- `git rev-parse "stable/F39l-recorrida-construccion-3^{commit}"` = `88f678f717554cc01c79209802d40b5252015c28` = `git rev-parse main^1`; en origin: `git ls-remote --tags origin stable/F39l-recorrida-construccion-3` da `ccb1f1d1…` (el objeto del tag anotado).
- CI de `main`: `gh run view 45107787390` (suelto, sin guion) → `✓ main ci`, job `python` en 9m7s; con `--json`: `status: completed`, `conclusion: success`, `event: push`, `headBranch: main`, `headSha: 8a10590b485ee3867426bf6dce6d08601e22d13b`. Es el run que dio el informe de cierre.
- `git branch -a` solo daba `main` (y `origin/main`); `git ls-remote --heads origin` solo da `refs/heads/main`.
- Sesión en Opus 5.5 (el esfuerzo no se ve desde la sesión; lo confirma Aleks); `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1` puesta (medido con `echo`): las corridas pueden ir en segundo plano.

## Los cuatro ficheros del Escritorio (sha256 medidos con `sha256sum`)

| Fichero | Bytes | sha256 medido | ¿Coincide con el del consultor? |
|---|---|---|---|
| `AUDITORIA-PROFUNDA-2026-11.md` | 271.910 | `542ee81011e9d82402d6c274bea3ffdfdaa886685fce24811ff146eaead01263` | sí |
| `auditoria-cazador-trabajo/INFORME-CAZADOR-2026-11-23.md` | 29.039 | `3a228954dcc81ed886add70f0aeb0702908e6593549c7b6f653043c459e1164a` | sí |
| el borrador del ADR | 19.965 | `aa4e95ff87144f4b748951fe6de16c68a1cb5950673b9815053eebd8bf58200b` | sí, en la segunda medida (abajo) |
| `PUENTE-TECHO.yaml` | 5.154 | `31e70e0a89db3f5b7c1500d7698f450f6d7d3f3659972ef5443ad383b524cfbf` | sí |

## Desviaciones de la apertura

- **PARADA antes de abrir por el borrador del ADR.** La primera medida dio 18.215 bytes y
  `26c81a4ecb12e9da5f84936e65c25a3cedc8c6d9b98c2d743951fa92c3caadb0` (LF, sin BOM; tampoco
  coincidía con CRLF, sin el salto final ni con uno de más). Se paró sin tocar nada ni leer su texto.
  Respuesta del consultor (2026-11-23): era una versión anterior; Aleks dejó la buena (19.965 bytes),
  cuyo sha coincide. Solo entonces se abrió la rama.
- **La fila de HOLDOUT-EXPOSICIONES del día** se escribió y estadió tras crear la rama y antes de
  cualquier otra escritura, lectura de material o `make check`. Su punto (8) se corrigió, aún
  estadiada y antes del primer `make check`, tras leer la auditoría profunda: el encargo dice que las
  dos auditorías leyeron «solo ficheros commiteados», y su eje P5 corrió `kb find`, que también recorre
  las transcripciones por la vía filtrada de la CLI (`src/botsito/retrieval/consultas.py:90-97`). Gana
  lo medido; la fila lo dice con su nombre. No es material reservado (CLAUDE.md, punto 1).
- **Los cuatro ficheros se leyeron enteros antes de usarlos.** Fechas, con un guion de la carpeta de
  trabajo que no imprime ninguna: 115 fechas en la auditoría profunda, 18 de ellas coinciden con un
  día de un caso reservado; todas son fechas de sucesos del repo dentro de nombres de fichero o ids ya
  commiteados en `main` (`SESION-01-<fecha>.md`, `fb-<fecha>-sesion-01-*`,
  `A-16-proveedor-de-datos-<fecha>.md`, `AUDITORIA-<fecha>-ultracode.md`) o la del primer commit del
  proyecto, y la propia auditoría las clasifica como legítimas en su §14, Parte 3. En el «cazador»,
  el borrador del ADR y el yaml, 0 coincidencias. Ningún resultado sin publicar: la aritmética va
  marcada como tal y la media de un subconjunto que se había colado se retiró allí (§14 y §15 de la
  auditoría profunda).

- **El primer `make check` de la apertura salió en rojo por algo mío** (1 failed, 3611 passed, 28:37):
  `tests/contract/test_repository_integrity.py::test_no_unexpected_ignored_paths` encontró
  `.claude/scheduled_tasks.lock`, el bloqueo del planificador de la sesión de Claude Code, creado a
  las 21:16 al programar con `ScheduleWakeup` un respaldo por si no llegaba el aviso del `make check`.
  Se cancelaron los respaldos pendientes, se borró ese fichero (sin seguir por git; no es del repo) y
  se repitió el `make check`. En esta rama no se vuelve a usar `ScheduleWakeup`: el aviso de las
  tareas de fondo basta. Fila preparada para ERRORES-RECURRENTES (§6).

## Estado

EN CURSO: apertura.
