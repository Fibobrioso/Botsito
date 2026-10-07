# El respaldo de A-11: DECIDIDA por ADR, y G1 sin excepciones

Rama `trabajo/respaldo-a11`, abierta el 2026-10-07 desde `main` en d96b703 (commit de estado sobre
el merge 363f826, tag `stable/F37d-activacion-a42`; `git rev-parse main origin/main` dio
`d96b70377c56bf877344f4a64aec865ee760793d` las dos). Encargo: `docs/encargos/trabajo-respaldo-a11.md`.
Cierra el punto U de la Next Action. Decisiones de partida del consultor (2026-10-06), D1 y D2, en
el encargo.

**Cómo se lee.** Los §0 a §7 son la fase 0, tal como se escribió antes de la PARADA (entonces no
se había cambiado nada del repositorio fuera del informe y los ficheros de apertura). La respuesta
del consultor, que SUSTITUYE la decisión D1 y deja A-11 RESUELTA, está en §6.1; la fase 1, en §8;
las comprobaciones y la CI, en §9; el revisor, en §10 y al final. Las medidas se hicieron en un clon desechable
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
bytes, así que el saldo de las ediciones de contenido será −177. **[Corregido en la fase 1: mide 180
bytes; ver §8.6.]**

### 6.1 Respuesta del consultor a la PARADA (2026-10-07), tal cual

> Modelo: Opus · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA de la fase 0 de trabajo/respaldo-a11 (2026-10-07). Cópiala tal cual al final del encargo y al informe.
>
> CAMBIO DE DECISIÓN, declarado: D1 queda SUSTITUIDA. Tu §1 muestra que A-11 ya está cerrada por el trader: fb-2026-09-09-sesion-01-69711f67 (RESOLVE_UNKNOWN sobre A-11, medio video, sesión 1, 1:43:51-1:44:36, confirmado en 2:00:01), con valor «el stop completo va en la orden». El consultor decidió D1 sin leer ese registro (hallazgo para la fila de la rama, abajo).
>
> 1. A-11 sigue RESUELTA. No hay ADR 0070 en esta rama, ni cambio de estado, ni de clase, ni de decision/decidida_el. D-a y D-b desaparecen.
>    Lo único que cambia en A-11: sale ev-v4-001207-0c4ffd4b de evidencia. Se queda ev-v1-000620-0f7dea14 (D-e: se mantiene, y el informe dice que lo que cierra A-11 es el registro del trader, no ese ítem). El texto de pregunta no se toca.
>    Antes de escribir, mide y deja en el informe que 1:43:51-1:44:36 y 2:00:01 de ese vídeo no caen en ningún tramo de knowledge/corpus/tramos_no_citables.yaml (léelo del yaml; no abras la transcripción). Si alguno cae dentro, PARA.
>    Trailer Fuente: fb-2026-09-09-sesion-01-69711f67. spec docs --escribir en el mismo commit si cambia algo generado.
> 2. D-c: opción (a). EXCEPCIONES = () con el mecanismo conservado, un test que exige que esté vacío, y los tests del mecanismo con una excepción sintética. Más el test que rompe a propósito: cada id supersedido real, citado en una spec temporal, hace fallar G1.
> 3. D-d: opción (a). test_una_ambiguedad_puede_citar_evidencia_ya_supersedida se reescribe con un YAML sintético en tmp_path.
> 4. test_ambiguedades_reales_y_esquema no cambia: A-11 sigue en RESUELTAS. Si falla, PARA.
> 5. D2 (el revisor) y la nota sobre ev-v6-021939-b430a110, como dice el encargo. Toca .claude/: push de fix/respaldo-a11 y CI de Linux con su número de run.
> 6. Fase 4 igual: la línea de Technical Debt de A-11 sale a HISTORIA bajo «# Technical Debt PAGADA», con saldo de bytes de PROJECT_STATE menor o igual que cero.
>
> Hallazgo del consultor para la fila de la rama en ERRORES-RECURRENTES (va en la orden de cierre): importa. El consultor decidió D1 (DECIDIDA por ADR) sin leer el registro RESOLVE_UNKNOWN que ya cerraba A-11, guiándose por la línea de deuda «su respaldo citable no dice el momento del stop». Lección: antes de decidir sobre una ambigüedad cerrada, se lee el registro que la cierra, no solo su campo evidencia.
>
> Sigue: knowledge validate antes del primer make check; luego make check y uv run botsito state check en verde, la CI de Linux y el revisor con su informe pegado al final, comprobando aparte que G1 no tiene ninguna excepción y que el test de rotura falla cuando debe.
>
> Rama lista para revisión, NO cerrada.

## 7. Lo que cambiaba esta rama al llegar a la PARADA

- `docs/encargos/trabajo-respaldo-a11.md`, `contrato.yaml`, el Archivo 21 de `HISTORIA.md` y
  `PROJECT_STATE.md` (`Current Branch`, `Current Feature` y las dos líneas del archivo).
- Este informe.

El contrato solo permitía entonces esas rutas; las de la fase 1 se añadieron tras la respuesta (§8).

**Añadido del consultor del 2026-10-06**, copiado al final del encargo: el bot es 100 % automático
y la línea J de la Next Action queda retirada (se sustituye en el commit del contrato del cierre); y
hasta que el ADR del umbral de mayo esté en `main`, nadie ejecuta `botsito motor arnes`. Esta rama
no lo necesita. La última vez que se ejecutó fue en `trabajo/activacion-a42` (§9.5 de su informe),
antes de esta regla.

## 8. Fase 1, tras la respuesta del consultor

### 8.1 Los instantes del registro que cierra A-11, contra los tramos no citables

Anexo `anexos/RESPALDO-A11/tramos_del_cierre.py`, salida en `tramos_del_cierre-SALIDA.txt`. Lee el
registro `fb-2026-09-09-sesion-01-69711f67`, `knowledge/corpus/fuentes.yaml` (para saber qué vídeo
es su `grabacion`) y los tramos por el lector único (`botsito.corpus.cuarentena`). Ninguna
transcripción.

```
registro: fb-2026-09-09-sesion-01-69711f67 (RESOLVE_UNKNOWN sobre {'tipo': 'ambiguedad', 'id': 'A-11'})
grabacion: Grabación de pantalla 2026-09-09 151552.mp4 -> v6
tramos no citables de v6: 4
  0:01:00-0:01:03
  0:41:00-0:50:11
  1:53:30-1:57:31
  2:26:17-2:26:18
respuesta (t0-t1) 1:43:51-1:44:36: tramos que pisa: ninguno
confirmacion (notas) 2:00:01-2:00:02: tramos que pisa: ninguno
VEREDICTO: ninguno cae en un tramo
```

Ninguno cae en un tramo: no hay PARADA. La confirmación de las `notas` («Confirmado en 2:00:01») se
mide como el segundo 2:00:01–2:00:02. Una lectura de más, declarada: para localizar los campos del
fichero de tramos imprimí sus 30 primeras líneas, que traen el `motivo` y el `acordado` del tramo
0:41:00–0:50:11 de v6 (las frases con que el trader avisa de que lo que sigue no es la operativa).
Es el registro de tramos, no una transcripción; no se usa para nada.

### 8.2 A-11 y G1, en el mismo commit

- **A-11** (`knowledge/spec/ambiguedades.yaml`): sale `ev-v4-001207-0c4ffd4b` de `evidencia`; se
  queda `ev-v1-000620-0f7dea14`. Ni estado, ni clase, ni `decision`/`decidida_el`, ni la `pregunta`
  cambian. **Lo que cierra A-11 es el registro del trader `fb-2026-09-09-sesion-01-69711f67`**
  (`RESOLVE_UNKNOWN`, v6 1:43:51–1:44:36, confirmado en 2:00:01, valor «el stop completo va en la
  orden»), no ese ítem, que se queda en su `evidencia` (D-e): habla de proteger el trade «apenas se genere la
  entrada» y admite las dos lecturas (GUARDIAS-CITAS.md §8.1).
- **G1** (`src/botsito/validation/citas_supersedidas.py`): `EXCEPCIONES = ()`, con el mecanismo
  conservado y un comentario que dice desde cuándo y por qué está vacía (D-c, opción a). Tiene que
  salir en el mismo commit: con A-11 sin el id, la excepción quedaría sin uso y G1 fallaría
  (`test_caducidad_la_excepcion_sin_uso_falla`).
- **`spec docs --escribir`**: no cambia ningún fichero generado (`docs/spec/ambiguedades.md` no
  lista la evidencia de cada ambigüedad); `test_spec_docs_generados` pasa.

### 8.3 Los tests

`tests/unit/test_citas_supersedidas.py`:
- `test_la_lista_real_de_excepciones_esta_vacia`: `EXCEPCIONES == ()` (sustituye a
  `test_la_excepcion_es_exactamente_un_par`).
- Los seis del mecanismo pasan una excepción **sintética** explícita, `SINTETICA = Excepcion("A-11",
  VIEJO, "sintetica: solo prueba el mecanismo de excepciones")`, en un `knowledge/spec/` temporal;
  y uno nuevo, `test_sin_la_excepcion_el_mismo_par_falla`, prueba que sin ella el mismo par falla.
- `test_g1_sobre_el_repositorio_real_pasa_sin_ninguna_excepcion` sustituye a
  `test_caducidad_en_el_repositorio_real`: G1 sobre el repo real da `[]`, con las excepciones reales
  y con `excepciones=()`.
- **El test de rotura**, `test_rotura_cada_supersedido_real_citado_en_una_spec_hace_fallar_g1`:
  con los ítems reales, cada uno de los 13 ids supersedidos, citado solo en el `evidencia` de una
  ambigüedad de un `knowledge/spec/` temporal, da exactamente un fallo que lo nombra.

**Que el test de rotura falla cuando debe**, medido en memoria sin tocar código ni tests
(`anexos/RESPALDO-A11/rotura_g1.py`, salida en `rotura_g1-SALIDA.txt`):

```
EXCEPCIONES reales: ()
supersedidos reales: 13; con G1 tal cual, fallan 13
ROTURA 1, una excepcion para (A-11, ev-v1-000448-346d6d90): ese id da 0 fallo(s) -> el test de rotura FALLARIA
ROTURA 2, G1 sin cadenas de sustitucion: fallan 0 de 13 -> el test de rotura FALLARIA
VEREDICTO: el test de rotura pasa hoy y falla con las dos roturas
```

`tests/unit/test_kit.py`:
- `test_una_ambiguedad_puede_citar_evidencia_ya_supersedida` se reescribe con un YAML sintético en
  `tmp_path` (D-d): tres ítems sintéticos (uno supersedido por otro), la plantilla `AMBIGUEDADES` del
  propio test, y la misma comprobación de antes: con todos los ítems la cita existe; con solo los
  vivos, «no existe».
- `test_ambiguedades_reales_y_esquema` **no cambia** y pasa: A-11 sigue en las RESUELTAS (punto 4).

### 8.4 D2 en el revisor

`.claude/agents/revisor.md`, eje (a), punto 10 nuevo: «La afirmacion de cada item de evidencia
nuevo». En cada ítem que la rama añade a `knowledge/evidence/`, el revisor lee `cita_literal` y
`afirmacion` y comprueba que la afirmación no dice nada que su cita no contenga; si dice más, es un
hallazgo `importa`. Dice también por qué lo hace él (no hay comprobación automática; es un juicio de
significado) y que un ítem commiteado no se edita, se supersede. Con fecha y fuente (D2 del
consultor, 2026-10-06; hallazgo §8.3 de GUARDIAS-CITAS.md).

`tests/unit/test_revisor.py` añade ese título a los fragmentos que exige en las instrucciones, para
que no se pierda.

Toca `.claude/`: push de `fix/respaldo-a11` y CI de Linux (§9).

### 8.5 La nota sobre `ev-v6-021939-b430a110` (D2)

`ev-v6-021939-b430a110` no se toca: la evidencia es inmutable. **Su `afirmacion` excede su
`cita_literal`**:
- `cita_literal`: «Es 0.80 Ya a 0.75 Acá nada más Ahora es a 0.8 No a 0.75»;
- `afirmacion`: «el stop que se introduce en la operacion es 0,80, ya no 0,75».

La cita dice la cifra (0,80 y no 0,75); «el stop que se introduce en la operación» no está en ella.
**Y no respalda el momento del stop**: no dice si el stop va en la orden pendiente o se pone tras el
llenado, que es lo que pregunta A-11. Es el sustituto de `ev-v4-001207-0c4ffd4b`, y por eso A-11 no
lo cita en su lugar.

### 8.6 PROJECT_STATE y la deuda

- Sale de Technical Debt «A-11 RESUELTA cita un ítem supersedido; su respaldo citable no dice el
  momento del stop; excepción en G1 hasta que decida el consultor (docs/validation/GUARDIAS-CITAS.md
  §8).» (180 bytes) y entra en `docs/state/HISTORIA.md` bajo «# Technical Debt PAGADA · sale de
  PROJECT_STATE.md en trabajo/respaldo-a11 (2026-10-07)», con el porqué.
- **Saldo de bytes:** 23.809 frente a los 23.826 de `main`. **−17 en total**, contando lo que
  añaden `Current Branch` y `Current Feature`, que el cierre devuelve. La línea de deuda que sale mide
  180 bytes (en §6 se dijo 177: era un recuento mal hecho).
- La Next Action no se toca: U sale en el commit del contrato del cierre.

### 8.7 El hallazgo del consultor, para el cierre

Para la fila de la rama en ERRORES-RECURRENTES (va en la orden de cierre; esa tabla no se toca
aquí): importa. El consultor decidió D1 (DECIDIDA por ADR) sin leer el registro `RESOLVE_UNKNOWN`
que ya cerraba A-11, guiándose por la línea de deuda «su respaldo citable no dice el momento del
stop». Lección: antes de decidir sobre una ambigüedad cerrada, se lee el registro que la cierra, no
solo su campo `evidencia`.

Una nota de la sesión, para la misma fila: la fase 0 lo tenía en su §1 (quién cierra A-11) y aun
así propuso cinco decisiones sobre la vía de DECIDIDA sin preguntar si A-11 necesitaba cambiar de
estado. La premisa del encargo no se discutió.

## 9. Comprobaciones, comandos y salidas de la fase 1

En este orden, sobre el árbol estadiado del commit `2f230fe` (el de la fase 1):

| Comando | Salida |
|---|---|
| `uv run python docs/validation/anexos/RESPALDO-A11/tramos_del_cierre.py` | `VEREDICTO: ninguno cae en un tramo` (§8.1) |
| `uv run python docs/validation/anexos/RESPALDO-A11/rotura_g1.py` | `VEREDICTO: el test de rotura pasa hoy y falla con las dos roturas` (§8.3) |
| `uv run botsito spec docs --escribir` | `OK` en los cuatro `docs/spec/*.md`, sin cambios en ninguno |
| `uv run pytest tests/unit/test_citas_supersedidas.py tests/unit/test_kit.py tests/contract/test_spec_docs_generados.py -q` | todo en verde |
| `uv run pytest tests/unit/test_revisor.py -q` | todo en verde |
| `uv run botsito knowledge validate` (antes del primer `make check`, a un fichero temporal) | exit 0, ningún `ERROR` |
| `uv run botsito state check` | primero `ERROR: 'Tests Currently Passing' dice 1357; hay 1359 funciones de test`; corregido el recuento, `OK: rama 'trabajo/respaldo-a11' …` |
| `uv run python scripts/contrato_rama.py` | `CONTRATO: 15 ficheros dentro del contrato de trabajo/respaldo-a11 (riesgo medio, artefacto docs/validation/RESPALDO-A11.md, 6 comprobaciones para el revisor)` |
| `make check > make-check.log 2>&1` | exit 0; `2102 passed`; `SELLO: make check en verde sobre el arbol 809f43e4f596498e725968ee5bc1f0c5be883b38` (el de `2f230fe`) |
| `git push origin trabajo/respaldo-a11:refs/heads/fix/respaldo-a11` | `* [new branch] trabajo/respaldo-a11 -> fix/respaldo-a11` (esta vez el clasificador no lo negó) |
| CI de Linux sobre `2f230fe` | **run #229** (`37574263700`): 1 failed, 2093 passed, 8 skipped. El único fallo es el aceptado, `tests/unit/test_cli.py::test_state_check_ok_on_real_repo` («PROJECT_STATE declara la rama 'trabajo/respaldo-a11'; la rama actual es 'fix/respaldo-a11'») |

**Nadie ejecutó `botsito motor arnes`** en esta rama (añadido del consultor del 2026-10-06).

Los commits de la rama: `68e9392` (apertura con la fase 0), `553de27` (el añadido del consultor al
encargo), `2f230fe` (la fase 1) y el de este informe del revisor. La CI de este último va en el
mensaje al consultor: un commit no puede llevar su propia CI, y solo toca el informe.

## 10. Lo que se hizo con los hallazgos del revisor

| # | Gravedad | Qué se hizo |
|---|---|---|
| a1 | menor | La «Cómo se lee» ya no habla de un ADR que no hay, y las referencias a «§9» existen ahora (este apartado). |
| a2 | menor | §6 dejaba 177 bytes: lleva una nota que remite a §8.6 (180, medido); la puntuación de §8.6, arreglada (la había roto una sustitución de separadores de miles al escribir el saldo). |
| a3 | menor | §8.2 ya no dice que `ev-v1-000620-0f7dea14` «abrió la pregunta»: dice que se queda en la `evidencia` (D-e), qué dice y que admite las dos lecturas. |
| b1 | importa | §9 recoge los comandos de la fase 1 y sus salidas: `knowledge validate`, `state check` (con su primer rojo), el contrato, `make check` con el sello y la CI de Linux con su run. |

Las dos comprobaciones aparte del revisor dan SÍ: G1 sin ninguna excepción, y el test de rotura
falla cuando debe (repitió el anexo; su contraste propio en memoria lo bloqueó la guardia de Claude
Code y no lo rodeó).

## Informe del revisor (subagente `revisor`, 2026-10-07), tal cual

## Informe del revisor · trabajo/respaldo-a11 · 2026-10-07

Base `main` d96b703 (merge-base verificado). Commits 68e9392, 553de27 y 2f230fe. `git status --short` limpio. Encargo `docs/encargos/trabajo-respaldo-a11.md`, que lleva el añadido del consultor y su respuesta a la PARADA. La respuesta SUSTITUYE D1, y la he tomado como el encargo vigente.

### Las dos comprobaciones aparte

**1. G1 no tiene ninguna excepción: VEREDICTO SÍ, se sostiene.**
- `src/botsito/validation/citas_supersedidas.py:51` dice `EXCEPCIONES: tuple[Excepcion, ...] = ()`. `EXCLUIDOS` (línea 46) también está vacío.
- `tests/unit/test_citas_supersedidas.py:155-157`, `test_la_lista_real_de_excepciones_esta_vacia`, exige `EXCEPCIONES == ()`.
- `test_g1_sobre_el_repositorio_real_pasa_sin_ninguna_excepcion` (líneas 216-224) comprueba que G1 sobre el repo real da `[]`, y que da `[]` también con `excepciones=()`.
- Con `uv run pytest tests/unit/test_citas_supersedidas.py -q -rA`, los 26 tests dan PASSED y ninguno FAILED. Entre ellos están los tres de arriba.
- Ningún fichero de `knowledge/spec/` cita un id supersedido suelto. Los 13 supersedidos reales salen de `knowledge/evidence/` con Grep de `^supersede:`. Los ids buscados en `knowledge/spec/` aparecen solo dos veces. En `strategy_spec.yaml:1633` y en `ambiguedades.yaml:1100` el id va junto a su sustituto, en el mismo valor o en la misma línea de comentario (`ambiguedades.yaml:1100` es un comentario), y G1 lo admite.
- `ev-v4-001207-0c4ffd4b` ya no aparece en `knowledge/spec/` (Grep: 0 apariciones) ni en `docs/spec/`.
- El diff de `knowledge/spec/ambiguedades.yaml` es una sola línea quitada: `-      - ev-v4-001207-0c4ffd4b`.
- Nada más usa el mecanismo de excepciones de G1. `git grep EXCEPCIONES` solo trae `citas_supersedidas.py` y su test; los demás resultados son otros `EXCEPCIONES` no relacionados (`corpus/cuarentena.py`, `test_historial_sin_git.py`).

**2. El test de rotura falla cuando debe: VEREDICTO SÍ, con una salvedad.**
- Repetí `uv run python docs/validation/anexos/RESPALDO-A11/rotura_g1.py`. La salida es idéntica a `rotura_g1-SALIDA.txt`:
  - `supersedidos reales: 13; con G1 tal cual, fallan 13`, con 1 fallo por id.
  - `ROTURA 1 ... ese id da 0 fallo(s) -> el test de rotura FALLARIA`.
  - `ROTURA 2 ... fallan 0 de 13 -> el test de rotura FALLARIA`.
  - `VEREDICTO: el test de rotura pasa hoy y falla con las dos roturas`.
- Leí el anexo. La comprobación que hace es la misma que `test_rotura_cada_supersedido_real_citado_en_una_spec_hace_fallar_g1` (líneas 227-243): un `knowledge/spec/` temporal por id, con los ítems reales y las excepciones reales. Las dos roturas (excepción para un par real, y `sustitutos` ciego) se hacen en memoria y los ficheros temporales van fuera del repo.
- Los 13 supersedidos del anexo coinciden con los 13 `supersede:` que saqué con Grep de `knowledge/evidence/`.
- Mi contraste propio en memoria NO pude ejecutarlo. Lo intenté dos veces con `uv run python -` y la guardia de Claude Code lo bloqueó: la primera por `Path(".")`, la segunda por derivar la raíz de `__file__`. No lo rodeé. Lo sustituye lo anterior más los PASSED del test real.
- Salvedad, no es hallazgo: el test de rotura cubre solo una excepción para un par de A-11. Una excepción para otra ambigüedad no la cazaría él, pero sí `test_la_lista_real_de_excepciones_esta_vacia`.

### Eje (a) · Reglas de la casa
Resumen: 0 bloquea, 0 importa, 3 menor.

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| 1 | menor | El informe conserva texto de la fase 0 que la respuesta dejó sin objeto, fuera de lo ya declarado en §8.7. La «Cómo se lee» dice «El ADR nuevo se nombra sin su id hasta que exista» y no hay ADR. §8.4 y §8.6 remiten a un «§9» que no existe. | `docs/validation/RESPALDO-A11.md:12-14`, `:310`, `:349-354` (no hay `## 9`) |
| 2 | menor | Cifras de bytes inconsistentes dentro del informe. §6 dice que la línea de deuda mide 177 bytes y que el saldo será −177. §8.6 dice 180. La medida real son 180. §8.6 tiene además puntuación rota («−17 en total**. contando…», «que el cierre devuelve. Las ediciones… −180.»). | `RESPALDO-A11.md:181-182` frente a `:326-332`. `git show main:PROJECT_STATE.md \| grep "A-11 RESUELTA cita" \| wc -c` da 180 |
| 3 | menor | §8.2 dice que `ev-v1-000620-0f7dea14` «se queda como la evidencia que abrió la pregunta». Ni el ítem ni el informe lo respaldan. El ítem trata de proteger el trade en 0,75 apenas se genere la entrada, y las dos lecturas son posibles (GUARDIAS-CITAS §8.1). No es lo que pidió el consultor, que era decir que el registro del trader cierra A-11. | `RESPALDO-A11.md:256-257`. `knowledge/evidence/v1/ev-v1-000620-0f7dea14.yaml:7-9` |

Comprobado sin hallazgos:
- **Contrato.** `uv run python scripts/contrato_rama.py` dio: «CONTRATO: 15 ficheros dentro del contrato de trabajo/respaldo-a11 (riesgo medio, artefacto docs/validation/RESPALDO-A11.md, 6 comprobaciones para el revisor)».
- **Comprobaciones del contrato:**
  - `tramos_del_cierre.py`: «VEREDICTO: ninguno cae en un tramo».
  - `rotura_g1.py`: OK, ver arriba.
  - `pytest` de `test_citas_supersedidas.py`, `test_kit.py` y `test_revisor.py`: 101 puntos, sin una sola F y exit 0. El resumen final de pytest no sale en este entorno.
  - `uv run botsito knowledge validate` (lo ejecuté sin redirigir a fichero): todo OK, también «OK: 55 ambiguedades registradas», «OK: 152 registros de feedback, historial intacto, commits con Fuente» y «OK: 503 items de evidencia … historial intacto». Los AVISO que salen son los de siempre.
  - `uv run botsito state check`: «OK: rama 'trabajo/respaldo-a11' …».
  - `make check` no lo ejecuté. `make-check.log` tiene `2102 passed in 1014.93s`, `SELLO: … 809f43e4f596498e725968ee5bc1f0c5be883b38` y `PICO DE MEMORIA … 290 MiB`. Ese árbol coincide con `git rev-parse 'HEAD^{tree}'` = 809f43e4…, el de 2f230fe.
- **Trailer `Fuente:`.** El único commit que toca `knowledge/spec/` es 2f230fe. Lleva `Fuente: fb-2026-09-09-sesion-01-69711f67` en el cuerpo, y ese registro existe en `knowledge/feedback/2026-09-09-sesion-01/`. `knowledge validate` confirma «commits con Fuente».
- **Holdout y material.** No hay cambios en `knowledge/cases/`, `knowledge/corpus/`, `data/`, `knowledge/evidence/` ni `knowledge/feedback/`. `git diff --name-status main...HEAD` solo trae `A` en contrato, encargo, informe y anexos, y `M` en el resto de ficheros permitidos. El informe no abre transcripciones, libros ni fotogramas. La única lectura de más, las 30 líneas de `tramos_no_citables.yaml`, ya está declarada (§8.1) y no la repito.
- **Ambigüedades.** `docs/spec/ambiguedades.md:243-247` no lista la evidencia de A-11, así que no necesita regenerarse. `tests/contract/test_spec_docs_generados.py` pasa (exit 0). La rama no abre ni cierra ninguna ambigüedad, así que la tabla de PROJECT_STATE y `AMBIGUEDADES.md` no se tocan.
- **A-11 sin cambios salvo la evidencia.** Misma `pregunta`, `estado: RESUELTA`, `decision: null`, `decidida_el: null`, sin `clase`. Solo queda `ev-v1-000620-0f7dea14`, que existe y no está supersedido.
- **`test_ambiguedades_reales_y_esquema` no cambió.** Los hunks de `tests/unit/test_kit.py` están todos entre las líneas 1392 y 1432, dentro del test de la evidencia supersedida. `test_kit.py` pasa.
- **Instantes del registro y tramos.**
  - `fb-2026-09-09-sesion-01-69711f67` es `RESOLVE_UNKNOWN` sobre A-11 en v6, con t0 1:43:51, t1 1:44:36 y la confirmación «Confirmado en 2:00:01» en sus notas.
  - Los tramos de v6, según el anexo, son 0:01:00-0:01:03, 0:41:00-0:50:11, 1:53:30-1:57:31 y 2:26:17-2:26:18. Ninguno pisa 1:43:51-1:44:36 ni 2:00:01.
  - El anexo solo lee yaml.
- **D2 en el revisor.** `.claude/agents/revisor.md` tiene el punto 10, «La afirmacion de cada item de evidencia nuevo». `tests/unit/test_revisor.py` lo exige (diff +2 líneas) y pasa.
- **PROJECT_STATE.** `main` pesa 23.826 bytes y la rama 23.809 (`wc -c`). El saldo es −17, o sea ≤ 0. La Next Action no cambia y U sigue en ella. HISTORIA solo gana líneas, con el Archivo 21 y «# Technical Debt PAGADA · sale de PROJECT_STATE.md en trabajo/respaldo-a11 (2026-10-07)», que lleva la línea de deuda exacta. El recuento de tests pasa de 1357 a 1359 y `state check` da OK; el diff de tests es +2 neto, que coincide.
- **Citas del informe contra su fuente.** `ev-v6-021939-b430a110`: `cita_literal` y `afirmacion` coinciden tal cual con §8.5. `ev-v1-000620-0f7dea14`: la cita coincide con §4. `fb-…-69711f67`: el `valor_resultante` coincide con lo que dice el informe. El segundo, `RESOLVE_UNKNOWN`, y el `supersede` del ítem `ev-v6-021939-b430a110` hacia `ev-v4-001207-0c4ffd4b` son correctos.
- **Las tres guardias de una `cita`.** La rama no añade ningún sitio con `cita`.
- **Ítems de evidencia nuevos (punto 10).** La rama no añade ninguno, así que no hay afirmación que contrastar.
- **ADR.** La rama no crea ni cambia ningún ADR.
- **Informes cerrados.** La rama no modifica ningún `docs/validation/*.md` previo.
- **`motor arnes`.** No lo ejecutó ningún comando que aparezca en el informe. Las únicas apariciones son el recordatorio de la regla (`RESPALDO-A11.md:216-220`) y el texto del encargo.
- **Cifras.** No hay ninguna cifra de negocio nueva.
- **CI de Linux.** `origin/fix/respaldo-a11` está en 2f230fe, el HEAD de la rama. No pude ver el resultado del run.

### Eje (b) · Encargo
Resumen: 0 bloquea, 1 importa, 0 menor. Requisitos: 22 hechos, 3 parciales, 0 no hechos.

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 1 | A-11 pierde `ev-v4-001207-0c4ffd4b`, conserva `ev-v1-000620-0f7dea14` | Hecho | `knowledge/spec/ambiguedades.yaml:178-179` (diff: una línea quitada) |
| 2 | A-11 sin cambio de estado, clase, decision/decidida_el ni pregunta | Hecho | Mismo diff; A-11 en 170-185 |
| 3 | Medir y dejar en el informe que 1:43:51-1:44:36 y 2:00:01 no caen en tramos | Hecho | `RESPALDO-A11.md:224-248`, anexo repetido |
| 4 | Trailer `Fuente: fb-2026-09-09-sesion-01-69711f67` | Hecho | `git log` del commit 2f230fe |
| 5 | `spec docs --escribir` en el mismo commit si cambia algo generado | Hecho | No cambia nada generado; `test_spec_docs_generados` pasa |
| 6 | `EXCEPCIONES = ()` con el mecanismo conservado | Hecho | `citas_supersedidas.py:47-51`, y `Excepcion` y los parámetros siguen |
| 7 | Test que exige la lista vacía | Hecho | `test_citas_supersedidas.py:155-157` |
| 8 | Tests del mecanismo con una excepción sintética | Hecho | `:144` (`SINTETICA`), `:160-213` |
| 9 | Test que rompe a propósito con cada id supersedido real | Hecho | `:227-243` |
| 10 | D-d: `test_una_ambiguedad_puede_citar_evidencia_ya_supersedida` con YAML sintético en `tmp_path` | Hecho | `test_kit.py:1392-1435` (diff) |
| 11 | `test_ambiguedades_reales_y_esquema` no cambia | Hecho | Hunks de `test_kit.py` en 1392-1432 |
| 12 | D2 en el revisor | Hecho | `.claude/agents/revisor.md` punto 10, más `test_revisor.py` |
| 13 | Nota sobre `ev-v6-021939-b430a110` (afirmación que excede la cita, no respalda el momento del stop) | Hecho | `RESPALDO-A11.md:312-322`; el ítem no se toca |
| 14 | El informe dice que A-11 la cierra el registro del trader, no el ítem | Hecho | `RESPALDO-A11.md:252-257` |
| 15 | Deuda de A-11 a HISTORIA bajo «# Technical Debt PAGADA» | Hecho | Diff de HISTORIA |
| 16 | Saldo de bytes de PROJECT_STATE ≤ 0 | Hecho | 23.809 frente a 23.826, es decir −17 |
| 17 | La Next Action no se toca | Hecho | Diff de PROJECT_STATE, sin hunks en Next Action |
| 18 | La respuesta del consultor copiada tal cual al encargo y al informe | Hecho | `encargo:47-69` y `RESPALDO-A11.md:184-206` (el texto coincide) |
| 19 | No cambia motor, parámetros, `strategy_spec`, evidencia, cifras; no se toca material reservado | Hecho | `git diff --name-status`, ninguna ruta protegida del contrato |
| 20 | Nadie ejecuta `botsito motor arnes` | Hecho | `grep -i "motor arnes"` solo da menciones de la regla |
| 21 | `knowledge validate` antes del primer `make check`; luego `make check` y `state check` en verde | Parcial | En verde en mi comprobación (sello 809f43e4 = árbol del HEAD, `state check` OK, `knowledge validate` OK). El informe NO recoge ninguno de los tres resultados |
| 22 | Push de `fix/respaldo-a11`, CI de Linux y su número de run | Parcial | Empujada en 2f230fe (`git rev-parse origin/fix/respaldo-a11`). Número de run y resultado, pendientes; el informe lo declara en «Estado». El encargo lo pide en el cierre |
| 23 | Informe: encargo frente a lo hecho, desviaciones, comandos y salidas | Parcial | Hay desviaciones (§6.1, §8.7) y varias salidas. Falta una lista de comandos con salida de la fase 1, y la comparación encargo-hecho está repartida en §8 |
| 24 | Revisor con su informe pegado al final del informe, con las dos comprobaciones aparte | Hecho (por mi parte) | Es de quien llamó pegarlo: no lo he pegado yo |
| 25 | Rama «lista para revisión», NO cerrada | Hecho | `RESPALDO-A11.md:349` «EN CURSO», sin cierre en `main` |

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| 1 | importa | El encargo pide `knowledge validate` antes del primer `make check`, después `make check` y `state check` en verde, y que el informe lleve «comandos y salidas». La fase 1 del informe no recoge el resultado de ninguna de esas tres comprobaciones, ni una lista de comandos con salida. Solo el log de `make check` (ignorado por git) tiene el sello. Quien lea el informe no puede comprobar que la fase 1 pasó. | Ningún resultado de `knowledge validate`, `state check` ni `make check` en `RESPALDO-A11.md:222-354`. El único `knowledge validate` del informe es la medida de la fase 0 (`:79`) |

Hecho de otra forma: ninguno. D1, la ADR 0070 y la vía DECIDIDA no se hicieron porque la respuesta del consultor los sustituyó, y el informe lo declara en §6.1 y §8.7.

### Lo que no pude comprobar
- Mi contraste propio en memoria del test de rotura: lo bloqueó la guardia de Claude Code (ver arriba). No lo rodeé.
- El resultado de la CI de Linux de `fix/respaldo-a11`: no tengo `gh` ni red en esta revisión, y el informe declara que puede seguir corriendo. Solo confirmé que la rama remota está en 2f230fe.
- `make check` sobre el árbol: no lo ejecuté. Me apoyo en `make-check.log` (2102 passed, sello 809f43e4…), cuyo árbol coincide con el HEAD, y en que `state check` sobre el HEAD da OK.
- `git write-tree` y `git branch` los bloqueó el hook de solo lectura. No eran necesarios.
- El resumen final de pytest: no sale en este entorno, así que el recuento total de las tres suites lo deduzco de los puntos (101).

### Comandos ejecutados
1. `git branch --show-current`, `git merge-base main HEAD`, `git log --format='%h %s' main..HEAD`, `git diff --stat main...HEAD`, `git status --short`, `git diff --name-status main...HEAD`.
2. `git diff main...HEAD -- knowledge/spec/ambiguedades.yaml src/botsito/validation/citas_supersedidas.py .claude/agents/revisor.md tests/unit/test_revisor.py tests/unit/test_kit.py PROJECT_STATE.md`.
3. `git log --format='%h%n%B---' main..HEAD -- knowledge/spec knowledge/cases`.
4. `uv run python scripts/contrato_rama.py`.
5. `uv run python docs/validation/anexos/RESPALDO-A11/tramos_del_cierre.py`.
6. `uv run python docs/validation/anexos/RESPALDO-A11/rotura_g1.py`.
7. `uv run pytest tests/unit/test_citas_supersedidas.py tests/unit/test_kit.py tests/unit/test_revisor.py -q`, dos veces, con exit 0 en la segunda.
8. `uv run botsito knowledge validate` y `uv run botsito state check`.
9. `uv run pytest tests/unit/test_citas_supersedidas.py -q -rA`.
10. `uv run pytest tests/contract/test_spec_docs_generados.py -q` (exit 0).
11. `git diff -U0 main...HEAD -- knowledge/spec/ambiguedades.yaml` y `git diff -U0 main...HEAD -- tests/unit/test_kit.py`.
12. `git grep -n "EXCEPCIONES" -- src tests scripts .claude`.
13. `git show main:PROJECT_STATE.md | wc -c`, `wc -c < PROJECT_STATE.md`, y las variantes del recuento de bytes de la línea de deuda.
14. `git diff main...HEAD -- docs/state/HISTORIA.md` (filtrado con grep).
15. `git diff main...HEAD --name-only -- .claude src/botsito/engine`.
16. `git grep -n -i "motor arnes"` en el informe y el encargo.
17. `grep` sobre `make-check.log`; `git rev-parse HEAD`, `git rev-parse 'HEAD^{tree}'`, `git rev-parse origin/fix/respaldo-a11`, `git for-each-ref` filtrado por «respaldo».
18. Grep y Read sobre `knowledge/spec`, `docs/spec`, `knowledge/evidence` y `knowledge/feedback`.
19. Bloqueados, sin efecto: `git write-tree` (hook de solo lectura, error mío), `git branch -a`, un `git grep` con `$(...)`, y dos `python -` en memoria.

## Estado

**LISTA PARA REVISIÓN, NO cerrada (2026-10-07).**

- A-11 sigue RESUELTA por el registro del trader que la cierra (`fb-2026-09-09-sesion-01-69711f67`)
  y ya no cita el ítem supersedido.
- G1 no tiene ninguna excepción; el test de rotura pasa hoy y falla con las dos roturas medidas.
- D2 está en el revisor (punto 10 del eje a); la nota sobre `ev-v6-021939-b430a110`, en §8.5.
- La deuda de A-11, pagada; PROJECT_STATE, −17 bytes sobre `main`.
- CI de Linux: run #229 sobre `2f230fe`, solo el fallo aceptado por el nombre `fix/`.
- Revisor: 0 bloquea, 1 importa, 3 menor; los cuatro, resueltos (§10).
- Para el cierre: el hallazgo del consultor de §8.7 va a la fila de ERRORES-RECURRENTES, y U sale de
  la Next Action con la orden de cierre (y J, según el añadido del consultor).
