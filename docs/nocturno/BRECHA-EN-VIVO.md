# La brecha hasta ejecutar en vivo en FTMO

Escrito en la sesión autónoma de la noche del 30 de septiembre al 1 de octubre de 2026, rama
`trabajo/nocturno-01oct`. **Es un inventario, no un diseño**: qué hay en el repositorio, qué falta,
qué funcionalidad del plan lo cubre y qué hay que decidir antes. No hay una línea de código de
conexión, y no se ha conectado nada a MetaTrader, a un bróker ni a una cuenta.

Cada «lo que hay» está comprobado contra el árbol de esta rama esa misma noche. Donde el encargo de
la noche daba por supuesto algo que el repositorio contradice, se dice con su nombre (punto 2).

**Sobre los números de funcionalidad.** En este documento `F23`, `F28`, `F31`… son los de la tabla A
de `docs/plan/MASTER_PLAN.md`. No son los de los tags (`stable/F31c-memoria-suite`) ni los de
`docs/nocturno/PLAN-01oct.md`, que siguen la numeración de los tags. Para no confundirlos, aquí
van siempre con su nombre.

## 0. El resumen

Lo que existe es un **simulador**: la spec ejecutable, el motor que la interpreta, un bróker
simulado con ticks, la capa de cuenta de FTMO y el veredicto de la firma, todo en Python y sobre
datos congelados. **De la fase 6 del plan —la ejecución en MetaTrader 5— no existe nada más que un
script de medición**: los directorios de `mql5/` solo tienen su `README.md`, y los paquetes
`botsito.mql5bridge` y `botsito.viewer` son un docstring.

| Punto | Lo que hay | Lo que falta | Lo cubre (plan maestro) |
|---|---|---|---|
| 1. Adaptador de MT5 | un script de medición en demo | todo lo demás | F28 a F32 |
| 2. Pérdida diaria | simulada y cableada, con el corte a medianoche de Praga | el mismo freno dentro del EA, contra la equity real | F31 (veto de riesgo), F30 |
| 3. 2.000 peticiones al día | el parámetro y una decisión de diseño | el contador, en el simulador y en el EA | F23 (diario), F31 |
| 4. Reconciliación | nada | todo | F34, con F33 antes |
| 5. Arranque y recuperación | nada que persista | todo | F23, F31 |
| 6. Registro de operaciones | informes del simulador, no un diario | el diario versionado y compartido | F23 |

Antes de todo eso hay una brecha anterior, que no es de plataforma: **el bot simulado todavía no
opera como el trader** (§7). Un adaptador perfecto ejecutaría hoy en vivo una estrategia que en
diagnóstico coincide con el trader en 0 de 77 operaciones.

## 1. El adaptador de MetaTrader 5

**Lo que hay.**
- `tools/mql5/MedirDemoFTMO.mq5`: un script que mide en una cuenta DEMO lo que ADR-0057, A-27 y
  A-28 dejaron pendiente, escribe un CSV y se niega fuera de una demo. Lo ejecuta Aleks a mano
  (`docs/runbooks/DEMO-FTMO.md`); `scripts/leer_demo_ftmo.py` lee el CSV. Es medición, no ejecución.
- `mql5/README.md` declara el destino: `Include/Botsito/Params.mqh` generado desde
  `knowledge/spec/`, `Scripts/RunCases.mq5`, `tester/`. Los cuatro subdirectorios solo tienen su
  `README.md`.
- `src/botsito/mql5bridge/__init__.py` es un docstring.
- La arquitectura sí está decidida: el dominio no puede importar `MetaTrader5` (contrato de
  import-linter en `pyproject.toml`), y el plan no prevé un puente Python en vivo sino **un Expert
  Advisor en MQL5 con el dominio reescrito y probado por diferencia contra Python**.
- El bróker simulado (`engine/broker.py`, ADR-0052 y ADR-0057) ya expone el contrato que el motor
  usa —colocar, modificar, cancelar, cerrar a mercado, leer `operacion_abierta` y
  `orden_limite_pendiente`— con órdenes límite y stop, rechazo por lado equivocado y por stops
  level. Es lo más parecido a una interfaz de adaptador que hay, y es PROVISIONAL hasta la demo.

**Lo que falta.** La exportación de la spec a MQL5, el dominio en MQL5, el arnés diferencial, el
Expert Advisor con órdenes idempotentes y códigos de retorno, y la paridad con el Strategy Tester.

**Funcionalidades del plan.** F28 `mql5-spec-export`, F29 `mql5-domain`, F30
`differential-testing`, F31 `mql5-expert-advisor`, F32 `strategy-tester-parity`.

**Decisiones que hacen falta.**
1. **Si el plan de la fase 6 sigue valiendo.** El plan maestro es del 2026-09-04 y prevé reescribir
   el dominio en MQL5. Desde entonces el motor pasó a ser un intérprete de la `forma` de la spec
   (ADR-0030) con primitivas escritas a mano. Hay que decidir qué se porta: el intérprete entero
   más sus primitivas, o un EA que solo ejecuta y recibe las decisiones de Python. Lo segundo exige
   un puente en vivo que el plan no tiene y que choca con el límite de peticiones (punto 3).
2. **Los valores del instrumento y del bróker**, que hoy son DEFAULT_AMBIGUOUS o UNKNOWN: lote
   mínimo, paso, stops level, freeze level y modos de llenado (A-27); el desfase del servidor y su
   regla de horario de verano (A-28); si una pendiente del lado equivocado se rechaza como el
   simulador supone (ADR-0057). Todo sale de los tres CSV de la demo (Next Action A2), que aún no
   existen en el repositorio.
3. **La rejilla H4 del servidor frente a `anclaje_h4`.** El sesgo y, desde ADR-0060, el cierre de
   RN-002 cuelgan de esa rejilla. `PERIOD_H4` nativo de MetaTrader sigue el reloj del servidor; si
   no coincide con `anclaje_h4` todo el año, el EA tiene que agregar su propia H4.

## 2. El límite de pérdida diaria, y con qué reloj se corta

**El encargo decía «en hora del servidor». El repositorio dice otra cosa, con fuente oficial, y
gana la fuente:** FTMO recalcula el límite diario «at 00:00 CE(S)T», y el reloj del servidor de
MetaTrader es «GMT+2 +DST», que es otro (`docs/validation/FTMO-REGLAS.md`, R2 y R10). ADR-0027
decidió por eso que el día de riesgo se corta a la medianoche civil de Europa central y que el
reloj del servidor no interviene. **El EA no puede usar `TimeCurrent()` a secas para el corte del
día**: tiene que convertir el reloj del servidor a CE(S)T, y para eso necesita A-28.

**Lo que hay.**
- La regla, con su cita: `firma_perdida_diaria_max`, `firma_base_perdida_diaria`
  (`saldo_corte_diario`), `firma_magnitud_vigilada` (equity) y `firma_huso_corte`
  (`Europe/Prague`) en `knowledge/cuentas/ftmo-2step-swing-100k.yaml`.
- La cuenta simulada (`engine/cuenta.py`, ADR-0050): corte a cada medianoche del huso del perfil,
  límite del día desde el saldo del corte, equity vigilada con la peor marca, suspensión con
  motivo e instante exactos.
- Las reglas del bot que frenan ANTES del límite: RN-029 (diario), RN-031 (total), RN-032 (no abrir
  lo que no cabe) y RN-030 (cerrar a mercado), con `firma_margen_seguridad` (ADR-0031), cableadas
  al motor por ADR-0053.
- Una guardia al arrancar: el cableado se niega si la medianoche de `huso_operativa` y la del
  perfil no coinciden en los días que va a correr («no hay un solo reloj»). Desde ADR-0063 de esta
  noche, ese reloj queda separado del de las sesiones.
- Una regresión con datos reales: la cuenta del 7 de agosto de construcción suspende en el tick
  del pico.

**Lo que falta.**
- El freno dentro del EA, contra la equity real, que incluye comisión y swap ya cobrados.
- La conversión del reloj del servidor a CE(S)T dentro del EA, probada en las dos semanas del año
  en que Europa y el servidor pueden no cambiar de hora a la vez (por eso las tres ejecuciones de
  la demo alrededor del 25 de octubre).
- El saldo del corte de medianoche cuando el EA arranca a media jornada (punto 5).
- En el simulador, dos piezas PROVISIONALES de ADR-0053: los eventos del bróker llegan al motor en
  el siguiente cierre de M1 (§2.1), y el cierre de RN-030 se ejecuta al precio de cierre de M1
  (§5.1). En vivo la equity se mueve por tick.

**Funcionalidades del plan.** F31 `mql5-expert-advisor` (el veto de riesgo), F30
`differential-testing` (que Python y MQL5 veten lo mismo) y la fila «Veto de riesgo solo en MQL5»
de la tabla H.2 del plan.

**Decisiones que hacen falta.**
1. **Si RN-030 en vivo actúa por tick o al cierre de M1.** ADR-0028 lo permite por tick; el
   simulador lo hace al cierre. Con el margen de seguridad actual hay que medir cuánto puede caer
   la equity dentro de un minuto.
2. **Si el margen de seguridad basta en vivo**: el deslizamiento del cierre a mercado no está
   medido (queda para la demo).
3. **La comisión real** (por lado o por operación completa, y su importe): cambia la equity que la
   firma vigila. Es la urgencia que ya encabeza Next Action.

## 3. El límite de 2.000 peticiones al servidor por día

**Lo que hay.**
- La regla con su cita (`FTMO-REGLAS.md`, R13) y el parámetro `firma_mensajes_dia_max` en
  `knowledge/spec/parametros.yaml`, CONFIRMED.
- Una decisión de diseño que existe para no acercarse: la fase de estrategia va al cierre de M1 y
  no por tick (ADR-0028).
- Los otros dos límites de R13 sí se simulan: `firma_ordenes_simultaneas_max` y
  `firma_posiciones_dia_max` producen rechazos en `engine/broker.py`.

**Lo que falta.**
- **Nada cuenta peticiones.** Ningún módulo de `src/botsito/engine/` lee `firma_mensajes_dia_max`:
  ni el bróker simulado cuenta las que emite el bot, ni hay una regla que frene al acercarse.
- La definición de «petición». La fuente dice «server requests»; no dice si una modificación, una
  cancelación o una orden rechazada cuentan, ni con qué reloj se corta el día.
- El contador persistente en el EA: si se reinicia a media jornada, el contador no puede volver a
  cero (fila «Estado de jornada no persistente en el EA» de la tabla H.2 del plan).

**Funcionalidades del plan.** F23 `engine-event-loop` (el diario, de donde saldría el recuento en
simulación) y F31 `mql5-expert-advisor`.

**Por qué importa ahora y no al final.** La rama 3 de ADR-0056 —la orden stop que nace en el
posible punto de breaker y **se mueve con él**— es la pieza de la estrategia que más peticiones
puede emitir: una modificación por cada M1 en que el punto cambie, en dos sesiones al día. Conviene
contar las peticiones en el simulador **antes** de diseñarla, no después.

**Decisiones que hacen falta.**
1. Qué cuenta como petición y con qué reloj se corta el día (preguntar a FTMO, o tomar la lectura
   más estricta: toda llamada que llega al servidor, aceptada o no).
2. El margen: a qué fracción del límite el bot deja de emitir, y qué hace entonces con una orden
   viva (dejarla, cancelarla). Es una regla nueva de la spec, con su parámetro.
3. Si se añade ya el contador al bróker simulado, para que el arnés lo informe por día.

## 4. La reconciliación con el bróker

**Lo que hay.** Nada. La palabra no aparece en `src/`. En el simulador no hace falta: el estado del
bróker y el del motor son el mismo objeto.

**Lo que falta.**
- Al arrancar y periódicamente: comparar lo que el bot cree —órdenes pendientes, posición, stop,
  objetivo, lote— con lo que el servidor tiene, y una regla para cada diferencia (orden que el bot
  no conoce, posición sin stop, stop que no está donde el bot lo puso, llenado parcial).
- La identidad de las órdenes: número mágico y comentario con el hash de la spec y el número de
  cartucho, que es lo que permite decir «esta orden es mía» (plan, tabla H.2).
- La reconciliación diaria demo ↔ simulación: las operaciones de la demo contra las que el
  simulador habría hecho con los mismos datos, con su triaje de divergencias.

**Funcionalidades del plan.** F31 `mql5-expert-advisor` («órdenes idempotentes… nunca duplica»),
F33 `demo-deployment` (el pre-vuelo «aborta si no cuadra») y F34 `shadow-reconciliation`
(«reconciliación diaria demo ↔ backtest… 3 meses en umbral»).

**Decisiones que hacen falta.**
1. Qué hace el bot ante una diferencia: parar y avisar, o corregir solo. La lectura conservadora es
   parar sin tocar lo que no reconoce y dejar la decisión a una persona.
2. La tolerancia de la reconciliación diaria (cuántos puntos y cuántos segundos separan «igual» de
   «divergencia»), que tendría que pre-registrarse como se hizo con el criterio de fidelidad
   (ADR-0043).
3. Si los tres meses de demo de F34 siguen siendo la condición de paso a real.

## 5. El arranque y la recuperación tras una caída

**Lo que hay.** Nada que persista. El estado del motor —hechos fijados, refracciones, cartuchos,
la memoria del productor de zonas por sesión— vive en memoria dentro de una corrida; en la
simulación de varios días la cuenta pasa de un día al siguiente y la estrategia y el bróker
empiezan de cero cada día. Ningún módulo de `src/botsito/engine/` escribe ni lee estado (el único
que escribe ficheros es el visor).

**Lo que falta.**
- Reconstruir la jornada al arrancar: qué sesión es, qué hechos están fijados (sesgo, liquidez
  tomada, zonas), cuántos cartuchos quedan, qué pérdida lleva el día y la semana, cuántas
  peticiones se han emitido, cuál fue el saldo del corte de medianoche.
- Qué hace el bot si arranca con una posición o una orden viva que no puede explicar.
- Qué pasa durante la caída: el stop y el objetivo están en el servidor y siguen valiendo; **el
  cierre de RN-002 —antes del fin de la vela H4 y al fin de la ventana—, el break even de RN-014 y
  el cierre de RN-030 no**: los ejecuta el bot, y sin bot no ocurren.
- El pre-vuelo: que el símbolo, los dígitos, el contrato, el stops level, el reloj y la rejilla H4
  del terminal son los que la spec espera, y si no, no arrancar.

**Funcionalidades del plan.** F23 `engine-event-loop` (diario versionado), F31
`mql5-expert-advisor` («al arrancar reconstruye la jornada desde el historial de MT5 y el journal;
test "reinicio a media jornada"») y F33 `demo-deployment` (pre-vuelo y runbooks).

**Decisiones que hacen falta.**
1. **De dónde se reconstruye**: del historial del terminal, de un diario propio en disco, o de los
   dos con el terminal mandando. El plan dice los dos; hay que decidir cuál gana si discrepan.
2. **Qué se hace con una posición viva durante una caída**: si la protección mínima (stop y
   objetivo en el servidor) basta, o si el cierre de RN-002 tiene que ir también en el servidor
   —por ejemplo con la caducidad de la orden pendiente— para no depender de que el bot esté vivo.
   Afecta a cómo se coloca la orden, así que se decide antes de F31.
3. Tras una caída a media sesión, si el bot retoma la sesión o la da por perdida. El trader no ha
   dicho nada parecido; es una decisión del consultor.
4. Dónde corre el terminal (la máquina de Aleks o un servidor), que decide cuántas caídas hay que
   esperar. El plan no lo dice.

## 6. El registro de operaciones

**Lo que hay.**
- En simulación: `cuenta.Operacion` con instantes, precios, lote, cargos y marcas; los eventos del
  bróker con su motivo; el informe de `motor arnes`, idéntico byte a byte entre corridas; y el
  detalle por día del visor (`docs/runbooks/VISOR-DIAS.md`).
- `Registro` anota qué defaults de ambigüedad se han leído, pensado para que el diario lo recoja.
- El criterio para comparar operaciones del bot con las del trader (ADR-0043).

**Lo que falta.**
- **El diario.** `engine/__init__.py` lo promete («Reloj determinista, bucle de eventos, journal»)
  y no existe ningún módulo que lo escriba. El plan lo describe: un esquema versionado y
  compartido entre Python y MQL5, con instante UTC, desfase del servidor, evento, regla, condición
  fallida, `spec_hash`, `risk_hash` y las lecturas ambiguas.
- En vivo, además: la petición enviada, el código de retorno, el precio pedido y el obtenido, el
  deslizamiento, y el ticket del servidor.
- Dónde se guarda, cuánto tiempo y cómo se versiona. En el repositorio, `data/` está fuera de git.

**Funcionalidades del plan.** F23 `engine-event-loop` (el diario), F25 `viewer` («igualdad con
journal»), F31 `mql5-expert-advisor` y F34 `shadow-reconciliation`, que lo consume.

**Decisiones que hacen falta.**
1. El esquema, antes de escribir el EA: es la pieza que comparten las dos mitades, y el arnés
   diferencial de F30 compara diarios.
2. Si el informe del arnés pasa a generarse desde el diario, para que no haya dos descripciones de
   la misma corrida.
3. Qué se conserva de cara a la firma: si FTMO retira operaciones del historial (R18), el diario
   propio es la única prueba.

## 7. Lo que va antes de todo lo anterior

No estaba en la lista del encargo, pero es la parte mayor de la brecha, y ninguna es de plataforma.

1. **La fidelidad.** En diagnóstico sobre construcción, tras esta noche, el bot simulado hace 2
   operaciones puntuables y coincide con el trader en **0 de 77** (`docs/nocturno/INFORME-01oct.md`).
   Faltan la vida de la orden stop y la caja por operación (ADR-0056 §4 y §7), RN-007, y las
   ambigüedades bloqueantes que siguen abiertas. Ninguna cifra de fidelidad se ha medido todavía
   fuera de diagnóstico.
2. **La viabilidad.** Con 10 USD de ida y vuelta por lote —5 por lado, el supuesto conservador
   del perfil— la esperanza neta de las operaciones anotadas del propio trader no queda por
   encima de cero con su intervalo; con 3 o con 5 USD, sí (`docs/validation/VIABILIDAD-TRADER.md`
   y `docs/validation/VIABILIDAD-COMISION.md`). Cuál es la comisión real lo dice el CSV de la demo.
3. **Las mediciones de la demo** (A-27, A-28, ADR-0057): tres ejecuciones de Aleks, la primera
   antes del 25 de octubre.
4. **El gap trading de FTMO** (R15): el bot no tiene calendario de cierres de mercado, y R15 frente
   a R6 sigue sin respuesta de FTMO. Bloqueada esta noche por falta del dato.
5. **A-42**: con qué reloj cuenta el trader su ventana en invierno. El mecanismo está desde esta
   noche (ADR-0063, PROPUESTO); el valor no, y el cambio de hora es el 25 de octubre.
6. **El holdout**: `fidelidad-1` y siguientes siguen cerrados, y el memorando de paso a real
   (F35 `go-live-gate`) exige F27 y F34 antes.

## Estado

Documento de inventario, escrito sin conexión a nada. No decide nada: cada «decisiones que hacen
falta» es de Aleks. Pendiente de su revisión.
