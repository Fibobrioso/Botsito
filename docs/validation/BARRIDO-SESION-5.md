# BARRIDO-SESION-5 · Las preguntas de la sesión 5 con el trader (R4.1)

Rama `trabajo/barrido-sesion-5`, abierta el 2026-10-19 desde `main` en e518707 (commit de estado
sobre el merge a1bb8a5, tag `stable/F37v-punto-usado`). Encargo:
`docs/encargos/trabajo-barrido-sesion-5.md`. Tramo: R4 (R4.1 de `docs/plan/HOJA-DE-RUTA.md`; V de la
Next Action). Modelo de la sesión: `claude-opus-5-5` según el entorno de la sesión (el encargo pide
Opus en esfuerzo alto; `/model` lo revisa Aleks en su terminal).

## 0 · La base, comprobada al abrir

Las cuatro comprobaciones de la skill `abrir-rama`, con su salida:

| Comprobación | Comando | Salida |
|---|---|---|
| `main` es el sha del encargo y es `origin/main` | `git rev-parse --short main`; `git rev-parse main origin/main` | `e518707`; dos veces `e51870796cb9078c7a793c04378932b4489d2fd8` |
| El último tag de HISTORIA apunta al merge bajo `main` | `git rev-parse "stable/F37v-punto-usado^{commit}"`; `git rev-parse main^1` | dos veces `a1bb8a5a48637995f297c1c4cd77082d79f33fcf`; `git ls-remote --tags origin stable/F37v-punto-usado` → `25171cf… refs/tags/stable/F37v-punto-usado` |
| La CI de `main` sobre su HEAD | `gh run view 39275923817 --json status,conclusion,headSha,headBranch,workflowName` (con `gh`, como pide el encargo; ni curl ni guion) | `{"conclusion":"success","headBranch":"main","headSha":"e51870796cb9078c7a793c04378932b4489d2fd8","status":"completed","workflowName":"ci"}` |
| Ninguna otra rama | `git branch --list`; `git ls-remote --heads origin "fix/*"` | `* main`; vacío |

`PROJECT_STATE.md` en `main`: 22.580 bytes (`wc -c`), como dice el encargo. `git status --short`
vacío antes de abrir.

## 1 · Fase 0 · Inventario sin tocar nada (2026-10-19)

Medido en el repo de la rama (base `main` e518707). Nada escrito fuera del informe, el encargo, el
contrato, `PROJECT_STATE.md` y HISTORIA (los del primer commit). Lo leído: los informes y ADR que
D1 nombra, `knowledge/spec/ambiguedades.yaml`, los ítems de evidencia de `knowledge/evidence/v10/`
por su campo `notas` (Grep) y los registros de feedback que se citan abajo (Read). Ninguna
transcripción, ninguna filtrada, ningún fotograma, ningún libro, ningún caso.

### 1.a La lista completa de D1, una fila por cosa

Estado: el de `knowledge/spec/ambiguedades.yaml` hoy. «Ya registrado»: lo que el trader ya dijo
sobre eso y está en el repo, con su id; «nada» si no hay ni ítem ni registro.

**Las de V (PROJECT_STATE, Next Action V, línea 54):**

| # | Cosa | De dónde sale | Nombra | Estado | Ya registrado |
|---|---|---|---|---|---|
| 1 | La ruptura simple sin cuerpo (una H4 rompe un extremo con la mecha y cierra donde abrió) | SESGO-H4-COLOR.md:936-939 (§4.4.1); sustituye a CORRIDA-CONSTRUCCION.md:1232 (pregunta 1) | RN-003, ADR-0080 §4 (D3, decisión del consultor) | regla ACTIVA con la decisión provisional (no decide, sigue el sesgo de antes) | en parte: la regla general por WhatsApp (`fb-2026-10-04-sesion-04-6e7da456`, trader_escrito, 14:55 del 2026-10-14) y la neutra de doble ruptura (`fb-2026-10-04-sesion-04-ca0afae6`, v10 1:40:05; `ev-v10-014005-7e2228f4`); la ruptura SIMPLE sin cuerpo no la describió (notas de 6e7da456) |
| 2 | La contradicción con la sesión 1 (con sesgo bajista, una H4 rompe por encima con la mecha y cierra roja) | SESGO-H4-COLOR.md:940-944 (§4.4.2) | RN-003, ADR-0080 §9 | ACTIVA la regla del WhatsApp (caso 3: sigue bajista) | sí, dos veces y en sentidos contrarios: el caso 3 del esquema de cuatro confirmado «Si, esta bien bro» (15:18 del 2026-10-14, en las notas de 6e7da456) y la sesión 1 (que por D2 no se cita ni se nombra) |
| 3 | A-35: cuándo está formado un alto o bajo de M15, y qué alto usa tras una superación con mecha | ACTIVAR-SESION-04.md:315-319 (§0.e.4) | A-35, RN-004 | ABIERTA, bloqueante | en parte: con mecha no cuenta, con cuerpo se actualiza (`ev-v10-012358-df6b36d2`, `ev-v10-012456-9dc1d221`, `ev-v10-012526-15de61b8`); «cuándo está formado», sin respuesta literal |
| 4 | A-44: el tope de la semana, y sobre qué se mide el 4,5 % | ACTIVAR-SESION-04.md:310-314 (§0.e.3) | A-44, RN-020 | ABIERTA, bloqueante | en parte: 4,5 % del día y las 9 seguidas se complementan, el 9 % semanal «es un error» y luego «no recuerdo» (`ev-v10-010913-c4949417`, `ev-v10-010950-7e5543df`, `ev-v10-011021-02f5dcf3`). **La segunda subpregunta ya está respondida**: «De la cuenta basado en el saldo, y que sea en el saldo inicial del día» (`fb-2026-09-09-sesion-01-bff260ea`, CORRECT de `perdida_maxima_diaria`, sesión 1). Ver 1.b |
| 5 | A-49: la caja con la vela cerrada o a veces en formación | ACTIVAR-SESION-04.md:299-303 (§0.e.1) | A-49, `caja_se_fija` | ABIERTA | en parte: la orden va en cuanto una M1 cierra más allá del extremo; la caja con la vela cerrada «o, si quieres, la vas actualizando» (ocho ítems `ev-v10-0002…-0019…` con nota S-1, tres con S-2) |
| 6 | A-13: el disparador del break even y si lo vuelve a mover | ACTIVAR-SESION-04.md:304-309 (§0.e.2) | A-13, RN-014, ADR-0065 | ABIERTA | en parte: «apenas toca» (`fb-2026-09-29-sesion-03-9f506366`, `ev-v6-005701-7ae2b8d3`) y «cuando la vela cierra, mejor con cuerpo» (`ev-v10-020410-e06f9581`, `ev-v10-020453-2d41dd25`, `ev-v10-020520-7bdf02b3`). **«¿Lo vuelves a mover?» ya está respondida**: «después el stop no se mueve» es parte de lo FIRME de A-13 (`ambiguedades.yaml:206-209`, `fb-2026-09-29-sesion-03-9f506366`). Ver 1.b |
| 7 | A-43, segunda parte: tomada a las 6:45 y otra vez a las 7:20 | ACTIVAR-SESION-04.md:320-323 (§0.e.5); §5 :837 («solo con su segunda parte») | A-43, `toma_antes_de_la_ventana` | ABIERTA | la primera parte, sí (`fb-2026-10-04-sesion-04-c3d0c855`, `ev-v10-014613-6cf002b2`); la segunda, «la más reciente» sin elegir (`ev-v10-014637-70d27645`, `ev-v10-014705-718c5f4e`) |
| 8 | A-50: la caja entera al otro lado del nivel o solo el 0 | ACTIVAR-SESION-04.md:324-327 (§0.e.6) | A-50, RN-005 | ABIERTA | en parte, con «creo» (`ev-v10-015003-dd8ab1bf`, confianza baja); lectura candidata de v9 0:51:23 en la propia pregunta |
| 9 | A-53: la orden sin llenar cuando el precio toma otra liquidez | ACTIVAR-SESION-04.md:328-331 (§0.e.7) | A-53, `orden_pendiente_al_abrir_escenario` | ABIERTA | en parte, con contradicción interna (`ev-v10-015716-5ea2575f`, `ev-v10-015831-fb95edf0`, `ev-v10-020114-55bdf502`) |
| 10 | A-32: qué era la línea que, rota con mecha, le hizo descartar la entrada | ACTIVAR-SESION-04.md:332-335 (§0.e.8); §5 :836-837 (el fotograma no se abre sin decisión) | A-32, `breaker_m1_criterio_ruptura` | ABIERTA | en parte: en M15 una toma con mecha invalida, en M1 la mecha cuenta (`ev-v10-020142-30fd2569`, `ev-v10-020308-75b88d40`); la línea concreta, no |
| 11 | S-14 de la sesión 4: el umbral de la vela casi plana | ACTIVAR-SESION-04.md:336-339 (§0.e.9); NA:H | RN-007 | regla DESALINEADA, sin umbral | en parte: sin cuerpo no cuenta (`fb-2026-09-29-sesion-03-ffab23dc`); el umbral, con dos lecturas del mismo minuto (`ev-v10-014310-2296423b`, `ev-v10-014438-95464201`, confianza baja); D7 |
| 12 | Confirmar el caso bajista de S-13 de la sesión 4 | ACTIVAR-SESION-04.md:834-835 (§5); MOTOR.md:934-935 | RN-003, ADR-0075 | ACTIVA (dicho solo con sesgo previo alcista) | en parte: `fb-2026-10-04-sesion-04-ca0afae6` (sus notas: «la confirmacion del caso bajista va a la sesion 5») |
| 13 | ADR-0076 §4.1: la vela sin cuerpo en medio del retroceso, ¿es alternancia? | MOTOR.md:923-928; ADR-0076:87-90 | RN-009, `zona_control_limpia` (A-21 RESUELTA) | pregunta sin ambigüedad abierta | nada sobre la vela sin cuerpo en el retroceso (A-21 la resolvió `fb-2026-10-04-sesion-04-22d08cbf`) |
| 14 | ADR-0076 §4.2: el breaker contrario que rompe con mecha tras una alternancia | MOTOR.md:928-930; ADR-0076:91-93 | RN-009 | ídem | nada |
| 15 | ADR-0077 §5: la racha tras la novena, ¿de cero o sigue en 9? | MOTOR.md:931-933; ADR-0077:78-98 | RN-036, `racha_perdidas_reinicio` | lectura PROVISIONAL de la sesión | en parte: tras la novena vuelve al día siguiente, la racha sigue de un día a otro (`fb-2026-10-04-sesion-04-8e2d728a`, `-d1792021`, `-fa5ef0f6`) |
| 16 | El último minuto: a qué hora exacta quita la orden pendiente al cerrar | MOTOR.md:936-939 (§1.4) | RN-035 `ventana_fin`, A-30 (RESUELTA) | pregunta sin ambigüedad abierta | en parte: se quita a las 11 y a las 3 (`fb-2026-10-04-sesion-04-766c8d2e`, `ev-v10-005427-1a0867af`); «un minuto antes» es frase del consultor (ACTIVAR-SESION-04.md, tabla 0.a, S-5) |
| 17 | Si el xlsx de julio es la exportación de v11 a v13 | ENTRADA-JULIO.md:703 (§8) | ADR-0078, NA:T | sin ambigüedad | de palabra a Aleks, el 2026-10-13, sin grabar: «el xlsx es la exportación de los 3 primeros vídeos» (ENTRADA-JULIO.md:336, punto 4); no es registro (regla 1 de SESION-DE-PREGUNTAS.md) |
| 18 | CORRIDA 2: el lote que no cabe | CORRIDA-CONSTRUCCION.md:1237-1238; sustituida y ampliada por MARGEN-LOTE.md:884-899 (§5) | A-57, `lote_si_no_cabe`, ADR-0081 | ABIERTA (pregunta) | nada (MARGEN-LOTE.md §5: ninguna frase del trader; dos citas de respaldo débil, `ev-v4-002457-5a2e88c6`, `ev-v4-012900-8ef676ed`) |
| 19 | CORRIDA 3: las reentradas tras un stop | CORRIDA-CONSTRUCCION.md:1239-1240; PUNTO-USADO.md:616-641 (§5, con el texto de la pregunta en :637-641) | RN-016, RN-019, ADR-0083 (PROVISIONAL) | sin ambigüedad abierta | en parte: el 29 de abril, «sería cuestión de poner otra reentrada aquí» (LA-CAJA-DEL-29-DE-ABRIL.md:236-243; sin ítem de evidencia: `kb find "otra reentrada"` lo localiza en el segmento 48 de la cruda de v5, 0:03:35-0:04:15, que no está en cuarentena); tres intentos por liquidez (`fb-2026-09-29-sesion-03-68a21dc0`) |
| 20 | CORRIDA 4: qué velas forman la caja, con la Δ | CORRIDA-CONSTRUCCION.md:1241 | A-48, A-49 | ABIERTA las dos | en parte: «desde el posible punto de breaker … hasta el punto más alto» (`ev-v9-004721-2e023ac6`, sesión 3) y «pueden ser velas consecutivas del mismo color» (`ev-v7-002403-8344331d`); `caja_bloque` sigue DEFAULT_AMBIGUOUS |
| 21 | VISOR A: la vela sin cuerpo dentro del tramo que marca el punto de breaker | VISOR-CONSTRUCCION.md:976-984 | `orden_stop_punto` (A-48), estructura M1 | sin ambigüedad propia | nada |
| 22 | CORRIDA 5: qué liquidez y qué zona elige, y el bajo de M15 de 2026-08-14 | CORRIDA-CONSTRUCCION.md:1242; VISOR-CONSTRUCCION.md:960-963 | A-43, A-50, A-53 (juntas en la pregunta), A-35 | ABIERTAS | lo de las filas 3, 7, 8 y 9 |
| 23 | VISOR B: una toma de la sesión anterior con el sesgo contrario | VISOR-CONSTRUCCION.md:985-995 | A-46 (RESUELTA; si contesta (a), se REABRE con `REOPEN`) | RESUELTA | A-46: «un mundo diferente» (`fb-2026-09-29-sesion-03-5021677e`), respondida sin distinguir el sesgo |
| 24 | CORRIDA 6: hasta cuándo mueve la orden con la caja, y cuándo la deja quieta o la quita | CORRIDA-CONSTRUCCION.md:1243 | ADR-0074, S-4 de la sesión 4 | sin ambigüedad abierta | en parte: el 1 se expande «mientras no se desarrolle otro punto breaker» (`ev-v10-004945-59ebac47` y su CONFIRM `fb-2026-10-04-sesion-04-35a080e2`); «sigue vivo hasta … otro posible punto de breaker» (`ev-v9-013205-85840dcc`) |
| 25 | CORRIDA 7: qué le hace no operar un día o una sesión | CORRIDA-CONSTRUCCION.md:1244 | P6; deuda «el no_trade por ausencia no está decidido» | sin ambigüedad | nada |
| 26 | CORRIDA 8: lado de ruido o más zonas de control de las admitidas | CORRIDA-CONSTRUCCION.md:1245-1246; VISOR-CONSTRUCCION.md:949-954 | RN-005, RN-009 | sin ambigüedad abierta | en parte: RN-005 y RN-009 citan lo que dijo (lado de ruido; una sola zona de control, `fb-2026-10-04-sesion-04-48fb5817`) |
| 27 | CORRIDA 9: el precio ya pasó el 0 cuando se forma la caja | CORRIDA-CONSTRUCCION.md:1247-1248; VISOR-CONSTRUCCION.md:955-959 | ADR-0057 | sin ambigüedad | nada |
| 28 | PUNTO-USADO: la caja de la reentrada, ¿la del primer intento o una nueva? | PUNTO-USADO.md:619-621 | ADR-0083 D5 | PROVISIONAL | nada |

**Las que R4.1 nombra y V no:** ADR-0076 §4 (filas 13 y 14), ADR-0077 §5 (fila 15) y la
confirmación bajista de S-13 (fila 12). Medido: **V ya las tiene todas** por remisión («las
preguntas de esos §5», que son ACTIVAR-SESION-04.md §5 y MOTOR §5); lo que V no nombra por su
número es ADR-0076 y ADR-0077. Al revés, R4.1 no tiene §0.e, MOTOR §6, ENTRADA-JULIO §8 ni la
pregunta 3 (PUNTO-USADO): es la línea del punto 6 del encargo. Las dos de R4.1 que no son preguntas:

| # | Cosa | De dónde sale | Destino |
|---|---|---|---|
| 29 | RN-004 tras A-35 | HOJA-DE-RUTA.md:201; ACTIVAR-A35-A44.md:197-227 (§5.1) | fuera de la hoja: es la medida con el arnés después de activar A-35 |
| 30 | RN-020 tras A-44 | ídem | fuera de la hoja: ídem, tras A-44 |

**Las ambigüedades ABIERTAS que no están ya** (las 15 de Known Ambiguities): A-13, A-32, A-35,
A-43, A-44, A-48, A-49, A-50, A-53 y A-57 ya están arriba. Las cinco de clase `medicion`:

| # | Cosa | Destino |
|---|---|---|
| 31-35 | A-16, A-28, A-54, A-55, A-56 | fuera de la hoja: se miden (demo de FTMO, NA:A; la respuesta de FTMO; F26), no se preguntan |

**Las candidatas de Known Ambiguities** (DISENO-ENTRADA-RUPTURA.md §2.8, PROJECT_STATE.md:96):

| # | Candidata | Destino |
|---|---|---|
| 36 | C1, la orden pendiente cuando aparece una caja nueva | se junta con la fila 24 (hasta cuándo mueve la orden): ADR-0074 ya dice que la orden sigue al 1 nuevo |
| 37 | C2 y C3 | son A-48 y A-49 (filas 20 y 5) |
| 38 | C4, el stop en dos tiempos y la orden sin stop de v8 n.º 1 | fuera: A-18 RESUELTA (el stop ya en el 0,8 al poner la orden, `fb-2026-10-04-sesion-04-87ccb0ee`); el consultor la sacó de la lista (ACTIVAR-SESION-04.md:833, sale el punto 12) |
| 39 | C5, la caja frente a la toma de M15 | fuera: A-29 RESUELTA (la orden nace tras la toma, `fb-2026-09-29-sesion-03-d3063920`) |
| 40 | C6, la orden 2 puntos más allá del 0 | fuera: A-36 RESUELTA (exactamente en el 0, `fb-2026-10-04-sesion-04-bbfb5c98`); sacada por el consultor con el punto 12 |
| 41 | C7, cuánto vive una orden stop sin llenar | se junta con las filas 24 y 16 (A-30 y A-39 RESUELTAS para el fin de sesión) |

**El feedback pendiente** (`uv run botsito feedback pending`, hoy: «2 pendientes de 125 activos»):

| # | Registro | Destino |
|---|---|---|
| 42 | `fb-2026-09-29-sesion-03-31fb311f` CORRECT RN-003 (sesión 3) | fuera: falso positivo conocido (HOJA-DE-RUTA.md G.2: `feedback pending` no admite dos CORRECT vivos sobre una regla) |
| 43 | `fb-2026-10-04-sesion-04-ca0afae6` CORRECT RN-003 (S-13 de la sesión 4) | fuera: **el mismo falso positivo, y el encargo no lo nombra**: desde `trabajo/sesgo-h4-color` RN-003 cita `6e7da456` y el de S-13 sale pendiente también. No es una pregunta (su caso bajista es la fila 12) |
| — | los 9 «sin forma mecánica» (REJECT y CORRECT sobre evidencia de la sesión 1) y las 7 confirmaciones | fuera: no son preguntas |

**Las que el encargo no nombra y el repo tiene para la sesión 5:**

| # | Cosa | De dónde sale | Destino propuesto |
|---|---|---|---|
| 44 | S-6 (lo mínimo al redondear el stop) | ACTIVAR-SESION-04.md:340-341 | fuera: el consultor la sacó (§5, :833) |
| 45 | A-21 (punto 11 de §0.e) | ACTIVAR-SESION-04.md:342-347 | fuera: RESUELTA (ADR-0076; MOTOR §5 :922) |
| 47 | A-24 (qué pivote de M15 marca: el más reciente ya formado) | `scripts/hoja_preguntas.py:55`; `ambiguedades.yaml:528-566` | fuera: DECIDIDA por ADR-0045, no ABIERTA (D1 mira las ABIERTAS); solo pasaría a RESUELTA con un registro del trader, y lo que tiene de pregunta lo cubre la de la zona (S-9) y A-35 (S-3). La hallé por el auditor (su punto 5) |
| 46 | «Para cerrar» (D6): diciembre con su voz, la exportación de agosto, la confirmación escrita de marzo | PROJECT_STATE.md:42 (I), :52 (Q); REGISTRO-MARZO.md:49-51 | bloque «Para cerrar», sin código. **REGISTRO-MARZO.md §2 pide** la «confirmacion escrita del trader de que es material que ya ha visto (F09)»; marzo en `vistos.yaml` es trabajo de la sesión, no del trader. **NA:I** no dice «con su voz»: dice «SIN vídeo»; preguntar si lo grabó es lo que hace falta para la decisión de construcción o reservado que NA:I deja al consultor |

### 1.b Lo que se junta, y lo que va fuera de la hoja

**Se juntan** (una pregunta, con su «Para precisar»):
- **CORRIDA 4 + A-48 + A-49** (filas 20 y 5): qué velas forman la caja y cuándo la traza. La A
  de VISOR (fila 21) va **justo detrás, como pregunta propia**: VISOR-CONSTRUCCION.md:981-984 dice
  que es otra cosa que ADR-0076 §4.1 y va «junto a la pregunta 4».
- **CORRIDA 6 + A-53 + C1 + C7** (filas 24, 9, 36 y 41): la vida de la orden sin llenar mientras
  el precio sigue (el 1 que se expande, otra liquidez tomada, una caja nueva).
- **CORRIDA 3 + PUNTO-USADO** (filas 19 y 28): las reentradas y la caja de la reentrada, con el
  texto de PUNTO-USADO.md:637-641.
- **CORRIDA 2 + A-57** (fila 18): MARGEN-LOTE.md §5 ya sustituyó una por la otra.
- **CORRIDA 5 + VISOR 2026-08-14** (fila 22): la pregunta de la zona; A-43, A-50 y A-53, que
  CORRIDA pone «junto», van cada una en la suya (una sola pregunta por código, D3).

**No se juntan aunque se parezcan** (medido): ADR-0076 §4.1 (vela sin cuerpo en el retroceso, como
alternancia) y la A de VISOR (vela sin cuerpo dentro del tramo que hace el punto): VISOR lo dice;
ADR-0077 §5 (la racha) y A-44 (el tope): la racha ya está RESUELTA (A-51) y la pregunta es su
lectura provisional.

**Lo ya respondido que la lista vieja repetía** (D3: nunca se repite):
- **A-44, «¿sobre el saldo del inicio del día o con las abiertas?»** (ACTIVAR-SESION-04.md:313-314):
  respondida en la sesión 1, «De la cuenta basado en el saldo, y que sea en el saldo inicial del
  día» (`fb-2026-09-09-sesion-01-bff260ea`, sobre `perdida_maxima_diaria`). Sale de la pregunta; si
  el consultor quiere que el 4,5 % de S-9 sea el mismo número que ese, va en «Para confirmar al
  final», no como pregunta.
- **A-13, «Después de ponerlo a la entrada, ¿lo vuelves a mover?»** (:308-309): lo FIRME de A-13
  ya dice «despues el stop no se mueve» (`ambiguedades.yaml:206-209`). Sale.

**Fuera de la hoja, con su porqué** (filas 29-35, 38-40, 42-45): RN-004 y RN-020 son la medida de
después de activar; A-16, A-28, A-54, A-55 y A-56 se miden; C4, C5 y C6 ya tienen su ambigüedad
RESUELTA (y C4 y C6 los sacó el consultor); los dos pendientes de RN-003 son el falso positivo de
G.2; S-6 y A-21, sacadas o RESUELTAS.

### 1.c El orden, la duración de la sesión 4 y la estimación de la 5

**La sesión 4 duró 2:07:36** (7656,2 s; `knowledge/corpus/fuentes.yaml:104`, v10, sin abrir el
vídeo), con 24 códigos: **5:19 por pregunta** de media, con cuatro cortes de audio dentro
(`fuentes.yaml:101-103`, unos 9:30 en total) que forman parte de esa duración.

**El orden propuesto (D4), 25 preguntas:**

| S | Bloque | Pregunta | Filas |
|---|---|---|---|
| S-1 | 1 | La ruptura simple sin cuerpo (esquema) | 1 |
| S-2 | 1 | Sesgo bajista, rompe por encima con mecha y cierra roja (esquema, sin la sesión 1) | 2 |
| S-3 | 1 | A-35: cuándo das por formado un alto de M15 | 3 |
| S-4 | 1 | A-44: el tope de la semana | 4 |
| S-5 | 2 | El lote que no cabe (A-57) | 18 |
| S-6 | 2 | Las reentradas en el mismo punto y su caja (el 29 de abril) | 19, 28 |
| S-7 | 2 | Qué velas forman la caja y cuándo la trazas (A-48, A-49) | 20, 5 |
| S-8 | 2 | La vela sin cuerpo dentro del tramo del punto (VISOR A) | 21 |
| S-9 | 2 | Qué liquidez y qué zona eliges | 22 |
| S-10 | 2 | A-43, segunda parte: la misma liquidez tomada dos veces | 7 |
| S-11 | 2 | Una toma de la sesión de la mañana con el sesgo contrario (VISOR B; A-46) | 23 |
| S-12 | 2 | A-50: la caja entera o solo el 0 frente al nivel | 8 |
| S-13 | 2 | Hasta cuándo mueves la orden sin llenar, y cuándo la quitas (con A-53) | 24, 9, 36, 41 |
| S-14 | 2 | Qué te hace no operar un día o una sesión | 25 |
| S-15 | 2 | El lado del ruido y las zonas de control | 26 |
| S-16 | 2 | El precio ya pasó el 0 cuando se forma la caja | 27 |
| S-17 | 3 | A-13: el disparador del break even | 6 |
| S-18 | 3 | A-32: la línea que, rota con mecha, te quita la entrada | 10 |
| S-19 | 3 | La vela sin cuerpo en el retroceso (ADR-0076 §4.1) | 13 |
| S-20 | 3 | El breaker contrario que rompe con mecha (ADR-0076 §4.2) | 14 |
| S-21 | 3 | La racha después de la novena (ADR-0077 §5) | 15 |
| S-22 | 3 | El último minuto | 16 |
| S-23 | 4 | Confirmar: la H4 sin color con sesgo bajista | 12 |
| S-24 | 4 | Confirmar: la vela casi plana (las dos lecturas, D7) | 11 |
| S-25 | 4 | Confirmar: el xlsx de julio y los tres primeros vídeos | 17 |

Dentro del bloque 2 el orden es el de CORRIDA 2-9, con cada ampliación junto a la suya: la A de
VISOR tras la 4 (S-8); A-43 segunda parte y la B tras la 5 (S-10, S-11: las dos son qué toma
cuenta); A-50 tras ellas (S-12: el nivel tomado); A-53 dentro de la 6 (S-13).

**Estimación:** 25 × 5:19 = **2:12:55**, unos 5 minutos más que la sesión 4. Se puede dejar, en
este orden: **S-25** (el xlsx de julio: lo comprueba además T, la rama que transcribe v11-v14) y
**S-23** (el caso bajista, de sí o no) para un WhatsApp, con un esquema; y **S-18** (A-32) para la
sesión 6 si el consultor no autoriza ningún gráfico (1.e). Con las tres fuera, 22 × 5:19 = 1:57:00.

### 1.d `scripts/hoja_preguntas.py`

**Corre hoy en la rama** (el código es el de `main`): `uv run python scripts/hoja_preguntas.py
--salida <carpeta de trabajo>/hoja-prueba.docx` → `OK: …`, exit 0. **Pero lo que escribe no sirve
para la sesión 5:**
- el encabezado dice «Sesión 2 · preguntas pendientes» (`:38`) y el nombre por defecto,
  `hoja-sesion-02.docx` (`:36`);
- la regla 2 dice «No enseñar ningún gráfico, de ningún día» (`:41`), que ya no es la de
  SESION-DE-PREGUNTAS.md regla 2 desde 2026-09-28;
- `ORDEN_SESION_02` (`:54-59`) lleva **A-24, que está DECIDIDA** (`ambiguedades.yaml:566`; pasa
  porque `ESTADOS_QUE_SE_PREGUNTAN` admite DECIDIDA, `:60`) y **no lleva A-50, A-53 ni A-57**,
  ABIERTAS de clase pregunta: nada obliga a añadirlas (la guardia de AMBIGUEDADES.md:30-33 es solo
  que no lleve una cerrada);
- solo sabe imprimir el campo `pregunta` de una ambigüedad: las preguntas que no son ambigüedades
  (filas 1, 2, 12-17, 19, 21, 24-28: 15 de las 25) no tienen sitio, ni los códigos S-n, ni las
  partes de D3;
- la B (fila 23) toca A-46, RESUELTA: `preguntas()` la rechaza (`:76-80`, «ya no se preguntan»).

**Los tests que lo fijan:** `tests/unit/test_hoja_preguntas.py` (el orden exacto, `ORDEN`, :28-33,
copia de `ORDEN_SESION_02`; cada pregunta tal cual y en su orden; que una cerrada, una repetida o
una inexistente la paren; que escribe un docx). **El de `tests/unit/test_transcribir_sesion.py:305`
(`test_el_orden_es_el_de_la_hoja_con_a46_tras_a21`) NO fija este script**: fija la copia
`ORDEN_SESION_02` de `scripts/transcribir_sesion.py:90`, la hoja de la sesión 02 tal como se llevó;
lo dice su propio docstring.

**Propuesta, sin tocarlo:** que la hoja de la sesión 5 sea el PDF del consultor hecho con
`docs/sesion-5/PREGUNTAS.md` (como en la sesión 4, cuya hoja tampoco salió de este script:
HOJA-USADA.md), y que el script se quede como lo que hoy es de verdad -el quinto sitio al cerrar
una ambigüedad- con un arreglo mínimo en su rama (decisión 3).

### 1.e Las que pedirían un gráfico o un fotograma de un día real

Los días de construcción que se nombran abajo, comprobados hoy con `casos_ocultos` (solo
`True`/`False`, un guion en la carpeta de trabajo con las fechas literales): **los diez dan
`False`** (2026-01-08, 2026-01-29, 2026-04-27, 2026-04-29, 2026-07-01, 2026-07-08, 2026-07-13,
2026-08-07, 2026-08-14 y 2026-08-20). Ninguno se ha abierto.

| S | Qué se enseñaría | Día | Por qué | Antes de enseñarlo |
|---|---|---|---|---|
| S-18 | el fotograma de v4 0:53:10 (`fr-v4-9ad0ebb8/3203000`, `/3209000`, ya vistos por Aleks el 2026-09-17, `ev-v4-005310-ce69f8c6`) | **sin identificar**: v4 es «entrevista … sobre el backtest de enero en FXReplay» (`fuentes.yaml:32`), y ningún registro dice qué día del replay enseña | A-32 pregunta qué era ESA línea; sin el gráfico solo se puede preguntar en abstracto, y S-23 de la sesión 4 ya dio la regla general | no se abre sin decisión (ACTIVAR-SESION-04.md:836-837). Si se autoriza: saber antes qué día enseña el replay, sin abrir la imagen, y comprobarlo; si no se puede, no se enseña |
| S-6 | la caja del 29 de abril, 09:55 y 09:58 | 2026-04-29 | D2 manda el ejemplo con su texto (PUNTO-USADO.md:637-641); se entiende sin gráfico | si se enseña: `contexto_h4.py` |
| S-7 | días de P2 (CORRIDA-CONSTRUCCION.md §4.5, «tres días que el consultor elegirá») | los de VISOR-CONSTRUCCION.md §2 | la Δ de la caja se ve, no se dice | volver a pasar `contexto_h4.py`: **ADR-0083 cambió el motor después del visor** (R3.2: «si el visor o la spec cambian lo que pintan, se vuelven a comprobar antes»), y las páginas del visor son de antes de ADR-0083 |
| S-8 | la verde con dos velas sin cuerpo y la roja | 2026-01-08, 09:16-09:19 | VISOR A, con su día | ídem |
| S-9 | la compra de las 08:30 sin toma de M15 visible | 2026-08-14 | VISOR, pregunta 5 | ídem |
| S-11 | la toma de las 10:54 y la venta de las 14:29 | 2026-01-08 | VISOR B | ídem |
| S-15 | las dos zonas de control | 2026-01-29 (14:00-14:01), 2026-08-20 (12:57-13:00) | VISOR, pregunta 8 | ídem |
| S-16 | el precio ya pasado el 0 | 2026-07-08 13:42, 2026-07-13 14:14, 2026-01-08 09:04, 2026-08-07 07:34 y 08:43, 2026-04-27 07:00, 07:05, 07:08 | VISOR, pregunta 9 | ídem; **los dos de julio pintan H4 de junio** (VISOR-CONSTRUCCION.md:341): por recuento y pertenencia, y declarado |
| — | **2026-07-01 11-15, el día de julio sin página** | 2026-07-01 | VISOR-CONSTRUCCION.md:444-480: su contexto pinta un día oculto; se comprobó solo con la traza | **no se enseña**: ninguna pregunta lo necesita (era de la pregunta 1 de CORRIDA, que ya no está) |
| S-1, S-2 | el sesgo de H4 | ninguno | D2 y SESGO-H4-COLOR.md:931-933: solo esquema dibujado | — |

Los gráficos «en directo»: ninguna de las preguntas propuestas enseña un gráfico en directo. Si al
preparar el PDF alguien propone uno (por ejemplo, un fotograma de una sesión con el trader), antes
se mira qué días enseña por la fecha de grabación del vídeo y se comprueba (SESGO-H4-COLOR.md §5.3).

**Mi propuesta** (decisión 4): sin gráficos de días reales, salvo los de S-8 y S-16 si el consultor
los quiere, y con `contexto_h4.py` vuelto a pasar antes; todo lo demás, con esquemas inventados.

### 1.f El encargo frente al repo (auditor `auditor-encargo`, 2026-10-19)

65 afirmaciones: 51 correctas, 1 incorrecta y 13 con matiz; 7 cosas que el repo pide y el encargo
no dice. Lo que cambia algo, con lo que hago (el informe entero del auditor queda en la
conversación; aquí, lo que se usa):

- **INCORRECTA (25): «el CORRECT de RN-003 de la sesión 3 sale pendiente»**: salen DOS, el de la
  sesión 3 y `fb-2026-10-04-sesion-04-ca0afae6` (S-13), medido hoy con `feedback pending` («2
  pendientes de 125 activos»). Los dos van fuera de la hoja (filas 42 y 43) y la línea de G.2 para
  el cierre los nombra a los dos (decisión 7).
- **MATIZ (31), las citas:** `kb at --video v7..v10` y `kb find --video v7..v10` los niega la
  guardia SIEMPRE (`.claude/hooks/guardia.py:913-917`, `:1878-1894`; ya lo encontró PUNTO-USADO.md
  :738). La vía que queda, y que D3 permite («por la vía que la guardia permita»), es Read de los
  YAML de `knowledge/evidence/` y `knowledge/feedback/`, y `kb find` sin `--video` para v1-v6.
  **No es PARADA**: hay vía permitida; la fase 1 no intentará la negada.
- **MATIZ (13):** ACTIVAR-SESION-04-MOTOR.md §6 son líneas de cierre, sin preguntas nuevas; repite
  las de §5. Se ha leído igual.
- **MATIZ (19):** V ya trae ADR-0076 §4, ADR-0077 §5 y el bajista de S-13 por «las preguntas de
  esos §5»; lo que le falta es nombrarlas.
- **MATIZ (36) y herencia 7:** lo del xlsx de julio ya lo dijo el trader **de palabra** a Aleks
  (ENTRADA-JULIO.md:336), sin grabar, y la rama de T lo medirá (:343). Su «Lo que nos has dicho»
  no es una cita grabada: decisión 6.
- **MATIZ (39):** NA:I no pide «si grabó diciembre con su voz»; dice «SIN vídeo». Es pregunta del
  consultor, y entra en «Para cerrar» como D6 manda.
- **MATIZ (41):** REGISTRO-MARZO.md §2 (:49-51) pide la confirmación **escrita** de que marzo es
  material que ya ha visto (F09; el heredado 2 dice «sin sus palabras, no vale»): en la sesión solo
  se le pide que la mande por escrito.
- **MATIZ (43):** por ADR-0072:18-21 el consultor es Claude en el chat y no ejecuta; quien lee el
  literal de 1:44:49 con «!» en su terminal es Aleks (NA:H). D7 se aplica igual.
- **MATIZ (52):** la sesión 4 sí preguntó A-32 (S-23 de HOJA-USADA.md:42), sin gráfico, y quedó «en
  parte»; lo que dejó fuera fue el barrido.
- **MATIZ (54):** 2026-07-01 no es un día de VISOR §3.2 sino de su §2.a; está en 1.e igual.
- **MATIZ (57):** V no tiene campo «Depende de»; es la frase «Depende de R1.1, de R3.1, de J (kit
  hoja) y de la copia de seguridad (A.4).». La línea del cierre sustituye «, de J (kit hoja) y» por
  « y», para que no quede «de R3.1,  y de».
- **MATIZ (6):** el contrato protege `scripts/` y `tests/` y no permite anexos: si la decisión 3
  toca el script, el contrato se amplía en su commit; `simular_cierre.py` corre desde la carpeta de
  trabajo, sin anexo commiteado.
- **Herencia 1, la copia de seguridad (A.4):** V y R4.1 dependen de ella, tiene que estar antes de
  grabar la sesión y no está HECHA (HOJA-DE-RUTA.md:214-216, :397-403). El encargo no la nombra.
  Es de Aleks, no del trader, así que no va en «Para cerrar»: va como aviso en el encabezado de
  PREGUNTAS.md y en la decisión 8.
- **Herencia 2:** sin cifras de VIABILIDAD-COMISION ni nada en dinero, y las horas en el reloj del
  trader (Europe/Madrid) (VISOR :943-944; MARGEN-LOTE :889-890; PUNTO-USADO :635). Se aplica en
  la fase 1.
- **Herencia 3:** A-35 y A-44 solo se activan con las lecturas cerradas de ACTIVAR-A35-A44.md
  (:45-95; si no encaja, PARAR, :164-180): las opciones de S-3 y S-4 se escriben para que cada una
  caiga en una lectura documentada.
- **Herencia 4:** la premisa de cada pregunta se comprueba contra la spec de hoy (la lista de §0.e
  es del 2026-10-11, anterior a ADR-0080, ADR-0081 y ADR-0083; ERRORES-RECURRENTES.md:56). La
  fase 1 escribe «Lo que todavía no sabemos» contra el valor vigente de cada parámetro.
- **Herencia 6:** en cualquier texto con días de un mes con reservados, nunca juntos un rango de
  fechas y un recuento de reservados (ERRORES-RECURRENTES.md:85): las de julio pintan H4 de junio.

### 1.g Lo que no pude medir

- **Qué día del replay enseña el fotograma de v4 0:53:10**: no consta en ningún registro y no se
  abre una imagen para saberlo (ADR-0038).
- **Si `contexto_h4.py` sigue dando «no» con el motor de hoy** en los días de 1.e: correrlo es
  generar contexto de esos días, y el encargo dice «no abras nada: lista y propón».
- **El ritmo de la sesión 4 por pregunta**, no la media: separar los minutos de cada código es leer
  la filtrada de v10, que está en cuarentena; la media sale de `fuentes.yaml` y de HOJA-USADA.md.

### 1.h Exposiciones de la fase 0

Ninguna. Lo leído son informes, ADR, la spec, ítems de evidencia y registros de feedback; un
`kb find "otra reentrada"` (la CLI filtrada, sin `--video`: dos resultados de v4 y v5, y la línea
OCULTOS); los diez días de 1.e se comprobaron con `casos_ocultos` imprimiendo solo `True`/`False`,
y todos son de construcción. No hay fila nueva en `HOLDOUT-EXPOSICIONES.md`.

## Lo que necesito que decidas

0. **El orden y las 25 preguntas de 1.c.** Opciones: (a) las 25, en el orden de 1.c, con S-25 y
   S-23 marcadas «si falta tiempo, por WhatsApp» y S-18 «si falta tiempo, a la sesión 6»; (b) las
   22 sin esas tres desde el principio. Recomiendo (a): la estimación pasa de la sesión 4 en unos
   5 minutos, poco para quitar nada de antemano. Coste de (b): tres respuestas por escrito, que no
   se graban, y una sesión 6 más larga.
1. **Las dos subpreguntas ya respondidas** (1.b: el saldo inicial del día en A-44, «¿lo vuelves a
   mover?» en A-13). Opciones: (a) salen; lo dicho va en «Lo que nos has dicho»; (b) quedan como
   «Para confirmar al final». Recomiendo (a): D3 prohíbe repetir lo respondido y las dos tienen
   registro. Coste de (b): ninguno grave, un minuto y el riesgo de que conteste otra cosa.
2. **El orden de las dos del sesgo, y qué lleva la de la contradicción.** El «Lo que nos has
   dicho» de S-1 (la ruptura simple sin cuerpo) tiene que ser el WhatsApp del 2026-10-14 («debe de
   haber roto con cuerpo o con mecha el bajo de la vela alcista Y terminar al cierre bajista»), y
   ese literal contesta S-2 antes de preguntarla. Opciones: (a) S-1 la contradicción, sobre el
   esquema y con «Lo que nos has dicho» vacío por D2 («se pregunta sobre el esquema»), y S-2 la
   ruptura sin cuerpo, con el WhatsApp; (b) el orden de SESGO-H4-COLOR.md §4.4 (sin cuerpo primero)
   y la contradicción con el WhatsApp delante; (c) el orden de §4.4, y la contradicción sin «Lo
   que nos has dicho». Recomiendo (a): la contradicción solo se resuelve si contesta sin tener
   delante la regla que la decide. Coste de (b): su respuesta será leer la regla; de (c): S-1 ya le
   ha leído la regla un minuto antes.
3. **`scripts/hoja_preguntas.py` (1.d).** Opciones: (a) no se toca en esta rama: la hoja de la
   sesión 5 es el PDF del consultor con `docs/sesion-5/PREGUNTAS.md`, como en la 4, y va una línea
   a G (encabezado y regla 2 de la sesión 2, A-24 DECIDIDA en el orden, A-50, A-53 y A-57 fuera);
   (b) el arreglo mínimo aquí: sale A-24, entran A-50, A-53 y A-57, el encabezado y la regla 2 al
   día, con sus tests, el contrato ampliado y CI por `fix/barrido-sesion-5`; (c) que el script
   genere la hoja desde PREGUNTAS.md. Recomiendo (a): la hoja de la 5 no sale del script en
   ninguna de las tres, y (b) y (c) meten código en una rama de documentos. Coste de (a): el
   script sigue desfasado hasta su rama.
4. **Gráficos de días reales (1.e).** Opciones: (a) ninguno: todas con esquemas inventados, y los
   días se quedan en el informe como clave de Aleks; (b) además, S-8 (2026-01-08) y S-16 (los
   cinco días del precio pasado el 0) con sus gráficos de construcción, tras pasar otra vez
   `contexto_h4.py` (ADR-0083 cambió el motor) y declarado; (c) además el fotograma de v4 0:53:10
   para S-18. Recomiendo (a): D2 lo pone por defecto, y las de la caja se entienden con un esquema
   como en la sesión 4. Coste de (b): un paso más con el visor y una fila de exposiciones; de (c),
   un día del replay que nadie sabe cuál es.
5. **A-32 sin el fotograma.** Opciones: (a) en abstracto: «¿hay alguna línea en M1 que, si el
   precio la rompe solo con la mecha, te quite la entrada? ¿Cuál?», con un esquema; (b) a la
   sesión 6, con el fotograma si se identifica el día; (c) fuera, como en el barrido de la 4.
   Recomiendo (a): S-23 ya dio la regla general, y lo que falta es si existe esa clase de línea, no
   cuál era esa. Coste de (b): A-32 sigue abierta un mes más.
6. **El xlsx de julio (S-25).** Opciones: (a) se pregunta, y «Lo que nos has dicho» dice «nos lo
   dijiste de palabra el 13 de octubre, sin grabar», para que quede en la voz; (b) no se pregunta:
   lo mide T. Recomiendo (a): cuesta medio minuto y deja la cita grabada que ENTRADA-JULIO.md:336
   no tiene. Coste de (b): ninguno si T lo mide; T todavía no tiene rama.
7. **Las líneas para el cierre de lo que el auditor encontró:** G.2 nombra los dos pendientes de
   RN-003 (`31fb311f` y `ca0afae6`); y una línea a G para el script (si 3a). Opciones: (a) van a
   «Líneas preparadas para el commit del contrato»; (b) se quedan solo en el informe. Recomiendo
   (a): G.2 hoy dice uno y son dos.
8. **La copia de seguridad (A.4)**, de la que V depende y que no está HECHA. Opciones: (a) aviso en
   el encabezado de PREGUNTAS.md («antes de grabar: A.4») y nada más; (b) el aviso y, además, V la
   conserva en su «Depende de» en la línea del cierre (solo sale J). Recomiendo (b): el encargo
   solo quita J, y A.4 sigue siendo verdad. Coste de (a): V perdería una dependencia real si alguien
   reescribe la frase entera.

Espero tu respuesta a la PARADA.

## Respuesta del consultor a la PARADA (2026-10-19)

Copiada tal cual (también al final del encargo):

> Respuesta del consultor a la PARADA de la fase 0 de trabajo/barrido-sesion-5 (2026-10-19). Cópiala tal cual en el informe y aplícala punto por punto (skill fase-cero).
>
> 0. (a). Las 25, en el orden de 1.c. S-25 y S-23 llevan la marca «si falta tiempo, por WhatsApp» y S-18 la de «si falta tiempo, a la sesión 6». Por qué: la estimación supera en unos 5 minutos a la sesión 4, y eso no basta para quitar nada de antemano.
> 1. (a). Las dos subpreguntas salen, y lo que ya está registrado pasa a «Lo que nos has dicho» con su id (fb-2026-09-09-sesion-01-bff260ea para el saldo inicial del día; lo FIRME de A-13, ambiguedades.yaml). Por qué: D3 prohíbe repetir lo respondido.
> 2. (a). S-1 es la contradicción: va sobre el esquema de dos velas y con «Lo que nos has dicho» vacío, con la frase «se pregunta sobre el esquema». S-2 es la ruptura simple sin cuerpo, y lleva el WhatsApp del 2026-10-14 como «Lo que nos has dicho». Las dos van con esquema inventado, como manda D2. Por qué: la contradicción solo se resuelve si el trader contesta sin tener delante la regla que la decide. Es una desviación del orden de SESGO-H4-COLOR.md §4.4, y el documento la declara.
> 3. (a). hoja_preguntas.py no se toca en esta rama. La hoja de la sesión 5 es el PDF del consultor hecho con docs/sesion-5/PREGUNTAS.md, como en la sesión 4. Una línea para G recoge lo que tiene desfasado: el encabezado y la regla 2 de la sesión 2, A-24 DECIDIDA dentro del orden, A-50, A-53 y A-57 fuera, y la B, que toca A-46 (RESUELTA). Por qué: la hoja de la 5 no sale del script, y esta rama es de documentos.
> 4. (a). Ningún gráfico de un día real: todo con esquemas inventados, y los días se quedan en el informe como clave de Aleks. Por qué: es lo que D2 pone por defecto, y así no hay que volver a pasar contexto_h4.py ni declarar exposiciones.
> 5. (a). A-32 en abstracto, con un esquema: «¿hay alguna línea en M1 que, si el precio la rompe solo con la mecha, te quite la entrada? ¿Cuál?». Por qué: S-23 de la sesión 4 ya dio la regla general, y lo que falta saber es si existe esa clase de línea.
> 6. (a). S-25 se pregunta. Su «Lo que nos has dicho» no es una cita: dice «nos lo comentaste de palabra el 13 de octubre, sin grabar», para que quede en la voz. Por qué: cuesta medio minuto y da la cita grabada que ENTRADA-JULIO.md no tiene.
> 7. (a). Van a «Líneas preparadas para el commit del contrato»: G.2 nombra los dos pendientes de RN-003 (31fb311f y ca0afae6), y entra la línea para G del punto 3. Por qué: hoy G.2 dice uno y son dos.
> 8. (b). Aviso en el encabezado de PREGUNTAS.md («antes de grabar, la copia de seguridad A.4»), y V conserva A.4 en su frase de dependencias. La línea del cierre sustituye «, de J (kit hoja) y» por « y», como propones en el matiz 57. Por qué: A.4 sigue siendo verdad, y solo sale J.
>
> Además:
> - Herencia 3: las opciones de S-3 (A-35) y S-4 (A-44) se escriben de modo que cada una caiga en una lectura documentada de ACTIVAR-A35-A44.md §1. Debajo de cada opción, en el documento y no en la hoja del trader, pon la lectura en la que cae.
> - Herencias 2, 4 y 6: se aplican como dices. Sin dinero, con las horas en Europe/Madrid, con cada premisa contrastada con la spec de hoy y sin juntar nunca un rango de fechas con un recuento de reservados.
> - Matiz 43: es correcto. El literal de 1:44:49 lo lee Aleks en su terminal; hasta que lo diga, S-24 va con las dos lecturas.
> - La corrección del punto 25 (dos falsos positivos, no uno) y la del matiz 31 (la guardia niega kb sobre v7-v10) van al informe como hallazgos del auditor sobre el encargo.
>
> Sigue con la fase 1 sin parar: PREGUNTAS.md, make check sellado (con la línea PICO DE MEMORIA), revisor, entregar-rama y «Rama lista para revisión, NO cerrada».

## 2 · Fase 1 · La respuesta aplicada y `docs/sesion-5/PREGUNTAS.md` (2026-10-19)

### 2.a La respuesta, punto por punto

| Punto | Qué manda | Hecho | Dónde |
|---|---|---|---|
| 0 | Las 25 en el orden de 1.c; S-25 y S-23 «si falta tiempo, por WhatsApp»; S-18 «si falta tiempo, a la sesión 6» | Hecho | PREGUNTAS.md §1 (las marcas en sus títulos y en la entrada del §1) |
| 1 | Las dos subpreguntas salen; lo registrado pasa a «Lo que nos has dicho» con su id | Hecho | S-4 cita `fb-2026-09-09-sesion-01-bff260ea`; S-17 cita `9f506366` y lo FIRME de A-13. Matiz: el literal de 9f506366 dice «se mantiene en M1»; «después el stop no se mueve» es la lectura registrada (`valor_resultante` y `ambiguedades.yaml:206-209`), y S-17 lo escribe así, como registrado y no entre comillas |
| 2 | S-1 la contradicción, con «se pregunta sobre el esquema»; S-2 la ruptura sin cuerpo, con el WhatsApp; las dos con esquema; la desviación del orden declarada | Hecho | PREGUNTAS.md S-1, S-2 y la desviación 2 del encabezado. S-1 no nombra ninguna sesión anterior ni en sus líneas para Aleks |
| 3 | `hoja_preguntas.py` no se toca; la hoja es el PDF del consultor; línea para G | Hecho | PREGUNTAS.md, encabezado; la línea, en §4 (G.2) |
| 4 | Ningún gráfico de un día real; los días, clave de Aleks en el informe | Hecho | PREGUNTAS.md, «Cómo se leen»; la clave en §2.c |
| 5 | A-32 en abstracto, con esquema | Hecho | S-18 |
| 6 | S-25 con «nos lo comentaste de palabra el 13 de octubre, sin grabar» | Hecho | S-25 |
| 7 | G.2 nombra los dos pendientes de RN-003 y entra la línea del punto 3 | Hecho | §4 |
| 8 | Aviso de A.4 en el encabezado; V conserva A.4; «, de J (kit hoja) y» → « y» | Hecho | PREGUNTAS.md, encabezado; §4 |
| Además · herencia 3 | Opciones de S-3 y S-4 en lecturas de ACTIVAR-A35-A44.md §1, con la lectura debajo, fuera de la hoja | Hecho | S-3: (a) `inicio_vela_contraria`, (b) `cierre_vela_contraria`. S-4: (a) `dia`, (b) `ambos`. «Otra» → PARAR. La opción vieja de §0.e.4 «(a) cuando cierra la vela que lo hace» **no caía en ninguna lectura** y se sustituyó |
| Además · herencias 2, 4 y 6 | Sin dinero, horas de Madrid, premisas con la spec de hoy, nunca rango de fechas con recuento de reservados | Hecho | §2.b |
| Además · matiz 43 | S-24 con las dos lecturas hasta que Aleks lea 1:44:49 | Hecho | S-24 cita los dos ítems (`ev-v10-014310-2296423b`, «1 o 2 puntos»; `ev-v10-014438-95464201`, «12 puntos») y las opciones no eligen |
| Además · punto 25 y matiz 31 | Al informe como hallazgos del auditor sobre el encargo | Hecho | §1.f (los dos primeros) y §3 |

### 2.b Cómo se comprobó el documento

- **Las citas salen de lo registrado.** Cada literal de «Lo que nos has dicho» se copió del campo
  `cita_literal` de un ítem de `knowledge/evidence/` o del `respuesta_literal` de un registro de
  `knowledge/feedback/`, leídos con Grep sobre sus ficheros, con su id al lado. Dos excepciones,
  declaradas: S-6 (el literal del 29 de abril no tiene ítem: sale de
  `LA-CAJA-DEL-29-DE-ABRIL.md:242`, y su minuto, del segmento de v5 que localiza `kb find`) y S-25
  (no es cita: lo manda el punto 6). S-13 dice, sin comillas, que en la misma respuesta dio por
  buena la otra opción, con la tabla 0.a de ACTIVAR-SESION-04.md como fuente.
- **Ninguna cita cae en un tramo no citable**: los t0-t1 de cada ítem citado de v6, v7, v9 y v10,
  comparados uno a uno con los tramos de su vídeo en `tramos_no_citables.yaml`. El más cercano,
  `ev-v10-014438-95464201` (1:44:38-1:45:04), empieza 17 s después del tramo 1:43:42-1:44:21.
- **Ninguna «en parte» repite lo respondido.** Además de las dos subpreguntas de la decisión 1,
  al repasar los «Para precisar» salieron siete que ya tenían respuesta registrada y se
  cambiaron antes del commit: el caso 4 del WhatsApp (S-1), el cuerpo de uno o dos puntos en H4
  (S-2, notas de `ca0afae6`), si cuenta lo abierto (S-4, la subpregunta que la decisión 1 quitó),
  el 1 de la caja en el punto más alto (S-7, `ev-v9-004721`), la toma de las 6:45 sola (S-10,
  `c3d0c855`), el M1 del break even (S-17, `9f506366`) y la ganadora y el break even en la racha
  (S-21, `8e2d728a`). El lado de ruido de la pregunta 8 tampoco se pregunta: lo dice
  `ev-v9-004919-c6bfb3ee` (S-15, línea para Aleks).
- **Las premisas, con la spec de hoy** (`knowledge/spec/parametros.yaml`, leído con un guion en la
  carpeta de trabajo): `caja_se_fija = en_cada_cierre_m1`, `caja_bloque = r6` y
  `orden_stop_punto = ultimo_pivote_m1` (DEFAULT_AMBIGUOUS, A-49 y A-48);
  `orden_pendiente_al_abrir_escenario = se_mueve` (DEFAULT_AMBIGUOUS, A-53); `lote_si_no_cabe =
  limitar` (DEFAULT_AMBIGUOUS, A-57); `toma_antes_de_la_ventana = cuenta`, `break_even_* = mecha /
  tocar`, `racha_perdidas_reinicio = nunca`, `zonas_control_max_por_esquema = 1` y
  `perdida_maxima_semanal = 9` (CONFIRMED); `liquidez_m15_pivote_formado`,
  `perdida_trader_alcance` y `perdida_trader_magnitud` (UNKNOWN). Cada «Para Aleks» dice lo que hace
  hoy el bot con esos valores. Una premisa cambió desde que se escribió la lista: la tabla 0.a de
  ACTIVAR-SESION-04.md daba `caja_se_fija = al_verse_el_punto`, y ADR-0074, en la misma rama, la
  pasó a `en_cada_cierre_m1`; S-7 lo dice con el valor de hoy. Las de ADR-0080, ADR-0081 y ADR-0083
  están en S-1, S-2, S-5, S-6 y S-16.
- **Sin dinero ni VIABILIDAD-COMISION**: la única cifra de la cuenta es la de S-5 (50 lotes y
  1:30), que MARGEN-LOTE.md §5 manda. **Horas**: las de S-6 (09:55 y 09:58) y S-11 (10:54, 11:00)
  son de Madrid; la del WhatsApp de S-2 (14:55) se dice «hora de Lima», como su registro.
- **Fechas**: PREGUNTAS.md nombra un solo día de mercado, el 29 de abril (S-6, por orden del
  encargo; `casos_ocultos` → `False`). Las demás fechas son de mensajes y de sesiones (el
  2026-10-14, el 13 de octubre, el 2026-10-19). Ningún recuento de reservados en ningún sitio.

### 2.c La clave de Aleks: los días de construcción de cada caso (no se enseñan)

Por la decisión 4, ninguna pregunta enseña un día real. Si en la sesión el trader pide un ejemplo,
estos son los días en que se ve cada caso (de VISOR-CONSTRUCCION.md §3.2 y CORRIDA-CONSTRUCCION.md
§4.5), todos con `casos_ocultos` → `False` (§1.e). **Antes de enseñar cualquiera, hay que volver a
pasar `contexto_h4.py`**: ADR-0083 cambió el motor después de las páginas del visor.

| S | Caso | Día y hora (Madrid) |
|---|---|---|
| S-6 | la reentrada en el mismo punto | 2026-04-29, 09:55 y 09:58 |
| S-8 | la verde, dos velas sin cuerpo y la roja | 2026-01-08, 09:16-09:19 (compra de las 09:21) |
| S-9 | la compra sin toma de M15 visible para el bot | 2026-08-14, 08:30 |
| S-11 | la toma de la mañana y la venta de la tarde | 2026-01-08, 10:54 y 14:29 |
| S-15 | dos zonas de control desde la toma | 2026-01-29 (13:51, 14:00-14:01); 2026-08-20 (12:46, 12:57-13:00) |
| S-16 | el precio ya pasado el 0 | 2026-07-08 13:42; 2026-07-13 14:14; 2026-01-08 09:04; 2026-08-07 07:34 y 08:43; 2026-04-27 07:00, 07:05 y 07:08 (los dos de julio pintan H4 de junio) |
| — | 2026-07-01 11-15 | no se enseña nunca: su contexto pinta un día oculto |

### 2.d Desviaciones

- **El orden de las dos del sesgo** (decisión 2), declarado en PREGUNTAS.md.
- **S-6 lleva dos preguntas**, porque D2 manda el texto de PUNTO-USADO.md §5 tal cual; D3 pide
  una. Declarado en PREGUNTAS.md.
- **S-6 cita un literal sin ítem de evidencia** (§2.b).
- **S-14 y S-5 tienen «Lo que nos has dicho» sin respuesta**: no hay nada registrado sobre eso
  (S-5 lleva el respaldo débil que MARGEN-LOTE.md §5 ya nombra).
- **`kb at` y `kb find --video` no se usaron sobre v7 a v10** (la guardia los niega): las citas de
  esas sesiones salen de los YAML, la vía que D3 permite. No es una guardia rodeada: no se intentó
  la vía negada.

## 3 · El encargo, punto por punto

| Punto | Qué pide | Hecho | Dónde |
|---|---|---|---|
| 0 | Base comprobada con git y con gh (sin curl); abrir con abrir-rama, tramo R4; artefacto y rutas | Hecho | §0; `contrato.yaml`; commit a70ea6e |
| 0 | Skills fase-cero (con auditor-encargo) y entregar-rama | Hecho | §1, §1.f; §7 |
| 1 | El barrido, como el de la sesión 4 | Hecho | §1; PREGUNTAS.md |
| 2 D1 | Todas las fuentes, leídas ahora; lo que no entra, a «fuera» con su porqué | Hecho | §1.a (47 filas); PREGUNTAS.md §3 |
| 2 D2 | Cerradas con «otra, ¿cuál?»; desviación declarada; esquemas; sin gráficos reales; la pregunta 3 con su texto | Hecho | PREGUNTAS.md, encabezado; S-6 |
| 2 D3 | Las seis partes; «en parte» sin repetir; citas de lo registrado | Hecho | §2.b |
| 2 D4 | Orden por impacto en cuatro bloques; duración de la 4 y estimación de la 5 | Hecho | §1.c; PREGUNTAS.md §1 |
| 2 D5 | S-1 a S-n de la sesión 5, dicho, con la forma en voz | Hecho | PREGUNTAS.md, encabezado |
| 2 D6 | «Para cerrar» sin código: diciembre, agosto, marzo (verificado qué pide) | Hecho | PREGUNTAS.md §2; §1.f (matices 39 y 41) |
| 2 D7 | S-14 de la sesión 4 (aquí S-24) con las dos lecturas | Hecho | S-24 |
| 3 | Rama de documentos; holdout solo de construcción, comprobado; «## 0. Qué se abrió»; PS 22.580 bytes | Hecho | PREGUNTAS.md §0; §1.h; §0 |
| 4 a-e | Inventario y PARADA | Hecho | §1 y «Lo que necesito que decidas» |
| 5 | PREGUNTAS.md y make check sellado con el PICO DE MEMORIA | Hecho | §5 |
| 6 | Encargo frente a lo hecho, desviaciones, fase 0 y las líneas del cierre, con la simulación | Hecho | §2.d, §3, §4 |
| 7 | Revisor con los cinco controles añadidos | Hecho | §7 |
| 8 | CI: decir que no toca hooks, rutas ni sistema de archivos, con la lista | Hecho | §6 |

## 4 · Líneas preparadas para el commit del contrato de la orden de cierre

**La decisión del consultor del 2026-10-19 sobre J, copiada tal cual:** «J (kit hoja) NO bloquea V.
kit hoja es la hoja Word para sesiones que etiquetan días; la sesión 5 es solo de preguntas
(SESION-DE-PREGUNTAS.md, scripts/hoja_preguntas.py y el PDF del consultor), como la 2, la 3 y la
4.»

**`PROJECT_STATE.md`:**
- **F** pasa a: «F. V. Las ramas de R6a (ADR-0082) van en los huecos de espera y no le quitan turno
  a V.»
- **V**: «Depende de R1.1, de R3.1, de J (kit hoja) y de la copia de seguridad (A.4).» pasa a
  «Depende de R1.1, de R3.1 y de la copia de seguridad (A.4). Hoja de preguntas:
  docs/sesion-5/PREGUNTAS.md (trabajo/barrido-sesion-5).» (decisión 8: A.4 se queda).
- **J** no cambia de texto: sigue viva, con NA:J en G.2.

**`docs/plan/HOJA-DE-RUTA.md`:**
- **R4.1, «Qué es»**: la frase partida de :212-213, « La hoja\n  Word necesita antes que `kit hoja`
  funcione con un paquete nuevo (NA:J).», sale entera, y en su lugar: «; y lo que V añade: las «en
  parte» de ACTIVAR-SESION-04.md §0.e, las líneas de ACTIVAR-SESION-04-MOTOR.md §6, si el xlsx de
  julio es la exportación de v11 a v13 (ENTRADA-JULIO.md §8) y la pregunta 3 con el ejemplo del 29
  de abril y la caja de la reentrada (PUNTO-USADO.md §5). Hoja de preguntas:
  docs/sesion-5/PREGUNTAS.md (trabajo/barrido-sesion-5).»
- **R4.1, «Refs»**: sale `NA:J · `.
- **G.2**: «(J, antes de R4)» y «(J, antes de R4.1)» pasan a «(J, antes de la próxima sesión que
  etiquete días)»; J sigue en G.2 con NA:J en sus Refs.
- **G.2, los pendientes de RN-003** (decisión 7): «(RN-003 cita el de S-13 y el de la sesión 3, y el
  segundo sale pendiente)» pasa a «(RN-003 cita `fb-2026-10-04-sesion-04-6e7da456` desde ADR-0080, y
  salen pendientes los dos CORRECT anteriores, `fb-2026-09-29-sesion-03-31fb311f` y
  `fb-2026-10-04-sesion-04-ca0afae6`, BARRIDO-SESION-5.md §1.f)».
- **G.2, la línea del script** (decisión 3) **y la del runbook** (encargo §6), al final de «Qué es»:
  «Y, desde `trabajo/barrido-sesion-5` (BARRIDO-SESION-5.md §1.d y §4): `scripts/hoja_preguntas.py`
  sigue con el encabezado y la regla 2 de la sesión 2, lleva A-24 (DECIDIDA) en su orden, no lleva
  A-50, A-53 ni A-57 y no puede llevar la B de VISOR-CONSTRUCCION.md §3.2 (toca A-46, RESUELTA); y
  el paso 6 de «Antes» de `docs/runbooks/SESION-DE-PREGUNTAS.md` dice todavía «abril o agosto», que
  su regla 2 amplió a julio del 1 al 17 y a enero del 2 al 30.»

**Simulado en memoria**, con un guion en la carpeta de trabajo (como `simular_cierre.py` de
VISOR-CONSTRUCCION, sin commitear: el contrato no admite anexos) que aplica cada cambio como
sustitución exacta que casa una vez y corre las funciones a, b y c de `test_hoja_de_ruta.py` y las
cuatro de `test_project_state.py` sobre el resultado:

```
a: []
b: []
c: []
test_project_state_exists: pasa
test_project_state_has_required_sections_in_order: pasa
test_project_state_declares_a_branch: pasa
test_project_state_cabe_en_el_tope: pasa
PROJECT_STATE hoy: 22694 bytes
PROJECT_STATE simulado: 22735 bytes
```

PROJECT_STATE quedaría en **22.735 bytes** con las líneas sobre el de la rama (22.694, que es el de
`main` más la `Current Feature` de la rama); el cierre vuelve a escribir esa sección. La función d
de `test_hoja_de_ruta.py` (las extracciones de las sesiones) no la tocan estas líneas.

## 5 · make check

| Commit | Resultado | PICO DE MEMORIA |
|---|---|---|
| a70ea6e (apertura), primer intento | rojo: 1 failed, 2689 passed (`test_project_state_rutas`: `Current Feature` citaba `docs/sesion-5/PREGUNTAS.md` antes de existir); arreglado sin rodear nada | — |
| a70ea6e (apertura) | 2690 passed, `SELLO` | PICO DE MEMORIA de make check: 296 MiB en test (suma de sus procesos, memoria comprometida, Windows; el mayor proceso, 286 MiB) |
| 758552d (fase 0) | 2690 passed, `SELLO` | PICO DE MEMORIA de make check: 294 MiB en test (suma de sus procesos, memoria comprometida, Windows; el mayor proceso, 284 MiB) |
| fase 1 (PREGUNTAS.md) | en curso al escribir esta línea; su resultado, en el commit siguiente | — |

`test_nunca_bloquea_y_es_rapido` no falló en ninguno: no hace falta la línea para G.

## 6 · CI de Linux

La rama no toca hooks, rutas ni el sistema de archivos: no hace falta `fix/barrido-sesion-5`.
Ficheros cambiados frente a `main` (`git diff main --name-only`):

```
PROJECT_STATE.md
contrato.yaml
docs/encargos/trabajo-barrido-sesion-5.md
docs/sesion-5/PREGUNTAS.md
docs/state/HISTORIA.md
docs/validation/BARRIDO-SESION-5.md
```

## Estado

EN CURSO · fase 1 hecha (2026-10-19): `docs/sesion-5/PREGUNTAS.md` escrito con las decisiones
del consultor; falta el revisor (§7) y entregar la rama.
