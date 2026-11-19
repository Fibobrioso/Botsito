---
status: ACTIVE
date: 2026-11-19
phase: post-F14 (rama `trabajo/preregistro`, R5.1 de la hoja de ruta; la G de la Next Action)
---

# 0096 · El pre-registro: la rentabilidad, fijada; F26, diagnóstico sobre el mes limpio

> Decisiones del consultor del 2026-11-19 (respuesta a la PARADA de la fase 0 de
> `trabajo/preregistro`, copiada tal cual en `docs/encargos/trabajo-preregistro.md` y en
> `docs/validation/PREREGISTRO-INVENTARIO.md`). Rellena `docs/validation/PREREGISTRO.md`.
> **No enmienda ADR-0021** (nada de esto lo contradice) **ni cambia ninguna cifra** de ADR-0043,
> ADR-0070, ADR-0092 o `knowledge/cases/criterio_fidelidad.yaml`. Recuadros en ADR-0092 §5 y §13.

## Decision

**0. El umbral de F26: la referencia de ADR-0043, sin ninguna cifra nueva, y F26 es
diagnóstico.** F26 no bloquea nada y se informa en el memorando (ADR-0092 §7). Su referencia son las
cifras de ADR-0043 -cobertura ≥ 0,70 y precisión ≥ 0,60- con su misma unidad (la operación),
emparejamiento y tolerancias (`criterio_fidelidad.yaml`: `umbral_cobertura`, `umbral_precision`,
`tolerancia_entrada_puntos`, `tolerancia_instante_min`). Vale lo escrito sobre su potencia (ADR-0036
§8; `src/botsito/cases/fidelidad.py:18-24`): por debajo de 36 unidades efectivas independientes lo
que sale es una cifra DESCRIPTIVA con su intervalo, y nadie la cita como si midiera. El informe de
F26 da N del trader, N del bot en días con operaciones del trader, las dos cifras, su intervalo y
cuántas unidades efectivas hay; solo con 36 o más escribe «llega» o «no llega» contra la referencia;
con menos, «descriptiva». Cómo se cuentan las unidades efectivas sobre operaciones y qué intervalo
se usa lo fija, leyendo `docs/validation/AUDITORIA-2026-09-13-ultracode.md` §6.1 y antes de medir
nada, el ADR de la rama que construya el comando de medida; este ADR no lo inventa. La cascada por
criterios (ADR-0092 §2) se informa al lado, sin umbral. El objetivo, el resultado y la gestión siguen
fuera (ADR-0043), así que A-56 no puntúa. A-16 sigue ABIERTA con la regla de ADR-0092 §9, que con la
medida de R3.7 no se dispara.

**1. Sobre qué se mide F26: sobre el mes limpio.** F26 se mide sobre febrero de 2026 cuando el
trader lo entregue grabado en vídeo y con voz (S-14), que entra reservado entero por su propia rama,
con su ADR y su partición. `holdout-1` sigue intacta y reservada para la nota de F26 (ADR-0021 §6) y
**no se abre mientras el mes limpio esté pendiente**; abrirla sin él exige un ADR que lo diga.
- **Cuándo:** no antes de que mayo `dev` esté medido (R5.2). Es el orden de la hoja de ruta (R5.5),
  no una regla de un ADR, y se dice así. Una sola vez, con la spec de esa corrida y **una cuenta para
  el mes**: la condición que ADR-0092 §8 pone a la construcción y a mayo, que este ADR extiende a la
  medida de F26.
- **`fidelidad-1`** (septiembre) no es ciega (ADR-0034) y no se usa para F26: queda sin uso asignado.
  Es lo que cambia respecto de `docs/validation/PUERTA-POR-PREGUNTA.md` §10, que preveía
  `fidelidad-1` como primera autorización; ese informe está cerrado y no se toca: lo dice este ADR.

**2. Cuántos días, y cómo se cuentan.** Hacen falta los que den 36 unidades efectivas: en la
práctica, un mes entero con vídeo. Se escribe así, con la densidad de construcción como fuente
(`PREREGISTRO-INVENTARIO.md` §0.4) y sin prometer un número de días.
- **El conjunto medido**, cuando exista, son los días de la partición que caen dentro de un TRAMO de
  `cobertura_material` de su camino (el criterio es el tramo, no el mes: un mes declarado con cero
  tramos no aporta ninguno); los demás quedan fuera POR ESCRITO, y no como días sin operación.
- Los dos días del universo de la sesión 1 que no están en ninguna partición (ADR-0035, «Impacto»)
  no entran en ningún conjunto medido, y toda cifra dice sobre qué conjunto se da.
- **El día quemado de `holdout-2`** (`docs/validation/HOLDOUT-EXPOSICIONES.md`, «Lo que esto obliga»,
  punto 4) **no entra ahora en `retirados.yaml`**: queda excluido por escrito en `PREREGISTRO.md`, y
  la rama que dé uso a `holdout-2` lo retira antes (ADR-0041).

**3. Otro mes al trader: febrero de 2026, con vídeo y con voz**, el que `meses_reservados.yaml` tiene
reservado entero como el mes limpio pedido. El mensaje lo redacta el consultor para Aleks; el
pre-registro lo deja escrito.

**4. «Una pregunta abre N particiones»** (ADR-0033, enmienda del 2026-09-21, «Lo que NO cierra»): la
rama que construya el comando de medida de F26 lo hace nacer abriendo UNA sola partición, y el
arreglo de `kappa_entre_sesiones` es una rama corta aparte, antes de cualquier autorización de
kappa. Esta rama no toca `src/`. Consecuencia aceptada: R5.1 no queda «hecha» con este ADR; queda con
el pre-registro relleno y lo de la puerta pendiente con dueño.

**5. Qué lleva `PREREGISTRO.md`.** Sale la marca de vacío (`holdout.MARCA_SIN_RELLENAR`), de todo el
fichero. Entran:
- la rentabilidad entera, copiada de ADR-0092 y del bloque `rentabilidad` de
  `criterio_fidelidad.yaml` sin cambiar una cifra;
- la parte de F26 con las decisiones 0 a 3 y 6, y sus límites conocidos (la potencia; el sesgo de
  los libros sin vídeo, S-14);
- quién autoriza: Aleks (ADR-0021 §3); el consultor decide el contenido y la sesión ejecuta
  (ADR-0072);
- las exposiciones POR REFERENCIA: el fichero, la fecha de cada fila y el recuento por partición
  del anexo de la rama, sin copiar el contenido de ninguna fila;
- **ninguna línea de pregunta**, tampoco como ejemplo, porque la puerta la leería como viva
  (`holdout._PREGUNTA`): la primera la añade, ABIERTA y con su partición escrita, la rama del
  comando de medida.

**El hash de la spec no se escribe ahora; se fija el procedimiento** (ADR-0092 §5, que lo ponía en
G). En la rama de la medida de rentabilidad, antes de correr y antes de que exista ninguna
autorización de holdout, se escriben en `PREREGISTRO.md`:
- el sha del commit desde el que se corre;
- en ese commit (`git rev-parse <commit>:<ruta>`), el id de blob de
  `knowledge/spec/strategy_spec.yaml`, `knowledge/spec/parametros.yaml`,
  `knowledge/cuentas/ftmo-2step-swing-100k.yaml` y `knowledge/simulador/llenado.yaml` (los cuatro
  de ADR-0092 §5);
- el id del árbol de `knowledge/cuentas` (cubre también el calendario de cierres,
  `knowledge/cuentas/cierres/`, que §5 no nombra y la corrida lee) y el del árbol de `src`.

Son bytes commiteados, no el hash canónico de `botsito spec manifest` (`spec/manifiesto.hash_de`,
que cubre `parametros.yaml`, `strategy_spec.yaml` y `glossary.yaml`), y no hace falta código nuevo.
Escribirlo antes de cualquier autorización evita que el cambio de blob la invalide
(`holdout.motivos_de_cierre`, `preregistro_blob`).

**6. Si F26 no llega:** un diagnóstico se informa y no se repite. `holdout-2` y `holdout-3` siguen
cerradas; el «si hace falta corregir y volver a medir» de ADR-0021 §6 es condicional y aquí no hace
falta, así que no se enmienda.

**7. Kappa, paridad y DSR** (`MASTER_PLAN.md` §H): cada uno se pre-registra en la rama de su
funcionalidad, antes de su primera medida: kappa, la sesión que etiquete; paridad, F30 y F32; DSR,
F27.

**8. Número:** este ADR es el 0096. El 0095 quedó declarado inexistente por
`trabajo/laminas-sesion-7b` en dos documentos, uno de ellos un informe cerrado, y se salta como se
saltó el 0087.

## Problema que resuelve

`PREREGISTRO.md` estaba vacío desde el 2026-09-12, y la G de la Next Action pedía rellenarlo con lo
de ADR-0092 §13. La fase 0 midió que el encargo daba por pre-registradas para F26 unas cifras que no
lo están: ADR-0043:55-56 llama a 0,70 y 0,60 umbral de DESARROLLO sobre los días `dev` de mayo, «NO
el PREREGISTRO del holdout», y ADR-0092 §7 dejó F26 como diagnóstico. Y midió lo que hay para medir:
`holdout-1` tiene unos 6 días de mayo con material, de un libro sin vídeo; a la densidad de
construcción (de 1,67 a 5,15 operaciones del trader por día según el mes) son entre unas 10 y unas 30
operaciones, por debajo de cualquier potencia. Abrirla sería gastar la única partición ciega en una
cifra que ya se sabe descriptiva.

## Alternativas consideradas

Las opciones que la PARADA puso y no se eligieron (`PREREGISTRO-INVENTARIO.md`, «Lo que necesito que
decidas»):
- 0(b): F26 sin referencia, solo descriptiva, enmendando ADR-0021 §3; 0(c): un umbral propio de F26.
- 1(a): **medir F26 sobre `holdout-1` ya**; 1(b): sobre `fidelidad-1`.
- 2(b): tomar los recuentos de mayo (6/4/3) de `PREREGISTRO.md` tal cual, sin medir; 2(c): juntar
  particiones en una medida; retirar ahora el día quemado de `holdout-2`.
- 3(b): contar solo con marzo y febrero; 3(c): no pedir otro mes.
- 4(b): arreglar «una pregunta abre N» en esta rama; 4(c): no hacer nada hasta la primera
  autorización.
- 5(b): dejar la marca hasta que F26 tenga comando; 5(c): dos ficheros de pre-registro; escribir hoy
  el hash de la spec.
- 6(a): corregir y volver a medir en `holdout-2`; 6(c): repetir solo con un mes nuevo.
- 7(b): fijar kappa, paridad y DSR en esta rama.
- 8(b): usar el 0095.

## Por que elegimos esta opcion

- Ninguna cifra nueva: la referencia de F26 es la de ADR-0043, y la rentabilidad se copia.
- Cumple ADR-0021 §3 (umbral pre-registrado antes de abrir) sin contradecir ADR-0092 §7 (F26 es
  diagnóstico), y la regla de las 36 unidades impide leer una cifra sin potencia como si midiera.
- Guarda la única partición ciega hasta que haya material con potencia y sin el sesgo de S-14.
- Deja la puerta cerrada por dos barreras que no dependen de la marca: ninguna pregunta y ninguna
  autorización; y ordena el hash antes de cualquier autorización.

## Por que descartamos las demas

- **Medir F26 sobre `holdout-1` ya** (1a): de 10 a 30 operaciones, un libro sin vídeo y la única
  partición ciega gastada en una cifra descriptiva.
- **`fidelidad-1`** (1b): septiembre no es ciego, y el trader dio su sesgo en directo sobre velas de
  esos días (`SESGO-H4-COLOR.md` «Para F26»).
- **Sin referencia** (0b): obligaba a enmendar ADR-0021 §3. **Un umbral propio** (0c): una cifra
  nueva elegida con las corridas de construcción a la vista.
- **Recuentos sin medir** (2b): no ven el retirado de `holdout-3` ni el criterio del tramo.
  **Juntar particiones** (2c): gasta dos oportunidades a la vez. **Retirar ya el quemado**: pide la
  huella de su id y cambia un test, y `holdout-2` no tiene uso asignado.
- **No pedir otro mes** (3b, 3c): todo lo reservado que existe es sin vídeo.
- **Arreglar la puerta aquí** (4b): convierte una rama de documentos en rama de código de la puerta;
  **no hacer nada** (4c): R5.1 no podría darse por hecha nunca.
- **La marca hasta el comando** (5b): cada edición siguiente choca con `test_puerta_holdout`; **dos
  ficheros** (5c): enmendar ADR-0092 §13; **el hash hoy**: caduca con la activación de la 7b.
- **Volver a medir en `holdout-2`** (6a): gasta una partición en una cifra que no decide nada.
- **Kappa, paridad y DSR aquí** (7b): tres cifras sin medida que las sostenga.
- **El 0095** (8b): editar un informe cerrado.

## Lo visto, declarado (ADR-0070 punto 4)

Lo que el consultor tenía delante al decidir, todo de construcción o recuentos sin claves:
- la última re-corrida que cuenta: `habilita medir … : no (cobertura 15.7 % …; precision 13.9 % …)`
  (`RECORRIDA-CONSTRUCCION-2.md:420`; `anexos/RECORRIDA-CONSTRUCCION-2/cuenta-por-mes.txt`);
- julio, en el pivote de ADR-0093 §6: parejas y operaciones del bot de más, 14 y 39 en la línea base,
  14 y 24 tras la primera activación de la 7a y 11 y 19 tras la segunda (`ACTIVAR-SESION-07.md:87` y
  `:790-791`);
- la densidad de construcción por día y por mes (`PREREGISTRO-INVENTARIO.md` §0.4,
  `anexos/PREREGISTRO-INVENTARIO/densidad-construccion.txt`);
- los recuentos por partición, sin claves (`PREREGISTRO-INVENTARIO.md` §0.3,
  `anexos/PREREGISTRO-INVENTARIO/recuento-particiones.txt`).
Ninguna salida del motor sobre la medida ni sobre lo reservado: mayo no se ha visto (ADR-0092 §12).

## Impacto

- `docs/validation/PREREGISTRO.md`, relleno; `tests/unit/test_puerta_holdout.py`: el test que
  exigía la marca se sustituye por uno que no depende de ella ni del estado de git (en el mismo
  commit).
- Recuadros en ADR-0092 §5 y §13: el hash lo escribe la rama de la medida, con el procedimiento de
  la decisión 5.
- `docs/plan/MASTER_PLAN.md`: una NOTA de cabecera (pre-registro, F26 diagnóstico sobre el mes
  limpio, kappa, paridad y DSR en su rama); ninguna fila cambia.
- Pendiente con dueño (líneas para el cierre): el comando de medida de F26, que abre una sola
  partición; el arreglo de `kappa_entre_sesiones`; el fallback de `leer_fichero`; la declaración del
  libro de septiembre; la retirada del día quemado de `holdout-2`; pedir febrero con vídeo.
- `docs/validation/PUERTA-POR-PREGUNTA.md` y ADR-0021 no se tocan.

## Fecha / fase

2026-11-19, post-F14, rama `trabajo/preregistro` (R5.1).

## Estado

ACTIVE
