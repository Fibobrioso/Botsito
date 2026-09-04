# tests/golden/ohlc/
H4 del 2026-07-02 (dia del caso del trader) agregada desde `tests/fixtures/ohlc/EURUSD_2026-07-02.bi5`
con anclaje `00:00 Europe/Madrid` (`_madrid.csv`) y `17:00 America/New_York` (`_servidor.csv`).
Formato agregado (`ts_utc,...,volumen,duracion_min,n_m1,completa`). Dos velas se comprobaron a mano
contra las M1 (ver `tests/unit/test_golden_ohlc.py`). Regenerar solo si cambia ADR-0005.
