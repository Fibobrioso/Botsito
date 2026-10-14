# ENTRADA-ENERO · X (los ticks por la rejilla) y enero de 2026 entra en construcción (R2.2)

Rama `trabajo/entrada-enero`, abierta el 2026-10-13 desde `main` en 6fb483b (commit de estado
sobre el merge a4e4fa6, tag `stable/F37o-entrada-julio`). Encargo:
`docs/encargos/trabajo-entrada-enero.md`. Tramo: R2 (R2.2 de `docs/plan/HOJA-DE-RUTA.md`; X de
la Next Action).

(Hasta que existió, ADR-0079 iba declarado aquí en un bloque `ids-inexistentes`, como exige
`knowledge validate`; salió con el commit de la fase 3, que lo crea.)

## Base, comprobada con git al abrir

- `git rev-parse main origin/main`: dos veces `6fb483bea6a2554dcaca41b4a113a74376d440df`.
- `git rev-parse main^1` y `git rev-parse "stable/F37o-entrada-julio^{commit}"`: los dos
  `a4e4fa652ddf31bc1e82b589a9f703474c5674ce`; el tag está en origin
  (`git ls-remote --tags origin`: objeto 6202f13, anotado), y es el último `- Tag: ` de HISTORIA.
- CI de `main` sobre 6fb483b (check-runs, sha literal): run 38463152743, `completed` / `success`.
- `git branch --list`: solo `main`; `git ls-remote --heads origin`: solo `main`.
- `/model`: Opus 5.5 con esfuerzo alto (lo pedía el encargo).

## 0. Fase 0 · inventario (2026-10-13), sin abrir nada y sin escribir en el repo

Medido en la rama sobre `main` 6fb483b. No se ha abierto ningún libro: lo que se lee son el
registro, los manifiestos de `data/manifests/`, las velas M1 de enero (ADR-0021 §1: leer velas no es
abrir) y los repartos por recuento. Los guiones de medida están en
`docs/validation/anexos/ENTRADA-ENERO/` con su salida (`*.txt`). El auditor del encargo
(`auditor-encargo`) contrastó el encargo con el repo; su resumen, en «El encargo frente al repo».

### 0.a La base y las tres medidas de la decisión 1

- Base: arriba, «Base, comprobada con git al abrir». CORRECTO.
- Con `casos_reservados(repo)` y `casos_ocultos(repo)` sobre los repartos commiteados de los dos
  caminos, contando por mes y sin imprimir ids (`anexos/ENTRADA-ENERO/medidas_enero.py`):
  `casos_reservados: 34 en total; en 2026-01: 0` y `casos_ocultos: 34 en total; en 2026-01: 0`
  (por partición: holdout-1, -2 y -3 con 8 cada una y fidelidad-1 con 10). CORRECTO.
- `knowledge/cases/meses_reservados.yaml`: `2026-01` aparece 0 veces. CORRECTO.
- `knowledge/cases/kit/vistos.yaml:34-38`: `mes: "2026-01"`, `visto_el: "2026-08-30"`, fuentes
  `ev-v4-000243-a1067c1c` y `ev-v4-001027-1b74d1a6` (backtest de enero recorrido en v4). CORRECTO.
- `knowledge/corpus/libros.yaml:53-67`: el libro `ee4ade46…` (`backtesting-analytics ENERO
  2026.xlsx`), formato `AAAA/MM/DD HH:MM:SS`, huso `UTC`, `declarado_el: "2026-10-06"`, fuente
  ADR-0039. CORRECTO. (De pasada: el comentario de cabecera de `libros.yaml:15`, «NO ESTAN enero ni
  septiembre», quedó falso el 2026-10-06; el fichero es SOLO AÑADIR y un comentario no se edita:
  va como nota, no como cambio.)
- Estado de partida: `construccion = ["2026-04", "2026-07", "2026-08"]`
  (`knowledge/cases/criterio_fidelidad.yaml:37`); 0 casos de enero en `knowledge/cases/dev/`; no
  existe `knowledge/cases/visto/2026-01/`; enero no tiene tramo en `cobertura_material` ni sha en
  `materiales` (`kit/config.yaml`).
- ADR-0079: `docs/adr/` termina en 0078; 0079 es el siguiente libre. CORRECTO.

### 0.b HOLDOUT-EXPOSICIONES y el falso positivo de `cases/visto.py`

**Lo que declara la fila del 2026-10-06 sobre el libro de enero** (`HOLDOUT-EXPOSICIONES.md:43`,
rama `trabajo/reloj-invierno`): del libro `backtesting-analytics ENERO 2026.xlsx` (sha256
`ee4ade46…`), por el lector único `corpus/libro.py`, «SOLO las columnas `dateStart` y `entryPrice`
de todas sus filas» (M1, el huso por velas, y M2, las horas de entrada en UTC), y «NO se lee ninguna
otra columna -ni resultado, ni R, ni PnL, ni stop, ni objetivo-». La fila complementaria
(`:44`, el mismo día) añade, de tres días de enero (27, 29 y 30), la hora y la entrada de 9 filas
«dentro de las dos columnas ya declaradas», y cuatro fotogramas de v4 con esos días en el gráfico
de 1 minuto, con las etiquetas de entrada, stop y objetivo dibujadas. Las filas de septiembre
(`:22`, `:23`) dicen expresamente «Enero queda sin abrir». **CORRECTO lo que dice el encargo**: el
libro de enero no se ha leído entero nunca; se leyeron dos columnas de todas sus filas.

**Matiz para la decisión 1 y el punto g**: la columna `dateStart` de enero, entera, ya la leyó la
SESIÓN el 2026-10-06, cuatro días antes de ADR-0072 (2026-10-10), que pone la lectura de fechas en
manos de Aleks «una sola vez, antes del sorteo». La lectura de Aleks de hoy (punto g) es la de
ADR-0072; no es la primera vez que esa columna se lee. Enero no tiene días en ninguna partición y
su reparto dev-visto no tiene sorteo (ADR-0042 §3), así que no hay nada que quemar; se dice para que
el informe no afirme más de lo que es.

**El falso positivo de `cases/visto.py:102-111`** (`requisitos`, la condición 2 de ADR-0042 §2):

```python
fichero = Path(_fichero_del_libro(repo, sha)).name
...
exposiciones = (repo / FICHERO_EXPOSICIONES).read_text(encoding="utf-8")
...
if not fichero or fichero not in exposiciones:
    problemas.append(... "la lectura completa de su libro no esta declarada" ...)
```

Comprueba que el NOMBRE del fichero aparezca en algún sitio del documento, no que una fila declare
su lectura completa. `grep -o` del nombre en el documento: 1 aparición, en la línea 43, que es la
fila que declara SOLO dos columnas. Medido en memoria, sin escribir nada
(`anexos/ENTRADA-ENERO/falso_positivo_visto.py`):

```
hoy, sin tramo: ['2026-01: cobertura_material no le da un tramo con UN `material_sha256`: ...']
con el tramo de la fase 2 en memoria y SIN fila nueva: NINGUNO: pasa
```

Es decir: en cuanto la fase 2 escriba el tramo, `casos visto --mes 2026-01` y la ingesta darían
por declarada la lectura completa aunque la fila nueva no existiera. **Es un falso positivo
confirmado.** No es un desvío del código respecto al ADR: ADR-0042 §2 dice literalmente «(se
comprueba por el nombre del fichero)»; el defecto es el mecanismo que el propio ADR eligió, que no
distingue «nombrado» de «leído entero». No se arregla aquí (lo dice el encargo); va como propuesta
de Technical Debt. En esta rama la protección es el orden: la fila nueva (2.b) entra en el commit
del tramo y del reparto, antes de `casos visto`, como en julio.

### 0.c `scripts/ticks_spread.py`, la rejilla y `simulador_config.py`

**Cómo cuenta hoy la ventana** (`scripts/ticks_spread.py:67-85`): lee `huso_operativa`
(`Europe/Madrid`) y `ventana_inicio`/`ventana_fin` (07:00 y 15:00), y por cada tick
`local = (epoca + timedelta(milliseconds=t.instante)).astimezone(huso)`; la clave es
`local.hour` si `inicio <= local.hour < fin`, y `fuera` si no. Es la hora de PARED de Madrid, no
la de la rejilla. Ya itera `criterio.construccion` (`:77`) y exige el manifiesto de ticks de cada
mes: `buscar_manifiesto_ticks` lanza `TicksError` si falta (`src/botsito/data/ticks.py:572-573`).

**Lo que ofrece la puerta** (`src/botsito/cases/relojes.py`, reexportada sin cambios en
`src/botsito/engine/relojes.py:12-25`): `reloj_de_las_sesiones(registro)` (`:202-222`) devuelve un
`RelojSesiones` que con `reloj_sesiones = rejilla_h4` (valor de hoy) lee `anclaje_h4` (17:00
America/New_York), `sesiones_primera_vela_h4` (3) y `ventana_inicio`. Tiene dos sentidos:
`instante(dia, "HH:MM")` → minuto UTC (`:126-131`), y `lectura(minuto_utc)` → (día operativo,
minutos nominales del día) (`:183-199`). Para contar un tick por la rejilla basta
`lectura(instante_ms // 60000)` y `hora = minutos // 60`: la hora NOMINAL (07..14), la misma clave
que hoy en los meses sin desfase.

**Ningún test suyo**: `grep -rln ticks_spread tests src scripts Makefile .github` solo da el propio
script (y su `.pyc`). CORRECTO. ADR-0069 §5 (líneas 124-127) lo deja «pendiente con dueño, la rama
que baje ticks de un mes de invierno, por la puerta de `engine/relojes.py`».

**`simulador_config.py`: SÍ queda desalineado los días de desfase.** `_hora_local`
(`src/botsito/engine/simulador_config.py:59-63`) busca el spread por la hora de PARED en
`spread.huso` (`knowledge/simulador/llenado.yaml:18`, `Europe/Madrid`), y la tabla
`por_hora_local` (7..14) se midió con la hora de pared de abril y agosto, que en esos meses es la
nominal. Medido (`anexos/ENTRADA-ENERO/spread_desfase.py`): el 2026-10-22 (sin desfase) las 11
horas de 04:30Z a 14:30Z dan el mismo spread por la pared y por la rejilla; el 2026-10-27 (con
desfase) **4 de 11 difieren en 1 punto**: 05:30Z (primera hora de la ventana: pared 06 → 4, fuera
de la tabla; rejilla 07 → 5), 10:30Z (5 frente a 4), 12:30Z (4 frente a 5) y 13:30Z (hora ya fuera
de la ventana: pared 14 → 5; rejilla 15 → 4). Ningún mes de construcción (enero, abril, julio,
agosto) tiene días de desfase, así que hoy no cambia ninguna cifra; afecta a marzo (9-27) y al bot
en tiempo real la semana del 26 de octubre. No se toca (lo dice el encargo): propuesta de Technical
Debt.

### 0.d Los tests y los textos que enumeran meses

- `tests/unit/test_criterio_fidelidad.py:108`:
  `assert c.construccion == ("2026-04", "2026-07", "2026-08") and c.medida == ("2026-05",)`.
  Rompe cuando enero entre en `construccion` (fase 3). CORRECTO.
- `tests/contract/test_mes_del_material.py:252`:
  `assert sorted(materiales.values()) == ["2026-04", "2026-05", "2026-07", "2026-08"]`. CORRECTO
  que rompe, **pero no en la fase 3: en la fase 2**, porque `materiales` sale del
  `material_sha256` de `cobertura_material` (`kit/config.yaml`), y es la fase 2.c la que escribe el
  tramo de enero con su sha. Con el encargo tal cual, el commit de la fase 2 no se puede sellar.
  Julio lo resolvió igual: lo amplió en el commit del reparto (79549c7) y dejó solo
  `test_criterio_fidelidad.py:108` para el del ADR (80e7a78). Decisión 1 abajo.
- Ningún otro test que lea el repo real enumera los meses de construcción (`grep` de `"2026-07"` en
  `tests/`: el resto son repos sintéticos en `tmp_path`, o la guardia, cuyos
  `meses_legibles` ya incluyen `2026-01`, `tests/unit/test_guardia_claude.py:145,153`).
- Textos vivos que nombran la construcción: la NOTA de ADR-0043 (`docs/adr/0043-…md:31-33`, «la
  construcción es abril, julio (del 1 al 17…) y agosto»), `docs/runbooks/ARNES-MOTOR.md:8-9`
  («hoy abril, julio -del 1 al 17- y agosto de 2026»), `docs/runbooks/SESION-DE-PREGUNTAS.md:21-22`
  («abril, julio del 1 al 17 y agosto, desde ADR-0078») y la fila 0078 de `docs/adr/README.md:84`
  (el índice lleva una fila por ADR: se añade la 0079). Además
  `knowledge/cases/criterio_fidelidad.yaml:37` (la lista). `CLAUDE.md:159` dice ya «enero, abril,
  julio y agosto» como DESARROLLO, que no cambia. CORRECTO.

### 0.e La ventana de ticks: julio frente a enero, por la rejilla

Medido con `reloj_de_las_sesiones` sobre el registro (`anexos/ENTRADA-ENERO/ventana_rejilla.py`):

| Tramo | Ventana por la rejilla (UTC) | Horas UTC de la ventana | `huso_operativa` pone las 07:00 en |
|---|---|---|---|
| enero de 2026, los 22 laborables del 1 al 30 | 06:00-14:00 | 06 a 13 | 06:00Z (igual) |
| julio de 2026, los 13 laborables del 1 al 17 | 05:00-13:00 | 05 a 12 | 05:00Z (igual) |
| 9-27 de marzo de 2026 (15 laborables) | 05:00-13:00 | 05 a 12 | 06:00Z (DESFASE) |
| 26-30 de octubre de 2026 (5 laborables) | 05:00-13:00 | 05 a 12 | 06:00Z (DESFASE) |

**El manifiesto de julio** (`data/manifests/ticks/eurusd-ticks-2026-07-6e7dc7cd.yaml:116-125`)
lleva `horas_utc` 5 a 13: las 8 horas de la ventana más UNA hora después del cierre, como abril y
agosto (sus manifiestos, `:176-185` y `:172-181`). Es la convención de DN-5 (ADR-0051 §7: «las
horas 05-13 UTC»; TICKS-LLENADO.md:49-50: «la ventana 07:00-15:00 CEST más una hora»; `--horas` es
inclusivo, `src/botsito/cli.py:3279`). **Para enero, con la misma convención: `--horas 06-14`** (la
ventana 06:00-14:00Z más una hora), 9 horas por día. CORRECTO lo que dice el encargo («06-14»),
entendido como el argumento inclusivo de `--horas`, no como la ventana: la ventana de la rejilla es
06:00-14:00Z (horas 06 a 13); ADR-0051 DN-5 y ADR-0069 §5 dicen lo mismo («06:00-14:00 UTC»).

### 0.f La decisión 2 medida: el sesgo H4 de enero sin diciembre

- **Velas M1 de enero** (`data/manifests/eurusd-m1-2026-01-e37291d4.yaml`): desde `2026-01-01`,
  primera vela `2026-01-01T22:04Z`, última `2026-01-30T21:59Z`, 30.150 velas, 31 días presentes,
  huecos de fin de semana de 2880 min. CORRECTO lo del auditor del consultor. No hay dataset M1 de
  `2025-12` en `data/manifests/`.
- **Cómo calienta el motor** (`src/botsito/engine/arnes.py:194-198`): las M1 del mes anterior si
  hay dataset y si no, «el calentamiento empieza en el mes». Sin diciembre, las H4 de enero empiezan
  en la que abre el `2026-01-01T22:00Z` (17:00 Nueva York).
- **Medido** (`anexos/ENTRADA-ENERO/sesgo_enero.py`, como `dias_de_mercado`: H4 con `anclaje_h4`,
  aperturas por `reloj_de_las_sesiones`, `domain.sesgo.sesgo_h4` con `sesgo_h4_tope_velas` 60 y
  criterio `mecha`), los 21 laborables del 2 al 30 por sus dos sesiones (06:00Z y 10:00Z): **0
  INSUFICIENTE** (19 alcista, 23 bajista). El 2 de enero abre con 2 H4 cerradas (07-11) y 3
  (11-15), y el sesgo se decide mirando 1 vela en las dos; ningún día de enero mira más de 2.
- **Qué días quedan afectados.** Ninguno en el resultado: el sesgo busca hacia atrás desde la última
  H4 cerrada y se detiene en la primera ruptura; todas las de enero se deciden con pares de velas
  de enero (como mucho 2 miradas; el par más antiguo, el del 2 de enero, son las dos primeras H4
  del día de rejilla del 2, desde el 1 a las 22:00Z), así que tener diciembre no cambiaría ninguno de los 42 sesgos. Lo que sí está
  recortado es el HORIZONTE: hasta el 15 de enero (56 y 57 H4 cerradas) hay menos de las 60 que
  permite el tope; desde el 16 (62) ya no. Un día solo saldría distinto si su búsqueda agotara las
  velas de enero sin ruptura, y no pasa ninguno. Lo mismo que abril sin marzo (MOTOR-SESGO-H4.md,
  líneas 103-104: «aun así no sale ningún insuficiente»).
- **Ojo para después**: el arnés y el visor cargan el mes anterior SI EXISTE su dataset
  (`arnes.py:194-198`, `visor.py:293`). Si un día se baja el M1 de diciembre (I), enero calentará
  con él sin cambiar una línea; con lo medido, ningún sesgo cambiaría.

### 0.g La columna de fechas del libro de enero, leída por Aleks (ADR-0072)

Copiado tal cual del encargo:

> PARADA. Copia tal cual en el informe la columna de fechas del libro de enero, leída por Aleks
> hoy, una sola vez (ADR-0072): mínima 2026-01-02, máxima 2026-01-30 (vio también la hora de esas
> dos filas, y nada más). Decláralo hoy en HOLDOUT-EXPOSICIONES. Entrega el inventario y espera mi
> respuesta antes de escribir nada.

Declarado hoy en `HOLDOUT-EXPOSICIONES.md` (fila del 2026-10-13, `trabajo/entrada-enero`, fase 0),
junto con lo que leyó la sesión. El tramo 2026-01-02 a 2026-01-30 cubre 21 laborables (el 1 es
festivo y no entra; medido con el calendario del guion de 0.e).

### El encargo frente al repo (auditor-encargo, 2026-10-13)

43 afirmaciones contrastadas: 34 correctas, 2 incorrectas y 7 con matiz; 6 cosas que el repo pide y
el encargo no recoge. Solo ejecutó un recuento de `casos_reservados`/`casos_ocultos` y
`gh run view` de la CI de `main`; la guardia le bloqueó un `grep -r .` desde la raíz y lo repitió
acotado a `docs/`. Lo que importa, verificado por la sesión con su evidencia:

**Incorrectas**
- **(38) La fase 3 no puede llevar `test_mes_del_material.py:252`**: rompe en la 2.c (0.d arriba).
  Es la lección (2) de julio (`docs/runbooks/ERRORES-RECURRENTES.md:82`). Decisión 1.
- **(26) `docs/adr/README.md` no dice «construcción = abril, julio y agosto»**: es un índice, con
  una fila por ADR (`:84`, la 0078). Lo que necesita es la fila 0079, no una corrección.

**Con matiz**
- (12) MOTOR-SESGO-H4.md midió abril sin marzo ANTES de ADR-0075; desde entonces una H4 neutra con
  una sola detrás da insuficiente. Por eso 0.f se midió con el motor de hoy (0 INSUFICIENTE).
- (16) El falso positivo de `visto.py` lo prescribe ADR-0042 §2 («se comprueba por el nombre del
  fichero», `docs/adr/0042-…md:16-17`): arreglarlo pide una NOTA u otro ADR, no solo código. Y hoy
  falla antes la condición 3 (sin tramo); el falso positivo actúa desde la 2.c. Confirmado en 0.b.
- (28) «06-14»: la ventana de invierno es 06:00-14:00Z; el `--horas` análogo a julio es `06-14`
  inclusivo (una hora más que la ventana). Decisión 2.
- (30) La columna `dateStart` de enero ya la leyó la sesión el 2026-10-06, antes de ADR-0072
  (0.b). Se dice en el informe y en la fila del día.
- (31) ADR-0069 §2 y §5 nombran como puerta `engine/relojes.py`; `cases/relojes.py` es el mismo
  objeto reexportado. `scripts/` puede importar cualquiera de los dos; se importa
  `botsito.engine.relojes`, el nombre del ADR.
- (32) `ticks_spread.py` ya itera `construccion` y ya exige el manifiesto de ticks de cada mes;
  enero no puede estar en la lista en la fase 1 (entra en la 3) y sus ticks llegan en la 4.
  Decisión 3.
- (43) y **H1, el más grave**: `cargar_criterio` conserva el orden de la lista
  (`src/botsito/cases/criterio_fidelidad.py:247-251`, `_meses` devuelve `tuple(valor)`), y siete
  ficheros de tests usan `construccion[0]` con el repo real (verificado:
  `test_preparar_a21.py:424`, `test_preparar_a35.py:404,411,429`, `test_preparar_a44.py:415`,
  `test_rutas_windows.py:79,85`, `test_selector_orden_stop.py:143,182`, `test_simulacion.py:262`,
  `test_visor.py:375`; cinco de ellos llaman a `motor arnes`, dos con `--simular`). Si enero
  entra PRIMERO, en orden cronológico, el `make check` del commit de ADR-0079 corre el arnés sobre
  enero, sin casos ni ticks: contra «No corras el arnés» y contra la decisión 3 del consultor.
  Decisión 0.

**Lo que el repo pide y el encargo no recoge**
- **H2.** `tests/unit/test_huecos_motor.py:290-338` corre el sesgo H4 del motor sobre los días dev
  de TODOS los meses de construcción; con enero en la lista y sus casos ingeridos, también sobre
  enero. En julio el consultor lo aceptó y ADR-0078 lo declara (ENTRADA-JULIO.md:313;
  ADR-0078:84-86). Decisión 4.
- **H3.** R2.2 lleva `HER:34` en sus Refs (`docs/plan/HOJA-DE-RUTA.md:77`); si R2.2 pasa a HECHA y
  el heredado 34 sigue vivo (sus partes b y c van con la A), `tests/unit/test_hoja_de_ruta.py:150-153`
  falla («esta HECHA y el heredado sigue vivo»). Va a las propuestas de cierre.
- **H4.** R5.4 dice «Depende de: R2.2 (NA:X)» (`HOJA-DE-RUTA.md:172`): cuando X salga de la Next
  Action, `test_hoja_de_ruta.py:148-149` falla. Va a las propuestas de cierre.
- **H5.** Tras la fase 1, dos ADR ACTIVE dicen algo que deja de ser cierto: ADR-0069 §5
  (`:124-127`, «`scripts/ticks_spread.py` sigue contando esa ventana en `huso_operativa` …
  pendiente con dueño») y ADR-0051 DN-5 (`:98-100`, la ventana de invierno «queda PENDIENTE y
  ligada a A-42»). El precedente de julio les pone NOTA sin reescribir el cuerpo. Decisión 5.
- **H6.** `docs/runbooks/VISOR-DIAS.md:9` dice «hoy abril y agosto de 2026»: falso desde julio, y
  más con enero. Decisión 5.

### Lo que no pude medir

- Que la columna de fechas del libro dé 2026-01-02 y 2026-01-30: es lectura de Aleks (ADR-0072) y
  la sesión no abre el libro para comprobarla.
- El coste de `RelojSesiones.lectura` por tick (cada llamada recalcula `limites_del_dia`; abril,
  julio y agosto suman unos 370.000 ticks por mes): se medirá al escribir la fase 1, y si es caro,
  se cachea la apertura por día sin cambiar la puerta.
- Si los siete tests de H1 fallarían o pasarían con enero primero: no se ejecutaron (no se corre el
  arnés). Que llamarían al arnés con enero está en el código citado.

### Exposiciones del día (fase 0)

- **Aleks**, hoy, una vez (ADR-0072): la fecha mínima (2026-01-02) y la máxima (2026-01-30) de la
  columna de fechas del libro de enero, y la hora de esas dos filas; nada más.
- **La sesión**: ningún libro, ninguna imagen, ningún fotograma, ninguna transcripción. Leyó el
  registro, los manifiestos de `data/manifests/` (velas M1 de enero y ticks de abril, julio y
  agosto: cabeceras y `seleccion`), las velas M1 de enero de 2026 para el sesgo (ADR-0021 §1) y los
  repartos por RECUENTO (34 reservados, 0 de enero; por partición, sin ids).
- **El auditor**: lo mismo por recuento; ningún contenido protegido.

Declarado en `HOLDOUT-EXPOSICIONES.md`, fila del 2026-10-13 de esta rama. Ninguna partición.

## Lo que necesito que decidas

0. **El orden de la lista `construccion` (H1).** Opciones: (a) añadir enero AL FINAL,
   `["2026-04", "2026-07", "2026-08", "2026-01"]`, con el motivo en un comentario y en ADR-0079;
   (b) orden cronológico `["2026-01", "2026-04", …]` y cambiar los siete tests para que no usen
   `construccion[0]` (por ejemplo, el primer mes con casos y ticks). Recomiendo (a): ningún test
   cambia, `construccion[0]` sigue siendo abril y el commit del ADR no corre el arnés sobre enero,
   como pide la decisión 3. Coste de (b): siete ficheros de tests fuera del encargo y del contrato,
   y una regla nueva que elegir para ellos.
1. **Dónde va `test_mes_del_material.py:252` (afirmación 38).** Opciones: (a) en el commit de la
   fase 2 (tramo, exposición y reparto), como julio en 79549c7; y la fase 3 lleva solo
   `test_criterio_fidelidad.py:108`; (b) juntar las fases 2 y 3 en un commit. Recomiendo (a): cada
   commit se sella y hace una cosa, y la decisión sigue siendo anterior a cualquier corrida con
   enero. Coste de (b): un commit que mezcla el reparto con la decisión.
2. **Las horas de ticks de enero.** Opciones: (a) `--horas 06-14` (la ventana 06:00-14:00Z más una
   hora, la convención de DN-5 con la que se bajaron abril, julio y agosto, 9 horas por día); (b)
   `--horas 06-13` (solo la ventana). Recomiendo (a): el mismo criterio que los otros tres meses.
   Coste de (b): enero con una hora menos que el resto, y el percentil de la hora 14 sin enero.
3. **Qué hace la fase 1 con la lista de meses.** Opciones: (a) `ticks_spread.py` sigue iterando
   `criterio.construccion` (ya lo hace) y su error por mes sin ticks nombra el mes; el test de la
   fase 1 cubre la cuenta por la rejilla con ticks sintéticos, y la salida real con enero se corre
   DESPUÉS de la fase 4, a un anexo, sin tocar `llenado.yaml`; (b) no correrlo con datos reales en
   esta rama. Recomiendo (a): deja medido qué daría el p90 con los cuatro meses para quien decida
   rehacer `llenado.yaml`, sin cambiarlo. Coste de (b): X se cierra sin haber corrido nunca el
   script por la rejilla sobre datos reales.
4. **`test_huecos_motor` sobre enero (H2).** Opciones: (a) aceptarlo y declararlo en ADR-0079,
   como julio en ADR-0078:84-86; (b) excluir enero del test. Recomiendo (a): es un diagnóstico del
   sesgo sobre los días dev, no una medida de fidelidad ni una corrida del arnés, y lo mismo se
   aceptó para julio. Coste de (b): tocar un test fuera del contrato y que enero no tenga esa red.
5. **Las NOTAS que la fase 1 y la 3 dejan pendientes (H5, H6).** Opciones: (a) en el commit de
   ADR-0079, NOTA (sin reescribir el cuerpo) en ADR-0069 §5 y en ADR-0051 DN-5 diciendo que la
   ventana de ticks ya sale de la rejilla (rama y ADR), y `VISOR-DIAS.md:9` corregido; amplío el
   contrato con `docs/adr/0069-*`, `docs/adr/0051-*` y `docs/runbooks/VISOR-DIAS.md`; (b) dejarlo
   como propuesta para el cierre. Recomiendo (a): lo que un commit deja falso se corrige en ese
   commit (respuesta de julio, punto 8). Coste de (b): dos ADR ACTIVE diciendo algo falso hasta otra
   rama.
6. **El falso positivo de `visto.py` (0.b).** Opciones: (a) solo propuesta de Technical Debt, con la
   observación de que el mecanismo lo prescribe ADR-0042 §2 y su arreglo pide NOTA u otro ADR; (b)
   arreglarlo aquí. Recomiendo (a), que es lo que dice el encargo; en esta rama protege el orden (la
   fila completa antes de `casos visto`). Coste de (b): código y ADR fuera del encargo.
7. **El desajuste de `simulador_config.py` (0.c).** Confirmado y medido: 4 de 11 horas con 1 punto
   distinto el 2026-10-27, ninguna en un mes de construcción. Opciones: (a) propuesta de Technical
   Debt con la medida, para la rama que toque marzo o el bot en tiempo real, lo que llegue antes;
   (b) arreglarlo aquí. Recomiendo (a), que es lo que dice el encargo. Coste de (b): tocar
   `engine/`, protegido.

Espero tu respuesta a la PARADA.

## Respuesta del consultor a la PARADA (2026-10-13)

Copiada tal cual:

> Respuesta a la PARADA de trabajo/entrada-enero (consultor, 2026-10-13). Cópiala tal cual en el informe y aplícala punto por punto.
>
> 0. Orden de construccion: aceptado, enero al final: ["2026-04","2026-07","2026-08","2026-01"]. Siete ficheros de tests usan construccion[0] y cinco corren el arnés; así ninguno cambia y el commit del ADR no corre el arnés sobre enero. Que ADR-0079 diga que el orden de la lista importa y por qué.
> 1. test_mes_del_material.py:252: aceptado, en el commit de la fase 2, como en julio. test_criterio_fidelidad.py:108, en la fase 3. Es el orden en que cada uno rompe.
> 2. Ticks de enero con --horas 06-14: aceptado. Es la ventana de la rejilla más una hora, el mismo criterio que abril, julio y agosto, y lo mediste.
> 3. Fase 1: aceptado. ticks_spread.py sigue recorriendo construccion, con su test sintético del día de desfase. La corrida real con los cuatro meses va después de la fase 4, a un anexo, sin tocar llenado.yaml.
> 4. test_huecos_motor correrá el sesgo sobre enero: aceptado y declarado en ADR-0079, como con julio. Lee solo velas; no mide nada.
> 5. NOTAS en ADR-0069 §5 y ADR-0051 DN-5, y corregir VISOR-DIAS.md:9, en el commit de ADR-0079: aceptado. Amplía el contrato a esos tres ficheros. Lo que un commit deja falso se corrige en ese commit.
> 6. Falso positivo de visto.py: aceptado, solo como Technical Debt. Anota que el mecanismo por nombre lo fija ADR-0042 §2, así que arreglarlo pide una NOTA o un ADR nuevo, no solo código. En esta rama, la fila nueva de HOLDOUT-EXPOSICIONES (fase 2.b) es la que cumple de verdad la condición 2.
> 7. simulador_config.py: aceptado como Technical Debt, con la medida (2026-10-27: 4 de 11 horas, 1 punto de spread distinto). Añade a la línea que importará cuando se mida un mes con días de desfase: marzo, del 9 al 27, y octubre.
>
> Además:
> - La lectura de fechas de enero: declara que la sesión ya leyó la columna el 2026-10-06, antes de ADR-0072, y que la de Aleks de hoy es la que fija el tramo según ADR-0072. No es una exposición nueva: enero no tiene ningún día en ninguna partición.
> - Para la orden de cierre, en §8: el heredado 34 frente a R2.2 HECHA, y R5.4 sin NA:X. Propón el texto exacto de los dos cambios para que test_hoja_de_ruta.py pase.
>
> Sigue con la fase 1. Si el Makefile cambia o el clasificador niega un push, para y dame el comando con «!». Al terminar: revisor, y «Rama lista para revisión, NO cerrada».

### Cómo se aplica, punto por punto

| Punto | Dónde | Estado |
|---|---|---|
| 0 | fase 3: `construccion: ["2026-04", "2026-07", "2026-08", "2026-01"]`; ADR-0079 dice por qué importa el orden | hecho, e803b39 (§3) |
| 1 | fase 2: `test_mes_del_material.py:252`; fase 3: `test_criterio_fidelidad.py:108` | hecho, 04e9d5b y e803b39 |
| 2 | fase 4: `--horas 06-14` | hecho (§4) |
| 3 | fase 1 (§1): `ticks_spread.py` por la rejilla con su test; corrida real tras la fase 4, a un anexo | hecho, 7bc7fa3 (§1); corrida en §4 |
| 4 | fase 3: ADR-0079 lo declara | hecho, e803b39 (§3) |
| 5 | contrato ampliado en el commit de la fase 1 con `docs/adr/0069-*.md`, `docs/adr/0051-*.md` y `docs/runbooks/VISOR-DIAS.md`; las NOTAS y la corrección, en el commit de ADR-0079 | hecho, 7bc7fa3 y e803b39 |
| 6 | §8, propuesta de Technical Debt con la observación sobre ADR-0042 §2; la fila de la fase 2.b cumple la condición 2 | hecho (§8.3; fila en 04e9d5b) |
| 7 | §8, propuesta de Technical Debt con la medida y los meses en que importa | hecho (§8.3) |
| Además 1 | 0.b ya lo dice; se repite en la fila de la fase 2.b y en ADR-0079 | hecho, 04e9d5b y e803b39 |
| Además 2 | §8, texto exacto de los dos cambios de la hoja de ruta | hecho (§8.2) |

## 1. Fase 1 · X: `scripts/ticks_spread.py` por la rejilla

**El cambio** (`scripts/ticks_spread.py`):
- La hora de cada tick sale de `reloj_de_las_sesiones` (importado de `botsito.engine.relojes`, el
  nombre que da ADR-0069 §2 y §5; es el mismo objeto que `cases/relojes.py`), no de
  `astimezone(huso_operativa)`. La función nueva `clave_de_hora(reloj, inicio, fin)` lee cada tick
  con `reloj.lectura(minuto)` y devuelve la hora NOMINAL «HH» si cae en
  [`ventana_inicio`, `ventana_fin`) y `fuera` si no. La lectura se guarda por minuto: la rejilla
  se calcula una vez por minuto, no por tick (el coste que el auditor dejó sin medir; no lo he
  cronometrado: la regresión de abajo, con los dos guiones sobre 1.603.424 ticks cada uno, terminó en
  una sola llamada sin acercarse al límite de 10 minutos).
- Sigue recorriendo `criterio.construccion` y ninguna otra cosa (punto 3), y ahora comprueba ANTES
  de medir que cada mes tenga su manifiesto de ticks: si falta uno, sale con 2 nombrando el mes y
  no escribe la salida. `main` acepta la raíz del repo como argumento para que el test lo ejerza.
- La cabecera de la salida dice «horas nominales [07, 15) del reloj de las sesiones (rejilla_h4,
  ADR-0069 §5)» en lugar de «horas locales … en Europe/Madrid».

**El test** (`tests/unit/test_ticks_spread.py`, con el registro real; 6 casos en 7bc7fa3 y 7 desde
el séptimo que añadió la entrega por el hallazgo b2 del revisor, §5):
- **Rompe a propósito con un día de desfase, el 2026-10-27**: hora a hora de 04:30Z a 14:30Z, la
  rejilla da `fuera, 07, 08, … 14, fuera, fuera` y la pared de `huso_operativa` (el método de
  antes, reproducido con `RelojSesiones.de_pared`) da `fuera, fuera, 07, … 14, fuera`: la hora
  sale corrida una. El tick de las 05:30Z, la primera hora de la sesión, cae DENTRO (07) por la
  rejilla y FUERA por la pared.
- **Sin desfase dan lo mismo**: el 2026-01-15 (invierno) y el 2026-07-15 (verano), minuto a
  minuto de 03:00Z a 16:00Z, las dos claves son iguales; y la ventana abre a las 06:00Z en enero y
  a las 05:00Z en julio (el minuto anterior, `fuera`).
- Un mes de construcción sin ticks se niega nombrándolo (repo temporal con el criterio y el
  registro reales y sin manifiestos: exit 2, «2026-04 es de construccion y no tiene ticks»).
- Un test de guarda: si cambian `reloj_sesiones`, `huso_operativa` o la ventana, cae y los días de
  arriba se rehacen.

**Regresión contra `main`** (`anexos/ENTRADA-ENERO/regresion_ticks_spread.py` y `.txt`): los dos
guiones, el de `main` copiado sin cambiar una línea, sobre los ticks de construcción de hoy (abril,
julio y agosto, sin días de desfase): 51 líneas cada uno y **una sola distinta, la cabecera
VENTANA**; todas las cifras iguales. Contar por la rejilla no cambia nada de lo ya medido.

**Rehecha en clones desechables tras el revisor (a1).** Ese anexo cargaba una COPIA SUELTA del
guion de `main` en la carpeta de trabajo y le cambiaba la global `RAIZ`. Así, el `sys.path` del
guion de `main` cargaba el `src/` de la rama. Ese método no es el que pide «Ensayos aislados»
(`CLAUDE.md`, punto 1). Las cifras valían porque la rama no toca `src/`, pero el método no era el
de la regla. No consta en qué carpeta escribió sus dos salidas: fue la carpeta de trabajo de la
sesión, fuera del repo. Rehecha con la skill `comparar-con-main`:
- clones `git worktree add --detach C:/cm/main 6fb483b` y `C:/cm/rama 7bc7fa3` (el commit de la
  fase 1, con la construcción de entonces: abril, julio y agosto);
- cada uno con su `config/settings.local.toml` apuntando al `data/` real, que solo se lee:
  `cargar_ticks`, `data/ticks.py:607` en adelante, no escribe; las escrituras de ese módulo son de
  la descarga;
- en cada clon, `uv run python scripts/ticks_spread.py --salida <clon>/salida_<lado>.txt`, exit 0
  en los dos.

| Fichero | sha256 | Líneas |
|---|---|---|
| `regresion_clon_main.txt` (main) | `2a97b9f1…a694ec` | 51 |
| `regresion_clon_7bc7fa3.txt` (rama) | `1d34a181…6712ec` | 51 |
| las dos sin la línea 1 (`tail -n +2`) | `942368bf…29725b` en las dos | 50 |

`diff`: una sola línea, la 1 (VENTANA, «horas locales [07, 15) en Europe/Madrid» frente a «horas
nominales [07, 15) del reloj de las sesiones (rejilla_h4, ADR-0069 §5)»). Es lo mismo que dio el
anexo de la copia suelta. Después, `git worktree remove --force` de los dos clones (por el `.venv`
sin seguir que deja `uv run`), `git worktree prune`, y `C:\cm` vacío.

**Un dato, sin tocar nada** (punto 3 y «Qué no cambia»): con julio en la cuenta, el p90 de la hora
11 sale 4 (`regresion_ticks_spread.txt`, línea 98); `llenado.yaml` dice 5 porque se midió solo sobre
abril y agosto (su `fuente`), y así se queda. La corrida con los cuatro meses va después de la fase
4, a un anexo.

## 2. Fase 2 · enero: lectura declarada, tramo y reparto

Todo en un commit, con `Fuente: ADR-0042, ADR-0072` (ADR-0079 aún no existe), y en este orden
dentro de él:

- **2.a** `anexos/ENTRADA-ENERO/medidas_enero.py`, repetido en 7bc7fa3 (el commit sobre el que se
  escribe éste), antes de leer nada: `casos_reservados: 34 en total; en 2026-01: 0`,
  `casos_ocultos: 34 en total; en 2026-01: 0`, `meses_reservados.yaml: '2026-01' aparece 0 veces`.
- **2.b** Fila nueva en `HOLDOUT-EXPOSICIONES.md`, hoy y antes de ingerir: la lectura completa del
  libro de enero por `casos ingerir`, con el nombre del fichero (`backtesting-analytics ENERO
  2026.xlsx`) y sus cuatro columnas (`dateStart`, `side`, `entryPrice`, `initialSL`,
  `src/botsito/cases/ingesta.py:103`) de las filas de los 21 días dev, que son el libro entero. Es
  la que cumple de verdad la condición 2 de ADR-0042 §2 (punto 6 de la respuesta); la fila dice
  además que la columna de fechas ya la leyó la sesión el 2026-10-06 y que la lectura de Aleks de
  hoy es la que fija el tramo según ADR-0072, sin ser una exposición nueva («Además» 1).
- **2.c** Tramo de 2026-01 en `cobertura_material` (`knowledge/cases/kit/config.yaml`): del
  2026-01-02 al 2026-01-30, `fuente: [ADR-0042]`, `material_sha256` copiado del manifiesto del
  corpus (`knowledge/corpus/manifest.yaml:273`, `ee4ade46…ab86`), con su comentario: límite
  inferior, como abril y julio; el 1 de enero no entra.
- **`tests/contract/test_mes_del_material.py:252`** ampliado con `2026-01` en este mismo commit,
  que es donde rompe (punto 1).
- **2.d** `uv run botsito casos visto --mes 2026-01`:
  `OK: knowledge/cases/visto/2026-01/particiones.yaml: 21 dias laborables, todos `dev`, sin sorteo;
  anclado en knowledge/cases/visto/anclas.yaml`. Ancla `2026-01: particiones.yaml: 5061655b…`.
  `material_sha256` del reparto, el del libro.

## 3. Fase 3 · ADR-0079, en su propio commit

`docs/adr/0079-enero-entra-en-construccion.md`, con `Fuente: ADR-0079`. En el mismo commit:

- `knowledge/cases/criterio_fidelidad.yaml`: `construccion: ["2026-04", "2026-07", "2026-08",
  "2026-01"]`, enero AL FINAL (punto 0), con un comentario que dice por qué importa el orden.
  ADR-0079 §2 lo explica: siete ficheros de tests toman `construccion[0]`, cinco corren el arnés.
- `tests/unit/test_criterio_fidelidad.py:108`, que rompe aquí (punto 1).
- ADR-0079 dice lo que pidió el consultor: la decisión 2 (diciembre no, medida: 0 INSUFICIENTE, y
  ningún sesgo cambiaría con diciembre; horizonte recortado hasta el 15), que `llenado.yaml` sigue
  medido sobre abril y agosto, lo que cambió la fase 1, `test_huecos_motor` sobre enero (punto 4),
  la lectura de fechas de la sesión del 2026-10-06 («Además» 1) y la deuda de
  `simulador_config.py`.
- **Un matiz al punto 4**: `test_huecos_motor` toma los días del REPARTO dev-visto
  (`engine/arnes.py:dias_de_construccion`, `:142-146`), no de los casos, así que corre el sesgo H4
  sobre los 21 días de enero desde ESTE commit, antes de la ingesta (un día sin caso entra sin
  operaciones). Solo lee velas; ADR-0079 lo dice así.
- NOTAS sin reescribir el cuerpo (punto 5): ADR-0043 (la construcción), ADR-0051 DN-5 (la ventana
  de invierno ya no está pendiente) y ADR-0069 §5 (`ticks_spread.py` ya cuenta por la rejilla).
  Corregidos `ARNES-MOTOR.md:9`, `SESION-DE-PREGUNTAS.md:21` y `VISOR-DIAS.md:9`, y la fila 0079
  en el índice `docs/adr/README.md`.
- ADR-0079 sale de los bloques `ids-inexistentes` del encargo y de este informe.

## 4. Fase 4 · casos y ticks (2026-10-13)

**Casos.** Sobre e803b39 (ADR-0079 ya commiteado, y la fila 2.b de `HOLDOUT-EXPOSICIONES.md`
commiteada antes, en 04e9d5b):

`uv run botsito casos ingerir --material "corpus/Estrategia del trader/Material adicional de su operativa/backtesting-analytics ENERO 2026.xlsx" --fecha 2026-10-13`

```
INGESTA: 4 filas SIN `initialSL` no produjeron caso: una fila sin stop no es una decision completa. Se cuentan aqui para que no desaparezcan en silencio
INGESTA: 21 casos escritos de 21 dias ingeribles; 58 filas leidas; 0 pestanas de agregado abiertas
OK: knowledge/cases/dev/ con 21 casos. Commitealos con `Fuente:`
```

(Las otras líneas `INGESTA:` de la salida hablan de junio, septiembre y los días de fidelidad, que
el comando no lee: las mismas que en julio.) Los 21 casos son los 21 días del reparto dev-visto, del
2 al 30, y suman **54 operaciones** (58 filas menos las 4 sin `initialSL`; contadas en los
ficheros, `^- direccion:`). `uv run botsito casos check`: `OK: los casos de la biblioteca tienen
la forma declarada y ninguno esta reservado`.

**Ticks.** Con las horas de invierno del punto 2 (06-14 UTC: la ventana de la rejilla, 06:00-14:00Z
en enero, más una hora, §0.e) y `--solo-dias-dev`:

`uv run botsito data download-ticks --dataset eurusd-ticks-2026-01 --simbolo EURUSD --escala 100000 --desde 2026-01-01 --hasta 2026-01-31 --solo-dias-dev --horas 06-14 --pausa 2`

```
OK: data/manifests/ticks/eurusd-ticks-2026-01-1ce59681.yaml (eurusd-ticks-2026-01-1ce59681)
  672356 ticks en 21 ficheros; horas presentes 184, ausentes (404) 0, vacias 0, PERDIDAS 5; cotizaciones cruzadas 0
  SELECCION: 21 dias y horas UTC 06-14; el resto del rango no esta en este dataset
```

`uv run botsito data check-ticks --dataset eurusd-ticks-2026-01-1ce59681 --hashes`: `OK:
eurusd-ticks-2026-01-1ce59681 coincide con el disco (hashes)`.

- **Los 21 días son los del reparto dev-visto** (del 2 al 30); el 1 y el 31 de enero no entran
  porque la selección sale de `dias_de_construccion`.
- **Se perdieron 5 de 189 horas** (21 × 9), listadas en el manifiesto: **2026-01-05 10h,
  2026-01-14 07h, 2026-01-20 11h, 2026-01-23 11h y 2026-01-29 11h** UTC, perdidas tras 5 intentos
  cada una (no son 404 ni horas vacías). Las cubre el respaldo M1 del modelo de llenado con el
  spread supuesto, como las 7 de abril, las 3 de agosto y las 3 de julio.
- **Fue la segunda pasada, como en abril, agosto y julio.** La primera (el mismo comando sin
  `--pausa`, que por defecto ya es 2 s, `cli.py:3281`) dio `eurusd-ticks-2026-01-dc8e286c`, con
  **31 horas perdidas** de 189 y 569.979 ticks, verificado también con `--hashes` (OK). Se descartó
  sin commitear: comprobé que git no seguía el manifiesto (`git ls-files --error-unmatch` falla) y
  borré el manifiesto y su carpeta de `data/ticks/` antes de relanzar. La segunda reanuda por la
  caché cruda (`con_cache_horas`) y solo vuelve a pedir lo que faltaba.
- Ninguna cotización cruzada. El manifiesto es inmutable desde su commit (`CLAUDE.md`).

**La corrida de `ticks_spread.py` con los cuatro meses** (punto 3: después de la fase 4, a un anexo,
sin tocar `llenado.yaml`): `uv run python scripts/ticks_spread.py --salida
docs/validation/anexos/ENTRADA-ENERO/ticks_spread_cuatro_meses.txt`. Recorre la construcción en su
orden (`2026-04, 2026-07, 2026-08, 2026-01`), con un dataset por mes, y cuenta la ventana por la
rejilla. El p90 total por hora contra `llenado.yaml` (`spread.por_hora_local`, medido sobre abril y
agosto):

| Hora nominal | 07 | 08 | 09 | 10 | 11 | 12 | 13 | 14 | fuera |
|---|---|---|---|---|---|---|---|---|---|
| Cuatro meses (anexo) | 5 | 5 | 5 | 5 | 5 | 4 | 4 | 5 | 5 |
| `llenado.yaml` | 5 | 5 | 5 | 5 | 5 | 4 | 4 | 5 | 4 |

Iguales de 07 a 14. Solo cambia `fuera` (5 frente a los 4 de `fuera_de_ventana`). Y la hora 11, que con abril, julio y agosto salía 4 (§1), vuelve a 5 con
enero. **No he tocado `llenado.yaml`** (lo dice el encargo y lo declara ADR-0079). Si el spread
supuesto se vuelve a medir sobre los cuatro meses, es una decisión con su ADR, no de esta rama.

## 5. El test del día de desfase, con el código de `main`

Con la skill `comparar-con-main` («Para probar un test con el codigo de main»): clon desechable
`git worktree add --detach C:/cm/main main` (6fb483b), con `tests/unit/test_ticks_spread.py` de la
rama copiado dentro, y `uv run pytest tests/unit/test_ticks_spread.py -q -p no:cacheprovider` allí:

```
.FFFFF                                                                   [100%]
E       AttributeError: module 'ticks_spread' has no attribute 'clave_de_hora'
tests\unit\test_ticks_spread.py:63: AttributeError
>       assert m.clave_de_hora(reloj_de_las_sesiones(registro), inicio, fin)(tick) == "07"
E       AttributeError: module 'ticks_spread' has no attribute 'clave_de_hora'
...
>       assert m.main(["--salida", str(salida)], raiz=tmp_path) == 2
E       TypeError: main() got an unexpected keyword argument 'raiz'
FAILED tests/unit/test_ticks_spread.py::test_un_dia_de_desfase_rompe_la_hora_de_pared_y_no_la_rejilla
FAILED tests/unit/test_ticks_spread.py::test_la_primera_hora_de_la_ventana_del_dia_de_desfase
FAILED tests/unit/test_ticks_spread.py::test_sin_desfase_la_rejilla_y_la_pared_dan_lo_mismo_minuto_a_minuto[invierno]
FAILED tests/unit/test_ticks_spread.py::test_sin_desfase_la_rejilla_y_la_pared_dan_lo_mismo_minuto_a_minuto[verano]
FAILED tests/unit/test_ticks_spread.py::test_un_mes_de_construccion_sin_ticks_se_niega_nombrandolo
```

En la rama, en 490c820: `......` (6 pasan). Con `main` solo pasa el de guarda del registro.
(Con los seis de entonces; el séptimo, abajo.)

**Lo que esto demuestra y lo que no.** Con el código de `main` el test falla por ESTRUCTURA: el
guion de `main` no tiene clave de hora ni acepta la raíz. No llega a comparar horas. La prueba de
que el método de `main` corre la hora un día de desfase está DENTRO del test:
`RelojSesiones.de_pared(huso_operativa)` reproduce `astimezone(Europe/Madrid)`, que es lo que
hacía `main` (`scripts/ticks_spread.py` de 6fb483b), y el test afirma que el 2026-10-27 da
`fuera, fuera, 07, …` donde la rejilla da `fuera, 07, …`, y que el tick de las 05:30Z cae FUERA por
la pared y en la hora 07 por la rejilla. Es la medida de la fase 0
(`anexos/ENTRADA-ENERO/ventana_rejilla.txt`).

**Lo que faltaba, tras el revisor (b2).** Esos tests protegían `clave_de_hora`, no el reloj que
elige `main()`: si `main` volviera a la pared, los seis seguirían en verde. Por eso hay un séptimo,
`test_el_guion_entero_cuenta_el_dia_de_desfase_por_la_rejilla`, que corre `main` de punta a punta
en un repo temporal:
- el criterio y el registro reales, cuatro manifiestos vacíos (uno por mes de construcción), y
  `cargar_manifiesto_ticks` y `cargar_ticks` sustituidos con `monkeypatch`, así que no lee ningún
  dato;
- tres ticks sintéticos del 2026-10-27, a las 05:30Z, 12:30Z y 13:30Z, con spread 9, 2 y 1;
- exige las líneas de abril `07:00` (n 1, 9), `14:00` (n 1, 2) y `fuera` (n 1, 1), y la cabecera
  `rejilla_h4`.

**Comprobado con un mutante**, en un clon desechable de 490c820 (`C:/cm/mutante`), con el test
nuevo copiado dentro y la línea 115 del guion cambiada a
`RelojSesiones.de_pared(registro.texto("huso_operativa"))` con `sed`:

```
......F                                                                  [100%]
E         At index 0 diff: '2026-04 13:00: n 1, media 2.00, p50 2, p90 2, p99 2, max 2' != '2026-04 07:00: n 1, media 9.00, p50 9, p90 9, p99 9, max 9'
FAILED tests/unit/test_ticks_spread.py::test_el_guion_entero_cuenta_el_dia_de_desfase_por_la_rejilla
```

Con la pared, el tick de las 12:30Z cae en la hora 13 y el de las 05:30Z fuera: el test lo caza.
En la rama, `.......` (7 pasan). El clon se quitó igual que los otros (`--force` por el `.venv`;
`prune`).

El clon se quitó con `git worktree remove --force`, porque `uv run` dejó dentro su `.venv` sin
seguir (la skill pide decirlo), y después `git worktree prune`. Al terminar, `git status --short`
vacío y `git branch --list` = `main` y `trabajo/entrada-enero`, como antes. No se creó ninguna rama
ni ningún tag. (`git worktree list` enseña además un worktree desacoplado de otra sesión,
`.../2ea2c3d2-.../scratchpad/wt-ci` en e7df30b: no es de esta rama y no lo he tocado.)

## 6. Desviaciones declaradas

- **El segundo `download-ticks` lleva `--pausa 2`**, que el comando del encargo no trae. Es el
  valor por defecto (`cli.py:3281`), así que no cambia nada: lo puse explícito como en el comando de
  julio. La primera pasada usó el comando sin él.
- **Una primera pasada de ticks descartada** (31 horas perdidas), como piden el encargo y los
  precedentes (§4).
- **`ticks_spread.py` hace dos cosas además de la rejilla**: niega con exit 2 un mes de construcción
  sin manifiesto de ticks, sin escribir la salida (el encargo pide que «exija sus ticks»; el guion de
  `main` salía con un `TicksError` sin capturar, `data/ticks.py:573`, al llegar al mes que faltaba), y `main` acepta la raíz del repo para que el test lo ejerza (§1).
- **`test_mes_del_material.py` se tocó en la fase 2 y no en la 3**, como pedía la respuesta del
  consultor (punto 1), y `test_huecos_motor` corre el sesgo sobre enero desde el commit de la fase
  3, no desde la ingesta (matiz al punto 4, §3; ADR-0079 lo dice).
- **El contrato se amplió en el commit de la fase 1** con `docs/adr/0069-*.md`, `docs/adr/0051-*.md`
  y `docs/runbooks/VISOR-DIAS.md` (punto 5).
- **Los guiones de medida de la fase 0 viven en `anexos/ENTRADA-ENERO/`** con su salida, como en
  julio. Ninguno escribe en el repo.
- **La regresión de la fase 1 se hizo primero con una copia suelta del guion de `main`**, no en un
  clon desechable. No lo declaré entonces; lo vio el revisor (a1). Rehecha en clones en la
  entrega, con el mismo resultado (§1). El anexo de la copia suelta se queda como estaba, porque
  es lo que se hizo.
- **La entrega añade un test y dos anexos de comprobación** por los hallazgos del revisor: el
  séptimo test (b2, §5) y `simular_cierre.py` con su salida (b1, §8.2).
- **La guardia de Claude Code me bloqueó varias veces** por encadenar en un solo comando `git add`,
  `cat` o `git status` con `uv run` o `make`. No eran bloqueos ilegítimos: la regla es de
  `trabajo/guion-mismo-comando`. Cada vez repetí el comando partido en llamadas separadas, como la
  guardia indica. Ninguna medida dejó de hacerse por ella.

## 7. Exposiciones del día, fases 1 a 4

Las de la fase 0 están en su apartado. En las fases 1 a 4:
- **Fase 2.b** (04e9d5b), declarada hoy y antes de ingerir: la lectura completa del libro de enero
  por `casos ingerir` (`HOLDOUT-EXPOSICIONES.md`, tercera fila del 2026-10-13). La lectura se
  hizo en la fase 4: 58 filas, 4 columnas, solo días dev (§4).
- **Fase 4**: además de esa lectura, los 21 casos que escribe la ingesta (de ellos solo conté las
  operaciones, `^- direccion:`) y los ticks de enero, que son datos de mercado de días dev y no
  etiquetas. Ninguna imagen, ningún fotograma, ninguna transcripción, ningún mes reservado,
  ninguna partición. `casos check` lo confirma: «ninguno esta reservado».
- **Fases 1 y 3**: ticks de abril, julio y agosto (construcción) y el registro; nada protegido.

## 8. Propuestas para la orden de cierre

Textos exactos. La hoja de ruta (`docs/plan/`) y la Next Action los edita el cierre, no la rama
(`docs/plan/` está en `rutas_protegidas`). Comprobado contra las reglas de
`tests/unit/test_hoja_de_ruta.py` (a: todo vivo tiene su `Refs:`; b: una entrada HECHA no cita una
letra ni un heredado vivos, y una no HECHA no cita una letra muerta, en todo su bloque; c: ninguna
entrada de la Next Action depende de una letra muerta).

**8.1 Next Action** (PROJECT_STATE.md):
- **X sale, HECHA** (registro `# Next Action HECHA · X ·` en HISTORIA, como manda el ritual).
- **F**, sustituida entera: «F. Orden de trabajo: lo siguiente es T (R2.4: transcribir v11 a v14 y
  compararlos con el xlsx de julio). R2.3 (Q, agosto) espera la exportación del trader, y R3.1
  depende de R2 entera.» (R2.4 es la única entrada de R2 sin hacer que no espera a nadie: «Depende
  de: R2.1 (HECHA)».)
- **I**: «… Entra por su propia rama después de X y de renovar hacia atrás …» pasa a «… Entra por
  su propia rama después de renovar hacia atrás …» (sin X; si no, `problemas_c` falla: I dependería
  de una letra muerta).
- **Heredado 34**, sustituido: «- 34. Ticks: el deslizamiento y el swap, las ejecuciones 2 y 3
  (A).» (la parte a, la ventana de invierno, es X y queda hecha; las partes b y c siguen vivas y ya
  las cita la entrada de la demo, `HOJA-DE-RUTA.md:208`, `HER:34`).

**8.2 Hoja de ruta** (`docs/plan/HOJA-DE-RUTA.md`), los dos cambios que pide el consultor:
- **R2.2 HECHA sin el heredado 34** (`:77`): la línea de Refs pasa de
  `- **Refs:** NA:X · HER:34 · ID:ADR-0069 · ID:ADR-0051` a
  `- **Refs:** NA:X · ID:ADR-0069 · ID:ADR-0051 · ID:ADR-0079`
  en el «Qué es» (`:80`), `(carril de Aleks, NA:A).` pasa a `(carril de Aleks, R7.1).`,
  y se añade al final de la entrada, tras `- **Hecho cuando:**`:
  `- **Estado:** HECHA (`trabajo/entrada-enero`, `stable/F37p-entrada-enero`; ENTRADA-ENERO.md,
  ADR-0079): la ventana de ticks sale de la rejilla, con su test; enero es construcción del 2 al
  30, con sus ticks. Las partes b y c del heredado 34 siguen en R7.1.`
  Con eso, `HER:34` y `NA:A` siguen en el `Refs:` de la demo (R7.1, `:208`; regla a) y ya no en
  ningún punto del bloque de una entrada HECHA (regla b mira el bloque ENTERO,
  `test_hoja_de_ruta.py:141`). **Corregido tras el revisor (b1):** la primera versión de este
  texto dejaba `NA:A` en el «Qué es» y en el `Estado`, y decía que eso valía «porque A está viva».
  Es al revés: por estar viva, la regla b lo niega.
- **R5.4 sin NA:X** (`:172`): `- **Depende de:** R2.2 (NA:X) y R2.1 (HECHA) y R1.1.` pasa a
  `- **Depende de:** R2.2 (HECHA) y R2.1 (HECHA) y R1.1.` (si no, la regla b la marca: «NA:X no es
  una letra viva»).
- El tag que cito, `stable/F37p-entrada-enero`, es el siguiente de la serie (el último es
  F37o); lo fija el cierre.
- **Comprobado en memoria, sin escribir nada** (`anexos/ENTRADA-ENERO/simular_cierre.py`, que
  aplica §8.1 y §8.2 como sustituciones exactas sobre los ficheros de la rama, añade a HISTORIA
  un registro `# Next Action HECHA · X ·` y corre las funciones del test):
  `uv run python docs/validation/anexos/ENTRADA-ENERO/simular_cierre.py .` →
  `a: []`, `b: []`, `c: []`, `PROJECT_STATE simulado: 23171 bytes`
  (`anexos/ENTRADA-ENERO/simular_cierre.txt`).

**8.3 Technical Debt**, dos líneas nuevas:
- «La condición 2 de ADR-0042 §2 (la lectura COMPLETA del libro, declarada) se comprueba buscando
  el NOMBRE del fichero en HOLDOUT-EXPOSICIONES (`cases/visto.py:requisitos`): una fila que lo
  nombra sin declarar la lectura completa la da por cumplida (falso positivo medido con enero,
  ENTRADA-ENERO.md §0.b). El mecanismo por nombre lo fija ADR-0042 §2: arreglarlo pide una NOTA o
  un ADR nuevo, no solo código.»
- «`engine/simulador_config.py` busca el spread supuesto de `llenado.yaml` por la hora de PARED de
  Europe/Madrid, no por la rejilla: los días de desfase sale corrido una hora (2026-10-27: 4 de 11
  horas, 1 punto de spread distinto; ENTRADA-ENERO.md §0.c). Importará cuando se mida un mes con
  días de desfase: marzo, del 9 al 27, y octubre.»

**8.4 Tamaño de PROJECT_STATE.** Hoy, en la rama, 23.406 bytes (tope del test, 25.000). Las
propuestas suman unos +600 bytes de Technical Debt y quitan unos −250 (X, 181 bytes, y la cola de
I y del heredado 34); con el cambio de `Current Feature` y `Stable Main State` del cierre, quedaría
hacia 23,8 KB. No pasa del tope, pero el margen se queda en ~1,2 KB. Si hace falta, propongo
condensar **A** (la demo, 987 bytes, la entrada más larga de la Next Action): dejar la fecha de
cada ejecución, el script 1.1 y qué mide cada una, y remitir el resto a
`docs/runbooks/DEMO-FTMO.md`, que ya lo dice entero. (La línea 7 de la hoja de ruta cita `NA:X`
como ejemplo, fuera de las entradas: con X registrada HECHA en HISTORIA, la regla b la admite.)

## 9. El encargo, punto por punto

Los puntos de la respuesta del consultor (0 a 7 y los dos «Además») van en «Cómo se aplica, punto
por punto», tras la respuesta: los diez están hechos.

| # | Requisito del encargo | Estado | Evidencia |
|---|---|---|---|
| 1 | BASE: rama desde main 6fb483b (tag F37o, merge a4e4fa6), CI 38463152743, ninguna otra rama; skill abrir-rama | Hecho | 5be95f0; «Base, comprobada con git al abrir» |
| 2 | No cambian el motor, la spec ni los umbrales; de `criterio_fidelidad.yaml`, solo `construccion` | Hecho | `git diff --stat main...HEAD`: nada en `src/botsito/engine/`, `src/botsito/domain/` ni `knowledge/spec/`; el diff de `criterio_fidelidad.yaml` es la lista y su comentario |
| 3 | `llenado.yaml` no cambia, y se declara | Hecho | fuera del diff; ADR-0079 (Impacto) y §4 |
| 4 | Ni diciembre ni ningún mes reservado | Hecho | ningún manifiesto ni caso de 2025-12; `casos_reservados` 0 en enero (§0.a, §2.a); `casos check` OK |
| 5 | No se corre el arnés ni se mide cobertura ni precisión | Hecho | ningún `motor arnes` en la rama. Los tests de `make check` que ya corrían el arnés siguen sobre `construccion[0]` = abril (punto 0); `test_huecos_motor` lee velas de enero (punto 4) |
| 6 | Decisión 1: las tres medidas en la fase 0 | Hecho | §0.a |
| 7 | Decisión 2: diciembre no se baja; días afectados e INSUFICIENTE medidos | Hecho | §0.f, `anexos/ENTRADA-ENERO/sesgo_enero.txt`; ADR-0079, decisión 5 |
| 8 | Decisión 3: ADR-0079, el siguiente número libre | Hecho | §0; e803b39 |
| 9 | Fase 0.a: base y medidas por recuento, sin ids | Hecho | 72c7848, §0.a |
| 10 | Fase 0.b: la fila del 2026-10-06 y el falso positivo de `visto.py` | Hecho | §0.b, `falso_positivo_visto.txt` |
| 11 | Fase 0.c: `ticks_spread.py`, `reloj_de_las_sesiones`, sin test; `simulador_config.py` | Hecho | §0.c, `spread_desfase.txt` |
| 12 | Fase 0.d: tests y textos que rompen | Hecho | §0.d |
| 13 | Fase 0.e: julio 05-13 frente a enero 06-14, medido con el reloj | Hecho | §0.e, `ventana_rejilla.txt` |
| 14 | Fase 0.f: velas M1 de enero e INSUFICIENTE sin diciembre | Hecho | §0.f: 0 INSUFICIENTE |
| 15 | Fase 0.g: PARADA, columna de fechas de Aleks copiada y declarada | Hecho | §0.g; `HOLDOUT-EXPOSICIONES.md` (segunda fila del 2026-10-13) |
| 16 | Fase 1: la ventana sale de `reloj_de_las_sesiones` | Hecho | 7bc7fa3, §1 |
| 17 | Fase 1: recorre toda la construcción, julio y enero incluidos, y exige sus ticks | Hecho | §1; la corrida de §4 lee los cuatro meses |
| 18 | Fase 1: test que rompe con un día de desfase sintético | Hecho (completado en la entrega) | `test_un_dia_de_desfase_rompe_la_hora_de_pared_y_no_la_rejilla` y el de la primera hora, 2026-10-27; tras el revisor (b2), `test_el_guion_entero_cuenta_el_dia_de_desfase_por_la_rejilla`, que corre `main` y cae con el mutante de pared (§5) |
| 19 | Fase 1: test de que sin desfase dan lo mismo | Hecho | `test_sin_desfase_…[invierno]` y `[verano]` |
| 20 | Fase 1: `simulador_config.py` no se toca; Technical Debt | Hecho | fuera del diff; §8.3 |
| 21 | Fase 2.a: `casos_reservados` y `casos_ocultos` 0 en el commit en que se lee | Hecho | §2.a (sobre 7bc7fa3) |
| 22 | Fase 2.b: fila de exposición hoy y ANTES de ingerir | Hecho | fila en 04e9d5b; ingesta en 490c820 |
| 23 | Fase 2.c: tramo 2026-01-02 a 2026-01-30 con el `material_sha256` | Hecho | 04e9d5b, §2.c |
| 24 | Fase 2.d: `casos visto` y commit del reparto y su ancla antes de ingerir | Hecho | 04e9d5b, §2.d |
| 25 | Fase 2: `Fuente: ADR-0042` (o 0039/0072) | Hecho | 04e9d5b: `Fuente: ADR-0042, ADR-0072` |
| 26 | Fase 3: ADR-0079 en su propio commit, con tests, textos vivos e índice; `Fuente: ADR-0079` | Hecho de otra forma | e803b39. `test_mes_del_material` fue a la fase 2 (punto 1 de la respuesta); se añadieron las NOTAS de ADR-0069 y ADR-0051 y `VISOR-DIAS.md` (punto 5) |
| 27 | Fase 3: el ADR dice la decisión 2, `llenado.yaml` y lo que cambió la fase 1 | Hecho | ADR-0079, decisión 5 e Impacto |
| 28 | Fase 4: `casos ingerir` y `casos check` | Hecho | 490c820, §4 |
| 29 | Fase 4: ticks de invierno, `check-ticks --hashes`, horas perdidas, repetir si son muchas | Hecho | §4: 5 de 189 en la segunda pasada; la primera, 31, descartada |
| 30 | Informe: fase 0, PARADA y respuesta literal, evidencia, desviaciones y exposiciones | Hecho | §0, respuesta, §1-§7 |
| 31 | Propuestas de cierre: X y R2.2 HECHAS, F, I, Technical Debt, tamaño de PS | Hecho (corregido en la entrega) | §8; el texto de R2.2 se corrigió por el hallazgo b1 y pasa las reglas a, b y c en memoria (`simular_cierre.txt`) |
| 32 | `make check` con sello antes de cada commit; nunca `--no-verify` | Hecho | los seis commits pasaron por el hook `pre-commit`, que exige el sello del árbol estadiado |
| 33 | Makefile o push negado: parar y dar el comando con «!» | No aplica | el Makefile no cambia; no hay push (§10) |
| 34 | `fix/` solo si se toca `.claude/` o código de plataforma | No aplica | §10 |
| 35 | Skill entregar-rama, revisor con su informe pegado y foco en orden de commits, fila antes de ingerir y test de desfase | Hecho | §11: el informe del revisor tal cual y lo que se hizo con cada hallazgo |
| 36 | Terminar con «Rama lista para revisión, NO cerrada» | Hecho | Estado, en el último commit |

`uv run python scripts/contrato_rama.py`: `CONTRATO: 57 ficheros dentro del contrato de
trabajo/entrada-enero (riesgo alto, artefacto docs/validation/ENTRADA-ENERO.md, tramo 'R2', 6
comprobaciones para el revisor)`. `PROJECT_STATE.md`: 23.406 bytes (tope 25.000; §8.4).

## 10. CI de Linux

Sin CI de `fix/`: la rama no toca `.claude/` ni código que dependa de la plataforma. Así lo pide
el encargo («No hace falta fix/ salvo que toques .claude/ o código que dependa de la plataforma»).
Lo único cercano es `zoneinfo`: el test nuevo lee husos (Europe/Madrid, America/New_York) a través
de `cases/relojes.py`, que no cambia y que la CI de `main` ya ejerce (`test_cases_rejilla.py`,
`test_sesiones_rejilla_h4.py` y `test_dos_relojes.py`; run 38463152743 de 6fb483b, en verde, la
base de la rama). El test de la ruta temporal usa `tmp_path` de pytest.
Si el consultor quiere la CI de Linux de todos modos, el comando es
`git push origin trabajo/entrada-enero:refs/heads/fix/entrada-enero`.

## 11. El revisor

Lanzado con el informe terminado (salvo esta sección), sobre los seis commits y la versión en disco
del informe, con el foco del encargo. Su informe, tal cual (no cita ningún tramo no citable: 0
retiradas):

### Informe del revisor · trabajo/entrada-enero · 2026-10-13

Revisado: los seis commits sobre `main` 6fb483b (5be95f0, 72c7848, 7bc7fa3, 04e9d5b, e803b39, 490c820) y la versión SIN commitear de `docs/validation/ENTRADA-ENERO.md` que está en disco (724 líneas; `git diff --stat`: +133 −1).

#### Eje (a) · Reglas de la casa
Resumen: 0 bloquea, 1 importa, 0 menor.

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| a1 | importa | **La regresión de la fase 1 se hizo con una copia suelta del guion de `main`, no en un clon desechable.** El informe no lo declara en §6. `ticks_spread.py` escribe ficheros (`--salida`), y la regla «Ensayos aislados», punto 1, dice que un script que escribe se ensaya en un clon `git worktree` y «no con copias sueltas de ficheros». La skill `comparar-con-main` es la vía para una regresión contra `main`, y la rama sí la usó en §5. Hay además un efecto lateral: el anexo cambia `viejo.RAIZ = raiz`, así que el `sys.path.insert(0, RAIZ/"src")` del guion de `main` cargó el `src/` de la RAMA, no el de `main`. La comparación solo vale porque la rama no toca `src/`. No puedo enseñar dónde escribió (la carpeta de salida no consta). Por eso lo pongo en importa y no en bloquea, aunque una lectura literal de la regla daría bloquea. | `docs/validation/anexos/ENTRADA-ENERO/regresion_ticks_spread.py:3-4` («copiado con `git show main:scripts/ticks_spread.py` a la carpeta de trabajo») y `:28-29` (`viejo = cargar(...)`, `viejo.RAIZ = raiz`). `CLAUDE.md`, «Ensayos aislados», punto 1. `git diff --name-status main...HEAD -- src` sale vacío, y por eso las cifras siguen valiendo. |

Comprobado sin hallazgos:
- **Contrato.** `uv run python scripts/contrato_rama.py` → `CONTRATO: 57 ficheros dentro del contrato de trabajo/entrada-enero (riesgo alto, artefacto docs/validation/ENTRADA-ENERO.md, tramo 'R2', 6 comprobaciones para el revisor)`, exit 0.
- **Comprobaciones del contrato que no escriben:**
  - `uv run pytest tests/unit/test_ticks_spread.py -q -p no:cacheprovider` → `......`, exit 0.
  - `uv run botsito casos check` → `OK: los casos de la biblioteca tienen la forma declarada y ninguno esta reservado`.
  - `uv run botsito data check-ticks --dataset eurusd-ticks-2026-01-1ce59681 --hashes` → `OK: ... coincide con el disco (hashes)`.
  - `uv run botsito knowledge validate` (a la pantalla, sin redirigir al log) → exit 0. Todas las líneas son OK o los AVISO conocidos; `4 repartos dev-visto`, `8 manifiestos de datos validos, historial intacto`.
- **`make check`, por su log.** `make-check.log` (21:54): `2621 passed`, `SELLO: make check en verde sobre el arbol 99ef679935469d1b8c19d6d68a1dcd9f407e5843`, `PICO DE MEMORIA ... 294 MiB`. `git rev-parse 490c820^{tree}` = 99ef679…, el mismo árbol. El informe modificado en disco necesitará otro `make check` antes del último commit.
- **Trailers `Fuente:`.** Los tres commits que tocan `knowledge/cases/` (`git log --format='%h' main..HEAD -- knowledge/spec knowledge/cases` → 490c820, e803b39, 04e9d5b) llevan `Fuente:` en el cuerpo:
  - 04e9d5b: `ADR-0042, ADR-0072`;
  - e803b39: `ADR-0079`;
  - 490c820: `ADR-0079, ADR-0042, ADR-0051`.

  Los cuatro ADR existen en `docs/adr/`. 5be95f0, 72c7848 y 7bc7fa3 no tocan ni spec ni cases.
- **Holdout y material.**
  - `git diff --name-status main...HEAD` sobre evidence, feedback, corpus, spec, holdout, `meses_reservados.yaml`, `src`, `.claude` y `Makefile`: solo `A data/manifests/ticks/eurusd-ticks-2026-01-1ce59681.yaml`.
  - Las filas del día en `HOLDOUT-EXPOSICIONES.md` (fase 0 y fase 2.b) solo añaden líneas (numstat 2/0).
  - Repetí `medidas_enero.py` en HEAD: `casos_reservados: 34 en total; en 2026-01: 0`, `casos_ocultos: ... en 2026-01: 0`, `meses_reservados.yaml: '2026-01' aparece 0 veces`.
- **Regímenes de cambio.** HISTORIA solo crece (+186/−0, Archivo 32). Ningún registro de feedback ni item de evidencia nuevo. `libros.yaml` no se toca.
- **Ambigüedades:** sin cambios.
- **ADR.** ADR-0079 tiene `## Estado` = `ACTIVE`. ADR-0043, 0051 y 0069 llevan NOTAS solo añadidas (3/0, 5/0, 5/0) y el cuerpo no cambia.
- **Informes cerrados:** ninguno se toca.
- **Tres guardias de una `cita`:** no aplica (la spec no se toca).
- **Citas del informe contra su fuente, todas sostienen lo que dicen:**
  - `data/ticks.py:572-573` (`raise TicksError`);
  - `cli.py:3279` (`--horas` «inclusivas») y `:3281` (`--pausa` por defecto 2.0);
  - `cases/ingesta.py:103` (las cuatro `COLUMNAS`);
  - `engine/arnes.py:142-146` (los días salen del reparto) y `:194-198` (sin el mes anterior, el calentamiento empieza en el mes);
  - `HOLDOUT-EXPOSICIONES.md:43` en `main` («SOLO las columnas `dateStart` y `entryPrice`», «NO se lee ninguna otra columna»);
  - `knowledge/corpus/manifest.yaml:273` (sha `ee4ade46…ab86`).
- **Afirmaciones medidas, contra sus anexos:**
  - p90 de los cuatro meses (`ticks_spread_cuatro_meses.txt`) frente a `llenado.yaml:19-28`;
  - `11: 4` en la línea 98 de `regresion_ticks_spread.txt`;
  - 5/7/3/3 horas perdidas (enero, abril, julio, agosto) en sus manifiestos;
  - 54 operaciones (Grep `^- direccion:` → 54 en 21 ficheros);
  - 21 días `dev` y el ancla `5061655b…`, igual a `git rev-parse HEAD:knowledge/cases/visto/2026-01/particiones.yaml`;
  - de 55 a 76 días dev (21+13+21+21);
  - `PROJECT_STATE.md` en 23.406 bytes (`wc -c`).
- **Evidencia nueva (punto 10):** ninguna.

#### Eje (b) · Encargo
Resumen: 1 bloquea, 1 importa, 1 menor. Requisitos: 39 hechos, 3 parciales, 1 no hecho (todavía, es la entrega) y 1 hecho de otra forma (declarado).

**Lo que pediste mirar en especial:**

1. **Orden de los commits: correcto.**
   - Sigue el de julio (`ENTRADA-JULIO.md:254-260`, decisión 5; los commits de julio fueron e2d2430 → 10002d9 → 79549c7 reparto → 80e7a78 ADR → e959c88 casos+ticks). Enero: 72c7848 PARADA → 7bc7fa3 fase 1 → 04e9d5b lectura/tramo/reparto/ancla → e803b39 ADR-0079 → 490c820 casos+ticks.
   - `test_mes_del_material.py` va en 04e9d5b y `test_criterio_fidelidad.py` en e803b39 (`git log --name-status`).
   - ADR-0079 tiene su propio commit.
   - El reparto y el ancla son anteriores a la ingesta.
   - Las `Fuente:` son correctas (eje a).
2. **La fila 2.b va antes de la ingesta: correcto.**
   - La fila de la lectura completa entra en 04e9d5b (`git show 04e9d5b -- docs/validation/HOLDOUT-EXPOSICIONES.md`: una línea `+`, con `backtesting-analytics ENERO 2026.xlsx`, `leido ENTERO` y las cuatro columnas). 04e9d5b es de las 17:36:56 −0500.
   - Los casos los trae 490c820, y sus ficheros tienen mtime 17:59:17, 9 s después de e803b39 (17:59:08). El manifiesto de ticks dice `generado_por: e803b39`.
   - Dentro de la fase 2, los mtimes dan el orden fila (17:15:34) → tramo (17:15:43) → test (17:15:49) → `casos visto` (17:15:55). La fila se escribió antes de que `casos visto` comprobara la condición 2.
3. **El test del día de desfase: rompe de verdad, con un matiz (b2).**
   - `RelojSesiones.de_pared` lee igual que el método de `main` (`cases/relojes.py:185-187`, `astimezone(zona)` y `hour*60+minute`).
   - Recalculé el método de `main` para el 2026-10-27, de 04:30Z a 14:30Z: horas de Madrid `[5, 6, 7, …, 15]`, es decir `fuera, fuera, 07…14, fuera`. Es exactamente lo que afirma el test en `:84`.
   - La rejilla abre a las 05:00Z (`ventana_rejilla.txt:69`), lo que afirma `:83`. Sin desfase (enero y julio) los dos coinciden minuto a minuto (`:100-119`).
   - §5 dice la verdad sobre `main`: allí falla por ESTRUCTURA (no existe `clave_de_hora` ni el parámetro `raiz`), no comparando horas.

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 1 | BASE y skill abrir-rama (encargo, contrato, Archivo) | Hecho | 5be95f0: A contrato.yaml, A encargo, M HISTORIA (Archivo 32) |
| 2 | Ni motor ni spec ni umbrales; solo `construccion` | Hecho | diff vacío en `src`/`knowledge/spec`; `criterio_fidelidad.yaml`: solo la lista y su comentario |
| 3 | `llenado.yaml` no cambia, y se declara | Hecho | fuera del diff; ADR-0079:107-110 |
| 4 | Ni diciembre ni meses reservados | Hecho | ningún manifiesto de 2025-12; recuento 0 en HEAD |
| 5 | No se corre el arnés ni se mide cobertura o precisión | Hecho (por lo que se ve) | ninguna salida del arnés en la rama; los tests siguen en `construccion[0]` = abril (`criterio_fidelidad.yaml`, enero al final) |
| 6 | Decisión 1: las tres medidas | Hecho | §0.a; repetidas por mí en HEAD |
| 7 | Decisión 2: días afectados e INSUFICIENTE | Hecho | `sesgo_enero.txt:26-27` (`INSUFICIENTE: 0`) |
| 8 | Decisión 3: 0079 es el siguiente libre | Hecho | §0.a; `docs/adr/0079-…` |
| 9-15 | Fase 0.a a 0.g | Hecho | §0.a-§0.g; anexos de 72c7848; fila de la fase 0 en 72c7848 |
| 16 | F1: la ventana sale de `reloj_de_las_sesiones` | Hecho | `scripts/ticks_spread.py:115` |
| 17 | F1: recorre la construcción y exige los ticks | Hecho | `ticks_spread.py:105-112`; anexo, líneas 2-6 (cuatro DATASET) |
| 18 | F1: un test que rompa con el día de desfase | Parcial | ver b2 |
| 19 | F1: sin desfase dan lo mismo | Hecho | `test_ticks_spread.py:100-119` |
| 20 | F1: `simulador_config.py` no se toca; deuda | Hecho | fuera del diff; §8.3 |
| 21 | F2.a: recuento 0 en el commit en que se lee | Hecho | §2.a (sobre 7bc7fa3; no se guardó la salida de esa repetición: la repetí yo en HEAD) |
| 22 | F2.b: fila hoy y antes de ingerir, con el nombre y la lectura completa | Hecho | ver el punto 2 de arriba |
| 23 | F2.c: tramo del 02 al 30 con el `material_sha256` | Hecho | `kit/config.yaml` (diff); `manifest.yaml:273` |
| 24 | F2.d: `casos visto`; reparto y ancla antes de ingerir | Hecho | 04e9d5b; el ancla coincide con el blob |
| 25 | F2: `Fuente: ADR-0042/0072` | Hecho | cuerpo de 04e9d5b |
| 26 | F3: ADR en su propio commit, con tests, textos, índice y `Fuente: ADR-0079` | Hecho de otra forma (declarado en §9 #26) | e803b39; `test_mes_del_material` fue a la fase 2 por el punto 1 de la respuesta |
| 27 | F3: el ADR dice la decisión 2, lo de `llenado.yaml` y lo que cambió la fase 1 | Hecho | ADR-0079:39-47, 93-110 |
| 28 | F4: `casos ingerir` y `casos check` | Hecho | 490c820; `casos check` OK, repetido |
| 29 | F4: ticks `--horas 06-14`, `--hashes` y horas perdidas | Hecho | manifiesto: `horas_utc` del 6 al 14, `perdidas` 5, `presentes: 184`; `check-ticks` OK, repetido |
| 30 | Informe: PARADA, respuesta literal, desviaciones, exposiciones | Hecho | §0-§7; la respuesta es idéntica en encargo e informe (`diff` → IGUALES) |
| 31 | Propuestas de cierre (X, R2.2, F, I, Technical Debt, tamaño de PS) | Parcial | el texto de R2.2 no deja pasar el test (b1) |
| 32 | `make check` sellado antes de cada commit | Hecho | log: el árbol del sello es el de 490c820 |
| 33 | Resp. 0: enero al final, y el ADR dice por qué | Hecho | `criterio_fidelidad.yaml` (comentario); ADR-0079:19-27 |
| 34 | Resp. 1: el orden de los dos tests | Hecho | 04e9d5b / e803b39 |
| 35 | Resp. 2: `--horas 06-14` | Hecho | manifiesto, `horas_utc` |
| 36 | Resp. 3: corrida con los cuatro meses, a un anexo, sin tocar `llenado.yaml` | Hecho | `ticks_spread_cuatro_meses.txt` (490c820) |
| 37 | Resp. 4: `test_huecos_motor` declarado | Hecho | ADR-0079:101-104 |
| 38 | Resp. 5: NOTAS, VISOR-DIAS y contrato ampliado | Hecho | contrato en 7bc7fa3; NOTAS en e803b39 |
| 39 | Resp. 6: deuda de `visto.py` con ADR-0042 §2 | Hecho | §8.3 |
| 40 | Resp. 7: deuda de `simulador_config` con la medida, marzo del 9 al 27 y octubre | Hecho | §8.3 |
| 41 | Además 1: la lectura de fechas de 10-06 frente a la de Aleks | Hecho | fila 2.b; ADR-0079 §4 |
| 42 | Además 2: texto exacto de R2.2 y R5.4 para que `test_hoja_de_ruta.py` pase | Parcial | b1 |
| 43 | Revisor pegado y «Rama lista para revisión, NO cerrada» | No hecho (todavía; es este paso) | Estado: «EN CURSO: entrega; falta el revisor (§11)» |
| 44 | E5: «El encargo, punto por punto» | Hecho | §9 |

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| b1 | **bloquea** | **El texto exacto que §8.2 propone para R2.2 hace fallar `test_hoja_de_ruta.py`, y la respuesta pedía expresamente el texto con el que pasa.** La regla b mira el bloque ENTERO de una entrada HECHA, y el bloque de R2.2 cita `NA:A`, una letra viva, dos veces: ya en su «Qué es» (`HOJA-DE-RUTA.md`, línea siguiente a `:77`: «(carril de Aleks, NA:A)») y otra en el `Estado:` propuesto («…siguen en el carril de Aleks (NA:A).»). Además, el «OJO» de §8.2 afirma lo contrario: «sigue siendo válida, porque A está viva». Es justo al revés: por estar viva, rompe la regla b que el propio §8 enuncia («una entrada HECHA no cita una letra ni un heredado vivos … en todo su bloque»). | Simulación en memoria, sin escribir nada: las funciones del test sobre la hoja y PROJECT_STATE de la rama con los cambios de §8.1 y §8.2 aplicados (X fuera, el 34 nuevo, I sin X, el Refs y el Estado de R2.2, R5.4, y X HECHA en HISTORIA) dan `a: []`, `c: []` y `b: ['R2 «R2.2 · Enero cuenta: los ticks de invierno por la rejilla»: NA:A esta HECHA y la letra sigue viva']`. `tests/unit/test_hoja_de_ruta.py:143-145` (la regla) y `:141` (`referencias(bloque)`, el bloque entero). |
| b2 | importa | **Ningún test ejerce la elección de reloj que hace `main()`.** Si la línea `reloj = reloj_de_las_sesiones(registro)` volviera a la pared (`RelojSesiones.de_pared(huso_operativa)`), los 6 tests seguirían en verde. Los tests de desfase prueban que `clave_de_hora` da horas distintas según el reloj que se le pasa, y ese reloj lo pone el propio test. La única llamada a `main()` (el mes sin ticks) sale antes de construir el reloj. §1, §9 #18 y la NOTA de ADR-0069 («lo rompe a propósito») dicen más de lo que el test cubre: el test protege la función, no el guion. | `tests/unit/test_ticks_spread.py:131`, la única llamada a `m.main` (Grep en `tests/`). `scripts/ticks_spread.py:112` (`return 2`) va antes de `:115` (`reloj = reloj_de_las_sesiones(registro)`). Las claves de los dos relojes se construyen en el test: `:80-81`, `:95-97`, `:111-112`. |
| b3 | menor | En §9, los requisitos #35 («revisor con su informe pegado») y #36 («Terminar con “Rama lista…”») van como «Hecho», pero §11 todavía no existe y el Estado dice «EN CURSO». Hay que dejarlos al día al pegar este informe. | `ENTRADA-ENERO.md:703-704` frente a `:721-723` |

Lo que la rama hace y el encargo no pide, y está justificado en el informe:
- `main(argv, raiz=…)` y la salida con 2 si falta un mes (§6).
- El anexo de regresión de la fase 1 (§1). Su método es el hallazgo a1.
- La línea de tests de PROJECT_STATE (1529 → 1534, cinco funciones nuevas).

Lo que el encargo dice que no se toca, comprobado con el diff: el motor, la spec, `llenado.yaml`, `simulador_config.py`, el Makefile y `.claude/` no cambian.

#### Lo que no pude comprobar
- **Las comprobaciones que escriben.** `make check` no lo ejecuté: uso `make-check.log` y que el árbol del sello coincide con el de 490c820. `knowledge validate > knowledge-validate.log` lo ejecuté sin redirigir. `git hash-object` y `git worktree list` los bloqueó `solo_lectura.py`: los sustituí por `git rev-parse HEAD:<ruta>` y por `ls .git/worktrees` (solo `wt-ci`, de otra sesión, como dice §5). `git tag --list` también lo bloqueó: `git for-each-ref` da solo `main` y `trabajo/entrada-enero`, y ningún `stable/F37p*`.
- **Que no se corrió `motor arnes`.** Es una ausencia: no hay salida suya en la rama, pero no puedo probar que no se ejecutó.
- **La columna de fechas de Aleks** (mínima 2026-01-02, máxima 2026-01-30) y **que las filas de los 21 días dev sean el libro entero**: no abro el xlsx. Las 58 filas leídas y las 4 sin `initialSL` son la salida de la ingesta que cita el informe.
- **Dónde escribió la regresión de la fase 1** (a1): el anexo recibe la carpeta de salida por argumento y el informe no dice cuál fue.
- **La hora a la que llegó la respuesta del consultor** frente al inicio de la fase 1. `scripts/ticks_spread.py` tiene mtime 16:52, nueve minutos después de 72c7848 (16:43). La respuesta solo entra en git con 7bc7fa3.
- **El orden dentro de 04e9d5b** solo lo puedo apoyar en los mtimes, no en git.

#### Comandos ejecutados
1. `git branch --show-current; git merge-base main HEAD; git log --format='%h %s' main..HEAD; git status --short; git diff --stat main...HEAD`
2. Read `docs/encargos/trabajo-entrada-enero.md`, `contrato.yaml`, `docs/validation/ENTRADA-ENERO.md` (en dos tramos)
3. `uv run python scripts/contrato_rama.py`
4. `uv run pytest tests/unit/test_ticks_spread.py -q -p no:cacheprovider`
5. `git log --format='=== %h %ad %s%n%b' --date=iso main..HEAD`
6. (`for c in …; git show --name-status` → lo bloqueó la guardia) `git log --name-status --format='=== %h %s' main..HEAD`
7. `git diff main...HEAD -- PROJECT_STATE.md knowledge/cases/kit/config.yaml knowledge/cases/criterio_fidelidad.yaml knowledge/cases/visto/anclas.yaml tests/contract/test_mes_del_material.py tests/unit/test_criterio_fidelidad.py docs/validation/HOLDOUT-EXPOSICIONES.md`
8. `git show --format= 04e9d5b -- docs/validation/HOLDOUT-EXPOSICIONES.md | cut -c1-300`; lo mismo para 72c7848
9. `stat -c '%y %n'` de los casos de enero, del manifiesto de ticks, de `particiones.yaml` y del anexo; después, de `config.yaml`, HOLDOUT, `anclas.yaml`, `test_mes_del_material.py`, `ticks_spread.py`, `test_ticks_spread.py`, `criterio_fidelidad.yaml` y ADR-0079
10. `sed -n 60,140p src/botsito/cases/visto.py`
11. `git diff main...HEAD -- scripts/ticks_spread.py`; Read `tests/unit/test_ticks_spread.py`
12. Grep y Read de `src/botsito/cases/relojes.py` (líneas 40-224)
13. Read `docs/validation/anexos/ENTRADA-ENERO/ventana_rejilla.txt`
14. `uv run python -c` con la hora de Madrid por `astimezone`, del 2026-10-27 de 04:30Z a 14:30Z
15. Grep de la decisión 5 en `ENTRADA-JULIO.md`; `git log --format='%h %s' a4e4fa6^1..a4e4fa6^2`
16. `git log --format='%h' main..HEAD -- knowledge/spec knowledge/cases`; `ls docs/adr | grep -E '^00(42|51|72|79)-'`
17. Read `docs/adr/0079-enero-entra-en-construccion.md`
18. `cat knowledge/cases/visto/2026-01/particiones.yaml; ls knowledge/cases/visto/`
19. (`git hash-object` → lo bloqueó `solo_lectura`) `grep -c ": dev$"` de los cuatro repartos; `git rev-parse HEAD:knowledge/cases/visto/2026-01/particiones.yaml`; Grep de `ee4ade46` en `knowledge/corpus/manifest.yaml`
20. Grep de `^- direccion:` en los casos de enero; Read de `caso-eurusd-2026-01-02.yaml`
21. grep y Read del manifiesto `eurusd-ticks-2026-01-1ce59681.yaml`
22. `uv run botsito casos check`
23. `uv run botsito data check-ticks --dataset eurusd-ticks-2026-01-1ce59681 --hashes`
24. `uv run botsito knowledge validate 2>&1 | tail -15`
25. `ls -la make-check.log`; grep de SELLO, PICO, passed y failed; `git rev-parse "490c820^{tree}"`; `sed -n 60,100p make-check.log`
26. `git diff main...HEAD` de las NOTAS de ADR-0043, 0051 y 0069, del README de ADR y de los runbooks ARNES-MOTOR, SESION-DE-PREGUNTAS y VISOR-DIAS
27. head y tail de `ticks_spread_cuatro_meses.txt`; `sed` de `regresion_ticks_spread.txt`; grep de `llenado.yaml`
28. Read de `regresion_ticks_spread.py`; grep en `.claude/skills/comparar-con-main/SKILL.md`; Grep de `git show main:scripts` en `docs/validation`
29. Read de `medidas_enero.py`; `uv run python docs/validation/anexos/ENTRADA-ENERO/medidas_enero.py "C:/Users/USER/Desktop/Bot v3"`
30. `git show main:scripts/ticks_spread.py | sed -n 67,85p`; `sed` de `data/ticks.py:570-574`, `cli.py:3276-3283`, `cases/ingesta.py:100-105` y `engine/arnes.py:140-147,192-199`
31. `git diff --numstat main...HEAD` de HISTORIA, HOLDOUT y `docs/adr/`; grep de líneas borradas en HISTORIA (0)
32. `diff <(sed -n 81,96p encargo) <(sed -n 346,361p informe)` → IGUALES
33. `git diff 5be95f0 HEAD -- docs/encargos/trabajo-entrada-enero.md`
34. `sed` de `HOJA-DE-RUTA.md:70-80,168-174`; grep de `HER:34` y `NA:X`
35. grep y Read de `tests/unit/test_hoja_de_ruta.py` (líneas 41-58, 60-169)
36. `uv run python -c`: referencias del bloque R2.2 y si A está viva
37. `uv run python -c`: simulación en memoria de §8.1 y §8.2 contra `problemas_a`, `problemas_b` y `problemas_c`
38. `uv run python -c`: el cambio de I contra `problemas_c`
39. grep de las letras F, I, T, Q y A en PROJECT_STATE; grep de las entradas y dependencias de la hoja
40. `wc -c PROJECT_STATE.md`; `git diff --stat` del informe en disco
41. `git diff --name-status main...HEAD` sobre las rutas de régimen protegido
42. Grep de bucles sobre `construccion` en `tests/`; Read de `tests/unit/test_rutas_windows.py:50-94`
43. Grep de `ticks_spread|m\.main\(` en `tests/`; Grep de `return 2|reloj =|def main|def clave_de_hora` en `scripts/ticks_spread.py`
44. grep de los manifiestos de ticks de abril, julio y agosto (horas perdidas)
45. (`git worktree list` y `git tag --list` → los bloqueó `solo_lectura`) `git for-each-ref --format='%(refname)' refs/heads refs/tags/stable/F37p; ls .git/worktrees`

Ficheros clave: `C:\Users\USER\Desktop\Bot v3\docs\validation\ENTRADA-ENERO.md` (§8.2 y §9), `C:\Users\USER\Desktop\Bot v3\tests\unit\test_ticks_spread.py`, `C:\Users\USER\Desktop\Bot v3\scripts\ticks_spread.py`, `C:\Users\USER\Desktop\Bot v3\docs\validation\anexos\ENTRADA-ENERO\regresion_ticks_spread.py`, `C:\Users\USER\Desktop\Bot v3\docs\plan\HOJA-DE-RUTA.md` y `C:\Users\USER\Desktop\Bot v3\tests\unit\test_hoja_de_ruta.py`.

### Lo que se hizo con los hallazgos del revisor

| # | Gravedad | Qué se hizo |
|---|---|---|
| b1 | bloquea | **Arreglado.** §8.2 propone ahora quitar `NA:A` del bloque entero de R2.2: el «Qué es» dice `(carril de Aleks, R7.1)` y el `Estado` dice «siguen en R7.1». `NA:A` y `HER:34` quedan en el `Refs:` de R7.1. Retirado el «OJO», que afirmaba lo contrario de la regla. Comprobado en memoria con las funciones del test: `a: []`, `b: []`, `c: []` (`anexos/ENTRADA-ENERO/simular_cierre.py` y `.txt`). |
| b2 | importa | **Arreglado.** Test nuevo, `test_el_guion_entero_cuenta_el_dia_de_desfase_por_la_rejilla`, que corre `main` de punta a punta con tres ticks sintéticos del 2026-10-27. Comprobado con un mutante de pared en un clon desechable: cae, con `13:00` donde la rejilla da `07:00` (§5). Con él, la NOTA de ADR-0069 («lo rompe a propósito») y §1 dicen lo que el test cubre; no las reescribo. |
| a1 | importa | **Arreglado y declarado.** La regresión de la fase 1 está rehecha en dos clones `--detach` (main 6fb483b y 7bc7fa3) con la skill `comparar-con-main`: 51 líneas cada uno, solo la cabecera distinta, y el resto con el mismo sha256 en los dos lados (§1; `regresion_clon_main.txt` y `regresion_clon_7bc7fa3.txt`). §6 declara el método de la primera. El anexo viejo se queda, porque es lo que se hizo. |
| b3 | menor | **Arreglado.** §9 #35 y #36 al día; Estado final abajo. |

## Estado

TERMINADA en la rama, con 7 commits sellados: fases 0 a 4 y la entrega con los arreglos del
revisor. Pendiente de la revisión del consultor y de la orden de cierre de Aleks (§8 tiene los
textos para el commit del contrato).

Rama lista para revisión, NO cerrada.
