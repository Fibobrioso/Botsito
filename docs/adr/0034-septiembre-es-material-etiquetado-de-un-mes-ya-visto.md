---
status: ACTIVE
date: 2026-09-20
phase: post-F13 (entrada del backtest de septiembre)
---

# 0034 · Septiembre es material ETIQUETADO de un mes que el trader ya ha visto

## Decision

1. **El backtest de septiembre 2026 es material ETIQUETADO de un mes que el trader YA HA VISTO.**
   Lo backtesteó él, así que sus días no son ciegos para él. Entra en
   `knowledge/cases/kit/vistos.yaml` como cualquier otro mes visto, con su `visto_el`.
2. **(a) NO es material ciego para una sesión en vivo.** No se puede usar para pedirle al trader que
   etiquete a ciegas: ya conoce esos días. Cualquier paquete de sesión que lo sortee está mal
   construido por definición, y el mecanismo lo impide solo: con septiembre en `vistos.yaml`,
   `construir()` lo quita del universo de toda sesión posterior a su `visto_el` (ADR-0011,
   `docs/validation/MESES-VISTOS.md`).
3. **(b) SÍ sirve para medir FIDELIDAD**, que es otra cosa: comparar lo que el bot decide contra lo
   que el trader decidió, sobre días que él ya etiquetó. Para eso vale, **con una condición
   innegociable: las particiones se fijan y se commitean ANTES de leer ninguna etiqueta de
   septiembre**, y esa anterioridad tiene que quedar probada por el historial de git, no por una
   declaración. Es la misma prueba que sostiene el reparto de mayo (ADR-0025).
4. **Que septiembre haya llegado NO cierra la petición del mes limpio** (ADR-0021 §7, ADR-0025
   punto 5, obligación 5 de `docs/validation/HOLDOUT-EXPOSICIONES.md`). Sigue pendiente pedirle al
   trader un mes que no haya tocado. Son dos cosas distintas y la confusión es la lectura fácil.
5. **Este ADR es el id citable** para el trailer `Fuente:` de los commits que toquen
   `knowledge/cases/` por causa de septiembre (`ADR-0034`), mientras no exista un `fb-*` del trader
   que fije la fecha real de su backtest.
6. **Lo que este ADR NO decide**: cómo se sortean esas particiones. El camino del kit (`kit build`)
   es el del etiquetado ciego y, por construcción, no sirve aquí; además hoy está bloqueado por dos
   motivos medidos (`docs/validation/SEPTIEMBRE-ENTRA.md` §4): los cupos de `config.yaml` suman 40 y
   septiembre tiene 14 días laborables, y descargar sus velas rompería la reproducción del paquete
   de la sesión 1. Eso se resuelve en su propia rama, con el universo congelado en el paquete.

## Problema que resuelve

El 2026-09-20 el trader entregó su backtest de septiembre (seis capturas y un xlsx). Hasta ese día
el proyecto solo conocía dos clases de material: **ciego** (mayo: etiquetado por el trader sin haber
visto nuestro reparto, y por eso reservable como holdout) y **visto sin etiquetas** (enero, abril,
julio, agosto: meses que el trader recorrió en vídeo, excluidos del universo por `vistos.yaml`).

Septiembre no es ninguna de las dos: **está visto Y viene con etiquetas**. Sin decidir qué es, las
dos lecturas equivocadas estaban servidas: tratarlo como material de sesión —y pedirle al trader que
etiquete a ciegas lo que ya backtesteó— o descartarlo entero por visto, perdiendo el único material
etiquetado nuevo que ha entrado desde mayo. Y F26, que mide fidelidad, no tenía dónde leer cuál de
las dos cosas es.

## Alternativas consideradas

1. **ADR propio que defina la clase de material** (elegida).
2. **Nota en ADR-0021 o en ADR-0025.** ADR-0021 decide qué cuenta como abrir un holdout; ADR-0025,
   que el reparto de mayo no se toca. Ninguno decide sobre clases de material.
3. **No escribir nada y resolverlo en el brief del paquete de septiembre.**
4. **Declarar septiembre como holdout sin más**, igual que mayo.

## Por que elegimos esta opcion

- **Es una decisión nueva, no la aclaración de una existente.** La categoría «mes ya visto **con**
  etiquetas» no existía en el proyecto. En este repositorio las notas dentro de un ADR se usan para
  registrar que otro ADR dio mecanismo a lo ya decidido, nunca para introducir regla nueva.
- **Reparte obligaciones entre piezas que hoy no se hablan**: F26 (que mide fidelidad), la sesión 2
  (que no debe sortear septiembre), `vistos.yaml` y `HOLDOUT-EXPOSICIONES.md`.
- **Hace falta un id citable.** Todo commit que toque `knowledge/cases/` lleva trailer `Fuente:` con
  ids que existan —`ev-*`, `fb-*` o `ADR-NNNN`—, y declarar septiembre en `vistos.yaml` es
  exactamente uno de esos commits. Una nota no es citable; un ADR sí.

## Por que descartamos las demas

- **(2) La nota** habría metido una regla nueva dentro de una decisión sobre otra cosa, y habría
  dejado el commit de `vistos.yaml` sin `Fuente:` válida.
- **(3) Dejarlo al brief** es lo que ya falló con `se_coloca_orden_limite` y con la definición de
  breaker: lo que no se escribe donde toca se vuelve a discutir dentro de un mes, y en medio se
  toman decisiones que lo dan por resuelto en un sentido u otro.
- **(4) Tratarlo como mayo** es falso y peligroso: mayo era ciego cuando se etiquetó, y por eso su
  holdout mide algo. Septiembre no lo es: una cifra de fidelidad sobre días que el trader ya había
  visto **cuando los etiquetó** mide otra cosa, y llamarla «holdout» sería vender por ciego lo que
  no lo es. Sirve para fidelidad, no para sustituir al mes limpio.

## Impacto

- `knowledge/cases/kit/vistos.yaml`: septiembre declarado con `visto_el: 2026-09-20`.
- **F26**: cuando mida sobre septiembre, cita este ADR y la fila del 2026-09-20 de
  `HOLDOUT-EXPOSICIONES.md`, y **excluye los días sin operaciones** del 1 al 18 (obligación 7 de esa
  tabla), que no se pueden nombrar sin abrir el fichero.
- **La sesión 2 no sortea septiembre**: el mecanismo de `vistos.yaml` ya lo impide, y esto lo
  explica.
- **Pendiente y con dueño en el tiempo, no «algún día»**: la guardia de ancestro empareja las
  etiquetas por el campo `sesion` del registro y nunca por el caso, así que una etiqueta sobre un
  caso de septiembre podría registrarse contra particiones commiteadas después.
  **Se arregla ANTES DE LA PRIMERA ETIQUETA de septiembre**, que es la línea roja: hoy no existe ni
  un `LABEL_CASE` en el repositorio y la guardia no puede fallar; en cuanto exista uno, ya es tarde.
- **No cierra** la petición del mes limpio (punto 4 de la decisión).

## Fecha / fase

2026-09-20, post-F13, rama `trabajo/septiembre-entra`. Informe:
`docs/validation/SEPTIEMBRE-ENTRA.md`.

## Estado

ACTIVE
