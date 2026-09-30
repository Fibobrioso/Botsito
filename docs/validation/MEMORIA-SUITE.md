# La memoria de la suite: `tracemalloc` a petición y el pico de `make check`

Rama `trabajo/memoria-suite`, 2026-09-29, sobre `main` en `7ff9a9c`. Punto A4 de `PROJECT_STATE.md`.
Sin cambios de estrategia, de spec ni de knowledge.

## 1. De dónde venía

El 2026-09-29 una corrida de la suite en segundo plano murió con el aviso de Claude Code «system
running low on memory». Ese recorte lo hace Claude Code con sus procesos en segundo plano cuando baja
la memoria LIBRE DEL SISTEMA, no la del proceso, y se evita arrancando Claude Code con
`CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1` (nota nueva en `CLAUDE.md`, *Trampas medidas*). Esta
sesión corrió con esa variable a 1, comprobado antes de lanzar nada.

La suite también tenía algo propio: casi todo su pico venía de UN test,
`test_la_cli_con_a47_fijada_pasa_a_pedir_a27` (753 MB y 192 s medido solo;
`ACTIVAR-SESION-03.md`, recuadro de corrección), que corre `motor arnes --simular` sobre un mes
entero, y `motor arnes` arrancaba siempre `tracemalloc`.

## 2. Qué cambia

1. **`motor arnes`** (`src/botsito/cli.py`): `tracemalloc` solo con `--tracemalloc`. Por defecto la
   línea `MEMORIA` da el pico del PROCESO, que lleva el sistema y leerlo no cuesta nada
   (`src/botsito/comun/memoria.py`: `PeakWorkingSetSize` de `GetProcessMemoryInfo` en Windows,
   `ru_maxrss` de `getrusage` en Linux). Con `--tracemalloc` se dan las dos cifras.
2. **`make check`** (`Makefile`, `scripts/pico_memoria.py`): cada paso corre dentro de `medir`, que
   apunta su pico en un acumulador del directorio de git (como el sello: git no lo sigue y no entra
   en la huella de la guardia), y la receta de `check`, que corre después de `sellar`, escribe UNA
   línea al final del log, `PICO DE MEMORIA de make check: <N> MiB en <paso> (...)`. En Windows mide con un Job Object: la
   memoria comprometida de la SUMA de los procesos del paso, y entre paréntesis la del mayor. En
   Linux (la CI), `ru_maxrss` del mayor proceso: el sistema no da la suma sin muestrear. La línea
   `check:` no cambia (desellar primero, sellar al final: lo congelan los tests del sello).
> **RECUADRO DE CORRECCION (2026-09-30, rama `fix/ci-linux-memoria`).** El primer test del punto 3
> no se probo en Linux y la CI de `67ab298` salio roja en el (run 36675429816: `141414400
> 141414400 141414400`, 1 failed, 1367 passed). No era la reserva: en Linux, `exec` conserva en
> `ru_maxrss` la RSS del proceso que hizo el fork, asi que el hijo lanzado directamente por pytest
> arrancaba ya con la de pytest (135 MiB), por encima de los 64 MiB de la reserva, y `antes`,
> `despues` y el final salian iguales. Windows no hereda ese contador. El test lanza ahora el hijo
> medido desde un intermediario pequeno; la reserva y las aserciones no cambian. El medidor de
> `make check` no se ve afectado: sus pasos los lanza `scripts/pico_memoria.py`, que es un proceso
> pequeno. La linea `MEMORIA` de `motor arnes` en Linux incluye, eso si, la RSS de su padre al
> lanzarlo, que desde una shell es despreciable. El cuerpo del informe queda intacto.

3. **Tests** (`tests/unit/test_memoria.py`, seis funciones, siete casos): el pico del proceso sube con
   una reserva de 64 MiB; `motor arnes` solo arranca `tracemalloc` si se pide; el medidor mide un
   hijo, devuelve su código, apunta cada paso y el informe da el mayor y vacía el acumulador; y todo
   paso de `check` en el Makefile va por `$(MEDIR)`. El medidor se prueba en subprocesos: en Windows
   mete en el Job al proceso que lo llama, y no debe ser el de pytest.
4. **Documentación**: `docs/runbooks/ARNES-MOTOR.md` (qué es la línea `MEMORIA`), `scripts/README.md`
   y la nota de `CLAUDE.md`.

## 3. Ninguna salida commiteada cambia

- **Los informes del arnés, byte a byte**, con el código de antes (`7ff9a9c`) y el de después, sobre
  construcción (42 días) con los diagnósticos A-35 `cierre_vela_contraria`, A-44 `sin_tope`, A-21
  `solo_una_zona_de_control`:

  | corrida | sha256 antes | sha256 después | tiempo antes | tiempo después |
  |---|---|---|---|---|
  | `motor arnes` | `edc6796c6ed51299…` | `edc6796c6ed51299…` | 275,6 s | 54,5 s |
  | `motor arnes --simular --diagnostico-a27 0` | `6dc03914bee95cce…` | `6dc03914bee95cce…` | 582,7 s | 92,1 s |
  | `motor arnes --tracemalloc` (después) | — | `edc6796c6ed51299…` | — | 274,5 s |

  El informe no lleva ni el tiempo ni la memoria, así que no podía cambiar; se comprueba igual. La
  línea de pantalla sí cambia, y ningún test ni documento commiteado la copiaba (buscado).
- **Ningún fichero seguido cambia al correr**: la guardia de la huella de `make check` lo vigila, y
  el sello de este commit lo prueba.

Con `--tracemalloc`, el mismo arnés tarda 274,5 s y el proceso llega a 211,2 MiB; sin él, 54,5 s y
85,5 MiB. `tracemalloc` multiplicaba por cinco el tiempo y por dos y medio la memoria del proceso.

## 4. El pico de `make check`, antes y después

Medido con el mismo instrumento las dos veces: `scripts/pico_memoria.py ejecutar -- make check`, un
Job Object que abarca TODO `make check` (Windows, memoria comprometida), con `data/` presente, en
esta máquina.

| | suma de procesos | mayor proceso | tiempo | tests |
|---|---|---|---|---|
| antes (`7ff9a9c`, `main`) | 844 MiB | 791 MiB | 15 min 31 s | 1369 passed |
| después (esta rama) | 330 MiB | 268 MiB | 10 min 31 s | 1376 passed |

El pico baja de 844 a 330 MiB (un 61 %), y el mayor proceso, que las dos veces es pytest, de 791 a
268 MiB. El tiempo, cinco minutos menos. Los 7 casos de más son los de `test_memoria.py`.

La línea nueva del log, en ese mismo `make check`:

```
PICO DE MEMORIA de make check: 278 MiB en `test` (suma de sus procesos, memoria comprometida, Windows; el mayor proceso, 268 MiB)
```

Es menor que la del instrumento externo (330 MiB) porque
mide PASO a PASO y no cuenta lo que vive durante todo `make check` -`make`, el shell, el `uv` de
cada receta y los medidores de fuera-; el mayor proceso coincide.

## 5. Lo que NO se hace aquí

- **La negativa por A-27 no se adelanta.** La propuesta de cambiar ADR-0057 §5 para que el arnés se
  niegue sin stops level ANTES de leer velas, como con A-47, queda anotada como PENDIENTE en
  `PROJECT_STATE.md` (A4) y no se aplica: la decide el consultor.
- No se toca el paralelismo de pytest ni las fixtures: sin `tracemalloc`, pytest entero se queda
  en 268 MiB (§4), y no hay pico que justifique tocarlos.
- El recorte de Claude Code depende de la memoria libre del SISTEMA: bajar el pico de la suite lo
  hace menos probable, no imposible. Lo que lo evita es la variable de la nota de `CLAUDE.md`.

## Estado

Rama lista para revisión, NO cerrada.
