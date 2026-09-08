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
  usuario): 21 preguntas (P-01 a P-03 bloqueantes: A-2, A-4, A-9), 40 casos de un universo de 42 dias no vistos (mayo y junio de 2026; 67 dias excluidos con motivo: 66 de meses vistos y el primer laborable de mayo por caer fuera del dataset), 16 `dev` + 8 + 8 + 8 con seed 20260915; `kit check` en verde; `knowledge validate` en verde con la capa kit.

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
Las 13 del brief (desviacion anotada: los commits de `ambiguedades.yaml` y `config.yaml` citan
`Fuente: ADR-0011`; los `ev-*` van dentro de los ficheros y `knowledge validate` lo acepta; las
bloqueantes van por numero: A-2, A-4, A-9). Destacan: julio y agosto estan VISTOS (v3 dibuja sobre julio; agosto tiene
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
`make check` verde: 344 funciones de test, 489 casos (antes 326 / 471 en `stable/F08`). Nuevos: ambiguedades (esquema real 12/12, errores, contexto,
anti-deriva), particiones (determinismo con orden de entrada distinto, seed distinto, errores),
gramatica de etiqueta (6 casos invalidos), kappa (matriz clasica 20/5/10/15 -> po 0,70, pe 0,50,
kappa 0,40; acuerdo total; una categoria; unidades distintas; etiqueta fuera), paquete
(determinista, universo con dia visto y dia fuera del dataset, limites H4 de los dos anclajes
en verano, cuestionario con fusion y contradiccion, hoja solo `dev` y sin `ev-*`, escribir sin
sobreescribir, `check` puro y con config cambiada, sin datos), config y mapa estrictos, kappa
desde registros con `supersede` y CLI, `validar_paquetes` sin git, ventana en invierno,
guardia de ancestro (antes = OK; despues y mismo commit = error).

## Resultados
### Paquete de la sesion 1 (real)
| Medida | Valor |
|---|---|
| Preguntas | 21 (12 ambiguedades con sus parametros fusionados, 9 parametros sueltos, 0 contradicciones sueltas: `stop.nivel` va con A-10) |
| Casos por pregunta | 2 a 3; todos con `ev-*` existente y fotograma de referencia |
| Universo de dias no vistos | 42 (mayo y junio de 2026; el 2026-05-01 queda fuera del dataset) |
| Casos en el paquete | 40 (16 dev, 8 holdout-1, 8 holdout-2, 8 holdout-3) |
| Dias excluidos | 67 (66 de enero, julio y agosto por meses vistos; 2026-05-01 por caer fuera del dataset) |
| Velas por caso | 889 a 900 (ventana de 900 min; minimo exigido 850) |
| Determinismo | `kit check` recompone los 4 ficheros byte a byte; dos `build` con el mismo seed = mismos bytes |

### Fallos lexicos y limites conocidos
Las preguntas se generan solo con evidencia existente: los 24 parametros UNKNOWN tienen al menos
un item de evidencia por tema (`kit build` falla si no). El anclaje `servidor-ny-17` es el unico
que reproduce las sesiones 07/11/15 del trader; la hoja lo marca.

## Que deberia observar el usuario
`knowledge validate` con la linea "OK: 12 ambiguedades registradas; 1 paquetes de sesion
validos, particiones anteriores al etiquetado"; `kit check` en verde; `hoja_trader.md` con
las 21 preguntas (3 bloqueantes primero) y solo los 16 casos `dev` con las dos rejillas H4.

## Que casos funcionan
Todo el alcance del brief.

## Que casos todavia no funcionan
- El runner de casos, las fixtures OHLC copiadas y las etiquetas del sistema son F14.
- Registrar el feedback de la sesion es `feedback new` (F09) tras la sesion.
- Golden H4 contra la captura del trader (test de regresion sobre F15, trasladado a F10 el
  2026-09-07): no hay captura todavia; P-03 la pide en la sesion 1 y el golden se escribe en F11 al
  fijar `anclaje_h4`.

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
Hecha el 2026-09-08 con dos agentes; todo lo que sigue esta aplicado en la rama.

**Codigo y tests** (1 bloqueante, 6 importantes, 8 menores):
- B-1 la guardia de particiones solo miraba el commit de alta: reasignar `particiones.yaml`
  DESPUES del etiquetado (commiteado o en el arbol de trabajo) pasaba `knowledge validate`.
  Ahora, en cuanto hay un `LABEL_CASE` de la sesion, `particiones.yaml` y `ventanas.yaml` deben
  ser identicos a su commit de alta (`comun.historial.intacto_desde`); test de contrato con los
  tres escenarios.
- I-1 paquete malformado daba traceback en `knowledge validate`: esquema estricto en
  `esquema_paquete`. I-2 `huso_operativa` no IANA daba traceback: `huso_canonico` en `build`.
  I-3 `AmbiguedadError` escapaba en `feedback new`. I-4 el mensaje de `kit build` daba un
  universo falso: `Paquete.universo`. I-5 escritura no atomica: temporal + `rename`. I-6 `build`
  citaba en silencio evidencia inexistente o superseded y admitia ambiguedades inexistentes en el
  mapa: ahora valida las ambiguedades contra el contexto, usa solo items activos y exige que el
  mapa cite ambiguedades existentes.
- M-1 hora `00-23:00-59` y claves `k=v` repetidas rechazadas; M-2 nombre de sesion, prefijo y
  dias validados; M-3 categorias sin unidades fuera del acuerdo por categoria; M-4 errores de
  `kit check` por stderr; M-5 duracion con 3 decimales; M-6 mapa afinado (`ventana_inicio`,
  `lotaje_base`); M-7 duplicados eliminados; M-8 el mes anterior contiguo aporta el contexto del
  primer dia de cada mes (por eso `caso-eurusd-2026-06-01` existe).
- Sin problema: ventanas en las 6 fechas de cambio de hora (ambos anclajes, subconjunto de
  `limites_del_dia`), `hash_ventana` determinista, dos datasets con el mismo dia = error,
  particiones con cupos menores que el universo, cuestionario real (21 preguntas, 59 casos con
  fotograma, 24 UNKNOWN cubiertos, A-10 fusiona tres origenes), determinismo con
  `PYTHONHASHSEED` distinto, gramatica y kappa (fixture clasica, prevalencia, `pe = 1`),
  `comprobar` puro, CRLF, `sesiones_del_kit`, git (rutas con espacios, repo sin commits, rename,
  sha corto), feedback (`t1 == duracion` aceptado, fichero con espacios), CLI sin tracebacks,
  contrato de capas KEPT.

**Docs y proceso** (1 bloqueante, 7 importantes, 6 menores):
- B-1 `hoja_trader.md` pedia al trader confirmar los meses VISTOS (enero, julio, agosto) en vez
  de los del paquete: la hoja calcula ahora los meses desde los casos ("2026-05, 2026-06"), con
  test; paquete regenerado (`particiones.yaml` y `ventanas.yaml` byte-identicos; sin
  `LABEL_CASE` todavia, la guardia no se dispara); `kit check` en verde.
- I-1 ADR-0010 y ADR-0011 en el indice de PROJECT_STATE; I-2 Important Files con el kit y el
  registro actualizado (25 parametros); I-3 Current Feature, Waiting, Next Feature y Next Action
  reescritos; I-4 MASTER_PLAN H.2 ("Sesion 1 sin registro...", "Tres particiones reservadas") y
  §G con lo hecho (guardia de ancestro, no de fecha; bloqueantes A-2/A-4/A-9); I-5 ADR-0011 con
  el mes anterior contiguo y la inmutabilidad tras el etiquetado; I-6 el golden H4 sobre F15
  queda declarado (pendiente de la captura de P-03; se escribe en F11) y la fila A-9 de Known
  Ambiguities apunta a la sesion 1; I-7 cifra de velas corregida (889 a 900).
- M-1 desviacion de `Fuente:` anotada en Decisiones tomadas; M-2 orden de las bloqueantes por
  numero en el brief; M-3 gramatica completa en el README del kit; M-4 README de feedback con
  ambiguedades, duracion y gramatica; M-5 comandos `kb` y `kit` en el HANDOFF; M-6 v5 en Drive.
- Correcto: las 13 decisiones del brief en codigo, datos y tests; ADR-0011 indexado; informe
  segun plantilla; `vistos.yaml` cita `ev-*` existentes; `particiones.yaml` commiteado antes de
  cualquier etiqueta; sin `generado_el` ni rutas absolutas; `fuentes.yaml` sin cambios; 7
  commits con trailers y `Fuente:` donde toca; ritual §F compatible con `state check`.

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
