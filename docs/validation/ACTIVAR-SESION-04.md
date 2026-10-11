# ACTIVAR-SESION-04 · Las respuestas de la sesión 4 entran en la spec (R1.1, entrada E)

Rama `trabajo/activar-sesion-04`, abierta el 2026-10-11 desde `main` en 11df2c4 (commit de estado
sobre el merge 11a63ad, tag `stable/F37l-entorno-code`). Encargo:
`docs/encargos/trabajo-activar-sesion-04.md`. Tramo: R1 (R1.1 de `docs/plan/HOJA-DE-RUTA.md`;
E de la Next Action).

Antes de abrir se comprobó con git (skill `abrir-rama`, paso 1):

- `git rev-parse --short main` = 11df2c4; `git rev-parse main origin/main` da dos veces
  11df2c4344fd0e55dd2cf84109cc2b87dde36b30; `git status --short` vacío.
- El último tag de `docs/state/HISTORIA.md` es `stable/F37l-entorno-code`;
  `git rev-parse "stable/F37l-entorno-code^{commit}"` = `git rev-parse main^1` =
  11a63ad28fa6906961dab576599d4226b113a119; `git ls-remote --tags origin stable/F37l-entorno-code`
  devuelve el tag.
- La CI de `main` sobre 11df2c4344fd0e55dd2cf84109cc2b87dde36b30 (API de check-runs con el sha
  literal): check `python`, `completed` / `success`, run 38156003516.
- `git branch --list` solo da `main`; `git ls-remote --heads origin "fix/*"` sale vacío.

## 0. Fase 0 · Inventario medido, sin tocar spec, knowledge ni código

Medido el 2026-10-11 sobre d77938c (la apertura, encima de 11df2c4). Lo leído: la extracción
(`SESION-04-EXTRACCION.md` §3–§6, su revisión y su orden de cierre), `SESION-03-EXTRACCION.md` §5,
`ambiguedades.yaml`, `parametros.yaml`, `strategy_spec.yaml`, los ADR 0039, 0040, 0053, 0060, 0061,
0064, 0065, 0066, 0069, 0070 y 0072, el motor (`domain/sesgo.py`, `domain/estructura_m1.py`,
`engine/zonas.py`, `engine/primitivas_broker.py`, `engine/cableado.py`, `engine/tope_trader.py`,
`engine/motor.py`, `cli.py`), los tests que congelan valores, `scripts/hoja_preguntas.py`,
`tests/unit/test_hoja_de_ruta.py`, `docs/sesion-4/PREGUNTAS.md` y `HOJA-USADA.md`,
`knowledge/corpus/tramos_no_citables.yaml` (v10) y dos ítems `ev-v10-*` de S-14. Los
`feedback trace` de las 17 ambigüedades y de A-42, `feedback pending` y `feedback apply --check`
de la sesión 4 se ejecutaron uno a uno (la guardia niega los bucles `for` y los comandos
encadenados). **Nada de material**: ni libros, ni crudas, ni fotogramas, ni holdout. De
`knowledge/cases/` solo se contaron ficheros de `knowledge/cases/dev/` por su ruta literal
(`git ls-files knowledge/cases/dev/caso-eurusd-2026-08-*.yaml | wc -l`): agosto es material de
desarrollo sin ningún día reservado (`fuentes.yaml`, v7, medido el 2026-09-27 con `casos_reservados`
y `casos_ocultos`). **Exposiciones: ninguna.**

### 0.a Tabla de activación (activar-sesion, paso 1)

Una fila por código de la tabla final (§5). «Registro que hoy la cierra» es `feedback trace`:
**ninguna de las 17 tiene registro** salvo A-36 (su cadena de REOPEN) y A-42 (RESUELTA). La hoja de
ruta (R1.1) la esperan todas; el detalle de quién más, en §0.c. Las citas son las de la extracción,
cruzadas con los 21 tramos de v10 de `tramos_no_citables.yaml`, márgenes incluidos (el final de
cada tramo es exclusivo y va un segundo más allá del bloque).

| Código | Amb. | Lo que dijo (resumen fiel; tramo mm:ss) | Parámetro hoy (estado, valor) | Premisa vigente | Reloj | Qué falta | Destino |
|---|---|---|---|---|---|---|---|
| S-7 | A-42 | 6–10 y 10–2 desde el 25-10, en su reloj (62:56–65:29) | `reloj_sesiones` = `rejilla_h4`, CONFIRMED (ADR-0069); `fb-2026-10-04-sesion-04-fb7831cc` RESOLVE_UNKNOWN activo | sí | fijado en la rejilla H4, UTC por zoneinfo (ADR-0069) | nada | **RESUELTA; no se toca** |
| S-1 | A-49 | la orden va en el punto en cuanto una M1 cierra más allá del extremo, con mecha o cuerpo; la caja se traza con la vela cerrada «o, si quieres, la vas actualizando» (00:09–20:00) | `caja_se_fija` = `al_verse_el_punto`, DEFAULT_AMBIGUOUS (A-49) | sí | n/a | lo firme (vela cerrada) es lo que hace el motor (ADR-0028; `zonas.py:364-368` solo M1 cerradas); «en formación» sigue sin fijar | sesión 5 |
| S-2 | A-49 | el mínimo pasa a punto cuando el precio toma en M1 el extremo anterior, aunque sea con mecha; el color de la vela siguiente no importa (20:04–28:22) | idem | sí | n/a | esquema inventado; coincide con S-1 | sesión 5 |
| S-3 | A-18 | stop ya en el 0,8 al poner la orden; el 1 solo plantea el RR; objetivo = 3 × (0→1); lote 0→0,8 (28:26–44:44; `ev-v10-003559-211855b7`, `ev-v10-003706-5b7055a2`, `ev-v10-003927-2f6d9f48`) | `base_calculo_objetivo` = `caja_completa`, `objetivo_rr` = 3, `stop_fraccion_caja` = 0,8, `lotaje_base` = `hasta_stop_fraccion`, todos CONFIRMED desde la sesión 3 o antes; sin registro sobre A-18 | sí (regla, repetida tres veces) | n/a | solo spec (el motor ya lo hace: RN-011 y RN-015); **choca con ADR-0040** | **PARADA b.1** |
| S-4 | A-49 | con la orden sin llenar, el 1 se expande al máximo nuevo «mientras no se desarrolle otro punto breaker»; el 0 y el punto se quedan; la distancia no importa (46:41–51:42; `ev-v10-004945-59ebac47`, `ev-v10-005056-1a55d5b4`, `ev-v10-005116-2a9ff066`) | `caja_se_fija` = `al_verse_el_punto` (DEFAULT_AMBIGUOUS, A-49); la otra opción `en_cada_cierre_m1` ya existe (`zonas.py:87`, `:395-399`) | sí | n/a | cambiar el VALOR de un parámetro de categoría `ejecucion`: `feedback apply` lo rechaza (`feedback/aplicar.py:187`: «solo se cambia por decision (ADR)») | **PARADA b.3** |
| S-5 | A-30, A-39 | la orden sin llenar se quita a las 11 y a las 3; si a las 11 cambia el sesgo de H4, también se quita (51:45–56:18; `ev-v10-005427-1a0867af`, `ev-v10-005603-6a62fca7`) | `orden_pendiente_al_abrir_sesion` = `se_retira`, DEFAULT_AMBIGUOUS (ambiguedad_id A-30); A-30 y A-39 llevan `parametros: []` | sí; **pregunta dirigida** (§3.6, A8) | «un minuto antes» es frase del consultor: no se fija | solo spec, más el docstring de `motor.py:4-6`, que ya no es verdad (§0.c) | activar |
| S-6 | ADR-0061 §2 | hacia fuera, «un pip» varias veces y, con la cuenta hecha, «un punto» (56:21–61:52; `ev-v10-005847-b4097030`, `ev-v10-010110-8d6830a9`) | `stop_fraccion_redondeo` = `alejandose_de_la_entrada`, CONFIRMED; el punto es la decisión nocturna de ADR-0061 §2 | sí | n/a | nada que cambiar: la spec ya dice un punto hacia fuera | sesión 5 solo si el consultor quiere oírlo sin corrección |
| S-22 | A-36 | exactamente en el 0 contando la mecha, siempre; sin tener en cuenta el spread (61:54–62:54; `ev-v10-010214-23a7fc0c`, `ev-v10-010228-868271ee`) | sin parámetro; **REOPEN activo** `fb-2026-09-29-sesion-03-f3caeb2d` (cadena 626c4dc7 ← a0b61bc9 ← f3caeb2d) | sí; la pregunta decía «orden límite» y la entrada es stop (A-47) | n/a | solo spec; el motor ya lo hace (§0.c); C6 queda sin explicar | activar, con `--supersede f3caeb2d` |
| S-8 | A-51 | un break even no corta la racha; tras la novena vuelve al día siguiente; la racha sigue de un día a otro y de una semana a otra (65:32–68:18; `ev-v10-010653-81316808`, `ev-v10-010715-fae17215`, `ev-v10-010804-5b6ad1a3`) | **sin parámetro**; `perdida_trader_*` UNKNOWN (A-44) | sí (regla con un ejemplo) | n/a | parámetros nuevos, regla nueva y código (`tope_trader.py` no tiene ningún acumulador de racha) | **PARADA** (parámetro, §0.c) → código |
| S-9 | A-44 | 9 seguidas y 4,5 % del día se complementan; el 9 % semanal «es un error» y luego «no recuerdo» (68:18–70:44) | `perdida_maxima_diaria` = 4,5 y `perdida_maxima_semanal` = 9, CONFIRMED (sesión 1); `perdida_trader_*` UNKNOWN | sí, con dudas | n/a | contradice un CONFIRMED (b.5); el motor sigue sin correr sin `--diagnostico-a44` | sesión 5 |
| S-10 | A-21 | limpia = sin velas verdes y rojas alternándose antes de la ruptura del posible punto de breaker, y solo eso; el número de velas del retroceso no importa (70:47–81:49; `ev-v10-011725-3741e266`, `ev-v10-011734-fedd3f8e`, `ev-v10-011957-7ebb3453`) | `zona_control_limpia` UNKNOWN, opciones `solo_una_zona_de_control` y `sin_mecha_mas_alla_del_extremo` (`parametros.yaml:877-896`) | sí (regla, compra y venta) | n/a | **es una tercera lectura**: `ACTIVAR-A35-A44.md` §6 manda PARAR y la opción nueva la decide el consultor; código en `domain/estructura_m1.py` + `LECTURAS_LIMPIA`; `--diagnostico-a21` | **PARADA** (§0.c) → código |
| S-11 | A-35 | una superación del alto de M15 con mecha no cuenta; con cuerpo, el alto se actualiza; «sigo usando el mismo alto» solo se deduce (81:49–85:40) | `liquidez_m15_pivote_formado` UNKNOWN | sí, esquema inventado | n/a | la pregunta de A-35 (cuándo está formado) sigue sin respuesta literal | sesión 5 |
| S-12 | A-33 | nunca deja correr; el objetivo es fijo, 3 respecto al 1 de la caja; lo de los primeros vídeos queda de lado «por ahora» (85:40–89:21; `ev-v10-012704-d3facd31`, `ev-v10-012902-257afe4b`) | `parciales` = no, `objetivo_rr` = 3, `base_calculo_objetivo` = `caja_completa`, CONFIRMED | sí | n/a | solo spec (RN-015 ya lo hace); **la pregunta de A-33 son las ganadoras del material por debajo de 3R, que esta respuesta no explica**; choca con ADR-0040 | **PARADA b.1** |
| S-13 | ADR-0060 §2 | una H4 neutra, sin color, mantiene el sesgo que había; con 1 o 2 puntos de cuerpo ya cuenta su color (89:29–101:49; `ev-v10-014005-7e2228f4`, `ev-v10-014040-fb7a153b`) | sin parámetro; `domain/sesgo.py:88-91` devuelve AMBIGUO y RN-033 prohíbe | sí; dicho solo con sesgo previo alcista | n/a | ADR (enmienda de ADR-0060 §2), CORRECT sobre RN-003, RN-033 y el token `ambiguo`, código y tests | **PARADA b.2** → código |
| S-14 | RN-007 | la vela que abre y cierra en el mismo precio no cuenta; sobre 1 o 2 puntos, dos versiones; el literal de 104:49 es «12» (101:49–105:50; `ev-v10-014310-2296423b`, `ev-v10-014438-95464201`, confianza baja) | sin parámetro de umbral; RN-007 DESALINEADA con el motor (`strategy_spec.yaml:1187-1188`) | sí | n/a | el umbral; y oír el minuto (§0.d) | sesión 5 (y Aleks, §0.d) |
| S-15 | A-43 | una liquidez tomada antes de las 7 sí la usa, siempre que la operación se dé desde las 7; la segunda parte (6:45 y 7:20) no la elige (105:51–108:05; `ev-v10-014613-6cf002b2`, `ev-v10-014705-718c5f4e`) | `toma_antes_de_la_ventana` = `no_cuenta`, DEFAULT_AMBIGUOUS (A-43); A-43 lleva `parametros: []` | sí | horas del trader, en su gráfico (ADR-0069) | **lo firme contradice el valor PROVISIONAL**: `no_cuenta` es lo contrario de lo que dijo | sesión 5; decisión sobre lo firme (§0.c) |
| S-16 | E-1 | vale el backtest de agosto del vídeo, «grabado en vivo», porque incluye los break even; el primero no (108:05–109:08; `ev-v10-014823-64248489`, `ev-v10-014853-76602fb4`) | no es ambigüedad; recuento en b.4 | **no**: al revés de `PREGUNTAS.md` 16 | n/a | decisión sobre el material (b.4) | **PARADA b.4**; nada cambia aquí |
| S-17 | A-50 | no descarta la entrada si la caja queda «a nivel» del nivel tomado; con «creo» y sobre pregunta reformulada (109:10–110:19; `ev-v10-015003-dd8ab1bf`, confianza baja) | sin parámetro; el motor mira solo el 0 (`zonas.py`, `se_desarrolla_en_el_lado_de_ruido`) | reformulada | n/a | «creo»; confirmación débil de v9 0:51:08 | sesión 5 |
| S-18 | A-25 | la toma de otra liquidez reinicia los tres intentos; la marca del alto viejo se descarta y pasa al nuevo; él «se iría por una cuarta» pero lo deja en 3 (110:26–114:36; `ev-v10-015152-6dad6eb3`, `ev-v10-015227-b360ebf1`, `ev-v10-015421-44b43053`) | `cartuchos_reinicio` = `siguiente_liquidez_m15` CONFIRMED; `intentos_tras_toma_nueva` = `vuelven_a_cartuchos_max`, DEFAULT_AMBIGUOUS (A-25) **y no está en la lista de A-25**; la marca al pivote más reciente es ADR-0045 (A-24 DECIDIDA) | sí | n/a | solo spec: confirmar `intentos_tras_toma_nueva` con el mismo valor | activar |
| S-20 | A-52 | sin máximo de escenarios: toma todo lo que haya en la sesión cumpliendo los criterios, hasta el tope de pérdida (114:37–116:45; `ev-v10-015449-8a41513d`, `ev-v10-015640-d35c5552`) | `max_escenarios_por_sesion` = `sin_limite`, DEFAULT_AMBIGUOUS (A-52) | sí | n/a | solo spec, mismo valor; la cita de 116:20 empieza un segundo después del tramo 1:56:07–1:56:19: se cita solo `ev-v10-015640-d35c5552` | activar |
| S-21 | A-53 | la deja y la mueve cuando aparece el punto de la liquidez nueva; si se llena la vieja, vale; pero dice «La A es verdadera» (116:55–121:23) | `orden_pendiente_al_abrir_escenario` = `se_mueve`, DEFAULT_AMBIGUOUS (A-53) | sí | n/a | contradicción interna | sesión 5 |
| S-23 | A-32 | en M15 una toma con mecha invalida; en M1 la mecha cuenta (121:25–123:43) | `breaker_m1_criterio_ruptura` = mecha, `liquidez_m15_criterio_toma` = cuerpo, CONFIRMED | la regla sí; la línea de v4 0:53:10 no | n/a | la pregunta concreta de A-32 | sesión 5 |
| S-24 | A-13 | el stop exactamente en la entrada; en su ejemplo espera a que la vela cierre más allá del nivel, «mejor con cuerpo» (123:45–126:42; `ev-v10-020410-e06f9581`, `ev-v10-020453-2d41dd25`, `ev-v10-020520-7bdf02b3`) | `break_even_criterio_ruptura` = mecha CONFIRMED; `break_even_condicion` = tocar; ADR-0065 al tick | sí | n/a | contradice un CONFIRMED y ADR-0065 (b.5) | sesión 5 |
| S-19 | marzo | las 7 capturas son estadísticas («stats», cuántas operativas al día) (126:42–127:29; `ev-v10-020715-7852af76`) | n/a | sí | n/a | nada: `CLAUDE.md` ya dice que no se abren (agregados) | nada que activar |

**Cuadre con el encargo:** 17 ambigüedades ABIERTA con respuesta (las 18 de la tabla menos A-42);
solo «resuelve»: A-18, A-21, A-25, A-30, A-33, A-36, A-39, A-51, A-52; mezclada: A-49; solo «en
parte»: A-13, A-32, A-35, A-43, A-44, A-50, A-53. **Coincide con el cuadre del consultor.** El
recuento de la tabla (13 resuelve, 11 en parte) incluye S-7, S-13, S-16 y S-19, que no son
ambigüedades ABIERTA.

**Lo que hace hoy el motor, por respuesta, y el test que lo probaría:**

| Código | Qué hace hoy el motor (fichero:línea) | Cierre | Test que fallaría en `main` |
|---|---|---|---|
| S-3 / S-12 | el stop va en la orden a `stop_fraccion_caja` redondeado hacia fuera (`primitivas_broker.py`, `escribir_stop_en_la_orden`; RN-011); el objetivo sobre la caja entera (RN-015); `parciales` no | solo spec | ninguno de motor: nada cambia |
| S-4 | `zona_del_punto` (`zonas.py:364-410`): con `al_verse_el_punto` la caja se liga una vez; con `en_cada_cierre_m1` recalcula el extremo R6 en cada cierre y cada 1 nuevo es una zona nueva que RN-006 reubica | valor del parámetro (decisión) | un test que lea el registro y exija `en_cada_cierre_m1` (en `main` da `al_verse_el_punto`); el mecanismo ya tiene tests (F35) |
| S-5 | RN-035 retira la orden al abrir la sesión siguiente (`primitivas_broker.py:540-552`, `se_retira`); a `ventana_fin` no hay regla: el cableado cancela lo pendiente al terminar el día (`cableado.py:229-236`, ADR-0053 §6); RN-002 solo cierra posiciones (`strategy_spec.yaml:858`) | solo spec (si se acepta que la retirada a las 3 siga en el cableado); con regla, código | `tests/unit/test_spec_fidelidad.py:214-226` congela DEFAULT_AMBIGUOUS/A-30: cambia de sentido; un test nuevo que exija CONFIRMED y A-30/A-39 RESUELTA |
| S-22 | el 0 es `punto.nivel`, el extremo con mecha del pivote de M1 (`estructura_m1.py:207-211`); la STOP se coloca en `z.entrada` sin desplazamiento ni spread (`primitivas_broker.py`, `colocar`; `broker.py:370-371`: la venta stop salta al tocar el bid, la compra al tocar el ask) | solo spec; **no falta código**, al revés de lo que dice R1.1 | ninguno falla en `main`: un test nuevo que fije «precio de la orden = nivel del pivote con mecha» pasa ya hoy; se escribe para congelarlo |
| S-8 | RN-020 solo lee `perdida_dia` y `perdida_semana` (`tope_trader.py:249-280`); sin `perdida_trader_alcance` el motor se niega salvo `--diagnostico-a44` | código: acumulador `racha_perdidas`, regla nueva, parámetros | un test sintético: nueve cierres con stop seguidos (con un break even en medio) prohíben abrir hasta el día siguiente; en `main`, `acumulador desconocido` |
| S-10 | `detectar_esquema` (`estructura_m1.py:295-350`) solo conoce dos lecturas (`:65`); `lectura_limpia` (`zonas.py:140-170`) se niega sin valor y rechaza `--diagnostico-a21` con valor fijado | código: opción nueva + función de alternancia; retirar o no `--diagnostico-a21` | `detectar_esquema(..., limpia="sin_alternancia_de_colores")`: en `main`, `EstructuraError`; `tests/unit/test_preparar_a21.py:369-417`, `test_visor.py` y `test_preparar_a35.py` corren con `--diagnostico-a21` y cambian de sentido |
| S-13 | `sesgo_h4` (`domain/sesgo.py:80-95`): doble ruptura sin cuerpo → AMBIGUO; RN-033 prohíbe | ADR + código + spec | `tests/unit/test_sesgo_h4.py:80-84` (`test_doble_ruptura_sin_cuerpo_es_ambiguo`) cambia de sentido; el nuevo exige el sesgo de la vela anterior |
| S-18 / S-20 | `abrir_escenario` (`zonas.py:270-312`) lee `intentos_tras_toma_nueva` y `max_escenarios_por_sesion` | solo spec, mismo valor | ninguno de motor; un test que exija CONFIRMED (en `main`, DEFAULT_AMBIGUOUS) |

### 0.b Lo que choca, medido

**b.1 A-18 (S-3) y A-33 (S-12) frente a ADR-0040.** ADR-0040 (ACTIVE, `docs/adr/0040-*.md:11-44`)
declara REFUTADA la combinación `(caja_completa, 0,8)` con tres meses: la región `[3,00, 3,75)` del
RR implícito tenía que estar vacía y está poblada (agosto 15 de 18, abril 7 de 15, mayo 4 de 5). Su
decisión 4 no cambia ningún parámetro: los dos siguen CONFIRMED «y se sabe que no pueden ser ciertos
los dos a la vez». El trader, en S-3, dice exactamente esa combinación, por tercera vez (sesión 3:
`fb-2026-09-29-sesion-03-f572f1a0`, `-d62c788a`; v7 0:06:07). **No se vuelve a medir nada: se cita.**
Qué cambia si se cierra A-18 hoy: solo la ambigüedad (ningún valor: los cuatro parámetros ya están
CONFIRMED con lo que dijo), y con ella HER:15, la deuda «F26 no puede puntuar el objetivo hasta que
A-18 esté cerrada» (`PROJECT_STATE.md:128`), la G y R5.1. Qué NO cambia: ADR-0040 sigue siendo un
hecho medido del material, y F26 tiene que leer la diferencia 3,00 frente a 3,75 como conocida
(ADR-0040 §Impacto). Y A-33: su pregunta de hoy («¿alguna vez cierras una ganadora antes del
objetivo?») queda contestada -nunca-, pero su título y su historia son las ganadoras del material por
debajo de 3R, que «es fijo» no explica. Opciones del ADR, en §«Lo que necesito que decidas», 0.

**b.2 S-13 frente a ADR-0060 §2.** ADR-0060 §2 es una DECISIÓN NOCTURNA: la doble ruptura de una
vela sin cuerpo sigue en `ambiguo` «porque el trader no describió ese caso», y deja la pregunta para
la sesión 4. El trader la contesta: la neutra «mantiene el sesgo que había», que es la alternativa 1
que ADR-0060 descartó («seguir buscando hacia atrás, como si esa vela no hubiera roto nada»). Hace
falta: (1) un ADR que enmiende ADR-0060 §2 (una DECIDIDA solo la cambia otro ADR; y aquí no hay
ambigüedad, hay una decisión nocturna); (2) spec: `entonces` y notas de RN-003 («solo si cierra sin
cuerpo el sesgo es AMBIGUO», `strategy_spec.yaml:921-923`), notas de RN-033 (`:994-996`), la
descripción del token `ambiguo` y de `sesgo_h4_al_abrir`, con un CORRECT sobre RN-003 citando
`ev-v10-014005-7e2228f4`; `spec_version` sube a MAYOR (RN-003 cambia lo que el motor hace, como en
ADR-0060); (3) motor: `domain/sesgo.py:88-91`, la rama `return ResultadoSesgo(Sesgo.AMBIGUO, ...)`
pasa a `continue` (la vela neutra no decide y la búsqueda sigue hacia atrás; `doble_ruptura` queda
en falso o se anota aparte); `ambiguo` deja de producirse y RN-033 queda solo para `insuficiente`;
(4) tests: `test_sesgo_h4.py:80-84` y `test_huecos_motor.py:79-110` cambian de sentido a propósito, y
uno nuevo con dos neutras seguidas. Medido en ADR-0060 §Impacto: en construcción no hay ninguna doble
ruptura sin cuerpo, así que el cambio no mueve ninguna cifra hoy. Reservas: lo dijo con sesgo previo
alcista y «suponiendo que no haya otro rango mayor»; el caso bajista es simétrico por construcción
del código, no por su frase. **Sobre S-14:** «con 1 o 2 puntos ya cuenta su color» es la vela H4
del sesgo; RN-007 (S-14) es la M1 del mapeo de estructura. Son dos velas y dos reglas distintas y no
comparten umbral: S-13 dice que en H4 no hay «casi plana» (cualquier cuerpo da color, que es lo que
`sesgo.py:88-89` ya hace con cierre ≠ apertura); S-14 pregunta cuánto cuerpo hace que una M1 no cuente
para trazar un punto. S-13 no toca el umbral de S-14.

**b.3 S-4 frente a `caja_se_fija` (ADR-0064 decisión 5).** La decisión 5 fija la caja la primera vez
que se ve el punto; su sensibilidad `en_cada_cierre_m1` (ADR-0064 §5) la pidió el consultor y existe
en el motor (`zonas.py:395-399`): el 1 se recalcula con R6 en cada cierre hasta el llenado, y cada 1
nuevo reubica la orden con su stop y su lote (RN-006). Es lo que S-4 describe («lo vamos actualizando
la caja mientras no se desarrolle otro punto breaker»; que el stop y el lote se recalculen con el 1
lo dijo en S-3, 37:27). Tres cosas medidas: (1) `caja_se_fija` es de categoría `ejecucion` con fuente
`decision: ADR-0064`: `feedback apply` rechaza cambiarlo («es de categoria ejecucion y solo se cambia
por decision (ADR)», `feedback/aplicar.py:187-189`), así que el valor se cambia a mano con fuente
`decision` y el testimonio se registra aparte; (2) el 1 que calcula R6 es «la máxima de las velas desde
el pivote hasta la última cerrada», que coincide con «el máximo nuevo» de S-4 mientras `caja_bloque` =
`r6` (DEFAULT_AMBIGUOUS bajo A-48, sin respuesta en la sesión 4); (3) A-49 pregunta otra cosa
(cerrada o en formación), que S-1 y S-2 dejan «en parte». Cómo queda A-49: **ABIERTA entera**, y S-4
activado aparte sobre `caja_se_fija`, o nada hasta la sesión 5 (decisión 2).

**b.4 S-16 (E-1), por recuento.** `libros.yaml` tiene UNA entrada de agosto, el xlsx
`backtesting-analytics AGOSTO 2026.xlsx` (sha `33a01f1d…`, declarado el 2026-09-22). Los 19 casos
`dev` de agosto (`git ls-files knowledge/cases/dev/caso-eurusd-2026-08-*.yaml | wc -l` = 19) salen
TODOS de ese libro (`grep -l 33a01f1d… | wc -l` = 19). El backtest en vídeo (v7 + v8) cubre 13 días
del 3 al 19 de agosto (`HOLDOUT-EXPOSICIONES.md`, filas del 2026-09-27); de los 19 casos, 11 son de
días del 3 al 19 y 8 de días del 20 al 31, que el vídeo no cubre; y hay 2 días del vídeo sin caso
`dev` del xlsx. En el corpus no hay exportación xlsx del backtest en vídeo (`fuentes.yaml:120`: una
sola exportación de agosto). La spec no cita el libro de agosto en ninguna regla ni parámetro; lo
citan comentarios de A-18 y A-33 en `ambiguedades.yaml` (las medidas de ADR-0037 y ADR-0040) y la
fila «agosto» de ADR-0040: sin ella, la refutación sigue en pie con abril y mayo. **Qué cambiaría si
se decide que vale el del vídeo:** `libros.yaml` ganaría una entrada (solo añadir, ADR-0039 §3) cuando
exista su exportación; los 19 casos `dev` de agosto se reconstruirían desde ella (los 8 de días
posteriores al 19 quedarían sin fuente), en una rama propia con `knowledge/cases/` y
`knowledge/corpus/` permitidos (aquí están protegidos); ADR-0040 ganaría un recuadro. **Nada cambia
sin decisión**, y nada de esto cabe en esta rama. Matiz del auditor: en v9 el trader dijo «el último
que fue el backtest completo» y la hoja dio por hecho cuál era el último; la sesión 3 ya dejó E-1
como «no resuelve: ¿el último o el completo?».

**b.5 Las «en parte» que contradicen un CONFIRMED.** (1) **S-24 frente a `break_even_criterio_ruptura`
= `mecha` (CONFIRMED, `fb-2026-09-29-sesion-03-2cff5008`) y ADR-0065** (al tick): en v10 espera a que
la M1 cierre más allá del nivel y «con cuerpo mucho mejor», contra el «apenas toca» de v6 0:57:01 y
v9 0:55:43. Ninguna de las dos fuentes se pisa: queda escrita para la sesión 5 (§0.e), con la nota en
el informe. (2) **S-9 frente a `perdida_maxima_semanal` = 9 (CONFIRMED,
`fb-2026-09-09-sesion-01-a85b6bc7`)**: «es un error» y después «no recuerdo muy bien»; el 4,5 % del
día se confirma. No se corrige por feedback: una retractación dudosa no es un CORRECT. A la sesión 5.

### 0.c Detalles que el repo ya pide

- **A-36.** `feedback trace A-36`: `fb-…-626c4dc7` (RESOLVE_UNKNOWN, superseded) ← `fb-…-a0b61bc9`
  (RESOLVE_UNKNOWN «sin resolver», superseded) ← **`fb-2026-09-29-sesion-03-f3caeb2d` (REOPEN,
  activo)**. El cierre es un RESOLVE_UNKNOWN nuevo con `--supersede fb-2026-09-29-sesion-03-f3caeb2d`
  (`AMBIGUEDADES.md`, «Volver a cerrarla»). Su título y su pregunta dicen «orden límite»; desde A-47
  la entrada es STOP (`entrada_tipo_orden` = `stop_en_ruptura`). El trader respondió sobre la orden
  de entrada tal como la pone hoy (S-22, «la orden va en… cero… me echa del cero de la caja»): la
  respuesta vale para la orden stop. El motor ya la pone ahí: el 0 de la caja es `punto.nivel`, el
  extremo CON MECHA del último pivote de M1 (`estructura_m1.py:207-211`), y la orden se coloca en ese
  precio sin sumar spread (`broker.py:370-371`: la stop salta al tocar el bid o el ask). C6 (v7 n.º 3,
  la orden 2 puntos más allá del 0) queda sin explicar, como dice la extracción.
- **A-21.** `zona_control_limpia` es UNKNOWN con dos opciones (`parametros.yaml:877-896`), que son
  `LECTURAS_LIMPIA` de `domain/estructura_m1.py:65` (no de `engine/`), consumidas en
  `detectar_esquema` (`:295-350`), `zonas.py:140-170` (`lectura_limpia`) y `:441`, `diagnostico.py:75`
  y `cli.py:2300`. La respuesta -sin alternancia de colores antes de la ruptura, y el número de velas
  del retroceso no importa- es la lectura candidata ya anotada en la pregunta desde la sesión 3, y es
  una TERCERA opción: `ACTIVAR-A35-A44.md` §6 manda PARAR y dice que añadir una opción al enum y su
  mecanismo es decisión del consultor. Propuesta: `sin_alternancia_de_colores`, definida sobre las M1
  del retroceso (desde el fin del bloque de origen hasta la vela que rompe la referencia, excluida):
  la zona está limpia si en ese tramo no hay cambio de color de una vela a la siguiente; con el
  esquema 1 (sin retroceso) está limpia siempre. Hay una segunda lectura posible de «alternándose»
  (más de un cambio de color), que se lleva a la PARADA. **`--diagnostico-a21`**: con el valor fijado,
  `lectura_limpia` lo rechaza siempre («ya esta fijado… no admite --diagnostico-a21», `zonas.py:150-155`),
  así que la opción solo puede dar error. La corrida de R3.1 no se ve afectada por retirarla
  (`OPCIONES_QUE_NO_CAMBIAN_LA_CORRIDA` es otra lista, ADR-0070 §3). Precedente de dejarla:
  `--diagnostico-a47` sigue en `cli.py:2314` con A-47 RESUELTA. La usan hoy `test_preparar_a21.py`,
  `test_visor.py` y `test_preparar_a35.py`, que cambian de sentido al fijar el valor. Propuesta:
  retirarla (y `Diagnostico.a21`) en el commit de A-21. **Cerrar A-21 no habilita R3.1**: A-35 y A-44
  siguen pidiendo diagnóstico (ADR-0070 §3; `HOJA-DE-RUTA.md:86-88`).
- **A-51, el parámetro que no tiene.** Propuesta, con nombres y valores, todo bajo RN-020 o una regla
  hermana (RN-036) y con la racha contando los MISMOS cierres que RN-016 cuenta como pérdida
  (`cartucho_criterio`), para no inventar qué es «una pérdida»:
  - `racha_perdidas_max` (entero, CONFIRMED, 9; cita `ev-v10-010653-81316808`, y ya en la sesión 3
    `ev-v9-011128-a267338b`): pérdidas seguidas que detienen la operativa;
  - `racha_perdidas_corte` (enum `[ganadora, ganadora_o_break_even]`, CONFIRMED `ganadora`;
    `ev-v10-010715-fae17215`): qué cierre vuelve la racha a cero. El trader dijo que el break even no
    la corta; que la ganadora la corta es la definición de «seguidas» y se dice así en la descripción;
  - `racha_perdidas_reinicio` (enum `[nunca, fin_de_dia, fin_de_semana]`, CONFIRMED `nunca`;
    `ev-v10-010804-5b6ad1a3`): la racha sigue de un día a otro y de una semana a otra;
  - `racha_perdidas_reanudacion` (enum `[dia_siguiente, semana_siguiente, sin_fecha]`, CONFIRMED
    `dia_siguiente`; `ev-v10-010804-5b6ad1a3`): cuándo vuelve a operar tras la novena.
  Código: un acumulador `racha_perdidas` que persiste entre días (hoy `EstadoDia` nace cada día de
  cero, ADR-0053 §6: el acumulador vive en el cableado o en la cuenta, como `SeguidorTope`), un hecho
  `detenido_por_racha` hasta el corte diario siguiente, y la forma de la regla con `alcanza_tope`.
  **No desbloquea RN-020**: `perdida_trader_alcance` sigue UNKNOWN (A-44 «en parte») y el motor sigue
  negándose sin `--diagnostico-a44`. Un parámetro `ejecucion` no vale aquí: son cifras del trader.
- **A-30 y A-39.** `ambiguedades.yaml:767` trae `parametros: []` en A-30 y `:1050` en A-39, pero
  `orden_pendiente_al_abrir_sesion` lleva `ambiguedad_id: A-30` (`parametros.yaml:771-790`): la lista
  de A-30 gana ese parámetro, y la de A-39 también (es el mismo mecanismo). RN-002 (`strategy_spec.yaml:858`)
  dice «LO QUE NO HACE: retirar la orden pendiente al vencer la vela; A-39 … sigue ABIERTA … (A-30)»:
  esa nota se reescribe. El docstring de `engine/motor.py:4-6` («aqui no se cierra ni se retira nada
  al cambiar de sesion», PROVISIONAL) ya no es verdad desde RN-035 (`primitivas_broker.py:540-552`):
  se corrige en el mismo commit (comentario, sin cambio de comportamiento). Lo que S-5 dice de «las 3»:
  hoy la orden pendiente a `ventana_fin` la cancela el cableado al terminar el día
  (`cableado.py:229-236`, ADR-0053 §6), sin regla de la spec. Cerrar A-30 solo por spec deja esa
  retirada como comportamiento del cableado; si el consultor quiere que la spec lo diga, RN-035 gana
  una segunda rama (`vence_vela_h4` / `alcanza_hora ventana_fin` → `retirar_orden_limite`) y es código
  con test (decisión 4).
- **La hoja de preguntas.** `ORDEN_SESION_02` (`scripts/hoja_preguntas.py:53-59`) lleva A-35, A-21,
  A-44, A-43, A-24, A-25, A-32, A-36, A-30, A-48, A-49, A-18, A-13, A-33 y A-39; **no lleva A-51 ni
  A-52**. El quinto sitio de `AMBIGUEDADES.md` es «la hoja se niega a llevar al trader una ambigüedad
  que ya no esté ABIERTA ni DECIDIDA»: para A-51 y A-52 no hay nada que quitar, y se dice en el
  informe; para A-25, A-30, A-36, A-39 (y A-18, A-21, A-33 si se cierran) se quitan de
  `ORDEN_SESION_02` y de `ORDEN` en `tests/unit/test_hoja_preguntas.py:19-29`.
- **Quién espera cada ambigüedad** (`grep -rn "A-n" CLAUDE.md docs/runbooks PROJECT_STATE.md
  docs/plan/HOJA-DE-RUTA.md`): `CLAUDE.md`, ninguna. `PROJECT_STATE.md`: E (las 17), HER:15 y HER:37
  (A-18), HER:25 y HER:30 (A-35, y A-21 en el texto de 25), HER:35 (A-44), Technical Debt `:127-128`
  (A-18), la tabla de Known Ambiguities (todas). `HOJA-DE-RUTA.md`: R1.1 (las 17 y RN-007), R3.1 (A-21,
  A-35, A-44), R4.1 (A-13, A-21, A-32, A-35, A-43, A-44, A-49, A-50, A-53), R5.1 (A-18). Runbooks:
  `ACTIVAR-A35-A44.md` (A-21, A-35, A-44) y `ERRORES-RECURRENTES.md:56` (A-36, histórico). **R4.1 no
  lleva A-18, A-25, A-30, A-33, A-36, A-39, A-51 ni A-52**: si alguna de las «resuelve» no cierra aquí,
  hay que decir adónde va su `ID:` (el test (d) exige que una respondida ABIERTA esté en R1 o R4).

### 0.d Herencias

- **Heredado 15** (A-18, `PROJECT_STATE.md:71`): sale solo si A-18 se cierra (decisión 0). Si no,
  se queda con su texto.
- **Heredado 37** (volumen máximo, «con A-18», `:77`): lo decide la respuesta de FTMO a P-D1 (O,
  A.2 de la hoja de ruta). **Queda fuera de esta rama**, cierre A-18 o no: su «con A-18» era de la
  rama de stop y lote, y el máximo de 50 lotes (ADR-0071 §2) no depende de la base del objetivo.
- **H (RN-007, S-14) y el punto 3 de la orden de cierre de `trabajo/sesion-04`.** El tramo personal de
  v10 va de 1:43:42 a 1:44:21 (`tramos_no_citables.yaml`); el ítem `ev-v10-014438-95464201` empieza
  en 1:44:38, 17 s después, y acaba en 1:45:04; el otro, `ev-v10-014310-2296423b`, va de 1:43:10 a
  1:43:31, 11 s antes del tramo. Ninguno pisa un tramo ni su segundo de margen; `evidence new` los
  aceptó y `knowledge validate` los cruza. **Lo que no pude medir: la CLI filtrada.** La guardia niega
  `botsito corpus transcript show --video v10` desde la sesión (`guardia.py:1866-1878`: v10 está en
  cuarentena y la CLI «imprime la transcripcion cruda»); no se rodea. Propuesta: que Aleks escuche
  ese minuto o lo lea con la CLI filtrada en su terminal, con este comando, y diga si a 1:44:49 el
  trader dice «1 o 2» o «12»:

  ```
  uv run botsito corpus transcript show --video v10 --t0 1:44:38 --t1 1:45:04 --margen-s 10
  ```

  Si dice «1 o 2», la contradicción con 1:43:17 es real y S-14 va a la sesión 5 con las dos versiones;
  si dice «12», no hay contradicción, pero el umbral sigue dicho «entre comillas» y «todas están
  correctas», así que la pregunta va igual a la sesión 5 y H se queda. **S-13 no toca el umbral de
  S-14** (b.2).
- **§4 de la extracción, sus once puntos:** 1 (break even, S-24) → b.5 y sesión 5; 2 (casi plana,
  S-14) → §0.d, Aleks y sesión 5; 3 (backtest de agosto, S-16) → b.4; 4 (S-4 contra `caja_se_fija`)
  → b.3; 5 (S-21, «La A es verdadera») → sesión 5; 6 (S-6, un pip y un punto) → nada cambia, sesión 5
  solo si el consultor quiere; 7 (S-9, el 9 % semanal) → b.5 y sesión 5; 8 (las 9 pérdidas vienen del
  0,5 % y podría extenderlas con menos riesgo) → para el consultor, no es regla: se anota en A-51 al
  cerrarla; 9 (junio y la cuarentena mecánica) → HECHO en `trabajo/cuarentena-por-condicion`
  (`meses_reservados.yaml`); 10 (la guardia y el guion nuevo) → HECHO en `trabajo/filtradas-escenario-b`
  y `trabajo/filtradas-con-tramos`; 11 (S-7 en el reloj del trader) → HECHO en `trabajo/activacion-a42`
  (ADR-0069).
- **Candidatas de `DISENO-ENTRADA-RUPTURA.md` §2.8:** C1 (orden pendiente cuando aparece una caja
  nueva): la tocan S-4 (el 1 se expande con la orden puesta) y S-21 (en parte); con S-4 activado, la
  orden se reubica con cada 1 nuevo, que es lo que C1 vio en v7 n.º 2; C1 no se abre. C4 (el stop en
  dos tiempos): la cierra S-3, «se usa el 1 al comienzo pero no de ejecución, sino como planteamiento»:
  no hay dos tiempos en la ejecución; la orden sin stop de v8 n.º 1 queda sin explicar. C6 (la orden
  2 puntos más allá del 0): S-22 dice exactamente en el 0, siempre; C6 sigue sin explicar y se deja
  anotada. También las toca la sesión 4, aunque el encargo no las nombra (auditor): C7 (cuánto vive una
  orden stop sin llenar): S-5 (hasta las 11 o las 3) y S-21 (hasta el punto de la liquidez nueva);
  C5 (la caja antes de la toma): nadie la toca.
- **Sesión 3, §5:** queda UNA con «resuelve» y ABIERTA: A-44, «resuelve con lectura NUEVA + abre
  ambigüedad nueva», que PARÓ en la activación (`ACTIVAR-A35-A44.md` §4) y en la sesión 4 es «en parte»
  (S-9). A-42, «resuelve en parte» en la sesión 3, está RESUELTA. El resto de «resuelve» de la sesión 3
  están RESUELTAS (A-26, A-31, A-34, A-37, A-38, A-40, A-41, A-45, A-46, A-47). El parser de
  `test_hoja_de_ruta.py:92-113` cuenta «resuelve en parte» como respondida, igual que «en parte»: para
  el test de «una en parte no entra en RESUELTAS» hace falta distinguirlas.

### 0.e La lista para la sesión 5 (hasta que exista su hoja, R4.1)

Cada «en parte» y cada cosa que no se cierre aquí, con lo que sí quedó claro (sin fijar nada) y la
pregunta cerrada con opciones. En el lenguaje del trader.

1. **A-49 (S-1, S-2).** Claro: la orden va en el punto en cuanto una vela de M1 cierra más allá del
   extremo anterior, con mecha o con cuerpo; la caja se traza con esa vela cerrada. Pregunta: «Cuando
   trazas la caja, ¿esperas siempre a que cierre la vela, o a veces la trazas con la vela todavía
   abierta? (a) siempre con la vela cerrada; (b) a veces con la vela abierta, ¿cuándo?; (c) otra,
   ¿cuál?»
2. **A-13 (S-24).** Claro: el stop va exactamente a la entrada. Dos versiones del disparador: «apenas
   toca» (v6, v9) y «cuando la vela cierra por debajo, mejor con cuerpo» (v10). Pregunta: «Para pasar
   el stop a la entrada, ¿esperas a que la vela de M1 cierre pasado el nivel, o lo haces en cuanto el
   precio lo toca? (a) en cuanto toca; (b) cuando cierra la vela, aunque sea con mecha; (c) cuando
   cierra con cuerpo; (d) otra, ¿cuál?» Y: «Después de ponerlo a la entrada, ¿lo vuelves a mover
   alguna vez? (a) nunca; (b) sí, ¿cuándo?»
3. **A-44 (S-9).** Claro: paras el día con un 4,5 % perdido y vuelves al día siguiente; las 9 seguidas
   y el 4,5 % se complementan. Pregunta: «Del tope de la semana, ¿cuál vale? (a) el 9 % de la semana,
   de lunes a viernes; (b) no hay tope de semana, solo el del día y las 9 seguidas; (c) otra, ¿cuál?»
   Y: «¿El 4,5 % lo mides sobre el saldo con que empezó el día o sobre lo que tienes en ese momento con
   las operaciones abiertas? (a) saldo del inicio del día; (b) con las abiertas; (c) otra.»
4. **A-35 (S-11).** Claro: una toma con mecha no cuenta; con cuerpo, el alto se actualiza. Pregunta:
   «Cuando el precio supera un alto de M15 solo con la mecha y vuelve, ¿qué alto usas después? (a) el
   mismo de antes; (b) el nuevo, el de la mecha; (c) otra, ¿cuál?» Y la de siempre: «¿En qué momento
   das por formado un alto o un bajo de M15? (a) cuando cierra la vela que lo hace; (b) cuando cierra la
   vela contraria que lo deja atrás; (c) otra, ¿cuál?»
5. **A-43 (S-15).** Claro: una liquidez tomada antes de las 7 sí la usas, si la operación se da desde
   las 7. Pregunta: «Si el precio la toma a las 6:45, vuelve por encima y a las 7:20 la toma otra vez,
   ¿cuál es tu toma? (a) la de las 7:20 también vale; (b) esa liquidez ya está gastada y espero otra;
   (c) otra, ¿cuál?»
6. **A-50 (S-17).** Claro: no filtras la entrada por dónde queda la caja frente al nivel (dicho con
   «creo»). Pregunta, con dos dibujos: «Aquí la caja entera queda al otro lado del nivel tomado; aquí
   el 0 queda de este lado y el 1 del otro. ¿Operas las dos? (a) las dos; (b) solo la primera; (c)
   otra, ¿cuál?»
7. **A-53 (S-21).** Claro: la orden sigue viva hasta que aparece el punto de la liquidez nueva y, si se
   llena mientras, vale. Pregunta: «Con una orden puesta sin llenar, el precio toma otra liquidez de
   M15. (a) la quitas en ese momento; (b) la dejas y la mueves cuando aparezca el punto nuevo, y si se
   llena antes, vale; (c) otra, ¿cuál?» (dijo las dos cosas en la misma frase).
8. **A-32 (S-23).** Claro: en M15 una toma con mecha invalida; en M1 la mecha cuenta. Pregunta, con el
   fotograma de v4 0:53:10 si se autoriza abrirlo: «En este vídeo descartaste la entrada porque el
   precio rompió con mecha esta línea. ¿Qué era esa línea? (a) la liquidez de M15; (b) un nivel de M1;
   (c) no lo recuerdo; (d) otra.»
9. **S-14 (RN-007, H).** Claro: la vela que abre y cierra en el mismo precio no cuenta. Pregunta:
   «Una vela de M1 con un cuerpo de 1 o 2 puntos, ¿la usas para trazar un punto de breaker? (a) sí,
   cuenta como cualquier otra; (b) no, es casi plana y no cuenta; (c) depende, ¿de qué?» Y: «¿Miras
   el cuerpo o también las mechas?»
10. **S-6 (ADR-0061 §2), solo si el consultor lo quiere:** «Al redondear el stop del 0,8 hacia fuera,
    ¿lo mínimo es un punto (0,1 pip) o un pip entero?»
11. **Lo que no se cierre aquí de las «resuelve»** (según la PARADA): A-18 y A-33 si queda la opción
    (b) de la decisión 0: «Cuando pones el stop en el 0,8, ¿tu objetivo lo mides desde el 0 hasta el 1
    de la caja, o hasta el 0,8? Y en tus backtests, ¿el stop estaba siempre en el 0,8?»; A-21 si no se
    decide la opción nueva: «Para que la zona esté limpia, ¿vale un cambio de color en el retroceso, o
    tienen que ser todas las velas del mismo color? (a) todas del mismo color; (b) un cambio sí, dos
    no; (c) otra.»
12. **Lo nuevo que la sesión 4 destapa, por si el consultor lo quiere en la hoja:** las 9 pérdidas con
    menos riesgo por operación (§4.8); la orden sin stop de v8 n.º 1 (C4) y la orden 2 puntos más allá
    del 0 (C6); «si queda muy lejos el máximo nuevo» (S-4 dijo que da igual).

### 0.f El plan de commits, y por dónde partir

Uno por respuesta activada; primero spec, después motor. Cada uno con los pasos del paso 3 de
`activar-sesion` (registro sobre la ambigüedad con todas las opciones, registros de parámetro,
`feedback apply --sesion 2026-10-04-sesion-04 --check` que proponga solo los suyos, los cinco sitios,
`test_kit.py`, `spec_version`, `spec manifest --escribir` y `spec docs --escribir`, `knowledge validate`,
`Fuente:` con los `fb-*` nuevos).

| # | Commit | Toca | Riesgo |
|---|---|---|---|
| 1 | fase 0 y PARADA (este) | informe | — |
| 2 | A-52 (S-20): `max_escenarios_por_sesion` → CONFIRMED `sin_limite`; A-52 RESUELTA | spec, test_kit, docs/spec | bajo |
| 3 | A-25 (S-18): `intentos_tras_toma_nueva` → CONFIRMED; `cartuchos_reinicio` confirmado; A-25 RESUELTA; hoja | spec, test_kit, hoja + test | bajo |
| 4 | A-30 y A-39 (S-5): `orden_pendiente_al_abrir_sesion` → CONFIRMED `se_retira`; listas de parámetros; nota de RN-002; docstring de `motor.py`; A-30 y A-39 RESUELTAS; hoja; `test_spec_fidelidad.py:214-226` cambia de sentido | spec, un comentario del motor, tests, hoja | bajo (medio si entra la rama de `ventana_fin` en RN-035) |
| 5 | A-36 (S-22): RESOLVE_UNKNOWN con `--supersede f3caeb2d`; nota a la pregunta (orden stop); test que congela el precio de la orden; hoja | spec, test nuevo, hoja | bajo |
| 6 | S-4 / `caja_se_fija` → `en_cada_cierre_m1`, si se decide; por decisión (recuadro en ADR-0064 §5 o ADR nuevo) y testimonio registrado | spec (`ejecucion`), ADR, test | medio |
| 7 | test «una en parte no entra en RESUELTAS» (tabla final de cada extracción × `ambiguedades.yaml`), demostrado por mutación en el informe | tests | bajo |
| 8 | A-21 (S-10): opción nueva + `detectar_esquema` + retirada de `--diagnostico-a21`; tests que cambian de sentido; A-21 RESUELTA (deja de ser bloqueante); hoja; `spec_version` | motor (domain), cli, spec, tests | alto |
| 9 | S-13: ADR, CORRECT RN-003, `sesgo.py`, RN-033 y token; `spec_version` MAYOR | motor (domain), ADR, spec, tests | alto |
| 10 | A-51 (S-8): ADR, cuatro parámetros, RN-036, acumulador y hecho nuevos; A-51 RESUELTA (deja de ser bloqueante) | motor (engine), ADR, spec, tests | alto |
| 11 | A-18 y A-33 (S-3, S-12), según la decisión 0: ADR y cierres; HER:15 | ADR, spec, hoja | medio |
| 12 | entrega: informe, revisor, CI, líneas para el cierre | informe | — |

**Propuesta de partición.** Los commits 8 a 10 traen tres mecanismos de motor nuevos (zona limpia,
sesgo con neutra, racha de pérdidas), dos o tres ADR y una subida MAYOR de `spec_version`, cada uno
con su `comparar-con-main`; y las «en parte» impiden de todas formas que R1.1 quede HECHA en este
cierre. Recomiendo **partir por el commit 7**: esta rama cierra lo que solo toca spec (2 a 7, y 11 si
la decisión 0 lo permite) y deja en el informe la lista de la sesión 5 y las líneas del cierre; una
segunda rama, `trabajo/activar-sesion-04-motor`, lleva A-21, S-13 y A-51 con sus ADR, con la PARADA
de aquí ya respondida. El coste de no partir: una rama de doce commits con tres ADR y tres cambios de
motor, y un cierre que cambia `spec_version` dos veces.

### 0.g El encargo frente al repo (auditor `auditor-encargo`, 2026-10-11)

50 afirmaciones sustantivas: 38 correctas, 0 incorrectas, 12 con matiz; 12 herencias no recogidas.
Verificado en la sesión lo que cambia el trabajo. Lo que importa:

1. **A-21 no es un «resuelve» que se active sin decisión.** La respuesta es una tercera lectura;
   `ACTIVAR-A35-A44.md` §6 (líneas 218-219 y 272-274) manda PARAR y dice que la opción nueva del enum
   la decide el consultor. El encargo da por hecha «la opción nueva en su enum» y no la pone en «Lo
   que necesito que decidas». Va en la decisión 3. Y cerrar A-21 no habilita R3.1 (A-35 y A-44 siguen
   en diagnóstico).
2. **Las líneas del cierre se quedan cortas.** Si E sale, `test_hoja_de_ruta` rompe por I
   (`PROJECT_STATE.md:41`, «después de X, S y E»), R2.1 y R5.4 (`HOJA-DE-RUTA.md:65` y `:138`,
   «(NA:E)»), y F («E es lo siguiente») deja de ser verdad. R1.1 no puede quedar HECHA mientras sigan
   vivos HER:15 y H ni mientras una «en parte» no esté en la hoja de la sesión 5, que no existe
   (`:57`). Las líneas preparadas al final del informe cubren también I, F, R2.1 y R5.4, y proponen
   cómo queda E (decisión 12).
3. **A-25 tiene un segundo parámetro** (`intentos_tras_toma_nueva`, `ambiguedad_id: A-25`) que su
   lista no trae, y **A-43** tiene `toma_antes_de_la_ventana` con la lista vacía. Se corrigen las
   listas en sus commits (A-25 aquí; A-43 cuando se cierre o en la decisión 9).
4. Matices que no cambian el trabajo: la pregunta de A-33 no es la que S-12 contesta (b.1); «lo que
   dijo en v9» sobre S-16 era ambiguo y la sesión 3 ya lo dejó como «no resuelve» (b.4);
   `LECTURAS_LIMPIA` vive en `domain/`, no en `engine/`; el punto 3 de la orden de cierre deja el
   «12» «para la rama de activación, que lo resolverá con el trader si hace falta», y que Aleks escuche
   el minuto es otra vía, compatible; faltaban C5 y C7 (§0.d); de la sesión 3 sí queda A-44 con
   «resuelve» (§0.d); R4.1 depende de R3.1 y de la copia de seguridad, no solo de J; de las «cuatro
   veces» del listado del holdout el auditor encuentra tres documentadas (`CASES-REJILLA.md:255`,
   `UMBRAL-MAYO.md:253`, `ENTORNO-CODE.md:908`); el `feedback apply --check` del encargo necesita
   `--sesion 2026-10-04-sesion-04` (el contrato lo lleva); hay dos P HECHAS en HISTORIA (`:4078` y
   `:7887`) porque las letras se reutilizan, y el test (b) admite la referencia NA:P de R0.1
   (`test_hoja_de_ruta.py:143-147`: una HECHA registrada en HISTORIA).
5. Herencias que el encargo no recoge y se atienden: los heredados 25, 30 y 35 (RN-004 tras A-35,
   RN-020 tras A-44) no se mueven, porque A-35 y A-44 siguen «en parte» y A-51 no desbloquea RN-020;
   si A-18 cierra, cambian la deuda de `PROJECT_STATE.md:128`, la G y R5.1 (líneas del cierre); la
   pregunta de reserva de A-18 en `V5-INSTANTES.md:95-104` queda superada si A-18 cierra; los
   precedentes `ACTIVAR-SESION-03.md`, `ACTIVACION-A42.md` y `ACTIVAR-A35-A44.md` se siguieron; la
   tabla lleva las columnas de la skill y las del encargo (ganan las de la skill, y el encargo lo
   admite); `knowledge/corpus/` y `knowledge/cases/` están protegidos en el contrato, así que lo de
   S-16 no cabe aquí (b.4).

### 0.h Lo que no pude medir

- La CLI filtrada sobre v10 (§0.d): la guardia la niega desde la sesión. Comando para Aleks arriba.
- Si `knowledge validate` admite un parámetro CONFIRMED colgado de una ambigüedad ABIERTA: no se
  ejecutó nada que escriba. Hay precedente en el repo (`break_even_criterio_ruptura` CONFIRMED con
  A-13 ABIERTA, sesión 3), así que se da por admitido.
- Una guardia bloqueó también un `grep -rln` legítimo sobre `tests/ src/ scripts/ docs/runbooks/
  Makefile` («leer el contenido de .»); se hizo con la herramienta Grep, que es la que corresponde.
  No hace falta corregir la guardia.

## Lo que necesito que decidas

0. **A-18 y A-33 frente a ADR-0040 (b.1).** Opciones: (a) un ADR nuevo, «el testimonio del trader
   fija la spec y la refutación de ADR-0040 queda como hecho medido del material»: A-18 y A-33
   RESUELTAS con sus registros (ningún valor cambia: los cuatro parámetros ya están CONFIRMED con lo
   que dijo), ADR-0040 sigue ACTIVE y F26 lee la diferencia 3,00 frente a 3,75 como conocida; A-33
   anota que las ganadoras del material por debajo de 3R quedan sin explicación del trader; (b)
   ninguna se cierra hasta un material que traiga la caja (ADR-0040 §2), y las dos van a la sesión 5
   con la pregunta de §0.e.11; (c) A-33 RESUELTA (su pregunta está contestada) y A-18 ABIERTA con lo
   firme ya activado. Recomiendo (a): el trader lo ha dicho tres veces, la spec ya corre con esa
   combinación desde la sesión 3 y mantener A-18 abierta no deja ninguna pregunta nueva que hacerle;
   lo que falta es material, no testimonio, y eso lo dice ADR-0040. Coste de (b): HER:15, la deuda de
   `PROJECT_STATE.md:128` y R5.1 siguen colgados de una pregunta ya respondida. Coste de (c): dos
   ambigüedades gemelas con destinos distintos sin un criterio escrito.
1. **S-13 (b.2).** Opciones: (a) ADR que enmiende ADR-0060 §2 (la neutra no decide y se sigue hacia
   atrás), CORRECT sobre RN-003, código y tests, en la rama de motor; (b) a la sesión 5 porque solo lo
   dijo con sesgo alcista. Recomiendo (a): lo dio como regla general («con la única condición de que
   sea una vela neutra») y en construcción no hay ningún caso, así que no mueve ninguna cifra.
2. **S-4 y A-49 (b.3).** Opciones: (a) A-49 sigue ABIERTA (S-1 y S-2 a la sesión 5) y `caja_se_fija`
   pasa a `en_cada_cierre_m1` por decisión -recuadro en ADR-0064 §5 o sección del ADR de esta sesión-
   con el testimonio registrado como feedback sobre A-49 sin cerrarla (CONFIRM/CORRECT no caben:
   `apply` rechaza un parámetro `ejecucion`); (b) nada hasta la sesión 5. Recomiendo (a): el mecanismo
   existe, está medido (`F35-ORDEN-STOP-PIVOTE.md` §4) y el trader lo describió sin dudar. Coste de
   (b): el bot sigue fijando la caja al verse el punto, que es la decisión «más conservadora» y no la
   suya.
3. **A-21, la opción nueva.** Opciones: (a) `sin_alternancia_de_colores`: ningún cambio de color de
   una M1 a la siguiente en el retroceso (desde el fin del bloque de origen hasta la vela que rompe,
   excluida); (b) `sin_alternancia_de_colores` como «no más de un cambio de color»; (c) a la sesión 5
   con la pregunta de §0.e.11. Recomiendo (a): es lo literal de v9 1:19:57 («una vela verde, una vela
   bajista, una vela verde, una bajista») y lo que confirma en v10 77:25-77:46 (una zona se ensucia
   con velas seguidas de colores distintos, «y es solo eso»); (b) admite un dibujo que él llamó sucio. Y: ¿la opción nueva sustituye a las dos de hoy en el enum, o
   se suma? Recomiendo sumarla y dejar las dos como lecturas sin fuente (como `referencia_de_la_toma`).
4. **A-30 y A-39: la retirada a las 3.** Opciones: (a) solo spec: `se_retira` CONFIRMED, listas de
   parámetros, nota de RN-002 y docstring; la retirada a `ventana_fin` sigue siendo el cableado
   (ADR-0053 §6) y se dice en las notas de RN-035; (b) además, RN-035 gana la rama de `ventana_fin`
   (`vence_vela_h4` / `alcanza_hora`) con `retirar_orden_limite`, código y test. Recomiendo (a) en
   esta rama y (b) apuntado para la de motor: el comportamiento ya es el que dijo, y la regla escrita
   es la forma honesta de que la spec lo diga.
5. **A-36.** Opciones: (a) cerrar con `--supersede f3caeb2d`, nota en la pregunta de que la respuesta
   vale para la orden stop (A-47) y título intacto; (b) además cambiar el título a «orden de entrada».
   Recomiendo (a): el título es historia y un test que congele el precio de la orden (= nivel del
   pivote con mecha, sin spread) basta. C6 se queda anotada en las candidatas sin abrir.
6. **A-51, el parámetro.** Opciones: (a) los cuatro de §0.c (`racha_perdidas_max`,
   `racha_perdidas_corte`, `racha_perdidas_reinicio`, `racha_perdidas_reanudacion`), una regla nueva
   RN-036 con `alcanza_tope` sobre un acumulador `racha_perdidas` que cuenta los cierres que RN-016
   cuenta como pérdida, un hecho `detenido_por_racha` hasta el corte diario siguiente, y un ADR; (b)
   solo dos (`racha_perdidas_max` y `racha_perdidas_reanudacion`) con el corte y el reinicio en la
   descripción. Recomiendo (a): que el break even no corte y que la racha cruce días son valores que
   el trader dio y podrían cambiar (ADR-0002). Y: la regla, ¿en RN-020 como tercera rama o en RN-036
   aparte? Recomiendo aparte: RN-020 sigue bloqueada por A-44 y así A-51 se cierra sin tocarla.
7. **`--diagnostico-a21`.** Opciones: (a) retirar la opción de la CLI y `Diagnostico.a21` en el
   commit de A-21, con los tres tests cambiados de sentido; (b) dejarla, como `--diagnostico-a47`.
   Recomiendo (a): con el valor fijado solo puede dar error. Lo mismo valdría para `--diagnostico-a47`,
   que no toca esta rama.
8. **S-14.** Opciones: (a) Aleks escucha o lee el minuto con el comando de §0.d y dice «1 o 2» o «12»;
   en los dos casos la pregunta va a la sesión 5 (§0.e.9) y H se queda; (b) directo a la sesión 5 sin
   oírlo. Recomiendo (a): cuesta un minuto y decide si la hoja lleva una contradicción o una duda.
9. **A-43, lo firme.** Opciones: (a) CORRECT sobre `toma_antes_de_la_ventana` a `cuenta` (registro
   del trader sobre el parámetro, `ev-v10-014613-6cf002b2`), estado CONFIRMED, A-43 ABIERTA por la
   segunda parte (precedente: `break_even_criterio_ruptura` con A-13), y la lista de A-43 gana el
   parámetro; (b) nada hasta la sesión 5. Recomiendo (a): el valor PROVISIONAL de hoy es lo contrario
   de lo que dijo sin dudar, y el motor corre con él.
10. **Las respuestas dadas con «creo», con pregunta dirigida o con un ejemplo sin regla.** S-5 fue una
    pregunta dirigida (§3.6, A8) y lo que la sostiene es la razón del trader a 54:38: ¿basta para
    activar A-30 y A-39? S-13 se dijo solo con sesgo alcista. S-17 lleva «creo» (ya en sesión 5).
    S-21 se contradice (ya en sesión 5). S-18: el trader duda del cuarto intento pero deja 3:
    `cartuchos_max` no se toca. Recomiendo activar S-5 y S-13 y dejar constancia de las reservas en
    las notas de la regla.
11. **Partir la rama (§0.f).** Opciones: (a) esta rama hasta el commit 7 (más el 11 si procede) y una
    segunda, `trabajo/activar-sesion-04-motor`, para A-21, S-13 y A-51 con sus ADR; (b) todo aquí.
    Recomiendo (a).
12. **Cómo queda E en el cierre de esta rama.** Opciones: (a) E sigue viva, reescrita: «activadas
    A-25, A-30, A-36, A-39, A-52 (y A-18, A-33, S-4 según la PARADA); quedan A-21, S-13 y A-51 para
    `trabajo/activar-sesion-04-motor`; las en parte, en la hoja de la sesión 5 (R4.1)»; I, R2.1 y
    R5.4 no cambian y F pasa a decir que lo siguiente es la rama de motor; (b) E HECHA y una letra
    nueva para la rama de motor, con I, F, R2.1 y R5.4 reescritas. Recomiendo (a): menos líneas que
    tocar y la hoja de ruta sigue diciendo la verdad.

**Espero tu respuesta a la PARADA.** Hasta entonces no se toca spec, knowledge ni código.

## Respuesta del consultor a la PARADA (2026-10-11)

Copiada tal cual:

> Modelo: Fable 5.1 · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA de trabajo/activar-sesion-04 (2026-10-11). Cópiala tal cual al final del encargo y del informe, en «Respuesta del consultor a la PARADA», con su fecha, y aplícala punto por punto (skill fase-cero). Si al aplicar algo medido lo contradice, PARADA 2.
>
> 0. A-18 y A-33 frente a ADR-0040: opción (a), escrita así para no chocar.
>    - ADR-0073 (comprueba que el número sigue libre): cierra A-18 y A-33 como RESUELTAS con registros RESOLVE_UNKNOWN de S-3 y S-12 (ningún valor cambia).
>    - El mismo ADR ENMIENDA ADR-0040: recuadro en 0040 y su fila de docs/adr/README.md como «ACTIVE (con enmienda de ADR-0073)», como 0064/0066 y 0063/0069. Lo que 0040 llama «refutada» pasa a ser «la regla dicha por el trader, contradicha por el material». Ningún dato de 0040 se toca.
>    - La contradicción pasa a una ambigüedad NUEVA, A-56 (comprueba que está libre): clase medicion, bloqueante: false (un bloqueante no se cierra como DECIDIDA y una medición nunca va al trader), resuelve_en [F26], con fuentes_documentales a ADR-0040. Su texto dice que la fila de agosto de ADR-0040 sale del xlsx y que en S-16 el trader da por bueno el backtest del vídeo.
>    - Se abre por sus sitios (AMBIGUEDADES.md: el yaml y la tabla de Known Ambiguities), con spec docs --escribir y test_kit.py en el mismo commit.
>    - A-33 lleva en sus notas la reserva literal de S-12 («no vamos a dejar correr nada por ahora»), y la de las ganadoras por debajo de 3R pasa a A-56.
>    - Líneas para el cierre: la deuda de PROJECT_STATE «F26 NO PUEDE PUNTUAR EL OBJETIVO HASTA QUE A-18 ESTE CERRADA», la G y R5.1 (Refs, texto y «Depende de») se reapuntan a A-56; sale el heredado 15 y R1.1 pierde HER:15 en sus Refs. V5-INSTANTES.md §95-104 queda superada: se dice, no se edita.
> 1. S-13: (a), en la rama de motor (punto 11). Reserva escrita en el ADR: lo dijo con sesgo previo alcista. La confirmación del caso bajista va a la lista de la sesión 5.
> 2. S-4: (a), por su régimen completo. ADR-0074 (comprueba que está libre) enmienda la decisión 5 de ADR-0064, con recuadro en 0064 y fila del índice: nunca uno sin el otro. caja_se_fija pasa a en_cada_cierre_m1 a mano, con fuente decision ADR-0074; su estado, el que el repo exija para un parámetro de ejecución bajo A-49 ABIERTA (dilo). El testimonio de S-4 va como registro sobre A-49 sin cerrarla. A-49 sigue ABIERTA y S-1 y S-2 van a la sesión 5. Sobre el freno de peticiones: ADR-0067 midió con la lectura de antes. El ADR-0074 da la cota con un test sintético (peticiones por M1 con el 1 expandiéndose; no dispara el bucle porque cambia el contenido), y la medida real queda para R3.1, dicho. Aquí sin arnés.
> 3. A-21: (a) sin_alternancia_de_colores (ningún cambio de color de una M1 a la siguiente en el retroceso, desde el fin del bloque de origen hasta la vela que rompe, excluida), y se SUMA al enum. Una vela sin cuerpo no cuenta como cambio de color: se salta, coherente con RN-007 (fuente fb-2026-09-29-sesion-03-ffab23dc). Es decisión del consultor y va en el ADR de la rama de motor, aparte del cierre de A-21, que es el RESOLVE_UNKNOWN del trader. Todo en la rama de motor.
> 4. A-30 y A-39: (a) aquí, solo spec. La rama ventana_fin de RN-035 (b) va a la rama de motor.
> 5. A-36: (a). Cierre con --supersede fb-2026-09-29-sesion-03-f3caeb2d, título intacto, nota de que vale para la orden stop (A-47) y test que congela el precio de la orden. C6 sigue anotada.
> 6. A-51: (a). Los cuatro parámetros, RN-036 aparte de RN-020 y un ADR, en la rama de motor. La nota §4.8 (las 9 pérdidas vienen de la cuenta con un 0,5 %) entra en la descripción de racha_perdidas_max: el bot también arriesga un 0,5 %.
> 7. --diagnostico-a21: (a), retirarlo en el commit de A-21 de la rama de motor. Línea para el cierre: --diagnostico-a47 (A-47 RESUELTA) y --diagnostico-a27 (A-27 DECIDIDA) siguen en la CLI sin deuda que los recoja; entran en G.2 de la hoja de ruta.
> 8. S-14: (a). Aleks lo lee en su propia terminal con --crudo, nunca con «!» en esta sesión, y te dirá «1 o 2» o «12». Si llega antes de la entrega, va al informe; si no, queda como pendiente de Aleks en las líneas del cierre. En los dos casos, S-14 va a la sesión 5 y H se queda.
> 9. A-43: (a), declarado como DESVIACIÓN de la regla de E («las en parte van a la sesión 5»), porque el valor provisional dice lo contrario de lo firme. CORRECT sobre toma_antes_de_la_ventana a cuenta, con ev-v10-014613-6cf002b2; la lista de A-43 gana el parámetro; A-43 sigue ABIERTA y la segunda parte va a la sesión 5. El informe y el commit lo dicen con esa palabra.
> 10. Activar S-5 (A-30, A-39) y S-13 con sus reservas en las notas de la regla. S-17 y S-21 siguen en la sesión 5. cartuchos_max no se toca.
> 11. Partir: (a). Esta rama: los commits 2 a 7 de §0.f, más ADR-0073 (punto 0) y ADR-0074 (punto 2). La rama de motor, trabajo/activar-sesion-04-motor, lleva A-21, S-13, A-51 y la rama ventana_fin de RN-035; su encargo lo escribo yo tras el cierre de esta.
> 12. E: (a), viva y reescrita, con F apuntando a la rama de motor. I, R2.1 y R5.4 no cambian.
> 13. S-16 (b.4): aquí no cambia nada, porque feedback new no tiene objetivo para E-1. Se registra en el informe y en ADR-0073 (por la fila de agosto). Línea para el cierre, nueva entrada de la Next Action: «el trader da por bueno el backtest de agosto grabado en vídeo (S-16); Aleks le pide su exportación; hasta que llegue, los casos dev de agosto siguen saliendo del xlsx; al llegar, entra por su propia rama (libros.yaml solo se amplía) y ADR-0040/A-56 se revisan». Lo mismo dijo el trader de julio, que ya está en S.
>
> LA LISTA PARA LA SESIÓN 5 (§0.e): vale con estos cambios:
> - quita el 10 (S-6: la spec ya dice un punto, y él se corrigió a un punto) y el 12;
> - el 11 queda solo para A-21 si la rama de motor no la cierra;
> - añade la confirmación bajista de S-13;
> - el fotograma de v4 del 8 no se abre sin decisión mía en R4.1.
>
> LÍNEAS DEL CIERRE: además de las de §0.g.2, las de los puntos 0, 7, 8 y 13, y la tabla de Known Ambiguities con A-56.
>
> Sigue lo que manda el encargo: un commit por respuesta, knowledge validate antes de make check, Fuente: en el cuerpo, CI de Linux por fix/activar-sesion-04 con su número de run, revisor (opus) con los dos alcances del encargo más un tercero (cada ADR enmendado tiene su recuadro y su fila del índice) y su informe pegado al final. Si el clasificador niega un push o la guardia un make, dame el comando exacto y lo lanzo yo con «!».
>
> Rama lista para revisión, NO cerrada.

## 1. La respuesta aplicada, punto por punto

Un commit por respuesta activada, en el orden de §0.f y con los pasos del paso 3 de
`activar-sesion`. Cada uno con `knowledge validate` en verde antes de `make check`, su sello y su
trailer `Fuente:`. Los registros de feedback son todos de `2026-10-04-sesion-04`, `medio: video`,
sobre la grabación de v10, con `t0`/`t1` de la cita y `procedencia: trader_grabado` salvo donde se
dice. `feedback apply --sesion 2026-10-04-sesion-04 --check` propuso en cada commit solo los
parámetros de esa respuesta (su salida va en cada punto).

### 1.1 Punto 11 · A-52 (S-20) · commit 89df2f4

- Registros: `fb-2026-10-04-sesion-04-f0e58d1f` (RESOLVE_UNKNOWN sobre A-52, 1:56:40–1:56:55) y
  `fb-2026-10-04-sesion-04-7ad9753b` (CONFIRM sobre `max_escenarios_por_sesion`, 1:54:49–1:55:04).
  `apply --check`: `~ max_escenarios_por_sesion 'sin_limite'`, 1 cambia, 0 ya estaban.
- `max_escenarios_por_sesion`: DEFAULT_AMBIGUOUS → CONFIRMED, mismo valor `sin_limite`; A-52
  RESUELTA; fila fuera de Known Ambiguities; `test_kit.py`; la hoja de la sesión 02 no la llevaba.
  `spec_version` 15.9.1 → 15.9.2.
- La copia de la respuesta del consultor no pudo ir en este commit: cita ADR-0073 y ADR-0074 y
  `knowledge validate` exige que los ids citados existan («id citado que no existe»). Se apartó con
  `git stash` y entra en el commit de ADR-0074 (§1.6). Es la trampa conocida de los ids futuros.

### 1.2 Punto 0 · ADR-0073: A-18 (S-3) y A-33 (S-12) RESUELTAS, A-56 abierta, ADR-0040 enmendado · commit 10a3922

- `docs/adr/0073-*.md` (número comprobado libre), recuadro de ENMIENDA al principio de ADR-0040 y
  su fila del índice «ACTIVE (con enmienda de ADR-0073)». Ningún dato de ADR-0040 se toca.
- Registros: `fb-2026-10-04-sesion-04-87ccb0ee` (A-18, 0:39:27–0:39:48) y
  `fb-2026-10-04-sesion-04-df162e6e` (A-33, 1:29:02–1:29:21). Ningún parámetro cambia (`apply
  --check`: 0 cambian). A-33 lleva en sus notas la reserva literal «no vamos a dejar correr nada por
  ahora», y las ganadoras por debajo de 3R pasan a A-56.
- A-56 nueva: clase `medicion`, `bloqueante: false`, `resuelve_en` [F26], `evidencia: []` y dos
  fuentes documentales a ADR-0040 (anclas «Decision» e «Impacto», literales dentro de la sección,
  comprobados por `knowledge validate`). Su texto dice que la fila de agosto de ADR-0040 sale del
  xlsx y que en S-16 el trader da por bueno el backtest del vídeo. Abierta por sus dos sitios (el
  yaml y la tabla de Known Ambiguities), `spec docs --escribir` y `test_kit.py` en el mismo commit.
- Notas de RN-011 y RN-015 y descripción de `base_calculo_objetivo`; la hoja de la sesión 02 y su
  test pierden A-18 y A-33; `spec_version` 15.9.2 → 15.9.3.
- Adelantado del plan (commit 7 de §0.f): `tests/unit/test_en_parte_no_se_cierra.py`: lo que la
  ÚLTIMA sesión da solo como «en parte» (o «resuelve en parte») no puede estar RESUELTA. La última
  sesión manda sobre la anterior: A-44 fue «resuelve con lectura nueva» en la 3 y es «en parte» en
  la 4, así que queda protegida. Demostrado por mutación en el propio test con un YAML sintético
  (A-13 RESUELTA → `["A-13 (RESUELTA)"]`).
- Su primer `make check` salió con 3 `MemoryError` de `lzma` en `tests/unit/test_ticks.py`
  (memoria libre del sistema, no la rama: los tres pasan solos y el `make check` repetido dio 2570
  passed). No es el recorte de procesos de Claude Code: el proceso terminó. Se relanzó.

### 1.3 Punto 11 · A-25 (S-18) · commit 1dc89d2

- Registros: `fb-2026-10-04-sesion-04-b3c218ce` (A-25, 1:54:21–1:54:34),
  `fb-2026-10-04-sesion-04-9f3e9dda` (CONFIRM `intentos_tras_toma_nueva`, 1:51:52–1:52:09) y la
  ratificación de `cartuchos_reinicio` (1:52:27–1:52:47), que tuvo dos formas: la primera,
  `fb-…-c145d9cc`, llevaba `--valor` y `knowledge validate` la negó («cartuchos_reinicio tiene 2
  registros vigentes que fijan su valor; uno debe superseder al otro»: la sesión 1 ya lo fija con
  `fb-2026-09-09-sesion-01-e3eedcaa`); la supersede `fb-2026-10-04-sesion-04-e0173b1b`
  (`reexpresion_consultor`, CONFIRM sin valor), que `feedback pending` cuenta como «confirmación de
  valor ya fijado». La fuente del parámetro sigue siendo la de la sesión 1. Lección: un CONFIRM de
  un valor que ya fija otro registro va SIN `--valor`, como los de la sesión 3.
- `intentos_tras_toma_nueva`: DEFAULT_AMBIGUOUS → CONFIRMED, mismo valor; A-25 RESUELTA y su lista
  gana el parámetro (hallazgo del auditor); notas de RN-004 y RN-016; la hoja pierde A-25;
  `spec_version` 15.9.3 → 15.9.4. `cartuchos_max` no se toca (el «se iría por una cuarta» queda en
  las notas).

### 1.4 Puntos 4 y 10 · A-30 y A-39 (S-5) · commit 0e18293

- Registros: `fb-2026-10-04-sesion-04-766c8d2e` (A-30, 0:54:27–0:54:51),
  `fb-2026-10-04-sesion-04-dd888b55` (A-39, 0:56:03–0:56:15) y `fb-2026-10-04-sesion-04-45e624c5`
  (CONFIRM `orden_pendiente_al_abrir_sesion`). `apply --check`: `~ orden_pendiente_al_abrir_sesion
  'se_retira'`, 1 cambia.
- `orden_pendiente_al_abrir_sesion`: DEFAULT_AMBIGUOUS → CONFIRMED, mismo valor; RN-035 deja de ser
  PROVISIONAL en su título y notas; A-30 y A-39 RESUELTAS y sus listas ganan el parámetro; la nota
  de RN-002 («LO QUE NO HACE») y la descripción de `retirar_orden_limite` se reescriben; el
  docstring de `engine/motor.py` deja de decir que al cambiar de sesión no se retira nada (comentario,
  sin cambio de comportamiento). La retirada a `ventana_fin` sigue siendo el cableado (ADR-0053 §6),
  sin regla: la rama `ventana_fin` de RN-035 va a `trabajo/activar-sesion-04-motor` (punto 4, opción
  (a)). Reservas en las notas: pregunta dirigida; «un minuto antes» es frase del consultor.
- `tests/unit/test_spec_fidelidad.py` cambia de sentido a propósito: la pendiente a las 15 ya no es
  una ambigüedad declarada sino un valor CONFIRMED, y A-30 sale del cuestionario. La hoja pierde
  A-30 y A-39 (y el bloque «Para terminar», que quedaba vacío). `spec_version` 15.9.4 → 15.9.5.

### 1.5 Punto 5 · A-36 (S-22) · commit b5a12e3

- Registro: `fb-2026-10-04-sesion-04-bbfb5c98` (RESOLVE_UNKNOWN sobre A-36, 1:02:14–1:02:37) con
  `--supersede fb-2026-09-29-sesion-03-f3caeb2d`, el REOPEN activo; la cadena queda 626c4dc7 ←
  a0b61bc9 ← f3caeb2d ← bbfb5c98. Título intacto; la nota dice que la respuesta vale para la orden
  stop (A-47). C6 sigue anotada.
- Sin parámetro. **No falta código**, al revés de lo que decía R1.1:
  `tests/unit/test_orden_en_el_0_con_mecha.py` congela que el 0 es el extremo con mecha del pivote
  (`punto.nivel == minima < cuerpo`), que `zona_del_punto` pone la entrada ahí y que la STOP se coloca
  a ese precio con un mercado con spread sin sumarlo. Pasa también en `main`: se escribe para que
  nadie lo mueva sin decirlo. `tests/unit/test_reabrir_y_fuente_documental.py` cambia de sentido a
  propósito (A-36 vuelve a RESUELTA y el REOPEN deja de estar activo). Nota en RN-011;
  `spec_version` 15.9.5 → 15.9.6. El primer `make check` cayó en el lint por una línea de comentario
  de 101 caracteres en `test_kit.py`; acortada y relanzado.

### 1.6 Punto 2 · ADR-0074: `caja_se_fija` = `en_cada_cierre_m1` (S-4); respuesta copiada

- `docs/adr/0074-*.md` (número comprobado libre), recuadro «Enmendada por ADR-0074» en la decisión 5
  de ADR-0064 y su fila del índice: los tres en el mismo commit.
- `caja_se_fija` pasa a `en_cada_cierre_m1` A MANO, con `fuente: {tipo: decision, id: ADR-0074}`:
  es de categoría `ejecucion` y `feedback apply` lo rechaza (`feedback/aplicar.py:187`). **Su estado
  queda en DEFAULT_AMBIGUOUS bajo A-49**, que es lo que el repo exige: `config/registro.py` solo
  admite `ambiguedad_id` con DEFAULT_AMBIGUOUS, y `tests/contract/test_provisional_cuelga_de_abierta.py`
  exige que esa ambigüedad esté ABIERTA (lo está: S-1 y S-2 van a la sesión 5). Cuando A-49 se
  cierre, pasará a CONFIRMED con esta misma fuente, como `reloj_sesiones` con ADR-0069.
- `tests/unit/test_caja_hasta_el_llenado.py`: (1) el registro dice `en_cada_cierre_m1` bajo A-49 con
  fuente ADR-0074 (falla en `main`); (2) con velas que suben el máximo una a una, una zona distinta
  del mismo punto por cada máximo nuevo, el 0 quieto y el 1 solo sube; (3) la cota de peticiones:
  dos por zona menos una, todas admitidas por el freno de ADR-0067 sin ningún corte, frente al
  mismo número de colocaciones con la MISMA firma, que sí dispara `freno_bucle`. Sin arnés: la
  medida real es R3.1; lo que F35 midió en DIAGNÓSTICO (hasta 14 peticiones al día y 59 en 42 días
  con esta lectura) se cita en el ADR. `tests/unit/test_orden_stop_pivote.py` cambia de sentido a
  propósito: la caja fija deja de ser el registro real y pasa a pedirse expresamente.
- `spec_version` 15.9.6 → 15.9.7. Entra la copia de la respuesta del consultor al final del encargo y
  de este informe (§1.1).
- **El testimonio de S-4 como registro sobre A-49 es la PARADA 2 (abajo).**

## PARADA 2 · La forma del registro de S-4 sobre A-49 (punto 2)

El punto 2 dice «el testimonio de S-4 va como registro sobre A-49 sin cerrarla». Medido:

- Un registro con `objetivo: ambiguedad` solo admite `RESOLVE_UNKNOWN` o `REOPEN`
  (`knowledge/feedback/README.md`, coherencia exigida; `feedback/modelo.py`). `CONFIRM`, `CORRECT` y
  `REJECT` van sobre evidencia, regla o parámetro.
- Un `RESOLVE_UNKNOWN` activo sobre una ambigüedad ABIERTA no lo niega `knowledge validate`
  (`problemas_de_cierre` solo exige que una RESUELTA tenga uno y que un REOPEN activo tenga ABIERTA),
  pero `feedback pending` lo cuenta como **pendiente** mientras A-49 siga ABIERTA (`cli.py:2029-2041`:
  «A-49 esta ABIERTA»), y la skill exige que `feedback pending` no liste nada de lo activado.
- Un `CORRECT` sobre el parámetro `caja_se_fija` hace fallar `feedback apply --check` de toda la
  sesión («es de categoria ejecucion y solo se cambia por decision (ADR)»): rompería los commits
  siguientes.

Opciones: (a) `RESOLVE_UNKNOWN` sobre A-49 con `valor` «caja_se_fija = en_cada_cierre_m1; A-49 sigue
ABIERTA (S-1 y S-2)», aceptando que `feedback pending` lo liste como pendiente hasta que la sesión 5
cierre A-49 (entonces ese registro será uno de los que la cierran); (b) `CONFIRM` sobre la evidencia
`ev-v10-004945-59ebac47` («confirma el ítem»), que `pending` lista como «sin forma mecánica de
comprobarlo», igual que los nueve de la sesión 1; (c) sin registro: el testimonio queda en el ADR y
en la descripción del parámetro, que ya citan los tres ítems. Recomiendo (b): es un registro del
trader sobre lo que dijo, no cierra nada y no deja un pendiente falso. Coste de (a): un pendiente
que nadie puede reflejar hasta la sesión 5. Coste de (c): el testimonio no entra en
`knowledge/feedback/`.

**Espero tu respuesta a la PARADA 2** para el registro; todo lo demás del punto 2 está en el commit.

## Estado

FASE 0 HECHA; respuesta del consultor recibida el 2026-10-11 y en aplicación.
