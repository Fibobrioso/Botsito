# FUNCTIONALITY VALIDATION REPORT

**Funcionalidad:** F10 · elicitation-kit
**Rama:** `feature/F10-elicitation-kit`
**Objetivo:** generar, de forma determinista, el paquete de la sesion 1 con el trader: el
cuestionario (una pregunta por parametro `UNKNOWN`, ambiguedad abierta y contradiccion, con
casos concretos de la evidencia), 40 ventanas de replay sobre dias que el trader NO ha visto,
con seed y particiones commiteadas antes de la sesion, y el calculo de kappa entre rondas de
etiquetado leidas de los registros F09. Primera funcionalidad de la fase 2. Metodo supervisado:
brief -> revision de diseno por agente (3 bloqueantes, 9 importantes y 6 menores, todos
aplicados al brief) -> construccion -> auditoria de cierre con dos agentes -> este informe.

## Que se construyo
- **Ambiguedades legibles por maquina** (`knowledge/spec/ambiguedades.yaml`, ADR-0011):
  A-1..A-12 con pregunta, evidencia (ids existentes), parametros del registro, contradiccion
  asociada, estado y `bloqueante`; validadas en `knowledge validate`; test anti-deriva con la
  tabla de PROJECT_STATE; el feedback valida ahora el objetivo `ambiguedad` contra el fichero.
- **Registro pre-poblado**: 23 parametros de estrategia nuevos en `UNKNOWN` sin valor (24 con
  `anclaje_h4`), para que `RESOLVE_UNKNOWN` tenga objetivo. El enlace parametro -> temas de
  evidencia, ambiguedad y opciones cerradas vive en `knowledge/cases/kit/mapa_parametros.yaml`.
- **Datos de negocio del kit como datos** (`knowledge/cases/kit/config.yaml`): simbolo,
  dia operativo `00:00-15:00` en `huso_operativa`, sesiones H4 `07-11` y `11-15`, los dos
  anclajes candidatos (Madrid 00:00 y Nueva York 17:00; solo el segundo reproduce las sesiones
  que el trader declara), etiquetas `compra | venta | no_trade`, cupos 16/8/8/8. `src/` no
  contiene ninguna cifra de negocio (`test_no_business_literals`).
- **Paquete `botsito.cases`**: `ambiguedades.py`, `cuestionario.py` (fusion de origenes: A-9 =
  `anclaje_h4`; A-10 = `stop_fraccion_caja` + `stop_colchon_spread` + contradiccion
  `stop.nivel`; hasta 3 casos `ev-*` por pregunta, con `valor` primero y `fr-*` de referencia),
  `ventanas.py` (universo de dias laborables no vistos cuya ventana completa cae dentro del
  dataset con >= 850 velas; `sha256` de las velas recomputable con `cargar_ventana`; limites
  H4 por anclaje con `limites_entre`), `particiones.py` (orden por `sha256(seed:caso)`,
  independiente de la version de Python), `kappa.py` (gramatica `07-11: venta@08:37 e=...;
  11-15: no_trade`, Cohen exacto en fracciones, rondas desde los `LABEL_CASE` activos),
  `paquete.py` (build determinista sin sobreescribir, `check` puro byte a byte, validacion con
  guardia de ancestro).
- **CLI**: `kit build --sesion --seed`, `kit check --sesion`, `kit kappa --sesion-a --sesion-b`.
  `knowledge validate` gana la capa kit (esquema, ids, evidencia y datasets existentes, y la
  guardia: el commit que anadio `particiones.yaml` es ancestro del que anadio el primer
  `LABEL_CASE` de esa sesion).
- **Corpus y feedback**: grabaciones de sesion como `videos` sin `drive_id`; `grabacion` puede
  citar un video; `t1` no supera su duracion. `comun.historial.{commit_que_anadio, es_ancestro}`.
- **Datasets** 2026-05 y 2026-06 congelados (`data download`, con reintentos por 503 del
  proveedor): los unicos meses sin mencion en el corpus.
- **Paquete real** `knowledge/cases/kit/2026-09-15-sesion-01/` (fecha provisional; la fija el
  usuario): {PAQUETE}

## Archivos creados
`src/botsito/cases/{ambiguedades,cuestionario,ventanas,particiones,kappa,paquete}.py`,
`knowledge/spec/ambiguedades.yaml`, `knowledge/cases/kit/{README.md,config.yaml,mapa_parametros.yaml,
vistos.yaml,2026-09-15-sesion-01/*}`, `data/manifests/eurusd-m1-2026-0{5,6}-*.yaml`,
`docs/adr/0011-kit-de-elicitacion.md`, `docs/plan/features/F10-elicitation-kit.md`,
`tests/unit/test_kit.py`, `tests/contract/test_kit_particiones.py`.

## Archivos modificados
`src/botsito/cli.py` (`kit`, contexto de feedback), `src/botsito/validation/knowledge.py`,
`src/botsito/feedback/modelo.py`, `src/botsito/corpus/inventario.py`, `src/botsito/comun/historial.py`,
`knowledge/spec/parametros.yaml`, `knowledge/{README,spec/README,cases/README}.md`,
`docs/adr/README.md`, `docs/plan/MASTER_PLAN.md`, `PROJECT_STATE.md`, `docs/HANDOFF.md`.

## Decisiones tomadas
Las 13 del brief. Destacan: julio y agosto estan VISTOS (v3 dibuja sobre julio; agosto tiene
dos backtests sin fecha por dia), asi que las ventanas salen de mayo y junio, y la sesion exige
antes la confirmacion escrita del trader de que no ha operado ni backtesteado esos meses; la
etiqueta es por sesion H4, no por dia; la guardia de particiones es de ancestro en git, no de
fecha; kappa se lee del feedback, no de ficheros aparte.

## Como ejecutarlo
```
uv run botsito kit build --sesion 2026-09-15-sesion-01 --seed 20260915
uv run botsito kit check --sesion 2026-09-15-sesion-01
uv run botsito kit kappa --sesion-a 2026-09-15-sesion-01 --sesion-b 2026-09-22-sesion-02
uv run botsito knowledge validate
```
Tras la sesion: `botsito feedback new --sesion ... --accion LABEL_CASE --objetivo-tipo caso
--objetivo-id caso-eurusd-2026-05-06 --valor "07-11: venta@08:37 e=1.15364; 11-15: no_trade" ...`.

## Como probarlo
`make check`. Sin `data/`: `uv run --no-sync pytest -q tests/unit/test_kit.py
tests/contract/test_kit_particiones.py` (dataset sintetico congelado en `tmp_path`, repo git
temporal para la guardia). Con `data/`: `kit check --sesion 2026-09-15-sesion-01` recompone el
paquete y compara bytes.

## Tests ejecutados
`make check` verde: {TESTS}. Nuevos: ambiguedades (esquema real 12/12, errores, contexto,
anti-deriva), particiones (determinismo con orden de entrada distinto, seed distinto, errores),
gramatica de etiqueta (6 casos invalidos), kappa (matriz clasica 20/5/10/15 -> po 0,70, pe 0,50,
kappa 0,40; acuerdo total; una categoria; unidades distintas; etiqueta fuera), paquete
(determinista, universo con dia visto y dia fuera del dataset, limites H4 de los dos anclajes
en verano, cuestionario con fusion y contradiccion, hoja solo `dev` y sin `ev-*`, escribir sin
sobreescribir, `check` puro y con config cambiada, sin datos), config y mapa estrictos, kappa
desde registros con `supersede` y CLI, `validar_paquetes` sin git, ventana en invierno,
guardia de ancestro (antes = OK; despues y mismo commit = error).

## Resultados
{RESULTADOS}

## Que deberia observar el usuario
`knowledge validate` con la linea "OK: 12 ambiguedades registradas; 1 paquetes de sesion
validos, particiones anteriores al etiquetado"; `kit check` en verde; `hoja_trader.md` con
las 21 preguntas (3 bloqueantes primero) y solo los 16 casos `dev` con las dos rejillas H4.

## Que casos funcionan
Todo el alcance del brief.

## Que casos todavia no funcionan
- El runner de casos, las fixtures OHLC copiadas y las etiquetas del sistema son F14.
- Registrar el feedback de la sesion es `feedback new` (F09) tras la sesion.

## Limitaciones
- El paquete es provisional hasta la confirmacion escrita del trader sobre mayo y junio.
- La fecha de la sesion (`2026-09-15`) es un supuesto: regenerar con otra fecha es un comando.
- Sin grabacion de la sesion, los registros seran `medio: escrito` sin `t0/t1`.

## Riesgos
Si el trader ha visto mayo o junio, `vistos.yaml` cambia y se descarga otro mes; los holdouts
pierden valor si el trader ve las ventanas antes de tiempo (la hoja solo lleva `dev`).

## Impacto sobre funcionalidades anteriores
`validar_contra_contexto` (F09) gana dos parametros opcionales; `rutas_corpus` incluye los
videos; `fuentes.yaml` admite videos de sesion sin `drive_id`; el registro pasa de 2 a 25
parametros (24 UNKNOWN de estrategia; `test_fichero_real_sin_valores_de_estrategia` sigue
verde); `knowledge validate` suma la capa kit. Ningun id existente cambia.

## Auditoria de cierre (dos agentes: codigo/tests y docs/proceso)
{AUDITORIA}

## Que debe decidir el usuario
1. Validar F10 y confirmar el cierre: merge `--no-ff` a `main` con tag `stable/F10`.
2. La FECHA real de la sesion 1: si no es 2026-09-15, regenerar (`kit build --sesion
   <fecha>-sesion-01 --seed 20260915`) y commitear ANTES de la sesion.
3. Obtener del trader, por escrito y antes de etiquetar, que no ha operado ni backtesteado mayo
   ni junio de 2026 (se registra con `feedback new --medio escrito`).
4. Siguiente funcionalidad: la sesion 1 con el trader (registros F09) y despues F11
   strategy-spec-schema.

## Que puede comprobar sin recursos especiales
`make check`; `uv run botsito knowledge validate`; `uv run botsito kit check --sesion
2026-09-15-sesion-01`; abrir `knowledge/cases/kit/2026-09-15-sesion-01/hoja_trader.md`;
`git diff stable/F08..HEAD --stat`.

## Estado
WAITING_FOR_USER_VALIDATION
