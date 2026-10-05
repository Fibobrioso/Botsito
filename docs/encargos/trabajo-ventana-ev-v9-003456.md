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

## Decisiones del consultor tras la fase 0 (2026-10-05)

Copiadas tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Visto bueno a la fase 0 de trabajo/ventana-ev-v9-003456, con estas decisiones. Cópialas al encargo y al informe con fecha 2026-10-05, como decisiones del consultor:
>
> 1. Vía de (a): AUTORIZADA a la vista. Es el anexo que carga el ítem viejo y llama a escribir_item con _EntornoEvidencia.comprobar, la misma comprobación que evidence new --supersede.
>    Porqué: la CLI obliga a leer y reescribir texto en cuarentena, y el anexo pasa por la misma comprobación. No es un rodeo.
>    Condiciones:
>    - el anexo vive en docs/validation/anexos/ y cita el archivo y la línea de la CLI que replica;
>    - comprueba que el ítem nuevo es igual campo a campo al viejo, salvo id, t0, supersede, notas y los campos de fecha o autoría que el modelo genere solo. Lista en el informe los campos que cambian;
>    - solo imprime el id nuevo y el resultado de la comprobación.
>    revisado_por lleva el mismo valor que el ítem viejo, porque la cita no cambia. notas dice: «ventana corregida por orden del consultor, 2026-10-05, VENTANA-EV-V9.md; la cita no se releyó». Si notas no admite texto libre, dímelo antes de escribir.
>
> 2. Orden de las fases. Primero el tramo de margen 0:34:44–0:34:57 (fase 2), con Fuente:, sin quitar ninguna línea. Después el anexo, en dos pasadas:
>    - con t0 = 2.096.000, la comprobación TIENE que rechazar el ítem por tramo_no_citable. Pega la salida en el informe. Si lo acepta, para: la vía no pasa por la guardia y no está autorizada;
>    - con t0 = 2.097.000, escribe el ítem nuevo, que supersede a ev-v9-003456-9ef48fb5. Fin en 2.100.000.
>    Porqué: así se demuestra que la vía pasa por la guardia y no la rodea.
>
> 3. A-46: SUSTITUIR el id viejo por el nuevo en ambiguedades.yaml, con Fuente:, y regenerar con uv run botsito spec docs --escribir.
>    Porqué: la spec tiene que citar el ítem activo, y si deja el viejo cita una ventana que pisa un tramo.
>    Mide y di en el informe si algo avisa hoy cuando la spec o las ambigüedades citan un ítem supersedido. Si nada avisa, añade una línea a Technical Debt que apunte a este informe. No lo arregles en esta rama.
>
> 4. Control de la fase 5: se cuentan los ítems ACTIVOS (los que nadie supersede). El anexo nuevo declara cuántos supersedidos deja fuera (se espera 1) y cuáles son.
>    Porqué: un ítem supersedido no se cita.
>
> 5. La condición de (e): APROBADA tal cual la nombras. «La ventana declarada de todo ítem activo no se solapa más de 0 ms con ningún tramo no citable de su vídeo, ni con ningún segmento de su transcripción que a su vez solape un tramo.»
>    - Va en una función junto a tramo_no_citable, en evidence/verificacion.py. La llaman knowledge validate, para todos los ítems activos de todos los vídeos (no solo v7–v10), evidence new y evidence propose --check.
>    - Solo usa milisegundos de los segmentos, por la vía autorizada. Nunca texto.
>    - Antes de activarla, mídela sobre el repo con el ítem ya corregido. Tiene que dar 0 ítems. Si sale cualquier otro, para y entrégame la lista (id, vídeo y ms de solape, sin texto). Su arreglo no entra en esta rama.
>    - Sin la transcripción disponible (por ejemplo, en la CI sin data/), mide qué hace hoy verificar_citas en ese caso y haz exactamente lo mismo. Nunca puede pasar en silencio: si no puede comprobar, lo dice. Declara el comportamiento en el informe.
>    - Tests que la rompen a propósito: ventana vieja → falla; ventana que solo pisa la cola de un segmento que solapa un tramo, sin tocar el tramo (el caso de este ítem) → falla; ventana que toca el tramo a 0 ms → pasa; ítem supersedido que pisa un tramo → no cuenta; ventana nueva → pasa.
>
> 6. Recuadros en FILTRADAS-ESCENARIO-B.md (§4.1 y §4.3, con tu corrección sobre knowledge validate) y en SESION-03-EXTRACCION.md, cada uno con fecha y la referencia a este informe. HISTORIA, encargos, anexos cerrados y la tabla de CUARENTENA-POR-DEFECTO.md no se tocan.
>
> 7. Tu corrección sobre §4.3 entra en el informe como hallazgo, para la fila de ERRORES-RECURRENTES en el cierre: un informe afirmó lo que hacía una comprobación sin medirlo.
>
> Sigue con las fases 1 a 5 y amplía el contrato. CI de Linux: solo si tocas hooks, rutas o algo que dependa de la plataforma; si no, di por qué no hace falta. Después:
> - uv run botsito knowledge validate (exit 0, sin ERROR);
> - uv run python scripts/ficheros_con_ocultos.py;
> - make check sellado;
> - informe completo en VENTANA-EV-V9.md con el revisor al final.
>
> Rama lista para revisión, NO cerrada.

## Decisión del consultor sobre ev-v10-010438-0d4e6798 (2026-10-05)

Copiada tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Decisión sobre ev-v10-010438-0d4e6798 (2026-10-05, consultor). Cópiala al encargo y al informe. CAMBIA lo que dije en la decisión 5 («su arreglo no entra en esta rama»): entra aquí, porque sin él la comprobación no se activa y el procedimiento es el mismo que el de v9.
>
> 1. Opción (i): un ítem nuevo que supersede a ev-v10-010438-0d4e6798, con la cita y la ventana recortadas antes del segmento 1058.
>    Porqué no (ii): que el filtro tape todo segmento que toque un tramo más de 0 ms es el criterio de Q, y falla cerrado a propósito. Acotar la condición solo para que este ítem pase es aflojar una guardia por un caso.
>    Porqué no se pierde nada que haga falta: el trozo que sale («…y el cierre también sería 10») es justo lo que se le ha preguntado al trader por escrito antes de activar A-42 (punto E). Su respuesta lo sustituye.
>
> 2. Cómo, con el mismo anexo sustituir_item.py o uno hermano:
>    - La cita nueva es la vieja sin la parte que cae en el segmento 1058. El anexo la construye por programa con los límites de los segmentos (vía autorizada) y verificar_citas. No imprimas el texto: solo el id nuevo, el número de segmentos que cubre la cita (se espera 1053–1057) y el resultado de las comprobaciones.
>    - Ventana nueva: mismo inicio (3.878.000) y fin en el último segundo entero que no solape el segmento 1058 (se espera 3.894.000; mídelo).
>    - Dos pasadas, como en v9:
>      · con la cita y la ventana viejas, la comprobación nueva (ventana_no_citable) TIENE que rechazarlo;
>      · con las nuevas, verificar_citas da 0 problemas y 1 aparición, ventana_no_citable pasa y escribe el ítem.
>    - revisado_por igual que el viejo. notas: «cita recortada antes del segmento 1058, que el filtro tapa por el tramo 1:04:56–1:05:29; orden del consultor, 2026-10-05, VENTANA-EV-V9.md; la cita no se releyó».
>    - Lista en el informe los campos que difieren del viejo.
>
> 3. Referencias, cada una por su régimen:
>    - A-42 en ambiguedades.yaml pasa a citar el ítem nuevo, con Fuente:, y se regenera con uv run botsito spec docs --escribir;
>    - recuadro con fecha en SESION-04-EXTRACCION.md §3.1, que diga que la cita de 64:38–64:54 ya no incluye «…y el cierre también sería 10» y por qué, y que esa parte la cubre la pregunta del punto E;
>    - mide si algo más cita el id viejo y dímelo.
>
> 4. Medida, solo para el informe (no se arregla aquí): cuántos segmentos VISIBLES (no en cuarentena) tapa hoy el filtro solo porque un tramo, registrado con el inicio o el fin redondeado al segundo, les pisa un trozo. Por vídeo, con ids de segmento y ms, sin texto. Ya conocemos v9 1:07:45, v10 0:00:58 y este. Sirve para la fase 0 de la activación de E.
>
> 5. Después, lo que quedaba:
>    - activa ventana_no_citable en knowledge validate, evidence new y evidence propose --check, con los cinco tests de rotura más uno con este caso (una ventana que no toca el tramo, pero cuya cita cae en un segmento que sí lo toca → falla);
>    - vuelve a medir en todos los vídeos: 0 ítems activos;
>    - anexo del control de la fase 5 (21 de 21 bloques y 0 ítems activos, más cuántos supersedidos deja fuera: se esperan 2);
>    - uv run botsito knowledge validate, uv run python scripts/ficheros_con_ocultos.py y make check sellado;
>    - revisor, con su informe al final de VENTANA-EV-V9.md.
>
> 6. PROJECT_STATE va en 24.014 bytes, cerca del tope de 25.000. En esta rama no crece más. Si la línea de deuda de los supersedidos lo empuja, condénsala a una línea que apunte al informe.
>
> Rama lista para revisión, NO cerrada.
