# La viabilidad del trader con la comisión más probable y las variantes del stop

> **NO SE ENSEÑA AL TRADER.** Ni este informe, ni sus cifras, ni nada que salga de él entra en
> material para él: sesgaría sus respuestas, y en particular las de A-18, que es justo lo que las
> variantes V2 a V4 suponen. Solo para el consultor y para Aleks.

> **Escenario de referencia: 5 USD ida y vuelta (comisión publicada por FTMO desde el 29-09-2025).
> El escenario de 3 USD corresponde a la tarifa anterior.** (Orden del consultor del 2026-09-28,
> antes del cierre; la fuente, en el recuadro de `FTMO-REGLAS.md`, sigue sin confirmar en demo.)
>
> **Y parte de la ventaja de V2 procede de las operaciones de stop cortísimo que excluye el tope de
> 100 lotes**: con su lote un 25 % mayor, V2 deja fuera 11 con 3 USD y 10 con 5 USD, frente a 7 en
> V1, y son precisamente las que más castiga la comisión (§2).

Rama `trabajo/viabilidad-comision`, 2026-09-28, desde `main` en `d09ca19`. Es una **medición**: no
cambia la estrategia, el bot, el bróker ni ningún parámetro del perfil; la comisión de cada
escenario vive solo en la corrida. **Las variantes V2 a V4 son hipótesis de A-18, no decisiones.**
No se ha ajustado nada para mejorar la cifra. Solo construcción: las 77 operaciones de los días
`dev` de abril y agosto de 2026, las mismas y leídas igual que en `VIABILIDAD-TRADER.md`. Script:
`scripts/viabilidad_comision.py`.

## Resumen

Esperanza **neta** en R (después de la comisión) con su intervalo del 95 % por bootstrap, y el
veredicto de la fase 1 de FTMO en **abril / agosto / abril+agosto**, al 0,5 % de riesgo. Columnas:
comisión de ida y vuelta por lote.

| variante | 3 USD | 5 USD | 10 USD |
|---|---|---|---|
| V1 · stop en el 1, lote para el 1, TP a 3 R (hoy) | +0,49 [−0,01; +0,99] · no concluyente / pasa / pasa | +0,34 [−0,15; +0,85] · no concluyente / no concluyente / pasa | −0,14 [−0,64; +0,36] · no concluyente / no pasa / no pasa |
| **V2** · stop en el 0,8, lote para el 0,8, TP a 3 D | **+0,67 [+0,06; +1,28]** · no concluyente / pasa / pasa | **+0,47 [−0,13; +1,08]** · no concluyente / pasa / pasa | **−0,04 [−0,64; +0,57]** · no concluyente / no concluyente / no concluyente |
| V3 · lote para el 1, stop al 0,8 tras llenar, TP a 3 D | +0,40 [−0,07; +0,89] · no concluyente / pasa / pasa | +0,26 [−0,21; +0,75] · no concluyente / no concluyente / no concluyente | −0,25 [−0,73; +0,25] · no concluyente / no pasa / no pasa |
| V4 · lote para el 1, stop al 0,8 tras llenar, TP a 3 veces 0,8 D | +0,34 [−0,07; +0,77] · no concluyente / no concluyente / pasa | +0,20 [−0,21; +0,63] · no concluyente / no concluyente / no concluyente | −0,30 [−0,74; +0,13] · no concluyente / no pasa / no pasa |
| **anotada** (sus salidas reales, lote para el 1) | **+0,73 [+0,23; +1,24]** · pasa / pasa / pasa | **+0,56 [+0,05; +1,08]** · pasa / pasa / pasa | +0,13 [−0,41; +0,67] · pasa / no concluyente / pasa |

**Lo que dice.**
- **La comisión decide.** Con 10 USD de ida y vuelta (el supuesto del perfil), ninguna variante
  tiene esperanza neta positiva y la serie anotada cruza el cero. Con 3 USD, todas las variantes
  quedan en positivo en la cifra puntual. **Sin embargo, solo dos intervalos no tocan el cero**: V2 y
  la serie anotada. Con 5 USD solo queda la anotada.
- **V2 sale la mejor de las simuladas en las tres comisiones**, y es la única que no rompe ningún
  límite con 10 USD. Hay que leerlo con cuidado: su lote es un 25 % mayor que el de V1 para la misma
  operación, así que más operaciones de stop corto pasan de 100 lotes y quedan fuera (11 con 3 USD,
  frente a 7 en V1). Son precisamente las que más castiga la comisión (§3).
- **Las salidas reales del trader son mejores que cualquier regla fija simulada**, en las tres
  comisiones: sus ganadoras llegan más lejos (6,25 pips de media, frente a 4,6 a 5,6) y sus
  perdedoras se quedan más cerca (−1,34 pips, frente a −1,6 a −2,1).
- **Abril solo no pasa en ninguna variante simulada.** Donde hay «pasa», el 10 % se alcanza en
  agosto o sumando abril y agosto. Con sus salidas reales, abril sí pasa, el 13 de abril.

## 1. Fase 1 · La comisión

Tres escenarios de comisión de forex, de ida y vuelta por lote (la mitad en cada lado):
- **3 USD**: la tarifa anterior de forex, 1,50 por lado (lo que FTMO publicó el 27 de marzo de 2025
  para dos pares nuevos, USDSGD y USDCNH, y lo que da una fuente de terceros);
- **5 USD, el escenario de referencia**: 2,50 por lado, la comisión de forex que FTMO fija desde la
  apertura del 29 de septiembre de 2025 (declarado por el consultor; casa con la API de símbolos,
  5 USD en EURUSD, R12);
- **10 USD**: 5 por lado, el supuesto conservador del perfil (`firma_comision_por_lado: true`).

Las fuentes, con su cita y marcadas **no confirmado en demo**, están en el recuadro nuevo de
`docs/validation/FTMO-REGLAS.md`. La actualización de FTMO del 25 de septiembre de 2025, que fija los
5 USD, la sesión **no la pudo leer** (el servidor cortó la conexión en los cuatro intentos): su
contenido lo declara el consultor. **El parámetro del perfil no cambia**: se fija solo con el CSV de la demo
(`docs/runbooks/DEMO-FTMO.md`).

## 2. Fase 2 · Las variantes de A-18

**Supuesto de las variantes:** la entrada es el 0 de la caja y el stop inicial del libro
(`initialSL`) es su 1; D es la distancia de 0 a 1. `BLOQUE-DE-LA-CAJA.md` §5 vio el stop colocado en
el 1 en 6 de 12 cajas y en el 0,8 en otras; donde el libro ya lo tuviera en el 0,8, las variantes
lo acercan más de lo que el trader hizo. Todo al 0,5 % de riesgo sobre el saldo realizado.

| variante | stop | lote calculado para | objetivo | R |
|---|---|---|---|---|
| V1 | el 1 | el 1 (D) | 3 D | D |
| V2 | el 0,8 | el 0,8 (0,8 D) | 3 D (RR efectivo 3,75) | 0,8 D |
| V3 | el 1, movido al 0,8 en el instante del llenado | el 1 (D) | 3 D | D: el stop pierde 0,8 R |
| V4 | el 1, movido al 0,8 en el instante del llenado | el 1 (D) | 3 veces 0,8 D (2,4 D) | D: el stop pierde 0,8 R |

- 0,8 D se redondea al punto más cercano (nunca cae en medio punto).
- En V3 y V4 el movimiento se hace en el mismo instante del llenado: el mismo stop que V2 con el lote
  de V1.
- V1 lleva el movimiento documentado de v7-3, como `VIABILIDAD-TRADER.md`. Las demás no, porque ya
  ponen el stop en el 0,8.

**Operaciones fuera por el tope de 100 lotes** (abril+agosto; depende de la comisión porque el lote
se calcula sobre el saldo, que crece más cuanto menos se paga):

| comisión | V1 | V2 | V3 | V4 |
|---|---|---|---|---|
| 3 USD | 7 | 11 | 7 | 7 |
| 5 USD | 7 | 10 | 7 | 7 |
| 10 USD | 4 | 8 | 3 | 3 |

## 3. Fase 3 · Las métricas

Todas sobre abril+agosto, y la esperanza bruta antes de la comisión. El «coste» es la comisión más
el spread del tick del llenado, en R; el spread se da como coste informativo, porque ya va dentro de
los precios (en la simulada, en la salida; en la anotada, en los llenados de OANDA) y no se resta
otra vez. «Peor día» es la mayor caída de la equity en un día desde el saldo del corte, sobre el
capital inicial (el límite es 5 %), en abril / agosto / abril+agosto.

| comisión | serie | n | acierto | esperanza bruta | esperanza neta [IC 95 %] | peor día | pips ganadoras | pips perdedoras | stop medio / mediano (pips) | coste en R (comisión + spread) |
|---|---|---|---|---|---|---|---|---|---|---|
| 3 | V1 | 70 | 46 % | +0,70 | +0,49 [−0,01; +0,99] | 2,57 / 3,16 / 3,38 % | +5,29 | −2,05 | 1,66 / 1,50 | 0,21 + 0,20 |
| 3 | V2 | 66 | 42 % | +0,91 | +0,67 [+0,06; +1,28] | 2,92 / 2,95 / 2,92 % | +5,58 | −1,83 | 1,33 / 1,20 | 0,25 + 0,24 |
| 3 | V3 | 70 | 40 % | +0,62 | +0,40 [−0,07; +0,89] | 2,39 / 3,00 / 3,14 % | +5,58 | −1,73 | 1,33 / 1,20 | 0,21 + 0,20 |
| 3 | V4 | 70 | 46 % | +0,56 | +0,34 [−0,07; +0,77] | 2,42 / 3,02 / 3,15 % | +4,63 | −1,70 | 1,33 / 1,20 | 0,21 + 0,20 |
| 3 | anotada | 77 | 43 % | +0,98 | +0,73 [+0,23; +1,24] | 0,69 / 1,33 / 0,69 % | +6,25 | −1,34 | 1,66 / 1,50 | 0,26 + — |
| 5 | V1 | 70 | 46 % | +0,70 | +0,34 [−0,15; +0,85] | 2,80 / 4,45 / 3,54 % | +5,29 | −2,05 | 1,66 / 1,50 | 0,35 + 0,20 |
| 5 | V2 | 67 | 42 % | +0,88 | +0,47 [−0,13; +1,08] | 3,20 / 3,02 / 3,20 % | +5,58 | −1,80 | 1,33 / 1,20 | 0,42 + 0,24 |
| 5 | V3 | 70 | 40 % | +0,62 | +0,26 [−0,21; +0,75] | 2,62 / 3,22 / 3,30 % | +5,58 | −1,73 | 1,33 / 1,20 | 0,35 + 0,20 |
| 5 | V4 | 70 | 46 % | +0,56 | +0,20 [−0,21; +0,63] | 2,65 / 3,24 / 3,31 % | +4,63 | −1,70 | 1,33 / 1,20 | 0,35 + 0,20 |
| 5 | anotada | 77 | 43 % | +0,98 | +0,56 [+0,05; +1,08] | 0,79 / 1,49 / 0,79 % | +6,25 | −1,34 | 1,66 / 1,50 | 0,43 + — |
| 10 | V1 | 73 | 44 % | +0,62 | −0,14 [−0,64; +0,36] | 3,35 / 5,38 / 5,35 % | +5,29 | −1,94 | 1,66 / 1,50 | 0,76 + 0,20 |
| 10 | V2 | 69 | 41 % | +0,83 | −0,04 [−0,64; +0,57] | 3,85 / 3,19 / 4,60 % | +5,58 | −1,74 | 1,33 / 1,20 | 0,87 + 0,25 |
| 10 | V3 | 74 | 38 % | +0,53 | −0,25 [−0,73; +0,25] | 3,10 / 5,05 / 4,90 % | +5,58 | −1,62 | 1,33 / 1,20 | 0,78 + 0,21 |
| 10 | V4 | 74 | 43 % | +0,47 | −0,30 [−0,74; +0,13] | 3,14 / 5,09 / 4,91 % | +4,63 | −1,59 | 1,33 / 1,20 | 0,78 + 0,21 |
| 10 | anotada | 77 | 43 % | +0,98 | +0,13 [−0,41; +0,67] | 1,02 / 1,89 / 1,02 % | +6,25 | −1,34 | 1,66 / 1,50 | 0,86 + — |

**Cuándo pasa, donde pasa** (el primer cierre que deja el saldo en el 10 % con los días mínimos):
- 3 USD: V1 en agosto el 31 y seguidos el 19 de agosto; V2 en agosto el 25 y seguidos el 6 de
  agosto; V3 en agosto el 31 y seguidos el 21 de agosto; V4 seguidos el 25 de agosto; la anotada en
  abril el 13, en agosto el 19 y seguidos el 13 de abril.
- 5 USD: V1 seguidos el 25 de agosto; V2 en agosto el 27 y seguidos el 21 de agosto; la anotada en
  abril el 13, en agosto el 20 y seguidos el 13 de abril.
- 10 USD: la anotada en abril y seguidos, el 13 de abril.

Los que no pasan con 10 USD rompen la **pérdida diaria el 7 de agosto** en agosto (el pico del dato,
`VIABILIDAD-TRADER.md` §3.1), y, en abril+agosto, V1 la diaria ese mismo día y V3 y V4 la **pérdida
total** (el 10 % del capital) el 12 de agosto.

**Los stops son de pips, no de decenas de pips.** El stop del trader mide 1,66 pips de media y 1,5
de mediana, y 1,33 y 1,2 con el 0,8. El spread ya cuesta cerca de 0,2 R por operación antes de la
comisión, y cada dólar de comisión de ida y vuelta cuesta de media entre 0,07 y 0,09 R. Por eso la
comisión, que en una estrategia de stops de 20 pips sería ruido, aquí es la cifra que decide.

**Lo que no dice.** Con 66 a 77 operaciones, los intervalos son anchos: en V2 con 3 USD y en la
anotada con 5, que no tocan el cero, el extremo bajo queda a centésimas de él (+0,06 y +0,05). Que V2 salga la mejor no hace de V2 la
regla: es la hipótesis de A-18 que mejor aguanta esta muestra, en parte porque saca del juego las
operaciones de stop más corto. Qué hace de verdad el trader con el stop lo contesta él (A-18), y qué
cobra de verdad FTMO, la demo.

## 4. Estado

Script, test e informe en un solo commit sellado, con el recuadro de fuentes en `FTMO-REGLAS.md` y el
que remite aquí en `VIABILIDAD-TRADER.md`. Nada de esto se enseña al trader. **Rama lista para
revisión, NO cerrada.**
