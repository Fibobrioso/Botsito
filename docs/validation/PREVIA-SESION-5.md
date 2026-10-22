# PREVIA-SESION-5 · El repo listo para la sesión 5 con el trader (R4.1 y A.3)

Rama `trabajo/previa-sesion-5`, abierta el 2026-10-21 desde `main` en 24b7cba (commit de estado
sobre el merge e76f829, tag `stable/F37x-ea-conexion`). Encargo:
`docs/encargos/trabajo-previa-sesion-5.md`. Tramo: R4 (R4.1 y A.3 de `docs/plan/HOJA-DE-RUTA.md`;
V de la Next Action). Modelo de la sesión: `claude-opus-5-5` según el entorno de la sesión, con
esfuerzo medio (`/effort` puesto por Aleks antes del encargo); `/model` lo revisa Aleks en su
terminal.

## 0 · La base, comprobada al abrir

Las cuatro comprobaciones de la skill `abrir-rama`, con su salida:

| Comprobación | Comando | Salida |
|---|---|---|
| `main` es el sha del encargo y es `origin/main` | `git rev-parse --short main`; `git rev-parse main origin/main` | `24b7cba`; dos veces `24b7cba26057520476a9b96639f2855ee5ba2406` |
| El último tag de HISTORIA apunta al merge bajo `main` | `git rev-parse "stable/F37x-ea-conexion^{commit}"`; `git rev-parse main^1` | dos veces `e76f8292d3774b2decf8775cc87a80783d95cc01`; `git ls-remote --tags origin stable/F37x-ea-conexion` → `c519054… refs/tags/stable/F37x-ea-conexion` |
| La CI de `main` sobre su HEAD | `gh run view 39705799089 --json headSha,status,conclusion,workflowName`, a mano y una vez | `{"conclusion":"success","headSha":"24b7cba26057520476a9b96639f2855ee5ba2406","status":"completed","workflowName":"ci"}` |
| Ninguna otra rama | `git branch --list`; `git ls-remote --heads origin "fix/*"` | `* main`; vacío |

`PROJECT_STATE.md` en `main`: 24.135 bytes (`wc -c`), como dice el encargo. `git status --short`
vacío.

El primer `make check` (commit de apertura 05a4eb0): exit 0, `2729 passed in 1065.04s`,
`SELLO: make check en verde sobre el arbol 2df884a708449cf63b93b7ef296aabfce9e1a044`.
`PICO DE MEMORIA de make check: 298 MiB en `test` (suma de sus procesos, memoria comprometida, Windows; el mayor proceso, 288 MiB)`.

**Negativas de la guardia** (regla del consultor del 2026-10-21: PARADA salvo seguir la forma que
propone la guardia, declarándolo). Tres, las tres resueltas con la forma que proponía su mensaje:
1. `git show` con un argumento construido al ejecutarse (`$(git log …)`): la guardia pedía «rutas
   LITERALES, sin `$(...)`». Partí el comando y usé el sha literal (a70ea6e).
2. `sed -i …` y, en el mismo comando, `uv run botsito state check`: la guardia pedía la ejecución
   «en OTRA llamada». Lo partí en tres llamadas.
3. Un `awk` con un programa fuera de su lista: lo quité y usé `sed -n` y `grep`, que la guardia
   nombra como admitidos.

## 1 · Fase 0: las dos preguntas y la orientación de la caja (punto 2)

**La regla, verificada.** `knowledge/spec/parametros.yaml:631-632` (`orden_stop_punto`,
`ultimo_pivote_m1`: «el ultimo pivote de M1 contrario al sentido de la entrada -un BAJO en una
venta-») y `:652-654` (`caja_bloque`: «el bloque que da el 1 de la caja de cada orden stop, con el 0
en el punto», `r6` «el extremo opuesto -la maxima en una venta-»). En una compra el 0 es un ALTO de
M1 (arriba) y el 1, el mínimo del bloque (abajo, del lado del stop). (a) = r1, (b) = r4 y (c) = r6
(`:653-656`); `valor: r6` y `valor: ultimo_pivote_m1`, los dos DEFAULT_AMBIGUOUS de A-48. Lo que
dice el encargo es correcto.

**Cada pregunta que nombra la caja:**

| Pregunta | Qué dice hoy (`docs/sesion-5/PREGUNTAS.md`) | Orientación |
|---|---|---|
| S-7 | Pregunta «¿desde dónde trazas el 0?» (`:254`) con (a) r1 y (b) r4, y (c) «depende» (`:255-257`) | **al revés**, como dice el encargo (matiz: la (c) de hoy no es r6, es «depende»). Además, **el esquema** (`:252-253`) dice de la compra «el punto de breaker es el mínimo de la última roja», y en una compra el punto es un alto: también está al revés, y el recuadro del encargo no lo sustituye (decisión 1). La línea «Si la última vela roja es muy pequeña, ¿pones el 0 en ella igual?» (`:261`) también estaba al revés, pero sale con la lista nueva de «Para precisar» del recuadro |
| S-12 | Esquema: «en el segundo el 1 queda por encima y el 0 por debajo» (`:376-377`) | **al revés**, como dice el encargo. Pero hay algo más grave: decisión 0 |
| S-13 | Para precisar: «Si el 1 de la caja sube mucho, ¿la sigues moviendo igual?» (`:414`), de una orden de compra con el precio que baja y toma otro bajo de M15 (`:404-406`) | **posible inversión**: en una compra el 1 es un mínimo y, mientras el precio baja, se aleja hacia abajo; no «sube» (decisión 2) |
| S-16 | En una compra, el precio «ya está por encima del 0», «donde iría tu orden de compra» (`:469-477`) | **correcta**: en una compra la orden va en el 0, arriba, y pasado el 0 es por encima |
| S-17 | El break even y la zona de control posterior a la entrada (`:489-520`) | **no nombra la caja** ni su 0 o su 1 (matiz del auditor: el encargo la cita entre las que la nombran) |

Barrido además con `grep -n -E '(el|del|al) [01]\b|extremo|mínimo de la última|punto de breaker es'`
sobre el fichero entero: ninguna otra pregunta nombra un extremo de la caja.

**El lado de S-12, contra el código (lo más grave de la fase 0).** En alcista la toma es un BAJO y la
entrada una COMPRA (`src/botsito/engine/zonas.py:115-116`), y la zona es ruido si
`e.entrada > toma["nivel"]` en una compra (`zonas.py:537-539`: «la operativa alcista va por debajo
de la liquidez tomada»). RN-005 prohíbe abrir en el ruido; el predicado dice «por encima si el sesgo
es alcista» (`knowledge/spec/strategy_spec.yaml:198-205`, que añade que «en alcista lo de ENCIMA sea
ruido es simetria del ejemplo bajista, no una frase del trader»). A-50 lo dice con todas las letras:
«una compra cuyo 0 queda por encima del nivel […] es ruido aunque el 1 quede del lado del trader»
(`knowledge/spec/ambiguedades.yaml`, A-50, comentario). Así:
- en los dos dibujos del recuadro de S-12 el 0 queda por encima del bajo tomado, y **hoy el bot no
  opera ninguno**: el «Para Aleks» del encargo («opera las dos: eso es (a)») no es lo que hace el
  código;
- el lado bueno que dibuja la pregunta («la caja entera por encima») es el que RN-005 llama ruido.
  Lo sostiene solo `ev-v9-004919-c6bfb3ee` («tiene que ser todo por encima», de una compra), que A-50
  cita junto a los ítems de RN-005 (`ev-v1-001306-f98e12e9`: «por debajo en alcista») con
  `contradiccion: null`. El repo se contradice y no lo marca.

No escribo el recuadro de S-12 hasta la decisión 0, ni los de S-7 y S-13 hasta las decisiones 1 y
2, para que cada pregunta lleve un solo recuadro.

**El régimen del recuadro** (matiz del auditor): la regla de los recuadros de `CLAUDE.md` es de
`docs/validation/`; `docs/sesion-5/` no tiene régimen escrito y `docs/sesion-4/` no lleva ninguno.
Que PREGUNTAS.md se corrija con recuadros es decisión del consultor en este encargo, por analogía,
y así se dirá en el recuadro. Y como los textos de los códigos entran en
`CODIGOS_DE_SESION_TEXTO["05"]` con la ingesta (`PREGUNTAS.md:22-24`), cada recuadro dirá que el
texto que vale para la hoja y para la ingesta es el suyo.

## 2 · El encargo frente al repo (auditor)

El subagente `auditor-encargo`: 40 afirmaciones, 24 correctas, 3 incorrectas y 13 con matiz, más
8 herencias no recogidas. Lo que cambia algo:

| # | Qué | Veredicto | Qué hago |
|---|---|---|---|
| 20-21 | El «Para Aleks» de S-12 y el lado de la caja | INCORRECTA y MATIZ grave | decisión 0 (§1) |
| 10 | Las opciones de hoy de S-7 son r1, r4 y «depende», no r1, r4 y r6 | MATIZ | §1 |
| 12 | La cita de §0.e.6 es «el 0 queda de este lado y el 1 del otro» (`ACTIVAR-SESION-04.md:324-327`) | MATIZ | ninguna: no cambia el recuadro |
| 15 | Los recuadros en `docs/sesion-5/` son por analogía, no por regla | MATIZ | §1 |
| 22 | S-17 no nombra la caja; S-13 «sube» puede estar al revés | MATIZ | decisión 2 |
| 29 | «deja una línea con el puntero»: `docs/state/README.md:75` dice que en PS «no queda ni un resumen», y plataforma-adelantada no dejó ninguno en PS | INCORRECTA | decisión 3 |
| 31-32 | El texto que sale va siempre a HISTORIA con su bloque (`README.md:72-75`); «# Next Action HECHA» es solo para letras de la Next Action, y un cambio de la Next Action va en el commit del contrato de la orden de cierre | MATIZ | uso los bloques del README (`# Technical Debt RECLASIFICADA`, `# Regla viva SUSTITUIDA`); ninguna letra de la Next Action cambia en las fases |
| 33 | BUSCAR EN EL CORPUS es una deuda abierta: el campo que pedía su condición no existe en `ambiguedades.yaml`, y ADELGAZAR-ESTADO (`:114`) y PLATAFORMA-ADELANTADA (`:243-244`) la dejaron | INCORRECTA | decisión 3, opción separada |
| 34-35 | Los heredados ya se revisaron y se quedaron (`PLATAFORMA-ADELANTADA.md:189-215`); la pasada anterior acabó en 22.517 | MATIZ | §4: no toco ningún heredado |
| 37, H3 | La consulta a `casos_ocultos` se declara en HOLDOUT-EXPOSICIONES el mismo día; el contrato no lo permitía | MATIZ | contrato ampliado en el commit de esta fase; fila del 2026-10-21 |
| 38 | `simular_cierre.py` de VISOR-CONSTRUCCION trae las sustituciones de su rama | MATIZ | escribiré uno propio en `docs/validation/anexos/PREVIA-SESION-5/` (amplío el contrato cuando toque) |
| H1 | A.4, la copia de seguridad: fecha límite «antes de grabar la próxima sesión», y sigue INCOMPLETA (`HOJA-DE-RUTA.md:408-414`; `PREGUNTAS.md:8-9`) | herencia | **para Aleks, antes del viernes** |
| H2 | La línea de G.2 sobre el paso 6 («dice todavía "abril o agosto"», `HOJA-DE-RUTA.md:470-471`) | herencia | corregida en esta fase, en la rama: dejaba de ser verdad con el cambio del runbook, y la hoja de ruta no es la Next Action (§3) |
| H5 | Los esquemas de S-7 y S-12 están al revés en el cuerpo, y el esquema se dibuja para el trader | herencia | decisiones 0 y 1 |
| H8 | La contradicción RN-005 frente a `ev-v9-004919-c6bfb3ee` sin marcar en A-50 | herencia | decisión 0 (marcarla en `ambiguedades.yaml` queda fuera de esta rama, que no toca la spec) |

El informe del auditor, entero, está en §11.

## 3 · El runbook y la fecha (punto 3), hecho

- **La fecha**: la línea del paso 1 de «Antes» (`SESION-DE-PREGUNTAS.md:53`) con `2026-10-23`
  imprime **`False`**. Declarado en `HOLDOUT-EXPOSICIONES.md`, fila del 2026-10-21.
- `docs/runbooks/SESION-DE-PREGUNTAS.md`, paso 6 de «Antes»: «y el día tiene que ser de abril o de
  agosto» pasa a «y el día tiene que ser de construcción, los que dice la regla 2 (abril, julio del 1
  al 17, agosto y enero del 2 al 30)».
- `docs/plan/HOJA-DE-RUTA.md`, A.3: una línea **Estado** con la fecha y la confirmación de marzo
  pendiente. A.3 no pasa a HECHA. La fecha no va a PROJECT_STATE.
- `docs/plan/HOJA-DE-RUTA.md`, G.2: la frase «el paso 6 … dice todavía "abril o agosto"» pasa a decir
  que remite a la regla 2 desde esta rama (herencia H2 del auditor).

## 4 · Fase 0: lo que propongo sacar de PROJECT_STATE (punto 4)

Criterio: `docs/state/README.md`, «Que sale de PROJECT_STATE, y con que criterio». Sale solo una
entrada entera; su texto literal va al final de `HISTORIA.md` con su condición y su evidencia, y
cuando su sitio es un runbook, el texto entero va también al runbook (como la opción 6a de
PLATAFORMA-ADELANTADA). Tamaño de partida, ya en la rama: **24.277 bytes** (Current Feature de la
rama). Bytes con el salto de línea.

**Conjunto A: hechos y reglas que no son deuda abierta (1.346 bytes).**

| PS | Entrada (inicio) | Bytes | Condición | Destino del texto entero |
|---|---|---|---|---|
| 132 | `idealTP`: UNA COLUMNA DEL MATERIAL QUE NO SABEMOS QUE ES Y NO USAMOS | 111 | (b) tras llevarlo | `MIRAR-EL-MATERIAL.md`, el texto del Archivo 1 (`HISTORIA.md:564`): es una regla sobre qué no se mira del material |
| 145 | Transcripciones heredadas (Whisper tiny, `_procesado/`) | 223 | (b) tras llevarla | `MIRAR-EL-MATERIAL.md`, «Donde esta el texto de las transcripciones» (que ya dice «sirve para LOCALIZAR, no para citar literal», `:89-90`, sin la decisión del 2026-09-05) |
| 147 | `data/fotogramas/` … no se copia a Drive | 249 | (b) tras llevarla | `MIRAR-EL-MATERIAL.md` |
| 148 | F07, limitacion declarada | 215 | (d) | ya entera en `docs/validation/F07-evidence-extraction.md:168-170` y `:188` («Sin cliente de API de LLM (no hay clave)»): no se escribe nada |
| 149 | Hook local: tras cambiar `scripts/git-hooks/`, ejecutar `make hooks` | 200 | (b) tras llevarla | `RITUAL.md`, «La primera vez con la puerta» (`:354-356` ya dice que se ejecuta cada vez que cambia un hook; falta el hecho del 2026-09-07 y que la garantía real son los tests de historial en CI) |
| 150-152 | Proteccion de rama en GitHub activada el 2026-09-04 | 237 | (b) tras llevarla | `RITUAL.md` |

Con A: **22.931 bytes**. **No llega a 22.000.** Ninguna de las seis es una deuda abierta: cuatro son
hechos o reglas sin nada pendiente, la de F07 es una limitación de un informe cerrado, y la de los
hooks y la de la protección de rama son reglas del ritual.

**Conjunto B: Reglas vivas que «solo viven aquí», llevadas enteras a un runbook (1.519 bytes).**

| PS | Bloque | Bytes | Destino |
|---|---|---|---|
| 159 | Change Regimes: `data/manifests/`, transcripciones y fotogramas INMUTABLES; corrección = manifiesto nuevo con `reemplaza_a`; una extracción activa por vídeo | 281 | `MIRAR-EL-MATERIAL.md` |
| 165-166 | Things That Must Not Be Changed: ficheros con LF y UTF-8; git con `core.quotepath=false` | 180 | `ERRORES-RECURRENTES.md` |
| 168-172 | Decisions and Rationale: las tres decisiones de proceso del 2026-09-04 (con su cabecera) | 688 | `RITUAL.md` o un `docs/runbooks/DECISIONES-DE-PROCESO.md` nuevo |
| 174-179 | Known Issues: el trailer `Fuente:` por commit y el hash de 8 hex de los ids (con su cabecera) | 370 | `AMBIGUEDADES.md` (el trailer) y `RITUAL.md` (los ids), o el mismo fichero nuevo |

Con A y B: **21.412 bytes**. Pero B saca de PROJECT_STATE reglas que ADELGAZAR-ESTADO (`:140-147`)
dejó porque «no viven en otro sitio», y mover una regla de proceso a un runbook decide dónde se lee
esa regla. Las sesiones leen PROJECT_STATE entero y los runbooks solo cuando la tarea lo pide.

**Fuera de los dos conjuntos:** BUSCAR EN EL CORPUS (111 bytes): el encargo la pone como ejemplo de
regla, y el auditor la mide como deuda abierta (fila 33). Ningún heredado: tienen `HER:n` en la hoja
de ruta y ya se revisaron (fila 34). Ninguna deuda de código.

**El puntero.** `README.md:75` dice que en PROJECT_STATE «no queda ni un resumen». Con una línea de
puntero por sección (unos 150 a 200 bytes cada una) los números de arriba suben.

## Lo que no pude medir

- El sentido de v9 0:49:19 (compra o venta) en la transcripción: no la abro; solo el ítem de
  evidencia, que dice «compra».
- Si el esquema de S-16 («una roja pequeña que cierra en el 0», en una compra) es coherente
  geométricamente con un punto que es un alto de M1: la orientación de la orden es correcta; la
  forma del dibujo no la juzgo.

## Exposiciones

Una fila nueva en `HOLDOUT-EXPOSICIONES.md`, del 2026-10-21: la consulta a `casos_ocultos` con la
fecha de la sesión (`False`) y lo que se leyó. Nada reservado.

## Lo que necesito que decidas

0. **S-12: de qué lado del bajo tomado opera el trader en una compra.** El código y RN-005 dicen
   por debajo (por encima es ruido); `ev-v9-004919-c6bfb3ee` dice «todo por encima»; A-50 junta las
   dos sin marcar la contradicción. Con el recuadro del encargo, el bot no opera ninguno de los dos
   dibujos. Opciones: (a) el recuadro del encargo tal cual, con el «Para Aleks» medido («hoy el bot
   no opera ninguno de los dos: en una compra llama ruido a todo 0 por encima del bajo tomado,
   RN-005; la pregunta dibuja el lado de `ev-v9-004919-c6bfb3ee`, que contradice a RN-005») y un
   esquema corregido con el 0 arriba; (b) el recuadro con los dibujos del lado de RN-005 (en el
   primero, la caja entera por debajo de la línea; en el segundo, el 0 por encima y el 1 por
   debajo), con (b) «solo la primera: la caja entera tiene que quedar por debajo» y el «Para Aleks»
   «hoy el bot opera el primero y no el segundo»; (c) antes de la de A-50, una pregunta del lado:
   «En una compra, después de tomar el bajo de M15, ¿tu caja tiene que quedar por encima o por
   debajo de la línea?», y la de A-50 sobre el lado que diga. Recomiendo (c): el repo se contradice
   y solo el trader lo decide; (a) y (b) eligen un lado por él. Coste de (c): una pregunta más en
   una hoja de 25 que ya va justa de tiempo.
1. **S-7: el esquema.** «El punto de breaker es el mínimo de la última roja» contradice el «0 en el
   punto de breaker, arriba» del recuadro. Opciones: (a) el recuadro sustituye también el esquema:
   «en M1, para una compra, un tramo de tres velas rojas seguidas y después la subida; el 0 va en
   el punto de breaker, el último alto de M1, arriba, y el 1 abajo, del lado del stop»; (b) el
   esquema queda como está. Recomiendo (a): el esquema se dibuja para el trader y hoy le enseña el 0
   abajo. Coste de (b): una pregunta cuyo dibujo contradice su texto.
2. **S-13: «Si el 1 de la caja sube mucho».** En una compra el 1 es un mínimo y se aleja hacia
   abajo. Opciones: (a) un recuadro en S-13 que lo cambia por «Si el 1 de la caja baja mucho (la
   caja se hace muy grande), ¿la sigues moviendo igual?»; (b) se queda. Recomiendo (a): es la misma
   clase de error que S-7 y S-12. Coste de (b): el trader contesta sobre un movimiento que en una
   compra no pasa.
3. **PROJECT_STATE.** Opciones: (a) solo el conjunto A, sin línea de puntero en PS (README:75):
   22.931 bytes, por encima del objetivo; (b) A y B, sin puntero: 21.412 bytes, con las reglas de
   proceso en runbooks; (c) A y B con un puntero por sección: hacia 21.800; (d) cualquiera de las
   anteriores más BUSCAR EN EL CORPUS en `AMBIGUEDADES.md` (−111). Recomiendo (a): saca todo lo que
   no es deuda ni regla viva sin cambiar dónde se leen las reglas de proceso, y deja 2.069 bytes
   libres hasta el tope para la ingesta. Si el objetivo de 22.000 manda, (c), y en el destino de B
   un runbook nuevo, `docs/runbooks/DECISIONES-DE-PROCESO.md`, antes que repartirlo. Coste de (b) o
   (c): las tres decisiones del 2026-09-04 y los Known Issues dejan de cargarse en cada sesión.

El `make check` del commit de la fase 0 (0402698): exit 0, `2729 passed in 1040.57s`,
`SELLO: make check en verde sobre el arbol ad9f23dd7d28202873418d90244e6875341b75ab`,
`PICO DE MEMORIA de make check: 297 MiB en `test` (suma de sus procesos, memoria comprometida, Windows; el mayor proceso, 287 MiB)`.

## Respuesta del consultor a la PARADA (2026-10-21)

Copiada tal cual (también al final de `docs/encargos/trabajo-previa-sesion-5.md`):

> Respuesta del consultor a la PARADA de la fase 0 de trabajo/previa-sesion-5 (2026-10-21). Cópiala tal cual en el informe y aplícala punto por punto (skill fase-cero).
>
> 0. (c), dentro de S-12 y sin cambiar la numeración. S-12 pasa a tener dos partes, en este orden: primero el lado («En una compra, después de que el precio toma la liquidez de M15, ¿tu caja tiene que quedar por encima o por debajo del nivel tomado? (a) por encima; (b) por debajo; (c) depende, ¿de qué?»), con un esquema neutro (el nivel tomado y una caja a cada lado, sin decir cuál vale); y después la de A-50, dicha sobre el lado que haya contestado («Y si la caja queda a caballo del nivel, con el 0 de tu lado y el 1 del otro, ¿la operas?»). En «Lo que nos has dicho» van las dos citas que se contradicen (la de RN-005, ev-v1-001306-f98e12e9, y ev-v9-004919-c6bfb3ee), sin decirle cuál sigue el bot. El «Para Aleks» corregido dice: hoy el bot sigue RN-005 (en una compra, la zona por encima del bajo tomado es ruido) y no opera ninguno de los dos dibujos del texto anterior; la respuesta a la primera parte decide si RN-005 sigue o se reabre. Por qué: el repo se contradice y solo el trader puede decidirlo; preguntar A-50 sobre un lado equivocado no cierra nada. El error del «Para Aleks» anterior («opera las dos: eso es (a)») es del consultor y va al informe y a la orden de cierre.
>    Lo mismo afecta a S-15: su «Para Aleks» dice que el lado del ruido ya está respondido con ev-v9-004919, y no lo está. Corrígelo en su recuadro: el lado se pregunta en S-12.
> 1. (a). El recuadro de S-7 sustituye también el esquema: el 0 arriba, en el último alto de M1 (el punto, donde va la orden de compra), y el 1 abajo, con los tres mínimos rotulados (la última roja, el tramo de rojas y todas las velas desde la que marca el punto).
> 2. (a). Recuadro en S-13: «sube mucho» pasa a «baja mucho (la caja se hace muy grande)».
> 3. (c). El conjunto A y las Reglas vivas, estas a un runbook nuevo, docs/runbooks/DECISIONES-DE-PROCESO.md, con el texto entero y en el mismo orden. En PROJECT_STATE se quedan los encabezados que exigen los tests, cada uno con una sola línea que apunta a su sección del runbook: un puntero, no un resumen. Cada entrada del conjunto A va entera a un destino que el informe nombra; ninguna se borra sin destino. «BUSCAR EN EL CORPUS» se queda en Technical Debt, como dice el auditor. Si al hacerlo algún test exige que un texto viva en PROJECT_STATE, PARADA. Por qué: la ingesta y las dos activaciones que vienen necesitan más de 2 KB libres.
> 4. Además: S-9 y S-10 nombran bajos de M15 para comprar, que es lo que dice RN-005. Comprueba en el informe que sus esquemas y su texto no dan por bueno ningún lado de la caja, y di lo que encuentres. No hace falta cambiarlas si no lo dan.
>
> Sigue sin parar hasta la entrega, con el revisor y su comprobación añadida: que en S-7, S-12, S-13 y S-15 la caja y el lado estén bien orientados contra RN-005, orden_stop_punto y caja_bloque.

## 5 · La respuesta, aplicada punto por punto

| Punto | Qué se hizo | Dónde |
|---|---|---|
| 0 | Recuadro de S-12: dos partes en este orden, el lado (con el texto literal de la respuesta y un esquema neutro, una caja a cada lado de la línea sin decir cuál vale) y la de A-50 sobre el lado contestado. «Lo que nos has dicho» con las dos citas que se contradicen (`ev-v1-001306-f98e12e9` y `ev-v9-004919-c6bfb3ee`), sin decir cuál sigue el bot, y la de la sesión 4 (v10 1:50:03), que ya estaba. «Para Aleks»: hoy el bot sigue RN-005 y no opera ninguno de los dos dibujos del texto anterior; la primera parte decide si RN-005 sigue o se reabre. **El recuadro dice que el error del «Para Aleks» anterior es del consultor.** Recuadro de S-15: su última frase del «Para Aleks» pasa a decir que el lado se pregunta en S-12, primera parte | `docs/sesion-5/PREGUNTAS.md`, recuadros antes de S-12 y de S-15 |
| 1 | Recuadro de S-7 con el texto del encargo y el esquema sustituido: el 0 arriba, en el último alto de M1 (el punto, donde va la orden de compra), y el 1 abajo con los tres mínimos rotulados | recuadro antes de S-7 |
| 2 | Recuadro de S-13: «Si el 1 de la caja baja mucho (la caja se hace muy grande), ¿la sigues moviendo igual?» | recuadro antes de S-13 |
| 3 | El conjunto A y las Reglas vivas del conjunto B, enteras, a su destino (abajo, «Lo que salió de PROJECT_STATE»); punteros; «BUSCAR EN EL CORPUS» se queda. **Ningún test exige texto de las Reglas vivas en PROJECT_STATE**: `test_project_state.py:7-17` exige solo los `## `, y ningún test, script ni módulo de `src/` lee `### Decisions and Rationale`, `### Known Issues`, `### Change Regimes` ni `### Things That Must Not Be Changed` (`grep -rn` sobre `tests`, `src` y `scripts`). Sí lo cita un **comentario**: el docstring de `tests/contract/test_tramos_fuente.py:5`, «(PROJECT_STATE, Decisions and Rationale, 2026-09-04)». No es una aserción, así que no es PARADA; `tests/` está protegido en esta rama, y va una línea de Technical Debt en el commit del contrato | `docs/runbooks/DECISIONES-DE-PROCESO.md`, `MIRAR-EL-MATERIAL.md`, `RITUAL.md`, `docs/runbooks/README.md`, PROJECT_STATE, HISTORIA |
| 4 | S-9 y S-10, abajo | — |

Los recuadros solo **añaden** líneas: `git diff --numstat docs/sesion-5/PREGUNTAS.md` da `105 0`. El
cuerpo queda intacto.

**Desviaciones al aplicarla (declaradas, para que el consultor las confirme en la revisión):**
1. **La segunda parte de S-12, con el lado (b).** La pregunta de la respuesta, «con el 0 de tu lado
   y el 1 del otro», solo se puede dibujar si contesta (a), por encima. En una compra el 0 está
   siempre arriba (`orden_stop_punto`, `parametros.yaml:631`). Si contesta (b), por debajo, una caja
   a caballo tiene el 1 de su lado y el 0 del otro. El recuadro lleva la pregunta de la respuesta
   tal cual para (a) y, para (b), la misma con el 0 y el 1 cambiados de lado, con la razón entre
   paréntesis. Con (b) es justo la lectura de hoy de A-50 (el 0 al otro lado es ruido), y el «Para
   Aleks» lo dice. No paré: la respuesta pide no parar hasta la entrega, el cambio es el mínimo que
   deja la pregunta bien orientada en los dos casos, y la rama queda para revisión.
2. **Lo que la respuesta no dictó y escribí yo**, en el mismo estilo de la hoja: el título de S-12
   («De qué lado del nivel tomado va tu caja, y si la operas a caballo»), su «Lo que todavía no
   sabemos», el esquema de la segunda parte (la caja cruzando la línea, el 0 arriba y el 1 abajo) y
   su «Para confirmar al final». La segunda parte va sin opciones, como la da la respuesta. «Para
   precisar» de S-12 es la del cuerpo, sin cambios.
3. **Destino de la limitación de F07.** En la fase 0 la puse en (d), porque su informe la dice. El
   texto entero del Archivo 1 (`HISTORIA.md:589`) añade el recall («acepto los 341 sin cambios…») y
   el dueño («si llega una clave…»), que el informe no trae literal. Como «ninguna se borra sin
   destino», va entera a `DECISIONES-DE-PROCESO.md`, en una sección propia que dice que no es una
   regla viva.
4. **El alcance del conjunto B.** La respuesta dice «las Reglas vivas»; la opción (c) que eligió es
   la de la fase 0, cuyo conjunto B son cuatro bloques. Negando por defecto, salen esos cuatro. Se
   quedan en PROJECT_STATE el régimen del holdout y las tres primeras de «Things That Must Not Be
   Changed», que ADELGAZAR-ESTADO (`:140-142`) dejó por no vivir literales en otro sitio y que la
   fase 0 no propuso mover. Con ellos dentro, PROJECT_STATE ya baja de 22.000.
5. **Los punteros.** `test_project_state.py` exige solo los `## `. Hay un puntero de una línea en
   cada uno de los dos de los que salió algo: «Technical Debt» lleva, en su línea de cabecera,
   «Lo que no era deuda, desde trabajo/previa-sesion-5: `docs/runbooks/MIRAR-EL-MATERIAL.md` y
   `RITUAL.md` (al final) y `DECISIONES-DE-PROCESO.md` (F07); tabla en PREVIA-SESION-5.md §6» (con
   los runbooks nombrados tras el hallazgo h2 del revisor), y «Reglas vivas» lleva, en la suya («Las
   que solo vivian aqui y se quedan», m1), la lista de lo que salió y
   `docs/runbooks/DECISIONES-DE-PROCESO.md`, «en sus secciones del mismo nombre». Los `###` de
   Decisions and Rationale y Known Issues salen enteros (ningún test los exige); en el runbook son
   `## ` con el mismo título.

**Punto 4: S-9 y S-10 no dan por bueno ningún lado de la caja.**
- S-9 (`PREGUNTAS.md`, el cuerpo): el esquema son tres bajos de M15 «para una compra», y la pregunta
  es cuál es la liquidez («¿Cuál es tu liquidez para comprar?»). No dibuja ninguna caja ni dice de
  qué lado del nivel va la operación. «Si el precio toma con cuerpo el más reciente y sigue bajando
  hacia el siguiente» habla del precio, no de la caja.
- S-10: el esquema es un bajo de M15 tomado a las 6:45 y otra vez a las 7:20, con «el precio vuelve
  por encima» entre las dos. Es lo que hace el precio entre dos tomas, no un lado de la caja, y la
  pregunta es cuál de las dos tomas vale. No nombra la caja.
- Ninguna de las dos se cambia.

## 6 · Lo que salió de PROJECT_STATE, y adónde

Cada entrada, entera, a un runbook; su texto literal, con su condición (b) y su evidencia, al final
de `docs/state/HISTORIA.md`, en dos bloques: «# Technical Debt RECLASIFICADA · sale de
PROJECT_STATE.md en trabajo/previa-sesion-5 (2026-10-21)» y «# Regla viva SUSTITUIDA · sale de
PROJECT_STATE.md en trabajo/previa-sesion-5 (2026-10-21)». Este último título es la clase que
`docs/state/README.md` da a las reglas que salen; el bloque dice que ninguna se sustituye, que se
mudan.

| Entrada | Sección de PS | Destino del texto entero |
|---|---|---|
| `idealTP` | Technical Debt | `MIRAR-EL-MATERIAL.md`, «Tres hechos del material que vivían en PROJECT_STATE», con el texto del Archivo 1 (`HISTORIA.md:564`), que PS recortaba |
| Transcripciones heredadas | Technical Debt | la misma sección |
| `data/fotogramas/` no se copia a Drive | Technical Debt | la misma sección |
| F07, limitación declarada | Technical Debt | `DECISIONES-DE-PROCESO.md`, «Limitacion declarada de F07», con el texto del Archivo 1 (`HISTORIA.md:589`) |
| Hook local, `make hooks` | Technical Debt | `RITUAL.md`, al final de «La primera vez con la puerta» |
| Protección de rama en GitHub | Technical Debt | la misma sección de `RITUAL.md` |
| `data/manifests/` … INMUTABLES | Reglas vivas, Change Regimes | `DECISIONES-DE-PROCESO.md`, «Change Regimes (must be respected), lo que CLAUDE.md no dice» |
| Ficheros con LF y UTF-8 | Reglas vivas, Things That Must Not Be Changed | `DECISIONES-DE-PROCESO.md`, «Things That Must Not Be Changed» |
| Decisions and Rationale (entero) | Reglas vivas | `DECISIONES-DE-PROCESO.md`, «Decisions and Rationale» |
| Known Issues (entero) | Reglas vivas | `DECISIONES-DE-PROCESO.md`, «Known Issues» |

`docs/runbooks/README.md` nombra el runbook nuevo.

**Comprobado con un guion**, `docs/validation/anexos/PREVIA-SESION-5/comprobar_movido.py <raiz>`
(solo lee: `git show main:PROJECT_STATE.md` y los ficheros). Cada línea que está en el PS de `main` y
no en el de la rama tiene que aparecer literal en uno de los tres runbooks y en la cola de HISTORIA
de esta rama, como línea entera (sin la sangría); en el runbook vale también como arranque de una
línea más larga, si tiene 40 caracteres o más, porque `idealTP` y F07 llevan allí el texto entero
del Archivo 1, que PS recortaba. Salen 28 líneas; 20 están en los dos sitios. Las otras 8 no se
mudaron:
- `main`, la Current Feature de `main` y las dos «— ninguna desde el Archivo 40» las cambió la
  apertura (Archivo 41);
- las dos cabeceras de «Technical Debt» y «Reglas vivas» siguen en PS, con su puntero añadido;
- `### Decisions and Rationale` y `### Known Issues` son `## ` en el runbook.

En la primera pasada la comprobación encontró dos líneas de HISTORIA que no eran literales: les
había antepuesto «(de «…»)». Se corrigieron antes del commit, con el origen en la línea de la
condición. La primera versión del guion comparaba por subcadena y daba por bueno `main`, que casa
con cualquier texto (hallazgo m2 del revisor); la de ahora compara líneas enteras.

## 7 · Tamaño final de PROJECT_STATE

**21.910 bytes** (`wc -c`; `main`: 24.135; tope del test: 25.000; objetivo: 22.000). Quedan 3.090
bytes libres hasta el tope. Con las líneas preparadas para el cierre quedaría en **22.359**.

## 8 · Líneas preparadas para el commit del contrato de la orden de cierre

Simuladas en memoria con `docs/validation/anexos/PREVIA-SESION-5/simular_cierre.py <raiz>` (como
el de VISOR-CONSTRUCCION y el de EA-CONEXION, con sus propias sustituciones):
`test_hoja_de_ruta.py` a, b y c sin problemas (`a: []`, `b: []`, `c: []`), y los cuatro de
`test_project_state.py` pasan. **PROJECT_STATE quedaría en 22.359 bytes.** El simulador lleva el
texto exacto; aquí, lo que dice:

- **PROJECT_STATE, V:** la hoja de preguntas lleva los recuadros de corrección de S-7, S-12, S-13 y
  S-15 (`trabajo/previa-sesion-5`), y la primera parte de S-12 decide si RN-005 sigue o se reabre.
- **Technical Debt, una línea:** el docstring de `tests/contract/test_tramos_fuente.py:5` cita
  «PROJECT_STATE, Decisions and Rationale, 2026-09-04», que vive desde esta rama en
  `DECISIONES-DE-PROCESO.md`; lo corrige la próxima rama que toque `tests/`.
- **Ninguna letra pasa a HECHA**: V se cumple con la sesión y su activación, y A.3 espera a la
  confirmación de marzo.
- **Para la orden de cierre** (respuesta, punto 0): el «Para Aleks» de S-12 en el encargo («opera
  las dos: eso es (a)») era un error del consultor; el bot no opera ninguno de los dos dibujos.
- **ERRORES-RECURRENTES**, la fila de la rama: la caja orientada al revés en tres preguntas del
  barrido (S-7, S-12 y S-13) y un «Para Aleks» que afirmaba lo que el código no hace. Es el patrón
  «nada afirma más de lo que su cita sostiene», aplicado a la geometría: se comprueba la caja de una
  compra contra `orden_stop_punto` y `caja_bloque`, y el lado contra RN-005 en el código, antes de
  dar una pregunta por buena. Con lo que encuentre el revisor.

## 9 · La CI

La rama no toca hooks, rutas, código ni tests. Solo cambian documentos y dos guiones de anexo que
no corre ninguna herramienta: `git diff main --stat` (abajo, en la entrega) da `PROJECT_STATE.md`,
`contrato.yaml`, `docs/encargos/trabajo-previa-sesion-5.md`, `docs/plan/HOJA-DE-RUTA.md`,
`docs/runbooks/` (`DECISIONES-DE-PROCESO.md` nuevo, `MIRAR-EL-MATERIAL.md`, `README.md`,
`RITUAL.md` y `SESION-DE-PREGUNTAS.md`), `docs/sesion-5/PREGUNTAS.md`, `docs/state/HISTORIA.md`,
`docs/validation/HOLDOUT-EXPOSICIONES.md`, `docs/validation/PREVIA-SESION-5.md` y
`docs/validation/anexos/PREVIA-SESION-5/` (`comprobar_movido.py` y `simular_cierre.py`). La CI de
Linux por `fix/` no hace falta.

**Negativas de la guardia después de la fase 0**, las tres resueltas con la forma que proponía su
mensaje: `wc -c` y `pytest` en el mismo comando (los partí en dos llamadas); un `sed -n` detrás de
la tubería de un guion (lo cambié por `grep`, que la guardia admite); y `git add` con
`contrato_rama.py` en el mismo comando, en la entrega (dos llamadas).

## 10 · El encargo, punto por punto

| # | Requisito (encargo y respuesta a la PARADA) | Estado | Evidencia |
|---|---|---|---|
| 0.1 | Base: `main` 24b7cba, `origin/main`, el tag, ninguna otra rama | Hecho | §0, tabla |
| 0.2 | La CI de 24b7cba con `gh`, a mano y una vez | Hecho | §0: `gh run view 39705799089` → success |
| 0.3 | Abrir con `abrir-rama`, tramo R4, informe `PREVIA-SESION-5.md`, rutas permitidas | Hecho, ampliado | 05a4eb0; `contrato.yaml` permite `docs/runbooks/` entero (los runbooks que reciben texto) y, ampliado después, `HOLDOUT-EXPOSICIONES.md` (fase 0) y `docs/validation/anexos/PREVIA-SESION-5/` (simulador) |
| 0.4 | Skills `fase-cero` con `auditor-encargo`, `entregar-rama`; `/model` | Hecho | §2 (auditor); este recorrido; `/model` lo revisa Aleks en su terminal |
| 0.5 | Negativas de la guardia: PARADA salvo seguir su forma, declarándolo | Hecho | seis negativas, las seis con la forma que proponía su mensaje: §0 (tres) y §9 (tres) |
| 1 | Rama solo de documentos, que cierre el jueves 22 | Hecho | §9: ni código, ni tests, ni hooks; lista para revisión el 2026-10-21 |
| 2.1 | Verificar la orientación con `orden_stop_punto` y `caja_bloque` | Hecho | §1: `parametros.yaml:631-632` y `:652-654` |
| 2.2 | Recuadro de S-7 con el texto del encargo | Hecho, ampliado por la respuesta (1) | recuadro antes de S-7; esquema sustituido (§5) |
| 2.3 | Recuadro de S-12 con el texto del encargo | Hecho de otra forma | la respuesta (0) lo sustituye por dos partes; desviación 1 de §5 (la segunda parte con el lado (b)) |
| 2.4 | El cuerpo de PREGUNTAS.md intacto | Hecho | `git diff --numstat` → `105 0` |
| 2.5 | Comprobar S-13, S-16 y S-17 | Hecho | §1, tabla: S-13 al revés (recuadro, respuesta 2), S-16 bien, S-17 no nombra la caja |
| 3.1 | El paso 6 del runbook remite a la regla 2 | Hecho | `SESION-DE-PREGUNTAS.md`, paso 6 de «Antes»; §3 |
| 3.2 | La línea del paso 1 con 2026-10-23; si True, PARADA | Hecho | `False` (§3); declarado en HOLDOUT-EXPOSICIONES, 2026-10-21 |
| 3.3 | A.3 con una línea de Estado y la fecha; no HECHA; la fecha no va a PS | Hecho | `HOJA-DE-RUTA.md`, A.3; PS no la nombra |
| 4.1 | Fase 0: lista, destinos y tamaño; PARADA si no llega sin tocar nada vivo | Hecho | §4; PARADA (0402698) |
| 4.2 | Solo entradas enteras, nada resumido ni perdido | Hecho | §6; `comprobar_movido.py`: 20 líneas en su runbook y en HISTORIA, las 8 restantes explicadas |
| 4.3 | 22.000 bytes o menos | Hecho | 21.910 (§7) |
| 4.4 | Los tests de PS siguen pasando | Hecho | `make check` (abajo); `state check` OK; `test_project_state`, `test_hoja_de_ruta`, `test_kit` en verde |
| 5 | Lo que NO cambia (motor, spec, parametros, ambigüedades, feedback, cases, holdout, `hoja_preguntas.py`, guardias, `.claude/`, Makefile) | Hecho | §9: `git diff main --stat`; `contrato_rama.py` en verde con todo eso protegido |
| 6.1 | Informe: encargo frente a lo hecho, desviaciones, lo movido, tamaño, líneas preparadas, simuladas | Hecho | §5 a §8 y esta tabla |
| 6.2 | La línea PICO DE MEMORIA de cada `make check` | Hecho | §0, §5 y «Los make check de la entrega» |
| 6.3 | Revisor opus, dos ejes, con las comprobaciones añadidas | Hecho | al final |
| 6.4 | CI: decir que no toca hooks, rutas ni código, con la lista | Hecho | §9 |
| R0 | S-12 en dos partes, citas enfrentadas, «Para Aleks» corregido; el error del consultor al informe y a la orden de cierre | Hecho, con la desviación 1 | recuadro de S-12; §5; §8 |
| R0b | S-15: el lado se pregunta en S-12 | Hecho | recuadro de S-15 |
| R1 | S-7: esquema con el 0 arriba y tres mínimos rotulados | Hecho | recuadro de S-7 |
| R2 | S-13: «baja mucho (la caja se hace muy grande)» | Hecho | recuadro de S-13 |
| R3 | Conjunto A y Reglas vivas a `DECISIONES-DE-PROCESO.md`, enteras y en orden; punteros; BUSCAR se queda; PARADA si un test exige texto en PS | Hecho, con las desviaciones 3 a 5 | §5, §6; ningún test lo exige (§5, punto 3) |
| R4 | S-9 y S-10 no dan por bueno ningún lado | Hecho | §5, «Punto 4» |
| R5 | Revisor con la comprobación de S-7, S-12, S-13 y S-15 contra RN-005, `orden_stop_punto` y `caja_bloque` | Hecho | al final |

## Los make check de la entrega

- Commit 45fcf82 (la respuesta aplicada): exit 0, `2729 passed in 955.41s`, ningún `failed`,
  `SELLO: make check en verde sobre el arbol 265118d76638d6c44af412b99db1d156fa1b5ad4`,
  `PICO DE MEMORIA de make check: 298 MiB en `test` (suma de sus procesos, memoria comprometida, Windows; el mayor proceso, 288 MiB)`.
- El último, el que sella este informe con los arreglos del revisor: su resultado (passed, SELLO y
  PICO DE MEMORIA) no puede ir dentro del árbol que sella; va en el mensaje de su commit.

## 11 · Informe del auditor (fase 0), entero

El subagente `auditor-encargo`, 2026-10-21, sobre el encargo antes de la fase 0. Pegado tal cual (sin
la sangría que añade el entorno); no cita ningún tramo no citable.

> ## Auditoría del encargo · trabajo/previa-sesion-5 · 2026-10-21
>
> Resumen: 40 afirmaciones; 24 correctas, 3 incorrectas y 13 con matiz. 8 herencias no recogidas.
>
> He leído el encargo en `C:\Users\USER\Desktop\Bot v3\docs\encargos\trabajo-previa-sesion-5.md`. Rama `trabajo/previa-sesion-5`, solo lectura. No he abierto material protegido ni he ejecutado ningún comando del encargo.
>
> ### Afirmaciones
> | # | Afirmación (literal del encargo) | Veredicto | Evidencia |
> |---|---|---|---|
> | 1 | «main 24b7cba, el commit de estado sobre el merge e76f829 (stable/F37x-ea-conexion)» | CORRECTA | `git rev-parse origin/main` da 24b7cba2…. `stable/F37x-ea-conexion^{commit}` da e76f829…. Solo existen `main` y la rama |
> | 2 | «NA:V, hoja de ruta R4.1 y A.3, tramo R4» | CORRECTA | `HOJA-DE-RUTA.md:195-199` (R4.1 lleva `NA:V`); `:401-406` (A.3); `PROJECT_STATE.md:32` «F. V.»; `contrato.yaml:4` dice `tramo: R4` (`contrato_rama.py:123-124` acepta el id) |
> | 3 | Skills abrir-rama, fase-cero (con auditor-encargo) y entregar-rama | CORRECTA | Existen en `.claude/skills/` y `.claude/agents/` |
> | 4 | La regla nueva del consultor del 2026-10-21 sobre las negativas de la guardia | CORRECTA | `HISTORIA.md:11140` y `:11153-11154` |
> | 5 | «la sesión 5 … es el viernes 23 de octubre … cerrar el jueves 22» | CORRECTA | El 2026-10-23 cae en viernes (calculado) |
> | 6 | «PROJECT_STATE, que está en 24.135 bytes (tope 25.000)» | CORRECTA, con matiz | `git show main:PROJECT_STATE.md \| wc -c` da 24135; el tope es `TOPE_BYTES = 25_000` en `tests/unit/test_project_state.py:21` y `:52`. En la rama ya pesa 24.277 |
> | 7 | «Es una rama solo de documentos: no cambia el motor, la spec…» | CORRECTA | `contrato.yaml:13-26` protege `src/`, `knowledge/`, `scripts/`, `tests/`, `.claude/` y el Makefile |
> | 8 | «En una compra, el 0 … es el punto (… arriba) y el 1 es el otro extremo, del lado del stop (abajo); en una venta, al revés» | CORRECTA | `parametros.yaml:631-632` (`ultimo_pivote_m1`: «un BAJO en una venta») y `:653-654` (`r6`: «el extremo opuesto -la maxima en una venta-») |
> | 9 | «S-7 preguntaba "desde dónde trazas el 0"» | CORRECTA | `docs/sesion-5/PREGUNTAS.md:254` |
> | 10 | «con opciones que son las del 1 (A-48: r1, r4 y r6 de caja_bloque)» | MATIZ | `PREGUNTAS.md:255-257`: (a) es r1 y (b) es r4, pero (c) es «depende, ¿de qué?». Ninguna opción es r6 |
> | 11 | «S-12 decía, de una compra, "el 1 queda por encima y el 0 por debajo", que es imposible» | CORRECTA | `PREGUNTAS.md:375-377` |
> | 12 | Su fuente §0.e.6 «decía "el 0 de este lado y el 1 del otro"» | MATIZ | El literal es «el 0 queda de este lado y el 1 del otro», y el primer dibujo es «la caja entera queda al otro lado del nivel tomado» (`ACTIVAR-SESION-04.md:324-327`). La cita del encargo está recortada |
> | 13 | «su propia línea "Para Aleks" habla del 0 por encima» | CORRECTA en lo literal | `PREGUNTAS.md:387-389`. Pero esa línea contradice al código (fila 20) |
> | 14 | «PREGUNTAS.md está cerrado en main» | CORRECTA | Está en main desde el cierre de barrido-sesion-5 (`HISTORIA.md:10889`, `:10912-10917`) |
> | 15 | «lleva un recuadro de corrección … y su cuerpo queda intacto» (como régimen) | MATIZ | La regla de recuadros de `CLAUDE.md` («Regimenes de cambio») cubre solo `docs/validation/`. `docs/sesion-N/` no tiene régimen escrito y `docs/sesion-4/` no tiene ningún recuadro. Es una decisión del consultor por analogía, no una regla, y conviene decirlo así en el informe |
> | 16 | S-7: «(a) = r1, (b) = r4, (c) = r6» | CORRECTA | `parametros.yaml:653-656` |
> | 17 | «r6 (el valor de hoy de caja_bloque)» | CORRECTA | `parametros.yaml:661-663`: `valor: r6`, DEFAULT_AMBIGUOUS, A-48 |
> | 18 | «último alto de M1 = ultimo_pivote_m1, el valor de hoy; el punto de la vela de la toma = referencia_de_la_toma» | CORRECTA | `parametros.yaml:628-641` |
> | 19 | «la de la vela abierta es A-49» | CORRECTA | `PROJECT_STATE.md:87`; `parametros.yaml:684-689` |
> | 20 | S-12, «Para Aleks»: «hoy el bot mira solo el 0 (RN-005) y opera las dos: eso es (a)» | **INCORRECTA** | En alcista la toma es un BAJO y la entrada una COMPRA (`engine/zonas.py:115-116`). Hay ruido si `e.entrada > toma["nivel"]` en compra (`zonas.py:539`), y RN-005 prohíbe abrir (`strategy_spec.yaml:1216-1219`, `:1244-1251`). La descripción del predicado dice que en alcista el ruido está «por encima» (`strategy_spec.yaml:198-205`). A-50 lo pone con todas las letras: «una compra cuyo 0 queda por encima del nivel … es ruido aunque el 1 quede del lado del trader» (`ambiguedades.yaml:1505-1508`). Resultado: en los dos dibujos del recuadro el 0 queda por encima de la línea, así que el bot no opera **ninguno**. No hace ni (a) ni (b) |
> | 21 | El dibujo de S-12: en una compra, «la caja entera queda por encima de la línea» del bajo tomado como lado bueno, y (b) «tiene que quedar por encima» | MATIZ grave | RN-005 y A-50 ponen el lado del trader en compra **por debajo** del bajo tomado (las mismas citas de la fila 20). Lo sostiene solo `ev-v9-004919-c6bfb3ee` («en una compra … tiene que desarrollarse todo por encima», `knowledge/evidence/v9/ev-v9-004919-c6bfb3ee.yaml:9-10`), y A-50 lo cita junto a los ítems de RN-005 con `contradiccion: null` (`ambiguedades.yaml:1515-1522`). El repo se contradice a sí mismo, y el recuadro hereda un lado que RN-005 llama ruido |
> | 22 | «S-13, S-16 y S-17 la nombran» | MATIZ | S-13 (`:414`) y S-16 (`:465-482`) nombran el 0 y el 1. S-17 (`:489-520`) no nombra la caja ni el 0 o el 1. Además, S-13 `:414` dice «Si el 1 de la caja sube mucho» sobre una compra (`:404`). Con r6 el 1 de una compra es un mínimo (`parametros.yaml:653-654`), que en una ventana creciente no sube: posible orientación al revés, y la sesión tiene que mirarla |
> | 23 | Runbook, paso 6 de «Antes» (hacia :76): «el día tiene que ser de abril o de agosto» | CORRECTA | `docs/runbooks/SESION-DE-PREGUNTAS.md:74-78`, la frase en `:76` |
> | 24 | Regla 2: «abril, julio del 1 al 17, agosto y enero del 2 al 30» | CORRECTA | `SESION-DE-PREGUNTAS.md:21-23`; ADR-0078:7 y ADR-0079:7 |
> | 25 | «Es un runbook: se edita directamente» | CORRECTA | `CLAUDE.md` no da régimen a `docs/runbooks/`, y `contrato.yaml:8` lo permite |
> | 26 | La línea del paso 1 «imprime solo True o False» | CORRECTA | `SESION-DE-PREGUNTAS.md:48-56`; `casos_ocultos` existe en `cases/holdout.py:456` |
> | 27 | «la confirmación de marzo sigue pendiente, así que A.3 no pasa a HECHA» | CORRECTA | Hecho cuando de A.3: «la confirmación está registrada y la sesión 5 tiene fecha» (`HOJA-DE-RUTA.md:406`). Lo pendiente: `PROJECT_STATE.md:67` (heredado 2) y `PREGUNTAS.md:696-698` |
> | 28 | «solo se mueven entradas enteras, nunca se resumen ni se pierde texto» | CORRECTA | `docs/state/README.md:71-75` |
> | 29 | Lo que sale «deja una línea con el puntero» | **INCORRECTA** | README: «En `PROJECT_STATE.md` no queda ni un resumen» (`:75`), y para las HECHAS «no queda ni el resumen» (`:37`). plataforma-adelantada no dejó ningún puntero en PS: el puntero fue a la hoja de ruta, en lugar del `HER:n` (`PLATAFORMA-ADELANTADA.md:456`, `:533-549`). El arranque con puntero de dieta-y-skills (`DIETA-Y-SKILLS.md:110-112`) es anterior al criterio del 2026-10-08 |
> | 30 | «como lo hicieron trabajo/dieta-y-skills y trabajo/plataforma-adelantada» | MATIZ | Las dos lo hicieron de forma distinta (fila 29). El criterio vigente nace en `trabajo/adelgazar-estado` (`README.md:58-60`), que el encargo no nombra |
> | 31 | Destino: «un runbook, ERRORES-RECURRENTES o el informe que la originó, si su texto ya está allí entero» | MATIZ | La condición (b) cuenta la Next Action, `CLAUDE.md` o un runbook, no un informe; un informe solo entra por (d) (`README.md:65-69`). El texto literal va siempre a HISTORIA con su bloque (`:72-75`). Llevar texto a un runbook para que valga (b) fue la opción 6a, con orden expresa del consultor (`PLATAFORMA-ADELANTADA.md:450-456`) |
> | 32 | «o sale a HISTORIA bajo "# Next Action HECHA"» | MATIZ | Ese encabezado es solo para letras de la Next Action (`README.md:36`; `test_hoja_de_ruta.py:61` lee la letra). Technical Debt y los heredados usan `# Technical Debt PAGADA/RECLASIFICADA`, `# Pendiente heredado SALE` y `# Regla viva SUSTITUIDA` (`README.md:73-75`). Y un cambio de la Next Action va en el commit del contrato de la orden de cierre, no en las fases (`README.md:34-42`, `:77-80`) |
> | 33 | Las deudas en mayúsculas de septiembre «son reglas o lecciones y no deudas abiertas (por ejemplo "BUSCAR EN EL CORPUS…")» | **INCORRECTA** | plataforma-adelantada (2026-10-18) las revisó una a una y se quedaron todas salvo tres (`PLATAFORMA-ADELANTADA.md:221-260`). La del ejemplo está «Abierta» (`:243-244`): el campo que pedía su condición (`HISTORIA.md:565`) no existe. `ADELGAZAR-ESTADO.md:114` también la dejó |
> | 34 | «y los pendientes heredados» como candidatos | MATIZ | Los que quedan (2, 6, 7, 8, 9, 10 y 27) ya se revisaron y se quedaron con su motivo (`PLATAFORMA-ADELANTADA.md:189-215`). El consultor dijo «No busques más recortes» (`:781`) |
> | 35 | «objetivo: 22.000 bytes o menos» | MATIZ | La pasada completa anterior se quedó en 22.517 (`PLATAFORMA-ADELANTADA.md:583`). Desde entonces EA-CONEXION añadió 5 líneas de Technical Debt (`HISTORIA.md:11176`). Lo probable es la PARADA, que el propio encargo prevé |
> | 36 | Los tests que vigilan PS: test_project_state, test_kit (la tabla), test_hoja_de_ruta y state check | CORRECTA | `CLAUDE.md`; `test_hoja_de_ruta.py:9-10`; `cli.py:2922-2924` |
> | 37 | «Los informes cerrados de docs/validation/ solo reciben recuadros» | CORRECTA, con matiz | `CLAUDE.md`, «Regimenes de cambio». Pero `contrato.yaml:6` solo permite `PREVIA-SESION-5.md` dentro de `docs/validation/`: hoy no cabe ningún recuadro ni ninguna fila de exposiciones (herencia 3) |
> | 38 | «como simular_cierre.py de VISOR-CONSTRUCCION» | CORRECTA, con matiz | `docs/validation/anexos/VISOR-CONSTRUCCION/simular_cierre.py:1-12` (a, b y c de test_hoja_de_ruta y las cuatro de test_project_state, en memoria). Sus sustituciones son las de esa rama (`:129`), así que hay que escribir uno propio, como hizo EA-CONEXION (`EA-CONEXION.md:769`). No cubre test_kit ni state check |
> | 39 | «CI: si la rama no toca hooks, rutas ni código, dilo con la lista de ficheros» | CORRECTA | Es lo que hizo barrido-sesion-5 (`HISTORIA.md:10934-10935`) |
> | 40 | «La fecha no va a PROJECT_STATE» | CORRECTA | Ninguna regla la pide allí; A.3 es su sitio (`HOJA-DE-RUTA.md:403`) |
>
> ### Lo que el repo pide y el encargo no recoge
> | # | Qué | Dónde lo pide | Evidencia |
> |---|---|---|---|
> | 1 | **A.4, la copia de seguridad: fecha límite «antes de grabar la próxima sesión».** R4.1 y V dependen de ella, y sigue INCOMPLETA | HOJA-DE-RUTA, PROJECT_STATE, PREGUNTAS | `HOJA-DE-RUTA.md:408-414`, `:217-219`, `:532`; `PROJECT_STATE.md:54` y `:146`; `PREGUNTAS.md:8-9` |
> | 2 | La línea de G.2 sobre el paso 6 («dice todavía "abril o agosto"») tiene que salir o cambiar en las líneas preparadas para el commit del contrato | G.2 | `HOJA-DE-RUTA.md:467-468`; entró con el cierre del barrido (`HISTORIA.md:10924-10925`) |
> | 3 | Declarar en HOLDOUT-EXPOSICIONES, el mismo día, la consulta de `casos_ocultos` del paso 1. El barrido la declaró tras el hallazgo a1 del revisor. Hoy el contrato no permite ese fichero | CLAUDE.md (ADR-0021 §4); precedente | `HOLDOUT-EXPOSICIONES.md:64`; `PREGUNTAS.md:60-63`; `contrato.yaml:5-12` |
> | 4 | Si sale un heredado de PS, su `HER:n` sale de la hoja en el mismo commit, o falla test_hoja_de_ruta (b). Y no pueden salir sin dejar al vacío a quien los cita: la Technical Debt de la copia de seguridad (A.4 la cita por su texto) y las condiciones previas que nombra G | test_hoja_de_ruta; precedente | `test_hoja_de_ruta.py:165`; `PLATAFORMA-ADELANTADA.md:456`, `:249-252`, `:263-264`; `HOJA-DE-RUTA.md:409`; `PROJECT_STATE.md:40` |
> | 5 | Las líneas «Esquema inventado» de S-7 («el punto de breaker es el mínimo de la última roja», en una compra) y de S-12, y «Si la última vela roja es muy pequeña, ¿pones el 0 en ella igual?», tienen la caja al revés. El texto corregido del encargo no las sustituye, y el esquema se dibuja para el trader | PREGUNTAS (cómo se leen) | `PREGUNTAS.md:252-253`, `:261`, `:375-377`; `:38-39` (los esquemas se enseñan) |
> | 6 | Los textos de los códigos entran en `CODIGOS_DE_SESION_TEXTO["05"]` con la ingesta: el recuadro tiene que decir que S-7 y S-12 se toman de él y no del cuerpo | PREGUNTAS | `PREGUNTAS.md:22-24` |
> | 7 | Todo cambio de la Next Action (incluida una letra HECHA) va en el commit del contrato de la orden de cierre, no en las fases | README (punto Y) | `docs/state/README.md:34-42`, `:77-80` |
> | 8 | La contradicción entre RN-005 (en compra, por encima es ruido) y `ev-v9-004919-c6bfb3ee` (en compra, todo por encima), que A-50 junta sin marcarla. Decide qué dibujo es el correcto en S-12 | A-50 | `ambiguedades.yaml:1491-1522`; `strategy_spec.yaml:198-205` |
>
> ### Comandos del encargo
> | # | Comando | ¿Existe y se ejecuta así? | Evidencia |
> |---|---|---|---|
> | 1 | La línea del paso 1: `uv run python -c "from pathlib import Path; from botsito.cases.holdout import casos_ocultos; print(any('<AAAA-MM-DD>' in c for c in casos_ocultos(Path('.'))))"` | Sí | `SESION-DE-PREGUNTAS.md:53`; `cases/holdout.py:456` |
> | 2 | `gh run view 39705799089 …`, a mano y una vez | Fuera de botsito; la sesión ya lo ejecutó | `PREVIA-SESION-5.md:18` |
> | 3 | `uv run python scripts/contrato_rama.py` | Sí | `contrato.yaml:28`; `scripts/contrato_rama.py` |
> | 4 | `make check > make-check.log 2>&1` | Sí | `CLAUDE.md` |
> | 5 | state check (`uv run botsito state check`) | Sí | `cli.py:2922-2924` |
> | 6 | simular_cierre como el de VISOR-CONSTRUCCION (`uv run python <guion> <raiz>`) | Existe, pero con las sustituciones de su rama: hace falta uno propio | `anexos/VISOR-CONSTRUCCION/simular_cierre.py:12`, `:20`, `:129` |
>
> ### Lo que no pude comprobar
> - La CI de main del run 39705799089: no consulto `gh`. El informe de la sesión trae la salida (`PREVIA-SESION-5.md:18`).
> - Si 22.000 bytes se alcanzan sin tocar nada vivo. Hace falta la lista de la fase 0; el precedente apunta a que no (fila 35).
> - El sentido real de v9 0:49:19 (compra o venta): no leo la transcripción, solo el ítem de evidencia.
> - Si el esquema de S-16 («una roja pequeña que cierra en el 0», en una compra) es coherente con un punto que es un alto de M1. No veo el 0 y el 1 cambiados, pero no lo afirmo.
> - La salida de la línea del paso 1 para el 2026-10-23: no la ejecuto, es un paso de la sesión.
>
> ### Lo más grave
> Hay dos cosas. La primera: el recuadro de S-12 se escribiría sobre algo falso. Su «Para Aleks» dice que el bot mira solo el 0 y opera los dos dibujos (a). Según el código, en una compra el bot llama ruido a todo 0 por encima del bajo tomado (`zonas.py:115-116` y `:539`; `ambiguedades.yaml:1505-1508`), así que no opera ninguno de los dos dibujos, que tienen el 0 por encima. Y el lado bueno que dibuja la pregunta («la caja entera por encima») es el que RN-005 llama ruido. Lo sostiene un único ítem, `ev-v9-004919`, que el repo no marca como contradicción. Antes de fijar el texto, el consultor tiene que decidir de qué lado del nivel opera el trader en una compra. Si no, el recuadro le pregunta al trader por el lado contrario al que sostiene la spec, y la respuesta no se podrá leer contra A-50.
>
> La segunda: el adelgazamiento de PROJECT_STATE va contra su propio criterio. Pide dejar «una línea con el puntero» y mandar a HISTORIA bajo «# Next Action HECHA» lo que no es de la Next Action, cuando `docs/state/README.md:37`, `:72-75` y `:77-80` lo prohíben o lo dejan para el commit del contrato. Además, su ejemplo de deuda «que no es deuda» es una deuda abierta que dos ramas recientes revisaron y dejaron (`PLATAFORMA-ADELANTADA.md:243-244`; `ADELGAZAR-ESTADO.md:114`).
>
> A eso se suma lo que el encargo no recoge. Los esquemas de S-7 y S-12 siguen al revés en el cuerpo que se dibuja. La copia de seguridad A.4 es condición para grabar el viernes. Y el contrato no permite declarar la exposición de `casos_ocultos` en HOLDOUT-EXPOSICIONES.

## 12 · Informe del revisor, entero

El subagente `revisor` (opus), 2026-10-21, sobre HEAD 45fcf82 más el informe estadiado (§10 y el
Estado). Pegado tal cual (sin la sangría que añade el entorno); no cita ningún tramo no citable.

> ## Informe del revisor · trabajo/previa-sesion-5 · 2026-10-21
>
> Revisé el árbol estadiado: HEAD 45fcf82 más `docs/validation/PREVIA-SESION-5.md` estadiado (la tabla de §10 y el Estado). Base: 24b7cba.
>
> **Veredicto:** no hay nada que bloquee. Hay 4 hallazgos que importan (1 en el eje a y 3 en el b) y 3 menores. Los cuatro recuadros de la caja (S-7, S-12, S-13 y S-15) están bien orientados según RN-005, `orden_stop_punto` y `caja_bloque`. La desviación 1 es correcta geométricamente.
>
> ### Eje (a) · Reglas de la casa
> Resumen: 0 bloquea, 1 importa, 0 menor.
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | a1 | importa | A la fila nueva de `HOLDOUT-EXPOSICIONES.md` (2026-10-21) le faltan tres de las cinco columnas de la tabla: «Particiones», «Quien» y «¿Quema?». La exposición está declarada el mismo día (ADR-0021 §4 se cumple), pero la fila acaba en la segunda celda. | `docs/validation/HOLDOUT-EXPOSICIONES.md:15`: la cabecera es `\| Fecha \| Que se vio \| Particiones \| Quien \| ¿Quema? \|`. En `git diff main...HEAD -- docs/validation/HOLDOUT-EXPOSICIONES.md`, la fila añadida es `\| 2026-10-21 \| **Fase 0 de la rama …** … ni febrero. \|`: solo dos celdas. Las filas anteriores llevan, por ejemplo, `\| ninguna \| la sesion, con el encargo … \| No: … \|`. |
>
> **Comprobado sin hallazgos:**
> - **Contrato.** `uv run python scripts/contrato_rama.py` da `CONTRATO: 15 ficheros dentro del contrato de trabajo/previa-sesion-5 (riesgo bajo, artefacto docs/validation/PREVIA-SESION-5.md, tramo 'R4', 2 comprobaciones para el revisor)` y sale con 0.
> - **`make check`.** No lo ejecuté, porque escribe. Su evidencia está en `make-check.log`:
>   - `2729 passed in 955.41s`;
>   - `SELLO: make check en verde sobre el arbol 265118d76638d6c44af412b99db1d156fa1b5ad4`;
>   - `PICO DE MEMORIA … 298 MiB`.
>   - El sello coincide con `git rev-parse HEAD^{tree}` (= 265118d7…). El cambio estadiado del informe todavía no tiene sello.
> - **Trailers `Fuente:`.** No aplica: la rama no toca `knowledge/spec/` ni `knowledge/cases/` (`git diff --name-status main...HEAD`).
> - **Holdout y material.** No se toca nada de `knowledge/cases/holdout/`, ni libros, ni imágenes, ni fotogramas, ni crudas. La consulta a `casos_ocultos` está declarada (con el defecto de a1).
> - **Regímenes de cambio.** No hay cambios en `knowledge/evidence/`, `knowledge/feedback/`, `data/manifests/` ni en el corpus. `HISTORIA.md` solo crece: 232 líneas añadidas y 0 borradas.
> - **Ambigüedades y ADR.** No cambian.
> - **Informes cerrados.** El único `docs/validation/` de main que cambia es `HOLDOUT-EXPOSICIONES.md`, que es un registro y recibe solo una fila añadida (`1 0`).
> - **Tres guardias de una `cita`.** No aplica.
> - **Cifras.** No hay código.
> - **Tres citas del informe, contrastadas con su fuente, correctas:**
>   - `parametros.yaml:631` (`un BAJO en una`), `:652-653` (`con el 0 en el punto`, `la maxima en una venta`) y `:662` (`valor: r6`);
>   - `zonas.py:115-116` y `:537-539` (`ruido = e.entrada > toma["nivel"] if e.lado == COMPRA …`);
>   - `strategy_spec.yaml:203`, y el comentario de A-50 en `ambiguedades.yaml:1505-1508`: «una compra cuyo 0 queda por encima del nivel … es ruido aunque el 1 quede del lado del trader».
> - **Citas de las dos evidencias de S-12.** Las de `ev-v1-001306-f98e12e9` y `ev-v9-004919-c6bfb3ee` en los recuadros son literales de su `cita_literal`.
> - **Punto 10.** No aplica: no hay ítems de evidencia nuevos.
>
> ### Eje (b) · Encargo
> Resumen: 0 bloquea, 3 importa, 3 menor. Requisitos: 22 hechos, 1 parcial, 0 no hechos.
>
> | # | Requisito | Estado | Evidencia |
> |---|---|---|---|
> | 1 | Base, tag, CI y ninguna otra rama | Hecho | informe §0, tabla. La CI no la reconsulté. |
> | 2 | Abrir con abrir-rama: tramo R4, informe y rutas | Hecho | `contrato.yaml:1-28` |
> | 3 | Negativas de la guardia declaradas | Hecho | informe §0 y §9 (cinco) |
> | 4 | S-7 y S-12 verificadas contra parametros.yaml | Hecho | informe §1; líneas comprobadas |
> | 5 | Recuadro S-7 con el texto del encargo | Hecho | `PREGUNTAS.md:240-271`. El título, «Lo que todavía no sabemos», la pregunta, «Para precisar», «Para confirmar» y «Para Aleks» coinciden palabra por palabra con el encargo (líneas 23-24). |
> | 6 | Recuadro S-12 | Hecho de otra forma (lo declara la respuesta, punto 0) | `PREGUNTAS.md:402-452` |
> | 7 | El cuerpo de PREGUNTAS.md intacto | Hecho | `git diff --numstat main...HEAD -- docs/sesion-5/PREGUNTAS.md`: `105 0` |
> | 8 | S-13, S-16 y S-17 comprobadas | Hecho | informe §1. Confirmo que S-16 (`:575-578`, «por encima del 0 en una compra») está bien. |
> | 9 | Paso 6 del runbook remite a la regla 2 | Hecho | `SESION-DE-PREGUNTAS.md:76-77`, que concuerda con `:21` |
> | 10 | Línea del paso 1 con 2026-10-23 → False | Hecho, según el informe | No la reejecuté (ver «Lo que no pude comprobar»). |
> | 11 | A.3 con Estado y fecha, sin HECHA; la fecha no va a PS | Hecho | `HOJA-DE-RUTA.md:407-409`. `grep -c "2026-10-23\|23 de octubre" PROJECT_STATE.md` → `0`. |
> | 12 | Fase 0: lista, destinos, tamaño y PARADA | Hecho | informe §4 y «Lo que necesito que decidas» |
> | 13 | Entradas enteras, nada resumido ni perdido | Hecho | `comprobar_movido.py`: 21 OK; los 7 FALTA son cabeceras o líneas de apertura. Lo contrasté con el diff de PS, la cola de HISTORIA (`:11384-11424`) y los tres runbooks. |
> | 14 | idealTP y F07 con el texto entero del Archivo 1 | Hecho | `HISTORIA.md:564` = `MIRAR-EL-MATERIAL.md`, viñeta idealTP. `HISTORIA.md:589` = `DECISIONES-DE-PROCESO.md`, última viñeta. Idénticos. |
> | 15 | PS en 22.000 bytes o menos | Hecho | `wc -c PROJECT_STATE.md` → `21805` |
> | 16 | Los tests de PS pasan | Hecho | `make-check.log` (2729 passed). El simulador los pasa sobre el texto simulado. |
> | 17 | Lo que NO cambia (§5 del encargo) | Hecho | `git diff --name-status main...HEAD`: solo docs, `contrato.yaml` y dos guiones de anexo. Nada en src, knowledge, scripts, tests, .claude ni Makefile. |
> | 18 | Líneas preparadas, simuladas | Hecho | `simular_cierre.py`: `a: []`, `b: []`, `c: []`, los cuatro tests de PS pasan, `PROJECT_STATE simulado: 22254 bytes`. Escribe solo en un `TemporaryDirectory`. |
> | 19 | PICO DE MEMORIA de cada make check | Hecho | informe:26, :217 y :408 |
> | 20 | Respuesta 0 (S-12 en dos partes) y 0b (S-15) | Hecho, con h1 | `PREGUNTAS.md:402-452` y `:538-546` |
> | 21 | Respuesta 1 (esquema de S-7) y 2 (S-13 «baja mucho») | Hecho | `PREGUNTAS.md:252-256` y `:478-484` |
> | 22 | Respuesta 3: DECISIONES-DE-PROCESO.md en el mismo orden, punteros, BUSCAR se queda | Hecho, con h2 | El orden es Change Regimes → Things → Decisions → Known Issues, igual que el PS de main. BUSCAR sigue en PS. |
> | 23 | Respuesta 4: S-9 y S-10 | Hecho | `PREGUNTAS.md:361-362`: S-10 solo dice «el precio vuelve por encima», del precio y no de la caja. La copia de la respuesta es idéntica en el informe y en el encargo (`diff` → IGUALES). |
> | 24 | Auditor pegado entero en la entrega | Parcial | h3 |
>
> **La geometría (comprobaciones añadidas 2 y 3).** En una compra la entrada es un ALTO de M1 (el pivote contrario: `:631`, un BAJO en una venta), y el 1 es el extremo opuesto, el mínimo (`:653`). El bot llama ruido a `entrada > nivel` (`zonas.py:539`).
> - **S-7:** el 0 está arriba, en el último alto, y el 1 abajo, con r1, r4 y r6 bien emparejados con (a), (b) y (c).
> - **S-13:** «baja mucho» es correcto, porque con r6 el 1 es un mínimo que baja al reubicar.
> - **S-15:** «en una compra, por encima del bajo tomado es ruido» es correcto.
> - **S-12, desviación 1:** es correcta. Con el 0 siempre por encima del 1, una caja a caballo tiene el 0 arriba y el 1 abajo. Si el trader contesta (b), su lado solo puede tener el 1. Que con (b) coincida con la lectura de hoy de A-50 también es correcto.
> - **Las demás desviaciones:** la 2 (texto propio), la 3 (F07 a DECISIONES con el texto del Archivo 1) y la 5 (punteros) están justificadas. La 4 (el alcance de «las Reglas vivas») es una lectura que se puede defender, pero el consultor debería confirmarla. La respuesta dice «En PROJECT_STATE se quedan los encabezados que exigen los tests», y eso admite también la lectura de sacarlo todo. La rama la declara.
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | h1 | importa | El «Para Aleks» del recuadro de S-12 describe el cuerpo de forma inexacta. Dice que los dos dibujos «del texto de abajo» tienen el 0 por encima, pero el cuerpo pone el segundo con el 0 POR DEBAJO. Leído tal cual, ese dibujo no es ruido para el bot, que compara solo el 0. Los que tienen los dos el 0 arriba son los dibujos del recuadro del encargo («texto anterior», como dice la respuesta). | `PREGUNTAS.md:449-450`: «no opera ninguno de los dos dibujos del texto de abajo, que tienen el 0 por encima de la línea». Frente a `PREGUNTAS.md:463-464`: «en el segundo el 1 queda por encima y el 0 por debajo». |
> | h2 | importa | Los punteros llevan a un apartado que no es el del texto. El de «Technical Debt» en PS no apunta a ninguna sección de runbook sino a «PREVIA-SESION-5.md §5», y la tabla de destinos está en §6. Lo mismo pasa con los párrafos de entrada de MIRAR-EL-MATERIAL y RITUAL. El encargo pide que cada puntero lleve al sitio del texto entero. | `PROJECT_STATE.md` (diff, línea de cabecera de Technical Debt): «Lo que no era deuda, en su runbook desde trabajo/previa-sesion-5 (PREVIA-SESION-5.md §5)». `docs/runbooks/MIRAR-EL-MATERIAL.md:109` y `RITUAL.md:369`: «(PREVIA-SESION-5.md §5)». El informe estadiado tiene `289:## 6 · Lo que salió de PROJECT_STATE, y adónde`. |
> | h3 | importa | El informe promete pegar entero el informe del auditor y no está, y el Estado ya dice «lista para revisión». | informe estadiado :109: «El informe del auditor, entero, se pega al final del informe en la entrega». Los `## ` del fichero acaban en `410:## Estado`, sin la sección del auditor. |
> | m1 | menor | La cabecera de «Reglas vivas» conserva «Las que solo viven aqui», y la misma línea dice a continuación que cuatro bloques viven en otro sitio. | `PROJECT_STATE.md`, línea de «## Reglas vivas» (diff) |
> | m2 | menor | §6 cuenta `main` entre las 7 líneas que «no se mudaron», pero el guion la marca OK: el `in` por subcadena casa cualquier línea corta. Para líneas cortas, el OK del guion no prueba nada. | Salida de `comprobar_movido.py`: `OK runbook=True historia=True \| main`. Informe:317. Guion: `en_rb = l.strip() in runbooks`. |
> | m3 | menor | Si el trader contesta (c) «depende» a la primera parte de S-12, la segunda parte no tiene formulación. | `PREGUNTAS.md:438-441`: solo se contemplan la de la respuesta y la variante (b). |
>
> ### Lo que no pude comprobar
> - La línea del paso 1 con `2026-10-23` (`casos_ocultos`). No la reejecuté: consultar `casos_ocultos` es una exposición que habría que declarar el mismo día, y yo no escribo. La evidencia que la sustituye es el informe §3 (`False`) y su fila en HOLDOUT-EXPOSICIONES.
> - `make check`, que escribe. Lo sustituyen `make-check.log` y el informe. El árbol estadiado actual (informe con §10 y Estado) no tiene sello.
> - La CI de main (run 39705799089). No consulté gh.
> - Que el encargo sea copia tal cual del prompt original: no tengo el original.
> - El sentido (compra o venta) de v9 0:49:19 en la transcripción, que es material protegido. Solo vi la `afirmacion` del ítem, que dice «en una compra».
>
> ### Comandos ejecutados
> 1. `git branch --show-current && git merge-base main HEAD && git log --format='%h %s' main..HEAD && git diff --stat main...HEAD && git status --short && git diff --cached --stat`
> 2. Read `docs/encargos/trabajo-previa-sesion-5.md` y `contrato.yaml`
> 3. `git show :docs/validation/PREVIA-SESION-5.md | cat -n`
> 4. `uv run python scripts/contrato_rama.py`
> 5. `PYTHONUTF8=1 uv run python docs/validation/anexos/PREVIA-SESION-5/comprobar_movido.py .`
> 6. `PYTHONUTF8=1 uv run python docs/validation/anexos/PREVIA-SESION-5/simular_cierre.py .`
> 7. `cat` de los dos guiones de anexo
> 8. `git diff main...HEAD -- PROJECT_STATE.md`
> 9. `git diff main...HEAD -- docs/runbooks/ docs/plan/HOJA-DE-RUTA.md docs/validation/HOLDOUT-EXPOSICIONES.md`
> 10. `sed -n '564p;589p'` y `grep -n` de idealTP/F07 en HISTORIA; cabecera de HOLDOUT-EXPOSICIONES
> 11. `grep -n "^# "` de HISTORIA y `sed -n '11380,11424p' docs/state/HISTORIA.md`
> 12. `sed -n '55,90p' docs/state/README.md`
> 13. Un `grep -rn` sobre `.` (lo bloqueó la guardia; lo sustituí por Grep con glob acotado: CLAUDE.md, runbooks, state/README, tests, src, scripts, .claude, plan)
> 14. `git diff --numstat` y `git diff -U2 main...HEAD -- docs/sesion-5/PREGUNTAS.md`
> 15. `sed -n` del cuerpo de S-7, S-12, S-13 y S-15 en PREGUNTAS.md
> 16. `sed -n` de `zonas.py:110-118,528-542`, `strategy_spec.yaml:195-207` y `parametros.yaml:624-666`
> 17. Grep de los tres ids de evidencia; `grep -A3 cita_literal/afirmacion` de ev-v1-001306 y ev-v9-004919
> 18. `git diff --name-status main...HEAD`, `--cached`, `make-check.log` (SELLO/PICO/passed) y `git rev-parse HEAD^{tree}`
> 19. `git diff --numstat main...HEAD`; regla 2 y paso 1 de SESION-DE-PREGUNTAS.md
> 20. Grep de las secciones de PS en tests/src/scripts; `grep -n` de líneas en parametros/strategy_spec; Grep de A-50 en ambiguedades.yaml; Grep de «sube mucho|baja mucho» y de «por encima|por debajo|el 0|el 1» en PREGUNTAS.md
> 21. `git show :docs/validation/PREVIA-SESION-5.md | grep -n "^## \|auditor"`; `git diff --cached … | grep "^-"`
> 22. `diff` de la respuesta del consultor: encargo líneas 51-60 frente a informe 223-232 → IGUALES
> 23. `grep -c` de la fecha en PS, `wc -c PROJECT_STATE.md` y conteo de líneas borradas en HISTORIA (0)

## 13 · Lo que se hizo con los hallazgos del revisor

| # | Gravedad | Qué se hizo |
|---|---|---|
| a1 | importa | Arreglado: la fila del 2026-10-21 de `HOLDOUT-EXPOSICIONES.md` lleva sus cinco celdas (Particiones «ninguna»; Quien «la sesion, con el encargo del consultor del 2026-10-21»; ¿Quema? «No: …»), como las anteriores. |
| h1 | importa | Arreglado en el recuadro de S-12, en los dos sitios: en el motivo, «no opera ninguno de los dos dibujos del recuadro de ese encargo, que tienen los dos el 0 por encima de la línea»; en el «Para Aleks», «no opera ninguno de los dos dibujos del recuadro del encargo de `trabajo/previa-sesion-5` (el texto anterior a este), que tienen los dos el 0 por encima de la línea; el segundo dibujo del cuerpo de abajo, con el 0 por debajo y el 1 por encima, no se puede dar en una compra». |
| h2 | importa | Arreglado. El puntero de «Technical Debt» en PS nombra los tres runbooks y la tabla de §6. Los párrafos de entrada de `MIRAR-EL-MATERIAL.md` y `RITUAL.md` apuntan a §6, y el de `DECISIONES-DE-PROCESO.md` a §5 y §6. Los recuadros de PREGUNTAS.md siguen citando §1 y §5, que es donde están el inventario y la aplicación. |
| h3 | importa | Arreglado: el informe del auditor está entero en §11. |
| m1 | menor | Arreglado: «Las que solo vivian aqui y se quedan». |
| m2 | menor | Arreglado en el guion: compara líneas enteras (y, en el runbook, el arranque de una línea más larga si tiene 40 caracteres o más, para `idealTP` y F07). Da 20 en los dos sitios y 8 explicadas, `main` entre ellas; §6 y la tabla de §10 lo dicen. |
| m3 | menor | Arreglado: la segunda parte de S-12 dice qué hacer si contesta (c): se le pide el caso del que depende y la segunda parte se hace sobre el lado que dé. Es texto mío, como los de la desviación 2. |

**La desviación 4** (el alcance de «las Reglas vivas») la deja el revisor para que el consultor la
confirme; la rama la mantiene negando por defecto (§5). Si el consultor quiere sacarlas todas, son
el régimen del holdout y las tres primeras de «Things That Must Not Be Changed», con el mismo
método.

Tras los arreglos, PROJECT_STATE pesa 21.910 bytes (el puntero de «Technical Debt» nombra ahora los
runbooks), y las líneas del cierre lo dejarían en 22.359; `simular_cierre.py` da `a: []`, `b: []`,
`c: []` y los cuatro tests de PS pasan.

## Estado

Rama lista para revisión, NO cerrada. Todo el encargo y la respuesta a la PARADA están hechos (§10),
con cinco desviaciones declaradas (§5); el revisor no encontró nada que bloquee, y sus cuatro
«importa» y sus tres «menor» están arreglados (§13).
