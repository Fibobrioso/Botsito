# knowledge/cases/holdout/ - particiones RESERVADAS. Prohibido leer desde spec/ y domain/ (guarda en tests, F14).

| Particion | Se abre en | Uso |
|---|---|---|
| `1/` | F26, sesion 2 con el trader | discrepancias y correccion |
| `2/` | una sola vez tras la correccion | cifra final de fidelidad |
| `3/` | fase 7 | correcciones de las sesiones mensuales |

Un holdout abierto queda quemado: no vuelve a usarse para medir.

## Que cuenta como ABRIRLO (ADR-0021)

Hasta el 2026-09-12 esta frase no decia que es abrir, y eso hizo falta el dia que ocurrio. Son dos
cosas, y solo estas dos:

1. **Leer sus etiquetas**: los `LABEL_CASE` de esos dias, o el detalle por operacion del backtest
   del trader sobre ellos (hora, direccion, entrada, stop, objetivo).
2. **Medir cualquier cifra del bot sobre esos dias**: fidelidad, aciertos, PnL simulado,
   sensibilidad. Aunque sea de pasada y aunque no se apunte.

**Ver el RESULTADO AGREGADO de esos dias no lo abre** -un PnL diario no contiene ninguna decision y
no se puede invertir para deducirlas- **pero si es una EXPOSICION y se declara**, el mismo dia, en
`docs/validation/HOLDOUT-EXPOSICIONES.md`: que se vio, que particiones toca, quien, y si quema.

## Quien autoriza, y con que

**Solo el usuario.** Y una apertura exige, antes de mirar nada:

- `docs/validation/PREREGISTRO.md` commiteado con los umbrales. Un umbral no se relaja despues de
  ver el resultado: para eso se pre-registra.
- un ADR que diga que se va a medir, sobre que particion y contra que umbral.

## Reparticionar

Cambiar los cupos de `knowledge/cases/kit/config.yaml` es legitimo **mientras no exista ningun
`LABEL_CASE`**; a partir de ahi, no. En los dos casos exige un ADR que diga por que.

## Estado hoy (2026-09-12)

Junio quedo descartado, asi que el universo es mayo: 19 dias, **6 `dev`** y **13 holdout** (6/4/3),
cuando `config.yaml` fue dimensionado para 40 dias con 16/8/8/8. Y hay **una exposicion declarada**:
el 2026-09-11 se vio el calendario de PnL diario de todo mayo. No quema (ADR-0021 §5), pero F26 la
cita en su informe.
