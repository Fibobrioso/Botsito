# tests/golden/
Salidas esperadas, revisadas a mano y versionadas. Un golden cambia solo con una decision
documentada. `ohlc/`: H4 del 2026-07-02 con dos anclajes (F15). Los golden de casos llegan con F14.
`journal/`: el journal v1 de la capa de MT5 (`mql5/JOURNAL.md`; trabajo/ea-conexion, R6a.1):
`continua/` es una cadena que sigue tras un reinicio y un cambio de dia, y `rota/` la cadena nueva
tras una ultima linea truncada. Los genera `docs/validation/anexos/EA-CONEXION/fase1/generar_golden.py`
y el script de pruebas de MQL5 (`mql5/Scripts/BotsitoPruebasCapa.mq5`) los escribe byte a byte con el
escritor del EA; `tests/unit/test_journal_mql5.py` fija el hash de la ultima linea de cada cadena, asi
que cambiar un byte rompe un test. Valores de prueba: ni el servidor, ni el simbolo, ni las horas son
de ninguna cuenta. Congelado desde que existe la v2: lo sigue leyendo el lector v1.
`journal_v2/`: los mismos casos en el formato v2 (trabajo/capa-generada, R6a.2), con `capa_hash` en
todas las lineas igual a un hash FIJO de prueba (`0123456789abcdef` cuatro veces), para que el golden
no dependa de lo generado. Lo genera, desde `journal/`,
`docs/validation/anexos/CAPA-GENERADA/fase1/generar_golden_v2.py`; el script de pruebas de MQL5 lo
escribe byte a byte (`compilar.py pruebas --golden tests/golden/journal_v2`), y
`tests/unit/test_journal_mql5.py` fija el hash de la ultima linea de cada cadena.
`informe_simulacion/`: el informe de la simulacion de `main` (e01e28c) sobre el dia SINTETICO de 2030
de `tests/unit/test_cableado.py`, con tres rutas (`main-hueco.txt`, `main-stop.txt`, `main-viva.txt`),
generado en un clon desacoplado de `main` con
`docs/validation/anexos/METODO-FIDELIDAD-RENTABILIDAD/montar_volcado.py` (trabajo/metodo-fidelidad-rentabilidad).
`tests/unit/test_metodo_adr0092.py` exige que la salida de hoy empiece EXACTAMENTE por ellos (lo de
ADR-0092 va despues): un cambio de decision o de llenado en el dia sintetico rompe el test.
