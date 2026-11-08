---
status: ACTIVE
date: 2026-11-07
phase: post-F14 (rama `trabajo/metodo-fidelidad-rentabilidad`, R3.7 de la hoja de ruta; R de la Next Action)
---

# 0092 · El bot se construye por fidelidad y se juzga por rentabilidad para operar en vivo (enmienda ADR-0043, ADR-0070 y ADR-0053 §6)

> Decisión de Aleks del 2026-10-29 (Next Action R; hoja de ruta R3.7). Umbrales y decisiones del
> consultor en su respuesta a la PARADA de `trabajo/metodo-fidelidad-rentabilidad` (2026-11-07),
> escritos ANTES de ninguna corrida nueva del arnés, sobre lo medido en
> `docs/validation/METODO-FIDELIDAD-RENTABILIDAD.md` §0. Cuando este ADR dice «la respuesta, punto
> n», es esa respuesta (copiada tal cual en el informe y al final del encargo). Recuadros en
> ADR-0043 (Decision, «Fuera del criterio» y «Cambios»), ADR-0070 (puntos 3 y 4) y ADR-0053 §6;
> NOTA en la cabecera de `docs/plan/MASTER_PLAN.md`; fila del índice. La NOTA de
> `docs/validation/PREREGISTRO.md` que pedía la respuesta (punto 12) no está: cualquier cambio de
> ese fichero sin commitear hace fallar `tests/unit/test_puerta_holdout.py` en el `make check` que
> sella el commit, porque la puerta compara el fichero con HEAD (`cases/holdout.py`,
> `_commiteado_y_sin_cambios`); lo que tendrá que llevar está en §13 y la decisión, en la PARADA 2
> del informe de la rama. Las cifras viven en `knowledge/cases/criterio_fidelidad.yaml`
> (ADR-0002); las funciones, puras, en `src/botsito/cases/criterio_fidelidad.py`; el arnés solo las
> escribe.

## Decision

### 1. La fidelidad es la herramienta de construcción, por operación y por criterios

La fidelidad se sigue midiendo por OPERACIÓN entera, como fija ADR-0043, sin cambiar nada de él
(unidad, emparejamiento, métricas, tolerancias de 3 puntos y 15 minutos). Y se mide además por
CRITERIOS, pieza a pieza (la respuesta, punto 0):

- **Entran, pieza a pieza:** la sesión y la dirección; la entrada (el 0 de la caja); el stop (el
  0,8); y el instante del llenado.
- **Entra, derivado y aparte:** el sesgo de H4, como el rn003 de la sesión frente a la dirección del
  trader. Se informa aparte porque no necesita ninguna orden del bot.
- **No entran como piezas propias:** la caja (el 1), porque la del trader se deriva solo de su
  entrada y su stop con la misma regla del 0,8 que usa el bot, así que con la entrada y el stop
  comparados no añade información y sí arrastra la duda de A-56; y el punto, porque su nivel es el
  0, ya comparado, y su vela no se deriva del caso.
- **No comparable:** la liquidez de M15. El caso del trader no la trae (`cases/ingesta.Operacion`:
  instante, sesión, dirección, entrada y stop); se declara así y no puntúa.
- **Tolerancias:** entrada 3 puntos e instante 15 minutos, las de ADR-0043; stop 3 puntos, campo
  nuevo `tolerancia_stop_puntos`, entero como `tolerancia_entrada_puntos`, con el mismo valor y la
  misma razón: los dos son un nivel leído en otra serie (A-16).
- **Sin umbral de paso.** La fidelidad por criterios es herramienta de construcción y diagnóstico.

### 2. La cascada por criterios, contra las órdenes del bot

Se compara contra las ÓRDENES que el bot colocó, llenadas o no (la respuesta, punto 1). Para cada
operación del trader:

1. ¿hay alguna orden del bot en el mismo (día, sesión, dirección)? De las que haya se toma la más
   cercana en ENTRADA y, a igualdad, la de colocación más cercana en instante;
2. la entrada de esa orden a ≤ `tolerancia_entrada_puntos`;
3. su stop a ≤ `tolerancia_stop_puntos`;
4. la orden se llenó y su llenado está a ≤ `tolerancia_instante_min` del llenado del trader. Si no
   se llenó, la operación cae en «en el nivel, no llenada».

Cada operación del trader se informa por el ÚLTIMO escalón que alcanza. Aparte, en recuento, las
órdenes del bot en un (día, sesión, dirección) sin ninguna operación del trader. Las cifras de la
cascada se dan por mes y en total, diciendo qué cuentan y sobre qué salida. La cascada es la
función pura `cascada_por_criterios` de `cases/criterio_fidelidad.py`; para el escalón 3 el criterio
lleva el stop del caso (`arnes._operacion`), y el emparejamiento por operación de ADR-0043 da lo
mismo con él que sin él.

### 3. La rentabilidad es la puerta para operar en vivo

La rentabilidad es condición NECESARIA de todo lo que decida operaciones en vivo (la respuesta,
punto 2). Unidad: el **R neto por operación** = PnL neto en USD (con la comisión del perfil, 2,50
por lote y lado, ADR-0090 §3, y los swaps) entre el riesgo en USD al colocar, tal como lo calcula la
cuenta al dimensionar (lote, distancia al stop y el valor del punto del contrato; ninguna fórmula
nueva). Se mide sobre las operaciones LLENADAS del bot, en la fase FONDEADA del perfil (`fase:
fondeada`; `firma_fases` la tiene), con el deslizamiento de §4 y sobre los meses de §5. **Pasa
solo si se cumplen todas:**

- a) N ≥ `n_minimo` (100) operaciones llenadas;
- b) esperanza (media del R neto) ≥ `esperanza_minima_r` (+0,10 R);
- c) el percentil `percentil_remuestreo` (5) de la media del R neto, por remuestreo POR DÍAS de
  mercado (`replicas_remuestreo` 10.000 réplicas, `semilla_remuestreo` 20261107), es > 0. **La
  forma la fijó el consultor en la PARADA 2** de `trabajo/metodo-fidelidad-rentabilidad` (punto 2),
  tal como la implementa `percentil_por_dias` (`remuestreo_por_dias`): cada réplica sortea con
  reemplazo tantos días como días de mercado corridos, con o sin operaciones; su cifra es la media
  del R neto de TODAS las operaciones de los días sorteados (agrupada, no la media de las medias de
  cada día); una réplica sin ninguna operación no cuenta, y la salida dice cuántas se descartaron
  por eso sobre las 10.000; el percentil es el de rango inferior, floor(percentil × (n − 1) / 100)
  sobre las medias ordenadas; el generador es `random.Random` de Python con la semilla;
- d) en ningún día la pérdida diaria, en la magnitud y con la base que vigila la firma
  (`firma_magnitud_vigilada`, `firma_base_perdida_diaria`), llega a `perdida_diaria_max` (el 3 %)
  del capital inicial. El límite de la firma es el 5 %: 2 puntos de margen;
- e) la menor equity del tramo no baja del capital inicial menos `perdida_total_max` (el 6 %), es
  decir, del 94 %. El límite es el 10 %: 4 puntos de margen;
- f) la cuenta no entra en SUSPENDIDA en ningún momento.

Los bloqueos de RN-032 no son criterio: si la cuenta llegó a donde RN-032 bloquea, ya incumplió d)
o e). **Si no se cumple a), el resultado es «insuficiente»** y se aplica la extensión de §5;
**cualquier otro incumplimiento es «no pasa».** Las funciones (R neto, remuestreo por días,
drawdown, N y el veredicto) son puras en `cases/criterio_fidelidad.py`.

### 4. El deslizamiento, pendiente de F17, con su regla escrita ahora

El deslizamiento no tiene modelo (`deslizamiento_fijo_puntos` 0 en `knowledge/simulador/llenado.yaml`;
ADR-0090 §7, ADR-0051 §4) y ADR-0002 prohíbe la cifra inventada (la respuesta, punto 3):

- la medida se corre UNA vez con `deslizamiento_fijo_puntos` en 0, sin tocar `llenado.yaml`;
- cuando F17 (heredado 10) mida el deslizamiento de las órdenes stop, se recalcula SIN volver a
  correr el bot: a cada llenado de orden stop y a cada cierre por stop o a mercado se le resta la
  MEDIANA medida (los cierres por objetivo no se tocan), y con el PnL recalculado se vuelven a
  evaluar b), c), d) y e) de §3; d) y e) sobre la curva recompuesta operación a operación, sumando
  el ajuste al día de cada cierre. Los lotes y los bloqueos de RN-032 no se recalculan, y el informe
  lo dice;
- además, la esperanza recalculada con el percentil `percentil_deslizamiento_f17` (90) de F17 tiene
  que ser > 0;
- **la puerta no puede dar «pasa» antes de F17** (`deslizamiento: pendiente_F17`);
- el informe de la medida da también el deslizamiento por llenado, en puntos, que llevaría la
  esperanza a +0,10 R (el punto de equilibrio), sin decidir nada con él.

### 5. Los meses no vistos: junio a noviembre de 2025, una sola vez

(La respuesta, punto 4.)

- **Los meses:** 2025-06 a 2025-11, seguidos, con la cuenta ARRASTRADA en todo el tramo (como
  operará) y en la fase fondeada. El simulador corre una fase por ejecución y no las encadena: pasar
  el reto y la verificación es otra pregunta, con su objetivo y sus días mínimos, que se informa
  aparte si alguna vez se mide, y no es la puerta.
- **Por qué esos:** no hay material del trader de 2025 salvo diciembre (NA:I; `"2025-12"` en
  `meses_reservados.yaml`), que queda fuera; no hay velas ni ticks de 2025 bajados (`data/manifests/`
  solo tiene 2026); el bloque cubre verano, los dos cambios de hora de 2025 (Europa el 26 de octubre,
  que mueve el día de riesgo; EE. UU. el 2 de noviembre, que mueve la rejilla H4 anclada a las 17:00
  de Nueva York) e invierno, que es como empezará el vivo; y no gasta febrero de 2026 (heredado 6,
  sin levantar) ni ninguna partición del holdout.
- **La extensión, fijada ahora:** si al acabar noviembre de 2025 N < 100, se añaden con la misma
  spec mayo, abril, marzo, febrero y enero de 2025, en ese orden y de uno en uno, hasta N ≥ 100; si
  con enero sigue N < 100, «insuficiente» y no pasa. La decisión de añadir mira solo N, nunca el
  resultado.
- **Dónde viven:** en el bloque `rentabilidad` de `criterio_fidelidad.yaml` (`meses`, `extension`)
  y aquí. El arnés los niega como niega todo lo que no es construcción (ADR-0048 §7). NO entran en
  `meses_reservados.yaml`, que es para material del trader y tapa por NÚMERO de mes en cualquier año
  (`cases/holdout.py`, `tapados = {int(mes[5:7]) ...}`): taparía julio y agosto de construcción,
  contra ADR-0078 y ADR-0079. Tampoco en `construccion` ni en `medida`.
- **Antes de correr la medida**, que fija su propia rama con su ADR (ADR-0070 punto 6: el comando no
  existe):
  - la spec sellada: el hash de `strategy_spec.yaml`, `parametros.yaml`, el perfil de
    `knowledge/cuentas/` y `knowledge/simulador/llenado.yaml`, y el sha de `src/`, en
    `PREREGISTRO.md`, que rellena G;
  - el calendario de cierres renovado hacia atrás hasta enero de 2025 (`RENOVAR-CIERRES.md`,
    condición 1, leída como la lee NA:I; hoy empieza el 2025-12-04);
  - las velas M1 y los ticks de Dukascopy de esos meses con su manifiesto, bajados y declarados
    según los heredados 7 y 9: el 7 porque la guardia de `stable/F14-cobertura` saca junio del
    universo de un paquete ciego, y junio de 2025 es un junio; el 9 porque `manifiestos_del_prefijo`
    toma todo lo que lleve el prefijo del kit y un manifiesto nuevo con ese prefijo cambia
    `universo()` (ninguno de 2025 solapa con 2026, pero entra en el universo);
  - la deuda del spread supuesto para minutos sin ticks, que se busca por la hora de pared de
    Madrid (Technical Debt), nombrada como riesgo de noviembre y de la extensión de invierno;
  - la construcción en el umbral de ADR-0070 (la línea «habilita medir», ya pre-registrada).
- **Una sola ejecución.** Si se repite por un fallo técnico, se declara con su causa y la spec no
  cambia entre las dos. Si no pasa, esos meses quedan escritos en el yaml como `vistos_rentabilidad`
  y no vuelven a medir nunca (no son construcción: no tienen casos del trader); la siguiente medida
  usa otros meses, que fijará su ADR.

### 6. Contra optimizar sobre resultados

Es el mecanismo de la Regla viva «Parametros no se optimizan contra resultados» (que hasta hoy no
tenía ADR: sale de `MASTER_PLAN.md` §0):

- ningún parámetro de la spec se elige ni se ajusta por la cifra de rentabilidad;
- la cifra se mide UNA vez, sobre meses que el bot no ha visto, con la spec sellada (§5);
- si no pasa, se vuelve a construir, y los meses medidos no vuelven a medir (`vistos_rentabilidad`);
- **las métricas de rentabilidad que el arnés imprima sobre CONSTRUCCIÓN son diagnóstico**, y
  ninguna rama de spec o de motor se justifica con ellas: las ramas de spec citan al trader (`ev-`,
  `fb-`), nunca una cifra de rentabilidad.

### 7. El papel de la fidelidad, de F26, F27 y F35

(La respuesta, punto 5.)

- La fidelidad, por operación y por criterios, es la herramienta de construcción.
- **ADR-0070 sigue gobernando cuándo se mide mayo**: su línea «habilita medir…» (la fija su punto
  5) y sus tests no cambian. De ADR-0070 este ADR enmienda solo una condición de la corrida que
  cuenta, el camino de la cuenta (§8).
- **F26** (el holdout de fidelidad) deja de ser la condición necesaria para operar en vivo y queda
  como diagnóstico que se informa en el memorando. Sus condiciones previas (F26 lee la diferencia
  3,00/3,75 como conocida y la mide en A-56; dos días del universo de la sesión 1 sin partición)
  siguen siendo de cualquier métrica sobre reservados; la rentabilidad de §5 no lee reservados ni
  material del trader.
- **F27** (sensibilidad y ventaja, DSR, N de pruebas) no se sustituye: sigue en el plan y F35 sigue
  dependiendo de ella. Su N es el de ejecuciones de backtest, no el N de operaciones de §3.
- **F35** sigue siendo el memorando y la decisión humana de Aleks: la puerta de §3 es condición
  necesaria, no la decisión.
- La segunda Regla viva de `PROJECT_STATE.md` se reescribe en el cierre de la rama: «La rentabilidad
  pre-registrada de ADR-0092, medida una vez sobre meses que el bot no ha visto, precede a todo lo
  que decida operaciones en vivo (F29, F30 y lo de F31-F32 que dependa de ellos), y la fidelidad
  sigue siendo la herramienta de construcción; la capa de plataforma de ADR-0082, que nunca decide
  una operación, puede ir antes.»

### 8. El camino de la cuenta: una cuenta por mes en construcción

(La respuesta, punto 6.) En construcción, y en mayo cuando se mida, **una cuenta por mes**; en los
meses no vistos, arrastrada en todo el tramo (§5). Enmienda ADR-0053 §6 («La cuenta PERSISTE en todo
el tramo») y la condición de la corrida que cuenta de ADR-0070 punto 3. Es una condición del
recorrido, no una opción: `OPCIONES_QUE_NO_CAMBIAN_LA_CORRIDA` no cambia, y
`--diagnostico-cuenta-diaria` sigue siendo diagnóstico. **La implementa una rama de motor corta,
propia, ANTES de la re-corrida que cuenta** (`trabajo/cuenta-por-mes`, con un test que rompe en
`main`), no la rama de este ADR ni la re-corrida. Por qué: en vivo la cuenta nunca salta de enero a
abril, y hoy el arrastre entre meses no contiguos es un hecho del código (`cli.py`, que ordena los
meses, y `cableado.py`, que guarda la cuenta entre días; METODO-FIDELIDAD-RENTABILIDAD.md §0.c).

> **NOTA (2026-11-07, `trabajo/cuenta-por-mes`; no reescribe el cuerpo).** Lo que empieza de nuevo
> al cambiar de mes, en `MotorCableado.correr_dia`, con una condición y no con una opción: el mes
> (el AAAA-MM de la clave del día corrido, la misma de `mercados` y `trazas_broker`) del día que se
> va a correr es distinto del del último día corrido. Empiezan de nuevo **la cuenta, desde el
> capital del perfil, el seguidor del tope del trader y el «primero en tocar un límite»**, que pasa
> a ser de cada cuenta mensual: el seguidor va con la cuenta (con la diaria, «nace cada día con la
> cuenta», ADR-0089) y el primer toque es un hecho de cada cuenta. La racha de pérdidas de RN-036, que el encargo pone en la
> misma lista, queda pendiente de la respuesta del consultor a la PARADA condicional de
> `docs/validation/CUENTA-POR-MES.md`, porque la spec la describe «contando en TODOS los dias de la
> corrida»: hasta esa respuesta no se reinicia. Nada más: el bróker y el estado de estrategia ya
> empiezan de cero cada día. Las cuentas cerradas se conservan en orden, solo para la salida;
> ninguna decisión las lee. `--diagnostico-cuenta-diaria` no cambia: reinicia cada día la cuenta, el
> seguidor y la racha, su primer toque sigue siendo de toda la corrida, y la condición de mes no
> hace nada ni conserva cuentas. La medida de rentabilidad sobre los meses no vistos (§5), que se
> quiere arrastrada en todo el tramo, no existe todavía: su rama dirá, con su ADR, cómo se arrastra
> allí.

### 9. Las tolerancias por operación quedan, y la regla de A-16

Los 3 puntos y los 15 minutos de ADR-0043 quedan (la respuesta, punto 7). Regla escrita ANTES de
medir A-16: si la mediana de la distancia M1 de A-16 supera 3 puntos, o la proporción dentro del
rango baja del 50 %, cada cifra de fidelidad lo dice («la cobertura tiene un techo que no es del
bot») y nace en Technical Debt una línea para que la decisión la tome un ADR propio. En la rama de
este ADR la tolerancia no cambia, salga lo que salga.

### 10. A-16 se mide, y sigue ABIERTA

(La respuesta, puntos 8 y 9.) Se mide en la rama de este ADR
(`anexos/METODO-FIDELIDAD-RENTABILIDAD/medir_a16.py`): para cada operación del trader de los días
dev de construcción, la distancia de su entrada al rango de la M1 BID de Dukascopy del minuto del
llenado y al tick más cercano de ese minuto del lado en que se llenaría (BID en la venta, ASK en la
compra) y, aparte, de los dos lados; N, mediana, p90 y proporción dentro del rango, en total y por
mes, y cuántas sin ticks; sin mes anterior. A-16 queda ABIERTA con `resuelve_en: [F26]`, sin tocar
`knowledge/spec/`; su cierre va a la primera rama que toque `knowledge/spec/` y pague la deuda del
panel de FTMO. Las medidas previas de la serie del trader se nombran con ella:
`BLOQUE-DE-LA-CAJA.md` §2.3 (leyendas OHLC, mediana +2 puntos, OANDA por encima),
`ABRIL-Y-LA-CAJA.md`, `LA-CAJA-DEL-29-DE-ABRIL.md` y `VIABILIDAD-TRADER.md` §4.

### 11. El sesgo del material sin vídeo, como diagnóstico

(La respuesta, punto 11.) La re-corrida que cuenta da la cifra entera y, además, la misma sin las
operaciones del bot que acabaron en break even (el desenlace `break_even` de `clasificar_cierre`: el
mecanismo, no un PnL cero) en los libros sin vídeo: enero, agosto y abril salvo el 29. Julio,
provisional como grabado hasta T (R2.4). Es diagnóstico: no entra en ningún umbral.

La lista vive en el bloque `material_sin_video` de `criterio_fidelidad.yaml` (`meses`,
`dias_con_video`, `provisionales_con_video`, `fuente`; PARADA 2, punto 1), y `cargar_criterio`
exige que el bloque exista, que sus meses y días sean de construcción, que ningún día con vídeo
caiga fuera de `meses` y que ningún mes esté a la vez en `meses` y en `provisionales_con_video`. Un
mes provisional cuenta como CON vídeo, y la salida lo dice. La sección de ADR-0092 del informe del
arnés lleva la línea DIAGNÓSTICO: la cascada y la esperanza sin esas operaciones, y cuántas se
quitaron. Si llega la exportación de agosto con vídeo (Q) o T comprueba julio, el bloque se cambia
en la rama que lo traiga, con su fuente (S-14: `ev-v15-011912-0ae32588`, `ev-v16-003421-b824b770`).

### 12. Lo visto, declarado

Por ADR-0070 punto 4 («cambiarlo exige un ADR nuevo que declare lo visto»):

- **Lo visto por el consultor antes de decidir** (la respuesta, L): el informe de la fase 0 entero,
  con las tablas de §0.c (165 de 198 operaciones del trader en días con la cuenta congelada, sobre
  `anexos/RESPALDO-M1/cuenta-arrastrada.txt`) y de §0.e (las distribuciones de Δ de las dos salidas
  de `anexos/RESPALDO-M1/`); de la línea base vigente, su curva de equity, su saldo y equity finales
  y el bloqueo de RN-032 por el límite total desde el 2026-01-20 (ADR-0070 punto 3, NOTA del
  2026-10-29) con su ritmo de llenadas; y la esperanza del TRADER en R, con comisión y remuestreo,
  de `VIABILIDAD-TRADER.md` §2 y `VIABILIDAD-COMISION.md`. No existe ninguna esperanza en R del BOT
  ni ninguna cifra suya sobre mes alguno fuera de construcción. Lo que se apoya en algo de eso, lo
  dice: el camino de la cuenta (§8) sale de un hecho del código, no de la cifra, pero la cifra se
  vio; el criterio e) y la forma del remuestreo se parecen a lo que VIABILIDAD-TRADER hace con
  el trader, y por eso el umbral de esperanza del bot es más alto que el borde estrecho que ahí se
  mide; las tolerancias no cambian.
- **Las salidas del arnés sobre construcción commiteadas antes de este ADR**, todas ya vistas:
  - las dos corridas que cuentan por ADR-0070 punto 3: `anexos/RECORRIDA-CONSTRUCCION/cuenta-arrastrada.txt`
    y `anexos/RESPALDO-M1/cuenta-arrastrada.txt` (la línea base vigente, NOTA del 2026-10-29), con
    sus diagnósticos `diaria.DIAGNOSTICO.cuenta=diaria.txt` en las dos carpetas y
    `anexos/RECORRIDA-CONSTRUCCION/diff-linea-base.txt`;
  - las corridas con diagnóstico de `anexos/CORRIDA-CONSTRUCCION/`, `anexos/SESGO-H4-COLOR/`,
    `anexos/MARGEN-LOTE/` y `anexos/PUNTO-USADO/` (los ficheros `*.DIAGNOSTICO.*.txt`);
  - las salidas de la raíz de `docs/validation/`: `ARNES-MOTOR-LINEA-BASE.txt`,
    `CABLEADO-SIMULADOR-LINEA-BASE.txt`, `HUECOS-MOTOR-LINEA-BASE.txt`,
    `ORDEN-STOP-O-LIMITE-SALIDA.txt`, `PREPARACION-A21-SALIDA.txt`, `SESGO-H4-DIAGNOSTICO.txt`,
    `VERIFICACION-A21-SALIDA.txt` y `VERIFICACION-A35-A44-SALIDA.txt`;
  - las páginas, trazas, contextos y ticks del visor sobre 20 días de construcción de
    `anexos/VISOR-CONSTRUCCION/dias/` (DIAGNÓSTICO, con órdenes y operaciones del bot y del
    trader por día), y lo que vio el visor por caso en los once días dev de
    `anexos/SELLO-RESPALDO-M1/` (sus prototipos y censos);
  - y todo lo DERIVADO de esas salidas y commiteado en sus anexos: los patrones (`patrones*.txt`),
    los censos (`censo-respaldo.txt`, `censo-cierre-*.txt`), `costes-y-sesiones.txt`,
    `entradas-antes-alternancia.txt`, las listas de S-14 (`lista-s14.txt`, `sesiones-s14.txt`) y
    los `diff-linea-base.txt`.
  (La lista sale de `grep -rlE '^(\[[^]]*\] )?CONJUNTO: construccion' docs/validation/` del
  2026-11-07, más los ficheros de diagnóstico, las páginas del visor y lo derivado de los anexos
  (revisor de la rama, b2); las corridas que no dejaron salida commiteada se citan en el informe de
  su rama.)
- **Mayo no se ha visto.** Ninguna salida del motor sobre el conjunto de medida: ninguna salida
  commiteada lleva 2026-05 en su CONJUNTO, ningún comando lleva `--meses 2026-05`, y el arnés niega
  todo mes de medida (`engine/arnes.py`, `validar_meses`). La cláusula «Cambios» de ADR-0043 se
  dispara con la primera salida del motor sobre la MEDIDA, que no se ha producido: este ADR enmienda
  el criterio SIN quemar mayo. Lo que obliga a declarar lo visto es ADR-0070 punto 4.

### 13. Dónde viven las cifras, y qué tiene que llevar PREREGISTRO.md

- `knowledge/cases/criterio_fidelidad.yaml` (ADR-0002; `test_no_business_literals`):
  `tolerancia_stop_puntos: 3` y el bloque `rentabilidad` (`fase`, `n_minimo`, `esperanza_minima_r`,
  `percentil_remuestreo`, `replicas_remuestreo`, `semilla_remuestreo`, `perdida_diaria_max`,
  `perdida_total_max`, `deslizamiento`, `percentil_deslizamiento_f17`, `meses`, `extension`,
  `vistos_rentabilidad`), y el bloque `material_sin_video` (§11), cargados y validados por
  `cargar_criterio`; un yaml sin ellos no carga.
- `PREREGISTRO.md`, para la rentabilidad (la ampliación de «Que tiene que llevar» y de la fila de
  `MASTER_PLAN.md` §H es de G): la métrica y su cálculo (§3); los umbrales; los meses, la extensión y
  por qué esos (§5); la fase; el hash de la spec sellada y el sha de `src/` (§5); el tratamiento del
  deslizamiento (§4); y qué se hace si no pasa (§5, `vistos_rentabilidad`).

## Problema que resuelve

Hasta hoy la única medida del bot era la fidelidad por operación entera (ADR-0043), y era también,
por ADR-0082 y la Regla viva, la condición para todo lo que decide operaciones en vivo. Esa cifra
mezcla dónde se separa el bot (una caja, una entrada, un sesgo) en un solo sí o no, y tiene sesgos
que no son del bot: la otra serie de precios (A-16), una cuenta que se arrastra entre meses no
contiguos y queda congelada por RN-032 (METODO-FIDELIDAD-RENTABILIDAD.md §0.c), un material sin
vídeo en que el trader se saltaba las sesiones de break even (S-14) y unas tolerancias fijas. Y un
bot puede ser fiel y no ganar, o ganar sin copiar cada operación: lo que se juega en vivo es la
cuenta. Aleks decidió el 2026-10-29 que la fidelidad sea la herramienta de construcción y la
rentabilidad la puerta; faltaba el criterio, pre-registrado antes de ver ninguna corrida nueva.

## Alternativas consideradas

1. Seguir con la fidelidad por operación como única medida y como puerta (lo de hasta hoy).
2. Fidelidad por criterios con la caja y el punto como piezas propias (la opción (a) entera de la
   fase 0, punto 0).
3. La rentabilidad medida sobre las particiones reservadas, en la misma apertura que F26, o sobre
   mayo, o sobre febrero de 2026.
4. El deslizamiento con una forma sin cifra (el punto de equilibrio con un umbral).
5. Una cuenta reiniciada en cada hueco del material, en vez de una por mes.
6. Lo elegido.

## Por que elegimos esta opcion

- Separa las dos preguntas: la fidelidad dice dónde se separa el bot del trader, y la rentabilidad,
  si el bot gana dinero dentro de las reglas de la firma.
- Los umbrales se escriben antes de ninguna corrida nueva, y lo que ya se vio se declara (§12).
- La rentabilidad no necesita etiquetas del trader: los meses de 2025 no gastan su material ni
  ninguna partición, y quedan fijados hoy, con su fase y su extensión.
- Ninguna cifra se inventa: el deslizamiento que falta solo puede venir de F17 (§4).
- Ningún umbral ya pre-registrado se mueve: ADR-0043 y la línea de ADR-0070 quedan.

## Por que descartamos las demas

- **La 1** deja la puerta en una cifra que no mide lo que se juega en vivo y que tiene los sesgos
  de arriba.
- **La 2** añade piezas redundantes (la caja del trader se deriva de su entrada y su stop con la
  regla del bot) o derivadas que A-56 discute, y el nivel del punto ya es la entrada.
- **La 3** gasta una partición o mayo, o febrero de 2026, el único mes ciego limpio confirmado por
  el trader, en una medida que no necesita su material.
- **La 4** solo traslada la cifra inventada al umbral del punto de equilibrio.
- **La 5** da hoy las mismas cuatro cuentas, pero en un mes de medida reiniciaría la cuenta en cada
  día reservado intercalado.

## Impacto

- `knowledge/cases/criterio_fidelidad.yaml`: `tolerancia_stop_puntos` y el bloque `rentabilidad`; la
  cabecera cita la NOTA de ADR-0043 «Cambios». Ningún campo existente cambia.
- `src/botsito/cases/criterio_fidelidad.py`: la carga de los campos nuevos y las funciones puras de
  §2, §3 y §4.
- `src/botsito/engine/arnes.py` y `cableado.py`, SOLO salida (la respuesta, punto 10): el stop del
  caso en el criterio, la tabla «### Posiciones» y las líneas de la cascada y de las métricas de
  rentabilidad, marcadas «diagnóstico» en construcción. Ninguna decisión ni ningún llenado cambia.
- Recuadros en ADR-0043, ADR-0070 y ADR-0053 §6; NOTA en la cabecera de `MASTER_PLAN.md`.
  `PREREGISTRO.md` no cambia (sigue SIN RELLENAR); lo que tendrá que llevar para la rentabilidad, en
  §13.
- Ramas que nacen: `trabajo/cuenta-por-mes` (§8), antes de la re-corrida que cuenta; la rama de la
  medida de rentabilidad con su ADR y su comando (§5); G amplía PREREGISTRO y `MASTER_PLAN.md` §H (y
  la fila de F30, que depende de F26).

## Fecha / fase

2026-11-07 · post-F14, rama `trabajo/metodo-fidelidad-rentabilidad` (R3.7; R de la Next Action).

## Estado

ACTIVE
