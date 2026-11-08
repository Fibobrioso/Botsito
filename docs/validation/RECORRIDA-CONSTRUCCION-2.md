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
   (`criterio_fidelidad.perdida_diaria_maxima`), y RN-032 sale de «Por sesion», columna `bloqueadas`
   (`arnes.py:260-265`). Se dice en §1 qué es leído y qué derivado.
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
| `orden_pendiente_al_abrir_escenario` | `se_mueve` | A-53 | fb-2026-09-29-sesion-03-c7fa3068 |
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

## Lo que necesito que decidas

Nada para seguir: la PARADA de la fase 0 es condicional y lo medido cuadra con D1 a D12 en lo que
decide (0.1). Dos cosas para la PARADA 2, que no detienen nada:

0. **El escalón entero de la cascada en la lista de D8.** Opciones: (a) dejarlo hasta la entrada,
   como sale de la salida sola (0.k, punto 6); (b) leer el stop del trader de los casos dev para
   cerrar los cinco escalones de detrás. Recomiendo (a) en esta rama, porque D8 dice «SOLO las
   salidas commiteadas»; si en la PARADA 2 hace falta, (b) es un guion más sobre material de
   desarrollo. Coste de (b): leer `knowledge/cases/dev/` (sin puerta, declarado) y otro guion.
1. **Una NOTA también en §5.1 de `ACTIVAR-A35-A44.md`** (herencia H2). Opciones: (a) no, la de §5
   basta (D7); (b) una línea igual en §5.1. Recomiendo (a): D7 lo fija. Coste de (b): un commit.

## Estado

EN CURSO: fase 0 hecha (PARADA condicional: sigue a la fase 1 sin esperar, 0.1); faltan la
fase 1 (README y guiones), la fase 2 (las corridas), el informe de §1 a §7 y el revisor.

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
