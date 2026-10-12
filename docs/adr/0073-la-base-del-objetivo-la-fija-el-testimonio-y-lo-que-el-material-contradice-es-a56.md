---
status: ACTIVE
date: 2026-10-11
phase: post-F14 (rama `trabajo/activar-sesion-04`, R1.1 de la hoja de ruta)
---

# 0073 · La base del objetivo y el stop los fija el testimonio del trader; lo que el material contradice es una medición abierta (A-56), y ADR-0040 queda enmendado

> Decisión del consultor del 2026-10-11 (respuesta a la PARADA de `trabajo/activar-sesion-04`,
> punto 0; informe `docs/validation/ACTIVAR-SESION-04.md`). **Enmienda ADR-0040** (recuadro allí
> y fila del índice). Ningún dato de ADR-0040 se toca.

## Decision

### 1. A-18 y A-33 quedan RESUELTAS por lo que el trader dijo en la sesión 4

- **A-18** («¿cómo decides dónde va el stop y dónde va el objetivo?»): S-3, v10 0:35:59–0:39:48. El
  stop va ya en el 0,8 al poner la orden («Sería directamente a 0.8», `ev-v10-003559-211855b7`);
  el 1 «se usa al comienzo pero no de ejecución, sino como planteamiento»
  (`ev-v10-003706-5b7055a2`); el objetivo se mide del 0 al 1 y el lote del 0 al 0,8 («se usa de 0
  a 1 para el cálculo de 1 a 3 [...] para la toma de la operativa se usa de 0 a 0,8»,
  `ev-v10-003927-2f6d9f48`). Es la tercera vez que lo dice (sesión 3:
  `fb-2026-09-29-sesion-03-f572f1a0` y `fb-2026-09-29-sesion-03-d62c788a`; v7 0:06:07). No hay
  stop en dos tiempos en la ejecución: la candidata C4 de `DISENO-ENTRADA-RUPTURA.md` §2.8 queda
  contestada en eso (la orden sin stop de v8 n.º 1, no).
- **A-33** («¿alguna vez cierras una ganadora antes del objetivo?»): S-12, v10 1:27:04–1:27:36 y
  1:29:02–1:29:21 (las ventanas de sus dos ítems; entre ellas hay un tramo de precaución).
  Nunca: «todo es 13 o sea fijo es 13 la regla es esa [...] respecto al 1 de la caja»
  (`ev-v10-012902-257afe4b`), con la reserva literal «no vamos a dejar correr nada por ahora»
  (`ev-v10-012704-d3facd31`), que queda en sus notas.
- **Ningún valor cambia.** `base_calculo_objetivo` = `caja_completa`, `objetivo_rr` = 3,
  `stop_fraccion_caja` = 0,8, `lotaje_base` = `hasta_stop_fraccion` y `parciales` = no ya estaban
  CONFIRMED con lo mismo. Los dos cierres son registros RESOLVE_UNKNOWN sobre la ambigüedad.

### 2. ADR-0040 queda enmendado: «refutada» pasa a «dicha por el trader y contradicha por el material»

ADR-0040 midió que la región [3,00, 3,75) del RR implícito de `maxTP` sobre entrada-stop está
poblada en tres meses (26 filas de 38) cuando la combinación `(caja_completa, 0,8)` predice que está
vacía, y por eso la llamó refutada y dejó A-18 abierta (su decisión 3). La medida no se toca: sigue
siendo cierta. Lo que cambia es el nombre de lo que mide: la combinación es la regla dicha por el
trader tres veces, y lo que el material contradice no es su testimonio sino la forma en que sus
operaciones acaban en el libro. Esa contradicción es una MEDICIÓN pendiente y no una pregunta al
trader: pasa a A-56 (§3). Las decisiones 1, 2 y 4 de ADR-0040 siguen en pie (la región medida, los
dos supervivientes como lecturas del material, ningún parámetro cambia); la 3 queda enmendada: A-18
se cierra.

### 3. A-56, nueva: la regla frente al material, una medición para F26

Clase `medicion`, no bloqueante (un bloqueante no se cierra como DECIDIDA, y una medición nunca va al
trader), `resuelve_en` [F26], con fuentes documentales a ADR-0040. Recoge: (a) la región poblada de
ADR-0040; (b) que su fila de agosto sale del xlsx `backtesting-analytics AGOSTO 2026.xlsx` y que en
S-16 (v10 1:48:23–1:48:53, `ev-v10-014823-64248489`, `ev-v10-014853-76602fb4`) el trader da por
bueno «el último» de sus dos backtests de agosto, el grabado en vídeo, «porque incluye los break
even» (que el xlsx sea el otro, el que «no lo incluía», es una lectura de la sesión y no su frase:
E-1 de la sesión 3 ya preguntaba por «tus dos backtests de los mismos días»); sin agosto la región
sigue poblada con abril (7 de 15) y mayo (4 de 5); (c) las ganadoras del material
por debajo de 3R (cuatro en tres meses, listadas en las notas de A-33 y en `MAYO-DEV.md`), que
hasta hoy vivían en A-33 y que «nunca cierro antes» no explica. Lo que la resolvería lo dice ADR-0040
§2: un material que traiga la caja; y, desde S-16, un libro de agosto que sea el que el trader da por
bueno.

### 4. Qué lee F26

F26 lee la diferencia 3,00 frente a 3,75 como conocida (ADR-0040 §Impacto), y A-56 es donde se
apunta lo que se mida. La deuda «F26 NO PUEDE PUNTUAR EL OBJETIVO HASTA QUE A-18 ESTE CERRADA», la G
de la Next Action y R5.1 se reapuntan a A-56 en el cierre de la rama; el heredado 15 sale; la
pregunta de reserva de A-18 en `docs/validation/V5-INSTANTES.md` («Pregunta al trader (RESERVA)»)
queda superada y no se edita.

### 5. S-16 queda registrado aquí

`feedback new` no tiene objetivo para E-1 (no es ambigüedad, regla, parámetro ni evidencia), así que
la decisión del trader sobre su material queda escrita en este ADR y en el informe: vale el backtest
de agosto grabado en vídeo (v7 y v8, días 3 a 19 de agosto; `fuentes.yaml`). Hasta que llegue su
exportación, los 19 casos `dev` de agosto siguen saliendo del xlsx; al llegar, entra por su propia
rama (`libros.yaml` solo se amplía, ADR-0039 §3) y ADR-0040 y A-56 se revisan. Lo mismo dijo de
julio (S de la Next Action).

## Problema que resuelve

A-18 llevaba tres respuestas iguales del trader y seguía ABIERTA por una medida del material que
ningún testimonio puede cambiar; A-33 preguntaba por ganadoras del material y el trader contestó lo
único que puede contestar: que él no cierra antes. Sin un ADR, cerrarlas contradecía la decisión 3
de ADR-0040, y no cerrarlas dejaba en la hoja de la sesión 5 una pregunta ya respondida.

## Alternativas consideradas

1. Un ADR que fije el testimonio y deje ADR-0040 como hecho medido, con la contradicción en una
   medición nueva (la elegida).
2. No cerrar ninguna hasta un material que traiga la caja (ADR-0040 §2).
3. Cerrar A-33 y dejar A-18 abierta con lo firme activado.

## Por que elegimos esta opcion

La spec ya corre con esa combinación desde la sesión 3 y mantener A-18 abierta no deja ninguna
pregunta nueva que hacerle al trader. Lo que falta es material, no testimonio, y una medición
pendiente tiene su sitio: una ambigüedad de clase `medicion`, como A-16 y A-28.

## Por que descartamos las demas

- La 2 cuelga HER:15, la deuda de F26 y R5.1 de una pregunta ya respondida tres veces.
- La 3 da destinos distintos a dos preguntas gemelas sin un criterio escrito.

## Impacto

- `knowledge/spec/ambiguedades.yaml`: A-18 y A-33 RESUELTAS, con sus registros; A-56 nueva.
- `PROJECT_STATE.md`: salen las filas de A-18 y A-33 y entra la de A-56; `tests/unit/test_kit.py`.
- `scripts/hoja_preguntas.py` y su test: salen A-18 y A-33.
- `docs/adr/0040-*.md`: recuadro de enmienda; `docs/adr/README.md`: «ACTIVE (con enmienda de
  ADR-0073)».
- Ningún valor de parámetro ni ninguna forma ejecutable cambia; solo las notas de RN-011 y RN-015 y
  la descripción de `base_calculo_objetivo` dicen que A-18 y A-33 están RESUELTAS. Ningún código.
- Líneas del cierre (commit del contrato): la deuda de F26, la G y R5.1 a A-56; HER:15 sale; R1.1
  pierde HER:15; entrada nueva de la Next Action por S-16.

## Fecha / fase

2026-10-11 · rama `trabajo/activar-sesion-04` (R1.1). Informe: `docs/validation/ACTIVAR-SESION-04.md`.

## Estado

ACTIVE
