# PREREGISTRO · lo que se fija antes de medir (ADR-0096)

Relleno el 2026-11-19 en la rama `trabajo/preregistro` con las decisiones del consultor de ese día
(ADR-0096; informe `docs/validation/PREREGISTRO-INVENTARIO.md`). Lleva dos cosas que no se parecen,
y se sabe: la RENTABILIDAD, la puerta para operar en vivo, que no lee ningún material reservado
(ADR-0092 §3 a §7), y F26, la fidelidad contra el trader sobre lo reservado, que es diagnóstico.

## Para qué sirve

Un umbral pre-registrado es un número que se escribe **antes** de ver el resultado, para que nadie
lo pueda ajustar después. Sin esto, siempre se puede encontrar un criterio con el que el bot apruebe.
Las cifras de aquí son COPIAS: viven en `knowledge/cases/criterio_fidelidad.yaml` (ADR-0002) y en
los ADR que se citan, y ninguna se cambia sin un ADR nuevo que declare lo visto (ADR-0070 punto 4;
ADR-0043, «Cambios»).

## Quién autoriza, quién decide y qué está cerrado

- **Abrir una partición reservada lo autoriza Aleks** (ADR-0021 §3), con un
  `docs/validation/AUTORIZACION-<particion>.md` commiteado que fija con `preregistro_blob` la versión
  exacta de este fichero (ADR-0033). El consultor decide el contenido de este fichero; la sesión lo
  ejecuta (ADR-0072).
- **Hoy la puerta está cerrada para las seis particiones** (`holdout-1/2/3`, `fidelidad-1/2/3`): no
  existe ninguna autorización y este fichero no declara ninguna pregunta. La puerta solo abre una
  pregunta declarada aquí y en estado ABIERTA (`src/botsito/cases/holdout.py`, `_PREGUNTA`); la
  primera la añade, ABIERTA y con su partición escrita, la rama que construya el comando de medida
  de F26 (ADR-0096 §5). Cualquier cambio de este fichero invalida las autorizaciones que haya.

## 1. La rentabilidad (ADR-0092 §3 a §6; bloque `rentabilidad` de `criterio_fidelidad.yaml`)

**La métrica** (ADR-0092 §3): el **R neto por operación** = PnL neto en USD (con la comisión del
perfil, 2,50 por lote y lado, ADR-0090 §3, y los swaps) entre el riesgo en USD al colocar, tal como
lo calcula la cuenta al dimensionar. Sobre las operaciones LLENADAS del bot, en la fase del perfil
que dice `fase`, con el deslizamiento de abajo y sobre los meses de abajo. Las funciones son puras,
en `src/botsito/cases/criterio_fidelidad.py`.

**Pasa solo si se cumplen todas** (los nombres son los campos del yaml; los valores, copiados):

| Criterio | Campo | Valor |
|---|---|---|
| a) operaciones llenadas, como mínimo | `n_minimo` | 100 |
| b) esperanza (media del R neto), como mínimo | `esperanza_minima_r` | "0.10" |
| c) el percentil de la media del R neto por remuestreo POR DÍAS es > 0 | `percentil_remuestreo` | 5 |
| c) réplicas del remuestreo | `replicas_remuestreo` | 10000 |
| c) semilla del remuestreo | `semilla_remuestreo` | 20261107 |
| d) ningún día la pérdida diaria (magnitud y base de la firma) llega a esta fracción del capital inicial | `perdida_diaria_max` | "0.03" |
| e) la menor equity del tramo no baja del capital inicial menos esta fracción | `perdida_total_max` | "0.06" |
| f) la cuenta no entra en SUSPENDIDA en ningún momento | — | — |

La forma del remuestreo (ADR-0092 §3 c, fijada en la PARADA 2 de
`trabajo/metodo-fidelidad-rentabilidad`): cada réplica sortea con reemplazo tantos días como días de
mercado corridos, con o sin operaciones; su cifra es la media del R neto de TODAS las operaciones de
los días sorteados (agrupada); una réplica sin ninguna operación no cuenta, y la salida dice cuántas
se descartaron; el percentil es el de rango inferior, floor(percentil × (n − 1) / 100) sobre las
medias ordenadas; el generador es `random.Random` de Python con la semilla. Los bloqueos de RN-032
no son criterio. Si no se cumple a), el resultado es «insuficiente»; cualquier otro incumplimiento
es «no pasa».

**La fase**: `fase: fondeada`. El simulador corre una fase por ejecución; pasar el reto y la
verificación es otra pregunta y no es la puerta (ADR-0092 §5).

**Los meses** (`meses`): 2025-06, 2025-07, 2025-08, 2025-09, 2025-10 y 2025-11, seguidos, con la
cuenta ARRASTRADA en todo el tramo. **La extensión** (`extension`): si al acabar noviembre de 2025
N < 100, se añaden con la misma spec 2025-05, 2025-04, 2025-03, 2025-02 y 2025-01, en ese orden y de
uno en uno, hasta N ≥ 100; si con enero sigue N < 100, «insuficiente» y no pasa. La decisión de
añadir mira solo N, nunca el resultado. **Por qué esos** (ADR-0092 §5): no hay material del trader
de 2025 salvo diciembre, que queda fuera; el bloque cubre verano, los dos cambios de hora de 2025 e
invierno; y no gasta febrero de 2026 ni ninguna partición reservada.

**El deslizamiento** (ADR-0092 §4; `deslizamiento: pendiente_F17`, `percentil_deslizamiento_f17:
90`): la medida se corre una vez con el deslizamiento del simulador en 0; cuando F17 lo mida, se
recalcula sin volver a correr el bot (a cada llenado de orden stop y a cada cierre por stop o a
mercado se le resta la MEDIANA medida; los cierres por objetivo no se tocan) y se vuelven a evaluar
b), c), d) y e), d) y e) sobre la curva recompuesta operación a operación, sumando el ajuste al día
de cada cierre. Los lotes y los bloqueos de RN-032 no se recalculan, y el informe lo dice. Además,
la esperanza recalculada con el percentil 90 de F17 tiene que ser > 0. **La puerta no puede dar
«pasa» antes de F17.** El informe de la medida da también el deslizamiento por llenado, en puntos,
que llevaría la esperanza a +0,10 R (el punto de equilibrio), sin decidir nada con él.

**Antes de correr la medida** (ADR-0092 §5), además de la spec sellada de abajo, que fija su propia
rama con su ADR (el comando no existe, ADR-0070 punto 6):
- el calendario de cierres renovado hacia atrás hasta enero de 2025 (`RENOVAR-CIERRES.md`,
  condición 1);
- las velas M1 y los ticks de Dukascopy de esos meses con su manifiesto, bajados y declarados según
  los heredados 7 y 9 (junio de 2025 es un junio; un manifiesto nuevo con el prefijo del kit entra
  en `universo()`);
- la deuda del spread supuesto para minutos sin ticks, que se busca por la hora de pared de Madrid,
  nombrada como riesgo de noviembre y de la extensión de invierno;
- la construcción en el umbral de ADR-0070 (la línea «habilita medir»).

**Una sola ejecución, y si no pasa** (ADR-0092 §5 y §6): si se repite por un fallo técnico, se
declara con su causa y la spec no cambia entre las dos. Si no pasa, esos meses se escriben en
`vistos_rentabilidad` (hoy vacío) y no vuelven a medir nunca; se vuelve a construir, y la siguiente
medida usa otros meses, que fijará su ADR. Ningún parámetro se ajusta por esta cifra.

**La spec sellada: el procedimiento, no el hash** (ADR-0096 §5; ADR-0092 §5). El hash no se escribe
aquí todavía: la spec cambia hasta que la construcción llegue al umbral de ADR-0070. En la rama de la
medida de rentabilidad, **antes de correr y antes de que exista ninguna autorización de holdout**, se
añade a este fichero:
- el sha del commit desde el que se corre;
- en ese commit (`git rev-parse <commit>:<ruta>`), el id de blob de
  `knowledge/spec/strategy_spec.yaml`, `knowledge/spec/parametros.yaml`,
  `knowledge/cuentas/ftmo-2step-swing-100k.yaml` y `knowledge/simulador/llenado.yaml`;
- y el id del árbol de `knowledge/cuentas` (lleva también el calendario de cierres,
  `knowledge/cuentas/cierres/`) y el del árbol de `src`.
Son bytes commiteados, no el hash canónico de `botsito spec manifest`.

## 2. F26: la fidelidad contra el trader sobre lo reservado (ADR-0096 §0 a §3 y §6)

**Su papel**: diagnóstico. No bloquea nada y se informa en el memorando (ADR-0092 §7).

**La referencia, sin ninguna cifra nueva**: la de ADR-0043, con su misma unidad (la operación,
dentro de su día y su sesión), su emparejamiento uno a uno y sus tolerancias:

| | Campo de `criterio_fidelidad.yaml` | Valor |
|---|---|---|
| cobertura, como referencia | `umbral_cobertura` | "0.70" |
| precisión, como referencia | `umbral_precision` | "0.60" |
| \|Δentrada\| en puntos | `tolerancia_entrada_puntos` | 3 |
| \|Δinstante de llenado\| en minutos | `tolerancia_instante_min` | 15 |

**La potencia manda sobre la frase** (ADR-0036 §8; `src/botsito/cases/fidelidad.py`): el informe de
F26 da N del trader, N del bot en días con operaciones del trader, la cobertura y la precisión, su
intervalo y cuántas unidades efectivas independientes hay. Solo con 36 o más escribe «llega» o «no
llega» contra la referencia; con menos, «descriptiva», y nadie la cita como si midiera. Cómo se
cuentan las unidades efectivas sobre operaciones y qué intervalo se usa lo fija, leyendo
`docs/validation/AUDITORIA-2026-09-13-ultracode.md` §6.1 y antes de medir nada, el ADR de la rama
que construya el comando de medida; aquí no se inventa. La cascada por criterios (ADR-0092 §2) se
informa al lado, sin umbral. El objetivo, el resultado y la gestión quedan fuera (ADR-0043), así que
A-56 no puntúa; A-16 sigue ABIERTA con la regla de ADR-0092 §9, que con la medida de R3.7 no se
dispara.

**Sobre qué se mide: el mes limpio.** Febrero de 2026, cuando el trader lo entregue grabado en vídeo
y con voz (S-14), reservado entero (`knowledge/cases/meses_reservados.yaml`) y por su propia rama,
con su ADR y su partición. **Hay que pedírselo**: el mensaje lo redacta el consultor para Aleks.
- `holdout-1` sigue intacta y reservada para la nota de F26 (ADR-0021 §6), y **no se abre mientras
  el mes limpio esté pendiente**; abrirla sin él exige un ADR que lo diga.
- `fidelidad-1` (septiembre) no es ciega (ADR-0034) y no se usa para F26.
- **Cuándo**: no antes de que mayo `dev` esté medido (R5.2; es el orden de la hoja de ruta, R5.5,
  no una regla de un ADR); una sola vez, con la spec de esa corrida y una cuenta para el mes
  (ADR-0092 §8, extendido por ADR-0096).

**Cuántos días**: los que den 36 unidades efectivas; en la práctica, un mes entero con vídeo. No se
promete un número de días. La fuente es la densidad de construcción (operaciones del trader por
día `dev`, `PREREGISTRO-INVENTARIO.md` §0.4): media 2,61 y mediana 2 sobre 76 días, de 1,67 a 5,15
de media según el mes; la más alta, julio, que cuenta como grabado en vídeo solo de forma
provisional, hasta que T lo compruebe (`criterio_fidelidad.yaml`, `material_sin_video`; de abril
solo el día 29 está grabado).

**El conjunto medido**, cuando exista: los días de la partición que caen dentro de un TRAMO de
`cobertura_material` de su camino. Los demás quedan fuera por escrito, no como días sin operación.
Fuera también, siempre:
- los dos días del universo de la sesión 1 que no están en ninguna partición (ADR-0035,
  «Impacto»); toda cifra dice sobre qué conjunto se da;
- los días retirados (`knowledge/cases/retirados.yaml`, ADR-0041), que no se abren nunca;
- el día quemado de `holdout-2`, que no está en `retirados.yaml`: lo excluye
  `docs/validation/HOLDOUT-EXPOSICIONES.md`, «Lo que esto obliga», punto 4
  (`HOLDOUT-EXPOSICIONES.md:177`), y la rama que dé uso a `holdout-2` lo retira antes.

**Si no llega**: un diagnóstico se informa y no se repite. `holdout-2` y `holdout-3` siguen cerradas.

**Sus límites, conocidos**: la potencia (arriba); y el sesgo de los libros sin vídeo: en ellos el
trader se saltaba las sesiones que iban a acabar en break even (S-14: `ev-v15-011912-0ae32588`,
`ev-v16-003421-b824b770`), y todo el material reservado que existe hoy -mayo, septiembre, marzo-
llegó sin vídeo. Por eso el mes limpio se pide con vídeo.

## 3. Las particiones, por recuento

Por partición, sin ninguna clave (`docs/validation/anexos/PREREGISTRO-INVENTARIO/`,
`recuento-por-tramo.txt` y `recuento-particiones.txt`):

| Partición | Camino | Días | Retirados | Medibles | Medibles dentro de un tramo de `cobertura_material` | En un mes con cero tramos |
|---|---|---|---|---|---|---|
| `holdout-1` | kit, sesión 1 | 8 | 0 | 8 | 6 | 2 |
| `holdout-2` | kit, sesión 1 | 8 | 0 | 8 | 4, de ellos el quemado: 3 medibles | 4 |
| `holdout-3` | kit, sesión 1 | 8 | 1 | 7 | 3 | 4 |
| `fidelidad-1` | fidelidad, septiembre | 10 | 4 | 6 | 6 | 0 |
| `fidelidad-2` | fidelidad | 0 | 0 | 0 | 0 | 0 |
| `fidelidad-3` | fidelidad | 0 | 0 | 0 | 0 | 0 |

Ningún día medible cae en un mes sin declarar ni fuera de los tramos de su mes. Los días «en un mes
con cero tramos» no tienen material del trader y quedan fuera por escrito. `fidelidad-2` y
`fidelidad-3` esperan a marzo (ADR-0046). Ninguna de las seis tiene uso asignado para F26 hasta el
mes limpio.

## 4. Las exposiciones, por referencia

Todas en `docs/validation/HOLDOUT-EXPOSICIONES.md` (ADR-0021 §4); F26 las cita en su informe. Aquí,
solo cuántas filas nombran cada partición y la fecha de cada una
(`docs/validation/anexos/PREREGISTRO-INVENTARIO/exposiciones-por-particion.txt`); el contenido se
lee en la tabla, no aquí:

| Partición | Filas | Fechas de las filas |
|---|---|---|
| `holdout-1` | 15 | 2026-09-11, 2026-09-12, 2026-09-13, 2026-09-22, 2026-10-04, 2026-10-10, 2026-10-14, 2026-10-17, 2026-10-18, 2026-10-27 |
| `holdout-2` | 16 | las de `holdout-1` y 2026-11-19 |
| `holdout-3` | 19 | las de `holdout-1` y 2026-11-08 |
| `fidelidad-1` | 4 | 2026-09-23, 2026-10-04, 2026-10-10, 2026-10-17 |
| `fidelidad-2`, `fidelidad-3` | 0 | — |

Además, 15 filas nombran el holdout sin partición. Una fila puede nombrar una partición sin
exponerla; si quema o no, lo dice cada fila en su última columna.

## 5. Lo que no está aquí

- **Kappa, paridad y DSR** (`docs/plan/MASTER_PLAN.md` §H): cada uno se pre-registra en la rama de
  su funcionalidad, antes de su primera medida: kappa, la sesión que etiquete; paridad, F30 y F32;
  DSR, F27 (ADR-0096 §7).
- **El comando que mide F26** no existe: lo construye su propia rama, con su ADR, abriendo UNA sola
  partición (ADR-0096 §4).
