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

**Cómo sigue la rama sin respuesta** (la PARADA es condicional): F1 y F2 cuadran en lo que la fase 0
puede medir (A-1 y A-4 con nota y sin REOPEN; con `cierre` y `cuerpo` el motor pide que la M1 cierre
más allá del extremo de la zona posterior). F1 se juzga además con las filas declaradas y el punto 6,
que se miden después de escribir la función. Sigo con F1, F2 y F3 y con las recomendaciones de
arriba.

## Estado

EN CURSO: fase 0 escrita y commiteada; siguen F1, F2 y F3.
