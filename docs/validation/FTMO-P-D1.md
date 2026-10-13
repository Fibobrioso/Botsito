# FTMO-P-D1 · La respuesta de FTMO a P-D1 y el margen que nadie comprueba

Rama `trabajo/entrada-julio`, fase 6 (2026-10-13), aparte de julio. Encargo:
`docs/encargos/trabajo-entrada-julio.md`. Informe de la rama: `docs/validation/ENTRADA-JULIO.md`.

**Por qué un fichero nuevo y no RESPUESTAS-FTMO.md.** La entrada O de la Next Action dice que la
respuesta «se registra parafraseada (RESPUESTAS-FTMO)», pero `docs/validation/RESPUESTAS-FTMO.md` es
un informe CERRADO en `main` (`stable/F37a-respuestas-ftmo`), que solo admite recuadros de corrección.
Ir a un fichero nuevo es una **desviación de la letra de O, aceptada por el consultor** en su
respuesta a la PARADA del 2026-10-12 («Además», punto 3).

## 1. La respuesta, en paráfrasis

P-D1 (`DEMO-EJECUCION-1.md` §0.c): si la cuenta FTMO Challenge 2-Step Swing de MT5 es de cobertura o
de compensación, si su volumen máximo en EURUSD es de 50 o de 100 lotes, y (punto 3, añadido al
enviarla) si hay un tope de volumen sumado entre varias órdenes o posiciones. Enviada a
support@ftmo.com el 2026-10-09; **respondida por correo el 2026-10-12, ticket JSP-CPQRQ-197**. Aquí
va solo la paráfrasis que dio el consultor en el encargo, nunca el texto del correo: su pie prohíbe
compartirlo y el repositorio es público.

1. **Cobertura.** Todas las cuentas de FTMO Global son de cobertura (hedging). Coincide con lo medido
   en la prueba gratuita (`ACCOUNT_MARGIN_MODE_RETAIL_HEDGING`, fila 25 de la ejecución 1).
2. **50 lotes.** El volumen máximo en EURUSD es de 50 lotes, el que enseña la especificación del
   símbolo en la plataforma. Coincide con `firma_volumen_max_lotes` = 50 (ADR-0071) y descarta los
   100 de la tabla de la web.
3. **El tope sumado: sin respuesta directa.** No dicen si hay un tope de volumen sumado entre varias
   órdenes o posiciones. Dan una **pauta general de gestión del riesgo, que no es una regla**: como
   orientación, hasta un 20 % del margen de la cuenta y un 1,5 % de riesgo por idea. Y recuerdan que
   las apuestas a un solo lado están prohibidas.

Lo que esto cierra y lo que no: 1 y 2 confirman lo que ya estaba en el perfil (no cambia nada); 3
queda abierto, pero el apartado 2 enseña que, para este bot, el límite que manda antes es el margen.

## 2. El margen: lo que ya decía ADR-0026, y que nadie comprueba

**No es un hallazgo nuevo.** ADR-0026, «Impacto» (líneas 116-123), ya lo dice: con 0,5 % de riesgo
sobre 100.000, el margen es 166.667 × P / d (P el precio, d el stop en pips) y «supera los 100.000 de
la cuenta con un stop por debajo de 1,67 × P pips (1,95 pips con P = 1,17). F21 lo comprueba con la
distribución real de cajas». Lo que el consultor ha visto, y lo que se mide aquí, es que **nada lo
comprueba**.

**Medido el 2026-10-13** (búsquedas sobre `src/`, `scripts/`, `tools/` y el perfil):
- `firma_apalancamiento` (30) **no lo lee ningún código del bot** (`src/`, `scripts/`, `tools/`):
  fuera de ellos aparece en `knowledge/spec/parametros.yaml:1821` y en
  `knowledge/cuentas/ftmo-2step-swing-100k.yaml:270`, y lo lee solo el anexo de esta medida
  (`anexos/ENTRADA-JULIO/margen_p_d1.py`), que no es del bot.
- **El simulador no comprueba el margen.** En `src/botsito/engine/` la palabra «margen» solo sale
  como el margen de minutos antes de un cierre largo (`broker.py:329`, `:696`, `:739`;
  `simulacion.py:108-115`), como un porcentaje sobre los topes de pérdida
  (`primitivas_broker.py:308-309`) y como márgenes de dibujo del visor (`visor.py`).
- **Son FALSAS dos descripciones** (no se tocan: el perfil y la spec están fuera de esta rama):
  - el perfil, `ftmo-2step-swing-100k.yaml:276`: «Lo consume el broker simulado (margen)»;
  - `parametros.yaml:1826-1829`: «F21 lo comprueba con la distribucion real de cajas».

**La fórmula** (documentación de MetaTrader 5, «Margin Calculation for Retail Forex, Futures»,
https://www.metatrader5.com/en/terminal/help/trading_advanced/margin_forex, leída el 2026-10-12):
para forex, «Volume in lots * Contract size / Leverage», en la divisa de margen (la base, el EUR en
EURUSD), y convertida a la del depósito con el precio: «The Ask price is used for buy deals, and the
Bid price is used for sell deals». En USD:

    margen = lotes × instrumento_contrato × precio / firma_apalancamiento

**Las cifras** (anexo `anexos/ENTRADA-JULIO/margen_p_d1.py`, que lee el registro y el perfil y no
lleva ninguna cifra dentro; salida tal cual, también en `margen_p_d1.txt`):

```
PARAMETROS: saldo 100000 USD; riesgo_por_operacion 0.5 % = 500.0 USD; instrumento_contrato 100000; paso 0.01; firma_apalancamiento 1:30; firma_volumen_max_lotes 50; valor del pip 10.0000 USD por lote
TOPE DE VOLUMEN (50 lotes): stop minimo 1.00 pips
PRECIO 1.10: margen de 1,00 lote 3666.67 USD; lote maximo con todo el saldo como margen 27.27; stop minimo para el 0.5 % 1.83 pips
PRECIO 1.20: margen de 1,00 lote 4000.00 USD; lote maximo con todo el saldo como margen 25.00; stop minimo para el 0.5 % 2.00 pips
```

Es decir: **con todo el saldo como margen caben 27,27 lotes a 1,10 y 25,00 a 1,20, y el 0,5 % deja
de cumplirse con un stop de menos de 1,83 y 2,00 pips**: casi el doble del pip que corta el tope de
50 lotes. El margen manda antes que el volumen máximo. Y es un límite optimista: usar todo el saldo
como margen deja el margen libre a cero. Con la pauta de FTMO (20 % del margen, que no es regla) el
lote cabría hasta 5,45 a 1,10, y el corte subiría a unos 9 pips; se da solo como orden de magnitud.

**Partir en varias órdenes no lo arregla.** En una cuenta de cobertura, MT5 suma el volumen de las
posiciones del mismo lado: «Their volumes are summed up and the weighted average open price is
calculated for them» (misma página, «Calculation in the hedging system of position accounting»). Solo
las posiciones de lados opuestos se tratan como cubiertas, con el margen que fije el broker. Cinco
órdenes de 6 lotes piden el mismo margen que una de 30.

## 3. La prueba en la ejecución 2 de la demo

El script 1.1 ya lo calcula (`tools/mql5/MedirDemoFTMO.mq5:594-611`, `MargenAlcanza`): antes de la
compra de 1,00 lote del paso 6 (`InpVolumenComision`) pide `OrderCalcMargin(ORDER_TYPE_BUY, ..., 1,00,
ask)` y escribe «margen necesario X; margen libre Y» en la fila `volumen_comision` del CSV (`:622-623`).
Con el `ask` de esa misma fila, **la fórmula predice X = 100.000 × ask / 30** (3.900 USD con un ask de
1,17). Si el CSV de la ejecución 2 da otra cifra, el apalancamiento o la divisa de margen de la cuenta
no son los supuestos, y el apartado 2 se rehace con el valor medido. No hace falta cambiar el script.

## 4. Propuestas para la orden de cierre

- **O sale** de la Next Action: P-D1 está respondida (1 y 2) y registrada aquí; el 3 queda sin
  respuesta directa y no se vuelve a preguntar mientras el margen corte antes.
- **El texto nuevo del heredado 37:**
  > 37. **LOS RECHAZOS POR VOLUMEN Y POR MARGEN, EN LA RAMA DE STOP Y LOTE (A-18).** FTMO confirma 50
  > lotes en EURUSD y cuenta de cobertura (P-D1, `docs/validation/FTMO-P-D1.md`, 2026-10-12). Pero
  > antes que el volumen corta el MARGEN (ADR-0026, Impacto): con `firma_apalancamiento` 1:30, todo
  > el saldo como margen da 27,27 lotes a 1,10 y 25,00 a 1,20, y el 0,5 % deja de cumplirse con un
  > stop de menos de 1,83 y 2,00 pips (el tope de 50 lotes corta en 1 pip). Partir en varias
  > órdenes no lo arregla: MT5 suma el margen de las posiciones del mismo lado. El simulador no
  > comprueba el margen y `firma_apalancamiento` no lo lee ningún código del bot (deuda abajo). La
  > ejecución 2 de la demo comprueba la fórmula con el margen de 1,00 lote que ya escribe el
  > script 1.1 (`MargenAlcanza`).
- **Una línea de Technical Debt:**
  > El simulador no comprueba el margen: `firma_apalancamiento` no lo lee ningún código del bot, y el perfil
  > («Lo consume el broker simulado») y `parametros.yaml` («F21 lo comprueba») dicen lo contrario
  > (`docs/validation/FTMO-P-D1.md` §2). Rama propia: que el broker simulado rechace la orden cuyo
  > margen (lotes × instrumento_contrato × precio / firma_apalancamiento) pase del margen libre, con
  > un test que lo rompa en los dos sentidos, y que las dos descripciones digan la verdad.

No se cambia ningún código ni ningún parámetro en esta rama.

## Estado

Completo en la rama `trabajo/entrada-julio`, a la espera de su revisión y su cierre: la respuesta
registrada en paráfrasis, el margen medido y las propuestas escritas. Lo que falta es de otras ramas
(la ejecución 2 de la demo y la rama del margen).
