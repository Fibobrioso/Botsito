# knowledge/cases/kit/ — kit de elicitacion (F10, ADR-0011)

Todo lo que se lleva a una sesion con el trader, generado de forma determinista con
`botsito kit build --sesion AAAA-MM-DD-sesion-NN --seed N` a partir del repo y de `data/`.
Regimen: versionado con `Fuente:` en cada commit (como todo `knowledge/cases/`).

| Fichero | Que es | Regimen |
|---|---|---|
| `config.yaml` | datos de negocio del kit (simbolo, ventana del dia, sesiones, anclajes candidatos, etiquetas, particiones) | manual |
| `mapa_parametros.yaml` | parametro del registro -> temas de evidencia, ambiguedad y opciones cerradas | manual |
| `vistos.yaml` | meses y dias que el trader ya vio (fuera del universo de ventanas) | manual |
| `<sesion>/cuestionario.yaml` | una pregunta por origen (parametro UNKNOWN, ambiguedad, contradiccion) con sus casos `ev-*` | generado; `kit check` lo recompone byte a byte |
| `<sesion>/ventanas.yaml` | los casos: dia, `dataset_id`, ventana UTC, velas, sha256, limites H4 por anclaje; y los dias excluidos con motivo | generado |
| `<sesion>/particiones.yaml` | seed y asignacion `dev` / `holdout-1` / `holdout-2` / `holdout-3`; commiteado ANTES de la sesion (guardia de ancestro en `knowledge validate`) | generado |
| `contexto_preguntas.yaml` | por que preguntamos cada cosa y que forma tiene una respuesta util, en lenguaje del trader (con acentos: lo lee una persona) | manual |
| `<sesion>/hoja_trader.md` | lo que el consultor lleva a la sesion: preguntas (bloqueantes primero) y solo los casos `dev` con las dos rejillas H4 | generado |

## Gramatica de la etiqueta (`LABEL_CASE`, `valor_resultante`)
Una decision por SESION del caso, separadas por `;`. Obligatorio `<sesion>: <decision>`; el
resto es opcional y llega a F14 tal cual:

```
07-11: venta@08:37 e=1.15364 sl=1.15420 tp=1.15200; 11-15: no_trade
```

Deben aparecer TODAS las sesiones de `config.yaml`, cada una una vez; `@HH:MM` en 00-23:00-59; una
clave `k=v` no se repite. `<sesion>` es un `nombre` de `config.yaml` (`07-11`, `11-15`); `<decision>` una de `etiquetas`
(`compra`, `venta`, `no_trade`); `@HH:MM` hora de entrada en `huso_operativa`; `e=`, `sl=`,
`tp=` precios; cualquier otro `clave=valor` se conserva. Cada sesion aparece una sola vez. El
objetivo del registro es `{tipo: caso, id: caso-eurusd-AAAA-MM-DD}`. `botsito kit kappa
--sesion-a --sesion-b` lee los `LABEL_CASE` activos de dos sesiones y calcula la kappa de Cohen
por unidad (caso, sesion).

## Hoja en Word para la sesion
`uv run --no-sync python scripts/hoja_sesion_docx.py` genera en la raiz del repositorio un `.docx`
con cada pregunta, su contexto, sus citas y una caja de respuesta, mas la tabla de etiquetado de
los casos `dev`. Se rellena a mano durante la sesion. No se versiona (esta en `.gitignore`): se
regenera cuando cambian el paquete o `contexto_preguntas.yaml`.

## Condicion previa de cada sesion
El trader confirma por escrito (registro F09, `medio: escrito`) que no ha operado ni
backtesteado los meses del paquete; si lo ha hecho, se anaden a `vistos.yaml` y se regenera.
