---
status: ACTIVE
date: 2026-09-14
phase: post-F13 (antes de F18-F22)
---

# 0030 · El motor interpreta la `forma`; las primitivas se escriben a mano

## Decision

1. **El reparto que rige es el de ADR-0019, dicho por escrito**: el motor recorre el árbol genérico
   de `forma` (`todos_de`, `cualquiera_de`, `ninguno_de`, `hace`, `permite`, `prohibe`) y **despacha
   por nombre** a primitivas escritas a mano: una por predicado, una por acción y una por
   acumulador.
2. **F18-F22 no se escriben como módulos aislados.** Se escriben como el conjunto de primitivas que
   ese árbol invoca, más el recorrido. Una regla nueva en la spec no exige código nuevo salvo que
   introduzca un predicado, una acción o un acumulador que no existían.
3. **F29 (MQL5) refleja las mismas primitivas con los mismos nombres** y no traduce el árbol línea a
   línea: la prueba diferencial de F30 compara decisiones, no implementaciones.
4. **El contrato Python↔MQL5 sigue cubriendo parámetros y casos** (ADR-0001), no reglas.

## Problema que resuelve

ADR-0019 decide la forma (predicados con argumentos, ligadura, árbol booleano) y dice que *«F12
valida que el predicado exista, no se duplique y no se contradiga; F22 lo implementa»*. No dice
cómo lo implementa. Mientras tanto, la tabla A de MASTER_PLAN describe F18-F21 como módulos por
tema («Tipos y sesgo H4», «Zonas M15 y mitigacion», «Mapeo M1, breaker, zonas de control»), que es
lenguaje de código a mano, y `strategy_spec.yaml` dice que *«el motor de F22-F23 implementa esta
lista y ninguna otra»*, que es lenguaje de intérprete.

La auditoría del 2026-09-13 lo recoge como decisión sin ADR (§9.3 (c)), y el contra-juez de ese
hallazgo lo matiza: el reparto híbrido se deduce de ADR-0019 y de la fase 6 del plan, pero *«falta
declarar por escrito que el reparto híbrido (árbol genérico + primitivas nombradas) es el que rige,
para que F18-F22 no se escriban como módulos aislados sin ese árbol»*. Sin este ADR, F18 se escribe
como cuatro módulos sueltos y el árbol no se usa nunca.

## Alternativas consideradas

1. **Árbol genérico con despacho por nombre a primitivas escritas a mano** (elegida).
2. **Código a mano por regla**, con la `forma` solo como documentación validada.
3. **Intérprete puro**: la `forma` como lenguaje completo, sin primitivas por nombre.
4. **Generar código desde la `forma`**, en Python y en MQL5.

## Por que elegimos esta opcion

Porque es la única en la que la `forma` que F12 valida es la misma que el motor ejecuta, sin pedirle
a la spec que describa geometría que no puede describir. Las guardias de F12 y F13 (argumentos que
faltan, valores crudos, hechos sin productor) solo protegen algo si el motor lee ese árbol; con
código a mano por regla, la spec y el motor divergen en silencio.

## Por que descartamos las demas

- **(2) Código a mano por regla**: convierte la `forma` en documentación. Todo lo que F12 comprueba
  dejaría de comprobar el comportamiento, y la precedencia por clase de ADR-0018 volvería a vivir en
  el orden del código.
- **(3) Intérprete puro**: la geometría —qué es romper un extremo, qué es una zona de control— no se
  expresa en el árbol, y la auditoría encontró que ni siquiera los acumuladores bastan: `perdida_dia`
  y `perdida_semana` declaran el mismo `reinicia_con: reloj_dia_riesgo`, y un intérprete no distingue
  el reinicio diario del semanal sin código específico por nombre. Que un intérprete puro sea
  inviable es una hipótesis que la auditoría declara no comprobada con prototipo; lo que sí está
  comprobado es que esta spec no le basta.
- **(4) Generar código**: duplica la frontera con MQL5 que ADR-0001 dejó fuera del contrato, y un
  generador es otro producto que mantener antes de tener un motor.

## Impacto

- **La tabla A de MASTER_PLAN se lee a través de este ADR**: las filas F18-F21 son grupos de
  primitivas, no módulos independientes. Si se reescribe la tabla, se cita este ADR.
- **El reinicio de cada acumulador lo sabe su primitiva**, por nombre. Es exactamente el caso del
  punto 1: el árbol dice `alcanza_tope: {acumulador: perdida_semana, ...}` y la primitiva del
  acumulador `perdida_semana` sabe que reinicia por semana. Que el campo `reinicia_con` no lo
  distinga es una deuda de la spec, declarada y fuera de esta rama.
- **Coste de una regla nueva**: cero código si solo combina vocabulario existente. RN-029 es el
  primer ejemplo: no introduce ningún predicado ni ninguna acción, solo dos acumuladores nuevos, y
  por eso exige dos primitivas de acumulador y nada más.
- F29 nombra sus funciones MQL5 igual que las primitivas de Python, y F30 compara las decisiones
  que salen del árbol.

## Fecha / fase

2026-09-14, después de F13 (decisión del consultor, sobre la auditoría del 2026-09-13).

## Estado

ACTIVE
