# Decisiones de arquitectura (ADR)

Una decision por fichero, `NNNN-titulo.md`, con el formato de `0000-template.md`. Estado `ACTIVE` o
`SUPERSEDED` (con enlace a la que la sustituye). Un ADR nunca se borra.

| ADR | Titulo | Estado |
|---|---|---|
| 0001 | Estructura del repositorio y regimenes de cambio | ACTIVE |
| 0002 | Registro de parametros: una sola puerta, tipos no intercambiables, lectura estricta | ACTIVE |
| 0003 | Hooks copiados desde scripts/git-hooks; sin framework pre-commit | ACTIVE |
| 0004 | Categorias de parametro y horas con huso | ACTIVE |
| 0005 | Datos de mercado: fuente publica, precios enteros en puntos, tres relojes y anclaje | ACTIVE (con enmienda REVOCADA por ADR-0017) |
| 0006 | Capas revisadas, paquete `comun` y accesores del registro por tipo declarado | ACTIVE |
| 0007 | Transcripcion en dos capas: cruda inmutable por muestras, corregida por glosario | ACTIVE |
| 0008 | Fotogramas: cobertura completa a 1 fps sin perdida, regla de seleccion por `pts` y manifiesto inmutable | ACTIVE |
| 0009 | Verificacion mecanica de citas y propuestas de evidencia trazables | ACTIVE |
| 0010 | Busqueda de desarrollo: capa `retrieval`, indice en memoria, lexica y con fuente | ACTIVE |
| 0011 | Kit de elicitacion: ambiguedades legibles por maquina, registro pre-poblado, ventanas no vistas con particiones commiteadas antes y kappa desde el feedback | ACTIVE (el esquema de ambiguedades gana el estado DECIDIDA en ADR-0022) |
| 0012 | El registro despues de la sesion 1: tipos nuevos, ausencia de valor, categorias y el reloj del trader | ACTIVE (punto 5 revertido por ADR-0017) |
| 0013 | StrategySpec: reglas que nombran parametros y nunca los contienen, y un hash que cubre lo que el bot hace | ACTIVE |
| 0014 | La base sobre la que se mide el objetivo: `base_calculo_objetivo` | ACTIVE (enmendado por ADR-0020; con nota del 2026-09-16: sus dos premisas estan revocadas y la base queda para el consultor) |
| 0015 | Los relojes tras la auditoria: el del grafico es un default, y el dia de riesgo necesita el suyo | ACTIVE (enmendado por ADR-0017, ADR-0020 y ADR-0027) |
| 0016 | De donde sale cada regla: el campo `decision`, y un hash que cubre lo que un humano lee | ACTIVE (con nota del 2026-09-11) |
| 0017 | El reloj del trader es su reloj civil: se revierte ADR-0012 y se confirma ADR-0005 | ACTIVE |
| 0018 | La precedencia va por clase, no por orden del fichero; y los siete defectos que eso destapo | ACTIVE (con nota del 2026-09-11: A-20 cerrada) |
| 0019 | La forma ejecutable de una regla: predicados con argumentos, ligadura, y cuatro cosas con nombre (cinco desde F12: nace `efectos`) | ACTIVE |
| 0020 | La base del lotaje es la distancia hasta el stop, no la caja completa | ACTIVE |
| 0021 | Que cuenta como abrir un holdout, y que se hace con la exposicion de mayo | ACTIVE |
| 0022 | El bot no opera noticias en la cuenta fondeada, y una ambiguedad puede cerrarse por decision | ACTIVE (con enmienda del 2026-09-14: con FTMO Swing el bot si opera noticias) |
| 0023 | El registro de feedback sabe cuando llego cada respuesta y por donde (`recibido_el`, `procedencia`) | ACTIVE |
| 0024 | La ventana no se amplia a Nueva York (A-15), y la referencia para medir es Dukascopy (A-23; A-16 se parte y conserva la medicion) | ACTIVE |
| 0025 | El reparto de mayo no se toca: 6 dias dev y 13 de holdout (6/4/3), y junio sale del universo de F14 | ACTIVE |
| 0026 | La prop firm es FTMO, reto 2-Step, tipo de cuenta Swing | ACTIVE |
| 0027 | Los relojes con FTMO: el dia de riesgo es el dia civil del trader | ACTIVE |
| 0028 | El reloj del motor: tres fases, y el riesgo va por tick | ACTIVE (con nota del 2026-09-16: el punto 5 aplicado y el 4 precisado por ADR-0032) |
| 0029 | Lado del precio y redondeo de niveles | ACTIVE |
| 0030 | El motor interpreta la `forma`; las primitivas se escriben a mano | ACTIVE |
| 0031 | El freno de la firma dispara antes del limite: margen declarado y lectura prospectiva | ACTIVE |
| 0032 | De donde sale cada hecho y cada evento, y como nace la orden limite | ACTIVE |
