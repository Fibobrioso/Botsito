---
status: ACTIVE
date: 2026-09-03
phase: F01
---

# 0001 · Estructura del repositorio y regimenes de cambio

## Decision
Un solo repositorio con cuatro zonas: `knowledge/` (datos versionados: evidencia, feedback,
especificacion, casos), `src/botsito/` (Python de referencia con `domain/` puro), `mql5/`
(ejecucion, con parametros generados desde `knowledge/spec/`) y `docs/` (plan, ADR, informes de
validacion, especificacion generada). Tres regimenes de cambio, cada uno con un mecanismo que lo hace
cumplir: evidencia inmutable (hook), feedback solo-anadir (hook), spec y casos versionados con cita
obligatoria (test sobre el diff). `knowledge/cases/holdout/` es ilegible para `spec/` y `domain/`
(guarda en tests). `domain/` no importa IO, reloj ni MetaTrader (import-linter + test AST).

## Problema que resuelve
La arquitectura aprobada distingue evidencia original, conocimiento confirmado por el experto y
especificacion derivada, y exige dos implementaciones (Python y MQL5) que lean la misma fuente. Sin una
estructura que separe estos contenidos y sin mecanismos automaticos, las reglas dependen de la memoria
de cada sesion de IA y se degradan.

## Alternativas consideradas
1. Dos repositorios (Python y MQL5) — descartada.
2. Conocimiento dentro de `src/` como modulos Python — descartada.
3. Evidencia y feedback en la misma carpeta con un campo `tipo` — descartada.
4. Reglas de pureza solo documentadas en CLAUDE.md o README — descartada.

## Por que elegimos esta opcion
El contrato entre Python y MQL5 (parametros y casos) debe cambiar en el mismo commit; un `diff` de
`strategy_spec.yaml` es un cambio de negocio visible y auditable; los regimenes distintos exigen
mecanismos distintos; y un contrato de importacion que falla en rojo sobrevive a la sesion 40, una
frase en prosa no.

## Por que descartamos las demas
(1) Dos repos permiten que spec y EA diverjan sin que nadie lo vea. (2) Conocimiento como codigo mezcla
regimen de cambio de datos con el de software y lo hace ilegible para el trader. (3) Una sola carpeta
no permite hooks con reglas distintas por ruta. (4) Sin mecanismo, la regla es una intencion.

## Impacto
Arbol fijado en `docs/plan/MASTER_PLAN.md` §B; contratos en `pyproject.toml [tool.importlinter]`;
tests en `tests/contract/`. Los hooks de inmutabilidad y solo-anadir se activan en F06 y F09; la guarda
de holdout en F14.

## Fecha / fase
2026-09-03 · F01

## Estado
ACTIVE
