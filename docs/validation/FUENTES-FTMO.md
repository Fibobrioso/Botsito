# FUNCTIONALITY VALIDATION REPORT · Fuentes escritas de FTMO

Rama `trabajo/fuentes-ftmo`, abierta el 2026-10-03 desde `main` `7dcbb6a` (tag
`stable/F36q-cierres-de-mercado`, que apunta al merge `aaac17b`). Encargo, copiado tal cual:
`docs/encargos/trabajo-fuentes-ftmo.md`. Solo documentación y knowledge: no cambia motor ni cifras.
Riesgo bajo en el contrato.

## 1. La respuesta literal del ticket VDW-DPMWR-965 (P0 de CIERRES-DE-MERCADO.md)

**Dónde va, y por qué ahí.** El repositorio no tiene una carpeta de fuentes de FTMO. Su patrón es el
de `docs/validation/FTMO-REGLAS.md`: cada regla con su cita LITERAL dentro del propio documento y la
fuente al lado (la URL de la página oficial y el día de lectura). Las copias descargadas no se
versionan. El correo no tiene URL, así que su fuente es el remitente y la hora:
`support@ftmo.com`, el 2026-09-29 a las 14:00:47 UTC, en respuesta al correo de Aleks del
2026-09-28.

`FTMO-REGLAS.md` es un informe CERRADO en `main`. Por la regla de `CLAUDE.md` («Regímenes de
cambio», `docs/validation/`), lo nuevo entra como un RECUADRO junto al pasaje que corrige, y el
cuerpo no se toca. Va justo después del recuadro del traslado del 29-09-2026, al final de §2. Lleva:
- la cabecera de la fuente;
- el texto tal cual, con sus negritas y sin la firma ni las imágenes (lo copia Aleks en el encargo);
- el contraste con el traslado;
- lo que no se contestó;
- lo que se repreguntó el 2026-10-03.

**Contra el traslado del 29-09-2026: coincide.** Swing permite noticias, noche y fin de semana. No
se permite el gap trading, en sus dos mitades: noticias programadas y «within two hours before a
relevant market closes for at least two hours». En MT5 la comisión se cobra 50 % al abrir y 50 % al
cerrar, sin importe. Nada de lo que el repositorio dio por bueno con el traslado cambia.

**Las citas que apuntaban al traslado** ahora apuntan a la fuente literal:

| Dónde | Qué decía | Cómo queda |
|---|---|---|
| `FTMO-REGLAS.md`, recuadro del ticket | «no hay cita literal en el repositorio» | el cuerpo, intacto; el recuadro nuevo de debajo lo corrige y trae el texto |
| `CIERRES-DE-MERCADO.md` §0.1 | «NO está literal en el repositorio … lo que Aleks trasladó» | recuadro de CORRECCIÓN encima: P0 hecho, y dónde está |
| `CIERRES-DE-MERCADO.md` §0.6, P0 | «guardar en el repositorio el texto literal» | recuadro de CORRECCIÓN debajo: P0 hecho; P1-P3 enviadas el 2026-10-03 |
| ADR-0068, «Problema que resuelve» | «(traslado de Aleks del 29-09-2026)» | la frase literal de FTMO y el puntero al recuadro |

No se tocan las copias de `docs/state/HISTORIA.md`, que solo se amplía, ni el informe del revisor
pegado en `CIERRES-DE-MERCADO.md` §5: es una cita de su tiempo. `git diff` de los dos informes
cerrados: solo líneas añadidas.

## 2. Lo que no se contestó y lo que se repreguntó

- **El tamaño de posición, sin respuesta.** El correo de Aleks del 2026-09-28 preguntaba tres
  cosas: noticias y gap trading, tamaño de posición y comisión. La segunda no se contestó: si un lote
  que varía con el stop, con riesgo constante, cuenta como «substantially larger position sizes»
  (R17, `FTMO-REGLAS.md` §4).
- **Repreguntado el 2026-10-03, en el mismo ticket**: diez preguntas numeradas del 1 al 10. La 1 a
  la 4 son los mensajes al servidor (A-54), la 5 a la 9 el gap trading (A-55) y la 10 el tamaño de
  posición (R17). Respuesta pendiente. El correo, literal, en `FTMO-REGLAS.md` (§8).

> **CORRECCIÓN (2026-10-03, segunda orden del consultor, §8).** Lo que este párrafo decía de abajo
> ya no vale: el correo está en el repositorio y el recuento cuadra. Son diez preguntas numeradas,
> y «P1-P4» fue un error del encargo. Se deja como estaba para que se vea qué se detectó.

**Lo que no estaba en el repositorio, y no se supuso** (antes de la segunda orden):
- **el texto del correo del 2026-10-03.** Las P1-P3 de gap trading sí están (en `CIERRES-DE-MERCADO.md`
  §0.6). Las P1-P4 de los mensajes al servidor no están en ningún documento: ni
  `FRENO-PETICIONES.md` ni A-54 las numeran;
- **el recuento.** Los grupos que nombra el encargo suman 4 + 3 + 1 = 8 si la del tamaño de posición
  es una, y el encargo dice diez. Puede que alguna se partiera (la P1 de gap trading tiene cuatro
  apartados), pero eso no consta. **Para Aleks:** guardar el texto de ese correo como se guardó la
  respuesta, para que cada pregunta tenga su texto cuando llegue la contestación.

## 3. Technical Debt

- **Sale a HISTORIA** la línea «PENDIENTE DE FTMO: EL BOT PUEDE ABRIR DENTRO DE LAS DOS HORAS
  PREVIAS…», con su texto literal, bajo `# Technical Debt PAGADA`. Lo que decía ya no es verdad: desde
  `stable/F36q-cierres-de-mercado` el broker no abre ni coloca en esa ventana (ADR-0068). Lo que
  quedaba abierto ya lo cubren otros dos sitios:
  - A-55, con las preguntas enviadas y la respuesta pendiente (§4);
  - la entrada N de Next Action, con la renovación del calendario.
  De las dos salidas que daba el encargo, esta deja una sola fuente para cada cosa.
- **Entra** una línea sobre el tamaño de posición, porque ninguna lo cubría: la de 2026-09-25 en
  «Decisions and Rationale» habla de la guardia sin cifra del simulador, no de la pregunta a FTMO.
  Dice qué se pregunta (R17), que el ticket no lo contestó y que se repreguntó el 2026-10-03.

## 4. A-54 y A-55

Las dos dicen ahora que sus preguntas a soporte se enviaron el 2026-10-03, en el ticket
VDW-DPMWR-965, con la respuesta pendiente y un puntero a este informe:
- A-54 decía «pendiente de la respuesta del soporte de FTMO, que pide Aleks»;
- A-55 decía «Se pregunta a soporte de FTMO».

Solo cambia el campo `pregunta`; el título, la clase, el estado y los parámetros no se tocan, así
que la tabla de `PROJECT_STATE.md` sigue igual. `botsito spec docs --escribir` regenera
`docs/spec/ambiguedades.md` en el mismo commit.

## 5. Comprobaciones

Antes del sello, sobre el árbol estadiado:
- `uv run botsito state check`: OK;
- `uv run botsito spec check`: OK, hash del manifiesto al día (`ambiguedades.yaml` no entra en él);
- `uv run botsito knowledge validate`: exit 0, todo id citado existe;
- `uv run python scripts/contrato_rama.py`: todo dentro del contrato;
- ningún fichero estadiado con CR;
- `PROJECT_STATE.md`: 22.913 bytes.

`make check` sobre `0e69da5` (arbol `53caf0d`), leído en `make-check.log`:
- `All checks passed!`;
- `1860 passed in 683.27s`;
- `SELLO: make check en verde sobre el arbol 53caf0d846f2c5331f467ade2f9608cc889ac14f`;
- `PICO DE MEMORIA de make check: 287 MiB en test`.

El commit del revisor lleva su propio sello.

## 6. Lo que encontró el revisor, y qué se hizo

Su informe, entero, en §7. Ningún hallazgo bloqueaba.

| # | Gravedad | Qué se hizo |
|---|---|---|
| a1 | importa | **Corregido.** §5 remitía a un «§6» que no existía. Ahora trae el sello, el recuento y el pico, leídos de `make-check.log` |
| a2 | menor | **Comprobado.** La línea del 2026-09-25 en «Decisions and Rationale» de `PROJECT_STATE.md` dice «la guardia de tamano de posicion sin cifra NO impide correr, porque es solo aviso». Habla del aviso del simulador (ADR-0050), no de la pregunta a FTMO. La línea nueva de Technical Debt no la duplica |
| a3 | menor | **Dicho.** `PROJECT_STATE.md` queda en 22.913 bytes, con 87 de margen hasta 23.000. La rama siguiente tendrá que sacar algo, o subir el tope si el consultor lo decide |
| b1 | menor | **Corregido:** el estado, abajo |

**Para Aleks** (§2): guardar el texto del correo del 2026-10-03 con las preguntas reenviadas, y
aclarar el recuento (el encargo dice diez; los grupos que nombra suman ocho si el tamaño de posición
es una pregunta).

## 7. Informe del revisor

Pegado tal cual, sobre `0e69da5`; lo que se hizo con cada hallazgo, en §6.

> ## Informe del revisor · trabajo/fuentes-ftmo · 2026-10-03
>
> ### Eje (a) · Reglas de la casa
> Resumen: 0 bloquea, 1 importa, 2 menor.
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | a1 | importa | El informe de la rama remite a un «§6» que no existe. Dice que el resultado de `make check` está «en el mensaje del commit y en §6». El informe acaba en §5 y «Estado», y el mensaje de 0e69da5 no menciona `make check`. El sello y el pico de memoria no constan en el informe. Aquí se comprobaron en `make-check.log` (ver abajo). Hay que pegar la línea `SELLO` y el pico en el informe, o quitar la frase. | `docs/validation/FUENTES-FTMO.md`, §5, última línea: «su resultado, en el mensaje del commit y en §6». `grep '^## ' docs/validation/FUENTES-FTMO.md` da §1 a §5 y Estado. |
> | a2 | menor | El informe cita «decisión de qué hacer» con la salida del encargo: el encargo daba dos salidas, reescribir o mover. El informe declara que eligió mover y por qué («deja una sola fuente para cada cosa»). Está bien declarado. Sin embargo, la afirmación «la de 2026-09-25 en "Decisions and Rationale" habla de la guardia sin cifra del simulador» no la verifiqué línea a línea. | `docs/validation/FUENTES-FTMO.md` §3 |
> | a3 | menor | `PROJECT_STATE.md` queda en 22.913 bytes, por debajo del tope de 23.000 pero con 87 bytes de margen. La siguiente rama lo pasará. No es defecto de esta rama. | `wc -c PROJECT_STATE.md` da 22913 |
>
> Comprobado sin hallazgos:
> - **Contrato.** `uv run python scripts/contrato_rama.py` dio: `CONTRATO: 10 ficheros dentro del contrato de trabajo/fuentes-ftmo (riesgo bajo, artefacto docs/validation/FUENTES-FTMO.md, 4 comprobaciones para el revisor)`. Los 10 ficheros del diff están en `rutas_permitidas`. Ninguno cae en `rutas_protegidas` (`git diff --name-status main...HEAD`: solo `PROJECT_STATE.md`, `contrato.yaml`, ADR-0068, `docs/encargos`, `docs/spec`, `HISTORIA`, los dos informes, el informe nuevo y `ambiguedades.yaml`).
> - **Comprobaciones del contrato.**
>   - `uv run botsito state check`: `OK: rama 'trabajo/fuentes-ftmo' - funcionalidad actual: trabajo/fuentes-ftmo · EN CURSO (2026-10-03) ...`
>   - `uv run botsito spec check`: `OK: 35 reglas de spec (30 vigentes, 30 con forma ejecutable), 11 terminos de glosario, hash del manifiesto al dia`.
>   - `knowledge validate > knowledge-validate.log` escribe: no lo ejecuté. `knowledge-validate.log` no existe en el árbol. La evidencia sustitutiva es el informe (§5: «exit 0, todo id citado existe»), que no pude verificar. Los ids del trailer sí existen (ver abajo).
> - **`make check` y sello.** `make-check.log`:
>   - `SELLO: make check en verde sobre el arbol 53caf0d846f2c5331f467ade2f9608cc889ac14f`.
>   - `1860 passed in 683.27s`.
>   - `PICO DE MEMORIA de make check: 287 MiB en test`.
>   - `git rev-parse HEAD^{tree}` da `53caf0d846f2c5331f467ade2f9608cc889ac14f`, igual que el sello. `git status --short` está limpio.
> - **Trailer `Fuente:`.** El único commit que toca `knowledge/spec` es 0e69da5 y lleva `Fuente: ADR-0068, ADR-0067` en el cuerpo. Los dos ADR existen en `docs/adr/`.
> - **Spec docs.** `knowledge/spec/ambiguedades.yaml` y `docs/spec/ambiguedades.md` cambian en el mismo commit, con el mismo texto de A-54 y A-55. `spec check` da OK. No se abre ni se cierra ninguna ambigüedad, así que la tabla de `PROJECT_STATE.md` y los cinco sitios del runbook no se tocan. El diff del yaml cambia solo el campo `pregunta`.
> - **HISTORIA solo se amplía.** `git diff main...HEAD -- docs/state/HISTORIA.md | grep -c '^-[^-]'` da 0. Añade `# Archivo 8` y una sección `# Technical Debt PAGADA` con la línea movida, literal.
> - **Informes cerrados.** `git diff main...HEAD` sobre `FTMO-REGLAS.md` es un solo hunk de líneas añadidas (+39), un recuadro `>` pegado tras el recuadro del traslado. En `CIERRES-DE-MERCADO.md` son dos recuadros de CORRECCIÓN (+9) con fecha y rama, y el cuerpo queda intacto. Ninguna línea fue eliminada ni editada.
> - **ADR-0068.** El cambio sustituye la cita «(traslado de Aleks del 29-09-2026)» por la frase literal de FTMO y un puntero. `## 8. Segunda orden del consultor (2026-10-03)

Copiada tal cual al final de `docs/encargos/trabajo-fuentes-ftmo.md`. Lo hecho:

1. **El recuento.** El consultor confirma que el error era del encargo. El correo tiene diez
   preguntas numeradas del 1 al 10:
   - la 1 a la 4, mensajes al servidor (A-54);
   - la 5 a la 9, gap trading (A-55): la 5 a la 7 son P1 (a-d) de `CIERRES-DE-MERCADO.md` §0.6, la 8
     es P2 y la 9 es P3;
   - la 10, tamaño de posición (R17).

   Se corrigió «P1-P4» en los textos de esta rama: el recuadro de `FTMO-REGLAS.md` y §2 de este
   informe, con un recuadro de corrección. El encargo y el informe del revisor pegado en §7 se dejan
   como estaban: son copias literales de su tiempo.
2. **El correo, como fuente escrita**, igual que la respuesta del 29-09. Va en `FTMO-REGLAS.md`, en
   un recuadro después del de la respuesta, con:
   - el remitente, el destinatario, la fecha, el asunto y el ticket;
   - el texto tal cual;
   - una tabla que dice a qué responde cada pregunta: A-54, cada P de `CIERRES-DE-MERCADO.md` §0.6 y
     R17.

   Del texto solo cambia el ajuste de línea, con las preguntas largas sangradas bajo su número.
3. **El número de pregunta**, en los tres sitios que lo piden:
   - A-54: «preguntas 1 a 4 de su correo»;
   - A-55: «preguntas 5 a 9 de su correo: la 5 a la 7 son P1 (a-d), la 8 es P2 y la 9 es P3»;
   - la línea de R17 en Technical Debt: «pregunta 10 del correo».

   `spec docs --escribir` va en el mismo commit.
4. **PROJECT_STATE**: no se saca nada más. El tope del test es 25.000 y el margen de 23.000 es del
   consultor. Queda en 22.937 bytes.

**Revisor:** solo sobre lo que cambia en esta orden. Su informe, en §9.

## 9. Informe del revisor, segunda pasada

INFORME_REVISOR_2

## Estado` no se toca. Está permitido por el contrato.
> - **Tres guardias de `cita`, régimen de evidence, feedback, manifiestos y libros, holdout y exposiciones.** No aplican: el diff no toca nada de eso.
> - **Literalidad del recuadro (pedido especial).** Comparé a mano el texto de `FTMO-REGLAS.md` líneas 124-155 con el del encargo, palabra por palabra: saludo, párrafo de Swing, «**gap trading is not permitted**», el párrafo de comisiones entero en negrita, la URL `<https://ftmo.com/en/symbols/>` y la despedida. Son idénticos. Solo cambia el ajuste de línea.
> - **Patrón de citas.** `FTMO-REGLAS.md` cita cada regla con texto literal entre comillas más la fuente al lado (URL y día de lectura, líneas 7-8 y tabla de la línea 48 en adelante). El recuadro nuevo hace lo mismo: texto literal más remitente, hora UTC y correo al que responde, porque el correo no tiene URL. Va junto al recuadro del mismo ticket (línea 97), que es el patrón de corrección de un informe cerrado.
> - **Citas del ticket.** `grep` de «traslado», «trasladó» y `VDW-DPMWR-965` fuera de HISTORIA y del informe de la rama:
>   - `FTMO-REGLAS.md:97` queda tal cual, a propósito, y lo corrige el recuadro de la línea 124.
>   - `CIERRES-DE-MERCADO.md:32` queda intacto bajo el recuadro de CORRECCIÓN de la línea 27.
>   - `CIERRES-DE-MERCADO.md:473` y `:515` son el informe del revisor pegado, citas de su tiempo.
>   - ADR-0068 línea 89 apunta ya a la fuente literal.
>   - `docs/encargos/feature-cierres-de-mercado.md:12` es un encargo cerrado.
>   - No queda ninguna cita viva que diga «traslado de Aleks» sin cambiar.
> - **Technical Debt.** La línea «PENDIENTE DE FTMO: EL BOT PUEDE ABRIR…» sale de `PROJECT_STATE.md` y entra literal en HISTORIA (diff, línea 223). La cubren A-55 (ahora con la pregunta enviada) y la entrada N de Next Action (`PROJECT_STATE.md:46`, renovación del calendario). La decisión es coherente con el ADR-0068 y con la salida «o muévela a HISTORIA» del encargo.
> - **Línea nueva del tamaño de posición.** `PROJECT_STATE.md:122` dice «SI UN LOTE QUE VARIA CON EL STOP… CUENTA COMO "substantially larger position sizes" (R17): el ticket… no lo contesto el 2026-09-29; repreguntado el 2026-10-03». Es exacta frente al encargo y frente a lo que decía el recuadro de la línea 97 («quedó sin respuesta, R17 sigue abierta»). `grep` de «substantially larger» no encontró otra línea de Technical Debt que la cubriera.
> - **A-54 y A-55.** El texto nuevo dice «enviado por Aleks el 2026-10-03 en el ticket VDW-DPMWR-965… respuesta pendiente». Es exacto frente al encargo. No inventa el contenido de las preguntas. Conserva la nota de que la cita de evidencia es de relleno.
> - **Las diez preguntas.**
>   - El recuadro de `FTMO-REGLAS.md` y el informe (§2) dicen «diez preguntas» y su reparto (mensajes P1-P4, gap trading P1-P3, tamaño de posición) como lo dijo el encargo.
>   - Declaran que el texto del correo no está en el repo.
>   - El informe nota que 4+3+1 = 8 ≠ 10 y no lo resuelve.
>   - Es correcto y no afirma más de lo que consta. Pendiente para Aleks: guardar ese correo.
>   - La rotulación «P1-P4 de mensajes» viene solo del encargo: no hay fuente escrita de la numeración. El informe lo dice.
>
> ### Eje (b) · Encargo
> Resumen: 0 bloquea, 0 importa, 1 menor. Requisitos: 10 hechos, 0 parciales, 0 no hechos (1 «hecho de otra forma», declarado).
>
> | # | Requisito | Estado | Evidencia |
> |---|---|---|---|
> | 1 | Existe `docs/encargos/trabajo-fuentes-ftmo.md` | Hecho | Lo creó c4adb52; es el texto del encargo copiado tal cual. |
> | 2 | Guardar como fuente escrita la respuesta literal de FTMO al ticket VDW-DPMWR-965, con remitente `support@ftmo.com`, recibida el 2026-09-29 a las 14:00:47 UTC, en respuesta al correo de Aleks del 2026-09-28 | Hecho | `docs/validation/FTMO-REGLAS.md` líneas 124-130 (cabecera del recuadro). |
> | 3 | Sitio según el patrón con el que `FTMO-REGLAS.md` cita sus fuentes | Hecho | Ver «Patrón de citas» arriba; el informe lo razona en §1. |
> | 4 | Texto literal, con negritas, sin firma ni imágenes | Hecho | Comparado palabra a palabra con el encargo, idéntico. |
> | 5 | Nota: el correo preguntaba tres cosas; la del tamaño de posición («substantially larger position sizes») NO se contestó | Hecho | `FTMO-REGLAS.md` líneas 150-154, y `FUENTES-FTMO.md` §2. |
> | 6 | Nota: Aleks reenvió el 2026-10-03, en el mismo ticket, diez preguntas (mensajes al servidor P1–P4, gap trading P1–P3 de CIERRES §0.6 y tamaño de posición); respuesta pendiente | Hecho | `FTMO-REGLAS.md` líneas 154-158; recuadro de CORRECCIÓN en `CIERRES-DE-MERCADO.md` §0.6. |
> | 7 | Cambiar las citas «traslado de Aleks» del ticket para que apunten a la fuente literal | Hecho | ADR-0068 línea 89; recuadros de CORRECCIÓN en `CIERRES-DE-MERCADO.md` líneas 27 y §0.6. El cuerpo de los informes cerrados no se toca, por la regla de `CLAUDE.md`. |
> | 8 | Technical Debt: reescribir la línea «PENDIENTE DE FTMO… HORAS PREVIAS…» o moverla a HISTORIA si ya la cubren A-55 y la línea N | Hecho de otra forma (una de las dos salidas del encargo, declarada) | Movida a HISTORIA. El informe (§3) justifica por qué: A-55 y la entrada N la cubren. |
> | 9 | Añadir una línea sobre el tamaño de posición sin respuesta, si no hay ninguna que lo cubra | Hecho | `PROJECT_STATE.md:122`. El informe justifica que ninguna lo cubría. |
> | 10 | A-54 y A-55 dicen que sus preguntas están enviadas el 2026-10-03, en el ticket VDW-DPMWR-965; `spec docs --escribir` en el mismo commit | Hecho | `knowledge/spec/ambiguedades.yaml` líneas ~1492-1540 y `docs/spec/ambiguedades.md` líneas 131 y 137, ambos en 0e69da5. |
> | 11 | PROJECT_STATE por debajo de 23.000 bytes | Hecho | 22.913 bytes. |
> | 12 | `make check` sellado | Hecho | Línea `SELLO` sobre el árbol de HEAD; ver eje (a). |
> | 13 | Revisor con su informe pegado; rama lista para revisión, NO cerrada | Pendiente de este paso | El informe dice «EN CURSO… falta el revisor»; pegar este informe al final de `FUENTES-FTMO.md` y actualizar el estado. No lo pego yo: lo devuelvo. |
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | b1 | menor | El «Estado» final de `FUENTES-FTMO.md` dice «EN CURSO… falta el revisor». Tras pegar este informe habrá que actualizarlo a «lista para revisión, NO cerrada». | `FUENTES-FTMO.md`, última línea. |
>
> Nada de lo que el encargo dice que NO se toca (motor, cifras, `src/`, `tests/`, `parametros.yaml`, `strategy_spec.yaml`) aparece en el diff. Nada de lo que la rama hace queda fuera del encargo: el ADR-0068 y los dos recuadros de `CIERRES-DE-MERCADO.md` son la consecuencia de «cambia las citas» y el informe los declara.
>
> ### Lo que no pude comprobar
> - `uv run botsito knowledge validate > knowledge-validate.log`: escribe un fichero, no lo ejecuté. No existe el log. Me fío del informe (§5) y del trailer, cuyos ids sí existen.
> - `make check > make-check.log`: no lo ejecuté. La evidencia es `make-check.log` (sello igual al árbol de HEAD, 1860 passed).
> - La afirmación del informe sobre la línea del 2026-09-25 en «Decisions and Rationale» (que no cubre la pregunta a FTMO): no la leí línea a línea.
> - El texto de las diez preguntas reenviadas y su recuento: no está en el repo, el informe lo declara y yo no puedo verificarlo.
> - La hora y el remitente del correo, la fecha de la respuesta y el reenvío del 2026-10-03: solo constan por el encargo, no hay fuente primaria en el repo (eso es justo lo que la rama guarda).
>
> ### Comandos ejecutados
> - `git log --format='%h %s' main..HEAD`, `git diff --stat main...HEAD`, `git status --short`, `cat contrato.yaml`, `cat docs/encargos/trabajo-fuentes-ftmo.md`
> - `git diff main...HEAD -- docs/validation/FTMO-REGLAS.md docs/validation/CIERRES-DE-MERCADO.md docs/adr knowledge/spec/ambiguedades.yaml docs/spec PROJECT_STATE.md`
> - `git log --format='%h%n%B' main..HEAD -- knowledge/spec`, `wc -c PROJECT_STATE.md`
> - `cat docs/validation/FUENTES-FTMO.md`, `git diff main...HEAD -- docs/state/HISTORIA.md` (varios filtros con `grep`)
> - `grep -E 'SELLO|PICO' make-check.log` y `grep -E 'passed|failed|exit' make-check.log`
> - `uv run python scripts/contrato_rama.py`, `uv run botsito state check`, `uv run botsito spec check`, `git diff --name-status main...HEAD`
> - Grep de «traslado», «trasladó» y `VDW-DPMWR-965` en `docs/`, `knowledge/spec/` y el resto del repo
> - `git rev-parse HEAD^{tree}`
> - Lectura de `docs/validation/FTMO-REGLAS.md` líneas 95-123 y de `PROJECT_STATE.md` línea 46
> - Un primer intento de `grep -r .` sobre todo el repo lo bloqueó la guardia (rozó material protegido); no lo rodeé y lo sustituí por Grep acotado a `docs/`, `knowledge/spec/` y excluyendo `corpus/`, `data/` y `.venv/`.

## Estado

EN CURSO: segunda orden hecha (§8); falta el revisor de la segunda pasada.
