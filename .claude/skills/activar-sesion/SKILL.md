---
name: activar-sesion
description: Activa en la spec y en el motor de Bot v3 las respuestas del trader -de una sesion ya extraida (tabla final de su SESION-0N-EXTRACCION.md) o llegadas por escrito fuera de sesion-, una por una, sin pisar nada fijado y cerrando cada ambiguedad por sus sitios. Usala cuando un encargo pide activar una sesion o unas respuestas concretas del trader.
argument-hint: "<AAAA-MM-DD-sesion-NN> [ids de ambiguedad]"
---

# activar-sesion

Activar es traducir lo que el trader DIJO, registrado, a la spec y al motor. **Nada de lo que hay
aqui decide por el trader.** Las reglas viven en `docs/runbooks/AMBIGUEDADES.md`,
`knowledge/feedback/README.md`, `CLAUDE.md` («Regimenes de cambio», «El trailer Fuente:», «Al
anadir un sitio con cita propia», «Las cifras van en el registro de parametros») y los
precedentes: `docs/validation/ACTIVAR-SESION-03.md`, `docs/validation/ACTIVACION-A42.md` y
`docs/runbooks/ACTIVAR-A35-A44.md`. Si esta skill y ellos discrepan, ganan ellos y se dice.
La ultima activacion cerrada es `docs/validation/ACTIVAR-SESION-06-MOTOR.md`
(`stable/F38o-activar-sesion-06-motor`, 2026-11-06), anterior a ADR-0093 (2026-11-11).

## Entradas

| Entrada | De donde sale | Si falta |
|---|---|---|
| La sesion y su extraccion | `docs/validation/SESION-0N-EXTRACCION.md`: tabla final y la seccion de cada pregunta | sin extraccion no se activa: primero `ingerir-sesion` |
| Respuestas escritas fuera de sesion (WhatsApp, correo) | `knowledge/feedback/README.md`, «Material que llega fuera de sesion» | — |
| Las respuestas a activar | el encargo; si no las acota, todas las «resuelve» de la tabla | se pregunta |
| La revision del consultor de esa extraccion | el informe de extraccion («Revisión del consultor»), si existe | se dice que no hay |
| Lo que el encargo hereda | grep del numero de sesion y de «activacion» en la Next Action (y sus «Pendientes heredados»), en `docs/plan/HOJA-DE-RUTA.md` y en `docs/state/HISTORIA.md` (p. ej. el heredado 15, la pregunta de A-18, que la hoja de ruta, R1.1, saca cuando se cierre A-18) | se busca antes de empezar |

## Limites

- **La fuente es la extraccion**: nada en cuarentena ni en tramos no citables; las citas, solo las
  que la extraccion ya dejo citables, por la CLI filtrada.
- **Lo fijado no se pisa.** Si una respuesta contradice un valor CONFIRMED, una regla con su
  `literal`, un ADR o una respuesta anterior del trader: PARADA, con las dos fuentes. Se corrige
  por su regimen: `CORRECT` sobre parametro, regla o evidencia (con `supersede` si retira otro
  registro); `REOPEN` y despues un `RESOLVE_UNKNOWN` nuevo sobre una ambiguedad RESUELTA; otro ADR
  sobre una DECIDIDA; o vuelve a la siguiente sesion. Nunca pisando.
- **«En parte» no se cierra**: va a la lista de la siguiente sesion con la pregunta reformulada, y
  lo que si quedo claro de ella se dice sin fijar nada.
- **Un parametro con valor provisional no es una respuesta activada**: si su ambiguedad sigue
  ABIERTA, la activacion la cierra o dice por que no.
- **Una respuesta con horas** se fija contra el reloj en que la dio el trader y su UTC (lo que paso
  con S-7 de la sesion 4).
- Toda cifra va al registro de parametros (ADR-0002), nunca dentro de la forma ejecutable.
- Ningun cambio de motor sin un test que falle antes (skill `comparar-con-main`, «Para probar un
  test con el codigo de main») y pase despues.
- **El arnes** (`uv run botsito motor arnes`). La corrida de julio de 2026 de ADR-0093 §4 forma
  parte de toda activacion y es diagnostico (seccion siguiente). Cualquier otra corrida del arnes,
  solo si el encargo o la respuesta a la PARADA la autorizan expresamente (`ACTIVAR-A35-A44.md` lo
  pedia tras activar; los encargos recientes lo prohiben salvo autorizacion). La corrida que cuenta
  ya no es la de R3.1: es la de R4.3 de `docs/plan/HOJA-DE-RUTA.md` («el pivote leído en la
  re-corrida siguiente»), «la primera corrida de ADR-0070 §3 [...] después de activar la 7b»
  (ADR-0093 §6, «Qué se mide»), con las opciones de ADR-0070 («Decision», punto 3) y la lectura del
  pivote de ADR-0093 §6. En la duda, PARADA.

## El metodo de ADR-0093 §4

Desde ADR-0093 (2026-11-11), con sus palabras:

- «Cada respuesta se escribe primero como test sobre casos de construcción que rompe en `main`».
- «Cada activación declara ANTES qué filas de la clasificación vigente debería convertir en
  pareja», y corre julio de 2026 en la rama, «con su delta de parejas y de operaciones de más frente
  a la línea base».
- La linea base: §4 no la define. Es la de ADR-0093 §6 («Línea base»), con sus cifras en
  `docs/plan/PIVOTES-SESION-7.yaml` (`linea_base`): esa lectura, y no otra.
- «Si el delta de julio de una activación no casa con lo que declaró, la regla no se retoca hasta
  que la cifra salga: PARADA» (ADR-0093 §4).
- El delta es diagnostico: «La cifra dice si la respuesta se entendió, nunca ajusta un parámetro»
  (ADR-0093 §4, que cita ADR-0092 §6) y «El delta nunca elige entre dos lecturas de un parámetro»
  (ADR-0093 §4).
- Como se corre julio en una activacion (el comando, sus opciones y como se calcula el delta) no
  esta escrito en ningun sitio (`docs/validation/SKILLS-METODO.md`, fase 0): lo fija y lo cita el
  encargo de cada activacion.

## El recorrido

1. **Tabla de activacion** (fase 0, con la skill `fase-cero`), una fila por respuesta:
   `codigo · ambiguedad · lo que dijo (resumen fiel, con su tramo) · registro que hoy la cierra o
   reabre (uv run botsito feedback trace <A-n>) · estado del parametro hoy (UNKNOWN /
   DEFAULT_AMBIGUOUS / CONFIRMED y valor, leido en knowledge/spec/parametros.yaml) · si la premisa
   de la pregunta sigue vigente · reloj y UTC si trae horas · quien la espera
   (grep -rn "A-n" CLAUDE.md docs/runbooks PROJECT_STATE.md docs/plan/HOJA-DE-RUTA.md, donde
   va como `ID:A-n`) · que falta (nada / cerrar /
   codigo / contradice X) · destino (activar / siguiente sesion / PARADA)`.
2. **PARADA** con la tabla. En especial: cada contradiccion, cada «en parte», cada respuesta dada
   con «creo» o con un ejemplo sin regla general.
3. **Por cada respuesta a activar, en su propio commit**, sin crear los registros de la siguiente
   hasta commitear esta (un `feedback apply` aplica la sesion entera):
   - el registro del trader sobre LA AMBIGUEDAD, con TODAS las opciones obligatorias
     (`src/botsito/cli.py`, `feedback new`; la plantilla de `knowledge/feedback/README.md`):
     `uv run botsito feedback new --sesion <AAAA-MM-DD-sesion-NN> --fecha <AAAA-MM-DD>
     --recibido-el <AAAA-MM-DD> --procedencia <trader_grabado|trader_escrito|...>
     --medio <replay|audio|video|escrito> [--grabacion <ruta> --t0 <h:mm:ss> --t1 <h:mm:ss>]
     --objetivo-tipo ambiguedad --objetivo-id <A-n> --accion RESOLVE_UNKNOWN --valor <...>
     --respuesta "<literal>" --registrado-por <quien>`; si la ambiguedad viene de un `REOPEN`,
     con `--supersede <id del REOPEN>`;
   - un registro por PARAMETRO que fije (`--objetivo-tipo parametro --valor ...`, con
     `--valor-canonico` si el registro espera otro tipo: `'0,8'` -> `'0.8'`), y despues
     `uv run botsito feedback apply --sesion <AAAA-MM-DD-sesion-NN> --check` (tiene que proponer
     SOLO los de esta respuesta) y sin `--check`;
   - los cinco sitios de cerrar una ambiguedad (`AMBIGUEDADES.md`): registro de parametros,
     `ambiguedades.yaml`, la regla de la spec que la citaba, la tabla de `PROJECT_STATE.md` y la
     hoja de preguntas (`scripts/hoja_preguntas.py`) con su test;
   - `tests/unit/test_kit.py` SIEMPRE: el conjunto de RESUELTAS y el de bloqueantes ABIERTAS;
   - subir `spec_version`, `uv run botsito spec manifest --escribir` y
     `uv run botsito spec docs --escribir`, en el mismo commit;
   - si toca un parametro que entra en la capa de MT5 (`ENTRAN` de
     `src/botsito/mql5bridge/generar_capa.py`; `parametros.yaml` o el perfil), se regenera
     `mql5/Include/Botsito/Capa/Generado.mqh` en el mismo commit:
     `uv run python src/botsito/mql5bridge/generar_capa.py --repo . --perfil ftmo-2step-swing-100k`
     (`docs/runbooks/RENOVAR-CIERRES.md`, «Cómo se comprueba»; `docs/validation/CAPA-GENERADA.md`,
     fase 2, D3); `tests/unit/test_capa_generada.py` falla si el fichero no es lo que da el generador;
   - si la regla gana un sitio con `cita`: las tres guardias de `src/botsito/spec/modelo.py`;
   - el codigo del motor, si falta, con su test;
   - los tests que congelaban el estado «sin fijar» cambian de sentido A PROPOSITO, y el commit y
     el informe lo dicen (`ACTIVAR-A35-A44.md` §2);
   - `uv run botsito knowledge validate` antes de `make check`; trailer `Fuente:` en el CUERPO del
     commit con los ids `fb-*` nuevos.
4. **Lo que se hereda** (entradas): hecho, o declarado con su motivo.
5. **Lo que no se activo**: lista para la siguiente sesion, con la pregunta reformulada en el
   lenguaje del trader y la razon.
6. **Next Action y hoja de ruta** (`docs/plan/HOJA-DE-RUTA.md`): las lineas que salen y entran, y
   las entradas de la hoja que cambian, se preparan en el informe para el commit del contrato del
   cierre; en la rama no se tocan.
7. Entrega con `entregar-rama`.

## Artefacto

`docs/validation/ACTIVAR-SESION-0N.md` con la tabla de activacion, la PARADA y su respuesta, una
seccion por respuesta activada (commits, registros, tests, sitios tocados), lo que no se activo y la
lista para la siguiente sesion.

## Verificacion

- Ninguna ambiguedad activada sigue ABIERTA; ninguna «en parte» se cerro.
- `uv run botsito feedback pending` no lista nada de lo activado.
- `uv run botsito knowledge validate` y `make check` en verde en cada commit.
- `git log --format='%h%n%B' main..HEAD -- knowledge/spec knowledge/cases`: todos con `Fuente:` en
  el cuerpo e ids que existen.
- Ninguna cita del informe ni de `HOLDOUT-EXPOSICIONES.md` cae en un tramo de
  `knowledge/corpus/tramos_no_citables.yaml`, margenes incluidos.
