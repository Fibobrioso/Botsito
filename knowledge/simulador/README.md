# knowledge/simulador/

La configuracion del SIMULADOR: lo que el modelo de llenado (ADR-0051, PROPUESTO) y el broker
simulado (ADR-0052, PROPUESTO) pueden elegir, en datos y no en codigo (ADR-0002). Nada de aqui
es un parametro de la estrategia del trader: eso vive en `knowledge/spec/parametros.yaml`. Los
perfiles de cuenta viven en `knowledge/cuentas/`.

| Fichero | Contenido |
|---|---|
| `llenado.yaml` | si una limite se llena al toque o al pasar el nivel; el deslizamiento fijo en puntos con su motivo; el spread supuesto por hora LOCAL para los minutos sin ticks, con la fuente de la que se midio (`scripts/ticks_spread.py` sobre los datasets de ticks de construccion) |

Lo lee `src/botsito/engine/simulador_config.py`, con lectura estricta: claves cerradas y sin
valores por defecto. Regimen de cambio: versionado; cada cambio de valor cita su medida o su ADR
en el mensaje del commit.
