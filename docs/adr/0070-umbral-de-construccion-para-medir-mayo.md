---
status: ACTIVE
date: 2026-10-07
phase: post-F14 (rama `trabajo/umbral-mayo`)
---

# 0070 · Mayo solo se mide cuando una corrida del arnés sobre construcción, solo con las opciones de una lista cerrada, llega al umbral de ADR-0043

Pre-registrado antes de cualquier corrida nueva del arnés (decisión del consultor del 2026-10-07,
punto J de la Next Action). Informe: `docs/validation/UMBRAL-MAYO.md`.

> **ENMIENDA (2026-10-07, rama `trabajo/umbral-mayo`, antes del cierre: el cuerpo se edita).**
> Respuesta del consultor del 2026-10-07: **la decisión 3 pasa a negar por defecto.** La primera
> versión enumeraba un caso, las opciones `--diagnostico-*`, y `--depuracion` mostró que se
> escapaban otros. Ahora el veredicto solo puede ser «sí» si la corrida usó ÚNICAMENTE opciones de
> una lista CERRADA de las que no cambian lo que el motor decide ni cómo se llena: `--salida`,
> `--tracemalloc` y `--meses` (esta solo si cubre todo `construccion`, decisión 2). Cualquier otra
> opción presente, conocida o futura, da «no», con el motivo «opción fuera de la lista:
> <nombre>». Las decisiones 3 y 5 de abajo ya están escritas así; la versión anterior, en la
> historia de git de la rama (commit `3320177`).

> **ENMIENDA (2026-10-07, rama `trabajo/umbral-mayo`, antes del cierre: el cuerpo se edita).**
> Respuesta del consultor del 2026-10-07 a la PARADA de `--simular` (`UMBRAL-MAYO.md` §8 y §11):
> 1. **La corrida que habilita LLEVA `--simular`, obligatoriamente.** Sin ella el motor de la spec
>    no produce operaciones (`engine/motor.py:233`), y ADR-0043 compara instantes de LLENADO, que
>    solo da el bróker simulado (`engine/cableado.py:250`); además es como operará el bot. Una
>    corrida sin `--simular` da «no» con el motivo «sin simulación».
> 2. **`--perfil` y `--fase` solo se admiten con el perfil de la cuenta real (FTMO 2-Step Swing
>    100k, ADR-0026) y su PRIMERA fase**, como condición sobre los valores EFECTIVOS de la corrida
>    (dados o por defecto): el perfil tiene que ser `perfil_para_medir` de
>    `criterio_fidelidad.yaml` (`ftmo-2step-swing-100k`, el único de `knowledge/cuentas/` y el que
>    `--perfil` da por defecto) y la fase la primera que declara ese perfil (`reto`, la primera de
>    `firma_fases`, y la que `--fase` da por defecto). Cualquier otro valor da «no» con su motivo.
> 3. **La lista cerrada queda** `--salida`, `--tracemalloc`, `--meses` (cubriendo todo
>    `construccion`), `--simular` (obligatoria), `--perfil` y `--fase` (solo con los valores del
>    punto 2). Todo lo demás, incluido `--repo`, `--depuracion` y cualquier opción futura, da «no».
>    Un día sin ticks exige `--depuracion`, que da «no».
>
> Las decisiones 3 y 5 y el impacto de abajo ya están escritos así; la versión anterior, en la
> historia de git de la rama (commit `5e46075`).

## Decision

1. **El umbral.** El conjunto de medida de ADR-0043 (hoy mayo, `medida: ["2026-05"]` en
   `knowledge/cases/criterio_fidelidad.yaml`) solo se mide cuando UNA corrida de
   `botsito motor arnes` sobre el conjunto de construcción vigente en ese mismo fichero dé, en esa
   misma corrida, una cobertura de al menos 0,70 y una precisión de al menos 0,60: las mismas cifras
   que ADR-0043 fija para la medida. Las dos condiciones a la vez. Una métrica sin definir (sin
   denominador: cero operaciones del trader o cero del bot puntuables, `criterio_fidelidad.medir`)
   cuenta como que no llega.
2. **Sobre el conjunto entero.** La corrida tiene que cubrir todos los meses de `construccion`. Una
   corrida sobre una parte (el comando admite `--meses`) no habilita: el umbral es de la
   construcción vigente, no de un mes elegido.
3. **Solo con las opciones de una lista cerrada, y simulada con la cuenta real** (enmiendas del
   2026-10-07). La corrida solo cuenta si usó únicamente `--salida`, `--tracemalloc`, `--meses`,
   `--simular`, `--perfil` y `--fase`, las que no cambian lo que el motor decide ni cómo se llena
   más allá de cómo operará el bot. Cualquier otra opción -un `--diagnostico-*` (A-35, A-44, A-21,
   A-47, A-27 o la cuenta diaria), `--depuracion`, `--repo` o una que se añada mañana- da «no». La
   lista vive en un solo sitio, `engine/arnes.py` (`OPCIONES_QUE_NO_CAMBIAN_LA_CORRIDA`), y las
   opciones de la corrida se leen de los propios parsers del comando, el raíz y el del subcomando
   (`cli.opciones_de_la_corrida`), no de otra lista. Mayo mide la spec, no una hipótesis del
   consultor: mientras el motor necesite un diagnóstico para correr -hoy A-21, A-35 y A-44-, mayo
   no se mide. Además:
   - **`--simular` es obligatoria.** Sin ella el motor de la spec no produce operaciones, y
     ADR-0043 compara instantes de llenado, que solo da el bróker simulado. Una corrida sin
     simulación da «no» con el motivo «sin simulación».
   - **El perfil y la fase EFECTIVOS** (dados o por defecto) tienen que ser el perfil de la cuenta
     real, `perfil_para_medir`, y la primera fase que ese perfil declara. Otro perfil da «no»
     («perfil <nombre>: solo cuenta <perfil_para_medir>»), y otra fase también («fase <nombre>:
     solo cuenta la primera del perfil, <primera>»).
4. **Si no llega, se sigue construyendo y mayo no se toca.** El umbral no se relaja después de ver
   una corrida: cambiarlo exige un ADR nuevo que declare lo visto.
5. **Dónde viven las cifras y quién lo dice.** Tres campos nuevos en `criterio_fidelidad.yaml`,
   `umbral_construccion_para_medir_cobertura: "0.70"`,
   `umbral_construccion_para_medir_precision: "0.60"` (ADR-0002: ninguna cifra en `src/`) y
   `perfil_para_medir: ftmo-2step-swing-100k` (ningún nombre de firma en el código, ADR-0050),
   cargados y validados (los umbrales entre 0 y 1; el perfil, un texto no vacío) por
   `cases/criterio_fidelidad.cargar_criterio`. La primera fase no es un campo: sale del propio
   perfil (`firma_fases`). El arnés imprime al final de su sección «## Criterio de fidelidad
   (ADR-0043)» una línea de veredicto, «habilita medir el conjunto de medida (…): sí» o «… : no»,
   con el motivo de cada condición que falte, incluida cada «opción fuera de la lista: <nombre>»,
   «sin simulación» y el perfil o la fase que no son los que cuentan.
6. **Esto no mide mayo.** No se construye ningún comando de medida: el arnés sigue negándose a
   cualquier mes de `medida` (ADR-0048 §7), y la medida tendrá su propia rama y su propio ADR. Un
   «sí» habilita esa rama; no la sustituye.

## Problema que resuelve

ADR-0043 fija el umbral de MEDIDA (cobertura ≥ 70 %, precisión ≥ 60 % sobre mayo) y dice que mayo
«se mide una vez por versión de la spec; si la spec cambia después de ver el resultado de mayo, mayo
pasa a construcción». Medir mayo con un motor que todavía no llega en construcción gasta el único
conjunto de medida limpio sin aprender nada: el resultado se sabría malo de antemano, y mirarlo
obliga a pasar mayo a construcción. Faltaba decir CUÁNDO se puede gastar. La línea J de la Next
Action hablaba de un umbral «para pasar al plan híbrido», un término que no estaba definido; la
decisión de Aleks del 2026-10-06 (el bot es 100 % automático, sin ningún plan con intervención
humana; `docs/encargos/trabajo-respaldo-a11.md`, «Añadido del consultor») la sustituyó por este
umbral.

## Alternativas consideradas

1. Medir mayo ya, con el motor de hoy.
2. Un umbral de construcción distinto del de ADR-0043 (más alto, para dejar margen a la caída de
   construcción a medida, o más bajo, para habilitar antes).
3. Admitir corridas con diagnóstico, que hoy son las únicas que el motor puede hacer; o, en la
   primera versión de este ADR, enumerar las opciones que dan «no» en vez de las que dan «sí».
4. El umbral de ADR-0043 sobre construcción, en una corrida sin diagnóstico y sobre el conjunto
   entero (la elegida).

## Por que elegimos esta opcion

- Usa las cifras que ya están pre-registradas: no hay ninguna cifra nueva que justificar ni que
  ajustar mirando una corrida.
- Pide al motor, en el material donde se ajusta, lo mismo que se le pedirá donde se mide. Si no lo
  da en construcción, no lo va a dar en mayo.
- La condición la evalúa el propio arnés en la misma corrida y lo escribe en su salida: nadie
  tiene que interpretar un informe para saber si mayo se puede medir.
- Un bot 100 % automático corre con la spec, no con una lectura que el consultor elige al
  lanzarlo: una corrida en hipótesis no dice nada de lo que la spec hará en mayo.
- La corrida que habilita es como operará el bot: simulada, con la cuenta real y la fase en la que
  empieza. Y solo la simulación da los instantes de llenado que ADR-0043 compara.

## Por que descartamos las demas

- **La 1** gasta mayo sin poder aprender de él: hoy el motor no corre sin tres diagnósticos, y su
  resultado obligaría a pasar mayo a construcción (ADR-0043).
- **La 2** introduce una cifra nueva sin medida que la sostenga, y cualquier valor se fijaría con
  las corridas de construcción ya vistas a la vista. Mantener las de ADR-0043 es lo único que no se
  puede elegir mirando el resultado.
- **La 3** mediría una hipótesis del consultor y no la spec: el «sí» dependería de qué lectura de
  A-21, A-35 o A-44 se eligió al lanzar la corrida, que es justo lo que el trader tiene que
  responder.
  Y enumerar lo que da «no» deja pasar lo que nadie enumeró: `--depuracion`, que corre sin ticks
  y cuya salida «NO cuenta» (ADR-0051 §8), habría dado «sí». Por eso la lista dice lo que da
  «sí».

## Impacto

- `knowledge/cases/criterio_fidelidad.yaml`: tres campos nuevos; ningún campo existente cambia
  (ni las tolerancias, ni los umbrales de medida, ni los conjuntos).
- `src/botsito/cases/criterio_fidelidad.py`: `Criterio` gana los dos umbrales y el perfil;
  `Simulacion` (perfil y fase efectivos, y la primera fase del perfil) y una función pura que da
  el veredicto.
- `src/botsito/engine/arnes.py`: la lista cerrada y la línea de veredicto; `informe` recibe las
  opciones que usó la corrida y su simulación (o `None`). `src/botsito/cli.py`:
  `opciones_de_la_corrida` las lee de los propios parsers del comando, y la simulación se construye
  con el perfil y la fase del motor cableado.
- Tests sintéticos de las situaciones que piden el encargo y la enmienda; las opciones se obtienen
  parseando argumentos, y ninguno corre el arnés.
- Si, como dice el encargo, el motor necesita hoy los diagnósticos de A-21, A-35 y A-44 para
  correr, hoy ninguna corrida puede dar «sí»: cualquier `--diagnostico-*` está fuera de la lista.
  No se midió en la rama (medirlo exigía correr el arnés, prohibido en ella).

## Fecha / fase

2026-10-07 · post-F14, rama `trabajo/umbral-mayo`.

## Estado

ACTIVE
