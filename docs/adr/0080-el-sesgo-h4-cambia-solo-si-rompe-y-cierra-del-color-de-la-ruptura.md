---
status: ACTIVE
date: 2026-10-17
phase: post-F14 (rama `trabajo/sesgo-h4-color`, R1.2 de la hoja de ruta)
---

# 0080 · El sesgo de H4 cambia solo si la vela rompe el extremo de la anterior y cierra del color de esa ruptura (enmienda ADR-0044 §2, ADR-0060 §1 y ADR-0075 §3)

> Decisiones del consultor del 2026-10-17 (encargo de `trabajo/sesgo-h4-color`, D1-D7, y su
> respuesta a la PARADA de la fase 0, `docs/validation/SESGO-H4-COLOR.md` §1.l). Lo dijo el trader
> por WhatsApp el 2026-10-14, en respuesta a la pregunta P1 de R3.1
> (`CORRIDA-CONSTRUCCION.md` §4.5): `fb-2026-10-04-sesion-04-6e7da456` (CORRECT sobre RN-003) y
> `fb-2026-10-04-sesion-04-d2e84172` (CONFIRM de `sesgo_h4_criterio_ruptura`). **Enmienda
> ADR-0044 §2 y su alternativa descartada, ADR-0060 §1 y ADR-0075 §3** (recuadro en cada uno y
> fila del índice).

## Decision

### 1. La regla

Una H4 cambia el sesgo solo si **rompe el extremo de la anterior** -con mecha o con cuerpo- **y
cierra del color de esa ruptura**. Rompe el bajo y cierra roja: bajista. Rompe el máximo y cierra
verde: alcista. Rompe un extremo y cierra del color contrario: no cambia, sigue el sesgo que
había. Es lo que el trader escribió a las 14:55 (hora de Lima) del 2026-10-14 -«Para el cambio de
sesgo, por ejemplo en el caso 1 la vela roja debe de haber roto con cuerpo o con mecha el bajo de
la vela alcista» y «Y terminar al cierre bajista»- y lo que confirmó a las 15:18 («Si, esta bien
bro») sobre el esquema de cuatro casos dibujado por el consultor (casos 1 y 2, cambia; 3 y 4,
sigue el que había). La primera respuesta, a las 14:45: «Dependerá de si cierra alcista o bajista
si lo hace con mecha o con cuerpo es válido para un cambio de sesgo». Las capturas y los dos
esquemas están en el corpus (`fuentes.yaml`, «Mensajes del trader»); los literales los transcribió
el consultor y los volvió a leer contra las capturas el 2026-10-17, y la sesión no abre ninguna
(ADR-0038).

### 2. D1 · Ruptura simple con el color contrario: la vela NO decide y la búsqueda sigue

La H4 que rompe un extremo y cierra del color contrario no fija nada: la búsqueda hacia atrás de
ADR-0044 §2 la salta y sigue en la H4 anterior, igual que hoy la neutra de doble ruptura
(ADR-0075). Es lo que dice el esquema confirmado: «sigue el sesgo que había». Si ninguna H4 del
tope fijó el sesgo, `insuficiente` (ADR-0044 §2, ADR-0060 §3): desde este ADR `insuficiente` sale
también cuando todas las rupturas del tope cerraron del color contrario o sin cuerpo (RN-033,
notas; el token lo dice).

### 3. D2 · Doble ruptura: el resultado no cambia

ADR-0060 §1 (la vela que rompe los dos extremos toma el lado de su color) y la neutra de ADR-0075
(no decide, la búsqueda sigue) ya son casos de la regla de §1.

### 4. D3 · Ruptura simple con una vela SIN CUERPO: decisión del consultor, no decide

El trader no describió la vela que rompe un extremo y cierra exactamente donde abrió. Decisión del
consultor: no decide y la búsqueda sigue, porque la regla pide cerrar del color de la ruptura y
una neutra no tiene color; es la lectura de S-13 (ADR-0075), con su reserva: el trader la dijo
solo con un sesgo previo alcista. **Va como pregunta de confirmación a la sesión 5** (lista «Para
el cuestionario de la sesión 5» de `SESGO-H4-COLOR.md`).

> **CONFIRMADO POR EL TRADER el 2026-10-23 (sesión 5, S-2, sobre un esquema dibujado; recuadro del
> 2026-10-26, `trabajo/activar-sesion-05`, que no reescribe el cuerpo).** «Sigue el sesgo que
> había … la respuesta es la B» (`ev-v15-000256-f3c52278`; `fb-2026-10-23-sesion-05-85ce7ba5`,
> CONFIRM sobre RN-003): la ruptura simple de una vela sin cuerpo no decide y la búsqueda sigue, y
> lo lejos que llegue la mecha es indiferente. D3 deja de ser una decisión provisional del
> consultor. Reserva: la subpregunta del caso al revés (sesgo bajista) se leyó y el trader volvió al
> ejemplo alcista; la regla que dio, «sigue el sesgo que había», cubre los dos lados, pero el caso
> bajista no lo dijo con sus palabras.

### 5. D4 · El extremo es el máximo o el mínimo, y romperlo con mecha o con cuerpo es superarlo con la mecha

La línea discontinua del esquema está en la mecha: el extremo de la anterior es su máximo o su
mínimo, y «con cuerpo o con mecha» equivale a superarlo con la mecha. `sesgo_h4_criterio_ruptura`
se queda en `mecha` y CONFIRMED, con fuente `fb-2026-10-04-sesion-04-d2e84172` (resuelve lo que
`CORRIDA-CONSTRUCCION.md` §4.7, punto 4.b, dejó a esta rama). Lo sostiene el WhatsApp de las 14:45
y lo que el trader ya había dicho de la mecha en voz: `fb-2026-09-09-sesion-01-41f46b21` (el
registro que cierra A-1: «o bien, con una mecha [...] la siguiente operativa [...] sería alcista»),
`ev-v9-001312-19e45e4a` («se ha llegado a romper con mecha, con una mecha base inclusive con un
pip») y `ev-v9-000902-25db5bf5` («con mecha o con cuerpo por debajo de esta vela que es nuestro
rango»). No se justifica con la idea de que «mecha» fuera solo una re-expresión del consultor: lo
inexacto de esa idea es que el trader no lo hubiera dicho nunca. Y la lección de
`ERRORES-RECURRENTES.md` (fila de `trabajo/corrida-construccion`: una re-expresión canónica que
añade un criterio que el literal no trae va como DEFAULT_AMBIGUOUS) sigue en pie y no aplica aquí:
el literal de `fb-2026-09-09-sesion-01-8eccf5c0` no decía mecha, y por eso aquel CONFIRMED era
prematuro; lo que lo confirma ahora es que el criterio lo dijo el trader, en voz y por escrito.

### 6. D5 · La exigencia del color no es un parámetro ni un interruptor

Es la definición del trader, como el color de la doble ruptura en ADR-0060: no nace ningún
parámetro ni ninguna opción de diagnóstico. La comparación con lo de antes se hace contra las
salidas commiteadas de R3.1 (`docs/validation/anexos/CORRIDA-CONSTRUCCION/`), en la re-corrida de
la fase 4 de la rama, que es diagnóstico (ADR-0070 §3): no decide ningún parámetro, no habilita
mayo y no mide cobertura contra ningún umbral.

### 7. D6 · Lo que enmienda

- **ADR-0044 §2**, «la última H4 que rompió un extremo de su anterior»: que rompió un extremo Y
  cerró del color de esa ruptura. Y su alternativa descartada «ante una ruptura doble, tomar el
  sentido del cierre», descartada porque «el color de la vela NO decide»: hoy el color sí cuenta,
  pero no el sentido del cierre a secas, sino la ruptura Y el color. El recuadro de ADR-0044 dice
  también que su §1 («doble ruptura = AMBIGUO») ya lo enmendaron ADR-0060 §1 y ADR-0075 sin poner
  recuadro allí (deuda G.2 de la hoja de ruta; respuesta del consultor, punto 7).
- **ADR-0060 §1**, «Con un solo extremo roto, el color sigue sin decidir nada»: sustituido.
- **ADR-0075 §3**, «con un solo extremo roto el color no decide»: sustituido.
- Ningún otro ADR lo contradice (medido en la fase 0: `grep` de «color … no decide» en `docs/adr`,
  `docs/runbooks`, `CLAUDE.md`, `docs/plan` y `knowledge/spec`).

### 8. D7 · El feedback y lo que cita cada sitio

Dos registros nuevos, los dos `trader_escrito`, `medio escrito`, `recibido_el 2026-10-14`, en la
carpeta `2026-10-04-sesion-04` (`fecha 2026-10-04`), por el precedente de A-42
(`ACTIVACION-A42.md` §6.1, D1) y porque el formato de `sesion` no admite otra cosa sin inventar
una sesión (respuesta del consultor, punto 1): el CORRECT sobre RN-003
(`fb-2026-10-04-sesion-04-6e7da456`; precedente, `fb-2026-10-04-sesion-04-ca0afae6`) y el CONFIRM
sobre `sesgo_h4_criterio_ruptura` con valor `mecha` (`fb-2026-10-04-sesion-04-d2e84172`), aplicado
con `feedback apply` (su fuente). Ninguno supersede a `fb-2026-09-09-sesion-01-8eccf5c0`, que
tiene cinco citas en `knowledge/spec/` y G1 de `knowledge validate` las negaría.

- RN-003 y el predicado `sesgo_h4_al_abrir` citan el CORRECT; `sesgo_h4_criterio_ruptura`, el
  CONFIRM.
- El término `equal` conserva `8eccf5c0` (lo que sostiene, que un equal no rompe, no cambia) y su
  definición gana «y cerrar del color de esa ruptura» (punto 2 de la respuesta).
- `rompe` se queda como está: ninguna regla lo invoca (`strategy_spec.yaml`, notas del predicado).
- `sesgo_h4_regla` (que ninguna forma lee desde F12) no se borra: solo su descripción dice que la
  regla vigente es la de este ADR.
- RN-033: una línea en sus notas y en la descripción del token `insuficiente` (§2); forma, cita y
  `cuando` no cambian (punto 3 de la respuesta).

### 9. La contradicción abierta con la sesión 1, y A-1

En la sesión 1 (v6 1:04:30-1:05:35, 2026-09-09; el tramo que cita
`fb-2026-09-09-sesion-01-41f46b21`), con un sesgo previo bajista, el trader dijo de una H4 que
rompió por encima con la mecha y cerró roja: «terminó bajista vale pero todo su movimiento como
tal su mecha fue alcista entonces buscaríamos nosotros ... operativa alcista» y «aunque fue roja la
vela, pues es indiferente, eso, entonces la siguiente operativa es alcista». Es el caso 3 del
esquema con el resultado contrario, y es lo que recogían las notas de `41f46b21` («el criterio es
la ruptura del extremo, no el color ni el cierre») y las de RN-003 («una vela que cierra roja pero
cuya mecha rompio por encima deja el sesgo alcista»). Decisión del consultor (respuesta, punto 0):

- **Se activa la regla del WhatsApp**: es la respuesta escrita a la pregunta exacta, cinco semanas
  posterior a la sesión 1, y el trader confirmó el caso 3 a propósito. Las notas de `41f46b21`
  quedan contradichas por el WhatsApp; **la contradicción queda ABIERTA y a la vista** (aquí, en
  las notas de RN-003 y en las del CORRECT), y va a la sesión 5 **con un esquema dibujado, nunca
  con los fotogramas de v6 ni con los instantes de ese gráfico**: lo que el trader enseña ahí es su
  sesgo sobre velas en directo de días de `fidelidad-1`, y enseñárselo sería pedirle una etiqueta
  (punto 0bis; `HOLDOUT-EXPOSICIONES.md`, fila del 2026-10-17).
- **Sin ítems de evidencia nuevos** (opción (b) de la PARADA): se midió en memoria que un ítem que
  supersediera a `ev-v3-011045-a185d2ba` rompe G1 en la lista de evidencia de A-1
  (`ambiguedades.yaml`), y un ítem de v6 solo no abre nada en `evidence contradictions` porque el
  viejo no tiene `valor` (`SESGO-H4-COLOR.md` §2.1). El detector no la ve; la cierra la sesión 5.
- **A-1 no se reabre** (punto 6): su pregunta -qué vela fija el sesgo y cuándo cambia- sigue
  contestada por `41f46b21` (la H4 previa; cambia cuando rompe el extremo, y basta la mecha); lo
  que cambia es la condición del cierre, que entra por el CORRECT sobre RN-003, como ADR-0060 y
  ADR-0075 cambiaron la regla sin reabrir A-1 ni A-34. Reabrirla quitaría el registro que sostiene
  `mecha`.

> **CONTRADICCIÓN CERRADA el 2026-10-23 (sesión 5, S-1, con el esquema dibujado; recuadro del
> 2026-10-26, `trabajo/activar-sesion-05`, que no reescribe el cuerpo).** Con el sesgo bajista y
> una H4 que rompe el máximo de la anterior solo con la mecha y cierra roja, el trader dijo «sigue
> bajista, claramente … como cierra bajista, pues sigue siendo bajista» (`ev-v15-000049-3b294480`;
> `fb-2026-10-23-sesion-05-af24c935`, CONFIRM sobre RN-003): es el caso 3 de la regla del color, y
> va con el WhatsApp y contra la sesión 1. Añadió que lo lejos que llegue la mecha y el tamaño del
> cuerpo no importan, y que el sesgo se decide al cierre de esa vela y no se cambia durante la
> siguiente (`ev-v15-000138-ef123dfc`). Lo que recogían las notas de `41f46b21` queda contradicho
> por dos respuestas del trader; A-1 sigue sin reabrirse (punto 6). Las notas de RN-003 lo dicen.

### 10. El motor y el arnés

- `src/botsito/domain/sesgo.py`: la ruptura de un extremo fija el sesgo solo con el color de esa
  ruptura (`cierre > abierta` para el máximo, `cierre < abierta` para el mínimo); con el color
  contrario (D1) o sin cuerpo (D3) la búsqueda sigue. `ResultadoSesgo` gana tres campos, con 0 por
  defecto: `saltadas_color_contrario`, `saltadas_neutras_simples` y `saltadas_neutras_dobles`
  (la neutra de doble ruptura de ADR-0075, que hasta hoy se saltaba sin contarse; punto 4 de la
  respuesta).
- `engine/primitivas.py`: tres anotaciones por sesión, `sesgo_h4_saltadas_color_contrario`,
  `sesgo_h4_saltadas_neutra_simple` y `sesgo_h4_saltadas_neutra_doble`, con el número como texto
  solo cuando es mayor que cero, junto a `sesgo_h4_doble_ruptura`.
- `engine/arnes.py`: «## RN-003 al abrir la sesion» gana tres líneas (sesiones con alguna H4
  saltada por cada motivo, y velas en total); ninguna fecha ni precio. Es «la anotación de 4.f»,
  lo único del arnés que cambia.
- El visor no cambia: deduce la H4 que decide por `velas_miradas`, que sigue apuntando a la que
  fijó el sesgo; enseñar las saltadas es una mejora para la rama de comprobaciones en el visor.
- Tests: `tests/unit/test_sesgo_h4.py` (los cuatro casos del esquema en los dos sentidos, la
  neutra simple, el color contrario sin nada detrás, varias seguidas, la doble ruptura sin
  cambios, con criterio `cuerpo`, sin mirar el futuro; y los siete de antes rehechos con el color
  explícito), `tests/unit/test_huecos_motor.py` (el motor anota) y `tests/unit/test_arnes_motor.py`
  (el informe cuenta). Medidos en rojo contra el código de `main` antes del motor: 16 fallan.

## Problema que resuelve

RN-003 decía que el sesgo cambia si la H4 rompe el extremo de la anterior, y que el color no
decide con un solo extremo roto. La corrida de R3.1 (`CORRIDA-CONSTRUCCION.md` §4.3-4.4) enseñó
que el literal del trader que sostenía `mecha` no decía mecha, y el patrón P1 (48 filas en 25
sesiones) pedía preguntarle. La respuesta llegó por escrito el 2026-10-14 y dice más de lo que se
preguntó: hace falta además cerrar del color de la ruptura. Sin este ADR, el motor fijaría un
sesgo con velas que el trader dice que no lo cambian.

## Alternativas consideradas

1. Un parámetro o un interruptor de diagnóstico para la exigencia del color (comparar con y sin).
2. Esperar a la sesión 5 para activar la regla, por la contradicción con la sesión 1.
3. Reabrir A-1 con un `REOPEN` y un `RESOLVE_UNKNOWN` nuevo.
4. Dos ítems de evidencia para que el detector abriera la contradicción.
5. Que la ruptura simple sin cuerpo decida por el lado de la ruptura.

## Por que elegimos esta opcion

- Es la respuesta escrita del trader a la pregunta exacta, confirmada sobre un esquema, y la más
  reciente; nada afirma más de lo que su literal sostiene (cada sitio cita el registro que lo dice).
- El criterio de la mecha lo dijo el trader en voz y por escrito: `mecha` queda CONFIRMED con una
  fuente que sí lo dice.
- La contradicción no se tapa: queda escrita donde se lee la regla y va a la sesión 5 sin exponer
  al trader ningún día reservado.

## Por que descartamos las demas

1. **Un parámetro o interruptor**: es la definición del trader, no una opción del proyecto, como el
   color en ADR-0060 (D5); la comparación la dan las salidas commiteadas de R3.1.
2. **Esperar a la sesión 5**: dejaría al motor con una regla que el trader acaba de corregir por
   escrito, y pararía W, F, V y R1.2 (punto 0 de la respuesta).
3. **Reabrir A-1**: la pregunta sigue contestada y reabrirla quitaría el registro que sostiene
   `mecha` (§9).
4. **Dos ítems de evidencia**: supersedir `ev-v3-011045` rompe G1 en la lista de A-1 y un ítem solo
   no abre nada (§9; medido).
5. **La neutra simple decide**: la regla pide cerrar del color de la ruptura y una neutra no lo
   tiene; es la lectura de S-13 (D3), y se pregunta.

## Impacto

- `knowledge/spec/strategy_spec.yaml`: RN-003 (`entonces`, `cita`, `literal`, notas), el predicado
  `sesgo_h4_al_abrir` (descripción, `cita`, `literal`), RN-033 (notas) y el token `insuficiente`.
  `glossary.yaml`: `equal`. `parametros.yaml`: la fuente de `sesgo_h4_criterio_ruptura` (por
  `feedback apply`, fase 1) y la descripción de `sesgo_h4_regla`. `spec_version` 17.0.2 → 17.0.3
  (la fuente, fase 1) → 18.0.0 (la regla cambia de sentido, como ADR-0075 subió a 16.0.0).
  `docs/spec/` regenerado. Ningún sitio nuevo con `cita`: las tres guardias de `spec/modelo.py` no
  cambian.
- El motor y el arnés (§10); el visor, los guiones de `scripts/` y los anexos cerrados no se tocan:
  si un guion cerrado diera otra cosa con el motor nuevo, el informe lo dice y la salida cerrada no
  se reescribe.
- Ningún otro parámetro ni cifra cambia (`sesgo_h4_tope_velas` sigue en 60); ni el simulador, la
  cuenta, el bróker o la geometría de M15 y M1.
- La re-corrida del arnés con los tres comandos de R3.1 (fase 4 de la rama,
  `docs/validation/anexos/SESGO-H4-COLOR/`), diagnóstico según ADR-0070 §3.
- Pregunta para la sesión 5: la ruptura simple sin cuerpo (D3) y la contradicción de §9, con un
  esquema dibujado.

## Fecha / fase

2026-10-17, rama `trabajo/sesgo-h4-color` (R1.2 de `docs/plan/HOJA-DE-RUTA.md`, W de la Next
Action).

## Estado
ACTIVE
