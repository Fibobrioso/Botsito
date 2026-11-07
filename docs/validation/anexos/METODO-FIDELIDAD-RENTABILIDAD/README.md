# Anexo de `trabajo/metodo-fidelidad-rentabilidad` (ADR-0092)

Informe: `docs/validation/METODO-FIDELIDAD-RENTABILIDAD.md`. Ningún guion de aquí corre el arnés,
y ninguno escribe en el repositorio: imprimen, y la salida commiteada es esa impresión (con
`PYTHONUTF8=1` y pasada a LF). La raíz va siempre por argumento.

| Guion | Qué hace | Salida |
|---|---|---|
| `medir_a16.py <raiz> --filas` | A-16 medida (punto 3): la entrada de cada operación del trader de los días dev de construcción contra la M1 BID y los ticks de Dukascopy de su minuto, por la compuerta del arnés (`arnes.dias_de_construccion`, `simulacion.mercado_de_construccion`), sin el mes anterior | `medir-a16.txt` |
| `recuentos_vistos.py <anexos/RESPALDO-M1>` | sobre las DOS salidas ya vistas de `anexos/RESPALDO-M1/`: los días con la cuenta congelada (c) y la distribución de Δ por tramos (e), partida por lado | `recuentos-vistos.txt` |
| `huecos_material.py <raiz>` | los huecos de días de mercado entre días corridos (c), con las fechas sin datos de los manifiestos M1 de los cuatro meses de construcción | `huecos-material.txt` |
| `recuento_compuerta.py <raiz>` | `casos_reservados` y `casos_ocultos` por mes, y días dev y operaciones del trader por mes, sin claves ni fechas | `recuento-compuerta.txt` |
| `montar_volcado.py <test_cableado.py> <salida>` y `comparar_volcados.py <clon main> <clon rama>` | la regresión del punto 2: el volcado autocontenido del informe de la simulación de un día sintético de 2030 y su comparación byte a byte | `volcados-main-rama.txt` |
| — | los dos ficheros de test nuevos, ejecutados en un clon de `main` | `tests-campos-con-main.txt`, `tests-metodo-con-main.txt` |
| `simular_cierre.py` (punto 4) | las líneas del cierre, en memoria, contra `test_hoja_de_ruta` y `test_project_state` | `simular-cierre.txt` |

`medir_a16.py` lee días dev y velas: declarado ANTES de correrlo en `HOLDOUT-EXPOSICIONES.md`
(2026-11-07, fase 1).
