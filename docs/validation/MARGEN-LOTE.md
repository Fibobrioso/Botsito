# MARGEN-LOTE · Qué hace el bot cuando el lote del 0,5 % no cabe en el margen o en el volumen (R3.3)

Rama `trabajo/margen-lote`, abierta el 2026-10-17 desde `main` en 9cf711e (commit de estado sobre
el merge 5296a31, tag `stable/F37r-sesgo-h4-color`). Encargo: `docs/encargos/trabajo-margen-lote.md`
(va fechado el 2026-10-18; el reloj de la máquina al abrir daba el 2026-10-17 a las 20:39, y las
fechas de este informe y de HOLDOUT-EXPOSICIONES son las reales).
Tramo: R3 (R3.3 de `docs/plan/HOJA-DE-RUTA.md`; E de la Next Action; heredado 37). Modelo de la
sesión: `claude-fable-5-1` según el entorno de la sesión; el esfuerzo lo fija `/model` en el
terminal de Aleks y la sesión no puede leerlo desde dentro.

## 0 · La base, comprobada al abrir

Las cuatro comprobaciones del paso 1 de la skill `abrir-rama`, con su salida:

- `git fetch origin` y `git status --short` vacío; `git rev-parse --short main` → `9cf711e`;
  `git rev-parse main origin/main` → dos veces `9cf711ee36cd4a08de4d2ab7230ee9153eddd3d1`.
- El último tag de los registros de cierre de `docs/state/HISTORIA.md` es
  `stable/F37r-sesgo-h4-color`; `git rev-parse "stable/F37r-sesgo-h4-color^{commit}"` y
  `git rev-parse main^1` dan los dos `5296a31329af369e40cb23273c6cce91e2e0ae0e`, y
  `git ls-remote --tags origin stable/F37r-sesgo-h4-color` lo trae
  (`020d917c4e84e2738cb81194d95fac885b121940 refs/tags/stable/F37r-sesgo-h4-color`).
- La CI de `main` sobre su HEAD, consultada con `gh run view 39083113877` (como pide el encargo:
  ni curl ni guion): `status completed`, `conclusion success`, `headSha 9cf711ee…dd3d1`,
  `headBranch main`, workflow `ci`.
- Ninguna otra rama: `git branch --list` da solo `main`; `git ls-remote --heads origin "fix/*"`
  sale vacío.

## 1 · Fase 0 · Inventario sin tocar nada (2026-10-17)

Lo que pide el punto 4 del encargo, medido en el repo y sin escribir código, spec ni knowledge. Lo
único escrito en esta fase: este informe, la fila de `HOLDOUT-EXPOSICIONES.md` (§1.j) y dos
ajustes del contrato (§1.h, h9).

### 1.a Dónde se calcula y se comprueba el lote hoy

**El lote.**
- `dimensionar_lote` (`src/botsito/engine/primitivas_broker.py:428-442`) NO calcula: anota en la
  `OrdenEnPreparacion` la base del lotaje, el riesgo y su base de cálculo (ADR-0053 §1.1).
- `_lote_resuelto` (`primitivas_broker.py:496-511`) lo resuelve la primera vez que alguien lo pide
  con el stop ya escrito: `dinero = saldo × riesgo / 100`, `saldo` es `ctx.cuenta.saldo` o
  `ctx.cuenta.saldo_corte` según `base_calculo_riesgo`, y
  `lote = dinero / (distancia / escala × contrato)`, con la distancia hasta el stop si
  `lotaje_base = hasta_stop_fraccion`. Lo guarda en `o.lote`.
- `redondear_lote` (`primitivas_broker.py:484-494`): `o.lote = max(⌊lote/paso⌋ × paso, minimo)`
  (línea 493; el encargo dice 492, que es la lectura de `contrato`). **Sube al mínimo**: es lo que
  dice ADR-0053 (tabla, línea 39: «no por debajo del mínimo») y lo contrario de la prosa de RN-027
  («si queda por debajo de instrumento_lote_minimo, no se opera», `strategy_spec.yaml:2065-2067`).
- RN-027 solo dispara si el lote NO es múltiplo del paso (`no_es_multiplo_de`,
  `primitivas_broker.py:284-294`; forma en `strategy_spec.yaml:2083-2085`): un lote que ya es
  múltiplo exacto no pasa por `redondear_lote`. Importa para dónde colgar el límite (§1.f y
  decisión 1).
- `colocar_orden_limite` (`primitivas_broker.py:513-547`) toma `_lote_resuelto(o)` y llama a
  `ctx.broker.colocar_stop` (o `colocar_limite`); si vuelve un `Rechazo`, anota
  `EventoBroker(..., "rechazo", ...)` y marca la zona rechazada. Sin lote (`None` o `<= 0`) lanza
  `CableadoError`: hoy no hay camino «no se coloca» que no sea un error.

**El bróker.**
- `_limite_infringido` (`broker.py:855-871`): `lotes > volumen_max_lotes` → `"volumen_max_lotes"`;
  después `ordenes_simultaneas_max` y `posiciones_dia_max`. Lo llaman `_colocar`
  (`broker.py:415`, tras el cierre de mercado y el freno, y antes de `_precio_infringido`) y
  `abrir_conocida` (`broker.py:539-541`, que levanta `BrokerError` porque no hay orden que
  rechazar). `modificar` (`broker.py:455-492`) también rechaza, por precio.
- `_aplicar` (`broker.py:698-729`): el llenado (`tipo == LLENADA`, :716-728) crea la `Posicion` con
  `o.lotes` y el precio del evento, **sin ninguna comprobación**: no existe el camino «rechazo al
  llenar». Un rechazo al llenar tampoco es una `Peticion` (R13, ADR-0067): la orden ya estaba en
  el servidor; en «### Rechazos por motivo (mes | motivo | peticion | rechazos)» hará falta una
  columna `peticion` nueva (`llenar`) y no contar petición (auditor, h13).
- El bróker **no conoce el saldo**: `Broker.__init__` (`broker.py:259-313`) recibe reglas, llenado,
  mercado, contrato y escala. Tiene `flotante()` (`broker.py:829-842`), el P/L de las posiciones
  vivas a su último precio marcado, y las `ReglasBroker` (`broker.py:119-141`) no llevan el
  apalancamiento: `reglas_broker_de` (`simulacion.py:121-146`) lee del perfil volumen máximo,
  órdenes simultáneas, posiciones por día, comisión, swaps, stops level y mensajes por día, y
  **no lee `firma_apalancamiento`** (FTMO-P-D1.md §2 ya lo midió; sigue así).
- `_precio_de_mercado(lado, ms)` (`broker.py:815-827`) devuelve el BID para `compra` y el ASK
  para `venta`: es el precio al que se MARCA o cierra la posición, el contrario del que convierte el
  margen (ask en compras, bid en ventas). Para el margen hace falta la lectura inversa.

**La cuenta.** `ctx.cuenta` es la `CuentaViva` (`ContextoDia`, `primitivas_broker.py:119-144`;
`engine/cuenta.py:391-553`): `saldo`, `saldo_corte`, `equity = saldo + flotante de las marcas`
(`cuenta.py:304-308`), `limite_dia`, `limite_total`. El cableado la crea ANTES que el bróker
(`cableado.py:195-198` y `:199-206`) y le pasa los eventos del bróker en `_a_la_cuenta`
(`cableado.py:328-382`): `abrir` con el lote y la entrada en moneda, los cargos, `marcar` con la
peor marca del minuto y `cerrar`. Con `--diagnostico-cuenta-diaria` la cuenta renace cada día
(`cableado.py:195-196`). El flotante a tick vive en el bróker (`flotante()`); el de la cuenta es
por marcas de minuto.

**La spec.** `dimensionar_lote` y `redondear_lote` son acciones del vocabulario
(`strategy_spec.yaml:404-406` y `:479-481`); RN-011 (`:1419-1523`, `decision: ADR-0020`) prepara
la orden y RN-027 (`:2062-2095`, `decision: ADR-0016`) la redondea. Con D1 y D2 **ninguna de las
dos tiene por qué cambiar de forma** si el límite va en la preparación de la orden (abajo): sus
`notas` ganan una línea que diga que el lote que colocan puede quedar por debajo del de RN-011
por el ADR 0081 (el nuevo), y eso ya obliga a `spec docs --escribir` en el mismo commit.

**Dónde propongo el límite: en los DOS sitios, con papeles distintos.**
1. *La preparación de la orden* (`colocar_orden_limite`, antes de llamar al bróker): el lote final
   es `min(lote de RN-011, firma_volumen_max_lotes, margen_libre × lote_margen_libre_fraccion
   convertido a lotes)`, redondeado hacia abajo al paso; con `lote_si_no_cabe = no_operar` y un lote
   que no cabe, no se envía y se anota (como `bloqueadas`). Los dos parámetros nuevos los lee el
   cableado del registro, como `cierre_pendientes` (ADR-0068, `simulacion.py:110-118`,
   `consumido_por: [ADR-0068]`); el tope de volumen y el apalancamiento llegan por `ReglasBroker`
   desde el perfil, que ya es «lo que el perfil lee solo el simulador» (ADR-0050 §3). La spec no
   lee el tope de volumen: no hace falta duplicar `firma_volumen_max_lotes` en `parametros.yaml`
   ni una regla nueva con una cita del trader que no habla de esto (decisión 1).
2. *El bróker* (`_colocar` y `_aplicar(LLENADA)`, y `abrir_conocida`): rechaza por margen aunque el
   bot calcule bien, porque hace de FTMO. Comprueba `margen_requerido(lotes, precio) >
   margen_libre`, con `margen_libre = equidad − margen de las posiciones vivas − margen de las
   pendientes stop` (§1.b), y la equidad del bróker = `saldo()` que le pasa el cableado desde la
   cuenta + `flotante()` al tick. Motivo nuevo `margen_libre`, en `Rechazo` como los demás.

Por qué los dos: el límite del bot es la decisión D1/D2 (fidelidad: misma operación, menos lote);
el rechazo del bróker es el contrato de ADR-0052 («es el que hace de FTMO») y el único que mide,
en la corrida ANTES del cambio, cuántas órdenes de hoy rechazaría el margen (§1.e).

### 1.b La documentación de MT5: cuándo se comprueba el margen de una pendiente (D3)

Página leída: «Margin Calculation for Retail Forex, Futures»,
https://www.metatrader5.com/en/terminal/help/trading_advanced/margin_forex (la misma de
FTMO-P-D1.md §2), leída el 2026-10-17 por `WebFetch` (la guardia no negó nada; la herramienta no
devuelve más de 125 caracteres seguidos por cita, así que van frases sueltas, cada una literal).

- Bajo el título de la página, en el párrafo que explica cómo se suma el margen de posiciones y
  órdenes: «**For all other order types (Stop and Stop Limit), the margin is summed up (charged for
  each order).**» La frase anterior: «The final margin is taken according to the highest of the two
  calculated values.» (la de las órdenes de mercado y límite opuestas, «the margin is calculated
  for each direction»). Y, de la misma sección: «the total margin is equal to the sum of the
  current position's and placed order's margins».
- Fórmula, bajo «Forex»: «Volume in lots * Contract size / Leverage». Conversión a la divisa del
  depósito: «The Ask price is used for buy deals, and the Bid price is used for sell deals.»
- Bajo «FORTS Futures»: «Once triggered, stop orders behave similar to market orders.»

**Lo que eso dice y lo que no.** La página dice que una orden STOP colocada **tiene margen cargado
mientras está colocada** («charged for each order»; «placed order's margins»): MT5 reserva margen
al colocar una pendiente stop, y una pendiente que no cabe en el margen libre no se coloca. Es una
inferencia de la frase, no una frase que diga «se comprueba al colocar»; la página **no da una
regla general del instante de la comprobación**. Así que D3 queda así: **se comprueba en los dos
instantes**, al colocar (lo sostiene la frase citada) y al llenar (el llenado de una stop es una
operación de mercado, y el margen libre puede haber cambiado desde que se colocó: ese es el
supuesto conservador que el encargo pide si la página no lo dice). Y el margen de la pendiente stop
colocada **cuenta como margen usado** hasta que se llena, se cancela o se rechaza. Medir en la demo
cuándo lo comprueba MT5 de verdad queda para la entrada A (ejecución 3), como manda el encargo.

Dos consecuencias para el diseño: (1) al colocar, el precio que convierte el margen es el ask (compra)
o el bid (venta) **del mercado en ese instante**, no el precio de la orden: hace falta un lector
inverso a `_precio_de_mercado`; (2) al llenar, el precio es el del evento de llenado.

### 1.c La medida 1: la vía, el recuento previo y el guion propuesto (NO corrido)

**La vía del arnés** (la misma que usa la corrida): `arnes.dias_de_construccion(repo, criterio,
meses)` (`engine/arnes.py:134-167`) lee los casos `dev` de cada mes por la compuerta
(`casos_ocultos` veta cualquier caso reservado o retirado, :145 y :153-156) y, de cada fichero
`knowledge/cases/dev/<caso>.yaml`, sus `operaciones`. Cada operación trae `instante_utc`,
`sesion`, `direccion`, `entrada` y `stop` (`cases/ingesta.py:116-121`; claves comprobadas en un
caso dev de enero SIN leer valores: 7 operaciones con esas cinco claves). El arnés carga el stop
por `visor._stops` (`engine/visor.py:239-251`) y `simulacion._del_trader` lo pone como primera marca
(`simulacion.py:208-227`); es lo que `test_cuenta_7_de_agosto.py:64-77` usa como stop inicial.

**Lo que el caso NO trae: la caja.** Solo entrada y stop. «Del 0 al 0,8» y «del 0 al 1» exigen
saber en qué nivel de la caja puso el trader el stop de su libro, y eso es justo lo que mide A-56
(ABIERTA): VIABILIDAD-COMISION.md (:76-79) lo tomó como el 1 (`initialSL` = el 1; D = entrada−stop;
0,8·D para el 0,8) y sus medianas 1,5 y 1,2 pips son D y 0,8·D con ese supuesto. El guion tiene que
declarar el supuesto y, como cuesta lo mismo, **contar las dos lecturas** (stop del libro = el 1, y
stop del libro = el 0,8), con los tres umbrales que pide el encargo (1,00, 1,83 y 2,00 pips): el
consultor ve de un vistazo cuánto depende la cifra de A-56 (decisión 5).

**Recuento previo (hecho hoy, antes de tocar nada dev)**, por un guion de la carpeta de trabajo
que solo cuenta y no imprime claves: `casos_reservados` 34 y `casos_ocultos` 34; por mes:
2026-05 13, 2026-06 11, 2026-09 10; **en los cuatro meses de construcción (2026-01, 04, 07, 08):
0 reservados**. Coincide con las filas del 2026-10-14 y del 2026-10-17 de HOLDOUT-EXPOSICIONES.

**El guion propuesto**: `docs/validation/anexos/MARGEN-LOTE/stops_cortos.py`, hermano de
`anexos/ENTRADA-JULIO/margen_p_d1.py` (lee el registro y el perfil; ninguna cifra dentro):
- carga `cargar_criterio`, `cargar_registro` y, por mes de `construccion`, `arnes.dias_de_construccion`
  (la compuerta); de cada operación, `D = |entrada − stop|` en pips (10 puntos de 0,00001, ADR-0071 §2);
- los umbrales salen del registro y del perfil, no del guion: `stop_volumen = riesgo_usd / (valor_pip
  × firma_volumen_max_lotes)` (1,00) y `stop_margen(P) = riesgo_usd / (valor_pip × lote_max(P))` para
  los dos precios de FTMO-P-D1 (1,83 y 2,00 con P = 1,10 y 1,20; también con el precio de la propia
  entrada de cada operación, que es lo exacto);
- por mes y en total: operaciones, y cuántas (y qué parte) tienen la distancia del lote por debajo de
  cada umbral, bajo las dos lecturas de A-56 (distancia del lote = 0,8·D si el stop del libro es el 1;
  = D si es el 0,8), y lo mismo para la distancia 0→1;
- `--noticias <csv>` y `--ventana-min 2` como argumentos (no son parámetros del registro): si se da
  el calendario, cuántas de esas operaciones tienen su `instante_utc` a ±ventana de una noticia;
- imprime solo recuentos y pips agregados por mes: ninguna fecha de operación, ningún precio.
- Agosto: sus `dev` salen del xlsx (PROJECT_STATE, Q). El trader da por bueno el backtest de agosto
  grabado en vídeo (S-16, ADR-0073 §5); que el xlsx sea «el otro» es lectura de la sesión, no su
  frase (ADR-0073:51-55, corrección a1 del revisor de activar-sesion-04). El informe lo dirá junto a
  la cifra de agosto con esas palabras, no con las del encargo.
No se corre hasta la respuesta a la PARADA; su lectura de los 76 casos dev se declarará en
HOLDOUT-EXPOSICIONES el día que corra.

### 1.d Las noticias: de dónde sale el calendario

- **La lista de eventos restringidos es de FTMO**, en su FAQ pública «Can I trade news?»
  (https://ftmo.com/en/faq/can-i-trade-news/, leída el 2026-10-17): «FTMO restricts order execution
  for 2 minutes before and 2 minutes after selected news releases» y «Restrictions for trading during
  selected news releases apply only to the Standard account type». La tabla de la FAQ da, para USD:
  Federal Funds Rate & Statement, Non-Farm Employment Change, Unemployment Rate & Wages, Advance GDP
  q/q, FOMC Meeting Minutes, CPI y/y; para EUR: Main Refinancing Rate. Y: «these restricted events
  are marked by the note “Restricted event“» en el Economic Calendar de FTMO.
- **Las fechas y horas de esos eventos en enero, abril, julio y agosto de 2026** no están en el
  repo ni en la FAQ. Fuente propuesta, por orden: (1) el Economic Calendar de FTMO (marca los
  restringidos) si deja ver meses pasados; (2) si no, ForexFactory (calendario público con histórico
  por mes; filtrar por esos nombres de evento y por USD/EUR, alto impacto). **Quién:** Aleks, en su
  navegador: descarga o copia a un CSV con `fecha_utc, hora_utc, divisa, evento` y lo deja en
  `corpus/noticias/` (fuera de git) con su sha256 anotado en el informe; la sesión no descarga nada
  (no es material del trader, pero es dato externo no revisado: entra por Aleks y se lee por
  argumento). El guion de §1.c lo lee con `--noticias`. Son ~7 eventos × 4 meses: cabe en una
  tabla a mano si hace falta.
- La medida solo informa (D7): el informe dará la cifra y no recomendará nada. Si Aleks no quiere
  bajarlo ahora, la medida queda sin fuente y va a la línea de A con quién la consigue.
- Fuentes consultadas por búsqueda web (secundarias, solo para localizar la FAQ): varias páginas de
  comparación de prop firms; ninguna se cita como fuente de nada.

### 1.e La medida 2: la cifra de partida y el campo que hay que añadir

**La cifra de partida, verificada en la salida commiteada de `main`**
(`docs/validation/anexos/SESGO-H4-COLOR/diaria.DIAGNOSTICO.a35=cierre_vela_contraria.a44=sin_tope.cuenta=diaria.txt`,
líneas 1620-1628, «### Rechazos por motivo»): `volumen_max_lotes` **96** (enero 18, abril 24, julio
20, agosto 34) y `precio_invalido` **11** (3, 4, 2, 2); `grep -c 'rechazada | volumen_max_lotes'`
sobre «### Ordenes» da también 96. Son las cifras del encargo. Frente a R3.1
(CORRIDA-CONSTRUCCION.md §3.12, línea 931): 100 por volumen (21, 24, 20, 35) y 11 por precio. El
informe sustituye la base por la de `main` porque desde ADR-0080 el sesgo es otro y es la salida
que el código de hoy reproduce.

**El campo.** «### Ordenes» lo escribe `engine/cableado.py` (`CABECERA_ORDENES`, :728-731;
`vida_de_las_ordenes`, :748-800; `_informe_ordenes`, :803-829), no `arnes.py` (el encargo y el
contrato lo decían al revés; corregido en el contrato, §1.h). Propuesta, cuatro columnas al FINAL de
cada fila, para que las aserciones por subcadena de `tests/unit/test_vida_de_la_orden.py` sigan
valiendo:

    ... | instante del resultado | lote | distancia (puntos) | margen requerido (USD) | margen libre al colocar (USD)

- `lote`: `o.lotes` (el pedido; es el que RN-027 redondeó);
- `distancia`: `|o.precio − o.stop|` en puntos;
- `margen requerido`: `o.lotes × contrato × (o.precio / escala) / firma_apalancamiento`, con el
  precio de la orden (al colocar, el ask del mercado difiere del precio de la orden en el spread:
  se declara la aproximación; el bróker nuevo usará el ask/bid, §1.b);
- `margen libre al colocar`: `cuenta.equity − margen de las posiciones vivas` en el instante de
  colocar, que el cableado conoce (`ctx.cuenta`); así la medida 2 cuenta con el margen libre real
  de cada orden, no con el saldo inicial.
Para ello `ReglasBroker` gana `apalancamiento: int | None` (del perfil, `firma_apalancamiento`;
`None` en los tests que no lo pasan) y `vida_de_las_ordenes` necesita la cuenta del día: la traza
del bróker (`TrazaBroker`) guardará, por orden, el margen libre al colocar. **Régimen de
`bloqueadas` (R3.1, CORRIDA-CONSTRUCCION.md §3.17, punto 1):** solo salida, ninguna decisión cambia,
test sintético en los dos sentidos (una orden con margen y una sin apalancamiento en el perfil, que
imprime `-`), `make check`, y las corridas repetidas con el `diff` de determinismo; si cambian
parejas, cobertura o precisión, PARADA.

**Cómo se cuenta la medida 2** (guion `anexos/MARGEN-LOTE/medida_2.py`, lee la salida por argumento,
como `patrones.py`): por mes, rechazos por `volumen_max_lotes` (por orden y por sesión), y órdenes
cuyo `margen requerido` supera (a) el margen libre al colocar, lo que FTMO rechazaría, y (b)
`lote_margen_libre_fraccion` × margen libre, lo que el bot limitará; por orden y por sesión
(una caja se recoloca varias veces, R3.1 §3.12).

### 1.f Los parámetros de D4, A-57 y los tests que cambian

**Los dos parámetros.** El perfil solo admite `prop_firm` y cada cifra cita una R de FTMO
(`engine/perfil_cuenta.py:129-141`; ADR-0050 §3; `test_perfil_cuenta.py:60-76`): ninguno de los
dos puede vivir en el perfil (el 0,95 es nuestro, no de FTMO). Van a `knowledge/spec/parametros.yaml`:
- `lote_si_no_cabe`: `ejecucion`, `enum`, `opciones: [limitar, no_operar]`, `DEFAULT_AMBIGUOUS`,
  `ambiguedad_id: A-57`, `consumido_por: [<ADR nuevo, 0081>]`, `fuente: {tipo: decision, id: <ADR nuevo, 0081>}`;
  mismo patrón que `cierre_pendientes` (`parametros.yaml:1792-1809`: `ejecucion`, DEFAULT_AMBIGUOUS
  bajo A-55, consumido por ADR-0068 y leído por el simulador, no por una regla). Es lo que se le
  pregunta al trader, pero su lectura la hace el cableado: `ejecucion` (categoría «qué hace el
  bróker/el bot al ejecutar»), no `estrategia`; si el consultor prefiere `estrategia`, nada cambia
  en el código.
- `lote_margen_libre_fraccion`: `ejecucion`, `decimal`, `0.95`, `minimo 0`, `maximo 1`, `CONFIRMED`,
  `consumido_por: [<ADR nuevo, 0081>]`, `fuente: {tipo: decision, id: <ADR nuevo, 0081>}`.
- `comprobar_consumo` (`spec/modelo.py:794-856`) acepta un `consumido_por` con un ADR que exista:
  el ADR 0081 (el nuevo) existirá en el mismo commit. Sin regla que los nombre, `comprobar_decisiones` no interviene.
- `firma_apalancamiento`: en el perfil, `consumido_por: [<ADR nuevo, 0081>]` y descripción «lo consume el
  bróker simulado (margen, ADR nuevo 0081) y el pre-vuelo de la demo»; en `parametros.yaml`,
  `consumido_por: [<ADR nuevo, 0081>, F33]` y la frase «F21 lo comprueba…» sustituida por «el bróker simulado
  lo comprueba (ADR nuevo 0081); la ejecución 2 de la demo comprueba la fórmula (FTMO-P-D1.md §3)». Siguen
  citando R9. `test_perfil_cuenta.py:105-119` solo cruza tipo, valor y opciones: las descripciones y
  `consumido_por` pueden diferir, y por eso difieren hoy.
- `firma_tamano_posicion_ratio_aviso` (G.3): la descripción pasa a decir que FTMO respondió sin cifra
  (FTMO-REGLAS.md, respuesta 10, 2026-10-05) y que «sustancialmente mayor» depende del histórico del
  propio trader; sigue `UNKNOWN` (congelado por `test_perfil_cuenta.py:60-76`) y sigue citando R17.
- **Cómo lee la spec el tope de volumen: no lo lee.** Lo lee el cableado desde `ReglasBroker`
  (perfil → `reglas_broker_de`), como hoy el bróker. Alternativa (regla nueva RN-037 con acción
  `limitar_lote`): obliga a duplicar `firma_volumen_max_lotes` en `parametros.yaml` (cruzado por
  `test_perfil_cuenta.py:110`), a una `cita` + `literal` del trader que no dice nada del límite
  (`comprobar_literales`; sería relleno, deuda ya conocida en RN-029..032) y a `decision: <ADR nuevo, 0081>`
  (`comprobar_decisiones`): tres costes por una visibilidad que ADR-0068 ya resolvió de la otra
  manera. Decisión 1.

**A-57.** La siguiente libre es A-57 (última A-56, `ambiguedades.yaml:1704`; ADR siguiente 0081:
`docs/adr/` acaba en 0080 y ningún fichero nombra 0081). Clase `pregunta`, no bloqueante,
`resuelve_en: [F24]`. **Lo que exige el esquema** (`cases/ambiguedades.py:191-206`): una `pregunta`
cita al menos un ítem de evidencia del trader y no admite `fuentes_documentales`. **Lo que encontró
la búsqueda en el corpus citable** (CLI filtrada; `kb find` ocultó 4.631 segmentos: 4.409 por
cuarentena, 121 por tramo no citable, 101 por material reservado, y 2 ítems de evidencia):
- `apalancamiento`: 0 resultados. `lotes`: 0. `lote` por prefijo, junto a «cabe», «máximo»,
  «bróker», «cuenta», «fondeo» o «FTMO»: 0. `margen`: 15 ítems, todos «margen de beneficio»,
  «margen para que se desarrolle el precio» o el margen del stop con noticias; ninguno del margen
  del bróker.
- `lotaje`: 20 ítems, todos de SOBRE QUÉ DISTANCIA se calcula (la base del lotaje, A-18 y ADR-0020).
  Los dos que hablan de su lote EN UNA CUENTA DE FONDEO: `ev-v4-002457-5a2e88c6` («he entrado sin
  lotaje o sea, han sido 3 que como tal no he entrado con el porcentaje de la cuenta») y
  `ev-v4-012900-8ef676ed` («estaba operando con algo fijo es un lotaje fijo, muy bajo», por falta de
  calculadora). Dicen lo que hizo con el lote en la prueba de fondeo; **no dicen qué hace cuando el
  lote de su riesgo no cabe**: ninguna frase del trader habla de eso.
- `knowledge/feedback/` y `knowledge/evidence/` por `grep`: ningún registro con «apalanc», «margen
  libre», «lote máximo» ni «no cabe».
Así que A-57 solo se abre como `pregunta` citando esos dos ítems de v4 como respaldo débil, dicho en
la propia pregunta (decisión 4). Y VIABILIDAD-COMISION.md (:3-5) «NO se enseña al trader»: ni A-57 ni
la pregunta de V llevan sus cifras ni su argumento de la esperanza; la pregunta se formula con la
cuenta y sus límites (50 lotes, 1:30), nada más.

**Los tests que cambian de resultado con el límite y el margen**, y cómo se rehacen sin rebajar lo
que comprueban (con el diseño de 1.a: el bróker comprueba margen SOLO si el cableado le pasa el
saldo y el perfil trae apalancamiento; sin ellos, como hoy):
- `tests/regression/test_cuenta_7_de_agosto.py` (2 tests, `data/` necesario): el primero (:80-97)
  espera `BrokerError` por `volumen_max_lotes` en `abrir_conocida` con el perfil real y >50 lotes;
  **no cambia** si el bróker mira el volumen antes que el margen y si se construye sin saldo. Gana
  un hermano: el mismo bróker CON saldo (100.000) y un lote que pasa el volumen pero no el margen
  (p. ej. 40 lotes a 1,17 piden 156.000 USD) → `BrokerError` por `margen_libre`. El segundo (:100-125)
  sube el volumen a 100 y abre con `abrir_conocida` operaciones de más de 50 lotes: con margen las
  rechazaría; sigue siendo la regresión del CORTE de la cuenta, así que se construye sin saldo (como
  ya declara `VOLUMEN_MAX_DE_LA_REGRESION`) y su docstring lo dice.
- `tests/unit/test_broker.py` (9 tests; `_broker` sin saldo): ninguno cambia. Ganan los de la
  fase 2 sobre `colocar_stop`/`colocar_limite` y `_aplicar` con saldo: justo por encima y justo por
  debajo, con una posición viva, ask/bid, pendiente que reserva margen.
- `tests/unit/test_broker_ordenes_stop.py` (14): ninguno cambia; gana el rechazo al llenar de una
  stop cuando el margen libre bajó entre colocar y llenar.
- `tests/unit/test_be_al_tick.py` (7) y `tests/unit/test_peticiones.py` (4): construyen
  `ReglasBroker(...)` por campos; `apalancamiento` entra con valor por defecto `None` y no cambian.
  Si el consultor prefiere apalancamiento obligatorio, los 11 ficheros que construyen `ReglasBroker`
  o `Broker` cambian una línea cada uno (lista en §1.h, h10).
- `tests/unit/test_vida_de_la_orden.py` (7): sus aserciones son por subcadena de la fila
  (`" | rechazada | precio_invalido | "`) y por igualdad de las filas de «### Rechazos por motivo»:
  con las columnas nuevas AL FINAL de «### Ordenes» no cambian; gana el test del campo (los dos
  sentidos). La sección de rechazos gana la fila `llenar` cuando exista un rechazo al llenar.
- `tests/unit/test_perfil_cuenta.py`: `consumido_por` y descripciones no se cruzan (:115); nada cambia.
  `test_kit.py`: la tabla de PROJECT_STATE gana la fila de A-57 (`:458-473`).
- Tests nuevos de la fase 2 (lista del encargo), todos en rojo sobre `main` antes del código.

### 1.g Lectura de material de las corridas

Como declaró R3.1 (HOLDOUT-EXPOSICIONES.md, fila del 2026-10-14, punto 2) y repitió R1.2 (fila del
2026-10-17): las corridas de `motor arnes --simular` leen, para calentar el sesgo H4
(`engine/arnes.py:179-215`: el M1 del mes anterior si existe su dataset), el M1 **entero de marzo**
(mes reservado entero) para abril y el **entero de junio** (11 días reservados) para julio; para
enero no hay M1 de 2025-12 en `data/manifests/` (enero calienta desde su propio mes). Cada corrida
(la de la fase 1 y las tres de la fase 4) llevará su fila el mismo día y ANTES de correr. Ninguna
salida ni este informe imprimirá fechas fuera de los días dev de construcción, salvo la línea de
cobertura del calendario de cierres, como en R3.1.

### 1.h El encargo frente al repo (auditor, 2026-10-17)

El agente `auditor-encargo` contrastó 66 afirmaciones: 47 correctas, 2 incorrectas y 17 con matiz;
y 13 cosas que el repo pide y el encargo no dice. Lo que cambia el trabajo (lo demás, en su informe,
resumido aquí por número):

| # | Qué | Veredicto | Evidencia |
|---|---|---|---|
| h1 | «Agosto sale del xlsx que el trader ya no da por bueno» | INCORRECTA la atribución | ADR-0073:51-55: que el xlsx sea «el otro» es lectura de la sesión. §1.c lo dice con esas palabras |
| h2 | «G.3 pasa a HECHA» tal cual | INCORRECTA | G.3 lleva `HER:27` (HOJA-DE-RUTA.md:344) y el 27 sigue vivo: `test_hoja_de_ruta.py:151-153` falla. Hay que quitar `HER:27` de G.3 en el commit del contrato |
| h3 | «A.2 queda con “el heredado 37 decidido” cumplido» | MATIZ | A.2 lleva `HER:37` (:268) y no es HECHA: con el 37 fuera falla «no es un heredado vivo» (:154-155). Hay que quitar `HER:37` de A.2 |
| h4 | «A-57 entra en los Refs de R4.1» | MATIZ | R4.1 lleva `NA:E` en Refs (:171) y en «Depende de» (:183): con E fuera falla «no es una letra viva» (:148-149). Hay que quitar `NA:E` de los dos sitios; y V dice «Depende de … E y O» (PROJECT_STATE.md:57): «de E» sale |
| h5 | «el heredado 37 sale con el criterio (a)» | MATIZ | Su texto (HISTORIA.md, Archivo 33) incluye «La ejecución 2 de la demo comprueba la fórmula … (MargenAlcanza)», que esta rama no hace: decisión 6 |
| h6 | D2: «Si la cita sostiene “no se opera”…» | la cita NO lo sostiene | §1.a; decisión 0 |
| h7 | D5: A-57 como `pregunta` | solo con evidencia del trader | §1.f; decisión 4 |
| h8 | Medida 1 «del 0 al 0,8 y del 0 al 1» | depende de A-56 | §1.c; decisión 5 |
| h9 | «### Ordenes» vive en `cableado.py`, no en `arnes.py`; su test es `test_vida_de_la_orden.py`, que no estaba en el contrato | CORRECTA | contrato corregido en el commit de apertura: comentario de `arnes.py` y `tests/unit/test_vida_de_la_orden.py` en `rutas_permitidas` |
| h10 | Seis ficheros de test más construyen `Broker` fuera del contrato (test_cableado, test_cierres_de_mercado, test_freno_peticiones, test_racha_perdidas, test_simulacion, test_diferencias_por_operacion) | CORRECTA | no cambian con el diseño de 1.a (saldo y apalancamiento opcionales); si la decisión 2 los hace obligatorios, se amplía el contrato en ese commit |
| h11 | ADR-0026:123 repite la frase falsa «F21 lo comprueba con la distribución real de cajas», y ADR-0026 está protegido | CORRECTA | decisión 7 |
| h12 | ADR-0052 §4 «solo prevé rechazos al colocar» | MATIZ | §4 no dice el instante; «rechazada en el acto» está en §1 (:28-30), y el bróker ya rechaza al MODIFICAR (ADR-0057). El recuadro de el ADR 0081 (el nuevo) irá en §4 y nombrará §1 |
| h13 | Un rechazo al llenar no es petición (R13) | lo pide el repo | §1.a y §1.e: columna `peticion` = `llenar`, sin `Peticion` |
| h14 | `primitivas_broker.py:492` → el `max` está en :493; `comprobar_decisiones` va de :423 a :455 | MATIZ (líneas) | §1.a |
| h15 | PROJECT_STATE «23.396 bytes» | MATIZ | es la cifra de `main`; la apertura lo deja en 23.597 (+201, la frase de Current Feature). La fila de A-57 sumará ~150; tope 25.000 |
| h16 | El encargo va fechado el 2026-10-18; el reloj de la máquina al abrir dio 2026-10-17 20:39 | MATIZ | las fechas factuales de la apertura, de este informe y de HOLDOUT-EXPOSICIONES son 2026-10-17 (corregido antes del primer commit) |
| h17 | «Dado por Aleks (consultor)» en la cabecera del encargo | MATIZ menor | ADR-0072: el consultor es Claude en el chat y Aleks quien lo da; es la cabecera habitual |
| h18 | «Los tres comandos de R3.1 tal cual» | MATIZ | R3.1 corrió además la repetición de la 2 fuera del repo para el `diff` de determinismo: se hará igual |
| h19 | «trailer Fuente: con los ids nuevos» | MATIZ | solo vale el id del ADR nuevo (0081) (`ev-*`, `fb-*`, `ADR-NNNN`); A-57 no es un id de Fuente |

Lo que el auditor no pudo comprobar y sí comprobó la sesión: la documentación de MT5 (§1.b), el run
de la CI (§0, con `gh`), la búsqueda en el corpus (§1.f) y que la vía del arnés trae entrada y stop,
no la caja (§1.c).

### 1.i Lo que no pude medir

- **Cuándo comprueba MT5 el margen de una pendiente stop**: la página lo implica («charged for each
  order») pero no lo enuncia; se mide en la demo (ejecución 3, línea para A).
- **El margen libre real que FTMO aplicaría a una posición cubierta** (hedging, ADR-0071 §2): con
  `firma_ordenes_simultaneas_max = 1` no hay dos posiciones vivas y no hace falta hoy; el bróker
  sumará el margen de todo lo vivo (lo conservador) y lo dirá.
- **Las fechas de las noticias restringidas** de los cuatro meses: sin el calendario (§1.d).
- **Cuántas órdenes rechazaría el margen**: exige el campo de §1.e y la corrida de la fase 1.

### 1.j Exposiciones de hoy (declaradas en `HOLDOUT-EXPOSICIONES.md`, fila del 2026-10-17)

Ninguna sobre material reservado. Lo leído: la salida commiteada de `main` de la corrida diaria de
R1.2 (días dev; recuentos y la cabecera de «### Ordenes»), las claves de un caso dev de enero (sin
ningún valor), el corpus por la CLI filtrada (`kb find`, que ocultó 4.631 segmentos y 2 ítems), los
registros de `knowledge/feedback/` y `knowledge/evidence/` por `grep` (texto citable), y los
recuentos de `casos_reservados` y `casos_ocultos` por mes sin imprimir claves (§1.c). El auditor solo
leyó el repo (sin `botsito`, sin `gh`, sin web). Dos páginas web públicas (MT5 y la FAQ de FTMO).

## Lo que necesito que decidas

0. **El lote por debajo del mínimo (D2).** La cita de RN-027 (`fb-2026-09-09-sesion-01-17ed6193`,
   «el 0.5% de riesgo de la cuenta se calcula sobre el nivel 0.8») NO sostiene «no se opera»: habla
   de dónde sale el lote; RN-027 lo escribe en sus notas y ADR-0016 (su `decision`) solo decide la
   dirección del redondeo. PARADA, como pedía D2. Opciones: (a) el código pasa a «no se opera» por
   DECISIÓN del consultor en el ADR 0081 (el nuevo) (no por la cita): `redondear_lote` deja el lote en `None` por
   debajo del mínimo, `colocar_orden_limite` no envía y lo anota (hoy lanza `CableadoError`), y
   ADR-0053 (tabla, línea 39) gana su recuadro; la prosa de RN-027 no cambia y sus notas dicen que lo
   decide el ADR 0081 (el nuevo). (b) La prosa de RN-027 pasa a decir lo que hace el código («sube al mínimo»),
   ADR-0053 intacto. Recomiendo (a): subir al mínimo arriesga MÁS que `riesgo_por_operacion`, lo
   contrario de limitar; y en la práctica no muerde (el lote del 0,5 % baja de 0,01 solo con un stop
   de 5.000 pips o un saldo ínfimo). Coste de (a): un camino «no se coloca» nuevo en el cableado, que
   de todos modos pide `lote_si_no_cabe = no_operar`.
1. **Dónde va el límite del bot.** Opciones: (a) en la preparación de la orden
   (`colocar_orden_limite`, cableado), leyendo los dos parámetros del registro (`ejecucion`,
   `consumido_por: [<ADR nuevo, 0081>]`, el patrón de `cierre_pendientes`/ADR-0068) y el tope y el
   apalancamiento del perfil vía `ReglasBroker`; RN-011 y RN-027 no cambian de forma. (b) Una regla
   nueva RN-037 (gate, `decision: <ADR nuevo, 0081>`) con acción `limitar_lote`: exige duplicar
   `firma_volumen_max_lotes` en `parametros.yaml` y una cita del trader de relleno. Recomiendo (a).
   Coste de (a): la decisión no se ve en `strategy_spec.yaml` más que en las notas de RN-011/RN-027;
   la ve el ADR y el registro.
2. **Cómo le llega la equidad al bróker.** Opciones: (a) `Broker(..., saldo=None)` con un
   `Callable[[], Decimal]` que el cableado pasa (`lambda: cuenta.saldo`); equidad = saldo() +
   `flotante()` al tick; `ReglasBroker.apalancamiento: int | None`; sin saldo o sin apalancamiento,
   el bróker no comprueba margen y LO DICE en la traza (`margen: sin comprobar`); un test exige que
   `construir_motor_cableado` lo pase siempre. (b) Obligatorios: 11 ficheros de test cambian y seis
   entran al contrato. Recomiendo (a): el arnés siempre lo pasa y los tests de bróker aislado siguen
   probando lo suyo. Coste de (a): un bróker construido a mano sin saldo no rechaza por margen.
3. **El instante del margen (D3).** La página de MT5 dice que una stop colocada tiene su margen
   cargado («charged for each order») y no enuncia el instante de la comprobación. Opciones:
   (a) comprobar al colocar (con el ask/bid del mercado en ese instante) Y al llenar (con el precio
   del llenado), y contar la pendiente stop como margen usado; (b) solo al llenar. Recomiendo (a):
   es lo que la frase sostiene y el supuesto conservador que D3 pedía si no lo decía.
4. **A-57 sin cita que la sostenga.** Opciones: (a) abrirla como `pregunta` citando
   `ev-v4-002457-5a2e88c6` y `ev-v4-012900-8ef676ed` (lo que hizo con el lote en su prueba de
   fondeo), y que la propia `pregunta` diga que ninguna frase del trader habla del lote que no cabe
   y que la búsqueda se hizo (§1.f); (b) no abrir A-57: `lote_si_no_cabe` nace CONFIRMED por decisión
   y la pregunta va a V solo por la lista de CORRIDA-CONSTRUCCION §4.5. Recomiendo (a), que es lo que
   pide D4/D5 y deja la pregunta en la hoja de la sesión 5. Coste de (a): una cita de respaldo
   débil más, declarada (como las de RN-029..032).
5. **La medida 1 y A-56.** El caso trae entrada y stop, no la caja. Opciones: (a) contar las dos
   lecturas (el stop del libro es el 1 → la distancia del lote es 0,8·D; el stop del libro es el 0,8
   → es D) y publicar las dos tablas con el supuesto delante; (b) solo la lectura de
   VIABILIDAD-COMISION (el 1). Recomiendo (a): mismo coste y enseña cuánto depende de A-56.
6. **El heredado 37 en el cierre.** Su texto incluye «La ejecución 2 de la demo comprueba la fórmula
   con el margen de 1,00 lote que ya escribe el script 1.1 (MargenAlcanza)», que esta rama no hace.
   Opciones: (a) sale entero por el criterio (a), y la línea nueva de A dice «la ejecución 2
   comprueba la fórmula con MargenAlcanza y la 3 mide cuándo comprueba MT5 el margen de una
   pendiente»; (b) se queda hasta la ejecución 2. Recomiendo (a): lo que queda vivo está en A.
7. **ADR-0026:123** repite «F21 lo comprueba con la distribución real de cajas». Opciones: (a) un
   recuadro de corrección en ADR-0026 (ampliar el contrato con ese fichero); (b) dejarlo y que
   el ADR 0081 (el nuevo) lo nombre. Recomiendo (a): es la regla de los informes cerrados aplicada a un ADR, y la
   frase falsa es la misma que se corrige en `parametros.yaml`.
8. **Las tres líneas de la hoja de ruta que faltan en el cierre** (h2-h4): quitar `HER:27` de G.3,
   `HER:37` de A.2 y `NA:E` de R4.1 (Refs y «Depende de»), y «de E» de V. No es una opción: sin
   ellas `test_hoja_de_ruta.py` deja `main` en rojo. Pido tu conformidad para incluirlas en «Líneas
   preparadas para el commit del contrato».

Espero tu respuesta a la PARADA.


### 1.k Respuesta del consultor a la PARADA (2026-10-17)

Copiada tal cual (también al final de `docs/encargos/trabajo-margen-lote.md`):

> Modelo: Fable 5.1 · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA de la fase 0 de trabajo/margen-lote (2026-10-17). Cópiala tal cual al final del encargo y en MARGEN-LOTE.md, y aplícala punto por punto con la skill fase-cero.
>
> 0. Lote por debajo del mínimo: (a). «No se opera» por DECISIÓN del consultor en ADR-0081, no por la cita de RN-027, con recuadro en ADR-0053 (tabla, línea 39). Por qué: subir al mínimo arriesga más que riesgo_por_operacion, lo contrario de limitar. El camino «no se coloca» es el mismo que usa lote_si_no_cabe = no_operar: uno solo, que anota el motivo y no lanza CableadoError.
>
> 1. Dónde va el límite del bot: (a), en la preparación de la orden, con los dos parámetros en parametros.yaml como ejecucion (patrón de cierre_pendientes y ADR-0068) y el tope de volumen y el apalancamiento por ReglasBroker desde el perfil. Por qué: no duplica firma_volumen_max_lotes ni inventa una cita del trader. Las notas de RN-011 y RN-027 dicen que el lote colocado puede quedar por debajo del de RN-011 por ADR-0081.
>    Además: el margen requerido y el margen libre se calculan en UNA sola función (dominio o engine, donde no rompa import-linter), y la usan el límite del bot y el rechazo del bróker, con el mismo precio (ask en compras y bid en ventas del instante). Por qué: si cada uno calcula el suyo, pueden discrepar y el bot colocaría órdenes que el bróker rechaza por un céntimo. Si el bot ve la equidad por marcas de minuto y el bróker al tick, el colchón de 0,95 absorbe la diferencia: dilo en el ADR.
>
> 2. La equidad del bróker: (a) con un cambio. El saldo llega como callable (lambda: cuenta.saldo) y ReglasBroker gana apalancamiento: int | None. Pero se niega por defecto: si ReglasBroker trae apalancamiento (el perfil real), el saldo es OBLIGATORIO y construir el bróker sin él es un error; solo sin apalancamiento (tests de bróker aislado que no lo pasan) no se comprueba el margen. Nada de «margen: sin comprobar» en silencio con el perfil real. Por qué: la condición tiene nombre (la cuenta declara apalancamiento) y lo demás se niega. test_cuenta_7_de_agosto.py, segundo test, es la regresión del corte de la cuenta: se construye con apalancamiento=None explícito y su docstring lo dice. El test de que construir_motor_cableado pasa siempre el saldo, como propones. Si esto obliga a tocar ficheros de test fuera del contrato, amplía el contrato en ese commit y dilo.
>
> 3. El instante del margen: (a). Al colocar, con el ask o el bid del mercado; al llenar, con el precio del llenado; y la pendiente stop cuenta como margen usado mientras vive. Por qué: es lo que sostiene la frase de MT5 y el supuesto conservador de D3. Cuida el orden en la reubicación (ADR-0074): la cancelación de la orden vieja libera su margen antes de calcular el lote de la nueva, en el mismo cierre; un test lo comprueba. El rechazo al llenar no es una Peticion (R13): columna peticion = llenar, como propones.
>
> 4. A-57: (a). Abrirla como pregunta citando ev-v4-002457-5a2e88c6 y ev-v4-012900-8ef676ed. La propia pregunta dice que ninguna frase del trader habla del lote que no cabe y que la búsqueda se hizo (§1.f). Y la formulas sin cifras ni argumentos de VIABILIDAD-COMISION, solo con la cuenta y sus límites (50 lotes, 1:30). Por qué: deja la pregunta en la hoja de la sesión 5 y lo débil queda declarado.
>
> 5. Medida 1: (a), las dos lecturas de A-56 con el supuesto delante de cada tabla. Por qué: el mismo coste, y enseña cuánto depende la cifra de A-56. El guion stops_cortos.py, como lo propones; su lectura de los casos dev se declara en HOLDOUT-EXPOSICIONES el día que corra.
>
> 6. Heredado 37: (a). Sale entero por el criterio (a), y la línea nueva de A dice: «la ejecución 2 comprueba la fórmula del margen con MargenAlcanza, y la 3 mide cuándo comprueba MT5 el margen de una pendiente stop». Por qué: lo que queda vivo ya está en A.
>
> 7. ADR-0026:123: (a), recuadro de corrección en ADR-0026, con el contrato ampliado a ese fichero. Por qué: es la misma frase falsa que se corrige en parametros.yaml, y ya hay precedente de recuadros de enmienda en ADR anteriores (ADR-0075 sobre ADR-0060).
>
> 8. Hoja de ruta: conforme. Entran en las «Líneas preparadas para el commit del contrato»: quitar HER:27 de G.3, HER:37 de A.2 y NA:E de R4.1 (en Refs y en «Depende de»), y «de E» en la V de PROJECT_STATE. Gracias por cazarlas antes del cierre.
>
> Además:
> - §1.i dice «con firma_ordenes_simultaneas_max = 1 no hay dos posiciones vivas». Es incorrecto: firma_ordenes_simultaneas_max vale 200 (perfil, ADR-0050), y el que vale 1 es operaciones_simultaneas_max (parametros.yaml, estrategia). Corrígelo en el informe con su nombre y di si operaciones_simultaneas_max impide de verdad tener a la vez una posición viva y una pendiente stop de otro escenario. Si no lo impide, el margen sumado de las dos es justo lo que cubre el punto 3.
> - Las noticias: el CSV lo hace Aleks a mano si quiere, y es opcional. Si está en corpus/noticias/ antes de correr la medida 1, se usa con su sha256 en el informe; si no, la medida queda sin fuente y va una línea a A («Aleks: calendario de las noticias restringidas de FTMO de los meses de construcción»). La rama no lo espera.
> - La repetición de la corrida 2 fuera del repo para el diff de determinismo (h18): sí, en la fase 1 y en la fase 4, como R3.1.
>
> Lo que sigue: la fase 1 (el campo de 4.e con su test, make check sellado, la corrida «antes» con su fila de exposiciones, y las medidas 1 y 2), y luego las fases 2 a 4 sin parar, salvo que una medida contradiga lo decidido aquí o que las parejas o la precisión cambien en la corrida «antes», que solo añade salida. En ese caso, PARADA.
>
> Rama lista para revisión, NO cerrada.

**Corrección a §1.i (punto «Además», primero).** Lo que vale 1 es `operaciones_simultaneas_max`
(`parametros.yaml:948-952`, `estrategia`; lo lee RN-018, `strategy_spec.yaml:1785-1805`);
`firma_ordenes_simultaneas_max` vale 200 (perfil, :307). ¿Impide `operaciones_simultaneas_max`
tener a la vez una posición viva y una pendiente stop de otro escenario? **Sí, pero no por sí
solo:** RN-018 (`operaciones_abiertas_alcanzan`, `primitivas_broker.py:181-185`) cuenta
POSICIONES vivas y prohíbe `abrir_operacion` cuando llegan al tope, así que no mira pendientes; lo
que impide la pendiente con posición viva es el `ninguno_de` de RN-011
(`strategy_spec.yaml:1486-1489`: no prepara una orden si hay `orden_limite_pendiente` u
`operacion_abierta`, los dos hechos del bróker). Con las dos reglas vigentes, el bot nunca tiene una
pendiente y una posición a la vez, ni dos pendientes. Aun así, el bróker suma el margen de todo lo
vivo (posiciones y pendientes stop), como pide el punto 3, porque hace de FTMO y no de la spec.

**Aplicación punto por punto:** 0 → fase 3 (camino «no se coloca» único); 1 → fases 1 y 3 (una
sola función de margen en `engine/broker.py`, usada por la salida de la fase 1 y por el límite y el
rechazo de la fase 3); 2 → fase 3 (apalancamiento en `ReglasBroker` desde la fase 1 para la salida;
el saldo obligatorio con apalancamiento, en la fase 3); 3 → fase 3, con el test de la reubicación;
4 → fase 3 (A-57); 5 → fase 1 (`stops_cortos.py`); 6, 7 y 8 → las líneas del cierre (§6) y el
recuadro de ADR-0026 en la fase 3 (contrato ampliado en ese commit); noticias: `corpus/noticias/`
no existe hoy (`ls`), la medida queda sin fuente y va la línea a A; el `diff` de determinismo en las
fases 1 y 4.

## 2 · Fase 1 · Medidas antes del cambio (2026-10-17)

### 2.a El campo de «### Ordenes» (4.e), solo salida

Cinco columnas al FINAL de cada fila de «### Ordenes» (`engine/cableado.py`, `CABECERA_ORDENES`):
`lote` (el pedido, ya redondeado por RN-027), `distancia (puntos)` (de la orden a su stop),
`margen requerido (USD)`, `margen libre al colocar (USD)` y `riesgo (% del saldo)`. Las tres
últimas las anota `colocar_orden_limite` (`engine/primitivas_broker.py`, `_margen_al_colocar`) en
el instante de colocar, ANTES de llamar al bróker, en `ContextoDia.margen_al_colocar`, que es el
mismo diccionario que `TrazaBroker.margen_al_colocar` lee para el informe; `-` en lo que no se pudo
medir (perfil sin apalancamiento, minuto sin precio). Lo que hace falta para medirlas, y es lo
único de código que entra en esta fase:

- `ReglasBroker.apalancamiento: int | None` (`engine/broker.py`), que `reglas_broker_de`
  (`engine/simulacion.py`) lee del perfil (`firma_apalancamiento`, 30 en FTMO) o deja en `None` si
  el perfil no lo declara o no le da valor (el sintético de `tests/fixtures/cuentas/`).
- **La única función de margen** (respuesta, punto 1): `broker.margen_requerido(lotes, precio,
  escala, contrato, apalancamiento)` = lotes × contrato × precio / apalancamiento, en la moneda de
  la cuenta. La usan esta salida y, en la fase 3, el límite del bot y el rechazo del bróker.
- `Broker.precio_de_conversion(lado, instante)`: el ask en una compra y el bid en una venta del
  último tick anterior al instante (con respaldo M1, el cierre más el spread supuesto en la compra):
  la lectura inversa de `_precio_de_mercado`, que da el precio al que se marca la posición.
- `Broker.margen_usado()`: el margen de cada posición abierta a su entrada y de cada pendiente STOP
  a su precio («charged for each order», §1.b). El margen libre al colocar es `cuenta.equity −
  margen_usado()`; la equidad de la cuenta va por marcas de minuto y el flotante del bróker al tick:
  es la diferencia que el colchón de 0,95 absorbe (respuesta, punto 1; va al ADR).
- El riesgo: lote × distancia × contrato / saldo, en %.

**Ninguna decisión cambia**: el bróker no rechaza nada nuevo, el lote es el mismo, y lo único que
ve el intérprete es lo de siempre. Régimen de `bloqueadas` (R3.1): el test en los dos sentidos vive
en `tests/unit/test_vida_de_la_orden.py`: (1) con el perfil de FTMO, la fila de la orden llenada del
día sintético de `test_cableado` acaba en `31.25 | 16 | <margen al ask> | 100000.00 | 0.500` (0,5 %
de 100.000 sobre 16 puntos son 31,25 lotes, y a 1,10 piden unos 114.586 USD: **más margen del que
tiene la cuenta**, el caso de la medida 2 en miniatura); (2) con `apalancamiento=None`, las dos
columnas de margen dicen `-` y el lote, la distancia y el riesgo siguen saliendo. El test que monta
la traza a mano (`viva al cerrar el dia`) comprueba que sin anotación las tres van en `None`.
Las aserciones por subcadena de los demás tests no cambian; `p4_ordenes.py` y `patrones.py` de los
anexos de R3.1 indexan las columnas por posición desde el principio y no se ven afectados.

**El ADR-0081 entra en este commit, antes del código de la fase 3, y por qué.** El primer
`make check` de esta fase salió en rojo (5 tests) porque `knowledge validate` niega todo id citado
que no exista («id citado que no existe: … ADR-0081»), y el id está en la respuesta del consultor,
copiada tal cual en el encargo y en §1.k. La salida que no toca la copia literal es que el ADR
exista: `docs/adr/0081-el-lote-que-no-cabe-se-limita-y-el-broker-rechaza-por-margen.md` recoge las
decisiones D1-D7 y las ocho respuestas de la PARADA (ya tomadas; las medidas no las cambian), con
sus recuadros en ADR-0052 §4, ADR-0053 §1 (tabla, `redondear_lote`) y ADR-0026 (Impacto; el
contrato gana ese fichero, respuesta punto 7) y su fila del índice. Es trabajo de la fase 3
adelantado una fase; el código, la spec y A-57 llegan en la suya.

### 2.b La medida 1: los stops cortos del trader en construcción (`stops_cortos.py`)

Corrida el 2026-10-17 con la fila de exposiciones escrita antes (§1.j, fila de la fase 1): `uv run
python docs/validation/anexos/MARGEN-LOTE/stops_cortos.py --precios 1.10 1.20 --escribir
docs/validation/anexos/MARGEN-LOTE/stops_cortos.txt`. El guion lee por la compuerta del arnés
(`arnes.dias_de_construccion` sobre los meses de `construccion` del criterio, y el stop de cada
operación por `visor._stops`, como `simulacion._del_trader`), tras comprobar que `casos_reservados`
da 0 en los cuatro meses (34 reservados en total, ninguno en construcción), e imprime solo recuentos
y medianas por mes. Las cifras salen del registro y del perfil (0,5 % de 100.000 = 500 USD; pip =
10 USD por lote; 50 lotes; 1:30); los precios de referencia (1,10 y 1,20, los de FTMO-P-D1.md §2)
llegan por argumento. **198 operaciones del trader con stop** (abril 35, julio 67, agosto 42, enero
54). Umbrales: el tope de volumen admite el lote del riesgo hasta un stop de **1,00** pips; el
margen con todo el saldo, hasta **1,83** (a 1,10) y **2,00** (a 1,20).

El caso trae entrada y stop, no la caja (§1.c), así que van las dos lecturas de A-56 (respuesta,
punto 5). «lote» es la distancia sobre la que se dimensiona el lote (0 → 0,8); «0→1», la caja.

**Lectura A: el stop del libro es el 1 de la caja** (la de VIABILIDAD-COMISION.md: lote sobre
0,8 × D). Medianas: 1,44 pips la distancia del lote, 1,80 la caja (abril 1,20 y 1,50: las mismas
que VIABILIDAD-COMISION.md).

| mes | n | lote < 1,00 (volumen) | lote < 1,83 (margen a 1,10) | lote < 2,00 (margen a 1,20) | lote < margen al precio de la entrada | 0→1 < 1,00 | 0→1 < 1,83 | 0→1 < 2,00 |
|---|---|---|---|---|---|---|---|---|
| abril | 35 | 10 (29 %) | 27 (77 %) | 28 (80 %) | 28 (80 %) | 6 (17 %) | 23 (66 %) | 24 (69 %) |
| julio (1-17) | 67 | 9 (13 %) | 36 (54 %) | 40 (60 %) | 38 (57 %) | 3 (4 %) | 27 (40 %) | 30 (45 %) |
| agosto | 42 | 17 (40 %) | 35 (83 %) | 35 (83 %) | 35 (83 %) | 13 (31 %) | 30 (71 %) | 31 (74 %) |
| enero | 54 | 20 (37 %) | 39 (72 %) | 42 (78 %) | 42 (78 %) | 12 (22 %) | 34 (63 %) | 34 (63 %) |
| **total** | **198** | **56 (28 %)** | **137 (69 %)** | **145 (73 %)** | **143 (72 %)** | 34 (17 %) | 114 (58 %) | 119 (60 %) |

**Lectura B: el stop del libro es el 0,8** (lote sobre D; la caja es D / 0,8). Medianas: 1,80 la
distancia del lote, 2,25 la caja.

| mes | n | lote < 1,00 | lote < 1,83 | lote < 2,00 | lote < margen al precio de la entrada | 0→1 < 1,00 | 0→1 < 1,83 | 0→1 < 2,00 |
|---|---|---|---|---|---|---|---|---|
| abril | 35 | 6 (17 %) | 23 (66 %) | 24 (69 %) | 24 (69 %) | 5 (14 %) | 16 (46 %) | 19 (54 %) |
| julio (1-17) | 67 | 3 (4 %) | 27 (40 %) | 30 (45 %) | 29 (43 %) | 1 (1 %) | 15 (22 %) | 18 (27 %) |
| agosto | 42 | 13 (31 %) | 30 (71 %) | 31 (74 %) | 31 (74 %) | 8 (19 %) | 20 (48 %) | 21 (50 %) |
| enero | 54 | 12 (22 %) | 34 (63 %) | 34 (63 %) | 34 (63 %) | 8 (15 %) | 24 (44 %) | 26 (48 %) |
| **total** | **198** | **34 (17 %)** | **114 (58 %)** | **119 (60 %)** | **118 (60 %)** | 22 (11 %) | 75 (38 %) | 84 (42 %) |

Lo que dicen las dos: **el margen corta en la mayoría de las operaciones del trader** (entre el 58 %
y el 73 % según la lectura de A-56 y el precio), y el volumen en una de cada cuatro o seis. Julio es
el mes de stops más anchos; agosto y enero, los de más cortos. Agosto: sus `dev` salen del xlsx
(PROJECT_STATE, Q); el trader da por bueno el backtest de agosto grabado en vídeo (S-16, ADR-0073
§5), y que el xlsx sea el otro es lectura de la sesión, no su frase (ADR-0073:51-55). **Noticias:
sin fuente.** `corpus/noticias/` no existe (`ls`), así que el guion corrió sin `--noticias` y la
columna de ±2 minutos queda sin medir; va la línea a A («Aleks: calendario de las noticias
restringidas de FTMO de los meses de construcción», §6). Cuando llegue el CSV, el mismo comando con
`--noticias <csv> --ventana-min 2` la da, con su sha256 en la salida. Esta medida informa (D7): no
recomienda nada.

### 2.c La corrida «antes» y la medida 2 (`medida_2.py`)

Comando (2026-10-17, fila de exposiciones escrita antes, §1.j): `uv run botsito motor arnes
--simular --diagnostico-a35 cierre_vela_contraria --diagnostico-a44 sin_tope
--diagnostico-cuenta-diaria --salida docs/validation/anexos/MARGEN-LOTE/antes-diaria.txt` →
`antes-diaria.DIAGNOSTICO.a35=cierre_vela_contraria.a44=sin_tope.cuenta=diaria.txt` (1.717 líneas;
`TIEMPO: 294.5 s; MEMORIA: pico del proceso de 633.2 MiB`, por pantalla).

**Solo añade salida, medido:** un guion de la carpeta de trabajo comparó esta salida con la diaria
commiteada de `main` (`anexos/SESGO-H4-COLOR/diaria…txt`) quitando a las filas de «### Ordenes» las
cinco columnas nuevas: 1.717 líneas en las dos y **0 líneas distintas**. Parejas, cobertura
(12/198, 6,1 %) y precisión (12/94, 12,8 %) son las de R1.2; «### Rechazos por motivo» es el de
§1.e: `volumen_max_lotes` 96 (18, 24, 20, 34) y `precio_invalido` 11 (3, 4, 2, 2). Nada que
parar. La repetición fuera del repositorio para el `diff` de determinismo, en §2.d.

**La medida 2** (`uv run python docs/validation/anexos/MARGEN-LOTE/medida_2.py <salida> --fraccion
0.95 --escribir docs/validation/anexos/MARGEN-LOTE/medida_2.txt`; la fracción llega por argumento
porque `lote_margen_libre_fraccion` no existe todavía en el registro). Sobre las 437 órdenes de
«### Ordenes» (todas con margen medido), con el margen requerido al ask/bid del instante y el margen
libre de la cuenta en ese instante:

| mes | órdenes | rechazadas por volumen | margen FTMO: requerido > libre | de ellas, sin rechazo por volumen | bot: requerido > 0,95 × libre |
|---|---|---|---|---|---|
| enero | 133 | 18 | 72 | 54 | 77 |
| abril | 121 | 24 | 74 | 50 | 79 |
| julio (1-17) | 65 | 20 | 44 | 24 | 45 |
| agosto | 118 | 34 | 88 | 54 | 91 |
| **total, por orden** | **437** | **96 (22 %)** | **278 (64 %)** | **182** | **292 (67 %)** |

Por sesión (una caja se recoloca varias veces; sesiones con al menos una orden):

| mes | sesiones con órdenes | con rechazo por volumen | con alguna orden que el margen rechazaría | de ellas, sin rechazo por volumen | con alguna que el bot limitaría |
|---|---|---|---|---|---|
| enero | 31 | 13 | 28 | 24 | 28 |
| abril | 31 | 14 | 28 | 25 | 28 |
| julio (1-17) | 18 | 9 | 17 | 13 | 17 |
| agosto | 29 | 23 | 28 | 19 | 29 |
| **total** | **109** | **59** | **101** | **81** | **102** |

Lo que dice: **el margen corta casi el triple que el volumen** (278 órdenes frente a 96; 101
sesiones de 109 frente a 59), y de las 341 órdenes que hoy el bróker coloca (437 − 96), **182
(53 %) las rechazaría FTMO por margen**: hoy el simulador las coloca y las llena como si cupieran.
Es la cifra que sustituye a la base de E («cuántas órdenes de R3.1 rechaza el volumen y cuántas el
margen», CORRIDA-CONSTRUCCION.md §3.12: 100 por volumen), porque desde ADR-0080 el sesgo es otro y
esta es la salida del código de hoy. Con el límite de ADR-0081 (fase 3) esas órdenes pasan a
colocarse con el lote que cabe; la fase 4 mide cuántas y con qué riesgo efectivo.

### 2.d Determinismo

La corrida 2 repetida con `--salida` en una carpeta temporal fuera del repositorio (la misma
lectura, declarada en la fila de la fase 1): `sha256sum` de las dos salidas idéntico
(`9b168d2f86b55229e22e…`); `TIEMPO: 291.7 s; MEMORIA: pico del proceso de 633.0 MiB`. La copia no
se commitea.

## 3 · Fases 2 y 3 · Los tests en rojo, y el código, la spec y A-57 (2026-10-17)

### 3.a Los tests, antes del código

`tests/unit/test_margen_lote.py` (17 tests), escritos antes del código y corridos sobre el de la
fase 1 (`main` más el campo de salida): **16 FAILED, 1 passed** (el que pasa es el de la fórmula,
`margen_requerido`, que ya existía como única función desde la fase 1). Los 16 cubren la lista de
la fase 2 del encargo: el rechazo al colocar justo por encima y justo por debajo del margen libre;
la posición abierta que ocupa margen; la pendiente STOP que reserva y la cancelación que libera
(la reubicación de ADR-0074, respuesta punto 3); la compra al ask y la venta al bid; el rechazo al
LLENAR cuando el margen libre bajó desde que se colocó (sin petición, orden `rechazada`, evento en
la traza) y que la reserva de la propia orden no cuenta contra ella; `abrir_conocida` por margen
tras el volumen; la función pura `limitar_lote` (cabe: no cambia; por margen; por volumen; por los
dos; por debajo del mínimo: `None` y `minimo`); el día sintético de `test_cableado` con el lote
limitado por margen y colocado; el mismo resultado en R con y sin límite; `no_operar`: no se envía
y queda anotada en «### Ordenes no enviadas por el bot»; el cableado pasa siempre el saldo; y el
rechazo al llenar contado como `llenar` en «### Rechazos por motivo». Las 17 verdes con el código
de 3.b. Un ajuste al escribirlos: los tests sintéticos colocan sus órdenes en el segundo 0 del
minuto y el primer tick está en el 5, así que al colocar no había precio con el que convertir el
margen y el bróker lo niega («sin precio de mercado»); las órdenes de estos tests se colocan a
partir del segundo 10. El cableado real coloca en el último milisegundo del cierre de M1, con los
ticks del minuto ya presentes (la corrida «antes» midió margen en las 437 órdenes).

### 3.b El código (ADR-0081)

- `engine/broker.py`: `Broker(..., saldo: Callable[[], Decimal] | None)`; **con apalancamiento en
  las reglas y sin saldo, el bróker no se construye** (respuesta punto 2); `margen_libre()` =
  saldo() + flotante al tick − `margen_usado()`; `_margen_infringido(lotes, precio, libre_extra)`
  → `margen_libre`; en `_colocar`, tras los límites del perfil y el precio, con el ask o el bid del
  instante (`precio_de_conversion`); en `_aplicar(LLENADA)`, con el precio del llenado y sumando
  al margen libre la reserva de la propia orden si es una stop (`libre_extra`); un rechazo al
  llenar deja la orden `rechazada` (historial `colocada → rechazada`), un `Rechazo` en la traza y
  un evento `rechazada`, sin `Peticion`; en `abrir_conocida`, con el precio del llenado conocido.
  `lote_que_cabe` (la inversa de la fórmula) y **`limitar_lote`** (función pura: el menor de tres,
  al paso; `None` + `minimo` por debajo del mínimo; sin apalancamiento solo mira el volumen) y las
  constantes de los límites y de `lote_si_no_cabe`.
- `engine/primitivas_broker.py`: `redondear_lote` ya no sube al mínimo (respuesta punto 0);
  `colocar_orden_limite` resuelve el lote del riesgo, lo pasa por `_lote_final` (volumen del
  perfil; margen libre del bróker × `lote_margen_libre_fraccion` con el precio de conversión del
  instante: **el mismo margen libre y la misma función que usará el bróker al colocar**) y, si
  `lote_si_no_cabe = no_operar` y algún límite mordió, o si queda por debajo del mínimo, **no envía**:
  anota `(instante, zona, motivo, lote del riesgo)` en `ContextoDia.no_enviadas`, marca la zona usada
  y su punto rechazado (como un rechazo del bróker, ADR-0064) y no lanza `CableadoError`. Es el
  único camino «no se coloca» (respuesta punto 0). La anotación de margen gana el lote del riesgo
  y el límite que mordió.
- `engine/cableado.py`: el bróker nace con `saldo=lambda: cuenta.saldo`; «### Ordenes» gana dos
  columnas más al final (`lote del riesgo | limite`); sección nueva «### Ordenes no enviadas por el
  bot (dia | sesion | instante UTC | zona | motivo | lote del riesgo)» con su recuento; «### Rechazos
  por motivo» distingue `colocar`, `llenar` (la orden estuvo colocada) y `modificar`.
- Spec y knowledge: `lote_si_no_cabe` (`ejecucion`, enum, `limitar`, DEFAULT_AMBIGUOUS bajo A-57) y
  `lote_margen_libre_fraccion` (`ejecucion`, decimal, 0,95, CONFIRMED), ambos `consumido_por:
  [ADR-0081]` y fuente ADR-0081, detrás de `cierre_pendientes`; notas de RN-011 y RN-027; **A-57**
  (pregunta, no bloqueante, `resuelve_en: [F24]`, evidencia `ev-v4-002457-5a2e88c6` y
  `ev-v4-012900-8ef676ed`, con la búsqueda declarada en la propia pregunta y sin ninguna cifra de
  VIABILIDAD-COMISION) y su fila en PROJECT_STATE; el perfil (`firma_apalancamiento`: quién lo
  consume, `consumido_por: [ADR-0081]`; `firma_tamano_posicion_ratio_aviso`: la respuesta 10 de
  FTMO, G.3) y `parametros.yaml` (`firma_apalancamiento`: la frase de F21 sustituida,
  `consumido_por: [ADR-0081, F33]`); `spec_version` 18.0.0 → **18.1.0** (menor: dos parámetros,
  ninguna regla cambia de sentido); `spec manifest --escribir` y `spec docs --escribir`;
  `knowledge validate` sin errores.

### 3.c Los tests que cambiaron, y cómo se rehicieron sin rebajar lo que comprobaban

- `tests/regression/test_cuenta_7_de_agosto.py`: el primero (volumen) construye el bróker con el
  saldo inicial del perfil (obligatorio con apalancamiento) y sigue esperando `volumen_max_lotes`
  (el volumen se mira antes). Gana un hermano por el margen: el lote que ocupa exactamente todo el
  saldo al precio de entrada se abre, y un paso más (0,01) se rechaza con `margen_libre`. El segundo
  (la regresión del CORTE de la cuenta) se construye con `apalancamiento=None` explícito y su
  docstring dice por qué (respuesta punto 2).
- `tests/unit/test_cableado.py`: dos tests afirmaban el lote colocado (31,25 y 29,41): ahora
  afirman el lote del RIESGO en la anotación de la traza (lo que RN-011 y RN-027 producen, que es
  lo que comprobaban) y que el colocado es menor y cabe en el 95 % del margen libre; la comisión y
  la pérdida se calculan con el lote colocado.
- `tests/unit/test_vida_de_la_orden.py`: las filas esperadas ganan las dos columnas; el test con el
  perfil real espera el lote limitado, `31.25 | margen` y `no enviadas: 0`; el de la traza a mano
  espera `None, None` y `-`; el bróker a mano recibe el saldo.
- `tests/unit/test_racha_perdidas.py`: el bróker a mano con el perfil real recibe `saldo=lambda:
  cuenta.saldo` (la cuenta se crea antes).
- Sin cambios: `test_broker.py`, `test_broker_ordenes_stop.py`, `test_be_al_tick.py`,
  `test_peticiones.py`, `test_cierres_de_mercado.py`, `test_freno_peticiones.py`, `test_simulacion.py`
  (reglas sintéticas sin apalancamiento), `test_huecos_motor.py`, `test_diferencias_por_operacion.py`,
  `test_arnes_motor.py`, `test_preparar_a21.py`, `test_perfil_cuenta.py`, `test_kit.py` (la fila de
  A-57). El contrato gana `tests/unit/test_margen_lote.py`, `test_racha_perdidas.py` y
  `test_cableado.py` (respuesta punto 2: «amplía el contrato en ese commit y dilo»).

## 4 · Fase 4 · La re-corrida con el límite y el rechazo por margen (2026-10-17)

Hace falta porque el límite cambia lo que simula: los rechazos por volumen pasan a ser órdenes
colocadas. Fila de exposiciones escrita antes de correr (HOLDOUT-EXPOSICIONES.md, fila de la fase
4). Los tres comandos de R3.1 tal cual, salvo la carpeta de `--salida` (`anexos/MARGEN-LOTE/README.md`);
son corridas con `--diagnostico-*`: no cuentan ni habilitan mayo (ADR-0070 §3), no deciden ningún
parámetro y no se mide cobertura contra ningún umbral.

| corrida | TIEMPO | MEMORIA (pico) |
|---|---|---|
| 1 arrastrada | 480,2 s | 631,9 MiB |
| 2 diaria | 451,3 s | 634,6 MiB |
| 3 a35-inicio | 415,4 s | 633,7 MiB |

### 4.a Los rechazos por motivo, antes y después

| corrida | antes (`main` + campo, §2.c; R1.2 para la arrastrada) | después (ADR-0081) |
|---|---|---|
| 2 diaria | `volumen_max_lotes` 96 (18, 24, 20, 34); `precio_invalido` 11 (3, 4, 2, 2) | `volumen_max_lotes` **0**; `precio_invalido` **26** (6, 8, 4, 8) |
| 1 arrastrada | `volumen_max_lotes` 29 (enero 24, abril 5); `precio_invalido` 4 (3, 1) (R1.2) | `volumen_max_lotes` **0**; `precio_invalido` **2** (enero) |
| órdenes, diaria | 437: cancelada 224, llenada 106, rechazada 107 | **504**: cancelada 299, llenada **179**, rechazada 26 |
| órdenes, arrastrada | 126: cancelada 65, llenada 36, rechazada 25 | **124**: cancelada 76, llenada **46**, rechazada 2 |
| no enviadas por el bot | — | **0** en las dos (ningún lote por debajo del mínimo; `lote_si_no_cabe = limitar`) |
| `margen_libre` | — | **0** rechazos: el bot limita con el mismo margen libre que el bróker comprueba |

**Por qué sube `precio_invalido` de 11 a 26 en la diaria:** el bróker mira el volumen antes que el
precio (`broker.py`, `_colocar`), así que una orden que antes salía por `volumen_max_lotes` no
llegaba a la comprobación del precio. De los 16 rechazos por precio nuevos, **14 están en el mismo
día e instante que un rechazo por volumen de antes**; los otros 2, y el que desaparece (26 = 11 − 1
+ 16), son recolocaciones desplazadas porque la vida de las órdenes de la sesión cambió (una orden
colocada y llenada donde antes había un rechazo). Nada se ajusta: es la cifra.

### 4.b Las órdenes limitadas, y por qué límite (`fase4_medidas.py`, corrida 2)

| mes | órdenes | `ninguno` | `volumen` | `margen` | `volumen+margen` |
|---|---|---|---|---|---|
| enero | 150 | 62 | 0 | 68 | 20 |
| abril | 144 | 48 | 0 | 70 | 26 |
| julio (1-17) | 84 | 28 | 0 | 36 | 20 |
| agosto | 126 | 27 | 0 | 61 | 38 |
| **total** | **504** | **165 (33 %)** | **0** | **235 (47 %)** | **104 (21 %)** |

**339 órdenes de 504 (67 %) salen con el lote limitado**, en 102 sesiones de 104 con órdenes. El
volumen nunca muerde solo: cuando el lote del riesgo pasa de 50 lotes (stop < 1 pip), el margen a
1:30 también lo corta y más abajo (`volumen+margen`: 104); el margen solo, 235. Es lo que FTMO-P-D1.md
§2 anticipaba («el margen manda antes que el volumen») y la medida 2 contaba antes del cambio (278
órdenes que el margen rechazaría, §2.c; ahora son 339 limitadas porque hay más órdenes: las que
antes se rechazaban por volumen viven y se recolocan).

### 4.c El riesgo efectivo de las operaciones del bot (corrida 2)

Sobre las 478 órdenes colocadas (no rechazadas), con el riesgo en % del saldo al colocar que anota la
traza (lote × distancia × contrato / saldo):

| mes | n | con el 0,5 % entero (`ninguno`) | mediana | mínimo | máximo |
|---|---|---|---|---|---|
| enero | 144 | 61 | 0,462 % | 0,098 % | 0,500 % |
| abril | 136 | 48 | 0,390 % | 0,025 % | 0,500 % |
| julio (1-17) | 80 | 28 | 0,374 % | 0,100 % | 0,500 % |
| agosto | 118 | 27 | 0,321 % | 0,074 % | 0,500 % |
| **total** | **478** | **164 (34 %)** | **0,390 %** | **0,025 %** | **0,500 %** |

Dos de cada tres órdenes arriesgan menos del 0,5 %; la mediana queda en 0,39 % y el mínimo en
0,025 % (una orden de abril con el stop tan corto que el margen deja un lote veinte veces menor que
el del riesgo). Es la consecuencia que ADR-0081 §1 acepta a cambio de conservar la decisión y el
resultado en R: la cifra va a la sesión 5 con A-57.

### 4.d La tabla T0 y P1-P7 (`patrones.py` de R3.1 sobre la corrida 2), frente a SESGO-H4-COLOR.md §4.3

Salida completa en `anexos/MARGEN-LOTE/patrones.txt` (359 filas, 104 sesiones con rn003; R1.2: 292
filas, las mismas 104 sesiones).

| mes | P1 sesgo | P2 entrada | P3 otra zona | P4 sin orden | P5 de más | P6 trader no operó | P7 repetidas | T0 pareja |
|---|---|---|---|---|---|---|---|---|
| enero | 7 (7) | 13 (9) | 26 (22) | 6 (15) | 41 (30) | 8 (5) | 0 (0) | 2 (1) |
| abril | 9 (9) | 4 (2) | 11 (8) | 6 (12) | 22 (11) | 20 (16) | 0 (0) | 5 (4) |
| julio (1-17) | 20 (20) | 9 (3) | 14 (13) | 14 (23) | 24 (9) | 2 (2) | 3 (3) | 7 (5) |
| agosto | 8 (8) | 7 (4) | 9 (5) | 14 (23) | 25 (14) | 19 (7) | 0 (0) | 4 (2) |
| **total** | **44 (44)** | **33 (18)** | **60 (48)** | **40 (73)** | **112 (64)** | **49 (30)** | **3 (3)** | **18 (12)** |

(entre paréntesis, SESGO-H4-COLOR.md §4.3.) P1 no cambia (el sesgo es el mismo: 44 filas en 21
sesiones). Lo que cambia es lo que el bot hace cuando el lote cabe: **P4 (sin orden) baja de 73 a 40**
y se reparte entre P2, P3 y T0; **P5 (de más) sube de 64 a 112 y P6 de 30 a 49**, porque las
órdenes que antes se rechazaban ahora se colocan, se llenan y se reentra. **Las parejas suben de 12
a 18; la cobertura, de 12/198 (6,1 %) a 18/198 (9,1 %); la precisión BAJA de 12/94 (12,8 %) a
18/162 (11,1 %)** porque el bot abre 68 operaciones puntuables más y solo 6 emparejan. Como pide el
encargo, se dice y se explica por sesión, y no se ajusta nada:

- **Las 6 parejas nuevas** están en 2026-01-14 07-11, 2026-04-23 07-11, 2026-07-02 11-15,
  2026-07-13 07-11, 2026-08-24 11-15 y 2026-08-26 07-11: **las seis sesiones tenían antes un rechazo
  por `volumen_max_lotes`** (cuatro de ellas, 2026-01-14 07-11, 2026-04-23 07-11, 2026-07-02 11-15
  y 2026-08-26 07-11, están en la fila P4 de CORRIDA-CONSTRUCCION.md §4.5: «todas las órdenes
  rechazadas, o rechazos y reubicaciones sin llenado, con algún rechazo por volumen»). La orden que antes se rechazaba ahora se coloca con el lote limitado, se llena en el
  mismo minuto que la del trader (±3 puntos, ±15 min) y empareja. **Ninguna pareja se pierde.**
- Las 62 operaciones puntuables de más sin pareja son del mismo origen: órdenes que antes no vivían.
  Su clasificación es la de siempre (P5 y P6, y las que el trader no operó).

La medida no habilita nada (ADR-0070 §3) y no cambia ninguna decisión de ADR-0081.

### 4.e La corrida 3 (a35-inicio) y el determinismo

La otra lectura de A-35 con la cuenta diaria da, como en R3.1 y R1.2, **las mismas parejas, cobertura
y precisión que la corrida 2** (18/198, 9,1 %; 18/162, 11,1 %; antes 12/198 y 12/94) y los mismos
rechazos (`precio_invalido` 26: 6, 8, 4, 8; antes 11 + `volumen_max_lotes` 96); 179 llenadas (antes
106) y 289 canceladas (antes 214; la diaria, 299: `inicio_vela_contraria` recoloca distinto, como ya
decía CORRIDA-CONSTRUCCION.md §3.4). Ninguna orden no enviada; ningún rechazo por `margen_libre`.

**Determinismo:** la corrida 2 repetida con `--salida` fuera del repositorio (la misma lectura,
declarada en la fila de la fase 4): `sha256sum` idéntico (`e584077bf767818b97b3e787…`); `TIEMPO:
424.1 s; MEMORIA: pico del proceso de 634.5 MiB`. La copia no se commitea.


## 5 · Lo que va a la sesión 5

**A-57** (`knowledge/spec/ambiguedades.yaml`; fila en PROJECT_STATE): qué hace el trader cuando el
lote de su riesgo no cabe en el margen o en el volumen máximo de la cuenta. Clase `pregunta`, no
bloqueante, `resuelve_en: [F24]`; `lote_si_no_cabe` es DEFAULT_AMBIGUOUS bajo ella (`limitar`). La
pregunta se formula con la cuenta y sus límites (50 lotes, 1:30) y sin ninguna cifra ni argumento de
VIABILIDAD-COMISION.md. **Lo que encontró la búsqueda** (§1.f): ninguna frase del trader habla del
lote que no cabe; las dos citas (`ev-v4-002457-5a2e88c6`, `ev-v4-012900-8ef676ed`) dicen lo que hizo
con el lote en su prueba de fondeo, y la propia pregunta lo declara como respaldo débil. Sustituye
y amplía la pregunta 2 de la lista «Para el cuestionario de la sesión 5» de CORRIDA-CONSTRUCCION.md
§4.5 (que solo hablaba del máximo de 50 lotes). La respuesta entra como `RESOLVE_UNKNOWN` sobre
A-57 (ADR-0022); si el trader dice «no entro», `lote_si_no_cabe` pasa a `no_operar` por `feedback
apply`, y el camino ya existe y está probado.

## 6 · Líneas preparadas para el commit del contrato de la orden de cierre

Las prepara la rama; las ejecuta el ritual (RITUAL.md, punto 3) solo con la orden de cierre de
Aleks. Todas con la conformidad del consultor (respuesta a la PARADA, puntos 6 y 8).

1. **E sale de la Next Action a HISTORIA** como HECHA: «E. La rama del margen (heredado 37): …» →
   registro en el cierre de `docs/state/HISTORIA.md` (ADR-0081; `stable/F37s-margen-lote`).
2. **El heredado 37 sale** con el criterio (a) de `docs/state/README.md`, bajo `# Pendiente heredado
   SALE · sale de PROJECT_STATE.md en trabajo/margen-lote (<fecha>)`, con su texto literal (Archivo
   33 de HISTORIA, línea 79): «37. **LOS RECHAZOS POR VOLUMEN Y POR MARGEN, EN LA RAMA DE STOP Y LOTE
   (A-18).** FTMO confirma 50 lotes en EURUSD y cuenta de cobertura (P-D1,
   `docs/validation/FTMO-P-D1.md`, 2026-10-12). Pero antes que el volumen corta el MARGEN (ADR-0026,
   Impacto): con `firma_apalancamiento` 1:30, todo el saldo como margen da 27,27 lotes a 1,10 y 25,00
   a 1,20, y el 0,5 % deja de cumplirse con un stop de menos de 1,83 y 2,00 pips (el tope de 50 lotes
   corta en 1 pip). Partir en varias órdenes no lo arregla: MT5 suma el margen de las posiciones del
   mismo lado. El simulador no comprueba el margen y `firma_apalancamiento` no lo lee ningún código
   del bot (deuda abajo). La ejecución 2 de la demo comprueba la fórmula con el margen de 1,00 lote
   que ya escribe el script 1.1 (`MargenAlcanza`).» Evidencia: ADR-0081 (la decisión), el rechazo
   `margen_libre` y `limitar_lote` en `engine/broker.py` (commit 80b0795), `reglas_broker_de` leyendo
   `firma_apalancamiento`, y `tests/unit/test_margen_lote.py`. Lo que de él sigue vivo (la ejecución 2
   con `MargenAlcanza`) va en la línea de A (punto 6). En PROJECT_STATE queda también la línea corta
   «- 37. **LOS RECHAZOS POR VOLUMEN Y POR MARGEN (A-18).** Va a E; …» (:82): sale con él.
3. **Hoja de ruta** (`docs/plan/HOJA-DE-RUTA.md`), en el mismo commit, para que
   `tests/unit/test_hoja_de_ruta.py` siga en verde:
   - R3.3 pasa a HECHA: «- **Estado:** HECHA (`trabajo/margen-lote`, `stable/F37s-margen-lote`;
     MARGEN-LOTE.md): ADR-0081 (el bot limita el lote al menor de tres; el bróker simulado rechaza por
     `margen_libre` al colocar y al llenar), A-57 abierta para la sesión 5, y las dos medidas de E
     (§2.b y §2.c). La re-corrida en diagnóstico, §4.»; sus Refs `NA:E · HER:37 · ID:A-18` se quedan
     (una HECHA puede nombrar una letra HECHA en HISTORIA y un heredado que SALE en ese mismo commit:
     comprobar con el test antes de commitear; si el heredado 37 que sale deja de ser «vivo» y la
     entrada HECHA lo nombra, el test lo admite —«esta HECHA y el heredado sigue vivo» es el fallo
     contrario—).
   - A.2: quitar `HER:37` de sus Refs y, en «Qué es», «(hedging, volumen máximo, tope sumado; decide
     el heredado 37)» → «(hedging, volumen máximo, tope sumado; el heredado 37 quedó decidido en
     ADR-0081)»; «Hecho cuando: las respuestas están registradas y el heredado 37 decidido» → «…
     registradas» (el 37 ya está decidido).
   - G.3 pasa a HECHA y pierde `HER:27` de sus Refs (el 27 sigue vivo en A.2): «- **Estado:** HECHA
     (`trabajo/margen-lote`): la descripción de `firma_tamano_posicion_ratio_aviso` dice lo que
     respondió FTMO (respuesta 10).» Refs: `(sin heredado; HER:27 sigue en A.2)` o vacío.
   - R4.1: quitar `NA:E` de los Refs y «R3.3 (NA:E)» → «R3.3 (HECHA)» en «Depende de»; añadir
     `ID:A-57` a los Refs y, en «Qué es», «…; y A-57 (el lote que no cabe, MARGEN-LOTE.md §5)».
4. **PROJECT_STATE, Next Action**: F pasa de «E → O → V» a «O → V»; en V, «Depende de R1.1, de R3.1,
   de E y O, …» → «de O, …» y gana «A-57 (el lote que no cabe, MARGEN-LOTE.md §5)» entre lo que lleva
   a la sesión 5.
5. **Una línea para A**: «La ejecución 2 comprueba la fórmula del margen con `MargenAlcanza`
   (FTMO-P-D1.md §3), y la 3 mide cuándo comprueba MT5 el margen de una pendiente stop (ADR-0081 §4)».
6. **Otra línea para A, porque la medida de noticias quedó sin fuente**: «Aleks: calendario de las
   noticias restringidas de FTMO (FAQ «Can I trade news?») de los meses de construcción, en
   `corpus/noticias/` como CSV `fecha_utc,hora_utc,divisa,evento`; `stops_cortos.py --noticias <csv>
   --ventana-min 2` da la medida (MARGEN-LOTE.md §2.b)».
7. Nada más cambia en PROJECT_STATE salvo lo que haga el ritual (la fila de A-57 ya entró en la rama).

## 7 · Encargo frente a lo hecho, punto por punto

| Punto | Pide | Hecho | Dónde |
|---|---|---|---|
| 0 | Base, CI con `gh`, skill `abrir-rama`, tramo R3, informe y anexos, `/model` | Hecho (la fecha real es el 2026-10-17; el encargo va fechado el 18) | §0; el esfuerzo de `/model` no se puede leer desde la sesión |
| 1 | ADR; bróker que rechaza por margen; medidas 1 y 2 sobre el código de hoy; sustituir la base de E | Hecho | ADR-0081; §2.b, §2.c (96/11 frente a 100/11 de R3.1) |
| D1 | Limitar y operar; PROVISIONAL; la pregunta ampliada al margen | Hecho | ADR-0081 §1; A-57 |
| D2 | Menor de tres × 0,95, al paso; el mínimo: PARADA si la cita no sostiene «no se opera» | Hecho; la cita no lo sostenía → PARADA → «no se opera» por decisión (respuesta 0), ADR-0053 enmendado | ADR-0081 §2; `limitar_lote` |
| D3 | Fórmula; al llenar; al colocar si MT5 lo dice; recuadro ADR-0052 §4; equidad al bróker; línea para A | Hecho (al colocar y al llenar; «charged for each order») | §1.b; ADR-0081 §4; recuadro ADR-0052; §6.5 |
| D4 | Dos parámetros, su sitio, cómo lee la spec el tope | Hecho: `ejecucion`, patrón ADR-0068; la spec no lee el tope (ReglasBroker) | §1.f; §3.b |
| D5 | A-57, búsqueda en el corpus declarada, tabla de PROJECT_STATE | Hecho | §1.f; §5 |
| D6 | ADR-0081 con sus citas; perfil y parametros.yaml corregidos; G.3 | Hecho; más el recuadro en ADR-0026 (respuesta 7) | ADR-0081 §5; §3.b |
| D7 | Swing; noticias solo informan | Hecho; noticias sin fuente (línea para A) | ADR-0081 §7; §2.b |
| 3 | Nada más cambia | Hecho: `git diff main --name-only` en §8 | §8 |
| 4.a-g | Fase 0 y PARADA | Hecho | §1 |
| 5 fase 1 | Campo + test + sello; corrida «antes» con su fila; medidas 1 y 2 | Hecho (44f31fb, ddb51c6) | §2 |
| 5 fase 2 | Tests en rojo, recuento de FAILED | Hecho: 16 FAILED, 1 passed | §3.a |
| 5 fase 3 | Código, spec, ADR, recuadros, perfil, G.3, spec_version, manifest, docs, Fuente | Hecho (80b0795, `Fuente: ADR-0081`) | §3.b |
| 5 fase 4 | Re-corrida, tres comandos, fila antes; rechazos antes/después; limitadas y por qué; riesgo efectivo; T0 y P1-P7 | Hecho | §4 |
| 6 | El informe con sus secciones y las líneas del cierre | Hecho | §5, §6, §7 |
| 7 | Revisor con los dos ejes + sin curl ni guion en la CI | §9 | §9 |
| 8 | CI: hooks, rutas o sistema de archivos → `fix/`; si no, la lista | No toca hooks, rutas ni el sistema de archivos: lista en §8 | §8 |

**Desviaciones declaradas:**
- ADR-0081 entró en el commit de la fase 1 (44f31fb), antes del código, porque `knowledge validate`
  niega un id citado que no existe y el id va en la respuesta del consultor copiada tal cual (§2.a).
- Las fechas: el encargo va fechado el 2026-10-18 y el reloj de la máquina dio el 2026-10-17 en toda
  la rama; las filas de HOLDOUT-EXPOSICIONES y el informe llevan la real (h16).
- El contrato se amplió dos veces, declarado en el propio contrato: ADR-0026 (respuesta 7) y tres
  ficheros de tests (respuesta 2).
- Los tests sintéticos del bróker colocan desde el segundo 10, no el 0, porque al colocar hace falta
  un precio con el que convertir el margen (§3.a).
- La medida de noticias quedó sin fuente (`corpus/noticias/` no existe): línea para A (§6.6).
- «Agosto sale del xlsx que el trader ya no da por bueno» (encargo, 4.c) se escribe en el informe
  como lo sostiene ADR-0073: el trader da por bueno el backtest en vídeo; que el xlsx sea el otro es
  lectura de la sesión (h1).

## 8 · CI de Linux

La rama **no toca hooks, rutas ni el sistema de archivos** (ni `.claude/`, ni `scripts/`, ni el
`Makefile`, ni `.github/`): no hace falta el push como `fix/margen-lote`. Lo que cambia frente a
`main` (`git diff main --name-only`, más los anexos de la fase 4):

- Estado y contrato: `PROJECT_STATE.md`, `contrato.yaml`, `docs/state/HISTORIA.md`,
  `docs/encargos/trabajo-margen-lote.md`.
- ADR: `docs/adr/0081-el-lote-que-no-cabe-se-limita-y-el-broker-rechaza-por-margen.md` (nuevo),
  `0026-…` (recuadro), `0052-…` (recuadro), `0053-…` (recuadro), `docs/adr/README.md`.
- Spec y knowledge: `knowledge/spec/parametros.yaml`, `strategy_spec.yaml`, `ambiguedades.yaml`,
  `spec_manifest.yaml`; `docs/spec/` (los cuatro generados); `knowledge/cuentas/ftmo-2step-swing-100k.yaml`.
- Código: `src/botsito/engine/broker.py`, `cableado.py`, `primitivas_broker.py`, `simulacion.py`.
- Tests: `tests/unit/test_margen_lote.py` (nuevo), `test_cableado.py`, `test_vida_de_la_orden.py`,
  `test_racha_perdidas.py`, `tests/regression/test_cuenta_7_de_agosto.py`.
- Informe y anexos: `docs/validation/MARGEN-LOTE.md`, `HOLDOUT-EXPOSICIONES.md`,
  `docs/validation/anexos/MARGEN-LOTE/` (README, `antes-diaria…`, `arrastrada…`, `diaria…`,
  `a35-inicio…`, `medida_2.py/.txt`, `stops_cortos.py/.txt`, `fase4_medidas.py/.txt`, `patrones.txt`).

Toda consulta de la CI de esta rama se hizo con `gh run view` (§0); ninguna con `curl` ni con un
guion.

## Estado

EN CURSO · fases 1 a 4 hechas (2026-10-17/18); falta el revisor (§9) y la entrega.
