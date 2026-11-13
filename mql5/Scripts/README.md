# mql5/Scripts/ - RunCases.mq5 para pruebas diferenciales (F30).

Desde R6a.1 (trabajo/ea-conexion, ADR-0082): `BotsitoPruebasCapa.mq5`, las pruebas dinamicas de la
capa de MT5 (la negativa con DEMO, CONTEST y REAL, el cambio de dia con fechas inyectadas, el SHA-256
y el escritor del journal contra `tests/golden/journal_v2/` desde R6a.2, con el capa_hash fijo de
prueba; y aparte, `capa/capa_hash.jsonl`, una linea con el `CAPA_HASH` real de `Generado.mqh` que
`compilar.py pruebas` compara con el del repo). No opera. Lo lanza
`src/botsito/mql5bridge/compilar.py pruebas` con `terminal64.exe /config`, y su salida va a los
anexos de la rama.
