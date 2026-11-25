---
status: ACTIVE
date: 2026-11-22
phase: post-F14 (rama `trabajo/recorrida-construccion-3`, la corrida (3) de la Next Action F, R4.3 de la hoja de ruta; commit del pre-registro, antes de ninguna corrida)
---

# 0098 · La meta se mide en la corrida (3): el techo del trader y el R de las parejas, con una salida escrita para cada resultado

> Decisión de Aleks del 2026-11-22 (la «opción 2» del chat de ese día, no la de
> AUDITORIA-2026-11-21.md §1: antes de la corrida (3), un ADR que pre-registra qué se mide y qué se
> hace con cada resultado). Números y redacción del consultor, aprobados por
> Aleks el 2026-11-22. Entra en un commit propio de la rama de la corrida (3), justo después del de
> apertura, con `docs/plan/META-TECHO-PAREJAS.yaml` y su test, antes de que la rama corra nada: el
> orden de los commits es la prueba del pre-registro. No cambia ninguna cifra ya pre-registrada (ADR-0043,
> ADR-0070, ADR-0092, ADR-0093, `PIVOTES-SESION-7.yaml`, `criterio_fidelidad.yaml`,
> `PREREGISTRO.md`). Sí enmienda dos cosas: el alcance de ADR-0092 §6, con recuadro (§3 de este
> ADR), y R5.7 de la hoja de ruta, que deja de ser solo diagnóstico (en la orden de cierre).

## Decision

### 1. Qué se mide, en la corrida (3), sobre días dev de construcción y sin holdout

Las dos medidas usan solo los días `dev` de los meses de `construccion` de
`knowledge/cases/criterio_fidelidad.yaml` (hoy 2026-04, 2026-07, 2026-08 y 2026-01), comprobados
con `casos_reservados` y declarados el día que se corran en `HOLDOUT-EXPOSICIONES.md`. Ningún mes
de `medida`, ninguna partición, ningún mes de `rentabilidad` (2025) y ningún material sin abrir.

**M1 · El techo.** Las operaciones del trader de esos días (198 en la última cuenta,
`RECORRIDA-CONSTRUCCION-2.md` §1.1; el informe da la cifra del día) se repiten con el mismo bróker
simulado, la misma cuenta y las mismas funciones de la spec que usa el bot en la corrida (3). El
modelo queda fijado aquí, antes de ver ningún R, porque cada pieza mueve el techo y sus efectos ya
se vieron en `VIABILIDAD-COMISION.md` (lo declara §5):

- **Entrada:** una orden stop en la entrada del caso (la orden de A-47, en el 0 de ADR-0064 y
  ADR-0092 §1), colocada al cierre de la vela M1 anterior al minuto de su llenado. Si en ese cierre
  el precio ya está del otro lado de la entrada y la orden no se puede colocar, cuenta como «no
  colocable»; si se coloca y no se llena en la sesión, como «no llenada». Ninguna de las dos entra
  en el R, y se cuentan aparte.
- **Stop y objetivo:** el stop del caso, leído como su 0,8; el 1 se deriva de la entrada y el stop
  con la misma regla del 0,8 que usa el bot (ADR-0092 §1), redondeado al punto alejándose de la
  entrada; el objetivo, por `objetivo_rr` sobre la distancia de `base_calculo_objetivo`, como en el
  bot. Una operación del caso sin stop no entra, y se cuenta.
- **Sin desfase de serie:** no se aplica ninguna corrección entre su serie y Dukascopy (A-16 sigue
  ABIERTA; ADR-0002).
- **Gestión:** el break even (RN-014), el objetivo y el cierre forzoso (RN-002) de la spec vigente,
  más el cierre de fin de día que el motor aplica a toda posición. Donde el motor tiene una
  función que se pueda llamar suelta (el bróker, la cuenta, el tope del lote, la zona del break
  even), se llama esa, sin reescribirla. Lo que hoy vive dentro del intérprete del motor (la
  gestión del break even de la posición viva, el dimensionado) se reproduce en el guion, y solo
  vale si pasa el control de abajo.
- **Lote:** el que calcula la cuenta para el bot, con el tope de `lote_si_no_cabe` (`limitar`). Solo
  queda fuera la operación cuyo lote limitado baje del mínimo, y se cuenta.
- **Costes:** ticks de Dukascopy con su spread; comisión del perfil, 2,50 USD por lote y lado
  (ADR-0090 §3); swaps; deslizamiento en 0, pendiente de F17 (ADR-0092 §4, sin tocar `llenado.yaml`).
- **Cuenta:** una por mes (ADR-0092 §8), en la misma fase que la corrida (3). La fase solo cambia el
  objetivo y la etiqueta SUPERADA, que nada lee en el camino del motor (`engine/cuenta.py`). Se usa
  ese camino, no `evaluar_fase`, que descarta lo posterior a SUPERADA o SUSPENDIDA.
- **Ninguna otra regla abre o cierra:** ni los frenos de su propia operativa (RN-020, RN-036),
  porque sus entradas ya son las que él tomó, ni los que el bot lleva por la firma (RN-029, RN-030,
  RN-031, RN-032). Así f) mide su cuenta sin esas protecciones: si queda SUSPENDIDA, se dice.
- **Rechazos del bróker:** una orden que el bróker rechaza por otra causa que el lado (margen libre,
  órdenes simultáneas, posiciones del día, la ventana de cierre de ADR-0068) cuenta como «rechazada
  por el bróker», con su motivo, y no entra en el R.
- **Control obligatorio:** el guion, alimentado con las órdenes llenadas del propio bot en la
  corrida (3), en su orden y con una cuenta por mes, tiene que reproducir posición a posición lo que
  el motor da en «### Posiciones»: el lote, el motivo y el instante del cierre y el PnL neto, al
  céntimo. Para el objetivo se le da la caja 1 real de la orden («### Ordenes»), no la derivada. Un
  cierre «manual» en el instante de RN-002 o del fin de día entra en el control; cualquier otro
  «manual» (RN-030 lo da así) queda fuera, contado con su instante, y si queda fuera más de una
  posición de cada veinte, el control no vale. Si una sola posición de las que entran no se
  reproduce, no se calcula ningún R del trader.

Se calculan con las funciones de `cases/criterio_fidelidad.py`, sin reescribirlas, y con las
réplicas y la semilla del bloque `rentabilidad`: los criterios a) a f) de ADR-0092 §3 sobre todos
los días dev corridos; el percentil 95 con la misma función; y el deslizamiento que lleva la
esperanza a +0,10 R (`punto_de_equilibrio`, ADR-0092 §4), sin decidir nada con él. Como diagnóstico,
sin umbral: lo mismo solo sobre julio (el único mes con vídeo, provisional según
`criterio_fidelidad.yaml`), y cuántas operaciones no tenían stop, no fueron colocables, no se
llenaron, las rechazó el bróker o quedaron fuera por el lote mínimo. Aplicar a) a f) al trader es una
medida nueva, no la puerta (§4 a).

**M2 · Las parejas.** Las parejas T0 (el criterio de ADR-0043) de la corrida (3) con una cuenta por
mes, sobre toda la construcción, no solo julio, y siempre de esa corrida aunque el pivote se lea
sobre la diaria por la contingencia de ADR-0093 §6. Para cada pareja con las dos posiciones
cerradas y la del trader llenada en M1: el R neto del bot, de la corrida (PnL neto entre riesgo,
con `r_neto`, no la columna redondeada), y el R neto del trader en la misma operación, de M1. La
pareja se encuentra por (día, instante del llenado, entrada) de la fila T0 de `patrones.py --filas`. Se dan N, la media del bot, la media del trader en las mismas operaciones
y la diferencia emparejada media (bot − trader). Para el bot y para la diferencia, los percentiles
5 y 95 con `remuestreo_por_dias`, sobre todos los días dev corridos (como ADR-0092 §3 c); la
diferencia pasa por la misma función como posiciones con PnL igual a la diferencia y riesgo 1). Las
parejas sin pata del trader se cuentan aparte.

El R del trader sale del simulador, no de la columna de resultado de su libro: así las dos patas
llevan los mismos costes y la misma gestión, y el libro no se abre. Esta medida sustituye a las dos
fases de R5.7.

> **RECUADRO de ADR-0100 (2026-11-24, `trabajo/diagnostico-premisa`; el cuerpo no se toca).** ADR-0100 §5 lee la salida del libro del trader (avgClosePrice y dateEnd) de las filas de los días dev, como la serie anotada de VIABILIDAD-TRADER.md, para un diagnóstico: su registro frente a la réplica, mes por mes. No relee la meta, que sigue midiéndose como dice este §1 y sigue en la salida C.

### 2. Cómo se lee cada medida

Las cifras propias de este ADR viven en `docs/plan/META-TECHO-PAREJAS.yaml` (§7).

**El techo:**

- **gana**: se cumplen a) a f) de ADR-0092 §3 con el deslizamiento en 0 (N ≥ 100; esperanza ≥
  +0,10 R; percentil 5 > 0; pérdida diaria máxima < 3 %; equity mínima ≥ 94 %; ninguna cuenta
  SUSPENDIDA). Se escribe siempre «gana en construcción, con el deslizamiento pendiente de F17»;
- **no gana**: incumple d), e) o f); o la esperanza es < 0; o el percentil 95 es < +0,10 R (ni la
  réplica favorable llega a la esperanza mínima);
- **no concluyente**: el resto, incluido N < 100 con esperanza ≥ 0.

Se lee en ese orden: con N < 100 y esperanza < 0, el techo no gana. No se usa el veredicto de
`veredicto_rentabilidad`, que da «insuficiente» antes de mirar nada más.

**Las parejas** (N = parejas con las dos patas):

- con N < 19, **no concluyente**, sin mirar más. El 19 no es nuevo: es el mínimo de parejas que el
  pivote ya pide solo a julio (`PIVOTES-SESION-7.yaml`); sobre toda la construcción es más fácil de
  cumplir;
- **ganan**: media del bot ≥ +0,10 R y su percentil 5 > 0;
- **pierden**: media del bot < 0 y percentil 95 de la diferencia emparejada < 0 (el bot pierde y, en
  las mismas operaciones, lo hace peor que el trader de forma sistemática);
- **ni una cosa ni otra**: el resto, incluido que pierdan tanto como el trader en esas mismas
  operaciones.

### 3. Qué se hace con cada resultado

Como el pivote de ADR-0093 §6, esto decide el método y el objetivo, nunca un parámetro de la spec.
Las ramas de spec siguen citando al trader (`ev-`, `fb-`), y ningún arreglo de motor se justifica
con el R. Así queda acotado ADR-0092 §6 (recuadro).

- **A · El techo gana y las parejas ganan.** El objetivo pasa a un bot que solo opera los setups
  que reproduce (RUMBO §4), con la rentabilidad de ADR-0092 §3 sobre 2025 como puerta, sin cambiar
  una cifra. Lo concreta un ADR de Aleks, antes de ninguna corrida nueva, que elige el subconjunto
  por §4 c) y declara lo visto. Ese ADR tiene que resolver primero la condición previa de R5.6: la
  línea «habilita medir» de ADR-0070 (repetida en ADR-0092 §5 y en `PREREGISTRO.md`) pide 0,70 de
  cobertura en toda la construcción, y un bot de subconjunto no la alcanza nunca. Este ADR no fija
  qué la sustituye. Sí prohíbe sustituirla por un umbral de fidelidad sobre el propio subconjunto en
  esta construcción, porque se cumpliría por cómo se elige y es la alternativa 2 que ADR-0070
  descartó. La sesión que pida el pivote se graba igual y sirve al subconjunto.
- **B · El techo gana y las parejas pierden.** Antes de grabar más sesiones de fidelidad, una rama
  de diagnóstico, sin tocar decisiones, que descompone la diferencia emparejada por pieza: entrada,
  stop, instante del llenado, lote y tope, break even, cierre forzoso, spread y comisión. Un arreglo
  posterior se justifica con la diferencia de una pieza o con un hecho de la plataforma, nunca con
  el R. La sesión siguiente se prepara y se graba cuando esa rama cierre.
- **C · El techo no gana.** Antes de seguir, se revisan los costes y la premisa: F17 en una prueba
  gratuita nueva de FTMO (deslizamiento y spread reales); el sesgo del material sin vídeo (S-14) y
  la otra serie de precios (A-16); y Aleks contrasta la premisa con el trader, con sus resultados
  reales, sin enseñarle ninguna cifra de esta medida. La sesión siguiente se prepara y no se graba
  hasta que un ADR de Aleks decida, con lo que salga, si se sigue y cómo.
- **D · No concluyente** (el techo no concluyente; o el techo gana y las parejas no concluyen o no
  son ni una cosa ni otra). No cambia el objetivo: siguen R4.6 y el pivote de ADR-0093 tal como
  están. La medida de las parejas se repite, con estos mismos números, en la corrida que siga a
  cada activación. El techo solo cambia con material de construcción nuevo (diciembre de 2025 si el
  consultor lo declara construcción, NA:I; un backtest nuevo con vídeo de un mes no visto) o con
  F17, y se relee cuando llegue cualquiera de los dos. Si tras dos relecturas más sigue en D, Aleks
  decide con un ADR, sin repetir esta medida.

**Con el pivote de ADR-0093 §6.** El pivote no se toca y se lee en la misma corrida, con sus
números. Cuando los dos se cruzan:

- C manda sobre cualquier salida del pivote: no tiene sentido seguir afinando ni pivotar al
  subconjunto si el trader no gana con nuestros costes;
- B retrasa la sesión que pida el pivote hasta que cierre su rama;
- A con «se pivota» lleva al mismo ADR del subconjunto. A con «una sesión más» o con «se sigue»
  cambia el objetivo por ese ADR, y la sesión se graba igual;
- con D, manda el pivote.

A abre una segunda vía al subconjunto, escrita sabiendo que el pivote dará casi seguro «una sesión
más» (§5). Es la decisión de Aleks del 2026-11-22: el pivote mide si las sesiones acercan al bot al
trader; esta medida, si merece la pena acercarlo.

> **RECUADRO de ADR-0099 (2026-11-23, `trabajo/puente-techo`; el cuerpo no se toca).** A lo que la salida C manda revisar (F17, S-14, A-16 y el contraste con el trader), ADR-0099 añade una medida que C no pedía: el puente del techo pieza a pieza, pre-registrado en `docs/plan/PUENTE-TECHO.yaml`. No cambia el modelo de §1 ni la salida, que sigue siendo C; releer la meta con otro modelo sigue pidiendo un ADR que declare lo visto (§5). El ADR de Aleks que C pide es el que ADR-0099 §7 acota.

### 4. Tres ajustes

a) **El techo positivo es necesario, no suficiente.** Las operaciones son de un backtest manual en
FX Replay; en los libros sin vídeo el trader se saltaba las sesiones que acababan en break even
(S-14: `ev-v15-011912-0ae32588`, `ev-v16-003421-b824b770`); su serie de precios no es la nuestra
(A-16); y el deslizamiento no tiene modelo hasta F17. Ningún resultado de esta medida da «pasa»
para operar en vivo ni sustituye a la medida de ADR-0092 §3 sobre 2025.

b) **La salida «no concluyente» queda escrita ahora** (D), con lo que se hace y cuándo deja de
repetirse.

c) **El subconjunto se elige por fidelidad, nunca por resultado.** En la corrida (3) no se calcula
ni se imprime ningún R por clase de setup, sesión o dirección, aparte de lo que lista §1 y de las
líneas por cuenta que el arnés ya imprime. Si se llega a A, el ADR del subconjunto lo elige con
cifras de fidelidad (la cascada por criterios de ADR-0092 §2, la precisión por clase) y declara lo
visto; ninguna clase entra o sale por su R.

### 5. Lo visto, declarado (ADR-0070 punto 4, al estilo de ADR-0092 §12)

Antes de fijar las bandas de §2 el consultor ha visto:

- **Julio:** 14 parejas y 39 operaciones de más en la línea base (`PIVOTES-SESION-7.yaml`); 11 y 19
  tras activar la 7a, y 10 y 20 tras la 7b (`ACTIVAR-SESION-08.md`, `pivote-julio-base.txt` y
  `pivote-julio-f2.txt`). Con 10 < 19 y 20 ≤ 33, la lectura del pivote en (3) dará casi seguro «una
  sesión más». Si el trader contesta A-43 antes de (3) y la rama la activa, estas cifras quedan
  viejas; las bandas no dependen de ellas.
- **Construcción entera, antes de la 7a:** esperanza del bot −0,533 R en 247 operaciones, percentil 5
  −0,715 sobre 76 días, y −0,606 sin las 62 de break even de los libros sin vídeo
  (`RECORRIDA-CONSTRUCCION-2.md` §1.3; diagnóstico, ADR-0092 §6); 31 parejas sobre 198 operaciones
  del trader y 223 del bot, 15,7 % y 13,9 % (§1.1). Ningún informe posterior rehace la construcción
  entera.
- **El R del trader, ya medido** con el motor de septiembre sobre abril y agosto:
  `VIABILIDAD-TRADER.md` §2 y §3; `VIABILIDAD-COMISION.md`, con 5 USD de ida y vuelta, la serie
  anotada +0,56 R [+0,05; +1,08] en 77 operaciones y la simulada con stop en el 0,8 y objetivo a 3 D
  (V2) +0,47 R [−0,13; +1,08] en 67, con intervalos por operación y no por días; y
  `F35-ORDEN-STOP-PIVOTE.md` §5.3 (el bot frente al trader en los mismos días, con R bruto).
- **El R de las parejas del bot no se ha publicado nunca.** Se podría derivar de los anexos de
  `RECORRIDA-CONSTRUCCION-2` (la tabla de posiciones y los patrones), que el consultor leyó, pero
  nadie lo ha calculado.

El consultor no ha visto las salidas de julio de ACTIVAR-SESION-07 y -08 más allá de sus recuentos
(viven en `data/`, en la laptop de Aleks). Si el modelo de §1 tuviera que cambiar después de ver la
corrida (3), solo lo cambiaría un ADR nuevo que declare lo visto.

Las bandas copian los umbrales de ADR-0092 §3 y el mínimo de ADR-0093 §6. Las dos piezas nuevas,
el percentil 95 con su umbral de +0,10 R y el uso del 19 sobre toda la construcción, se eligieron
con lo de arriba a la vista; lo declaro. La salida D existe porque, con lo visto en abril y agosto,
el techo puede quedar entre las dos bandas.

### 6. Marzo de 2027 no cabe con ninguna vía

F34 pide tres meses en umbral (`MASTER_PLAN.md`, fila F34) y no empieza hasta que el bot decide en
una demo. Antes hacen falta la medida de rentabilidad (R5.6: los datos de 2025, el calendario de
cierres hacia atrás, F17 y su propia rama con su ADR y su comando, que no existe) y la plataforma
que decide: el porte a MQL5 (F29-F30, unas 8 a 12 semanas), o Python decidiendo en vivo si un ADR
nuevo reabre ADR-0082 §4. `AUDITORIA-2026-11-21.md` sitúa F35 a finales de mayo de 2027 como pronto
con porte, aun quitando hoy la puerta de fidelidad. Sin porte y con la salida A en (3), F34 no
acabaría antes de abril. Se dice ahora para que ninguna salida de este ADR se lea como una forma de
llegar a marzo. La meta de agosto de 2027 depende de lo que salga aquí y de dos decisiones que se
toman con los ingenieros (hacia el 2026-12-03, fecha dada por Aleks): la arquitectura en vivo y los
tres meses fijos de F34.

### 7. Dónde viven las cifras

En `docs/plan/META-TECHO-PAREJAS.yaml`, que fija `tests/unit/test_meta_techo_parejas.py` por su
sha256, con un test que rompe a propósito con una banda cambiada (como `test_pivotes_sesion_7.py`).
Las de ADR-0092 §3 y ADR-0093 §6 no se copian como literales nuevos: el yaml remite a
`criterio_fidelidad.yaml` y a `PIVOTES-SESION-7.yaml`, y añade solo lo propio (el percentil 95 y su
umbral, las cuatro salidas, su precedencia con el pivote y las dos relecturas de D). Ninguna cifra
en `src/` (ADR-0002).

## Problema que resuelve

El objetivo de fidelidad (las mismas decisiones que el trader en toda la construcción, 0,70 y 0,60)
está hoy en 15,7 % y 13,9 % y no tiene trayectoria medida que lo acerque; la meta de marzo no cabe
con las reglas actuales (AUDITORIA-2026-11-21.md). Seguir sesión tras sesión sin saber si el
trader gana con nuestros costes, ni si el bot gana cuando sí lo replica, es construir sin saber si
el objetivo es alcanzable o rentable. Las dos preguntas se pueden contestar ya, sobre construcción
y sin gastar holdout, y su respuesta solo vale si qué se hace con ella queda escrito antes de verla.

## Alternativas consideradas

1. Seguir con R4.6 y el pivote de ADR-0093 sin medir nada más (la opción 1 que se le planteó a
   Aleks).
2. Lo elegido: medir el techo y las parejas en (3), con las salidas escritas antes.
3. Medir sin salidas escritas, como diagnóstico de R5.7, y decidir después de verlo.
4. Medir el R del trader con la columna de resultado de su libro (su salida real), como planeaba
   R5.7.
5. Elegir el subconjunto por su rentabilidad en construcción.
6. Fijar ya, en la salida A, la condición previa de R5.6 para el bot del subconjunto.

## Por que elegimos esta opcion

Contesta con datos ya disponibles, sin holdout, si el objetivo es alcanzable y rentable antes de
gastar más sesiones; las salidas, escritas antes, impiden leer el resultado a conveniencia; y no
mueve ningún umbral pre-registrado.

## Por que descartamos las demas

- **La 1** gasta sesiones sin saber si el trader gana con nuestros costes.
- **La 3** no sería un pre-registro: la decisión se tomaría ya vista la cifra (ADR-0070 punto 4).
- **La 4** compara dos patas con costes y gestión distintos (su salida real frente a la regla del
  bot), y abre una columna del libro que no hace falta.
- **La 5** elige por resultado sobre el mismo material en que se mide: es optimizar contra
  resultados (ADR-0092 §6).
- **La 6**: cualquier umbral de fidelidad sobre el subconjunto en esta construcción se cumpliría
  por cómo se elige, y es la alternativa 2 que descartó ADR-0070. Lo decide el ADR de A, con lo que
  haya entonces, sin esa vía.

## Impacto

- `docs/plan/META-TECHO-PAREJAS.yaml` y `tests/unit/test_meta_techo_parejas.py`, nuevos, en el
  commit del pre-registro de la rama de (3), con este ADR, su fila del índice y el recuadro en ADR-0092 §6.
- La rama de (3) construye el guion de M1 y M2 (anexos, sin tocar `src/` ni `knowledge/spec/`), con
  el control de §1, y su informe da la salida (A a D) y la del pivote.
- Hoja de ruta, en la orden de cierre de esa rama: R5.7 se sustituye por esta medida y deja de ser
  solo diagnóstico; R4.3 y R4.6 citan este ADR (el «Hecho cuando» de R4.6 añade «o la lectura de
  ADR-0098 cambia el objetivo»); la salida que toque, en la Next Action F.

## Fecha / fase

2026-11-22; post-F14, rama de la corrida (3) (R4.3, NA:F).

## Estado

ACTIVE (decisión de Aleks del 2026-11-22, opción 2; números del consultor aprobados el 2026-11-22;
pre-registra dos medidas y cuatro salidas; acota ADR-0092 §6 con recuadro y sustituye R5.7; no
cambia ninguna cifra pre-registrada)
