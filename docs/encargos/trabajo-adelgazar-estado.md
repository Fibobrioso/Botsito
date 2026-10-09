# Encargo · trabajo/adelgazar-estado

Dado por Aleks (consultor) el 2026-10-08. Copiado tal cual:

> Modelo: Opus · Esfuerzo: medio
>
> Rama nueva: trabajo/adelgazar-estado, desde main en 8cfd479 (commit de estado sobre el merge 8d1578d, tag stable/F37g-guion-mismo-comando). Antes de abrirla, verifica con git que main está en 8cfd479 y que el tag apunta a 8d1578d; si no, para y dímelo. Ábrela con la skill abrir-rama: este prompt tal cual en docs/encargos/trabajo-adelgazar-estado.md, su contrato.yaml y el archivo en HISTORIA del PROJECT_STATE.md de main.
>
> Objetivo: dejar PROJECT_STATE.md en 20.000 bytes o menos (hoy 24.362; tope del test 25.000), sacando a HISTORIA lo que ya no es presente, hacer el punto Y de la Next Action (RITUAL.md) y apuntar en el repo dos decisiones de la demo de FTMO que hoy solo viven en la conversación.
> NO cambia: motor, spec, knowledge, parámetros, guardias, hooks, tests de código (salvo lo que pida el tamaño, que no debería), ni el tope de 25.000 del test. Nadie ejecuta uv run botsito motor arnes en esta rama (solo se ejecuta para medir según ADR-0070, y aquí no se mide nada).
>
> Criterio único para sacar algo de PROJECT_STATE (decisión del consultor del 2026-10-08, que la cabecera de «Pendientes heredados» le reserva): una línea sale SOLO si cumple una de estas condiciones, con su evidencia citada (fichero:línea, commit, tag o ADR):
>  (a) HECHA o PAGADA: hay commit, tag, ADR o test que lo muestra;
>  (b) REPETIDA: su contenido está vivo, entero, en otra entrada de la Next Action, en CLAUDE.md o en un runbook (cita dónde);
>  (c) SUSTITUIDA: un hecho posterior la dejó sin objeto (cita cuál);
>  (d) NO ES DE SU SECCIÓN: una regla o un hecho que vive literal en otro sitio (cita dónde). Si no vive en ningún otro sitio, se queda.
> Niega por defecto: si dudas, la línea se queda. No resumas ni reescribas lo que se queda, salvo las introducciones de sección (fase 2).
>
> FASE 0, inventario sin tocar nada. Para cada línea de «Pendientes heredados», «Technical Debt» y «Reglas vivas»: condición (a/b/c/d o «se queda») y evidencia. Comprueba en particular, sin darlo por hecho:
>  - A4: HISTORIA (línea 656 aprox.) la da HECHA en stable/F31c-memoria-suite y stable/F31d-ci-linux-memoria.
>  - A2 y 36 frente a la entrada A; 2, 12 y 23 frente a CLAUDE.md y docs/runbooks/ENTRADA-MARZO.md; 6 frente a CLAUDE.md (verifica si CLAUDE.md dice lo de febrero; si no, se queda).
>  - 22 (sesión 02) y 10 (no comprar; confirmar que el tipo Swing existe) frente a lo que ya pasó (sesiones 3 y 4 activadas; prueba gratuita Swing creada el 2026-10-08, en la entrada A).
>  - A3 y su d): verifica si RN-006, la vida de la orden stop, tiene rama cerrada; RN-007 ya está en la entrada H.
>  - Technical Debt: «LOS CINCO PATRONES…» (su propia línea dice que está entera en ERRORES-RECURRENTES), «BUSCAR EN EL CORPUS ANTES DE REDACTAR…» (verifica si lo dice docs/runbooks/AMBIGUEDADES.md), la de v5 en Drive (verifica si fuentes.yaml lleva el drive_id) y cualquier otra que se haya pagado.
>  - Reglas vivas, la decisión del 2026-09-25 sobre firma_comision_por_lado («PENDIENTE DE IMPLEMENTAR… hoy UNKNOWN»): mide qué valor y qué fuente lleva hoy el parámetro. Si ya tiene valor con fuente, la línea está SUSTITUIDA (c).
> Entrega en el informe la tabla y los bytes de cada sección antes y la previsión después. No pares: sigue, salvo que la previsión no baje de 20.000 bytes; en ese caso para y dime qué más haría falta.
>
> FASE 1, salidas a HISTORIA. Al final de docs/state/HISTORIA.md (solo se amplía), un bloque por clase, con el texto literal de cada línea que sale, su condición y su evidencia, siguiendo el formato de los bloques que ya hay («# Technical Debt PAGADA · sale de PROJECT_STATE.md en …»):
>  # Pendiente heredado SALE · sale de PROJECT_STATE.md en trabajo/adelgazar-estado (2026-10-08)
>  # Technical Debt PAGADA · … / # Technical Debt RECLASIFICADA · …
>  # Regla viva SUSTITUIDA · …
> En PROJECT_STATE no queda ni un resumen de lo que sale.
>
> FASE 2, introducciones. Las de la cabecera del fichero y de cada sección (Known Ambiguities, Technical Debt, Reglas vivas, Pendientes heredados, Completed Features, Change Log) se acortan a una o dos líneas que apunten a docs/state/README.md, que ya lo explica. Si alguna dice algo que README no dice, primero pásalo a README, literal, y luego acórtala. Lo que exigen los tests (secciones y orden; la tabla de ambigüedades de test_kit.py) no se toca.
> En docs/state/README.md, un párrafo corto con las nuevas clases de salida de la fase 1 y el criterio (a)-(d) con negación por defecto, con fecha y rama.
>
> FASE 3, punto Y (RITUAL.md; decisión del consultor del 2026-10-08):
>  - Paso del commit de estado (línea 216 aprox.): Next Action sale de la lista de líneas que se editan ahí. Se dice que la Next Action ya cambió en el commit del contrato (punto 3) y que en el commit de estado solo cambia si la orden de cierre lo pide expresamente.
>  - Punto 3 del commit del contrato: ampliarlo a TODO cambio de la Next Action que mande la orden de cierre. Salen las HECHAS (como hoy), entran las nuevas y cambian las que la orden diga, todo en ese commit. Con eso se comprueba que PROJECT_STATE sigue por debajo de 25.000 bytes, y si no, se para antes del commit.
>  - Cambia en consecuencia el comentario «# solo si el punto 3 sacó alguna entrada de Next Action» y la puerta («más M PROJECT_STATE.md si el punto 3 sacó algo»): debe pasar a decir «si el punto 3 cambió la Next Action».
>  - Busca con grep en .claude/skills/ (cerrar-rama, abrir-rama), docs/state/README.md, CLAUDE.md y docs/runbooks/ cualquier otro sitio que diga que la Next Action se edita en el commit de estado, o que el punto 3 solo saca HECHAS, y alinéalo en el mismo commit. Lista en el informe cada sitio, con su antes y después.
>
> FASE 4, la demo de FTMO en docs/runbooks/DEMO-FTMO.md: una sección corta «La prueba de octubre de 2026», con lo que declara Aleks (fuente: Aleks, 2026-10-08; NO escribas el número de cuenta, porque el repo es público):
>  - prueba gratuita creada el 2026-10-08: 2-Step, Swing, USD, 100k, MT5, servidor FTMO-Demo; vence hacia el 22-10; script copiado y compilado con 0 errores el 2026-10-08;
>  - ejecución 1 entre las 03:00 y las 08:00 hora de Lima, evitando las 07:30 de Lima. Calcula con zoneinfo la equivalencia en Europe/Madrid para un día anterior al 25-10 (espero 10:00-15:00 y 14:30) y escríbela, comprobando que cae dentro de la ventana del bot (07-15 de España) y de la franja 9-18 de este runbook. Si la medida da otra cosa, gana la medida y me lo dices;
>  - MT5 muestra la cuenta de prueba como «Netting». Si la cuenta Swing real es netting o hedging está SIN COMPROBAR y no se supone: lo comprueba la rama de ADR-0057 y A-27. Mira si tools/mql5/MedirDemoFTMO.mq5 registra el modo de la cuenta (ACCOUNT_MARGIN_MODE o equivalente) y escribe en el informe si lo hace o no; no cambies el script en esta rama.
>  - En la entrada A de PROJECT_STATE, como mucho una frase que apunte a esa sección.
>
> Cierre de la rama:
>  - make check > make-check.log 2>&1, con el exit 0, ningún failed y la línea SELLO. En el informe van el tamaño final exacto de PROJECT_STATE.md y la comprobación de que test_historia.py y test_project_state.py pasan.
>  - La rama no toca hooks, rutas ni plataforma: no hace falta CI de Linux.
>  - Informe en docs/validation/ADELGAZAR-ESTADO.md, con la tabla de la fase 0, lo que salió y adónde, los sitios alineados en la fase 3 y su estado al final.
>  - Pasa el revisor (subagente revisor), con este alcance: que nada salga sin evidencia, que todo lo que sale esté literal en HISTORIA, que lo que se queda no cambie de texto (salvo las introducciones) y la coherencia de RITUAL tras Y. Pega su informe al final del tuyo.
>  - Y sale de la Next Action en el commit del contrato, cuando yo dé la orden de cierre. No la marques HECHA antes.
>
> Rama lista para revisión, NO cerrada.
