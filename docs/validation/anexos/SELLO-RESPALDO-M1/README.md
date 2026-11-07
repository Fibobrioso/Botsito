# Anexos de SELLO-RESPALDO-M1 (R3.6, H de la Next Action)

Lo medido en la fase 0 de `trabajo/sello-respaldo-m1` (`docs/validation/SELLO-RESPALDO-M1.md`).
**Ninguna corrida del arnés y ninguna cifra agregada nueva** (regla del consultor para esta rama):
solo días concretos de construcción con el visor, tests, sondas sintéticas y salidas ya
commiteadas.

## Los guiones

| Guion | Qué hace | Lee | Salida |
|---|---|---|---|
| `censo_cierre.py` | reconstruye el `censo_cierre.py` de RESPALDO-M1 (§0.l, :351), que no está en el repo: las cancelaciones del bot en el cierre de una M1 de una hora sin ticks, fila a fila | una salida del arnés ya commiteada | `censo-cierre-recorrida.txt` (la diaria de RECORRIDA: 22 filas, el recuento de RESPALDO-M1) y `censo-cierre-respaldo-m1.txt` (la diaria de RESPALDO-M1: 26) |
| `horas_perdidas.py` | copia IDÉNTICA de la de `anexos/RESPALDO-M1/` (la importa `censo_cierre.py`) | — | — |
| `prototipo_sello.py` | (e2) y (c2) en memoria, con funciones escritas en el guion (sin `exec`), y el visor de la CLI por caso (`motor visor --caso <id> --simular`, páginas fuera del repo) | las M1 y los ticks de los días dados y el M1 del mes anterior para calentar | `prototipo-main.txt`, `prototipo-e2.txt`, `prototipo-c2.txt` (los once días) |
| `comparar_formas.py` | compara dos salidas del prototipo día a día: operaciones (entra o no, lado, vela de entrada, R) y órdenes | dos salidas del prototipo | `censo-main-c2.txt`, `censo-main-e2.txt` |
| `sondas_h.py` | las sondas S1-S9 del diagnóstico `diagH` (2026-10-31), copia con un cambio declarado en su cabecera (sin `sys.path.insert`) y ruff format | nada (velas sintéticas de 2030) | `sondas_main.txt`, `sondas_e2.txt`, `sondas_c2.txt` (en el clon `C:/cm/h`) |
| `simular_cierre.py` | las líneas del cierre en memoria contra `test_hoja_de_ruta` y `test_project_state` | PROJECT_STATE, la hoja de ruta y HISTORIA | `simular-cierre.txt` |

Los once días: 2026-01-14, 01-23, 04-03, 04-06, 04-07, 04-22, 04-23, 07-10, 07-16, 08-17 y
08-20 (los que las dos diarias ya commiteadas señalan), con 0 casos reservados por día y por mes
(`casos_reservados`).

## Lo medido en el clon de `main` (`C:/cm/h`, `git worktree add --detach`)

- `forma_c2_main2e04b63.diff` y `forma_e2_main2e04b63.diff`: las dos formas, escritas con Edit en
  el clon (la guardia niega `git apply`), con `git diff` del clon.
- `tests_c2.txt` y `tests_e2.txt`: 29 ficheros de test de `main` que tocan el bróker, el llenado, el
  cableado o la simulación (343 tests), con cada forma: (c2) 10 rotos; (e2) ninguno.
- `test_sonda5_main.txt`: el test nuevo de la rama, `tests/unit/test_peor_del_minuto.py`, copiado en
  el clon con el código de `main`: los dos primeros fallan y los otros dos pasan.

## Comandos (desde la raíz del repo, salvo los del clon)

    uv run python -B docs/validation/anexos/SELLO-RESPALDO-M1/censo_cierre.py "docs/validation/anexos/RECORRIDA-CONSTRUCCION/diaria.DIAGNOSTICO.cuenta=diaria.txt"
    uv run python -B docs/validation/anexos/SELLO-RESPALDO-M1/censo_cierre.py "docs/validation/anexos/RESPALDO-M1/diaria.DIAGNOSTICO.cuenta=diaria.txt"
    uv run python -B docs/validation/anexos/SELLO-RESPALDO-M1/prototipo_sello.py <main|e2|c2> <carpeta fuera del repo> 2026-01-14 2026-01-23 2026-04-03 2026-04-06 2026-04-07 2026-04-22 2026-04-23 2026-07-10 2026-07-16 2026-08-17 2026-08-20
    uv run python -B docs/validation/anexos/SELLO-RESPALDO-M1/comparar_formas.py docs/validation/anexos/SELLO-RESPALDO-M1/prototipo-main.txt docs/validation/anexos/SELLO-RESPALDO-M1/prototipo-c2.txt
    cd C:/cm/h && uv run python -B "C:/Users/USER/Desktop/Bot v3/docs/validation/anexos/SELLO-RESPALDO-M1/sondas_h.py" C:/cm/h <main|e2|c2>
    uv run python -B docs/validation/anexos/SELLO-RESPALDO-M1/simular_cierre.py

Las tres salidas del prototipo se repitieron tras el `ruff format` de los guiones y salieron
idénticas (salvo la línea `TIEMPO`).
