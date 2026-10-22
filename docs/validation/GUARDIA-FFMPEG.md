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
   patrón de secuencia son muchos ficheros), que no sea un directorio, y que pase
   `motivo_fichero`: sobre material protegido niega con su motivo, con el mensaje de `main`
   («ejecutar <ruta>. Regla: …»). La salida de la extracción pasa por las mismas comprobaciones de
   protocolo y `%`.
5. **El resto de la línea**: las tuberías, las redirecciones de entrada y los nombres de entorno se
   analizan como antes (cada comando de la tubería por su cuenta; `FFREPORT` sigue negado por
   `NOMBRES_DE_ENTORNO`, con `R_EJECUCION`). En estas formas, además, se niega: ir dentro de un
   `$(...)`; una sustitución en el comando (`$(...)`, acentos graves, `<(...)`); un `cd`/`pushd`/
   `popd` anterior a un sitio que no se sabe (las rutas relativas caerían donde no se ve); y una
   redirección de la salida estándar o de errores a un fichero DENTRO del repo (o a uno que se
   construye al ejecutarse). `2>&1` y los dispositivos nulos pasan.
6. **Excepción a la familia 3, declarada**: estas cuatro formas YA NO pasan por
   `exigir_ejecucion_verificable`. Lo que ejecutan es ffmpeg, no un fichero de la rama, y sus
   ficheros son datos de audio y vídeo; lo que se comprueba es la lista cerrada. Escrito en la
   cabecera de `guardia.py`, en la familia 3. `ffprobe` sale de `SIN_LECTURA_DE_RUTAS` (cambio
   declarado; ya no se llegaba a consultar). Lo que no encaja en ninguna forma se niega con
   `R_FFMPEG` -no vuelve a la regla del programa desconocido-: «todo lo demás negado».
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
de `tmp_path` con los vídeos SIN SEGUIR, y las rutas del material a trozos por la misma razón.

- `test_la_matriz_de_ffmpeg`: 63 comandos (16 que pasan y 47 negados) con su decisión esperada -las cuatro formas, con rutas
  relativas y absolutas, a `-`, `NUL` y `/dev/null`, con `2>&1 | grep`, con `2>` fuera del repo y
  tras `cd`, y las cuatro formas exactas de la skill; y todos los negados que pide el encargo y
  algunos más (tabla en el anexo, §A)-.
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

**De PASA a NIEGA (endurecimiento, declarado)**: ocho casos que `main` dejaba pasar porque el
argumento no es un fichero que exista y la regla del programa desconocido solo mira ficheros:

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

El de marzo se añadió a la matriz al ver los otros, y es un agujero de `main`: con el
prefijo `file:` delante, `ffprobe` sobre el vídeo de la carpeta de marzo pasaba, porque
`file:corpus/…` no es un fichero que exista y `motivo_fichero` nunca lo veía. Se cierra aquí. El
encargo dice «ninguno fuera de las cuatro formas»; lo leo como «ninguno se ABRE fuera de las cuatro
formas», que es lo que se cumple, y declaro estos ocho cierres: `ffmpeg -version` pasa a negarse
porque no está en la lista (nada del repo lo usa: `inventario.py` llama a `ffprobe -version` desde
Python, no por Bash).

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
de entrada en `analizar_comando` y el bloque nuevo. PowerShell: sin cambio (la regla solo entra con
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
vídeos de los tests son ficheros de una línea inventados en `tmp`.

## §A · Anexo (`docs/validation/anexos/GUARDIA-FFMPEG/`)

- `fase0-main.txt`: la tabla de §0.1, con la guardia de `main` (`git show main:`).
- `fase0-rama.txt`: los mismos diez casos con la guardia de la rama: pasan los siete de las formas
  permitidas salvo la extracción DENTRO del repo (`R_FFMPEG`, «la salida `audio.wav` esta dentro
  del repositorio»); marzo sigue negado con `R_SIN_ABRIR`; el que no existe sigue pasando.
- `salidas-pytest.txt`: `uv run pytest -q -s tests/unit/test_guardia_ffmpeg.py`, exit 0. Contiene:
  - §A.1, la matriz entera (`| caso | comando | obtenido | esperado |`);
  - §A.2, las dos roturas a propósito (`sin la regla | …` y `con una opcion de mas | …`);
  - §A.3, la comparación con `main` caso a caso (`| caso | main X | rama Y |`).

## Estado

EN CURSO.
