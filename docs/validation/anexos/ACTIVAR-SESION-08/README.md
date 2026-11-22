# Anexos de `trabajo/activar-sesion-08` (ACTIVAR-SESION-08.md)

Escrito ANTES de correr nada (encargo, D0). Aquí van solo salidas de guiones que leen salidas: las
de `pivote_julio.py` y de `delta_julio.py`. Las del arnés (`motor arnes --simular`), las de
`patrones.py` y las de `motor decisiones` se quedan en `data/activar-sesion-08/`, fuera de git, y no
son línea base de nada (encargo, «Sin corrida que cuente»).

## La corrida de julio de ADR-0093 §4 (D0)

Las tres órdenes del recuadro del 2026-11-18 de ADR-0093 §4, cada una suelta, desde la raíz del
repositorio, sobre código commiteado y nunca a la vez que un `make check`; `<etiqueta>` es `base`
(el código de `main`, el control) o `f2` (tras F2):

1. `uv run botsito motor arnes --simular --meses 2026-07 --salida data/activar-sesion-08/julio-<etiqueta>.txt`
2. `uv run python docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/patrones.py data/activar-sesion-08/julio-<etiqueta>.txt --filas > data/activar-sesion-08/patrones-julio-<etiqueta>.txt`
   y, después, `sed -i 's/\r$//' data/activar-sesion-08/patrones-julio-<etiqueta>.txt`.
3. `uv run python docs/validation/anexos/PREPARACION-SESION-7/pivote_julio.py data/activar-sesion-08/patrones-julio-<etiqueta>.txt`
   (sale con 1 cuando no da 14 y 39: no es un fallo, es el delta).

**El control (desviación declarada del recuadro, del encargo):** el recuadro pide «OK: 14 y 39», que
con el motor de `main` ya no puede salir (la 7a está activada). El control es que la corrida `base`
repita la última de julio hecha con el motor de `main`, la de después de F2 de la 7a:
`anexos/ACTIVAR-SESION-07/pivote-julio-f2.txt`, y fila por fila contra
`data/activar-sesion-07/patrones-julio-f2.txt`, que sigue en la laptop.

El delta, contra la línea base de `docs/plan/PIVOTES-SESION-7.yaml` (parejas = T0 − 14; operaciones
de más = (P5 + P6 en sesión) − 39) y contra el control. Y fila por fila, con
`docs/validation/anexos/ACTIVAR-SESION-07/delta_julio.py <patrones base> <patrones nuevo> <arnés base> <arnés nuevo>`
(el guion de `main`, sin copiarlo).

## Los ficheros

- `pivote-julio-<etiqueta>.txt`: la salida de la orden 3 de cada corrida.
- `delta-julio-<de>-<a>.txt`: la salida de `delta_julio.py` entre dos corridas (`f39e-base` es el
  control: la F2 de la 7a contra la base de esta rama).
