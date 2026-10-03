# Encargo · trabajo/renovar-cierres

Dado por Aleks (consultor) el 2026-10-03. Copiado tal cual:

> Modelo: Opus · Esfuerzo: medio
>
> Rama nueva trabajo/renovar-cierres, desde main. Verifica antes de abrirla que main está en 60d540c con el tag stable/F36r-fuentes-ftmo como último stable/*, y si no coincide, para y dímelo. Ábrela con la skill abrir-rama: este prompt, tal cual, en docs/encargos/, más contrato.yaml y el archivo en HISTORIA.
>
> OBJETIVO: que el calendario de cierres (knowledge/cuentas/cierres/ftmo-2step-swing-100k.yaml, hoy con hasta: "2026-10-07") no caduque sin que nadie lo vea, y dejar escrito quién lo renueva y cuándo (regla de las guardas con fecha de fin).
> NO CAMBIA: el motor, la spec, el knowledge salvo ese YAML, ADR-0068 en su decisión, ni ninguna cifra de la estrategia.
>
> FASE 0, inventario sin tocar nada. Entrégamela antes de escribir nada:
> 1. Qué hace exactamente el código cuando el calendario ha caducado. Mídelo, no lo leas solo: ¿lo que se niega depende de la fecha simulada o de la fecha de hoy? ¿Se rompe una simulación sobre días históricos de construcción a partir del 8 de octubre? ¿Se rompe algún test o la CI? Escribe cada comando tal como lo ejecutas (uv run botsito … con todos sus flags) y lo que devuelve. Para no tocar el reloj del sistema, usa un test con la fecha inyectada o un worktree desechable.
> 2. Qué fuente cubre la semana del 4 al 10 de octubre y la siguiente: las Trading Updates de ftmo.com/en/blog/trading-updates/, la pauta semanal ya declarada y cualquier festivo de esas fechas que afecte a EURUSD o al servidor. Cita la URL y la fecha de consulta, y separa lo que dice la fuente de lo que supones.
> 3. El procedimiento más ligero que cumpla el ritual para renovar cada semana. Tocar el YAML en knowledge/ exige rama, merge y tag por la regla 5 de state check: mide si eso es así de verdad, no lo des por hecho. Propón quién lo hace (Claude Code con orden de Aleks), qué día y con qué aviso previo (por ejemplo, un aviso en make check o en state check cuando falten 3 días o menos para hasta:).
>
> FASE 1, tras mi visto bueno: renovar hasta donde la fuente lo cubra, nunca más allá; el aviso de caducidad próxima, si lo apruebo; y un runbook corto docs/runbooks/RENOVAR-CIERRES.md con el procedimiento, el responsable y el día.
> Tests que rompen la guardia a propósito: un calendario caducado tiene que fallar y uno a punto de caducar tiene que avisar. Comprueba que cada test falla con el defecto y pasa sin él.
> Si toca rutas o código que dependa de la plataforma, push como fix/trabajo-renovar-cierres y CI de Linux en verde antes del merge; dame los números de run.
> Informe en docs/validation/RENOVAR-CIERRES.md, con el revisor al final.
>
> Rama lista para revisión, NO cerrada.

## Segunda orden: decisiones del consultor sobre la Fase 0 (2026-10-03)

Copiada tal cual:

> Modelo: Opus · Esfuerzo: medio
>
> Decisiones del consultor sobre la Fase 0 de trabajo/renovar-cierres (2026-10-03). Cópialas con su fecha al informe docs/validation/RENOVAR-CIERRES.md:
>
> 1. No se renueva cada semana: ni la opción A ni la B. Motivo: hoy nadie consume el calendario en tiempo real y no hay fuente para el 8-10. Renovar a ciegas cada semana es coste sin efecto, y meter la renovación en otra rama mezcla un dato ajeno con el contrato de esa rama.
> 2. La renovación se ata a una condición, no al calendario. Hay dos casos:
>    a) Una simulación pide días posteriores a hasta: el simulador ya se niega (exit 2, nombrando los días) y en ese momento se renueva hacia atrás, con las Trading Updates archivadas de esas semanas, en una rama propia.
>    b) Antes de que el bot corra en tiempo real (demo o real): la rama que lo conecte trae la lectura de SymbolInfoSessionTrade (línea N, ADR-0068 §4) o un procedimiento de renovación que cierre el hueco del jueves por la mañana. Sin uno de los dos, esa rama no se cierra.
> 3. No hay aviso en state check ni comando botsito cierres check. Motivo: leer la fecha de hoy en make check y en la CI es una entrada global que cambia sola (patrón 1 de ERRORES-RECURRENTES), y un aviso que sale todas las semanas deja de leerse. La guardia que vale es la que ya existe: negarse por la fecha simulada.
> 4. El hueco del jueves se acepta mientras no haya bot en tiempo real. Lo resuelve el punto 2b.
> 5. Verifica antes de seguir, porque las decisiones 1 a 4 dependen de ello: busca si MedirDemoFTMO.mq5, scripts/leer_demo_ftmo.py o cualquier otra pieza que vaya a correr en la demo de FTMO lee knowledge/cuentas/cierres/. Si alguna lo lee, para y dímelo antes de la Fase 1.
> 6. El Columbus Day y todo lo que no tenga fuente siguen fuera del YAML. El YAML no se toca en esta rama.
>
> FASE 1, reducida:
> a) Pasa el «cable trampa» a un test permanente: cargar el calendario y simular un día fijo con el reloj del sistema saboteado (que lance una excepción si se lee) tiene que pasar. Rómpelo a propósito con una variante que lea el reloj y comprueba que falla. Así queda vigilado que los cierres dependen solo de la fecha simulada.
> b) Un test de que simular un día posterior a hasta se niega con exit 2 y nombra ese día. Si ya existe, cita cuál es y no lo dupliques. Rómpelo a propósito y comprueba que falla.
> c) El runbook docs/runbooks/RENOVAR-CIERRES.md, corto, con los dos casos del punto 2: cuándo se renueva, quién (Claude Code con orden de Aleks, en rama propia), de dónde sale el dato (Trading Updates archivadas, URL y fecha de consulta en el YAML) y la condición que bloquea la rama que conecte el bot en tiempo real.
> d) En el informe, di qué 2 tests fallan y cuáles 3 se saltan en el clon y por qué. Aclara también por qué cuentas 1855 tests cuando PROJECT_STATE dice 1208 funciones (¿parametrizados?).
> e) PROJECT_STATE no se toca en la rama: el texto nuevo de la línea N lo fijo yo en la orden de cierre.
>
> No hace falta la CI de Linux salvo que toques rutas o el sistema de archivos. Si las tocas, empuja como fix/trabajo-renovar-cierres y dame el número de run.
> Después, el revisor, con su informe pegado al final.
>
> Rama lista para revisión, NO cerrada.
