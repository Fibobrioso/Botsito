# F14b · el ciclo de vida de los hechos (propuesta, NO aplicada)

**Estado:** PROPUESTA. Sale de la auditoría del 2026-09-12
(`docs/validation/AUDITORIA-2026-09-12-material.md` §2) y de un diseño encargado a un agente el
mismo día. **No se ha aplicado nada de este documento**, salvo lo que se dice en §0.

> **Numeración obsoleta (2026-09-14).** Los ids de regla de este documento son PROVISIONALES y
> quedaron obsoletos: RN-029 y RN-030 ya existen en la spec con otro significado —el freno de la
> firma y su cierre a mercado (ADR-0026, rama `trabajo/ftmo-y-arquitectura`)—. El "RN-030" de §2
> es un ejemplo de una propuesta descartada y **NO es esa regla**; lo mismo vale para cualquier
> otro id nuevo que se cite aquí (RN-034). Al aplicar F14b se numera desde el primer id libre.
> Mismo cuidado que A-24..A-26, que siguen reservadas para este documento (§3).

> **§0 deshecho (2026-09-16, rama `trabajo/fidelidad-de-la-spec`, ADR-0032).** Lo único que esta
> propuesta había aplicado -que RN-010 fije `operacion_abierta` y que el test exija dos productores-
> contradecía ADR-0028 §5 y ya no existe: `operacion_abierta` y `orden_limite_pendiente` declaran
> `origen: broker`, ninguna forma puede fijarlos y el test comprueba lo contrario. Es la segunda nota
> de este documento (la primera, la numeración). Dos cosas más de §3 cambiaron en esa rama: el token
> `equal` ya no existe -el resultado es `break_even`/`ganancia`/`perdida` y la forma de activarse va
> en `por`-, y las ambigüedades nuevas de esa rama se numeraron A-29 y A-30 para respetar la reserva
> de A-24..A-26.

---

## 0. Lo que SÍ se aplicó ya, y por qué solo eso

| Aplicado | Dónde |
|---|---|
| **RN-010 fija `operacion_abierta`** | una entrada activada por un `equal` no lo fijaba, así que era **invisible** para RN-002 (cierre forzoso) y RN-014 (break even). Defecto claro, arreglo aislado, sin dependencias |
| El test de hechos exige **dos** productores | encodifica la lección: toda regla que deje una posición viva lo declara |

Todo lo demás espera, y **no por prudencia genérica: por un defecto concreto del diseño** (§2).

## 1. Los tres problemas que esto tiene que resolver

1. **`liquidez_tomada` se enciende y no se apaga nunca.** RN-004 la pone en `"si"`,
   `se_da_esquema` la exige, nadie la apaga. El motor reentraría sobre la misma liquidez
   indefinidamente y de un día para otro.
2. **No existe regla que diga QUÉ nivel es la liquidez de M15.** El token `liquidez_m15` se usa
   como si estuviera dado.
3. **El token `equal` está mal definido** —dice "la operación cerró sin ganancia ni pérdida" y el
   glosario dice "dos extremos al mismo precio"— y con esa definición **RN-019 no dispara nunca**.

## 2. Por qué el diseño propuesto no se puede aplicar tal cual

El diseño propone apagar `liquidez_tomada` con cuatro reglas, una de ellas:

```yaml
  - id: RN-030   # PROPUESTA, no aplicada
    cuando:
      todos_de:
        - hecho: detenido_por_cartuchos
    entonces:
      hace:
        - fijar: {hecho: liquidez_tomada, a: "no"}
```

**Nada apaga `detenido_por_cartuchos`.** Se fija con `a: hasta_cartuchos_reinicio` y ninguna regla
lo retira. Con RN-030 dentro, la secuencia es: RN-034 marca liquidez → RN-004 la toma
(`liquidez_tomada: si`) → RN-030 la borra en el acto → `se_da_esquema` no dispara → **el bot queda
muerto tras agotar cartuchos por primera vez**.

La raíz es un patrón que el diseño no reconcilió: **los hechos DURATIVOS**. `detenido_por_tope` lo
dice en su propia descripción —*"es un HECHO que dura, no un instante"*— y se fija con un token que
codifica **cuándo expira** (`hasta_el_corte_siguiente`, `hasta_cartuchos_reinicio`). Nadie los
apaga porque el motor debe interpretar la duración. `liquidez_tomada`, en cambio, se fija con
`"si"`, sin duración.

**La pregunta de diseño que hay que contestar antes de escribir una sola regla:**

> ¿Un hecho se apaga con una regla que lo pone en `"no"`, o se declara con la duración dentro y el
> motor la interpreta? Hoy conviven las dos formas y **ninguna está documentada como la buena**.

De la respuesta dependen las seis reglas nuevas, dos hechos nuevos y la mitad del diseño. Y afecta
a lo ya escrito: si la respuesta es "durativo", `liquidez_tomada: "si"` está mal puesto desde F12 y
`detenido_por_cartuchos` no tiene ningún defecto.

## 3. Lo que el diseño aporta y hay que conservar

Aunque la mecánica esté en cuestión, esto está medido y no cambia:

- **Las tres condiciones del corpus para `liquidez_tomada`**, cada una con su cita: tras ganadora
  (`ev-v6-003227-c4efcf49`, creado en la auditoría), tras agotar cartuchos (`ev-v4-005151`), y el
  cambio de día (`ev-v4-010921`, *"de hace 2 o 3 días ese ahí no se toma"* — y esta última **no la
  sostiene el literal**: necesita ADR).
- **Tras una pérdida con cartuchos vivos NO hace falta liquidez nueva**, pero sí una zona de
  control nueva y **fuera** de la anterior (`ev-v4-003820`). Es un freno distinto y necesita su
  propio hecho: no es lo mismo "no hay liquidez" que "no se reentra todavía".
- **`equal` es geometría, no un resultado de cierre**, y solo RN-019 usaba `resultado: equal`, así
  que el colateral está acotado. Hace falta un token nuevo para el resultado que `equal` ocupaba
  por error.
- **Tres preguntas que el corpus no cierra** y que habría que abrir como ambigüedades:
  - **A-24**: con varios pivotes candidatos en M15, **¿qué hace que marque uno y no otro?**
  - **A-25**: **la vida de la marca** — ¿se mueve a un pivote más reciente mientras está viva?
  - **A-26**: el flujo es el de **M15** (cerrado) — **¿qué pasa cuando va contra el sesgo de H4?**

> **CORREGIDO el 2026-09-20** (rama de la liquidez de M15, `docs/validation/LIQUIDEZ-M15.md`). Las
> tres estaban mal enunciadas, y las tres se midieron contra los fotogramas antes de reescribirse.
> Se abren ya en `knowledge/spec/ambiguedades.yaml` con sus ids reservados; esta sección es un
> resumen, y manda el fichero.
>
> - **A-24 no era «el más reciente o el más extremo».** Ese eje no existe: `ev-v3-001531` —el que
>   sostenía el polo «más extremo»— mide lo mismo que los otros dos. En pantalla
>   (`fr-v3-982da728/944000`) el trader **descarta** el alto más alto y marca el de abajo, que es a
>   la vez el más próximo al precio y el más reciente. Y `ev-v3-001242` («el alto más alto» en un
>   *complex pullback*) está dicho sobre un **croquis a mano alzada en un gráfico de 1h**
>   (`fr-v3-982da728/781000`), donde el alto más alto **es además el último**: no discrimina. Ese
>   item lo cita ahora A-24. La pregunta pasa a ser abierta y por el **criterio**.
> - **A-25 no tenía corpus**: nada dice que un pivote nuevo invalide una liquidez **ya tomada**; la
>   premisa era del análisis. Lo abierto es si la marca **se mueve** mientras vive.
> - **A-26 tenía una mitad ya cerrada**: el flujo es el de **M15**, dicho cuatro veces
>   (`ev-v3-001204`, `ev-v4-003451`, `ev-v6-003701`, `ev-v3-011147`). Eso está **escrito en la spec**
>   desde el 2026-09-20, no solo preguntado. Lo abierto es el choque con el sesgo de H4.
> - `ev-v3-001531-1b12a896` **está supersedido** por `ev-v3-001528-87eef4f0`, que añade la cita de
>   pantalla y respeta el «suelo» y el «en este caso» de la cita original.

## 4. Cómo seguir

Esto es una funcionalidad, no un parche: 6 reglas, 2 hechos, 3 tokens, 2 parámetros, 3
ambigüedades, un ADR y `spec_version` a 11.0.0. Le toca el camino normal — brief, revisión de
diseño, rama, informe— y **empieza por contestar la pregunta de §2**, que es un ADR de método por
sí sola.

Lo que NO debe hacerse: aplicar las reglas nuevas sin resolver eso. El bot que resultaría deja de
operar para siempre la primera vez que agote cartuchos, y eso no lo caza ninguna guardia de hoy
porque todas miran la spec, no lo que el motor haría con ella.
