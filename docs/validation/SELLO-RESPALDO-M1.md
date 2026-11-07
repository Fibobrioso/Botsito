# SELLO-RESPALDO-M1 · la marca de _peor_del_minuto y las cancelaciones en el cierre de una M1 sin ticks

Rama `trabajo/sello-respaldo-m1`, abierta el 2026-11-07 desde `main` (2e04b63, commit de estado
sobre el merge 8f43d38 del tag `stable/F38p-demo-ejecuciones-2-3`). Encargo:
`docs/encargos/trabajo-sello-respaldo-m1.md`. Tramo «R3 · Una corrida del arnés sobre toda la
construcción» (R3.6 de la hoja de ruta; H de la Next Action). Rama de noche, con las decisiones del
consultor por adelantado (D1-D5) y PARADA condicional.

```ids-inexistentes
ADR-0091 — el número que el encargo reserva para el ADR del sello; D2 dio (c2) y esta rama NO lo crea: aquí solo va su borrador (§2), y el ADR lo escribe la rama de (c2)
```

## Base comprobada al abrir (2026-11-07)

- `git rev-parse main origin/main`: `2e04b632b81df9d702939626dbe26afdf1b7beea` las dos veces; su
  asunto es `docs(state): trabajo/demo-ejecuciones-2-3, cerrada en main (stable/F38p-demo-ejecuciones-2-3)`.
- `git rev-parse main^1` = `git rev-parse "stable/F38p-demo-ejecuciones-2-3^{commit}"` =
  `8f43d381a50a0466c31aea13401323c0eeb37ae5`; el tag esta en origin (`git ls-remote --tags`), y es
  la ultima linea `- Tag: ` de `docs/state/HISTORIA.md`.
- CI de `main` sobre su HEAD: `gh run view 42342344212` → `completed` / `success`, headSha
  `2e04b632b81df9d702939626dbe26afdf1b7beea`, rama `main`, workflow `ci`.
- `git branch -a` solo daba `main` y `origin/main`; `git ls-remote --heads origin` solo `main`.

## Resumen

- **Los «22» son CANCELACIONES del bot, no eventos del respaldo** (el auditor, afirmación 8): órdenes
  que el motor cancela en el cierre de una M1 sin ticks, cuya vela nunca se evalúa para ellas. La
  reconstrucción de `censo_cierre.py` da **22** sobre la diaria de RECORRIDA (la que contó
  RESPALDO-M1) y **26** sobre la de RESPALDO-M1; con el código de **este main**, día a día con el
  visor, son **27** en los mismos once días de construcción.
- **D2 da (c2).** Con el código de main, la M1 k de **2 de las 27** las habría llenado
  (2026-01-23, o29, venta stop; 2026-07-10, o3, compra stop), y con (c2) en el prototipo las dos
  pasan a ser **operaciones nuevas del bot** (−1,00 R cada una). Por la regla de D2, el camino es
  (c2) y NO se implementa esta noche: PARADA con el plan (§2).
- **(e2), D1:** una línea en `broker.py:955`; con (e2) pasan los 343 tests de main de los 29 ficheros
  que tocan el bróker, el llenado, el cableado o la simulación; en las sondas solo cambian las
  marcas (S5, S7, S7b); en los once días, órdenes y operaciones idénticas a main. Se aplica en la
  fase 1, con su test (`tests/unit/test_peor_del_minuto.py`: 2 rompen en main, 2 pasan en los dos).
- Ninguna corrida del arnés; ninguna cifra agregada sobre un mes ni sobre la construcción.

## 0. Fase 0 · inventario sin commitear cambios de código (2026-11-07)

Ni una línea de `src/`, tests, spec ni knowledge en el commit de la fase 0. Lo medido sale de: el
código de `main`; dos salidas ya commiteadas (las diarias de RECORRIDA y de RESPALDO-M1), leídas por
`censo_cierre.py`; el visor por caso sobre once días dev, con (e2) y (c2) parcheadas en memoria
(`prototipo_sello.py`); y un clon desechable de `main` (`C:/cm/h`, `git worktree add --detach`, con
`config/settings.local.toml` apuntando al `data/` real) con las formas escritas a mano. Guiones y
salidas, en `docs/validation/anexos/SELLO-RESPALDO-M1/` (su README). Exposiciones: §0.j.

### 0.a diagH, contrastado con este main

Encontrado y leído en solo lectura (la guardia no lo negó):
`C:\Users\USER\AppData\Local\Temp\claude\C--Users-USER-Desktop-Bot-v3\d3c2b437-47f5-42c0-a80a-f34a5dc48fc2\scratchpad\diagH\INFORME-DIAG-H.md`
(490 líneas, base `main` = 7a3a1ff, F38k, comisión 5), con sus guiones (`formas.py`, `sondas_h.py`),
sus siete diffs y las salidas de tests y sondas.

| Afirmación de diagH (y de lo que el consultor tiene apuntado) | Lo medido sobre 2e04b63 |
|---|---|
| (e2) es una línea en `_peor_del_minuto` (`broker.py:955`) | **Sí**: `broker.py` no ha cambiado desde 7a3a1ff (`git diff --stat 7a3a1ff main -- src/` toca `cableado.py`, `motor.py`, `tope_trader.py`, `pivotes_m15.py` y `cuarentena.py`, no `broker.py` ni `llenado.py` ni `primitivas_broker.py`). La línea sigue en :955 |
| (e2) «no rompe nada» | **Matiz, medido más ancho**: diagH corrió 13 ficheros (145 tests, 1 deselect). Aquí, 29 ficheros (343 tests, incluidos `test_simulacion.py` y `tests/regression/test_cuenta_7_de_agosto.py`, que leen `data/` por el `settings.local.toml` del clon): **0 rotos** (`tests_e2.txt`, exit 0). La suite entera la corre el `make check` de la fase 1 |
| (c2) = sellar en k fin − 1 + (e2) + leer el minuto de apertura con «+ 1» | **Sí** (`forma_c2.diff` de diagH; reescrito a mano en el clon, `forma_c2_main2e04b63.diff`: 4 ficheros, 15+/11−). `cableado.py:464` de diagH está hoy en `:469` (5 líneas de ed09769) |
| (c2) rompe 10 tests de main | **Sí, los mismos 10** en los 29 ficheros (no solo en los 13 de diagH): 8 por el milisegundo y 2 por la secuencia (§0.d). Los otros 333, en verde |
| (c2) enmienda ADR-0051 §5 y ADR-0057 §1 | **Sí** (ADR-0051:86 «El instante de un evento del respaldo es el CIERRE de la vela»; ADR-0057:25-27 «sellado al cierre de la vela»), y además la NOTA de §5 de ADR-0051 («sigue en el cierre de la vela», :104) y, si el consultor acepta S4 y S5, una NOTA en ADR-0068 (§2) |
| (c2) toca «unos 6 lectores» de `abierta_ms` | **Matiz**: el prototipo de diagH tocó 3 (`broker.py:933`, `cableado.py:469`, `primitivas_broker.py:279`) y nombró los que faltarían para ser neutral (S9: `broker.py:962` y `:1091`; y el instante de comisiones y criterio, `broker.py:1107`, `:1110`, `cableado.py:478`). Lista completa, §0.e |
| (d) rompe 17 y toca ADR-0053 | No se ha vuelto a medir: D3 la descarta |
| Sondas S1-S9 con main, (e2) y (c2) | **Idénticas** a las de diagH sobre este main (`diff` de `sondas_*.txt` sin la primera línea, que nombra la carpeta: vacío las tres) |
| «Todo esto solo afecta a los minutos SIN ticks» | Lectura del código, coherente con todo lo medido (el «+ 1» de (c2) movería además un llenado por TICK en el ms .999 de un minuto, `INFORME-DIAG-H.md:296`; no medido aquí) |

### 0.b Los 22: de dónde salen, y la lista otra vez

**Qué son.** RESPALDO-M1.md:351: «de las órdenes canceladas, 0 de 158 en la corrida 1 y **22 de 1002
en la 2** se cancelaron en el cierre de una M1 sin ticks (las 22, en horas perdidas)». La corrida 2
es la diaria de **RECORRIDA-CONSTRUCCION**, con el código anterior a Z (HOLDOUT-EXPOSICIONES.md:83;
el auditor, 14 y 34). **Son cancelaciones que pide el bot, no eventos del respaldo**: el motor
decide en el cierre de la M1 k menos 1 ms (`cableado.py:302`), el bróker evaluaría la vela k en su
cierre (`_fin_ms`, `llenado.py:184,240`), y la orden cancelada en ese instante no se evalúa nunca
contra la vela en que aún vivía (con ticks, sí: sus ticks ya pasaron).

**`censo_cierre.py` no está en el repo**: reconstruido desde esa descripción (cabecera del guion):
una cancelación del bot (tabla «### Ordenes», resultado `cancelada`) en un instante `:59.999`, en una
hora sin ticks por la clasificación de `censo_respaldo.donde`. Sin ningún recuento por categoría:
solo las filas.

| Salida commiteada | Filas | Días |
|---|---|---|
| `anexos/RECORRIDA-CONSTRUCCION/diaria…txt` | **22** (`censo-cierre-recorrida.txt`): la cifra de RESPALDO-M1, reproducida | los once de abajo, menos 2026-04-07 |
| `anexos/RESPALDO-M1/diaria…txt` (la que nombra el encargo) | **26** (`censo-cierre-respaldo-m1.txt`): no salen 22; gana este recuento, y las órdenes están renumeradas (el auditor, 35) | los once |

**Pero ninguna de las dos es main** (el auditor, «lo más grave»): main ha cambiado después (S-2, S-4,
la comisión a 2,50). Las salidas viejas solo sirven para ELEGIR los días; la lista que cuenta sale
del visor, día a día, con el código de main (§0.c). Los once días: 2026-01-14, 01-23, 04-03, 04-06,
04-07, 04-22, 04-23, 07-10, 07-16, 08-17 y 08-20. **Todos de material de desarrollo** (enero, abril,
julio y agosto) y `casos_reservados(repo)` da **0 casos reservados en cada uno y 0 en cada uno de los
cuatro meses** (guion de la carpeta de trabajo que solo imprime recuentos, sin claves).

### 0.c EL CENSO, evento por evento: main frente a (c2), por día

Con `prototipo_sello.py` (el visor de la CLI por caso, `motor visor --caso caso-eurusd-<día>
--simular`; la cuenta empieza ese día, como en la diaria) y `comparar_formas.py`
(`censo-main-c2.txt`). Para cada cancelación en el cierre de una M1 sin ticks, el guion comprueba
en el MERCADO del día que la M1 k no tiene ticks y le pasa la función del respaldo de main sobre esa
sola vela: «la llenaría» o «no la llena». Con el código de main hay **27** en los once días:

| Día | Sesión | Orden (main) | Colocada → cancelada (UTC) | Vela k con main | Con (c2) | ¿Cambia una operación? |
|---|---|---|---|---|---|---|
| 2026-01-14 | 07-11 | o6 | 07:55:59.999 → 07:56:59.999 | sin ticks; no la llena | igual | no |
| 2026-01-14 | 07-11 | o7 | 07:56:59.999 → 07:57:59.999 | sin ticks; no la llena | igual | no |
| 2026-01-23 | 11-15 | o28 | 11:00:59.999 → 11:01:59.999 | sin ticks; no la llena | igual | no |
| 2026-01-23 | 11-15 | **o29** (venta stop) | 11:01:59.999 → 11:03:59.999 | **sin ticks; la LLENARÍA** | **llenada en 11:03:59.999 (respaldo); posición 11-15, venta, vela de entrada 11:03, sale por stop (respaldo) a las 11:08:59.999, −1,00 R** | **SÍ: entra una operación que en main no existe** |
| 2026-04-03 | 11-15 | o16 | 09:47:59.999 → 09:48:59.999 | sin ticks; no la llena | igual | no |
| 2026-04-03 | 11-15 | o17 | 09:48:59.999 → 09:51:59.999 | sin ticks; no la llena | igual | no |
| 2026-04-06 | 11-15 | o10 | 09:57:59.999 → 10:00:59.999 | sin ticks; no la llena | igual | no |
| 2026-04-06 | 11-15 | o12 | 10:47:59.999 → 10:50:59.999 | sin ticks; no la llena | igual | no |
| 2026-04-07 | 11-15 | o28 | 10:21:59.999 → 10:22:59.999 | sin ticks; no la llena | igual | no |
| 2026-04-07 | 11-15 | o29 | 10:22:59.999 → 10:23:59.999 | sin ticks; no la llena | igual | no |
| 2026-04-07 | 11-15 | o30 | 10:23:59.999 → 10:24:59.999 | sin ticks; no la llena | igual | no |
| 2026-04-22 | 07-11 | o9 | 07:48:59.999 → 07:51:59.999 | sin ticks; no la llena | colocada un cierre antes (07:47:59.999: el llenado anterior se ve un cierre antes), cancelada igual; no la llena | no |
| 2026-04-22 | 11-15 | o13 | 09:59:59.999 → 10:00:59.999 | sin ticks; no la llena | igual | no |
| 2026-04-23 | 07-11 | o2 | 05:02:59.999 → 05:04:59.999 | sin ticks; no la llena | igual (renumerada o3) | no |
| 2026-04-23 | 07-11 | o3 | 05:04:59.999 → 05:05:59.999 | sin ticks; no la llena | igual (o4) | no |
| 2026-04-23 | 07-11 | o4 | 05:05:59.999 → 05:06:59.999 | sin ticks; no la llena | igual (o5) | no |
| 2026-04-23 | 07-11 | o5 | 05:06:59.999 → 05:07:59.999 | sin ticks; no la llena | igual (o6) | no |
| 2026-04-23 | 07-11 | o6 | 05:07:59.999 → 05:08:59.999 | sin ticks; no la llena | igual (o7) | no |
| 2026-04-23 | 07-11 | o7 | 05:08:59.999 → 05:09:59.999 | sin ticks; no la llena | igual (o8) | no |
| 2026-04-23 | 07-11 | o8 | 05:09:59.999 → 05:13:59.999 | sin ticks; no la llena | igual (o9) | no |
| 2026-04-23 | 07-11 | o9 | 05:13:59.999 → 05:15:59.999 | sin ticks; no la llena | igual (o10) | no |
| 2026-07-10 | 07-11 | **o3** (compra stop) | 05:26:59.999 → 05:27:59.999 | **sin ticks; la LLENARÍA** | **llenada en 05:27:59.999 (respaldo); posición 07-11, compra, vela de entrada 05:27, sale por stop (respaldo) a las 05:30:59.999, −1,00 R** | **SÍ: entra una operación que en main no existe** |
| 2026-07-16 | 11-15 | o13 | 10:59:59.999 → 11:00:59.999 | sin ticks; no la llena | igual | no |
| 2026-07-16 | 11-15 | o14 | 11:00:59.999 → 11:01:59.999 | sin ticks; no la llena | igual | no |
| 2026-08-17 | 11-15 | o19 | 11:19:59.999 → 11:20:59.999 | sin ticks; no la llena | igual | no |
| 2026-08-17 | 11-15 | o20 | 11:20:59.999 → 11:22:59.999 | sin ticks; no la llena | igual | no |
| 2026-08-20 | 07-11 | o13 | 07:42:59.999 → 07:44:59.999 | sin ticks; no la llena | igual | no |

**Lo demás que (c2) cambia en esos días, sin cambiar ninguna operación** (`censo-main-c2.txt`): el
instante de cada evento del respaldo, 1 ms antes (04-06, 04-07, 04-22, 04-23, 08-20); y como el motor
ve el llenado del respaldo un cierre antes (S1 y S6 de diagH), la orden siguiente se coloca un cierre
antes: en 2026-04-22 o9 (arriba), y en 2026-04-23 y 2026-08-20 **una cancelación más** en el cierre
de una M1 sin ticks (05:01:59.999 → 05:02:59.999 y 07:58:59.999 → 07:59:59.999), que su vela tampoco
llena. En los nueve días restantes, las operaciones (sesión, lado, vela de entrada, salida y R) son
idénticas a main. En 2026-01-23 y 2026-07-10 la única diferencia en operaciones es la nueva.

**La regla de D2, aplicada.** Escrita antes del censo: «si AL MENOS UNO cambia una operación […] el
camino es (c2), pero NO se implementa en esta rama esta noche: PARADA con el plan». Dos cambian una
operación (entran). **Resultado: (c2), PARADA con el plan (§2); en la fase 1, solo D1.** Ninguno de
los 27 quedó sin decidir.

### 0.d Lo de la entrada H, medido con (c2)

Sondas sintéticas de 2030 de diagH (`sondas_h.py`, copia), sobre este main en el clon:

| Lo que nombra H | main | (c2) | Lectura |
|---|---|---|---|
| Las marcas meten la vela del llenado (S1) | primera marca `(M0+2 −1ms, 1000)` | **sin marca de M0**; `(M0+2 −1ms, 1000)`: neutral gracias al «+ 1» de `broker.py:933` | (c) sin el «+ 1» sí la metía (diagH, S1) |
| `m1_entre` del break even mete la vela del llenado (S2) | `[M0+1]` | `[M0+1]`: neutral, por el «+ 1» de `primitivas_broker.py:279` | idem |
| La sesión de un llenado en la última vela de 07-11 (S3) | 11-15 | 11-15: neutral, por el «+ 1» de `cableado.py:469` | idem |
| El fin de la ventana (S4) | la última vela no se evalúa: la límite no se llena; `p` cierra a mercado a 990 | **la última vela se evalúa**: la límite se llena (y cierra a mercado a 990); `p` sale por stop a 988 | **cambia**: decisión del consultor (§2, punto 2) |
| El borde de ADR-0068 (S5) | la pendiente se cancela en W sin llenarse | **se llena en W − 1 ms**, antes de la ventana | **cambia**: idem |
| Swap y día local de un llenado en la última vela antes del corte (S9) | `abierta` = medianoche; sin swap; día 16 | **`abierta` = medianoche − 1 ms; un swap; día 15** | **cambia**: (c2) de diagH no lleva «+ 1» en `broker.py:962` ni `:1091` (§2, punto 1) |
| El motor ve un llenado del respaldo | un cierre después (el evento sellado en k fin entra en el `avanzar` del cierre siguiente) | **en el mismo cierre** (S1, S6) | es lo que mueve las colocaciones de §0.c |
| Los tests de main que rompen | — | **10** (`tests_c2.txt`) | abajo |

Los 10, con la línea de su `def` en `main` y su motivo:

| Test | Motivo |
|---|---|
| `test_llenado.py:94` `test_una_m1_con_stop_y_objetivo_a_la_vez` | `assert 1894694459999 == 1894694460000`: 1 ms |
| `test_llenado.py:149` `test_un_tramo_sin_ticks_cae_al_respaldo_y_queda_marcado` | el evento en `…519999` y no en `…520000`: 1 ms |
| `test_broker.py:222` `test_el_respaldo_m1_llena_cierra_y_marca_sin_ticks` | `(…519999, 'respaldo_m1') == (…520000, …)`: 1 ms |
| `test_broker_ordenes_stop.py:145` `test_el_respaldo_m1_llena_al_nivel_o_a_la_apertura_si_la_vela_abre_pasada` | la llenada en `…519999`: 1 ms |
| `test_broker_ordenes_stop.py:161` `test_misma_vela_la_stop_sigue_la_convencion_de_la_limite` | el `stop` 1 ms antes (la salida sigue en la vela siguiente) |
| `test_respaldo_m1_decision.py:122` `test_la_vela_del_stop_movido_que_toca_el_stop_original_sale_por_el_sin_break_even` | **por la secuencia**: `BrokerError: posicion 'p' no esta abierta`. La vela se evalúa en `avanzar(cierre)` con el stop original ANTES de que el test lo mueva (sale a 990, lo que pide ADR-0065 §4) |
| `test_respaldo_m1_decision.py:142` `test_la_vela_de_una_modificacion_se_evalua_con_la_orden_anterior` | **por la secuencia**: `BrokerError: orden 'o' no esta pendiente`: la vela llena la orden antes de `modificar` (el resultado es el que pide el test) |
| `test_respaldo_m1_decision.py:160` `test_la_vela_de_una_modificacion_no_llena_la_version_nueva` | la llenada en `…579999`: 1 ms |
| `test_respaldo_m1_decision.py:189` `test_una_pendiente_de_antes_de_una_vela_sin_ticks_se_llena_en_esa_vela` | la llenada en `…519999`: 1 ms |
| `test_respaldo_m1_decision.py:212` `test_la_salida_tras_un_llenado_del_respaldo_se_mira_desde_la_vela_siguiente` | `abierta_ms` 1 ms antes; la salida sigue en la vela siguiente |

**H decía 5 y diagH 10: no se contradicen** (el auditor, 37): son 5 de ficheros anteriores a
`trabajo/respaldo-m1` y 5 de `test_respaldo_m1_decision.py`, que el auditor del consultor no tenía.

### 0.e Los lectores de `abierta_ms` y de `_peor_del_minuto`, en este main

Grep de `abierta_ms|_peor_del_minuto` en `src/botsito/`:

| Lector | Qué hace | ¿Lo toca (c2) de diagH? |
|---|---|---|
| `broker.py:251` | el campo (`Posicion.abierta_ms`); nace en `_aplicar` LLENADA (`:875`, el instante del evento) | — |
| `broker.py:715` | `_mover`: `vigente_desde` del stop anterior | no |
| `broker.py:783`, `:785` | `_proximo_evento`: `desde` y `decidido` de la salida | no (la vela del llenado sigue fuera: `_sello_ms <= desde`) |
| `broker.py:933` | `_marcar_hasta`: el primer minuto que se marca | **sí, «+ 1»** |
| `broker.py:936`, `:943-958` | `_peor_del_minuto(lado, m, abierta_ms, hasta)`: ticks en `[abierta, hasta]` y la condición de la vela en **`:955`** | **sí, (e2)** |
| `broker.py:962` | `_swaps`: desde `abierta_ms` | **no** (S9) |
| `broker.py:1091` | `_limite_infringido`: el día local de `abierta_ms` para `posiciones_dia_max` | **no** (S9) |
| `broker.py:1107`, `:1110` | `_operacion`: las comisiones en `abierta_ms` | no |
| `broker.py:1117` | `_operacion`: las marcas con `abierta_ms <= ms <= cerrada_ms` | no |
| `broker.py:1123` | `_operacion`: la apertura | no |
| `cableado.py:468-469` | `_operaciones_del_bot`: el orden y la sesión de la posición | **sí, «+ 1» en `:469`** |
| `cableado.py:478` | el instante de la operación para el criterio (ADR-0043) | no |
| `cableado.py:684`, `:688` | el detalle del visor | no |
| `cableado.py:886` | `llenada_en`, para «### Ordenes» | no |
| `primitivas_broker.py:279` | el break even por velas (RN-014): `m1_entre(abierta_ms // 60000, instante)` | **sí, «+ 1»** |

Fuera de `src/`, solo lo nombran `scripts/embudo_77.py` (`:494`, que rehace `colocada_ms` como
`breaker_fin·60000 − 1`; `abierta_ms` en `:584`, `:648`, `:722`, `:778`, `:795`, `:797`, `:826`) y
`scripts/orden_stop_o_limite.py` (`:441`, `:453`). Las líneas que citaba la respuesta del consultor
de RESPALDO-M1 (`broker.py:888`, `:909-913`) ya no son las de las marcas: hoy son el comentario de
ADR-0065 §4 en `_aplicar` y `_cancelar_por_cierre` (el auditor, 24).

### 0.f (e2) en el prototipo, y su test

**El diff que se commiteará** (fase 1, punto 1), el mismo que se midió en el clon
(`forma_e2_main2e04b63.diff`):

```diff
         vela = self.mercado.m1(minuto)
-        if vela is None or int(vela.fin) * MS_POR_MINUTO > hasta_ms + MS_POR_MINUTO:
+        # sin ticks, la vela cuenta si EMPIEZA antes de `hasta` (le queda al menos 1 ms dentro): al
+        # avanzar a un instante redondo no se marca la vela que empieza en el (NA:H, (e2))
+        if vela is None or int(vela.inicio) * MS_POR_MINUTO >= hasta_ms:
             return None
```

- **Tests de main que rompe: ninguno** de los 343 de los 29 ficheros (`tests_e2.txt`, exit 0); la
  suite entera, en el `make check` de la fase 1.
- **Qué cambia: solo la marca de `_peor_del_minuto`.** Sondas: S5, S7 y S7b, las tres marcas de la
  vela que empieza en el instante redondo; S1-S4, S6, S8 y S9, idénticas a main (`sondas_e2.txt`). En
  los once días, órdenes y operaciones idénticas a main (`censo-main-e2.txt`). Lo que el prototipo
  no imprime son las marcas mismas ni la equity: si una marca de menos cambiara un tope en algún
  día, se vería como una operación distinta, y no la hay.
- **ADR-0053 no cambia** (el auditor, 9): su §5 (`0053:163-165`) dice que la cuenta recibe «la peor
  marca del minuto de cada posición viva»; (e2) es exactamente eso, y la marca de un minuto que aún
  no ha empezado no lo es. Ninguna NOTA.
- **El test** (`tests/unit/test_peor_del_minuto.py`, en la fase 1; hoy en la carpeta de trabajo y en
  el clon): `test_avanzar_a_un_instante_redondo_no_marca_la_vela_que_empieza_en_el` (la sonda 5) y
  `test_una_expiracion_en_un_instante_redondo_no_marca_la_vela_siguiente` (S7b) rompen en main; los
  otros dos, a media vela y en el cierre menos 1 ms, pasan en los dos lados. **Contra main** (el test
  copiado en el clon de main, `test_sonda5_main.txt`):

```
E   assert [(18946944599...4460000, 900)] == [(1894694459999, 989)]
E     Left contains one more item: (1894694460000, 900)
E   assert [(18946944000...4460000, 900)] == [(18946944599...4519999, 900)]
E     At index 0 diff: (1894694400000, 995) != (1894694459999, 995)
FAILED tests/unit/test_peor_del_minuto.py::test_avanzar_a_un_instante_redondo_no_marca_la_vela_que_empieza_en_el
FAILED tests/unit/test_peor_del_minuto.py::test_una_expiracion_en_un_instante_redondo_no_marca_la_vela_siguiente
========================= 2 failed, 2 passed in 0.41s =========================
```

  Con (e2) en el clon: `4 passed in 0.34s`.

**D1 se cumple sin PARADA**: (e2) no rompe ningún test de main medido y solo cambia la marca.

### 0.g Las líneas del cierre (preparadas sobre una copia; no aplicadas en la rama)

En el caso que dio D2, (c2). Simuladas con `simular_cierre.py` (en memoria, contra
`test_hoja_de_ruta` y `test_project_state`; `simular-cierre.txt`): `a: [] b: [] c: []`, los cuatro
tests de `test_project_state` en verde y **PROJECT_STATE en 22.794 bytes** (por debajo de 23.000).

- **H no sale HECHA: se queda reescrita.** «H. El respaldo M1 sella el evento de una vela en su
  cierre, un milisegundo después de que el motor decida (ADR-0051 §5, ADR-0057 §1), así que la vela
  k no se evalúa para la orden que el motor cancela en su cierre. Medido con el código de main, día a
  día con el visor: en 11 días de construcción, 2 de esas cancelaciones en una M1 sin ticks las
  habría llenado su vela, y con la forma (c2) (sellar en k fin - 1, con los lectores del minuto de
  apertura en «+ 1») son 2 operaciones nuevas del bot (SELLO-RESPALDO-M1.md §0.c). Rama propia con un
  ADR que enmiende esos dos ADR (borrador en SELLO-RESPALDO-M1.md §PARADA): 10 tests de main
  reescritos, los lectores de §0.e y las NOTAS que pida la decisión del consultor. La marca
  adelantada de _peor_del_minuto ya está corregida, (e2) en trabajo/sello-respaldo-m1. Va antes de
  la re-corrida que cuenta (ADR-0070 §3).» (Sin el número del ADR: un id que no existe en
  PROJECT_STATE rompe `knowledge validate`.)
- **F**: «Siguiente: H, la rama de (c2) con su ADR (SELLO-RESPALDO-M1.md, la PARADA), R y la
  re-corrida que cuenta (ADR-0070 §3), con las dos corridas que pedía R3.6 y la primera con la
  comisión medida (ADR-0090 §3);» en lugar de «Siguiente: H (fase 0: el diagnóstico de H …), R y la
  re-corrida que cuenta (ADR-0070 §3), la primera con la comisión medida (ADR-0090 §3);».
- **R3.6**: en «Qué es», «La marca de `_peor_del_minuto` ya está corregida ((e2),
  `trabajo/sello-respaldo-m1`); queda el sello, la forma (c2), que cambia operaciones del bot
  (SELLO-RESPALDO-M1.md §0.c).»; y su «Hecho cuando», **sin las dos corridas**: «el ADR está aceptado
  y un test que rompe en `main` pasa en la rama. Las dos corridas pasan a la re-corrida que cuenta,
  después de R3.7 (regla del consultor del 2026-11-07: los umbrales de R se fijan antes de ver
  ninguna corrida nueva).»
- **R3.7**: no hace falta tocarla (ya dice «antes de ver ninguna corrida nueva», HOJA:240-241).
- **R5.2**: sigue con `NA:H` (H sigue viva; el auditor, herencia 1).
- **Technical Debt**: nada nuevo.
- **La fila de ERRORES-RECURRENTES**, preparada en §3.

### 0.h El encargo frente al repo (auditor)

El subagente `auditor-encargo` (2026-11-07, sobre 13d9ad3 estadiado): **45 afirmaciones, 28
correctas, 1 incorrecta y 16 con matiz; 8 herencias**. Lo que cambia lo que se hace:

| # | Afirmación del encargo | Veredicto | Lo medido, y dónde se recoge |
|---|---|---|---|
| 8 | «los 22 eventos del respaldo M1 que se sellan en el cierre de su vela» | **INCORRECTA** | Son cancelaciones del bot en el cierre de una M1 sin ticks (RESPALDO-M1.md:351, :416-420). Y la diaria de RESPALDO-M1 tiene, aparte, exactamente 22 **eventos** del respaldo (RESPALDO-M1.md:722), que son otra cosa. §0.b; la fila de §3 lo recoge |
| 14, 34, 35 | «localizar los 22» en las salidas de RESPALDO-M1 | MATIZ | Los 22 se contaron en la diaria de RECORRIDA; la de RESPALDO-M1 da 26 y es de F38j; main ha cambiado después. La lista sale de main con el visor (§0.c) |
| 9 | «NO cambia: ADR-0053» | MATIZ | diagH proponía «a lo sumo una NOTA en 0053 §5» para (e2): medido, no hace falta (§0.f) |
| 10 | «solo días de desarrollo» | MATIZ | `--simular` calienta el sesgo H4 con el M1 entero del mes anterior (marzo, junio, julio): declarado (§0.j) |
| 20, 21 | la sonda y el prototipo del auditor del consultor (§0.l, :448, :1097) | MATIZ | §0.l es el auditor de la sesión; la sonda del consultor está descrita en :468 y el prototipo en :448-454 (era de (c)). diagH ya los reconstruyó (`sondas_h.py`: S5, S7, S7b; `formas.py`/`forma_c2.diff`). D5, §0.i |
| 26, 28, 30 | «(e2) no rompe nada», «rompe 10», «unos 6 lectores» | MATIZ | §0.a: medidos más anchos aquí (29 ficheros) y los lectores, completos en §0.e |
| 36 | «(o censo_respaldo.py, si sirve)» | MATIZ | No sirve: censa eventos del respaldo, no cancelaciones. Guion nuevo `censo_cierre.py` |
| 38 | PROJECT_STATE «por debajo de 23.000» | MATIZ | El tope del repo es 25.000; el 23.000 es la alerta del consultor. El PROJECT_STATE de la apertura medía 23.008: recortado en esta rama (Current Feature) |
| 42 | el bloque `ids-inexistentes` | MATIZ | Solo exime en su documento: este informe lleva el suyo, porque cita ADR-0091 en el borrador. Con (c2), el del encargo y el de este informe se quedan (el ADR no se crea) |
| 43 | «el plan del 2026-11-01 mandaba a H "las dos corridas del arnés"» | MATIZ | No hay ningún plan del 2026-11-01 en el repo: las dos corridas de H vienen de la respuesta del consultor del 2026-10-29 (RESPALDO-M1.md:485 = HOJA:222-223), y diagH también las pedía (§4.5, §5). La fila de §3 se escribe con la fecha que el consultor da y esta nota |
| H1 | R5.2 depende de `NA:H` | herencia | Con (c2), H sigue viva y R5.2 no cambia (§0.g) |
| H3 | el visor no conecta `--diagnostico-cuenta-diaria` | herencia | Con `--caso`, la cuenta se construye sobre un solo día: equivale a la diaria para ese día (§0.c; en 2026-01-14 el visor reproduce o6 y o7 de la diaria con sus instantes) |
| H4 | lo que diagH midió y d) no lista (S9; el motor ve el respaldo un cierre antes; la versión anterior inalcanzable; las NOTAS de 0068 y 0053) | herencia | §0.d y §2 |
| H5 | el test de (e2) cubre S7 y S7b, y además la ventana S5 | herencia | El test lleva S7 (sonda 5) y S7b; S5 es la misma condición en otro llamador (`_proxima_ventana`): no se añade un test por llamador |
| H6 | `test_las_negativas_por_la_cli` lee `knowledge/cases/criterio_fidelidad.yaml` | herencia | No está entre los 29 ficheros corridos en el clon; lo corre `make check` en la rama, como siempre |
| H7 | saber si las canceladas se habrían llenado exige el mercado de esos días | herencia | Leído por el visor, declarado (§0.j) |
| H8 | si H sale HECHA, su registro HECHA es el segundo | herencia | No sale HECHA |

Las búsquedas de «a H», «para H», «NA:H» y «R3.6» en RESPALDO-M1.md, ACTIVAR-SESION-06*.md y el final
de HISTORIA no dejan nada más para H que lo de arriba (el auditor: «su única condición, ir después de
la activación de la sesión 6, está cumplida»).

### 0.i Lo que no pude medir

- **Las cancelaciones de este tipo en los otros días de construcción.** El censo cubre los once días
  que señalan las salidas ya commiteadas; con el código de main puede haber otras en días que esas
  salidas no señalan. Encontrarlas exige el motor sobre toda la construcción, que la regla de la rama
  prohíbe (D4). No hace falta para decidir: D2 ya da (c2) con dos. Lo verá la re-corrida que cuenta.
- **La equity y los topes con (e2) y con (c2)**: el prototipo imprime órdenes y operaciones, no las
  marcas ni la equity de la cuenta. Que no cambie ninguna operación en los once días dice que ningún
  tope se disparó distinto en ellos, no que la peor equity sea la misma.
- **La sonda y el prototipo del auditor del consultor** (D5): no están en el repo ni en la carpeta de
  diagH. Lo que su descripción permite reconstruir ya lo reconstruyó diagH (la sonda: «avanzar a un
  instante redondo marca la vela siguiente» = S7 y S7b; el prototipo de (c) = `forma_c.diff`), y
  aquí se ha vuelto a medir. Lo que no se puede reconstruir, y se declara perdido: el código exacto
  de los dos y la lista exacta de los «5 tests» que el auditor rompió.
- **`censo_cierre.py` original**: perdido; el reconstruido reproduce su cifra (22) sobre la misma
  salida, pero no se puede comparar línea a línea.
- **La suite entera con (c2)**: solo los 29 ficheros que tocan el bróker; (c2) no se implementa.

### 0.j Exposiciones

Declaradas en `docs/validation/HOLDOUT-EXPOSICIONES.md` el 2026-11-07, antes de correr el prototipo:
(1) los `make check` de la rama (el M1 de marzo de siempre); (2) `censo_cierre.py` sobre las dos
diarias ya commiteadas (solo filas de cancelaciones, sin precios ni R); (3) `casos_reservados`, solo
recuentos (0); (4) el prototipo, el visor por caso en los once días dev, que lee sus M1 y sus ticks y
el M1 del mes anterior para calentar (diciembre de 2025 si existe, marzo, junio y julio), páginas
fuera del repo, y que imprime órdenes y operaciones del bot con instantes y R, sin precios; (5) el
auditor (diagH y `grep -c`). Además, en el clon `C:/cm/h`: 29 ficheros de test de main, dos de los
cuales (`test_simulacion.py` y `test_cuenta_7_de_agosto.py`) leen `data/` de construcción, como en
cada `make check`. **Ninguna partición tocada; ningún día reservado mirado; ninguna corrida del
arnés.**

### 0.k Negativas de la guardia (ninguna del clasificador)

Ninguna se rodeó: en cada una se usó la forma que propone el propio mensaje, o se dejó la medida.

1. `prototipo_sello.py` con `exec(...)` de la fuente de cada función: «el codigo carga o ejecuta
   `exec(...)`: el codigo que ejecuta no es literal». **Reescrito sin `exec`** (las funciones de cada
   forma, copias literales escritas en el guion), que es la forma que propone su mensaje («o sin
   cargarlo»).
2. `git apply --check <diff de diagH>` en el clon: «`git apply`: subcomando fuera de la lista
   cerrada». Las formas se escribieron con Edit en el clon, fuera del repo.
3. `sondas_h.py` de diagH: «cambia `sys.path` con un valor que no se calcula». La copia del repo va
   sin esa línea (su cabecera lo dice) y comprueba que `botsito` sale del clon.
4. `PYTHONPATH=. uv run python …/simular_cierre.py`: «`PYTHONPATH` no esta en la lista cerrada».
   Y `from tests.unit import …` por `python -c` con `runpy`: «no se pudo resolver el modulo». Y
   `spec_from_file_location` con la ruta por parámetro: «la ruta del fichero que carga no se
   calcula». **Las rutas, literales en la llamada**: así corre.
5. Formas de comando partidas en varias llamadas por su mensaje («antes, en el mismo comando, va
   …»: `uv run python -` delante de `state check`; `cp` delante de un `python`; dos `python`
   seguidos; `$'\r'` en un `grep`; `<(...)` en un `diff`; `| rev`).

Ninguna bloqueó algo legítimo sin forma alternativa: no hay entrada nueva de Next Action por la
guardia.

## 1. Fase 1 (el plan; los commits, en §4)

Por la PARADA condicional del encargo («si da (c2), aplica solo D1 en la fase 1 y para con el plan de
(c2)»):

1. **(e2) y su test de la sonda 5** (§0.f). En curso tras este commit.
2. ~~ADR-0091 y el test del límite declarado~~: **no se hace** (D2 dio (c2)). El bloque
   `ids-inexistentes` del encargo se queda, y el de este informe también.
3. El informe con las líneas del cierre preparadas (§0.g) y el revisor.

## 2. PARADA · el plan de (c2)

### Borrador de ADR-0091 (no se crea en esta rama)

> **ADR-0091 · El evento del respaldo M1 se sella un milisegundo antes del cierre de su vela.**
> Estado propuesto: ACTIVE. Enmienda ADR-0051 §5 (y su NOTA del 2026-10-29) y ADR-0057 §1.
>
> **Problema.** El respaldo sella el evento de la vela k en su cierre (k fin), y el motor decide en
> k fin − 1 ms (ADR-0053 §5). Una orden que el motor cancela, o una posición que cierra a mercado, en
> ese cierre no se evalúa nunca contra la vela k, en la que vivía. Medido con el código de main
> (SELLO-RESPALDO-M1.md §0.c): en 11 días de construcción, 27 cancelaciones en el cierre de una M1
> sin ticks, de las que la vela k habría llenado 2; con este ADR son 2 operaciones del bot que hoy no
> existen.
>
> **Decisión.** (1) En las tres funciones del respaldo (`primer_llenado_limite`,
> `primer_llenado_stop`, `primera_salida`), el instante del evento y el borde de aceptación de la
> vela son `k fin − 1 ms`, el último milisegundo de la vela: lo evalúa el `avanzar` del cierre en
> que decide el motor, antes de que decida. `Mercado.cotizacion`, que también usa `_fin_ms`, no
> cambia. (2) Los lectores del minuto de apertura leen `(abierta_ms + 1) // 60000` [según el punto 1
> de la PARADA: los tres de diagH, `broker.py:933`, `cableado.py:469` y `primitivas_broker.py:279`;
> y `broker.py:962` y `:1091` si se elige la neutralidad completa], para que la vela del llenado
> siga fuera de lo que viene después. (3) La salida tras un llenado del respaldo se sigue mirando
> desde la vela siguiente (ADR-0051 §3 y su NOTA). (4) La versión anterior de un objeto (NOTA de
> §5) deja de alcanzarse desde el motor, que decide en el cierre; se queda para quien decida a media
> vela [punto 3]. (5) [Punto 2: el fin del día y el borde de ADR-0068.]
>
> **Alcance.** Solo los minutos SIN ticks: el bot en vivo opera con ticks (ADR-0051 §8), y en
> construcción quedan las horas perdidas. Tests: los 10 de §0.d, reescritos (8 por el milisegundo; 2
> por la secuencia, punto 4).

### Lo que necesito que decidas

0. **Abrir la rama de (c2).** Opciones: (a) rama propia de H con ADR-0091, ahora, antes de R; (b)
   después de R, antes de la re-corrida que cuenta. Recomiendo (a): H va antes de la re-corrida
   (PROJECT_STATE, H) y R no depende de ella, así que el orden H → R se conserva y R no se queda
   esperando nada. Coste de (b): ninguno técnico; la re-corrida espera a las dos.
1. **Los lectores del minuto de apertura** (§0.d S9, §0.e). Opciones: (a) neutralidad completa: «+ 1»
   en los tres de diagH y además en los swaps (`broker.py:962`) y el día local (`:1091`), y el
   instante de comisiones y criterio (`broker.py:1107`, `:1110`, `cableado.py:478`) se queda en el
   sellado, que está dentro de la vela del llenado; (b) solo los tres de diagH, y el swap y el día de
   un llenado en la última vela antes del corte pasan a ser los de esa vela (S9). Recomiendo (a): lo
   único que el ADR pretende cambiar es qué vela se evalúa, no a qué día pertenece un llenado. Coste
   de (a): dos líneas más y dos tests (S9 en los dos lados).
2. **El fin del día y el borde de ADR-0068** (S4, S5). Opciones: (a) aceptarlo: la última vela del
   día se evalúa y un llenado en la vela que acaba en W ocurre antes de la ventana, con una NOTA en
   ADR-0068; (b) excluir esas dos velas a propósito. Recomiendo (a): las dos velas transcurren enteras
   antes de su borde y hoy se descartan solo por el sello (como diagH). Coste de (b): dos excepciones
   en el código y sus tests.
3. **La versión anterior** (`Orden.anterior`, `Posicion.stop_anterior`). Opciones: (a) se queda, con
   la NOTA diciendo que desde el motor ya no se alcanza; (b) se retira en la misma rama. Recomiendo
   (a): retirarla es otra rama, y quien decida a media vela la necesita. Coste de (b): más diff.
4. **Los dos tests que rompen por la secuencia** (`test_respaldo_m1_decision.py:122` y `:142`).
   Opciones: (a) reescribirlos para que muevan o modifiquen A MEDIA VELA, donde la versión anterior
   sigue alcanzándose, y añadir uno en el cierre que fije lo nuevo (la vela se evalúa antes de mover
   o modificar); (b) solo cambiar su secuencia al cierre. Recomiendo (a): conserva lo que prueban.
5. **El universo del censo** (§0.i). Opciones: (a) basta con los once días: D2 ya está decidida, y la
   re-corrida que cuenta verá el resto; (b) autorizar en la rama de (c2) el visor por caso sobre los
   76 días, sin agregar nada. Recomiendo (a): (b) es, en la práctica, la corrida que la regla de esta
   rama prohíbe, día a día.

## 3. La fila de ERRORES-RECURRENTES (preparada para el cierre)

| `trabajo/sello-respaldo-m1` | (§0.h, §0.k) | (1) **(importa, del consultor)** el plan del 2026-11-01 mandaba a H "las dos corridas del arnés", y R3.7 pide fijar los umbrales de R antes de ver ninguna corrida nueva. Lección: antes de mandar una corrida, mirar si hay un umbral pendiente de pre-registrar. (Nota del auditor: en el repo, esas dos corridas vienen de la respuesta del 2026-10-29, RESPALDO-M1.md:485; no hay un plan del 2026-11-01.) (2) **(Del consultor)** El encargo llamó «eventos del respaldo» a 22 cancelaciones del bot, y mandó sacarlos de una salida (la diaria de RESPALDO-M1) que no es la que los contó y que tiene, aparte, 22 eventos del respaldo de verdad. Lección: una cifra heredada se cita con QUÉ cuenta y SOBRE QUÉ salida, y una lista que va a decidir algo se saca del código vigente, no de una salida vieja. Señal: el mismo número en dos sitios con nombres distintos. (3) **Una lista vieja solo elige días**: la de RESPALDO-M1 daba 26, y main da 27 en esos días, con ids renumerados; el censo se hizo con el visor sobre main. (4) **La guardia y los prototipos en memoria**: `exec` de una fuente, `git apply`, `sys.path` calculado, `PYTHONPATH` y `spec_from_file_location` con la ruta por parámetro se niegan; las formas que pasan son funciones literales escritas en el guion, Edit en el clon y rutas literales en la llamada. Señal: un prototipo que parchea por texto. |

## 4. Los commits de la rama

| Commit | Qué | `make check` |
|---|---|---|
| 13d9ad3 | apertura: encargo, contrato, Archivo 59 | sello `833d532f…`, 3237 passed |
| (este) | fase 0: este informe, los anexos, la fila de exposiciones y el recorte de Current Feature | — |

## Estado

EN CURSO: fase 0 entregada; D2 dio (c2): PARADA con el plan (§2). La fase 1 sigue solo con D1,
(e2) y su test, sin esperar (PARADA condicional del encargo).
