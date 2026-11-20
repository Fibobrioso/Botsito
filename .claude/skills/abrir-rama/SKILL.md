---
name: abrir-rama
description: Abre una rama de trabajo de Bot v3 desde main - crea la rama, copia el encargo tal cual en docs/encargos/, escribe su contrato.yaml y archiva en docs/state/HISTORIA.md el PROJECT_STATE.md de main - y la deja con su primer commit sellado. Usala cuando Aleks pide una rama nueva («Rama nueva: trabajo/...»).
argument-hint: "<rama trabajo/... o feature/...>"
---

# abrir-rama

Lo que `CLAUDE.md` («Como se trabaja») pide al abrir una rama, en un solo recorrido. Las reglas
viven en `CLAUDE.md`, `docs/runbooks/CONTRATO-DE-RAMA.md` y `docs/state/README.md`: aqui solo el
orden y las puertas.

## Entradas

| Entrada | De donde sale | Si falta |
|---|---|---|
| Nombre de la rama (`trabajo/<x>` o `feature/F##-<x>`) | el encargo | se pregunta |
| Base: `main` y su sha (y tag) | el encargo («desde main (df6aa2c, tag ...)») | se usa `main` y se dice |
| El texto del encargo, ENTERO | el mensaje de Aleks | sin el, no se abre: «el encargo guardado es copia literal del prompt» |
| Riesgo (bajo / medio / alto) | se elige con `CONTRATO-DE-RAMA.md`, «Como elegir el riesgo» | — |
| Tramo (el `## ` de `docs/plan/HOJA-DE-RUTA.md` al que pertenece la rama) | el encargo, o la entrada de la hoja de ruta que cita la letra de la Next Action que la origina | se pregunta; obligatorio si la hoja de ruta esta en `main` |

## Limites

- Si `Current Feature` de `PROJECT_STATE.md` esta en WAITING_FOR_USER_VALIDATION, se pregunta antes.
- El encargo se copia TAL CUAL: no se resume, no se corrige, no se traduce. Si el encargo cita algo
  que no esta en el repo («lo que hablamos»), se pregunta antes de abrir
  (`docs/runbooks/ERRORES-RECURRENTES.md`, «Una decision del consultor que se queda en la
  conversacion»).
- `rutas_permitidas` del contrato, tan estrechas como permita el encargo; lo que el encargo dice que
  no se toca, en `rutas_protegidas`. Si a mitad de rama hace falta ampliar, se amplia en un commit
  y el informe lo dice.
- `docs/state/HISTORIA.md` solo se amplia: se anade al final, nunca se edita lo que hay.
- Nada se commitea sin el sello (`CLAUDE.md`, «main no se toca»).

## Herramientas

Bash (git, `git fetch` y `git ls-remote`, la API de check-runs con el sha literal, `printf`,
`grep -c`, `make check`, `uv run botsito state check`), Write para el encargo y el contrato, Edit
para `PROJECT_STATE.md`.

## El recorrido

1. **Base.** `git fetch origin`, `git checkout main`, `git status --short` vacio, y la base entera
   comprobada con git, no de memoria (lo que cada encargo repetia a mano; E6 de
   `trabajo/entorno-code`):
   - `git rev-parse --short main` igual al sha del encargo, y `main` = `origin/main`
     (`git rev-parse main origin/main` da dos veces el mismo);
   - el ultimo tag de `docs/state/HISTORIA.md` (la ultima linea `- Tag: ` de sus registros de
     cierre) apunta al merge sobre el que esta `main`: `git rev-parse "stable/<tag>^{commit}"` igual
     a `git rev-parse main^1` (`main` es el commit de estado sobre el merge), y esta en origin
     (`git ls-remote --tags origin stable/<tag>` no sale vacio);
   - la CI de `main` sobre su HEAD (el commit de estado, no el merge: `RITUAL.md`, «La CI que
     cuenta es la del `docs(state)`, que es `HEAD`») en `completed` / `success`, por la API de check-runs
     con el sha de 40 caracteres escrito tal cual (las ordenes de cierre del consultor,
     `docs/state/HISTORIA.md`; la orden de `RITUAL.md` lo monta con `$(git rev-parse HEAD)`, y
     el clasificador puede negarla);
   - ninguna otra rama: `git branch --list` solo da `main` (ni `trabajo/*`, ni `feature/*`, ni
     `fix/*`), y `git ls-remote --heads origin "fix/*"` sale vacio.

   Si algo no cuadra, se para y se pregunta.
2. **Rama.** `git checkout -b <rama>`.
3. **Encargo.** `docs/encargos/<rama con - en lugar de />.md`: un titulo `# Encargo · <rama>`, una
   linea con la fecha y quien lo da, y el prompt entero citado con `>` linea a linea, sin tocarlo
   (ejemplo: `docs/encargos/trabajo-dieta-y-skills.md`).
4. **Contrato.** `contrato.yaml` en la raiz con la plantilla de `docs/runbooks/CONTRATO-DE-RAMA.md`:
   `rama`, `riesgo` con su motivo en el comentario, `artefacto: docs/validation/<NOMBRE>.md`,
   `tramo` (desde que `docs/plan/HOJA-DE-RUTA.md` esta en `main`: el titulo, o el id, de su `## `;
   entre comillas si lleva `: `; `make check` falla si falta o no existe en la hoja), `rutas_permitidas` (siempre `docs/encargos/`, `PROJECT_STATE.md`, `docs/state/HISTORIA.md`, el
   artefacto y `docs/validation/HOLDOUT-EXPOSICIONES.md`, por la fila del dia del paso 6), `rutas_protegidas` y `comprobaciones`. **El artefacto tiene que existir y estar
   estadiado ya en el primer commit**: `make check` lo exige en cuanto hay contrato (medido el
   2026-10-01 al abrir `trabajo/cuarentena-por-defecto`). Nace con su cabecera y EN CURSO; la
   fase 0 la escribe fase-cero en su commit.
   Nace tambien con su linea de PLANTILLA en sus primeros 600 caracteres:
   `tests/unit/test_hoja_de_ruta.py` lo comprueba solo en los `docs/validation/SESION-*-EXTRACCION.md`
   (sin ella, el primer `make check` de la rama sale en rojo, por segunda vez en
   `docs/validation/SESION-06-EXTRACCION.md` §7, punto 1); en los demas informes es la convencion
   que piden sus encargos (`docs/validation/DIETA-ESTADO.md`, `docs/validation/ACTIVAR-SESION-06.md`
   y `docs/validation/SKILLS-METODO.md`).
5. **Archivo de PROJECT_STATE** (`docs/state/README.md`, «Como se archiva»):
   - `N` = `grep -c '^# Archivo ' docs/state/HISTORIA.md` mas uno;
   - `printf '\n# Archivo N · PROJECT_STATE.md de main en <sha corto> (<AAAA-MM-DD>), al abrir <rama>\n\n' >> docs/state/HISTORIA.md`;
   - `git show main:PROJECT_STATE.md >> docs/state/HISTORIA.md`;
   - en `PROJECT_STATE.md`, `Completed Features` y `Change Log` vuelven a
     `— ninguna desde el Archivo N (<fecha>).`, y `Current Branch` y `Current Feature` dicen la rama
     nueva (EN CURSO, con su encargo y su informe), sustituyendo lo que habia.
6. **La fila del dia, y todo estadiado ANTES de comprobar.** Se escribe la fila de
   `docs/validation/HOLDOUT-EXPOSICIONES.md` del dia (reloj local), que nombre la rama ENTERA y diga
   que leeran sus `make check` (el M1 de marzo y de junio para calentar, como todos, mas lo que
   toque), y `rutas_permitidas` la incluye. Despues, `git add` de los ficheros nombrados: encargo,
   contrato, `PROJECT_STATE.md`, `docs/state/HISTORIA.md`, el artefacto y la fila. Desde
   `trabajo/guardias-holdout` (G2), `scripts/contrato_rama.py` falla en una rama `trabajo/*` sin
   esa fila ESTADIADA, y sin el artefacto estadiado ya fallaba antes
   (`docs/runbooks/CONTRATO-DE-RAMA.md`, «Que comprueba `make check`, y que no»). Es tambien la
   leccion 3 de la fila de `trabajo/guardia-falsos-positivos` en
   `docs/runbooks/ERRORES-RECURRENTES.md`: la fila va antes del primer `make check`.
7. **Comprobar antes de sellar.** `uv run botsito state check` (rama y recuento de tests fallan al
   FINAL de `make check`: mejor verlo antes) y `uv run python scripts/contrato_rama.py`, que tiene
   que dar `CONTRATO:` en verde y, en una rama `trabajo/*`, `G2: fila de HOLDOUT-EXPOSICIONES del
   <hoy> para <rama>, estadiada` (en `feature/` G2 no actua y esa linea no sale; la fila del dia se
   escribe igual, porque lo pide ADR-0021 §4). Y, antes de cada `make check`, `uv run botsito knowledge validate` sin `ERROR`, con
   su log en la carpeta de trabajo de la sesion, fuera del repo (fila de
   `trabajo/preparacion-sesion-7` en `docs/runbooks/ERRORES-RECURRENTES.md`, leccion 11): un id
   inexistente citado en el informe tumba `make check` (fila de `trabajo/dieta-estado`, misma
   tabla).
8. **Sello y commit.** Con lo del paso 6 estadiado y nada mas, `make check > make-check.log 2>&1`,
   esperar el aviso, leer el log (exit 0, ningun `failed`, la linea `CONTRATO:`, la `G2:` si la rama
   es `trabajo/*`, la linea `SELLO`) y commit `chore(rama): abre <rama> (encargo, contrato y Archivo N de PROJECT_STATE)`.

## Artefacto

La rama con un commit sellado que trae `docs/encargos/<rama>.md`, `contrato.yaml`, el Archivo N
nuevo al final de `docs/state/HISTORIA.md`, `PROJECT_STATE.md` apuntando a la rama, el artefacto y
la fila del dia en `docs/validation/HOLDOUT-EXPOSICIONES.md` (paso 6).

## Verificacion

- `git branch --show-current` es la rama, y `git log --oneline main..HEAD` tiene un commit.
- `make-check.log` con `CONTRATO:` en verde, la linea `G2:` de la fila del dia (en `trabajo/*`) y
  la linea `SELLO`.
- `tests/unit/test_historia.py` en verde dentro de `make check` (HISTORIA solo se amplio).
- `git diff main --stat` = encargo, contrato, `PROJECT_STATE.md`, `docs/state/HISTORIA.md`, el
  artefacto y `docs/validation/HOLDOUT-EXPOSICIONES.md` (la fila del dia, paso 6); nada mas.
- Las cuatro comprobaciones de la base (paso 1), con su salida, en el informe de la rama.
