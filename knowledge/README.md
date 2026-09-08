# knowledge/
La base de conocimiento del proyecto. Son DATOS versionados, no codigo, y se validan en CI.

| Carpeta | Contenido | Regimen de cambio |
|---|---|---|
| corpus/ | `fuentes.yaml` y `manifest.yaml` (F03), `glosario_asr.yaml` (F04, manual), `transcripciones/<id>.yaml` (F04, INMUTABLE por historial), `fotogramas_obligatorios.yaml` (F05, manual) y `fotogramas/<id>.yaml` (F05, INMUTABLE por historial) | mixto: ver knowledge/corpus/README.md |
| evidence/ | EvidenceItem en YAML, uno por fichero, con cita verificable por maquina (F06, F07: cita localizada en la cruda `transcripcion` o fotograma `fr-*` real); `_temas.yaml` (taxonomia, manual) y `_contradicciones.yaml` (generado) | INMUTABLE tras commit (items); manual (`_temas.yaml`); generado (`_contradicciones.yaml`) |
| _proposals/ | propuestas de evidencia (F07, ADR-0009): prompt, modelo, contexto, salida y decision humana por item; `PROMPT.md` canonico | manual, versionado; la salida queda sellada tras `propose --check` y solo cambian los campos de decision |
| feedback/ | FeedbackRecord del trader, por sesion (F09); `ambiguedad` se valida contra `spec/ambiguedades.yaml` y `t1` contra la duracion de la grabacion (F10) | SOLO ANADIR |
| spec/ | parametros.yaml (F02, ADR-0002/0004: LA puerta de los parametros; 24 de estrategia en UNKNOWN desde F10), ambiguedades.yaml (F10, ADR-0011: A-1..A-12 legibles por maquina), strategy_spec.yaml y glossary.yaml (F11) | versionado; cada commit cita `Fuente:` (evidence-id, feedback-id o ADR) |
| cases/kit/ | kit de elicitacion (F10, ADR-0011): `config.yaml`, `mapa_parametros.yaml`, `vistos.yaml` (manuales) y un paquete por sesion (`cuestionario.yaml`, `ventanas.yaml`, `particiones.yaml`, `hoja_trader.md`, generados con `botsito kit build`) | versionado con cita; `particiones.yaml` commiteado ANTES de la sesion (guardia de ancestro) |
| cases/dev/ | casos ejecutables usados para cerrar reglas (F14) | versionado con cita |
| cases/holdout/{1,2,3}/ | tres particiones reservadas (F26, cifra final, fase 7): src/botsito/spec y src/botsito/domain NO pueden leerlas; cada una se abre una sola vez | versionado con cita |
| cases/fixtures/ | instantaneas OHLC/ticks de cada caso, con hash | inmutable |

Ver ADR-0001.

Consultar (F08, ADR-0010; lexico, determinista, toda linea con fuente, nada se escribe):
`botsito kb find "break even" [--video v4] [--tema stop] [--desde 0:05:00 --hasta 0:15:00]
[--solo evidencia|cruda] [--frase] [--prefijo] [--top N] [--contexto] [--json]` y
`botsito kb at --video v4 --t 0:44:56 [--margen-s 10] [--contexto] [--json]`. Sin `data/` responde
solo con evidencia (aviso en stderr). `0,75` = `0.75`; `limite` = `límite`; `1:3` no casa con el
`1.3` del ASR (fallo lexico conocido).
