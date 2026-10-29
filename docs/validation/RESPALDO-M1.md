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

## Respuesta del consultor a la PARADA 2 (2026-10-29)

Copiada tal cual:

> Modelo: Opus 5.5 · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA 2 de trabajo/respaldo-m1 (2026-10-29). Cópiala tal cual al final del encargo y del informe, en «Respuesta del consultor a la PARADA 2», con su fecha, y aplícala.
>
> 1. (a). sesiones_s14.py compara, en las 8 sesiones, lo que el gráfico dibuja (la M1 de colocación y el punto de la primera orden) y, además, el precio y el lado deducido por la caja 1, que ya está validado en las 291 llenadas de la diaria de RECORRIDA cuyo lado se conoce. El informe dice que el lado se deduce, con esa validación. Si en alguna sesión cambia CUALQUIERA de las cuatro cosas (M1, punto, precio o lado deducido) entre la diaria de RECORRIDA y la nueva, o si deja de ser P6, PARADA antes de seguir, sin imprimir ningún R.
> 2. La letra H para el punto 8: aceptada, con su grep en el informe.
> 3. Un hallazgo más del consultor para la fila de ERRORES-RECURRENTES, en el cierre: en la respuesta a la PARADA pedí comparar «el mismo lado que dibujó scripts/graficos_sesion.py» sin leer el script, que no dibuja el lado (graficos_sesion.py:98-101). Lección: una comprobación contra un artefacto se escribe después de leer qué contiene ese artefacto.
> 4. Lo que sigue: el commit con esta respuesta; Aleks reinicia Claude Code con la variable; compruebas que vale 1 y escribes cómo lo has comprobado; la fase 2 como dice el encargo, una corrida cada vez, en segundo plano y nunca a la par de un make check; el informe, el revisor y la entrega. Si la variable no está puesta, PARADA antes de correr.
>
> make check en verde antes de cada commit. Si la guardia o el clasificador niegan algo, PARADA con el comando exacto, y lo lanza Aleks con «!».
>
> Rama lista para revisión, NO cerrada.

**La respuesta aplicada.** 1: `sesiones_s14.py` ya compara las cuatro cosas (M1 de colocación,
punto, precio y lado deducido por la caja 1, validada en 291 de 291 llenadas, §3) y si sigue siendo
P6; si cambia cualquiera, PARADA antes de seguir. 2: la letra H, con su grep en §1. 3: el hallazgo
va a la fila de ERRORES-RECURRENTES preparada para el cierre. 4: este commit; después, el reinicio.

## 4. Fase 2 · Las corridas repetidas (2026-10-29)

### 4.1 La variable, antes de correr (punto 10)

`printenv CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP` → `1` (código 0), en el shell de la
herramienta Bash, que hereda el entorno del proceso de Claude Code. No sale de un perfil de bash
(`grep` en `~/.bashrc`, `~/.bash_profile` y `~/.profile`: nada) ni de ningún `settings*.json` de
`~/.claude/` ni de `.claude/` del proyecto (Grep: nada): viene del entorno con que se arrancó Claude
Code. Leerla en el registro de Windows con PowerShell (`[Environment]::GetEnvironmentVariable`) lo
niega la guardia («una llamada a .NET»), y no la he rodeado. Como ya valía 1, pregunté a Aleks si
reiniciaba o lanzaba; respondió «Lanza ya». Ninguna corrida murió.

### 4.2 Los comandos, en orden, con su salida

Todos desde la raíz, sobre el código commiteado (823404a), uno a uno, en segundo plano, sin nada a
la par:

| # | Comando | Salida | TIEMPO / MEMORIA |
|---|---|---|---|
| 1 | `uv run botsito motor arnes --simular --salida docs/validation/anexos/RESPALDO-M1/cuenta-arrastrada.txt` | `exit=0`; `OK: informe del arnes en docs\validation\anexos\RESPALDO-M1\cuenta-arrastrada.txt` | `TIEMPO: 351.0 s; MEMORIA: pico del proceso de 630.3 MiB` |
| 2 | `uv run botsito motor arnes --simular --diagnostico-cuenta-diaria --salida docs/validation/anexos/RESPALDO-M1/diaria.txt` | `exit=0`; escribe **`diaria.DIAGNOSTICO.cuenta=diaria.txt`** (el nombre real, como en RECORRIDA) | `TIEMPO: 315.8 s; MEMORIA: pico del proceso de 638.4 MiB` |
| 3 | `uv run botsito motor arnes --simular --salida "C:/Users/USER/AppData/Local/Temp/claude/C--Users-USER-Desktop-Bot-v3/c5921e91-beb5-4611-b646-e089f72fda40/scratchpad/cuenta-arrastrada.txt"`; `diff docs/validation/anexos/RESPALDO-M1/cuenta-arrastrada.txt "C:/Users/USER/AppData/Local/Temp/claude/C--Users-USER-Desktop-Bot-v3/c5921e91-beb5-4611-b646-e089f72fda40/scratchpad/cuenta-arrastrada.txt"`; `rm "C:/Users/USER/AppData/Local/Temp/claude/C--Users-USER-Desktop-Bot-v3/c5921e91-beb5-4611-b646-e089f72fda40/scratchpad/cuenta-arrastrada.txt"` | `exit=0`; `diff=0` (**idénticas byte a byte**); `rm=0` | `TIEMPO: 347.7 s; MEMORIA: pico del proceso de 630.1 MiB` |
| 4 | `python -B docs/validation/anexos/RESPALDO-M1/sesiones_s14.py "docs/validation/anexos/RECORRIDA-CONSTRUCCION/diaria.DIAGNOSTICO.cuenta=diaria.txt" "docs/validation/anexos/RESPALDO-M1/diaria.DIAGNOSTICO.cuenta=diaria.txt" > docs/validation/anexos/RESPALDO-M1/sesiones-s14.txt` | `exit=0` | — |
| 5 | `python -B docs/validation/anexos/RESPALDO-M1/censo_respaldo.py docs/validation/anexos/RESPALDO-M1/cuenta-arrastrada.txt "docs/validation/anexos/RESPALDO-M1/diaria.DIAGNOSTICO.cuenta=diaria.txt" docs/validation/anexos/RECORRIDA-CONSTRUCCION/cuenta-arrastrada.txt "docs/validation/anexos/RECORRIDA-CONSTRUCCION/diaria.DIAGNOSTICO.cuenta=diaria.txt" > docs/validation/anexos/RESPALDO-M1/censo-respaldo.txt` (vuelto a correr tras a4 del revisor: `diff` con el anterior vacío) | `exit=0` | — |
| 6 | `python -B docs/validation/anexos/RESPALDO-M1/patrones.py docs/validation/anexos/RESPALDO-M1/cuenta-arrastrada.txt > docs/validation/anexos/RESPALDO-M1/patrones-arrastrada.txt` y `python -B docs/validation/anexos/RESPALDO-M1/patrones.py "docs/validation/anexos/RESPALDO-M1/diaria.DIAGNOSTICO.cuenta=diaria.txt" > docs/validation/anexos/RESPALDO-M1/patrones-diaria.txt`; después `sed -i 's/$//'` sobre las dos (su `print` escribe CRLF en Windows) | `exit=0` (las dos) | — |
| 7 | `diff docs/validation/anexos/RECORRIDA-CONSTRUCCION/cuenta-arrastrada.txt docs/validation/anexos/RESPALDO-M1/cuenta-arrastrada.txt > docs/validation/anexos/RESPALDO-M1/diff-linea-base.txt` | `diff=1` (hay diferencias: no es un fallo); 544 líneas | — |

Los tiempos caen en lo esperado (299 a 343 s en RECORRIDA; 351,0 s, un 2 % por encima del máximo);
la memoria, igual (629 a 638 MiB).

### 4.3 Las 8 sesiones de S-14 (antes que nada; respuesta a la PARADA 2, punto 1)

`sesiones-s14.txt`: **las 8 siguen siendo P6** (las mismas filas P6 en cada una) y **su primera
orden tiene la misma M1 de colocación, el mismo punto, el mismo precio y el mismo lado deducido**
(«sesiones que cambian: 0»). El lado se deduce de la caja 1 (venta si queda por encima del precio,
compra si por debajo), validado en las 291 llenadas de la diaria de RECORRIDA cuyo lado se conoce
(291 cuadran, §3). No hay PARADA: los gráficos de S-14 de la sesión 6 siguen valiendo. Ningún R
impreso.

### 4.4 El criterio de hecho: cero eventos con la vela de su decisión

`censo-respaldo.txt` (por la condición general: el inicio de la vela del evento frente al instante
en que se decidió lo evaluado):

| Salida | eventos del respaldo | llenadas | stops | `stop_movido` | modificar = stops movidos | **Z** |
|---|---|---|---|---|---|---|
| RESPALDO-M1 / corrida 1 | 7 | 3 | 3 | 1 | 21 = 21 | **0** |
| RESPALDO-M1 / corrida 2 | 22 | 9 | 9 | 4 | 118 = 118 | **0** |
| RECORRIDA / corrida 1 | 8 | 4 | 3 | 1 | 21 = 21 | 2 |
| RECORRIDA / corrida 2 | 34 | 16 | 14 | 4 | 118 = 118 | 10, y 2 stops en la vela del stop movido que con `main` eran Z (§0.e) |

**Criterio de hecho cumplido: Z = 0 en las dos corridas nuevas**, y ningún stop en la vela de su
stop movido. Los demás eventos del respaldo, todos en horas perdidas y con la vela posterior a su
decisión: en la corrida 1, 3 llenadas (2026-01-05 o19 a las 10:22, **o20 a las 10:25, una vela
después que en RECORRIDA**, o21 a las 10:56), sus 3 stops y 1 stop movido (pos-o20, 10:28:59.999),
que salta a las 10:37 con la vela posterior. En la corrida 2, 9 llenadas, 9 stops y 4 stops movidos
(su lista, en el fichero). Desaparecen del respaldo las 2 del borde de la ventana (2026-01-06 o1,
que ahora se llena por ticks a las 06:00:03.566 a 1.17297, y 2026-04-07 o1) y, en la diaria, las de
2026-04-06 o12, 2026-04-07 o28, 2026-04-23 o3, 2026-07-10 o3 y o4 y 2026-08-20 o14 dejan de llenarse
con su vela. Los dos stops de §0.e ya no saltan en la vela de su stop movido: el 2026-04-06, o11
se llena a las 10:02 (la vela siguiente a la que la colocó) y ya no hay una segunda llenada a las
10:03 (los ids de las órdenes posteriores se renumeran: la o12 nueva es otra orden); el stop de pos-o11,
movido a las 10:06:59.999, salta a las 10:15. El 2026-04-07, el de pos-o29, movido a las
10:32:59.999, salta a las 10:38.

### 4.5 Qué cambia frente a recorrida-construccion, por corrida

Sin interpretar: la clasificación de las diferencias es del consultor.

**Corrida 1 (la que cuenta).** El veredicto literal no cambia:
`habilita medir el conjunto de medida (2026-05) (ADR-0070): no (cobertura 3.5 % por debajo de 70.0 %; precision 13.2 % por debajo de 60.0 %)`.

| mes | trader | bot puntuables | parejas | cobertura | precisión | llenadas |
|---|---|---|---|---|---|---|
| 2026-04 | 35 | 0 (0) | 0 (0) | 0,0 % (0,0) | sin definir | 0 (0) |
| 2026-07 | 67 | 0 (0) | 0 (0) | 0,0 % | sin definir | 0 (0) |
| 2026-08 | 42 | 0 (0) | 0 (0) | 0,0 % | sin definir | 0 (0) |
| 2026-01 | 54 | 53 (53) | 7 (7) | 13,0 % (13,0) | 13,2 % (13,2) | 53 (53) |

(entre paréntesis, RECORRIDA). RN-032 congela la cuenta arrastrada **desde el mismo día, el
2026-01-20** (la última sesión con llenado es la 11-15 del 2026-01-20 en las dos; desde el 21 la
curva no cambia), con `estado: EN_CURSO`. Lo que sí cambia: las dos llenadas de Z (2026-01-05 o20
a las 10:25:00 en vez de las 10:24:00; 2026-01-06 o1 por ticks a las 06:00:03.566 y 1.17297 en vez
del respaldo a las 06:00:00 y 1.17293), y con ellas el saldo y la equity de cada día desde el
2026-01-06 (saldo final 90.652,93 frente a 90.741,16) y los lotes de las órdenes posteriores, que se
calculan sobre el saldo (`diff-linea-base.txt`, 544 líneas: «Por operacion» 2 filas, la curva, los
eventos y «### Ordenes»). Patrones (`patrones-arrastrada.txt`): idénticos a los de RECORRIDA (T0 7,
P1 44, P2 11, P3 11, P4 124, P5 37, P6 9, P7 1).

**Corrida 2 (la diaria, diagnóstico).** El veredicto literal:
`habilita medir el conjunto de medida (2026-05) (ADR-0070): no (opción fuera de la lista: --diagnostico-cuenta-diaria; cobertura 20.2 % por debajo de 70.0 %; precision 15.4 % por debajo de 60.0 %)`
(RECORRIDA: 20,7 % y 15,6 %).

| mes | trader | bot puntuables | parejas | cobertura | precisión | llenadas |
|---|---|---|---|---|---|---|
| 2026-04 | 35 | 51 (53) | 7 (7) | 20,0 % (20,0) | 13,7 % (13,2) | 69 (72) |
| 2026-07 | 67 | 54 (56) | 14 (15) | 20,9 % (22,4) | 25,9 % (26,8) | 54 (56) |
| 2026-08 | 42 | 73 (73) | 12 (12) | 28,6 % (28,6) | 16,4 % (16,4) | 82 (82) |
| 2026-01 | 54 | 81 (81) | 7 (7) | 13,0 % (13,0) | 8,6 % (8,6) | 81 (81) |

Parejas 40 (41): la que se va es la T0 de 2026-07-10 o4, una de las llenadas de Z (§2.8 c de
RECORRIDA). Llenadas 286 (291). Patrones (`patrones-diaria.txt`, total frente a RECORRIDA): T0 40
(41), P1 44 (44), P2 40 (40), P3 62 (60), P4 8 (8), P5 171 (173), P6 75 (77), P7 4 (5). La cuenta
diaria no congela: cada día empieza de cero.

**Herencia H7 (R4.2).** R4.2 cita cifras de la diaria de RECORRIDA (34 sesiones de P6, 77
llenadas, 259 / 149 / 110). Siguen siendo las de esa salida, que es la que se usó para la hoja de
la sesión 6; la diaria nueva tiene 75 filas P6 (77) y las 8 sesiones elegidas no cambian (§4.3). No
he recontado las 34 sesiones ni las 259 (exige `entradas_antes_alternancia.py`, que no se corre:
punto 5); las líneas del cierre no tocan R4.2.

## 5. El encargo, punto por punto

El encargo y las dos respuestas del consultor, partidos en requisitos (E = encargo; P = respuesta a
la PARADA; P2 = respuesta a la PARADA 2). Estados: Hecho / Hecho de otra forma (declarado) /
Parcial / No hecho.

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 1 | E0: base 0e021bf, merge 89dc902, tag F38i; la CI 40815230287 con `gh` | Hecho | Apertura (tabla) |
| 2 | E0: `abrir-rama`; encargo tal cual; contrato con R3 y riesgo alto; Archivo en HISTORIA | Hecho | 4036818 |
| 3 | E0: las rutas del contrato; nada más sin ampliarlo a la vista | Hecho | `contrato.yaml`; ACTIVAR-A35-A44 ampliado en 556452a; `contrato_rama.py` en verde |
| 4 | E1: QUÉ NO CAMBIA (spec, casos, `parametros.yaml`, `llenado.yaml`, motor, ADR-0051 §1/§4/§6, ADR-0057 §1, ninguna cifra) | Hecho | `git diff --name-status main...HEAD`: en `src/` solo `llenado.py` y `broker.py`; nada en `knowledge/` ni `config/` |
| 5 | E2 a): las lecturas del respaldo y los precios sin tick, con los dos casos de futuro y la diferencia de velas | Hecho | §0.a |
| 6 | E2 b): la deuda de cotizar | Hecho | §0.b |
| 7 | E2 c): el instante de la decisión, `ultimo_cambio_ms` y los tres «NO» | Hecho | §0.c |
| 8 | E2 d): ADR-0051 §3 frente a ADR-0057 §1 | Hecho | §0.d |
| 9 | E2 e): los eventos que no son llenadas | Hecho | §0.e |
| 10 | E2 f): la forma de la corrección y lo que sigue igual | Hecho (con prototipo de (a)) | §0.f |
| 11 | E2 g): los guiones | Hecho | §0.g |
| 12 | E2 h): la línea base | Hecho | §0.h |
| 13 | E2 i): recuentos y tiempos | Hecho | §0.i |
| 14 | E2 j): herencias | Hecho | §0.j |
| 15 | E2 k): la exposición de la fase 0 el mismo día, en su commit | Hecho de otra forma (declarado) | La fila del 2026-10-28 entró a las 00:37 del 29 (56b2233): desviación 7 |
| 16 | E2: PARADA con «Lo que necesito que decidas», numerada y con recomendación | Hecho | 56b2233 |
| 17 | P: respuesta tal cual en el encargo y el informe | Hecho | 556452a |
| 18 | P0: las dos cifras en el informe y en el cierre | Hecho | §4.4; `simular_cierre.py` (registro HECHA de Z) |
| 19 | P1: la forma (b), sin tocar `desde`, «ahora − 1», ticks, `_fin_ms` ni el instante | Hecho | §2.1; beb9c93 |
| 20 | P1: tests de `main` que la rozan, sin tocarlos | Hecho | `tests/` solo añade un fichero; 3038 passed |
| 21 | P1 y E3: tests 1-3 del encargo, el 4 (stop movido) y los dos de la modificación, que rompen en `main` | Hecho | §2.2 (8 FAILED en `main`, PASSED en la rama) |
| 22 | E3: los cuatro de f) en los dos lados | Hecho | §2.2 |
| 23 | E3: `comparar-con-main`, los dos lados pegados | Hecho | §2.2 |
| 24 | E3: docstring de `llenado.py` sin «PROPUESTO», con la regla del respaldo | Hecho | `llenado.py:1`, `:13-19` |
| 25 | P4 y E3: NOTAS de ADR-0051 §5 y §3 | Hecho | beb9c93 |
| 26 | P9: la NOTA dice que la repetición del trader sin ticks ya no se reproduce igual | Hecho | ADR-0051 §5, NOTA |
| 27 | P2: los dos casos de futuro no se arreglan; `_peor_del_minuto` a H con su sonda | Hecho | la sonda 5, en `anexos/RESPALDO-M1/sonda_z.py` (tras b2 del revisor); H en §6 |
| 28 | P3: la línea de Technical Debt de las cotizaciones, con su texto | Hecho (en las líneas del cierre) | §6 |
| 29 | P5 y P2-1: `censo_respaldo.py` por la condición general y `sesiones_s14.py` con las cuatro cosas | Hecho | §3, §4.3, §4.4 |
| 30 | P6: el contrato a ACTIVAR-A35-A44, solo para la NOTA de §5 | Hecho | 556452a; e808391 |
| 31 | P7 y E4: la fila de la fase 2 en su commit, antes de correr | Hecho | d380632, antes de las corridas |
| 32 | P8 y P2-2: la letra H con su grep; R3.6; R5.2 | Hecho | §1; §6 |
| 33 | P10 y P2-4: la variable comprobada y cómo; corridas en segundo plano sin ella delante | Hecho de otra forma (declarado) | §4.1: ya valía 1 y Aleks eligió no reiniciar |
| 34 | E4.1-3: las tres corridas, una a la vez; el nombre real de la diaria; la repetición con `diff` y borrada | Hecho | §4.2 |
| 35 | E4: criterio de hecho, Z = 0 en las dos | Hecho | §4.4 |
| 36 | E4: los demás eventos del respaldo, contados y explicados | Hecho | §4.4 |
| 37 | E4: qué cambia por corrida (veredicto, cobertura, precisión, parejas, llenadas, RN-032) | Hecho | §4.5 |
| 38 | E4 y P2-1: las 8 sesiones de S-14, sin R; PARADA si cambia algo | Hecho: no cambian | §4.3 |
| 39 | E4 y P6: NOTA de ADR-0070 §3 y de ACTIVAR-A35-A44 §5 | Hecho | e808391 |
| 40 | E5: el informe con fases, PARADAS, tests, corridas, exposiciones y desviaciones | Hecho | este fichero |
| 41 | E5: las líneas del cierre medidas sobre una copia, contra `test_hoja_de_ruta` | Hecho | §6 |
| 42 | E5: PROJECT_STATE por debajo de 25.000 y, si se puede, de 23.000 | Parcial | 23.968: por debajo del tope, no de la alerta (desviación 2) |
| 43 | E5, P y P2-3: la fila de ERRORES-RECURRENTES con los tres hallazgos del consultor | Hecho | §7 |
| 44 | E5: el revisor (opus) con los cinco alcances, pegado; lo que importe, arreglado | Hecho | §8 |
| 45 | E5: sin `fix/` (no toca hooks, rutas ni plataforma) | Hecho | `git diff --name-status`: nada en `.claude/`, `Makefile` ni scripts de plataforma |
| 46 | Siempre: `make check` antes de cada commit, con ruff y mypy; mensajes con Write y `-F` | Hecho | §5.3 |

**Desviaciones declaradas.**
1. La variable del punto 10 ya valía 1 y Aleks eligió no reiniciar (§4.1).
2. PROJECT_STATE con las líneas del cierre mide 23.968 bytes: por debajo del tope de 25.000, pero
   por encima de la alerta de 23.000. Los textos que lo suben (la entrada H y la línea de Technical
   Debt de las cotizaciones) son los que dictó el consultor; recortarlos sería cambiarlos (§6).
3. El punto 5 de la respuesta pedía comparar el lado contra el que dibujaba `graficos_sesion.py`, que
   no lo dibuja (PARADA 2, resuelta).
4. La suite entera no se pudo correr en el clon del prototipo de la fase 0 (guardia, §0.m); la corre
   cada `make check` de la rama.
5. El encargo citaba como precedente la fila a1 de recorrida-construccion; es la de
   `trabajo/activar-sesion-05` (auditor, 45).
6. Los dos errores de `mypy` de `patrones.py` y `horas_perdidas.py` al tipar las copias vienen de los
   originales de `anexos/RECORRIDA-CONSTRUCCION/` y `make check` no tipa esa carpeta; las copias son
   idénticas y no se tocan.
7. **La fila del 2026-10-28 de HOLDOUT-EXPOSICIONES no entró el mismo día** (hallazgo a1 del
   revisor). Declara el `make check` de la apertura y la primera lectura de las salidas de
   RECORRIDA, del 28 por la tarde y la noche (hora local), pero entró en 56b2233, a las 00:37 del 29
   (hora local; en UTC, las dos cosas son del 29). Se escribió en el árbol después de esas
   lecturas, durante la fase 0. No se reescribe: lo dice este punto, y §5.2 ya no afirma «todas
   antes».
8. **Dos lecturas de salidas de días dev quedaron sin fila hasta el revisor** (a2): `lado_caja1.py` y
   `llenadas_mes.py`, más las lecturas con `grep` de la fase 2. Ahora tienen su fila, del mismo día
   (2026-10-29).

### 5.1 Comandos ejecutados (literales, en orden; los de la fase 2 en §4.2)

1. Apertura: `git fetch origin`, `git rev-parse`, `git ls-remote`, `gh run view 40815230287 --json …`,
   `git checkout -b trabajo/respaldo-m1`, el Archivo 52 con `printf` y `git show main:PROJECT_STATE.md`.
2. Fase 0: `python -B <carpeta de trabajo>/censo_z.py <salida>` (×2), `uv run python -B …/sonda_z.py`,
   `…/recuentos.py .`, `…/tres_no.py .`, `…/be_vela.py .`, `…/censo_cierre.py <salida>` (×2),
   `…/letras.py .`, `…/parche_a.py C:/cm/z-proto` y los nueve ficheros de tests en ese clon.
3. Fase 1: `ruff format`, `ruff check`, `mypy` sobre lo tocado; los diez ficheros de tests en el repo;
   `comparar-con-main` (§2.2).
4. Antes de la fase 2: `…/lado_caja1.py docs/validation/anexos/RECORRIDA-CONSTRUCCION`; los guiones
   nuevos sobre las salidas de RECORRIDA.
5. Cierre simulado: `uv run python -B docs/validation/anexos/RESPALDO-M1/simular_cierre.py .`.
6. Un `make check > make-check.log 2>&1` antes de cada commit.

**Negativas de la guardia, sin rodear**: comandos compuestos con `python -` o con `git add` delante
de un `python`, `grep -r` sin ruta, `pytest` sobre un directorio o sin rutas en el clon, la variable
de entorno delante del comando, un `for` en Bash, `rev`, y PowerShell con una llamada a .NET. Cada
una se rehízo en la forma que propone la propia guardia, o se dejó (la suite en el clon, el registro
de Windows); ninguna bloqueó una medida necesaria.

### 5.2 Exposiciones

Las filas de HOLDOUT-EXPOSICIONES de la rama:
- 2026-10-28: la apertura y el comienzo de la fase 0. Se escribió después de esas lecturas y entró
  a las 00:37 del 29 (desviación 7).
- 2026-10-29: la fase 0, en su commit (56b2233).
- 2026-10-29: la fase 1, antes de su primer `make check` (beb9c93).
- 2026-10-29: la fase 2, en d380632, antes de correr; git lo fecha antes de las corridas, que
  usan 823404a.
- 2026-10-29: lo que las anteriores no nombraban, añadida tras el revisor (desviación 8).

Ninguna partición tocada; ningún libro, imagen, fotograma ni transcripción; ningún R de las
sesiones de S-14.

### 5.3 Los `make check` de la rama

| Commit | Árbol del `SELLO` | Duración | `PICO DE MEMORIA` |
|---|---|---|---|
| 4036818 (apertura) | 5ebeb8d4… | 1117 s | 300 MiB en `test` |
| 56b2233 (fase 0) | 2aaf46ed… | 1090 s | 300 MiB |
| 556452a (respuesta a la PARADA) | 94a2a4f8… | 1179 s | 300 MiB |
| beb9c93 (fase 1) | f9c33d73… | 1139 s (3038 passed) | 300 MiB |
| d380632 (anexos y fila de la fase 2) | 5cb071cc… | 1124 s | 300 MiB |
| 823404a (respuesta a la PARADA 2) | 239ede82… | 1065 s | 300 MiB |
| e808391 (fase 2) | 7617087e… | 1162 s (3038 passed) | 300 MiB |
| (el de la entrega) | §8.1 | | |

Todos: exit 0 y ningún `failed`, leídos en `make-check.log` antes de cada commit.

## 6. Las líneas del cierre (preparadas y medidas sobre una copia; no aplicadas en la rama)

`docs/validation/anexos/RESPALDO-M1/simular_cierre.py` las aplica en memoria sobre PROJECT_STATE,
la hoja de ruta y HISTORIA de la rama y corre `test_hoja_de_ruta` (a, b, c) y `test_project_state`:

```
letra H: viva en la copia simulada? True; HECHA en HISTORIA? True; NA:H en la hoja de main? False; Z viva en la copia? False; NA:Z en la hoja simulada? False
a: []
b: []
c: []
PROJECT_STATE con las lineas del cierre: 23968 bytes (wc -c de la copia: 23968); los cuatro tests de test_project_state: ok
```

Las líneas (literales en el guion):
- **Next Action**: sale Z, con su registro nuevo `# Next Action HECHA · Z · sale de PROJECT_STATE.md
  en trabajo/respaldo-m1 (<fecha>)` en HISTORIA (RITUAL, punto 3; el registro HECHA de Z de
  `cases-rejilla` es anterior, `DECISIONES-DE-PROCESO.md:29`), con las dos cifras del punto 0 (2
  llenadas y 0 stops en la corrida 1; 10 llenadas y 2 stops en la 2). Entra **H** en su sitio, con
  el texto del punto 8 tal cual. F termina en «R6a en los huecos.».
- **Technical Debt**: entra la línea de las cotizaciones sin tick del punto 3, tal cual.
- **Hoja de ruta**: R3.5 pierde `NA:Z` en Refs y gana su «Estado: HECHA» con la rama y el informe;
  entra **R3.6** con `NA:H · ID:ADR-0051 · ID:ADR-0057`, Depende de R3.5, y el «Hecho cuando» del
  punto 8; R5.2 nombra `NA:H, el sello del respaldo M1 (R3.6)` en lugar de `NA:Z`.
- **PROJECT_STATE**: 23.968 bytes con todas las líneas (tope 25.000; alerta 23.000: desviación 2).
  Los recuentos de «Tests Currently Passing» ya van en la rama (1777).

## 7. La fila de ERRORES-RECURRENTES (preparada para el cierre)

| Rama | El revisor | Lo que se aprende |
|---|---|---|
| `trabajo/respaldo-m1` | (§8) | (1) **(Del consultor)** El encargo escribió la condición de Z sin medir el borde ni leer ADR-0057 §1. Lección: una condición sobre instantes se escribe con el borde medido (qué vale exactamente en el instante de la decisión) y con todos los ADR que fijan ese borde. (2) **(Del consultor)** El primer borrador de la respuesta movía el sello del respaldo a k fin − 1 sin buscar los otros lectores de `abierta_ms` y del minuto del evento, con una regla que se contradecía. Lección: antes de proponer que se mueva un instante, se buscan con grep todos los que lo leen; y una regla que deja decidir a la sesión no puede contradecirse ni tocar lo que «QUÉ NO CAMBIA» protege. (3) **(Del consultor)** La respuesta pidió comparar «el lado que dibujó `graficos_sesion.py`» sin leer el script, que no lo dibuja. Lección: una comprobación contra un artefacto se escribe después de leer qué contiene. Señal: el artefacto se nombra pero no se cita su línea. (4) **Un prototipo en un clon antes de proponer la forma**: midió que los tests de `main` que el encargo no listaba (abrir a media vela) pasaban con (a), y así la PARADA llevó una medida y no una lectura. (5) **La versión anterior de un objeto también es una decisión**: excluir la vela del cambio dejaba sin evaluar el stop original (ADR-0065 §4); la condición correcta elige la versión vigente al inicio de la vela, no solo «después de la decisión». Señal: un objeto con historia (stop movido, orden modificada) y una regla que solo mira el último cambio. |

## 8. El revisor

Subagente `revisor` (opus), lanzado el 2026-10-29 sobre e808391 con el informe terminado y los
cinco alcances del encargo. Su informe, tal cual (ninguna cita de un tramo no citable: nada
retirado):

> ## Informe del revisor · trabajo/respaldo-m1 · 2026-10-29
>
> HEAD e808391, base 0e021bf (`git merge-base main HEAD` = 0e021bf9…). `git status --short` vacío. Siete commits, de 4036818 a e808391.
>
> Veredicto: nada bloquea. Hay 4 hallazgos que importan (2 en cada eje) y 5 menores. Los cinco alcances que pediste se cumplen, con un matiz en el 3: los relojes de las filas de exposiciones.
>
> ### Eje (a) · Reglas de la casa
> Resumen: 0 bloquea, 2 importa, 3 menor.
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | a1 | importa | La fila de exposiciones del 2026-10-28 se commiteó ya el 29 en hora local, y después de una de las lecturas que declara. Por eso §5.2 no se sostiene cuando dice «todas antes de la lectura que declaran». Esa fila declara el `make check` de la apertura y la lectura de las salidas de RECORRIDA del día 28. Pero no entra en 4036818, la apertura: entra en 56b2233. Es «el mismo día» solo si se escribió en el árbol antes de medianoche, y eso no se puede comprobar. En UTC, los dos commits caen el 29 (04:59Z y 05:37Z), así que la fecha de la fila tampoco cuadra en UTC. | `git log main..HEAD -- docs/validation/HOLDOUT-EXPOSICIONES.md` → 56b2233 `2026-10-29 00:37:40 -0500` (añade las filas del 10-28 y del 10-29 de la fase 0); 4036818 `2026-10-28 23:59:39 -0500`. `git show 56b2233 -- …HOLDOUT-EXPOSICIONES.md \| grep '^+\|'` → `+\| 2026-10-28 \| **Rama trabajo/respaldo-m1 … apertura y comienzo de la fase 0.**`. RESPALDO-M1.md:841-842 («todas antes de la lectura que declaran: 2026-10-28 (apertura y comienzo de la fase 0)…») |
> | a2 | importa | `lado_caja1.py` leyó `entradas-antes-alternancia.txt` y la diaria de RECORRIDA el 2026-10-29, y ninguna fila lo declara. La fila de la fase 0 del 10-29 solo nombra `censo_cierre.py` sobre «las dos salidas» (cuenta-arrastrada y diaria). La de la fase 2 solo nombra los guiones de `anexos/RESPALDO-M1/`, y `lado_caja1.py` es de la carpeta de trabajo. No es holdout: son salidas de días dev. Pero CLAUDE.md pide declarar el mismo día también el material de desarrollo. | RESPALDO-M1.md:647-650 («`lado_caja1.py`, guion de la carpeta de trabajo que solo lee esos dos ficheros»); Grep `lado_caja1` en HOLDOUT-EXPOSICIONES.md → sin coincidencias; la fila de la fase 0 (HOLDOUT-EXPOSICIONES.md:83) dice «`censo_cierre.py`, las dos salidas de (2) de la fila anterior» |
> | a3 | menor | El docstring de un test no coincide con su código: dice 990 y el código modifica a 995. | tests/unit/test_respaldo_m1_decision.py:143 («se modifica a 990») y :145 («se evalua con 990»), frente a :154 `precio=995` |
> | a4 | menor | El censo no sale con 3, como dicen su docstring y el README: sale con 1. `SystemExit` con una cadena da código 1. | censo_respaldo.py:12-13 («el guion sale con 3») y :96-99 `raise SystemExit(f"…")`; README.md:46 («sale con 3») |
> | a5 | menor | Un docstring cita una línea que ya no es: el «ahora - 1» está ahora en broker.py:759-760, no en :743-744. | test_respaldo_m1_decision.py:199; broker.py:759-760 en la rama |
>
> Comprobado sin hallazgos:
> - **Contrato.** `uv run python -B scripts/contrato_rama.py` dice: `CONTRATO: 25 ficheros dentro del contrato de trabajo/respaldo-m1 (riesgo alto, artefacto docs/validation/RESPALDO-M1.md, tramo 'R3', 2 comprobaciones para el revisor)`, exit 0.
> - **Comprobación 1 del contrato.** `uv run python -B -m pytest tests/unit/test_llenado.py tests/unit/test_broker.py tests/unit/test_broker_ordenes_stop.py tests/unit/test_respaldo_m1_decision.py tests/unit/test_be_al_tick.py tests/unit/test_instante_llenado.py tests/unit/test_caja_hasta_el_llenado.py -p no:cacheprovider` → `64 passed in 43.69s`.
> - **Comprobación 2 (`make check`).** No la ejecuté. `make-check.log`: `3038 passed in 1072.61s`, `SELLO: make check en verde sobre el arbol 7617087e…`, que es el `HEAD^{tree}` de e808391, y `PICO DE MEMORIA de make check: 300 MiB en test`. Ningún `failed` ni `error`.
> - **Trailers `Fuente:`.** Ningún commit toca `knowledge/spec/` ni `knowledge/cases/`, así que no hacen falta.
> - **Holdout.** Nada en `knowledge/cases/holdout/`. Ningún libro, imagen ni fotograma.
> - **Fechas en los anexos.** En las salidas de la rama solo hay los 76 días dev (21+21+13+21), más dos fechas del calendario de cierres (2025-12-04 y 2026-10-08, que no son mercado). Ningún desfase `+01:00` o `+02:00`, y ninguna hora `T00`-`T03`.
> - **Ningún R de S-14.** `sesiones-s14.txt` solo trae id, colocada, precio, punto y lado.
> - **Régimen de cambio.** `git diff --name-status`: nada en `knowledge/`, `data/manifests/`, `config/`, `.claude/`, el Makefile ni `anexos/RECORRIDA-CONSTRUCCION/`. `tests/` solo añade `test_respaldo_m1_decision.py`. HISTORIA, HOLDOUT-EXPOSICIONES, ADR-0051, ADR-0070 y ACTIVAR-A35-A44 solo añaden líneas (numstat con 0 borradas).
> - **Ambigüedades.** Ninguna tocada.
> - **ADR.** El `## Estado` de ADR-0051 y de ADR-0070 sigue en `ACTIVE`.
> - **Informes cerrados.** Ninguno cambia.
> - **Citas en la spec y evidencia nueva.** Ningún sitio nuevo con `cita` y ningún item nuevo de evidencia.
> - **Citas del informe, comprobadas contra su fuente.**
>   - ADR-0057:26-27, «la misma que la límite (la salida se mira desde la vela siguiente)»: sí.
>   - graficos_sesion.py:98-101, `Orden` solo con `colocada` y `punto`: sí.
>   - DECISIONES-DE-PROCESO.md:29, la regla de letras: sí. Además, H tiene un único registro HECHA (HISTORIA:12855) y ningún `NA:H` en la hoja.
>   - El 13,7 % y «ninguna de las dos es pareja»: RECORRIDA-CONSTRUCCION.md:960-961.
>   - Saldo 90652.93 y o1 por ticks a las 06:00:03.566 a 1.17297: cuenta-arrastrada.txt:605, :697 y :798.
> - **Copias de guiones.** `patrones.py` y `horas_perdidas.py` tienen el mismo sha256 que los de RECORRIDA (330b7d62… y dfa782a3…).
>
> Alcances del encargo:
> - **Alcance 1: los 8 tests rompen en main por la causa de Z.** Lo he razonado sobre el código de main, que se ve en el contexto del diff: `_fin_ms(vela) <= desde_ms` sin `decidido`, y `desde = max(ahora-1, ultimo_cambio_ms)`.
>   - Tests 1-3: la vela M0, colocada en `_cierre(M0)`, entra entera. 1894694460000 es el fin de M0 y 1894694480000 es M0+1 a los 20 s, las cifras de la salida pegada.
>   - Test 4: el stop movido a 1000 se evalúa contra M0, cuya mínima es 1000 (`assert (False)`).
>   - Test 5: sale a 1000 y no a 990.
>   - Tests 6-7: la vela de la modificación se evalúa con la versión nueva.
>   - Test 8: sin `decidido`, el `desde` a media vela cuenta.
>   - Ninguno rompe por otra causa (rechazo, freno o firma): las funciones de main aceptan los 6 argumentos posicionales y `modificar` y `mover_stop` existen con la misma firma.
> - **Alcance 2: la condición se aplica en toda lectura del respaldo.**
>   - Solo `broker._proximo_evento` llama a las tres funciones del respaldo (Grep en `src/` y en `scripts/`), y les pasa siempre el instante del objeto (broker.py:767-772 y :783-795). Las llamadas sin él toman `decidido = desde_ms` (llenado.py:169, :219 y :299), así que se niega por defecto.
>   - Las otras cuatro lecturas del inventario (`cotizacion`, `_precio_de_mercado`, `precio_de_conversion` y `_peor_del_minuto`) no se tocan, como decidió la PARADA (puntos 2 y 3).
>   - Lo que va por ticks, `desde`, el «ahora - 1», `_fin_ms` y el instante del evento no cambian en el diff.
>   - ADR-0057 §1 se mantiene: `abierta_ms` es el inicio de la vela siguiente y `>=` la cuenta. Lo fijan el test 11 y los de main.
> - **Alcance 2: la restauración frente a ADR-0065 §4.** No encontré ningún defecto.
>   - La regla de `_nivel_de_la_vela` (inicio ≥ decidido) y la de `_de_la_version_anterior` (minuto·60000 < cambio) son la misma, negada.
>   - La orden se restaura antes de la comprobación de margen (broker.py:846-849, antes de :850).
>   - El stop vuelve al anterior y `stop_original` pasa a `None` solo si el anterior era el de nacimiento (:890-892). Con dos movimientos, se conserva como break even.
>   - La traza conserva el `stop_movido` y su petición, y el informe lo declara (§2.1).
> - **Alcance 4: las NOTAS solo añaden** (diff -U2 de los tres ficheros).
> - **Alcance 5: las líneas del cierre pasan.** `uv run python -B docs/validation/anexos/RESPALDO-M1/simular_cierre.py .` → `a: [] b: [] c: []`, `23968 bytes … los cuatro tests de test_project_state: ok`, exit 0. La deuda de cotizar está en las líneas del cierre (`DEUDA`, simular_cierre.py:77-85), letra a letra igual al punto 3 de la respuesta. El texto de H es letra a letra el del punto 8.
>
> ### Eje (b) · Encargo
> Resumen: 0 bloquea, 2 importa, 2 menor. Requisitos (46): 41 hechos, 1 hecho de otra forma y declarado, 2 parciales, 1 no hecho y 1 pendiente (el revisor, que es este informe).
>
> | # | Requisito | Estado | Evidencia |
> |---|---|---|---|
> | 1 | Base 0e021bf y CI 40815230287 verificadas con gh | Hecho | RESPALDO-M1.md:9-15 |
> | 2 | Encargo tal cual, contrato con R3 y riesgo alto, Archivo en HISTORIA | Hecho | contrato.yaml:2-4; HISTORIA +166/-0 |
> | 3 | Rutas del contrato; ACTIVAR-A35-A44 ampliado a la vista | Hecho | contrato.yaml:14; 556452a; contrato_rama.py exit 0 |
> | 4 | QUÉ NO CAMBIA (spec, casos, parámetros, llenado.yaml, motor, ADR-0051 §1/§4/§6, ADR-0057 §1) | Hecho | name-status: solo llenado.py y broker.py en `src/`; ADR-0051 solo NOTAs en §3 y §5 |
> | 5-14 | Fase 0, a) a j) | Hecho | §0.a-§0.j (RESPALDO-M1.md:31-294) |
> | 15 | k) La lectura de la fase 0 se declara el mismo día, en el commit de la fase 0 | Parcial | La fila del 10-28 entra el 29 a las 00:37 local (56b2233). Ver a1 en el eje (a) |
> | 16 | PARADA con «Lo que necesito que decidas», numerada y con recomendación | Hecho | RESPALDO-M1.md:366-438 |
> | 17 | Respuestas de las PARADAS 1 y 2 tal cual, en el encargo y en el informe | Hecho | `diff <(sed -n '128,182p' encargo) <(sed -n '444,498p' informe)` vacío; las de la PARADA 2 también |
> | 18 | Tests 1-3 del encargo: rompen en main y pasan en la rama | Hecho | test_respaldo_m1_decision.py:79-105; §2.2 |
> | 19 | Test 4 (e) | Hecho | :108-119 |
> | 20 | Tests de la PARADA: el stop original sin break even, la modificación con su precio anterior | Hecho | :122-173 |
> | 21 | Los cuatro puntos de f) pasan en los dos lados; tests de main sin tocar | Hecho | :189-242; `git diff --name-status main...HEAD -- tests/` = solo `A test_respaldo_m1_decision.py`; 3038 passed |
> | 22 | `comparar-con-main`, los dos lados pegados | Hecho | RESPALDO-M1.md:584-617 |
> | 23 | Docstring de llenado.py, sin «PROPUESTO» | Hecho | llenado.py:1 y :15-19 |
> | 24 | NOTAs de ADR-0051 §3 y §5; la repetición del trader (punto 9) | Hecho | diff de ADR-0051 |
> | 25 | La fila de la fase 2 en su commit, antes de correr | Hecho | d380632 (10:49), antes de las corridas sobre 823404a (11:36) |
> | 26 | Corridas una a una, en segundo plano, con la variable | Hecho de otra forma, declarado | §4.1; desviación 1 |
> | 27 | El nombre real del fichero de la diaria | Hecho | §4.2, fila 2 |
> | 28 | Guiones de g) con las condiciones del punto 5 | Hecho | censo_respaldo.py:106-122; sesiones_s14.py:45-99 |
> | 29 | Criterio de hecho Z = 0 en las dos corridas | Hecho | censo-respaldo.txt:2 y :13 |
> | 30 | Qué cambia por corrida (veredicto, cobertura, precisión, parejas, llenadas, RN-032) | Hecho | §4.5 |
> | 31 | Las 8 sesiones de S-14, sin R | Hecho | sesiones-s14.txt:11 («0») |
> | 32 | NOTA de ADR-0070 §3 y de ACTIVAR §5 | Hecho | diff |
> | 33 | Informe con fases, comandos, tiempos y picos | Hecho, con el menor b4 | §2-§5 |
> | 34 | Z sale, con su registro HECHA y las dos cifras | Hecho | simular_cierre.py:66-75 |
> | 35 | F termina en «R6a en los huecos.» | Hecho | :76 |
> | 36 | R3.5 con «Estado: HECHA» | Hecho, con el menor b3 | :107-115 |
> | 37 | R5.2 nombra la letra nueva (PARADA, punto 8) | Hecho | :116-120 |
> | 38 | Deuda de cotizar en Technical Debt, con su texto | Hecho | :77-85 |
> | 39 | Letra H, R3.6 y el grep | Hecho | §1 (RESPALDO-M1.md:516-536); :93-106 |
> | 40 | `_peor_del_minuto` en H, «con su sonda 5 y con la del auditor» (PARADA, punto 2) | Parcial | Ver b2 |
> | 41 | PROJECT_STATE medido con wc -c | Hecho | 23968 bytes; la alerta de 23.000, declarada (desviación 2) |
> | 42 | La copia pasa test_hoja_de_ruta | Hecho | lo ejecuté |
> | 43 | Fila de ERRORES-RECURRENTES con los 3 hallazgos del consultor | Hecho | §7 |
> | 44 | El revisor, pegado al final del informe | Pendiente | §8 «Pendiente.» (es este informe) |
> | 45 | «El encargo, punto por punto» (E5) | No hecho | Ver b1 |
> | 46 | No toca hooks, rutas ni plataforma | Hecho | name-status |
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | b1 | importa | Falta la tabla «El encargo, punto por punto» que pide la skill. La §5 «El encargo frente a lo hecho» va por bloques, sin requisitos numerados ni los estados Parcial / No hecho / Hecho de otra forma, y no parte las respuestas del consultor. | RESPALDO-M1.md:786-802; .claude/skills/entregar-rama/SKILL.md:46-50 y :97 |
> | b2 | importa | El punto 2 de la PARADA pide que `_peor_del_minuto` vaya a H «con su sonda 5 y con la del auditor». En el repo no quedan las sondas: `sonda_z.py` está fuera, en la carpeta de trabajo. La sonda 5 solo está descrita en §0.a, fila 7. La del auditor no aparece en el informe fuera de la respuesta citada. El informe no lo declara como desviación. | RESPALDO-M1.md:24-27 y :49; simular_cierre.py:93-100 (R3.6 remite a «§0.a y §0.l»); Grep «instante redondo» en el informe: solo en la cita (:468 y :484) |
> | b3 | menor | El «Estado: HECHA» de R3.5 dice «el tag de su cierre» y no el tag, que las demás entradas HECHA sí nombran. El tag previsto es `stable/F38j-respaldo-m1`. | simular_cierre.py:111; HOJA-DE-RUTA.md:30, :40 y :77 |
> | b4 | menor | Los «comandos literales» no lo son del todo: §4.2, filas 3-7, y §5.1 llevan marcadores y «…». Y faltan el SELLO y el pico de los `make check` de d380632, 823404a y e808391 (el log solo cubre e808391). | RESPALDO-M1.md:696-700, :821-831, :17-19 y :621-624 |
>
> ### Lo que no pude comprobar
> - Si las filas del 10-28, de la fase 0 y de la fase 1 se escribieron en el árbol antes de sus lecturas. Git solo da la hora del commit: las de la fase 0 y la fase 1 entran en el mismo commit que cierra la lectura.
> - El lado de main de los 8 tests, ejecutado de verdad. Hace falta `git worktree add`, que escribe, así que lo sustituyo por la lectura del código de main y por la salida que pega §2.2.
> - `test_simulacion.py`, `test_cableado.py` y `tests/regression/test_cuenta_7_de_agosto.py` en mi sesión: leen `data/` de agosto y no lo declaré. Su evidencia es el `make check` sellado sobre HEAD (3038 passed).
> - `make check` (escribe) y el sello de los commits intermedios.
> - La sonda del auditor del consultor y los guiones de la carpeta de trabajo (`sonda_z.py`, `tres_no.py`, `be_vela.py`, `lado_caja1.py`, `letras.py`): no están en el repo.
> - El contenido de `cuenta-arrastrada.txt` y de la diaria, más allá de fechas, horas y las líneas citadas.
>
> ### Comandos ejecutados
> 1. `git branch --show-current && git merge-base main HEAD && git log --format='%h %ad %s' --date=iso main..HEAD && git diff --stat main...HEAD && git status --short`
> 2. Read: el encargo, `contrato.yaml`, RESPALDO-M1.md (entero), test_respaldo_m1_decision.py, llenado.py:270-349, broker.py:560-904, censo_respaldo.py, sesiones_s14.py, simular_cierre.py, el README de los anexos, sesiones-s14.txt, censo-respaldo.txt, ADR-0070:84-101, graficos_sesion.py:94-103, DECISIONES-DE-PROCESO.md:26-31
> 3. `git diff main...HEAD -- src/`
> 4. `git diff --name-status main...HEAD` y lo mismo sobre las rutas protegidas
> 5. Grep de llamadores y campos en `src/` y en `scripts/`; Grep de `m1_entre`
> 6. `uv run python -B scripts/contrato_rama.py`
> 7. `uv run python -B -m pytest …` (dos veces, con `-p no:cacheprovider`)
> 8. `grep` de SELLO, PICO, passed y failed en make-check.log; `git rev-parse HEAD^{tree}`
> 9. `git log … -- HOLDOUT-EXPOSICIONES.md`; `git diff main...HEAD -- HOLDOUT-EXPOSICIONES.md`; `git show {56b2233,beb9c93,d380632} -- HOLDOUT-EXPOSICIONES.md | grep '^+|'` (el `for` lo negó la guardia; lo partí en tres llamadas, como ella propone)
> 10. Grep de fechas fuera de los días dev en los anexos; `grep -ohE` de fechas por mes; `grep` de `+0[12]:00` y de las horas `T0[0-3]`
> 11. `git diff main...HEAD --numstat` y `-U2` de los ADR y de ACTIVAR; `git diff … -- PROJECT_STATE.md`
> 12. Grep de los nombres de test, del `## Estado` de los ADR, de ADR-0065 §4, de la cita de ADR-0057, del 13,7 % en RECORRIDA, de H en HISTORIA y en la hoja, de «punto por punto» en la skill, de «Estado: HECHA» en la hoja, de `lado_caja1` en HOLDOUT-EXPOSICIONES y de los datos de cuenta-arrastrada
> 13. `diff <(sed -n …) <(sed -n …)` de las dos respuestas del consultor
> 14. `sha256sum` de las copias de los guiones
> 15. `git show --stat d380632` y `e808391`; `git show e808391 -- censo_respaldo.py`
> 16. `uv run python -B docs/validation/anexos/RESPALDO-M1/simular_cierre.py .`

### 8.1 Lo que se hizo con los hallazgos del revisor

| # | Gravedad | Qué se hizo |
|---|---|---|
| a1 | importa | **Declarado, no reescrito**: desviación 7 de §5; §5.2 ya no dice «todas antes». La fila no se edita (HOLDOUT-EXPOSICIONES solo admite filas nuevas en esta rama); la lectura que declara es de material de desarrollo, sin días reservados. |
| a2 | importa | **Arreglado**: fila nueva del 2026-10-29 en HOLDOUT-EXPOSICIONES que nombra `lado_caja1.py`, `llenadas_mes.py`, las lecturas con `grep` de la fase 2 y las del revisor; desviación 8. |
| a3 | menor | **Arreglado**: el docstring dice 995 (`test_respaldo_m1_decision.py:143` y `:145`). |
| a4 | menor | **Arreglado**: `censo_respaldo.py` imprime el motivo por stderr y sale con 3. Vuelto a correr: `censo-respaldo.txt`, sin cambios (`diff` vacío). |
| a5 | menor | **Arreglado**: cita `broker.py:759-760`. |
| b1 | importa | **Arreglado**: §5 es ahora «El encargo, punto por punto», con 46 requisitos numerados (encargo y las dos respuestas) y sus estados. |
| b2 | importa | **Arreglado**: `anexos/RESPALDO-M1/sonda_z.py` entra en la rama, con las seis sondas, la 5 entre ellas (la de `_peor_del_minuto`). Corrida con el código de la rama: las 1 a 3 ya no llenan con la vela de su decisión, y la 3 sale por el stop original (990); las 4 a 6 dan lo mismo que en §0.a. La sonda del auditor del consultor no está en el repo, es del consultor: la entrada H (texto del punto 8, tal cual) no la nombra, y la rama de H la tendrá que pedir. Requisito 27 de §5. |
| b3 | menor | **Arreglado**: R3.5 nombra `stable/F38j-respaldo-m1` en `simular_cierre.py`; la simulación vuelve a dar `a: [] b: [] c: []` y 23.968 bytes. |
| b4 | menor | **Arreglado**: §4.2 lleva los comandos literales, con rutas enteras; §5.3, el `SELLO` y el pico de cada `make check` de la rama. §5.1 sigue resumiendo la fase 0 con «…» en las rutas de la carpeta de trabajo, que es temporal y no está en el repo. |

El `make check` de este último commit: en su mensaje.

## Estado

Hecho, con las desviaciones declaradas en §5. La corrección de Z está en `llenado.py` y
`broker.py`, con 12 tests (8 rompen en `main`). Las dos corridas, repetidas, dan Z = 0, y la que
cuenta sigue en «no». Las líneas del cierre están preparadas y simuladas (§6), y la fila de
ERRORES-RECURRENTES, preparada (§7). Sin CI de Linux: la rama no toca hooks, rutas ni plataforma.

Rama lista para revisión, NO cerrada.

## Orden de cierre del consultor (2026-10-29)

Copiada tal cual:

> Modelo: Opus 5.5 · Esfuerzo: medio
>
> Orden de cierre de trabajo/respaldo-m1 (consultor, 2026-10-29), tras revisar RESPALDO-M1.md entero. Cópiala tal cual al final del informe, en «Orden de cierre del consultor (2026-10-29)», en un commit antes del ritual. Después cierra con la skill cerrar-rama cuando Aleks escriba /cerrar-rama trabajo/respaldo-m1.
>
> 1. Tag: stable/F38j-respaldo-m1. Comprueba antes que no existe ni en local ni en origin. Mensaje del merge: «merge: trabajo/respaldo-m1, el respaldo M1 no evalúa contra precios anteriores a la decisión (Z)».
>
> 2. Hallazgos del consultor que el revisor no vio: ninguno que bloquee ni importe. Una observación para el informe, sin cambio en la rama. En la corrida que cuenta, el bot no tiene ninguna operación puntuable en abril, julio ni agosto, porque RN-032 congela la cuenta arrastrada desde el 2026-01-20 (§4.5). Así, su precisión es solo de enero, y su cobertura no tiene ninguna pareja fuera de enero. Va a la entrada nueva del punto 4.c.
>
> 3. La fila de ERRORES-RECURRENTES, la de §7, con el revisor de §8 (0 bloquea, 4 importan, 5 menores). Corrige una frase: de los tres hallazgos del consultor, los dos primeros los cazó su auditor antes de llegar a la sesión, y el tercero (el lado que no dibuja graficos_sesion.py) lo encontró la sesión en la PARADA 2. Lección para el revisor: ninguna nueva.
>
> 4. En el commit del contrato, además de lo de §6 (sale Z con su registro HECHA nuevo, entra H, R3.5 HECHA, R3.6 nueva, R5.2 con NA:H y la línea de cotizar en Technical Debt), estos cambios. En PROJECT_STATE, todo corto; el detalle va a la hoja de ruta:
>
>    a) F, entera: «F. La sesión 6 con el trader (R4.2), el martes 2026-11-03: la hoja es docs/sesion-6/PREGUNTAS.md y el PDF del consultor, y los gráficos de S-14 están fuera del repo; después, su ingesta. R6a en los huecos.» En R4.2 de la hoja de ruta, una frase: los gráficos de S-14 siguen valiendo con el bróker corregido (RESPALDO-M1.md §4.3).
>
>    b) A, en PROJECT_STATE: solo cambian dos frases y lo demás se queda tal cual (lo que miden las ejecuciones, el calendario de noticias opcional).
>       - «la 2 entre el 26 y el 30 de octubre, con el script 1.1 compilado antes; la 3 después del 1 de noviembre.» pasa a: «la 2, hecha el 2026-10-29 (script 1.1; CSV en data/demo_ftmo/ sin congelar, el original sigue en MQL5\Files); la 3, del 2026-11-02 al 2026-11-06.»
>       - «La ejecución 2 comprueba la fórmula del margen con `MargenAlcanza` (FTMO-P-D1.md §3), y la 3 mide cuándo comprueba MT5 el margen de una pendiente stop (ADR-0081 §4).» pasa a: «En la 2, el margen de 1,00 lote cuadra con FTMO-P-D1.md §3. Cuándo comprueba MT5 el margen de una pendiente stop (ADR-0081 §4) pide un script 1.2, que aún no existe: una rama corta antes de la 3; si no llega, esa medida pasa a la siguiente prueba.»
>       Antes, verifica en el CSV las cifras:
>       - con el lector, desfase 180 y comisión de 2,50 por lado con 1,00 lote, en valor absoluto (DEAL_COMMISSION sale negativa);
>       - el margen, en la nota de la fila volumen_comision (3720,77), con el ask de la fila apertura_compra_mercado, porque la fila volumen_comision no trae precios: 100.000 × ask / 30.
>       Si la guardia de K (exigir_sin_crudo) niega el lector, PARADA y lo lanza Aleks con «!».
>
>    c) En la hoja de ruta:
>       - A.1: el «Depende de» pasa a «la prueba nueva de FTMO del 2026-10-29». El «Qué es» gana la ejecución 2 hecha, con sus tres cifras (desfase 180; comisión 2,50 por lado; margen 3720,77 con el ask de la apertura, que cuadra con FTMO-P-D1 §3), y el script 1.2 que falta para el instante del margen de una pendiente stop.
>       - R6a.6: «Depende de» nombra el script 1.2 y la ejecución 3.
>       - «Fechas fijas»: sale la línea de la prueba del 2026-10-08. La de la ejecución 2 pasa a: «La ejecución 2, hecha el 2026-10-29 en la prueba creada ese día; la 3, del 2 al 6 de noviembre de 2026 (NA:A).» Y entra: «La sesión 6 con el trader, el martes 3 de noviembre de 2026 (NA:F).»
>
>    d) Entrada NUEVA de la Next Action con la letra R. La regla de DECISIONES-DE-PROCESO.md (2026-10-27) deja R, V y Z, y el precedente de la rama es el orden alfabético; compruébalo con el grep y dilo. En una sola línea, corta:
>       «R. Decisión de Aleks (2026-10-29): fidelidad por criterios, además de por operación, y rentabilidad pre-registrada como puerta para operar en vivo. Rama de método con ADR (enmienda ADR-0043 y ADR-0070) y medida de los sesgos de la cifra de fidelidad, antes de la próxima corrida que cuente (R3.7).»
>
>    e) Hoja de ruta, entrada nueva «R3.7 · Método: rentabilidad como puerta, fidelidad por criterios y los sesgos de la cifra», con estos campos:
>       - Refs: NA:R · ID:ADR-0043 · ID:ADR-0070 · ID:A-16 · F:F27.
>       - Qué es: «Decisión de Aleks del 2026-10-29. La fidelidad se mide por CRITERIOS (la misma liquidez de M15, la misma caja, el mismo punto y la misma entrada, pieza a pieza) además de por operación entera, y la RENTABILIDAD pasa a ser la puerta para operar en vivo, con su criterio pre-registrado: esperanza después de comisión y deslizamiento, drawdown dentro de los límites de FTMO, diario y total, medida una sola vez sobre meses que el bot no ha visto. La fidelidad sigue siendo la herramienta de construcción. Una rama de método con su ADR, que enmienda ADR-0043 y ADR-0070 y declara lo ya visto (las corridas de RECORRIDA-CONSTRUCCION y RESPALDO-M1); su fase 0 revisa también la NOTA de MASTER_PLAN §0 (F26 antes de todo lo que opera en vivo) y F35. Y una medida de los sesgos de la cifra: (1) Oanda frente a Dukascopy contra la tolerancia de 3 puntos (A-16, adelantada desde F26: R5.1 lo dice); (2) el camino de la cuenta: la corrida que cuenta no puntúa ninguna operación del bot en abril, julio ni agosto porque RN-032 congela la cuenta desde el 2026-01-20 (RESPALDO-M1.md §4.5); (3) el material sin vídeo, donde el trader se saltaba las sesiones que iban a break even (S-14 de la sesión 5); (4) las tolerancias de entrada e instante. Los umbrales los fija el consultor en la PARADA de esa rama, antes de ver ninguna corrida nueva.»
>       - Depende de: la activación de la sesión 6 (R4.2).
>       - Quién: la sesión, con el encargo del consultor.
>       - Hecho cuando: el ADR está aceptado con los umbrales pre-registrados y la medida de los cuatro sesgos tiene su informe.
>       En R5.1, una frase: A-16 se mide antes, en R3.7. Y R5.2 nombra también NA:R en «Depende de».
>
>    f) El tamaño. Mide PROJECT_STATE con wc -c sobre la copia con TODAS las líneas (las de §6 y estas). Si pasa de 24.700 bytes, PARADA antes del commit, con la medida y tu propuesta de qué pasa a la hoja de ruta o a HISTORIA. Pasa test_hoja_de_ruta y test_project_state sobre la copia antes del commit.
>
> 5. El ritual, como manda RITUAL.md con la skill cerrar-rama:
>    - merge y tag;
>    - commit de estado, que solo cambia Current Branch, Current Feature, Stable Main State y Last Stable Commit;
>    - make check sellado;
>    - push atómico de main y el tag; Aleks confirma la regla ask con «1. Yes»;
>    - CI de main en verde antes de borrar nada;
>    - y borrar la rama local.
>    Sin --no-verify, sin push --force y sin consultar la CI con un guion ni con un bucle.
>
> 6. Informe final: sha de main, tag, run de la CI de main, ramas que quedan, tamaño de PROJECT_STATE y la letra usada en 4.d.
