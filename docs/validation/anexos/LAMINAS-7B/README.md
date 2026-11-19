# Anexos de `trabajo/laminas-sesion-7b` (LAMINAS-7B.md)

Solo salidas de guiones que imprimen recuentos de días de construcción. Ninguna lámina, ninguna
clave y nada que diga qué carpeta de láminas es qué sesión: eso va fuera del repositorio
(`clave.txt`, que guarda Aleks).

Cada orden, suelta, desde la raíz del repositorio y nunca a la vez que un `make check`, con su fila
de `HOLDOUT-EXPOSICIONES.md` antes:

- `h4_cargadas.py` (0.2; parte de `anexos/ACTIVAR-SESION-07/arranque.py`):
  `uv run python docs/validation/anexos/LAMINAS-7B/h4_cargadas.py` → `h4-cargadas.txt`. Las H4
  cerradas cargadas al abrir cada sesión del bloque de la 7b, cargadas como el arnés (el mes y el
  anterior; enero solo el suyo; abril calienta con marzo y julio con junio). Solo el recuento y si
  llega a 60; a diferencia de `arranque.py`, no imprime el sesgo.
- `compuerta_7b.py` (0.2; copia de `anexos/PREPARACION-SESION-7/dias_d3.py` que solo cambia
  `CANDIDATAS`): `uv run python docs/validation/anexos/LAMINAS-7B/compuerta_7b.py` →
  `compuerta-7b.txt`. La compuerta de ADR-0093 §3, a) a c), sesión a sesión.
- `filas-por-sesion-7b.txt`: `uv run python docs/validation/anexos/PREPARACION-SESION-7/filas_por_sesion.py docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/patrones-cuenta-por-mes.txt 2026-04-24:07-11 2026-04-27:11-15 2026-04-15:11-15 2026-01-19:11-15 2026-01-21:07-11 2026-01-22:11-15 2026-07-16:07-11`.
  Las filas de la clasificación de la línea base (antes de activar la 7a) de las siete sesiones.

Las tres salidas se copiaron a mano de la consola de su única ejecución (2026-11-18), sin volver a
correr nada.
