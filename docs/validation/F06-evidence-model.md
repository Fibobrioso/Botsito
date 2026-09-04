# FUNCTIONALITY VALIDATION REPORT

**Funcionalidad:** F06 · evidence-model
**Rama:** `feature/F06-evidence-model`
**Objetivo:** definir la unidad de conocimiento extraido del corpus (`EvidenceItem`) con cita
verificable y hacerla inmutable por construccion: id con hash del contenido, nombre de fichero = id,
hook local y test contra el historial de git. Las contradicciones se regeneran, no se escriben.

## Que se construyo
- `src/botsito/evidence/modelo.py`: esquema (12 campos obligatorios, 4 opcionales), parseo de
  tiempos `h:mm:ss[.d]`, contenido canonico (claves ordenadas, espacios normalizados), id
  `ev-<video>-<hhmmss>-<hash8>`, carga y validacion, validacion contra el manifiesto del corpus
  (video existe, `t1` dentro de la duracion, fotogramas inventariados, `supersede` existe),
  `escribir_item` que nunca sobreescribe, `activos()` (no superseded).
- `src/botsito/evidence/contradicciones.py`: items activos con el mismo `tema` y `valor` distinto →
  `_contradicciones.yaml` generado y determinista; validador que exige que el fichero coincida con
  la regeneracion.
- `src/botsito/evidence/historial.py`: `git log --name-status` sobre `knowledge/evidence/`; toda
  modificacion, renombrado o borrado de un `*.yaml` (salvo `_contradicciones.yaml`) es violacion;
  version sobre el indice para el hook.
- Hook `scripts/git-hooks/pre-commit`: rechaza commits con evidencia modificada o borrada
  (`make hooks` reinstalado). Cabecera corregida (ya no menciona `core.hooksPath`).
- CLI: `botsito evidence new` (crea un item con id correcto), `botsito evidence contradictions`
  (regenera), `botsito knowledge validate` cubre evidencia, contradicciones e historial.
- `knowledge/evidence/README.md` con el esquema; `_contradicciones.yaml` generado (vacio).
- Regla de la seccion H "sin inferencias": cita literal obligatoria (minimo 5 caracteres),
  afirmacion no mas larga que 2x la cita + 40, `revisado_por` obligatorio, `provenance` en
  `botsito | bot-v2`.

## Correcciones aplicadas tras la auditoria global (2026-09-04)
- **Edicion escondida en un commit de merge no se detectaba.** `git log --name-status` omite los
  diffs de los merges; una simulacion lo demostro. La guardia ahora compara, para cada fichero de
  evidencia que alguna vez se anadio, el blob de HEAD con el blob del commit que lo anadio, y exige
  que siga existiendo; tambien detecta ediciones sin commitear. Cinco escenarios en tests
  (modificar, borrar, renombrar, editar en merge, editar sin commit).
- **`make check` no ejecutaba `knowledge validate` de forma explicita** (solo a traves de un test).
  Ahora es un paso propio.
- **`0,75` y `0.75` habrian sido una contradiccion.** Los valores numericos con coma se normalizan
  antes de comparar; las mayusculas tambien.

## Archivos creados
```
src/botsito/evidence/{modelo,contradicciones,historial}.py
knowledge/evidence/_contradicciones.yaml
tests/unit/test_evidence.py  tests/contract/test_evidence_history.py
docs/plan/features/F06-evidence-model.md  docs/validation/F06-evidence-model.md
```

## Archivos modificados
`src/botsito/cli.py`, `src/botsito/evidence/__init__.py`, `scripts/git-hooks/pre-commit`,
`knowledge/evidence/README.md`, `tests/unit/test_tree.py`, `tests/contract/test_repository_integrity.py`,
`PROJECT_STATE.md`.

## Decisiones tomadas
- **Id con hash del contenido** en vez de contador: editar un fichero rompe su id y el cargador lo
  rechaza aunque el hook y el test de historial fallaran.
- **Contradiccion = mismo `tema` y `valor` distinto entre items activos.** Los items sin `valor` no
  generan contradicciones: la deteccion es mecanica solo donde el valor esta normalizado.
- **`CONTRADICTION` no es un tipo de item escribible**: solo existe en el fichero generado.
- **Heuristica de longitud de la afirmacion** como freno mecanico a las inferencias; la revision
  humana (`revisado_por`) sigue siendo la garantia real.
- **Tolerancia de duracion de 1 s** (`TOLERANCIA_DURACION_S`): el detector de literales de negocio
  atrapo un `0.5` de tolerancia; se renombro y se subio a 1 s para no confundirlo con el stop reducido.

## Como ejecutarlo
```
make check
uv run botsito evidence new --video v4 --t0 0:15:33 --t1 0:16:10 --modalidad audio \
  --tipo RULE_STATEMENT --cita "..." --afirmacion "..." --tema mitigacion.m15.cierre \
  --valor cuerpo --confianza alta --extractor humano --revisado-por aleks
uv run botsito evidence contradictions
uv run botsito knowledge validate
```

## Como probarlo
- Crear un item, editar su `valor` a mano y ejecutar `knowledge validate`: falla por id.
- Intentar commitear esa edicion: el hook la rechaza. Commitearla con `--no-verify`:
  `tests/contract/test_evidence_history.py` falla en CI.
- Crear dos items con el mismo tema y valores distintos y regenerar: aparece la contradiccion;
  crear un tercero con `supersede` al segundo: desaparece.

## Tests ejecutados
`make check` en `feature/F06-evidence-model`, Windows 11. Hook probado en un repositorio temporal:
acepta anadir, rechaza editar, acepta regenerar `_contradicciones.yaml`, rechaza borrar, rechaza renombrar.
(Una primera pasada dio un falso fallo por un error del guion de prueba: la edicion rechazada seguia en el indice.)

## Resultados
- ruff, mypy strict (43 ficheros), 3 contratos KEPT.
- pytest: 105 passed (92 funciones; 11 rechazos parametrizados; property test de estabilidad del id).
- `state check`, `config validate`, `knowledge validate` (0 items, 0 contradicciones, historial
  intacto): OK.
- CI GitHub Actions (ubuntu-latest, con historial completo): verde, run 33892467496.

## Que deberia observar el usuario
`knowledge/evidence/README.md` con el esquema; `_contradicciones.yaml` vacio y generado;
`uv run botsito knowledge validate` en verde; el hook rechazando una edicion de evidencia.

## Que casos funcionan
Todo el alcance del brief.

## Que casos todavia no funcionan
- No hay items reales todavia: los crea F07 (extraccion) sobre la transcripcion nueva (F04) y los
  fotogramas nuevos (F05); hasta entonces solo se pueden citar fotogramas heredados del manifiesto.
- La busqueda (F08) y el feedback que supersede items (F09) llegan despues.

## Limitaciones
La heuristica de longitud no detecta una inferencia corta; la garantia es la revision humana y, en
F07, la medicion de precision del extractor. El test de historial necesita `fetch-depth: 0` en CI
(ya configurado desde F01).

## Riesgos
Rigidez que frene F07: mitigada con `evidence new`, el campo `notas` y `confianza: baja`.

## Impacto sobre funcionalidades anteriores
`knowledge validate` es mas estricto; el hook anade una regla. Nada anterior cambia de resultado.

## Estado
WAITING_FOR_USER_VALIDATION
