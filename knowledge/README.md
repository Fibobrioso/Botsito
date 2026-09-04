# knowledge/
La base de conocimiento del proyecto. Son DATOS versionados, no codigo, y se validan en CI.

| Carpeta | Contenido | Regimen de cambio |
|---|---|---|
| corpus/ | manifiesto de videos y derivados con hash, duracion y huecos (F03) | regenerable |
| evidence/ | EvidenceItem en YAML, uno por fichero, con cita verificable (F06) | INMUTABLE tras commit |
| feedback/ | FeedbackRecord del trader, por sesion (F09) | SOLO ANADIR |
| spec/ | strategy_spec.yaml, glossary.yaml (F11) | versionado; cada cambio cita evidence-id o feedback-id |
| cases/dev/ | casos ejecutables usados para cerrar reglas (F14) | versionado con cita |
| cases/holdout/ | casos reservados: src/botsito/spec y src/botsito/domain NO pueden leerlos | versionado con cita |
| cases/fixtures/ | instantaneas OHLC/ticks de cada caso, con hash | inmutable |

Ver ADR-0001.
