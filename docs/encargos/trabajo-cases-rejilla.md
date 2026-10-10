# Encargo · trabajo/cases-rejilla

Dado por Aleks (consultor) el 2026-10-10. Copiado tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Rama nueva: trabajo/cases-rejilla, desde main en 26326b2 (commit de estado sobre el merge 0b1c8ef, tag stable/F37i-demo-ejecucion-1). Antes de abrirla, verifica con git que main está en 26326b2, que el tag apunta a 0b1c8ef y que no hay otra rama abierta; si algo no cuadra, para y dímelo. Ábrela con la skill abrir-rama: este prompt tal cual en docs/encargos/trabajo-cases-rejilla.md, su contrato.yaml y el archivo en HISTORIA del PROJECT_STATE.md de main.
>
> Objetivo: puntos W y Z de la Next Action. cases/ (kit, fidelidad, ingesta y hoja) cuenta la ventana de cada caso por la rejilla H4 de ADR-0069, por la misma puerta que ya usa el motor (engine/relojes.py), y no en huso_operativa. Así la ventana congelada de los días de desfase sale a la hora a la que opera el trader (ACTIVACION-A42.md §3.6, §5.3 y §6.2; recuadro de corrección del paso b de docs/runbooks/ENTRADA-MARZO.md).
> Día de desfase, en todo este encargo: un día en que solo uno de los dos, EE. UU. (el huso del ancla de anclaje_h4) o Europa (Europe/Madrid), ha cambiado ya la hora, en primavera o en otoño. Se calcula con zoneinfo a partir de esa condición, nunca con una lista de fechas.
> NO cambia: el motor ni su puerta (salvo exponer lo que cases/ necesite, sin cambiar su comportamiento), spec, knowledge, parámetros, el día de riesgo (huso_operativa, ADR-0063), scripts/ticks_spread.py (eso es X, no esta rama), ni ningún fichero ya congelado (ventanas.yaml de sorteos hechos, kits, autorizaciones, preregistro). Marzo no se abre, no se lista, no se sortea y no se ingiere en esta rama. Nadie ejecuta uv run botsito motor arnes (solo se ejecuta para medir según ADR-0070, y aquí no hace falta).
>
> Holdout, antes de nada (CLAUDE.md, «Que se puede mirar y que no»):
> - Nunca se lista una carpeta que contenga meses reservados; cada fichero se nombra por su ruta literal (lección de trabajo/reloj-invierno y de activacion-a42).
> - Los tests usan fechas sintéticas o semanas de 2024 o 2025. Las dos de ACTIVACION-A42.md §4 valen: la del 27 al 31 de octubre de 2024 es de desfase; la del 3 al 7 de noviembre de 2024 es la de control, fuera de desfase. Nunca días de 2026 de meses reservados. Ningún texto commiteado lleva fechas de días reservados.
> - kit build y kit check declaran por recuento los días reservados cuyas velas leen (ADR-0033); toda exposición se declara el mismo día en HOLDOUT-EXPOSICIONES.md.
>
> FASE 0, inventario sin tocar código, con entrega y PARADA antes de escribir código:
> a) Cada sitio de cases/ (ventanas.py, ingesta.py, fidelidad.py, paquete.py, hoja_docx.py y el kit) que convierte una hora nominal en un instante, o al revés, con huso_operativa o ventana_local: fichero:línea y qué calcula. Incluye lo que la hoja le dice al trader en texto (las horas del gráfico que verá) y la asignación de cada operación a su sesión en la ingesta.
> b) Lo que la puerta de engine/relojes.py ya ofrece (de (día, hora nominal) a instante UTC y al revés, para los tres selectores) y si cases/ puede llamarla tal cual. Si hace falta tocar la puerta, dilo y por qué, sin cambiar su comportamiento para el motor.
> c) Qué ficheros congelados existen hoy con ventanas (ventanas.yaml, kits u otros) y si alguno contiene un día de desfase. Mídelo por recuento y por la condición de arriba, sin leer etiquetas ni precios y sin abrir nada de holdout/: solo las fechas que la puerta de ADR-0033 deje ver sin abrir; si eso exige abrir, dilo y para. Si alguno contiene un día de desfase, PARADA: no se recalcula nada congelado sin decisión del consultor.
> d) El formato de lo congelado: qué congela hoy ventanas.yaml (el bloque config con huso_operativa, la ventana de cada caso) y qué congelaría con la rejilla. Si cambia el esquema, cómo siguen leyéndose y comprobándose (kit check, fidelidad check) los artefactos ya congelados sin cambiar un byte. Propón lo mínimo.
> e) Las guardias de la puerta (cada límite de sesión es un límite de la rejilla; un día de rejilla con vela irregular no es operable): qué hace cases/ con un día no operable. Propón el comportamiento, negando por defecto: un día que la puerta no puede decidir no entra en el universo ni se sortea, con un mensaje que lo nombra. Mide además si algún día laborable real (lunes a viernes) cae en un día de rejilla con vela irregular, o si eso solo pasa en domingo. Si nunca le pasa a un día laborable, dilo: el test de esa guardia la fuerza con un ancla o una configuración sintética, no con un día que nunca sale.
> f) Tu propuesta de tests y del criterio de regresión (abajo), con su mecánica medida: un git worktree no trae data/ (está fuera de git) y kit build no sobreescribe. Di cómo leen las velas el clon de main y el de la rama sin copiarlas a otro sitio del repo y sin volver a descargar nada (pendiente heredado 9), y dónde escribe cada build para no pisar nada.
> Entrega la fase 0 en el informe y PARA.
>
> FASE 1 (tras mi respuesta a la PARADA):
> - cases/ calcula toda ventana por la puerta. Un solo camino: ningún sitio de cases/ convierte horas con huso_operativa para la ventana del caso (test que lo busque y falle si aparece otro).
> - Tests que rompen a propósito: un día de desfase de 2024 o 2025 donde la ventana por la rejilla sale una hora antes que en huso_operativa (el test falla con el código de main); un día de rejilla con vela H4 irregular, que no entra en el universo (forzado como diga e); y un día de la semana de control, idéntico al de main.
> - Criterio de regresión: en enero, abril y agosto de 2026 (construcción, sin días de desfase; compruébalo con casos_reservados y con la condición del desfase antes de usarlos) kit build, kit check y las ventanas calculadas salen idénticos byte a byte a los de main. Compáralo por hash, con la salida de main y la de la rama en dos clones desechables (git worktree add en un directorio temporal), con la mecánica de f.
> - Z: corrige el párrafo de CLAUDE.md «Marzo de 2026 esta RECIBIDO y SIN ABRIR». Ya no espera a A-42; espera a esta rama (W) y a lo que mida que sigue pendiente en ENTRADA-MARZO.md (paso 0, paso a con la columna de fechas por el consultor, PARADA B0). Mide antes qué dice hoy ENTRADA-MARZO y escribe solo lo que sostiene. Si con esta rama la PARADA B0 deja de tener motivo, añade en ENTRADA-MARZO un recuadro de corrección con fecha y rama, sin tocar el cuerpo.
>
> Cierre de la rama:
> - make check > make-check.log 2>&1, con el exit 0, ningún failed y la línea SELLO, antes de cada commit.
> - La rama toca código dependiente del reloj y de la plataforma (zoneinfo): empújala como fix/cases-rejilla (el nombre, como dice RITUAL.md) y pasa la CI de Linux. El único fallo aceptado es el de state check por el nombre fix/. Dame los números de run.
> - Informe en docs/validation/CASES-REJILLA.md, con la fase 0, la PARADA y mi respuesta tal cual, las fases, la comparación de regresión con sus hashes, las exposiciones declaradas (o «ninguna») y su estado al final.
> - Pasa el revisor (subagente revisor), con este alcance: un solo camino de cálculo, ningún fichero congelado cambiado, el holdout (nada listado ni abierto, ninguna fecha reservada en textos ni tests) y que los tests fallen con el código de main. Pega su informe al final del tuyo.
>
> Nota del consultor para la orden de cierre (no es trabajo de esta rama; queda aquí escrita con fecha 2026-10-10):
> - O: Aleks envió el 2026-10-09 a FTMO la pregunta P-D1 con un punto 3 añadido: si la cuenta 2-Step Swing real es hedging, si el volumen máximo en EURUSD es de 50 o 100 lotes y si hay tope de volumen sumado entre varias órdenes. La respuesta se registra parafraseada (RESPUESTAS-FTMO) y decide el pendiente 37: recortar a 50, partir en varias órdenes o no operar. En el commit del contrato, la entrada O se reescribe con esto.
> - A: la prueba gratuita actual vence hacia el 2026-10-22; la ejecución 2 va en la prueba nueva del 26 de octubre, como ya dice A.
>
> Rama lista para revisión, NO cerrada.
