# Encargo · trabajo/hoja-de-ruta

Dado por Aleks (consultor) el 2026-10-10. Copiado tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Rama nueva: trabajo/hoja-de-ruta, desde main en 2a007b7 (commit de estado sobre el merge f472e06, tag stable/F37j-cases-rejilla). Antes de abrirla, verifica con git que main y origin/main están en 2a007b7, que el tag apunta a f472e06, que la CI de main sobre 2a007b7 está en success y que no hay otra rama abierta en local ni fix/* en origin; si algo no cuadra, para y dímelo. Ábrela con la skill abrir-rama: este prompt tal cual en docs/encargos/trabajo-hoja-de-ruta.md, su contrato.yaml y el archivo en HISTORIA del PROJECT_STATE.md de main.
>
> Objetivo: entradas F y P de la Next Action. Un mapa vivo de todo lo pendiente hasta operar en vivo, en docs/plan/HOJA-DE-RUTA.md, y guardias que hagan fallar make check cuando la Next Action, la hoja de ruta y las respuestas del trader se descuadren. Motivo (consultor, 2026-10-10, medido con un auditor independiente): el plan maestro no se mantiene desde el 2026-09-14; los tags desde F16 son contador y no funcionalidades del plan; la activación de la sesión 4 se cayó de la Next Action porque solo vivía como condición dentro de otras entradas; y la propia F, redactada por el consultor, depende de W, que ya está hecha.
> NO cambia: código de src/ salvo el test nuevo, spec, knowledge, parámetros, ningún informe cerrado ni fichero congelado. Nada de holdout: ninguna fecha de día reservado ni ningún resultado en la hoja de ruta. PROJECT_STATE.md está en 22.799 bytes: el saldo de bytes de la rama sobre él es ≤ 0.
>
> FASE 0, inventario sin escribir nada, con entrega y PARADA:
> a) Cada entrada de la Next Action (incluidas E, F, G, I, J y P, que entraron en el cierre de W) y cada pendiente heredado (texto entero desde docs/state/HISTORIA.md), con su estado medido: viva, hecha sin salir o superada en parte. Mide en concreto el heredado 15 frente a S-3 de la sesión 4 (y la candidata C4), y el 27 frente a RESPUESTAS-FTMO, ADR-0068 y ADR-0071 (qué sigue vivo: A-28, firma_tamano_posicion_ratio_aviso, la maximum capital allocation rule, el asterisco de USD/LOT*). Fichero:línea de la evidencia.
> b) Las dependencias colgantes u huérfanas: todo «después de», «antes de», «espera a», «junto a» o «tras» dentro de una entrada cuyo objeto no tenga entrada propia viva (hoy, al menos, F frente a W). Mídelo con grep.
> c) Cada ambigüedad que una tabla final de docs/validation/SESION-*-EXTRACCION.md da como «resuelve» o «en parte» y sigue ABIERTA en ambiguedades.yaml; para cada una, si su parámetro ya tiene valor (DEFAULT_AMBIGUOUS o CONFIRMED) o si falta código. Solo los informes, la spec y los ADR: nada de la cruda ni de la cuarentena.
> d) El estado real de F01-F35 de MASTER_PLAN.md §A: hecha, parcial o sin empezar, con el tag o el informe que lo prueba; mide por el contenido, no por el número del tag.
> e) Las condiciones previas de F26 (entrada G): PREREGISTRO.md, «una pregunta abre N particiones», los dos días del universo de la sesión 1 sin partición, «F26 no puede puntuar el objetivo hasta que A-18 esté cerrada», A-16, y lo que PREREGISTRO pida al trader.
> f) Herencias sin dueño visible: el refiltrado de las filtradas v7–v10 (va con E), la copia de seguridad incompleta desde el 2026-09-09 y las candidatas C1–C7 sin abrir.
> g) P: de qué ADR sale la regla general de CLAUDE.md «QUIEN: el consultor» sobre la columna de fechas de un backtest. Busca en todos los ADR y en el historial de CLAUDE.md la decisión que la introdujo. Si no sale de ninguno, propón la corrección de CLAUDE.md o el ADR, con las dos opciones.
> h) Cómo encaja la hoja de ruta con tests/contract/test_documentos_vivos.py (prohíbe recuentos que caducan en los documentos vivos) y con tests/unit/test_project_state_rutas.py (toda ruta citada en PROJECT_STATE existe).
> Entrega la fase 0 en el informe y PARA.
>
> FASE 1 (tras mi respuesta):
> - docs/plan/HOJA-DE-RUTA.md. Cada entrada lleva sus referencias con la forma NA:X (letra de la Next Action), HER:n (pendiente heredado), ID:<A-nn, ADR-nnnn o RN-nnn> o F:Fnn, y dice qué es, de qué depende, quién la hace y su criterio de hecho. Nombra ids, nunca recuentos que caducan. Contenido: (1) los tramos en orden de dependencia: R1 activar la sesión 4 (NA:E, con las ambigüedades de la fase 0 c como ID: y el refiltrado); R2 material de construcción (julio, NA:S, con sus ticks; NA:X para que enero cuente, ADR-0051 §8); R3 una corrida del arnés sobre toda la construcción según ADR-0070 y la clasificación de las diferencias por el consultor; R4 sesión 5 con el trader y su activación; R5 fidelidad (NA:G y las condiciones de la fase 0 e, mayo, marzo, NA:I, F26, F27); R6 plataforma F28-F32; R7 demo y sombra F33-F35; y antes de todo, R0 con lo que ordena el trabajo (esta rama y trabajo/entorno-code); (2) tres carriles aparte: lo de Aleks (NA:A, NA:O, agenda con el trader, copia de seguridad), guardias y deuda (NA:B, C, D, K, L, J...), y material reservado que no se toca; (3) la tabla F01-F35 de la fase 0 d; (4) las fechas fijas, sin días reservados. Escribe solo lo que la fase 0 sostiene.
> - La hoja de ruta entra en la lista de documentos vivos de test_documentos_vivos.py.
> - tests/unit/test_hoja_de_ruta.py, negando por defecto, que falle si: (a) una letra viva de la Next Action o un pendiente heredado vivo no aparece como NA:/HER: en la hoja de ruta; (b) una referencia NA:, HER:, ID: o F: de la hoja de ruta no existe, o una entrada marcada como hecha sigue viva; (c) una entrada de la Next Action depende («después de», «antes de», «espera a», «junto a», «tras») de una letra que no está viva; (d) una ambigüedad que una tabla final de SESION-*-EXTRACCION.md da como «resuelve» o «en parte» sigue ABIERTA y no aparece como ID: en un tramo de activación o de sesión. Tests sintéticos que lo rompen a propósito en los cuatro sentidos; el (c) falla con el main de hoy por F.
> - contrato.yaml gana el campo tramo (la entrada de la hoja de ruta a la que pertenece la rama): abrir-rama lo pide y make check falla si falta o no existe en la hoja de ruta. Rige desde la rama siguiente: el contrato de esta no lo lleva, porque la hoja de ruta aún no existe al abrirla.
> - RITUAL.md y la skill cerrar-rama: en el commit del contrato, junto a la Next Action, se actualiza la hoja de ruta. Revisa caso a caso contra main que no se pierde ninguna puerta.
> - MASTER_PLAN.md: un recuadro al principio, con fecha y rama, que diga que el orden y el estado vivos están en HOJA-DE-RUTA.md y que §E queda como historia. Sin tocar el cuerpo.
> - P: lo que decida en la PARADA sobre la regla «QUIEN».
> - Para el cierre, prepara en el informe (no en la Next Action de la rama) las líneas del commit del contrato: P sale HECHA; F se reescribe sin depender de W («F. Orden de trabajo: trabajo/entorno-code y después E; la hoja de ruta (docs/plan/HOJA-DE-RUTA.md) manda el orden.»), o como decida en la PARADA.
>
> Cierre de la rama:
> - make check > make-check.log 2>&1, con el exit 0, ningún failed y la línea SELLO, antes de cada commit.
> - Toca .claude/skills, RITUAL y el contrato: empújala como fix/hoja-de-ruta y pasa la CI de Linux. El único fallo aceptado es el de state check por el nombre fix/. Dame los números de run.
> - Informe en docs/validation/HOJA-DE-RUTA.md, con la fase 0, la PARADA y mi respuesta tal cual, lo hecho y su estado al final.
> - Pasa el revisor (subagente revisor), con este alcance: cada línea de la hoja de ruta tiene una fuente que existe, los tests fallan de verdad en los cuatro sentidos, no se pierde ninguna puerta de RITUAL, de cerrar-rama ni de abrir-rama, el saldo de bytes de PROJECT_STATE es ≤ 0, y nada de holdout. Pega su informe al final del tuyo.
>
> Rama lista para revisión, NO cerrada.
