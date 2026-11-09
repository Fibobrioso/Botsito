# RECORRIDA-CONSTRUCCION-2 · La re-corrida que cuenta: comisión medida, sello, sesión 6, método y cuenta por mes

Rama `trabajo/recorrida-construccion-2`, abierta el 2026-11-08 desde `main` (ad225de) con el encargo
del consultor del mismo día (`docs/encargos/trabajo-recorrida-construccion-2.md`). Tramo «R3 · Una
corrida del arnés sobre toda la construcción». Rama de medida: no toca el motor.

## La base, comprobada con git (2026-11-08)

- `git rev-parse HEAD` en `main`: `ad225de3658b760dff5259acc6cf5dc8616f24e3`; `git rev-parse origin/main`: el mismo.
- `git rev-parse "stable/F38s-cuenta-por-mes^{commit}"`: `41d47b33aedd6029323b21deac69f2970ed1faa3` = `git rev-parse main^1`; el tag está en origin (`git ls-remote --tags origin`: objeto `b9bba05`, anotado).
- `gh run view 42502468946 --json headSha,status,conclusion,headBranch,workflowName`: `ci`, `main`, `ad225de3658b760dff5259acc6cf5dc8616f24e3`, `completed` / `success`.
- `git branch -a`: solo `main` y `origin/main`; `git ls-remote --heads origin`: solo `refs/heads/main`.
- `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1` puesta en la sesión; `PROJECT_STATE.md` 22.832 bytes en `main` (`wc -c`).

## 0. Las decisiones del consultor y la fase 0 (2026-11-08)

### 0.1 Las decisiones del consultor (D1 a D12), escritas antes de correr

Copiadas TAL CUAL del encargo (`docs/encargos/trabajo-recorrida-construccion-2.md`):

> D1. La corrida 1 de la fase 2 es la que cuenta por ADR-0070 §3, con la condición de ADR-0092 §8 ya en el motor (una cuenta por mes). Su línea «habilita medir el conjunto de medida (2026-05) (ADR-0070): …» se copia literal al informe. Si dice «no»: se sigue construyendo, mayo no se toca y el umbral no cambia (ADR-0070 §4). Si dice «sí»: PARADA, y nada de mayo: por ADR-0070 §6 un «sí» habilita la rama de medida con su propio ADR y no la sustituye; y la rentabilidad de ADR-0092 §5 sigue necesitando G (PREREGISTRO) y su propia rama.
>
> D2. La salida de la corrida 1 pasa a ser la línea base vigente tal como queda en anexos, sin copia; la de anexos/RESPALDO-M1/ no se toca. ADR-0070 §3 gana una NOTA fechada al final de las que ya tiene (el cuerpo no se toca, las NOTAS y el recuadro anteriores tampoco), en un commit propio después de la fase 2, con el veredicto literal, la frase «Desde esta rama la línea base vigente es anexos/RECORRIDA-CONSTRUCCION-2/cuenta-por-mes.txt», qué entró en el motor desde la línea base anterior (ADR-0090 §3, ADR-0091, F38o, ADR-0092 y su §8) y cuántas cuentas mensuales acabaron SUSPENDIDA o bloqueadas por RN-032, si alguna.
>
> D3. Dos diffs contra la línea base anterior, los dos a fichero en anexos: (a) diff anexos/RESPALDO-M1/cuenta-arrastrada.txt anexos/RECORRIDA-CONSTRUCCION-2/cuenta-por-mes.txt > diff-linea-base.txt, que mezcla el cambio del motor con el del camino de la cuenta; (b) diff "anexos/RESPALDO-M1/diaria.DIAGNOSTICO.cuenta=diaria.txt" "anexos/RECORRIDA-CONSTRUCCION-2/diaria.DIAGNOSTICO.cuenta=diaria.txt" > diff-diaria.txt, que aísla el cambio del motor, porque la diaria no la toca la cuenta por mes (ADR-0092 §8, NOTA; CUENTA-POR-MES.md y el registro de cierre de F38s: «sigue byte a byte»). Es la repetición de las dos corridas que pedían R3.6 y R3.7. El informe resume cada diff por sección y dice qué cambia por la comisión, qué por el sello, qué por la sesión 6 y qué por el camino de la cuenta, con la evidencia de cada atribución (una fila de «Ordenes», una llenada, un evento del bróker); lo que no se pueda atribuir se dice así.
>
> D4. La clasificación por patrones (T0, P1 a P7) se hace sobre las DOS corridas, y la que manda es la corrida 1: con la cuenta por mes el bot puntúa en abril, julio y agosto, que con la cuenta arrastrada quedaban congelados desde el 2026-01-20 por RN-032 (RESPALDO-M1.md §4.5), así que la razón por la que R3.1 y R4.1 clasificaban sobre la diaria ha desaparecido. La diaria se clasifica como contexto. Los guiones patrones.py y horas_perdidas.py se copian IDÉNTICOS desde anexos/RESPALDO-M1/ (diff vacío contra el origen, en el README): ni una regla se ajusta. Si la salida nueva (los bloques «### Cuenta de AAAA-MM», la tabla «### Posiciones», la sección de ADR-0092) rompe la lectura de patrones.py, PARADA con la línea que lo rompe: no se adapta por tu cuenta.
>
> D5. Lo que el informe da de la corrida 1, por mes (= por cuenta) y en total, SIN interpretar: operaciones del trader, puntuables del bot, parejas, cobertura y precisión (ADR-0043); la cascada de ADR-0092 §2 por escalón (en el (día, sesión, dirección); entrada a 3 puntos; stop a 3 puntos; llenada a 15 min; «en el nivel, no llenada») y las órdenes del bot sin operación del trader; las líneas literales de la sección «## El metodo de ADR-0092» (fidelidad por criterios, rentabilidad y material sin vídeo, con su marca DIAGNOSTICO tal cual); de cada bloque «### Cuenta de AAAA-MM»: veredicto, saldo y equity finales, equity mínima, peor pérdida diaria, racha al cerrar el mes, primero en tocar un límite, y el día y la regla si RN-032 bloquea; las peticiones (total y máximo diario frente a 2000, y si saltó algún umbral del freno de ADR-0067, PROVISIONAL bajo A-54); y que el tramo no es continuo y la curva es indicativa, como dijo R3.1. De la corrida 2, lo mismo que en RESPALDO-M1.md §4.5.
>
> D6. Lo que el arnés hace ahora y antes no, para medirlo en el informe: ADR-0089 (el tope del trader se reinicia al abrir la primera sesión del día siguiente: cuántas sesiones detiene RN-020 y con qué regla, frente a las de RESPALDO-M1), ADR-0085 §2 en M15 (recuadro de la sesión 6: la vela sin cuerpo no corta la racha; y si `solo_la_contraria` cambió operaciones del bot, que ACTIVAR-SESION-06.md deja a la re-corrida), ADR-0085 §4 (S-10, la orden que nace en el primer punto tras la toma: «la re-corrida lo mira»; cuántas llenadas), ADR-0086, RN-036 y RN-037, el sello de ADR-0091 (cuántos eventos del bróker salen del respaldo M1 y cuántos del tick, y cuántas cancelaciones del tipo que SELLO-RESPALDO-M1.md dejó a la re-corrida aparecen fuera de los once días), si RN-032 bloquea alguna cuenta mensual y en qué día (con la arrastrada bloqueaba desde el 2026-01-20; ahora enero es la cuarta cuenta y propia), y la lista, del registro, de los parámetros DEFAULT_AMBIGUOUS con los que corrió la corrida que cuenta, con su ambigüedad. La fase 3 de S-22 no se hace aquí (decisión del consultor en ACTIVAR-SESION-06-MOTOR.md: después de la re-corrida, en la rama de S-22).
>
> D7. El visor NO se abre en esta rama. ACTIVAR-A35-A44.md §5 manda un motor visor --caso y nombra la línea base: gana una NOTA de una línea al principio de §5 (commit propio, con el de D2 si quieres) que diga cuál es la línea base vigente desde esta rama y declare la desviación del visor, como hizo la NOTA de F38g (la de F38j no la declaró: no la repitas, dilo). El cuerpo de §5 sigue haciendo diff contra CABLEADO-SIMULADOR-LINEA-BASE.txt: no se reescribe, la NOTA basta. Los días que haga falta mirar en el visor los pido yo en la respuesta a la PARADA 2.
>
> D8. La lista «Para clasificar», en anexos y resumida en el informe: cada operación del trader de construcción con el escalón de la cascada en que se queda en la corrida 1 (y en la 2), su patrón, el primer hecho del camino del bot que falta en esa sesión (el embudo), si el día viene de vídeo (material_sin_video: abril solo el 29; julio provisional; enero y agosto no) y si toca una hora perdida (posible M). Y aparte, cada orden del bot sin operación del trader en su (día, sesión, dirección), con su resultado en R, su patrón y si pasó por break even. Es la materia de la PARADA 2: sin conclusiones.
>
> D9. Esperado para no esperar de más (no es un criterio): RESPALDO-M1 dio 351 s y 630 MiB por corrida con la cuenta arrastrada congelada; la diaria de ACTIVAR-SESION-06-MOTOR, 452 s y 640 MiB. Con la cuenta por mes la corrida 1 operará en los cuatro meses: espera tiempos del orden de la diaria. Si una corrida pasa de 20 minutos o de 1,5 GiB de pico, dilo en el informe; si muere, PARADA con el error literal y sin relanzar.
>
> D10. Si la corrida 1 repetida (fase 2, punto 3) no es idéntica byte a byte a la commiteada, PARADA: el determinismo es condición de la línea base.
>
> D11. Si cualquier cosa de esta rama pidiera tocar src/, tests/ o knowledge/, PARADA con la alternativa; no se hace.
>
> D12. Nada de esta rama entra en la hoja de la sesión 7 por su cuenta: qué pregunta nace de la clasificación lo decido yo en la PARADA 2 y va al encargo de la preparación de la sesión 7.

**La PARADA condicional: lo medido cuadra con D1 a D12 en lo que decide, y sigo a la fase 1 sin
esperar**, como dice el encargo. Lo que no cuadra son cuatro afirmaciones de hecho, que no cambian
ninguna decisión y donde gana la medida (CLAUDE.md, «Como se trabaja»); van en «El encargo frente al
repo» (0.k), cada una con lo que hago: (1) enero es la PRIMERA cuenta, no la cuarta (D6); (2) la lista
de lo que entró en el motor de D2 y D6 sobra por un lado y falta por otro; (3) `test_humo.py` no se
puede copiar tal cual; (4) dos datos de D5 que la salida no imprime y se derivan, y uno de D8 que no
está en la salida.

### 0.a La corrida 1 y la lista cerrada; la corrida 2; el motivo f)

- **Las opciones.** `OPCIONES_QUE_NO_CAMBIAN_LA_CORRIDA = {"--salida", "--tracemalloc", "--meses",
  "--simular", "--perfil", "--fase"}` (`src/botsito/engine/arnes.py:80-82`). La corrida 1 lleva
  `--simular` y `--salida`: las dos dentro. El veredicto mira las opciones que salen de los parsers
  (`cli.py:2450`, `opciones_de_la_corrida`) y da «opción fuera de la lista» por cualquier otra
  (`arnes.py:286-289`; `criterio_fidelidad.py:208`).
- **Perfil y fase efectivos.** Sin `--perfil`, `perfil_del_repo` toma el único de
  `knowledge/cuentas/` (`cableado.py:649-663`; la carpeta solo tiene
  `ftmo-2step-swing-100k.yaml`, `cierres/` y `README.md`); sin `--fase`, `fase_real =
  perfil.fases()[0]` (`cableado.py:698`), y `Simulacion(motor.perfil, motor.fase,
  perfil_cuenta.fases()[0])` (`cli.py:2441`). `perfil_para_medir: ftmo-2step-swing-100k`
  (`knowledge/cases/criterio_fidelidad.yaml:37`) y `firma_fases: "reto verificacion fondeada"`
  (`ftmo-2step-swing-100k.yaml:86`): perfil y primera fase, `reto`, son los que cuentan
  (`criterio_fidelidad.py:212-218`).
- **Ningún `--diagnostico-*`.** A-35 tiene valor y `--diagnostico-a35`/`-a44` se rechazan desde la
  sesión 5 (ADR-0070 §3, NOTA del 2026-10-26); el motor lee la lectura del registro sin diagnóstico
  (`cli.py:2396-2403`). Lo comprueba la propia corrida: sin la lectura fijada se negaría.
- **La cuenta por mes sin opción.** `MotorCableado.correr_dia`: si `mes != self.mes_en_curso`, cierra
  la cuenta del mes y pone a cero cuenta, seguidor, racha y primer toque (`cableado.py:306-316`);
  `cuenta_diaria` solo la pone `--diagnostico-cuenta-diaria` (`cli.py:2438`, `:2261`). La cabecera
  con varias cuentas: `CUENTA: UNA POR MES (ADR-0092 §8): {n} cuentas` (`cableado.py:879-880`), y cada
  mes su bloque `### Cuenta de AAAA-MM` (`cableado.py:829-847`, `:890-892`).
- **El nombre de la corrida 2.** `nombre_etiquetado` (`engine/diagnostico.py:169-185`) convierte la
  etiqueta `DIAGNOSTICO-CUENTA-diaria` en `cuenta=diaria`: `--salida
  docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/diaria.txt` escribe
  **`diaria.DIAGNOSTICO.cuenta=diaria.txt`**, el nombre que D3 (b) usa.
- **El motivo f) con varias cuentas** (`criterio_fidelidad.py:805-810`): con una cuenta, «f) la
  cuenta entro en SUSPENDIDA»; con varias, «f) alguna cuenta entro en SUSPENDIDA (<meses>)». La
  línea de la salida (`cableado.py:1531-1533`): «f) alguna cuenta entro en SUSPENDIDA: si (<meses>)»
  o «: no». `medir_por_cuentas` (`criterio_fidelidad.py:696-711`) da d) y e) de la peor cuenta con
  su mes y los meses suspendidos.

### 0.b Ticks y horas perdidas

Guion `recuentos_fase0.py` de la carpeta de trabajo (raíz por argumento; los cuatro manifiestos por
ruta literal, `data/manifests/ticks/eurusd-ticks-2026-{01-1ce59681,04-1d189bdd,07-6e7dc7cd,08-75bd3a08}.yaml`,
los únicos de `ls data/manifests/ticks/`), frente a los días dev de `arnes.dias_de_construccion`:

| Mes | ficheros del manifiesto | días dev | coinciden | horas UTC | perdidas | días dev sin ticks |
|---|---|---|---|---|---|---|
| 2026-01 | 21 | 21 | sí | 06-14 | 5 | 0 |
| 2026-04 | 21 | 21 | sí | 05-13 | 7 | 0 |
| 2026-07 | 13 | 13 | sí | 05-13 | 3 | 0 |
| 2026-08 | 21 | 21 | sí | 05-13 | 3 | 0 |

**Ningún día dev sin ticks: ni PARADA ni `--depuracion`.** 18 horas perdidas, iguales una a una a las
de `anexos/RESPALDO-M1/horas_perdidas.py:18-24`; 17 dentro de las sesiones y `2026-04-22T13Z` fuera
(`FUERA_DE_SESION`, `:25`), como contó RECORRIDA-CONSTRUCCION.md §0.b. El respaldo M1 las cubre:
`_ticks_del_dia` suma los ticks de los manifiestos y sus `horas_perdidas`
(`engine/simulacion.py:166-180`), y el bróker llena por M1 en el minuto sin ticks (ADR-0051 §5 y
ADR-0091).

### 0.c El perfil

`knowledge/cuentas/ftmo-2step-swing-100k.yaml`: `firma_comision_usd_por_lote` con `valor: "2.50"`
(líneas 382-400) y `firma_comision_por_lado` con `valor: true`, CONFIRMED (líneas 401-414); el broker
los lee por su nombre (`engine/simulacion.py:140-141`) y la tabla de posiciones cobra
`comision_por_lote * lotes * (2 si por lado)` (`cableado.py:1290`). Es el perfil que la corrida usa
(0.a).

### 0.d Recuentos de partida

Por la compuerta del arnés (`arnes.dias_de_construccion`, `recuentos_fase0.py`):

| Mes | días dev | operaciones del trader | vídeo (`material_sin_video`) |
|---|---|---|---|
| 2026-01 | 21 | 54 | sin vídeo |
| 2026-04 | 21 | 35 | sin vídeo salvo 2026-04-29 |
| 2026-07 | 13 | 67 | con vídeo, provisional |
| 2026-08 | 21 | 42 | sin vídeo |
| total | **76** | **198** | |

Las cifras de la línea base anterior (76 y 198) se confirman. `material_sin_video`
(`knowledge/cases/criterio_fidelidad.yaml:61-65`): `meses: ["2026-01", "2026-04", "2026-08"]`,
`dias_con_video: ["2026-04-29"]`, `provisionales_con_video: ["2026-07"]`, fuente
ACTIVAR-SESION-05.md §0.b.7. `construccion: ["2026-04", "2026-07", "2026-08", "2026-01"]`,
`medida: ["2026-05"]` (`:47-48`).

**Antes de leer casos dev** (CLAUDE.md, «Material de DESARROLLO»): `casos_reservados(repo)` da 34 en
total y **0 en cada uno de los cuatro meses de construcción**; `casos_ocultos(repo)`, 34 y 0 en cada
uno. Sin imprimir ninguna clave (fila del 2026-11-08 de HOLDOUT-EXPOSICIONES).

### 0.e Los guiones de anexos/RESPALDO-M1/ y la salida nueva

- **`patrones.py`** lee solo dos clases de línea (`:75-85`): las filas de «## Diferencias por
  operacion» que empiezan por `trader | ` o `bot | `, y las de «## Por sesion» que casan
  `^AAAA-MM-DD <sesion> \| trader N \| bot N \| rn003 <sesgo> \|` (`POR_SESION`, `:60-62`).
- **`horas_perdidas.py`** lee solo las filas `trader | ` y `bot | ` (`:37-41`).
- **`censo_respaldo.py`** y **`sesiones_s14.py`**: no se copian ni se corren (D4; encargo, e).
- **La salida nueva.** Ninguna línea de lo que añade la cuenta por mes (`### Cuenta de AAAA-MM`, sus
  curvas `AAAA-MM-DD | saldo | …`), de «### Posiciones» (`AAAA-MM-DD | sesion | id | …`), de la
  cascada (`AAAA-MM | …`) ni de la rentabilidad empieza por `trader | `/`bot | ` ni casa
  `POR_SESION` (`cableado.py:829-847`, `:1231-1235`, `:1351-1374`, `:1454-1463`).
- **Medido sobre la salida sintética de dos meses** (la de
  `test_con_varios_meses_la_salida_lleva_un_bloque_por_cuenta`, más la sección de ADR-0092 con el
  criterio real: `escenarios_cuenta_por_mes.informe_dos_meses_con_criterio`, volcada por
  `volcar_dos_meses.py` a la carpeta de trabajo, 104 líneas, sin tocar el test). Como esa salida es
  solo la cola de la simulación (no lleva «Diferencias por operacion» ni «Por sesion»), la monté con
  `combinar.py` detrás de la parte del arnés de `anexos/RESPALDO-M1/cuenta-arrastrada.txt` (683
  líneas, hasta «## Simulacion (ADR-0053)»), en lugar de su cola, y corrí los dos guiones sobre las
  dos: `patrones.py --filas` da **la misma salida salvo el nombre del fichero** de la primera línea
  (`diff`: solo `1c1`), y `horas_perdidas.py` lo mismo, «12 de 244» en las dos. **La salida nueva no
  rompe la lectura de `patrones.py`: no hay PARADA por D4.**
- **Las cifras de contexto de §4**, leídas en `anexos/RESPALDO-M1/patrones-arrastrada.txt` y
  `patrones-diaria.txt`: arrastrada T0 7, P1 44, P2 11, P3 11, P4 124, P5 37, P6 9, P7 1 (244
  filas); diaria T0 40, P1 44, P2 40, P3 62, P4 8, P5 171, P6 75, P7 4 (444 filas). Las del encargo.

### 0.f Herencias

Buscadas por el subagente `auditor-encargo` sobre las rutas literales del punto f) («re-corrida»,
«recorrida», «corrida que cuenta», «línea base»). Las que el encargo ya nombra, confirmadas:

| Herencia | Dónde | Entra |
|---|---|---|
| R3.6 «Hecho cuando» pasa las dos corridas a R3.7 y a la re-corrida | `docs/plan/HOJA-DE-RUTA.md:222-224` | las corridas 1 y 2 (fase 2) |
| R3.7: «la re-corrida que cuenta repite las dos corridas que pedía R3.6, ya con el sello de ADR-0091» | `HOJA-DE-RUTA.md:246-247` | las mismas |
| R5.2 «Depende de» cita la corrida que cuenta como R4.1 | `HOJA-DE-RUTA.md:376-378` | la línea del cierre (§6) |
| R5.6 pide la re-corrida con «habilita medir: sí» | `HOJA-DE-RUTA.md:419` | §6, sin cambio salvo «sí» |
| ADR-0090 §3: la re-corrida que cuenta es la primera con la tarifa medida | `docs/adr/0090-*.md:107-110` | §1 y §3 (la comisión) |
| ADR-0091: «lo demás lo ve la re-corrida» | `docs/adr/0091-*.md:143-148`; `SELLO-RESPALDO-M1.md:341-344` | D6: las cancelaciones fuera de los once días |
| ADR-0085 §4 (S-10): «la re-corrida lo mira» | `docs/adr/0085-*.md:125-131` | D6 |
| ADR-0085 §2 en M15, recuadro de la sesión 6 | `docs/adr/0085-*.md:70-83` | D6 |
| `solo_la_contraria`: si cambia operaciones del bot lo mide la re-corrida | `ACTIVAR-SESION-06.md:286-287` | D6 |
| La fase 3 de S-22, después de la re-corrida | `ACTIVAR-SESION-06-MOTOR.md:791` | no se hace aquí (D6) |

Las que el encargo no recogía, y qué hago con cada una:

| Herencia | Dónde | Qué hago |
|---|---|---|
| H1. Tres cosas que la rama del método dejó a la primera corrida real: cuánto tarda el remuestreo de 10.000 réplicas sobre 76 días (nunca medido), si RN-032 sigue congelando con el motor de hoy, y la primera salida real de la cascada, la rentabilidad y «Posiciones» | `METODO-FIDELIDAD-RENTABILIDAD.md:1048-1053` | Entra: la segunda y la tercera ya están en D5 y D6; el tiempo, en 0.h y en §1 (las líneas TIEMPO). |
| H2. §5.1 de `ACTIVAR-A35-A44.md` dice que la re-corrida con su `diff` contra la línea base es «lo que queda de R4.1», y su cuerpo sigue llamando «línea base vigente» a `CABLEADO-SIMULADOR-LINEA-BASE.txt` | `docs/runbooks/ACTIVAR-A35-A44.md:261-266`, `:281`, `:292` | No entra: D7 pide la NOTA solo en §5 y el cuerpo no se reescribe. La NOTA de §5 nombra la línea base vigente para todo el runbook; lo dejo dicho al consultor en la PARADA 2 por si quiere una NOTA también en §5.1. |
| H3. La equity, los topes y el margen libre con el sello de ADR-0091 no se midieron («no que la peor equity sea la misma») | `SELLO-RESPALDO-M1.md:345-347` | Entra: la corrida 1 los da (bloques por cuenta, «Ordenes», rechazos por margen); §3 los compara. |

### 0.k El encargo frente al repo (informe del auditor, 52 afirmaciones: 38 correctas, 3 incorrectas, 11 con matiz)

Lo que no cuadra, con lo que hago (gana la medida):

1. **D6, «ahora enero es la cuarta cuenta y propia»: INCORRECTA.** `validar_meses` devuelve los
   meses ORDENADOS (`arnes.py:121`) y `dias_de_construccion` los recorre en ese orden
   (`arnes.py:148-151`): la corrida va enero, abril, julio, agosto. **Enero es la PRIMERA cuenta**, y
   ya lo era con la arrastrada, que empezaba en el capital el primer día de enero. Solo el yaml pone
   enero cuarto (`criterio_fidelidad.yaml:47`). Consecuencia para D3: en enero el camino de la cuenta
   no cambia, así que **todo lo que cambie en enero en `diff-linea-base.txt` es del motor**; el camino
   de la cuenta solo puede explicar abril, julio y agosto. Así lo atribuyo en §3.
2. **Lo que entró en el motor desde la línea base anterior (D2 y D6).** Desde `stable/F38j-respaldo-m1`
   (la de RESPALDO-M1), medido con `git diff --stat` tag a tag sobre `src/botsito/engine`,
   `src/botsito/domain`, `src/botsito/cases`, `knowledge/spec/parametros.yaml`,
   `knowledge/spec/strategy_spec.yaml` y `knowledge/cuentas`: F38k, F38l y F38m, **nada**; **F38n**,
   `parametros.yaml` y `strategy_spec.yaml` (la spec de la sesión 6: entre otros,
   `liquidez_m15_mecha_que_vuelve` pasa a `solo_la_contraria`, que el motor lee en `arnes.py:219`);
   **F38o**, `pivotes_m15.py`, `tope_trader.py`, `motor.py`, `cableado.py` y la spec (ADR-0089 y
   ADR-0085 §2); **F38p**, el perfil (la comisión medida, ADR-0090), el calendario de cierres
   (`knowledge/cuentas/cierres/ftmo-2step-swing-100k.yaml`, 7 líneas) y `parametros.yaml`;
   **F38q**, `broker.py`, `llenado.py`, `primitivas_broker.py` y `cableado.py` (el sello, ADR-0091);
   **F38r**, `criterio_fidelidad.py`, `cableado.py` y `arnes.py` (ADR-0092: SOLO SALIDA,
   `cableado.py:1221-1229`); **F38s**, `cableado.py`, `racha.py`, `criterio_fidelidad.py`,
   `diagnostico.py` y la spec (la cuenta por mes). La lista de D2 («ADR-0090 §3, ADR-0091, F38o,
   ADR-0092 y su §8») se queda sin la spec de F38n y el calendario de F38p; los nombro en la NOTA de
   D2 y en §3. Y **ADR-0086, RN-036 y RN-037 no son
   nuevos**: ADR-0086 es de F38f, anterior a RECORRIDA (F38g); la línea base anterior ya lleva RN-037
   en 110 líneas y RN-036 en 20 (`grep -c` del auditor sobre `anexos/RESPALDO-M1/cuenta-arrastrada.txt`).
   Lo que puede cambiar es su EFECTO (RN-020 por ADR-0089; la racha de RN-036, que desde F38s se
   reinicia con cada cuenta): eso mide D6.
3. **D3 (b), «aísla el cambio del motor»: MATIZ.** Contra RESPALDO-M1 el `diff-diaria.txt` recoge
   también la salida nueva de F38r («### Posiciones», «## El metodo de ADR-0092»), que no decide
   nada. En §3 hay una categoría más: «salida nueva, sin decisión».
4. **`test_humo.py` copiado tal cual falla: INCORRECTA** (`anexos/RECORRIDA-CONSTRUCCION/test_humo.py:15-18`
   importa `entradas_antes_alternancia`, que no se copia; y su `test_la_lectura_vieja_rompe_sin_rotulo`
   carga el guion de R3.1 por una ruta calculada, que la guardia niega fuera de `main`: medido, la
   negativa a `importlib.util.spec_from_file_location`). Hago: el `test_humo.py` de la carpeta nueva
   lleva copiados tal cual sus constantes, `_clasifica` y los dos tests de `patrones.py` que no
   dependen de nada más, más uno de `horas_perdidas.py` (el original no lo probaba) y los de
   `para_clasificar.py`; y el original se corre en su sitio, idéntico al de `main`. Desviación
   declarada.
5. **D5: la peor pérdida diaria por cuenta y el bloqueo de RN-032 no están en el bloque «### Cuenta de
   AAAA-MM»: MATIZ** (`cableado.py:829-847`). La salida da d) solo para la peor cuenta, con su mes
   (`:1522-1526`); la de cada cuenta la derivo de su curva con la misma función
   (`criterio_fidelidad.perdida_diaria_maxima`), y RN-032 sale de «Por sesion», columna
   `disparadas`. *Corregido tras el revisor (a1): la primera redacción decía «columna
   `bloqueadas`»; esa columna nunca nombra RN-032 (lleva `RN-015:accion:colocar_orden_limite:prohibida:abrir_operacion`
   en 96 de las 104 sesiones, dispare RN-032 o no; `arnes.py:260-265`).* Se dice en §1 qué es leído
   y qué derivado.
6. **D8, el escalón de la cascada por operación: la salida no trae el stop del trader** (la fila de
   «Por operacion» lleva lado, instante y entrada, `arnes.py:619-649`) **ni la dirección de una orden
   no llenada** («### Ordenes», `cableado.py:949-953`). Por D8 («dilo y deja la columna vacía»):
   `para_clasificar.py` calcula la cascada hasta la entrada y agrupa los cinco escalones de detrás en
   «entrada dentro»; la dirección de una no llenada la lee de su caja (el 1 de la caja, por encima
   del precio, venta), y comprueba lo contado contra la cascada por mes que imprime la propia salida.
   Si el consultor quiere el escalón entero, el stop del trader está en los casos dev
   (`knowledge/cases/dev/`), que se pueden leer; no lo hago sin su orden porque D8 dice «SOLO las
   salidas commiteadas».
7. **Los `diff` de D3 escritos con rutas relativas a `docs/validation/`**: desde la raíz no se
   ejecutan así; los escribo con la ruta entera (README de anexos).
8. **D7 «al principio de §5»** y **D2 «al final de las que ya tiene»: MATIZ.** En §5 ya hay dos NOTAS
   al principio, en orden de fecha (`ACTIVAR-A35-A44.md:222`, `:238`): la nueva va detrás de ellas,
   antes del bloque de comandos. En ADR-0070 §3 lo último es el recuadro «ENMENDADO POR ADR-0092»
   (`:115-122`): la NOTA va detrás del recuadro.
9. **D9, 452 s y 640 MiB de la diaria de ACTIVAR-SESION-06-MOTOR: MATIZ** (0.h).
10. **«enero no tiene mes anterior»: MATIZ.** `_mes_anterior("2026-01")` da `2025-12`
    (`arnes.py:181`); no se lee porque no hay manifiesto M1 de ese mes y el código sigue con
    `continue` (`arnes.py:209-210`). El efecto es el del encargo.
11. **PROJECT_STATE, 22.832 bytes**: en `main`, sí; en la rama, tras abrir-rama, 22.849.

El informe entero del auditor, en el apéndice A (al final).

### 0.g La fila de exposiciones antes del primer make check

La fila del 2026-11-08 de `trabajo/recorrida-construccion-2` se escribió y se estadió
(`git add docs/validation/HOLDOUT-EXPOSICIONES.md`) a las **14:07:29** (hora local, `date` justo
después del `git add`), antes de cualquier lectura del día, de cualquier clon (no hay ninguno) y del
primer `make check`, que se lanzó a las **14:10:25** y escribió su `SELLO` sobre el árbol
`17f4413c6d530e8ea0f823853c870869c4120ecb` (log de las 14:35:38). Va en el commit de apertura,
`5eca8e3` (`2026-11-08 14:35:57 -0500`). La única lectura anterior a la fila fue la de la base con
git (`rev-parse`, `ls-remote`, `gh run view`), que no lee material.

### 0.h Tiempo y memoria esperados

RESPALDO-M1 dio, con la cuenta arrastrada, `TIEMPO: 351.0 s; MEMORIA: pico del proceso de 630.3 MiB`
(corrida 1), `315.8 s; 638.4 MiB` (la diaria) y `347.7 s; 630.1 MiB` (la repetición)
(RESPALDO-M1.md:694-696). Las de ACTIVAR-SESION-06-MOTOR.md:128-130 (`452.1 s; 640.2 MiB` y
`428.5 s; 640.3 MiB`) son corridas diarias **en proceso, con dos funciones observadas por un guion**
(`medir_f2_f3.py`, :118-123), no la corrida del comando: sirven de orden de magnitud, no de
comparación. Esperado: unos 6-8 min y unos 650 MiB por corrida, tres corridas (unos 25 min) y los
`make check` de 20-25 min cada uno (el de la apertura: 1510 s, pico 309 MiB). Cabe en una sesión.
Lo que nunca se ha medido (herencia H1): el remuestreo de 10.000 réplicas de la rentabilidad sobre
los 76 días, que esta corrida es la primera en hacer con datos reales; si la corrida pasa de 20 min,
se dice (D9).

### 0.i Lo que no pude medir

- Nada de lo que la fase 0 pedía queda sin medir. Lo que solo dan las corridas (D5, D6) va a §1-§3.
- Si el cambio del calendario de cierres de F38p toca algún día dev (el auditor no lo pudo ver): lo
  dirá la sección «### Los cierres de mercado (ADR-0068)» de la corrida 1, y §3.

### 0.j Los parámetros DEFAULT_AMBIGUOUS con los que corre la corrida que cuenta (D6)

Del registro (`knowledge/spec/parametros.yaml`, `estado: DEFAULT_AMBIGUOUS` y su `ambiguedad_id`; guion
`default_ambiguous.py` de la carpeta de trabajo):

| Parámetro | Valor | Ambigüedad | Fuente |
|---|---|---|---|
| `liquidez_m15_mecha_que_vuelve` | `solo_la_contraria` | A-35 | ev-v17-001319-419307f6 |
| `orden_stop_punto` | `ultimo_pivote_m1` | A-48 | ev-v7-002201-2b2f20aa |
| `orden_pendiente_al_abrir_escenario` | `se_mueve` | A-53 | un `fb-` de la sesión 3 con el trader (su `fuente` en `parametros.yaml`; el id lleva la fecha de la sesión, de un mes con días reservados, y aquí no se escribe) |
| `freno_peticiones_aviso` | 1000 | A-54 | ADR-0067 |
| `freno_peticiones_corte` | 1500 | A-54 | ADR-0067 |
| `freno_bucle_repeticiones` | 5 | A-54 | ADR-0067 |
| `freno_bucle_minutos` | 1 | A-54 | ADR-0067 |
| `cierre_pendientes` | `cancelar` | A-55 | ADR-0068 |

Ocho en total. Ninguno se toca (encargo, «Qué no cambia»).

### 0.l Exposiciones del día

La fila del 2026-11-08 de esta rama en `HOLDOUT-EXPOSICIONES.md` (0.g): los `make check` (M1 de marzo),
las tres corridas (calentamiento con el M1 entero de marzo, de junio y de julio), los guiones de
anexos y los subagentes. En la fase 0, además: `casos_reservados` y `casos_ocultos` por recuento
(0.d), los cuatro manifiestos de ticks (0.b), la salida sintética de dos meses y la parte del arnés
de `anexos/RESPALDO-M1/cuenta-arrastrada.txt` (días dev), y el auditor, que leyó solo el repo.
Nada más.

## Lo que necesitaba decidir en la fase 0 (sin parar)

Nada para seguir: la PARADA de la fase 0 es condicional y lo medido cuadra con D1 a D12 en lo que
decide (0.1). Dos cosas para la PARADA 2, que no detienen nada:

0. **El escalón entero de la cascada en la lista de D8.** Opciones: (a) dejarlo hasta la entrada,
   como sale de la salida sola (0.k, punto 6); (b) leer el stop del trader de los casos dev para
   cerrar los cinco escalones de detrás. Recomiendo (a) en esta rama, porque D8 dice «SOLO las
   salidas commiteadas»; si en la PARADA 2 hace falta, (b) es un guion más sobre material de
   desarrollo. Coste de (b): leer `knowledge/cases/dev/` (sin puerta, declarado) y otro guion.
1. **Una NOTA también en §5.1 de `ACTIVAR-A35-A44.md`** (herencia H2). Opciones: (a) no, la de §5
   basta (D7); (b) una línea igual en §5.1. Recomiendo (a): D7 lo fija. Coste de (b): un commit.

## Fase 1 · el README y los guiones (2026-11-08, commit `686a8b3`)

- `anexos/RECORRIDA-CONSTRUCCION-2/README.md`, con la forma del de `anexos/RESPALDO-M1/`, en su
  propio commit ANTES de correr, con las copias y los guiones.
- `patrones.py` y `horas_perdidas.py`, copias idénticas de `anexos/RESPALDO-M1/`: `diff` vacío y los
  mismos `sha256` (`330b7d62…` y `dfa782a3…`), pegados en el README.
- `para_clasificar.py` (D8), que lee solo las dos salidas, y su test de humo.
- `test_humo.py`: **desviación declarada** (0.k, punto 4): no es la copia tal cual del de
  `anexos/RECORRIDA-CONSTRUCCION/`, que importa `entradas_antes_alternancia.py` (no se copia) y
  carga el guion de R3.1 por una ruta calculada (la guardia lo niega fuera de `main`: medido). Lleva
  copiados tal cual sus constantes, `_clasifica` y los dos tests de `patrones.py` que no dependen de
  nada más; el original se corrió en su sitio. Cómo y salida (README):
  `uv run pytest docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/test_humo.py -v -p no:cacheprovider`
  → `11 passed`; `uv run pytest docs/validation/anexos/RECORRIDA-CONSTRUCCION/test_humo.py -v -p no:cacheprovider`
  → `10 passed`. En la fase 2, con los tests añadidos (abajo), `13 passed`.
- ruff format, ruff check y mypy sobre los ficheros tocados: limpios, salvo dos avisos de mypy
  (`sys.stdout.reconfigure` en `patrones.py:180` y `horas_perdidas.py:34`) que son de las copias
  idénticas y no se tocan (D4).

## Fase 2 · las corridas (2026-11-08)

Desde la raíz, sin `--meses`, sobre el código commiteado (`686a8b3`), una a la vez, en segundo
plano (`CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1`) y nunca a la par de un `make check`:

| # | Comando (literal) | exit | TIEMPO y MEMORIA (literal) | Fichero escrito (tal cual) |
|---|---|---|---|---|
| 1 | `uv run botsito motor arnes --simular --salida docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/cuenta-por-mes.txt` | 0 | `TIEMPO: 339.5 s; MEMORIA: pico del proceso de 635.6 MiB` | `docs\validation\anexos\RECORRIDA-CONSTRUCCION-2\cuenta-por-mes.txt` |
| 2 | `uv run botsito motor arnes --simular --diagnostico-cuenta-diaria --salida docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/diaria.txt` | 0 | `TIEMPO: 331.5 s; MEMORIA: pico del proceso de 641.6 MiB` | `docs\validation\anexos\RECORRIDA-CONSTRUCCION-2\diaria.DIAGNOSTICO.cuenta=diaria.txt` |
| 3 | `uv run botsito motor arnes --simular --salida "<carpeta de trabajo>/cuenta-por-mes.repetida.txt"` | 0 | `TIEMPO: 353.9 s; MEMORIA: pico del proceso de 635.2 MiB` | la carpeta de trabajo, fuera del repo; borrada tras el `diff` |

Ninguna pasa de 20 minutos ni de 1,5 GiB (D9); son del orden de RESPALDO-M1 (351 s, 630 MiB), no
de la diaria instrumentada de ACTIVAR-SESION-06-MOTOR. El remuestreo de 10.000 réplicas sobre 76
días (herencia H1) cabe en esos tiempos. **D10, determinismo:** `diff` de la commiteada contra la
repetida, `diff=0`, y el mismo `sha256` las dos
(`e6ca305ba31c6307f405d963a8eb043a66d85fafd8262a1806abd53075798054`); la copia se borró. Ninguna
pidió días fuera de la construcción ni `--depuracion`.

Después, desde la raíz. Cada comando TAL CUAL se ejecutó (revisor, b3), con su resultado; `A2` abrevia
aquí, y solo aquí, `docs/validation/anexos/RECORRIDA-CONSTRUCCION-2` y `R1` abrevia
`docs/validation/anexos/RESPALDO-M1` (en el comando ejecutado iba la ruta entera):

```
# 4 (diff=1; 3.840 lineas)
diff R1/cuenta-arrastrada.txt A2/cuenta-por-mes.txt > A2/diff-linea-base.txt
# 5 (diff=1; 3.801 lineas)
diff "R1/diaria.DIAGNOSTICO.cuenta=diaria.txt" "A2/diaria.DIAGNOSTICO.cuenta=diaria.txt" > A2/diff-diaria.txt
# 6 (exit=0 las dos)
uv run python A2/patrones.py A2/cuenta-por-mes.txt --filas > A2/patrones-cuenta-por-mes.txt
sed -i 's/\r$//' A2/patrones-cuenta-por-mes.txt
uv run python A2/patrones.py "A2/diaria.DIAGNOSTICO.cuenta=diaria.txt" --filas > A2/patrones-diaria.txt
sed -i 's/\r$//' A2/patrones-diaria.txt
# 7 (exit=0; «coincide»)
uv run python A2/para_clasificar.py A2/cuenta-por-mes.txt "A2/diaria.DIAGNOSTICO.cuenta=diaria.txt" > A2/para-clasificar.txt
# 8 (exit=0 las cuatro)
uv run python A2/resumen_corrida.py A2/cuenta-por-mes.txt > A2/resumen-cuenta-por-mes.txt
uv run python A2/resumen_corrida.py "A2/diaria.DIAGNOSTICO.cuenta=diaria.txt" > A2/resumen-diaria.txt
uv run python A2/resumen_corrida.py R1/cuenta-arrastrada.txt > A2/resumen-respaldo-m1-arrastrada.txt
uv run python A2/resumen_corrida.py "R1/diaria.DIAGNOSTICO.cuenta=diaria.txt" > A2/resumen-respaldo-m1-diaria.txt
# 9 (exit=0 las dos)
uv run python -B docs/validation/anexos/SELLO-RESPALDO-M1/censo_cierre.py A2/cuenta-por-mes.txt > A2/censo-cierre-cuenta-por-mes.txt
uv run python -B docs/validation/anexos/SELLO-RESPALDO-M1/censo_cierre.py "A2/diaria.DIAGNOSTICO.cuenta=diaria.txt" > A2/censo-cierre-diaria.txt
# 10 (exit=0 las dos)
uv run python A2/diff_por_seccion.py R1/cuenta-arrastrada.txt A2/cuenta-por-mes.txt A2/diff-linea-base.txt > A2/diff-linea-base-por-seccion.txt
uv run python A2/diff_por_seccion.py "R1/diaria.DIAGNOSTICO.cuenta=diaria.txt" "A2/diaria.DIAGNOSTICO.cuenta=diaria.txt" A2/diff-diaria.txt > A2/diff-diaria-por-seccion.txt
# 11 (exit=0: 0 lineas con algo antes del dia o fuera de la construccion en los 16)
uv run python A2/antes_del_dia.py A2/cuenta-por-mes.txt "A2/diaria.DIAGNOSTICO.cuenta=diaria.txt" A2/diff-linea-base.txt A2/diff-diaria.txt A2/patrones-cuenta-por-mes.txt A2/patrones-diaria.txt A2/para-clasificar.txt A2/resumen-cuenta-por-mes.txt A2/resumen-diaria.txt A2/resumen-respaldo-m1-arrastrada.txt A2/resumen-respaldo-m1-diaria.txt A2/censo-cierre-cuenta-por-mes.txt A2/censo-cierre-diaria.txt A2/diff-linea-base-por-seccion.txt A2/diff-diaria-por-seccion.txt A2/README.md > A2/antes-del-dia.txt
# 12 (exit=0; a: [] b: [] c: []; 22837 y 22761 bytes)
uv run python -B A2/simular_cierre.py > A2/simular-cierre.txt
```

La pasada 11 ampliada en la entrega (revisor, b1) a los `.py`, a `simular-cierre.txt` y al informe:
marca solo la fecha sintética de 2030 de `test_humo.py:280` (a propósito: es el caso «fuera de la
construcción» de su test) y, en el informe, fechas de DOCUMENTOS de octubre de 2026 (NOTAS de ADR-0070
y el apéndice del auditor), que no es un mes con días reservados.

**Los guiones de la fase 0 no se commitearon** (revisor, b3): `recuentos_fase0.py` (leyó
`casos_reservados`, `casos_ocultos`, `arnes.dias_de_construccion` y los cuatro manifiestos de ticks;
imprimió solo recuentos), `volcar_dos_meses.py` (el volcado sintético de
`escenarios_cuenta_por_mes.informe_dos_meses_con_criterio`), `combinar.py` (la parte del arnés de
`R1/cuenta-arrastrada.txt` con la cola sintética), `default_ambiguous.py` (`parametros.yaml`, los
`DEFAULT_AMBIGUOUS` con su `ambiguedad_id`) y `cuenta_cr.py` (cuenta bytes CR). Estaban en la carpeta
de trabajo de la sesión, con la raíz o los ficheros por argumento, y no escribían en el repo.

`resumen_corrida.py`, `diff_por_seccion.py` y `antes_del_dia.py` son guiones nuevos de la fase 2,
con su sitio en el README, sus tests (`antes_del_dia.py`) y su fila de exposiciones; y a
`para_clasificar.py` se le añadió el resumen por mes de las órdenes sin trader (con su test).
Ninguno lee una vela, un tick ni un caso. Ningún fichero de la carpeta lleva CR (contado).

## 1. La corrida 1, la que cuenta (`cuenta-por-mes.txt`)

**El veredicto (D1), literal:**

`habilita medir el conjunto de medida (2026-05) (ADR-0070): no (cobertura 15.7 % por debajo de 70.0 %; precision 13.9 % por debajo de 60.0 %)`

Dice «no»: por ADR-0070 §4 se sigue construyendo, mayo no se toca y el umbral no cambia. La salida no
lleva ningún rótulo DIAGNOSTICO; su cabecera de simulación dice `PERFIL: ftmo-2step-swing-100k; FASE:
reto` y `CUENTA: UNA POR MES (ADR-0092 §8): 4 cuentas`.

**El tramo no es continuo y la curva es indicativa** (como dijo R3.1): cuatro meses separados, cada
uno su cuenta desde 100.000.

### 1.1 Por mes (= por cuenta) y en total (ADR-0043), sin interpretar

| mes | trader | bot puntuables | bot en días sin trader | parejas | cobertura | precisión | llenadas |
|---|---|---|---|---|---|---|---|
| 2026-01 | 54 | 88 | 0 | 7 | 7/54 (13,0 %) | 7/88 (8,0 %) | 88 |
| 2026-04 | 35 | 51 | 19 | 8 | 8/35 (22,9 %) | 8/51 (15,7 %) | 70 |
| 2026-07 | 67 | 53 | 0 | 14 | 14/67 (20,9 %) | 14/53 (26,4 %) | 53 |
| 2026-08 | 42 | 31 | 5 | 2 | 2/42 (4,8 %) | 2/31 (6,5 %) | 36 |
| total | 198 | 223 | 24 | 31 | 31/198 (15,7 %) | 31/223 (13,9 %) | 247 |

(«### Resumen por mes» y «## Criterio de fidelidad»; llenadas, «### Posiciones» por mes, en
`resumen-cuenta-por-mes.txt`.) Parejas en el mismo minuto: 18.

### 1.2 La cascada de ADR-0092 §2, por escalón (literal de «### Fidelidad por criterios»)

| mes | sin orden en su (día, sesión, dirección) | entrada fuera (3 puntos) | stop fuera (3 puntos) | sin stop en el caso | en el nivel, no llenada | llenada fuera (15 min) | las cuatro piezas | total |
|---|---|---|---|---|---|---|---|---|
| 2026-01 | 8 | 25 | 18 | 0 | 1 | 0 | 2 | 54 |
| 2026-04 | 9 | 13 | 7 | 0 | 1 | 0 | 5 | 35 |
| 2026-07 | 20 | 22 | 16 | 0 | 3 | 0 | 6 | 67 |
| 2026-08 | 30 | 7 | 3 | 0 | 1 | 0 | 1 | 42 |
| total | 67 | 67 | 44 | 0 | 6 | 0 | 14 | 198 |

`ordenes del bot en un (dia, sesion, direccion) sin ninguna operacion del trader: 425`.

### 1.3 Las líneas literales de «## El metodo de ADR-0092»

```
posiciones: 247; PnL neto total (USD): -33488.67
tolerancias: entrada 3 puntos, stop 3 puntos, llenado 15 min
### Material sin video (ADR-0092 §11; DIAGNOSTICO, ningun umbral lo lee)
libros sin video: 2026-01, 2026-04, 2026-08, salvo 2026-04-29; cuentan como CON video, provisionales hasta que T lo compruebe: 2026-07 (fuente: ACTIVAR-SESION-05.md §0.b.7)
operaciones del bot quitadas (break_even en un dia sin video): 62
cascada sin ellas, total | sin orden del bot en su (dia, sesion, direccion) 67 | orden, con la entrada fuera de tolerancia 70 | entrada, con el stop fuera de tolerancia 43 | entrada; el caso no trae stop 0 | en el nivel, no llenada 6 | en el nivel, llenada fuera de tolerancia de instante 0 | las cuatro piezas 12
esperanza sin ellas (media del R neto, 185 operaciones): -0.606
### Rentabilidad (ADR-0092 §3; DIAGNOSTICO sobre construccion, ADR-0092 §6: la puerta solo se mide sobre 2025-06, 2025-07, 2025-08, 2025-09, 2025-10, 2025-11, fase fondeada)
FASE de esta corrida: reto
a) N (operaciones llenadas y cerradas): 247
b) esperanza (media del R neto): -0.533
c) percentil 5 de la media del R neto, por remuestreo por dias (10000 replicas, semilla 20261107, 76 dias): -0.715; replicas descartadas por no tener ninguna operacion: 0 de 10000
d) perdida diaria maxima (equity, base saldo_corte_diario), por cuenta: 4.31 % del capital inicial; la peor, la cuenta de 2026-01
e) equity minima, por cuenta: 90.68 % del capital inicial; la peor, la cuenta de 2026-07
f) alguna cuenta entro en SUSPENDIDA: no
criterios a) a f): no pasa (b) esperanza -0.533 por debajo de 0.10 R; c) percentil 5 del remuestreo -0.715, no mayor que 0; d) perdida diaria maxima 4.3 %, en o por encima de 3.0 %; e) equity minima 90.7 %, por debajo de 94.0 %)
deslizamiento por llenado afectado que lleva la esperanza a 0.10 R (ADR-0092 §4, sin decidir nada): -4.30 puntos
```

Diagnóstico sobre construcción (ADR-0092 §6): ninguna cifra de aquí justifica nada.

### 1.4 Cada cuenta mensual («### Cuenta de AAAA-MM»)

| cuenta | estado (veredicto) | saldo final = equity final | días de trading / en la curva | equity mínima (derivada) | peor pérdida diaria (derivada) | racha al cerrar el mes | primero en tocar |
|---|---|---|---|---|---|---|---|
| 2026-01 | EN_CURSO, «sin objetivo alcanzado ni limite infringido» | 90.946,91 | 21 / 21 | 90,71 % (2026-01-30) | 4,31 % (2026-01-13) | 7 seguidas; la última el 2026-01-29 | ninguno |
| 2026-04 | EN_CURSO, ídem | 93.989,60 | 21 / 21 | 92,78 % (2026-04-29) | 1,80 % (2026-04-09) | 0 seguidas; la última el 2026-04-28 | ninguno |
| 2026-07 | EN_CURSO, ídem | 90.682,74 | 12 / 13 | 90,68 % (2026-07-17) | 2,46 % (2026-07-14) | 3 seguidas; la última el 2026-07-17 | ninguno |
| 2026-08 | EN_CURSO, ídem | 90.892,08 | 11 / 21 | 90,75 % (2026-08-18) | 1,88 % (2026-08-03) | 3 seguidas; la última el 2026-08-18 | ninguno |

Lo literal es del bloque; la equity mínima y la peor pérdida diaria de cada cuenta son DERIVADAS de
su curva con las funciones del criterio (`resumen_corrida.py`, D5 y 0.k punto 5): la salida solo da
la peor (d) 4,31 %, cuenta de enero; e) 90,68 %, julio), y coinciden. «0 seguidas; la última el
2026-04-28» es literal. **Ninguna cuenta acabó SUSPENDIDA.**

**RN-032** (sin columna propia; de «Por sesion», las sesiones con operaciones del trader, columna
`disparadas`). La cuarta columna cuenta COINCIDENCIAS, no causas: sesiones con RN-032 disparada y,
en la misma línea, `bloqueadas` con `prohibida:abrir_operacion`, que es la acción de RN-015
(`colocar_orden_limite`) bloqueada por un gate que la línea no nombra, y sale en 96 de las 104
sesiones haya RN-032 o no (revisor, a1; RECORRIDA-CONSTRUCCION.md §2.2, a4). *Corregido tras la
respuesta del consultor a la PARADA 2, punto 9: la redacción del a1 decía «que es siempre de
RN-015».*

| mes | sesiones | RN-032 disparada | de ellas, con la acción de RN-015 bloqueada (`prohibida:abrir_operacion`) | primer y último día |
|---|---|---|---|---|
| 2026-01 | 30 | 3 | 3 | 2026-01-13 a 2026-01-30 |
| 2026-04 | 23 | 0 | 0 | — |
| 2026-07 | 25 | 2 | 2 | 2026-07-17 |
| 2026-08 | 26 | 14 | 13 | 2026-08-19 a 2026-08-31 |

Sobre las 152 sesiones corridas, `RN-032: 25 de 152; 19 de 104`. En la cuenta de agosto el bot no
llena ninguna orden desde el 2026-08-19 (0 filas `llenada` en «Ordenes» del 19 al 31; última posición
el 2026-08-18): 11 días de trading de 21. La última posición de las otras: enero, el 2026-01-30;
abril, el 2026-04-29; julio, el 2026-07-17.

### 1.5 Las peticiones y el freno

| mes | días | total | máximo diario |
|---|---|---|---|
| 2026-01 | 21 | 715 | 66 |
| 2026-04 | 21 | 626 | 64 |
| 2026-07 | 13 | 420 | 53 |
| 2026-08 | 21 | 365 | 57 |
| total | 76 | 2.126 | 66 |

`maximo diario: 66 (2026-01-19); firma_mensajes_dia_max: 2000`. El freno de ADR-0067 (PROVISIONAL
bajo A-54): `umbrales: aviso 1000, corte 1500, bucle 5 iguales en 1 min` y `ningun aviso ni ninguna
peticion negada`. Los cierres de ADR-0068: `ninguna peticion negada ni ninguna pendiente cancelada`.
Rechazos del bróker: 32, todos `precio_invalido` al colocar (8, 11, 9 y 4 por mes).

### 1.6 Lo que el arnés hace ahora y antes no (D6)

- **ADR-0089 (RN-020).** La cabecera pasa de `reinicio en Europe/Prague; SUPUESTO: reinicio con el
  huso de corte del perfil (el trader no dijo otro)` a `reinicio al abrir la primera sesion del dia
  siguiente (de sesion en sesion)`. RN-020 **no dispara en ninguna de las 152 sesiones** en la
  corrida 1 ni en la 2, ni lo hacía en las dos de RESPALDO-M1 (`RN-020: no sale en la seccion` en
  los cuatro `resumen-*.txt`; `detenido_por_tope: 0 de 104` en el embudo): ADR-0089 no detiene
  ninguna sesión que antes no, ni al revés.
- **ADR-0085 §2 en M15 y `solo_la_contraria` (F38n y F38o).** No se pueden separar en esta rama:
  el efecto de la spec y el motor de la sesión 6 va mezclado con el del sello en el `diff` de la
  diaria (§3.2), y separarlo pediría correr el motor con otra lectura, que la rama no hace (D11 y
  la autorización expresa). Lo medido: en la diaria cambian 16 de las 104 líneas «Por sesion» y las
  llenadas pasan de 286 a 302.
- **ADR-0085 §4 (S-10, la orden que nace en el primer punto tras la toma).** **No medible con la
  salida sola**: la salida no trae el instante de la toma ni las zonas formadas desde ella; lo
  medía `anexos/RECORRIDA-CONSTRUCCION/entradas_antes_alternancia.py`, que carga velas y no está
  autorizado. Lo que la salida sí da: las 247 posiciones de la corrida 1 son órdenes **stop**
  (`tipo stop` en «Posiciones», los cuatro meses), el camino por el que ADR-0085 §4 dice que S-10
  entra. Queda para la PARADA 2.
- **ADR-0086, RN-036 y RN-037: no son nuevos** (0.k, punto 2). Lo que cambia es su efecto: RN-036
  dispara en 6 de 152 sesiones (en la arrastrada de RESPALDO-M1, 2; en las dos diarias, 0) y
  `detenido_por_racha` en 4 de 104 (una por mes; antes, 1), porque la racha vive lo que vive cada
  cuenta; RN-037, 152 de 152 en las cuatro salidas.
- **El sello de ADR-0091.** Eventos del bróker: `eventos: 594; por fuente: respaldo_m1 18, ticks
  576` (por mes, `resumen-cuenta-por-mes.txt`). Las cancelaciones del bot en el cierre de una M1
  sin ticks (el tipo que SELLO-RESPALDO-M1.md §0.i dejó a la re-corrida), con su `censo_cierre.py`:
  **24 en la corrida 1**, todas en hora perdida, y **una fuera de los once días** de SELLO-RESPALDO-M1
  §0.b: 2026-01-05, sesión 11-15, o22 (`censo-cierre-cuenta-por-mes.txt`). En la diaria, 28, y la
  misma, 2026-01-05, fuera de los once.
- **RN-032 por cuenta**: §1.4. Con la arrastrada bloqueaba desde el 2026-01-20 y con ella abril,
  julio y agosto enteros (`RN-032: 128 de 152`); **enero es la primera cuenta, no la cuarta** (0.k,
  punto 1), y en enero RN-032 dispara ahora en 3 sesiones con trader (antes 14).
- **Los parámetros DEFAULT_AMBIGUOUS** con los que corrió: los ocho de 0.j.
- La fase 3 de S-22 no se hace aquí (D6).

## 2. La corrida 2, la de contexto (`diaria.DIAGNOSTICO.cuenta=diaria.txt`)

El veredicto literal:
`habilita medir el conjunto de medida (2026-05) (ADR-0070): no (opción fuera de la lista: --diagnostico-cuenta-diaria; cobertura 20.2 % por debajo de 70.0 %; precision 14.6 % por debajo de 60.0 %)`
(RESPALDO-M1: 20,2 % y 15,4 %).

| mes | trader | bot puntuables | parejas | cobertura | precisión | llenadas |
|---|---|---|---|---|---|---|
| 2026-04 | 35 | 52 (51) | 8 (7) | 22,9 % (20,0) | 15,4 % (13,7) | 71 (69) |
| 2026-07 | 67 | 57 (54) | 14 (14) | 20,9 % (20,9) | 24,6 % (25,9) | 57 (54) |
| 2026-08 | 42 | 77 (73) | 11 (12) | 26,2 % (28,6) | 14,3 % (16,4) | 86 (82) |
| 2026-01 | 54 | 88 (81) | 7 (7) | 13,0 % (13,0) | 8,0 % (8,6) | 88 (81) |

(entre paréntesis, RESPALDO-M1 §4.5). Parejas 40 (40). Su cascada: 48 sin orden, 72 entrada fuera, 54
stop fuera, 6 no llenada, 18 las cuatro piezas; 526 órdenes sin trader. Rentabilidad: N 302,
esperanza -0.572, percentil 5 -0.734; d) 1,13 % y e) 98,87 % son las del ÚLTIMO día (la cuenta
empieza cada día: `CUENTA: REINICIADA CADA DIA (diagnostico)`). Ninguna sesión con RN-020; RN-032 en
1 de 152.

## 3. Los dos diffs (D3), por sección, con sus atribuciones

Repartidos por `diff_por_seccion.py` (`diff-linea-base-por-seccion.txt` y
`diff-diaria-por-seccion.txt`; líneas quitadas y puestas por sección y por mes). Las categorías:
comisión (F38p, ADR-0090 §3), sello (F38q, ADR-0091), sesión 6 (F38n y F38o), camino de la cuenta
(F38s, ADR-0092 §8), salida nueva sin decisión (F38r, ADR-0092 y la cola de F38s), y «sin atribuir».

### 3.1 `diff-linea-base.txt` (arrastrada de RESPALDO-M1 → corrida 1): 670 líneas quitadas, 2.973 puestas

| Sección | quitadas / puestas | Atribución y evidencia |
|---|---|---|
| «Criterio de fidelidad», «Embudo», «Reglas disparadas» | 6/6, 3/3, 17/18 | todo junto; sin atribuir línea a línea |
| «Avisos de orden» | 27 / 438 | camino de la cuenta: abril, julio y agosto vuelven a operar |
| «Por sesion» | 74 / 74 (enero 15, abril 23, julio 24, agosto 12) | abril, julio y agosto, camino de la cuenta (RN-032 23/25/26 sesiones → 0/2/14); enero, motor (comisión y lo demás): enero tiene el mismo camino de cuenta en las dos |
| «Resumen por mes», «Embudo por mes», «Por operacion» | 4/4, 8/8, 135/305 | lo mismo: en abril, julio y agosto el bot pasa de 0 operaciones puntuables a 51, 53 y 31 |
| La cuenta: «Veredicto de la cuenta sobre el tramo» y «Curva de equity» salen; entran los cuatro «### Cuenta de AAAA-MM» | 5+77 / 32+32+22+28 | salida nueva de F38s (con varias cuentas, un bloque por mes, `cableado.py:879-892`) y, dentro, el camino de la cuenta |
| «Eventos del broker» | 44 / 511 | enero: 42 quitadas y 124 puestas (comisión y motor); abril, julio y agosto solo puestas (camino de la cuenta) |
| «Ordenes» | 209 / 1.144 | **comisión**, evidencia: el 2026-01-02 las dos tienen los mismos eventos (`llenada o7`, `stop pos-o7`, `llenada o9`) y el saldo final pasa de 99.686,25 a 99.875,16 (+188,91): o7 lleva 24,30 lotes en las dos y o9 13,45 en la vieja y 13,46 en la nueva; la comisión de ese día era (24,30 + 13,45) × 10 = 377,50 (5 USD por lote y lado) y es 121,50 + 67,30 = 188,80 (2,50; «Posiciones»): 188,70 de ahorro, y los 0,21 que faltan los da el lote mayor de o9 en su ganancia de 21 puntos (*corregido tras el revisor, b2: la primera redacción atribuía 0,11 a un lote de o1*). Desde ahí, saldos y lotes distintos en enero; abril, julio y agosto, camino de la cuenta |
| «Rechazos por motivo» | 1 / 4 | camino de la cuenta (abril, julio y agosto con rechazos) |
| «Peticiones al servidor» | 58 / 58 | abril, julio y agosto: 0 → 626, 420 y 365 (camino de la cuenta); enero, 14 días (motor) |
| «Los cierres de mercado» | 0 / 1 | la línea en blanco antes de la sección nueva; la línea `calendario:` es la misma en las dos (228 cierres, el mismo margen y la misma política; no se copia aquí porque nombra el inicio de lo que cubre, en diciembre: revisor, b7): el cambio de F38p no se ve en la salida |
| «## El metodo de ADR-0092» y sus cuatro tablas | 0 / 280 | salida nueva, sin decisión (F38r) |

En enero no hay camino de la cuenta que atribuir: todo lo de enero es del motor. Separarlo entre
comisión, sello y sesión 6 lo hace el `diff` de la diaria.

### 3.2 `diff-diaria.txt` (diaria de RESPALDO-M1 → diaria nueva): 1.488 quitadas, 1.953 puestas

| Sección | quitadas / puestas | Atribución y evidencia |
|---|---|---|
| «Ordenes» | 1.078 / 1.137 | **comisión**: el 2026-01-02 o8, con los mismos instantes y precio, el margen libre al colocar pasa de 99.538,30 a 99.659,80 (+121,50 = 24,30 lotes × 2,50 × 2 lados que se ahorra pos-o7) y su lote de 24,19 a 24,22 (`diff-diaria.txt:1006-1011`); así en cada orden posterior a una posición del día |
| «Eventos del broker» | 264 / 296 | **sello**: un evento del respaldo M1 pasa del inicio de la vela al cierre de la anterior, p. ej. 2026-04-06 `llenada o11` de `10:02:00` a `10:01:59.999` y su `stop` de `10:15:00` a `10:14:59.999` (`diff-diaria.txt:600-607`); y operaciones nuevas, como 2026-04-08 o7 (`llenada`, `stop_movido`, `objetivo`, por ticks, `diff-diaria.txt:615-618`): **sin atribuir** entre sesión 6 y sello |
| «Por sesion», «Por operacion», «Resumen por mes», «Embudo» | 16/16, 43/59, 4/4, 2/1 | motor (sesión 6 y sello), sin atribuir entre ellos: llenadas 286 → 302 (enero 81 → 88, abril 69 → 71, julio 54 → 57, agosto 82 → 86) |
| «Veredicto», «Curva» | 2/2, 1/1 | el último día (2026-08-31), comisión y motor |
| «## El metodo de ADR-0092» y sus tablas | 0 / 335 | salida nueva, sin decisión (F38r) |

Lo que no se puede atribuir con lo commiteado: cuántas de las 16 sesiones que cambian en la diaria
son de la sesión 6 y cuántas del sello (las dos entran a la vez entre F38j y F38s, y la rama no corre
el motor con otra versión).

## 4. Los patrones, de las dos corridas, por mes (D4)

`patrones.py`, copia idéntica, sobre las dos salidas (`patrones-cuenta-por-mes.txt`,
`patrones-diaria.txt`; con `--filas`). **Manda la corrida 1.**

| mes | T0 | P1 | P2 | P3 | P4 | P5 | P6 | P7 |
|---|---|---|---|---|---|---|---|---|
| **corrida 1** 2026-01 | 7 | 7 | 17 | 21 | 1 | 66 | 15 | 1 |
| 2026-04 | 8 | 9 | 5 | 12 | 1 | 29 | 33 | 0 |
| 2026-07 | 14 | 20 | 14 | 15 | 1 | 37 | 2 | 3 |
| 2026-08 | 2 | 8 | 4 | 6 | 22 | 21 | 13 | 0 |
| **total corrida 1** | **31** | **44** | **40** | **54** | **25** | **153** | **63** | **4** |
| corrida 2 (diaria), total | 40 | 44 | 44 | 60 | 6 | 185 | 77 | 4 |
| RESPALDO-M1, arrastrada | 7 | 44 | 11 | 11 | 124 | 37 | 9 | 1 |
| RESPALDO-M1, diaria | 40 | 44 | 40 | 62 | 8 | 171 | 75 | 4 |

(Las de RESPALDO-M1, de `anexos/RESPALDO-M1/patrones-*.txt`: las del encargo.) La diaria nueva por
mes: enero 7/7/17/21/1/66/15/1, abril 8/9/5/12/1/30/33/0, julio 14/20/14/15/1/41/2/3, agosto
11/8/8/12/3/48/27/0. Filas marcadas «posible M»: 18 en la corrida 1, 23 en la diaria.

Lo que separa las corridas, sin ajustar nada: entre la arrastrada y la corrida 1, el camino de la
cuenta (abril, julio y agosto pasan de P4 a tener bot: P4 124 → 25) y el motor; entre las dos
diarias, solo el motor (P1 igual, 44; P4 8 → 6; P5 171 → 185); entre la corrida 1 y la diaria nueva,
solo el camino de la cuenta, y la diferencia está casi entera en agosto (P4 22 frente a 3, T0 2
frente a 11), donde la cuenta de agosto deja de llenar desde el 2026-08-19 (§1.4).

## 5. La lista «Para clasificar» (D8), resumida

Entera en `anexos/RECORRIDA-CONSTRUCCION-2/para-clasificar.txt`. **El escalón llega hasta la
entrada** (0.k, punto 6): la salida no trae el stop del trader. `para_clasificar.py` comprueba lo
que cuenta contra la cascada que imprime cada salida: **coincide** en las dos (los dos primeros
escalones, mes a mes; los cinco últimos, sumados; y las órdenes sin trader, 425 y 526).

**Operaciones del trader por escalón:**

| mes | corrida | sin orden en su (día, sesión, dirección) | entrada fuera | entrada dentro (stop, llenado: sin leer) | órdenes del bot sin trader |
|---|---|---|---|---|---|
| 2026-01 | 1 | 8 | 25 | 21 | 79 |
| 2026-04 | 1 | 9 | 13 | 13 | 193 |
| 2026-07 | 1 | 20 | 22 | 25 | 34 |
| 2026-08 | 1 | 30 | 7 | 5 | 119 |
| total | 1 | 67 | 67 | 64 | 425 |
| total | 2 | 48 | 72 | 78 | 526 |

(La corrida 2 por mes, en el fichero; enero, abril y julio igual que la 1; agosto 11, 12 y 19, y 185.)
De las 64 «entrada dentro» de la corrida 1, la cascada de la salida da 44 con el stop fuera, 6 en el
nivel no llenadas y 14 con las cuatro piezas.

**Órdenes del bot sin trader en su (día, sesión, dirección), corrida 1:**

| mes | órdenes | llenadas | suma del R neto de las llenadas | stop movido | desenlaces | patrones |
|---|---|---|---|---|---|---|
| 2026-01 | 79 | 19 | -0,281 | 8 | break_even 4, ganancia 5, salto_el_stop 10 | P5 4, P6 15 |
| 2026-04 | 193 | 43 | -25,861 | 21 | break_even 17, ganancia 4, salto_el_stop 22 | P5 10, P6 33 |
| 2026-07 | 34 | 12 | -14,285 | 3 | break_even 2, ganancia 1, salto_el_stop 9 | P5 10, P6 2 |
| 2026-08 | 119 | 22 | -24,171 | 10 | break_even 10, salto_el_stop 12 | P5 9, P6 13 |
| total | 425 | 96 | -64,598 | 42 | break_even 33, ganancia 10, salto_el_stop 53 | P5 33, P6 63 |

«Si pasó por break even» (D8) se lee con dos columnas (revisor, b6): «stop movido», que es «sí» si en
«### Eventos del broker» hay un `stop_movido` de su posición (el stop movido por RN-014; la salida no
dice a qué nivel, así que no prueba que fuera al precio de entrada), y «desenlace», que es
`break_even` cuando la posición se cerró por el stop después de moverlo (`clasificar_cierre`).

Cada fila del trader en el fichero lleva también su patrón (corrida 1 y 2), el primer hecho que
falta en su sesión, el vídeo del día (`material_sin_video`) y la marca de hora perdida. Sin
conclusiones: la clasificación (error nuestro o regla desconocida) es del consultor en la PARADA 2.

## 6. Las líneas del cierre, preparadas y medidas (no aplicadas)

Con `anexos/RECORRIDA-CONSTRUCCION-2/simular_cierre.py` (en memoria sobre copias; en el repo no
escribe nada), contra `tests/unit/test_hoja_de_ruta.py` y `tests/unit/test_project_state.py`:

- **Next Action, F** (el texto del encargo, con el veredicto literal resumido en una línea):
  «F. Sesión 6 ACTIVADA en spec (F38n) y motor (F38o); S-22 y S-19 a la sesión 7 (§d de
  ACTIVAR-SESION-06-MOTOR.md). La re-corrida que cuenta está hecha (RECORRIDA-CONSTRUCCION-2.md;
  veredicto «no» (cobertura 15.7 % por debajo de 70.0 %; precision 13.9 % por debajo de 60.0 %);
  línea base vigente anexos/RECORRIDA-CONSTRUCCION-2/cuenta-por-mes.txt). Siguiente: la preparación
  de la sesión 7 (hoja + gráficos 2 a 6 con contexto; lista en ACTIVAR-SESION-06.md §«Para la sesión
  7», más S-22 y S-19 con sus esquemas y el 52 %, más lo que la clasificación de la re-corrida añada,
  RECORRIDA-CONSTRUCCION-2.md §5); J antes si la hoja sale de kit hoja. El vídeo de mapeo, si llega,
  SIN ABRIR y fuera del repo. R6a en los huecos.» Ninguna letra sale ni entra: vivas en la copia,
  `A D F G I J L M N Q T U` (J viva: «J antes» pasa la regla de la letra suelta).
- **Hoja de ruta:** R3.9 nueva tras R3.8 («La re-corrida que cuenta: comisión medida, sello, sesión
  6, método y cuenta por mes»; Refs `ID:ADR-0070 · ID:ADR-0090 · ID:ADR-0091 · ID:ADR-0092`, sin
  `NA:F` porque F sigue viva; HECHA con el veredicto); R5.2 «Depende de» cita R3.9 en lugar de R4.1;
  R5.6 sin cambio (la corrida dio «no»).
- **Technical Debt:** nada sale ni entra (lo que decida la PARADA 2, aparte).
- **Medido:** `a: []`, `b: []`, `c: []` de `test_hoja_de_ruta`; los cuatro tests de
  `test_project_state`, en verde sobre las dos copias; **PROJECT_STATE con las líneas aplicadas:
  22.837 bytes**, y **22.761 con las cuatro líneas de cabecera del cierre** (con un `Current Feature`
  y un `Last Stable Commit` en la forma corta de los cierres anteriores). Una primera versión mía de
  esas dos cabeceras, con la lista entera de lo que entró en la corrida, daba **23.053**: las
  cabeceras las escribe el ritual del cierre, no el encargo, y en la corta no se recorta nada de
  PROJECT_STATE. Margen: 163 bytes con las líneas aplicadas; si la PARADA 2 añade Technical Debt,
  hay que medir otra vez.

## 7. La fila de ERRORES-RECURRENTES, preparada

La rellenan los hallazgos del consultor en la PARADA 2. Lo de la sesión, para su columna de
lecciones: (1) un test de humo «copiado tal cual» no se copia si importa un guion que la rama no
copia o carga uno por una ruta calculada (la guardia lo niega fuera de `main`): se copian sus partes
y el original se corre en su sitio (fase 1); (2) la salida del arnés no trae el stop del trader ni la
dirección de una orden no llenada: una cascada por operación desde la salida sola llega a la entrada,
y lo deducido se comprueba contra la cascada impresa (§5); (3) las cuatro líneas de cabecera del
cierre cuentan para los 23.000 bytes: se miden en la forma que escribirá el ritual (§6); (4) unos
guiones de la fase 2 se nombraron en HOLDOUT-EXPOSICIONES después de correr (el mismo día, antes del
`make check`): la fila de la apertura los cubría solo como «los guiones de anexos». Y del revisor:
(5) **(importa, se repite)** la NOTA de ADR-0070 y §1.4 volvieron a atribuir a RN-032 el
`prohibida:abrir_operacion` de RN-015, el mismo error que el a4 del revisor de RECORRIDA-CONSTRUCCION
§2.2 y que el docstring de `resumen_corrida.py` ya advertía (a1). Lección: una columna de
coincidencia no se cuenta como causa, y lo que el propio guion advierte se lee antes de redactar la
NOTA; (6) **(importa)** fechas de meses con reservados en fixtures sintéticas de un test de anexos
(b1): las fixtures, de días dev o de 2030; y `antes_del_dia.py` sobre los `.py` y el informe, no solo
sobre las salidas.

## El encargo, punto por punto

| Punto del encargo | Hecho | Evidencia |
|---|---|---|
| Base: main ad225de, tag → 41d47b3, CI 42502468946 verde, ninguna otra rama | Hecho | apertura del informe |
| /model y REAP | Hecho: Opus 5.5; `REAP=1` | 0.h, fase 2 |
| Fila de HOLDOUT antes del primer make check | Hecho (14:07:29 frente a 14:10:25) | 0.g |
| abrir-rama: contrato, encargo, Archivo 62 | Hecho | `5eca8e3` |
| Fase 0, a) a h) | Hecho; PARADA condicional sin parar | §0, 46e69c5 |
| Fase 1: README, copias, test de humo, para_clasificar.py | Hecho, con la desviación del test de humo | Fase 1, `686a8b3` |
| Fase 2: tres corridas, D10, diffs, patrones, para_clasificar | Hecho | Fase 2, §1-§5 |
| D1 veredicto literal | Hecho: «no» | §1 |
| D2 NOTA en ADR-0070 §3 | Hecho, commit propio | `83727c3` |
| D3 dos diffs con atribuciones | Hecho; lo no atribuible, dicho | §3 |
| D4 patrones, manda la 1, copias idénticas | Hecho | §4, README |
| D5 | Hecho; dos cifras derivadas y dichas | §1 |
| D6 | Hecho, salvo S-10 (no medible con la salida) y la separación sesión 6 / sello | §1.6 |
| D7 NOTA en ACTIVAR-A35-A44.md §5, desviación del visor | Hecho, commit propio (con D2) | `83727c3` |
| D8 lista «Para clasificar» | Hecho, con el escalón hasta la entrada (0.k, 6) | §5 |
| D9 tiempos | Dentro | Fase 2 |
| D10 determinismo | `diff=0` | Fase 2 |
| D11 nada de src/, tests/, knowledge/ | Hecho | `git diff main --stat` (revisor, alcance 2) |
| D12 nada a la hoja de la sesión 7 | Hecho | — |
| Líneas del cierre | Preparadas y medidas | §6 |
| Revisor | Ver su sección | al final |

## Desviaciones declaradas

1. **El visor no se abrió** (D7): ningún `motor visor --caso`; los días los pide el consultor en la
   PARADA 2. Lo dice la NOTA de §5 de `ACTIVAR-A35-A44.md`.
2. **`test_humo.py` no es la copia tal cual** del de `anexos/RECORRIDA-CONSTRUCCION/` (fase 1).
3. **La lista de D8 llega hasta la entrada**, no a los siete escalones (0.k, 6).
4. **Dos cifras de D5 son derivadas** (la equity mínima y la peor pérdida diaria de cada cuenta) y
   RN-032 se lee por «Por sesion» (0.k, 5; §1.4).
5. **S-10 no se midió** y **la sesión 6 no se separó del sello** (§1.6).
6. **Guiones de anexos nuevos en la fase 2** (`resumen_corrida.py`, `diff_por_seccion.py`,
   `antes_del_dia.py`) y `censo_cierre.py` de SELLO corrido sobre las salidas nuevas: el encargo no
   los pedía; leen solo salidas y están en el README y en su fila de exposiciones, escrita después
   de correrlos (§7, punto 4).
7. **Las cabeceras del cierre en forma corta** (§6).
8. **Enero es la primera cuenta**, no la cuarta como decía D6 (0.k, 1).
9. **Un id con fecha de un mes con días reservados en cuatro versiones commiteadas del informe**
   (`46e69c5`, `686a8b3`, `7918f29` y `83727c3`, tabla de 0.j; revisor, b5): la `fuente` de `orden_pendiente_al_abrir_escenario` es un `fb-` cuyo id lleva la fecha de la
   sesión 3 con el trader (un día de septiembre: no es un día de mercado ni una cifra del bot, y el
   mismo id está en `knowledge/spec/parametros.yaml` de `main`). Lo vio, en la entrega, una pasada de
   `antes_del_dia.py` sobre el informe que no quedó en `antes-del-dia.txt` (solo cubre los 16
   ficheros de la carpeta); se quita de la tabla y la historia no se reescribe (rebase y squash no
   pasan por la puerta).

## Las exposiciones de cada día

Un solo día de trabajo, el 2026-11-08: seis filas de esta rama en `HOLDOUT-EXPOSICIONES.md`, tres de
las fases 0 a 2 (la de la apertura, la de lo que no nombraba y la de la entrega) y tres de la fase 3
(la de la apertura de la fase, la de lo que no nombraba y la de los recuentos que pidió el revisor,
a3). Ninguna etiqueta ni cifra del bot de un día reservado; nada
de mayo; `antes_del_dia.py` da 0 líneas con algo anterior al día de su fila o fuera de la
construcción en los 16 ficheros de la carpeta.

## Los make check de la rama

| Commit | Árbol sellado | Resultado |
|---|---|---|
| `5eca8e3` (apertura) | `17f4413c…` | 3343 passed, 1510 s, pico 309 MiB |
| `46e69c5` (fase 0) | `0433be14…` | 3343 passed, 1473 s |
| `686a8b3` (fase 1) | `3e666d1f…` | 3343 passed |
| `7918f29` (salidas) | `e84906ac…` | 3343 passed, 1434 s |
| `83727c3` (NOTAS de D2 y D7) | `151ff208…` | 3343 passed, 1303 s |
| `d77b0a9` (entrega de la PARADA 2) | `d5b66a09…` | 3343 passed, 1378 s |
| fase 3, antes de los arreglos del revisor | `51e3f58b…` | 3343 passed; no se commiteó: los arreglos lo cambiaron |
| fase 3 (PARADA 3) | ver el log del commit | ver «Estado» |

## Lo que necesito que decidas (PARADA 2)

La clasificación de cada diferencia (error nuestro o regla desconocida), qué días van al visor y qué
entra en la hoja de la sesión 7 son tuyos (D12). Además:

0. **El escalón entero de la cascada por operación (D8).** Opciones: (a) dejarlo hasta la entrada,
   como sale de la salida sola (§5); (b) un guion que lea el stop del trader de los casos dev
   (`knowledge/cases/dev/`, material de desarrollo, sin puerta) para cerrar los cinco escalones de
   detrás, en la rama de la preparación de la sesión 7. Recomiendo (b) si la clasificación necesita
   separar «stop fuera» de «no llenada» por operación: la cascada por mes ya lo da (44 y 6). Coste de
   (b): un guion y su declaración.
1. **S-10 (ADR-0085 §4) y la separación sesión 6 / sello (§1.6).** Opciones: (a) dejarlos sin medir;
   (b) medir S-10 con el visor en los días que elijas, en tu respuesta. Recomiendo (b) solo para los
   días que vayan al visor de todos modos. Coste de (b): ninguno aparte del visor.
2. **Una NOTA también en §5.1 de `ACTIVAR-A35-A44.md`** (herencia H2: su cuerpo sigue llamando
   «línea base vigente» a `CABLEADO-SIMULADOR-LINEA-BASE.txt`). Opciones: (a) no, la de §5 basta (D7);
   (b) una línea igual, en el commit del cierre. Recomiendo (a). Coste de (b): una línea.
3. **Las cabeceras del cierre (§6).** Opciones: (a) la forma corta (22.761 bytes); (b) la larga
   (23.053, por encima de 23.000). Recomiendo (a). Coste de (b): pasa la alerta.

Espero tu respuesta a la PARADA 2.

## Apéndice A · El informe del auditor del encargo (fase 0, 2026-11-08), tal cual

> ## Auditoría del encargo · trabajo/recorrida-construccion-2 · 2026-11-08
> Resumen: 52 afirmaciones; 38 correctas, 3 incorrectas, 11 con matiz. 3 herencias no recogidas.
>
> Encargo: `C:\Users\USER\Desktop\Bot v3\docs\encargos\trabajo-recorrida-construccion-2.md`. Solo he leído: no he ejecutado el arnés, ni make, ni gh. No he listado ni leído nada de holdout, corpus/ ni data/ (salvo los nombres de `data/manifests/`). No imprimo ninguna fecha reservada.
>
> ### Afirmaciones
> | # | Afirmación (literal o resumida del encargo) | Veredicto | Evidencia |
> |---|---|---|---|
> | 1 | «main es ad225de» | CORRECTA | `git rev-parse --short main` → ad225de |
> | 2 | «stable/F38s-cuenta-por-mes apunta al merge 41d47b3» | CORRECTA | `git rev-parse --short "stable/F38s-cuenta-por-mes^{commit}"` → 41d47b3 |
> | 3 | «no queda otra rama ni local ni en origin» | CORRECTA | `git for-each-ref refs/heads refs/remotes` → main, trabajo/recorrida-construccion-2, origin/main |
> | 4 | OPCIONES_QUE_NO_CAMBIAN_LA_CORRIDA está en engine/arnes.py y la corrida 1 solo usa opciones de esa lista | CORRECTA | arnes.py:80-82 (`--salida --tracemalloc --meses --simular --perfil --fase`); las opciones se leen de los parsers, cli.py:2218-2232 y 2450 |
> | 5 | Perfil y fase efectivos = perfil_para_medir y la primera fase del perfil | CORRECTA (con matiz menor) | cli.py:2398 y 2441; cableado.py:649-663 (hay un solo perfil en knowledge/cuentas) y :698; criterio_fidelidad.yaml:37. Matiz: `perfil_para_medir` no vive en arnes.py sino en criterio_fidelidad.py:78 y en el yaml |
> | 6 | «el motor no necesita ningún --diagnostico-*» | CORRECTA | ADR-0070:81-88 (NOTA del 2026-10-26); diagnostico.py:105-118 (A-35 fijada); ambiguedades.yaml:1442 (A-44 RESUELTA) |
> | 7 | La cuenta por mes es una condición del recorrido, sin opción (MotorCableado.correr_dia) | CORRECTA | cableado.py:306-316; ADR-0092:197-205 |
> | 8 | La corrida 2 se llamará diaria.DIAGNOSTICO.cuenta=diaria.txt (nombre_etiquetado) | CORRECTA | diagnostico.py:39, 93-94 y 169-185 |
> | 9 | El motivo f) con varias cuentas: medir_por_cuentas en criterio_fidelidad.py | CORRECTA | criterio_fidelidad.py:696 y :809; cableado.py:1501-1533 |
> | 10 | _mes_anterior en arnes.py: marzo calienta abril, junio calienta julio, julio calienta agosto | CORRECTA | arnes.py:179-181 y 206-211 |
> | 11 | «enero no tiene mes anterior» / «enero calienta desde su propio mes» | MATIZ | `_mes_anterior("2026-01")` da "2025-12" (arnes.py:181). No lo lee porque no existe ningún manifiesto eurusd-m1-2025-12 (nombres de data/manifests) y el código salta con `continue` (arnes.py:209-210). El resultado es el que dice el encargo; la razón es la falta de datos, no el código |
> | 12 | Hay ticks para cada día dev de los cuatro meses | CORRECTA (por informe y git) | RECORRIDA-CONSTRUCCION.md:108-115; los manifiestos de ticks no cambian desde 490c820 (`git log -- data/manifests/ticks`); son 4 manifiestos, uno por mes |
> | 13 | «18 horas perdidas, 17 dentro de sesiones» | CORRECTA | RECORRIDA-CONSTRUCCION.md:116-118 |
> | 14 | El perfil lleva `firma_comision_usd_por_lote` 2.50 y `firma_comision_por_lado` true | CORRECTA | ftmo-2step-swing-100k.yaml:382-397 y 401-413 |
> | 15 | ADR-0090 §3: «las corridas anteriores … eran pesimistas en las suspensiones», y la re-corrida es la primera con la tarifa medida | CORRECTA | ADR-0090:107-110 |
> | 16 | «76 días dev y 198 operaciones» | CORRECTA (con matiz) | Operaciones contadas con `grep -c instante_utc` en knowledge/cases/dev: 54 (enero) + 35 (abril) + 67 (julio) + 42 (agosto) = 198. Días: 21+21+13+21 = 76 (RESPALDO-M1.md:268; ADR-0070:92). Matiz: en esos meses hay solo 21/16/13/19 ficheros de caso. Los días dev sin operaciones no tienen fichero; salen del reparto de vistos (arnes.py:154-172) |
> | 17 | material_sin_video: abril solo el 29; julio provisional; enero y agosto no | CORRECTA | criterio_fidelidad.yaml:61-65 |
> | 18 | Los guiones de anexos/RESPALDO-M1/ son patrones.py, horas_perdidas.py, censo_respaldo.py y sesiones_s14.py | MATIZ | Existen los cuatro. Hay dos más que el encargo no nombra: sonda_z.py y simular_cierre.py (anexos/RESPALDO-M1/README.md:53-57) |
> | 19 | patrones.py y horas_perdidas.py se copian idénticos | CORRECTA | Ya son idénticos a los de RECORRIDA-CONSTRUCCION (`git diff --no-index`, vacío). patrones.py importa horas_perdidas (README.md:39-40) |
> | 20 | «Su test de humo de anexos/RECORRIDA-CONSTRUCCION/test_humo.py se copia también y se corre» | INCORRECTA | test_humo.py:15-18 pone su propia carpeta en sys.path e importa `entradas_antes_alternancia` (`eaa`), que el encargo no copia: copiado tal cual, falla al importar. Además casi todo prueba `eaa`; lo que prueba de patrones compara con `CORRIDA-CONSTRUCCION/patrones.py` (:22, :135), y horas_perdidas no se prueba en ningún sitio |
> | 21 | El test test_con_varios_meses_la_salida_lleva_un_bloque_por_cuenta, y que no hay golden de varios meses | CORRECTA (con matiz) | tests/unit/test_cuenta_por_mes.py:242; tests/golden/cuenta_por_mes/ = main-dentro-de-un-mes.txt y main-diaria-dos-meses.txt. Matiz: ya hay salidas sintéticas de dos meses commiteadas en anexos/CUENTA-POR-MES/rama/ (dos-meses.txt, dos-meses-con-criterio.txt) |
> | 22 | Patrones de la arrastrada: T0 7, P1 44, P2 11, P3 11, P4 124, P5 37, P6 9, P7 1 | CORRECTA | anexos/RESPALDO-M1/patrones-arrastrada.txt:7 |
> | 23 | Patrones de la diaria: T0 40, P1 44, P2 40, P3 62, P4 8, P5 171, P6 75, P7 4 | CORRECTA | anexos/RESPALDO-M1/patrones-diaria.txt:7 |
> | 24 | RESPALDO-M1: 351 s y 630 MiB por corrida | CORRECTA | RESPALDO-M1.md:694 (la corrida 1, 351.0 s y 630.3 MiB; la diaria fue 315.8 s y 638.4 MiB, :695) |
> | 25 | «la diaria de ACTIVAR-SESION-06-MOTOR, 452 s y 640 MiB» | MATIZ | ACTIVAR-SESION-06-MOTOR.md:118-130: fue una corrida en proceso con el guion medir_f2_f3.py, que observa funciones (instrumentada), sobre el código previo a F38o; la segunda dio 428.5 s. Lo que no se ha medido nunca es el tiempo del remuestreo de 10.000 réplicas sobre 76 días (METODO-FIDELIDAD-RENTABILIDAD.md:1052-1053), que esta corrida es la primera en hacer |
> | 26 | Con la arrastrada, RN-032 congela desde el 2026-01-20 (RESPALDO-M1.md §4.5) | CORRECTA | RESPALDO-M1.md:754-756 |
> | 27 | D6: «ahora enero es la cuarta cuenta y propia» | INCORRECTA | `validar_meses` ordena los meses (arnes.py:121) y `dias_de_construccion` los recorre en ese orden (:148-151); CUENTA-POR-MES.md:40-46; CORRIDA-CONSTRUCCION.md:487 («enero, y luego de abril a agosto»). Enero es la PRIMERA cuenta. Ya lo era con la arrastrada, que empezaba en el capital en enero, así que el camino de su cuenta no cambia. Enero va cuarto solo en el yaml (criterio_fidelidad.yaml:47) |
> | 28 | D6: «Lo que el arnés hace ahora y antes no»: ADR-0086, RN-036 y RN-037 | INCORRECTA (en parte) | ADR-0086 es del 2026-10-26 (`trabajo/activar-sesion-05-motor`, F38f), anterior a RECORRIDA (F38g) y a RESPALDO-M1 (F38j); la línea base anterior ya lleva RN-037 en 110 líneas y RN-036 en 20 (`grep -c` sobre anexos/RESPALDO-M1/cuenta-arrastrada.txt). Lo que cambia ahora es su efecto: RN-020 por ADR-0089, y la racha de RN-036, que se reinicia con cada cuenta (F38s) |
> | 29 | D2: qué entró en el motor desde la línea base anterior: «ADR-0090 §3, ADR-0091, F38o, ADR-0092 y su §8» | MATIZ | Falta F38n: `liquidez_m15_mecha_que_vuelve` pasa de cualquier_mecha a solo_la_contraria (`git diff stable/F38j-respaldo-m1 stable/F38n-activar-sesion-06 -- knowledge/spec/parametros.yaml`), y el motor lo lee (arnes.py:219). ADR-0092 (F38r), en cambio, es solo salida (ADR-0092:371-373). F38p también cambió el calendario de cierres (`knowledge/cuentas/cierres/`, 7 líneas), sin medir |
> | 30 | D3(b): la diaria «aísla el cambio del motor» | MATIZ | La diaria de F38s sigue byte a byte (HISTORIA:16019), pero contra RESPALDO-M1 el diff también recoge la salida nueva de F38r («### Posiciones», «## El metodo de ADR-0092»; cableado.py:1226-1237). En las atribuciones de §3 hace falta una categoría «salida nueva, sin decisión» |
> | 31 | «sigue byte a byte» (registro de cierre de F38s) | CORRECTA | HISTORIA.md:16019 |
> | 32 | D2: NOTA «al final de las que ya tiene» en ADR-0070 §3 | MATIZ | Lo último de §3 no es una NOTA: es el recuadro «ENMENDADO POR ADR-0092» (ADR-0070:115-122), que va tras la NOTA del 2026-10-29 (:102-113). «Al final» quiere decir detrás del recuadro |
> | 33 | D7: la NOTA de F38g declaró la desviación del visor y la de F38j no | CORRECTA | ACTIVAR-A35-A44.md:222-236 y :238-244 |
> | 34 | D7: «una NOTA de una línea al principio de §5» | MATIZ | Las dos NOTAS que ya hay están al principio, en orden de fecha (:222, :238): «al principio» rompería ese orden si va delante. Y §5.1 sigue llamando «línea base vigente» a CABLEADO-SIMULADOR-LINEA-BASE (:281, :292) (herencia 2) |
> | 35 | El cuerpo de §5 hace diff contra CABLEADO-SIMULADOR-LINEA-BASE.txt y manda `motor visor --caso` | CORRECTA | ACTIVAR-A35-A44.md:246-250 |
> | 36 | R3.6 «Hecho cuando» pasa las dos corridas a R3.7 y a la re-corrida | CORRECTA | HOJA-DE-RUTA.md:222-224 |
> | 37 | R3.7: «la re-corrida que cuenta repite las dos corridas que pedía R3.6, ya con el sello de ADR-0091» | CORRECTA | HOJA-DE-RUTA.md:246-247 |
> | 38 | R5.2 «Depende de» cita la corrida que cuenta como R4.1 | CORRECTA | HOJA-DE-RUTA.md:376-378 |
> | 39 | R5.6 sigue pidiendo la re-corrida con «habilita medir: sí» | CORRECTA | HOJA-DE-RUTA.md:419 |
> | 40 | ADR-0091: «lo demás lo ve la re-corrida» | CORRECTA | ADR-0091:147-148 |
> | 41 | ADR-0085 §4: «la re-corrida lo mira» (S-10) | CORRECTA | ADR-0085:125-131 |
> | 42 | ADR-0085 §2 en M15: el recuadro de la sesión 6 | CORRECTA | ADR-0085:70-83 |
> | 43 | ACTIVAR-SESION-06.md: el efecto de `solo_la_contraria` lo mide la re-corrida | CORRECTA | ACTIVAR-SESION-06.md:286-287 |
> | 44 | ACTIVAR-SESION-06-MOTOR.md: la fase 3 de S-22, después de la re-corrida | CORRECTA | ACTIVAR-SESION-06-MOTOR.md:791 |
> | 45 | SELLO-RESPALDO-M1 deja a la re-corrida las cancelaciones fuera de los once días | CORRECTA | SELLO-RESPALDO-M1.md:341-344; ADR-0091:143-148 |
> | 46 | D5: de cada «### Cuenta de AAAA-MM»: veredicto, saldo, equity, equity mínima, peor pérdida diaria, racha, primer toque, y el día y la regla si RN-032 bloquea | MATIZ | El bloque (cableado.py:829-847) lleva estado, motivo, instante, saldo, equity, días, racha, primer toque y la curva (de ahí sale la equity mínima). La peor pérdida diaria por cuenta no la imprime: solo sale la del tramo con su mes (:1522-1526). RN-032 tampoco está en el bloque: va en «Por sesion», `bloqueadas` (arnes.py:336-339). Hay que derivarlas |
> | 47 | La cabecera dirá «CUENTA: UNA POR MES (ADR-0092 §8): 4 cuentas»; «## El metodo de ADR-0092» y «### Posiciones» | CORRECTA (en formato) | cableado.py:880, 1232 y 1237 |
> | 48 | PROJECT_STATE «hoy 22.832 bytes» | MATIZ | `git show main:PROJECT_STATE.md \| wc -c` = 22832; en el árbol de la rama, tras abrir-rama, `wc -c` = 22849 |
> | 49 | ADR-0070 §4 y §6; ADR-0092 §5 necesita G/PREREGISTRO; §6, la rentabilidad es diagnóstico; el tope del test es 25.000 | CORRECTA | ADR-0070:124-125 y 142-144; ADR-0092:140-144 y 160-170; test_project_state.py:21 |
> | 50 | ADR-0067 PROVISIONAL bajo A-54 | CORRECTA | ADR-0067:9 y 122-123; A-54 ABIERTA (ambiguedades.yaml:1835) |
> | 51 | Las filas del 2026-10-27, 2026-10-29 y 2026-11-08 en HOLDOUT-EXPOSICIONES | CORRECTA | `grep -c "^\| <fecha>"`: 3, 4 y 4 (en main, 3 del 2026-11-08) |
> | 52 | Tramo R3; R3.7 y R3.8 HECHAS; la re-corrida es lo siguiente según F | CORRECTA (con matiz) | HOJA-DE-RUTA.md:129, 252, 267; PROJECT_STATE.md:28 («Siguiente: la re-corrida que cuenta»). Matiz: ningún `###` de R3 lleva NA:F en sus Refs (NA:F está solo en :304 R4.2, :340 R4.3 y :677), y R3.9 no existe (`grep -c "R3\.9"` = 0). El encargo lo resuelve creando R3.9 en el cierre |
>
> ### Lo que el repo pide y el encargo no recoge
> | # | Qué | Dónde lo pide | Evidencia |
> |---|---|---|---|
> | 1 | Tres cosas que la rama del método dejó para la primera corrida real: cuánto tarda el remuestreo de 10.000 réplicas sobre 76 días, si RN-032 sigue congelando con el motor de hoy, y la primera salida real de la cascada, la rentabilidad y Posiciones. D9 no tiene en cuenta el remuestreo al calcular el tiempo | METODO-FIDELIDAD-RENTABILIDAD.md, «Lo que no pude medir (fase 1)» | :1048-1053 |
> | 2 | En §5.1 la NOTA dice que la re-corrida con su diff contra la línea base es «lo que queda de R4.1», y el cuerpo sigue llamando «línea base vigente» a CABLEADO-SIMULADOR-LINEA-BASE. D7 solo pone la NOTA en §5 | docs/runbooks/ACTIVAR-A35-A44.md §5.1 | :261-266, 281, 292 |
> | 3 | La equity, los topes y el margen libre con el sello no se midieron («no que la peor equity sea la misma»). No lo pasa a nadie por escrito, pero solo una corrida entera lo puede ver | SELLO-RESPALDO-M1.md §0.i | :345-347 |
> | — | Lo comprobé y no falta: ADR-0092 §11 (la cifra sin break even en los libros sin vídeo) entra en D5; ADR-0089:104 («después de H y R») ya se cumple; la deuda de la fila de exposición y la del calentamiento de marzo y junio (PROJECT_STATE.md:102 y :107) están en el encargo. `curva_con_deslizamiento` y `veredicto_con_f17` (PROJECT_STATE.md:101) son de F17 y no de esta rama | — | — |
>
> ### Comandos del encargo
> | # | Comando | ¿Existe y se ejecuta así? | Evidencia |
> |---|---|---|---|
> | 1 | `uv run botsito motor arnes --simular --salida docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/cuenta-por-mes.txt` | Sí | cli.py:3080-3096 y 2333-2338; arnes.py:80-82 |
> | 2 | `uv run botsito motor arnes --simular --diagnostico-cuenta-diaria --salida docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/diaria.txt` | Sí; escribe `diaria.DIAGNOSTICO.cuenta=diaria.txt` | cli.py:2321-2328, 2405-2407; diagnostico.py:169-185 |
> | 3 | La 1 con `--salida` en la carpeta de trabajo, más `diff` | Sí | cli.py:2405 (comprueba la ruta absoluta), :2473 |
> | 4 | `diff anexos/RESPALDO-M1/cuenta-arrastrada.txt anexos/RECORRIDA-CONSTRUCCION-2/cuenta-por-mes.txt > diff-linea-base.txt` | No tal como está escrito | Rutas relativas a docs/validation/, y la salida cae en el directorio actual; la fase 2 corre «desde la raíz». RESPALDO-M1 usó las rutas `docs/validation/anexos/...` completas (anexos/RESPALDO-M1/README.md:34) |
> | 5 | `diff "anexos/RESPALDO-M1/diaria.DIAGNOSTICO.cuenta=diaria.txt" "anexos/RECORRIDA-CONSTRUCCION-2/…" > diff-diaria.txt` | No tal como está escrito | El mismo problema que el 4 |
> | 6 | patrones.py sobre las dos salidas, con el sed del CRLF «como en RESPALDO-M1 §4.2» | Sí, es lo que se hizo entonces | RESPALDO-M1.md:699 (allí con `python -B`) |
> | 7 | La copia de `test_humo.py`, y correrla | No, si se copia tal cual | test_humo.py:17 importa `entradas_antes_alternancia`, que no se copia (afirmación 20) |
>
> ### Lo que no pude comprobar
> - La CI de main, run 42502468946: no consulto gh. La cifra solo está en la memoria de sesión, y eso no es evidencia.
> - Que cada día dev tenga su fichero de ticks y las horas perdidas actuales: no leo los manifiestos de data/. Me apoyo en RECORRIDA-CONSTRUCCION §0.b y en que los manifiestos no han cambiado según git log.
> - Que los 76 días salgan del reparto de vistos: no leo vistos.yaml, que nombra particiones.
> - El punto g) (la fila estadiada antes del primer make check): todavía no hay commit de apertura. HOLDOUT-EXPOSICIONES aparece estadiado en git status.
> - Si el cambio del calendario de cierres de F38p afecta a algún día dev.
> - Si anexos/CUENTA-POR-MES/rama/dos-meses-con-criterio.txt tiene ya el formato final de la salida.
> - Si la salida nueva rompe la lectura de patrones.py: no corrí nada. patrones.py solo lee filas `trader | ` / `bot | ` y las de «Por sesion» (patrones.py:60-81), y no he encontrado otras líneas con esos prefijos en cableado.py ni en criterio_fidelidad.py.
>
> ### Lo más grave
> 1. **D6 está mal y cambia las atribuciones de D3.** Dice que «enero es la cuarta cuenta», pero el arnés ordena los meses (arnes.py:121), así que enero es la primera cuenta, tanto ahora como con la arrastrada. Su camino de cuenta es el mismo que antes: todo lo que cambie en enero en diff-linea-base es del motor, nunca de la cuenta por mes. El camino de la cuenta solo explica abril, julio y agosto. Si la sesión trabaja con «enero cuarta», mezclará las dos causas justo donde están separadas.
> 2. **La copia de test_humo.py falla.** Importa `entradas_antes_alternancia`, que no se copia, y no prueba horas_perdidas. Hay que decidir si se copia también ese guion o se escribe otro test de humo.
> 3. **La lista de cambios del motor está incompleta por los dos lados.** D6 da como nuevos ADR-0086, RN-036 y RN-037, que ya estaban en la línea base anterior. D2 y D3 se dejan F38n (solo_la_contraria, que sí cambia una decisión) y la salida nueva de F38r, que aparecerá en los dos diffs sin cambiar ninguna decisión.
> 4. **Los dos diffs de D3, escritos así, no se ejecutan desde la raíz.**
> 5. **Matices menores:** el sitio de las NOTAS de D2 y D7, el §5.1 que sigue nombrando CABLEADO como línea base, y que el tiempo de D9 no cuenta con el remuestreo de 10.000 réplicas, que nunca se ha medido.
>
> Ficheros clave: `src/botsito/engine/arnes.py`, `src/botsito/engine/cableado.py`, `docs/validation/anexos/RECORRIDA-CONSTRUCCION/test_humo.py`, `docs/adr/0070-umbral-de-construccion-para-medir-mayo.md`, `docs/runbooks/ACTIVAR-A35-A44.md`, `docs/plan/HOJA-DE-RUTA.md`.

## Apéndice B · El informe del revisor (opus, 2026-11-08), tal cual

> ## Informe del revisor · trabajo/recorrida-construccion-2 · 2026-11-08
>
> Encontré cinco hallazgos de gravedad «importa», cuatro menores y ninguno que bloquee. Lo más serio está en la NOTA de ADR-0070: atribuye a RN-032 un bloqueo que la salida muestra en 96 de 104 sesiones, haya o no RN-032.
>
> Revisado contra `main` (base `ad225de`), los 5 commits y lo estadiado. La sesión hace los arreglos; yo no he tocado nada.
>
> ### Eje (a) · Reglas de la casa
> Resumen: 0 bloquea, 1 importa, 1 menor.
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | a1 | importa | **RN-032 aparece como la causa de un bloqueo que la salida no le atribuye.** La NOTA de D2 en ADR-0070 dice «RN-032 dispara en 25 de las 152 sesiones … y con él se bloquea `abrir_operacion` en 18 de esas 19». El informe dice lo mismo: §0.k punto 5 afirma que «RN-032 sale de «Por sesion», columna `bloqueadas`», y la tabla de §1.4 tiene una columna «y `prohibida:abrir_operacion`». Lo que dice la salida: la columna `bloqueadas` nunca nombra RN-032. Lo que lleva es `RN-015:accion:colocar_orden_limite:prohibida:abrir_operacion`, en el formato regla:acción:motivo que fija `bloqueadas_de`. Y eso sale en **96 de las 104** sesiones, también en las que no dispara RN-032 (por ejemplo 2026-01-02 11-15, donde el bot sí operó). El guion de la rama ya lo advierte: «el `prohibida:abrir_operacion` lo dan tambien otras reglas: no mide SOLO RN-032». Es el mismo error que señaló el a4 del revisor de RECORRIDA-CONSTRUCCION §2.2. Incumple «Nada afirma más de lo que su cita sostiene». | `docs/adr/0070-umbral-de-construccion-para-medir-mayo.md:139`; `docs/validation/RECORRIDA-CONSTRUCCION-2.md:231` y `:458-463`; `cuenta-por-mes.txt:725` (sin RN-032 en `disparadas`, con esa `bloqueadas`); `sed -n '724,828p' cuenta-por-mes.txt \| grep -o "bloqueadas.*" \| sort \| uniq -c` → `96 bloqueadas RN-015:accion:colocar_orden_limite:prohibida:abrir_operacion`, `8 bloqueadas ninguna`; `src/botsito/engine/arnes.py:260-265`; `resumen_corrida.py:13-16`. **Qué hacer:** quitar de la NOTA «y con él se bloquea `abrir_operacion` en 18 de esas 19». Puede ir con un commit nuevo, porque la NOTA aún no está en `main`, y basta con añadir líneas o cambiar solo lo que añadió esta rama. En el informe, decir que la columna cuenta coincidencias y no causas, y corregir §0.k punto 5: RN-032 sale de `disparadas`. |
> | a2 | menor | El informe no termina en su estado. Después de «## Estado» viene el «Apéndice A» del auditor, y detrás irá además este informe. CLAUDE.md dice «con su estado al final». | `RECORRIDA-CONSTRUCCION-2.md:770-776`. **Qué hacer:** mover «## Estado» detrás de los apéndices, o decir que es la forma de la casa. |
>
> **Comprobado sin hallazgos en este eje:**
> - `uv run python scripts/contrato_rama.py` → «CONTRATO: 34 ficheros dentro del contrato … 3 comprobaciones», exit 0.
> - `uv run botsito state check` → OK, exit 0.
> - `make-check.log`: el sello es del árbol `151ff208…`, que coincide con `git rev-parse 83727c3^{tree}`; «3343 passed»; «PICO DE MEMORIA … 307 MiB». Lo estadiado de la entrega todavía no tiene sello, lo que es esperado.
> - Trailers `Fuente:`: no hacen falta. Ningún commit toca `knowledge/spec` ni `knowledge/cases`; `git diff main --stat` sobre src, tests, knowledge, scripts, .claude, Makefile, tools y data/manifests sale vacío, y lo estadiado también.
> - Holdout: la rama no lo toca. No se leyó ningún libro, imagen, fotograma ni transcripción.
> - Regímenes de cambio: no hay cambios en evidence, feedback, manifests, transcripciones ni fotogramas. HISTORIA tiene +163/−0 y HOLDOUT-EXPOSICIONES +2/−0.
> - Ambigüedades: no cambia ninguna.
> - ADR-0070: solo +19/−0, y su `## Estado` no se toca. No hay ADR nuevo.
> - Informes cerrados: ninguno se modifica. RESPALDO-M1 y RECORRIDA-CONSTRUCCION no tienen diff.
> - No se añade ningún sitio con `cita`.
> - Tres citas comprobadas: `arnes.py:80-82` (la lista cerrada), `cableado.py:879-880` (la cabecera «CUENTA: UNA POR MES») y `criterio_fidelidad.yaml:61-65` (material sin vídeo). Coinciden.
> - No hay items de evidencia nuevos.
> - `ruff check` y `ruff format --check` sobre la carpeta de anexos: limpios.
>
> ### Eje (b) · Encargo
> Resumen: 0 bloquea, 4 importa, 3 menor. Requisitos: 27 hechos (2 de ellos de otra forma, declarada), 6 parciales, 0 no hechos. R33 es esta revisión.
>
> | # | Requisito | Estado | Evidencia |
> |---|---|---|---|
> | R1 | Base: main `ad225de`, tag → `41d47b3`, CI, ninguna otra rama | Hecho | informe:7-13; `git merge-base main HEAD` = ad225de… (la CI no la pude comprobar, ver abajo) |
> | R2 | Fila de exposiciones estadiada antes del primer make check y dentro del commit de apertura | Hecho | `git show --stat 5eca8e3` incluye `HOLDOUT-EXPOSICIONES.md \| 1 +`; informe:258-263 |
> | R3 | Contrato con tramo, riesgo, artefacto y rutas | Hecho | `contrato.yaml:1-26` |
> | R4 | Encargo copiado en `docs/encargos/` | Hecho | `docs/encargos/trabajo-recorrida-construccion-2.md` (no puedo comprobar que sea literal) |
> | R5 | Ningún ADR nuevo | Hecho | `git diff --name-status main...HEAD`: en docs/adr solo `M 0070` |
> | R6 | Nada de src, tests, knowledge, scripts, Makefile ni .claude (alcance 2) | Hecho | `git diff main --stat -- src tests knowledge scripts .claude Makefile tools data/manifests` vacío; `--cached` vacío |
> | R7 | Fase 0, puntos a) a h) | Hecho | informe §0.a-0.l |
> | R8 | README en su propio commit ANTES de correr | Hecho | 686a8b3 va antes que 7918f29 |
> | R9 | Copias idénticas de patrones.py y horas_perdidas.py, con el diff en el README (alcance 2) | Hecho | `git diff --no-index`: p=0, h=0; sha256 `330b7d62…` y `dfa782a3…` iguales en los dos sitios; README:96-106 |
> | R10 | test_humo copiado y corrido | Hecho de otra forma (declarado, desviación 2) | `uv run python -B -m pytest …/RECORRIDA-CONSTRUCCION-2/test_humo.py -q -p no:cacheprovider` → 13 tests en verde |
> | R11 | para_clasificar.py lee solo salidas y tiene test en los dos sentidos | Hecho | README:53-59; test_humo en verde |
> | R12 | ruff y mypy antes de cada commit | Hecho | ruff limpio al repetirlo; los avisos de mypy están declarados (informe:340-342) |
> | R13 | Tres corridas con los comandos literales y sin opciones fuera de la lista (alcance 1) | Hecho | informe:349-353. La salida no lleva rótulo `[DIAGNOSTICO`: solo aparece «DIAGNOSTICO» como marca del método en `cuenta-por-mes.txt:3512` y `:3518`. Cabecera en `cuenta-por-mes.txt:1274`: «CUENTA: UNA POR MES (ADR-0092 §8): 4 cuentas». El veredicto no dice «opción fuera de la lista» (la diaria sí) |
> | R14 | Líneas TIEMPO y MEMORIA, y el nombre final de cada fichero | Hecho | informe:351-353 |
> | R15 | Los dos diff de D3 | Hecho | `diff-linea-base.txt`, `diff-diaria.txt` |
> | R16 | patrones.py con el sed del CRLF | Hecho | `grep -c -U -P "\r"` da 0 en los patrones-*.txt |
> | R17 | D1, el veredicto literal | Hecho | `cuenta-por-mes.txt:13` igual a informe:384 y a la NOTA de ADR-0070 |
> | R18 | D2, la NOTA en ADR-0070 §3, en commit propio y después de la fase 2 (alcance 5) | Hecho, salvo el contenido de a1 | `git show --stat 83727c3`: solo ADR-0070 (+19) y el runbook (+2). `git diff main` de los dos ficheros: solo líneas añadidas, detrás del recuadro ENMENDADO |
> | R19 | D3, atribuciones con su evidencia | Parcial | ver b2 |
> | R20 | D4, patrones de las dos corridas, manda la corrida 1 | Hecho | `patrones-cuenta-por-mes.txt:3-7` y `patrones-diaria.txt:3-7` coinciden con informe:586-597 |
> | R21 | D5 | Hecho (los valores derivados están declarados) | ver comprobaciones a mano, abajo |
> | R22 | D6 | Parcial, declarado (S-10, y la sesión 6 sin separar del sello) | informe:493-503; desviación 5 |
> | R23 | D7, NOTA de una línea en §5 del runbook que declare el visor y diga lo de F38j (alcance 5) | Hecho | `ACTIVAR-A35-A44.md:246` (solo se añade) |
> | R24 | D8 | Hecho de otra forma (declarado: el escalón llega hasta la entrada) | para-clasificar.txt; desviación 3; ver b6 |
> | R25 | D9 | Hecho | 339,5 s, 331,5 s y 353,9 s; ninguna pasa de 642 MiB |
> | R26 | D10 | Hecho según el informe | informe:357-360 (la repetición se borró) |
> | R27 | D11 y D12 | Hecho | R6 |
> | R28 | Estructura del informe (§0-§7, punto por punto, desviaciones, comandos literales, exposiciones) | Parcial | ver b3 |
> | R29 | Líneas del cierre preparadas y medidas | Hecho | `simular-cierre.txt:1-7`: a, b y c vacíos; 22.837 / 22.761 bytes |
> | R30 | La Next Action y la hoja de ruta no se tocan | Hecho | HOJA-DE-RUTA no está en el diff; en PROJECT_STATE solo cambian Current Branch, Current Feature y las dos líneas «Archivo 62» |
> | R31 | Toda exposición declarada ANTES de hacerla | Parcial | ver b4 |
> | R32 | Ningún texto con fechas de días reservados ni nada anterior a su día (alcance 4) | Parcial | ver b1, b5 y b7 |
> | R33 | Revisor | esta revisión | — |
> | R34 | Las NOTAS en commit propio | Hecho | 83727c3 |
> | R35 | PROJECT_STATE: solo lo que exige abrir-rama | Hecho | `git diff main -- PROJECT_STATE.md` |
>
> **Comprobado a mano (alcance 3):**
> - **§1.1**: las cuatro filas coinciden con `cuenta-por-mes.txt:832-835`, y los totales 223 y 24 cuadran. Llenadas 88/70/53/36 = 247, contadas en «Posiciones» por mes; las 247 son de tipo `stop`.
> - **§1.2**: igual que `:3504-3508`, y 425 en `:3509`.
> - **§1.3**: igual que `:3498`, `:3502` y `:3512-3527`.
> - **§1.4**, las cuatro cuentas recalculadas desde la curva (`:1276-1394`):
>   - Equity mínima: 90.709,91, 92.778,895, 90.682,74 y 90.746,415.
>   - Peor pérdida diaria, de saldo al corte a equity mínima: 4.305,21 el 01-13, 1.798,9 el 04-09, 2.462,85 el 07-14 y 1.875,43 el 08-03.
>   - Días 21/21, 12/13 y 11/21; las rachas 7/0/3/3.
>   - Todo coincide.
> - **§1.5**: sumando las filas `:3162-3237` salen 715/66, 626/64, 420/53 y 365/57. Coincide.
> - **D8, cinco filas** contrastadas con «Ordenes» y «Posiciones»:
>   - para-clasificar:34, el 01-07: o2 a 1,1693, llenada a las 06:34:16, pareja T0.
>   - :35 y :36, el 01-08: o6 a 1,16757, rechazada; a 11 y a 1 punto.
>   - :224, o20 el 01-06: break_even, R −0,462 (`cuenta-por-mes.txt` pos-o20).
>   - :645, o9 el 08-18: break_even, R −0,400.
>   - Todo coincide.
> - **§3, tres atribuciones**:
>   - §3.2 «Ordenes»: en `diff-diaria.txt:1006-1011`, 99.538,30 pasa a 99.659,80 y el lote 24,19 a 24,22. Correcto.
>   - §3.2 «Eventos»: en `diff-diaria.txt:600-607`, 10:02:00 pasa a 10:01:59.999. Correcto.
>   - §3.1 «Ordenes»: tiene un error, ver b2.
>   - Los recuentos por sección de §3.1 y §3.2 coinciden con los `diff-*-por-seccion.txt`, incluidos 280 y 335.
>
> **Alcance 4, comprobado por mi cuenta y sin fiarme de `antes_del_dia.py`:**
> - Con `awk` sobre los 9 ficheros de salida, diff, patrones, para-clasificar y censo:
>   - Cada `nivel@minuto` frente al minuto 00:00 UTC del día de su fila: 13.507 filas, 6.102 niveles, **0 anteriores**.
>   - Cada fecha ISO frente al día de su fila: 21.014 fechas, **0 anteriores**.
>   - No hay ningún `@minuto` en una línea que no empiece por un día.
> - Los meses que aparecen en esas salidas son solo los de construcción, más 2026-05 (el rótulo del veredicto), 2025-06 a 2025-11 (rótulos de mes de la ventana de ADR-0092 §5), y 2025-12 y 2026-10 (la línea del calendario).
> - Mensajes de commit (`git log main..HEAD --format=%B`): sin fechas, salvo la del encargo (2026-11-08).
> - Líneas añadidas a ADR-0070, al runbook, a HOLDOUT-EXPOSICIONES, a PROJECT_STATE, al contrato y al encargo: solo 2026-01, 2026-01-20, 2026-05 (rótulo), 2026-08-19 y fechas de trabajo de 2026-10 y 2026-11.
> - Límites del guion: solo mira los 16 ficheros de la carpeta. No mira los `.py`, ni el informe, ni las NOTAS, ni los commits. Se salta enteras las líneas del calendario y de la cabecera de rentabilidad. Por eso no vio b1.
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | b1 | importa | **Hay fechas de meses con días reservados en un fichero commiteado, sin declarar.** Las fixtures sintéticas de `test_humo.py` usan dos fechas de marzo (mes reservado entero) y una de mayo. No llevan ningún dato del mercado, pero el encargo dice «Ningún texto commiteado lleva fechas de días reservados». | `test_humo.py:268`, `:276`, `:278-280`; `git log -S "<la fecha de mayo>" main..HEAD -- …/test_humo.py` → 7918f29. **Qué hacer:** en un commit nuevo, cambiar las fixtures. Para «anterior al día» basta una fila del 2026-04-02 con un instante del 2026-04-01; para «fuera de la construcción», un mes sintético de 2030. Ampliar `antes_del_dia.py` a los `.py` y al informe, y declararlo en las desviaciones. La historia no se reescribe. |
> | b2 | importa | **La evidencia de la atribución «comisión» de §3.1 tiene mal las cuentas.** El informe dice que la comisión es 121,50 + 67,30 = 188,80 y que «los 0,11 restantes [son] del lote (24,31 → 24,30)». No es así. o7 tiene 24,30 lotes en las dos salidas, y 24,31 es el lote de o1, que se canceló en las dos. El lote que cambia es el de o9, de 13,45 a 13,46. Por tanto, el ahorro de comisión es (24,30 + 13,45) × 5 = 188,70 (con 5 USD la comisión era 377,50, no el doble exacto de 188,80). Los +0,21 que faltan vienen del lote mayor de o9 en una ganancia de 21 puntos. 188,70 + 0,21 = 188,91. La atribución a la comisión se mantiene; lo que está mal son las cifras de la evidencia. | informe:556; `RESPALDO-M1/cuenta-arrastrada.txt:919` y `:921` (o7 24,30; o9 13,45; margen 99.538,30 = 100.000 − 218,70 − 243,00); `cuenta-por-mes.txt:2005` y `:3251-3252` (o9 13,46). **Qué hacer:** corregir la frase. |
> | b3 | importa | **Los comandos del informe no son literales.** El encargo pide «comandos literales ejecutados». Las filas 6 a 11 de la fase 2 llevan `<cada salida>`, `<salida>`, `…/` y `<los 16 ficheros>`. Los guiones de la fase 0 (`recuentos_fase0.py`, `volcar_dos_meses.py`, `combinar.py`, `default_ambiguous.py`) se corrieron desde la carpeta de trabajo y no tienen comando ni código en el repo. | informe:368-373, :88, :150-152, :288. **Qué hacer:** escribir cada comando tal cual se ejecutó. Para los guiones de la fase 0, decir que no se commitearon y qué leyó cada uno. |
> | b4 | importa | **Hay exposiciones declaradas después de hacerlas.** La segunda fila de la rama dice «Ya corrido cuando se escribe», contra el «ANTES de hacerla» del encargo (lo declara la desviación 6). Además, `simular_cierre.py`, que está estadiado y ya corrido, no está declarado en ninguna de las dos filas de la rama. No leen material reservado. | `HOLDOUT-EXPOSICIONES.md`, las dos filas añadidas; `grep "recorrida-construccion-2" … \| grep -c simular_cierre` → 0. **Qué hacer:** declarar `simular_cierre.py` hoy mismo, antes del make check de la entrega. |
> | b5 | menor | **La desviación 9 se queda corta.** Dice que el id `fb-` con fecha de septiembre está en el commit `46e69c5`. Está en **cuatro** versiones commiteadas del informe: `46e69c5`, `686a8b3`, `7918f29` y `83727c3`. Solo lo estadiado lo quita. Y «lo vio `antes_del_dia.py` sobre el informe» no se ve en `antes-del-dia.txt`, que no incluye el informe. | `git show <c>:docs/validation/RECORRIDA-CONSTRUCCION-2.md \| grep -c -E "fb-[^ ]*20[0-9]{2}-?09"` da 1 en cada uno de los cuatro; en el árbol de trabajo, 0; `antes-del-dia.txt:1-16`. **Qué hacer:** nombrar los cuatro commits. |
> | b6 | menor | D8 pide «si pasó por break even» y la lista da una columna «stop movido» sin decir si es lo mismo. | `para-clasificar.txt:220`; informe:629. **Qué hacer:** decirlo en una línea. |
> | b7 | menor | §3.1 cita literalmente la línea `calendario: cubre …` del calendario, con una fecha de diciembre. Ya estaba en `main`: está en `RESPALDO-M1.md` y en `RESPALDO-M1/cuenta-arrastrada.txt`, y `antes_del_dia.py` la exime a propósito. | informe:559; `grep -c "calendario: cubre"` da 1 en las dos salidas. **Qué hacer:** quitar la fecha del informe o decir por qué se queda. |
>
> ### Lo que no pude comprobar
> - **La CI de `main` (run 42502468946)**: no ejecuto `gh`.
> - **D10, el determinismo**: la repetición se borró. Solo tengo el sha256 que da el informe.
> - **El sello de lo estadiado de la entrega**: `make check` escribe y no lo corro. El log que hay sella el árbol de `83727c3`.
> - **Las horas de §0.g y los make check de los commits anteriores**: solo queda el último log.
> - **Que el encargo esté copiado literalmente**: no tengo el mensaje original.
> - **Los guiones de la carpeta de trabajo de la fase 0**: no están en el repo.
> - **`casos_reservados` y `casos_ocultos`**: no los recalculé, porque leen la partición.
> - **Si la fecha del id `fb-` o el inicio del calendario son días reservados**: no se puede saber sin mirar el holdout.
> - **El test original de `anexos/RECORRIDA-CONSTRUCCION/test_humo.py`**: no lo corrí.
>
> ### Comandos ejecutados
> 1. `git branch --show-current; git merge-base main HEAD; git log --format='%h %s' main..HEAD; git diff --stat main...HEAD; git status --short; git diff --cached --stat`
> 2. El mismo comando con `-- … corpus data` lo negó la guardia; lo repetí sin esas rutas.
> 3. `git diff main --stat -- src tests knowledge scripts .claude Makefile tools data/manifests; git diff --cached --stat -- …; git diff --name-status main...HEAD`
> 4. `git diff --no-index --stat` de patrones.py y horas_perdidas.py (origen y copia); `sha256sum` de los cuatro
> 5. `uv run python scripts/contrato_rama.py`; `uv run botsito state check`
> 6. `ls -la make-check.log; grep -n "SELLO\|PICO DE MEMORIA\|passed\|failed" make-check.log`
> 7. Read del encargo, `contrato.yaml`, el informe, `antes_del_dia.py`, `antes-del-dia.txt`, el README, `simular-cierre.txt`, `simular_cierre.py`, `para-clasificar.txt` y los tramos de `cuenta-por-mes.txt` y `diff-diaria.txt` citados arriba
> 8. `grep` de fechas en el informe, los anexos, los `.py` y las líneas añadidas a los documentos; `git log --format='=== %h%n%B' main..HEAD`
> 9. `git show <commit>:…RECORRIDA-CONSTRUCCION-2.md | grep -c` del id `fb-` con fecha de septiembre (un `for` lo negó la guardia; lo hice commit a commit)
> 10. `git diff main --` de ADR-0070, ACTIVAR-A35-A44, HOLDOUT-EXPOSICIONES y PROJECT_STATE; `git diff --numstat`; `git diff --cached -U0` del informe
> 11. `sed -n | awk | cut | grep | sort | uniq -c` sobre `cuenta-por-mes.txt` (peticiones, Posiciones, Por sesion, Ordenes) y `RESPALDO-M1/cuenta-arrastrada.txt` (2026-01-02)
> 12. `grep` sobre `censo-cierre-cuenta-por-mes.txt` y `SELLO-RESPALDO-M1.md` (los once días)
> 13. `awk` del alcance 4 (`nivel@minuto` y fechas ISO frente al día de su fila). La forma con `TZ=` la negó la guardia; la repetí con aritmética de días.
> 14. `uv run python -B -m pytest docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/test_humo.py -q -p no:cacheprovider` → 13 en verde (el `__pycache__` que hay es de antes e ignorado por git; `git status` sin cambios)
> 15. `uv run ruff check --no-cache …/RECORRIDA-CONSTRUCCION-2/`; `uv run ruff format --check --no-cache …`
> 16. `git rev-parse 83727c3^{tree} 5eca8e3^{tree} 7918f29^{tree}`; `git show --stat` de 5eca8e3, 7918f29 y 83727c3
> 17. `grep -c -U -P "\r"` sobre siete ficheros de anexos
> 18. `sed -n` de `arnes.py:80-82`, `:119-122`, `cableado.py:877-881` y `criterio_fidelidad.yaml:61-65`; Read de `arnes.py:250-294`

(Pegado tal cual salvo en tres sitios, para no repetir en el informe las fechas que b1 y b7 piden
quitar: en b1, las tres fechas de las fixtures (dos de marzo y una de mayo) quedan en «dos fechas
de marzo (…) y una de mayo», y su `git log -S` en «<la fecha de mayo>»; en b7 y en «Lo que no pude
comprobar», la fecha de inicio del calendario queda en «`calendario: cubre …`» y «el inicio del
calendario».)

## Lo hecho con cada hallazgo del revisor

| # | Lo hecho |
|---|---|
| a1 | La NOTA de ADR-0070 §3 pierde «y con él se bloquea `abrir_operacion` en 18 de esas 19» (la NOTA es de esta rama: se cambia solo lo que añadió); §0.k punto 5 corregido con recuadro en cursiva («columna `disparadas`»); la tabla de §1.4 dice que su cuarta columna cuenta coincidencias de RN-015, no causas. |
| a2 | «## Estado» pasa al final, detrás de los apéndices. |
| b1 | Las fixtures de `test_humo.py` pasan a 2026-04-02 con instantes del 2026-04-01 y a una fecha sintética de 2030; 13 en verde. `antes_del_dia.py` corrido también sobre los `.py`, `simular-cierre.txt` y el informe (fase 2, punto 11). La historia no se reescribe: las fechas quedan en `7918f29` y `83727c3`, declarado aquí. |
| b2 | §3.1 corregido: (24,30 + 13,45) × 10 = 377,50 frente a 188,80; 188,70 de ahorro y 0,21 del lote de o9 (comprobado en las dos salidas). |
| b3 | Los comandos de la fase 2, tal cual (con dos abreviaturas de ruta declaradas); los guiones de la fase 0, dichos: no se commitearon, y qué leyó cada uno. |
| b4 | Fila nueva en HOLDOUT-EXPOSICIONES (el mismo día, antes del `make check` de la entrega): `simular_cierre.py`, la pasada ampliada de `antes_del_dia.py` y el test de humo. Sigue declarado que se escribió después de correrlos. |
| b5 | La desviación 9 nombra los cuatro commits y dice que la pasada que lo vio no está en `antes-del-dia.txt`. |
| b6 | §5 dice cómo se leen «stop movido» y «desenlace» para «si pasó por break even», y que el primero no prueba el nivel. |
| b7 | La línea del calendario ya no se copia en §3.1. |
| Lo que no pudo comprobar | La CI: `gh run view 42502468946` en la apertura (`success`). D10: el `sha256` igual de las dos, en la fase 2. El sello de la entrega: abajo, «Los make check de la rama». |

## Respuesta del consultor a la PARADA 2 (2026-11-08)

Copiada tal cual:

> Modelo: Opus 5.5 · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA 2 de trabajo/recorrida-construccion-2 (2026-11-08). Cópiala tal cual al final del encargo y del informe, en «Respuesta del consultor a la PARADA 2», con su fecha, y aplícala punto por punto (skill fase-cero). Abre una fase 3 en esta misma rama: la clasificación tiene que estar hecha antes de preparar la sesión 7 (hoja de ruta, el muro), así que no se deja para la rama de la preparación. NUNCA cierra.
>
> ANTES DE NADA
> - La fila del día en HOLDOUT-EXPOSICIONES.md, escrita y estadiada ANTES del primer make check, de la primera lectura de casos dev y del primer visor de esta fase (lección 8 de F38r): casos_reservados(repo) por recuento, y que ninguno de los días que se leen aparece en él (su ausencia dice «no reservado», que es lo que hace falta; no dice «sin partición»); los casos dev de construcción de los cuatro meses (el stop del trader); los nueve visores del punto 3 y lo que calientan (el M1 entero de marzo para los días de abril y de junio para los de julio, por recuento; enero, desde su propio mes); los guiones nuevos de anexos y el revisor. Si el trabajo pasa la medianoche, el día nuevo tiene su fila antes de su primer make check.
> - Se amplía la autorización expresa del encargo SOLO a los nueve comandos del visor del punto 3, escritos exactamente así. Ningún motor arnes más.
>
> 1. LA CLASIFICACIÓN PROVISIONAL POR PATRONES (decisión del consultor, 2026-11-08). Va al informe en un §8 nuevo, «La clasificación», como tabla con una fila por patrón: filas, clase, evidencia y destino. La fase 3 la completa con las medidas de los puntos 2 y 3, aplicando las reglas que aquí se fijan antes de medir; no se cambia ninguna clase por tu cuenta.
>    a) T0 (31): pareja. Nada.
>    b) P4 (25): 22 son de agosto, desde el 2026-08-19, cuando la cuenta de agosto deja de llenar con la equity cerca del 90 % (§1.4); en la diaria, agosto da 3. Clase «efecto de la cuenta»: ni error del motor ni regla desconocida, sale cuando bajen las pérdidas del bot. Di qué gate prohíbe abrir desde ese día, si la salida lo trae (por su definición debería ser RN-032: la pérdida total más el riesgo de la operación llega al límite menos el margen, strategy_spec.yaml); la línea `RN-015:accion:colocar_orden_limite:prohibida:abrir_operacion` es la acción de RN-015 que un gate bloquea, no una prohibición de RN-015, y no nombra el gate. Si la salida no lo trae, escribe «la cuenta de agosto deja de llenar» sin regla. Las 3 restantes (una en enero, abril y julio): sin clase, en la lista del punto 4.
>    c) P7 (4): el trader vuelve a entrar en la misma zona y el bot no. patrones.py no comprueba que la operación del bot esté ya emparejada (lo infiere: _ops_bot mezcla emparejadas y sueltas, y el docstring no dice lo que hace el código); compruébalo en las 4 filas contra «Por operacion». Clase «error nuestro conocido»: la deuda de RN-019 de Technical Debt (no dispara nunca en el motor; la acción reentrar no está escrita, PUNTO-USADO.md §1.h). Verifica en la salida que en esas 4 sesiones el bot no tenía una reentrada que RN-016 negara; si alguna la tenía, o la operación del bot no estaba emparejada, dilo y pasa a sin clase. Destino: la rama de RN-019, que no es esta.
>    d) La caja: las 44 operaciones con la entrada a 3 puntos o menos y el stop fuera, y las 24 de P2 con la entrada a 4-10 puntos. Clase según la regla del punto 2.
>    e) P1 (44, en 21 sesiones; 42 con el sesgo del bot al contrario y 2 insuficiente), P3 (54; 42 a más de 20 puntos), las 16 de P2 a más de 10 puntos, P5 (153; 120 del mismo lado) y P6 (63): sin clase hasta el punto 3 y, en julio, hasta T (punto 5). Nota que no clasifica: 20 de las 44 P1 son de julio, el único mes con vídeo, y P6 se concentra en abril (33), mes sin vídeo, donde S-14 dice que el trader se saltaba en sus backtests las sesiones que iban a acabar en break even (ACTIVAR-SESION-05.md §0.b.7); eso se mide, no se supone (punto 3).
>
> 2. LA CAJA: EL STOP DEL TRADER DE LOS CASOS DEV (decisión 0 de tu PARADA: opción b, aquí y no en la preparación de la sesión 7). Un guion de anexos (caja_stop.py, con su test de humo que rompa en los dos sentidos) que lee el stop de cada operación del trader de los casos dev de construcción (comprobado antes con casos_reservados y declarado) y, para las 64 operaciones con la entrada dentro en la corrida 1 y las 40 de P2, escribe por operación: entrada y stop del trader, entrada y stop de la orden del bot que ya nombra para-clasificar.txt (de «Ordenes» y «Posiciones»), Δentrada y Δstop con signo (positivo = el del bot más lejos de la entrada que el del trader, en la dirección de la operación), y el cociente entre la distancia entrada-stop del bot y la del trader. Además, de las 6 «en el nivel, no llenada», el motivo literal de la salida (cancelada por qué regla, o caducada). Salida a anexos/RECORRIDA-CONSTRUCCION-2/caja-stop.txt, con su resumen: la distribución de Δstop y del cociente, y cuántas tienen cada signo.
>    Regla, fijada antes de medir: si al menos dos tercios de las 44 con el stop fuera tienen el mismo signo de Δstop, la diferencia es SISTEMÁTICA y la clase es «la caja: regla desconocida», con A-48 (qué velas forman el bloque de la caja, y el 0, S-16, punto 5 de «Para la sesión 7»): entra en la hoja de la sesión 7 con un esquema inventado. Con menos de dos tercios es DISPERSA: sin clase, y dos de ellas van al visor como ejemplo en la rama de la preparación. Lo mismo, con la misma regla y por separado, para el signo de Δentrada de las 24 de P2 a 4-10 puntos. Antes de dar la clase, mira si el redondeo del stop (alejándose de la entrada, al punto) o la comisión explican la diferencia; si la explican, la clase es «error nuestro» y PARADA 3 con la evidencia.
>
> 3. EL VISOR, NUEVE SESIONES (decisión 1: opción b; S-10 se mide aquí). Elegidas por el consultor entre las que más filas tienen de cada patrón, fuera del 1 de abril y del 1 de julio y sin «posible M». Una vez cada comando, la salida a data/visor/ (ignorada por git; nada del visor se commitea):
>    uv run botsito motor visor --simular --caso caso-eurusd-2026-07-06
>    uv run botsito motor visor --simular --caso caso-eurusd-2026-07-07
>    uv run botsito motor visor --simular --caso caso-eurusd-2026-07-15
>    uv run botsito motor visor --simular --caso caso-eurusd-2026-01-22
>    uv run botsito motor visor --simular --caso caso-eurusd-2026-07-02
>    uv run botsito motor visor --simular --caso caso-eurusd-2026-04-13
>    uv run botsito motor visor --simular --caso caso-eurusd-2026-01-13
>    uv run botsito motor visor --simular --caso caso-eurusd-2026-04-15
>    uv run botsito motor visor --simular --caso caso-eurusd-2026-07-14
>    Las sesiones y su porqué: P1, 2026-07-06 07-11, 2026-07-07 07-11 y 11-15, 2026-07-15 11-15 y 2026-01-22 11-15; P3, 2026-07-02 11-15 y 2026-04-13 07-11; P5, 2026-01-13 07-11; P6, 2026-04-15 11-15; la caja (P2), 2026-07-14 11-15.
>    a) Primero, por sesión: si las órdenes del visor son las de la corrida 1 en esa sesión (ids, instantes, entradas, stops). Si alguna no coincide (el visor con un solo caso empieza la cuenta desde el capital y la corrida 1 la trae del mes), dilo con la diferencia y usa la corrida 1 como verdad.
>    b) P1: el sesgo del bot, de qué H4 sale (por su hora de cierre y su color, sin precios; si es de un día anterior, dilo así), y el paso de RN-003 y de domain/sesgo.py que lo decide, con ADR-0080 si salta una H4 por el color.
>    c) P3, P5 y P6: cada escenario de la sesión (ADR-0066 §1 y §2: una toma nueva abre escenario cuando el vigente terminó; con el vigente vivo decide intentos_tras_toma_nueva; tope max_escenarios_por_sesion), de qué toma de M15 sale, sus puntos y zonas, qué orden coloca cada uno y, si el trader entró en un nivel que el bot formó y no usó, qué regla lo descartó (el breaker de S-22, la alternancia RN-009, A-53 con se_mueve, RN-016). En la de P6 de abril, si la sesión acaba en break even para el bot (S-14).
>    d) S-10 (ADR-0085 §4): en las nueve sesiones, si cada orden del bot nace en el primer punto tras la toma o en otro.
>    e) Cada caso, marcado «regla aplicada como está escrita» o «no», con su evidencia (regla, fichero:línea, instante). Si alguno es «no» (el motor no aplica la spec como dice), PARADA 3 en eso antes del revisor y sigue con lo demás. Si todos son «sí», sigue sin parar.
>    Ninguna línea del informe imprime una vela, un precio, un nivel ni un instante anteriores al día dev del caso.
>
> 4. LA TABLA DE §8, COMPLETA. Con 2 y 3 aplicados, cada patrón queda en una de estas clases: «error nuestro» (el motor no aplica la spec, o la spec lee mal lo que el trader dijo y está citado), «regla desconocida» (el motor aplica la spec y el trader hizo otra cosa: pregunta para la sesión 7, que redacto yo), «efecto de la cuenta», «material» (S-14 y días sin vídeo) o «sin clase hasta T». Para cada fila, el destino: una rama nombrada, la hoja de la sesión 7, T o ninguno. Una lista aparte con las filas sin clase que no cubre ni el visor ni T. Sin cambiar nada de lo decidido en el punto 1.
>
> 5. EL ORDEN DE LO QUE SIGUE (decisión del consultor). T (trabajo/video-julio, ENTRADA-JULIO.md §5) pasa por delante de la preparación de la sesión 7: julio es el mes con más operaciones del trader (67), el único con vídeo, y en él están 20 de las 44 P1 y cinco de las nueve sesiones del visor; su voz explica cada entrada y cada descarte, y lo que aclare no gasta tiempo de la sesión. Va en las líneas del cierre (punto 6).
>
> 6. LAS LÍNEAS DEL CIERRE, rehechas y medidas sobre una copia (no las apliques):
>    - Next Action, F, con este texto exacto y la cifra literal del veredicto: «F. Sesión 6 ACTIVADA en spec (F38n) y motor (F38o); S-22 y S-19 a la sesión 7 (§d de ACTIVAR-SESION-06-MOTOR.md). La re-corrida que cuenta está hecha (RECORRIDA-CONSTRUCCION-2.md: «no», cobertura 15.7 % y precisión 13.9 %; línea base anexos/RECORRIDA-CONSTRUCCION-2/cuenta-por-mes.txt; la clasificación, en su §8). Siguiente: T, con la voz del trader sobre julio; después, la preparación de la sesión 7 (hoja + gráficos 2 a 6 con contexto; ACTIVAR-SESION-06.md §«Para la sesión 7», S-22 y S-19 con sus esquemas y el 52 %, y lo que deje §8); J antes si la hoja sale de kit hoja. El vídeo de mapeo, si llega, SIN ABRIR y fuera del repo. R6a en los huecos.» Ninguna letra sale ni entra.
>    - Hoja de ruta: R3.9 como la preparaste, con «Hecho cuando: el veredicto literal está en el informe y en ADR-0070 §3, la línea base vigente es la suya y cada diferencia tiene su clase o su destino (§8)» y el Estado HECHA con el veredicto y el recuento de §8 por clase. R5.2 cita R3.9 en lugar de R4.1. R5.6 sin cambio. En la entrada de T, una línea: «Va antes de la preparación de la sesión 7 (RECORRIDA-CONSTRUCCION-2.md §8, respuesta a la PARADA 2)».
>    - Technical Debt: nada, salvo lo que la PARADA 3 decida.
>    - PROJECT_STATE con las líneas aplicadas y las cuatro cabeceras en forma corta (decisión 3: opción a): por debajo de 23.000 bytes, medido con wc -c sobre una copia, con test_hoja_de_ruta y test_project_state en verde. Si pasa de 23.000, PARADA con la cifra; no recortes nada por tu cuenta.
>
> 7. LAS OTRAS DOS DECISIONES DE TU PARADA. La 2: opción a, no hay NOTA en §5.1 de ACTIVAR-A35-A44.md; la de §5 basta (D7). La 3: opción a, la forma corta.
>
> 8. LA DESVIACIÓN 9 (el id con la fecha de la sesión 3 en cuatro commits): de acuerdo, no se reescribe la historia. Es la fecha de la sesión grabada, no un día de mercado ni una cifra del bot, y el mismo id está en knowledge/spec/parametros.yaml de main. Queda declarada como está.
>
> 9. LA FILA DE ERRORES-RECURRENTES. A tus lecciones de §7 añade, en «del consultor», estos tres, todos menores, con su lección:
>    (a) D6 dijo que enero era la cuarta cuenta: el orden de los meses lo pone arnes.validar_meses, que los ordena, y lo leí en el encargo de F38s sin aplicarlo. Lección: el orden de un recorrido se lee en el código que lo fija, no en el yaml que lo lista.
>    (b) D8 pidió el escalón entero de la cascada por operación sin comprobar que la salida trae el stop del trader. Lección: antes de pedir una tabla por operación desde una salida, se comprueba que la salida trae cada campo.
>    (c) D6 pidió S-10 desde la salida, y la salida no trae la toma ni las zonas. La misma lección que (b).
>    Y uno para el revisor (menor): su a1 dejó escrito en §1.4 que `prohibida:abrir_operacion` «es siempre de RN-015»; es la acción de RN-015 bloqueada por un gate, y la línea no nombra cuál. Corrige §1.4 con esa frase (la NOTA de ADR-0070, si dice lo mismo, también, en su commit). Lección para el revisor: al corregir una atribución, se lee la regla en strategy_spec.yaml antes de escribir la nueva.
>    Y lo que el revisor no vio, si tu revisión del punto 10 encuentra algo.
>
> 10. EL REVISOR (opus), sobre la fase 3, con estos alcances: (1) que caja-stop.txt dice lo que dicen los casos dev y las salidas, comprobado a mano en cinco operaciones (dos con el stop fuera de cada signo y una no llenada), y que la regla de dos tercios se aplicó tal como está escrita; (2) que en las nueve sesiones las órdenes del visor coinciden con las de la corrida 1, o la diferencia está dicha; (3) que cada «regla aplicada como está escrita» tiene su evidencia, comprobada en tres casos; (4) que §8 no cambia ninguna clase del punto 1 y que cada fila tiene destino; (5) que ningún texto commiteado lleva algo anterior al día dev del caso ni fechas de días reservados; (6) que nada de src/, tests/, knowledge/, scripts/ ni .claude/ cambia. Su informe, pegado al final; arregla lo que bloquee o importe, o di por qué no.
>
> PARADA 3 · ENTREGA: commitea la respuesta, los guiones con su test, caja-stop.txt, §8, el informe y el revisor, y para. Con eso escribo la orden de cierre y, en el encargo de la preparación de la sesión 7, las preguntas que salgan de §8.
>
> make check en verde antes de cada commit, con ruff format, ruff check y mypy antes sobre lo tocado. Si la guardia o el clasificador niegan algo, PARADA con el comando exacto y lo lanza Aleks con «!».
>
> Rama lista para revisión, NO cerrada.

## Fase 3 · la respuesta del consultor a la PARADA 2, aplicada punto por punto (2026-11-08)

**Antes de nada.** La fila del día en HOLDOUT-EXPOSICIONES, escrita y estadiada a las 17:49:09, antes
de cualquier lectura de casos dev, visor o `make check` de la fase. Con un guion de la carpeta de
trabajo, que solo imprime recuentos: `casos_reservados` da 34 y `casos_ocultos` 34. De los 76 días
dev de construcción hay **0** en cada uno, y de los nueve del visor (los nueve son dev de
construcción), también **0**. Su ausencia dice «no reservado», no «sin partición». Una segunda fila
nombra lo que la primera cubría solo en general (`visor_sesiones.py`, `recuento_clases.py`,
`salida_comun.py` y la lectura de spec y código); se escribió después de correrlos, el mismo día y
antes del primer `make check` de la fase.

### F3.1 · P4 (punto 1.b)

- **Desde el 2026-08-19 las P4 son 19, no 22.** Las 22 de agosto incluyen 3 anteriores al 19: dos
  del 2026-08-10, sesión 11-15, con `detenido_por_racha`, y una del 2026-08-14, sesión 07-11, sin
  `orden_dimensionada` (`recuento-clases.txt`; las filas, en `patrones-cuenta-por-mes.txt`). Gana la
  medida: las 19 desde el 19 van a «efecto de la cuenta», como decidió el consultor, y las 3
  anteriores, a la lista sin clase.
- **El gate.** La salida lleva RN-032 entre las `disparadas` de las **14 sesiones con trader** del
  2026-08-19 al 2026-08-31 (14 de 14), con `bot 0` en las 14. En 13 de ellas, la línea `bloqueadas`
  es `RN-015:accion:colocar_orden_limite:prohibida:abrir_operacion`, que no nombra el gate; en la
  otra, `ninguna`. Escrito así: **la cuenta de agosto deja de llenar desde el 2026-08-19; RN-032
  dispara en cada una de sus 14 sesiones con trader («disparadas») y la línea de bloqueadas no dice
  qué gate prohíbe abrir**. Por su definición (`strategy_spec.yaml:2536-2544`: «la perdida acumulada
  de la firma … mas el riesgo de la operacion … llega al limite menos firma_margen_seguridad … no se
  abre esa operacion»), es el candidato. La salida no lo prueba.
- Las otras 3: una de enero (2026-01-08 11-15), una de abril (2026-04-21 07-11) y una de julio
  (2026-07-08 11-15). Sin clase, a la lista.

### F3.2 · P7 (punto 1.c)

Las 4 filas, comprobadas contra «Por operacion»: la operación del bot más cercana de cada una **es
la pareja de OTRA operación del trader** (fila T0 `PAREJA bot <instante> <entrada>`) y no sale como
fila del bot suelta. Son: 2026-07-10 07-11 (la del bot de las 07:14:10, pareja de la del trader de
las 07:10:50), 2026-07-10 11-15, dos filas (la del bot de las 10:58:43, pareja de la de las
10:58:40), y 2026-01-02 11-15 (la del bot de las 13:28:06, pareja de la de las 13:28:15). Horas UTC
de la salida. En las tres sesiones, RN-016 no está entre las `disparadas` y
`detenido_por_cartuchos` es `no`: el bot no tenía ninguna reentrada que RN-016 negara. **Clase
«error nuestro conocido»** (la deuda de RN-019 de Technical Debt, PUNTO-USADO.md §1.h), como decidió
el consultor. Destino: la rama de RN-019.

### F3.3 · La caja (punto 2): `caja_stop.py` → `caja-stop.txt`

El stop del trader sale de los casos dev, por la compuerta del arnés
(`arnes.dias_de_construccion`). La orden del bot es la de `para-clasificar.txt` (sus «Ordenes»: precio
y distancia; el stop, desde los dos). Los signos van en el docstring: Δ > 0 cuando la cifra del bot
está más allá de la del trader, del lado del stop. Para Δentrada uso la misma orientación, porque la
frase del consultor no la fija para la entrada; la regla de los dos tercios solo mira si los signos
coinciden, así que la orientación no cambia la clase.

- **Las 64 con la entrada dentro**, comprobadas contra la cascada impresa: 44 con el stop fuera, 6
  en el nivel no llenadas y 14 con las cuatro piezas. Las tres cifras coinciden con
  «### Fidelidad por criterios».
- **Las 44 con el stop fuera: Δstop > 0 en 18 y < 0 en 26** (59 %, por debajo de dos tercios): **DISPERSA**.
  Δstop va de −26 a +35 puntos (mediana −5); el cociente de distancias, de 0,21 a 9,25 (mediana 0,83).
- **Antes de la clase.** El redondeo del stop al punto mueve 1 punto como mucho, así que solo podría
  explicar las que están a 4 puntos exactos: son **7 de 44** (4 con +4 y 3 con −4). Quitando las 7,
  quedan 14 frente a 23 de 37 (62,2 %); quitando solo las 4 positivas, las únicas que el redondeo
  «alejándose de la entrada» puede dar, quedan 14 frente a 26 de 40 (65,0 %), a 1,7 puntos del
  umbral. Dispersa en las dos cuentas. *Corregido tras el revisor de la fase 3 (a1): la primera
  redacción decía que 26 de 37 no llegaba a dos tercios, y llega (70,3 %).* La comisión no mueve
  ningún precio. **No explican la diferencia: ni «error nuestro» ni PARADA por esto.**
- **La medida del signo** (revisor, b3): stop contra stop, «del lado del stop», no la diferencia de
  distancias que dice la frase del consultor. En las 44 dan el mismo signo, porque la diferencia de
  distancias es Δstop − Δentrada, con |Δentrada| ≤ 3 < 4 ≤ |Δstop|.
- **El cruce con los patrones** (revisor, b4): de las 44, 20 son T0, 11 P3, 11 P2 y 2 P7 (medido con
  un guion de la carpeta de trabajo sobre `caja-stop.txt` y las filas de los patrones). Una misma
  operación lleva su clase de patrón en §8 y, aparte, la de la caja.
- **Las 40 P2**: 24 a 4-10 puntos y 16 a más de 10, las del consultor. En las 24: **Δentrada > 0 en 10
  y < 0 en 14** (58 %): **DISPERSA**. Por mes, las 24 son 8 de enero, 5 de abril, 7 de julio y 4 de
  agosto; las 16 de más de 10, 9 de enero y 7 de julio.
- **Las 6 no llenadas**: canceladas las seis, `reglas disparadas en ese cierre: …`. Las reglas de cada
  una van en su fila de `caja-stop.txt`: RN-006, RN-011, RN-015 y RN-027 en las seis, y RN-004 o
  RN-005 en cuatro de ellas.
- Las dos, **sin clase**; dos de cada grupo van al visor como ejemplo en la rama de la preparación
  (regla del punto 2).

### F3.4 · El visor, nueve sesiones (punto 3): `visor_sesiones.py` → `visor-sesiones.txt`

Los nueve comandos del punto 3, tal cual, una vez cada uno: `exit=0` los nueve, entre 2,2 y 8,6 s;
la salida, en `data/visor/`, ignorada por git. Las horas del visor son de pared (Europe/Madrid).

**Lo que el visor NO muestra, medido** (va a la PARADA 3): no nombra las tomas de M15 (RN-004 fija
`liquidez_tomada=si` en cada cierre, sin nivel) ni los escenarios. De los gates, solo los frenos:
cuando salta uno, la tabla de hechos lo dice minuto a minuto (`RN-016 | detenido_por_cartuchos |
hasta_cartuchos_reinicio`). Cuando la prohibición de abrir no viene de un freno, solo se ve
`RN-015 | orden_dimensionada | no` y no qué regla la fija. En la tabla de hechos y en los títulos del
gráfico de 04-13 solo salen RN-003, RN-004 (155), RN-011 (345) y RN-015 (345). Por eso (c) y (e) solo
se pueden hacer en parte, y (d) suponiendo una toma por sesión (la primera).

**(a) Las órdenes del visor frente a las de la corrida 1**: iguales en id, colocación, precio, stop y
estado en ocho de los nueve días. **2026-07-15: el visor tiene 5 más** (o25 a o29), porque en la
corrida 1 la sesión 11-15 acaba en `detenido_por_racha:si` (RN-036 entre las disparadas), tras la
pérdida de o24, con la racha que arrastra la cuenta de julio. El visor empieza el día desde el
capital, sin esa racha, y sigue. Como dice el punto 3.a, manda la corrida 1.

**(b) P1, el sesgo** (el lado que anota `domain/sesgo.py` y el color de la H4 que decide en el gráfico,
el rectángulo marcado «rompe esta H4», sin precios):

| Sesión | Sesgo del bot | H4 que decide | Color | Paso de `sesgo.py` (RN-003, `strategy_spec.yaml:1079`) | Trader |
|---|---|---|---|---|---|
| 2026-07-06 07-11 | bajista, 46 puntos | la que abre a las 03:00 del día, contra la anterior, que es de un día anterior | baja | ruptura de un extremo con su color, `sesgo.py:124-127` | 4 compras |
| 2026-07-07 07-11 | bajista, 25 puntos | la de las 03:00 del día, contra la anterior, de un día anterior | baja | `sesgo.py:124-127` | 4 compras |
| 2026-07-07 11-15 | bajista, 106 puntos | la de las 07:00, contra la de las 03:00 (las dos del día) | baja | `sesgo.py:124-127` | 4 compras |
| 2026-07-15 11-15 | bajista, 126 puntos, doble ruptura | la de las 07:00, contra la de las 03:00 | baja | doble ruptura, decide el color, `sesgo.py:110-115` (ADR-0060) | 4 compras |
| 2026-01-22 11-15 | alcista, **2 puntos** | la de las 07:00, contra la de las 03:00 | sube | `sesgo.py:124-127` | 3 ventas |

En las cinco, `1 H4 miradas`: ninguna H4 saltada por color (ADR-0080 D1 no actúa). El bot solo forma
zonas del lado de su sesgo: en las cinco sesiones, «ninguna zona del bot de su lado formada antes»
para cada operación del trader. Las tres sesiones de julio con trader en 07-11 o 11-15 tampoco tienen
órdenes del bot del lado del trader. **Regla aplicada como está escrita: sí** en las cinco, con esta
evidencia: el lado anotado es el del color de la H4 que decide, como piden RN-003 y `sesgo.py`. La
ruptura en puntos es la que anota el motor; sin precios no la recalculo.

**(c) P3, P5, P6 y la caja (P2):**

| Sesión | Lo medido | Regla aplicada como está escrita |
|---|---|---|
| 2026-07-02 11-15 (P3) | Sesgo alcista. 120 zonas de compra formadas, 21 órdenes (5 llenadas: o7 en break even; o10, o22, o23 y o25 con el stop saltado). Cuatro entradas del trader caen a 0-1 puntos de una zona que el bot formó en la sesión, sin ninguna orden en esa entrada antes (hora de pared). **A las 14:10:00 y a las 14:23:05**, el bot está detenido por RN-016: `detenido_por_cartuchos | hasta_cartuchos_reinicio` de las 14:08 al final, tras la tercera pérdida del barrido (o22, o23 y o25, desde las 14:01; la de o10 era de un barrido anterior), con `cartuchos_max = 3` «por barrido de liquidez». **A las 12:25:50 y a las 12:45:20**, RN-011 dimensiona la zona (`zona:140`, `zona:149`) y RN-015 queda en `no`, sin ningún freno en esos cierres y sin posición viva. | **sí** las de las 14:10 y 14:23 (RN-016, `strategy_spec.yaml:1861-1867`; hechos de las 14:08 a las 15:00); **no comprobable con el visor** las de las 12:25 y 12:45 (no dice qué gate prohíbe) |
| 2026-04-13 07-11 (P3) | Sesgo alcista, 5 H4 miradas: la que decide es de un día anterior. 129 zonas, 14 órdenes. Las tres entradas del trader, a 2 puntos de zonas del bot (zona:59, :60 y :107) sin orden. A las 08:47, RN-011 da `zona:59` y RN-015 `no`; no había ninguna posición viva (pos-o5 cerró a las 07:08), así que no es RN-018. | **no comprobable con el visor** (el gate) |
| 2026-01-13 07-11 (P5) | Sesgo bajista, 2 H4 miradas: la que decide es de un día anterior. 79 zonas, 19 órdenes, 7 llenadas: 5 con el stop saltado y 2 en break even. Las tres primeras pérdidas (o5, o6 y o7; la última cierra a las 08:46:47) agotan `cartuchos_max = 3`: el visor da `RN-016 | detenido_por_cartuchos | hasta_cartuchos_reinicio` de las 08:47 a las 08:58 (12 cierres) y el freno se levanta antes de o8 (colocada a las 08:58:59), como dice `cartuchos_reinicio = siguiente_liquidez_m15`. Después llenan o9 (pérdida), o14 (break even), o17 (pérdida) y o19 (break even): dos pérdidas en los barridos siguientes, menos de tres, y ningún freno más. La racha (`racha_perdidas_max = 9`) no llega. El trader opera una vez, a las 08:42:25, a 5 puntos de la zona de o7. | **sí** (RN-016, `strategy_spec.yaml:1861-1867`; hechos de las 08:47 a las 08:58). Lo que no se ve es la toma que levanta el freno |
| 2026-04-15 11-15 (P6) | El trader no opera ese día. Sesgo alcista. 123 zonas, 15 órdenes, 5 llenadas: pos-o19, o28 y o29 en break even, pos-o24 y o27 con el stop saltado; la sesión acaba en **−3,626 R** para el bot (su R neto en «Posiciones»: −0,096, −1,400, −1,600, −0,391 y −0,139). **No acaba en break even**: la sesión no es de las de S-14. Dos pérdidas, menos de `cartuchos_max`: ningún freno tenía que saltar, y no salta ninguno. | **sí en lo que se ve** (ningún freno debía saltar y ninguno salta); por qué entra en cada zona, sin las tomas, no se ve |
| 2026-07-14 11-15 (P2, la caja) | Sesgo alcista, doble ruptura (decide el color). 110 zonas, 7 órdenes, 3 llenadas. De las seis entradas del trader: a las 12:33:40, a 2 puntos de zona:116, donde o14 se colocó a las 12:31:59 y se llenó a las 12:33:30 (la T0 de la sesión); las otras, a 0-4 puntos de zonas del bot sin orden (11:35:15, 11:48:20 y 13:06:45) o a 19-21 puntos. En la sesión hay tres pérdidas (o10 y o12, que cierran a las 11:23 y a las 11:29, y o14, a las 12:35) y RN-016 no aparece en ningún hecho (0 filas). Si las tres son del mismo barrido, el freno tendría que saltar a las 12:36; con un barrido nuevo entre o12 y o14, no. Sin las tomas no se puede saber. | **no comprobable con el visor**: el gate de las tres sin orden, y si las tres pérdidas son del mismo barrido |

**(d) S-10** (ADR-0085 §4), en las nueve sesiones. Suponiendo que la toma es la primera
`liquidez_tomada=si` de la sesión, **la primera orden de cada sesión con órdenes nace en la primera
zona formada desde esa toma** (o1, o7, o22, o5, o1, o1, o15 y o8 en sus sesiones). **Todas las
demás nacen en zonas posteriores**: en cada zona nueva se cancela la anterior y se coloca otra
(RN-006 entre las disparadas), y unas pocas se recolocan sobre una zona anterior sin formar ninguna
nueva («sin zona formada en su cierre»). Si dentro de la sesión hubo tomas nuevas, el visor no las
deja ver.

**(e) Resumen:** «sí» en las cinco de P1, en 01-13 (P5) y en lo que se ve de 04-15 (P6); 07-02 (P3),
«sí» en dos de sus cuatro entradas del trader y «no comprobable» en las otras dos; 04-13 (P3) y 07-14
(P2), «no comprobable con el visor». **Ninguna «no»**: en lo que se ve, el motor no se aparta de la
spec. La PARADA 3 sale de lo que no se ve (abajo, decisión 0), y en 07-14 con una pregunta concreta:
si tres pérdidas del mismo barrido tendrían que haber parado al bot a las 12:36.

**`antes_del_dia.py` sobre lo nuevo de la fase 3** (revisor, a4): 0 líneas en `caja-stop.txt`,
`visor-sesiones.txt`, `recuento-clases.txt`, `simular-cierre.txt`, el README y los cuatro guiones
nuevos. Su límite: en `visor-sesiones.txt` el día va en los encabezados `## AAAA-MM-DD`, así que el
guion no compara sus horas con él («0 filas con dia»). El revisor las revisó a mano y todas son del
día del caso. Sobre el informe entero marca 6 líneas: fechas de documentos de octubre y la del
apéndice A, todas de antes de la fase 3.

### F3.5 · §8 · La clasificación

Sobre las 414 filas de `patrones-cuenta-por-mes.txt` (corrida 1). Los recuentos, en
`recuento-clases.txt`; las clases del punto 1, sin cambiar ninguna.

| Patrón | Filas | Clase | Evidencia | Destino |
|---|---|---|---|---|
| T0 | 31 | pareja | `patrones-cuenta-por-mes.txt` | ninguno |
| P4, agosto desde el 2026-08-19 | 19 | efecto de la cuenta | F3.1: la cuenta de agosto deja de llenar; RN-032 en las `disparadas` de sus 14 sesiones con trader; la línea de bloqueadas no nombra el gate | ninguno (sale cuando bajen las pérdidas del bot) |
| P4, las demás | 6 | sin clase | F3.1 (3 de agosto antes del 19, 1 de enero, 1 de abril, 1 de julio) | lista |
| P7 | 4 | error nuestro conocido | F3.2: el bot ya emparejado y ninguna reentrada negada por RN-016 | la rama de RN-019 |
| P1, julio | 20 | sin clase hasta T | F3.4 (b): en las 4 sesiones de julio del visor, sesgo «sí» | T |
| P1, 2026-01-22 11-15 | 3 | sin clase: «regla desconocida», «material» o A-16, a decidir | F3.4 (b): sesgo alcista por una ruptura de 2 puntos de la H4 de las 07:00, con su color; regla aplicada «sí»; el trader vende; libro sin vídeo; 2 puntos es la discrepancia de serie de A-16 (ABIERTA) | PARADA 3, decisión 3 (*corregido tras el revisor de la fase 3, b1: la primera versión la ponía en «regla desconocida»*) |
| P1, el resto | 21 | sin clase | sin sesión en el visor; 2 de ellas, de 2026-08-27 07-11, dentro del periodo en que la cuenta de agosto no llena (`bot 0`; revisor, para el consultor) | lista |
| P2, a 4-10 puntos | 24 | sin clase (la caja, DISPERSA) | F3.3: 10 frente a 14 | dos al visor en la rama de la preparación |
| P2, a más de 10 puntos | 16 | julio (7): sin clase hasta T; enero (9): sin clase | F3.3 | T / lista |
| P3, julio | 15 | sin clase hasta T | F3.4 (c), 2026-07-02: no comprobable | T |
| P3, el resto | 39 | sin clase | F3.4 (c), 2026-04-13: no comprobable | lista (y PARADA 3, decisión 0) |
| P5, julio | 37 | sin clase hasta T | F3.4 (c): las de 2026-07-02, 07-07, 07-14 y 07-15 son de sesiones de julio del visor | T |
| P5, 2026-01-13 07-11 | 7 | sin clase: «regla desconocida» o «material», a decidir | F3.4 (c): regla aplicada «sí» (RN-016 y su reinicio); el trader opera una vez en un libro sin vídeo | PARADA 3, decisión 3 |
| P5, el resto | 109 | sin clase | sin sesión en el visor (salvo 1 fila de 2026-04-13, no comprobable) | lista |
| P6, julio | 2 | sin clase hasta T | — | T |
| P6, 2026-04-15 11-15 | 5 | sin clase: «regla desconocida» o «material», a decidir | F3.4 (c): «sí» en lo que se ve; la sesión acaba en −3,626 R (no es S-14); el trader no opera ese día, libro sin vídeo | PARADA 3, decisión 3 |
| P6, el resto | 56 | sin clase | sin sesión en el visor | lista |
| La caja: las 44 con el stop fuera (cruce de la cascada, no un patrón: van también en las filas de arriba) | 44 | sin clase (DISPERSA) | F3.3: 18 frente a 26; el redondeo explica 7 como mucho; la comisión, ninguna | dos al visor en la rama de la preparación |

**Por clase, sobre las 414 filas:** 31 pareja, 19 efecto de la cuenta, 4 error nuestro conocido, 81
sin clase hasta T (julio: P1 20, P2 de más de 10 puntos 7, P3 15, P5 37, P6 2) y 279 sin clase (con
las 3 de 2026-01-22, las 7 de 2026-01-13 y las 5 de 2026-04-15 de la decisión 3). Ninguna en
«regla desconocida» ni en «material» hasta que decidas la 3: la única sesión de P6 medida no es de
S-14.

**La lista aparte: las filas sin clase que no cubren ni el visor ni T** (279 en total): P4 6; P1 24
(enero 7, con las 3 de 2026-01-22; abril 9; agosto 8); P2 33 (las 24 de 4-10 puntos y las 9 de enero de más de 10); P3 39
(enero 21, abril 12, agosto 6, con las 3 de 2026-04-13 que el visor miró sin poder cerrar); P5 116
(enero 66, abril 29, agosto 21; incluye las 7 de 2026-01-13 de la decisión 3); P6 61 (enero 15,
abril 33, agosto 13; incluye las 5 de 2026-04-15 de la decisión 3).

### F3.6 · Los puntos 5 a 9

- **5 y 6, el orden y las líneas del cierre**, rehechas y medidas con `simular_cierre.py` sobre
  copias. F lleva el texto exacto del punto 6. R3.9 lleva el «Hecho cuando» del punto 6 y el Estado
  con el veredicto y el recuento por clase. R5.2 cita R3.9 y R5.6 no cambia. En R2.4 (T) entra la
  línea «Va antes de la preparación de la sesión 7 (RECORRIDA-CONSTRUCCION-2.md §8, respuesta a la
  PARADA 2)». Resultado: `a: []`, `b: []`, `c: []`, F viva y ninguna letra sale ni entra (vivas: `A D
  F G I J L M N Q T U`); **PROJECT_STATE, 22.773 bytes con las líneas aplicadas y 22.697 con las
  cuatro cabeceras cortas**, con los cuatro tests de `test_project_state` en verde
  (`simular-cierre.txt`). Technical Debt: nada.
- **7**: sin NOTA en §5.1 y cabeceras en forma corta; hecho así.
- **8**: la desviación 9 queda declarada como está.
- **9**: §1.4 corregido («la acción de RN-015 bloqueada por un gate, que la línea no nombra»). La NOTA
  de ADR-0070 ya no lo decía (se quitó en la entrega, a1). Las lecciones del consultor y la del
  revisor, en §7 (abajo).

### F3.7 · Lo que añade la fase 3 a la fila de ERRORES-RECURRENTES (§7)

Del consultor, menores:
- (a) D6 dijo que enero era la cuarta cuenta. Lección: el orden de un recorrido se lee en el código
  que lo fija, no en el yaml que lo lista.
- (b) D8 pidió el escalón entero de la cascada por operación sin comprobar que la salida trae el stop
  del trader. Lección: antes de pedir una tabla por operación desde una salida, se comprueba que la
  salida trae cada campo.
- (c) D6 pidió S-10 desde la salida, y la salida no trae ni la toma ni las zonas. La misma lección.
- Y de esta fase, el mismo patrón: el punto 3 pidió al visor el escenario, la toma y la regla que
  descartó cada nivel, y el visor no muestra ni tomas, ni escenarios, ni el gate de cada cierre
  (F3.4). La lección es la de (b), ahora aplicada al visor.

Para el revisor, menor: su a1 dejó escrito que `prohibida:abrir_operacion` «es siempre de RN-015».
Lección: al corregir una atribución, se lee la regla en `strategy_spec.yaml` antes de escribir la
nueva.

De la sesión:
- Medido en esta fase: la guardia niega un test cuya cadena de carga pasa de tres niveles (test →
  `caja_stop` → `para_clasificar` → `patrones` → `horas_perdidas`). Se resolvió con lo que propone
  la propia guardia: lo común pasa a `salida_comun.py`, sin importaciones locales, y un test
  comprueba que lee igual que `para_clasificar`.
- Las 22 P4 «desde el 19» eran 19. Las juntó el §4 de esta rama («P4 22 frente a 3, … donde la
  cuenta de agosto deja de llenar desde el 2026-08-19») y la respuesta del consultor lo copió
  (revisor, b5). Lección: una cifra que se va a usar como regla se mide con su condición, no con la
  frase que la acompañaba. El Estado de R3.9 (19 y 279) se rehace si la decisión 1 sale (b).

### F3.8 · La respuesta a la PARADA 2, punto por punto (revisor de la fase 3, b2)

| Punto | Lo pedido | Estado | Evidencia |
|---|---|---|---|
| Antes de nada | Fila del día antes de casos dev, visor y `make check`; recuento de reservados | Hecho | F3 (17:49:09); 0 de 76 y 0 de 9; segunda y tercera fila, declaradas |
| Antes de nada | Autorización solo a los nueve visores | Hecho | Nueve comandos, una vez cada uno (F3.4) |
| 1.a | T0, pareja | Hecho | §8 |
| 1.b | P4, efecto de la cuenta; el gate; las 3 restantes | Hecho de otra forma, declarado: 19 desde el 19, y 6 a la lista | F3.1; PARADA 3, decisión 1 |
| 1.c | P7, comprobado contra «Por operacion» y RN-016 | Hecho | F3.2 |
| 1.d y 2 | La caja: `caja_stop.py`, test en los dos sentidos, regla de los dos tercios, redondeo y comisión, las 6 no llenadas | Hecho | F3.3; `caja-stop.txt`; `test_humo.py` |
| 1.e | Las sin clase, hasta el punto 3 y, en julio, hasta T | Hecho | §8 |
| 3.a | Visor frente a corrida 1 | Hecho | F3.4 (a) |
| 3.b | P1: sesgo, H4, color, paso de RN-003 y `sesgo.py` | Hecho | F3.4 (b) |
| 3.c | Escenarios, tomas, regla que descartó | Parcial, declarado: el visor no muestra tomas, escenarios ni el gate de lo que no es un freno | F3.4 (c); PARADA 3, decisión 0 |
| 3.d | S-10 | Parcial, declarado: con una toma por sesión | F3.4 (d) |
| 3.e | «Regla aplicada como está escrita» con evidencia; PARADA si alguna es «no» | Hecho: ninguna «no»; «no comprobable» declarado | F3.4 (e) |
| 4 | §8 completo, con destino, y la lista aparte | Hecho | F3.5 |
| 5 | T antes de la sesión 7 | Hecho, en las líneas del cierre | F3.6 |
| 6 | Líneas del cierre rehechas y medidas | Hecho: 22.773 y 22.697 bytes | `simular-cierre.txt` |
| 7 | Decisiones 2 y 3 de la PARADA 2 | Hecho | F3.6 |
| 8 | Desviación 9, declarada | Hecho | F3.6 |
| 9 | Fila de ERRORES-RECURRENTES; §1.4 | Hecho de otra forma: en F3.7, para la fila del cierre | F3.7; §1.4 |
| 10 | Revisor | Hecho | Apéndice C |
| PARADA 3 | Commitear y parar | Hecho | el commit de la fase 3 |

### Lo que necesito que decidas (PARADA 3)

0. **Lo que el visor no deja ver: las tomas, los escenarios y el gate de las prohibiciones que no son
   un freno.** Por eso (c) y (e) quedan «no comprobables» en 04-13, en 07-14 y en dos entradas de
   07-02, y (d) se apoya en una toma por sesión. Opciones:
   (a) dejarlo así y que la rama de la preparación de la sesión 7 lo cubra con el visor a ojo en los
   días que elijas;
   (b) un guion que corra el motor EN PROCESO sobre esos tres días y observe la traza de cada cierre
   (las tomas de RN-004 con su nivel, los escenarios de ADR-0066 y qué regla fija cada prohibición),
   sin cambiar lo que devuelve, como `medir_f2_f3.py` de ACTIVAR-SESION-06-MOTOR. Corre el motor, así
   que necesita tu autorización expresa.
   Recomiendo (b), en su propia rama corta antes de la preparación de la sesión 7: es lo único que
   convierte esas «no comprobable» en «sí» o «no», y en 07-14 hay una pregunta concreta (si tres
   pérdidas del mismo barrido tenían que parar al bot). Si alguna sale «no», es error nuestro, y
   conviene saberlo antes de preguntar al trader. Coste de (a): esas sesiones sin clase y preguntas a
   la sesión 7 que quizá sean errores nuestros.
1. **Las 3 P4 de agosto anteriores al 19** (dos con `detenido_por_racha` el 2026-08-10). Opciones:
   (a) sin clase, en la lista, como están; (b) «efecto de la cuenta», porque la racha de RN-036 es
   de la cuenta de agosto. Recomiendo (a): la regla del punto 1.b habla del 19, y cambiarla es tuyo.
2. **El signo de Δentrada** (F3.3). Opciones: (a) la orientación del docstring de `caja_stop.py`; (b)
   la contraria. Recomiendo (a): la clase no cambia. Coste de (b): ninguno.
3. **P1 de 2026-01-22 11-15 (3 filas), P5 de 2026-01-13 07-11 (7 filas) y P6 de 2026-04-15 11-15
   (5 filas).** En 01-22 hay además una tercera lectura: la ruptura de 2 puntos que decide el sesgo
   cae en la discrepancia de serie de A-16 (ABIERTA; `sesgo.py:61-62`), así que el trader pudo ver
   otra vela; el bot no tuvo toma ni zonas en la sesión (revisor de la fase 3, b1). En las tres el motor aplica la regla
   como está escrita y el trader casi no opera: una vez, o ninguna, en libros sin vídeo. Encaja en las
   dos clases del punto 4. Opciones: (a) «material» (días sin vídeo), sin pregunta; (b) «regla
   desconocida», pregunta para la sesión 7 (¿por qué paras tras una entrada, o no entras en todo el
   día?); (c) sin clase hasta medir más días así. Recomiendo (c): son dos sesiones, y la medida de
   S-14 en P6 (que la sesión acabe en break even) aquí da que no. Coste de (a) o (b): clasificar 63
   + 116 filas por dos sesiones.

Espero tu respuesta a la PARADA 3.

## Apéndice C · El informe del revisor de la fase 3 (opus, 2026-11-08), tal cual

> ## Informe del revisor · trabajo/recorrida-construccion-2 (fase 3, lo estadiado sobre d77b0a9) · 2026-11-08
>
> Encontré dos hallazgos que importan, uno por eje, y siete menores. Ninguno bloquea. Ninguno cambia una clase del punto 1, pero los dos cambian lo que el informe afirma. El primero es una cuenta: «26 de 37 no llega a dos tercios» es falso, porque 26/37 son el 70,3 %. La conclusión sigue en pie con los signos medidos. El segundo es la clase «regla desconocida» de 2026-01-22: el informe la pone sin plantear la alternativa que sí plantea en dos sesiones iguales, y la ruptura de 2 puntos cae en la discrepancia abierta de A-16.
>
> ### Eje (a) · Reglas de la casa
> Resumen: 0 bloquea, 1 importa, 3 menor.
>
> | # | Gravedad | Hallazgo | Evidencia | Qué hacer |
> |---|---|---|---|---|
> | a1 | importa | Una afirmación que su cifra no sostiene. En F3.3 el informe dice: «Aunque se quitaran, el signo sigue disperso (por cualquiera de los dos lados, 26 de 37 o 19 de 37 no llegan a dos tercios)». Pero 26/37 = 70,3 %, que sí llega a dos tercios (66,7 %). La conclusión se sostiene por otra cuenta. De las 7 a 4 puntos exactos, 4 tienen Δstop +4 y 3 tienen −4. Quitando las 7 quedan 14 frente a 23 de 37 (62,2 %). Si solo cuenta el redondeo «alejándose de la entrada», que solo puede dar positivos, se quitan las 4 positivas y quedan 14 frente a 26 de 40 (65,0 %), justo por debajo del umbral. | `docs/validation/RECORRIDA-CONSTRUCCION-2.md:1215-1218`. En `caja-stop.txt`, Δstop ±4 en las líneas 20 (−4), 21 (+4), 29 (+4), 36 (+4), 42 (−4), 43 (−4) y 58 (+4). | Cambiar la frase por las dos cuentas medidas (62 % y 65 %) y decir que la segunda queda a 1,7 puntos del umbral. |
> | a2 | menor | «Las exposiciones de cada día» sigue diciendo «las dos filas de esta rama». Ahora son cinco: tres de las fases 0 a 2 y dos de la fase 3. | `RECORRIDA-CONSTRUCCION-2.md:787-790`. `git diff --cached -- docs/validation/HOLDOUT-EXPOSICIONES.md` añade dos filas a las tres que ya había. | Actualizar en la fase 3: es el informe propio de la rama y no está cerrado en `main`. |
> | a3 | menor | La fila 1 de la fase 3 en HOLDOUT-EXPOSICIONES dice «por el recuento: marzo… entero y holdout-3 (los días de junio)» sin ningún número. La respuesta pedía lo que calientan los visores «por recuento». | `HOLDOUT-EXPOSICIONES.md`, la fila añadida en la línea 86 del diff estadiado (columna «por el recuento»). | Dar el número de días reservados cuyas velas se leen, igual que se dan 34/34 para `casos_reservados` y `casos_ocultos`. Es una fila del día, así que solo se puede añadir otra. |
> | a4 | menor | F3 no dice que se pasara `antes_del_dia.py` sobre los ficheros nuevos. Yo lo pasé: da 0 líneas en `caja-stop.txt`, `visor-sesiones.txt`, `recuento-clases.txt` y los cuatro guiones nuevos. Sobre el informe entero marca 6 líneas «fecha fuera de la construccion» (69, 840, 862, 866 y 885 dos veces), todas anteriores a la fase 3, ya commiteadas y en lo que vio el revisor de la fase 2 (desviación 9 y Apéndice A). Ninguna está en lo estadiado. Ojo: el guion no mira las horas de `visor-sesiones.txt` («0 filas con dia»), porque sus días van en encabezados `## AAAA-MM-DD`. Esas horas las revisé a mano: todas son del día del caso. | La salida de `antes_del_dia.py` (comando 26). | Declarar la pasada en F3, con el límite sobre `visor-sesiones.txt`. |
>
> Comprobado sin hallazgos:
> - (6) Nada cambia en `src/`, `tests/`, `knowledge/`, `scripts/` ni `.claude/`. `git diff main --stat` y `git diff --cached --stat` sobre esas rutas salen vacíos. Los 14 ficheros estadiados están todos en `rutas_permitidas` del contrato.
> - (5) En las líneas añadidas no hay ninguna fecha de mes reservado (2025/2026-02, 03, 05, 06, 09, 10, 11, 12). La única fecha que aparece es 2026-11-08, el día de trabajo, 11 veces.
>   - Las H4 de un día anterior van tapadas: «de un día anterior» y «abre un dia anterior», sin hora (`RECORRIDA-CONSTRUCCION-2.md:1252-1253, 1270-1271`; `visor-sesiones.txt:151, 180`).
>   - Las horas y los bloques de `visor-sesiones.txt` son del día del caso.
>   - Los instantes de `caja-stop.txt` son todos del día de su fila.
> - HOLDOUT-EXPOSICIONES solo añade líneas.
> - La respuesta a la PARADA 2 está copiada idéntica en el encargo y en el informe: md5 `0448c7f0…` en las dos, quitando la línea en blanco final del informe.
> - §1.4 está corregido con la frase del punto 9. ADR-0070 no nombra RN-015.
> - No hay ADR nuevos ni informes cerrados de `main` tocados. `RECORRIDA-CONSTRUCCION-2.md` no está en `main`.
> - Las citas del informe coinciden con su fuente:
>   - `strategy_spec.yaml:1861-1867` (RN-016) y `:2536-2544` (RN-032);
>   - `sesgo.py:110-115` (doble ruptura por color) y `:124-127` (una ruptura con su color);
>   - `cartuchos_max = 3` en `parametros.yaml:1109`;
>   - `cartucho_criterio = solo_perdida`: el break even cuenta por mecanismo, así que pos-o28 de 04-15 no suma, y el «ningún freno debía saltar» se sostiene.
> - El informe acaba en su estado: «Rama lista para revisión, NO cerrada».
>
> ### Eje (b) · Encargo de la fase 3 (respuesta a la PARADA 2)
> Resumen: 0 bloquea, 1 importa, 4 menor. Requisitos: 22 hechos, 3 parciales (declarados), 1 no hecho, 2 hechos de otra forma (declarados), 1 pendiente (el commit).
>
> | # | Requisito | Estado | Evidencia |
> |---|---|---|---|
> | 1 | La fila de HOLDOUT, estadiada antes de casos dev, visor y make check | Hecho | Fila de la línea 86 del diff. Los nueve HTML de `data/visor/` son de 17:53:15 a 17:54:19; el informe estadió la fila a las 17:49:09 (`:1162`). |
> | 2 | Solo los nueve comandos del visor, una vez cada uno | Hecho | Nueve ficheros de hoy, en el orden del consultor, uno por día (`ls --time-style=full-iso data/visor/`). |
> | 3 | 1.a T0 (31): pareja | Hecho | §8, `:1296`. En `recuento-clases.txt` T0 suma 7+8+14+2 = 31. |
> | 4 | 1.b P4: la clase, el gate, las 3 restantes | Hecho de otra forma, declarado (decisión 1 de la PARADA 3) | 19 desde el 19, comprobadas a mano (`patrones-cuenta-por-mes.txt:281-302` sin 297 y 298). Las 3 anteriores: 08-10 ×2 con `detenido_por_racha` (`:254-255`) y 08-14 con `orden_dimensionada:no` (`:273`). RN-032 está en `disparadas` en las 14 sesiones del 19 al 31, con `bot 0`; en 13 bloqueadas sale RN-015 y en una «ninguna» (`cuenta-por-mes.txt:814-827`). |
> | 5 | 1.c P7 contra «Por operacion» y RN-016 | Hecho | `patrones-cuenta-por-mes.txt:177-178, 183-185, 308-309`: el bot más cercano es la PAREJA de otra operación del trader. RN-016 no está en `disparadas` y `detenido_por_cartuchos:no` en 01-02 11-15, 07-10 07-11 y 07-10 11-15 (`cuenta-por-mes.txt:725, 790-791`). |
> | 6 | 2. `caja_stop.py`, con un test de humo que rompa en los dos sentidos | Hecho | `test_humo.py`, diff estadiado: signos en compra y en venta, borde de dos tercios en SISTEMATICA y DISPERSA. Lo vuelvo a correr y da los mismos resúmenes y las mismas 122 líneas que `caja-stop.txt`. |
> | 7 | 2. Campos por operación y resumen | Hecho | Comprobadas a mano cinco operaciones (abajo). |
> | 8 | 2. Regla de los dos tercios aplicada como está escrita | Hecho | 18/26 de 44 (59 %) y 10/14 de 24 (58 %): DISPERSA las dos (`caja-stop.txt:72, 121`). Recontadas a mano; los meses de las 24 y las 16 coinciden. |
> | 9 | 2. Redondeo y comisión antes de dar la clase | Parcial | La conclusión es correcta y la cuenta que la sostiene no: ver a1. |
> | 10 | 2. Motivo literal de las 6 no llenadas | Hecho | `caja-stop.txt:7, 32, 40, 56, 60, 69`, igual que en «Ordenes» (o24 de 07-13 en `cuenta-por-mes.txt:2867`). |
> | 11 | 3.a Órdenes del visor frente a la corrida 1 | Hecho | Iguales en ocho días. 07-15 tiene o25 a o29 de más, y en la corrida 1 la sesión 11-15 acaba en `detenido_por_racha:si` con RN-036 (`cuenta-por-mes.txt:797`), tras pos-o24 (`:3456`). `visor_sesiones.py` vuelto a correr: 255 líneas, las mismas. |
> | 12 | 3.b P1: sesgo, la H4 que decide, su color y el paso de `sesgo.py` | Hecho | Comprobado en 07-15 11-15: el rect `decide` contiene el rect `baja`, con doble ruptura a la vista y RN-003 en `bajista` (HTML). |
> | 13 | 3.c Escenarios, tomas y regla que descartó | Parcial, declarado (decisión 0 de la PARADA 3) | `:1233-1239`. Confirmo que en 04-13 solo salen RN-003 (2), RN-004 (155), RN-011 (345) y RN-015 (345). |
> | 14 | 3.c P6 de abril: ¿acaba en break even? | Hecho | Las R netas suman −3,626 (`cuenta-por-mes.txt:3372-3376`). |
> | 15 | 3.d S-10 | Parcial, declarado (supone una toma por sesión) | `visor-sesiones.txt`: las primeras órdenes son o1, o7, o22, o5, o1, o1, o15 y o8. Coinciden. |
> | 16 | 3.e «Regla aplicada como está escrita», con evidencia | Hecho, con un tercer estado «no comprobable» declarado | Tres casos comprobados (abajo). |
> | 17 | 3. Ningún instante anterior al día dev | Hecho | Ver eje (a), (5). |
> | 18 | 4. Tabla de §8 completa, con destino, y la lista aparte | Hecho | Cada fila tiene destino. Las filas suman 414. Por clase: 31+19+4+3+81+276 = 414. La lista: 6+21+33+39+116+61 = 276. Todo recontado contra `recuento-clases.txt`. |
> | 19 | 5. T antes de la sesión 7 | Hecho | `simular_cierre.py`: F y la línea en R2.4. |
> | 20 | 6. Las líneas del cierre, medidas | Hecho | F es el texto exacto del punto 6. Vuelto a correr: la salida es idéntica a `simular-cierre.txt` (22.773 y 22.697 bytes, menos de 23.000; a, b y c vacíos). |
> | 21 | 7. Decisiones 2 y 3 | Hecho | F3.6, `:1335`. |
> | 22 | 8. Desviación 9 | Hecho | `:1336`. |
> | 23 | 9. Las lecciones del consultor y la del revisor | Hecho de otra forma (en F3.7, no dentro de §7) | `:1341-1363`. |
> | 24 | 9. Corregir §1.4 (y la NOTA de ADR-0070 si hace falta) | Hecho | Diff estadiado, líneas 9-18. ADR-0070 no nombra RN-015. |
> | 25 | Copia de la respuesta, tal cual, en el encargo y en el informe | Hecho | md5 igual. |
> | 26 | Tabla «El encargo, punto por punto» de la fase 3 | No hecho | Ver b1. |
> | 27 | 10. Revisor, informe pegado al final | En curso | Este informe. |
> | 28 | PARADA 3: commitear y parar | Pendiente | Está estadiado, sin commit; el make check de la fase 3 no se ve todavía. |
>
> Las cinco operaciones de la caja, a mano (stop del trader del caso dev; orden del bot de `cuenta-por-mes.txt`, con stop = precio ∓ distancia). Todas coinciden con `caja-stop.txt`:
> - 01-02 12:12:20, venta, stop fuera, positiva: o9, 1.17243 con 37 puntos, da stop 1.17280. Δstop +35, cociente 9,25.
> - 08-03 09:46:15, venta, stop fuera, positiva: o23, 16 puntos, da 1.15292. Δstop +8, cociente 1,60.
> - 04-01 12:30:20, compra, stop fuera, negativa: o7, 14 puntos, da 1.15956. Δstop −19, cociente 0,42.
> - 07-16 06:00:10, compra, stop fuera, negativa: o6, 11 puntos, da 1.14641. Δstop −19, cociente 0,34.
> - 07-13 11:25:05, no llenada: o24, 21 puntos, da 1.14256. Δstop −3; el motivo coincide literalmente.
>
> Los stops del trader salen de `knowledge/cases/dev/caso-eurusd-2026-{01-02,08-03,04-01,07-16,07-13}.yaml`.
>
> Las tres «regla aplicada: sí», a mano:
> - **07-15 11-15, el sesgo:** en el SVG de la H4, el rect «11-15: bajista, rompe esta H4» contiene una vela `baja` que rompe los dos extremos de la anterior. Corresponde a `sesgo.py:110-115`.
> - **07-02, RN-016:** `detenido_por_cartuchos=hasta_cartuchos_reinicio` de 14:08 a 15:00 (53 cierres). La tercera pérdida del barrido, pos-o25, cierra a las 12:07:23 UTC = 14:07 de pared (`cuenta-por-mes.txt:3417-3419`).
> - **01-13, RN-016:** de 08:47 a 08:58, 12 cierres. pos-o7 cierra a las 07:46:47 UTC = 08:46 de pared (`:3279`). Después llenan o9 y o17 (pérdidas) y o14 y o19 (break even), como dice el informe.
>
> | # | Gravedad | Hallazgo | Evidencia | Qué hacer |
> |---|---|---|---|---|
> | b1 | importa | En §8, la fila P1 de 2026-01-22 11-15 (3 filas) va a «regla desconocida», con destino la hoja de la sesión 7. Hay dos problemas. **(i)** Las sesiones 01-13 (P5) y 04-15 (P6) están en la misma situación: regla «sí» y un libro sin vídeo. Para esas dos el informe dice que «encaja en las dos clases del punto 4» y las lleva a la decisión 3 de la PARADA. La de 01-22, que también es de enero (sin vídeo, o sea «material» según el punto 4), la cierra la sesión sin plantear la alternativa. **(ii)** La única evidencia es «ruptura de 2 puntos». Eso cae justo en la zona que `sesgo.py:61-62` y A-16 (ABIERTA) llaman discrepancia entre la serie del trader y la nuestra («2 puntos de mediana», `ambiguedades.yaml:288-302`). La cita no sostiene que «el trader hizo otra cosa» frente a la regla: pudo ver otra vela. Además el bot no tuvo toma ni zonas en la sesión. | `RECORRIDA-CONSTRUCCION-2.md:1256, 1301, 1386-1392`. `visor-sesiones.txt:99-102`. | Pasar 01-22 a la decisión 3 (o a una decisión propia), con A-16 nombrada como tercera lectura. Rehacer en consecuencia el recuento por clase de §8 y el Estado de R3.9 en `simular_cierre.py`. |
> | b2 | importa | No hay tabla «El encargo, punto por punto» para la fase 3. La de `:736` es de la fase 2. F3.1 a F3.7 van punto por punto en prosa, pero sin el estado de cada requisito (Hecho, Parcial, Hecho de otra forma) que pide la skill `entregar-rama`. | `RECORRIDA-CONSTRUCCION-2.md:1160-1394`: no hay tabla. | Añadir la tabla en F3. Puede partir de la de requisitos de arriba. |
> | b3 | menor | La convención de Δstop no es literalmente la del consultor. El consultor pide «el del bot más lejos de la entrada» (distancias). El guion mide stop contra stop, «del lado del stop». Para las 44 da el mismo signo, porque la diferencia de distancias es Δstop − Δentrada, con \|Δentrada\| ≤ 3 < 4 ≤ \|Δstop\|. Pero no se declara. | `caja_stop.py:25-31`; `RECORRIDA-CONSTRUCCION-2.md:1204-1208`. | Una frase en F3.3: es otra medida y da el mismo signo en las 44, por esa desigualdad. |
> | b4 | menor | Las 44 de la caja se cruzan con filas que ya tienen clase y no se dice cuántas. Por ejemplo, 07-10 07:17:40 y 01-02 13:21:50 son P7, «error nuestro conocido» (`caja-stop.txt:47, 8`). Y la de 07-02 11:59:30 parece la T0, «pareja», de esa sesión (`:41`; `recuento-clases.txt:54`). Así una misma operación sale como «sin clase (DISPERSA)» y con otra clase a la vez. | `RECORRIDA-CONSTRUCCION-2.md:1313`. | Decir cuántas de las 44 caen en cada patrón. |
> | b5 | menor | La lección «Las 22 P4 “desde el 19” eran 19: una cifra del consultor se mide antes de copiarla» atribuye el origen al consultor. Pero fue el §4 de la propia rama el que puso juntos «P4 22» y «deja de llenar desde el 2026-08-19». Además, el Estado de R3.9 ya lleva el 19 y el 276, y eso cambia si la decisión 1 de la PARADA 3 sale (b). | `RECORRIDA-CONSTRUCCION-2.md:644-645, 1363`; `simular_cierre.py`, R39. | Nombrar el §4 en la lección. Avisar de que R3.9 se rehace según la decisión 1. |
> | b6 | menor | 3.b pide «el paso de RN-003» y la tabla de P1 solo cita `sesgo.py`, sin la línea de RN-003 en `strategy_spec.yaml`. | `RECORRIDA-CONSTRUCCION-2.md:1250-1256`. | Añadir la línea de RN-003. |
>
> Lo que la rama hace y el encargo no pide:
> - `salida_comun.py`, para no pasar de los tres niveles de carga que deja la guardia. Está declarado y justificado (`:1359-1362`; README).
> - La lista de lo que el visor no muestra. Está declarada y va a la PARADA 3.
>
> Las dos cosas están dichas. Nada de lo que el encargo dice que no se toca aparece en el diff: ni ningún motor arnes ni nada del visor commiteado. `data/` está ignorado.
>
> Sobre la pregunta (4), P4 19 frente a 22: no cambia ninguna clase. Aplica la definición del consultor tal como está escrita: «desde el 2026-08-19, cuando la cuenta deja de llenar». Lo medido lo confirma: las 3 anteriores tienen otra causa, racha y `orden_dimensionada:no` con la cuenta todavía llenando. Las deja sin clase y pide la decisión 1. Está bien llevado. Aparte, para el consultor: 2 filas P1 del 2026-08-27 07-11 caen dentro del periodo sin llenar, con `bot 0` (`patrones-cuenta-por-mes.txt:297-298`), y siguen en la lista como P1.
>
> ### Lo que no pude comprobar
> - **El make check y el sello de la fase 3.** No se ejecuta (escribe) y no leí `make-check.log`, porque está en la raíz y el alcance la excluye. La tabla «Los make check de la rama» (`:792-801`) no recoge ni la entrega (d77b0a9) ni la fase 3.
> - **`scripts/contrato_rama.py` y `botsito state check`.** Quedan fuera de lo que se me permitió ejecutar.
> - **El recuento 34/34 de `casos_reservados`/`casos_ocultos` y el 0 de los días leídos.** Sale de un guion de la carpeta de trabajo de la sesión, fuera del repo.
> - **`test_humo.py` (21 passed).** No lo corrí: pytest escribe caché y tmp_path. Leí los tests nuevos y cubren los dos sentidos.
> - **La hora real del estadiado de la fila de HOLDOUT (17:49:09).** Solo puedo decir que los nueve HTML son posteriores.
>
> (La lista de comandos del revisor, 20 entradas, queda en su transcripción: git de lectura, Read y Grep de rutas literales, las páginas de `data/visor/`, `uv run python -B` de `simular_cierre.py`, `caja_stop.py`, `visor_sesiones.py` y `antes_del_dia.py`; y cuatro formas que negaron las guardias y no reescribió para rodearlas: un `for`, una redirección a la carpeta de trabajo, `| md5sum` y un comando compuesto.)

## Lo hecho con cada hallazgo del revisor de la fase 3

| # | Lo hecho |
|---|---|
| a1 | F3.3 corregido con las dos cuentas medidas: quitando las 7 a 4 puntos, 14 frente a 23 de 37 (62,2 %); quitando solo las 4 positivas, 14 frente a 26 de 40 (65,0 %), a 1,7 puntos del umbral. Dispersa en las dos. |
| a2 | «Las exposiciones de cada día»: cinco filas (tres de las fases 0 a 2 y dos de la fase 3) y una sexta con lo que pide a3. |
| a3 | Fila nueva en HOLDOUT-EXPOSICIONES con los recuentos: junio, 11 días reservados (holdout-3, `casos_reservados`); marzo, mes reservado entero sin sortear (`meses_reservados.yaml`; 0 en `casos_reservados`, porque no tiene partición). |
| a4 | F3 declara la pasada de `antes_del_dia.py` sobre los ficheros nuevos y su límite sobre `visor-sesiones.txt` (horas revisadas por el revisor a mano). |
| b1 | 01-22 pasa a la decisión 3 con A-16 como tercera lectura; §8 y el Estado de R3.9 se rehacen: 0 «regla desconocida» y 279 sin clase. |
| b2 | Tabla F3.8, la respuesta a la PARADA 2 punto por punto. |
| b3 | Frase en F3.3: medido stop contra stop; da el mismo signo que la diferencia de distancias en las 44, porque \|Δentrada\| ≤ 3 < 4 ≤ \|Δstop\|. |
| b4 | De las 44 con el stop fuera: 20 son T0, 11 P3, 11 P2 y 2 P7 (medido con un guion de la carpeta de trabajo). Dicho en §8. |
| b5 | La lección nombra el §4 de la rama, y F3.6 avisa de que R3.9 se rehace según la decisión 1. |
| b6 | La tabla de P1 cita RN-003 (`strategy_spec.yaml:1079`). |
| Para el consultor | Las 2 filas P1 de 2026-08-27 07-11, dentro del periodo sin llenar de agosto, dichas en §8 (P1, el resto). |
| No pudo comprobar | El `make check` de la fase 3 y su sello: tabla «Los make check de la rama» completada. |

## Estado

**Rama lista para revisión, NO cerrada.** PARADA 3: la entrega de la fase 3 (respuesta del
consultor a la PARADA 2): la caja medida (dispersa en los dos grupos), las nueve sesiones del
visor (ninguna «no»; tres con partes «no comprobables», decisión 0), §8 con su recuento por clase
y las líneas del cierre rehechas y medidas. El revisor de la fase 3 (apéndice C): 0 bloquea, 2 importa, 7 menor; todo arreglado o declarado en
«Lo hecho con cada hallazgo del revisor de la fase 3». Nada de esta
rama entra en la hoja de la sesión 7 por su cuenta.
