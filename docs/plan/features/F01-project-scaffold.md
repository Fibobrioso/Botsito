# F01 · project-scaffold

**Rama:** `feature/F01-project-scaffold` · **Fase:** 0 · **Depende de:** —

## Objetivo
Repositorio con paquete instalable, CI, contratos de importacion, plantillas de ADR, brief e informe de
validacion, y `PROJECT_STATE.md` operativo. Todas las garantias del plan son mecanismos; deben existir
antes de la primera funcionalidad de conocimiento.

## Alcance cerrado (que SI)
- Arbol de MASTER_PLAN §B con README de responsabilidad por carpeta.
- `pyproject.toml` (uv, ruff, mypy strict, pytest, hypothesis, import-linter), `Makefile`, CI Linux.
- Contratos de importacion declarados y verificados (import-linter + test AST).
- `.gitattributes` (LF), hook local anti-main (`scripts/git-hooks/`), `uv sync --locked` en CI.
- CLI minima: `botsito --version`, `botsito state check`, `botsito knowledge validate` (no-op).
- ADR-0001, plantillas, MASTER_PLAN.md en Markdown.
- Tests de estructura de documentos y de arbol.

## Fuera de alcance (que NO)
Ninguna logica de negocio, ningun parametro, ninguna evidencia, ningun hook activo de inmutabilidad
(se activan en F06/F09/F14).

## Entradas
`docs/plan/MASTER_PLAN.html` (plan aprobado), `PROJECT_STATE.md` inicial.

## Salidas (ficheros)
Ver `docs/validation/F01-project-scaffold.md`, seccion "Archivos creados".

## Tests
- `tests/unit/test_project_state.py` — secciones obligatorias y en orden.
- `tests/unit/test_adr.py` — estado y secciones de cada ADR.
- `tests/unit/test_tree.py` — arbol de §B con README.
- `tests/unit/test_cli.py` — `state check` coherente con la rama.
- `tests/contract/test_import_contracts.py` — pureza de `domain` y `spec` por AST; config de import-linter presente.
- `tests/contract/test_no_business_literals.py` — esqueleto (lista vacia) que F02 puebla.
- `tests/contract/test_repository_integrity.py` — ficheros esperados en `git ls-files`, sin CRLF, ignorados
  previstos, `.gitignore` anclado (anadido tras la auditoria de fases).

## Criterio de aceptacion
`make check` verde; arbol identico a §B; PROJECT_STATE completo; ADR-0001 con formato completo; sin
logica de negocio; informe de validacion emitido con estado WAITING_FOR_USER_VALIDATION.

## Riesgos
Sobre-ingenieria. Mitigacion: nada que F02 no vaya a usar.

## Que habilita
F02 (registro de parametros) y F03 (inventario del corpus) pueden empezar el mismo dia.
