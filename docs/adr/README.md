# Decisiones de arquitectura (ADR)

Una decision por fichero, `NNNN-titulo.md`, con el formato de `0000-template.md`. Estado `ACTIVE` o
`SUPERSEDED` (con enlace a la que la sustituye). Un ADR nunca se borra.

| ADR | Titulo | Estado |
|---|---|---|
| 0001 | Estructura del repositorio y regimenes de cambio | ACTIVE |
| 0002 | Registro de parametros: una sola puerta, tipos no intercambiables, lectura estricta | ACTIVE |
| 0003 | Hooks copiados desde scripts/git-hooks; sin framework pre-commit | ACTIVE |
| 0004 | Categorias de parametro y horas con huso | ACTIVE |
| 0005 | Datos de mercado: fuente publica, precios enteros en puntos, tres relojes y anclaje | ACTIVE |
| 0006 | Capas revisadas, paquete `comun` y accesores del registro por tipo declarado | ACTIVE |
| 0007 | Transcripcion en dos capas: cruda inmutable por muestras, corregida por glosario | ACTIVE |
| 0008 | Fotogramas: cobertura completa a 1 fps sin perdida, regla de seleccion por `pts` y manifiesto inmutable | ACTIVE |
| 0009 | Verificacion mecanica de citas y propuestas de evidencia trazables | ACTIVE |
| 0010 | Busqueda de desarrollo: capa `retrieval`, indice en memoria, lexica y con fuente | ACTIVE |
| 0011 | Kit de elicitacion: ambiguedades legibles por maquina, registro pre-poblado, ventanas no vistas con particiones commiteadas antes y kappa desde el feedback | ACTIVE |
| 0012 | El registro despues de la sesion 1: tipos nuevos, ausencia de valor, categorias y el reloj del trader | ACTIVE |
| 0013 | StrategySpec: reglas que nombran parametros y nunca los contienen, y un hash que cubre lo que el bot hace | ACTIVE |
| 0014 | La base sobre la que se mide el objetivo: `base_calculo_objetivo` | ACTIVE |
| 0015 | Los relojes tras la auditoria: el del grafico es un default, y el dia de riesgo necesita el suyo | ACTIVE |
| 0016 | De donde sale cada regla: el campo `decision`, y un hash que cubre lo que un humano lee | ACTIVE |
| 0017 | El reloj del trader es su reloj civil: se revierte ADR-0012 y se confirma ADR-0005 | ACTIVE |
| 0018 | La precedencia va por clase, no por orden del fichero; y los siete defectos que eso destapo | ACTIVE |
| 0019 | La forma ejecutable de una regla: predicados con argumentos, ligadura, y cuatro cosas con nombre | ACTIVE |
| 0020 | La base del lotaje es la distancia hasta el stop, no la caja completa | ACTIVE |
