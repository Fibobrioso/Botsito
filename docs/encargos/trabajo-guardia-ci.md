# Encargo · trabajo/guardia-ci

Dado por Aleks (consultor) el 2026-10-23. Copiado tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Rama nueva: trabajo/guardia-ci (carril de guardias y deuda; la deuda vive solo en Technical Debt de PROJECT_STATE, no en G.1 de la hoja de ruta, y el cierre no añade nada a G.1), desde main en 2a99e64 (el commit de estado sobre el merge 975c086, que es al que apunta el tag stable/F38a-guardia-ffmpeg). Verifica con git las tres cosas, que el tag está también en origin (git ls-remote --tags), que la CI de main sobre su HEAD está en success (con la forma de abrir-rama) y que no hay otra rama abierta; si algo no cuadra, para y avísame. Ábrela con la skill abrir-rama: encargo en docs/encargos/, contrato.yaml y archivo en HISTORIA. Copia este prompt tal cual al encargo, con la fecha de hoy. Tag de cierre: stable/F38b-guardia-ci (la ingesta de la sesión 5 pasa a F38c).
>
> POR QUÉ ESTA RAMA, Y POR QUÉ AHORA
> La sesión 5 se partió en dos: el 23-oct se llegó hasta S-17 y el resto se graba el 24-oct. La ingesta va con las dos grabaciones juntas, después del 24, así que hasta entonces la rama está libre. Esta es corta y no toca nada de la sesión 5. Cierra un hueco que ya se repitió dos veces seguidas: la sesión esperó a la CI con un guion que la consultaba en bucle, contra la orden del encargo (cierre de trabajo/barrido-sesion-5 y entrega de trabajo/ea-conexion, EA-CONEXION.md §13). La regla ya está escrita (docs/runbooks/DECISIONES-DE-PROCESO.md, entrada del 2026-10-21, punto 2), pero la guardia no la hace cumplir. Verifica que la línea de Technical Debt de PROJECT_STATE que empieza «La guardia no niega un guion que espera a la CI en bucle» sigue abierta; esta rama la paga.
> Debe quedar cerrada antes de abrir la ingesta (una sola rama abierta, skill abrir-rama). Si no da tiempo, se para limpia y se retoma con retomar-rama: no se corre.
>
> OBJETIVO
> 1. Que la guardia (.claude/hooks/guardia.py) niegue, por la condición, esperar a la CI con una consulta repetida: una consulta de CI dentro de un bucle o acompañada de una espera.
> 2. Que no niegue la consulta suelta, que es la vía buena: gh run view <run> (con --json, --log-failed o --exit-status), gh run list --branch …, y gh run rerun <run>, uno por comando.
> 3. Una limpieza de documentos: la copia de seguridad (A.4) está HECHA desde el 2026-10-22 y V todavía la pone como dependencia.
>
> QUÉ CUENTA COMO «CONSULTA DE CI»
> gh run (view, list, watch), gh api sobre actions/runs, check-runs o check-suites, y curl contra esas mismas rutas de la API de GitHub. Las formas sueltas que usan hoy los runbooks y skills tienen que seguir pasando tal cual: entre ellas la de RITUAL.md (curl sobre check-runs con $(git rev-parse HEAD) y una tubería a grep, «se espera y se repite la misma línea», a mano), la de abrir-rama (CI de main antes de abrir), la de entregar-rama y la de cerrar-rama. Verifica en la fase 0 si hay alguna más y dilo.
>
> QUÉ SE NIEGA (una lista que la fase 0 puede ampliar, nunca recortar sin PARADA)
> - En shell: una consulta de CI dentro de while, until o for, o en la misma línea de comandos que sleep, timeout con reintento, watch o un bucle; y gh run watch siempre (es una espera que consulta en bucle).
> - En un guion o código en línea (Python con -c, un .py de la carpeta de trabajo o del scratchpad, PowerShell): que llame a gh o a curl con una de esas rutas y además tenga un bucle o una espera (time.sleep, asyncio.sleep, Start-Sleep, while, for). Reutiliza analizar_codigo y lo que la guardia ya lee de los guiones; no abras un analizador nuevo si el que hay sirve.
> - El mensaje de la negativa dice qué hacer en su lugar: «una consulta suelta con gh run view <run>; si hay que esperar, una espera sin consulta (sleep solo, o en segundo plano) y después otra consulta suelta». Con eso, la regla del 2026-10-21 deja a la sesión seguir la forma que propone la guardia, declarándolo.
>
> QUÉ NO CAMBIA
> El motor, la spec, parámetros, ambigüedades, feedback, casos, holdout, corpus, data/, tools/mql5/, el Makefile, CI (.github/) y las reglas de la guardia que no son esta: las formas de ffmpeg de trabajo/guardia-ffmpeg, la cuarentena, motivo_fichero y K siguen tal cual. Lo PRIORITARIO de G.1 (el alias de la raíz, K) NO entra aquí: va en su propia rama. Esta rama no lee ningún material del punto 3 de CLAUDE.md, ni transcripciones, ni fotogramas; si por algo tuviera que hacerlo, PARADA.
>
> REGLAS DE ESTA RAMA
> - Si la guardia o el clasificador niegan un comando: PARADA, salvo seguir la forma que la propia guardia propone en su mensaje, declarándolo en el informe.
> - La CI no se consulta con un guion ni con un bucle: un gh run view suelto cada vez. En esta rama más que en ninguna.
> - Si cambias la guardia y a partir de ese commit te niega algo que antes hacías, es un hallazgo de la rama: PARADA con el comando y el mensaje.
>
> FASE 0 (sin escribir código; con PARADA)
> Mide y apunta, con fichero:línea:
> a) Cómo trata hoy la guardia cada uno de estos comandos: escríbelos en una tabla y pásalos por la función de decisión de la guardia en memoria (como hacen tests/unit/test_guardia_claude.py y test_guardia_ffmpeg.py), sin ejecutarlos de verdad. Mínimo: el bucle while/until/for con gh run view y sleep; gh run view <run> && sleep 30 && gh run view <run>; gh run watch <run>; watch -n 30 gh run view <run>; python -c con subprocess y time.sleep; un .py del scratchpad con lo mismo (el esperar_run.py de EA-CONEXION.md §13 rehecho desde su descripción, no desde un fichero que no existe); un for de PowerShell con Start-Sleep; y, del lado bueno, gh run view <run> --json status,conclusion,headSha, gh run view <run> --log-failed, gh run list --branch fix/x, gh run rerun <run> y sleep 120 suelto.
> b) Qué partes de la guardia ya ven bucles y esperas (PALABRAS_CLAVE, el tokenizador, NO_EJECUTAN, _modo_que_ejecuta para gh, GH_SUBCOMANDOS, analizar_codigo, decidir), y dónde encaja la condición nueva con el menor cambio. Y si .claude/hooks/solo_lectura.py (la guardia de los agentes) deja hoy a un subagente esperar a la CI en bucle: propón si la regla va también allí.
> c) Qué skills o runbooks mandan esperar a la CI y cómo (entregar-rama, cerrar-rama, RITUAL.md): que ninguno quede contradicho por la guardia nueva; si alguno dice «gh run watch» o un bucle, se corrige en esta rama.
> d) Los dos sitios de la limpieza de V: la línea de V en la Next Action de PROJECT_STATE («Depende de R1.1, de R3.1 y de la copia de seguridad (A.4)») y el «Depende de» de R4.1 en docs/plan/HOJA-DE-RUTA.md, que no dice «A.4» sino «la copia de seguridad del carril de Aleks», partido en dos líneas. Verifica que son esos y que no hay un tercero vivo (HISTORIA es registro y no se toca).
> PARADA con la tabla de a), tu propuesta de condición y cualquier caso que no sepas clasificar.
>
> FASE 1 · LA CONDICIÓN (tras mi respuesta)
> - Tests primero, en un fichero propio (tests/unit/test_guardia_ci.py), cada uno roto a propósito en los dos sentidos y con las dos salidas en el informe: los negados de la fase 0 se niegan con el mensaje de arriba; los buenos pasan; y un caso disfrazado por cada familia (la consulta en una variable, gh con la ruta completa del programa, un alias o función de shell, el bucle en una línea con ;), porque las dos ramas de guardia anteriores encontraron sus agujeros justo ahí (ERRORES-RECURRENTES.md, filas de trabajo/guardia-ffmpeg). Lo que no se pueda decidir se niega, con su test.
> - La guardia lee como código sin revisar el fichero de test que se le pasa a pytest (CLAUDE.md, guiones nuevos o cambiados; test_guardia_ffmpeg.py, cabecera): en test_guardia_ci.py, y en cualquier .py de la rama, los literales que junten gh o curl, la ruta de la API y un bucle o una espera se montan a trozos, como hace test_guardia_ffmpeg.py, para que la regla nueva no niegue su propio test. Comprueba que pytest tests/unit/test_guardia_ci.py y make check siguen pasando por la guardia después del cambio; si no, PARADA.
> - Hoy el for con gh run view y sleep ya se niega, pero por otra regla (la variable del bucle fuera de NOMBRES_DE_ENTORNO): los tests comprueban el MOTIVO de cada negativa, no solo que se niega.
> - El código, lo mínimo para que pasen. Comentario en la regla con el porqué y el origen (EA-CONEXION.md §13 y DECISIONES-DE-PROCESO.md).
> - make check completo, con su línea PICO DE MEMORIA, y el tiempo de toda la suite de la guardia antes y después del cambio.
>
> FASE 2 · DOCUMENTOS
> - La limpieza de V de la fase 0 d): «(A.4, HECHA el 2026-10-22)» o quitarla, lo que dejen pasar test_hoja_de_ruta.py y test_project_state.py; di cuál.
> - El Technical Debt del guion de CI sale de PROJECT_STATE en el cierre, no antes: en esta rama solo se prepara la línea para la orden de cierre.
> - Lo que la fase 0 c) haya encontrado falso, corregido aquí; si es un informe cerrado, con un recuadro.
>
> CIERRE DE LA RAMA
> Informe en docs/validation/GUARDIA-CI.md, con la tabla de la fase 0 antes y después del cambio. make check sellado; push a fix/guardia-ci (git push origin trabajo/guardia-ci:refs/heads/fix/guardia-ci; si el clasificador lo niega, me lo dices y lo lanza Aleks con «!») y CI de Linux con solo el fallo esperado de state check; dame el número de run, consultado con gh run view suelto. Después el revisor, lanzado con el informe YA TERMINADO, con este encargo: buscar cinco formas de esperar a la CI que la tabla no recoja y pasarlas por decidir EN MEMORIA, como los tests, sin ejecutar ninguna de verdad ni consultar la CI; decir cuáles pasan. Su informe pegado al final.
>
> Rama lista para revisión, NO cerrada.

## Respuesta del consultor a la PARADA de la fase 0 (2026-10-23)

Copiada tal cual:

> Respuesta del consultor a la PARADA de la fase 0 (2026-10-23). Cópiala al informe, en su sección.
>
> 0. Monitor: SÍ, en esta rama. Amplía el contrato a .claude/settings.json en un commit propio que lo declare. Monitor entra en el matcher de PreToolUse de guardia.py y la guardia decide su comando con las mismas reglas que Bash; si el formato de su entrada no se reconoce, se niega. Tests en los dos sentidos: un Monitor que espera a la CI en bucle se niega, un Monitor que lee material protegido se niega (ruta montada a trozos) y un Monitor inocuo pasa (por ejemplo, esperar a que exista un fichero de la carpeta de trabajo sin leerlo). Además, en el informe: la lista de TODAS las herramientas de esta sesión que ejecutan comandos o leen ficheros, frente al matcher, con fichero:línea. Si aparece otra fuera del matcher que no sea Monitor, no la arregles: PARADA con la lista. Cuando cambie settings.json, di si la sesión tiene que reiniciarse para que el hook nuevo cargue y compruébalo con un caso negado de verdad, sin consultar la CI.
> 1. Rutas de CI: SÍ, añade actions/jobs y commits/<sha>/status y statuses.
> 2. SÍ, negar una espera y una consulta en el mismo comando (sleep 300 && gh run view). timeout N gh run view pasa. El mensaje de la negativa ya da la vía buena: la espera sola, o en segundo plano, y después la consulta suelta en otro comando.
> 3. SÍ, negar un guion con una sola consulta de CI aunque no tenga bucle: es la regla escrita de DECISIONES-DE-PROCESO.md («ninguna consulta de la CI con un guion»).
> 4. SÍ, un recuadro de corrección en docs/sesion-5/PREGUNTAS.md:8-9 (A.4 HECHA el 2026-10-22), ampliando el contrato. Que sea solo ese recuadro: el resto de PREGUNTAS.md lo toca la ingesta.
> 5. SÍ, una línea con la forma de esperar en entregar-rama, cerrar-rama y RITUAL.md:320, con el mismo texto que el mensaje de la negativa. Amplía el contrato a esas skills.
> 6. SÍ, corrige la cabecera de test_guardia_ffmpeg.py y pon un recuadro en GUARDIA-FFMPEG.md: la guardia no lee lo que está bajo tests/ (guardia.py:1989). Mi encargo repetía ese error; lo declaro como error del consultor para la orden de cierre. Como la guardia no lee tests/, los literales de test_guardia_ci.py no hace falta montarlos a trozos, salvo los que nombren material protegido, que siguen a trozos por costumbre.
> 7. SÍ: la limpieza de V se prepara en el informe y se aplica en el commit del contrato del cierre, como manda el punto Y de RITUAL. Lo mismo para la línea de Technical Debt que paga esta rama.
> 8. SÍ, la regla solo en guardia.py, siempre que se demuestre que corre para los subagentes: cita el fichero:línea de la configuración que lo hace y añade un test o una prueba en memoria que lo enseñe. Si no se puede demostrar, PARADA.
>
> También: el for con la variable n, que hoy pasa, entra en los tests junto a los que hoy se niegan por otra regla, comprobando el MOTIVO. Y la fila única de trabajo/guardia-ffmpeg en ERRORES-RECURRENTES: los tests de disfraz cubren los agujeros que dice esa fila, no los cuatro que nombraba mi encargo.
>
> Sigue con las fases 1 y 2 y la entrega tal como dice el encargo, con el revisor al final. Si tocar settings.json te deja sin poder ejecutar algo que antes hacías, PARADA.

## Respuesta del consultor a la PARADA 2 (2026-10-23)

Copiada tal cual:

> Respuesta del consultor a la PARADA 2 (2026-10-23). Cópiala al informe, en su sección.
>
> 0. Artifact, ArtifactData, DesignSync y file_upload de claude-in-chrome: en esta rama NO se meten en el matcher ni en la guardia. Este repo no las necesita para nada, así que se cierran ya por permisos: añádelas a permissions.deny de .claude/settings.json (ya está en el contrato por el punto 0 de la respuesta 1), con su nombre EXACTO tal como aparece en tu lista de herramientas (las de MCP, con su prefijo mcp__…). La regla fina (mirar sus rutas como un Read, por si algún día hacen falta) va a una línea de Technical Debt para su propia rama del carril de guardias, junto a la línea PRIORITARIA del alias de la raíz (K).
> 1. navigate de claude-in-chrome: también a permissions.deny, y con él get_page_text y read_page (las que leerían una página file://). No hace falta medir si la extensión abre file://: el repo no usa el navegador. Va a la misma línea de Technical Debt.
> 2. EnterWorktree: fuera, de acuerdo; solo hace lo mismo que git worktree add por Bash, y eso la guardia ya lo deja pasar.
> 3. SÍ, aplica ya los puntos 0 a 8 de la respuesta 1, Monitor incluido.
>
> Para lo nuevo de los puntos 0 y 1:
> - Un test en test_guardia_ci.py (o donde estén hoy los de settings.json, test_guardia_claude.py:1131) que falle si alguno de esos nombres sale de permissions.deny, roto a propósito en los dos sentidos.
> - En cuanto settings.json cambie, prueba la negativa de verdad con una llamada inofensiva: Artifact con action list, y navigate a about:blank. Las dos tienen que salir negadas, y la salida va en el informe. No hagas ninguna llamada que lea o suba un fichero. Si alguna no sale negada (nombre mal escrito, o hace falta reiniciar la sesión), dilo y PARADA.
> - Si la sesión tiene que reiniciarse para cargar settings.json, dímelo antes de hacerlo y retoma con retomar-rama.
>
> Lo demás, como dicen el encargo y la respuesta 1.
