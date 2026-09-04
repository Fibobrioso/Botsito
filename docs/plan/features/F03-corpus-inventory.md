# F03 · corpus-inventory

**Rama:** `feature/F03-corpus-inventory` · **Fase:** 1 · **Depende de:** F01

## Objetivo
Manifiesto del corpus: cada fichero de `corpus/` con ruta, tamano, hash SHA-256, papel (video
original, heredado de Bot v2, material adicional) y, para los videos, duracion real (ffprobe),
resolucion, fps y pista de audio. Los cuatro videos se verifican contra un registro de fuentes
esperadas (id de Drive y tamano). Se calculan los huecos de cobertura de los fotogramas heredados.

## Alcance cerrado (que SI)
- `knowledge/corpus/fuentes.yaml`: registro escrito a mano de las fuentes esperadas (id de Drive,
  titulo, bytes, papel). Es el ancla para re-descargar y verificar.
- `src/botsito/corpus/inventario.py`: recorrido determinista de `corpus/`, hash en streaming,
  ffprobe por subproceso, clasificacion por papel, huecos > umbral en los `index.txt` heredados.
- `botsito corpus inventory` genera `knowledge/corpus/manifest.yaml` (determinista: sin fechas;
  incluye version de ffprobe). `botsito corpus check` compara el manifiesto con el disco (tamanos,
  y hashes con `--hashes`).
- `botsito knowledge validate` valida tambien el manifiesto (esquema, referencias a fuentes).
- Fixture `tests/fixtures/clip_2s.mp4` (2 s, 320x180, con audio) generado con ffmpeg.

## Fuera de alcance (que NO)
Transcribir (F04), extraer fotogramas (F05), leer el contenido de Excel o imagenes (F07/F26),
copiar o modificar el corpus.

## Entradas
`corpus/Estrategia del trader/` con los 4 videos, `_procesado/` (heredado) y
`Material adicional de su operativa/` (2 xlsx de FXReplay, 15 capturas de balance). ffprobe 9.

## Salidas (ficheros)
`knowledge/corpus/fuentes.yaml`, `knowledge/corpus/manifest.yaml`, `src/botsito/corpus/inventario.py`,
`src/botsito/cli.py` (subcomando corpus), tests, `docs/validation/F03-corpus-inventory.md`.

## Tests
- Unit: huecos sobre indices sinteticos; clasificacion por papel; esquema de fuentes y manifiesto;
  hash en streaming = hashlib; determinismo (dos ejecuciones identicas); fuente esperada ausente o
  con tamano distinto → error.
- Integration: ffprobe sobre `clip_2s.mp4` (duracion ~2 s, 320x180, audio presente); si ffprobe no
  esta en PATH el test se salta con aviso (nunca falla en silencio).
- Regresion: el manifiesto versionado valida y sus 4 videos coinciden con `fuentes.yaml`.

## Criterio de aceptacion
`make check` verde; `manifest.yaml` regenerable sin diff; los cuatro videos con hash, duracion y
resolucion; tamanos identicos a Drive; huecos > 3 min listados por video heredado; informe con
estado WAITING_FOR_USER_VALIDATION.

## Riesgos
Hash de 14 GB tarda minutos: se hace una vez y `corpus check` sin `--hashes` compara solo tamanos.
El corpus vive fuera de git: `fuentes.yaml` guarda id de Drive y bytes para re-descargar.

## Que habilita
F04 (transcripcion) y F05 (fotogramas) citan `video_id` y duracion del manifiesto; F06 valida
cada cita contra esa duracion.
