# Encargo · trabajo/guardia-falsos-positivos

Dado por Aleks (consultor) el 2026-11-12, en un solo mensaje. Copiado tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Rama nueva: trabajo/guardia-falsos-positivos (carril «guardias y deuda»: G.6 de la hoja de ruta y la deuda de la guardia que dejó trabajo/capa-generada). Encargo del consultor, 2026-11-12.
>
> 0. Apertura
> - Base: main en el commit de estado de stable/F38z-capa-generada. Verifica con git main, origin/main y el tag, que no hay otra rama abierta y, con gh, la CI de main en verde; si el clasificador niega gh, PARADA. Si trabajo/capa-generada no está cerrada, no abras nada: PARADA.
> - Ábrela con la skill abrir-rama: este encargo tal cual en docs/encargos/, contrato.yaml y el Archivo de PROJECT_STATE en HISTORIA. En el contrato:
>   · tramo: "Carril: guardias y deuda" (entre comillas, como el encabezado de la hoja);
>   · rutas_permitidas, además de lo de siempre: .claude/hooks/guardia.py, tests/unit/test_guardia_*.py, docs/validation/anexos/GUARDIA-G1/medir_g1.py, docs/validation/GUARDIAS-CLAUDE.md y docs/validation/HOLDOUT-EXPOSICIONES.md (la fila del día por los make check, como en capa-generada);
>   · rutas_protegidas: .claude/settings.json, .claude/skills/, .claude/agents/, .claude/hooks/solo_lectura.py y .claude/hooks/estado_sesion.py (lo protegido manda sobre lo permitido, CONTRATO-DE-RAMA.md).
> - Informe: docs/validation/GUARDIA-FALSOS-POSITIVOS.md. Anexos: docs/validation/anexos/GUARDIA-FALSOS-POSITIVOS/.
> - Skills: fase-cero (con el agente auditor-encargo) y entregar-rama. Revisa /model: Opus en esfuerzo alto.
>
> 1. Objetivo
> Que la guardia (.claude/hooks/guardia.py) deje de negar dos cosas legítimas, sin abrir ningún hueco: lo que hoy niega por material protegido lo sigue negando.
>  F1. Un literal de un guion nuevo que empieza por «//» y un espacio (un comentario de MQL5 que el guion escribe), tomado por ruta de red. Caso real: generar_capa.py, en capa-generada, con el literal «// CAPA_HASH = SHA-256 de este fichero sin su linea (docs/validation/CAPA-GENERADA.md).» (verifica que es generar_capa.py:364). Pasa solo en Windows: _canonica llama a _sin_prefijos cuando os.name == "nt", y su regex de recurso de red casa por las barras que vienen detrás.
>  F2. cmp de dos ficheros que no son guiones, leído como si ejecutara el primero: cmp no está en NO_EJECUTAN, y _ficheros_de_un_programa_desconocido toma cada argumento como un guion de lenguaje desconocido. Es G.6 de la hoja de ruta («cmp y diff…»); verifica que diff ya está en NO_EJECUTAN y pasa, y si es así G.6 se cierra con F2.
> Por qué ahora: R6a.3 a R6a.8 escribirán MQL5 desde Python, y en capa-generada estas negativas pararon la rama y empujaron a cambiar de herramienta (diff -q tras cmp). Va en el hueco hasta la sesión 7a (domingo 15): lista para revisión el sábado 14 por la tarde, para cerrarse esa noche.
>
> 2. Lo que queda fuera, y por qué
> - El literal «/» de compilar.py («el codigo nombra la carpeta /»): no se cambia. Hay 39 guiones de main con un literal que es solo separadores, 10 de ellos con recorrido, y la guardia no puede saber cuál lo usa como ruta. Un guion cambiado en la rama que lo nombre lo sigue lanzando Aleks con «!». Lo mismo para la deuda de F38y en Technical Debt (« / » entre espacios, </li> y $'\r' tomados por ruta): mismo mecanismo y misma decisión. La línea de la guardia que entró con F38z se reescribe para decirlo (línea para el cierre).
> - La negativa de git worktree add que se contó en el chat de capa-generada: guardia.py no tiene regla para worktree add (lo niega solo_lectura.py, que es del revisor y del auditor), así que no es de esta rama. No se reproduce ejecutándolo.
> - Los demás lectores con el mismo fallo (comm, xxd, less, nl, tac, base64, strings, sha1sum): la lista solo crece cuando un comando la pide (guardia.py, el comentario de NO_EJECUTAN). Se nombran en el informe. fc no es un lector: en Git Bash es un comando interno que vuelve a ejecutar el historial.
> - D (las formas raras de GUION-MISMO-COMANDO.md §1.26).
>
> 3. Decisiones del consultor (antes de medir; si la fase 0 las contradice, PARADA)
> D1. F1 se nombra en negativo y solo donde nace: en analizar_codigo, un literal cuyos dos primeros caracteres son separadores («//» o «\\») seguidos de un espacio o un tabulador no se trata como ruta, y no llega a _absoluta, _canonica ni realpath. _sin_prefijos no cambia, así que Read, Grep y Bash siguen igual. Nada de una gramática positiva de «nombre de máquina»: reabriría lo que cerró trabajo/guardia-alias.
> D2. F2: cmp entra en NO_EJECUTAN con su porqué, y sus argumentos se comprueban con la política de lectura, como los de diff. La fase 0 mide que cmp con un fichero protegido sigue negado.
> D3. Ningún caso que hoy se niega deja de negarse. Siguen negados, con test, todos los que ya fijan test_guardia_alias.py (las rutas de red y de dispositivo hacia :183-199, :439-463 y :512-520) y test_guardia_g1.py (file:// hacia :622), más los de esta rama: un literal «//host/share/…» y «\\host\share\…» sin espacio en un guion nuevo, cmp con un fichero protegido, y un guion nuevo que nombra y recorre una carpeta protegida.
> D4. Se mide como en trabajo/guardia-g1: en memoria, con decidir() sobre un repo sintético con ficheros falsos; las rutas protegidas se montan a trozos y nunca se imprimen enteras; cada caso dice si se reproduce en Linux o solo en Windows; ninguna excepción por nombre de fichero, solo la condición. F1 y el literal real de generar_capa.py se reproducen en el repo sintético con una copia cambiada del guion (tras el cierre de F38z, el de main ya pasa por ser idéntico al de main). Los casos son los literales reales que estén en CAPA-GENERADA.md y sus anexos; de cmp no quedó la orden literal: usa cmp sobre dos ficheros de docs/ y dilo.
> D5. La comparación caso a caso dentro de la suite: sube GUARDIA_DE_REFERENCIA (test_guardia_g1.py) al último stable, stable/F38z-capa-generada, vacía CAMBIOS_DECLARADOS (medir_g1.py) y declara en ella lo que la guardia nueva deja pasar y ese stable niega: F1 y F2, nada más. Es la regla escrita junto a GUARDIA_DE_REFERENCIA.
> D6. F1 solo existe en Windows: sus tests son de solo Windows y la CI de Linux los salta. La puerta de F1 es el make check de la laptop; la CI de Linux por fix/guardia-falsos-positivos cubre lo demás. Mide en Windows que un literal de F1 no tarda (no debe llegar a realpath; el hook tiene un tope de 30 s en settings.json).
> D7. Antes del merge real, el cierre entero se ensaya en un clon independiente (git clone, no git worktree, que comparte main), como en trabajo/guardia-g1. Los clones, su borrado y cualquier orden que la guardia niegue los lanzo yo con «!».
>
> 4. Lo que NO cambia
> - El motor, la spec, knowledge/, src/, mql5/, el holdout, las demás reglas de la guardia, .claude/settings.json, las skills, los agentes, solo_lectura.py, el Makefile y .gitattributes.
> - Ninguna regla de lectura del material protegido se relaja. Si algo lo necesitara, PARADA.
> - Si la guardia niega algo durante la rama, no se cambia de vía ni de herramienta, ni para comprobar: PARADA, y lo lanzo yo con «!» (lección de capa-generada).
> - PROJECT_STATE, salvo el ritual y «Tests Currently Passing». Mide su tamaño tras F38z: si el cierre le añade algo, recorta antes con los criterios de docs/state/README.md.
>
> 5. Fase 0 (sin tocar la guardia) y PARADA
> a. F1 y F2 reproducidos en memoria (D4): el caso, el motivo literal, la función y la línea que niega, y si pasa en Linux o solo en Windows.
> b. Los casos de D3, cada uno con su decisión en la guardia de hoy.
> c. diff: si está en NO_EJECUTAN, si pasa con dos ficheros de docs/ y si niega con uno protegido. Con eso, si G.6 se cierra.
> d. Cómo propones el cambio de D1 y D2 (función y líneas), y qué tests nuevos rompen con la guardia de stable/F38z.
> e. Herencias: busca F1, F2, cmp, _no_canonizable, _sin_prefijos y NO_EJECUTAN en PROJECT_STATE (Technical Debt), la hoja de ruta (G.6), HISTORIA, GUARDIAS-CLAUDE.md, GUION-MISMO-COMANDO.md (hacia :664-667, la variante de lectores ya medida) y GUARDIA-ALIAS.md. Lo que lo nombre entra o se dice por qué no.
> f. Si no cabe para estar lista el sábado 14 por la tarde, qué recortas.
> PARADA siempre al final de la fase 0. Si lo medido cuadra con D1-D7, mientras esperas puedes escribir los tests.
>
> 6. Fases, tras mi respuesta: tests primero (rotos contra la guardia de stable/F38z), el cambio en guardia.py, la referencia de D5, GUARDIAS-CLAUDE.md si describe lo que cambia, make check sellado en cada commit, CI por fix/, revisor y el ensayo del cierre (D7).
>
> 7. El informe: el encargo frente a lo hecho y las desviaciones; la fase 0 y mi respuesta; cada caso con su test y su decisión con la guardia de stable/F38z y con la de la rama, y si es de Windows o de Linux; las líneas para el commit del contrato: G.6 HECHA en la hoja, la línea de la guardia de Technical Debt que entró con F38z reescrita (F1 y F2 resueltos; «/» y la deuda de F38y siguen, con el porqué del punto 2), simuladas, y el tamaño que quedaría de PROJECT_STATE.
>
> 8. Revisor (opus), con los dos ejes de siempre, y además: que compare caso a caso la guardia de la rama con la de stable/F38z (al partir o recortar una regla se pierden casos), que ningún caso de D3 pase en la rama, que cada test falle con la guardia de stable/F38z por el motivo que dice, y que el cambio de F1 no toque _sin_prefijos.
>
> 9. Plazo: si el sábado 14 a las 18:00 de Lima la rama no está lista para revisión, PARADA y decido yo. La ingesta de la 7a no espera a esta rama.
>
> Rama lista para revisión, NO cerrada.

## Respuesta del consultor a la PARADA de la fase 0 (2026-11-12, 23:00)

Copiada tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA de la fase 0 de trabajo/guardia-falsos-positivos (2026-11-12, 23:00). Cópiala tal cual al informe y al final del encargo, y aplícala punto por punto. Buena fase 0: tus cuatro correcciones al encargo quedan aceptadas.
>
> 0. (a) D1d, solo en Windows: un literal de un guion cuyos dos primeros caracteres son separadores seguidos de un espacio o un tabulador no se trata como ruta, solo si además el tramo hasta el siguiente separador lleva un blanco y el literal no lleva ningún fragmento de SENSIBLES. _sin_prefijos no cambia. Es la única variante medida que deja pasar la copia real de generar_capa.py (los dos literales, :359 y :364) y sigue negando h1-h8. Cada uno de h1-h8 entra como test que tiene que seguir negado, con su columna de Windows o Linux.
> 1. (a) F1 y F2 entran como casos de medir_g1.py; la clave del test que se rompe a propósito pasa a la de F2; y la referencia sube a stable/F38z-capa-generada en el mismo commit que el cambio de la guardia. Declara en CAMBIOS_DECLARADOS solo lo que esa referencia niega y la rama deja pasar.
> 2. (a) «//| docs/x |» y la f-cadena «// …{x}/…» con una variable calculable se declaran como residuo en el informe, con su porqué: ningún guion real lo pide hoy.
> 3. (b) No se lanza medir_windows.py: con D1d no hace falta. Dilo en el informe y no lo commitees si no se usa.
> 4. (a) h1b ('x' + ruta[1:]) se declara como límite conocido, y queda fuera porque ya pasa hoy con cualquier variante y la barrera es el código. Va al informe y, si GUARDIAS-CLAUDE.md tiene una sección de límites, también ahí. No va a Technical Debt, porque PROJECT_STATE está en 24.380 bytes.
> 5. Las correcciones al encargo: la deuda de « / » y </li> es de F38w, y $'\r' es otro mecanismo (la comilla ANSI-C de tokenizar). La línea de Technical Debt que entró con F38z se reescribe para el cierre así: F1 y F2 resueltos; «/» y la deuda de F38w siguen con «!», con el porqué del encargo; $'\r', aparte, sin cambios. Para la fila de ERRORES, del consultor: D1 tal como estaba escrita dejaba pasar ocho casos, contra su propia D3 (importa); D5 rompía test_roto_la_comparacion_con_main (menor); F38y en lugar de F38w (menor); $'\r' metido en el mismo mecanismo (menor).
> 6. Esta noche sigue sin parar: tests primero (rotos contra la guardia de stable/F38z), el cambio en guardia.py, medir_g1.py y la referencia, GUARDIAS-CLAUDE.md si describe lo que cambia, make check sellado en cada commit, push a fix/guardia-falsos-positivos con su CI, y el revisor. Solo paras si un caso de D3 o de h1-h8 pasa, si un test no rompe contra stable/F38z por el motivo que dice, o si la guardia niega algo legítimo (no cambias de vía: lo dejas para mi «!»).
> 7. El ensayo del cierre en un clon independiente (D7): si la guardia te deja hacer el git clone y su make check, hazlo. Si no, déjalo preparado con las órdenes exactas y lo lanzo yo por la mañana.
> Rama lista para revisión, NO cerrada.

## Respuesta del consultor a la PARADA 2 (2026-11-13, 01:15)

Copiada tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA 2 de trabajo/guardia-falsos-positivos (2026-11-13, 01:15). Cópiala tal cual al informe y al final del encargo, y aplícala.
>
> 0. B1: (a). En la condición de F1, los blancos del tramo hasta el siguiente separador se quitan por los dos lados antes de mirar si queda un blanco dentro.
> 1. B2: (a). En un literal de F1, lo único que se exime es leer su cabeza como ruta de red; cada sufijo tras un separador se mira como ruta con las comprobaciones de siempre. Lo que queda (un recorte a mitad de un nombre) es la clase de h1b, que ya pasa con la guardia de stable/F38z: decláralo junto a h1b, con la medida que lo demuestra contra stable/F38z.
> 2. B3 a B7: (a), como están contestados en el informe.
> 3. Los dos xfail estrictos pasan a tests normales que tienen que seguir negados. make check sellado, commit, push a fix/guardia-falsos-positivos con el último commit y su CI (solo el fallo aceptado).
> 4. El revisor otra vez, una pasada entera, no corta, con un alcance más: intentar romper F1 (literales que empiecen por separadores y blanco, con recortes, sufijos, f-cadenas y mezclas de / y \) contra la guardia de stable/F38z. Si encuentra un caso que stable/F38z niega y la rama deja pasar, no paras: F1 sale de la rama (vuelves a la condición de stable/F38z para esos literales, con sus tests como xfail estricto documentado y lo medido al informe, como «F1, aplazado: ninguna condición medida aguanta»), y la rama se queda con F2 y G.6. Después, make check, push y CI.
> 5. El ensayo del cierre (D7): deja en el informe las órdenes exactas para que las lance yo con «!», en el estado final de la rama.
> 6. Al terminar: «Rama lista para revisión, NO cerrada», con la tabla de commits, los runs, el resultado del revisor y si F1 entró o se aplazó.
