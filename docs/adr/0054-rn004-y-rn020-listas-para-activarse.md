---
status: ACTIVE
date: 2026-09-26
phase: post-F14 (rama `trabajo/preparar-a35-a44`)
---

# 0054 · RN-004 y RN-020, listas para activarse con la respuesta del trader

> **ACEPTADO** por el consultor en la orden de cierre de `trabajo/preparar-a35-a44`, tras revisar
> `docs/validation/PREPARACION-A35-A44.md` y `docs/validation/VERIFICACION-A35-A44.md`.

## Decision

### 1. Los selectores de A-35 y A-44 son parámetros UNKNOWN, y sin fijar el motor se niega

- **A-35** (cuándo un pivote de M15 está formado): `liquidez_m15_pivote_formado`, `estrategia`,
  `enum`, **UNKNOWN**, con las dos lecturas que el corpus documenta y ninguna más:
  `inicio_vela_contraria` (v4 #942, `ev-v4-005749-1e9325cb`) y `cierre_vela_contraria` (v4 #846 y
  #849, `ev-v4-005053-885e2773`). El extremo lo marca la vela contraria al flujo de M15; el más
  reciente ya formado manda (ADR-0045). Vive en `domain/pivotes_m15.py`.
- **A-44** (el tope propio del trader): seis parámetros `perdida_trader_*`, todos **UNKNOWN**:
  alcance, magnitud, unidad, las dos cifras en dinero y el huso del reinicio.
- **Sin fijar no es un valor válido.** El arnés y el visor se niegan tras la compuerta de
  construcción, nombrando la ambigüedad y sin leer una vela.
- **El modo diagnóstico es la única excepción.** `--diagnostico-a35 <lectura>` y
  `--diagnostico-a44 <sin_tope|marcador|marcador_cero>` corren con un valor hipotético. Cada línea,
  cada fichero y cada página llevan `DIAGNOSTICO-A35-<lectura>` o `DIAGNOSTICO-A44-<modo>`, y nada
  de eso puede alimentar una medida de fidelidad ni un conjunto de medición. Con el parámetro ya
  fijado, pedir el diagnóstico se rechaza. No es «un modo que no bloquee» (lo que ADR-0048 y
  ADR-0049 H4 rechazaron): los gates se evalúan con el valor hipotético, no se saltan.
  *(Nota del 2026-09-26, rama `trabajo/preparar-a21`: el NOMBRE del fichero lleva la forma
  compacta `DIAGNOSTICO.a35=<lectura>.a44=<modo>[.a21=<lectura>]` por el límite de 260 caracteres
  de Windows; las líneas y las páginas siguen llevando las etiquetas completas. El contrato no
  cambia: un fichero de diagnóstico nunca se llama como una línea base.)*
- Activar cada regla es escribir un valor y correr un comando: `docs/runbooks/ACTIVAR-A35-A44.md`.

### 2. El tope del trader tiene tres estados y es independiente de la firma

- **SIN FIJAR**: el motor se niega (salvo diagnóstico).
- **`sin_tope`**: respuesta válida; RN-020 nunca bloquea.
- **Un valor concreto**: alcance (día, semana o ambos), magnitud (saldo o equity), unidad
  (porcentaje sobre las bases CONFIRMED de la sesión 1, o dinero) y huso del reinicio. Si el trader
  no da huso, se usa el corte del perfil de cuenta y la traza lo marca **SUPUESTO**.
- Ningún campo `firma_*` se reutiliza (`engine/tope_trader.py`). Con los dos límites activos se
  aplica el que se toque primero y el informe de simulación dice cuál fue y cuándo.

### 3. La corrección del cableado del selector

La primera versión exigía que la vela que toma el nivel fuera **posterior** a la vela contraria, y
eso dejaba el selector sin efecto en el motor: medido por el arnés real, las dos lecturas daban
trazas idénticas. Ahora la vela que puede tomar el nivel es la última M15 cerrada **si el pivote ya
existía antes de su cierre** (`formado_en < fin`), y la traza lleva la huella del selector en las
anotaciones `liquidez_m15` y `liquidez_m15_alcanzada` (`VERIFICACION-A35-A44.md` §1).

### 4. La granularidad de la toma de RN-004 es PROVISIONAL, ligada a A-45

Ninguna fuente fija qué vela tiene que «cerrar con cuerpo» (`VERIFICACION-A35-A44.md` §2). Evaluar
al cierre de M15 fue una elección de implementación. Se mantiene como **PROVISIONAL** hasta que el
trader responda **A-45**, con tres lecturas: al cierre de M15 (la actual), al cierre de M1 o al
tick. En construcción, en 13 operaciones el trader entró antes del cierre de la M15 en la que una
M1 ya había tomado el nivel; ese dato no decide la lectura.

### 5. Un empate entre gates que solo prohíben no es un aviso de H3

Los seis avisos de la línea base eran RN-001 y RN-033 dando SÍ a la vez: dos gates cuyo `entonces`
solo prohíbe. Las prohibiciones se acumulan y una prohibición gana siempre (ADR-0018 §1), así que en
cualquier orden el evento termina igual. `_empate_inocuo` deja de anotar ese caso y solo ese; un gate
que además hace algo sigue avisando. Complementa ADR-0049 H3.

## Problema que resuelve

La reunión con el trader tiene que convertir sus respuestas en reglas activas sin decidir nada por
él. Sin este ADR, cada respuesta obligaría a escribir el mecanismo después, con la respuesta en la
mano y la tentación de ajustarlo a ella.

## Alternativas consideradas

1. Selectores UNKNOWN con diagnóstico rotulado (elegida).
2. Un valor provisional por defecto para cada selector.
3. Esperar a la respuesta para escribir el mecanismo.

## Por que elegimos esta opcion

Porque el mecanismo queda probado antes de la respuesta y la respuesta solo elige un valor. El
diagnóstico permite ver el embudo sin que ninguna cifra cuente.

## Por que descartamos las demas

- **(2)** es un mecanismo inventado haciéndose pasar por método del trader (ADR-0045 lo prohibió
  para A-35).
- **(3)** deja la activación para después de la reunión, que es cuando más fácil es ajustar el
  mecanismo a la respuesta.

## Impacto

- `domain/pivotes_m15.py`, `engine/diagnostico.py`, `engine/tope_trader.py`; `alcanza_nivel` y
  `cruza` en `engine/primitivas.py`; `DatosMercado` con M15 y M1; el cableado de RN-020 en
  `engine/cableado.py`; `_empate_inocuo` en `engine/interprete.py`.
- Registro: `liquidez_m15_pivote_formado` y los seis `perdida_trader_*`, todos UNKNOWN; spec
  13.2.0.
- Nace A-45; la hoja de la sesión 02 la lleva justo después de A-35.
- `docs/runbooks/ACTIVAR-A35-A44.md`, `scripts/verificacion_a35_a44.py`.

## Fecha / fase

2026-09-26 · rama `trabajo/preparar-a35-a44`.

## Estado

ACTIVE
