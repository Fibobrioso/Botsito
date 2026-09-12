---
status: ACTIVE
date: 2026-09-12
phase: F12-holdout
---

# 0021 · Que cuenta como abrir un holdout, y que se hace con la exposicion de mayo

## Decision

1. **Abrir un holdout** es cualquiera de estas dos cosas, y solo estas dos:
   - **leer sus etiquetas** (`LABEL_CASE`, o el detalle por operacion del backtest del trader en
     esos dias: hora, direccion, entrada, stop, objetivo);
   - **medir cualquier cifra del bot sobre esos dias** (fidelidad, aciertos, PnL simulado,
     sensibilidad), aunque sea de pasada y aunque no se apunte.
2. **Ver el RESULTADO AGREGADO de esos dias no lo abre**, pero **si es una exposicion** y se
   declara. Un PnL diario no permite reconstruir ni una sola decision del trader, que es lo que el
   bot tiene que replicar; pero es informacion sobre el dia y quien la tiene deja de poder afirmar
   que no la tuvo.
3. **Solo el usuario autoriza abrir un holdout**, y la apertura exige `docs/validation/PREREGISTRO.md`
   commiteado ANTES con los umbrales, mas un ADR que diga que se midio y contra que umbral.
4. **Toda exposicion se anota el mismo dia** en `docs/validation/HOLDOUT-EXPOSICIONES.md`: fecha,
   que se vio exactamente, que particion toca, quien lo vio y si la deja quemada o no.
5. **La exposicion del 2026-09-11 NO quema ninguna particion.** Se vio el calendario de PnL diario
   de todo mayo, holdout incluido; no se vio ni una decision. Queda declarada, y F26 la cita en su
   informe: sin esa frase, su cifra de fidelidad no es defendible.
6. **`holdout-1` se reserva intacto para la nota de F26.** Nadie lo toca hasta que exista el
   pre-registro. Si hace falta corregir y volver a medir, se usa `holdout-2`, y `holdout-3` queda
   para la fase final.
7. **Se le pide al trader un mes mas que no haya tocado**, en paralelo y sin bloquear F13/F14. Es
   la unica forma de tener una particion limpia de verdad: mayo ya esta expuesto y junio quedo
   descartado.

## Problema que resuelve

El proyecto lleva desde F01 diciendo *"Un holdout abierto queda quemado: no vuelve a usarse para
medir"* (`knowledge/cases/holdout/README.md`, `PROJECT_STATE.md`) y **nunca escribio que es abrir**.
La auditoria de proceso del 2026-09-12 lo encontro junto con dos cosas peores: que **nadie dice
quien autoriza** una apertura, y que **no hay procedimiento para una exposicion accidental** — que
ya habia ocurrido.

Porque ocurrio. El 2026-09-11 el trader entrego el backtest de mayo y, con el, siete capturas de la
pestana Analytics de FX Replay. Una de ellas es el **calendario de PnL dia a dia del mes entero**:
4 may +30 $, 5 may +133 $, … 21 may −51 $, 29 may −118 $. Trece de esos diecinueve dias son
holdout-1, holdout-2 y holdout-3, y la sesion de trabajo que proceso el material los vio.

Y hay una tercera cosa que agrava la decision: **la guarda que protege el holdout no existe
todavia**. `PROJECT_STATE` afirma *"prohibido leer desde `src/botsito/spec` y `src/botsito/domain`
(guarda en tests)"*, pero `tests/conftest.py` tiene un stub que dice, textualmente, *"Se implementa
y se hace autouse en F14"*. Lo unico vivo es un contrato que busca la cadena "holdout" en los `.py`.

## Impacto

- **Mayo sigue sirviendo para medir**, que es lo que estaba en juego: junio quedo descartado el
  2026-09-12, asi que si la exposicion hubiera quemado las tres particiones, F26 se habria quedado
  con seis dias `dev` y ninguno para la nota.
- **F26 hereda una obligacion**: citar la exposicion en su informe, junto al pre-registro. Una cifra
  de fidelidad sobre `holdout-1` que no la mencione es una cifra que no se puede defender.
- **F14 hereda dos**: implementar de verdad la guarda de `tests/conftest.py` (hoy stub) y tratar el
  detalle por operacion del backtest de mayo como material de holdout, no como material libre.
- `knowledge/cases/holdout/README.md` pasa a ser el sitio donde vive esta definicion; `PROJECT_STATE`
  apunta ahi en vez de repetirla.
- Nace `docs/validation/HOLDOUT-EXPOSICIONES.md`, que empieza con la del 2026-09-11.

## Alternativas consideradas

1. **Ver el resultado agregado NO abre, pero se declara** (elegida).
2. **Lectura estricta: ver el PnL de un dia lo quema.** Las tres particiones de mayo quedarian
   quemadas hoy mismo.
3. **No decidir nada y seguir**, dejando "abrir" sin definir.
4. **Quemar solo los dias concretos que se vieron**, no la particion entera.

## Por que elegimos esta opcion

Porque es la que distingue lo que de verdad contamina de lo que no. El bot tiene que reproducir
**decisiones**: a que hora entra, en que direccion, donde pone el stop. El PnL de un dia no contiene
ninguna de esas cosas y no se puede invertir para deducirlas. Lo que si contiene es una pista
—"el 29 fue malo"— y por eso no se ignora: se declara, para que quien lea la cifra de F26 sepa
exactamente que sabia quien la produjo.

La alternativa estricta es mas pura y, hoy, mas cara de lo que protege: nos quedariamos sin ninguna
particion para medir, con junio descartado y sin material nuevo del trader. Se paga el coste de
detener el proyecto a cambio de eliminar un riesgo que, en este caso concreto, es de segundo orden.

## Por que descartamos las demas

- **(2) La estricta**: correcta en abstracto, pero dejaria a F26 sin nota y obligaria a esperar un
  mes nuevo del trader antes de poder medir nada. Se adopta su exigencia util —declarar— sin su
  coste.
- **(3) No decidir**: es lo que llevabamos, y produjo exactamente esto: una exposicion sin
  procedimiento y una regla que nadie sabia aplicar.
- **(4) Quemar solo los dias vistos**: se vieron los diecinueve, asi que quemaria las tres
  particiones igual. Y una particion a la que le faltan dias deja de ser comparable con las otras.

## Fecha / fase

2026-09-12, rama de trabajo `trabajo/holdout-y-exposicion` (tras cerrar F12).

## Estado

ACTIVE
