---
status: ACTIVE
date: 2026-09-11
phase: F12
---

# 0020 · La base del lotaje es la distancia hasta el stop, no la caja completa

## Decision

1. **`lotaje_base` pasa de `distancia_completa` a `hasta_stop_fraccion`**: el lote se dimensiona
   sobre la distancia que va de la entrada a `stop_fraccion_caja`, no sobre la caja entera.
   `riesgo_por_operacion` deja de ser un nominal y pasa a ser **lo que cuesta el stop de verdad**.
2. La segunda opcion del enum **se renombra `desde_075` → `hasta_stop_fraccion`**. Nombraba un
   `0,75` que A-10 cerro en `0,8`: un numero de negocio dentro del nombre de una opcion es la
   doble puerta que ADR-0002 prohibe. El nivel lo pone `stop_fraccion_caja` y solo el.
3. **RN-012 se invierte.** Decia "la perdida real es menor que el riesgo nominal, y es a
   proposito"; ahora dice que el stop cuesta el riesgo entero y que el tramo entre
   `stop_fraccion_caja` y el extremo de la caja no es presupuesto de riesgo. La accion
   `realizar_perdida` pierde el argumento `fraccion`, que ya no multiplica nada.
4. **RN-011 y RN-012 declaran `decision: ADR-0020`** (ADR-0016): el literal del trader que las
   sostenia decia lo contrario, y una regla que dice mas que su cita tiene que declararlo.

## Problema que resuelve

Hasta hoy la spec dimensionaba el lote sobre la caja completa y ponia el stop en `0,8`. La
consecuencia aritmetica, escrita en RN-012, era que el stop costaba `riesgo_por_operacion ×
stop_fraccion_caja`: con `0,5` y `0,8`, un **0,4 %** por operacion en vez del 0,5 % declarado. El
`0,2` restante de la caja no se perdia nunca porque la operacion ya estaba cerrada en `0,8`.

El **acuerdo final** que el consultor cierra el 2026-09-11 es el otro: el 0,5 % se mide **en el
nivel 0,8**. El presupuesto de riesgo se gasta entero cuando el stop salta.

## Impacto

- **El lote sube un 25 %** sobre la misma caja (`1 / 0,8`). Es el efecto que hay que vigilar en
  F24 y F33: el mismo setup mueve una posicion mayor.
- **La perdida por operacion sube de 0,4 % a 0,5 %** del saldo (`base_calculo_riesgo =
  saldo_actual`). Los topes de RN-019 y RN-020 (dia y semana) se consumen mas rapido: con el
  4,5 % diario, el margen pasa de once perdidas a nueve.
- **El RR realizado NO cambia**: sigue siendo `objetivo_rr / stop_fraccion_caja` = 3,75. Las dos
  distancias se escalan igual, asi que la razon se conserva; lo unico que cambia es el tamano del
  lote y, con el, el dinero de cada lado.
- **ADR-0014 queda enmendado en una frase**: decia que la caja completa es "la misma distancia
  sobre la que se dimensiona el lote". Ya no lo es. Lo demas de ADR-0014 sigue en pie: el objetivo
  se mide sobre la caja completa.
- **RN-027 (redondeo a la baja) importa mas**, porque redondea un lote mayor.
- `stop_proteccion_capital` sigue UNKNOWN: derivado de `stop_fraccion_caja`, no es una segunda
  puerta.

## Evidencia, y lo que la evidencia NO dice

El acuerdo es **del consultor**, referido por escrito el 2026-09-11, y asi queda registrado en
`fb-2026-09-09-sesion-01-17ed6193`: no es una transcripcion del trader. El registro que supersede
(`fb-2026-09-09-sesion-01-a089315e`) llevaba el literal contrario, escrito en la hoja de la sesion
1: *"El lotaje se pone sobre la caja completa de SL, pero automaticamente se mueve al 0.8 de la
misma para que corra la operacion"*.

**Queda anotada una tension que nadie debe leer como confirmacion.** El mismo 2026-09-11 el trader
entrega el backtest de mayo y escribe por WhatsApp: *"sin tomar el margen a 0,20 en mayo tiro un
21%, cubriendo/protegiendo el margende 0,20, la rentabilidad en mayo tira un 27,6"* y *"promediando
a 1:3,4 tira un 28,2"*. Con los 18 ganadores y 33 perdedores que da FX Replay para mayo, esas tres
cifras salen exactas de esta cuenta:

| cifra | cuenta | convencion que implica |
|---|---|---|
| 21 | `18 × 3 − 33 × 1` | gana 3 cajas, pierde 1 caja |
| 27,6 | `18 × 3 − 33 × 0,8` | gana 3 cajas, pierde 0,8 de caja |
| 28,2 | `18 × 3,4 − 33 × 1` | la media 1:3,4 con perdida de 1 caja |

Es decir: **el trader cuenta en unidades de CAJA COMPLETA**, y lo que llama "el margen de 0,20" es
justo la parte de la caja que el stop en `0,8` le ahorra en cada perdida. Esa es la convencion
vieja, no la nueva. No es prueba de que el acuerdo sea otro -son medidas retrospectivas de un mes
ya operado, no una instruccion de dimensionamiento-, pero **si es la pregunta que hay que hacerle
al trader antes de que esto llegue a una cuenta real**: con la base nueva, los mismos 51 trades de mayo que no
acabaron en break even (18 + 33, de 68) rinden `18 × 3,75 − 33 × 1 = 34,5` unidades de riesgo, y el 27,6 % de su mensaje seria un
34,5 % a igual riesgo declarado. Hasta que lo ratifique, manda el acuerdo del consultor y esta es
la regla vigente.

**Y no puede ratificarse midiendo mayo.** Trece de los diecinueve dias de mayo estan asignados a
`holdout-1/2/3` (`knowledge/cases/kit/2026-09-09-sesion-01/particiones.yaml`): elegir la base del
lotaje comparando rentabilidades sobre ese mes quemaria el holdout antes de que F26 exista.

## Alternativas consideradas

1. **`hasta_stop_fraccion`** (elegida): el lote absorbe `riesgo_por_operacion` en la distancia que
   va de la entrada al stop.
2. **Dejar `distancia_completa` y bajar `riesgo_por_operacion` a 0,625 %** para que el stop cueste
   0,5 %.
3. **Conservar el nombre `desde_075`** y cambiar solo el valor.
4. **Marcar RN-012 DESCARTADA** en vez de invertirla.

## Por que elegimos esta opcion

Porque es lo que dice el acuerdo -el 0,5 % se mide EN el nivel 0,8- y porque deja el registro
diciendo la verdad con un solo numero: `riesgo_por_operacion` es lo que cuesta el stop, sin que
nadie tenga que multiplicarlo por nada para saber lo que arriesga. La opcion ya existia en el enum
desde F10; lo que cambia es cual esta elegida y como se llama.

## Por que descartamos las demas

- **(2) Bajar el riesgo a 0,625 %**: dos puertas para el mismo numero y un parametro que ya no
  significa lo que dice. El trader habla de 0,4-0,5 %, no de 0,625 %.
- **(3) Conservar `desde_075`**: el registro habria dicho "desde 0,75" mientras el stop vive en
  0,8. Es exactamente el defecto que P13 encontro en la auditoria de F11.
- **(4) Descartar RN-012**: la regla sigue afirmando algo vivo -que el tramo tras el stop no es
  presupuesto de riesgo- y descartarla dejaria a `realizar_perdida` sin ninguna regla que la use.

## Fecha / fase

2026-09-11, F12 (acuerdo final del consultor, entre el piloto de la forma y el cierre).

## Estado

ACTIVE
