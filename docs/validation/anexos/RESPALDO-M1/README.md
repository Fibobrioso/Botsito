# Anexos de RESPALDO-M1 (R3.5, Z de la Next Action)

Las salidas de la fase 2 de `trabajo/respaldo-m1` (`docs/validation/RESPALDO-M1.md`): las dos corridas
de `trabajo/recorrida-construccion` repetidas con el respaldo M1 corregido (una vela solo evalúa lo
decidido antes de que empezara; ADR-0051 §5, NOTA del 2026-10-29), sobre toda la construcción vigente
(abril, julio del 1 al 17, agosto y enero del 2 al 30 de 2026; `criterio_fidelidad.yaml`,
`construccion`), y los guiones que las leen. Este README existe ANTES de correr para que la carpeta
esté en git: el arnés no la crea (`cli.py`, `salida.write_text`). Lo que cada corrida lee para
calentar el sesgo H4 (el M1 entero de marzo, de junio y de julio; enero calienta desde su propio mes,
sin M1 de 2025-12) está declarado en `docs/validation/HOLDOUT-EXPOSICIONES.md` antes de correr nada.

## Las corridas del arnés (fase 2)

Desde la raíz del repositorio, sin `--meses`, sobre el código commiteado, una a la vez, en segundo
plano y nunca a la par de un `make check` (Claude Code arrancado con
`CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1`, respuesta del consultor a la PARADA, punto 10):

1. **La que cuenta por ADR-0070 §3**, cuenta arrastrada, sin ningún `--diagnostico-*`:
   `uv run botsito motor arnes --simular --salida docs/validation/anexos/RESPALDO-M1/cuenta-arrastrada.txt`
   → `cuenta-arrastrada.txt`. **Pasa a ser la línea base vigente** desde esta rama (respuesta a la
   PARADA, punto 6; la NOTA de ADR-0070 §3 y la de `docs/runbooks/ACTIVAR-A35-A44.md` §5); la de
   `anexos/RECORRIDA-CONSTRUCCION/` no se toca. No se edita.
2. **La de clasificar**, cuenta reiniciada cada día (diagnóstico etiquetado: no cuenta ni habilita
   mayo):
   `uv run botsito motor arnes --simular --diagnostico-cuenta-diaria --salida docs/validation/anexos/RESPALDO-M1/diaria.txt`
   → `diaria.DIAGNOSTICO.cuenta=diaria.txt` (el nombre lo pone `diagnostico.nombre_etiquetado`).
3. **La 1 repetida** con `--salida` en la carpeta de trabajo de la sesión, fuera del repositorio,
   comparada con `diff` contra la commiteada (determinismo); la copia se borra y no se commitea.

`entradas_antes_alternancia.py` **no** se vuelve a correr (respuesta a la PARADA, punto 5).

## El diff contra la línea base anterior

`diff docs/validation/anexos/RECORRIDA-CONSTRUCCION/cuenta-arrastrada.txt docs/validation/anexos/RESPALDO-M1/cuenta-arrastrada.txt > docs/validation/anexos/RESPALDO-M1/diff-linea-base.txt`
→ `diff-linea-base.txt` (`diff` sale con 1 cuando hay diferencias: no es un fallo).

## Los guiones, solo leen

- `patrones.py` y `horas_perdidas.py`: copias IDÉNTICAS de las de `anexos/RECORRIDA-CONSTRUCCION/`
  (`patrones.py` importa `horas_perdidas` de su directorio). Ninguna regla de clasificación cambia.
  `uv run python docs/validation/anexos/RESPALDO-M1/patrones.py <salida>` → `patrones-arrastrada.txt`
  y `patrones-diaria.txt`.
- `censo_respaldo.py`: el censo de los eventos del respaldo M1 y el criterio de hecho de la rama
  (CERO eventos evaluados con una vela que empieza antes del instante en que se decidió lo
  evaluado), por la condición general y no solo por «colocada = evento − 1 ms» (respuesta a la
  PARADA, punto 5). Recibe las salidas por argumento; sale con 3 si hay modificaciones de orden que
  la salida no fecha. → `censo-respaldo.txt`, sobre las dos salidas nuevas y las dos de RECORRIDA.
- `sesiones_s14.py`: las 8 sesiones de S-14 de la sesión 6 (BARRIDO-SESION-6.md §1.d), en la diaria
  de RECORRIDA y en la nueva: si siguen siendo P6 y si su primera orden tiene la misma M1 de
  colocación, el mismo punto, el mismo precio y el mismo lado. **Sin ningún R.**
  → `sesiones-s14.txt`.

Las líneas `TIEMPO` y `MEMORIA` de cada corrida van por pantalla, no al fichero: están en el informe
de la rama. Si una corrida muere o sale con un código distinto de 0, no se relanza sin decirlo.
