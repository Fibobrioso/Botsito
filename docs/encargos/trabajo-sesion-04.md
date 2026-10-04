# Encargo · trabajo/sesion-04

Dado por Aleks (consultor) el 2026-10-04. Copiado tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Rama nueva: trabajo/sesion-04, desde main en 48f9701 (tag stable/F36u-historial-sin-git). Ábrela con la skill abrir-rama: encargo en docs/encargos/, contrato.yaml y archivo en HISTORIA. Copia este prompt tal cual al encargo, con fecha 2026-10-04.
>
> OBJETIVO
> Ingerir la sesión 4 con el trader y entregar el informe de extracción por pregunta, siguiendo la skill ingerir-sesion de principio a fin. Esta rama NO resuelve nada: no hay feedback apply, ni ambigüedades cerradas, ni cambios en la spec o en el motor. El destino de cada respuesta lo decido yo después, en otra rama.
>
> ENTRADAS
> - Vídeo: corpus/Estrategia del trader/Grabación de pantalla 2026-10-04 105617.mp4. Va como v10, con drive_id null y fecha_grabacion "2026-10-04", y entra en SESIONES_EN_CUARENTENA.
> - Sesión: 2026-10-04-sesion-04.
> - Antes de nada, comprueba que el día no esté reservado con la línea de SESION-DE-PREGUNTAS.md («Antes», paso 1) y la fecha 2026-10-04. Tiene que imprimir False; si imprime True, para y avísame.
> - Antes de transcribir, pregúntale a Aleks en el terminal si en la sesión el trader habló de operaciones concretas de septiembre o de marzo, o si dio cifras en la pregunta de las capturas de marzo, y en qué minuto aproximado. Esos tramos se declaran como no citables y en HOLDOUT-EXPOSICIONES.md el mismo día, sin leerlos.
>
> LA HOJA QUE SE LLEVÓ (las decisiones del consultor de los días 2026-10-03 y 2026-10-04, copiadas aquí para que queden en el repo)
> 1. Los códigos de voz fueron S-1 a S-24 («pregunta ese siete» … «fin de pregunta»). S-n es el número de la pregunta en docs/sesion-4/PREGUNTAS.md, más dos nuevas: S-23 (A-32, el nivel que, roto con mecha, anula la entrada) y S-24 (A-13, confirmar el break even tapado por el corte de audio de v9).
> 2. Orden de la sesión: S-1, S-2, S-3, S-4, S-5, S-6, S-22, S-7, S-8, S-9, S-10, S-11, S-12, S-13, S-14, S-15, S-16, S-17, S-18, S-20, S-21, S-23, S-24, S-19.
> 3. Subpreguntas añadidas a las de PREGUNTAS.md:
>    - S-1: si la caja se traza con la vela del bloque cerrada o en formación (A-49);
>    - S-3: si el objetivo de 3 a 1 se mide sobre la distancia 0→1 o 0→0,8 (A-18);
>    - S-5: qué hace con la orden si a las 11:00 cambia el sesgo de H4 (A-39);
>    - S-18: qué pasa con la marca del alto viejo (A-25).
> 4. Se enseñaron 4 esquemas INVENTADOS (S-2, S-4, S-11 y S-13), rotulados «Esquema inventado, no es un día real», que muestran la situación sin las opciones. Esto enmienda, por decisión del consultor, el «sin gráficos» del encargo del barrido. No hubo ningún gráfico de un día real.
> 5. En scripts/transcribir_sesion.py, da de alta la hoja de la sesión 4: ORDEN_SESION_04 con S-1..S-24 y sus títulos. OJO: S-1 ya existía en la sesión 3 con otro texto («cómo decide el sesgo del día»). Antes de tocar nada, mide cómo usan los códigos codigos_validos y CODIGOS_DE_SESION_TEXTO, y hazlo sin romper la transcripción de la sesión 3 (textos por sesión, no un diccionario que se pisa). Test que lo compruebe, roto a propósito.
> 6. Escribe todo esto, la tabla código → título → número de PREGUNTAS.md → ambigüedad, en docs/sesion-4/HOJA-USADA.md. Sin citas del trader, que la hoja de papel no va al repo.
>
> EXTRACCIÓN
> Informe en docs/validation/SESION-04-EXTRACCION.md, con el paso 6 de la skill:
> - por cada código S-n: el tramo (mm:ss), el literal de la FILTRADA, y si resuelve / resuelve en parte / no resuelve;
> - en cada respuesta, si el trader dio la regla general o solo un ejemplo, si dijo «creo», y si cubre compra y venta;
> - S-7 (el reloj de invierno, A-42) va la primera del informe, porque el cambio de hora es el 25 de octubre.
> La cruda no la lee nadie. Los fotogramas, solo por instante localizado, como manda la skill.
>
> CIERRE DE LA RAMA
> make check sellado; push a fix/sesion-04 (git push origin trabajo/sesion-04:refs/heads/fix/sesion-04) y CI de Linux con solo el fallo esperado de state check; dame el número de run. Después el revisor, lanzado con el informe YA TERMINADO, y su informe pegado al final.
>
> Rama lista para revisión, NO cerrada.
