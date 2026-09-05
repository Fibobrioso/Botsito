# knowledge/corpus/ — tres regimenes

| Fichero o carpeta | Que es | Regimen |
|---|---|---|
| `fuentes.yaml` | lo que DEBE haber en el corpus (videos con id de Drive, carpetas con papel) | manual, versionado |
| `manifest.yaml` | lo que HAY en disco (hash, duracion, huecos de fotogramas heredados) | GENERADO por `corpus inventory`, regenerable |
| `glosario_asr.yaml` | vocabulario del motor y correcciones del ASR con ejemplo real | manual, versionado; cada edicion cambia la version y obliga a `corpus glossary apply` |
| `transcripciones/<id>.yaml` | un manifiesto por transcripcion cruda (motor, corte, hashes, huecos, senales) | INMUTABLE: hook y `knowledge validate` (historial de git); una retranscripcion es otro manifiesto con `reemplaza_a` |

Los ficheros pesados (WAV, fragmentos, `cruda.jsonl`, `corregida.jsonl`) viven en
`data/transcripciones/` (ignorado por git) y se verifican por hash contra el manifiesto. La
corregida es regenerable (`cruda + glosario`) y no lleva hash: `knowledge validate` la recomputa.
