# El respaldo de A-11: DECIDIDA por ADR, y G1 sin excepciones

Rama `trabajo/respaldo-a11`, abierta el 2026-10-07 desde `main` en d96b703 (commit de estado sobre
el merge 363f826, tag `stable/F37d-activacion-a42`; `git rev-parse main origin/main` dio
`d96b70377c56bf877344f4a64aec865ee760793d` las dos). Encargo: `docs/encargos/trabajo-respaldo-a11.md`.
Cierra el punto U de la Next Action. Decisiones de partida del consultor (2026-10-06), D1 y D2, en
el encargo.

**Este informe llega hasta la PARADA de la fase 0.** Fuera de él y de los ficheros de apertura de la
rama no se ha cambiado nada del repositorio. El ADR nuevo se nombra sin su id hasta que exista
(`knowledge validate` rechaza la cita de un ADR que no existe). Las medidas se hicieron en un clon desechable
(`git worktree add` en la carpeta temporal, borrado después; CLAUDE.md, «Ensayos aislados»). Solo se
leyó YAML de spec, código y docs: ninguna transcripción, ningún libro, ningún fotograma.

## 0. Resumen de la fase 0

| Punto | Resultado |
|---|---|
| a. A-11 hoy | RESUELTA, sin `clase`, dos ítems de evidencia (uno supersedido), cerrada por un `RESOLVE_UNKNOWN` grabado de la sesión 1 (§1). |
| b. RESUELTA → DECIDIDA | **El código lo deja pasar** (medido en el clon: `knowledge validate` exit 0). **Ningún documento lo describe ni lo prohíbe.** Dos efectos que hay que decidir: el `RESOLVE_UNKNOWN` de A-11 sigue activo y `test_kit` congela los conjuntos de RESUELTAS y DECIDIDAS (§2). No paro: el régimen lo permite; propongo la vía y la decides tú (§6, D-a). |
| c. La excepción de G1 | `src/botsito/validation/citas_supersedidas.py:45-52` y 8 tests de `tests/unit/test_citas_supersedidas.py`; sin el par, 8 de esos tests fallan, como se espera (§3). |
| d. Quién cita A-11 y el id | El id solo en `ambiguedades.yaml:179` dentro de la spec; A-11 en prosa en spec, código y tests. Al quitarlo se rompen, además de los 8 de G1, 2 tests de `test_kit.py` (§4). |
| e. El revisor | `.claude/agents/revisor.md`: añadir D2 toca `.claude/` → push de `fix/respaldo-a11` y CI de Linux (§5). |
| f. Siguiente ADR libre | **0070** (§5). |

**PARADA.** Lo que hace falta del consultor está en §6.

## 1. Fase 0 a · A-11 hoy

`knowledge/spec/ambiguedades.yaml:170-186`, leído con `grep -n`:

| Campo | Línea | Valor |
|---|---|---|
| `id`, `titulo` | 170-171 | A-11, «SL en la orden o tras el llenado» |
| `pregunta` | 172-176 | «¿el SL va en la orden pendiente o se pone tras el llenado? RESPONDIDA por el trader el 2026-09-10: "el SL se pone junto a la orden limite, no cuando se apertura recien". Hasta entonces figuraba RESUELTA pero su valor era una INFERENCIA nuestra, que el barrido de fidelidad dejo anotada en la descripcion del parametro» |
| `evidencia` | 178-180 | `ev-v4-001207-0c4ffd4b` (**supersedido** por `ev-v6-021939-b430a110`) y `ev-v1-000620-0f7dea14` (activo) |
| `parametros` | 181 | `[stop_en_orden_pendiente]` |
| `estado` | 183 | `RESUELTA` |
| `decision`, `decidida_el` | 184-185 | `null`, `null` |
| `bloqueante` | 186 | `false` |
| `clase` | — | **no la tiene** |

**Quién la cierra hoy:** `fb-2026-09-09-sesion-01-69711f67`, `RESOLVE_UNKNOWN` sobre la ambigüedad
A-11, `medio: video` (v6, 1:43:51–1:44:36), sin `supersede` y sin nadie que lo superseda (activo).
Su `valor_resultante`: «el stop completo va en la orden y sirve para dimensionar el lote; tras el
llenado se mueve inmediatamente a 0,80». La respuesta referida del 2026-09-10 es otro registro,
`fb-2026-09-09-sesion-01-76fd91ba` (`CONFIRM` sobre el parámetro `stop_en_orden_pendiente`, valor
`en_la_orden`), que es la `fuente` de ese parámetro (`parametros.yaml:817-833`).

## 2. Fase 0 b · Cerrar como DECIDIDA, y pasar de RESUELTA a DECIDIDA

**Lo que exige una DECIDIDA**, con su fuente:

| Exigencia | Dónde |
|---|---|
| Hay dos formas de cerrar: RESUELTA con un registro del trader sobre la ambigüedad, o «`DECIDIDA` por el consultor con el ADR que la nombre» | `docs/runbooks/AMBIGUEDADES.md:37` (ADR-0022) |
| «una DECIDIDA solo [se reabre] con otro ADR»; «Una `DECIDIDA` no se reabre con feedback» | `CLAUDE.md:175`; `AMBIGUEDADES.md:54` |
| `decision` con un `ADR-NNNN` y `decidida_el` `AAAA-MM-DD`; y los dos solo en DECIDIDA | `src/botsito/cases/ambiguedades.py:174-187` (al cargar) |
| El ADR **existe** y **la nombra**; la ambigüedad **no es `bloqueante`**; **ningún parámetro** la lleva en su `ambiguedad_id` | `src/botsito/validation/knowledge.py:829-857` (`knowledge validate`); probadas en `tests/unit/test_kit.py:1352` y `:1428` |
| Una DECIDIDA no entra en el cuestionario | `tests/unit/test_kit.py:1496` |
| `clase`: **no la exige**; solo es obligatoria en una ABIERTA | `ambiguedades.py:48-49` y `abiertas_sin_clase` (`:267-279`) |
| Un `REOPEN` sobre una DECIDIDA es error | `knowledge.py:169-173`; `tests/unit/test_reabrir_y_fuente_documental.py:171` |

A-11 cumple las condiciones semánticas: no es bloqueante y `stop_en_orden_pendiente` no lleva
`ambiguedad_id` (`parametros.yaml:817-833`).

**RESUELTA → DECIDIDA sin cambiar su valor: el código lo deja pasar.**
- Ninguna guardia compara el estado de una ambigüedad con el de su historial: el régimen de
  `knowledge/spec/` es «versionado, cada cambio cita su fuente» (`CLAUDE.md`, trailer `Fuente:`).
- `problemas_de_cierre` (`knowledge.py:139-178`) exige un `RESOLVE_UNKNOWN` activo a una RESUELTA y
  prohíbe un `REOPEN` sobre una DECIDIDA; **no dice nada de un `RESOLVE_UNKNOWN` activo sobre una
  DECIDIDA**.
- `feedback pending` (`cli.py:2034`) da por reflejado un registro sobre una ambigüedad que no está
  ABIERTA.
- **Medido en un clon desechable** (`git worktree add`, con A-11 DECIDIDA, `decision` con el número 0070
  -un ADR de prueba que la nombra-, `decidida_el: '2026-10-06'`, sin `clase`, sin el id supersedido
  y `EXCEPCIONES = ()`): `uv run botsito knowledge validate` → **exit 0**, «OK: 55 ambiguedades
  registradas».

**Ningún documento lo describe ni lo prohíbe.** `AMBIGUEDADES.md` cuenta cómo se abre, cómo se
cierra y cómo se reabre (`REOPEN` → ABIERTA), no el paso directo de una forma de cierre a la otra.
Por eso no paro, pero el paso deja dos cosas que decide el consultor (§6, D-a):

1. **`fb-2026-09-09-sesion-01-69711f67` sigue activo**, un `RESOLVE_UNKNOWN` del trader sobre una
   ambigüedad que ya no cierra él. No hay forma limpia de retirarlo: un `REOPEN` exige que la
   ambigüedad quede ABIERTA y está prohibido sobre una DECIDIDA, y el feedback es solo-añadir.
   Queda como historia, y el ADR lo dice.
2. **La guardia de DECIDIDA tiene un porqué escrito**: «una decision del consultor no puede tapar una
   pregunta que le toca al trader» (`test_kit.py:1428-1440`). Mecánicamente A-11 la pasa; el
   argumento de D1 para no preguntarle es la restricción impuesta por el mundo y que ya se decidió no
   volver a preguntarle (ACTIVACION-A42.md §5.4). El ADR lo tiene que decir con esas palabras.

## 3. Fase 0 c · La excepción de G1

- **Dónde:** `src/botsito/validation/citas_supersedidas.py:45-52`,
  `EXCEPCIONES = (Excepcion("A-11", "ev-v4-001207-0c4ffd4b", "respaldo de A-11 pendiente de decisión
  del consultor, GUARDIAS-CITAS.md §8; 2026-10-06"),)`. El mecanismo (la clase `Excepcion`, el
  parámetro `excepciones` de `problemas_en_texto` y `citas_a_supersedidos`, y el fallo «excepcion de
  G1 sin uso») vive en el mismo fichero.
- **Sus tests:** `tests/unit/test_citas_supersedidas.py:136-222`. **Medido en el clon:** con A-11 sin
  el id y `EXCEPCIONES = ()`, fallan **los 8** que dependen del par:
  `test_la_excepcion_es_exactamente_un_par`, `_deja_pasar_su_par`,
  `_no_cubre_otro_supersedido_de_a11`, `_no_cubre_el_mismo_id_en_otra_ambiguedad`,
  `_no_cubre_el_par_en_otro_fichero_sin_objeto_a11`, `_no_cubre_un_comentario`,
  `test_caducidad_la_excepcion_sin_uso_falla` y `test_caducidad_en_el_repositorio_real`. Los de la
  condición, que pasan `excepciones=()`, siguen en verde.
- **Para que la excepción salga en el mismo commit** que A-11: vaciar `EXCEPCIONES` (o quitar el
  mecanismo, §6 D-c); en el test, `EXCEPCIONES == ()` en vez del par; los seis que prueban el
  mecanismo pasan una excepción sintética explícita (si se conserva) o salen (si se quita);
  `test_caducidad_en_el_repositorio_real` pasa a «G1 sobre el repo real da `[]` sin ninguna
  excepción»; y un test nuevo que **rompe a propósito**: con los ítems reales del repo, un
  `knowledge/spec/` temporal que cita cada id supersedido falla, uno por uno.

## 4. Fase 0 d · Quién cita A-11 y el id supersedido

**El id `ev-v4-001207-0c4ffd4b`** (`git grep`, fuera de HISTORIA):
- en la spec, solo `knowledge/spec/ambiguedades.yaml:179`;
- `knowledge/cases/kit/2026-09-09-sesion-01/cuestionario.yaml:483`: el cuestionario de la sesión 1,
  un artefacto congelado fuera del alcance de G1 (`knowledge/cases/`, protegido en el contrato);
- `knowledge/_proposals/pr-v4-000500-001500-28a0de27.yaml:1577`: la propuesta de F07 de la que salió;
- `src/botsito/validation/citas_supersedidas.py:50` y `tests/unit/test_citas_supersedidas.py:18, 222`;
- informes cerrados (`GUARDIAS-CITAS.md`, `F11-strategy-spec-schema.md`, la auditoría del
  2026-09-13) y salidas de anexos: historia, no se tocan.

**A-11** se nombra en prosa en `parametros.yaml` (líneas 530, 823, 1156, 1340), `strategy_spec.yaml`
(298, 1499), `glossary.yaml` (119), `ambiguedades.yaml` (248, en A-14), tres comentarios de código
(`cases/paquete.py:700`, `engine/primitivas_broker.py:431`, `feedback/modelo.py:114`) y
`knowledge/cases/kit/contexto_preguntas.yaml:183`. Ninguna depende de su estado: dicen que A-11
«cerró» que el stop viaja en la orden, y sigue siendo cierto.

**Lo que se rompe al quitarlo**, medido con la suite entera en el clon (`uv run pytest -q`): 13
fallos.
- **8 de G1** (§3).
- **2 de `test_kit.py`**:
  - `test_ambiguedades_reales_y_esquema`: congela las RESUELTAS (`{A-1..A-12} | {…}`, línea 315) y
    las DECIDIDAS (`{A-15, A-17, A-19, A-22, A-23, A-24}`, línea 342). A-11 pasa de un conjunto al
    otro.
  - `test_una_ambiguedad_puede_citar_evidencia_ya_supersedida` (línea 1392): exige que alguna
    ambigüedad real cite un ítem supersedido, y su propio mensaje dice que si deja de existir «hay
    que revisar si el test sigue teniendo sentido». Con G1 sin excepciones, ninguna puede: el caso
    ya solo se puede probar con un YAML sintético (§6 D-d).
- **3 del propio clon de medida**, que no saldrán en la rama: dos de `test_adr.py` (el ADR de prueba
  no estaba en el índice) y `test_repository_integrity.py::test_no_unexpected_ignored_paths` (el
  `settings.local.toml` y el `.venv` del clon).

## 5. Fase 0 e y f · El revisor, y el número del ADR

**El revisor** se define en `.claude/agents/revisor.md` (140 líneas): un subagente con su lista del
eje (a). Su punto 9 ya dice «nada afirma mas de lo que su cita sostiene (comprueba al menos tres
citas del informe contra su fuente)», pero habla de las citas del INFORME, no de los ítems de
evidencia. D2 entra como un punto nuevo del eje (a), junto al 4 (regímenes de cambio, donde ya mira
la evidencia nueva).
- **Toca `.claude/`**: por RITUAL («Antes del merge: la CI de Linux»), push de `fix/respaldo-a11` y
  CI de Linux con su número de run.
- Lo vigila `tests/unit/test_revisor.py` (frontmatter, herramientas de solo lectura, los dos ejes y
  las tres gravedades): un punto más no lo rompe.
- `.claude/settings.json` no tiene reglas `deny` ni `ask` sobre editar `.claude/`, y la guardia solo
  mira Read, Grep, Glob, Bash y PowerShell.

**El siguiente ADR libre es 0070**: el índice (`docs/adr/README.md`) acaba en 0069, y `ls docs/adr`
también.

## 6. Lo que decide el consultor (PARADA)

| # | Decisión | Opciones, y la que recomiendo |
|---|---|---|
| D-a | **La vía de RESUELTA a DECIDIDA** | (a) **Recomendada:** paso directo en un commit con el ADR nuevo, el 0070 (`decision` con su id, `decidida_el: '2026-10-06'`, la fecha de D1), sin el id supersedido, y el ADR dice que `fb-…-69711f67` queda activo como historia y por qué no se pregunta al trader. (b) Lo mismo, y además escribir en `AMBIGUEDADES.md` que una RESUELTA puede pasar a DECIDIDA con un ADR, sin `REOPEN`, para que la vía quede escrita (toca un runbook, fuera del encargo). |
| D-b | **`clase` de A-11** | (a) **Recomendada:** sin `clase`, como las otras DECIDIDAS: no la exige y ya no se pregunta. (b) `clase: pregunta`, para dejar dicho que era una pregunta al trader. |
| D-c | **El mecanismo de excepciones de G1** | (a) **Recomendada:** se conserva vacío, `EXCEPCIONES = ()`, como `EXCLUIDOS`, con un test que exige `== ()` y los tests del mecanismo con una excepción sintética: añadir una vuelve a ser una decisión que se ve en el diff. (b) Se quita entero, con sus seis tests: «sin ninguna excepción» queda estructural. |
| D-d | **`test_una_ambiguedad_puede_citar_evidencia_ya_supersedida`** | (a) **Recomendada:** se reescribe con un YAML sintético en `tmp_path`: lo que vigila (que `kit check` y `knowledge validate` cuenten como existente un ítem supersedido) sigue valiendo. (b) Se borra, porque G1 ya no deja que ocurra en la spec. |
| D-e | **La evidencia que le queda a A-11** | `ev-v1-000620-0f7dea14` («proteger el trade, a inicio apenas se genere la entrada»): habla de la pregunta y admite las dos lecturas (GUARDIAS-CITAS.md §8.1). Recomiendo dejarla, y que el ADR diga que no es lo que decide. |

Lo que el encargo ya fija y no pide decisión: el ADR nuevo (0070) con D1; D2 en el revisor; la nota sobre
`ev-v6-021939-b430a110` en este informe (su `afirmacion`, «el stop que se introduce en la operacion
es 0,80, ya no 0,75», excede su `cita_literal`, «Es 0.80 Ya a 0.75 Acá nada más Ahora es a 0.8 No a
0.75», y no respalda el momento del stop); y la deuda a HISTORIA.

**Saldo de bytes de PROJECT_STATE**: hoy +141 sobre `main` (23.967 frente a 23.826), todo de
`Current Branch` y `Current Feature`, que el cierre devuelve. La línea de deuda que sale mide 177
bytes, así que el saldo de las ediciones de contenido será −177.

## 7. Lo que cambia esta rama hasta aquí

- `docs/encargos/trabajo-respaldo-a11.md`, `contrato.yaml`, el Archivo 21 de `HISTORIA.md` y
  `PROJECT_STATE.md` (`Current Branch`, `Current Feature` y las dos líneas del archivo).
- Este informe.

El contrato solo permite hoy esas rutas; las de las fases 1-4 se añaden tras la respuesta.

## Estado

**EN CURSO: PARADA de la fase 0 (2026-10-07).** Espera la respuesta del consultor al §6.
