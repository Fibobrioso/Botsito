# F14b · el ciclo de vida de los hechos (propuesta, NO aplicada)

**Estado:** PROPUESTA. Sale de la auditoría del 2026-09-12
(`docs/validation/AUDITORIA-2026-09-12-material.md` §2) y de un diseño encargado a un agente el
mismo día. **No se ha aplicado nada de este documento**, salvo lo que se dice en §0.

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
  - **A-24**: con varios pivotes candidatos en M15, ¿la liquidez es **el más reciente**
    (`ev-v1-001334`, `ev-v4-010921`) o **el más extremo** (`ev-v3-001531`)? No son el mismo nivel.
  - **A-25**: con la liquidez ya tomada y cartuchos vivos, ¿un pivote más reciente la invalida?
  - **A-26**: la vela que marca la liquidez es "contraria al flujo" — ¿ese flujo es el **sesgo de
    H4**, o se lee en M15 y puede ir contra el sesgo?

## 4. Cómo seguir

Esto es una funcionalidad, no un parche: 6 reglas, 2 hechos, 3 tokens, 2 parámetros, 3
ambigüedades, un ADR y `spec_version` a 11.0.0. Le toca el camino normal — brief, revisión de
diseño, rama, informe— y **empieza por contestar la pregunta de §2**, que es un ADR de método por
sí sola.

Lo que NO debe hacerse: aplicar las reglas nuevas sin resolver eso. El bot que resultaría deja de
operar para siempre la primera vez que agote cartuchos, y eso no lo caza ninguna guardia de hoy
porque todas miran la spec, no lo que el motor haría con ella.
