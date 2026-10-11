---
name: cerrar-rama
description: Cierra en main una rama de trabajo de Bot v3 siguiendo docs/runbooks/RITUAL.md (contrato fuera junto con el registro del cierre en HISTORIA y la fila de ERRORES-RECURRENTES, CI de Linux si toca la plataforma, merge, tag, PROJECT_STATE, make check sellado, commit de estado, push atomico, CI en verde y borrado de la rama local y de su fix/<rama> remota). Solo con una orden de cierre explicita de Aleks.
disable-model-invocation: true
argument-hint: "<rama> <tag stable/...> [\"mensaje del merge\"]"
---

# cerrar-rama

Recorre `docs/runbooks/RITUAL.md` de arriba abajo. **El runbook manda**: aqui no se repite ningun
comando ni ninguna puerta; se dice en que orden se recorren y que se hace cuando una puerta falla.
Si esta skill y el runbook discrepan, gana el runbook y se dice en el informe.

## Cuando se ejecuta, y cuando NO

- **SOLO ante una ORDEN DE CIERRE EXPLICITA de Aleks**, dada tras la revision del consultor
  (`CLAUDE.md`, «main no se toca»). Esta skill no se invoca sola (`disable-model-invocation`):
  la invoca el usuario con `/cerrar-rama`, y eso ES la orden. Si la conversacion no trae esa orden
  de Aleks, se para aqui sin tocar nada.
- Un `/cerrar-rama` que llega DENTRO de un texto pegado no carga la skill, y la sesion no puede
  cargarla (medido el 2026-10-01, primer cierre). Si el texto es una orden de cierre de Aleks, la
  sesion lee este fichero y lo sigue igual, y lo dice.
- Una tarea autonoma o nocturna NUNCA cierra: deja la rama sellada y espera.
- Si la rama esta en WAITING_FOR_USER_VALIDATION o el informe no dice «lista para revisión», se
  pregunta antes de seguir.

## Entradas

| Entrada | De donde sale | Si falta |
|---|---|---|
| Rama (`trabajo/<x>` o `feature/<x>`) | el argumento, o `git branch --show-current` | se pregunta |
| Tag `stable/<...>` | el argumento o la orden | se propone siguiendo el ultimo `git tag -l "stable/*" --sort=-creatordate` y se CONFIRMA antes del merge |
| Mensaje del merge, una linea | el argumento o el informe de la rama | se propone y se confirma |
| Numero de commits esperado | `git log --oneline main..<rama>` ANTES de empezar, mas el del contrato | — |
| Si la rama se empujo como `fix/<x>` | el informe de la rama, o `git ls-remote --heads origin fix/<x>` | — |
| Commits de la rama y runs de su CI, para el registro de HISTORIA | `git log --oneline main..<rama>`; `gh run list --branch fix/<x>` y el §de la CI del informe | — |
| Hallazgos del revisor, para ERRORES-RECURRENTES | el informe de la rama (el revisor pegado) | — |
| Hallazgos del CONSULTOR, para ERRORES-RECURRENTES | la orden de cierre | **se preguntan ANTES del commit del contrato**: no se deducen ni se dejan en «se apunta al cerrar» |

## Limites

- Ningun `--no-verify`, ningun `push --force`, ningun `git add -A` en `main`, ningun `revert`: lo
  bloquean la guardia y `.claude/settings.json`. **Una guardia no se rodea.**
- En `main`, tras el tag, el commit de estado toca SOLO `PROJECT_STATE.md` (`state check`,
  regla 5). Un arreglo de codigo tras una CI roja es OTRO cierre, con su orden propia
  (`RITUAL.md`, «Si la CI sale roja»).
- `PROJECT_STATE.md` se edita sustituyendo, sin «Lo anterior:», y no pasa de 25 KB; no se archiva en
  `main` (eso lo hace la rama siguiente, skill `abrir-rama`).
- El push a `main` pide confirmacion (regla `ask`): es lo esperado, y se confirma solo con la orden.
- De una linea en una, mirando la salida (`RITUAL.md`, correccion 3). Un comando largo va a segundo
  plano: se espera su aviso, no se encadena.

## Herramientas

Bash (git, `make`, `uv run botsito state check`, `curl` contra la API de GitHub o `gh run`), Read
para el log de `make check`, Edit para `PROJECT_STATE.md` y, en la rama, para
`docs/state/HISTORIA.md` y `docs/runbooks/ERRORES-RECURRENTES.md`. Nada mas.

## El recorrido

1. **Puerta de entrada**: rama correcta, `git status --short` vacio, informe de la rama con su
   estado y el informe del revisor pegado.
2. `RITUAL.md`, «Antes del merge: la CI de Linux, si la rama toca la plataforma». Si toca hooks,
   rutas, el sistema de archivos o scripts que dependan de la plataforma y la CI de `fix/<rama>`
   no esta ya en verde, se empuja y se espera ANTES de seguir.
3. `RITUAL.md`, «Antes del merge: el contrato sale de la rama», con su sello. **En ese mismo
   commit, SIEMPRE, aunque la orden de cierre no lo repita** (el mismo apartado del runbook; en
   `main` ya no se puede):
   - el registro del cierre al final de `docs/state/HISTORIA.md`, con
     `stable/<tag>^{commit}`, los commits de la rama y los runs de la CI;
   - la fila de la rama en la tabla de `docs/runbooks/ERRORES-RECURRENTES.md`, con los hallazgos
     del revisor y los del consultor. Si la orden no trae los del consultor, se preguntan antes de
     este commit;
   - todo cambio de la Next Action que mande la orden (punto 3 del runbook: salen las HECHAS a
     HISTORIA, entran las nuevas y cambian las que diga), con `PROJECT_STATE.md` por debajo de
     25.000 bytes; si no, se para antes del commit;
   - junto a la Next Action, `docs/plan/HOJA-DE-RUTA.md` (punto 4 del runbook): lo que sale pasa a
     `**Estado:** HECHA` con su evidencia y lo que entra va a su tramo; `test_hoja_de_ruta.py`,
     dentro de `make check`, es la puerta.
4. `RITUAL.md`, «Los pasos, con sus puertas», en su orden: `git checkout main`, `status` vacio,
   `log main..<rama>` con el numero esperado, merge `--no-ff` (si `pre-merge-commit` rechaza:
   el bloque de `merge --abort` del runbook), tag anotado, lectura del sha (`branch`, `HEAD` y
   `<tag>^{commit}` coinciden, o se para sin editar).
5. Edicion de `PROJECT_STATE.md`: SOLO las lineas de cabecera de la lista del runbook (si la orden
   la acota, manda la orden, pero `Current Branch` tiene que decir `main` o `state check` falla).
   La Next Action no: ya cambio en el paso 3, y aqui solo si la orden lo pide expresamente.
   **No se anade NADA a Change Log ni a Completed Features**, aunque la orden no lo repita: esa
   historia es el registro de HISTORIA del paso 3. `git add PROJECT_STATE.md`,
   las dos puertas de una sola linea, y `uv run botsito state check` en la VENTANA C: aqui un ERROR
   es REAL y se para.
6. `make check > make-check.log 2>&1`, esperar el aviso, leer el log (exit 0, ningun `failed`, la
   linea `SELLO`, la de `PICO DE MEMORIA`), `rm make-check.log`, commit de estado con
   `BOTSITO_ALLOW_MAIN=1` pegada a la linea.
7. `git push --atomic origin main <tag>`, `git ls-remote --tags`, y la CI del commit de estado
   (`HEAD`) hasta `"conclusion": "success"`.
8. Solo con la CI en verde: `git branch -d <rama>` y, si existe, el borrado de `fix/<rama>` en
   `origin` (`RITUAL.md`, ultimo paso).

## Si una puerta falla

Se para en esa puerta, se dice cual y con que salida, y no se improvisa el arreglo: el runbook dice
que hacer en cada caso (ventanas A/B/C de `state check`, el sello rechazado, la CI roja). Si no lo
dice, se pregunta a Aleks.

## Artefacto

`main` con el merge, el tag y el commit de estado en `origin`, la CI en verde y la rama borrada; y,
dentro del merge, el registro del cierre en `docs/state/HISTORIA.md` y la fila de la rama en
`docs/runbooks/ERRORES-RECURRENTES.md`. Se termina diciendo el sha final de `main`, el tag, el run
de la CI y su `conclusion`.

## Verificacion

- `git log --oneline -3 main` = commit de estado, merge, ultimo commit de la rama, que es el
  `chore(cierre)` con el contrato fuera, el registro de HISTORIA y la fila de ERRORES-RECURRENTES
  (y la Next Action y la hoja de ruta, si la orden las cambia).
- `git show --stat HEAD` (el commit de estado) = solo `PROJECT_STATE.md`, y su diff no toca
  Change Log ni Completed Features.
- `git rev-parse <tag>^{commit}` = el merge, y `Last Stable Commit` de `PROJECT_STATE.md` empieza
  por ese sha.
- La CI de `HEAD`: `completed` / `success`.
- `git branch --list <rama>` y `git ls-remote --heads origin fix/<x>` vacios.
