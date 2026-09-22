# Lo que no cabía en main

Rama `trabajo/lo-que-no-cabia-en-main`, desde `c5f67a7`. Sin merge, sin tag, sin push.

**Esta rama no mide nada: corrige el cierre de la anterior.** Es corta a propósito y no toca
`knowledge/`, ni datos, ni código.

## De dónde sale

**De un fallo del consultor, y de que la sesión lo obedeciera sin contrastarlo con lo escrito.**

El 2026-09-22, al cerrar `stable/F14-caja`, el brief decía: *«si están en un sitio que no es
PROJECT_STATE.md, va igual en este commit»*. **Eso contradice MASTER_PLAN §F**, que dice que tras el
tag, en `main`, sólo puede cambiar `PROJECT_STATE.md`; lo demás entra por una rama con su tag.

**La sesión conocía la regla y la escribió igual.** No la contrastó. Es el mismo defecto que este
proyecto lleva la semana entera señalando en otros sitios —obedecer una instrucción sin cruzarla con
lo que ya está decidido— y esta vez el que lo cometió fue quien lo señalaba.

**Lo paró `botsito state check`**, con su motivo completo. Pero lo paró **tarde**, y de ahí las tres
correcciones.

## (a) La nota de vuelta en ADR-0038

Entra íntegra —**no reconstruida de memoria**, que era el riesgo que su anotación nombraba— en
recuadro, justo antes de `## Problema que resuelve`, sin tocar el cuerpo. Cierra el cruce en los dos
sentidos: el patrón 4 de `PROJECT_STATE.md` nombra la decisión 3 del ADR, y ahora el ADR apunta de
vuelta al patrón.

## (b) El hueco del ritual estaba en DOS sitios, no en uno

**Una corría tarde y la otra no frenaba nada.**

**`state check` corría DESPUÉS del commit**, dentro de `make check`. Medido: el error disparó sobre
el **árbol de trabajo**, con el fichero modificado y **sin commitear** —así que corriéndolo antes,
el cambio que rompía la regla **no habría entrado nunca** ni en el historial ni en `origin`—. Ahora
es una puerta explícita **antes** del commit.

> **Con un matiz que hay que leer, porque si no la puerta se ignora:** entre el merge y el
> `docs(state)`, `state check` **falla a propósito** —`PROJECT_STATE.md` todavía describe la rama
> como pendiente—. **Pero acumula los errores y los imprime todos**: medido en `cli.py:state_check`,
> que hace `errores.append(...)` y un bucle al final, **sin cortocircuito**. Así que **cualquier
> otra línea de error es real**, y hay que leerlas todas, no la primera.

**`make check` no condicionaba el push**: imprimía el código de salida, borraba el log y empujaba
igual. Ahora el push es una rama del `if`, y **el log se queda cuando falla**, que es cuando hace
falta leerlo.

**Y una tercera puerta que ya existía y se saltó.** El runbook decía desde el 2026-09-17:
`git add PROJECT_STATE.md` y `git diff --cached --name-only` → **SOLO `PROJECT_STATE.md`**. **Esa
puerta habría bastado.** Lo que falló es que se estadió con **`git add -A`** y no se miró la salida.
Por eso la corrección nueva no es una puerta más, sino **nombrar el fichero**: hace innecesario
acordarse de mirar.

**El resumen, con fecha y sin adornos:** el 2026-09-22 un commit que `state check` rechazaba llegó a
`origin` con la CI en rojo, y **ninguna de las tres comprobaciones pudo pararlo** —una corría tarde,
otra no frenaba nada, y la tercera no se ejecutó como estaba escrita—.

## (c) Los comandos, como se invocan de verdad

**Por qué no es cosmético: dentro de un bloque pegado, un `command not found` es indistinguible de
una comprobación que pasa.** Imprime su error y la línea siguiente se ejecuta igual. El 2026-09-22
`botsito state check` a secas dio `command not found`.

**Revisado el runbook entero**, no sólo ese caso. Los comandos que aparecen son `git`, `make`,
`curl` y ahora `uv run botsito`. **El que estaba mal es el `curl`:**

```
ANTES:  curl -s https://api.github.com/...
AHORA:  curl -s --ssl-no-revoke https://api.github.com/... | grep -o '"status"...'
```

**`--ssl-no-revoke` hace falta en esta máquina y sin él `curl` falla** — llevaba mal desde que se
escribió el runbook el 2026-09-17, y nunca se notó porque quien lo ejecutaba lo añadía de memoria.
Se añade también el `grep`, porque la salida cruda son cientos de líneas de JSON y la puerta es una
palabra. Y queda dicho que **un `"status": "422"` no es un fallo de la CI: es GitHub diciendo que no
conoce ese commit**, o sea que el push no se ha hecho.

## La frase general, y lo que NO decido

> **UNA COMPROBACIÓN QUE NO PUEDE PARAR NADA NO ES UNA COMPROBACIÓN; UNA QUE CORRE DESPUÉS DEL PASO
> QUE VIGILA, TAMPOCO; Y UNA QUE NI SIQUIERA SE EJECUTA SE PARECE DEMASIADO A LAS DOS ANTERIORES.**

Las tres se midieron el mismo día sobre el mismo incidente: `make check` no frenaba, `state check`
corría tarde, y `botsito` a secas no existía.

**No la meto en la lista de patrones por mi cuenta.** Encaja como cara nueva del **patrón 3** —*una
regla que enumera los casos en vez de nombrar la condición*— porque las tres comparten que **la
comprobación existía y no cubría el caso**; pero también podría ser un patrón propio, porque el
defecto no está en **lo que la regla dice** sino en **cuándo y si se ejecuta**, que es otra
dimensión. **Lo decide el consultor.**

## Qué debe decidir el usuario

1. **Validar la rama** y, si procede, el ritual.
2. **La frase general**: cara nueva del patrón 3, patrón propio, o ninguna de las dos.
3. **La ambigüedad que queda en `PROJECT_STATE.md`**, y es de una línea: `Current Feature` dice que
   lo siguiente es `trabajo/mayo-dev-ingerido`, y el Next Action 5 reservaba **la primera rama** para
   ésta. Al cerrarse ésta, las dos frases vuelven a ser compatibles — pero conviene que el
   `docs(state)` de este cierre lo deje dicho sin que haya que deducirlo.

## Estado
WAITING_FOR_USER_VALIDATION
