---
status: ACTIVE
date: 2026-10-17
phase: post-F14 (rama `trabajo/margen-lote`, R3.3 de la hoja de ruta; heredado 37, A-18)
---

# 0081 · El lote que no cabe en el margen o en el volumen se limita, y el bróker simulado rechaza por margen libre al colocar y al llenar (enmienda ADR-0052 §4, ADR-0053 §1 y ADR-0026, Impacto)

> Decisiones del consultor del 2026-10-17 (encargo de `trabajo/margen-lote`, D1-D7, fechado el
> 2026-10-18, y su respuesta a la PARADA de la fase 0, `docs/validation/MARGEN-LOTE.md` §1.k). Las
> tomó ANTES de ver las medidas de la rama, y las medidas no las cambian. Lo que el trader hace en
> su cuenta cuando el lote de su riesgo no cabe NO está en el corpus (§6): la decisión D1 es
> PROVISIONAL hasta la sesión 5 (A-57). **Enmienda ADR-0052 §4, ADR-0053 §1 (tabla, `redondear_lote`)
> y ADR-0026 (Impacto)**, con recuadro en cada uno y fila del índice.
> *(NOTA del 2026-10-26, `trabajo/activar-sesion-05`: D1 ya no es provisional; el trader la confirmó
> en la sesión 5, recuadro de §1.)*

## Decision

### 1. D1 · Cuando el lote del riesgo no cabe, el bot LIMITA el lote y opera

El lote que dimensiona RN-011 (`riesgo_por_operacion`, 0,5 % del saldo, sobre la distancia hasta
el stop; ADR-0020) puede no caber en la cuenta por dos límites: el **volumen máximo por orden** de
la firma (`firma_volumen_max_lotes`, 50 lotes en FTMO, ADR-0071 §2: corta todo stop de menos de
1 pip) y el **margen libre** a 1:30 (`firma_apalancamiento`; con todo el saldo como margen caben
27,27 lotes a 1,10 y 25,00 a 1,20, y el 0,5 % deja de cumplirse con un stop de menos de 1,83 y
2,00 pips: FTMO-P-D1.md §2). De las tres salidas que ADR-0071 §2 dejó abiertas -recortar el lote,
partir la operación en varias órdenes, no operar-, **partir queda descartada** por FTMO-P-D1.md §2
(MT5 suma el margen de las posiciones del mismo lado: cinco órdenes de 6 lotes piden el mismo
margen que una de 30) y **el bot limita el lote y opera**.

Por qué limitar y no abstenerse: el objetivo de fidelidad son las MISMAS DECISIONES que el trader
-misma operación, mismo lado, misma vela y mismo resultado en R-, y limitar el lote conserva la
decisión y el resultado en R; solo cambia el riesgo en dinero. No operar quitaría justo las
operaciones de stop corto, y VIABILIDAD-COMISION.md enseña que sacarlas del juego mueve la
esperanza: elegir por eso sería ajustar contra resultados. La decisión es **PROVISIONAL hasta que
el trader diga qué hace él** (A-57, §6): la pregunta ya estaba en la lista «Para el cuestionario de
la sesión 5» de CORRIDA-CONSTRUCCION.md §4.5 («El lote que no cabe: ¿qué hace el trader en su
cuenta real cuando el stop es tan pequeño que el lote del 0,5 % pasa del máximo de la firma (50
lotes)?») y se amplía al margen.

> **CONFIRMADO POR EL TRADER el 2026-10-23 (sesión 5, S-5; recuadro del 2026-10-26,
> `trabajo/activar-sesion-05`, que no reescribe el cuerpo).** A la pregunta de A-57 respondió la
> opción (a): «bajo el lote y a lo que cabe y entro igual» (`ev-v15-001758-c27d9c4c`;
> `fb-2026-10-23-sesion-05-146c4789`, RESOLVE_UNKNOWN sobre A-57, que queda RESUELTA). D1 deja de
> ser PROVISIONAL y `lote_si_no_cabe` pasa a CONFIRMED en `limitar` con fuente esta decisión (es
> de `ejecucion`: el valor lo decide el ADR y el trader lo confirma). Reservas, escritas en el
> registro: lo dijo «por ahora» y con «creo», y después de que Aleks, preguntado por él, le
> planteara la disyuntiva entre una gestión de riesgo fija y una variable
> (`SESION-05-EXTRACCION.md` §3.2, S-5), y, según esa misma sección y fuera de los ítems, no ha
> vivido el caso en su cuenta.

### 2. D2 · El lote final es el menor de tres, redondeado hacia abajo al paso

    lote = min( lote del riesgo (RN-011),
                firma_volumen_max_lotes,
                lote_que_cabe_en( margen_libre × lote_margen_libre_fraccion ) )
    y después hacia abajo al paso (instrumento_lote_paso, RN-027)

donde `lote_que_cabe_en(M) = M × firma_apalancamiento / (instrumento_contrato × precio)` con el
precio de conversión del margen (§4). `lote_margen_libre_fraccion` vale **0,95**: el 5 % de colchón
cubre el deslizamiento del llenado y la diferencia entre el precio con que se convierte el margen al
colocar (el ask o el bid del cierre de M1) y al llenar (el precio del tick que llena). El bot y el
bróker usan EL MISMO margen libre (`Broker.margen_libre()`, al tick, §4) y la misma función, así que
entre los dos no hay diferencia de equidad que cubrir (la respuesta del consultor lo preveía por si
el bot leía la equidad de la cuenta por marcas de minuto; no es el caso: hallazgo a1 del revisor).
Es una decisión nuestra, no del trader (fuente de los dos parámetros: este ADR).

**El lote por debajo del mínimo (respuesta a la PARADA, punto 0).** RN-027 decía en su prosa que
por debajo de `instrumento_lote_minimo` «no se opera», y el código y ADR-0053 §1 (tabla,
`redondear_lote`: «no por debajo del mínimo») subían el lote AL mínimo. La cita de RN-027
(`fb-2026-09-09-sesion-01-17ed6193`, «el 0.5% de riesgo de la cuenta se calcula sobre el nivel 0.8»)
no sostiene ni lo uno ni lo otro: habla de dónde sale el lote, y ADR-0016 (su `decision`) solo
decide la dirección del redondeo. **Desde este ADR, por decisión del consultor, por debajo del
mínimo NO SE OPERA**: subir al mínimo arriesga MÁS que `riesgo_por_operacion`, lo contrario de
limitar. En la práctica no muerde: con 0,5 % de 100.000 el lote baja de 0,01 solo con un stop de
5.000 pips, o con un saldo ínfimo; con el margen, solo con el margen libre casi a cero. ADR-0053 §1
gana su recuadro. El camino «no se coloca» es UNO SOLO, el de §3: anota el motivo y no lanza error.

### 3. D4 · Dos parámetros nuevos en el registro, de `ejecucion`, y dónde se aplica el límite

En `knowledge/spec/parametros.yaml`, con el patrón de `cierre_pendientes` (ADR-0068: un parámetro
de ejecución que lee el simulador, no una regla de la spec):

- **`lote_si_no_cabe`**: `enum`, opciones `limitar` | `no_operar`, valor **`limitar`**,
  `DEFAULT_AMBIGUOUS` bajo **A-57**, `consumido_por: [ADR-0081]` *(NOTA del 2026-10-26,
  `trabajo/activar-sesion-05`: CONFIRMED en `limitar` con fuente esta decisión, A-57 RESUELTA por el
  trader en la sesión 5; recuadro de §1)*. Con `no_operar`, una orden cuyo
  lote del riesgo no cabe NO SE ENVÍA y queda anotada con su motivo en la traza del día (como
  `bloqueadas`); el camino es el mismo que el del lote por debajo del mínimo (§2).
- **`lote_margen_libre_fraccion`**: `decimal`, valor **`0.95`**, entre 0 y 1, `CONFIRMED`,
  `consumido_por: [ADR-0081]`, fuente `{tipo: decision, id: ADR-0081}`.

**El límite va en la preparación de la orden** (`colocar_orden_limite`, `engine/primitivas_broker.py`;
respuesta a la PARADA, punto 1), no en una regla nueva de la spec: el cableado lee los dos
parámetros del registro y el tope de volumen y el apalancamiento de `ReglasBroker`, que ya los
trae del perfil (ADR-0050 §3: «el perfil lo lee solo el simulador»). Así la spec NO lee
`firma_volumen_max_lotes` -no hace falta duplicarlo en `parametros.yaml`- y no nace una regla con
una cita del trader que no habla de esto. RN-011 y RN-027 no cambian de forma; sus notas dicen que
el lote que se coloca puede quedar por debajo del de RN-011 por este ADR. No se confunda con
`firma_margen_seguridad` (ADR-0031), que es el colchón de los frenos de pérdida de la firma.

### 4. D3 · El bróker simulado rechaza por margen al colocar y al llenar, con una sola función

El bróker (`engine/broker.py`) hace de FTMO (ADR-0052): **rechaza por margen aunque el bot calcule
bien**. El margen de una orden es la fórmula de forex de la documentación de MetaTrader 5
(«Margin Calculation for Retail Forex, Futures»,
https://www.metatrader5.com/en/terminal/help/trading_advanced/margin_forex; FTMO-P-D1.md §2):

    margen_requerido = lotes × instrumento_contrato × precio / firma_apalancamiento   (en USD)

con el precio que convierte el margen a la moneda de la cuenta: **el ask en una compra y el bid en
una venta** («The Ask price is used for buy deals, and the Bid price is used for sell deals»). Es
**UNA sola función** (`broker.margen_requerido`), y la usan el límite del bot (§3), el rechazo del
bróker y la salida del arnés, para que no discrepen y el bot no coloque una orden que el bróker
rechace por un céntimo (respuesta a la PARADA, punto 1).

- **El margen libre** = equidad − margen usado, con la equidad del bróker = saldo realizado de la
  cuenta (que el cableado le pasa como un `Callable`, `lambda: cuenta.saldo`) + su flotante al
  tick, y el margen usado = la suma del margen de cada posición abierta (a su precio de entrada) y
  de **cada pendiente STOP** (a su precio): la documentación de MT5 dice que «For all other order
  types (Stop and Stop Limit), the margin is summed up (charged for each order)» y que «the total
  margin is equal to the sum of the current position's and placed order's margins». Una pendiente
  stop RESERVA margen mientras vive; al cancelarla lo libera, y en la reubicación de ADR-0074 la
  cancelación de la orden vieja va ANTES del cálculo del lote de la nueva, en el mismo cierre.
- **Se comprueba en los dos instantes**: al COLOCAR, con el ask o el bid del mercado en ese instante
  (es lo que sostiene la frase de MT5: una stop colocada tiene su margen cargado) y al LLENAR, con el
  precio del llenado (el llenado de una stop es una operación de mercado, «Once triggered, stop
  orders behave similar to market orders», y el margen libre puede haber cambiado desde que se
  colocó). La página no enuncia el instante exacto de la comprobación: el segundo es el supuesto
  conservador que D3 pedía, y **cuándo lo comprueba MT5 de verdad se mide en la demo (ejecución 3,
  entrada A de la Next Action)**. También en `abrir_conocida` (las operaciones conocidas del trader
  que se repiten por el bróker), que levanta error porque no hay orden que rechazar.
- **El motivo es `margen_libre`**, un `Rechazo` como los demás. El rechazo al llenar es un camino
  NUEVO: ADR-0052 §4 solo preveía rechazos al colocar (y ADR-0057, al modificar); la orden pasa a
  `rechazada`, el evento llega al intérprete como los demás y la salida lo cuenta en «### Rechazos
  por motivo» con `peticion = llenar`. **No es una `Peticion` al servidor** (R13, ADR-0067): la
  orden ya estaba en el servidor cuando se rechaza.
- **Negar por defecto** (respuesta a la PARADA, punto 2): si `ReglasBroker` trae apalancamiento (el
  perfil real), el saldo es OBLIGATORIO y construir el bróker sin él es un error; solo sin
  apalancamiento (un perfil sintético que no lo declara) no se comprueba el margen. Nada de «margen:
  sin comprobar» en silencio con el perfil real. Un test exige que el cableado del arnés pase
  siempre el saldo.

### 5. D6 · Lo que enmienda, y lo que corrige en el perfil y en el registro

- **ADR-0052 §4**: los rechazos del perfil ganan el margen libre, y el instante del llenado (recuadro).
- **ADR-0053 §1**, tabla, `redondear_lote`: «no por debajo del mínimo» → por debajo del mínimo no se
  opera (recuadro, §2 de aquí).
- **ADR-0026, Impacto**: «F21 lo comprueba con la distribución real de cajas» era falso
  (FTMO-P-D1.md §2: nada lo comprobaba); lo comprueba el bróker simulado desde este ADR (recuadro).
- **El perfil** (`knowledge/cuentas/ftmo-2step-swing-100k.yaml`): `firma_apalancamiento` decía «Lo
  consume el broker simulado (margen)» sin que ningún código lo leyera; desde este ADR lo lee
  `reglas_broker_de` y su `consumido_por` dice `[ADR-0081]`. En `parametros.yaml`, la frase «F21 lo
  comprueba…» pasa a decir quién lo comprueba (el bróker simulado) y su `consumido_por`,
  `[ADR-0081, F33]`: el pre-vuelo de la demo lo vuelve a leer. Siguen citando R9.
- **G.3 de la hoja de ruta**: la descripción de `firma_tamano_posicion_ratio_aviso` pasa a decir lo
  que respondió FTMO (FTMO-REGLAS.md, respuesta 10, 2026-10-05): sin cifra, «sustancialmente mayor»
  depende del histórico del propio trader; sigue `UNKNOWN` y citando R17.
- ADR-0050 (el perfil como capa) y ADR-0056 §8 (rama 5, «lote por el bróker») no se contradicen:
  el lote sigue saliendo del cableado y el perfil sigue siendo lo que lee solo el simulador.

### 6. D5 · A-57, y lo que la búsqueda en el corpus (no) encontró

Nace **A-57** (`pregunta`, no bloqueante): qué hace el trader cuando el lote de su riesgo no cabe en
el margen o en el volumen máximo de la cuenta. Antes de redactarla se buscó en el corpus citable
(evidencia, feedback y transcripciones activas fuera de cuarentena, por la CLI que filtra;
MARGEN-LOTE.md §1.f): «apalancamiento», «lotes» y «lote» junto a «cabe», «máximo», «bróker»,
«cuenta», «fondeo» o «FTMO» dan 0 resultados; «margen» solo da el margen de beneficio o del stop;
«lotaje» da 20 ítems, todos de SOBRE QUÉ DISTANCIA se calcula (A-18, ADR-0020). **Ninguna frase
del trader habla del lote que no cabe.** A-57 cita como respaldo débil, dicho en la propia
pregunta, los dos ítems que hablan de su lote en una cuenta de fondeo: `ev-v4-002457-5a2e88c6`
(«he entrado sin lotaje … han sido 3 que como tal no he entrado con el porcentaje de la cuenta») y
`ev-v4-012900-8ef676ed` («es un lotaje fijo, muy bajo», por falta de calculadora). La pregunta se
formula con la cuenta y sus límites (50 lotes, 1:30), sin ninguna cifra ni argumento de
VIABILIDAD-COMISION.md, que no se enseña al trader. `lote_si_no_cabe` es `DEFAULT_AMBIGUOUS` bajo
ella; la respuesta del trader entra como `RESOLVE_UNKNOWN` sobre A-57 (ADR-0022).

### 7. D7 · La cuenta sigue siendo FTMO 2-Step Swing

ADR-0026 no cambia. **Aleks decidió el 2026-10-13 quedarse en Swing** (no estaba escrito en el
repositorio; entra aquí con esa fecha). La medida de cuántas operaciones del trader caen a ±2
minutos de una noticia restringida de FTMO (la lista de la cuenta Standard, FTMO FAQ «Can I trade
news?») es información para más adelante, no una propuesta de cambiar de tipo de cuenta: el informe
da la cifra, si hay calendario, y no recomienda nada.

### 8. Lo que mide la rama, y dónde

Las cifras no cambian estas decisiones y viven en `docs/validation/MARGEN-LOTE.md`: la medida 1
(qué parte de las operaciones del trader en construcción tiene un stop de menos de 1,00, 1,83 y
2,00 pips, bajo las dos lecturas de A-56), la medida 2 (cuántas órdenes de la corrida diaria rechaza
el volumen y cuántas rechazaría el margen, antes del cambio) y la re-corrida con el límite (rechazos
por motivo antes y después, órdenes limitadas y por qué límite, riesgo efectivo, T0 y P1-P7). Es una
corrida con `--diagnostico-*`: no cuenta ni habilita mayo (ADR-0070 §3).

## Problema que resuelve

Con `riesgo_por_operacion` sobre 100.000 y los stops del trader -de pips, no de decenas de pips
(VIABILIDAD-COMISION.md: 1,5 de mediana en abril y agosto)-, el lote de RN-011 pasa con frecuencia
de lo que la cuenta admite: la corrida diaria de R3.1 sobre `main` tenía 96 rechazos por
`volumen_max_lotes` de 107 (MARGEN-LOTE.md §1.e), y el margen a 1:30 corta ANTES que el volumen
(FTMO-P-D1.md §2) sin que el simulador lo comprobara: `firma_apalancamiento` no lo leía ningún
código del bot. Un rechazo por volumen deja la sesión sin operación (P4 de la clasificación de
R3.1, 17 sesiones), y una cuenta real habría rechazado además por margen. Hacía falta decidir qué
hace el bot (heredado 37, A-18) y que el bróker simulado rechace lo que FTMO rechazaría.

## Alternativas consideradas

1. **Limitar el lote y operar** (esta).
2. **No operar** cuando el lote no cabe.
3. **Partir la operación en varias órdenes** de hasta 50 lotes.
4. Una **regla nueva de la spec** (RN-037, `gate`) con una acción `limitar_lote`, en vez del límite
   en la preparación de la orden.
5. Comprobar el margen **solo al llenar**, o solo al colocar.
6. El saldo del bróker **opcional en silencio**: sin él, no se comprueba el margen aunque el perfil
   declare apalancamiento.

## Por que elegimos esta opcion

Limitar conserva la decisión del trader y el resultado en R, que es lo que mide la fidelidad
(ADR-0043); solo cambia el riesgo en dinero, que se declara en la salida. El límite en la
preparación de la orden usa lo que el perfil ya da al simulador sin duplicarlo en la spec ni
inventar una cita (precedente: `cierre_pendientes`, ADR-0068). Una sola función de margen para el
bot, el bróker y la salida evita discrepancias por un céntimo. Comprobar en los dos instantes es lo
que la documentación de MT5 sostiene (el margen de una stop colocada se carga) más el supuesto
conservador para el llenado, hasta medirlo en la demo. Negar por defecto -saldo obligatorio cuando
hay apalancamiento- es la regla de la casa: la condición tiene nombre y lo demás se niega.

## Por que descartamos las demas

- **No operar** quita justo las operaciones de stop corto, y VIABILIDAD-COMISION.md enseña que eso
  mueve la esperanza: elegirlo sería ajustar contra resultados. Queda como opción
  (`lote_si_no_cabe = no_operar`) para cuando el trader diga qué hace él.
- **Partir** no cabe en MT5 con cuenta de cobertura: suma el margen del mismo lado (FTMO-P-D1.md §2).
- **La regla nueva** obligaba a duplicar `firma_volumen_max_lotes` en `parametros.yaml`, a una
  `cita` + `literal` del trader que no dice nada del límite (relleno, la deuda de RN-029..032) y a
  `decision` (comprobar_decisiones), por una visibilidad que ADR-0068 ya resolvió de otra manera.
- **Un solo instante** deja fuera o la reserva al colocar (que MT5 sí hace) o el margen libre que
  cambió entre colocar y llenar.
- **El saldo opcional en silencio** haría que un bróker construido con el perfil real pudiera correr
  sin comprobar el margen sin que nadie lo viera.

## Impacto

- Código: `engine/broker.py` (`ReglasBroker.apalancamiento`, `margen_requerido`,
  `precio_de_conversion`, `margen_usado`, `margen_libre`, el rechazo `margen_libre` al colocar, al
  llenar y en `abrir_conocida`, el saldo como `Callable`), `engine/simulacion.py`
  (`reglas_broker_de` lee `firma_apalancamiento`), `engine/primitivas_broker.py` (el límite en
  `colocar_orden_limite` y el camino «no se coloca»), `engine/cableado.py` (el saldo al bróker; las
  columnas de margen de «### Ordenes» y la fila `llenar` de «### Rechazos por motivo»).
- Spec: `lote_si_no_cabe` y `lote_margen_libre_fraccion`; A-57; las notas de RN-011 y RN-027;
  `spec_version` 18.0.0 → 18.1.0 (menor: parámetros nuevos, ninguna regla cambia de sentido) y
  18.1.1 tras el revisor de la rama (parche: la redacción de dos descripciones).
- Perfil y registro: las descripciones y `consumido_por` de `firma_apalancamiento`, y G.3.
- Tests: los del margen (justo por encima y por debajo, con una posición viva, ask/bid, pendiente
  que reserva, reubicación, `no_operar`, el lote que cabe no cambia, el mismo resultado en R con el
  lote limitado) y los rehechos (`test_cuenta_7_de_agosto.py`, con `apalancamiento=None` explícito
  en la regresión del corte de la cuenta).
- Lo que NO cambia: la geometría, el sesgo, la ventana, `riesgo_por_operacion` (0,5 %), el script
  1.1 de la demo, los informes cerrados, las guardias y el Makefile.
- Queda para A (Next Action): la ejecución 2 de la demo comprueba la fórmula del margen con
  `MargenAlcanza`, y la 3 mide cuándo comprueba MT5 el margen de una pendiente stop.

## Fecha / fase

2026-10-17 · post-F14, rama `trabajo/margen-lote` (R3.3 de la hoja de ruta; E de la Next Action;
heredado 37; A-18).

## Estado

ACTIVE (D1 confirmada por el trader en la sesión 5, 2026-10-23: A-57 RESUELTA, activada el
2026-10-26, con sus reservas en el recuadro de §1; enmienda ADR-0052 §4, ADR-0053 §1 y ADR-0026,
Impacto)
