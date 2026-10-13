# ENTRADA-ENERO · X (los ticks por la rejilla) y enero de 2026 entra en construcción (R2.2)

Rama `trabajo/entrada-enero`, abierta el 2026-10-13 desde `main` en 6fb483b (commit de estado
sobre el merge a4e4fa6, tag `stable/F37o-entrada-julio`). Encargo:
`docs/encargos/trabajo-entrada-enero.md`. Tramo: R2 (R2.2 de `docs/plan/HOJA-DE-RUTA.md`; X de
la Next Action).

(Hasta que exista, ADR-0079 va declarado aquí en un bloque `ids-inexistentes`, como exige
`knowledge validate`; sale con el commit de la fase 3, que lo crea.)

```ids-inexistentes
ADR-0079 — el ADR de la fase 3 que el encargo manda escribir (enero entra en construcción); no existe hasta su commit
```

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
| 0 | fase 3: `construccion: ["2026-04", "2026-07", "2026-08", "2026-01"]`; ADR-0079 dice por qué importa el orden | en su fase |
| 1 | fase 2: `test_mes_del_material.py:252`; fase 3: `test_criterio_fidelidad.py:108` | en su fase |
| 2 | fase 4: `--horas 06-14` | en su fase |
| 3 | fase 1 (§1): `ticks_spread.py` por la rejilla con su test; corrida real tras la fase 4, a un anexo | §1 |
| 4 | fase 3: ADR-0079 lo declara | en su fase |
| 5 | contrato ampliado en el commit de la fase 1 con `docs/adr/0069-*.md`, `docs/adr/0051-*.md` y `docs/runbooks/VISOR-DIAS.md`; las NOTAS y la corrección, en el commit de ADR-0079 | contrato hecho; resto en su fase |
| 6 | §8, propuesta de Technical Debt con la observación sobre ADR-0042 §2; la fila de la fase 2.b cumple la condición 2 | en su fase |
| 7 | §8, propuesta de Technical Debt con la medida y los meses en que importa | en su fase |
| Además 1 | 0.b ya lo dice; se repite en la fila de la fase 2.b y en ADR-0079 | en su fase |
| Además 2 | §8, texto exacto de los dos cambios de la hoja de ruta | en su fase |

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

**El test** (`tests/unit/test_ticks_spread.py`, 6 casos, con el registro real):
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

## Estado

EN CURSO: fases 1 y 2 hechas; sigue la fase 3 (ADR-0079).
