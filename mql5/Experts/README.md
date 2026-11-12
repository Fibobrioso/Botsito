# mql5/Experts/ - el EA (F31).

Desde R6a.1 (trabajo/ea-conexion, ADR-0082): `Botsito.mq5`, el EA de la capa que nunca decide una
operacion. Se niega fuera de una cuenta DEMO (lo primero de OnInit, y otra vez al conectar), lee la
cuenta, el reloj del servidor y las sesiones del simbolo del grafico, y lo escribe en el journal
(`../JOURNAL.md`; v2 desde R6a.2, con el `CAPA_HASH` de `Include/Botsito/Capa/Generado.mqh` en cada
linea). No llama a ninguna funcion de trading (`tests/contract/test_capa_mt5.py`). Las
ramas siguientes de R6a lo amplian. Se compila con `src/botsito/mql5bridge/compilar.py`, nunca
dentro del repo.
