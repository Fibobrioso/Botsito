---
name: entregar-rama
description: Deja una rama de Bot v3 «lista para revision» -repaso del encargo punto por punto, make check sellado, CI de Linux por fix/<rama> si toca la plataforma, informe completo con su estado, revisor con su alcance y su informe pegado- y da a Aleks el resumen final. Usala cuando el trabajo de una rama esta hecho y el encargo termina en «Rama lista para revision, NO cerrada».
argument-hint: "<rama>"
---

# entregar-rama

El final de toda rama, en un solo recorrido. No cierra nada: el cierre es `cerrar-rama`, y solo con
orden de Aleks. Las reglas viven en `CLAUDE.md`, `docs/runbooks/RITUAL.md` («Antes del merge: la CI
de Linux») y `.claude/agents/revisor.md`; aqui solo el orden y las puertas. La fila de la rama en
`ERRORES-RECURRENTES.md` NO se escribe aqui: la escribe `cerrar-rama`.

## Entradas

| Entrada | De donde sale | Si falta |
|---|---|---|
| El encargo y las respuestas del consultor | `docs/encargos/<rama con - en lugar de />.md` (al final) y el informe | — |
| El informe | el `artefacto` de `contrato.yaml` | se pregunta |
| Si toca la plataforma | el encargo, o el diff: hooks, rutas, sistema de archivos, scripts que dependan del sistema (`RITUAL.md`), y zoneinfo (lo piden los encargos: `docs/encargos/trabajo-cases-rejilla.md`) | en la duda, SI |
| El alcance del revisor | el encargo («Pasa el revisor ... con este alcance») | los dos ejes de siempre |

## Limites

- Ningun commit sin sello; nunca `--no-verify`; nada se reescribe para que una guardia no lo vea.
- **Una desviacion no declarada es un defecto**, aunque el resultado sea mejor: todo lo hecho de
  otra forma o de mas se declara en el informe con su porque.
- El informe no afirma nada que no muestre (`fichero:linea`, comando y salida, o hash).
- Una rama `trabajo/<x>` se empuja como `fix/<x>`, SIN tocar la local, con la forma exacta de
  `RITUAL.md`. Una `feature/*` ya dispara la CI con su nombre.
- **Si el clasificador niega un push**, se da a Aleks el comando exacto para lanzarlo con «!» desde
  su terminal; no se rodea.
- **Si la rama cambia el `Makefile`**, la guardia de Claude Code no deja ejecutar ningun `make`
  (sus recetas son codigo sin revisar: medido en `trabajo/entorno-code`): ese `make check` lo
  lanza Aleks con «!», y se dice en el informe.
- El codigo de `main` se prueba en un clon `--detach` (skill `comparar-con-main`), nunca con un
  checkout en el repo real.

## Herramientas

Bash (git, `make check`, `gh run list` / `gh run view <run> --log-failed` o la API de check-runs
de GitHub con el sha escrito tal cual), Read, Edit para el informe, y el subagente `revisor`.

## El recorrido

1. **Repaso del encargo contra lo hecho.** Parte el encargo, y cada respuesta del consultor, en
   requisitos numerados (cada fase, cada viñeta, cada «test que rompe», cada «NO cambia»). Para
   cada uno: Hecho / Parcial / No hecho / Hecho de otra forma, con evidencia. Lo Parcial y lo No
   hecho se terminan o se declaran con su motivo ANTES de seguir. Esa tabla va al informe
   («El encargo, punto por punto»).
2. **Lo que NO cambia**: `git diff --stat main...HEAD` contra la lista del encargo; un fichero que
   no debia tocarse es un bloqueo. `uv run python scripts/contrato_rama.py` en verde.
3. **Tests que rompen a proposito**: cada uno que pida el encargo, demostrado fallando con el codigo
   de `main` (skill `comparar-con-main`) y pasando con el de la rama; comando y salida al informe.
4. **Informe completo**: fase 0, PARADAS y respuestas tal cual, lo hecho por fase, desviaciones,
   exposiciones declaradas (o «ninguna»), regresion con hashes si la hubo, y `## Estado` sin
   «EN CURSO». Y, preparadas para el commit del contrato del cierre (`RITUAL.md`, puntos 3 y 4),
   las lineas de la Next Action que salen, entran o cambian y las entradas de
   `docs/plan/HOJA-DE-RUTA.md` que cambian (p. ej. la de la rama, HECHA): en la rama no se tocan.
5. **Tamaño de `PROJECT_STATE.md`**: `wc -c PROJECT_STATE.md`; el tope es el de
   `tests/unit/test_project_state.py`, y el saldo de bytes de la rama o el tope que fije el
   encargo, si fija alguno.
6. **Sello y commit**: `git add` de los ficheros nombrados, `uv run botsito knowledge validate` si
   se toco `knowledge/`, `make check > make-check.log 2>&1`, esperar, leer el log (exit 0, ningun
   `failed`, la linea `SELLO`), commit.
7. **CI de Linux, si toca la plataforma** (`RITUAL.md`): `git push origin trabajo/<x>:refs/heads/fix/<x>`,
   esperar el run (como dice el mensaje de la guardia, `trabajo/guardia-ci`: una consulta suelta
   con `gh run view <run>`; si hay que esperar, una espera sin consulta (`sleep` en segundo plano)
   y despues otra consulta suelta) y anotar numero, commit y resultado: con
   `gh run list --branch fix/<x>`, o por
   la API de check-runs con el sha de 40 caracteres escrito tal cual (las ordenes de cierre del
   consultor, `docs/state/HISTORIA.md`), que vale tambien si el clasificador niega lo otro; el
   log de un fallo, con `gh run view <run> --log-failed`. Unico fallo aceptado: `state check` por
   el nombre `fix/`. Cualquier otro se arregla en la rama y se vuelve al paso 6. Un run cancelado
   por tiempo no es resultado: `gh run rerun <run>`. El run que cuenta es el del ULTIMO commit.
8. **Revisor**, con el informe ya terminado: lanzar el subagente `revisor` con la rama y el alcance
   del encargo. Pegar su informe al final del de la rama TAL CUAL, salvo lo que cite de un tramo no
   citable, que se retira diciendo cuantas retiradas. Cada hallazgo **bloquea** o **importa** se
   arregla o se contesta en «Lo que se hizo con los hallazgos del revisor», uno por uno; si se
   arreglo algo, se vuelve al paso 6 (y al 7 si toca la plataforma).
9. **Ultimo commit sellado** y, si toca, el ultimo push a `fix/<x>` con su run en verde.
10. **Frase final** del informe y del mensaje: «Rama lista para revisión, NO cerrada.»

## El mensaje final a Aleks

Cabe en una pantalla, en este orden:
- commits de la rama (sha corto y de que tratan);
- runs de la CI (numero, commit y resultado), o «sin CI: no toca la plataforma» con el motivo;
- el encargo: N requisitos, cuantos hechos, y las desviaciones declaradas en una linea cada una;
- el revisor: cuantos bloquea / importa / menor, y que se hizo;
- lo que pide decidir al consultor, si algo;
- «Rama lista para revisión, NO cerrada.»

## Verificacion

- `git status --short` vacio y el ultimo commit sellado.
- El informe tiene «El encargo, punto por punto», el informe del revisor, sus respuestas y `## Estado`.
- Si toca la plataforma: el ultimo run de `fix/<x>` es del ultimo commit de la rama.
