# DIAGNOSTICO-PREMISA · La premisa con costes, pre-registrada antes de que llegue, y dos diagnósticos de construcción (R4.7, entrada F)

> PLANTILLA hasta la fase 0: el inventario lo escribe la fase 0 (skill fase-cero) en su commit.

Rama `trabajo/diagnostico-premisa`, abierta el 2026-11-24 desde `main` en 76ca9996 (commit de
estado sobre el merge 7a3087e9 del tag `stable/F39m-puente-techo`). Encargo:
`docs/encargos/trabajo-diagnostico-premisa.md`. Tramo: R4 (R4.7 de `docs/plan/HOJA-DE-RUTA.md`, lo
que la salida C de ADR-0098 pide antes de seguir; la F de la Next Action). El ADR de la premisa lo
escribe la fase P, con el fichero que trae Aleks. Tag previsto: `stable/F39n-diagnostico-premisa`
(no existe ni en local ni en origin: `git tag -l "stable/F39n*"` y `git ls-remote --tags origin
"stable/F39n*"` vacíos).

## Base comprobada (abrir-rama, paso 1)

- `git rev-parse HEAD main origin/main` (tras `git fetch --prune origin`):
  `76ca9996c20c0f1aeede10472a5abeafc1cac7f5` tres veces; `git status --short` vacío.
- `git rev-parse "stable/F39m-puente-techo^{commit}"` = `7a3087e94d524232190eda90f58a4bcedc328bde`
  = `main^1` (el merge); en origin, `git ls-remote --tags origin "stable/F39m*"` da `81cf0884…` (el
  objeto del tag anotado) y `7a3087e9…` (`^{}`). Es el último `- Tag: ` de HISTORIA (línea 20958).
- CI de `main`: `gh run view 45490418025 --json …` (suelto, sin guion) → `name: ci`, `status:
  completed`, `conclusion: success`, `headBranch: main`, `headSha:
  76ca9996c20c0f1aeede10472a5abeafc1cac7f5`, creado el 2026-11-24T21:22:21Z. Es el run que dio el
  informe de cierre.
- `git branch -a` solo daba `main` (y `origin/main`); `git ls-remote --heads origin` solo da
  `refs/heads/main` (ningún `fix/*`).
- Sesión en Opus 5.5, esfuerzo alto (`/effort` puesto a alto al empezar la sesión);
  `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1` puesta (medido con `echo`): las corridas pueden ir
  en segundo plano.

## Los dos ficheros del Escritorio (sha256 medidos con `sha256sum`)

| Fichero | Bytes | sha256 medido | ¿Coincide con el del consultor? |
|---|---|---|---|
| `ADR-0100-borrador.md` | 17.996 | `d598776b945c83838513fcfea20d753287043a0486f3e978a8835e3b9b3e2feb` | sí |
| `PREMISA-COSTES.yaml` | 6.335 | `1294bdb1b7dfd992dd87e14ccb0f9d1d6b2bc6e45168bd19ed64a719f68f3b33` | sí |

Leídos enteros antes de usarlos. Fechas, con un guion de la carpeta de trabajo que no imprime
ninguna: 11 en el borrador (2 distintas) y 3 en el yaml (1 distinta), 0 en un día de un caso
reservado; son las de la decisión y del contraste con el trader. Ningún resultado sin publicar: las
cifras de su §1 y §7 están en `PUENTE-TECHO.md` y `VIABILIDAD-COMISION.md`, y los totales de los
libros vistos el 2026-11-24 no se copian (el §7 los nombra sin cifras).

## Estado

EN CURSO: apertura.
