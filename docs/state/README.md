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
