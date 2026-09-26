# El cableado del simulador

Rama `trabajo/cableado-simulador`, 2026-09-26, sesión autónoma. Sin merge, sin tag y sin push: el
cierre lo decide Aleks. Un ADR nuevo, PROPUESTO (ADR-0053, el cableado del simulador): lo acepta o
corrige el consultor. Next Action 33.

Guardas, verificadas al terminar: `docs/validation/PREREGISTRO.md` con blob `52649183…`, el
declarado; cero autorizaciones en `knowledge/cases/holdout/`; nada del material de septiembre;
mayo, marzo y febrero ni se descargaron ni se ejecutaron (la compuerta del arnés se niega a
cualquier mes de medida o fuera de construcción antes de leer, y ahora también con `--simular`,
con test); ninguna fecha de día reservado o retirado en ningún fichero de esta rama; la spec,
`ambiguedades.yaml`, `engine/interprete.py` y `engine/motor.py` sin un solo cambio (`git diff
--stat main..HEAD` sobre esas rutas está vacío); ningún `--no-verify`; cada commit con su sello de
`make check` en primer plano. Las velas y los ticks de construcción (abril y agosto de 2026,
material de desarrollo sin días reservados) se leen para simular, que no es abrir (ADR-0021 §1).

## 1. Qué se cableó, pieza a pieza

| pieza | commit | dónde |
|---|---|---|
| ADR-0053, el cableado del simulador, PROPUESTO | `c5f2c29` | `docs/adr/0053-el-cableado-del-simulador.md` |
| bucle y cableado | `57526b4` | `engine/cableado.py` (`MotorCableado`), `engine/primitivas_broker.py`, `cuenta.CuentaViva`, `Broker.mover_stop` |
| comando y visor | `a7263d5` | `motor arnes --simular`, `motor visor --simular`; runbooks ARNES-MOTOR y VISOR-DIAS |
| tests | `e34c58b` | `tests/unit/test_cableado.py`, 9 tests; PROJECT_STATE con el recuento |
| línea base e informe | este commit | `CABLEADO-SIMULADOR-LINEA-BASE.txt`, este fichero |

**El bucle.** `MotorCableado` cumple el protocolo `Motor` del arnés, así que el arnés, su informe y
el visor lo usan sin cambios. Por cada minuto de la ventana, en el orden de ADR-0053 §5: el bróker
avanza tick a tick hasta el último milisegundo anterior al cierre de M1 y la cuenta viva recibe sus
eventos (apertura con comisión, cierre con comisión por lado y swaps, la peor marca del minuto de
cada posición viva); los hechos de origen bróker y los eventos del tramo quedan a la vista del
intérprete; y el intérprete corre el evento del cierre de M1 con la spec real. Un solo reloj (§4):
el del perfil, comprobado al arrancar contra `huso_operativa` día a día; si no dan la misma
medianoche, el cableado se niega. La cuenta persiste toda la corrida; el estado de estrategia y el
bróker empiezan cada día de cero, y lo que quede vivo o pendiente al cerrar la ventana se cierra a
mercado o se cancela y se cuenta (§6). Ticks obligatorios (§7): un día sin dataset se rechaza salvo
con `--depuracion`, y entonces la salida entera lleva `DEPURACION: respaldo M1, no cuenta`.

**Las primitivas.** Sobre `primitivas_escritas` (ADR-0048), sin tocarlas: de fuente bróker,
`operaciones_abiertas_alcanzan`, `se_activa_entrada`, `salta_stop` y `se_cierra_operacion` (con
el mecanismo del cierre clasificado: `salto_el_stop`, `break_even` si el stop se movió, `ganancia`
o `perdida`); de fuente bot, `distancia_menor_que` y `no_es_multiplo_de` sobre la orden en
preparación; los acumuladores de la firma, `perdida_dia_firma` y `perdida_total_firma`, leídos de
la cuenta viva y recortados en cero, con la primitiva que distingue `alcanza_tope`,
`se_acerca_al_limite` y `no_cabe_la_operacion` por sus argumentos (§3.2); y las acciones que hablan
con el bróker: `dimensionar_lote`, `escribir_stop_en_la_orden`, `fijar_objetivo`,
`redondear_lote`, `colocar_orden_limite`, `cerrar_a_mercado`, `retirar_orden_limite`,
`reubicar_orden_limite` y `mover_stop`. Ninguna cifra vive en el código: cada valor se lee del
registro por el nombre que la spec pasa como argumento.

**El comando y el visor.** `motor arnes --simular` escribe el informe del arnés de siempre y, al
final, la sección «Simulación»: veredicto de la cuenta sobre el tramo, curva de equity por día,
eventos del bróker con su fuente, rechazos y huecos con nombre. `motor visor --simular` corre el
día con el motor cableado: las operaciones del bot llevan el stop y el objetivo REALES de la orden y
la página añade «Bróker simulado» con las órdenes, las posiciones y los eventos, recortados por
`--hasta`. Los dos admiten `--perfil`, `--fase` y `--depuracion`, y los dos se niegan a medida y a
lo que no es construcción antes de construir nada. Medido: abril y agosto enteros, 42 días, en
320,5 s y 247,5 MiB de pico; un día en el visor, 2,0 s.

## 2. Las decisiones, todas pendientes de validar

Las de ADR-0053, tomadas en el ADR y ejecutadas tal cual: **1.1** el lote se resuelve al colocar,
con el stop ya escrito; **1.2** `OP` es la única posición viva, y con varias la acción es un error
con nombre; **1.3** la zona `Z` es una ligadura de texto `zona:<id>` a una `Zona` del contexto del
día; **2.1** los eventos del bróker se entregan en el siguiente cierre de M1; **3.1** los
acumuladores de la firma se recortan en cero; **3.2** la primitiva del acumulador distingue por
argumentos, con comparaciones `>=`; **5.1** el cierre de RN-030 se ejecuta al precio del cierre de
M1.

Las que salieron al construir, todas por la opción conservadora:

- **El perfil y la fase por defecto.** Sin `--perfil`, el único fichero de `knowledge/cuentas/`;
  con varios, se pide. Sin `--fase`, la PRIMERA que declara el perfil (`reto`). Ningún nombre de
  firma vive en el código.
- **La cuenta arranca un milisegundo antes de la ventana** del primer día, para que el primer
  avance del bróker (el último milisegundo antes del primer cierre de M1) no la haga retroceder.
- **Las primitivas de fuente bot sin orden en preparación dan NO**, no DESCONOCIDO:
  `distancia_menor_que` y `no_es_multiplo_de` solo tienen sentido con una orden preparada, y sin
  ella RN-026 y RN-027 no tienen nada que frenar.
- **Un gate de la firma sin cuenta** (`ctx.acumuladores` vacío) da NO_IMPLEMENTADA con nombre, no
  un valor.
- **`fijar_objetivo` con extensión activa o parciales** es un error con nombre y deja el hueco
  `accion:fijar_objetivo:extension_o_parciales`; hoy el registro tiene las dos apagadas.
- **`mover_stop` solo a `precio_entrada`**; otro destino deja el hueco `accion:mover_stop:<destino>`.
- **El stop se llena al precio del tick que lo cruza** (DN-3 de ADR-0051, que ya era provisional):
  el test lo mide, un punto por debajo del stop en el día sintético.
- **La curva de equity solo nombra días CORRIDOS.** La cuenta corta todos los días de calendario
  que cruza entre dos días corridos, porque el límite diario se recalcula cada día, y la primera
  versión de la línea base listaba esos cortes: todos los días de calendario de mayo, junio y
  julio, con el saldo intacto. Ninguno se leyó y la lista no distingue días, pero la guarda del
  brief dice «ninguna fecha de día reservado en ningún fichero de la rama» y se cumple al pie de la
  letra: la curva filtra por los días con mercado, el test lo exige con un salto de seis días, la
  línea base se regeneró (idéntica salvo la curva) y el commit que la traía se rehízo antes de
  existir fuera de esta máquina.

## 3. Los huecos con nombre

Lo que la spec no da queda NO_IMPLEMENTADA con nombre, en la traza y en el embudo; nunca un valor
inventado:

- **Acumuladores del trader (ADR-0053 §3.3):** `perdida_dia` y `perdida_semana` (la spec no declara
  `magnitud`, saldo o equity, ni la semana tiene corte aparte), y `cartuchos` (depende de
  `cartucho_criterio` y de un cierre con esquema, que es geometría). Los dos primeros son **los
  que hoy paran el embudo** de construcción: RN-020 los pide en cada sesión.
- **La geometría (A-29, A-35):** `toca_colocar_orden_limite`, `se_desarrolla_en_el_lado_de_ruido`,
  `se_da_esquema`, `zonas_desarrolladas_superan`, `se_mapea_estructura`, `se_completa_zona_de_control`,
  `alcanza_nivel`, `cruza`, `contexto_filtrable` y `ninguna_regla_de_entrada_aplica`.
- **Acciones sin contrato:** `abstenerse`, `agrupar_estructura`, `gestionar_salida`,
  `realizar_perdida` y `reentrar`. El intérprete ya las deja en `no_implementadas` como
  `accion:<nombre>` cuando una regla llega a ejecutarlas; en construcción ninguna llega.

## 4. Qué gates pasan de DESCONOCIDO a evaluados, MEDIDO

ADR-0049 H4 contaba diez gates en DESCONOCIDO que prohibían `abrir_operacion`: RN-005, 008, 009,
016, 018, 020, 026, 029, 031 y 032. Medido sobre tres días de construcción de abril (seis sesiones),
comparando las primitivas NO_IMPLEMENTADA de cada regla con el motor de la spec y con el cableado:

| | motor de la spec (ADR-0049) | motor cableado (ADR-0053) |
|---|---|---|
| reglas con alguna primitiva NO_IMPLEMENTADA | RN-004, 005, 007, 008, 009, 010, 011, 012, 016, 017, 018, 019, 020, 021, 022, 026, 027, 029, 031, 032 (20) | RN-004, 005, 007, 008, 009, 011, 020, 021, 022 (9) |
| pasan a evaluadas | | **RN-010, 012, 016, 017, 018, 019, 026, 027, 029, 031, 032** (11) |
| gates de H4 que siguen en DESCONOCIDO | los diez | **RN-005, RN-008, RN-009** (geometría) y **RN-020** (hueco) |

**Corrección a ADR-0053, «Impacto».** El ADR anunciaba RN-018, 026, 027, 029, 030, 031 y 032 como
evaluados y RN-016 entre los que seguían en DESCONOCIDO. La medida dice otra cosa en dos puntos:
**RN-016 SÍ se evalúa** en construcción, porque `se_cierra_operacion` es de fuente bróker, da NO
mientras no haya cierres y el `y` de Kleene ya no llega a pedir `cartuchos` (el hueco sigue ahí y
volverá a aparecer el día que haya un cierre); y **RN-030 no estaba en ninguna de las dos listas
medidas** porque es una regla terminal que lee el hecho `detenido_por_tope_total`, no el
acumulador. Además pasan a evaluados RN-010, RN-012, RN-017 y RN-019, que el ADR no nombraba
porque no son gates de `abrir_operacion`. El ADR queda corregido en el mismo commit; sigue
PROPUESTO.

Lo que esto significa para la cobertura: aunque mañana la geometría estuviera escrita, **RN-020
seguiría prohibiendo `abrir_operacion`** hasta que `perdida_dia` y `perdida_semana` tengan
contrato (una decisión de spec: la `magnitud` y el corte semanal). El test de punta a punta lo
esquiva con acumuladores sintéticos que dan NO, y por eso lo dice en su docstring.

## 5. Los tests (`tests/unit/test_cableado.py`, 9)

Sobre un día SINTÉTICO de 2030 y la spec REAL, con la estrategia sintética viviendo en el test
(la geometría NO_IMPLEMENTADA resuelta a mano por `primitivas_extra`, `acumuladores_extra` y
`zonas_de`, las tres puertas que el motor deja para eso):

- **Punta a punta:** en el minuto de la zona, `toca_colocar_orden_limite` sintético liga `Z`;
  RN-011 dimensiona y escribe el stop (0,8 de la caja), RN-015 fija el objetivo (1:3 sobre la caja
  completa) y coloca la limite por el bróker; los ticks la llenan; el stop salta al precio del tick
  que lo cruza; RN-012 dispara; la cuenta viva descuenta la pérdida y la comisión por lado del
  perfil; el veredicto es EN_CURSO; ninguna primitiva de acumulador de la firma falta.
- **Un gate de la firma prohíbe cuando la cuenta cruza su límite:** un hueco de 2.000 puntos por
  debajo del stop; la cuenta queda SUSPENDIDA en el instante del tick, y RN-029 y RN-031 —antes en
  DESCONOCIDO— disparan, prohíben y fijan `detenido_por_tope` y `detenido_por_tope_total` en el
  primer cierre de M1 posterior al tick, nunca antes.
- **Reloj único:** un perfil con otro reloj de corte se rechaza al arrancar.
- **Sin mirar al futuro:** recortar los ticks un minuto después del stop no cambia nada de lo
  fijado ni ningún evento hasta el corte.
- **Determinismo:** el informe del arnés más la sección de simulación, idénticos byte a byte.
- **Ticks obligatorios:** sin dataset se niega; con `--depuracion` corre sobre el respaldo M1 y
  la traza y el informe lo marcan.
- **La cuenta persiste y la estrategia empieza de cero:** dos días por el mismo motor, la zona se
  liga otra vez, el lote del segundo día sale del saldo mermado, dos días de trading, y el bróker
  del día dos no arrastra posiciones del día uno.
- **El detalle para el visor:** órdenes, posiciones y eventos con sus estados y precios.
- **Las negativas por la CLI:** `--simular` en el arnés y en el visor se niega a medida y a lo que
  no es construcción sin escribir nada. El centinela de un día oculto vive en
  `dias_de_construccion` y `caso_de_construccion`, las dos puertas que el cableado llama, y sus
  tests siguen verdes.

Los tests del arnés, del bróker, de la cuenta, del llenado, de la simulación y del visor siguen
verdes; `make check` en verde en cada commit, con su sello (1.152 casos en el último).

## 6. La línea base nueva frente a las anteriores

`docs/validation/CABLEADO-SIMULADOR-LINEA-BASE.txt`, escrito con `uv run botsito motor arnes
--simular --salida …` (320,5 s, 247,5 MiB), al lado de `ARNES-MOTOR-LINEA-BASE.txt` y
`HUECOS-MOTOR-LINEA-BASE.txt`, que no se tocan.

| | HUECOS-MOTOR (ADR-0049) | CABLEADO-SIMULADOR (ADR-0053) |
|---|---|---|
| días · sesiones con trader · operaciones del trader | 42 · 49 · 77 | 42 · 49 · 77 |
| operaciones del bot · cobertura · precisión | 0 · 0/77 · sin definir | 0 · 0/77 · sin definir |
| `sesgo` producido | 49 de 49 | 49 de 49 |
| paradas NO_IMPLEMENTADA en el embudo | 9: cartuchos, perdida_dia, perdida_dia_firma, perdida_semana, perdida_total_firma, alcanza_nivel, cruza, se_cierra_operacion, toca_colocar_orden_limite (49 de 49 cada una) | **5: perdida_dia, perdida_semana, alcanza_nivel, cruza, toca_colocar_orden_limite** (49 de 49 cada una) |
| reglas disparadas por sesión | RN-001 42 de 84; RN-003 84 de 84; RN-033 15 de 84 | idéntico |
| avisos H3 | 6, todos `gate RN-001, RN-033` | los mismos 6 |
| RN-003 por sesión · por operación | 21/6/22 · 58/12/7 | idéntico |
| eventos del bróker · rechazos | (no había bróker) | 0 · 0 |
| veredicto de la cuenta sobre el tramo | (no había cuenta) | EN_CURSO, saldo y equity en el capital inicial, 0 días de trading |
| huecos con nombre pedidos | | `acumulador:perdida_dia`, `acumulador:perdida_semana` |

Las filas «Por sesión» son idénticas a las de HUECOS-MOTOR salvo los corchetes de los tres hechos
detenidos, que es exactamente lo que cambió: `detenido_por_tope` ya no se para en
`perdida_dia_firma` (la cuenta lo alimenta), `detenido_por_tope_total` pasa a «productoras sin
cumplirse» (RN-031 evaluado, y NO) y `detenido_por_cartuchos` también (RN-016 evaluado, y NO,
por §4). Cobertura 0, como esperaba el brief: el motor sigue parado en RN-011
(`toca_colocar_orden_limite`, A-35) y RN-004 (`alcanza_nivel`, `cruza`), y por detrás, RN-020.
Cero eventos del bróker es lo coherente con cero órdenes: la cuenta no se mueve y el veredicto es
EN_CURSO por construcción, no por mérito.

## 7. Lo que decide el consultor

- Aceptar o corregir ADR-0053 y las decisiones de §2, en especial 1.2 (`OP`), 2.1 (eventos al
  cierre de M1) y 5.1 (RN-030 al cierre de M1), que tienen alternativa a un cambio de intérprete
  o de spec de distancia.
- La `magnitud` y el corte semanal de `perdida_dia` y `perdida_semana` (spec): sin eso RN-020
  prohíbe `abrir_operacion` aunque la geometría exista (§4).
- La fase por defecto (`reto`) y el perfil único como convención de la CLI.
- El deslizamiento y el precio de llenado del stop siguen atados a DN-3 (demo de MetaTrader).

## Estado

WAITING_FOR_USER_VALIDATION.
