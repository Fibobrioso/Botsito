# BARRIDO-SESION-6 · la sesión 6 con el trader, lista antes de grabar (R4.2)

Rama `trabajo/barrido-sesion-6`, abierta el 2026-10-28 desde `main` b929de2 (commit de estado sobre
el merge d5f6b81, tag `stable/F38h-cuarentena-por-condicion-2`). Encargo:
`docs/encargos/trabajo-barrido-sesion-6.md`. Tramo R4 de `docs/plan/HOJA-DE-RUTA.md`.

## Apertura: la base, comprobada con git

| Comprobación | Salida |
|---|---|
| `git rev-parse main origin/main main^1` | b929de2d9698d3aab3ec9addba8e16548f00bda4 (dos veces) y d5f6b81bb05a2ba43fe1208976a5903e63ce3ac4 |
| `git rev-parse "stable/F38h-cuarentena-por-condicion-2^{commit}"` | d5f6b81bb05a2ba43fe1208976a5903e63ce3ac4 = `main^1`; en origin (`git ls-remote --tags origin "stable/F38*"`), y es el último F38 |
| último `- Tag: ` de HISTORIA | `stable/F38h-cuarentena-por-condicion-2` (línea 13582) |
| `gh run view 40754656734 --json headSha,status,conclusion,headBranch` | `{"conclusion":"success","headBranch":"main","headSha":"b929de2d9698d3aab3ec9addba8e16548f00bda4","status":"completed"}` |
| `git branch --list` / `git ls-remote --heads origin` | solo `main` |

Tag previsto del cierre: `stable/F38i-barrido-sesion-6` (el último es F38h).

## 0. Qué se abrió (exposición)

- **Informes, ADR, spec y runbooks** que nombra el encargo, leídos con Read y Grep:
  `ACTIVAR-SESION-05.md` §3, `ACTIVAR-SESION-05-MOTOR.md` §2, `RECORRIDA-CONSTRUCCION.md` §3 y §4,
  `SESION-05-EXTRACCION.md` §5, ADR-0084 y ADR-0086, `knowledge/spec/ambiguedades.yaml`,
  `knowledge/spec/parametros.yaml`, `docs/runbooks/SESION-DE-PREGUNTAS.md`,
  `docs/plan/HOJA-DE-RUTA.md` (R4), `knowledge/corpus/fuentes.yaml` (los comentarios de v15 y v16,
  sin abrir los vídeos).
- **Los anexos commiteados de la re-corrida** (`docs/validation/anexos/RECORRIDA-CONSTRUCCION/`):
  `lista-s14.txt`, `patrones-diaria.txt` y `diaria.DIAGNOSTICO.cuenta=diaria.txt` (secciones «Por
  operacion», «### Ordenes» y «Reglas disparadas por sesion»), leídos por un guion de la carpeta de
  trabajo de la sesión (fuera del repo) que solo extrae las filas de las 34 sesiones de P6. Son de
  la corrida de construcción (enero, abril, julio y agosto); ninguna fila es de un día reservado.
  Las operaciones del trader de esos días salen de ese anexo (los casos dev que el arnés carga),
  nunca de un xlsx.
- **`casos_ocultos`**, por recuento: un guion de la carpeta de trabajo comprobó, para cada uno de
  los 30 candidatos, los días de calendario (en Madrid y en UTC) que tocaría su gráfico; imprime
  solo cuántos dan `True` (0 en los 30). Ninguna clave impresa.
- **`uv run botsito feedback pending`** (solo ids y estado).
- **Nada más**: ninguna vela, ningún tick, ninguna transcripción, ningún ítem de evidencia, ningún
  fotograma, ningún libro, ningún caso. **Declarado** en `HOLDOUT-EXPOSICIONES.md`, fila del
  2026-10-28 (este mismo commit).

## 1. Fase 0 · Inventario (2026-10-28)

Medido en la rama sobre `main` b929de2. Nada escrito fuera del informe, el encargo, el contrato,
`PROJECT_STATE.md`, HISTORIA y la fila de exposiciones.

### 1.a La lista completa de D1, una fila por cosa

Estado y valor: los de hoy, con su línea de `knowledge/spec/parametros.yaml` (medidos con un guion
que lee el fichero, no de otro informe). «Ya registrado»: lo que el trader ya dijo, con su id.

**ACTIVAR-SESION-05.md §3 (13 puntos), con lo que MOTOR §2 le junta:**

| # | Cosa | De dónde sale | Nombra | Estado y valor hoy | Ya registrado |
|---|---|---|---|---|---|
| 1 | A-44, la magnitud: ¿cuenta lo abierto? | ACTIVAR-SESION-05.md:1006-1011 (§3.1) | A-44 (bloqueante), RN-020, `perdida_trader_magnitud` | DEFAULT_AMBIGUOUS `saldo` (`parametros.yaml:1475-1476`), lectura del consultor | la base del porcentaje, «De la cuenta basado en el saldo, y que sea en el saldo inicial del día» (`fb-2026-09-09-sesion-01-bff260ea`; habla de la BASE, no de si lo abierto cuenta, `parametros.yaml:1466-1470`); el alcance `dia` (`fb-2026-10-23-sesion-05-e9559876`) y la unidad `porcentaje` (`fb-2026-10-23-sesion-05-1772d9ef`), CONFIRMED |
| 2 | A-44, el reloj del reinicio | ACTIVAR-SESION-05.md:1011-1014 (§3.1) | A-44, `perdida_trader_reinicio_huso` | UNKNOWN (`parametros.yaml:1530`); tipo `texto`, «nombre IANA del huso cuya medianoche reinicia el conteo» (`:1524`): la opción (c) de §3.1 no cabe | nada |
| 3 | A-35, la mecha (i) de la contraria o (ii) también de una posterior, y el bajo | ACTIVAR-SESION-05.md:1015-1019 (§3.2), **ampliada y sustituida por** MOTOR:732-737 (§2.1) | A-35 (bloqueante), RN-004, `liquidez_m15_mecha_que_vuelve` | DEFAULT_AMBIGUOUS `cualquier_mecha` (`parametros.yaml:554-555`), lectura del consultor (ADR-0084) | «se actualiza el de la mecha» (`ev-v15-000553-9d95178a`); «en cuanto la vela roja de después ya cerrado» (`ev-v15-000447-6699c708`) fijó `liquidez_m15_pivote_formado` = `cierre_vela_contraria`, CONFIRMED (`:526-527`) |
| 4 | A-13, el break even al toque o al cierre de M1 | ACTIVAR-SESION-05.md:1020-1025 (§3.3) | A-13, RN-014, `break_even_condicion` | CONFIRMED `tocar` (`parametros.yaml:931-932`) | «apenas toque» (`ev-v15-013605-c041b814`); «apenas toca» (`fb-2026-09-29-sesion-03-9f506366`); y lo contrario en la sesión 4 (S-17 de la 5, «se contradice dentro de la respuesta», SESION-05-EXTRACCION.md:1220) |
| 5 | A-53, la subpregunta del recuadro y la orden llenada antes del punto nuevo | ACTIVAR-SESION-05.md:1026-1030 (§3.4) | A-53, `orden_pendiente_al_abrir_escenario` | DEFAULT_AMBIGUOUS `se_mueve` (`parametros.yaml:854-855`) | en parte, hacia (b) (S-13 de la 5, SESION-05-EXTRACCION.md:1216) |
| 6 | A-43, la segunda parte (la misma liquidez antes y después de las 7) | ACTIVAR-SESION-05.md:1031-1034 (§3.5) | A-43, `toma_antes_de_la_ventana` | CONFIRMED `cuenta` (`parametros.yaml:788-789`), la primera parte | la primera parte (`fb-2026-10-04-sesion-04-c3d0c855`); la segunda, en parte (S-10 de la 5) |
| 7 | A-49 y A-48, el 0 y el 1 de la caja, cerrada o en formación | ACTIVAR-SESION-05.md:1035-1038 (§3.6) | A-48, A-49, `caja_bloque`, `caja_se_fija`, `orden_stop_punto` | DEFAULT_AMBIGUOUS `r6` (`:708-709`), `en_cada_cierre_m1` (`:735-736`) y `ultimo_pivote_m1` (`:687-688`) | en parte (S-7 de la 5: la traza al cierre, el 1 se actualiza, sin elegir opción) |
| 8 | A-50, «la caja entera» con dos dibujos | ACTIVAR-SESION-05.md:1039-1042 (§3.7) = MOTOR:763 (§2.7) | A-50, RN-005, `caja_lado_de_ruido` | DEFAULT_AMBIGUOUS `caja_entera` (`parametros.yaml:762-763`), lectura del consultor | en parte (S-12b de la 5, `ev-v15-010451-5b123278`) |
| 9 | ADR-0083: cuántas reentradas, qué caja, y tras un break even | ACTIVAR-SESION-05.md:1043-1047 (§3.8) | ADR-0083 (PROVISIONAL en D1), RN-016, RN-019 | sin parámetro | en parte (S-6 de la 5: se actualiza el 0 y el 1 sigue; sin número) |
| 10 | S-16, el precio ya más allá del 0 al formarse la caja | ACTIVAR-SESION-05.md:1048-1050 (§3.9) | ADR-0057 | sin parámetro | no resuelve (S-16 de la 5) |
| 11 | S-19 frente a S-24: la vela de 1 o 2 puntos, y las mechas de una vela sin cuerpo en M1 | ACTIVAR-SESION-05.md:1051-1055 (§3.10); el valor de hoy, MOTOR:738-739 (§2.2) y :761-762 (§2.6) | RN-007, RN-009, ADR-0085 §3 | sin parámetro: la vela de 1 o 2 puntos sigue siendo de su color y las mechas de la vela sin cuerpo cuentan donde cuentan (ADR-0085 §3, decisión del consultor) | S-19 y S-24 de la 5, resueltas en sentidos que chocan (SESION-05-EXTRACCION.md:1222, :1227) |
| 12 | S-20: la mecha que rompe frente a la alternancia | ACTIVAR-SESION-05.md:1056-1058 (§3.11) | RN-009, ADR-0076 §4, ADR-0085 | sin parámetro | en parte (S-20 de la 5) |
| 13 | S-14: los días en que el bot opera y él no | ACTIVAR-SESION-05.md:1059-1064 (§3.12) + RECORRIDA-CONSTRUCCION.md:1287-1350 (§4) | P6; deuda «el no_trade por ausencia» | sin parámetro | en parte (S-14 de la 5: se salta sesiones que iban a break even en los backtests sin vídeo) |
| 14 | S-11 «en parte»: la toma de la mañana con el MISMO sesgo por la tarde | ACTIVAR-SESION-05.md:1065-1073 (§3.13) | A-46 (RESUELTA, sin tocar) | sin parámetro | `ev-v15-005839-f2e43c27`, primera mitad; A-46 respondida al revés (`fb-2026-09-29-sesion-03-5021677e`) |

**Lo que MOTOR §2 añade y §3 no tiene:**

| # | Cosa | De dónde sale | Nombra | Estado hoy | Ya registrado |
|---|---|---|---|---|---|
| 15 | En M15, ¿una vela sin cuerpo entre la racha y la contraria corta la racha? | MOTOR:740-743 (§2.3) | A-35, `pivotes_m15` (ADR-0085 §2) | la corta (sin parámetro) | nada |
| 16 | La condición de `ev-v15-004037-a2ab3980` (romper cerrando por debajo, flujo bajista) | MOTOR:744-749 (§2.4) | ADR-0085 §3 (no aplicada) | basta con que sea roja (en M1 la mecha siempre vale, A-32 RESUELTA) | el propio ítem, sin aplicar |
| 17 | S-15, dibujo 2 (alternancia en el primer retroceso, el segundo punto limpio) | MOTOR:750-756 (§2.5) | RN-009, ADR-0076 | sin parámetro | S-15 de la 5 resolvió «la zona más reciente» (SESION-05-EXTRACCION.md:1218) |
| 18 | S-15, dibujo 3 (la orden en el primer punto, llenada antes de la alternancia) | MOTOR:756-760 (§2.5) + RECORRIDA-CONSTRUCCION.md:976-1018 (§3: 259 llenadas con menos de dos zonas, 149 con cero y 110 con una) | RN-009 | sin parámetro | ídem |

**La tabla final de SESION-05-EXTRACCION.md §5** (:1198-1229), filas «en parte» y «no resuelve»:
S-3 → fila 3; S-4 → filas 1 y 2; S-6 → fila 9; S-7 → fila 7; S-10 → fila 6; S-11 (recuadro) →
fila 14; S-12b → fila 8; S-13 → fila 5; S-14 → fila 13; S-16 → fila 10; S-17 → fila 4; S-20 → fila
12. **Todas cubiertas por §3 o por MOTOR §2.** S-25 (en parte) → fuera (fila 25). Medido.

**Las ambigüedades ABIERTAS** (`ambiguedades.yaml`, Known Ambiguities de PROJECT_STATE.md:75-89):
de clase `pregunta`, exactamente A-13, A-35, A-43, A-44, A-48, A-49, A-50 y A-53 (verificado: las
ocho y ninguna más), todas ya arriba. De clase `medicion`: A-16, A-28, A-54, A-55 y A-56 → fuera
(fila 21).

**Las candidatas C1-C7** (PROJECT_STATE.md:92) y **el feedback pendiente** (`feedback pending`:
«2 pendientes de 139 activos», `fb-2026-09-29-sesion-03-31fb311f` y
`fb-2026-10-04-sesion-04-ca0afae6`, los dos CORRECT de RN-003: el falso positivo de G.2,
verificado):

| # | Cosa | Destino |
|---|---|---|
| 19 | C1, la orden pendiente cuando aparece una caja nueva | se junta con la fila 5 (A-53): ADR-0074 ya dice que la orden sigue al 1 nuevo y `ev-v10-015716-5ea2575f` lo responde («no vamos a dejar en un punto de breaker antiguo»), como dejó la sesión 5 (BARRIDO-SESION-5.md:91, :622) |
| 20 | C2 y C3 | son A-48 y A-49 (fila 7) |
| 21 | C4, C5, C6; A-16, A-28, A-54, A-55, A-56; los dos CORRECT de RN-003 | fuera: C4, C5 y C6 tienen su ambigüedad RESUELTA (A-18, A-29, A-36; BARRIDO-SESION-5.md:93-95); las de `medicion` se miden; los dos CORRECT son el falso positivo de G.2 |
| 22 | C7, cuánto vive una orden stop sin llenar | fuera: la sesión 5 lo respondió (S-22, «un minuto antes», RN-035, SESION-05-EXTRACCION.md:1225, activada en ADR-0086 y la rama de motor), y lo que queda es A-53 (fila 5) |

**Lo que manda algo «a la sesión 6»** (Grep en `knowledge/spec`, `docs/adr`, `docs/validation`,
`docs/plan` y `docs/runbooks`): todo cae en filas de arriba (A-44 `ambiguedades.yaml:1362-1363`;
A-35 `:975`, `:1010-1018`, `parametros.yaml:549`, `strategy_spec.yaml:614`, `:1291`, `:1302`; A-50
`parametros.yaml:761`, `strategy_spec.yaml:1374`, `ambiguedades.yaml:1557`; la vela sin cuerpo
`strategy_spec.yaml:1466`; ADR-0083, ADR-0085, ADR-0076 §4) salvo dos:

| # | Cosa | De dónde sale | Destino propuesto |
|---|---|---|---|
| 23 | «El nivel se congela al tomarse», DECISIÓN DEL CONSULTOR con efecto visible: una M1 que cierra con cuerpo sobre el nivel ORIGINAL ya no es toma si una mecha anterior lo movió | ADR-0084:41-48 (hallazgo b5 del revisor de la rama de motor) | **dentro de la pregunta de A-35 (fila 3), como «Para precisar»**: es la consecuencia directa de (ii) y solo se entiende con su dibujo; no gana código propio (decisión 2) |
| 24 | Preguntar al trader si RN-020 retira la orden pendiente al llegar al tope | ADR-0086:56 y :66 (alternativa 3, descartada) | fuera: el consultor la descartó en ADR-0086 («sin que el trader haya mostrado ninguna preferencia distinta a la de RN-036»); no es una nota que la mande a la sesión 6 |
| 25 | S-25, el Excel de julio y los tres primeros vídeos | SESION-05-EXTRACCION.md:1228; ACTIVAR-SESION-05.md:1083 («lo mide T») | fuera: lo mide T (R2.4) |
| 26 | «Para cerrar»: diciembre con su voz (NA:I) y la exportación de agosto (NA:Q) | PROJECT_STATE.md:42 (I), :50 (Q); D4 punto 4 | bloque «Para cerrar», sin código, cada una con «si ya lo contestó por WhatsApp, se salta» |

### 1.b Lo que se junta y lo que va fuera

**Se juntan:**
- **§3.2 + MOTOR §2.1** (fila 3): gana el texto de MOTOR §2.1 (D1). Con ADR-0084:41-48 (fila 23)
  como «Para precisar», si el consultor lo acepta (decisión 2).
- **§3.7 = MOTOR §2.7** (fila 8): la misma pregunta; MOTOR solo añade el valor de hoy.
- **§3.10 + MOTOR §2.2 + MOTOR §2.6** (fila 11): el texto es el de §3.10; MOTOR da el valor de hoy
  de sus dos preguntas (ADR-0085 §3), que va a «Para Aleks».
- **§3.12 + RECORRIDA §4** (fila 13): los días reales salen de §4 (D5).
- **MOTOR §2.5 + RECORRIDA §3** (filas 17 y 18): dos preguntas, una por dibujo (D2: S-15 solo con
  sus esquemas, sin días reales).
- **A-53 + C1** (filas 5 y 19).

**Fuera de la hoja, con su porqué:** filas 21, 22, 24 y 25 (y las de `medicion`).

**Desacuerdo medido entre la hoja de ruta y los informes** (D1: gana el informe más reciente, y la
línea va al punto 7): R4.2 «Qué es» (`HOJA-DE-RUTA.md:244-261`) **no nombra** la fila 23
(ADR-0084, el nivel congelado) ni la ampliación de §3.2 por MOTOR §2.1 la pone en su sitio (la
nombra aparte, :250-252); y dice «S-14 con las 34 sesiones de P6» sin las 4 que salen (3 E y la
del 1 de abril). La línea irá en «Líneas preparadas para el commit del contrato de la orden de
cierre», al final del informe.

### 1.c El orden (D4), la duración de la sesión 5 y la estimación de la 6

**La sesión 5 duró 2:15:47** (v15 1:40:57 = 6057,2 s, `fuentes.yaml:167`; v16 34:50 = 2090,0 s,
`:185-186`; sin abrir los vídeos), con 25 códigos y «Para cerrar»: **5:26 por código** de media
(8147,2 s / 25), el mismo método que para la sesión 4 (5:19). S-14 de la 5, sin gráficos, ocupó
11:17 (v15 69:10–80:27, SESION-05-EXTRACCION.md:1217). «Para cerrar», 2:31 (v16 32:10–34:41).

**El orden propuesto, 23 códigos:**

| S | Bloque | Pregunta | Filas |
|---|---|---|---|
| S-1 | 1 | A-44: la pérdida del día, ¿solo con las cerradas o también con la abierta? | 1 |
| S-2 | 1 | A-44: cuándo vuelves a contar desde cero | 2 |
| S-3 | 1 | A-35: la mecha que mueve el alto (de la contraria o también de una posterior), y el bajo | 3 (+23) |
| S-4 | 1 | En M15, la vela sin cuerpo entre la racha y la contraria | 15 |
| S-5 | 2 | S-15, dibujo 2: el segundo punto limpio tras un retroceso con alternancia | 17 |
| S-6 | 2 | S-15, dibujo 3: la orden llenada antes de la alternancia | 18 |
| S-7 a S-12 | 2 | S-14: «Gráfico 1» a «Gráfico 6», uno por código (D7) | 13 |
| S-13 | 3 | A-13: el break even al toque o al cierre de M1 | 4 |
| S-14 | 3 | A-53: la orden sin llenar cuando el 1 baja mucho, y la llenada antes del punto nuevo | 5 |
| S-15 | 3 | A-43: la misma liquidez antes y después de las 7 | 6 |
| S-16 | 3 | A-49 y A-48: el 0 y el 1 de la caja | 7 |
| S-17 | 3 | A-50: solo el 0 o la caja entera | 8 |
| S-18 | 3 | ADR-0083: las reentradas en el mismo punto | 9 |
| S-19 | 3 | S-16: el precio ya más allá del 0 al formarse la caja | 10 |
| S-20 | 3 | La vela de 1 o 2 puntos y la vela sin cuerpo con mechas largas | 11 |
| S-21 | 3 | La mecha que rompe frente a la alternancia | 12 |
| S-22 | 3 | Para que el máximo de la verde sea punto de breaker, ¿la roja tiene que cerrar por debajo? | 16 |
| S-23 | 4 | S-11 «en parte»: la toma de la mañana con el mismo sesgo por la tarde | 14 |
| — | 4 | «Para cerrar»: diciembre con su voz; la exportación de agosto | 26 |

**El bloque 3 va en el orden de ACTIVAR-SESION-05.md §3 y después MOTOR §2, no por decisiones del
bot**: los anexos commiteados no lo miden. «Reglas disparadas por sesion»
(`diaria.DIAGNOSTICO.cuenta=diaria.txt:32-54`) cuenta sesiones en que una regla disparó, no
decisiones que cambiaría cada opción (RN-005 dispara en 127 de 152 sesiones con cualquier valor de
A-50, por ejemplo), y ninguna salida guarda qué opción de un parámetro decidió una orden. Medirlo
pide correr el motor con cada opción, que el encargo no autoriza.

**La estimación de la 6:** 17 códigos sin gráfico × 5:26 = 1:32:22, más S-14 a 3 minutos por día
(6 × 3 = 18:00), más «Para cerrar» (2:31): **unas 1:53**. Por debajo de 2 horas, con poco margen
(S-14 de la 5 se llevó 11 minutos sin gráficos; con seis días y tres pasos cada uno, los 3 minutos
por día son el supuesto del encargo, no una medida). **Propuesta (decisión 3):** una sola sesión;
si a la hora y media no se ha llegado a S-17, se corta ahí y el resto (S-17 a S-23) va a un segundo
día, como la 5. Para WhatsApp, si hace falta: «Para cerrar» (ya previsto) y S-22.

**Encabezado de PREGUNTAS.md (D4):** «Antes de grabar: la copia de seguridad de v15 y v16 (crudas y
audios, SESION-05-EXTRACCION.md §12) en el Drive de A.4». Medido: PROJECT_STATE.md:142 dice «hecha
hasta v10 … Cada sesión nueva se añade tras su ingesta», y no consta la de v15 y v16.

### 1.d Los candidatos de S-14 (D5): 30 filas, sin R

**El recuento, verificado:** 34 sesiones en `RECORRIDA-CONSTRUCCION.md:1300-1335` (enero 7, abril
14, julio 1, agosto 12); fuera las 3 marcadas E (2026-04-06 11-15, 2026-04-07 07-11 y 2026-04-07
11-15; las dos «posible M» son 04-06 y 04-07 de 11-15) y la del 1 de abril (07-11); el 1 de julio
no tiene fila. **Quedan 30: 7 de enero, 10 de abril, 1 de julio y 12 de agosto.** Por clase: 20
«en sesión» y 10 «en día» (enero, 7 y 0; abril, 4 y 6; julio, 1 y 0; agosto, 8 y 4). Por sesión:
11 de 07-11 y 19 de 11-15 (enero, 1 y 6; abril, 4 y 6; julio, 1 y 0; agosto, 5 y 7).

Columnas: «P6», de `patrones-diaria.txt`; las operaciones del trader, de «Por operacion» de
`diaria.DIAGNOSTICO.cuenta=diaria.txt` (los casos dev que carga el arnés), en hora de Madrid; la
primera orden del bot, de «### Ordenes» de ese mismo fichero (la M1 en cuyo cierre se coloca, por
su hora de inicio en Madrid: el corte de D6 c) está en el cierre de esa vela); las órdenes
colocadas en la sesión, canceladas incluidas, del mismo «### Ordenes»; los días de calendario con
la ventana que propone la decisión 5 (H4 desde las 00:00 de Madrid de cuatro días antes, M15 desde
las 00:00 del día anterior, M1 desde una hora antes del inicio de la sesión; todo hasta el corte),
contados en Madrid y en UTC y ya recortados a la construcción; «ocultos», cuántos de esos días dan
`True` en `casos_ocultos`. Todos los días tocados son de construcción (regla 2).

| # | día | mes | sesión | P6 | operaciones del trader ese día (sesión, lado, hora de Madrid) | primera orden del bot: cierre de la M1 que la coloca (Madrid) | órdenes colocadas en la sesión | días de calendario del gráfico (H4 · M15 · M1) | ocultos |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 2026-01-06 | enero | 11-15 | en sesion | 07-11 compra 10:22 | 14:35 | 5 | 2026-01-02..2026-01-06 (5) · 2026-01-04..2026-01-06 (3) · 2026-01-06..2026-01-06 (1) | 0 |
| 2 | 2026-01-07 | enero | 11-15 | en sesion | 07-11 venta 07:34 | 11:02 | 16 | 2026-01-02..2026-01-07 (6) · 2026-01-05..2026-01-07 (3) · 2026-01-07..2026-01-07 (1) | 0 |
| 3 | 2026-01-09 | enero | 11-15 | en sesion | 07-11 venta 10:07 | 11:38 | 6 | 2026-01-04..2026-01-09 (6) · 2026-01-07..2026-01-09 (3) · 2026-01-09..2026-01-09 (1) | 0 |
| 4 | 2026-01-15 | enero | 11-15 | en sesion | 07-11 venta 09:42 | 11:34 | 2 | 2026-01-10..2026-01-15 (6) · 2026-01-13..2026-01-15 (3) · 2026-01-15..2026-01-15 (1) | 0 |
| 5 | 2026-01-16 | enero | 11-15 | en sesion | 07-11 venta 08:20 | 13:24 | 10 | 2026-01-11..2026-01-16 (6) · 2026-01-14..2026-01-16 (3) · 2026-01-16..2026-01-16 (1) | 0 |
| 6 | 2026-01-22 | enero | 07-11 | en sesion | 11-15 venta 12:13; 11-15 venta 12:51; 11-15 venta 13:27 | 07:31 | 5 | 2026-01-17..2026-01-22 (6) · 2026-01-20..2026-01-22 (3) · 2026-01-22..2026-01-22 (1) | 0 |
| 7 | 2026-01-27 | enero | 11-15 | en sesion | 07-11 compra 09:42; 07-11 compra 09:45 | 12:05 | 9 | 2026-01-22..2026-01-27 (6) · 2026-01-25..2026-01-27 (3) · 2026-01-27..2026-01-27 (1) | 0 |
| 8 | 2026-04-02 | abril | 11-15 | en dia | ninguna | 14:02 | 9 | 2026-04-01..2026-04-02 (2) · 2026-04-01..2026-04-02 (2) · 2026-04-02..2026-04-02 (1) | 0 |
| 9 | 2026-04-08 | abril | 07-11 | en dia | ninguna | 09:10 | 6 | 2026-04-03..2026-04-08 (6) · 2026-04-06..2026-04-08 (3) · 2026-04-08..2026-04-08 (1) | 0 |
| 10 | 2026-04-10 | abril | 11-15 | en sesion | 07-11 compra 08:33; 07-11 compra 10:05 | 11:18 | 16 | 2026-04-05..2026-04-10 (6) · 2026-04-08..2026-04-10 (3) · 2026-04-10..2026-04-10 (1) | 0 |
| 11 | 2026-04-15 | abril | 07-11 | en dia | ninguna | 07:01 | 14 | 2026-04-10..2026-04-15 (6) · 2026-04-13..2026-04-15 (3) · 2026-04-15..2026-04-15 (1) | 0 |
| 12 | 2026-04-15 | abril | 11-15 | en dia | ninguna | 11:03 | 14 | 2026-04-10..2026-04-15 (6) · 2026-04-13..2026-04-15 (3) · 2026-04-15..2026-04-15 (1) | 0 |
| 13 | 2026-04-20 | abril | 07-11 | en dia | ninguna | 07:26 | 5 | 2026-04-15..2026-04-20 (6) · 2026-04-18..2026-04-20 (3) · 2026-04-20..2026-04-20 (1) | 0 |
| 14 | 2026-04-20 | abril | 11-15 | en dia | ninguna | 11:27 | 7 | 2026-04-15..2026-04-20 (6) · 2026-04-18..2026-04-20 (3) · 2026-04-20..2026-04-20 (1) | 0 |
| 15 | 2026-04-22 | abril | 11-15 | en sesion | 07-11 venta 10:02; 07-11 venta 10:19 | 11:54 | 13 | 2026-04-17..2026-04-22 (6) · 2026-04-20..2026-04-22 (3) · 2026-04-22..2026-04-22 (1) | 0 |
| 16 | 2026-04-27 | abril | 07-11 | en sesion | 11-15 compra 13:45; 11-15 compra 14:00 | 06:59 | 14 | 2026-04-22..2026-04-27 (6) · 2026-04-25..2026-04-27 (3) · 2026-04-27..2026-04-27 (1) | 0 |
| 17 | 2026-04-28 | abril | 11-15 | en sesion | 07-11 venta 10:12 | 13:05 | 6 | 2026-04-23..2026-04-28 (6) · 2026-04-26..2026-04-28 (3) · 2026-04-28..2026-04-28 (1) | 0 |
| 18 | 2026-07-02 | julio | 07-11 | en sesion | 11-15 compra 11:34; 11-15 compra 12:25; 11-15 compra 12:45; 11-15 compra 13:59; 11-15 compra 14:10; 11-15 compra 14:23 | 07:32 | 4 | 2026-07-01..2026-07-02 (2) · 2026-07-01..2026-07-02 (2) · 2026-07-02..2026-07-02 (1) | 0 |
| 19 | 2026-08-05 | agosto | 07-11 | en dia | ninguna | 07:02 | 13 | 2026-08-01..2026-08-05 (5) · 2026-08-03..2026-08-05 (3) · 2026-08-05..2026-08-05 (1) | 0 |
| 20 | 2026-08-05 | agosto | 11-15 | en dia | ninguna | 14:43 | 4 | 2026-08-01..2026-08-05 (5) · 2026-08-03..2026-08-05 (3) · 2026-08-05..2026-08-05 (1) | 0 |
| 21 | 2026-08-06 | agosto | 11-15 | en sesion | 07-11 venta 08:07 | 12:28 | 9 | 2026-08-01..2026-08-06 (6) · 2026-08-04..2026-08-06 (3) · 2026-08-06..2026-08-06 (1) | 0 |
| 22 | 2026-08-10 | agosto | 07-11 | en sesion | 11-15 compra 13:57; 11-15 compra 14:38 | 07:06 | 12 | 2026-08-05..2026-08-10 (6) · 2026-08-08..2026-08-10 (3) · 2026-08-10..2026-08-10 (1) | 0 |
| 23 | 2026-08-11 | agosto | 11-15 | en sesion | 07-11 compra 10:08 | 13:01 | 7 | 2026-08-06..2026-08-11 (6) · 2026-08-09..2026-08-11 (3) · 2026-08-11..2026-08-11 (1) | 0 |
| 24 | 2026-08-12 | agosto | 11-15 | en sesion | 07-11 compra 07:25 | 11:12 | 7 | 2026-08-07..2026-08-12 (6) · 2026-08-10..2026-08-12 (3) · 2026-08-12..2026-08-12 (1) | 0 |
| 25 | 2026-08-17 | agosto | 11-15 | en sesion | 07-11 compra 07:17 | 12:05 | 11 | 2026-08-12..2026-08-17 (6) · 2026-08-15..2026-08-17 (3) · 2026-08-17..2026-08-17 (1) | 0 |
| 26 | 2026-08-18 | agosto | 07-11 | en dia | ninguna | 07:46 | 10 | 2026-08-13..2026-08-18 (6) · 2026-08-16..2026-08-18 (3) · 2026-08-18..2026-08-18 (1) | 0 |
| 27 | 2026-08-18 | agosto | 11-15 | en dia | ninguna | 11:30 | 8 | 2026-08-13..2026-08-18 (6) · 2026-08-16..2026-08-18 (3) · 2026-08-18..2026-08-18 (1) | 0 |
| 28 | 2026-08-24 | agosto | 07-11 | en sesion | 11-15 venta 13:29 | 07:21 | 23 | 2026-08-19..2026-08-24 (6) · 2026-08-22..2026-08-24 (3) · 2026-08-24..2026-08-24 (1) | 0 |
| 29 | 2026-08-28 | agosto | 07-11 | en sesion | 11-15 venta 12:42 | 07:57 | 6 | 2026-08-23..2026-08-28 (6) · 2026-08-26..2026-08-28 (3) · 2026-08-28..2026-08-28 (1) | 0 |
| 30 | 2026-08-31 | agosto | 11-15 | en sesion | 07-11 compra 08:30; 07-11 compra 08:58 | 14:38 | 2 | 2026-08-26..2026-08-31 (6) · 2026-08-29..2026-08-31 (3) · 2026-08-31..2026-08-31 (1) | 0 |

**Lo que la tabla enseña y cambia la elección:**
- **Julio tiene un solo candidato (fila 18), y su H4 se recorta a día y medio** (desde el 1 de julio
  a las 02:00 de Madrid): el 30 de junio no es de construcción. Lo mismo el 2 de abril (fila 8,
  desde el 1 de abril a las 02:00). Los demás tienen cinco o seis días de calendario de H4.
- **En la fila 16 la orden se coloca en el cierre de la M1 de las 06:59** (a las 07:00 en punto):
  la toma la hace una vela de antes de las 7 (A-43, `toma_antes_de_la_ventana` = `cuenta`).
  Enseñarla mete A-43 en S-14.
- **Enero no tiene ningún día «en día»**: los siete son «en sesión».

### 1.e Los gráficos de D6: visor o guion, las dos marcas y la guardia

**El visor no cumple D6, medido en el código** (`src/botsito/cli.py:2478-2596`,
`src/botsito/engine/visor.py`):
- **b) calienta con el mes anterior**: `Preparador._m1` carga «las M1 del mes y del anterior»
  (`visor.py:287-306`, el bucle `for m in (arnes._mes_anterior(mes), mes)` de :293): marzo para
  abril y junio para julio, los dos con días reservados. Technical Debt lo dice (PROJECT_STATE.md:
  108, :110); verificado.
- **c) `--hasta` no recorta todo**: el motor corre el día entero (`resultado = self.motor.correr_dia
  (mercado)`, `visor.py:325`) y la página pinta las H4 de contexto (`_h4_de_contexto(h4_todas,
  sesgos, hasta)`, :340, con el `hasta` de la VENTANA, no el de `--hasta`); Technical Debt
  (PROJECT_STATE.md:111) dice que `--hasta` no recorta las H4 de contexto, las listas ni el
  resumen del bróker: verificado en el código, sin correrlo.
- **d) fechas**: escribe HTML, no PNG; el nombre es el id del caso (`f"{c.id}.html"`, cli.py:2526,
  y `.hasta-…html`, :2528), y el título lleva `d.dia.isoformat()` (`visor.py:1010`, :1018).
- **Enseña las operaciones del trader** del día (`OperacionVisor(TRADER, …)`, `visor.py:343-346`),
  que S-14 no puede enseñar.
- **f)** la salida sí sale de `--salida` (cli.py:2501).

**Así que el guion.** Lo que mide la fase 0 para escribirlo:
- **Las dos marcas salen de los anexos sin correr el motor** (D6 e): la vertical, de `liquidez_tomada`
  del camino (`lista-s14.txt`); la horizontal, del `punto` de la primera fila de la sesión en «###
  Ordenes» (`diaria.DIAGNOSTICO.cuenta=diaria.txt`, cabecera en :2078; columna `punto`, de la forma
  `117073@29461775`: el precio en puntos y el minuto). **Dos hechos medidos que cambian lo que
  enseñan** (decisión 4):
  1. **En las 34 sesiones, el precio de la primera orden ES su punto** (`round(precio × 100000) ==
     punto`, 34 de 34): la horizontal «en el punto» es exactamente el nivel de entrada de la
     orden stop (`orden_stop_punto`, ADR-0064: la orden nace en el punto). No enseña el stop, el
     objetivo ni el resultado, pero sí el precio de la orden.
  2. **En las 34, la liquidez tomada y la primera orden caen en el mismo cierre de M1** (el camino
     da el mismo minuto, y «### Ordenes» la coloca en el cierre de esa vela; RECORRIDA-CONSTRUCCION.md
     :1337-1338 ya lo decía): **la vertical cae justo en el borde derecho del gráfico**, en el corte.
     Dice «aquí el bot vio la toma», pero no separa la toma de la orden.
- **El nivel de M15 tomado no está en ningún anexo**, medido: ni `lista-s14.txt`, ni «### Ordenes»
  (solo `punto` y `caja 1`), ni `entradas-antes-alternancia.txt` lo traen. **Sin él, la vertical
  en el borde se entiende**: el trader ve en M15 qué nivel se acaba de cruzar en la última vela.
  No pido correr nada (decisión 4).
- **b) La API del manifiesto lee el mes entero**: `cargar_ventana` (`src/botsito/data/dataset.py:
  414-467`) lee el fichero mensual completo (`leer_fichero(ruta)`, :442, con su hash, :440) y
  filtra la ventana en memoria (:453-459). «Solo se leen las velas de los días que salen en la
  imagen» no se puede cumplir al byte con la API del proyecto: se leen los ficheros de los meses
  de la ventana (enero, abril, julio y agosto; nunca marzo ni junio, porque la ventana se recorta
  antes) y se quedan solo los minutos de la ventana. En el de julio están también del 18 al 31, y
  en el de enero el 1 y el 31 (decisión 5).
- **No hay librería de gráficos** en el entorno: ni `matplotlib`, ni Pillow, ni otra
  (`pyproject.toml` y `uv.lock` sin ninguna; `.venv/Lib/site-packages` tampoco). Añadir una toca
  `pyproject.toml` y `uv.lock`, fuera del contrato (decisión 6).
- **La guardia, medida con una sonda** (la forma del guion, en la carpeta de trabajo, fuera del
  repo; sin leer velas): un guion que importa `casos_ocultos` y `dias_de_casos` y no recorre
  directorios **pasó** (el de los recuentos de §1.d). La sonda con la API del manifiesto y un
  escritor de PNG con `zlib` **la negó**: «el codigo que se ejecuta pide el corpus SIN FILTRAR»
  (`exigir_sin_crudo`), porque el escritor guardaba los bytes en una variable llamada `crudo`. Es
  el falso positivo de la deuda K (PROJECT_STATE.md:48, «una asignación a una variable llamada
  crudo»). **No la reescribí** (encargo, punto 3): decisión 7.
- **La carpeta propuesta** (D6 f): `C:\Users\USER\Desktop\sesion-06-graficos\`, fuera del repo; el
  guion se niega a escribir dentro del repo (como `transcribir_sesion.py`).

### 1.f La hoja 06 en `scripts/transcribir_sesion.py`

Lo que hay que añadir (medido en `scripts/transcribir_sesion.py`):
- `ORDEN_SESION_06` (S-1 a S-23 en el orden de la hoja, que es el numérico), con su comentario,
  junto a `ORDEN_SESION_05` (:127-131);
- `CODIGOS_DE_SESION_TEXTO["06"]` (:139-206), con el título de cada pregunta de
  `docs/sesion-6/PREGUNTAS.md`;
- `HOJAS["06"] = ORDEN_SESION_06` (:208-213) y `SESION_EN_CURSO = "06"` (:214);
- el docstring: el ejemplo de uso dice `--video v15` (:48); pasa a `v17`, el siguiente id libre
  (hoy el último es v16, `fuentes.yaml:179`).
- **`_RE_CODIGO` (:241-245)** admite una letra y una o dos cifras: S-1 a S-23 caben, sin sufijos
  (D7).

Los tests (`tests/unit/test_transcribir_sesion.py`):
- `test_la_hoja_05_tiene_los_25_codigos_con_su_texto` (:598-604) ata los títulos con
  `_RE_TITULO = r"^\*\*S-(\d+)\. (.+?)\*\*"` (:582, multilínea y con DOTALL): **los títulos de
  `docs/sesion-6/PREGUNTAS.md` irán en negrita como `**S-n. Título**`**, el formato de la 5. Uno
  nuevo, igual, para la 06 (sin el recuadro: la 6 no tiene).
- `test_la_sesion_en_curso_es_la_05` (:607-610) cambia a la 06 (a propósito, y falla con el código
  de `main`).
- uno nuevo: S-23 vale en la 06 y no en la 05 (como `test_s25_vale_en_la_05_y_no_en_la_04`,
  :613-618), y la filtrada de la 06 agrupa con su hoja (como :634-641); y que la 05 no cambia.

**Lo que la ingesta de la 6 necesitará además, y no es de esta rama:** v17 en `fuentes.yaml` y en
`SESIONES_EN_CUARENTENA` (`src/botsito/corpus/cuarentena.py:51`), como hizo `trabajo/sesion-05`
(SESION-05-EXTRACCION.md:157); la guardia no tiene ids de sesión escritos (Grep de `v15`/`v16` en
`.claude/hooks/guardia.py`: nada). `scripts/barrido_dias.py` no lleva nada de la sesión (su rango es
un argumento). La skill `ingerir-sesion` nombra `ORDEN_SESION_NN` en general (`SKILL.md:20`).
**Frases que asignan esto «a la ingesta»** (Grep de «con la ingesta» en `docs`, `knowledge`,
`scripts` y `.claude/skills`): solo las de la sesión 5 (`docs/sesion-5/PREGUNTAS.md:28`, :265,
:434, :502, ya corregidas con recuadro) y los informes de la 5; ninguna de la 6.

### 1.g El encargo frente al repo (informe del auditor, 2026-10-28)

El subagente `auditor-encargo` comprobó 68 afirmaciones: 61 correctas, 1 incorrecta y 6 con matiz,
y seis herencias que el encargo no recoge. Lo que cambia algo, con lo que hago:

| Del auditor | Qué dice | Lo medido y lo que hago |
|---|---|---|
| Fila 35, INCORRECTA | D4.2 llama «la corrida que cuenta» a la que tiene P5 y P6 grandes, y esos son de la corrida 2 | Verificado en `RECORRIDA-CONSTRUCCION.md:758-776` y :1295-1298: decisión 8 |
| Fila 62, MATIZ | D8 dice «pasa a permitir… con un recuadro» y el revisor tiene que ver que «los recuadros no tocan el cuerpo» | Decisión 7 |
| Fila 53, MATIZ | La vertical de D6 e) coincide con el corte | Lo mismo que medí en §1.e: decisión 3 |
| Fila 11, MATIZ, y herencia 1 | NA:F no está en las Refs de R4.2 (`HOJA-DE-RUTA.md:242-243`) sino en G.4 (:547) | Va a las líneas del cierre: R4.2 gana NA:F en sus Refs. No lo toco en la rama: la hoja de ruta no está en el contrato |
| Fila 61, MATIZ | En la sesión 4 «otra, ¿cuál?» solo iba donde las opciones podían sugerir | El recuadro de «Durante» (D8) dirá «desde la sesión 4, cerradas con opciones; desde la 5, con "otra, ¿cuál?" en todas» |
| Fila 39, MATIZ, y herencia 3 | §12 de SESION-05-EXTRACCION lista además los vídeos, la captura de marzo y los fotogramas; los vídeos de las sesiones están «recomendado, sin hacer» | El encabezado va con el texto de D4; el «Para Aleks» del encabezado remite a §12 entera |
| Fila 6 | `rutas_permitidas` no cubre `.claude/` ni `barrido_dias.py`, por si la ingesta pidiera algo | Medido en §1.f: la ingesta no necesita nada de esta rama en esos ficheros |
| Herencia 2 | Declarar en la fila de exposiciones lo que lee cada `make check` (el M1 de marzo de `test_visor.py` y `test_preparar_a35.py`, el calentamiento de `arnes.dias_de_mercado`) | En la fila del 2026-10-28 de esta rama |
| Herencia 4 | Lección B1 de `trabajo/cuarentena-por-condicion-2`: los datos de prueba no forman fechas posibles de meses reservados (`ERRORES-RECURRENTES.md:102`) | Se aplica a los tests del guion (fase 2): sus velas sintéticas, con fechas de construcción o de un año que no es del material |
| Herencia 5 | Para días al borde de un mes, el contexto llega a marzo, junio o diciembre de 2025 | La tabla de §1.d da los días YA recortados: ninguno es de esos meses (el recorte de D6 a) los deja fuera antes de contar); no se imprime ninguno |
| Herencia 6 | S-14 sale de la corrida 2; en la que cuenta, 29 de 34 sin orden | Decisión 8 |

El resto (fechas, ids, líneas, cifras de la sesión 5, recuento de 30, `_RE_CODIGO`, el test de los
títulos, 22.804 bytes) lo confirma con su evidencia.

### 1.h Lo que no pude medir

- **Qué dice la guardia del guion entero**: la sonda se paró en `crudo` (§1.e); lo que vendría
  después (la lectura de velas con `--leer`, la escritura fuera del repo) queda sin medir hasta la
  decisión 6.
- **Cuántas decisiones del bot toca cada pregunta del bloque 3**: hace falta correr el motor con
  cada opción (§1.c).
- **Si 3 minutos por día de S-14 bastan**: es el supuesto del encargo; la sesión 5 no enseñó ningún
  gráfico.

## Lo que necesito que decidas

0. **El orden y la duración (§1.c).** Opciones: (a) los 23 códigos de la tabla de §1.c en una sola
   sesión de unas 1:53, con corte en S-17 si a la hora y media no se ha llegado (S-17 a S-23, otro
   día, como la 5); (b) partirla de antemano en dos días: bloques 1 y 2 el primero (S-1 a S-12,
   unos 51 minutos) y 3 y 4 el segundo (unos 1:02). Recomiendo (a): la estimación cabe en 2 horas y
   la 5 ya enseñó que partir sobre la marcha funciona. Coste de (b): dos citas con el trader para
   algo que cabe en una.
1. **«El nivel se congela al tomarse» (ADR-0084:41-48, fila 23).** Opciones: (a) dentro de S-3,
   como un «Para precisar» con su dibujo (una mecha mueve el alto; después una M1 cierra con cuerpo
   por encima del alto ORIGINAL pero por debajo del movido: «¿esa vela toma tu liquidez?»); (b)
   pregunta propia, con su código; (c) fuera de la hoja, como decisión del consultor. Recomiendo
   (a): solo tiene sentido si el trader contesta (ii) en S-3, y es la misma figura. Coste de (b):
   un código más para una pregunta que depende de la anterior; de (c), una decisión con efecto
   visible sin respaldo del trader.
2. **Los días de S-14 (§1.d).** Los eliges tú; mi propuesta, con tus criterios y sin mirar ningún R:
   **julio, fila 18** (el único, entra de antemano); **enero, filas 4 (11-15) y 6 (07-11)**;
   **abril, filas 9 (07-11, en día) y 17 (11-15, en sesión)**; **agosto, fila 20 (11-15, en día)**;
   reservas, **filas 26 (agosto, 07-11, en día) y 10 (abril, 11-15, en sesión)**. Cubre los cuatro
   meses, las dos sesiones (3 y 3) y las dos clases (2 «en día» y 4 «en sesión»). He evitado la
   fila 16 (la toma antes de las 7 mete A-43) y la 8 (H4 recortado a día y medio); la 18 lo tiene
   igual y entra por tu criterio. Opciones: (a) esta; (b) la tuya.
3. **Las dos marcas, con lo medido (§1.e).** En las 34 sesiones el punto ES el precio de la orden, y
   la toma cae en el mismo cierre que la orden (la vertical, en el borde derecho, en el corte).
   Opciones: (a) las dos marcas como dice D6 e), y la guía de Aleks dice que la horizontal es el
   nivel donde el bot pondría su orden (sin stop, objetivo ni resultado) y que la vertical marca la
   vela en que el bot da la liquidez por tomada; D8 lo escribe así; (b) solo la horizontal, porque
   la vertical coincide con el corte y no añade; (c) ninguna marca, solo el gráfico limpio. Recomiendo
   (a): S-14 pregunta por qué no entró «aquí», y el «aquí» es ese nivel; la vertical le ahorra al
   trader buscar el borde. Coste de (b): ninguno grande, una línea menos. De (c): la pregunta no se
   puede contestar (el porqué de D8).
4. **Las ventanas y la lectura de las velas (§1.e, D6 a y b).** Opciones: (a) H4 desde las 00:00 de
   Madrid de cuatro días antes, M15 desde las 00:00 del día anterior y M1 desde una hora antes del
   inicio de la sesión, todo hasta el cierre de la M1 de la primera orden y recortado a la
   construcción en Madrid y en UTC (las vela que tocan un día que no lo sea, fuera enteras); por la
   API del manifiesto, que lee el fichero mensual entero de enero, abril, julio o agosto (nunca
   marzo ni junio) y se queda con la ventana; declarado por recuento; (b) un lector que lea solo
   las líneas de los días de la imagen: tocaría `src/botsito/data/` (protegido) o saltaría el hash
   del manifiesto. Recomiendo (a): es la API que pide D6 b) y lo que hace el arnés con su mes, sin
   el mes anterior. Coste de (b): código nuevo fuera del contrato, o una lectura sin comprobar.
5. **Cómo se escribe el PNG (§1.e).** Opciones: (a) un escritor propio en el guion, con `zlib` y
   `struct` de la biblioteca estándar y una fuente de mapa de bits para las horas y el marco
   («H4», «M15», «M1», «07:00»): sin dependencias nuevas, bytes deterministas y ningún trozo de
   texto en el PNG (la prueba de metadatos de D6 g es que solo haya `IHDR`, `IDAT` e `IEND`); (b)
   `matplotlib` como dependencia de desarrollo: `pyproject.toml` y `uv.lock` entran en el contrato,
   la CI instala más y el PNG lleva el trozo `Software` que hay que quitar a mano. Recomiendo (a).
   Coste de (a): unas 250 líneas más en el guion, con sus tests.
6. **La guardia y la palabra `crudo` (§1.e).** La sonda la negó por una variable llamada `crudo` (el
   falso positivo de K). Opciones: (a) que el guion no use esa palabra como nombre (es mío y no
   significa nada: el contenido del PNG), repetir la sonda una vez con otro nombre y declararlo;
   (b) que la lances tú con «!»: no mide la guardia; (c) arreglar K antes, en su rama. Recomiendo
   (a): no rodea la regla, que va contra `--crudo` y `crudo=True` sobre el corpus, y la sonda se
   repite tal cual salvo ese nombre. Coste de (c): una rama más antes de la sesión 6.
7. **D8: ¿cuerpo o recuadro? (auditor, fila 62).** D8 dice que la regla 2 «pasa a permitir» la
   segunda imagen «con un recuadro "Por qué cambió" como el del 2026-09-28», y el punto 8 manda al
   revisor comprobar «que los recuadros de D8 no tocan el cuerpo de la regla». El precedente del
   2026-09-28 cambió el CUERPO y guardó el texto viejo en el recuadro (`SESION-DE-PREGUNTAS.md:21-39`).
   Con solo un recuadro, el cuerpo seguiría diciendo «sin la operación». Opciones: (a) como el
   precedente: el cuerpo de la regla 2 gana la frase de la segunda imagen (solo días de
   construcción, las dos marcas, nunca la orden, el stop, el objetivo ni el resultado), y el recuadro
   nuevo copia el texto anterior tal cual y dice por qué cambió; el de «Durante», paso 2, es solo
   recuadro y su cuerpo no se toca; el revisor comprueba que el cuerpo cambia SOLO en esa frase y
   que el recuadro del 2026-09-28 queda intacto; (b) solo recuadros, sin tocar ningún cuerpo: el
   recuadro dice que manda sobre la frase de arriba. Recomiendo (a): una regla que se lee entera sin
   tener que cruzarla con un recuadro, y es lo que se hizo la otra vez. Coste de (b): el cuerpo queda
   diciendo lo contrario de lo que se hace.
8. **De qué corrida salen S-14 y su «por qué» (auditor, fila 35; medido en
   `RECORRIDA-CONSTRUCCION.md:758-776`).** «La corrida que cuenta, que dio "no"» es la 1 (ADR-0070
   §3, cuenta arrastrada): en ella el bot casi no opera (P4 = 124; P5 = 37 y P6 = 9), porque RN-032
   la para el 20 de enero, y 29 de las 34 sesiones de S-14 no tienen ninguna orden
   (`RECORRIDA-CONSTRUCCION.md:1295-1298`). P5 = 173 y P6 = 77 son de la corrida 2 (cuenta
   reiniciada cada día, diagnóstico), cuya clasificación «es la que cuenta» por tu decisión 4 de
   aquella rama (:762). Los 30 candidatos y las dos marcas salen de la corrida 2. No cambia tu D4
   (el bloque 2 sigue siendo lo que más separa al bot, en la clasificación que cuenta). Opciones: (a)
   la guía de Aleks y el «Para Aleks» de S-7 a S-12 dicen que los días y las marcas son del bot con
   la cuenta reiniciada cada día, y que con la cuenta arrastrada no habría operado en casi ninguno;
   el texto del trader no lo lleva; (b) no decirlo. Recomiendo (a): es la lección (5) de
   `trabajo/recorrida-construccion` («la cuenta llega» no es «pudo operar»,
   `ERRORES-RECURRENTES.md:101`).

## Respuesta del consultor a la PARADA (2026-10-28)

Copiada tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA de la fase 0 de trabajo/barrido-sesion-6 (2026-10-28). Cópiala tal cual al final del encargo y del informe, en «Respuesta del consultor a la PARADA», con su fecha, y aplícala punto por punto (skill fase-cero).
>
> 0. (a). Los 23 códigos de §1.c en una sola sesión, con corte en S-17 si a la hora y media no se ha llegado: S-17 a S-23 pasan a otro día, como en la 5. «Para cerrar» se salta si el trader ya contestó por WhatsApp (D4). Por qué: la estimación cabe en dos horas y partir sobre la marcha ya funcionó en la 5.
> 1. (a). «El nivel se congela al tomarse» (ADR-0084:41-48) va dentro de S-3 como «Para precisar», con su dibujo, y se pregunta conteste lo que conteste a (i)/(ii). Su «Para Aleks» dice que hoy es una decisión del consultor con efecto visible. Por qué: es la misma figura que S-3, y una decisión del consultor con efecto visible necesita el respaldo del trader.
> 2. (a). Los días de S-14 son las filas 18, 4, 6, 9, 17 y 20 de §1.d, y las de reserva la 26 y la 10. Por qué: cumplen los criterios de D5, fijados antes de elegir y no por el R. Los gráficos 1 a 6 siguen el orden que propongas, mezclando meses; la clave queda solo en clave.txt.
> 3. (b), con un cambio sobre tu recomendación: una sola marca, la horizontal en el punto de la primera orden. Como mediste, ese punto ES el precio de entrada de la orden stop. La vertical sale porque coincide con el corte y no añade nada. La segunda imagen es la misma que la limpia más esa línea. La guía de Aleks y el «Para Aleks» de S-7 a S-12 dicen: «la línea es el nivel donde el bot pondría su orden de entrada; el gráfico acaba en la vela en que el bot da la liquidez por tomada; no hay stop, objetivo, llenado ni resultado». Por qué: es lo único que la pregunta necesita.
> 4. (a). Ventanas de §1.d (H4 desde las 00:00 de Madrid de cuatro días antes, M15 desde las 00:00 del día anterior y M1 desde una hora antes de la sesión, todo hasta el corte y recortado a la construcción en Madrid y en UTC), leídas por la API del manifiesto. Esa API lee el fichero mensual entero de enero, abril, julio o agosto (nunca marzo ni junio) y se queda con la ventana. Es lectura de velas, que no es abrir (CLAUDE.md, «Que se puede mirar y que no», punto 2; ADR-0021 §1; ADR-0033 §4). La fila de HOLDOUT-EXPOSICIONES declara, por recuento, cuántos días reservados tienen velas en los ficheros leídos (verifica que en julio son 0, ADR-0078). Sin recorrer directorios: la guardia niega un guion nuevo que recorre carpetas y nombra data/ (SENSIBLES).
> 5. (c), en lugar de (a) o (b): SVG escrito por el propio guion, solo con la biblioteca estándar, sin dependencias nuevas, con las etiquetas como <text> («H4», «M15», «M1» y las horas). Sin <metadata>, sin <title> con fecha, sin comentarios y sin ningún atributo con fecha. Los ficheros: grafico-N-limpio.svg y grafico-N-marcado.svg, más clave.txt. Los tests de D6 g) pasan a ser sobre el SVG: ningún texto del fichero casa con una fecha (AAAA-MM-DD, DD/MM, DD-MM o el nombre de un mes), ningún elemento cae a la derecha del corte, y un día fuera de la construcción o en casos_ocultos hace salir con error sin escribir. Por qué: un PNG propio son unas 250 líneas más y una fuente de mapa de bits; un SVG es texto, se abre en el navegador a pantalla completa y se comprueba leyéndolo. El paso 6 de «Antes» de SESION-DE-PREGUNTAS.md no fija formato (verificado).
> 6. (a). En el guion, ninguna variable, parámetro ni clave se llama crudo (la guardia caza crudo = …, crudo=None y "crudo": …, guardia.py:195). La sonda se repite una sola vez con el guion casi final y se declara en el informe. Por qué: no rodea la regla, que va contra el corpus sin filtrar; el nombre no significaba nada. La deuda K sigue en K.
> 7. (a), y corrijo mi D8: se cambia el CUERPO de la regla 2, como hizo el precedente del 2026-09-28, con la frase de la segunda imagen (solo días de construcción, la marca del pun 3 y nunca la orden, el stop, el objetivo, el llenado ni el resultado). El recuadro nuevo copia el texto anterior tal cual y dice por qué cambió. El de «Durante», paso 2, es solo un recuadro, con tu texto de la fila 61. El punto 8 del encargo queda así para el revisor: el cuerpo de la regla 2 cambia SOLO en esa frase, el recuadro del 2026-09-28 queda intacto y el de «Durante» no toca su cuerpo. Error del consultor: el encargo pidió «un recuadro» contra el precedente que citaba.
> 8. (a). La guía de Aleks y el «Para Aleks» de S-7 a S-12 dicen que los días y la marca salen del bot con la cuenta reiniciada cada día (corrida 2), y que con la cuenta arrastrada (la que cuenta, corrida 1) el bot no llena ninguna orden desde la última sesión del 20 de enero, por RN-032. El texto para el trader no lo lleva. Y corrijo mi D4.2: el bloque 2 se justifica con la clasificación de patrones de la corrida 2 (P5 y P6), no con la corrida que cuenta. Error del consultor: D4.2 mezcló las dos corridas.
>
> Además, para las líneas del cierre (§7 del informe): R4.2 gana NA:F en sus Refs (fila 11 del auditor), y la fila 23 (ADR-0084) entra en su «Qué es». Y prepara la fila de ERRORES-RECURRENTES con los dos errores del consultor de los puntos 7 y 8, con esta lección: «Para el consultor: antes de mandar cómo se enmienda un documento, se lee el precedente que se cita; y una cifra o un patrón se nombra con la corrida de la que sale.»
>
> Sigue sin parar: fase 1 (PREGUNTAS.md y los dos cambios de D8), fase 2 (guion, tests, ensayo en un clon con git worktree add, y después los gráficos, una sola vez, en C:\Users\USER\Desktop\sesion-06-graficos\, con su fila de HOLDOUT-EXPOSICIONES y dos comprobados a mano contra «### Ordenes») y fase 3 (la hoja 06). make check sellado antes de cada commit, con la línea PICO DE MEMORIA en el informe. Después, push como fix/barrido-sesion-6 con la CI de Linux, el revisor (opus) con el punto 8 del encargo ya corregido, y entregar-rama. Si la guardia o el clasificador niegan algo, PARADA con el comando exacto y lo lanzo yo con «!».
>
> Rama lista para revisión, NO cerrada.

## 2. La respuesta aplicada (2026-10-28)

### 2.0 Los sellos, con su pico de memoria

| Commit | `make check` | PICO DE MEMORIA (la línea del log) |
|---|---|---|
| 543099d (apertura) | exit 0, ningún `failed`, `SELLO` sobre el árbol e0295eb9…; 1170 s | `PICO DE MEMORIA de make check: 298 MiB en `test` (suma de sus procesos, memoria comprometida, Windows; el mayor proceso, 289 MiB)` |
| 17335ad (fase 0) | exit 0, ningún `failed`, `SELLO` sobre el árbol 8820d706…; 1100 s | `PICO DE MEMORIA de make check: 299 MiB en `test` (suma de sus procesos, memoria comprometida, Windows; el mayor proceso, 288 MiB)` |
| 60ebcf2 (fase 1) | exit 0, ningún `failed`, `SELLO` sobre el árbol 8e43f9a5…; 1118 s | `PICO DE MEMORIA de make check: 299 MiB en `test` (suma de sus procesos, memoria comprometida, Windows; el mayor proceso, 289 MiB)` |
| 09afe20 (fase 2, el guion) | exit 0, ningún `failed`, `SELLO` sobre el árbol 3825290f…; 1022 s (un primer intento, en rojo por `mypy`, §2.2) | `PICO DE MEMORIA de make check: 300 MiB en `test` (suma de sus procesos, memoria comprometida, Windows; el mayor proceso, 290 MiB)` |

### 2.1 Fase 1: `docs/sesion-6/PREGUNTAS.md` y los dos cambios de D8

**La hoja**, con los 23 códigos en el orden de §1.c (decisión 0) y las partes de D3. Punto por
punto de la respuesta:

| Punto | Hecho | Dónde |
|---|---|---|
| 0 | Los 23 códigos en una sesión, con el corte en S-17 escrito en la cabecera de la lista; «Para cerrar» con «si ya lo contestó por WhatsApp, se salta» | `PREGUNTAS.md`, §1 y «Para cerrar» |
| 1 | «El nivel se congela al tomarse», dentro de S-3 como primer «Para precisar», con su esquema y sus opciones, «se pregunta conteste lo que conteste arriba»; su «Para Aleks» dice que hoy es DECISIÓN DEL CONSULTOR con efecto visible y qué pasa si contesta (a) | S-3 |
| 2 | Los días de las filas 18, 4, 6, 9, 17 y 20, y las reservas 26 y 10: en la hoja solo «Gráfico 1» a «Gráfico 6» (S-7 a S-12); el orden, mezclando meses, lo fija la fase 2 en `clave.txt`, fuera del repo | S-7 a S-12; §2.2 |
| 3 | Una sola marca; el «Para Aleks» de S-7 (y por remisión S-8 a S-12) lleva la frase literal del punto 3 | S-7 |
| 7 | El cuerpo de la regla 2 gana una sola frase (la segunda imagen, solo con días de construcción, una sola marca, nunca la orden, el stop, el objetivo, el llenado ni el resultado); el recuadro nuevo copia el texto anterior tal cual y dice por qué cambió; el recuadro del 2026-09-28 queda intacto; «Durante», paso 2, gana solo un recuadro, con el matiz de la fila 61 del auditor, y su cuerpo no cambia | `docs/runbooks/SESION-DE-PREGUNTAS.md` |
| 8 | El «Para Aleks» de S-7 dice que los días y la marca son de la corrida 2 (cuenta reiniciada cada día) y que con la cuenta arrastrada el bot no llena ninguna orden desde la última sesión del 20 de enero, por RN-032; el texto del trader no lo lleva; la cabecera del bloque 2 nombra la clasificación de la corrida diaria (P5 y P6), no la corrida que cuenta | S-7; cabecera del bloque 2 |

**Las citas.** Todas de ítems de evidencia y de registros de feedback, por la vía que la guardia
permite (Read de los YAML; un guion de la carpeta de trabajo que lee ficheros nombrados y se niega a
leer los de `.claude/hooks/ficheros_con_ocultos.txt`), con su vídeo y su minuto. Ninguna de
transcripción, ninguna de `kb`. El de v6 (0:57:01) cae fuera de los tramos no citables de v6.
Declarado en la fila de exposiciones de la fase 1.

**La caja y el lado, comprobados antes de escribir** contra `orden_stop_punto`
(`parametros.yaml:671-688`: el último pivote de M1 contrario a la entrada, un BAJO en una venta),
`caja_bloque` (`:693-709`: el 1 es el extremo opuesto, la máxima en una venta), RN-005 y
`caja_lado_de_ruido` (`engine/zonas.py:541-558`: en una compra la caja va por debajo del bajo
tomado y el ruido es lo de encima). Los esquemas con caja: S-6 (compra, el 0 arriba), S-16 (venta,
el 0 abajo y el 1 arriba), S-17 (compra: A con el 0 por encima de la línea y el 1 por debajo; B
entera por encima; (a) → `solo_el_0`, (b) → `caja_entera`, comprobado con las dos funciones de
`zonas.py:553-558`), S-18 (venta, el punto un bajo) y S-19 (compra, el 0 arriba).

**Ninguna pregunta repite lo ya contestado** (D3), cruzada con las RESUELTAS, ADR-0084 a ADR-0086 y
lo dicho en las «en parte». Tres desviaciones de las listas fuente, declaradas:
1. **S-14 (A-53) va sin las dos subpreguntas de `ACTIVAR-SESION-05.md` §3.4**: «si el 1 de la caja
   baja mucho, ¿la sigues moviendo?» ya está contestada en la sesión 4 (S-4, «si el máximo nuevo
   queda muy lejos…», `ev-v10-005056-1a55d5b4`, y «en una compra es lo mismo»,
   `ev-v10-005116-2a9ff066`), y «si la orden se llena antes de que aparezca el punto nuevo, ¿esa
   operación vale?» también («¿La operación vale? Sí, vale», `ev-v10-020114-55bdf502`). Van a «Lo
   que nos has dicho» y a la confirmación; la pregunta se queda en la letra, que en la sesión 4 se
   contradijo («La A es verdadera») y en la 5 no se oyó bien.
2. **S-20 lleva la segunda pregunta de §3.10 (la vela sin cuerpo con mechas largas) en «Para
   precisar»**, con sus opciones, porque D3 pide una sola pregunta.
3. **S-16 (A-48 y A-49) pregunta solo de qué velas sale el 1**: que traza al cierre y que el 1 se
   va actualizando ya lo dijo (`ev-v15-003244-dcd8a834`, `ev-v15-003619-9fbc7f08`, y la sesión 4,
   S-4); van a «Para precisar» (el cierre) y a la confirmación. Las opciones de §3.6 («solo la vela
   contraria / todo el tramo») se parten en las tres de `caja_bloque` (`r1`, `r4`, `r6`), porque «todo
   el tramo» casaba con dos.

**Una negativa de la guardia en esta fase, sin rodearla:** `grep -rn "HUSO_CORTE =" src/botsito/engine/perfil_cuenta.py; grep -rln "huso_corte" knowledge/cuentas | head -3`
→ «bloquea: leer el contenido de .» (la regla de las capturas de Analytics). Era para saber qué huso
usa el perfil; lo medí con preguntas distintas a ficheros concretos (Grep sobre
`src/botsito/engine/perfil_cuenta.py`, Glob de `knowledge/cuentas/*.yaml` y Read del perfil), no con
el mismo comando. Parece un falso positivo de la guardia con `grep -rln` sobre una carpeta; queda
para el carril de guardias.

### 2.2 Fase 2: el guion de los gráficos y los gráficos

**El guion**, `scripts/graficos_sesion.py`, y sus tests, `tests/unit/test_graficos_sesion.py`, en
09afe20 (sellado: árbol 3825290f…, 1022 s, `PICO DE MEMORIA de make check: 300 MiB en `test` (suma de
sus procesos, memoria comprometida, Windows; el mayor proceso, 290 MiB)`; el primer intento de ese
`make check` salió en rojo por `mypy` sobre los tests, arreglado antes de sellar). Lo que fija cada
condición de D6 y de la respuesta:

| Condición | En el guion | El test que la fija |
|---|---|---|
| a) negar por defecto: día fuera de la construcción o en `casos_ocultos` | `CONSTRUCCION` (la regla 2, cruzada con `cargar_criterio(...).construccion`: si difieren, error); `preparar` niega el día pedido; `recorte` recorta cada marco al primer minuto permitido en Madrid y en UTC; `comprobar`, la última puerta | `test_un_dia_fuera_de_la_construccion_sale_con_error`, `test_un_dia_en_casos_ocultos_sale_con_error`, `test_el_recorte_empieza_en_el_primer_minuto_permitido_en_los_dos_relojes`, `test_la_ventana_se_recorta_antes_de_un_dia_no_permitido`, `test_un_dia_oculto_dentro_de_la_ventana_la_recorta` |
| b) solo la ventana, por la API del manifiesto, sin calentamiento, sin recorrer carpetas | `cargar` lee el mes del día con `buscar_manifiesto`/`cargar_manifiesto`/`cargar_ventana`; ninguna ventana cruza de mes (si cruzara, error); ni `glob`, ni `iterdir`, ni `listdir`, ni `scandir`, ni `walk`; ninguna variable llamada como la palabra vetada | `test_el_guion_no_recorre_carpetas_ni_usa_la_palabra_vetada` (por `ast`) |
| c) el corte | la última M1 es la que coloca la primera orden; un lector que devuelve velas fuera de la ventana hace salir con error | `test_ninguna_vela_pasa_del_corte`, `test_un_lector_que_devuelve_velas_tras_el_corte_hace_salir_con_error`, `test_ningun_elemento_del_svg_cae_a_la_derecha_del_corte` |
| d) sin fecha | `lleva_fecha` (AAAA-MM-DD, DD/MM, DD-MM o un mes) sobre cada SVG y cada nombre; sin `<title>`, `<metadata>` ni comentarios; horas de Madrid; el marco en cada panel | `test_la_comprobacion_de_fechas_caza_cada_forma`, `test_las_horas_y_los_precios_no_son_fechas`, `test_los_svg_y_sus_nombres_no_llevan_fecha_ni_metadatos`, `test_un_svg_con_fecha_no_se_escribe` |
| e) una sola marca (decisión 3) | la línea `class="punto"` en el panel de M1 del marcado; la escala de ese panel incluye el punto en las dos imágenes | `test_los_svg_y_sus_nombres_no_llevan_fecha_ni_metadatos` (el marcado es el limpio más UNA línea) |
| f) la raíz, fuera del repo; nada se escribe si algo falla | `escribir` niega una raíz dentro del repo, no pisa nada y genera todo en memoria antes del primer fichero | `test_la_raiz_no_puede_estar_dentro_del_repo`, `test_no_pisa_una_salida_que_ya_existe`, `test_un_svg_con_fecha_no_se_escribe` |
| g) datos sintéticos | velas de 2030 en enero y agosto, meses libres (lección B1 de `trabajo/cuarentena-por-condicion-2`) | todos |

**Los tests rompen de verdad** (lección b3 de `trabajo/hoja-sesion-05`): siete mutantes del guion,
aplicados uno a uno en el clon (`mutantes.py`, carpeta de trabajo de la sesión), y el test de cada
condición falla con ellos: el día fuera de la construcción («DID NOT RAISE»), `casos_ocultos`
ignorado (el `pytest.raises` no casa: salta otra puerta), la ventana sin recorte (la paraba la
última puerta, `comprobar`, antes de la aserción del test de `preparar`: por eso entra
`test_el_recorte_empieza_en_el_primer_minuto_permitido_en_los_dos_relojes`, y ese mutante, cargado
en memoria con el test nuevo, falla en su `assert`), las velas tras el corte (otra puerta), una
fecha en el SVG («DID NOT RAISE»), la raíz dentro del repo (escribió en el clon, que es lo que el
clon protege) y un guion que recorre una carpeta (`iterdir`). El guion queda restaurado y el clon,
quitado.

**La guardia** (decisión 6): la segunda y única sonda repetida, con el guion casi final y un
`--dias` vacío (`uv run python scripts/graficos_sesion.py --dias <vacio.txt> --salida <carpeta de
trabajo>`), pasó: el guion salió con «ERROR: --dias no trae ningun dia. No se ha escrito nada.»
antes de leer ninguna vela. Las dos ejecuciones con velas, desde el clon, también pasaron.

**El ensayo en un clon y la generación, una sola vez** (D6 f y regla 1 de «Ensayos aislados»):
`git worktree add --detach C:/cm/graficos 09afe20`, con su `config/settings.local.toml` apuntando al
`data/` real (sin copiar velas; el guion solo escribe en `--salida`, `escribir`). Primero, la raíz
dentro del clon: «ERROR: la raiz de salida esta dentro del repositorio. No se ha escrito nada.», y
`git status --short --ignored` del clon sin nada nuevo salvo `.venv`, la configuración y
`__pycache__`. Después, la generación, con los 8 días en el orden que propuse (la lista, en un
fichero de la carpeta de trabajo; el orden, solo en `clave.txt`):
`uv run python scripts/graficos_sesion.py --dias <dias-s14.txt> --salida "C:/Users/USER/Desktop/sesion-06-graficos"`
→ «OK: 17 ficheros (8 graficos y clave.txt) en la salida», con cuatro líneas `LECTURA:` (los cuatro
ficheros mensuales: 26, 26, 27 y 26 días con velas; 0 en `casos_ocultos` en cada uno, julio
incluido; 1 y 12 días fuera de la construcción, de enero y de julio). Los gráficos 7 y 8 son las
reservas. `git worktree remove --force C:/cm/graficos` (por `.venv`, la configuración y la carpeta
que dejó el mutante de la raíz) y `git worktree prune`.

**Dos comprobados a mano contra «### Ordenes»** (sin decir aquí cuáles: la clave está solo en
`clave.txt`): en los dos, el corte de `clave.txt` es la M1 de la primera fila de su sesión en «###
Ordenes» de `diaria.DIAGNOSTICO.cuenta=diaria.txt` (una cancelada, colocada en el cierre de esa M1),
pasada a la hora de Madrid de ese día; el punto de `clave.txt` es la columna `punto` de esa fila, que
es también su precio; y el panel de M1 del SVG tiene exactamente las velas de la ventana (una hora
antes de la sesión hasta la M1 del corte, sin huecos en esos dos días), con la última hora rotulada
en esa misma M1 o en la del mismo rótulo. En los 8: cada marcado es su limpio más una sola línea, la
`class="punto"`, y ningún SVG lleva una fecha, un comentario ni metadatos (`comprobar_svg.py`,
carpeta de trabajo).

**Lo que queda para la guía de Aleks** (decisiones 3 y 8; está en el «Para Aleks» de S-7): la línea
es el nivel donde el bot pondría su orden de entrada; el gráfico acaba en la vela en que el bot da
la liquidez por tomada; sin stop, objetivo, llenado ni resultado; corrida 2; velas de Dukascopy. El
gráfico 3 (el único de julio) tiene la H4 recortada a día y medio, como dijo §1.d.

**Una negativa de la guardia en esta fase, sin rodearla:** `grep -rn "^Puntos\|Puntos = " src/botsito/domain/*.py | head -3`
→ «bloquea: leer el contenido de  .» (la regla de las capturas de Analytics), la misma forma que la
de la fase 1 (§2.1): un patrón entre comillas que acaba en espacio. Era para el tipo `Puntos` de los
tests; lo encontré con la herramienta Grep sobre `src/botsito/domain`, otra petición. Para el carril
de guardias, con la de §2.1.

### 2.3 Fase 3: la hoja 06 en `scripts/transcribir_sesion.py`

Los gráficos quedaron en 6c114cb (sellado: árbol 5c28fcdd…, 1118 s, `PICO DE MEMORIA de make check:
299 MiB en `test` (suma de sus procesos, memoria comprometida, Windows; el mayor proceso, 289 MiB)`).

En `scripts/transcribir_sesion.py`, lo que midió §1.f, con los códigos finales de
`docs/sesion-6/PREGUNTAS.md`:
- `ORDEN_SESION_06` = S-1 a S-23, en el orden de la hoja (el numérico), con su comentario;
- `CODIGOS_DE_SESION_TEXTO["06"]`: el título de cada pregunta, con la primera letra en minúscula
  (S-7 a S-12, «gráfico 1» a «gráfico 6»), y el comentario de encima lo dice;
- `HOJAS["06"] = ORDEN_SESION_06` y `SESION_EN_CURSO = "06"`;
- el docstring: el ejemplo de uso pasa a `--video v17`, el siguiente id libre.
`_RE_CODIGO` no cambia: S-1 a S-23 caben en una letra y una o dos cifras (D7).

En `tests/unit/test_transcribir_sesion.py`:
- `test_la_hoja_06_tiene_los_23_codigos_con_su_texto`: los títulos, leídos de
  `docs/sesion-6/PREGUNTAS.md` con la misma `_RE_TITULO` que la 05 (`^\*\*S-(\d+)\. (.+?)\*\*`), son
  exactamente los del guion;
- `test_la_sesion_en_curso_es_la_06` (falla con el guion de `main`, que dice «05»);
- `test_s24_y_s25_valen_en_la_05_y_no_en_la_06` y `test_la_filtrada_de_la_06_agrupa_con_su_hoja`;
- `test_la_sesion_en_curso_es_la_05` pasa a `test_la_hoja_05_sigue_en_su_sitio`: la 05 ya no es la
  sesión en curso y su hoja no cambia (comprueba el texto de su S-14).

`PREGUNTAS.md` ya decía (fase 1) que los textos están en el guion antes de grabar, sin «con la
ingesta». Lo que la ingesta de la 6 hará y no es de esta rama (§1.f): v17 en `fuentes.yaml` y en
`SESIONES_EN_CUARENTENA`.

## Estado

EN CURSO: fases 1, 2 y 3 hechas; siguen la CI de Linux por fix/barrido-sesion-6, el revisor y la entrega.
