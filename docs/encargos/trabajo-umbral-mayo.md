# Encargo · trabajo/umbral-mayo

Dado por Aleks (consultor) el 2026-10-07, como tarea nocturna. Copiado tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> TAREA NOCTURNA (Aleks duerme; 2026-10-07). Nunca cierres: deja la rama con sus commits sellados y el informe, y espera la orden de cierre. Ni merge, ni tag, ni push a main. Si algo de lo que sigue te obliga a parar, para, deja escrito en el informe dónde y por qué, y no improvises una vía alternativa.
>
> Rama nueva trabajo/umbral-mayo, desde main 9e4c89a4a64f2c717fa7feaf31ea1e3b79d2c6b7 (commit de estado sobre el merge 92312e3, tag stable/F37e-respaldo-a11). Comprueba ese sha y ábrela con la skill abrir-rama. Copia este prompt tal cual al encargo.
>
> Objetivo: pre-registrar como ADR, antes de cualquier corrida nueva del arnés, el umbral que habilita medir mayo (punto J de la Next Action). NO cambia: el motor, las reglas, parametros.yaml, strategy_spec.yaml, las tolerancias ni los umbrales de ADR-0043, los conjuntos construccion/medida ni ningún dato.
>
> PROHIBIDO en esta rama ejecutar botsito motor arnes, sobre cualquier mes y con cualquier opción. Todos los tests, sintéticos. Si algo lo pide, PARA.
>
> Decisión del consultor (2026-10-07):
> D1. Mayo (el conjunto de medida de ADR-0043) solo se mide cuando una corrida de botsito motor arnes sobre el conjunto de construcción vigente en knowledge/cases/criterio_fidelidad.yaml dé, en esa misma corrida, una cobertura de al menos 0,70 y una precisión de al menos 0,60 (las mismas cifras de ADR-0043). Una métrica sin definir (sin denominador) cuenta como que no llega.
> D2. Solo cuenta una corrida SIN ninguna opción --diagnostico-*. Mayo mide la spec, no una hipótesis del consultor: mientras el motor necesite un diagnóstico para correr (hoy A-21, A-35 y A-44), mayo no se mide.
> D3. Si no llega, se sigue construyendo y mayo no se toca. El umbral no se relaja después de ver una corrida; cambiarlo exige un ADR nuevo que declare lo visto.
> D4. Las cifras viven en criterio_fidelidad.yaml (ADR-0002), con dos campos nuevos (nombres a tu criterio, que se lean como «umbral de construcción para medir»), y el arnés imprime una línea de veredicto («habilita medir mayo: sí/no», con el motivo, incluido «corrida con diagnóstico») al final de la sección del criterio. No se construye ningún comando de medida de mayo: esa rama vendrá después con su propio ADR (ADR-0048 §7).
>
> Fase 0, sin tocar nada, escrita en el informe. Sigues sin esperarme salvo en las condiciones de PARA:
> a) Comprueba que mayo nunca se ha medido: cita el código del arnés que rechaza los meses de medida y busca en los informes de validation/ cualquier corrida sobre 2026-05. Si alguna lo midió, PARA.
> b) Comprueba que añadir campos a criterio_fidelidad.yaml no choca con su cabecera («no se modifica una vez que el motor produzca su primera salida sobre el conjunto de medida») ni con ADR-0043 «Cambios»; cítalo. Si choca, PARA.
> c) Dónde imprime el arnés la sección del criterio, cómo sabe si la corrida lleva diagnósticos, y qué tests cubren su salida. Si algún test compara la salida con un fichero guardado de una corrida real, PARA: regenerarlo exigiría ejecutar el arnés.
> d) El siguiente número de ADR libre (verifica en el índice que 0070 lo es).
>
> Fases:
> 1. ADR con D1 a D4: problema (mayo solo se mide una vez por versión de la spec y no se puede gastar con un motor que no llega), alternativas (medir mayo ya, un umbral distinto del de ADR-0043, admitir corridas con diagnóstico) y por qué. Cita ADR-0043, ADR-0048 y la decisión de Aleks del 2026-10-06 (el bot es 100 % automático; está en docs/encargos/trabajo-respaldo-a11.md).
> 2. Los dos campos en criterio_fidelidad.yaml, cargados por cargar_criterio con su validación (entre 0 y 1). Trailer Fuente: con el id del ADR.
> 3. La línea de veredicto en el arnés, con tests sintéticos que la rompan a propósito: llega a las dos; falla por cobertura; falla por precisión; métrica sin definir; corrida con diagnóstico que llega a las dos y aun así sale «no».
> 4. Next Action: J no se toca en la rama; sale con la orden de cierre.
>
> knowledge validate antes del primer make check; luego make check y uv run botsito state check en verde, con un commit sellado por fase. Esta rama no toca .claude/ ni la plataforma: sin CI de Linux. Si una ejecución larga muere por memoria, no la relances: anótalo y para.
>
> Informe en docs/validation/UMBRAL-MAYO.md: fase 0, encargo frente a lo hecho, desviaciones, comandos y salidas, y una línea que diga que no se ejecutó el arnés. Revisor con su informe pegado al final, comprobando aparte que ningún commit de la rama ejecutó el arnés y que el test de «corrida con diagnóstico» falla si se quita la condición D2. Arregla en la rama lo que el revisor marque y que no contradiga este encargo; lo que lo contradiga, déjalo anotado para el consultor.
>
> Rama lista para revisión, NO cerrada.

## Respuesta del consultor (2026-10-07), copiada tal cual

> Modelo: Opus · Esfuerzo: alto
>
> Respuesta del consultor a trabajo/umbral-mayo (2026-10-07). Cópiala tal cual al encargo y al informe.
>
> Aceptadas las tres desviaciones de §6 (todo el conjunto de construcción; la línea nombra el conjunto por sus meses; con_diagnostico obligatorio).
>
> 1. CAMBIO DE D2: se niega por defecto. D2 enumeraba un caso (--diagnostico-*), y --depuracion demuestra que se escapan otros. Nueva D2: el veredicto solo puede ser «sí» si la corrida usó únicamente opciones de una lista CERRADA de opciones que no cambian lo que el motor decide ni cómo se llena: --salida, --tracemalloc y --meses (este último solo si cubre todo el conjunto, como ya haces). Cualquier otra opción presente, conocida o futura, da «no» con el motivo «opción fuera de la lista: <nombre>». La lista vive en un solo sitio, con un comentario que cita ADR-0070. Tests que lo rompan a propósito: --depuracion da «no»; una opción inventada añadida al parser en el test da «no»; solo las de la lista da «sí» si llega a las cifras. El test de diagnóstico sigue fallando si se quita la condición. ADR-0070: un recuadro de enmienda en la propia rama (el ADR aún no está cerrado, así que puedes editar su cuerpo; dilo en el informe).
> 2. Antes de escribir el punto 1, mide y deja en el informe una tabla con TODAS las opciones de botsito motor arnes, leídas del código de cli.py (NO ejecutes el comando, tampoco --help): nombre, qué cambia en la corrida y si con ella se puede medir fidelidad. Si --simular (o la que decida si hay simulación del bróker) cambia las operaciones del bot o sus instantes de llenado, PARA solo en ese punto: decido yo si la corrida que habilita tiene que llevarla o no llevarla. El resto del punto 1 lo puedes dejar hecho.
> 3. Hallazgo para la fila de la rama (menor, sesión): se ejecutó uv run botsito motor arnes --help con el encargo prohibiéndolo «con cualquier opción»; sin efecto, declarado. Lección: la ayuda de un comando prohibido se lee en el código, no ejecutándolo.
>
> Sigue igual: no se ejecuta el arnés. knowledge validate, make check y state check en verde; revisor de nuevo sobre lo cambiado, comprobando aparte que una opción nueva del parser da «no» sin tocar la lista.
>
> Rama lista para revisión, NO cerrada.

## Respuesta del consultor a la PARADA de --simular (2026-10-07), copiada tal cual

> Modelo: Opus · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA de --simular en trabajo/umbral-mayo (2026-10-07). Cópiala tal cual al encargo y al informe.
>
> 1. La corrida que habilita medir el conjunto de medida LLEVA --simular, obligatoriamente. Por qué: sin ella el motor no produce operaciones (engine/motor.py:233), y ADR-0043 compara instantes de LLENADO, que solo da el bróker simulado (cableado.py:250); además es como operará el bot. Una corrida sin --simular da «no» con el motivo «sin simulación».
> 2. --perfil y --fase: solo se admiten con el perfil de la cuenta real (FTMO 2-Step Swing 100k, ADR-0026) y su PRIMERA fase. Antes de escribir, lee en el código los valores por defecto de las dos y el nombre de ese perfil y esa fase en knowledge/cuentas/, y déjalo en el informe. La regla se escribe como condición: el perfil y la fase EFECTIVOS de la corrida (dados o por defecto) tienen que ser esos dos; cualquier otro valor da «no» con su motivo. Si el perfil por defecto no es el de FTMO 2-Step Swing 100k, o no hay una fase que sea claramente la primera, PARA y dímelo.
> 3. La lista cerrada queda: --salida, --tracemalloc, --meses (cubriendo todo construcción), --simular (obligatoria), --perfil y --fase (solo con los valores del punto 2). Todo lo demás, incluido --repo, --depuracion y cualquier opción futura, da «no». Lo de los ticks queda cubierto: un día sin ticks exige --depuracion, que da «no».
> 4. Tests que lo rompan a propósito: sin --simular da «no»; --simular con otro perfil o con otra fase da «no»; --simular con perfil y fase por defecto y con las cifras da «sí»; los anteriores siguen. ADR-0070: su recuadro de enmienda recoge 1 a 3, con fecha.
>
> Sigue sin ejecutarse el arnés. knowledge validate, make check y state check en verde, y el revisor sobre lo cambiado, comprobando aparte que sin --simular nunca sale «sí».
>
> Rama lista para revisión, NO cerrada.
