# FUNCTIONALITY VALIDATION REPORT · Cerrar A-29 y A-36

Rama `trabajo/cerrar-a29-a36`, abierta el 2026-10-02 desde `main` `487c64f` (tag
`stable/F36n-escenarios-por-sesion`). Encargo, copiado tal cual:
`docs/encargos/trabajo-cerrar-a29-a36.md`. Tarea autónoma: NO se cierra.

Cierra dos ambigüedades que ya tenían respuesta grabada del trader en la sesión 3 (v9) y seguían
ABIERTAS (`docs/sesion-4/PREGUNTAS.md` §4). Sin cobertura agregada: nada de esta rama cuenta
parejas ni compara con las operaciones del trader.

## 1. Antes de tocar nada: los dos tramos, por la vía autorizada (punto 1)

**Tramos no citables.** `knowledge/corpus/tramos_no_citables.yaml` tiene trece tramos de v9. Los
más cercanos son 0:22:11-0:22:16 (para 0:01:43) y 1:13:04-1:14:16 y 1:39:43-1:44:28 (para
1:17:14). Ninguno toca 0:01:43-0:01:52 ni 1:17:14-1:17:21.

**La cuarentena de v9.** v9 está entera en `SESIONES_EN_CUARENTENA`
(`src/botsito/corpus/cuarentena.py`): su transcripción cruda no la lee nadie. La guardia de
Claude Code bloqueó `botsito kb at --video v9 --t 0:01:43` («imprime la transcripcion cruda») y
**no se rodeó**. La evidencia tiene su propio criterio: `kb` solo oculta el ítem cuya cita cae en un
tramo no citable, lo copia o trae un día reservado. Con `kb find --frase --solo evidencia`, que
filtra por defecto:
- `ev-v9-000143-214aacde` (0:01:43-0:01:52) y `ev-v9-011714-08536830` (1:17:14-1:17:21) salen, no
  ocultos;
- el aviso «OCULTOS: 1 items de evidencia: 1 por tramo no citable (b)» sale igual con una búsqueda
  sin resultados (`"zzqx inexistente"`): es un ítem de otro sitio, no uno de estos dos.

**La cita literal sale de la verificación de citas, no de memoria ni de `PREGUNTAS.md`.** Script
de solo lectura en la carpeta de trabajo, que llama a `evidence.modelo.verificar_citas` -la vía
autorizada que usa `knowledge validate` para leer la cruda- SOLO con esos dos ítems, e imprime
tiempos y recuentos, ningún texto de la cruda:

| Ítem | Tramo del ítem | Localizada en la cruda activa | Segmentos | Problemas | Avisos |
|---|---|---|---|---|---|
| `ev-v9-000143-214aacde` | 0:01:43-0:01:52 | 0:01:43,5-0:01:50,3 | 2 | 0 | 0 |
| `ev-v9-011714-08536830` | 1:17:14-1:17:21 | 1:17:15,2-1:17:20,9 | 3 | 0 | 0 |

Las dos citan `tr-v9-large-v3-int8-float16-dcd6e5bd`, la transcripción activa de v9. Los literales de
los registros de feedback son los `cita_literal` de esos dos ítems; para A-36, la respuesta dentro
de la cita.

**Lo que no se pudo comprobar, y se dice:**
- Que la pregunta de v9 0:01:30 «ofrecía las tres lecturas» lo dicen `PREGUNTAS.md` §2 y la
  extracción de la sesión 3, que leyó la versión filtrada antes de que la CLI la ocultara. Hoy no
  hay vía autorizada para leer esa pregunta, y no se leyó.
- Los dos ítems tienen confianza media: la cruda no separa voces y el hablante se atribuye por
  contexto (`revisado_por` de cada ítem).
- `PREGUNTAS.md` daba para A-36 el tramo 1:17:14-1:17:18; el del ítem verificado es
  1:17:14-1:17:21, y es el que llevan el registro y `PREGUNTAS.md` ahora.

Ningún tramo cae en uno protegido: la rama siguió.

## 2. El cierre, por `docs/runbooks/AMBIGUEDADES.md` (punto 2)

**Tres registros de feedback** en `knowledge/feedback/2026-09-29-sesion-03/`, todos
`RESOLVE_UNKNOWN`, `trader_grabado`, `recibido_el` 2026-09-29, con la grabación de la sesión 3 y su
tramo:

| Registro | Objetivo | Tramo | Literal | Valor |
|---|---|---|---|---|
| `fb-2026-09-29-sesion-03-b41ecf9b` | ambigüedad A-29 | 0:01:43-0:01:52 | «Lo primero es que primero se desarrolla una toma de liquidez Para recién nosotros poder trazar los posibles puntos de breaker» | `al_aparecer_punto_de_breaker` |
| `fb-2026-09-29-sesion-03-755c534e` | parámetro `orden_limite_nace` | el mismo | el mismo | `al_aparecer_punto_de_breaker` (canónico) |
| `fb-2026-09-29-sesion-03-626c4dc7` | ambigüedad A-36 | 1:17:14-1:17:21 | «Mecha incluida, siempre.» | en el extremo del bloque, mecha incluida |

**A-29 lleva DOS registros, no uno.** El encargo dice «un FeedbackRecord por respuesta», y la
mecánica pide dos cuando la ambigüedad tiene parámetro. `knowledge validate` solo da por RESUELTA una
ambigüedad con un registro cuyo objetivo es la AMBIGÜEDAD (ADR-0022), y `feedback apply` solo lleva
al registro uno cuyo objetivo es el PARÁMETRO. Es lo que se hizo con A-47 en la sesión 3
(`…-92a38105` y `…-8f091ed8`). A-36 no tiene parámetro: lleva uno.

**Los cuatro sitios:**
1. **El registro de parámetros.** `feedback apply --sesion 2026-09-29-sesion-03 --check` primero:
   «4 parametros; 1 cambian, 3 ya estaban». El único que cambia es `orden_limite_nace`, que pasa
   de DEFAULT_AMBIGUOUS (A-29, fuente `ev-v7-001457-1fe7fdfe`) a CONFIRMED (fuente
   `fb-…-755c534e`), con el MISMO valor. Su descripción decía «Sigue DEFAULT_AMBIGUOUS: A-29 no se
   resuelve»: ahora dice que se resolvió, con la cita.
2. **`knowledge/spec/ambiguedades.yaml`.** A-29 y A-36 pasan a RESUELTA. Su `pregunta` lleva al
   final la respuesta con su registro, como A-37, y su `evidencia` suma el ítem de v9.
3. **La regla de la spec que la cita.** A-29 la nombraban cuatro sitios de
   `strategy_spec.yaml`: el predicado `toca_colocar_orden_limite` (un comentario), las notas de
   RN-010 y RN-011, y las de RN-019 (la reentrada). Los cuatro dicen ahora que está RESUELTA en
   `al_aparecer_punto_de_breaker`, con el registro. **A A-36 no la cita ninguna regla**: ni
   `strategy_spec.yaml`, ni `parametros.yaml`, ni `glossary.yaml`. Ese sitio no tiene nada que
   cambiar.
4. **La tabla «Known Ambiguities» de `PROJECT_STATE.md`.** Salen las filas de A-29 y A-36.

Además:
- `tests/unit/test_kit.py` congela las RESUELTAS, y suma A-29 y A-36 con una línea de por qué;
- `botsito spec docs --escribir` regenera los cuatro de `docs/spec/`, y la spec pasa de 15.5.1 a
  15.6.0;
- `spec check`, `knowledge validate` (147 registros de feedback, 53 ambigüedades) y `state check`
  pasan. `feedback pending`: 0 pendientes.

**Un sitio más que el runbook no nombra: la hoja de preguntas.** El primer `make check` salió en
rojo, con 3 fallos:
- `scripts/hoja_preguntas.py` se niega a llevar al trader una ambigüedad que ya no está ABIERTA
  («ya no se preguntan (estan RESUELTA): A-36, A-29»), y su test copia el orden;
- `test_spec_fidelidad.py` usaba A-29 como ejemplo de abierta en el cuestionario.

A-29 y A-36 salen del orden de la hoja y de su test, como hizo `trabajo/activar-sesion-03` con las
nueve de la sesión 3. En `test_spec_fidelidad.py`, A-29 cede su sitio a A-43, que sigue abierta y
es `pregunta`. El contrato se amplía a `scripts/hoja_preguntas.py`, con su motivo.
`docs/runbooks/AMBIGUEDADES.md` dice «cerrarla, cuatro»: con esta van cinco, y la hoja solo la vigila
su propio test. Queda para el consultor si se escribe allí; esta rama no toca el runbook (no está en
el contrato).

**Cómo se lee A-36, y qué afirma de más.** A-36 pregunta «¿En qué punto de la mecha va la orden
límite?», y la respuesta grabada habla del 0 de la caja: a «el cero de la caja va siempre en el
extremo del bloque, mecha incluida, o ese es un poco dentro?», «Mecha incluida, siempre.». Contesta
a A-36 porque, desde ADR-0064, la orden (stop, A-47) nace en el 0 de la caja. Así lo escriben su
registro y `ambiguedades.yaml`. La pregunta se escribió cuando la orden era límite en el
retroceso; con una orden límite la respuesta no diría por sí sola dónde va la orden.

## 3. ¿Cambia cuándo se coloca la orden? No: medido (punto 3)

El valor de `orden_limite_nace` no cambia: `al_aparecer_punto_de_breaker` desde
`feature/F35-orden-stop-pivote` (ADR-0064). Cambian el estado y la fuente, y el motor no ramifica
por el estado. En `src/`, `Estado.DEFAULT_AMBIGUOUS` solo lo miran el registro, para anotar la
lectura como ambigua, y la CLI, para contarlo.

**Test sintético, antes y después**: `test_cerrar_a29_no_cambia_cuando_nace_la_orden`
(`tests/unit/test_orden_stop_pivote.py`). Corre el día de la cadena colocada-cancelada-recolocada
por el cableado real y la spec real dos veces:
- con el registro de ANTES, el bloque de `orden_limite_nace` tal como estaba: DEFAULT_AMBIGUOUS, A-29,
  fuente de v7;
- con el de DESPUÉS, el de la rama.

Las peticiones al servidor (tipo, orden, instante y si se aceptó), las órdenes (precio, estado,
colocación y último cambio) y los eventos del broker son iguales. Solo cambia que la lectura deja de
anotarse como ambigua. El test exige además que la cadena coloque algo, para que mida de verdad
cuándo nace la orden: el mismo día con `al_darse_el_esquema` no coloca nada (el test de al lado).
El día de la cadena pasó a una función, `_cadena`, que usan los dos tests.

**Lo que cambia en los tests, y por qué.** `feedback apply` escribe el valor sin comillas
(`valor: al_aparecer_punto_de_breaker`), y cuatro tests buscaban la línea con comillas para
sustituirla: `test_escenarios_por_sesion.py`, `test_orden_stop_pivote.py`,
`test_preparar_a21.py` y `test_sesiones_independientes.py`. Solo cambia la cadena que buscan. El
docstring de `engine/zonas.py` decía «A-29, DEFAULT_AMBIGUOUS» y ahora dice RESUELTA; el párrafo se
reenvolvió sin cambiar otra palabra.

## 4. `docs/sesion-4/PREGUNTAS.md` (punto 4)

Ninguna de las dos estaba entre las pendientes de la sección 1. Las dos ya estaban en la sección 2,
«ya respondidas», que ahora lleva su registro y la fecha del cierre, y el tramo verificado de A-36.
Las dos notas de §4, «sigue ABIERTA», dicen ahora CERRADA el 2026-10-02 en esta rama. El recuento
del pie no cambia: ninguna era «por preguntar».

## 5. El comentario de `SECCIONES_EXENTAS` (punto 5)

`tests/contract/test_documentos_vivos.py` decía que `Completed Features` lleva «una linea por rama
cerrada, con las cifras de ese dia». Desde `trabajo/ajustes-cierre` el cierre no le añade nada. Ahora
dice que es archivo y que lo cerrado vive en el registro de cierre de HISTORIA. `Change Log` tenía
el mismo desfase («el archivo por excelencia»), y dice también que el cierre no le añade.

El pendiente sale de `docs/runbooks/ERRORES-RECURRENTES.md`. Estaba en DOS filas: la de
`trabajo/ajustes-cierre`, donde nació, y la de `feature/escenarios-por-sesion`, que lo arrastró al
cerrar. Sale de las dos.

## 6. PROJECT_STATE (punto 6)

`wc -c PROJECT_STATE.md`: **22.638 bytes**, por debajo de 23.000. Lo que lo movió:
- 22.531 en `main`;
- el puntero a la rama al abrirla;
- las dos filas de la tabla, que salen;
- el recuento de tests, que pasa a 1166.

## Estado

EN CURSO: falta el revisor.
