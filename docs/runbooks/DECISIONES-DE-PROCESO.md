# Decisiones de proceso: las reglas vivas que salieron de PROJECT_STATE

Las «Reglas vivas» de `PROJECT_STATE.md` que hasta el 2026-10-21 solo vivían allí, mudadas TAL CUAL,
con su título de entonces y en el mismo orden, en `trabajo/previa-sesion-5` (respuesta del consultor
a la PARADA de su fase 0, punto 3; `docs/validation/PREVIA-SESION-5.md` §5 y §6). Siguen vigentes: lo que
cambia es dónde se leen. En `PROJECT_STATE.md`, «Reglas vivas», queda una línea que apunta aquí, y
el texto literal de cada una, con su condición, en `docs/state/HISTORIA.md`
(«# Regla viva SUSTITUIDA · sale de PROJECT_STATE.md en trabajo/previa-sesion-5 (2026-10-21)»).
Las reglas de `PROJECT_STATE.md` que no se mudaron (el régimen del holdout y las tres primeras de
«Things That Must Not Be Changed») siguen allí. Desde el 2026-10-22 (`trabajo/hoja-sesion-05`)
también lleva entradas que nacen aquí y no vienen de esa mudanza: cada una lo dice en su texto.

## Change Regimes (must be respected), lo que CLAUDE.md no dice

- data/manifests/, knowledge/corpus/transcripciones/ y knowledge/corpus/fotogramas/ → INMUTABLES tras commit (hook + historial de git; ADR-0005, ADR-0007 y ADR-0008). Corrección = manifiesto nuevo con `reemplaza_a`; exactamente una extracción de fotogramas activa por vídeo.

## Things That Must Not Be Changed

- Ficheros de texto siempre con LF y UTF-8 (escribir con `newline="\n"`); toda salida de git se
  decodifica como UTF-8 con `core.quotepath=false` (la consola Windows es cp1252).

## Decisions and Rationale

Formato obligatorio por decision (ver docs/adr/0000-template.md). Decisiones de proceso vigentes:
- 2026-09-04 · Tres particiones reservadas (holdout-1/2/3) y pre-registro de umbrales antes de F26. Problema: holdout unico se quema al abrirlo; umbral ajustable a posteriori. Alternativas: holdout unico (descartada), validacion cruzada temporal (insuficiente con pocos casos). Estado: ACTIVE.
- 2026-09-04 · La garantia de inmutabilidad/solo-anadir es un test en CI contra el historial de git; los hooks son comodidad. Estado: ACTIVE.
- 2026-09-04 · Sin inferencias en evidence/; todo lo importado de Bot v2 se re-cita o entra como UNKNOWN. Estado: ACTIVE.
- 2026-10-21 · Para los encargos, dos reglas del consultor. Esta entrada NACE AQUI, en `trabajo/hoja-sesion-05` (2026-10-22): no viene de la mudanza de PROJECT_STATE de `trabajo/previa-sesion-5`. (1) «Si la guardia o el clasificador niegan un comando, PARADA, salvo seguir la forma que la propia guardia propone en su mensaje, declarándolo en el informe.» Origen: el encargo de `trabajo/previa-sesion-5` (`docs/encargos/trabajo-previa-sesion-5.md`, «0. Apertura», «Regla del consultor desde el 2026-10-21») y `docs/validation/PREVIA-SESION-5.md` §0, que la aplicó; antecedente, `docs/validation/EA-CONEXION.md` §12, fila 3g («PARADA, sin cambiar de vía ni reescribirlo»), que la orden de cierre de esa rama corrigió a la forma de hoy (registro de cierre de `trabajo/ea-conexion` en `docs/state/HISTORIA.md`, punto 3). (2) «Ninguna consulta de la CI con un guion ni con un bucle.» Origen: el guion de espera de la CI de `docs/validation/EA-CONEXION.md` §13 (§12, fila 0/7) y su fila en `docs/runbooks/ERRORES-RECURRENTES.md`; la orden de cierre de `trabajo/sesgo-h4-color`, copiada en `docs/validation/SESGO-H4-COLOR.md` §10 (`:1301`, un hallazgo sobre el cierre de `trabajo/corrida-construccion`: «cambiar de vía tras una negativa es rodearla»); y la línea de Technical Debt de `PROJECT_STATE.md` sobre el guion que espera a la CI en bucle, que sigue abierta para el carril de guardias. Problema: tras una negativa, rodear la guardia por otra vía, y esperar a la CI con un guion que la consulta en bucle. Alternativas: «PARADA, sin reescribir» (la de EA-CONEXION, descartada: no contemplaba la vía que propone la propia guardia). Estado: ACTIVE.

## Known Issues

- El trailer `Fuente:` se exige por commit, no por linea: un commit que mezcle esquema y valor
  cita ambas fuentes.
- El hash de 8 hex en los ids de evidencia/feedback (32 bits) se considera suficiente para
  cientos de items; desde F07 `escribir_item` distingue "mismo contenido" (idempotente) de una
  colision real (error). 353 items sin colision.

## Limitacion declarada de F07 (de «Technical Debt»)

No es una regla viva: es una entrada de «Technical Debt» de `PROJECT_STATE.md` que no era deuda
abierta y sale en la misma rama (conjunto A de PREVIA-SESION-5.md §4). Su texto entero, el del
Archivo 1 de `docs/state/HISTORIA.md` (`:589`), porque el de `PROJECT_STATE.md` lo recortaba y el
informe de F07 (`docs/validation/F07-evidence-extraction.md:168-170` y `:188`) no trae literal ni
el recall ni el dueño:

- F07, limitacion declarada: el proponente de las 20 propuestas, el autor de la lista de referencia (golden) y el primer filtro fueron la misma sesion (`claude-fable-5-1`); no hay cliente de API de LLM (sin clave). El control independiente es el usuario (acepto los 341 sin cambios; recall humano de V4 0:05-0:15 sin faltas). Dueno: si llega una clave, otro proponente rellena una propuesta del mismo tramo y se compara; mientras tanto no bloquea.
