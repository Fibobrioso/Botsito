# tests/golden/
Salidas esperadas, revisadas a mano y versionadas. Un golden cambia solo con una decision
documentada. `ohlc/`: H4 del 2026-07-02 con dos anclajes (F15). Los golden de casos llegan con F14.
`journal/`: el journal v1 de la capa de MT5 (`mql5/JOURNAL.md`; trabajo/ea-conexion, R6a.1):
`continua/` es una cadena que sigue tras un reinicio y un cambio de dia, y `rota/` la cadena nueva
tras una ultima linea truncada. Los genera `docs/validation/anexos/EA-CONEXION/fase1/generar_golden.py`
y el script de pruebas de MQL5 (`mql5/Scripts/BotsitoPruebasCapa.mq5`) los escribe byte a byte con el
escritor del EA; `tests/unit/test_journal_mql5.py` fija el hash de la ultima linea de cada cadena, asi
que cambiar un byte rompe un test. Valores de prueba: ni el servidor, ni el simbolo, ni las horas son
de ninguna cuenta.
