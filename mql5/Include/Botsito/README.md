# mql5/Include/Botsito/ - dominio espejo y Params.mqh generado (F28, F29).

Desde R6a.1 (trabajo/ea-conexion, ADR-0082), `Capa/` guarda lo comun de la capa que nunca decide
una operacion, sin nada de la estrategia: `Journal.mqh` (el escritor del journal v1, `../../JOURNAL.md`),
`Cuenta.mqh` (la negativa fuera de DEMO y la lectura de la cuenta), `Reloj.mqh` (el reloj del
servidor y el cambio de dia) y `Sesiones.mqh` (las sesiones del simbolo). Los usan el EA y el script
de pruebas; se incluyen con `#include <Botsito/Capa/...>` y `/include` apuntando a `mql5/`.
