---
status: ACTIVE
date: 2026-09-26
phase: post-F14 (rama `trabajo/preparar-a21`)
---

# 0055 · RN-011 y la zona de entrada: preparada para A-21, con el selector de «limpia» PROVISIONAL

> **ACEPTADO** por el consultor en la orden de cierre de `trabajo/preparar-a21`, tras revisar
> `docs/validation/PREPARACION-A21.md` y `docs/validation/VERIFICACION-A21.md` (commit `b007abd`).

## Decision

### 1. Los predicados del motor son puros

RN-011 no disparaba aunque el esquema existía. El predicado `toca_colocar_orden_limite` tenía un
efecto de un solo disparo («la primera vez que se ve el esquema»), y el intérprete evalúa el
`cuando` de las demás reglas de la misma clase de forma ESPECULATIVA para el aviso de empates H3
(`Interprete._empatadas`, `engine/interprete.py`; ADR-0049). El disparo se consumía en esa
evaluación, que no ejecuta nada, y cuando le tocaba a RN-011 el predicado ya daba NO.

Qué se cambió (`engine/zonas.py`, `primitivas_zona`): `toca_colocar_orden_limite` da SI
exactamente en el minuto del cierre del breaker y NO en cualquier otro, sin estado consumible, y
registra la zona de forma IDEMPOTENTE (el mismo id para el mismo esquema, aunque se evalúe varias
veces en la misma pasada). La regla que queda: **un predicado no tiene efectos que dependan de
cuántas veces se evalúe**; el estado que tenga que producir se registra de forma idempotente.

Qué test lo cubre: `tests/unit/test_preparar_a21.py::test_el_primer_esquema_forma_la_zona_y_rn011_la_liga_en_el_cierre_del_breaker`,
que corre la spec real por el intérprete y exige que RN-011 dispare y fije `orden_dimensionada`
en el cierre del breaker; con el predicado de un solo disparo fallaba. No hay un test dedicado que
evalúe el predicado dos veces seguidas: la cobertura es de punta a punta.

### 2. El selector de «limpia» es PROVISIONAL, y A-21 sigue ABIERTA

`zona_control_limpia` (UNKNOWN) ofrece las dos condiciones de validez que el corpus enuncia:
`solo_una_zona_de_control` (lo que ya dice RN-009) y `sin_mecha_mas_alla_del_extremo` (v4 0:53:10,
`ev-v4-005310-ce69f8c6`, con el nivel supuesto, A-32). Ninguna es una definición documentada de
«limpia», y en construcción casi no difieren: ligan la misma zona cuando ligan las dos, y el
«dentro» medido es el mismo con ambas (6 y 6). El selector queda como mecanismo para recibir la
respuesta del trader; si la respuesta no calza en ninguna de las dos, se para
(`docs/runbooks/ACTIVAR-A35-A44.md` §6). A-21 no se resuelve ni se decide aquí.

### 3. El veredicto de la verificación (`VERIFICACION-A21.md`)

Con las cifras del informe, en DIAGNÓSTICO y solo sobre construcción:

- **6 de 77** entradas del trader caen dentro de la zona viva del motor en el instante del
  llenado; **7 de 77** con la tolerancia de entrada de ADR-0043 (3 puntos). Igual con las dos
  lecturas del selector.
- **38 de 77** operaciones no tienen zona viva en el llenado (lectura `solo_una_zona_de_control`):
  18 antes de cualquier toma del día y 20 con toma pero sin esquema válido antes del llenado.
- Las variantes **cuerpo en lugar de mecha**, **grupo de velas contrarias** y **otra vela
  contraria entre la toma y el breaker** casan con **0 operaciones**: quedan descartadas como
  explicación principal de las entradas que caen fuera.
- Las coincidencias medidas son **«zona anterior a la toma» (19)** y **«M15 del bloque» (7)**.

Esto no dice cuál es la geometría correcta. Eso lo decide la respuesta del trader (A-21 y el
material de dibujo de la reunión); el ADR solo deja constancia de lo medido.

### 4. Incoherencia conocida entre reglas con una toma de otra sesión: DEUDA

`liquidez_tomada` no caduca al abrir la sesión (la spec escribe `caduca` solo para `sesgo`), así que
el productor de la zona usa la PRIMERA toma del día. Medido en construcción: en las 31 sesiones que
abren con una toma hecha en una sesión anterior del mismo día, **RN-008 y RN-009 disparan con esa
toma (31 de 31) y RN-011 no dispara nunca (0 de 31)**, porque el minuto del breaker de esa toma ya
pasó. Las tres reglas leen la misma toma y no son coherentes entre sí. **No se corrige en esta
rama**: queda como deuda conocida, ligada a la ambigüedad A-46 («si la liquidez se tomó en una
sesión anterior del mismo día, ¿sigue valiendo para operar en la siguiente?»). Según la respuesta,
o la spec escribe la caducidad de `liquidez_tomada` y el productor la sigue, o hay que decidir qué
hace RN-011 con una toma de la mañana.

### 5. Rutas que caben en Windows y etiquetas cortas del diagnóstico

El nombre del fichero de diagnóstico lleva la forma compacta
`.DIAGNOSTICO.a35=<lectura>.a44=<modo>.a21=<lectura>` en lugar de las etiquetas completas; las
líneas y las páginas siguen llevando las etiquetas completas, y el contrato de ADR-0054 no cambia:
un fichero de diagnóstico nunca se llama como una línea base. `comprobar_ruta`
(`engine/diagnostico.py`, `LIMITE_RUTA_WINDOWS = 259`) rechaza, ANTES de leer una vela, toda ruta
que el arnés o el visor vayan a escribir y que pase de ese límite, con código 2 y un mensaje que
dice cuántos caracteres tiene. Lo vigila `tests/unit/test_rutas_windows.py`.

## Problema que resuelve

RN-011 era una parada NO_IMPLEMENTADA (`toca_colocar_orden_limite`) y el embudo no pasaba de ahí.
La geometría de la zona de entrada tenía que construirse sin decidir por el trader lo único que el
corpus no documenta, «limpia»; y la primera medida contra sus entradas tenía que verificarse antes
de llevarla a la reunión.

## Alternativas consideradas

1. Construir la geometría con el selector de «limpia» UNKNOWN y verificar la medida antes de
   aceptarla (lo elegido).
2. Elegir una lectura de «limpia» por cobertura sobre construcción.
3. Esperar a la respuesta del trader para escribir nada.
4. Corregir en esta rama la incoherencia de RN-008/RN-009/RN-011 con la toma de otra sesión.

## Por que elegimos esta opcion

Deja RN-011 activable con un valor y un comando, con la medida verificada y sus supuestos escritos,
y sin elegir nada que le toque al trader.

## Por que descartamos las demas

- **(2)** la lectura la elige el trader, no el ajuste; y además las dos lecturas casi no difieren.
- **(3)** sin la geometría no hay material de dibujo para la reunión ni forma de medir la respuesta.
- **(4)** la corrección depende de la respuesta a A-46; corregirla antes sería decidirla.

## Impacto

- `domain/estructura_m1.py`, `engine/zonas.py`, `EstadoDia.memoria` en `engine/interprete.py`, el
  cableado y el visor con la zona; `engine/diagnostico.py` con `comprobar_ruta` y el nombre
  compacto; `--diagnostico-a21` en la CLI.
- Registro: `zona_control_limpia` UNKNOWN; spec 13.3.0.
- Nace A-46 (la liquidez de otra sesión del mismo día).
- `docs/validation/PREPARACION-A21.md`, `docs/validation/VERIFICACION-A21.md`, §6 de
  `docs/runbooks/ACTIVAR-A35-A44.md`, `scripts/verificacion_a21.py`,
  `scripts/verificacion_a21_entradas.py`.

## Fecha / fase

2026-09-26 · rama `trabajo/preparar-a21`.

## Estado

ACTIVE
