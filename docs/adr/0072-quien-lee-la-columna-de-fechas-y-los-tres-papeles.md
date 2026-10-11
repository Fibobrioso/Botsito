---
status: ACTIVE
date: 2026-10-10
phase: post-F14 (rama `trabajo/hoja-de-ruta`)
---

# 0072 · Quién lee la columna de fechas de un backtest, y los tres papeles: Aleks, el consultor y la sesión

> La regla general de `CLAUDE.md` («Lo minimo para fijar el universo SI se lee») decía «QUIEN: el
> consultor. No una sesion, no un agente.», y no salía de ningún ADR: la introdujo el commit
> `52c0220` (2026-09-20) a partir de `docs/validation/SEPTIEMBRE-ENTRA.md` §2b. ADR-0046 §6a ya
> fijaba, para marzo, que la columna la lee Aleks. Decisión del consultor del 2026-10-10 (respuesta a
> la PARADA de `trabajo/hoja-de-ruta`, `docs/validation/HOJA-DE-RUTA.md` §2, punto 1).

## Decision

1. **Los tres papeles.**
   - **Aleks** es el usuario: decide, da las órdenes de cierre y es el único que lee la columna de
     fechas de un backtest del trader.
   - **El consultor** es Claude en el chat: revisa los informes, decide lo técnico y escribe los
     encargos. No ejecuta nada en el repositorio. De un backtest recibe de Aleks solo la LISTA DE
     FECHAS, nunca el fichero.
   - **La sesión** es Claude Code: ejecuta en el repositorio lo que dicen los encargos y las
     órdenes de cierre.
2. **La columna de fechas de un backtest la lee Aleks**, para TODO backtest del trader (no solo
   marzo), con las tres ataduras de siempre:
   - **QUIEN:** Aleks. Ni el consultor ni la sesión, que son agentes.
   - **CUANDO:** una sola vez, ANTES del sorteo. Nunca después.
   - **QUE:** solo la columna de fechas: ni resultados, ni PnL, ni una fila de operaciones.
   Se declara el mismo día en `docs/validation/HOLDOUT-EXPOSICIONES.md` (ADR-0021 §4).
3. **ADR-0046 §6a es el caso de marzo de esta regla**, y no cambia: es la misma lectura, con el
   tramo como intersección de UTC y Europe/Madrid. ADR-0021 §1 tampoco cambia: leer las fechas no es
   abrir un holdout; este ADR solo dice QUIÉN las lee.
4. **`CLAUDE.md` cita este ADR** en la regla general y en el párrafo de marzo. Un informe cerrado
   que diga otra cosa no se reescribe: lleva un recuadro de corrección con fecha y rama
   (`docs/validation/SEPTIEMBRE-ENTRA.md`, que contó la lectura del consultor del 2026-09-20).

## Problema que resuelve

La atadura más importante de la lectura de fechas -quién- vivía solo en un fichero de
instrucciones, sin ADR que la sostuviera, y además en contradicción con ADR-0046 §6a: CLAUDE.md
decía «el consultor» en la regla general y «Aleks» en el párrafo de marzo. Y el consultor es Claude
en el chat, un agente, así que la propia regla («no una sesion, no un agente») lo excluía. Ningún
documento definía los papeles, y un encargo copió la regla general sin contrastarla con el ADR
(`docs/runbooks/ERRORES-RECURRENTES.md`, fila de `trabajo/cases-rejilla`, hallazgo 1 del consultor).

## Alternativas consideradas

1. Escribir un ADR que fije los papeles y el QUIEN para todo backtest (elegida).
2. Corregir solo CLAUDE.md («QUIEN: Aleks»), sin ADR.
3. Dejar «el consultor» y definirlo como un papel que delega en Aleks.

## Por que elegimos esta opcion

La regla vale para todos los backtests que vienen (julio, diciembre, los meses que el trader
entregue), y CLAUDE.md pide que una prohibición se pueda revisar contra su ADR. Fijar los tres
papeles en el mismo ADR cierra también la ambigüedad de fondo, que no era solo de esta regla.

## Por que descartamos las demas

- (2) deja la atadura sin ADR, que es justo el defecto que la puso en duda.
- (3) mantiene a un agente como lector de un fichero con material que puede ser reservado, y una
  delegación que nadie podría comprobar.

## Impacto

- `CLAUDE.md`: «QUIEN: Aleks», con este ADR; el párrafo de marzo lo cita junto a ADR-0046 §6a.
- `docs/validation/SEPTIEMBRE-ENTRA.md`: recuadro de corrección al principio, cuerpo intacto.
- Ningún código cambia: la lectura de fechas la hace una persona fuera del repositorio.

## Fecha / fase

2026-10-10 · rama `trabajo/hoja-de-ruta`, entrada P de la Next Action.

## Estado

ACTIVE
