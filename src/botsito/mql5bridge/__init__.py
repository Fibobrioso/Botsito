"""Exporta spec y casos a MQL5; lanza compilacion y tester; parsea resultados (F28, F30).

Desde R6a.1 (trabajo/ea-conexion, ADR-0082): `journal` lee y valida el journal v1 de la capa de MT5
(`mql5/JOURNAL.md`), y `compilar` compila los fuentes de `mql5/` con MetaEditor desde una copia del
indice de git y lanza el script de pruebas en el terminal.
"""
