# El contador de peticiones al servidor (R13)

Rama `feature/contador-peticiones`, 2026-09-30, desde `main` en `5731f71`
(`stable/F36-nocturno-01oct`). Es la B del Next Action. **Solo mide**: ninguna regla frena por
peticiones, y no cambia la spec, ningún parámetro, ninguna regla ni el motor de reglas.

## 1. De dónde viene

FTMO prohíbe «an excessive number of more than 2,000 server requests per day» (R13 de
`docs/validation/FTMO-REGLAS.md`; parámetro `firma_mensajes_dia_max` = 2000, CONFIRMED, en el
perfil y en `parametros.yaml`). Hasta hoy nada lo contaba: ningún módulo de `src/botsito/engine/`
leía el parámetro (`docs/nocturno/BRECHA-EN-VIVO.md` §3).

## 2. Qué cuenta, y qué no

**Lectura: la más estricta de R13, hasta que FTMO diga otra cosa.** La fuente dice «server
requests» y no aclara si una modificación, una cancelación o una petición rechazada cuentan. Aquí
cuentan todas.

| cuenta | tipo en el informe | método del bróker |
|---|---|---|
| colocar una orden límite o stop, **aceptada o rechazada** | `colocar` | `colocar_limite`, `colocar_stop` |
| modificar una pendiente, **aceptada o rechazada** | `modificar` | `modificar` |
| mover el stop de una posición viva (el break even de RN-014) | `modificar` | `mover_stop` |
| cancelar una pendiente | `cancelar` | `cancelar` |
| cerrar a mercado (RN-002, el fin de la ventana, el fin del día de ADR-0053 §6) | `cerrar` | `cerrar_a_mercado` |

**No cuentan:**
- lo que el servidor hace solo: llenar, expirar, saltar el stop o el objetivo;
- `abrir_conocida`, que repite una operación del trader y no la emite el bot;
- una petición que el bróker no admite (`BrokerError`): es un error de quien llama y la corrida se
  para, así que nunca llega a contarse.

**El día** se corta a medianoche CE(S)T, el mismo reloj del día de riesgo (ADR-0027): el
`firma_huso_corte` del perfil, Europe/Prague, con su horario de verano. Es el reloj con que el
bróker ya contaba `firma_posiciones_dia_max`.

## 3. Qué cambia

1. **`engine/broker.py`**: cada petición se apunta como `Peticion(instante_ms, tipo, id,
   aceptada)` y sale en `Traza.peticiones`. `peticiones_por_dia(peticiones, huso_corte)` las agrupa
   por día de la firma, con el total, cada tipo y las rechazadas. `ReglasBroker` gana
   `mensajes_dia_max`, que solo se informa.
2. **`engine/simulacion.py`**: `reglas_broker_de` lee `firma_mensajes_dia_max` del perfil.
3. **`engine/cableado.py`**: `TrazaBroker` guarda las peticiones de cada día. El informe de
   `motor arnes --simular` gana una sección al final:

   ```
   ### Peticiones al servidor (R13; dia de la firma en Europe/Prague)
   LECTURA: colocar, modificar, cancelar y cerrar, aceptadas o rechazadas, emitidas por el bot; solo se mide, nada frena
   dia | total | colocar | modificar | cancelar | cerrar | rechazadas
   ...
   maximo diario: <n> (<dia>); firma_mensajes_dia_max: 2000
   ```

   Salen **todos los días corridos**, también los que no tienen ninguna petición. El informe sin
   `--simular` no cambia.
4. **Tests**:
   - `tests/unit/test_peticiones.py`, cuatro funciones: cada tipo aceptado o rechazado cuenta, y el
     llenado, el objetivo y `abrir_conocida` no; nada frena aunque se pase del límite; el corte a
     medianoche CE(S)T en invierno y en verano; y el perfil da Europe/Prague y 2000.
   - `tests/unit/test_cableado.py`, dos funciones: la sección del informe sobre el día sintético,
     con una petición, y un día corrido sin peticiones, con cero.

## 4. Lo medido sobre construcción (en DIAGNÓSTICO)

`motor arnes --simular` sobre abril y agosto de 2026 (42 días `dev`), con los diagnósticos de la
noche del 30 de septiembre: A-35 `cierre_vela_contraria`, A-44 `sin_tope`, A-21
`solo_una_zona_de_control` y A-27 a 0 puntos. **No es una medida de nada que cuente**: el bot de
hoy casi no opera. La salida está fuera del repositorio y se reproduce con el comando de
`docs/runbooks/ARNES-MOTOR.md` y esos diagnósticos.

| | |
|---|---|
| días corridos | 42 |
| días con alguna petición | 11, con **1** cada uno (todas `colocar`) |
| días sin ninguna | 31 |
| peticiones en total | 11, de ellas **9 rechazadas**: los 9 rechazos del bróker del mismo informe |
| **máximo diario** | **1**, frente a `firma_mensajes_dia_max` = 2000 |

Las dos órdenes que se llenan cierran por stop o por objetivo, que no son peticiones. Con un bot
que opera una o dos veces por sesión y decide al cierre de M1 (ADR-0028), el límite queda lejos.
Lo que puede acercarlo es la vida de la orden stop (F35), que la reubica. **Esta medida hay que
repetirla cuando F35 entre.**

## 5. Lo que no hace

- **No frena.** No hay regla que prohíba al acercarse al límite; esa decisión es del consultor, y
  se toma cuando F35 dé cifras reales.
- **No define «petición» para el EA en vivo.** MT5 puede emitir peticiones que el bróker simulado
  no modela, como reintentos o consultas. Y el contador del EA tiene que sobrevivir a un reinicio
  (fila «Estado de jornada no persistente en el EA» del plan, H.2).
- **No cuenta las peticiones del trader** (`abrir_conocida`).

## Estado

Lista para revisión, **no cerrada**. `make check` en verde y sellado sobre la rama; la CI de Linux
va en el resumen de la sesión.
