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
- **Repreguntado el 2026-10-03, en el mismo ticket**, según el encargo: diez preguntas sobre los
  mensajes al servidor (P1-P4), el gap trading (P1-P3 de `CIERRES-DE-MERCADO.md` §0.6) y el tamaño de
  posición. Respuesta pendiente.

**Lo que no está en el repositorio, y no se supone:**
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

`make check` sella cada commit de la rama; su resultado, en el mensaje del commit y en §6.

## Estado

EN CURSO: los tres puntos del encargo hechos; falta el revisor.
