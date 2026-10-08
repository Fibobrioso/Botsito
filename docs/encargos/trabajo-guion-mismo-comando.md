# Encargo · trabajo/guion-mismo-comando

Dado por Aleks (consultor) el 2026-10-07. Copiado tal cual (incluye las dos decisiones que el encargo registra, con su fecha, en «DECISIONES QUE ESTE ENCARGO REGISTRA»):

> Modelo: Opus · Esfuerzo: alto
>
> Rama nueva: trabajo/guion-mismo-comando (punto V de la Next Action). Antes de abrirla, comprueba y dime: el sha de main (en la captura del cierre anterior, cbfe4e4…), que stable/F37f-umbral-mayo apunta al merge 9a313e0 y que la última CI de main sobre ese sha terminó en completed/success (consúltala con el sha de 40 caracteres escrito tal cual). Si algo no cuadra, para y dímelo. Si cuadra, abre la rama desde main con la skill abrir-rama: encargo en docs/encargos/, contrato.yaml y PROJECT_STATE de main archivado en HISTORIA.
>
> OBJETIVO. Cerrar el hueco de RELOJ-INVIERNO.md §4.5 en su forma general. La guardia (.claude/hooks/guardia.py) solo deja ejecutar un guion (un fichero que ejecuta un intérprete, un shell o pytest) si lo que se ejecuta es seguro que es lo que ella leyó al inspeccionar el comando. Si no puede garantizarlo, NIEGA. La condición se escribe así, negando por defecto, y no como lista de casos.
>
> LO QUE NO CAMBIA: motor, spec, knowledge/, cifras, criterio_fidelidad.yaml, CLAUDE.md (salvo que la fase 0 demuestre que hace falta, y entonces me lo propones primero). Nadie ejecuta uv run botsito motor arnes en esta rama, ni siquiera con --help (ADR-0070). No se abre ningún material protegido: todos los tests usan rutas sintéticas, como hacen hoy los de la guardia.
>
> FASE 0, INVENTARIO SIN TOCAR NADA, Y PARADA. Entrega antes de escribir código:
> a) Todas las vías por las que la guardia decide sobre un fichero que luego se EJECUTA: _exigir_guion (shells e intérpretes, también tras uv run), _analizar_pytest (fuera de tests/), make, PowerShell (analizar_powershell, ¿mira siquiera un python x.py dentro de pwsh -c?) y cualquier otra que encuentres. De cada vía, la línea de código y qué hace hoy si el fichero no existe o no se puede leer.
> b) Mide cada hueco con un comando sintético que NO toque material protegido; vale con un test que llame a decidir() sobre un texto de comando. Como mínimo:
>    1. cp a.py b.py && uv run python b.py, con b.py inexistente al inspeccionar;
>    2. el mismo patrón sobre un guion IDÉNTICO al de main (cp otro.py scripts/<uno de main>.py && uv run python scripts/<ese>.py);
>    3. cat > x.py <<'EOF' … EOF && python x.py;
>    4. python x.py $(cp a.py x.py), es decir, una sustitución que corre antes;
>    5. algo que escribe el guion en paralelo (… & python x.py, y tee x.py en una tubería);
>    6. pytest sobre un fichero fuera de tests/ que aún no existe.
>    Di cuáles pasan hoy y cuáles no.
> c) Lo que la regla NO cubre y declaras como límite: por ejemplo, un proceso en segundo plano lanzado en una llamada ANTERIOR, o módulos locales que el guion importa y la guardia no lee. Para cada uno, si cabe en esta rama o si propones dejarlo como entrada nueva de la Next Action.
> d) Tu propuesta de la lista cerrada de lo que puede ir antes de la ejecución, o a la vez, en el mismo comando. Mi punto de partida: antes, solo cd, asignaciones literales, export con valor literal y set -e/-u/-o pipefail; después de la ejecución en la misma tubería, solo filtros que leen de stdin sin redirección de salida (head, tail, grep, wc, sort, uniq, cut). Además: ninguna sustitución $(…) ni `…` en el mismo comando, y ninguna redirección de salida hacia el propio guion. Si propones añadir algo, cada añadido con su porqué y el comando real que lo necesita.
> PARADA: no escribas código hasta que te responda.
>
> FASE 1, TRAS MI RESPUESTA:
> - Una sola función con nombre propio, la que decide que la ejecución es verificable, llamada desde TODAS las vías del inventario. No se arregla vía por vía.
> - Un guion que no existe o no se puede leer → se niega, con un mensaje que diga cómo reescribirlo: el guion con la herramienta Write, y su ejecución en otra llamada.
> - Tests que rompen la guardia a propósito, uno por cada caso de b) y de la lista cerrada (lo admitido pasa; lo de fuera de la lista se niega, incluido un programa inventado).
> - Un anexo de mutaciones, como docs/validation/anexos/UMBRAL-MAYO/sin_d2.py, que demuestre que esos tests fallan si se quita la condición.
> - Compara caso a caso con la guardia de main: todos los tests de la guardia que ya existen siguen pasando, y no se pierde ningún caso que hoy se bloquea.
>
> CI DE LINUX: la rama toca .claude/. Empuja como fix/trabajo-guion-mismo-comando y dame el número de run. El único fallo aceptado es el de state check por el nombre fix/.
>
> DECISIONES QUE ESTE ENCARGO REGISTRA (cópialas tal cual en docs/encargos/, con su fecha):
> 1. Decisión de Aleks del 2026-10-07 (punto 5): el repo Fibobrioso/Botsito sigue público. Está en el plan Free: pasarlo a privado quitaría la protección de main, y lo ya publicado no se borra. Las respuestas de FTMO se siguen registrando parafraseadas, no literales. Los literales ya commiteados (RESPUESTAS-FTMO.md §0.e) no se tocan. Comprueba que la Next Action no tiene ninguna entrada sobre este punto; si la tuviera, sale como HECHA en el commit del contrato del cierre.
> 2. Demo de FTMO (punto A), registrado por el consultor el 2026-10-07:
>    a) Respuesta de soporte de FTMO del 2026-10-07, parafraseada: el acceso de Aleks al área de cliente queda reactivado con un único registro; los demás registros se desactivaron; la norma de FTMO (cláusula 4.2 de sus condiciones generales) no permite más de un registro por persona. Con esto, la incidencia que bloqueaba crear la prueba queda resuelta. En el repo no entra ningún correo ni ningún nombre.
>    b) Dato comprobado en ftmo.com/en/ftmo-free-trial: la prueba gratuita dura 14 días, cada trader puede tener solo una a la vez, y se puede borrar y crear otra. Toda prueba nueva se crea desde el mismo registro, nunca con otro.
>    c) Plan: la ejecución 1 de MedirDemoFTMO, con una prueba nueva, antes del 25 de octubre; las ejecuciones 2 (del 26 al 30 de octubre) y 3 (2 o 3 de noviembre), con una segunda prueba creada el 26, para que el reloj del servidor de A-28 se compare en la misma cuenta. Aleks apunta el nombre del servidor en cada ejecución.
> Estas dos solo se registran en el encargo: no cambian código ni runbooks en esta rama.
>
> INFORME en docs/validation/GUION-MISMO-COMANDO.md: el encargo frente a lo hecho, punto por punto con su evidencia; las desviaciones; los comandos y sus salidas; los límites declarados; y la comparación caso a caso con main. Después, el revisor (subagente revisor), con su informe pegado al final. Pídele expresamente que compruebe si la condición está enumerada o niega por defecto (lección de trabajo/umbral-mayo).
>
> Rama lista para revisión, NO cerrada.
