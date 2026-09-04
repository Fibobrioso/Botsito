# FUNCTIONALITY VALIDATION REPORT

**Funcionalidad:** F03 · corpus-inventory
**Rama:** `feature/F03-corpus-inventory`
**Objetivo:** manifiesto determinista del corpus (hash, papel, duracion, resolucion, audio),
verificado contra un registro de fuentes esperadas, con los huecos de cobertura de los fotogramas
heredados. Es el ancla de todas las citas posteriores (F04-F07).

## Que se construyo
- `knowledge/corpus/fuentes.yaml` (escrito a mano): los 4 videos con id de Drive, tamano y fecha;
  las dos carpetas con su papel (`heredado_v2`, `material_adicional`); umbral de hueco 180 s.
- `src/botsito/corpus/inventario.py`: carga y validacion de fuentes; SHA-256 en streaming; ffprobe
  por subproceso (duracion, resolucion, fps, audio); clasificacion por papel; huecos en los
  `index.txt` heredados (incluye tramo inicial y final); manifiesto determinista sin fechas;
  validacion de esquema y coherencia; comprobacion contra disco.
- CLI: `botsito corpus inventory [--sin-hash]`, `botsito corpus check [--hashes]`;
  `botsito knowledge validate` valida tambien el manifiesto.
- `knowledge/corpus/manifest.yaml` GENERADO: 4 videos, 477 ficheros heredados (117,6 MB), 17 de
  material adicional (2,0 MB), 4 indices heredados con sus huecos.
- Fixture `tests/fixtures/clip_2s.mp4` (2 s, 320x180, 10 fps, audio) generado con ffmpeg.

## Lo que el manifiesto dice del corpus (hechos)
| Video | Duracion | Resolucion | fps | Audio | Bytes = Drive |
|---|---|---|---|---|---|
| v1 (2026-08-20) | 0h 29m 12s | 1920x1080 | 60 | si | si |
| v2 (2026-08-03) | 1h 08m 54s | 1898x1074 | 30 | si | si |
| v3 (2026-08-06) | 1h 17m 56s | 1762x884 | 30 | si | si |
| v4 (2026-08-30) | 1h 33m 37s | 1778x952 | 30 | si | si |

Las duraciones coinciden con las marcas finales de las transcripciones heredadas. Los originales
tienen mas resolucion que las capturas heredadas (1200 px): F05 debe extraer a resolucion nativa.

Huecos > 3 min sin fotograma heredado: v1 ninguno (29 fotogramas); v2 tres (4:03-8:02, 8:49-12:27,
23:19-27:57); v3 ocho, el mayor 12:27-23:49 (11,4 min); v4 uno (30:13-33:20). Son los tramos que
F05 reextrae a 1 fps.

Material adicional: `backtesting-analytics ENERO 2026.xlsx`, `backtesting-analytics AGOSTO 2026.xlsx`
(exportaciones de FXReplay pedidas en el informe de investigacion) y 15 capturas de balance
(2026-09-03). Inventariadas; su contenido se lee en F07 y F26.

## Archivos creados
```
knowledge/corpus/fuentes.yaml  knowledge/corpus/manifest.yaml
src/botsito/corpus/inventario.py
tests/unit/test_inventario.py  tests/fixtures/clip_2s.mp4  tests/fixtures/README.md
docs/plan/features/F03-corpus-inventory.md  docs/validation/F03-corpus-inventory.md
```

## Archivos modificados
`src/botsito/cli.py` (subcomando corpus, knowledge validate), `tests/unit/test_tree.py`,
`PROJECT_STATE.md`.

## Decisiones tomadas
- **El corpus vive en `corpus/Estrategia del trader/`** con los nombres originales del usuario. Se
  movio desde la raiz del repositorio porque solo `corpus/` esta ignorado por git: 14 GB en la raiz
  eran un `git add` de distancia de entrar al historial.
- **`_procesado` se inventaria como `heredado_v2`** sin renombrar: la ruta esperada esta en
  `fuentes.yaml`, no en el codigo.
- **Sin fecha de generacion en el manifiesto** para que regenerar no produzca diff; la version de
  ffprobe si se registra porque afecta a la duracion medida.
- **ffmpeg instalado con winget** (`Gyan.FFmpeg` 9.0.1) por peticion del usuario.
- **`corpus check` compara tamanos por defecto y hashes con `--hashes`** (25 s sobre 14 GB en esta
  maquina).

## Como ejecutarlo
```
make check
uv run botsito corpus inventory        # regenera el manifiesto (sin diff si el disco no cambio)
uv run botsito corpus check --hashes   # verifica el corpus contra el manifiesto
uv run botsito knowledge validate
```

## Como probarlo
- Cambiar un byte de `fuentes.yaml` (p. ej. los bytes de v1) → `corpus inventory` falla nombrando
  el video. Borrar una captura de `Material adicional` → `corpus check` la nombra.
- Regenerar el manifiesto y `git diff`: vacio.

## Tests ejecutados
`make check` en `feature/F03-corpus-inventory`, Windows 11, ffprobe 9.0.1. `corpus check --hashes`
sobre el corpus real: OK.

## Resultados
- ruff, mypy strict (38 ficheros), 3 contratos KEPT.
- pytest: 76 passed (74 funciones); el test de ffprobe se salta con aviso si no hay ffprobe.
- `state check`, `config validate`, `knowledge validate` (registro + manifiesto): OK.
- Manifiesto regenerado dos veces: identico.
- CI GitHub Actions (ubuntu-latest): verde, run 33890615366 (test de ffprobe omitido con aviso).

## Que deberia observar el usuario
`knowledge/corpus/manifest.yaml` con los 4 videos y sus hashes; `corpus check --hashes` OK;
`git status` limpio aunque `corpus/` contenga 14 GB.

## Que casos funcionan
Todo el alcance del brief.

## Que casos todavia no funcionan
- Los huecos se calculan solo sobre los indices heredados; la cobertura nueva la produce F05.
- El manifiesto es regenerable (no inmutable): la inmutabilidad contra el historial de git se
  introduce con los manifiestos de datos (F15) segun la seccion H.

## Limitaciones
`ffprobe` debe estar en PATH; en CI (ubuntu) no lo esta y el test de video se salta con aviso.
Anadir `ffmpeg` al workflow es tarea de F04, que lo necesita de verdad.

## Riesgos
Perdida del unico ejemplar local del corpus: `fuentes.yaml` guarda los ids de Drive para
re-descargar y el manifiesto los hashes para verificar. Copia de seguridad fuera de la maquina:
tarea del usuario.

## Impacto sobre funcionalidades anteriores
Ninguno funcional. `knowledge validate` ahora tambien valida el manifiesto.

## Estado
WAITING_FOR_USER_VALIDATION
