# Encargo · trabajo/guardias-holdout

Dado por Aleks (consultor) el 2026-11-19, por la noche, en un solo mensaje. Copiado tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Encargo del consultor (2026-11-19, noche) · trabajo/guardias-holdout · carril de guardias de la hoja de ruta · rama para dejar trabajando de noche
>
> Rama nueva: trabajo/guardias-holdout, desde main (fa592071, commit de estado sobre el merge 2fc884ac del tag stable/F39g-preregistro). Ábrela con la skill abrir-rama: base comprobada con git y la CI de main sobre fa592071 comprobada con un gh run view suelto (debería ser el run 44653987599, verde; dime si no lo es). Contrato con riesgo alto, tramo "Carril: guardias y deuda" (tal cual, como en docs/encargos/trabajo-guardia-falsos-positivos.md) y artefacto docs/validation/GUARDIAS-HOLDOUT.md. Es lista blanca: CLAUDE.md, scripts/ y tests/unit/ que toques van en rutas_permitidas, y si alguna está protegida, sale de rutas_protegidas en el mismo commit (lo protegido manda). Tag previsto: stable/F39h-guardias-holdout (comprueba en origin que no existe). Rama de laptop. Mandan las skills abrir-rama, fase-cero y entregar-rama; si este encargo y ellas chocan, ganan ellas y lo dices. No se usan herramientas de NotebookLM. Ningún ADR nuevo.
>
> LA PARADA ES CONDICIONAL: Aleks la deja corriendo de noche. Las decisiones van por adelantado, abajo. Sigues con todo lo que cuadre con lo que midas; donde lo medido contradiga una decisión, apartas solo esa pieza, la dejas descrita en una PARADA final con la alternativa que ves, y sigues con lo demás. Nunca cierras. Nunca eliges «no volver a preguntar». Si te frena la guardia de Claude Code o un permiso, no la rodeas: apartas esa pieza y sigues.
>
> EL MAKEFILE NO SE TOCA. Si una pieza solo se puede hacer cambiándolo, va a la PARADA final y no se hace.
>
> LA MEDIANOCHE. Si un make check va a empezar en un día sin fila de HOLDOUT-EXPOSICIONES de esta rama, escribe antes la fila de ese día (qué leerá: el M1 de marzo y de junio para calentar, como todos los make check, más lo que toque), estadíala y sigue.
>
> OBJETIVO
> Tres piezas del carril de guardias que se han roto a mano: (G2) que make check no selle en una rama trabajo/* sin la fila de HOLDOUT-EXPOSICIONES del día (Technical Debt, PROJECT_STATE.md:102, propuesta en CUENTA-POR-MES.md); (H) dos huecos de test_hoja_de_ruta; y (G1) el ESTUDIO, sin implementar, de una guardia contra fechas de días reservados en lo que añade una rama.
>
> QUÉ NO CAMBIA
> - src/botsito/, knowledge/, el motor, la spec, ninguna cifra, ningún ADR, el Makefile, docs/plan/HOJA-DE-RUTA.md (va en el cierre).
> - Nada de lo reservado se abre ni se imprime. Ningún mensaje, log, assert de pytest, fichero commiteado ni salida de terminal lleva una fecha de un día reservado. Los recuentos de G1 se dan por CLASE o por CARPETA de primer o segundo nivel, nunca por nombre de fichero: un nombre de fichero puede llevar una fecha (ids, carpetas de sesión).
> - knowledge/cases/holdout/ queda fuera de todo git show, git diff o git log -p que lances (la guarda de pytest no ve los subprocesos): usa una pathspec que la excluya.
> - La fila de HOLDOUT del día, antes del primer make check.
>
> F0 · FASE 0 (inventario; PARADA condicional: sigues tú)
> 0.1 Herencias: en Technical Debt, en «Carril: guardias y deuda» de la hoja de ruta, en CUENTA-POR-MES.md y en ERRORES-RECURRENTES.md, todo lo que pida estas piezas. Tabla con fichero y línea.
> 0.2 Dónde vive G2 sin tocar el Makefile. scripts/contrato_rama.py corre el primero en make check y ya actúa también en la CI (fix/<rama> trae contrato.yaml y _sin_prefijo iguala fix/x con trabajo/x), y sus 16 tests de tests/unit/test_contrato_rama.py corren en trabajo/prueba sin fila. Decisión: G2 en una función aparte, llamada desde contrato_rama.py SOLO si la rama local empieza por «trabajo/» (un startswith explícito, no _sin_prefijo); en la CI, en main y en fix/ no actúa. La función recibe el día y el texto por parámetro. Si llamarla desde comprobar() rompe los 16 tests, llámala desde main() o dale a los tests una fila; elige lo que menos toque y dilo. Si va en un módulo nuevo, añádelo a la línea de mypy --strict solo si eso no exige tocar el Makefile; si lo exige, la función vive en el propio contrato_rama.py.
> 0.3 La guardia de Claude Code: comprueba leyendo .claude/hooks/guardia.py que editar contrato_rama.py y lanzar make check no se bloquean, y que el «uv run python scripts/contrato_rama.py» del paso 6 de abrir-rama tampoco, con el código nuevo (no debe recorrer directorios y nombrar algo sensible a la vez). Si lo bloqueara, el diseño se ajusta para no recorrer directorios: G2 solo lee un fichero, HOLDOUT-EXPOSICIONES.md, del índice de git.
> 0.4 Las filas: la forma de HOLDOUT-EXPOSICIONES.md (columna Fecha AAAA-MM-DD, la tabla no está al final del fichero, las filas de noviembre nombran la rama) y el reloj (el día local de la laptop, Lima).
>
> G2 · NO SE SELLA SIN LA FILA DEL DÍA
> - Pasa si docs/validation/HOLDOUT-EXPOSICIONES.md TAL COMO ESTÁ ESTADIADO (git show :ruta) tiene al menos una fila de la tabla cuya primera columna es el día de hoy (reloj local) y que nombra la rama («trabajo/<nombre>»).
> - Al fallar: «G2: falta la fila de HOLDOUT-EXPOSICIONES del <hoy> para trabajo/<rama>; escríbela y estadíala antes de este make check (ADR-0021 §4)».
> - Tests que rompen, con texto y día inyectados: sin fila; fila de ayer; fila de hoy de otra rama; fila de hoy solo sin estadiar; fila buena; rama fix/x y main (no actúa).
> - CLAUDE.md: una línea «Guardia:» en la regla de exposiciones (la frase «Toda exposicion se declara … el mismo dia»), en el mismo commit.
>
> H · DOS HUECOS DE test_hoja_de_ruta (buzón del consultor, 2026-11-08)
> - (c) no reconoce «Depende de» ni «después,» sin «de» como dependencia; (b) su conjunto de letras HECHAS no ve que falte el registro de una letra reutilizada.
> - Decisión: arréglalos SOLO si, con la detección nueva, la hoja de ruta y PROJECT_STATE.md de main siguen pasando. Si la detección nueva encuentra problemas reales en la hoja de hoy, no la cambies (la hoja se toca en el cierre): apártalo a la PARADA final con la lista de lo que encontró.
> - Tests sintéticos que rompen en cada caso nuevo.
>
> G1 · ESTUDIO, SIN IMPLEMENTAR: FECHAS DE DÍAS RESERVADOS EN LO QUE AÑADE UNA RAMA
> No escribas la guardia. Lo que te pido es la medida que permita decidirla. El problema que ya se ve: los días reservados de septiembre coinciden con fechas de trabajo del proyecto, que viven legítimamente en ids de evidencia y feedback (ev-…, fb-…, …-sesion-…), en trailers Fuente:, en uv.lock y en los ficheros de asignación del holdout. Una guardia ingenua que mire toda la historia de la rama la dejaría sin poder sellar.
> - Con un guion commiteado en anexos/GUARDIAS-HOLDOUT/ que use la función de la compuerta que da los días ocultos sin imprimirlos, mide sobre las líneas AÑADIDAS por los commits de las ramas cerradas desde stable/F39a-guardia-falsos-positivos (y sus mensajes de commit), excluyendo knowledge/cases/holdout/: cuántas contienen como AAAA-MM-DD un día oculto, por CLASE (dentro de un id ev-/fb-/sesion; en un trailer Fuente:; en uv.lock; en un fichero de asignación del holdout; en un fichero de docs/state/; en prosa de docs/; en código o tests; otra). Solo recuentos. Declara la lectura en la fila de HOLDOUT antes de lanzarlo.
> - Con eso, en el informe: qué condición separaría una fuga (una fecha dicha como día de mercado reservado) de una fecha de trabajo, cuántos falsos positivos y cuántas fugas reales habría dado cada variante sobre esa historia, y tu propuesta (o que no es viable). Si la fase 0 del propio guion choca con la guardia, apártalo a la PARADA y dilo.
>
> INFORME, CI Y REVISOR
> docs/validation/GUARDIAS-HOLDOUT.md: la fase 0, lo hecho punto por punto, las desviaciones, los límites declarados (el reloj de G2) y la PARADA final con lo apartado. Push a fix/guardias-holdout y CI de Linux (obligatoria: toca git y fechas); el único fallo aceptado es el de state check por el nombre fix/; comprueba ahí que G2 no actúa en fix/. Revisor sobre la rama entera, con estos alcances además de los suyos: (1) que nada de lo commiteado ni de lo impreso lleve una fecha reservada ni un nombre de fichero que la delate; (2) que G2 no actúe fuera de trabajo/* ni en la CI; (3) que G2 lea lo estadiado y no el árbol de trabajo; (4) que H no deje la hoja de ruta de main en rojo. PROJECT_STATE.md por debajo de 25.000 bytes (hoy 24.528); prepara para el cierre, sin tocarla, la línea de Technical Debt que G2 paga y una línea nueva para G1 con lo que salga del estudio. Dame el número del run, el sha del último commit y el número de commits.
>
> Rama lista para revisión, NO cerrada.

## Respuesta del consultor a la PARADA final (2026-11-20)

Dada por Aleks (consultor) el 2026-11-20, en un solo mensaje. Copiada tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA final de trabajo/guardias-holdout (§9 de GUARDIAS-HOLDOUT.md), 2026-11-20. Cópiala tal cual al informe, en una sección «Respuesta del consultor a la PARADA final».
>
> Antes de nada: hoy es 2026-11-20 en el reloj de la laptop. La fila de HOLDOUT-EXPOSICIONES de hoy, que nombre trabajo/guardias-holdout, se escribe y se estadía antes del primer make check. G2 ya la exige en esta rama.
>
> 0. La fuga del rango y los 32 ids heredados: (a), pero NO en esta rama. Va a una rama propia del carril «guardias y deuda», después de la ingesta y la activación de la 7b; no adelanta el camino crítico. Sus condiciones, para el cierre y para su encargo:
>    - Se localizan con la puerta y en memoria, sin imprimir ids, fechas ni líneas.
>    - En tests/unit y tests/contract se sustituyen por ids sintéticos, o por ids calculados desde la puerta al ejecutarse, sin escribirlos.
>    - Los informes CERRADOS de docs/validation no se reescriben, porque el régimen es el recuadro con el cuerpo intacto. Su fase 0 dice cuántos de los 9 están en informes cerrados, y el consultor decide si un recuadro sin el id sirve o se declaran sin más.
>    - Si alguno «quema», su fase 0 lo propone con ADR-0021 §5 y ADR-0041, y lo decide el consultor en su PARADA.
>    - El AVISO de knowledge validate de §6 entra en esa rama como pregunta, porque toca src/.
>    - Por qué no aquí: ya está en main, no hay exposición nueva y esta rama no puede tocar tests/contract ni src/.
>
> 1. G2 en el cierre: (a). G2 actúa en todo make check de trabajo/*, también en el del chore(cierre).
>    - Como el commit chore(cierre) solo admite contrato, HISTORIA, ERRORES-RECURRENTES, PROJECT_STATE y HOJA-DE-RUTA (la puerta de RITUAL.md enumera esos ficheros), la fila del día del cierre va ANTES, en un commit propio de la rama, sellado: «docs(<rama>): la fila de HOLDOUT del <día>, antes de los make check del cierre». Es lo que hizo trabajo/sesion-07 en f663aa2. Si la fila del día ya está, ese commit no hace falta.
>    - Por qué: el make check del cierre lee lo mismo que los demás, y ADR-0021 §4 no distingue.
>
> 2. abrir-rama, entregar-rama y los runbooks: (a), en esta rama.
>    - Se amplía contrato.yaml con rutas_permitidas: .claude/skills/abrir-rama/SKILL.md, .claude/skills/entregar-rama/SKILL.md, docs/runbooks/CONTRATO-DE-RAMA.md y docs/runbooks/RITUAL.md. También .claude/skills/cerrar-rama/SKILL.md, SOLO si su recorrido necesita nombrar el commit de la fila del punto 1; si con RITUAL.md basta, no se toca y se dice. Verifica que ninguna esté en rutas_protegidas; si alguna está, sale de ahí.
>    - Qué se escribe:
>      - abrir-rama: la fila del día, que nombre la rama, y el artefacto, estadiados ANTES del paso 6, porque desde G2 el guion del paso 6 falla sin ella. Se reordena el texto del paso 7, que hoy la pone después.
>      - entregar-rama, paso 2: el guion en verde exige también la fila del día.
>      - CONTRATO-DE-RAMA.md, «Que comprueba make check, y que no»: G2, con su mensaje y dónde no actúa.
>      - RITUAL.md: lo del punto 1, en su sitio, antes del bloque del chore(cierre), con su puerta.
>    - Solo documentación: nada de código ni de tests nuevos. Pero comprueba con un make check que test_hoja_de_ruta y los tests de skills (si hay alguno que lea esas skills) siguen en verde.
>
> 3. La guardia de fechas: (a). V2 en su propia rama, después de la del punto 0 y con sus tres condiciones de §4.3. Para el cierre, la línea de Technical Debt que entra es esta (ajústala solo si pasa de 400 bytes o el tope de PROJECT_STATE lo pide):
>    «Sin guardia contra fechas de días ocultos en lo que añade una rama. En main hay 32 ids exactos de casos ocultos fuera de knowledge/cases, uno de ellos de F39a-F39g en tests/unit. Primero, una rama que los sustituya en tests sin abrirlos (los informes cerrados, por recuadro o declarados); después, la variante estrecha V2 (GUARDIAS-HOLDOUT.md §4.3 y §9).»
>    Salen las dos líneas de §10.
>
> 4. La comprobación del contrato: (a). Vale el make check: es el mismo guion y el mismo comando.
>
> 5. El guion de G1: (a), ratificado. Seguiste la forma literal que propone el propio mensaje de la guardia, y la permite DECISIONES-DE-PROCESO (2026-10-21, punto 1): lo que la guardia leyó es lo que se ejecutó, y eso no es rodearla. La cláusula «apártalo a la PARADA» del encargo era más estricta que esa regla, y es un error del consultor, que irá a la fila del cierre.
>
> 6. Las fechas en la historia de la rama: (a). Se aceptan en la historia de main con el merge de siempre, declaradas aquí y en HOLDOUT-EXPOSICIONES. No se reescribe nada.
>
> 7. Los mutantes a mano: (a). Editar el fichero real, pasar la suite normal y restaurar por hash no rodea la guardia: la guardia negaba cargar código sin revisar por otra vía, y el mutante pasa por la vía normal. Una condición: comprueba y escribe en el informe que ningún commit de la rama contiene un mutante, es decir, que contrato_rama.py solo tiene la versión final en aff916c8 y 72ebedfa (git log -p sobre ese fichero, sin imprimir nada fuera de él).
>
> Lo que sigue: commit con la fila de hoy, los cambios del punto 2 y esta respuesta en el informe (make check sellado antes, como siempre); push a fix/guardias-holdout y CI de Linux con su número de run; revisor con alcance en lo nuevo (las skills y los runbooks frente a G2 y al RITUAL, caso a caso); su informe pegado al final. PROJECT_STATE no se toca más allá de lo que ya lleva la rama; las líneas de §10 entran en el cierre.
>
> Rama lista para revisión, NO cerrada.
