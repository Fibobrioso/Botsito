---
status: ACTIVE
date: 2026-09-10
phase: F11
---

# 0017 · El reloj del trader es su reloj civil: se revierte ADR-0012 y se confirma ADR-0005

## Decision

1. **`huso_operativa` vuelve a `Europe/Madrid`.** Es el reloj del trader como persona: se sienta a
   las 7 y cierra a las 3 **sea cual sea la fecha**, asi que su horario cambia con el horario de
   verano igual que el de cualquiera.
2. **`ventana_inicio` y `ventana_fin` cuelgan de `huso_operativa`**, no del reloj de la pantalla.
3. **`anclaje_h4` pasa a `17:00 America/New_York`**, que es la convencion de brokers para "00:00 de
   servidor" que **ADR-0005 ya habia escrito**. Sigue el calendario de Nueva York, como confirma
   `broker_dst: us`, medido contra la demo real.
4. **`huso_grafico` = `Europe/Madrid`, `CONFIRMED`, y ninguna regla cuelga de el.** Queda como lo
   que siempre fue: la etiqueta con la que el trader lee su pantalla, util para traducir "la vela
   empieza a las 23" a un instante.
5. **Los 28 dias al año en que su horario y la rejilla H4 no cuadran, manda su horario.** El bot
   opera de 07:00 a 15:00 de Madrid y esos dias empieza una hora dentro de la vela. A-14 se
   reescribe con esa pregunta para ratificarla con el trader.

## Problema que resuelve

ADR-0012 cambio `huso_operativa` de `Europe/Madrid` a `Etc/GMT-2` -un offset **fijo**- apoyandose en
que "la sesion 1 lo desmintio". **ADR-0015 mostro que esa afirmacion no se sostiene**: todas las
lecturas del repositorio son de verano y el propio trader ata el UTC+2 a Madrid (*"utc mas 2 que son
ahora ya madrid"*, `ev-v3-000136`).

El 2026-09-10 el consultor lo cierra sin ambigüedad: **el trader opera siempre a la misma hora suya,
sea cual sea la fecha, y no hay ninguna configuracion deliberada de huso.** Eso es, por definicion,
un reloj civil. Un offset fijo dice justo lo contrario.

Y al separar los dos relojes aparece la cuenta que nadie habia hecho. Si la ventana es su hora local
y la rejilla H4 se ancla al dia del servidor:

| Fecha | Madrid | Nueva York | Primera H4 en su pantalla |
|---|---|---|---|
| 15 ene | UTC+1 | UTC−5 | **23:00** (22:00 UTC) |
| 12 mar | UTC+1 | UTC−4 | **22:00** (21:00 UTC) |
| 15 jul | UTC+2 | UTC−4 | **23:00** (21:00 UTC) |
| 28 oct | UTC+1 | UTC−4 | **22:00** (21:00 UTC) |

**337 dias al año la ve a las 23:00** -por eso contesto "es la misma hora" y por eso parecia que no
habia pregunta-. **28 dias no**: del 8 al 28 de marzo y del 25 al 31 de octubre, porque la UE cambia
la hora el ultimo domingo de marzo y octubre y EE.UU. el segundo de marzo y el primero de noviembre.

Lo caro no es la ventana. Es que **en UTC el ancla es 21:00 en verano y 22:00 en invierno**: con un
huso fijo el bot la habria calculado a las 21:00 UTC **todo el invierno**, una hora antes que la vela
real, repartiendo mal **todas** las velas H4. Y la vela H4 es de donde sale el sesgo, que es lo
primero de lo que cuelga la estrategia entera (RN-003). No habria fallado nada: habria operado un
mercado ligeramente distinto durante cinco meses.

## Alternativas consideradas

- **A. Dejar `Etc/GMT-2`** y tratar el desfase como ruido.
- **B. `anclaje_h4` = `23:00 Europe/Madrid`**, que es lo que el trader ve.
- **C. Esos 28 dias, mover la ventana a 06:00-14:00** para seguir empezando en la apertura de la H4.
- **D. Esos 28 dias, no operar.**

## Por que elegimos esta opcion

Porque **es lo que ADR-0005 ya habia decidido** antes de que la sesion 1 confundiera las cosas: tres
relojes explicitos, `huso_operativa = Europe/Madrid` para el dia del trader, y el reloj del servidor
escrito como `17:00 America/New_York`. La regla de anclaje de ADR-0005 -particion de la recta UTC
por hora de pared en el huso del anclaje- ya reproduce el desplazamiento de una hora entre semanas,
asi que F15 no necesita nada nuevo.

Y porque el desfase de 28 dias **no es ruido: es una decision de negocio**. El trader se sienta a su
hora. Un bot que esos dias empiece a las 06:00 para cuadrar con la vela estaria operando cuando el no
opera, y F26 mediria fidelidad contra sesiones que nunca existieron.

## Por que descartamos las demas

- **A**: cinco meses al año de velas H4 mal repartidas. Es el fallo mas caro que ha encontrado esta
  auditoria, y el unico que no habria dado ningun sintoma.
- **B**: correcto 337 dias y **equivocado exactamente los 28 que importan**, porque esos dias su
  pantalla y el servidor no dicen lo mismo. Escribirlo asi seria congelar la observacion en vez del
  hecho.
- **C**: mantiene intacta la premisa de RN-001 a costa de operar cuando el trader no opera. Cambia
  la estrategia para salvar una frase.
- **D**: tira un 11 % del año operativo por un desfase de una hora. Defendible ante una prop firm,
  desproporcionado como decision por defecto.

## Que sustituye de otros ADR

- **Revierte el punto 5 de ADR-0012** (el reloj) y **restituye ADR-0005** en sus tres relojes y su
  anclaje. Lo demas de ADR-0012 -tipos nuevos, ausencia de valor, categorias, `valor_canonico`-
  sigue entero.
- **Completa ADR-0015**, que habia bajado `huso_grafico` a `DEFAULT_AMBIGUOUS` por falta de dato.
  Ahora hay dato, y sube a `CONFIRMED` con el valor que la evidencia sostiene: `Europe/Madrid`.
- La enmienda de ADR-0005 fechada el 2026-09-09 ("`huso_operativa` deja de valer `Europe/Madrid`")
  queda **revocada por este ADR**.

## Impacto

- `spec_version` **2.0.0 -> 3.0.0**. En invierno el bot abre a las 06:00 UTC y no a las 05:00, y las
  velas H4 se parten en otro sitio: es otro comportamiento, no otra redaccion.
- RN-001 cambia de titulo: **dejaba dicho que las sesiones estan "alineadas con H4"**, y no lo estan
  28 dias al año.
- RN-003 deja de nombrar `huso_grafico`: la rejilla no depende del reloj de la pantalla.
- `no_confirmados()` baja de 7 a 6: `huso_grafico` vuelve a `CONFIRMED`, esta vez con una cita que
  lo sostiene de verdad.
- **A-14 sigue ABIERTA**, pero por fin con la pregunta util, que ademas es corta y se puede hacer
  por escrito sin sesion.

## Fecha / fase

2026-09-10, F11 (auditoria previa a la validacion).

## Estado

ACTIVE
