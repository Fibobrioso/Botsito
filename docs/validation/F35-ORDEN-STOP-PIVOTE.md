# F35 · La vida de la orden stop, en el último pivote de M1 y con la caja por operación

Rama `feature/F35-orden-stop-pivote`, 2026-09-30, desde `main` en `3375249`
(`stable/F36c-caja-77`). Es la D del Next Action: la rama 3 de ADR-0056, con la caja por operación
de su rama 4. **ADR-0064**, aceptado en su dirección por el consultor.

> **Aviso de nombre.** En `docs/plan/MASTER_PLAN.md`, F35 es `feature/F35-go-live-gate`. «F35» como
> «la vida de la orden stop» viene de la numeración de la noche del 30 de septiembre
> (`docs/nocturno/PLAN-01oct.md`) y choca con el plan. Por eso el parámetro nuevo no dice «F35» en
> `consumido_por`: dice ADR-0064.

## 1. Qué cambia

**Las decisiones del consultor (ADR-0064 §1–§3):**

- **El punto de nacimiento: `orden_stop_punto`**, DEFAULT_AMBIGUOUS bajo A-48.
  - `ultimo_pivote_m1` (el valor): el último pivote de M1 contrario a la entrada, que es la función
    de R5 de CAJA-77 (`ultimo_punto_de_ruptura`). Se actualiza con cada pivote nuevo.
  - `referencia_de_la_toma`: el pivote de `referencia_del_breaker` en la toma, fijo.
- **La caja: `caja_bloque`**, DEFAULT_AMBIGUOUS bajo A-48. Con el 0 en el punto, el 1 lo dan
  `r6` (el valor), `r4` o `r1` (`extremo_de_la_caja`). Cada reubicación recalcula la caja, el stop y
  el lote.
- **El stop**: `stop_fraccion_caja`, sin cambios. A-18 sigue abierta.

**La vida de la orden, desde ADR-0056 §7 (ADR-0064 §4):**
- Corre con `orden_limite_nace` = `al_aparecer_punto_de_breaker`: el valor nuevo, que sigue
  DEFAULT_AMBIGUOUS bajo A-29.
- **Nace tras la toma de su sesión**, como STOP en el punto.
- **Se reubica con cada punto nuevo**: RN-006 la cancela, y RN-011 y RN-015 la vuelven a colocar
  en el mismo cierre de M1.
- **Se llena al romper el punto**, que es el esquema 1.
- **Se cancela al cerrar la ventana.**
- **RN-008 no frena la colocación**, con el predicado `la_orden_nace_antes_del_esquema`. Es lo que
  ADR-0056 §7 dejaba PROVISIONAL para esta rama, y un test lo fija.

**DECISIONES** (ADR-0064 §4, la lectura más conservadora donde nadie decidió):
1. Un punto ya usado (con la orden enviada, aceptada o rechazada) no se reintenta.
2. Una sola vida de orden por sesión que llega a llenarse.
3. La orden pendiente de una sesión no se reubica con los puntos de la siguiente.
4. RN-005 se aplica a la zona del punto, y RN-009 sigue en pie.
5. La caja se fija la primera vez que se ve el punto.
6. La ventana de M1 es la del productor: 240 minutos antes de la toma.

**Ninguna de esas decisiones cambia lo que el bot opera de forma que hubiera que parar a
preguntar.** La 1 y la 2 son las más fuertes, y las dos restringen: menos órdenes, no más.

**Spec** (`spec_version` 14.4.1 → **15.0.0**, MAYOR porque RN-008 cambia de sentido con la orden en
el punto):
- la forma y las notas de RN-008, que ahora declara `decision: ADR-0064`;
- las notas de RN-006;
- las descripciones de `toca_colocar_orden_limite` y `se_completa_zona_de_control`;
- el predicado nuevo;
- `orden_limite_nace`, con su valor y su cita nuevos, y los parámetros `orden_stop_punto` y
  `caja_bloque`, con A-48 nombrándolos.

**Las citas: un ítem de evidencia nuevo.** Una guardia del repositorio
(`test_fichero_real_cada_valor_de_estrategia_cita_al_trader`) exige que un valor de estrategia
cite al trader y no a un ADR nuestro. Los tres valores citan evidencia de v7, y la elección entre
lecturas vive en ADR-0064, como cualquier DEFAULT_AMBIGUOUS:
- `orden_limite_nace` cita `ev-v7-001457-1fe7fdfe`: la Sell stop puesta en el punto antes de la
  ruptura;
- `orden_stop_punto` cita `ev-v7-002201-2b2f20aa`: el punto que se actualiza «conforme se
  desarrolla el precio»;
- `caja_bloque` cita un **ítem NUEVO, `ev-v7-001550-82e5cffc`**, de v7 0:15:50: «trazamos el GAN
  desde el posible punto de breaker hasta el punto más alto», literal de la transcripción cruda. Es
  la frase que `BLOQUE-DE-LA-CAJA.md` §1.4 cita para R6. Lo creó esta sesión con `botsito evidence
  new` y lleva **«PENDIENTE de revisión del consultor»** en `revisado_por`.

**Tests**:
- `tests/unit/test_orden_stop_pivote.py`, nueve casos:
  - el punto y la caja en una venta y en una compra;
  - que el punto y la caja son las funciones de R5, R6, R4 y R1 de `bloque_de_la_caja.py`, sobre 60
    series al azar por lado;
  - que el productor liga una zona por punto y no repite un punto usado;
  - que con la referencia de la toma el punto no se mueve;
  - que RN-008 no frena con la orden en el punto y sí con la orden en el esquema;
  - que RN-006 sigue sin escribirse con la orden en el esquema;
  - y la cadena **colocada → cancelada → recolocada en el mismo cierre → llenada → objetivo** por el
    cableado real y la spec real, con las peticiones «colocar, cancelar, colocar».
- `test_preparar_a21.py` y `test_sesiones_independientes.py` prueban la zona del esquema y ahora
  fijan `al_darse_el_esquema` en su registro.

## 2. Lo medido (en DIAGNÓSTICO)

> **No es fidelidad.** El criterio de la caja y del punto se eligió mirando construcción
> (`CAJA-77.md` §3), y esto mide sobre construcción. Ninguna cifra cuenta como medida.

- **Cómo**: `motor arnes --simular` y `scripts/embudo_77.py` sobre abril y agosto de 2026 (42 días
  `dev`, 77 operaciones del trader), con A-35 `cierre_vela_contraria`, A-44 `sin_tope`, A-21
  `solo_una_zona_de_control` y A-27 a 0 puntos.
- **Dónde**: cada configuración en un clon desechable (`git worktree add` en la carpeta de trabajo,
  con `parametros.yaml` editado en el clon y los datos del repositorio). Nada se escribió en el
  repositorio.
- **«Antes»** es `main` (`3375249`).
- **Control de la línea base**: la rama con `orden_limite_nace` = `al_darse_el_esquema` da el
  informe del arnés y el embudo **idénticos byte a byte a `main`**.

| | antes (`main`) | después: `ultimo_pivote_m1` + `r6` | `referencia_de_la_toma` + `r6` | `ultimo_pivote_m1` + `r4` |
|---|---|---|---|---|
| **cobertura** (operaciones del trader que el bot iguala) | 0 de 77 | **2 de 77** | 0 de 77 | **2 de 77** |
| **operaciones puntuables del bot** | 2 | **10** | 7 | 10 |
| operaciones del bot en el embudo | 2 | 15 | 7 | 15 |
| eventos del bróker | 4 | 30 | 14 | 30 |
| rechazos del bróker | 9 | 3 | 2 | 3 |
| **peticiones al servidor**, total en 42 días | 11 | 35 | 13 | 36 |
| · colocar / modificar / cancelar / cerrar | 11 / 0 / 0 / 0 | 24 / 5 / 6 / 0 | 9 / 4 / 0 / 0 | 24 / 5 / 6 / 1 |
| · días con alguna petición | 11 | 14 | 8 | 14 |
| **máximo diario** frente a `firma_mensajes_dia_max` 2000 | 1 | **7** (2026-04-07) | 2 | 7 |
| saldo final simulado | 97.227,30 | 90.218,33 | 96.124,04 | 90.210,83 |

- **`ultimo_pivote_m1` frente a `referencia_de_la_toma`.** Con el último pivote el bot iguala 2
  operaciones del trader (antes, 0) y puntúa 10 (antes, 2). Con la referencia de la toma no iguala
  ninguna. Encaja con `CAJA-77.md` §3.3: la referencia de la toma casi nunca es el pivote que rompe
  el trader.
- **`r6` frente a `r4`: casi idénticos.** Las mismas órdenes en los mismos puntos, la misma
  cobertura y las mismas operaciones. Cambian una petición (un cierre a mercado más con r4) y el
  saldo en 7,50. El bloque solo mueve el 1 de la caja, es decir el stop, el lote y el objetivo. No
  mueve dónde nace la orden ni cuándo se llena, que es lo que decide la cobertura. **Con esta
  medida, `caja_bloque` no se distingue.**
- **Las peticiones siguen lejos del límite**: como mucho 7 al día frente a 2000. La reubicación
  suma dos por punto nuevo (cancelar y colocar). `modificar` son los break even de RN-014.
- **Lo que hay que mirar, aunque no sea una medida.** En «después», 14 de los 15 llenados acaban en
  el stop, 10 de ellos en menos de 6 minutos y 4 en menos de uno, y el saldo simulado baja de
  97.227 a 90.218.
  Con la caja de R6, el stop al 0,8 queda muy cerca del punto. Toca A-18 (el stop en el 0,8 o en el
  1, `CAJA-77.md` §2.1) y la F de la sesión 4. Aquí no se decide nada.

**El embudo de las 77**:

| paso | antes | después (r6) | referencia | r4 |
|---|---|---|---|---|
| sesión | 0 | 0 | 0 | 0 |
| sesgo | 15 | 15 | 15 | 15 |
| liquidez | 1 | 1 | 1 | 1 |
| breaker | 46 | 44 | 46 | 44 |
| caja | 12 | 12 | 12 | 12 |
| reglas | 3 | 3 | 3 | 3 |
| **coincide** | **0** | **2** | 0 | 2 |

**Límite del embudo**: sus pasos 4 a 6 (breaker, caja, momento) siguen describiendo el esquema del
productor anterior, que el motor todavía calcula pero que ya no es lo que coloca. Con la vida de la
orden stop, **solo son comparables los pasos 1 a 3 y «coincide»**. Adaptar el embudo a la zona del
punto es una rama aparte.

## 3. Lo que no hace

- **No resuelve A-18, A-29, A-48 ni A-49**, ni cambia ningún parámetro CONFIRMED.
- **Los cartuchos siguen sin geometría.** Con la DECISIÓN 2, una sesión con un llenado no vuelve a
  entrar.
- **La vela casi plana (RN-007)** sigue sin umbral.
- **El embudo** no está adaptado (§2).

## 4. Diagnóstico del stop (2026-09-30, revisión del consultor)

> **Pedido tras ver §2.** La sospecha era que el stop del bot fuera demasiado corto, porque 14 de 15
> llenados acababan en el stop. Todo es DIAGNÓSTICO sobre construcción y **ningún valor por defecto
> cambia**. Las corridas se hicieron en clones desechables sobre `7449490`, con los mismos
> diagnósticos que §2.

**Lo nuevo en el código (`7449490`):**
- El selector `caja_se_fija`, de categoría `ejecucion`, DEFAULT_AMBIGUOUS bajo A-49 y con el valor
  `al_verse_el_punto` sin cambiar (ADR-0064 §5). Con `en_cada_cierre_m1`, el 1 de la caja se
  recalcula en cada cierre de M1 hasta el llenado, y RN-006 reubica la orden con su stop y su lote.
- **El embudo adaptado** a la vida de la orden stop, con sus pasos nuevos (nace, punto, bróker,
  reubica, llenado) y el diagnóstico del stop.

**Controles:**
- la rama con `al_darse_el_esquema` da el arnés y el embudo idénticos byte a byte a `main`;
- la combinación por defecto da el arnés idéntico al de §2.

### 4.1 Distancia entrada-stop y tamaño de la caja: el stop NO es más corto que el del trader

Todo en puntos. El trader son las 77 operaciones del libro: entrada menos stop inicial. Su caja con
el stop en el 1 (lo que midió CAJA-77) es esa misma distancia.

| | mínimo | Q1 | mediana | Q3 | máximo |
|---|---|---|---|---|---|
| **stop del bot**, 0,8 (sus 15 llenados) | 5 | 12 | **13** | 18 | 74 |
| **stop del bot**, en el 1 (sus 15 llenados) | 5 | 11 | **16** | 22 | 92 |
| **stop del trader** (77, libro) | 3 | 10 | **15** | 20 | 49 |
| **caja del bot** (sus 15 llenados) | 6 | 14 | **16** | 22 | 92 |
| **caja del trader**, stop en el 1 (77) | 3 | 10 | **15** | 20 | 49 |

- **La caja del bot tiene el tamaño de la del trader**: 16 frente a 15 de mediana. Con el stop al
  0,8, el stop del bot queda 2 puntos por debajo del del trader en la mediana (13 frente a 15); en
  el 1, uno por encima (16).
- **La hipótesis «el stop es demasiado corto» no se sostiene con estas cifras.** Poner el stop en el
  1 no cambia nada (§4.3).

### 4.2 Los 15 llenados (caja fija, stop al 0,8)

| día | orden | lado | caja | stop | min caja → llenado | min llenado → cierre | cierre | spread en el llenado | spread en el cierre |
|---|---|---|---|---|---|---|---|---|---|
| 04-01 | o1 | compra | 17 | 14 | 0,4 | 4,7 | objetivo | 4 | 3 |
| 04-02 | o1 | venta | 43 | 35 | 0,4 | 6,6 | stop | 4 | 4 |
| 04-06 | o1 | compra | 16 | 13 | 1,0 | 5,0 | stop | 4 | 5 |
| 04-07 | o3 | venta | 15 | 12 | 1,4 | 5,7 | stop | 4 | 3 |
| 04-07 | o5 | compra | 22 | 18 | 0,0 | 6,0 | stop | 1 | 1 |
| 04-09 | o1 | compra | 20 | 16 | 1,5 | 0,7 | stop | 4 | 4 |
| 04-10 | o1 | venta | 92 | 74 | 3,8 | 5,8 | stop | 5 | 3 |
| 04-13 | o1 | compra | 6 | 5 | 1,0 | 2,1 | stop | 2 | 5 |
| 04-14 | o1 | compra | 8 | 7 | 0,5 | 0,6 | stop | 4 | 5 |
| 04-14 | o2 | compra | 15 | 12 | 0,8 | 4,1 | stop | 4 | 2 |
| 04-15 | o2 | compra | 65 | 52 | 2,0 | 21,7 | stop | 2 | 1 |
| 04-16 | o1 | compra | 11 | 9 | 0,3 | 0,5 | stop | 4 | 4 |
| 04-16 | o3 | venta | 16 | 13 | 0,5 | 7,5 | stop | 1 | 2 |
| 04-20 | o1 | compra | 14 | 12 | 0,3 | 0,9 | stop | 3 | 5 |
| 04-22 | o1 | venta | 11 | 9 | 2,0 | 1,1 | stop | 5 | 4 |

- **La orden se llena casi en cuanto se fija la caja**: mediana 0,8 minutos, y nunca más de 4.
- **Las posiciones duran poco**: mediana 4,7 minutos hasta el cierre.
- **El spread de Dukascopy en los ticks es de 4 puntos de mediana**, en el llenado y en el cierre.
  Frente a un stop de 13 es casi un tercio. En una compra (10 de 15), la orden salta con el ASK en el
  punto y el stop salta con el BID, así que el margen real hasta el stop es el stop menos el spread.
  Es una sospecha con cifras, no una medida de causa.

### 4.3 Las cuatro combinaciones

| caja | stop | cobertura | operaciones puntuables | llenados → stop | saldo simulado | máximo diario de peticiones (2000) | peticiones en 42 días |
|---|---|---|---|---|---|---|---|
| **fija (el valor)** | **0,8 (el valor)** | **2/77** | 10 | 14 de 15 | 90.218,33 | 7 | 35 |
| fija | 1 | 2/77 | 10 | 14 de 15 | 90.236,11 | 4 | 32 |
| recalculada en cada M1 | 0,8 | 1/77 | 10 | 13 de 15 (+1 manual) | 89.651,41 | 14 | 59 |
| recalculada en cada M1 | 1 | 1/77 | 11 | 15 de 16 | 90.246,58 | 14 | 60 |

- **El stop en el 1 no cambia los llenados ni las salidas**: 14 de 15 al stop, y el saldo apenas se
  mueve. Solo baja el máximo diario de peticiones.
- **Recalcular la caja en cada M1 empeora un poco**: 1 coincidencia en vez de 2, casi el doble de
  peticiones y hasta 14 al día (sigue lejos de 2000). Con esta medida no hay razón para cambiar la
  decisión 5.

### 4.4 El embudo de la vida de la orden (las cuatro combinaciones)

| paso | fija, 0,8 | fija, 1 | recalculada, 0,8 | recalculada, 1 |
|---|---|---|---|---|
| 1. sesión | 0 | 0 | 0 | 0 |
| 2. sesgo | 15 | 15 | 15 | 15 |
| 3. liquidez | 1 | 1 | 1 | 1 |
| **4. nace** | **49** | 49 | 49 | 48 |
| 5. punto | 8 | 8 | 8 | 9 |
| 6. bróker | 0 | 0 | 0 | 0 |
| 7. reubica | 1 | 1 | 2 | 2 |
| 8. llenado | 1 | 1 | 1 | 1 |
| coincide | 2 | 2 | 1 | 1 |

**El hallazgo que manda, y que no es el stop: la cuenta se frena el 22 de abril.**
- La cuenta simulada, que persiste entre días (ADR-0053 §6), llega el 22 de abril a 90.218, casi un
  −10 %. Desde ese día el freno de pérdida total de la firma (RN-031 y RN-032, con
  `firma_margen_seguridad`; RN-001 por `detenido_por_tope_total`) prohíbe toda colocación.
- **El bot no coloca ninguna orden en los 21 días de agosto** ni en los últimos de abril.
- En el embudo, **46 de las 49 operaciones que mueren en «nace» mueren por ese freno** (39 + 7), y 3
  por RN-005.
- **Consecuencia para leer §2 y §4.3**: la cobertura (2 de 77) se mide sobre un tramo en el que, a
  partir del 22 de abril, el bot no puede operar. Las 42 operaciones de agosto no tienen ninguna
  oportunidad. La cifra no dice cuánto iguala el bot cuando puede operar.
- **Lo que haría falta para separarlo** (no se ha hecho, porque no estaba en el encargo): una
  corrida de diagnóstico con la cuenta reiniciada cada día, o sin los gates de la firma, para medir
  cobertura sin el camino de la cuenta.

### 4.5 Lo que el diagnóstico sostiene y lo que no

- **Sostiene**:
  - que el stop y la caja del bot tienen el tamaño de los del trader;
  - que poner el stop en el 1 no cambia los llenados ni las salidas;
  - que recalcular la caja en cada M1 no mejora y cuesta peticiones;
  - que las entradas se llenan al minuto de fijarse la caja y se cierran en unos 5 minutos;
  - que el freno de la firma deja agosto sin operar.
- **No sostiene**:
  - que el problema sea el stop;
  - ni que sea el spread. El spread de 4 puntos frente a un stop de 13 es una sospecha, y medirla
    exige comparar con el spread de FTMO, que es la demo (A-27, DN-3).

## 5. La cuenta reiniciada cada día, el momento, el resultado en R y el spread (2026-09-30, tercera revisión)

> **DIAGNÓSTICO**, pedido tras aceptar §4. **Ningún valor por defecto cambia**: la decisión 5 y el
> stop en el 0,8 se quedan.
>
> **Código**: `c02755d`.
> - `--diagnostico-cuenta-diaria` en `motor arnes --simular` y `--cuenta-diaria` en `embudo_77`.
>   La cuenta empieza de cero cada día, y la etiqueta `DIAGNOSTICO-CUENTA-diaria` va en cada línea y
>   en el nombre del fichero. La corrida normal sigue arrastrando la cuenta (ADR-0053 §6).
> - El embudo gana la tabla por mes, el momento, el R, las compras y ventas y el precio mid.
> - `scripts/f35_resultado_r.py` cruza el R del bot con el del trader.
>
> **Dónde se corrió**: el arnés y el embudo, en un clon desechable. El cruce de R, desde el
> repositorio, porque lee el libro de `corpus/`; solo lee y escribe fuera.

### 5.1 Con la cuenta reiniciada cada día

| | cuenta arrastrada (la normal) | **cuenta reiniciada cada día** |
|---|---|---|
| cobertura | 2/77 | **7/77** (abril 4, agosto 3) |
| operaciones puntuables | 10 | **30** |
| llenados | 15 (solo abril) | **36** (19 en abril, 17 en agosto) |
| llenados que acaban en el stop | 14 de 15 | **33 de 36** |
| máximo diario de peticiones (2000) | 7 | 7 |

**El embudo de la vida, por mes (cuenta reiniciada):**

| paso | todas | abril | agosto |
|---|---|---|---|
| sesión | 0 | 0 | 0 |
| sesgo | 15 | 9 | 6 |
| liquidez | 1 | 0 | 1 |
| nace | 22 | 8 | 14 |
| **punto** | **26** | 12 | 14 |
| bróker | 2 | 0 | 2 |
| reubica | 2 | 1 | 1 |
| llenado | 2 | 1 | 1 |
| **coincide** | **7** | 4 | 3 |

- **Sin el freno de la cuenta, agosto opera** y el primer sitio donde se pierde una operación deja
  de ser «nace» (de 49 a 22) y pasa a ser **«punto»: el bot pone la orden en un punto que no es el
  del trader (26)**.
- De las 22 de «nace», 18 las prohíbe RN-005, el lado de ruido, y 4 son sesiones con puntos pero sin
  orden.
- El freno de la firma ya no aparece.

### 5.2 El momento de entrada

Minutos desde que se forma el último pivote de M1 contrario a la entrada (el 0 de R5, al cierre de
su vela contraria) hasta el llenado. Es la misma función para los dos.

| | n | mínimo | Q1 | mediana | Q3 | máximo |
|---|---|---|---|---|---|---|
| **bot** (cuenta reiniciada) | 36 | 0 | 0,4 | **0,9** | 1,4 | 3,8 |
| **trader** (las 77) | 77 | 0,2 | 1,2 | **2,5** | 5,2 | 12,2 |

**El bot entra antes que el trader**: más o menos a la mitad de tiempo desde que se forma el
pivote, y el trader tiene una cola hasta 12 minutos que el bot no tiene. El bot coloca en cuanto ve
el pivote y la primera vela que lo toca lo llena. Encaja con §5.1: su punto no es el del trader en
26 de 77.

### 5.3 El resultado en R, bot frente a trader

- **Bot**: R sobre su stop inicial, con la cuenta reiniciada.
- **Trader**: `viabilidad_trader.py` en sus dos series, la ANOTADA (la salida real del libro) y la
  SIMULADA (repetida por el bróker sobre ticks).

| | n | Q1 | mediana | Q3 | media | ganadoras |
|---|---|---|---|---|---|---|
| **bot**, todos los días | 36 | −1,00 | −1,00 | 0,00 | **−0,44** | **3 (8 %)** |
| **trader, anotada** | 77 | −1,00 | −0,77 | 3,22 | **+0,98** | **33 (43 %)** |
| trader, simulada | 73 | −1,00 | −1,00 | 3,00 | +0,62 | 32 (44 %) |
| bot, abril / agosto | 19 / 17 | | −1,00 / −1,00 | | −0,38 / −0,52 | 2 (11 %) / 1 (6 %) |
| trader anotada, abril / agosto | 35 / 42 | | −0,77 / 0,00 | | +1,05 / +0,93 | 15 (43 %) / 18 (43 %) |
| **en los 23 días en que operan los dos**: bot | 30 | −1,00 | −1,00 | 0,00 | −0,43 | 3 (10 %) |
| mismos días: trader anotada | 50 | −1,00 | −1,00 | 3,29 | +0,94 | 21 (42 %) |

- **La diferencia no es de tamaño de pérdida, es de acierto.** Las pérdidas del bot son de 1 R, como
  las del trader, y su stop mide lo mismo (§4.1). Pero gana el 8 % y el trader el 43 %.
- Q3 = 0 en el bot son los break even de RN-014.

**Compras y ventas**:

| | compras | ventas |
|---|---|---|
| bot, cuenta reiniciada | 19 | 17 |
| trader | 32 | 45 |
| bot, cuenta arrastrada | 10 | 5 |

El bot está equilibrado; el trader vende más (58 %).

### 5.4 El spread: con el precio medio, ningún stop se salva

Para cada llenado que acabó en el stop se recorrieron los ticks con el precio medio (bid + ask) / 2,
desde el llenado hasta el fin de la ventana, mirando qué salta primero, el stop o el objetivo.

| | stops con bid y ask | con el precio medio: siguen en el stop | se salvan |
|---|---|---|---|
| compras | 17 | 17 | **0** |
| ventas | 16 | 16 | **0** |

**El spread no explica las pérdidas**: con el precio medio saltan los mismos 33 stops.

### 5.5 Lo que el diagnóstico sostiene y lo que no

- **Sostiene**:
  - que el freno de la cuenta tapaba agosto: sin él la cobertura sube de 2 a 7 de 77;
  - que ni el tamaño del stop (§4) ni el spread (§5.4) explican las pérdidas;
  - que el bot entra antes que el trader desde el pivote (0,9 frente a 2,5 minutos de mediana);
  - que con la cuenta reiniciada su punto no es el del trader en 26 de 77;
  - que gana el 8 % de sus operaciones frente al 43 % del trader.
- **No sostiene** qué espera el trader después del pivote. Los 1,6 minutos de diferencia en la
  mediana, y una cola hasta 12, dicen que no entra en el primer toque, no por qué. Es la pregunta de
  la F de la sesión 4 («¿pones la orden en el último mínimo que se formó en M1 y la vas moviendo?»):
  queda más afilada, porque el bot, que hace justo eso, entra antes y pierde.

### 5.6 Punto 5 del encargo: ffmpeg en la CI se queda

La CI no instala el grupo `asr`, pero **cuatro ficheros de test necesitan ffprobe o ffmpeg**:
`tests/unit/test_audio.py`, `tests/unit/test_inventario.py`,
`tests/unit/test_pipeline_transcripcion.py` y `tests/integration/test_fotogramas_ffmpeg.py`. Con
`CI` o `BOTSITO_EXIGE_FFPROBE` definidas, fallan en vez de saltarse, que es lo que pone el workflow.
**No se ha quitado.** La lentitud del 30 de septiembre fue del espejo de `apt` del runner (20 min en
`apt-get install`), no de la instalación en sí.

## Estado

**ACEPTADA por el consultor el 2026-09-30, con orden de cierre en `main`.** ADR-0064 queda ACEPTADO
en su dirección, con sus valores en DEFAULT_AMBIGUOUS bajo A-48 y A-29 (`orden_stop_punto`,
`caja_bloque`, `caja_se_fija`). Ningún valor por defecto cambia al cerrar. El tag no lleva «F35» en el
nombre, porque en MASTER_PLAN F35 es la puerta del go-live.

Lo que sigue es el estado previo a la revisión, sin tocar.

Lista para revisión, **no cerrada**. Commits:
- `051d4c6`: el código;
- `2ea0390`: la medida de §2;
- `7449490`: `caja_se_fija` y el embudo de la vida;
- `17460d7`: el informe con §4;
- `c02755d`: la cuenta diaria y el resto del diagnóstico de §5;
- el de este informe con §5.

Cada uno con `make check` en verde y sellado. Ningún valor por defecto ha cambiado en la revisión.
Pendientes del consultor: las seis DECISIONES de ADR-0064 y lo que §5 destapa. El bot entra antes
que el trader y en otro punto, y gana el 8 % frente al 43 %.
