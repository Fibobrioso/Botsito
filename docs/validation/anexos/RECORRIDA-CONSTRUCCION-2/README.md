# Anexos de RECORRIDA-CONSTRUCCION-2 (la re-corrida que cuenta, ADR-0070 §3)

Las salidas de la fase 2 de `trabajo/recorrida-construccion-2`
(`docs/validation/RECORRIDA-CONSTRUCCION-2.md`): la re-corrida que cuenta por ADR-0070 §3, la
primera con la comisión medida (ADR-0090 §3), el sello del respaldo M1 (ADR-0091), el motor de la
sesión 6 (F38n y F38o), la salida del método de ADR-0092 y la cuenta por mes de su §8, sobre toda la
construcción vigente (enero del 2 al 30, abril, julio del 1 al 17 y agosto de 2026;
`criterio_fidelidad.yaml`, `construccion`); su contexto con la cuenta diaria; los dos `diff` contra
la línea base anterior y los guiones que las leen. Este README existe ANTES de correr para que la
carpeta esté en git: el arnés no la crea (`cli.py`, `salida.write_text`). Lo que cada corrida lee
para calentar el sesgo H4 (el M1 entero de marzo, de junio y de julio; enero calienta desde su propio
mes, sin M1 de 2025-12) está declarado en `docs/validation/HOLDOUT-EXPOSICIONES.md` (fila del
2026-11-08) antes de correr nada.

## Las corridas del arnés (fase 2)

Desde la raíz del repositorio, sin `--meses`, sobre el código commiteado, una a la vez, en segundo
plano y nunca a la par de un `make check` (Claude Code arrancado con
`CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1`). Son los tres únicos comandos del arnés que autoriza
el encargo («Autorización expresa»):

1. **La que cuenta por ADR-0070 §3**, una cuenta por mes, sin ningún `--diagnostico-*`:
   `uv run botsito motor arnes --simular --salida docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/cuenta-por-mes.txt`
   → `cuenta-por-mes.txt`. **Pasa a ser la línea base vigente** desde esta rama (D2; la NOTA de
   ADR-0070 §3 y la de `docs/runbooks/ACTIVAR-A35-A44.md` §5); la de `anexos/RESPALDO-M1/` no se
   toca. No se edita.
2. **La de contexto**, cuenta reiniciada cada día (diagnóstico etiquetado: no cuenta ni habilita
   mayo):
   `uv run botsito motor arnes --simular --diagnostico-cuenta-diaria --salida docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/diaria.txt`
   → `diaria.DIAGNOSTICO.cuenta=diaria.txt` (el nombre lo pone `diagnostico.nombre_etiquetado`).
3. **La 1 repetida** con `--salida` en la carpeta de trabajo de la sesión, fuera del repositorio,
   comparada con `diff` contra la commiteada (determinismo, D10); la copia se borra y no se
   commitea.

## Los dos diff contra la línea base anterior (D3)

Desde la raíz (las rutas del encargo, relativas a `docs/validation/`, escritas enteras; `diff` sale
con 1 cuando hay diferencias: no es un fallo):

- `diff docs/validation/anexos/RESPALDO-M1/cuenta-arrastrada.txt docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/cuenta-por-mes.txt > docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/diff-linea-base.txt`
  → `diff-linea-base.txt`: mezcla el cambio del motor con el del camino de la cuenta.
- `diff "docs/validation/anexos/RESPALDO-M1/diaria.DIAGNOSTICO.cuenta=diaria.txt" "docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/diaria.DIAGNOSTICO.cuenta=diaria.txt" > docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/diff-diaria.txt`
  → `diff-diaria.txt`: sin el camino de la cuenta (la diaria no la toca la cuenta por mes).

## Los guiones, solo leen salidas

- `patrones.py` y `horas_perdidas.py`: copias IDÉNTICAS de las de `anexos/RESPALDO-M1/` (D4; ni una
  regla se ajusta). `patrones.py` importa `horas_perdidas` de su directorio.
  `uv run python docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/patrones.py <salida> --filas`
  → `patrones-cuenta-por-mes.txt` y `patrones-diaria.txt`, con el `sed` del CRLF como en
  RESPALDO-M1 §4.2. Con `--filas`: la cabecera es la de RESPALDO-M1 y detrás va cada fila con su
  patrón.
- `para_clasificar.py` (nuevo, D8): la lista «Para clasificar», de las dos salidas y nada más
  (ninguna vela, ningún tick, ningún caso). Lo que la salida no trae (el stop del trader; la
  dirección de una orden no llenada, que se lee de su caja) lo dice su docstring, y comprueba lo
  que cuenta contra la cascada que imprime cada salida.
  `uv run python docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/para_clasificar.py docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/cuenta-por-mes.txt "docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/diaria.DIAGNOSTICO.cuenta=diaria.txt"`
  → `para-clasificar.txt`. Al final, un resumen por mes de las órdenes sin trader (añadido en la
  fase 2, antes de commitear las salidas).

Añadidos en la fase 2 (para D5, D6 y D3, y para el alcance 4 del revisor), con la misma regla: solo
leen salidas commiteadas:

- `resumen_corrida.py`: lo que una salida imprime, repartido por mes, y lo que no imprime y se
  deriva de ella (la equity mínima y la peor pérdida diaria de CADA cuenta, con las funciones del
  criterio; RN-032 por las sesiones de «Por sesion»). Su docstring dice qué es derivado.
  `uv run python docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/resumen_corrida.py <salida>`
  → `resumen-cuenta-por-mes.txt` y `resumen-diaria.txt` (las dos de esta rama) y
  `resumen-respaldo-m1-arrastrada.txt` y `resumen-respaldo-m1-diaria.txt` (las dos de
  `anexos/RESPALDO-M1/`, para comparar).
- `diff_por_seccion.py`: un `diff` repartido por sección y por mes, sin imprimir ninguna línea.
  `uv run python docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/diff_por_seccion.py <vieja> <nueva> <diff>`
  → `diff-linea-base-por-seccion.txt` y `diff-diaria-por-seccion.txt`.
- `antes_del_dia.py`: la regla «(antes del dia)» sobre los ficheros de esta carpeta (ninguna fecha
  ni ningún `nivel@minuto` anterior al día de su fila; ninguna fecha fuera de la construcción).
  `uv run python docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/antes_del_dia.py <ficheros>`
  → `antes-del-dia.txt`.
- `docs/validation/anexos/SELLO-RESPALDO-M1/censo_cierre.py`, el de `main` y en su sitio (no se
  copia): las cancelaciones del bot en el cierre de una M1 sin ticks, las que SELLO-RESPALDO-M1.md
  §0.i dejó a la re-corrida (D6).
  `uv run python -B docs/validation/anexos/SELLO-RESPALDO-M1/censo_cierre.py <salida>`
  → `censo-cierre-cuenta-por-mes.txt` y `censo-cierre-diaria.txt`.
- `simular_cierre.py`: las líneas del cierre (RECORRIDA-CONSTRUCCION-2.md §6), en memoria sobre
  copias, contra `test_hoja_de_ruta` y `test_project_state`; en el repo no escribe nada.
  `uv run python -B docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/simular_cierre.py`
  → `simular-cierre.txt`.
Añadidos en la fase 3 (respuesta del consultor a la PARADA 2):

- `caja_stop.py` (punto 2): el stop del trader, leído de los casos dev por la compuerta del arnés,
  frente al de la orden del bot, con los signos y la regla de los dos tercios que su docstring
  explica.
  `uv run python docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/caja_stop.py docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/cuenta-por-mes.txt docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/para-clasificar.txt`
  → `caja-stop.txt`.
- `visor_sesiones.py` (punto 3): lo que las nueve páginas de `data/visor/` (ignoradas por git; las
  escriben los nueve `motor visor --simular --caso` del punto 3) dicen de cada sesión, comparado con
  la corrida 1, en horas de pared y sin precios.
  `uv run python docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/visor_sesiones.py data/visor docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/cuenta-por-mes.txt`
  → `visor-sesiones.txt`.
- `recuento_clases.py` (§8): los recuentos por patrón, mes y sesión del visor.
  `uv run python docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/recuento_clases.py docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/patrones-cuenta-por-mes.txt`
  → `recuento-clases.txt`.
- `salida_comun.py`: lo que comparten `caja_stop.py` y `visor_sesiones.py`, sin importar ningún
  otro guion de la carpeta. Así la cadena de carga del test de humo cabe en los tres niveles que
  admite la guardia; un test comprueba que lee las órdenes igual que `para_clasificar.py`.
- `test_humo.py`: sus tests de humo, sobre salidas sintéticas y en los dos sentidos; `make check` no
  los recoge (`testpaths = ["tests"]`):
  `uv run pytest docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/test_humo.py -q`.
  Qué viene copiado de `anexos/RECORRIDA-CONSTRUCCION/test_humo.py` y qué no, en su docstring.

### Las copias son idénticas

Desde `docs/validation/anexos/` (2026-11-08):

```
$ diff RESPALDO-M1/patrones.py RECORRIDA-CONSTRUCCION-2/patrones.py; echo "patrones diff=$?"
patrones diff=0
$ diff RESPALDO-M1/horas_perdidas.py RECORRIDA-CONSTRUCCION-2/horas_perdidas.py; echo "horas diff=$?"
horas diff=0
$ sha256sum RESPALDO-M1/patrones.py RECORRIDA-CONSTRUCCION-2/patrones.py RESPALDO-M1/horas_perdidas.py RECORRIDA-CONSTRUCCION-2/horas_perdidas.py
330b7d621273eb66e2b17993f8e85a9ea5606a0ead836f9468f80964241c63e6 *RESPALDO-M1/patrones.py
330b7d621273eb66e2b17993f8e85a9ea5606a0ead836f9468f80964241c63e6 *RECORRIDA-CONSTRUCCION-2/patrones.py
dfa782a3968713e097e9aa00f4988d147ace049fc4facfdaf20fdf70bddb4c6b *RESPALDO-M1/horas_perdidas.py
dfa782a3968713e097e9aa00f4988d147ace049fc4facfdaf20fdf70bddb4c6b *RECORRIDA-CONSTRUCCION-2/horas_perdidas.py
```

Los mismos hashes que RESPALDO-M1 dio para sus copias (RESPALDO-M1.md, «330b7d62… y dfa782a3…»).

### Los tests de humo, corridos (2026-11-08)

```
$ uv run pytest docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/test_humo.py -v -p no:cacheprovider
======================== 11 passed in 64.12s (0:01:04) ========================
$ uv run pytest docs/validation/anexos/RECORRIDA-CONSTRUCCION/test_humo.py -v -p no:cacheprovider
============================= 10 passed in 0.52s ==============================
```

En la fase 2, con los tests de `resumen_sin_trader` y de `antes_del_dia.py` añadidos:

```
$ uv run pytest docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/test_humo.py -v -p no:cacheprovider
============================= 13 passed in 0.78s ==============================
```

En la fase 3, con los de `caja_stop.py`, `visor_sesiones.py` y `salida_comun.py`:
`21 passed in 0.81s` (el mismo comando).

El segundo de arriba es el original, en su sitio e idéntico al de `main`: cubre lo que la copia no trae
(`test_la_lectura_vieja_rompe_sin_rotulo` y los de `entradas_antes_alternancia.py`).

Las líneas `TIEMPO` y `MEMORIA` de cada corrida van por pantalla, no al fichero: están en el informe
de la rama. Si una corrida muere o sale con un código distinto de 0, no se relanza (D9).
