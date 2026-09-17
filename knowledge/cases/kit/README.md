# knowledge/cases/kit/ — kit de elicitacion (F10, ADR-0011)

Todo lo que se lleva a una sesion con el trader, generado de forma determinista con
`botsito kit build --sesion AAAA-MM-DD-sesion-NN --seed N` a partir del repo y de `data/`.
Regimen: versionado con `Fuente:` en cada commit (como todo `knowledge/cases/`).

| Fichero | Que es | Regimen |
|---|---|---|
| `config.yaml` | datos de negocio del kit (simbolo, ventana del dia, sesiones, anclajes candidatos, etiquetas, particiones) | manual |
| `mapa_parametros.yaml` | parametro del registro -> temas de evidencia. **Solo eso desde F13**: las `opciones` las sostiene el registro y la `ambiguedad`, `ambiguedades.yaml` | manual |
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
`uv run botsito kit hoja` genera en la raiz del repositorio un `.docx`
con cada pregunta, su contexto, sus citas y una caja de respuesta, mas la tabla de etiquetado de
los casos `dev`. Se rellena a mano durante la sesion. No se versiona (esta en `.gitignore`): se
regenera cuando cambian el paquete o `contexto_preguntas.yaml`.

## Condicion previa de cada sesion
El trader confirma por escrito (registro F09, `medio: escrito`) que no ha operado ni
backtesteado los meses del paquete; si lo ha hecho, se anaden a `vistos.yaml` y se regenera.

Esa confirmacion se registra como `CONFIRM` sobre un objetivo de tipo `paquete` cuyo id es la
propia sesion (`--objetivo-tipo paquete --objetivo-id <sesion>`). Si el trader dice que si los ha
visto, es un `REJECT` sobre el mismo objetivo: el mes se anade a `vistos.yaml` citando ese
`fb-...` en `fuente`, y el paquete se regenera desde cero.

**Cada entrada de `vistos.yaml` lleva `visto_el`** (desde el 2026-09-17): el dia a mas tardar en
que el trader lo habia visto. Cuenta para un paquete solo si es igual o anterior a la fecha de su
SESION, la del nombre `AAAA-MM-DD-sesion-NN`, que es el dia en que el trader etiqueta. Asi un mes
visto despues no borra lo que un paquete anterior pregunto, `kit build` no puede sortearlo en un
paquete posterior y `knowledge validate` denuncia un paquete escrito que lo tenga.

**Para la sesion 2** (informe `docs/validation/MESES-VISTOS.md`): se etiqueta sobre el paquete de la
sesion 1, y solo son ciegos sus `dev` de junio. Los `dev` de mayo ya no lo son: el trader entrego el
backtest de mayo el 2026-09-11, y `kit kappa` lo avisa al comparar cualquier ronda posterior que los
incluya. La confirmacion escrita de ESTA sesion tiene que decir expresamente que no ha backtesteado
junio: la de la sesion 1 decia que lo haria.

## Si cambia la fecha de la sesion
    uv run --no-sync python scripts/mover_sesion.py --a AAAA-MM-DD
    uv run botsito kit hoja

El script reutiliza el seed del paquete que ya existe y despues comprueba que los casos, el
reparto y las preguntas son los mismos que antes; si no lo son, restaura el paquete original y no
mueve nada. Se niega a mover una sesion que ya tenga registros de feedback.

A mano la trampa es el seed: `kit build` lo pide, el seed decide que dias caen en `dev` y cuales
quedan en holdout, y con otro seed el paquete sale con dias distintos sin aviso y sin que nada
falle. Cambiarlo solo tiene sentido si se quiere un sorteo nuevo a proposito.

Regenerar la hoja en Word es siempre lo ultimo, justo antes de imprimir.
