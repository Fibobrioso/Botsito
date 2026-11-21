# Encargo · trabajo/guardia-enlaces

Dado por Aleks (consultor) el 2026-11-20, por la tarde, en un solo mensaje. Copiado tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Encargo del consultor (2026-11-20): rama trabajo/guardia-enlaces, tag previsto stable/F39i-guardia-enlaces. Tramo: «Carril: guardias y deuda», entrada G.8 de docs/plan/HOJA-DE-RUTA.md. Riesgo: alto (toca la guardia de Claude Code).
>
> BASE: main en 0562a77b (commit de estado de stable/F39h-guardias-holdout, merge fb1f02e9). Verifica con git que main y origin/main están ahí, que el tag existe en origin, que la CI de main sobre 0562a77b (run 44821324976) está en verde y que no hay otra rama. Ábrela con la skill abrir-rama, con su nuevo paso 6: la fila de HOLDOUT-EXPOSICIONES del día, que nombre la rama, estadiada antes de comprobar.
>
> RELOJ Y PARADA DE MAÑANA
> - Si trabajas pasada la medianoche, la fila del 2026-11-21 se escribe y se estadía antes del primer make check de ese día. G2 la exige.
> - Aleks graba mañana el bloque de días de la sesión 7b y necesita la RAM. A las 09:00 de Lima del 2026-11-21 no puede haber ningún make check ni ningún trabajo pesado corriendo: deja la rama donde esté, con lo hecho commiteado y sellado si da tiempo, y para. Nunca cierras.
>
> OBJETIVO: que la guardia proteja el material protegido por lo que ES y no solo por dónde está respecto de la raíz del repo. Hoy (GUARDIAS-HOLDOUT.md §17; hoja de ruta G.8):
> - con corpus/ como enlace de unión a otro disco, la ruta canónica queda fuera de la raíz y dejan de aplicarse las reglas del material adicional (una imagen de «Backtest marzo 2026» salió PERMITIDA);
> - un Read de la carpeta Backtest <mes> en sí no se niega.
> Lo que veo en el código, y que verificas tú: Guardia.relativa devuelve None fuera de la raíz, y en motivo_fichero, tras la regla del nombre de los libros backtesting-analytics, «if rel is None: return None» deja pasar todo lo demás. Por tanto una COPIA del material fuera del repo (como D:\BotsitoCorpus\corpus, la copia de respaldo que Aleks hizo el 2026-11-20, o un clon desechable de comparar-con-main o de git worktree add en una carpeta temporal) tampoco estaría protegida.
>
> QUÉ NO CAMBIA: src/, knowledge/, config/, scripts/, mql5/, el Makefile, docs/adr/, la hoja de ruta (va en el cierre) y las otras familias de reglas de la guardia (operaciones prohibidas, ejecución verificable, ffmpeg, CI, Monitor). Ninguna regla que hoy niega pasa a permitir: esta rama solo añade negativas.
>
> FASE 0 (inventario, sin tocar código; PARADA condicional: sigue con lo que cuadre con estas decisiones y aparta a la PARADA final lo que no)
> 0.1 Herencias: busca en PROJECT_STATE (Technical Debt), HISTORIA, la hoja de ruta (G.1, G.8) y GUARDIA-ALIAS.md lo que nombre enlaces, realpath, copias fuera del repo o clones desechables. Lo que lo nombre entra o se dice por qué no.
> 0.2 Mide, con la guardia por stdin (JSON de PreToolUse simulado, SIN leer contenido) y con rutas que existan o no según haga falta, la decisión de HOY para cada clase protegida de la familia 1 (holdout 1/2/3, libros de meses no legibles, imágenes del material adicional, carpetas Backtest de meses no legibles, Sesiones/, crudas en cuarentena y *cruda-NO-LEER*, tramos no citables, ficheros con id de caso reservado) en cuatro formas de ruta:
>    (a) dentro del repo;
>    (b) por un enlace dentro del repo que apunta fuera (simúlalo con _realpath, que existe para eso, y, si la plataforma lo permite, con un enlace real en una carpeta temporal);
>    (c) una copia con la misma estructura fuera del repo (una carpeta temporal con corpus/Estrategia del trader/…, knowledge/cases/holdout/1/…, etc., con ficheros sintéticos y vacíos);
>    (d) la carpeta en sí, cuando la clase es una carpeta.
>    Tabla de resultados: permitida o negada por clase y forma. No abras D:\BotsitoCorpus ni nada real protegido: para D:\ solo la decisión de la guardia por stdin.
> 0.3 Pasa el auditor-encargo sobre este encargo.
>
> DECISIONES (tomadas por el consultor; si lo medido las contradice, a la PARADA)
> D1. Una ruta se decide por TODAS sus formas, y se niega si CUALQUIERA niega: la textual relativa a la raíz (sin resolver enlaces), la canónica relativa a la raíz y, si cae fuera de la raíz, por su ESTRUCTURA. Por estructura quiere decir que una ruta canónica que contiene, en cualquier lugar y comparada como hoy (minúsculas, «/»), uno de los anclajes de las clases protegidas se decide como si ese anclaje estuviera en la raíz. Los anclajes son las colas de las constantes MATERIAL, SESIONES, HOLDOUT (con 1, 2 o 3 detrás) y TRANSCRIPCIONES (con un vídeo en cuarentena detrás). Para el material y las sesiones, el anclaje mínimo es «estrategia del trader/material adicional de su operativa/» y «estrategia del trader/sesiones/», sin exigir «corpus/» delante. Nombra la condición, no enumeres rutas.
> D2. La carpeta Backtest <mes> de un mes no legible, como objetivo directo de Read, Grep o Glob, se niega como su contenido. Listar sus nombres con ls, dir o Get-ChildItem se queda como hoy (mídelo en 0.2 y dilo); si hoy se niega, sigue negado.
> D3. Lo que no se pueda canonizar sigue negado (R_ALIAS), igual que hoy.
> D4. Falsos positivos: mide en 0.2 qué lecturas legítimas de hoy pasarían a negarse con D1, en especial en los tests de la guardia que montan árboles en carpetas temporales y en el scratchpad de la sesión. Si alguna lectura que el proceso necesita se niega, a la PARADA con el caso. Los tests que montan árboles falsos y llaman a las funciones con su propia raíz no cambian de resultado: compruébalo.
>
> FASES
> 1. D1 y D2 en .claude/hooks/guardia.py, en el sitio que la fase 0 diga que menos toca (probablemente motivo_fichero, motivo_directorio y la entrada de rutas de Read/Grep/Glob). Sin tocar las demás familias.
> 2. Tests nuevos en tests/unit (un fichero nuevo, test_guardia_enlaces.py o el nombre que encaje con los de la guardia), que ROMPEN con el código de main y pasan con el de la rama, demostrado con la skill comparar-con-main:
>    - la imagen de Backtest marzo por un enlace simulado (forma b), negada;
>    - la misma imagen en una copia fuera del repo (forma c), negada;
>    - un libro de un mes no legible y un fichero de knowledge/cases/holdout/1/ en una copia fuera del repo, negados;
>    - la carpeta Backtest <mes no legible> como objetivo de Read, de Grep y de Glob, negada;
>    - una ruta fuera del repo sin ningún anclaje (un fichero cualquiera de una carpeta temporal), PERMITIDA, para que la regla no se pase de frenada;
>    - si la plataforma lo deja, un enlace real (os.symlink en Linux; en Windows, una unión si se puede crear sin permisos de administrador, y si no, se salta con su motivo).
>    Mutantes a mano como en GUARDIAS-HOLDOUT, restaurados por hash: quitar cada una de las tres formas de D1 tiene que romper al menos un test. Que ningún commit contenga un mutante.
> 3. Los tests de la guardia que ya existen, todos en verde. CLAUDE.md, en «Las guardias de Claude Code», una línea «Guardia:» que diga que las clases protegidas se deciden también por estructura fuera del repo y por la forma textual y la canónica.
> 4. Informe en docs/validation/GUARDIA-ENLACES.md: fase 0 con la tabla de 0.2, lo hecho, los mutantes, desviaciones, exposiciones («ninguna» si nada se abrió) y la PARADA final.
> 5. CI de Linux: push a fix/guardia-enlaces (RITUAL.md:102), con su número de run; solo se acepta el fallo de state check por el nombre fix/.
> 6. Revisor, con este alcance: comparar la guardia de la rama con la de main CASO A CASO en las clases de la familia 1, porque al reescribir una regla se pierden casos; y buscar una ruta protegida que siga pasando (otra forma de enlace, una mayúscula, una barra invertida, un prefijo \\?\, una unidad subst). Su informe, pegado al final.
>
> Contrato: rutas_permitidas = .claude/hooks/guardia.py, tests/unit/ (solo los ficheros de la guardia y el nuevo), CLAUDE.md, docs/validation/GUARDIA-ENLACES.md, docs/validation/anexos/GUARDIA-ENLACES/, docs/validation/HOLDOUT-EXPOSICIONES.md, docs/encargos/, docs/state/HISTORIA.md y PROJECT_STATE.md; lo de «Qué no cambia», en rutas_protegidas. Recuerda que en esta rama la guardia cambiada es código sin revisar: si niega un comando legítimo, no lo reescribas para esquivarla; si es un falso positivo, a la PARADA, y Aleks lo lanza con «!» tras revisarlo el consultor.
>
> Al terminar: «Rama lista para revisión, NO cerrada.»

## Respuesta del consultor a la PARADA final (2026-11-20)

Dada por Aleks (consultor) el 2026-11-20, por la noche, en un solo mensaje. Copiada tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA final de trabajo/guardia-enlaces (§8 de GUARDIA-ENLACES.md), 2026-11-20. Cópiala tal cual al informe, en una sección «Respuesta del consultor a la PARADA final». Si pasas de medianoche, la fila de HOLDOUT del 2026-11-21 va antes del primer make check de ese día. A las 09:00 de Lima del 21 no puede haber nada pesado corriendo (Aleks graba).
>
> 1. Las clases sin anclar: (a), se añaden en ESTA rama. Los tramos no citables (data/transcripciones/<vídeo con tramos>/), los ficheros con id de caso reservado en knowledge/cases/ y data/visor/, el feedback que etiqueta un caso reservado (knowledge/feedback/) y la lista de ficheros con ocultos, como anclajes con la misma regla de D1: se decide como si el anclaje estuviera en la raíz. Un test por clase, en una copia fuera del repo (negada), que rompa con el código de antes de este cambio. Por qué: es la misma condición que D1 («nombra la condición»), y dejarla a medias deja copias o clones fuera del repo sin proteger.
>
> 2. Glob sobre la carpeta Backtest: vuelve a pasar, como ls y Get-ChildItem. D2 queda solo para Read y Grep con la carpeta como objetivo. Por qué: listar nombres no es leer contenido, y ADR-0021 §1 lo permite; una prohibición que no sale de un ADR no se escribe (CLAUDE.md). Error del consultor, que irá a la fila del cierre. Ajusta el test y la línea de CLAUDE.md.
>
> 3. Apagar las capas nuevas en test_roto_a_proposito: sí, con una condición. Añade un test que, con TODAS las capas encendidas, compruebe que esas mismas rutas salen negadas, para que la combinación también quede cubierta. El cambio en tests existentes que D4 no previó es error del consultor y va a la fila del cierre.
>
> 4. El tope de 20.000 entradas, negando al pasarlo: se queda. Es negar por defecto, y lo impone el límite de 30 s del hook. Escríbelo en el informe, en la línea de CLAUDE.md y con su test (pasado el tope, se niega).
>
> 5 y 6. Los residuos que ya pasaban en main (enlaces encontrados al recorrer, enlaces duros, C:\ con un clon fuera del repo): residuo aceptado, sin rama propia por ahora. Van a la entrada G.1 de la hoja de ruta en el cierre, no a Technical Debt, porque PROJECT_STATE está en 24.776. Por qué: piden que alguien cree a propósito un enlace duro o un clon en la raíz de un disco, y la barrera sigue siendo el código.
>
> 7. G.8: de acuerdo. El código queda hecho con esta rama; la entrada pasa a HECHA solo cuando Aleks repita el traslado a D: y la guardia simulada niegue las cuatro rutas. Eso lo registra la orden de cierre de la rama siguiente.
>
> Lo que sigue: un commit con 1-4 y esta respuesta en el informe (make check sellado antes); push a fix/guardia-enlaces y CI de Linux con su número de run; revisor con alcance en lo nuevo (los anclajes añadidos, caso a caso contra el commit anterior, y el cambio de Glob); su informe pegado al final.
>
> Rama lista para revisión, NO cerrada.
