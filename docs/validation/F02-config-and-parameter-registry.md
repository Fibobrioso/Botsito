# FUNCTIONALITY VALIDATION REPORT

**Funcionalidad:** F02 · config-and-parameter-registry
**Rama:** `feature/F02-config-and-parameter-registry`
**Objetivo:** una sola puerta por la que pasa cada parametro de negocio, con valor, tipo, fuente y
estado; lectura estricta; tipos de valor no intercambiables; `state check` que detecta un estado
desactualizado. Registro vacio de valores hasta F11.

## Que se construyo
- `src/botsito/domain/valores.py`: `Fraccion` y `Porcentaje` sobre `Decimal`. No se suman ni se
  comparan entre si (TypeError); conversion explicita `como_fraccion()` / `como_porcentaje()`;
  `float` y `bool` rechazados; inmutables.
- `src/botsito/config/registro.py`: `Parametro` (nombre, tipo, unidad, descripcion, estado, valor,
  fuente, ambiguedad_id, minimo, maximo), `Fuente` (evidence | feedback | decision), `Estado`
  (`CONFIRMED | DEFAULT_AMBIGUOUS | UNKNOWN`), `cargar_registro()` con validacion completa y
  `Registro.obtener()`: `UNKNOWN` falla siempre; `DEFAULT_AMBIGUOUS` exige `ambiguedad_id` y la
  lectura queda anotada en `lecturas_ambiguas()` para el journal (F23).
- `src/botsito/config/ajustes.py`: solo `[entorno]` y `[rutas]` con claves conocidas; una clave que
  coincida con un nombre del registro es error (una sola puerta).
- `knowledge/spec/parametros.yaml`: esquema documentado, lista vacia.
- `botsito state check` ampliado: rama, recuento de funciones de test (AST), `Last Stable Commit`
  contra el ultimo tag `stable/*`, informe de validacion por funcionalidad completada.
- `botsito knowledge validate` valida el registro.
- `tests/contract/test_no_business_literals.py` con la lista real (0,75 · 0,5 · 0,25 · 0,40 · 0,45 ·
  2000 · 07:00/11:00/15:00 · 1:3 · EURUSD) por AST, ignorando docstrings y `config/`; incluye un test
  que demuestra que el detector detecta.
- Contratos: `domain` no puede importar `config` (import-linter + AST); `config` en la capa de
  conocimiento/datos.
- ruff en modo preview con `PLW1514` (encoding obligatorio). ADR-0002 y ADR-0003.
  `.pre-commit-config.yaml` retirado (ADR-0003).

## Archivos creados
```
src/botsito/domain/valores.py  src/botsito/config/{__init__,registro,ajustes}.py
knowledge/spec/parametros.yaml
tests/unit/{test_valores,test_registro,test_ajustes}.py
docs/plan/features/F02-config-and-parameter-registry.md
docs/adr/0002-registro-de-parametros-una-sola-puerta.md
docs/adr/0003-hooks-copiados-sin-framework-pre-commit.md
docs/validation/F02-config-and-parameter-registry.md
```

## Archivos modificados
`src/botsito/cli.py` (state check ampliado, knowledge validate real), `tests/unit/test_cli.py`,
`tests/unit/test_tree.py`, `tests/contract/test_no_business_literals.py`,
`tests/contract/test_import_contracts.py`, `tests/contract/test_repository_integrity.py`,
`pyproject.toml` (contratos, ruff preview), `.gitignore` (`.hypothesis/`), `docs/adr/README.md`,
`PROJECT_STATE.md`. Eliminado: `.pre-commit-config.yaml`.

## Decisiones tomadas
- **Excepciones con sufijo `Error`** (`RegistroError`, `ParametroDesconocidoError`,
  `AmbiguedadNoDeclaradaError`, `AjustesError`) por la convencion N818 de ruff.
- **`state check` cuenta funciones de test, no casos de pytest.** Con una parametrizacion x3 hay 59
  funciones y 61 casos; PROJECT_STATE declara 59 y lo aclara. Se prefirio el AST porque no ejecuta
  nada y no depende de plugins.
- **Sin framework pre-commit** (ADR-0003): los hooks son la copia de `scripts/git-hooks/`.
- **Valores YAML entre comillas.** Un `0.75` sin comillas llega como float y se rechaza: evita que
  YAML convierta silenciosamente a binario.

## Como ejecutarlo
```
make sync
make check
uv run botsito knowledge validate
uv run botsito state check
```

## Como probarlo
- Anadir al YAML un parametro con `estado: UNKNOWN` y `valor: 3` → `knowledge validate` falla.
- Cambiar el `59` de "Tests Currently Passing" por otro numero → `state check` falla nombrando la
  diferencia (ocurrio de verdad durante la construccion: el estado decia 26).
- `Fraccion("0.5") + Porcentaje("50")` → `TypeError`.
- Anadir `stop = 0.75` a `config/settings.example.toml` bajo `[entorno]` → `test_ajustes` falla.
- Escribir `x = 0.75` en cualquier modulo fuera de `config/` → `test_no_business_literals` falla.

## Tests ejecutados
`make check` en `feature/F02-config-and-parameter-registry`, Windows 11, Python 3.12.10.

## Resultados
- ruff (preview, PLW1514): sin errores. mypy strict: 35 ficheros (src + tests), sin incidencias.
- import-linter: 3 contratos KEPT.
- pytest: 61 passed (59 funciones; property test con hypothesis incluido).
- `state check`: OK. `knowledge validate`: OK, registro con 0 parametros.
- CI GitHub Actions (ubuntu-latest): verde, run 33883045053.

## Que deberia observar el usuario
`make check` verde; `knowledge/spec/parametros.yaml` sin valores; `uv run botsito state check`
falla si se altera el recuento de tests o el commit estable; ADR-0002 y 0003 en el indice.

## Que casos funcionan
Todo el alcance del brief.

## Que casos todavia no funcionan
- El registro no tiene valores (por diseno: F11).
- La anotacion de lecturas ambiguas existe pero nadie la consume hasta el journal (F23).

## Limitaciones
`state check` no verifica el contenido de "Completed Phases" (se anade cuando se cierre la fase 0).

## Riesgos
Que F11 anada valores sin fuente: imposible por el cargador. Que alguien escriba un literal en
`config/`: el test excluye `config/` a proposito porque es el registro; revisar en cada informe.

## Impacto sobre funcionalidades anteriores
F01 intacta; `state check` es mas estricto y `PROJECT_STATE.md` se ajusto a lo que mide.

## Estado
WAITING_FOR_USER_VALIDATION
