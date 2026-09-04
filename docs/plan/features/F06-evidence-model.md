# F06 · evidence-model

**Rama:** `feature/F06-evidence-model` · **Fase:** 1 · **Depende de:** F03

## Objetivo
Definir `EvidenceItem`: la unidad minima de conocimiento extraido del corpus, con cita verificable
(video, `t0`, `t1`, fotogramas), cita literal obligatoria, afirmacion normalizada, tipo, confianza,
extractor y revisor. Inmutable tras commit: el id incluye el hash del contenido y un test en CI
compara cada fichero con su primera version en el historial de git. Las contradicciones no se
escriben: se regeneran desde los items.

## Alcance cerrado (que SI)
- `src/botsito/evidence/modelo.py`: esquema, carga desde YAML (un fichero por item), validacion
  contra el manifiesto del corpus (video existe, `t0 < t1 <= duracion`, fotogramas referenciados
  existen), id = `ev-<video>-<hhmmss>-<hash8>` donde `hash8` es SHA-256 del contenido canonico sin
  el id; el nombre del fichero debe ser `<id>.yaml`.
- Campos obligatorios: `id, video_id, t0, t1, modalidad, tipo, cita_literal, afirmacion, tema,
  confianza, extractor, revisado_por, provenance`. Opcionales: `fotogramas, valor, supersede, notas`.
  `tipo` en `RULE_STATEMENT | PARAMETER | EXAMPLE_TRADE | NO_TRADE | MANAGEMENT | UNKNOWN`.
  `CONTRADICTION` solo existe en el fichero generado. `provenance` en `botsito | bot-v2`.
- Regla de la seccion H: sin inferencias. `cita_literal` no puede estar vacia; `afirmacion` no puede
  ser mas larga que 2x la cita (heuristica que obliga a mantenerse cerca del texto; ajustada a
  `2x + 40` durante la construccion para citas muy cortas) y el revisor es obligatorio.
- `src/botsito/evidence/contradicciones.py`: items activos (no superseded) con el mismo `tema` y
  `valor` distinto generan `knowledge/evidence/_contradicciones.yaml`; el validador falla si el
  fichero no coincide con la regeneracion.
- Inmutabilidad: `tests/contract/test_evidence_history.py` recorre `git log` y falla si un fichero
  de `knowledge/evidence/**/*.yaml` (salvo `_contradicciones.yaml`) fue modificado o borrado en
  cualquier commit; hook local que rechaza el commit antes.
- CLI: `botsito evidence new` (crea un item con id correcto), `botsito evidence contradictions`
  (regenera), `botsito knowledge validate` cubre evidencia y contradicciones.

## Fuera de alcance (que NO)
Poblar evidencia (F07). Busqueda (F08). Feedback (F09). Reglas o parametros con valor.

## Entradas
`knowledge/corpus/manifest.yaml` (videos, duraciones, ficheros heredados).

## Salidas (ficheros)
`src/botsito/evidence/{modelo,contradicciones}.py`, `knowledge/evidence/README.md` (esquema),
`knowledge/evidence/_contradicciones.yaml` (generado, vacio), tests, hook, informe.

## Tests
- Unit: esquema; id/hash y nombre de fichero; cita fuera de duracion; video desconocido; fotograma
  inexistente; sin revisor; afirmacion desproporcionada; supersede a id inexistente; tipo invalido;
  contradicciones (mismo tema, distinto valor; superseded no cuenta; regeneracion determinista).
- Contract: inmutabilidad contra historial en un repositorio temporal (modificar y borrar) y sobre
  el repositorio real; `_contradicciones.yaml` igual a la regeneracion.
- Property: el id es estable ante reordenacion de claves y cambios de espacio en blanco del YAML,
  y cambia ante cualquier cambio de contenido.

## Criterio de aceptacion
`make check` verde; un item sin cita, sin revisor o con cita fuera del video es rechazado; editar
un item ya commiteado rompe el test de historial y el hook; `_contradicciones.yaml` regenerable
sin diff; informe con estado WAITING_FOR_USER_VALIDATION.

## Riesgos
Rigidez excesiva que frene F07: mitigado con `botsito evidence new` y con el campo `notas` libre.

## Que habilita
F07 (extraccion) tiene un objeto que rechaza lo que no cita; F09 referencia ids estables; F11
deriva estados de regla desde items y feedback.
