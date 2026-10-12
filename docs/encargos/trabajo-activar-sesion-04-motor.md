# Encargo · trabajo/activar-sesion-04-motor

Dado por Aleks (consultor) el 2026-10-11. Copiado tal cual (el bloque de abajo no es del encargo:
declara los ids que el encargo cita y que todavía no existen, como exige `knowledge validate`;
cada uno sale de aquí en el commit que lo crea):

```ids-inexistentes
ADR-0076 — el ADR de A-21 que este encargo manda escribir (decisión 3); no existe hasta su commit
ADR-0077 — el ADR de A-51 que este encargo manda escribir (decisión 4); no existe hasta su commit
```

> Modelo: Fable 5.1 · Esfuerzo: alto
>
> Encargo del consultor (2026-10-11) · trabajo/activar-sesion-04-motor · tramo R1 (entrada R1.1 de la hoja de ruta; E de la Next Action)
>
> Rama nueva: trabajo/activar-sesion-04-motor, desde main d4b7917 (commit de estado sobre el merge del tag stable/F37m-activar-sesion-04, que apunta a cbe8e09; CI de main en verde según el cierre, run 38197306105: compruébalo con gh si puedes y, si no, dilo). Ábrela con la skill abrir-rama: base comprobada con git (su paso 1), contrato con tramo R1, riesgo alto (spec y motor), artefacto docs/validation/ACTIVAR-SESION-04-MOTOR.md. El recorrido lo mandan las skills activar-sesion (paso 3 por cada respuesta), comparar-con-main (los tests que rompen) y entregar-rama (entrega). Si este encargo y ellas chocan, ganan ellas y lo dices.
>
> OBJETIVO
> Que lo que la respuesta a la PARADA del 2026-10-11 (docs/encargos/trabajo-activar-sesion-04.md, puntos 1, 3, 4, 6 y 7) y la PARADA 2 dejaron para esta rama entre en la spec y en el motor, cada cosa con su test: CONFIRM de S-4, S-13, A-21, A-51 y el tramo ventana_fin de RN-035. Cópiate este encargo a docs/encargos/trabajo-activar-sesion-04-motor.md.
>
> QUÉ NO CAMBIA
> - Nada fijado se pisa: lo que una decisión de aquí cambia se cambia por su régimen (ADR que enmienda, con recuadro en el enmendado y fila del índice; CORRECT sobre la regla; RESOLVE_UNKNOWN sobre la ambigüedad).
> - A-49 sigue ABIERTA y no se toca. Ninguna «en parte» se cierra. A-35 y A-44 no se tocan: --diagnostico-a35 y --diagnostico-a44 siguen.
> - «Casi plana» (RN-007, H, S-14) NO se resuelve aquí: sin umbral.
> - RN-020 no cambia (ni su prosa ni lo que hace con una orden pendiente).
> - Ninguna cifra dentro de una forma ejecutable (ADR-0002): el 9 de A-51 vive en parametros.yaml.
> - Sin arnés y sin medidas agregadas sobre material: todo con tests sintéticos.
> - Nada de material: ni julio (S), ni diciembre (I), ni marzo, ni febrero, ni la cruda de v10. Citas, solo las que SESION-04-EXTRACCION.md dejó citables, cruzadas con knowledge/corpus/tramos_no_citables.yaml, márgenes incluidos.
> - La Next Action y la hoja de ruta no se tocan en la rama: sus líneas van en el informe para el commit del contrato del cierre.
> - El Makefile, .claude/ y la guardia no se tocan.
> - Los informes cerrados de docs/validation que nombran --diagnostico-a21 no se editan: son histórico.
>
> FASE 0 (corta, sin tocar nada; skill fase-cero)
> Inventario en el informe, con fichero:línea: (1) que existen las evidencias ev-v10-004945-59ebac47 (S-4), ev-v10-014005-7e2228f4 y ev-v10-014040-fb7a153b (S-13), ev-v10-011725-3741e266, ev-v10-011734-fedd3f8e y ev-v10-011957-7ebb3453 (S-10), ev-v10-010653-81316808, ev-v10-010715-fae17215, ev-v10-010804-5b6ad1a3 (S-8) y ev-v9-011128-a267338b, y el registro fb-2026-10-04-sesion-04-45e624c5 (S-5); (2) que ADR-0075, ADR-0076 y ADR-0077 y RN-036 están libres; (3) todo lo que produce o consume el valor ambiguo del sesgo (src, scripts, visor, spec, tests); (4) todo lo que nombra --diagnostico-a21 (mi lista: cli.py, engine/zonas.py, el campo a21 de engine/diagnostico.py, y los tests test_preparar_a21, test_preparar_a35, test_visor, test_renovar_cierres, test_rutas_windows y test_selector_orden_stop); (5) el ADR que fija hoy cada cosa que se toca: grep del id del parámetro, de la regla y de la ambigüedad en docs/adr (lección de ERRORES-RECURRENTES de activar-sesion-04).
> PARADA solo si algo de lo medido contradice una decisión de abajo, si el valor ambiguo del sesgo sale de algún sitio además de la H4 neutra, o si alguna decisión necesita tocar algo de «QUÉ NO CAMBIA». Si no, sigue y lo dices.
>
> DECISIONES (ya tomadas; cada una en su propio commit, en este orden)
>
> 1. CONFIRM de S-4 (PARADA 2, opción b). Primer commit: uv run botsito feedback new … --objetivo-tipo evidence --objetivo-id ev-v10-004945-59ebac47 --accion CONFIRM, con las opciones obligatorias de la plantilla (knowledge/feedback/README.md). A-49 sigue ABIERTA. feedback pending puede listarlo como «sin forma mecánica de comprobarlo», igual que los de la sesión 1: dilo.
>
> 2. S-13 · ADR-0075: una H4 neutra mantiene el sesgo. Enmienda ADR-0060 §1 y §2 (la vela sin cuerpo con doble ruptura ya no fija el sesgo ni da ambiguo: no decide, y la búsqueda sigue hacia atrás como en ADR-0044 §2). Recuadro en 0060 y su fila del índice como «ACTIVE (con enmienda de ADR-0075)».
>    - Neutra = cierre == apertura exacto, que es lo que ya hace sesgo.py. El trader dice que con 1 o 2 puntos de cuerpo ya cuenta el color: no hay umbral en H4.
>    - Reserva escrita en el ADR y en las notas de RN-003: lo dijo con sesgo previo alcista. La confirmación del caso bajista va a la lista de la sesión 5.
>    - Spec: CORRECT sobre RN-003 citando ev-v10-014005-7e2228f4; las notas de RN-033 dicen que queda solo para insuficiente (la prohibición de operar sin lado sigue saliendo de ADR-0044 y ADR-0049).
>    - El token ambiguo se queda declarado en la spec y en Sesgo, porque lo usan scripts y el visor, con su descripción diciendo que el motor ya no lo produce desde ADR-0075. Retirarlo es deuda: va en las líneas del cierre (G.2).
>    - spec_version según la regla del propio manifiesto (una regla cambia de sentido: mayor). Se sube A MANO en knowledge/spec/spec_manifest.yaml; luego spec manifest --escribir y spec docs --escribir.
>    - Motor: en sesgo.py, la rama del AMBIGUO pasa a seguir buscando. Tests que cambian de sentido a propósito: test_sesgo_h4.py (test_doble_ruptura_sin_cuerpo_es_ambiguo) y lo que congela ambiguo en test_huecos_motor.py (mídelo: el auditor lo sitúa hacia :171-192, :202, :305 y :341). Uno nuevo con dos neutras seguidas y otro con neutra tras sesgo bajista.
>
> 3. A-21 · ADR-0076. Opción nueva sin_alternancia_de_colores, que se SUMA al enum de zona_control_limpia: ningún cambio de color de una M1 a la siguiente en el retroceso, desde el fin del bloque de origen hasta la vela que rompe (excluida). Cierre de A-21: RESOLVE_UNKNOWN del trader (S-10) y registro de parámetro con ese valor, CONFIRMED vía feedback apply.
>    - Decisión del consultor, en ADR-0076 y aparte del registro del trader: una vela sin cuerpo (cierre == apertura, color 0 en pivotes_m15.color) no cuenta como cambio de color: se salta. Coherente con fb-2026-09-29-sesion-03-ffab23dc, que habla de la vela «casi plana»; su umbral sigue abierto (H, S-14) y el ADR dice que aquí solo se salta la vela de cuerpo cero.
>    - La opción entra en LECTURAS_LIMPIA, en detectar_esquema y donde zonas.py la despache.
>    - Se retira --diagnostico-a21: cli.py, zonas.py, el campo a21 de diagnostico.py y sus tests, que cambian de sentido a propósito. Como ADR-0055 creó ese flag, ADR-0076 lo enmienda en esa parte, con recuadro y fila del índice.
>    - Cinco sitios de AMBIGUEDADES.md:
>      · A-21 sale de ORDEN_SESION_02 (scripts/hoja_preguntas.py) y de ORDEN en test_hoja_preguntas.py;
>      · test_kit.py: A-21 entra en RESUELTAS y sale de las bloqueantes ABIERTAS;
>      · la tabla de Known Ambiguities se prepara para el cierre.
>    - La tabla de opciones de docs/runbooks/ACTIVAR-A35-A44.md §6 gana la opción nueva; el resto del runbook no se reescribe.
>
> 4. A-51 · ADR-0077 y RN-036, aparte de RN-020. Cuatro parámetros del trader (no de ejecución), CONFIRMED vía feedback apply:
>    - racha_perdidas_max = 9 (ev-v10-010653-81316808; ya en v9, ev-v9-011128-a267338b). Su descripción lleva la nota de SESION-04-EXTRACCION.md §4.8: las 9 pérdidas vienen de una cuenta con un 0,5 % de riesgo, y el bot también arriesga un 0,5 %.
>    - racha_perdidas_corte = ganadora, enum [ganadora, ganadora_o_break_even] (ev-v10-010715-fae17215: el break even no la corta).
>    - racha_perdidas_reinicio = nunca, enum [nunca, fin_de_dia, fin_de_semana] (ev-v10-010804-5b6ad1a3).
>    - racha_perdidas_reanudacion = dia_siguiente, enum [dia_siguiente, semana_siguiente, sin_fecha] (ev-v10-010804-5b6ad1a3).
>    Lo que cuenta como pérdida es lo mismo que gasta un cartucho en RN-016 (cartucho_criterio): no se inventa otra definición.
>    - El acumulador persiste entre días. Vive junto a SeguidorTope o la cuenta, nunca en EstadoDia (nace de cero cada día, ADR-0053 §6), y respeta cuenta_diaria como lo hace el seguidor.
>    - «Día siguiente» se cuenta con reloj_sesiones (ADR-0063): tras la novena no se opera más en ese día de operativa, y se vuelve en la primera sesión del día siguiente. El ADR dice por qué: la ventana entera cae dentro de un día civil.
>    - Decisión del consultor, en el ADR: al llegar a la novena, RN-036 prohíbe abrir y además RETIRA la orden pendiente que quede (el broker la llenaría por ticks, y el trader deja de operar).
>    - RN-036 no lee ningún parámetro de A-44. Si para correr necesita --diagnostico-a44, PARADA.
>    - RN-036 lleva cita propia: las tres guardias de spec/modelo.py (comprobar_contra, comprobar_literales, comprobar_citas_revocadas) en el mismo commit.
>    - Cinco sitios: A-51 no está en la hoja de preguntas, así que no hay nada que quitar, y se dice; test_kit.py: A-51 a RESUELTAS y fuera de las bloqueantes (quedan A-35 y A-44).
>    - Tests: nueve pérdidas seguidas con un break even en medio detienen hasta el día siguiente; una ganadora a la octava la pone a cero; la racha cruza un fin de semana; la orden pendiente se retira en la novena.
>
> 5. RN-035, tramo ventana_fin. La forma de RN-035 gana la rama: al llegar a ventana_fin con una orden pendiente, se retira, según orden_pendiente_al_abrir_sesion (se_retira). Es la respuesta de S-5 (fb-2026-10-04-sesion-04-45e624c5), en el instante que dijo el trader: «un minuto antes» es frase del consultor y no se fija.
>    - Las notas de RN-035 quitan «LO QUE ESTA REGLA NO HACE TODAVIA».
>    - La cancelación del cableado al terminar el día (ADR-0053 §6) se queda como red de seguridad. Un test exige que a ventana_fin la retirada la haga RN-035 (con su motivo en el journal o en las decisiones del motor) y que el cableado ya no encuentre nada que cancelar.
>    - Hueco que no se arregla aquí: una orden pendiente puede llenarse en el último minuto de la H4 [fin−1, fin), después de que RN-002 cierre, tanto a las 11 como a ventana_fin. Mídelo con un test sintético que congele lo que pasa hoy, y escribe la pregunta para la sesión 5 en el lenguaje del trader («¿la orden que no se llenó la quitas a las 11 y a las 3 en punto, o cuando cierras la operación un minuto antes?», con opciones y «otra, ¿cuál?»).
>
> Por cada commit, el paso 3 de activar-sesion entero:
> - registros con todas las opciones obligatorias;
> - feedback apply --check, que propone SOLO los de esa respuesta, y después sin --check;
> - los cinco sitios;
> - test_kit.py;
> - spec_version a mano, más manifest y docs --escribir;
> - el código con su test;
> - uv run botsito knowledge validate antes de make check;
> - trailer Fuente: en el CUERPO, con ids fb-* que existen.
> Los ADR nuevos se escriben con docs/adr/0000-template.md y entran en el índice. Si make check da un MemoryError de lzma en tests/unit/test_ticks.py (dato conocido, ajeno a la rama), repítelo una vez; si se repite, dame la salida y el comando exacto, y lo lanzo yo.
>
> TESTS QUE ROMPEN A PROPÓSITO
> - Por cada cambio de motor (decisiones 2 a 5), el test que falla con el código de main y pasa con el de la rama (skill comparar-con-main), con las dos salidas en el informe.
> - Uno que demuestre que detectar_esquema con una lectura fuera de LECTURAS_LIMPIA sigue fallando.
> - Uno que demuestre que una «en parte» (A-49) no puede entrar en RESUELTAS de test_kit.py.
> - grep de --diagnostico-a21 y diagnostico.a21 en src/ y tests/: vacío, con la salida en el informe.
> - Todo test que necesite data/ se salta en la CI de Linux, como los demás.
>
> HOLDOUT
> - Nunca listes knowledge/cases ni ninguna carpeta madre de meses reservados con un filtro detrás (grep, grep -v, awk): las rutas se nombran literales en el propio comando. Ya ha pasado cuatro veces: dale también esta regla al revisor.
> - Toda exposición, aunque sea dudosa, el mismo día en docs/validation/HOLDOUT-EXPOSICIONES.md y en el informe.
> - Ninguna fecha de día reservado ni ningún resultado de operación en nada de lo que escribas.
>
> Si antes de la entrega te pego lo que oí en 1:44:49 de v10 («1 o 2» o «12»), va al informe y a las líneas de H; si no, H se queda como está.
>
> ENTREGA (skill entregar-rama)
> - CI de Linux con git push origin trabajo/activar-sesion-04-motor:refs/heads/fix/activar-sesion-04-motor, y el número de run; solo se acepta el fallo de state check.
> - Si el clasificador niega un push o la guardia un make, no lo rodees: dame el comando exacto y lo lanzo yo con «!».
> - Revisor (opus), con el informe terminado y cuatro alcances:
>   (1) A-21 y A-51 tienen sus cinco sitios, su test y su Fuente:; ninguna «en parte» se cerró; A-49 no se tocó;
>   (2) ADR-0060 y ADR-0055 llevan su recuadro y su fila del índice; nada contradice un ADR sin otro ADR;
>   (3) cada test de motor falla con main;
>   (4) ninguna cita del informe ni de HOLDOUT-EXPOSICIONES.md cae en un tramo no citable, márgenes incluidos.
>   Su informe va pegado al final.
> - Al final del informe, las líneas preparadas para el commit del contrato:
>   · E sale a HISTORIA como HECHA; F apunta a lo siguiente según la hoja de ruta (propónlo);
>   · R1.1: su estado (la parte de motor, hecha; queda que las «en parte» entren en la hoja de la sesión 5, R4.1);
>   · R3.1: Refs y «Depende de» sin A-21 (quedan A-35 y A-44);
>   · R4.1: gana la pregunta del último minuto de la decisión 5 y pierde A-21 de sus Refs;
>   · heredados 25 y 30: lo que cambia porque A-21 ya está RESUELTA;
>   · G.2: --diagnostico-a47 y --diagnostico-a27 siguen; el token ambiguo es deuda;
>   · Known Ambiguities: A-21 y A-51;
>   · y dos notas:
>     – que RN-020 tampoco retira la orden pendiente al llegar a su tope, para cuando se active A-44 (heredado 35);
>     – que ADR-0070 §3 dice «hoy A-21, A-35 y A-44»: no lo edito; lo dice R3.1.
>   · La lista de la sesión 5, actualizada: sale el punto 11 (A-21) y entran la confirmación bajista de S-13 y la pregunta del último minuto.
>
> Rama lista para revisión, NO cerrada.

## Añadido de Aleks en la misma conversación (2026-10-11), tras abrir la base

Llegó mientras se comprobaba la base (paso 1 de `abrir-rama`). Copiado tal cual:

> TRABAJO NOCTURNO (Aleks no está hasta mañana)
> - Nada se queda esperando una respuesta mía: lo que dependa de mí se apunta en una sección «Pendiente de Aleks» al principio del informe, con el comando exacto, y sigues con lo que no dependa de eso.
> - Si el clasificador niega el push a fix/activar-sesion-04-motor, no lo rodees: deja el comando en «Pendiente de Aleks», lanza igualmente el revisor sobre la rama y deja la CI para la mañana.
> - Si la fase 0 da una PARADA, escríbela entera en el informe, deja commiteado lo que no dependa de ella (como mínimo el CONFIRM de S-4) y para ahí: no decidas por mí.
> - Si el MemoryError de test_ticks se repite, apúntalo con la salida y sigue con knowledge validate y los tests de los ficheros tocados; el make check completo lo lanzo yo por la mañana.
> - Todo commiteado en la rama local antes de terminar. Nunca se cierra la rama.
