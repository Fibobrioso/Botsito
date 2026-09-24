# El criterio de fidelidad en desarrollo, antes del motor (ADR-0043)

Rama `trabajo/criterio-fidelidad`, 2026-09-24. Es el punto 18 de Next Action. Sin merge, sin tag y
sin push.

En esta rama no se ha escrito ni una línea del motor, ni se ha ejecutado nada que simule decisiones
del bot. Tampoco se ha abierto nada de septiembre ni de febrero. `PREREGISTRO.md` sigue vacío y no
se ha firmado ninguna autorización.

## 0. El paso 0

- **Un «punto» es 0,00001**, y no es ambiguo:
  - `src/botsito/domain/velas.py` dice «los precios son `Puntos` (enteros) con la `escala` de la
    serie (EURUSD: 100000 puntos por unidad)»;
  - `ABRIL-Y-LA-CAJA.md` dice «las series cuadran a 1 y 2 puntos (0,1 y 0,2 pips)»;
  - ADR-0039 usa la misma unidad en su `[mínima − 2, máxima + 2]`.
- **El siguiente ADR libre era el 0043.**

## 1. El instante del xlsx es el LLENADO (`d641cba`)

**La medida.** `scripts/instante_llenado.py`, con su test sintético
(`tests/unit/test_instante_llenado.py`). Se ejecutó una sola vez sobre las 94 operaciones `dev`, y
su salida está tal cual en `docs/validation/INSTANTE-LLENADO-SALIDA.txt`.

**La regla, fijada antes de medir por el consultor:**
- la entrada tiene que caer dentro de `[mínima − 2, máxima + 2]` puntos de la vela M1 de su
  instante;
- ≥ 90 % dentro → llenado; ≤ 50 % → colocación; entre las dos → se pregunta al trader;
- si el control a −30 y +30 min no baja, la medida no vale.

**Cómo se hizo operativo «el control baja»:** cada control tiene que quedar por debajo del 50 % y
por debajo de la tasa del instante. Si no, el veredicto es «la medida NO VALE».

**El resultado:**

| | instante | −30 min | +30 min |
|---|---|---|---|
| abril | 34/35 = 97,1 % | 5,7 % | 11,4 % |
| mayo | 17/17 = 100,0 % | 0,0 % | 5,9 % |
| agosto | 42/42 = 100,0 % | 7,1 % | 16,7 % |
| **total** | **93/94 = 98,9 %** | **5,3 %** | **12,8 %** |

**Veredicto: LLENADO.** El control cae claramente.

**No es del todo independiente.** Este mismo test, `[mínima − 2, máxima + 2]` sobre la M1, es el
que fijó el huso de los libros (ADR-0039). Lo nuevo es el control. Y el 98,9 % dice que, con el
huso ya fijado, la entrada cae en el minuto del instante; no prueba el huso por segunda vez.

## 2. El criterio (ADR-0043), literal

- **Unidad:** la operación, dentro de su día y su sesión.
- **Emparejamiento uno a uno:**
  - una operación del bot empareja con una del trader si coinciden el día, la sesión y la
    dirección, |Δentrada| ≤ 3 puntos y |Δinstante de llenado| ≤ 15 min;
  - si hay varias candidatas, gana la de menor |Δinstante|, luego la de menor |Δentrada|, y luego
    la más temprana (determinista).
- **Métricas:**
  - cobertura = operaciones del trader emparejadas / operaciones del trader;
  - precisión = operaciones del bot emparejadas / operaciones del bot, contando solo los días con
    al menos una operación del trader;
  - las operaciones del bot en días sin ninguna del trader se informan aparte y no puntúan
    (ADR-0016);
  - se informa también la distribución de Δinstante (cuántas en el mismo minuto) y de Δentrada.
- **Fuera del criterio hasta que se resuelva su ambigüedad:** stop (A-18, A-31), TP y resultado
  (ADR-0037 §7), gestión (A-13, A-33).
- **Conjuntos:**
  - construcción = abril y agosto;
  - medida = mayo (y marzo cuando entre);
  - mayo se mide una vez por versión de la spec; si la spec cambia después de ver el resultado de
    mayo, mayo pasa a construcción y queda escrito.
- **Umbral de desarrollo:** cobertura ≥ 70 % y precisión ≥ 60 % sobre el conjunto de medida. Esto
  NO es el PREREGISTRO del holdout.
- **Calentamiento:** el bot puede leer velas de días anteriores para su sesgo; solo puntúan los días
  evaluados. Leer velas no es abrir casos (ADR-0021 §1).
- **Cambios:** este criterio no se modifica una vez que el motor produzca su primera salida sobre el
  conjunto de medida, salvo con un ADR nuevo que diga por qué y declare quemado lo que se haya
  visto.

## 3. La función del criterio, sin motor

**Las cifras** están en `knowledge/cases/criterio_fidelidad.yaml`, porque `src/` no admite cifras
de negocio (ADR-0002, `test_no_business_literals`): 3 puntos, 15 min, escala 100000, 0,70 y 0,60,
construcción `2026-04` y `2026-08`, y medida `2026-05`.

**La función es pura** (`src/botsito/cases/criterio_fidelidad.py`):
- `emparejar` y `medir`;
- **el desempate es voraz y global:** se ordenan todas las parejas compatibles por |Δinstante|,
  luego |Δentrada|, luego la más temprana, y ninguna operación se usa dos veces;
- **sin denominador, la métrica es `None`**, «sin definir». Nunca divide por cero.

**Los tests** (`tests/unit/test_criterio_fidelidad.py`) usan solo operaciones sintéticas y cubren
los casos obligatorios:
- el emparejamiento exacto;
- fuera de tolerancia de entrada (3 puntos dentro, 4 fuera);
- fuera de tolerancia de tiempo (15 min dentro, 15,5 fuera);
- dirección contraria;
- dos candidatas, que se desempatan por |Δinstante|, luego por |Δentrada| y luego por la más
  temprana, sea cual sea el orden de entrada;
- una operación del bot en un día sin operaciones del trader, que se informa aparte y no puntúa;
- cero operaciones del bot: cobertura 0 y precisión sin definir.

Y además:
- otra sesión u otro día no emparejan;
- el uno a uno no reutiliza una operación;
- cero operaciones del trader dejan la cobertura sin definir;
- el fichero del criterio dice lo que dice ADR-0043.

## 4. Cierre

- `make check` en verde en cada commit, con el log borrado. El commit solo se hacía si pasaba.
- Guardia de ids OK.
- `state check` OK.
- `kit check` del paquete de la sesión 1 y `fidelidad check` idénticos a su línea base.
- PREREGISTRO con blob `52649183…`.
- Cero autorizaciones.

## Estado

WAITING_FOR_USER_VALIDATION
