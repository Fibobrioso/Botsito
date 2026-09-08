---
status: ACTIVE
date: 2026-09-08
phase: F10
---

# 0011 · Kit de elicitacion: ambiguedades legibles por maquina, registro pre-poblado, ventanas no vistas con particiones commiteadas antes y kappa desde el feedback

## Decision
1. **Ambiguedades legibles por maquina** en `knowledge/spec/ambiguedades.yaml` (`id` A-N,
   `titulo`, `pregunta`, `resuelve_en`, `evidencia` con ids existentes, `parametros` del
   registro, `contradiccion` o null, `estado` ABIERTA | RESUELTA, `bloqueante`). La tabla de
   PROJECT_STATE es su reflejo y un test exige que ids y titulos coincidan. F09 valida el
   objetivo `ambiguedad` contra este fichero. Se cierra una ambiguedad solo con un registro del
   trader, en un commit con `Fuente:`.
2. **Registro pre-poblado**: todo parametro de estrategia que la evidencia nombra existe en
   `knowledge/spec/parametros.yaml` en `UNKNOWN` sin valor (24 con `anclaje_h4`), para que
   `RESOLVE_UNKNOWN` tenga objetivo en la sesion 1 y F11 solo ponga valores con fuente. El
   enlace parametro -> temas de evidencia, ambiguedad y opciones cerradas vive en
   `knowledge/cases/kit/mapa_parametros.yaml` (el esquema estricto del registro no admite claves
   extra).
3. **Los datos de negocio del kit son DATOS** (`knowledge/cases/kit/config.yaml`: simbolo,
   ventana del dia operativo, sesiones H4, anclajes candidatos, etiquetas, cupos de particion),
   nunca literales en `src/` (`test_no_business_literals`). Las horas van en `huso_operativa`.
4. **Ventanas de replay = dias operativos NO vistos** por el trader: `vistos.yaml` excluye meses
   enteros cuando no se puede saber que dias vio (enero, julio y agosto de 2026) y dias sueltos;
   el universo son los dias laborables de los datasets congelados cuya ventana completa cae
   dentro del dataset y tiene suficientes velas M1 (el mes anterior congelado y contiguo aporta
   el contexto de la vispera del primer dia; el caso cita el dataset de su dia). Cada caso: `caso-<simbolo>-<dia>`,
   `dataset_id`, ventana UTC, `n_velas`, `sha256` de las velas (recomputable con
   `cargar_ventana`) y los limites H4 de cada anclaje candidato (`limites_entre`). CONDICION de
   cada sesion: confirmacion escrita del trader (registro F09) de que no ha visto esos meses.
5. **Seed y particiones**: orden por `sha256(f"{seed}:{caso}")` (independiente de la version de
   Python), cupos dev / holdout-1 / holdout-2 / holdout-3 de `config.yaml`. `particiones.yaml`
   se commitea ANTES de la sesion; la guardia (`knowledge validate`) es de ANCESTRO en git: el
   commit que anadio `particiones.yaml` precede al que anadio el primer `LABEL_CASE` de esa
   sesion (`git merge-base --is-ancestor`); la fecha de committer es solo informativa; desde ese
   momento `particiones.yaml` y `ventanas.yaml` son inmutables (`intacto_desde`). La hoja del
   trader solo lleva los casos `dev`.
6. **Etiqueta por SESION H4**, no por dia: `LABEL_CASE` con `valor_resultante` en la gramatica
   `07-11: venta@08:37 e=... sl=... tp=...; 11-15: no_trade` (una decision por sesion
   declarada, decision en `etiquetas`). F14 la formaliza.
7. **Kappa de Cohen desde los registros F09** (`kit kappa --sesion-a --sesion-b`): unidades
   (caso, sesion) de los `LABEL_CASE` activos (respetando `supersede`); exacto en fracciones,
   con matriz, acuerdo por categoria y aviso de prevalencia. Sin kappa ponderado.
8. **Grabaciones de sesion como `videos` de `fuentes.yaml`** (transcribibles con F04, citables),
   con `drive_id` opcional cuando la `naturaleza` empieza por `sesion`; `grabacion` de un
   registro puede ser un video y `t1` no supera su `duracion_s`. Sin grabacion, `medio: escrito`.
9. **Paquete determinista y sin sobreescritura**: `kit build --sesion --seed` escribe
   `knowledge/cases/kit/<sesion>/{cuestionario.yaml,ventanas.yaml,particiones.yaml,
   hoja_trader.md}` sin `generado_el` ni rutas; `kit check` es puro (recompone y compara bytes;
   sin `data/`, solo esquema). Todo commit bajo `knowledge/cases/` lleva `Fuente:`.

## Problema que resuelve
La sesion 1 con el trader (MASTER_PLAN §G) necesita preguntas con caso concreto por cada
incognita, un paquete de etiquetado ciego sobre dias que no ha visto, y la asignacion a
particiones cerrada antes de que etiquete; y F26 necesita medir el acuerdo entre rondas. Nada de
eso puede vivir en codigo con cifras de negocio ni depender de ficheros editables a mano.

## Alternativas consideradas
(1) Ambiguedades solo en PROJECT_STATE (Markdown). (2) Ventanas de julio/agosto (ya
descargados). (3) Etiqueta por dia. (4) `random.shuffle(seed)`. (5) Guardia por fecha de
committer. (6) Rondas de kappa en ficheros aparte. (7) Nombrar los parametros en F11.

## Por que elegimos esta opcion
Un YAML con esquema es validable y citable desde el feedback; la revision de diseno demostro que
julio y agosto estan vistos (v3 dibuja sobre julio; agosto tiene dos backtests sin fecha por dia)
y que el trader decide por sesion H4, no por dia; el orden por hash es reproducible en cualquier
Python; el ancestro en git no se falsifica con `GIT_COMMITTER_DATE`; las rondas en F09 tienen
autor y fecha (invariante de §G); nombrar los parametros ahora da objetivo a `RESOLVE_UNKNOWN`.

## Por que descartamos las demas
(1) No es legible por maquina ni validable. (2) Un paquete sobre dias vistos no mide nada. (3)
Mezcla una compra de 07-11 con una venta de 11-15 y rompe FP/FN por caso. (4) Sin garantia entre
versiones. (5) Cambia con rebase y es falsificable. (6) Duplica la verdad fuera de la guardia de
historial. (7) Dejaria la sesion 1 sin objetivos.

## Impacto
`src/botsito/cases/{ambiguedades,cuestionario,ventanas,particiones,kappa,paquete}.py`,
`src/botsito/cli.py` (`kit build|check|kappa`), `src/botsito/validation/knowledge.py` (capa
kit, ambiguedades, duraciones), `src/botsito/feedback/modelo.py`, `src/botsito/corpus/inventario.py`,
`src/botsito/comun/historial.py` (`commit_que_anadio`, `es_ancestro`),
`knowledge/spec/{ambiguedades,parametros}.yaml`, `knowledge/cases/kit/*`, datasets 2026-05 y
2026-06, tests. Ningun id existente cambia.

## Fecha / fase
2026-09-08 · F10

## Estado
ACTIVE
