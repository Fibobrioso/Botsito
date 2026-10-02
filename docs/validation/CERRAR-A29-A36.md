# FUNCTIONALITY VALIDATION REPORT · Cerrar A-29 y A-36

Rama `trabajo/cerrar-a29-a36`, abierta el 2026-10-02 desde `main` `487c64f` (tag
`stable/F36n-escenarios-por-sesion`). Encargo, copiado tal cual:
`docs/encargos/trabajo-cerrar-a29-a36.md`. Tarea autónoma: NO se cierra.

> **CORRECCIÓN (2026-10-02, segunda orden del consultor, §8).** A-29 queda RESUELTA. **A-36 NO**:
> se cerró en `541a4f5` y el consultor la reabrió. Vuelve a ABIERTA, con un registro nuevo que retira
> el cierre, y va a la sesión 4 como pregunta 22. Lo que §2 a §7 cuentan de A-36 es el cierre que se
> deshizo, y queda como estaba.

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

## 7. Informe del revisor

Subagente `revisor`, sobre `e7851f7` y `541a4f5`. Los hallazgos, tal cual; lo comprobado sin
hallazgos, resumido.

> ## Informe del revisor · trabajo/cerrar-a29-a36 · 2026-10-02
>
> ### Eje (a) · Reglas de la casa
> Resumen: 0 bloquea, 0 importa, 2 menor.
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | a1 | menor | `PROJECT_STATE.md` línea 108 (candidatas C5 y C6) sigue diciendo «toca RN-004, RN-008 y A-29» y «toca A-36». Son notas históricas de candidatas y no contradicen nada, pero nombran como pendientes dos ambigüedades que ya están cerradas. | `grep -n "A-36" PROJECT_STATE.md` → línea 108 |
> | a2 | menor | El informe de la rama acaba en «EN CURSO: falta el revisor». Es lo esperado antes de pegar este informe, pero el consultor lo verá así. Tampoco hay `make-check.log` en el árbol, así que no pude ver las líneas `SELLO` ni `PICO DE MEMORIA`. El informe cuenta que el primer `make check` salió rojo con 3 fallos y que se arreglaron, pero no cita el sello final. | `ls make-check.log` → no existe; `docs/validation/CERRAR-A29-A36.md` §2 y «Estado» |
>
> Comprobado sin hallazgos: el contrato (28 ficheros; la ampliación a `scripts/hoja_preguntas.py` con su motivo); `state check`, `spec check` y `knowledge validate` (53 ambigüedades, 147 registros de feedback con historial intacto y commits con Fuente, 437 ítems); los ocho ficheros de test tocados, que pasan; el trailer `Fuente:` (los tres `fb-*`, los dos `ev-*` y ADR-0022 existen); los regímenes (feedback solo añade, HISTORIA solo se amplía, nada en evidence, cases, corpus ni manifests, ni holdout); los tres registros RESOLVE_UNKNOWN (dos sobre ambigüedad y uno sobre parámetro, como A-47), sin cambiar un valor fijado; A-29 y A-36 en RESUELTA con su esquema, sus docs generados (ABIERTA 23→21, RESUELTA 24→26), sus filas fuera de la tabla y `test_kit.py`; ningún ADR ni informe cerrado tocado; ningún sitio nuevo con `cita`; ninguna cifra en la forma ejecutable; `spec_version` 15.6.0 con su hash (subir la menor por un cierre es discutible, pero coherente con los anteriores); `PROJECT_STATE.md` 22.638 bytes; 1166 funciones de test; `feedback apply` solo cambió `orden_limite_nace`, con el mismo valor; los literales de los registros son los `cita_literal` de los ítems, con sus tramos; los cuatro tests solo cambian la cadena que buscan; la hoja de preguntas y su test; las dos filas de ERRORES-RECURRENTES y el comentario de `SECCIONES_EXENTAS`, con `Change Log`; el docstring de `engine/zonas.py`.
>
> ### Eje (b) · Encargo
> Resumen: 0 bloquea, 1 importa, 1 menor. Requisitos: 8 hechos, 1 parcial, 0 no hechos (el parcial: la regla de la spec que cita A-36, que no existe, declarado; y el pegado del revisor, que es esta entrega).
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | b1 | importa | **La lectura de A-36 es un puente de inferencia.** La pregunta de A-36 es «¿en qué punto de la mecha la colocas?» (orden límite). La respuesta del trader habla del 0 de la caja («el cero de la caja va siempre en el extremo del bloque, mecha incluida, o ese es un poco dentro? Mecha incluida, siempre»). Cerrarla como RESUELTA depende de la premisa de que, con la orden stop de ADR-0064, la orden nace en el 0 de la caja. El informe lo declara con franqueza («con una orden límite la respuesta no diría por sí sola dónde va la orden»), así que el declarado es correcto. Aun así, lo que cierra A-36 es una lectura del equipo apoyada en un ADR, no la cita sola, y A-36 deja de aparecer en la hoja de la sesión 4. El `valor_resultante` del registro («en el extremo del bloque, mecha incluida») es fiel a la cita. Hay una discrepancia menor: la afirmación del ítem de evidencia dice «a la pregunta del consultor», y su `notas` apuntan a A-21 y no a A-36. | `docs/validation/CERRAR-A29-A36.md` «Cómo se lee A-36, y qué afirma de más»; `knowledge/evidence/…/ev-v9-011714-08536830.yaml` (`notas: A-21`, `tema: herramientas.caja.cero_mecha_incluida`); `knowledge/spec/ambiguedades.yaml` (pregunta de A-36) |
> | b2 | menor | **El test antes/después mide lo que dice, con un límite.** Corre `_cadena` con el bloque antiguo y el nuevo de `orden_limite_nace` (mismo valor, distinto estado y fuente) y compara peticiones (tipo, id, instante, aceptada), órdenes (precio, estado, colocada, último cambio) y eventos. Falla si la cadena no coloca nada o si el estado cambia el comportamiento. Si el valor cambiara en `parametros.yaml`, falla antes por `texto.count(A29_DESPUES) == 1`, no por la comparación. Es una prueba de que el motor lee el valor y no el estado; no prueba por sí sola que `al_aparecer_punto_de_breaker` nazca en el instante «correcto» (eso lo prueba el test anterior, que sí falla con `al_darse_el_esquema`, como el informe dice). | `tests/unit/test_orden_stop_pivote.py:374-425` y `:340-350` |
>
> ### Lo que no pude comprobar
> La salida de `make check` (escribe; no hay `make-check.log`); la localización de las citas en la cruda de v9 (cuarentena), que no reprodujo; que la pregunta de v9 0:01:30 ofrecía las tres lecturas de A-29, y que A-36 no tenga otra lectura; que no haya tramos protegidos en los dos segmentos (no leyó `tramos_no_citables.yaml`).

**Respuesta de la sesión, hallazgo a hallazgo:**
- **a1, declarado, sin tocar `PROJECT_STATE.md`: y es más que una nota histórica.** La línea es una
  deuda técnica con siete candidatas a ambigüedad SIN ABRIR, y lo que dice sigue siendo verdad.
  C5 y C6 «tocan» A-29 y A-36, y ahora tocan dos RESUELTAS. **C6 es la orden puesta 2 puntos más
  allá del 0 en v7 n.º 3**: algo visto en pantalla que habla justo de dónde va la orden frente al 0.
  No contradice por sí solo «Mecha incluida, siempre» (el 0 en el extremo con la mecha), pero es lo
  primero que la lectura de A-36 tiene que mirar (b1). **Para el consultor.**
- **a2, arreglado**: el estado de abajo, y el sello del commit `541a4f5`: `make check` en verde
  (1814 pasados) sobre el árbol `167cda21…`, con `PICO DE MEMORIA` 286 MiB. El primer `make check`
  salió en rojo (3 fallos, §2), y el commit es el del segundo.
- **b1, declarado; lo decide el consultor.** El cierre de A-36 se apoya en la cita y en ADR-0064, y
  el informe lo dice (§2). Pesan además dos cosas: la candidata C6 (a1) y las `notas` del ítem, que
  apuntan a A-21. Si el consultor prefiere preguntarlo en la sesión 4, A-36 vuelve a ABIERTA con un
  registro que la reabra; en `knowledge/feedback/` solo se añade.
- **b2, de acuerdo, y declarado**: el test mide que el motor lee el valor y no el estado. Que
  `al_aparecer_punto_de_breaker` coloque en su instante lo mide el test de al lado
  (`test_la_cadena_colocada_cancelada_recolocada_y_llenada_por_el_cableado`), que con
  `al_darse_el_esquema` no coloca nada.
- **Lo que no pudo comprobar**: los tramos no citables, en §1; la cruda de v9 no la lee nadie, y la
  verificación de citas la hizo la sesión por la vía autorizada (§1).

## 8. Segunda orden del consultor (2026-10-02)

Copiada tal cual en el encargo, «Segunda orden».

### 8.1 A-29: aceptada, con la nota del contexto

El registro de feedback es inmutable: la nota no se escribe en `fb-…-b41ecf9b`. Va en un registro
NUEVO que lo sustituye (`supersede`), con el mismo literal, el mismo tramo y el mismo valor:
**`fb-2026-09-29-sesion-03-d3063920`**. Su `notas` cita `docs/validation/SESION-03-EXTRACCION.md`
§3.4 y dice que hoy no se puede releer porque v9 está en cuarentena. La spec (RN-010, RN-011,
RN-019), `ambiguedades.yaml` y `PREGUNTAS.md` citan ahora el registro vigente.

**Lo que la orden afirmaba se midió, y no cuadra entero.** `SESION-03-EXTRACCION.md` §3.4 recoge el
contexto de la respuesta:
- 01:24, el consultor: «aquí queda confirmado que se entra siempre por stop»;
- 01:29, el trader: «Sí, exacto»;
- 01:43–01:46, la respuesta.

**No recoge una pregunta en 0:01:30 que ofreciera las tres lecturas.** Esa frase solo está en
`docs/sesion-4/PREGUNTAS.md` §2, escrita en el barrido (`stable/F36e-barrido-sesion-4`), y no hay otro
documento que la sostenga (Grep en `docs/`). Así lo dice la nota del registro: el contexto, en la
extracción; las tres lecturas, solo en `PREGUNTAS.md`. `ambiguedades.yaml` y la descripción de
`orden_limite_nace` ya no dicen «a la pregunta que ofrecía las tres lecturas»: citan la extracción.
La fila de `PREGUNTAS.md` §2 conserva su frase, que es del barrido, y añade dónde está el contexto.

### 8.2 A-36: reabierta

**El registro que la reabre, `fb-2026-09-29-sesion-03-a0b61bc9`**, sustituye al que la cerró
(`fb-…-626c4dc7`). Es `escrito`, procedencia `correccion_consultor` -la que «retira lo que otro
registro afirmaba» y exige `supersede`, como `fb-…-86dc2801`- y su literal es el motivo del
consultor: la pregunta se hizo sobre una orden límite, desde A-47 la entrada es con orden stop, y
está C6.

**Lo que se deshace** (el diff contra `main` lo dice: de A-36 solo quedan el comentario, la
evidencia de v9 en su lista y la pregunta 22):
- `ambiguedades.yaml`: A-36 vuelve a ABIERTA. Su `pregunta` pierde la línea de RESUELTA, y un
  comentario cuenta el cierre y la reapertura con los dos registros. `ev-v9-011714-08536830` se
  queda en su `evidencia`: es lo que el trader dijo del 0 de la caja.
- La tabla «Known Ambiguities» de `PROJECT_STATE.md`: la fila de A-36 vuelve, en su sitio.
- `tests/unit/test_kit.py`: A-36 sale de las RESUELTAS.
- La hoja de preguntas y su test: A-36 vuelve a su sitio en el orden.
- `spec docs --escribir` en el mismo commit; spec 15.6.0 → 15.6.1.
- **Parámetros: ninguno cambió de estado por A-36**, que no tiene (`parametros: []`). Nada que
  devolver.

**La pregunta 22**, en la sección A de `PREGUNTAS.md`, detrás de la 6. Va numerada 22 y no 7 para
no mover el número de las demás, que la spec y los ADR citan (como se hizo con la 20 y la 21). Es
la pregunta de la orden, cerrada con «otra, ¿cuál?», y cita A-36 y C6, sin fechas ni resultados.
El pie dice 22 por preguntar y 14 ya respondidas: A-36 sale de la tabla de §2.

**Lo que el modelo de feedback no sabe hacer.** No hay acción para REABRIR una ambigüedad: sobre
una ambigüedad solo se admite `RESOLVE_UNKNOWN`. Así que el registro que la reabre es un
`RESOLVE_UNKNOWN` con valor «sin resolver», y `feedback pending` lo cuenta: «1 pendientes de 101
activos», `fb-…-a0b61bc9 … A-36 esta ABIERTA`. No rompe nada (`knowledge validate` en verde), y
desaparecerá cuando la sesión 4 responda la pregunta 22. Arreglarlo es tocar
`src/botsito/feedback/`, que no está en el contrato: queda para el consultor.

### 8.3 Cerrar toca cinco sitios

`docs/runbooks/AMBIGUEDADES.md` decía «cerrarla, cuatro» en dos sitios: el título de la sección y su
apartado. Ahora dice cinco: la hoja de preguntas y su test, con lo medido aquí. Las guardias que la
vigilan pasan de dos a tres, y reabrir toca los mismos cinco al revés. `CLAUDE.md` lo repetía
(«cerrarla cuatro») y ahora dice cinco; su lista de guardias suma `tests/unit/test_hoja_preguntas.py`.
El contrato se amplía a los dos ficheros, con su motivo.

### 8.4 PROJECT_STATE

`wc -c`: **22.722 bytes** (la fila de A-36 vuelve), por debajo de 23.000.

## Estado

**Rama lista para revisión, NO cerrada.** Tarea autónoma: no se cierra. A-29 RESUELTA con la
respuesta grabada de la sesión 3, verificada por la vía autorizada y con la nota del contexto (§8.1).
A-36 cerrada y reabierta por el consultor: va a la sesión 4 como pregunta 22 (§8.2). El
comportamiento del motor no cambia, y está medido (§3). Cerrar una ambigüedad toca cinco sitios
(§8.3). `PROJECT_STATE.md` pesa 22.722 bytes. Para el consultor: que la frase «las tres lecturas»
solo la sostiene `PREGUNTAS.md` (§8.1), y que el modelo de feedback no sabe reabrir (§8.2). El
revisor de la segunda orden está en §8.5.
