---
status: ACTIVE
date: 2026-10-07
phase: post-F14 (rama `trabajo/umbral-mayo`)
---

# 0070 · Mayo solo se mide cuando una corrida del arnés sobre construcción, sin diagnóstico, llega al umbral de ADR-0043

Pre-registrado antes de cualquier corrida nueva del arnés (decisión del consultor del 2026-10-07,
punto J de la Next Action). Informe: `docs/validation/UMBRAL-MAYO.md`.

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
3. **Sin diagnóstico.** Solo cuenta una corrida SIN ninguna opción `--diagnostico-*` (A-35, A-44,
   A-21, A-47, A-27 o la cuenta diaria: las que etiquetan la salida, `engine/diagnostico.py`). Mayo
   mide la spec, no una hipótesis del consultor: mientras el motor necesite un diagnóstico para
   correr -hoy A-21, A-35 y A-44-, mayo no se mide.
4. **Si no llega, se sigue construyendo y mayo no se toca.** El umbral no se relaja después de ver
   una corrida: cambiarlo exige un ADR nuevo que declare lo visto.
5. **Dónde viven las cifras y quién lo dice.** Dos campos nuevos en `criterio_fidelidad.yaml`,
   `umbral_construccion_para_medir_cobertura: "0.70"` y
   `umbral_construccion_para_medir_precision: "0.60"` (ADR-0002: ninguna cifra en `src/`), cargados
   y validados (entre 0 y 1) por `cases/criterio_fidelidad.cargar_criterio`. El arnés imprime al
   final de su sección «## Criterio de fidelidad (ADR-0043)» una línea de veredicto, «habilita
   medir el conjunto de medida (…): sí» o «… : no», con el motivo de cada condición que falte,
   incluido «corrida con diagnóstico».
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
3. Admitir corridas con diagnóstico, que hoy son las únicas que el motor puede hacer.
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

## Por que descartamos las demas

- **La 1** gasta mayo sin poder aprender de él: hoy el motor no corre sin tres diagnósticos, y su
  resultado obligaría a pasar mayo a construcción (ADR-0043).
- **La 2** introduce una cifra nueva sin medida que la sostenga, y cualquier valor se fijaría con
  las corridas de construcción ya vistas a la vista. Mantener las de ADR-0043 es lo único que no se
  puede elegir mirando el resultado.
- **La 3** mediría una hipótesis del consultor y no la spec: el «sí» dependería de qué lectura de
  A-21, A-35 o A-44 se eligió al lanzar la corrida, que es justo lo que el trader tiene que
  responder.

## Impacto

- `knowledge/cases/criterio_fidelidad.yaml`: dos campos nuevos; ningún campo existente cambia (ni
  las tolerancias, ni los umbrales de medida, ni los conjuntos).
- `src/botsito/cases/criterio_fidelidad.py`: `Criterio` gana los dos umbrales y una función pura que
  da el veredicto.
- `src/botsito/engine/arnes.py` y `src/botsito/cli.py`: `informe` recibe si la corrida lleva
  diagnóstico y escribe la línea de veredicto.
- Tests sintéticos de las cinco situaciones que pide el encargo; ninguno corre el arnés sobre datos.
- Mientras A-21, A-35 y A-44 sigan sin respuesta, el veredicto será «no» por diagnóstico en toda
  corrida que hoy se pueda hacer.
- Queda para el consultor: si una corrida con `--depuracion` (sin ticks, sobre el respaldo M1; «la
  salida lo marca y NO cuenta», ADR-0051 §8) tiene que contar como «no» también. Este ADR no lo
  decide.

## Fecha / fase

2026-10-07 · post-F14, rama `trabajo/umbral-mayo`.

## Estado

ACTIVE
