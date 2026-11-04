---
status: ACTIVE
date: 2026-11-04
phase: post-F14 (rama `trabajo/guardia-g1`, carril G.1 de la hoja de ruta)
---

# 0088 · Los nombres de dentro del holdout se cuentan, no se listan

> **DECISIÓN DEL CONSULTOR** del 2026-11-04 (respuesta a la PARADA de la fase 0 de
> `trabajo/guardia-g1`, puntos 0 y 1; docs/validation/GUARDIA-G1.md §1.e). No enmienda ADR-0021 ni
> ADR-0033: los dos dicen qué es ABRIR un holdout, y esto no lo es.

## Decision

1. **Listar los nombres de dentro de `knowledge/cases/holdout/{1,2,3}` no es abrir** (ADR-0021 §1:
   abrir es leer etiquetas o medir una cifra del bot sobre esos días; ADR-0033 §1: «listar nombres
   no cuenta»), **pero es una exposición de proceso que la sesión no hace: se cuenta, no se
   imprime.**
2. La condición es el ALCANCE, no la herramienta ni el filtro: no se ejecuta ningún listado cuya
   salida contenga un nombre de dentro de esas tres carpetas -nombrando una de ellas o algo de
   dentro, recorriendo una carpeta que las contiene, o con un comodín que llegue dentro-, aunque un
   filtro detrás quite esas líneas (el filtro va después de listar, y la lista ya se hizo). El
   recuento sí: una salida que es solo un número.
3. Medir o hashear un fichero NOMBRADO en el propio comando sigue permitido (su nombre ya está
   escrito), igual que contar y la CLI del proyecto (`botsito corpus inventory`, `kit build`,
   `casos_reservados`), que es la puerta.
4. La guardia de Claude Code lo hace cumplir (`.claude/hooks/guardia.py`, `R_LISTADO`); CLAUDE.md,
   «Las guardias de Claude Code», dice que deja «contarlo, medirlo y hashearlo por la CLI».

## Problema que resuelve

Cuatro ramas seguidas listaron la carpeta madre del holdout con un filtro detrás (`git ls-files
knowledge/cases | grep -v ...`; docs/runbooks/ERRORES-RECURRENTES.md, filas de
`trabajo/activacion-a42`, `trabajo/cases-rejilla` y `trabajo/entorno-code`), la cuarta vez el propio
revisor. La lección se escribió en ERRORES-RECURRENTES y en la skill `fase-cero`, pero ningún ADR la
sostenía y la guardia, que citaba ADR-0021 §1 para dejar listar, no la veía. CLAUDE.md pide para una
prohibición sin ADR «o se corrige aquí o se cambia el ADR».

## Alternativas consideradas

1. La guardia cita la respuesta del consultor y la lección, y el ADR queda como deuda.
2. No se niega: se rebaja la lección.
3. Negar solo el listado de la madre CON un filtro detrás.

## Por que elegimos esta opcion

Es lo que CLAUDE.md pide para una prohibición sin ADR, cuesta un fichero, y nombra la condición (el
alcance) y no los casos. Es la cuarta exposición.

## Por que descartamos las demas

1. Una regla de la guardia más estricta que su ADR es el patrón que CLAUDE.md dice que ya ha costado
   tres veces.
2. Cuatro repeticiones dicen que la advertencia no basta.
3. `git ls-files knowledge/cases` a secas, `ls -R` o un Glob imprimen los mismos nombres sin filtro.

## Impacto

- `.claude/hooks/guardia.py`: `R_LISTADO`, `Politica.lista_dentro_del_holdout`,
  `_lista_nombres_del_holdout` (Bash), `_patron_lista_el_holdout` (Glob y comodines) y
  `_powershell_lista_el_holdout`; `COMO_REESCRIBIR` deja de mandar `ls` para lo protegido.
- `tests/unit/test_guardia_claude.py`: `git ls-files` sin rutas y `find . -exec sha256sum {} +`
  pasan a negarse (`test_listar_desde_la_raiz_imprime_los_nombres_del_holdout_y_se_niega`).
- Lo que no cambia: un listado no es una exposición que se declare en HOLDOUT-EXPOSICIONES
  (ADR-0021 §4 sigue igual), y la CLI del proyecto no pasa por esta regla.

## Fecha / fase

2026-11-04 · `trabajo/guardia-g1` (carril G.1 de la hoja de ruta).

## Estado

ACTIVE
