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

Bash (git, `printf`, `grep -c`, `make check`, `uv run botsito state check`), Write para el encargo y
el contrato, Edit para `PROJECT_STATE.md`.

## El recorrido

1. **Base.** `git checkout main`, `git status --short` vacio, y `git rev-parse --short main` igual al
   sha del encargo. Si no coincide, se para y se pregunta.
2. **Rama.** `git checkout -b <rama>`.
3. **Encargo.** `docs/encargos/<rama con - en lugar de />.md`: un titulo `# Encargo · <rama>`, una
   linea con la fecha y quien lo da, y el prompt entero citado con `>` linea a linea, sin tocarlo
   (ejemplo: `docs/encargos/trabajo-dieta-y-skills.md`).
4. **Contrato.** `contrato.yaml` en la raiz con la plantilla de `docs/runbooks/CONTRATO-DE-RAMA.md`:
   `rama`, `riesgo` con su motivo en el comentario, `artefacto: docs/validation/<NOMBRE>.md`,
   `rutas_permitidas` (siempre `docs/encargos/`, `PROJECT_STATE.md`, `docs/state/HISTORIA.md` y el
   artefacto), `rutas_protegidas` y `comprobaciones`.
5. **Archivo de PROJECT_STATE** (`docs/state/README.md`, «Como se archiva»):
   - `N` = `grep -c '^# Archivo ' docs/state/HISTORIA.md` mas uno;
   - `printf '\n# Archivo N · PROJECT_STATE.md de main en <sha corto> (<AAAA-MM-DD>), al abrir <rama>\n\n' >> docs/state/HISTORIA.md`;
   - `git show main:PROJECT_STATE.md >> docs/state/HISTORIA.md`;
   - en `PROJECT_STATE.md`, `Completed Features` y `Change Log` vuelven a
     `— ninguna desde el Archivo N (<fecha>).`, y `Current Branch` y `Current Feature` dicen la rama
     nueva (EN CURSO, con su encargo y su informe), sustituyendo lo que habia.
6. **Comprobar antes de sellar.** `uv run botsito state check` (rama y recuento de tests fallan al
   FINAL de `make check`: mejor verlo antes) y `uv run python scripts/contrato_rama.py`.
7. **Sello y commit.** `git add` de los ficheros nombrados (encargo, contrato, `PROJECT_STATE.md`,
   `docs/state/HISTORIA.md`), `make check > make-check.log 2>&1`, esperar el aviso, leer el log
   (exit 0, ningun `failed`, la linea `SELLO`) y commit
   `chore(rama): abre <rama> (encargo, contrato y Archivo N de PROJECT_STATE)`.

## Artefacto

La rama con un commit sellado que trae `docs/encargos/<rama>.md`, `contrato.yaml`, el Archivo N
nuevo al final de `docs/state/HISTORIA.md` y `PROJECT_STATE.md` apuntando a la rama.

## Verificacion

- `git branch --show-current` es la rama, y `git log --oneline main..HEAD` tiene un commit.
- `make-check.log` con `CONTRATO:` en verde y la linea `SELLO`.
- `tests/unit/test_historia.py` en verde dentro de `make check` (HISTORIA solo se amplio).
- `git diff main --stat` = encargo, contrato, `PROJECT_STATE.md` y `docs/state/HISTORIA.md`, nada mas.
