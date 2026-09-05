# knowledge/corpus/ — tres regimenes

| Fichero o carpeta | Que es | Regimen |
|---|---|---|
| `fuentes.yaml` | lo que DEBE haber en el corpus (videos con id de Drive, carpetas con papel) | manual, versionado |
| `manifest.yaml` | lo que HAY en disco (hash, duracion, huecos de fotogramas heredados) | GENERADO por `corpus inventory`, regenerable |
| `glosario_asr.yaml` | vocabulario del motor y correcciones del ASR con ejemplo real | manual, versionado; cada edicion cambia la version y obliga a `corpus glossary apply` |
| `transcripciones/<id>.yaml` | un manifiesto por transcripcion cruda (motor, corte, hashes, huecos, senales) | INMUTABLE: hook y `knowledge validate` (historial de git); una retranscripcion es otro manifiesto con `reemplaza_a` |
| `fotogramas_obligatorios.yaml` | instantes que deben existir con precision de fotograma (motivo, marca heredada) | manual, versionado; `knowledge validate` exige que cada uno este en la extraccion activa |
| `fotogramas/<id>.yaml` | un manifiesto por extraccion de fotogramas (build de ffmpeg, regla de seleccion, `sha256_index`, huecos sobre `pts`, extra) | INMUTABLE, exactamente uno activo por video; otra extraccion es otro manifiesto con `reemplaza_a` (ADR-0008) |

Los ficheros pesados (WAV, fragmentos, `cruda.jsonl`, `corregida.jsonl`) viven en
`data/transcripciones/` (ignorado por git) y se verifican por hash contra el manifiesto. La
corregida es regenerable (`cruda + glosario`) y no lleva hash: `knowledge validate` la recomputa.
Los fotogramas (PNG a 1 fps, `index.jsonl`) viven en `data/fotogramas/<video>/png-1fps/`
(~7 GiB, regenerables en ~10 min con `corpus frames extract`); `knowledge validate` compara el
sha256 de `index.jsonl` y recomputa recuentos y huecos; `corpus frames check` verifica ademas por
hash los fotogramas extra y una muestra de 20 regulares. Una cita de pantalla es `fr-<id>/<t_ms>`.
