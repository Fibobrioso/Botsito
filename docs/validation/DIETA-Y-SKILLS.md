# FUNCTIONALITY VALIDATION REPORT · La dieta de PROJECT_STATE y las skills

**Funcionalidad:** menos contexto por sesion y los rituales repetidos como una sola orden.
**Rama:** `trabajo/dieta-y-skills`, desde `main` en `df6aa2c` (`stable/F36j-guardia-linux`).
**Encargo:** `docs/encargos/trabajo-dieta-y-skills.md` (copia literal). **Contrato:** `contrato.yaml`,
riesgo medio.
**Objetivo:** que cada sesion cargue menos contexto y que los rituales repetidos sean una sola orden.
No cambia motor, spec, knowledge ni ninguna cifra: el diff no toca `knowledge/`, `config/`,
`src/botsito/{engine,domain,spec}/` ni `docs/adr/` (`rutas_protegidas` del contrato).

## 0. La guardia de borrado remoto

**Que cambia.** Hasta hoy `.claude/hooks/guardia.py` bloqueaba todo `git push` que borrara una
referencia remota (`--delete`, `-d` o un refspec `:<ref>`), y `RITUAL.md` manda borrar la
`fix/<rama>` que se empuja para la CI de Linux. Ahora `decidir_borrado_remoto` niega por defecto y
solo deja pasar ramas que casen con `RAMA_BORRABLE`: `trabajo/`, `feature/` o `fix/` (con o sin
`refs/heads/`), nombradas una a una, sin `..` ni `.lock`. Todo lo demas se bloquea, y un borrado de
varias referencias se bloquea ENTERO si una sola no casa: `main`, cualquier tag (`stable/*` y
`refs/tags/*` citan la regla de los tags, `R_TAG`), un comodin, un refspec vacio (`git push origin :`)
y una referencia construida al ejecutarse (`$RAMA`).

**Lo que hice de mas, y por que** (todo dentro de «cualquier comando que no pueda decidir con
seguridad»):
- `.claude/settings.json`: la regla `deny` `Bash(git push * --delete *)` denegaba cualquier borrado
  ANTES de que la guardia lo viera, asi que el encargo no se podia cumplir sin tocarla. Se parte en
  `--delete main*`, `--delete stable/*`, `--delete refs/tags/*`, `:main*`, `:stable/*` y
  `:refs/tags/*`. La decision fina es de la guardia; `settings.json` es el cinturon.
- `git push --prune` se bloquea: borra ramas remotas sin nombrarlas.
- Un refspec construido al ejecutarse se bloquea tambien en un push SIN `--delete`: `$X` podria
  valer `:main`.
- PowerShell no miraba el borrado remoto en absoluto; ahora aplica la misma decision a cada
  `git ... push` de la linea (y un `$` en un argumento lo bloquea).

**Lo que queda, dicho:** un nombre a secas (`fix/x`) lo resuelve git contra las ramas y los tags del
remoto; si existiera un TAG llamado `fix/x` y ninguna rama, `--delete fix/x` borraria el tag. En
este repo los tags son `stable/*` y ninguno empieza por `trabajo/`, `feature/` o `fix/`.

**Tests** (`tests/unit/test_guardia_claude.py`): `test_se_puede_borrar_una_rama_remota_de_trabajo`
(6 formas, entre ellas `--delete fix/x`, `:fix/x` y el push `trabajo/x:refs/heads/fix/x` del
ritual); `test_no_se_borra_main_ni_un_tag_ni_lo_que_no_se_puede_decidir` (17: `main`,
`stable/F36j-guardia-linux`, `refs/tags/x`, `--delete fix/x main`, `--delete fix/x stable/...`,
`:fix/x :main`, comodin, `..`, `$RAMA`, `--prune`, `:` a secas...);
`test_borrar_un_tag_remoto_cita_la_regla_de_los_tags`; `test_powershell_borra_solo_ramas_de_trabajo`
(6). La lista `RITUAL` gana el push a `fix/<rama>` y su borrado, y el test de `settings.json`
comprueba que ninguna `deny` toca `--delete fix/x` y que siguen denegados `main`, `refs/tags/` y
`:stable/`. Medido a mano el motivo de cada bloqueo (que salta por lo que debe y no por otra cosa):
`--delete fix/x main` → «borra la referencia remota `main`»; `"$RAMA"` → «se construye al
ejecutarse»; `--prune` → «borra ramas remotas sin nombrarlas».

**La CI de Linux** (regla de `RITUAL.md`, porque toca un hook): PENDIENTE, se rellena al empujar.

## 1. La dieta de PROJECT_STATE.md

### 1.1 Tamanos

| Fichero | Antes (`df6aa2c`) | Despues |
|---|---|---|
| `PROJECT_STATE.md` | 418.819 bytes (904 lineas) | 20.619 bytes |
| `docs/state/HISTORIA.md` | — | 419.885 bytes (cabecera de 1.066 + el original entero) |
| `CLAUDE.md` | 20.554 bytes | 14.983 bytes |

El encargo decia 407 KB: son 418.819 bytes = 409 KiB.

### 1.2 Que se queda en PROJECT_STATE.md

Las once secciones que exige ahora `tests/unit/test_project_state.py`, y ninguna mas: Current
Branch, Current Feature, Stable Main State (la primera linea: `main` y su ultimo tag), Last Stable
Commit, Tests Currently Passing (el numero y un puntero), Next Action, Known Ambiguities, Technical
Debt, Reglas vivas, Completed Features y Change Log (estas dos, lo cerrado desde el ultimo archivo:
hoy, nada). Lo compone `docs/validation/anexos/DIETA-Y-SKILLS/construir.py` a partir de la salida
de `dieta.py`; **cada trozo que conserva se busca literal en el original y el guion se para si no
esta**. Lo unico escrito de nuevo son los marcos de cada seccion (que hay y donde esta lo demas) y la
linea J.

Decisiones, todas mias y todas revisables:
- **Next Action vigente = lo que no esta HECHO.** De la lista AHORA quedan A, E, F, H e I, tal cual.
  B, C, D y G dicen HECHA y se quedan en HISTORIA; lo que dos de ellas dejan pendiente va citado
  literal en una linea («El item nuevo ev-v7-001550-82e5cffc espera la revision del consultor», de
  D, y el break even de una venta que salta por el ASK, ADR-0065 §6, de G). Debajo de la lista habia
  ~29 KB de «LO QUE DECIA…», «LO QUE ERA AHORA…» y los puntos 0 a 37: pasan a HISTORIA, y una linea
  lista, con un criterio MECANICO (sin HECHO ni HECHA en su propia linea), los que siguen sin
  marca: A2, A3 y sus ramas, A4, A5 y los puntos 2, 6, 7, 8, 9, 10, 12, 15, 22, 23, 25, 27, 30, 34,
  35, 36 y 37. No juzgo cuales siguen vivos: eso es del consultor.
- **Known Ambiguities = las ABIERTAS**, con columnas que salen del YAML (id, titulo, clase,
  bloqueante, resuelve en). La cuarta columna de antes -notas de estado que se iban alargando- queda
  en HISTORIA y la pregunta entera en `docs/spec/ambiguedades.md`. El test anti-deriva se endurece:
  `test_project_state_refleja_las_ambiguedades_abiertas` exige exactamente las `ABIERTA` y compara
  titulo, clase, bloqueante y «resuelve en». De «Open Questions» se conserva, tal cual, la linea de
  las candidatas a ambiguedad sin abrir (C1 a C7).
- **Technical Debt = una linea por deuda abierta**: el ARRANQUE literal de su entrada (hasta el
  primer parentesis con fecha, o la entrada entera si es corta), con el texto entero en HISTORIA.
  Fuera quedan las 15 entradas que su PROPIO texto daba por cerradas: n.os 7 (RESUELTA), 8
  (DECIDIDO), 10 (RESUELTA, con el bloque `ids-inexistentes`), 11 (CORREGIDA), 16 (DECIDIDA), 25
  (CERRADA), 39 (APLICADO), 40 (REGISTRADOS), 41 (RESUELTO), 44 (RESUELTOS), 45 (REGISTRADO), 46
  (RESUELTA), 47 (CERRADA), 50 (CERRADA) y 51 (HECHO). Quedan 39. La de «LOS CINCO PATRONES DE
  DEFECTO» es una regla, no una deuda: va ENTERA a `docs/runbooks/ERRORES-RECURRENTES.md` y aqui
  queda su arranque con el puntero.
- **Reglas vivas que solo estaban aqui**, copiadas tal cual con su titulo de entonces: «Things That
  Must Not Be Changed», «Decisions and Rationale», «Known Issues» y, de «Change Regimes», las dos
  lineas que `CLAUDE.md` no dice (las particiones del holdout y la correccion de manifiestos con
  `reemplaza_a`). Las demas lineas de «Change Regimes» estan en `CLAUDE.md` con las mismas palabras.
  No se copian, y estan en HISTORIA: Project Goal y Approved Architecture (orientacion, con
  `docs/plan/MASTER_PLAN.md` como referencia), Development Strategy y How to Start a Session
  (superadas por `CLAUDE.md`), Lineamientos (hechos de negocio con su id de evidencia, que la spec
  ya cita), Expert Entry Points y Expert Validations (caducadas o vacias), Current Phase y Next
  Feature (caducadas: hablan de F12 y F14), Existing Components, Important Files, Known
  Contradictions (la deduce `evidence contradictions`) y Features Waiting for Validation (vacia).
- **El indice de ADR** (24 KB) duplicaba `docs/adr/README.md`. Sale, y la guardia que lo vigilaba
  (K-01 de la sesion 02) pasa al README con la misma fuerza: que falte, que sobre o que se repita
  (`test_el_readme_indexa_exactamente_los_adr_que_existen`).
- **Las rutas citadas**: `test_project_state_rutas.py` miraba solo «Important Files»; ahora mira
  PROJECT_STATE entero (sin `data/`, que la CI no tiene).
- **Tope**: `test_project_state_cabe_en_el_tope`, 25.000 bytes. Hoy hay 4,4 KB de margen, para que
  el commit de estado de un cierre (que anade una linea y una entrada) quepa.

### 1.3 HISTORIA.md, y que ningun texto se pierde

`docs/state/HISTORIA.md` es una cabecera y, como «Archivo 1», `PROJECT_STATE.md` ENTERO tal como
estaba en `df6aa2c`. Comprobado de dos formas:
- `git show df6aa2c:PROJECT_STATE.md` a un fichero del scratchpad y
  `tail -c 418819 docs/state/HISTORIA.md | cmp - <ese fichero>`: identicos byte a byte;
- `test_el_archivo_1_es_project_state_entero_antes_de_la_dieta`, que lo comprueba en cada
  `make check` contra el historial de git.

Asi «todo lo anterior esta en HISTORIA.md o en PROJECT_STATE.md» es literal: esta todo en HISTORIA,
y lo que PROJECT_STATE conserva es copia. **Solo se amplia**: `test_historia_solo_se_amplia` exige
que cada version commiteada empiece, byte a byte, por la de su padre, y el disco por la de `HEAD`;
`test_la_guardia_caza_una_reescritura_y_deja_pasar_lo_anadido` lo rompe a proposito.

### 1.4 El regimen desde hoy (`docs/state/README.md`)

- En PROJECT_STATE se SUSTITUYE lo que deja de ser verdad, sin «Lo anterior:».
- Al ABRIR una rama, la skill `abrir-rama` anade al final de HISTORIA un `# Archivo N` con el
  PROJECT_STATE de `main` entero (`git show main:PROJECT_STATE.md`) y vacia Completed Features y
  Change Log. Asi el cierre de cada rama -que en `main` solo puede tocar PROJECT_STATE, regla 5 de
  `state check`- lo archiva la rama siguiente, y en `main` no cambia nada mas.
- `state check`, regla 4: mira las «Completed Features» de PROJECT_STATE y de CADA archivo de
  HISTORIA (`_read_sections`; test `test_completed_features_de_la_historia_tambien_cuentan`).
- `RITUAL.md`: la lista de lo que edita el cierre pierde «Features Waiting for Validation» (ya no
  existe) y gana la regla de sustituir y el tope; el ultimo paso gana el borrado de `fix/<rama>`.

Coste aceptado: un archivo por rama, ~20 KB cada uno. HISTORIA no se lee al arrancar.

### 1.5 Lo que tarda en arrancar una sesion

PENDIENTE: se mide con `claude -p` en dos clones desechables (`git worktree add`), uno en `df6aa2c`
y otro en el commit de esta rama, con la misma orden.

## 2. CLAUDE.md con los criterios de writing-for-agents

20.554 → 14.983 bytes. Los tres criterios del encargo:

**(a) Lo que ya hace cumplir un test, un hook o el contrato queda en una linea que nombra la
guardia** («Guardia: ...»): el sello y los hooks `pre-commit`/`pre-merge-commit`; `--no-verify` y
`core.hooksPath` (guardia y `settings.json`); `cherry-pick`/`rebase` (guardia); la huella de
`make check`; la inmutabilidad de evidencia, feedback y manifiestos (hook); `libros.yaml`
(`knowledge validate`); `domain/` (import-linter); el trailer `Fuente:` (`comun/historial.py`); las
cifras fuera de la forma ejecutable (`test_no_business_literals.py`); el contrato (`make check`); el
`## Estado` de un ADR (`test_adr.py`); el heredoc sin comillas y `make check` sin fichero (guardia);
la lista de lo que bloquea la guardia de Claude Code (su cabecera); y las ambiguedades
(`test_kit.py`, `test_spec_docs_generados.py`). Se quitaron, por eso, los detalles de mecanismo que
la guardia ya contiene (p. ej. «Medido hoy: a `/dev/null` sale 1; al fichero, 0»).

**(b) Lo que solo se usa en algunos casos se muda TAL CUAL a `docs/runbooks/`**, con un puntero que
dice cuando leerlo (`docs/validation/anexos/DIETA-Y-SKILLS/mudar_claude_md.py`, que comprueba la
primera linea de cada bloque contra `git show df6aa2c:CLAUDE.md`):

| Bloque de CLAUDE.md (lineas en `df6aa2c`) | A donde |
|---|---|
| «Estan infrautilizados…»: 25.372 PNG y las recuentas de fotogramas citados (96-103) | `docs/runbooks/MIRAR-EL-MATERIAL.md` |
| Los dos recuadros «Por que cambio esta regla» (142-161) | idem |
| «COMO SE ABRE UN FOTOGRAMA», el reloj de FX Replay UTC+2 FIJO y «fijar el huso de las dos fuentes» (163-187) | idem |
| «Donde esta el texto de las transcripciones» entera (230-243) | idem |
| «Abrir una ambiguedad toca dos sitios; cerrarla, cuatro» y «Cerrar una ambiguedad toca cuatro sitios…» (191-210) | `docs/runbooks/AMBIGUEDADES.md`, con un recuadro: desde hoy la tabla de PROJECT_STATE lleva solo las abiertas |

En `CLAUDE.md` queda de cada uno la regla corta: el fotograma por instante localizado (ADR-0038) y
el agregado que se declara el mismo dia; «antes de abrir fotogramas, leer transcripciones o comparar
el video con las velas: MIRAR-EL-MATERIAL.md»; «antes de abrir, editar o cerrar una ambiguedad:
AMBIGUEDADES.md»; y la «regla de la regla» (una prohibicion que no salga de un ADR se revisa contra
el ADR), con la historia de las tres veces en el runbook.

Acortado sin mudar (la fuente sigue en su sitio): las citas literales de ADR-0021 §1, ADR-0025 §4 y
`HOLDOUT-EXPOSICIONES.md` dentro del punto 3 quedan como referencia al ADR; «Paso el 2026-09-29
(PROJECT_STATE.md, Next Action A4)» del recorte por memoria pasa a `ERRORES-RECURRENTES.md`.

**(c) Las prohibiciones, primero en positivo**: «el orden de un commit es siempre el mismo» antes de
«NUNCA `--no-verify`»; «el trabajo entra por commits y merges» antes de `cherry-pick`/`rebase`; «la
raiz sale de un argumento o de una variable de entorno» antes de `sed`; «lo que haya que escribir
espera» antes de la huella; «un registro nuevo» antes de «nunca se edita»; «la forma ejecutable
nombra el parametro» en vez de «las cifras no van en la forma ejecutable»; el titulo de la seccion
de ramas pasa a «Se trabaja en una rama: main no se toca». Las citas literales que hace la guardia
(`R_NO_VERIFY`, `R_CHERRY`, `R_DEVNULL`, `R_HEREDOC`) y los nombres de seccion que cita siguen
estando en `CLAUDE.md`, y la frase exacta del revisor que exige `tests/unit/test_revisor.py`
tambien.

## 3. Las skills del proyecto (`.claude/skills/`)

| Skill | Que hace | Quien la invoca |
|---|---|---|
| `cerrar-rama` | recorre `RITUAL.md` entero: contrato fuera, CI de Linux si toca la plataforma, merge, tag, PROJECT_STATE, `make check` sellado, commit de estado, push atomico, CI en verde, borrado de la rama y de su `fix/<rama>` | SOLO el usuario (`disable-model-invocation: true`): `/cerrar-rama <rama> <tag>` ES la orden de cierre; sin orden de Aleks se para |
| `abrir-rama` | base comprobada, rama, encargo tal cual, `contrato.yaml`, Archivo N de PROJECT_STATE en HISTORIA, `state check` y contrato antes del sello, primer commit | Claude, cuando Aleks pide una rama nueva |
| `ingerir-sesion` | registro, audio, transcripcion, cuarentena, fotogramas, extraccion por pregunta y evidencia, hasta el informe de extraccion; no resuelve nada | Claude, cuando llega una grabacion de sesion |

Cada una tiene Entradas, Limites, Herramientas, Artefacto y Verificacion, y cita el runbook en vez
de copiar sus comandos (`cerrar-rama` no repite ningun bloque de `RITUAL.md`: «el runbook manda»).
`ingerir-sesion` sale de los informes de v7, v8 y v9; al escribirla aparecieron tres cosas que se
dicen y no se arreglan aqui:
- `SESION-DE-PREGUNTAS.md` dice que la cita «se copia de la CRUDA», pero desde la cuarentena nadie
  lee la cruda de una sesion (la guardia la bloquea de v7 en adelante): en v9 se cito de la
  FILTRADA, que funciona fuera de los bloques en cuarentena porque `evidence new` comprueba contra
  la cruda. La skill dice la filtrada.
- No hay comando del repo para la comprobacion de audio ni para el audio de respaldo: la skill
  remite a `ffmpeg silencedetect` y al procedimiento escrito en `SESION-03-EXTRACCION.md`.
- La ayuda de `corpus transcribe --video` y de `evidence new --video` sigue diciendo «v1..v5».

No las he ejecutado de punta a punta: `cerrar-rama` solo se puede probar cerrando una rama (con
orden), e `ingerir-sesion`, con una grabacion nueva. `abrir-rama` describe lo que se hizo a mano al
abrir esta.

## 4. ERRORES-RECURRENTES.md

Cinco filas nuevas en «Patrones que ya se conocen», cada una con patron, senal y que hacer, y el
caso medido con su fuente: la CI sin `data/` (`e7df30b`, `7ff9a9c`); el commit en `main` tras el
tag (regla 5; `7ff9a9c` y el run `36174003223`); el recorte por memoria de Claude Code
(`MEMORIA-SUITE.md`); el test cuyo nombre promete lo que no comprueba
(`test_la_cli_con_a47_fijada_pasa_a_pedir_a27_antes_de_leer_velas`) con su primo, la comprobacion
que no puede fallar; y la decision del consultor que se queda en la conversacion. **Esta ultima es
PREVENTIVA y lo dice**: buscado en `docs/`, PROJECT_STATE y la memoria, el repo no documenta ningun
caso medido; lo mas cerca es un informe que remite a «la conversación de la rama» (`MAYO-DEV.md` §4)
y un revisor sin el prompt original (`GUARDIAS-CLAUDE.md`). Y una seccion nueva, «Los cinco
patrones de defecto», con la entrada de Technical Debt copiada tal cual.

## 5. Next Action

Linea J: «Pendiente del consultor: umbral de cobertura tras la sesión 4 para pasar al plan
híbrido, pre-registrado antes de medir». El umbral no lo he escrito.

## Archivos creados

`docs/state/HISTORIA.md`, `docs/state/README.md`, `docs/runbooks/MIRAR-EL-MATERIAL.md`,
`docs/runbooks/AMBIGUEDADES.md`, `.claude/skills/{abrir-rama,cerrar-rama,ingerir-sesion}/SKILL.md`,
`tests/unit/test_historia.py`, `docs/encargos/trabajo-dieta-y-skills.md`, `contrato.yaml`, este
informe y sus anexos (`docs/validation/anexos/DIETA-Y-SKILLS/{dieta,construir,mudar_claude_md}.py`,
guiones de una sola ejecucion que escriben FUERA del repo).

## Archivos modificados

`PROJECT_STATE.md`, `CLAUDE.md`, `.claude/hooks/guardia.py`, `.claude/settings.json`,
`.claude/agents/revisor.md` (la tabla de ambiguedades y los cuatro sitios, que ahora estan en el
runbook), `src/botsito/cli.py` (regla 4), `docs/runbooks/{RITUAL,ERRORES-RECURRENTES,README}.md`, y
los tests `test_guardia_claude`, `test_project_state`, `test_project_state_rutas`, `test_adr`,
`test_kit`, `test_cli`, `test_tree` y `test_documentos_vivos`.

## Tests ejecutados

PENDIENTE: `make check` sellado.

## Limitaciones y riesgos

- HISTORIA crece ~20 KB por rama. No se lee al arrancar; si algun dia pesa, se decide aparte.
- Un cierre que haga crecer PROJECT_STATE por encima de 25 KB no se puede sellar en `main`: el
  ritual lo dice y manda acortar lo sustituido.
- Las tres skills no se han ejecutado de punta a punta (§3).

## Que debe decidir el usuario

1. Si «Next Action vigente» es lo no HECHO (§1.2): B, C, D y G fuera.
2. Si la lista mecanica de pendientes del bloque viejo (A2… y 2, 6, 7… 37) sigue viva o se poda.
3. El umbral de cobertura de la linea J.

## Estado

PENDIENTE.
