# DIAGNOSTICO-PREMISA · La premisa con costes, pre-registrada antes de que llegue, y dos diagnósticos de construcción (R4.7, entrada F)

> Informe de la rama. La fase 0 (skill fase-cero) está en §0; los controles y las medidas, en §1 a §5.

Rama `trabajo/diagnostico-premisa`, abierta el 2026-11-24 desde `main` en 76ca9996 (commit de
estado sobre el merge 7a3087e9 del tag `stable/F39m-puente-techo`). Encargo:
`docs/encargos/trabajo-diagnostico-premisa.md`. Tramo: R4 (R4.7 de `docs/plan/HOJA-DE-RUTA.md`, lo
que la salida C de ADR-0098 pide antes de seguir; la F de la Next Action). El ADR de la premisa lo
escribe la fase P, con el fichero que trae Aleks. Tag previsto: `stable/F39n-diagnostico-premisa`
(no existe ni en local ni en origin: `git tag -l "stable/F39n*"` y `git ls-remote --tags origin
"stable/F39n*"` vacíos).

## Base comprobada (abrir-rama, paso 1)

- `git rev-parse HEAD main origin/main` (tras `git fetch --prune origin`):
  `76ca9996c20c0f1aeede10472a5abeafc1cac7f5` tres veces; `git status --short` vacío.
- `git rev-parse "stable/F39m-puente-techo^{commit}"` = `7a3087e94d524232190eda90f58a4bcedc328bde`
  = `main^1` (el merge); en origin, `git ls-remote --tags origin "stable/F39m*"` da `81cf0884…` (el
  objeto del tag anotado) y `7a3087e9…` (`^{}`). Es el último `- Tag: ` de HISTORIA (línea 20958).
- CI de `main`: `gh run view 45490418025 --json …` (suelto, sin guion) → `name: ci`, `status:
  completed`, `conclusion: success`, `headBranch: main`, `headSha:
  76ca9996c20c0f1aeede10472a5abeafc1cac7f5`, creado el 2026-11-24T21:22:21Z. Es el run que dio el
  informe de cierre.
- `git branch -a` solo daba `main` (y `origin/main`); `git ls-remote --heads origin` solo da
  `refs/heads/main` (ningún `fix/*`).
- Sesión en Opus 5.5, esfuerzo alto (`/effort` puesto a alto al empezar la sesión);
  `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1` puesta (medido con `echo`): las corridas pueden ir
  en segundo plano.

## Los dos ficheros del Escritorio (sha256 medidos con `sha256sum`)

| Fichero | Bytes | sha256 medido | ¿Coincide con el del consultor? |
|---|---|---|---|
| `ADR-0100-borrador.md` | 17.996 | `d598776b945c83838513fcfea20d753287043a0486f3e978a8835e3b9b3e2feb` | sí |
| `PREMISA-COSTES.yaml` | 6.335 | `1294bdb1b7dfd992dd87e14ccb0f9d1d6b2bc6e45168bd19ed64a719f68f3b33` | sí |

Leídos enteros antes de usarlos. Fechas, con un guion de la carpeta de trabajo que no imprime
ninguna: 11 en el borrador (2 distintas) y 3 en el yaml (1 distinta), 0 en un día de un caso
reservado; son las de la decisión y del contraste con el trader. Ningún resultado sin publicar: las
cifras de su §1 y §7 están en `PUENTE-TECHO.md` y `VIABILIDAD-COMISION.md`, y los totales de los
libros vistos el 2026-11-24 no se copian (el §7 los nombra sin cifras).

## Desviaciones de la apertura

- **Lo que vio Aleks de la conversación del trader.** El encargo manda declarar que «el consultor y
  Aleks vieron» los totales mensuales de enero, abril y agosto en la conversación del trader con otro
  asistente, y preguntarle a Aleks antes de escribir la fila qué vio él. Su respuesta, con sus
  palabras: «no lei nada la verdad, solo pasé el enlace». Gana lo medido: la fila del 2026-11-24
  copia la frase del encargo tal cual y añade la respuesta, y dice que quien vio los totales es el
  consultor. ADR-0100 §7, que entra byte a byte, conserva «el consultor y Aleks han visto»: la
  declaración es más amplia que lo ocurrido, no más estrecha, y no se toca. No nombraba ningún mes
  reservado, así que no hay PARADA.
- **Un añadido del consultor a la fila del día (2026-11-24, 18:26), llegado con el `make check` de
  la apertura en marcha**: una captura de la ventana de creación de sesión de FX Replay, con el panel
  de cuenta detrás (Backtesting, Lifetime), un agregado que incluye meses reservados. No se escribió
  mientras corría el `make check` (nada escribe en el repo mientras corre; cambiar la fila
  estadiada, además, rompía su sello): la apertura se commiteó con la fila que se había sellado, y el
  añadido entra, el mismo día, en el punto (9) de la fila del 2026-11-24 con el commit del
  pre-registro, tal cual, con las columnas de particiones, quién y quema ajustadas. La sesión no ha
  visto la captura.

## §0 · Las decisiones del consultor, la fase P y la fase 0

### §0.1 · Las decisiones del consultor (2026-11-24), escritas antes de correr

Tal cual del encargo (`docs/encargos/trabajo-diagnostico-premisa.md`, «DECISIONES DEL CONSULTOR»):

> D1. El guion es docs/validation/anexos/DIAGNOSTICO-PREMISA/premisa.py. Carga por su ruta, sin copiarlo, anexos/PUENTE-TECHO/puente.py tal como está en main (que a su vez carga techo_parejas.py) y usa sus funciones para correr las variantes base y todo_junto de PUENTE-TECHO.yaml sin cambiar ninguna pieza. Lee los cuatro yaml (PREMISA-COSTES, PUENTE-TECHO, META-TECHO-PAREJAS y criterio_fidelidad) y no lleva ninguna de sus cifras escrita dentro.
> D2. Tres controles antes de leer nada: (a) base y todo_junto, corridas por premisa.py, repiten las líneas de N, esperanza antes y después de comisión y percentiles de anexos/PUENTE-TECHO/base.txt y todo_junto.txt, sobre los cuatro meses y sobre abril y agosto, con diff; (b) el registro de abril y agosto (D3), sobre todas sus operaciones con stop inicial y antes de restringirlo a las de todo_junto, da N = 77 y una media de R bruto que casa a 0,02 con la serie anotada de VIABILIDAD-COMISION.md §3 (77 y +0,98: verifícalo allí); (c) el «R con lote fijo» de D5, en el test de humo, con todas las D iguales, coincide con el R neto. Si (a) falla, PARADA en §6 y en la réplica de §5; si (b), PARADA en el registro de §5; si (c), PARADA en §6. Lo demás sigue.
> D3. El registro: por cada caso dev de los cuatro meses con stop inicial, su fila del libro del mes, unida con el mismo criterio que scripts/viabilidad_trader.py (léelo: su cargar aborta si la construcción no es solo abril y agosto, lleva escritos sus dos libros y exige 77, así que la unión se REESCRIBE en premisa.py para los cuatro meses, y D2 b la comprueba). Las rutas de los cuatro libros van en el guion como literales completos, uno por mes, copiados del campo fichero de su entrada en libros.yaml (no hay en src una función que las resuelva), y el guion verifica cada una contra libros.yaml por su sha con declaracion_de (src/botsito/corpus/libros.py) antes de leer nada. Nunca una ruta compuesta con un valor leído de un fichero o de una variable: la guardia analiza entero un guion nuevo y niega la composición que no puede calcular (guardia.py, SENSIBLES y su análisis de rutas). R = (avgClosePrice − entrada) × dirección ÷ D, con D la distancia de la entrada al stop inicial del caso, sin costes. Las filas sin stop inicial, fuera y contadas. Los libros de enero y julio están en libros.yaml: verifícalo, y lee cada fecha solo con sus lecturas declaradas. Si la guardia niega leer algún libro, no lo reescribas: PARADA con el comando exacto, y lo lanza Aleks con «!».
> D4. La réplica: la variante todo_junto, con su R antes de comisión por posición. Las dos series se comparan sobre las mismas operaciones, las que todo_junto abre (las que deja fuera por el tope de lotes o el bróker rechaza, contadas aparte y por motivo). N, ganadoras, perdedoras y break even con los tramos de PREMISA-COSTES.yaml, y la media, por mes y por bloque, para el registro y para la réplica; la brecha por bloque; y la lectura de §5, que escribe el guion.
> D5. El techo con lote fijo: para base y para todo_junto, por posición, su R neto por su D (en puntos, la distancia de la entrada a su stop inicial), entre la mediana de D de las mismas posiciones; la esperanza y sus percentiles 5 y 95 por remuestreo por días con las réplicas y la semilla del bloque rentabilidad, con la misma función que usa techo_parejas.py; sobre los cuatro meses y aparte sobre abril y agosto. La lectura de todo_junto, la de backtest_del_trader en el yaml; la de base, solo dato.
> D6. El retroceso de las ganadoras del registro (R > +0,2): entre el instante del llenado del caso y dateEnd, con los ticks de Dukascopy, en una compra el bid mínimo y en una venta el ask máximo, contra la entrada menos desfase_puntos de PUENTE-TECHO.yaml, en fracciones de D, por los tramos del yaml. Los minutos sin ticks van por el respaldo M1, que es de bid: en una compra, el mínimo de la vela; en una venta, el máximo más el spread por hora del respaldo, como lo usa el bróker simulado; se cuentan aparte. Solo recuentos por tramo y por bloque.
> D7. Lo que imprime el guion y nada más: por mes y por bloque, las cifras de D4; los recuentos de D6; las de D5 con sus lecturas; y los recuentos de fuera (sin stop, sin fila, sin ticks). Ninguna fila por operación.
> D8. Determinismo: premisa.py repetido da la misma salida byte a byte; si no, PARADA.
> D9. Tiempo y memoria: mide una corrida y di cuánto tardará todo. Si pasa de 2 horas o de 1,5 GiB de pico, dilo y sigue. Si una corrida muere, PARADA con el error literal y sin relanzar.
> D10. Si algo pidiera tocar src/, tests/ (salvo test_premisa_costes.py) o knowledge/, PARADA con la alternativa; no se hace.
> D11. Arreglar un error de programación del guion para que pase los controles de D2 está permitido y se declara. Cambiar una pieza del puente, la definición de una medida o una cifra del yaml, no: PARADA en eso.

### §0.2 · La fase P: el pre-registro, antes de cualquier corrida

- **El commit del pre-registro:** `7b97ca49500fe1bf37bd1f162c280c92b2bfa2f5`, el 2026-11-24 a las
  19:26:05 (−05:00), «docs(adr): ADR-0100, la premisa con costes pre-registrada antes de que llegue»,
  sellado sobre el árbol `80a09d47e1455921a9935dfe3558322d2d3def2e` (`git rev-parse
  "7b97ca49^{tree}"`, igual al de la línea `SELLO` de su `make check`: 3624 passed, 28:31). Es el
  primero tras la apertura (`f7b4285e`, 18:46:54). **La primera corrida del guion**, con su hora, en
  §1: a esa hora `premisa.py` no existía en el repo.
- **ADR-0100** (`docs/adr/0100-la-premisa-se-mide-con-costes.md`): igual byte a byte que el fichero de
  Aleks, sha256 `d598776b945c83838513fcfea20d753287043a0486f3e978a8835e3b9b3e2feb` (el del fichero y
  el del blob indexado, `git show :<ruta> | sha256sum`). No lleva marcas de fecha.
- **`docs/plan/PREMISA-COSTES.yaml`**: igual byte a byte, sha256
  `1294bdb1b7dfd992dd87e14ccb0f9d1d6b2bc6e45168bd19ed64a719f68f3b33`; `git ls-files --eol` da
  `i/lf w/lf attr/text=auto eol=lf`: git no convierte los saltos.
- **`tests/unit/test_premisa_costes.py`**, con la forma de `test_puente_techo.py`: seis tests (el
  sha256; los saltos LF; `problemas()` vacío sobre el yaml, que comprueba la decisión y su fecha, los
  meses propuestos, `regla`, `regimen` y `extension`, `maximo_de_meses`, las tres condiciones,
  `c_pips`, los órdenes `antes` y `orden` y sus textos, las cinco combinaciones con exactamente
  `{por_riesgo, con_lote_fijo, propone}` y sus valores en su orden, ningún valor nulo en todo el árbol,
  los dos bloques en su orden, `tramos_r`, `margen_r`, el orden de §5, los tramos de retroceso y las
  variantes del techo con lote fijo; las claves a las que remite, en `criterio_fidelidad.yaml`
  —`n_minimo` 100, `esperanza_minima_r` "0.10", `percentil_remuestreo`, `replicas_remuestreo` y
  `semilla_remuestreo`—, en `META-TECHO-PAREJAS.yaml` —`propios.percentil_alto` 95 y
  `propios.techo_no_gana_si_percentil_alto_por_debajo_de_r` "0.10"— y en `PUENTE-TECHO.yaml`
  —`propios.desfase_puntos` 2 y las dos variantes—; y dos que rompen a propósito: `margen_r` a
  "0.25", que cambia el sha y da exactamente `["margen_r no es '0.20'"]`, y un texto con comas en el
  mapa en línea de `tramos_r`, que el lector parte sin error en una clave con valor nulo y el test
  caza). `uv run pytest tests/unit/test_premisa_costes.py -p no:cacheprovider -q`: 6 passed; `ruff
  format`, `ruff check` y `mypy`, limpios.
- **La fila del índice** en `docs/adr/README.md`, con la forma de la de 0099 (su título y su
  `## Estado`), y **los tres recuadros** tal cual, con la fecha del commit (2026-11-24), sin tocar el
  cuerpo: al final de ADR-0092 §6, detrás del de ADR-0099; al final de ADR-0098 §1, justo antes de
  «### 2. Cómo se lee cada medida»; al final de ADR-0099 §7, justo antes de «### 8. Lo visto,
  declarado». La forma de los recuadros de esos ADR es la supuesta (`> **RECUADRO de ADR-NNNN (<fecha>,
  `<rama>`; el cuerpo no se toca).** …`).
- **Las dos frases** (los dos diffs, de `git show 7b97ca49`):

```diff
--- a/CLAUDE.md
+++ b/CLAUDE.md
@@ -160,6 +160,9 @@
 `casos_reservados(repo)`, no se supone, y se declara igual el mismo dia. Sus imagenes no se abren.
+Además, por ADR-0100, los meses de 2024 del backtest con costes del trader son de construcción para
+la premisa: no van a meses_reservados.yaml ni son `construccion` de criterio_fidelidad.yaml, y se
+leen solo desde su rama de entrada.
```

```diff
--- a/docs/runbooks/MIRAR-EL-MATERIAL.md
+++ b/docs/runbooks/MIRAR-EL-MATERIAL.md
@@ -121,7 +121,7 @@
 Todo mes del que se reciba material del trader y que no sea ya de construcción por su ADR (hoy
-enero, abril, julio y agosto) entra en meses_reservados.yaml el mismo día que se recibe, antes de
+enero, abril, julio y agosto de 2026, y los meses de 2024 del backtest con costes de ADR-0100) entra en meses_reservados.yaml el mismo día que se recibe, antes de
@@ -134,4 +134,5 @@
-agosto (ADR-0043), julio (ADR-0078) y enero (ADR-0079).
+agosto (ADR-0043), julio (ADR-0078) y enero (ADR-0079); para la premisa, los meses de 2024 del
+backtest con costes (ADR-0100).
```

  Los dos textos citados casaban tal cual; el primero de MIRAR-EL-MATERIAL partía «(hoy» y «enero…»
  en dos líneas, y el cambio respeta ese salto (la línea queda larga: es el mínimo cambio).
- **ADR-0100 sale del bloque `ids-inexistentes`** del encargo, y el bloque con él, en el mismo commit;
  `state check`, `contrato_rama.py` (15 ficheros, G2) y `knowledge validate` (0 `ERROR`, log fuera
  del repo), en verde antes del `make check`. Tests Currently Passing, de 2143 a 2149.

### §0.3 · La fase 0 (skill fase-cero; el auditor, después de la fase P)

**a) Lo que se carga de `puente.py` y de dónde sale cada cifra por posición.** `premisa.py` carga
`anexos/PUENTE-TECHO/puente.py` por su ruta literal, como `puente.py` carga `techo_parejas.py`
(`puente.py:72-80`; las dos rutas son relativas a la raíz, así que se lanza desde ella). Usa, sin
cambiar nada: `cargar_yaml` (`:1043-1052`, que también carga META-TECHO-PAREJAS por
`tp._cargar_meta`), `tp.entorno` (`techo_parejas.py:403-434`: registro, mercados por día, reglas del
bróker y de la fase, configuración del llenado, contrato, reloj, sesiones, días dev y criterio),
`piezas_de` (`:130-164`), `variantes_del_yaml` (`:913-926`), `correr` (`:766-771`, que filtra las
filas con riesgo no positivo), `correr_variante` (`:929-975`, para D2 a), `bloque` (`:855-903`) y
`lecturas_de` (`:788-799`). Por posición:
- **R antes de comisión** = `bruto / riesgo` (la media es `esperanza_bruta`, `puente.py:629-634`);
  **R neto** = `neto / riesgo` (`r_neto`, `src/botsito/cases/criterio_fidelidad.py:582-585`).
- **El riesgo**: en las de orden, `lotes × |precio de la orden − su stop| / escala × contrato`
  (`src/botsito/engine/cableado.py:1352`); en las de `abrir_conocida` (todo_junto),
  `lotes × |entrada − stop de apertura| / escala × contrato` (`puente.py:588-589`). **La D en puntos**
  sale de ahí: `riesgo × escala / (lotes × contrato)`, la distancia de la entrada a su stop inicial;
  el guion exige que sea un entero positivo. Así `R neto × D` es el PnL neto por lote en puntos, que
  es lo que pesa el lote fijo.
- **La operación del caso de cada posición**: `pedidos_del_techo` da a cada operación del día el id
  `t<k>`, con k su posición en el caso (`puente.py:738-751`); `abrir_conocida` usa ese id como id de
  la posición y de su orden (`src/botsito/engine/broker.py:684-686`), y en `base` es el id de la
  orden stop (`puente.py:518-519`). El guion empareja por (día, k).
- **Sin cambios desde el cierre de F39m:** `git diff stable/F39m-puente-techo HEAD --stat --
  docs/validation/anexos/PUENTE-TECHO/puente.py
  docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/techo_parejas.py`, vacío; su último commit es el de
  F39m (`5fab2992`/`da15d984`) y el de F39l (`bca9ba20`).

**b) La unión caso-fila de `scripts/viabilidad_trader.py`.** `cargar` (`:219-343`): aborta si la
construcción no es solo abril y agosto (`:234-237`; hoy son cuatro meses, así que abortaría), lleva
escritos sus dos libros (`:253-256`) y exige 77 (`:331-332`). Lee del lector `corpus.libro`
(`filas_de_los_dias`, `:267-269`) las columnas `dateStart`, `side`, `entryPrice`, `initialSL`,
`avgClosePrice`, `rPnL`, `status` y `dateEnd` (`:257-260`). La clave es `(instante UTC del llenado,
entrada)` sobre las filas con `initialSL` (`:275-278`), con la entrada buscada por valor si el libro
no la escribe normalizada (`:296-306`); el stop del caso tiene que ser el `initialSL` (`:312-314`);
`dateEnd` se parsea con `corpus.libro._instante` y la declaración del libro (`:273`, `:309`). Se
puede cargar sin ejecutar su `main` (`:625-639`, bajo `__main__`), pero `cargar` no sirve para cuatro
meses: la unión se reescribe en `premisa.py` con ese mismo criterio (D3), y D2 b la comprueba.
`premisa.py` lee seis columnas, no ocho: no lee `rPnL` ni `status`.

**c) Los cuatro libros en `libros.yaml` y el filtro del lector.** `knowledge/corpus/libros.yaml`:
agosto `:17-28` (`AAAA/MM/DD HH:MM:SS`, UTC), abril `:29-39` (ídem), enero `:53-67` (ídem) y julio
`:68-83` (`AAAA-MM-DD HH:MM:SS`, **Europe/Madrid**). Su comentario de cabecera (`:15`, «NO ESTAN
enero ni septiembre») es anterior a la entrada de enero; el fichero es de solo añadir y no es de esta
rama. El lector (`src/botsito/corpus/libro.py:92-206`) verifica el sha (`:128-132`), parsea el
`dateStart` de cada fila con las lecturas declaradas (`:179-192`), calcula su día en
`huso_de_los_dias` y **descarta la fila si su día no está entre los pedidos ANTES de copiar ninguna
columna** (`:193-195` frente a `:203-204`); no devuelve ni cuenta las demás. Los días pedidos son los
de `arnes.dias_de_construccion` (los dev de construcción, sin ocultos). `dateEnd` no lo parsea el
lector: el guion lo parsea con `_instante` y la declaración del libro, como `viabilidad_trader.py`.
Las rutas: el `fichero` de cada entrada es relativo a `corpus/Estrategia del trader/` (el auditor,
fila 25), así que el literal completo lleva ese prefijo delante (`viabilidad_trader.py:261`); el
guion lo compara con `libros.yaml` por trozos, sin componer ninguna ruta con el valor leído (la
composición con un valor leído que nombra `corpus` la negaría la guardia: `guardia.py:4703-4725`,
`SENSIBLES` en `:4504-4516`).

**d) Los ticks y el respaldo M1 para el retroceso (D6), sin tocar `src/`.** El mercado de cada día es
`ent.mercados[dia]` (`techo_parejas.py:425`); `md.mercado()` da un `Mercado` con `ticks_del_minuto`
y `m1` por minuto (`src/botsito/engine/llenado.py:76-97`). La M1 es de BID (`:77`), y el spread
supuesto de un minuto sin ticks es `Configuracion.spread_supuesto` (`:63-64`), en
`ent.config_llenado`. Para los stops el bróker mira, en un minuto sin ticks, el BID de la vela en
una larga y el ASK = BID + spread en una corta (`llenado.py:340-342`; `_peor_del_minuto`,
`broker.py:972-989`): es lo que hace el guion (compra, la mínima de la vela; venta, la máxima más el
spread de ese minuto). El auditor (fila 35) recuerda que el bróker tiene otra lectura sin ticks, la
última M1 cerrada (`Mercado.cotizacion`, `llenado.py:99-118`), para el precio a mercado; para el peor
precio en contra, la de los stops es la que aplica. Un minuto con ticks pero ninguno dentro del tramo
(los de los bordes) no pasa al M1, como en el bróker. Lo que no cubra el mercado del día se cuenta
(«sin ningún precio en el tramo», «con algún minuto sin ticks ni M1»).

**e) Recuentos de partida**, contados hoy con `arnes.dias_de_construccion` y los casos dev, con un
guion de la carpeta de trabajo que no imprime fechas: **76 días dev y 198 operaciones del trader, las
198 con stop** (enero 21 días / 54, abril 21 / 35, julio 13 / 67, agosto 21 / 42); **77 en abril y
agosto**. Casan con `PUENTE-TECHO.md` y con `base.txt:10`. Las filas del libro sin `initialSL`
publicadas: abril 3 y agosto 5 (`VIABILIDAD-TRADER.md:35`), enero 4 (`ENTRADA-ENERO.md:502`), julio 5
(`ENTRADA-JULIO.md:577`; las cuatro, del auditor, fila 39).

**f) Las cifras publicadas de D2, verificadas en sus ficheros.** `anexos/PUENTE-TECHO/base.txt`:
cuatro meses (`:34-39`) N 191, antes de comisión y swaps 0.127, neta −0.239, percentiles −0.450 y
−0.026 (76 días); abril y agosto (`:46-50`) N 74, 0.113, −0.318, −0.679 y 0.031 (42 días).
`todo_junto.txt`: cuatro meses (`:10-15`) N 190, 8 fuera por el tope, 0 rechazadas, 0.350, 0.022,
−0.190 y 0.246; abril y agosto (`:22-26`) N 71, 6 fuera, 0.649, 0.285, −0.095 y 0.660.
`VIABILIDAD-COMISION.md:110` (§3): la serie «anotada», 77 operaciones y esperanza bruta **+0,98**
(igual en `:115` y `:120`, con otras comisiones; también `VIABILIDAD-TRADER.md:96`). El +0,98 sale
de las 77 con stop, antes de cualquier tope (`scripts/viabilidad_comision.py:313-326`; el auditor,
fila 18).

**g) Herencias** (grep de «R4.7», «salida C», «lote fijo», «registro», «anotada», «premisa», «V01»
y «V03» sobre las rutas literales del encargo y las últimas 400 líneas de HISTORIA, y lo que añade el
auditor):
1. **V01** (proveedor y spread de FX Replay, abierta; `AUDITORIA-CAZADOR-2026-11-23.md:138`): ADR-0100
   la nombra (§1, §2, §5) y la deja abierta; aquí no se toca. **V03** (coste por tramo de D, `:146`):
   ADR-0100 no la nombra y aquí no se mide: no es una de las tres medidas.
2. **La deuda de los docstrings de `viabilidad_trader.py`** (`PROJECT_STATE.md:85`): no es de esta
   rama (no se toca `scripts/`).
3. **El b2 del revisor de F39m** (el test de humo de `puente.py` no pasa el break even ni el tope por
   el bucle): la orden de cierre de F39m dijo que iría a Technical Debt «solo si una rama futura
   reutiliza `puente.py`» (`docs/state/HISTORIA.md:20980-20983`). Esta rama lo reutiliza (D1): **entra
   como línea de Technical Debt en las líneas del cierre** (§6), medida con el tope.
4. **El contraste con el trader** (ADR-0099 §6, `0099:183-188`: sus respuestas del 2026-11-23 entran
   por su propia rama, con su `fb-`): ninguna rama lo ha hecho y esta no lo abre. La frase nueva de la
   F que da el encargo deja de nombrarlo: **es lo que no cuadra** (abajo, decisión 0).
5. **La fila de ERRORES-RECURRENTES lleva cuatro columnas** (la de F39m se preparó con tres y el cierre
   la completó, `HISTORIA.md:20986-20987`): la de §7 se prepara con las cuatro.
6. **Lo que el auditor señala y no entra**, por ser medidas o lecturas que el encargo no pide: V00 (la
   matriz de desenlaces del trader frente al techo, operación a operación) y «el techo sobre las 77
   del registro, igual por igual» (`AUDITORIA-CAZADOR-2026-11-23.md:69`, `:105-126`); que el registro
   de agosto es el xlsx que el trader no avala (`:70-72`; la letra Q); y que los bloques de §5 mezclan
   meses con y sin vídeo (S-14, en R4.7). Las lecturas de ADR-0100 están pre-registradas y el informe
   no las matiza (encargo); estos puntos siguen donde están.
7. **Dos deudas del bróker que hereda D6** al leer el respaldo «como lo usa el bróker»: el spread
   supuesto va por hora de pared de Europe/Madrid, y las cotizaciones sin tick no usan la misma vela
   (`PROJECT_STATE.md:116` y `:138`). Se heredan tal cual; se cuenta cuántas ganadoras usan el
   respaldo.

**h) La fila de HOLDOUT-EXPOSICIONES del día, estadiada antes del primer `make check`.** Se estadió a
las 18:12 (la hora de `date` al estadiar; las seis rutas, `git status --short`), antes de
`state check`, `contrato_rama.py` (que dio `G2: fila de HOLDOUT-EXPOSICIONES del 2026-11-24 para
trabajo/diagnostico-premisa, estadiada`), `knowledge validate` y el primer `make check` (27:29, 3618
passed), cuya línea `SELLO` da el árbol `cfae88a2e2a952fdc97118559affd620905d14d1`, el mismo que
`git rev-parse "f7b4285e^{tree}"`: la fila iba dentro del árbol sellado del commit de apertura
(18:46:54). El añadido del consultor de las 18:26, en el commit del pre-registro (`80a09d47…`, ídem).

**i) Tiempo y memoria esperados (D9).** `puente.py` tardó de 75 a 90 s por variante con el entorno, y
un pico de 592 MiB en `base` (`PUENTE-TECHO.md:445-447`). `premisa.py control` construye el entorno
una vez y corre dos variantes; `todo`, otras dos y lee los cuatro libros: unos 3 a 5 minutos cada uno
y un pico del orden de 0,6 GiB. Todo cabe en esta sesión; se mide en la primera corrida (§1).

### §0.4 · El encargo frente al repo (el subagente `auditor-encargo`)

El auditor (solo lectura, sin libros, `corpus/`, `data/` ni `knowledge/cases/` salvo
`criterio_fidelidad.yaml`; un `git grep` sobre la raíz se lo negó el clasificador y lo repitió con
rutas literales) comprobó 57 afirmaciones: 42 correctas, 1 incorrecta y 14 con matiz, y 7 herencias.
Lo que cambia algo:

- **INCORRECTA (9):** «el consultor y Aleks vieron» los totales de la conversación del trader; Aleks
  no leyó nada. Ya tratado en la apertura (arriba).
- **MATIZ (8), la fila de HOLDOUT:** el encargo dicta «la salida y su instante»; la unión lee además
  `dateStart`, `side`, `entryPrice` e `initialSL`. La fila del 2026-11-24 ya nombra las seis columnas
  (su punto 5).
- **MATIZ (40), PROJECT_STATE:** «hoy 24.740 bytes» es el de `main` (`git show
  main:PROJECT_STATE.md | wc -c` = 24.740); en la rama son ya más. Las líneas del cierre se miden
  sobre la copia de `main` con ellas aplicadas (el cierre devuelve Current Branch y Current Feature),
  como hizo F39m (§6).
- **MATIZ grave (43), la F:** la herencia 4 de arriba; decisión 0.
- **MATICES de forma, que no cambian lo pedido:** el run 45490418025 no está escrito en ningún texto
  commiteado (la sesión lo verificó con `gh`, en la apertura); el `fichero` de `libros.yaml` es
  relativo (c); hay en `src/botsito/cases/visto.py:115-121` una `_fichero_del_libro` privada que da
  el `fichero` relativo, así que «no hay en src una función que las resuelva» vale para la ruta
  completa; `filas_de_los_dias` solo parsea `dateStart` y `dateEnd` va por `_instante` (c); el
  remuestreo pide montar posiciones de riesgo 1 con PnL igual al R con lote fijo, como
  `techo_parejas.percentil_de_diferencias` (`:228-246`), sin tocar `src/`; D5 no dice «con su propia
  mediana» para abril y agosto, y el ADR y el yaml sí (`0100:170-171`, yaml `:81`): se hace con su
  propia mediana; el respaldo «como lo usa el bróker» tiene dos lecturas (d); R4.7 «depende de» una
  prueba de FTMO para F17 y la rama no la necesita (la dependencia es solo de F17, como en F39m); el
  push como `fix/` lo pide `entregar-rama` solo si se toca la plataforma, y pedirlo no choca; «ningún
  agregado de un libro» es más estricto que CLAUDE.md para meses sin días reservados y no bloquea
  nada de lo pedido.

### §0.5 · Lo que no pude medir

- Si la guardia deja pasar `premisa.py`, guion nuevo, con los cuatro literales completos de los
  libros (julio, dentro de su carpeta `Backtest Julio 2026`): por el código, los cuatro meses son
  legibles (`guardia.py:353`, `MESES_DE_DESARROLLO`), pero solo se sabe lanzándolo. Si niega, PARADA
  con el comando exacto (D3).
- Que la unión de enero y julio no deje operaciones fuera: se mide en la primera corrida (los
  recuentos de fuera, por mes).

### §0.6 · Exposiciones

Las de la fila del 2026-11-24 de `HOLDOUT-EXPOSICIONES.md`, nada más: los dos ficheros del
Escritorio, los recuentos por mes, los casos dev, y el punto (9) (la conversación del trader, vista
por el consultor; la captura del panel de cuenta, vista por Aleks y el consultor). La fase 0 no abrió
ningún libro, imagen, fotograma, transcripción ni cruda.

### §0.7 · ¿Cuadra?

**Cuadra para las tres medidas**: D3 a D6 se pueden hacer como dicen sin tocar `src/` (a-d), y los
controles de D2 tienen sus cifras verificadas (f). Se sigue a la fase 1 sin esperar (encargo).
**No cuadra en una cosa, que no toca ninguna medida: las líneas del cierre** (decisión 0). Se para
solo en eso: las dos versiones de la F se preparan y se miden en §6, y la rama sigue.

## Lo que necesito que decidas

0. La frase nueva de la F. Opciones: (a) la del encargo con el contraste dentro: «F17 (ADR-0099 §5),
   el contraste con el trader (ADR-0099 §6) y el backtest del trader con costes (ADR-0100, R4.10),
   pendientes; el diagnóstico de la premisa, hecho.»; (b) la del encargo tal cual, que deja el
   contraste solo en el «Qué es» de R4.7. Recomiendo (a): ADR-0099 §6 manda que sus respuestas
   entren por su propia rama con su `fb-` y ninguna lo ha hecho; la Next Action es donde se ve lo
   pendiente. Coste de (b): un pendiente sin rama que deja de verse en PROJECT_STATE.
1. La línea de Technical Debt del b2 de `puente.py` (herencia 3). Opciones: (a) entra con el cierre,
   preparada y medida en §6, como dijo la orden de cierre de F39m; (b) no entra. Recomiendo (a): es lo
   que dejó escrito esa orden para el caso de que una rama reutilizara `puente.py`, y esta lo
   reutiliza. Coste de (b): contradecir esa respuesta sin decirlo en su sitio.

## Estado

EN CURSO: fase 0 escrita; se sigue a la fase 1 (cuadra para las tres medidas). Las dos decisiones de
arriba, solo de las líneas del cierre, esperan al consultor en la PARADA final.
