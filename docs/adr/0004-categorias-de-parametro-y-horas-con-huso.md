---
status: ACTIVE
date: 2026-09-04
phase: F09 (auditoria extrema previa a F15)
---

# 0004 · Categorias de parametro y horas con huso

## Decision
Cada parametro del registro declara una `categoria`: `estrategia` (lo que el trader sabe y
confirma), `instrumento` (digitos, punto, tamano de contrato, lote minimo/paso/maximo, stops y
freeze level), `broker` (simbolo con sufijo, modo de llenado, expiraciones admitidas, comision,
huso del servidor), `prop_firm` (perdida diaria y total, lote maximo, presupuesto de mensajes,
reglas de consistencia) y `ejecucion` (magic number, modelo de llenado simulado, latencia
supuesta). Solo `estrategia` se cita por evidencia o feedback y se le pregunta al trader; el resto
se cita por decision (`ADR-NNNN`) y se verifica contra el terminal en el pre-vuelo (F33).
`no_confirmados()`, `feedback pending` y el kit de F10 filtran por `estrategia`.

Todo parametro de tipo `hora` lleva `huso` (nombre IANA, validado con `zoneinfo`; `tzdata` es
dependencia del proyecto porque Windows no trae base de datos de husos). El dominio recibe un
`HoraLocal(hora, huso)`, nunca una cadena `HH:MM`.

## Problema que resuelve
La auditoria extrema del 2026-09-04 encontro dos huecos que habrian aparecido al operar: (1) los
parametros del instrumento, del broker y de la prop firm no tenian hogar, asi que Python (F24) y
MQL5 (F28/F31) los habrian declarado por separado y `no_confirmados()` se los habria preguntado al
trader, que no puede confirmar una regla de FundedNext; (2) `07:00` sin huso no dice de que reloj
es, y el plan tiene tres relojes (trader en Europe/Madrid, servidor del broker en GMT+2/+3, datos
en UTC) cuyo desfase cambia en las semanas en que el horario de verano de Europa y el de Nueva York
no coinciden.

## Alternativas consideradas
1. Un fichero distinto por categoria (`instrumento.yaml`, `prop_firm.yaml`).
2. Meter instrumento y broker en `settings.toml`.
3. Un unico `huso_global` en `settings.toml` y horas desnudas en el registro.

## Por que elegimos esta opcion
Una sola puerta con categoria conserva lo que ADR-0002 protege (tipos, estados, fuente por valor,
un solo hash de spec en F11/F28) y anade la distincion que faltaba: quien puede confirmar cada
valor. El huso viaja con la hora porque un valor sin unidad es exactamente el error de factor 100
que ADR-0002 quiso impedir, ahora en el eje del tiempo.

## Por que descartamos las demas
(1) Varios ficheros son varias puertas: hashes distintos y sin categoria en el journal. (2)
`settings.toml` es entorno, no negocio, y `config validate` lo prohibe por diseno. (3) Un huso
global se pierde en cuanto hay una hora del servidor y otra del trader en la misma spec.

## Impacto
`config/registro.py` (campo `categoria`, `huso`, `por_categoria()`, formato de ids de fuente,
`HoraLocal`), `domain/valores.py`, `knowledge/spec/parametros.yaml` (esquema), `pyproject.toml`
(`tzdata`). F11 puebla las categorias de entorno citando este ADR; F15 declara `huso_datos` y
`huso_operativa`; F28 exporta `estrategia + instrumento + ejecucion` a `Params.mqh` y `prop_firm`
a `Risk.mqh` con dos hashes; F33 compara `instrumento` y `broker` con `SymbolInfo*` y
`AccountInfo*` y aborta si difieren.

## Fecha / fase
2026-09-04 · F09 (auditoria extrema)

## Estado
ACTIVE
