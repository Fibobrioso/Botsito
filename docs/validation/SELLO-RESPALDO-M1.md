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

En el caso que dio D2, (c2). Simuladas con `simular_cierre.py` (en memoria, contra
`test_hoja_de_ruta` y `test_project_state`; `simular-cierre.txt`): `a: [] b: [] c: []`, los cuatro
tests de `test_project_state` en verde y **PROJECT_STATE en 22.794 bytes** (por debajo de 23.000).
Esa cifra lleva el Current Feature de la rama (125 bytes); el que escribe el cierre, con la forma
del de main, medía 263: **unos 22.930 bytes** tras el cierre, todavía por debajo de 23.000 con un
margen de unos 70 (revisor, b7).

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

Cuatro columnas, como la tabla de destino (`ERRORES-RECURRENTES.md:50`; revisor, b8): la del
revisor resume §6; la del consultor después la rellena el cierre; la última lleva lo que el encargo
pide y lo aprendido.

| `trabajo/sello-respaldo-m1` | Una pasada, opus, sobre dacd533 más el informe sin estadiar, con los cinco alcances del encargo (SELLO-RESPALDO-M1.md §6; lo hecho, §6.1). Reglas: 0 bloquea, 1 importa, 1 menor; encargo: 0 bloquea, 5 importa, 3 menor. Arreglados: a1 (el clon sin declarar en la fila de exposiciones), b1 (los lectores de `cerrada_ms`, del minuto del evento y del resultado de `_peor_del_minuto`), b2 (la marca mueve también el margen libre), b3 (ADR-0083 D2 sin contrastar), b4 (las líneas de main frente a las de la rama), b5 (la regresión sin la lista de ficheros) y los cuatro menores | (los rellena el cierre) | (1) **(importa, del consultor)** el plan del 2026-11-01 mandaba a H "las dos corridas del arnés", y R3.7 pide fijar los umbrales de R antes de ver ninguna corrida nueva. Lección: antes de mandar una corrida, mirar si hay un umbral pendiente de pre-registrar. (Nota del auditor: en el repo, esas dos corridas vienen de la respuesta del 2026-10-29, RESPALDO-M1.md:485; no hay un plan del 2026-11-01.) (2) **(Del consultor)** El encargo llamó «eventos del respaldo» a 22 cancelaciones del bot, y mandó sacarlos de una salida (la diaria de RESPALDO-M1) que no es la que los contó y que tiene, aparte, 22 eventos del respaldo de verdad. Lección: una cifra heredada se cita con QUÉ cuenta y SOBRE QUÉ salida, y una lista que va a decidir algo se saca del código vigente, no de una salida vieja. Señal: el mismo número en dos sitios con nombres distintos. (3) **Una lista vieja solo elige días**: la de RESPALDO-M1 daba 26, y main da 27 en esos días, con ids renumerados; el censo se hizo con el visor sobre main. (4) **La guardia y los prototipos en memoria**: `exec` de una fuente, `git apply`, `sys.path` calculado, `PYTHONPATH` y `spec_from_file_location` con la ruta por parámetro se niegan; las formas que pasan son funciones literales escritas en el guion, Edit en el clon y rutas literales en la llamada. Señal: un prototipo que parchea por texto. |

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
| 4 | grep de «0091» en docs/ y en Technical Debt antes de usar el número | Hecho (el auditor, 6): solo en el encargo; los demás «0091» de docs/ son ids `ev-v15-000913-…` y precios. ADR-0091 no se crea (D2 dio (c2)); este informe lo cita en el borrador con su bloque `ids-inexistentes` | §0.h; cabecera |
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
| 24 | g) las líneas del cierre sobre una copia, con test_hoja_de_ruta y test_project_state y la previsión de bytes < 23.000 | Hecho: 22.794 bytes | §0.g; `simular-cierre.txt` |
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

## Estado

Fase 0 entregada (460595f); D2 dio (c2): **PARADA con el plan** (§2), con seis decisiones para el
consultor. Fase 1 hecha en lo que el encargo deja hacer con (c2): (e2) y su test (dacd533). ADR-0091
no se crea. Ninguna corrida del arnés ni cifra agregada.

Rama lista para revisión, NO cerrada.
