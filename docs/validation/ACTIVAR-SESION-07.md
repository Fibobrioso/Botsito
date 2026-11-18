# ACTIVAR-SESION-07 · Las respuestas de la sesión 7a entran en la spec y en el motor (R4.3, entrada F)

> PLANTILLA hasta la fase 0 (la línea con que nació): la tabla de activación ya está, en «0.1».

Rama `trabajo/activar-sesion-07`, abierta el 2026-11-18 desde `main` en f66743e3 (commit de estado
sobre el merge 5c047f31 del tag `stable/F39d-sesion-07`). Encargo:
`docs/encargos/trabajo-activar-sesion-07.md`. Tramo: R4 (R4.3 de `docs/plan/HOJA-DE-RUTA.md`; el
punto (1) de la F de la Next Action). Tag previsto: `stable/F39e-activar-sesion-07` (no existe ni en
local ni en origin: `git tag -l` y `git ls-remote --tags origin 'stable/F39e*'` vacíos).

## Base comprobada (abrir-rama, paso 1)

- `git rev-parse main origin/main`: `f66743e3d8ec7fc75769d17be75c34d55d2bc4a7` dos veces; `git status --short` vacío.
- `git rev-parse "stable/F39d-sesion-07^{commit}"` = `5c047f3115806a7a8cddc17614c7d40ba9bd2cfc` = `git rev-parse main^1`; en origin: `git ls-remote --tags origin stable/F39d-sesion-07` da `e5490708…` (el objeto del tag anotado).
- CI de `main`: `gh run view 44316126260` (suelto, sin guion) → `status: completed`, `conclusion: success`, `headSha: f66743e3d8ec7fc75769d17be75c34d55d2bc4a7`.
- `git branch --list` solo daba `main`; `git ls-remote --heads origin "fix/*"` vacío.

## Desviaciones de la apertura

- **A-58 no va en el bloque `ids-inexistentes` del encargo.** El encargo pide declarar el ADR nuevo y
  A-58; el bloque solo admite ids de fuente (`comun.ids.FUENTE`: `ev-*`, `fb-*`, `ADR-NNNN`), y
  `validation/ids_citados.py` da «declaracion de ids-inexistentes mal formada: linea sin un id al
  principio» con cualquier otra cosa. Esa guardia no comprueba ids de ambigüedad en `docs/`, así que
  A-58 no necesita declaración: solo va el ADR nuevo.

## Fase 0 (2026-11-18; skill fase-cero, sin tocar nada)

La PARADA es CONDICIONAL (encargo): la fase 0 se escribe entera y se commitea; después cada fase cuya
medida CUADRA con la decisión del consultor se hace, y la que no cuadre se queda en la PARADA con su
alternativa. Las decisiones de abajo, en «Lo que necesito que decidas», no frenan ninguna fase: o
son lo que el encargo ya decide, o son añadidos de documento que aplico con la recomendación y se
dicen.

### 0.1 La tabla de activación (una fila por fila de la tabla final de `SESION-07-EXTRACCION.md` §6)

Columnas de la skill `activar-sesion` («El recorrido», 1), con el destino del encargo (MIS
DECISIONES) y lo que veo distinto. «Registro de hoy» es `uv run botsito feedback trace <id>`;
«estado hoy», `knowledge/spec/parametros.yaml`. Ninguna fila trae horas de reloj (las del bloque de
días son de construcción y no se activan). Quién la espera: la tabla Known Ambiguities de
`PROJECT_STATE.md` (A-13, A-35, A-43, A-53 y A-16 ABIERTAS) y R4.3 de `docs/plan/HOJA-DE-RUTA.md`
(«7a y 7b ingeridas y activadas»).

| Fila de §6 | Ambigüedad / sitio | Lo que dijo (ítem) | Registro de hoy | Estado hoy | Premisa vigente | Qué falta | Destino (encargo) | Lo que veo distinto |
|---|---|---|---|---|---|---|---|---|
| S-4, pregunta 1 | A-35 (ABIERTA, bloqueante) | no elige (§3.1) | — | `liquidez_m15_mecha_que_vuelve` = `solo_la_contraria`, DEFAULT_AMBIGUOUS | sí | sin respuesta | siguiente sesión (7b, reformulada) | nada |
| S-4, pregunta 2 | A-35 | (a), la punta de la mecha, «en el esquema planteado» (`ev-v18-002511-eec0acec`) | — | ídem | sí | no da valor sola | F3: la descripción del parámetro lo gana, sin valor | nada |
| S-4, la mecha de una verde | A-35 | también fija el alto si queda más alta (`ev-v18-002701-62875550`) | — | ídem | sí | en parte | F3: «en parte», a la 7b | nada |
| **S-2** | A-13 (ABIERTA, no bloqueante); A-4 (RESUELTA); RN-014 | «otra»: el break even al formarse y validarse una zona de control, al cierre (`ev-v18-001327-70f1d014`, `ev-v18-001900-1581efbe`) | `break_even_condicion`: `fb-2026-09-09-sesion-01-0ccafcba` (CORRECT, activo); `break_even_criterio_ruptura`: `fb-2026-09-29-sesion-03-2cff5008` (activo); RN-014: `fb-2026-09-29-sesion-03-9f506366` (activo); A-4: `fb-2026-09-09-sesion-01-7fcb971c` (activo) | `tocar` y `mecha`, los dos CONFIRMED | sí | **contradice lo fijado** (dos CONFIRMED y el literal «apenas toca» de RN-014) | F2: tres CORRECT con supersede (desviación declarada de «en parte no se cierra») | nada que cambie el destino; ver 0.4 |
| S-2, el imbalance | A-13 | no lo usa, no hay excepción (`ev-v18-001145-901d8aa0`) | — | la excepción vivía solo en la descripción de `break_even_condicion` (sesión 6) | sí | — | F2: las descripciones dicen que queda descartada | nada |
| S-2, el margen | A-13 | «un par de puntos o un pip», una vez, en un ejemplo (`ev-v19-011529-8ae8b581`) | — | sin parámetro | sí | en parte | F2.3: no se activa; A-13 sigue ABIERTA solo por él | nada |
| **S-1** | RN-003 (sin ambigüedad abierta; A-1 RESUELTA) | (a), «El rango es la vela verde grande y sigo buscando compras» (`ev-v18-000249-bb7b1c07`); lado por ruptura con mecha o cuerpo y color (`ev-v18-000408-c48297b1`) | RN-003: `fb-2026-10-04-sesion-04-6e7da456` (CORRECT, activo); A-1: `fb-2026-09-09-sesion-01-41f46b21` | `sesgo_h4_criterio_ruptura` = `mecha`, CONFIRMED (no cambia) | sí | **contradice la regla fijada** (la H4 previa frente a su anterior) | F1: CORRECT sobre RN-003, ADR nuevo | ver 0.3 |
| S-1, qué vela pasa a ser el rango nuevo | ídem | la vela que rompe, arriba o abajo, y su color; no dice su alto y su bajo (`ev-v18-000822-57145b90`) | — | — | sí | en parte | F1: parámetro `sesgo_h4_rango_nuevo` DEFAULT_AMBIGUOUS bajo A-58 (nueva) | nada |
| S-1, «rango mayor» | ídem | el rango cuya liquidez no se ha mitigado, ni por encima ni por debajo; manda hasta mitigarse (`ev-v18-000912-52594a58`) | — | — | sí | — | F1 (lo sostiene la regla a) | nada |
| S-3 | RN-009 | «otra»: A y B (`ev-v18-002115-bf40ec0b`); definición (`ev-v18-002229-2be4ecf1`) | — | `zonas_control_max_por_esquema` sin cambio | sí | no dice si con A y B descarta el esquema | F3: nada; a la 7b reformulada | nada |
| S-3, el bajo de la propia toma | RN-009 | «todo el esquema», sin sí ni no (`ev-v18-002223-fa0fc6ab`) | — | — | sí | no resuelve | a la 7b | nada |
| S-5 | ADR-0064 | sin letra; por «Para precisar», la mecha mete (`ev-v18-003237-df38be59`, `ev-v18-003341-ce760e43`) | — | `orden_limite_nace` sin cambio | sí | — | F3: no cambia nada | nada |
| S-5, ¿M1 o M15? | ADR-0064; S-18 de la sesión 5 | M1, el cuerpo de la toma de M15 (`ev-v18-003351-5bf50a14`) | — | — | sí | — | F3: no contradice `ev-v16-000234-9a4fa375`; recuadro en TRAZAS-ABLACION.md | nada |
| S-6 | F7 #10 | (a), salvo las de break even (`ev-v18-003634-de26ff65`, `ev-v18-003706-83ce78dd`) | — | — | sí | — | F3: ninguna regla; línea para la orden de cierre | nada |
| Sesiones 1, 2 y 4 del bloque | — | correcciones sobre construcción (§4) | — | — | — | ejemplos, sin «¿siempre…?» | ninguna se activa; las de S-1 y S-2 solo sostienen lo dicho en el bloque técnico | nada |
| Sesión 3 del bloque (07-03 07-11) | — | — | — | — | — | sin extraer | gastada; no se vuelve a usar | nada |
| Reserva (04-13) | A-13, A-43, A-53, A-16 | el margen; la toma con velas de la sesión; una sola orden que se mueve; la vela de otro color | — | `toma_antes_de_la_ventana` = `cuenta`, CONFIRMED | — | ejemplos | F3: ninguna se activa | nada |

**Las dos contradicciones con lo fijado, con sus dos fuentes** (la skill pide PARADA con las dos;
las decisiones del consultor del 2026-11-18, en el encargo, son la respuesta anticipada):

1. **RN-003.** Lo fijado: `fb-2026-10-04-sesion-04-6e7da456` (CORRECT por WhatsApp, ADR-0080): «la
   vela roja debe de haber roto con cuerpo o con mecha el bajo de la vela alcista Y terminar al
   cierre bajista», con la vela H4 previa contra su anterior. Lo nuevo: `ev-v18-000249-bb7b1c07`
   («El rango es la vela verde grande y sigo buscando compras») y `ev-v18-000912-52594a58` (el rango
   mayor manda hasta mitigarse). Decisión del encargo: F1, CORRECT sobre RN-003 con ADR nuevo.
2. **El break even.** Lo fijado: `fb-2026-09-09-sesion-01-0ccafcba` (`break_even_condicion` =
   `tocar`, «Apenas toca»), `fb-2026-09-29-sesion-03-2cff5008` (`break_even_criterio_ruptura` =
   `mecha`) y `fb-2026-09-29-sesion-03-9f506366` (RN-014, «apenas toca, pues se pone en B la
   entrada»). Lo nuevo: `ev-v18-001327-70f1d014` y `ev-v18-001900-1581efbe` (al cierre, cuando se
   valida una zona de control), `ev-v18-001145-901d8aa0` (sin excepción del imbalance). Decisión del
   encargo: F2, tres CORRECT con supersede.


### 0.2 El control de D0 (etiqueta `base`, código de `main`)

Fila de `HOLDOUT-EXPOSICIONES.md` del 2026-11-18 escrita y commiteada antes de correr. La carpeta
`data/activar-sesion-07/` se creó antes (`motor arnes` no crea la de `--salida`: `cli.py:2473`,
hallazgo del auditor). Las tres órdenes, sueltas y sin `make check` en marcha:

1. `uv run botsito motor arnes --simular --meses 2026-07 --salida data/activar-sesion-07/julio-base.txt` → exit 0.
2. `uv run python docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/patrones.py data/activar-sesion-07/julio-base.txt --filas > data/activar-sesion-07/patrones-julio-base.txt` y `sed -i 's/\r$//'` sobre ese fichero → exit 0.
3. `uv run python docs/validation/anexos/PREPARACION-SESION-7/pivote_julio.py data/activar-sesion-07/patrones-julio-base.txt` → **«OK: 14 y 39»** (T0 14; P5 37, 10 del otro lado y 27 del mismo; P6 en sesión 2; P1 20, P2 14, P3 15, P4 1, P7 3; salida en `anexos/ACTIVAR-SESION-07/pivote-julio-base.txt`).

Y las filas: `grep "| 2026-07-"` de `patrones-julio-base.txt` y de
`anexos/RECORRIDA-CONSTRUCCION-2/patrones-cuenta-por-mes.txt` dan 106 líneas cada uno y `cmp` los da
**idénticos**. **El control reproduce con `--meses 2026-07`**: no hizo falta la corrida de toda la
construcción (la línea base se produjo sin `--meses`, RECORRIDA-CONSTRUCCION-2.md:354; con julio
solo sale lo mismo porque los datos y la cuenta van por mes). Esa es la forma de toda la rama.

`delta_julio.py` (con su README antes de correr, en `anexos/ACTIVAR-SESION-07/`) probado contra sí
mismo (base frente a base): 106 y 106 filas, 25 sesiones de julio, 0 cambios. **Desviación
declarada**: lleva cuatro argumentos, no dos; el rn003 de cada sesión no está en la salida de
`patrones.py`, así que lo lee de la línea «Por sesion» de las dos salidas del arnés.

**El rn003 de hoy en las siete sesiones declaradas de F1** (de esa misma salida): 07-01 07-11
bajista, 07-06 07-11 bajista, 07-06 11-15 bajista, 07-07 07-11 bajista, 07-07 11-15 bajista, 07-15
11-15 bajista y 07-17 11-15 alcista: las siete del lado contrario al del trader, como dice
VIDEO-JULIO.md.

### 0.3 F1: los lectores del sesgo, RN-003 y sus regímenes

**Quién llama a `sesgo_h4` y quién lee `ResultadoSesgo`** (`grep` de `sesgo_h4(`, de cada campo y
de las anotaciones `ANOTACION_SESGO*` en `src/`, `scripts/` y `docs/validation/anexos/`):

| Lector | Qué lee | fichero:línea |
|---|---|---|
| el motor (predicado `sesgo_h4_al_abrir`) | `sesgo`; `doble_ruptura`, las tres `saltadas_*`, `vela_que_fija` y `h4_saltadas` como anotaciones de la sesión (solo registro) | `src/botsito/engine/primitivas.py:196-238` (el sujeto, `SUJETO_SESGO`, en `:61`) |
| el arnés, «## RN-003 al abrir la sesion» | las anotaciones: el sesgo por sesión, las dobles y las sesiones con saltadas por motivo | `src/botsito/engine/arnes.py:300-331`, `:418-429` |
| el arnés, «## Por sesion» | la anotación `sesgo_h4` como `rn003 <valor>` | `src/botsito/engine/arnes.py:328-337` (`patrones.py` la lee con `POR_SESION`, `anexos/RECORRIDA-CONSTRUCCION-2/patrones.py:60`) |
| el visor | llama a `sesgo_h4` él mismo y deduce la H4 que decide y su anterior por `velas_miradas` (`cerradas[len - velas_miradas]`); escribe `velas_miradas`, `ruptura_puntos`, `doble_ruptura` y «rompe la H4 que abre a las … contra la anterior» | `src/botsito/engine/visor.py:394-403`, `:766-783`, `:1064` |
| las láminas | las anotaciones: el sesgo (contra el hecho), la doble, la vela que fija (dentro o fuera de la ventana) y las saltadas, que tienen que casar con sus recuentos o dan `LaminaError` | `src/botsito/engine/laminas.py:462-497` (frases), `:824-856`; el panel, `laminas_svg.py:337-358` |
| `motor decisiones` | lo mismo que el arnés, a través de la traza (no lee `ResultadoSesgo`) | — |
| guiones de diagnóstico de ramas cerradas | llaman a `sesgo_h4` con su firma de hoy | `scripts/sesgo_h4_diagnostico.py`, `scripts/bloque_de_la_caja.py`, `scripts/orden_stop_o_limite.py`, `scripts/verificacion_a21.py`, `scripts/verificacion_a21_entradas.py`, `scripts/verificacion_a35_a44.py`, `anexos/CORRIDA-CONSTRUCCION/sesgo_p1.py` y `sesgo_2x2.py`, `anexos/ENTRADA-ENERO/sesgo_enero.py` |

Los guiones son de ramas cerradas: no se corren ni se tocan aquí (con el parámetro nuevo como
argumento con valor por defecto, su llamada sigue valiendo y darían la regla nueva).

**Qué significa cada campo con la regla nueva** (propuesta; la regla es la del encargo, a) a e)):

- `sesgo`: el lado del rango vigente; INSUFICIENTE si ninguna H4 lo fijó desde el arranque.
- `ruptura_puntos`: cuánto superó la H4 que fijó el lado el extremo del rango que rompió (con doble
  ruptura, el del lado del color). Hoy es contra su H4 anterior.
- `velas_miradas`: cuántas H4 se compararon con el rango en el recorrido (sin la del arranque). Hoy
  es cuántas miró hacia atrás hasta decidir. **El visor deja de deducir la H4 que decide por él**:
  la toma de `vela_que_fija` y el rango de los campos nuevos.
- `doble_ruptura`: la H4 que fijó el lado rompió los dos extremos del rango.
- `saltadas_*` y `h4_saltadas`: las H4 que rompieron el rango DESPUÉS de la que lo fijó (o desde el
  arranque, si ninguna lo fijó) sin decidir; con ellas el rango no cambió (d y c sin cuerpo). Hoy
  son las que la búsqueda hacia atrás saltó antes de la que decide, que es el mismo conjunto
  temporal (las posteriores a la que fija). Las láminas siguen exigiendo que casen con sus
  recuentos.
- `vela_que_fija`: la H4 que fijó el lado, que con la regla nueva es también la del rango.
- Nuevos, solo registro: `rango_alto`, `rango_bajo` y `rango_vela` (con lado, la misma que
  `vela_que_fija`; sin lado, la del arranque).

**RN-003 en `knowledge/spec/strategy_spec.yaml:1079-1181`.** Título «el sesgo lo fija la vela H4
previa, y solo cambia si rompe su extremo»; `entonces` con la regla de ADR-0080; `cita`
`fb-2026-10-04-sesion-04-6e7da456` con su `literal`; `notas` con la historia (ADR-0060, ADR-0075,
ADR-0080 y las tres CONFIRM de la sesión 5), donde vive la reserva «suponiendo que no haya otro
rango mayor» (`:1127-1128`, de `SESION-04-EXTRACCION.md` §3.14); `forma` con el predicado
`sesgo_h4_al_abrir` (`que: vela_h4_previa`, `contra: extremo_de_la_h4_anterior`, `criterio`,
`tope`); `decision: ADR-0044`. El predicado tiene su propia `cita` y `literal`
(`strategy_spec.yaml:62-82`), y los dos sujetos son tokens del vocabulario (`:594-597`). **Con la
regla nueva cambian el título, el `entonces`, la `cita` y su `literal`, la forma (el sujeto y un
argumento nuevo, `rango_nuevo`), la descripción y la cita del predicado, y dos tokens nuevos; las
notas se conservan y ganan su párrafo.** Que el predicado cambie de `cita` no es un sitio nuevo con
`cita` (las tres guardias de `spec/modelo.py` ya lo cubren); si el modelo lo pide, se mide al
escribirlo.

**El régimen del CORRECT sobre RN-003**: un registro `CORRECT` con `objetivo.tipo: regla`, como sus
tres anteriores (ADR-0060: `fb-2026-09-29-sesion-03-31fb311f`; ADR-0075:
`fb-2026-10-04-sesion-04-ca0afae6`; ADR-0080: `fb-2026-10-04-sesion-04-6e7da456`), **sin
`supersede`**: los anteriores siguen sosteniendo lo que la regla nueva conserva (el color con doble
ruptura, la neutra, el color con un extremo), como hizo ADR-0080 §8 («Ninguno supersede a…»).

**A-1**: RESUELTA con `fb-2026-09-09-sesion-01-41f46b21` (la H4 previa). `AMBIGUEDADES.md` no pide
`REOPEN` ante un CORRECT sobre una regla: el `REOPEN` es para volver a preguntar una ambiguedad, y
ADR-0080 §9 decidió no reabrirla en el mismo caso («lo que cambia es la condición del cierre, que
entra por el CORRECT sobre RN-003, como ADR-0060 y ADR-0075 cambiaron la regla sin reabrir A-1»).
Reabrirla quitaría la fuente de `sesgo_h4_regla` (CONFIRMED). **CUADRA con tu lectura: una nota,
sin REOPEN.**

**La ambigüedad nueva (A-58)**: abrirla toca dos sitios (`ambiguedades.yaml` y la tabla Known
Ambiguities, `tests/unit/test_kit.py`) y obliga a `spec docs --escribir`; `clase: pregunta` exige
evidencia del trader (no fuentes documentales); el parámetro DEFAULT_AMBIGUOUS lleva
`ambiguedad_id: A-58`. La deuda «buscar en el corpus antes de redactar cualquier ambigüedad, y
escribir qué se buscó» (el precedente de cómo se escribe es A-57, `ambiguedades.yaml`: la búsqueda
va en la `pregunta`) se paga en el commit que la abre, con `kb find` y lo que salga.

### 0.4 F2: el break even

**El nivel de RN-014.** `se_completa_zona_de_control` con `posterior_a`
(`src/botsito/engine/primitivas_broker.py:259-299`) llama a
`domain/estructura_m1.zona_posterior_completada` (`estructura_m1.py:263-316`): sobre las M1 cerradas
desde la de la entrada, una vela CONTRARIA que sigue a una racha a favor deja el punto extremo de
esa racha -el alto en una compra, el bajo en una venta- y abre el retroceso, que es la zona de
control; la zona se completa cuando una M1 posterior PASA ese punto con el criterio (manda el
último punto formado; la vela sin cuerpo no corta la racha, ADR-0085). **Es el extremo de la zona de
control posterior a la entrada (ADR-0061 §4).**

**Qué hace cada opción hoy.** `_pasa` (`estructura_m1.py:105-113`): con `mecha`, el máximo (compra)
o el mínimo (venta) pasa el nivel; con `cuerpo`, **el cierre** pasa el nivel (`cierre > nivel` en
una compra, `cierre < nivel` en una venta). Con `break_even_condicion = tocar` y criterio `mecha`, el
cableado vigila el nivel al tick (`cableado.py:414-421`, `primitivas_broker.py:281-287`); con `cierre`
o con `cuerpo` no hay vigilancia al tick y el stop se mueve en el cierre de la M1 que pasa el punto
(ADR-0065 §5; `primitivas_broker.py:289-291`). **Con `cierre` y `cuerpo`, el motor pide que una M1
CIERRE más allá del nivel, y mueve el stop en ese cierre. CUADRA.** No falta código: las dos
opciones existen.

**El régimen de los tres CORRECT** (`feedback trace`):

| Objetivo | Registro activo hoy | El CORRECT nuevo supersede |
|---|---|---|
| `break_even_condicion` | `fb-2026-09-09-sesion-01-0ccafcba` (CORRECT, `tocar`; supersede a `01d4d267`) | `fb-2026-09-09-sesion-01-0ccafcba` |
| `break_even_criterio_ruptura` | `fb-2026-09-29-sesion-03-2cff5008` (RESOLVE_UNKNOWN, `mecha`) | `fb-2026-09-29-sesion-03-2cff5008` |
| RN-014 | `fb-2026-09-29-sesion-03-9f506366` (CORRECT; el literal «apenas toca») | `fb-2026-09-29-sesion-03-9f506366` |

Los tres se citan en `knowledge/spec/` (`parametros.yaml:500` y `:1004`, `strategy_spec.yaml:1759`
y en prosa en `:1764`, `:1768-1769` y `ambiguedades.yaml:209`): cada commit pasa su cita al registro
nuevo, y G1 de `knowledge validate` dice si la prosa también cuenta.

**A-4** (RESUELTA, `fb-2026-09-09-sesion-01-7fcb971c`, `RESOLVE_UNKNOWN` sobre la ambigüedad con
valor `tocar`, `parametros: [break_even_condicion, break_even_criterio_ruptura]`): ninguno de los
tres CORRECT supersede su registro, que es otro (el del parámetro es `0ccafcba`). Nada del régimen
pide `REOPEN` para cambiar un parámetro con CORRECT (`AMBIGUEDADES.md`; `knowledge validate` lo
dirá). **CUADRA con tu lectura: una nota, sin REOPEN**, que diga que su valor `tocar` lo corrige el
CORRECT del parámetro. **A-13** (ABIERTA, no bloqueante, `parametros: [break_even_criterio_ruptura]`):
sigue ABIERTA solo por el margen; su `pregunta` lo dice.

**Los tests que congelan `tocar` y `mecha`** (`grep` de los dos parámetros, `BREAK_EVEN_AL_TOCAR`,
`vigilar_break_even` y `break_even_vigilable` en `tests/`): `tests/unit/test_be_al_tick.py:209-275`
(`_registro_con_break_even` reescribe `valor: "tocar"` del registro real, y
`test_por_el_motor_el_break_even_al_tocar_salva_la_m1_que_toca_y_vuelve` toma el registro real como
`tocar`); los de `test_kit.py:80-128` y `test_spec.py:955-978` son registros sintéticos o la
declaración del parámetro en RN-014, que no cambian. Lo que más rompa, lo dirá `make check` en F2.

**Las cifras del break even, en julio** (auditor, #54): las «100 líneas `stop_movido` frente a 247
operaciones llenadas y cerradas» del encargo son de toda la construcción
(`anexos/RECORRIDA-CONSTRUCCION-2/resumen-cuenta-por-mes.txt:84-87`); en julio, el mes de la corrida,
son **18 frente a 53**.

### 0.5 Lo que el encargo hereda, y lo que choca

**Herencias** (skill activar-sesion, «Entradas»; `grep` de «7a», «activación» y «sesion-07» en la
Next Action, la hoja de ruta, HISTORIA y los informes; y el auditor):

| # | Herencia | Dónde | Qué hago |
|---|---|---|---|
| 1 | Las láminas de la 7b, la revisión de `PREGUNTAS-7B.md` y `SESION_EN_CURSO = "08"` eran de «la activación de la 7a» | la F (`PROJECT_STATE.md`), R4.3 «Qué es» (`HOJA-DE-RUTA.md:386`), recuadro D4 de `docs/sesion-7/PREGUNTAS-7B.md:8-14` | el encargo las pasa a la rama siguiente («primera de dos ramas»): no se hacen; la sección «Para la rama siguiente» las lista, y la línea de la F se prepara para que lo diga |
| 2 | b1 y el `LaminaError` de RN-004 «van al encargo de la rama de activación de la 7a» | `LAMINAS-MOTIVOS.md:826` y `:848` | a «Para la rama siguiente», que es la que genera las láminas |
| 3 | Revisar las filas de cada pregunta de la 7b con la corrida nueva, y si entra alguna de §3 | recuadro D4 de `PREGUNTAS-7B.md:11-13`; `PREPARACION-SESION-7.md:349` y `:736` | a «Para la rama siguiente»; la corrida de julio de esta rama no da las filas de enero y abril del bloque |
| 4 | El 2026-04-15 de 11 a 15 (sesión 2 del bloque de la 7b) ya salió en la 7a, abierto por error | `SESION-07-EXTRACCION.md` §5.1, punto 9 | a «Para la rama siguiente», junto al 2026-07-03 gastado |
| 5 | M de la Next Action: el break even de una venta por el ASK (ADR-0065 §6) | `PROJECT_STATE.md`, Next Action | con `cierre` la vigilancia al tick no se arma (ADR-0065 §1-§2 y §5): M queda sin objeto mientras `break_even_condicion` sea `cierre`. Lo dice el recuadro de ADR-0065 y se prepara la línea de M para la orden de cierre (decisión 2) |
| 6 | ADR-0061 §3-§5 dicen «al tocar» y `mecha` | `docs/adr/0061-*.md` | no está en la lista de recuadros del encargo: decisión 1 |
| 7 | Technical Debt «El visor no enseña las H4 que el sesgo salta por el color» | `PROJECT_STATE.md`, Technical Debt (ADR-0080 §10) | F1 toca el visor: dirá el rango vigente; la deuda de las saltadas sigue (decisión 3) |
| 8 | El punto 6 de F1 mide sobre toda la construcción y calienta con marzo y junio | `PROJECT_STATE.md`, Technical Debt | fila de `HOLDOUT-EXPOSICIONES.md` antes de correrlo |
| 9 | `engine/decisiones.py:7-8` viejo con ADR-0093 | `PROJECT_STATE.md`, Technical Debt | fuera del alcance: no se toca |

**Lo que choca con un ADR o con una respuesta anterior** (medido contra los ADR, no contra el
encargo):

- **«NO es un parámetro ni un interruptor» (F1.1).** ADR-0080 D5 y su alternativa 1 descartan un
  interruptor para la exigencia del COLOR (`0080:83-89`, `:214`); para la regla del rango es la
  misma razón por analogía (es la definición del trader), y el ADR nuevo lo dirá así, sin atribuir a
  ADR-0080 lo que no dice (auditor, #44).
- **ADR-0060 descartó una alternativa por depender de cuántas velas hubiera cargadas**
  (`0060:152-153`): la regla e) vuelve a depender de ello. El encargo lo sabe y lo mide (punto 6);
  el ADR nuevo lo dirá.
- **La desviación de «en parte no se cierra» (F2).** La fila S-2 está «en parte» por «otra»
  (`SESION-07-EXTRACCION.md` §6:769); el margen es otra fila (§6:771), también «en parte» (auditor,
  #52). La desviación activa la primera y deja la segunda: el informe lo dirá así.
- **El revisor y la CI.** La skill `entregar-rama` pone la CI (paso 7) antes del revisor (paso 8), y
  la fila de `trabajo/activar-sesion-06-motor` en ERRORES-RECURRENTES dice «el revisor tras la CI».
  El encargo los nombra al revés; ganan las skills.
- Ninguna otra: el resto del encargo casa con los ADR que nombra (auditor: 49 de 60 correctas).

### El encargo frente al repo (auditor-encargo, 2026-11-18)

60 afirmaciones contrastadas: 49 correctas, 1 incorrecta, 10 con matiz; 9 herencias no recogidas;
3 defectos del contrato. Lo que cambia algo:

- **INCORRECTA (#5)**: declarar A-58 en el bloque `ids-inexistentes` (ya declarado como desviación
  de la apertura).
- **Matices** que se aplican: la orden 1 de D0 no crea su carpeta (#20; se creó a mano) y la línea
  base salió sin `--meses` (el control reproduce igual, 0.2); `generar_capa.py --comprobar` compara
  el `Generado.mqh` y exige `--repo` y `--perfil` (#16; medido: «al dia», y ninguno de los
  parámetros de la rama está en `ENTRAN`, `generar_capa.py:59-95`); `feedback new` con medio vídeo
  exige `--grabacion` (#18); la deuda de «buscar en el corpus antes de redactar» vive en Technical
  Debt de `PROJECT_STATE.md`, no en `AMBIGUEDADES.md` (#32); el literal de RN-014 es entero «apenas
  toca, pues se pone en B la entrada» (#33); #44, #52, #54 y #60, arriba.
- **El ítem vigente de v11 0:00:38** es `ev-v11-000038-fef9789d`, que supersede a
  `ev-v11-000038-a322e483` (cuya afirmación decía «de H4», que la cita no trae) (#41).
- **Las 30 filas** de VIDEO-JULIO.md: P1 2+4+1+8+4+1 = 20 y P5 del otro lado 3+6+1 = 10, en las
  siete sesiones nombradas (#48).
- **Tres defectos del contrato** (míos): la comprobación `scripts/generar_capa.py` (no existe: es
  `src/botsito/mql5bridge/generar_capa.py --repo . --perfil ftmo-2step-swing-100k --comprobar`);
  `scripts/generar_capa.py` y `docs/validation/PREGUNTAS-7B.md` en `rutas_protegidas` no existen (el
  real es `docs/sesion-7/PREGUNTAS-7B.md`, que quedaba sin proteger); y el log de `knowledge
  validate` en la raíz, que rompe el sello. **Corregidos en el commit de esta fase 0** (y
  protegidos además `src/botsito/mql5bridge/` y `mql5/`).

### Lo que no pude medir (todavía)

- Lo que la regla nueva da en las siete sesiones declaradas, en las del bloque de la 7b y en el
  resto: se mide con la función ya escrita (F1, punto 6) y en la corrida tras F1.
- Cuántas H4 tienen cargadas las sesiones de enero de la 7b (con solo enero cargado, las primeras
  pueden tener menos de 60): punto 6 de F1.
- Si `knowledge validate` acepta supersedir `fb-2026-09-29-sesion-03-9f506366` y
  `fb-2026-09-29-sesion-03-2cff5008`, que siguen nombrados en prosa (A-13, notas de RN-014): se mide
  en cada commit de F2.
- Si la guardia deja ejecutar los guiones nuevos de la rama: `delta_julio.py` sí (medido).

### Exposiciones

Las dos filas del 2026-11-18 de `HOLDOUT-EXPOSICIONES.md` (la apertura y la fase 0; el control de
D0): `make check` (marzo para calentar, como todos) y la corrida de julio, que calienta con junio.
Nada más: ningún fotograma, ninguna transcripción ni filtrada, ningún libro, ningún caso.

### Lo que necesito que decidas

0. **Las herencias de la 7b que el encargo pasa a la rama siguiente** (0.5, filas 1 a 4). Opciones:
   (a) listarlas en «Para la rama siguiente» y preparar la línea de la F que las nombre; (b) hacer
   aquí la revisión de las filas de la 7b. Recomiendo (a): el encargo lo decide así y las láminas
   tienen que salir del motor cerrado. Coste de (b): una corrida de enero y abril que el encargo no
   autoriza.
1. **ADR-0061 §3-§5** («al tocar», `mecha`), que el encargo no lista. Opciones: (a) un recuadro
   fechado en ADR-0061, en el commit de F2 que mueve el motor, ampliando el contrato en ese commit;
   (b) solo el recuadro de ADR-0065, que remite a ADR-0061. Recomiendo (a): un ADR que dice lo
   contrario del motor sin recuadro es la deuda G.2 que ya se pagó en ADR-0044. Coste de (b): ADR-0061
   queda viejo. **Lo aplico con (a)** salvo que digas otra cosa; es un recuadro, el cuerpo no se toca.
2. **M de la Next Action** (el break even de una venta por el ASK, ADR-0065 §6). Opciones: (a) el
   recuadro de ADR-0065 dice que con `cierre` no hay vigilancia al tick y M queda sin objeto mientras
   lo sea, y se prepara la línea de M para la orden de cierre; (b) no tocar M. Recomiendo (a). Coste
   de (b): una entrada de la Next Action que ya no describe al motor.
3. **El visor** (Technical Debt de las H4 saltadas). Opciones: (a) el visor dice el rango vigente
   (su alto, su bajo y la H4 que lo fijó) y deja de deducir la H4 que decide por `velas_miradas`;
   la deuda de enseñar las saltadas sigue; (b) además, pagar la deuda. Recomiendo (a): el encargo
   pide coherencia, no la mejora. Coste de (b): más código de visor sin pedirlo.
4. **El significado de los campos de `ResultadoSesgo`** con la regla nueva (0.3). Opciones: (a) el
   de 0.3 (`velas_miradas` cuenta las H4 comparadas con el rango; las saltadas, las que rompieron el
   rango sin decidir después de la que lo fijó; tres campos nuevos de registro para el rango); (b)
   conservar `velas_miradas` como distancia de la última cerrada a la que fija. Recomiendo (a):
   (b) le da un nombre de búsqueda hacia atrás a un recorrido hacia delante. Coste de (a): el visor
   cambia de lector (decisión 3).

5. **F1 no cumple (iv) en julio** (F1.4): 2026-07-01 de 11 a 15 gana una P1 (la venta del trader
   de las 12:59 en Madrid) porque el bot pasa a alcista con el rango de la mañana; la voz del
   trader en esa sesión dice alcista y la pantalla una venta. (i), (ii), (iii) y el punto 6, sí.
   Opciones: (a) dar F1 por bueno tal como está, con esa fila como la contradicción voz-pantalla
   que VIDEO-JULIO.md ya dejaba «a preguntar solo si se repite», y llevarla a la 7b (¿qué lado
   tenía tu rango el 1 de julio a las 11, y por qué vendes a las 12:59?); (b) revertir F1 hasta
   la 7b. Recomiendo (a): la regla es lo que el trader dijo en el bloque técnico, las siete
   sesiones declaradas casan, y la única fila que no casa es una en que su voz y su operación se
   contradicen. Coste de (b): vuelven las 20 P1 y las 10 P5 del otro lado. **El código de F1
   queda commiteado y no se retoca hasta tu respuesta.**

**Cómo sigue la rama sin respuesta** (la PARADA es condicional): F1 y F2 cuadran en lo que la fase 0
puede medir (A-1 y A-4 con nota y sin REOPEN; con `cierre` y `cuerpo` el motor pide que la M1 cierre
más allá del extremo de la zona posterior). F1 se juzga además con las filas declaradas y el punto 6,
que se miden después de escribir la función. Sigo con F1, F2 y F3 y con las recomendaciones de
arriba.

## F1 · S-1, el sesgo de H4 por el rango vigente (ADR-0094)

**Commit** `feat(sesgo): el sesgo de H4 es el del rango vigente (S-1 de la 7a, ADR-0094)`, con su
`make check` sellado (3532 passed, 6 xfailed). El primero salió en rojo con un fallo:
`test_registro.py::test_fichero_real_cada_valor_de_estrategia_cita_al_trader` (un parámetro de
`estrategia` no puede tener por fuente una decisión); la fuente de `sesgo_h4_rango_nuevo` pasó a ser
lo que el trader sí dijo, en parte (`ev-v18-000822-57145b90`), y la lectura del consultor la nombra
`consumido_por: [ADR-0094]` (como `liquidez_m15_mecha_que_vuelve`, cuya fuente es un ítem).

### F1.1 Lo que se hizo

- **Registro**: `fb-2026-11-16-sesion-07-33fdaa6c`, CORRECT sobre RN-003 con
  `ev-v18-000249-bb7b1c07` (`--fecha 2026-11-16`, `--recibido-el 2026-11-16`, `trader_grabado`,
  vídeo, v18 0:02:49-0:02:56), sin `supersede`, como `31fb311f`, `ca0afae6` y `6e7da456`.
  `feedback new` creó la carpeta `knowledge/feedback/2026-11-16-sesion-07/` (verificado: no
  existía). `feedback pending` lista ahora como «pendientes» los tres CORRECT anteriores sobre
  RN-003 («RN-003 no lo cita todavia»): la regla solo refleja el registro que cita
  (`cli.py:2064-2075`), y en `main` ya pasaba con dos de ellos (RN-003 citaba solo `6e7da456`); no
  es nuevo ni se arregla aquí.
- **Spec** (spec 18.6.4 → 19.0.0, mayor: la regla cambia de sentido, como ADR-0080): RN-003 (título,
  `entonces`, `cita`, `literal`, forma con `que: vela_h4_cerrada`, `contra: rango_h4_vigente` y
  `rango_nuevo: sesgo_h4_rango_nuevo`, y un párrafo al frente de sus notas, que se conservan); el
  predicado `sesgo_h4_al_abrir` (descripción, argumentos, `cita`, `literal`); dos tokens nuevos y
  una línea en los dos viejos (ya ninguna forma los nombra); las notas de RN-033 y el token
  `insuficiente`; `sesgo_h4_rango_nuevo` (nuevo, DEFAULT_AMBIGUOUS en
  `vela_que_rompe_con_su_color`, opciones esa y `otra`, que el motor niega con nombre); las
  descripciones de `sesgo_h4_regla` y `sesgo_h4_tope_velas`. `sesgo_h4_criterio_ruptura` no
  cambia.
- **A-58** (nueva, `pregunta`, no bloqueante, `resuelve_en: [F18]`), con la búsqueda en el corpus
  escrita en su `pregunta` (la deuda de Technical Debt): «nuevo rango» como frase, «actualiz» y
  «rango», «rango» y «mitig» por prefijo; evidencia `ev-v18-000822-57145b90`,
  `ev-v18-011054-fbf8e9ae` y `ev-v11-000038-fef9789d`. Su fila en la tabla Known Ambiguities.
- **A-1**: una NOTA al frente de su `pregunta`, sin REOPEN (0.3).
- **ADR-0094**, su fila del índice y recuadros fechados en ADR-0044, ADR-0060, ADR-0075 y ADR-0080
  (el cuerpo no se toca). ADR-0094 salió del bloque `ids-inexistentes` del encargo, y el bloque con
  él.
- **Motor** (`domain/sesgo.py`): la regla a) a e); `ResultadoSesgo` gana `rango_alto`, `rango_bajo`
  y `rango_vela` (solo registro), con el significado de cada campo de 0.3 (decisión 4, opción a).
  `engine/primitivas.py`: el sujeto nuevo, el argumento `rango_nuevo` y la anotación
  `sesgo_h4_rango` (`alto:bajo:inicio`, solo registro). El arnés no cambia: la línea «Por sesion»
  sigue igual (la lee `patrones.py`, medido en la corrida de abajo).
- **Visor** (decisión 3, opción a): toma la H4 que fija el lado y la del rango del resultado (ya no
  las deduce por `velas_miradas`), y dice «el rango vigente es la H4 que abre a las HH:MM (alto, bajo,
  en puntos)», o «la del arranque, sin lado». La deuda de enseñar las saltadas sigue.
- **Láminas**: las frases del sesgo dicen el rango vigente en el idioma del trader («el rango es la
  vela H4 que rompió por arriba el rango anterior y cerró verde, y nadie lo ha roto después cerrando
  de su color»), una frase nueva con la hora, el alto y el bajo del rango, las saltadas como «Después,
  N velas H4 rompieron el rango y cerraron del color contrario: el rango no cambia», y «La vela H4
  que es el rango viene de antes de la ventana» cuando nace antes del panel. El panel de H4 dibuja el
  alto y el bajo del rango. Con lado, el rango anotado tiene que ser la H4 que fija el sesgo, o
  `LaminaError`. No se generó ninguna lámina.

### F1.2 Los tests, antes que el código (ADR-0093 §4)

- **Sintéticos de a) a e)**, `tests/unit/test_sesgo_rango.py` (15). Contra el código de `main` (el
  `src/` de la rama era idéntico al de `main` al correrlos: `git diff main --stat -- src tests
  knowledge` vacío): 11 fallan. Los que deciden el lado fallan por la aserción, no por un atributo:
  `test_a_la_roja_que_rompe_solo_a_su_anterior_dentro_del_rango_no_cambia_el_lado` (main: BAJISTA),
  `test_a_al_reves_en_un_rango_bajista` (main: ALCISTA) y
  `test_b_el_rango_nuevo_manda_para_las_siguientes` (main: ALCISTA); los demás, por los campos
  nuevos.
- **Por el camino real**, `tests/unit/test_sesgo_rango_real.py`: las H4 que recibe el motor
  (`arnes.dias_de_mercado`, por la compuerta) y los parámetros del registro, el 2026-07-07 y el
  2026-07-15 de 11 a 15 dan ALCISTA. Contra `main`, con una copia temporal adaptada a su firma (sin el
  quinto argumento, que en `main` no existe; borrada después y nunca commiteada): los dos fallan con
  `assert <Sesgo.BAJISTA> is <Sesgo.ALCISTA>`. Con la regla nueva, pasan.
- **Cambian de sentido A PROPÓSITO**: ocho de `test_sesgo_h4.py` (seis por `velas_miradas`, que ahora
  cuenta las H4 comparadas con el rango; `test_rompe_arriba_y_cierra_verde_es_alcista`, porque la
  ruptura se mide contra el rango; `test_rompe_abajo_y_cierra_roja_es_bajista`, que gana el caso a);
  y `test_varias_seguidas…`, cuya última vela rompía el alto del rango y cerraba verde); dos de
  `test_laminas_registro.py`, que comparaban con una copia literal del `sesgo_h4` de `main` y ahora
  comprueban que el registro cuadra con la regla del rango (`_cuadra`); y las dos frases de
  `test_laminas_svg.py`. Nuevos: dos de láminas (el panel dibuja el rango; un rango que no es la H4
  que fija se niega) y la anotación del rango en el test de las dos evaluaciones.

### F1.3 El arranque (punto 6), con la función ya escrita y antes de la corrida

`anexos/ACTIVAR-SESION-07/arranque.py 60 120` → `arranque-60-120.txt` (fila de HOLDOUT antes):

| mes | sesiones | cambian de lado | < 60 H4 cargadas | < 120 H4 cargadas | INSUFICIENTE con 60 | con 120 |
|---|---|---|---|---|---|---|
| 2026-01 | 42 | 0 | 20 | 40 | 1 | 1 |
| 2026-04 | 42 | 0 | 0 | 0 | 0 | 0 |
| 2026-07 | 26 | 0 | 0 | 0 | 0 | 0 |
| 2026-08 | 42 | 0 | 0 | 0 | 0 | 0 |
| total | 152 | **0** | 20 | 40 | 1 | 1 |

**Ninguna sesión de construcción cambia de lado entre 60 y 120.** La reserva: en enero (que solo
carga el suyo) 20 sesiones tienen menos de 60 H4 cargadas y 40 menos de 120; en ellas los dos topes
arrancan en la misma primera vela cargada, así que la comparación no mide su dependencia del
historial: **es la dependencia de ADR-0060, y para esas 20 no se puede medir sin descargar diciembre
de 2025**, que el encargo no autoriza. Una sesión de enero queda INSUFICIENTE con los dos topes.

Una por una (todas de construcción): las siete declaradas, con 134 a 207 H4 cargadas, dan **alcista**
(07-01 07-11, 07-06 07-11, 07-06 11-15, 07-07 07-11, 07-07 11-15, 07-15 11-15) y **bajista** (07-17
11-15), con 60 y con 120: ninguna depende del arranque. Las siete del bloque de la 7b: 2026-01-13
07-11 (44 cargadas) bajista; 2026-04-15 11-15 (195) alcista; **2026-01-07 07-11 (20 cargadas)**
bajista; 2026-01-19 11-15 (69) alcista; 2026-01-21 07-11 (80) bajista; 2026-01-22 11-15 (87)
bajista; 2026-07-16 07-11 (200) alcista. **El 01-07 y el 01-13 tienen menos de 60**: su sesgo sale
del rango que arranca en la primera H4 de enero, y depende del historial cargado sin que se pueda
medir aquí (para la rama siguiente).

### F1.4 La corrida de julio tras F1 (D0, etiqueta `f1`)

Las tres órdenes de D0 sobre el código commiteado de F1 (fila de HOLDOUT antes):
`pivote-julio-f1.txt` y `delta-julio-base-f1.txt` en los anexos.

| | base | f1 | delta |
|---|---|---|---|
| T0 (parejas) | 14 | 14 | **0** |
| P5 + P6 en sesión (operaciones de más) | 39 | 24 | **−15** |
| P1 | 20 | 1 | −19 |
| P5 del otro lado | 10 | 2 | −8 |
| P4 | 1 | 17 | +16 |
| T0 + P2 + P3 + P7 | 46 | 49 | +3 |

**El rn003 cambia en 8 sesiones de julio**: las siete declaradas (las seis a alcista, la 07-17 11-15
a bajista) y **07-01 11-15** (bajista → alcista), que no estaba declarada.

**Las filas declaradas, contra lo que CASA:**

- **(i) CUMPLE**: el rn003 de las siete sesiones es el lado del trader.
- **(ii) CUMPLE**: ninguna de las 20 filas del trader sigue en P1: pasan a T0 (5: 07-06 06:22 y
  10:11, 07-07 05:02, 10:01 y 11:57), P2 (4), P3 (5), P7 (1) y P4 (5: las cuatro de 07-15 11-15 y la
  de 07-17 11-15).
- **(iii) CUMPLE**: las 10 P5 del otro lado desaparecen (07-01 07-11 ×3, 07-07 07-11 ×1, 07-07 11-15
  ×5, 07-15 11-15 ×1).
- **(iv) NO CUMPLE**: **2026-07-01 de 11 a 15 gana una P1 que hoy no tiene**: la venta del trader de
  las 10:59:05 UTC (12:59 en Madrid), que era P2 (7 puntos de la venta del bot), con el sesgo del bot
  ahora alcista. Y dos P5 del otro lado nuevas en la misma sesión (compras del bot de las 09:25 y
  11:53 UTC). Lo que hay que saber para leerla (VIDEO-JULIO.md §4.1, :604): en esa sesión **la voz
  del trader dice alcista** («Como todavía no se ha roto nuestro rango, entonces nosotros todavía nos
  planteamos traer alcistas […] nos enfocamos en buscar 3 alcistas», v11 0:05:44-0:06:09) **y en
  pantalla vende**; VIDEO-JULIO.md la dejó «sin clase: la voz dice compras y la pantalla una venta: a
  preguntar solo si se repite». El bot de F1 dice lo que dice la voz.
- **El punto 6**: ninguna de las siete depende del arranque.

**PARADA de F1, por (iv)** (abajo, «Lo que necesito que decidas», punto 5). **La regla no se retoca.**
El código de F1 queda commiteado; F2 y F3 siguen.

**Las 14 parejas de la línea base** (`motor decisiones --bitacora 2026-07-03,2026-07-14` sobre el
código de F1, en `data/activar-sesion-07/decisiones-f1/`): **9 siguen** y **5 dejan de serlo**, y
las cinco por un freno de la cuenta del mes, de rebote, no por el sesgo (el rn003 de esas sesiones no
cambia):

| Pareja de la base | Ahora | Causa |
|---|---|---|
| 2026-07-03 07-11, compra 07:43 UTC | P3 | **RN-036** (la racha de pérdidas seguidas, que la cuenta arrastra entre días; ADR-0077) prohíbe abrir desde las 07:24 UTC; en la base no la prohibía en esa sesión (el bot compró a las 07:24 y a las 07:35): la cuenta del mes cambia desde el 07-01 |
| 2026-07-14 11-15, compra 10:33 UTC | P3 | **RN-032** (la lectura prospectiva del límite total) prohíbe abrir desde las 09:24 UTC |
| 2026-07-15 07-11, compra 05:06 UTC | P4 | **RN-032**: desde el 07-15 el bot no abre (su saldo queda en 90.908,38 desde el cierre del 07-14) |
| 2026-07-16 07-11, compra 06:00 UTC | P4 | RN-032, igual |
| 2026-07-17 07-11, venta 05:46 UTC | P4 | RN-032, igual |

Las P4 nuevas (16) son las operaciones del trader del 07-15 al 07-17 (y la de 07-03 11-15), sin
ninguna orden del bot por esos frenos. **Cuántas de las 20 pasan a pareja: 5** (no se declaró
mínimo; a la tasa de la línea base serían unas 6). Ningún parámetro se elige por estas cifras
(ADR-0093 §4).

## F2 · S-2, el break even al cierre y con cuerpo (A-13)

**CUADRA (0.4)**: el nivel de RN-014 es el extremo de la zona de control posterior a la entrada
(ADR-0061 §4) y, con `cierre` y `cuerpo`, el motor pide que una M1 CIERRE más allá de ese nivel y
mueve el stop en ese cierre (ADR-0065 §5). No falta código. **Desviación declarada** de «en parte no
se cierra» (encargo): la fila S-2 está «en parte» por «otra» (§6:769) y se activa lo que el trader
dijo como regla general en el bloque técnico; el margen, otra fila «en parte» (§6:771), no se activa.
El precedente es `toma_antes_de_la_ventana` (sesión 4).

### F2.0 El caso real y los tests, antes que los registros

**Los `stop_movido` de julio en la línea base**: 18 (los «100 frente a 247» del encargo son de toda
la construcción; en julio, 18 frente a 53). Para cada uno, con las M1 de julio (un guion de
diagnóstico en la carpeta de trabajo, fuera del repo, que solo lee las M1 y la salida base), el
nivel de la zona posterior y si la M1 del toque cierra más allá: **11 cierran más allá y 7 no**
(2026-07-03 o5, o11 y o15; 2026-07-07 o11 y o22; 2026-07-13 o13; 2026-07-16 o12). Elegido
**2026-07-16, sesión de 11 a 15, compra o12** (llenada a las 09:35:57 UTC, stop movido a las
09:39:10 UTC): el nivel es 1.14634 y la M1 de las 09:39 cierra en 1.14629. No es la reserva de la 7b
(2026-07-16 de 7 a 11) ni un día del rango de H4 que F1 cambia.

`tests/unit/test_break_even_cierre.py`: el registro dice `cierre` y `cuerpo`; sintéticos en compra y
en venta (la M1 que pasa el nivel con la mecha y cierra sin pasarlo no rompe la zona; la que cierra
con cuerpo más allá, sí, en esa vela); y el camino real sobre las M1 del 2026-07-16 (con `mecha` la
zona se rompía en la M1 del toque; con el criterio del registro, no). **Contra los parámetros de
`main`** (el `src/` de la rama no cambia en F2; corridos antes del primer registro): **los cuatro
fallan por la aserción** (`'tocar' == 'cierre'`; `3 is None` en compra y en venta; `4 != 4` en el
real). Entra en el commit del criterio, cuando el registro ya lo cumple.

### F2.1 `break_even_condicion` → `cierre`

`fb-2026-11-16-sesion-07-828031df`, CORRECT con `supersede` de `fb-2026-09-09-sesion-01-0ccafcba`,
con `ev-v18-001327-70f1d014` (v18 0:13:27-0:13:45; «nosotros esperamos a que cierre la vela y si
cierra por debajo no vamos a poder»); `feedback apply --check` proponía solo ese parámetro, y
`feedback apply` lo escribió. La descripción dice el valor nuevo, que la excepción del imbalance
queda descartada por el trader (`ev-v18-001145-901d8aa0`) y que el margen no se activa. spec
19.0.0 → 19.0.1. **Cambian de sentido A PROPÓSITO**: `test_be_al_tick.py` (el registro real es
`cierre`; `tocar` se prueba con una copia reescrita) y
`test_cableado.py::test_rn014_pone_el_stop_en_la_entrada_al_completarse_la_zona_posterior` (el del
mecanismo al tick de ADR-0065, que se corre con `tocar` y `mecha` en una copia del registro:
`registro_con_valores`).

### F2.2 `break_even_criterio_ruptura` → `cuerpo`

`fb-2026-11-16-sesion-07-a094ab28`, CORRECT con `supersede` de `fb-2026-09-29-sesion-03-2cff5008`,
con `ev-v18-001327-70f1d014` («la entrada tiene que cerrar por encima de su nivel alto de su de su
máximo nivel para nosotros pues poder poner en break even»); `feedback apply --check` proponía solo
ese cambio (el de F2.1, «ya estaba»). La descripción dice el valor nuevo, la excepción del imbalance
descartada y el margen sin activar, y lo que decía de A-13 («sigue ABIERTA solo por el corte de
audio») pasa a pasado. spec 19.0.1 → 19.0.2. Entra `tests/unit/test_break_even_cierre.py` (F2.0),
que ya pasa. **Cambia A PROPÓSITO**: el ayudante de `test_be_al_tick.py` prueba `tocar` con `mecha`
(el par de ADR-0065: un cuerpo no se ve en un tick), en una copia del registro.

### F2.3 La regla RN-014, A-4, A-13 y los recuadros

`fb-2026-11-16-sesion-07-223a2951`, CORRECT sobre RN-014 con `supersede` de
`fb-2026-09-29-sesion-03-9f506366`, con `ev-v18-001900-1581efbe` (v18 0:19:00-0:19:14; «pasas el stop
de la entrada cuando se se desarrolla una zona de control completamente validada», y en una venta al
revés). RN-014: su `cita`, su `literal` (era «apenas toca, pues se pone en B la entrada») y su
`entonces` (decía «en el instante del toque»: ahora, «cuando la zona de control posterior queda
validada», con los dos parámetros), y un párrafo al frente de sus notas; la forma no cambia (ya
nombraba los dos parámetros). spec 19.0.2 → 19.0.3.

- **A-4** (RESUELTA): una NOTA al frente de su `pregunta`, sin REOPEN (0.4): su RESOLVE_UNKNOWN sigue
  activo como lo que el trader dijo en la sesión 1; los parámetros los corrigen los CORRECT.
- **A-13** (ABIERTA): su `pregunta` dice qué se respondió en la 7a y que **sigue ABIERTA solo por el
  margen**, con la pregunta reformulada para la 7b.
- **Recuadros fechados** en ADR-0065 (el break even va por §5; **§6, M de la Next Action, queda sin
  objeto mientras la condición sea `cierre`**: decisión 2, opción a) y en **ADR-0061** (decisión 1,
  opción a): `contrato.yaml` se amplió en este commit con `docs/adr/0061-*.md`, con su motivo en un
  comentario; **desviación declarada** del contrato del encargo.
- `knowledge validate` acepta las citas en prosa de los tres registros supersedidos (A-13, notas de
  RN-014 y descripciones de los parámetros): lo que G1 niega son las citas en campos de fuente.

## Estado

EN CURSO: fase 0 y F1 commiteadas (F1 en PARADA por la condición (iv), punto 5 de las decisiones); siguen F2 y F3.
