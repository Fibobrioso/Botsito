# GUARDIA-FFMPEG · ffprobe y ffmpeg sobre un vídeo que no se protege, por lista cerrada

Rama: `trabajo/guardia-ffmpeg`, abierta el 2026-10-22 desde `main` en `8cfed04` (commit de estado
sobre el merge `e044b15`, tag `stable/F37z-hoja-sesion-05`). Encargo:
`docs/encargos/trabajo-guardia-ffmpeg.md`. NA:K (la parte de ffprobe y ffmpeg, ampliada a
`volumedetect` y a la extracción del audio: ampliación declarada por el encargo), hoja de ruta G.1,
carril de guardias y deuda. Las otras dos partes de K (el falso positivo de `exigir_sin_crudo` y los
tests de un clon de `comparar-con-main`) no van aquí y siguen en K; G.1 no pasa a HECHA.

## Base comprobada al abrir

- `git fetch --prune origin`; `git status --short` vacío en `main`.
- `git rev-parse main origin/main`: `8cfed041c59cb3db319346cc19330fff6ad96175` las dos veces.
- `git rev-parse main^1` = `git rev-parse "stable/F37z-hoja-sesion-05^{commit}"` =
  `e044b15dbafd3fa61923e8009acd0f1dbd1d9285`; el tag está en origin (`git ls-remote --tags`:
  `49d58cf… refs/tags/stable/F37z-hoja-sesion-05`), y es el último `- Tag:` de `docs/state/HISTORIA.md`.
- CI de `main` sobre `8cfed041c59cb3db319346cc19330fff6ad96175` (check-runs): `python completed
  success`, run 39806538052.
- Ninguna otra rama: `git branch --list -a` da solo `main` y `origin/main`; `git ls-remote --heads
  origin` da solo `refs/heads/main`.
- Primer commit `0252d4f` (encargo, contrato y Archivo 43), sellado: `make check` exit 0, 2734
  passed, `SELLO … fb436c89…`.

## §0 · Fase 0

### 0.1 La medida del auditor, reproducida

Con `decidir` de la guardia del repo (idéntica a la de `main` en ese momento) sobre el texto de
cada comando, en un repo de `tmp` con los vídeos inventados y SIN SEGUIR -como el vídeo real de una
sesión, que vive en `corpus/`, fuera de git-; ffmpeg no se ejecutó y el corpus no se tocó. Guion en
la carpeta de trabajo (`fase0.py`), ejecutado con el Python del sistema:

| Caso | Comando | Decisión | Regla | Mensaje (primera línea) |
|---|---|---|---|---|
| ffprobe sobre un vídeo | `ffprobe -v error -show_format -show_streams "corpus/Estrategia del trader/sesion-05.mp4"` | NIEGA | R_EJECUCION | ejecutar `ffprobe`: la guardia no sabe con que se ejecuta corpus/…/sesion-05.mp4 (ni extension ni `#!`). |
| ffprobe, absoluto | `ffprobe -v error -show_format "<tmp>/repo/corpus/…/sesion-05.mp4"` | NIEGA | R_EJECUCION | ídem |
| ffprobe, vídeo sin seguir en `videos/` | `ffprobe -v error -show_format videos/sesion.mp4` | NIEGA | R_EJECUCION | ídem |
| silencedetect | `ffmpeg -hide_banner -nostdin -i "<vídeo>" -vn -sn -dn -af silencedetect=noise=-50dB:d=30 -f null -` | NIEGA | R_EJECUCION | ejecutar `ffmpeg`: la guardia no sabe con que se ejecuta … |
| volumedetect | `ffmpeg -hide_banner -nostdin -i "<vídeo>" -vn -sn -dn -af volumedetect -f null -` | NIEGA | R_EJECUCION | ídem |
| extracción dentro del repo | `ffmpeg -i "<vídeo>" -vn -sn -dn -ac 1 -ar 16000 audio.wav` | NIEGA | R_EJECUCION | ídem |
| extracción fuera del repo | `ffmpeg -i "<vídeo>" -vn -sn -dn -ac 1 -ar 16000 "<tmp>/fuera/audio.wav"` | NIEGA | R_EJECUCION | ídem |
| ffprobe sobre marzo | `ffprobe -v error -show_format "corpus/…/Material adicional de su operativa/Backtest marzo 2026/v.mp4"` | NIEGA | R_SIN_ABRIR | ejecutar corpus/…/Backtest marzo 2026/v.mp4. |
| ffmpeg sobre marzo | `ffmpeg -i "<marzo>/v.mp4" -vn -sn -dn -af volumedetect -f null -` | NIEGA | R_SIN_ABRIR | ídem |
| ffprobe sobre un vídeo que no existe | `ffprobe -v error -show_format videos/no-existe.mp4` | PASA | — | — |

Coincide con la medida del encargo: no hay PARADA. Un matiz medido, que no la contradice: en el
primer ensayo el vídeo inventado estaba COMMITEADO en el `main` del repo de `tmp`, y entonces todo
PASABA (un fichero idéntico al de `main` es «código revisado», `_igual_que_en_main`). El vídeo real
no está en git, así que la medida que cuenta es la de la tabla; el test nuevo crea los vídeos
después del commit, sin seguir, por eso mismo.

### 0.2 Los tests que tienen que seguir en verde

`test_ejecucion_lo_que_no_esta_en_la_lista_es_una_ejecucion`,
`test_ejecucion_lo_que_si_se_puede_decidir_pasa`,
`test_ejecucion_una_sola_funcion_y_ninguna_via_decide_por_su_cuenta`,
`test_el_ritual_y_los_runbooks_pasan` y `test_ninguna_denegacion_toca_el_ritual`: ninguno nombra
ffmpeg ni ffprobe, y siguen en verde con la regla (§2).

## §1 · La regla

En `.claude/hooks/guardia.py`, una función propia, `_analizar_ffmpeg`, con su constante de regla,
`R_FFMPEG`, y su «Como reescribirlo», `COMO_FFMPEG`. Entra en `analizar_comando` justo antes de la
llamada a `_ejecucion_de_un_programa_desconocido`, para `ffmpeg` y `ffprobe` (`PROGRAMAS_FFMPEG`) y
solo si el contexto no es PowerShell (`not ctx.powershell`): en PowerShell no cambia nada.

**Lista cerrada** (constantes, cada una con su patrón de valor):

1. **ffprobe** (`FFPROBE_CON_VALOR`, `FFPROBE_SIN_VALOR`): `-v`, `-loglevel`, `-hide_banner`,
   `-show_format`, `-show_streams`, `-show_entries`, `-of`, `-print_format`, `-select_streams`, y
   un único fichero de entrada, posicional o con `-i`. Ninguna más.
2. **ffmpeg, medida**: generales (`FFMPEG_GENERALES_*`: `-hide_banner -nostdin -nostats -y -n`,
   `-v X`, `-loglevel X`) en cualquier sitio; un `-i <vídeo>`; DETRÁS de él `-vn -sn -dn` (las tres)
   y `-af` con valor SOLO `silencedetect=noise=<número>dB:d=<número>` o SOLO `volumedetect`, y
   `-f null`; la salida, el último argumento, `-`, `NUL` o `/dev/null` (`SALIDAS_NULAS`).
3. **ffmpeg, extracción**: generales; un `-i`; detrás `-vn -sn -dn`, y opcionales `-ac N`, `-ar N`,
   y `-c:a X` o `-acodec X` (no los dos) (`FFMPEG_EXTRACCION_CON_VALOR`); UNA salida, la última,
   con extensión `.wav`, `.flac`, `.mp3` o `.m4a` (`EXTENSIONES_DE_EXTRACCION`, propia: no reutiliza
   `EXTENSIONES_AUDIO` de `transcribir_sesion.py`) y FUERA de la raíz del repositorio
   (`Politica.relativa` es None). Sin `-f`, `-map`, `-af` ni `-filter_complex`.

Y la forma en ffmpeg: antes de `-i` solo van generales (una opción de salida antes de `-i` sería
de ENTRADA: `-f concat -i lista`); ninguna opción se repite; nada va detrás de la salida.

4. **Cada fichero de entrada** (`_ffmpeg_ruta`): un solo valor resoluble (sin glob, sin expansión de
   llaves, sin variable desconocida, sin `$(...)`), que no sea `-` ni lleve prefijo de protocolo
   (`_PROTOCOLO`: los caracteres de esquema de ffmpeg seguidos de `:` o `,` -`concat:`, `file:`,
   `subfile,`-; una letra de unidad con su barra, `C:/` o `C:\`, no lo es; `C:x`, sí), sin `%` (un
   patrón de secuencia son muchos ficheros), que no empiece por `\\` o `//` (`\\?\C:\…`, `\\.\`,
   una ruta de red), que no sea un directorio, y que pase `motivo_fichero` POR SU TEXTO Y RESUELTA
   (`os.path.realpath`: un enlace o un nombre corto 8.3 de Windows): sobre material protegido niega
   con su motivo, con el mensaje de `main` («ejecutar <ruta>. Regla: …»). Y si existe, BINARIA: un
   fichero cuyos primeros 4096 bytes no llevan ningún nulo se niega, porque ffmpeg detecta por el
   CONTENIDO, no por la extensión, una lista que nombra otros ficheros (`ffconcat version 1.0`,
   `#EXTM3U`, un `.mpd`); un vídeo o un audio llevan nulos en su cabecera. La salida de la
   extracción pasa por las mismas comprobaciones de protocolo, `%` y `\\`, y «fuera del repo» se
   mira también resuelta (`_ffmpeg_dentro_del_repo`). (Lo de `\\`, `realpath` y la entrada de
   texto entró tras el revisor: b3 y «lo que no pude comprobar».)
5. **El resto de la línea**: lo que va antes y a la vez en el mismo comando se exige igual que en
   `main`, con las dos piezas de la familia 3 (`_exigir_lo_de_antes`: delante solo `cd` literal
   -no `cd -`-, asignaciones literales, `export` o `set -e/-u/-o pipefail`; `_exigir_lo_de_a_la_vez`:
   detrás en la tubería solo filtros, y nada en segundo plano), que niegan con `R_EJECUCION`; los
   nombres de entorno, igual (`FFREPORT` sigue negado por `NOMBRES_DE_ENTORNO`, con `R_EJECUCION`).
   En estas formas, además, se niega: ir dentro de un `$(...)`; una sustitución en el comando
   (`$(...)`, acentos graves, `<(...)`); CUALQUIER redirección de entrada (`<`, `<>`, `<<`: la
   medida no lee de la entrada estándar; `1<>fichero` escribiría); y una redirección de la salida
   estándar o de errores a un fichero DENTRO del repo, por su texto o resuelto (o a uno que se
   construye al ejecutarse). `2>&1` y los dispositivos nulos pasan. La primera versión (`4dbb48b`)
   NO llamaba a `_exigir_lo_de_antes` ni a `_exigir_lo_de_a_la_vez`, y con eso pasaban
   `find <dir que contiene el repo> -exec ffprobe {} ;`, `cd X && cd - && ffprobe …`, `| tee` y `&`
   (revisor, b1, b2 y b4): corregido, y cada uno es ahora un caso de la matriz.
6. **Excepción a la familia 3, declarada**: estas cuatro formas YA NO pasan por
   `exigir_ejecucion_verificable`: lo que se deja es LEER UN GUION -no lo hay: lo que ejecutan es
   ffmpeg, y sus ficheros son datos de audio y vídeo-; lo que va antes y a la vez se sigue
   exigiendo con las mismas dos funciones, y en lugar del guion se comprueba la lista cerrada.
   Escrito en la cabecera de `guardia.py`, en la familia 3. `ffprobe` sale de
   `SIN_LECTURA_DE_RUTAS` (cambio declarado; ya no se llegaba a consultar). Lo que no encaja en
   ninguna forma se niega con `R_FFMPEG` -no vuelve a la regla del programa desconocido-: «todo lo
   demás negado». `DISPOSITIVOS_NULOS` admite `NUL` y también `nul` (Windows no distingue
   mayúsculas en los nombres de dispositivo): el encargo dice «NUL o /dev/null»; declarado.
7. **«Fuera del repo» no protege el fichero de una lectura posterior**: el audio extraído queda
   donde la guardia no mira, y un Read o un `cat` posterior de ese fichero no lo para nada. Es
   aceptable porque es audio binario (`.wav`, `.flac`, `.mp3`, `.m4a`), que no se lee como texto; y
   el audio de una sesión es la entrada de `transcribir_sesion.py --audio`, que ya es la puerta de
   la cuarentena.

Nada de esto ha necesitado algo que la guardia no supiera ya del comando (sus palabras resueltas,
sus redirecciones, el nivel y la secuencia): sin PARADA.

## §2 · El test: `tests/unit/test_guardia_ffmpeg.py`

Un fichero nuevo (el de `test_guardia_claude.py` no se toca: si cambiara, la guardia lo leería
entero como código de la rama y sus literales del material la harían negarlo). Monta su propio repo
de `tmp_path` con los vídeos SIN SEGUIR y binarios (el principio de un mp4), y las rutas del
material a trozos por la misma razón.

- `test_la_matriz_de_ffmpeg`: 75 comandos (16 que pasan y 59 negados) con su decisión esperada
  -las cuatro formas, con rutas relativas y absolutas, a `-`, `NUL` y `/dev/null`, con
  `2>&1 | grep`, con `2>` fuera del repo y tras `cd`, y las cuatro formas exactas de la skill; y
  todos los negados que pide el encargo y algunos más, entre ellos los doce del revisor: `find
  -exec ffprobe {}`, `cd -`, `cd` dinámico, `cp` y `cd … || true` delante, `| tee`, `&`, una
  sustitución en el mismo comando, `1<>`, `< fichero`, un directorio y una entrada de texto
  `ffconcat` con extensión `.mp4` (tabla en el anexo, §A)-.
- `test_un_alias_de_la_raiz_no_saca_la_salida_ni_abre_la_entrada` (solo Windows): la salida a
  `\\?\<raíz>\a.wav` y a `<raíz en 8.3>\a.wav` se niega, y `ffprobe` sobre `<raíz en
  8.3>\…\marzo\v.mp4` niega con `R_SIN_ABRIR`. Medido en esta máquina con el nombre corto real de
  la raíz del repo de `tmp` (`…\PYTEST~1\…\TEST_U~1\repo`): si el volumen no tiene nombres 8.3, la
  parte 8.3 no se puede probar y el test lo dice.
- `test_sin_la_regla_las_permitidas_vuelven_a_negarse`: roto a propósito, con `PROGRAMAS_FFMPEG`
  vacío las 16 permitidas vuelven a negarse con `R_EJECUCION` (salida en §A.2).
- `test_con_una_opcion_de_mas_un_negado_pasa`: roto a propósito en el otro sentido, con `-map` en
  la extracción y `-report` en ffprobe, los dos negados correspondientes PASAN (salida en §A.2).
- `test_la_matriz_frente_a_la_guardia_de_main`: la misma matriz con la guardia de `main` (cargada
  de `git show main:` o `origin/main`, como `test_la_guardia_frente_a_la_de_main_caso_a_caso`),
  con `decidir`. Exige que ningún caso pase a PASAR fuera de las formas permitidas y que ninguna
  permitida se niegue. Ya en `main`, las dos guardias son la misma y no cambia ninguno.

### Casos que cambian de decisión frente a `main`

**De NIEGA a PASA: solo las cuatro formas permitidas**, los 16 casos de `PERMITIDAS` (ffprobe
relativa, absoluta con `-i`, con `-print_format`; silencios relativa y absoluta a `NUL`; volumen a
`/dev/null`, absoluta y con `2>` fuera del repo; extracción absoluta, relativa `../fuera`, `.mp3` y
`.m4a` tras `cd`; y las cuatro de la skill). En `main` todas niegan con `R_EJECUCION`.

**De PASA a NIEGA (endurecimiento, declarado)**: nueve casos que `main` dejaba pasar porque el
argumento no es un fichero que exista (o es un directorio) y la regla del programa desconocido
solo mira ficheros:

| Caso | main | rama |
|---|---|---|
| protocolo `concat:` | pasa | R_FFMPEG |
| protocolo `subfile,` | pasa | R_FFMPEG |
| protocolo `file:` | pasa | R_FFMPEG |
| protocolo en ffprobe | pasa | R_FFMPEG |
| **protocolo sobre marzo** (`ffprobe -show_format "file:<marzo>/v.mp4"`) | **pasa** | R_FFMPEG |
| letra de unidad sin barra (`C:x.mp4`) | pasa | R_FFMPEG |
| una entrada con `%d` | pasa | R_FFMPEG |
| `ffmpeg -version` | pasa | R_FFMPEG |
| una entrada que es un directorio (`ffprobe -show_format docs`) | pasa | R_FFMPEG |

El de marzo se añadió a la matriz al ver los otros, y es un agujero de `main`: con el
prefijo `file:` delante, `ffprobe` sobre el vídeo de la carpeta de marzo pasaba, porque
`file:corpus/…` no es un fichero que exista y `motivo_fichero` nunca lo veía. Se cierra aquí. El
encargo dice «ninguno fuera de las cuatro formas»; lo leo como «ninguno se ABRE fuera de las cuatro
formas», y declaro estos nueve cierres: `ffmpeg -version` pasa a negarse porque no está en la lista
(nada del repo lo usa: `inventario.py` llama a `ffprobe -version` desde Python, no por Bash).

**El alcance de «ninguno se abre»** (revisor, b5): lo demuestra el test sobre los 75 casos de la
matriz, no sobre todo comando posible. El revisor encontró tres formas fuera de la matriz que se
ABRÍAN en `4dbb48b` (b1, b2, b4); están corregidas y en la matriz, y la comparación con `main` las
da como «main R_EJECUCION | rama R_EJECUCION» (sin cambio). Una cuarta, el alias de la raíz (b3),
es de `main` y se cierra solo para ffmpeg (§1.4); queda para el consultor (§9).

**De NIEGA a NIEGA con otra regla**: el resto de los negados pasan de `R_EJECUCION` a `R_FFMPEG`
(la misma decisión, el mensaje de la lista cerrada); los de material protegido siguen con su motivo
(`R_SIN_ABRIR`, `R_CAPTURA`) y `FFREPORT` con `R_EJECUCION`. Tabla completa en §A.3.

## §3 · La skill `ingerir-sesion`, paso 2

Las cuatro formas exactas -silencios, volumen, metadatos y el audio fuera del repo- copiadas de la
lista, y lo que admite cada una entero. Esas cuatro líneas están, tal cual, en la matriz del test
(«skill: …») y pasan.

## §4 · Qué no cambia

El motor, la spec, las ambigüedades, el feedback, los casos, el corpus, el Makefile y cualquier otra
regla de la guardia: el diff de `guardia.py` es la cabecera, `SIN_LECTURA_DE_RUTAS`, las tres líneas
de entrada en `analizar_comando` y el bloque nuevo (`git diff --stat main...HEAD`: `guardia.py`,
`ingerir-sesion/SKILL.md`, el test nuevo, el informe y su anexo, el encargo, `contrato.yaml`,
`PROJECT_STATE.md` y `HISTORIA.md`; `scripts/contrato_rama.py` en verde). PowerShell: sin cambio (la regla solo entra con
`not ctx.powershell`, y `analizar_powershell` no se toca).

## §5 · Comandos negados durante la rama

Dos negativas de la guardia de `main`, las dos resueltas con la forma que la propia guardia propone
en su mensaje (`DECISIONES-DE-PROCESO.md`, entrada del 2026-10-21):
- `uv run botsito state check …; uv run python scripts/contrato_rama.py …` en una llamada: «antes,
  en el mismo comando, va `uv run botsito state check`» → en dos llamadas.
- `python - <<'EOF' … EOF` seguido de `python fase0.py`: → el guion con Write y su ejecución en
  otra llamada.
Y tres más del mismo tipo -un comando que no está en la lista cerrada delante de una ejecución:
`git diff --stat && uv run pytest …`, `uv run pytest … | grep -c …; uv run pytest …` y
`sed -i … PROJECT_STATE.md && git add … && uv run botsito state check`- → cada una en llamadas
separadas. Ninguna se rodeó.

## §6 · Exposiciones

Ninguna. La rama no leyó material del punto 3 de `CLAUDE.md`, ni transcripciones, ni fotogramas; los
vídeos de los tests son ficheros de 16 bytes inventados en `tmp`.

## §7 · Sello y CI

- `4dbb48b` (la regla, el test, la skill, el informe y el anexo): `make check` exit 0, 2738 passed,
  `SELLO … 813ebc7a…`, pico 297 MiB. Un primer `make check` salió en rojo por mypy (dos listas sin
  anotar en el test nuevo, `abiertos` y `cerrados`); corregido y relanzado. `PROJECT_STATE.md`:
  1647 → 1651 funciones de test (1652 con la de los alias, en el commit de los arreglos).
- CI de Linux: push a `fix/guardia-ffmpeg` (`git push origin
  trabajo/guardia-ffmpeg:refs/heads/fix/guardia-ffmpeg`), run 39822012476 sobre `4dbb48b`:
  `1 failed, 2727 passed, 10 skipped`, y el único fallo es el esperado,
  `tests/unit/test_cli.py::test_state_check_ok_on_real_repo` (la rama se llama `fix/`, `RITUAL.md`).
  Ninguno de los 10 saltados es de `test_guardia_ffmpeg.py`: las cuatro pruebas corrieron en Linux,
  también la comparación con la guardia de `main` (el checkout lleva `fetch-depth: 0`).
- El commit de los arreglos del revisor (§10), el último de la rama: `test_guardia_ffmpeg.py` (5
  pruebas; la de los alias, solo en Windows) y `test_guardia_claude.py` enteros en verde antes del
  sello; su `make check` y su run de la CI de Linux por `fix/guardia-ffmpeg` no caben en el commit
  que sellan: van en el mensaje de entrega a Aleks, y el run que cuenta es ese.
- No se pasó el revisor una segunda vez sobre los arreglos; si el consultor lo quiere, va antes del
  cierre.

## §8 · El encargo, punto por punto

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 1 | `git fetch --prune`, las tres cosas de la base, ninguna otra rama ni local ni en origin | Hecho | «Base comprobada al abrir» |
| 2 | Abrir con `abrir-rama`: encargo, `contrato.yaml`, Archivo en HISTORIA | Hecho | `0252d4f` (Archivo 43) |
| 3 | Encargo copiado tal cual, con la fecha | Hecho | `docs/encargos/trabajo-guardia-ffmpeg.md` |
| 4 | Objetivo: exactamente cuatro formas, todo lo demás negado, test que rompe los dos sentidos | Hecho | §1, §2 |
| 5 | Condición 1, ffprobe | Hecho | `FFPROBE_CON_VALOR`, `FFPROBE_SIN_VALOR` |
| 6 | Condición 2, medida | Hecho (+`nul` en minúsculas, declarado) | `FFMPEG_MEDIDA_CON_VALOR`, `SALIDAS_NULAS`; §1.6 |
| 7 | Condición 3, extracción fuera del repo, sin reutilizar `EXTENSIONES_AUDIO` | Hecho | `EXTENSIONES_DE_EXTRACCION`, `_ffmpeg_dentro_del_repo` |
| 8 | Condición 4, cada entrada resoluble, sin protocolo, por `motivo_fichero` | Hecho (+ resuelta, `\\`, binaria: de más, declarado) | §1.4 |
| 9 | Condición 5, el resto de la línea; redirección dentro del repo negada | Hecho (tras el revisor; + toda redirección de entrada, declarado) | §1.5 |
| 10 | Condición 6, función y constante propias, justo antes de `_ejecucion_de_un_programa_desconocido` | Hecho | `analizar_comando`, `_analizar_ffmpeg`, `R_FFMPEG` |
| 11 | Condición 6, la excepción en el informe y en la cabecera | Hecho | §1.6; cabecera de `guardia.py`, familia 3 |
| 12 | Condición 6, ffprobe sale de `SIN_LECTURA_DE_RUTAS` | Hecho | `guardia.py` |
| 13 | Condición 6, PowerShell sin cambio | Hecho | `not ctx.powershell`; el revisor lo midió (b, fila 13) |
| 14 | Condición 7, el límite de «fuera del repo» dicho | Hecho | §1.7 |
| 15 | PARADA si algo no se puede comprobar con lo que la guardia sabe | No hizo falta | §1, final |
| 16 | Fase 0: la medida reproducida con el arnés | Hecho | §0.1; `fase0-main.txt` |
| 17 | Fase 0: los cinco tests en verde | Hecho | §0.2; `test_guardia_claude.py` entero en verde (§7) |
| 18 | Fase 1: matriz con las cuatro formas (relativas y absolutas) y los negados pedidos | Hecho | §2; los 20 negados pedidos están, y 39 más |
| 19 | Roto a propósito en los dos sentidos, salidas al informe | Hecho | §2; `salidas-pytest.txt` |
| 20 | La matriz frente a la guardia de `main`, test nuevo con `decidir`, tabla y «ninguno fuera de las cuatro» | Hecho, con la lectura declarada | §2 («El alcance de “ninguno se abre”») |
| 21 | La skill `ingerir-sesion`, paso 2 | Hecho | §3 |
| 22 | Negativas: PARADA salvo la forma que propone la guardia, declarada | Hecho | §5 |
| 23 | No probar la regla ejecutando ffmpeg | Hecho | ningún ffmpeg ejecutado; todo por `decidir` |
| 24 | CI sin guion ni bucle: un `gh run view` suelto | Hecho | §7 (la espera, un `sleep` de fondo sin consulta) |
| 25 | Qué NO cambia | Hecho | §4 |
| 26 | Informe; `make check` sellado; push a `fix/`; CI con solo el fallo esperado; números de run | Hecho | §7 |
| 27 | Revisor con el informe terminado, su informe pegado | Hecho | §10 |
| 28 | «Rama lista para revisión, NO cerrada» | Hecho | Estado |

Desviaciones, todas por exceso y declaradas: la entrada se mira también resuelta, se niegan las
rutas `\\`/`//`, las entradas de texto y toda redirección de entrada; `nul` en minúsculas; nueve
casos que `main` dejaba pasar se niegan (§2).

## §9 · Para el consultor, y la Next Action del cierre

**Preguntas** (ninguna bloquea la ingesta de mañana):
1. La lectura de «ninguno fuera de las cuatro formas» como «ninguno se ABRE», con los nueve cierres
   de §2 (revisor, b5).
2. El alias de la raíz en `motivo_fichero` es de `main` (revisor, a3): `cat`, `Read`, `grep -r` o
   `find … -exec cat` sobre la raíz escrita con `\\?\` o en 8.3, o sobre un directorio que CONTIENE
   el repo, pasan hoy. Aquí se cierra solo para ffmpeg (§1.4); para el resto, una línea de Technical
   Debt o una rama de G.1.
3. Las desviaciones por exceso de §8 (sobre todo la entrada binaria): si alguna sobra.

**Next Action, preparada para el commit del contrato del cierre** (`RITUAL.md`, puntos 3 y 4; en la
rama no se toca). La K pierde su segunda frase; queda:

> K. La guardia exigir_sin_crudo da un falso positivo con una asignación a una variable llamada
> crudo (scripts/leer_demo_ftmo.py; DEMO-EJECUCION-1.md). Rama propia, junto a B o C si cabe: que
> la guardia nombre la forma de la opción, con un test que rompa a propósito los dos sentidos. Y en
> la misma rama, el arreglo que queda de ENTRADA-JULIO.md §8: que reconozca como tests los de un
> clon `git worktree add --detach` de comparar-con-main (`C:/cm/`), con su test de los dos
> sentidos. (ffprobe y ffmpeg: hecho en trabajo/guardia-ffmpeg, GUARDIA-FFMPEG.md.)

Y, si el consultor lo acepta, una línea nueva de Technical Debt con la pregunta 2. G.1 de
`docs/plan/HOJA-DE-RUTA.md` no pasa a HECHA (lo dice el encargo).

## §10 · El revisor

### Lo que se hizo con los hallazgos del revisor

| # | Gravedad | Qué se hizo |
|---|---|---|
| b1 | bloquea | Arreglado: `_analizar_ffmpeg` llama a `_exigir_lo_de_antes` y `_exigir_lo_de_a_la_vez`. `find "<repo>/.." -name "*.mp4" -exec ffprobe -show_format {} \;` niega con `R_EJECUCION`, como en `main`; caso «find -exec ffprobe {}» de la matriz. |
| b2 | bloquea | Arreglado por lo mismo: `cd -` no es preparación. Casos «cd - delante», «cd dinamico delante», «cd o true delante» y «cp delante», todos `R_EJECUCION`. |
| b3 | importa | Arreglado para ffmpeg: se niegan las rutas `\\`/`//`, y la entrada y «fuera del repo» se miran también resueltas (`realpath`). Test solo de Windows con `\\?\` y con el 8.3 real. Lo de `main` (a3) queda como pregunta 2 de §9. |
| b4 | importa | Arreglado: `| tee` y `&`, por `_exigir_lo_de_a_la_vez`; `1<>fichero`, al negar toda redirección de entrada. Casos en la matriz. §1.5 reescrito. |
| b5 | importa | Contestado: la afirmación se acota a la matriz y se dice qué se abrió fuera de ella y cómo se cerró (§2, «El alcance…»); pregunta 1 de §9. |
| b6 | importa | Hecho: §8. |
| b7 | menor | Declarado en §1.6. |
| a1 | importa | Arreglado (b1, b2, b4) y §1.5, §1.6 y la cabecera dicen ahora qué se deja de la familia 3 (leer un guion) y qué se conserva (lo de antes y a la vez). |
| a2 | importa | Hecho: `## Estado` y la Next Action preparada (§9). |
| a3 | importa (de `main`) | Pregunta 2 de §9. |
| a4 | menor | Hecho: `cd` dinámico, una sustitución en el mismo comando y un directorio, en la matriz. |
| a5 | menor | Aceptado: como `test_la_guardia_frente_a_la_de_main_caso_a_caso`, tras el merge compara la guardia consigo misma; lo dice su docstring. |
| — | «lo que no pude comprobar» | La entrada que es una lista (`ffconcat`, `m3u8`): arreglado, una entrada de texto se niega (§1.4), caso «entrada de texto (ffconcat)» con extensión `.mp4`. Qué hace ffmpeg de verdad con `\\?\` y 8.3: no se mide (no se ejecuta ffmpeg); la regla ya no lo deja llegar. |

Tras los arreglos: `test_guardia_ffmpeg.py` y `test_guardia_claude.py` enteros en verde, `make check`
sellado y la CI de Linux del último commit (§7).

### Informe del revisor (pegado tal cual)

## Informe del revisor · trabajo/guardia-ffmpeg · 2026-10-22

Base: `git merge-base main HEAD` = 8cfed041. Commits: 0252d4f (apertura) y 4dbb48b (la regla). Sin commitear: solo el §7 de `docs/validation/GUARDIA-FFMPEG.md`, que es el resultado de la CI.

En corto: la rama aún NO está lista. Hay dos bloqueos y los dos tienen la misma raíz. `_analizar_ffmpeg` sale de `exigir_ejecucion_verificable` y con eso pierde también `_exigir_lo_de_antes` y `_exigir_lo_de_a_la_vez`, las comprobaciones de «lo que va antes o a la vez en el mismo comando». En `main` esas dos negaban formas de ffmpeg/ffprobe que ahora pasan. Todas las decisiones de abajo las medí con `decidir` de la rama y con el de `main` (cargado desde `git show main:`), sobre el texto del comando. No ejecuté ffmpeg ni find.

### Eje (a) · Reglas de la casa
Resumen: 0 bloquea, 3 importa, 2 menor.

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| a1 | importa | El informe dice algo que la medida contradice. En §1.5 afirma que «las tuberías, las redirecciones de entrada y los nombres de entorno se analizan como antes». No es así: en `main`, detrás de una ejecución en la tubería solo podían ir filtros, delante solo «preparación» y no se admitía `&`. En la rama ffprobe/ffmpeg ya no tienen ninguna de las tres restricciones. La excepción de la cabecera (`guardia.py:41-45`) tampoco lo dice, y la familia 3 que exceptúa (`guardia.py:38-40`) nombra justo esas restricciones. | Medido, rama frente a main. `ffprobe -show_format README.md \| tee meta.json`: rama PASA; main NIEGA («detras, en la misma tuberia, va `tee meta.json`…»). `ffprobe -show_format /c/zz/v.mp4 & cat /c/zz/x.txt`: rama PASA; main NIEGA («lanza algo en segundo plano»). `cp /c/zz/a.mp4 /c/zz/b.mp4 && ffprobe …`: rama PASA; main NIEGA («antes, en el mismo comando, va `cp …`»). `ln -s /c/zz/dir /c/zz/m && ffprobe -show_format /c/zz/m/v.mp4`: lo mismo. |
| a2 | importa | El informe está incompleto según la skill `entregar-rama`, paso 4. `## Estado` sigue en «EN CURSO» aunque el informe se da por terminado. Tampoco están preparadas las líneas de la Next Action que cambian en el cierre: la K de PROJECT_STATE todavía lleva «que `ffprobe` y `ffmpeg -i` sobre un vídeo lean y no ejecuten». | `GUARDIA-FFMPEG.md:222-224`. `PROJECT_STATE.md:48`. `.claude/skills/entregar-rama/SKILL.md:55-59`. |
| a3 | importa (es de main, no lo introduce la rama) | `motivo_fichero` decide por el texto de la ruta. Lo que no reconoce como «dentro del repo» devuelve None, y ninguna regla de material se aplica. Dos casos medidos: (1) la ruta del repo escrita con prefijo `\\?\` o con su nombre corto 8.3 `C:\Users\USER\Desktop\BOTV3~1`; (2) leer de forma recursiva un directorio que CONTIENE el repo. En `main`, `cat` y `Read` ya pasan así. La rama añade ffprobe/ffmpeg a la lista de lectores que pasan (ver b3). Para el consultor o la Technical Debt. | `relativa('\\?\C:\Users\USER\Desktop\Bot v3\README.md')` = None. main: `cat C:/Users/USER/Desktop/BOTV3~1/README.md` PASA; `Read` con `\\?\…README.md` PASA; `find /c/Users/USER/Desktop -name *.jpeg -exec cat {} ;` PASA; `grep -r x /c/Users/USER/Desktop` PASA. El código: `guardia.py:441-442` (`rel is None → return None`) y `503-505`. |
| a4 | menor | Hay piezas declaradas de la regla sin ningún caso en la matriz: el `cd` dinámico anterior, una sustitución en el mismo comando y una entrada que es un directorio. Si se borran, ningún test cae. | `grep 'cd "\$'` en `tests/unit/test_guardia_ffmpeg.py` no encuentra nada. Las tres funcionan: `cd "$HOME_X" && ffprobe …` NIEGA («antes va un cambio de directorio que se construye al ejecutarse»); `ffprobe -show_format docs` NIEGA («es un directorio»). |
| a5 | menor | Tras el merge, `test_la_matriz_frente_a_la_guardia_de_main` compara la guardia consigo misma y no prueba nada. Su propio docstring lo reconoce. | `test_guardia_ffmpeg.py:287-289`. |

Comprobado sin hallazgos:
- **Contrato:** `uv run python scripts/contrato_rama.py` da «CONTRATO: 11 ficheros dentro del contrato … 3 comprobaciones para el revisor».
- **Comprobación de pytest del contrato:** `uv run pytest -q -rfE tests/unit/test_guardia_claude.py tests/unit/test_guardia_ffmpeg.py`, todo en puntos, ninguna F ni E.
- **make check:** en `make-check.log` están «2738 passed», «SELLO: … 813ebc7a7bca…» y «PICO DE MEMORIA … 297 MiB». `git rev-parse 4dbb48b^{tree}` = 813ebc7a…, el mismo árbol del sello. El sello de 0252d4f (fb436c89) también coincide.
- **CI:** `gh run view 39822012476` da headSha 4dbb48b9 en fix/guardia-ffmpeg, con «1 failed, 2727 passed, 10 skipped». El único FAILED es `test_cli.py::test_state_check_ok_on_real_repo`, y ninguno de los SKIPPED es de `test_guardia_ffmpeg.py`.
- **Trailers `Fuente:`, ADR, ambigüedades, guardias de `cita`, evidencia nueva:** no aplican. No hay ningún commit en `knowledge/`, `docs/adr/` ni `data/manifests/`.
- **Regímenes de cambio:** el diff `--name-status` no toca ningún directorio inmutable. HISTORIA crece +167/-0, y el Archivo 43 es el PROJECT_STATE de main (164 líneas más la cabecera).
- **Informes cerrados:** ninguno modificado.
- **PROJECT_STATE:** 22.628 bytes.
- **Material protegido:** la rama no lo toca. «Exposiciones: ninguna» es coherente con eso: los vídeos de los tests son ficheros «x\n» en `tmp`.
- **Tres citas del informe comprobadas:** el sello y el árbol; «63 = 16 + 47»; los 8 casos PASA→NIEGA (anexo, líneas 120-125, 134 y 139). Y además: `inventario.py` llama a `ffprobe -version` desde Python (`inventario.py:139-149`).

### Eje (b) · Encargo
Resumen: 2 bloquea, 4 importa, 1 menor. Requisitos: 19 hechos, 6 parciales, 1 no hecho.

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 1 | Base: fetch, las tres cosas, ninguna otra rama | Hecho | Informe:10-20; merge-base 8cfed04 |
| 2 | Abrir con abrir-rama: encargo, contrato y Archivo | Hecho | 0252d4f; HISTORIA +167/-0 |
| 3 | Encargo copiado tal cual y con fecha | Hecho (la literalidad no se puede comprobar) | encargo:3 |
| 4 | Objetivo: exactamente cuatro formas y todo lo demás negado | Parcial | b1, b2, b4 |
| 5 | Condición 1: lista cerrada de ffprobe | Hecho | `FFPROBE_CON_VALOR/SIN_VALOR` |
| 6 | Condición 2: medida | Hecho (la lista acepta además `nul`, ver b7) | `FFMPEG_MEDIDA_CON_VALOR`, `SALIDAS_NULAS` |
| 7 | Condición 3: extracción con salida FUERA del repo | Parcial | b3 |
| 8 | Condición 4: cada entrada resoluble, sin protocolo, que pase `motivo_fichero` | Parcial | b1 (`{}`), b2 (`cd -`), b3 |
| 9 | Condición 5: el resto de la línea no cambia; se niega una redirección a un fichero dentro del repo | Parcial | b4 |
| 10 | Condición 6: función y constante propias, justo antes de `_ejecucion_de_un_programa_desconocido`; el test de la «sola función» en verde | Hecho | `guardia.py:1410-1414`; test en verde |
| 11 | Condición 6: declarado en el informe y en la cabecera como excepción a la familia 3 | Hecho (incompleto, ver a1) | informe §1.6; `guardia.py:41-45` |
| 12 | Condición 6: ffprobe sale de `SIN_LECTURA_DE_RUTAS` | Hecho | `guardia.py:906` |
| 13 | Condición 6: PowerShell sin cambio | Hecho | Medido: con `tool_name` PowerShell, ffprobe, ffmpeg, `cmd /c` y `bash -c` niegan con el mismo mensaje en la rama y en main |
| 14 | Condición 7: el límite de «fuera del repo» dicho en el informe | Hecho | §1.7 |
| 15 | Fase 0: reproducir la medida | Hecho | §0.1; `fase0-main.txt` |
| 16 | Fase 0: los cinco tests en verde | Hecho | Medido: `-k` con los cinco, todos PASSED |
| 17 | Matriz con los negados mínimos y rutas relativas y absolutas | Hecho | Los 20 negados pedidos están en `NEGADAS` (`test_guardia_ffmpeg.py:141-208`) |
| 18 | Roto a propósito en los dos sentidos, con las salidas al informe | Hecho | anexo, líneas 64-81 |
| 19 | Matriz frente a main: tabla y «ninguno fuera de las cuatro formas» | Parcial | Tabla hecha; el «ninguno» solo vale dentro de la matriz (b5) |
| 20 | Skill ingerir-sesion, paso 2 | Hecho | Diff del SKILL; los 4 casos «skill:» pasan |
| 21 | Qué NO cambia | Hecho | `git diff --name-status`; contrato |
| 22 | Negativas declaradas con la forma propuesta | Hecho | §5 |
| 23 | make check sellado | Hecho | SELLO = árbol de 4dbb48b |
| 24 | Push a fix/ y CI con solo el fallo esperado; números de run | Hecho | run 39822012476 |
| 25 | Revisor con el informe terminado y su informe pegado al final | Parcial | En curso (esta revisión); el Estado sigue EN CURSO |
| 26 | «Rama lista para revisión, NO cerrada» | No hecho | `GUARDIA-FFMPEG.md:224` |

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| b1 | bloquea | `find <directorio que contiene el repo> -exec ffprobe\|ffmpeg … {} ;` PASA en la rama y NIEGA en main. La guardia toma `{}` como la ruta literal `<cwd>/{}`, que no existe, y no la niega. Pero ffmpeg recibiría cada fichero que encuentre find, incluido lo de `corpus/…/Material adicional…`. Es una forma fuera de las cuatro que pasa de NIEGA a PASA, y su entrada no es «resoluble sin sustitución». | `find /c/Users/USER/Desktop -name *.mp4 -exec ffprobe -show_format {} ;`: rama PASA; main NIEGA («antes, en el mismo comando, va `find …`»). Lo mismo con `find .. …`, con `-execdir … +` y con `-exec ffmpeg -i {} -vn -sn -dn -ac 1 -ar 16000 /c/zz/a.wav ;`. Con `find . …` la rama sí niega («lee el contenido de lo que encuentra»), porque `.` cae dentro del repo. |
| b2 | bloquea | `cd X && cd - && ffprobe v.mp4` PASA en la rama y NIEGA en main. La guardia resuelve `cd -` como el directorio `<cwd>/-` (`guardia.py:1321-1327`), y la comprobación de `cd` de la rama (`guardia.py:3092-3098`) solo mira si el valor es literal. Si X es la carpeta de marzo, `motivo_fichero` mira `<otro>/-/v.mp4` mientras ffprobe abre `X/v.mp4`. Lo medí con X=/c/zz; con marzo no lo ejecuté porque mi guardia niega el literal, pero la decisión no depende de X. Mismo patrón: `cd /c/zz \| true;` y `cd /c/zz \|\| true;`, que PASAN en la rama y NIEGAN en main. | `cd /c/zz && cd - && ffprobe -show_format v.mp4`: rama PASA; main NIEGA («antes, en el mismo comando, va `cd -`»). Con ffmpeg y volumedetect, igual. |
| b3 | importa | Condición 3: la comprobación «salida fuera del repo» se salta con un alias de la raíz. Y una entrada del repo escrita con alias deja de verse en `motivo_fichero`: main la negaba (R_EJECUCION) y la rama la deja pasar. La causa es a3 (anterior a la rama). Es la puerta que el propio encargo elige, así que es pregunta para el consultor. Si ffmpeg en Windows abre esas formas no lo medí. | `ffmpeg -i ../fuera/v.mp4 -vn -sn -dn '\\?\C:\Users\USER\Desktop\Bot v3\data\a.wav'`: rama PASA. `… 'C:/Users/USER/Desktop/BOTV3~1/data/a.wav'`: rama PASA. `ffprobe -show_format C:/Users/USER/Desktop/BOTV3~1/README.md`: rama PASA; main NIEGA (R_EJECUCION). |
| b4 | importa | La condición 5 dice «el resto del análisis de la línea no cambia» y pide negar la salida a un fichero dentro del repo. Pero `\| tee <repo>`, `&`, lo que va antes en el mismo comando y `1<>fichero` pasan, y el informe no lo declara (ver a1). La condición 6, que pide salir de `exigir_ejecucion_verificable`, choca con esta: hay que declararlo o preguntarlo. Una posible salida que NO medí: llamar a `_exigir_lo_de_antes` y `_exigir_lo_de_a_la_vez` desde `_analizar_ffmpeg`. Eso devolvería el comportamiento de main en b1, b2 y b4, y las formas de la skill (`cd` y `\| grep`) seguirían dentro de esas listas. | `ffprobe -show_format README.md \| tee meta.json`: rama PASA; main NIEGA. `ffprobe -show_format README.md 1<>meta.json`: rama PASA. |
| b5 | importa | Pregunta 2. Los 8 casos que pasan de PASA a NIEGA tienen defensa: el propio encargo exige negar los protocolos y «todo lo demás», y el informe los declara en §2. El agujero de `file:` sobre marzo que se cierra está bien visto. Pero la frase «ninguno fuera de las cuatro formas» se demuestra solo sobre la matriz de 63 casos. b1, b2 y b4 son formas fuera de las cuatro que pasan de NIEGA a PASA. Esto va como pregunta al consultor, o se acota la afirmación. | Informe §2:155-161; mis medidas de b1, b2 y b4 |
| b6 | importa | Falta «El encargo, punto por punto», la tabla de la skill `entregar-rama`. | `grep "punto por punto"` en el informe no encuentra nada; `entregar-rama/SKILL.md:46-50` |
| b7 | menor | `DISPOSITIVOS_NULOS` acepta también `nul` en minúsculas, que el encargo no pide («NUL o /dev/null») y el informe no declara (§1.2). | `guardia.py`, en el diff: `DISPOSITIVOS_NULOS = frozenset({"NUL", "nul", "/dev/null"})` |

Pregunta 3: el test de la «sola función» y los otros cuatro siguen en verde (lo medí). La excepción está declarada donde pide el encargo, en el informe §1.6 y en la cabecera (`guardia.py:41-45`), pero le falta decir lo que se pierde con ella (a1).

Pregunta 1, lo que la lista sí cierra: las opciones fuera de la lista, las que consumen un valor, el orden respecto a `-i`, las repetidas, lo que va detrás de la salida, los protocolos `concat:`, `file:`, `subfile,` y `C:x`, `%`, `xargs` (niega en la rama y en main), las sustituciones y FFREPORT. Lo que no cierra está en b1-b4.

### Lo que no pude comprobar
- **Qué hace ffmpeg de verdad (no se ejecuta):** si abre `\\?\…` y los nombres 8.3; y si una entrada que es una LISTA reenvía a otro fichero: un `ffconcat` detectado por su contenido, o un `.m3u8`. La guardia deja pasar cualquier fichero existente y no protegido sin mirar su contenido: los vídeos del test son texto «x\n» (`test_guardia_ffmpeg.py:59-62`) y pasan. El informe no declara ese límite, que sería el equivalente para la entrada del de la condición 7 para la salida.
- **Medidas sobre rutas protegidas literales:** las hice con análogos (/c/zz, README.md), porque mi propia guardia niega el literal. En b1 y b2 la decisión no depende del destino.
- **Contenido real de la carpeta de marzo:** no sé si hay vídeos; no la listo.
- **Literalidad del encargo:** no puedo compararlo con el prompt original.
- **Ejecuciones que escriben:** no ejecuté `make check`; la evidencia es `make-check.log`. Tampoco la CI del commit final con el §7 y este informe, que aún no existe.

### Comandos ejecutados
1. `git branch --show-current && git merge-base main HEAD && git log --format='%h %s' main..HEAD && git diff --stat main...HEAD && git status --short`
2. `git diff -- docs/validation/GUARDIA-FFMPEG.md`; `git diff main...HEAD -- .claude/hooks/guardia.py`
3. Varios `grep -n` y `sed -n` sobre `guardia.py` (envoltorios, xargs, find, cd, `NO_EJECUTAN`, `LECTOR_DE_METADATOS`, `exigir_*`)
4. Seis llamadas `uv run python -c "…"` que cargan la guardia de la rama y la de main (`git show main:…` + `exec`) y llaman a `decidir` sobre los comandos citados arriba, sin escribir ficheros; más una con `GetShortPathNameW` para obtener el nombre 8.3.
5. `uv run pytest -q tests/unit/test_guardia_ffmpeg.py`
6. `uv run pytest -q tests/unit/test_guardia_claude.py -k "<los cinco de la fase 0>" -rA`, más dos repeticiones filtradas
7. `uv run python scripts/contrato_rama.py`
8. Un intento con dos pytest en la misma llamada: la guardia lo NEGÓ («antes, en el mismo comando, va `uv run pytest …`»). Seguí la forma que propone y lo lancé en una sola llamada: `uv run pytest -q -rfE tests/unit/test_guardia_claude.py tests/unit/test_guardia_ffmpeg.py`
9. `ls -la make-check.log && grep -nE "SELLO|PICO DE MEMORIA|passed|failed" make-check.log`; `git rev-parse 4dbb48b^{tree} 0252d4f^{tree}`
10. `git diff --name-status main...HEAD`; `git log … -- knowledge docs/adr data/manifests`; `git diff main...HEAD -- PROJECT_STATE.md`; `git diff --numstat … HISTORIA.md`; `git show main:PROJECT_STATE.md | wc -l`
11. `git diff main...HEAD -- .claude/skills/ingerir-sesion/SKILL.md`; `wc -c PROJECT_STATE.md`; varios `grep` sobre el informe, la skill, `src/` y `inventario.py`
12. `gh run view 39822012476`; `gh run view 39822012476 --log-failed | grep …`; `gh run view 39822012476 --json headSha,headBranch`
13. Ficheros leídos con Read: el encargo, `contrato.yaml`, `GUARDIA-FFMPEG.md`, `test_guardia_ffmpeg.py`, los tres anexos y tramos de `guardia.py` y de `entregar-rama/SKILL.md`.

Ficheros de referencia: `C:\Users\USER\Desktop\Bot v3\.claude\hooks\guardia.py`, `C:\Users\USER\Desktop\Bot v3\tests\unit\test_guardia_ffmpeg.py`, `C:\Users\USER\Desktop\Bot v3\docs\validation\GUARDIA-FFMPEG.md`, `C:\Users\USER\Desktop\Bot v3\docs\encargos\trabajo-guardia-ffmpeg.md`.

## §A · Anexo (`docs/validation/anexos/GUARDIA-FFMPEG/`)

- `fase0-main.txt`: la tabla de §0.1, con la guardia de `main` (`git show main:`), regenerada con
  los vídeos binarios (las decisiones, las mismas que con los de texto).
- `fase0-rama.txt`: los mismos diez casos con la guardia de la rama: pasan los de las formas
  permitidas salvo la extracción DENTRO del repo (`R_FFMPEG`, «la salida `audio.wav` esta dentro
  del repositorio»); marzo sigue negado con `R_SIN_ABRIR`; el que no existe sigue pasando.
- `salidas-pytest.txt`: `uv run pytest -q -s tests/unit/test_guardia_ffmpeg.py`, exit 0, sobre el
  último commit. Contiene:
  - §A.1, la matriz entera (`| caso | comando | obtenido | esperado |`);
  - §A.2, las dos roturas a propósito (`sin la regla | …` y `con una opcion de mas | …`);
  - §A.3, la comparación con `main` caso a caso (`| caso | main X | rama Y |`).

## Estado

TERMINADA, pendiente de la revisión del consultor: las cuatro formas de ffprobe y ffmpeg pasan,
todo lo demás se niega, y los dos bloqueos y los cinco «importa» del revisor están arreglados o
contestados (§10); tres preguntas para el consultor en §9, ninguna bloquea la ingesta.

Rama lista para revisión, NO cerrada.
