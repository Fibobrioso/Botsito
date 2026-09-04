# knowledge/
La base de conocimiento del proyecto. Son DATOS versionados, no codigo, y se validan en CI.

| Carpeta | Contenido | Regimen de cambio |
|---|---|---|
| corpus/ | manifiesto de videos y derivados con hash, duracion y huecos (F03) | regenerable |
| evidence/ | EvidenceItem en YAML, uno por fichero, con cita verificable (F06) | INMUTABLE tras commit |
| feedback/ | FeedbackRecord del trader, por sesion (F09) | SOLO ANADIR |
| spec/ | parametros.yaml (F02, ADR-0002/0004: LA puerta de los parametros), strategy_spec.yaml y glossary.yaml (F11) | versionado; cada commit cita `Fuente:` (evidence-id, feedback-id o ADR) |
| cases/dev/ | casos ejecutables usados para cerrar reglas (F14) | versionado con cita |
| cases/holdout/{1,2,3}/ | tres particiones reservadas (F26, cifra final, fase 7): src/botsito/spec y src/botsito/domain NO pueden leerlas; cada una se abre una sola vez | versionado con cita |
| cases/fixtures/ | instantaneas OHLC/ticks de cada caso, con hash | inmutable |

Ver ADR-0001.
