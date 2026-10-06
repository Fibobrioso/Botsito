# Encargo · trabajo/respuestas-ftmo

Dado por el consultor el 2026-10-05. Copiado tal cual:

> Modelo: Opus · Esfuerzo: medio
>
> Encargo de rama: trabajo/respuestas-ftmo (punto T del Next Action). Consultor, 2026-10-05.
>
> BASE
> main en 54c69fe (commit de estado de stable/F36z-ventana-no-citable, que apunta a f8b291c), CI de main run 221 en verde. Compruébalo antes de abrir; si algo no cuadra, para. Abre con la skill abrir-rama (encargo en docs/encargos/, contrato.yaml, archivo de PROJECT_STATE en HISTORIA). Copia este prompt tal cual al encargo.
>
> OBJETIVO
> Registrar la respuesta de FTMO del 2026-10-05 al ticket VDW-DPMWR-965 SIN COPIAR EL CORREO LITERAL, y dejar en RITUAL.md la regla de numeración de tags tras agotar las letras de F36.
> NO cambia: motor, broker, freno, spec ejecutable, parámetros, knowledge/evidence, cifras. No se abre ni se cierra ninguna ambigüedad.
>
> POR QUÉ NO VA LITERAL
> El pie del correo de FTMO prohíbe compartirlo sin su consentimiento y el repo es público. Regla para toda la rama: ningún texto commiteado lleva frases en inglés del correo ni el nombre de la persona de soporte. Solo se citan: el ticket, el remitente support@ftmo.com, la fecha y hora de llegada (2026-10-05 10:29:36 UTC), que responde al correo de Aleks del 2026-10-03 (el de las diez preguntas, literal en FTMO-REGLAS.md), y los nombres de las páginas públicas de FTMO (Symbols, Forbidden Trading Practices). La fuente del contenido es la paráfrasis del consultor de abajo, con su fecha.
>
> PARÁFRASIS DEL CONSULTOR (2026-10-05), por número de pregunta del correo del 2026-10-03
> - 1 a 3 (qué cuenta para el límite diario): FTMO contesta en bloque que todo tipo de orden cuenta para el límite de 2.000 órdenes al día. No distingue rechazadas, modificaciones, cancelaciones ni cierres, ni excluye ninguna. Estado: respondida en parte.
> - 4 (reinicio): el límite se reinicia a las 00:00 hora de Europa central (CET/CEST) cada día, igual que los objetivos y límites de trading. Estado: respondida.
> - 5 (colocar pendientes dentro de las dos horas): se desaconseja si refleja intención de hacer gap trading y no trading genuino; recuerda que el gap trading está prohibido (Forbidden Trading Practices). No hay prohibición expresa de colocar. Estado: respondida en parte.
> - 6 (pendiente colocada antes y llenada dentro de la ventana; si hay que cancelarla): sin respuesta.
> - 7 (modificar el precio de una pendiente dentro de la ventana): en general se considera gestionar una orden existente, no abrir una operación nueva. Estado: respondida.
> - 8 (qué mercado cuenta): cada instrumento tiene su propio horario de cierre y remite a la página Symbols, instrumento por instrumento. No menciona bolsas ni otros mercados. Estado: respondida en parte (cuenta el horario del propio instrumento).
> - 9 (pausa diaria): el rollover de lunes a viernes no se considera gap trading. Estado: respondida.
> - 10 (tamaño de posición, R17): FTMO no valida estrategias, métodos de tamaño ni patrones de ejecución concretos, y no fija límites numéricos de exposición o de tamaño ni multiplicadores. «Sustancialmente mayor» depende del comportamiento histórico del propio trader. Recomienda evitar aumentos bruscos o desproporcionados del tamaño o del número de operaciones y mantener un tamaño consistente y consciente del riesgo, dentro de las reglas de gestión de riesgo de sus Términos. Estado: respondida sin cifra. No se repregunta.
> - Además: una nota sobre el tipo de cuenta Normal que no aplica a Swing (ADR-0026). Se anota sin efecto.
>
> FASE 0 · INVENTARIO SIN TOCAR NADA (entrégala antes de escribir)
> a) Tag F37a. Comprueba que ningún test, guardia ni la skill cerrar-rama lea el formato del tag de forma que stable/F37a-<nombre> lo rompa. Como mínimo:
>    - .claude/skills/cerrar-rama/SKILL.md: cómo propone el tag (git tag -l "stable/*" --sort=-creatordate);
>    - .claude/hooks/guardia.py: patrones de tags y ramas;
>    - state check (Last Stable Commit, Current Feature);
>    - src/botsito/validation/knowledge.py (F\d{2} contra MASTER_PLAN) y src/botsito/cli.py (F\d{2} en Completed Features);
>    - tests/unit/test_project_state.py y tests/unit/test_guardia_claude.py;
>    - un grep de "F36" y de patrones stable/F en tests/, scripts/, src/, .claude/ y .github/.
>    Por cada lector: qué lee, si F37a pasa, y la prueba (un comando ejecutado, no una lectura). Si alguno lo rompe, para y dímelo.
> b) ADR-0067 frente a las preguntas 1 a 4: qué peticiones cuenta hoy el freno, si una orden rechazada por el servidor cuenta, y el valor actual de firma_huso_corte. ¿Coincide con las 00:00 CET/CEST en las dos estaciones? Mídelo con un test o un comando sobre las medianoches de un año, no lo deduzcas.
> c) ADR-0068 frente a las preguntas 5 a 9: qué hace hoy el bot al colocar, modificar o tener puesta una pendiente en la ventana (cierre_pendientes), y qué mercado usa el calendario.
> d) Dónde vive hoy cada cosa que esta rama actualiza: FTMO-REGLAS.md (recuadros del ticket y fila R17), la línea de R17 en Technical Debt de PROJECT_STATE.md, y A-54 y A-55 en ambiguedades.yaml.
> e) Textos literales de FTMO ya commiteados (el recuadro de la respuesta del 2026-09-29 en FTMO-REGLAS.md y cualquier otro): solo la lista, sin tocarlos.
>
> DECISIONES (aplícalas salvo que la fase 0 las contradiga; si las contradice, para)
> 1. FTMO-REGLAS.md: recuadro nuevo fechado (2026-10-05, rama trabajo/respuestas-ftmo) con la cabecera de fuente de arriba y una tabla con una fila por pregunta 1-10. Columnas: lo que responde (la paráfrasis), estado, qué cambia en el bot. La columna «qué cambia» dice «nada» en todas, por lo que sigue:
>    - 1-3: el freno ya cuenta todo lo que llega al servidor. Lo que el propio bot niega no sale y no cuenta.
>    - 4: coincide con firma_huso_corte. Si la fase 0 b) dice que no coincide, para.
>    - 5 y 7: el bot sigue negando colocar y modificar dentro de la ventana. Es una restricción ELEGIDA, más estricta que FTMO, y se declara así.
>    - 6: cierre_pendientes sigue en cancelar.
>    - 8: el calendario de EURUSD ya es el mercado relevante.
>    - 9: la pausa diaria no es cierre.
>    - 10: el riesgo fijo del 0,5 % desde el primer día es el patrón histórico de la cuenta y no hay nada que cambiar.
>    Los recuadros anteriores no se editan.
> 2. A-54 y A-55: solo cambia el campo pregunta, que añade «respondida en parte el 2026-10-05 (FTMO-REGLAS.md, recuadro de esa fecha)» y, en A-55, «la pregunta 6 sigue sin respuesta». Siguen ABIERTAS con la misma clase y bloqueante. spec docs --escribir en el mismo commit.
> 3. PROJECT_STATE.md: la línea de Technical Debt «PENDIENTE DE FTMO: SI UN LOTE QUE VARIA CON EL STOP…» sale de PROJECT_STATE y pasa literal a HISTORIA, en esta rama. No entra otra en su lugar. El saldo neto de bytes de PROJECT_STATE en esta rama tiene que ser menor o igual que cero.
> 4. RITUAL.md: junto a la regla que manda consultar la última letra en HISTORIA, esta línea literal: «Agotadas las letras de una serie, se sigue en el número siguiente con la a; un número posterior a F35 es un contador, no una fase del MASTER_PLAN». Fecha y fuente: decisión del consultor del 2026-10-05; tras stable/F36z la serie sigue en stable/F37a-<nombre>. Si la fase 0 a) muestra que la skill cerrar-rama deriva la letra de forma mecánica que F37a rompe, el arreglo va en esta rama: un cambio mínimo, comparado línea a línea con main en el informe. Ningún otro cambio en .claude/.
> 5. Literales previos (fase 0 e): no se tocan. Borrarlos no los saca del historial y no se reescribe historia. En el informe, una línea que los liste.
>
> COMPROBACIONES
> - make check y uv run botsito state check en verde, con su salida en el informe.
> - Ningún texto commiteado en esta rama lleva frases en inglés del correo ni el nombre de la persona de soporte. Compruébalo releyendo el diff y decláralo.
> - Trailer Fuente: con ids que existan, según la convención de trabajo/fuentes-ftmo.
> - Si la rama no toca hooks, rutas ni código de plataforma, no hace falta fix/. Si toca .claude/ (decisión 4), sí: fix/respuestas-ftmo y CI de Linux, con su número de run.
>
> INFORME
> docs/validation/RESPUESTAS-FTMO.md: fase 0 con su evidencia, tabla encargo frente a lo hecho, desviaciones, comprobaciones y bytes de PROJECT_STATE. El cierre de esta rama será el primero con stable/F37a-respuestas-ftmo: la fase 0 a) tiene que dejarlo probado.
>
> REVISOR
> Pasa el revisor y pega su informe al final. Que compruebe aparte la regla de no-literal, la línea de RITUAL tal cual y la prueba de F37a.
>
> Rama lista para revisión, NO cerrada.
