# Blindar make check: un cambio en el árbol mientras corre no se sella

Rama `trabajo/blindar-make-check`, 2026-09-28, desde `main` en `stable/F20-preparar-a47`
(`9292e89`). Sale del incidente del instalador sobre copias de la rama `trabajo/preparar-a47`.

## 0. Lo que la rama deja, en cinco líneas

- **`make check` toma una huella del árbol de trabajo al empezar y otra al sellar.** Si difieren,
  sale en rojo con código 1, nombra los ficheros que cambiaron y no sella.
- **La exclusión es `.gitignore`, sin lista aparte.** Todo lo que `make check` escribe hoy dentro
  del árbol está ignorado, medido con una foto del árbol en dos corridas (§2).
- **Ningún test escribe en el árbol seguido ni en `data/`.** No hay hallazgo que tapar.
- **El coste es de 0,28 s y 1,5 MB por corrida.** La memoria de pico de `make check` no cambia de
  forma apreciable (§4).
- **Una regla nueva en `CLAUDE.md`**: ensayos en un clon desechable, la raíz por argumento o
  variable de entorno, y nada escribe mientras corre `make check`.

## 1. El incidente, y lo que el sello de antes ya cubría

En `trabajo/preparar-a47` (2026-09-28) un instalador de la Fase 2 se ensayó sobre copias sueltas
de seis ficheros. La copia del instalador se generó con `sed` para cambiar su ruta raíz por la de la
carpeta de ensayo; sobre una ruta de Windows, con sus barras invertidas, el patrón no casó, `sed` no
avisó, y la copia se ejecutó con la raíz real. Escribió en seis ficheros del repositorio mientras
`make check` corría sobre otro árbol estadiado. Se restauraron con `git checkout --`, se paró esa
comprobación y se relanzó limpia; ningún commit llevó nada de aquello.

**Lo medido en el código:** aquel incidente no habría producido un sello. `sellar` ya se negaba a
sellar si al final había cambios sin estadiar o ficheros sin seguir, y los seis ficheros quedaron
modificados sin estadiar. Pero `make check` habría terminado con código 0 y un simple aviso, y el
sello de antes dejaba pasar otros casos que la guardia sí ve:

| lo que pasa durante `make check` | sello de antes | con la guardia |
|---|---|---|
| un fichero seguido cambia y se queda sin estadiar | no sella; aviso y código 0 | **código 1**, lo nombra y no sella |
| un fichero sin seguir aparece y se queda | no sella; aviso y código 0 | **código 1**, lo nombra y no sella |
| un fichero cambia **y se estadía** | **sellaba el árbol nuevo, que nadie probó entero** | código 1 y no sella |
| un fichero cambia y se deshace antes del final | **sellaba**: los tests pudieron leer el otro contenido | código 1: el `mtime` lo delata |
| se hace un commit a mitad | **sellaba** el índice nuevo | código 1: nombra HEAD y los ficheros |
| un fichero sin seguir aparece y desaparece | no lo veía | **tampoco lo ve** (§3) |

## 2. Qué escribe hoy `make check` dentro del árbol

Medido con una foto de todos los ficheros del árbol de trabajo, menos `.git` y `.venv`, antes y
después de dos corridas completas de `make check` (script de lectura fuera del repositorio,
`mtime` y tamaño de cada fichero). La clasificación, con `git check-ignore -v` y
`git ls-files --others --exclude-standard`, que salió vacío después de las dos.

| qué | corrida 1: código sin cambios | corrida 2: con el código de esta rama | regla de `.gitignore` |
|---|---|---|---|
| `make-check.log` | creado | reescrito | `/make-check.log` |
| `.pytest_cache/` | 1 fichero | 1 fichero | `.pytest_cache/` |
| `.mypy_cache/3.12/cache.3.db` | modificado | modificado | `.mypy_cache/` |
| `.import_linter_cache/` | 2 ficheros | 2 ficheros | `.import_linter_cache/` |
| `.ruff_cache/` | nada | 1 fichero | `.ruff_cache/` |
| `.hypothesis/` | nada | 1 fichero nuevo | `.hypothesis/` |
| `__pycache__/` | nada | 2 bytecodes, uno el de `scripts/sello_make_check.py` | `__pycache__/` |
| ficheros seguidos | **ninguno** | **ninguno** | — |
| `data/` | **nada** | **nada** | `/data/*` |

Lo que cambia entre las dos corridas son las cachés que se reescriben cuando cambia el código. Todo
está ignorado, así que **no hace falta ninguna exclusión aparte de `.gitignore`**: la huella solo
mira ficheros seguidos y ficheros sin seguir fuera de `.gitignore`. Si mañana un test escribiera en
un fichero seguido, la guardia saltaría, y eso sería un hallazgo que corregir en el test, no algo
que excluir.

## 3. La guardia

`scripts/sello_make_check.py`. `borrar`, el primer objetivo de `make check`, borra el sello
anterior y toma la huella; la guarda en `git rev-parse --git-path botsito-huella`, junto al sello,
dentro del directorio de git, así que git nunca la sigue. `sellar`, el último, toma otra, la compara
con la guardada y la borra: la huella se consume.

**La huella** es un mapa ruta → estado, más el commit de HEAD:
- por cada fichero seguido, su entrada del índice (`git ls-files -s`: modo, blob y etapa) y el
  `mtime` en nanosegundos y el tamaño del fichero en disco;
- por cada fichero sin seguir fuera de `.gitignore`, `mtime`, tamaño y hash SHA-256 del contenido.

El índice ve lo que se estadía; el `mtime` ve cualquier escritura en un fichero seguido, aunque
luego se deshaga; HEAD ve un commit o un cambio de rama. Solo lee: no escribe nada en el árbol.

**Lo que no ve:**
- un fichero sin seguir que se crea y se borra entre las dos huellas;
- lo que se escriba en un fichero ignorado.

Lo segundo es lo que la exclusión quiere. Lo primero se cubre con la regla 3 de `CLAUDE.md`.

**`sellar` fuera de `make check`**, sin huella guardada, se comporta como antes. Lo usan el fixture
de los tests y la salida documentada del ritual, y los dos llaman antes a `borrar` cuando simulan
una comprobación completa.

## 4. Coste: tiempo y memoria, antes y después

`make check` completo, con el tiempo de pared y la memoria muestreados cada segundo: la suma del
working set de los procesos `python`, `uv`, `make`, `git` y `sh`, y la memoria libre del sistema.

| | antes (`9292e89`) | después (esta rama) |
|---|---|---|
| tiempo de pared de `make check` | 716,8 s | 727,9 s |
| tiempo de pytest | 652,1 s (1296 tests) | 668,8 s (1303 tests) |
| pico de memoria de los procesos | 281 MB | 284 MB |
| memoria libre mínima del sistema | 1758 MB | 1730 MB |

La huella sola, medida cinco veces sobre el repositorio real (1126 entradas): tomar dos huellas y
compararlas cuesta entre **0,273 y 0,285 s**, con un pico de **1,47 MB** de memoria de Python
(`tracemalloc`). Los siete tests nuevos suman unos 3,8 s. El resto de la diferencia de tiempo está
dentro de lo que varía una corrida a otra; la memoria de pico no cambia de forma apreciable.

## 5. Tests

En `tests/unit/test_sello_make_check.py`, todos sobre repositorios temporales con los hooks
versionados, sin tocar el repositorio real. Los tres primeros corren `make` con la línea `check:`
real del Makefile y un objetivo `test` simulado que escribe en el repositorio, como lo haría
cualquier cosa que corriera a la vez.

- `test_un_fichero_seguido_cambiado_durante_la_comprobacion_falla_y_no_sella`: el fichero se cambia
  y se estadía a mitad; `make` sale en rojo, el mensaje lo nombra y no hay sello.
- `test_un_fichero_sin_seguir_nuevo_durante_la_comprobacion_falla_y_no_sella`: lo mismo con un
  fichero sin seguir nuevo.
- `test_lo_que_make_check_escribe_de_verdad_no_dispara_la_guardia`: con el `.gitignore` real,
  escribe el log, las cachés y los bytecodes medidos en §2; `make` sale en verde y sella.
- `test_un_cambio_deshecho_antes_del_final_tambien_se_ve`.
- `test_un_commit_a_mitad_se_ve_como_head`: el commit se escribe con `commit-tree` y `update-ref`,
  que no pasan por hooks, para no saltarse ninguna puerta.
- `test_sin_cambios_la_guardia_deja_sellar_igual_que_antes`: con el árbol limpio el sello es el de
  siempre, y sin huella `sellar` sella como antes.
- `test_main_sale_con_1_si_la_guardia_salta`.

Tres tests existentes se ajustaron a la semántica nueva, sin cambiar lo que comprueban: en
`test_cambios_sin_estadiar_no_sella` y `test_fichero_sin_seguir_no_sella_pero_uno_ignorado_si` el
cambio que «ya estaba» va ahora antes de `borrar`; y en
`test_merge_no_ff_sin_sello_rechazado_y_queda_a_medias`, «sellar en la rama» es `borrar` más
`sellar`, que es lo que hace `make check`. Ese último falló en la primera corrida con la guardia, y
el fallo era correcto: llamaba a `sellar` con la huella de un `borrar` tomado en otra rama.

## 6. Estado

La guardia y sus tests están commiteados y sellados (`16113dc`); la regla de `CLAUDE.md`, la
ampliación del test de exclusiones con las cachés de la segunda corrida y este informe van en el
commit siguiente. **Rama lista para revisión, NO cerrada.**
