# El ritual de cierre

Como se cierra una rama de verdad: **lo ejecuta el usuario**, con lineas `!` desde Claude Code. La
sesion no hace merge, ni tag, ni push. Escrito el 2026-09-17 con lo aprendido en las ramas de
fidelidad de la spec, la guarda del holdout y los meses vistos.

## Seis correcciones que han costado tiempo

1. **`BOTSITO_ALLOW_MAIN=1` va PEGADA a la linea del `git commit`.** Cada linea `!` abre una shell
   nueva, asi que un `export` en una linea anterior no sobrevive. El merge, el tag y el push no la
   necesitan: el merge no dispara `pre-commit` sino `pre-merge-commit`, que solo mira el sello
   (correccion 7).
2. **`make check` va ANTES del commit y lo SELLA; el commit y el push van DESPUES.** Pasa de los
   120 s y se va a segundo plano: se espera el aviso. Historia: el 2026-09-17 se pusheo antes de
   saber si pasaba; el 2026-09-22 el push se encadeno detras de `make check` con `&&`, despues del
   commit. **Desde el 2026-09-25 (`trabajo/blindaje`) el hook rechaza un commit cuyo arbol no tenga
   el sello de un `make check` en verde, asi que el orden commit → `make check` → push ya no
   funciona**: el commit se rechazaria. Ahora la puerta la pone el hook, y no la cadena.
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
6. **Ninguna comprobacion que pase siempre.** Hasta el 2026-09-22 aqui iba
   `git diff --stat stable/<tag>..HEAD` justo despues del tag, como «puerta 2». Tras el tag, `HEAD`
   ES el commit del tag, asi que compara un commit consigo mismo: **sale vacio siempre**, y un diff
   entre commits ni siquiera ve lo estadiado. Una puerta que no puede fallar no para nada. Lo que de
   verdad mira que no entre nada mas es `git diff --cached --name-only` junto con `git status --short`.

7. **La puerta del sello (2026-09-25, `trabajo/blindaje`).** `make check` en verde escribe el hash
   del arbol ESTADIADO en un sello; `pre-commit` y `pre-merge-commit` rechazan cualquier arbol que
   no sea ese. Por eso se estadia primero y se prueba despues, y por eso `make-check.log` esta en
   `.gitignore`: si no, el sello no se escribiria nunca. **`--no-verify` esta prohibido**
   (`CLAUDE.md`). Los hooks se instalan con `make hooks` (ver «La primera vez con la puerta»).

## Cuándo falla `state check`, y cuándo un fallo es REAL

**`uv run botsito state check` lee el FICHERO DEL DISCO, no el commit.** Por eso el tramo en el que
falla a propósito **termina al EDITAR `PROJECT_STATE.md`, no al commitearlo**. Medido el 2026-09-22 en
un clon desechable, las tres ventanas:

- **(A) Tras el MERGE y antes del TAG → falla, y es ESPERADO.** El último tag estable todavía es el
  anterior, y `diff <último tag>..HEAD` trae los ficheros de la rama recién fusionada: *«main tiene
  cambios sin tag estable desde stable/…»*.
- **(B) Tras el TAG y antes de EDITAR `PROJECT_STATE.md` → falla, y es ESPERADO.** `Last Stable
  Commit` todavía declara el sha viejo mientras el tag nuevo apunta al merge: *«'Last Stable Commit'
  dice '…'; el tag … apunta a …»*.
- **(C) Con `PROJECT_STATE.md` YA EDITADO, aunque sin commitear → da OK.** **Aquí un ERROR no es
  esperado: ES REAL, y se para.**

En el ritual, `state check` **solo se corre en la ventana C**. El 2026-09-22 el error real estaba
justo ahí («main tiene cambios sin tag estable»), y este runbook decía que era esperado. Esa frase ya
no está.

## Los pasos, con sus puertas

Así se ejecutó el cierre de `trabajo/mayo-dev-ingerido` el 2026-09-22, en este orden. Una línea `!`
por paso, mirando la salida de cada una.

```
git checkout main
git status --short
```
→ **Puerta:** tiene que salir VACÍO. Si hay algo sin commitear, se para aquí.

```
git log --oneline main..trabajo/<rama>
```
→ **Puerta:** salen **los commits de la rama, en el número esperado** (el informe o la sesión lo
dice antes), y ninguno más.

```
git merge --no-ff trabajo/<rama> -m "merge: <qué entra, en una línea>"
```
→ **Puerta:** el `--stat` del merge trae los ficheros de la rama y ninguno más. Si la rama no tocaba
`knowledge/spec/`, `knowledge/evidence/` ni `knowledge/feedback/`, ahí no puede aparecer nada.
→ **Puerta del sello (desde el 2026-09-25):** el merge pasa por `pre-merge-commit`, que exige que el
árbol fusionado tenga sello. Si `main` no se ha movido desde que salió la rama, ese árbol es el del
último commit de la rama, que se selló al commitearlo, y pasa sin hacer nada. **No se corre
`make check` en `main` antes del merge:** reescribiría el sello con el árbol viejo. Si sale
`pre-merge-commit: rechazado`, el merge queda a medias. **No se sella en `main` a mitad de merge**:
`PROJECT_STATE.md` todavía declara la rama de trabajo y `state check` falla por diseño (ventana A),
así que `make check` saldría en rojo. Se vuelve atrás y se sella en la rama:

```
git merge --abort
git checkout trabajo/<rama>
make check > make-check.log 2>&1
grep "SELLO: make check en verde" make-check.log
rm make-check.log
git checkout main
git merge --no-ff trabajo/<rama> -m "merge: <qué entra, en una línea>"
```
Si `main` se hubiera movido desde que salió la rama, el árbol fusionado no es el de la rama, y esto
no basta: se para y se decide con el consultor.
→ Estamos en la **ventana A**: aquí `state check` fallaría por diseño. No se corre.

```
git tag -a stable/<tag> -m "<resumen de una línea>"
git rev-parse --short HEAD
```
→ Ese sha es el del merge, y es el que va en `PROJECT_STATE.md`.
→ Estamos en la **ventana B**: aquí `state check` también fallaría por diseño. No se corre.

**La sesión edita SOLO `PROJECT_STATE.md`**, **sin estadiar** y sin commitear: Current Branch,
Current Feature, Stable Main State, Completed Features, Features Waiting for Validation, la entrada
del Change Log, Next Action y Last Stable Commit.

**El sha del merge lo LEE la sesión del repositorio; el mensaje que se le pasa NO lleva hueco
`<SHA>`.** Antes de editar, la sesión ejecuta:

```
git branch --show-current
git rev-parse --short HEAD
git rev-parse --short "stable/<tag>^{commit}"
```
→ **Puerta:** la rama es `main` y los dos sha coinciden. Si no está en `main`, o el tag no existe, o
no apunta a `HEAD`, **la sesión se para sin editar nada** y dice qué falta. Hasta el 2026-09-23 el
mensaje llevaba un hueco `<SHA>` que se rellenaba a mano, y se pegó sin rellenar cuatro veces, dos de
ellas antes del merge (patrón 5).

```
git add PROJECT_STATE.md
git diff --cached --name-only
git status --short
```
→ **Puerta:** `git diff --cached --name-only` da **una sola línea, `PROJECT_STATE.md`**. Se estadía
**nombrando el fichero**, nunca con `-A`.
→ **Puerta:** `git status --short` da **una sola línea, `M  PROJECT_STATE.md`**, con la **M en la
PRIMERA columna** (estadiado). Una `M` en la segunda columna (` M`) significa que no se ha estadiado.
Cualquier otra línea es un fichero de más, y tras el tag en `main` no puede cambiar nada más
(MASTER_PLAN §F).

```
uv run botsito state check
```
→ **Puerta, ventana C:** tiene que dar **OK**. **Un ERROR aquí es REAL.** `state check` acumula los
errores y los imprime todos, sin cortocircuito (`cli.py:state_check`): se leen TODAS las líneas.

**Desde aquí el orden cambió el 2026-09-25: el hook solo deja entrar un commit cuyo árbol tenga el
sello de un `make check` en verde, así que `make check` va antes del commit, y el push, después.**

```
make check > make-check.log 2>&1
```
→ Tarda más de 120 s y se va a segundo plano: **se espera el aviso de la tarea antes de seguir.** La
salida va a un FICHERO, nunca a `/dev/null` (`lint-imports` falla al escribir ahí y `make` sale con 2
aunque todo esté verde). Si sale distinto de 0, no hay sello: el log se queda para leerlo y **no se
sigue**.

```
grep "SELLO: make check en verde" make-check.log
```
→ **Puerta:** una línea con el hash del árbol. Si en su lugar sale un `AVISO: ... NO se sella`, hay
algo sin estadiar o sin seguir: se arregla y se repite `make check`. Sin esta línea, el commit se
rechazará.

```
rm make-check.log
BOTSITO_ALLOW_MAIN=1 git commit -m "docs(state): trabajo/<rama>, cerrada en main (stable/<tag>)"
```
→ **Puerta:** el commit sale con su sha. Si sale `pre-commit: rechazado`, el árbol no es el que se
probó: se vuelve a `make check`, nunca a `--no-verify`.

```
git push origin main
git push origin stable/<tag>
```
→ **Puerta:** los dos pushes terminan sin error. Solo se ejecutan con el commit hecho.

```
git ls-remote --tags origin stable/<tag>
```
→ **Puerta:** el tag está en `origin`. **El sha que sale es el del OBJETO TAG, no el del commit**,
porque el tag es anotado (`-a`). El commit al que apunta se ve con
`git rev-parse stable/<tag>^{commit}`, y tiene que ser el merge. El 2026-09-22 salió `0c477f3…`
para un tag que apunta al merge `48075f6`.

```
curl -s --ssl-no-revoke https://api.github.com/repos/Fibobrioso/Botsito/commits/$(git rev-parse HEAD)/check-runs | grep -o '"status": *"[^"]*"\|"conclusion": *"[^"]*"'
```
→ **`--ssl-no-revoke` hace falta en esta máquina**; sin él el `curl` falla.
→ **`"status": "in_progress"` o `"queued"`:** la CI sigue corriendo. Se espera y se repite la misma
línea.
→ **`"status": "422"`:** no es un fallo de la CI. Es GitHub diciendo que **no conoce ese commit**, o
sea que **el push no llegó**.
→ **Puerta:** `"status": "completed"` con `"conclusion": "success"`. La CI que cuenta es la del
`docs(state)`, que es `HEAD`, no la del merge.

```
git branch -d trabajo/<rama>
```
→ **Solo con la CI en verde.** `-d` y no `-D`: si git se niega, es que algo no está fusionado.

## Si la CI sale roja

No se revierte `main`. Se mira que fallo y se arregla con un commit encima, con el mismo orden:
estadiar el arreglo, `make check > make-check.log 2>&1`, comprobar el `SELLO`, `rm make-check.log`,
`BOTSITO_ALLOW_MAIN=1 git commit` y los dos pushes.

## La primera vez con la puerta

Los hooks viven en `scripts/git-hooks/` y se COPIAN a `.git/hooks` con **un solo comando, desde la
raíz: `make hooks`**. Hay que ejecutarlo cada vez que cambia un hook. **Copia los hooks de la rama
EN LA QUE ESTÁS**, así que tras `trabajo/blindaje` va en esa rama, ANTES de `git checkout main`: en
`main`, antes del merge, instalaría los viejos. En ese primer cierre:

```
git branch --show-current
make hooks
```
→ **Puerta:** la rama es `trabajo/blindaje`, y `make hooks` lista `pre-commit` y `pre-merge-commit`.
Después, el ritual de siempre desde `git checkout main`. El merge pasa sin más, porque el último
commit de la rama ya se selló al hacerse.
