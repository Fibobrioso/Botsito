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

## Segunda orden: respuesta del consultor (2026-10-03)

Copiada tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Respuesta del consultor a trabajo/historial-sin-git (2026-10-03). Cópiala con su fecha al informe y al final del encargo.
>
> 1. La guardia nombra la condición, no las palabras. Hoy Historial reconoce la afirmación por su texto («intacto», «commits con Fuente»), y una comprobación nueva que diga «íntegro» se escaparía: lo dejaste escrito como límite y lo vio el revisor. La condición real es «esta comprobación lee el historial de git». Mide primero si las primitivas que leen git en src/botsito/validation/ (las que sean: hay_git, historial_evaluable, contenido_en_head, resolver, ancla_desviada y las que encuentres) están centralizadas. Si lo están, añade un test que recorra src/botsito/validation/ con ast y falle si alguna de esas primitivas se llama fuera de Historial (o de una lista explícita de excepciones, cada una con su porqué en un comentario). Rómpelo a propósito con una comprobación falsa que llame a una primitiva directamente. La comprobación por palabras se queda como segunda red. Si las primitivas NO están centralizadas y hacerlo exige tocar más que validation/, no lo hagas: para, dímelo con lo medido y añade una línea a Technical Debt que apunte al informe.
> 2. Las dos comprobaciones que callan sin git (las anclas de paquetes, fidelidad y dev-visto, y la subida de spec_version): aceptado, no se tocan en esta rama. No afirman nada, pero el encargo de la rama anterior pedía que sin git nada saliera en silencio. Una línea corta en Technical Debt que apunte a §3 de tu informe. PROJECT_STATE tiene que seguir por debajo de 25 KB: di su tamaño.
> 3. El push: empuja todo, el informe incluido, a fix/historial-sin-git (git push origin trabajo/historial-sin-git:refs/heads/fix/historial-sin-git). CI de Linux con solo el fallo esperado de state check; dame el número de run. La CI revisa también documentos, así que un commit de solo documentación no se queda fuera.
> 4. El revisor revisó un informe a medias. Pasada corta del revisor sobre el informe ya completo y sobre lo que cambie por los puntos 1 y 2, con su informe pegado al final. Para el cierre, la lección que irá a la fila de ERRORES-RECURRENTES de esta rama: el revisor se lanza con el informe terminado, nunca antes.
> 5. El clon superficial no montado para no copiar el holdout: aceptado, con ese motivo escrito en el informe, como ya está.
>
> make check sellado antes de cada commit.
>
> Rama lista para revisión, NO cerrada.

## Orden de cierre del consultor (2026-10-03)

Copiada tal cual:

> Modelo: Opus · Esfuerzo: medio
>
> Orden de cierre de trabajo/historial-sin-git (consultor, 2026-10-03). Cópiala con su fecha al informe y al final del encargo. Se ejecuta cuando Aleks escriba /cerrar-rama trabajo/historial-sin-git; hasta entonces no hagas nada más.
>
> Tag: stable/F36u-historial-sin-git. Antes de usarlo, comprueba en HISTORIA que la última letra cerrada es la t; si no lo es, usa la siguiente libre y dilo.
>
> En el commit que saca el contrato, además de lo que manda RITUAL.md:
> 1. Informe, hallazgo a1 del revisor: en §1.4, donde dice «seis funciones» y «los seis pasan», añade «(siete tras §6.1, 1246)». No reescribas nada más.
> 2. Informe, hallazgo a2: en §6.1, junto al límite ya declarado, añade que el test tampoco ve __import__ ni importlib, y que solo recorre los *.py de primer nivel de validation/ (glob, no rglob). No se cambia código: es límite declarado.
> 3. Fila de la rama en ERRORES-RECURRENTES, con los hallazgos del consultor que el revisor no vio:
>    - importa: en la primera vuelta, el commit del informe (ac08b5a) se quedó sin push a fix/ y sin CI, y el revisor no lo señaló. Lección para el revisor: comprobar que el último commit de la rama, el que se va a fusionar, tiene su run de CI, no solo el commit del código.
>    - menor: el revisor se lanzó la primera vez con el informe sin terminar. Lección (§6.4): el revisor se lanza con el informe terminado, nunca antes.
>    - menor: la guardia de la primera vuelta reconocía palabras («intacto») en vez de la condición (leer git). Lo vio el revisor; se apunta como un caso más del patrón «nombra la condición, no los casos».
> 4. El registro del cierre en HISTORIA, con la deuda de §4.2 de REABRIR-Y-FUENTE-DOCUMENTAL.md como pagada.
>
> Después, el ritual completo: merge --no-ff, tag, commit de estado que solo sustituye Current Branch, Current Feature, Stable Main State y Last Stable Commit (Next Action no cambia), state check, make check sellado, push atómico de main y el tag, CI de main en verde y, solo entonces, borrar la rama local y fix/historial-sin-git de origin.
>
> Informe final: sha de main, tag, run de la CI de main, ramas que quedan en local y en remoto, y tamaño de PROJECT_STATE.
