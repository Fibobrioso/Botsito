# El ritual de cierre

Como se cierra una rama de verdad: **lo ejecuta el usuario**, con lineas `!` desde Claude Code. La
sesion no hace merge, ni tag, ni push. Escrito el 2026-09-17 con lo aprendido en las ramas de
fidelidad de la spec, la guarda del holdout y los meses vistos.

## Tres correcciones que han costado tiempo

1. **`BOTSITO_ALLOW_MAIN=1` va PEGADA a la linea del `git commit`.** Cada linea `!` abre una shell
   nueva, asi que un `export` en una linea anterior no sobrevive. El merge, el tag y el push no la
   necesitan: el hook solo mira los commits.
2. **`make check` pasa de los 120 s y se va a segundo plano, y el push VA DENTRO DE SU `if`.** El
   2026-09-17 se pusheo antes de saber si pasaba (paso, pero fue suerte) y esto decia «el push NO se
   encadena detras: se espera el aviso y se pushea despues», que dependia de que alguien se
   acordara. **Desde el 2026-09-22 el push es una rama del `if`** (ver mas abajo): la tarea de
   segundo plano avisa cuando termina, y si `exit != 0` no hay push que esperar. Se sigue esperando
   el aviso; lo que ya no hace falta es acordarse de mirar.
3. **De una linea en una, mirando la salida.** `git status --short` vacio antes del merge, y
   `git diff --cached --name-only` con SOLO `PROJECT_STATE.md` antes del commit.
4. **`git add PROJECT_STATE.md`, NUNCA `git add -A`.** El 2026-09-22 se uso `git add -A`, entro un
   fichero de mas -una nota en un ADR- y el commit llego a `origin` con la CI en rojo. **La puerta
   del punto 3 existia y habria bastado**: lo que fallo es que se estadio con `-A` y no se miro la
   salida. Nombrar el fichero hace innecesario acordarse de mirar.
5. **Los comandos van COMO SE INVOCAN DE VERDAD**, con su `uv run` y sus flags. Dentro de un bloque
   pegado, **un `command not found` es indistinguible de una comprobacion que pasa**: imprime su
   error y la linea siguiente se ejecuta igual. El 2026-09-22 `botsito state check` a secas dio
   `command not found`.

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
git diff --stat stable/<tag ultimo>..HEAD
uv run botsito state check
```
→ **Puerta 1:** `git diff --cached --name-only` tiene que dar **SOLO `PROJECT_STATE.md`**. Se
estadia **nombrando el fichero**, nunca con `-A`.

→ **Puerta 2:** `git diff --stat stable/<tag ultimo>..HEAD` mas lo estadiado tiene que tocar **solo
`PROJECT_STATE.md`**. Tras el tag, en `main` no puede cambiar nada mas (MASTER_PLAN §F).

→ **Puerta 3, y va ANTES del commit a proposito:** `uv run botsito state check`. **Va a fallar, y
hay que leer TODAS sus lineas, no la primera.** Entre el merge y el `docs(state)` falla A PROPOSITO
por una razon conocida -`PROJECT_STATE.md` todavia describe la rama como pendiente-, pero
**acumula los errores y los imprime todos** (medido en `cli.py:state_check`: `errores.append(...)`
y un bucle al final, sin cortocircuito). Asi que **cualquier OTRA linea de error es real**. El
2026-09-22 la linea real decia *«main tiene cambios sin tag estable desde stable/F14-caja:
docs/adr/...»*, y no se leyo porque `state check` solo se corria despues, dentro de `make check`,
cuando el commit ya existia.

```
BOTSITO_ALLOW_MAIN=1 git commit -m "docs(state): <rama>, cerrada en main (stable/<tag>)"
```
→ Entre el merge y este commit, `state check` falla A PROPOSITO: `PROJECT_STATE.md` todavia describe
la rama como pendiente. Por eso `make check` va DESPUES del `docs(state)`, no antes.

**`make check` CONDICIONA EL PUSH. Una sola linea, y el push va dentro:**

```
make check > make-check.log 2>&1; ec=$?; echo "exit=$ec"
if [ $ec -eq 0 ]; then rm make-check.log; git push origin main && git push origin <tag>;
else echo "PARA. make check en rojo; el log se queda en make-check.log"; fi
```

→ **Puerta:** `exit=0`. La salida va a un FICHERO, nunca a `/dev/null` (`lint-imports` falla al
escribir ahi y `make` sale con 2 aunque todo este verde). Como tarda mas de 120 s, la linea se va a
segundo plano: **se espera el aviso de la tarea antes de seguir.**

**EL LOG SE QUEDA CUANDO FALLA**, que es justo cuando hace falta leerlo. La version anterior hacia
`rm make-check.log` siempre y **empujaba igual**: imprimia el codigo de salida y no frenaba nada.

```
curl -s --ssl-no-revoke https://api.github.com/repos/Fibobrioso/Botsito/commits/<sha del docs(state)>/check-runs \
  | grep -o '"status": *"[^"]*"\|"conclusion": *"[^"]*"'
```
→ **`--ssl-no-revoke` hace falta en esta maquina**, y sin el `curl` falla. Estaba escrito sin el
desde que se escribio el runbook. Y un `"status": "422"` no es un fallo de la CI: es GitHub diciendo
que **no conoce ese commit**, o sea que el push no se ha hecho.
→ **Puerta:** `"conclusion": "success"`. La CI que cuenta es la del `docs(state)`, no la del merge.

```
git branch -d trabajo/<rama>
```
→ Solo con la CI en verde. `-d` (no `-D`): si git se niega, es que algo no esta fusionado.

## Si la CI sale roja

No se revierte `main`. Se mira que fallo y se arregla con un commit encima.
