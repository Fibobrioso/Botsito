---
name: fase-cero
description: Hace la fase 0 de un encargo de Bot v3 -inventario medido en el repo, el encargo contrastado por el auditor, y la PARADA con las decisiones para el consultor- y, cuando llega su respuesta, la copia tal cual y la aplica punto por punto. Usala cuando un encargo pide «FASE 0», un inventario o una PARADA antes de escribir codigo, y cuando llega la respuesta del consultor a esa PARADA.
argument-hint: "<rama>"
---

# fase-cero

Una fase 0 existe para que el consultor decida sobre lo MEDIDO y no sobre lo supuesto. Esta skill
dice el orden y las puertas; las reglas viven en `CLAUDE.md` («Que se puede mirar y que no»,
«Como se trabaja»), `docs/runbooks/MIRAR-EL-MATERIAL.md` y `docs/runbooks/ERRORES-RECURRENTES.md`.
Si esta skill y esos ficheros discrepan, ganan ellos y se dice en el informe.

## Entradas

| Entrada | De donde sale | Si falta |
|---|---|---|
| El encargo | `docs/encargos/<rama con - en lugar de />.md` | sin el no se empieza: la rama se abre con `abrir-rama` |
| Los puntos a inventariar (a, b, c...) | el encargo, seccion FASE 0 | se pregunta |
| Cuando parar | el encargo: por defecto se para; si dice «no pares: sigue, salvo que...» o es tarea nocturna, se para solo en sus condiciones | se para |
| El informe de la rama | el `artefacto` de `contrato.yaml` | se pregunta |
| El tramo de la rama | el `tramo` de `contrato.yaml`, en `docs/plan/HOJA-DE-RUTA.md` | se pregunta |

## Limites

- **Ni una linea de codigo, spec, knowledge ni parametros** antes de la respuesta, salvo lo que la
  propia FASE 0 del encargo mande escribir (un manifiesto congelado, un test de medida), declarado
  en el informe.
- **Holdout, sin excepciones:**
  - nunca se lista una carpeta que contenga meses reservados, ni su carpeta madre con un filtro
    detras: las rutas se nombran literales EN EL PROPIO COMANDO
    (`git ls-files knowledge/cases/dev knowledge/cases/kit`, no `git ls-files knowledge/cases | grep ...`);
  - lo que pueda contener dias reservados se mide por RECUENTO (`grep -c`, `grep -L`, `wc -l`) y
    sin imprimir contenido ni fechas; `casos_reservados(repo)` se cuenta por mes y no se imprimen
    sus claves;
  - antes de abrir material de desarrollo, `casos_reservados` comprueba que no tiene dias
    reservados (`CLAUDE.md`);
  - ningun agregado de un rango con dias reservados, ninguna captura de Analytics, nada en
    cuarentena ni en tramos no citables;
  - la columna de fechas de un backtest no la lee la sesion ni el auditor: la lee Aleks, una vez
    y antes del sorteo (ADR-0072; `CLAUDE.md`, «Que se puede mirar y que no»); si la fase 0 la
    necesita, es motivo de PARADA;
  - toda exposicion, aunque sea dudosa, se declara el MISMO DIA en
    `docs/validation/HOLDOUT-EXPOSICIONES.md` y en el informe.
- **Una guardia no se rodea.** Si bloquea una medida legitima, es un hallazgo **importa** en el
  informe, con una entrada propuesta para la Next Action que la corrija en su rama; no se reescribe
  el comando para que no la vea.
- **La ayuda de un comando se lee en `src/botsito/cli.py`**, no ejecutando `--help`.
- **Lo que no se puede medir no se afirma**: va en «Lo que no pude medir», con el motivo.

## Herramientas

Read, Grep, Glob y Bash de solo lectura (git de lectura, `uv run python -c` sin escritura,
`uv run pytest <fichero>` de tests concretos), el subagente `auditor-encargo`, y Write o Edit solo
para el informe y lo que la FASE 0 mande escribir.

## El recorrido

1. **Leer el encargo entero**, y las respuestas o añadidos del consultor que ya tenga al final.
2. **Auditarlo antes de usarlo**: lanzar el subagente `auditor-encargo` con la rama. Cada
   afirmacion INCORRECTA o con MATIZ y cada herencia no recogida van al informe en «El encargo
   frente al repo», con su evidencia, y se trabaja con lo medido. Si una cambia lo que se pide, es
   motivo de PARADA aunque el encargo no la prevea.
3. **Inventariar punto por punto**, en el orden del encargo. Cada hallazgo con `fichero:linea` o
   el comando y su salida recortada a lo que demuestra. Cada cifra, contada contra su fuente en
   esta sesion; si la publica mas de un informe, se cita el mas reciente y se dice que hay otro.
4. **Contrastar reglas con su ADR.** Toda regla que el inventario o el encargo usen se busca en el
   ADR del que sale; si no coinciden, manda el ADR y se dice (`CLAUDE.md`, «Una prohibicion escrita
   aqui que no salga de un ADR»).
5. **Escribir la seccion de decisiones**, con esta forma exacta:

   ```
   ## Lo que necesito que decidas
   0. <tema>. Opciones: (a) ... (b) ... Recomiendo (a): <porque en una linea>. Coste de (b): <...>.
   1. ...
   ```

   Una decision por punto, numerada desde 0, con opciones, recomendacion y porque. Nunca «lo que
   veas»: si ninguna opcion es recomendable, se dice por que.
6. **Sellar y commitear**: `uv run botsito knowledge validate` primero si se toco `knowledge/`;
   despues `make check > make-check.log 2>&1` (exit 0, ningun `failed`, `SELLO`) y commit del
   informe (con `HOLDOUT-EXPOSICIONES.md` si toca).
7. **PARAR, salvo que el encargo diga cuando seguir** (y entonces se sigue y se para solo en sus
   condiciones, dicho en el informe). El mensaje a Aleks cabe en una pantalla: que se midio (de
   tres a seis lineas), lo que cambia respecto al encargo, la lista numerada de decisiones con la
   recomendacion, y «Espero tu respuesta a la PARADA».

## Cuando llega la respuesta del consultor

1. **Copiarla TAL CUAL al final de `docs/encargos/<rama con - en lugar de />.md` y en el informe**,
   en «Respuesta del consultor a la PARADA», con su fecha. Sin resumir ni corregir.
2. **Aplicarla punto por punto.** Por cada punto numerado: hecho, o PARADA nueva si al aplicarlo
   algo medido lo contradice (un test que dejaria de pasar, un contrato de capas, un fichero
   congelado). Una PARADA nueva lleva el formato del paso 5 y se numera (PARADA 2, 3...). Nunca se
   ajusta en silencio una decision del consultor.
3. Si la respuesta no contesta a un punto de «Lo que necesito que decidas», se pregunta ANTES de
   seguir.

## Artefacto

El informe de la rama con: el inventario por punto, «El encargo frente al repo» (con el informe del
auditor), «Lo que no pude medir», las exposiciones declaradas (o «ninguna»), «Lo que necesito que
decidas», y despues cada respuesta del consultor tal cual.

## Verificacion

- `git diff main --stat` en la PARADA: el informe, el encargo, el contrato, `PROJECT_STATE.md`,
  `docs/state/HISTORIA.md`, `HOLDOUT-EXPOSICIONES.md` si toca, y lo que la FASE 0 mande escribir.
- Cada punto de la FASE 0 del encargo tiene su seccion en el informe.
- Toda ruta del inventario se nombra literal en el comando que la mide.
