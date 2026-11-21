# Sesión 7b con el trader: la extracción por pregunta y por sesión del bloque de días

> **PLANTILLA mientras la rama está EN CURSO**: la tabla final entra con la extracción.

> **Borrador para el consultor. Esta rama NO resuelve nada**: no hay `feedback apply`, ni
> ambigüedades cerradas, ni cambios en la spec, en el motor, en los casos, en las cifras, en
> `SESION_EN_CURSO` ni en la hoja de ruta (R4.3 sigue ABIERTA); de `PREGUNTAS-7B.md` solo cambia el
> recuadro de la hoja usada. Cada «resuelve» de abajo es una propuesta sobre lo que dijo el trader;
> el destino de cada respuesta lo decide el consultor en la rama de activación de la 7b (encargo del
> 2026-11-21, `docs/encargos/trabajo-sesion-08.md`).

Rama `trabajo/sesion-08`, abierta el 2026-11-21 desde `main` en `5ae7c482` (commit de estado sobre
el merge `c6d5a9c2`, tag `stable/F39i-guardia-enlaces`). Tramo R4 de la hoja de ruta (R4.3, NA:F,
paso (2)). Skill `ingerir-sesion`, de principio a fin, y ADR-0093 §2. Plantilla:
`SESION-07-EXTRACCION.md`. Tag de cierre previsto: `stable/F39j-sesion-08` (no existe ni en local
ni en origin: `git tag -l 'stable/F39j*'` y `git ls-remote --tags origin 'stable/F39j*'` vacíos).

## Base comprobada al abrir

- `git fetch --prune`; en `main`, `git status --short` vacío.
- `git rev-parse main origin/main` da dos veces `5ae7c482f6dd4ef00f333dbc307ac23466f3dee0`.
- El último `- Tag: ` de `docs/state/HISTORIA.md` es `stable/F39i-guardia-enlaces`;
  `git rev-parse "stable/F39i-guardia-enlaces^{commit}"` = `git rev-parse main^1` =
  `c6d5a9c2cf39c6e1922f7721aa6b7f0448437ee5`; `git ls-remote --tags origin` da
  `9fb6345d… refs/tags/stable/F39i-guardia-enlaces` (el objeto del tag anotado) y su `^{}`,
  `c6d5a9c2…`. Es también el primero de `git tag -l 'stable/*' --sort=-creatordate`.
- CI de `main` sobre su HEAD, una consulta suelta de `gh run view 44871267577`: `completed`,
  `success`, `headSha` `5ae7c482f6dd4ef00f333dbc307ac23466f3dee0`, rama `main`.
- `git branch -a` solo da `main` y `origin/main`; `git ls-remote --heads origin` solo da
  `refs/heads/main` (ningún `fix/*`).
- `scripts/transcribir_sesion.py` de `main`: `"08": {` en la línea 260 de
  `CODIGOS_DE_SESION_TEXTO`, con 7 textos, S-1 a S-7; `"08": ORDEN_SESION_08` en `HOJAS` (línea
  278); `SESION_EN_CURSO = "08"` (línea 283).
- `PROJECT_STATE.md`: 24.576 bytes en `main` y 24.614 tras abrir (`wc -c`), por debajo de 24.900.
- **El corpus no es un enlace de unión**: `fsutil reparsepoint query corpus` da «Error 4390: El
  archivo o directorio no es un punto de análisis repetido» (exit 1): es una carpeta normal.

## Decisiones de proceso de la rama

- Al comprobar qué vídeos del primer nivel faltan en `fuentes.yaml`, la guardia negó (solo lectura)
  un bucle `for f in ...; do b=$(basename "$f"); grep -qF "$b" ...` («`basename` recibe un argumento
  que se construye al ejecutarse»); seguí su forma (guion con Write, ejecutado en otra llamada), y
  ese guion lo negó también («el codigo nombra la carpeta C:\Users\USER\Desktop\Bot v3, que contiene
  material protegido»); seguí la forma que propone su segundo mensaje, «rutas LITERALES»: un solo
  `grep -o -F -e "<nombre>" ...` con los 17 nombres del listado escritos tal cual sobre
  `knowledge/corpus/fuentes.yaml` (`docs/runbooks/DECISIONES-DE-PROCESO.md`).
- La guardia negó las dos líneas de «Antes», paso 1, en un solo comando («antes, en el mismo
  comando, va `uv run python -c ...`»); seguí su forma: una llamada por ejecutable.

## 0. Lo primero

### 0.1 Los días, antes de registrar

La línea de `SESION-DE-PREGUNTAS.md` («Antes», paso 1), que imprime solo `True` o `False`:
- `2026-11-20`: `False`.
- `2026-11-21`: `False`.

### 0.2 Los vídeos

Son los dos únicos vídeos del primer nivel de `corpus/Estrategia del trader/` que no estaban en
`fuentes.yaml` (los otros 15 vídeos de ese nivel salen una vez cada uno):
- `Grabación de pantalla 2026-11-20 182155.mp4`, 4.878.875.346 bytes (v20, el primer día);
- `Grabación de pantalla 2026-11-21 104411.mp4`, 8.440.884.009 bytes (v21, el segundo día).

El id de la sesión es `2026-11-20-sesion-08` (el del primer día; encargo, OBJETIVO).

## Estado

EN CURSO.
