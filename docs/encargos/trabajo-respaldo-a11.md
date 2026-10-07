# Encargo · trabajo/respaldo-a11

Dado por Aleks (consultor) el 2026-10-07. Copiado tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Rama nueva trabajo/respaldo-a11, desde main d96b70377c56bf877344f4a64aec865ee760793d (commit de estado sobre el merge 363f826, tag stable/F37d-activacion-a42). Comprueba ese sha antes de empezar y ábrela con la skill abrir-rama (encargo en docs/encargos/, contrato.yaml, archivo en HISTORIA). Copia este prompt tal cual al encargo.
>
> Objetivo: cerrar el punto U de la Next Action. A-11 pasa a respaldarse en una decisión del consultor con ADR, sale la excepción de G1 y se decide el hallazgo §8.3 de GUARDIAS-CITAS.md. NO cambia: el motor, el bróker simulado, ningún valor de parametros.yaml ni de strategy_spec.yaml (stop_en_orden_pendiente sigue en en_la_orden), ningún ítem de evidencia y ninguna cifra.
>
> Decisión del consultor (2026-10-06), con fecha y fuente en todo lo que escribas:
> D1. A-11: el stop se pone en la misma orden pendiente, no al llenarse. Fundamento: (1) impuesto por el mundo: el bot no puede quedar con una posición abierta sin stop en el servidor mientras ve el llenado (corte de conexión, límite de pérdida diaria de FTMO); (2) coincide con la respuesta referida del trader del 2026-09-10 (fb-2026-09-09-sesion-01-76fd91ba), que ya es la fuente de stop_en_orden_pendiente; (3) en fidelidad solo cambiaría algo si el precio tocara el 0,8 en el mismo instante del llenado. Ningún ítem activo lo dice en su cita (GUARDIAS-CITAS.md §9.2), y no se le vuelve a preguntar al trader (ACTIVACION-A42.md §5.4).
> D2. §8.3: no se construye ninguna comprobación automática de afirmación frente a cita (es un juicio de significado). Se añade al revisor, en su checklist o su definición, una comprobación: «en cada ítem de evidencia nuevo de la rama, la afirmación no dice nada que su cita no contenga». ev-v6-021939-b430a110 no se toca (evidencia inmutable), y el informe deja escrito que su afirmación excede su cita y que no respalda el momento del stop.
>
> Fase 0, sin tocar nada, con entrega y PARADA antes de escribir:
> a) A-11 en knowledge/spec/ambiguedades.yaml: estado, clase (hoy no la tiene), evidencia y pregunta, con sus líneas.
> b) Cómo se cierra una ambigüedad como DECIDIDA: campos exigidos, si pide ADR, si exige clase, y si el régimen de cambio deja pasar de RESUELTA a DECIDIDA una ambigüedad ya cerrada sin cambiar su valor. Cítalo de docs/runbooks/AMBIGUEDADES.md, CLAUDE.md, ambiguedades.py y su test. Si el régimen no lo permite, PARA y propón la vía, sin elegirla.
> c) La excepción de G1 (el par A-11 con su id) y su test de caducidad: dónde están y qué hay que tocar para que la excepción salga en el mismo commit.
> d) Quién cita hoy A-11 y el id supersedido, y si algo más se rompe al quitarlo.
> e) Dónde se define el revisor (agente, skill o checklist) y si añadir D2 toca .claude/.
> f) El siguiente número de ADR libre (verifica en docs/adr/README.md que lo es).
>
> Fases tras mi respuesta:
> 1. ADR nuevo con D1: problema, alternativas (esperar al trader, citar un ev con lectura forzada, DECIDIDA) y por qué. Restricción impuesta por el mundo, declarada como tal.
> 2. A-11 a DECIDIDA según b), sin el id supersedido; sale la excepción de G1 y su test queda coherente: la guardia pasa sin ninguna excepción y sigue fallando con cualquier par supersedido (test que lo rompa a propósito). spec docs regenerado.
> 3. D2 en el revisor, y en el informe la nota sobre b430a110.
> 4. PROJECT_STATE: la línea de Technical Debt «A-11 RESUELTA cita un ítem supersedido…» sale a HISTORIA bajo «# Technical Debt PAGADA». La Next Action no se toca aquí: U sale en el commit del contrato con la orden de cierre. El saldo de bytes de PROJECT_STATE tiene que ser menor o igual que cero.
>
> Antes del primer make check, uv run botsito knowledge validate. Después, make check y uv run botsito state check en verde. Si la rama toca .claude/, empuja fix/respaldo-a11 y pasa la CI de Linux (el único fallo aceptado es test_state_check_ok_on_real_repo, por el nombre fix/), y dame el número de run. Si el clasificador te niega el push, dame el comando exacto para lanzarlo yo con «!» y no lo rodees.
>
> Nada de material reservado ni de cuarentena: esta rama solo lee yaml de spec, código y docs. Si algo te lleva a una transcripción o a un libro, PARA.
>
> Informe en docs/validation/RESPALDO-A11.md: encargo frente a lo hecho, desviaciones, comandos y salidas. Revisor con su informe pegado al final, comprobando aparte que G1 no tiene ninguna excepción y que su test de rotura falla cuando debe.
>
> Rama lista para revisión, NO cerrada.
