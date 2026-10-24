# Encargo · trabajo/guardia-alias

Dado por Aleks (consultor) el 2026-10-24. Llegó en dos pegados: el primero se cortó a mitad del
punto b) de la FASE 0 («fichero:línea de cada») y el segundo lo retomó desde ese punto b) entero;
aquí van juntos, tal cual. Copiado tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Rama nueva: trabajo/guardia-alias (NA:K, la parte PRIORITARIA; carril G.1 de la hoja de ruta), desde main en af89a78 (el commit de estado sobre el merge 2cc3b93, que es al que apunta el tag stable/F38b-guardia-ci; CI de main run 40092378098). Verifica con git las tres cosas, que el tag está en origin, que la CI de main sobre su HEAD está en success (con la forma de abrir-rama, una consulta suelta) y que no hay otra rama abierta; si algo no cuadra, para y avísame. Ábrela con la skill abrir-rama: encargo en docs/encargos/, contrato.yaml y archivo en HISTORIA. Copia este prompt tal cual al encargo, con la fecha de hoy. Tag de cierre: stable/F38c-guardia-alias (la ingesta de la sesión 5 pasa a F38d).
>
> POR QUÉ ESTA RAMA, Y POR QUÉ AHORA
> La línea PRIORITARIA de G.1 (docs/plan/HOJA-DE-RUTA.md, «PRIORITARIO, porque lee material protegido», y K en la Next Action de PROJECT_STATE) dice que hoy pasan cat, Read, grep -r y find … -exec cat sobre la raíz escrita con \\?\ o con su nombre corto 8.3, o sobre un directorio que CONTIENE el repo, y que las variables se resuelven con el entorno del hook (GUARDIA-FFMPEG.md §9 y §11). El 2026-10-24 una sesión lo midió sin rama, en memoria con decidir, contra un repo inventado con ficheros falsos en tres sitios protegidos: 123 lecturas protegidas pasan. Seis formas de la raíz (\\?\, //?/, \\localhost\C$, \\?\UNC\localhost\C$, el nombre 8.3 y el punto final) en Bash, Read, Grep, Monitor y un guion de Python, y las tres sin \\?\ también en PowerShell (99); una carpeta que contiene el repo con grep -r, find … -exec cat, Grep y Monitor (18); y variables propias con alias y $env: en PowerShell (6). Propuesta de esa sesión: una función _canonica dentro de _absoluta. Sus ficheros están en C:\Users\USER\AppData\Local\Temp\claude\C--Users-USER-Desktop-Bot-v3\49e8894b-c04f-4137-9483-9024a98edd2b\scratchpad\diagK\ (DIAGNOSTICO-K.md, tabla.md, medir_k.py, existe.py, contar.py): verifica que existen y que dicen eso. Si no están, se rehace la medida en la fase 0.
> La ingesta de la sesión 5 va después de esta rama: tiene que quedar cerrada antes de abrirla (una sola rama abierta). Si se alarga, se para limpia y se retoma con retomar-rama; no se corre.
>
> OBJETIVO
> Que motivo_fichero niegue la lectura del material protegido escriba como se escriba la ruta: canonizar antes de comparar, y negar lo que no se pueda canonizar y pueda caer bajo la raíz. Lo mismo en .claude/hooks/solo_lectura.py si la medida lo pide. Lo bueno (src/, docs/, tests/ con cualquier forma de raíz) sigue pasando.
>
> QUÉ NO CAMBIA
> El motor, la spec, parámetros, ambigüedades, feedback, casos, holdout, corpus, data/, tools/mql5/, el Makefile, .github/, .claude/settings.json (salvo que la fase 0 lo pida: PARADA), y las reglas de la guardia que no son esta: la regla de la CI de trabajo/guardia-ci, las formas de ffmpeg, la cuarentena. Las otras partes de K (el falso positivo de exigir_sin_crudo con la variable crudo, y reconocer los tests de un clon de comparar-con-main) NO entran: siguen en K. Tampoco el riesgo residual de trabajo/guardia-ci (la mención a trozos, aiohttp, tests/). Esta rama no lee ningún material del punto 3 de CLAUDE.md, ni transcripciones, ni fotogramas; si por algo tuviera que hacerlo, PARADA.
>
> REGLAS DE ESTA RAMA
> - Todo lo que toque material protegido se mide EN MEMORIA, con decidir de guardia.py y la función de solo_lectura.py, contra un repo inventado en tmp_path o en el scratchpad con ficheros falsos, como hizo el diagnóstico. Nunca se ejecuta de verdad un comando ni una herramienta (Read, Grep, Glob, Monitor) sobre material protegido real. Las rutas protegidas se montan a trozos y no se imprimen enteras; ni fechas de días reservados ni contenido.
> - Si la guardia o el clasificador niegan un comando: PARADA, salvo seguir la forma que la propia guardia propone en su mensaje, declarándolo en el informe.
> - La CI se consulta con un gh run view suelto cada vez (la guardia ya niega lo demás).
> - Si a partir del cambio la guardia te niega algo que antes hacías, PARADA con el comando y el mensaje.
>
> FASE 0 (sin escribir código de la guardia; con PARADA)
> a) Copia el diagnóstico a docs/validation/anexos/GUARDIA-ALIAS/diagnostico/, después de comprobar que ninguno de sus ficheros lleva una fecha de un día reservado, un resultado ni una ruta protegida entera; si alguno la lleva, no lo copies y dilo. Vuelve a pasar medir_k.py sobre el HEAD de la rama y confirma la cifra (123) o da la nueva.
> b) Dónde entra la ruta en cada herramienta (Bash, PowerShell, Read, Grep, Glob, Monitor, el código en línea y los guiones): fichero:línea de cada llamada a _absoluta, _normcase, relativa y motivo_fichero, y si alguna se salta _absoluta.
> c) En Windows: si GetFullPathNameW y GetLongPathNameW (ctypes) están disponibles desde el hook y cuánto tardan (la guardia corre en cada llamada: da el tiempo por ruta). En Linux (CI): qué hace realpath con las mismas formas y qué tests tendrían que ir con skip en Linux.
> d) El lector recursivo sobre una carpeta que contiene la raíz: qué programas y herramientas recorren (grep -r, find, Grep, Glob, Get-ChildItem -Recurse, rg) y cómo los ve hoy la guardia.
> e) Las variables: dónde resuelve hoy la guardia $HOME, ~, $env:… y las variables propias, y por qué pasa S="//?/…".
> f) solo_lectura.py: cuáles de las 123 pasan también allí.
> PARADA con la tabla, la propuesta de condición (una sola función, el orden de los pasos y qué se niega por no canonizable) y cualquier forma que no sepas clasificar.
>
> FASE 1 · LA CONDICIÓN (tras mi respuesta)
> - Tests primero, en tests/unit/test_guardia_alias.py, cada uno roto a propósito en los dos sentidos y con las dos salidas en el informe: cada familia de la tabla negada con su motivo; lo bueno pasando con cada forma de raíz; y un disfraz por familia (mayúsculas cambiadas, barras mezcladas, . y .. intercalados, un espacio o un punto final, la variable definida en el mismo comando). Los de 8.3 y UNC, con skip fuera de Windows y declarados.
> - El código, lo mínimo para que pasen, con el porqué y el origen en un comentario.
> - La tabla del diagnóstico, antes y después, en el anexo.
> - make check completo, con su línea PICO DE MEMORIA, y el tiempo de la suite de la guardia antes y después.
>
> FASE 2 · DOCUMENTOS
> - Lo que la fase 0 encuentre falso en runbooks o skills, corregido aquí; si es un informe cerrado, con un recuadro.
> - Para el commit del contrato del cierre (punto Y de RITUAL), preparado en el informe: la línea PRIORITARIA de G.1 y la parte de K que paga esta rama, con su texto nuevo (lo que queda de K sigue), y cualquier riesgo residual como línea de Technical Debt. PROJECT_STATE está en 23.955 bytes: si lo de esta rama no cabe bajo 25.000, propón qué sale.
>
> CIERRE DE LA RAMA
> Informe en docs/validation/GUARDIA-ALIAS.md. make check sellado; push a fix/guardia-alias (git push origin trabajo/guardia-alias:refs/heads/fix/guardia-alias; si el clasificador lo niega, me lo dices y lo lanza Aleks con «!») y CI de Linux con solo el fallo esperado de state check; dame el número de run. Después el revisor, lanzado con el informe YA TERMINADO, con este encargo: buscar cinco formas de escribir la raíz o una carpeta que la contenga que la tabla no recoja y pasarlas por decidir EN MEMORIA contra el repo inventado, sin leer nada real. Su informe pegado al final.
>
> Rama lista para revisión, NO cerrada.
