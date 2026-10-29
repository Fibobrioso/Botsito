# RESPALDO-M1 · el respaldo M1 no evalúa contra precios anteriores a la decisión (Z, R3.5)

Rama `trabajo/respaldo-m1`, abierta el 2026-10-28 desde `main` 0e021bf (commit de estado sobre el
merge 89dc902, tag `stable/F38i-barrido-sesion-6`). Encargo: `docs/encargos/trabajo-respaldo-m1.md`.
Tramo R3 de `docs/plan/HOJA-DE-RUTA.md`.

## Apertura: la base, comprobada con git

| Comprobación | Salida |
|---|---|
| `git rev-parse main origin/main main^1` | 0e021bf9ca1b108089feda6e6d9f455bcda441be (dos veces) y 89dc9028a912991e47d3ce54cdd3915d2b932606 |
| `git rev-parse "stable/F38i-barrido-sesion-6^{commit}"` | 89dc9028a912991e47d3ce54cdd3915d2b932606 = `main^1`; en origin (`git ls-remote --tags origin stable/F38i-barrido-sesion-6`: e553e2a5…, el objeto del tag anotado) |
| último `- Tag: ` de HISTORIA | `stable/F38i-barrido-sesion-6` |
| `gh run view 40815230287 --json status,conclusion,headSha,headBranch,event` | `{"conclusion":"success","event":"push","headBranch":"main","headSha":"0e021bf9ca1b108089feda6e6d9f455bcda441be","status":"completed"}` |
| `git branch --list` / `git ls-remote --heads origin` | solo `main` (y ningún `fix/*` en origin) |

Tag previsto del cierre: `stable/F38j-respaldo-m1` (el último es F38i). Commit de apertura: 4036818
(`make check` exit 0, ningún `failed`, `SELLO` sobre el árbol 5ebeb8d4…; 1117 s; `PICO DE MEMORIA de
make check: 300 MiB en test`).

## 0. Fase 0 · inventario sin tocar nada (2026-10-28/29)

Ni una línea de `src/`, tests, spec ni knowledge. Lo medido sale de: lecturas del código; cuatro
guiones de la carpeta de trabajo de la sesión, fuera del repositorio, con la raíz por argumento
(`sonda_z.py`, velas y ticks SINTÉTICOS de 2030 sobre el código de la rama, que en `src/` es el de
`main`; `censo_z.py`, que solo lee una salida commiteada; `tres_no.py` y `be_vela.py`, que leen el
mercado de días dev por la compuerta `simulacion.mercado_de_construccion`; `recuentos.py`, la
compuerta). Ninguno escribe nada; ninguno imprime nada anterior a las 00:00Z del día dev (solo horas
del día desde las 04:58Z). Exposiciones: §0.k.

### 0.a Cada lectura del respaldo M1 y cada precio sin tick

Lista completa: Grep de `\.m1\(|cotizacion\(|RESPALDO_M1|_precio_de_mercado|precio_de_conversion|primer_llenado_|primera_salida\(|ticks_del_minuto`
en `src/`. Las lecturas de una vela M1 del mercado son siete; nada más en `src/` las hace
(`cableado.py:63,109,764` solo importan la constante para contar fuentes). `simulacion.py:79` es
`MercadoDia.mercado()`, el constructor común del `Mercado`, y no lee ninguna vela. **La repetición del
trader** no está ahí (auditor, 19): es `scripts/repeticion_trader.py:128` (`Mercado((), md.m1)`, sin
ticks) con `Broker.abrir_conocida` (`broker.py:614-645`), que abre la posición **a media vela**, en
el instante del trader; lo que cambie en `primera_salida` la cambia (§0.f, PARADA punto 9).

| # | Lectura | Sirve a | ¿Vela con precios ANTERIORES a lo que evalúa? (Z) | ¿Precios POSTERIORES al instante que cotiza? |
|---|---|---|---|---|
| 1 | `primer_llenado_limite`, `llenado.py:159-166` | llenar una límite | **SÍ**: acepta toda vela con `_fin_ms(vela) > desde_ms` (`:160`); la orden colocada en el cierre de la M1 *k* menos 1 ms tiene `desde = max(ahora-1, ultimo_cambio_ms)` = *k*fin − 1 (`broker.py:749`), y la vela *k* (fin = *k*fin) entra entera. Sonda 1: límite de compra en 1000 colocada en el cierre de M0, M0 baja a 990 y M0+1 no baja de 1004 → `llenada … respaldo_m1` al fin de M0 | no (el evento se sella en el fin de la vela) |
| 2 | `primer_llenado_stop`, `llenado.py:208-222` | llenar una orden stop | **SÍ**, la misma condición (`:209`). Sonda 2: venta stop en 995 colocada en el cierre de M0 → `llenada` al fin de M0 | no |
| 3 | `primera_salida`, `llenado.py:287-309` | stop u objetivo de una posición | **SÍ para el stop movido**: `desde = max(ahora-1, abierta_ms, stop_movido_ms)` (`broker.py:763`); el stop movido en el cierre de *k* menos 1 ms se evalúa contra la vela *k* entera. Sonda 3: larga en 1000 con stop 990, la M0 baja a 985 y en su cierre el stop pasa a 1000 → sale `stop 1000` al fin de M0. **No** para la posición recién llenada por el respaldo: `abierta_ms` = fin de la vela del llenado y esa vela queda fuera (`_fin_ms <= desde`): ADR-0057 §1 | no |
| 4 | `Mercado.cotizacion`, `llenado.py:93-113` | `_precio_infringido` (`broker.py:537`: `precio_invalido` y `stops_level`) al colocar y al modificar | no evalúa un evento: da la cotización; sin ticks, la última M1 con fin ≤ instante, es decir la *k*−1 en el cierre de *k* menos 1 ms (§0.b) | no (`_fin_ms(vela) <= instante_ms`, `:110`) |
| 5 | `Broker._precio_de_mercado`, `broker.py:933-945` | `cerrar_a_mercado` (`:607`), el fin de la ventana (`cableado.py:350-353`) | no evalúa un evento contra un rango | **sí, por construcción**: sin ticks en el minuto, el cierre de la vela de ESE minuto (`:941-945`), que cierra 1 ms después del instante del motor (*k*fin − 1). Y con ticks en el minuto pero ninguno ≤ instante, cae a la misma vela (sonda 6: tick a los :30, instante a los :10 → precio 1020 = cierre de la vela). En el motor no ocurre: decide siempre en *k*fin − 1 y todo tick del minuto *k* es ≤ ese instante |
| 6 | `Broker.precio_de_conversion`, `broker.py:947-964` | margen al colocar (`:511`) y de las primitivas (`primitivas_broker.py:542`, `:585`) | igual que 5 | igual que 5 (sonda 6: 1023 = cierre + spread) |
| 7 | `Broker._peor_del_minuto`, `broker.py:898-913` | `_marcar_hasta` (`:882-896`): las marcas de la posición, que van a la operación (`_operacion`, `:1072`) y a `cuenta.marcar` (`cableado.py:447-450`), la peor equity que leen los topes | no evalúa un evento | **sí, hasta un minuto**: acepta la vela si `fin·60000 ≤ hasta + 60000` (`:910`), es decir toda vela que EMPIEZA en o antes de `hasta`. Cuando un evento del respaldo se sella en el fin de *k* (`_aplicar` → `_marcar_hasta(k fin)`, `:797`), la vela *k*+1 entra entera, marcada en el instante *k* fin. Sonda 5: larga que salta por stop al fin de M0; sus marcas son `(fin de M0 − 1 ms, 989)` y **`(fin de M0, 900)`**, la mínima de M0+1, y la posición cerró en el fin de M0: la marca de un minuto futuro queda dentro de la operación (`p.abierta_ms <= ms <= p.cerrada_ms`, `:1072`) |

Además `mover_stop` (`broker.py:665-669`) no lee ninguna vela: solo mira si el minuto tiene ticks
para la fuente del evento `stop_movido`.

**La diferencia en una misma colocación a cierre menos 1 ms** (sonda 4, sin ticks, M0−1 cierra en
1000 y M0 en 1010, spread 3): `cotizacion` → `(1000, 1003)`, la M1 *anterior*; `precio_de_conversion`
(compra) → 1013, el cierre de la M1 *de la colocación* más el spread; `_precio_de_mercado` (compra)
→ 1010. En la misma colocación el rechazo por precio se juzga con la vela *k*−1 y el margen con la
*k*.

Los dos casos de futuro del encargo, **verificados** (filas 5-7) y llevados a la PARADA sin arreglar
(punto 2): `_peor_del_minuto` mira hasta un minuto adelante cuando el instante es el fin de un
minuto (en el motor, en cada evento del respaldo); `_precio_de_mercado` y `precio_de_conversion`
toman el cierre de la vela del minuto, 1 ms posterior al instante del motor, y en un minuto con
ticks sin ninguno anterior, la vela entera (no ocurre en el motor).

### 0.b La deuda de COTIZAR

La línea que salió de Technical Debt en `trabajo/recorrida-construccion` (RECORRIDA-CONSTRUCCION.md
§6, `:1526-1528`; la última copia en `docs/state/HISTORIA.md:13286`): «El bróker simulado cotiza con
el respaldo M1 la orden del primer cierre de la ventana: los ticks empiezan en ventana_inicio y la
orden lleva 1 ms antes (VISOR-CONSTRUCCION.md §4.3).» Su evidencia, VISOR-CONSTRUCCION.md §4.3 punto
6 (`:1155-1162`): `Mercado.cotizacion` no encuentra ningún tick hasta el instante y usa la última M1
cerrada más el spread supuesto.

**No es la condición de Z.** Z es un EVENTO del modelo de llenado evaluado contra precios anteriores
al instante en que se decidió lo evaluado (filas 1-3). `cotizacion` no evalúa nada sobre un rango: da
la cotización vigente, y toda cotización es por definición la última anterior o igual al instante
(ADR-0057 §4, «la última M1 CERRADA»). El defecto de cotizar es otro: **en un minuto sin ticks va una
vela por detrás de lo que el motor ya vio** (el motor decide en el cierre de *k* con la vela *k*; la
cotización usa *k*−1), y no coincide con `precio_de_conversion` en la misma colocación (§0.a, sonda
4). Arreglarlo cambia decisiones de `precio_invalido` y obliga a elegir entre la vela *k* (1 ms de
futuro, la convención del motor) y la *k*−1 (lo que dice ADR-0057 §4): es una decisión sobre
ADR-0057 §4, fuera de lo que esta rama puede cambiar. PARADA, punto 3.

### 0.c El instante de la decisión y qué vela llenó los tres «NO»

- **Se decide y se coloca en el cierre de la M1 menos 1 ms**: `cableado.py:297`
  `hasta_ms = instante * MS_POR_MINUTO - 1`, `broker.avanzar(hasta_ms)` (`:299`) y
  `ctx.instante_ms = hasta_ms` (`:313`), con el que colocan, modifican, cancelan, cierran y mueven
  las primitivas (`primitivas_broker.py:645`, `:670`, `:762`, `:775`). `instante` es el minuto
  siguiente a la vela que cierra, así que la vela *k* cierra en `instante·60000` y el motor decide en
  ese instante menos 1 ms. `avanzar(hasta_ms)` NO evalúa todavía la vela *k* (`_fin_ms(vela) >
  hasta_ms`, `llenado.py:160`): la evalúa el `avanzar` del minuto siguiente, para todo lo que haya
  entonces, también lo que se decidió en su cierre.
- **`ultimo_cambio_ms`**: al colocar, el instante de colocar (`broker.py:522-523`, décimo argumento
  posicional; en un rechazo, `:517-519`); al modificar, `:585`; al cancelar, `:596`; al expirar,
  `:805`; al rechazar al llenar, `:831`; al llenar, `:837`; al cancelar por cierre, `:863`. Para un
  llenado solo cuenta el de colocar o modificar: los demás dejan la orden fuera de `COLOCADA,
  MODIFICADA` (`:738`).

Los tres casos, con «### Ordenes» de las salidas commiteadas (`anexos/RECORRIDA-CONSTRUCCION/`) y el
mercado del día dev por la compuerta (`tres_no.py`; precios en puntos BID):

| Caso | Colocada | La vela que la llenó | ¿Ticks en ese minuto? | Lo que habría pasado sin esa vela |
|---|---|---|---|---|
| 2026-04-07 07-11 o1, venta stop en 115378 (corrida 2) | 04:59:59.999Z | la M1 de 04:59 (mínima 115377 ≤ nivel): `llenada` 05:00:00.000Z, `respaldo_m1` | no: los ticks de abril son 05-13 UTC (RECORRIDA §0.b); es el borde de la cobertura | el minuto 05:00 tiene 79 ticks y el primero con BID ≤ nivel es **05:00:33.503Z** (BID 115378): se llenaría por ticks, a ese tick |
| 2026-04-23 07-11 o3, venta stop en 117003 (corrida 2) | 05:04:59.999Z | la M1 de 05:04 (mínima 117001, abre en 117003): `llenada` 05:05:00.000Z | no: hora perdida 05Z | 05:05, 05:06 y 05:07, sin ticks, no bajan del nivel (mínimas 117004, 117005, 117012): **no se llena en esos tres minutos** |
| 2026-01-05 11-15 o20, venta stop en 116853 (corridas 1 y 2) | 10:23:59.999Z | la M1 de 10:23 (mínima 116851): `llenada` 10:24:00.000Z | no: hora perdida 10Z | la M1 de 10:24, sin ticks, baja a 116844: **se llenaría con el respaldo a las 10:25:00.000Z**, una vela más tarde |

Entró porque la orden se colocó en el último milisegundo de la vela *k* y el respaldo acepta toda
vela cuyo fin es posterior a `desde`, que es ese milisegundo: la vela *k* entera, con sus precios del
minuto que la orden aún no existía.

### 0.d La vela del llenado frente a la salida (ADR-0051 §3 frente a ADR-0057 §1)

ADR-0051 §3: «dentro de una M1 que cubre la límite de entrada y luego el stop, se toma que la entrada
se llenó y el stop saltó en la misma vela». ADR-0057 §1 (ACTIVE): «para la vela del llenado, la misma
[convención] que la límite (la salida se mira desde la vela siguiente)». **El código hace lo de
ADR-0057 §1**: el llenado del respaldo pone `abierta_ms` en el fin de la vela (`llenado.py:166`,
`:218`; `broker.py:840-843`) y la salida se busca con `desde ≥ abierta_ms`, que deja fuera esa vela
(`_fin_ms(vela) <= desde_ms`, `llenado.py:288`). Lo fijan `test_broker_ordenes_stop.py:160-176`
(`test_misma_vela_la_stop_sigue_la_convencion_de_la_limite`, `:161-188`, «la salida no se mira en la
vela del llenado», para la límite y la stop; el `:145-159` del encargo es el del hueco a la
apertura) y `test_broker.py:222-236`
(la límite se llena al fin de M0+1 y el stop salta en la M0+2). ADR-0051 no lleva NOTA que lo diga.
Propuesta: la NOTA de esta rama en ADR-0051 recoge también §3, remitiendo a ADR-0057 §1 sin cambiar
lo que decide (PARADA, punto 4).

### 0.e Los eventos del respaldo que no son llenadas

`censo_z.py` sobre las dos salidas commiteadas (solo lee; tipos, instantes e ids):

| Corrida | eventos del respaldo | llenadas | … con la vela que colocó la orden | stops | … con la vela en cuyo cierre se movió el stop | `stop_movido` | objetivos | peticiones `modificar` / eventos `stop_movido` |
|---|---|---|---|---|---|---|---|---|
| 1 (`cuenta-arrastrada.txt`) | 8 | 4 | 2 (2026-01-05 o20, 2026-01-06 o1) | 3 | **0** | 1 | 0 | 21 / 21 |
| 2 (`diaria…txt`) | 34 | 16 | 10 | 14 | **2** (2026-04-06 pos-o12 a las 10:07:00.000Z, movido a las 10:06:59.999Z; 2026-04-07 pos-o29 a las 10:33:00.000Z, movido a las 10:32:59.999Z) | 4 | 0 | 118 / 118 |

- **Modificaciones de orden: ninguna.** Todas las peticiones `modificar` son stops movidos (mismo
  número). Es la spec vigente: con `orden_limite_nace = al_aparecer_punto_de_breaker`
  (`parametros.yaml`, CONFIRMED), `reubicar_orden_limite` cancela y vuelve a colocar
  (`primitivas_broker.py:755-760`); `modificar` (`:762`) no se alcanza.
- **Los `stop_movido` del respaldo** (1 y 4) no se evalúan contra nada: son decisiones del motor al
  cierre de la M1 (ADR-0065 §5).
- **Los 2 stops de la corrida 2**: el stop nuevo (a break even) saltó contra la vela en cuyo cierre se
  movió. `be_vela.py`: en las dos, esa vela llega a la entrada (mínima 115509 = entrada; mínima
  115550 < 115553) y **no** al stop original (115496; 115475); la vela siguiente no llega a la
  entrada. Con la condición de Z ninguna de las dos posiciones saldría en esa vela.
- **ADR-0065 §4** dice que con el respaldo «una M1 que pasa el nivel y toca el stop original»:
  «manda lo de siempre (ADR-0051 §3): el stop primero, pesimista, y no hay break even». Hoy el código
  no lo cumple (sonda 3: sale a 1000, el break even, aunque la vela tocó 990), y la forma «inicio ≥
  instante» tampoco: con ella esa vela no se evalúa con ningún stop. En las cuatro velas de los
  stops movidos del respaldo de las dos corridas, ninguna toca el stop original (`be_vela.py`), así
  que en estas corridas no hay ningún caso; el código, sí. PARADA, punto 1.

### 0.f La forma de la corrección

**Propuesta (b)**: las tres funciones del respaldo reciben el instante de la DECISIÓN de lo que
evalúan (`decidido_ms`) y una vela solo cuenta si **empieza en o después** de él; el instante sale
del objeto y no del `desde` de `_proximo_evento`:

```python
# llenado.py, en primer_llenado_limite / primer_llenado_stop / primera_salida
if vela is None or _fin_ms(vela) <= desde_ms or _fin_ms(vela) > hasta_ms:
    continue
if int(vela.inicio) * MS_POR_MINUTO < decidido_ms:   # nuevo: la vela de la decisión no cuenta
    continue
```

con `decidido_ms` por defecto igual a `desde_ms` (lo más estricto: niega por defecto, y los tests de
`test_llenado.py`, que pasan `desde` en el inicio exacto de una vela, no cambian), y desde
`broker.py:749` y `:763` el del objeto: `o.ultimo_cambio_ms` para una orden, `p.abierta_ms` para la
salida con el stop de nacimiento. Y, para que el stop movido cumpla ADR-0065 §4 sin mirar atrás, la
vela que contiene `stop_movido_ms` (empieza antes, termina después) se evalúa con el **stop
anterior** (`Posicion` guarda el que tenía; el objetivo no cambia), y las siguientes con el nuevo.

**Por qué es la condición y no el caso**: no se mira de dónde viene la orden (borde de la ventana,
hora perdida) ni su tipo; se exige en toda vela del respaldo que lo evaluado estuviera decidido antes
de que la vela empezara, que es lo que los ticks ya cumplen (`t.instante <= desde_ms → continue`). El
`desde` sigue mandando como hoy para no repetir lo ya procesado, sin tocar el `ahora - 1`.

**(a), la lectura del consultor tal cual**, sin el stop anterior: lo mismo con `decidido_ms =
max(p.abierta_ms, p.stop_movido_ms or 0)` para la posición. Más simple, pero la vela del stop movido
no se evalúa con ningún stop (contra ADR-0065 §4 en el caso que este describe; en estas corridas,
ninguno, §0.e).

Lo que sigue igual, y por qué (se prueba en la fase 1):
- **pendiente desde antes de una vela sin ticks**: su `ultimo_cambio_ms` es anterior al inicio de esa
  vela → la vela cuenta;
- **el tick del último evento llena otra pendiente («ahora − 1»)**: los ticks no pasan por
  `decidido_ms`; `desde` no cambia;
- **la salida tras un llenado del respaldo desde la vela siguiente** (ADR-0057 §1): `abierta_ms` es
  el fin de la vela del llenado = inicio de la siguiente → la siguiente cuenta (`>=`), la del llenado
  ya estaba fuera;
- **los tests de `main` que colocan en el inicio exacto de una vela**, sin tocarlos:
  `test_broker.py:222-236` (coloca en `_ms(M0)`, inicio de M0: M0 cuenta), `test_broker_ordenes_stop.py:145-176`
  (colocan en `_ms(M0 + 1)`, inicio de M0+1: cuenta; la salida, desde M0+2) y los del respaldo de
  `test_llenado.py:94-166` (llaman a las funciones sin `decidido_ms`, con `desde` en el inicio de una
  vela: cuenta).

Lo que NO se puede excluir: la vela que empieza JUSTO en el instante de la decisión (forma descartada
por el auditor del consultor): con `>=` cuenta.

**Medido con un prototipo de (a)** en un clon desechable (`git worktree add --detach C:/cm/z-proto`,
ya quitado; el parche, un guion de la carpeta de trabajo con la raíz del clon por argumento que se
niega a correr en el repositorio; `config/settings.local.toml` del clon con la ruta absoluta de
`data/`): `uv run pytest tests/unit/test_llenado.py tests/unit/test_broker.py
tests/unit/test_broker_ordenes_stop.py tests/unit/test_be_al_tick.py tests/unit/test_instante_llenado.py
tests/unit/test_caja_hasta_el_llenado.py tests/unit/test_simulacion.py tests/unit/test_cableado.py
tests/regression/test_cuenta_7_de_agosto.py -q` → **todos pasan sin tocarlos**, también los que el
auditor añade a la lista de f) (H3: `test_be_al_tick.py:91`, que abre a media vela, `:137`,
`test_cableado.py:684`, `test_simulacion.py:249`) y la regresión del 7 de agosto con los datos de
agosto (dev). La suite entera en el clon no la dejó correr la guardia (§0.m); la corre el `make check`
de la fase 1. La forma (b) no la he prototipado: lo que digo de ella es lectura.

**Lo que la condición cambia y el encargo no nombraba (auditor, H2):** una posición abierta A MEDIA
VELA con `abrir_conocida` (la repetición del trader, `test_be_al_tick.py`, la regresión de agosto)
deja de evaluarse contra la vela de su apertura en el respaldo, porque esa vela empieza antes de
`abierta_ms`. Es la condición tal cual (la vela lleva precios anteriores a la apertura), y negar por
defecto lo pide; pero cambia la repetición de ADR-0051 §8 sin ticks. Con ticks no cambia nada.
PARADA, punto 9.

### 0.g Los guiones de la fase 2

Medido en `anexos/RECORRIDA-CONSTRUCCION/`: `costes_y_sesiones.py:28-31` fija `AQUI`/`RAIZ` y mete
su carpeta en `sys.path`, importa `horas_perdidas` (`:33`) y lee `entradas-antes-alternancia.txt`
(`:44`, `:146-175`, `:455`) para las partes a y b; la parte c (`:416-436`) solo marca la llenada con
`colocada_ms == e.ms - 1`. `patrones.py:53-54` importa `horas_perdidas` de su carpeta y recibe la
salida por argumento (`:217`). `lista_s14.py:16-18` recibe la carpeta e importa `patrones` de ella;
lee `entradas-antes-alternancia.txt` (`:24`, `:91-97`) para el sesgo, el camino y **el R de cada
llenada**, que imprime (`:132-151`).

Propuesta (PARADA, punto 5): **no se vuelve a correr `entradas_antes_alternancia.py`**. En
`anexos/RESPALDO-M1/` van:
- `patrones.py` y `horas_perdidas.py`, copias IDÉNTICAS (el primero ya recibe la salida por
  argumento);
- `censo_respaldo.py`, nuevo, con las salidas por argumento y sin `entradas-antes-alternancia.txt`:
  la parte c ampliada, como `censo_z.py` de esta fase: llenada con `colocada == ms − 1`; stop u
  objetivo con un `stop_movido` de la misma posición en `ms − 1`; modificaciones, por la igualdad
  peticiones `modificar` = eventos `stop_movido` (si difiere, sale con error: habría modificaciones
  de orden que la salida no fecha); y la clasificación borde de la ventana / hora perdida de
  `costes_y_sesiones.clasificar_respaldo`, con `horas_perdidas.py` al lado;
- `sesiones_s14.py`, nuevo, para las 8 sesiones de S-14: P6 por `patrones.py` y la primera orden
  de «### Ordenes» (colocada, precio y el lado, que se deduce de la caja 1 respecto al precio: en una
  venta queda por encima y en una compra por debajo, medido en 2026-04-07 o1 y 2026-04-06 o12), en la
  diaria de RECORRIDA y en la nueva; **sin ninguna columna de R**.

Las partes a y b de `costes_y_sesiones.py` (R y sesiones cargadas) no se repiten: no las pide el
criterio de hecho y necesitan la lista.

### 0.h La línea base vigente

La nombran hoy: la NOTA del 2026-10-27 de ADR-0070 §3 (`0070-…md:90-100`, «la línea base vigente
desde esa rama»); `ACTIVAR-A35-A44.md` §5, la NOTA de `:206-219` («Desde esa rama la línea base
vigente es `docs/validation/anexos/RECORRIDA-CONSTRUCCION/cuenta-arrastrada.txt`»); y el README de
`anexos/RECORRIDA-CONSTRUCCION/` (`:18-20`, «Es la línea base vigente desde esta rama …; no se edita»).
Propuesta (PARADA, punto 6): la corrida 1 de esta rama (`anexos/RESPALDO-M1/cuenta-arrastrada.txt`)
pasa a ser la vigente por una NOTA nueva en ADR-0070 §3 y otra en ACTIVAR-A35-A44.md §5, que la
nombran y remiten a la anterior; el README y las salidas de RECORRIDA no se tocan; el
README de `anexos/RESPALDO-M1/` lo dice. El `diff` contra la anterior, a fichero en
`anexos/RESPALDO-M1/diff-linea-base.txt`.

### 0.i Recuentos de partida por la compuerta

`recuentos.py .` (la raíz por argumento; ninguna clave):
- `casos_reservados`: 34 (2026-05: 13; 2026-06: 11; 2026-09: 10); `casos_ocultos`: 34, el mismo
  reparto. Ninguno en los cuatro meses de construcción.
- Construcción (`criterio.construccion`): 2026-04, 2026-07, 2026-08, 2026-01; días dev 21, 13, 21 y
  21 = **76**; operaciones del trader 35, 67, 42 y 54 = 198 (RECORRIDA §0.d y la NOTA de ADR-0070:
  76 y 198).
- Manifiestos de ticks (`ls data/manifests/ticks/`): `eurusd-ticks-2026-01-1ce59681`,
  `-04-1d189bdd`, `-07-6e7dc7cd`, `-08-75bd3a08`, los cuatro de RECORRIDA §0.b; el último commit que
  los tocó es 490c820 (enero).
- Tiempo esperado: corridas de 299,0 a 342,6 s y de 629,1 a 638,3 MiB (RECORRIDA §2, `:612-720`);
  `make check` de 1022 a 1170 s (BARRIDO-SESION-6, `:486-489`); el de la apertura de esta rama,
  1117 s y 300 MiB.

### 0.j Herencias

- **Next Action**: Z (la rama) y F, que termina en «R6a y Z en los huecos.» (`PROJECT_STATE.md:32`);
  ninguna otra letra nombra el respaldo, ADR-0051 ni ADR-0057 §1.
- **Pendientes heredados** (`PROJECT_STATE.md:60-71`): ninguno los nombra.
- **Technical Debt**: la línea de cotizar salió en recorrida-construccion (§0.b); su texto vive en
  HISTORIA. La de `engine/simulador_config.py` (`PROJECT_STATE.md:119`, el spread supuesto por la
  hora de pared) **no entra**: solo importa en los días de desfase (marzo del 9 al 27 y octubre,
  dice la propia línea; ENTRADA-ENERO.md §0.c), y la construcción es enero, abril, julio y agosto
  (`criterio.construccion`, §0.i).
- **Hoja de ruta**: R3.5 (la rama) y R5.2, que depende de «NA:Z, el respaldo M1 corregido (R3.5)»
  (`HOJA-DE-RUTA.md:291`).
- **Informes de octubre**: CORRIDA-CONSTRUCCION §3.6 (`:765-770`, los llenados de segundo `:00` en
  horas sin ticks) y VISOR-CONSTRUCCION §4.3 punto 6 (cotizar) son los antecedentes que Z ya
  recoge; ENTRADA-JULIO, ENTRADA-ENERO, MARGEN-LOTE y UMBRAL-MAYO nombran el respaldo sin un
  pendiente. HISTORIA, al final: nada que no esté ya en Z.
- **Entra, además, por el inventario**: ADR-0065 §4 (§0.e) y los dos casos de futuro (§0.a), a la
  PARADA.

### 0.k Exposiciones

**La de esta fase** (fila del 2026-10-29 en HOLDOUT-EXPOSICIONES, en el commit de la fase 0):
las salidas commiteadas `anexos/RECORRIDA-CONSTRUCCION/cuenta-arrastrada.txt` y
`diaria.DIAGNOSTICO.cuenta=diaria.txt` (días dev) y `entradas-antes-alternancia.txt`, por Grep y por
`censo_z.py`; el mercado (ticks y M1) de cinco días dev de construcción (2026-01-05, 2026-04-06,
2026-04-07, 2026-04-23 y 2026-08-20) por la compuerta, solo minutos desde las 04:58Z de su día;
`casos_reservados` y `casos_ocultos`, solo recuentos por mes; `arnes.dias_de_construccion`, solo
recuentos. Ningún libro, ninguna imagen, ningún fotograma, ninguna transcripción, nada de un mes
reservado. Y el `make check` de la apertura (lee el M1 de marzo, como en `main`: la lectura fija de
`test_visor.py` y `test_preparar_a35.py`). Los tests del prototipo en el clon (§0.f): sintéticos
salvo `test_cuenta_7_de_agosto.py` y `test_simulacion.py`, que leyeron las M1 y los ticks de
agosto de 2026 (dev) desde `data/` por la ruta absoluta del `settings.local.toml` del clon (el
precedente de que un test en un clon sí lee `data/` es el a1 de `trabajo/activar-sesion-05`,
`ERRORES-RECURRENTES.md:99`, no el de recorrida-construccion: auditor, 45). El auditor del encargo:
documentos, ADR, código y tests, de las salidas commiteadas solo listados y de `data/manifests`
solo recuentos; ninguna fecha reservada impresa.

**La propuesta para las fases 1 y 2** (PARADA, punto 7), una fila antes de correr nada:
(1) cada `make check` de la rama, que lee el M1 entero de marzo (`test_visor.py`,
`test_preparar_a35.py`); (2) las pruebas de `comparar-con-main` en clones desechables (`git worktree
add --detach`): los tests nuevos son sintéticos, pero los del lado de `main` que lean `data/` (la
regresión de agosto, `test_simulacion.py`) leen las M1 y los ticks de construcción por la ruta
absoluta del clon (precedente: a1 de `trabajo/activar-sesion-05`);
(3) las corridas 1, 2 y la repetición de la 1: los 76 días dev y, para calentar
(`arnes.dias_de_mercado`), el M1 entero de marzo (para abril), de junio (para julio) y de julio
(para agosto; los días 18 a 31 de julio no están en ninguna partición ni son construcción); enero
se calienta desde su propio mes, porque no hay manifiesto M1 de 2025-12 (`git ls-files
data/manifests`: de 2026-01 a 2026-09) y `arnes.dias_de_mercado` lo salta (`arnes.py:201-205`,
«sin el mes anterior, el calentamiento empieza en el mes»), lo mismo que RECORRIDA §0.c;
(4) los guiones de `anexos/RESPALDO-M1/` sobre las salidas nuevas y las de RECORRIDA. Ninguna
etiqueta ni cifra del bot de un día reservado.

### 0.l El encargo frente al repo (auditor)

El subagente `auditor-encargo` (2026-10-29, sobre 4036818): 50 afirmaciones, 39 correctas, **1
incorrecta** y 10 con matiz; 8 herencias. Lo que cambia lo que se hace, con lo medido después:

| # | Afirmación del encargo | Veredicto | Lo medido, y dónde se recoge |
|---|---|---|---|
| 45 | «precedente: la fila a1 de recorrida-construccion en ERRORES-RECURRENTES» | **INCORRECTA** | En la fila de recorrida-construccion (`ERRORES-RECURRENTES.md:101`) a1 es el recuento de R de las 77 llenadas de P6; el precedente de los tests del clon que sí leen `data/` es el a1 de `trabajo/activar-sesion-05` (`:99`). La fila propuesta (§0.k) lo dice así |
| 4 | ACTIVAR-A35-A44.md «solo si la PARADA decide» | MATIZ | No está en `rutas_permitidas`: si se decide (punto 6), el contrato se amplía en un commit a la vista |
| 19 | «simulacion.py (:79, la repetición del trader)» | MATIZ | §0.a: la repetición es `scripts/repeticion_trader.py` con `abrir_conocida` |
| 22 | caída a la vela en un minuto con ticks sin ninguno anterior | MATIZ | Verificado (sonda 6) y no alcanzable desde el motor (§0.a, fila 5) |
| 24, H1 | la deuda de cotizar | MATIZ | La regla es de ADR-0057 §4, fuera del contrato y de «QUÉ NO CAMBIA» (§0.b, punto 3) |
| 26 | `ultimo_cambio_ms` «al modificar (:585, :805, :831, :837, :863)» | MATIZ | Solo `:585` modifica una orden viva; los otros son estados terminales, y falta `:596` (cancelar) (§0.c) |
| 29, 33, H3 | los tests de f) | MATIZ | Líneas corregidas en §0.d y §0.f, y los tests de H3 medidos con el prototipo (§0.f) |
| 37, H5 | volver a correr `entradas_antes_alternancia.py` | MATIZ | Autorizado «una sola vez» (README de RECORRIDA, `:61`) y su raíz sale de `__file__`, contra «Ensayos aislados», punto 2: refuerza la recomendación del punto 5 |
| 39 | el README «dice que no se edita» | MATIZ | Lo que no se edita es `cuenta-arrastrada.txt` (README `:18-19`); la carpeta entera está en `rutas_protegidas` del contrato (§0.h) |
| 50 | cierre: el registro «# Next Action HECHA · Z ·» | MATIZ | Ya hay uno de `cases-rejilla` (`HISTORIA.md:7644`); `DECISIONES-DE-PROCESO.md:29` deja reutilizar la letra porque el registro nuevo lleva fecha |
| H2 | las posiciones abiertas a media vela | herencia | §0.f; PARADA, punto 9 |
| H4 | a5: cifras del registro escritas a mano en `costes_y_sesiones.py` | herencia | Con la propuesta del punto 5 no se copian las partes que las usan |
| H6 | ya hay un guion que simula las líneas del cierre | herencia | `anexos/RECORRIDA-CONSTRUCCION/simular_cierre.py`: se reutiliza como modelo en la entrega |
| H7 | R4.2 cita cifras de la corrida 2 (34 sesiones de P6, 77 llenadas, «sin las marcadas E») | herencia | Las marcas E son las llenadas de Z: la fase 2 dirá si esas cifras cambian (hoy solo se miran 8 sesiones), y las líneas del cierre lo recogen si R4.2 queda desfasada |
| H8 | la llenada del borde de la corrida 1 (2026-01-06 07-11 o1) no está en c) | herencia | Está en el censo de §0.e; la fase 2 la cuenta |
| obs. | el motor decide en un cierre que el bróker aún no ha evaluado | sin medir en el auditor | **Medido**, `censo_cierre.py`: de las órdenes canceladas, 0 de 158 en la corrida 1 y **22 de 1002 en la 2** se cancelaron en el cierre de una M1 sin ticks (las 22, en horas perdidas); los cierres a mercado (1 y 5), todos con ticks. Esa vela no se evalúa nunca para la orden cancelada (hoy y con la corrección): es la condición contraria a Z, una vela que no se evalúa para lo que existía mientras transcurría. PARADA, punto 8 |

### 0.m Lo que no pude medir

- Qué cambia en las corridas: exige correrlas (fase 2).
- La suite entera con el prototipo, en el clon: la guardia niega `pytest` sin rutas fuera de la
  raíz («recoge ficheros que la guardia no lee»), y `tests/regression` como directorio. Es su regla
  (`trabajo/guion-mismo-comando`), no un bloqueo de algo necesario: la suite entera la corre el
  `make check` de la rama.
- Si alguna de las 22 órdenes canceladas sin ticks se habría llenado con su vela: exige el mercado
  de esos días y no lo pide ningún punto del encargo.
- **El comando de la fase 2 con `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1` delante**: la guardia
  lo niega (el nombre no está en `NOMBRES_DE_ENTORNO`). CLAUDE.md lo dice de otra forma: la variable
  se pone «arrancando Claude Code con» ella, no delante de cada comando. PARADA, punto 10.

## Lo que necesito que decidas

0. **El número de casos de Z en las corridas.** Medido: 2 + 0 en la corrida 1 y 10 + 2 en la 2
   (llenadas + stops con la vela de su decisión); el encargo y la hoja de ruta dicen 2 y 10
   (solo llenadas). Opciones: (a) el informe y las líneas del cierre dicen las dos cifras; (b) solo
   las llenadas. Recomiendo (a): el criterio de hecho del encargo ya cuenta stops. Coste de (b):
   ninguno técnico; deja fuera 2 eventos que la rama corrige.
1. **La forma de la corrección (f, e).** Opciones: (a) vela válida si empieza en o después de
   `ultimo_cambio_ms` (orden) o de `max(abierta_ms, stop_movido_ms)` (posición); (b) lo mismo para
   la orden y para la salida con el stop de nacimiento, y la vela que contiene `stop_movido_ms` se
   evalúa con el stop ANTERIOR (ADR-0065 §4: stop primero, sin break even). Las dos con
   `decidido_ms` por defecto = `desde_ms` (niega por defecto) y sin tocar `desde` ni los ticks.
   Recomiendo (b): cumple la condición y ADR-0065 §4, que (a) incumple en el caso que este
   describe. Coste de (b): un campo más en `Posicion` (el stop anterior) y un test más; en estas
   corridas no cambia nada frente a (a) (§0.e: ninguna vela de un stop movido toca el original).
   (a) está medida con un prototipo (los tests de `main` que la rozan pasan, §0.f); (b), no.
   Y las modificaciones de orden (ninguna en las corridas): con (b), la misma regla con el precio
   anterior; con (a), la vela de la modificación no se evalúa. Recomiendo la misma de la posición.
2. **Los dos casos de futuro (a).** Opciones: (a) vuelven a Technical Debt, cada uno con su línea y
   su sonda: `_peor_del_minuto` mira hasta un minuto adelante en cada evento del respaldo, y la
   marca entra en la operación aunque cierre en ese instante; `_precio_de_mercado` y
   `precio_de_conversion` toman la vela del minuto (1 ms de futuro, la convención del motor; y la
   vela entera en un minuto con ticks sin ninguno anterior, que el motor no alcanza); (b) el de
   `_peor_del_minuto` entra en esta rama (condición «la vela empieza antes del instante», con su
   test). Recomiendo (a) para los dos y que el de `_peor_del_minuto` sea una entrada de la Next
   Action antes de la próxima corrida que cuente: cambia la peor equity que leen los topes, que es
   otra condición que la de Z. Coste de (b): ampliar el alcance y la fase 2 mide dos cambios a la vez.
3. **La deuda de cotizar (b).** Opciones: (a) vuelve a Technical Debt con su texto, ampliado: «en
   un minuto sin ticks, `Mercado.cotizacion` juzga `precio_invalido` con la M1 anterior a la que vio
   el motor, y no coincide con `precio_de_conversion` en la misma colocación (RESPALDO-M1.md §0.a,
   §0.b)»; (b) entra en esta rama. Recomiendo (a): no es la condición de Z y su arreglo es una
   decisión sobre ADR-0057 §4. Coste de (b): un ADR o una NOTA que decida la vela.
4. **La NOTA en ADR-0051 §3 (d).** Opciones: (a) la NOTA de esta rama va en §5 y en §3: en §3,
   que la salida tras un llenado del respaldo se mira desde la vela siguiente (ADR-0057 §1, el
   código y sus tests), sin cambiar lo que decide; (b) solo §5. Recomiendo (a): hoy el ADR dice lo
   contrario de lo que hace el código.
5. **Los guiones (g).** Opciones: (a) copias idénticas de `patrones.py` y `horas_perdidas.py`, y dos
   guiones nuevos (`censo_respaldo.py`, `sesiones_s14.py`), sin `entradas-antes-alternancia.txt` y
   sin R; (b) volver a correr `entradas_antes_alternancia.py` (otra corrida entera del motor con
   calentamiento, con su fila) y copiar `costes_y_sesiones.py` y `lista_s14.py` con la raíz por
   argumento. Recomiendo (a): el criterio de hecho y la comprobación de S-14 no necesitan la lista,
   y `lista_s14.py` imprime el R de las sesiones de S-14, que el encargo prohíbe imprimir. Coste de
   (b): una corrida más (~6 min, ~630 MiB) y quitar el R de la copia.
6. **La línea base (h).** Opciones: (a) NOTAS nuevas en ADR-0070 §3 y en ACTIVAR-A35-A44.md §5
   (amplía el contrato a ese runbook, como prevé el encargo), y el README nuevo de
   `anexos/RESPALDO-M1/`; los de RECORRIDA no se tocan; (b) solo la NOTA de ADR-0070. Recomiendo
   (a): las dos que hoy la nombran como documento de trabajo quedan al día.
7. **La fila de las fases 1 y 2 (k).** Opciones: (a) la de §0.k, en su propio commit antes de correr,
   con el mes de calentamiento de enero medido antes de escribirla; (b) una fila por fase. Recomiendo
   (a): son las mismas lecturas que en RECORRIDA y se declaran juntas, el mismo día que empiezan.
8. **Las decisiones en el cierre de una M1 sin ticks que dejan de evaluar algo** (observación del
   auditor, medida: 22 cancelaciones en horas perdidas en la corrida 2, 0 en la 1). El motor
   decide en el cierre de *k* menos 1 ms y el bróker evalúa la vela *k* después, así que una orden
   cancelada en ese cierre nunca se evalúa contra la vela en que aún vivía (con ticks, sí: sus
   ticks van antes). Es la condición contraria a la de Z y no la cambia ninguna de las dos formas.
   Opciones: (a) Technical Debt con su línea y el recuento, y una entrada de la Next Action antes de
   la próxima corrida que cuente; (b) entra en esta rama (sellar la vela *k* para lo que ya existía
   antes de la decisión, que toca el instante del evento de ADR-0051 §5). Recomiendo (a): cambia
   ADR-0051 §5 y es otra condición. Coste de (b): un ADR y medir dos cambios a la vez.
9. **Las posiciones abiertas a media vela (`abrir_conocida`, la repetición del trader sin ticks).**
   Opciones: (a) la condición vale también para ellas: la vela de la apertura no cuenta en el
   respaldo (negar por defecto; con ticks no cambia); (b) excepción para `abrir_conocida`, con la
   vela de la apertura evaluada entera, como hoy. Recomiendo (a): la condición es la misma y la
   vela lleva precios anteriores a la apertura; los tests de `main` que la usan pasan con el
   prototipo (§0.f). Coste de (a): la repetición del trader sin ticks (ADR-0051 §8,
   `REPETICION-TRADER-SALIDA.txt`) ya no se reproduciría igual; no se vuelve a correr en esta rama
   y la NOTA de ADR-0051 lo dice.
10. **El comando de las corridas con `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1` delante.** La
   guardia lo niega (no está en `NOMBRES_DE_ENTORNO`). Opciones: (a) Aleks arranca Claude Code con
   la variable antes de la fase 2, como dice CLAUDE.md, y las corridas van sin ella delante, en
   segundo plano; (b) Aleks las lanza con `!` y la variable delante. Recomiendo (a): es lo que dice
   CLAUDE.md y no hace falta tocar la guardia. Coste de (b): ninguno, salvo que el `TIEMPO` y la
   `MEMORIA` los copio de su salida.

## Respuesta del consultor a la PARADA (2026-10-29)

Copiada tal cual:

> Modelo: Opus 5.5 · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA de la fase 0 de trabajo/respaldo-m1 (2026-10-29). Cópiala tal cual al final del encargo y del informe, en «Respuesta del consultor a la PARADA», con su fecha, y aplícala punto por punto (skill fase-cero).
>
> Contexto de la decisión del punto 1. Tu fase 0 mide cuatro síntomas: los casos de Z, los 22 cancelados en el cierre de una M1 sin ticks (punto 8), la marca un minuto adelante de _peor_del_minuto (punto 2) y ADR-0065 §4 sin cumplir. Pensé que tenían una raíz común: el respaldo sella su evento en el cierre de la vela (k fin, ADR-0051 §5 y ADR-0057 §1), un milisegundo después de que el motor decida (k fin - 1). Por eso estudié una forma (c): sellar en k fin - 1. Mi auditor la probó con un prototipo en memoria sobre main, con datos sintéticos, y midió que (c) no es neutral fuera de las tres funciones de llenado.py:
> - la posición abierta por el respaldo cae en el minuto k, así que las marcas (broker.py:888 y :909-913) meten la vela del llenado. En la sonda, una marca de 970 por debajo de un stop de 990 llega a cuenta.marcar y a los topes antes de la decisión;
> - el break even por velas (primitivas_broker.py:279, m1_entre desde abierta_ms) mete la vela del llenado en la zona posterior de RN-014;
> - un llenado en la última vela de 07-11 pasa de la sesión 11-15 a la 07-11 (cableado.py:464-465);
> - cambian el fin de la ventana (la última vela pasa a evaluarse) y el borde de la ventana prohibida (ADR-0068);
> - rompen 5 tests de main, todos por ese milisegundo;
> - y choca con ADR-0057 §1, que también sella al cierre y está en «QUÉ NO CAMBIA».
> Así que (c) es otra rama con su propio ADR, no esta. Va como entrada nueva (punto 8), con lo que midió el auditor.
>
> 0. (a). El informe y las líneas del cierre dicen las dos cifras: 2 llenadas y 0 stops en la corrida 1; 10 llenadas y 2 stops en la 2.
>
> 1. (b), tal como la propones:
>    - las tres funciones del respaldo reciben el instante de la decisión de lo que evalúan, decidido_ms, que por defecto vale desde_ms. Una vela solo cuenta si EMPIEZA en o después de él. El instante sale del objeto: ultimo_cambio_ms en la orden; abierta_ms en la salida con el stop de nacimiento;
>    - la vela que contiene stop_movido_ms se evalúa con el stop ANTERIOR (ADR-0065 §4) y las siguientes con el nuevo;
>    - una orden modificada sigue la misma regla con su precio anterior.
>    Sin tocar desde, el «ahora - 1», los ticks, el instante del evento (sigue en el cierre de la vela, ADR-0051 §5 y ADR-0057 §1) ni _fin_ms, que también usa Mercado.cotizacion.
>    (b) no está prototipada. Los tests de main que la rozan (los de §0.f y los nueve ficheros del prototipo de (a)) tienen que pasar sin tocarlos. Si alguno tiene que cambiar, PARADA.
>    Los tests de la fase 1 cubren, además de los del encargo, el stop movido: una vela que toca el stop original y la entrada sale por el stop original, sin break even. Y la modificación de una orden con su precio anterior.
>
> 2. Los dos casos de futuro no se arreglan aquí.
>    - _peor_del_minuto entra en la letra nueva del punto 8, nombrado por su condición: acepta toda vela que EMPIEZA en o antes de «hasta», así que cuando se avanza hasta un instante redondo (cada evento del respaldo, una cancelación por ventana, una expiración) marca entera la vela siguiente. Va con su sonda 5 y con la del auditor (avanzar a un instante redondo marca la vela siguiente).
>    - _precio_de_mercado y precio_de_conversion van al punto 3.
>
> 3. (a), en una línea de Technical Debt que nombra la condición: «Las cotizaciones sin tick del bróker no usan la misma vela. En el cierre de la M1 k, Mercado.cotizacion (precio_invalido y stops_level, ADR-0057 §4) usa lo último cerrado antes del instante, que sin ticks es la M1 k-1 o el último tick anterior, y _precio_de_mercado y precio_de_conversion (cierre a mercado y margen) usan la k. Y en un minuto con ticks sin ninguno anterior al instante, estas dos toman el cierre de su vela; el motor no llega a ese caso (RESPALDO-M1.md §0.a y §0.b). Decidirlo es una NOTA o un ADR sobre ADR-0057 §4.»
>
> 4. (a). La NOTA va en ADR-0051 §5, con la condición de (b): la vela cuenta si empieza en o después de lo decidido, y la vela del stop movido se evalúa con el stop anterior. Y otra en §3: la salida tras un llenado del respaldo se mira desde la vela siguiente (ADR-0057 §1, el código y sus tests), sin cambiar lo que decide.
>
> 5. (a), con dos condiciones:
>    - censo_respaldo.py detecta Z por la condición general (el inicio de la vela del evento, (ms - 1) // 60000 en minutos, es anterior al instante decidido) y no solo por colocada == ms - 1. Así el criterio de hecho de la fase 2 no queda vacío por construcción.
>    - sesiones_s14.py toma el lado de «### Ordenes» si lo trae. Si no, la deducción por la caja 1 se comprueba en las 8 sesiones contra la diaria de RECORRIDA, y tiene que dar el mismo lado que dibujó scripts/graficos_sesion.py. Si alguna no cuadra, PARADA.
>
> 6. (a). El contrato se amplía a docs/runbooks/ACTIVAR-A35-A44.md en un commit a la vista, solo para la NOTA de §5.
>
> 7. (a).
>
> 8. (a), en UNA letra nueva de la Next Action, no en Technical Debt. Elígela con la regla de letras de DECISIONES-DE-PROCESO.md y di cuál es, con el grep. Su texto, en el cierre:
>    «<letra>. En el respaldo M1 el evento de una vela se sella en su cierre, un milisegundo después de que el motor decida (ADR-0051 §5, ADR-0057 §1). Por eso la vela k no se evalúa para lo que vivía en ella cuando el motor actúa en su cierre (22 de 1002 cancelaciones en la corrida diaria de recorrida-construccion, RESPALDO-M1.md §0.l), y _peor_del_minuto marca entera la vela siguiente cuando se avanza hasta un instante redondo. Rama propia con un ADR que enmiende esos dos ADR. Antes de decidir, se mide lo que el auditor de RESPALDO-M1 encontró en la forma «sellar en k fin - 1»: las marcas y m1_entre del break even empiezan a contar la vela del llenado, cambia la sesión de un llenado en la última vela de 07-11, cambian el fin de la ventana y el borde de ADR-0068, y rompen 5 tests de main por el milisegundo. Va antes de la próxima corrida del arnés que cuente (ADR-0070 §3).»
>    En la hoja de ruta entra R3.6 con esa letra (Refs NA:<letra> · ID:ADR-0051 · ID:ADR-0057; Depende de: R3.5; Quién: la sesión, con el encargo del consultor; Hecho cuando: el ADR está aceptado, un test que rompe en main pasa en la rama y las dos corridas están repetidas). R5.2 nombra la letra nueva en «Depende de», en lugar de NA:Z.
>    Comprueba la copia contra test_hoja_de_ruta.
>
> 9. (a). La NOTA de ADR-0051 dice que la repetición del trader sin ticks (ADR-0051 §8, REPETICION-TRADER-SALIDA.txt) ya no se reproduce igual, y que esta rama no la vuelve a correr.
>
> 10. (a). Antes de la fase 2, Aleks cierra Claude Code y lo vuelve a abrir con la variable puesta. Al empezar la fase 2, compruebas que vale 1 y escribes en el informe cómo lo has comprobado. Las corridas van sin la variable delante y en segundo plano. Si la variable no está puesta, PARADA antes de correr.
>
> Dos hallazgos del consultor para la fila de ERRORES-RECURRENTES de la rama, en el cierre. Los dos los encontró su auditor antes de que llegaran a la sesión:
> - En el encargo escribí la condición de Z como «una vela cuyo intervalo empieza en o antes de ese instante no cuenta», con la NOTA en el mismo sentido, sin medir el borde y sin leer ADR-0057 §1. Lección: una condición sobre instantes se escribe con el borde medido (qué vale exactamente en el instante de la decisión) y con todos los ADR que fijan ese borde.
> - En el primer borrador de esta respuesta propuse mover el sello del respaldo a k fin - 1, con una regla para que la sesión decidiera sola. No había buscado los otros lectores de abierta_ms y del minuto del evento (las marcas, el break even por velas, la sesión, la ventana). Y la regla se contradecía: pedía tests de main intactos y a la vez admitía que cambiaran. Lección: antes de proponer que se mueva un instante, se buscan con grep todos los que lo leen. Y una regla que deja decidir a la sesión no puede contradecirse ni tocar lo que «QUÉ NO CAMBIA» protege.
>
> Lo que sigue, en este orden: el commit con esta respuesta; la fase 1; Aleks reinicia Claude Code con la variable; la fase 2; el informe, el revisor y la entrega. make check en verde antes de cada commit, con ruff format, ruff check y mypy antes sobre lo tocado. Si la guardia o el clasificador niegan algo, PARADA con el comando exacto, y lo lanza Aleks con «!».
>
> Rama lista para revisión, NO cerrada.

## 1. La respuesta aplicada, punto por punto

| Punto | Qué | Estado |
|---|---|---|
| 0 | Las dos cifras (2 llenadas y 0 stops en la corrida 1; 10 y 2 en la 2) en el informe y en las líneas del cierre | en las líneas del cierre (entrega) |
| 1 | La forma (b) en `llenado.py` y `broker.py`, con sus tests | **hecho** (§2.1, §2.2) |
| 2 | `_peor_del_minuto` a la letra nueva (punto 8); `_precio_de_mercado` y `precio_de_conversion` al punto 3 | en las líneas del cierre |
| 3 | La línea de Technical Debt de las cotizaciones sin tick, con su texto | en las líneas del cierre |
| 4 | Las NOTAS de ADR-0051 §5 y §3 | **hecho** (§2.1) |
| 5 | `censo_respaldo.py` (Z por la condición general) y `sesiones_s14.py` (el lado, comprobado) | guiones escritos y probados (§3); el lado, PARADA 2 |
| 6 | El contrato se amplía a `docs/runbooks/ACTIVAR-A35-A44.md`, solo para la NOTA de §5 | **hecho** en este commit (`contrato.yaml`) |
| 7 | La fila de exposiciones de las fases 1 y 2, en su propio commit antes de correr | **hecho**: la de la fase 1 en beb9c93; la de la fase 2, en el commit de §3, antes de correr |
| 8 | La letra nueva de la Next Action, R3.6 en la hoja de ruta, R5.2 | **letra elegida: H** (abajo); el texto, en las líneas del cierre |
| 9 | La NOTA de ADR-0051 sobre la repetición del trader sin ticks | **hecho** (NOTA de §5) |
| 10 | La variable `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP`, comprobada al empezar la fase 2 | fase 2 |

**La letra del punto 8.** Regla (`DECISIONES-DE-PROCESO.md:29`): una letra se reutiliza solo si su
registro «# Next Action HECHA» es anterior y la hoja de ruta no la nombra. Medido con un guion de la
carpeta de trabajo (`letras.py <raíz>`, que solo lee `PROJECT_STATE.md`, `docs/state/HISTORIA.md` y
`docs/plan/HOJA-DE-RUTA.md`, con `^# Next Action HECHA · X · ` y `\bNA:X\b`):

```
vivas: ABCDFGIJKLMNQTUZ
E: registros HECHA 3; NA:E en la hoja 1
H: registros HECHA 1; NA:H en la hoja 0
O: registros HECHA 2; NA:O en la hoja 1
P: registros HECHA 2; NA:P en la hoja 1
R: registros HECHA 1; NA:R en la hoja 0
S: registros HECHA 1; NA:S en la hoja 1
V: registros HECHA 2; NA:V en la hoja 0
W: registros HECHA 2; NA:W en la hoja 1
X: registros HECHA 1; NA:X en la hoja 2
Y: registros HECHA 2; NA:Y en la hoja 1
```

Cumplen las dos condiciones H, R y V; se toma **H**, la primera por orden alfabético. Z, al salir en
el cierre, también quedaría libre, pero hoy la hoja de ruta la nombra (R3.5 y R5.2).

## 2. Fase 1 · La corrección y sus tests (2026-10-29)

### 2.1 La corrección (forma (b) del punto 1)

- `engine/llenado.py`: `primer_llenado_limite`, `primer_llenado_stop` y `primera_salida` reciben
  `decidido_ms` (por defecto `desde_ms`: niega por defecto) y `anterior` (instante en que se decidió
  la versión anterior, su nivel). En el respaldo, el nivel de cada vela lo da `_nivel_de_la_vela`:
  el vigente si la vela empieza en o después de `decidido_ms`; si no, el anterior si se decidió en o
  antes de que la vela empiece; si no, la vela no cuenta. No cambian `desde`, el «ahora − 1», los
  ticks, `_fin_ms` ni el instante del evento (el cierre de la vela).
- `engine/broker.py`: `Orden.anterior` (instante, precio, stop, objetivo) lo guarda `modificar`;
  `Posicion.stop_anterior` (desde cuándo valía, stop) lo guarda `_mover`. `_proximo_evento` pasa
  `o.ultimo_cambio_ms` y la versión anterior a la orden, y `abierta_ms` o `stop_movido_ms` con el
  stop anterior a la salida. `_aplicar`: si llena una orden la versión anterior (el evento del
  respaldo sale de una vela que empezó antes de la modificación), la orden vuelve a su precio, stop
  y objetivo de antes; si salta el stop anterior en la vela en cuyo cierre se movió, la posición
  vuelve a ese stop y, si era el de nacimiento, `stop_original` queda en `None`: se clasifica como
  stop entero y no como break even (ADR-0065 §4). La traza conserva el `stop_movido` y su petición,
  porque se enviaron.
- Docstring de `llenado.py`: la cabecera ya no dice «PROPUESTO»; la línea del respaldo dice la
  regla, como la de los ticks, y «SIN MIRAR AL FUTURO» gana su contrapartida («NI AL PASADO»).
- NOTAS en ADR-0051 §3 (la salida tras un llenado del respaldo, desde la vela siguiente: ADR-0057
  §1) y §5 (la condición, la versión anterior y la repetición del trader sin ticks: puntos 4 y 9).
  El cuerpo no cambia.

Ninguna cifra, parámetro, spec ni caso: `git diff main --stat -- knowledge/ config/` vacío.

### 2.2 Los tests, en los dos lados

`tests/unit/test_respaldo_m1_decision.py`, 12 tests con velas y ticks sintéticos de 2030:

| Test | Qué fija | `main` | rama |
|---|---|---|---|
| `test_una_stop_colocada_en_el_cierre_de_una_m1_sin_ticks_no_se_llena_con_esa_vela` | encargo 1 | FAILED (`llenada … respaldo_m1` con la vela de la decisión) | PASSED |
| `test_una_limite_colocada_en_el_cierre_de_una_m1_sin_ticks_no_se_llena_con_esa_vela` | encargo 2 | FAILED (ídem) | PASSED |
| `test_en_el_borde_de_la_ventana_la_orden_solo_se_evalua_contra_los_ticks_que_siguen` | encargo 3 | FAILED (respaldo al fin de M0 en vez del tick de M0+1) | PASSED |
| `test_el_stop_movido_en_el_cierre_de_una_m1_sin_ticks_no_salta_con_esa_vela` | encargo 4 (e) | FAILED (sale a break even con la vela que lo movió) | PASSED |
| `test_la_vela_del_stop_movido_que_toca_el_stop_original_sale_por_el_sin_break_even` | punto 1, ADR-0065 §4 | FAILED (`('stop', 1000, …)` en vez de 990) | PASSED |
| `test_la_vela_de_una_modificacion_se_evalua_con_la_orden_anterior` | punto 1 | FAILED (no llena) | PASSED |
| `test_la_vela_de_una_modificacion_no_llena_la_version_nueva` | punto 1 | FAILED (llena una vela antes) | PASSED |
| `test_sin_instante_decidido_la_funcion_pura_niega_por_defecto` | negar por defecto | FAILED (llena con `desde` a media vela) | PASSED |
| `test_una_pendiente_de_antes_de_una_vela_sin_ticks_se_llena_en_esa_vela` | f), 1 | PASSED | PASSED |
| `test_el_tick_del_ultimo_evento_puede_llenar_otra_pendiente` | f), 2 | PASSED | PASSED |
| `test_la_salida_tras_un_llenado_del_respaldo_se_mira_desde_la_vela_siguiente` | f), 3 (ADR-0057 §1) | PASSED | PASSED |
| `test_con_ticks_el_instante_de_la_decision_ya_no_contaba` | lo que va por ticks | PASSED | PASSED |

**Lado `main`** (`comparar-con-main`; estado del repo antes: `git status --short` con los tres
ficheros de la fase 1 sin commitear, `git branch --list` = `main` y `trabajo/respaldo-m1`, 143
tags): `git worktree add --detach C:/cm/main main`, el test copiado dentro del clon, `uv run pytest
tests/unit/test_respaldo_m1_decision.py -q -p no:cacheprovider -rA` → 8 FAILED y 4 PASSED; con
`--tb=line`, las 8 son `AssertionError` por la vela de la decisión, ninguna por otra causa:

```
E   AssertionError: assert [(18946944600...respaldo_m1')] == []
E   AssertionError: assert [(18946944600...respaldo_m1')] == []
E   AssertionError: assert [(18946944600...respaldo_m1')] == [(18946944800...'v', 'ticks')]
E   AssertionError: assert (False)
E   AssertionError: assert ('stop', 1000...'respaldo_m1') == ('stop', 990,...'respaldo_m1')
E   AssertionError: assert [] == [(18946945200...respaldo_m1')]
E   AssertionError: assert [(18946945200...respaldo_m1')] == [(18946945800...respaldo_m1')]
E   AssertionError: assert Evento(tipo='llenado', instante_ms=1894694460000, precio=1000, fuente='respaldo_m1', minuto=31578240) is None
```

(1894694460000 es el fin de M0, 2030-01-15 08:01:00Z.) El clon se quitó con `--force` (llevaba el
test copiado, sin seguir) y `git worktree prune`; después, `git branch --list` y los 143 tags,
iguales.

**Lado rama**: en el repositorio, `uv run pytest tests/unit/test_respaldo_m1_decision.py
tests/unit/test_llenado.py tests/unit/test_broker.py tests/unit/test_broker_ordenes_stop.py
tests/unit/test_be_al_tick.py tests/unit/test_instante_llenado.py tests/unit/test_caja_hasta_el_llenado.py
tests/unit/test_simulacion.py tests/unit/test_cableado.py tests/regression/test_cuenta_7_de_agosto.py
-q` → todos pasan: los 12 nuevos y **los nueve ficheros de `main` del prototipo de (a), sin
tocarlos** (punto 1: ninguno tuvo que cambiar; con los datos de agosto, la regresión no se salta).
La suite entera, en el `make check` del commit (§2.3).

Y, con la rama ya commiteada (beb9c93), su clon desechable (`git worktree add --detach C:/cm/rama
HEAD`): `uv run pytest tests/unit/test_respaldo_m1_decision.py -q -p no:cacheprovider -rA` → **12
PASSED**. Clon quitado sin `--force` (no quedaba nada sin seguir) y `git worktree prune`; después,
`git status --short` vacío, `git branch --list` = `main` y `trabajo/respaldo-m1`, 143 tags: lo mismo
que antes. Nada se creó en origin (ningún push).

### 2.3 El commit de la fase 1

`ruff format`, `ruff check` y `mypy` sobre `llenado.py`, `broker.py` y el test: limpios. `make
check` de beb9c93: exit 0, ningún `failed`, `SELLO` sobre el árbol f9c33d73…; **3038 passed** en
1056 s (la suite entera: ningún test de `main` cambió ni rompió); 1139 s en total; `PICO DE MEMORIA
de make check: 300 MiB en test`.

## 3. Antes de la fase 2: los guiones, el README y la fila

En su propio commit, antes de correr nada (punto 7): `docs/validation/anexos/RESPALDO-M1/` con su
README; `patrones.py` y `horas_perdidas.py`, copias idénticas (`sha256sum`: 330b7d62… y dfa782a3…,
los mismos que en `anexos/RECORRIDA-CONSTRUCCION/`); `censo_respaldo.py` y `sesiones_s14.py`,
nuevos; y la fila del 2026-10-29 de la fase 2 en HOLDOUT-EXPOSICIONES.

**Los guiones, probados sobre las salidas de RECORRIDA** (solo leen ficheros commiteados):
- `censo_respaldo.py` sobre `cuenta-arrastrada.txt` y la diaria de RECORRIDA: Z = 2 y Z = 10
  (las llenadas), y 2 stops de la diaria en «vela del stop movido», que con el código de `main`
  eran Z (§0.e). Reproduce el censo de §0.e por la condición general, como pide el punto 5.
- `sesiones_s14.py` con la diaria de RECORRIDA a los dos lados: las 8 sesiones P6, «0 cambian», y
  la M1 de colocación de cada primera orden, la misma que la tabla de BARRIDO-SESION-6.md §1.d en
  hora de Madrid (por ejemplo, la fila 18: 05:32:59.999Z = 07:32 de Madrid).

**Lo que el punto 5 da por hecho y no es así (PARADA 2).** `scripts/graficos_sesion.py` **no dibuja
el lado**: su `Orden` solo lleva `colocada` y `punto` (`graficos_sesion.py:98-101`), y lo dibujado
son las velas cortadas en la M1 de colocación y, en el marcado, la línea del punto (BARRIDO-SESION-6
§2.2; la fila del 2026-10-28 de HOLDOUT-EXPOSICIONES: «sin orden, stop, objetivo, llenado ni
resultado»). «### Ordenes» tampoco trae el lado. Así que «tiene que dar el mismo lado que dibujó
`scripts/graficos_sesion.py`» no se puede comprobar. Lo que sí he medido: la regla de la caja 1
(venta si queda por encima del precio, compra si por debajo) contra el lado de las 291 llenadas de la
diaria de RECORRIDA que trae `entradas-antes-alternancia.txt` → **291 cuadran, 0 no**
(`lado_caja1.py`, guion de la carpeta de trabajo que solo lee esos dos ficheros e imprime
recuentos). `sesiones_s14.py` compara lo que el gráfico SÍ dibuja (la M1 de colocación y el punto)
y, además, el precio y el lado deducido.

## Estado

EN CURSO: fase 1 hecha (beb9c93); fase 2 preparada. PARADA 2 (el lado del punto 5) y espera a que
Aleks reinicie Claude Code con la variable (punto 10).
