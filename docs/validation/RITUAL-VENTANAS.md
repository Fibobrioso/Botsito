# El ritual y sus ventanas

Rama `trabajo/ritual-ventanas`, 2026-09-22. Solo toca documentación: `docs/runbooks/RITUAL.md`,
`CLAUDE.md` y `PROJECT_STATE.md`. No cambia código, tests ni `knowledge/`, y no hay ADR.
El objetivo es que el runbook diga lo que de verdad se ejecuta, para que `PROJECT_STATE.md` deje de
tener que corregirlo. Es el patrón 5: lo escrito y lo ejecutado se separan.

## 1. Qué se midió: las ventanas de `state check`

**Cómo se midió.** Un `git clone` local del repositorio en la carpeta de trabajo de la sesión,
fuera del repo, con `main` en `9fab546`. En el clon:
- se creó una rama `trabajo/prueba` con un único commit que añade `docs/runbooks/README-prueba.md`;
- se fusionó en `main` con `merge --no-ff`, se le puso el tag `stable/F14-prueba` y se editó solo
  la línea de `Last Stable Commit`, sin estadiar;
- en cada ventana se corrió `uv run botsito --repo <clon> state check`.

El clon **está borrado**. Se midió dos veces el mismo día con el mismo resultado; la segunda sin
recortar la salida.

| ventana | momento | exit | mensaje exacto |
|---|---|---|---|
| **A** | tras el merge, antes del tag | 1 | `ERROR: main tiene cambios sin tag estable desde stable/F14-mayo-dev: docs/runbooks/README-prueba.md (en main, tras el tag, solo puede cambiar PROJECT_STATE.md; el HANDOFF y cualquier otro fichero entran por una rama con su tag: MASTER_PLAN §F)` |
| **B** | tras el tag, antes de editar `PROJECT_STATE.md` | 1 | `ERROR: 'Last Stable Commit' dice '48075f6'; el tag stable/F14-prueba apunta a 810043c` |
| **C** | `PROJECT_STATE.md` editado y sin commitear (` M PROJECT_STATE.md`) | 0 | `OK: rama 'main' - funcionalidad actual: …` |

**Conclusión:** `state check` lee el fichero del disco, no el commit. El tramo en el que falla por
diseño termina al **editar** `PROJECT_STATE.md`, no al commitearlo, así que en la ventana C un
error es **real**. Hasta el 2026-09-22 A y B estaban solo deducidas de `cli.py`, y C medida una vez.
La ventana C también se comprobó en el cierre real de `trabajo/mayo-dev-ingerido`.

## 2. Qué cambió en `RITUAL.md`, y por qué

- **Las líneas 67 y 78** decían que `state check` falla a propósito «entre el merge y el
  `docs(state)`». Eso enseñaba a ignorar justo el caso C. Ahora hay una sección con las tres
  ventanas medidas, y el bloque marca en qué paso cae cada una. `state check` solo se corre en la C.
- **El bloque sigue el orden que se ejecutó** en el cierre de mayo:
  1. `status` vacío;
  2. `log main..<rama>`;
  3. merge, tag y `rev-parse`;
  4. edición sin estadiar;
  5. `add`, `diff --cached` y `status --short` con `M  PROJECT_STATE.md`;
  6. `state check`;
  7. commit;
  8. `make check && push` en una línea;
  9. `ls-remote` del tag, con la nota de que el sha es el del objeto tag anotado y el del commit sale
     con `^{commit}`;
  10. `curl` con `in_progress`/`queued` y `422`;
  11. `branch -d`.
- **La «puerta 2» desaparece** (corrección 6, «ninguna comprobación que pase siempre»). Era
  `git diff --stat stable/<tag>..HEAD` justo después del tag. Tras el tag, `HEAD` es el commit del
  tag, así que compara un commit consigo mismo y sale vacía siempre. Medido:
  `git diff --stat stable/F14-mayo-dev..48075f6` da 0 líneas. Además, un diff entre commits no ve
  lo estadiado.
- **La corrección 2 se actualiza a `&&` en una línea.** El runbook describía un `if` de tres líneas,
  pero el cierre de mayo se ejecutó con la cadena `&&`, que hace lo mismo. Dejarlo así habría sido
  otra vez el patrón 5 dentro del mismo documento.

## 3. La regla de los briefs, en `CLAUDE.md`

Next Action 5 dejaba sin colocar esta extensión: *«toda afirmación del consultor sobre cómo se
comporta un mecanismo se mide antes de escribirla en ningún documento»*. Ahora está en
`CLAUDE.md`, «Como se trabaja», junto a «se contesta MIDIENDO, no razonando» (`4747d25`). **La
segunda mitad no estaba en Next Action 5**: *«si la medida la contradice, gana la medida y se dice
con su nombre»*. La añadió el consultor al colocarla. Next Action 5 pasa a hecha (`c5198dc`).

## 4. El patrón 5: instancias sexta y séptima

- **Sexta, compartida.** El consultor escribió la «puerta 2» en el runbook en `4880079` (rama
  `trabajo/lo-que-no-cabia-en-main`). La sesión la copió sin medirla al bloque del ritual de mayo. Es
  una comprobación que no puede fallar, escrita como si parara algo.
- **Séptima, de orden y sin daño.** En el cierre de mayo, `git diff --cached --name-only` y
  `git status --short` se corrieron **antes** del `git add`. Salió vacío y ` M` en la segunda
  columna. **La propia comprobación lo delató**, porque con el fichero sin estadiar no puede dar la
  línea esperada, y se repitió en orden.

Las dos están anotadas en `PROJECT_STATE.md`, Technical Debt. **Lo que no está en esa lista:** la
instancia del trailer `Fuente:` con un sha, cuando el brief lo pedía y el trailer solo admite
`ev-*`, `fb-*` y `ADR-NNNN`. Vive solo en `MAYO-DEV.md` §5.

## 5. Inconsistencia anotada, sin corregirla hacia atrás

**La rama «Reglas de la casa»** (`stable/F13-reglas`, 2026-09-17), que tampoco tocaba código, **cerró
sin informe en `docs/validation/`**. `CLAUDE.md` dice «un informe por rama», y `state check` no lo
vigila: dio OK en esta rama antes de que este informe existiera. No se escribe ahora el informe que
le faltó.

## 6. Cierre

`state check` OK. `make check` en verde (804 tests, 4 contratos de importación), con el log borrado.
`kit check --sesion 2026-09-09-sesion-01` idéntico a la línea base. PREREGISTRO con blob
`52649183…` y cero autorizaciones.

## Estado

WAITING_FOR_USER_VALIDATION
