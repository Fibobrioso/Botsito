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

## §1 · Los controles (D2) y D8

- Test de humo (`test_premisa.py`): 10 passed; contra cuatro mutantes del guion en la carpeta de
  trabajo (`>` por `>=` en el tramo de R y en la lectura de §5, la mediana invertida en el lote fijo,
  la referencia con `+ desfase`), cada uno cae en su test (1 failed, 9 passed); con D iguales el de
  lote fijo pasa (D2 c).
- **Primera corrida del guion: 20:48:24** (`premisa.py control`), 1 h 22 min después del commit del
  pre-registro (19:26:05). 90 s, pico 592 MiB. **D2 a PASA** (los dos `diff` vacíos: `tail -n +8
  …/PUENTE-TECHO/base.txt | diff - …/base-repetida.txt` y lo mismo con `todo_junto`); **D2 b PASA**
  (77 operaciones, media del R bruto +0.984 frente a +0,98). La guardia dejó leer los cuatro libros.
- `premisa.py todo` (20:50:14, 90 s, pico 616 MiB): D2 a y b otra vez sobre sus corridas, PASA.
- Arreglo declarado (D11, de forma): la mediana salía «18» o «15.0» según N fuera impar o par
  (`statistics.median`); pasa a `mediana_de` en Decimal, con su test. Repetidas las dos corridas
  (20:52:57 y 20:54:31): `control.txt` igual byte a byte; `premisa.txt` solo cambia en dos líneas, el
  formato de la mediana («15.0» → «15», «18.0» → «18»); ninguna cifra.
- **D8 PASA**: `todo` otra vez a una carpeta fuera del repo (20:56:22) y `cmp` de `premisa.txt` y
  `lectura.txt`: iguales.
- **Segundo arreglo, tras el revisor (a1; D11):** en un minuto sin ticks, `extremo_en_contra` tomaba
  la vela del respaldo de todo minuto del tramo; el bróker solo la toma si su sello (su último
  milisegundo, `_sello_ms`) cae en (desde, hasta] (`src/botsito/engine/llenado.py:335`, `:124-129`).
  Ahora igual, con dos asserts nuevos en el test de humo (la salida antes del sello: la vela no entra;
  justo en el sello: sí). Repetidas `control` (22:12:17, 592 MiB) y `todo` (22:13:58, 617 MiB):
  `control.txt` igual byte a byte, los dos `diff` de D2 a vacíos, y **`premisa.txt` sin ningún cambio**
  (`diff` vacío con la de antes del arreglo): ninguna ganadora tenía un minuto del respaldo pasada su
  salida. D8 otra vez (22:15:38): `cmp` de `premisa.txt` y `lectura.txt`, iguales.
- La salida del test de humo, tal cual (la última, tras el segundo arreglo):

```
$ uv run pytest docs/validation/anexos/DIAGNOSTICO-PREMISA/test_premisa.py -p no:cacheprovider -v
============================= test session starts =============================
platform win32 -- Python 3.12.10, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\USER\Desktop\Bot v3
configfile: pyproject.toml
plugins: anyio-4.15.0, hypothesis-6.167.1
collected 10 items

docs\validation\anexos\DIAGNOSTICO-PREMISA\test_premisa.py ..........    [100%]

============================= 10 passed in 0.44s ==============================
```

## §2 · El registro frente a la réplica (`premisa.txt`, §5)

Sobre las mismas operaciones: las que `todo_junto` abre (190 de 198). Fuera, contadas: las filas del
libro sin `initialSL` (enero 4, abril 3, julio 5, agosto 5; no se unen a ningún caso); las 8 que
`todo_junto` deja fuera por el tope de lotes (enero 2, abril 2, julio 0, agosto 4), que tienen fila
en el registro y no posición en la réplica; ninguna rechazada por el bróker; ninguna operación del
caso sin fila, ni sin stop, ni con el stop distinto del `initialSL`. Tramos: ganadora R > +0,2,
perdedora R < −0,2, el resto break even; el R de la réplica es el de antes de comisión.

| Mes | Serie | N | Ganadoras | Perdedoras | Break even | Media del R |
|---|---|---|---|---|---|---|
| 2026-01 | registro | 52 | 16 | 33 | 3 | +0.531 |
| 2026-01 | réplica | 52 | 16 | 36 | 0 | +0.152 |
| 2026-04 | registro | 33 | 15 | 16 | 2 | +1.178 |
| 2026-04 | réplica | 33 | 13 | 20 | 0 | +0.541 |
| 2026-07 | registro | 67 | 18 | 31 | 18 | +0.375 |
| 2026-07 | réplica | 67 | 21 | 45 | 1 | +0.187 |
| 2026-08 | registro | 38 | 18 | 17 | 3 | +1.128 |
| 2026-08 | réplica | 38 | 18 | 20 | 0 | +0.743 |

| Bloque | Serie | N | Ganadoras | Perdedoras | Break even | Media del R | Brecha |
|---|---|---|---|---|---|---|---|
| abril_y_agosto | registro | 71 | 33 | 33 | 5 | +1.151 | +0.502 |
| abril_y_agosto | réplica | 71 | 31 | 40 | 0 | +0.649 | |
| enero_y_julio | registro | 119 | 34 | 64 | 21 | +0.443 | +0.271 |
| enero_y_julio | réplica | 119 | 37 | 81 | 1 | +0.172 | |

Brecha de enero_y_julio menos brecha de abril_y_agosto: −0.231; `margen_r`: 0.20. Lectura (la del
guion): **enero_y_julio_peores_tambien_para_el**.

## §3 · El retroceso de las ganadoras del registro (`premisa.txt`, sin lectura)

De las ganadoras del registro sobre las mismas operaciones de §2 (b4: ver «Desviaciones»), entre el
llenado del caso y `dateEnd`, contra la entrada menos `desfase_puntos` (2), en fracciones de D.

| Bloque | Ganadoras | por debajo de 0 | [0; 0,5) | [0,5; 0,8) | [0,8; 1,0) | 1,0 o más | Con algún minuto del respaldo | Extremo en el respaldo | Algún minuto sin ticks ni M1 |
|---|---|---|---|---|---|---|---|---|---|
| abril_y_agosto | 33 | 0 | 23 | 7 | 1 | 2 | 1 | 0 | 1 |
| enero_y_julio | 34 | 1 | 23 | 7 | 2 | 1 | 1 | 1 | 0 |

Ninguna sin ningún precio en el tramo, ninguna con `dateEnd` antes del llenado.

## §4 · El techo con lote fijo (`premisa.txt`, §6)

R neto × D / mediana de D, por posición, con D la del riesgo de su fila; percentiles 5 y 95 por
remuestreo por días (10000 réplicas, semilla 20261107).

| Variante | Conjunto | N | Mediana de D (puntos) | Esperanza con lote fijo | Media del R neto (por riesgo) | Percentil 5 | Percentil 95 | Días | Lectura |
|---|---|---|---|---|---|---|---|---|---|
| base | los cuatro meses | 191 | 18 | −0.017 | −0.239 | −0.230 | +0.212 | 76 | sin lectura (dato) |
| base | abril y agosto | 74 | 15 | −0.058 | −0.318 | −0.377 | +0.280 | 42 | sin lectura (dato) |
| todo_junto | los cuatro meses | 190 | 18 | +0.196 | +0.022 | −0.069 | +0.483 | 76 | **no_concluyente** |
| todo_junto | abril y agosto | 71 | 16 | +0.510 | +0.285 | −0.050 | +1.069 | 42 | sin lectura (dato) |

Ninguna réplica descartada. La «media del R neto (por riesgo)» repite la de `base.txt` y
`todo_junto.txt` (−0.239, −0.318, +0.022, +0.285).

## §5 · Las lecturas, literales (`lectura.txt`)

- LECTURA DE §5 (ADR-0100): enero_y_julio_peores_tambien_para_el
- LECTURA DE §4 CON LOTE FIJO, todo_junto sobre los cuatro meses (ADR-0100 §6): no_concluyente

## §6 · Las líneas del cierre (preparadas, no aplicadas)

En `anexos/DIAGNOSTICO-PREMISA/simular_cierre.py` y su salida `simular-cierre.txt`, sobre el
PROJECT_STATE de `main` (24.740 bytes): `test_hoja_de_ruta` a, b y c vacíos con las dos F; ninguna
letra sale ni entra; R4.9 HECHA sin `NA:`, R4.10 ABIERTA con `NA:F`, R4.7 con ADR-0100 en Refs y en
su «Qué es». **Bytes:** con la F del encargo, 24.807; con la de la decisión 0, 24.850; **con la línea
del b2 (257 bytes), 25.064 y 25.107: pasa de 24.970 (y del tope). PARADA con la cifra; no se recorta
nada.** Las líneas, tal cual (las de `simular_cierre.py`):

- **Next Action, en la F** (sustituye «F17 rediseñado (ADR-0099 §5) y el contraste con el trader,
  pendientes.»):
  - la del encargo: «F17 (ADR-0099 §5) y el backtest del trader con costes (ADR-0100, R4.10),
    pendientes; el diagnóstico de la premisa, hecho.»
  - la de la decisión 0: «F17 (ADR-0099 §5), el contraste con el trader (ADR-0099 §6) y el backtest
    del trader con costes (ADR-0100, R4.10), pendientes; el diagnóstico de la premisa, hecho.»
- **Technical Debt, al final** (decisión 1; no cabe): «- El test de humo de
  `anexos/PUENTE-TECHO/puente.py` no pasa el break even ni el tope por el bucle de `repetir` (b2 del
  revisor de F39m, PUENTE-TECHO.md); lo reutiliza `anexos/DIAGNOSTICO-PREMISA/premisa.py`. Dueño: la
  rama que vuelva a tocar `puente.py`.»
- **Hoja de ruta, R4.7:** sus Refs pasan a «NA:F · ID:ADR-0098 · ID:ADR-0099 · ID:ADR-0100 · ID:A-16
  · F:F17»; en su «Qué es», tras «…y el contraste de la premisa con el trader (ADR-0099 §6).», entra
  «ADR-0100: la premisa se mide con el backtest del trader con costes y dos diagnósticos, con la
  lectura escrita antes (R4.9, HECHA; R4.10).»
- **Hoja de ruta, detrás de R4.8:**

```
### R4.9 · El diagnóstico de la premisa (ADR-0100 §5-§6)
- **Refs:** ID:ADR-0100 · ID:ADR-0099
- **Qué es:** sobre los días dev de construcción, el registro del trader frente a la réplica (la variante todo_junto del puente), mes por mes, con el retroceso de sus ganadoras, y el techo con lote fijo (base y todo_junto), con las lecturas pre-registradas en docs/plan/PREMISA-COSTES.yaml. Diagnóstico de construcción: ninguna cifra cambia un valor (ADR-0092 §6, recuadro de ADR-0100).
- **Depende de:** nada (el pre-registro de ADR-0100).
- **Quién:** la sesión, con el encargo del consultor; lee el consultor.
- **Hecho cuando:** las dos medidas, con sus lecturas.
- **Estado:** HECHA (trabajo/diagnostico-premisa, DIAGNOSTICO-PREMISA.md): la lectura de §5, «enero_y_julio_peores_tambien_para_el»; todo_junto con lote fijo sobre los cuatro meses, «no_concluyente».

### R4.10 · El backtest del trader con costes (ADR-0100 §2-§4)
- **Refs:** ID:ADR-0100 · NA:F
- **Qué es:** dos meses de 2024 que el trader no haya operado nunca en backtest, en su plataforma con spread de 0,2 pips y comisión de 5 USD por lote de ida y vuelta, grabados y con el libro completo; medido por riesgo y con lote fijo, con la lectura de ADR-0100 §4 escrita antes (docs/plan/PREMISA-COSTES.yaml). Material de construcción para la premisa (ADR-0100 §2); entra SIN ABRIR y fuera del repo hasta su rama.
- **Depende de:** que el trader lo haga y Aleks lo traiga.
- **Quién:** el trader lo hace, Aleks lo trae SIN ABRIR y la sesión lo mide en su propia rama, con el encargo del consultor.
- **Hecho cuando:** su lectura de ADR-0100 §4, escrita.
- **Estado:** ABIERTA.
```

  Sin fila en el Marcador.

## §7 · La fila de ERRORES-RECURRENTES, preparada (cuatro columnas)

| `trabajo/diagnostico-premisa` | Una pasada, opus, con los seis alcances del encargo (DIAGNOSTICO-PREMISA.md, «Informe del revisor»; lo hecho, en «Lo que se hizo con los hallazgos del revisor»): eje (a) 0 bloquea, 1 importa, 0 menor; eje (b) 1 bloquea, 4 importa, 2 menor. a1 (el respaldo M1 sin el sello del bróker en el retroceso), b1 (§2-§4 sin sus tablas), b2 (§6 sin el texto de las líneas), b3 (sin la tabla del encargo punto por punto), b4 (el retroceso sobre las mismas operaciones, sin declarar), b5 (el número del ADR en el artefacto antes del pre-registro, sin declarar), b6 (comandos incompletos) y b7 (la salida del test de humo), arreglados o declarados. | <del consultor, tras la PARADA final> | (1) El encargo dictaba en la fila de HOLDOUT «la salida y su instante»; la unión lee además `dateStart`, `side`, `entryPrice` e `initialSL` (el auditor, fila 8): la fila nombra las seis. (2) La frase del encargo declaraba «el consultor y Aleks vieron»; Aleks no leyó nada: gana lo preguntado. (3) Las líneas del cierre de un encargo no contaban con el b2 que la orden de cierre anterior dejó condicionado a reutilizar `puente.py`, ni con su tamaño: no cabe. (4) De la sesión: `statistics.median` imprimía «18» o «15.0» según la paridad de N; un guion nuevo que componga una ruta con un valor leído que nombre `corpus` lo niega la guardia, y se comparó por trozos. |

## El encargo, punto por punto

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 1 | Base: main 76ca9996, tag sobre su merge, CI de main en verde, ninguna otra rama | Hecho | «Base comprobada»; run 45490418025 `success` sobre 76ca9996 |
| 2 | Tag `stable/F39n-diagnostico-premisa` libre | Hecho | `git tag -l` y `git ls-remote --tags`, vacíos |
| 3 | Opus 5.5, esfuerzo alto; REAP=1 | Hecho | «Base comprobada» (`echo`) |
| 4 | La fila del día, lo primero, por recuento, antes del primer `make check` | Hecho | §0.3 h: estadiada a las 18:12; SELLO cfae88a2 = árbol de f7b4285e |
| 5 | Preguntar a Aleks qué vio y escribirlo con sus palabras | Hecho | Fila del 2026-11-24, punto (9); «Desviaciones de la apertura» |
| 6 | La exposición del 2026-11-24, literal, comprobada por recuento | Hecho | Punto (9); 0 reservados en enero, abril y agosto |
| 7 | Los dos ficheros del Escritorio, con su sha, leídos enteros | Hecho | «Los dos ficheros del Escritorio» |
| 8 | Contrato: R4, riesgo medio, lista blanca y protegidos | Hecho | `contrato.yaml`; `contrato_rama.py` en verde en cada commit |
| 9 | El encargo tal cual, con ADR-0100 en `ids-inexistentes` | Hecho | f7b4285e; sale en 7b97ca49 |
| 10 | Hasta el pre-registro, el id solo en el encargo | Parcial | b5: el nombre del fichero del Escritorio («ADR-0100-borrador.md») en la tabla del artefacto de la apertura; «Desviaciones» |
| 11 | Fase P 1-2: ADR y yaml byte a byte, LF | Hecho | §0.2 (sha y `git ls-files --eol`) |
| 12 | Fase P 3: el test del yaml, con un test que rompe | Hecho | §0.2; 6 passed; dos tests de rotura |
| 13 | Fase P 4: fila del índice, tres recuadros, dos frases con sus diffs | Hecho | §0.2 |
| 14 | Fase P 5: state check, ruff, mypy, `make check`; sha y hora frente a la primera corrida | Hecho | 7b97ca49 a las 19:26:05; primera corrida a las 20:48:24 (§1) |
| 15 | La fase P antes de la fase-cero y de su auditor | Hecho | El auditor se lanzó tras 7b97ca49 |
| 16 | Fase 0 a-i, con `fichero:línea`, en su commit | Hecho | §0.3; 7671148a |
| 17 | PARADA condicional: seguir si cuadra, parar solo en lo que no | Hecho | §0.7; decisiones 0 y 1 |
| 18 | README en su commit antes de correr | Hecho | 3877edf5 (20:47:04), solo el README |
| 19 | `premisa.py` con `control` y `todo`, el entorno una vez | Hecho | `premisa.py`, `modo_control` y `modo_todo` |
| 20 | Test de humo en los dos sentidos, con su salida pegada | Hecho | §1 (salida pegada; cuatro mutantes) |
| 21 | ruff format, ruff check y mypy sobre los guiones | Hecho | «Comandos ejecutados» |
| 22 | `make check` en verde antes de cada commit | Hecho | Las líneas `SELLO` de cada commit |
| 23 | D1 | Hecho | `premisa.py` carga `puente.py` por su ruta; ninguna pieza cambiada (revisor, b22) |
| 24 | D2 a, b y c | Hecho | §1 |
| 25 | D3 | Hecho | §0.3 b-c; `verificar_libros` y `cargar_registro_del_trader` |
| 26 | D4 | Hecho | §2 |
| 27 | D5 | Hecho | §4 (abril y agosto con su propia mediana, como ADR-0100 §6) |
| 28 | D6 | Hecho de otra forma | Sobre las ganadoras de las mismas operaciones de §2 (b4); el respaldo, con el sello del bróker tras a1 |
| 29 | D7 | Hecho | `premisa.txt`: solo recuentos y medias |
| 30 | D8 | Hecho | §1 (dos veces, tras cada arreglo) |
| 31 | D9 | Hecho | §1: unos 90 s por corrida; picos de 592 y 617 MiB |
| 32 | D10 y D11 | Hecho | Nada de `src/`, `tests/` (salvo el test del yaml) ni `knowledge/`; dos arreglos de programación declarados |
| 33 | Fase 2: `control.txt` y los diffs | Hecho | §1 |
| 34 | Fase 3: `premisa.txt`, `lectura.txt`, las lecturas literales | Hecho | §5 |
| 35 | Informe: apertura, §0 a §7 con sus tablas | Hecho | §0 a §7 |
| 36 | Ninguna recomendación de spec, motor ni gestión del dinero | Hecho | Solo «Recomiendo» en las decisiones del cierre |
| 37 | Las líneas del cierre, preparadas en §6 y medidas sobre una copia | Hecho | §6; `simular-cierre.txt` |
| 38 | PROJECT_STATE ≤ 24.970 con las líneas | Hecho, con PARADA | 24.807 con la F del encargo; la línea del b2 no cabe (decisión 1) |
| 39 | Qué no cambia | Hecho | `git diff --name-status main...HEAD`: nada fuera del contrato |
| 40 | Revisor opus con los seis alcances, pegado al final | Hecho | «Informe del revisor» |
| 41 | Push como `fix/`, CI de Linux, runs en el informe | Hecho | «La CI de Linux» |
| 42 | «Rama lista para revisión, NO cerrada.» | Hecho | Al final |

## Desviaciones

- **La fila de HOLDOUT nombra seis columnas leídas, no dos** (auditor, fila 8): las de la unión y la
  salida.
- **b5 (revisor): el número del ADR antes del pre-registro.** En el commit de apertura, la tabla del
  artefacto nombraba el fichero del Escritorio, `ADR-0100-borrador.md`, con su número; el encargo
  pedía que hasta el pre-registro el id solo estuviera en el encargo. `knowledge validate` pasó (el
  bloque `ids-inexistentes` lo declaraba). Se dice aquí; el commit de apertura no se reescribe.
- **b4 (revisor): el retroceso sobre las mismas operaciones.** D6 dice «las ganadoras del registro»;
  el guion las toma de las mismas operaciones de §2 (las que `todo_junto` abre), porque ADR-0100 §5
  pone toda la sección «sobre las mismas operaciones en las dos series». Las 8 que deja fuera el tope
  no entran en el retroceso.
- **Dos arreglos de programación (D11):** la mediana en Decimal (formato; ninguna cifra cambió) y el
  sello del respaldo M1 como el bróker (a1; ninguna cifra cambió). Con las corridas repetidas y D8
  después de cada uno.
- **`simular_cierre.py` y `simular-cierre.txt`**, no previstos, añadidos al README tras las corridas;
  `simular_cierre.py` lee el PROJECT_STATE de `main` de un fichero volcado fuera del repo (un guion
  nuevo que llamara a `git` podía negarlo la guardia).
- **El retroceso cuenta aparte lo que cae por debajo de 0** («por_debajo», el precio no llegó a la
  entrada menos el desfase): queda fuera de los cuatro tramos del yaml, que empiezan en 0.
- Las dos decisiones del cierre (abajo).

## Comandos ejecutados (2026-11-24)

La carpeta de trabajo de la sesión es
`C:/Users/USER/AppData/Local/Temp/claude/d82effbe86c6c5d6/9410a1ab-0b58-43e2-af47-8ff37567416b/scratchpad`
(fuera del repo). Las horas de los `make check` son las de su commit, que va justo después, con su
duración; el log no guarda la de arranque.

```
18:12     git add docs/encargos/trabajo-diagnostico-premisa.md contrato.yaml PROJECT_STATE.md docs/state/HISTORIA.md docs/validation/DIAGNOSTICO-PREMISA.md docs/validation/HOLDOUT-EXPOSICIONES.md
18:13     uv run botsito state check ; uv run python scripts/contrato_rama.py ; uv run botsito knowledge validate > <carpeta de trabajo>/validate-apertura.log 2>&1
          make check > make-check.log 2>&1   (27:29, 3618 passed; SELLO cfae88a2)
18:46:54  git commit -F <carpeta de trabajo>/msg-apertura.txt   (f7b4285e)
~19:00    cp de los dos ficheros del Escritorio a docs/adr/0100-la-premisa-se-mide-con-costes.md y docs/plan/PREMISA-COSTES.yaml ; sha256sum de los dos
          uv run pytest tests/unit/test_premisa_costes.py -p no:cacheprovider -q   (6 passed)
          uv run ruff format / ruff check / mypy tests/unit/test_premisa_costes.py   (limpios)
          git show :docs/plan/PREMISA-COSTES.yaml | sha256sum ; git ls-files --eol (los dos)
          uv run botsito state check ; uv run python scripts/contrato_rama.py ; uv run botsito knowledge validate > <carpeta de trabajo>/validate-faseP.log 2>&1
          make check > make-check.log 2>&1   (28:31, 3624 passed; SELLO 80a09d47)
19:26:05  git commit -F <carpeta de trabajo>/msg-faseP.txt   (7b97ca49)
          uv run python <carpeta de trabajo>/recuento_dev.py "C:/Users/USER/Desktop/Bot v3"   (76 días, 198 operaciones)
          uv run python scripts/contrato_rama.py ; uv run botsito knowledge validate > <carpeta de trabajo>/validate-fase0.log 2>&1
          make check > make-check.log 2>&1   (28:26, 3624 passed; SELLO 561e37c2)
20:15:59  git commit -F <carpeta de trabajo>/msg-fase0.txt   (7671148a)
          make check > make-check.log 2>&1   (26:53, 3624 passed; SELLO 8b30c0be)
20:47:04  git commit -F <carpeta de trabajo>/msg-readme.txt   (3877edf5)
20:47     uv run ruff format / ruff check / mypy docs/validation/anexos/DIAGNOSTICO-PREMISA/premisa.py docs/validation/anexos/DIAGNOSTICO-PREMISA/test_premisa.py   (limpios)
20:47     uv run pytest docs/validation/anexos/DIAGNOSTICO-PREMISA/test_premisa.py -p no:cacheprovider -v   (10 passed)
20:48     uv run python -B <carpeta de trabajo>/hacer_mutantes.py ; uv run pytest <carpeta de trabajo>/mut_tramo/test_premisa.py -p no:cacheprovider -q (y mut_lectura5, mut_lote_fijo, mut_retroceso, uno a uno)   (1 failed, 9 passed, cada uno)
20:48:24  uv run python scripts/pico_memoria.py ejecutar -- uv run python -B docs/validation/anexos/DIAGNOSTICO-PREMISA/premisa.py control docs/validation/anexos/DIAGNOSTICO-PREMISA   (592 MiB; exit 0)
20:50     tail -n +8 docs/validation/anexos/PUENTE-TECHO/base.txt | diff - docs/validation/anexos/DIAGNOSTICO-PREMISA/base-repetida.txt   (vacío)
20:50     tail -n +8 docs/validation/anexos/PUENTE-TECHO/todo_junto.txt | diff - docs/validation/anexos/DIAGNOSTICO-PREMISA/todo_junto-repetida.txt   (vacío)
20:50:14  uv run python scripts/pico_memoria.py ejecutar -- uv run python -B docs/validation/anexos/DIAGNOSTICO-PREMISA/premisa.py todo docs/validation/anexos/DIAGNOSTICO-PREMISA   (616 MiB; exit 0)
20:52:57  (tras la mediana en Decimal) el mismo control   (592 MiB; cmp de control.txt con la anterior: igual; los dos diff, vacíos)
20:54:31  el mismo todo   (617 MiB; diff con la anterior: solo las dos líneas de la mediana)
20:56:22  uv run python -B docs/validation/anexos/DIAGNOSTICO-PREMISA/premisa.py todo <carpeta de trabajo>/d8 ; cmp de premisa.txt y lectura.txt   (iguales)
~21:10    git show main:PROJECT_STATE.md > <carpeta de trabajo>/ps-main.md
~21:12    uv run python -B docs/validation/anexos/DIAGNOSTICO-PREMISA/simular_cierre.py <carpeta de trabajo>/ps-main.md > docs/validation/anexos/DIAGNOSTICO-PREMISA/simular-cierre.txt
          uv run python scripts/contrato_rama.py ; uv run botsito knowledge validate > <carpeta de trabajo>/validate-guion.log 2>&1
          make check > make-check.log 2>&1   (30:13, 3624 passed; SELLO c4d1f453)
22:00:07  git commit -F <carpeta de trabajo>/msg-guion.txt   (71ddfa7f)
22:00     git push origin trabajo/diagnostico-premisa:refs/heads/fix/diagnostico-premisa ; gh run list --branch fix/diagnostico-premisa --limit 3   (run 45536934319)
~22:11    gh run view 45536934319 --json ... ; gh run view 45536934319 --log-failed   (solo state check por el nombre fix/)
22:12:17  (tras el sello del respaldo, a1) el mismo control   (592 MiB; control.txt igual; los dos diff, vacíos)
22:13:58  el mismo todo   (617 MiB; diff con la anterior: vacío)
22:15:38  uv run python -B docs/validation/anexos/DIAGNOSTICO-PREMISA/premisa.py todo <carpeta de trabajo>/d8b ; cmp de premisa.txt y lectura.txt   (iguales)
```

## Exposiciones de cada día

2026-11-24: la fila de ese día en `HOLDOUT-EXPOSICIONES.md`, entera (puntos 1 a 9, con el añadido
del consultor de las 18:26). Lo que la rama leyó cabe en ella: los casos dev, las seis columnas de las
filas de los días dev de los cuatro libros por el lector, los ticks y el M1 de los días dev, y los
documentos. Ningún libro de otro mes, imagen, fotograma, transcripción ni cruda.

## Lo que necesito que decidas

0. La frase nueva de la F. Opciones: (a) la del encargo con el contraste dentro: «F17 (ADR-0099 §5),
   el contraste con el trader (ADR-0099 §6) y el backtest del trader con costes (ADR-0100, R4.10),
   pendientes; el diagnóstico de la premisa, hecho.»; (b) la del encargo tal cual, que deja el
   contraste solo en el «Qué es» de R4.7. Recomiendo (a): ADR-0099 §6 manda que sus respuestas
   entren por su propia rama con su `fb-` y ninguna lo ha hecho; la Next Action es donde se ve lo
   pendiente. Coste de (b): un pendiente sin rama que deja de verse en PROJECT_STATE.
1. **PARADA con la cifra:** la línea de Technical Debt del b2 de `puente.py` (herencia 3), que la
   orden de cierre de F39m manda si una rama reutiliza `puente.py`, NO CABE: con ella PROJECT_STATE
   queda en 25.064 bytes (F del encargo) o 25.107 (F de la decisión 0), por encima de 24.970 y del
   tope de 25.000 (§6; `simular-cierre.txt`). Opciones: (a) el b2 queda en el registro del cierre de
   HISTORIA y en este informe, sin línea en PROJECT_STATE; (b) entra en PROJECT_STATE con el recorte
   que el consultor diga (otra línea acortada a HISTORIA, como las «Technical Debt ACORTADA»);
   (c) no entra. Recomiendo (a): deja escrito el pendiente donde lo dejó F39m sin tocar el tope. Coste
   de (b): un recorte que esta rama no puede elegir (encargo: no se recorta nada por cuenta propia).

## La CI de Linux

- `fix/diagnostico-premisa` sobre 71ddfa7f (el commit del guion y las medidas): **run 45536934319**,
  `failure` en «Run make check» por un solo test, `tests/unit/test_cli.py::test_state_check_ok_on_real_repo`
  («PROJECT_STATE declara la rama 'trabajo/diagnostico-premisa'; la rama actual es
  'fix/diagnostico-premisa'»): 1 failed, 3527 passed, 102 skipped. Es el único fallo aceptado.
- El run del último commit (el de este informe con el revisor) va en el mensaje de entrega: escribirlo
  aquí exigiría otro commit y otro run.

## Informe del revisor

Pegado tal cual (subagente `revisor`, opus, sobre HEAD 71ddfa7f; no cita ningún tramo no citable):

> ## Informe del revisor · trabajo/diagnostico-premisa · 2026-11-24
>
> He revisado HEAD 71ddfa7f contra la base 76ca9996. La rama no está lista: hay un hallazgo que bloquea en el eje (b). Los seis alcances del encargo se sostienen. El bloqueo y los avisos son de cómo está escrito el informe, no de las medidas.
>
> ### Eje (a) · Reglas de la casa
> Resumen: 0 bloquea, 1 importa, 0 menor.
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | a1 | importa | El informe dice que el retroceso de D6 lee el respaldo M1 «como el bróker», y en el último minuto del tramo no es así. El bróker descarta la vela M1 de un minuto sin ticks si su sello (el último milisegundo de la vela) cae después de `hasta`. `extremo_en_contra` usa la vela de todo minuto entre `desde//MS` y `hasta//MS` sin mirar el sello. Así, en el minuto de `dateEnd`, si no tiene ticks, entra la vela entera, hasta 59 s después de la salida. Afecta como mucho a las ganadoras con algún minuto por el respaldo, que son 1 por bloque. No está declarado. | `src/botsito/engine/llenado.py:335` (`if vela is None or _sello_ms(vela) <= desde_ms or _sello_ms(vela) > hasta_ms: continue`) y `:126-131` (`_sello_ms`) frente a `premisa.py:243-262`. `DIAGNOSTICO-PREMISA.md:207-212` («es lo que hace el guion»). `premisa.txt:56` y `:60` («con algun minuto por el respaldo M1: 1») |
>
> Comprobado sin hallazgos:
> - **Contrato.** `uv run python scripts/contrato_rama.py` dio, tal cual:
>   - `CONTRATO: 25 ficheros dentro del contrato de trabajo/diagnostico-premisa (riesgo medio, artefacto docs/validation/DIAGNOSTICO-PREMISA.md, tramo 'R4', 4 comprobaciones para el revisor)`
>   - `G2: fila de HOLDOUT-EXPOSICIONES del 2026-11-24 para trabajo/diagnostico-premisa, estadiada` (exit 0).
> - **Comprobaciones del contrato.**
>   - `uv run botsito state check`: `OK: rama 'trabajo/diagnostico-premisa' ...` (exit 0).
>   - `make check`: no lo ejecuté. `make-check.log:104` da `3624 passed, 6 xfailed ... (0:30:13)`, `:128` da `SELLO ... c4d1f4536a543b9f3556d55b4b23a4a5688a7535` y `:130` da `PICO DE MEMORIA ... 319 MiB`. Ese árbol es `git rev-parse HEAD^{tree}` (c4d1f453).
>   - Los sellos de los commits anteriores también casan con su árbol: f7b4285e con cfae88a2, 7b97ca49 con 80a09d47, 7671148a con 561e37c2 y 3877edf5 con 8b30c0be.
>   - `knowledge validate`: no lo ejecuté (escribe su log).
> - **Trailers `Fuente:`.** Ningún commit toca `knowledge/spec` ni `knowledge/cases`: el `git log ... -- knowledge/spec knowledge/cases` sale vacío.
> - **Holdout y material.**
>   - Nada toca `knowledge/`.
>   - Hay fila del 2026-11-24 en HOLDOUT-EXPOSICIONES con los cuatro libros, las seis columnas y los ticks y el M1 de los días dev.
>   - No se abrió ningún fotograma ni imagen.
>   - La captura del panel de cuenta es un agregado. Está declarada el mismo día con sus cifras, y ninguna se usa (ADR-0021 §2).
> - **Regímenes de cambio.**
>   - Evidencia, feedback, manifests, transcripciones, fotogramas y `libros.yaml`: sin cambios.
>   - HISTORIA y HOLDOUT: solo líneas añadidas (`grep -c "^-[^-]"` = 0).
>   - HISTORIA: `# Archivo 82` añadido al final.
> - **Ambigüedades.** Ninguna tocada.
> - **ADR.** El `## Estado` de 0100 empieza por `ACTIVE`. Los recuadros de 0092, 0098 y 0099 son solo líneas `+`, en el sitio pedido y con el texto literal del encargo.
> - **Informes cerrados.** La rama no modifica ningún `docs/validation/*.md` que ya estuviera en main, salvo la fila añadida a HOLDOUT.
> - **Guardias de `cita`.** No hay sitios nuevos con `cita`.
> - **Cifras.** Nada en `src/`. El guion no lleva cifras de los cuatro yaml. Las constantes `CONTROL_ANOTADA_*` (`premisa.py:109-112`) son del control D2 b, sacadas de VIABILIDAD-COMISION, y están comentadas.
> - **Citas del informe** que contrasté con su fuente:
>   - `puente.py:72-80`: carga techo_parejas por su ruta.
>   - `puente.py:738-751`: el id `t{k}` en la línea 750.
>   - `llenado.py:340-342`: BID en una larga y BID + spread en una corta; el sello de la 335 no lo cita (a1).
>   - `libro.py:193-195` frente a `:203-204`.
>   - `VIABILIDAD-TRADER.md:35`: 3 y 5 filas sin `initialSL`.
>   - `VIABILIDAD-COMISION.md:110`: anotada, 77, +0,98.
>   - `VIABILIDAD-COMISION.md:115` y `:120`.
> - **Evidencia nueva.** Ninguna.
> - **Una precisión sobre el lector, sin gravedad (es código de main).** `libro.py:180` (`_fila_como_dict`) parsea en memoria todas las celdas de cada fila antes del filtro por día de `:193-195`. Al guion solo le llegan las filas de los días pedidos. La frase del informe («antes de copiar ninguna columna») es exacta.
>
> ### Eje (b) · Encargo
> Resumen: 1 bloquea, 4 importa, 2 menor. Requisitos: 34 hechos, 5 parciales, 1 no hecho; además 1 hecho de otra forma y 1 en curso (este revisor).
>
> | # | Requisito | Estado | Evidencia |
> |---|---|---|---|
> | 1 | Base: main = 76ca9996, tag sobre su merge, CI de main, ninguna otra rama | Hecho | `git merge-base main HEAD` = 76ca9996. `stable/F39m-puente-techo^{commit}` = `main^1` = 7a3087e9. La CI la declara el informe en `DIAGNOSTICO-PREMISA.md:20-23` (no la verifiqué). |
> | 2 | Tag F39n libre | Hecho | `git tag -l "stable/F39n*"` vacío |
> | 3 | Modelo y REAP=1 | Hecho | `DIAGNOSTICO-PREMISA.md:26-28`, declarado |
> | 4 | Fila HOLDOUT, lo primero, por recuento, antes del primer make check | Hecho | Fila del 2026-11-24 de la rama. El SELLO cfae88a2 = árbol de f7b4285e (la fila iba dentro) |
> | 5 | Preguntar a Aleks y escribir su respuesta con sus palabras | Hecho | Punto (9) de la fila («no lei nada la verdad, solo pasé el enlace»). Desviación declarada en `DIAGNOSTICO-PREMISA.md:45-52` |
> | 6 | La frase de la exposición, literal | Hecho | Punto (9) de la fila, igual a `encargo:15` |
> | 7 | Ficheros del Escritorio con sus sha | Hecho | sha256 medidos: d598776b… (ADR) y 1294bdb1… (yaml), en el Escritorio, en el repo y en los blobs de 7b97ca49 y de HEAD |
> | 8 | Contrato: R4, medio, lista blanca | Hecho | `contrato.yaml:2-20` |
> | 9 | ADR-0100 en `ids-inexistentes` y fuera en el pre-registro | Hecho | `git diff f7b4285e 7b97ca49 -- docs/encargos/...`: el bloque sale |
> | 10 | Hasta el pre-registro, «el ADR de la premisa», sin el número | Parcial | b5 |
> | 11 | Fase P 1-2: ADR y yaml byte a byte, con LF | Hecho | sha arriba. `git ls-files --eol`: `i/lf w/lf` |
> | 12 | Fase P 3: test del yaml con todo lo pedido y uno que rompe | Hecho | `tests/unit/test_premisa_costes.py:151-204`. `uv run pytest ... -q`: 6 pasan. El de `margen_r` a 0.25 (`:182-190`) y el de las comas (`:193-204`) rompen a propósito |
> | 13 | Fase P 4: fila del índice y tres recuadros | Hecho | Diffs de `docs/adr/README.md`, 0092, 0098 y 0099 |
> | 14 | Fase P 4: las dos frases, con sus diffs en el informe | Hecho | Diff de `CLAUDE.md` y de `MIRAR-EL-MATERIAL.md`. `DIAGNOSTICO-PREMISA.md:117-138` |
> | 15 | Fase P 5: sha y hora del pre-registro frente a la primera corrida | Hecho | `:82-87` y `:333`. 7b97ca49 a las 19:26:05; `premisa.py` no está en los árboles de 7b97ca49 ni de 3877edf5 (`git ls-tree`) |
> | 16 | Fase 0 a-i con fichero:línea, en su commit | Hecho | 7671148a; `§0.3` |
> | 17 | PARADA condicional | Hecho | `§0.7`; decisiones 0 y 1 (`:430-445`) |
> | 18 | README en su commit antes de correr | Hecho | 3877edf5 a las 20:47:04, con el README solo |
> | 19 | `premisa.py` con modos `control` y `todo` | Hecho | `premisa.py:721-820` |
> | 20 | Test de humo en los dos sentidos, sobre la lista del encargo | Hecho | `test_premisa.py:49-201`: fronteras +0,2, −0,2, 0,20 y 1,0 a los dos lados. `uv run pytest ... -q`: 10 pasan |
> | 21 | ruff y mypy | Hecho | `ruff check --no-cache` («All checks passed!») y `ruff format --check --no-cache` («5 files already formatted»). mypy, sin comprobar |
> | 22 | D1: puente.py por su ruta, sin cambiar piezas, los cuatro yaml | Hecho | `premisa.py:64-72`, `:428-431` y `:462-472`. Ninguna asignación ni `setattr` sobre `pt.`/`tp.` (Grep). `git diff --stat stable/F39m-puente-techo HEAD` sobre los anexos de PUENTE-TECHO y RC-3: vacío |
> | 23 | D2 a, b y c | Hecho | Mis dos `tail -n +8 … \| diff - …`: exit 0, vacíos. `control.txt:3-9` (77; +0.984). D2 c en `test_premisa.py:98-100` |
> | 24 | D3: rutas literales verificadas por sha, sin componer rutas | Hecho | `premisa.py:80-98` y `:338-356` |
> | 25 | D4 | Hecho | `premisa.txt:11-49`. Cuadra: 52+33+67+38 = 190; fuera por el tope 2+2+0+4 = 8; brechas +0.502 y +0.271, diferencia −0.231 |
> | 26 | D5 | Hecho | `premisa.txt:62-83`. `remuestreo_por_dias`, la misma función que `techo_parejas.py:236-246`. Lectura no_concluyente: el percentil 5 es −0.069 |
> | 27 | D6 | Hecho de otra forma | b4 y a1 |
> | 28 | D7: nada por operación | Hecho | `premisa.txt` entero: solo recuentos y medias por mes, por bloque y por variante |
> | 29 | D8 | Hecho | Declarado en `:342-343` (no verificable) |
> | 30 | D9 | Hecho | `:333` y `:337`: 90 s, 592 y 616 MiB |
> | 31 | Fase 2: `control.txt` y los diffs en el informe | Hecho | `:334-336` y `:413-414` |
> | 32 | Fase 3: `premisa.txt`, `lectura.txt` y las lecturas literales en el informe | Hecho | `:354-355`, iguales a `lectura.txt:2-3`. Las escribe el guion: `premisa.py:589-596`, `:699-701` y `:794-802` |
> | 33 | Informe §2, §3 y §4 con sus tablas | No hecho | b1 |
> | 34 | Informe §6: las líneas del cierre preparadas y medidas sobre una copia | Parcial | b2 |
> | 35 | Informe §7: la fila de ERRORES con cuatro columnas | Hecho | `:368` |
> | 36 | El encargo frente a lo hecho, punto por punto, con evidencia | Parcial | b3 |
> | 37 | Comandos literales con su hora | Parcial | b6 |
> | 38 | Exposiciones de cada día | Hecho | `:423-428` |
> | 39 | Ninguna recomendación de spec, motor ni gestión del dinero | Hecho | Grep: solo «Recomiendo» en `:435` y `:444`, sobre las líneas del cierre |
> | 40 | Qué no cambia | Hecho | `git diff --name-status main...HEAD`: nada en `src/`, `knowledge/`, `scripts/`, Makefile, `.claude/`, HOJA-DE-RUTA ni los yaml del plan. La Next Action, intacta |
> | 41 | Revisor | En curso | Este informe |
> | 42 | Push como `fix/`, CI, números de run en el informe y la frase final | Parcial | La ref local `origin/fix/diagnostico-premisa` = 71ddfa7f = HEAD. El informe (`:449`) aún dice que falta el push y no trae ningún run |
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | b1 | bloquea | Faltan en el informe el §2, el §3 y el §4 que pide el encargo: tabla por mes y por bloque con la brecha y su lectura, recuentos del retroceso por tramo y por bloque, y el techo con lote fijo de las dos variantes en los dos conjuntos. El informe solo remite a `premisa.txt` («tal cual») y no dice por qué lo hace de otra forma. | `encargo:102` frente a `DIAGNOSTICO-PREMISA.md:345-350` |
> | b2 | importa | El §6 no trae el texto de las líneas del cierre: la F, R4.7, R4.9, R4.10 y la línea del b2. Da sus bytes y remite al guion; el texto solo está en `simular_cierre.py`. | `encargo:105` («prepáralas en §6»). `DIAGNOSTICO-PREMISA.md:357-364`. El texto, en `simular_cierre.py:65-72` y `:105-130` |
> | b3 | importa | No hay tabla «El encargo, punto por punto» (la de la skill `entregar-rama`): ni requisitos numerados, ni estados Hecho/Parcial, ni evidencia por punto. Hay una lista de viñetas que remite a secciones. | `DIAGNOSTICO-PREMISA.md:370-388`. `.claude/skills/entregar-rama/SKILL.md:46-50` y `:107` |
> | b4 | importa | El retroceso de D6 se mide solo sobre las ganadoras de las operaciones que `todo_junto` abre (190), no sobre todas las ganadoras del registro (198 operaciones con fila). La lectura es defendible por el marco de ADR-0100 §5 («sobre las mismas operaciones»), pero D6 dice «las ganadoras del registro» y el informe no declara la elección. | `premisa.py:622` (`ganadoras = [o for o, _ in parejas ...]`). `encargo:49`. `premisa.txt:54` (33 = las ganadoras del registro emparejado de `:40`) |
> | b5 | importa | En el commit de apertura, el artefacto ya llevaba el número del ADR (el nombre del fichero del Escritorio), y el encargo decía que hasta el pre-registro el id solo podía estar en el encargo. `knowledge validate` pasó por el bloque `ids-inexistentes`, pero el informe no lo declara. | `git grep -n "0100" f7b4285e -- docs/validation/DIAGNOSTICO-PREMISA.md` da `:34`: `` `ADR-0100-borrador.md` ``. `encargo:24` |
> | b6 | menor | «Comandos ejecutados» está incompleto y lleva marcadores en vez de literales. Falta el `make check` del último commit (SELLO c4d1f453, 3624 passed, 30:13), y faltan ruff, mypy, `pytest` de `test_premisa_costes.py`, `state check` y `contrato_rama.py` de cada commit. Las rutas de los mutantes van como `<carpeta de trabajo>` y las horas como `~`. | `DIAGNOSTICO-PREMISA.md:400-421`. `make-check.log:104` y `:128` |
> | b7 | menor | El encargo pide pegar la salida del test de humo; el informe da solo «10 passed». | `encargo:93`. `DIAGNOSTICO-PREMISA.md:329` |
>
> Alcances del encargo, uno a uno:
> 1. **El pre-registro va antes de la primera corrida.** Confirmado: los sha son los de Aleks; 7b97ca49 (19:26:05) es el primer commit tras la apertura; `premisa.py` no existe en los árboles de 7b97ca49 ni de 3877edf5.
> 2. **Los controles de D2 pasaron de verdad.** Confirmado: los dos diffs, vacíos, y `premisa.py` usa las funciones de `puente.py` sin cambiar ninguna pieza.
> 3. **El guion no lee nada que no sea de un día dev.** Confirmado:
>    - Los días salen de `arnes.dias_de_construccion`, con ocultos vetados (`arnes.py:149-161`).
>    - El lector solo devuelve filas de esos días.
>    - El retroceso solo mira el `MercadoDia` del día dev (`simulacion.py:56-79`, la ventana del día).
>    - No hay ningún agregado del libro: los recuentos de fuera son de filas de días dev.
>    - No imprime nada por operación.
> 4. **Las lecturas las escribe el guion desde el yaml.** Confirmado: `orden` y `margen_r` salen del yaml, y los umbrales, de criterio y META. El informe no las matiza.
> 5. **Los dos tests rompen donde deben.** Confirmado: 6 y 10 pasan; los dos de rotura del yaml están, y el de humo prueba los dos lados de cada frontera.
> 6. **La fila de HOLDOUT lleva lo leído y la exposición.** Confirmado: lleva lo leído, la frase literal, la respuesta de Aleks y el añadido de las 18:26.
>
> ### Lo que no pude comprobar
> - La hora de la primera corrida (20:48:24) y las de D8: no hay huella en el repo, solo lo que dice el informe.
> - Los cuatro mutantes del test de humo: viven en la carpeta de trabajo, fuera del repo. Por lectura, cada mutación descrita la cazaría su test.
> - El recuento de `casos_reservados` y `casos_ocultos` (34; 0 en los cuatro meses): exige ejecutar código sobre `knowledge/cases/`.
> - Que el añadido de las 18:26 sea «tal cual» y que la respuesta de Aleks sea literal: los mensajes no están en el repo.
> - El run de CI 45490418025 de main y la CI de `fix/diagnostico-premisa`: no consulté la red.
> - Que la guardia dejó leer los cuatro libros, y la hora del estadiado de la fila (18:12): solo los declara el informe.
> - mypy (escribe su caché), `knowledge validate` (escribe su log) y `make check` (escribe): no los ejecuté. Para `make check` vale `make-check.log`.
> - Tras mis dos `pytest` aparecen `__pycache__/` ignorados en `docs/validation/anexos/DIAGNOSTICO-PREMISA/` y en `tests/unit/`. No sé si ya existían por las corridas de la sesión. `git status --short` no ve nada sin seguir.
>
> ### Comandos ejecutados
> 1. `git branch --show-current && git merge-base main HEAD && git log --format='%h %ad %s' --date=iso main..HEAD && git diff --stat main...HEAD && git status --short`
> 2. `uv run python scripts/contrato_rama.py`
> 3. `sha256sum` de los dos ficheros del repo y de los dos del Escritorio; `git show 7b97ca49:<ruta> | sha256sum` y `git show HEAD:<ruta> | sha256sum` para los dos
> 4. `git show --stat --format='%h %ad%n%B' --date=iso f7b4285e 7b97ca49 7671148a 3877edf5 71ddfa7f` (antes, un intento con `for` lo negó la guardia; no lo reescribí para esquivarla, lo cambié por un solo `git show`)
> 5. `git diff main...HEAD -- docs/validation/HOLDOUT-EXPOSICIONES.md CLAUDE.md docs/runbooks/MIRAR-EL-MATERIAL.md docs/adr/README.md docs/adr/0092-* docs/adr/0098-* docs/adr/0099-* PROJECT_STATE.md`
> 6. `grep -n "^## Variante"` sobre los cuatro ficheros de los bloques; `wc -l` de las salidas
> 7. `tail -n +8 docs/validation/anexos/PUENTE-TECHO/base.txt | diff - docs/validation/anexos/DIAGNOSTICO-PREMISA/base-repetida.txt` (exit 0)
> 8. `tail -n +8 docs/validation/anexos/PUENTE-TECHO/todo_junto.txt | diff - docs/validation/anexos/DIAGNOSTICO-PREMISA/todo_junto-repetida.txt` (exit 0)
> 9. `git diff --stat stable/F39m-puente-techo HEAD -- <anexos PUENTE-TECHO y RC-3, yamls del plan, knowledge, src, scripts, Makefile, .claude, tests>`; `git diff --name-status main...HEAD`
> 10. `uv run pytest tests/unit/test_premisa_costes.py -p no:cacheprovider -q` (6 pasan)
> 11. `uv run pytest docs/validation/anexos/DIAGNOSTICO-PREMISA/test_premisa.py -p no:cacheprovider -q` (10 pasan)
> 12. `git status --short --ignored docs/validation/anexos/DIAGNOSTICO-PREMISA tests/unit`
> 13. `git grep -n "0100" f7b4285e -- <artefacto, HOLDOUT, PROJECT_STATE, contrato, HISTORIA>`; `git show f7b4285e:docs/encargos/... | head -12`; `git diff --stat 8a10590b main -- tests/`
> 14. `git log --format='%h%n%B' main..HEAD -- knowledge/spec knowledge/cases`; `git diff ... 0100 | grep "^+## Estado"`; `grep` de SELLO, PICO, passed y failed en `make-check.log`
> 15. `git rev-parse` del árbol de HEAD y de los otros cuatro commits; `ls -la make-check.log`
> 16. `git log --format='%h a=%ad c=%cd'`; `git ls-tree -r --name-only` en 7b97ca49 y 3877edf5 sobre el anexo; `git ls-files --eol` del ADR y del yaml
> 17. `git diff main...HEAD -- HISTORIA HOLDOUT | grep -c "^-[^-]"`; `grep "^+# Archivo"`; `git show main:PROJECT_STATE.md | wc -c`; `wc -c PROJECT_STATE.md`
> 18. `uv run ruff check --no-cache …`; `uv run ruff format --check --no-cache …`
> 19. `git tag -l "stable/F39n*"`; `git rev-parse "stable/F39m-puente-techo^{commit}" main main^1`; `git branch -a`; `git rev-parse origin/fix/diagnostico-premisa HEAD`
> 20. `uv run botsito state check`
> 21. `git diff f7b4285e 7b97ca49 -- docs/encargos/trabajo-diagnostico-premisa.md`
> 22. Lecturas con Read y Grep:
>     - de la rama: el encargo, `contrato.yaml`, `DIAGNOSTICO-PREMISA.md`, `premisa.py`, `premisa.txt`, `control.txt`, `lectura.txt`, `README.md` del anexo, `simular_cierre.py` y `simular-cierre.txt`, los dos tests, `PREMISA-COSTES.yaml` y ADR-0100;
>     - de main: `libro.py:1-207`, `arnes.py:139-173`, `simulacion.py:40-99`, `cableado.py:720-759`, `llenado.py:93-131` y `:330-345`, `puente.py:68-83`, `:735-774` y `:905-975`, `techo_parejas.py:380-449` (más un Grep de `remuestreo_por_dias`), `VIABILIDAD-COMISION.md:104-121`, `VIABILIDAD-TRADER.md` (Grep de `initialSL`) y la skill `entregar-rama`.
>
> No abrí ningún libro, ni `corpus/`, `data/`, `knowledge/cases/` (salvo lo que lee `test_premisa_costes.py`, `criterio_fidelidad.yaml`), imágenes, fotogramas, transcripciones ni crudas. No ejecuté `premisa.py`, `puente.py`, el arnés ni `make check`.

## Lo que se hizo con los hallazgos del revisor

- **a1 (importa), el respaldo M1 sin el sello:** arreglado en `extremo_en_contra` (la vela entra solo
  si su sello cae en (desde, hasta], como `llenado.py:335`), con dos asserts nuevos en el test de humo
  (10 passed). Corridas repetidas: `premisa.txt` sin ningún cambio; D8 otra vez, igual (§1).
- **b1 (bloquea), §2-§4 sin tablas:** escritas, con las cifras de `premisa.txt` (§2, §3 y §4).
- **b2 (importa), §6 sin el texto de las líneas:** escrito (§6).
- **b3 (importa), sin la tabla punto por punto:** «El encargo, punto por punto», 42 requisitos.
- **b4 (importa), el retroceso sobre las mismas operaciones:** declarado («Desviaciones»), con su
  porqué en ADR-0100 §5; no se cambia la medida (D11: la definición de una medida no se cambia).
- **b5 (importa), el número del ADR en el artefacto de la apertura:** declarado («Desviaciones»); el
  commit no se reescribe.
- **b6 (menor), los comandos:** completados, con la carpeta de trabajo nombrada literal una vez, los
  `make check` de cada commit con su sello y los del revisor aparte (su informe).
- **b7 (menor), la salida del test de humo:** pegada (§1).

## Estado

**Rama lista para revisión, NO cerrada.** Medidas hechas (§1-§5), líneas del cierre preparadas (§6),
revisor pasado y sus hallazgos arreglados o declarados, CI de Linux con el único fallo aceptado. Las
dos decisiones de arriba, solo de las líneas del cierre, esperan al consultor: la 1, PARADA con su
cifra.
