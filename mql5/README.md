# mql5/
Ejecucion en MetaTrader 5 (fase 6). Include/Botsito/Params.mqh se GENERA desde knowledge/spec/ (F28)
y no se edita a mano. Scripts/RunCases.mq5 ejecuta la biblioteca de casos (F30). tester/ guarda los .ini
y resultados del Strategy Tester (F32).

Desde R6a.1 (trabajo/ea-conexion, ADR-0082) vive aqui la capa que nunca decide una operacion: el EA,
lo comun en Include/Botsito/Capa/ y el script de pruebas, cada uno descrito en el README de su
carpeta. JOURNAL.md define el formato del journal que escribe el EA (v2 desde R6a.2,
trabajo/capa-generada: cada linea lleva el capa_hash de Include/Botsito/Capa/Generado.mqh, que se
genera con src/botsito/mql5bridge/generar_capa.py y no se edita a mano).
