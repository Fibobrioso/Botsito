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
