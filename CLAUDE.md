# Reglas de la casa

Lo que toda sesion tiene que saber antes de tocar nada. Cada regla de aqui esta comprobada contra el
repositorio (la primera version, el 2026-09-17 en `trabajo/reglas-de-la-casa`); si alguna deja de
ser cierta, se corrige aqui en el mismo commit que la rompe. Cada regla dice primero QUE SE HACE y
despues la guarda; lo que ya hace cumplir un test, un hook o el contrato va en una linea que nombra
esa guardia, y lo que solo se usa en algunas tareas vive en `docs/runbooks/` con su puntero
(revision del 2026-10-01, `trabajo/dieta-y-skills`).

## Por donde se empieza

1. `PROJECT_STATE.md`: el presente, y manda sobre cualquier otro documento. La historia vive en
   `docs/state/HISTORIA.md`: se lee solo si la tarea la necesita.
2. `docs/plan/features/<Current Feature>.md`, si hay funcionalidad abierta.
3. `docs/HANDOFF.md` (contexto humano de la ultima sesion; si contradice a `PROJECT_STATE.md`, manda
   `PROJECT_STATE.md`).
4. `make check > make-check.log 2>&1`.

Si `Current Feature` esta en WAITING_FOR_USER_VALIDATION, se pregunta antes de avanzar.

Las tareas repetidas tienen skill en `.claude/skills/`: `abrir-rama`, `cerrar-rama` (solo con orden
de cierre de Aleks) e `ingerir-sesion`.

## Se trabaja en una rama: main no se toca

Se trabaja en una rama (`feature/F##-nombre` o `trabajo/<nombre>`), que se abre con la skill
`abrir-rama`. **Los commits en las ramas `trabajo/*` los hace Claude Code. El cierre en `main`
-merge, tag, `PROJECT_STATE`, push atomico, verificacion de la CI y borrado de la rama- lo ejecuta
Claude Code SOLO ante una ORDEN DE CIERRE EXPLICITA de Aleks, dada tras la revision del consultor;
una tarea autonoma o nocturna NUNCA cierra**: deja la rama con sus commits sellados y espera la
orden (regla del 2026-09-26; skill `cerrar-rama`, que sigue `docs/runbooks/RITUAL.md` con todas sus
puertas).
- Guardias: el hook `pre-commit` rechaza un commit directo en `main` salvo con `BOTSITO_ALLOW_MAIN=1`,
  que solo usa el ritual; el push a `main` pide confirmacion (regla `ask` de `.claude/settings.json`).

**El orden de un commit es siempre el mismo: estadiar lo que se va a commitear →
`make check > make-check.log 2>&1` → leer el log (exit 0, ningun `failed` y la linea `SELLO`) →
commit.** Si quedan cambios sin estadiar o ficheros sin seguir, `make check` lo avisa y no sella.
**Ningún commit sin el sello de `make check`, y NUNCA `--no-verify`**, ni en `git commit` ni en
`git merge`: si el hook rechaza, se vuelve a `make check`.
- Guardias: `make check` en verde sella el hash del arbol ESTADIADO y los hooks `pre-commit` y
  `pre-merge-commit` rechazan cualquier otro (`trabajo/blindaje`, `RITUAL.md` correccion 7); la
  guardia de Claude Code y `.claude/settings.json` bloquean `--no-verify` y `core.hooksPath`.
- El trabajo entra por commits y merges, que pasan por los hooks: `cherry-pick` y `rebase` no pasan
  por `pre-commit`: no se usan para meter trabajo (la guardia los bloquea).

**Ensayos aislados, y nada escribe mientras corre `make check`** (regla del 2026-09-28,
`docs/validation/BLINDAR-MAKE-CHECK.md`):
1. Un script que escribe archivos se ensaya en un clon desechable creado con `git worktree add` en
   un directorio temporal, no con copias sueltas de ficheros.
2. La raiz de un instalador, o de cualquier script que escriba, sale de un argumento o de una
   variable de entorno. Una sustitucion con `sed` no sirve: sobre una ruta de Windows, con sus
   barras invertidas, `sed` no casa y no avisa, y el script escribe en el repositorio real.
3. Mientras corre `make check`, lo que haya que escribir en el repositorio espera. Guardia: `make
   check` toma una huella del arbol al empezar y otra al sellar; si difieren sale en rojo, nombra
   los ficheros y no sella.

## Regimenes de cambio

- `knowledge/evidence/` → INMUTABLE tras commit. Una correccion es un item nuevo que supersede, con
  `botsito evidence new --supersede <id>` y el MISMO tema que el item que corrige (lo exige la
  guardia). La via de propuesta (`evidence propose --check` + `accept`) no admite `supersede`: por
  ahi no se puede corregir (deuda anotada el 2026-09-17). Guardia: el hook `pre-commit`.
- `knowledge/feedback/` → SOLO ANADIR: un registro nuevo, nunca se edita uno. Guardia: el hook.
- `knowledge/corpus/libros.yaml` → SOLO ANADIR (ADR-0039). El sha fija los bytes, asi que el formato
  y el huso con que se lee un libro no pueden cambiar nunca: una entrada commiteada no se edita ni se
  borra. Y ningun libro se lee sin su entrada. Guardia: `knowledge validate` contra el historial (el
  hook no, porque solo sabe de inmutabilidad fichero a fichero).
- `knowledge/spec/`, `knowledge/cases/` → versionados; cada cambio de valor cita su fuente (el
  trailer `Fuente:`, abajo).
- `docs/validation/` → un informe CERRADO en `main` se corrige con un RECUADRO DE CORRECCION al
  principio (o junto al pasaje que corrige), con fecha y rama, y el cuerpo queda intacto (practica de
  `F14A-INGESTA.md` y ADR-0037 §7, escrita como regla el 2026-09-22). Nada lo comprueba
  mecanicamente todavia (Technical Debt).
- `PROJECT_STATE.md` → solo el PRESENTE: lo que deja de ser verdad se SUSTITUYE, sin
  «Lo anterior:», porque lo de antes ya esta archivado (regla del 2026-10-01, `trabajo/dieta-y-skills`;
  el cierre lo edita asi, `RITUAL.md`). Guardia: `tests/unit/test_project_state.py` (sus secciones y
  un tope de 25.000 bytes).
- `docs/state/HISTORIA.md` → SOLO SE AMPLIA: al abrir cada rama se anade al final, como `# Archivo N`,
  el `PROJECT_STATE.md` de `main` entero (`docs/state/README.md`). Guardia:
  `tests/unit/test_historia.py` contra el historial.
- `data/manifests/`, `knowledge/corpus/transcripciones/`, `knowledge/corpus/fotogramas/` → INMUTABLES
  tras commit. Guardia: el hook.
- `src/botsito/domain/` → sin IO, sin reloj, sin MetaTrader. Guardia: import-linter.

## El trailer `Fuente:`

Todo commit que toque `knowledge/spec/` o `knowledge/cases/` lleva en el CUERPO del mensaje (en el
asunto no cuenta) un trailer `Fuente:` con ids que EXISTAN: `ev-*`, `fb-*` o `ADR-NNNN`. Un sha de
commit no es un id valido. Guardia: `comun/historial.py` (`DIRECTORIOS_CON_FUENTE`).

## Al anadir un sitio con `cita` propia, las TRES guardias

Un sitio nuevo que lleve `cita` amplia, EN EL MISMO COMMIT, las tres de `src/botsito/spec/modelo.py`:
`comprobar_contra`, `comprobar_literales` y `comprobar_citas_revocadas`. Ha nacido corta cuatro
veces, y nada lo comprueba.

## Las cifras van en el registro de parametros

Si un valor puede cambiar, es un parametro del registro (ADR-0002: una sola puerta, tipos no
intercambiables, lectura estricta), y la forma ejecutable nombra el parametro sin llevar el numero
dentro. Guardia: `tests/contract/test_no_business_literals.py`.

## Que se puede mirar y que no: son TRES cosas distintas, no una

`corpus/` y casi todo `data/` estan fuera de git (`.gitignore`: `/corpus/`, `/data/*` salvo
`/data/manifests/`), asi que viven en la maquina.

**1. SE LEEN, y conviene leerlos: `data/fotogramas/**` y `data/transcripciones/**`.** No son holdout,
y se regeneran desde el corpus. Son la fuente primaria de lo que el trader hace EN PANTALLA, y la via
es `botsito corpus frames show --video <v> --t h:mm:ss [--n N]`. **Un fotograma se abre por un
instante LOCALIZADO antes** -por la transcripcion, por un item que ya lo cite, o por una marca de
tiempo registrada-, nunca por muestreo (ADR-0038): no se puede saber que hay en un PNG antes de
abrirlo, y una clase entera de imagenes -las capturas de Analytics- esta prohibida. Si uno trae un
AGREGADO, se declara el MISMO DIA con sus cifras listadas y ninguna se usa (ADR-0021 §2). **Antes de
abrir fotogramas, leer transcripciones o comparar el video con las velas: `docs/runbooks/MIRAR-EL-MATERIAL.md`**
(como se abre un fotograma, donde esta el texto de cada transcripcion, y que el reloj de los graficos
de FX Replay es UTC+2 FIJO: antes de comparar dos fuentes se fija el huso de las dos, medido).

**2. LAS VELAS DE `data/` SE LEEN para recalcular ventanas, y eso NO es abrir un holdout** (ADR-0021
§1). `kit build` y `kit check` se ejecutan con `data/` presente y declaran en su salida, por RECUENTO y
no por fechas, los dias reservados cuyas velas leen (ADR-0033). Ninguna etiqueta y ningun precio.

**3. PROHIBIDO sin pasar por la puerta de ADR-0033** (`botsito.cases.holdout`, que exige `PREREGISTRO.md`
relleno y autorizacion commiteada por particion, atada por `preregistro_blob`). **El criterio no es
el TIPO DE FICHERO: es la GRANULARIDAD DEL DATO** (ADR-0037):
- `knowledge/cases/holdout/**` (particiones 1, 2 y 3);
- el **detalle por operacion** de los xlsx del corpus **DE LOS DIAS QUE ESTEN EN UNA PARTICION
  RESERVADA** -hora, direccion, entrada, stop, objetivo-. El dia manda, no el fichero: las filas de
  un dia `dev` del MISMO libro se leen sin puerta (ADR-0021 §1; ADR-0025 §4 para mayo);
- **todo AGREGADO sobre un rango que incluya un dia reservado** -totales del mes, un calendario de
  PnL, un recuento por columna del fichero entero, la lista de fechas presentes en el libro- y esto
  **no lo abre ninguna autorizacion**, porque un agregado no se trocea por dia: mirarlo ES leer una
  cifra que contiene los reservados. Vale aunque viva en el mismo fichero que las filas que si se
  pueden leer;
- las **capturas de Analytics** de FX Replay, EN BLOQUE y de cualquier mes: no se pueden trocear
  por dia.

**Material de DESARROLLO, que no es holdout y se abre sin puerta:** enero, abril y agosto de 2026
(`HOLDOUT-EXPOSICIONES.md`). Que no tienen ni un dia en ninguna particion se COMPRUEBA antes de abrir
con `casos_reservados(repo)`, no se supone, y se declara igual el mismo dia.

**Lo minimo para fijar el universo SI se lee, y no es abrir.** De un backtest del trader se puede
leer QUE DIAS CUBRE EL MATERIAL -la columna de fechas- porque eso no es leer una etiqueta ni medir
una cifra del bot (ADR-0021 §1), y sin universo no hay sorteo. Vale para CUALQUIER backtest, no solo el de septiembre: febrero
o marzo vienen detras. Con tres ataduras:

- **QUIEN:** el consultor. No una sesion, no un agente.
- **CUANDO:** una sola vez, ANTES del sorteo. Nunca despues.
- **QUE:** solo la columna de fechas. Ni resultados, ni PnL, ni una fila de operaciones.

**Marzo de 2026 esta RECIBIDO y SIN ABRIR** (`docs/validation/REGISTRO-MARZO.md`, decision del
consultor del 2026-09-30): entra por el camino de fidelidad como mes reservado, y no se sortea ni se
ingiere hasta que A-42 este RESUELTA con el trader en la sesion 4 (PARADA B0 de
`docs/runbooks/ENTRADA-MARZO.md`); lo unico que se lee antes es la columna de fechas, por el
consultor (arriba), y sus 7 imagenes no se abren. Guardia: la de Claude Code bloquea su carpeta
`Backtest marzo 2026`.

**Toda exposicion se declara en `docs/validation/HOLDOUT-EXPOSICIONES.md` el mismo dia, siempre**
(ADR-0021 §4).

**Una prohibicion escrita aqui que no salga de un ADR se revisa contra el ADR antes de aplicarla**:
tres veces este fichero fue mas estricto que ADR-0021 sin que ningun ADR lo dijera y bloqueo un paso
que el proceso exige. Si se aparta del ADR, o se corrige aqui o se cambia el ADR, pero no se deja el
desacuerdo por escrito (historia de las tres, en `docs/runbooks/MIRAR-EL-MATERIAL.md`).
- Guardia: la de Claude Code bloquea leer el contenido de lo del punto 3 (abajo). La barrera sigue
  siendo el codigo: `casos_reservados` y la puerta de ADR-0033.

## Ambiguedades

**Antes de abrir, editar o cerrar una ambiguedad de `knowledge/spec/ambiguedades.yaml`, se lee
`docs/runbooks/AMBIGUEDADES.md`**: abrirla toca dos sitios, cerrarla cinco (y hay dos formas,
ADR-0022); una RESUELTA se REABRE con un registro `REOPEN` y una DECIDIDA solo con otro ADR; una
`medicion` puede citar una fuente documental en vez de evidencia; y tocar su texto obliga a
`botsito spec docs --escribir` en el MISMO commit, igual que
`parametros.yaml`, `strategy_spec.yaml` y `glossary.yaml`. Guardias: `tests/unit/test_kit.py` (la
tabla de `PROJECT_STATE.md` son exactamente las abiertas),
`tests/contract/test_spec_docs_generados.py`, `tests/unit/test_hoja_preguntas.py` (la hoja de
preguntas no lleva una cerrada) y `tests/unit/test_reabrir_y_fuente_documental.py` (REOPEN y
fuentes documentales).

## Como se trabaja

- Antes de escribir codigo, revision de diseno; se contesta MIDIENDO, no razonando.
- **Y lo mismo vale para los briefs: toda afirmacion del consultor sobre como se comporta un
  mecanismo se mide antes de escribirla en ningun documento; si la medida la contradice, gana la
  medida y se dice con su nombre.** Es la regla de arriba aplicada a los briefs, y cubre el sub-caso
  del patron 5 que mas ha costado; el patron 5 entero sigue sin deteccion mecanica
  (`docs/runbooks/ERRORES-RECURRENTES.md`, «Los cinco patrones de defecto»).
- Un informe por rama en `docs/validation/`, con su estado al final.
- Nada afirma mas de lo que su cita sostiene.
- **Al abrir una rama** (skill `abrir-rama`): el prompt que la origina se copia tal cual en
  `docs/encargos/<rama con - en lugar de />.md`, se escribe su `contrato.yaml`
  (`docs/runbooks/CONTRATO-DE-RAMA.md`) y se archiva en `docs/state/HISTORIA.md` el
  `PROJECT_STATE.md` de `main`. Guardia: `make check` comprueba el contrato.
- Antes de declarar una rama lista para revisión: guarda el encargo en docs/encargos/, pasa el revisor y pega su informe al final del informe de la rama.
  El revisor es el subagente `revisor` (`.claude/agents/revisor.md`); lo que encuentra el y lo que
  encuentra despues el consultor se apunta en `docs/runbooks/ERRORES-RECURRENTES.md`, que tambien
  recoge los errores que ya se conocen, con su senal y que hacer.

## Trampas medidas

- **Los regex se escriben con Write, nunca dentro de un heredoc con delimitador sin comillas.** En Git
  Bash, `cat > f <<EOF` convierte `\b` en BACKSPACE (0x08) antes de que Python lo vea; con `<<'EOF'`
  se conserva, pero lo seguro es Write, y lo mismo para Python con comillas y sangrado complicado:
  script a la carpeta de trabajo y ejecutarlo. Guardia: la de Claude Code bloquea el heredoc sin
  comillas con `\`.
- **Un texto que contenga literalmente la opcion `--crudo` o `crudo=True` (un encargo, un informe,
  un mensaje de commit) se escribe con Write o Edit, nunca con un heredoc ni con `-m`**: la guardia
  bloquea cualquier comando de Bash o PowerShell que los lleve. El mensaje de commit va a un fichero
  escrito con Write, y `git commit -F <fichero>`. Guardia: la de Claude Code
  (`.claude/hooks/guardia.py`, `exigir_sin_crudo`).
- **`make check` con la salida a un FICHERO, nunca a `/dev/null`:** `lint-imports` falla al escribir
  ahi y `make` sale con 2 aunque todo este verde. Guardia: la de Claude Code bloquea `make check` sin
  fichero de salida.
- El `## Estado` de un ADR empieza por `ACTIVE` o `SUPERSEDED`, sin punto: se lee con `split()[0]`.
  Guardia: `tests/unit/test_adr.py`.
- **Si una ejecucion larga en segundo plano muere con «system running low on memory», no es un fallo
  de la suite**: es el recorte de procesos en segundo plano de Claude Code. No se relanza sin
  permiso; se evita arrancando Claude Code con `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1`
  (`docs/runbooks/ERRORES-RECURRENTES.md`). El pico de cada `make check` sale en la ultima linea del
  log, `PICO DE MEMORIA`.

## Las guardias de Claude Code (`.claude/`)

Un hook `PreToolUse` (`.claude/hooks/guardia.py`, desde el 2026-10-01,
`docs/validation/GUARDIAS-CLAUDE.md`) mira cada Read, Grep, Glob, Bash y PowerShell. **Bloquea leer
el CONTENIDO del material protegido** del punto 3 -el holdout, los libros de meses con dias
reservados o sin sortear, las imagenes del material adicional, las hojas de las sesiones, las crudas
de las sesiones en cuarentena (v7 en adelante) y lo que nombre un caso reservado- y deja listarlo,
medirlo y hashearlo; y bloquea las operaciones prohibidas que su cabecera enumera (`--no-verify`,
`push --force`, borrar tags o una rama remota que no sea `trabajo/`, `feature/` o `fix/`, ...). Lo
que cuenta para la sesion:
- **La CLI ensena el corpus filtrado.** `kb find`, `kb at`, `corpus transcript show`,
  `corpus frames show` y `evidence propose` ocultan por defecto las sesiones en cuarentena, los
  tramos no citables y el material reservado o sin sortear, y dicen cuantos segmentos ocultaron
  (`src/botsito/corpus/cuarentena.py`, la UNICA fuente). La opcion que lo ensena todo es solo de
  Aleks, en su terminal, y su equivalente en Python solo lo usan las FUNCIONES de `AUTORIZADOS`
  (`tests/unit/test_cuarentena.py`, negar por defecto: nunca un fichero entero; cada una con su
  motivo: la verificacion de citas, `corpus glossary apply`, `corpus transcript check`, la evidencia
  de kb que copia un tramo no citable y dos funciones de `scripts/transcribir_sesion.py`) y los
  tests. La EVIDENCIA tiene su propio criterio, porque es un extracto revisado y se lee con Read:
  `kb` solo oculta el item cuya cita cae en un tramo no citable o cuyo texto lo copia, o el que
  trae un dia de `casos_ocultos` (decision del consultor del 2026-10-01).
  Un fichero del repositorio que copia texto oculto no se lee: las propuestas de
  `knowledge/_proposals/` con segmentos ocultos y las salidas de medicion con lineas ocultas (lista
  calculada en `.claude/hooks/ficheros_con_ocultos.txt` por `scripts/ficheros_con_ocultos.py`).
  Guardias: la de Claude Code bloquea las dos cosas, y `tests/unit/test_cuarentena.py` falla si
  aparece otro llamador o alguien lee la cruda sin pasar por las funciones que filtran.
- **Una guardia no se rodea.** Si bloquea algo legitimo, se dice en el informe y se corrige la
  guardia en su rama; no se reescribe el comando para que no la vea.
- **Solo un guion identico al de `main` es codigo revisado.** Uno nuevo o cambiado en la rama en
  curso, aunque este commiteado, se lee como codigo sin revisar: por eso un guion que nombre una
  carpeta protegida se bloquea aunque no la abra.
- **Los tramos no citables** (`knowledge/corpus/tramos_no_citables.yaml`) de un video que no esta en
  cuarentena tampoco se leen: v6 queda fuera de la cuarentena solo con sus tramos bloqueados
  (0:41:00-0:50:11 y 1:53:30-1:57:31), en sus ficheros, en las propuestas que copian sus segmentos y
  en la CLI; su cruda se lee por trozos (Read con `offset` y `limit`) que no los toquen. Decisiones
  del consultor del 2026-10-01.
- Es defensa en profundidad: la barrera sigue siendo el codigo (`casos_reservados`, la compuerta del
  arnes).
