# tests/
- `unit/`: comportamiento de cada modulo, con `tmp_path`; los pocos tests sobre el repo real
  (`repo` fixture) comprueban que los ficheros versionados son coherentes hoy.
- `contract/`: contratos estructurales (importaciones, arbol, literales de negocio, integridad del
  indice, historial de git de evidencia, feedback y manifiestos de datos).
- `golden/`: salidas esperadas revisadas a mano (`ohlc/`: H4 del 2026-07-02, F15). `regression/`,
  `differential/`, `integration/`: desde F14 (ver sus README).
- `fixtures/`: ficheros pequenos usados por los tests (`clip_2s.mp4`; `ohlc/`: dias reales de M1
  en formato bi5 con sha256 en su README).

`tests/` es un paquete (mypy strict lo cubre). `make check` ejecuta todo; `PYTHONHASHSEED=0`.
