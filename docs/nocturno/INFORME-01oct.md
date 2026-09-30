# Informe de la noche del 30 de septiembre al 1 de octubre de 2026

Rama `trabajo/nocturno-01oct`, **solo en local**. Nada sobre `main`, ningún push, ninguna rama
cerrada ni borrada, ninguna credencial, ninguna conexión a bróker ni a MetaTrader, ninguna descarga
de datos ni dependencia nueva. El plan con el que empezó la noche es `docs/nocturno/PLAN-01oct.md`.

## 0. Lo primero: el cierre de la parte 2 terminó con la CI de `main` en ROJO

**`main` está en `67ab298`, subido al remoto, y su CI está en rojo.** No se ha tocado desde
entonces, como pedía la instrucción para este caso.

Lo que se hizo del cierre de `trabajo/memoria-suite`, en el orden pedido:

| Paso | Resultado |
|---|---|
| 1. Rama al día sobre `main` (`14e01bc`) | `09d6acd`, sin conflictos |
| 2. `make check` en la rama | verde y sellado |
| 3. Merge en `main`, `make check` en `main`, tag | merge `1cca80e`, tag `stable/F31c-memoria-suite` |
| 4. `docs(state)` solo en `PROJECT_STATE.md` | `67ab298`; la entrada PENDIENTE de A-27 (ADR-0057 §5) sigue como estaba, sin aplicar |
| 5. `git push --atomic` de `main` y del tag | hecho |
| 5. CI de `main` | **ROJA**: falla el paso `make check` a los 2 min 57 s, dentro de `pytest` |
| 6. Borrar `trabajo/memoria-suite` | **NO hecho**: exigía la CI en verde. La rama sigue en local, en `09d6acd` |
| 7. Clon de la sesión anterior (`scratchpad/wt-ci`) | sin tocar |

**Por qué falla, y qué no sé.** No he podido leer el log de la CI: bajarlo exige una credencial y
esa vía quedó denegada en el primer intento de la tarde; no busqué otra. Lo único medido es dónde
falla (el paso y el minuto). **Hipótesis, sin medir** —no hay un Linux en esta máquina para
reproducirlo—: `tests/unit/test_memoria.py::test_el_pico_del_proceso_sube_con_una_reserva_y_no_baja_al_soltarla`.
En Linux, el pico de memoria de un proceso hijo recién lanzado puede heredar el del `pytest` que lo
lanza, así que la subida que el test exige no se vería. En Windows el test pasa. Si es eso, el
arreglo es leer el pico de otra fuente en Linux; pero hasta ver el log es una suposición.

**Consecuencia para esta rama.** Sale de `14e01bc`, el último `main` con la CI en verde, y **no
contiene la memoria de la suite**. `state check` exige que `Last Stable Commit` nombre el tag más
reciente del repositorio, que es `stable/F31c-memoria-suite`, así que `PROJECT_STATE.md` lo nombra
con una nota que dice que esta rama no lo contiene.

## 1. Funcionalidades terminadas

Cada commit entró con `make check` en verde y sellado. La última corrida: 1419 tests, 12 min 23 s.

| Funcionalidad | Commit | Tests tras el commit | `spec_version` | ADR (PROPUESTO) |
|---|---|---|---|---|
| Plan de la noche | `3e006d0` | — | — | — |
| F32 · el sesgo con doble ruptura lo decide el color; RN-002 cierra antes del fin de la vela H4 | `6698426` | 1005 funciones, 1393 casos | 14.0.0 | ADR-0060 |
| F33 · cada sesión es un escenario propio: `liquidez_tomada` caduca al abrir la sesión | `bf1dc0b` | 1010, 1398 | 14.1.0 | — (A-46 ya RESUELTA; ADR-0055 §4) |
| F34 (1 de 2) · el stop se redondea alejándose de la entrada; el break even de RN-014 | `2cca34d` | 1015, 1403 | 14.2.0 | ADR-0061 |
| F34 (2 de 2) · la toma de RN-004 la hace una vela de M1 | `2763ceb` | 1015, 1403 | 14.3.0 | ADR-0062 |
| F36 · el reloj de las sesiones se separa del reloj del día de riesgo | `fad0305` | 1022, 1419 | 14.4.0 | ADR-0063 |

Los cuatro ADR van como PROPUESTOS en su título y en un recuadro; su campo `status` dice `ACTIVE`
porque la guardia de ADR no admite otro valor.

De paso, dos errores que ya estaban y que las medidas destaparon, arreglados con su test:

- **Una orden preparada y no enviada se arrastraba a la zona siguiente** (`CableadoError: la zona
  ligada no es la de la orden preparada`). Solo aparece con más de una zona al día, o sea desde
  F33. En `bf1dc0b`.
- **`scripts/embudo_77.py` no corría desde que A-47 se fijó**: pedía un diagnóstico que el motor ya
  rechaza. En `bf1dc0b`.

## 2. Lo medido

Todo sobre construcción —abril y agosto de 2026, 42 días `dev`, 84 sesiones, 49 con operaciones del
trader, 77 operaciones—, por la compuerta, **en DIAGNÓSTICO** (A-35 `cierre_vela_contraria`, A-44
`sin_tope`, A-21 `solo_una_zona_de_control`, A-27 con 0 puntos). **Ninguna cifra cuenta como medida
de fidelidad.** Ninguna corrida tocó mayo, marzo, febrero ni septiembre. **No se abrió nada nuevo**:
ni un libro xlsx, ni un fotograma, ni el texto de una transcripción. Las corridas leen los casos ya
ingeridos de construcción, como las ramas anteriores, así que no hay exposición que declarar.

| | antes de la noche | tras F32 | tras F33 | tras F34 (1 de 2) | tras F34 (2 de 2) | tras F36 |
|---|---|---|---|---|---|---|
| Sesiones que RN-033 prohíbe por sesgo ambiguo (de 84) | 15 | 0 | 0 | 0 | 0 | 0 |
| `orden_dimensionada` (sesiones de 49) | — | 15 | 26 | 26 | 14 | 14 |
| Operaciones puntuables del bot (simulado) | 6 | 5 | 8 | 8 | 2 | 2 |
| Cobertura: operaciones del trader que el bot iguala (de 77) | 2 | 2 | 2 | 2 | **0** | 0 |
| Rechazos del bróker simulado | — | 12 | 26 | 26 | 9 | 9 |

- **F32.** El sesgo de las 49 sesiones con operaciones pasa de 21 alcistas, 6 ambiguas y 22
  bajistas a 24 alcistas y 25 bajistas. Por operación: de 58 a favor, 7 ambiguas y 12 en contra a
  62 a favor y 15 en contra. RN-002 no llega a disparar en construcción: ninguna posición del bot
  sigue viva al vencer su vela H4.
- **F33.** El embudo de las 77 cambia de sitio: sesgo 15, liquidez 11, breaker 24, caja 22, bróker
  2, llenado 1, coincide 2.
- **F34 (1 de 2).** Operaciones, cobertura y embudo, iguales. RN-014 dispara en 3 sesiones de 84.
  El saldo final simulado pasa de 95.605,67 a 96.253,00.
- **F34 (2 de 2). Es la única pieza que empeora las cifras.** Con la toma en M1, `liquidez_tomada`
  se produce en 47 de 49 sesiones (antes 44), pero el productor encuentra menos esquemas: en el
  embudo, liquidez baja de 11 a 1 y breaker sube de 24 a 46; coincide, de 2 a 0. No se revirtió
  —la lectura la eligió el trader (A-45 RESUELTA)— y va **en su propio commit** para poder
  revisarla sola. Por qué encuentra menos esquemas está razonado leyendo el código en
  ADR-0062 §3, **no medido**.
- **F36.** El informe del arnés, simulado y sin simular, sale idéntico byte a byte antes y después.
  Con el selector en `grafico` solo está probado sobre días sintéticos: construcción es verano.

## 3. Bloqueadas y no intentadas

- **F35, la vida de la orden stop (rama 3 de ADR-0056): BLOQUEADA. Necesita una decisión tuya.**
  El plan de la noche la daba por desbloqueada «con selectores y diagnóstico». La estudié entera
  antes de escribir una línea, y no lo está. ADR-0056 §7 la describe, pero deja sin decidir las dos
  cosas de las que cuelga todo lo demás:
  1. **En qué precio nace la orden.** El ADR dice que el posible punto de breaker «es hoy
     `referencia_del_breaker`» —el último pivote de M1 contrario a la entrada— y manda la otra
     lectura a A-48. Pero el repositorio ya tiene medido que ese pivote no es el punto del trader:
     en `docs/validation/ORDEN-STOP-O-LIMITE.md` §4, su entrada está a 3 puntos o menos de
     `referencia` en 2 de las 39 operaciones con zona viva, con una mediana de 15 puntos antes del
     nivel. Y `docs/validation/BLOQUE-DE-LA-CAJA.md` §4.1 midió, en 12 cajas leídas en el vídeo, que
     la orden va en el 0 de la caja en 10 de 12. Son dos precios distintos.
  2. **Qué caja lleva una orden que nace antes de la ruptura**, que es de donde salen su stop y su
     lote. El ADR la remite a la caja por operación (§4, la rama 4) y a los selectores `caja_bloque`
     y `caja_vela`, que no existen. A-48 y A-49 siguen ABIERTAS.

  Escribirla con el pivote era construir la vida de la orden sobre un punto que la medida
  desmiente; escribirla con el 0 de la caja era elegir yo entre las lecturas de A-48. En los dos
  casos inventaba la decisión. Además pide reescribir RN-008 «o parar» y un diagnóstico nuevo
  (`--diagnostico-a29`). Es lo que más pesa hoy: desde F34 (2 de 2), sin esta rama y sin la caja
  por operación el bot no iguala ninguna operación del trader.
- **La caja por operación (ADR-0056 §4, rama 4): NO INTENTADA.** Va detrás de la rama 3 y depende
  de las mismas dos decisiones.
- **RN-007, la vela casi plana: BLOQUEADA.** El trader no dio el umbral de «casi plana».
- **F37, el calendario de cierres de mercado: BLOQUEADA.** No hay en el repositorio ninguna fuente
  de los cierres del bróker, y bajarla era descargar datos. Además, R15 frente a R6 sigue sin
  respuesta de FTMO (`docs/validation/FTMO-REGLAS.md` §4).

Agotado lo desbloqueado, queda escrito `docs/nocturno/BRECHA-EN-VIVO.md`.

## 4. Decisiones de interpretación que tomé, y dónde quedan

| # | Decisión | Dónde |
|---|---|---|
| 1 | Una vela sin cuerpo que rompe los dos extremos sigue dando `ambiguo`, y RN-033 prohíbe | ADR-0060 §2 |
| 2 | `insuficiente` se conserva: es un tope del proyecto, no del trader | ADR-0060 §3 |
| 3 | El cierre de RN-002 vale también en el propio límite de la vela H4: ninguna posición cruza de una vela a otra | ADR-0060 §5 |
| 4 | El cierre antes del fin de la H4 usa el mismo interruptor, `cierre_forzoso_fin_ventana` | ADR-0060 §4 |
| 5 | `cierre_h4_antelacion` cita el ítem de evidencia y no el registro de feedback, porque ese registro es un CORRECT sobre la regla | ADR-0060 §4 y §6 |
| 6 | Las reglas RN-002, RN-003 y RN-033 siguen citando los registros de la sesión 1: sus tres CORRECT de la sesión 3 siguen saliendo en `feedback pending` | ADR-0060 §6 |
| 7 | La memoria del productor es por sesión; lo que cruza de una sesión a otra —órdenes pendientes, posiciones— no se toca (A-39 ABIERTA) | `engine/zonas.py`, commit `bf1dc0b` |
| 8 | «Lo mínimo posible» es un punto, no un pip entero | ADR-0061 §2 |
| 9 | Qué es «la zona de control posterior» a la entrada, en M1 | ADR-0061 §4 |
| 10 | El break even se pone al cierre de la M1 que toca el punto, no en el tick | ADR-0061 §5 |
| 11 | A-43 no se activa con la toma en M1 | ADR-0062 §2 |
| 12 | El reloj de las sesiones es un selector entre los relojes que ya existen, no un huso nuevo; el kit y la ingesta siguen en `huso_operativa` | ADR-0063 §1 y §5 |
| 13 | `Last Stable Commit` nombra un commit que la rama no contiene, con nota | `PROJECT_STATE.md` |
| 14 | F34 en dos commits, con la toma en M1 aparte | commits `2cca34d` y `2763ceb` |

## 5. Preguntas para Aleks, por urgencia

1. **La CI de `main` en rojo.** ¿Me pegas el final del log del run de `67ab298`, como con
   `7ff9a9c`? Con él se confirma o se descarta la hipótesis de §0 y se arregla en una rama. Mientras
   tanto `main` tiene un tag estable sobre un commit cuya CI no pasa.
2. **F35, el punto de la orden stop.** Antes de la rama 3 hay que decidir (a) en qué precio nace
   la orden —el pivote de `referencia_del_breaker`, que la medida desmiente, o el 0 de la caja— y
   (b) con qué caja (A-48, A-49). Si te sirve, el paso siguiente sería una medición con el
   criterio escrito antes: las reglas R1 a R6 de `BLOQUE-DE-LA-CAJA.md` §1.4 sobre las 77
   operaciones de construcción, contra la entrada y el stop de los libros. No la hice: es una
   medición nueva sobre las filas de los libros, con su declaración, y no estaba en el encargo.
3. **F34 (2 de 2), la toma en M1 (`2763ceb`).** ¿Entra ya, con la cobertura en diagnóstico a 0 de
   77, o espera a la vida de la orden stop y a la caja por operación? Es lo que el trader dijo; el
   coste es que el bot queda peor hasta que lleguen esas dos ramas.
4. **Los cuatro ADR PROPUESTOS** (ADR-0060 a ADR-0063): aceptar, corregir o rechazar cada uno.
5. **A-42 y el invierno.** El cambio de hora es el 25 de octubre. El mecanismo ya está (F36); falta
   (a) cuándo pasa `reloj_sesiones` a `grafico` —el trader dijo «creo»— y (b) con qué reloj asigna
   el kit la sesión de las operaciones del trader en un mes de invierno, antes de que entre marzo.
6. **El redondeo del stop**: ¿un punto o un pip entero? (decisión 8).
7. **Las citas de RN-002, RN-003 y RN-033** (decisión 6): ¿las cambias tú a los registros de la
   sesión 3? En RN-033 no es trivial: el trader dice que siempre hay sesgo y la regla sigue
   prohibiendo en dos casos que él no describió.
8. **Para la sesión 4 con el trader**: el umbral de la vela casi plana (RN-007); qué sesgo da una
   vela sin cuerpo que rompe los dos extremos (decisión 1); y si el break even «al tocar» es en el
   tick (decisión 10).
9. **El calendario de cierres** (F37): de dónde sale —el horario de sesiones del símbolo en la
   plataforma de FTMO, en la demo— y la respuesta de FTMO a R15 frente a R6.
10. **La brecha hasta el vivo**: `docs/nocturno/BRECHA-EN-VIVO.md` deja sus decisiones punto por
    punto. La primera es si el plan de la fase 6 (reescribir el dominio en MQL5) sigue valiendo
    ahora que el motor es un intérprete de la spec. Y una corrección al encargo: el límite diario de
    FTMO se corta a medianoche CE(S)T, no en la hora del servidor (ADR-0027).
11. **`trabajo/memoria-suite`** sigue sin borrar, a la espera de la CI.

## 6. Qué revisar antes de integrar esto en `main`

1. **Primero, `main` en verde.** Esta rama no debería entrar sobre un `main` con la CI en rojo.
2. **Poner la rama al día sobre `main`.** Sale de `14e01bc` y `main` está en `67ab298`. Ensayado
   sin tocar nada (`git merge-tree`): **un solo conflicto, en `PROJECT_STATE.md`**
   (`Current Branch`, la nota de `Last Stable Commit` y la línea de tests); `src/botsito/cli.py` se
   fusiona solo. Al resolverlo, la nota de `Last Stable Commit` sobra y el recuento de tests hay
   que volver a contarlo, porque `main` trae los de `tests/unit/test_memoria.py`.
3. **Los ADR, uno a uno**, con las decisiones de §4. Los commits van separados por funcionalidad
   para revisarlos así; **no he ensayado revertir ninguno por separado**, y los posteriores tocan
   ficheros de los anteriores.
4. **`2763ceb` aparte** (pregunta 2).
5. **El diff de `knowledge/spec/`**: cinco subidas de `spec_version` (de 13.5.0 a 14.4.0), un
   predicado nuevo (`vence_vela_h4`), dos parámetros nuevos (`cierre_h4_antelacion`,
   `reloj_sesiones`), un argumento nuevo en una acción (`redondeo`) y el cambio de `huso` a `reloj`
   en dos predicados. Cada commit lleva su trailer `Fuente:`.
6. **Las líneas base.** `docs/validation/ARNES-MOTOR-LINEA-BASE.txt` y las demás no se han
   regenerado: son de ramas cerradas. Las salidas de esta noche están fuera del repositorio, en la
   carpeta de trabajo de la sesión, y se reproducen con los comandos de `docs/runbooks/ARNES-MOTOR.md`.
7. **Lo que esta rama NO tiene**: informe en `docs/validation/` (el informe es este), ni la entrada
   de Change Log en `PROJECT_STATE.md`, ni Next Action actualizado. Son del cierre, que es tuyo.

## Estado

Rama lista para revisión, **NO cerrada**. Último commit verde: el que contiene este informe.
