# Anexos de RECORRIDA-CONSTRUCCION-3 (la corrida (3), ADR-0070 §3, y la meta de ADR-0098)

Las salidas de `trabajo/recorrida-construccion-3` (`docs/validation/RECORRIDA-CONSTRUCCION-3.md`): la
corrida que cuenta por ADR-0070 §3 con el motor de la 7b (F39k) y una cuenta por mes (ADR-0092 §8),
sobre toda la construcción vigente (enero del 2 al 30, abril, julio del 1 al 17 y agosto de 2026;
`criterio_fidelidad.yaml`, `construccion`); su contexto con la cuenta diaria; la lectura del pivote de
ADR-0093 §6; los dos `diff` contra la línea base anterior; y la medida de la meta de ADR-0098 (el techo
del trader y el R de las parejas), pre-registrada en `539f7983` antes de correr nada. Este README existe
ANTES de correr para que la carpeta esté en git: el arnés no la crea (`cli.py`, `salida.write_text`).
Lo que cada corrida y el guion de la meta leen está declarado en
`docs/validation/HOLDOUT-EXPOSICIONES.md` (fila del 2026-11-22) antes de correr nada.

## Las corridas del arnés (fase 2)

Desde la raíz del repositorio, sin `--meses`, sobre el código commiteado, una a la vez, en segundo plano
y nunca a la par de un `make check` (Claude Code arrancado con
`CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1`). Son los tres únicos comandos del arnés que autoriza el
encargo («Autorización expresa»):

1. **La que cuenta por ADR-0070 §3**, una cuenta por mes, sin ningún `--diagnostico-*`:
   `uv run botsito motor arnes --simular --salida docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/cuenta-por-mes.txt`
   → `cuenta-por-mes.txt`. **Pasa a ser la línea base vigente** desde esta rama (D2; la NOTA de
   ADR-0070 §3); la de `anexos/RECORRIDA-CONSTRUCCION-2/` no se toca. No se edita.
2. **La de contexto**, cuenta reiniciada cada día (diagnóstico etiquetado: no cuenta ni habilita mayo):
   `uv run botsito motor arnes --simular --diagnostico-cuenta-diaria --salida docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/diaria.txt`
   → `diaria.DIAGNOSTICO.cuenta=diaria.txt` (el nombre lo pone `diagnostico.nombre_etiquetado`).
3. **La 1 repetida** con `--salida` en la carpeta de trabajo de la sesión, fuera del repositorio,
   comparada con `diff` contra la commiteada (determinismo, D11); la copia se borra y no se commitea.

Las líneas `TIEMPO` y `MEMORIA` de cada corrida van por pantalla, no al fichero: están en el informe.

## Lo que se lee de las corridas, con los guiones de `main` en su sitio (sin copiarlos)

- `patrones.py` (de `anexos/RECORRIDA-CONSTRUCCION-2/`), con el `sed` del CRLF:
  `uv run python docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/patrones.py <salida> --filas > <destino>`
  y `sed -i 's/\r$//' <destino>` → `patrones-cuenta-por-mes.txt` y `patrones-diaria.txt`.
- `pivote_julio.py` (de `anexos/PREPARACION-SESION-7/`), sobre los patrones de la corrida 1 (o de la 2,
  si la contingencia de ADR-0093 §6 lo pide): sale con 1 cuando no da 14 y 39, que no es un fallo
  → `pivote-julio.txt` (la corrida 1) y, como la contingencia aplicó (la cuenta de julio deja de
  llenar por RN-032 desde el 2026-07-10), `pivote-julio-diaria.txt` (la 2, la que se lee):
  `uv run python -B docs/validation/anexos/PREPARACION-SESION-7/pivote_julio.py docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/patrones-diaria.txt > docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/pivote-julio-diaria.txt`.
- `delta_julio.py` otra vez, de la corrida 1 a la diaria (D6):
  `uv run python -B docs/validation/anexos/ACTIVAR-SESION-07/delta_julio.py docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/patrones-cuenta-por-mes.txt docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/patrones-diaria.txt docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/cuenta-por-mes.txt "docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/diaria.DIAGNOSTICO.cuenta=diaria.txt"`
  → `delta-julio-cuenta-por-mes-diaria.txt`.
- `frenos_julio.py` (nuevo, D6): solo lee la corrida 1 y ese delta; por sesión de julio, las filas que
  cambian y el freno que dispara (RN-032 o RN-036 en «disparadas»), y por cuenta mensual la primera
  sesión con freno (de «Por sesion» y de las líneas «gate» de «Avisos») con su saldo al corte:
  `uv run python -B docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/frenos_julio.py docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/cuenta-por-mes.txt docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/delta-julio-cuenta-por-mes-diaria.txt`
  → `frenos-julio.txt`.
- `simular_cierre.py` (nuevo, §7): las líneas del cierre en memoria sobre copias, contra
  `test_hoja_de_ruta` y `test_project_state`; no escribe en el repo:
  `uv run python -B docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/simular_cierre.py` → `simular-cierre.txt`.
- Las salidas capturadas de la consola (`control.txt`, `meta.txt`, `pivote-julio*.txt`,
  `delta-julio-*.txt`, `frenos-julio.txt`) salen con CRLF en Windows; se les quitó el CR con
  `sed -i 's/\r$//'` antes de commitear, como a los patrones.
- `delta_julio.py` (de `anexos/ACTIVAR-SESION-07/`), el control de julio de D5:
  `uv run python docs/validation/anexos/ACTIVAR-SESION-07/delta_julio.py data/activar-sesion-08/patrones-julio-f2.txt docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/patrones-cuenta-por-mes.txt data/activar-sesion-08/julio-f2.txt docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/cuenta-por-mes.txt`
  → `delta-julio-f2-cuenta-por-mes.txt`.
- Los dos `diff` de D10 (sale con 1 si hay diferencias: no es un fallo), y su resumen por sección con
  `diff_por_seccion.py` (de `anexos/RECORRIDA-CONSTRUCCION-2/`):
  - `diff docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/cuenta-por-mes.txt docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/cuenta-por-mes.txt > docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/diff-linea-base.txt`
    → `diff-linea-base.txt` y `diff-linea-base-por-seccion.txt`;
  - `diff "docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/diaria.DIAGNOSTICO.cuenta=diaria.txt" "docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/diaria.DIAGNOSTICO.cuenta=diaria.txt" > docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/diff-diaria.txt`
    → `diff-diaria.txt` y `diff-diaria-por-seccion.txt`.
- `resumen_corrida.py` (de `anexos/RECORRIDA-CONSTRUCCION-2/`) → `resumen-cuenta-por-mes.txt` y
  `resumen-diaria.txt`.
- `para_clasificar.py` (de `anexos/RECORRIDA-CONSTRUCCION-2/`): pendiente de la decisión 0 de la fase 0
  (imprime un R por clase de órdenes, que ADR-0098 §4 c) no deja en esta corrida).

## La meta de ADR-0098 (fase 4)

- `techo_parejas.py`: el guion de la meta, con tres modos (`control`, `techo` y `parejas`), que repite
  órdenes con el mismo bróker simulado, la misma cuenta (una por mes, en la fase de la corrida) y la
  misma gestión que el bot, con el modelo de ADR-0098 §1. Lee `docs/plan/META-TECHO-PAREJAS.yaml` y
  `knowledge/cases/criterio_fidelidad.yaml` y escribe él mismo las lecturas y la salida A a D. Imprime
  solo lo que permiten ADR-0098 §1 y §4 c). Su docstring dice qué llama suelto del motor y qué
  reproduce. Comandos, salidas y orden: los fija la fase 4 en el informe y aquí, antes de correrlo.
- `test_techo_parejas.py`: su test de humo, sobre datos sintéticos (fechas de 2030), en los dos sentidos;
  `make check` no lo recoge (`testpaths = ["tests"]`):
  `uv run pytest docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/test_techo_parejas.py -p no:cacheprovider`.

Los comandos de la fase 4, desde la raíz y después de las corridas (los tres corren primero el control
y salen con 4 si no pasa: PARADA 4, ningún R del trader):

1. `uv run python -B docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/techo_parejas.py control docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/cuenta-por-mes.txt`
   → `control.txt`.
2. Si pasa: `uv run python -B docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/techo_parejas.py parejas docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/cuenta-por-mes.txt docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/patrones-cuenta-por-mes.txt docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/pivote-julio-diaria.txt`
   → `meta.txt` (el control, el techo, las parejas y la salida A a D con la precedencia del pivote).
   El último argumento es el pivote que se lee: el de la diaria, porque la contingencia aplicó (escrito
   antes de correr con `pivote-julio.txt`, que era el de la corrida 1; las parejas de M2 son siempre las
   de la corrida 1, ADR-0098 §1).

### Antes de correr (2026-11-22)

```
$ uv run ruff format docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/techo_parejas.py docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/test_techo_parejas.py
2 files left unchanged
$ uv run ruff check docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/
All checks passed!
$ uv run mypy docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/techo_parejas.py docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/test_techo_parejas.py
Success: no issues found in 2 source files
$ uv run pytest docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/test_techo_parejas.py -p no:cacheprovider -v
14 passed
```

**El ensayo del control** sobre `data/activar-sesion-08/julio-f2.txt` (julio, el motor de hoy; fila
complementaria del 2026-11-22 de HOLDOUT-EXPOSICIONES), con el guion en la carpeta de trabajo de la
sesión y el modo `control` solo (ningún R del trader): «posiciones del bot en la salida: 30; entran en
el control: 30; fuera: 0; reproducidas al centimo (lote, motivo, instante del cierre, PnL neto): 30 de
30; control: PASA». Un primer ensayo se paró en la lectura de «### Ordenes», que acaba en una línea de
resumen («ordenes: …»): `_seccion` para ahora en la primera línea sin columnas. Es un error de
lectura del guion, no una pieza del modelo.

**Tras el revisor (hallazgo b4):** la fila del control del test de humo copiaba una posición real de la
línea base anterior con el año cambiado; ahora sus valores son sintéticos (`o1`, 1,00 lotes, -100,00) y
el test de tres días se llama así. Mismo comando: `14 passed`. `techo_parejas.py` no cambia.
