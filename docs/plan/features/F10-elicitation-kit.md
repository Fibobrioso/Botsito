# F10 · elicitation-kit

**Rama:** `feature/F10-elicitation-kit` · **Fase:** 2 (retroalimentacion del experto) ·
**Depende de:** F09 (feedback), F15 (datasets OHLC), fase 1 cerrada (F03-F08, `stable/F08`)

## Objetivo
Generar, de forma determinista y reproducible, el paquete de la SESION 1 con el trader:
(a) el cuestionario con un caso concreto por cada parametro `UNKNOWN`, ambiguedad abierta
(A-1..A-12) y contradiccion abierta, cada pregunta enlazada a la evidencia que la origina
(`ev-*`, instante, `fr-*`); (b) un paquete de 40 ventanas de replay sobre dias NO vistos por el
trader, con ids de caso, seed y asignacion dev / holdout-1 / holdout-2 / holdout-3 commiteada
ANTES de la sesion; (c) el calculo de kappa de Cohen entre dos rondas de etiquetado leidas de
los registros F09. La sesion produce registros F09 (`RESOLVE_UNKNOWN`, `LABEL_CASE`, ...). Sin
motor, sin reglas, sin spec.

## Hechos de partida
- 341 items de evidencia (`kb find | at`, F08); 12 ambiguedades A-1..A-12 con ids en
  PROJECT_STATE (tabla en Markdown, no legible por maquina); 1 contradiccion mecanica abierta
  (`stop.nivel` 0,75 / 0,8 = A-10); 62 items con `valor` en 19 raices de tema.
- Registro de parametros (`knowledge/spec/parametros.yaml`, ADR-0002/0004): `huso_operativa`
  CONFIRMED (ADR-0005) y `anclaje_h4` UNKNOWN (A-9). El esquema admite UNKNOWN sin valor y no
  admite claves extra. `Registro.obtener` rechaza leer un UNKNOWN.
- `tests/contract/test_no_business_literals.py` prohibe en `src/botsito/` los literales
  `07|11|15:00`, `17:00`, `1:3`, `Europe/Madrid`, `America/New_York`, `EURUSD`, `0.75`, `0.5`...:
  el kit no puede escribir en codigo la ventana del trader, los anclajes candidatos ni el
  simbolo.
- Feedback (F09): `ambiguedad` y `caso` solo por formato; `grabacion` se comprueba contra
  `manifest.ficheros` (los `videos` de `fuentes.yaml` NO son citables hoy) y `t0/t1` no se
  comprueban contra la duracion; `duracion_s` solo existe para `videos`. 0 registros.
- Datasets congelados (F15): enero, julio y agosto de 2026. VISTOS por el trader: enero
  (backtest recorrido en v4), julio (v3 dibuja sobre el grafico de julio: "esto es en julio",
  `tr-v3-…-270a4851/389-390`; v2 muestra las dos operaciones del 2 de julio,
  `ev-v2-003320-a736fd37`), agosto (dos backtests de agosto en v4, `ev-v4-011742-3a6b5367`,
  `ev-v4-011856-52f0f859`, xlsx de agosto sin columna de fecha: mes entero; v1 = operativa real
  desde el 20-08). `kb find` de "mayo", "junio", "marzo" y "febrero": 0 resultados.
- `dias.presentes` de los manifiestos cuenta domingos (velas desde 21:00Z) y dias truncados
  (2026-07-01 arranca en el limite del dataset): el universo de dias hay que calcularlo sobre
  la ventana real, no sobre el recuento.
- Anclajes (medido con `limites_del_dia`, 2026-07-15): `00:00 Europe/Madrid` da H4 en 00, 04,
  08, 12, 16 Madrid; `17:00 America/New_York` da 23, 03, 07, 11, 15 Madrid. Solo el segundo
  produce las sesiones "de 7 a 11 y de 11 a 3" que el trader declara (`ev-v3-000157-b26147c7`,
  `ev-v4-011425-ae028b78`, ficha `ev-v3-000138-8399c18a`). Lo que A-9 deja abierto de verdad es
  el comportamiento en las semanas en que EE. UU. y Europa no coinciden en el cambio de hora
  (servidor GMT+2/+3 frente a "UTC+2" de TradingView, `ev-v3-000136-6160fcea`).
- El trader opera y etiqueta por SESION H4 (dos por dia), no por dia: `ev-v1-000049-6a31caa6`,
  `ev-v3-000157-b26147c7`, varias operaciones por dia (`ev-v1-000948-*`, `ev-v1-002334-*`), "el
  dia termina con la primera ganadora" (`ev-v4-004936-d7004417`). F26 mide FP/FN por caso.
- `knowledge/cases/` exige trailer `Fuente:` en TODO commit (`historial.DIRECTORIOS_CON_FUENTE`),
  igual que `knowledge/spec/`. `random.Random(seed).shuffle` no esta garantizado entre versiones
  de Python. `git log --diff-filter=A` da el commit que anadio un fichero; la fecha de committer
  es falsificable y cambia con rebase.
- `knowledge/cases/{dev,holdout/1,2,3,fixtures}` vacios; `ids.CASO = ^caso-[a-z0-9][a-z0-9-]*$`;
  `src/botsito/cases/` vacio; ADR-0006: el kit vive en `cases/`.

## Decisiones de diseno (cerradas tras la revision del 2026-09-08)
1. **Paquete `botsito.cases`**: `ambiguedades.py`, `cuestionario.py`, `ventanas.py`,
   `particiones.py`, `kappa.py`, `paquete.py`. Importa `retrieval`, `data`, `config`,
   `evidence`, `feedback`, `corpus`, `comun`. No importa `validation` ni `cli`. En la CLI el
   subcomando es `kit`; en disco `knowledge/cases/kit/`; "elicitation" solo en el titulo de F10.
2. **Ambiguedades legibles por maquina**: `knowledge/spec/ambiguedades.yaml` con A-1..A-12:
   `id`, `titulo`, `pregunta`, `resuelve_en`, `evidencia: [ev-*]` (existentes), `parametros:
   [nombres del registro]`, `contradiccion: tema | null` (A-10 = `stop.nivel`), `estado:
   ABIERTA | RESUELTA`, `bloqueante: bool`. F09 valida desde ahora el objetivo `ambiguedad`
   contra este fichero (`validar_contra_contexto` recibe el conjunto de ids). Test anti-deriva:
   los ids y titulos de la tabla de PROJECT_STATE coinciden con el YAML. Commit con `Fuente:` =
   ids de evidencia citados + `ADR-0011` (el ADR entra en el mismo commit o antes).
3. **Datos de negocio del kit como DATOS**, nunca en codigo (test de literales):
   `knowledge/cases/kit/config.yaml` (manual, `Fuente:` con `ev-*`): `simbolo`, `dataset_prefijo`,
   `ventana_local: {desde: "00:00", hasta: "15:00"}` (dia operativo: contexto de mapeo desde
   medianoche; la ventana operativa 07-15 la confirma la sesion 1), `sesiones: [{nombre:
   "07-11", desde, hasta}, {nombre: "11-15", ...}]` (unidades de etiqueta; horas en
   `huso_operativa`), `anclajes_candidatos: [{etiqueta, hora, huso}]` (los dos de H.2, con
   `coincide_con_sesiones: true` en el que produce 07/11/15), `min_velas_ventana`, `etiquetas:
   [compra, venta, no_trade]`, `particiones: {dev: 16, holdout-1: 8, holdout-2: 8, holdout-3:
   8}`. El paquete copia esta cabecera y `kit check` recompone desde ella.
4. **Pre-poblado del registro** (`knowledge/spec/parametros.yaml`, categoria `estrategia`,
   todos `UNKNOWN`, sin `valor`, sin `huso` en las horas hasta que A-6/A-9 lo fijen; commit
   `Fuente: ADR-0004, ADR-0011`): `ventana_inicio`, `ventana_fin` (hora), `cierre_forzoso_fin_ventana`,
   `sesgo_h4_regla`, `liquidez_m15_criterio_toma`, `stop_fraccion_caja` (fraccion),
   `stop_colchon_spread`, `stop_reduccion_fraccion` (fraccion), `stop_reduccion_umbral_vela`
   (porcentaje), `stop_proteccion_capital` (fraccion), `stop_segundo_esquema` (fraccion),
   `stop_en_orden_pendiente`, `break_even_condicion`, `objetivo_rr` (decimal),
   `objetivo_extension` (fraccion), `cartuchos_max` (entero), `reentrada_tras_equal`,
   `reubicacion_cadencia`, `salida_sin_ruptura`, `mapeo_dos_velas`, `parciales`,
   `riesgo_por_operacion` (porcentaje), `lotaje_base` (texto). 23 nuevos + `anclaje_h4` = 24
   UNKNOWN de estrategia (test). Las opciones cerradas de los `texto` (si/no, fijo/spread,
   cuerpo/mecha, tocar/cierre) y el mapa parametro -> temas de evidencia (raices de
   `_temas.yaml`) y -> ambiguedad viven en `knowledge/cases/kit/mapa_parametros.yaml` (manual).
5. **Cuestionario** (`cuestionario.yaml` + `hoja_trader.md`): una pregunta `P-NN` por origen
   (parametro UNKNOWN de estrategia, ambiguedad ABIERTA, contradiccion abierta), fusionando en
   una sola pregunta los origenes que el mapa enlaza (A-9 = `anclaje_h4`; A-10 = `stop.nivel` =
   `stop_colchon_spread`: tres origenes, una pregunta). Cada pregunta: `origenes`, `enunciado`,
   `respuesta_esperada` (tipo y opciones cerradas), `casos` = hasta 3 items elegidos con
   `retrieval.buscar(Opciones(tema=raiz, solo="evidencia"))` (los que tienen `valor` primero,
   luego orden temporal) con `t0`, cita y `fr-*`. Bloqueantes y primero (por numero: A-2, A-4, A-9): A-9 (pide la CAPTURA de
   la configuracion del grafico y que pasa en las semanas de cambio de hora = golden H4 sobre
   F15), A-2, A-4. Toda pregunta cita al menos un `ev-*` existente (error de generacion si no).
6. **Caso, unidad de etiqueta y gramatica**: el CASO es el dia operativo (unidad de datos,
   hash y particion): `caso-<simbolo>-<AAAA-MM-DD>`, `dataset_id`, `desde_utc`/`hasta_utc` (ISO
   `Z`, de `ventana_local` + `huso_operativa`), `n_velas`, `sha256` de las velas de la ventana
   (`cargar_ventana`), y por anclaje candidato la lista de limites H4 (`limites_entre`). La
   ETIQUETA es por SESION (2 unidades por caso): `LABEL_CASE` con `valor_resultante` en la
   gramatica minima `07-11: venta@08:37 e=1.15364 sl=1.15420 tp=1.15200; 11-15: no_trade`
   (obligatorio `<sesion>: <decision>`; el resto opcional; documentada en
   `knowledge/cases/kit/README.md`; `cases.kappa.parsear_etiqueta` la valida; F14 la formaliza).
   Se pregunta en la sesion 1 si la sesion H4 es su unidad de "operar / no operar".
7. **Universo de dias NO vistos**: `knowledge/cases/kit/vistos.yaml` (manual, `Fuente:`): meses
   enteros vistos (2026-01, 2026-07, 2026-08) con su fuente, y dias sueltos. Universo = dias
   laborables de los datasets congelados NO vistos cuya ventana completa cae dentro de
   `[ficheros.primera, ficheros.ultima]` y tiene `>= min_velas_ventana` velas; los excluidos se
   listan con motivo en `ventanas.yaml`. Se descargan y congelan 2026-05 y 2026-06 (sin ninguna
   mencion en el corpus) con `data download`; el numero de ventanas se deriva del universo (40
   exige ~42 dias limpios). CONDICION de la sesion: antes de etiquetar, el trader confirma por
   escrito (registro F09 `medio: escrito`, objetivo `caso` o nota) que no ha operado ni
   backtesteado esos meses; el paquete es provisional hasta esa confirmacion.
8. **Seed y particiones**: `seed` entero; orden determinista e independiente de la version de
   Python por clave `sha256(f"{seed}:{dia}")`; 40 = 16 dev + 8 + 8 + 8 (de `config.yaml`).
   `particiones.yaml` commiteado ANTES de la sesion. Guardia (`knowledge validate`, capa kit):
   el commit que anadio `particiones.yaml` es ANCESTRO del commit que anadio el primer
   `LABEL_CASE` de esa sesion (`git merge-base --is-ancestor`), con la fecha de committer en UTC
   solo como informe; helper `comun.historial.commit_que_anadio(repo, ruta) -> (sha, fecha_utc)`.
   `hoja_trader.md` lleva solo los casos `dev`; los holdouts quedan en `particiones.yaml` (el id
   revela el dia: lo que protege es no ponerlos en la hoja y, en F14, la guarda de lectura).
9. **Kappa de Cohen** (`kappa.py`): `kit kappa --sesion-a --sesion-b` lee los `LABEL_CASE`
   ACTIVOS (respetando `supersede`) de dos sesiones de `knowledge/feedback/`, proyecta la
   etiqueta por unidad (caso, sesion) con la gramatica de la decision 6 y calcula `po`, `pe`,
   `kappa`, matriz de confusion y acuerdo por categoria, con aviso de prevalencia; error si los
   conjuntos de unidades difieren o una etiqueta no esta en `etiquetas`. `kappa.calcular(a, b,
   etiquetas)` es puro y se prueba con fixtures: acuerdo total = 1; matriz [[20,5],[10,15]] ->
   po 0,70, pe 0,50, kappa 0,40; unidad ausente = error; etiqueta fuera = error.
10. **CLI `botsito kit`**: `build --sesion AAAA-MM-DD-sesion-NN --seed N` (escribe
    `knowledge/cases/kit/<sesion>/{cuestionario.yaml,ventanas.yaml,particiones.yaml,
    hoja_trader.md}`; se niega a sobreescribir; exige `data/`), `check --sesion` (PURO:
    recompone desde el repo + `data/` y compara bytes tras normalizar CRLF; sin `data/`
    comprueba esquema y avisa), `kappa`. `knowledge validate` capa kit: esquema de cada paquete,
    ids unicos, `dataset_id` existente, cada pregunta con `ev-*` existente, particiones antes
    del primer `LABEL_CASE` de su sesion.
11. **Corpus y feedback**: las grabaciones de sesion entran como `videos` de `fuentes.yaml`
    (transcribibles con F04 y citables): `drive_id` opcional (vacio) cuando `naturaleza` empieza
    por `sesion`; `rutas_corpus` incluye `videos[].fichero`; `validar_contra_contexto` recibe
    `duraciones` (`manifest.videos[].duracion_s`) y rechaza `t1 > duracion`. Sin grabacion, los
    registros de la sesion son `medio: escrito` y no citan `t0/t1`. Nada se anade a
    `fuentes.yaml` hasta que exista la grabacion.
12. **Determinismo**: sin `generado_el` ni rutas absolutas en los ficheros; `yaml.safe_dump(
    sort_keys=True, allow_unicode=True, width=100)` y `newline="\n"`; mismo repo + `data/` +
    seed = mismos bytes (test con dataset sintetico congelado en `tmp_path`, como F15).
13. **ADR-0011**: kit de elicitacion (ambiguedades legibles por maquina, registro pre-poblado,
    datos de negocio del kit como datos, dias no vistos y meses limpios, seed por hash,
    particiones como ancestro, etiqueta por sesion y gramatica, kappa desde F09, grabaciones de
    sesion como videos).

## Alcance cerrado (que SI)
Decisiones 1-13 con tests: ambiguedades (esquema, ids unicos, evidencia existente, anti-deriva
con PROJECT_STATE), registro (24 UNKNOWN de estrategia, carga estricta, `test_fichero_real_sin_
valores_de_estrategia` sigue), config/mapa/vistos (esquema; raices en `_temas.yaml`; parametros
del mapa en el registro), cuestionario (una pregunta por origen fusionado, bloqueantes primero,
cada una con `ev-*`, sin duplicados), ventanas (dias vistos excluidos por mes y por dia; ventana
UTC correcta en verano e invierno; limites H4 por anclaje; hash recomputable; truncados y fines
de semana excluidos con motivo), particiones (orden por hash reproducible, 16/8/8/8, ids unicos),
`check` puro byte a byte, kappa (fixtures), gramatica de etiqueta (casos validos e invalidos),
kappa desde registros F09 con `supersede`, CLI (`build` no sobreescribe, `check`, `kappa`,
errores sin traceback), `knowledge validate` capa kit (ancestro: repo temporal con commits en
orden y en orden inverso), feedback (ambiguedad existente/inexistente, `t1 > duracion`, video
de sesion sin `drive_id` citable). Datasets 2026-05 y 2026-06 congelados. Paquete real
`knowledge/cases/kit/2026-09-15-sesion-01/` generado con seed y commiteado (la fecha de la
sesion la fija el usuario; regenerar es un comando).

## Fuera de alcance (que NO)
Runner de casos, fixtures OHLC copiadas y etiquetas del sistema (F14); reglas y spec (F11);
visor (F25); registrar el feedback de la sesion (se hace con `feedback new` tras la sesion);
ventanas sinteticas; mas de un simbolo; kappa ponderado.

## Entradas
`knowledge/evidence/**` (via `retrieval`), `knowledge/spec/{parametros,ambiguedades}.yaml`,
`knowledge/cases/kit/{config,mapa_parametros,vistos}.yaml`, `_contradicciones` via `detectar`,
`data/manifests/*.yaml` + `data/ohlc/**`, `knowledge/corpus/{fuentes,manifest}.yaml`,
`knowledge/feedback/**`, `config/ajustes`, `comun.historial`.

## Salidas (ficheros)
`src/botsito/cases/{__init__,ambiguedades,cuestionario,ventanas,particiones,kappa,paquete}.py`,
`src/botsito/cli.py` (`kit build|check|kappa`), `src/botsito/validation/knowledge.py` (capa kit,
duraciones, ambiguedades), `src/botsito/feedback/modelo.py`, `src/botsito/corpus/inventario.py`,
`src/botsito/comun/historial.py` (`commit_que_anadio`, `es_ancestro`),
`knowledge/spec/{ambiguedades,parametros}.yaml`, `knowledge/cases/kit/{README.md,config.yaml,
mapa_parametros.yaml,vistos.yaml,<sesion>/*}`, `data/manifests/eurusd-m1-2026-0{5,6}-*.yaml`,
`docs/adr/0011-*.md`, tests, `docs/validation/F10-elicitation-kit.md`, READMEs, PROJECT_STATE,
HANDOFF, MASTER_PLAN.

## Tests
Ver "Alcance cerrado". Negativos: seed no entero; mas ventanas que dias del universo; dataset
sin datos en disco; paquete existente; sesion con formato invalido; etiqueta fuera del conjunto;
gramatica rota (`07-11 venta`, sesion desconocida, sesion repetida); unidades distintas entre
rondas; pregunta sin evidencia; ambiguedad duplicada o con `ev-*` inexistente; `particiones.yaml`
commiteado DESPUES del `LABEL_CASE` (falla `knowledge validate`); mapa con raiz fuera de
`_temas.yaml` o parametro fuera del registro; `t1 > duracion` en feedback.

## Criterio de aceptacion
`make check` verde; `kit build` determinista (bytes) con seed; kappa correcto sobre fixtures y
desde registros F09; cada pregunta enlaza el item que la origina; 40 ventanas sobre dias no
vistos (2026-05, 2026-06) con hash recomputable; particiones commiteadas antes de la sesion con
guardia de ancestro; registro con 24 UNKNOWN; ninguna cifra de negocio en `src/`; hoja del
trader legible con las ventanas `dev` y las dos rejillas H4.

## Riesgos
- Nombres de parametros antes de F11: se acepta (UNKNOWN sin valor; renombrar es un commit con
  `Fuente:`).
- El trader puede haber operado mayo o junio sin que conste: la confirmacion escrita previa a
  la sesion es condicion del paquete; si la niega, `vistos.yaml` cambia y se regenera con otro
  mes (`data download`).
- Los holdouts pierden valor si el trader ve las ventanas: la hoja solo lleva `dev`.
- Sin grabacion de la sesion 1, `t0/t1` no se citan: se acepta (`medio: escrito`).

## Revision de diseno (agente, 2026-09-08, antes de programar)
Aceptados con cambio en el brief: B-1 julio y agosto vistos -> `vistos.yaml` por meses, descarga
de 2026-05/06, confirmacion escrita del trader (7); B-2 literales de negocio prohibidos en
`src/` -> `config.yaml` como datos (3); B-3 etiqueta por sesion H4, no por dia, con gramatica
(6, 9); I-1 el anclaje NY es el que reproduce 07/11/15 y A-9 pregunta por el cambio de hora y la
captura (Hechos, 5); I-2 orden por hash en vez de `shuffle` (8); I-3 guardia de ancestro (8);
I-4 grabaciones como `videos` con `drive_id` opcional y `rutas_corpus` ampliado, duracion desde
`manifest.videos` (11); I-5 kappa desde F09 (9); I-6 universo por ventana real y limites por
`limites_entre` (7); I-7 `Fuente:` en todo commit de `knowledge/cases/` (2, 3, 4); I-8 campos de
ambiguedades y test anti-deriva (2); I-9 `check` puro y holdouts fuera de la hoja (8, 10); M-1
seis parametros mas, `stop_segundo_esquema` fraccion, horas sin `huso`, 24 UNKNOWN (4); M-2
origenes fusionados y raices de `_temas.yaml` (5); M-3 hoja sin `ev-*` (5, 10); M-4 sin
`generado_el`, dump ordenado, CRLF (12); M-5 nombre `kit` (1); M-6 `medio: escrito` sin
`t0/t1` (11). Descartados: ninguno.

## Que habilita
Sesion 1 con el trader (registros F09), F11 (parametros nombrados y ambiguedades resueltas),
F14 (casos con `dataset_id` + ventana + hash + gramatica de etiqueta), F26 (holdout-1 y kappa).
