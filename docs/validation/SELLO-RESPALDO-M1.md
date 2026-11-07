# SELLO-RESPALDO-M1 · la marca de _peor_del_minuto y las cancelaciones en el cierre de una M1 sin ticks

Rama `trabajo/sello-respaldo-m1`, abierta el 2026-11-07 desde `main` (2e04b63, commit de estado
sobre el merge 8f43d38 del tag `stable/F38p-demo-ejecuciones-2-3`). Encargo:
`docs/encargos/trabajo-sello-respaldo-m1.md`. Tramo «R3 · Una corrida del arnés sobre toda la
construcción» (R3.6 de la hoja de ruta; H de la Next Action). Rama de noche, con las decisiones del
consultor por adelantado (D1-D5) y PARADA condicional. **Tras la PARADA, la respuesta del consultor
del 2026-11-07 (§7) manda implementar (c2) en esta rama, con ADR-0091**: lo de §1 y §2 que dice que
el ADR no se crea aquí queda sin efecto. El bloque `ids-inexistentes` que declaraba ADR-0091 salió en
el commit que lo crea.

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
| (c2) enmienda ADR-0051 §5 y ADR-0057 §1 | **Sí** (ADR-0051:86 «El instante de un evento del respaldo es el CIERRE de la vela»; ADR-0057:25-27 «sellado al cierre de la vela»), y además la NOTA de §5 de ADR-0051 («sigue en el cierre de la vela», :102-103) y, si el consultor acepta S4 y S5, una NOTA en ADR-0068 (§2) |
| (c2) toca «unos 6 lectores» de `abierta_ms` | **Matiz**: el prototipo de diagH tocó 3 (`broker.py:933`, `cableado.py:469`, `primitivas_broker.py:279`) y nombró los que faltarían para ser neutral (S9: `broker.py:962` y `:1091`; y el instante de comisiones y criterio, `broker.py:1107`, `:1110`, `cableado.py:478`). Lista completa, §0.e |
| (d) rompe 17 y toca ADR-0053 | No se ha vuelto a medir: D3 la descarta |
| Sondas S1-S9 con main, (e2) y (c2) | **Idénticas** a las de diagH sobre este main (`diff` de `sondas_*.txt` sin la primera línea, que nombra la carpeta: vacío las tres) |
| Con (c)/(c2), en ADR-0083 D2, «un llenado o un rechazo del respaldo gasta o libera el punto un cierre antes» (`INFORME-DIAG-H.md:305`) | **Sin un test propio aquí** (revisor, b3), pero es el mismo mecanismo que §0.c sí mide: el motor ve el llenado del respaldo un cierre antes, y por eso coloca la orden siguiente un cierre antes (2026-04-22, 04-23, 08-20). `test_punto_usado.py` pasa con (c2) (está entre los 29 ficheros). Va al borrador del ADR (§2) |
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

Grep de `abierta_ms|_peor_del_minuto` en `src/botsito/` (las líneas son las de **main**; en la rama,
dacd533 añade dos líneas de comentario en `broker.py:955-956` y todo lo de debajo baja dos: la
condición de (e2) está en `:957`, y `:962`, `:1091`, `:1107`, `:1110`, `:1117` y `:1123` pasan a
`:964`, `:1093`, `:1109`, `:1112`, `:1119` y `:1125`; revisor, b4. La rama de (c2) parte de main
con (e2) dentro y tiene que volver a localizarlas, como pide la lección de RESPALDO-M1.md:494):

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

**Lo que el primer grep no buscaba** (revisor, b1; el encargo pedía también «el minuto del evento»).
Líneas de la rama:

| Lector | Qué hace | Con (c2) |
|---|---|---|
| `broker.py:314` (`_de_la_version_anterior`) | compara `evento.minuto` (el minuto de la vela, no el instante) con el del cambio | no cambia (el minuto de la vela es el mismo) |
| `broker.py:917` y los lectores de `cerrada_ms`: `:1110` (la comisión del cierre), `:1114` (los swaps hasta el cierre), `:1119` (las marcas dentro de la operación), `:1126` (el cierre), `cableado.py:685` (el visor) | (c2) adelanta 1 ms también la SALIDA por stop u objetivo del respaldo (sondas: «cerrada en M0+1 −1ms») | 1 ms antes; ninguno lee el minuto, salvo `:1114` con un swap justo en el corte (S9, el mismo caso) |
| `broker.py:940` → `p.ultimo_precio` → `flotante()` (`:1057-1070`) → `margen_libre()` (`:1034-1039`, ADR-0081) | la marca de `_peor_del_minuto` mueve el flotante y el margen libre | lo cambian (e2) y (c2): ver §0.f |
| `cableado.py:454-455` | la última marca va a `cuenta.marcar` (la peor equity, los topes) | idem |

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
  día, se vería como una operación distinta, y no la hay. **La marca no es solo la marca** (revisor,
  b2): `_peor_del_minuto` escribe `p.ultimo_precio` (`broker.py:940`), que entra en el flotante
  (`:1065`) y por él en el margen libre de ADR-0081 (`:1039`), y la última marca va a
  `cuenta.marcar` (`cableado.py:455`). Así que (e2) puede cambiar también un rechazo por margen o un
  tope en un instante redondo; en los once días no cambia ninguna orden (ningún rechazo distinto) ni
  ninguna operación, y en la suite entera no rompe nada (3241 passed). Lo que cambia es siempre a
  favor de no usar un precio de un minuto que aún no había empezado.
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

**Reescrito el 2026-11-07 tras la respuesta del consultor (punto 10)**: la versión de la PARADA
(H reescrita, F con «la rama de (c2)», R3.6 sin HECHA) queda sin efecto y está en el historial
(460595f). Simuladas con `simular_cierre.py` (en memoria, contra `test_hoja_de_ruta` y
`test_project_state`; `simular-cierre.txt`): `a: [] b: [] c: []`, los cuatro tests de
`test_project_state` en verde, **PROJECT_STATE en 21.860 bytes** con las líneas del cierre y
**21.986** con un Current Feature del cierre con la forma del de `main` (por debajo de 23.000).

- **H sale HECHA**, de PROJECT_STATE a HISTORIA, con su registro (el segundo de la letra H; el
  primero, RN-007, del 2026-10-26, y este lleva fecha, DECISIONES-DE-PROCESO.md:29):
  `# Next Action HECHA · H · el sello del respaldo M1 · sale de PROJECT_STATE.md en
  trabajo/sello-respaldo-m1 (2026-11-07)`, con el texto literal de H y «HECHA en
  `trabajo/sello-respaldo-m1` (docs/validation/SELLO-RESPALDO-M1.md): ADR-0091 sella el evento del
  respaldo M1 en el último milisegundo de su vela (enmienda ADR-0051 §5, ADR-0057 §1, ADR-0068 §2 y
  ADR-0083 D2), con los lectores del minuto de apertura neutros, y (e2) corrige la marca de
  `_peor_del_minuto`. En once días de desarrollo, 27 cancelaciones en el cierre de una M1 sin
  ticks, 2 que su vela llenaba: 2 operaciones nuevas del bot, verificadas con el visor por caso.
  Las dos corridas que pedía R3.6 pasan a la re-corrida que cuenta, después de R3.7.»
- **F**: «Siguiente: R y después la re-corrida que cuenta (ADR-0070 §3), la primera con la comisión
  medida (ADR-0090 §3) y con el sello del respaldo de ADR-0091;» en lugar de «Siguiente: H (fase 0:
  el diagnóstico de H …), R y la re-corrida que cuenta (ADR-0070 §3), la primera con la comisión
  medida (ADR-0090 §3);».
- **R3.6**: `Refs` sin `NA:H` (`ID:ADR-0091 · ID:ADR-0051 · ID:ADR-0057`); «Hecho cuando: el ADR
  está aceptado, los tests que rompen en `main` pasan en la rama y los once días del censo,
  verificados con el visor por caso, dan lo que dio el prototipo. Las dos corridas que pedía pasan a
  R3.7 y a la re-corrida que cuenta (ADR-0070 §3).»; y «Estado: HECHA (`trabajo/sello-respaldo-m1`;
  SELLO-RESPALDO-M1.md): ADR-0091 sella el evento del respaldo en el último milisegundo de su vela,
  con los lectores del minuto de apertura neutros, y (e2) corrige la marca de `_peor_del_minuto`; en
  once días de desarrollo, 2 operaciones nuevas del bot y las demás idénticas.»
- **R3.7**: al final de «Qué es», «Después, la re-corrida que cuenta (ADR-0070 §3) repite las dos
  corridas que pedía R3.6, ya con el sello de ADR-0091.» (su «Hecho cuando» no cambia: los umbrales
  se pre-registran antes de ver ninguna corrida nueva).
- **R5.2**: sin `NA:H` («…rama de medida (ADR-0070 §6); y NA:R, el método (R3.7). El sello del
  respaldo M1 (R3.6) está HECHO (ADR-0091).»).
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
| 42 | el bloque `ids-inexistentes` | MATIZ | Solo exime en su documento: este informe lleva el suyo, porque cita ADR-0091 en el borrador. Con (c2), el del encargo y el de este informe se quedan (el ADR no se crea). **Sin efecto desde la fase 2 (§7)**: el ADR se creó en 3252548 y los dos bloques salieron en ese commit |
| 43 | «el plan del 2026-11-01 mandaba a H "las dos corridas del arnés"» | MATIZ | No hay ningún plan del 2026-11-01 en el repo: las dos corridas de H vienen de la respuesta del consultor del 2026-10-29 (RESPALDO-M1.md:485 = HOJA:222-223), y diagH también las pedía (§4.5, §5). La fila de §3 se escribe con la fecha que el consultor da y esta nota |
| H1 | R5.2 depende de `NA:H` | herencia | Con (c2), H sigue viva y R5.2 no cambia (§0.g). **Sin efecto desde la fase 2 (§7)**: H sale HECHA y R5.2 pierde `NA:H` (§0.g reescrito) |
| H3 | el visor no conecta `--diagnostico-cuenta-diaria` | herencia | Con `--caso`, la cuenta se construye sobre un solo día: equivale a la diaria para ese día (§0.c; en 2026-01-14 el visor reproduce o6 y o7 de la diaria con sus instantes) |
| H4 | lo que diagH midió y d) no lista (S9; el motor ve el respaldo un cierre antes; la versión anterior inalcanzable; las NOTAS de 0068 y 0053) | herencia | §0.d y §2 |
| H5 | el test de (e2) cubre S7 y S7b, y además la ventana S5 | herencia | El test lleva S7 (sonda 5) y S7b; S5 es la misma condición en otro llamador (`_proxima_ventana`): no se añade un test por llamador |
| H6 | `test_las_negativas_por_la_cli` lee `knowledge/cases/criterio_fidelidad.yaml` | herencia | No está entre los 29 ficheros corridos en el clon; lo corre `make check` en la rama, como siempre |
| H7 | saber si las canceladas se habrían llenado exige el mercado de esos días | herencia | Leído por el visor, declarado (§0.j) |
| H8 | si H sale HECHA, su registro HECHA es el segundo | herencia | No sale HECHA. **Sin efecto desde la fase 2 (§7)**: sale HECHA, con el segundo registro de la letra, con fecha (§0.g) |

Las búsquedas de «a H», «para H», «NA:H» y «R3.6» en RESPALDO-M1.md, ACTIVAR-SESION-06*.md y el final
de HISTORIA no dejan nada más para H que lo de arriba (el auditor: «su única condición, ir después de
la activación de la sesión 6, está cumplida»).

### 0.i Lo que no pude medir

- **Las cancelaciones de este tipo en los otros días de construcción.** El censo cubre los once días
  que señalan las salidas ya commiteadas; con el código de main puede haber otras en días que esas
  salidas no señalan. Encontrarlas exige el motor sobre toda la construcción, que la regla de la rama
  prohíbe (D4). No hace falta para decidir: D2 ya da (c2) con dos. Lo verá la re-corrida que cuenta.
- **La equity, los topes y el margen libre con (e2) y con (c2)**: el prototipo imprime órdenes y operaciones, no las
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
  **Sin efecto desde la fase 2 (§7)**: (c2) se implementó en 7eda14d y la suite entera pasa (3249).

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

1. **(e2) y su test de la sonda 5** (§0.f). Hecho: dacd533, suite entera en verde (3241 passed).
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
> vela [punto 3]. (5) [Punto 2: el fin del día y el borde de ADR-0068.] (6) El motor ve un evento
> del respaldo en el MISMO cierre de su vela, no en el siguiente: lo que se decide a partir de él
> (la orden siguiente; el punto que gasta o libera un llenado o un rechazo, ADR-0083 D2) llega un
> cierre antes (§0.c; diagH:305). (7) Las salidas del respaldo también se sellan 1 ms antes, y con
> ellas los lectores de `cerrada_ms` (§0.e, segunda tabla).
>
> **Alcance.** Solo los minutos SIN ticks: el bot en vivo opera con ticks (ADR-0051 §8), y en
> construcción quedan las horas perdidas. Tests: los 10 de §0.d, reescritos (8 por el milisegundo; 2
> por la secuencia, punto 4). Las líneas citadas son las de main 2e04b63; con (e2) dentro, las de
> `broker.py` por debajo de `:955` bajan dos (§0.e).

## Lo que necesito que decidas

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

Cuatro columnas, como la tabla de destino (`ERRORES-RECURRENTES.md:50`; revisor, b8). **Reescrita el
2026-11-07 con el punto 11 de la respuesta del consultor**: la lección (2) de la versión anterior
pasa a la columna del consultor, la (1) se corrige (no hubo un «plan del 2026-11-01») y entra el
error de la regla D2. La columna del revisor resume sus dos pasadas (§6 y §8); el cierre la
completa si el consultor encuentra algo después.

| `trabajo/sello-respaldo-m1` | Dos pasadas, opus. La primera, sobre dacd533 con los cinco alcances del encargo (§6; lo hecho, §6.1): reglas 0 bloquea, 1 importa, 1 menor; encargo 0 bloquea, 5 importa, 3 menor; todos arreglados: a1 (el clon sin declarar en la fila de exposiciones), b1 (los lectores de `cerrada_ms`, del minuto del evento y del resultado de `_peor_del_minuto`), b2 (la marca mueve también el margen libre), b3 (ADR-0083 D2 sin contrastar), b4 (las líneas de main frente a las de la rama), b5 (la regresión sin la lista de ficheros) y los cuatro menores. La segunda, tras la fase 2, con los alcances de la respuesta (§8) | (1) **(importa, del consultor)** la respuesta del 2026-10-29 (RESPALDO-M1.md:485) mandaba a H «las dos corridas del arnés», y R3.7 pide fijar los umbrales de R antes de ver ninguna corrida nueva. Lección: antes de mandar una corrida, mirar si hay un umbral pendiente de pre-registrar. (2) **(importa, del consultor)** el encargo llamó «eventos del respaldo» a 22 cancelaciones del bot y las mandó sacar de la salida equivocada (la diaria de RESPALDO-M1, que no es la que las contó y que tiene, aparte, 22 eventos del respaldo de verdad). Lección: una cifra heredada se cita con QUÉ cuenta y SOBRE QUÉ salida, y una lista que va a decidir algo se saca del código vigente, no de una salida vieja. Señal: el mismo número en dos sitios con nombres distintos. (3) **(menor, del consultor)** el encargo citó «el plan del 2026-11-01» cuando las dos corridas de R3.6 vienen de la respuesta del 2026-10-29: corregido en (1). (4) **(menor, del consultor)** la regla D2 prohibía implementar (c2) en la rama que ya era la de H, y costó una PARADA más. Lección: la regla de una PARADA condicional decide el camino, no la rama en la que se hace | (5) **Una lista vieja solo elige días**: la de RESPALDO-M1 daba 26, y main da 27 en esos días, con ids renumerados; el censo se hizo con el visor sobre main. (6) **La guardia y los prototipos en memoria**: `exec` de una fuente, `git apply`, `sys.path` calculado, `PYTHONPATH` y `spec_from_file_location` con la ruta por parámetro se niegan; las formas que pasan son funciones literales escritas en el guion, Edit en el clon y rutas literales en la llamada. Señal: un prototipo que parchea por texto. (7) **Un test que importa `tests.unit` solo corre en un clon si es idéntico al del repo** (la guardia lo resuelve contra el repo): en el clon de la rama, con el fichero aún sin copiar al repo, se negó; copiado, corrió en el de main. (8) **Un test de respaldo que copia uno de ticks puede no medir lo mismo**: sin ticks, la stop se llena al nivel salvo hueco, y el rechazo al llenar de D3b necesitó una vela que abriera ya pasada |

## 4. Los commits de la rama

| Commit | Qué | `make check` |
|---|---|---|
| 13d9ad3 | apertura: encargo, contrato, Archivo 59 | sello `833d532f…`, 3237 passed |
| 460595f | fase 0: este informe, los anexos, la fila de exposiciones y el recorte de Current Feature | sello `9eadefec…`, 3237 passed |
| dacd533 | fase 1, punto 1: (e2) en `broker.py:955` (el diff de §0.f, idéntico al medido en el clon: `diff` de sus líneas `+`/`-`, vacío) y `tests/unit/test_peor_del_minuto.py` (4 tests; 2 rompen en main, salida en §0.f); «Tests Currently Passing» de 1861 a 1865 | sello `900b664f…`, **3241 passed** (la suite entera: (e2) no rompe ningún test de main) |
| (este) | fase 1, punto 3: el encargo punto por punto, la regresión contra main, el informe del revisor y lo hecho con sus hallazgos (y su fila en HOLDOUT-EXPOSICIONES) | el del último commit (el mensaje de entrega lo da) |

### 4.1 Regresión contra main (skill comparar-con-main)

- **Clon**: `git worktree add --detach C:/cm/h main` (2e04b63), con `config/settings.local.toml`
  (`[entorno] nombre = "backtest"`; `[rutas]` `corpus`, `knowledge` y `data` = el `data/` real, ruta
  absoluta). Ningún test de los corridos escribe en `data/` (grep de `write_text|mkdir|to_csv` en los
  dos que lo leen: nada). Un solo clon (no dos): lo que se compara es main con cada forma escrita a
  mano en él, y el test de la rama copiado en él; la rama la mide su propio `make check`.
- **Universo**: 29 ficheros de test (los que importan el bróker, el llenado, el cableado, las
  primitivas del bróker o la simulación, más `test_instante_llenado.py`), 343 tests. **El comando**,
  tal cual, en `C:/cm/h` (revisor, b5), con `> C:/cm/tests_<forma>.txt 2>&1`:

      uv run pytest -q -p no:cacheprovider -rf --tb=line tests/regression/test_cuenta_7_de_agosto.py tests/unit/test_be_al_tick.py tests/unit/test_broker.py tests/unit/test_broker_ordenes_stop.py tests/unit/test_cableado.py tests/unit/test_caja_hasta_el_llenado.py tests/unit/test_cierres_de_mercado.py tests/unit/test_dos_relojes.py tests/unit/test_escenarios_por_sesion.py tests/unit/test_freno_peticiones.py tests/unit/test_llenado.py tests/unit/test_margen_lote.py tests/unit/test_orden_stop_pivote.py tests/unit/test_peticiones.py tests/unit/test_preparar_a21.py tests/unit/test_preparar_a44.py tests/unit/test_punto_usado.py tests/unit/test_racha_perdidas.py tests/unit/test_reinicio_tope_trader.py tests/unit/test_renovar_cierres.py tests/unit/test_respaldo_m1_decision.py tests/unit/test_rn020_retira_pendiente.py tests/unit/test_rn035_ventana_fin.py tests/unit/test_selector_orden_stop.py tests/unit/test_sesiones_rejilla_h4.py tests/unit/test_simulacion.py tests/unit/test_ultimo_minuto.py tests/unit/test_vida_de_la_orden.py tests/unit/test_instante_llenado.py

  La línea base (main intacto) se corrió igual, sin `-rf --tb=line` y sin fichero: 343 puntos, exit
  0. `tests_e2.txt` no trae la línea de resumen (con `-q` y sin fallos, la salida se cortó en los
  puntos: 4 × 72 + 55 = 343); lo que lo dice es el exit 0 y, mejor, el `make check` de dacd533, que
  corre la suite entera (3241 passed). **Sin tabla de hashes** (desviación de la skill, declarada):
  no hay ficheros de salida que comparar entre dos lados, sino resultados de tests y sondas, y las
  sondas se compararon con `diff` contra las de diagH (§0.a).
- **Resultados** (exit de pytest): main intacto, 0; (c2), 1 (10 failed, `tests_c2.txt`); (e2), 0
  (`tests_e2.txt`); el test de la rama con main, 1 (2 failed, 2 passed, `test_sonda5_main.txt`); con
  (e2), 0 (4 passed). Sondas S1-S9: `sondas_{main,e2,c2}.txt`, iguales a las de diagH (§0.a).
- **Lo que difiere a propósito**, y nada más: con (e2), las marcas de S5, S7 y S7b; con (c2), lo de
  §0.d.
- **El repo y origin, antes y después**: `git status --short` (antes, la fila de exposiciones y los
  anexos sin estadiar; después, los mismos ficheros commiteados), `git branch --list` = `main` y la
  rama, 150 tags, `git ls-remote --heads origin` = solo `main`, los dos momentos. El clon, retirado
  con `git worktree remove C:/cm/h` (sin `--force`, tras borrar el test copiado y el
  `settings.local.toml`); `git worktree list` = solo el repo.

## 5. El encargo, punto por punto

| # | Lo que pide | Estado | Dónde |
|---|---|---|---|
| 1 | Comprobar con git la base (main = docs(state) del cierre, el tag en su merge, la CI de main en verde con un `gh run view` suelto, ninguna otra rama); si falla, PARAR | Hecho | «Base comprobada al abrir» |
| 2 | Abrir con `abrir-rama`: contrato con el tramo entre comillas, riesgo alto, artefacto SELLO-RESPALDO-M1.md | Hecho | 13d9ad3; `contrato.yaml` |
| 3 | El recorrido lo mandan fase-cero, comparar-con-main y entregar-rama; si chocan, ganan ellas | Hecho, sin choque | fase-cero: §0 y §2 con «Lo que necesito que decidas»; comparar-con-main: el clon `C:/cm/h` (§0.d, §0.f); entregar-rama: §6 |
| 4 | grep de «0091» en docs/ y en Technical Debt antes de usar el número | Hecho (el auditor, 6): solo en el encargo; los demás «0091» de docs/ son ids `ev-v15-000913-…` y precios. ADR-0091 no se crea (D2 dio (c2)); este informe lo cita en el borrador con su bloque `ids-inexistentes`. **Sin efecto desde la fase 2 (§7)**: se creó en 3252548 | §0.h; cabecera |
| 5 | Objetivo: decidir y aplicar (e2) y qué se hace con los 22 | Hecho | (e2): fase 1, punto 1; los 22: D2 → (c2), PARADA (§2) |
| 6 | NO cambia: la estrategia, strategy_spec, parametros, el perfil, ADR-0053, nada de knowledge/ | Cumplido | `git diff main --stat`: `src/botsito/engine/broker.py`, el test nuevo y documentos; ADR-0053 sin NOTA (§0.f) |
| 7 | Solo días de desarrollo, comprobados con `casos_reservados(repo)` y declarados el mismo día | Hecho | §0.b (0 por día y por mes); HOLDOUT-EXPOSICIONES.md, fila del 2026-11-07 |
| 8 | REGLA: ninguna corrida del arnés ni cifra agregada nueva; visor por caso (`--caso`, `--simular`), nunca `--todos` ni `--meses`; leer las salidas commiteadas de RESPALDO-M1 vale | Cumplido | §0.c (once llamadas al visor por forma, una por día); ningún recuento por categoría ni sobre un mes (`censo_cierre.py` solo da filas) |
| 9 | Las dos corridas del «Hecho cuando» de R3.6, a la re-corrida que cuenta: línea preparada | Hecho | §0.g (R3.6) |
| 10 | Herencia: la entrada H entera (marcas y m1_entre, sesión 07-11, fin de ventana, borde de ADR-0068, tests por el ms) | Hecho | §0.d |
| 11 | Herencia: R3.6 (RESPALDO-M1.md §0.a y §0.l) | Hecho | §0.a, §0.b; §0.g |
| 12 | Herencia: punto 27 y b2: `_peor_del_minuto` con su sonda 5 y la del auditor del consultor | Hecho, con lo perdido declarado | la sonda 5 es el test (§0.f); la del auditor, reconstruida por diagH (S7, S7b) y repetida aquí; el código original, perdido (§0.i) |
| 13 | Herencia: `censo_cierre.py` no está en el repo | Hecho: reconstruido y comprobado (22 sobre la misma salida) | §0.b |
| 14 | Herencia: la lección de :494 (grep de TODOS los lectores) y relocalizar `broker.py:888`, `:909-913` | Hecho | §0.e |
| 15 | Herencia: diagH, en solo lectura; si no aparece, seguir sin él; sus afirmaciones verificadas, no copiadas | Hecho: apareció; cada afirmación, contrastada | §0.a |
| 16 | Herencia: «a H», «para H», «NA:H», «R3.6» en RESPALDO-M1.md, ACTIVAR-SESION-06*.md y el final de HISTORIA | Hecho (el auditor) | §0.h, último párrafo |
| 17 | FASE 0 sin commitear código; el prototipo en memoria en un guion de los anexos, que parchea en tiempo de ejecución y llama al visor por caso; si la guardia lo niega, PARADA | Hecho, con una negativa: el `exec` se negó y el guion se reescribió con funciones literales, la forma que propone la guardia (no es rodearla: se declara) | §0.k, 1 |
| 18 | a) diagH contrastado | Hecho | §0.a |
| 19 | b) los 22: origen y lista de nuevo (día, caso, sesión, orden, qué hizo la vela k), con un guion nuevo; si no salen 22, gana el recuento; días de desarrollo | Hecho: 22 / 26 / 27 (main) | §0.b, §0.c |
| 20 | c) el censo evento por evento, main frente a (c2), por día | Hecho | §0.c |
| 21 | d) H medido con (c2) y los tests de main que rompe | Hecho: 10 | §0.d |
| 22 | e) los lectores con fichero:línea | Hecho | §0.e |
| 23 | f) (e2): el diff, los tests que rompe y la sonda 5 como test que rompe en main y pasa con (e2) | Hecho | §0.f |
| 24 | g) las líneas del cierre sobre una copia, con test_hoja_de_ruta y test_project_state y la previsión de bytes < 23.000 | Hecho: 22.794 bytes en la primera entrega; tras la fase 2, 21.860 (21.986 con el Current Feature del cierre) | §0.g; `simular-cierre.txt` |
| 25 | D1: (e2) pase lo que pase; PARADA solo si rompe un test de main o cambia algo más que la marca | Hecho, sin PARADA | §0.f; fase 1, punto 1 |
| 26 | D2: la regla de los 22 | Aplicada: 2 cambian una operación → (c2) → PARADA con el plan, sin implementar | §0.c; §2 |
| 27 | D3: (d) descartada | Cumplido: no se midió ni se toca | §0.a |
| 28 | D4: nada de corridas agregadas; si faltara una, PARADA | Cumplido: no hizo falta ninguna (§0.i dice lo que solo una corrida vería) | §0.i |
| 29 | D5: la sonda y el prototipo del consultor reconstruidos desde su descripción; lo que no, perdido | Hecho | §0.i |
| 30 | PARADA condicional: fase 0 commiteada; con (c2), solo D1 en la fase 1 y PARADA con el plan | Hecho | 460595f; fase 1, punto 1; §2 |
| 31 | FASE 1: un commit por punto, con estadiar, state check, make check y su log; antes ruff format, ruff check y mypy | Hecho | §4 |
| 32 | 1) (e2) y su test | Hecho | §4 |
| 33 | 2) ADR-0091 y el test del límite (solo si D2 da límite) | No aplica: D2 dio (c2) | §1 |
| 34 | 3) el informe con las líneas del cierre | Hecho | §0.g, este informe |
| 35 | Negativas de guardia o clasificador: PARADA con el comando exacto para eso y seguir | Ninguna bloqueó algo sin forma alternativa; todas, con su forma | §0.k |
| 36 | TESTS QUE ROMPEN A PROPÓSITO: el de la sonda 5, con su salida contra main | Hecho (y la S7b) | §0.f |
| 37 | El test del límite declarado | No aplica (D2 dio (c2)) | — |
| 38 | CI: sin fix/ (no se tocan hooks, rutas, .claude/ ni plataforma) | Cumplido | `git diff main --stat` |
| 39 | INFORME: el encargo punto por punto, la fase 0, el censo, lo que no se pudo medir, las líneas del cierre y la fila de ERRORES-RECURRENTES con el error del consultor | Hecho | §0-§5 |
| 40 | El revisor (opus) con sus alcances, y su informe pegado | Hecho | §6 |
| 41 | Rama lista para revisión, NO cerrada | Hecho | «Estado» |

## 6. El revisor

Subagente `revisor` (opus), una pasada, sobre dacd533 más el informe sin estadiar, con los cinco
alcances del encargo. Pegado tal cual (no cita ningún tramo no citable: 0 retiradas):

> ## Informe del revisor · trabajo/sello-respaldo-m1 · 2026-11-07
>
> Revisión de los commits 13d9ad3, 460595f y dacd533 sobre main 2e04b63, más el informe sin estadiar `docs/validation/SELLO-RESPALDO-M1.md` (§4.1, §5 y «Estado»). No he escrito nada en el repo. No he ejecutado el arnés ni `prototipo_sello.py`.
>
> ### Eje (a) · Reglas de la casa
> Resumen: 0 bloquea, 1 importa, 1 menor.
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | a1 | importa | La fila del 2026-11-07 en HOLDOUT-EXPOSICIONES no declara el clon `C:/cm/h`. En él corrieron 29 ficheros de test de main, y al menos dos leen el `data/` real por `settings.local.toml`. El informe sí lo dice en §0.j y §4.1. Las filas anteriores sí declaran sus clones. Como la lista de los 29 no está en ningún sitio, tampoco se puede saber si alguno lee el M1 de marzo (como `test_visor.py` o `test_preparar_a35.py`). No es la exposición de un día reservado, pero el registro tiene menos que el informe. | Fila añadida (`git diff main...HEAD -- docs/validation/HOLDOUT-EXPOSICIONES.md`): solo (1) los make check, (2) censo_cierre, (3) casos_reservados, (4) el prototipo y (5) el auditor; no nombra el clon. `SELLO-RESPALDO-M1.md:339-341`: «Además, en el clon `C:/cm/h`: 29 ficheros de test de main, dos de los cuales (`test_simulacion.py` y `test_cuenta_7_de_agosto.py`) leen `data/`». Precedente: fila del 2026-11-05, punto «(3) **Un clon desechable de `main`** … con el `data/` real por `settings.local.toml`, y 31 ficheros de test del motor». |
> | a2 | menor | Una cita apunta dos líneas abajo: «sigue en el cierre de la vela» no está en ADR-0051:104 sino en :102-103. | `SELLO-RESPALDO-M1.md:63` cita «:104». Grep de «sigue en el cierre» en `docs/adr/0051-el-modelo-de-llenado.md` da `102:> … el instante del evento (sigue en el cierre`. La línea 104 es «> NOTA). Código: `engine/llenado.py`…». |
>
> Comprobado sin hallazgos:
> - **El contrato.** `uv run python scripts/contrato_rama.py`: «CONTRATO: 31 ficheros dentro del contrato de trabajo/sello-respaldo-m1 (riesgo alto, artefacto docs/validation/SELLO-RESPALDO-M1.md, tramo 'R3 · Una corrida del arnés sobre toda la construcción', 4 comprobaciones para el revisor)», exit 0.
> - **Las comprobaciones del contrato.**
>   - `uv run botsito state check`: OK, exit 0.
>   - `knowledge validate`: lo corrí a stdout y no a su fichero, porque escribir el log no me está permitido. Todo OK; los avisos son los de siempre; exit 0.
>   - `make check`: no lo corrí (escribe). Evidencia: `make-check.log` termina en «3241 passed in 1022.35s», «SELLO: make check en verde sobre el arbol 900b664fc2cd22011cc020215d9283705b59fdfd» y «PICO DE MEMORIA de make check: 307 MiB». `git rev-parse dacd533^{tree}` da ese mismo árbol.
>   - Los árboles de 460595f (9eadefec…) y 13d9ad3 (833d532f…) coinciden con la tabla de §4.
>   - El make check incluye ruff check, ruff format --check, mypy y state check.
>   - El informe sin estadiar todavía no tiene sello: lo necesita antes de su commit.
> - **Trailers `Fuente:`.** `git log … main..HEAD -- knowledge/spec knowledge/cases` sale vacío: la rama no toca `knowledge/`.
> - **Holdout.**
>   - Ningún fichero de `knowledge/cases/holdout/`.
>   - `casos_reservados(repo)`, contado por mí sin imprimir claves: 0 en cada uno de los once días y 0 en 2026-01, 04, 07 y 08. Hay 34 reservados en total y los 34 llevan «caso-eurusd-2026-», así que el recuento por fecha sí los habría encontrado.
>   - El calentamiento con el M1 de marzo, junio y julio está declarado en la fila; leer velas no es abrir un holdout (CLAUDE.md, punto 2).
> - **Regímenes de cambio.** `git diff --name-status main...HEAD -- knowledge/ data/manifests/ docs/adr/ .claude/ Makefile tools/` sale vacío. HISTORIA.md da 164+/0− y HOLDOUT-EXPOSICIONES.md 1+/0−.
> - **Ambigüedades y ADR.** No se tocan ni ambigüedades ni ADR. ADR-0091 no existe: el grep de «0091» en docs/ solo da ids de evidencia y precios, más el encargo y el informe, cada uno con su bloque `ids-inexistentes`.
> - **Informes cerrados.** Ningún `docs/validation/*.md` cerrado cambia; HOLDOUT-EXPOSICIONES es un registro y solo gana una fila.
> - **Tres guardias de una `cita`.** No aplica: la rama no añade ningún sitio con `cita`.
> - **Cifras y parámetros.** No entran cifras nuevas en la forma ejecutable: el cambio de `broker.py` es solo una condición.
> - **Ensayos.** El clon se hizo con `git worktree add --detach`. `git worktree list` ya solo muestra el repo y hay 150 tags (§4.1:466-468). El prototipo escribe sus páginas fuera del repo con la carpeta por argumento y comprueba que está fuera (`prototipo_sello.py:253-254`).
> - **Citas comprobadas contra su fuente** (todas bien salvo a2):
>   - RESPALDO-M1.md:351 («22 de 1002 en la 2») y :485.
>   - ADR-0051:86, ADR-0057:25-27 y ADR-0053:163-165 (dentro de su §5, que empieza en :159).
>   - HOJA-DE-RUTA:222-223 y :240-241.
>   - `cableado.py:302` (`hasta_ms = instante * MS_POR_MINUTO - 1`).
>   - `llenado.py:184,193,240,252,327,345,351`.
>   - Las diez líneas `def` de §0.d contra `git grep` en main.
> - **Evidencia nueva.** No aplica: no se añade ningún ítem.
>
> ### Eje (b) · Encargo
> Resumen: 0 bloquea, 5 importa, 3 menor. Requisitos: 29 hechos, 2 parciales, 0 no hechos (además: 1 hecho de otra forma y declarado, 1 que no aplica, 2 pendientes del commit final).
>
> | # | Requisito | Estado | Evidencia |
> |---|---|---|---|
> | 1 | Comprobar la base (main = docs(state), tag en su merge, CI en verde, ninguna otra rama) | Hecho | `git rev-parse "stable/F38p-demo-ejecuciones-2-3^{commit}" main^1` da 8f43d381… dos veces; `git branch --list` da main y la rama. La CI no la comprobé (ver abajo). |
> | 2 | Contrato: tramo entre comillas, riesgo alto, artefacto | Hecho | `contrato.yaml:2-4` |
> | 3 | Grep de «0091» antes de usar el número | Hecho | Grep en docs/: ningún ADR-0091; PROJECT_STATE sin «0091». |
> | 4 | NO cambian estrategia, spec, parámetros, perfil, ADR-0053 ni knowledge/ | Hecho | name-status: solo `src/botsito/engine/broker.py`, el test nuevo y documentos. |
> | 5 | Solo días de desarrollo, comprobados con casos_reservados y declarados | Hecho (ver a1) | Mis recuentos dan 0; la fila del 2026-11-07 existe. |
> | 6 | Ninguna corrida del arnés ni cifra agregada nueva; solo visor por caso | Hecho | `prototipo_sello.py:269-272` llama solo a `motor visor --caso <id> --simular --salida`. Ni el grep de `motor arnes`, `--todos`, `--meses` ni el de `diagnostico-cuenta-diaria` encuentran una llamada en los anexos o el informe. El «26» es el recuento que el encargo autoriza («gana tu recuento»); el «27» es de once días concretos. Los prototipos dan R por operación y por día, sin totales. |
> | 7 | Las dos corridas de R3.6 pasan a la re-corrida que cuenta (línea preparada) | Hecho | `simular_cierre.py:79-86`; lo volví a ejecutar: «a: [] b: [] c: []». |
> | 8 | Herencia: H entera (marcas, m1_entre, sesión de 07-11, fin de ventana, ADR-0068, tests) | Hecho | §0.d frente a `sondas_{main,e2,c2}.txt`: S1-S9 coinciden con lo que dice la tabla. |
> | 9 | Herencia: R3.6 | Hecho | §0.a, §0.b y §0.g |
> | 10 | Herencia: `_peor_del_minuto` con su sonda 5 (punto 27, b2) | Hecho | `tests/unit/test_peor_del_minuto.py:65-93` |
> | 11 | Herencia: reconstruir `censo_cierre.py` | Hecho | Lo volví a ejecutar: «## filas: 22» sobre RECORRIDA y «## filas: 26» sobre RESPALDO-M1, idéntico a los .txt commiteados. |
> | 12 | Herencia (:494) y punto e): grep de TODOS los lectores de abierta_ms y del minuto del evento | **Parcial** | b1 |
> | 13 | Herencia diagH y punto a): cada afirmación contrastada | **Parcial** | b3 |
> | 14 | Buscar «a H», «para H», «NA:H» y «R3.6» | Hecho (por el auditor) | §0.h:309-311; no lo repetí. |
> | 15 | Prototipo en memoria en los anexos; si la guardia lo niega, PARADA | Hecho de otra forma, declarado | §0.k:348-351 y §5 fila 17. Lo cubre la regla escrita en DECISIONES-DE-PROCESO.md:28 («salvo seguir la forma que la propia guardia propone en su mensaje, declarándolo»). |
> | 16 | b) los 22: de dónde salen y la lista otra vez | Hecho | §0.b; 22 y 26 reproducidos; `grep -c "M1 k sin ticks" prototipo-main.txt` da 27. |
> | 17 | c) el censo evento por evento, main frente a (c2), por día | Hecho | `comparar_formas.py`, vuelto a ejecutar, sale idéntico a `censo-main-c2.txt`. Las dos operaciones nuevas están en `prototipo-c2.txt:65` y `:237`. |
> | 18 | d) los tests de main que rompe (c2) | Hecho | `tests_c2.txt`: 10 FAILED, los mismos 10 que `diagH/tests_c2.txt`. |
> | 19 | f) (e2): el diff, los tests que rompe y la sonda 5 como test | Hecho | El diff de `src/` es el de §0.f más dos líneas de comentario. `uv run pytest tests/unit/test_peor_del_minuto.py -q` da 4 pasados. `test_sonda5_main.txt` da «2 failed, 2 passed», con los fallos en las líneas 75 y 93, que son las del test commiteado. |
> | 20 | g) las líneas del cierre, con los tests en verde y PROJECT_STATE por debajo de 23.000 | Hecho (ver b7) | Vuelto a ejecutar: «22794 bytes; los cuatro tests de test_project_state: ok». |
> | 21 | D1: (e2) pase lo que pase; PARADA si rompe un test o cambia algo más que la marca | Hecho (ver b2) | 3241 pasados en el make check de dacd533; `censo-main-e2.txt` vuelto a ejecutar: los once días con «operaciones IGUALES; ordenes iguales». |
> | 22 | D2: la regla de los 22 | Hecho, bien aplicada | Dos días con «operaciones DISTINTAS» (01-23 y 07-10). La regla manda (c2) con PARADA, y es lo que se hace (§0.c:142-145, §2). |
> | 23 | D3: (d) descartada | Hecho | No se mide ni se toca. |
> | 24 | D4: ninguna corrida agregada; PARADA si faltara una | Hecho | §0.i:315-318 |
> | 25 | D5: reconstruir la sonda y el prototipo del auditor; declarar lo perdido | Hecho | §0.i:322-326 |
> | 26 | PARADA condicional: fase 0 commiteada; con (c2), solo D1 y PARADA con el plan | Hecho | 460595f no toca src/ ni tests; dacd533; §2. |
> | 27 | Fase 1, punto 1: commit sellado de (e2) | Hecho | El sello 900b664f… es el árbol de dacd533. |
> | 28 | Fase 1, punto 2: ADR-0091 y test del límite | No aplica | D2 dio (c2) (§1:373-374). |
> | 29 | Fase 1, punto 3: el informe en su commit | Pendiente | `git status --short`: « M docs/validation/SELLO-RESPALDO-M1.md», sin sello todavía. |
> | 30 | Tests que rompen a propósito, con su salida contra main | Hecho | `test_sonda5_main.txt`, pegado en §0.f:238-245. |
> | 31 | CI: sin fix/ | Hecho | No se tocan hooks, `.claude/`, rutas ni plataforma. |
> | 32 | El informe: punto por punto, fase 0, censo, lo no medido, el cierre y la fila de ERRORES-RECURRENTES con el error del consultor | Hecho (ver b8) | §5 existe; la frase del consultor está en §3 idéntica a la del encargo:60. |
> | 33 | El revisor, con su informe pegado | Pendiente | Es este informe. |
> | 34 | (c2) no aplicado en src/ | Hecho | `git diff main...HEAD -- src/` solo da la hunk de `broker.py` (@@ -952,7 +952,9): una condición cambiada y dos comentarios. `llenado.py`, `cableado.py` y `primitivas_broker.py` no cambian. |
> | 35 | NO cerrada | Hecho | No hay merge, tag ni push de main. |
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | b1 | importa | §0.e no busca lo que la herencia pedía. El encargo pide buscar «TODOS los lectores de abierta_ms y del minuto del evento», y el grep de §0.e es solo `abierta_ms\|_peor_del_minuto`. Se quedan fuera tres grupos de lectores. **(i) El minuto del evento:** `broker.py:314` (`evento.minuto`, la versión anterior). **(ii) Los de `cerrada_ms`:** (c2) también adelanta 1 ms la salida por stop u objetivo del respaldo (en las sondas, «cerrada en M0+1 -1ms»). Esos lectores son la comisión del cierre (`broker.py:1110` en la rama, `:1108` en main), `:1114`, `:1119` y `cableado.py:685`. **(iii) Los del resultado de `_peor_del_minuto`:** `p.ultimo_precio` (`:940`) llega a `flotante()` (`:1057-1070`) y de ahí a `margen_libre()` (`:1039`); y `p.marcas` llega a `cuenta.marcar` (`cableado.py:454-455`). | `SELLO-RESPALDO-M1.md:182` («Grep de `abierta_ms\|_peor_del_minuto`»). Grep de `cerrada_ms` en src: `broker.py:1110 cargos.append(Cargo(_instante(p.cerrada_ms), comision, "comision"))`. `sondas_c2.txt`: «S7 … cerrada en M0+1 -1ms». La herencia está en el encargo:28 y en RESPALDO-M1.md:494. |
> | b2 | importa | «(e2) solo cambia la marca» no menciona que la marca también mueve el flotante y el margen libre (ADR-0081). Con (e2) podría cambiar un rechazo por margen o un tope. En los once días no cambia ninguna orden, así que lo medido aguanta, pero el informe solo menciona la equity y los topes (§0.f:226-228, §0.i), no el margen. | `SELLO-RESPALDO-M1.md:35-38`, `:224` y `:250` («solo cambia la marca»). `broker.py:940 p.ultimo_precio = peor`; `:1039 return self.saldo() + self.flotante() - self.margen_usado()`; `:1065 * Decimal(p.ultimo_precio - p.entrada)`. |
> | b3 | importa | Falta contrastar una afirmación de diagH, aunque §0.a dice haberlas contrastado todas. diagH apunta que con (c)/(c2), en ADR-0083 D2, «un llenado o un rechazo del respaldo gasta o libera el punto un cierre antes». Eso no aparece ni en la tabla de §0.a ni en el borrador de ADR-0091 ni en «Lo que necesito que decidas». | `diagH/INFORME-DIAG-H.md:305`. Grep de `0083\|punto usado\|punto_usado` en `SELLO-RESPALDO-M1.md`: ninguna coincidencia. |
> | b4 | importa | Los números de línea del plan son los de main y la propia rama ya los mueve. dacd533 añade dos líneas en `broker.py:955-956`, así que todo lo que hay debajo baja dos: :962 pasa a :964, :1091 a :1093, :1107 a :1109, :1110 a :1112, :1117 a :1119 y :1123 a :1125. La condición de (e2) ya está en :957 y no en :955. La rama de (c2) partirá de main con (e2) dentro, y el borrador de ADR-0091 y la decisión 1 citan las líneas viejas. Es justo la lección que el encargo heredaba («ya no cuadran con main: vuelve a localizarlas»). | `SELLO-RESPALDO-M1.md:35` y `:447` y el mensaje de dacd533 («Una linea (broker.py:955)»); en la rama, `broker.py:957`. `:396-397` y `:413-415` citan `broker.py:962`, `:1091`, `:1107` y `:1110`; el grep de la rama los da en `:964`, `:1093`, `:1109` y `:1112`. La línea H preparada (`simular_cierre.py:58-59`) remite a «los lectores de §0.e». |
> | b5 | importa | La regresión de §4.1 no se puede repetir: no nombra los 29 ficheros ni el comando de pytest. `tests_e2.txt` no trae la línea de resumen (los 343 solo salen de contar puntos). La skill pide «los comandos tal cual». Que se usara un solo clon está declarado; que no haya tabla de hashes, no. | `SELLO-RESPALDO-M1.md:457-458` («29 ficheros de test (los que importan el bróker, …)», sin lista). `tests_e2.txt`: cinco líneas de puntos, sin «passed». `.claude/skills/comparar-con-main/SKILL.md:73-75`. |
> | b6 | menor | El encabezado de las decisiones va a un nivel de título distinto del que fija la skill. | `SELLO-RESPALDO-M1.md:407` usa «### Lo que necesito que decidas»; `.claude/skills/fase-cero/SKILL.md:73` pide «## Lo que necesito que decidas». |
> | b7 | menor | La previsión de 22.794 bytes se hace sobre el Current Feature de la rama (125 bytes). El que escribe el cierre, con el formato del de main, mide 263. Eso son unos 138 bytes más, alrededor de 22.930: sigue por debajo de 23.000, pero el informe no da este margen. | `grep -A1 "^## Current Feature"`: 263 bytes en main y 125 en la rama. `simular_cierre.py:10-11` («No simula lo que el ritual de cierre pone en … Current Feature»). |
> | b8 | menor | La fila preparada para ERRORES-RECURRENTES tiene 3 celdas y la tabla de destino tiene 4 columnas. | `SELLO-RESPALDO-M1.md:439` frente a `docs/runbooks/ERRORES-RECURRENTES.md:50` («\| Rama \| Hallazgos del revisor \| Hallazgos del consultor despues \| Que se le escapo \|»). |
>
> ### Lo que no pude comprobar
> - **La CI de main (run 42342344212):** no ejecuté `gh`.
> - **El make check del árbol final**, con el informe estadiado: escribe y no lo ejecuto. Hace falta antes del commit del punto 3.
> - **Que el test copiado en el clon fuera idéntico al commiteado:** el clon ya no existe. Lo que lo apoya es indirecto: las líneas de fallo 75 y 93 de `test_sonda5_main.txt` coinciden con las del test commiteado.
> - **Qué 29 ficheros corrieron en el clon**, y si alguno lee el M1 de marzo (ver a1 y b5).
> - **Que las salidas del prototipo salgan de una ejecución real**, y que la fila de exposiciones se escribiera antes de ejecutarlo: no volví a ejecutar `prototipo_sello.py`, como se me indicó.
> - **Las búsquedas «a H», «para H», «NA:H» y «R3.6»** del auditor, y lo de (d) en diagH: no las repetí.
> - **Lo que tiene que declarar la sesión de lo que yo he mirado hoy** (no lo puedo escribir yo):
>   - Leí parte de diagH: `ls`, un grep, las líneas 286-325 de `INFORME-DIAG-H.md`, y los FAILED y el resumen de sus `tests_c2.txt` y `tests_e2.txt`.
>   - Ejecuté `censo_cierre.py` sobre las dos diarias commiteadas (solo filas), y `comparar_formas.py` y `simular_cierre.py`.
>   - Conté `casos_reservados` (solo recuentos, sin claves).
>   - Leí las salidas del prototipo con head y grep: órdenes y R por día de once días de desarrollo.
>   - Ejecuté pytest de `tests/unit/test_peor_del_minuto.py` (velas sintéticas) y `knowledge validate`.
>   - **Sin querer**, un `sed -n '1,0p'` me imprimió la primera fila de HOLDOUT-EXPOSICIONES.md (línea 17, la del 2026-09-11, que copia agregados de mayo). Esa fila ya está en main y declarada desde ese día, pero lo dejo dicho para que la sesión decida si lo anota.
>
> ### Comandos ejecutados
> 1. `git branch --show-current`; `git merge-base main HEAD`; `git log --format='%h %s' main..HEAD`; `git diff --stat main...HEAD`; `git status --short`
> 2. Read: el encargo, `contrato.yaml`, `SELLO-RESPALDO-M1.md`
> 3. `uv run python scripts/contrato_rama.py`
> 4. `git diff --name-status main...HEAD`; `git diff main...HEAD -- src/`
> 5. Read: `tests/unit/test_peor_del_minuto.py`, `broker.py:920-969`
> 6. `uv run pytest tests/unit/test_peor_del_minuto.py -q`
> 7. `uv run botsito state check`
> 8. `uv run botsito knowledge validate 2>&1 | tail -15`
> 9. `grep -nE "SELLO|PICO DE MEMORIA|passed|failed" make-check.log`; `sed -n '1,12p;84,108p' make-check.log`
> 10. `git rev-parse dacd533^{tree} 460595f^{tree} 13d9ad3^{tree}`
> 11. `git log --format='%h%n%B' main..HEAD -- knowledge/spec knowledge/cases`; `git diff --name-status main...HEAD -- knowledge/ data/manifests/ docs/adr/ .claude/ Makefile tools/`; `git log --format='%h %s%n%b' main..HEAD`
> 12. `git diff main...HEAD -- docs/validation/HOLDOUT-EXPOSICIONES.md PROJECT_STATE.md`
> 13. `cat` del README, `tests_e2.txt` y `tests_c2.txt` (head y tail) de los anexos
> 14. Read: las skills comparar-con-main, entregar-rama y fase-cero
> 15. Intento de un `for` (la guardia lo negó: «el bucle `for` fija `c`»); en su lugar, `git show --stat --format='== %h' 13d9ad3 460595f dacd533`
> 16. `wc -c PROJECT_STATE.md`; `git show main:PROJECT_STATE.md | wc -c`; `git show 13d9ad3:PROJECT_STATE.md | wc -c`; `cat simular-cierre.txt`
> 17. Read: `simular_cierre.py`, `censo_cierre.py`, `comparar_formas.py`, `prototipo_sello.py`, `forma_c2_main2e04b63.diff`, `test_sonda5_main.txt`, `censo-cierre-respaldo-m1.txt`, `censo-main-c2.txt`, RESPALDO-M1.md:440-499
> 18. `uv run python -B …/censo_cierre.py` sobre las diarias de RECORRIDA y de RESPALDO-M1
> 19. `uv run python -B …/comparar_formas.py` main frente a c2 y main frente a e2; `cat censo-main-e2.txt`
> 20. `grep -c "M1 k sin ticks"` y `grep -n LLENARIA` en las salidas del prototipo; `head -30 prototipo-main.txt`; `grep` de las operaciones nuevas en `prototipo-c2.txt`
> 21. Grep en src: `abierta_ms|_peor_del_minuto`, `cerrada_ms`, `ultimo_precio`, `flotante\(\)|\.marcas\b`, `class Evento|…|\.minuto\b`, `def fin|def inicio|inicio:`; Read `broker.py:1050-1074`
> 22. `git show main:src/botsito/engine/broker.py | grep -n abierta_ms`; `git show main:…/cableado.py | sed -n '298,304p'`; `grep -n _fin_ms llenado.py`
> 23. Grep «minuto del evento» en RESPALDO-M1.md
> 24. `uv run python -c` con `casos_reservados`, solo recuentos (dos llamadas)
> 25. Grep de `motor arnes|--todos|--meses|cobertura|precisi|veredicto|diagnostico-cuenta-diaria` en los anexos y el informe; grep de los argumentos del visor en `cli.py`
> 26. diagH: `ls`, `wc -l` y `grep -n` en `INFORME-DIAG-H.md`; Read de sus líneas 286-325; `grep ^FAILED` y `tail` de sus `tests_c2.txt` y `tests_e2.txt`
> 27. `git grep -n` de las diez `def` en main; `sed` de ADR-0051:86 y :104, ADR-0057:25-27 y ADR-0053:163-165; grep de las secciones y de «peor marca» en ADR-0053; grep de «sigue en el cierre» en ADR-0051
> 28. `sed` de RESPALDO-M1.md:351 y :722 y de HOLDOUT-EXPOSICIONES.md:83 (con el `sed -n '1,0p'` que imprimió sin querer su línea 17)
> 29. `sed -n '218,226p;238,242p'` de HOJA-DE-RUTA.md; grep de `NA:H` en la hoja de ruta
> 30. `git diff --stat 7a3a1ff main -- src/`
> 31. `git rev-parse "stable/F38p-demo-ejecuciones-2-3^{commit}" main^1`; grep del run en HISTORIA (sin resultado)
> 32. `git tag -l | wc -l`; `git worktree list`; `git branch --list`
> 33. Grep de «0091» en docs/ y en PROJECT_STATE.md; grep de las reglas de la guardia en docs/runbooks; `sed -n '28p'` de DECISIONES-DE-PROCESO.md
> 34. `grep -A1 "^## Current Feature"` en main, en la rama, en 13d9ad3 y en 460595f
> 35. `grep -n "^| Rama"` en ERRORES-RECURRENTES.md; `grep -l "Dado por Aleks (consultor)"` en los encargos

### 6.1 Lo que se hizo con los hallazgos del revisor

| # | Gravedad | Qué se hizo |
|---|---|---|
| a1 | importa | **Arreglado**: fila nueva del 2026-11-07 en HOLDOUT-EXPOSICIONES con el clon (los 29 ficheros, por remisión a §4.1, y los dos que leen `data/`: `test_cuenta_7_de_agosto.py`, el 2026-08-07, y `test_simulacion.py`, por la compuerta; ninguno es `test_visor.py` ni `test_preparar_a35.py`), con lo que miró el revisor y con la línea 17 que imprimió sin querer (ya declarada desde el 2026-09-11) |
| a2 | menor | **Arreglado**: §0.a cita ADR-0051:102-103 |
| b1 | importa | **Arreglado**: §0.e lleva una segunda tabla con el minuto del evento (`broker.py:314`), los lectores de `cerrada_ms` (`:917`, `:1110`, `:1114`, `:1119`, `:1126`, `cableado.py:685`) y los del resultado de `_peor_del_minuto` (`ultimo_precio` → flotante → margen libre; `cuenta.marcar`); y el borrador del ADR, el punto (7) |
| b2 | importa | **Arreglado**: §0.f dice que la marca mueve el flotante y el margen libre (ADR-0081), y qué se midió (ninguna orden ni operación distinta en los once días; la suite entera en verde); §0.i lo añade a lo no medido. D1 no cambia: lo que (e2) mueve sale todo de la marca de `_peor_del_minuto` |
| b3 | importa | **Arreglado**: fila nueva en §0.a (ADR-0083 D2: el mismo mecanismo que §0.c mide, sin test propio) y punto (6) del borrador del ADR |
| b4 | importa | **Arreglado**: §0.e y el «Alcance» del borrador dicen que las líneas son las de main y dan las de la rama (`:957`, `:964`, `:1093`, `:1109`, `:1112`, `:1119`, `:1125`). El mensaje de dacd533 («broker.py:955») no se reescribe: es la línea de main, donde cae el cambio |
| b5 | importa | **Arreglado**: §4.1 lleva el comando de pytest tal cual con los 29 ficheros, de dónde salen los 343 y la falta de tabla de hashes declarada como desviación de la skill, con su motivo |
| b6 | menor | **Arreglado**: «## Lo que necesito que decidas» |
| b7 | menor | **Arreglado**: §0.g da la previsión tras el cierre (~22.930 bytes, margen ~70) |
| b8 | menor | **Arreglado**: la fila de §3 lleva las cuatro columnas de la tabla de destino |

Lo que el revisor no pudo comprobar: la CI de main la comprobó la sesión al abrir («Base comprobada
al abrir»: run 42342344212, success); el `make check` del árbol final es el del último commit (§4).

## Respuesta del consultor a la PARADA (2026-11-07)

Copiada tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA de trabajo/sello-respaldo-m1 (2026-11-07). Cópiala tal cual en el informe (skill fase-cero) y aplícala punto por punto. Puede correr sin supervisión: decisiones por adelantado y PARADA condicional. NUNCA cierra.
>
> 0. (c2) se implementa EN ESTA RAMA, en una fase 2 con ADR-0091. Porqué: es el trabajo de la entrada H, no depende de R, y hay precedente de ampliar el contrato con un ADR tras una PARADA (ENTRADA-ENERO.md:635). Quedan sin efecto, por escrito en el informe: la segunda mitad de la regla D2 del encargo («NO se implementa en esta rama esta noche»), la frase del informe «el ADR lo escribe la rama de (c2)» y la línea F de §0.g, que se reescribe. El contrato se amplía en un commit propio con src/, tests/, los ADR 0051, 0057, 0068, 0083 y el nuevo 0091, y el bloque ids-inexistentes de ADR-0091 sale en el commit que lo crea. Riesgo: alto.
> 1. Lectores del minuto de apertura: (a), neutralidad completa. Los tres de diagH más broker.py:962 (swap) y :1091 (día local) leen (abierta_ms + 1) // 60000; el instante de comisiones y criterio se queda en el sellado. Porqué: el ADR cambia qué vela se evalúa, no a qué minuto ni a qué día pertenece un llenado. Test de S9 en los dos lados. Lo mismo para los lectores de cerrada_ms de §0.e: cada uno, neutral o no, con su porqué en una línea del ADR.
> 2. Fin del día y borde de ADR-0068: (a), se aceptan. Las dos velas transcurren enteras antes de su borde. NOTA en ADR-0068 §2: con el respaldo, un llenado en la vela que acaba en W se sella en W − 1 ms, fuera de la ventana (R15 prohíbe abrir desde dos horas antes y ADR-0068 §1 mete W dentro); la pendiente sigue cancelándose al empezar la ventana. Test en los dos lados para S4 y S5.
> 3. Versión anterior (Orden.anterior, Posicion.stop_anterior): (a), se queda, con la NOTA en ADR-0051 §5 de que desde el motor ya no se alcanza. Porqué: retirarla es otra rama.
> 4. Los dos tests de secuencia: (a), reescritos a media vela, más uno nuevo en el cierre que fije que la vela se evalúa antes de mover o modificar.
> 5. Universo del censo: (a), los once días bastan; la re-corrida que cuenta verá el resto. Ninguna corrida del arnés ni cifra agregada en esta rama, como en el encargo.
> 6. ADR-0083 D2 (hallazgo del auditor del consultor): con (c2), un rechazo al llenar gasta el punto, y un stop u objetivo sin ganancia libera la zona, un cierre ANTES; D4 ve la posición abierta un cierre antes. Va con test propio en los dos lados (el rechazo gasta en el cierre de k; la liberación y la reentrada por D5 llegan en el cierre de k) y como punto (6) del ADR, con fichero:línea de cableado.correr_dia.
> 7. ADR-0091: el borrador de §2 con lo de arriba, estado ACTIVE, recuadros en ADR-0051 §5 (y su NOTA del 2026-10-29), ADR-0057 §1, ADR-0068 §2 y ADR-0083 D2, filas del índice. Lo medido de §0.c entra como alcance (27 cancelaciones en 11 días de desarrollo, 2 operaciones nuevas), sin ninguna cifra agregada sobre un mes. Escribe también que el bot en vivo opera con ticks (ADR-0051 §8) y el respaldo solo cubre minutos sin ticks.
> 8. Verificación tras implementar, con el visor por caso (nunca --todos ni --meses): los once días de §0.c con el código de la rama dan exactamente lo que dio el prototipo (las 2 operaciones nuevas, −1,00 R cada una, y las demás idénticas a main). Si algún día difiere del prototipo, PARADA solo para ese día, con el diff.
> 9. Tests que rompen a propósito en main y pasan en la rama (comparar-con-main, salida pegada): el llenado de la vela k de una orden cancelada en su cierre; S4 y S5; S9; el de ADR-0083 D2; los 8 del milisegundo reescritos. Los dos de la secuencia, reescritos a media vela, pasan en los dos lados y el informe lo dice.
> 10. Hoja de ruta, líneas preparadas para el cierre: R3.6 pasa a HECHA en esta rama con su «Hecho cuando» corregido (el ADR aceptado, los tests que rompen en main, los once días verificados); las «dos corridas repetidas» salen de R3.6 y pasan a R3.7 y a la re-corrida que cuenta (ADR-0070 §3), porque R3.7 pide pre-registrar los umbrales antes de ver ninguna corrida nueva. H sale HECHA. F se reescribe: siguiente R, después la re-corrida que cuenta, la primera con la comisión medida y el sello de ADR-0091. Probadas sobre una copia, con wc -c por debajo de 23.000.
> 11. Fila de ERRORES-RECURRENTES preparada, con estos errores del consultor añadidos a los de §3: (importa) el encargo llamó «eventos del respaldo» a 22 cancelaciones del bot y las mandó sacar de la salida equivocada (la lección (2) de §3 pasa a la columna del consultor); (menor) citó «el plan del 2026-11-01» cuando las dos corridas de R3.6 vienen de la respuesta del consultor del 2026-10-29 (RESPALDO-M1.md:485): se corrige la lección (1); (menor) la regla D2 prohibía implementar (c2) en la rama que ya era la de H, y costó una PARADA más. Lección: la regla de una PARADA condicional decide el camino, no la rama en la que se hace.
>
> FASE 2, un commit por punto, cada uno con estadiar, uv run botsito state check, make check > make-check.log 2>&1, leer el log (exit 0, ningún failed y la línea SELLO), y ruff format, ruff check y mypy sobre lo tocado:
> a) El contrato ampliado.
> b) ADR-0091 y sus recuadros (sale el bloque ids-inexistentes).
> c) Las tres funciones del respaldo y los lectores (puntos 1 y 6), con los tests nuevos y los reescritos.
> d) La verificación del punto 8 y el informe, con §0.g y §3 reescritos y las líneas del cierre probadas sobre la copia.
> Si la guardia niega algo legítimo, PARADA para eso con el comando exacto, y sigue con lo demás.
>
> CI: toca src/ del motor; no toca hooks, rutas, .claude/ ni plataforma: sin fix/. Si tocaras alguno, fix/<rama> y el run.
>
> Revisor (opus) otra vez, con estos alcances: reglas de la casa; esta respuesta punto por punto; que los once días coincidan con el prototipo; que cada lector de abierta_ms y cerrada_ms esté decidido en el ADR; ninguna corrida agregada; ningún día fuera de enero, abril, julio y agosto; exposiciones declaradas. Pega su informe al final.
>
> Rama lista para revisión, NO cerrada.

## 7. La respuesta aplicada: fase 2 (2026-11-07)

**Quedan sin efecto, por escrito** (respuesta, punto 0):
- la segunda mitad de la regla D2 del encargo, «NO se implementa en esta rama esta noche»: (c2) se
  implementa aquí, en la fase 2, con ADR-0091;
- la frase del bloque `ids-inexistentes` que encabezaba este informe, «el ADR lo escribe la rama de
  (c2)», y lo mismo en §1, punto 2, y en §2 («no se crea en esta rama»): lo escribe esta rama, en el
  commit b), que quitó los dos bloques (el del encargo y el de este informe);
- la línea F de §0.g, y con ella H y R3.6: §0.g está reescrito (punto 10).

### 7.1 Punto por punto

| # | Lo que manda la respuesta | Hecho | Dónde |
|---|---|---|---|
| 0 | (c2) en esta rama, fase 2, con ADR-0091; lo que queda sin efecto, por escrito; el contrato ampliado en su commit (src/, tests/, ADR 0051, 0057, 0068, 0083 y 0091); el bloque sale en el commit del ADR; riesgo alto | Hecho | arriba; cdffbfb (a): `src/botsito/engine/`, `tests/`, los cinco ADR y el índice; 3252548 (b) |
| 1 | Lectores del minuto de apertura, neutralidad completa: los tres de diagH más el swap y el día local con `(abierta_ms + 1) // 60000`; comisiones y criterio en el sellado; test de S9 en los dos lados; los de `cerrada_ms`, cada uno con su porqué en el ADR | Hecho, con una sola definición, `broker.minuto_de_apertura`, que leen `_marcar_hasta`, `_swaps`, `_limite_infringido`, `cableado._operaciones_del_bot` y el break even por velas. Los de `cerrada_ms`, en el instante sellado y **no neutros** en el swap del cierre (una posición que sale por la última vela antes del corte no paga su swap: no vivió más allá), cada uno con su línea en ADR-0091 §3. **S9 rompe en `main`** (por el sello, `abierta_ms` = corte − 1 ms) y fija la neutralidad del swap y del día: «en los dos lados» se lee así, y el punto 9 lo pone entre los que rompen | 7eda14d; ADR-0091 §2-§3; `test_un_llenado_en_la_ultima_vela_antes_del_corte_no_paga_ese_swap_ni_cambia_de_dia` |
| 2 | Fin del día y borde de ADR-0068 aceptados; NOTA en ADR-0068 §2; tests de S4 y S5 | Hecho | ADR-0091 §5; recuadro en ADR-0068 §2; los dos tests rompen en `main` |
| 3 | La versión anterior se queda, con la NOTA en ADR-0051 §5 de que desde el motor ya no se alcanza | Hecho | recuadro en ADR-0051 §5; ADR-0091 §6 |
| 4 | Los dos tests de secuencia, a media vela, y uno nuevo en el cierre | Hecho | `test_respaldo_m1_decision.py`: los dos, a media vela (pasan en `main` y en la rama), y `test_en_el_cierre_la_vela_se_evalua_antes_de_mover_el_stop_o_modificar_la_orden` (rompe en `main`) |
| 5 | Los once días bastan; ninguna corrida del arnés ni cifra agregada | Cumplido | §7.3 |
| 6 | ADR-0083 D2: el rechazo al llenar gasta, y el stop u objetivo sin ganancia libera, un cierre antes; D4 un cierre antes; test propio en los dos lados; punto (6) del ADR con fichero:línea de `cableado.correr_dia` | Hecho. **Va en ADR-0091 §4, no en un §6**: el borrador numeraba en una lista, y el ADR lo ordena por tema (§6 es la versión anterior); lleva `engine/cableado.py:305`, `:306` y `:308`, las de la rama (en la primera versión, las de `main`: revisor, segunda pasada, b2) | recuadro en ADR-0083 D2; dos tests por el cableado sin ticks, que rompen en `main` |
| 7 | ADR-0091 ACTIVE con el borrador y lo de arriba; recuadros en ADR-0051 §5 (y su NOTA), 0057 §1, 0068 §2 y 0083 D2; filas del índice; el alcance medido sin cifra agregada sobre un mes; que el bot en vivo opera con ticks | Hecho | `docs/adr/0091-el-sello-del-respaldo-m1-en-el-ultimo-milisegundo-de-su-vela.md` (§7, el alcance: 27 cancelaciones y 2 operaciones en once días); `docs/adr/README.md` |
| 8 | Verificación con el visor por caso: los once días dan lo que dio el prototipo; si alguno difiere, PARADA para ese día | Hecho, **sin PARADA**: idénticos línea a línea | §7.3 |
| 9 | Tests que rompen en `main` y pasan en la rama, con su salida; los dos de la secuencia pasan en los dos lados | Hecho | §7.2 |
| 10 | Las líneas del cierre: R3.6 HECHA, las dos corridas a R3.7 y a la re-corrida que cuenta, H HECHA, F reescrita; probadas sobre una copia, < 23.000 | Hecho: 21.860 bytes, y 21.986 con un Current Feature del cierre | §0.g; `simular-cierre.txt` |
| 11 | La fila de ERRORES-RECURRENTES con los errores del consultor añadidos | Hecho | §3 |
| a-d | Un commit por punto, cada uno sellado, con ruff format, ruff check y mypy antes | Hecho | §7.4 |
| CI | Sin fix/ (no se tocan hooks, rutas, `.claude/` ni plataforma) | Cumplido | `git diff --stat main...HEAD` |
| Revisor | Otra pasada, opus, con los alcances de la respuesta; su informe, pegado | Hecho | §8 |

### 7.2 Los tests, contra `main`

En un clon desechable de `main` (`C:/cm/m`, `git worktree add --detach`, sin `data/`), con los seis
ficheros de test de la rama que tocan el sello copiados dentro (skill comparar-con-main):

    uv run pytest -p no:cacheprovider -q -rf --tb=line tests/unit/test_sello_respaldo.py tests/unit/test_broker.py tests/unit/test_broker_ordenes_stop.py tests/unit/test_llenado.py tests/unit/test_respaldo_m1_decision.py tests/unit/test_peor_del_minuto.py

Exit 1, **18 FAILED** (`anexos/SELLO-RESPALDO-M1/tests_rama_con_main.txt`, repetido tras la
segunda pasada del revisor con el test del swap al cierre y la línea de resumen; la primera vez
fueron 17, sin ese test). La salida, recortada:

```
FAILED tests/unit/test_sello_respaldo.py::test_la_vela_en_cuyo_cierre_el_motor_cancela_la_orden_la_llena_antes
FAILED tests/unit/test_sello_respaldo.py::test_el_fin_del_dia_evalua_la_ultima_vela_antes_de_cerrar_y_cancelar
FAILED tests/unit/test_sello_respaldo.py::test_un_llenado_en_la_vela_que_acaba_en_la_ventana_se_sella_fuera_de_ella
FAILED tests/unit/test_sello_respaldo.py::test_un_llenado_en_la_ultima_vela_antes_del_corte_no_paga_ese_swap_ni_cambia_de_dia
FAILED tests/unit/test_sello_respaldo.py::test_una_salida_en_la_ultima_vela_antes_del_corte_no_paga_ese_swap
FAILED tests/unit/test_sello_respaldo.py::test_sin_ticks_el_punto_se_libera_y_se_vuelve_a_colocar_en_el_cierre_de_la_vela_del_stop
FAILED tests/unit/test_sello_respaldo.py::test_sin_ticks_un_rechazo_al_llenar_gasta_el_punto_en_el_cierre_de_la_vela_del_llenado
FAILED tests/unit/test_broker.py::test_el_respaldo_m1_llena_cierra_y_marca_sin_ticks
FAILED tests/unit/test_broker_ordenes_stop.py::test_el_respaldo_m1_llena_al_nivel_o_a_la_apertura_si_la_vela_abre_pasada
FAILED tests/unit/test_broker_ordenes_stop.py::test_misma_vela_la_stop_sigue_la_convencion_de_la_limite
FAILED tests/unit/test_llenado.py::test_una_m1_con_stop_y_objetivo_a_la_vez
FAILED tests/unit/test_llenado.py::test_un_tramo_sin_ticks_cae_al_respaldo_y_queda_marcado
FAILED tests/unit/test_respaldo_m1_decision.py::test_en_el_cierre_la_vela_se_evalua_antes_de_mover_el_stop_o_modificar_la_orden
FAILED tests/unit/test_respaldo_m1_decision.py::test_la_vela_de_una_modificacion_no_llena_la_version_nueva
FAILED tests/unit/test_respaldo_m1_decision.py::test_una_pendiente_de_antes_de_una_vela_sin_ticks_se_llena_en_esa_vela
FAILED tests/unit/test_respaldo_m1_decision.py::test_la_salida_tras_un_llenado_del_respaldo_se_mira_desde_la_vela_siguiente
FAILED tests/unit/test_peor_del_minuto.py::test_avanzar_a_un_instante_redondo_no_marca_la_vela_que_empieza_en_el
FAILED tests/unit/test_peor_del_minuto.py::test_una_expiracion_en_un_instante_redondo_no_marca_la_vela_siguiente
18 failed, 39 passed in 5.14s
```

| Qué | Tests que rompen en `main` |
|---|---|
| (c2), nuevos (`test_sello_respaldo.py`) | la vela en cuyo cierre el motor cancela la orden la llena antes (S6); el fin del día evalúa la última vela (S4); el llenado en la vela que acaba en la ventana se sella fuera de ella (S5); S9; la salida en la última vela antes del corte no paga ese swap (ADR-0091 §3, tras la segunda pasada del revisor); y los dos de ADR-0083 D2 por el cableado sin ticks (el punto se libera y se vuelve a colocar en el cierre de la vela del stop; el rechazo al llenar lo gasta en el cierre de la vela del llenado) |
| (c2), los 8 del milisegundo, reescritos | `test_broker.py::test_el_respaldo_m1_llena_cierra_y_marca_sin_ticks`; `test_broker_ordenes_stop.py::test_el_respaldo_m1_llena_al_nivel_o_a_la_apertura_si_la_vela_abre_pasada` y `::test_misma_vela_la_stop_sigue_la_convencion_de_la_limite`; `test_llenado.py::test_una_m1_con_stop_y_objetivo_a_la_vez` y `::test_un_tramo_sin_ticks_cae_al_respaldo_y_queda_marcado`; `test_respaldo_m1_decision.py::test_la_vela_de_una_modificacion_no_llena_la_version_nueva`, `::test_una_pendiente_de_antes_de_una_vela_sin_ticks_se_llena_en_esa_vela` y `::test_la_salida_tras_un_llenado_del_respaldo_se_mira_desde_la_vela_siguiente` |
| (c2), el nuevo del cierre | `test_respaldo_m1_decision.py::test_en_el_cierre_la_vela_se_evalua_antes_de_mover_el_stop_o_modificar_la_orden` |
| (e2), de la fase 1 | los dos de `test_peor_del_minuto.py` que ya rompían (la sonda 5, que ahora cierra en el sello nuevo, y la S7b) |

**Pasan en `main` y en la rama**: los dos de la secuencia reescritos a media vela
(`test_la_vela_del_stop_movido_que_toca_el_stop_original_sale_por_el_sin_break_even` y
`test_la_vela_de_una_modificacion_se_evalua_con_la_orden_anterior`), S1 (la marca de la vela del
llenado no se toma) y los demás de esos ficheros. En la rama, los seis ficheros pasan enteros, y la
suite entera también (3249 passed en el `make check` de 7eda14d). Con (c2) solo, sin (e2), la sonda 5
ya no rompería: la salida del respaldo se sella antes del instante redondo; la S7b (la expiración en
el instante redondo) sigue fijando (e2). En la rama, `test_sello_respaldo.py` tiene 8 tests y pasan todos.

**Lo que la guardia negó, y cómo se hizo**: en el clon de la rama (`C:/cm/r`) la guardia no resolvió
`from tests.unit import …` de `test_sello_respaldo.py`, que aún no estaba en el repo; ese fichero se
corrió en el repo y, ya copiado, en el clon de `main`, donde sí corrió (el mismo fichero que el del
repo). Los demás, en el clon de la rama. Ninguna medida dejó de hacerse.

### 7.3 La verificación del punto 8 (el visor por caso, con el código de la rama)

`prototipo_sello.py` con la forma nueva `rama` (nada parcheado: el código commiteado en 7eda14d; la
sesión de cada posición, leída con `minuto_de_apertura`), sobre los MISMOS once días de la fase 0, y
nada más (`motor visor --caso <id> --simular`, una llamada por día; ni `--todos` ni `--meses`):

    uv run python -B docs/validation/anexos/SELLO-RESPALDO-M1/prototipo_sello.py rama <carpeta fuera del repo> 2026-01-14 2026-01-23 2026-04-03 2026-04-06 2026-04-07 2026-04-22 2026-04-23 2026-07-10 2026-07-16 2026-08-17 2026-08-20

→ `verificacion-rama.txt`, exit 0. **Sin sus líneas de cabecera (`#`, `OK:` y `TIEMPO`), `diff`
contra `prototipo-c2.txt` sale vacío: los once días dan EXACTAMENTE lo que dio el prototipo**, orden
a orden y posición a posición, con sus instantes y su R. Y `comparar_formas.py` de main frente a la
rama (`censo-main-rama.txt`) es el de main frente al prototipo con otro nombre de fichero: las 2
operaciones nuevas (2026-01-23, venta en la vela de las 11:03, −1,00 R; 2026-07-10, compra en la de
las 05:27, −1,00 R) y las demás operaciones de los once días idénticas a main. Ningún día difiere:
no hay PARADA.

### 7.4 Los commits de la fase 2

| Commit | Qué | `make check` |
|---|---|---|
| cdffbfb | a) la respuesta copiada y el contrato ampliado | sello `7dbf0937…`, 3241 passed |
| 3252548 | b) ADR-0091, los cuatro recuadros, el índice; salen los dos bloques `ids-inexistentes` | sello `9ede7820…`, 3241 passed |
| 7eda14d | c) las tres funciones del respaldo y los lectores, con los tests nuevos y los reescritos; «Tests Currently Passing» 1873 | sello `27ef41ab…`, **3249 passed** |
| (este) | d) la verificación, el informe (§0.g y §3 reescritos, §7, §8), las líneas del cierre probadas y lo hecho con la segunda pasada del revisor: ADR-0091 y los recuadros corregidos, el test del swap al cierre y los docstrings; «Tests Currently Passing» 1874 | el del último commit |

## 8. El revisor, segunda pasada

Subagente `revisor` (opus), segunda pasada, sobre cdffbfb, 3252548 y 7eda14d más el punto d) sin
estadiar, con los alcances de la respuesta del consultor. Pegado tal cual (no cita ningún tramo no
citable: 0 retiradas):

> ## Informe del revisor · trabajo/sello-respaldo-m1 (segunda pasada, tras la fase 2) · 2026-11-07
>
> Qué revisé: los commits cdffbfb (a), 3252548 (b) y 7eda14d (c) sobre main 2e04b63, y el punto d), que sigue sin estadiar (el informe, HOLDOUT-EXPOSICIONES.md, el README de los anexos, `prototipo_sello.py`, `simular_cierre.py` y sus salidas). No escribí nada en el repo. No ejecuté ni el arnés ni `prototipo_sello.py`, ni volví a correr el visor.
>
> ### Eje (a) · Reglas de la casa
> Resumen: 0 bloquea, 3 importa, 2 menor.
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | a1 | importa | **«Con ticks no cambia nada» choca con lo que dice el propio ADR-0091.** ADR-0091 §2 reconoce que el «+ 1» también mueve al minuto siguiente un llenado por TICK en el milisegundo .999. Sin embargo, la cabecera de ADR-0091, su fila del índice y los recuadros de ADR-0051, 0068 y 0083 dicen que solo cambian los minutos sin ticks. Con ticks, ese «+ 1» cambia cuatro cosas: la sesión de un llenado en el último ms de una sesión, el swap de una posición llenada a las 23:59:59.999 locales que pasa la noche (deja de pagarlo), el día de `posiciones_dia_max` y la marca de su minuto. Ningún test ni sonda lo mide; el informe ya lo daba por «no medido aquí» en §0.a. | ADR-0091:12 «**Solo cambia los minutos SIN ticks**» frente a ADR-0091:49-51 «El «+ 1» mueve también un llenado por TICK en el milisegundo .999 de un minuto al minuto siguiente». ADR-0051, recuadro: «Solo los minutos sin ticks: con ticks no cambia nada (§8)». ADR-0083 y ADR-0068, recuadros: «Con ticks no cambia nada». `docs/adr/README.md`, fila 0091: «solo los minutos sin ticks». `broker.py:975`: `ultimo = … minuto_de_apertura(p) * MS_POR_MINUTO`. SELLO-RESPALDO-M1.md:67: «no medido aquí». |
> | a2 | importa | **El cambio no neutro del swap al cierre está escrito en el ADR, pero sin medir.** Con el sello nuevo, una posición que sale por el respaldo en la última vela antes de un corte ya no paga el swap de ese corte. ADR-0091 §3 lo afirma («con el sello en k fin lo pagaba»), pero ningún test lo fija y no cae en los once días: el prototipo no imprime swaps. Es un cambio de coste de la cuenta, y CLAUDE.md pide medir antes de escribir cómo se comporta un mecanismo. El código sostiene lo que dice el ADR (`_aplicar` llama a `_marcar_hasta(instante)` y, con él, a `_swaps(p, instante)` antes de `_cerrar`; y el corte se cobra solo si `corte <= hasta_ms`), así que lo que falta es el test, no la razón. | ADR-0091:60-63. `broker.py:837`, `:950`, `:978`, `:1127`. `test_sello_respaldo.py` solo tiene S9, que es el swap de la APERTURA (`:155-173`). Grep de `cerrada` en ese fichero: solo `:131` y `:267`, ninguno con swaps. |
> | a3 | importa | **Varios pasajes del informe contradicen ya la fase 2 y no están marcados como sin efecto.** §7 deja sin efecto la regla D2, la frase del bloque, §1 punto 2, §2 y la línea F. Siguen vigentes en el texto, sin marca: H1 «H sigue viva y R5.2 no cambia» y H8 «No sale HECHA», cuando §0.g dice ahora que H sale HECHA y que R5.2 pierde `NA:H`; §0.i «(c2) no se implementa»; la fila 42 de §0.h; y en §5 la fila 4 («ADR-0091 no se crea») y la fila 24 («22.794 bytes»). El informe no es un informe cerrado, así que se puede corregir. | SELLO-RESPALDO-M1.md:325, :327, :333, :355, :524, :544, frente a :281 («**H sale HECHA**») y :305 (R5.2 sin `NA:H`). Lista de lo que queda sin efecto: :767-773. |
> | a4 | menor | **`prototipo_sello.py`, que d) toca, no pasa `ruff check`: 6 errores E501.** Vienen de la fase 0: el lint de `make check` solo cubre `src tests scripts .claude/hooks`. Aun así, la respuesta pide «ruff format, ruff check y mypy sobre lo tocado». | `uv run ruff check docs/validation/anexos/SELLO-RESPALDO-M1/prototipo_sello.py docs/validation/anexos/SELLO-RESPALDO-M1/simular_cierre.py` → «Found 6 errors» (líneas 1, 7, 14, 17, 26 y 32). `git show 460595f:…/prototipo_sello.py \| head -1` ya traía la línea 1 larga. `Makefile:36-37`. |
> | a5 | menor | **El docstring del módulo `test_respaldo_m1_decision.py` sigue diciendo que «los ocho del primer bloque ROMPEN en `main`».** Dos de esos ocho, los de la secuencia reescritos a media vela, pasan ahora en el `main` actual. El párrafo añadido lo matiza, pero no corrige la frase. | `tests/unit/test_respaldo_m1_decision.py:8` frente a §7.2 (SELLO-RESPALDO-M1.md:811-813: «Pasan en `main` y en la rama: los dos de la secuencia»). |
>
> Comprobado sin hallazgos:
> - **El contrato.** `uv run python scripts/contrato_rama.py`: «CONTRATO: 46 ficheros dentro del contrato de trabajo/sello-respaldo-m1 (riesgo alto, artefacto docs/validation/SELLO-RESPALDO-M1.md, tramo 'R3 · Una corrida del arnés sobre toda la construcción', 4 comprobaciones para el revisor)», exit 0. `rutas_permitidas` cubre src/botsito/engine/, tests/, los cinco ADR y el índice.
> - **Las comprobaciones del contrato.**
>   - `uv run botsito state check`: OK, exit 0.
>   - `knowledge validate`, a stdout: todo OK, con los dos AVISO de siempre, exit 0.
>   - `make check`: no lo corrí. `make-check.log`: «3249 passed in 1230.51s», «SELLO: … 27ef41ab5f94e53122c60380a93e73ab7d22f329», «PICO DE MEMORIA … 308 MiB». `git rev-parse` de los árboles da cdffbfb = 7dbf0937…, 3252548 = 9ede7820… y 7eda14d = 27ef41ab…, como dice la tabla de §7.4.
>   - **El punto d) todavía no tiene sello**: le falta su `make check`.
> - **Trailers `Fuente:`.** `git log … main..HEAD -- knowledge/spec knowledge/cases` sale vacío.
> - **Holdout.** Ningún fichero de holdout. `casos_reservados(repo)`, contado por mí: 34 en total, los 34 con el prefijo `caso-eurusd-2026-`; 0 en los once días y en 2026-08-07; 0 en enero, abril, julio y agosto.
> - **Regímenes de cambio.**
>   - `git diff --name-status main...HEAD` sobre knowledge/, data/manifests/, .claude/, Makefile y tools/: vacío.
>   - HISTORIA.md: 164+/0−. HOLDOUT-EXPOSICIONES.md: 2+/0− commiteado y 1+/0− sin estadiar.
>   - Los ADR 0051, 0057, 0068 y 0083 solo ganan recuadros (13, 6, 8 y 9 líneas, ninguna borrada), junto al pasaje que corrigen.
> - **ADR.** 0091 tiene `## Estado` = `ACTIVE`; `test_adr.py`, `test_hoja_de_ruta.py` y `test_project_state.py` pasan (exit 0). El índice tiene la fila 0091 y las cuatro de los ADR enmendados.
> - **Informes cerrados.** No cambia ninguno.
> - **Tres guardias de una `cita`.** No aplica.
> - **Cifras.** El código solo añade `± 1` ms estructurales; no entra ningún literal de negocio.
> - **Ensayos.**
>   - `git worktree list` ya solo muestra el repo; `git branch -a` da main y la rama; hay 150 tags.
>   - `prototipo_sello.py` comprueba que la carpeta de páginas queda fuera del repo (`:257-258`).
>   - `simular_cierre.py` escribe solo en un `TemporaryDirectory`.
> - **Citas comprobadas contra su fuente.**
>   - RESPALDO-M1.md:485: «Hecho cuando: … las dos corridas están repetidas».
>   - DECISIONES-DE-PROCESO.md:29: la regla de la letra reutilizada, con fecha.
>   - ENTRADA-ENERO.md:635: el contrato ampliado con un ADR en una fase posterior.
>   - El docstring de `minuto_de_apertura` frente a `_sesion_de` (`cableado.py:828-834`).
> - **CRLF.** `simular-cierre.txt` lleva CRLF en la copia de trabajo (5 CR), pero `.gitattributes` tiene `* text=auto eol=lf`: se guarda con LF en el índice.
>
> ### Eje (b) · La respuesta del consultor a la PARADA
> Resumen: 0 bloquea, 2 importa, 2 menor. Requisitos: 14 hechos, 2 parciales, 0 no hechos, 1 pendiente (d) y 1 en curso (este revisor).
>
> | # | Requisito | Estado | Evidencia |
> |---|---|---|---|
> | 0 | (c2) en esta rama, fase 2; lo que queda sin efecto, por escrito; el contrato ampliado en su commit; el bloque `ids-inexistentes` sale en el commit del ADR; riesgo alto | Hecho (ver a3) | §7:767-773; cdffbfb toca `contrato.yaml`; el grep de `ids-inexistentes` en HEAD solo da menciones narrativas; `contrato.yaml:2` |
> | 1 | Neutralidad completa: los tres de diagH, el swap y el día local con `(abierta_ms+1)//60000`; comisiones y criterio en el sellado; test de S9; los de `cerrada_ms`, cada uno con su porqué en el ADR | **Parcial** | Código: `broker.py:284`, `:943`, `:975`, `:1106`; `cableado.py:470`; `primitivas_broker.py:281`; comisiones en `:1122-1125` y criterio en `cableado.py:479`, sin tocar. Los de `cerrada_ms`, en ADR-0091 §3. Faltan lectores de `abierta_ms` en el ADR: b1 |
> | 2 | S4 y S5 aceptados; NOTA en ADR-0068 §2; tests | Hecho | ADR-0091 §5; el recuadro de ADR-0068; `test_sello_respaldo.py:108-152`, los dos FAILED en `tests_rama_con_main.txt` |
> | 3 | La versión anterior se queda, con NOTA en ADR-0051 §5 | Hecho | recuadro en ADR-0051; ADR-0091 §6 |
> | 4 | Los dos tests de secuencia a media vela, y uno nuevo en el cierre | Hecho | diff de `test_respaldo_m1_decision.py` (`_ms(M0, 30)`, `_ms(M0+1, 30)`); `test_en_el_cierre_la_vela_se_evalua_antes…`, FAILED en main |
> | 5 | Bastan los once días; ninguna corrida ni cifra agregada | Hecho | Grep de `motor arnes\|--todos\|--meses\|diagnostico-cuenta-diaria` en los anexos: nada. `prototipo_sello.py:273-276` solo llama a `motor visor --caso … --simular`. El «27 en 11 días» es lo que autoriza el punto 7 |
> | 6 | ADR-0083 D2 con test propio, y el punto en el ADR con fichero:línea de `cableado.correr_dia` | **Parcial** | Los dos tests (`test_sello_respaldo.py:250-295`) rompen en main. El fichero:línea del ADR no cuadra: b2 |
> | 7 | ADR-0091 ACTIVE, recuadros en los cuatro, filas del índice, alcance sin cifra de mes, el bot en vivo con ticks | Hecho (ver a1) | ADR-0091:12-13 y §7; diff de README.md |
> | 8 | Los once días, con el código de la rama, dan lo que dio el prototipo | **Hecho, comprobado** | `verificacion-rama.txt` frente a `prototipo-c2.txt` sin las líneas `#`, `OK:` y `TIEMPO`: 310 líneas cada uno, iguales (`a==b True`, diff vacío). 11 secciones `## `, 11 `OK:`. `comparar_formas.py` main frente a rama, vuelto a correr: 2761 bytes, como `censo-main-rama.txt`, que solo difiere de `censo-main-c2.txt` en el nombre del fichero. Operaciones distintas solo en 01-23 (venta, M1 11:03Z, −1.00) y 07-10 (compra, M1 05:27Z, −1.00) |
> | 9 | Los tests que rompen en main pasan en la rama, con la salida pegada; los dos de secuencia pasan en los dos lados | Hecho (ver b4) | `tests_rama_con_main.txt`: 17 FAILED (6 nuevos, 8 del ms, el del cierre y los 2 de (e2)). En la rama, los 7 ficheros con `test_punto_usado` dan exit 0 |
> | 10 | Las líneas del cierre probadas sobre una copia, por debajo de 23.000 | Hecho | Vuelto a correr: «H viva en la copia? False; H HECHA en HISTORIA? True; NA:H en la hoja simulada? False / a: [] b: [] c: [] / 21860 bytes …; 21986 …; ok», igual que `simular-cierre.txt` |
> | 11 | La fila de ERRORES-RECURRENTES con los errores del consultor | Hecho | §3:476: (1) corregida con la fecha del 2026-10-29, (2) en la columna del consultor, (3) y (4) nuevas |
> | a | El contrato ampliado, sellado | Hecho | cdffbfb, árbol 7dbf0937… |
> | b | ADR y recuadros; sale el bloque | Hecho | 3252548, árbol 9ede7820… |
> | c | Funciones y lectores, con los tests | Hecho | 7eda14d, árbol 27ef41ab… = el SELLO de `make-check.log`, 3249 passed |
> | d | La verificación, el informe con §0.g y §3 reescritos, las líneas probadas | Pendiente | `git status --short`: 6 M y 2 ??, sin estadiar ni sellar |
> | CI | Sin fix/ | Hecho | La rama no toca .claude/, Makefile, tools/, hooks ni plataforma |
> | Rev | El revisor, con su informe pegado | En curso | Es este informe; §8 sigue con «REVISOR2» |
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | b1 | importa | **Alcance 4: ADR-0091 no decide todos los lectores de `abierta_ms` de src/botsito/engine/.** §2 decide los cinco que pasan a `minuto_de_apertura` y los que se quedan en el instante sellado (comisiones, criterio, apertura de la `Operacion`, visor, «### Ordenes»). Faltan cuatro: **`_mover`** (`vigente_desde = p.abierta_ms`, la versión anterior del stop); **`_proximo_evento`**, con su `desde` (`max(ahora−1, abierta_ms, …)`) y su `decidido = p.abierta_ms`, que lo excluye de la vela del llenado; **`_marcar_hasta` → `_peor_del_minuto(…, p.abierta_ms, …)`** (el filtro de ticks); y las claves de orden de `cableado.py`. §0.e del informe sí los nombraba. «Lo que no cambia» del ADR («el «ahora − 1», la vela de la salida tras un llenado») cubre `:793` de forma implícita, pero ni `:725`, ni `:795`, ni `:945`. Por mi lectura, los tres son neutros (`_nivel_de_la_vela` compara `inicio >= decidido`, y k fin − 1 sigue por debajo del inicio de k+1), pero el ADR no lo dice ni da su porqué. | Grep de `abierta_ms\|cerrada_ms\|minuto_de_apertura` en src/botsito/engine: `broker.py:725`, `:793`, `:795`, `:945`; `cableado.py:469`, `:689`. ADR-0091:30-51 y :143-144. `llenado.py:140-142`. |
> | b2 | importa | **Los fichero:línea de `cableado.py` en ADR-0091 son los de main, no los del código que el ADR describe.** 7eda14d añade `minuto_de_apertura,` en `cableado.py:52`, y todo lo de debajo baja una línea. El punto 6 pedía expresamente «fichero:línea de cableado.correr_dia», y es justo la lección heredada de RESPALDO-M1.md:494. §7.1, fila 6, repite las mismas líneas. | ADR-0091:22 `:302` (en la rama, `hasta_ms` está en `:303`); :74-75 `:304`, `:305` y `:307` (en la rama, `broker.avanzar` en `:305`, `_a_la_cuenta` en `:306` y `_el_punto_tras_el_evento` en `:308`); :84 `:355` (en la rama, `fin_ms` en `:356`). `git show main:src/botsito/engine/cableado.py \| sed -n '302,307p;355p'` da las líneas que cita el ADR. SELLO-RESPALDO-M1.md:785. |
> | b3 | menor | **ADR-0091 §4 remite a «la verificación de §7»**, y el §7 del propio ADR es «Alcance medido». La verificación está en SELLO-RESPALDO-M1.md §7.3. | ADR-0091:73 frente a ADR-0091:100. |
> | b4 | menor | **El punto 9 pide la salida «pegada», y §7.2 solo nombra los tests con una tabla.** La salida está solo en el anexo, que además no trae la línea de resumen de pytest: los 17 salen de contar las líneas FAILED. En la fase 0 sí se pegó un extracto (§0.f:258-266). | SELLO-RESPALDO-M1.md:802-809; `tail -3 tests_rama_con_main.txt`: la línea de puntos y FAILED, sin «17 failed». |
>
> Lo que la rama hace y la respuesta no pide, declarado:
> - `test_peor_del_minuto.py` se reescribe en 7eda14d. Con (c2), la sonda 5 rompe en main ya por el milisegundo, y quien sigue fijando (e2) es la S7b. Está dicho en §7.2:815-817.
> - `minuto_de_apertura` es una función única. Está dicho en §7.1, fila 1.
>
> Lo que la respuesta dice que no se toca: knowledge/, strategy_spec, parametros, ADR-0053, corpus y holdout. Ninguno aparece en `git diff --name-status main...HEAD`.
>
> ### Lo que no pude comprobar
> - **El `make check` del árbol final del punto d)**: escribe. Hace falta antes del commit de d).
> - **Que los clones `C:/cm/r` y `C:/cm/m` fueran como los describe la fila de exposiciones**, y qué dieron en `C:/cm/r` los 29 ficheros de §4.1: el informe no lo registra y los clones ya no existen.
> - **Que `verificacion-rama.txt` salga de una ejecución real con el código de 7eda14d**: no volví a correr el visor, como se me indicó. Lo apoya que coincide byte a byte con `prototipo-c2.txt` sin las cabeceras, y que `prototipo_sello.py` no parchea nada en la forma `rama` (`aplicar`: `if forma in ("main", "rama"): return`).
> - **Una sospecha sin demostrar:** con el sello en k fin − 1 = `ahora`, el «ahora − 1» de `_proximo_evento` (`broker.py:777`, `:793`) hace que el `avanzar` siguiente vuelva a evaluar la vela k para las órdenes y posiciones que no cambiaron. Por mi lectura da siempre el mismo resultado (misma vela, mismo nivel, mismo `decidido`), pero no lo he medido, y el ADR dice que el «ahora − 1» «no cambia».
> - **El efecto de a1 con ticks reales** (cuántos llenados por tick caen en .999): necesitaría datos y una corrida.
>
> ### Comandos ejecutados
> 1. `git branch --show-current`; `git merge-base main HEAD`; `git log --format='%h %s' main..HEAD`; `git diff --stat main...HEAD`; `git status --short`
> 2. Read: el encargo, `contrato.yaml` y `SELLO-RESPALDO-M1.md` entero
> 3. `uv run python scripts/contrato_rama.py`; `uv run botsito state check`
> 4. `git diff --stat`; `git diff` de HOLDOUT-EXPOSICIONES.md, el README, `simular-cierre.txt` y `prototipo_sello.py`
> 5. `wc -l` y `head -12` de `verificacion-rama.txt` y `prototipo-c2.txt`; comparación en memoria sin cabeceras (`uv run python -c`, difflib)
> 6. `grep` de `^## `, `^OK:` y de las líneas con R en `verificacion-rama.txt`; `cat censo-main-rama.txt`
> 7. `head -30` y `grep` de IO de `comparar_formas.py`; `uv run python -B …/comparar_formas.py prototipo-main.txt verificacion-rama.txt` (a /dev/null y a `wc -c`; el `| diff -` lo negó la guardia y no lo rodeé); `wc -c` y `diff censo-main-c2.txt censo-main-rama.txt`
> 8. `git diff main...HEAD -- src/`; Grep de `abierta_ms|cerrada_ms|minuto_de_apertura` en src/botsito/engine; Grep de `_sesion_de`
> 9. Read: ADR-0091 entero; `broker.py:715-804`, `:828-855`, `:855-902`, `:900-989`, `:1110-1144`; `cableado.py:296-359`; `llenado.py:134-157`; `prototipo_sello.py:186-205` y `:240-287`; `simular_cierre.py`; `tests/unit/test_sello_respaldo.py`; `.gitattributes`
> 10. `git diff main...HEAD` de los cuatro ADR enmendados y del índice; `git diff main...HEAD` de los cuatro ficheros de test reescritos; `git diff dacd533 7eda14d -- tests/unit/test_peor_del_minuto.py`
> 11. `grep FAILED/passed`, `head` y `tail` de `tests_rama_con_main.txt`
> 12. `uv run pytest -p no:cacheprovider -q` de test_sello_respaldo, test_broker, test_broker_ordenes_stop, test_llenado, test_respaldo_m1_decision, test_peor_del_minuto y test_punto_usado (exit 0); y de test_adr, test_hoja_de_ruta y test_project_state (exit 0)
> 13. `grep SELLO|PICO|passed|failed make-check.log`; `git rev-parse` de los árboles de cdffbfb, 3252548 y 7eda14d; `ls -la make-check.log`
> 14. `git diff --name-status main...HEAD` sobre knowledge/, data/manifests/, .claude/, Makefile, tools/, docs/validation/, docs/state/ y docs/adr/; `git log … -- knowledge/spec knowledge/cases`; `git diff --numstat` de HISTORIA, HOLDOUT-EXPOSICIONES y los ADR
> 15. `git worktree list`; `git branch -a`; `git tag -l | wc -l`
> 16. `grep` de las operaciones de escritura en `simular_cierre.py`; `uv run python -B …/simular_cierre.py`
> 17. Recuento de CR con Python en siete ficheros de los anexos (el `grep -c -U $'\r'` lo negó la guardia; el `git config` lo negó solo_lectura)
> 18. Comparación con Python de las dos copias de la respuesta del consultor (encargo e informe): iguales, 6124 caracteres cada una
> 19. `uv run python -c` con `casos_reservados`, solo recuentos
> 20. `git show --stat` de cdffbfb, 3252548 y 7eda14d; `git grep ids-inexistentes HEAD -- …`
> 21. Grep en el informe de «No sale HECHA|H sigue viva|22.794|no se implementa|no se crea|Va al borrador»
> 22. `sed` de RESPALDO-M1.md:483-487, DECISIONES-DE-PROCESO.md:29 y ENTRADA-ENERO.md:633-637
> 23. `git diff main...HEAD -- PROJECT_STATE.md`; `wc -c PROJECT_STATE.md`
> 24. `uv run botsito knowledge validate` (a stdout)
> 25. `uv run ruff check` y `ruff format --check` de `prototipo_sello.py` y `simular_cierre.py`; `git show 460595f:…/prototipo_sello.py | head -1`; `grep ruff|lint Makefile`
> 26. `git show main:src/botsito/engine/cableado.py | sed -n '302,307p;355p'`; `git show 3252548:… | sed -n '304,307p'`
>
> ### Lo que la sesión tiene que declarar de esta pasada (no lo puedo escribir yo)
> - **Salidas del prototipo.** Leí `verificacion-rama.txt` y `prototipo-c2.txt` (cabeceras, la comparación en memoria y un grep de las líneas con R) y `censo-main-rama.txt` y `censo-main-c2.txt`. Son órdenes y operaciones con instantes y R, por día, de los once días dev, sin precios.
> - **Guiones.** Ejecuté `comparar_formas.py` (main frente a rama) y `simular_cierre.py` (PROJECT_STATE, la hoja de ruta y HISTORIA en memoria, con una copia temporal fuera del repo).
> - **Recuentos.** Conté `casos_reservados`, solo recuentos: 34 en total; 0 en los once días, en 2026-08-07 y en los cuatro meses.
> - **Tests y validación.** Ejecuté pytest de diez ficheros (sintéticos, con la spec y el registro reales en `test_punto_usado` y en los tests del cableado) y `knowledge validate`.
> - **Lecturas.** Leí `tests_rama_con_main.txt`, `make-check.log` (grep), el código de src/botsito/engine, los ADR 0051, 0057, 0068, 0083 y 0091, y tres pasajes de RESPALDO-M1.md, DECISIONES-DE-PROCESO.md y ENTRADA-ENERO.md.
> - **Lo que no toqué.** Ningún holdout, corpus, cruda, fotograma, libro, caso ni diagH; ningún listado de `knowledge/cases`; ninguna corrida del arnés.

### 8.1 Lo que se hizo con los hallazgos de la segunda pasada

| # | Gravedad | Qué se hizo |
|---|---|---|
| a1 | importa | **Arreglado en el texto**: la cabecera de ADR-0091, su §2, la fila del índice y el recuadro de ADR-0051 dicen ahora que el SELLO solo cambia los minutos sin ticks y que, con ticks, lo único que cambia es el «+ 1» de `minuto_de_apertura` en un llenado por tick en el ms .999 (su sesión, su swap, su día y la marca de ese minuto), sin medir. Los recuadros de ADR-0068 y ADR-0083 hablan solo del sello, y para el sello «con ticks no cambia nada» es cierto: no se tocan. El código sigue la letra de la respuesta (punto 1: «leen (abierta_ms + 1) // 60000»); limitar el «+ 1» a las aperturas del respaldo sería una desviación, y queda para el consultor si la quiere |
| a2 | importa | **Arreglado**: `test_una_salida_en_la_ultima_vela_antes_del_corte_no_paga_ese_swap` (rompe en `main`, que lo pagaba; pasa en la rama) y ADR-0091 §3 lo nombra |
| a3 | importa | **Arreglado**: H1, H8, la fila 42 de §0.h, §0.i y las filas 4 y 24 de §5, cada una con «Sin efecto desde la fase 2 (§7)» y lo que vale ahora |
| a4 | menor | **Arreglado**: `prototipo_sello.py` lleva `# ruff: noqa: E501` a nivel de fichero, como `simular_cierre.py` (las líneas largas son el comando de uso y rutas literales); `ruff check` de los dos, en verde. `censo_cierre.py` y `comparar_formas.py` (fase 0, no tocados en d) conservan una línea larga cada uno: el lint de `make check` no cubre `docs/` |
| a5 | menor | **Arreglado**: el docstring dice que los ocho rompían en el `main` de antes de `trabajo/respaldo-m1`, y que contra el de ADR-0091 los dos de la versión anterior pasan |
| b1 | importa | **Arreglado**: ADR-0091 §2 lleva una lista nueva, «Leen `abierta_ms` y no cambian, sin tocarlos», con `_proximo_evento` (`desde` y `decidido`), `_mover` (`vigente_desde`), el filtro de ticks de `_peor_del_minuto` y el orden de las posiciones del cableado, cada uno con su porqué |
| b2 | importa | **Arreglado**: las líneas de `cableado.py` en ADR-0091 son las de la rama (`:303`, `:305`, `:306`, `:308`, `:356`), y el «Impacto» lo dice; §7.1, fila 6, también |
| b3 | menor | **Arreglado**: ADR-0091 §4 remite a SELLO-RESPALDO-M1.md §7.3 |
| b4 | menor | **Arreglado**: los 18 FAILED pegados en §7.2, con la línea de resumen (`18 failed, 39 passed`), de una ejecución repetida en un clon de `main` nuevo (`C:/cm/m`, ya retirado) |

**La sospecha del «ahora − 1»**: escrita en el «Impacto» de ADR-0091 con su porqué (la misma vela,
el mismo nivel y el mismo `decidido` dan lo mismo, y lo decidido en el cierre lleva su instante en
`desde`), y declarada sin test propio. **Lo que no pudo comprobar de los clones**: `C:/cm/r` corrió
los 29 ficheros de §4.1 con (c2) escrito a mano y dio los mismos 10 rotos de §0.d, más la sonda 5 de
la rama, que entonces cerraba en el sello viejo (se reescribió en 7eda14d); no se guardó a fichero.

## Estado

Fase 0 (460595f), fase 1 ((e2), dacd533) y fase 2 ((c2) con ADR-0091: cdffbfb, 3252548, 7eda14d y el commit del informe) hechas. D2 dio (c2) y la respuesta del consultor del 2026-11-07 lo mandó implementar aquí; los once días verificados dan lo que dio el prototipo. Ninguna corrida del arnés ni cifra agregada.

Rama lista para revisión, NO cerrada.
