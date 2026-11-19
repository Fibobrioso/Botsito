# Encargo · trabajo/laminas-sesion-7b

Dado por Aleks (consultor) el 2026-11-18, en un solo mensaje. Copiado tal cual. El ADR que el
encargo nombra para el arreglo de F2, ADR-0095, va declarado en el bloque `ids-inexistentes`, como
exige `knowledge validate`; sale del bloque en el commit que lo crea o, si al final no existe, en el
último commit de la rama.

```ids-inexistentes
ADR-0095 — el encargo lo nombra para el arreglo de F2 si (a) pasa; aún no existe
```

> Modelo: Opus · Esfuerzo: alto
>
> Encargo del consultor (2026-11-18) · trabajo/laminas-sesion-7b · tramo R4 (R4.3; el punto (1) de la F de la Next Action)
>
> Rama nueva: trabajo/laminas-sesion-7b, desde main (b174d714, commit de estado sobre el merge cf33a916 del tag stable/F39e-activar-sesion-07). Ábrela con la skill abrir-rama: base comprobada con git y la CI de main sobre b174d714 (run 44446460628) comprobada con un gh run view suelto. Contrato con tramo R4, riesgo alto si entra el arreglo de F2 en src/botsito/engine/ y medio si no (se fija al abrir como alto y se dice) y artefacto docs/validation/LAMINAS-7B.md. Es lista blanca: en rutas_permitidas van ese informe y docs/validation/anexos/LAMINAS-7B/, docs/sesion-7/PREGUNTAS-7B.md, scripts/transcribir_sesion.py y su test, .claude/skills/activar-sesion/SKILL.md (una línea), docs/validation/HOLDOUT-EXPOSICIONES.md, docs/validation/LAMINAS.md, docs/validation/LAMINAS-MOTIVOS.md y docs/runbooks/LAMINAS.md (solo recuadros o notas, si F2 cambia una frase), src/botsito/engine/ y tests/ (solo si hace falta el arreglo de F2), docs/adr/0095-*.md y docs/adr/README.md, docs/encargos/, PROJECT_STATE.md, docs/state/HISTORIA.md y docs/runbooks/ERRORES-RECURRENTES.md. Tag previsto: stable/F39f-laminas-sesion-7b (comprueba que no existe). Al copiar este encargo a docs/encargos/, declara ADR-0095 en el bloque ids-inexistentes; si al final no existe, sale del bloque en el último commit. Es una rama de laptop: necesita data/. Mandan las skills abrir-rama, fase-cero y entregar-rama, y docs/runbooks/LAMINAS.md; si este encargo y ellas chocan, ganan ellas y lo dices.
>
> LA PARADA ES CONDICIONAL. Puede que Aleks no esté delante. Cada paso cuya medida cuadre con mi decisión se hace; el que no, se deja en la PARADA final con la alternativa que ves y la rama sigue con lo demás. Nunca cierras y nunca eliges «no volver a preguntar». Si te frena algo de holdout o de guardia, te quedas ahí.
>
> OBJETIVO
> Dejar la 7b lista para grabar: el bloque de días con sesiones que el motor de F39e pueda enseñar sin depender de cuántas velas haya cargadas, PREGUNTAS-7B.md revisado con lo que dejó la 7a, sus láminas generadas y revisables, y SESION_EN_CURSO en "08".
>
> QUÉ NO CAMBIA
> - Ninguna regla del motor ni ningún valor de knowledge/spec/. El único código que puede cambiar es el del punto F2, y solo como registro.
> - Corridas autorizadas, y ninguna más: las de motor laminas (cada llamada corre dos por dentro) y, solo si hay arreglo en F2, la corrida de julio de D0 antes y después. Nada de lo que salga se commitea como línea base.
> - Ningún fichero del repo describe lo que dice una lámina, cuántas tiene una sesión ni qué carpeta es qué sesión. La clave solo en clave.txt, fuera del repo, y en el terminal.
> - Ninguna fecha de un día reservado en nada commiteado; los días del bloque son todos de construcción y se comprueban con casos_reservados antes de escribirlos.
> - Nada se lee de knowledge/evidence/ más allá de los ítems que ya cita PREGUNTAS-7B.md o ACTIVAR-SESION-07.md.
>
> F0 · FASE 0 (sin tocar nada)
> 0.1 Lo que el encargo hereda: «Para la rama siguiente» de ACTIVAR-SESION-07.md, el recuadro D4 de PREGUNTAS-7B.md, «Lo que no me convence» de LAMINAS-MOTIVOS.md (puntos 1 y 2) y la F de la Next Action.
> 0.2 Para cada sesión del bloque que queda en F1 (las cuatro y las tres reservas): H4 cargadas al abrir la sesión, medidas con un guion commiteado en anexos/LAMINAS-7B/ (parte de anexos/ACTIVAR-SESION-07/arranque.py), y la compuerta de ADR-0093 §3 pasada HOY con una copia de anexos/PREPARACION-SESION-7/dias_d3.py que lleve esas candidatas, con su fila de HOLDOUT-EXPOSICIONES del día. Solo esos dos datos por sesión; ningún resultado.
> 0.3 Las filas de cada pregunta candidata del punto F3, contadas sobre fuentes commiteadas (anexos de RECORRIDA-CONSTRUCCION-2, de PREPARACION-SESION-7 y de ACTIVAR-SESION-07). Donde no haya fuente commiteada, se dice «sin recuento por fila», como hoy.
>
> MIS DECISIONES (2026-11-18)
>
> F1 · El bloque de días
> 1. Sale toda sesión que abra con menos de 60 H4 cargadas: hoy, 2026-01-13 de 07 a 11 (sesión 1) y 2026-01-07 de 07 a 11 (sesión 3). Su sesgo sale del rango que arranca en la primera H4 de enero, no de lo que vería el trader, y le haríamos corregir un efecto de nuestros datos.
> 2. Entran en su lugar 2026-04-24 de 07 a 11 (sesión 1) y 2026-04-27 de 11 a 15 (sesión 3). Salen de anexos/PREPARACION-SESION-7/sustitutas.txt: son las dos únicas de la lista «stop fuera» marcadas «cumple» que no están ya en el bloque, no se usaron en la 7a y caen fuera de las sesiones de enero de F1.3; sirven a la pregunta del 0 de la caja, como las que salen. No se eligieron mirando lo que hace el bot ni el trader en ellas. Las reservas no cambian: 2026-01-21 de 07 a 11, 2026-01-22 de 11 a 15 y 2026-07-16 de 07 a 11. En la tabla de §1, la columna «Sirve a» y la de filas se rellenan con lo que digan sustitutas.txt y filas-por-sesion.txt.
> 3. 2026-04-15 de 11 a 15 se queda como sesión 2: es el único caso de «el trader no opera y el bot sí», y en la 7a el trader no vio ninguna lámina de ese día. Pero ya lo marcó y lo operó entonces, por error (el tramo sigue no citable): §1 lo dice, y para ese día el paso de abrir una sesión de replay nueva y sin marcas va subrayado. Al pie de §1, la frase «el bloque de días es la primera vez que se le oye operarlas» se corrige.
> 3b. Una sesión para la que motor laminas no dé ninguna lámina (F2) no sirve al bloque: sale y entra la primera reserva que sí tenga, y se regenera. Vale también para el 2026-04-15. Si con eso no quedan cuatro sesiones con láminas, PARADA.
> 4. 2026-07-03 de 07 a 11 está gastado y no se usa.
> 5. Los pasos de §1, por cada sesión, ganan lo que aprendimos en la 7a (ERRORES-RECURRENTES.md, filas de trabajo/sesion-07 y trabajo/activar-sesion-07): Aleks comprueba el día ANTES de grabar; el trader borra cualquier marca anterior; dice la fecha en voz alta al abrir cada gráfico y otra vez después de abrir cada replay; opera la sesión entera ANTES de ver ninguna lámina; y en CADA corrección Aleks pregunta «¿siempre, solo en este caso, o de qué depende?». En el bloque técnico solo se usan los esquemas; si el trader quiere poner un ejemplo en su gráfico, tiene que ser un día de construcción y decir la fecha en voz alta al abrirlo.
> CUADRA si las siete sesiones (cuatro y tres reservas) pasan hoy la compuerta de ADR-0093 §3 y tienen 60 o más H4. Si alguna no, sale por la siguiente reserva y se dice; si no quedan cuatro, PARADA.
>
> F2 · Las láminas, y b1 y el LaminaError de F38y
> 1. Con el bloque de F1 cerrado y commiteado: la fila de HOLDOUT del día, y uv run botsito motor laminas con las siete sesiones en un orden barajado que no se escribe en el repo, --salida C:\Users\USER\Desktop\laminas-sesion-7b-v1 (LAMINAS.md: sola, nunca junto a un make check). clave.txt la guarda Aleks.
> 2. Mide, solo con recuentos y en el informe: (a) si alguna sesión da LaminaError porque RN-004 abre escenario en el mismo cierre en que RN-016 o RN-001 dispararon por los intentos; (b) b1: en cuántos cortes detenido_por_tope está encendido por una regla y la otra causa de tope también se cumple.
> 3. Si (a) pasa, se arregla aquí: la foto guarda los hechos del principio del evento SOLO COMO REGISTRO (nada lo lee para decidir), con un test que rompe en main y la prueba de que el motor no cambia: la corrida de julio de D0 (recuadro de ADR-0093 §4) antes y después, con las salidas de pivote_julio.py y delta_julio.py idénticas (cero filas que cambian). Como toca el motor, ADR-0095, aunque sea corto. Si (b) pasa, la lámina dice las dos causas, con su test; sin ADR. Después se regeneran las láminas en laminas-sesion-7b-v2 y se borra v1. Si no pasa ninguno, no se toca nada y cada uno queda como una línea de Technical Debt propuesta para el cierre.
> 4. En el terminal, no en el repo: por sesión, cuántas láminas y de qué tipo, para que Aleks y yo las revisemos.
>
> F3 · PREGUNTAS-7B.md revisado
> Recuadro fechado arriba, como el de PREGUNTAS-7A.md, que diga qué cambió y por qué. Las seis técnicas, ordenadas como manda ADR-0093 §1: primero las que tocan el dinero y después por las filas que mueven.
> - S-1, NUEVA, la mecha que vuelve en M15 (A-35, pregunta 1 de la 7a), con la reformulada de ACTIVAR-SESION-07.md. Toca el dinero.
> - S-2, NUEVA, las zonas de control y el break even (RN-009 y A-13), con dos preguntas, como la de A-43 de hoy: la 1, la reformulada de las zonas de control, con la duda de SESION-07-EXTRACCION.md §5.1, punto 4; la 2, la del margen del break even, también reformulada en ACTIVAR-SESION-07.md. Toca el dinero por A-13.
> - S-3, NUEVA, el rango de H4 (A-58), con la reformulada de ACTIVAR-SESION-07.md; en «Para precisar», además: «¿Marcas tu rango siempre en el gráfico de 4 horas, o a veces en otro?».
> - S-4, el 0 de la caja (A-48): la S-1 de hoy, como está.
> - S-5, el punto del breaker (S-22): la S-2 de hoy, como está.
> - S-6, el precio más allá del 0 (S-19): la S-3 de hoy, como está.
> - S-7, la de material: como está, al final.
> Con la tabla de 0.3, ordena S-3 a S-6 de más a menos filas (las que no tienen recuento por fila, detrás) y dilo; S-1 y S-2 no se mueven. Desviación que declaro: S-22 y S-19 siguen entre las seis sin recuento por fila, porque su rama es el punto (2) de la Next Action y sin su respuesta no se puede abrir.
> Cada pregunta nueva, con las partes de las demás («Lo que nos has dicho» solo con ítems citables que ya citan SESION-07-EXTRACCION.md o ACTIVAR-SESION-07.md, «Lo que todavía no sabemos», la pregunta cerrada con «otra, ¿cuál?», «Para precisar», «Para confirmar al final») y su línea «Para Aleks» con el destino de cada respuesta (parámetro, opción y régimen). El esquema de cada una, descrito como los de hoy (lo dibujo yo en el PDF).
> Pasan a §3, en su tabla y sin título «**S-n.**» a principio de línea (el test de la hoja 08 lee esos títulos): la reentrada (hoy S-4); A-53 (hoy S-5), que gana la cita ev-v18-011801-8b4f738d; A-43 (hoy S-6), que gana las dos citas de v19 que nombra ACTIVAR-SESION-07.md; el punto de breaker por la mecha más larga de la segunda vela del mismo color (ev-v18-013614-cfd2b45d, ev-v19-011138-5c622b1f); y la de 2026-07-01 de 11 a 15, con la reformulada de ACTIVAR-SESION-07.md. Si la tabla de 0.3 da a alguna de §3 más filas que a S-5 o S-6, ponlo en la PARADA final, sin cambiarlas.
> Después: CODIGOS_DE_SESION_TEXTO["08"] de scripts/transcribir_sesion.py con los títulos de las siete que queden, SESION_EN_CURSO = "08" y el comentario de encima al día. test_la_sesion_en_curso_es_la_07 se sustituye A PROPÓSITO por el de la 08, como se hizo con el de la 06, y test_la_hoja_08_es_la_de_preguntas_7b tiene que seguir pasando.
>
> F4 · Lo pequeño
> - .claude/skills/activar-sesion/SKILL.md: la línea preparada en ACTIVAR-SESION-07.md («Para la orden de cierre», la línea para la skill), en su sitio (la sección «El metodo de ADR-0093 §4», donde hoy dice que cómo se corre julio no está escrito). Si la guardia niega la edición, PARADA de ese punto solo.
>
> INFORME, REVISOR Y ENTREGA
> docs/validation/LAMINAS-7B.md con lo que piden las skills, más: la tabla de 0.2; el bloque final con el porqué de cada cambio; los recuentos de F2; la tabla de filas de 0.3; y, preparado para la orden de cierre sin aplicarlo: la F nueva (el punto (1) hecho; lo siguiente, (2) grabar, ingerir y activar la 7b), la línea de Estado de R4.3 y su «Qué es» puesto al día (hoy dice que las láminas las genera la activación de la 7a y trae el reparto viejo de la 7b). PROJECT_STATE.md por debajo de 25.000 bytes (hoy 24.109): di su tamaño.
> Revisor, con estos alcances además de los suyos: (1) que ningún fichero del repo describa una lámina ni deje deducir la clave; (2) que los días del bloque cumplan ADR-0093 §3 y tengan 60 o más H4; (3) que las preguntas nuevas no sugieran la respuesta y no citen nada no citable; (4) si hubo arreglo en F2, que nada lo lea para decidir y que julio no cambie.
> Push a fix/laminas-sesion-7b y CI de Linux (el único fallo aceptado es el de state check por el nombre fix/); dame el número del run. Después, la PARADA final: lo que no cuadró, la tabla de filas de F3 y lo que no te convence.
>
> Rama lista para revisión, NO cerrada.
