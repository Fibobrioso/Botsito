# Reflejar en la spec el feedback pendiente de la sesión 3

Rama `feature/reflejar-feedback-s3`, desde `main` en `5c6a89c`, el 2026-09-30. Encargo del consultor
en tres partes:
1. reflejar en la spec los 9 registros que `botsito feedback pending` daba como pendientes, sin
   cambiar ningún valor CONFIRMED sin un CORRECT, y listar como desalineación lo que exija tocar el
   motor;
2. dos retoques en `docs/sesion-4/PREGUNTAS.md`;
3. medir en los fotogramas la caja 0 → 1 de las siete ganadoras de G-2.

**No se ha tocado el motor.** Ningún valor del registro cambia. La spec pasa de 15.1.0 a **15.2.0**,
y se sube la versión menor porque RN-007 dice ahora algo que antes no decía (la vela casi plana),
aunque su forma ejecutable no cambia.

## 1. Los nueve registros: cuatro reflejados y cinco que no caben

**Cómo decide `feedback pending` que un registro está reflejado**, medido en el código
(`cli.py`, `situacion_de`): un registro sobre un parámetro está reflejado si **el parámetro lo
cita** (`fuente.id`), y uno sobre una regla si **la regla lo cita** (`cita`). **Cada parámetro y
cada regla tienen UNA sola cita.**

### 1.1 Reflejados (4)

| registro | objetivo | qué se hizo | valor |
|---|---|---|---|
| `fb-2026-09-29-sesion-03-f572f1a0` (CONFIRM) | `base_calculo_objetivo` | la fuente pasa de `ev-v2-003256-0197f4e1` a este registro: «desde el punto 0 al punto 1» | `caja_completa`, sin cambio |
| `fb-2026-09-29-sesion-03-9f506366` (CORRECT) | RN-014 | la regla cita la corrección: «apenas toca, pues se pone en B la entrada» | sin cambio |
| `fb-2026-09-29-sesion-03-3f69a5f7` (CONFIRM, G-2) | RN-015 | la regla cita «el objetivo es fijo» | sin cambio |
| `fb-2026-09-29-sesion-03-ffab23dc` (CORRECT, E-3) | RN-007 | la regla cita la corrección; el título y el `entonces` dicen ahora que una vela casi plana no cuenta y no se traza sobre ella punto de breaker | sin cambio |

**Ninguna de las citas sustituidas se queda sin dueño.** `fb-…-0ccafcba` la sigue citando
`break_even_condicion`, `fb-…-7fbbb2e7` la cita `objetivo_rr` y `fb-…-7ee9cabc` la cita
`mapeo_dos_velas`. Así que ningún registro de la sesión 1 pasa a pendiente. `feedback pending` baja
de 9 a 5 pendientes y de 79 a 83 reflejados.

### 1.2 Lo que no cabe con una sola cita (5)

**Medido antes de decidirlo.** Se cambió en una copia la fuente de `liquidez_m15_criterio_toma` para
que citara el CONFIRM de la sesión 3, y se ejecutó `feedback pending`. El registro de la sesión 3
salió de la lista y entró el de la sesión 1 (`fb-2026-09-09-sesion-01-6e15504f`, el que FIJA el
valor `cuerpo`). El pendiente cambia de registro, pero no desaparece. Se restauró el fichero.

| registro | objetivo | por qué no se refleja |
|---|---|---|
| `fb-2026-09-29-sesion-03-43e0f90e` (CONFIRM) | `liquidez_m15_criterio_toma` | el parámetro cita `fb-…-6e15504f`, que fija `cuerpo`; cambiarlo pone ese en pendiente |
| `fb-2026-09-29-sesion-03-68a21dc0` (CONFIRM) | `cartuchos_max` | cita `fb-…-1a3064b0`, que fija `3`; mismo caso |
| `fb-2026-09-29-sesion-03-d62c788a` (CONFIRM) | `lotaje_base` | cita `fb-…-17ed6193`, que fija `hasta_stop_fraccion`; mismo caso |
| `fb-2026-09-29-sesion-03-280cf8f7` (CONFIRM, G-1) | RN-015 | la única cita de RN-015 ya la ocupa G-2; las notas de la regla recogen los dos |
| `fb-2026-09-29-sesion-03-1168f036` (CORRECT, S-1) | RN-033 | **decisión del consultor al aceptar ADR-0060**: RN-033 es una guardia del proyecto y no cita este CORRECT. Lo que el trader dijo («siempre hay sesgo») lo hace ya el motor en RN-003 (el color decide la doble ruptura) |

En los cuatro CONFIRM **el valor del registro coincide con el de la spec**. No hay nada que cambiar
en el valor: lo único que falta es un sitio donde citar la confirmación.

**Propuesta, sin aplicar**, para el consultor:
- **(a) Un campo de confirmaciones.** Añadir a parámetros y reglas una lista opcional
  `confirmado_por` y que `feedback pending` dé por reflejado un CONFIRM que figure en ella. Es un
  sitio nuevo con cita, así que obliga a ampliar en el mismo commit las tres guardias de
  `spec/modelo.py`, a meter el campo en el hash y a subir la versión de la spec.
- **(b) Tratar el CONFIRM sin valor como no pendiente.** Igual que ya se hace con un CONFIRM sobre
  evidencia («confirma un ítem que ya vive: no deja trabajo»). Es más barato, pero no deja rastro en
  la spec.
- **(c) Aceptar los cinco como pendientes conocidos** y dejarlo escrito.
- **El caso de RN-033 es aparte**, porque no es un hueco del mecanismo sino una decisión. Si el
  consultor la mantiene, el registro seguirá pendiente: la salida limpia es un ADR que lo diga, o
  que el registro apunte a RN-003, que es donde se refleja.

### 1.2.1 La decisión del consultor: la opción (b), aplicada (2026-09-30)

Tras la revisión, el consultor eligió la **(b)**. Un registro de confirmación cuyo valor coincide
con el valor CONFIRMED vigente del parámetro o la regla que nombra **deja de contar como
pendiente** sin ocupar la cita. `feedback pending` lo lista aparte, bajo «confirmaciones de valores
ya fijados», con el id y el objetivo. Si el valor no coincide, sigue pendiente, como antes.

**Cómo queda en el código** (`cli.py`, `situacion_de`; `feedback/aplicar.py`,
`confirma_el_vigente`):
- **Parámetro:** un CONFIRM sobre un parámetro CONFIRMED que no lo cita es confirmación si su valor
  coincide con el vigente. Se convierte con el mismo conversor que usa `feedback apply`.
- **Parámetro, CONFIRM sin valor propio:** también es confirmación. **Es la lectura que ha habido
  que hacer, y se dice:** los cuatro CONFIRM reales no traen `valor_resultante` ni
  `valor_canonico`. El trader dice «sí, es eso», así que no hay valor que pueda discrepar.
- **Regla:** no tiene un valor con que comparar. Solo cuenta como confirmación un CONFIRM sin valor
  propio sobre una regla VIGENTE; uno que traiga valor sigue pendiente.
- **Sigue pendiente:** el CONFIRM cuyo valor no coincide, el que nombra un parámetro que no existe y
  todo lo que no sea CONFIRM.
- **Tests** (`tests/unit/test_cli.py`):
  - una confirmación coincidente, con valor y sin él, no es pendiente y sale en su cajón;
  - una discrepante es pendiente;
  - una sobre un parámetro inexistente es pendiente;
  - una sobre una regla que trae valor es pendiente.

**Resultado sobre el repositorio:** `feedback pending` pasa a **1 pendiente**, 83 reflejados,
**4 confirmaciones** (`liquidez_m15_criterio_toma`, `cartuchos_max`, `lotaje_base` y G-1 sobre
RN-015) y 9 sin mecanismo.

**S-1 sobre RN-033 sigue pendiente, y es a propósito: medido, no es una confirmación.**
`fb-2026-09-29-sesion-03-1168f036` es un **CORRECT** con `valor_resultante` en prosa («siempre hay
sesgo: no se deja de operar por un sesgo no claro»), así que la regla (b) no lo alcanza. Meterlo
habría exigido una excepción a la regla que se acaba de escribir. Queda para el consultor: un ADR
que diga que RN-033 no lo refleja, o un registro que lo lleve a RN-003, que es donde el motor ya lo
hace.

### 1.3 Desalineaciones con el motor (no se ha tocado)

- **RN-014 (break even al tocar).** El trader dice «apenas toca», y el motor evalúa la estrategia al
  cierre de M1 (ADR-0028), así que mueve el stop en el cierre de la M1 que toca, no en el tick. Ya
  estaba anotado (ADR-0053 §2.1) y se revisa con la demo.
- **RN-007 (vela casi plana).** El mapeo de M1 no trata aparte las velas casi planas. Falta el
  umbral, que el trader no dio (pregunta 14 de la hoja), y una rama de código. La forma ejecutable
  no cambia.

## 2. La hoja de la sesión 4

- **Pregunta 16, opción (b):** queda en «el del vídeo», sin «aunque te saltaste algunos break even».
- **Pregunta 19:** lleva la nota para Aleks: «pregunta solo qué tipo de capturas son; si empieza a
  dar cifras, córtalo; el tramo va a cuarentena».

## 3. G-2: la caja de las siete ganadoras, en sus fotogramas

En `ACTIVAR-SESION-03.md` §4.1.1, como apartado nuevo; el cuerpo del informe no se toca. **Ninguna de
las siete se puede medir en pantalla.**
- **04-01, 04-06 y las dos del 13 de abril:** ningún vídeo enseña esos días.
- **04-29 09:36:** tampoco sale en vídeo; v5 solo recorre la entrada de las 07:55 y su reentrada.
- **04-29 07:58:** v5 tiene la caja dibujada, pero sin eje de precios. Es la medida que
  `LA-CAJA-DEL-29-DE-ABRIL.md` ya dio por NO CONCLUYENTE.
- **08-07:** el backtest grabado pasa por esa sesión sin entrar, que es lo que pregunta E-1.

Siguen valiendo las cotas de §4.1. No va en la hoja del trader. Los siete fotogramas abiertos, y
las cifras de saldo que se vieron en ellos sin usarlas, están declarados en
`HOLDOUT-EXPOSICIONES.md`.

## Estado

**Revisada por el consultor el 2026-09-30, con la opción (b) aplicada** (§1.2.1). En Next Action
quedan dos puntos nuevos: G, la rama de código de RN-014 (break even al tick), y H, RN-007 a la
espera de la pregunta 14. Queda pendiente S-1 sobre RN-033, que no es una confirmación.

Antes de la revisión decía: «Rama lista para revisión, NO cerrada. Pendiente del consultor: elegir
(a), (b) o (c) para los cuatro CONFIRM que no caben, y decidir qué se hace con S-1 sobre RN-033».
