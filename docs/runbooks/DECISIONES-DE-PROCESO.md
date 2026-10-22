# Decisiones de proceso: las reglas vivas que salieron de PROJECT_STATE

Las «Reglas vivas» de `PROJECT_STATE.md` que hasta el 2026-10-21 solo vivían allí, mudadas TAL CUAL,
con su título de entonces y en el mismo orden, en `trabajo/previa-sesion-5` (respuesta del consultor
a la PARADA de su fase 0, punto 3; `docs/validation/PREVIA-SESION-5.md` §5 y §6). Siguen vigentes: lo que
cambia es dónde se leen. En `PROJECT_STATE.md`, «Reglas vivas», queda una línea que apunta aquí, y
el texto literal de cada una, con su condición, en `docs/state/HISTORIA.md`
(«# Regla viva SUSTITUIDA · sale de PROJECT_STATE.md en trabajo/previa-sesion-5 (2026-10-21)»).
Las reglas de `PROJECT_STATE.md` que no se mudaron (el régimen del holdout y las tres primeras de
«Things That Must Not Be Changed») siguen allí.

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
