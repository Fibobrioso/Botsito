# Anexos de `trabajo/preparacion-sesion-7` (PREPARACION-SESION-7.md)

Los guiones de la fase 0, tal como se ejecutaron desde la carpeta de trabajo de la sesión (solo
leen; ninguno escribe en el repositorio), y sus salidas. Se ejecutan desde la raíz del repo con
`uv run python docs/validation/anexos/PREPARACION-SESION-7/<guion>`.

| Guion | Salida | Qué mide | Informe |
|---|---|---|---|
| `pivote_julio.py <patrones-cuenta-por-mes.txt>` | `pivote-julio.txt` | T0 y P5 + P6 en sesión de 2026-07 (sale con 1 si no son 14 y 39), y T0 + P2 + P3 + P7 | §0.3 y §0.7 |
| `dias_d3.py` | `dias-d3.txt` | D3 a) a c) por la compuerta (`casos_reservados` y `casos_ocultos`, solo contados) sobre las sesiones candidatas, y la condición b) sobre los 76 días dev | §0.4 |
| `sustitutas.py <caja-stop.txt> <para-clasificar.txt>` | `sustitutas.txt` | D3 d): las sustitutas de cada grupo de la caja, por cociente | §0.4 |
| `filas_por_sesion.py <patrones-cuenta-por-mes.txt> <dia:sesion> ...` | `filas-por-sesion.txt` | las filas de cada sesión candidata, por patrón | §0.4 |
| `ensayo_evidencia.py` | `ensayo-evidencia.txt` | lo que `evidence new` comprueba antes de escribir, sin escribir, para F7 #1, #2, #3, #6 y #10 (la salida no lleva el id calculado: los rechazados no existen) | §0.5 |
| `tres_fechas.py` | `tres-fechas.txt` | las tres fechas de «día anterior» que lleva `3e1995df`, contadas por la compuerta (`casos_reservados`, `casos_ocultos` y los días dev), sin imprimir ninguna; comprueba antes que son las de `3e1995df` y que las salidas de ahora no las llevan | «Respuesta del consultor a la PARADA final» |

Los guiones no pasan por el lint de `make check` (`Makefile:36-37`: `src`, `tests`, `scripts` y
`.claude/hooks`) y se dejan como se ejecutaron; `ensayo_evidencia.py` se cambió una vez para no
imprimir el id calculado, y `dias_d3.py` y `sustitutas.py` para no imprimir la fecha del día de
mercado anterior cuando no es de construcción (revisor de la rama, b7); sus salidas son las de
después del cambio. `simular_cierre.py` comprueba las propuestas de la orden de cierre sobre copias
en memoria (PARADA final del informe); no escribe nada.
