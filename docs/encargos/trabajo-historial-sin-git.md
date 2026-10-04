# Encargo · trabajo/historial-sin-git

Dado por Aleks (consultor) el 2026-10-03. Copiado tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Rama nueva: trabajo/historial-sin-git, desde main en 48ccbd2 (commit de estado sobre el merge c76aaf6, tag stable/F36t-reabrir-y-fuente-documental). Ábrela con la skill abrir-rama: encargo en docs/encargos/, contrato.yaml y archivo en HISTORIA. Copia este prompt tal cual al encargo, con fecha 2026-10-03.
>
> OBJETIVO
> Ninguna comprobación de knowledge validate afirma lo que no evaluó. Hoy, sin git, las comprobaciones de historial imprimen «historial intacto» o «solo-añadir intacto» sin haber comprobado nada (docs/validation/REABRIR-Y-FUENTE-DOCUMENTAL.md §4.2: transcripciones, fotogramas, manifiestos, libros, días retirados, feedback y evidencia). Es la deuda abierta en Technical Debt que apunta a ese informe.
>
> QUÉ NO CAMBIA
> Motor, spec, knowledge/, cifras y ambigüedades. Con git y el historial evaluable, la salida de knowledge validate es idéntica a la de hoy, línea por línea, y también su código de salida. Sin git, el código de salida tampoco cambia: lo nuevo son avisos, no errores (la garantía sigue siendo la CI, que tiene git).
>
> LA REGLA (nombra la condición, no los casos)
> Toda comprobación cuyo resultado depende del historial de git, cuando ese historial no se evaluó, por la causa que sea (sin git, o con git pero historial_evaluable() diciendo que no se puede), no imprime «intacto». Imprime un AVISO que dice que NO se comprobó y por qué, igual que ya hace aviso_sin_git con las fuentes documentales. Niega por defecto: que una comprobación de historial nueva no pueda imprimir «intacto» sin pasar por el mismo mecanismo. Si la forma natural es una función común por la que pasen todas, hazlo así; si no, justifícalo en el informe.
>
> FASE 0 · Inventario, sin tocar nada
> Lista en el informe todas las comprobaciones que dependen de con_git o de historial_evaluable (busca en src/botsito/validation/knowledge.py y en lo que llama, como src/botsito/corpus/libros.py), no solo las siete de §4.2. Para cada una: qué imprime hoy con git, sin git y con historial no evaluable. Mide la salida real de validar sobre una copia sin .git (la de test_kit.py) y sobre una con historial no evaluable si se puede montar; si no se puede, dilo. Sigue sin esperarme, salvo que encuentres una comprobación que, sin git, cambie algo más que un mensaje (que deje pasar un error real, por ejemplo). En ese caso para y dímelo.
>
> FASE 1 · El cambio
> - Cada comprobación del inventario, sin historial evaluado, emite su AVISO de «NO se comprobó» y su línea OK deja de decir «intacto» (que diga lo que sí comprobó, si comprobó algo).
> - Con git, nada cambia.
>
> TESTS, cada uno roto a propósito antes de darlo por bueno
> 1. Sobre la copia sin .git: ninguna línea de la salida contiene «intacto», y hay un aviso por cada comprobación del inventario. Rómpelo devolviendo a una de ellas su OK de antes: tiene que fallar.
> 2. El mecanismo común (o lo que lo sustituya): una comprobación de historial falsa que imprime «intacto» sin pasar por él tiene que hacer fallar un test.
> 3. Con git: la salida de validar sobre el repo real es la misma que en main. Rómpelo cambiando una palabra de un OK: tiene que fallar.
> 4. Si montaste el caso de historial no evaluable, su test con su rotura. Si no, dilo en el informe.
>
> CI DE LINUX
> Esto depende del entorno (git presente o no). Empuja con el nombre que manda docs/runbooks/RITUAL.md (léelo antes, no lo supongas): git push origin trabajo/historial-sin-git:refs/heads/fix/historial-sin-git. La CI tiene que salir con solo el fallo esperado de state check por el nombre fix/. Dame el número de run.
>
> CIERRE DE LA DEUDA
> La línea de Technical Debt de PROJECT_STATE que apunta a §4.2 se quita en la rama que la paga, que es esta; su registro va a HISTORIA al cerrar, como manda RITUAL.md. No añadas nada más a PROJECT_STATE.
>
> INFORME Y REVISOR
> Informe en docs/validation/HISTORIAL-SIN-GIT.md: inventario, el cambio, los tests con su rotura y su resultado, el run de la CI y make check sellado. Después, el subagente revisor, con su informe pegado al final.
>
> Rama lista para revisión, NO cerrada.
