---
status: ACTIVE
date: 2026-09-04
phase: F15 (auditoria de arquitectura previa a la fusion)
---

# 0006 · Capas revisadas, paquete `comun` y accesores del registro por tipo declarado

## Decision
1. El contrato de capas pasa a: `cli` → `validation` → `viewer | mql5bridge` → `engine` →
   `cases` → `spec` → `feedback` → `evidence | corpus | data | config` → `comun` → `domain`.
   `validation` (F26, F30, F32) conduce el motor y el puente MQL5; `viewer` (F25) lee el journal
   del motor; `engine` (F23, F24) consume `cases`, `spec` y `data`. Antes eran hermanos
   independientes y el contrato habria roto en F25.
2. El kit de elicitacion (F10) vive en `cases/` (o en un paquete por encima), no en `feedback/`:
   necesita generar ids de caso, seed y particiones, que estan por encima de `feedback`.
3. Nuevo paquete `botsito.comun`, sin logica de negocio, por encima de `domain` y por debajo de
   todo lo demas: `yaml_estricto` (antes en la raiz), `historial` (antes en `evidence/`, pero
   vigila feedback, manifiestos de datos y trailers de spec/cases), `documentos` (normalizacion,
   vacios, hash corto, recorrido de directorios, cadenas de supersede, activos), `ids` (todos los
   formatos de identificador, ASCII estricto) y `husos` (nombre IANA canonico, un solo criterio
   para registro y datos). `domain` no puede importar `comun`.
4. Los accesores tipados del registro (`registro.fraccion("x")`, `.entero`, `.puntos`...)
   comprueban el `tipo` DECLARADO del parametro, no el tipo Python del valor: `Puntos`, `Minutos`
   o `Lotes` son `int`/`Decimal` en tiempo de ejecucion y no se distinguirian. Un test de
   contrato recorre el AST de `src/` y exige que cada `registro.<accesor>("nombre")` cite un
   parametro existente con ese tipo.
5. `SerieVelas` lleva `origen` (dataset_id) y `cargar_serie` acepta ventana por instante
   (`MinutoUtc`) ademas de por dia UTC: un caso (F14) y el journal (F23) citan de que dataset y
   ventana salen sus velas, y una H4 anclada a 17:00 Nueva York cruza la medianoche UTC.
   `agregar_serie` devuelve una `SerieVelas` con escala y procedencia; `agregar` (lista) se
   conserva para el nucleo puro.

## Problema que resuelve
La auditoria de arquitectura previa a fusionar F15 encontro que el contrato de capas contradecia
las dependencias de la fase 5 y 6, que tres capas copiaban las mismas utilidades (regex de ids,
normalizacion, hash, directorios, supersede) y que el registro no podria separar puntos de
minutos en F11/F18. Corregirlo con los paquetes vacios cuesta un refactor mecanico; en F25 seria
una urgencia.

## Alternativas consideradas
1. Dejar el contrato y relajarlo cuando fallara.
2. Un paquete `infra` con IO ademas de utilidades.
3. Constantes generadas para los nombres de parametro.

## Por que elegimos esta opcion
El contrato escrito hoy es el que el plan (tabla A, H.2) ya implica; `comun` no tiene IO ni
negocio, asi que no compite con `domain`; el test AST detecta typos de nombre sin abrir una
segunda puerta a los valores (ADR-0002).

## Por que descartamos las demas
(1) Deja una contradiccion conocida en el repositorio. (2) Mezclaria IO con utilidades puras y
tentaria a `domain`. (3) Duplica la fuente de verdad del registro.

## Impacto
`pyproject.toml` (contrato), `src/botsito/comun/*`, imports en `config`, `corpus`, `evidence`,
`feedback`, `data`, `cli` y tests; `config/registro.py` (`_tipado`); `domain/velas.py`
(`SerieVelas.origen`), `data/dataset.py`, `data/agregacion.py`; `tests/contract/
test_import_contracts.py` (prohibiciones ampliadas, sin `float`/`Decimal` en `domain` salvo
`valores.py`, accesores del registro); ADR-0001 remite a este ADR. Los ids ya escritos no cambian
(`contenido_canonico` sigue en cada capa, byte a byte).

## Fecha / fase
2026-09-04 · F15

## Estado
ACTIVE
