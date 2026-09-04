# tests/
- `unit/`: comportamiento de cada modulo, con `tmp_path`; los pocos tests sobre el repo real
  (`repo` fixture) comprueban que los ficheros versionados son coherentes hoy.
- `contract/`: contratos estructurales (importaciones, arbol, literales de negocio, integridad del
  indice, historial de git de evidencia y feedback).
- `golden/`, `regression/`, `differential/`, `integration/`: desde F14 (ver sus README).
- `fixtures/`: ficheros pequenos usados por los tests (`clip_2s.mp4`).

`tests/` es un paquete (mypy strict lo cubre). `make check` ejecuta todo; `PYTHONHASHSEED=0`.
