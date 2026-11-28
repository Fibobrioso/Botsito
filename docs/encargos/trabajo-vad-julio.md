# Encargo · trabajo/vad-julio

Dado por Aleks (consultor) el 2026-11-27. Copiado tal cual:

> Modelo: Opus 5.5 · Esfuerzo: alto
>
> ENCARGO DEL CONSULTOR (2026-11-27) · rama `trabajo/vad-julio` · tag al cerrar: `stable/F39s-vad-julio` (verifica con `abrir-rama`, contra origin, que el último tag es F39r)
>
> Antes de nada, revisa /model (Opus 5.5, alto). Aleks deja esta rama corriendo de noche: las PARADAS de §4 son condicionales y las decisiones van por adelantado en §5. Nunca cierres.
>
> ## 0. Base y apertura
>
> - Base: `main` en `139800f5` (commit de estado del cierre de F39r; el merge `d44f3e58` lleva el tag `stable/F39r-renovar-cierres-2026-11-26`; CI de main 46066643655 según el informe final que vio el consultor: confírmalo con `gh`), sin ninguna otra rama. Verifícalo con la skill `abrir-rama`; si algo no cuadra, PARA y dilo.
> - Abre con `/abrir-rama trabajo/vad-julio`: encargo copiado tal cual en `docs/encargos/trabajo-vad-julio.md`, `contrato.yaml` y el Archivo en HISTORIA. Tramo: R2 (R2.5, letra C). Riesgo: alto (toca `src/botsito/corpus/` y el ASR de ADR-0007). Ningún ADR nuevo: el cambio de ADR-0007 va como enmienda dentro del propio ADR (D1), como la del 2026-09-06 (`docs/adr/README.md` recoge enmiendas así en otros ADR); el bloque ids-inexistentes no declara ninguno.
> - Lista blanca del contrato:
>   - este encargo y `contrato.yaml`;
>   - `src/botsito/corpus/motor_whisper.py`, `src/botsito/corpus/pipeline_transcripcion.py`, `src/botsito/corpus/transcripcion.py` (el motor `falso` vive ahí) y `src/botsito/cli.py`, solo para D1 y D2;
>   - `docs/adr/0007-transcripcion-en-dos-capas.md`, solo la enmienda de D1 y su `## Fecha / fase`;
>   - el test nuevo `tests/unit/test_transcripcion_vad.py`, y los tests existentes que la fase 0 diga que hay que tocar (se añaden al contrato en el mismo commit que los toca, con su motivo);
>   - `knowledge/corpus/transcripciones/`, solo manifiestos NUEVOS (nunca se edita uno);
>   - `knowledge/corpus/fuentes.yaml`, solo el comentario de v12 a v14 y solo si lo medido contradice lo que dice;
>   - el informe `docs/validation/VAD-JULIO.md` y sus anexos (`docs/validation/anexos/VAD-JULIO/`, con el guion de medida de D3);
>   - `docs/validation/HOLDOUT-EXPOSICIONES.md`;
>   - `PROJECT_STATE.md` y `docs/state/HISTORIA.md` (lo de `abrir-rama` y el recuento de tests si `state check` lo pide);
>   - y, SOLO para el commit de F5 posterior a la respuesta a la PARADA final (§6): `knowledge/cases/criterio_fidelidad.yaml`, `src/botsito/engine/cableado.py`, `src/botsito/cases/criterio_fidelidad.py` (las frases «hasta que T lo compruebe» de VIDEO-JULIO.md:142), los tres goldens `tests/golden/metodo_adr0092/main-{hueco,stop,viva}.txt`, `tests/unit/test_criterio_campos_adr0092.py` y `tests/unit/test_metodo_adr0092.py`, según lo que rompa (VIDEO-JULIO.md §0.4, :106-161). Antes de esa respuesta no se tocan.
> - `rutas_protegidas`: las de la plantilla de `docs/runbooks/CONTRATO-DE-RAMA.md`, sin tapar ninguna ruta de la lista blanca. Lo protegido manda y los patrones no admiten clases `[...]` (`scripts/contrato_rama.py`:156-177): lo que haya que proteger dentro de un directorio permitido se nombra fichero a fichero.
> - Lecciones que aplican:
>   - la fila de HOLDOUT-EXPOSICIONES del día va ANTES del primer `make check` del día, y si el trabajo pasa la medianoche, la del día nuevo antes del siguiente;
>   - toda frase «la herramienta X da Y» se ejecuta antes de escribirla;
>   - nada de `make check` mientras corre una transcripción (VIDEO-JULIO.md §1.7);
>   - `state check` pide el recuento de tests al día si añades funciones (córrelo antes);
>   - un guion de anexo recibe la raíz y la salida por argumento;
>   - un fotograma de un backtest solo se abre después de que la voz o un fotograma ya abierto sitúen el tramo en julio, nunca en el arranque de una grabación, y antes de abrirlo se mira si el segmento o sus vecinos leen cifras del mes: si las leen, no se abre (VIDEO-JULIO.md, respuesta a la PARADA final, puntos 0 y 5; ERRORES-RECURRENTES).
>
> ## 1. Objetivo
>
> La letra C y R2.5: el VAD de `corpus transcribe` (el de Silero dentro de faster-whisper; `vad_filter=True` por ADR-0007 §3, con sus parámetros por defecto, `motor_whisper.py`:7) se salta frases cortas del trader. En v14, de 0:10:00 a 0:11:00, Aleks escuchó que el trader solo dice «bias bajista», que se le oye toser a él y que no hay más voz (VIDEO-JULIO.md, «El minuto de escucha», 2026-11-09); ninguna transcripción lo tiene.
>
> Lo que se pide, en orden:
> - exponer la configuración del VAD;
> - elegir, con un criterio escrito antes, la configuración que recupera esa voz sin inventar texto;
> - retranscribir v12, v13 y v14 con `--reemplaza-a`;
> - volver a medir en los huecos lo de F2, F3, F4 y F6 de VIDEO-JULIO.md;
> - llevar al consultor lo medido para decidir F5 (`material_sin_video` de julio).
>
> Por qué ahora: no depende de FTMO, del trader, de los ingenieros ni del ADR de la salida C, y R4.7 pide revisar antes de ese ADR el sesgo del material sin vídeo (S-14), del que F5 decide la parte de julio. Julio es material de construcción.
>
> ## 2. Qué NO cambia
>
> - Motor de la estrategia, simulador, spec, casos, evidencia, feedback y `data/manifests/`.
> - La hoja de ruta: va en el cierre.
> - Lo de F5 de la lista blanca, hasta la respuesta a la PARADA final.
> - La configuración POR DEFECTO de `corpus transcribe`: ningún manifiesto de transcripción ya commiteado cambia de huella ni de significado.
> - Las transcripciones de otros vídeos: no se rehacen.
> - No se crea ningún ítem de evidencia ni ningún caso.
> - No se copian cifras de resultados que diga el trader.
>
> ## 3. Fase 0 (inventario, sin tocar código)
>
> - 0.1 La fila de HOLDOUT del día. Esta rama lee transcripciones filtradas de v12 a v14 y abre fotogramas de julio por instantes localizados: la fila lo dice. Antes, comprueba con `casos_reservados` que ningún día de julio está en una partición.
> - 0.2 Lee y resume, con fichero:línea:
>   - ADR-0007 (§3 y la enmienda del 2026-09-06);
>   - `motor_whisper.py`: dónde se fija `vad_filter`, qué entra en `describir()` y que `describir()` carga el modelo;
>   - `pipeline_transcripcion.py`: `huella_de`, `CLAVES_FUERA_DE_HUELLA`, `_carpeta_base_registrada_ajena` y cómo se ve la huella de una transcripción registrada (los manifiestos no la guardan; las carpetas llevan `hash_corto(huella+sha256_video)`, `trabajo.py`:52);
>   - `scripts/transcribir_sesion.py`:559-575, que también usa `huella_de`;
>   - el motor `falso` (`transcripcion.py`:100-120);
>   - `cli.py`: `corpus transcribe` y `corpus transcript show`;
>   - `cargar_cruda` y `filtro_de`;
>   - VIDEO-JULIO.md: §0.4, §1.5-§1.7, §3.0, §3.2, §3.5, §4, §5, §6, §10.9 y las respuestas del consultor a las PARADAS 4 y final.
> - 0.3 Los parámetros del VAD de la faster-whisper instalada (nombres y valores por defecto), LEÍDOS en el código del paquete del `.venv`, no recordados.
> - 0.4 Las transcripciones activas de v12 a v14 (deben ser `tr-v12-…-cb502503`, `tr-v13-…-7f5333a0` y `tr-v14-…-1d289df6`), sus parámetros de corte (v12 600/420/780; v13 y v14 300/180/420) y sus huecos de más de 30 s. Los huecos están en el campo `huecos` de cada manifiesto: `corpus transcript gaps` no existe.
> - 0.5 Si `corpus transcribe` puede correr una candidata SIN registrarla como activa ni escribir su manifiesto en `knowledge/`; y si no, qué escribe y dónde.
> - 0.6 Qué citan las activas por su id. El auditor del consultor midió que `ev-v12-000015-7fc04520` y `ev-v12-000650-370c4bd8` citan `cb502503`, que `ev-v14-004404-ab0281c6` cita `1d289df6`, y que al reemplazar salta un aviso, no un error, mientras la cruda vieja siga en disco (`evidence/modelo.py`:372-413). Confírmalo con `knowledge validate`.
> - 0.7 La tarde del 10 de julio ya está contestada: el trader dijo en la sesión 8 que no se grabó (SESION-08-EXTRACCION.md §3.7, `ev-v20-011213-947092b6`; recuadro en VIDEO-JULIO.md). Las 3 NO APARECE de esa tarde son firmes.
> - 0.8 El auditor `auditor-encargo`, contra este encargo.
>
> ## 4. PARADAS condicionales
>
> Escribe la fase 0 en el informe y SIGUE con §5 si todo cuadra. Para solo si se da alguno de estos casos:
> - (a) Cambiar el VAD obliga a cambiar la huella de los manifiestos ya registrados, y D1 no se puede cumplir.
> - (b) Ninguna candidata cumple el criterio de D3. Para con lo medido y NO retranscribas v12 ni v13.
> - (c) Reemplazar una activa rompe con error la verificación de una cita.
> - (d) Un fotograma que abrirías cae en un tramo no citable (v13 0:00:00-0:00:35, `tramos_no_citables.yaml`), en la vista de Analytics del final de v13 (0:40:42) o donde la voz lee cifras del mes (v13 desde 0:35:43, VIDEO-JULIO.md:297 y :322). En este caso no lo abras: apúntalo y sigue con lo demás.
>
> Deja hecho todo lo que no dependa de la PARADA.
>
> ## 5. Decisiones dadas por adelantado
>
> - D1. **El VAD se configura por transcripción, y lo de hoy no se mueve.**
>   - `corpus transcribe` gana opciones para el VAD: apagarlo y fijar sus parámetros de Silero, con los nombres de 0.3.
>   - La parte del VAD de la descripción del motor sale a una función pura que no carga el modelo, para poder probarla sin GPU.
>   - Con los valores por defecto, esa descripción y la huella dan EXACTAMENTE lo mismo que hoy, sin claves nuevas, y toda transcripción registrada sigue casando.
>   - Con otros valores, el manifiesto los anota y entran en la huella.
>   - Los tests, en `tests/unit/test_transcripcion_vad.py`, rompen a propósito con un cambio deliberado:
>     - (i) para cada manifiesto commiteado, la huella recalculada con la configuración por defecto es la de `main`; la lista de huellas se calcula en `main` con la skill `comparar-con-main` y se fija en el test;
>     - (ii) una configuración distinta cambia la huella y queda anotada;
>     - (iii) la CLI rechaza los valores fuera de rango con un mensaje claro;
>     - todo con el motor `falso`, porque la CI no tiene GPU.
>   - ADR-0007 gana, en el commit del código, una enmienda fechada antes de `## Fecha / fase` (`## Enmienda 2026-11-27 (VAD configurable, R2.5)`). Dice qué cambia, por qué (el minuto de escucha) y qué no cambia, y `## Fecha / fase` se pone al día. La configuración que elija D3 se añade a esa enmienda en el commit de los manifiestos.
> - D2. **Un ensayo no registra nada.**
>   - Si 0.5 dice que hoy no se puede correr una candidata sin registrarla, añade a `corpus transcribe` una opción de ensayo, con su test. Escribe la cruda bajo `data/transcripciones/<video>/`, fuera de las carpetas activas, para que la guardia de los tramos siga aplicándose, y sin manifiesto.
>   - Las candidatas se corren así; solo la ganadora se registra, con `--reemplaza-a`.
>   - La medida de D3 la hace un guion de anexo, `docs/validation/anexos/VAD-JULIO/medir_vad.py`, con la raíz y la salida por argumento. Lee cada cruda con `cargar_cruda(carpeta, filtro_de(...))`, sin `crudo=True`, y dice cuántos segmentos ocultó.
>   - Las crudas de v12 y v14 NO se leen con Read: que la guardia no lo niegue es Technical Debt, y leerlas así sería rodearla.
> - D3. **El criterio para elegir la configuración**, escrito ANTES de correr ninguna candidata. Cópialo tal cual al informe antes de la primera corrida.
>   - Se mide sobre v14 entero, con los parámetros de corte de su activa: solo cambia el VAD.
>   - Candidatas: K0, la activa (la referencia); K1, sin VAD; K2, con VAD pero con el umbral de habla a la mitad del de defecto, el relleno de habla (speech pad) al doble y lo demás por defecto.
>   - **Palabra útil:** una palabra con tiempo, de un segmento que cumple dos condiciones: no lleva ninguna de las señales `repeticion`, `compresion` ni `no_habla` (`transcripcion.py`, `SENALES`; `baja_prob` no excluye), y su texto normalizado no se repite idéntico en 3 o más segmentos de la misma cruda. La segunda condición está porque lo que un VAD apagado inventa en música o ruido suele ser una frase que vuelve. Los segundos se miden con los tiempos de las palabras, no con la duración del segmento. Los segmentos ocultos no cuentan para ninguna candidata.
>   - Para cada candidata:
>     - (i) **control positivo:** en v14 0:10:00-0:11:00 hay palabras útiles que, normalizadas (minúsculas, sin acentos, con el glosario aplicado), incluyen «bias» y «bajista», que es lo que Aleks oyó, no lo que dice un ASR;
>     - (ii) **control de lo inventado:** en ese mismo minuto, en el que según Aleks no hay más voz, las palabras útiles que no son «bias» ni «bajista» son como mucho 4;
>     - (iii) **lo que gana:** los segundos de palabras útiles dentro de los huecos de más de 30 s de K0;
>     - (iv) **lo que pierde:** los segundos de palabras útiles de K0 que la candidata no cubre con palabras útiles, como fracción de los de K0;
>     - (v) **sospecha de invención:** la fracción de segmentos de la candidata que quedan fuera de «útil» solo por la regla de las 3 repeticiones.
>   - **Gana** la que cumple (i), (ii), (iv) ≤ 0,10 y (v) ≤ 0,05 con más (iii). Si las dos cumplen y la que gana menos se queda a menos del 10 % de la otra en (iii), gana la de menor (iv). Si ninguna cumple, PARADA (b).
>   - El informe dice si hay palabra útil y si casa con lo que oyó Aleks, nunca otras palabras del ASR como hecho.
> - D4. **v12 y v13, con la ganadora y su propia comprobación.**
>   - Cada vídeo se corre en ensayo con la configuración ganadora y los parámetros de corte de su activa.
>   - Se registra con `--reemplaza-a` solo si en ese vídeo (iii) > 0, (iv) ≤ 0,10 y (v) ≤ 0,05. Si no, su activa sigue y lo dices con las cifras.
>   - v14 se registra con la ganadora.
>   - Tras cada registro, `uv run botsito corpus transcript check` en verde. Los manifiestos nuevos van en su commit, sin `make check` a la vez que una transcripción.
> - D5. **Volver a medir F2, F3, F4 y F6 de VIDEO-JULIO** con las transcripciones nuevas, y con las viejas por su id (respuesta a la PARADA 4, punto 1). Se usan los criterios ya escritos allí, sin criterio nuevo: §1.5 para los huecos, §3.0 y §3.2 para F3, las clases de F4 y la tabla de F6.
>   - En F3, solo las 24 operaciones no comprobadas (8 NO LOCALIZABLE y 16 «sin ver», §3.5); las 43 ya clasificadas no se tocan.
>     - Un fotograma se abre solo en un instante localizado por la voz, y nunca por un segmento que no sea útil según D3, con las lecciones de §0 y la PARADA (d). Sin muestrear (ADR-0038).
>     - Sale la tabla de §3.5 de nuevo, con lo que cambia en cada día.
>   - F4: las filas «sin clase (voz no transcrita)» que ahora tienen voz, con la clase que les corresponda.
>   - F6: los días «sin datos (hueco del ASR)» (23, 24 y 27) que ahora tienen voz.
>   - F2: el mapa de cobertura de v12 a v14, al día.
> - D6. **Lo que no se hace**: ni casos, ni evidencia, ni F5 antes de la respuesta del consultor. El comentario de `fuentes.yaml` solo cambia si lo medido lo contradice.
>
> ## 6. PARADA final (siempre)
>
> Con todo lo anterior hecho, el informe escrito y la CI de la rama y el revisor pasados (su informe pegado y sus hallazgos resueltos), la PARADA final lleva al consultor la propuesta de F5. Se hace con el criterio de VIDEO-JULIO.md §3.2, que manda sobre el resumen de la respuesta a la PARADA 4:
> - La primera vía no es posible: las 3 NO APARECE de la tarde del 10 son firmes (0.7).
> - Va la **segunda vía**: julio pasa a `meses`, con `dias_con_video` = los días en que, tras D5, todas sus operaciones quedan en COINCIDE o APARECE. Un día con alguna operación aún NO LOCALIZABLE o «sin ver» no entra.
> - La propuesta da la lista de días y los diffs propuestos, sin aplicar, de `criterio_fidelidad.yaml`, `cableado.py`, `criterio_fidelidad.py`, los goldens y los tests (VIDEO-JULIO.md §0.4 y §10.9).
> - También dice lo que cambia para U y para la sesión siguiente, si algo.
>
> El consultor decide. Su cambio va después, en un commit propio con trailer `Fuente:` (ADR-0092 y `ev-v20-011213-947092b6`; verifica que existen), seguido de una pasada corta del revisor sobre ese commit.
>
> ## 7. Entrega
>
> - Los commits de la rama, cada uno con su `make check` sellado:
>   - el código de D1 y D2, con sus tests y la enmienda de ADR-0007;
>   - los manifiestos nuevos, con la línea de la enmienda;
>   - el informe;
>   - y, tras la PARADA final, el de F5.
> - La CI de Linux, porque toca `src/` y la CLI: `git push origin trabajo/vad-julio:refs/heads/fix/vad-julio` (`RITUAL.md`:101-103), con el número de run. El único fallo aceptado es el de `state check` por el nombre `fix/`.
> - El informe `docs/validation/VAD-JULIO.md`, con:
>   - la fase 0;
>   - el criterio de D3, copiado antes de las corridas;
>   - la tabla de candidatas, de (i) a (v), con los tiempos de GPU;
>   - D4 por vídeo;
>   - D5, con la tabla de §3.5 nueva;
>   - las desviaciones;
>   - `make check` y la CI;
>   - la PARADA final;
>   - y, para el cierre, las líneas propuestas de la hoja de ruta (R2.5) y de `PROJECT_STATE.md` (la C sale si R2.5 queda HECHA; quedan unos 887 bytes de margen), comprobadas contra `test_hoja_de_ruta`.
> - El revisor (`.claude/agents/revisor.md`), antes de la PARADA final, con su informe pegado al final del informe de la rama.
> - Tras la respuesta a la PARADA final y el commit de F5, termina con: «Rama lista para revisión, NO cerrada.»

## Respuesta del consultor a la PARADA (b) (2026-11-27)

Copiada tal cual (vale también como respuesta a la PARADA final):

> Modelo: Opus 5.5 · Esfuerzo: alto
>
> RESPUESTA DEL CONSULTOR A LA PARADA (b) de `trabajo/vad-julio` (2026-11-27). Vale también como respuesta a la PARADA final. Cópiala tal cual al informe, en una sección «Respuesta del consultor a la PARADA (b)», y aplícala punto por punto. Leída sobre `f84f4fc` en `fix/vad-julio`.
>
> 1. **R2.5: salida (c). Se cierra sin retranscribir, y el criterio de D3 no se toca.**
>    - D3 se escribió antes de medir y no se relaja después para que pase una candidata. No va ni (b) ni otra tanda (a).
>    - Es una decisión de coste y beneficio, no algo medido. En v14:
>      - K1 (sin VAD) gana 607 s en los huecos, pero escribe 10 palabras en un minuto en el que Aleks no oyó más voz. Queda la salvedad que el revisor dejó abierta: no está medido que el minuto del reproductor y el eje de la cruda coincidan al segundo.
>      - K2 gana solo 31 s.
>    - La pregunta que importaba para F3 era si un VAD distinto recupera las operaciones pendientes de v12 y v13, y eso no se midió: D3 corrió solo sobre v14, que no tiene ninguna operación de F3. Además, 16 de las 24 pendientes son «sin ver» por motivos que no son del ASR (capturas sin eje o sin marcas).
>    - Seguir midiendo cuesta ramas y GPU para un resultado que, como mucho, toca un diagnóstico que ningún umbral lee. Por eso se para aquí.
>    - Queda hecho el VAD configurable y el ensayo (D1 y D2), útil para vídeos y sesiones nuevas. v12 a v14 siguen con sus activas. Las crudas de ensayo se quedan en `data/transcripciones/v14/` (fuera de git), sin borrar.
>
> 2. **F5: NO cambia. Julio sigue provisional** (la tercera salida de la respuesta a la PARADA 4 de VIDEO-JULIO).
>    - Siguen en pie dos respuestas anteriores del consultor:
>      - la de la PARADA 4, punto 3: «si alguna no está comprobada, el bloque no cambia»;
>      - la de la PARADA final, punto 1: no marcar «sin vídeo» ocho días que F2 midió como grabados, salvo la tarde del 10.
>    - El §6 del encargo las sustituía «tras D5», y D5 no se hizo.
>    - Comprobar las 24 operaciones pendientes ya no es trabajo del ASR: pasa al ADR de la salida C como parte del sesgo del material sin vídeo (S-14, R4.7).
>    - No se toca `criterio_fidelidad.yaml`, `cableado.py`, `criterio_fidelidad.py`, los goldens, `fuentes.yaml` ni ningún test de F5. No hay commit de F5.
>    - Lo que sigue diciendo «hasta que T lo compruebe» (T ya no es una letra viva) queda como una línea de Technical Debt propuesta para el cierre: «el texto de julio provisional cita a T, que ya no existe; se reescribe cuando el ADR de C decida S-14».
>
> 3. **Lecciones del consultor.** El cierre las apunta en ERRORES-RECURRENTES como «Error del consultor, apuntado también», como en las filas de renovar-cierres y de reabrir-y-fuente-documental, y no en la columna que mide al revisor.
>    - (a) Fijé el umbral de (iv) en 0,10 sin medir antes el ruido de la propia medida: dos transcripciones con el mismo VAD y otro corte ya dan 0,142. Lección: antes de fijar un umbral sobre una diferencia entre dos salidas, medir con un control cuánto da sin cambio real.
>    - (b) El control positivo (i) exigía un token exacto sin saber cómo escribe ese término el ASR.
>    - (c) D3 midió en v14, donde estaba el minuto de control, pero las operaciones que había que recuperar estaban en v12 y v13. Lección: la candidata se mide donde vive lo que se quiere mejorar, y el control se busca allí.
>    - (d) En el primer borrador de esta respuesta, el consultor dio por medido que «el VAD no las recupera» y cambiaba F5. Lo cazó su auditor antes de entregarla.
>
> 4. **Desviación 2: ACEPTADA.** Los valores por defecto del VAD se quedan fuera del código y solo se guardan los nombres. Así el código no copia valores de una versión del paquete, y esa versión ya está en la huella. Que un valor dado a mano igual al de defecto abra otra carpeta con el mismo resultado es un coste aceptable, y la enmienda de ADR-0007 lo dice. No se usa la exención `# no-negocio:`.
>
> 5. **Desviación 1: ACEPTADA.** Los huecos se toman del manifiesto y no de §1.5. En la práctica ya no aplica, porque D5 no se hace.
>
> 6. **La enmienda de ADR-0007** gana, en un commit propio, un párrafo final: el resultado de D3 (ninguna candidata cumplió; v12 a v14 siguen con sus activas), que solo se midió en v14, y la remisión a `VAD-JULIO.md`.
>
> 7. **Después:**
>    - `make check` sellado en cada commit.
>    - Push a `fix/vad-julio` y el número de run (solo con el fallo aceptado de `state check`).
>    - Una pasada corta del revisor sobre los commits nuevos, con su informe pegado y sus hallazgos resueltos.
>    - En el informe, las líneas propuestas para el cierre, comprobadas contra `test_hoja_de_ruta`:
>      - Hoja de ruta: R2.5 HECHA, con una nota de que se cierra sin cumplir su «Hecho cuando» original, por la decisión del punto 1 y con este informe. R2.4 (:142, «julio sigue provisional») no cambia. En R4.7 (:439, S-14), que la parte de julio no la resuelve el ASR y la decide el ADR de C.
>      - `PROJECT_STATE.md`: la letra C sale, con su texto literal a HISTORIA bajo «# Next Action HECHA · C ·» (no hay ningún registro previo de C), más la línea de Technical Debt del punto 2. Mide el margen: hoy, en la rama, quedan unos 783 bytes.
>      - ERRORES-RECURRENTES: la fila de la rama, con el revisor y las cuatro lecciones del punto 3.
>    - Termina con «Rama lista para revisión, NO cerrada.»
