# El ritual de cierre

Como se cierra una rama de verdad: **lo ejecuta el usuario**, con lineas `!` desde Claude Code. La
sesion no hace merge, ni tag, ni push. Escrito el 2026-09-17 con lo aprendido en las ramas de
fidelidad de la spec, la guarda del holdout y los meses vistos.

## Tres correcciones que han costado tiempo

1. **`BOTSITO_ALLOW_MAIN=1` va PEGADA a la linea del `git commit`.** Cada linea `!` abre una shell
   nueva, asi que un `export` en una linea anterior no sobrevive. El merge, el tag y el push no la
   necesitan: el hook solo mira los commits.
2. **`make check` pasa de los 120 s y se va a segundo plano.** El push NO se encadena detras en la
   misma tanda: se espera el aviso de la tarea y se pushea despues. El 2026-09-17 se pusheo antes de
   saber si pasaba (paso, pero fue suerte).
3. **De una linea en una, mirando la salida.** `git status --short` vacio antes del merge, y
   `git diff --cached --name-only` con SOLO `PROJECT_STATE.md` antes del commit.

## Los pasos, con sus puertas

```
git checkout main
git status --short
```
→ **Puerta:** tiene que salir VACIO. Si hay algo sin commitear, se para aqui.

```
git merge --no-ff trabajo/<rama> -m "merge: <que entra, en una linea>"
```
→ **Puerta:** el `--stat` del merge tiene que traer los ficheros de la rama y ninguno mas. Si la rama
no tocaba `knowledge/spec/`, `knowledge/evidence/` ni `knowledge/feedback/`, ahi no puede aparecer
nada.

```
git tag -a stable/<tag> -m "<resumen de una linea>"
git rev-parse --short HEAD
```
→ Ese sha es el del merge: es el que va en `PROJECT_STATE.md`.

En este punto la sesion edita **SOLO `PROJECT_STATE.md`** (Current Branch, Current Feature, Stable
Main State, Completed Features, Features Waiting for Validation, la entrada del Change Log, Next
Action y Last Stable Commit) y **no commitea**.

```
git add PROJECT_STATE.md
git diff --cached --name-only
```
→ **Puerta:** SOLO `PROJECT_STATE.md`.

```
BOTSITO_ALLOW_MAIN=1 git commit -m "docs(state): <rama>, cerrada en main (stable/<tag>)"
```
→ Entre el merge y este commit, `state check` falla A PROPOSITO: `PROJECT_STATE.md` todavia describe
la rama como pendiente. Por eso `make check` va DESPUES del `docs(state)`, no antes.

```
make check > make-check.log 2>&1; echo "exit=$?"; tail -5 make-check.log; rm make-check.log
```
→ **Puerta:** `exit=0`. La salida va a un FICHERO, nunca a `/dev/null` (`lint-imports` falla al
escribir ahi y `make` sale con 2 aunque todo este verde). Como tarda mas de 120 s, la linea se va a
segundo plano: **se espera el aviso de la tarea antes de seguir.** Si falla, NO se pushea.

```
git push origin main
git push origin stable/<tag>
```

```
curl -s https://api.github.com/repos/Fibobrioso/Botsito/commits/<sha del docs(state)>/check-runs
```
→ **Puerta:** `"conclusion": "success"`. La CI que cuenta es la del `docs(state)`, no la del merge.

```
git branch -d trabajo/<rama>
```
→ Solo con la CI en verde. `-d` (no `-D`): si git se niega, es que algo no esta fusionado.

## Si la CI sale roja

No se revierte `main`. Se mira que fallo y se arregla con un commit encima.
