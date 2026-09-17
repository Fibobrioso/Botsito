---
status: ACTIVE
date: 2026-09-16
phase: post-F13 (antes de F18-F24)
---

# 0031 · El freno de la firma dispara antes del límite: margen declarado y lectura prospectiva

## Decision

1. **Nace `firma_margen_seguridad`** (`prop_firm`, porcentaje del capital inicial
   `saldo_inicial_cuenta`, fuente este ADR). Los dos límites de la firma se vigilan en
   `firma_perdida_diaria_max − firma_margen_seguridad` y en `firma_perdida_total_max −
   firma_margen_seguridad`, no en el límite. **Valor: 0,5**, a validar por el consultor (ver
   «Lo que queda abierto»).
2. **El margen se aplica a las tres reglas de la firma**: RN-029 (detiene por el día), RN-031
   (detiene para siempre por el total, nace en esta rama) y RN-030 (cierra a mercado la posición
   viva). Las tres leen el acumulador sobre equity (`firma_magnitud_vigilada`).
3. **Lectura prospectiva, en una regla aparte (RN-032)**: no se abre una operación si la pérdida
   acumulada de la firma MÁS el riesgo de esa operación (`riesgo_por_operacion` sobre
   `base_calculo_riesgo`) llega al límite menos el margen. Vale para el límite diario y para el
   total. Solo prohíbe: no fija ninguna detención, porque la cuenta puede recuperar holgura en el
   mismo día (una ganadora sube el equity).
4. **El tope del trader (RN-020) NO cambia de lectura.** Sigue diciendo lo que el trader dijo:
   se deja de operar al alcanzar `perdida_maxima_diaria`. Su desbordamiento por construcción
   queda declarado en sus notas, y lo que impide que ese desbordamiento cueste la cuenta es este
   ADR, no un cambio en la regla del trader.

## Problema que resuelve

Dos defectos distintos, que la revisión de diseño de la rama de fidelidad (2026-09-16) separó:

- **Llegar al límite de la firma ES la infracción.** RN-029 y RN-030 disparaban *al alcanzarlo*:
  no evitaban perder la cuenta, solo impedían seguir operando después. Con equity vigilado tick a
  tick, un cierre a mercado que se ejecuta en el límite se ejecuta con el límite ya roto.
- **Los topes se rebasan por construcción.** `alcanza_tope` se comprueba antes de abrir sin descontar
  el riesgo de la operación que se abre. Medido en la auditoría del 2026-09-13 (`s05a`,
  [d1-interprete-04], el único hallazgo de su dimensión que el escéptico confirmó sin matizar): el
  tope del trader del 4,5 % acaba en 4,865 %. Con la aritmética en el borde, el peor caso de cada
  tope con la lectura vigente es tope + un riesgo: 4,9775 % (trader, saldo del día 100.000), 5,475 %
  (firma diaria) y 10,45 % (firma total).

## Alternativas consideradas

1. **Margen y lectura prospectiva, las dos** (elegida).
2. **Solo lectura prospectiva.**
3. **Solo margen.**
4. **Dejarlo a F21-F24** y que el motor decida.

## Por que elegimos esta opcion

Porque **arreglan cosas distintas** y ninguna cubre lo de la otra:

| | Desbordamiento por construcción (abrir con el tope casi lleno) | Deslizamiento, gap, costes, equity flotante antes de que el cierre se ejecute |
|---|---|---|
| Prospectiva | **lo cierra** para el riesgo nominal | no |
| Margen | lo cierra solo si el margen ≥ un riesgo, y a cambio de operar menos siempre | **deja colchón** del tamaño del margen |

Con las dos, la última operación que se abre cabe entera por debajo de `límite − margen`, y el margen
queda libre para lo que la prospectiva no puede ver: que el stop salte más allá de su nivel, las
comisiones, o que el equity cruce el umbral y RN-030 cierre a mercado con deslizamiento.

## Por que descartamos las demas

- **(2) Solo prospectiva**: protege la contabilidad de los cierres, no el equity. Con una posición
  viva el equity se mueve tick a tick y un cierre a mercado en el propio límite se ejecuta con el
  límite roto.
- **(3) Solo margen**: para cubrir el desbordamiento tendría que ser de al menos un riesgo, y ese
  riesgo se sumaría al del deslizamiento; cuesta el doble de capacidad para la misma protección.
- **(4) Dejarlo al motor**: es exactamente lo que ADR-0002 prohíbe. Una cifra que decide cuándo se
  deja de operar vive en el registro, y una lectura del tope que cambia lo que el bot hace vive en
  la spec, con su guardia.

## Lo que queda abierto, y conviene no creer que está cerrado

- **El valor 0,5 es una decisión del consultor pendiente de validar**, no un dato medido. Lo que
  implica: con el margen y la prospectiva, en un día que empieza con 100.000 o más, la décima
  pérdida seguida del día ya no se abre: tras nueve, `s05a` mide 4.388,99 de pérdida, y sumando el
  riesgo de la décima (0,5 % de 95.611,01 = 478,06) da 4.867,05, por encima de 4.500. Con el tope del
  trader solo, se abría y acababa en ~4,87 %. Es un día de nueve pérdidas; con tres cartuchos por
  zona hacen falta al menos tres zonas perdidas enteras. Con 0,25 pasaría lo mismo (4.867,05 >
  4.750); la décima solo se abriría con un margen por debajo de 0,13. Mientras la pérdida del día
  más el riesgo de la operación siguiente quede por debajo de 4.500 -en la práctica, una pérdida
  acumulada por debajo de ~4.000-, el margen no cambia nada.
- **Ningún control discreto cubre un gap mayor que el margen.** Si el precio salta el stop y el
  umbral de un tick al siguiente, el cierre se ejecuta donde se ejecute. Es un riesgo declarado.
- **El margen de la firma y el tope del trader no se suman ni se comparan**: son frenos distintos
  sobre bases distintas (capital inicial frente a saldo inicial del día). Manda siempre el primero
  que dispara.

## Impacto

- `parametros.yaml`: `firma_margen_seguridad`.
- `strategy_spec.yaml`: predicados `se_acerca_al_limite` y `no_cabe_la_operacion` (fuente
  acumulador); RN-029 se queda con el límite diario; RN-031 y RN-032 nacen; RN-030 lee los dos
  límites con margen y pasa a `terminal` (la clase, por ADR-0018, es otra decisión de la misma rama).
- `spec_version` 12.0.0 (un solo bump con el resto de la rama).
- F21-F24 implementan las dos primitivas de acumulador sobre equity (ADR-0028, fase de riesgo por
  tick).

## Fecha / fase

2026-09-16, rama `trabajo/fidelidad-de-la-spec` (revisión de diseño antes de programar).

## Estado

ACTIVE
