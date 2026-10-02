# El ritual de cierre

Como se cierra una rama de verdad. **Desde el 2026-09-26 lo ejecuta Claude Code, paso a paso y
mirando cada puerta, SOLO ante una orden de cierre explicita de Aleks dada tras la revision del
consultor**; hasta entonces lo ejecutaba el usuario con lineas `!` y la sesion no hacia merge, ni
tag, ni push. Los commits en las ramas `trabajo/*` los hace Claude Code; una tarea autonoma o
nocturna NUNCA cierra: deja la rama con sus commits sellados y espera la orden. Ninguna puerta
cambia: el sello, `main` y el tag en un solo push atomico, y la CI en verde antes de borrar la
rama. Las dos primeras ramas cerradas asi fueron `trabajo/visor-dias` (2026-09-25, con la orden
«sigue el ritual tal cual») y `trabajo/ticks-llenado` (2026-09-26, con la orden de cierre tras la
revision del consultor). Escrito el 2026-09-17 con lo aprendido en las ramas de fidelidad de la
spec, la guarda del holdout y los meses vistos. Desde el 2026-10-01 lo ejecuta la skill
`cerrar-rama` (`.claude/skills/cerrar-rama/SKILL.md`), que sigue este runbook paso a paso: aqui
estan las puertas, y alli solo como se recorren.

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

8. **`main` y el tag se empujan en el MISMO push, `--atomic`.** El run `36174003223` salió rojo porque
   se empujaron en dos líneas: el push de `main` (`ac4e3a0`) creó el run a las 18:31:45, y la CI hizo
   su `git fetch --tags` a las 18:31:50, antes de que llegara el tag. Sin el tag, `state check` ve el
   merge como «cambios sin tag estable» y falla. Relanzado con el tag ya en `origin`, el mismo árbol
   salió verde (intento 2). Hasta el 2026-09-25 el ritual encadenaba los dos pushes con `&&`, y
   `trabajo/blindaje` los separó en dos líneas; `git push --atomic` actualiza los dos refs de una
   vez (`docs/validation/ARREGLO-CI.md`).

9. **Ya no hace falta anteponer `PYTHONUTF8=1` al `git commit` (2026-09-25, rama
   `trabajo/simulador-cuenta`).** Desde una consola de Windows en cp1252, `lint-imports` pintaba un
   emoji, Python reventaba con `UnicodeEncodeError` y el hook lo contaba como «contrato de
   importacion roto»; la salida era escribir `PYTHONUTF8=1` pegada a cada `git commit`. Ahora los
   dos hooks versionados exportan la variable ellos mismos antes de lanzar ninguna herramienta
   Python, porque un hook no puede depender de lo que cada terminal tenga configurado. Lo vigila
   `tests/unit/test_hooks_utf8.py` con una consola cp1252 simulada y un `uv` falso: el hook
   versionado pasa y el mismo hook sin la linea vuelve a rechazar. Hay que reinstalarlos una vez con
   `make hooks` desde la rama que los trae.

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

### Antes del merge: la CI de Linux, si la rama toca la plataforma (desde el 2026-10-01)

**Toda rama que toque hooks (`scripts/git-hooks/`, `.claude/hooks/`), rutas, el sistema de archivos
o scripts que dependan de la plataforma se empuja como rama y espera la CI de Linux en verde ANTES
del merge a `main`.** Los tests en local corren en Windows, y Windows tapa tres cosas que Linux no:
el separador `\`, `os.path.normcase` (que en Linux no baja a minúsculas) y las mayúsculas y
minúsculas de las rutas. Así salió roja la CI de `main` tras cerrar `trabajo/guardias-claude`
(run 36889215829, con todo verde en local; `docs/validation/GUARDIAS-CLAUDE.md`, recuadro inicial).

Una rama `trabajo/*` no dispara la CI (`.github/workflows/ci.yml` solo corre en `main`,
`feature/**` y `fix/**`), así que se empuja con otro nombre, sin tocar la local:
`git push origin trabajo/<rama>:refs/heads/fix/<rama>` (en texto y no en bloque: los bloques de este
runbook solo llevan el push atómico de `main` y el tag, `tests/unit/test_push_atomico.py`).
→ **Puerta:** la CI de ese commit termina en `"conclusion": "success"`, salvo UN fallo esperado y
solo ese: `state check` avisa de que `PROJECT_STATE` declara `trabajo/<rama>` y la rama es
`fix/<rama>` (`test_state_check_ok_on_real_repo`). Cualquier otro fallo para el merge. Medido el
2026-10-01 con `trabajo/guardia-linux` (run 36894169605, intento 2: 1 fallo, ese). Si la CI se
cancela por tiempo antes de `make check` (el intento 1 se colgó 20 minutos instalando `ffmpeg`), no
es un resultado: se relanza con `gh run rerun <run>`. La rama remota `fix/<rama>` se borra al final
del ritual, con las demás.

### Antes del merge: el contrato sale de la rama (desde el 2026-10-01)

Si la rama tiene `contrato.yaml` (`docs/runbooks/CONTRATO-DE-RAMA.md`), sale de ella ANTES del
merge, en la propia rama y con su sello, porque en `main` no se exige y la rama siguiente lo
heredaría. Es el único commit que el cierre añade a la rama, y se cuenta en la puerta de
`git log --oneline main..trabajo/<rama>`.

**TODO cierre lleva, en ESTE MISMO commit, dos cosas más. Son OBLIGATORIAS aunque la orden de cierre
no las repita** (decisión del consultor del 2026-10-01, `trabajo/ajustes-cierre`; antes solo iban si
la orden las pedía). Van aquí porque en `main`, tras el tag, solo puede cambiar `PROJECT_STATE.md`
(`state check`, regla 5):

1. **El registro del cierre en `docs/state/HISTORIA.md`**, al final del fichero, con el encabezado
   `# Registro de cierre · <rama> (<fecha>)` y, como mínimo:
   - el tag, y el merge escrito como `git rev-parse "stable/<tag>^{commit}"`: su sha todavía no
     existe, y el literal queda después en `Last Stable Commit`;
   - los commits de la rama, con su sha corto y de qué trata cada uno, más este;
   - los runs de la CI, con el commit de cada uno y su resultado (los de la CI de Linux por
     `fix/<rama>`, si la rama se empujó así; si no hubo ninguno, se dice).
2. **La fila de la rama en la tabla de `docs/runbooks/ERRORES-RECURRENTES.md`** («La tabla»), con
   las cuatro columnas: los hallazgos del revisor (cuántos de cada gravedad, dónde están en el
   informe y qué se hizo con ellos), los del consultor, y lo que se le escapó al revisor o lo que hay
   que enseñarle. **Si la orden de cierre no trae los hallazgos del consultor, la sesión los pregunta
   antes de este commit**: no los deduce ni deja la columna en «se apunta al cerrar».
3. **Las entradas de Next Action que la rama deja HECHAS salen de `PROJECT_STATE.md`** y entran al
   final de `docs/state/HISTORIA.md`, con su texto literal, bajo
   `# Next Action HECHA · <letra> · sale de PROJECT_STATE.md en <rama> (<fecha>)`. En
   `PROJECT_STATE.md` no queda ni el resumen ni un «HECHA» (decisión del consultor del 2026-10-02,
   `feature/escenarios-por-sesion`: el cierre no puede pasar de 25 KB). Si la rama no cierra ninguna,
   este punto no toca nada.

El commit se llama siempre `chore(cierre): sale el contrato y entra el registro en HISTORIA`.

```
git branch --show-current
git rm contrato.yaml
git add docs/state/HISTORIA.md docs/runbooks/ERRORES-RECURRENTES.md
git add PROJECT_STATE.md   # solo si el punto 3 sacó alguna entrada de Next Action
make check > make-check.log 2>&1
grep "SELLO: make check en verde" make-check.log
rm make-check.log
git commit -m "chore(cierre): sale el contrato y entra el registro en HISTORIA"
```
→ **Puerta:** la rama es la de trabajo; `git status --short` da `D  contrato.yaml`,
`M  docs/state/HISTORIA.md` y `M  docs/runbooks/ERRORES-RECURRENTES.md` (las tres en la primera
columna), más `M  PROJECT_STATE.md` si el punto 3 sacó algo; y `make check` dice
`CONTRATO: sin contrato.yaml`. Sin contrato, `make check` no comprueba
nada del contrato, así que este sello es el de siempre.

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

**La sesión edita SOLO `PROJECT_STATE.md`**, **sin estadiar** y sin commitear, y en él SOLO las
líneas de cabecera: Current Branch (`main`), Current Feature, Stable Main State, Next Action y Last
Stable Commit. **Desde el 2026-10-01 (`trabajo/dieta-y-skills`) se SUSTITUYE lo que deja de ser
verdad, sin «Lo anterior:»**: lo de antes ya está en `docs/state/HISTORIA.md`, y la rama siguiente
archiva allí este `PROJECT_STATE.md` al abrirse (`docs/state/README.md`). **En el commit de estado no
se añade NADA a Change Log ni a Completed Features**, aunque la orden no lo repita: la historia del
cierre vive en el registro de HISTORIA que entró con el contrato (arriba). Decisión del consultor
del 2026-10-01 (`trabajo/ajustes-cierre`); hasta entonces este runbook decía que Completed Features
ganaba una línea y Change Log una entrada. `PROJECT_STATE.md` no pasa de 25 KB
(`tests/unit/test_project_state.py`, dentro de `make check`): si lo pasara, `make check` sale en
rojo y no hay sello, así que se acorta lo sustituido, no se archiva en `main` (regla 5). **Una
entrada de Next Action que esta rama dejó HECHA ya salió en la rama** (punto 3 de arriba): aquí no se
marca HECHA ni se resume.

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
git push --atomic origin main stable/<tag>
```
→ **Puerta:** termina sin error y lista los dos refs, `main` y el tag. Solo se ejecuta con el commit
hecho. **Desde el 2026-10-01 Claude Code pide confirmacion antes de este push** (regla `ask` de
`.claude/settings.json`, `trabajo/guardias-claude`): es lo esperado, y se confirma solo con la orden
de cierre dada. **`main` y el tag van SIEMPRE en el mismo push `--atomic`** (corrección 8): o llegan los dos,
o ninguno.

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

Si la rama se empujó como `fix/<rama>` para la CI de Linux («Antes del merge: la CI de Linux»), su
rama remota se borra también aquí, con la CI en verde: `git push origin --delete fix/<rama>` (en
texto y no en bloque, como el push de la rama: `tests/unit/test_push_atomico.py`).
→ **Puerta:** `git ls-remote --heads origin fix/<rama>` sale vacío. La guardia de Claude Code solo
deja borrar así ramas `trabajo/`, `feature/` o `fix/`, nombradas una a una; `main`, un tag o un
borrado que mezcle alguno de ellos los bloquea entero (`trabajo/dieta-y-skills`).

## Si la CI sale roja

No se revierte `main`. Se mira que fallo y se arregla con un commit encima, con el mismo orden:
estadiar el arreglo, `make check > make-check.log 2>&1`, comprobar el `SELLO`, `rm make-check.log`,
`BOTSITO_ALLOW_MAIN=1 git commit` y el push, que ahí es solo `git push origin main` porque no hay tag
nuevo.

**Eso vale solo si el arreglo toca `PROJECT_STATE.md` y nada más** (medido el 2026-09-29 y otra vez
el 2026-10-01, al cerrar `trabajo/guardias-claude`). `state check` (regla 5) no admite en `main`,
después del último tag `stable/*`, commits que toquen otra cosa: un arreglo de código encima de
`main` vuelve a poner la CI en rojo. Ese arreglo va por una rama corta, con su merge, su tag y su
commit de estado, y eso es otro cierre: necesita su propia orden de cierre. La rama que se estaba
cerrando no se borra hasta que la CI esté en verde.

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
