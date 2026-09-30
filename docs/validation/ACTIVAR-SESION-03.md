# Activar la sesión 3 en knowledge

Rama `trabajo/activar-sesion-03`, desde `main` en `5f0903a` (`stable/F30-sesion-03`). Brief del
consultor del 2026-09-29. **Solo knowledge, spec y la documentación que se regenera: ninguna línea
del motor cambia.** Lo que la spec dice ahora y el motor todavía no hace queda en el §3, como lista
de trabajo para las ramas de código.

Se activa lo que `SESION-03-EXTRACCION.md` marcó «resuelve» y, de lo marcado «en parte», solo lo
que el consultor enumeró como firme. Todo por las dos vías del runbook `SESION-DE-PREGUNTAS.md`:
un registro de feedback por respuesta (sesión `2026-09-29-sesion-03`, 24 registros, procedencia
`trader_grabado`, grabación v9) y `feedback apply` para los parámetros. Los textos de las reglas
cambian solo en la prosa (`notas`): **ninguna `forma` se toca**, porque cambiar una forma es cambiar
lo que el motor ejecuta.

## 1. Lo activado, código a código

| Código | Qué dijo el trader | Dónde queda (RN o parámetro) | Registro |
|---|---|---|---|
| A-47 | se entra siempre por stop | `entrada_tipo_orden` = `stop_en_ruptura` (UNKNOWN → CONFIRMED); A-47 RESUELTA; notas de RN-006 y RN-011 | fb-2026-09-29-sesion-03-92a38105 (A-47), fb-2026-09-29-sesion-03-8f091ed8 (parámetro) |
| A-34 | con la doble ruptura decide el color de la vela | RN-003 (CORRECT, notas); A-34 RESUELTA | fb-2026-09-29-sesion-03-617f496a, fb-2026-09-29-sesion-03-31fb311f |
| S-1 | siempre hay sesgo; doble ruptura: el color; toda operación se cierra un minuto antes del fin de su vela H4 | RN-033 (CORRECT), RN-003 (CORRECT), RN-002 (CORRECT) | fb-2026-09-29-sesion-03-1168f036, fb-2026-09-29-sesion-03-31fb311f, fb-2026-09-29-sesion-03-c38c4aef |
| A-26 | manda el sesgo; en M15, solo a favor | notas de RN-005; A-26 RESUELTA | fb-2026-09-29-sesion-03-fc2c5c1f |
| A-46 | cada sesión es un mundo aparte; no importa cómo acabó la primera; sin tope de escenarios | A-46 RESUELTA (el hecho `liquidez_tomada` no se toca: §3) | fb-2026-09-29-sesion-03-5021677e |
| A-45 | la toma la hace una vela de M1 que cierra con cuerpo pasado el nivel de M15 | `liquidez_m15_criterio_toma` = `cuerpo` confirmado; notas de RN-004; A-45 RESUELTA | fb-2026-09-29-sesion-03-b2e074e3, fb-2026-09-29-sesion-03-43e0f90e |
| A-40 | después del break even el stop se queda quieto | notas de RN-014; A-40 RESUELTA | fb-2026-09-29-sesion-03-7a79dcd7 |
| A-13, lo firme | break even al tocar, en M1, exactamente en la entrada | `break_even_criterio_ruptura` = `mecha` (DEFAULT_AMBIGUOUS → CONFIRMED, mismo valor); RN-014 (CORRECT). **A-13 sigue ABIERTA** | fb-2026-09-29-sesion-03-2cff5008, fb-2026-09-29-sesion-03-9f506366 |
| G-1 | no cierra a mano antes del stop | RN-015 (CONFIRM) | fb-2026-09-29-sesion-03-280cf8f7 |
| G-2 | no deja correr: el objetivo es fijo | RN-015 (CONFIRM) | fb-2026-09-29-sesion-03-3f69a5f7 |
| A-18, lo firme | objetivo = 3 × la distancia 0 → 1; lote del 0 al 0,8; el 0,8 se redondea alejándose de la entrada | `base_calculo_objetivo` y `lotaje_base` confirmados; **`stop_fraccion_redondeo` nace** = `alejandose_de_la_entrada`; notas de RN-011 | fb-2026-09-29-sesion-03-f572f1a0, fb-2026-09-29-sesion-03-d62c788a, fb-2026-09-29-sesion-03-11910e0a |
| G-3 | no hay tamaño mínimo ni máximo de caja | **nada que activar**: la spec no tiene ningún filtro de tamaño, así que ya dice lo mismo | — |
| A-31 | el stop entero de una activación sin ruptura gasta un intento | notas de RN-016 (era lectura nuestra; ahora es del trader); A-31 RESUELTA | fb-2026-09-29-sesion-03-d36ba0d2 |
| E-3 | una vela casi plana no cuenta: sobre ella no se traza punto de breaker | RN-007 (CORRECT, notas nuevas) | fb-2026-09-29-sesion-03-ffab23dc |
| A-41 | tres intentos por liquidez, sin tope por día | `cartuchos_max` = 3 confirmado; notas de RN-016; A-41 RESUELTA | fb-2026-09-29-sesion-03-7b87c3ee, fb-2026-09-29-sesion-03-68a21dc0 |
| A-38 | la orden sigue viva hasta el siguiente posible punto de breaker | notas de RN-006; A-38 RESUELTA | fb-2026-09-29-sesion-03-c7fa3068 |
| A-37 | la vela contraria del stop se mira en M1 | notas de RN-011; A-37 RESUELTA | fb-2026-09-29-sesion-03-91eeee94 |
| A-42, PROVISIONAL | las sesiones 07–11 y 11–15 van fijas en el reloj del gráfico (UTC+2) todo el año; en invierno equivalen a 06:00–14:00 de Madrid | **decisión PROVISIONAL, ADR-0059** (recuadro en ADR-0017), **sin cambiar `huso_operativa`**: en el motor es también el reloj del día de riesgo, y separarlos es rama de código (desalineación 9). **A-42 sigue ABIERTA y bloqueante** («el trader dijo "creo"; confirmar en la próxima sesión») | ninguno: la fuente son `ev-v9-010753-063c8cb7`, `ev-v9-010809-68e4ea44` y el tramo de A-42 solo con máscara |

**CORRECT, dicho expresamente, como pidió el consultor.** Ningún parámetro CONFIRMED cambia de
valor en esta rama. El redondeo del 0,8 **no era un parámetro**: vivía en una línea de código,
`escribir_stop_en_la_orden` (`src/botsito/engine/primitivas_broker.py:306`), que calcula la
distancia con `ROUND_DOWN` y acerca el stop a la entrada. Así que no había nada CONFIRMED que
corregir con CORRECT. Nace `stop_fraccion_redondeo` (opciones `hacia_la_entrada` y
`alejandose_de_la_entrada`) y se resuelve con RESOLVE_UNKNOWN; el motor no lo lee (§3).
`break_even_criterio_ruptura` pasa de DEFAULT_AMBIGUOUS a CONFIRMED **con el mismo valor**, `mecha`.
CORRECT sí se usa sobre cinco reglas cuya prosa cambia de sentido: RN-002, RN-003, RN-007, RN-014 y
RN-033.

**Diez ambigüedades RESUELTAS**: A-26, A-31, A-34, A-37, A-38, A-40, A-41, A-45, A-46 y A-47, cada
una con su registro RESOLVE_UNKNOWN apuntando a ella (la guardia de `knowledge validate` lo exige).
A-47 era bloqueante y deja de serlo.

## 2. Lo que no se activó, y lo que se añadió sin activar

- **A-42 queda como decisión PROVISIONAL (ADR-0059), sin cambiar ningún valor**, por orden del
  consultor tras revisar el tramo con máscara (opción (a), fila del §1). Se probó a pasar
  `huso_operativa` a `Etc/GMT-2` y el motor se negaba a correr en invierno (8 tests en rojo; §3,
  desalineación 9), así que el cambio se deshizo. El texto sin máscara no está copiado en ningún
  sitio. **A-39**, sin tocar: su
  contenido firme (el cierre al vencer la vela H4) entra por S-1 en RN-002, pero la ambigüedad sigue
  ABIERTA por el corte de audio y por la orden pendiente. **A-13** sigue ABIERTA por el corte de
  57:00–58:06, con una nota de lo firme activado. **E-1** y **A-24**, sin tocar.
- **A-44 → A-51, nueva.** A-44 sigue ABIERTA, con una nota: la respuesta (9 pérdidas **seguidas**, sin
  porcentaje) no encaja en ningún `perdida_trader_*`, así que para (`ACTIVAR-A35-A44.md` §4). Nace
  **A-51**, «qué corta la racha de 9 pérdidas seguidas del trader y cuándo vuelve a operar»: ABIERTA,
  PREGUNTA, bloqueante de RN-020 como A-44, con `ev-v9-011128-a267338b` y `ev-v9-011139-a26a5b11`.
- **A-50, lectura candidata sin activar:** el trader no usa la posición de la caja frente al nivel
  tomado como filtro («no importa»). Anotada en la pregunta, con sus ítems.
- **A-21, lectura candidata sin activar:** zona limpia = sin alternancia de colores. Anotada en la
  pregunta. **No se añade al enum** `zona_control_limpia`: sus opciones tienen que coincidir con
  `LECTURAS_LIMPIA` del motor (`domain/estructura_m1.py`), y tocar eso es rama de código.

## 3. Desalineaciones entre knowledge y el motor: lista de trabajo para las ramas de código

Medidas en el código, no supuestas. Cada una dice qué afirma ahora la spec y qué hace el motor.

1. **RN-003 y RN-033, sesgo con doble ruptura y «siempre hay sesgo»** (A-34, S-1). La spec dice que
   decide el color y que no se deja de operar por un sesgo no claro. El motor, en `sesgo_h4_al_abrir`,
   fija `ambiguo` con la doble ruptura, y RN-033 prohíbe operar (15 sesiones de 84 en construcción,
   medido el 2026-09-25); `insuficiente` sigue existiendo (0 en construcción).
2. **RN-002, cierre un minuto antes del fin de la vela H4** (S-1). La spec dice 10:59 y 14:59 del
   gráfico. La forma cierra solo al alcanzar `ventana_fin` (15:00, en punto) y no cierra al vencer la
   primera vela de la ventana. Hace falta un predicado de fin de vela H4 sobre la rejilla de
   `anclaje_h4`. **No se toca `ventana_fin`**, que también decide qué sesiones se operan.
3. **El hecho `liquidez_tomada` no caduca al abrir la sesión** (A-46). Solo `sesgo` lleva
   `caduca: al_abrir_sesion`. Para el trader, cada sesión es un escenario propio.
4. **RN-004 evalúa la toma en la última M15 cerrada** (A-45). El trader la hace con una vela de M1
   que cierra con cuerpo. En `engine/primitivas.py` la vela que puede tomar el nivel es
   `ultima_m15_cerrada`, marcada PROVISIONAL por ADR-0054 §4.
5. **`stop_fraccion_redondeo` no lo lee nadie** (A-18). `escribir_stop_en_la_orden` redondea con
   `ROUND_DOWN`, hacia la entrada; el trader, al revés. El lote depende de esa distancia, así que
   cambia con ella. Declarado `consumido_por: [F21]`.
6. **RN-007, la vela casi plana** (E-3). El mapeo de M1 no la trata aparte, y el trader no dio el
   umbral de «casi plana».
7. **RN-006, la vida de la orden** (A-38). La spec dice que la orden sigue viva hasta el siguiente
   posible punto de breaker. Es la rama 3 de ADR-0056 (la vida de la orden stop), que no está hecha:
   **sin comprobar**.
9. **SEPARAR EL RELOJ DE LAS SESIONES (gráfico, UTC+2 fijo según A-42 provisional) DEL RELOJ DEL
   DÍA DE RIESGO (FTMO, Europe/Prague).** **Requisito previo de cualquier corrida sobre meses de
   invierno, incluida fidelidad-dev.** Hoy los dos son `huso_operativa` (`engine/motor.py`,
   `engine/simulacion.py`), y `engine/cableado.py` exige que su medianoche sea la de FTMO (ADR-0053
   §4). Medido en esta rama: con `huso_operativa` = `Etc/GMT-2`, el cableado se niega en invierno
   («no hay un solo reloj») y fallan 8 tests: 5 de `test_preparar_a44.py`, 1 de
   `test_perfil_cuenta.py` y 2 de `test_registro.py`. Los dos últimos solo fijaban ADR-0017. El
   cambio se deshizo (ADR-0059).
8. **A-43, sin activar pero desalineado ya**: el motor cuenta como toma dentro de la sesión la M15
   que cierra a las 07:00 (7 de 40 días con toma en construcción), y el trader dice que la toma tiene
   que ser dentro del horario.

**Alineadas, comprobado en el código:**
- **RN-014 y lo firme de A-13:** la forma mueve el stop a `OP.precio_entrada`, con
  `break_even_condicion` = `tocar`, sobre la zona de control de M1, y ninguna otra regla vuelve a
  mover el stop (A-40).
- **A-47:** `entrada_tipo_orden` lo lee el selector de ADR-0058 (PROVISIONAL), así que fijarlo cambia
  el tipo de orden que el motor coloca sin tocar el código. Medido en la CLI: con A-47 fijada, la
  corrida ya no se para en A-47 y se para en la siguiente puerta, la orden stop sin stops level
  (A-27, `firma_stops_level_puntos` UNKNOWN, ADR-0057), también antes de leer una vela.
- **A-42 (PROVISIONAL):** en construcción (días de verano) el motor ya opera en la ventana de la
  lectura nueva, porque UTC+2 es el huso de Madrid en verano. En invierno no, hasta la
  desalineación 9.
- **A-41 y A-31:** `cartuchos_max` = 3, `cartucho_criterio` y `cartuchos_reinicio` =
  `siguiente_liquidez_m15` ya cuentan por liquidez y gastan con el stop.
- **G-1 y G-2:** no hay ninguna regla de cierre manual ni de extensión (`objetivo_extension_activa` =
  false).

## 4. Las 20 diferencias grandes de VIABILIDAD-TRADER §4, frente a las reglas nuevas

Solo construcción: las 77 operaciones de los días `dev` de abril y agosto, cargadas con `cargar()`
de `scripts/viabilidad_trader.py` (el caso manda y el libro solo se lee por esos días). **No se
simuló nada**: se leyó, de cada operación, la hora de cierre anotada y su distancia al fin de la vela
H4 del gráfico (UTC+2 fijo: 11:00 y 15:00, que son 09:00 y 13:00 UTC), el R anotado sobre el stop
inicial y la distancia del cierre a la entrada.

| Categoría de §4 | n | Operación (llenado UTC) · cierre UTC · R anotado | Frente a las reglas nuevas |
|---|---|---|---|
| la anotada cierra a cero | 5 | 04-24 11:30 · 11:42 · 0,00 — 04-29 11:02 · 11:23 · 0,00 — 08-03 12:10 · 12:16 · 0,00 — 08-07 12:14 · 12:30 · 0,00 — 08-27 12:13 · 12:41 · 0,00 | **explicadas por el break even al tocar**: las cinco cierran **exactamente en la entrada, a 0 puntos**, que es el break even de la sesión 3 (a la entrada exacta, sin puntos para costes). Ninguna cerca del fin de la vela H4 (19 a 96 min antes) |
| las dos ganan, la anotada más allá de 3 R | 5 | 04-01 12:30 · 12:44 · +4,15 — 04-13 06:50 · 07:00 · +4,19 — 04-13 10:26 · 11:00 · +5,05 — 04-29 07:58 · 08:02 · +4,60 — 04-29 09:36 · 09:57 · +4,18 | **no explicadas; las contradicen**: con el objetivo fijo (G-2) no se llega a 4,2–5,1 R. Tampoco las explica el cierre de la vela H4: la más cercana cierra 15 min antes de las 13:00 UTC |
| la anotada gana y la simulada pierde, en la frontera | 2 | 04-06 06:34 · 06:50 · +4,69 — 08-07 05:14 · 05:29 · +5,33 | **no explicadas**: la diferencia es el bróker o la fuente (1 a 3 puntos). Además, la anotada pasa también de 3 R, contra G-2 |
| la anotada gana antes del objetivo | 2 | 04-09 07:12 · 07:32 · +2,94 — 08-03 09:52 · 10:17 · +2,50 | **no explicadas**: cierra antes del objetivo, lejos del fin de la vela H4 (87 y 78 min), contra G-1 y G-2 |
| una serie toca un nivel que la otra no | 4 | 04-22 08:02 · +3,00 — 08-26 05:49 · +3,00 — 04-14 12:06 · −1,00 — 08-21 11:56 · −1,00 | **no explicadas**: es la fuente (OANDA frente a Dukascopy, A-16) |
| las dos pierden, la simulada mucho más | 2 | 04-09 09:15 · −1,00 — 04-23 05:53 · −1,00 | **no explicadas**: llenado al tick y respaldo M1 |

**Cuántas quedan explicadas: 5 de 20**, todas por el break even al tocar, a la entrada exacta.
- El **cierre un minuto antes del fin de la vela H4 explica 0**: ninguna de las 20 cierra a menos de
  15 minutos de un fin de vela H4 de la ventana.
- El **objetivo = 3 × (0 → 1) explica 0**. Además, en 7 de las 20 la anotada pasa de 3 R (+4,15 a
  +5,33 R), lo que contradice lo que el trader dijo en G-2. Aunque el stop del libro fuera el 0,8 de
  la caja, el objetivo quedaría en 3,75 R, todavía por debajo.
- **Explicadas** quiere decir que el desenlace anotado es el que da la regla. Que la serie simulada
  también llegue a él exige simular el break even en el bróker, que es rama de código.

Esas siete son la diferencia más grande entre lo que el trader dice y lo que hace en su propio
backtest. Se anota para el consultor; aquí no se interpreta.

### 4.1 G-2 en las siete ganadoras de más de 3 R (revisión del consultor, 2026-09-29)

El consultor pidió medir, solo en construcción, la distancia de la entrada a la salida y el stop del
libro, las dos divididas por la caja 0 → 1, para ver si la salida cae en unas 3 cajas (compatible
con «objetivo fijo») o claramente más allá (el trader deja correr).

**La caja 0 → 1 de estas siete no está medida en ningún sitio.** El caso guarda solo la entrada y el
stop del libro (`initialSL`), y las 12 cajas leídas en pantalla (`BLOQUE-DE-LA-CAJA.md` §2.2) son de
los días 3, 4, 6 y 12 de agosto: ninguna de las siete. Lo que sí se sabe de esas 12 es que el stop
va en el 1 en seis y en el 0,8 en otras seis. Así que se da la medida con las dos posiciones del
stop, que son las dos cotas:

| operación (llenado UTC) | entrada → salida, puntos | stop del libro, puntos | salida / stop | si el stop es el 1: salida / caja | si el stop es el 0,8: salida / caja |
|---|---|---|---|---|---|
| 04-01 12:30 (`caso-eurusd-2026-04-01-1`) | 137 | 33 | 4,15 | 4,15 | 3,32 |
| 04-06 06:34 (`caso-eurusd-2026-04-06-1`) | 61 | 13 | 4,69 | 4,69 | 3,75 |
| 04-13 06:50 (`caso-eurusd-2026-04-13-2`) | 67 | 16 | 4,19 | 4,19 | 3,35 |
| 04-13 10:26 (`caso-eurusd-2026-04-13-4`) | 96 | 19 | 5,05 | 5,05 | 4,04 |
| 04-29 07:58 (`caso-eurusd-2026-04-29-2`) | 69 | 15 | 4,60 | 4,60 | 3,68 |
| 04-29 09:36 (`caso-eurusd-2026-04-29-3`) | 46 | 11 | 4,18 | 4,18 | 3,35 |
| 08-07 05:14 (`caso-eurusd-2026-08-07-1`) | 32 | 6 | 5,33 | 5,33 | 4,27 |

(Los puntos salen de las operaciones de construcción cargadas con `cargar()`; «salida / stop» es el R
anotado de §4.)

**Resultado.**
- **Si el stop del libro es el 1** (la caja es la distancia al stop), las siete salen entre 4,15 y
  5,33 cajas: **claramente más allá de 3**.
- **Si es el 0,8** (la cota más favorable a «objetivo fijo»), salen entre 3,32 y 4,27 cajas:
  - cuatro, **claramente más allá** (3,68 a 4,27: 04-06, 04-13 10:26, 04-29 07:58 y 08-07);
  - tres, **cerca de 3 sin llegar a cuadrar** (3,32 a 3,35: 04-01, 04-13 06:50 y 04-29 09:36).
- En ninguna de las dos lecturas las siete caen en unas 3 cajas.

**No cuadra con «objetivo fijo»: PENDIENTE PARA LA SESIÓN 4.** Antes de la sesión, y solo en
construcción: **medir la caja 0 → 1 de estas siete operaciones en sus fotogramas**, en el instante
de su colocación si está grabada, abriendo fotogramas solo por instante localizado (ADR-0038). Con
eso, la salida entre cajas deja de ser una cota y se lleva el dato a la sesión. Y preguntar al
trader por estas salidas sin enseñarle cifras de viabilidad. No se ha hecho aquí.

## 5. Tests que cambian a propósito

**Los que fallaron en la primera corrida, y por qué.** La suite se cortó por memoria al 69 %, con dos
tests en rojo. Lanzado solo el módulo sospechoso, `tests/unit/test_selector_orden_stop.py`, fallan
**tres**, y los tres porque A-47 ahora vale `stop_en_ruptura`:
- `test_el_selector_esta_en_el_registro_sin_valor_y_con_las_dos_lecturas` exigía UNKNOWN en el
  registro real;
- `test_sin_fijar_y_sin_diagnostico_se_niega_nombrando_a47` esperaba la negativa del registro real;
- `test_la_cli_con_simular_se_niega_sin_a47_antes_de_leer_velas` esperaba que la CLI nombrara A-47,
  y ahora nombra A-27, la puerta siguiente.

Se reescriben con el valor nuevo, y **la negativa se conserva con A-47 fijada a UNKNOWN de forma
explícita**, en una copia del registro real:
- el primero pasa a `test_el_selector_esta_en_el_registro_fijado_en_stop_y_con_las_dos_lecturas`,
  que además comprueba que el registro real corre con stop y rechaza el diagnóstico;
- el segundo y el tercero cargan esa copia; en el tercero, la CLI la recibe sustituyendo
  `cargar_registro` en el test;
- uno nuevo, `test_la_cli_con_a47_fijada_pasa_a_pedir_a27_antes_de_leer_velas`, fija lo que hace hoy
  la CLI con el registro real.

> **CORRECCIÓN (2026-09-29, `main`, arreglo de la CI tras `stable/F31-activar-sesion-03`).** El
> nombre de ese test nuevo afirmaba más de lo que pasa: la negativa por A-27 **no** llega antes de
> leer velas. La comprueba el bróker al colocar la primera orden stop (ADR-0057 §5), después de leer
> las velas y los ticks del mes y de correr el motor hasta esa orden. En la CI, sin `data/`, la CLI
> se paraba antes por «falta en disco» y el test fallaba: la CI de `e7df30b` salió roja por eso. Se
> renombra a `test_la_cli_con_a47_fijada_pasa_a_pedir_a27`, se salta sin las velas en la máquina como
> `test_preparar_a35.py`, y sus aserciones no cambian. Es también el test que se cortaba por memoria
> al 69 %: medido solo, 753 MB y 192 s, casi todo de `tracemalloc` en `motor arnes`
> (`trabajo/memoria-suite`).

`tests/unit/test_cableado.py`, el otro módulo que nombra A-47, pasa sin cambios.

- `tests/unit/test_transcribir_sesion.py::test_el_orden_es_el_de_la_hoja_con_a46_tras_a21`: comparaba
  el orden de la sesión 02 de `transcribir_sesion.py` con la hoja viva de `hoja_preguntas.py`. Al
  quitar de la hoja las nueve RESUELTAS, se separaron. Ese orden agrupa la grabación de la sesión 02
  tal como se llevó, así que no cambia: el test lo fija explícito. Salió en el primer `make check`
  de la rama.

- `tests/unit/test_kit.py::test_ambiguedades_reales_y_esquema`: las bloqueantes ABIERTAS pierden A-47
  y ganan A-51; las RESUELTAS ganan las diez de la sesión 3.
- `tests/unit/test_hoja_preguntas.py` y `scripts/hoja_preguntas.py` (`ORDEN_SESION_02`): salen las
  nueve RESUELTAS que estaban en la hoja, porque la hoja se niega a preguntar una pregunta cerrada.

## Estado

**Rama `trabajo/activar-sesion-03`: LISTA PARA REVISIÓN, NO CERRADA.**
