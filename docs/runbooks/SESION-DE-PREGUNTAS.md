# Una sesión de preguntas con el trader

Cómo se prepara, se hace y se registra una sesión **solo de preguntas**: sin `kit build`, sin
paquete, sin casos y sin etiquetado. Escrito el 2026-09-25 en la rama `trabajo/sesion-02`, para la
sesión 02. Hasta hoy el procedimiento estaba repartido en cinco sitios, y aquí se consolida:
- ADR-0011 §8 (la grabación como vídeo del corpus);
- ADR-0012 §7 (`feedback apply`);
- ADR-0022 §7 y ADR-0023 §2 (qué cierra una ambigüedad y con qué procedencia);
- `knowledge/cases/kit/README.md`;
- `docs/validation/SESION-01-*.md` §1.

Si una sesión lleva además días que etiquetar, **no es de este runbook**: va por el kit
(`knowledge/cases/kit/README.md`), con su paquete, sus particiones commiteadas antes y su
precondición de ceguera.

## Las reglas de la sesión

1. **Se graba, con permiso del trader, y sin grabación no hay registro.** El permiso se pide al
   empezar y su «sí» queda dentro de la grabación. Lo que no esté grabado no entra como respuesta
   del trader ni cierra ninguna ambigüedad.
2. **No se enseña ningún gráfico de ningún día.** Ni en pantalla compartida ni en captura. Si el
   trader quiere enseñar algo sobre un gráfico, se le pide que lo describa con palabras. Una
   pantalla con un día reservado dentro es una exposición del holdout (ADR-0021), y un gráfico
   cualquiera puede traerlo sin que se sepa antes.
3. **Si el trader empieza a comentar operaciones concretas de septiembre, se reconduce la
   conversación** hacia la pregunta, sin discutir la operación. Septiembre tiene días reservados.
4. **Las respuestas entran después, y solo por dos vías:** la grabación al corpus y un
   `FeedbackRecord` `RESOLVE_UNKNOWN` por respuesta, en un commit con `Fuente:`. La hoja con las
   notas de Aleks ayuda a localizar, pero no es la fuente: la fuente es la voz.

## Antes (Aleks)

1. **Fijar el día y comprobar que no es un día reservado.** La sesión 01 se grabó en un día que
   resultó estar reservado, y hoy está retirado (ADR-0041). Con el día elegido, en la raíz del
   repositorio (imprime solo `True` o `False`, nunca una fecha):

   ```
   uv run python -c "from pathlib import Path; from botsito.cases.holdout import casos_ocultos; print(any('<AAAA-MM-DD>' in c for c in casos_ocultos(Path('.'))))"
   ```

   Tiene que salir `False`. Si sale `True`, se cambia el día.
2. **El id de la sesión** es `<AAAA-MM-DD>-sesion-02`: el formato que exige el registro de
   feedback, con la fecha del día de la sesión.
3. **Revisar las preguntas** en `knowledge/spec/ambiguedades.yaml`. La hoja las copia tal cual,
   así que un cambio se hace allí, en un commit, y no en el Word.
4. **Generar la hoja, lo último antes de imprimir:**

   ```
   uv run python scripts/hoja_preguntas.py
   ```

   Escribe `hoja-sesion-02.docx` en la raíz del repositorio. **No es un sitio commiteable:**
   `/*.docx` está en `.gitignore`. La hoja no se versiona porque se regenera desde el yaml; lo que
   se versiona es su fuente (`ambiguedades.yaml`) y su orden (`ORDEN_SESION_02` en el script). La
   hoja rellenada se guarda después en el corpus (paso 2 de «Después»).
5. **Preparar la grabación:** grabación de pantalla y de audio de la llamada, probada con unos
   segundos antes de empezar. Sin gráficos abiertos en la pantalla que se graba.

## Durante (Aleks)

1. **Pedir permiso para grabar** y empezar a grabar antes de la primera pregunta.
2. **Seguir la hoja en orden**, leyendo cada pregunta como está. Si el trader no la entiende, se
   le describe la situación de otra manera, **sin ofrecerle opciones ni respuestas**: la pregunta
   se escribió abierta para no sugerir.
3. **Anotar en el recuadro** la idea de la respuesta y, si se puede, el minuto aproximado de la
   grabación. Sirve para encontrar el tramo; la cita saldrá de la transcripción.
4. **Si responde a medias o con un ejemplo**, se le puede pedir que lo diga en general («¿eso lo
   haces siempre así?»), sin proponer la regla.
5. **Gráficos y septiembre:** reglas 2 y 3.
6. **Al terminar**, repasar si alguna quedó sin contestar y parar la grabación.

## Después (Aleks y la sesión)

1. **La grabación al corpus** (ADR-0011 §8). Aleks copia el fichero a
   `corpus/Estrategia del trader/`; la sesión añade el vídeo a `knowledge/corpus/fuentes.yaml` con
   el siguiente `video_id` libre, `drive_id: null`, `fecha_grabacion` y su `naturaleza`, y
   regenera el inventario:

   ```
   uv run botsito corpus inventory
   ```

2. **La hoja rellenada** se copia a `corpus/…/Sesiones/<sesion>/` y queda en el inventario como
   material adicional, como la de la sesión 01. El `.docx` de la raíz lo pisa el generador.
3. **Transcripción y fotogramas**, con el mismo motor que los demás vídeos:

   ```
   uv run botsito corpus transcribe --video <vN>
   uv run botsito corpus frames extract --video <vN>
   ```

4. **Si en la grabación salió algo de septiembre** o cualquier día reservado, ese tramo se declara
   en `knowledge/corpus/tramos_no_citables.yaml` y en `docs/validation/HOLDOUT-EXPOSICIONES.md`
   **el mismo día** (ADR-0021 §4).
5. **Una respuesta, un registro.** Por cada pregunta respondida, con la cita copiada de la
   transcripción CRUDA (`data/transcripciones/<vN>/<modelo>/cruda.txt`) y su tramo:

   ```
   uv run botsito feedback new --sesion <sesion> --fecha <AAAA-MM-DD> --medio video \
     --grabacion "<ruta en el corpus>" --t0 <h:mm:ss> --t1 <h:mm:ss> \
     --objetivo-tipo ambiguedad --objetivo-id A-NN --accion RESOLVE_UNKNOWN \
     --respuesta "<literal de la cruda>" --registrado-por Aleks \
     --recibido-el <AAAA-MM-DD> --procedencia trader_grabado
   ```

   El objetivo es **la ambigüedad**, no el parámetro (ADR-0022). Si la respuesta fija un valor del
   registro, va además el registro sobre el parámetro, y `feedback apply` lo lleva al registro
   (ADR-0012 §7).
6. **Cerrar una ambigüedad toca cuatro sitios** (`CLAUDE.md`): el registro de parámetros vía
   `feedback apply`, `ambiguedades.yaml` en `RESUELTA`, la regla de la spec que la citaba y la
   tabla «Known Ambiguities» de `PROJECT_STATE.md`. Más el test de `tests/unit/test_kit.py` que
   congela cuáles están RESUELTAS, y `botsito spec docs --escribir`. Todo en un commit con
   `Fuente:` y los ids `fb-*` nuevos en el cuerpo.
7. **Una respuesta que no responde** (a medias, con un ejemplo, o en dos sentidos) no cierra
   nada: la ambigüedad sigue ABIERTA, con una nota que cite el tramo. **Una bloqueante no la cierra
   el consultor por decisión**: solo el trader.
8. **El informe de la sesión** en `docs/validation/`: qué quedó resuelto, con qué registro, qué
   sigue abierto y qué compromisos salieron. Con su estado al final.
9. `make check` con la salida a un fichero, y el ritual (`docs/runbooks/RITUAL.md`) lo hace el
   usuario.
