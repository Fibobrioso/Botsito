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
