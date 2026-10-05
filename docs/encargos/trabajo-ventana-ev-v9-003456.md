# Encargo · trabajo/ventana-ev-v9-003456

Dado por el consultor el 2026-10-05. Copiado tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Rama nueva trabajo/ventana-ev-v9-003456, desde main en fffaa03 (commit de estado; tag stable/F36y-filtradas-con-tramos en 06adac1). Ábrela con la skill abrir-rama: encargo en docs/encargos/, contrato.yaml y archivo de PROJECT_STATE en HISTORIA. Es el punto R del Next Action.
>
> OBJETIVO: corregir, por el régimen de la evidencia, la ventana declarada de ev-v9-003456-9ef48fb5. Hoy empieza en 2.096.000 ms, sobre la cola del segmento 612, que está en cuarentena (FILTRADAS-ESCENARIO-B.md §4.1). Sus palabras citadas caen todas en el segmento 613.
> NO CAMBIA: el motor, la spec, el texto de la cita, ningún otro ítem ni ninguna línea ya escrita de tramos_no_citables.yaml.
>
> MATERIAL: v9 es material en cuarentena. Mide solo con n, t0_ms y t1_ms de los segmentos, por la misma vía que ancla_v9.py (contexto.crudas y verificar_citas, el llamador autorizado). No imprimas texto, palabras ni longitudes de cita. No abras ninguna filtrada de v7–v10: se rehacen en la fase 0 de la activación de E y hasta entonces nadie las lee. Si algo te obliga a ver texto, para y avisa.
>
> FASE 0 · Inventario sin tocar nada. Entrégamelo antes de escribir:
> a) Qué régimen corrige la ventana de un ítem ev-* (sustitución o supersede, no edición). Cita CLAUDE.md o el ADR. Di si existe una vía por la CLI. Si la única vía rodea una guardia, no la uses: dilo y propón cómo autorizarla a la vista.
> b) Medida, por la vía de arriba: fin del segmento 612 y principio y fin del 613. La ventana nueva cumple a la vez estas condiciones:
>    - no solapa más de 0 ms ningún segmento en cuarentena ni ningún tramo no citable, incluido el de margen del punto c;
>    - verificar_citas da 0 problemas y 1 aparición;
>    - el inicio es un segundo entero, el más temprano que cumpla lo anterior.
>    Si el fin actual (2.100.000) deja de cumplir, dilo.
> c) Decisión del consultor: en esta rama entra, solo añadiendo, el tramo de margen 0:34:44–0:34:57 que se quitó en FILTRADAS-ESCENARIO-B §4.2 porque solapaba la ventana vieja. Comprueba que no solapa la ventana nueva más de 0 ms.
> d) Quién cita ev-v9-003456-9ef48fb5 (spec, feedback, ambigüedades, informes, anexos) y por qué régimen se mueve cada referencia si el id cambia: feedback solo añade y los informes cerrados se corrigen con recuadro.
> e) Si hay alguna comprobación que falle cuando la ventana declarada de un ítem ev-* solapa más de 0 ms un tramo no citable o un segmento en cuarentena. Si no la hay, propón dónde va. Nombra la condición, no una lista de ítems.
>
> FASES, tras mi visto bueno a la 0:
> 1. Sustitución del ítem por su régimen, con trailer Fuente: y la referencia a FILTRADAS-ESCENARIO-B.md §4.1.
> 2. Tramo de margen en tramos_no_citables.yaml, con Fuente:. El diff no quita ninguna línea.
> 3. Referencias movidas, cada una por su régimen.
> 4. La comprobación del punto e), si no existía. Lleva un test que la rompe a propósito con la ventana vieja (2.096.000) y otro que pasa con la nueva.
> 5. Comprobaciones, con su salida en el informe:
>    - uv run botsito knowledge validate: exit 0, sin ERROR;
>    - uv run python scripts/ficheros_con_ocultos.py: OK, o regenerado con su diff;
>    - control positivo de tramos_registrados.py: 21 de 21 bloques de B de v9 y v10 caben enteros en un tramo, y 0 ítems ev-* de v7–v10 solapan un tramo más de 0 ms;
>    - make check sellado.
>    Si tocas hooks, rutas o algo que dependa de la plataforma, empuja también fix/ventana-ev-v9-003456 y dame el run de la CI de Linux.
>
> INFORME en docs/validation/VENTANA-EV-V9.md:
> - encargo frente a lo hecho;
> - desviaciones declaradas;
> - las medidas de la fase 0;
> - exposición en HOLDOUT-EXPOSICIONES.md el mismo día, si la hubo, o «ninguna» con el porqué;
> - tamaño de PROJECT_STATE.
> Pega al final el informe del revisor.
>
> Rama lista para revisión, NO cerrada.
