---
status: ACTIVE
date: 2026-10-18
phase: post-F14 (rama `trabajo/plataforma-adelantada`, tramo R0 de la hoja de ruta; abre el tramo R6a)
---

# 0082 · La capa de MT5 que nunca decide una operación va antes de F26: ejecuta, frena, veta, mide y registra, y ninguna de sus entradas es un hecho ni un parámetro de la estrategia (enmienda MASTER_PLAN §0, la regla de PROJECT_STATE, ADR-0067 §1 y ADR-0068 §4)

> Decisiones de Aleks y del consultor del 2026-10-18 (encargo de `trabajo/plataforma-adelantada`,
> D1-D9, y la respuesta del consultor a la PARADA de su fase 0, que decide D4 y precisa D3 y D5:
> `docs/validation/PLATAFORMA-ADELANTADA.md`, «Respuesta del consultor a la PARADA»). Cada decisión
> lleva su autor. **Enmienda** el principio de `docs/plan/MASTER_PLAN.md` §0 («Validacion de
> fidelidad (F26) antes de cualquier MQL5», con una NOTA arriba: el cuerpo del plan no se toca), la
> regla de «Things That Must Not Be Changed» de `PROJECT_STATE.md`, **ADR-0067 §1** y **ADR-0068
> §4**, con recuadro en cada ADR y fila del índice. No cambia el motor, la spec, el registro, las
> guardias ni el código: no se escribe una línea de MQL5 ni de Python.

## Decision

### 1. D1 (Aleks, 2026-10-18) · Sí se adelanta, antes de F26, la capa de MT5 que no depende de la estrategia

Sus casos: la conexión; las órdenes stop idempotentes; el freno de peticiones (ADR-0067); el veto
antes de los cierres de mercado (ADR-0068 y `SymbolInfoSessionTrade`); el margen (ADR-0081); el
reloj del servidor (A-28); el journal y la reconciliación (§5 de este ADR); y el pre-vuelo de F33.

### 2. D2 (Aleks, 2026-10-18) · F29 y F30 siguen esperando a F26

El dominio de la estrategia en MQL5 (F29) y el harness Python-MQL5 (F30) no empiezan antes de F26.
La regla queda así, y sustituye a la de `MASTER_PLAN.md` §0 y a la de `PROJECT_STATE.md`:

> La validación de fidelidad (F26) precede a todo lo que decida operaciones en vivo (F29, F30 y lo
> de F31-F32 que dependa de ellos); la capa de plataforma de ADR-0082, que nunca decide una
> operación, puede ir antes.

### 3. D3 (consultor, 2026-10-18) · La frontera es una CONDICIÓN; la lista de D1 son sus casos

**La capa ejecuta, frena, veta, mide y registra, pero nunca decide una operación.** Su prueba:
ninguna de sus entradas es un hecho de la estrategia (sesgo, liquidez, caja, zona, escenario,
distancia del stop) ni un parámetro de categoría `estrategia`; lee solo cuenta, símbolo, sesiones
del símbolo, reloj, órdenes, posiciones, **los parámetros de firma, bróker, instrumento y
ejecución, y el perfil de cuenta (`knowledge/cuentas/`)** (la categoría `instrumento` y el perfil,
añadidos por la respuesta a la PARADA, punto 2: ninguno es un hecho de la estrategia, y sin ellos no
se limita un lote). Lo que no cumpla la condición, o deje duda, espera a F26: **niega por defecto**.
Una pieza nueva que una rama de R6a quiera meter en la capa entra si cumple la condición, aunque no
esté en la lista de D1; y una de la lista que no la cumpla se queda fuera.

Consecuencias, escritas como D3 las pide:

- **La capa sabe mover un stop; cuándo se pone el break even (ADR-0065) es de la estrategia.**
- **De ADR-0081 entran el tope por margen libre y por volumen y el rechazo por margen; el lote del
  riesgo es de la estrategia.** RN-011 (`knowledge/spec/strategy_spec.yaml:1419`) usa
  `riesgo_por_operacion`, de categoría `estrategia`, y la distancia del stop: la capa recibe un lote
  y lo limita; no lo calcula. **`lote_si_no_cabe`** (`ejecucion`, hoy `limitar`, DEFAULT_AMBIGUOUS
  bajo A-57, ADR-0081): su opción `no_operar` es un veto, porque la capa no elige qué operar, se niega
  a enviar lo que no cabe, leyendo solo cuenta, símbolo y un parámetro de ejecución. La capa cumple
  las dos opciones, con el valor que deje A-57 en la sesión 5 (respuesta a la PARADA, punto 3).
- **El veto de la firma entra en la capa con RN-029, RN-030 y RN-031**, que solo leen parámetros
  `prop_firm`, los acumuladores de pérdida de la firma y, RN-030, la posición viva
  (`strategy_spec.yaml:2138-2300`). **RN-032 se queda fuera y espera a F26**: lee
  `riesgo_por_operacion` y `base_calculo_riesgo`, los dos de categoría `estrategia`
  (`strategy_spec.yaml:2302-2356`). El encargo decía que las cuatro cumplían la condición; la fase 0
  lo midió y la respuesta a la PARADA (punto 1) lo decidió así.
- **RN-030 es del veto de la firma**, no una regla de la estrategia: ver el recuadro en ADR-0067 §1.

### 4. D4 (consultor, respuesta a la PARADA del 2026-10-18) · La capa vive en el EA de MQL5

**La capa es el EA de MQL5**, no un adaptador en vivo en Python. Por qué:

- El bot final es un EA (F29-F31 de `MASTER_PLAN.md` §A; ADR-0001:20-21, «exige dos
  implementaciones (Python y MQL5) que lean la misma fuente»): una capa en Python habría que tirarla
  al llegar F29.
- `docs/research/2026-09-03-del-corpus-al-bot.html:483` da cuatro razones para «que la ejecución
  final sea un EA MQL5 nativo», escritas para FundedNext. Cada una, como es:
  - el tope de 2.000 peticiones vale igual en FTMO (`docs/validation/FTMO-REGLAS.md:60`, R13;
    `firma_mensajes_dia_max` en el perfil, `knowledge/cuentas/ftmo-2step-swing-100k.yaml:327`): un
    bucle de Python que sondea gasta presupuesto; el EA reacciona a `OnTick`;
  - el Strategy Tester con ticks reales y el VPS sin puente **no tienen cita de FTMO en el repo**:
    son razones de la investigación, no se afirman para FTMO, y las mide R6a.1 (D7);
  - la equivalencia entre dos implementaciones (E6 del informe) es la de F30, y sigue valiendo.
- **Responde a la pregunta 1 de `docs/nocturno/BRECHA-EN-VIVO.md` §1 (`:62-66`)**: se descarta el
  EA que recibe las decisiones de Python, porque exige un puente en vivo que choca con el tope de
  peticiones; el dominio se porta a MQL5 en F29, después de F26; y antes de F26 solo va la capa de
  este ADR.

Lo que ADR-0067, ADR-0068 y ADR-0081 deciden hoy sigue siendo la referencia: el EA **porta**
`FrenoPeticiones` (`src/botsito/engine/freno.py`), `cierres_desde_sesiones` y `unir_cierres`
(`src/botsito/domain/cierres.py`) y el límite del lote (`limitar_lote`, `src/botsito/engine/broker.py`),
y lo de Python sigue siendo la referencia y lo que usa el simulador. **Cada pieza portada se prueba
contra los mismos casos que sus tests de Python; eso no sustituye a F30.** Enmienda, con recuadro,
ADR-0067 §1 («el adaptador real de MetaTrader usará la misma clase») y ADR-0068 §4 («el adaptador de
MetaTrader convierte… con `cierres_desde_sesiones` y… `unir_cierres`»). El docstring de
`engine/freno.py:7-8` dice lo mismo que ADR-0067 §1; es código, y lo arregla R6a.4 (deuda en
`PROJECT_STATE.md`).

### 5. La reconciliación de la capa (respuesta a la PARADA, punto 4)

En la capa, «reconciliación» quiere decir **reconstruir el estado al arrancar**: órdenes, posiciones
y journal contra la cuenta, con el test «reinicio a media jornada» de `MASTER_PLAN.md` §H.2 (fila
«Estado de jornada no persistente en el EA»). La reconciliación demo↔backtest sigue en F34: el
backtest es de la estrategia.

### 6. D5 (consultor, 2026-10-18) · Ninguna cifra escrita a mano en la capa

Los parámetros de firma, bróker, instrumento y ejecución, el perfil de cuenta y el calendario de
cierres (`knowledge/cuentas/cierres/<perfil>.yaml`) le llegan **generados desde el repo**, con sus
hashes en el journal. `MASTER_PLAN.md` §H.2 habla de dos hashes, y se dice como está: «F28:
`Params.mqh` (estrategia+instrumento+ejecucion) y `Risk.mqh` (prop_firm) con dos hashes en el
journal», con `spec_hash` y `risk_hash` en el journal de F23. El de `Params.mqh` mezcla la
estrategia. **Lo que la capa recibe antes de F26 lleva su propio hash, que se fija en R6a.2**
(respuesta a la PARADA, punto 5): no se decide ahora lo que R6a.2 va a medir. La parte de estrategia
de F28 espera a F26.

### 7. D6 (consultor, 2026-10-18) · Solo en DEMO hasta F35, y la condición 2 de N al pie de la letra

Hasta F35, la capa se niega a funcionar fuera de una cuenta DEMO, como
`tools/mql5/MedirDemoFTMO.mq5:759`:
`if((ENUM_ACCOUNT_TRADE_MODE)AccountInfoInteger(ACCOUNT_TRADE_MODE) != ACCOUNT_TRADE_MODE_DEMO)`.
Y la condición 2 de `docs/runbooks/RENOVAR-CIERRES.md` («Antes de que el bot corra en tiempo
real») se cumple al pie de la letra: la primera rama que conecta, R6a.1, trae la lectura de las
sesiones del símbolo con `SymbolInfoSessionTrade`, y R6a.5 la usa para el veto.

### 8. D7 (consultor, 2026-10-18) · MT5 no se supone: se mide

Cómo se compila y se prueba lo que haga falta en MT5 (MetaEditor por línea de órdenes en la máquina
de Aleks, el Strategy Tester o la demo) lo mide la fase 0 de R6a.1, con PARADA. Ningún
comportamiento de MT5 entra en un encargo como hecho sin medirlo en la demo o citarlo de la
documentación oficial de MQL5. El formato del journal se fija en R6a.1 pensando en F34, que compara
la demo con el backtest línea a línea: **un solo formato, versionado**.

### 9. D8 (Aleks, 2026-10-18) · En los huecos de espera, sin quitarle turno a F

Las ramas de la capa van en los huecos de espera (del trader, de FTMO, de la demo) y no le quitan
turno al camino crítico de F de la Next Action (hoy Y → V). La ganancia realista es de 1 a 2
meses, porque los 3 meses en sombra de F34 no se acortan: lo dice el Impacto.

### 10. D9 (consultor, 2026-10-18) · El orden: una rama por entrada, salvo que su encargo diga otra cosa

El tramo R6a de `docs/plan/HOJA-DE-RUTA.md`:

- **R6a.1**: conexión, reloj del servidor, sesiones del símbolo y journal; y, al arrancar, la
  comprobación de `ACCOUNT_MARGIN_MODE` (`MASTER_PLAN.md` §H, fila «MQL5: …», que la pone en F29 y
  F31).
- **R6a.2**: parámetros, perfil y calendario generados (D5).
- **R6a.3**: órdenes stop idempotentes y reconciliación (§5).
- **R6a.4**: freno de peticiones (ADR-0067, A-54) y veto de la firma (RN-029, RN-030 y RN-031).
- **R6a.5**: veto antes de los cierres de mercado (ADR-0068, A-55).
- **R6a.6**: tope por margen y volumen (ADR-0081, A-57), con la ejecución 3 de la demo, que mide
  cuándo comprueba MT5 el margen de una pendiente stop.
- **R6a.7**: pre-vuelo (`MASTER_PLAN.md` §H y §H.2: el hash de la spec contra el tag stable
  vigente, el desfase del reloj contra la tabla, `ACCOUNT_MARGIN_MODE`, `SymbolInfo`/`AccountInfo`
  contra el perfil; aborta si no cuadra).

Las ejecuciones 2 y 3 de la demo y A-28 siguen en el carril de Aleks (A.1): R6a.1 lee el desfase
del reloj, no lo decide.

> **CORRECCIÓN (2026-10-19, rama `trabajo/ea-conexion`, respuesta del consultor a la PARADA de su
> fase 0, punto 0).** En R6a.1, «la comprobación de `ACCOUNT_MARGIN_MODE`» al arrancar queda en
> **leerlo y registrarlo en el journal, sin abortar**. Motivo: no hay ningún valor con fuente con el
> que compararlo hasta que FTMO conteste si la cuenta Swing es de hedging (hoja de ruta A.2, P-D1);
> el perfil (`knowledge/cuentas/`) y el registro no traen modo de margen, y comparar con un valor sin
> fuente sería una cifra escrita a mano (D5). La comparación que aborta es la de R6a.7, y antes de
> ella hay que crear el parámetro del modo de margen con su fuente (la respuesta de FTMO).
> `docs/validation/EA-CONEXION.md`, «Respuesta del consultor a la PARADA».

## Problema que resuelve

La regla «la validación de fidelidad (F26) precede a cualquier MQL5» (`MASTER_PLAN.md` §0) dejaba
parada toda la plataforma detrás de F26, también lo que no depende de la estrategia y se puede
medir ya en la demo: la conexión, el reloj, las sesiones del símbolo, el freno, los cierres y el
margen. Y en el repo convivían dos lecturas de dónde vive en vivo lo que ADR-0067 y ADR-0068 ya
decidieron (un EA de MQL5, por MASTER_PLAN §A F31; o un adaptador Python que reutiliza las clases,
por la letra de ADR-0067 §1 y ADR-0068 §4), sin que nadie lo hubiera decidido (fase 0, b).

## Alternativas consideradas

1. **Mantener la regla**: nada de MQL5 hasta F26.
2. **Adelantar la capa como lista cerrada** (las piezas de D1, sin condición).
3. **Adelantar la capa como adaptador en vivo en Python** (`mql5bridge`), reutilizando
   `engine/freno.py` y `domain/cierres.py` tal cual.
4. **Un EA que solo ejecuta y recibe las decisiones de Python** (BRECHA-EN-VIVO.md §1, decisión 1).
5. **Esta**: la capa como condición, en el EA de MQL5.

## Por que elegimos esta opcion

Lo que la capa hace no depende de que la estrategia sea fiel: ejecuta, frena, veta, mide y registra.
Hacerlo en los huecos de espera adelanta la parte de la plataforma que más riesgo de MT5 tiene, sin
tocar lo que F26 tiene que medir. La condición (y no una lista) resuelve sola la pieza que nadie ha
pensado todavía, y ya decidió una pieza que el encargo daba por dentro (la tercera consecuencia de
D3 nombraba el veto de la firma «RN-029 a RN-032»): RN-032 se queda fuera. Y vive donde va a vivir
el bot (D4).

## Por que descartamos las demas

- (1) Deja esperando, sin motivo de fidelidad, lo que solo la demo puede medir.
- (2) Una lista no dice qué hacer con lo que no está en ella, ni saca lo que está y no debería: el
  veto de la firma enumerado como «RN-029 a RN-032» metía RN-032, que lee parámetros de la
  estrategia.
- (3) El bot final es un EA (F29-F31): la capa habría que tirarla al llegar F29 (D4).
- (4) Exige un puente en vivo que choca con el tope de peticiones (D4).

## Impacto

- **Lo que se gana es de 1 a 2 meses, no más (D8, Aleks)**: los 3 meses en sombra de F34
  (`MASTER_PLAN.md` §A, «3 meses en umbral») no se acortan.
- Documentos: la NOTA nueva de `docs/plan/MASTER_PLAN.md` (el cuerpo no se toca); la regla de
  `PROJECT_STATE.md` (la vieja va a HISTORIA); el tramo R6a de `docs/plan/HOJA-DE-RUTA.md`, R6.1 y
  R7.1; los recuadros en ADR-0067 §1 y ADR-0068 §4; las notas en ADR-0050 §4 y ADR-0053 §3.2
  («de la estrategia» quiere decir allí del bot; RN-029, RN-030 y RN-031 son el veto de la firma, y
  RN-032 espera a F26; respuesta del consultor a la revisión, 2026-10-18); y la deuda del docstring
  de `engine/freno.py`.
- Lo que NO cambia: el motor, la spec, el registro, las guardias, los hooks, el Makefile, `src/`,
  `tests/`, `mql5/` y `tools/`. F29 y F30 siguen detrás de F26 (D2). Las instantáneas congeladas
  (`MASTER_PLAN.html`, el informe de investigación) siguen diciendo lo que decían.
- Queda para la orden de cierre de la rama: la Next Action (F, N y las ramas de R6a en los huecos).

## Fecha / fase

2026-10-18 · post-F14, rama `trabajo/plataforma-adelantada` (tramo R0 de la hoja de ruta).

## Estado

ACTIVE (enmienda MASTER_PLAN §0, la regla de PROJECT_STATE, ADR-0067 §1 y ADR-0068 §4)
