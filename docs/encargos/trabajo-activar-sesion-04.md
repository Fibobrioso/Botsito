# Encargo · trabajo/activar-sesion-04

Dado por Aleks (consultor) el 2026-10-11. Copiado tal cual:

> Modelo: Fable 5.1 · Esfuerzo: alto
>
> Encargo del consultor (2026-10-11) · trabajo/activar-sesion-04 · tramo R1 (entrada R1.1 de la hoja de ruta; E de la Next Action)
>
> Rama nueva: trabajo/activar-sesion-04, desde main (11df2c4, commit de estado sobre el merge del tag stable/F37l-entorno-code; CI de main en verde, run 38156003516). Ábrela con la skill abrir-rama: base comprobada con git (su paso 1), contrato con tramo R1, riesgo alto (spec y motor), artefacto docs/validation/ACTIVAR-SESION-04.md. El recorrido lo mandan las skills activar-sesion (la activación), fase-cero (fase 0 y PARADA) y entregar-rama (entrega). Si este encargo y ellas chocan, ganan ellas y lo dices.
>
> OBJETIVO
> Que cada respuesta de la sesión 4 que de verdad cierra su ambigüedad quede RESUELTA en la spec y, si hace falta, en el motor, con su test; y que todo lo demás quede escrito para la sesión 5 con la pregunta reformulada.
>
> QUÉ NO CAMBIA
> - Nada fijado se pisa (valor CONFIRMED, regla con su literal, ADR, respuesta anterior del trader): si una respuesta lo contradice, PARADA con las dos fuentes, y se corrige solo por su régimen.
> - Ninguna «en parte» se cierra.
> - Ninguna cifra dentro de una forma ejecutable (ADR-0002).
> - Sin arnés y sin medidas agregadas sobre material: el comportamiento se prueba con tests sintéticos. La corrida que cuenta es la de R3.1, en otra rama.
> - Nada de material: ni julio (S), ni diciembre (I), ni marzo, ni febrero, ni la cruda de v10 (solo la lee Aleks). Las citas, solo las que SESION-04-EXTRACCION.md dejó citables, ninguna de un ejemplo del replay de julio o de enero, y todas cruzadas con knowledge/corpus/tramos_no_citables.yaml, márgenes incluidos.
> - La Next Action y la hoja de ruta no se tocan en la rama: sus líneas se preparan en el informe para el commit del contrato del cierre.
> - El Makefile, .claude/ y la guardia no se tocan.
>
> FASE 0 (skill fase-cero; termina en PARADA)
> a. Tabla de activación (activar-sesion, paso 1), una fila por cada código de SESION-04-EXTRACCION.md §5, también los que no son ambigüedad: S-6 (ADR-0061 §2), S-13 (ADR-0060 §2), S-14 (RN-007), S-16 (E-1), S-19 (marzo) y S-7 (A-42: verifica que está RESUELTA y no la toques). Mi cuadre, que compruebas y no copias: 17 ambigüedades ABIERTA con respuesta; solo «resuelve»: A-18, A-21, A-25, A-30, A-33, A-36, A-39, A-51, A-52; mezclada: A-49 (S-4 resuelve; S-1 y S-2 en parte); solo «en parte»: A-13, A-32, A-35, A-43, A-44, A-50, A-53. Añade a cada fila qué hace hoy el motor (fichero:línea), si el cierre es solo de spec o necesita código, y el test que lo probaría fallando en main.
> b. Lo que ya sé que choca, para medirlo y llevarlo a la PARADA:
>    1. A-18 (S-3) y A-33 (S-12): el trader dice stop en el 0,8 y objetivo fijo de 3 veces el 0→1, y ADR-0040 (ACTIVE) declara refutada esa combinación con el material. Ni la E ni R1.1 citan ADR-0040. Mi criterio por defecto: ninguna de las dos se cierra en esta rama sin un ADR que diga cómo conviven el testimonio y la refutación. Propón las opciones de ese ADR. No vuelvas a medir el material: lo que ADR-0040 ya midió se cita.
>    2. S-13 frente a ADR-0060 §2: allí la doble ruptura sin cuerpo sigue siendo «ambiguo» y RN-033 prohíbe operar; el trader dice que la neutra mantiene el sesgo. Qué haría falta (ADR, regla, motor, tests).
>    3. S-4 frente a caja_se_fija y la decisión 5 de ADR-0064 (y la opción en_cada_cierre_m1 que ya existe en src/botsito/engine/zonas.py): cómo queda A-49, entera a la sesión 5 o con lo de S-4 activado aparte.
>    4. S-16 (E-1): el trader da por bueno el backtest de agosto del vídeo, al revés de la premisa de docs/sesion-4/PREGUNTAS.md y de lo que dijo en v9. Mide por recuento, sin abrir filas ni resultados, qué cambiaría (libros, casos dev de agosto, spec). libros.yaml solo se amplía (ADR-0039 §3). Nada cambia sin decisión.
>    5. Las «en parte» que contradicen un CONFIRMED, para dejarlas escritas: S-24 frente a break_even_criterio_ruptura y ADR-0065; S-9 frente a perdida_maxima_semanal.
> c. Detalles que el repo ya pide:
>    - A-36 viene de un REOPEN (fb-2026-09-29-sesion-03-f3caeb2d): su cierre va con --supersede. Su texto habla de orden límite y A-47 fijó orden stop: dilo.
>    - A-21: la opción nueva en su enum y en LECTURAS_LIMPIA, y qué pasa con --diagnostico-a21 (src/botsito/cli.py), porque la corrida de R3.1 solo cuenta sin ningún --diagnostico-* (ADR-0070 §3). Propón si se retira; no la retires sin decisión.
>    - A-51 no tiene parámetro: propón cuál, con nombre y valores.
>    - A-30/A-39: ambiguedades.yaml trae parametros: [] en A-30. Revisa en knowledge/spec/strategy_spec.yaml el «LO QUE NO HACE: retirar la orden pendiente al vencer la vela» y el docstring de src/botsito/engine/motor.py.
>    - La hoja de scripts/hoja_preguntas.py (ORDEN_SESION_02) no trae A-51 ni A-52: di qué se hace en ese caso con el quinto sitio de docs/runbooks/AMBIGUEDADES.md.
>    - Quién espera cada ambigüedad: grep -rn "A-n" CLAUDE.md docs/runbooks PROJECT_STATE.md docs/plan/HOJA-DE-RUTA.md.
> d. Herencias, cada una hecha o declarada con su motivo:
>    - Heredado 15 (la pregunta de A-18): sale solo si A-18 se cierra.
>    - Heredado 37 (volumen máximo, «con A-18»): lo decide la respuesta de FTMO a P-D1 (O). Queda fuera de esta rama, y se dice.
>    - H (RN-007, S-14 en parte) y el punto 3 de la orden de cierre de trabajo/sesion-04 (el «12 puntos» de 1:44:44 es ambigüedad del ASR): comprueba con la CLI filtrada si ese segundo es citable con sus márgenes (hay un tramo no citable que acaba 23 s antes). Si lo es, propón que Aleks escuche ese minuto; si no, va a la sesión 5. Di también si S-13 («1 o 2 puntos ya cuentan») toca el umbral de S-14.
>    - §4 de la extracción: sus once puntos, cada uno con su destino.
>    - Candidatas C1, C4 y C6 de docs/validation/DISENO-ENTRADA-RUPTURA.md §2.8 (C2 y C3 ya son A-48 y A-49): si la sesión 4 las toca.
>    - R1.1 cita también SESION-03-EXTRACCION.md §5: comprueba que no queda nada de la sesión 3 con «resuelve» y ABIERTA.
> e. La lista para la sesión 5: cada «en parte» y cada cosa que no se cierre aquí, con lo que sí quedó claro (sin fijar nada) y la pregunta reformulada en el lenguaje del trader, cerrada con opciones y «otra, ¿cuál?». Va en el informe hasta que exista la hoja de la sesión 5 (R4.1, que espera a J).
> f. El plan de commits: uno por respuesta activada; primero las que solo tocan spec y después las de motor. Si los ADR nuevos y el motor no caben con garantías en esta rama, propón partirla y por dónde.
>
> «Lo que necesito que decidas» trae como mínimo b.1 a b.5, A-36, el parámetro de A-51, --diagnostico-a21, S-14 y cada respuesta dada con «creo» o con un ejemplo sin regla general.
>
> DESPUÉS DE MI RESPUESTA
> Cópiala tal cual al final del encargo y del informe y aplícala punto por punto (fase-cero). Cada respuesta activada sigue entero el paso 3 de activar-sesion, en su propio commit: registro sobre la ambigüedad con todas las opciones (con --supersede si viene de un REOPEN), registros de parámetro, feedback apply --check que propone solo los de esa respuesta, los cinco sitios de AMBIGUEDADES.md, tests/unit/test_kit.py, spec_version con uv run botsito spec manifest --escribir y uv run botsito spec docs --escribir, el código con su test, uv run botsito knowledge validate antes de make check, y el trailer Fuente: en el cuerpo con ids fb-* que existen. Los tests que congelaban «sin fijar» cambian de sentido a propósito, y el commit y el informe lo dicen. Si decido un ADR nuevo, se escribe con docs/adr/0000-template.md, se comprueba que su número está libre y entra en el índice de docs/adr/README.md.
>
> TESTS QUE ROMPEN A PROPÓSITO
> - Por cada cambio de motor, el test que falla con el código de main y pasa con el de la rama (skill comparar-con-main), con las dos salidas en el informe.
> - Uno que demuestre que una «en parte» no puede entrar en el conjunto de RESUELTAS de test_kit.py.
> - Todo test que necesite data/ se salta en la CI de Linux, como los demás.
>
> HOLDOUT
> - Nunca listes knowledge/cases ni ninguna carpeta madre de meses reservados con un filtro detrás (grep, grep -v, awk): las rutas se nombran literales en el propio comando. Ya ha pasado cuatro veces, la última con el propio revisor: dale también esta regla a él.
> - Toda exposición, aunque sea dudosa, el mismo día en docs/validation/HOLDOUT-EXPOSICIONES.md y en el informe.
> - Ninguna fecha de día reservado ni ningún resultado de operación en nada de lo que escribas.
>
> ENTREGA (skill entregar-rama)
> - CI de Linux con git push origin trabajo/activar-sesion-04:refs/heads/fix/activar-sesion-04, y el número de run; solo se acepta el fallo de state check.
> - Si el clasificador niega un push o la guardia un make, no lo rodees: dame el comando exacto y lo lanzo yo con «!».
> - Revisor con el informe terminado y dos alcances: (1) cada ambigüedad cerrada tiene sus cinco sitios, su test y su Fuente:, ninguna «en parte» se cerró y nada contradice un ADR sin otro ADR; (2) ninguna cita del informe ni de HOLDOUT-EXPOSICIONES.md cae en un tramo no citable, márgenes incluidos. Su informe, pegado al final.
> - Al final del informe, las líneas preparadas para el commit del contrato: E y H de la Next Action, S (julio va después de E), los heredados 15 y 37, R1.1 y R4.1 de la hoja de ruta, y la referencia NA:P de R0.1 (P ya está HECHA: di si el test la admite y si conviene tocarla).
>
> Rama lista para revisión, NO cerrada.
