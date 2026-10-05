# Encargo · trabajo/cuarentena-por-condicion

Dado por Aleks (consultor) el 2026-10-04. Copiado tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Rama nueva trabajo/cuarentena-por-condicion, desde main. Antes de abrirla, dime el sha de main y el tag al que apunta (espero e98815a sobre stable/F36v-sesion-04). Si no coincide, para y dímelo. Ábrela con la skill abrir-rama: encargo en docs/encargos/, contrato.yaml y archivo de PROJECT_STATE en HISTORIA.
>
> OBJETIVO (una frase)
> El filtro de cuarentena de las transcripciones deja de ser una lista fija de meses (MESES_FILTRADOS en src/botsito/corpus/cuarentena.py) y pasa a tapar todo mes que no se pueda demostrar libre. Viene de docs/validation/SESION-04-EXTRACCION.md §2.4 y §6, pendiente a), y es el punto P de la Next Action.
>
> QUÉ NO CAMBIA
> Ni el motor, ni la spec, ni knowledge/feedback, ni las ambigüedades. No se activa nada de la sesión 4 en esta rama. Las transcripciones, los fotogramas y la evidencia son inmutables: no se editan.
>
> LA CONDICIÓN (decisión del consultor, 2026-10-04)
> Un mes se filtra salvo que se cumplan las tres cosas siguientes:
> (a) no tiene ningún día en casos_ocultos ni en casos_reservados, en ningún año;
> (b) no está reservado entero aunque no tenga casos, como un mes que no se ha descargado;
> (c) se ha podido comprobar (a) y (b). Si no se ha podido, se filtra.
> Un mes sin datos, por ejemplo uno futuro, cuenta como libre solo si (a) y (b) se comprueban. Las grafías del ASR y las abreviaturas que hoy cubre MESES_FILTRADOS se mantienen para todo mes filtrado, y se generan para cada mes por su nombre en español, en inglés y por su abreviatura.
>
> FASE 0: inventario sin tocar nada. Entrégamelo antes de escribir código.
> 1. ¿De dónde sale hoy la lista de meses reservados enteros (b)? ¿Hay una fuente única en el repo (CLAUDE.md, config, holdout) o habría que crearla? Cita el fichero y la línea.
> 2. ¿Quién construye hoy el filtro y cómo le llegan los días de casos_ocultos? cuarentena.py, ¿es puro o lee el repo? Propón por dónde entra la condición sin que domain/ ni el filtro lean el repo por su cuenta.
> 3. Todos los sitios que usan MESES_FILTRADOS, _RE_MES o _RE_ABREV: scripts/transcribir_sesion.py, verificación de citas, tests y docs.
> 4. Mide con la regla nueva, sin aplicarla, sobre las transcripciones activas de v1 a v10. Por cada vídeo, imprime SOLO recuentos y marcas de tiempo, nunca texto ni qué mes: segmentos que pasarían a ocultos y que hoy no lo están, y cuántos ítems ev-* caerían dentro. Si hay ítems afectados, dime cuántos y de qué vídeo, y propón cómo se retiran respetando el régimen de evidencia (sustitución, no edición). Eso lo decido yo antes de la fase 1.
>
> FASE 1: la condición, con estos criterios comprobables
> - MESES_FILTRADOS deja de ser la fuente de verdad. Si se conserva una tabla de grafías, es un diccionario de grafías por mes, no una lista de meses vigilados.
> - Si el filtro se construye sin los datos que necesita para comprobar (a) y (b), filtra todos los meses. No vale un valor por defecto que deje meses a la vista.
> - Sigue funcionando el «marco» que no se filtra (el verbo del trader) y siguen los límites de palabra («mayor», «siempre»).
>
> FASE 2: aplicación
> - Las transcripciones filtradas y los tramos no citables se regeneran con la regla nueva por la vía que exija su régimen: tramo o manifiesto nuevo, nunca editar. El tramo manual de v10 1:55:29–1:55:32 se queda como está.
> - Lo que decida sobre los ítems ev-* afectados de la fase 0.
> - Si al medir hay alguna exposición nueva, se declara hoy mismo en docs/validation/HOLDOUT-EXPOSICIONES.md, sin texto ni fechas reservadas.
>
> TESTS QUE ROMPEN LA GUARDIA A PROPÓSITO
> 1. Un caso oculto inventado en un mes que hoy no se filtra: ese mes pasa a filtrarse sin tocar ninguna lista. Hazlo en un repo temporal, no en el real.
> 2. Un filtro construido sin datos de casos filtra todos los meses.
> 3. Un mes reservado entero sin casos se filtra.
> 4. Un mes libre de verdad (sin casos ocultos ni reservados y no reservado entero) no se filtra. Esto demuestra que la guardia puede dejar pasar algo.
> 5. Ningún mes con días en casos_ocultos o casos_reservados queda sin cubrir, medido contra el repo real. Solo recuento: «0 sin cubrir».
> 6. Los tests de grafías que ya existían siguen pasando.
>
> CI
> Como toca una guardia del holdout, empújala como fix/cuarentena-por-condicion y pasa la CI de Linux antes del merge. El único fallo aceptado es el de state check por el nombre fix/. Dame los números de run.
>
> INFORME
> docs/validation/CUARENTENA-POR-CONDICION.md, con:
> - la fase 0;
> - la condición tal cual quedó;
> - recuentos antes y después por vídeo (sin texto);
> - los ítems afectados y qué se hizo con ellos;
> - desviaciones declaradas;
> - tamaño de PROJECT_STATE.
> En PROJECT_STATE, el punto P pasa a «en revisión en trabajo/cuarentena-por-condicion». No lo muevas a HISTORIA: eso va en el cierre.
>
> REVISOR
> Al terminar, un revisor independiente con su informe pegado al final. Que mire en concreto si queda alguna lista de meses escrita a mano en algún sitio que decida qué se tapa.
>
> Rama lista para revisión, NO cerrada.
