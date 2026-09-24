# El motor, primera regla: el sesgo H4 (RN-003, ADR-0044)

Rama `trabajo/motor-sesgo-h4`, 2026-09-24. Es el punto 19 de Next Action. Sin merge, sin tag y sin
push.

No se ha abierto nada de septiembre ni de febrero. **Mayo no se ha tocado**: ni sus casos, ni
ninguna medida sobre él, porque es el conjunto de medida de ADR-0043.

## 0. El paso 0: RN-003 dejaba cuatro cosas sin definir

Se leyeron RN-003, sus tres parámetros (todos CONFIRMED; `anclaje_h4` está sin verificar en FTMO),
la agregación H4 y los contratos de import-linter. La rama se paró antes de escribir código, con
cuatro preguntas:

1. ¿Qué pasa si la vela rompe los dos extremos de la anterior?
2. ¿Cuál es el estado inicial, y cuánto se mira hacia atrás?
3. ¿El sesgo se fija al abrir la sesión, como dice RN-003, o en cualquier instante?
4. ¿Qué es exactamente un equal?

**Y una propuesta**, que el consultor aceptó: una vela se da por cerrada por su hora de **fin**, no
por la marca `completa` de la agregación. Esa marca depende de cuántas M1 recibe, y con el día
entero marcaría como cerrada la vela en curso.

## 1. Las decisiones: ADR-0044 y la spec (`818de5f`)

1. **Si la vela rompe los dos extremos**, el sesgo es AMBIGUO y no se opera. Queda abierta **A-34**,
   una pregunta para el trader.
2. **Estado inicial.**
   - Se busca hacia atrás la última H4 que rompió, con un tope de `sesgo_h4_tope_velas` = 60.
   - Si no la hay, el sesgo es INSUFICIENTE y no se opera.
   - El tope es una decisión **provisional del proyecto**. Va en la categoría `ejecucion`, no en
     `estrategia`, porque el registro exige, con un test, que un valor de estrategia solo lo diga
     el trader.
3. **El sesgo se fija AL ABRIR la sesión**, con las H4 cuyo fin es anterior o igual a la apertura.
   En las semanas de desfase entre la UE y EE. UU., la H4 que cierra a mitad de sesión cuenta desde
   la sesión siguiente.
4. **Romper es superar el extremo por al menos 1 punto** (0,00001). Una diferencia de 0 es un equal
   y no rompe. A-16 queda anotada: la serie del trader y la nuestra difieren 1-2 puntos.

**Qué cambió en la spec:**
- RN-003 recoge las cuatro decisiones y declara `decision: ADR-0044`, porque ahora opera sobre un
  parámetro que no dijo el trader.
- La spec pasa de 12.1.1 a **12.2.0**. Es una versión menor, porque entra un parámetro nuevo.
- `docs/spec` se regeneró en el mismo commit.

**Un ajuste que pidió la guardia de la spec:** `entonces` no admite cifras, ni en número ni en
letra. Por eso «un punto» se escribió «por poco que sea», y las referencias a A-34 y ADR-0044
quedaron en las notas.

## 2. El sesgo, en el dominio (`5616bc5`)

- **Dónde vive:** `src/botsito/domain/sesgo.py`, con la firma `sesgo_h4(velas_h4, apertura_sesion,
  tope, criterio)`.
- **Qué recibe:** velas ya agregadas, con los precios como enteros en puntos, y el minuto UTC de la
  apertura.
- **Qué devuelve:** ALCISTA, BAJISTA, AMBIGUO o INSUFICIENTE, junto con cuánto rompió la vela que
  decide y cuántas velas se miraron.
- **Pureza:** no importa `datetime` ni `zoneinfo`, como exige import-linter.
- **La rejilla H4** con `anclaje_h4` la sigue construyendo `data.agregacion`.
- **Sin cifras en el código:** el tope y el criterio de ruptura los pasa quien llama, leídos del
  registro.

**Tests** (`tests/unit/test_sesgo_h4.py`), todos sintéticos:
- **Las ramas de la regla:**
  - rompe arriba, y el color de la vela no decide;
  - rompe abajo;
  - no rompe, y el sesgo se arrastra;
  - un equal no rompe;
  - romper por un punto basta;
  - rompe los dos extremos, y es ambiguo;
  - sin ruptura dentro del tope, es insuficiente;
  - con menos de dos velas, es insuficiente;
  - con el criterio cuerpo, la mecha no rompe.
- **Sin mirar el futuro:** añadir velas posteriores a la apertura no cambia nada, y una vela en
  curso marcada `completa` no cuenta.
- **Cambio de hora de EE. UU.**, en primavera (2026-03-10) y en otoño (2026-10-27), sobre la
  agregación real con el anclaje del servidor. La H4 que cierra a mitad de la sesión de las 07
  cuenta en la de las 11. En verano, una vela que termina justo en la apertura sí cuenta.
- **El registro** da el tope y el criterio de ADR-0044.

## 3. El diagnóstico sobre construcción (`99a81e3`)

**Qué es.** `scripts/sesgo_h4_diagnostico.py`, ejecutado una sola vez sobre las 77 operaciones de
abril y agosto. Mayo no se lee. La salida está tal cual en `SESGO-H4-DIAGNOSTICO.txt`.

**Qué se compara.** El sesgo del bot al abrir la sesión de cada operación, frente a la dirección de
la operación.

| | operaciones | a favor | en contra | ambiguo | insuficiente | ruptura de 1-2 puntos (zona A-16) |
|---|---|---|---|---|---|---|
| abril | 35 | 24 | 7 | 4 | 0 | 0 |
| agosto | 42 | 34 | 5 | 3 | 0 | 0 |
| **total** | **77** | **58** | **12** | **7** | **0** | **0** |

- **No es una medida de fidelidad** (ADR-0043): no tiene umbral, y la regla no se cambia por lo que
  sale.
- **Las 12 operaciones en contra** se anotan en A-26, que pregunta por el flujo de M15 contra el
  sesgo de H4. No toca la regla. Son recuentos: no se nombra ninguna operación.
- **Las 7 ambiguas** son sesiones en que el bot no operaría mientras A-34 siga abierta.
- **Ninguna ruptura cae en la zona de 1-2 puntos**, así que en este material A-16 no decidió ningún
  sesgo.
- **Sobre el calentamiento.**
  - Abril no tiene el mes anterior, porque no hay dataset de marzo, y aun así no sale ningún
    insuficiente.
  - Agosto calienta con las velas de julio. Leer velas no es abrir casos (ADR-0043, ADR-0021 §1).

## 4. La siguiente regla en orden causal: RN-004, y está BLOQUEADA

- **RN-004** es «la liquidez de M15 se toma con cuerpo». Su `cuando` es «el precio alcanza el alto o
  el bajo de M15 marcado», y lee el token `liquidez_m15`.
- **Ningún `fijar` de la spec produce ese token.** Lo dice la propia nota de RN-004: es el hueco del
  productor que anotó `trabajo/liquidez-m15`.
- **Qué regla marcaría ese nivel:** es exactamente **A-24**, «qué hace que marques un pivote de
  M15», y A-24 es **bloqueante**.
- **Así que el paso siguiente no se puede codificar sin decidir antes A-24**, sea el trader o una
  decisión del consultor.

## 5. Cierre

- **`make check`** en verde en cada commit, con el log borrado. El commit solo se hacía si pasaba.
- **Un intento de commit salió en rojo y no se hizo:** el del tope como parámetro de `estrategia`,
  que el test del registro rechazó. Se recategorizó y el commit salió en verde.
- **Comprobaciones:**
  - guardia de ids OK;
  - `state check` OK;
  - `kit check` del paquete de la sesión 1 y `fidelidad check` idénticos a su línea base;
  - PREREGISTRO con blob `52649183…`;
  - cero autorizaciones.

## Estado

WAITING_FOR_USER_VALIDATION
