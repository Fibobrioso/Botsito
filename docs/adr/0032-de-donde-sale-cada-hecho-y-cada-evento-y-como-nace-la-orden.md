---
status: ACTIVE
date: 2026-09-16
phase: post-F13 (antes de F18-F24)
---

# 0032 · De dónde sale cada hecho y cada evento, y cómo nace la orden límite

## Decision

1. **Un hecho declara su `origen`: `regla` o `broker`.** Los de origen `regla` siguen como hasta
   hoy (`produce` y `consume`, comparados con las formas). Los de origen `broker` -hoy
   `operacion_abierta` y `orden_limite_pendiente`, por ADR-0028 §5- **no llevan `produce`**:
   llevan `decision` (el ADR que los deriva) y `lo_provoca`, la lista de ACCIONES cuyo efecto en el
   bróker los hace verdaderos. La guardia exige que **ninguna forma los fije** y que cada acción de
   `lo_provoca` exista y la ejecute alguna regla vigente, que es lo que sustituye a "tiene un
   productor real": sin esto, derivar del bróker dejaría a sus consumidores inalcanzables en silencio.
2. **Un predicado declara su `fuente`**: `mercado`, `reloj`, `broker`, `bot`, `motor` o
   `acumulador`. Los de fuente `broker` o `bot` llevan `lo_provoca` con la misma guardia. Es la que
   habría cazado `se_coloca_orden_limite` el día que se escribió: un evento del bot que ninguna
   acción producía.
3. **Una acción puede declarar el `efecto` que la bloquea.** `colocar_orden_limite` lleva
   `efecto: abrir_operacion`. Una acción con efecto se ejecuta solo si, **en el instante de
   ejecutarla** -con lo que las acciones anteriores de la misma regla ya escribieron-, ningún `gate`
   prohíbe ese efecto; si alguno lo prohíbe, esa acción no se ejecuta y el resto de la regla sí.
   Toda acción que aparezca en un `lo_provoca` declara su efecto: si provoca un hecho del bróker,
   un gate tiene que poder frenarla. **Esto precisa ADR-0028 §4** (punto fijo con refracción), que
   no decía cuándo se miran los gates respecto de las acciones de una misma regla.
4. **La orden límite nace en DOS reglas encadenadas por un hecho**, porque ADR-0028 §4 no ordena
   las reglas de la misma clase dentro de un evento:
   - **RN-011** (al tocar colocarla, según `orden_limite_nace`, y sin orden pendiente ni posición
     viva): dimensiona el lote, escribe el stop y fija `orden_dimensionada` con la zona.
   - **RN-015** (con `orden_dimensionada`): escribe el objetivo, coloca la orden y apaga
     `orden_dimensionada` en la misma regla.
   Entre las dos pasan los gates (RN-027 redondea el lote), y dentro de RN-015 los gates que
   prohíben abrir se miran ya con el objetivo escrito (RN-026 compara stop y objetivo con el mínimo
   del bróker). Como RN-015 apaga el hecho aunque la colocación quede prohibida, no queda ninguna
   orden a medio preparar para el día siguiente.
5. **Los valores con los que se fija un hecho y los que admite un argumento de predicado se
   declaran** (`valores`), y la guardia los compara: un `permanente` no puede acabar en
   `detenido_por_tope`, ni un `resultado` fuera de su conjunto cerrado.
6. **Las claves del vocabulario son un conjunto cerrado** por sección (predicados, acciones,
   efectos, hechos, acumuladores, tokens): un `origen` mal escrito ya no se ignora en silencio.

## Problema que resuelve

- **La spec contradecía un ADR ACTIVE.** ADR-0028 §5 deriva los dos hechos del bróker y RN-010,
  RN-011 y RN-013 los seguían fijando. Quitar los `fijar` sin más hacía fallar la guardia que exige
  productor real, que es justo el riesgo que el brief señalaba como capaz de costar la rama.
- **Nada colocaba la orden.** `se_coloca_orden_limite` era un evento que ninguna regla producía;
  leída al pie de la letra, la jornada daba `colocaciones=0` (auditoría del 2026-09-13).
- **Colocar y comprobar en la misma regla dejaba a los gates sin ventana.** RN-026 y RN-027 necesitan
  el lote y los niveles calculados ANTES de enviar. Con todo en un `hace`, la orden salía sin
  redondear y sin el veto del mínimo del bróker ([d1-interprete-05] de la misma auditoría,
  reintroducido por diseño).
- **`prohibe: [abrir_operacion]` no estaba ligado a ninguna acción.** Una acción de colocación nueva
  no habría quedado frenada por ninguno de los gates que prohíben abrir.

## Alternativas consideradas

1. **`origen: broker` + `lo_provoca`, `fuente` en predicados, `efecto` en acciones, dos reglas
   encadenadas** (elegida).
2. **`produce: [broker]`**, con `broker` declarado como productor ficticio.
3. **Una sola regla de colocación** con lote, stop, objetivo y colocar en el mismo `hace`.
4. **Tres reglas** (lote y stop, objetivo, colocar) encadenadas por dos hechos.

## Por que elegimos esta opcion

Porque cada pieza responde a un fallo medido y ninguna se apoya en el orden del fichero. `origen` +
`lo_provoca` conserva lo que la guardia de productor real protegía (que un consumidor sea
alcanzable) sin fingir un productor que no existe. `efecto` es lo mínimo que ata un `prohibe` a la
acción que frena. Y dos reglas encadenadas son lo mínimo que deja pasar los gates entre calcular y
enviar sin depender de un orden entre disparadores que ADR-0028 no da.

## Por que descartamos las demas

- **(2) `produce: [broker]`**: mezcla ids de regla con un nombre mágico en la misma lista, y la
  guardia tendría que tratarlo como excepción en cada sitio que la lee.
- **(3) Una sola regla**: es la que deja a los gates sin ventana (arriba).
- **(4) Tres reglas**: el orden entre la segunda y la tercera dentro del evento no lo fija nada, y la
  que colocara podía disparar antes de que el objetivo existiera: la posición sin objetivo que el
  brief quería eliminar, por otra vía. Y un hecho que queda encendido cuando un gate prohíbe
  colocar sobrevive al día.

## Lo que esto NO decide

- **Cuándo nace la orden.** El corpus da dos lecturas (A-29): al darse el esquema
  (`ev-v3-004201-bfeb3734`) o ya colocada tras tomar la liquidez y movida al completarse cada zona
  (`ev-v1-001358-a2b8ec0d`, `ev-v3-002511-b12d67be`, v6 1:22:14). `orden_limite_nace` corre con la
  primera como default. Con la segunda, RN-008 prohibiría la colocación antes del breaker y habría
  que reescribirla.
- **Qué pasa con una orden pendiente al llegar `ventana_fin`** (A-30). `retirar_orden_limite` queda
  declarada y ninguna regla la usa.

## Impacto

- `strategy_spec.yaml`: campos `origen`, `decision`, `lo_provoca` y `valores` en hechos; `fuente`,
  `lo_provoca` y `valores` en predicados; `efecto` en acciones; `clase` en tokens; claves cerradas.
  RN-010, RN-011 y RN-013 dejan de fijar hechos del bróker; RN-013 queda DESCARTADA (su `hace` se
  quedaba vacío: el stop único es cierto por construcción, RN-011 no lee el esquema); nacen
  `colocar_orden_limite`, `retirar_orden_limite` y `orden_dimensionada`.
- `src/botsito/spec/modelo.py`: las guardias de los puntos 1, 2, 3, 5 y 6.
- `docs/plan/features/F14b-ciclo-de-vida-de-los-hechos.md`: su §0 queda deshecho (RN-010 ya no fija
  `operacion_abierta`).
- F22-F23 implementan la semántica del punto 3 al escribir el punto fijo.

## Fecha / fase

2026-09-16, rama `trabajo/fidelidad-de-la-spec` (revisión de diseño antes de programar, dos agentes).

## Estado

ACTIVE
