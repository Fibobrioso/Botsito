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

## Estado

Lista para revisión, **no cerrada**:
- `make check` en verde y sellado sobre el código (`051d4c6`) y sobre este informe;
- la CI de Linux va en el resumen de la sesión;
- pendiente de la revisión del consultor: ADR-0064, las seis DECISIONES y el ítem
  `ev-v7-001550-82e5cffc`.
