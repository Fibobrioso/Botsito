# GUARDIA-ENLACES · La guardia protege el material por lo que es, no solo por donde esta (G.8)

> PLANTILLA hasta la fase 0 (la línea con que nació): ya no lo es.

Rama `trabajo/guardia-enlaces`, abierta el 2026-11-20 (18:27, reloj de la laptop en Lima, UTC-5)
desde `main` en 0562a77b (commit de estado sobre el merge fb1f02e9 del tag
`stable/F39h-guardias-holdout`). Encargo: `docs/encargos/trabajo-guardia-enlaces.md`. Tramo:
«Carril: guardias y deuda» (entrada G.8 de la hoja de ruta). Tag previsto:
`stable/F39i-guardia-enlaces`. Riesgo: **alto**, como manda el encargo.

La PARADA es condicional (encargo): las decisiones D1 a D4 vinieron por adelantado. Seguí con lo que
cuadraba con lo medido; lo que no cuadra, o lo que el encargo no decide, está en la PARADA final
(§8).

## 0. Apertura: la base comprobada

- `git rev-parse main origin/main`: dos veces `0562a77ba0e58da25904801640c98f4287bd6a95`.
- `git rev-parse "stable/F39h-guardias-holdout^{commit}"` = `fb1f02e9712e63fcb4e75fd53cf3ac5a5eadd9ec`
  = `main^1`; en origin, `git ls-remote --tags origin stable/F39h-guardias-holdout` da
  `5050047e… refs/tags/stable/F39h-guardias-holdout` (tag anotado).
- CI de `main` sobre 0562a77b (check-runs con el sha literal): `python completed success`, run
  44821324976.
- `git branch --list` solo daba `main`; `git ls-remote --heads origin "fix/*"`, vacío.
- Primer commit, 0333a957, con el sello de `make check` (3561 passed, 6 xfailed; `CONTRATO:` y `G2:`
  en verde).

## 1. Fase 0

### 1.1 Herencias (0.1)

Buscado en `PROJECT_STATE.md` (Technical Debt), `docs/state/HISTORIA.md`, la hoja de ruta (G.1 y
G.8) y `GUARDIA-ALIAS.md` lo que nombra enlaces, `realpath`, copias fuera del repo o clones
desechables. El auditor (§1.3) señaló los mismos sitios.

| Herencia | Dónde | ¿Entra? |
|---|---|---|
| El hueco mismo: con `corpus/` como unión, la ruta canónica sale de la raíz y no se miran las reglas del material; la carpeta `Backtest <mes>` no se niega | hoja de ruta, G.8 (`HOJA-DE-RUTA.md:828-835`); `GUARDIAS-HOLDOUT.md` §17 | **Entra**: es la rama. La segunda mitad de su «Hecho cuando» («Aleks repite el traslado con la guardia simulada denegando las cuatro») no la hace la sesión: PARADA, punto 6 |
| De dónde viene: la respuesta a la PARADA 1 de `trabajo/guardia-alias` (punto 1) eligió `realpath`, que resuelve uniones y enlaces, y el test que pidió fue un enlace DENTRO del repo hacia lo protegido (`test_leer_por_una_union_o_un_enlace_hacia_lo_protegido_se_niega`) | `GUARDIA-ALIAS.md:381`, `:455` | **Entra** como causa: nadie midió un enlace de dentro hacia FUERA ni una copia fuera. Ese test sigue en verde (§3) |
| Si `realpath` lanza `OSError`, se compara la forma sin prefijos | PROJECT_STATE, Technical Debt («Riesgos residuales del alias de la raíz») | **No entra**: es D3 (lo que no se puede canonizar sigue negado, igual que hoy); no cambia |
| La excepción de la carga por ruta vale para cualquier fichero que acabe en `.claude/hooks/guardia.py`, también fuera del repo | PROJECT_STATE; HISTORIA.md:14627 | **No entra**: familia 3 (ejecución verificable), fuera del encargo |
| El test de un clon de comparar-con-main cuenta como test del repo | HISTORIA.md:14623 | **No entra**: familia 3. La rama lo usa (§4) |
| Riesgo residual de ADR-0088: `git status --untracked-files=all` y `fd` sacan nombres de dentro del holdout | HISTORIA.md:14628 | **No entra**: ni enlaces ni copias; sigue en su sitio |
| Read de crudas de un vídeo sin cuarentena ni tramos; Read del PNG de un fotograma en un tramo no citable | PROJECT_STATE, Technical Debt (VIDEO-JULIO.md §10.8 y §11.1) | **No entra**: familia 1, pero no son rutas fuera de la raíz; otra rama del carril |
| `test_guardia_falsos_positivos` falla a veces por el nombre aleatorio de una carpeta temporal | PROJECT_STATE, Technical Debt | Se vigiló en D4 (§1.4): no salió en ninguna corrida de la rama |
| La CI de Linux se cuelga a veces instalando ffmpeg | PROJECT_STATE, Technical Debt; RITUAL.md | Se vigila en §5 |
| G.1 (las formas raras, D; lo que queda de `trabajo/guardia-g1`) | `HOJA-DE-RUTA.md:734` | **No entra**: ni enlaces ni copias |

### 1.2 La decisión de hoy por clase y forma (0.2)

**Cómo se midió** (Windows 11, Python 3.12 del sistema, la guardia de `main` = la del árbol en ese
momento). Un test TEMPORAL en `tests/unit/` (la guardia no lee `tests/`), corrido una vez con la
guardia de `main` y otra con la de la rama, y sacado de `tests/` antes del commit; queda como anexo
con sus salidas (`anexos/GUARDIA-ENLACES/medir_enlaces.py`, `medida-main-SALIDA.txt`,
`medida-rama-SALIDA.txt`, resumidas en `tabla-main.md` y `tabla-rama.md` por `resumir.py`).
Precedente: `anexos/GUARDIA-FALSOS-POSITIVOS/medida_parada2.py`. Dos partes, y ninguna lee
contenido protegido:

1. **En memoria**, con `decidir` (lo que llama `main()`), sobre un repo INVENTADO en `tmp_path` con
   la estructura del real y ficheros falsos en cada clase de la familia 1 (las del encargo y las
   tres que el auditor añadió: el feedback que etiqueta un reservado, `data/visor/` con su id y la
   lista de ficheros con ocultos), en las formas del encargo: (a) dentro; (b) por un enlace de
   dentro hacia fuera, simulado con `_realpath` CON la estructura detrás (`corpus/`, `knowledge/` y
   `data/` a otro disco) y SIN ella (`holdout/1`, `Backtest marzo 2026`, `Material…`, `Sesiones` y
   `data/transcripciones` a nombres sin anclaje), y con dos uniones REALES (`mklink /J`, sin
   administrador): `corpus/` a otra carpeta con la estructura, y `holdout/1` y `Backtest marzo
   2026` a carpetas sin ella; (c) una copia con la misma estructura fuera, y un clon (`…/clon/Bot
   v3/…`); (d) la carpeta en sí. Por herramienta: Read, Grep, Glob, `cat`, `Get-Content` y, para
   las carpetas, `ls`, `Get-ChildItem` y `grep -r`.
2. **Por stdin** (`python .claude/hooks/guardia.py` con el JSON de PreToolUse simulado) con la
   raíz REAL: holdout (la sonda `caso-eurusd-2000-01-01.yaml`), el libro de marzo por su nombre,
   una imagen y un fichero INVENTADOS de `Backtest marzo 2026`, una hoja inventada de `Sesiones/` y
   la cruda de v7, en las formas (a), (c) y (d), y las mismas rutas bajo `D:\BotsitoCorpus` (solo la
   decisión; los `ls`, `grep -r` y `Get-ChildItem` de D: ni simulados). Nada de D: se abrió ni se
   listó desde la sesión.

**Lo que decide `main`** (Read como representante de los lectores de contenido; Grep, `cat` y
`Get-Content` deciden igual en todas las filas de ficheros; «N» negada, «P» permitida):

| Clase | (a) dentro | (b) sim., con estructura | (b) sim., sin estructura | (b) unión real de `corpus/` | (b) unión real sin estructura | (c) copia fuera | (c) clon fuera | D:\BotsitoCorpus (stdin) |
|---|---|---|---|---|---|---|---|---|
| `holdout/1` | N | **P** | **P** | N | **P** | **P** | **P** | — |
| `holdout/2`, `holdout/3` | N | **P** | N | N | N | **P** | **P** | — |
| libro por su nombre (`backtesting-analytics MARZO 2026.xlsx`) | N | N | N | N | N | N | N | N |
| libro de un mes reservado por la regla del material (`resumen mayo 2026.xlsx`) | N | **P** | **P** | **P** | N | **P** | **P** | — |
| imagen del material adicional | N | **P** | **P** | **P** | N | **P** | **P** | — |
| imagen de `Backtest marzo 2026` | N | **P** | **P** | **P** | **P** | **P** | **P** | **P** |
| otro fichero de `Backtest marzo 2026` | N | **P** | **P** | **P** | **P** | **P** | **P** | **P** |
| hoja de `Sesiones/` | N | **P** | **P** | **P** | N | **P** | **P** | **P** |
| cruda en cuarentena (v7) | N | **P** | **P** | N | N | **P** | **P** | — |
| `*cruda-NO-LEER*` | N | N | N | N | N | N | N | — |
| tramo no citable (v6) | N | **P** | **P** | N | N | **P** | **P** | — |
| id de caso reservado en `knowledge/cases/` y en `data/visor/` | N | **P** | N | N | N | **P** | **P** | — |
| feedback que etiqueta un reservado | N | **P** | N | N | N | **P** | **P** | — |
| fichero de la lista con ocultos | N | **P** | N | N | N | **P** | **P** | — |

(«(b) unión real de `corpus/`» solo enlaza `corpus/`: por eso lo de `knowledge/` y `data/` sigue
negado ahí. Por stdin, la forma (a) dio lo mismo que en memoria en sus cinco clases, y la (c),
también «P» salvo el libro por su nombre.)

**Las carpetas (d)** en `main`:

| Carpeta | Read | Grep | Glob (`*`) | `ls` | `Get-ChildItem` | `grep -r` |
|---|---|---|---|---|---|---|
| `Backtest marzo 2026`, dentro (con su imagen; por stdin, la real) | **P** | N | **P** | P | P | N |
| `Backtest marzo 2026`, copia fuera, unión real o D: | **P** | **P** | **P** | P | P | **P** |
| `holdout/1`, dentro | P | N (con un caso; la real, solo con su README: P) | N | N | N | N (la real: P) |
| `holdout/1`, copia o clon fuera | P | **P** | **P** | **P** | **P** | **P** |
| `Sesiones/` y la carpeta de la cruda v7, dentro | P | N | P | P | P | N |
| las mismas, copia fuera | P | **P** | P | P | P | **P** |
| la carpeta que CONTIENE una copia (sin anclaje en su ruta) | P | **P** | P | P | P | **P** |
| una carpeta temporal cualquiera, y un fichero suyo | P | P | P | P | P | P |

D2, medido: hoy `ls`, `dir` y `Get-ChildItem` sobre la carpeta `Backtest <mes>` **pasan** (listan
nombres: `LECTOR_DE_METADATOS`, `guardia.py:1076`; `Get-ChildItem` es de metadatos). Se quedan así.
Un Glob de un fichero NOMBRADO, sin comodín, pasa en todas las formas (lista un nombre que ya está
en el patrón): no es un lector.

**Lo que cambia con la rama** (`comparacion-caso-a-caso.txt`, por `comparar.py`): de 868 decisiones,
**0 pasan de negada a permitida**, 315 pasan de permitida a negada, 551 quedan iguales y 2 siguen
negadas con otra regla (el Grep y el `grep -r` de la carpeta real `Backtest marzo 2026`: antes
`R_CAPTURA` por su primera imagen, ahora `R_SIN_ABRIR` por la carpeta misma, D2). Tras la rama,
todas las celdas en negrita de las tablas de arriba son «N», salvo:

- las clases que D1 no ancla (tramo de v6, caso reservado en `cases/` y `visor/`, feedback y la
  lista con ocultos) en una COPIA o un CLON fuera: siguen «P» (PARADA, punto 1). Por un enlace de
  dentro (b), sí se niegan: las decide la forma textual;
- en (b) simulado con estructura, el feedback y el Grep de las carpetas `holdout/1`, `Sesiones/` y
  la cruda v7 siguen «P»: es la simulación, no la regla (el destino simulado no existe en disco y
  no hay contenido que leer ni ficheros que recorrer); con la unión REAL, se niegan;
- el Read de una carpeta que no es `Backtest <mes>` (`holdout/1`, `Sesiones/`, la cruda v7), en
  cualquier forma: «P», como dentro del repo en `main` (un Read de una carpeta no lee nada; D2 solo
  habla de `Backtest <mes>`);
- `ls`, `Get-ChildItem` y Glob de `Sesiones/` y de la cruda v7: listan nombres, como dentro.

### 1.3 El auditor (0.3)

El subagente `auditor-encargo` comprobó 29 afirmaciones del encargo: 17 correctas, 0 falsas, 12 con
matiz, y 14 cosas que el repo pide y el encargo no dice. Los matices que cambian algo:

| # | Matiz | Qué se hizo |
|---|---|---|
| 8 | La clase es `Politica`, no `Guardia`; `relativa` hace lo que dice el encargo (`guardia.py:544-551`) | nada que cambiar |
| 6 | La imagen de §17 era INVENTADA, por la ruta del repo con el enlace puesto | la medida usa también imágenes inventadas |
| 13, 18 | D1 no ancla todas las clases de la familia 1: tramos de v6, R_CASO en `cases/`, `visor/` y `feedback/`, propuestas y la lista con ocultos | medido (§1.2) y a la PARADA, punto 1 |
| 19 | Negar Glob sobre la carpeta (D2) y dejar `ls` choca con ADR-0021 §1 («listar nombres no es abrir») y con ADR-0088, que hizo falta para negar los nombres del holdout; `docs/adr/` no cambia en esta rama | hecho como decide D2 y a la PARADA, punto 2 |
| 21 | Más sitios devuelven None fuera de la raíz: `lista_dentro_del_holdout`, `motivo_dentro_de_zona`, `lineas_de_tramo`, `_patron_lista_el_holdout` | los cuatro deciden por todas las formas (§2) |
| 22 | El Grep sobre la carpeta `Backtest` ya lo negaba `main` dentro del repo si tenía algún fichero | el test usa también una carpeta VACÍA (`Backtest junio 2026`) y las formas b y c |
| 24 | Los mutantes «como en GUARDIAS-HOLDOUT» editarían el hook que está corriendo, y la guardia de la sesión quedaría más débil mientras estén puestos; el precedente de la guardia es `_romper` dentro del test | a mano, pero en el clon desechable de la rama, no en el hook vivo (§4.2) |
| 26 | El comando del push a `fix/` está en `RITUAL.md:103` (las líneas 101-102 lo explican) | §5 |
| 29 | `test_cuarentena_por_condicion.py` también carga `guardia.py` | se corrió con los de la guardia (§3) |
| falta 1 | El «Hecho cuando» de G.8 pide que Aleks repita el traslado | PARADA, punto 6 |
| falta 9 | El temporal de pytest lleva `AppData\`, que casó con `data\` como subcadena en `trabajo/guardia-falsos-positivos` | los anclajes se comparan por TRAMOS enteros (`por_estructura`), no como subcadena; test `test_fuera_sin_ningun_anclaje_pasa` |
| falta 10 | Un clon lleva los tres README de `holdout/{1,2,3}`, que se leen | la exención se cuenta desde el anclaje; test `test_el_readme_de_una_particion_de_la_copia_se_sigue_leyendo` |
| falta 11 | CLAUDE.md, párrafo de marzo: «la de Claude Code bloquea su carpeta Backtest marzo 2026» no era del todo cierto | con D2 ya lo es; la línea «Guardia:» nueva lo dice (§3) |

### 1.4 Falsos positivos (D4)

- **Las lecturas legítimas de la medida** (un fichero cualquiera de una carpeta temporal, la
  carpeta misma, `ls` y Glob de ella): «P» antes y después.
- **La carpeta de trabajo de la sesión**: un Grep sobre ella con el hook vivo de la rama pasa
  (medido en la sesión; no tiene anclajes en sus rutas).
- **Los tests de la guardia que montan árboles falsos con su propia raíz**: en la primera corrida
  con la rama fallaron 12, en dos grupos. Ninguno es una lectura legítima negada:
  1. **4 de `test_guardia_ffmpeg.py`**: sus repos inventados no tienen `knowledge/corpus/fuentes.yaml`,
     y la lectura por estructura lo pedía siempre para el anclaje de las transcripciones. Arreglado
     en la guardia: `fuentes.yaml` solo se lee si la ruta lleva `data/transcripciones/` (los
     anclajes fijos, en `Politica.ANCLAJES`). Los tests, sin tocar.
  2. **8 de `test_roto_a_proposito` en `test_guardia_alias.py`**: cada uno rompe una pieza del alias
     de la raíz (`_canonica`, el contenedor, la segunda lectura de la herramienta, `/proc/cygdrive`,
     la unidad sin barra, `_sin_disfraz_posix`) y exige que sus tests FALLEN. Ya no fallan, porque
     las rutas de esos tests llevan el anclaje de su clase y la estructura o la forma textual las
     niegan igual: la guardia tiene ahora dos capas donde había una. **Esto contradice lo que D4
     daba por hecho («no cambian de resultado»)**. Lo que hice: en `test_roto_a_proposito` se apagan
     las tres capas nuevas -la forma textual, la estructura y el recorrido de una carpeta de fuera-
     con cuatro parches (`_textual`, `_sin_resolver`, `Politica.por_estructura` y
     `Politica.lo_que_alcanza_fuera`) antes de romper la pieza, para que cada pieza del alias se
     mida SOLA, como en `main`; las capas nuevas las sostiene `test_guardia_enlaces.py`. Es el único
     test existente que cambia. A la PARADA, punto 3, por si el consultor prefiere otra cosa.
- Tras los dos arreglos, todos los tests de la guardia en verde (§3).

## 2. Lo hecho (fase 1): D1 y D2 en `.claude/hooks/guardia.py`

Todo en la familia 1; las demás familias (operaciones prohibidas, ejecución verificable, ffmpeg, CI,
Monitor) no se tocan. Las funciones que deciden sobre una ruta siguen recibiendo la canónica; lo
nuevo es que esa canónica RECUERDA su forma textual.

- **`RutaCanonica`** (subclase de `str`) y **`_absoluta`**: `_absoluta` devuelve la canónica de
  siempre (mismo cálculo, mismo resultado) con un atributo `textual`: la ruta absoluta sin prefijos,
  sin puntos ni espacios finales y normalizada, pero SIN `realpath` (`_sin_resolver`). Una relativa
  cuelga del directorio de trabajo TEXTUAL. Por qué así: `_absoluta` es la puerta de todas las
  herramientas (`GUARDIA-ALIAS.md` §1); cambiar las ~40 llamadas para pasar dos rutas tocaba mucho
  más. Lo que se calcula de una `RutaCanonica` con `os.path` es un `str` sin forma textual, y
  entonces deciden la canónica y la estructura.
- **`Politica.relativas(ruta)`** (D1): todas las formas relativas a la raíz -la canónica, la textual
  y, de cada una que caiga fuera, su lectura por estructura-; se niega si cualquiera niega.
  **`Politica.por_estructura(ruta)`**: una ruta de fuera que contiene, en cualquier TRAMO (no como
  subcadena) y comparada como siempre (`_normcase`), un anclaje, se lee como si el anclaje
  estuviera en la raíz. Anclajes: `estrategia del trader/material adicional de su operativa` y
  `estrategia del trader/sesiones` (sin `corpus/` delante), `knowledge/cases/holdout/{1,2,3}` y
  `data/transcripciones/<vídeo en cuarentena>`. `relativa` no cambia (la usan las familias 3 y
  ffmpeg para saber si algo está DENTRO del repo).
- **`motivo_fichero`**: el nombre (`cruda-no-leer`, el libro por su nombre) en la canónica y en la
  textual, y las reglas de cada sitio (`_motivo_en_el_sitio`, el cuerpo de antes) en cada forma.
  **`lineas_de_tramo`** toma la forma que está en `data/transcripciones/`.
- **`motivo_directorio`**: D2 primero; un ancestro de la raíz, como siempre; luego cada forma
  (`_motivo_directorio_en`, el cuerpo de antes, bajando a la zona desde la carpeta misma); y una
  carpeta de fuera SIN anclaje en su ruta, lo que alcanzaría, fichero a fichero
  (`lo_que_alcanza_fuera`; PARADA, punto 4). **`_primer_protegido`** recibe la forma relativa de la
  carpeta y, si no es la canónica (una carpeta que es un enlace de dentro hacia fuera), decide cada
  fichero también por ella: la medida «después» encontró que sin esto el Grep de una `holdout/1`
  enlazada de verdad pasaba.
- **`motivo_dentro_de_zona`** y **`lista_dentro_del_holdout`** (ADR-0088): por todas las formas; la
  segunda, además, en recursivo, una carpeta de fuera sin anclaje que tiene debajo una copia de
  `holdout/{1,2,3}` (`holdout_debajo`). **`_patron_lista_el_holdout`** y
  **`_candidatos_del_holdout`**: el patrón en su forma canónica y en la textual, y los candidatos
  de la copia (la carpeta del holdout que contiene la base, o las que tiene debajo). En Glob, el
  patrón cuelga también de la base textual.
- **D2**: `_motivo_backtest` -la carpeta `Backtest <mes>` de un mes no legible, ella misma y todo
  lo de dentro- lo usan `_motivo_material` (Read y todos los lectores), `motivo_directorio` (Grep y
  los lectores recursivos) y, en la primera vuelta, Glob (`motivo_carpeta_backtest` sobre la base y
  la parte literal del patrón, `_parte_literal`); **Glob salió** con la respuesta del consultor a la
  PARADA final, punto 2 (§10). Lo de dentro, como siempre (cualquier carpeta `backtest*`); la carpeta
  misma, solo con `backtest` como palabra: la medida «después» encontró que con `startswith` un
  libro SUELTO `backtesting-analytics …` caía también, y su Glob no debe negarse (leerlo lo niega su
  propia regla). `ls`, `dir` y `Get-ChildItem` no pasan por estas funciones: siguen como estaban.
- **D3**: sin cambios; `_sin_resolver` se calcula después de `_canonica`, que ya habría negado lo no
  canonizable.
- **Tras el revisor** (§9, B1 y B3): `_nombres_largos` expande en la forma textual los tramos 8.3
  (`KNOWLE~1`) con `GetLongPathNameW`, que cambia el nombre de cada tramo y no sigue uniones (solo
  en Windows y solo si la ruta lleva `~`); y los recorridos de una carpeta de fuera
  (`lo_que_alcanza_fuera` y `holdout_debajo`) tienen tope, `LIMITE_DEL_RECORRIDO` = 20.000
  entradas: pasado el tope se niega (`R_RECORRIDO`, o el listado del holdout) en vez de arriesgar
  el plazo de 30 s del hook (`.claude/settings.json`). Y un ANCESTRO de la raíz vuelve a decidirse
  sin recorrerlo, como en `main` (`_candidatos_del_holdout` no mira fuera si la base contiene la
  raíz): el revisor midió 11,3 s para un Glob `**/*.yaml` desde el Escritorio, que `main` negaba al
  instante.

## 3. Tests (fases 2 y 3)

(Tras la respuesta del consultor, §10: 23 tests; la carpeta Backtest, solo Read y Grep; y uno por
cada clase anclada en el punto 1. La tabla de abajo es la de la primera vuelta.)

`tests/unit/test_guardia_enlaces.py`, nuevo, 17 tests EN MEMORIA sobre repos y copias inventados
(rutas a trozos, como `test_guardia_alias.py`): los 14 de la primera vuelta y, tras el revisor,
`test_un_enlace_escrito_con_un_tramo_83_se_niega` (B1; solo Windows; con `_nombres_largos`
apagado en un test TEMPORAL, borrado antes del commit, falla: «Read … OTV3C~1\KNOWLE~1\cases\holdout\1\caso-eurusd-2026-05-04.yaml:
pasa (se esperaba R_HOLDOUT)»), `test_el_recorrido_de_una_carpeta_de_fuera_tiene_tope` y
`test_un_ancestro_de_la_raiz_se_decide_sin_recorrerlo_fuera` (B3):

| Test | Lo que pide el encargo |
|---|---|
| `test_la_imagen_de_backtest_marzo_por_un_enlace_simulado_se_niega` | la imagen de Backtest marzo por un enlace simulado (b) |
| `test_la_imagen_de_backtest_marzo_en_una_copia_fuera_se_niega` | la misma imagen en una copia fuera (c) |
| `test_cada_clase_en_una_copia_fuera_se_niega_con_su_regla`, `test_el_libro_y_el_holdout_de_una_copia_se_niegan_tambien_en_mayusculas_y_con_barras` | un libro de un mes no legible y un caso de `holdout/1` en una copia fuera (y el resto de las clases de D1; con mayúsculas, `/` y, en Windows, `\`) |
| `test_la_carpeta_backtest_como_objetivo_de_read_grep_y_glob_se_niega` | la carpeta `Backtest <mes no legible>` como objetivo de Read, Grep y Glob, vacía y con contenido, dentro y en la copia |
| `test_fuera_sin_ningun_anclaje_pasa` | una ruta de fuera sin anclaje, PERMITIDA (y dos que solo lo parecen: `otraestrategia del trader/…` y `holdout/4`) |
| `test_un_enlace_real_de_dentro_hacia_fuera_se_niega` | un enlace real: unión en Windows (`mklink /J`, sin administrador), `symlink_to` fuera; se salta con su motivo si no se puede crear. También el Grep, `grep -r` y Glob de la `holdout/1` enlazada |
| `test_un_enlace_de_dentro_a_un_nombre_sin_estructura_se_niega` | sostiene la forma TEXTUAL |
| `test_un_enlace_de_fuera_hacia_el_holdout_se_niega` | sostiene la forma CANÓNICA |
| `test_el_anclaje_minimo_del_material_y_de_sesiones_no_exige_corpus` | D1, el anclaje mínimo |
| `test_el_readme_de_una_particion_de_la_copia_se_sigue_leyendo` | la exención del README desde el anclaje (auditor, falta 10) |
| `test_listar_el_holdout_de_una_copia_se_niega` | ADR-0088 por estructura (Glob, `ls`, `find` de la carpeta que la contiene) |
| `test_un_lector_recursivo_sobre_la_carpeta_de_la_copia_se_niega` | lo que alcanza un lector recursivo desde fuera (PARADA, punto 4) |
| `test_listar_la_carpeta_backtest_con_ls_o_get_childitem_sigue_como_estaba` | D2: `ls`, `dir`, `Get-ChildItem` pasan; el Glob de un libro suelto pasa y su Read no |

**Los de la guardia que ya existían, en verde** con la rama: `test_guardia_claude.py`,
`test_guardia_alias.py`, `test_guardia_ci.py`, `test_guardia_falsos_positivos.py`,
`test_guardia_ffmpeg.py`, `test_guardia_g1.py`, `test_cuarentena_por_condicion.py`,
`test_cuarentena.py` y `test_hooks_utf8.py` (corrida del 2026-11-20, sin ningún `FAILED`; los
arreglos que necesitaron, §1.4). El único cambiado, `test_guardia_alias.py`, en su
`test_roto_a_proposito`.

**CLAUDE.md**, «Las guardias de Claude Code»: una línea «Guardia:» que dice que las clases
protegidas se deciden por la forma textual y la canónica y, fuera del repo, por su estructura, y
que la carpeta `Backtest <mes>` como objetivo de Read, Grep o Glob se niega como su contenido.

## 4. Regresión contra main y mutantes

### 4.1 Los tests nuevos ROMPEN con el código de main (skill comparar-con-main)

Con la rama commiteada (1c9c3e4e), dos clones desechables en una ruta corta:
`git worktree add --detach C:/cm/ge-main main` (0562a77b) y
`git worktree add --detach C:/cm/ge-rama HEAD` (1c9c3e4e). El test de la rama, copiado DENTRO del
clon de main (sha256 `6833793f0b45f626…`, el mismo en el repo y en los dos clones). En cada clon,
`uv run pytest tests/unit/test_guardia_enlaces.py -q -p no:cacheprovider -rfs --tb=line`. Ningún
comando escribe en `data/` (tests en memoria, en `tmp_path`); no hace falta `settings.local.toml`
ni se leen velas.

| Clon | Código de salida | Resultado |
|---|---|---|
| `main` | 1 | **10 de 14 FALLAN**: las dos imágenes de Backtest marzo (copia y enlace simulado), cada clase en una copia, el libro y el holdout con mayúsculas y barras, el anclaje mínimo, listar el holdout de una copia, el lector recursivo sobre la carpeta de la copia, el enlace de dentro a un nombre sin estructura, el enlace real y la carpeta Backtest como objetivo de Read, Grep y Glob |
| rama | 0 | los 14 pasan |

(Revisor, A3: los anexos no traen la línea de resumen de pytest -la configuración del repo no la
imprime con `-q`- ni el código de salida: los dos códigos son los de la consola de la sesión
(`echo exit=$?` tras cada corrida), y los hashes, de `sha256sum` en la sesión; el revisor los
volvió a medir y cuadran. Lo que traen los anexos son los `FAILED` de main y la barra de puntos de
la rama.) Esta regresión es de los 14 tests de la primera vuelta (1c9c3e4e). De los tres que entraron
tras el revisor: el del 8.3 rompe sin `_nombres_largos` (§3, medido con un test temporal) y el del
tope, por lectura, rompe en `main` (que no recorre una carpeta de fuera y deja pasar el Grep); el
del ancestro es de no regresión y pasa en los dos.

Los 4 que pasan también en `main` son los que deben: lo que no se niega (fuera sin anclaje, el
README de la copia, `ls`/`Get-ChildItem`) y `test_un_enlace_de_fuera_hacia_el_holdout_se_niega`,
que sostiene la forma canónica, que `main` ya tenía. Salidas: `anexos/GUARDIA-ENLACES/clon-main-SALIDA.txt`
y `clon-rama-SALIDA.txt`. Repo real antes y después: `git branch --list` (`main` y la rama), 168
tags, `git worktree list` solo con el repo, `git status --short` sin más que los anexos nuevos, y
ninguna `fix/*` en origin hasta el push de §5. Los dos clones se quitaron con `git worktree remove`
sin `--force` (del de main, antes, el test copiado) y `git worktree prune`.

### 4.2 Mutantes a mano

En el clon de la RAMA (`C:/cm/ge-rama`), editando SU `.claude/hooks/guardia.py` y no el hook que
corre (desviación 1), uno cada vez, con `test_guardia_enlaces.py` corrido tras cada uno y el fichero
restaurado con `git checkout --` y comprobado por hash (`137ab492…187e`, el mismo que el del repo,
las tres veces; `git status --short` del clon, vacío al final). Ningún commit lleva un mutante: se
hicieron fuera del repo.

| Mutante | Cambio | Tests que rompe |
|---|---|---|
| 1 · sin la forma TEXTUAL | `_textual` devuelve la ruta misma | `test_un_enlace_de_dentro_a_un_nombre_sin_estructura_se_niega`, `test_un_enlace_real_de_dentro_hacia_fuera_se_niega` |
| 2 · sin la forma CANÓNICA | `relativas` solo mira la textual | `test_un_enlace_de_fuera_hacia_el_holdout_se_niega` |
| 3 · sin la ESTRUCTURA | `por_estructura` devuelve `[]` | las dos de las copias, cada clase en una copia, mayúsculas y barras, el anclaje mínimo, listar el holdout de una copia y la carpeta Backtest (6) |

Salidas: `anexos/GUARDIA-ENLACES/clon-mutante1.txt`, `clon-mutante2.txt` y `clon-mutante3.txt`.
Con el mutante 3, `test_un_lector_recursivo_sobre_la_carpeta_de_la_copia_se_niega` sigue pasando:
el recorrido encuentra antes el libro por su nombre, que se niega en cualquier sitio.

## 5. CI de Linux

`git push origin trabajo/guardia-enlaces:refs/heads/fix/guardia-enlaces` (`RITUAL.md:103`), sin
tocar la local:

| Run | Commit | Resultado |
|---|---|---|
| 44847455495 | 1c9c3e4e (la guardia y los tests) | `failure` con UN fallo, el aceptado: `test_cli.py::test_state_check_ok_on_real_repo` («PROJECT_STATE declara la rama 'trabajo/guardia-enlaces'; la rama actual es 'fix/guardia-enlaces'»); `1 failed, 3487 passed, 93 skipped`; ruff, «All checks passed!» |

Tras los arreglos del revisor (§9), que tocan la guardia, la CI se repite sobre el ÚLTIMO commit
de la rama, el que trae este informe: su número no puede ir dentro de ese mismo commit, así que va
en el mensaje final a Aleks y en el registro del cierre.

El log de la CI no nombra los tests saltados. Por recuento: en `main` (run 44821324976) `3473 passed,
94 skipped` (3567); aquí 3487 + 1 + 93 = 3581 = 3567 + los 14 nuevos, con un saltado MENOS. Si
alguno de los 14 se hubiera saltado en Linux (el del enlace real solo se salta si no se puede crear
el enlace), los saltados no bajarían. No es una prueba directa: es un recuento.

## 5b. El encargo, punto por punto

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 1 | Base verificada con git (main, origin/main, tag en origin, CI de main, ninguna otra rama) | Hecho | §0 |
| 2 | Abrir con `abrir-rama` y la fila del día estadiada antes de comprobar | Hecho | 0333a957; `make-check.log` con `G2:` |
| 3 | Reloj: fila del 2026-11-21 si se pasa la medianoche; nada pesado a las 09:00 del 21; nunca cerrar | Hecho hasta aquí | todo el trabajo, el 2026-11-20; no se cierra |
| 4 | QUÉ NO CAMBIA: `src/`, `knowledge/`, `config/`, `scripts/`, `mql5/`, `Makefile`, `docs/adr/`, la hoja de ruta, las otras familias; solo se añaden negativas | Hecho | `git diff --stat main...HEAD` (§5b, abajo); las otras familias sin tocar (§2); 0 de 868 decisiones pasan de negada a permitida (§1.2) |
| 5 | 0.1 Herencias | Hecho | §1.1 |
| 6 | 0.2 Tabla por clase y forma (a, b simulada y real, c, d), por stdin y sin leer contenido; D: solo por stdin | Hecho | §1.2; anexos `medir_enlaces.py`, `medida-*-SALIDA.txt`, `tabla-*.md` |
| 7 | 0.3 Auditor | Hecho | §1.3 |
| 8 | D1: las tres formas; anclajes por condición, sin enumerar rutas | Hecho | §2 (`relativas`, `por_estructura`, `ANCLAJES`) |
| 9 | D2: la carpeta Backtest como objetivo de Read, Grep y Glob; `ls`/`dir`/`Get-ChildItem` como hoy (medido: pasan) | Hecho; Glob, retirado por la respuesta a la PARADA (punto 2) | §1.2, §2 y §10 |
| 10 | D3: lo no canonizable sigue negado | Hecho | sin cambios; `test_lo_que_no_se_puede_canonizar_se_niega_con_la_forma_buena` en verde |
| 11 | D4: falsos positivos medidos; los tests con árboles falsos no cambian | Hecho de otra forma | §1.4: 12 cambiaron; 4 arreglados en la guardia, 8 (`test_roto_a_proposito`) con las capas nuevas apagadas en el test; PARADA, punto 3 |
| 12 | Fase 1 en `guardia.py`, sin tocar las demás familias | Hecho | §2 |
| 13 | Fase 2: los seis tests pedidos, que rompen con main y pasan con la rama (comparar-con-main) | Hecho | §3 y §4.1 (10 de 14 fallan con main) |
| 14 | Mutantes: quitar cada forma de D1 rompe al menos un test; ningún commit con un mutante | Hecho de otra forma | §4.2: en el clon, no en el hook vivo (desviación 1) |
| 15 | Fase 3: los tests de la guardia en verde; la línea «Guardia:» en CLAUDE.md | Hecho | §3 |
| 16 | Fase 4: informe con todo lo pedido | Hecho | este fichero |
| 17 | Fase 5: CI de Linux por `fix/`, con su run | Hecho | §5: run 44847455495 sobre 1c9c3e4e, solo el fallo aceptado; y el del último commit |
| 18 | Fase 6: revisor con el alcance del encargo, su informe pegado | Hecho | §9 |
| 19 | Contrato con `rutas_permitidas` y lo de «Qué no cambia» en `rutas_protegidas` | Hecho | `contrato.yaml`; `CONTRATO:` en verde |
| 20 | Si la guardia cambiada niega un comando legítimo, no se rodea: a la PARADA | Hecho | no negó ninguno: los comandos que negó en la rama eran de la familia 3 (dos comandos en una llamada), los mismos que niega en `main` |

`git diff --stat main...HEAD` (1c9c3e4e): `.claude/hooks/guardia.py`, `CLAUDE.md`,
`PROJECT_STATE.md`, `contrato.yaml`, `docs/encargos/trabajo-guardia-enlaces.md`,
`docs/state/HISTORIA.md`, `docs/validation/GUARDIA-ENLACES.md`,
`docs/validation/HOLDOUT-EXPOSICIONES.md`, `docs/validation/anexos/GUARDIA-ENLACES/*`,
`tests/unit/test_guardia_alias.py` y `tests/unit/test_guardia_enlaces.py`. Nada de lo protegido.
`PROJECT_STATE.md`: 24.788 bytes (tope 25.000, `tests/unit/test_project_state.py`); la rama solo
cambió su rama, su funcionalidad, el Archivo 77 y el recuento de tests (2097 → 2111, sin cambiar de
tamaño).

**Para el commit del contrato del cierre** (`RITUAL.md`, puntos 3 y 4; en la rama no se tocan):

- Next Action: ninguna letra sale ni entra (G.8 no tiene letra: `Refs: —`).
- Hoja de ruta, G.8: la primera mitad del «Hecho cuando» (el test que la rompe a propósito con la
  ruta del repo a través del enlace, la resuelta y la carpeta en sí) HECHA por
  `stable/F39i-guardia-enlaces`; queda la segunda, de Aleks: repetir el traslado del corpus a D:
  con la guardia simulada denegando las cuatro rutas. «Hasta corregirlo, el corpus no sale de Bot
  v3\corpus» pasa a «hasta que Aleks repita el traslado con la guardia simulada».
- Tras la respuesta del consultor (§10): nada a Technical Debt; los residuos de los puntos 5 y 6, a
  la entrada G.1 de la hoja de ruta; y dos errores del consultor a la fila del cierre de
  `ERRORES-RECURRENTES.md` (§10.1).

## 6. Desviaciones

1. **Los mutantes, en el clon y no en el hook vivo** (auditor, matiz 24): el encargo dice «a mano
   como en GUARDIAS-HOLDOUT»; se hacen a mano y restaurados por hash, pero sobre el `guardia.py` del
   clon desechable de la rama, para no debilitar la guardia de la sesión mientras estén puestos.
2. **`test_guardia_alias.py` cambia** (§1.4, grupo 2): `test_roto_a_proposito` apaga las capas
   nuevas antes de romper cada pieza del alias.
3. **La estructura se mira también en la forma TEXTUAL** cuando cae fuera de la raíz (D1 dice «una
   ruta canónica que contiene»): solo añade negativas, y cubre un enlace de FUERA, de nombre con
   anclaje, hacia un sitio sin él.
4. **Más allá de la letra de D1, solo negativas**: el recorrido de una carpeta de fuera sin anclaje
   para un lector recursivo y para un listado recursivo del holdout (PARADA, punto 4); y D2 alcanza
   también a un fichero SUELTO en el material cuyo nombre empiece por la palabra `backtest` y un mes
   no legible (p. ej. `Backtest marzo 2026.pdf`): la carpeta y lo que se llame como ella.
5. **El contrato**: `tests/unit/` con los seis `test_guardia_*.py` y el nuevo; los tests de
   `test_cuarentena*.py` y `test_hooks_utf8.py` se corrieron, no se tocaron.
6. **Tras el revisor, el tope de los recorridos de fuera** (B3): `R_RECORRIDO` es una regla nueva
   que el encargo no nombra; solo niega, y solo en las carpetas de fuera que la rama empezó a
   recorrer (PARADA, punto 4).

## 7. Exposiciones

Declaradas en `HOLDOUT-EXPOSICIONES.md`, fila del 2026-11-20: los `make check` del día (el M1 de
marzo y de junio para calentar, como todos); el código y los documentos de la fase 0; y las
decisiones de la guardia por stdin y en memoria sobre rutas protegidas inventadas, del repo, de
copias sintéticas en carpetas temporales y de `D:\BotsitoCorpus` (solo la decisión). **Ningún
contenido protegido abierto**: ni velas, ni etiquetas, ni libros, imágenes, fotogramas o
transcripciones; nada de `knowledge/cases/holdout/**` ni de `D:\BotsitoCorpus`. La guardia, al
decidir un Grep sobre la carpeta real `Backtest marzo 2026` y sobre la copia de D:, recorre los
NOMBRES de sus ficheros en memoria, como en cada evento; la salida solo da la decisión.

## 8. PARADA final

Respondida el 2026-11-20: la respuesta, tal cual, y su aplicación, en §10. Lo que se pidió decidir
(lo hecho, hecho está: la rama solo añade negativas):

1. **D1 no ancla todas las clases de la familia 1.** En una COPIA o un CLON fuera del repo siguen
   pasando: los tramos no citables de v6, los ficheros con el id de un caso reservado en
   `knowledge/cases/` (kit, fidelidad, visto) y `data/visor/`, el feedback que etiqueta un
   reservado y las rutas de la lista con ocultos (medido, §1.2). Por un enlace de dentro sí se
   niegan (forma textual). Un clon de comparar-con-main lleva `knowledge/` entero. ¿Se añaden como
   anclajes `knowledge/cases/`, `data/visor/`, `knowledge/feedback/`, `knowledge/_proposals/` y
   `data/transcripciones/<vídeo con tramos>`?
2. **D2 en Glob**: hecho como decide D2, pero el auditor señala que choca con ADR-0021 §1 («listar
   nombres no es abrir») y que negar los nombres del holdout necesitó ADR-0088, mientras `ls` y
   `Get-ChildItem` siguen pasando (D2). ¿Se queda Glob negado, sin ADR, o vuelve a pasar? Y un Glob
   con comodín desde el material (`Back*/x`) que llega dentro no es «objetivo directo» y pasa.
3. **`test_roto_a_proposito` de `test_guardia_alias.py`** cambió de resultado con la rama, contra lo
   que D4 daba por hecho (§1.4): ¿vale apagar las capas nuevas en ese test, o el consultor prefiere
   otra forma?
4. **Más allá de la letra de D1**: un lector recursivo sobre una carpeta de fuera sin anclaje (la
   que contiene una copia, `D:\BotsitoCorpus`, un clon) se decide por lo que alcanza, recorriéndola
   fichero a fichero; y un listado recursivo, por si tiene debajo una copia de `holdout/{1,2,3}`. Es
   la analogía de «un ancestro de la raíz se recorre como la raíz», pero cuesta un recorrido de la
   carpeta en cada evento. Tras el revisor (B3) tiene tope: 20.000 entradas, y pasado el tope se
   niega con `R_RECORRIDO` (una carpeta de fuera enorme, p. ej. `D:\`, se niega entera a un lector
   recursivo: hay que darle una ruta más estrecha). ¿Se queda, con ese tope?
5. **Residuos de «otra forma de enlace»** (revisor, B4, ya en `main`): (a) un enlace que aparece AL
   RECORRER una carpeta del repo fuera de las zonas no se mira: `grep -R x docs` con `docs/u` como
   enlace a una copia o a `holdout/1` pasa, porque `docs` no contiene ninguna zona y no se recorre
   (y `os.walk` no sigue enlaces simbólicos; en Windows sí entra en las uniones); (b) un enlace DURO
   (`mklink /H`, sin administrador) es una copia sin anclaje en su nombre: ninguna forma de la ruta
   lo distingue, por diseño. ¿Rama propia del carril (G.1), o se aceptan como residuo?
6. **Un ancestro de la raíz que contiene una copia o un clon FUERA del repo** (revisor, B2, ya en
   `main`): un Grep sobre `C:\` se decide como la raíz (lo que alcanza DENTRO del repo) y no mira un
   clon en `C:\cm`. Recorrer `C:\` entero en cada evento no cabe en el plazo del hook. ¿Residuo
   declarado?
7. **El 8.3** (revisor, B1): el residuo que este punto describía en la primera vuelta estaba mal
   descrito (ese caso sí se negaba, por la estructura de la forma textual); el de verdad -un enlace
   de dentro hacia un nombre sin anclaje, con un tramo 8.3 por encima- quedó cerrado con
   `_nombres_largos` y su test. Nada que decidir: se informa.
8. **G.8, «Hecho cuando»**: la segunda mitad -Aleks repite el traslado del corpus a D: con la
   guardia simulada denegando las cuatro rutas- es de Aleks, tras el cierre. Con esta rama, la
   imagen y la carpeta `Backtest marzo 2026` por la ruta de D: salen negadas (§1.2, stdin).

## 9. El revisor

Subagente `revisor` (`.claude/agents/revisor.md`), lanzado el 2026-11-20 sobre 0333a957 y
1c9c3e4e (más el informe y los anexos `clon-*.txt` aún sin commitear), con el alcance del encargo:
la guardia de la rama contra la de `main` caso a caso en la familia 1, y buscar una ruta protegida
que siga pasando. Su informe, tal cual (sin retiradas: no cita ningún tramo no citable):

## Informe del revisor · trabajo/guardia-enlaces · 2026-11-20

Base 0562a77b (= main = origin/main; `stable/F39h-guardias-holdout^{commit}` = fb1f02e9). Commits 0333a957 y 1c9c3e4e. En el árbol, sin commitear: `GUARDIA-ENLACES.md` y cinco anexos `clon-*.txt`. El `guardia.py` del árbol es igual al de HEAD (sha256 `137ab492…187e`).

**En corto:** no encuentro ninguna regla que `main` negara y la rama deje pasar en las clases de la familia 1 (comparado función a función, abajo). Sí encuentro cuatro huecos que siguen abiertos y que el informe no declara (o declara mal), y un posible paso de negado a permitido que depende del límite de 30 s del hook y que no pude confirmar. Además, el informe no está al día: la CI ya terminó y el revisor figura como hecho.

### Eje (a) · Reglas de la casa
Resumen: 0 bloquea, 1 importa, 3 menor.

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| A1 | importa | La cabecera y el Estado del informe dicen que faltan la regresión y los mutantes, pero el §4 ya los trae, con sus anexos. | `GUARDIA-ENLACES.md:3-4` («faltan la regresión en clones, los mutantes…»), `:418-419` («faltan la regresión contra main y los mutantes en clones (§4)»), frente a `:260-301` |
| A2 | menor | Dice «las tres capas nuevas» y nombra cuatro parches. Lo mismo en el comentario del test. | `GUARDIA-ENLACES.md:175-176`; `tests/unit/test_guardia_alias.py:821-828` |
| A3 | menor | El §4.1 afirma códigos de salida 1/0, «14 pasan», y sha256 `6833793f…` y `137ab492…` comprobados en los clones. Los anexos no traen ni la línea de resumen de pytest, ni el código de salida, ni ningún hash. Los hashes sí cuadran con el repo (medido por mí). | Grep `passed\|exit\|6833793f\|137ab492` en `anexos/GUARDIA-ENLACES/clon-*.txt`: sin coincidencias. `clon-rama-SALIDA.txt` acaba en `..............  [100%]`. `sha256sum`: `137ab4921af3…187e` (guardia), `6833793f0b45…b450` (test) |
| A4 | menor | El §7 dice que la fila de HOLDOUT cubre también las decisiones «en memoria» y los clones. La fila (3) solo dice «por stdin» y «ficheros vacíos», y los tests escriben `"dato falso\n"`. | `GUARDIA-ENLACES.md:376-379`; `HOLDOUT-EXPOSICIONES.md` (fila 2026-11-20 de la rama); `test_guardia_enlaces.py:81` |

Comprobado sin hallazgos:
- **Contrato:** `uv run python scripts/contrato_rama.py` da «CONTRATO: 18 ficheros dentro del contrato…» y «G2: fila de HOLDOUT-EXPOSICIONES del 2026-11-20 para trabajo/guardia-enlaces, estadiada».
- **`make-check.log` (19:54):** «3575 passed, 6 xfailed», «SELLO: make check en verde sobre el arbol 9aa611ad…», «PICO DE MEMORIA … 320 MiB». No ejecuté `make check`: escribe.
- **Tests de la guardia del contrato:** los siete ficheros, con `python -B -m pytest … -p no:cacheprovider`, salen con código 0 y sin ningún `FAILED`. La cola de la salida no conserva el recuento.
- **Trailers `Fuente:`:** no aplica; la rama no toca `knowledge/spec` ni `knowledge/cases`.
- **Holdout:** nada de la rama lo toca. La fila del día existe.
- **Regímenes de cambio:** nada en `evidence/`, `feedback/`, `manifests/`, `corpus/`.
- **Ambigüedades, ADR y `cita`:** no aplican.
- **Informes:** `HOLDOUT-EXPOSICIONES.md` solo gana una fila. `HISTORIA.md` es solo añadido (183/0).
- **`PROJECT_STATE.md`:** cambia la rama, la funcionalidad, el Archivo 77 y 2097→2111 (+14 = los tests nuevos).
- **`CLAUDE.md`:** tiene la línea «Guardia:» que pide el encargo.
- **Citas comprobadas contra su fuente:** `HOJA-DE-RUTA.md:828-835` (G.8), `RITUAL.md:101-103`, `GUARDIA-ALIAS.md:381` y `:455`, y `relativa` en `main:guardia.py:544-551`.

### Eje (b) · Encargo
Resumen: 0 bloquea, 5 importa, 0 menor. Requisitos: 15 hechos, 2 hechos de otra forma (declarados), 2 parciales, 2 no hechos todavía.

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 1 | Base verificada | Hecho | `git rev-parse main origin/main` da dos veces 0562a77b. Tag → fb1f02e9. `git branch --list`: main y la rama |
| 2 | `abrir-rama` y fila del día estadiada | Hecho | Línea `G2:` del contrato |
| 3 | Reloj; no cerrar | Hecho hasta ahora | Push de la CI a las 01:00Z del 21 = 20:00 del 20 en Lima. Ningún merge |
| 4 | QUÉ NO CAMBIA | Hecho | `git diff --stat main...HEAD`: nada de `src/`, `knowledge/`, `config/`, `scripts/`, `mql5/`, `Makefile`, `docs/adr/` ni la hoja de ruta. CONTRATO en verde |
| 5 | Solo añade negativas | Hecho por lectura, salvo lo condicional de B3 | Comparación caso a caso, abajo. `comparacion-caso-a-caso.txt`: 0 de 868 pasan de negada a permitida |
| 6 | 0.1 Herencias | Hecho | §1.1 |
| 7 | 0.2 Tabla por clase y forma | Hecho | §1.2; `tabla-main.md`, `tabla-rama.md` |
| 8 | 0.3 Auditor | Hecho (según el informe) | §1.3 |
| 9 | D1: tres formas; anclajes por condición | Hecho, con los huecos B1 y B4 | `guardia.py:557-592` |
| 10 | D2: carpeta Backtest en Read, Grep y Glob; `ls`/`Get-ChildItem` como hoy | Hecho | `guardia.py:663-686`, `:709`, `:5885-5890`. Test `test_listar_la_carpeta_backtest…` |
| 11 | D3: lo no canonizable sigue negado | Hecho | `guardia.py:1461-1462`: `_canonica` antes de `_sin_resolver` |
| 12 | D4: falsos positivos | Hecho de otra forma, declarado | §1.4: 12 tests cambiaron; PARADA 3 |
| 13 | Fase 1 en `guardia.py` | Hecho | Diff |
| 14 | Fase 2: los seis tests, que rompen con main | Hecho | `clon-main-SALIDA.txt:284-293`: 10 FAILED. En la CI de Linux ninguno se salta |
| 15 | Mutantes: cada forma rompe al menos un test | Hecho de otra forma, declarado (desviación 1) | `clon-mutante1.txt:3-4`, `clon-mutante2.txt:3`, `clon-mutante3.txt:3-8` |
| 16 | Fase 3: tests en verde y línea en `CLAUDE.md` | Hecho | Mi corrida: código 0. Diff de `CLAUDE.md` |
| 17 | Fase 4: informe completo | Parcial | PARADA «PENDIENTE»; estados viejos (A1) |
| 18 | Fase 5: CI de Linux | Parcial | `gh run view 44847455495`: «X Run make check». El log: «ERROR: PROJECT_STATE declara la rama 'trabajo/guardia-enlaces'; la rama actual es 'fix/guardia-enlaces'» y «1 failed, 3487 passed, 93 skipped». Es el único fallo que el encargo acepta, pero el informe sigue en «PENDIENTE» (§5, línea 310) |
| 19 | Fase 6: revisor pegado | No hecho todavía | Es este informe; no existe ningún §9 |
| 20 | Contrato | Hecho | `contrato.yaml` |
| 21 | «Rama lista para revisión, NO cerrada» | No hecho todavía | — |

**Comparación caso a caso con main (alcance 1): ninguna regresión encontrada leyendo el código.**
- `motivo_fichero` → `_motivo_en_el_sitio`: la forma canónica dentro de la raíz va siempre la primera en `relativas` (`:587-591`) y pasa por el mismo cuerpo que en main. `nombre` sale de `rel` y no de `basename`, pero para la canónica es lo mismo. La exención del README ahora sigue mirando las demás formas, así que solo puede negar más.
- `_motivo_material`/`_motivo_backtest`: con «/» en `resto` la condición es la de main (`:673-676`).
- `motivo_directorio`: el ancestro recorre la raíz como en main (`:712-715`). `_ruta_real(zona[len(rel):], Path(ruta))` equivale a `_ruta_real(zona)` cuando `ruta` es `<raíz>/<rel>`, y solo se llega con `isdir` cierto.
- `_primer_protegido`: `extra` es falso para la forma canónica, así que hace lo mismo que en main.
- `lista_dentro_del_holdout`: el ancestro recursivo sigue en True, y con `rel` presente hace el mismo bucle.
- `motivo_dentro_de_zona`: igual que main.
- `lineas_de_tramo`: R_TRAMO solo sale si ninguna forma anterior negó, y la forma que elige es la que lo produjo.
- `_patron_lista_el_holdout`: el mismo número de tramos que `_normcase` en Windows. `_candidatos_del_holdout` solo añade candidatos.
- `RutaCanonica`: tiene el mismo valor de `str` y no hay ninguna comprobación de tipo exacto (grep `type(…) is str`: nada).

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| B1 | importa | **La forma textual no expande los nombres cortos 8.3, y el residuo del §8.5 está mal descrito.** `_sin_resolver` solo quita prefijos, puntos finales y normaliza; quien expande el 8.3 es `realpath`. Si dentro del repo hay un enlace a una carpeta sin anclaje (`holdout/1` → `C:\zz`, `Backtest marzo 2026` → `D:\bm`) y la ruta se escribe con un tramo 8.3 por encima (`KNOWLE~1\cases\holdout\1\…`, `corpus\ESTRAT~1\MATERI~1\Backtest marzo 2026\x.png`), no niega nadie: ni la textual (`knowle~1/…` no casa), ni la canónica (sin anclaje), ni la estructura. Por el contrario, el caso que el §8.5 da por invisible (la raíz en 8.3 y `knowledge/` enlazado) sí se niega: la textual cae fuera de la raíz y `por_estructura(textual)` encuentra `knowledge/cases/holdout/1`. En este volumen los 8.3 existen. No lo pude medir en memoria (ver «Lo que no pude comprobar»). | `guardia.py:1439-1445`, `:1518-1534`, `:581-592`, `:563-579`. `GUARDIA-ENLACES.md:409-412`. `GetShortPathNameW` medido: `Bot v3` → `BOTV3~1`, `knowledge` → `KNOWLE~1` |
| B2 | importa | **Un ancestro de la raíz que contiene una copia o un clon no se recorre fuera del repo.** Para un ancestro (`C:\`, el Escritorio), `motivo_directorio` devuelve solo lo que encuentra dentro de la raíz y nunca llama a `lo_que_alcanza_fuera`. Un Grep sobre `C:\` alcanza un clon en `C:\cm\ge-main` (la ruta que usó el §4.1), cuyo `holdout/` versionado ripgrep sí lee, y pasa. La PARADA 4 no lo dice. Ya ocurría en main; no es regresión. | `guardia.py:712-715` (return temprano), `:716-721` |
| B3 | importa | **Recorridos sin tope en cada evento, con un hook de 30 s.** `holdout_debajo` (sin corte al primer resultado) y `lo_que_alcanza_fuera` recorren todo el árbol de cualquier carpeta de fuera o ancestro. En main, el Glob de un ancestro no recorría nada: casaba con la sonda y negaba. Medido en memoria: Glob `**/*.yaml` con `path` = el Escritorio tarda 11,3 s en frío (niega) y `**/*.md`, 1,9 s en caliente. Sobre `C:\` o el perfil seguramente pasa de 30 s, aunque no lo pude medir. Si al vencer el plazo Claude Code deja pasar la herramienta, un Glob que main negaba pasaría a permitirse, contra «solo añade negativas». La PARADA 4 dice «lento», no el plazo ni lo que pasa cuando vence. | `guardia.py:817-827`, `:2120-2127`, `:723-727`. `.claude/settings.json:81` (`"timeout": 30`). Mi medida: «`**/*.yaml` -> NIEGA … 11.3 s», «`**/*.md` -> PASA 1.9 s» |
| B4 | importa | **Residuos de «otra forma de enlace» sin declarar.** (1) Un enlace que se encuentra AL RECORRER no se sigue: `os.walk` va sin `followlinks` (en Windows sí entra en las uniones, porque `islink` es falso para ellas), y en una carpeta del repo fuera de las zonas no se recorre nada. Pero `grep -R`, `find -L` y `rg -L` siguen enlaces, y la guardia trata `-R` igual que `-r`. Ejemplo: `grep -R x docs` con `docs/u` → copia o `holdout/1` (la unión de `test_leer_por_una_union…` está justo en `docs/`) pasa. (2) Un enlace duro (`mklink /H`, sin administrador) es una copia sin anclaje que D1 no puede ver por diseño. Ninguno de los dos está en el §8. | `guardia.py:729-751` (solo zonas), `:787`, `:1975-1977`. `GUARDIA-ALIAS.md:455` |
| B5 | importa | **El «punto por punto» da por hechas dos cosas que no lo están.** El #17 dice «Hecho» con el §5 en «PENDIENTE»; la CI ya terminó, con un fallo aceptable que el informe no recoge. El #18 dice «Hecho \| §9», y el informe no tiene §9. | `GUARDIA-ENLACES.md:310`, `:332-333`. `gh run view 44847455495` |

Lo hecho fuera del encargo, ya declarado: el recorrido de carpetas de fuera sin anclaje (desviación 4, PARADA 4), la forma textual por estructura (desviación 3) y el cambio en `test_roto_a_proposito` (desviación 2). Lo que el encargo dice que no se toca: comprobado con el diff, sin hallazgos.

### Lo que no pude comprobar
- **Medidas en memoria de B1 y B2, y el recorrido de `C:\Users\USER` para B3:** la guardia negó los dos guiones. El primero nombraba rutas del holdout («el codigo nombra \Bot v3\knowledge\cases\holdout\1\…»); el segundo recorría y nombraba la carpeta del repo («el codigo nombra la carpeta … que contiene material protegido»). No reescribí los comandos para esquivarla (CLAUDE.md); B1, B2 y B4 salen de leer el código.
- **Qué hace Claude Code cuando el hook pasa de sus 30 s** (si deja pasar o bloquea): no lo medí. De eso depende que B3 sea una regresión de verdad.
- **El tiempo de main para el mismo Glob:** no cargué el `guardia.py` de main en memoria. Que main no recorre sale del código: `_candidatos_del_holdout(politica)` solo mira las zonas de la raíz.
- **Que el encargo sea copia literal del mensaje original, la salida del auditor y la CI de main (run 44821324976):** no los verifiqué.
- **El recuento de mi corrida de pytest:** la cola de la salida no lo conserva; solo el código 0 y ningún `FAILED`.
- **`make check`:** no lo ejecuté porque escribe. Evidencia: `make-check.log`.

### Comandos ejecutados
1. `git branch --show-current && git merge-base main HEAD && git log --format='%h %s' main..HEAD && git diff --stat main...HEAD && git status --short`
2. `git diff main...HEAD -- .claude/hooks/guardia.py`
3. `grep -n "def \|^MATERIAL…" .claude/hooks/guardia.py`
4. `git show main:.claude/hooks/guardia.py | sed -n '544,712p'`
5. `grep -n "_absoluta(\|ctx.cwd = \|\.cwd = " .claude/hooks/guardia.py`
6. `sed -n '1,80p' .claude/hooks/solo_lectura.py`
7. `python --version && python -c …` (negado por la guardia: dos comandos)
8. `python -c 'import os, sys; print(os.name, sys.version)'`
9. `python -c` con la medida de 8.3 en memoria (negado por la guardia: nombra el holdout)
10. `python -c` con `GetShortPathNameW` sobre la raíz, `knowledge` y `docs/validation`
11. `uv run python scripts/contrato_rama.py`
12. `PYTHONDONTWRITEBYTECODE=1 uv run --no-sync pytest …` (negado: nombre de entorno)
13. `uv run --no-sync python -B -m pytest <los 7 test_guardia_*> -q -p no:cacheprovider` (en segundo plano; código 0)
14. `git diff main...HEAD -- CLAUDE.md PROJECT_STATE.md docs/validation/HOLDOUT-EXPOSICIONES.md tests/unit/test_guardia_alias.py; git diff --numstat main...HEAD -- docs/state/HISTORIA.md`
15. `grep -c/-n -i "worktree\|clon desechable…" docs/validation/HOLDOUT-EXPOSICIONES.md | cut -c1-14` y `sed -n '143p' … | grep -o …`
16. `grep -n -i '\$DATA…'` y `'enlace duro\|hardlink…'` en la guardia y los informes
17. `for f in clon-*…` (negado por la guardia: `for`); después, Grep sobre `clon-*.txt` y `tail` de los cinco anexos
18. `git hash-object …` (negado por solo_lectura); `sha256sum .claude/hooks/guardia.py tests/unit/test_guardia_enlaces.py && git diff --stat HEAD -- …`
19. `gh run view 44847455495`; `gh run view 44847455495 --log-failed | grep …` (dos veces)
20. `grep -n "type(.*) is str…" .claude/hooks/guardia.py`
21. `grep -n -B2 -A8 'guardia.py' .claude/settings.json`
22. `grep -n -- '--follow\|dereference\|"-L"\|followlinks\|"-R"' .claude/hooks/guardia.py`
23. `time (echo '{…Glob…}' | python .claude/hooks/guardia.py …)` (negado por la guardia)
24. `python -c` con el tiempo de `decidir` para Glob en el Escritorio (11,3 s y 1,9 s)
25. `python -c` con el Glob sobre `C:\Users\USER` y tope de 45 s (negado por la guardia)
26. `git rev-parse main origin/main "stable/F39h-guardias-holdout^{commit}" && git branch --list && git ls-remote --heads origin && git log --format='%h %G? %s' main..HEAD`
27. `ls -la make-check.log; grep -E "SELLO|PICO DE MEMORIA|…" make-check.log`
28. `grep -n "LECTOR_DE_METADATOS =" …` (rama y main); `sed -n '826,836p' docs/plan/HOJA-DE-RUTA.md`
29. `sed -n '101,103p' docs/runbooks/RITUAL.md; sed -n '381p;455p' docs/validation/GUARDIA-ALIAS.md`

Ficheros: `C:\Users\USER\Desktop\Bot v3\.claude\hooks\guardia.py`, `C:\Users\USER\Desktop\Bot v3\docs\validation\GUARDIA-ENLACES.md`, `C:\Users\USER\Desktop\Bot v3\tests\unit\test_guardia_enlaces.py`, `C:\Users\USER\Desktop\Bot v3\tests\unit\test_guardia_alias.py`, `C:\Users\USER\Desktop\Bot v3\.claude\settings.json`, `C:\Users\USER\Desktop\Bot v3\docs\validation\anexos\GUARDIA-ENLACES\` (los `clon-*.txt` y `comparacion-caso-a-caso.txt`).

### Lo que se hizo con los hallazgos del revisor

| # | Gravedad | Respuesta |
|---|---|---|
| A1 | importa | Arreglado: la cabecera y el `## Estado` dicen lo que hay |
| A2 | menor | Arreglado: «tres capas, cuatro parches», en el informe (§1.4) y en el comentario de `test_guardia_alias.py` |
| A3 | menor | Contestado en §4.1: los códigos de salida son de la consola y los hashes de `sha256sum` en la sesión; los anexos traen los `FAILED` y la barra de puntos |
| A4 | menor | Arreglado: la fila del 2026-11-20 de `HOLDOUT-EXPOSICIONES.md` se amplía el mismo día con lo hecho en memoria, los ficheros «dato falso», las uniones, los clones y la medida del revisor |
| B1 | importa | Arreglado en la guardia (`_nombres_largos`) con su test, que falla sin el arreglo (§3); el punto 7 de la PARADA corrige la descripción del residuo |
| B2 | importa | Ya en `main`; declarado: PARADA, punto 6 |
| B3 | importa | Arreglado: tope de 20.000 entradas en los recorridos de fuera (`R_RECORRIDO`) y el ancestro de la raíz sin recorrer, con dos tests (§2, §3); qué hace Claude Code al vencer el plazo de 30 s no se midió: con el tope, la guardia no llega a él en las carpetas de fuera |
| B4 | importa | Ya en `main`; declarado: PARADA, punto 5 |
| B5 | importa | Arreglado: §5 y §5b con la CI terminada y el §9 |

Tras los arreglos: los tests de la guardia y los 17 nuevos, en verde (§3); `make check` sellado y la
CI de Linux del último commit (§5).

## 10. Respuesta del consultor a la PARADA final

Del 2026-11-20, por la noche; copiada tal cual (también al final del encargo):

> Modelo: Opus · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA final de trabajo/guardia-enlaces (§8 de GUARDIA-ENLACES.md), 2026-11-20. Cópiala tal cual al informe, en una sección «Respuesta del consultor a la PARADA final». Si pasas de medianoche, la fila de HOLDOUT del 2026-11-21 va antes del primer make check de ese día. A las 09:00 de Lima del 21 no puede haber nada pesado corriendo (Aleks graba).
>
> 1. Las clases sin anclar: (a), se añaden en ESTA rama. Los tramos no citables (data/transcripciones/<vídeo con tramos>/), los ficheros con id de caso reservado en knowledge/cases/ y data/visor/, el feedback que etiqueta un caso reservado (knowledge/feedback/) y la lista de ficheros con ocultos, como anclajes con la misma regla de D1: se decide como si el anclaje estuviera en la raíz. Un test por clase, en una copia fuera del repo (negada), que rompa con el código de antes de este cambio. Por qué: es la misma condición que D1 («nombra la condición»), y dejarla a medias deja copias o clones fuera del repo sin proteger.
>
> 2. Glob sobre la carpeta Backtest: vuelve a pasar, como ls y Get-ChildItem. D2 queda solo para Read y Grep con la carpeta como objetivo. Por qué: listar nombres no es leer contenido, y ADR-0021 §1 lo permite; una prohibición que no sale de un ADR no se escribe (CLAUDE.md). Error del consultor, que irá a la fila del cierre. Ajusta el test y la línea de CLAUDE.md.
>
> 3. Apagar las capas nuevas en test_roto_a_proposito: sí, con una condición. Añade un test que, con TODAS las capas encendidas, compruebe que esas mismas rutas salen negadas, para que la combinación también quede cubierta. El cambio en tests existentes que D4 no previó es error del consultor y va a la fila del cierre.
>
> 4. El tope de 20.000 entradas, negando al pasarlo: se queda. Es negar por defecto, y lo impone el límite de 30 s del hook. Escríbelo en el informe, en la línea de CLAUDE.md y con su test (pasado el tope, se niega).
>
> 5 y 6. Los residuos que ya pasaban en main (enlaces encontrados al recorrer, enlaces duros, C:\ con un clon fuera del repo): residuo aceptado, sin rama propia por ahora. Van a la entrada G.1 de la hoja de ruta en el cierre, no a Technical Debt, porque PROJECT_STATE está en 24.776. Por qué: piden que alguien cree a propósito un enlace duro o un clon en la raíz de un disco, y la barrera sigue siendo el código.
>
> 7. G.8: de acuerdo. El código queda hecho con esta rama; la entrada pasa a HECHA solo cuando Aleks repita el traslado a D: y la guardia simulada niegue las cuatro rutas. Eso lo registra la orden de cierre de la rama siguiente.
>
> Lo que sigue: un commit con 1-4 y esta respuesta en el informe (make check sellado antes); push a fix/guardia-enlaces y CI de Linux con su número de run; revisor con alcance en lo nuevo (los anclajes añadidos, caso a caso contra el commit anterior, y el cambio de Glob); su informe pegado al final.
>
> Rama lista para revisión, NO cerrada.

### 10.1 La respuesta, aplicada punto por punto

| Punto | Hecho | Evidencia |
|---|---|---|
| 1 · Las clases sin anclar, como anclajes con la regla de D1 | Hecho | `Politica.por_estructura`: `data/transcripciones/<vídeo>` también con un vídeo con tramos no citables (`tramos_vigilados`); `ANCLAJES_POR_FICHERO` = `knowledge/cases/`, `data/visor/`, `knowledge/feedback/`; y una ruta cuya cola es exactamente una de la lista con ocultos (`ficheros_ocultos`). La ruta se lee como si el anclaje estuviera en la raíz y deciden las reglas de siempre (`_motivo_en_el_sitio`: `R_TRAMO` con su lectura por líneas, `R_CASO` por el nombre o el contenido, `R_FICHERO_OCULTO`). Un test por clase en una copia fuera, negada: `test_un_tramo_no_citable_…`, `test_un_caso_reservado_en_cases_…`, `test_un_caso_reservado_en_el_visor_…`, `test_el_feedback_de_un_reservado_…`, `test_un_fichero_de_la_lista_con_ocultos_…`; y uno de que no se pasan de frenada (`test_lo_que_no_es_reservado_en_esas_clases_de_la_copia_pasa`: un caso no reservado, un feedback que no etiqueta ninguno, una cruda sin cuarentena ni tramos, una propuesta fuera de la lista y la cruda de v6 leída por un trozo fuera del tramo). **Rompen con el código de antes de este cambio**: en un clon `git worktree add --detach C:/cm/ge-antes 99b512b8` con el test nuevo copiado dentro, los cinco FALLAN (exit 1; `anexos/GUARDIA-ENLACES/clon-antes-de-la-respuesta-SALIDA.txt`); el clon se quitó sin `--force`. Las propuestas con un tramo pisado (`_motivo_propuesta`, `knowledge/_proposals/`) no eran una de las clases de la respuesta y siguen sin anclaje: lo que de ellas está en la lista con ocultos, sí se niega |
| 2 · Glob sobre la carpeta Backtest vuelve a pasar | Hecho | El bloque de D2 de Glob en `decidir`, fuera, y con él `_parte_literal`; D2 queda en `_motivo_material` (Read) y en `motivo_directorio` (Grep). El test pasa a `test_la_carpeta_backtest_como_objetivo_de_read_y_grep_se_niega`, y Glob (`*` con la carpeta de base y `…/*.xlsx`) entra en `test_listar_la_carpeta_backtest_con_ls_get_childitem_o_glob_pasa`, que falla con el código anterior (lo negaba). La línea de `CLAUDE.md` dice «Read o Grep» y que Glob, `ls` y `Get-ChildItem` la listan (ADR-0021 §1). El Glob de una copia de `holdout/{1,2,3}` sigue negado: es ADR-0088 |
| 3 · El test con todas las capas encendidas | Hecho | `test_roto_con_las_capas_encendidas_sigue_negando` en `tests/unit/test_guardia_alias.py`, parametrizado con las ocho combinaciones de §1.4 (`CUBIERTAS_POR_LAS_CAPAS`): rompe la pieza del alias SIN apagar las capas y exige que el test de la pieza PASE (las rutas, negadas). Es la combinación que pide el punto: la pieza rota y las capas puestas. Con la pieza entera, las mismas rutas ya las cubren los tests de la pieza, que corren con todo encendido |
| 4 · El tope de 20.000 entradas | Hecho | Estaba (§2, «Tras el revisor»; `test_el_recorrido_de_una_carpeta_de_fuera_tiene_tope`); ahora también en la línea de `CLAUDE.md` |
| 5 y 6 · Residuos aceptados, a G.1 en el cierre | Para el cierre | Preparado abajo, en «Para el commit del contrato del cierre» |
| 7 · G.8 | Para el cierre | Igual |

**Lo que cambia en «Para el commit del contrato del cierre»** (§5b) con esta respuesta: no va nada a
Technical Debt. A la entrada **G.1** de la hoja de ruta, como residuos aceptados sin rama propia: un
enlace que aparece al recorrer una carpeta del repo fuera de las zonas, un enlace duro, y un ancestro
de la raíz (`C:\`) con un clon fuera del repo. **G.8**: el código, hecho con esta rama; pasa a HECHA
cuando Aleks repita el traslado a D: y la guardia simulada niegue las cuatro rutas (lo registra la
orden de cierre de la rama siguiente). A la fila del cierre en `ERRORES-RECURRENTES.md`, dos errores
del consultor que él mismo nombra: D2 negaba Glob sin un ADR (punto 2) y D4 no previó que cambiaran
tests existentes (punto 3).

**Tests y medidas tras la respuesta**: los 23 de `test_guardia_enlaces.py`, el nuevo de
`test_guardia_alias.py` (ocho casos) y los de la guardia, en
verde (§3); `PROJECT_STATE.md`, 2121 funciones de test. La medida de la fase 0.2
(`anexos/GUARDIA-ENLACES/medida-*`) es de antes de esta respuesta y no se rehízo: los anclajes nuevos
solo añaden negativas en las cinco filas de copia y clon que tenían «P» (§1.2), y el Glob de la
carpeta Backtest vuelve a lo de `main`.

## Estado

EN CURSO: la respuesta del consultor a la PARADA final, aplicada (§10); faltan la CI de Linux de
este commit y el revisor sobre lo nuevo.
