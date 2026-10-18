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
    trató por su fecha UTC una H4 del último día de junio como de un día de junio, y
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
| `precio_invalido`: el bid o el ask del instante | ningún sitio: la página pinta M1 | **guion de ticks** (`ticks_del_rechazo.py`): lee el mercado del día dev por la compuerta (`simulacion.mercado_de_construccion`, sin nombrar `data/manifests/ticks`: la guardia niega un guion que lo nombre, G.1) y da el último tick anterior al instante de cada orden rechazada (bid, ask), junto al precio de la orden; solo el día dev. **6 de los 26 rechazos caen en una de las 18 horas sin ticks** [corrección de la fase 1: es una cota inferior; la orden del primer cierre de la ventana también va con el respaldo M1, §2.g y §4.3 punto 6] (CORRIDA-CONSTRUCCION.md §1.e: 2026-04-06 10Z, 04-07 10Z, 04-22 10Z, 07-10 05Z dos veces, 08-17 11Z; auditor, punto 4): ahí el bróker tomó el cierre de la M1 más el spread supuesto (`llenado.py:96-112`), y el guion lo da igual y lo marca «respaldo M1» |
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

**Aplicación punto por punto** (dónde está cada uno, en §5): 0 → los tres días de P2 entran en la fase 1; 1 → el
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

### 2.b Respuesta del consultor a la PARADA 2 (2026-10-18)

Copiada tal cual (también al final de `docs/encargos/trabajo-visor-construccion.md`):

> Modelo: Opus 5.5 · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA 2 de trabajo/visor-construccion (2026-10-18). Cópiala tal cual al final del encargo y en VISOR-CONSTRUCCION.md, y aplícala con la skill fase-cero.
>
> 0. La sesión 2026-07-01 11-15: (a). Se comprueba solo con traza_por_cierre.py, sin generar su página, y la traza no imprime nada anterior a las 00:00Z del 1 de julio. Por qué: la comprobación (qué gate prohíbe en cada cierre y si RN-001 corta por los cartuchos o por ventana_fin) la da la traza entera; la página solo añadiría pintar velas de un día retirado, y no se abre material oculto cuando no hace falta, aunque ya esté fuera del holdout. Que el motor lea el M1 de junio para calentar ya está declarado en la fila de la fase 1. En el informe va «sin página: su contexto pintaría un día oculto (contexto_h4.py)», y en las líneas del cierre, que V no tendrá página de esa sesión. Si V la necesita para el cuestionario, se hará con un esquema dibujado, como la contradicción del sesgo (SESGO-H4-COLOR.md §4.4).
>
> 1. Los otros 19 días: sigue con ellos ya, con sus páginas y los guiones, en las fases 1 y 2. contexto_h4.py se corre antes de generar CADA página, no una vez para todas. Si en alguna sale un día oculto, se trata como el punto 0, sin parar, y se dice en el informe.
>
> Además:
> - Las páginas pintan entre 51 y 120 velas M1 de antes de las 00:00Z, y V las abrirá en el navegador. Que contexto_h4.py haya dado «no» para esos 19 días se escribe en la línea de Estado de R3.2, para que V sepa que esas páginas se pueden enseñar. Si un cambio posterior del visor o de la spec cambia lo que pintan, hay que volver a comprobarlas con contexto_h4.py antes de enseñarlas.
> - Lo de esta PARADA va a la fila de ERRORES-RECURRENTES como acierto de la regla («contexto_h4.py antes de cada página»), no como error.
>
> Lo que sigue: las fases 1 y 2 sin parar, salvo lo que ya manda PARADA: que la traza no reproduzca la corrida de main o que la guardia niegue un guion.
>
> Rama lista para revisión, NO cerrada.

**Aplicación punto por punto:** 0 → 2026-07-01 se mira solo con la traza y su página no se genera
(`dias/2026-07-01.pagina.txt` dice «sin página: su contexto pintaría un día oculto
(contexto_h4.py)»); 1 → `contexto_h4.py` corre antes de CADA página, dentro de `revisar_dia.py`, y
ningún otro día dio un día oculto (§2.c); «Además» → la línea de Estado de R3.2 y la fila de
ERRORES-RECURRENTES, en §4. Ninguna PARADA nueva: la traza reprodujo la corrida de `main` en los 20
días y la guardia no negó ningún guion (sí negó cuatro comandos compuestos de la sesión, que se
partieron en llamadas sueltas sin cambiar lo que hacían: §2.c).

### 2.c Cómo se corrió cada día

Un guion por día, `anexos/VISOR-CONSTRUCCION/revisar_dia.py`, en el orden que manda la respuesta a
la PARADA 2:

1. `contexto_h4.py <caso>`. Si sale distinto de 0, la página NO se genera.
2. La página, con el comando de la corrida 2, a `data/visor/visor-construccion/` (fuera de git):

       uv run botsito motor visor --simular --diagnostico-a35 cierre_vela_contraria --diagnostico-a44 sin_tope --diagnostico-cuenta-diaria --caso caso-eurusd-AAAA-MM-DD --salida data/visor/visor-construccion

   (el guion llama a `botsito.cli.main` con esa misma lista de argumentos).
3. `extraer_pagina.py <página> --sin-hechos`: lo del día dev de la página, a `dias/<fecha>.pagina.txt`.
4. `traza_por_cierre.py <caso> --rn004 --gates`: la traza por cierre, a `dias/<fecha>.traza.txt`;
   PARA con código 3 si sus órdenes no son las de «### Ordenes» de `main`.
5. `ticks_del_rechazo.py <caso>`: los rechazos por `precio_invalido` frente al bid y el ask, a
   `dias/<fecha>.ticks.txt`.

Los 20 días, en dos lotes en segundo plano (cada uno, un proceso):

    uv run python docs/validation/anexos/VISOR-CONSTRUCCION/revisar_dia.py caso-eurusd-2026-01-08 caso-eurusd-2026-01-29 caso-eurusd-2026-01-30 caso-eurusd-2026-04-17 caso-eurusd-2026-04-27 caso-eurusd-2026-07-01 caso-eurusd-2026-07-08 caso-eurusd-2026-07-09 caso-eurusd-2026-07-13 caso-eurusd-2026-07-14 --dias docs/validation/anexos/VISOR-CONSTRUCCION/dias --paginas data/visor/visor-construccion
    uv run python docs/validation/anexos/VISOR-CONSTRUCCION/revisar_dia.py caso-eurusd-2026-07-16 caso-eurusd-2026-08-03 caso-eurusd-2026-08-07 caso-eurusd-2026-08-11 caso-eurusd-2026-08-14 caso-eurusd-2026-08-19 caso-eurusd-2026-08-20 caso-eurusd-2026-08-21 caso-eurusd-2026-08-25 caso-eurusd-2026-08-27 --dias docs/validation/anexos/VISOR-CONSTRUCCION/dias --paginas data/visor/visor-construccion

Lo que dijeron, día a día (la salida de los dos lotes, en `anexos/VISOR-CONSTRUCCION/lotes.txt`):
- **«ORDENES frente a «### Ordenes» de main: iguales» en los 20 días.** El visor con `--caso`
  reproduce la corrida 2, como decía §1.a.
- **`contexto_h4.py` dio «ok» en 19 días y PARADA en 2026-07-01**, el de la PARADA 2: su página no
  se generó. En los 19, 0 velas en un día oculto o un mes reservado.
- **Los anexos salen de estos comandos, con los guiones tal como se commitean:** una pasada de los
  dos lotes, después del último cambio de los guiones de traza, dio los mismos `sha256` en los 84
  ficheros de `dias/` y en `lotes.txt`; y `reentradas.py`, `listas.py`, `resumen_gates.py` y los
  cuatro `--velas`, vueltos a correr, dan los mismos bytes que sus salidas guardadas. Tras el
  hallazgo a1 del revisor (`revisar_dia.py` sacaba de su propia ruta dónde escribir), las carpetas
  de salida llegan por `--dias` y `--paginas`, y la pasada final se hizo con las dos FUERA del
  repositorio (en la carpeta de trabajo de la sesión): §8, lo que se hizo con a1.

Además, tres comandos sueltos (el mismo guion de traza con `--velas`, que imprime las M1 del día dev
que empiezan en un tramo UTC), para ver dónde estaba el 0 del trader en los días de P2:

    uv run python docs/validation/anexos/VISOR-CONSTRUCCION/traza_por_cierre.py caso-eurusd-2026-01-29 --sesion 11-15 --velas 12:56-13:02
    uv run python docs/validation/anexos/VISOR-CONSTRUCCION/traza_por_cierre.py caso-eurusd-2026-08-20 --sesion 11-15 --velas 10:44-11:01
    uv run python docs/validation/anexos/VISOR-CONSTRUCCION/traza_por_cierre.py caso-eurusd-2026-01-08 --sesion 07-11 --velas 08:00-08:22

(salidas en `dias/<fecha>.velas-trader.txt`), y uno más para la toma previa de 2026-01-08 (§2.f),
con salida en `dias/2026-01-08.velas-toma.txt`:

    uv run python docs/validation/anexos/VISOR-CONSTRUCCION/traza_por_cierre.py caso-eurusd-2026-01-08 --sesion 11-15 --velas 09:44-10:01
 Y dos guiones que solo leen salidas ya escritas:
`reentradas.py` (sobre «### Ordenes» de `main`; §2.d) y `resumen_gates.py` (sobre las trazas;
§2.e).

**Lo que la guardia negó, y cómo se hizo:** cuatro comandos de la sesión, ninguno un guion: una
variable de entorno `F=` con el nombre de la salida, un `for f in …` sobre tres trazas, un `date`
detrás de un `ls`, y la ejecución de un guion en el mismo comando que su `sed -i`. Cada uno se partió
en llamadas sueltas, con el nombre del fichero literal, como dice su mensaje; ninguno cambió lo que
se medía. No hay hallazgo de guardia.

**Cómo se lee la traza.** Cada cierre de M1 es un instante; la vela que cierra en `t` empieza en
`t − 1 min`. Las horas van en UTC y, entre paréntesis, en el reloj del trader (Europe/Madrid). Una
orden «colocada hh:mm:59Z» se coloca en el cierre de `hh:mm+1`. «Antes del día» tapa todo lo
anterior a las 00:00Z de la fecha del caso; ninguna vela, hora ni precio de antes entra en este
informe.

**La regla del pivote que se comprueba** (el «punto» de ADR-0064): `ultimo_punto_de_ruptura`
(`domain/estructura_m1.py:189-212`) toma el último pivote de M1 contrario a la entrada, formado con
`CIERRE_VELA_CONTRARIA` (`domain/pivotes_m15.py:76-121`): una vela de color contrario cierra tras una
racha de velas del otro color, y el nivel es el extremo de ESA racha (el máximo en una compra, el
mínimo en una venta), sin contar la vela contraria. Una vela sin cuerpo no es de ningún color y corta
la racha (ADR-0076 §2). El 0 de la caja es ese nivel, y el punto se identifica por el nivel y el
inicio de la vela contraria (`zonas.py:352-403`). Con `caja_se_fija = en_cada_cierre_m1`
(ADR-0074 §1), cada 1 nuevo del mismo punto es una zona nueva con el mismo 0.

### 2.d P2: el 0 de la caja, en los tres días que eligió el consultor

#### 2026-01-29 11-15 (venta, Δentrada 52)

Página: `dias/2026-01-29.pagina.txt`. Traza: `dias/2026-01-29.traza.txt` y
`dias/2026-01-29.velas-trader.txt`.

- **Sesgo y toma:** RN-003 fija `sesgo=bajista` a las 10:00Z (11:00 del trader); RN-004 fija
  `liquidez_tomada` a las 12:51Z (13:51): el alto de M15 de 1.19518, formado a las 12:45Z (13:45).
- **Las órdenes del bot:**

  | orden | colocada | 0 | 1 | punto (nivel @ vela contraria) | resultado |
  |---|---|---|---|---|---|
  | o16 | 12:53:59Z (13:53:59) | 1.19549 | 1.19566 | 1.19549 @ 12:53Z | llenada 12:54:12Z |
  | o17 | 12:54:59Z (13:54:59) | 1.19549 | 1.1959 | 1.19549 @ 12:53Z | llenada 12:55:00Z |
  | o18 | 12:56:59Z (13:56:59) | 1.1954 | 1.19593 | 1.1954 @ 12:56Z | cancelada |
  | o19 | 12:57:59Z (13:57:59) | 1.1954 | 1.1961 | 1.1954 @ 12:56Z | cancelada |

- **El 0 sale del pivote que dice la spec.** La vela de las 12:52Z (13:52) es roja (abre 1.1956,
  cierra 1.19549, mínimo 1.19549), la de las 12:51Z es verde y la de las 12:53Z es verde: la racha
  roja es solo la de las 12:52Z, y su mínimo, 1.19549, es el pivote bajo que forma la vela contraria
  de las 12:53Z. Ese es el 0 de o16 y o17. El de o18 y o19 es el mínimo de la vela roja de las 12:55Z
  (1.1954), que forma la verde de las 12:56Z. El 0 no se mueve dentro de un punto; el 1 sí: el
  máximo de las velas desde la que marca el punto hasta la última cerrada (1.19566 con la de las
  12:52Z y las 12:53Z; 1.1959 con la de las 12:54Z). Es lo que dicen ADR-0064 §2 y ADR-0074 §1.
- **Pero o17 vuelve a colocar el punto de o16 después de que o16 se llenara.** o16 se llena a las
  12:54:12Z; su stop (1.19563) queda dentro de la vela de las 12:54Z (máximo 1.1959); en el cierre
  siguiente RN-011 liga una zona NUEVA del mismo punto, con el 1 nuevo, y o17 se coloca y se llena.
  ADR-0064, decisión 1: «Un punto ya usado no se vuelve a colocar. Usado es con la orden enviada,
  aceptada o rechazada.» Y ADR-0074 §1 recalcula el 1 «hasta el llenado». Ver 2.d.4.
- **El 0 del trader:** vende a las 14:01:15 de su reloj (13:01:15Z) en 1.19601, con el stop en
  1.19616. La vela de las 12:58Z es roja (mínimo 1.19603) y la de las 12:59Z es verde: con la regla
  del bot, eso es un pivote bajo de 1.19603, formado en el cierre de las 13:00Z, 2 puntos por encima
  de la entrada del trader. **Y el bot lo vio:** de 13:00Z a 13:01Z su zona tiene el 0 en 1.19603
  (`gates` de la traza), pero RN-009 la prohíbe: desde las 12:59Z hay 2 zonas de control contadas
  desde la toma, y el tope es 1 (ADR-0076 §2 fija que se cuentan tras la toma). RN-005 no prohíbe
  (el 0 está por encima de la toma, el lado de la operativa bajista).
- **Conclusión: el 0, correcto. La Δ de 52 puntos es de regla:** el bot entra en el primer pivote
  tras la toma, y el trader en uno posterior que el bot ve y RN-009 prohíbe. Va a V con la
  pregunta 8 (§3.2). La reentrada en el punto de o16 es **E** (2.d.4).

#### 2026-08-20 11-15 (compra, Δentrada 36)

Página: `dias/2026-08-20.pagina.txt`. Traza: `dias/2026-08-20.traza.txt` y
`dias/2026-08-20.velas-trader.txt`.

- **Sesgo y toma:** `sesgo=alcista` a las 09:00Z (11:00); `liquidez_tomada` a las 10:46Z (12:46).
- **Las órdenes del bot:**

  | orden | colocada | 0 | 1 | punto | resultado |
  |---|---|---|---|---|---|
  | o10 | 10:48:59Z (12:48:59) | 1.17012 | 1.16996 | 1.17012 @ 10:48Z | cancelada (RN-006) |
  | o11 | 10:49:59Z (12:49:59) | 1.17012 | 1.16994 | 1.17012 @ 10:48Z | llenada (12:50:01 del trader) |
  | o12 a o15 | 10:50:59Z a 10:53:59Z | 1.17007 | de 1.16991 a 1.16949 | 1.17007 @ 10:50Z | canceladas |
  | o16 | 11:47:59Z (13:47:59) | 1.16865 | 1.1685 | 1.16865 @ 11:47Z | cancelada |
  | o17 | 11:48:59Z (13:48:59) | 1.16865 | 1.16834 | 1.16865 @ 11:47Z | llenada (13:49:09 del trader) |
  | o18 | 11:51:59Z (13:51:59) | 1.16869 | 1.16833 | 1.16869 @ 11:50Z | cancelada |

- **El 0 sale del pivote que dice la spec.** La vela de las 10:47Z es verde (máximo 1.17012), la de
  las 10:46Z roja y la de las 10:48Z roja: el pivote alto es 1.17012, el 0 de o10 y o11. o10 se
  cancela y o11 la sustituye con el 1 nuevo, sin llenarse antes: es la reubicación de ADR-0074, no una
  reentrada. Lo mismo con o12 a o15 (punto 1.17007) y con o16 y o17 (punto 1.16865). **o17 forma
  pareja con la segunda compra del trader** (13:49:10, 1.16868; «pareja 1» en la página).
- **El 0 del trader:** compra a las 13:00:00 de su reloj (11:00:00Z) en 1.16976, con el stop en
  1.1696. Las velas de las 10:54Z y las 10:55Z son verdes (máximo 1.16974) y la de las 10:56Z roja:
  con la regla del bot, pivote alto de 1.16974, formado en el cierre de las 10:57Z, 2 puntos por
  debajo de la entrada del trader; la vela de las 11:00Z lo rompe (máximo 1.16981). **Y el bot lo
  vio:** de 10:57Z a 11:00Z su zona tiene el 0 en 1.16974, pero RN-009 la prohíbe (2 zonas de control
  desde las 10:55Z, 3 desde las 11:00Z).
- **Conclusión: el 0, correcto; la Δ de 36 puntos, de regla**, igual que el 29 de enero: el trader
  entra en un pivote posterior que el bot ve y RN-009 prohíbe. Pregunta 8 (§3.2).

#### 2026-01-08 07-11 (compra, Δentrada 21)

Página: `dias/2026-01-08.pagina.txt`. Traza: `dias/2026-01-08.traza.txt` y
`dias/2026-01-08.velas-trader.txt`.

- **Sesgo y toma:** `sesgo=alcista` a las 06:00Z (07:00); `liquidez_tomada` a las 06:28Z (07:28), y
  una toma nueva del bajo de M15 de 1.16774 desde las 08:01Z (09:01), que abre otro escenario.
- **Las órdenes del bot:**

  | orden | colocada | 0 | 1 | punto | resultado |
  |---|---|---|---|---|---|
  | o1 | 08:04:59Z (09:04:59) | 1.16757 | 1.16748 | 1.16757 @ 08:04Z | rechazada, `precio_invalido` (2.g) |
  | o2 | 08:06:59Z (09:06:59) | 1.16767 | 1.16755 | 1.16767 @ 08:06Z | cancelada (RN-006) |
  | o3 | 08:07:59Z (09:07:59) | 1.16767 | 1.16744 | 1.16767 @ 08:06Z | llenada (09:08:57 del trader) |

- **El 0 sale del pivote que dice la spec.** o1: la vela de las 08:03Z es verde (máximo 1.16757) entre
  dos rojas (08:02Z y 08:04Z). o2 y o3: la de las 08:05Z es verde (máximo 1.16767) y la de las 08:06Z
  roja. o3 sustituye a o2 sin llenado previo: reubicación.
- **El 0 del trader:** compra a las 09:21:25 de su reloj (08:21:25Z) en 1.16746, con el stop en
  1.16739. La vela de las 08:16Z es verde (máximo 1.16746); las de las 08:17Z y las 08:18Z no tienen
  cuerpo (abren y cierran en el mismo precio; máximo 1.16745 y 1.16746); la de las 08:19Z es roja; la
  de las 08:21Z rompe 1.16746 (máximo 1.16754). Con la regla del bot, **ahí no hay pivote**: la vela
  sin cuerpo corta la racha y la roja de las 08:19Z no tiene racha verde justo antes (ADR-0076 §2:
  «un doji no es de ningún color, no es contraria y corta la racha: no forma pivote»). El trader
  pone el 0 justo en ese máximo. A esa hora el bot tenía su zona en otro punto (0 1.16787) y la
  prohibían RN-005 y RN-009 (`gates`, 08:15Z a 08:22Z).
- **Conclusión: el 0 del bot, correcto; la Δ de 21 puntos, de regla:** el trader marca un punto de
  breaker en una racha con velas sin cuerpo, que la regla del bot no reconoce. Va a V como pregunta
  nueva, junto a la 4 (§3.2).

#### 2.d.4 La reentrada en un punto ya llenado: E

Lo que se ve en 2026-01-29 11-15 (o16 → o17) pasa también en 2026-07-13 11-15: o11, o12 y o13
tienen el mismo punto (1.14301 @ la vela contraria de las 09:36Z) y **las tres se llenan**
(`dias/2026-07-13.traza.txt`).

**Por qué, en el código:** `toca_colocar_orden_limite` (`engine/zonas.py:469-475`) niega una zona
si ya está usada (`zonas_usadas`) o si su PUNTO fue rechazado (`punto_rechazado`). Pero «usada» se
apunta por ZONA (`marcar_usada`, `zonas.py:418-420`, llamado en `primitivas_broker.py:635` y :650), y
con `en_cada_cierre_m1` cada 1 nuevo es una zona nueva del mismo punto (`zonas.py:381-401`). Así,
tras un llenado, el cierre siguiente con un 1 distinto da una zona «sin usar» del mismo punto, y se
coloca. El rechazo sí se apunta por punto (`marcar_rechazada`, :404-410); el llenado, no.

**Lo que dice la decisión:** ADR-0064, decisión 1 («Un punto ya usado no se vuelve a colocar. Usado
es con la orden enviada, aceptada o rechazada»), que ADR-0066 no enmienda (enmienda las decisiones
2 y 3: tras una pérdida, la misma liquidez sigue dando intentos, que no es el mismo punto; y la
orden pendiente entre sesiones), y
ADR-0074 §1 (el 1 se recalcula «hasta el llenado»). El docstring del módulo dice lo mismo
(`zonas.py:41-42`). El código hace otra cosa.

**Cuántas veces, en la corrida 2 de `main`:** `reentradas.py`, sobre «### Ordenes» de la diaria
(salida en `anexos/VISOR-CONSTRUCCION/reentradas.txt`):

    uv run python docs/validation/anexos/VISOR-CONSTRUCCION/reentradas.py

    ordenes en el 0 de una orden ya llenada de su sesion: 47, en 22 sesiones; de ellas, llenadas: 16

Es un recuento por el PRECIO de la orden (el 0, que es el nivel del punto) colocada DESPUÉS del
llenado de otra de su sesión en ese mismo 0, así que es una COTA SUPERIOR: un pivote nuevo al mismo
nivel también cuenta. Hay al menos un caso que casi seguro lo es: en 2026-01-05 07-11, o5 se coloca
a las 09:27:59Z en el 0 de o3, que se llenó a las 06:04:22Z, más de tres horas antes (hallazgo b2 del
revisor). El punto exacto (nivel e instante de la vela contraria) solo lo da la traza, y es el mismo
en las tres sesiones de las trazas de esta rama que aparecen en la lista: 2026-01-29 11-15 (o17 en
el punto de o16, llenada), 2026-07-13 11-15 (o12 y o13 en el de o11, llenadas las tres) y 2026-01-29
07-11 (o3 y o4 en el punto de o2, ya llenada; las dos canceladas por RN-006). Dos de las cuatro sesiones con `detenido_por_cartuchos:si` están en la lista (2026-07-13 11-15
y 2026-08-26 07-11): las reentradas gastan cartuchos.

**Conclusión: E.** El código no hace lo que dice ADR-0064, decisión 1. Afecta a P5 de R3.1 («el bot
se para en uno o dos minutos y vuelve a entrar», clasificado R con destino V, pregunta 3): parte de
esas reentradas son este error, no una regla desconocida. La pregunta 3 sigue: si el trader reentra
en el mismo nivel tras un stop, lo dirá, y entonces cambiará el ADR, no el código solo.

### 2.e Las 14 sesiones sin orden: RN-005, RN-009 y RN-001, cierre a cierre

`traza_por_cierre.py --gates` apunta en cada cierre el valor de los tres predicados de gate y lo que
los decide: RN-005 (`se_desarrolla_en_el_lado_de_ruido`: el lado y el 0 de la zona que ve el motor
en ese cierre frente al nivel de la toma), RN-009 (`zonas_desarrolladas_superan`: cuántas zonas de
control hay desde la toma, con `domain/estructura_m1.zonas_de_control`, frente al tope 1) y RN-001
(`en_ventana` y los `detenido_por_*` fijados). `resumen_gates.py` cuenta los cierres de cada sesión
por combinación, con el primero de cada una (salida en `anexos/VISOR-CONSTRUCCION/resumen_gates.txt`):

    uv run python docs/validation/anexos/VISOR-CONSTRUCCION/resumen_gates.py 2026-01-30 07-11 2026-04-17 07-11 2026-04-27 11-15 2026-07-01 11-15 2026-07-09 07-11 2026-07-14 07-11 2026-07-14 11-15 2026-07-16 11-15 2026-08-03 07-11 2026-08-11 07-11 2026-08-19 11-15 2026-08-21 11-15 2026-08-25 07-11 2026-08-27 11-15 2026-07-01 07-11

| sesión | toma: primer cierre con zona | RN-005 SÍ desde | RN-009 SÍ desde | cierres tras la toma sin ningún gate | zonas de control, como mucho | RN-001 |
|---|---|---|---|---|---|---|
| 2026-01-30 07-11 | 07:32Z (08:32) | 07:32Z | 07:40Z (08:40) | 0 | 34 | no dispara |
| 2026-04-17 07-11 | 05:29Z (07:29) | 05:29Z | 05:43Z (07:43) | 0 | 40 | no dispara |
| 2026-04-27 11-15 | 10:16Z (12:16) | 10:16Z | 10:27Z (12:27) | 0 | 17 | 13:00Z (15:00), ventana |
| 2026-07-01 11-15 | 10:52Z (12:52) | 10:52Z | 10:59Z (12:59) | 0 | 32 | 09:00Z a 10:52Z, cartuchos; 13:00Z, ventana |
| 2026-07-09 07-11 | 07:44Z (09:44) | 07:44Z | 07:53Z (09:53) | 0 | 15 | no dispara |
| 2026-07-14 07-11 | 06:19Z (08:19) | 06:19Z | 06:30Z (08:30) | 0 | 26 | no dispara |
| 2026-07-14 11-15 | 09:19Z (11:19) | 09:19Z | 09:28Z (11:28) | 0 | 33 | 13:00Z (15:00), ventana |
| 2026-07-16 11-15 | 09:05Z (11:05) | 09:05Z | 09:11Z (11:11) | 0 | 23 | 13:00Z (15:00), ventana |
| 2026-08-03 07-11 | 05:47Z (07:47) | 05:47Z | 05:54Z (07:54) | 0 | 23 | no dispara |
| 2026-08-11 07-11 | 05:21Z (07:21) | 05:21Z | 05:34Z (07:34) | 0 | 21 | no dispara |
| 2026-08-19 11-15 | 09:02Z (11:02) | 09:02Z | 09:11Z (11:11) | 0 | 50 | 13:00Z (15:00), ventana |
| 2026-08-21 11-15 | 11:33Z (13:33) | 11:33Z | 11:44Z (13:44) | 0 | 9 | 13:00Z (15:00), ventana |
| 2026-08-25 07-11 | 06:15Z (08:15) | 06:15Z | 06:24Z (08:24) | 0 | 17 | no dispara |
| 2026-08-27 11-15 | 11:55Z (13:55) | 11:55Z | 12:05Z (14:05) | 0 | 15 | 13:00Z (15:00), ventana |

(En 2026-01-30 la hora del trader es UTC+1; en las demás, UTC+2.)

Lo que dice la tabla, sesión por sesión, con el mismo patrón en las 14:
- **Antes de la toma no hay zona** («sin zona o sin toma»): ningún gate tiene nada que prohibir y
  no hay nada que colocar.
- **En el cierre de la toma, RN-005 dice SÍ**: la primera zona tras la toma tiene el 0 al otro lado
  de la liquidez tomada (por encima en una compra, por debajo en una venta), que es el lado de ruido
  de RN-005 tal como lo escribe la spec («el precio se desarrolla por encima de la liquidez de M15 en
  sesgo alcista, o por debajo de ella en sesgo bajista»; `zonas.py:503-521`).
- **Entre 6 y 14 cierres después, RN-009 dice SÍ** con 2 zonas de control (tope 1). Las zonas se
  cuentan desde la toma del ESCENARIO vigente (ADR-0076 §2; `zonas.zonas_desarrolladas_superan` lee
  `_anotar_toma`, que da la toma del último escenario abierto), y **el recuento vuelve a 0 cada vez
  que RN-004 toma otra liquidez**, que abre un escenario nuevo (ADR-0066; la identidad de la
  liquidez es lado, nivel e instante de formación, `zonas.py:179-203`). Pasa 14 veces en 10 de las
  14 sesiones, y `resumen_gates.py` comprueba que **las 14 coinciden con una toma de RN-004 de otro
  pivote** en ese cierre o en el anterior (`resumen_gates.txt`, «el recuento de RN-009 vuelve a
  bajar»: ninguna «NINGUNA»). En 2026-08-11 07-11 el pivote nuevo tiene el MISMO nivel que el
  anterior (bajo 1.15402) pero se formó a otra hora (05:30Z frente a 05:00Z): para el motor es otra
  liquidez. Tras cada reinicio, ningún cierre queda sin gate: en los cierres tras la toma con RN-009
  en NO, RN-005 está en SÍ (no hay ninguna combinación «NO | NO» tras la toma). Esto lo corrige el
  hallazgo b1 del revisor: la primera redacción decía que el recuento «solo sube».
- **Tras la toma, 0 cierres sin un gate en SÍ** en las 14: la orden no se coloca nunca. Cuando RN-015
  pide colocarla, lo que la traza apunta es su acción `colocar_orden_limite` bloqueada por el efecto
  prohibido `abrir_operacion`.
- **RN-001 dispara en el cierre de `ventana_fin`** (15:00 del trader) en las 7 sesiones 11-15, con
  `en_ventana` en NO: el intervalo es medio abierto (RN-001, «incluye hasta el instante anterior a
  ventana_fin»), así que ese cierre ya está fuera. En las sesiones 07-11 no dispara: la ventana es
  continua de 07:00 a 15:00. **La excepción es 2026-07-01 11-15** (el «Además» del consultor): de
  09:00Z a 10:52Z (11:00 a 12:52) RN-001 dispara por `detenido_por_cartuchos=hasta_cartuchos_reinicio`,
  con `en_ventana` en SÍ: los cartuchos se gastaron por la mañana (2.h). En el cierre de las 10:52Z,
  la toma de una liquidez nueva reinicia los cartuchos (`cartuchos_reinicio =
  siguiente_liquidez_m15`, ADR-0066), y desde las 10:53Z ningún `detenido_por_*` está fijado; a las
  13:00Z dispara otra vez, por `ventana_fin`. **Que R3.1 dijera «por el minuto de `ventana_fin`»
  vale para 6 de las 7**; en 2026-07-01 11-15 RN-001 corta antes por los cartuchos, pero en esos
  cierres todavía no había toma ni zona, así que no cambia nada de lo que el bot habría hecho.

**Conclusión: correcto en las 14.** Cada gate prohíbe en el instante en que su condición, tal como
está escrita, se cumple; ninguna sesión tiene un cierre tras la toma en que el bot debiera colocar
y no lo hiciera. Si el trader entra en el lado de ruido o con más zonas de control es la pregunta 8
de V, que ya existe (§3.2); 2026-01-29 y 2026-08-20 (2.d) la ilustran mejor que estas 14, porque en
ellas el bot VE el 0 del trader y RN-009 lo prohíbe.

### 2.f Las 2 sesiones sin `orden_dimensionada`: por qué no hubo toma

Las dos con `--rn004` (`dias/2026-01-08.traza.txt` y `dias/2026-08-14.traza.txt`; páginas
`dias/2026-01-08.pagina.txt` y `dias/2026-08-14.pagina.txt`). La traza da, en cada cierre, el
valor de los tres predicados de RN-004 (`alcanza_nivel`, `cruza`, `la_toma_es_de_la_sesion`), el
pivote de M15 que es la liquidez en ese cierre (lado, nivel e instante en que quedó formado), y el
extremo de las M1 del tramo en el lado del pivote. Como dijo la fase 0 (§1.c), en las dos falta la
TOMA, antes de RN-011: no es RN-011 el que no dimensiona.

#### 2026-01-08 11-15 (sesgo bajista: la liquidez es un alto de M15)

| cierres | `alcanza_nivel` / `cruza` / `la_toma_es_de_la_sesion` | pivote | máximo de las M1 del tramo |
|---|---|---|---|
| 10:00Z a 10:29Z (11:00 a 11:29) | SÍ / SÍ / NO | alto 1.16753, formado 09:45Z (10:45) | 1.16817, en la M1 de 10:12Z |
| 10:30Z a 11:14Z (11:30 a 12:14) | NO | alto 1.16817, formado 10:30Z | 1.16804 |
| 11:15Z a 11:59Z (12:15 a 12:59) | NO | alto 1.16804, formado 11:15Z | 1.16793 |
| 12:00Z a 14:00Z (13:00 a 15:00) | NO | alto 1.16782, formado 12:00Z | 1.16779 |

- **Lo que pasa:** al abrir la sesión, el precio ya está por encima del alto de 1.16753, y
  `la_toma_es_de_la_sesion` dice NO porque ese alto ya se rompió con cuerpo ANTES de abrirla: la M1
  de las 09:54Z (10:54 del trader) abre en 1.16743 y cierra en 1.16755
  (`dias/2026-01-08.velas-toma.txt`). Fue en la sesión 07-11, cuyo sesgo era alcista. ADR-0066 y A-46 («cada sesión es un mundo diferente»): una liquidez
  tomada en una sesión anterior del día no cuenta para esta (`primitivas.py:266-296`). Después, cada
  alto de M15 nuevo queda por encima de todo lo que hace el precio: máximos más bajos toda la tarde,
  y ninguna toma.
- **¿Es la lectura de A-35?** No solo: la corrida `a35-inicio` de R3.1 (`--diagnostico-a35
  inicio_vela_contraria`, `anexos/CORRIDA-CONSTRUCCION/a35-inicio…txt`, línea «Por sesion» de
  2026-01-08 11-15) tampoco tiene `liquidez_tomada`, con el mismo sesgo bajista. Esa corrida es
  anterior a ADR-0080 y ADR-0081.
- **El trader:** vende a las 14:29:05 de su reloj (13:29:05Z) en 1.1675, con el stop en 1.16768.
- **Conclusión: R.** La regla se aplica como está escrita; lo que no sabemos es si el trader cuenta,
  para la segunda sesión, una toma que ocurrió en los últimos minutos de la primera, cuando el
  sesgo era el contrario. Pregunta nueva (§3.2, B).

#### 2026-08-14 07-11 (sesgo alcista: la liquidez es un bajo de M15)

| cierres | `alcanza_nivel` | pivote | mínimo de las M1 del tramo |
|---|---|---|---|
| 05:00Z a 06:44Z (07:00 a 08:44) | NO | bajo 1.15366, formado 04:45Z (06:45) | 1.15382, en la M1 de 05:01Z |
| 06:45Z a 08:44Z (08:45 a 10:44) | NO | bajo 1.15387, formado 06:45Z | 1.15408 |
| 08:45Z a 09:00Z (10:45 a 11:00) | NO | bajo 1.15502, formado 08:45Z | 1.1552 |

(el cierre de las 09:00Z, que abre la sesión 11-15, sale en las dos sesiones).

- **Lo que pasa:** el precio no llega nunca al bajo de M15 vigente: el mínimo de la sesión,
  1.15382, queda 16 puntos por encima del bajo de 1.15366. `alcanza_nivel` dice NO en los 241
  cierres; los otros dos predicados ni se evalúan. Sin toma no hay escenario ni zona (`gates`: «sin
  zona o sin toma» en toda la sesión).
- **¿Es la lectura de A-35?** No solo: la corrida `a35-inicio` de R3.1 tampoco tiene
  `liquidez_tomada` en 2026-08-14 07-11, con el mismo sesgo alcista.
- **El trader:** compra a las 08:30:10 de su reloj (06:30:10Z) en 1.15404, con el stop en 1.15388.
  El bot, con ADR-0045 («la liquidez es el pivote de M15 más reciente ya formado»), mira el bajo de
  1.15366 hasta las 06:45Z; el trader toma otra liquidez, que la traza no puede nombrar.
- **Conclusión: R.** Qué liquidez marcó el trader: pregunta 5 (§3.2), con este día.

### 2.g Los rechazos por `precio_invalido`

`ticks_del_rechazo.py` (dentro de `revisar_dia.py`; salidas en `dias/<fecha>.ticks.txt`) lee, para
cada orden rechazada, la cotización con la MISMA función que usó el bróker al rechazarla
(`Mercado.cotizacion`: el último tick anterior o igual al instante; donde no hay ticks, la última M1
más el spread supuesto, «respaldo_m1») y la regla del lado equivocado (`llenado.lado_equivocado`,
ADR-0057). La vela que marca cada 0 y sus vecinas salen de la traza.

| sesión | orden | colocada | el 0 | bid / ask (fuente) | el ask pasó el 0 por | la vela contraria que forma el pivote |
|---|---|---|---|---|---|---|
| 2026-07-08 11-15 | o3 compra | 11:42:59Z (13:42:59) | 1.13955 | 1.13954 / 1.13958 (ticks) | 3 puntos | la de las 11:42Z: roja, cierra en 1.13954, 1 punto por debajo del 0 |
| 2026-07-13 11-15 | o14 compra | 12:14:59Z (14:14:59) | 1.14223 | 1.14222 / 1.14224 (ticks) | 1 punto | la de las 12:14Z: roja, máximo 1.14228, cierra en 1.14222 |
| 2026-01-08 07-11 | o1 compra | 08:04:59Z (09:04:59) | 1.16757 | 1.16758 / 1.1676 (ticks) | 3 puntos | la de las 08:04Z: roja, abre en 1.16761, por encima del 0, y cierra en 1.16758 |
| 2026-08-07 07-11 | o1 compra | 05:34:59Z (07:34:59) | 1.15226 | 1.15223 / 1.15228 (ticks) | 2 puntos | la de las 05:34Z: roja, máximo 1.15228, cierra en 1.15223 |
| 2026-08-07 07-11 | o2 compra | 06:43:59Z (08:43:59) | 1.1522 | 1.1522 / 1.15225 (ticks) | 5 puntos | la de las 06:43Z: roja, cierra en 1.1522, en el 0 |
| 2026-04-27 07-11 | o1 compra | 04:59:59Z (06:59:59) | 1.17264 | 1.17268 / 1.17272 (respaldo_m1) | 8 puntos | la de las 04:55Z, antes de la ventana: la orden solo se pudo colocar en el primer cierre de la sesión, las 05:00Z, con el precio ya por encima |
| 2026-04-27 07-11 | o2 compra | 05:05:59Z (07:05:59) | 1.1727 | 1.1727 / 1.17273 (ticks) | 3 puntos | la de las 05:05Z: roja, abre en 1.17271, cierra en 1.1727, en el 0 |
| 2026-04-27 07-11 | o3 compra | 05:08:59Z (07:08:59) | 1.17275 | 1.17274 / 1.1728 (ticks) | 5 puntos | la de las 05:08Z: roja, máximo 1.17279, cierra en 1.17274 |

- **Dónde colocó el bot la orden frente al precio (ADR-0057):** en las 8, una STOP de compra en el
  0, con el ask ya por encima: el bróker la rechaza porque es del lado equivocado, como dice
  ADR-0057 y como prevé ADR-0064 («se coloca como STOP con el precio todavía al otro lado; si ya lo
  ha pasado, el bróker la rechaza»). El bróker hace lo que dice su regla.
- **Si la caja ya había quedado atrás:** sí, en las 8. Con la regla del pivote, el 0 es el máximo
  de la racha verde SIN la vela roja que la cierra; cuando esa roja es pequeña y cierra en el 0, a 1
  punto o por encima (o el pivote se formó antes de abrir la ventana), en el cierre en que el bot ve
  el punto el ask ya lo ha pasado, porque el ask es el bid más el spread (de 2 a 6 puntos en estas
  filas). Es la pregunta 9 de V.
- **El punto rechazado no se vuelve a colocar con otra caja (ADR-0064, decisión 1; ADR-0074):** se
  cumple en los cinco días. La traza lista los puntos rechazados de cada sesión y busca las órdenes
  NO rechazadas colocadas en uno de ellos (`traza_por_cierre.py`, el filtro `f[5] != "rechazada"`):
  no hay ninguna. Una recolocación rechazada otra vez no la vería ese filtro, pero tampoco la hay:
  los puntos rechazados de cada sesión son todos distintos (2026-04-27: 117264, 117270 y 117275;
  2026-08-07: 115226 y 115220; uno por sesión en los otros tres días). La primera redacción decía
  «cualquier orden posterior», más de lo que hace el guion (hallazgo b8 del revisor). El rechazo, a
  diferencia del llenado (2.d.4), sí se apunta por punto (`marcar_rechazada`).
- **Uno de los ocho se decidió con el respaldo M1:** o1 de 2026-04-27 («respaldo_m1»), aunque esa
  hora no es de las 18 sin ticks: la orden del primer cierre de la ventana lleva 1 ms antes del
  primer tick cargado (§4.3, punto 6). Corrige lo que la fase 0 daba por hecho (§1.d y la decisión
  4: «6 de los 26 rechazos caen en una de las 18 horas sin ticks», y 2026-04-27 como rechazo «con
  ticks reales»): el recuento de 6 es una cota inferior (hallazgo b3 del revisor).
- **2026-04-16 07-11 ya no rechaza**, sin página, como mandó el consultor. Hoy, en «### Ordenes» de
  `main`: o1 se coloca a las 06:07:59Z en 1.18025 y se llena a las 06:08:17Z; o2 y o3, en el mismo
  0, se cancelan; o4, en el mismo 0, se llena a las 06:11:29Z. Es una de las 22 sesiones de
  `reentradas.txt` (2.d.4): sin traza, no se puede decir si o4 es el mismo punto que o1.
- **Conclusión: correcto.** El bróker aplica ADR-0057, el bot no reintenta el punto rechazado, y
  que el bot no entre cuando la caja ya quedó atrás es la regla; si el trader entra o no en ese
  caso, es la pregunta 9 de V, que gana estos cinco días (§3.2).

### 2.h Las 4 sesiones con los cartuchos agotados, como dato

El consultor pidió llevarlas al informe como dato (respuesta a la PARADA, «Además»): son las 4 con
`detenido_por_cartuchos:si` en la diaria de `main` (§1.c). Lo que se ve, sin nada en dinero:

| sesión | órdenes llenadas antes de agotarse | ¿el mismo punto? | cuándo se fija `detenido_por_cartuchos` |
|---|---|---|---|
| 2026-07-01 07-11 | o1, o2 y o4 (llenadas de 05:00Z a 05:11Z) | no: tres puntos (1.14093, 1.14084 y 1.14085) | 05:12Z (07:12), RN-016; RN-001 prohíbe hasta el final de la sesión |
| 2026-07-01 11-15 | ninguna: lo arrastra de la mañana | — | 09:00Z (11:00), el primer cierre; se reinicia con la toma de las 10:52Z (2.e) |
| 2026-07-13 11-15 | o11, o12 y o13 (09:37Z a 09:39Z) | sí: 1.14301 @ 09:36Z, en las tres (traza) | 09:40Z (11:40) |
| 2026-08-26 07-11 | o1, o3 y o4 (05:39Z a 05:44Z) | el mismo 0, 1.16657 (sin traza: «### Ordenes») | en la diaria, `detenido_por_cartuchos:si` en la sesión |

Dos de las cuatro se agotan con reentradas en el mismo 0 en pocos minutos, que es la E de 2.d.4. Si
Y (§4.1) se arregla, esas dos sesiones cambian; 2026-07-01 07-11 no.

## 3 · Fase 2 · El resumen

### 3.1 La tabla

| comprobación | sesiones | conclusión | destino |
|---|---|---|---|
| P2: ¿el 0 sale del pivote que dice la spec? (§2.d) | 2026-01-29 11-15, 2026-08-20 11-15, 2026-01-08 07-11 | **correcto**: el 0 es el pivote de la regla, no se mueve dentro del punto, y el 1 se recalcula | — |
| P2: ¿dónde estaba el 0 del trader? (§2.d) | las mismas | **R**: en 01-29 y 08-20, en un pivote posterior que el bot VE y RN-009 prohíbe; en 01-08, en un máximo que la regla no toma por pivote (velas sin cuerpo en la racha) | V: pregunta 8 (01-29, 08-20) y pregunta nueva A (01-08) |
| P2: el punto de una orden ya llenada se vuelve a colocar (§2.d.4) | 2026-01-29 11-15, 2026-07-13 11-15 y 2026-01-29 07-11 con traza; hasta 47 órdenes en 22 sesiones por recuento (cota superior) | **E** | Y (rama propuesta, §3.3), antes de V |
| RN-005, RN-009 y RN-001 en las sesiones sin orden (§2.e) | las 14 | **correcto** | V: pregunta 8 |
| RN-001 en 2026-07-01 11-15: ¿cartuchos o `ventana_fin`? (§2.e) | 2026-07-01 11-15 | **correcto**: los dos, en tramos distintos; no cambia nada de lo que el bot habría hecho | — |
| Por qué no hubo `orden_dimensionada` (§2.f) | 2026-01-08 11-15 | **R**: la toma fue en la sesión anterior, con el sesgo contrario | V: pregunta nueva B |
| Por qué no hubo `orden_dimensionada` (§2.f) | 2026-08-14 07-11 | **R**: el precio no llega a ningún bajo de M15 formado; el trader toma otra liquidez | V: pregunta 5 |
| Rechazos por `precio_invalido` (§2.g) | 2026-07-08 11-15, 2026-07-13 11-15, 2026-01-08 07-11, 2026-08-07 07-11, 2026-04-27 07-11; 2026-04-16 07-11 sin rechazo | **correcto**: el bróker aplica ADR-0057 y el punto rechazado no vuelve | V: pregunta 9 |
| Los cartuchos agotados (§2.h) | 4 sesiones | dato: dos se agotan por la E | — |

«Correcto» quiere decir aquí que la regla se aplica tal como está escrita, en su instante, y que la
diferencia con el trader, si la hay, es de regla: va a V como pregunta, no a una rama de código.

### 3.2 Las preguntas para V

Redactadas para el trader, sin cifras de VIABILIDAD-COMISION ni nada en dinero. Las horas, en su
reloj (Europe/Madrid).

**Las que ya existen** («Para el cuestionario de la sesión 5», CORRIDA-CONSTRUCCION.md §4.5), por su
texto, con los días que ganan:

- **Pregunta 8:** «¿Entra el trader cuando la zona se desarrolla en el lado de ruido de la liquidez
  de M15, o cuando hay más zonas de control de las admitidas? (las 14 sesiones de §4.6).» Gana dos
  días que la enseñan mejor que esas 14: **2026-01-29**, venta de las 14:01 (el bot ve el mismo
  punto de breaker a las 14:00 y no entra porque ya cuenta dos zonas de control desde la toma de las
  13:51), y **2026-08-20**, compra de las 13:00 (lo mismo: ve el punto a las 12:57, con dos zonas
  desde la toma de las 12:46).
- **Pregunta 9:** «Si el precio ya pasó el 0 cuando se forma la caja, ¿entra o no? (las 3
  sesiones con `precio_invalido`).» Gana los cinco días de §2.g, con su forma: la vela roja que
  cierra el tramo verde es pequeña y cierra en el 0 o a un punto, así que el precio de compra ya
  está por encima cuando se forma el punto: **2026-07-08** 13:42, **2026-07-13** 14:14,
  **2026-01-08** 09:04, **2026-08-07** 07:34 y 08:43, **2026-04-27** 07:00, 07:05 y 07:08.
- **Pregunta 5:** «Qué liquidez y qué zona elige (P3, con A-43, A-50 y A-53).» Gana **2026-08-14**,
  compra de las 08:30 con el stop en 1.15388: el bot no ve ninguna toma de liquidez de M15 en esa
  sesión (el bajo de M15 vigente, de las 06:45, no se alcanza). ¿Qué bajo de M15 tomó el precio
  antes de esa compra?
- **Pregunta 3** (las reentradas): sigue como está. La parte de P5 que es la E de §2.d.4 (el bot
  vuelve a entrar en el MISMO punto tras un stop) se arregla en Y; lo que quede después de Y es lo
  que hay que preguntar.

**Las nuevas:**

- **A (la vela sin cuerpo dentro del tramo que marca el punto de breaker).** «Después de una vela
  verde vienen una o dos velas sin cuerpo (abren y cierran en el mismo precio) y luego una roja. Para
  tu orden de compra, ¿el máximo de la verde es un punto de breaker? (a) sí, las velas sin cuerpo no
  cortan el tramo; (b) no, la roja tiene que venir justo después de la verde; (c) otra, ¿cuál?».
  En venta, lo mismo en espejo. Día: **2026-01-08**, compra de las 09:21 (verde de las 09:16,
  máximo 1.16746; sin cuerpo las de las 09:17 y las 09:18; roja la de las 09:19); el bot no ve ahí
  ningún punto. Es distinta de la pregunta 1 de ADR-0076 §4, que va sobre la vela sin cuerpo en el
  retroceso como alternancia, no sobre el tramo que forma el punto; va junto a la pregunta 4 (qué
  velas forman la caja).
- **B (una toma de la sesión anterior, con el sesgo contrario).** «En la sesión de 11 a 15 el sesgo
  es bajista, y en la de 7 a 11 era alcista. El alto de M15 que ahora es tu liquidez se rompió con
  cuerpo en la vela de las 10:54, todavía en la sesión de la mañana. ¿Esa toma vale para la sesión
  de la tarde, o esperas a que el precio tome otro alto después de las 11:00? (a) vale, entro en la
  tarde con esa toma; (b) no vale, espero otra; (c) otra, ¿cuál?». Día: **2026-01-08**, venta de
  las 14:29. Hoy el bot aplica (b) (ADR-0066). **A-46 está RESUELTA** («cada sesión es un mundo
  diferente», sesión 3, v9 0:32:53; `ambiguedades.yaml:1355`), y B no la repite: A-46 se respondió
  sin distinguir el sesgo, y aquí la toma de la mañana iba contra el sesgo de la mañana y a favor
  del de la tarde. Si el trader contesta (a), A-46 se REABRE con un registro `REOPEN`
  (docs/runbooks/AMBIGUEDADES.md), no se cambia sin más (hallazgos b4 y b5 del revisor).

### 3.3 La E: la rama que se propone (sin escribirla)

**Y. Un punto ya llenado no se vuelve a colocar con otra caja.**
- **Qué arreglaría:** que, tras llenarse la orden de un punto, ninguna zona nueva de ese MISMO punto
  (con otro 1) se vuelva a colocar en la sesión, como dice ADR-0064, decisión 1, y como el código ya
  hace con un punto rechazado (`marcar_rechazada`). La reubicación de una orden PENDIENTE con el 1
  nuevo (ADR-0074) no cambia.
- **Qué ficheros toca:** `src/botsito/engine/zonas.py` (apuntar el punto llenado, como
  `marcar_rechazada`, y que `toca_colocar_orden_limite` lo niegue, :469-475) y
  `src/botsito/engine/cableado.py` (donde llega el evento LLENADA del bróker, :366-375, que conoce la
  zona de la orden por `ctx.zona_de_orden`); quizá `primitivas_broker.py` (`_punto_nuevo`, :235-253,
  si la reubicación tiene que ver lo mismo). Sin ADR nuevo: aplica la decisión 1 de ADR-0064; si el
  consultor prefiere fijarlo por escrito, una nota en ADR-0074.
- **Con qué test:** en `tests/unit/test_caja_hasta_el_llenado.py`, una serie sintética en que la
  orden del punto se llena, salta su stop en la vela siguiente y el máximo sube (1 nuevo): en `main`
  se coloca una segunda orden en el mismo punto (el test falla); en la rama no. Y su pareja: con la
  orden SIN llenar, el 1 nuevo la reubica igual que hoy (el test pasa en los dos). Después, la corrida
  2 repetida con los tres comandos de R3.1, y `reentradas.py` sobre la salida nueva (debería dar 0
  órdenes en el punto de una llenada, salvo un pivote nuevo al mismo nivel).
- **Por qué antes de V:** cambia las reentradas que la pregunta 3 enseña al trader, y dos de las
  cuatro sesiones con los cartuchos agotados (§2.h).

## 4 · Para la orden de cierre

### 4.1 Líneas preparadas para el commit del contrato de la orden de cierre

**Next Action** (`PROJECT_STATE.md`):

- **O sale** a `docs/state/HISTORIA.md`, con su texto literal, bajo:

      # Next Action HECHA · O · las comprobaciones en el visor · sale de PROJECT_STATE.md en trabajo/visor-construccion (2026-10-18)

      O. Comprobaciones en el visor de R3.1, con sus días (CORRIDA-CONSTRUCCION.md §4.5, «Ramas candidatas»). El cuestionario de V necesita esos gráficos.

      La hace `trabajo/visor-construccion` (docs/validation/VISOR-CONSTRUCCION.md).

  (Ya hay un «# Next Action HECHA · O ·» de `trabajo/entrada-julio`, de otra O: el título lleva por
  eso su nombre.)
- **F cambia** a:

      F. Y → V. Las re-corridas de R3.1 con el sesgo nuevo (SESGO-H4-COLOR.md §4) y con el límite del lote (MARGEN-LOTE.md §4) están hechas. Y va antes de V: cambia las reentradas de la pregunta 3.

- **Y entra** (ninguna entrada de la hoja de ruta la nombra; E, la de la rama del margen, ya está
  HECHA en R3.3, y reutilizarla haría fallar `test_hoja_de_ruta`). HISTORIA ya tiene una «# Next
  Action HECHA · Y ·» de `trabajo/adelgazar-estado` (HISTORIA.md:7130), como pasa con la O: cuando
  esta Y salga, su título llevará nombre (hallazgo b7 del revisor). El consultor puede elegir otra
  letra libre en la hoja de ruta (R o Z) y cambiarla en las tres líneas de §4.1 y en R3.4.

      Y. Que el punto de una orden ya llenada no se vuelva a colocar con otra caja (ADR-0064, decisión 1): hoy se marca la zona y no el punto; en la corrida 2, hasta 47 órdenes en 22 sesiones van al 0 de una ya llenada (VISOR-CONSTRUCCION.md §2.d.4). Rama de código, con su test y la corrida 2 repetida.

- **V cambia:** «y A-57 (el lote que no cabe, MARGEN-LOTE.md §5). Depende de R1.1, de R3.1, de O,
  de J (kit hoja) y de la copia de seguridad (A.4).» pasa a «A-57 (el lote que no cabe,
  MARGEN-LOTE.md §5); y las preguntas de VISOR-CONSTRUCCION.md §3.2. Depende de R1.1, de R3.1, de Y,
  de J (kit hoja) y de la copia de seguridad (A.4).» V no tendrá página de 2026-07-01 11-15 (§2.a):
  si la necesita para el cuestionario, un esquema dibujado (respuesta a la PARADA 2, punto 0).

**Hoja de ruta** (`docs/plan/HOJA-DE-RUTA.md`):

- **R3.2 pasa a HECHA**, con esta línea tras su «Hecho cuando»:

      - **Estado:** HECHA (`trabajo/visor-construccion`; VISOR-CONSTRUCCION.md): los gráficos son
        las páginas del visor, regenerables con los comandos del informe (§2.c), fuera de git; 19
        días con «no» de `contexto_h4.py`, que se pueden enseñar a V (si el visor o la spec cambian
        lo que pintan, se vuelven a comprobar antes), y 2026-07-01 sin página (su contexto pinta un
        día oculto). Una E (la reentrada en un punto ya llenado: R3.4) y el resto «correcto», que
        aquí quiere decir que la regla se aplica como está escrita y la diferencia con el trader es
        de regla: va a V con sus preguntas (§3.2).

- **R3.4 entra**, al final del tramo R3:

      ### R3.4 · Un punto ya llenado no se vuelve a colocar
      - **Refs:** NA:Y · ID:ADR-0064 · ID:ADR-0074
      - **Qué es:** que el bot no vuelva a colocar, con otra caja, el punto cuya orden ya se llenó
        (ADR-0064, decisión 1; VISOR-CONSTRUCCION.md §2.d.4), y la corrida 2 repetida.
      - **Depende de:** R3.2 (HECHA).
      - **Quién:** la sesión, con el encargo del consultor.
      - **Hecho cuando:** un test lo rompe en `main` y pasa en la rama, y la corrida 2 está repetida
        con los tres comandos de R3.1.

- **R4.1:** en sus Refs, `NA:O` pasa a `NA:Y`; en «Qué es», «y A-57 (el lote que no cabe,
  MARGEN-LOTE.md §5).» pasa a «A-57 (el lote que no cabe, MARGEN-LOTE.md §5); y las preguntas de
  VISOR-CONSTRUCCION.md §3.2 (las dos nuevas y los días que ganan la 5, la 8 y la 9; R3.2).»; y
  «Depende de» dice «R3.2 (HECHA), R3.3 (HECHA), R3.4 (NA:Y)».

**Technical Debt** (seis líneas nuevas; su evidencia, en §4.3):

    - El visor no conecta `--diagnostico-cuenta-diaria` (cli.py:2557; el arnés sí, :2437): con `--todos` arrastra la cuenta (VISOR-CONSTRUCCION.md §4.3).
    - VISOR-DIAS.md no recoge las opciones de diagnóstico del visor ni que calienta con el M1 del mes anterior (VISOR-CONSTRUCCION.md §4.3).
    - El visor no enseña las H4 que el sesgo salta por el color (ADR-0080 §10; VISOR-CONSTRUCCION.md §4.3).
    - `test_visor.py` hace leer al visor el M1 de marzo (calienta abril) en cada make check (HOLDOUT-EXPOSICIONES, 2026-10-18; VISOR-CONSTRUCCION.md §4.3).
    - `motor visor --hasta` no recorta las H4 de contexto, las listas ni el resumen del bróker (VISOR-CONSTRUCCION.md §4.3).
    - El bróker simulado cotiza con el respaldo M1 la orden del primer cierre de la ventana: los ticks empiezan en ventana_inicio y la orden lleva 1 ms antes (VISOR-CONSTRUCCION.md §4.3).

### 4.2 Las líneas, aplicadas en memoria contra los tests

`anexos/VISOR-CONSTRUCCION/simular_cierre.py` aplica en memoria, como sustituciones exactas que
tienen que casar una vez, todas las líneas de §4.1, y corre las funciones a, b y c de
`tests/unit/test_hoja_de_ruta.py` y los cuatro tests de `tests/unit/test_project_state.py` (las
secciones y su orden, `Current Branch` no vacío, menos de 25.000 bytes) sobre una copia del
PROJECT_STATE simulado en una carpeta temporal fuera del repo:

    uv run python docs/validation/anexos/VISOR-CONSTRUCCION/simular_cierre.py .

    a: []
    b: []
    c: []
    test_project_state_exists: pasa
    test_project_state_has_required_sections_in_order: pasa
    test_project_state_declares_a_branch: pasa
    test_project_state_cabe_en_el_tope: pasa
    PROJECT_STATE hoy: 23629 bytes
    PROJECT_STATE simulado: 24742 bytes

**Pasan.** La primera versión de las líneas daba 25.036 bytes y no cabía: se acortaron las deudas
(su evidencia vive en §4.3) y las líneas de F, Y y V. Con la sexta deuda y la línea Y corregida
(hallazgos b2 y b3 del revisor), el margen queda en 276 bytes; con la línea de `test_visor.py`
citando la fila nueva de HOLDOUT-EXPOSICIONES (orden de cierre, punto 1), 24.742 bytes, por debajo
de los 24.800 que fija la orden. El cierre cambia
además las líneas de cabecera de PROJECT_STATE (rama y estado), que hoy hablan de esta rama.

### 4.3 La deuda, con su evidencia

1. **El visor no conecta `--diagnostico-cuenta-diaria`.** `cli.py:2437` lo pone en el motor del
   arnés y `motor_visor` no lo copia a `cableado_motor` tras `cli.py:2557` (§1.a). Con `--caso` no
   cambia nada, porque el motor es nuevo para un día (§1.a, y los 20 días de §2.c lo confirman:
   órdenes iguales a las de `main`); con `--todos`, la cuenta se arrastra entre días.
2. **VISOR-DIAS.md no recoge las opciones de diagnóstico ni el calentamiento.** `grep -n -i
   "diagnostico\|mes anterior\|calienta\|calentar" docs/runbooks/VISOR-DIAS.md` no da ninguna línea.
   El visor exige `--diagnostico-a35` y `--diagnostico-a44` mientras A-35 y A-44 sigan abiertas
   (`test_visor.py:381-385`), y lee el M1 entero del mes anterior (§1.b; `Preparador._m1`).
3. **El visor no enseña las H4 que el sesgo salta por el color.** ADR-0080 lo dejó dicho: «enseñar
   las saltadas es una mejora para la rama de comprobaciones en el visor» (`0080…md:157-158`), que es
   esta, y esta rama no toca código (encargo §2).
4. **`test_visor.py` hace leer al visor un mes reservado en cada `make check`.** El test
   `test_por_la_cli_sobre_un_dia_dev_de_construccion_si_hay_datos` (`test_visor.py:368-401`) corre el
   visor sobre el primer día dev del primer mes de construcción (`real.construccion[0]`, que es
   `2026-04`), y el visor calienta con el M1 entero de marzo. **Medido, corrige la redacción de la
   fase 0 (§1.f, h13) y de la respuesta del consultor («marzo y junio»):** el test solo lee marzo;
   junio solo lo leen las páginas de julio de esta rama, declaradas en HOLDOUT-EXPOSICIONES. Por eso
   la línea de §4.1 dice «marzo (calienta abril)».
5. **`--hasta` no recorta las H4 de contexto, las listas ni el resumen del bróker** (§1.b, con sus
   líneas de `visor.py`), aunque VISOR-DIAS.md:40-41 promete una vista recortada.
6. **El bróker cotiza con el respaldo M1 la orden del primer cierre de la ventana** (medido en la
   fase 1, hallazgo b3 del revisor). `simulacion.mercado_de_construccion` carga los ticks solo entre
   `ventana_inicio` y `ventana_fin` (`simulacion.py:196-205`), y la orden que se coloca en el primer
   cierre de la ventana lleva el instante de ese cierre menos 1 ms (en 2026-04-27, o1 «colocada
   04:59:59Z»). `Mercado.cotizacion` (`llenado.py:93-113`) no encuentra ningún tick hasta ese
   instante y usa la última M1 cerrada más el spread supuesto («respaldo_m1» en
   `dias/2026-04-27.ticks.txt`). No es una de las 18 horas sin ticks de R3.1: es el borde de la
   ventana, y toca a toda orden de la primera sesión colocada en su primer cierre. No cambia la
   conclusión de 2026-04-27 (el bid del respaldo ya está 4 puntos por encima del 0), pero el
   rechazo se decidió con un precio aproximado.

### 4.4 Para ERRORES-RECURRENTES (los escribe `cerrar-rama`, en la fila de la rama)

- **Del consultor (respuesta a la PARADA 1, punto 8), dos:**
  1. La PARADA 4 de R3.1, punto 2, leyó «no se produjo un hecho del camino» como «RN-011 no
     dimensiona con los hechos del camino producidos», y el encargo lo heredó (h3 del auditor). La
     lección: citar el hecho que falta por su nombre (`liquidez_tomada`), no por su consecuencia.
  2. El encargo dio como hechos dos afirmaciones del auditor que el repo contradice (la página solo
     enseña la caja final; `--depuracion` da una traza). La lección: una afirmación del auditor entra
     al encargo como «verifica que…», no como hecho.
- **Del consultor (respuesta a la PARADA 2, «Además»), un acierto de la regla:** `contexto_h4.py`
  antes de cada página encontró 2026-07-01 antes de pintar nada: la regla «contexto_h4.py antes de
  cada página» funcionó, y la PARADA 2 salió de ella.
- **De la sesión, dos:**
  1. Un guion de la carpeta de trabajo que escribe su salida con `>` en Windows la deja en CRLF y,
     si imprime caracteres fuera de ASCII sin `reconfigure`, en cp1252: `lotes.txt` salió en cp1252
     y cuatro salidas en CRLF, y se normalizaron (§2.c). La lección: `sys.stdout.reconfigure(encoding
     ="utf-8", newline="\n")` en todo guion cuya salida va a un anexo.
  2. La primera captura de `detenido_por_*` en la traza buscaba el valor «si», y RN-016 fija
     `hasta_cartuchos_reinicio`: habría dicho «ninguno» en 2026-07-01 11-15. Se vio al cruzar la
     traza con las reglas disparadas, y las 20 trazas se regeneraron. La lección: un hecho de la
     forma (`hecho:`) vale con CUALQUIER valor fijado (`interprete._hecho`); se busca por presencia.
- Y lo que diga el revisor (§8).
- **Del consultor (orden de cierre, punto 1), un hallazgo que el revisor no vio (importa):** §4.3,
  punto 4, midió que `test_visor.py` hace leer al visor el M1 entero de marzo en cada `make check`,
  y la rama lo dejó solo como deuda. Se declaró en HOLDOUT-EXPOSICIONES (fila del 2026-10-18, desde
  `50045c8`). La lección, para el revisor: cuando una rama descubre una lectura de material
  reservado que ya ocurre, comprobar que queda declarada en HOLDOUT-EXPOSICIONES y no solo como
  deuda.

## 5 · El encargo, punto por punto

| # | requisito | estado | dónde |
|---|---|---|---|
| 0.1 | Base: `main` d1137eb, origin, el tag, ninguna otra rama, la CI de d1137eb con `gh run view` | Hecho | §0 |
| 0.2 | Abrir con `abrir-rama`: encargo tal cual, `contrato.yaml` con HOLDOUT-EXPOSICIONES, Archivo de PROJECT_STATE | Hecho | f85fb1e |
| 0.3 | Informe y anexos en sus rutas; fase-cero con el auditor; entregar-rama; leer VISOR-DIAS.md | Hecho | §1.f, este informe |
| 1.1 | Las comprobaciones E de R3.1 sobre el motor de hoy, cada una con E, R o correcto | Hecho | §2, §3.1 |
| 1.2 | Sobre la diaria de `main` de hoy (`anexos/MARGEN-LOTE/diaria…`) | Hecho | §1.c, §2.c |
| 1.3 | «Gráfico» = la página, con su comando y lo que se lee; los HTML no se commitean | Hecho | §2.c; `data/visor/` |
| 2.1 | Ningún código de `src/`, regla, parámetro, ambigüedad, ADR, evidencia, feedback ni caso | Hecho | §7 (ficheros) |
| 2.2 | Los informes y anexos cerrados no se editan | Hecho | §7 |
| 2.3 | El heredado 30 no se toca | Hecho | §2.f lo cita, no lo cambia |
| 2.4 | Ni guardias, ni `.claude/`, ni el `Makefile` | Hecho | §7 |
| 2.5 | PROJECT_STATE, solo lo del ritual | Hecho | solo la apertura (f85fb1e) |
| 2.6 | La salida del visor a `data/visor/` | Hecho | §2.c |
| 2.7 | HOLDOUT: la lectura del visor declarada antes de la primera página | Hecho | HOLDOUT-EXPOSICIONES, fila del 2026-10-18 (f39e0da, antes de ninguna página) |
| 2.8 | Las H4 de contexto, medidas en el código | Hecho | §1.b, §2.a |
| 2.9 | Ninguna vela, hora ni precio anterior al día dev, ni nada en dinero, al informe | Hecho | `extraer_pagina.py`, `comun_visor.antes_del_dia`; el revisor lo comprueba (§8) |
| 2.10 | Si el clasificador niega un comando, PARADA | No hizo falta | el clasificador no negó nada; la guardia negó cuatro comandos (§2.c) |
| 3.a-d | Fase 0: reproducir la corrida 2, qué lee el visor, las listas, de dónde sale cada dato | Hecho | §1, 8cceb46 |
| 3.e | PARADA con a-d | Hecho | §1, «Lo que necesito que decidas» |
| 4.1 | Fase 1: la fila de exposiciones antes de la primera página | Hecho | 2.7 |
| 4.2 | P2 en los tres días: el 0 frente al pivote de la spec y el 0 del trader | Hecho | §2.d |
| 4.3 | RN-005, RN-009 y el minuto de `ventana_fin` de RN-001, sesión por sesión | Hecho | §2.e |
| 4.4 | Las 2 sesiones: «por qué RN-011 no dimensionó con los hechos del camino producidos» | Hecho de otra forma | la premisa no se cumple (falta la toma, §1.c): se miró por qué no hubo toma, con RN-004 por cierre (§2.f) |
| 4.5 | Los rechazos elegidos: frente al bid o el ask, la caja atrás, el punto rechazado no vuelve | Hecho | §2.g |
| 4.6 | Para cada sesión: el comando exacto del visor y del guion | Hecho de otra forma | un comando por día con su caso (§2.c, plantilla y lista de casos) y las salidas por día en `dias/`, no un bloque por sesión |
| 4.7 | Lo que se ve, con UTC y hora del trader, solo del día dev | Hecho | §2.d a §2.h |
| 4.8 | Fase 2: la tabla | Hecho | §3.1 |
| 4.9 | Para cada E, la rama: qué arregla, ficheros, test | Hecho | §3.3 |
| 4.10 | Para cada R, la pregunta para V; las 8 y 9 por su texto; las demás, nuevas | Hecho | §3.2 |
| 5.1 | El encargo frente a lo hecho y las desviaciones | Hecho | §5, §6 |
| 5.2 | La deuda: el visor sin `--diagnostico-cuenta-diaria`; VISOR-DIAS.md sin diagnóstico ni calentamiento | Hecho | §4.1, §4.3 |
| 5.3 | Las líneas del cierre: O a HISTORIA; F; V sin «de O» y con las preguntas; R3.2 HECHA con su Estado; R4.1 sin NA:O, con «R3.2 (HECHA)» | Hecho | §4.1 |
| 5.4 | Las líneas aplicadas en memoria contra `test_hoja_de_ruta.py` y `test_project_state.py` | Hecho, pasan | §4.2 |
| 6 | El revisor (opus), con los dos ejes y el alcance extra | Hecho | §8 |
| 7 | CI: si no toca la plataforma, decirlo con la lista de ficheros | Hecho | §7 |
| R1.0 | Respuesta 1, punto 0: los tres días de P2 | Hecho | §2.d |
| R1.1 | Punto 1: `traza_por_cierre.py`, que solo lee el `Evento`; PARADA si sus órdenes no son las de `main` | Hecho | §2.c: iguales en los 20 días |
| R1.2 | Punto 2: `extraer_pagina.py`; la sesión no abre una página entera | Hecho | §2.c |
| R1.3 | Punto 3: las 2 sesiones por la traza de RN-004; R (A-35) salvo error de código; heredados 25 y 30 sin tocar | Hecho de otra forma | R, pero no solo por A-35: la otra lectura de A-35 tampoco da toma (§2.f); una pregunta nueva (B) y la 5 |
| R1.4 | Punto 4: los cinco rechazos; 2026-04-16 sin página | Hecho | §2.g |
| R1.5 | Punto 5: «anterior al día dev» por la fecha UTC de la vela | Hecho | `comun_visor.antes_del_dia` |
| R1.6 | Punto 6: las tres deudas más; R4.1 «Qué es» con las preguntas nuevas; el Estado de R3.2 explica «correcto» | Hecho | §4.1, §4.3 (con una corrección medida: §4.3, punto 4) |
| R1.7 | Punto 7: el cierre simulado con los dos tests | Hecho | §4.2 |
| R1.8 | Punto 8: los dos hallazgos del consultor para ERRORES-RECURRENTES | Hecho | §4.4 |
| R1.A | «Además»: 2026-07-01 11-15, cartuchos o `ventana_fin`; las 4 sesiones con los cartuchos agotados; sin las columnas en USD | Hecho | §2.e, §2.h; `reentradas.py` corta antes de esas columnas |
| R2.0 | Respuesta 2, punto 0: 2026-07-01 11-15 solo con la traza, sin página | Hecho | §2.a, `dias/2026-07-01.pagina.txt` |
| R2.1 | Punto 1: los otros 19 días; `contexto_h4.py` antes de CADA página | Hecho | `revisar_dia.py`, §2.c |
| R2.A | «Además»: el «no» de `contexto_h4.py` en el Estado de R3.2; la PARADA 2 a ERRORES-RECURRENTES como acierto | Hecho | §4.1, §4.4 |

## 6 · Desviaciones

- **El guion de traza tiene otras opciones que las que proponía la fase 0** (§1.d decía `--desde`
  y `--hasta`): tiene `--sesion`, `--rn004`, `--gates`, `--velas` y `--todos-los-cierres`. Lo que
  hacía falta era ver los predicados de RN-004 y de los gates en cada cierre, y las M1 de un tramo;
  un recorte por horas no lo daba.
- **Guiones que la fase 0 no nombraba:** `revisar_dia.py` (el orden de la respuesta a la PARADA 2
  en un solo guion), `reentradas.py` (el recuento de la E), `resumen_gates.py` (el resumen de §2.e),
  `simular_cierre.py` (§4.2), `listas.py` (el guion de las listas de la fase 0, que §1.c anunciaba,
  con su salida en `listas.txt`) y, tras el revisor, `pivotes_m15_del_dia.py` (§8.1). Ninguno escribe en el repo salvo `revisar_dia.py`, que escribe en
  `anexos/VISOR-CONSTRUCCION/dias/` y en `data/visor/`.
- **La E de §2.d.4 sale de mirar P2, no de una comprobación del encargo.** Entra en P2 porque el
  encargo pide comprobar que «lo que recalcula ADR-0074 en cada cierre de M1 hasta el llenado es el
  1»: o17 recalcula el 1 DESPUÉS del llenado.
- **Las páginas y las trazas se generaron seis veces**, mientras el guion de traza ganaba opciones
  (RN-004 en tramos, los gates, la captura de los `detenido_por_*` con cualquier valor: §4.4). Lo que
  hay en `dias/` es de la última pasada (los dos lotes de `lotes.txt`), y cada pasada corrió
  `contexto_h4.py` antes de cada página, con el mismo resultado.
- **Una corrección a la fase 0 y a la respuesta del consultor:** `test_visor.py` lee el M1 de marzo,
  no el de junio (§4.3, punto 4).
- **Las salidas guardadas con `>` se normalizaron** a UTF-8 y LF (§4.4); los guiones llevan ahora
  `reconfigure(newline="\n")` para que su comando dé el mismo fichero.
- **`revisar_dia.py` escribió en el repositorio real, con la raíz sacada de su propia ruta**, en
  las seis pasadas de desarrollo y en la de verificación anterior al revisor: contra CLAUDE.md,
  «Ensayos aislados», puntos 1 y 2 (hallazgo a1 del revisor). Escribía solo en
  `anexos/VISOR-CONSTRUCCION/dias/` y en `data/visor/` (ignorada), nunca mientras corría `make
  check`. Un clon con `git worktree` no tiene `data/` (fuera de git), así que el visor no habría
  corrido ahí; lo que la regla pide en ese caso es que la salida vaya por argumento a una carpeta
  fuera del repo, y así se hizo la pasada final (§2.c).

## 7 · Exposiciones, ficheros y CI

**Exposiciones:** la fila del 2026-10-18 de HOLDOUT-EXPOSICIONES (fase 1), ampliada el mismo día con
lo leído tras la PARADA 2 (su punto 8). Ninguna otra.

**Ficheros que cambian frente a `main`:** el estado y el contrato (`PROJECT_STATE.md`,
`contrato.yaml`, `docs/state/HISTORIA.md`, `docs/encargos/trabajo-visor-construccion.md`); este
informe y `docs/validation/HOLDOUT-EXPOSICIONES.md`; y los anexos de
`docs/validation/anexos/VISOR-CONSTRUCCION/` (los guiones `comun_visor.py`, `contexto_h4.py`,
`traza_por_cierre.py`, `ticks_del_rechazo.py`, `extraer_pagina.py`, `revisar_dia.py`, `listas.py`,
`reentradas.py`, `resumen_gates.py`, `simular_cierre.py`, `pivotes_m15_del_dia.py`; sus salidas
`contexto_h4.txt`, `listas.txt`, `lotes.txt`, `reentradas.txt`, `resumen_gates.txt`,
`pivotes_m15.txt`; y `dias/`). Ningún fichero de `src/`, `tests/`,
`scripts/`, `knowledge/`, `config/`, `docs/adr/`, `docs/spec/`, `docs/plan/`, `docs/runbooks/`,
`.claude/`, `.github/` ni el `Makefile`.

**`make check` de cada commit** (sus líneas, leídas del log antes de commitear; hallazgo a2 del
revisor, que no las encontró):
- 304da27 (fases 1 y 2): `SELLO: make check en verde sobre el arbol
  a78d20c50bb6412eb7f27eed1a8923c07364a7e3`; exit 0; ningún `failed`; `DURACION de make check: 930
  s`; `PICO DE MEMORIA de make check: 295 MiB en test`.
- El commit de los hallazgos del revisor: su `make check` sella el árbol de ese mismo commit, así
  que sus líneas no pueden ir dentro de él; se dan en el mensaje de entrega, y el sello queda en
  `.git/botsito-sello` igual a `git rev-parse HEAD^{tree}`.

**CI:** la rama no toca código, hooks, rutas ni el sistema de archivos: no hace falta el push como
`fix/visor-construccion`. Ninguna consulta de la CI se hizo con `curl`, con `gh run watch` ni con un
guion.

## 8 · El revisor

Agente `revisor` (opus) sobre la rama en 304da27, el 2026-10-18, con los dos ejes y el alcance
extra del punto 6 del encargo. Su informe, pegado tal cual (nada cita un tramo no citable; 0
retiradas):

> ## Informe del revisor · trabajo/visor-construccion · 2026-10-18
>
> Base `d1137eb` (merge-base con main). Rama en `304da27` y árbol limpio. Son 4 commits y 105 ficheros, todos dentro del contrato. Ningún fichero se borra ni cambia de nombre. Solo cambian (M) `PROJECT_STATE.md`, `docs/state/HISTORIA.md` y `docs/validation/HOLDOUT-EXPOSICIONES.md`; los demás son nuevos (A).
>
> ### Eje (a) · Reglas de la casa
> Resumen: 1 bloquea, 0 importa, 1 menor.
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | a1 | bloquea | `revisar_dia.py` escribe en el repositorio, pero la raíz no le llega por un argumento ni por una variable de entorno: la saca de `__file__`. Rompe el punto 2 de «Ensayos aislados» de CLAUDE.md («La raiz de un instalador, o de cualquier script que escriba, sale de un argumento o de una variable de entorno»). Además, el informe cuenta que el guion se ejecutó seis veces sobre el repositorio real mientras se desarrollaba, y no en un clon con `git worktree` (punto 1 de esa misma regla). El precedente de main sí la cumple: `anexos/MARGEN-LOTE/fase4_medidas.py:136` escribe en `a.escribir`, que es un argumento. | `anexos/VISOR-CONSTRUCCION/revisar_dia.py:29` `AQUI = Path(__file__).resolve().parent`, `:39` `CARPETA_PAGINAS = cv.RAIZ / "data" / "visor" / "visor-construccion"`, `:40` `CARPETA_DIAS = AQUI / "dias"`, `:61` `write_text(...)`; `comun_visor.py:21` `RAIZ = Path(__file__).resolve().parents[4]`; `VISOR-CONSTRUCCION.md:1153-1156` («Las páginas y las trazas se generaron seis veces…») |
> | a2 | menor | El informe no deja constancia del `make check` de la rama: ni la línea `SELLO` ni la de `PICO DE MEMORIA`. Además, `make-check.log` no existe en la raíz. La única prueba de que pasó es que el sello coincide con el árbol de HEAD. | `ls make-check.log` → «No such file»; `grep -n "SELLO\|PICO" VISOR-CONSTRUCCION.md` → nada; `cat .git/botsito-sello` = `a78d20c5…a7e3` = `git rev-parse HEAD^{tree}` |
>
> Comprobado sin hallazgos:
> - **Contrato.** `uv run python scripts/contrato_rama.py` → «CONTRATO: 105 ficheros dentro del contrato de trabajo/visor-construccion (riesgo alto, … tramo 'R3', 3 comprobaciones para el revisor)», exit 0. `git diff main --name-only` solo da rutas permitidas.
> - **Trailers `Fuente:`.** La rama no toca `knowledge/spec` ni `knowledge/cases`, así que no aplican.
> - **Holdout y material.** Nada toca `knowledge/cases/holdout/`. La fila del 2026-10-18 está en HOLDOUT-EXPOSICIONES: nombra el visor, el calentamiento con marzo y junio, `contexto_h4.py`, las M1 de `--velas` y la lectura de `a35-inicio`. Ningún fotograma, libro, transcripción ni agregado.
> - **Regímenes de cambio.** HISTORIA es +189/-0. HOLDOUT-EXPOSICIONES es +1/-0. El encargo solo crece desde f85fb1e (+60/-0). Ningún cambio en evidence, feedback, manifests ni corpus.
> - **Ambigüedades, ADR, informes cerrados y guardias de `cita`.** No hay cambios: no aplican.
> - **Cifras en el registro.** No hay código: no aplica.
> - **Informe.** Existe y acaba en «## Estado», que todavía dice PENDIENTE DEL REVISOR.
> - **Citas contra su fuente.** Comprobé que lo citado dice lo que el informe afirma en estas fuentes:
>   - `zonas.py:41-42` (docstring);
>   - ADR-0064, decisión 1 (`0064…md:79-81`);
>   - ADR-0080 §10 (`0080…md:156-158`);
>   - `VISOR-DIAS.md:40-41`;
>   - `test_visor.py:373`, junto con `criterio_fidelidad.yaml:40` (`construccion[0]` = 2026-04, como dice §4.3, punto 4);
>   - `cli.py:2437`/`:2557`;
>   - `cableado.py:207-208`;
>   - `primitivas.py:266-296`;
>   - `primitivas_broker.py:635,650`;
>   - `estructura_m1.py:189-212`;
>   - `pivotes_m15.py` (`_racha_anterior`, `_pivote_de`);
>   - RN-005 en `zonas.py:503-521` y en la spec (`lado_de_ruido: {alcista: por_encima, bajista: por_debajo}`).
> - **Evidencia nueva.** La rama no añade ningún item a `knowledge/evidence/`.
>
> ### Eje (b) · Encargo
> Resumen: 0 bloquea, 4 importa, 4 menor. Requisitos: 30 hechos, 2 parciales, 0 no hechos (y 3 hechos de otra forma, declarados).
>
> | # | Requisito | Estado | Evidencia |
> |---|---|---|---|
> | 1 | Base: main, origin, tag, la CI con `gh run view` y ninguna otra rama | Hecho | §0, `VISOR-CONSTRUCCION.md:13-23`. No lo pude volver a comprobar (ver abajo) |
> | 2 | Abrir con abrir-rama: encargo, contrato con HOLDOUT-EXPOSICIONES y Archivo de PS | Hecho | f85fb1e; `contrato.yaml:8`; HISTORIA +189 |
> | 3 | Informe y anexos en sus rutas | Hecho | diff --stat |
> | 4 | Comprobaciones sobre la diaria de main de hoy (MARGEN-LOTE) | Hecho | `comun_visor.py:143-161` lee `anexos/MARGEN-LOTE/diaria…txt` |
> | 5 | «Gráfico» = la página, con su comando; los HTML fuera de git | Hecho | §2.c, `:494`; ningún `.html` en el diff |
> | 6 | No se toca src, spec, parámetros, ADR, evidencia, feedback ni casos | Hecho | `git diff --name-status`: solo docs/ y anexos |
> | 7 | No se editan los informes ni anexos cerrados (CORRIDA, SESGO, MARGEN) | Hecho | no aparecen en el diff |
> | 8 | Heredado 30, guardias, `.claude/` y Makefile intactos | Hecho | diff |
> | 9 | PS, solo lo del ritual | Hecho | `git diff main...HEAD -- PROJECT_STATE.md`: rama, Feature, Completed y Change Log (apertura) |
> | 10 | Fila de HOLDOUT antes de la primera página, nombrando el visor | Hecho (orden no verificable) | `HOLDOUT-EXPOSICIONES.md`, fila del 2026-10-18 (f39e0da) |
> | 11 | Nada anterior a las 00:00Z del día dev ni nada en dinero (informe y anexos) | Hecho | ver la comprobación extra 2 |
> | 12 | Fase 0.a: reproducir la corrida 2; la deuda de `cuenta_diaria` con su línea | Hecho | §1.a; `lotes.txt`: «iguales» en los 20 días |
> | 13 | Fase 0.b: lo que lee el visor de fuera del día dev | Hecho | §1.b |
> | 14 | Fase 0.c: listas P2, 14 sin orden, 2 sin `orden_dimensionada`, `precio_invalido` | Hecho | `listas.txt:29` «33 en 26 … 18 en 14»; `:131` «26 en 20 … 11 en 9»; tablas §1.c coinciden |
> | 15 | Fase 0.d: de dónde sale cada dato y cómo sacarlo | Hecho | §1.d |
> | 16 | PARADA con a-d | Hecho | `:306-357` |
> | 17 | P2 en los tres días: el 0 frente al pivote de la spec y el 0 del trader | Hecho | comprobado vela a vela en `dias/*.velas-trader.txt` (abajo) |
> | 18 | RN-005, RN-009 y RN-001 sesión por sesión | Parcial | tabla §2.e = `resumen_gates.txt`; la explicación de RN-009 es falsa (b1) |
> | 19 | Las 2 sin `orden_dimensionada` | Hecho de otra forma (declarado, §5 4.4 y R1.3) | `2026-01-08.traza.txt:184-188`, `2026-08-14.traza.txt` RN-004 |
> | 20 | Rechazos `precio_invalido`: frente al bid y el ask, la caja ya atrás, y que el punto rechazado no vuelve | Hecho | `dias/*.ticks.txt`; restas comprobadas (3,1,3,2,5,8,3,5) |
> | 21 | Para cada sesión, el comando exacto | Hecho de otra forma (declarado, §5 4.6) | §2.c |
> | 22 | Instantes en UTC y en hora del trader | Hecho | §2.d-2.h |
> | 23 | Fase 2: la tabla | Hecho | §3.1 |
> | 24 | Para cada E, la rama propuesta (qué arregla, ficheros, test) | Hecho | §3.3 |
> | 25 | Para cada R, su pregunta; la 8 y la 9 por su texto | Hecho | §3.2; el texto coincide con `CORRIDA-CONSTRUCCION.md:1246-1249` |
> | 26 | Deuda: el visor sin `cuenta_diaria`; VISOR-DIAS sin diagnóstico ni calentamiento | Hecho | §4.1, §4.3; `grep` sobre VISOR-DIAS → rc=1 |
> | 27 | Líneas del cierre (O a HISTORIA, F, V, R3.2 HECHA, R4.1) | Parcial | están, pero la de Y afirma más de lo medido (b2) y la letra Y ya se usó (b7) |
> | 28 | Simulación en memoria con los dos tests | Hecho | volví a ejecutar `simular_cierre.py .`: a/b/c `[]`, 4 tests pasan, 23629 → 24526 bytes, igual que §4.2 |
> | 29 | Respuesta 1, puntos 0-8 y «Además» | Hecho | §5, R1.0-R1.A |
> | 30 | Respuesta 2, punto 0: 07-01 sin página; punto 1: `contexto_h4` antes de CADA página | Hecho | `dias/2026-07-01.pagina.txt`; `revisar_dia.py:66-93` |
> | 31 | Las respuestas copiadas tal cual en el informe y en el encargo | Hecho | md5 idéntico: encargo 100-134 = informe 363-397; encargo 140-154 = informe 462-476 |
> | 32 | «El encargo, punto por punto» | Hecho | §5 |
> | 33 | CI: decirlo, con la lista de ficheros | Hecho | §7 |
> | 34 | Revisor y su informe pegado | Pendiente | §8 vacío; lo pega la sesión |
> | 35 | «Lo que necesito que decidas» (las dos PARADAS) | Hecho | `:306`, `:442` |
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | b1 | importa | §2.e dice de RN-009: «ya no vuelve a NO en la sesión: las zonas se cuentan desde la toma (ADR-0076 §2) y solo suben». Sus propios anexos lo desmienten en 12 de las 14 sesiones. La conclusión «0 cierres sin gate» se sostiene, porque en esos tramos RN-005 está en SÍ. Pero el mecanismo que hace volver el recuento a 0, incluso con la MISMA toma, no se examina, y es justo el gate que se está comprobando: ¿«tras la toma» de ADR-0076 §2 es la primera toma o la última? | `VISOR-CONSTRUCCION.md:730-731`. `resumen_gates.txt:11`: «SI \| NO …: 25, desde 05:29», con RN-009 en SÍ desde 05:43 (14 cierres), así que hay 11 cierres SI\|NO más tarde. Lo mismo en `:18,33,40,46,54,62,69,83,91`. `dias/2026-08-11.traza.txt` (gates): «05:54:00Z - 06:02:00Z, 9 \| SI, compra 0 1.15409 > toma 1.15402 \| NO, 0», con la misma toma 1.15402 que a las 05:21Z. `dias/2026-04-17.traza.txt`: «08:35:00Z … toma 1.17844 \| NO, 0» |
> | b2 | importa | La línea Y preparada para PS, que `simular_cierre.py:59-64` ya mete en la simulación, afirma como hecho que «vuelven a colocarse 47 órdenes en 22 sesiones». Pero §2.d.4 reconoce que es un recuento por PRECIO, no por punto, y el anexo trae al menos un caso que casi seguro es otro pivote al mismo nivel. | `VISOR-CONSTRUCCION.md:682-684` frente a `:973`. `reentradas.txt:2`: «2026-01-05 \| 07-11 \| o5 \| …T09:27:59 \| 1.16852 \| llenada \| o3 (…T06:04:22…)», más de 3 h después |
> | b3 | importa | La fase 0 afirmó que solo «6 de los 26 rechazos» caen sin ticks, con su lista, y la PARADA propuso 2026-04-27 07-11 como un rechazo «con ticks reales, fuera de las horas sin ticks». La medida lo desmiente: o1 de 04-27 se decidió sobre el respaldo M1. Ni §1.d ni §6 lo corrigen; la tabla de §2.g solo lo etiqueta. | `VISOR-CONSTRUCCION.md:239`, `:336-337`. `dias/2026-04-27.ticks.txt`: «o1 … colocada 04:59:59Z … bid 1.17268 ask 1.17272 (respaldo_m1)» |
> | b4 | importa | La pregunta nueva B («¿esa toma vale para la sesión de la tarde…?») cae encima de A-46, que está RESUELTA por el trader. El informe cita A-46 solo como la regla que aplica el bot. No dice que está resuelta ni por qué B es otra pregunta: el matiz es que el sesgo era el contrario en la sesión anterior. Sin eso, V puede volver a preguntar lo ya resuelto, y si el trader contesta otra cosa haría falta un REOPEN. | `VISOR-CONSTRUCCION.md:774`, `:921-926`. `knowledge/spec/ambiguedades.yaml:1355`: «RESUELTA el 2026-09-29 en la sesion 3 (v9 0:32:53): cada sesion es «un mundo diferente»» |
> | b5 | menor | La hora del cuerpo que se le da al trader no coincide con la de §2.f. §2.f dice «la M1 de las 09:54Z (10:54 del trader)»; la pregunta B le dice «se rompió con cuerpo a las 10:55». En su gráfico, la vela de las 10:55 es la siguiente, 09:55Z. | `VISOR-CONSTRUCCION.md:773` frente a `:923`; `dias/2026-01-08.velas-toma.txt` («09:54:00Z (10:54:00 del trader) O 1.16743 … C 1.16755») |
> | b6 | menor | Dos imprecisiones en §2.d.4. Primera: «coincide en las dos sesiones que la tienen», pero la traza también tiene 2026-01-29 07-11, que coincide (o3 y o4 en el punto de o2, ya llenada). Segunda: «ADR-0066 … solo sustituye la decisión 2», cuando el recuadro de ADR-0064 dice que ADR-0066 cambia también la decisión 3. | `VISOR-CONSTRUCCION.md:684-685`, `:670-671`. `dias/2026-01-29.traza.txt`: o2, o3 y o4 con «punto 119820@29494445». `0064…md`, recuadro bajo la decisión 3 («La decision 3 pasa a ser la opcion `sigue_hasta_ventana_fin`…») |
> | b7 | menor | «Y entra (letra nueva…)», pero HISTORIA ya tiene una Y cerrada. Es la misma colisión que h9 detectó para O, y aquí no se menciona: el título HECHA de esta Y necesitará un descriptor. | `VISOR-CONSTRUCCION.md:970`; `docs/state/HISTORIA.md:7130` «# Next Action HECHA · Y · sale de PROJECT_STATE.md en trabajo/adelgazar-estado (2026-10-08)» |
> | b8 | menor | §2.g dice que la traza «busca cualquier orden posterior» en un punto ya rechazado. Pero el guion excluye las órdenes que salieron rechazadas: un punto recolocado y rechazado otra vez no se imprimiría. En los cinco días los puntos rechazados son distintos (04-27: 117264, 117270 y 117275; 08-07: 115226 y 115220), así que la conclusión vale, pero la frase dice más que el guion. | `traza_por_cierre.py:363` `… and f[5] != "rechazada"`; `VISOR-CONSTRUCCION.md:837-839` |
>
> **Lo que pide el punto 6 del encargo:**
>
> 1. **Cada conclusión E, R o correcto, contra lo que cita.**
>    - **P2, el 0 y los pivotes.** Comprobé vela a vela los 0 y los pivotes:
>      - 01-29: 12:52Z roja 1.1956→1.19549; 12:58Z roja con mínimo 1.19603; 12:59Z verde; RN-009 «SI, 2» a las 13:00Z.
>      - 08-20: 10:47Z verde con máximo 1.17012 entre rojas; 10:54Z y 10:55Z verdes con máximo 1.16974; 10:56Z roja; «SI, 2/3».
>      - 01-08: 08:03Z y 08:05Z verdes; 08:17Z y 08:18Z con O=C (sin cuerpo); 08:19Z roja.
>
>      Coinciden con `dias/*.velas-trader.txt` y con las trazas. ADR-0076 lo dice (`0076…md:55-56`: «un doji no es de ningún color, no es contraria y corta la racha»).
>    - **La E de la reentrada.** La sostienen tres cosas: el código, donde `marcar_usada` va por zona y `marcar_rechazada` por punto (`zonas.py:404-420`, `:469-475`); el docstring (`zonas.py:41-42`); y ADR-0064, decisión 1. Las trazas de 01-29 y de 07-13 dan el mismo punto en las tres órdenes llenadas. El recuento 47/22/16 lo volví a obtener con `reentradas.py`: 5838 bytes, iguales a los del fichero guardado.
>    - **Las 14 «correcto».** La tabla coincide con `resumen_gates.txt`, que reproduje: 7369 bytes, iguales. La explicación está mal (b1), pero la conclusión se sostiene.
>    - **Las dos R de §2.f.** Coinciden con las tablas RN-004 de las trazas y con `a35-inicio` (líneas «Por sesion»: `liquidez_tomada:no` en las dos).
>    - **«Correcto» de los rechazos.** Lo confirman las restas de los `ticks.txt` y las velas marcadas, con la salvedad de b3.
> 2. **Nada anterior al día dev ni nada en dinero.** No encontré nada; no hay hallazgo «bloquea».
>    - Ninguna hora Z entre 16 y 23 en los anexos ni en el informe.
>    - Ninguna hora del trader antes de las 06:00 ni después de las 15:59 en las páginas extraídas.
>    - Ninguna fila tapada como «(antes del dia)», salvo el inicio de la ventana; ninguna «(antes del dia)» en las trazas.
>    - Ni «rompe la H4», ni datos de H4, ni USD, saldo, equity, PnL ni margen; solo «(saldo y equity omitidos)».
>    - El pivote de M15 más temprano que se imprime se formó a las 03:15Z.
>
> ### Lo que no pude comprobar
> - **El `make check`.** `make-check.log` no existe: no hay `SELLO` ni `PICO DE MEMORIA` que leer. Lo sustituye `.git/botsito-sello` = árbol de HEAD. Que nada escribiera mientras corría no se puede comprobar.
> - **Que la fila de HOLDOUT se escribiera antes de leer ninguna vela.** Entró en el mismo commit (f39e0da) que `contexto_h4.py` y su salida, y git no da un orden más fino.
> - **Las páginas HTML de `data/visor/`.** No las abro, por orden. Revisé el código de `extraer_pagina.py`, pero no que su salida sea fiel a cada página. Tampoco puedo comprobar que la sesión no abriera ninguna entera.
> - **Las órdenes «iguales a main».** No ejecuté el visor, `revisar_dia.py` ni `traza_por_cierre.py`, por orden. Me apoyo en `lotes.txt` y en el código de `comun_visor.ordenes_coinciden`, que compara las 7 primeras columnas.
> - **Los niveles de los pivotes de M15 formados a las 03:15Z y 03:30Z.** El nivel es el extremo de su racha. No verifiqué que ninguna vela de esa racha sea anterior a las 00:00Z; para eso harían falta unas 13 M15 seguidas del mismo color.
> - **Los cuatro comandos que negó la guardia.** No puedo comprobar que se partieran sin cambiar lo que medían.
> - **La CI.** No la consulté. La rama no tiene CI propia.
>
> ### Comandos ejecutados
> 1. `git branch --show-current && git merge-base main HEAD && git log --format='%h %s' main..HEAD && git diff --stat main...HEAD && git status --short`
> 2. `uv run python scripts/contrato_rama.py; git diff main --name-only | grep -v anexos/VISOR-CONSTRUCCION/; ls -la make-check.log …`
> 3. `git diff main...HEAD -- docs/validation/HOLDOUT-EXPOSICIONES.md PROJECT_STATE.md`
> 4. Varios `grep -nE` de horas Z entre 16 y 23, de horas del trader entre 00 y 05 y entre 16 y 23, de «antes del dia», «H4», «rompe la H4» y de dinero (usd, saldo, equity, pnl, margen, …) sobre `anexos/VISOR-CONSTRUCCION/` y el informe
> 5. `sed -n` sobre `src/botsito/engine/zonas.py`, `primitivas.py`, `cableado.py`, `cli.py`, `domain/estructura_m1.py`, `domain/pivotes_m15.py`; `docs/adr/0064*`, `0066*`, `0074*`, `0076*`, `0080*`; `CORRIDA-CONSTRUCCION.md:1230-1256`; `criterio_fidelidad.yaml:36-46`; `test_visor.py:366-402`; `VISOR-DIAS.md:38-42`
> 6. `grep` y `sed` sobre `dias/*.traza.txt`, `*.velas-*.txt`, `*.ticks.txt`, `*.pagina.txt`; `cat` de los `ticks.txt`; `grep` sobre `anexos/CORRIDA-CONSTRUCCION/a35-inicio…txt`
> 7. `uv run python docs/validation/anexos/VISOR-CONSTRUCCION/reentradas.py | tail -4` y `| wc -c` (5838 = el fichero)
> 8. `uv run python docs/validation/anexos/VISOR-CONSTRUCCION/resumen_gates.py <las 15 sesiones> | wc -c` (7369 = el fichero)
> 9. `uv run python docs/validation/anexos/VISOR-CONSTRUCCION/simular_cierre.py .`
> 10. Comparación con `md5sum` de las respuestas del consultor en el encargo y en el informe
> 11. `git diff f85fb1e HEAD --numstat -- docs/encargos/…`; `git show --stat f39e0da 8cceb46`; `git diff --numstat main...HEAD -- HISTORIA HOLDOUT PS`
> 12. `cat .git/botsito-sello; git rev-parse HEAD^{tree}`
> 13. `grep -n "^# Next Action HECHA · Y\|· O"` en HISTORIA; `grep "id: A-46"` en `ambiguedades.yaml`
> 14. Negados por la guardia y no rodeados: un `for f in …` y una ejecución de guion seguida de otra en el mismo comando (los partí como pide su mensaje). `solo_lectura.py` me negó un `git config`.

### 8.1 Lo que se hizo con los hallazgos del revisor

- **a1 (bloquea): arreglado.** `revisar_dia.py` recibe las dos carpetas en que escribe por
  argumentos obligatorios, `--dias` y `--paginas`, y ya no las saca de su ruta (`comun_visor.RAIZ`
  sigue saliendo de la ruta del guion, pero solo para LEER el repo y los datos). La pasada final de
  verificación se hizo con las dos carpetas FUERA del repositorio (`--dias` y `--paginas` en la
  carpeta de trabajo de la sesión): los 80 ficheros por día que escribió dan los mismos `sha256` que
  los de `anexos/VISOR-CONSTRUCCION/dias/` (los otros 4 son los `--velas`), y su registro, los mismos
  bytes que `lotes.txt`. Lo que
  pasó antes (seis pasadas de desarrollo en el repo real) va a §6 como desviación.
- **a2 (menor): arreglado.** §7 lleva el `SELLO`, la duración y el pico de memoria del `make check`
  de 304da27, leídos del log antes de commitear, y los del commit de estos arreglos.
- **b1 (importa): arreglado.** §2.e explica el reinicio del recuento: las zonas se cuentan desde la
  toma del escenario vigente, y cada toma de otra liquidez abre uno nuevo (ADR-0066). `resumen_gates.py`
  gana una sección que comprueba los 14 reinicios: los 14 coinciden con una toma de RN-004 de otro
  pivote (en 2026-08-11, el mismo nivel formado a otra hora). La conclusión no cambia.
- **b2 (importa): arreglado.** §2.d.4 dice que el recuento es una cota superior, con el caso de
  2026-01-05; la línea Y dice «hasta 47».
- **b3 (importa): arreglado y medido.** El respaldo de o1 de 2026-04-27 no es una hora sin ticks:
  los ticks se cargan desde `ventana_inicio` y la orden del primer cierre de la ventana lleva 1 ms
  antes (§4.3, punto 6, con sus líneas). §1.d y §2.g lo corrigen, y va como sexta línea de Technical
  Debt (la simulación del cierre sigue pasando: 24.724 bytes).
- **b4 y b5: arreglados.** La pregunta B dice que A-46 está RESUELTA, por qué B no la repite y que
  una respuesta (a) obliga a un `REOPEN`; y nombra la vela de las 10:54.
- **b6 (menor): arreglado.** §2.d.4 cuenta las tres sesiones con traza y dice que ADR-0066 enmienda
  las decisiones 2 y 3.
- **b7 (menor): arreglado.** §4.1 dice que HISTORIA ya tiene una Y y que el título de esta llevará
  nombre, o que el consultor puede elegir R o Z.
- **b8 (menor): arreglado.** §2.g dice lo que hace el filtro del guion y por qué la conclusión vale.
- **«Lo que no pude comprobar»:** el orden de la fila de HOLDOUT frente a la primera página no lo da
  git (entraron en el mismo commit, f39e0da); lo atestigua el texto de la propia fila, escrito antes
  de generar ninguna página, y §2.a. **Los pivotes de M15 formados de madrugada, medido:** el nivel
  de un pivote es el extremo de su racha de M15, y si la racha empezara el día UTC anterior el
  precio impreso podría ser de ese día (en 2026-07-01, el oculto). `pivotes_m15_del_dia.py` corre el
  mismo motor que la traza, reúne los pivotes que la traza imprime y cuenta, sin imprimir horas ni
  precios, cuántos tienen la racha o el nivel antes de las 00:00Z (salida en `pivotes_m15.txt`):
  **0 en los 20 días**, también en 2026-07-01 y 2026-07-14, los de los pivotes formados a las 03:30Z
  y 03:15Z; ningún pivote se quedó sin su vela contraria en las M15 del día.

      uv run python docs/validation/anexos/VISOR-CONSTRUCCION/pivotes_m15_del_dia.py caso-eurusd-2026-01-08 caso-eurusd-2026-01-29 caso-eurusd-2026-01-30 caso-eurusd-2026-04-17 caso-eurusd-2026-04-27 caso-eurusd-2026-07-01 caso-eurusd-2026-07-08 caso-eurusd-2026-07-09 caso-eurusd-2026-07-13 caso-eurusd-2026-07-14 caso-eurusd-2026-07-16 caso-eurusd-2026-08-03 caso-eurusd-2026-08-07 caso-eurusd-2026-08-11 caso-eurusd-2026-08-14 caso-eurusd-2026-08-19 caso-eurusd-2026-08-20 caso-eurusd-2026-08-21 caso-eurusd-2026-08-25 caso-eurusd-2026-08-27

## Estado

LISTA PARA REVISION, NO CERRADA (2026-10-18). Fases 0, 1 y 2 hechas: una E (la reentrada en un punto ya llenado, rama Y propuesta) y el resto correcto o R, con sus preguntas para V (§3); las líneas del cierre, preparadas y simuladas (§4); el revisor, con 1 «bloquea», 4 «importa» y 5 «menor», todos arreglados (§8.1); sin CI de Linux porque la rama no toca la plataforma (§7). El cierre en main solo con la orden de Aleks.

Rama lista para revisión, NO cerrada.

## 9 · Orden de cierre del consultor (2026-10-18)

Copiada tal cual:

> Modelo: Opus 5.5 · Esfuerzo: medio
>
> ORDEN DE CIERRE de trabajo/visor-construccion (consultor, 2026-10-18). Revisada la rama (VISOR-CONSTRUCCION.md entero, con el informe del revisor): se cierra. Copia esta orden tal cual al final de VISOR-CONSTRUCCION.md, en una sección «## 9 · Orden de cierre del consultor (2026-10-18)», y sigue la skill cerrar-rama (RITUAL.md) cuando Aleks escriba /cerrar-rama.
>
> 1. Antes del ritual, en la rama, un commit corto con make check sellado:
>    - Hallazgo del consultor que el revisor no vio (importa): §4.3, punto 4, mide que test_visor.py hace leer al visor el M1 entero de marzo (mes reservado) en cada make check, y la rama lo deja solo como deuda. Una lectura que ocurre y no está declarada se declara en HOLDOUT-EXPOSICIONES el mismo día en que se descubre, como se hizo con el calentamiento del arnés (fila del 2026-10-14). Añade una fila del 2026-10-18 que declare:
>      · esa lectura;
>      · desde cuándo ocurre: el commit que añadió test_por_la_cli_sobre_un_dia_dev_de_construccion_si_hay_datos, medido con git log;
>      · que solo calienta el sesgo, sin imprimir ninguna fecha ni ningún precio.
>      La línea de Technical Debt de §4.1 se queda, porque el arreglo es de código, y pasa a citar esa fila.
>    - Lección para el revisor (va a la fila de ERRORES-RECURRENTES): cuando una rama descubre una lectura de material reservado que ya ocurre, comprobar que queda declarada en HOLDOUT-EXPOSICIONES y no solo como deuda.
>
> 2. Tag: stable/F37t-visor-construccion (verifica que el último en HISTORIA es F37s).
>
> 3. En el commit del contrato (chore(cierre)), las líneas de §4.1 tal como están, con estas precisiones:
>    - La letra Y, aceptada. Su título en HISTORIA, cuando salga, llevará nombre, como el de O.
>    - O sale bajo «# Next Action HECHA · O · las comprobaciones en el visor · …».
>    - F, Y, V, R3.2 HECHA con su línea de Estado, R3.4 nueva, R4.1 y las seis líneas de Technical Debt: tal como están en §4.1.
>    - No añadas a PROJECT_STATE nada más que eso. Corre simular_cierre.py y test_hoja_de_ruta.py antes del commit. Si PROJECT_STATE pasa de 24.800 bytes, PARADA. La siguiente rama lo adelgaza.
>    - Fila de trabajo/visor-construccion en ERRORES-RECURRENTES.md con lo de §4.4 (los dos hallazgos del consultor de la PARADA 1, el acierto de contexto_h4.py y las dos lecciones de la sesión), el revisor (1 bloquea, 4 importa y 5 menor, todos arreglados o declarados; el bloquea, revisar_dia.py escribiendo en el repo real con la raíz sacada de su propia ruta) y el hallazgo del punto 1 con su lección.
>
> 4. El commit de estado tras el tag solo reemplaza Current Branch, Current Feature, Stable Main State y Last Stable Commit.
>
> 5. make check sellado y push atómico de main y del tag en un solo comando; Aleks confirma la regla ask con «1. Yes». Si el clasificador niega algún comando, no cambies de vía: PARADA, y lo lanza Aleks con «!».
>
> 6. CI de main: consúltala con gh run view. Si el clasificador lo niega, PARADA y la consulta Aleks con «!». Nunca con curl, con gh run watch ni con un guion. Con la CI en verde, borra la rama local (no hubo fix/ remota). Si sale roja, el arreglo va por una rama corta con su propia orden de cierre.
>
> 7. Informe final: sha de main, el tag, el run de la CI de main y su resultado, las ramas que quedan, el tamaño de PROJECT_STATE en bytes, y la fila nueva de HOLDOUT-EXPOSICIONES con su commit.

**Punto 1, hecho en la rama** (antes del ritual): la fila del 2026-10-18 en HOLDOUT-EXPOSICIONES
(«El VISOR lee el M1 entero de marzo en cada `make check`», desde `50045c8`, del 2026-09-25,
medido con `git log -S "def test_por_la_cli_sobre_un_dia_dev_de_construccion_si_hay_datos" --
tests/unit/test_visor.py`); la línea de Technical Debt de §4.1 la cita; la lección, en §4.4.
`simular_cierre.py` con la línea nueva: a, b y c sin problemas, los cuatro tests de PROJECT_STATE
pasan, 24.742 bytes simulados.
