---
status: ACTIVE
date: 2026-09-12
phase: post-F13 (habilita F14)
---

# 0025 · El reparto de mayo no se toca: seis días de biblioteca valen menos que la prueba de que se repartió antes

> **Nota del 2026-09-21 (enmienda de ADR-0035).** La DECISION de abajo sigue entera: los cupos de
> `config.yaml` no se tocan para reparticionar mayo, y el reparto real de la sesión 1 se queda como
> está. Lo que ha caducado es uno de sus ARGUMENTOS. El punto 3 y la alternativa (3) dicen que
> cambiar los cupos «rompería la comprobación del paquete entero» porque `cases/paquete.py` compara
> el `config` que el paquete guardó contra el `config.yaml` de hoy. Desde la enmienda de ADR-0035
> **eso ya no pasa**: `comprobar()` recompone con el bloque `config:` congelado del paquete, así que
> editar `config.yaml` —lo que septiembre exige— deja la sesión 1 idéntica y solo produce un aviso
> de deriva. El motivo que queda en pie para no reparticionar mayo es el de siempre, y es el bueno:
> `particiones.yaml` es la única prueba mecánica de que las particiones se fijaron antes de
> etiquetar.

## Decision

1. **El universo de F14 son los 19 días de MAYO de 2026.** Los 21 de junio salen: el trader se
   comprometió a dos meses y entregó uno, así que para junio no hay ninguna decisión suya con la
   que comparar. Siguen en el paquete de la sesión 1, que es histórico y no se toca.
2. **No se repartición.** Mayo conserva la asignación que el paquete commiteado le dio:
   **6 días `dev`** (2026-05-08, 05-12, 05-15, 05-18, 05-20 y 05-28) y **13 de holdout**, repartidos
   `holdout-1` 6, `holdout-2` 4 y `holdout-3` 3.
3. **Los cupos de `config.yaml` se quedan como están** (16/8/8/8). Están dimensionados para 40 días
   y ahora describen un universo que ya no existe; su comentario lo dice y cita este ADR. Cambiar
   el fichero **rompería la comprobación del paquete entero**, no solo los cupos.
4. **El detalle por operación del xlsx de mayo se puede abrir para esos 6 días `dev`, y solo para
   ellos.** Para los 13 reservados sigue cerrado (ADR-0021, `HOLDOUT-EXPOSICIONES.md` §3).
5. **La vía para crecer no es repartir otra vez, es el mes limpio** que se le ha pedido al trader
   (febrero o marzo de 2026). Cuando llegue, entra como paquete nuevo con sus propios cupos.

   > **NOTA del 2026-09-24 (ADR-0046, no reescribe el cuerpo). Enmienda de este §5 para marzo.**
   > Marzo NO entra por el kit ciego como paquete nuevo: el backtest lo hace el propio trader, ese
   > material no es ciego para él, y ADR-0036 §1 lo saca del kit. Entra por el camino de fidelidad,
   > con sorteo, puerta y la reserva de `fidelidad-2` y `fidelidad-3` (ADR-0046).

## Problema que resuelve

F14 construye la biblioteca de casos y necesita saber sobre qué días trabaja. Hoy hay tres cosas
que no encajan entre sí:

- `config.yaml` pide **16 `dev` y 24 de holdout**, dimensionado para los 40 días de mayo **más**
  junio;
- el paquete commiteado repartió esos 40 días 16/8/8/8, de los cuales **21 son de junio**;
- **junio quedó descartado** el 2026-09-12, así que de aquel reparto solo sobrevive lo que le tocó
  a mayo: 6 `dev` y 13 de holdout.

Seis días de desarrollo es poco, y la tentación evidente es volver a repartir los 19 de mayo con
cupos nuevos —diez y nueve, por ejemplo— ahora que todavía es legítimo: **no existe ni un solo
`LABEL_CASE`** (comprobado: cero registros). Esta decisión es decir que no, y por qué.

## Impacto

- **F14 se construye con 6 días etiquetables.** Es una biblioteca pequeña y hay que decirlo en su
  brief: con seis días no se sostiene ninguna afirmación estadística sobre fidelidad, solo casos
  concretos con los que trabajar.
- **`kit check` sigue dando exit 0 sobre el paquete de la sesión 1**, y con él la única prueba
  mecánica de que las particiones se fijaron antes de etiquetar.
- **Los 13 días reservados siguen intactos**, con el reparto 6/4/3 que ya tenían.
- **El mes limpio pasa de "conviene" a "es la vía"**: es lo único que puede hacer crecer la
  biblioteca sin tocar nada de lo que ya está sellado.

## Alternativas consideradas

1. **No repartir: mayo se queda con lo que le tocó** (elegida).
2. **Repartir los 19 días de mayo con cupos nuevos** (p. ej. 10 `dev` / 9 holdout), que es legítimo
   mientras no exista ningún `LABEL_CASE`.
3. **Cambiar los cupos de `config.yaml`** para que describan el universo real.
4. **Rescatar los 10 días `dev` de junio** que el reparto commiteado ya había asignado.

## Por que elegimos esta opcion

Porque lo que se ganaría es pequeño y lo que se perdería es la garantía más fuerte que tiene el
proyecto.

`particiones.yaml` **no está exento** de reproducirse byte a byte ni siquiera cuando la sesión ya
se celebró: `cases/paquete.py` lo dice con todas las letras —*"no depende de las respuestas, sale
de los hashes de los casos y del seed, así que sigue teniendo que reproducirse byte a byte: es la
prueba de que las particiones se fijaron antes de etiquetar"*—. Repartir otra vez significa
reescribir ese fichero, y a partir de ahí "las particiones se fijaron antes" pasa a ser una
afirmación que hay que creerse en vez de una que se comprueba.

A cambio de qué: de cuatro días más de desarrollo, sobre un mes que **ya está expuesto** (su PnL
diario entero se vio el 2026-09-11) y que por tanto nunca va a ser la partición limpia de la que
salga la cifra de fidelidad de F26. Los días que de verdad importan son los del mes que aún no
tenemos.

## Por que descartamos las demas

- **(2) Repartir de nuevo**: es el canje de arriba. Legítimo, y aun así malo: se cambia una prueba
  por cuatro días de un mes quemado.
- **(3) Cambiar los cupos de `config.yaml`**: no es solo cosmético. `cases/paquete.py` compara el
  `config` que el paquete guardó contra el `config.yaml` de hoy y falla con *"config.yaml cambió
  después de generar el paquete"*. Tocarlo rompe la comprobación de la sesión 1 **entera**, no solo
  la de los cupos. El comentario del fichero explica el desajuste; el fichero se queda quieto.
- **(4) Rescatar los `dev` de junio**: son diez días para los que no existe ninguna decisión del
  trader. Etiquetarlos exigiría pedirle un backtest de junio que ya no va a llegar —y si llegara,
  llegaría después de que se le pidiera el mes limpio, que es más valioso porque no lo ha visto—.

## Fecha / fase

2026-09-12, después de cerrar F13. Habilita F14.

## Estado

ACTIVE
