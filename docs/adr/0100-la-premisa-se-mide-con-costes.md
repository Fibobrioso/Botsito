---
status: ACTIVE
date: 2026-11-24
phase: post-F14 (rama `trabajo/diagnostico-premisa`, R4.7 de la hoja de ruta; commit del pre-registro, antes de ninguna corrida y antes de que el backtest del trader llegue a nadie del proyecto)
---

# 0100 · La premisa se mide con un backtest del trader con costes y con dos diagnósticos de construcción, con la lectura escrita antes

> Decisión de Aleks del 2026-11-24, tras el puente del techo (ADR-0099, lectura «solo_juntas») y el
> contraste con el trader del 2026-11-23. Números y redacción del consultor, aprobados por Aleks el
> 2026-11-24. Entra en un commit propio de la rama, con `docs/plan/PREMISA-COSTES.yaml` y su test,
> antes de ninguna corrida y antes de que el backtest del trader llegue al repo o a nadie del
> proyecto: el orden de los commits es la prueba del pre-registro. El trader puede haber empezado ya
> a operarlo; no conoce esta lectura, y nadie del proyecto verá un resultado antes de su rama. No
> cambia ninguna cifra ya pre-registrada (ADR-0070, ADR-0092, ADR-0096, ADR-0098, ADR-0099,
> `criterio_fidelidad.yaml`, `META-TECHO-PAREJAS.yaml`, `PUENTE-TECHO.yaml`, `PREREGISTRO.md`) ni la
> salida de la meta, que sigue siendo C.

## Decision

### 1. Lo que se mide y por qué

El puente (ADR-0099) dejó tres cosas claras y dos abiertas. Claras: el simulador reproduce lo que se
publicó en septiembre; ninguna pieza sola saca al techo de «no gana»; y la forma en que el trader
opera de verdad (objetivo a 3 veces el stop, sin break even, entrando a su precio y sin las
operaciones de más de 100 lotes, la variante `todo_junto`) da, después de comisión, +0,285 R en
abril y agosto (sin lectura, con N = 71) y +0,022 R en los cuatro meses de construcción («no
concluyente» por el R; «no gana» por la lectura de ADR-0098 §2, porque incumple d)). Abiertas: si enero y julio son peores también para él o solo para nuestra réplica, y
si lo que no paga los costes es la estrategia o la forma en que pesamos cada operación.

El contraste del 2026-11-23 añadió que, según el trader, sus backtests de FX Replay no llevan
comisión ni spread (su respuesta entra con su `fb-` por su propia rama, ADR-0099 §6; la auditoría
«cazador», V01, ve indicios de que el spread sí está en las compras, y sigue abierta), y los totales
de sus libros que se vieron el 2026-11-24 (§7) van con un lote fijo. Con un riesgo fijo del 0,5 %
cada operación pesa lo mismo en R, y la comisión, fija por lote, se come las de stop más corto; con
un lote fijo cada operación pesa por sus pips. Son dos medidas distintas de la misma estrategia, y la
segunda no se ha hecho nunca.

> **RECUADRO de corrección (2026-11-25, `trabajo/contraste-trader`; el cuerpo no se toca).** La frase de este §1 «su respuesta entra con su `fb-` por su propia rama, ADR-0099 §6» no se cumple así: esa respuesta no tiene objetivo de `fb-` en el esquema (la premisa y el coste de FX Replay no son ninguno de los objetivos de `feedback/modelo.py`, y nada se cierra), y entra, sin registro de feedback, por `docs/validation/CONTRASTE-TRADER.md` (§6.3, el literal de la respuesta; §6.8, por qué no lleva `fb-`), con su captura en el corpus.

Se miden tres cosas, con la lectura de cada una escrita aquí:

1. **El backtest del trader con costes** (§2 a §4): su estrategia, decidida por él y en su
   plataforma, con spread y comisión. Es la medida de la premisa.
2. **Su registro frente a nuestra réplica, mes por mes** (§5), sobre los días `dev` de
   construcción. Es diagnóstico.
3. **El techo con lote fijo** (§6): las variantes `base` y `todo_junto` del puente, pesadas por pips
   en lugar de por R. Es diagnóstico.

Ninguna de las tres cambia un parámetro, una regla ni una decisión del motor (ADR-0092 §6). Lo que
§4 escribe para cada resultado es lo que el consultor propone al ADR de Aleks que resuelve la salida
C (ADR-0099 §7); ese ADR lo decide Aleks.

### 2. El backtest del trader: material y condiciones

- **Los meses:** dos meses de 2024 que el trader no haya operado nunca en backtest, uno de cada
  mitad del año: los que Aleks le pidió por escrito, o los que él declare por escrito antes de
  empezar. El consultor propone enero y julio de 2024, porque sus números de mes son los de
  construcción y la cuarentena del texto, que tapa por número de mes en cualquier año
  (`meses_libres`), dejará leer sus transcripciones. Si son otros, valen igual: sus transcripciones
  quedan tapadas por la cuarentena, y la medida, que sale del libro, no las necesita. Ningún mes de
  2025 (la puerta de rentabilidad de ADR-0092 §5 los usa, con su extensión hasta enero, y diciembre
  está en `meses_reservados.yaml`) ni de 2026.
- **Su régimen:** los meses de 2024 de este backtest son **material de construcción por este ADR**,
  para la premisa, desde el commit del pre-registro: no entran en `meses_reservados.yaml` (la regla
  del material recibido de `MIRAR-EL-MATERIAL.md` excluye los meses que ya son de construcción por su
  ADR), sus cifras son diagnóstico como toda cifra de construcción (ADR-0092 §6), y no son meses de
  la puerta de rentabilidad ni la sustituyen. No son `construccion` de `criterio_fidelidad.yaml`:
  no entran en el arnés ni en la fidelidad salvo por otro ADR. El commit del pre-registro lo escribe
  también en `CLAUDE.md` y en `MIRAR-EL-MATERIAL.md`, que listan los meses de construcción.
- **Las condiciones:** datos de OANDA, como siempre (qué proveedor sirve FX Replay es V01, abierta);
  spread de 0,2 pips (la cifra que propuso Aleks); comisión de 5 USD por lote de ida y vuelta (la del
  perfil de FTMO, puesta en su plataforma); el lote para arriesgar el 0,5 % en cada operación, para
  que opere como operaría la cuenta (las medidas de §3 salen de los precios y no dependen del lote);
  opera exactamente igual que siempre; graba en vídeo y con su voz las sesiones enteras; y exporta el
  libro completo de cada mes.
- **Si N < `n_minimo` al acabar los dos meses**, se añade un mes más de 2024 con número de mes de
  construcción (abril o agosto), declarado antes de empezar, de uno en uno, hasta un máximo de
  cuatro meses. La decisión de añadir mira solo N, nunca el resultado. Con cuatro meses y N <
  `n_minimo`, la lectura es «insuficiente».
- **Cuándo vale:** solo si el libro trae todas las operaciones de los días grabados y las
  condiciones se ven en el vídeo o en la configuración exportada. Si falta algo, la lectura es «no
  válida», se dice qué faltó y no se lee ninguna cifra.
- **Cómo entra:** SIN ABRIR y fuera del repo hasta su propia rama. Esa rama, por este orden:
  amplía a esos meses la lista de meses legibles de la guardia de Claude Code
  (`MESES_DE_DESARROLLO`), con sus tests, y comprueba que la guardia reconoce el nombre del fichero
  del libro; baja las velas M1 de esos meses de 2024 y mide el huso del libro (el procedimiento de
  `libros.yaml`); y lo declara en `libros.yaml` (solo añadir), en `vistos.yaml` y en
  `HOLDOUT-EXPOSICIONES.md`. Nadie del proyecto ve sus resultados antes de
  esa rama; si el trader los enseña por su cuenta, se declara el mismo día y la lectura sigue siendo
  la de aquí.

### 3. El backtest del trader: las dos medidas

Por operación, con la entrada, el stop inicial y el precio de salida del libro:

- **D**, la distancia de la entrada al stop inicial, en pips. Una operación sin stop inicial queda
  fuera, contada.
- **P**, los pips de precio: (salida − entrada) × dirección. Si la plataforma aplica el spread en
  los precios, ya está dentro; si no, la rama de entrada resta 0,2 pips y lo dice.
- **c**, la comisión en pips: 0,5 (5 USD por lote de ida y vuelta, a 10 USD el pip por lote).
- **R por riesgo** = (P − c) ÷ D: como la de ADR-0092 §3, sin swaps, con cada operación pesando
  lo mismo.
- **R con lote fijo** = (P − c) ÷ mediana de D, con la mediana sobre todas las operaciones medidas:
  cada operación pesa por sus pips. La mediana no mira ningún resultado.

Como control, el signo de P − c casa con el del resultado en USD del libro; si no casa en alguna
operación, se cuenta y se dice. Para las dos medidas, la esperanza y sus percentiles
`percentil_remuestreo` y `percentil_alto` por remuestreo por días, sobre los días de mercado de los meses medidos,
con o sin operaciones, y con las réplicas y la semilla del bloque `rentabilidad` de
`criterio_fidelidad.yaml` (como ADR-0092 §3 c).

### 4. El backtest del trader: la lectura

Para cada medida, con las cifras del bloque `rentabilidad` y el umbral del percentil alto de
`META-TECHO-PAREJAS.yaml`, en este orden:

- **gana**: N ≥ `n_minimo`, esperanza ≥ `esperanza_minima_r` y percentil `percentil_remuestreo` > 0;
- **no gana**: esperanza < 0, o percentil `percentil_alto` <
  `techo_no_gana_si_percentil_alto_por_debajo_de_r`;
- **no concluyente**: el resto.

«Insuficiente» y «no válida» (§2) van antes que las tres, y con ellas el backtest se lee como si no
hubiera llegado.

Lo que el consultor propone para cada combinación:

| Por riesgo | Con lote fijo | Qué significa | Qué propone para el ADR de la salida C |
|---|---|---|---|
| gana | cualquiera | La estrategia paga los costes con la gestión que pensábamos usar. | Se comprueban d), e) y f) con la serie del backtest; si se cumplen, se retoma la fidelidad (R4.6) y F17 sigue; si no, se lee como la fila de «no concluyente». |
| no gana o no concluyente | gana | La estrategia paga los costes pesando por pips; lo que no los paga es el riesgo fijo. | Se le pregunta al trader cómo dimensiona en una cuenta real. Una gestión distinta del 0,5 % entra solo por un ADR propio que cite su respuesta, comprueba d), e) y f) de la cuenta con esa gestión y se juzga en la puerta de ADR-0092 §5, nunca por esta cifra. |
| no concluyente | no concluyente | La muestra no decide. | Decide con F17 y el resto, sin pedir más meses salvo por N. |
| no gana | no gana | Ni siquiera él, en su plataforma y con costes, gana. | Elige entre replantear la estrategia con el trader (todo cambio sale de su palabra, ADR-0092 §6) y parar. |

Las dos combinaciones que no salen en la tabla («no gana» por riesgo con «no concluyente» con lote
fijo, y «no concluyente» por riesgo con «no gana» con lote fijo) se leen como la fila de «no
concluyente».

### 5. Diagnóstico: su registro frente a nuestra réplica, mes por mes

Sobre los días `dev` de los cuatro meses de construcción, por mes y por los dos bloques {abril y
agosto} y {enero y julio}, y sobre las mismas operaciones en las dos series: las que la variante
`todo_junto` abre (sin las que deja fuera por el tope de lotes, que se cuentan aparte):

- del **registro del trader** (las filas de su libro de esos días, por el lector de `corpus/libro.py`,
  como la serie anotada de `VIABILIDAD-TRADER.md`): N; ganadoras, perdedoras y break even
  (R > +0,2; R < −0,2; el resto); y la media de su R bruto, con R = (salida − entrada) × dirección ÷
  D, a sus precios y sin costes. Es la columna de salida que ADR-0098 §1 no abrió para la meta;
  aquí se lee para un diagnóstico, sin releer la meta, y solo de los días `dev`;
- de **nuestra réplica**, la variante `todo_junto` del puente: lo mismo, con su R antes de comisión
  (que lleva el spread de Dukascopy, y el registro no, o solo en parte: V01).

La **brecha** de un bloque es la media del R del registro menos la de la réplica, sobre las mismas
operaciones. La lectura, escrita antes de medir:

- **la réplica pierde más en enero y julio**, si la brecha de {enero y julio} supera a la de {abril y
  agosto} en más de 0,20 R: hay algo que no replicamos en esos meses, y se busca;
- **enero y julio son peores también para él**, en caso contrario.

Además, como dato y sin lectura: de las ganadoras del registro (R > +0,2), cuánto retrocedieron
entre su entrada y su salida, en fracciones de D, con los ticks de Dukascopy en el lado que
cerraría la posición y con el desfase de `desfase_puntos` de `PUENTE-TECHO.yaml`, por tramos
[0; 0,5), [0,5; 0,8), [0,8; 1,0) y 1,0 o más. Una ganadora que retrocede 1,0 D o más tocó su stop
inicial en nuestros precios: o el registro no lo recoge o las dos series de precios no casan ahí
(A-16). Se cuenta, y la cuenta va como pregunta al trader o a A-16, sin cambiar nada.

### 6. Diagnóstico: el techo con lote fijo

Las variantes `base` y `todo_junto` de `PUENTE-TECHO.yaml`, sin tocar ninguna pieza (las que
`todo_junto` deja fuera por el tope de lotes siguen fuera, y se dice), con el «R con lote fijo» de
§3: el R neto de cada posición por su D, entre la mediana de D de las posiciones del mismo conjunto.
Sobre los cuatro meses, con la lectura de §4 para `todo_junto` (gana, no gana o no concluyente); y aparte sobre abril y agosto, con
su propia mediana y sin lectura. La de `base` es solo un dato. Su lectura es un dato más para el ADR
de la salida C, sin consecuencia propia.

### 7. Lo visto, declarado (ADR-0070 punto 4)

Antes de fijar todo lo de arriba, el consultor y Aleks han visto:

- el puente entero (`PUENTE-TECHO.md`, sus tablas por variante sobre los cuatro meses y sobre abril y
  agosto, y el cierre) y el contraste con el trader del 2026-11-23;
- el 2026-11-24, en una conversación del trader con otro asistente que Aleks compartió por enlace, los
  totales mensuales de sus libros de enero, abril y agosto de 2026 (operaciones, ganadoras,
  perdedoras y break even, y el resultado en USD con 1 lote fijo), declarados en
  `HOLDOUT-EXPOSICIONES.md`. Con ellos, el consultor estimó a mano que su registro con lote fijo deja
  un margen positivo de entre 1 y 1,5 pips por operación tras unos 0,8 pips de costes, sin el efecto
  del spread en las barreras. Es lo que motivó §6;
- y lo que de ahí se deriva para §5: el R bruto medio de la serie anotada de abril y agosto está
  publicado (+0,98, `VIABILIDAD-COMISION.md` §3, sobre 77 operaciones y no sobre las de
  `todo_junto`); el R bruto medio de `todo_junto` por bloque se deriva de `PUENTE-TECHO.md` (0,649 en
  abril y agosto; con los cuatro meses, unos 0,17 en enero y julio); así que la brecha de abril y
  agosto, unos +0,33 R, ya se podía estimar, y de enero se vieron sus totales. El margen de 0,20 R
  se fijó con eso a la vista.

Nadie ha visto ningún backtest del trader con costes, ni el registro de enero y julio en R, ni el
techo con lote fijo.

Las piezas nuevas son el «R con lote fijo», los tramos de R del registro (±0,2), el margen de 0,20 R
de §5, los tramos de retroceso, la regla de los meses de §2 y las condiciones del backtest (el spread
de 0,2 pips lo propuso Aleks). Se eligieron con lo de arriba a la vista, y se declara.

> **RECUADRO de corrección (2026-11-24, `trabajo/diagnostico-premisa`; el cuerpo no se toca).** Este §7 dice que «el consultor y Aleks» vieron los totales de la conversación del trader con otro asistente: los vio solo el consultor; Aleks pasó el enlace sin leerla (fila de `HOLDOUT-EXPOSICIONES.md` del 2026-11-24). Ese mismo día, después de escribir este ADR, Aleks y el consultor vieron además, detrás de una captura de configuración de FX Replay que mandó el trader, su panel de cuenta con agregados que incluyen meses reservados; está declarado en la misma fila y ninguna cifra se usa (ADR-0021 §2). Ninguna de las dos cosas cambia una cifra ni una lectura de este ADR ni de `docs/plan/PREMISA-COSTES.yaml`.

### 8. Dónde viven las cifras

En `docs/plan/PREMISA-COSTES.yaml`, que fija `tests/unit/test_premisa_costes.py` por su sha256, con
un test que rompe a propósito con una cifra cambiada. Las del bloque `rentabilidad`, las de
`META-TECHO-PAREJAS.yaml` y las de `PUENTE-TECHO.yaml` no se copian: el yaml remite a ellas. Las
condiciones del backtest son instrucciones para la plataforma del trader, no parámetros del bot.
Ninguna cifra en `src/` (ADR-0002).

## Problema que resuelve

Con el puente, la salida C ya no se puede resolver sin saber si la estrategia del trader paga los
costes en su propia plataforma, y si lo que no paga es la estrategia o la forma en que la pesamos.
Las dos preguntas se pueden contestar en días, sin FTMO y sin gastar ningún mes reservado.

## Alternativas consideradas

1. Esperar a F17 y decidir con el spread real de FTMO.
2. Lo elegido: el backtest del trader con costes y los dos diagnósticos, con las lecturas escritas
   antes.
3. Pedirle al trader que repita con costes meses que ya operó (enero, abril, julio o agosto de 2026).
4. Medir el techo con lote fijo sin pre-registro, como diagnóstico suelto.
5. Pasar ya a un lote fijo como gestión del bot.
6. Medir el registro con el simulador, sin abrir la columna de salida del libro, como ADR-0098 §1
   (que descartó abrirla para la meta porque allí no hacía falta).
7. Meter los meses de 2024 en `meses_reservados.yaml` al llegar, como cualquier material recibido.

## Por que elegimos esta opcion

Contesta la premisa con las decisiones del propio trader, en meses que nadie del proyecto ha visto y
que no están en ningún plan, y separa la estrategia de la gestión del dinero sin cambiar nada del
bot. F17 sigue haciendo falta, pero no decide esto.

## Por que descartamos las demas

- **La 1** deja sin contestar si la estrategia paga los costes con sus propias decisiones.
- **La 3** tiene memoria: él ya sabe cómo salieron esos meses.
- **La 4** elegiría la medida después de ver los totales, sin decir qué se hace con el resultado.
- **La 5** cambiaría la gestión del bot por una cifra (ADR-0092 §6), sin la palabra del trader y sin
  confirmarla en meses no vistos.
- **La 6** mide las entradas del trader con nuestras salidas, y la pregunta de §5 es justo por sus
  salidas reales: aquí la columna sí hace falta, y solo de los días `dev` (ADR-0021 §1).
- **La 7** taparía por número de mes enero y julio de 2026, contra ADR-0078 y ADR-0079, y estos meses
  no hace falta tenerlos ciegos: la medida está escrita antes y es de la estrategia del trader, no
  del bot.

## Impacto

- `docs/plan/PREMISA-COSTES.yaml` y `tests/unit/test_premisa_costes.py`, nuevos, en el commit del
  pre-registro, con este ADR, su fila del índice, una frase en `CLAUDE.md` y otra en
  `MIRAR-EL-MATERIAL.md` (los meses de 2024 de §2) y tres recuadros: al final de ADR-0092 §6, al final
  de ADR-0098 §1 (el registro del trader se lee aquí para un diagnóstico, no para releer la meta) y
  al final de ADR-0099 §7 (el ADR de la salida C lee también la lectura de §4, si ha llegado, y si
  no, dice que falta).
- La rama mide §5 y §6 con un guion en anexos, sin tocar `src/` ni `knowledge/`.
- El backtest del trader entra por su propia rama, que aplica §2 a §4 tal cual.

## Fecha / fase

2026-11-24; post-F14, rama del diagnóstico de la premisa (R4.7, NA:F).

## Estado

ACTIVE (decisión de Aleks del 2026-11-24; números del consultor aprobados el 2026-11-24;
pre-registra la lectura del backtest del trader con costes y dos diagnósticos de construcción en
`docs/plan/PREMISA-COSTES.yaml`, fijado por `tests/unit/test_premisa_costes.py`; declara de
construcción los meses de 2024 de ese backtest; aplica ADR-0092 §6 con recuadros; no cambia ninguna
cifra pre-registrada ni la salida C)
