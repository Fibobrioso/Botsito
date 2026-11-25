---
status: ACTIVE
date: 2026-11-23
phase: post-F14 (rama `trabajo/puente-techo`, R4.7 de la hoja de ruta; commit del pre-registro, antes de ninguna corrida)
---

# 0099 · La salida C se resuelve midiendo primero: el puente del techo pieza a pieza, F17 rediseñado y el contraste con el trader, con una lectura escrita para cada resultado

> Decisión de Aleks del 2026-11-23, tras la auditoría profunda del 2026-11-22/23
> (`docs/validation/AUDITORIA-PROFUNDA-2026-11.md`, copiada tal cual en esta rama) y la revisión del
> consultor. Números y redacción del consultor, aprobados por Aleks el 2026-11-23. Entra en un
> commit propio de la rama del puente, con `docs/plan/PUENTE-TECHO.yaml` y su test, antes de que la
> rama corra ninguna variante: el orden de los commits es la prueba del pre-registro. No cambia
> ninguna cifra ya pre-registrada (ADR-0043, ADR-0070, ADR-0092, ADR-0093, ADR-0096, ADR-0098,
> `PIVOTES-SESION-7.yaml`, `META-TECHO-PAREJAS.yaml`, `criterio_fidelidad.yaml`, `PREREGISTRO.md`)
> ni la salida de la meta, que sigue siendo C. Añade a lo que ADR-0098 §3 C manda revisar una
> medida que C no pedía (recuadro allí) y aplica ADR-0092 §6 a esa medida (recuadro allí).

## Decision

### 1. Qué se decide hoy y qué no

La salida C de ADR-0098 dice que el techo del trader no gana con nuestros costes y pide revisar
los costes y la premisa antes de seguir. La auditoría encuentra que eso no basta para decidir:

- la comisión es la misma en lo que se creía y en el techo (5 USD por lote de ida y vuelta,
  ADR-0090 §3), así que no explica la diferencia; la caída está en el R antes de comisión;
- el techo aplica la regla tal como el trader la dicta (stop en el 0,8, objetivo a 3 veces la caja,
  break even de RN-014, entrada con orden stop) a unas operaciones cuyo registro no la sigue del
  todo: ADR-0040, enmendado por ADR-0073, midió 26 de 38 ganadoras con el objetivo entre 3,00 y
  3,75 veces la distancia al stop, y el techo lo pone a 3,75;
- la salida C es firme frente a lo que ADR-0098 §3 C manda revisar (el deslizamiento, el sesgo del
  material sin vídeo), y no lo es, sin signo conocido, frente a dos piezas que no manda revisar,
  el objetivo (A-56) y la geometría de la zona que dispara el break even (ADR-0061 §4), ni frente
  a una que sí manda revisar pero nunca se ha medido a esta escala: la serie con el modelo de
  entrada (A-16);
- en el repo no hay ninguna fuente de que el trader gane en una cuenta real con esta estrategia (el
  contraste con él está en marcha, §6).

Por eso hoy se decide **el método**, no si la estrategia gana:

1. No se graba ninguna sesión de fidelidad (sigue R4.7). La siguiente se prepara.
2. Antes de decidir si se sigue y cómo, se miden tres cosas: el puente del techo pieza a pieza
   (§2 a §4, en esta rama); F17 rediseñado (§5, en su rama); y el contraste de la premisa con el
   trader (§6, de Aleks).
3. No se mide la rentabilidad de 2025 (ADR-0092 §5): gastaría de una vez meses que no vuelven, la
   puerta no puede dar «pasa» antes de F17 (ADR-0092 §4) y la línea «habilita medir» sigue en «no».
4. Lo que resuelve la salida C es el ADR siguiente de Aleks (§7), que este ADR deja acotado.

### 2. El puente: el techo de ADR-0098 §1 con una pieza cambiada cada vez

Sobre los mismos días `dev` de los meses de `construccion` de `criterio_fidelidad.yaml`, con el
modelo de ADR-0098 §1 sin tocar una pieza salvo la que nombra cada variante, el mismo bróker
simulado, la misma cuenta por mes y las mismas funciones de medida. La lista es cerrada y su orden
está en `docs/plan/PUENTE-TECHO.yaml`:

- **`base`**: el techo tal cual. Es el control: tiene que repetir el bloque M1 de
  `anexos/RECORRIDA-CONSTRUCCION-3/meta.txt` línea a línea. Si no lo repite, no se lee nada.
- **Una pieza suelta sobre `base`:**
  - `objetivo_sobre_el_stop`: el objetivo a `objetivo_rr` veces la distancia de la entrada al stop
    del caso (3,00), en lugar de 3 veces la caja derivada (3,75). Es lo que predicen los dos
    supervivientes de ADR-0040 §2;
  - `sin_break_even`: RN-014 no mueve el stop;
  - `entrada_al_precio_del_caso`: la posición se abre en el precio y el instante del caso, sin
    orden stop ni modelo de llenado (como hacía `scripts/viabilidad_comision.py`); no hay «no
    colocables»;
  - `sin_las_de_mas_de_100_lotes`: quedan fuera, contadas, las operaciones cuyo lote por riesgo,
    antes de limitarlo, pasa de 100 lotes (la exclusión de `VIABILIDAD-COMISION.md` §2; son las de
    stop más corto, las que más comisión pagan en R);
  - `desfase_menos_2`: la entrada, el stop y el objetivo, 2 puntos por debajo (el `DESFASE_PUNTOS`
    de `scripts/viabilidad_trader.py`);
  - `spread_menos_1`, `spread_menos_2` y `sin_spread`: el ask de cada tick, 1 o 2 puntos más cerca
    del bid sin cruzarlo, o igual al bid.
- **`todo_junto`**: las cuatro primeras a la vez. Es la geometría de la V1 de
  `VIABILIDAD-COMISION.md` sobre el simulador de hoy y los cuatro meses.
- **De vuelta**: `todo_junto` con una sola pieza del techo repuesta, una variante por pieza (cuatro).
  Con las sueltas, enseña si las piezas se suman o dependen unas de otras.
- **El cierre del puente**, leído solo sobre abril y agosto: `v1_de_hoy` (`todo_junto`, sin el
  cierre al final de la H4 y con `desfase_menos_2`) frente a la V1 publicada con 5 USD (70
  operaciones, +0,70 R antes de comisión y +0,34 R después), y `v2_de_hoy` (lo mismo con el stop
  y el lote en 0,8 veces la distancia) frente a la V2 publicada (67, +0,88 y +0,47). El puente
  «cierra» si N queda a 3 operaciones o menos y la esperanza neta a 0,10 R o menos de la publicada.

Cada variante imprime, sobre los cuatro meses y, aparte, sobre abril y agosto juntos: N, las no
colocables, las de break even movido y **las que cierran en el break even**, los cierres forzosos,
la esperanza antes y después de comisión, los percentiles 5 y 95 por remuestreo por días (la
función, las réplicas y la semilla del bloque `rentabilidad`), y d), e) y f) por cuenta. No imprime
ninguna operación con su R, ningún R por clase de setup, por sesión ni por dirección (ADR-0098 §4 c),
ningún precio y nada anterior al día `dev` al que pertenece.

### 3. Cómo se lee

Cada variante se lee **por el R**, con las cifras ya fijadas (`criterio_fidelidad.yaml`, bloque
`rentabilidad`, y `META-TECHO-PAREJAS.yaml`), sobre los cuatro meses:

- **gana**: N ≥ 100, esperanza ≥ +0,10 R y percentil 5 > 0;
- **no gana**: esperanza < 0, o percentil 95 < +0,10 R;
- **no concluyente**: el resto.

Los criterios d), e) y f) se dan al lado, como dato y sin entrar en esta lectura: miden la cuenta
del trader sin los frenos que el bot sí lleva (ADR-0098 §1, «ninguna otra regla abre o cierra») y
dependen del orden de las operaciones, y el puente pregunta por piezas del R. Esta lectura es
nueva y se eligió sabiendo que `base` incumple d) y e); se declara en §8. No sustituye a la lectura
de ADR-0098 §2, que el guion imprime también para cada variante.

El puente entero se lee así, en este orden:

- **una pieza basta**: alguna variante suelta deja de dar «no gana»;
- **solo juntas**: ninguna suelta, pero `todo_junto` deja de dar «no gana»;
- **ni juntas**: `todo_junto` da «no gana».

Son ocho variantes sueltas y basta una para la primera lectura, sin corrección por comparar varias
veces: por eso la lectura solo dice dónde mirar primero, y no prueba nada sobre la pieza.

### 4. Qué se hace con cada lectura, y qué no se hace con ninguna

Ninguna lectura cambia un parámetro, una regla ni una decisión del motor, y ninguna sustituye al
techo ni a la salida C: releer la meta con otro modelo pide un ADR nuevo que declare lo visto
(ADR-0098 §5). Lo que el puente decide es **dónde se comprueba primero la premisa**:

- **Una pieza basta.** La pieza nombra a quién se le pregunta y qué se mide:
  - `objetivo_sobre_el_stop`: A-56 deja de esperar a F26 y se mide, en su rama, donde el material
    traiga la caja (ADR-0040 §2): los días `dev` de julio grabados en vídeo, si la herramienta en
    pantalla la enseña. Sigue siendo una medición: al trader no se le vuelve a preguntar la regla
    (ADR-0073 §3), salvo que el ADR siguiente lo cambie. Si lo medido cambia la regla, entra por
    su rama con su fuente, y después un ADR relee la meta;
  - `sin_break_even`: la zona del break even (ADR-0061 §4, A-13) es lo primero del bloque técnico
    y del bloque de días de la sesión siguiente, cuando se pueda grabar;
  - `entrada_al_precio_del_caso`, `desfase_menos_2` o alguna de spread: decide F17 (§5), que pasa
    a ser la rama siguiente, y la pregunta al trader por el precio que ve en FX Replay y por sus
    costes (§6);
  - `sin_las_de_mas_de_100_lotes`: queda como dato. No se añade ningún filtro por tamaño de stop
    (ADR-0081 descartó «no operar» esas operaciones porque elegirlo sería ajustar contra
    resultados) y no se le vuelve a preguntar al trader: A-57 está RESUELTA.
- **Solo juntas.** La regla dictada, entera, se separa de su registro, y ninguna pieza lo explica
  sola. Decide el contraste con el trader (si en real hace lo que dicta o lo que muestra su
  registro); F17 sigue.
- **Ni juntas.** Con la geometría de su registro, sin break even, con sus entradas y sin los stops
  más cortos, los cuatro meses no ganan en nuestro simulador con la comisión de FTMO. Lo que se
  creía eran dos meses. Solo sus resultados reales con costes, leídos como fije un ADR (§6), o un
  spread de FTMO claramente menor (§5), reabren la premisa; si no, el ADR siguiente decide entre
  cambiar de objetivo y parar.

Si el puente no cierra (§2), se dice, se da el residuo sin explicar y las lecturas de arriba valen
igual: salen de los cuatro meses, no del cierre.

Es ADR-0092 §6 aplicado a esta medida, como su NOTA del 2026-11-09 lo aplicó a la ablación por
regla: las cifras del puente son diagnóstico de construcción; las ramas de spec citan al trader
(`ev-`, `fb-`) o un hecho de la plataforma, nunca un R; y lo que opere en vivo lo juzga la
rentabilidad de ADR-0092 §3 sobre meses no vistos, no esta medida.

### 5. F17, rediseñado

`MASTER_PLAN.md` define F17 como un grabador de ticks y spread, y la hoja de ruta (A.5) dice que
«también mide el deslizamiento». Un grabador que no coloca órdenes no puede medirlo. F17 pasa a
tener tres partes, en una prueba gratuita de FTMO (una cuenta DEMO; ADR-0082 D6 deja la capa solo
en DEMO hasta F35) y en su rama:

- **el historial, antes que nada**: el servidor de la demo ya sirve ticks reales al Strategy
  Tester (`EA-CONEXION.md`, medido un solo día). Se mide hasta dónde llegan hacia atrás y con qué
  calidad, con el criterio escrito antes (huecos dentro de la ventana, minutos sin ticks y
  coherencia con su propio M1; un recuento por día no basta, porque el tester genera ticks donde
  faltan). Si cubren los meses de construcción, se exportan y se congelan con su hash, y el spread
  de FTMO sale de ahí sin esperar al grabador. Usarlos como fuente de una medida pide un ADR que
  enmiende ADR-0005 y ADR-0024 §4;
- **el grabador** de ticks de EURUSD (bid, ask e instante), del que sale el spread de FTMO por
  hora, comparable con el de Dukascopy, para lo que el historial no cubra;
- **la medida de las órdenes stop**: un guion aparte del EA de la capa, que hoy no envía órdenes
  (`tests/contract/test_capa_mt5.py`), que coloca órdenes stop con lotes del orden de los del bot, espaciadas y muy por
  debajo del tope de peticiones (ADR-0067), y registra de cada una el nivel, el tick que la
  dispara, el precio y el instante del llenado y los lotes; y lo mismo en los cierres por stop y a
  mercado.

La referencia del deslizamiento es el precio del llenado menos el del tick que dispara la orden en
FTMO: el simulador ya cobra el hueco entre el nivel y el tick. Es una precisión nueva de la regla
de ADR-0092 §4, escrita con el techo ya visto (§8); la regla (la mediana y el percentil 90) no
cambia. El spread de FTMO se lee contra el puente, como diagnóstico: vale la
fila `spread_menos_1` o `spread_menos_2` cuyo número sea el mayor que no pase de la diferencia
mediana medida entre los dos spreads en las horas de la ventana; si FTMO no es más barato, ninguna.

### 6. El contraste con el trader

Empezó el 2026-11-23: Aleks le mandó por WhatsApp cinco preguntas del consultor que no llevaban
ninguna cifra ni resultado nuestro (ADR-0098 §3 C), no repetían ninguna pregunta ya contestada y no
llevaban A-56 al trader (ADR-0073 §3). Contestó el mismo día por escrito y por audio. Las capturas
y los audios van al corpus, a «Mensajes del trader», fuera de git. Lo que dijo, lo que se le enseñó
durante el intercambio y su registro entran por su propia rama, con su `fb-` donde toque, y el ADR
de §7 los lee; este ADR no los resume. Si comparte un historial de una cuenta real o de fondeo,
llega SIN ABRIR y fuera del repo: quién lo lee, qué y cuándo lo fija antes un ADR (con ADR-0072
como precedente), porque sus días pueden caer en meses reservados.

### 7. Lo que resuelve la salida C

Un ADR de Aleks, que se escribe cuando estén la lectura del puente, las respuestas del trader y
F17, o, como tarde, en la semana en que lleguen los ingenieros (hacia el 2026-12-03, ADR-0098 §6)
con lo que haya, diciendo qué falta. Ese ADR elige entre: seguir con las sesiones de fidelidad
(R4.6) con la regla corregida por el trader, si la hay; probar el bot sobre precios de FTMO grabados
(la sombra en diferido de R7.3, con su condición de entrada reescrita); o cambiar de objetivo o
parar. Y declara lo visto. Hasta entonces R4.7 sigue ABIERTA.

> **RECUADRO de ADR-0100 (2026-11-24, `trabajo/diagnostico-premisa`; el cuerpo no se toca).** El ADR de Aleks que resuelve la salida C lee también los dos diagnósticos de ADR-0100 §5-§6 y la lectura del backtest del trader con costes (ADR-0100 §4), si ha llegado; si no, dice que falta, como dice este §7 de lo demás.

### 8. Lo visto, declarado (ADR-0070 punto 4, al estilo de ADR-0098 §5)

Antes de fijar las variantes y las lecturas, el consultor y Aleks han visto:

- **La meta** (`RECORRIDA-CONSTRUCCION-3.md` §4): 198 operaciones, 7 no colocables y 191 llenadas;
  esperanza −0,239 R; percentiles 5 y 95, −0,450 y −0,026; d) 4,88 % y e) 92,05 %; break even
  movido en 79 y 7 cierres por RN-002; el equilibrio en −2,52 puntos por llenado afectado; julio,
  −0,245 en 64; las parejas, 29, «ni una cosa ni otra»; salida C.
- **`VIABILIDAD-COMISION.md`**, con 5 USD, sobre abril y agosto: V1, 70 operaciones, +0,70 R antes
  de comisión y +0,34 después [−0,15; +0,85]; V2, 67, +0,88 y +0,47 [−0,13; +1,08]; la anotada, 77,
  +0,98 y +0,56 [+0,05; +1,08]; fuera por el tope de 100 lotes, 7 en V1 y 10 en V2.
- **ADR-0040 y ADR-0073**: 26 de 38 ganadoras con el objetivo en [3,00; 3,75); la regla, dicha por
  el trader tres veces; A-56, abierta.
- **La auditoría profunda**: su aritmética sobre cifras publicadas (la comisión del techo entre
  0,34 y 0,67 R por operación, y el techo antes de comisión entre +0,10 y +0,43 R); que el techo
  comparte con V1 el stop y con V2 la relación de 3,75; y sus tablas de piezas. No mide ningún R
  nuevo.

- **Las respuestas del trader del 2026-11-23** (§6), que llegaron después de fijar las variantes y
  no movieron ninguna.
- **La auditoría «cazador» del 2026-11-23** (`docs/validation/AUDITORIA-CAZADOR-2026-11-23.md`,
  copiada tal cual en esta rama), que también llegó con las variantes ya fijadas y no movió
  ninguna. No mide ningún R nuevo. De ella se ha visto, sobre cifras publicadas: que V3 y V4 de
  `VIABILIDAD-COMISION.md`, que solo se distinguen por el objetivo, dan +0,62 y +0,56 R antes de
  comisión (bajar el objetivo mueve poco la media); su cota de lo que valdría apagar el break even
  (+0,27 R como mucho, con un supuesto generoso); su cuenta de que con spread cero el techo
  quedaría entre −0,04 y +0,03 R; y que 15 de 111 compras del trader, y ninguna de 87 ventas, caen
  fuera del rango de la M1 de Dukascopy. De ella sale la primera parte de §5.

Nadie ha visto el techo con una pieza cambiada. La lectura por el R sin d), e) y f), el 100 de los
lotes, el 2 del desfase, los 1 y 2 puntos de spread y las tolerancias del cierre (3 operaciones y
0,10 R) y la referencia del deslizamiento de §5 son las piezas nuevas: el 100 y el 2 se copian de
las medidas de septiembre; lo demás se eligió con lo de arriba a la vista, y se declara. Con el
total, el bloque de julio de `base` y el subtotal de abril y agosto, el R de enero de `base` se
puede derivar, y en las demás variantes el de enero y julio juntos: se sabe y se acepta, porque un
mes no es una clase de setup, y no se decide nada por mes.

### 9. Dónde viven las cifras

En `docs/plan/PUENTE-TECHO.yaml`, que fija `tests/unit/test_puente_techo.py` por su sha256, con un
test que rompe a propósito con una cifra cambiada (como `test_meta_techo_parejas.py`). Las de
ADR-0092 §3 y ADR-0098 §2 no se copian: el yaml remite a `criterio_fidelidad.yaml` y a
`META-TECHO-PAREJAS.yaml`. Ninguna cifra en `src/` (ADR-0002).

## Problema que resuelve

ADR-0098 §3 C dejó la decisión en un ADR de Aleks «con lo que salga» de revisar los costes y la
premisa. Lo que manda revisar no puede cambiar el signo del techo (el deslizamiento en una orden
stop solo empeora; el sesgo del material sin vídeo, por dirección razonada y no medida, también), y
las piezas que sí podrían no se han medido nunca por separado. Decidir hoy si se sigue sería
decidir sin saber si lo que no gana es su estrategia o nuestra lectura de ella.

## Alternativas consideradas

1. Seguir con R4.6 tras F17 y el contraste, sin medir nada más.
2. Lo elegido: medir primero (el puente, F17 rediseñado y el contraste), con las lecturas escritas
   antes, y decidir con un segundo ADR.
3. Tomar ya como objetivo probar el bot sobre precios de FTMO grabados, corrigiendo día a día.
4. Medir ya la rentabilidad sobre 2025, desatando la línea «habilita medir».
5. Parar todo hasta que el trader conteste.
6. Medir solo el techo con el objetivo a 3,00, como diagnóstico suelto y sin ADR.

## Por que elegimos esta opcion

Contesta con días `dev` de construcción, que no son holdout, y en una rama, cuál de las piezas
separa la regla dictada de su registro; las preguntas al trader no cuestan nada y ya salieron; F17
hace falta en cualquier caso (ADR-0092 §4); y con las lecturas escritas antes, el R solo puede
decir dónde preguntar, no qué cambiar.

## Por que descartamos las demas

- **La 1** gasta sesiones del trader acercando el bot a un techo que no gana.
- **La 3** es la mejor herramienta si el problema resulta ser de precios, pero hoy le faltan el
  grabador, un proveedor de datos nuevo y dos ADR, y lo primero que necesita es F17.
- **La 4** quema meses irrepetibles para confirmar, lo más probable, un «no».
- **La 5** deja sin usar dos medidas baratas que no dependen de él.
- **La 6** mide una pieza elegida después de ver la cifra y sin decir qué se hace con el
  resultado: no sería un pre-registro (ADR-0070 punto 4).

## Impacto

- `docs/plan/PUENTE-TECHO.yaml` y `tests/unit/test_puente_techo.py`, nuevos, en el commit del
  pre-registro, con este ADR, su fila del índice y dos recuadros: al final de ADR-0092 §6 y al
  final de ADR-0098 §3. Una enmienda en `RUMBO-2026-11.md` §4 y una NOTA en `MASTER_PLAN.md`, en
  otro commit de la rama.
- La rama construye el guion del puente en anexos, sin tocar `src/` ni `knowledge/`, y su informe
  da la lectura.
- Hoja de ruta, en la orden de cierre de esa rama: R4.7 cita este ADR y sus tres medidas; una
  entrada nueva en R4 para el puente; A.5 con F17 rediseñado; R6.0 y la línea de Metas, con lo que
  ADR-0082 (recuadro del 2026-11-22) y ADR-0098 §6 ya dicen.

## Fecha / fase

2026-11-23; post-F14, rama del puente (R4.7, NA:F).

## Estado

ACTIVE (decisión de Aleks del 2026-11-23; números del consultor aprobados el 2026-11-23;
pre-registra el puente del techo y sus lecturas; añade una medida a ADR-0098 §3 C con recuadro y
aplica ADR-0092 §6 con recuadro; no cambia ninguna cifra pre-registrada ni la salida C)
