# Anexos de `trabajo/activar-sesion-07` (ACTIVAR-SESION-07.md)

Escrito ANTES de correr nada (encargo, D0). Aquí van solo salidas de guiones que leen salidas: las
del arnés (`motor arnes --simular`) y de `patrones.py` se quedan en `data/activar-sesion-07/`, fuera
de git, y no son línea base de nada (encargo, «Sin corrida que cuente»).

## La corrida de julio de ADR-0093 §4 (D0)

Tres órdenes, cada una suelta, desde la raíz del repositorio, sobre código commiteado y nunca a la
vez que un `make check`; `<etiqueta>` es `base` (el código de `main`), `f1` (tras F1) o `f2` (tras
F2):

1. `uv run botsito motor arnes --simular --meses 2026-07 --salida data/activar-sesion-07/julio-<etiqueta>.txt`
2. `uv run python docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/patrones.py data/activar-sesion-07/julio-<etiqueta>.txt --filas > data/activar-sesion-07/patrones-julio-<etiqueta>.txt`
   y, después, `sed -i 's/\r$//' data/activar-sesion-07/patrones-julio-<etiqueta>.txt`.
3. `uv run python docs/validation/anexos/PREPARACION-SESION-7/pivote_julio.py data/activar-sesion-07/patrones-julio-<etiqueta>.txt`
   (sale con 1 cuando no da 14 y 39: no es un fallo, es el delta).

El delta, contra la línea base de `docs/plan/PIVOTES-SESION-7.yaml`: parejas = T0 − 14; operaciones
de más = (P5 + P6 en sesión) − 39. Y fila por fila, con `delta_julio.py` (abajo).

## Los ficheros

- `delta_julio.py`: `uv run python docs/validation/anexos/ACTIVAR-SESION-07/delta_julio.py <patrones base> <patrones nuevo> <arnés base> <arnés nuevo>`.
  Solo lee salidas: las filas de 2026-07 de dos salidas de `patrones.py` (las que cambian de
  patrón, aparecen o desaparecen) y el rn003 de cada sesión de julio de la línea «Por sesion» de
  dos salidas del arnés. **Desviación del encargo, declarada**: el encargo le da dos argumentos (los
  dos patrones); el rn003 de cada sesión no está en la salida de `patrones.py` (que solo lo usa para
  clasificar), así que lee además las dos salidas del arnés, solo esa línea.
- `pivote-julio-<etiqueta>.txt`: la salida de la orden 3 de cada corrida.
- `delta-julio-<de>-<a>.txt`: la salida de `delta_julio.py` entre dos corridas.
