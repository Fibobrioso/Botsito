# FTMO y los cuatro ADR de arquitectura — INFORME DE VALIDACIÓN

**Rama:** `trabajo/ftmo-y-arquitectura` (rama de trabajo sin número propio, MASTER_PLAN §F)
**Cierre previsto:** tag `stable/F13-ftmo`
**Decisiones:** ADR-0026, ADR-0027, ADR-0028, ADR-0029, ADR-0030 y la enmienda de ADR-0022
**spec_version:** 10.2.0 → 11.1.0 (11.0.0 es el cambio mayor —una regla nueva y otra que cambia de sentido, ADR-0013—; 11.0.1, el parche que exige la guardia del manifiesto al corregir lo que encontró la auditoría de cierre; 11.1.0, la regla y el parámetro nuevos de las correcciones del consultor del 2026-09-14)
**Estado:** WAITING_FOR_USER_VALIDATION

---

## 1. Por qué existe esta rama

FundedNext **no admite bots en cuentas de 50.000 o más**, ni en el reto ni en la fondeada:
*«traders on account sizes of $50,000 and above must trade manually and may not use Expert
Advisors, trading bots, or any automated tools»*. El objetivo del proyecto —un bot en una cuenta
fondeada de 100.000— era imposible ahí. Se cambia de firma, y con la firma cambian los relojes, la
regla de noticias y la procedencia de los parámetros medidos en su demo.

Sale además de la auditoría del 2026-09-13 (`AUDITORIA-2026-09-13-ultracode.md`, veredicto ROJO,
§9.3: «cuatro decisiones de arquitectura sin ADR»). Van juntas porque son la misma decisión: el
reglamento de la firma es el que obliga a que el riesgo vaya por tick.

No se ha escrito una línea de motor. No se ha tocado `knowledge/evidence/` ni `knowledge/feedback/`.

## 2. Qué se decidió

| | Decisión | Dónde |
|---|---|---|
| **Firma** | FTMO, 2-Step, tipo **Swing**, 100.000. Doce parámetros de la firma (`firma` y `firma_*`) | ADR-0026 |
| **Freno de la firma** | **RN-029** (`gate`): 5 % diario desde el saldo a medianoche CE(S)T y 10 % total estático, los dos del capital inicial y sobre equity; prohíbe y detiene. **RN-030** (`gate`, complementa a RN-029): cierra a mercado solo con posición viva | ADR-0026 |
| **Noticias** | Swing no las restringe: `filtro_noticias` vuelve a `no`, **RN-028 DESCARTADA**, **A-17 DECIDIDA**, A-22 invierte su sentido | enmienda de ADR-0022 |
| **Día de riesgo** | Medianoche CE(S)T = reloj civil del trader. `reloj_dia_riesgo = civil_operativa`, **A-19 DECIDIDA**. Desaparece el tercer reloj | ADR-0027 |
| **Reloj del motor** | Riesgo por tick sobre equity, estrategia al cierre de M1, órdenes por evento, punto fijo con refracción, hechos del bróker derivados | ADR-0028 |
| **Lado y redondeo** | Geometría en BID, llenado por dirección, al punto más cercano con empate en contra del bot, lote a la baja | ADR-0029 |
| **Árbol y primitivas** | El motor recorre `forma` y despacha por nombre a primitivas escritas a mano | ADR-0030 |
| **Instrumento** | Cinco parámetros a DEFAULT_AMBIGUOUS bajo **A-27** (medición en FTMO) | ADR-0026 |
| **Reloj del servidor** | `broker_offset_base` y `broker_dst` a UNKNOWN bajo **A-28** | ADR-0026, ADR-0027 |

## 3. Lo que el reglamento dice, y cómo se leyó

Todas las afirmaciones del brief sobre FTMO se contrastaron el 2026-09-14 contra las páginas de la
firma (un agente, con cita literal y URL por afirmación). Resultado: **todas se sostienen**, con
tres matices que cambian cómo están escritos los ADR:

1. **El ejemplo oficial del límite diario va sobre 200.000** (190.000 el día 1; 194.000 el día 2 si
   se cerró en 204.000), no sobre 100.000. La fórmula es la misma. ADR-0026 cita el de 200.000 y
   declara que el escalado a 100.000 es cuenta nuestra.
2. **La ficha dice «GMT+2 +DST» sin nombrar el calendario** de horario de verano. Por eso A-28 no
   se puede cerrar leyendo: hay que observar una transición.
3. **FX Replay no dice en ninguna fuente oficial qué lado dibuja.** El punto 1 de ADR-0029 queda
   escrito como decisión sobre los datos de referencia, y lo de que coincida con lo que ve el
   trader, como NO verificado (§6).

Las citas se tomaron a través de un paso automático de lectura de página, no del HTML crudo.
Conviene que el dueño las vea en el panel antes de comprar (§7).

## 4. Lo que cambió respecto al brief, y por qué

| Pedía el brief | Se hizo | Motivo |
|---|---|---|
| Los siete parámetros de FundedNext a **UNKNOWN con `ambiguedad_id`** | Cinco a **DEFAULT_AMBIGUOUS** bajo A-27 y dos a **UNKNOWN** bajo A-28 | El registro solo admite `ambiguedad_id` en DEFAULT_AMBIGUOUS, y `spec check` falla si una regla vigente (RN-026, RN-027) nombra un UNKNOWN. **Lo decidió el consultor** antes de escribir: modo mixto, A-27 partida en dos y el paso a UNKNOWN condicionado a las guardias |
| Una sola A-27 | **A-27** (instrumento, `[F17, F33]`) y **A-28** (reloj, `[F17]`) | Petición del consultor: son dos mediciones con sitio y momento distintos, como A-16 en ADR-0024 |
| A-27 sin más | **Reserva de A-24..A-26** en `test_kit` (`IDS_RESERVADOS`), con aserción de que no existen | `test_kit` exigía ids correlativos sin huecos. Petición del consultor: la exención se autoliquida el día que el brief de la geometría cree A-24 |
| RN-029 consume `detenido_por_tope` | Lo consume, y **ya no cierra nada** | La guardia `test_los_hechos_declarados_coinciden_con_lo_que_las_formas_hacen` exige que quien fija un freno lo lea. El cierre, que por eso se disparaba también con el freno del trader y en cada evento, se mudó a RN-030 al validar (§5, corrección del 2026-09-14) |
| Dos reglas de la spec | Tres: **RN-020 también** | Su `cuando` decía que el corte «cae en el reloj del servidor», que ADR-0027 vuelve falso. Deja de nombrar `broker_dst` y `broker_offset_base`, y su `decision` pasa a ADR-0027. Es el tercero de los cuatro sitios que el HANDOFF manda tocar al cerrar una ambigüedad |
| RN-028 a DESCARTADA | DESCARTADA **y sin `forma`** | `comprobar_forma` revisa también las descartadas, y su `pendiente_definicion: A-17` apuntaba a una ambigüedad ya cerrada |
| `reloj_dia_riesgo`: `servidor` → `civil_operativa` | Además, la opción `grafico` se sustituye por `civil_operativa` | El gráfico del trader está en el mismo huso: serían dos puertas para el mismo instante (ADR-0002) |
| «Sin punto fijo se rebasa el tope (4,889 %)» | ADR-0028 lo matiza | La auditoría dice que **con** punto fijo se evita la 11.ª orden, pero el tope sigue rebasado (4,885 %), porque `alcanza_tope` no descuenta la operación que se abre. Esa lectura prospectiva queda como decisión abierta (§6) |
| «Con 4,5 lotes, el margen cabe de sobra» | Cabe **con ese stop**, no con cualquiera | Margen = 166.667 × P / d (d, stop en pips; P, precio de EURUSD). Supera los 100.000 de la cuenta con un stop de menos de 1,67 × P pips (1,95 con P = 1,17). F21 lo comprueba |
| `saldo_inicial_cuenta`: «su descripción nombra a FundedNext» | No la nombraba; se reescribió igual | Decía «NO es la base de ningún cálculo», y con FTMO **sí** es la base de los topes de la firma |
| Guardia de literales ampliada a `prop_firm` | Hecho, y además `FTMO` entra en los textos prohibidos en `src/` | Mismo criterio que `FundedNext` |

**Las tres guardias de `DECIDIDA` (criterio 4 del brief), una por una.** El ADR existe y nombra la
ambigüedad: pasa en A-17 (ADR-0026) y en A-19 (ADR-0027). Ninguna de las dos es bloqueante. Y la
tercera —no cerrar por decisión una que sostiene el default de un parámetro— **no se quejó, y hay
que decir por qué, para que nadie lo lea como un rodeo**:

- **A-17**: `filtro_noticias` era CONFIRMED por ADR-0022 y no declaraba `ambiguedad_id`. No
  sostenía ningún default.
- **A-19**: `reloj_dia_riesgo` **sí** lo sostenía (DEFAULT_AMBIGUOUS, `ambiguedad_id: A-19`). La
  guardia no salta porque, en el mismo cambio, el parámetro deja de ser un default nuestro: su
  valor pasa a ser el que escribe el reglamento (`civil_operativa`, CONFIRMED, fuente ADR-0027).
  Eso es lo que la guardia protege —que el bot no corra con una suposición nuestra por culpa de una
  pregunta cerrada por decisión— y aquí la suposición desaparece, no se esconde. Si se juzga que un
  reglamento leído por el consultor no basta para CONFIRMED sin verlo en el panel, la alternativa
  honesta es dejar A-19 ABIERTA y el parámetro en DEFAULT_AMBIGUOUS con el valor nuevo (§6).

Otros hallazgos de la rama:

- **ADR-0028 punto 5 no está aplicado a la spec.** RN-010, RN-011 y RN-013 siguen fijando
  `operacion_abierta` y `orden_limite_pendiente`, así que hasta el brief siguiente la spec contradice
  un ADR ACTIVE. Está dicho en el propio ADR. F18 no debería empezar sin ese cambio.
- **Dos BACKSPACE literales en el HANDOFF**, uno heredado de antes: la lección de F11 sobre `\b` en
  heredocs estaba escrita con el defecto que describe. Arreglados los dos. Queda uno en
  `docs/plan/features/F04-transcription-pipeline.md`, fuera de alcance.
- **Mi `make check` no expuso el holdout**: `knowledge validate` carga los YAML del paquete sin
  datos (`esquema_paquete`), y los tests del kit construyen repositorios temporales.

## 5. La auditoría de cierre

Dos agentes en paralelo (Sonnet, sin permiso de escritura y con prohibición expresa de ejecutar
`kit check` o leer `data/` y el holdout): uno sobre conocimiento, spec y tests, y otro sobre ADR,
documentos vivos y proceso.

**ADR y documentos: sin hallazgos graves.** Comprobó una a una las citas de la auditoría en ADR-0028,
0029 y 0030 contra su texto y su sección, que ningún ADR afirma más que el reglamento verificado
(el ejemplo de 100.000 va declarado como cuenta nuestra, el calendario de horario de verano como no
nombrado, el BID de FX Replay como no verificado), que no queda en los documentos vivos ninguna
afirmación ya falsa (FundedNext vigente, día de servidor, RN-028 vigente, A-17 o A-19 abiertas) y
que los commits de `knowledge/spec` llevan `Fuente:`. Dos menores, aplicados: «once parámetros
`firma_*`» cuando uno se llama solo `firma`, y el propio informe, que aún no estaba commiteado.

**Spec, registro y tests:**

| Hallazgo | Gravedad | Qué se hizo |
|---|---|---|
| A-27 y A-28 citaban solo `ev-v4-012524-0ef85a89` (los límites que el trader recordaba de FundedNext), sin relación con digits, lotes o husos | grave | **Corregido.** A-27 cita además el instrumento leído en pantalla (`ev-v2-003320-a736fd37`) y el lotaje de la prueba de fondeo (`ev-v4-012900-8ef676ed`); A-28, la H4 que el trader ve abrir a las 23 (`ev-v6-005830-48b30e48`) y lo que dice del cambio de hora (`ev-v6-005810-5cb1ef06`). Se conserva la de la firma, que es dónde se midió lo que no se hereda |
| A-27 y A-28 son mediciones, pero `cuestionario.py` mete toda ambigüedad ABIERTA en la sesión siguiente, y `spec status` pone `broker_dst` y `broker_offset_base` bajo «falta preguntarlo» | grave | **No se toca** (alcance cerrado, y le pasa igual a A-16 desde el 09-12). Va a §6 |
| El literal de RN-029 se cortaba en «O un 10» y escondía que el trader cierra en «8, 8. Un 8, sí» | media | **Corregido**: el literal llega hasta el final y las notas dicen que ese 8 % era de otra firma |
| `reinicia_con: firma_perdida_total_arrastra` apunta a un booleano, no a un reloj o un evento | media | **Se deja declarado**: la descripción del acumulador lo explica, y ADR-0030 ya anota que `reinicia_con` no distingue tipos de reinicio. Deuda de la spec, fuera de esta rama |
| El tope total fija `hasta_el_corte_siguiente` como el diario, y las notas dicen que es permanente | media | **Aclarado en las notas**: como `perdida_total_firma` no se reinicia, RN-029 vuelve a disparar en el primer evento tras el corte. No hay guardia que lo compruebe |
| El efecto de leer `detenido_por_tope` | — | El auditor lo dio por bien razonado; el consultor no, y lo corrigió al validar (fila siguiente) |

**Correcciones del consultor al validar (2026-09-14).** La rama se aprobó con estas correcciones
dentro de ella, y vuelve a WAITING_FOR_USER_VALIDATION:

| Fecha | Hallazgo | Quién | Qué se hizo |
|---|---|---|---|
| 2026-09-14 | RN-029 usaba `OP` en `entonces` (`cerrar_a_mercado: {de: OP}`) **sin ligarlo en `cuando`**: la única de las reglas de la spec que lo hacía (RN-002 y RN-014 lo ligan). Ninguna guardia lo vio, porque `OP` es también un token declarado | consultor | **La forma no puede expresarlo dentro de RN-029**: su `cuando` es un `cualquiera_de`, la prohibición tiene que valer sin posición, y ADR-0019 no da semántica a una ligadura atada en una sola rama ni a una acción condicionada dentro de `entonces`. No se fuerza. Con el vocabulario que ya existe, el cierre **se parte a una regla nueva, RN-030** (`gate`, `complementa: [RN-029]`): `todos_de` con los dos `alcanza_tope` de la firma y `hecho: operacion_abierta, liga: OP`, como RN-002. RN-029 se queda con `prohibe` y `fijar`. **Es una decisión a validar** (§6): la alternativa era dejar RN-029 como estaba y llevar el hallazgo al brief siguiente. ADR-0030 anota el límite del árbol |
| 2026-09-14 | `cerrar_a_mercado {si: "si"}` llevaba un literal donde RN-002 usa `cierre_forzoso_fin_ventana`; y como RN-029 lee `detenido_por_tope`, que dura hasta el corte, habría emitido un cierre en cada evento mientras el bot está parado, contra `firma_mensajes_dia_max` | consultor | **Resuelto por las dos vías**: la ligadura de RN-030 hace que sin posición viva no dispare (y no lee `detenido_por_tope`, así que tampoco cierra por el freno del trader), y `si` pasa a ser el parámetro nuevo **`firma_cierre_al_tope`** (`prop_firm`, `si`, fuente ADR-0026) |
| 2026-09-14 | A-28 no pedía verificar el corte del día de riesgo en el panel | consultor | A-28 gana el punto explícito: confirmar en el panel de FTMO que el límite diario se recalcula a **medianoche CE(S)T y no a la medianoche del servidor** (se separan una hora). `reloj_dia_riesgo` **se queda CONFIRMED**, no se añade a los parámetros de A-28 (lo sacaría como «en revisión» en `spec status`), y su descripción remite a esa comprobación |

**Al brief siguiente, NO a esta rama** (lo decide el consultor): `firma_magnitud_vigilada` no tiene
lector ejecutable —el equity solo vive en la prosa de los acumuladores—; `detenido_por_tope` necesita
un valor permanente para el tope total; y `perdida_total_firma.reinicia_con` debería ser un token de
«nunca» y no un booleano. Y un candidato a guardia que sale de la primera fila: una acción que usa una
ligadura tiene que tenerla atada en un `todos_de` del `cuando`.

Comprobado por el auditor en una copia sin `data/`: crear una A-24 falsa hace fallar
`test_ambiguedades_reales_y_esquema` (la reserva se autoliquida), y poner `firma_perdida_diaria_max`
en 4,9 hace fallar la guardia de valores vigilados (la ampliación a `prop_firm` muerde). Toda la
aritmética de ADR-0026 y RN-029 cuadra con Python. Ninguna guardia quedó más débil.

## 6. Qué debe decidir el usuario

1. **¿Validar la rama y hacer el ritual** (merge `--no-ff`, tag `stable/F13-ftmo`, `docs(state)`)?
2. **A-19: ¿basta el reglamento para CONFIRMED?** Está cerrada como DECIDIDA con
   `reloj_dia_riesgo = civil_operativa` CONFIRMED, porque lo escribe el reglamento. Si prefieres
   verlo en el panel de la prueba gratuita antes, la alternativa es A-19 ABIERTA y el parámetro en
   DEFAULT_AMBIGUOUS con el valor nuevo. No cambia lo que el bot hace, solo lo que se afirma.
3. **Las mediciones en el cuestionario.** A-16, A-27 y A-28 entrarían en el `kit build` de la sesión
   2 como preguntas al trader, y `spec status` llama «falta preguntarlo» a los parámetros de A-28.
   Opciones: un campo en `ambiguedades.yaml` que distinga medición de pregunta (código, rama
   propia), o recordarlo al construir la sesión 2. Recomiendo el campo: el cuestionario es lo único
   que se ejecuta delante del trader.
4. **Margen antes del límite de la firma.** Llegar al 5 % o al 10 % ya es la infracción. Hoy nada deja
   margen: RN-029 y RN-030 disparan al alcanzarlo, y el tope del trader se rebasa por construcción hasta
   ~4,9 % porque no descuenta la operación que se abre (auditoría del 09-13, [d1-interprete-04]).
   ¿Se decide ahora un margen o una lectura prospectiva del tope, o se deja a F21-F24?
5. **ADR-0029 punto 1, sin verificar.** ¿Se le pregunta al trader —o se mira en su FX Replay— si
   sus velas son BID? Si fueran ASK o medio, se abre ambigüedad.
6. **RN-030.** ¿Se acepta partir el cierre de la firma en una regla propia, o se prefiere revertir a
   RN-029 sin cierre y llevar el cierre entero al brief siguiente, junto con la ampliación de
   ADR-0019 que permitiría expresarlo en una sola regla?
7. **El orden del siguiente brief.** ADR-0028 punto 5 (derivar `operacion_abierta` y
   `orden_limite_pendiente`) no está en la spec; conviene que vaya en el mismo brief que las
   correcciones de fidelidad (RN-005, la acción que coloca la orden límite, `equal`, RN-013/RN-015)
   y antes de F18.

## 7. Lo que tiene que hacer el dueño, en paralelo

1. **No comprar todavía.** El tipo Swing se elige en la compra y Standard → Swing no existe.
   Confirmar en el panel de FTMO que Swing está disponible para 100.000 y para su región, y con qué
   apalancamiento.
2. **Abrir la prueba gratuita de FTMO y medir en MT5**: `digits`, tamaño de contrato, lote mínimo,
   paso y máximo, `stops_level`, `freeze_level`, modos de llenado (cierra A-27); desfase del reloj
   del servidor y rejilla H4 real (A-28, que además necesita ver el cambio de hora de octubre).
3. **Grabar spread y ticks de esa demo desde el primer día.** Es el dato irrecuperable.
4. **Pedirle al trader el mes limpio** (febrero o marzo de 2026). Sigue pendiente desde el 09-13.
5. **Declarar en `HOLDOUT-EXPOSICIONES.md` la exposición de la auditoría del 09-13**: un agente
   ejecutó `kit check` con `data/` presente, lo que recompone `ventanas.yaml` leyendo velas M1 de
   días reservados de mayo. No se leyó ninguna etiqueta ni ningún precio. Por ADR-0021 se declara
   igual. Esta rama **no** la ha escrito: esa tabla la firma quien vio, y el brief la deja al dueño.

## 8. Cómo comprobarlo

```
git checkout trabajo/ftmo-y-arquitectura
make check                                  # 663 casos; state check con la rama
uv run botsito spec check                   # RN-029 y RN-030 vigentes y ejecutables; RN-028 descartada
uv run botsito spec status                  # A-17 y A-19 en "cerradas por decision"; A-27 y A-28 en revision
uv run botsito knowledge validate           # guardias de DECIDIDA, trailers Fuente
git diff 0a9612d..HEAD --stat -- knowledge/evidence knowledge/feedback   # vacio
```

## Estado
WAITING_FOR_USER_VALIDATION
