# FUNCTIONALITY VALIDATION REPORT

**Funcionalidad:** F01 · project-scaffold
**Rama:** `feature/F01-project-scaffold`
**Objetivo:** repositorio con paquete instalable, CI, contratos de importacion, plantillas y
`PROJECT_STATE.md` operativo, para que las garantias del plan sean mecanismos desde el primer commit.

## Que se construyo
- Arbol completo de MASTER_PLAN seccion B, con README de responsabilidad en cada carpeta de datos y
  documentacion, y docstring en cada subpaquete Python.
- Paquete `botsito` (src layout, hatchling, uv) con CLI minima: `botsito --version`,
  `botsito state check` (compara `Current Branch` de PROJECT_STATE con la rama real de git),
  `botsito knowledge validate` (no-op hasta F06).
- `pyproject.toml` con ruff, mypy strict, pytest, hypothesis e import-linter; tres contratos de
  importacion: pureza de `domain`, independencia de `spec`, y capas cli → validacion/motor →
  conocimiento/datos → domain.
- `Makefile` (`sync`, `lint`, `types`, `contracts`, `test`, `state`, `check`, `regress`),
  `.pre-commit-config.yaml`, CI Linux en GitHub Actions.
- Documentacion: `docs/plan/MASTER_PLAN.md` (Markdown), brief `docs/plan/features/F01-project-scaffold.md`,
  plantillas de brief, ADR e informe de validacion, ADR-0001 (estructura y regimenes de cambio).
- Tests de estructura (PROJECT_STATE, ADR, arbol), de CLI y de contratos por AST; esqueleto del test de
  literales de negocio que F02 rellena; fixture `holdout_guard` declarada (se activa en F14).

## Archivos creados
```
pyproject.toml  Makefile  .pre-commit-config.yaml  .github/workflows/ci.yml  uv.lock
config/settings.example.toml
docs/plan/MASTER_PLAN.md  docs/plan/features/_template.md  docs/plan/features/F01-project-scaffold.md
docs/adr/README.md  docs/adr/0000-template.md  docs/adr/0001-repository-structure-and-change-regimes.md
docs/validation/_template.md  docs/validation/F01-project-scaffold.md
docs/spec/README.md  docs/runbooks/README.md
knowledge/README.md  knowledge/{corpus,evidence,feedback,spec,cases/dev,cases/holdout,cases/fixtures}/README.md
data/manifests/README.md  scripts/README.md
mql5/README.md  mql5/{Experts,Include/Botsito,Scripts,tester}/README.md
src/botsito/__init__.py  src/botsito/cli.py
src/botsito/{corpus,evidence,feedback,spec,cases,data,domain,engine,validation,viewer,mql5bridge}/__init__.py
tests/conftest.py
tests/unit/test_project_state.py  tests/unit/test_adr.py  tests/unit/test_tree.py  tests/unit/test_cli.py
tests/contract/test_import_contracts.py  tests/contract/test_no_business_literals.py
tests/{integration,golden,regression,differential}/README.md
```

## Correcciones aplicadas tras la auditoria de fases (2026-09-04)
- `.gitattributes` (`* text=auto eol=lf`, binarios declarados); indice renormalizado: cero ficheros con CRLF.
- `tests/contract/test_repository_integrity.py`: ficheros esperados presentes en `git ls-files`, sin CRLF,
  sin rutas ignoradas imprevistas, patrones de `.gitignore` anclados. Nacio de dos incidentes reales.
- Hook local `scripts/git-hooks/pre-commit` (instalado por `make sync` via `core.hooksPath`): rechaza
  commits directos en `main` salvo `BOTSITO_ALLOW_MAIN=1`; comprueba contratos de importacion.
- CI y `make sync` con `uv sync --locked`; `PYTHONHASHSEED=0` exportado por el Makefile.
- `docs/plan/MASTER_PLAN.html` marcado como instantanea congelada; `MASTER_PLAN.md` es la fuente viva,
  con la seccion H (salvaguardas aprobadas) y Change Log.
- `docs/plan/AUDITORIA_FASES_2026-09-04.html` versionada como referencia.
- `tests/`, `tests/unit/`, `tests/contract/` son paquetes (necesario para compartir constantes entre tests);
  mypy strict cubre tambien `tests/`.
- Tercera auditoria: hook con modo ejecutable en el indice (100755), README en todas las carpetas sin
  exenciones, `knowledge/cases/holdout/{1,2,3}/` fisico segun la decision de tres particiones.

## Archivos modificados
`README.md` (arranque, nombre del paquete, enlace al plan en Markdown), `PROJECT_STATE.md`,
`Makefile`, `.github/workflows/ci.yml`, `docs/plan/MASTER_PLAN.md`, `docs/plan/MASTER_PLAN.html`.

## Decisiones tomadas
- **Nombre del paquete: `botsito`**, coherente con el repositorio. Confirmado implicitamente al aprobar la
  ejecucion del plan; renombrar despues costaria.
- **Contratos de importacion en dos capas** (import-linter + test AST) para que el contrato exista y se
  verifique aunque los paquetes esten vacios. Registrado en ADR-0001.
- **`state check` usa `git symbolic-ref`** en vez de `rev-parse`: el test de desajuste descubrio que
  `rev-parse` falla en un repositorio sin commits.
- **Hooks de inmutabilidad, solo-anadir y guarda de holdout NO se activan aqui**: pertenecen a F06, F09 y
  F14, que son las funcionalidades que crean el contenido que protegen. Estan declarados (fixture,
  README, ADR) para que no se olviden.
- **Sin `CLAUDE.md`**: la memoria operativa es `PROJECT_STATE.md`; duplicarla crearia deriva.

## Como ejecutarlo
```
make sync    # uv sync --locked + instala hooks (core.hooksPath)
make check
uv run botsito --help
uv run botsito state check
```

## Como probarlo
- `make check`: lint, formato, mypy strict, import-linter, pytest, `state check`.
- Provocar un fallo a proposito: cambiar `## Current Branch` en PROJECT_STATE.md y ejecutar
  `uv run botsito state check` → debe devolver 1 con mensaje. Anadir `import datetime` en
  `src/botsito/domain/__init__.py` y ejecutar `make contracts` → debe romper el contrato.

## Tests ejecutados
`make check` completo en `feature/F01-project-scaffold`, Windows 11, Python 3.12.10, uv 0.12.7.
Hook anti-main probado en un repositorio temporal (ver seccion Resultados).

## Resultados
- ruff: sin errores; 22 ficheros formateados.
- mypy strict: 13 ficheros, sin incidencias.
- import-linter: 3 contratos, 3 KEPT, 0 rotos.
- pytest: 26 passed (5 nuevos de integridad del indice).
- `botsito state check`: OK sobre la rama actual.
- Hook pre-commit: rechaza commit en `main` de un repositorio temporal; acepta con `BOTSITO_ALLOW_MAIN=1`.

## Pruebas cruzadas (2026-09-04)
| Entorno | Resultado |
|---|---|
| Clon limpio desde el repo local, `autocrlf=false`, `uv sync --locked`, `make sync`, `make check` | verde (26 tests, 3 contratos, mypy 28 ficheros) |
| Clon limpio con `core.autocrlf=true` (Windows por defecto) | copia de trabajo sin CRLF gracias a `.gitattributes`; tests verdes; hook con LF, acepta en feature y rechaza `main` |
| HEAD separado (checkout de CI en pull request) | `state check` avisa y devuelve 0; tests de CLI verdes |
| PowerShell 7 en vez de Git Bash | ruff, mypy, contratos, pytest, `state check` y `make check` verdes |
| Python 3.13 (entorno aislado) ademas de 3.12 | pytest, mypy y contratos verdes |
| Linux (ubuntu del CI) | NO probado localmente: sin WSL, Docker ni `act`. Se verifica en el primer push |

## Que deberia observar el usuario
`make check` termina en verde; el arbol coincide con MASTER_PLAN seccion B; `PROJECT_STATE.md` declara
`Current Feature = F01` y `Current Branch = feature/F01-project-scaffold`; ADR-0001 tiene las ocho
secciones del formato acordado.

## Que casos funcionan
Todos los del alcance: estructura, CLI, contratos declarados y verificados, documentos con formato.

## Que casos todavia no funcionan
- CI en GitHub no se ha ejecutado (no hay push por decision del usuario). El workflow es el mismo
  `make check`; se verificara en el primer push.
- `.pre-commit-config.yaml` (framework pre-commit) queda como opcion; los hooks activos son los de
  `scripts/git-hooks/` via `core.hooksPath`. Si se instala el framework, ambos no pueden coexistir
  sin ajustar `hooksPath`: decision para F02.

## Limitaciones
`botsito knowledge validate` no valida contenido (no hay contenido). El job de Windows para MQL5 no
existe hasta F29.

## Riesgos
Ninguno de negocio: no hay logica, parametros ni evidencia. Riesgo de proceso: si F02 anade un
parametro sin fuente, el test de literales aun esta vacio; F02 debe rellenarlo como primer paso.

## Impacto sobre funcionalidades anteriores
Ninguna anterior. El punto cero (documentacion) se conserva intacto.

## Estado
WAITING_FOR_USER_VALIDATION
