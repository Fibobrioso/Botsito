# anexos/DIAGNOSTICO-PREMISA · Los dos diagnósticos de construcción de ADR-0100

Rama `trabajo/diagnostico-premisa` (`docs/validation/DIAGNOSTICO-PREMISA.md`). Pre-registrado en
`7b97ca49` (ADR-0100 y `docs/plan/PREMISA-COSTES.yaml`, fijado por
`tests/unit/test_premisa_costes.py`) antes de que existiera ningún fichero de esta carpeta. Este
README entra en su propio commit antes de la primera corrida (encargo, fase 1).

## Qué es cada fichero

- `premisa.py`: el guion. Carga de `main`, por su ruta y sin copiarlo,
  `anexos/PUENTE-TECHO/puente.py` (que a su vez carga
  `anexos/RECORRIDA-CONSTRUCCION-3/techo_parejas.py`) y corre con sus funciones las variantes `base`
  y `todo_junto` de `PUENTE-TECHO.yaml` sin cambiar ninguna pieza (D1). Lee `PREMISA-COSTES.yaml`,
  `PUENTE-TECHO.yaml`, `META-TECHO-PAREJAS.yaml` y `knowledge/cases/criterio_fidelidad.yaml`; no
  lleva ninguna cifra de ellos dentro. Lee, por el lector de `corpus/libro.py` y solo de los días
  dev de construcción, las filas de los libros de enero, abril, julio y agosto de 2026 (rutas
  literales, verificadas contra `libros.yaml` por su sha antes de leer nada; D3). Dos modos, con la
  carpeta de salida como argumento: `control` (D2 a y b) y `todo` (las tres medidas con sus
  lecturas, con el entorno construido una sola vez; repite D2 a y b sobre sus propias corridas antes
  de medir). Sale con 0 si todo se hizo, con 4 si D2 a no pasa, con 5 si D2 b no pasa y con 2 ante
  un error de entrada. Escribe sus salidas en la carpeta que se le da (con saltos LF), no en la
  salida estándar.
- `test_premisa.py`: su test de humo, sobre datos sintéticos, en los dos sentidos. `make check` no lo
  recoge (`testpaths = ["tests"]`).
- `control.txt`: lo que escribe `premisa.py control` (D2 a y b).
- `base-repetida.txt` y `todo_junto-repetida.txt`: los bloques de las dos variantes regenerados por
  `premisa.py control`, para el `diff` contra `anexos/PUENTE-TECHO/base.txt` y `todo_junto.txt` desde
  su línea «## Variante» (D2 a).
- `premisa.txt`: lo que escribe `premisa.py todo` (D2 a y b otra vez, §5, el retroceso y §6).
- `lectura.txt`: las dos lecturas de ADR-0100, literales, que escribe `premisa.py todo`.
- `simular_cierre.py` y `simular-cierre.txt`: las líneas del cierre aplicadas en memoria sobre copias
  y medidas contra `test_hoja_de_ruta` y `test_project_state` (DIAGNOSTICO-PREMISA.md §6), y su
  salida; no escribe en el repo (la salida va a fichero por la redirección del comando). Lee el
  PROJECT_STATE de `main` de un fichero fuera del repo que se le da como argumento:
  `git show main:PROJECT_STATE.md > <carpeta>/ps-main.md` y
  `uv run python -B docs/validation/anexos/DIAGNOSTICO-PREMISA/simular_cierre.py <carpeta>/ps-main.md > docs/validation/anexos/DIAGNOSTICO-PREMISA/simular-cierre.txt`.

(Esta lista se amplió tras las corridas con estos dos ficheros, que no estaban previstos.)

## Comandos (desde la raíz; una corrida a la vez, nunca a la par de un `make check`)

```
uv run pytest docs/validation/anexos/DIAGNOSTICO-PREMISA/test_premisa.py -p no:cacheprovider
uv run python scripts/pico_memoria.py ejecutar -- uv run python -B docs/validation/anexos/DIAGNOSTICO-PREMISA/premisa.py control docs/validation/anexos/DIAGNOSTICO-PREMISA
tail -n +8 docs/validation/anexos/PUENTE-TECHO/base.txt | diff - docs/validation/anexos/DIAGNOSTICO-PREMISA/base-repetida.txt
tail -n +8 docs/validation/anexos/PUENTE-TECHO/todo_junto.txt | diff - docs/validation/anexos/DIAGNOSTICO-PREMISA/todo_junto-repetida.txt
uv run python scripts/pico_memoria.py ejecutar -- uv run python -B docs/validation/anexos/DIAGNOSTICO-PREMISA/premisa.py todo docs/validation/anexos/DIAGNOSTICO-PREMISA
```

`pico_memoria.py` (D9) escribe su línea en la salida estándar, que el guion no usa. D8
(determinismo): `premisa.py todo` otra vez, a una carpeta fuera del repositorio, y `cmp` de sus
`premisa.txt` y `lectura.txt` con los de aquí, byte a byte. Los comandos ejecutados, con su hora y
su salida, en el informe.

## Lo que no imprime

Ninguna operación con su R, sus precios ni su fecha; ningún R por clase de setup, por sesión ni por
dirección; ninguna vela ni ningún nivel; nada de un día que no sea dev (ADR-0100 §5-§6;
`que_no_imprime` del yaml). Por mes y por bloque, recuentos y medias; el retroceso, solo recuentos
por tramo y por bloque. Las cifras son diagnóstico de construcción (ADR-0092 §6, recuadro de
ADR-0100): ninguna fija ni cambia un valor.
