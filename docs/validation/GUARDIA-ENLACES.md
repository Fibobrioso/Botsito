# GUARDIA-ENLACES · La guardia protege el material por lo que es, no solo por donde esta (G.8)

> PLANTILLA hasta la fase 0 (la línea con que nació): ya no lo es; la fase 0 y las fases 1 a 4 están
> hechas, y faltan la regresión en clones, los mutantes, la CI de Linux y el revisor (§9).

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
     las tres capas nuevas (`_textual`, `_sin_resolver`, `Politica.por_estructura` y
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
  los lectores recursivos) y Glob (`motivo_carpeta_backtest` sobre la base y la parte literal del
  patrón, `_parte_literal`). Lo de dentro, como siempre (cualquier carpeta `backtest*`); la carpeta
  misma, solo con `backtest` como palabra: la medida «después» encontró que con `startswith` un
  libro SUELTO `backtesting-analytics …` caía también, y su Glob no debe negarse (leerlo lo niega su
  propia regla). `ls`, `dir` y `Get-ChildItem` no pasan por estas funciones: siguen como estaban.
- **D3**: sin cambios; `_sin_resolver` se calcula después de `_canonica`, que ya habría negado lo no
  canonizable.

## 3. Tests (fases 2 y 3)

`tests/unit/test_guardia_enlaces.py`, nuevo, 14 tests EN MEMORIA sobre repos y copias inventados
(rutas a trozos, como `test_guardia_alias.py`):

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

PENDIENTE: se hace tras este commit, en dos clones `git worktree add --detach` en `C:\cm`.

### 4.2 Mutantes a mano

PENDIENTE: en el clon de la rama, editando SU `guardia.py` (no el hook que corre), restaurado por
hash; quitar cada una de las tres formas de D1 tiene que romper al menos un test.

## 5. CI de Linux

PENDIENTE: push a `fix/guardia-enlaces` (`RITUAL.md:103`).

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

PENDIENTE de cerrar tras la regresión, la CI y el revisor. Lo que va:

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
   carpeta en cada evento (rápido en una carpeta temporal; lento en una enorme, p. ej. `D:\`). ¿Se
   queda?
5. **Residuo**: el anclaje del holdout es la constante entera (`knowledge/cases/holdout/N`). Si
   `knowledge/` fuera un enlace a otro sitio Y la ruta se escribiera con el nombre corto 8.3 de la
   raíz, ni la textual (no casa con la raíz) ni la canónica (sin `knowledge/`) ni la estructura lo
   verían. Con `cases/holdout/N` como anclaje se cerraría. ¿Se amplía?
6. **G.8, «Hecho cuando»**: la segunda mitad -Aleks repite el traslado del corpus a D: con la
   guardia simulada denegando las cuatro rutas- es de Aleks, tras el cierre.

## Estado

EN CURSO: fase 0 y fases 1 a 4 hechas; faltan la regresión contra main y los mutantes en clones
(§4), la CI de Linux (§5), el revisor y la PARADA final cerrada.
