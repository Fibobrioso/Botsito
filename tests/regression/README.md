# tests/regression/
Regresiones de fallos medidos: cada test fija el comportamiento correcto de un error que ya paso,
con el caso real que lo destapo. Los que necesitan `data/` (fuera de git) se saltan sin ella.

- `test_cuenta_7_de_agosto.py` · `evaluar_fase` y la marca en el instante del cierre
  (`trabajo/corregir-evaluar-fase`, VIABILIDAD-TRADER.md §6): la cuenta del 7 de agosto de
  construccion suspende por perdida diaria en el tick del pico, no antes. Necesita los ticks.
