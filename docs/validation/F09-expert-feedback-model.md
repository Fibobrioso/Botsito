# FUNCTIONALITY VALIDATION REPORT

**Funcionalidad:** F09 · expert-feedback-model
**Rama:** `feature/F09-expert-feedback-model`
**Objetivo:** cada aportacion del trader como registro trazable y solo-anadir, con respuesta
literal, medio, objetivo tipado y accion; nunca modifica la evidencia (la supersede); cadena
evidencia → feedback reconstruible; todo cambio de spec o casos cita su fuente en el commit.

## Que se construyo
- `src/botsito/feedback/modelo.py`: `FeedbackRecord` (7 campos obligatorios, 6 opcionales), id
  `fb-<sesion>-<hash8>` por hash del contenido, carpeta = sesion, nombre = id; nueve acciones;
  seis tipos de objetivo con formato propio; tabla de coherencia accion/objetivo; acciones que
  exigen `valor_resultante`; medio distinto de `escrito` exige grabacion y minuto; `supersede`;
  `activos()`; `trazar()`; validacion contra contexto (evidencia existente, parametro del registro,
  contradiccion abierta, grabacion inventariada; regla/ambiguedad/caso por formato hasta F11/F14).
- `src/botsito/evidence/historial.py` generalizado: guardia por blobs para cualquier directorio
  (`knowledge/feedback/` incluido) y `commits_sin_fuente`: todo commit posterior a `stable/F06` que
  toque `knowledge/spec/` o `knowledge/cases/` debe llevar un trailer `Fuente:` con ids de
  evidencia, feedback o ADR existentes.
- Hook `pre-commit`: rechaza modificar, renombrar o borrar feedback (ademas de evidencia).
- CLI: `botsito feedback new`, `feedback trace <id>`, `feedback pending`; `knowledge validate`
  cubre feedback, su historial y los trailers `Fuente:`.
- `knowledge/feedback/README.md`: esquema, coherencia y plantilla de sesion.
- Contrato de capas refinado en `pyproject.toml`: `cases -> spec -> feedback -> evidencia/corpus/
  datos/config -> domain`. El contrato anterior tenia evidencia y feedback como hermanos
  independientes y se rompio (correctamente) al importar; la jerarquia nueva es la que el plan
  describe (seccion G y H).

## Archivos creados
```
src/botsito/feedback/modelo.py
tests/unit/test_feedback.py  tests/contract/test_feedback_history.py
docs/plan/features/F09-expert-feedback-model.md  docs/validation/F09-expert-feedback-model.md
```

## Archivos modificados
`src/botsito/evidence/historial.py` (generalizacion + trailers), `src/botsito/cli.py`,
`src/botsito/feedback/__init__.py`, `scripts/git-hooks/pre-commit`, `knowledge/feedback/README.md`,
`pyproject.toml` (capas), `tests/contract/test_evidence_history.py` (firma), `PROJECT_STATE.md`.

## Decisiones tomadas
- **`feedback apply` se difiere a F11** (con reason en el brief): sin esquema de `strategy_spec.yaml`
  no hay diff que proponer. `feedback pending` lista lo que F11 debera reflejar.
- **Trailer `Fuente:` desde `stable/F06`** y no desde el inicio: los commits anteriores crearon el
  esquema vacio del registro sin fuente de negocio. Los cambios de esquema futuros citan un ADR
  (`Fuente: ADR-NNNN`), los de valor citan evidencia o feedback.
- **Medio `escrito` sin grabacion**: la respuesta literal es el texto exacto del trader; los demas
  medios exigen grabacion inventariada y minuto, porque la sesion se graba (seccion H).
- **Coherencia accion/objetivo en el cargador**, no en la revision: un `RESOLVE_CONTRADICTION`
  sobre un tema sin contradiccion abierta no entra.

## Como ejecutarlo
```
make check
# El registro de parametros esta vacio hasta F11: un objetivo `parametro` se rechaza por contexto.
uv run botsito feedback new --sesion 2026-09-20-sesion-01 --fecha 2026-09-20 --medio escrito \
  --objetivo-tipo ambiguedad --objetivo-id A-10 --accion RESOLVE_UNKNOWN \
  --valor "0,75 + spread" --respuesta "el 0,8 es el 0,75 mas el spread" --registrado-por aleks
uv run botsito feedback trace A-10
uv run botsito feedback pending
uv run botsito knowledge validate
```

## Como probarlo
- Crear un registro y editarlo a mano: `knowledge validate` falla por id; el hook rechaza el
  commit; con `--no-verify`, el test de historial falla.
- Tocar `knowledge/spec/parametros.yaml` y commitear sin `Fuente:`: `knowledge validate` nombra el
  commit.
- Un `LABEL_CASE` con objetivo `evidence`: rechazado por coherencia.

## Tests ejecutados
`make check` en `feature/F09-expert-feedback-model`, Windows 11, Python 3.12 (`.python-version`). Hook probado en repositorio
temporal: acepta anadir feedback, rechaza editar y borrar.

## Resultados
- ruff, mypy strict (48 ficheros), 3 contratos KEPT con la jerarquia nueva.
- pytest: 208 passed (149 funciones tras la auditoria de cierre; rechazos parametrizados de
  evidencia, feedback y registro; property de estabilidad del id; historial con modificar,
  borrar, anadir en merge, rutas con acento, clon superficial, repo anidado y tag movido;
  trailers validos, invalidos, inexistentes, con ADR inexistente, con digitos Unicode y con
  mensaje acentuado; detector de literales con 8 formas de elusion; CLI de feedback y evidencia
  con contexto en un knowledge/ temporal).
- `state`, `config`, `knowledge validate` (0 registros, historial intacto, commits con Fuente): OK.
- CI GitHub Actions (ubuntu-latest, historial completo): verde, run 33894611220 (01477bf) y,
  tras la auditoria extrema, run 33909186793 (d217a11).
- Pruebas cruzadas tras la auditoria: clon sin tags valida por el ancla SHA; clon superficial
  falla con ERROR explicito; `make hooks` desde PowerShell; hook con rutas con acento y espacio.

## Auditoria extrema (2026-09-04, tres agentes: codigo, plan/ejecucion, repositorio)
Hallazgos corregidos en esta rama (cada uno con test o prueba manual):
- CRITICO · `subprocess` decodificaba git en cp1252: un mensaje de commit con `Í`/`Á` dejaba la
  salida en `None` y `knowledge validate` lo leia como "sin problemas" (solo Windows). Ahora UTF-8
  con `core.quotepath=false`; test con mensaje acentuado; `None` con git presente es ERROR.
- ALTO · Ficheros anadidos dentro de un commit de merge quedaban fuera de la guardia para siempre
  (`git log` sin `-m`). Test `test_adicion_escondida_en_un_merge_queda_protegida`.
- ALTO · `evidence new --video V1` creaba ids fuera de formato y rutas que el hook no veia (awk por
  espacios, rutas entrecomilladas). `video_id` validado (`^[a-z0-9]+$`) y contra `fuentes.yaml`;
  hook con `-F'\t'` y sin entrecomillar; test con ruta `vídeo 1`.
- ALTO (repo) · Sin el tag `stable/F06` la comprobacion de trailers pasaba en silencio. Ancla
  tag + SHA; clon superficial = ERROR; CI hace `git fetch --tags --force`.
- MEDIO · `fecha: 2026-09-20` sin comillas reventaba con `TypeError`; `t0: 1:05:00` se cargaba
  como 3900; `valor_resultante: yes` era `"True"`; claves YAML duplicadas ganaba la ultima.
  Cargador estricto `yaml_estricto.py` + tipos texto exigidos + `fecha` = fecha de la `sesion`.
- MEDIO · `decimal.InvalidOperation`, `NaN`, `Infinity`, `25:99` y `minimo > maximo` en el
  registro; `lecturas_ambiguas()` crecia una entrada por lectura (por tick en F24).
- MEDIO (repo) · `make hooks` fallaba desde PowerShell (`cmd.exe`); `main` con un commit
  `docs(state)` tras el tag sin que `state check` lo vigilara; CI corria dos veces por PR.
- Diseno · ADR-0004: categorias de parametro y horas con huso (`tzdata` anadido: Windows no
  tenia base de husos, `ZoneInfo("Europe/Madrid")` fallaba). Resto de riesgos de ejecucion en
  MASTER_PLAN H.2, absorbidos por F07, F10, F11, F15, F17, F18, F21–F24, F28–F31, F33.

## Auditoria de cierre (2026-09-04, tres agentes: codigo, plan/docs, infraestructura)
Segunda pasada antes de la validacion del usuario. Todo corregido en esta rama, con test:
- ALTO · `feedback new` / `evidence new` con un campo en blanco (`--valor "   "`) escribian un
  fichero cuyo id no coincidia con su contenido (nadie podia cargarlo). Ahora los textos se
  normalizan y los vacios se descartan ANTES de calcular el id; lo escrito se recarga como
  invariante y, si fallara, se borra.
- ALTO · `Fuente: ADR-9999` pasaba (los ADR se comprobaban solo por formato). Ahora los ids de ADR
  reales (`docs/adr/NNNN-*.md`) entran en `ids_validos` como cualquier otra fuente.
- ALTO · `test_no_business_literals` no veia `Decimal("0.75")`, `"0.5"`, `3 / 4`, `"07" + ":00"`
  ni f-strings, y excluia todo `config/`. Ahora evalua constantes de texto numericas y expresiones
  formadas solo por constantes, y excluye unicamente `config/registro.py`.
- MEDIO · `--sesion ""` y `--t0 ""` daban `KeyError`; ahora error de dominio. `feedback new` y
  `evidence new` validan contra el contexto (evidencia, registro, contradicciones, manifiesto)
  antes de escribir. Fechas imposibles (`2026-13-45`) y digitos Unicode en ids/tiempos rechazados
  (`re.ASCII`). Supersede cruzado (otro objetivo/tema) y ciclos detectados. Un fichero que no sea
  `*.yaml` en evidencia/feedback es error. Manifiesto con `ficheros: null`, `duracion_s: abc` o
  entradas no-mapa, TOML roto o UTF-16, YAML con clave no hashable: errores de dominio, no
  tracebacks. `bytes: 1.5` o `true` en fuentes rechazados. ffprobe leido en UTF-8 sin `check`.
- MEDIO · El ancla de trazabilidad es siempre el SHA; si el tag `stable/F06` existe y apunta a otro
  commit, `knowledge validate` lo denuncia. Clon superficial o proyecto anidado en otro repo:
  "no evaluable" (ERROR), no "sin violaciones". El asunto del commit no cuenta como trailer.
- MEDIO · Registro: `texto` vacio, claves de nivel superior ajenas y `minimo/maximo` en `hora` o
  `texto` rechazados.
- MEDIO (infra) · `instalar_hooks.py` instalaba en `--git-dir/hooks`, que un worktree no lee
  (ahora `--git-path hooks`); no detectaba `core.hooksPath` global (ahora aborta); sobrescribia un
  hook ajeno (ahora `.bak`); git ausente daba traceback. El hook ejecuta `uv run --locked` (no
  reescribe `uv.lock` dentro de un commit) y rechaza el commit si `uv` no esta en PATH; la exencion
  `_*.yaml` exige que TODAS las rutas de un rename sean exentas. `.python-version` fija 3.12 en
  local y en CI (antes local 3.13 y CI 3.12). CI con `permissions`, `concurrency`, `timeout` y
  `BOTSITO_EXIGE_FFPROBE` (sin ffprobe los tests de video fallan en CI, no se omiten).
- Tests · `_git` de integridad solo omite si no hay git (antes cualquier fallo era skip verde);
  allowlist de ignorados por componente; `**/` en `.gitignore` cubierto; `state check` en HEAD
  separado es skip explicito; `evidence new` ya no se prueba contra el repo real.
- Docs · ADR-0004 (`feedback pending` filtra por `estrategia`: ahora implementado), ejemplo de este
  informe (usaba un parametro inexistente), H.2 anclaje H4 coherente con el orden E, dueno por
  ambiguedad en PROJECT_STATE, READMEs de `docs/`, `docs/research/`, `tests/` y `scripts/`.

## Que deberia observar el usuario
`knowledge/feedback/README.md` con esquema y plantilla de sesion; `feedback pending` vacio;
`knowledge validate` en verde; el hook rechazando una edicion de feedback.

## Que casos funcionan
Todo el alcance del brief salvo `feedback apply`, diferido a F11 por diseno.

## Que casos todavia no funcionan
- No hay registros reales: la sesion 1 con el trader va tras F10 y F15.
- Objetivos `regla`, `ambiguedad` y `caso` se validan solo por formato hasta F11/F14.
- `feedback trace` muestra el item de evidencia y los registros de feedback; la cadena hasta la
  regla de la spec llega con F11.

## Limitaciones
El trailer `Fuente:` se exige por commit, no por linea cambiada: un commit que mezcle un cambio
de esquema y uno de valor debe citar ambas fuentes.

## Riesgos
Sesiones sin grabacion: el modelo obliga a `escrito` con texto exacto; la paráfrasis del
intermediario queda excluida por construccion, no por disciplina.

## Impacto sobre funcionalidades anteriores
`historial.py` cambia de firma (directorio opcional, por defecto evidencia); los tests de F06
siguen en verde. `knowledge validate` es mas estricto.

## Estado
WAITING_FOR_USER_VALIDATION
