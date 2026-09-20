# La liquidez de M15: quién la marca, y el eje que F14b tenía al revés

Rama `trabajo/liquidez-m15`, desde `60216f8` (tag `stable/F13-breaker`). Sin tocar main, sin merge,
sin tag, sin push. Sin abrir holdout, ni xlsx, ni capturas de Analytics: fotogramas de v1/v3/v4,
transcripciones crudas y el repositorio.

## 1. La revisión de diseño, antes de escribir nada

Dos agentes en paralelo, los dos obligados a **abrir los fotogramas antes de opinar**: uno midió la
pantalla (v3 0:12:42‑0:13:00, v3 0:15:31‑0:15:44 y el contexto de 0:15:08); el otro, el repositorio
—el hueco del productor, A‑25, A‑26 y las guardias—, mirando también los fotogramas.

**Discreparon en lo principal** —si A‑24 es una elección o dos casos— y esa discrepancia la resolvió
la pantalla, no el arbitraje. Lo que sigue está medido por la sesión, no solo por los agentes.

| Instante | Lo que hay en pantalla | Cita |
|---|---|---|
| v3 0:12:42‑0:13:01 | **Gráfico en 1h**, no en M15: el título dice «Euro/Dólar estadounidense · **1h** · FXCM» mientras el audio dice «esto es en M15». El *complex pullback* es un **croquis a mano alzada**, no pivotes de mercado. En ese croquis, la escalera es monótona ascendente: **el alto más alto es además el último** | `fr-v3-982da728/781000`, `/786000` |
| v3 0:13:26 | Un nivel con **etiqueta escrita a mano: «m15 lq»** | `fr-v3-982da728/806000` |
| v3 0:15:08 | **M15** («· 15 ·»). El sesgo bajista no se lee aquí: está en el audio («esto es H4, está bajista») y en `ev-v3-001508-e1a49a38` | `fr-v3-982da728/908000` |
| v3 0:15:38 y 0:15:44 | **M15.** Primero un segmento sobre el alto anterior y más alto; después **otro nivel, con sus dos círculos de extremo**, más abajo y más a la derecha, **pegado al precio**. El primero se queda sin marcar | `fr-v3-982da728/938000`, `/944000` |
| v4 0:57:06 | **M15.** Lo marcado es una **línea horizontal etiquetada «15 lq»** a ~1,17375. Ningún rectángulo, ninguna banda | `fr-v4-9ad0ebb8/3423000`, `/3426000` |
| v1 0:14:15 | **Gráfico en 1m.** Es donde el trader dice «el último pico en este retroceso complejo» | `fr-v1-5a2a42c3/855000` |

## 2. A‑24 no es una elección, y tampoco son dos casos

La hipótesis del consultor —que el criterio dependa del tipo de estructura— **se cae**, y la mata el
croquis:

1. **En el croquis del *complex pullback*, el alto más alto es a la vez el último.** Ese dibujo no
   distingue «el más alto» de «el más reciente», así que `ev-v3-001242` no sostiene un criterio rival.
   Y está dicho sobre un gráfico de **1h**, no sobre M15.
2. **«Estructura simple», «retroceso simple», «pullback simple»: cero apariciones** en `knowledge/`,
   en `data/transcripciones/` y en `docs/`. La variable que discriminaría **no tiene nombre en el
   corpus**.
3. **El eje de F14b tampoco existe.** `ev-v3-001531` —el que sostenía el polo «más extremo»— mide lo
   mismo que `ev-v1-001334` y `ev-v4-010921`: en pantalla el trader **descarta** el alto más alto y
   marca el de abajo, que con sesgo bajista es el **menos extremo, el más próximo y el más reciente**
   a la vez.

**Conclusión: los cuatro items apuntan al mismo polo.** No hay contradicción que arbitrar, y A‑24
pasa a ser lo que siempre debió ser: **una regla de selección abierta**, anclada en el caso medido.

### La tercera pata, y por qué la retiro

En la revisión apareció como apoyo v1 0:14:13 («el último pico en este retroceso complejo»), que **no
tenía item**. Lo he creado por la vía normal (`ev-v1-001403-eea19530`) y, medido, **no sirve de
apoyo**: en `fr-v1-5a2a42c3/855000` el gráfico es **M1**, y la frase va del límite que el trader va
bajando, no de la liquidez de M15. Queda en el corpus porque es material real, y queda **fuera** del
razonamiento: la conclusión se sostiene sobre las dos patas de arriba.

## 3. A‑24 redactada, con las dos condiciones del consultor

Abierta en `knowledge/spec/ambiguedades.yaml` con su id reservado, `clase: pregunta`,
`bloqueante: true`:

> Cuando en M15 tienes varios pivotes candidatos, ¿qué hace que marques uno y no otro? En v3 0:15:31
> (`fr-v3-982da728/944000`) descartas expresamente el alto más alto —«aunque yo invadiría este
> alto»— y marcas el de abajo, el que te deja el precio. No te preguntamos si es «el más reciente» o
> «el más extremo»: las dos veces que lo hemos medido, el que eliges es el mismo. La pregunta es por
> el **criterio**, y lo necesitamos dicho de forma que se pueda reproducir sin ti: que dos personas
> mirando el mismo gráfico marquen el mismo nivel. Si la respuesta es «el que yo considere»
> (v3 0:39:16, `ev-v3-003916-447dc8d7`), dinos **qué miras** para considerarlo: cuántas velas
> atrás, qué tamaño de movimiento, qué lo descalifica.

**Sin menú falso** —va abierta y anclada en la pantalla— y **pidiendo un criterio operativo**.

### El riesgo de fidelidad, dicho como es

El trader dice «marcas tu zona de liquidez **que tú consideres**» (`ev-v3-003916-447dc8d7`) y
«tienes tiempo de sobra para **marcar tú** tus zonas» (v3 0:15:28, cruda). **Si la respuesta de la sesión 2 se queda en juicio
humano, el bot no puede reproducirlo.** Eso no es un detalle de la spec: es un riesgo de fidelidad
**del proyecto entero**. Todo lo que hay aguas abajo —los dos esquemas de entrada, la orden límite,
el reinicio de cartuchos, el único filtro direccional— cuelga de un nivel que hoy pone una persona a
ojo. Si A‑24 no sale con un criterio reproducible, la respuesta honesta no es inventar la regla: es
decidir si el bot marca peor que el trader y cuánto cuesta eso en fidelidad, que es una pregunta de
proyecto y no de esta rama.

## 4. El hueco del productor: verificado, y peor que «no dispara»

`liquidez_m15` tiene **cero producciones**: su declaración (`strategy_spec.yaml:420`) y tres
lecturas —RN‑004 en `:706` y `:707`, RN‑005 en `:743`—. Ningún `fijar`, ningún `hace`.

```
liquidez_m15 sin productor
 └─ RN-004 nunca fija liquidez_tomada
     ├─ se_da_esquema nunca cierto  → RN-008 es un `ninguno_de`: prohibe abrir_operacion SIEMPRE
     └─ toca_colocar_orden_limite nunca cierto → RN-011 y RN-015 nunca colocan la orden
 └─ RN-005, el unico filtro direccional, vigila el lado de ruido de un nivel que no existe
 └─ cartuchos_reinicio = siguiente_liquidez_m15 (CONFIRMED) espera un reinicio imposible
```

**Por qué ninguna guardia lo ve, medido:** `CLAVES_VOCABULARIO["tokens"]` es literalmente
`{descripcion, clase}`, así que **un token no tiene dónde declarar productor**; y la guardia que
nació de `se_coloca_orden_limite` (`_problemas_lo_provoca`) solo se invoca para predicados con
`fuente` en `(broker, bot)` y para hechos de `origen: broker`, mientras que a los de `mercado` se les
**prohíbe** declarar `lo_provoca`. Los tres lectores son `fuente: mercado`. El hueco es estructural.

**Anotado y no tapado:** nota en RN‑004 y en el token, con la cadena entera, y **ninguna regla de
marcado nueva**. Deuda técnica en `PROJECT_STATE.md`.

## 5. A‑25 y A‑26, sustituidas conservando sus ids

- **A‑25** ya no pregunta por «un pivote que invalida una liquidez ya tomada» —eso no lo dice ni el
  corpus ni ninguna pantalla: la premisa era del análisis—. Pregunta por **la vida de la marca**: si
  se mueve mientras vive, o solo la retiran el trade ganador, la invalidación o el cambio de día.
- **A‑26** conserva solo lo que sigue abierto. **La mitad cerrada se ha escrito en la spec**, como
  pediste: el token `liquidez_m15` dice ahora que la vela que lo marca es contraria al **flujo de
  M15**, no al sesgo de H4, con sus cuatro citas (`ev-v3-001204-889179d2`, `ev-v4-003451-d750e553`,
  `ev-v6-003701-7613b381`, `ev-v3-011147-fa2e6984`: «sería solo M15, M15 y ya»). Lo que se pregunta
  es el choque: en v3 0:12:42 el sesgo de H4 es bajista y el flujo de M15 es un *pullback alcista*,
  y RN‑005 lee hoy el lado de ruido del `sesgo`.

## 6. A‑33 no se abre: la pantalla ya responde

Fui a medir v4 0:57:03 antes de abrirla, y **la pantalla la cierra**: lo que el trader deja dibujado
es una **línea** etiquetada «15 lq», no una banda (`fr-v4-9ad0ebb8/3426000`). Abrir una ambigüedad
que la pantalla responde es el error que este proyecto ya ha repetido, así que lo que entra es una
**nota en el token**: la liquidez es un nivel, que es lo que `alcanza_nivel` y `cruza` necesitan.

## 7. Tres items con el mismo vicio: eso es un patrón de extracción

| Item | Cita | Afirmación de más | Cuándo |
|---|---|---|---|
| `ev-v4-005319-dee95093` | «el precio me rompe **aquí** con mecha» | «una rotura con mecha no valida el trade», sin decir de qué ruptura | 2026‑09‑17 |
| `ev-v3-001531-1b12a896` | «**suelo** usar… **en este caso** la zona más baja» | «usa la zona de liquidez más baja… en M15», regla general | hoy |
| `ev-v4-005703-4e43180e` | «todo lo que hay es liquidez… **me es indiferente**» | «todo el rango de M15 lo considera liquidez», una banda | hoy |

**Los tres son el mismo error de extracción:** la `afirmacion` **quita el deíctico o el matiz** de la
cita («aquí», «suelo», «en este caso», «me es indiferente») y la convierte en regla general. Los tres
son de `extractor: llm`, revisados en la hoja F07 del 2026‑09‑07, y los tres se detectaron **mirando
la pantalla**, no releyendo el texto. La regla 2 del prompt del proponente dice «`afirmacion` normaliza
la cita **sin añadir condiciones que la cita no diga**»; lo que falla es lo contrario —**quitar** las
que sí dice—, y eso el prompt no lo prohíbe con esas palabras. No lo arregla esta rama: queda escrito
aquí y en el HANDOFF para que el próximo repaso de F07 lo mire con esa lente.

Los dos de hoy se han supersedido con `evidence new --supersede` (la vía de propuesta no admite
`supersede`, deuda ya anotada el 2026‑09‑17):
`ev-v3-001528-87eef4f0` y `ev-v4-005644-e06ef304`, los dos con cita de audio **y** de pantalla.

**Guardias medidas antes de aceptar**, con el método de `BREAKER-M1.md` §2: ningún registro de
feedback tiene a estos items como objetivo, ninguna ambigüedad los citaba y el cuestionario de la
sesión 1 no los usa; `knowledge validate` da 368 items y 0 contradicciones. `F14b` §3 y
`AUDITORIA-2026-09-12-material.md`, que citaban `ev-v3-001531` por id, quedan actualizados en el
mismo commit.

## 8. El detector de contradicciones: tercera aparición

Los ~10 items que describen qué nivel es la liquidez viven en **temas hermanos** y **ninguno tiene
`valor`**: invisibles por los dos motivos.

**Y un punto ciego más, encontrado al validar esta rama:** una `pregunta` de ambigüedad puede
**nombrar un instante del corpus sin enlazar su item** —A‑24 citaba «v3 0:39:16», el item que
sostiene el riesgo de fidelidad entero, y no estaba en su `evidencia:`— y **ninguna guardia se
queja**: se comprueba que los ids de `evidencia:` existan, nunca que las marcas de tiempo de la prosa
tengan item. Corregido a mano aquí (A‑25 y A‑26 se revisaron igual y estaban completas). La guardia
**no se hace en esta rama**: queda contado. Van contados en `PROJECT_STATE.md` como la tercera vez
—0,75 en 2026‑09‑12, el breaker en 2026‑09‑17, la liquidez hoy— y con la consecuencia escrita: **a la
tercera deja de ser deuda y pasa a rama con nombre**, que la próxima planificación abre. No se toca
aquí.

## 9. Lo que NO se ha hecho

- **Ninguna regla de marcado.** Es lo que A‑24 decide.
- **F14b §2** (hechos durativos) no se toca.
- **v1 0:14:54** (`stop.origen_vela_contraria`) queda anotado y sin tocar: es otra rama.
- **`_contradicciones.yaml`** se regenera y sigue en 0.
- **Holdout**: nada. `knowledge/feedback/` intacto.

## 10. Qué debe decidir el usuario

1. **¿Validar la rama** y hacer el ritual (`docs/runbooks/RITUAL.md`, tag `stable/F13-liquidez`)?
2. **A‑24 con `bloqueante: true`**: hoy solo tres ambigüedades lo llevan. La justificación es que sin
   ella no hay entrada posible. ¿De acuerdo?
3. **El riesgo de fidelidad del §3**: si la sesión 2 responde «el que yo considere», ¿se decide ahí
   mismo o se lleva a una pregunta de proyecto aparte?
4. **El patrón de extracción del §7**: ¿repaso de los items de `extractor: llm` con esa lente, y
   cuándo?

## 11. Cómo comprobarlo

```
uv run botsito corpus frames show --video v3 --t 0:15:44 --n 3
cat knowledge/evidence/v3/ev-v3-001528-87eef4f0.yaml
cat knowledge/evidence/v4/ev-v4-005644-e06ef304.yaml
grep -n "liquidez_m15" knowledge/spec/strategy_spec.yaml
uv run botsito knowledge validate     # 368 items, 32 ambiguedades, 0 contradicciones
uv run botsito spec check             # 32 reglas, hash al dia (12.1.1)
make check > make-check.log 2>&1; echo "exit=$?"
```

## Estado
WAITING_FOR_USER_VALIDATION
