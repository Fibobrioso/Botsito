# tests/
- `unit/`: comportamiento de cada modulo, con `tmp_path`; los pocos tests sobre el repo real
  (`repo` fixture) comprueban que los ficheros versionados son coherentes hoy.
- `contract/`: contratos estructurales (importaciones, arbol, literales de negocio, integridad del
  indice, historial de git de evidencia, feedback, manifiestos de datos, de transcripciones y de
  fotogramas; `faster_whisper` solo importable desde `corpus/motor_whisper.py`; argv `ffmpeg`
  solo en `corpus/{audio,inventario,fotogramas}.py`).
- `golden/`: salidas esperadas revisadas a mano (`ohlc/`: H4 del 2026-07-02, F15). `integration/`: extraccion
  real con ffmpeg sobre el clip fixture y clips sinteticos (F05). `regression/`, `differential/`:
  desde F14 (ver sus README).
- `fixtures/`: ficheros pequenos usados por los tests (`clip_2s.mp4`; `ohlc/`: dias reales de M1
  en formato bi5 con sha256 en su README; `audio/tono_silencio_tono_10s.wav`: tono, silencio
  3-5 s y tono, para el corte por silencios de F04). Los tests que necesitan ffmpeg se saltan sin
  el en local y FALLAN en CI (`BOTSITO_EXIGE_FFPROBE=1`); ninguno carga el modelo Whisper
  (`MotorFalso`).

`tests/` es un paquete (mypy strict lo cubre). `make check` ejecuta todo; `PYTHONHASHSEED=0`.
