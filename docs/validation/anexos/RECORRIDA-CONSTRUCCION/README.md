# Anexos de RECORRIDA-CONSTRUCCION (R4.1, lo que queda: entradas V y F)

Las salidas de la fase 2 de `trabajo/recorrida-construccion` (`docs/validation/RECORRIDA-CONSTRUCCION.md`)
sobre toda la construcción vigente (abril, julio del 1 al 17, agosto y enero del 2 al 30 de 2026;
`criterio_fidelidad.yaml`, `construccion`), y los guiones que las leen. Este README existe ANTES de
correr para que la carpeta esté en git: el arnés no la crea (`cli.py`, `salida.write_text`). Lo que
cada corrida y cada guion leen para calentar el sesgo H4 (el M1 entero de marzo y de junio, meses
con días reservados) está declarado en `docs/validation/HOLDOUT-EXPOSICIONES.md`, fila del
2026-10-27, antes de correr nada.

## Las corridas del arnés (fase 2; autorización expresa del encargo del 2026-10-27)

Desde la raíz del repositorio, sin `--meses`, sobre el código commiteado:

1. **La que cuenta por ADR-0070 §3**, cuenta arrastrada, sin ningún `--diagnostico-*` y sin rótulo
   (la primera corrida que cuenta; `OPCIONES_QUE_NO_CAMBIAN_LA_CORRIDA`, `engine/arnes.py`):
   `uv run botsito motor arnes --simular --salida docs/validation/anexos/RECORRIDA-CONSTRUCCION/cuenta-arrastrada.txt`
   → `cuenta-arrastrada.txt`. **Es la línea base vigente** desde esta rama (respuesta del consultor a
   la PARADA, punto 4; `docs/runbooks/ACTIVAR-A35-A44.md` §5, NOTA); no se edita.
2. **La de clasificar**, cuenta reiniciada cada día (diagnóstico etiquetado: no cuenta ni habilita
   mayo; sobre ella se clasifican los patrones y se sacan las dos listas para la sesión 6):
   `uv run botsito motor arnes --simular --diagnostico-cuenta-diaria --salida docs/validation/anexos/RECORRIDA-CONSTRUCCION/diaria.txt`
   → `diaria.DIAGNOSTICO.cuenta=diaria.txt` (`diagnostico.nombre_etiquetado` añade el rótulo; cada
   línea empieza por `[DIAGNOSTICO-CUENTA-diaria] `).
3. **La 1 repetida** con `--salida` en una carpeta temporal fuera del repositorio, comparada con
   `diff` contra la commiteada para comprobar que el informe es determinista byte a byte; la copia
   se borra y no se commitea.

Las líneas `TIEMPO` y `MEMORIA` van por pantalla, no al fichero: están copiadas en el informe de la
rama. Si una corrida muere o sale con un código distinto de 0, PARADA sin relanzar (punto 7).

## El diff contra la línea base anterior

`diff docs/validation/CABLEADO-SIMULADOR-LINEA-BASE.txt docs/validation/anexos/RECORRIDA-CONSTRUCCION/cuenta-arrastrada.txt > docs/validation/anexos/RECORRIDA-CONSTRUCCION/diff-linea-base.txt`
→ `diff-linea-base.txt` (`diff` sale con 1 cuando hay diferencias: no es un fallo). Qué secciones
son comparables y cuáles cambian por el motor o por la construcción más amplia:
`RECORRIDA-CONSTRUCCION.md` §0.g y §3.

## Los guiones (fase 1), solo leen

- `patrones.py`: la clasificación PROVISIONAL por patrones del consultor (T0, P1 a P7 y «P? solo
  otro lado»), copiada de `anexos/CORRIDA-CONSTRUCCION/patrones.py` con **una sola diferencia**: el
  rótulo de diagnóstico se corta solo si la línea empieza por `[DIAGNOSTICO` (la copia de R3.1
  cortaba por el primer `"] "`, y sobre una salida SIN rótulo, como la corrida 1, se comía el
  principio de cada línea «Por sesion» y daba un P1 falso: `RECORRIDA-CONSTRUCCION.md` §0.e).
  Ninguna regla de clasificación cambia.
  `uv run python docs/validation/anexos/RECORRIDA-CONSTRUCCION/patrones.py <salida> [--filas]`
  → `patrones-arrastrada.txt` (corrida 1, contexto) y `patrones-diaria.txt` (corrida 2).
- `horas_perdidas.py`: copia IDÉNTICA de `anexos/CORRIDA-CONSTRUCCION/horas_perdidas.py`, porque
  `patrones.py` lo importa de su propio directorio (respuesta a la PARADA, punto 3); las 18 horas
  perdidas de los cuatro manifiestos de ticks no han cambiado (`RECORRIDA-CONSTRUCCION.md` §0.b).
- `entradas_antes_alternancia.py`: la lista «Entradas antes de la alternancia» (decisión 5 del
  encargo, respuesta a la PARADA, puntos 0, 1 y 2). Construye el motor como `cli.motor_arnes`, con
  la cuenta reiniciada cada día (reproduce la corrida 2, no la 1), corre los cuatro meses y lee la
  memoria del motor: por cada orden LLENADA, las zonas de control formadas desde la toma de su
  escenario al llenar y al colocar (`estructura_m1.zonas_de_control`), dónde estaba la orden
  (referencia / primer punto tras la toma / posterior), cuántas órdenes anteriores del escenario
  canceló RN-006, si la zona es de otro escenario, su R, su pareja o patrón, y el sesgo y el camino
  del bot en su sesión (para la lista «Para S-14»). Antes de escribir nada comprueba que sus órdenes
  llenadas coinciden una a una con las `llenada` de «### Ordenes» de la corrida 2; si no, sale con 3
  (PARADA). Comando autorizado, una sola vez y después de las tres corridas:
  `uv run python docs/validation/anexos/RECORRIDA-CONSTRUCCION/entradas_antes_alternancia.py --diaria "docs/validation/anexos/RECORRIDA-CONSTRUCCION/diaria.DIAGNOSTICO.cuenta=diaria.txt" --salida docs/validation/anexos/RECORRIDA-CONSTRUCCION/entradas-antes-alternancia.txt`
  → `entradas-antes-alternancia.txt`. Nada de lo que imprime es anterior a las 00:00Z del día dev
  (`antes_del_dia`, como `anexos/VISOR-CONSTRUCCION/comun_visor.py`).
- `test_humo.py`: los tests de humo de los dos guiones sobre salidas sintéticas, que rompen en los
  dos sentidos; no los recoge `make check` (`pyproject.toml`, `testpaths = ["tests"]`):
  `uv run pytest docs/validation/anexos/RECORRIDA-CONSTRUCCION/test_humo.py -q`
- `comparar_rn003.py`: el rn003 de cada sesión con operaciones del trader de abril y agosto en la
  línea base de 2026-09-26 frente a la corrida 1, porque «RN-003 al abrir» es un agregado de todas
  las sesiones y no se parte por mes en el diff (`RECORRIDA-CONSTRUCCION.md` §2.5). Solo lee las
  dos salidas. `uv run python docs/validation/anexos/RECORRIDA-CONSTRUCCION/comparar_rn003.py docs/validation/CABLEADO-SIMULADOR-LINEA-BASE.txt docs/validation/anexos/RECORRIDA-CONSTRUCCION/cuenta-arrastrada.txt`
  → `rn003-abril-agosto.txt`.
- `lista_s14.py`: la lista «Para S-14» (`RECORRIDA-CONSTRUCCION.md` §4): las sesiones de P6 de la
  corrida 2 (de `patrones.py` sobre la diaria) cruzadas con `entradas-antes-alternancia.txt` (el
  sesgo, el camino del bot y la R de cada llenada) y con `cuenta-arrastrada.txt` (la última sesión
  con un llenado de la corrida 1). Solo lee los ficheros de esta carpeta.
  `uv run python docs/validation/anexos/RECORRIDA-CONSTRUCCION/lista_s14.py docs/validation/anexos/RECORRIDA-CONSTRUCCION`
  → `lista-s14.txt`.

- `costes_y_sesiones.py` (respuesta del consultor a la PARADA 2, punto 1; `RECORRIDA-CONSTRUCCION.md`
  §2.8): las llenadas de la corrida 2 cuyo R se aparta más de 0,25 del de su motivo sin costes, con
  su causa leída en la salida y en los ticks; las sesiones con más de 4 llenadas; y el censo de los
  eventos del respaldo M1 de las dos corridas. Solo lee las salidas de esta carpeta y los ticks de
  los días dev en ventanas de un minuto (`data.ticks.cargar_ticks`); no corre el motor ni lee el
  calentamiento. `uv run python docs/validation/anexos/RECORRIDA-CONSTRUCCION/costes_y_sesiones.py`
  → `costes-y-sesiones.txt`.

- `simular_cierre.py` (respuesta a la PARADA 3, punto 1 c): aplica en memoria las líneas del cierre
  preparadas en `RECORRIDA-CONSTRUCCION.md` §6 con la letra que se le da, corre las funciones a, b y c
  de `tests/unit/test_hoja_de_ruta.py` y los cuatro tests de `tests/unit/test_project_state.py`
  sobre una copia fuera del repo, y mide PROJECT_STATE. No escribe en el repo.
  `uv run python docs/validation/anexos/RECORRIDA-CONSTRUCCION/simular_cierre.py . <letra>`.
- `lista_s14.py` marca además, desde la respuesta a la PARADA 3 (punto 1 a), las llenadas que el
  bróker hizo con la vela que colocó la orden («E: llenada con la vela que la colocó (ADR-0051 §2)»).

## Las salidas (fase 2)

`cuenta-arrastrada.txt` (corrida 1; la línea base vigente), `diaria.DIAGNOSTICO.cuenta=diaria.txt`
(corrida 2), `diff-linea-base.txt`, `patrones-arrastrada.txt` y `patrones-diaria.txt` (con `--filas`),
`entradas-antes-alternancia.txt`, `rn003-abril-agosto.txt` y `lista-s14.txt`. Las líneas `TIEMPO` y
`MEMORIA` de cada corrida, en `RECORRIDA-CONSTRUCCION.md` §2.

## Lo que no hay aquí

Ninguna vela, ninguna H4, ningún pivote de M15 ni ningún precio anteriores al día dev al que
pertenecen; nada de mayo ni de ningún mes reservado; ninguna página del visor (`motor visor --caso`
no se abre en esta rama: desviación declarada del runbook `ACTIVAR-A35-A44.md` §5).
