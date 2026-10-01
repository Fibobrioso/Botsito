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

**Tras el revisor (B1 y B2 de su informe, al final).** Medido por el hook completo, no por la
funcion suelta: `git push origin +:main` ya lo bloqueaba la regla del push forzado, en Bash y en
PowerShell; `git push --mirror origin` lo bloqueaba en Bash (como forzado) pero **en PowerShell
pasaba**, y no es de esta rama: PowerShell nunca miro `--mirror`. Arreglado en
`decidir_borrado_remoto`, que ahora tambien bloquea `--mirror` y lee `+:<ref>` como un borrado, con
`test_la_decision_de_borrado_sola_tambien_cierra_el_forzado_y_el_espejo` y los dos casos en las
listas de Bash y de PowerShell.

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

**La CI de Linux** (regla de `RITUAL.md`, porque toca un hook): `63efc02` empujado como
`fix/dieta-y-skills` (`git push origin trabajo/dieta-y-skills:refs/heads/fix/dieta-y-skills`), run
`36911338342`: **1 failed, 1716 passed, 8 skipped**, y el unico fallo es el esperado que el runbook
nombra, `test_state_check_ok_on_real_repo` («PROJECT_STATE declara la rama
'trabajo/dieta-y-skills'; la rama actual es 'fix/dieta-y-skills'»). Lint y tipos, verdes. Como
`make check` se para en `test`, en la CI no corren `state`, `config` ni `knowledge`; en local, si.
La rama remota `fix/dieta-y-skills` se queda hasta el cierre, y la borra la skill `cerrar-rama`
(ya lo permite esta guardia).

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
- **Tope**: `test_project_state_cabe_en_el_tope`, 25.000 bytes. Con la primera version habia 4,4 KB de margen (tras la revision del consultor, 1.915 bytes: §6.4), para que
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

Medido el 2026-10-01 con `claude -p` (Claude Code 2.1.287, el mismo modelo y la misma memoria de
usuario) en dos clones desechables (`git worktree add --detach`), uno en `df6aa2c` y otro en
`63efc02`, con la misma orden: «lee PROJECT_STATE.md ENTERO con la herramienta Read (por trozos si
no cabe) y responde Current Branch, el numero de secciones `## ` y el numero de lineas». `CLAUDE.md`
lo carga Claude Code solo en los dos. Las dos respuestas fueron correctas (`main` · 30 · 904, y
`trabajo/dieta-y-skills` · 11 · 172).

| | Antes (`df6aa2c`) | Despues (`63efc02`) |
|---|---|---|
| Duracion (`duration_ms`) | 75,9 s | 9,7 s |
| Turnos | 22 (lectura a trozos) | 2 (una lectura) |
| Contexto en el ultimo turno (tokens de entrada) | 246.835 | 49.178 |
| Tokens de entrada leidos de cache, sumados | 2.126.446 | 51.954 |
| Coste que informa la CLI | 2,42 USD | 0,31 USD |

Una sola corrida por lado: es un orden de magnitud, no una media. El contexto que una sesion arrastra
el resto del dia baja un 80 % (de ~247 mil a ~49 mil tokens), y en esos 49 mil esta todo lo demas
que Claude Code carga (herramientas, memoria, `CLAUDE.md`).

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

## 6. La revision del consultor (2026-10-01), punto por punto

La orden esta copiada tal cual en `docs/encargos/trabajo-dieta-y-skills.md`, «Segunda orden».

### 6.1 `.claude/settings.json` frente a `main`

El diff completo (`git diff main -- .claude/settings.json`), tras esta revision:

```diff
diff --git a/.claude/settings.json b/.claude/settings.json
index b04a0ca..41ff446 100644
--- a/.claude/settings.json
+++ b/.claude/settings.json
@@ -20,8 +20,26 @@
       "Bash(git push * -f *)",
       "Bash(git tag -d *)",
       "Bash(git tag --delete *)",
-      "Bash(git push * --delete *)",
+      "Bash(git push * --delete main*)",
+      "Bash(git push * --delete stable/*)",
+      "Bash(git push * --delete refs/tags/*)",
+      "Bash(git push * --delete refs/heads/main*)",
+      "Bash(git push * --delete * main*)",
+      "Bash(git push * --delete * stable/*)",
+      "Bash(git push * --delete * refs/tags/*)",
+      "Bash(git push * --delete * refs/heads/main*)",
+      "Bash(git push * -d main*)",
+      "Bash(git push * -d stable/*)",
+      "Bash(git push * -d refs/tags/*)",
+      "Bash(git push * -d refs/heads/main*)",
+      "Bash(git push * -d * main*)",
+      "Bash(git push * -d * stable/*)",
+      "Bash(git push * -d * refs/tags/*)",
+      "Bash(git push * -d * refs/heads/main*)",
+      "Bash(git push * :main*)",
+      "Bash(git push * :stable/*)",
       "Bash(git push * :refs/tags/*)",
+      "Bash(git push * :refs/heads/main*)",
       "Bash(rm -rf data*)",
       "Bash(rm -rf ./data*)",
       "Bash(rm -rf corpus*)",
```

**Se habia perdido algo al partir la regla, y se recupera.** La regla vieja `Bash(git push * --delete *)`
denegaba cualquier `--delete`, y con eso tambien los borrados MIXTOS -una rama de trabajo delante y
`main` o un tag detras: `--delete fix/x main`, `--delete fix/x stable/…`, `--delete fix/x
refs/tags/x`- y `--delete refs/heads/main`. Las seis reglas de la primera version solo casaban con
el nombre prohibido JUSTO despues de `--delete` o de `:`, asi que esos cuatro casos los paraba solo
el hook. Ahora hay una forma `* <nombre>` para cada uno, que exige un ESPACIO delante del nombre
prohibido: `--delete * main*` deniega `--delete fix/x main` y no `--delete fix/main-nueva`. Y
lo mismo con `-d`, que la regla vieja tampoco cubria.

Que sigue denegado en la capa de permisos, comprobado con `_casa_regla` en
`test_los_ajustes_registran_la_guardia_y_las_denegaciones`:
- **borrar tags**: `git tag -d` y `git tag --delete` (sin cambios); en remoto, `--delete stable/*`,
  `--delete refs/tags/*`, `-d` con los mismos, `:stable/*` y `:refs/tags/*`, solos o detras de
  una rama de trabajo;
- **borrar `main`**: `--delete main`, `--delete refs/heads/main`, `-d main`, `:main`,
  `:refs/heads/main`, solos o mixtos;
- **`push --force`**: `--force*`, `-f` (sin cambios);
- **`--no-verify`**: en `commit`, `merge` y `push` (sin cambios).

Y NO se deniega `--delete fix/x`, `:fix/x`, `-d fix/dieta-y-skills`, `--delete trabajo/x
feature/F35-orden-stop-pivote` ni `--delete fix/main-nueva` (el mismo test), ni ninguna linea del
ritual (`test_ninguna_denegacion_toca_el_ritual`, que ya lleva el push a `fix/<rama>` y su borrado).
Lo que la capa de permisos no ve y el hook si: un tag que no se llame `stable/*` ni vaya con
`refs/tags/`, y el `+` de un refspec forzado; por eso la decision fina sigue siendo del hook.

### 6.2 CLAUDE.md: lo que se mudo, y las reglas que tienen que quedarse

Mudado TAL CUAL (la tabla de §2 con sus lineas):
- a `docs/runbooks/MIRAR-EL-MATERIAL.md`: «Estan infrautilizados…» (los 25.372 PNG y el recuento de
  fotogramas citados); los dos recuadros «Por que cambio esta regla»; «COMO SE ABRE UN FOTOGRAMA:
  POR INSTANTE LOCALIZADO, NUNCA POR MUESTREO» con su procedimiento; «EL RELOJ DE LOS GRAFICOS DE FX
  REPLAY ES UTC+2 FIJO» y «Y LA REGLA QUE SALE DE AHI» (fijar el huso de las dos fuentes); y la
  seccion entera «Donde esta el texto de las transcripciones»;
- a `docs/runbooks/AMBIGUEDADES.md`: las secciones enteras «Abrir una ambiguedad toca dos sitios;
  cerrarla, cuatro» y «Cerrar una ambiguedad toca cuatro sitios, y solo dos los vigila una guardia».

Las reglas que la orden nombra, en el `CLAUDE.md` de la rama:

| Regla | Donde esta en CLAUDE.md |
|---|---|
| Holdout | «Que se puede mirar y que no», punto 3: `knowledge/cases/holdout/**` y la puerta de ADR-0033 |
| Meses con dias reservados o sin sortear | punto 3 (el detalle de los dias reservados y los agregados) y «Las guardias de Claude Code»: «los libros de meses con dias reservados o sin sortear, las imagenes del material adicional…». **Esa lista se habia acortado en la primera version: devuelta tal cual** |
| Marzo sin abrir | **parrafo nuevo** «Marzo de 2026 esta RECIBIDO y SIN ABRIR», con `REGISTRO-MARZO.md`, la PARADA B0 y la guardia. En el `CLAUDE.md` de `main` no estaba (solo «febrero o marzo vienen detras», que tambien se habia quitado y vuelve) |
| Tramos no citables | «Las guardias de Claude Code»: los de v6, con sus dos tramos, en ficheros, propuestas y CLI (vuelve la redaccion de `main`) |
| Transcripciones en cuarentena | «Las guardias de Claude Code»: «las crudas de las sesiones en cuarentena (v7 en adelante)» |
| `--no-verify` | «Se trabaja en una rama: main no se toca»: «Ningún commit sin el sello de `make check`, y NUNCA `--no-verify`», con su guardia |
| Cierre solo por orden del usuario | la misma seccion: «SOLO ante una ORDEN DE CIERRE EXPLICITA de Aleks», y «Por donde se empieza»: `cerrar-rama` (solo con orden de cierre de Aleks) |
| Trailer `Fuente:` | «El trailer `Fuente:`», entero |

Ninguna de ellas se mudo entera; lo que faltaba era recorte de la primera version y ya esta
devuelto.

### 6.3 Los hallazgos del revisor

**El «importa», literal (B1):** «La guardia permite borrar `main` con el refspec forzado `+:main`:
`git push origin +:main`. `decidir_borrado_remoto` solo trata como borrado el refspec que empieza por
`:`. `.claude/settings.json` tampoco lo cubre, porque sus `deny` son `:main*` y `--delete main*`. No
es una regresión, porque el código anterior también exigía `startswith(":")`. Pero el encargo pide
«sigue bloqueando main» y «cualquier comando que no pueda decidir con seguridad», y los tests no
tienen un caso `+:`.» **Como quedo:** medido por el hook completo, `+:main` ya lo bloqueaba la regla
del push forzado en Bash y en PowerShell; la funcion sola no. Arreglado en `e5e257f`:
`decidir_borrado_remoto` quita el `+` y lo lee como borrado, con un test de la funcion sola y el caso
en las listas de Bash y de PowerShell.

Los tres menores, una linea cada uno:
- **A1** (las skills no se ejecutaron de punta a punta): sigue igual y declarado (§3); solo se
  prueban con un cierre o una grabacion de verdad.
- **B2** (`--mirror` pasa por `decidir_borrado_remoto`): arreglado en `e5e257f`; en PowerShell
  pasaba DE VERDAD, no solo en la funcion.
- **B3** (un tag llamado como una rama de trabajo): sigue declarado como riesgo residual (§0); los
  tags de este repo son `stable/*`.

### 6.4 La lista vieja de Next Action, punto por punto

Regla de la orden: con evidencia de estar hecho, solo a HISTORIA; sin ella, se queda en
`PROJECT_STATE.md`, en «Pendientes heredados (sin verificar)», una linea cada uno con su arranque
literal (los primeros ~110 caracteres, cortados en un espacio: un corte a mitad de una ruta la rompia
y lo cazo `test_las_rutas_de_project_state_existen`). Un punto hecho A MEDIAS cuenta como sin
evidencia y se queda, con lo que si esta hecho dicho en la tabla. Lo genera
`docs/validation/anexos/DIETA-Y-SKILLS/pendientes_heredados.py` desde el Archivo 1; la evidencia la
puse yo, punto por punto.

| Punto | Texto literal (arranque) | Evidencia de que esta hecho | Destino |
|---|---|---|---|
| A2 | A2. **Aleks ejecuta MedirDemoFTMO en la demo de FTMO** (docs/runbooks/DEMO-FTMO.md), tres ejecuciones: antes… | sin evidencia | PROJECT_STATE, «Pendientes heredados (sin verificar)» |
| A3 | A3. **Ramas de codigo, en este orden** (orden del consultor del 2026-09-29): | encabezado: de sus ramas, a), c) y 0) estan hechas; b), d) y e), no del todo | PROJECT_STATE, «Pendientes heredados (sin verificar)» |
| a | a) **sesgo**: RN-003 y RN-033 (siempre hay sesgo; la doble ruptura la decide el color) y RN-002 (cierre un… | ADR-0060; commit `6698426` (F32), tag `stable/F36-nocturno-01oct` | solo HISTORIA |
| b | b) **sesiones independientes y varios escenarios por sesion**: `liquidez_tomada` caduca al abrir la sesion… | a medias: `liquidez_tomada` caduca al abrir la sesion en `bf1dc0b` (F33, A-46); la caja por operacion no: NOCTURNO-01OCT.md §5 la deja «detrás de F35», y nada la cierra | PROJECT_STATE, «Pendientes heredados (sin verificar)» |
| c | c) **gestion**: `stop_fraccion_redondeo` hacia fuera (hoy ROUND_DOWN hacia la entrada), RN-004 en la vela de… | redondeo hacia fuera: ADR-0061, `2cca34d`; RN-004 en M1: ADR-0062, `2763ceb` (los dos en `stable/F36-nocturno-01oct`); break even al tocar: ADR-0065, `stable/F36h-be-al-tick` | solo HISTORIA |
| d | d) **vida de la orden stop** (RN-006, rama 3 de ADR-0056) y RN-007 (la vela casi plana; falta el umbral); | a medias: RN-006 en ADR-0064 (`stable/F36d-orden-stop-pivote`); RN-007 espera el umbral (Next Action H) | PROJECT_STATE, «Pendientes heredados (sin verificar)» |
| 0 | 0) **REQUISITO PREVIO de cualquier corrida sobre meses de invierno, incluida fidelidad-dev: separar el reloj… | ADR-0063; commit `fad0305` (F36), tag `stable/F36-nocturno-01oct` | solo HISTORIA |
| e | e) **calendario de cierres de mercado** para la regla de gap trading de FTMO (Technical Debt, 2026-09-29). | sin evidencia | PROJECT_STATE, «Pendientes heredados (sin verificar)» |
| A4 | A4. **La memoria de la suite: EN REVISION en `trabajo/memoria-suite`** (docs/validation/MEMORIA-SUITE.md). El… | a medias: la memoria de la suite en `stable/F31c-memoria-suite` y `stable/F31d-ci-linux-memoria`; la propuesta sobre ADR-0057 §5, sin aplicar (ningun commit la toca) | PROJECT_STATE, «Pendientes heredados (sin verificar)» |
| A5 | A5. **Para la sesion 4 con el trader**: confirmar A-42 (dijo «creo»); las siete ganadoras anotadas de mas de… | sin evidencia | PROJECT_STATE, «Pendientes heredados (sin verificar)» |
| 2 | 2. MARZO INTERRUMPE LO QUE HAYA EN VUELO CUANDO LLEGUE. El trader confirmo el 2026-09-21 que no habia visto… | a medias: el libro esta en el corpus (`stable/F36f-registro-marzo`), pero marzo no esta en `knowledge/cases/visto/` ni hay CONFIRM del trader | PROJECT_STATE, «Pendientes heredados (sin verificar)» |
| 6 | 6. FEBRERO NO SE TOCA Y NO SE DESCARGA. Unico mes ciego limpio confirmado por el trader. Bajar sus velas es… | sin evidencia | PROJECT_STATE, «Pendientes heredados (sin verificar)» |
| 7 | 7. JUNIO, LA GUARDIA Y LOS ONCE DIAS. La guardia de `stable/F14-cobertura` saca junio del universo de un… | sin evidencia | PROJECT_STATE, «Pendientes heredados (sin verificar)» |
| 8 | 8. EL BRIEF PARA ABRIR LOS 4 `dev` DE SEPTIEMBRE, que es lo unico que se puede abrir de ese material y no se… | sin evidencia | PROJECT_STATE, «Pendientes heredados (sin verificar)» |
| 9 | 9. LA CITA QUE YA TENEMOS CON UN PROBLEMA, y no es una deuda abstracta: RE-DESCARGAR UN MES ROMPE `kit build`… | sin evidencia | PROJECT_STATE, «Pendientes heredados (sin verificar)» |
| 10 | 10. EL DUEÑO, EN PARALELO: no comprar todavia -confirmar en el panel de FTMO que el tipo Swing existe para… | sin evidencia | PROJECT_STATE, «Pendientes heredados (sin verificar)» |
| 12 | 12. **MARZO, AL LLEGAR, ENTRA POR SU PROPIA RAMA**: declaracion en `knowledge/corpus/libros.yaml` con formato… | sin evidencia | PROJECT_STATE, «Pendientes heredados (sin verificar)» |
| 15 | 15. **EN ESPERA: A-18: pregunta de reserva enviada al trader el 2026-09-23** (lo declara el consultor; es la… | sin evidencia | PROJECT_STATE, «Pendientes heredados (sin verificar)» |
| 22 | 22. **SIGUIENTE: la sesion 02 con el trader, con A-35 y A-44 como PRIORIDAD** (desde ADR-0049 A-43 va en la… | a medias: la sesion 02 se grabo e ingirio (`stable/F19-sesion-02-videos`), pero no hay `knowledge/feedback/*-sesion-02/` y A-35 y A-44 siguen ABIERTAS | PROJECT_STATE, «Pendientes heredados (sin verificar)» |
| 23 | 23. **MARZO: RECIBIDO el 2026-09-30 y SIN ABRIR** (`stable/F36f-registro-marzo`,… | sin evidencia | PROJECT_STATE, «Pendientes heredados (sin verificar)» |
| 25 | 25. **RN-004, bloqueada SOLO por A-35** (K-04, docs/validation/SESION-02-DECISIONES.md §1): A-21 es la zona… | sin evidencia | PROJECT_STATE, «Pendientes heredados (sin verificar)» |
| 27 | 27. **PENDIENTE PARA ALEKS, CON FTMO:** donde esta la linea entre operar con noticias en Swing y el gap… | sin evidencia | PROJECT_STATE, «Pendientes heredados (sin verificar)» |
| 30 | 30. **DESPUES DE LA SESION 02: RN-004 TRAS A-35, medida con el arnes y mirada con el visor** (`botsito motor… | sin evidencia | PROJECT_STATE, «Pendientes heredados (sin verificar)» |
| 34 | 34. **PENDIENTES QUE DEJA `trabajo/ticks-llenado`, con dueno** (ADR-0051 §7): (a) la VENTANA DE TICKS DE… | sin evidencia | PROJECT_STATE, «Pendientes heredados (sin verificar)» |
| 35 | 35. **DESPUES DE LA SESION 02: RN-020 TRAS A-44.** Con A-44 respondida -que perdida hace que el trader deje… | sin evidencia | PROJECT_STATE, «Pendientes heredados (sin verificar)» |
| 36 | 36. **EN MARCHA (el script existe desde `stable/F26-demo-ftmo-script`; lo ejecuta Aleks, punto A2): MEDIR EN… | sin evidencia | PROJECT_STATE, «Pendientes heredados (sin verificar)» |
| 37 | 37. **PENDIENTE: LOS RECHAZOS POR VOLUMEN MAXIMO, EN LA RAMA DE STOP Y LOTE (A-18)** (2026-09-28, orden de… | sin evidencia | PROJECT_STATE, «Pendientes heredados (sin verificar)» |

Resultado: 3 puntos (a, c, 0) solo en HISTORIA; 24 en «Pendientes heredados (sin verificar)», como
subseccion `###` de Next Action (el test de secciones admite solo las once `##`). La primera linea
del bloque viejo daba por HECHA tambien la rama b), y la evidencia dice que a medias: gana la
evidencia. `PROJECT_STATE.md` pasa de 20.622 a 23.085 bytes: sigue por debajo de 25.000, pero el
margen para el commit de estado de un cierre baja a 1.915 bytes (§1.2 decia 4,4 KB).

### 6.5 Donde quedo la regla de mi memoria

Lo que apunte en la memoria de la sesion (`project-state-historia-y-skills.md`) son cuatro reglas, y
cada una esta ahora en `CLAUDE.md` o en `RITUAL.md`:
- PROJECT_STATE solo presente, se sustituye sin «Lo anterior:», tope de 25 KB: `CLAUDE.md`,
  «Regimenes de cambio», linea de `PROJECT_STATE.md` (**nueva en esta revision**), y `RITUAL.md`, la
  lista de lo que edita el cierre;
- HISTORIA solo se amplia y recibe el Archivo N al abrir cada rama: `CLAUDE.md`, «Regimenes de
  cambio» (ampliada) y «Como se trabaja», «Al abrir una rama» (**nueva**); el como, en
  `docs/state/README.md` y la skill `abrir-rama`;
- la tabla de ambiguedades lleva solo las abiertas: `CLAUDE.md`, «Ambiguedades», y
  `docs/runbooks/AMBIGUEDADES.md`;
- `/cerrar-rama` es la orden de cierre: `CLAUDE.md`, «Por donde se empieza» y «Se trabaja en una
  rama», y `RITUAL.md`, cabecera.

### 6.6 La CI de Linux

| Commit | Run | Resultado |
|---|---|---|
| `63efc02` (la rama) | `36911338342` | 1 failed, 1716 passed, 8 skipped: solo el esperado, `test_state_check_ok_on_real_repo` por `fix/` frente a `trabajo/` |
| `e5e257f` (tras el revisor) | `36913763335` | 1 failed, 1721 passed, 8 skipped: el mismo, y solo ese |
| `e5e257f` | `36913763427` | `cancelled` a los 2 s: el mismo push disparo dos runs y la concurrencia de la CI cancelo uno; no es un resultado |

El run del commit de esta revision se apunta en la respuesta a la orden, porque escribirlo aqui
exigiria otro commit y otro run.

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

- `make check` antes del primer commit (`63efc02`): verde, 1725 passed, `Contracts: 4 kept, 0
  broken`, `state check` OK, `SELLO` sobre el arbol `51c706ec…`, `PICO DE MEMORIA` 284 MiB.
- CI de Linux de `63efc02` como `fix/dieta-y-skills`: run `36911338342`, el unico fallo esperado
  (§0).
- Tras el revisor: `tests/unit/test_guardia_claude.py` en verde, y `make check` otra vez antes del
  segundo commit (su resultado, en el mensaje de ese commit y en «Estado»).
- 1120 funciones de test (antes de la rama, 1110): 4 de la guardia de borrado + 1 tras el revisor, 3
  de HISTORIA, 1 de la regla 4 y 1 del tope; las del indice de ADR, la tabla de ambiguedades y las
  rutas se reescriben con el mismo numero.

## Limitaciones y riesgos

- HISTORIA crece ~20 KB por rama. No se lee al arrancar; si algun dia pesa, se decide aparte.
- Un cierre que haga crecer PROJECT_STATE por encima de 25 KB no se puede sellar en `main`: el
  ritual lo dice y manda acortar lo sustituido.
- Las tres skills no se han ejecutado de punta a punta (§3).

## Que debe decidir el usuario

1. Si «Next Action vigente» es lo no HECHO (§1.2): B, C, D y G fuera.
2. Los 24 «Pendientes heredados (sin verificar)» (§6.4): cuales se cierran o se podan, uno a uno; la regla de la revision los deja todos mientras no haya evidencia.
3. El umbral de cobertura de la linea J.

## Estado

**Rama lista para revisión, NO cerrada.** WAITING_FOR_USER_VALIDATION: el cierre en `main` solo con
orden de cierre explicita de Aleks (skill `/cerrar-rama trabajo/dieta-y-skills <tag>`), que borra
tambien `fix/dieta-y-skills` en `origin`.

## Informe del revisor

Pegado del subagente `revisor`, sobre `63efc02` y antes de arreglar B1 y B2 (§0). Los hallazgos y
las tablas van tal cual; la lista de comandos ejecutados y dos frases de relleno («Ya está relleno,
aunque me dijiste…», «este texto es el que se pega»), resumidas o quitadas.

> ## Informe del revisor · trabajo/dieta-y-skills · 2026-10-01
>
> Base main df6aa2c, HEAD 63efc02, un solo commit. Contrato: `CONTRATO: 31 ficheros dentro del contrato de trabajo/dieta-y-skills (riesgo medio, artefacto docs/validation/DIETA-Y-SKILLS.md, 4 comprobaciones para el revisor)`.
>
> ### Eje (a) · Reglas de la casa
> Resumen: 0 bloquea, 0 importa, 1 menor.
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | A1 | menor | Las tres skills no se ejecutaron de punta a punta. El informe lo declara en §3 y en «Limitaciones», así que no es ocultación. Queda anotado porque `cerrar-rama` y `ingerir-sesion` son lo único de la rama que no tiene ninguna prueba. | `docs/validation/DIETA-Y-SKILLS.md` §3, último párrafo |
>
> Comprobado sin hallazgos:
> - **Contrato y pytest.** `uv run pytest tests/unit/test_guardia_claude.py test_project_state.py test_historia.py test_kit.py test_adr.py tests/contract/test_documentos_vivos.py -q`: todo en verde, 100 %.
> - **Más pytest.** `test_cli.py`, `test_tree.py`, `test_project_state_rutas.py`, `test_revisor.py` y `test_push_atomico.py`: verdes. `test_revisor` sigue pasando con el cambio de `revisor.md`.
> - **state check.** `uv run botsito state check` da OK.
> - **HISTORIA.md.** Con `git show df6aa2c:PROJECT_STATE.md` leído en Python, el original mide 418.819 bytes y HISTORIA 419.885. El original está contenido byte a byte en HISTORIA (`o in h` = True). La cabecera añade 1.066 bytes, como dice el informe.
> - **Literalidad de PROJECT_STATE.md.** Comparé cada línea no vacía con las del original. Las 95 líneas que no están en el original son solo marcos: la cabecera, los punteros, la línea J, el texto de las secciones «Reglas vivas» y «Known Ambiguities», y las líneas «— ninguna desde el Archivo 1». La tabla de ambigüedades sale del YAML y la deuda es el arranque literal. El resto es copia.
> - **Tamaños.** PROJECT_STATE.md 20.622 bytes (tope 25.000). CLAUDE.md 14.983 contra 20.554 en main, cifras que coinciden con el informe.
> - **Rutas protegidas.** `git diff --stat` no toca `knowledge/`, `config/`, `data/manifests/`, `src/botsito/{engine,domain,spec}/` ni `docs/adr/`. No hay ADR nuevos, ni trailers `Fuente:` que exigir, ni tocados de `ambiguedades.yaml`, holdout o libros.
> - **Informes cerrados.** La rama no cambia ningún `docs/validation/*.md` ya existente: solo añade `DIETA-Y-SKILLS.md` y sus anexos.
> - **Decisiones de «vigente» declaradas.** Next Action = lo no HECHO; ambigüedades = las abiertas; 15 deudas descartadas por su propio texto, con números; qué se queda en «Reglas vivas»; y qué se descarta, con motivo. Todo está en informe §1.2 y «Que debe decidir el usuario» 1 y 2.
> - **CLAUDE.md sin pérdidas.** Las reglas movidas tienen puntero, o la guardia que las cubre, o se conservan: vecindario del fotograma y «vía de localización es la transcripción» (`MIRAR-EL-MATERIAL.md` líneas 41-42); vmmem y el recorte por memoria (`ERRORES-RECURRENTES.md`); las puertas del ritual (remiten a `RITUAL.md`); las ambigüedades (`AMBIGUEDADES.md`); los tramos no citables de v6 (se conservan los dos tramos).
> - **Skills.** Las tres tienen Entradas, Límites, Herramientas, Artefacto y Verificación. Se leyó `cerrar-rama` entera y las cabeceras y cuerpos de `abrir-rama` e `ingerir-sesion`; `ingerir-sesion` solo hasta Límites, así que no se comprobó que traiga Herramientas, Artefacto y Verificación. `cerrar-rama` lleva `disable-model-invocation: true`, cita `RITUAL.md` paso a paso sin copiar sus bloques de comandos e incluye el borrado de `fix/<rama>`.
> - **ERRORES-RECURRENTES.md.** Las cinco filas pedidas, cada una con patrón, señal y qué hacer. La de conversaciones sin traspaso dice que es preventiva y que el repo no documenta ningún caso medido.
> - **RITUAL.md.** El diff añade el borrado de `fix/<rama>` con su puerta y la regla de sustituir con tope de 25 KB.
> - **Contrato.** `rutas_permitidas` cubre los 31 ficheros modificados.
>
> ### Eje (b) · Encargo
> Resumen: 0 bloquea, 1 importa, 2 menor. Requisitos: 15 hechos, 1 parcial, 0 no hechos. El parcial es el requisito 0.3, y por eso es lo que cuenta en el hallazgo B1.
>
> | # | Requisito | Estado | Evidencia |
> |---|---|---|---|
> | 0.1 | Permitir `push --delete <rama>` y `push :<rama>` solo para `trabajo/`, `feature/`, `fix/` | Hecho | Llamé a `decidir_borrado_remoto`: `--delete fix/x`, `:fix/x` y `-d fix/x` pasan; `--delete trabajo/main` pasa. Código en `.claude/hooks/guardia.py`, `RAMA_BORRABLE`. |
> | 0.2 | Sigue bloqueando main, tags (`stable/*`), `refs/tags/`, comodines y lo indecidible | Hecho | Bloquean: `--delete main`, `--delete stable/F36j-guardia-linux`, `:refs/tags/x`, `'fix/*'`, `--delete refs/heads/main`, `:heads/main`, `fix/x/../../main`, `fix/{a,b}`, `--prune`. Con `None` (referencia construida) también bloquea. |
> | 0.3 | Un borrado de varias referencias con una prohibida se bloquea | Parcial | Bloquean `--delete fix/x main`, `--delete fix/x refs/tags/x` y `fix/a :main`. Falla `+:main` (ver B1). |
> | 0.4 | Tests pedidos: deja borrar `fix/x`, bloquea `main`, `stable/F36j-guardia-linux`, `refs/tags/x` y el borrado mixto | Hecho | `tests/unit/test_guardia_claude.py` líneas 557 y 575-589; el test mixto es la línea 581. |
> | 0.5 | Empujar como `fix/dieta-y-skills` y esperar la CI de Linux | Parcial, y es PENDIENTE declarado en informe §0, no se cuenta como hallazgo | — |
> | 1.1 | Historia y bloques «LO QUE DECÍA» a `docs/state/HISTORIA.md`, que solo se amplía | Hecho | HISTORIA contiene el original entero; `tests/unit/test_historia.py` verde. |
> | 1.2 | PROJECT_STATE conserva main/último tag, Next Action vigente, ambigüedades abiertas, deuda técnica y reglas vivas copiadas tal cual, y pesa menos de 25 KB | Hecho | 20.622 bytes. Secciones presentes. Líneas verificadas contra el original (ver eje (a)). |
> | 1.3 | Ajustar `state check`, ritual y tests que leían lo movido | Hecho | `cli.py` (`_read_sections`, regla 4), `RITUAL.md`, y los tests de project_state, rutas, kit y adr ajustados. Todos verdes. |
> | 1.4 | Comprobar que ningún texto se pierde | Hecho | `o in h` = True, y el test lo repite en cada `make check`. |
> | 1.5 | Medir el tamaño antes y después, y el arranque | Hecho | Informe §1.1 y §1.5. No pude reproducir las medidas de arranque. |
> | 2.1 | CLAUDE.md: quitar lo que ya hace cumplir un test, hook o contrato y dejar un puntero | Hecho | Líneas «Guardia: …» en CLAUDE.md. |
> | 2.2 | Lo ocasional pasa a `docs/runbooks/` con puntero | Hecho | `MIRAR-EL-MATERIAL.md` y `AMBIGUEDADES.md`, con punteros en CLAUDE.md. |
> | 2.3 | Prohibiciones primero en positivo, luego la guarda | Hecho | «El orden de un commit es siempre el mismo…» antes del NUNCA `--no-verify`; el trabajo entra por commits y merges antes de cherry-pick/rebase. |
> | 2.4 | Entregar antes/después en KB y la lista de lo movido | Hecho | Informe §2: 20.554 → 14.983 bytes y tabla de bloques movidos. |
> | 3.1 | Tres skills con entradas, límites, herramientas, artefacto y verificación | Hecho | Las tres existen con esas secciones. |
> | 3.2 | `cerrar-rama` solo se ejecuta si el usuario lo ordena | Hecho | `disable-model-invocation: true` y sección «Cuando se ejecuta, y cuando NO». |
> | 3.3 | No duplican RITUAL.md, lo citan | Hecho | `cerrar-rama`: «aquí no se repite ningún comando ni ninguna puerta». |
> | 4 | Completar ERRORES-RECURRENTES con los cinco patrones | Hecho | Diff: cinco filas nuevas más la sección «Los cinco patrones de defecto». |
> | 5 | Línea J de Next Action, sin escribir el umbral | Hecho | PROJECT_STATE.md Next Action J, textual con el encargo. |
> | 6 | Ritual con make check sellado, informe del revisor al terminar | Parcial, pendiente declarado (§Tests y Estado) | — |
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | B1 | importa | La guardia permite borrar `main` con el refspec forzado `+:main`: `git push origin +:main`. `decidir_borrado_remoto` solo trata como borrado el refspec que empieza por `:`. `.claude/settings.json` tampoco lo cubre, porque sus `deny` son `:main*` y `--delete main*`. No es una regresión, porque el código anterior también exigía `startswith(":")`. Pero el encargo pide «sigue bloqueando main» y «cualquier comando que no pueda decidir con seguridad», y los tests no tienen un caso `+:`. | Llamada directa a `g.decidir_borrado_remoto(["origin","+:main"])` devolvió `PERMITE`. Un test del estilo `"git push origin +:main"` no existe. No pude reproducirlo pasando por el hook completo: mi intento de invocar `guardia.py` fue bloqueado por la propia guardia («una guardia no se rodea»), así que no lo rodeé. |
> | B2 | menor | `git push --mirror origin` pasa por `decidir_borrado_remoto` sin bloqueo, aunque `--mirror` borra en el remoto las referencias que no existen en local, incluidas ramas o tags. No es regresión y el repo no lo usa; si se quiere cerrar la familia, `--mirror` entra junto a `--prune`. | `decidir_borrado_remoto(["--mirror","origin"])` devolvió `PERMITE`; el código solo trata `--prune`. |
> | B3 | menor | Los borrados de rama no cubren un tag llamado igual que una rama. El informe lo declara en §0, «Lo que queda, dicho». Anotado como riesgo residual, no como defecto. | Informe §0 |
>
> Lo que la rama hace y el encargo no pide, y está justificado en el informe (§0 «Lo que hice de más», §1.2, §3): cambios en `.claude/settings.json`; bloqueo de `--prune`; control en PowerShell; cambio en `.claude/agents/revisor.md`; los tres anexos `.py`; el test endurecido de ambigüedades; el movimiento del índice de ADR a su README. No hay hechos fuera de encargo sin declarar. Lo que el encargo dice que no se toca (motor, spec, knowledge, cifras): el diff no toca nada de eso.
>
> ### Lo que no pude comprobar
> - **`make check`.** Escribe, así que no lo ejecuté. Acepto sin verificar el SELLO sobre el árbol 51c706ec…, 1725 passed y PICO 284 MiB que me diste.
> - **CI de Linux de `fix/dieta-y-skills`.** Pendiente.
> - **Medida de arranque** (75,9 s contra 9,7 s). No la repetí; exige `claude -p` en clones desechables, con escritura.
> - **Tres citas del informe contra su fuente.** Comprobé la estructura de las filas nuevas de ERRORES-RECURRENTES, pero no abrí `ACTIVAR-SESION-03.md` ni `MEMORIA-SUITE.md` para verificar que cada cita las sostiene.
> - **Los `Fuente:` y el commit.** No había nada en `knowledge/spec` ni `knowledge/cases` que lo exigiera.
> - **Si las 39 deudas restantes son las abiertas correctas.** La dieta usa un criterio mecánico; eso lo declara el informe y lo decide el consultor.
>
> ### Comandos ejecutados
> `git log/diff/status`, `cat` del encargo y del contrato; `uv run python scripts/contrato_rama.py`; `uv run pytest` sobre los tests citados; `uv run botsito state check`; `git show df6aa2c:PROJECT_STATE.md | wc -c` y `wc -c`; scripts Python de solo lectura que comparan HISTORIA y PROJECT_STATE con el original y llaman a `decidir_borrado_remoto`; `cat`/`sed`/`grep` de CLAUDE.md, el informe, las skills, `MIRAR-EL-MATERIAL.md` y `docs/state/README.md`. Dos intentos que la guardia o el hook de solo lectura bloquearon, sin rodearlos.

Respuesta de la sesion a los hallazgos: **B1 y B2, arreglados** (§0; B1 ya lo paraba el push forzado en el hook completo, B2 pasaba de verdad en PowerShell). **A1 y B3, declarados**, sin cambio. Las citas que el revisor no abrio (`ACTIVAR-SESION-03.md`, `MEMORIA-SUITE.md`) las comprobe yo contra su fuente al escribir `ERRORES-RECURRENTES.md` (recuadro de correccion de ACTIVAR-SESION-03 y §1 y §5 de MEMORIA-SUITE).

## Informe del revisor, segunda pasada (la revision del consultor)

Pegado del subagente `revisor`, sobre los 7 ficheros estadiados encima de `e5e257f` y antes de
`make check`. Los hallazgos y las tablas, tal cual; la lista de comandos, resumida.

> ## Informe del revisor · trabajo/dieta-y-skills (cambios estadiados sobre e5e257f) · 2026-10-01
>
> Alcance: los 7 ficheros estadiados (`git diff --cached e5e257f`) frente a la «Segunda orden» (puntos 1 a 6) y a `docs/validation/DIETA-Y-SKILLS.md` §6. `make check` y el «pega su informe» no se cuentan.
>
> ### Eje (a) · Reglas de la casa
> Resumen: 0 bloquea, 0 importa, 2 menor.
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | A1 | menor | §6.6 anota el run `36913763427` como `cancelled` a los 2 s, y `gh` lo marca con X en la vista resumen. La conclusión real es `cancelled`, así que el informe acierta. Un lector que mire solo el resumen lo verá como fallo. | `gh run view 36913763427 --json conclusion` → `"conclusion":"cancelled"`; anotación «Canceling since a higher priority waiting request for ci-refs/heads/fix/dieta-y-skills exists» |
> | A2 | menor | §6.2 dice que «febrero o marzo vienen detras» «vuelve». Es cierto, pero CLAUDE.md:146 queda con el corte de línea en mitad de la frase («…no solo el de septiembre: febrero / o marzo vienen detrás»). Es forma, no contenido. | `CLAUDE.md:145-146` |
>
> Comprobado sin hallazgos: los tests de permisos (`-k "ajustes or ritual"`) en verde; el diff de §6.1 coincide con `git diff --cached main -- .claude/settings.json` (19 líneas añadidas y 1 quitada); PROJECT_STATE.md pesa 23.085 bytes; `6698426`, `2cca34d`, `2763ceb`, `fad0305` y `bf1dc0b` existen, son ancestros de `stable/F36-nocturno-01oct` y sus asuntos casan con la tabla; los tags y los ADR 0060 a 0065 citados existen; holdout, meses «reservados o sin sortear», cuarentena, tramos no citables de v6, `--no-verify`, ORDEN DE CIERRE y trailer `Fuente:` están en CLAUDE.md, y el párrafo de marzo es nuevo y sus referencias existen; `RITUAL.md:179-181` y CLAUDE.md:76-78 llevan la regla «sin Lo anterior» y el tope; nada en `knowledge/`, ADR ni spec.
>
> ### Eje (b) · Encargo (Segunda orden, puntos 1 a 6)
> Resumen: 0 bloquea, 0 importa, 1 menor. Requisitos: 6 hechos, 0 parciales, 0 no hechos.
>
> | # | Requisito | Estado | Evidencia |
> |---|---|---|---|
> | 1a | Pegar el diff completo de settings.json frente a main | Hecho | §6.1 pega el diff, y coincide con el real. |
> | 1b | La capa de permisos sigue denegando borrar tags (`stable/*`, `refs/tags/`), borrar main, `push --force` y `--no-verify`, también en mixtos y con `-d` | Hecho | `settings.json` añade 14 reglas: `--delete`, `-d` y `:`, solos y con `* <nombre>` delante, más `refs/heads/main*`. El test cubre `--delete fix/x main`, `-d fix/x stable/F01`, `:fix/x :main`, `--force fix/x` y `push --no-verify`. |
> | 1c | No chocar con borrar `trabajo/`, `feature/`, `fix/` | Hecho | El test comprueba que NO se deniegan `--delete fix/x`, `:fix/x`, `-d fix/dieta-y-skills`, `--delete trabajo/x feature/F35-…` y `--delete fix/main-nueva`. |
> | 2 | Lista de secciones movidas, y reglas nombradas que se quedan en CLAUDE.md con puntero | Hecho | §6.2 lista lo movido; las 8 reglas aparecen en CLAUDE.md, con punteros en CLAUDE.md:116, 165 y 172. |
> | 3 | Citar literal el hallazgo «importa» (B1) y dar los tres menores en una línea | Hecho | La cita de §6.3 coincide palabra por palabra con la celda «Hallazgo» de B1, salvo que omite la celda de evidencia. |
> | 4 | Tabla de cuatro columnas; con evidencia solo a HISTORIA; sin evidencia a «Pendientes heredados (sin verificar)»; sin borrar por criterio propio; PROJECT_STATE < 25 KB | Hecho | 27 filas: a, c y 0 a HISTORIA, 24 a «Pendientes». Los 24 son prefijos literales de su línea en HISTORIA «Archivo 1» (script de solo lectura: `True 1` en los 24). b), d), A4 y 2 «a medias», comprobados; 22 (sin `*-sesion-02` en `knowledge/feedback/`) y 12 (sin marzo en `libros.yaml`), comprobados. |
> | 5 | La regla de memoria, en RITUAL.md o CLAUDE.md | Hecho | CLAUDE.md:76-78, «Al abrir una rama», Ambigüedades y `RITUAL.md:179-181`. |
> | 6 | Runs de la CI de Linux | Hecho | `36911338342`: failure, «1 failed, 1716 passed, 8 skipped», solo `test_state_check_ok_on_real_repo`. `36913763335`: failure, «1 failed, 1721 passed, 8 skipped», el mismo test. `36913763427`: cancelado por concurrencia. |
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | B1 | menor | §6.6 fecha el run `36911338342` en `63efc02`. Es plausible, y la hora cuadra con el push. No contrasté el sha del run, solo la vista resumen de `gh`. | `gh run view 36911338342` (el sha del commit no sale en la vista corta) |
>
> ### Lo que no pude comprobar
> - **`+:main` en la capa de permisos.** No se deniega ahí. Lo para el hook, y §6.1 lo dice. No lo probé con el hook completo: la guardia me bloquea invocar `guardia.py`.
> - **Que los 21 puntos «sin evidencia» no estén hechos.** Solo comprobé a fondo 12, 22 y 2.
> - **El sha de cada run de CI.** Solo vi la vista de `gh`.
> - **`make check` y el sello.** Escriben, y no los ejecuté.

Respuesta de la sesion: **A1**, nada que cambiar (el informe ya dice `cancelled`). **A2**, forma: se
deja. **B1**, comprobado despues con `gh run view <run> --json headSha,conclusion`: `36911338342` →
`63efc02 failure`; `36913763335` → `e5e257f failure`; `36913763427` → `e5e257f cancelled`.

## Cierre: hallazgo A1, la primera ejecucion real de `cerrar-rama` (2026-10-01)

Orden de cierre de Aleks tras revisar `09a1bd1` (run `36920348532`). A1 del revisor decia que
`cerrar-rama` no se habia ejecutado nunca; este es su primer uso. Escrito ANTES del merge, porque
despues, en `main`, solo puede cambiar `PROJECT_STATE.md`: lo que pase desde el merge hasta el
borrado de las ramas se dice en la respuesta a la orden y lo archiva la rama siguiente.

Donde la skill se quedo corta o dijo algo distinto de `RITUAL.md`, hasta el merge:

| # | Paso | Que paso | Estado |
|---|---|---|---|
| A1.1 | Invocacion | El `/cerrar-rama` venia dentro de un texto pegado: no cargo la skill, y con `disable-model-invocation` la sesion no puede cargarla. Se siguio leyendo su `SKILL.md`. | CERRADO: la skill lo dice ahora («Cuando se ejecuta») |
| A1.2 | Registro en HISTORIA | La orden pedia el registro del merge en `docs/state/HISTORIA.md`; ni la skill ni `RITUAL.md` decian donde, y en `main` tras el tag lo impide la regla 5. El consultor decidio: en la rama, en el commit que saca el contrato, con el sha como `stable/<tag>^{commit}`. | CERRADO: escrito en `RITUAL.md` («Antes del merge: el contrato sale de la rama») y en el paso 3 de la skill |
| A1.3 | Numero de commits | El cierre anade a la rama un commit (contrato y registro), como dice `RITUAL.md`; la skill lo contaba bien. | Sin diferencia |
| A1.4 | Edicion de `PROJECT_STATE.md` | La orden acotaba las secciones a «main, ultimo tag y Next Action»; la skill no decia que la orden manda ni que `Current Branch` tiene que pasar a `main`. Preguntado: se tocan tambien `Current Branch` y `Current Feature`, y no se anaden Completed Features ni Change Log. | CERRADO: paso 5 de la skill |
| A1.5 | Del merge al borrado de las ramas | Aun no ejecutado al escribir esto. | PENDIENTE: en la respuesta a la orden |
