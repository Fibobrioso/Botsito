# El camino de fidelidad (ADR-0036)

Aquí se reparte **material ETIQUETADO de un mes que el trader ya vio**. No es el kit, y la
diferencia no es de forma: el kit (`knowledge/cases/kit/`) es el camino del etiquetado **ciego** y
por construcción no sirve para esto (ADR-0034 §6).

## Qué es y qué NO es

| | |
|---|---|
| **Sí es** | un universo, un reparto fijado antes de leer ninguna etiqueta, y un ancla |
| **No es** | ciego. El trader ya vio estos días: por eso están etiquetados y por eso sirven |
| **No tiene** | cuestionario, hoja del trader, sesión ni fecha de reunión — no hay reunión |

## Lo que este camino puede prometer, y lo que no

**Puede prometer anterioridad demostrable**: que el reparto se fijó antes de leer ninguna etiqueta,
y lo comprueba una máquina (`cases/anterioridad.py`, emparejando por CASO).

**No puede prometer una cifra con potencia estadística.** El mínimo para F26 son **36 unidades
efectivas independientes** (`docs/validation/AUDITORIA-2026-09-13-ultracode.md` §6.1) y **nada
construible hoy lo alcanza**: los 14 días laborables de septiembre dan 28 unidades brutas y ~23
efectivas —potencia 0,50-0,68—, y ninguna combinación de mayo llega tampoco. Lo que sale de aquí es
una **cifra descriptiva con su intervalo**. Quien la cite como si midiera fidelidad con potencia
estará afirmando lo que no se probó.

Está escrito aquí, en `cases/fidelidad.py` y en ADR-0036 a propósito: es lo que impide que dentro de
seis meses alguien cite esa cifra como si midiera algo.

## Lo que se salta a propósito

El filtro de meses y días vistos de `vistos.yaml`. `universo()` recibe `meses_vistos=set()` y
`dias_vistos=set()`. **El kit no se toca**: su guardia sigue entera, y forzar septiembre por allí
habría exigido falsear la fecha de la sesión o desactivar ese filtro — dos formas de corromper un
mecanismo para reaprovechar código.

En cuanto ese filtro se salta, **`cobertura_material` pasa de adorno a ser el único filtro** entre el
universo y un día sin etiquetar. Por eso vive en `config.yaml`, con su motivo propio en `excluidos:`
y con la prohibición explícita de declarar días en vez de tramos.

## Nombres de partición propios, y con puerta

`fidelidad-dev`, `fidelidad-1`, `fidelidad-2`, `fidelidad-3`. No son los del kit porque los del kit
son **globales**: un `AUTORIZACION-<nombre>.md` por nombre y un mapa plano que tira el paquete, así
que mezclar estos días con los ciegos de mayo daría un cubo cuya cifra no se puede interpretar.

Pasan por la **misma puerta** (`cases/holdout.py`, ADR-0033). ADR-0034 separó dos cegueras: la **del
trader**, que septiembre ya no tiene, y **la nuestra**, que sigue intacta. Es la nuestra la que la
puerta protege.

> **Antes de la PRIMERA autorización hay que cerrar el agujero de `kappa_entre_sesiones`**: tras
> pasar la puerta, `excluir` queda vacío y una autorización lee las etiquetas de todos los cubos.
> Extender una puerta con fuga multiplica la fuga. Hoy es seguro porque `PREREGISTRO.md` sigue
> vacío y no hay ninguna autorización. Es bloqueante para ABRIR, no para crear los nombres.

## Estructura

```
config.yaml          los datos de negocio del camino (arriba)
anclas.yaml          artefacto -> fichero -> sha del BLOB (ADR-0035 enmendado)
<artefacto>/         p. ej. eurusd-2026-09 — sin fecha, sin "sesion"
  ventanas.yaml      artefacto, config congelado, casos, datasets, universo, excluidos
  particiones.yaml   artefacto, seed, cupos, asignacion
```

Un artefacto congela su universo (`datasets:`) y sus cupos (bloque `config:`) igual que el kit, y se
ancla igual. Lo que cambia: **aquí ningún fichero se exime nunca** de reproducirse byte a byte,
porque no hubo sesión celebrada cuyas respuestas expliquen una diferencia.
