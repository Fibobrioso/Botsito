---
status: ACTIVE
date: 2026-10-26
phase: post-F14 (rama `trabajo/activar-sesion-05-motor`, R4.1 de la hoja de ruta)
---

# 0085 · La vela sin cuerpo en M1 no corta la racha, no es contraria, no forma pivote, no entra en el extremo del punto y no cuenta como alternancia: «casi plana» es cuerpo cero (enmienda ADR-0076 §2; nota en ADR-0061 §4)

> Decisión del consultor del 2026-10-26 (encargo de `trabajo/activar-sesion-05-motor`, puntos 2 y
> 3, y su respuesta a la PARADA, puntos 2, 3 y 6), sobre lo que el trader dijo en la sesión 5 (S-8,
> S-19 y S-24). **Enmienda ADR-0076 §2** (la fila DISTINTO de la vela de cuerpo cero) y su
> cabecera (la regla de la vela sin cuerpo que el consultor retiró el 2026-10-11 vuelve, ahora
> dicha por el trader), con recuadros allí y su fila del índice; **NOTA en ADR-0061 §4**, porque la
> zona de control posterior usa la misma geometría. Lo que el trader no dijo va marcado como
> **DECISIÓN DEL CONSULTOR**.

## Decision

### 1. Lo que dijo el trader

- `ev-v15-003959-5898c61e` (v15 0:39:59): «cambia algo si son 3 velas sin cuerpo en vez de una,
  es indiferente, o sea, las velas sin cuerpo pues no cuentan, en venta lo mismo revés es igual»:
  las velas sin cuerpo dentro del tramo que marca el punto de breaker no cuentan, sean una o tres,
  y en venta igual al revés.
- `ev-v15-004037-a2ab3980` (v15 0:40:37): si entre la verde y la roja hay velas sin cuerpo, el
  máximo de la verde es punto de breaker, «siempre que el precio … haya venido de un order flow
  bajista … pero luego nos tiene que romper, o sea, tiene que cerrar por debajo».
- `ev-v16-000851-f5ae3b6f` (v16 0:08:51): en el retroceso, una vela sin cuerpo, una de uno o dos
  puntos o dos sin cuerpo seguidas no cuentan como alternancia: «no afecta, sigo manteniendo la
  estructura».
- `ev-v16-002841-8cfe382a` (v16 0:28:41, S-24): una vela casi plana «tiene que ser cero puntos … o
  sea si no tiene que ser plana totalmente porque estas velas pues pueden servir también como
  trazo a punto breaker»: el umbral de RN-007 es cero, y corrige lo que dijo en la sesión 4
  (`ev-v10-014310-2296423b`, «casi plana con 1 o 2 puntos», entre comillas): CORRECT sobre ese
  ítem (`fb-2026-10-23-sesion-05-a9e4f879`).

RN-007 ya decía que la casi plana «cuenta como si no existiera» y que sobre ella no se traza punto
de breaker (`fb-2026-09-29-sesion-03-ffab23dc`, CORRECT vivo de la sesión 3); la sesión 5 lo
confirma (`fb-2026-10-23-sesion-05-72c9a9e8`, CONFIRM sobre RN-007) y pone el umbral en cero.

### 2. El cambio, solo en M1 y solo con cuerpo cero

«Sin cuerpo» es `color() == 0` (cierre igual a la apertura, `domain/pivotes_m15.py`): ni cifra
nueva ni parámetro de umbral (ADR-0002, encargo). En M1 la vela sin cuerpo:

- **no corta la racha** del color que la precede, **no es contraria** y **no forma pivote**;
  V, sin cuerpo, R forma el ALTO en el máximo de la verde (`ev-v15-004037`); hasta hoy no formaba
  nada (ADR-0076 §2: «un doji no es de ningún color, no es contraria y corta la racha»);
- **no entra en el extremo del punto**: el punto es el máximo de la verde, no el de la vela sin
  cuerpo;
- **no cuenta como cambio de color en el retroceso** (`ev-v16-000851`): R, sin cuerpo, V, R da lo
  mismo que R, V, R (dos zonas de control; RN-009 lo descarta, como la serie S-10).

Dónde: `pivotes_formados` y `pivote_mas_reciente` (`domain/pivotes_m15.py`) ganan el argumento
`sin_cuerpo` con dos lecturas, `corta_la_racha` (lo de siempre, el valor por defecto y el de M15)
y `no_cuenta`; los tres llamadores con velas de M1 de `domain/estructura_m1.py`
(`referencia_del_breaker`, `zonas_de_control`, `ultimo_punto_de_ruptura`) piden `no_cuenta`, y
`_recorrer_zona_posterior` -la zona de control posterior de RN-014, ADR-0061 §4, «con la misma
geometría de M1 que ya usa el breaker»- salta la vela sin cuerpo sin cortar la racha a favor.
**No cambian** `bloque_de_origen` (la vela sin cuerpo ya no era contraria), `extremo_de_la_caja`
(el 1 de la caja; A-48 ABIERTA; con `r6` el 1 sale de la vela que marca el punto, que se mueve
con él) ni `_pasa` (la ruptura). Medido consumidor por consumidor en la fase 0
(`ACTIVAR-SESION-05-MOTOR.md` §0.b.5).

**M15 no cambia.** `ev-v15-000530-234d4a81` solo dice que una vela sin cuerpo no cuenta como la
vela de después que forma el alto o el bajo, y eso `pivotes_m15` ya lo hacía (no es contraria).
Si en M15 una vela sin cuerpo entre la racha y la contraria corta o no la racha es una pregunta
para la sesión 6. Un test por marco dice que el otro no se mueve.

### 3. DECISIONES DEL CONSULTOR

- **La mecha de una vela sin cuerpo sigue contando donde hoy cuenta**: romper un nivel (`_pasa`,
  la referencia del breaker, el punto de la orden) y el 1 de la caja (`extremo_de_la_caja`).
  Si se mira o no es la pregunta de la sesión 6 (`ACTIVAR-SESION-05.md` §3, 10).
- **Una vela de 1 o 2 puntos de cuerpo sigue siendo de su color**, aunque `ev-v16-000851` diga
  que tampoco cuenta en el retroceso: S-24 dice que vale para trazar el punto, y esa tensión va a
  la sesión 6 (§3, 10). Por eso S-19 no lleva registro: su ítem mete en el mismo saco las velas
  de uno o dos puntos.
- **La condición de `ev-v15-004037` no se aplica.** «Venga de un flujo bajista y después rompa
  cerrando por debajo»: medido, el motor forma el punto con cualquier roja que cierra tras una
  racha verde, sin exigir un flujo previo ni que cierre por debajo del mínimo de la verde;
  exigir «cerrar por debajo» sería pedir cuerpo en M1, contra A-32 RESUELTA (en M1 la mecha
  siempre vale). Va a la lista de la sesión 6.

### 4. Lo que enmienda, y lo medido en la fase 0 sobre S-10

- **ADR-0076 §2**, la fila «alternancia con cuerpo cero en medio (R, doji, V, R) y breaker V»:
  deja de ser DISTINTO. Con este ADR da dos zonas y ningún esquema, igual que la lectura literal
  «sin alternancia»; la única fila DISTINTO que queda es la del breaker contrario que rompe con la
  mecha tras una alternancia, que es la pregunta 2 de ADR-0076 §4 (S-20, «en parte», a la sesión
  6). La cabecera de ADR-0076 retiraba «la regla de la vela sin cuerpo que el consultor había
  decidido el 2026-10-11» porque no hacía falta medirla antes: ahora la dice el trader.
- **NOTA en ADR-0076 §2 con lo medido** (`ACTIVAR-SESION-05-MOTOR.md` §0.b.8): la serie S-10 se
  midió allí con `detectar_esquema`, y por el camino real del cableado (la orden stop en el
  último pivote de M1, `orden_limite_nace = al_aparecer_punto_de_breaker`) S-10 YA ENTRA: la orden
  nace en el primer punto tras la toma y se llena en la primera verde que lo pasa, antes de que
  la alternancia exista; RN-009 solo muerde en el cierre en que hay que colocar o recolocar con
  dos o más zonas ya formadas desde la toma. No se decide nada con eso: va a la sesión 6 (S-15,
  tercer dibujo) y la re-corrida lo mira.
- **ADR-0061 §4**: la zona de control posterior sigue leyéndose con la misma geometría; ahora esa
  geometría salta la vela sin cuerpo. Nota allí.

### 5. Lo que NO se decide aquí

- S-15 (la zona más reciente, RN-009): ninguna frontera de retroceso deja S-10 sin esquema
  (§0.b.8); a la sesión 6 sin registro.
- S-20 (qué pesa más, la mecha que rompe o la alternancia): a la sesión 6.
- Ninguna ambigüedad se cierra; A-21 sigue RESUELTA como la deja ADR-0076.

## Problema que resuelve

El motor formaba el punto de breaker solo si la contraria seguía a la racha sin ninguna vela sin
cuerpo en medio, y contaba una vela sin cuerpo como un corte de la alternancia del retroceso.
El trader dijo en la sesión 5 que las velas sin cuerpo no cuentan, sean una o tres, y que su
umbral es cero: lo que RN-007 decía desde la sesión 3 y el motor no hacía («DESALINEADO»).

## Alternativas consideradas

1. Un argumento `sin_cuerpo` en `pivotes_formados` con `no_cuenta` solo para los llamadores de
   M1, y la zona posterior igual (la elegida).
2. Cambiar `pivotes_formados` para los dos marcos.
3. Quitar las velas sin cuerpo de la serie de M1 antes de medir.

## Por que elegimos esta opcion

Porque el trader lo dijo de M1 y de M15 solo dijo que la vela sin cuerpo no es la contraria; cada
marco con su argumento, y un test que dice que el otro no se mueve (fase 0, b.3).

## Por que descartamos las demas

- La 2 movería la liquidez de M15 con una respuesta que no es de M15.
- La 3 cambiaría los índices de las velas (la que marca el punto, la caja) y las mechas de las
  velas sin cuerpo, que el consultor decide que siguen contando donde hoy cuentan.

## Impacto

- **Registro y spec:** sin parámetro nuevo. RN-007: sus notas (casi plana es cuerpo cero desde
  `fb-2026-10-23-sesion-05-a9e4f879`; el motor lo hace por este ADR; las mechas y las velas de 1
  o 2 puntos van a la sesión 6); su literal y su cita no cambian. Registros:
  `fb-2026-10-23-sesion-05-72c9a9e8` (CONFIRM sobre RN-007) y `fb-2026-10-23-sesion-05-a9e4f879`
  (CORRECT sobre `ev-v10-014310-2296423b`). `spec_version` 18.2.0 → **18.2.1** (redacción).
- **Código:** `domain/pivotes_m15.py` (`sin_cuerpo`), `domain/estructura_m1.py` (los tres
  llamadores y `_recorrer_zona_posterior`).
- **Docs:** recuadros en ADR-0076 (cabecera y §2) y su fila del índice; nota en ADR-0061 §4 y su
  fila.
- **Tests:** `tests/unit/test_velas_sin_cuerpo_m1.py` (nuevo): V, sin cuerpo, R da el punto en el
  máximo de la verde, en compra y en venta, con una y con tres; R, sin cuerpo, V, R da lo mismo
  que R, V, R; una vela de 1 punto sigue contando como color; la zona posterior salta la vela sin
  cuerpo; por el camino real, el productor liga la zona del punto que la vela sin cuerpo cortaba;
  las series de M15 no se mueven. `tests/unit/test_a21_series.py`: la fila del doji y
  `test_las_diferencias_son_solo_el_doji_y_el_breaker_por_mecha` (ahora solo el breaker por mecha)
  cambian de sentido a propósito. `tests/unit/test_orden_stop_pivote.py::test_son_las_funciones_de_r5_y_r6_de_caja_77`
  compara con el guion de CAJA-77 solo las series sin velas sin cuerpo, y un test nuevo exige que
  en las que las llevan la única diferencia sea este punto (el guion no se toca). Fallan con el
  código de `main`: `ACTIVAR-SESION-05-MOTOR.md` §1.2.
- **Sin arnés y sin material**: velas sintéticas.

## Fecha / fase

2026-10-26 · rama `trabajo/activar-sesion-05-motor` (R4.1). Informe:
`docs/validation/ACTIVAR-SESION-05-MOTOR.md`.

## Estado

ACTIVE
