---
status: ACTIVE
date: 2026-09-23
phase: post-F14 (rama `trabajo/casos-agosto-abril`)
---

# 0042 · Material ya visto entra por un reparto dev-visto, sin sorteo y sin holdout

## Decision

1. **Hay un tercer camino de reparto, dev-visto**, en `knowledge/cases/visto/<AAAA-MM>/`. Un
   mes, un libro, un reparto.
2. **Solo entra material que cumpla las tres condiciones.** Se comprueban al construir, en
   `dias_ingeribles` y en `knowledge validate` (`cases/visto.py:requisitos`):
   - el mes está en `vistos.yaml`;
   - su libro está en `libros.yaml` y su **lectura completa ya está declarada** en
     `docs/validation/HOLDOUT-EXPOSICIONES.md` (se comprueba por el nombre del fichero);
   - `cobertura_material` le da al mes un tramo con el `material_sha256` de ese libro.
3. **Todos sus días son `dev`.** El reparto no tiene semilla y el cupo de holdout es 0. La
   asignación son los días laborables de los tramos del mes.
4. **El mismo régimen de fichero que los otros repartos.**
   - `particiones.yaml` se recompone byte a byte desde `cobertura_material`, sin `data/`.
   - Va anclado por el sha de su blob en `knowledge/cases/visto/anclas.yaml`.
   - Si la cobertura cambia, deja de reproducirse y hay que reconstruirlo a la vista.
   - Lo construye y lo ancla `botsito casos visto --mes AAAA-MM`, que no sobreescribe.
5. **No toca los repartos del kit ni de fidelidad.** ADR-0036 queda intacto.
6. **La puerta aplica «ocultos» (ADR-0041) también a este camino.** Un día oculto no se ingiere
   aunque esté en dev-visto. Y la puerta recorre este directorio igual que los otros dos
   (`repartos_commiteables`).
7. **Si un reparto dev-visto no cumple sus condiciones, no se reproduce o no está anclado, la
   ingesta FALLA CERRADA.** Un reparto que no debería existir no puede hacer ingerible nada.

## Problema que resuelve

La ingesta (F14a, ADR-0037) solo pedía días de un reparto commiteado del kit. Ni abril ni agosto
tenían un solo día en ningún reparto, así que por el camino de mayo pedían 0 días
(`docs/validation/CASOS-AGOSTO-ABRIL.md`, paso 0).

Ninguno de los dos caminos existentes les sirve:
- **el kit** sortea días CIEGOS para una sesión con el trader, y estos meses no son ciegos;
- **el de fidelidad** sortea y reserva material etiquetado para una medida con holdout, y
  reservar días de un libro que ya se leyó entero no protege nada.

## Alternativas consideradas

- Meterlos en un paquete nuevo del kit.
- Un artefacto de fidelidad por mes, con todo el cupo en `fidelidad-dev`.
- Una lista de días a mano en la línea de comandos.
- Un reparto propio, sin sorteo y todo `dev`. Es el elegido.

## Por que elegimos esta opcion

- **Dice lo que el material es:** desarrollo ya visto y ya leído entero.
- **No finge un sorteo** ni reserva nada que no se pueda proteger.
- **Conserva las garantías de los otros repartos:** se reproduce, se ancla y pasa por la misma
  puerta.
- **Sus tres condiciones cierran el uso indebido.** Un mes ciego, o uno cuyo libro no se haya
  leído y declarado entero, no puede entrar por aquí.

## Por que descartamos las demas

- **El kit** exigiría falsear la ceguera: su filtro de vistos está para eso.
- **Fidelidad con todo `dev`** pervertiría un camino cuyo sentido es reservar, y mezclaría sus
  nombres.
- **Una lista a mano** es exactamente lo que `casos ingerir` prohíbe: el conjunto se deriva, no se
  elige.

## Impacto

- Nuevo `src/botsito/cases/visto.py`.
- `holdout.repartos_commiteables` recorre tres caminos.
- `ingesta.dias_ingeribles` acepta días del kit y de dev-visto, y falla cerrada si un dev-visto es
  inválido.
- `knowledge validate` comprueba los repartos dev-visto.
- `casos visto --mes` los construye y los ancla.
- Tests en `tests/contract/test_visto.py`.
- Los primeros meses que entran por aquí son abril y agosto, con los tramos que fija el
  consultor.

## Fecha / fase

2026-09-23, post-F14, rama `trabajo/casos-agosto-abril`. Decisión del consultor sobre el paso 0.

## Estado

ACTIVE
