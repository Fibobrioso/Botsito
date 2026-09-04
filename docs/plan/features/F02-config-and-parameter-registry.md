# F02 · config-and-parameter-registry

**Rama:** `feature/F02-config-and-parameter-registry` · **Fase:** 0 · **Depende de:** F01

## Objetivo
Un solo lugar por el que pasa cada parametro de negocio, con valor, tipo, fuente (id de evidencia,
de feedback o de decision) y estado `CONFIRMED / DEFAULT_AMBIGUOUS / UNKNOWN`. El registro nace
VACIO de valores: los valores llegan en F11 citando evidencia.

## Alcance cerrado (que SI)
- Tipos de valor en `domain/valores.py`: `Fraccion` y `Porcentaje`, sobre `Decimal`, no
  intercambiables; conversion explicita `Porcentaje.como_fraccion()`. Sin `float`.
- Registro en `config/registro.py`: modelo `Parametro`, `Fuente`, `Estado`; cargador YAML de
  `knowledge/spec/parametros.yaml`; `obtener(nombre)`:
  - `UNKNOWN` → `ParametroDesconocidoError` siempre.
  - `DEFAULT_AMBIGUOUS` → solo si `ambiguedad_id` esta declarado; la lectura se anota en el registro
    de lecturas (`lecturas_ambiguas()`), para que el journal la recoja (F23).
  - Sin fuente → error de carga. Duplicado → error de carga. Fuera de rango → error de carga.
- Ajustes de entorno en `config/ajustes.py`: carga `config/settings*.toml`; solo secciones
  `[entorno]` y `[rutas]`; cualquier clave que coincida con un nombre de parametro del registro o una
  seccion desconocida es error (una sola puerta).
- Test de literales de negocio rellenado (0,75 · 0,5 · 0,25 · 0,40 · 0,45 · 07:00 · 11:00 · 15:00 ·
  1:3 · 2000 · EURUSD) con regex de frontera, sobre `src/botsito/` excluyendo `config/` y docstrings.
- `state check` ampliado: recuento de tests declarado = tests reales (AST de `tests/`); `Last Stable
  Commit` = commit del ultimo tag `stable/*`; toda funcionalidad en "Completed Features" tiene informe
  en `docs/validation/`.
- ruff: regla de `encoding` obligatorio (`PLW1514`).
- Decision sobre el framework pre-commit (ADR-0003): se retira `.pre-commit-config.yaml`; los hooks
  son la copia de `scripts/git-hooks/`.
- `botsito.config` entra en los contratos de importacion: `domain` no puede importarlo.

## Fuera de alcance (que NO)
Ningun valor de parametro real. Ninguna regla. Ninguna evidencia. Ningun parametro del EA (MQL5).

## Entradas
MASTER_PLAN F02 y seccion H (filas F02); ADR-0001.

## Salidas (ficheros)
`src/botsito/domain/valores.py`, `src/botsito/config/{__init__,registro,ajustes}.py`,
`knowledge/spec/parametros.yaml` (vacio, con esquema documentado), `docs/adr/0002-*.md`,
`docs/adr/0003-*.md`, tests unit y contract, `docs/validation/F02-*.md`.

## Tests
- Unit `test_valores.py`: Fraccion/Porcentaje no se mezclan; conversion explicita; sin float; Decimal exacto.
- Unit `test_registro.py`: carga valida; sin fuente; duplicado; fuera de rango; UNKNOWN falla;
  DEFAULT_AMBIGUOUS con y sin ambiguedad declarada; registro de lecturas.
- Unit `test_ajustes.py`: secciones permitidas; clave que colisiona con el registro falla.
- Unit `test_cli.py` ampliado: recuento de tests, tag estable, informes de validacion.
- Contract `test_no_business_literals.py` con la lista real; contract de importacion con `config`.
- Property (hypothesis): Decimal de ida y vuelta por YAML sin perdida.

## Criterio de aceptacion
`make check` verde; registro vacio de valores; leer `UNKNOWN` falla; `Porcentaje` y `Fraccion` no
son intercambiables por tipo; `settings.toml` no admite claves del registro; `state check` detecta
un recuento de tests falso y un commit estable que no coincide con el tag; ADR-0002 y ADR-0003;
informe con estado WAITING_FOR_USER_VALIDATION.

## Riesgos
Sobre-disenar el registro antes de tener valores. Mitigacion: solo los campos que la seccion H
exige; nada de jerarquias ni perfiles.

## Que habilita
F11 (StrategySpec) tiene donde poner los valores con procedencia; F18-F22 leen parametros por una
sola puerta; F28 exporta desde el registro.
