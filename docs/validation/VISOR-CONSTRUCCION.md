# VISOR-CONSTRUCCION · Las comprobaciones de R3.1 en el visor, sobre el motor de hoy (R3.2)

Rama `trabajo/visor-construccion`, abierta el 2026-10-18 desde `main` en d1137eb (commit de estado
sobre el merge 3762429, tag `stable/F37s-margen-lote`). Encargo:
`docs/encargos/trabajo-visor-construccion.md`. Tramo: R3 (R3.2 de `docs/plan/HOJA-DE-RUTA.md`; O de
la Next Action). Modelo de la sesión: Opus 5.5 (`/model`), esfuerzo alto (`/effort`), los dos
fijados por Aleks en su terminal antes del encargo.

## 0 · La base, comprobada al abrir

Las cuatro comprobaciones del paso 1 de la skill `abrir-rama`, con su salida:

- `git fetch origin` y `git status --short` vacío; `git rev-parse --short main` → `d1137eb`;
  `git rev-parse main origin/main` → dos veces `d1137eb9fd37192d52c4f2331631493af2bf8729`.
- El último tag de los registros de cierre de `docs/state/HISTORIA.md` es
  `stable/F37s-margen-lote`; `git rev-parse "stable/F37s-margen-lote^{commit}"` y
  `git rev-parse main^1` dan los dos `3762429aefe9094cb928cafd420fe7c6294f53b9`, y
  `git ls-remote --tags origin stable/F37s-margen-lote` lo trae
  (`8033c590643a5875615ccb0672dbd4a92dc2819e refs/tags/stable/F37s-margen-lote`).
- La CI de `main` sobre su HEAD, con `gh run view 39136089919` (ni curl, ni `gh run watch`, ni
  guion): `status completed`, `conclusion success`, `headSha d1137eb9…af2bf8729`, `headBranch main`.
- Ninguna otra rama: `git branch --list` da solo `main`; `git ls-remote --heads origin "fix/*"`
  sale vacío.


## 1 · Fase 0 · Inventario sin abrir ninguna página (2026-10-18)

Medido en el código y en salidas ya commiteadas de días dev. No se ha generado ninguna página del
visor, no se ha corrido el arnés y no se ha leído ninguna vela. Lo único escrito: este informe.

### 1.a Cómo reproducir la corrida 2 en el visor

**Lo que hace el arnés** (`src/botsito/cli.py`, `motor_arnes`): construye el motor cableado
(`cableado.construir_motor_cableado`, :2420-2436) y le pone `motor.cuenta_diaria =
diag.cuenta_diaria` (:2437); el mercado de cada día sale de `arnes.dias_de_mercado`
(`engine/arnes.py:179-215`: las M1 del mes y del anterior, agregadas a H4 y M15 con `anclaje_h4`,
en un `DatosMercado` con la lectura de A-35, y un `DiaDeMercado` con el reloj de las sesiones).

**Lo que hace el visor** (`cli.py`, `motor_visor`, :2478-2588): con `--simular` construye el MISMO
motor cableado con los mismos argumentos (`cableado.construir_motor_cableado`, :2540-2556: perfil,
fase, `--depuracion`, tope de A-44, lectura de A-21, `diagnostico_a27`, tipo de orden de A-47) y
lo pone en el `Preparador` (:2557), **pero no le pasa `cuenta_diaria`**: `_diagnostico_de` lee la
opción (:2250-2251 y :2261) y nadie la copia a `cableado_motor`. **Deuda, con su línea:** falta en
`cli.py:2557`, tras `preparador.motor = cableado_motor`, el equivalente de `cli.py:2437`
(`cableado_motor.cuenta_diaria = diag.cuenta_diaria`). No se arregla aquí. El mercado del día lo
arma `visor.Preparador.preparar` (`engine/visor.py:308-319`) igual que el arnés: las M1 del mes y
del anterior (`Preparador._m1`, :287-297), las mismas agregaciones con `anclaje_h4`, el mismo
`DatosMercado(h4, m15, m1, lectura_pivote)` y el mismo `DiaDeMercado(dia, huso, sesiones, datos,
reloj=reloj_de_las_sesiones(registro))`; y llama a `motor.correr_dia(mercado)` (:319), el mismo
método que el arnés (`arnes.correr`, :222-229).

**Por qué con `--caso` da lo mismo que la corrida 2, medido en el código.** Lo que el motor
cableado arrastra entre días son cuatro campos (`cableado.py:180-186`): `cuenta`, `seguidor` (tope
de A-44), `racha` (RN-036) y `primero_en_tocar` (solo para el informe). Con
`--diagnostico-cuenta-diaria` el arnés los pone a `None` al empezar cada día (`cableado.py:207-208`)
y los recrea (:209-213). Con `--caso`, el visor construye un motor nuevo para UN día, así que los
tres nacen en `None` y se crean igual (:209-213): mismo saldo inicial, mismo seguidor (con
`sin_tope`), misma racha vacía. El broker es nuevo por día en los dos (`cableado.py:214-224`), el
mercado de ticks sale de `construir_motor_cableado` (`mercado_de_construccion`, la compuerta del
arnés) en los dos, y las opciones de diagnóstico pasan igual. **Para un día con `--caso`, las
órdenes y las operaciones del bot son las de la corrida 2**; con `--todos`, la cuenta se arrastra
y no lo son. Se COMPRUEBA además en la fase 1 para cada día: el guion de 1.d compara las órdenes
del día (id, instante, precio, resultado, motivo) con las de «### Ordenes» de la salida de `main`;
si difieren, PARADA.

**El comando de cada página** (fase 1), con las opciones de la corrida 2 y `--simular`, siempre
`--caso`, la salida fuera de git:

    uv run botsito motor visor --simular --diagnostico-a35 cierre_vela_contraria --diagnostico-a44 sin_tope --diagnostico-cuenta-diaria --caso caso-eurusd-AAAA-MM-DD --salida data/visor/visor-construccion

(`--diagnostico-cuenta-diaria` no cambia nada con `--caso`, por lo de arriba, pero se pasa para
que el rótulo de la página sea el de la corrida 2; con `--hasta HH:MM`, la vista recortada.)

### 1.b Qué lee y qué enseña el visor del material de fuera del día dev, medido en el código

- **El mes anterior entero** (`Preparador._m1`, `visor.py:287-297`): para un día de abril, el M1
  entero de marzo de 2026 (mes reservado entero y sin sortear); para julio, el de junio (11 días
  reservados por recuento); para agosto, julio (sin reservados); para enero, ninguno (no hay M1 de
  2025-12 en `data/manifests/`). La misma lectura que el arnés: se declara en HOLDOUT-EXPOSICIONES,
  nombrando el visor, el día que se genere la primera página y ANTES.
- **Lo que la página pinta de fuera del día dev** (`render_dia`, `visor.py:958-1040`):
  - el gráfico de **H4 de contexto** (`_h4_svg`, :683-714; `_h4_de_contexto`, :400-416): las H4
    cerradas antes del fin de la ventana, desde la `anterior` de la H4 que decide el sesgo más
    antiguo de las dos sesiones, y **al menos las 8 últimas** (`H4_DE_CONTEXTO_MIN`, :77). La
    ventana acaba a las 15:00 del trader, así que las 8 últimas H4 llegan siempre a días anteriores
    al día dev; y la que decide el sesgo puede estar hasta **60 H4 atrás** (`sesgo_h4_tope_velas`,
    `parametros.yaml`), unos diez días de mercado. **No es solo «los primeros días» del mes**: un
    día de abril hasta mediados de mes puede pintar H4 de marzo, y uno de julio hasta mediados, H4
    de junio. Cuál exactamente depende de las velas; no se mide sin leerlas (§1.e);
  - el párrafo **«Sesgo anotado»** de cada sesión (`_sesion_html`, :765-778): «rompe la H4 que abre
    a las HH:MM», el número de H4 miradas y la ruptura en puntos, que pueden ser de un día anterior;
  - la línea del **bróker simulado** (`_broker_html`, :938-945): «saldo al cierre …, equity …»:
    **dinero**;
  - **el propio gráfico M1/M15 de la ventana** (`preparar`, `visor.py:321-325`; hallazgo del
    auditor, punto 14): la ventana va de las 00:00 a las 15:00 del trader
    (`knowledge/cases/kit/config.yaml:9-11`), y con la rejilla de ADR-0069 las 00:00 del día
    operativo caen antes de medianoche UTC (`cases/relojes.py:126-131`): las primeras horas del
    gráfico son del **día UTC anterior**. En una página del 2026-04-01 son velas del 31 de marzo (mes
    reservado entero); en una del 2026-07-01, del 30 de junio. El precedente de R3.1
    (CORRIDA-CONSTRUCCION.md §11, ERRORES-RECURRENTES.md, fila de `trabajo/corrida-construccion`)
    trató por su fecha UTC una H4 de las 21:00Z del último día de junio como de un día de junio, y
    ese día salió del holdout. **Por eso en esta rama «anterior al día dev» se lee por la fecha UTC
    de la vela**: nada del informe ni de los anexos lleva un instante, una vela ni un precio
    anterior a las 00:00Z de la fecha del caso.
  Todo lo demás de la página es del día dev: las M1 y M15 de la ventana desde las 00:00Z, las
  operaciones del trader y del bot, las zonas (bloque y cierre del día), órdenes, posiciones,
  eventos y la traza por sesión (hechos fijados con su instante, embudo, reglas disparadas,
  acciones bloqueadas). `--hasta` NO recorta las H4 de contexto, ni «Acciones bloqueadas»,
  «Reglas disparadas», «Donde se para» y los avisos H3, ni el resumen del bróker (auditor, punto
  27; `visor.py:785`, `:796-816`, `:942-945`, `:1028`): lo que `VISOR-DIAS.md:40-41` promete
  («solo lo cerrado y fijado hasta esa hora») no vale para esas partes.
- **Las sesiones de las listas que pueden pintar H4 del mes anterior** (por fecha, sin medir
  velas): de abril, 04-01 (11-15), 04-06, 04-07, 04-13, 04-14 y 04-16/04-17 (marzo); de julio,
  07-01, 07-02, 07-03, 07-08, 07-09, 07-10, 07-13 y 07-14 (junio). En la fase 1, antes de abrir cada
  página, un guion dice por recuento si su contexto H4 empieza en el mes anterior (sí o no) y si
  alguna de esas H4 cae en un día con caso reservado, por pertenencia y sin imprimir fechas
  (`casos_reservados`), como en R3.1 (CORRIDA-CONSTRUCCION.md §3.14).
- **Cómo se mira entonces una página sin copiar nada de fuera del día dev:** la sesión NO lee el
  HTML entero. Un guion de anexo (`extraer_pagina.py`, §1.d) extrae solo las tablas del día dev
  (zonas, órdenes, posiciones, eventos, hechos fijados por sesión, reglas disparadas, acciones
  bloqueadas y el valor del sesgo anotado, sin su paréntesis) y se salta el SVG de H4, el
  paréntesis del sesgo y la línea de saldo y equity. Las páginas se generan para que V las abra;
  la sesión no abre ninguna imagen.

### 1.c Las listas, rehechas sobre la salida de `main` de hoy

Fuente: `anexos/MARGEN-LOTE/diaria.DIAGNOSTICO…txt` («## Por sesion» y «### Ordenes») y
`anexos/MARGEN-LOTE/patrones.txt`, frente a los de R3.1 (`anexos/CORRIDA-CONSTRUCCION/`). Un guion
de la carpeta de trabajo que solo lee esas salidas (días dev); va a los anexos en la fase 1 como
`listas.py` con su salida.

**P2 (entrada): 33 filas en 26 sesiones hoy; 18 en 14 en R3.1.** Para elegir los tres días:

| sesión | hoy frente a R3.1 | filas de hoy (lado, Δentrada) |
|---|---|---|
| 2026-01-02 07-11 | desaparece | — (R3.1: compra, 11 puntos) |
| 2026-01-02 11-15 | nueva | venta 4; venta 5 |
| 2026-01-05 07-11 | sigue | venta 17 |
| 2026-01-05 11-15 | sigue | venta 7; venta 12 |
| 2026-01-08 07-11 | sigue | compra 21 |
| 2026-01-13 11-15 | sigue | compra 8 |
| 2026-01-15 07-11 | nueva | venta 20 |
| 2026-01-20 11-15 | sigue | compra 11 |
| 2026-01-21 07-11 | nueva | venta 7 |
| 2026-01-26 07-11 | sigue | compra 12 |
| 2026-01-28 07-11 | nueva | compra 4 |
| 2026-01-29 11-15 | sigue | venta 52 |
| 2026-04-01 11-15 | sigue | compra 7 |
| 2026-04-13 07-11 | nueva | compra 11 |
| 2026-04-16 07-11 | nueva | compra 4 |
| 2026-04-16 11-15 | sigue | venta 10 |
| 2026-07-02 11-15 | nueva | compra 43 |
| 2026-07-03 07-11 | sigue | compra 11; compra 15 |
| 2026-07-09 11-15 | sigue | compra 13 |
| 2026-07-10 07-11 | nueva | compra 32; compra 4 |
| 2026-07-13 11-15 | nueva | compra 6 |
| 2026-07-17 07-11 | nueva | venta 15; venta 7 |
| 2026-08-03 11-15 | sigue | venta 9; venta 4; venta 6 |
| 2026-08-20 11-15 | sigue | compra 36 |
| 2026-08-25 11-15 | nueva | venta 6 |
| 2026-08-26 07-11 | nueva | venta 4 |
| 2026-08-28 11-15 | nueva | venta 4 |

(Δentrada = la distancia, en puntos, entre la entrada del trader y la del bot más cercana del mismo
lado a menos de 15 minutos, «minima» en `patrones.txt`. Las 12 nuevas vienen de órdenes que ADR-0081
deja vivir: antes se rechazaban por volumen.)

**Las 14 sesiones sin orden (RN-005, RN-009 y RN-001): las 14 siguen igual.** En cada una, hoy como
en R3.1: 0 operaciones del bot, 0 órdenes en «### Ordenes», `orden_dimensionada:si`,
`liquidez_tomada:si` y `bloqueadas RN-015:accion:colocar_orden_limite:prohibida:abrir_operacion`;
RN-005 y RN-009 entre las disparadas de las 14, y RN-001 en las mismas 7 sesiones 11-15 (2026-04-27,
07-01, 07-14, 07-16, 08-19, 08-21 y 08-27). Ninguna ha dejado de ser P4. Las 14: 2026-01-30 07-11,
2026-04-17 07-11, 2026-04-27 11-15, 2026-07-01 11-15, 2026-07-09 07-11, 2026-07-14 07-11 y 11-15,
2026-07-16 11-15, 2026-08-03 07-11, 2026-08-11 07-11, 2026-08-19 11-15, 2026-08-21 11-15,
2026-08-25 07-11, 2026-08-27 11-15. **Un cambio que importa para RN-001:** 2026-07-01 11-15 dispara
además RN-016 y hoy lleva `detenido_por_cartuchos:si`. R3.1 dedujo que RN-001 disparaba por el
minuto de `ventana_fin` porque las 104 sesiones tenían 0 `detenido_por_*`; hoy hay 4 con los
cartuchos agotados (2026-07-01 07-11 y 11-15, 2026-07-13 11-15, 2026-08-26 07-11; `grep -c
'detenido_por_cartuchos:si'` sobre la diaria de `main` = 4), porque las órdenes que ADR-0081 deja
vivir gastan cartuchos. En 2026-07-01 11-15 la prohibición de RN-001 puede venir de los cartuchos y
no de la ventana: la fase 1 lo dice por cierre (guion de traza).

**Las 2 sesiones sin bloqueo y sin `orden_dimensionada` siguen así:** 2026-01-08 11-15 (dispara
RN-001 y RN-003; `liquidez_tomada:no[productoras sin cumplirse]`) y 2026-08-14 07-11 (dispara solo
RN-003; ídem). Las dos con `bloqueadas ninguna` y 0 órdenes. **Un matiz que cambia la comprobación:**
hoy, como en R3.1, el embudo dice que en las dos falta `liquidez_tomada` (sus productoras no se
cumplieron), no que RN-011 fallara con el camino producido: el hecho del camino que falta es la
toma de liquidez, antes de RN-011 (el camino es sesgo, `orden_dimensionada` y `liquidez_tomada`,
`arnes.py:447-450`; sin toma, `zona_del_punto` devuelve None, `zonas.py:357-360`). §4.6 de R3.1 ya
lo decía («no se produjo un hecho del camino»); la respuesta del consultor a la PARADA 4, punto 2,
lo leyó como «RN-011 no dimensiona con los hechos del camino producidos». La causa probable está en
RN-004 y en la lectura de «formado» de A-35, que es el terreno del heredado 25 (`liquidez_tomada`
falta en 6-7 de 104 sesiones; PROJECT_STATE, heredado 25) y del 30 (RN-004 tras A-35, «mirada con el
visor»), que esta rama no toca. Decisión 3.

**Los rechazos por `precio_invalido`: 26 en 20 sesiones hoy; 11 en 9 en R3.1.**

| sesión | hoy | R3.1 | ¿R3.1 tenía rechazo por volumen en la sesión? |
|---|---|---|---|
| 2026-01-08 07-11 | 1 | 0 | sí |
| 2026-01-14 07-11 | 1 | 0 | sí |
| 2026-01-23 07-11 | 1 | 0 | no |
| 2026-01-29 07-11 | 3 | 3 | no |
| 2026-04-06 11-15 | 1 | 1 | no |
| 2026-04-07 07-11 | 1 | 0 | sí |
| 2026-04-07 11-15 | 1 | 0 | sí |
| 2026-04-14 07-11 | 1 | 0 | sí |
| **2026-04-16 07-11** | **0** | 1 | sí |
| 2026-04-22 11-15 | 1 | 1 | no |
| 2026-04-27 07-11 | 3 | 1 | sí |
| **2026-07-08 11-15** | **1** | 1 | no |
| 2026-07-10 07-11 | 2 | 0 | sí |
| **2026-07-13 11-15** | **1** | 1 | sí |
| 2026-08-05 07-11 | 1 | 0 | sí |
| 2026-08-06 11-15 | 1 | 0 | sí |
| 2026-08-07 07-11 | 2 | 1 | sí |
| 2026-08-17 11-15 | 1 | 1 | sí |
| 2026-08-26 11-15 | 1 | 0 | sí |
| 2026-08-27 07-11 | 1 | 0 | sí |
| 2026-08-31 07-11 | 1 | 0 | sí |

**De las 3 de R3.1, dos siguen y una no:** 2026-07-08 11-15 sigue igual (1 rechazo, nada más);
2026-07-13 11-15 sigue con su rechazo, pero hoy coloca y llena 3 órdenes más (en R3.1: el rechazo,
uno por volumen y una cancelada); **2026-04-16 07-11 ya no rechaza**: hoy coloca 4 órdenes (2
llenadas, 2 canceladas) y el bot tiene 2 operaciones. Las sesiones con más rechazos que en R3.1 son
14; 13 de ellas tenían en R3.1 un rechazo por volumen en la misma sesión (la otra, 2026-01-23
07-11), coherente con MARGEN-LOTE.md §4.a (el volumen se miraba antes que el precio).

### 1.d De dónde sale cada dato, y cómo sacarlo sin tocar código

| Lo que hay que comprobar | Dónde está | Qué falta y cómo se saca |
|---|---|---|
| P2: el 0 y el 1 de la caja en cada instante | **la página SÍ lo tiene** (corrección del auditor, punto 26, sobre la premisa del encargo): `Zona` es inmutable (`zonas.py:122-134`) y, con `caja_se_fija = en_cada_cierre_m1`, cada 1 recalculado es una zona NUEVA, con su id, su entrada (el 0), su extremo (el 1) y su `formada` (`zonas.py:380-401`); la tabla «Zonas de entrada ligadas por el motor» las lista todas (`_filas_zonas`, `visor.py:844-861`) y el gráfico las dibuja todas (`:612-633`). La caja de un instante es la última zona del punto formada antes de él. Lo que NO tiene: hasta cuándo estuvo viva cada caja (cada rectángulo llega al borde derecho, `:620`) | la vida de cada caja sale de **«### Ordenes»** (cada recolocación es una fila con su precio, el 0, y su `distancia (puntos)` al stop, 0,8 de la caja) y del guion de traza, que dice qué zona liga RN-011 en cada cierre |
| P2: el 0 del trader | página: operaciones del trader (entrada y stop del caso) | ya está en la página y en «Diferencias por operación» |
| RN-005, RN-009 y RN-001: qué gate prohibió y en qué cierre | página y salida: `bloqueadas` y `disparadas` son conjuntos POR SESIÓN, sin instante ni autor (`motor.py:175-183`; `cableado.py:284-289`); la página no lo tiene | **guion de traza** (`traza_por_cierre.py`, abajo): el `Evento` de cada cierre de M1 sí lo lleva (`interprete.py:118-129`: `disparadas` en orden, `prohibidos`, `bloqueadas`) |
| El minuto de `ventana_fin` (RN-001) | página: los límites de sesión; salida: el motivo de cancelación «en ventana_fin» (`cableado.py:140-150`) | el guion de traza dice en qué cierre dispara RN-001 |
| Las 2 sin `orden_dimensionada`: por qué no hubo camino | página: «Hechos fijados» con su instante (`_sesion_html`, :787-794) y el embudo | la página basta; el guion de traza da además las reglas que evaluaron SÍ/NO por cierre si hace falta |
| `precio_invalido`: el motivo | **«### Ordenes»** (`motivo`) | la página no lo lleva (`_filas_ordenes`: solo estado). De «### Ordenes» se copian solo día, sesión, id, instante, precio, resultado, motivo, lote, distancia y límite: **las dos columnas de margen van en USD y no se copian** (encargo §2, «nada en dinero»; auditor, punto 30) |
| `precio_invalido`: el bid o el ask del instante | ningún sitio: la página pinta M1 | **guion de ticks** (`ticks_del_rechazo.py`): lee el mercado del día dev por la compuerta (`simulacion.mercado_de_construccion`, sin nombrar `data/manifests/ticks`: la guardia niega un guion que lo nombre, G.1) y da el último tick anterior al instante de cada orden rechazada (bid, ask), junto al precio de la orden; solo el día dev. **6 de los 26 rechazos caen en una de las 18 horas sin ticks** (CORRIDA-CONSTRUCCION.md §1.e: 2026-04-06 10Z, 04-07 10Z, 04-22 10Z, 07-10 05Z dos veces, 08-17 11Z; auditor, punto 4): ahí el bróker tomó el cierre de la M1 más el spread supuesto (`llenado.py:96-112`), y el guion lo da igual y lo marca «respaldo M1» |
| ADR-0074: el punto rechazado no se recoloca con otra caja | «### Ordenes» (precios de la sesión tras el rechazo) y `zonas.marcar_rechazada` (`zonas.py:404-410`) | el guion de traza anota los puntos rechazados de la sesión y si alguna orden posterior usa el mismo precio |

**Una contradicción con el encargo (decisión 1): `--depuracion` no es una traza.** Es la opción que
deja correr un día sin ticks sobre el respaldo M1 (`cli.py:2339-2342`, ADR-0051 §8): cambia la
simulación y la marca como que no cuenta. Usarla daría otra corrida, no la de `main`. La traza por
cierre que hace falta la da un guion de anexo que corre el mismo motor y LEE el `Evento` de cada
cierre, sin tocar `src/`.

**Los guiones que propongo** (en `anexos/VISOR-CONSTRUCCION/`, sin cifras dentro, con los mismos
argumentos que el comando del visor y `--caso`):
1. `traza_por_cierre.py --caso … --desde HH:MM --hasta HH:MM`: construye el motor cableado como
   `motor_visor` (mismas opciones de la corrida 2), envuelve `Interprete.evento` DENTRO del guion
   (sin tocar `src/`) y, por cada cierre de M1 de la sesión, imprime el instante (UTC y hora del
   trader), las reglas disparadas en orden, los efectos prohibidos y las acciones bloqueadas con su
   regla; y por cada orden colocada, la zona (entrada y extremo) de ese instante. Al final, compara
   sus órdenes con las de «### Ordenes» de la salida de `main` para ese día: si difieren, PARADA.
2. `ticks_del_rechazo.py --caso …`: para cada orden rechazada por `precio_invalido` del día, el
   último bid y ask anteriores al instante, y el precio y el lado de la orden. Solo ticks del día dev.
3. `extraer_pagina.py <html>`: de una página generada, las tablas del día dev y nada del contexto
   H4, del paréntesis del sesgo ni de la línea de saldo y equity (§1.b).
4. `contexto_h4.py --caso …`: si el contexto H4 de la página empieza en el mes anterior y si
   alguna de sus H4 cae en un día con caso reservado, por recuento y pertenencia, sin fechas.
Los cuatro leen velas o ticks (el 1, el 2 y el 4) o una página (el 3): se corren después de la fila
de exposiciones de la fase 1.

### 1.e Lo que no pude medir

- **Qué H4 exactas pinta el contexto de cada sesión**, y si alguna cae en un día reservado: exige
  leer velas (fase 1, con su fila, por recuento y pertenencia).
- **El autor de cada prohibición** en las 14 sesiones: no está en ninguna salida; lo da el guion de
  traza en la fase 1.
- **Hasta cuándo estuvo viva cada caja**: la página tiene todas las cajas con su instante de
  formación, pero no su fin; sale de «### Ordenes» y del guion de traza.
- **Si la guardia deja leer con Read una página de `data/visor/`** y ejecutar los guiones nuevos de
  anexo: se ve en la fase 1; si niega, PARADA (no se rodea).
- **Que el visor dé de verdad las mismas órdenes que la corrida 2 en un día**: leído en el código
  (1.a); se comprueba en la fase 1 con el guion de traza.

### 1.f El encargo frente al repo (auditor, 2026-10-18)

El agente `auditor-encargo` contrastó 46 afirmaciones: 30 correctas, 3 incorrectas y 13 con matiz;
y 10 cosas que el repo pide y el encargo no dice. Lo que cambia el trabajo:

| # | Qué | Veredicto | Evidencia |
|---|---|---|---|
| h1 | «enseña la zona con su estado final del día, no la caja de cada instante» | INCORRECTA | cada 1 recalculado es una zona nueva e inmutable con su `formada` (`zonas.py:122-134`, `:380-401`); la página las lista y dibuja todas (`visor.py:612-633`, `:844-861`). Falta solo hasta cuándo estuvo viva cada una (§1.d) |
| h2 | «la traza con --depuracion» | INCORRECTA | `--depuracion` admite días sin ticks sobre el respaldo M1 y marca la corrida como que no cuenta (`cli.py:2339-2343`; `cableado.py:199-203`): cambia la corrida y no da ninguna traza. Decisión 1 |
| h3 | «por qué RN-011 no dimensionó con los hechos del camino producidos» | INCORRECTA | en las dos sesiones falta `liquidez_tomada` (§1.c); el camino no se produjo. Decisión 3 |
| h4 | «la sección de H4 de contexto pinta velas de días anteriores» | MATIZ | también el gráfico M1/M15 de la ventana empieza el día UTC anterior (§1.b) |
| h5 | RN-001 «el minuto de ventana_fin» | MATIZ | hoy 4 sesiones con `detenido_por_cartuchos:si`, una de ellas 2026-07-01 11-15 de la lista (§1.c) |
| h6 | «RN-011 y ADR-0064 §1: el 0 y el punto no se mueven; lo que recalcula ADR-0074 es el 1» | MATIZ | la frase es de ADR-0074 §1 (`0074…md:20`); ADR-0064 §1 define el punto (`orden_stop_punto` = `ultimo_pivote_m1`, DEFAULT_AMBIGUOUS bajo A-48) y su §4 dice que el punto se reubica con cada pivote nuevo (`0064…md:59-62`); RN-011 no nombra el pivote. En la fase 1 la comprobación de P2 se hace contra ADR-0064 §2 (el 0 es el punto) y ADR-0074 §1 (con el punto fijo, se recalcula el 1), y se dice si el punto cambió por un pivote nuevo (§4 de ADR-0064) |
| h7 | «Las columnas de MARGEN-LOTE» de «### Ordenes» | MATIZ | dos van en USD: no se copian (§1.d) |
| h8 | El guion de ticks | MATIZ | la guardia niega nombrar `data/manifests/ticks` (G.1), y 6 de los 26 rechazos caen en horas sin ticks (§1.d) |
| h9 | «O sale a HISTORIA bajo “# Next Action HECHA · O · …”» | MATIZ | HISTORIA ya tiene un «HECHA · O» (la O de P-D1, `HISTORIA.md:8906`); como hizo E, el nuevo lleva un descriptor («· O · las comprobaciones en el visor ·») |
| h10 | «aplícalas en memoria y corre test_hoja_de_ruta.py y test_project_state.py, como el simular_cierre.py» | MATIZ | ese guion corre `problemas_a`, `_b` y `_c` y mide los bytes (`simular_cierre.py:45-49`); `test_project_state` lee el fichero del disco con su fixture, así que el guion de esta rama reproduce además sus secciones, la rama y el tope de 25.000 bytes |
| h11 | «la salida de main de hoy» | MATIZ | la diaria se generó en 5f68f40; d1137eb solo cambió comentarios, descripciones y `spec_version` (d46e753): las decisiones son las mismas, no la corrida sobre d1137eb |
| h12 | La skill `abrir-rama` pide la CI por la API de check-runs | MATIZ | el encargo dice gh o la skill; se usó `gh run view` (§0) |
| h13 | Lo que el repo pide y el encargo no dice | — | (1) ADR-0080 §10 dejó «para la rama O» enseñar en el visor las H4 saltadas por color (`0080…md:157-158`): esta rama no toca código; va como deuda o rama. (2) el visor es un segundo lector del M1 de marzo y junio, también en cada `make check` (`tests/unit/test_visor.py:368-401`), y la Technical Debt y G.2 solo nombran el arnés. (3) R4.1, «Qué es», gana también las preguntas nuevas, como A-57 en margen-lote. (4) el «Hecho cuando» de R3.2 dice «(E o R)»: la línea de Estado explica la tercera conclusión, «correcto». (5) el heredado 25 ya midió la falta de `liquidez_tomada` |

### 1.g Exposiciones de hoy

Ninguna. La sesión no generó ninguna página, no corrió el arnés ni leyó ninguna vela, tick, libro o
imagen: leyó código y las salidas commiteadas de `main` y de R3.1 (días dev). El auditor solo leyó
el repo y corrió `gh run view 39136089919`. No hace falta fila en HOLDOUT-EXPOSICIONES; la de la fase
1 va antes de la primera página.

## Lo que necesito que decidas

0. **Los tres días de P2** (te toca elegir). Para ayudarte: recomiendo tres sesiones que SIGUEN
   desde R3.1, con Δentrada grande y fuera de los primeros días de abril y julio (sin H4 de marzo ni
   de junio en la página): 2026-01-29 11-15 (venta, 52 puntos), 2026-08-20 11-15 (compra, 36) y
   2026-01-08 07-11 (compra, 21). Alternativa: incluir una nueva de ADR-0081 (2026-07-02 11-15,
   compra, 43; pinta H4 de junio). Coste de la alternativa: una página con velas de un mes con días
   reservados, declarada.
1. **La traza por cierre (h2).** `--depuracion` cambia la corrida. Opciones: (a) el guion
   `traza_por_cierre.py` de §1.d, que corre el mismo motor que el visor con las opciones de la
   corrida 2, LEE el `Evento` de cada cierre de M1 (reglas disparadas en orden, efectos prohibidos,
   acciones bloqueadas, zona ligada) sin tocar `src/`, y comprueba que sus órdenes son las de
   «### Ordenes» de `main`; (b) solo la página y «### Ordenes», sin el autor de cada prohibición.
   Recomiendo (a): sin él no se puede decir qué gate prohibió en cada cierre en las 14 sesiones, que
   es lo que pide la comprobación. Coste de (a): un guion nuevo que la guardia trata como código sin
   revisar (si lo niega, PARADA).
2. **Cómo mira la sesión una página (§1.b).** Opciones: (a) la sesión no lee el HTML entero: un
   guion `extraer_pagina.py` saca solo las tablas del día dev y omite el SVG de H4, el paréntesis
   del sesgo y la línea de saldo y equity; los HTML los abre V; (b) la sesión lee la página entera
   con Read y no copia lo de fuera del día dev. Recomiendo (a): con (b) la sesión lee de verdad
   horas y precios de días anteriores (marzo, junio) y la regla depende de no copiarlos; con (a) no
   los ve. Coste de (a): otro guion.
3. **Las 2 sesiones sin `orden_dimensionada` (h3).** El hecho que falta es `liquidez_tomada`, no
   RN-011. Opciones: (a) se mira con la traza por qué RN-004 no produjo la toma en cada cierre de
   la sesión (qué pivote y qué lectura de «formado» de A-35), y la conclusión es R (A-35, ya en V)
   salvo que se vea un error de código, sin tocar los heredados 25 y 30; (b) se dejan fuera de esta
   rama por ser terreno del heredado 30. Recomiendo (a): es la comprobación que pediste, con la
   premisa corregida; si la causa es la lectura de A-35 se dice y no se toca. Coste de (a):
   rozar el heredado 30, que queda vivo.
4. **Qué rechazos por `precio_invalido` se miran.** De los 3 de R3.1, 2026-04-16 07-11 ya no rechaza
   (§1.c). Opciones: (a) 2026-07-08 11-15 y 2026-07-13 11-15 (los que siguen) más tres nuevos con
   ticks reales, fuera de las horas sin ticks: 2026-01-08 07-11 (nuevo, con volumen en R3.1),
   2026-08-07 07-11 (dos rechazos, uno nuevo) y 2026-04-27 07-11 (tres rechazos, dos nuevos); y
   2026-04-16 07-11 se cita como «ya no rechaza» con lo que hace hoy, sin página; (b) solo los dos
   que siguen. Recomiendo (a): cubre los tres meses y los dos orígenes (el que siempre fue precio y
   el que antes tapaba el volumen). Coste: tres páginas más; 2026-07-08 y 07-13 pintan H4 de junio.
5. **«Anterior al día dev» por la fecha UTC (§1.b).** El gráfico M1 de la página empieza el día UTC
   anterior. Opciones: (a) leer «anterior al día dev» por la fecha UTC de la vela: nada antes de las
   00:00Z de la fecha del caso entra al informe ni a los anexos, aunque sea del día operativo; (b)
   por el día operativo de la rejilla. Recomiendo (a), por el precedente de R3.1.
6. **Lo que el repo pide y el encargo no dice (h13).** Opciones: (a) la deuda de esta rama lleva
   tres líneas más: que el visor enseñe las H4 saltadas por el color (ADR-0080 §10, que lo dejó para
   O), que el visor también lee el M1 de marzo y junio en cada `make check` (`test_visor.py`), y que
   `--hasta` no recorta las H4, las listas por sesión ni el resumen del bróker (VISOR-DIAS.md); y
   las líneas del cierre añaden las preguntas nuevas también a R4.1, y la línea de Estado de R3.2
   explica «correcto»; (b) solo las dos deudas del encargo. Recomiendo (a).
7. **El guion de cierre simulado (h10).** Reproduce `problemas_a`, `_b` y `_c` de
   `test_hoja_de_ruta` como `simular_cierre.py` y, además, las comprobaciones de
   `test_project_state` (secciones, rama, tope de 25.000 bytes) sobre el texto en memoria. Pido tu
   conformidad.

Espero tu respuesta a la PARADA.

### 1.h Respuesta del consultor a la PARADA (2026-10-18)

Copiada tal cual (también al final de `docs/encargos/trabajo-visor-construccion.md`):

> Modelo: Opus 5.5 · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA de la fase 0 de trabajo/visor-construccion (2026-10-18). Cópiala tal cual al final del encargo y en VISOR-CONSTRUCCION.md, y aplícala punto por punto con la skill fase-cero.
>
> 0. Los tres días de P2: los que recomiendas, 2026-01-29 11-15 (venta, 52 puntos), 2026-08-20 11-15 (compra, 36) y 2026-01-08 07-11 (compra, 21). Por qué: siguen desde R3.1, tienen la Δentrada más grande y no pintan H4 de marzo ni de junio. 2026-07-02 11-15 no entra.
>
> 1. La traza por cierre: (a), traza_por_cierre.py. Por qué: sin ella no se sabe qué regla prohibió en cada cierre. Condiciones: el guion solo LEE el Evento de cada cierre y no cambia ninguna decisión del motor; si sus órdenes no son las de «### Ordenes» de main para ese día, PARADA. Si la guardia lo niega por código sin revisar, PARADA: no se rodea.
>
> 2. Cómo se mira una página: (a), extraer_pagina.py. La sesión no abre el HTML entero. Por qué: así no ve horas ni precios de días anteriores, en lugar de depender de no copiarlos.
>
> 3. Las 2 sesiones sin orden_dimensionada: (a). Se mira con la traza por qué RN-004 no produjo la toma de liquidez en cada cierre (qué pivote y qué lectura de «formado»). La conclusión es R (A-35, ya en V) salvo que se vea un error de código. Los heredados 25 y 30 quedan vivos y no se tocan. La premisa de mi encargo y de mi respuesta a la PARADA 4 de R3.1 (punto 2: «RN-011 no dimensiona con los hechos del camino producidos») era falsa: el hecho que falta es liquidez_tomada. Ver punto 8.
>
> 4. Los rechazos por precio_invalido: (a). Se miran 2026-07-08 11-15 y 2026-07-13 11-15, que siguen de R3.1, más 2026-01-08 07-11, 2026-08-07 07-11 y 2026-04-27 07-11. 2026-04-16 07-11 se cita como «ya no rechaza», con lo que hace hoy, sin página. Las de julio pintan H4 de junio: contexto_h4.py antes de generar su página, por recuento y pertenencia, y declarado en la fila.
>
> 5. «Anterior al día dev»: (a), por la fecha UTC de la vela. Nada anterior a las 00:00Z de la fecha del caso entra al informe ni a los anexos, aunque sea del día operativo. Por qué: es el precedente de R3.1.
>
> 6. Lo que el repo pide y el encargo no decía: (a). Tres líneas más de deuda, todas como propuestas para Technical Debt, sin tocar código:
>    - que el visor enseñe las H4 saltadas por color (ADR-0080 §10, que lo dejó para O);
>    - que el visor también lee el M1 de marzo y junio en cada make check (test_visor.py);
>    - que --hasta no recorta las H4, las listas por sesión ni el resumen del bróker (VISOR-DIAS.md).
>    En las líneas de cierre, las preguntas nuevas van también a R4.1 («Qué es»), y la línea de Estado de R3.2 explica la conclusión «correcto».
>
> 7. El guion de cierre simulado: conforme, con test_hoja_de_ruta y test_project_state (secciones, rama y tope de 25.000 bytes) sobre el texto en memoria.
>
> 8. Para la fila de ERRORES-RECURRENTES de esta rama, dos hallazgos del consultor, con su lección:
>    - Consultor, PARADA 4 de R3.1, punto 2: leí «no se produjo un hecho del camino» (§4.6) como «RN-011 no dimensiona». Lección: al clasificar, citar el hecho que falta por su nombre (el embudo lo da), no la regla que se supone detrás.
>    - Consultor, encargo de esta rama: puse como hechos dos cosas del visor que venían de un auditor sin medirlas: que la página solo enseña la caja final y que --depuracion da una traza (h1 y h2). Lección: lo que un auditor dice de cómo funciona un mecanismo entra en el encargo como «verifica que…», nunca como hecho (regla de oro 1 del consultor).
>
> Además:
> - 2026-07-01 11-15: la traza dice en qué cierre prohíbe RN-001 y si lo que corta son los cartuchos agotados (RN-016) o el minuto de ventana_fin. Las 4 sesiones con detenido_por_cartuchos:si van al informe como dato: el lote limitado de ADR-0081 gasta cartuchos que antes no se gastaban. Si eso cambia la conclusión de alguna sesión de las 14, se dice.
> - Las dos columnas en USD de «### Ordenes» no se copian, como propones.
>
> Lo que sigue: la fase 1 (la fila de exposiciones antes de la primera página; los cuatro guiones a anexos; las comprobaciones sesión por sesión) y la fase 2, sin parar, salvo que la traza no reproduzca la corrida de main, que la guardia niegue un guion o que contexto_h4.py encuentre una H4 en un día con caso reservado. En cualquiera de esos casos, PARADA.
>
> Rama lista para revisión, NO cerrada.

**Aplicación punto por punto (en curso):** 0 → los tres días de P2 entran en la fase 1; 1 → el
guion de traza; 2 → el extractor; 3 → las 2 sesiones por la traza de RN-004; 4 → los cinco rechazos
y 2026-04-16 sin página; 5 → la regla de la fecha UTC en `comun_visor.antes_del_dia`; 6 → las tres
deudas y las líneas del cierre; 7 → el guion de cierre simulado; 8 → la fila de ERRORES-RECURRENTES
en el cierre; «Además» → 2026-07-01 11-15 por la traza y las 4 sesiones con los cartuchos agotados.

## 2 · Fase 1 · Las comprobaciones en el visor (2026-10-18)

### 2.a Antes de la primera página: `contexto_h4.py`, y la PARADA 2

La fila de exposiciones del 2026-10-18 se escribió antes de leer ninguna vela. Los dos primeros
ficheros de `docs/validation/anexos/VISOR-CONSTRUCCION/`:
- `comun_visor.py`: construye el motor cableado y prepara UN día exactamente como `motor visor
  --simular --caso` con las opciones de la corrida 2 (las mismas llamadas que `cli.motor_visor`,
  :2478-2557); y la puerta de lo que se imprime (`antes_del_dia`: nada anterior a las 00:00Z de la
  fecha del caso; punto 5).
- `contexto_h4.py`: antes de cada página, por recuento y por pertenencia a `casos_ocultos` y a los
  meses reservados enteros, si las H4 de contexto o el M1 de la ventana caen en un día oculto. No
  imprime ninguna fecha, hora ni precio.

Comando, sobre los 20 días de la fase 1 (P2: 01-08, 01-29, 08-20; las 14 sin orden; las 2 sin
`orden_dimensionada`; los cinco rechazos):

    uv run python docs/validation/anexos/VISOR-CONSTRUCCION/contexto_h4.py caso-eurusd-2026-01-08 caso-eurusd-2026-01-29 caso-eurusd-2026-01-30 caso-eurusd-2026-04-17 caso-eurusd-2026-04-27 caso-eurusd-2026-07-01 caso-eurusd-2026-07-08 caso-eurusd-2026-07-09 caso-eurusd-2026-07-13 caso-eurusd-2026-07-14 caso-eurusd-2026-07-16 caso-eurusd-2026-08-03 caso-eurusd-2026-08-07 caso-eurusd-2026-08-11 caso-eurusd-2026-08-14 caso-eurusd-2026-08-19 caso-eurusd-2026-08-20 caso-eurusd-2026-08-21 caso-eurusd-2026-08-25 caso-eurusd-2026-08-27

Salida en `anexos/VISOR-CONSTRUCCION/contexto_h4.txt` (código de salida 2). Lo que dice:
- **Las 20 páginas pintan 8 H4 de contexto, 5 de ellas de antes del día** (las del sesgo nunca van
  más atrás que las 8 mínimas en estos días), **y entre 51 y 120 velas M1 de antes de las 00:00Z**
  (la ventana empieza a las 00:00 del trader, que con la rejilla es el día UTC anterior): esto vale
  para todos los días, no solo para los primeros del mes.
- **19 días: 0 velas en un día oculto o en un mes reservado.** 2026-08-03 pinta 4 H4 de julio, sin
  ningún día oculto.
- **2026-07-01: PARADA.** Su página pintaría 5 H4 y 118 M1 del día UTC anterior, y ese día está
  oculto. Una comprobación de pertenencia por huella (un guion de la carpeta de trabajo que solo
  imprime «sí» o «no»: `holdout.huella_de_caso` contra `retirados.yaml`) dice que es el día que
  HOLDOUT-EXPOSICIONES ya declaró el 2026-10-14 (hallazgo a1 del revisor de R3.1) y que salió del
  holdout por ADR-0041 ese día: retirado, no medido. No es información nueva sobre ningún día que
  mida. La página de 2026-07-01 no se ha generado.

**PARADA 2.** La respuesta del consultor manda PARADA si `contexto_h4.py` encuentra una H4 en un día
con caso reservado, y aquí la encuentra, aunque sea el día ya retirado. 2026-07-01 11-15 es una de
las 14 sesiones sin orden, y la del «Además» (si RN-001 corta por los cartuchos o por `ventana_fin`).

## Lo que necesito que decidas (PARADA 2)

0. **2026-07-01 11-15 sin su página.** Opciones: (a) esa sesión se comprueba SOLO con
   `traza_por_cierre.py`, que corre el mismo motor y no imprime nada anterior a las 00:00Z del 1 de
   julio, y sin página (el «gráfico» de esa sesión queda como el comando del visor que V no debe
   abrir sin decidirlo); (b) se genera la página igual, porque el día es el retirado y no mide, y la
   sesión la lee solo con `extraer_pagina.py`; (c) 2026-07-01 11-15 sale de esta rama. Recomiendo
   (a): la traza da lo que la comprobación necesita (qué regla prohíbe en cada cierre, cartuchos o
   ventana) y no pinta nada del día retirado; ADR-0041 dice que un retirado sigue oculto. Coste de
   (a): V no tendrá página de esa sesión para el cuestionario.
1. **Los otros 19 días.** Opciones: (a) sigo con ellos ya (fase 1 y fase 2), con las páginas y los
   guiones; (b) espero tu respuesta para todo. Recomiendo (a): `contexto_h4.py` los da limpios, y la
   decisión 0 no les afecta. Coste: ninguno; si la respuesta a 0 lo pide, 07-01 se añade después.

Espero tu respuesta a la PARADA 2.

## Estado

EN CURSO · PARADA 2 (2026-10-18): `contexto_h4.py` encontró que la página de 2026-07-01 pintaría velas del día ya retirado por ADR-0041; esa página no se generó. Se espera la respuesta del consultor.
