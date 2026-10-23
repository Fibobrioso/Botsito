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
   (`os.path.realpath`: un enlace o un nombre corto 8.3 de Windows) Y SIN LOS PUNTOS NI ESPACIOS
   DEL FINAL de cada nombre, que Windows quita al abrir (`_ffmpeg_formas_de_la_ruta`): sobre
   material protegido niega con su motivo, con el mensaje de `main` («ejecutar <ruta>. Regla: …»).
   Y la entrada tiene que ser **un contenedor de vídeo reconocido** (`_ffmpeg_es_video`, desde la
   respuesta del consultor, §11-§12): extensión `.mp4`, `.mov`, `.mkv` o `.webm`
   (`EXTENSIONES_DE_VIDEO`, comparada en minúsculas) Y sus bytes mágicos -ISO BMFF, `ftyp` en el
   desplazamiento 4 (`MAGIA_ISO_BMFF`); Matroska/WebM, `1A 45 DF A3` al principio
   (`MAGIA_MATROSKA`)-. Todo lo demás se niega, también un fichero que no existe o no se puede leer:
   ffmpeg detecta por el CONTENIDO una lista que nombra otros ficheros (`#EXTM3U`, `ffconcat
   version 1.0`). Detrás, como segunda barrera, la de antes (`_ffmpeg_es_texto`): sin ningún nulo
   en los primeros 4096 bytes, se niega. La salida de la extracción pasa por las mismas
   comprobaciones de protocolo, `%` y `\\`, y «fuera del repo» se mira en las tres formas
   (`_ffmpeg_dentro_del_repo`). (Lo de `\\`, `realpath` y la entrada de texto entró tras el
   revisor: b3 y «lo que no pude comprobar»; los bytes mágicos y los finales, tras el consultor.)
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
8. **La comilla ANSI-C, para toda la guardia** (ampliación del encargo, declarada; respuesta del
   consultor, punto 2): `tokenizar` copiaba el interior de `$'…'` tal cual, sin interpretar sus
   escapes, y con eso `cat $'…/Back\x74est marzo 2026/v.mp4'` pasaba en `main`. Ahora una comilla
   `$'…'` cuyo interior lleva una barra invertida (`_ansi_c_con_escapes`) tiene VALOR DESCONOCIDO:
   se marca como una variable sin valor y `resolver` la niega (`DinamicoError`), igual que
   `$X` sin valor; lo que ya se negaba con un valor desconocido se niega, y lo demás no cambia.
   Sin barra, sigue siendo literal. Además, el final de la comilla se busca saltando los escapes
   (`$'a\'b'` es una sola palabra), dentro y fuera de un `$(...)`. Qué cambia, medido, en §12.
   Y la comilla de traducción `$"…"` (segunda respuesta del consultor, punto 1): se lee como
   `"…"` (`_comilla_de_locale`), porque bash solo la traduce con un catálogo de mensajes, que la
   guardia no deja fijar (matiz en §15); antes el `$`
   se quedaba en la palabra y `cat $"<marzo>/v.mp4"` pasaba. Qué cambia, en §15.

Nada de esto ha necesitado algo que la guardia no supiera ya del comando (sus palabras resueltas,
sus redirecciones, el nivel y la secuencia): sin PARADA.

## §2 · El test: `tests/unit/test_guardia_ffmpeg.py`

Un fichero nuevo (el de `test_guardia_claude.py` no se toca: si cambiara, la guardia lo leería
entero como código de la rama y sus literales del material la harían negarlo). Monta su propio repo
de `tmp_path` con los vídeos SIN SEGUIR y binarios (el principio de un mp4), y las rutas del
material a trozos por la misma razón.

- `test_la_matriz_de_ffmpeg`: 102 comandos (20 que pasan y 82 negados) desde la segunda respuesta
  del consultor (§15; con la primera, 94: 19 y 75; antes, 75: 16 y 59) con su decisión esperada
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
- `test_sin_los_bytes_magicos_la_lista_hls_vuelve_a_pasar` y
  `test_sin_el_arreglo_de_la_comilla_ansi_c_los_cuatro_pasan`: las dos roturas a propósito de la
  respuesta del consultor (§12); `test_sin_el_arreglo_de_la_comilla_de_locale_los_cinco_pasan`, la
  de la segunda (§15).
- `test_la_matriz_frente_a_la_guardia_de_main`: la misma matriz con la guardia de `main` (cargada
  de `git show main:` o `origin/main`, como `test_la_guardia_frente_a_la_de_main_caso_a_caso`),
  con `decidir`. Exige que ningún caso pase a PASAR fuera de las formas permitidas y que ninguna
  permitida se niegue. Ya en `main`, las dos guardias son la misma y no cambia ninguno.

### Casos que cambian de decisión frente a `main`

**De NIEGA a PASA: solo las cuatro formas permitidas**, los 19 casos de `PERMITIDAS` (ffprobe
relativa, absoluta con `-i`, con `-print_format`; silencios relativa y absoluta a `NUL`; volumen a
`/dev/null`, absoluta y con `2>` fuera del repo; extracción absoluta, relativa `../fuera`, `.mp3` y
`.m4a` tras `cd`; las cuatro de la skill; y, desde §12, ffprobe y volumen sobre un `.mkv` y una
comilla `$'…'` sin barra). En `main` todas niegan con `R_EJECUCION`. La vigésima permitida, de §15
(`ffprobe` sobre el vídeo con `$"…"`), no cambia: en `main` también pasaba, porque allí la ruta con
`$` no existe y el programa desconocido solo mira ficheros que existen.

**De PASA a NIEGA (endurecimiento, declarado)**: veinte casos que `main` dejaba pasar. Nueve, de
la primera versión, porque el argumento no es un fichero que exista (o es un directorio) y la
regla del programa desconocido solo mira ficheros; seis, de §12, y cinco, de §15, al final de la
tabla:

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
| una entrada que no existe (`ffprobe -show_format no-existe.mp4`) | pasa | R_FFMPEG |
| **ANSI-C: `ffprobe -show_format $'<raíz>/…/Back\x74est marzo 2026/v.mp4'`** | **pasa** | R_FFMPEG |
| **ANSI-C: `ffmpeg -i $'<raíz>/…/Back\164est marzo 2026/v.mp4' … -`** | **pasa** | R_FFMPEG |
| **ANSI-C: `cat $'<raíz>/…/Back\x74est marzo 2026/v.mp4'`** | **pasa** | niega (argumento dinámico) |
| **ANSI-C: `cd $'<raíz>/…/Back\x74est marzo 2026' && ffprobe -show_format v.mp4`** | **pasa** | R_EJECUCION |
| **`ffprobe -show_format "<raíz>/…/Backtest marzo 2026 /v.mp4"`** (espacio final) | **pasa** | R_SIN_ABRIR |
| **locale: `cat $"<marzo>/v.mp4"`** | **pasa** | R_SIN_ABRIR |
| **locale: `head -c 10 $"<marzo>/v.mp4"`** | **pasa** | R_SIN_ABRIR |
| **locale: `grep x $"<marzo>/v.mp4"`** | **pasa** | R_SIN_ABRIR |
| **locale: `ffprobe -show_format $"<raíz>/<marzo>/v.mp4"`** | **pasa** | R_SIN_ABRIR |
| **locale: `cd $"<carpeta de marzo>" && ffprobe -show_format v.mp4`** | **pasa** | R_SIN_ABRIR |

El de marzo se añadió a la matriz al ver los otros, y es un agujero de `main`: con el
prefijo `file:` delante, `ffprobe` sobre el vídeo de la carpeta de marzo pasaba, porque
`file:corpus/…` no es un fichero que exista y `motivo_fichero` nunca lo veía. Se cierra aquí. El
encargo dice «ninguno fuera de las cuatro formas»; lo leo como «ninguno se ABRE fuera de las cuatro
formas», y declaro estos nueve cierres: `ffmpeg -version` pasa a negarse porque no está en la lista
(nada del repo lo usa: `inventario.py` llama a `ffprobe -version` desde Python, no por Bash).

Los diez en negrita del final leían la carpeta de marzo en `main` (§12 y §15). En `cat` y `Read`, el
espacio o el punto final ya se negaban en `main` (medido: `espacio_final.py`, §12); el hueco del
espacio final era de `ffprobe`, que estaba en `SIN_LECTURA_DE_RUTAS`.

**El alcance de «ninguno se abre»** (revisor, b5): lo demuestra el test sobre los 102 casos de la
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
`not ctx.powershell`, y `analizar_powershell` no se toca). La única excepción, declarada y pedida
por el consultor: las comillas `$'…'` y `$"…"` de §1.8, que tocan `tokenizar` y `resolver` y
valen para todo Bash, y también para `.claude/hooks/solo_lectura.py`, el hook de los agentes de
solo lectura, que usa el mismo `tokenizar` (no se toca el fichero); lo que cambia con ellas está
medido en §12 y §15.

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

Al aplicar la respuesta del consultor (§12), cuatro más, resueltas igual:
- `RAIZ_REAL=… uv run python medir_respuesta.py …`: «el nombre de entorno `RAIZ_REAL` no esta en
  la lista cerrada» → «sin esa variable»: la raíz pasa como argumento del guion.
- `uv run pytest … | sed 's/\r$//'`: detrás en la tubería solo filtros de la lista → sin el `sed`.
- `cp guardia.py <carpeta de trabajo> && uv run python medir_respuesta.py …`: «antes, en el mismo
  comando, va `cp`» → en dos llamadas.
- (La misma forma, otra vez, al regenerar el anexo: en dos llamadas.)

Al aplicar la segunda respuesta (§15), dos más:
- `ls -la "$(dirname "$(which ffmpeg)")"`: «`which` va dentro de una sustitucion» → `which` suelto
  y la carpeta nombrada a mano.
- `A=<anexo> && sed -i … $A && grep -c … $A`: «el nombre de entorno `A` no esta en la lista
  cerrada» → sin la variable, con `cd` a la carpeta del anexo.

## §6 · Exposiciones

> **CORRECCIÓN (2026-10-22, `trabajo/guardia-ffmpeg`, en el commit del cierre; hallazgo de la
> sesión en la orden de cierre del consultor).** Este apartado decía «Ninguna» y llamaba a los tres
> vídeos de la medida del byte nulo «vídeos de sesión que no se protegen». Uno de ellos,
> `Grabación de pantalla 2026-10-04 105617.mp4`, es **v10, la sesión 4, en cuarentena**. Lo que se
> leyó fueron sus primeros 4096 bytes, y lo que se imprimió, solo la cabecera del contenedor y la
> posición del primer byte nulo: ningún contenido, ninguna transcripción. Va declarado en
> `docs/validation/HOLDOUT-EXPOSICIONES.md`, fila del 2026-10-22. El cuerpo de abajo queda intacto.

Ninguna. La rama no leyó material del punto 3 de `CLAUDE.md`, ni transcripciones, ni fotogramas; los
vídeos de los tests son ficheros inventados en `tmp`. Para fijar la condición de §12 se leyeron, con
un guion de Python (`cabeceras.py`, no ffmpeg), los primeros 4096 bytes de tres vídeos de sesión que
no se protegen -`2026-08-20 22-33-04.mp4` (v1), `2026-09-05 21-03-59.mkv` (v5) y `Grabación de
pantalla 2026-10-04 105617.mp4`- y se imprimió solo su cabecera de contenedor (16 bytes en hex) y
la posición del primer byte nulo: 0, 45 y 0. No es contenido de la sesión.

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
- `3372f7a` (los arreglos del revisor): `make check` exit 0, 2739 passed, `SELLO … 621a13ff…`,
  pico 295 MiB; CI de Linux, run 39830835494: `1 failed, 2727 passed, 11 skipped`, el único fallo
  el esperado (`test_state_check_ok_on_real_repo`) y el salto de más, el test de los alias (solo
  Windows).
- `c0510f2` (la respuesta del consultor, §12): `make check` exit 0, 2741 passed, `SELLO … 0bdda303…`,
  pico 297 MiB; CI de Linux, run 39871631795: `1 failed, 2729 passed, 11 skipped`, el único fallo
  el esperado. El revisor, la segunda pasada, sobre este commit (§13).
- `79a560b` (el informe del revisor pegado en §13): `make check` exit 0, 2741 passed,
  `SELLO … 0d194ea0…`, pico 297 MiB; CI de Linux, run 39876229031: `1 failed, 2729 passed, 11
  skipped`, el único fallo el esperado.
- `8347e4e` (la segunda respuesta, §15): `make check` exit 0, 2742 passed, `SELLO … 9140f35f…`,
  pico 297 MiB; CI de Linux, run 39880288314: `1 failed, 2730 passed, 11 skipped`, el único fallo
  el esperado. La pasada corta del revisor, sobre este commit (§16).
- El commit que pega esa pasada (§16), el último de la rama, con lo que se hizo con sus hallazgos
  (declararlos, y el docstring de `_comilla_de_locale`): su `make check` y su run de la CI de
  Linux no caben en el commit que sellan; van en el mensaje de entrega a Aleks, y el run que
  cuenta es ese.

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
casos que `main` dejaba pasar se niegan (§2). El consultor las aceptó todas (§11, sus respuestas
a las tres preguntas); lo que añadió su respuesta, punto por punto, en §12.

## §9 · Para el consultor, y la Next Action del cierre

**Preguntas** (ninguna bloquea la ingesta de mañana):
1. La lectura de «ninguno fuera de las cuatro formas» como «ninguno se ABRE», con los nueve cierres
   de §2 (revisor, b5).
2. El alias de la raíz en `motivo_fichero` es de `main` (revisor, a3): `cat`, `Read`, `grep -r` o
   `find … -exec cat` sobre la raíz escrita con `\\?\` o en 8.3, o sobre un directorio que CONTIENE
   el repo, pasan hoy. Aquí se cierra solo para ffmpeg (§1.4); para el resto, una línea de Technical
   Debt o una rama de G.1.
3. Las desviaciones por exceso de §8 (sobre todo la entrada binaria): si alguna sobra.

Las tres las contestó el consultor el 2026-10-22 (§11): 1, sí; 2, una línea nueva en K, la parte
prioritaria, en el commit del contrato del cierre (no un Technical Debt); 3, no sobra ninguna.

4. (Nueva, de la segunda pasada del revisor, §13 a1.) La comilla `$"…"` deja leer la carpeta de
   marzo con `cat`, `head` o `grep`, en `main` y en la rama. Opciones: (a) cerrarla aquí, como
   `$'…'`: una línea en `tokenizar` (`$"` se lee como `"`), con sus casos en la matriz, roto a
   propósito, la tabla de qué cambia frente a `main`, otro `make check` y otra CI; (b) dejarla en
   la línea prioritaria de K (ya preparada abajo). Recomiendo (a): lee material reservado, el
   arreglo es una línea, y la clase es la misma que el consultor ya mandó cerrar aquí. Coste de
   (b): el agujero sigue abierto en `main` hasta la rama de K.
   **Contestada** por el consultor el 2026-10-22 (§14): (a), se cierra en esta rama (§15).

**Next Action, preparada para el commit del contrato del cierre** (`RITUAL.md`, puntos 3 y 4; en la
rama no se toca). La K pierde la frase de ffprobe y gana, delante, la línea del alias de la raíz
(respuesta del consultor, pregunta 2, y «lo menor», tercer punto); queda:

> K. PRIORITARIA, porque lee material protegido: el alias de la raíz en motivo_fichero. Hoy pasan
> cat, Read, grep -r y find … -exec cat sobre la raíz escrita con \\?\ o con su nombre corto 8.3,
> o sobre un directorio que CONTIENE el repo; y las variables se resuelven con el entorno del hook,
> otro caso del mismo hueco (GUARDIA-FFMPEG.md §9 y §11; en ffprobe y ffmpeg ya está cerrado).
> Rama propia de la familia 1 de la guardia, con un test que rompa a propósito los dos sentidos.
> Después, la guardia exigir_sin_crudo da un falso positivo con una asignación a una variable
> llamada crudo (scripts/leer_demo_ftmo.py; DEMO-EJECUCION-1.md). Rama propia, junto a B o C si
> cabe: que la guardia nombre la forma de la opción, con un test que rompa a propósito los dos
> sentidos. Y en la misma rama, el arreglo que queda de ENTRADA-JULIO.md §8: que reconozca como
> tests los de un clon `git worktree add --detach` de comparar-con-main (`C:/cm/`), con su test de
> los dos sentidos. (ffprobe y ffmpeg: hecho en trabajo/guardia-ffmpeg, GUARDIA-FFMPEG.md.)

**Fila de `docs/runbooks/ERRORES-RECURRENTES.md`, preparada para el cierre** (respuesta del
consultor, pregunta 1): la de esta rama, con sus dos pasadas del revisor y la revisión del
consultor, y dos agujeros de `main` que se cierran aquí y leían la carpeta de marzo: `ffprobe` con
el prefijo `file:` (o con un espacio final en el nombre de la carpeta), la comilla ANSI-C `$'…'`
con escapes, que el tokenizador copiaba sin interpretar (`cat $'…Back\x74est…'`), y la comilla
de traducción `$"…"`, que dejaba el `$` en la palabra (`cat $"<marzo>/v.mp4"`; y también
`$"git" push --force`, `git commit $"--no-verify"`, `git push origin $":main"` y un heredoc
`<<$"EOF"` que escondía lo de detrás, §15). La señal: una
forma de escribir la misma ruta que la guardia no normaliza; qué hacer: cada regla mira la ruta
en todas sus formas, o niega lo que no sabe calcular.

G.1 de `docs/plan/HOJA-DE-RUTA.md` no pasa a HECHA (lo dice el encargo).

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

## §11 · Respuesta del consultor (2026-10-22, sobre `3372f7a`), copiada tal cual

> Modelo: Opus · Esfuerzo: alto
>
> Respuesta del consultor a trabajo/guardia-ffmpeg (3372f7a, run 39830835494), 2026-10-22. Cópiala tal cual al final del informe (§11) y aplícala punto por punto. La rama NO está lista: una revisión independiente del consultor sobre 3372f7a (decidir de la rama y de main cargados con importlib sobre un repo inventado en tmp; ffmpeg 6.1 real solo sobre vídeos inventados con lavfi) da por buenos los arreglos de b1 a b7 y encuentra dos cosas nuevas.
>
> LO NUEVO, A ARREGLAR EN ESTA RAMA
> 1. BLOQUEA. Una lista HLS con un byte nulo burla la comprobación de «entrada de texto». _ffmpeg_es_texto solo busca \x00 en los primeros 4096 bytes, y la lista cerrada no limita la entrada. Se escribe fuera del repo, con printf o con Write, un p.m3u8 con «#EXTM3U», un «#EXTINF:3,\0» y la ruta absoluta del vídeo de la carpeta de marzo; después «ffprobe -v error -show_format -show_streams "<F>/p.m3u8"», la extracción y volumedetect sobre él PASAN en la rama (en main, R_EJECUCION), y ffprobe real devuelve format_name=hls con los códecs del vídeo de marzo. Arreglo, nombrando la condición: una entrada solo vale si es un contenedor de vídeo reconocido por sus bytes mágicos (ISO BMFF: «ftyp» en el desplazamiento 4; Matroska/WebM: 1A 45 DF A3 al principio) Y su extensión es .mp4, .mov, .mkv o .webm. Todo lo demás se niega, también un fichero que no se puede leer. _ffmpeg_es_texto se queda como segunda barrera o sale si sobra: dilo.
> 2. IMPORTA (lo abre la rama) y BLOQUEA (heredado de main). La comilla ANSI-C $'…' no se interpreta: el tokenizador copia su interior tal cual. En la rama, «ffmpeg -i "<vídeo>" -vn -sn -dn $'<R>\x2fa.wav'» pasa y bash escribe dentro del repo. Y en main y en la rama, «ffprobe -show_format $'…/Back\x74est marzo 2026/v.mp4'», «ffmpeg -i $'…\164…' …», «cat $'…\x74…'» y «cd $'…\x74…' && ffprobe v.mp4» PASAN: leen la carpeta de marzo. Arreglo, para toda la guardia y no solo para ffmpeg: una palabra con comilla ANSI-C que lleve una barra invertida tiene valor desconocido (como una sustitución), y lo que ya se niega con un valor desconocido se niega. Mide antes en qué reglas cambia la decisión, ponlo en la tabla de comparación con main, y que test_el_ritual_y_los_runbooks_pasan y test_ninguna_denegacion_toca_el_ritual sigan en verde. Es una ampliación del encargo, declarada: el agujero lee material protegido y el arreglo es de una línea de condición.
> Cada uno con sus casos en la matriz y roto a propósito en los dos sentidos (sin la comprobación de los bytes mágicos, el .m3u8 vuelve a pasar; con ella, un .mp4 de verdad sigue pasando; sin el arreglo de $'…', los cuatro de arriba pasan). En Windows, ejecuta además el test de los alias que se salta en Linux (8.3 y \\?\) y mide «…\Bot v3.\a.wav» y «…\Bot v3 \a.wav» como salida: tienen que quedar dentro del repo y negarse. Las salidas, al informe.
>
> TUS TRES PREGUNTAS DEL §9
> 1. Sí. «Ninguno fuera de las cuatro formas» quería decir que no se abre nada nuevo. Que nueve comandos que main dejaba pasar ahora se nieguen está bien, y el de ffprobe con file: sobre la carpeta de marzo era un agujero: va declarado en el informe y a la fila de ERRORES-RECURRENTES en el cierre.
> 2. El alias de la raíz (\\?\, el nombre corto 8.3 y un directorio que contiene el repo) que hoy deja pasar cat, Read y grep -r: una línea nueva en K de la Next Action, en el commit del contrato del cierre, como la parte prioritaria de K, porque lee material protegido. No se arregla aquí: es otra familia de reglas. Prepara el texto en el §9.
> 3. No sobra ninguna. Negar las entradas de texto se queda (ahora con la condición del punto 1); negar \\ y // y cualquier redirección de entrada, también. nul en minúsculas, bien.
>
> LO MENOR (sin cambios, al informe)
> - «ffprobe "<vídeo>" &» solo pasa: se acepta, no abre nada.
> - Una línea partida con barra invertida y salto se niega: se acepta; la skill no la usa.
> - Las variables se resuelven con el entorno del hook (de main): a la línea de K del punto 2, como otro caso del mismo hueco.
>
> DESPUÉS
> make check sellado, commit, push a fix/guardia-ffmpeg y la CI de Linux con un gh run view suelto (dame el número). Después el revisor OTRA VEZ, sobre el último commit y con el informe terminado, con el encargo de comprobar los arreglos de esta respuesta y de intentar romper la regla con formas que no estén en la matriz (envoltorios, comillas, escapes, ficheros que se hacen pasar por otro formato). Su informe, pegado al final.
>
> Rama lista para revisión, NO cerrada.

## §12 · La respuesta, punto por punto

Antes de tocar nada se midió lo que dice la respuesta, con `decidir` de tres guardias -la de `main`
(`git show main:`), la de `3372f7a` y la nueva- sobre un repo inventado en `tmp`, sin ejecutar
ffmpeg (`medir_respuesta.py` en la carpeta de trabajo; salida entera en
`anexos/GUARDIA-FFMPEG/respuesta-consultor-medida.txt`).

### Punto 1 (bloquea): la lista HLS con un byte nulo

| Caso | main | 3372f7a | rama |
|---|---|---|---|
| `ffprobe -v error -show_format -show_streams "<fuera>/p.m3u8"` | R_EJECUCION | **pasa** | R_FFMPEG |
| la extracción sobre `p.m3u8` | R_EJECUCION | **pasa** | R_FFMPEG |
| `volumedetect` sobre `p.m3u8` | R_EJECUCION | **pasa** | R_FFMPEG |

Reproducido: en `3372f7a` las tres pasaban. Hecho: la condición nombrada de la respuesta,
`_ffmpeg_es_video` (§1.4): extensión `.mp4`, `.mov`, `.mkv` o `.webm` Y bytes mágicos (`ftyp` en
el 4, o `1A 45 DF A3` en el 0); todo lo demás se niega, también lo que no existe o no se puede
leer. **`_ffmpeg_es_texto` se queda, como segunda barrera**: sola no basta (un nulo la burla, que es
el hallazgo), pero no cuesta nada sobre los vídeos de verdad -el primer nulo de tres vídeos de
sesión medidos cae en el byte 0 (los dos mp4) y en el 45 (el mkv)- y niega un fichero que lleva
`ftyp` en el 4 y es texto (caso «ftyp en un texto sin nulos»).

En la matriz, siete casos nuevos: las tres de arriba, la misma lista llamada `.mp4`, los bytes de
un mp4 en un `.txt`, `ftyp` en un texto sin nulos y una entrada que no existe (esta, de `pasa` en
`main` a `R_FFMPEG`). Los vídeos del test llevan ahora la cabecera real de 16 bytes de v1 (mp4) y
de v5 (mkv), y pasan ffprobe y volumen sobre el `.mkv` (dos permitidas nuevas).

Roto a propósito: `test_sin_los_bytes_magicos_la_lista_hls_vuelve_a_pasar` -con `_ffmpeg_es_video`
siempre verdadero, las tres HLS PASAN-; y con la comprobación, los vídeos de verdad pasan (las
permitidas de la matriz).

**Lo que no pude medir:** qué hace ffmpeg de verdad con un fichero que lleva los bytes mágicos y
algo más (no se ejecuta ffmpeg). Por lo que se sabe de sus formatos -no medido aquí-, los que
nombran otros ficheros buscan su marca en el byte 0 (`#EXTM3U`, `ffconcat version`) o leen el
fichero entero como XML (un `.mpd` de DASH), y ninguno de los dos casa con un fichero que empieza
por una caja `ftyp` o por la marca de Matroska. Va al revisor (§13) como forma que intentar.
(Después: el consultor lo acepta como riesgo residual, acotado como se dice en §15.)

### Punto 2 (importa y bloquea): la comilla ANSI-C

| Caso | main | 3372f7a | rama |
|---|---|---|---|
| `ffmpeg -i "<vídeo>" -vn -sn -dn $'<raíz>\x2fa.wav'` | R_EJECUCION | R_FFMPEG en Windows (la `\` es un separador y la ruta cae dentro); **pasa** en Linux (la medida del consultor) | R_FFMPEG |
| `ffprobe -show_format $'…/Back\x74est marzo 2026/v.mp4'` | **pasa** | **pasa** | R_FFMPEG |
| `ffmpeg -i $'…/Back\164est marzo 2026/v.mp4' … -` | **pasa** | **pasa** | R_FFMPEG |
| `cat $'…/Back\x74est marzo 2026/v.mp4'` | **pasa** | **pasa** | niega (argumento dinámico) |
| `cd $'…/Back\x74est marzo 2026' && ffprobe -show_format v.mp4` | **pasa** | **pasa** | R_EJECUCION |

Reproducido: los cuatro que leen la carpeta de marzo pasaban en `main` y en `3372f7a`. Hecho, para
toda la guardia (§1.8): `$'…'` con una barra invertida tiene valor desconocido.

**Antes del arreglo se midió en qué reglas cambia la decisión** (la misma tabla, más filas; con
`$X` sin valor al lado, para comparar):

| Comando | main | rama | Por qué |
|---|---|---|---|
| `head -c 10 $'…\x74…/v.mp4'`, `grep -f $'…\x74…' f`, `echo $(cat $'…\x74…')`, `bash -c "cat $'…\x74…'"` | pasa | niega (argumento dinámico) | como `cat "$X"`, que ya se niega en `main` |
| `grep $'\t' otro.wav` | pasa | niega (argumento dinámico) | el patrón es dinámico; la forma literal es `grep -P '\t'` |
| `git log --format=$'%h\t%s' -1` | excepción en el repo de `tmp` (la regla de git lee `knowledge/corpus/fuentes.yaml`, que allí no existe); no medido en el real | niega | `git log` con un argumento dinámico, como con `$X` |
| `ls $'…\x74…'`, `sha256sum $'…\x74…/v.mp4'` | pasa | pasa | listar y hashear se dejan también con un argumento dinámico, como en `main` |
| `echo $'a\nb'`, `printf $'%s\n' x` | pasa | pasa | no leen ficheros |
| `sed -n $'1p' f`, `awk $'{print}' f`, `cat $'otro.wav'`, `echo $'hola'` | pasa | pasa | sin barra: literal, como antes |
| `IFS=$'\n'; ls`, `sed -n $'1r …'`, `awk $'BEGIN{…getline…}'`, `source $'…'` | niega | niega | ya negados por otra regla |
| `echo $'a\'b' && cat otro.wav` | niega («una comilla simple sin cerrar») | **pasa** | el final de la comilla se busca ahora saltando `\'`: la línea se parte bien. El único caso que pasa a PASAR; no abre nada (un `echo` y un fichero sin proteger) |

Ni el ritual, ni los runbooks, ni las skills, ni el Makefile usan `$'…'` (`grep -rn "\$'"` sobre
`docs/runbooks`, `.claude/skills`, `CLAUDE.md`, `Makefile`, `scripts` y `.github`: solo `.pyc`).
`test_el_ritual_y_los_runbooks_pasan` y `test_ninguna_denegacion_toca_el_ritual` (62 casos) y
`test_guardia_claude.py` entero, en verde con el arreglo.

En la matriz, cinco casos nuevos (los de la primera tabla) y una permitida: `$'…'` sin barra. Roto a
propósito: `test_sin_el_arreglo_de_la_comilla_ansi_c_los_cuatro_pasan`, con `_ansi_c_con_escapes`
siempre falso, como en `main`. **Matiz medido:** sin ese arreglo, `cat` pasa, pero los tres de
ffmpeg los sigue negando la barrera del punto 1 -la guardia mira la ruta sin interpretar, que no
existe, y una entrada que no se puede leer se niega-; sin las dos barreras, pasan los cuatro. El
test comprueba las dos cosas.

### Punto 2, la medida de Windows

`test_un_alias_de_la_raiz_no_saca_la_salida_ni_abre_la_entrada`, ejecutado en esta máquina: pasa,
con el nombre corto real de la raíz del repo de `tmp`
(`C:\Users\USER\AppData\Local\Temp\PYTEST~1\PYTEST~2\TEST_U~1\repo`): `\\?\<raíz>\a.wav` y
`<raíz 8.3>\a.wav` se niegan con `R_FFMPEG`, y `ffprobe` sobre `<raíz 8.3>\…\marzo\v.mp4`, con
`R_SIN_ABRIR`.

La salida en la raíz con un punto o un espacio al final del nombre, con la raíz real del repo y con
la de `tmp`:

| Salida | main | 3372f7a | rama |
|---|---|---|---|
| `C:\Users\USER\Desktop\Bot v3.\a.wav` | pasa | R_FFMPEG | R_FFMPEG |
| `C:\Users\USER\Desktop\Bot v3 \a.wav` | pasa | **pasa** | R_FFMPEG |
| `C:\Users\USER\Desktop\Bot v3. \a.wav` | pasa | **pasa** | R_FFMPEG |
| `C:\Users\USER\Desktop\Bot v3..\a.wav` | pasa | **pasa** | R_FFMPEG |
| `<tmp>\repo.\a.wav` | R_EJECUCION | R_FFMPEG | R_FFMPEG |
| `<tmp>\repo \a.wav` (y `repo. `, `repo..`) | R_EJECUCION | **pasa** | R_FFMPEG |

Con el punto pasaba ya bien (`realpath` lo quitaba); con el espacio, NO: `3372f7a` dejaba escribir
dentro del repo. Arreglado con `_ffmpeg_formas_de_la_ruta`: la ruta se mira también sin los puntos
ni espacios del final de cada nombre, para la salida, para las redirecciones y para la entrada. En
la matriz, cuatro casos: la salida con punto, con espacio y con los dos, y `ffprobe` sobre la
carpeta de marzo con un espacio final, que en `main` PASABA (ffprobe estaba en
`SIN_LECTURA_DE_RUTAS`) y ahora niega con `R_SIN_ABRIR`. En Linux un nombre con espacio final es
otro directorio: negarlo allí es negar de más y no abre nada. En `main`, las de la raíz real
pasaban porque allí el vídeo del comando no existe y la regla del programa desconocido solo mira
ficheros que existen (en `tmp`, donde existe, niega con `R_EJECUCION`); es la regla que esta rama
sustituye para ffmpeg. Para `cat` y `Read`, el punto y el espacio final ya se niegan en `main`
(medido con `espacio_final.py`).

### Las tres preguntas del §9

1. «Ninguno se abre»: aceptado. El de `file:` sobre marzo va declarado en §2 y a la fila de
   `ERRORES-RECURRENTES.md` del cierre, preparada en §9.
2. El alias de la raíz: no se arregla aquí. La línea de K, la parte prioritaria, preparada en §9
   para el commit del contrato del cierre.
3. No sobra ninguna: sin cambios.

### Lo menor

- `ffprobe "<vídeo>" &` solo, pasa: aceptado (el caso «en segundo plano» de la matriz, con algo
  detrás, sigue negado).
- La línea partida con barra invertida y salto se niega: aceptado; la skill no la usa.
- Las variables con el entorno del hook: a la línea de K (§9), como otro caso del mismo hueco.

### Después

Matriz: 94 casos (19 permitidas, 75 negadas); frente a `main`, se abren solo las 19 permitidas y
se cierran quince (§2). `test_guardia_ffmpeg.py` (7 pruebas, la de los alias solo en Windows) y
`test_guardia_claude.py` enteros, en verde antes del sello. El `make check`, el commit, el push a
`fix/guardia-ffmpeg` y el run de la CI de Linux, en el mensaje de entrega (§7). El revisor, otra
vez, en §13.

## §13 · El revisor, segunda pasada

Lanzado sobre `c0510f2` (el commit de §12), con este informe terminado y el encargo de la respuesta
del consultor: comprobar sus arreglos e intentar romper la regla con formas que no estén en la
matriz (envoltorios, comillas, escapes, ficheros que se hacen pasar por otro formato). Resultado:
eje (b), 8 de 8 hechos y ningún hallazgo; la regla aguantó todo lo que probó fuera de la matriz.
Eje (a), un «importa» heredado de `main`.

### Lo que se hizo con los hallazgos del revisor (segunda pasada)

| # | Gravedad | Qué se hizo |
|---|---|---|
| a1 | importa (de `main`) | **No se arregla en esta rama.** La comilla `$"…"` (traducción de locale) se tokeniza con el `$` literal, y `cat`, `head` o `grep` sobre `$"<carpeta de marzo>/v.mp4"` pasan en `main` y en la rama. No atraviesa la regla de ffmpeg (allí niega `R_FFMPEG`). El encargo dice que no cambia «cualquier otra regla de la guardia salvo lo declarado», y la respuesta del consultor amplió solo a `$'…'`: ampliar otra vez lo decide el consultor (pregunta 4 de §9). El arreglo propuesto es de una línea: en `tokenizar`, `$"` se lee como `"` (sin catálogo de traducción, bash da el mismo texto). Mientras, va a la línea prioritaria de K, preparada en §9. **Después:** el consultor eligió (a) y se cerró en esta rama (§14, §15); la línea de K ya no la nombra. |
| — | «lo que no pude comprobar» | Qué hace ffmpeg con un fichero que lleva los bytes mágicos y algo más: sin medir, en §12 y aquí. Un enlace que cambia entre la decisión y la ejecución: fuera del alcance de una guardia que decide antes; el enlace que ya existe se resuelve con `realpath`. Las permitidas con un envoltorio delante y las redirecciones `2>>`, `&>` o `3>` con una entrada válida: no medidas por el revisor (solo lee); el bucle de las salidas no mira el operador. |

### Informe del revisor, segunda pasada (pegado tal cual)

## Informe del revisor · trabajo/guardia-ffmpeg · 2026-10-22 (SEGUNDA pasada, sobre c0510f2)

Base: `git merge-base main HEAD` = 8cfed04. Commits de la rama: 0252d4f (apertura), 4dbb48b (regla), 3372f7a (hallazgos 1a pasada), c0510f2 (respuesta del consultor). `git status --short` vacío. Todo lo medí con `decidir` de la rama (HEAD) y de `main`, cargando el fuente de cada una con `exec` del `git show` (sin escribir a disco) y apuntando `Politica` al repo real, para que `motivo_fichero` sea el de verdad; nunca ejecuté ffmpeg ni ffprobe. Soy de solo lectura: no pude usar Write ni crear ficheros con Bash (lo niega `solo_lectura.py`), así que no monté un repo de `tmp` con vídeos propios; medí sobre entradas inventadas/inexistentes y rutas protegidas reales (sin abrir su contenido), y para confirmar que las PERMITIDAS PASAN me apoyo en la matriz del test (fixtures con cabeceras reales, en verde local y en CI).

### Eje (a) · Reglas de la casa
Resumen: 0 bloquea, 1 importa, 0 menor.

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| a1 | importa (heredado de `main`, NO lo introduce la rama) | La comilla de traducción de locale `$"..."` no se interpreta: el tokenizador conserva el `$` literal, y con eso un lector normal lee material reservado. `cat $"<marzo>"`, `head -c 10 $"<marzo>"` y `grep x $"<marzo>"` **PASAN en la rama Y en main**, mientras bash quita el `$` y abre el vídeo real de la carpeta de marzo (holdout/material reservado, CLAUDE.md §3). Es el hermano exacto del agujero de `$'...'` que el consultor mandó cerrar en esta rama «porque lee material protegido»: el arreglo de la rama (`_ansi_c_con_escapes`, `tokenizar`) cubre `$'...'` pero no `$"..."`. No rompe la regla de ffmpeg (sobre una entrada `$"..."` la regla niega con R_FFMPEG, porque la ruta con `$` no es un vídeo válido), ni es un fallo de implementar lo que el consultor pidió (pidió ANSI-C `$'...'`); es un agujero guard-wide que esta pasada destapa al «intentar romper con comillas». | Medido rama vs main: `cat $"corp…/Back…test marzo 2026/v.mp4"` → rama PASA, main PASA. Control: `cat "<marzo>"` (comillas normales) → las dos «leer el contenido de corpus/…». Control del hermano ya cerrado: `cat $'…Back\x74est…'` → rama niega («el argumento `$'corpus/…` se construye al ejecutarse»), main PASA. En la regla de ffmpeg: `ffprobe -show_format $"<marzo>"` → rama R_FFMPEG (ruta `$corpus/…`, no es contenedor). |

Comprobado sin hallazgos:
- **Contrato:** `uv run python scripts/contrato_rama.py` → «CONTRATO: 12 ficheros dentro del contrato … 3 comprobaciones». Comprobación 1 (`contrato_rama.py`) ✓. Comprobación 2 (`uv run pytest -q tests/unit/test_guardia_claude.py tests/unit/test_guardia_ffmpeg.py`) → todo en puntos, sin F ni E. Comprobación 3 (`make check`, que escribe → no la ejecuto): en `make-check.log` «2741 passed», «SELLO … sobre el arbol 0bdda303d6b5ef94ba243eb1567b5fb42d737abd», «PICO DE MEMORIA … 297 MiB»; `git rev-parse c0510f2^{tree}` = 0bdda303… (coincide con el sello).
- **CI:** `gh run view 39871631795` → headSha c0510f2, fix/guardia-ffmpeg, conclusion failure con `1 failed, 2729 passed, 11 skipped`; el único FAILED es `tests/unit/test_cli.py::test_state_check_ok_on_real_repo` (rama `fix/`, único fallo aceptado); el 11º skip es el test de alias (solo Windows). El informe §7 dice que ese run es «el que cuenta»; cuadra.
- **Trailers `Fuente:`, ADR, ambigüedades, guardias de `cita`, evidencia nueva:** no aplican. `git log main..HEAD -- knowledge/spec knowledge/cases` vacío; ningún commit toca `knowledge/`, `docs/adr/`, `data/manifests/` ni ambigüedades.
- **Regímenes de cambio:** `git diff --name-status main...HEAD` → solo M/A sobre rutas del contrato (`guardia.py`, `ingerir-sesion/SKILL.md`, `PROJECT_STATE.md`, `HISTORIA.md`, `contrato.yaml`, encargo, informe y anexos, `test_guardia_ffmpeg.py`). Ningún directorio inmutable tocado.
- **Informes cerrados:** ninguno modificado (GUARDIA-FFMPEG.md es A/nuevo).
- **PROJECT_STATE:** 22.628 bytes (< 25.000). El informe acaba en «Rama lista para revisión, NO cerrada» y el Estado = TERMINADA, pendiente de revisión del consultor.
- **Material protegido:** no lo abrí; sobre rutas de marzo solo medí `motivo_fichero`/`decidir` (que niegan sin leer).

### Eje (b) · Encargo (original + respuesta del consultor §11)
Resumen: 0 bloquea, 0 importa, 0 menor. Requisitos: 8 hechos, 0 parciales, 0 no hechos.

| # | Requisito (respuesta del consultor + encargo de esta pasada) | Estado | Evidencia |
|---|---|---|---|
| 1 | Punto 1: la entrada solo vale si es contenedor de vídeo por extensión (.mp4/.mov/.mkv/.webm) Y bytes mágicos (ftyp@4; `1A45DFA3`@0); `_ffmpeg_es_video`/`_ffmpeg_es_texto` | Hecho | `guardia.py` `_ffmpeg_es_video`, `MAGIA_ISO_BMFF`, `MAGIA_MATROSKA`, `EXTENSIONES_DE_VIDEO`; medido: `.m3u8`, `.mpd`, `.ffconcat`, `.mp4`/`.MP4` inexistente, `.mov` → todas R_FFMPEG «no es un contenedor»; `_ffmpeg_es_video(inexistente)=False`, `(.mpd)=False`. `_ffmpeg_es_texto` declarado como 2ª barrera (§1.4) |
| 2 | Punto 2: `$'...'` con barra invertida = valor desconocido, para TODA la guardia (`_ansi_c_con_escapes`, `tokenizar`, `sustitucion`, `resolver`); tabla de qué cambia vs main; `test_el_ritual_y_los_runbooks_pasan` y `test_ninguna_denegacion_toca_el_ritual` en verde | Hecho | Diff de `tokenizar` y `resolver`; `cat $'…\x74…'` rama niega / main pasa; los 5 casos ANSI-C de la matriz; §12 tiene la tabla de reglas que cambian; los dos tests en verde (suite completa de `test_guardia_claude.py` passed) |
| 3 | Windows: `_ffmpeg_formas_de_la_ruta` (puntos/espacios finales) y el test de alias (8.3, `\\?\`); salidas `…\Bot v3.\a.wav` y `…\Bot v3 \a.wav` dentro del repo y negadas | Hecho | `test_un_alias_de_la_raiz…` corrió en esta máquina Windows y pasó (en CI Linux es el 11º skip); §12 tabla de salidas con punto/espacio → R_FFMPEG. Confirmado a nivel función: salida `\\?\<raíz>\data\a.wav` la corta `_ffmpeg_ruta` (prefijo `\\`); `../fuera/a.wav` dentro=False, `data/a.wav` dentro=True |
| 4 | Cada arreglo roto a propósito en los dos sentidos | Hecho | `test_sin_los_bytes_magicos_la_lista_hls_vuelve_a_pasar`, `test_sin_el_arreglo_de_la_comilla_ansi_c_los_cuatro_pasan` (+ la variante «y sin los bytes magicos»); todos en verde |
| 5 | K y fila de ERRORES-RECURRENTES del §9 según la respuesta | Hecho | §9: K reescrita (alias de la raíz como parte prioritaria + variables con el entorno del hook) y fila de ERRORES preparada (file: y espacio final, y `$'…'`) |
| 6 | Intentar romper con envoltorios | Hecho (la regla aguanta) | env/command/exec/nice/timeout/nohup/stdbuf/time/bash -c/sh -c/`\ffprobe`/`/usr/bin/ffprobe`/`ffprobe.exe`/`command -p`/`builtin`/`timeout env`: todos ENCAMINADOS a la regla de ffmpeg (rama R_FFMPEG donde main PASA); sobre marzo → rama niega con el motivo (R_SIN_ABRIR). `env -C <dir>`, `uv --directory`, `xargs`, `FFREPORT` → IndecidibleError/R_EJECUCION en rama y main |
| 7 | Intentar romper con comillas/escapes/redirecciones | Hecho | Concatenación de comillas bien cerrada sobre marzo → R_SIN_ABRIR; backslash-escapando los espacios de marzo → R_SIN_ABRIR; llaves `{v,w}` y `$S/…` y glob → «se construye al ejecutarse»; `~` expandido; `0< <marzo>` y `<<<` → redirección de entrada negada; `$"..."` → ver a1 (único escape que filtra, por lectores no-ffmpeg). Redirecciones de salida raras (`2>>`, `&>`, `3>`) sobre un fichero del repo: la regla las trata en el mismo bucle `_ffmpeg_dentro_del_repo` que la matriz prueba con `2>` y `>`; no pude llegar a ese bucle con una entrada inexistente (el chequeo de la entrada dispara antes), así que su cierre lo verifico por lectura de código, no empíricamente |
| 8 | Ficheros que se hacen pasar por otro formato | Hecho hasta donde no hace falta ejecutar | La reja de extensión niega de entrada `.m3u8`/`.mpd`/`.ffconcat`/`.m3u` (no son `.mp4/.mov/.mkv/.webm`). Un fichero con los bytes mágicos de mp4/mkv renombrado `.mp4` pasaría `_ffmpeg_es_video` y `_ffmpeg_es_texto`; que ffmpeg lo trate como mov/mp4 (y NO como lista HLS/DASH/IMF/ffconcat) es el razonamiento del consultor §12, que no re-medí (ver «Lo que no pude comprobar») |

Sin hallazgos en el eje (b): los dos arreglos de la respuesta del consultor están implementados tal como se pidió, con sus casos en la matriz, rotos en los dos sentidos, y los tests del ritual en verde. La regla de ffprobe/ffmpeg aguantó TODAS las formas que probé fuera de la matriz: ningún envoltorio, comilla, escape o redirección consiguió que la regla ABRIERA un vídeo que no debe ni que una entrada protegida pasara; los envoltorios se despojan y se encaminan a `_analizar_ffmpeg` (que vuelve a pasar por `motivo_fichero`). El único escape que filtra (`$"..."`) NO atraviesa la regla de ffmpeg: filtra por `cat`/`head`/`grep`, y por eso es un asunto de la guardia entera (eje a, a1), no de esta rama.

### Lo que no pude comprobar
- **Qué hace ffmpeg de verdad con un fichero que lleva los bytes mágicos de mp4/mkv y además es una lista (DASH `.mpd`, IMF, HLS, `ffconcat`):** no se ejecuta ffmpeg (prohibido por el encargo, y además la CLI no está en mi entorno). La reja de extensión ya niega esas extensiones; un fichero disfrazado de `.mp4` con `ftyp`@4 y sin nulos pasaría las dos barreras de la guardia, y el que ffmpeg elija el demuxer mov/mp4 por puntuación de sonda (y no la lista) es el razonamiento del consultor (§12), no una medida mía.
- **TOCTOU / enlaces que cambian entre decisión y ejecución:** la guardia resuelve enlaces con `realpath` en el momento de decidir (un symlink a marzo se cierra por ahí), pero no puede defenderse de un enlace o una ruta que se cree o cambie DESPUÉS de decidir y antes de que ffmpeg abra. No medible sin escribir en disco.
- **Confirmar que las 19 PERMITIDAS PASAN con un envoltorio delante (p. ej. `timeout 10 ffmpeg -i <vídeo válido> …`):** necesitaría un vídeo real con cabecera válida en disco, y no puedo crear ficheros (agente de solo lectura). Mis medidas de envoltorios usan entradas inexistentes, que dan R_FFMPEG «no es contenedor»: eso demuestra que el envoltorio se despoja y se encamina a la regla de ffmpeg, no que un vídeo válido envuelto pase. El PASO de las PERMITIDAS lo cubre `test_la_matriz_de_ffmpeg` con los fixtures (verde local y en el CI Linux, donde además se instaló ffmpeg).
- **Las redirecciones de salida `2>>`, `&>`, `3>` a un fichero del repo con una entrada VÁLIDA:** no pude observar ese tramo (el chequeo de la entrada dispara antes con entrada inexistente, y no puedo crear un vídeo válido); su cierre lo verifico por lectura del bucle `for op, destino in cmd.salidas` de `_analizar_ffmpeg`, que trata cualquier `destino` por `_ffmpeg_dentro_del_repo` sin mirar el operador.
- **Literalidad del encargo y de la respuesta del consultor copiados:** no los comparo con el prompt original.

### Comandos ejecutados
1. `git branch --show-current && git merge-base main HEAD && git log --format='%h %s' main..HEAD && git diff --stat main...HEAD && git status --short`
2. Lecturas: `contrato.yaml`, encargo, `GUARDIA-FFMPEG.md` (entero, dos páginas), `test_guardia_ffmpeg.py`, y tramos de `guardia.py` (`analizar_comando`, `_envoltorios`, `_ejecucion_de_un_programa_desconocido`, `_exigir_lo_de_antes/_a_la_vez`, `_es_fichero_programa`, el bloque `_analizar_ffmpeg` y el diff `main...HEAD`), `solo_lectura.py`.
3. `uv run python scripts/contrato_rama.py` (en su propia llamada; la guardia me negó encadenarlo tras `cat contrato.yaml` → lo leí con Read y lo ejecuté suelto).
4. `uv run pytest -q tests/unit/test_guardia_claude.py tests/unit/test_guardia_ffmpeg.py` (y `-rs` para ver que no hay skips inesperados en local): todo passed.
5. `grep -nE "SELLO|PICO DE MEMORIA|passed|failed" make-check.log`; `git rev-parse c0510f2^{tree} 3372f7a^{tree}`.
6. `gh run view 39871631795` (suelto); `gh run view 39871631795 --log-failed | grep …`; `gh run view 39871631795 --json headSha,headBranch,conclusion`.
7. Cinco `uv run python -c "…"` que exec'an las dos guardias (rama = `git show HEAD:…`, main = `git show main:…`) y llaman a `decidir`/`motivo_fichero`/`_ffmpeg_*` sobre: envoltorios con entrada inventada; protegido vía envoltorios/quoting/redirecciones; concatenación de comillas y `$"..."` y backslash-espacios; lectores no-ffmpeg con `$"..."`/`$'...'`/comillas; reja de extensión y normalización. Ninguno escribe en disco.
8. `git diff --name-status main...HEAD`; `git log main..HEAD -- knowledge/spec knowledge/cases`; `wc -c PROJECT_STATE.md`; `tail docs/validation/GUARDIA-FFMPEG.md`.

### Recomendación (para el consultor)
El único hallazgo, a1 (`$"..."` lee material reservado por `cat`/`head`/`grep`, en main y en la rama), es de la misma clase que el alias de la raíz y la expansión de variables que ya van a la línea K del cierre: no rompe la regla de ffmpeg ni contradice lo que el consultor pidió, pero es el hermano de `$'...'` y lee holdout. Encaja en la K (parte prioritaria, con el alias y las variables), no en esta rama salvo que el consultor decida ampliarla otra vez como hizo con `$'...'`. El fuente relevante: `C:\Users\USER\Desktop\Bot v3\.claude\hooks\guardia.py` (`tokenizar`, el tramo `$'`/`$"`), `C:\Users\USER\Desktop\Bot v3\docs\validation\GUARDIA-FFMPEG.md` (§9, la K) y `C:\Users\USER\Desktop\Bot v3\tests\unit\test_guardia_ffmpeg.py`.

Este informe va al §13 del informe de la rama; no lo pego yo (lo devuelvo, como pide el encargo).

## §14 · Segunda respuesta del consultor (2026-10-22, sobre `79a560b`), copiada tal cual

> Modelo: Opus · Esfuerzo: alto
>
> Segunda respuesta del consultor a trabajo/guardia-ffmpeg (79a560b, run 39876229031), 2026-10-22. Cópiala tal cual al final del informe y aplícala.
>
> 1. Pregunta 4 del §9 (la comilla $"…"): opción (a), se cierra en esta rama. Por qué: lee material protegido, es la misma clase que ya mandé cerrar aquí ($'…') y el arreglo es de una línea con la condición nombrada: en el tokenizador, $"…" se lee como "…" (bash solo traduce la cadena según el idioma, nunca la convierte en otra ruta). Con sus casos en la matriz (cat, head, grep, ffprobe, cd sobre la carpeta de marzo con $"…"; y un $"…" legítimo fuera de lo protegido, que pasa), roto a propósito en los dos sentidos, en la tabla de comparación con main, y los dos tests del ritual en verde.
> 2. Lo que queda sin medir (un fichero con los bytes mágicos y algo más dentro): se acepta como riesgo residual y se escribe así en el informe. Dos cosas lo acotan y hay que dejarlas dichas: la lista cerrada no admite ninguna opción de demuxer (por ejemplo, -enable_drefs, la que haría que el demuxer de MP4 siga referencias a ficheros externos), y la entrada tiene que pasar motivo_fichero por su propia ruta. Verifica en la documentación de ffmpeg de la versión que hay en la máquina que enable_drefs viene desactivado por defecto, y apunta la versión y la fuente; si no lo puedes verificar, dilo así, sin afirmarlo.
> 3. Después: make check sellado, commit, push a fix/guardia-ffmpeg y la CI de Linux con un gh run view suelto; dame el número. El revisor, una pasada corta solo sobre el diff de este commit (el arreglo de $"…" y su matriz), pegada al final.
>
> Con eso la rama queda para su orden de cierre. Rama lista para revisión, NO cerrada.

## §15 · La segunda respuesta, punto por punto

### Punto 1: la comilla `$"…"`, cerrada aquí

Hecho, con la condición nombrada de la respuesta: `_comilla_de_locale` en `tokenizar` (§1.8);
un `$` seguido de `"` no entra en la palabra, y lo que sigue se lee como una comilla doble. Dentro
de un `$(...)` no hace falta nada más: su interior se vuelve a tokenizar con la misma regla.

En la matriz, los cinco casos que pide la respuesta sobre la carpeta de marzo, todos `R_SIN_ABRIR`
(antes, en `main`, los cinco PASABAN): `cat $"<marzo>/v.mp4"`, `head -c 10 $"…"`, `grep x $"…"`,
`ffprobe -show_format $"<raíz>/<marzo>/v.mp4"` y `cd $"<carpeta de marzo>" && ffprobe -show_format
v.mp4`; y el legítimo, `ffprobe -v error -show_format $"<vídeo de la sesión>"`, que pasa (y que ya
pasaba en `main`, §2).

Roto a propósito: `test_sin_el_arreglo_de_la_comilla_de_locale_los_cinco_pasan`, con
`_comilla_de_locale` siempre falso, como en `main`: `cat`, `head` y `grep` PASAN; `ffprobe` y el
`cd` los para además la barrera de los bytes mágicos (la ruta con `$` no existe); y sin esa barrera
también, pasan los cinco. En el otro sentido, con el arreglo, los cinco se niegan y el del vídeo
pasa (la matriz).

Qué cambia fuera de la matriz, medido con `decidir` de `main` y de la rama sobre un repo de `tmp`
(`medir_locale.py`; salida entera en `anexos/GUARDIA-FFMPEG/locale-medida.txt`):

| Comando | main | rama |
|---|---|---|
| `echo $"hola"`, `printf $"%s\n" x` | pasa | pasa |
| `cat $"notas.txt"`, `grep hola $"notas.txt"` (sin proteger) | pasa | pasa |
| `ls $"<carpeta de marzo>"`, `sha256sum $"<marzo>/v.mp4"` (listar y hashear) | pasa | pasa |
| `cat $"<marzo>/v.mp4"` | **pasa** | R_SIN_ABRIR |
| `cat corp$"us/…/<marzo>/v.mp4"` (pegada a otra palabra) | **pasa** | R_SIN_ABRIR |
| `cat $"$X_NO/v.mp4"` (una variable sin valor dentro) | niega (dinámico) | niega (dinámico) |
| `cat $"$(pwd)/notas.txt"` | R_EJECUCION | R_EJECUCION |
| `git log --format=$"%h %s" -1` | excepción en el repo de `tmp` (le falta `knowledge/corpus/fuentes.yaml`) | la misma |

En esa tabla solo cambia lo que leía material protegido. **Pero el arreglo cierra más de lo que
decía la tabla** (pasada corta del revisor, §16, a1; las cuatro primeras, medidas también por la
sesión con `decidir` de `main` y de la rama en la raíz real, `verificar_a1.py`), siempre en el
sentido de negar más:

| Comando | main | rama |
|---|---|---|
| `$"git" push --force` | **pasa** | «`git push` forzado» |
| `git commit $"--no-verify" -m x` | **pasa** | «`git commit --no-verify`» |
| `git push origin $":main"` | **pasa** | «`git push` que borra la referencia remota `main`» |
| un heredoc `cat <<$"EOF"` y, detrás del `EOF`, `git push --force` (o `cat "<marzo>/v.mp4"`) | **pasa**: el delimitador quedaba como `$EOF` y lo de detrás se leía como cuerpo | niega |
| en `solo_lectura.py` (el hook de los agentes de solo lectura, que usa el mismo `tokenizar`): `$"rm" x`, `$"git" commit -m x` | pasa | «`rm` escribe», «`git commit` cambia el repositorio» (medido por el revisor) |

Son agujeros de `main` de la misma clase -operaciones prohibidas escritas con `$"…"`- y van a la
fila de `ERRORES-RECURRENTES.md` preparada en §9. No van a la matriz de ffmpeg: son de otras
reglas, cuyos tests viven en `test_guardia_claude.py`, que esta rama no toca (§2). El arreglo de
`$'…'` de §12 pasa igual por `solo_lectura.py`, y tampoco se había dicho: se declara aquí.

Un matiz de la frase de la respuesta, «nunca la convierte en otra ruta» (revisor, «lo que no pude
comprobar»): con un catálogo de mensajes (`TEXTDOMAIN`, `TEXTDOMAINDIR`) bash SÍ sustituye la
cadena por su traducción. Lo que se midió: el entorno no trae ningún `TEXTDOMAIN*`, y la guardia
niega fijarlo (`TEXTDOMAIN=… cat` y `export TEXTDOMAIN`, `R_EJECUCION` en `main` y en la rama).
Sin catálogo, el texto es el mismo, que es lo que lee la guardia.

Ni el ritual, ni los runbooks, ni las skills, ni el Makefile, ni la CI usan `$"` (`grep -rnF
'$"'`, sin resultados).
`test_el_ritual_y_los_runbooks_pasan` y `test_ninguna_denegacion_toca_el_ritual` (62 casos) y
`test_guardia_claude.py` entero, en verde.

### Punto 2: el riesgo residual, escrito

**Riesgo residual aceptado** (respuesta del consultor del 2026-10-22, punto 2): no está medido qué
hace ffmpeg con un fichero que lleva los bytes mágicos de un mp4 o un mkv y algo más dentro (no se
ejecuta ffmpeg). Lo acotan dos cosas:

1. **La lista cerrada no admite ninguna opción de demuxer.** Antes de `-i` solo van las generales
   (`-hide_banner -nostdin -nostats -y -n -v -loglevel`) y ffprobe no tiene ninguna opción de
   entrada en su lista; `-enable_drefs`, la que haría que el demuxer de MP4 siguiera referencias a
   ficheros externos, se niega. Dos casos nuevos en la matriz lo demuestran:
   `ffprobe -enable_drefs 1 -show_format <vídeo>` y `ffmpeg -enable_drefs 1 -i <vídeo> … -`, los
   dos `R_FFMPEG`.
2. **La entrada pasa `motivo_fichero` por su propia ruta** (por su texto, resuelta y sin puntos ni
   espacios finales, §1.4): un fichero de la carpeta de marzo no llega a ffmpeg, se llame como se
   llame.

**`enable_drefs` viene desactivado por defecto: verificado en la documentación de la versión de
la máquina, sin ejecutar ffmpeg.** La versión: FFmpeg 9.0.1, compilación de gyan.dev instalada con
WinGet (`C:\Users\USER\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.1-full_build\README.txt`,
línea 3: «Version: 9.0.1-full_build-www.gyan.dev»). La fuente: `doc\ffmpeg-formats.html` de esa
misma carpeta, sección «3.18 mov/mp4/3gp», «3.18.1 Options», líneas 1660-1663:
«enable_drefs — Enable loading of external tracks, disabled by default. Enabling this can
theoretically leak information in some use cases.» La versión no se leyó con `ffmpeg -version`,
que la regla niega; sale del README y del nombre de la carpeta. La de la CI de Linux es otra, y
allí no se comprobó.

### Punto 3: después

Matriz: 102 casos (20 permitidas, 82 negadas); frente a `main`, se abren 19 (las permitidas menos
la de `$"…"`, que ya pasaba) y se cierran veinte (§2). `test_guardia_ffmpeg.py` (8 pruebas; la de
los alias, solo en Windows) y `test_guardia_claude.py` enteros, en verde antes del sello.
`PROJECT_STATE.md`: 1655 funciones de test. El `make check`, el commit, el push a
`fix/guardia-ffmpeg` y el run de la CI, en el mensaje de entrega (§7); la pasada corta del revisor
sobre el diff de este commit, en §16.

## §16 · El revisor, pasada corta sobre el diff de §15

Lanzado sobre `8347e4e` (el commit de §15), solo sobre su diff (`git diff 79a560b 8347e4e`: el
arreglo de `$"…"` y su matriz). Resultado: eje (b), 8 de 8 hechos y ningún hallazgo; ninguna forma
rara de `$"…"` lee la carpeta de marzo ni escribe en la rama. Eje (a), un «importa» y un «menor».

### Lo que se hizo con los hallazgos del revisor (pasada corta)

| # | Gravedad | Qué se hizo |
|---|---|---|
| a1 | importa | Declarado: §15 dice ahora que el arreglo también cierra operaciones prohibidas escritas con `$"…"` (`push --force`, `--no-verify`, el borrado de `main`), el heredoc `<<$"EOF"` y dos casos de `solo_lectura.py`; las cuatro de la guardia, medidas también por la sesión. §4 nombra `solo_lectura.py`, que comparte `tokenizar`, también para el arreglo de `$'…'`. La fila de `ERRORES-RECURRENTES.md` preparada en §9 los lleva. No van a la matriz de ffmpeg: son de otras reglas, y `test_guardia_claude.py` no se toca en esta rama. |
| a2 | menor | Corregido: la tabla de §15 dice `$X_NO`, como el anexo. |
| — | «lo que no pude comprobar» | La CI de `8347e4e` no había terminado cuando miró: su resultado, en §7 y en el mensaje de entrega. El matiz de «nunca la convierte en otra ruta» (con `TEXTDOMAIN`): escrito en §15, y el docstring de `_comilla_de_locale` dice ya lo que se midió. |

### Informe del revisor, pasada corta (pegado tal cual)

## Informe del revisor · trabajo/guardia-ffmpeg · 2026-10-22 (pasada corta, solo `git diff 79a560b 8347e4e`)

Resumen: el arreglo de `$"…"` está bien hecho y la matriz y el §15 se sostienen. Hay un hallazgo «importa»: el arreglo cierra en `main` más huecos de los que el informe declara. Ninguno bloquea. La CI de 8347e4e no había terminado cuando miré.

### Eje (a) · Reglas de la casa
Resumen: 0 bloquea, 1 importa, 1 menor.

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| a1 | importa | **El arreglo cambia más de lo que el §15 declara.** `docs/validation/GUARDIA-FFMPEG.md:810` dice «Solo cambia lo que leía material protegido». No es así: el arreglo también cierra en `main` huecos de operaciones prohibidas, y endurece el otro hook que usa `tokenizar`, `solo_lectura.py`. Todo va en el sentido de negar más, así que es una mejora. Pero no está declarado, no está en la tabla de §15 ni en la matriz, y el §4 (línea 254) no nombra `solo_lectura.py`. Medido con `decidir` de main y de la rama (repo real, `exec` del `git show`). | `$"git" push --force`: main **pasa**, rama «`git push` forzado». `git commit $"--no-verify" -m x`: main **pasa**, rama «`git commit --no-verify`». `git push origin $":main"`: main **pasa**, rama «borra la referencia remota `main`». Un heredoc con delimitador `<<$"EOF"` seguido de `cat "<marzo>/v.mp4"` o de `git push --force`: main **pasa** (toma el delimitador como `$EOF` y esconde lo que va detrás dentro del cuerpo), rama los niega. Bash cierra el cuerpo en `EOF`: `bash -c 'cat <<$"EOF"⏎hola⏎EOF⏎echo FUERA_DEL_CUERPO'` imprime `hola` y `FUERA_DEL_CUERPO`. En `solo_lectura.motivo`, `$"rm" x` y `$"git" commit -m x` dan `None` en main y «`rm` escribe» / «`git commit` cambia el repositorio» en HEAD. Son agujeros de `main` de la misma clase que la fila de ERRORES-RECURRENTES preparada en §9. Faltan en esa fila y en la tabla de §15. |
| a2 | menor | La tabla de §15 y su anexo no muestran el mismo comando. | `GUARDIA-FFMPEG.md:806` dice `` `cat $"$X/v.mp4"` ``; `anexos/GUARDIA-FFMPEG/locale-medida.txt:9` dice `` `cat $"$X_NO/v.mp4"` ``. |

Comprobado sin hallazgos:
- **El cambio en `guardia.py` es solo el declarado:** la función `_comilla_de_locale` (`texto.startswith('$"', i)`, la condición con nombre) y tres líneas en `tokenizar` (`guardia.py:805-807`). Va después de la rama de `$'…'` y antes de la de `"`.
- **Solo afecta a Bash:** `tokenizar` solo se llama desde `analizar_bash` (`guardia.py:1082`), así que PowerShell no cambia.
- **Formas raras que no están en la matriz** (main → rama):
  - Pasaban en main y ahora `R_SIN_ABRIR`: pegada delante (`cat corp$"us/…"`), dos trozos `$"…"$"…"`, `$"…"` seguido de `'…'`, dentro de `$(...)` y de acentos graves, `bash -c '…'`, `sh -c 'head …'`, heredoc con comillas a `bash`, `cat < $"…"`, `$"cat" $"…"`, `dd if=$"…"`, `cd $"…" && cat v.mp4`, `cd … && ffmpeg …`, `cp $"…" /tmp`.
  - `find $"<carpeta>" -exec cat {} +`: main pasa, rama `R_CAPTURA`.
  - `ffprobe $"file:…"` y `ffprobe file:$"…"`: main pasa, rama `R_FFMPEG`.
  - `python $"…"`: main `R_EJECUCION`, rama `R_SIN_ABRIR`.
  - Ya negadas igual en las dos (`R_EJECUCION`): heredoc sin comillas a `bash`, asignación y `cat "$X"` (con `;`, `&&`, `export` y como prefijo de entorno), `while read … < $"…"`, `source`, `xargs cat`, `TEXTDOMAIN=… cat` y `export TEXTDOMAIN`. `grep -r x $"<material>"` da `R_CAPTURA` en las dos.
  - Pasan en las dos y no leen nada: `$$"…"`, `\$"…"`, `"$"…""` y `'$"…"'`. Bash los convierte en el PID o en `$` delante de la ruta, o en un literal, y esa ruta no existe. El tokenizador da lo mismo que bash: `['\x00V$\x00p']`, `['$p']`, `['a$b']`, `['$"p"']`.
  - El heredoc que solo lleva datos pasa en las dos (es texto, no se lee ningún fichero).
  - Ninguna forma probada lee la carpeta de marzo ni escribe en la rama.
- **Lo legítimo sigue pasando:** `echo $"hola"`, `git log --format=$"%h %s" -1` y `ls $"<carpeta de marzo>"` (listar), en main y en la rama.
- **Ritual y tests:** ni `docs/runbooks`, ni `.claude/skills`, ni `Makefile`, ni `.github` usan `$"` (`grep -rnF`, vacío). `pytest tests/unit/test_guardia_ffmpeg.py` más `test_el_ritual_y_los_runbooks_pasan` y `test_ninguna_denegacion_toca_el_ritual`: `70 passed`, exit 0 (8 + 62).
- **`make-check.log`:** `2742 passed`. `SELLO … 9140f35f66f2028ab385a3e883894ce05edbf382`, que coincide con `git rev-parse 8347e4e^{tree}`. `PICO DE MEMORIA … 297 MiB`.
- **PROJECT_STATE.md:** pasa de 1654 a 1655 funciones de test, +1, que es el test nuevo.
- **Copias de la respuesta del consultor:** la del §14 y la del final del encargo son idénticas (`diff` de sus líneas `>`: IGUALES).
- `git status --short` sigue vacío al terminar.

### Eje (b) · Encargo (segunda respuesta del consultor)
Resumen: 0 bloquea, 0 importa, 0 menor. Requisitos: 8 hechos, 0 parciales, 0 no hechos.

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 1 | `$"…"` se lee como `"…"`, con la condición nombrada | Hecho | `guardia.py:654-659, 805-807`; `tokenizar('cat $"a b"')` da `['cat','a b']` (main: `'$a b'`) |
| 2 | Los cinco casos sobre la carpeta de marzo (cat, head, grep, ffprobe, cd) en la matriz | Hecho | `test_guardia_ffmpeg.py`, `NEGADAS` con «locale:»; `LOCALE_EN_MARZO` tiene los 5, todos `R_SIN_ABRIR` (anexo A.1) |
| 3 | Un `$"…"` legítimo que pasa | Hecho | `PERMITIDAS`, «comilla de locale, el video»: pasa / pasa |
| 4 | Roto a propósito en los dos sentidos | Hecho | `test_sin_el_arreglo_de_la_comilla_de_locale_los_cinco_pasan`: sin el arreglo, cat/head/grep pasan y ffprobe/cd dan `R_FFMPEG` por «no se puede leer»; sin además los bytes mágicos, pasan los 5. Con el arreglo se niegan (la matriz). En verde |
| 5 | En la tabla de comparación con main | Hecho | Anexo A.3: los 5 «main pasa \| rama R_SIN_ABRIR»; §2, «veinte» (9+6+5). Recuento: 20 permitidas, 82 negadas, 102 en total (medido importando el módulo) |
| 6 | Los dos tests del ritual en verde | Hecho | 70 passed (arriba) |
| 7 | El riesgo residual escrito y acotado: ninguna opción de demuxer y `-enable_drefs` negado; la entrada pasa `motivo_fichero` | Hecho | §15 punto 2. Dos casos `R_FFMPEG` en la matriz. Listas cerradas en `guardia.py:2965-2988`: ninguna opción de demuxer |
| 8 | `enable_drefs` desactivado por defecto, con la versión y la fuente | Hecho, verificado | `README.txt`, línea 3: «Version: 9.0.1-full_build-www.gyan.dev». `doc\ffmpeg-formats.html`, líneas 1649 («3.18 mov/mp4/3gp»), 1656 («3.18.1 Options») y 1660-1662: «enable_drefs … Enable loading of external tracks, disabled by default. Enabling this can theoretically leak information in some use cases.» `which ffmpeg ffprobe` apunta a `…/WinGet/Links/`, la misma instalación. `use_absolute_path` (línea 1665) también viene desactivado y tampoco está en la lista |

Sin hallazgos en este eje. La rama no toca nada fuera de lo que la respuesta pide, salo lo de a1, que ya va en el eje (a).

### Lo que no pude comprobar
- **La CI de Linux de 8347e4e:** run 39880288314, `headSha` 8347e4e…, `status: in_progress`, sin conclusión en las dos consultas que hice. No había terminado.
- **La frase «nunca la convierte en otra ruta»** (del consultor, copiada en el docstring y en §1.8). Si hay un catálogo de mensajes (`TEXTDOMAIN`/`TEXTDOMAINDIR`), bash sustituye la cadena por su traducción, y no tengo manual local de bash para citarlo. Montar un catálogo para probarlo escribe, así que no lo hice. Lo que sí medí: `env` no trae ningún `TEXTDOMAIN*`; `bash -c 'echo $"hola" ${TEXTDOMAIN-sin_TEXTDOMAIN}'` da `hola sin_TEXTDOMAIN`; y la guardia niega fijarlo (`TEXTDOMAIN=… cat`, `export TEXTDOMAIN`: `R_EJECUCION` en main y en la rama).
- No ejecuté ffmpeg ni ffprobe, como se pidió.

### Comandos ejecutados
1. `git log --format='%h %s' -3 && git diff --stat 79a560b 8347e4e && git status --short`
2. `git diff 79a560b 8347e4e -- .claude/hooks/guardia.py tests/unit/test_guardia_ffmpeg.py PROJECT_STATE.md docs/encargos/trabajo-guardia-ffmpeg.md`
3. `git diff 79a560b 8347e4e -- docs/validation/` (leído del fichero de salida)
4. Read de `guardia.py:600-899` y `1070-1094`; Grep de `tokenizar(`
5. `sed -n 1,80p .claude/hooks/solo_lectura.py`
6. `uv run python -c` (sin registrar en `sys.modules`; falló, AttributeError de dataclass)
7. `uv run python -c` con el tokenizador de la rama y el de main sobre formas raras
8. `uv run python -c` con `decidir` de main y de la rama sobre 38 comandos
9. `grep -rnF '$"' docs/runbooks .claude/skills Makefile .github scripts/*.sh`
10. `uv run pytest -q -p no:cacheprovider tests/unit/test_guardia_ffmpeg.py …::test_el_ritual_y_los_runbooks_pasan …::test_ninguna_denegacion_toca_el_ritual` (dos veces; la segunda, sin `-q`: 70 passed, exit 0)
11. `uv run python -c "…import test_guardia_ffmpeg…"` (recuento 20/82/102) y `git status --short`
12. `grep -n "comilla de locale" …/salidas-pytest.txt` y recuentos del anexo
13. `ls`, `sed -n 1,6p README.txt` y `grep -n enable_drefs doc/ffmpeg-formats.html`; Read de `ffmpeg-formats.html:1649-1668`
14. `which ffmpeg ffprobe`; `grep -n` de las listas de opciones; Read de `guardia.py:2965-2989`
15. `gh run list --branch fix/guardia-ffmpeg --limit 1`, después `gh run view 39880288314` y dos veces `gh run view 39880288314 --json headSha,status,conclusion`
16. `grep -n "SELLO\|PICO DE MEMORIA\|passed\|failed" make-check.log`, `git rev-parse 8347e4e^{tree}`, `ls -la make-check.log`
17. `diff` de las líneas `>` del encargo y del §14
18. `env | grep TEXTDOMAIN` con `bash -c 'echo $"hola" …'` en el mismo comando: la guardia lo negó («antes, en el mismo comando, va `env`»). Seguí su forma y los partí en dos llamadas: `env | grep -c "^TEXTDOMAIN"` y `bash -c 'echo $"hola" ${TEXTDOMAIN-sin_TEXTDOMAIN}'`
19. `uv run python -c` con `solo_lectura.motivo` de main y de HEAD (cada uno con su guardia, cargados por `exec` del `git show`)
20. `uv run python -c` con `decidir` sobre `$"git" push --force`, `git commit $"--no-verify"`, `git push origin $":main"` y otros
21. `bash -c 'cat <<$"EOF"⏎hola⏎EOF⏎echo FUERA_DEL_CUERPO'`
22. `uv run python -c` con `decidir` sobre el heredoc `<<$"EOF"` seguido de `cat "<marzo>"` y de `git push --force`
23. `git ls-files | grep medir_…` y `grep -n` en `GUARDIA-FFMPEG.md`

Ficheros relevantes: `C:\Users\USER\Desktop\Bot v3\.claude\hooks\guardia.py`, `C:\Users\USER\Desktop\Bot v3\.claude\hooks\solo_lectura.py`, `C:\Users\USER\Desktop\Bot v3\tests\unit\test_guardia_ffmpeg.py`, `C:\Users\USER\Desktop\Bot v3\docs\validation\GUARDIA-FFMPEG.md`, `C:\Users\USER\Desktop\Bot v3\docs\validation\anexos\GUARDIA-FFMPEG\locale-medida.txt`, `C:\Users\USER\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.1-full_build\doc\ffmpeg-formats.html`.

Este informe va al §16 de la rama; no lo pego yo, lo devuelvo.

## §A · Anexo (`docs/validation/anexos/GUARDIA-FFMPEG/`)

- `fase0-main.txt`: la tabla de §0.1, con la guardia de `main` (`git show main:`), regenerada con
  los vídeos binarios (las decisiones, las mismas que con los de texto).
- `fase0-rama.txt`: los mismos diez casos con la guardia de la rama, regenerado tras §12: pasan
  los de las formas permitidas salvo la extracción DENTRO del repo (`R_FFMPEG`, «la salida
  `audio.wav` esta dentro del repositorio»); marzo sigue negado con `R_SIN_ABRIR`; el que no
  existe, que pasaba en `3372f7a`, se niega ahora (`R_FFMPEG`, no se puede leer).
- `salidas-pytest.txt`: `uv run pytest -q -s tests/unit/test_guardia_ffmpeg.py`, en Windows, sobre
  el commit de §15, las 8 pruebas en verde. Contiene:
  - §A.1, la matriz entera (`| caso | comando | obtenido | esperado |`);
  - §A.2, las cuatro roturas a propósito (`sin la regla | …`, `con una opcion de mas | …`,
    `sin los bytes magicos | …`, `sin el arreglo de $'...' | …` y `sin el arreglo de $"..." | …`,
    cada una con su `y sin los bytes magicos | …`) y el nombre corto de la raíz del test de los
    alias;
  - §A.3, la comparación con `main` caso a caso (`| caso | main X | rama Y |`).
- `respuesta-consultor-medida.txt`: las tablas de §12, con `decidir` de `main`, de `3372f7a` y de
  la rama nueva (`medir_respuesta.py`).
- `locale-medida.txt`: la tabla de §15, con `decidir` de `main` y de la rama (`medir_locale.py`).

## Estado

TERMINADA, pendiente de la revisión del consultor: las cuatro formas de ffprobe y ffmpeg pasan,
todo lo demás se niega. Los hallazgos de la primera pasada del revisor (§10) y los dos de la
revisión del consultor (§11) están arreglados, cada uno con sus casos en la matriz y roto a
propósito en los dos sentidos (§12). La segunda pasada del revisor (§13) no encuentra nada en el
encargo y un «importa» heredado de `main`, la comilla `$"…"`; el consultor mandó cerrarla aquí
(§14) y está cerrada, con su matriz y roto a propósito (§15), y el riesgo residual de los bytes
mágicos, escrito y acotado (§15). La pasada corta del revisor sobre ese diff (§16) no encuentra
nada en el encargo; su «importa» -el arreglo cierra en `main` más de lo declarado, siempre
negando más- y su «menor» están declarados y corregidos. Queda para la orden de cierre.

Rama lista para revisión, NO cerrada.
