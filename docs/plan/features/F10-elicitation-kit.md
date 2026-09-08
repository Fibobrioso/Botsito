# F10 · elicitation-kit

**Rama:** `feature/F10-elicitation-kit` · **Fase:** 2 (retroalimentacion del experto) ·
**Depende de:** F09 (feedback), F15 (datasets OHLC), fase 1 cerrada (F03-F08, `stable/F08`)

## Objetivo
Generar, de forma determinista y reproducible, el paquete de la SESION 1 con el trader:
(a) el cuestionario con un caso concreto por cada parametro `UNKNOWN`, ambiguedad abierta
(A-1..A-12) y contradiccion abierta, cada pregunta enlazada a la evidencia que la origina
(`ev-*`, instante, `fr-*`); (b) un paquete de 40 ventanas de replay sobre fechas NO vistas por
el trader, con ids de caso, seed y asignacion dev / holdout-1 / holdout-2 / holdout-3 commiteada
ANTES de la sesion; (c) el calculo de kappa de Cohen entre dos rondas de etiquetado. La sesion
produce registros F09 (`RESOLVE_UNKNOWN`, `LABEL_CASE`, ...). Sin motor, sin reglas, sin spec.

## Hechos de partida
- 341 items de evidencia (`kb find | at`, F08); 12 ambiguedades A-1..A-12 con ids en
  PROJECT_STATE (tabla en Markdown, no legible por maquina); 1 contradiccion mecanica abierta
  (`stop.nivel` 0,75 / 0,8 = A-10); 89 items `tipo: UNKNOWN` y 16 `PARAMETER`; 62 items con
  `valor` en 19 raices de tema.
- Registro de parametros (`knowledge/spec/parametros.yaml`, ADR-0002/0004): 2 parametros
  (`huso_operativa` CONFIRMED por ADR-0005; `anclaje_h4` UNKNOWN, A-9). Sin valores de
  estrategia a proposito; el esquema no admite claves extra por parametro.
- Feedback (F09): acciones y objetivos tipados; `ambiguedad` (`A-N`) y `caso` (`caso-…`) se
  validan solo por formato "hasta F11/F14"; `grabacion` debe estar inventariada en el corpus;
  `t0/t1` no se comprueban contra la duracion. `PAPELES_CARPETA = (heredado_v2,
  material_adicional)`; los videos de `fuentes.yaml` exigen `drive_id`.
- Datasets congelados (F15): `eurusd-m1-2026-01-e37291d4`, `-07-aa162170`, `-08-0d42230e`
  (M1 UTC, escala 100000, dias presentes/sin datos en el manifiesto); `cargar_ventana(manifiesto,
  carpeta_datos, desde_min, hasta_min)` con hash por fichero; `data/ohlc/` esta en esta maquina
  (gitignored). Enero fue el backtest que el trader recorre en v4 (visto); v1 recapitula el 19 y
  20 de agosto (vistos); julio no aparece en los videos.
- `knowledge/cases/{dev,holdout/1,2,3,fixtures}` existen vacios con README; `ids.CASO =
  ^caso-[a-z0-9][a-z0-9-]*$`; `src/botsito/cases/` vacio. ADR-0006: el kit vive en `cases/`
  (por encima de `spec`, `retrieval`, `feedback`, `evidence`, `data`, `config`).
- MASTER_PLAN §G: sesion 1 = 3 preguntas bloqueantes elegidas en este brief (candidatas A-9,
  A-2, A-4) + ronda 1 de etiquetado + hoja de reglas. H.2: pre-poblar `parametros.yaml` con todos
  los nombres en `UNKNOWN` (commit `Fuente: ADR-0004`), ids de caso, seed y particiones con test
  de fecha; papel `sesion_feedback`; `drive_id` opcional para grabaciones locales; `t0/t1` del
  feedback contra la duracion; dibujar cada caso con los dos anclajes mientras A-9 siga abierta;
  el golden H4 del trader (captura de su grafico) se pide en la sesion 1.

## Decisiones de diseno (propuestas; se cierran tras la revision)
1. **Paquete `botsito.cases`** (ya en el contrato de capas): `ambiguedades.py` (registro
   legible por maquina), `cuestionario.py`, `ventanas.py` (seleccion de dias y ventanas),
   `particiones.py` (seed y asignacion), `kappa.py`, `paquete.py` (escritura/lectura del kit
   y `check`). Importa `retrieval` (evidencia por tema e instante), `data` (datasets),
   `config` (registro), `evidence`, `feedback`. No importa `validation` ni `cli`.
2. **Ambiguedades legibles por maquina**: `knowledge/spec/ambiguedades.yaml` con A-1..A-12
   (`id`, `titulo`, `pregunta`, `resuelve_en`, `evidencia: [ev-*]`, `bloqueante: bool`),
   copiadas de PROJECT_STATE (que pasa a remitir al fichero). F09 valida desde ahora el objetivo
   `ambiguedad` contra este fichero (deja de ser "solo formato"). Commit con `Fuente:` = los ids
   de evidencia citados + `ADR-0011`.
3. **Pre-poblado del registro** (`knowledge/spec/parametros.yaml`, todos `UNKNOWN`, categoria
   `estrategia`, sin `valor`; commit `Fuente: ADR-0004, ADR-0011`): `ventana_inicio` (hora,
   Europe/Madrid), `ventana_fin`, `cierre_forzoso_fin_ventana` (texto si/no), `sesgo_h4_regla`
   (texto), `liquidez_m15_criterio_toma` (texto: cuerpo/mecha), `stop_fraccion_caja` (fraccion),
   `stop_colchon_spread` (texto: fijo/spread), `stop_reduccion_fraccion` (fraccion),
   `stop_reduccion_umbral_vela` (porcentaje), `break_even_condicion` (texto), `objetivo_rr`
   (decimal), `cartuchos_max` (entero), `reentrada_tras_equal` (texto), `parciales` (texto),
   `riesgo_por_operacion` (porcentaje), `lotaje_base` (texto), `stop_segundo_esquema` (texto).
   El mapa parametro -> temas de evidencia y ambiguedad vive en
   `knowledge/cases/kit/mapa_parametros.yaml` (manual): es lo que permite generar el caso
   concreto de cada pregunta sin tocar el esquema estricto del registro.
4. **Cuestionario** (`cuestionario.yaml` + `cuestionario.md` generados): una pregunta `P-NN`
   por (a) parametro `UNKNOWN` de categoria `estrategia`, (b) ambiguedad de
   `ambiguedades.yaml`, (c) contradiccion abierta (`contradicciones.detectar`), sin duplicar (si
   un parametro y una ambiguedad apuntan al mismo tema, una sola pregunta con dos `origenes`).
   Cada pregunta lleva `origenes` (`{tipo, id}`), `enunciado`, `casos` = hasta 3 items de
   evidencia elegidos con `retrieval.buscar` por tema (orden temporal, los de `valor` primero) con
   `t0`, `fr-*` de referencia y la cita, y `respuesta_esperada` (tipo del parametro o lista de
   valores en conflicto). Las 3 bloqueantes: A-9 (anclaje H4: hora y huso del grafico, pide ademas
   la CAPTURA de la configuracion del grafico = golden H4 sobre F15), A-2 (2 o 3 cartuchos), A-4
   (break even al tocar o al cierre). `bloqueante: true` y van primero. Toda pregunta cita al
   menos un `ev-*` (test).
5. **Ventanas de replay**: universo = dias con datos de los datasets congelados que NO estan
   vistos: se excluye enero entero (backtest recorrido en v4) y los dias citados en la evidencia
   (`vistos.yaml` manual en el kit: 2026-08-19, 2026-08-20 por v1); quedan julio y agosto
   (~44 dias operables). Ventana de un caso = dia operativo del trader `[00:00, 15:00]`
   Europe/Madrid (contexto de mapeo desde medianoche; la ventana operativa es 07:00-15:00, que
   la sesion 1 confirma) convertido a `[desde_min, hasta_min)` UTC con `huso_operativa`; se
   anotan las fronteras de las velas H4 con los DOS anclajes candidatos (00:00 Madrid y 17:00
   Nueva York) para que la hoja las dibuje mientras A-9 siga abierta. Cada caso: `caso-eurusd-
   2026-08-05`, `dataset_id`, `desde_utc`, `hasta_utc`, `n_velas`, `sha256` de las velas de la
   ventana (recomputable con `cargar_ventana`; F14 guarda la fixture con ese hash).
6. **Seed y particiones**: `seed` explicito (entero) en el paquete; barajado con
   `random.Random(seed)` sobre la lista ordenada de dias; 40 casos = 16 `dev` + 8 `holdout-1` +
   8 `holdout-2` + 8 `holdout-3` (proporciones en el paquete). El fichero
   `knowledge/cases/kit/<sesion>/particiones.yaml` se commitea ANTES de la sesion; test de fecha:
   la fecha del commit que introdujo `particiones.yaml` (git) es anterior a la `fecha` de todo
   registro de feedback `LABEL_CASE` de esa sesion (`knowledge validate`, capa nueva). Los casos
   de holdout NO se listan en la hoja del trader de la sesion 1 (solo `dev`); la asignacion
   completa queda en el fichero (secreto de contenido, no de existencia).
7. **Kappa de Cohen** (`kappa.py`): dos rondas = dos ficheros `ronda-N.yaml` con
   `{caso, etiqueta}` sobre el MISMO conjunto de casos y un conjunto cerrado de etiquetas
   declarado en el paquete (`etiquetas: [compra, venta, no_trade]`); devuelve `po`, `pe`, `kappa`
   y la matriz de confusion; error si los conjuntos de casos difieren o una etiqueta no esta en
   el conjunto. Golden con fixtures conocidas (acuerdo total = 1, azar = 0, ejemplo clasico).
8. **CLI `botsito kit`**: `build --sesion AAAA-MM-DD-sesion-NN --seed N [--ventanas 40]`
   (escribe `knowledge/cases/kit/<sesion>/{cuestionario.yaml,cuestionario.md,ventanas.yaml,
   particiones.yaml,hoja_trader.md}`; se niega a sobreescribir un paquete existente),
   `check <sesion>` (recomputa todo desde el repo + `data/` y compara byte a byte: determinismo),
   `kappa --ronda1 --ronda2`. `knowledge validate`: capa `kit` (esquema, particiones antes del
   feedback, casos con `dataset_id` existente, ids unicos, cada pregunta con `ev-*` existente).
9. **Corpus y feedback**: `PAPELES_CARPETA` gana `sesion_feedback`; los videos de `fuentes.yaml`
   admiten `drive_id` ausente si `naturaleza` empieza por `sesion_feedback` (grabacion local);
   `feedback new` comprueba `t0/t1` contra la duracion del video de `grabacion` (manifest.yaml).
   La sesion 1 aun no tiene grabacion: nada se anade a `fuentes.yaml` hasta que exista.
10. **Sin datos en CI**: `kit build` exige `data/ohlc/` (los hashes de ventana se calculan sobre
    velas reales); los tests usan un dataset sintetico congelado en `tmp_path` (como F15) y el
    paquete real se commitea con sus hashes; `kit check` con `data/` recomputa, sin `data/`
    comprueba esquema y avisa.
11. **Determinismo**: mismo repo + mismo `data/` + mismo seed = mismos bytes (test de bytes en
    el paquete sintetico); sin hora ni rutas absolutas dentro de los ficheros; `generado_el`
    solo en la cabecera del `.md` (fuera del `check`).
12. **ADR-0011**: kit de elicitacion (ambiguedades legibles por maquina, pre-poblado UNKNOWN,
    ventanas = dias no vistos, seed y particiones commiteadas antes, kappa, papel
    `sesion_feedback`).

## Alcance cerrado (que SI)
Todo lo de las decisiones 1-12, con tests: ambiguedades (esquema, ids A-N unicos, evidencia
existente), cuestionario (una pregunta por origen, sin duplicados, 3 bloqueantes primero, cada
una con `ev-*`), ventanas (dias vistos excluidos, ventana UTC correcta en verano e invierno,
fronteras H4 de los dos anclajes, hash recomputable), particiones (seed reproducible, 16/8/8/8,
ids unicos, `check` byte a byte), kappa (fixtures), CLI (`build` no sobreescribe, `check`,
`kappa`, errores sin traceback), `knowledge validate` capa kit (particiones antes del feedback,
con un repo temporal con commits), registro pre-poblado (carga estricta, 17 UNKNOWN), feedback
sobre ambiguedad existente/inexistente, `t0/t1` contra la duracion, papel `sesion_feedback`.
Paquete real de la sesion 1 generado y commiteado: `knowledge/cases/kit/2026-09-XX-sesion-01/`
(la fecha la fija el usuario; hasta entonces `sesion-01` con fecha placeholder NO se commitea:
se genera en la validacion con la fecha real).

## Fuera de alcance (que NO)
Runner de casos, fixtures OHLC copiadas y etiquetas del sistema (F14); reglas y spec (F11);
visor de replay (F25); registrar el feedback de la sesion (se hace con `feedback new` tras la
sesion); ventanas sinteticas (hay datos reales); mas de un simbolo.

## Entradas
`knowledge/evidence/**` (via `retrieval`), `knowledge/spec/parametros.yaml`, PROJECT_STATE
(tabla de ambiguedades, se traslada), `knowledge/evidence/_contradicciones.yaml` (via
`detectar`), `data/manifests/*.yaml` + `data/ohlc/**`, `knowledge/corpus/{fuentes,manifest}.yaml`,
`config/ajustes` (carpeta de datos), `comun.historial` (fecha de commit).

## Salidas (ficheros)
`src/botsito/cases/{ambiguedades,cuestionario,ventanas,particiones,kappa,paquete}.py`,
`src/botsito/cli.py` (`kit build|check|kappa`), `src/botsito/validation/knowledge.py` (capa kit),
`src/botsito/feedback/modelo.py` (ambiguedad contra fichero, `t0/t1` contra duracion),
`src/botsito/corpus/inventario.py` (papel, `drive_id` opcional), `knowledge/spec/ambiguedades.yaml`,
`knowledge/spec/parametros.yaml` (17 UNKNOWN), `knowledge/cases/kit/{README.md,mapa_parametros.yaml,
vistos.yaml}`, `knowledge/cases/kit/<sesion>/*` (en la validacion), `docs/adr/0011-*.md`,
`tests/unit/{test_cases_*,test_kappa}.py`, `tests/contract/test_kit_particiones.py`,
`docs/validation/F10-elicitation-kit.md`, READMEs, PROJECT_STATE, HANDOFF, MASTER_PLAN.

## Tests
Ver "Alcance cerrado". Negativos: seed no entero; `--ventanas` mayor que los dias disponibles;
dataset sin datos en disco; paquete existente; ronda con caso ausente o etiqueta fuera del
conjunto; pregunta sin evidencia (error de generacion, no aviso); ambiguedad duplicada;
`particiones.yaml` commiteado DESPUES de un `LABEL_CASE` (falla `knowledge validate`).

## Criterio de aceptacion
`make check` verde; `kit build` determinista (bytes) con seed; kappa correcto sobre fixtures;
cada pregunta enlaza el item que la origina; 40 ventanas sobre dias no vistos con hash
recomputable; particiones commiteadas antes de la sesion con test de fecha; registro con todos
los nombres en UNKNOWN; hoja del trader legible (`hoja_trader.md`) que el usuario puede llevar
a la sesion.

## Riesgos
- Nombrar parametros antes de tener reglas (F11) puede dejar nombres que F11 renombre: se acepta
  porque un parametro UNKNOWN sin valor no tiene fuente que romper; renombrar es un commit con
  `Fuente:`.
- El trader puede haber visto dias de julio/agosto fuera de los videos (backtest de agosto en el
  xlsx de `material_adicional`): `vistos.yaml` es manual y el informe lista los dias excluidos;
  el usuario decide si se excluye tambien agosto (entonces solo julio: 22 dias, y el paquete
  bajaria a 20 ventanas o se anadiria otro mes con `data download`).
- Los holdouts pierden valor si el trader ve las ventanas antes de tiempo: la hoja de la sesion
  1 solo lleva `dev`.

## Revision de diseno (agente, antes de programar)
Pendiente.

## Que habilita
Sesion 1 con el trader (registros F09), F11 (reglas con parametros ya nombrados y ambiguedades
resueltas), F14 (casos con `dataset_id` + ventana + hash), F26 (holdout-1 y kappa).
