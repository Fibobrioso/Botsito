# A-16 · ¿de dónde salen las velas? Medición del 2026-09-09

Pregunta del consultor: *"pensé que los datos serían desde MT5, ya que ahí es donde se operará con
la cuenta de FundedNext"*. Esto es lo que hay, medido, no supuesto.

## 1. La demo de FundedNext no tiene histórico útil

Cuenta 34891752 en `FundedNext-Server 3`, EURUSD M1, pedido con `copy_rates_range` y forzando la
descarga con `copy_rates_from`:

| Mes | Velas M1 que sirve el bróker |
|---|---|
| enero 2026 | **0** (la primera vela disponible es del 2026-06-03 22:15 UTC) |
| mayo 2026 | **0** |
| junio 2026 | 27 571, pero **desde el día 3 a las 16:32** |

Los 40 casos del paquete de la sesión 1 son de **mayo y junio**. Con este histórico, mayo entero y
la primera semana de junio no existirían: el bróker no sirve lo que no tiene, y forzar la descarga
no lo cambia.

## 2. Cuando hay datos, los dos proveedores coinciden

Día 2026-06-10 completo, Dukascopy (nuestro dataset congelado `eurusd-m1-2026-06-9c45983f`) contra
MT5/FundedNext:

| Desplazamiento aplicado a MT5 | Velas comparadas | Idénticas | Mediana | p90 | Máx |
|---|---|---|---|---|---|
| ninguno | 1409 | 0 | 82 pt | 151 pt | 263 pt |
| −2 h | 1310 | 0 | 49 pt | 130 pt | 274 pt |
| **−3 h** | **1261** | **15** | **2 pt** | **3 pt** | **20 pt** |

1 punto = 0,00001. La diferencia real entre proveedores es de **2 puntos (0,2 pips) de mediana**,
que confirma lo medido en F15 ("M1 coincide con Dukascopy a 1-2 puntos").

**La trampa está en el reloj, no en los precios.** El módulo `MetaTrader5` de Python devuelve
`time` en **hora de servidor** (GMT+3), no en UTC. Sin corregirlo, la comparación da 8 pips de
diferencia y parecería que los proveedores no tienen nada que ver. Es exactamente el riesgo que
MASTER_PLAN H.2 (fila de los tres relojes) anota para F17 y F31, y con el que se tropieza a la
primera.

## 3. Qué se decide

- **El histórico sigue siendo Dukascopy** (ADR-0005): cubre 2026 entero, es público y
  reproducible, y está a 2 puntos del feed del bróker donde se puede comparar. MT5 no puede
  sustituirlo porque no tiene los meses del paquete.
- **MT5/FundedNext se usa para lo que sí aporta**: spread real, condiciones de ejecución, reloj de
  servidor y paridad con Strategy Tester (F17, F24, F30–F33). Ahí es donde el feed del bróker es la
  única verdad que cuenta.
- **La diferencia de 2 puntos entra como margen declarado en F26**, no como ruido ignorado: una
  regla que depende de romper "por una milésima" puede cambiar de decisión dentro de ese margen, y
  hay que contarlo como tal en la medida de fidelidad.
- Queda una tercera fuente en juego, que es la del trader: él backtestea en **FX Replay, que usa
  datos de Oanda**. Esta medición no la cubre.
