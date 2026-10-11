---
name: retomar-rama
description: Retoma una rama de Bot v3 tras una sesion nueva, una conversacion compactada o un corte -reconstruye desde el repo en que fase esta, que respondio el consultor y que falta- sin fiarse de la memoria de la conversacion. Usala al empezar a trabajar en una rama ya abierta, o cuando la conversacion se haya resumido.
argument-hint: "[rama]"
---

# retomar-rama

Una conversacion larga se compacta, y lo que se resume se pierde o se deforma. El estado de una rama
vive en el repo; esta skill lo lee en un orden fijo y lo dice en una pantalla. Lo que lee primero
toda sesion esta en `CLAUDE.md`, «Por donde se empieza»; el hook de arranque
(`.claude/hooks/estado_sesion.py`) ya pone delante la rama, el contrato y si se espera al
consultor.

## El recorrido

1. **Donde estoy**: `git branch --show-current`, `git status --short`, `git log --oneline main..HEAD`
   y `git stash list`. Si hay cambios sin commitear, se dicen antes de nada y no se tocan. Y el
   tramo: el `tramo` de `contrato.yaml` y la entrada de `docs/plan/HOJA-DE-RUTA.md` a la que
   pertenece la rama (el `###` de ese tramo con la `NA:` del encargo).
2. **Que me pidieron**: `docs/encargos/<rama con - en lugar de />.md` entero, incluidas las
   respuestas y añadidos del consultor copiados al final.
3. **Que respondio el consultor**: en el encargo y en el informe (el `artefacto` de
   `contrato.yaml`), cada «Respuesta del consultor», «Añadido» y PARADA, en orden de fecha. Una
   PARADA (o un «Lo que necesito que decidas») posterior a la ultima respuesta significa que se
   espera: no se avanza.
4. **Que se hizo**: el informe por fases, y el ultimo `make-check.log` si existe (exit, `failed`,
   `SELLO`).
5. **Que falta**: los requisitos del encargo y de las respuestas sin evidencia en el informe ni en
   los commits.
6. **Decirlo** a Aleks en una pantalla: rama y ultimo commit; fase actual; lo ultimo que decidio el
   consultor; lo que falta, en orden; y si hay algo que pedir antes de seguir. Despues, seguir con
   la skill que toque (`fase-cero`, `activar-sesion`, `comparar-con-main`, `entregar-rama`).

## Limites

- Lo que la conversacion «recuerda» y el repo no muestra no existe: se pregunta.
- Si el informe y los commits no cuadran (el informe da por hecho algo que no esta), se dice como
  hallazgo antes de seguir.
- Si una ejecucion larga murio con «system running low on memory», no se relanza sin permiso
  (`CLAUDE.md`, «Trampas medidas»).
