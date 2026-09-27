# Preparación de A-21: RN-011 (la geometría de la zona de entrada) lista para activarse con la respuesta del trader

Rama `trabajo/preparar-a21`, 2026-09-26, sesión autónoma sobre `main` en
`stable/F25-preparar-a35-a44`. Sin merge, sin tag y sin push: el cierre lo decide Aleks tras la
revisión del consultor. Ningún ADR nuevo: el mecanismo no decide nada; deja construida la geometría
que el corpus SÍ documenta y deja escrito, con opciones cerradas y sin valor, lo único que no
documenta: qué hace «limpia» a una zona de control.

Guardas, verificadas al empezar y al terminar: `PREREGISTRO.md` con blob `52649183…` y sin
rellenar; cero autorizaciones en `knowledge/cases/holdout/`; nada de septiembre, mayo, marzo ni
febrero (la compuerta de construcción se niega antes de leer, también con `--diagnostico-*`, con
test); ninguna fecha de día reservado o retirado en ningún fichero commiteado; ningún
`--no-verify`; un commit sellado por paso.

**La misma contradicción entre el brief y el código que en la rama anterior, resuelta igual y al
mínimo.** El brief dice «en PROJECT_STATE solo lo que exige state check»; `state check` exige la
RAMA ACTUAL y el RECUENTO de funciones de test, y sin ellos `make check` no sella. Se tocaron esas
dos cosas y nada más; lo narrativo queda para el cierre.

## 1. Lo que el corpus documenta de la geometría, dimensión por dimensión

Cada dimensión de la zona de entrada, con su lectura documentada y su fuente. Donde hay UNA lectura
consistente, el mecanismo la lleva fija y visible; donde hay MÁS DE UNA, es un selector; donde no
hay ninguna, es candidato (§5) y el mecanismo la deja fija diciendo que la eligió él.

| dimensión | lectura(s) documentada(s) | fuente | en el mecanismo |
|---|---|---|---|
| **temporalidad** | la entrada se desarrolla en M1, encima de la liquidez de M15 tomada | `ev-v3-001630-a911f624` («la entrada correcta se desarrolla por encima de la liquidez con un flujo de órdenes en M1»), `ev-v2-001329-e766675a`, `ev-v3-010431-20bddf07` | fija: M1 (`domain/estructura_m1.py`) |
| **qué marca el breaker (BOS)** | el bloque de origen lo definen el BOS y el breaker; el trader no usa el CHoCH; dos esquemas | `ev-v3-011653-38c712f3` | fija: la referencia es el último pivote de M1 contrario a la entrada (el último ALTO de M1 para una compra), y el breaker es la primera M1 que lo pasa |
| **criterio de ruptura del breaker** | con MECHA | `breaker_m1_criterio_ruptura` (CONFIRMED, mecha; `docs/validation/BREAKER-M1.md`), `ev-v4-010415-6d8b1d02`, `ev-v4-005910-d24c0345` | fija por el registro: el productor lee el parámetro |
| **qué vela es el bloque de origen** | la última vela contraria al impulso antes de la ruptura («una vela contraria marca el punto del mapeo») | `ev-v3-010818-010bd2b3`, `ev-v3-011540-5425b533` | fija: la última contraria (`bloque_de_origen`) |
| **agrupar varias contrarias como una** | lo que en una temporalidad mayor es una vela (un «order block») cuenta como una | `ev-v3-010648-0039e34d`; A-8 RESUELTA con `mapeo_dos_velas = order_block_mayor` (CONFIRMED) | **NO**: `agrupar_estructura` (RN-007) sigue NO_IMPLEMENTADA porque el valor no trae criterio ejecutable (§5, candidato 1); el bloque es UNA vela |
| **extremos de la zona: mecha o cuerpo** | con las MECHAS: «el mapeo en M1 considera las mechas y parte del punto más bajo»; la orden «siempre en la mecha» | `ev-v3-010500-f3a1bebc`, `ev-v3-001827-72bc1e81`, `ev-v4-010605-a11249c0` | fija: la zona va del extremo cercano al lejano de la vela, mechas incluidas |
| **dónde va la orden dentro de la zona** | en el borde cercano (la mecha más próxima al precio), y el stop sale del extremo lejano («desde el punto más bajo donde se genera la vela contraria»; el lote «de máximo a mínimo») | `ev-v4-010605-a11249c0`, `ev-v1-001454-69cebe62`, `ev-v3-004353-b7661782` | fija: `entrada` = borde cercano, `extremo` = borde lejano; el punto EXACTO dentro de la mecha es A-36 (abierta) |
| **los dos esquemas** | primer esquema: rompe directo, sin retroceso («con el breaker ya me basta»); segundo: pequeño retroceso con UNA zona de control y luego rompe | `ev-v4-000243-5f8875ce`, `ev-v3-004201-bfeb3734`, `ev-v3-004230-ed95f336`; v3 #514-#516 | fija: `se_da_esquema` con `cual` primer/segundo, contando las zonas de control del retroceso |
| **qué la invalida (recuento)** | más de una zona de control invalida | `fb-2026-09-09-sesion-01-1b2203b0`; v3 #624-#627 | fija por el registro: RN-009 con `zonas_control_max_por_esquema` (`zonas_desarrolladas_superan`) |
| **cuándo nace la orden** | al darse el esquema (A-29, `orden_limite_nace` DEFAULT_AMBIGUOUS) | A-29 | `al_darse_el_esquema` implementado; `al_tomarse_la_liquidez` NO_IMPLEMENTADA (§5) |
| **lado** | el sesgo manda: alcista → compra sobre el BAJO tomado; bajista → venta sobre el ALTO | RN-005 | fija: `LADO_ENTRADA` / `LADO_PIVOTE` en `engine/zonas.py` |
| **«limpia, sin ruido»** | **NINGUNA**: 0 de 14 pasajes la definen (`A24-A21-A26-A34-CLASIFICACION.md` §A-21). Lo más cercano son dos CONDICIONES DE VALIDEZ que el corpus sí enuncia: (a) más de una zona de control invalida (RN-009, pasaje 7); (b) «me rompe aquí con mecha, no hay validez» (v4 0:53:10, `ev-v4-005310-ce69f8c6`, con el nivel sin etiqueta: A-32) | `ev-v1-001435-f0586d02` (el control positivo: nombra «limpia» sin definirla) | **SELECTOR** `zona_control_limpia`, UNKNOWN, con las dos como opciones (§2) |

**Sobre las dos opciones del selector, dicho con su nombre.** Ninguna es una definición documentada
de «limpia»: son las dos únicas condiciones de validez que el corpus enuncia para la zona, y el
selector las ofrece porque la respuesta del trader tiene que poder calzar en algo cerrado. La
opción (a) hace de «limpia» lo mismo que ya dice RN-009 —si el trader responde eso, A-21 no pedía
nada distinto de RN-009, que es la «pregunta de fondo» de la clasificación—. La opción (b) lee el
pasaje de v4 con UNA suposición que el ítem no sostiene: que el nivel que la mecha no puede pasar es
el extremo lejano del bloque de origen; el ítem dice que el nivel roto NO lleva etiqueta (A-32
abierta). Si el trader nombra otro nivel, la opción no vale y se PARA (runbook §6).

## 2. Qué se construyó, y dónde

| paso | commit | qué |
|---|---|---|
| dominio | `8e6b404` | `domain/estructura_m1.py`: la referencia del breaker, la ruptura con mecha o cuerpo, el bloque de origen, las zonas de control del retroceso, el esquema como dato (`Esquema`, con `caja`) y la lectura de «limpia» como SELECTOR con dos opciones y ninguna más. Puro, sin mirar al futuro. 7 tests sobre M1 sintéticas |
| RN-011 | el segundo commit de la rama | `zona_control_limpia` en el registro (estrategia, enum, **UNKNOWN**); `engine/zonas.py`, el productor: anota la toma cuando RN-004 fija `liquidez_tomada`, detecta el esquema con las M1 desde la toma y produce `se_da_esquema`, `zonas_desarrolladas_superan` y `toca_colocar_orden_limite` (SI exactamente en el cierre del breaker, y liga `Z` a la zona), más `se_desarrolla_en_el_lado_de_ruido`; `EstadoDia.memoria` para el estado por día del productor; el cableado lee la zona del motor (la sintética de los tests sigue siendo la puerta de los tests); `--diagnostico-a21`; el visor pinta la zona (rectángulo y tabla, solo con `--simular`). spec 13.2.0 → 13.3.0. 9 tests |
| este informe | el tercer commit | §3 y §5, `scripts/verificacion_a21.py` y su salida `PREPARACION-A21-SALIDA.txt` |
| el runbook | el tercer commit | `docs/runbooks/ACTIVAR-A35-A44.md` §6 |

**El contrato, el mismo de A-35 y A-44 (ADR-0054).** SIN FIJAR no es un valor válido: con
`zona_control_limpia` UNKNOWN el arnés y el visor se niegan tras las compuertas de construcción, de
A-35 y de A-44, nombrando A-21 y sin leer una sola vela. La única excepción es pedir el diagnóstico
a propósito, y entonces cada línea y cada página llevan `DIAGNOSTICO-A21-<lectura>` junto a las
etiquetas de A-35 y A-44, y el nombre del fichero su forma compacta (`.DIAGNOSTICO.a35=<lectura>.a44=<modo>.a21=<lectura>`,
desde la segunda tarea de la rama, por el límite de 260 caracteres de Windows); con el valor fijado, pedir el diagnóstico se rechaza (test con
un registro sintético CONFIRMED). Las salidas en diagnóstico nunca alimentan una medida de fidelidad
(el informe lo dice en su cabecera; test). **Las dos lecturas dejan trazas DISTINTAS por
`arnes.correr`** (test obligatorio del brief): sobre un día sintético en el que la primera vela del
impulso baja con la mecha por debajo del extremo del bloque, `solo_una_zona_de_control` liga la zona
y `sin_mecha_mas_alla_del_extremo` no.

**Una trampa medida y corregida en la fase 2.** RN-011 no disparaba aunque el esquema existía: el
predicado `toca_colocar_orden_limite` tenía un efecto de un solo disparo («la primera vez que se ve
el esquema»), y el intérprete evalúa el `cuando` de las demás reglas de la clase de forma
ESPECULATIVA para el aviso H3 (`_empatadas`), así que el disparo se consumía en una evaluación que
no ejecutaba nada. Regla que sale de ahí: **los predicados del motor son puros; el estado que
tengan que producir se registra de forma idempotente.** Ahora es SI exactamente en el minuto del
cierre del breaker y registra la zona una sola vez aunque se evalúe varias.

**Lo que el mecanismo deja FIJO Y VISIBLE sin decidirlo por el trader** (cada cosa es un candidato
del §5): el bloque de origen es UNA vela, la última contraria; la referencia del breaker es el último
pivote de M1 contrario ya formado —con la misma lectura de «formado» que RN-004 (`cierre_vela_contraria`)—,
y la ventana de M1 que mira empieza 240 minutos antes de la toma; **la toma es el primer instante
DEL DÍA en que RN-004 fija `liquidez_tomada` y no se mueve después**, porque el hecho no caduca al
abrir la sesión (la spec lo escribe solo para `sesgo`, y su propia nota dice que F14b anticipó esa
caducidad para `liquidez_tomada` sin escribirla); las zonas de control del retroceso son los pivotes
en la dirección de la entrada formados después de la primera vela del impulso; el esquema se busca
desde la toma y, si el primer breaker no vale con la lectura, no se busca otro para la misma toma;
una vela sin cuerpo (doji) no es contraria; la mecha que mira la opción (b) es la de cualquier M1
entre el bloque y el breaker, contra el extremo lejano del bloque.

## 3. El embudo descriptivo, en DIAGNÓSTICO, solo sobre construcción (abril y agosto)

Cuatro corridas de `botsito motor arnes` sobre los 42 días de construcción (84 sesiones, 49 con
operaciones del trader, 77 operaciones), con A-35 en `cierre_vela_contraria` y A-44 en `sin_tope`
—las dos también en diagnóstico— y A-21 en cada una de sus dos lecturas, sin y con `--simular`.
**Todas rotuladas DIAGNÓSTICO, ninguna vale para nada.** Frente a la rama anterior
(`PREPARACION-A35-A44.md` §3): `toca_colocar_orden_limite` deja de ser una parada NO_IMPLEMENTADA,
RN-011 dispara y, con `--simular`, el embudo llega por primera vez a operaciones del bot.

| variante (DIAGNÓSTICO) | RN-004 | RN-008 / RN-009 | **RN-011 y RN-015** | `orden_dimensionada` | operaciones del bot | paradas NO_IMPLEMENTADA (sesiones del trader) | cobertura / precisión |
|---|---|---|---|---|---|---|---|
| (a) `solo_una_zona_de_control` | 61 de 84; 38 de 49 | 63 / 71 de 84 | **28 de 84; 17 de 49** | 17 de 49 | 0 (sin bróker nadie coloca) | 4: `cartuchos`, `perdida_dia_firma`, `perdida_total_firma`, `se_cierra_operacion` (49 de 49; las de siempre sin bróker) | 0 de 77 / sin definir |
| (b) `sin_mecha_mas_alla_del_extremo` | idéntico | 67 / 71 de 84 | **21 de 84; 14 de 49** | 14 de 49 | 0 | idéntico | idéntico |
| (a) · `--simular` | idéntico | 63 / 71 de 84 | 28 de 84; 17 de 49 | 17 de 49 | **7 puntuables + 2 en días sin operación del trader; 3 sesiones del trader**; RN-012 (el stop salta) 9 de 84 | **1**: `cartuchos` (3 de 49: las sesiones en que el bot perdió) | **1 de 77 / 1 de 7** |
| (b) · `--simular` | idéntico | 67 / 71 de 84 | 21 de 84; 14 de 49 | 14 de 49 | 7 puntuables + 2; 4 sesiones del trader; RN-012 9 de 84 | 1: `cartuchos` (4 de 49) | 1 de 77 / 1 de 7 |

Con `--simular` disparan además RN-027 (redondeo del lote; 27 y 20 de 84), RN-032 (el riesgo no
cabe antes del límite de la firma; 29 y 15 de 84) y RN-018 (no hay operaciones en paralelo; 2 de
84). Las 9 operaciones del bot acaban las 9 con el stop (RN-012): ninguna llega al objetivo en
construcción, con las dos lecturas. Las cifras de la cuenta simulada (saldo, equity) NO se copian
aquí: son un resultado en hipótesis sobre días de desarrollo y no dicen nada de ninguna lectura.

**Las dos lecturas SÍ se separan en construcción**: con (a) RN-011 liga una zona en 28 de las 84
sesiones (17 de las 49 del trader); con (b), en 21 (14). Las 7 sesiones de diferencia son sesiones
en las que hay una M1 entre el bloque y el breaker cuya mecha pasa el extremo lejano del bloque: (a)
liga la zona y (b) no liga ninguna. **No hay ninguna sesión en la que las dos liguen zonas
DISTINTAS**: cuando las dos ligan, ligan la misma, porque la diferencia entre lecturas es solo si el
esquema vale o no. Que (b) tenga MENOS zonas y UNA operación del bot MÁS no se ha separado por
causa en este informe: la cuenta simulada arrastra las pérdidas de un día al siguiente, así que una
zona menos por la mañana cambia lo que RN-032 deja abrir por la tarde. **Y nada de esto sirve para
elegir: la lectura la elige el trader, no el ajuste.**

**Dónde se detiene ahora cada sesión y cuál es el siguiente bloqueador.** Sin `--simular`, las
sesiones con zona llegan a `orden_dimensionada:si` (RN-011 y RN-015 disparan) y ahí acaban, porque
el motor de la spec no tiene bróker; las sin zona se quedan en `orden_dimensionada:no[productoras
sin cumplirse]`. Con `--simular`, las 17 (a) o 14 (b) sesiones del trader con
`orden_dimensionada:si` se reparten así (contado sobre las filas por sesión del informe): en 7 (a) o
4 (b) dispara además RN-032 —el riesgo de la operación ya no cabe antes del límite de la firma,
porque la cuenta simulada arrastra las pérdidas anteriores— y la orden no se abre; en 3 (a) o 4 (b)
la orden se llena, el stop salta (RN-012) y **la sesión se para en `acumulador:cartuchos` (RN-016),
la primera NO_IMPLEMENTADA que queda**; en las 7 restantes, en las dos lecturas, la orden queda
colocada (RN-015, RN-027) y la sesión acaba sin llenado (2 de ellas las rechaza el bróker). Detrás de RN-016, `se_cierra_operacion` y los acumuladores de la firma ya no aparecen porque
el bróker los alimenta. **El siguiente bloqueador tras RN-011 es RN-016 (los cartuchos)**; y el
siguiente hueco de la geometría, no bloqueante todavía, es qué pasa con una orden colocada que el
precio deja sin llenar (A-38, candidato 6).

**El tamaño de las zonas, medido, porque es lo primero que se ve en las páginas del visor.** Las
cajas de las zonas que el motor liga en construcción van de 5 a 28 puntos (mediana 10; 17 zonas con
(a), 13 con (b)): el bloque de origen es UNA vela de M1 y a las 07:00 de Madrid esas velas miden
medio pip. La distancia entrada-stop del trader en sus 77 operaciones va de 3 a 49 puntos (mediana
15): es el mismo orden de magnitud, así que las zonas pequeñas NO son por sí solas una señal de que
el bloque esté mal elegido; lo que sí se ve en una página de la fase 4 es una orden con el stop a 4
puntos y 125 lotes que el bróker rechazó: el lote que sale de una caja así es el que hay que mirar
(candidato 1, agrupar velas; y RN-027, el escalón del bróker).

**En cuántas operaciones del trader la entrada cae dentro de la zona según cada lectura**
(`scripts/verificacion_a21.py`, salida en `PREPARACION-A21-SALIDA.txt`; la zona vigente es la que
tendría el productor del motor en ese instante: el esquema desde la primera toma del día, mirando
solo las M1 anteriores al llenado del trader):

| lectura | operaciones con una zona vigente antes de su llenado | la entrada del trader cae DENTRO de la zona | fuera | la dirección del trader coincide con el lado de la zona | sin zona todavía (o sin lado, o sin toma) |
|---|---|---|---|---|---|
| (a) `solo_una_zona_de_control` | 37 de 77 | **6** | 31 | 30 | 40 |
| (b) `sin_mecha_mas_alla_del_extremo` | 32 de 77 | **6** | 26 | 28 | 45 |

Las 6 operaciones «dentro» son las mismas en las dos lecturas, y todas del primer esquema. De las 37
con zona en (a), 7 van en dirección CONTRARIA al lado de la zona: ahí el sesgo de H4 del motor y el
lado del trader no coinciden, que es cosa de RN-003/RN-005 y no de A-21. Que la entrada del trader
caiga «fuera» de la zona no dice que la zona esté mal: dice que en esa sesión el trader no operó el
primer esquema que el motor detecta desde la primera toma del día, y eso tiene tres causas posibles
que este informe no separa: otra toma (la toma del motor no se mueve en el día, §2), otra vela como
bloque, u otra cosa que no está escrita. Es material para la reunión (fase 4), no para el registro.

**El aviso H3 nuevo, medido y explicado.** Las corridas listan 28 (a) o 21 (b) avisos «disparador
RN-004, RN-011» —uno por sesión en la que RN-011 dispara— y, con `--simular`, 8 o 9 más «disparador
RN-004, RN-012». Causa medida (`verificacion_a21.py`): RN-004 vuelve a dar SI y a fijar
`liquidez_tomada = si` cada minuto mientras la última M15 cerrada siga cruzando el nivel (entre 15 y
120 minutos por sesión), y RN-011 dispara en uno de esos minutos en TODAS las sesiones en que
dispara (17 de 17 y 14 de 14). El orden no cambia nada —RN-004 escribe el valor que el hecho ya
tiene, y RN-011 lee una toma anotada antes—, pero no es el caso que `_empate_inocuo` reconoce (gates
que solo prohíben), así que avisa. **No se tapa aquí**: hacer que RN-004 no re-dispare es tocar la
spec (un `ninguno_de: hecho liquidez_tomada`) y ampliar `_empate_inocuo` a «re-fijar el mismo
valor» es una regla nueva del intérprete; las dos son del consultor (§5, candidato 8).

## 4. Lo que este informe NO hace, por regla

**No recomienda una lectura, no fija ningún parámetro y no marca A-21 como resuelta.** Las cifras
del §3 describen qué hace cada lectura sobre construcción y nada más; que una liga más zonas, que
las 6 entradas «dentro» coincidan o que una tenga una operación del bot más no dice cuál es la del
trader. **La lectura la elige el trader, no el ajuste.** Las corridas van rotuladas DIAGNÓSTICO en el
nombre y en cada línea y no se commitean: se regeneran con
`uv run botsito motor arnes --salida <f> --diagnostico-a35 cierre_vela_contraria --diagnostico-a44 sin_tope --diagnostico-a21 <lectura> [--simular]`
(con `<f>` en una ruta CORTA: el rótulo triple de diagnóstico sumado a una ruta larga supera el
límite de 260 caracteres de Windows y la corrida falla al escribir, medido hoy dos veces).

## 5. Candidatos a ambigüedad, SIN tocar `ambiguedades.yaml`

Cosas que el mecanismo deja fijas porque nadie las decidió, o que dependen de una respuesta que
no está. Ninguna se abre aquí: se llevan a la revisión del consultor.

1. **Agrupar varias velas contrarias en un bloque.** A-8 está RESUELTA con `mapeo_dos_velas =
   order_block_mayor` («lo que en una temporalidad mayor es una vela»), pero eso no es un criterio
   ejecutable en M1 (¿qué temporalidad? ¿cuántas velas?), y `agrupar_estructura` (RN-007) sigue
   NO_IMPLEMENTADA: el bloque de origen es UNA vela. Decidirlo es del consultor, con el trader si hace
   falta; no se tapa con un número.
2. **El punto exacto de la orden dentro de la mecha (A-36, abierta).** El mecanismo pone la
   entrada en el borde cercano de la vela, mechas incluidas; el stop sale del borde lejano. Si el
   trader entra «un poco dentro», la zona no cambia pero la orden sí.
3. **La temporalidad de la vela contraria (A-37, abierta).** El mecanismo la busca en M1.
4. **`orden_limite_nace = al_tomarse_la_liquidez`** (A-29, DEFAULT_AMBIGUOUS) sigue
   NO_IMPLEMENTADA: si el trader dice que la orden nace antes del esquema, RN-011 vuelve a parar.
5. **La reubicación de la orden (RN-006)** sigue NO_IMPLEMENTADA: la zona no se mueve una vez ligada.
6. **Cuándo se anula una orden que el precio deja sin llenar (A-38, abierta)** y **si una zona se
   invalida después de formada** (una mecha que la atraviese sin llenar, otra zona que nazca): el
   mecanismo no invalida nada tras el cierre del breaker, y en construcción la mayoría de las órdenes
   colocadas acaban la sesión sin llenar (§3).
7. **El nivel que la mecha no puede pasar (A-32, abierta).** La opción (b) del selector SUPONE que es
   el extremo lejano del bloque de origen; el ítem que la sostiene dice que el nivel no lleva
   etiqueta. Si el trader nombra la liquidez de M15 u otro nivel, la opción se reescribe (ADR).
8. **RN-004 re-dispara cada minuto y empata con RN-011 y RN-012 (H3).** Medido en §3. O la spec
   impide el re-disparo, o el intérprete reconoce el empate por re-fijar el mismo valor; decisión del
   consultor.
9. **La toma es del DÍA, no de la sesión.** `liquidez_tomada` no caduca al abrir la sesión (solo
   `sesgo` lo hace), así que la toma anotada por la mañana gobierna la tarde: si por la mañana hubo
   esquema, la tarde no busca otro, y si no lo hubo, la tarde lo busca desde la toma de la mañana.
   Medido: en una sesión de tarde el motor no liga la zona que sí saldría de la toma de esa misma
   sesión. La nota de la spec sobre `caduca` dice que F14b anticipó la caducidad de `liquidez_tomada`
   y hoy está escrita solo para `sesgo`: si el consultor la escribe, el productor la sigue sin tocar
   nada, porque la toma sigue al hecho.
10. **La ventana de M1 de la referencia (240 minutos antes de la toma).** Es una constante del
    productor (`LOOKBACK_M1`), no un parámetro del registro: fija cuánto atrás puede estar el último
    pivote contrario. Si un día la referencia está más atrás, no hay esquema.
11. **Un doji no es contraria.** Igual que en A-35: una vela sin cuerpo no cuenta como bloque ni corta
    el impulso.
12. **Qué cuenta como zona de control del retroceso.** El mecanismo cuenta los pivotes en la dirección
    de la entrada formados después de la primera vela del impulso; «pequeño retroceso» no tiene tamaño
    y «zona de control» no tiene definición propia en el corpus más allá de ese pivote.

## 6. Estado

Rama lista para revisión, NO cerrada. Tres commits sellados; sin push, así que la CI no se ha
ejecutado. Material de la reunión fuera del repo, en `C:\Users\USER\Desktop\reunion-a35-a44\a21\`
(cinco parejas de páginas del visor, la correspondencia solo para Aleks y cinco repreguntas
cerradas).
