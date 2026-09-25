# Blindaje: la puerta del commit y el índice de ADR

Rama `trabajo/blindaje`, 2026-09-25. Sin merge, sin tag y sin push. Next Action 24: dos guardias que
hasta hoy dependían de que alguien se acordara.

Guardas verificadas al empezar: `docs/validation/PREREGISTRO.md` con blob `52649183…`, el declarado;
cero ficheros `docs/validation/AUTORIZACION-*`. Nada del material de septiembre, mayo ni febrero.

## 1. Cómo estaba

- **El hook estaba versionado y se instalaba por copia.** La fuente es `scripts/git-hooks/pre-commit`
  (ADR-0003) y `make hooks` (`scripts/instalar_hooks.py`) lo copia a `.git/hooks`; no hay
  `core.hooksPath`. El motivo, en `scripts/git-hooks/README.md`: «con una ruta relativa, git busca
  el hook en la rama actual; si la rama no contiene el fichero [...] git lo omite en silencio y el
  commit pasa». La copia instalada era idéntica a la versionada (`diff` vacío).
- **Qué hacía:**
  - rechazaba el commit directo en `main` sin `BOTSITO_ALLOW_MAIN=1`;
  - rechazaba editar los `*.yaml` inmutables;
  - exigía `uv lock --check` y `lint-imports`.

  Nada miraba si el árbol había pasado `make check`.
- **`make check`** era `lint types contracts test state config knowledge` (`Makefile`): ruff, mypy,
  import-linter, pytest, `state check`, `config validate` y `knowledge validate`, en serie, parando
  en el primero que falla.
- **El ritual iba en este orden:** `BOTSITO_ALLOW_MAIN=1 git commit` y, después,
  `make check > make-check.log 2>&1 && rm make-check.log && git push …` (`RITUAL.md`, antes de esta
  rama). Todo lo que protegía del commit en rojo era la disciplina: `40759cb` (2026-09-23) y
  `2753ac1` (2026-09-25, rehecho con `--amend` antes de seguir) entraron con `make check` en rojo.

## 2. La puerta

- **El sello** (`scripts/sello_make_check.py`). `make check` empieza por `desellar` y termina con
  `sellar`, y `make` para en el primer objetivo que falla, así que el sello solo se escribe con todo
  en verde. `.NOTPARALLEL:` asegura ese orden aunque alguien use `-j`.

  El sello es el hash de `git write-tree`, el árbol del ÍNDICE. Vive en `git rev-parse --git-path
  botsito-sello`, dentro del directorio de git, que git nunca sigue.

  **No se sella** si hay cambios sin estadiar o ficheros sin seguir fuera de `.gitignore`: lo avisa,
  lista cuáles y deja `make check` en verde. El hook rechazará el commit.
- **`make-check.log` pasa a `.gitignore`**, y a la lista cerrada de ignorados de
  `test_repository_integrity.py`. Sin esto, la salida que CLAUDE.md manda escribir a fichero
  impediría sellar siempre.
- **Los hooks.** `pre-commit` compara su `git write-tree` con el sello, justo después de la regla de
  `main`, que no cambia. El nuevo `pre-merge-commit` hace lo mismo sin mirar la rama. El bloque es
  idéntico en los dos, entre marcadores, y un test lo comprueba. Al rechazar dicen:
  - si no hay sello o si el sello es de otro árbol;
  - qué ejecutar: `make check > make-check.log 2>&1`;
  - que `--no-verify` está prohibido;
  - en el merge, cómo salir.
- **Ninguna vía de escape nueva.** La única variable sigue siendo `BOTSITO_ALLOW_MAIN`, y un test lo
  comprueba. `CLAUDE.md` prohíbe `--no-verify` de forma explícita, en commit y en merge.

### Qué cubre y qué no, medido con git 2.55.0 en repos temporales

| operación | ¿pasa por la puerta? | medido |
|---|---|---|
| `git commit` | sí, `pre-commit` | tests |
| `git commit -a` | sí: `git write-tree` usa el índice temporal que git va a escribir | test |
| `git commit --amend` | sí: el árbol es el enmendado | medido y test |
| `git merge --no-ff` sin conflictos | sí, **`pre-merge-commit`**. El README de los hooks decía que no existía, y era falso desde git 2.24 | medido y tests |
| `git merge` con conflictos | se cierra con `git commit`, que pasa por `pre-commit` | medido |
| `git cherry-pick` | **no**: crea el commit sin `pre-commit` | medido |
| `git rebase` (motor merge y `--apply`) | **no**: reescribe sin `pre-commit` | medido |

`cherry-pick` y `rebase` no se usan para meter trabajo (`CLAUDE.md`). La garantía de fondo sigue
siendo la CI.

**El merge rechazado.** Queda a medias (`MERGE_HEAD`). En `main` **no se puede sellar a mitad de
merge**, porque `PROJECT_STATE.md` todavía declara la rama de trabajo y `state check` falla por
diseño (ventana A). La salida es:
- `git merge --abort`;
- `make check` en la rama que se fusiona;
- repetir el merge.

La primera versión de esta rama decía otra cosa y se corrigió en la pieza 3.

## 3. El índice de ADR

`tests/unit/test_adr.py` comprueba que la sección «Architectural Decisions (index)» de
`PROJECT_STATE.md` lista EXACTAMENTE los ADR de `docs/adr/`, sin la plantilla `0000`: ni falta, ni
sobra, ni se repite ninguno. Lleva su prueba sobre un índice sintético. Aplicado en memoria al
`PROJECT_STATE.md` real sin la línea de ADR-0045, lo caza: «existen en docs/adr/ y faltan en el
indice: ['0045']», que es el K-01 de la sesión 02.

## 4. El ritual nuevo

`docs/runbooks/RITUAL.md`. Desde el `docs(state)`, el orden pasa a ser **estadiar → `make check`
(sella) → commit → push**, porque el hook rechaza un commit sin sello. Con las puertas en el runbook:

```
git add PROJECT_STATE.md
git diff --cached --name-only
git status --short
uv run botsito state check
make check > make-check.log 2>&1
grep "SELLO: make check en verde" make-check.log
rm make-check.log
BOTSITO_ALLOW_MAIN=1 git commit -m "docs(state): trabajo/<rama>, cerrada en main (stable/<tag>)"
git push origin main
git push origin stable/<tag>
```

El merge tiene su puerta del sello y su salida si se rechaza. `ENTRADA-MARZO.md` y
`SESION-DE-PREGUNTAS.md` llevan el mismo orden: el paso e de marzo declara la lectura antes de
probar, y estadía los casos y la declaración juntos.

## 5. La transición: el primer cierre con la puerta

- **`make hooks` EN ESTA RAMA, antes de `git checkout main`.** Copia los hooks de la rama en la que se
  está. En `main`, antes del merge, instalaría los viejos, sin sello ni `pre-merge-commit`. Una vez:

  ```
  git branch --show-current
  make hooks
  ```

  La rama tiene que ser `trabajo/blindaje`, y `make hooks` tiene que listar `pre-commit` y
  `pre-merge-commit`.
- **El merge pasa sin más:** el último commit de la rama se selló al hacerse, y `main` no se ha
  movido desde `1e1bb0f`. **No se corre `make check` en `main` antes del merge**, porque
  reescribiría el sello.
- **El `docs(state)`** ya sigue el orden nuevo, porque el `Makefile` de `main` sella tras el merge.
- **Los commits de esta rama pasaron por el hook VIEJO**, sin sello, porque la sesión no instala
  hooks en el repositorio del usuario. Aun así, cada uno se hizo tras un `make check` en verde cuyo
  sello es exactamente su árbol:

  | commit | árbol | sello |
  |---|---|---|
  | `ac86865` | `dcc4d1e` | `dcc4d1e` |
  | `2067dfd` | `17f9aff` | `17f9aff` |
  | `252224c` | `a668f9a` | `a668f9a` |

  Este informe, con el mismo criterio.
- **En la CI** `make check` también sella o avisa, sin efecto: allí no se commitea.

## 6. Lo que salió al hacerlo

- **El primer `make check` de la pieza 1 salió en rojo** (`test_no_unexpected_ignored_paths`:
  `make-check.log` no estaba en la lista cerrada de ignorados), y **la puerta funcionó**: no quedó
  sello. Se arregló antes de commitear.
- **Un `make check` de la pieza 3 lo cortó el sistema por memoria.** Se paró sin reintentar, con todo
  estadiado, y se relanzó cuando el usuario lo pidió.

## Estado

WAITING_FOR_USER_VALIDATION. Cierre con el ritual nuevo, y antes `make hooks` en esta rama (§5).
