# docs/state

La historia de `PROJECT_STATE.md`. Nace el 2026-10-01 en `trabajo/dieta-y-skills`
(docs/validation/DIETA-Y-SKILLS.md): `PROJECT_STATE.md` pesaba 418.819 bytes y cada sesion lo
cargaba entero; ahora lleva solo el presente y lo demas vive aqui.

- `HISTORIA.md` → SOLO SE AMPLIA. Cada version commiteada empieza, byte a byte, por la anterior, y
  su Archivo 1 es `PROJECT_STATE.md` entero tal como estaba en `df6aa2c`. Lo vigila
  `tests/unit/test_historia.py` contra el historial de git.

## Que va en cada sitio

`PROJECT_STATE.md` lleva lo que es verdad HOY: la rama, `main` y su ultimo tag, el Next Action
vigente, las ambiguedades abiertas, la deuda abierta (una linea cada una) y las reglas que solo
vivian alli. No pasa de 25 KB (`tests/unit/test_project_state.py`). Lo que deja de ser verdad se
SUSTITUYE, sin «Lo anterior:», porque lo anterior ya esta aqui.

`Completed Features` y `Change Log` siguen en `PROJECT_STATE.md`, pero desde el 2026-10-01
(`trabajo/ajustes-cierre`) el cierre de una rama NO les anade nada: lo cerrado se apunta aqui, en
el `# Registro de cierre · <rama> (<fecha>)` que entra en la propia rama, en el mismo commit que
saca el contrato (`docs/runbooks/RITUAL.md`, «Antes del merge: el contrato sale de la rama»).

## Lo HECHO del Next Action sale de PROJECT_STATE en la rama que lo cierra

Desde el 2026-10-02 (decision del consultor, `feature/escenarios-por-sesion`): una entrada de Next
Action que pasa a HECHA se mueve a `HISTORIA.md` EN LA MISMA RAMA QUE LA CIERRA, con su texto
literal, bajo `# Next Action HECHA · <letra> · sale de PROJECT_STATE.md en <rama> (<fecha>)`, y en
`PROJECT_STATE.md` no queda ni el resumen. Va en el commit que saca el contrato
(`docs/runbooks/RITUAL.md`, «Antes del merge: el contrato sale de la rama», punto 3), porque en
`main` solo cambia `PROJECT_STATE.md` y alli no se archiva. Sin esto, el cierre suma entradas
HECHAS y `PROJECT_STATE.md` pasa de los 25 KB. Desde el 2026-10-08 (punto Y,
`trabajo/adelgazar-estado`) ese commit lleva TODO cambio de la Next Action que mande la orden de
cierre, no solo las HECHAS (abajo, «Que sale de PROJECT_STATE, y con que criterio»).

## Como se archiva

Al ABRIR una rama (skill `abrir-rama`, paso de archivo), en la propia rama y antes de tocar nada:

1. Se anade AL FINAL de `HISTORIA.md` un encabezado
   `# Archivo N · PROJECT_STATE.md de main en <sha corto> (<fecha>), al abrir <rama>` y, debajo, el
   `PROJECT_STATE.md` de `main` entero, tal cual (`git show main:PROJECT_STATE.md`).
2. En `PROJECT_STATE.md` se vacian `Completed Features` y `Change Log` (lo suyo ya esta en el
   archivo): `— ninguna desde el Archivo N (<fecha>).`

Asi el cierre de cada rama -que solo puede tocar `PROJECT_STATE.md` en `main`: `state check`,
regla 5- queda archivado por la rama siguiente, y en `main` no cambia nada mas. Su registro de
cierre (tag, commits, runs de la CI) ya entro antes, en la rama.

## Que sale de PROJECT_STATE, y con que criterio

Desde el 2026-10-08 (decision del consultor, `trabajo/adelgazar-estado`): una linea de «Pendientes
heredados», «Technical Debt» o «Reglas vivas» sale de `PROJECT_STATE.md` SOLO si cumple una de
estas condiciones, con su evidencia citada (fichero:linea, commit, tag o ADR):

- (a) HECHA o PAGADA: hay commit, tag, ADR o test que lo muestra;
- (b) REPETIDA: su contenido esta vivo, entero, en otra entrada de la Next Action, en `CLAUDE.md` o
  en un runbook;
- (c) SUSTITUIDA: un hecho posterior la dejo sin objeto;
- (d) NO ES DE SU SECCION: una regla o un hecho que vive literal en otro sitio. Si no vive en
  ningun otro sitio, se queda.

**Niega por defecto: si hay duda, la linea se queda**, y lo que se queda no se resume ni se
reescribe. Lo que sale va al final de `HISTORIA.md`, con su texto literal, su condicion y su
evidencia, en un bloque por clase: `# Pendiente heredado SALE`, `# Technical Debt PAGADA`,
`# Technical Debt RECLASIFICADA` o `# Regla viva SUSTITUIDA`, seguido de
`· sale de PROJECT_STATE.md en <rama> (<fecha>)`. En `PROJECT_STATE.md` no queda ni un resumen.

Y desde el mismo dia (punto Y, `docs/runbooks/RITUAL.md`): TODO cambio de la Next Action que mande
la orden de cierre -salen las HECHAS, entran las nuevas y cambian las que diga la orden- se hace en
la rama, en el commit que saca el contrato (punto 3); en el commit de estado de `main` la Next
Action solo cambia si la orden de cierre lo pide expresamente.

## Lo que decian las introducciones de PROJECT_STATE.md hasta el 2026-10-08

En `trabajo/adelgazar-estado` las introducciones del fichero y de sus secciones se acortaron a una
o dos lineas que apuntan aqui. Lo que decian, tal cual:

- La cabecera: «Memoria operativa: lo que es verdad HOY, y nada mas. Una sesion nueva lee este
  fichero y `CLAUDE.md`; lo demas, solo si la tarea lo pide (`CLAUDE.md`, «Por donde se empieza»).
  **Lo que dejo de ser presente vive en `docs/state/HISTORIA.md`, que solo se amplia**: la historia
  de merges, las funcionalidades cerradas, el Change Log, los bloques «LO QUE DECIA…», las deudas
  pagadas, el indice de ADR (que vive en `docs/adr/README.md`), los componentes y los ficheros
  importantes. Desde el 2026-10-01 (`trabajo/dieta-y-skills`) aqui se SUSTITUYE lo que deja de ser
  verdad, sin «Lo anterior:», y al abrir cada rama se archiva en HISTORIA el `PROJECT_STATE.md` de
  `main` (docs/state/README.md, skill `abrir-rama`). Tope: 25 KB (`tests/unit/test_project_state.py`).»
- «Pendientes heredados (sin verificar)»: «Los puntos del Next Action viejo (Archivo 1 de
  docs/state/HISTORIA.md, donde esta su texto entero) que no tienen evidencia de estar hechos
  -commit, tag, ADR o test-, uno por linea con su arranque literal; la evidencia, punto por punto, en
  docs/validation/DIETA-Y-SKILLS.md §6. Las ramas a), c) y 0) de A3 si la tienen y solo estan en
  HISTORIA. Se quitan de aqui cuando haya evidencia o lo decida el consultor.»
- «Known Ambiguities»: «Las ABIERTAS. La fuente es `knowledge/spec/ambiguedades.yaml`, y
  `tests/unit/test_kit.py` exige que esta tabla tenga exactamente sus ids `ABIERTA`, con el mismo
  titulo, clase y bloqueante: abrir una anade su fila; cerrarla (RESUELTA o DECIDIDA) la quita. La
  pregunta entera y su historia, en `docs/spec/ambiguedades.md` (generado); las cerradas y la tabla
  con sus notas hasta el 2026-10-01, en docs/state/HISTORIA.md (Archivo 1, «Known Ambiguities»).»
- «Technical Debt»: «Una linea por deuda ABIERTA: el arranque literal de su entrada; el texto
  entero, buscando esa frase en docs/state/HISTORIA.md (Archivo 1, «Technical Debt»). Una deuda
  nueva entra con una linea que apunte a su informe; una pagada se borra de aqui. Las entradas que
  su propio texto ya daba por cerradas el 2026-10-01 (RESUELTA, CORREGIDA, DECIDIDA, CERRADA,
  HECHO…) solo estan en HISTORIA, y la de los cinco patrones de defecto, que es una regla, esta
  entera en docs/runbooks/ERRORES-RECURRENTES.md.»
- «Reglas vivas»: «Las que hasta el 2026-10-01 solo estaban en este fichero, copiadas tal cual con
  su titulo de entonces. Las demas viven en `CLAUDE.md` y en `docs/runbooks/`.»
- «Completed Features»: «Las cerradas desde el ultimo archivo de docs/state/HISTORIA.md; las
  anteriores, alli. `state check` (regla 4) mira las dos. Desde `trabajo/ajustes-cierre`
  (2026-10-01) el cierre de una rama NO anade aqui nada: lo cerrado va al `# Registro de cierre` de
  HISTORIA, en la rama (docs/runbooks/RITUAL.md).»
- «Change Log»: «Las entradas desde el ultimo archivo de docs/state/HISTORIA.md; las anteriores,
  alli. El cierre de una rama no anade ninguna desde `trabajo/ajustes-cierre` (2026-10-01): va al
  registro de HISTORIA.»
