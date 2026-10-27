---
status: ACTIVE
date: 2026-10-26
phase: post-F14 (rama `trabajo/activar-sesion-05-motor`, R4.1 de la hoja de ruta)
---

# 0084 · La mecha que pasa el nivel de M15 y vuelve lo mueve a esa mecha: `liquidez_m15_mecha_que_vuelve` bajo A-35 (enmienda ADR-0045)

> Decisión del consultor del 2026-10-26 (encargo de `trabajo/activar-sesion-05-motor`, punto 1, y
> su respuesta a la PARADA, puntos 0 y 1), sobre lo que el trader dijo en la sesión 5 (S-3,
> segunda mitad de A-35). **Enmienda ADR-0045** en la frase «no se sustituye por un parámetro
> provisional, porque es un mecanismo y no una cifra» (recuadro en su Decisión y fila del índice)
> y lleva NOTA en ADR-0054, «Por qué descartamos las demás», (2). Lo que el trader no dijo va
> marcado como **LECTURA DEL CONSULTOR** o **DECISIÓN DEL CONSULTOR**. A-35 sigue ABIERTA.

## Decision

### 1. Lo que dijo el trader

A la segunda pregunta de A-35 («¿y qué haces si después el precio lo supera un poco?») contestó
en la sesión 5: «Ah, se actualiza el de la mecha Se actualiza el de la mecha»
(`ev-v15-000553-9d95178a`, v15 0:05:53; afirmación: si el precio pasa el alto de M15 solo con la
mecha y vuelve, el alto pasa a ser el de esa mecha). Lo enseñó en su replay con el caso de la
vela contraria que deja la mecha y cierra roja por debajo, y dijo que en un bajo es lo mismo:
las dos cosas están en `SESION-05-EXTRACCION.md` §3.1 (S-3), fuera de un ítem, y aquí se
remiten sin citarlas.

### 2. El mecanismo, en `domain/pivotes_m15.py`

Dos casos caben en el ítem, y el motor hace los dos según el selector:

- **(i) La mecha de la propia vela contraria.** La contraria que forma el alto pasa con su mecha
  el extremo de la racha y cierra por debajo: el nivel es su mecha (`_pivote_de`, con
  `solo_la_contraria` o `cualquier_mecha`). Es el caso del ejemplo del replay (§3.1). Hasta hoy
  el módulo lo dejaba «fijo y visible» al revés: el extremo de la racha, sin la mecha.
- **(ii) La mecha de una M1 posterior.** Con el pivote ya formado, una M1 que lo pasa con la mecha
  sin cruzarlo con `liquidez_m15_criterio_toma` (`cuerpo`, ADR-0062) no es toma, y el nivel pasa
  a esa mecha (`nivel_con_mecha_que_vuelve`, solo con `cualquier_mecha`). Que (ii) también valga
  es **LECTURA DEL CONSULTOR**: el ítem contesta a «si después el precio lo supera un poco», que es
  (ii), y el ejemplo es (i); el trader no eligió entre los dos.
- **El nivel se congela al tomarse: DECISIÓN DEL CONSULTOR** (respuesta a la PARADA, punto 1; no
  sale de ningún ítem, y tiene efecto: una M1 que cierra con cuerpo sobre el nivel ORIGINAL ya no
  es toma si una mecha anterior lo movió). `nivel_con_mecha_que_vuelve` recorre las M1 cerradas desde
  que el pivote está formado: cada una que lo pasa solo con la mecha lo mueve; la primera que lo
  cruza con el criterio lo toma y las siguientes ya no lo mueven. Medido en la fase 0
  (`ACTIVAR-SESION-05-MOTOR.md` §0.b.4): el productor de la zona guarda `(lado, nivel,
  formado_en)` como identidad de la toma (`engine/zonas.py`, `_toma_del_momento`); si el nivel
  siguiera moviéndose tras la toma, cada M1 posterior con mecha abriría una «toma nueva».
- **En un bajo, en espejo**: DECISIÓN DEL CONSULTOR (el ítem habla del alto; que en bajista «sería
  lo mismo» está en §3.1 fuera de un ítem). La sesión 6 lo confirma.
- **Lo aplica quien tiene las velas**: `DatosMercado.liquidez_m15` (`engine/motor.py`) pasa el
  selector a `pivote_mas_reciente` (caso (i)) y, con `cualquier_mecha`, las M1 desde `formado_en`
  hasta el instante a `nivel_con_mecha_que_vuelve` (caso (ii)); el arnés y el visor le dan el
  selector y el criterio del registro. **Solo M15**: `domain/estructura_m1.py` llama a
  `pivotes_formados` con velas de M1 y no pide ninguna mecha (`no_mueve`), así que la referencia
  del breaker, el punto de la orden y las zonas de control no se mueven (test por marco).

### 3. El selector: `liquidez_m15_mecha_que_vuelve`, y por qué enmienda ADR-0045

`liquidez_m15_mecha_que_vuelve`, `estrategia`, `enum` `[no_mueve, solo_la_contraria,
cualquier_mecha]`, **DEFAULT_AMBIGUOUS** en `cualquier_mecha` bajo A-35, fuente
`ev-v15-000553-9d95178a`, `consumido_por: [ADR-0084]`, escrito a mano y **sin registro de
feedback**: un registro pondría en boca del trader la elección entre (i) y (ii) que no hizo
(precedente: `perdida_trader_magnitud`, ADR-0054 §1, nota del 2026-10-26).

ADR-0045 dijo que A-35 «no se sustituye por un parámetro provisional, porque es un mecanismo y
no una cifra», y ADR-0054 descartó por eso «un valor provisional por defecto para cada selector».
**Este ADR enmienda esa frase de ADR-0045.** El motivo: aquella prohibición era contra un
mecanismo inventado que se hiciera pasar por método del trader (ADR-0054, «Por qué descartamos
las demás», (2)); este mecanismo lo dijo el trader (`ev-v15-000553-9d95178a`), y el valor
provisional solo elige su ALCANCE, que es lectura del consultor y va a la sesión 6. Error del
consultor, con su nombre: el encargo pidió un DEFAULT_AMBIGUOUS bajo A-35 sin leer ADR-0045 ni
ADR-0054; antes de proponer un valor provisional bajo una ambigüedad se lee el ADR que la abrió.

### 4. Contraste con la sesión 4 y con ADR-0062

- `ev-v10-012456-9dc1d221` («marcas un alto en m15 después el precio lo pasa por poco con la mecha
  y vuelve que haces pues no tiene la regla es que lo tiene que pasar con cuerpo no con mecha»):
  los dos ítems contestan a la misma pregunta. El de la sesión 4 dice que eso NO ES TOMARLO; el de
  la sesión 5, QUÉ NIVEL QUEDA. Con el nivel congelado al tomarse son compatibles: una mecha no
  toma (RN-004 exige cuerpo) y, mientras no haya toma, el nivel que se usa es el de la mecha. Es
  la tensión que este ADR deja escrita; la sesión 6 pregunta (i) o (ii).
- `ev-v10-020142-30fd2569` («un nivel en M15 … si es roto con mecha, se anula la entrada … en
  M1 … es válido con mecha y cuerpo»; A-32 RESUELTA en la sesión 5: la única ruptura que pide
  cuerpo es la de la zona lineal de M15): habla de la RUPTURA que habilita la entrada, que sigue
  pidiendo cuerpo (RN-004, `cruza`). Una mecha sobre el nivel sigue sin habilitar nada; lo que
  hace ahora es mover el nivel. No se contradice.
- ADR-0062 §1 (la toma la hace una M1 con cuerpo) no cambia: `alcanza_nivel` y `cruza` miran la
  última M1 cerrada contra el nivel ya movido, y `la_toma_es_de_la_sesion` también.

### 5. Lo que NO se decide aquí

- Cuál de las dos mechas vale (i o ii), y el bajo: la sesión 6 (línea R4.2 del cierre).
- Nada de M1: la vela sin cuerpo en M1 va en el ADR siguiente de esta rama (punto 2 del encargo);
  el punto de la orden, ADR-0064.
- Ninguna ambigüedad se cierra: A-35 sigue ABIERTA y bloqueante.

## Problema que resuelve

El trader dijo en la sesión 5 que el alto de M15 se actualiza a la mecha que lo pasa y vuelve, y
el motor lo dejaba fijo en el extremo de la racha (`pivotes_m15.py`, «fijo y visible»). Con el
arnés corriendo a secas (A-35 con valor desde `trabajo/activar-sesion-05`), la liquidez que toma
RN-004 no era la suya.

## Alternativas consideradas

1. Selector de tres opciones con `cualquier_mecha` por defecto, bajo A-35, y ADR-0045 enmendado
   (la elegida).
2. `solo_la_contraria` por defecto: solo el caso del ejemplo, y (ii) a la sesión 6.
3. Sin parámetro: `cualquier_mecha` fijo en el código y declarado aquí.
4. Esperar a la sesión 6.

## Por que elegimos esta opcion

Porque el ítem contesta literalmente a la pregunta del caso (ii) y el ejemplo enseña el (i); con
el nivel congelado al tomarse, hacer los dos no contradice la sesión 4. El valor vive en el
registro (ADR-0002) y cambia con un registro del trader.

## Por que descartamos las demas

- La 2 hace menos de lo que el trader dijo a la pregunta que se le hizo.
- La 3 deja un mecanismo sin puerta en el registro (ADR-0002).
- La 4 deja el motor con un nivel que el trader ya dijo que no es el suyo.

## Impacto

- **Registro:** `liquidez_m15_mecha_que_vuelve` (DEFAULT_AMBIGUOUS, `cualquier_mecha`, A-35,
  fuente `ev-v15-000553-9d95178a`); A-35 gana el parámetro en su lista y su texto lo dice; RN-004,
  sus notas. `spec_version` 18.1.9 → **18.2.0** (un parámetro nuevo).
- **Código:** `domain/pivotes_m15.py` (`_pivote_de` con la mecha de la contraria, el argumento
  `mecha_que_vuelve` de `pivotes_formados` y `pivote_mas_reciente`, `nivel_con_mecha_que_vuelve`;
  docstring), `engine/motor.py` (`DatosMercado` recibe el selector y el criterio y aplica los dos
  casos), `engine/arnes.py` y `engine/visor.py` (los leen del registro).
- **Docs:** recuadro en ADR-0045 y su fila del índice; NOTA en ADR-0054 y su fila.
- **Tests:** `tests/unit/test_pivotes_m15.py` (la mitad de la mecha de
  `test_lo_fijo_y_visible_doji_y_mecha_de_la_contraria` cambia de sentido a propósito y se parte
  en dos; (i) y (ii) en alto y en bajo con cada opción; la M1 que cruza con cuerpo toma y no mueve;
  dos mechas seguidas mueven dos veces) y `tests/unit/test_mecha_que_vuelve.py` (por el camino
  real: `DatosMercado.liquidez_m15` y `alcanza_nivel`/`cruza` con el registro vigente; un valor
  fuera del enum falla al leer el registro; las series de M1 no se mueven). Falla con el código
  de `main`: `ACTIVAR-SESION-05-MOTOR.md` §1.1.
- **Sin arnés y sin material**: velas sintéticas.

## Fecha / fase

2026-10-26 · rama `trabajo/activar-sesion-05-motor` (R4.1). Informe:
`docs/validation/ACTIVAR-SESION-05-MOTOR.md`.

## Estado

ACTIVE
