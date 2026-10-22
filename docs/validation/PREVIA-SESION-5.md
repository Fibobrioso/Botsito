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

El informe del auditor, entero, se pega al final del informe en la entrega.

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
   «Lo que no era deuda, en su runbook desde trabajo/previa-sesion-5 (PREVIA-SESION-5.md §5)», y
   «Reglas vivas» lleva, en la suya, la lista de lo que salió y
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
de esta rama. Salen 28 líneas; 21 están en los dos sitios. Las otras 7 no se mudaron:
- `main`, la Current Feature de `main` y las dos «— ninguna desde el Archivo 40» las cambió la
  apertura (Archivo 41);
- las dos cabeceras de «Technical Debt» y «Reglas vivas» siguen en PS, con su puntero añadido;
- `### Decisions and Rationale` y `### Known Issues` son `## ` en el runbook.

En la primera pasada la comprobación encontró dos líneas de HISTORIA que no eran literales: les
había antepuesto «(de «…»)». Se corrigieron antes del commit, con el origen en la línea de la
condición.

## 7 · Tamaño final de PROJECT_STATE

**21.805 bytes** (`wc -c`; `main`: 24.135; tope del test: 25.000; objetivo: 22.000). Quedan 3.195
bytes libres hasta el tope. Con las líneas preparadas para el cierre quedaría en **22.254**.

## 8 · Líneas preparadas para el commit del contrato de la orden de cierre

Simuladas en memoria con `docs/validation/anexos/PREVIA-SESION-5/simular_cierre.py <raiz>` (como
el de VISOR-CONSTRUCCION y el de EA-CONEXION, con sus propias sustituciones):
`test_hoja_de_ruta.py` a, b y c sin problemas (`a: []`, `b: []`, `c: []`), y los cuatro de
`test_project_state.py` pasan. **PROJECT_STATE quedaría en 22.254 bytes.** El simulador lleva el
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

**Negativas de la guardia después de la fase 0**, las dos resueltas con la forma que proponía su
mensaje: `wc -c` y `pytest` en el mismo comando (los partí en dos llamadas), y un `sed -n` detrás de
la tubería de un guion (lo cambié por `grep`, que la guardia admite).

## Estado

EN CURSO. La respuesta a la PARADA está aplicada; faltan el `make check`, el revisor y la entrega.
