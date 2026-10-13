# Encargo · trabajo/entrada-julio

Dado por Aleks (consultor) el 2026-10-12. Copiado tal cual (el bloque de abajo no es del encargo:
declara los ids que el encargo cita y que todavía no existen, como exige `knowledge validate`;
cada uno sale de aquí en el commit que lo crea):

```ids-inexistentes
ADR-0078 — el ADR de la fase 2 que este encargo manda escribir (julio entra en construcción); no existe hasta su commit
```

> Modelo: Opus · Esfuerzo: alto
>
> ENCARGO: trabajo/entrada-julio — julio de 2026 entra como material de CONSTRUCCIÓN (R2.1, NA:S)
>
> BASE
> - Rama nueva trabajo/entrada-julio desde main 1d37c7a (tag stable/F37n-activar-sesion-04-motor, que apunta al merge 79e74b2). Ábrela con la skill abrir-rama: comprueba la base entera, copia este encargo tal cual en docs/encargos/, escribe el contrato.yaml y archiva el PROJECT_STATE de main en HISTORIA. Si algo de la base no cuadra (sha, tag, CI de main, otra rama viva), PARA y dímelo.
> - Antes de nada, revisa /model: una pestaña guardó Sonnet con esfuerzo bajo.
>
> DECISIÓN DEL CONSULTOR (2026-10-12), que entra en el informe y en el ADR de la fase 2
> Julio de 2026 es material de CONSTRUCCIÓN, no reservado. Comprobado sobre main 1d37c7a; repite cada punto en la fase 0:
> 1. 2026-07 no está en knowledge/cases/meses_reservados.yaml.
> 2. Ningún particiones.yaml de knowledge/cases/{kit,fidelidad,visto}/ asigna un caso de 2026-07 a una partición reservada. Cuéntalo con casos_reservados(repo) y casos_ocultos(repo), dando el recuento y sin imprimir ids.
> 3. Está en kit/vistos.yaml (visto_el 2026-08-03; v2 y v3 dibujan y operan sobre julio), así que no sirve como mes ciego.
> 4. Tampoco sirve como mes de fidelidad al estilo de septiembre (ADR-0034): en v10 el trader enseñó en pantalla operaciones de julio comentadas en voz (HOLDOUT-EXPOSICIONES, fila del 2026-10-04).
> 5. Es un mes de verano: su ventana de ticks no depende de X (huso_operativa es Europe/Madrid, y en julio la rejilla y Madrid coinciden; ADR-0069 §1 y §5).
> 6. ADR-0073 §5: el trader da por bueno su backtest grabado en vídeo, y «lo mismo dijo de julio».
>
> QUÉ NO CAMBIA
> - Ni el motor (src/botsito/engine, domain) ni la spec (parametros.yaml, ambiguedades.yaml, strategy_spec).
> - Ni los umbrales de criterio_fidelidad.yaml: solo cambia la lista `construccion`, con su ADR (fase 2).
> - Ni febrero, ni marzo, ni diciembre, ni ningún día reservado. PREREGISTRO.md sigue sin rellenar.
> - No corras el arnés sobre la construcción ni midas cobertura ni precisión: eso es R3.1.
> - Las fotos de julio NO se abren nunca, ni miniaturas. Solo se hashean en el inventario.
>
> FASE 0 — inventario, sin abrir nada y sin escribir en el repo (skill fase-cero, con el agente auditor-encargo)
> a) Mide la base y repite los puntos 1, 2 y 5 de la decisión.
> b) Dónde está el material de julio. Pídeme que lo copie, sin abrir nada, a «corpus/Material adicional de su operativa/Backtest julio 2026/». Lista solo los NOMBRES y tamaños de esa carpeta (nunca otra carpeta de meses), y calcula los sha256 del xlsx, el vídeo y las fotos sin abrirlos.
> c) Mide el terreno y escribe en el informe, con fichero:línea, sin cambiar nada:
>    - guardia.py: MESES_DE_DESARROLLO y las reglas que hoy bloquearían el libro de julio (R_SIN_ABRIR).
>    - El camino dev-visto de ADR-0042 (cases/visto.py: requisitos) y lo que pide cada condición.
>    - Cómo deriva los días `casos ingerir` (cases/ingesta.py) y si incluye dev-visto.
>    - Qué exige `data download-ticks` (criterio_fidelidad.yaml `construccion`, cli.py) y qué exige `dias_de_construccion` (engine/arnes.py).
>    - Las horas UTC y los parámetros del manifiesto de ticks de agosto (data/manifests/ticks/eurusd-ticks-2026-08-*.yaml), para repetirlos tal cual.
>    - Cómo se declaró el libro de enero en libros.yaml (medida por velas sobre todas las filas, sin días ocultos) y su control.
>    - El vídeo: el siguiente video_id libre (verifica que es v11), cómo entró v5 (fuentes.yaml, drive_id), qué obliga problemas_de_la_lista en cuarentena.py a un vídeo con drive_id null, y qué tests listan los vídeos (test_inventario.py, test_cuarentena.py).
>    - Los textos vivos que dicen otra cosa de julio o de quién lee las fechas: el párrafo «Material de DESARROLLO» de CLAUDE.md; la cabecera de knowledge/cases/kit/config.yaml (dice «EL CONSULTOR», contra ADR-0072, y que julio «no se declara»); la cabecera de libros.yaml («NO ESTAN enero…»); docs/runbooks/MIRAR-EL-MATERIAL.md (dice que julio «SI tiene dias reservados»; el recuento dice 0). Di cuáles se pueden corregir en la rama y cuáles son de solo añadir.
> d) PARADA. Pregúntame en el terminal, y copia mis respuestas tal cual en el informe:
>    1. Qué son las fotos de julio: si son capturas de Analytics, o de estadística en general, no se abren nunca. Aunque no lo sean, en esta rama tampoco se abren.
>    2. La fecha MÍNIMA y la MÁXIMA de la columna de fechas del xlsx de julio, leídas por mí una sola vez (ADR-0072: QUIÉN, Aleks; QUÉ, solo esa columna). Las declaras ese mismo día en HOLDOUT-EXPOSICIONES.
>    3. Si el xlsx es la exportación del backtest grabado en el vídeo, o de otro backtest.
>    4. Cómo llegó el vídeo (Drive o WhatsApp) y si lo subo a Drive como v5.
>    Entrega el inventario con lo que propones para el vídeo y espera mi respuesta antes de escribir nada.
>
> FASE 1 — la guardia y los textos (rama fix/, porque toca .claude/)
> - Añade 2026-07 a MESES_DE_DESARROLLO de .claude/hooks/guardia.py, con un test que rompa a propósito los dos sentidos: julio se lee; febrero, marzo y diciembre siguen bloqueados, y las imágenes de la carpeta de julio siguen bloqueadas.
> - Corrige en el mismo commit los textos vivos de la fase 0.c que se puedan corregir: CLAUDE.md («enero, abril, julio y agosto»), la cabecera de kit/config.yaml (quién lee la columna de fechas es Aleks, ADR-0072) y MIRAR-EL-MATERIAL.md con un recuadro de corrección fechado.
> - Si libros.yaml es de solo añadir también en la cabecera, no la toques y decláralo.
> - Compara la guardia caso a caso con la de main en el informe: ningún caso que bloqueaba deja de bloquearse, salvo el libro de julio.
>
> FASE 2 — ADR-0078: julio entra en construcción
> - ADR nuevo (verifica que el siguiente número es 0078): 2026-07 se añade a `construccion` en knowledge/cases/criterio_fidelidad.yaml. Cita la decisión del consultor de arriba y ADR-0043, ADR-0070 §2 (el umbral es de «la construcción vigente») y ADR-0042.
> - Ningún umbral cambia, y la decisión es anterior a cualquier corrida del arnés que incluya julio. Que lo diga.
> - Commit con trailer Fuente: ADR-0078.
>
> FASE 3 — el libro, su lectura y su reparto
> a) Verifica de nuevo, en el mismo commit en que vas a leer, casos_reservados y casos_ocultos para 2026-07: 0. Si no da 0, PARA.
> b) Mide el huso del libro por velas con el procedimiento de la cabecera de libros.yaml, sobre todas las filas, con UTC y con Europe/Madrid, y con control sobre un libro de huso conocido (agosto). Si no da ≥90 % / ≤50 %, NO CONCLUYENTE: PARA y no lo declares.
> c) Entrada nueva en libros.yaml (solo añadir) y lectura completa declarada en HOLDOUT-EXPOSICIONES con el nombre del fichero, el mismo día (ADR-0042 §2, ADR-0021 §4).
> d) Tramo de 2026-07 en cobertura_material con la mínima y la máxima que te di y el material_sha256 del libro (como abril).
> e) `uv run botsito casos visto --mes 2026-07`, y commit del reparto y su ancla antes de ingerir.
> f) `uv run botsito casos ingerir --material "<ruta del xlsx>" --fecha <hoy>`. Después `uv run botsito casos check`.
> g) Corrige el docstring de casos_ingerir («DEL KIT») si sigue sin nombrar dev-visto.
> Todo commit que toque knowledge/cases/ lleva Fuente: ADR-0078 (y ADR-0042 o ADR-0039 donde toque).
>
> FASE 4 — los ticks de julio
> - `uv run botsito data download-ticks` con el mismo símbolo, escala y horas que el manifiesto de agosto (fase 0.c), --desde y --hasta de julio y --solo-dias-dev.
> - Luego `uv run botsito data check-ticks --dataset <id> --hashes`.
> - Si una hora no baja, queda marcada y se dice cuántas. Un día sin ticks no cuenta (ADR-0051 §8).
>
> FASE 5 — el vídeo, según lo que yo decida en la PARADA
> - Por defecto: entra en el inventario (manifest.yaml, fuentes.yaml con su naturaleza: backtest de julio del trader, material de desarrollo) y en los tests de vídeos.
> - No es una sesión: no va a SESIONES_EN_CUARENTENA salvo que yo lo diga. La cuarentena por condición se le aplica igual que a todos.
> - La transcripción y los fotogramas NO van en esta rama. Mide solo la duración y propón en el informe la rama que los haga y compare el vídeo con el xlsx.
>
> FASE 6 — aparte, sin relación con julio: la respuesta de FTMO a P-D1
> RESPUESTAS-FTMO.md es un informe cerrado, así que va en un fichero nuevo: docs/validation/FTMO-P-D1.md. Paráfrasis, nunca el texto del correo (su pie prohíbe compartirlo y el repo es público). Recibida por correo el 2026-10-12, ticket JSP-CPQRQ-197:
> - Todas las cuentas de FTMO Global son de cobertura (hedging).
> - El máximo en EURUSD es de 50 lotes, el que enseña la especificación del símbolo en la plataforma.
> - A la pregunta 3 (tope de volumen sumado entre varias órdenes o posiciones) no responden directamente. Dan una pauta general de gestión de riesgo, que no es una regla (como orientación, hasta un 20 % del margen de la cuenta y un 1,5 % de riesgo por idea), y recuerdan que las apuestas a un solo lado están prohibidas.
> Y un hallazgo del consultor, que MIDES antes de escribirlo (regla de oro 1):
> - Verifica que firma_apalancamiento (30) no lo consume ningún código de src/ y que el simulador no comprueba el margen.
> - Con la fórmula de margen de forex de MT5 (lotes × tamaño de contrato × precio / apalancamiento) y con los parámetros del perfil (riesgo_por_operacion, tamaño de contrato, valor del pip), calcula el lote máximo que cabe con todo el margen de 100.000 USD para EURUSD a 1,10 y a 1,20, y el stop mínimo en pips con el que el 0,5 % todavía se cumple.
> - Partir en varias órdenes no lo arregla si el margen se suma; verifícalo en la documentación de MT5 para cuentas hedging (el margen de posiciones del mismo lado) y cítala.
> - Propón en el informe el texto nuevo del heredado 37 y una prueba en la ejecución 2 de la demo: el script 1.1 ya calcula el margen de 1,00 lote (MargenAlcanza), y eso basta para comprobar la fórmula.
> - No cambies código ni parámetros por esto.
>
> INFORME docs/validation/ENTRADA-JULIO.md
> - Fase 0 con la PARADA y mis respuestas literales; cada fase con su evidencia; las desviaciones declaradas.
> - Las exposiciones del día.
> - Las propuestas para la orden de cierre, una por línea:
>   - S sale (HECHA) y F apunta a lo siguiente según la hoja de ruta;
>   - R2.1 pasa a HECHA en HOJA-DE-RUTA.md;
>   - O sale por P-D1;
>   - el texto nuevo del heredado 37;
>   - la entrada nueva de la Next Action «Preparar, celebrar y activar la sesión 5 (R4.1)» con las 8 «en parte» (A-13, A-32, A-35, la segunda parte de A-43, A-44, A-49, A-50, A-53 y S-14; verifica la lista contra ACTIVAR-SESION-04.md §5 y ACTIVAR-SESION-04-MOTOR.md §5);
>   - la rama del vídeo de julio;
>   - y que R0.1 de la hoja de ruta cita NA:P, que ya no está viva.
> - Tamaño de PROJECT_STATE.
>
> TESTS Y CI
> - `make check > make-check.log 2>&1` antes de cada commit, con el sello. Nunca --no-verify.
> - Si la rama cambia el Makefile, la guardia te niega todo make: para y pídeme que lo lance yo con «!». Igual con un push que niegue el clasificador.
> - Empuja la rama como fix/entrada-julio y pasa la CI de Linux (toca .claude/). El único fallo aceptado es el de state check por el nombre fix/. Dame los números de run.
>
> REVISOR Y ENTREGA
> - Skill entregar-rama: el subagente revisor, con su informe pegado al final del tuyo.
> - Que mire en especial la comparación caso a caso de la guardia, que no se haya abierto ninguna foto y que ninguna fecha reservada aparezca en nada commiteado.
> - Termina con: «Rama lista para revisión, NO cerrada.»

## Respuesta del consultor a la PARADA (2026-10-12)

Copiada tal cual:

> Respuesta a la PARADA de trabajo/entrada-julio (consultor, 2026-10-12). Copia esta respuesta tal cual en el informe y aplícala punto por punto.
>
> 0. Ruta: (a), corpus/Estrategia del trader/Material adicional de su operativa/Backtest julio 2026/. Es la raíz del corpus, la que protege la guardia y la que inventaría corpus inventory; la ruta del encargo era un error del consultor.
> 1. Las fotos: ______ (Aleks). Sea lo que sea, en esta rama no se abren: solo se hashean.
> 2. Columna de fechas del xlsx, leída por Aleks una sola vez hoy (ADR-0072): mínima ____-__-__, máxima ____-__-__. Declárala hoy en HOLDOUT-EXPOSICIONES.
> 3. ¿El xlsx es la exportación del backtest del vídeo?: ______ (Aleks). Si es «no» o «no lo sé», sigue igual con el xlsx y apúntalo para la rama del vídeo y para el cuestionario de la sesión 5.
> 4. El vídeo: (a). Aleks lo subió a Drive, a la carpeta de v5; enlace: ______. Entra como v11 con su drive_id y la naturaleza «backtest de julio del trader, material de desarrollo». Es el único camino que no toca código. La transcripción y los fotogramas, en su rama propia.
> 5. El orden: (a). Fase 1 → 3.a-e (inventario, huso, libros.yaml, exposición, cobertura, reparto y ancla) → fase 2 en su propio commit (ADR-0078, construccion y test_criterio_fidelidad.py:108) → 3.f → fase 4 → fase 5 → fase 6. Así cada commit se sella y la decisión sigue siendo anterior a cualquier corrida con julio.
> 6. El huso: (a). Un anexo huso_julio.py que repite el de enero con las funciones de main, comprobando dentro 0 ocultos y 0 reservados, y con el control de agosto por la herramienta de main. Es el procedimiento ya revisado. Amplía el contrato con docs/validation/anexos/ENTRADA-JULIO/.
> 7. El inventario: (a). Aleks copió solo julio. Mira el diff de manifest.yaml y PARA si entra cualquier cosa que no sea de julio.
> 8. Los textos: (a). Corrige R_SIN_ABRIR, R_LIBRO y el docstring de la guardia en la fase 1; y ARNES-MOTOR.md, SESION-DE-PREGUNTAS.md y una NOTA en ADR-0043 en el commit de ADR-0078. Amplía el contrato. Lo que un commit deja falso se corrige en ese commit.
> 9. Las fechas antes del libro: (a). ADR-0078 extiende a julio la excepción de ADR-0039 §1, con una NOTA en ADR-0039 §1 que apunte a ADR-0078. La excepción se ve donde está la regla.
> 10. La fase 6: (a). FTMO-P-D1.md cita ADR-0026 «Impacto» como origen; no es un hallazgo nuevo, y así lo corrige el consultor. Declara que es falso lo que dicen el perfil («Lo consume el broker simulado») y parametros.yaml («F21 lo comprueba»). Propón para el cierre una línea de Technical Debt (que el simulador compruebe el margen, con su rama) y el texto nuevo del heredado 37. No toques el perfil ni la spec.
>
> Además:
> - Las «en parte» son 9 elementos (8 ambigüedades y S-14). La entrada de R4.1 que propongas para el cierre nombra también las preguntas de los §5 (la confirmación bajista de S-13, el último minuto, las dos de ADR-0076 §4 y la racha tras la novena).
> - R0.1 y NA:P: de acuerdo, no hay nada que corregir. Retiro esa propuesta.
> - O va a un fichero nuevo porque RESPUESTAS-FTMO es un informe cerrado: declárala como desviación de la letra de O, aceptada por el consultor.
> - La consecuencia de 0.c (make check corre el sesgo H4 sobre las velas de julio) queda aceptada: solo lee velas y no mide nada.
>
> Sigue con la fase 1. Si la rama cambia el Makefile o el clasificador niega un push, para y dame el comando con «!». Al terminar, revisor, CI de fix/entrada-julio con los números de run, y «Rama lista para revisión, NO cerrada».

## Datos para la fase 3 (Aleks y consultor, 2026-10-13)

Copiados tal cual:

> Datos para la fase 3 (Aleks y consultor, 2026-10-13). Si recibiste antes un mensaje que recortaba la rama porque no había xlsx, queda ANULADO: el Excel llegó y sigue el plan completo de la respuesta a la PARADA (decisiones 0 a 10, con el orden de la decisión 5).
>
> 1. Material copiado a corpus/Estrategia del trader/Material adicional de su operativa/Backtest julio 2026/: el xlsx de julio (nombre tal como lo exportó FX Replay), 4 vídeos de julio y fotos de resumen. Nada de otros meses.
> 2. Las fotos son capturas de resumen (estadística del mes): se tratan como Analytics y no se abren nunca. Solo nombre, tamaño y sha256.
> 3. Columna de fechas del xlsx, leída por mí una sola vez hoy (ADR-0072): mínima 2026-07-01, máxima 2026-07-17. Al leerla vi también la hora de esas dos filas, y nada más. Declárala hoy en HOLDOUT-EXPOSICIONES.
> 4. Lo que dice el trader, de palabra a Aleks el 2026-10-13: el xlsx es la exportación de los 3 primeros vídeos. El 4.º termina el mes (desde el 20 de julio), pero de esos días no exportó el Excel, y ya no puede porque borró el backtest. Así que del 1 al 17 hay vídeo y Excel; del 20 al 31, solo vídeo y las fotos de resumen.
> 5. Vídeos: 4, en Drive de Aleks (carpeta «backtest Julio 2026», 1W0KQ12C-TKCQDTlYmekWgUmYQoCxj2Jq). Entran por orden de grabación, que es el de su nombre:
>    - v11: «2026-10-02 20-18-00.mkv», drive_id 13v1eZMhVq-g9ao17hqqv-hQwjC6xTb1T, 419918585 bytes en Drive
>    - v12: «2026-10-02 20-53-08.mkv», drive_id 1C7lZOtYZ0J12IjzdpWnCEo-CPzwchCz_, 739623714 bytes
>    - v13: «2026-10-04 09-45-43.mkv», drive_id 1w0zlVCMFt1e_TjMOUbNpzPxtQ7-_pYwT, 815725885 bytes
>    - v14: «2026-10-04 12-40-14.mkv», drive_id 19yHqjeekIllhB0zV9Ks_78M3jKZrubU6, 1194821502 bytes
>    Comprueba que los bytes en disco coinciden con los de Drive. Si alguno no coincide, PARA.
>    Naturaleza: «backtest de julio del trader en FX Replay, material de desarrollo». Que v11 a v13 son los del xlsx (1 a 17 de julio) y v14 el del tramo final sin xlsx es lo que dice el trader; como el orden de grabación lo hace probable pero no lo prueba, escríbelo así en fuentes.yaml y en el informe, y lo comprueba la rama de transcripción.
>    De cada uno, con ffprobe y sin abrir fotogramas: duración y si tiene pista de audio, al informe.
>
> DECISIÓN DEL CONSULTOR SOBRE EL TRAMO
> - El tramo de 2026-07 en cobertura_material es 2026-07-01 a 2026-07-17, con el material_sha256 del xlsx. Igual que abril, es un LÍMITE INFERIOR de lo que cubre el libro: un día del borde sin operaciones no se distingue de uno no cubierto.
> - Los días del 20 al 31 de julio NO entran en el reparto dev-visto ni en los casos: no hay libro que los cubra (ADR-0042 §2). Quedan solo en v14.
> - Las fotos tampoco sirven para ellos: son un agregado del mes entero.
> - En el informe y en ADR-0078 queda escrito por qué julio entra en construcción solo del 1 al 17, y que la decisión de sacar casos del vídeo para el resto va después de la rama que transcriba v11-v14.
> - Ticks: download-ticks con --solo-dias-dev bajará solo los días del reparto (1 al 17). Compruébalo en su salida.
> - Propuesta para la orden de cierre: R2.1 pasa a HECHA en lo del libro, y entra una entrada nueva, «Julio 20-31: solo en vídeo (v14); decidir si se extraen casos del vídeo, tras transcribir v11-v14».
>
> Sigue con la fase 3 y el resto, en el orden aprobado. Si el diff de manifest.yaml trae cualquier cosa que no sea de Backtest julio 2026, PARA. Si el Makefile cambia o el clasificador niega un push, para y dame el comando con «!». Al terminar: revisor, CI de fix/entrada-julio con los números de run, y «Rama lista para revisión, NO cerrada».
