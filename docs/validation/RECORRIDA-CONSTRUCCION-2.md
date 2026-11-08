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
en la misma línea, `bloqueadas` con `prohibida:abrir_operacion`, que es siempre de RN-015 y sale en
96 de las 104 sesiones haya RN-032 o no (revisor, a1; RECORRIDA-CONSTRUCCION.md §2.2, a4):

| mes | sesiones | RN-032 disparada | de ellas, con `prohibida:abrir_operacion` (de RN-015) | primer y último día |
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

Un solo día de trabajo, el 2026-11-08: las dos filas de esta rama en `HOLDOUT-EXPOSICIONES.md` (la de
la apertura y la de lo que no nombraba). Ninguna etiqueta ni cifra del bot de un día reservado; nada
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
| (entrega: este informe, `simular_cierre.py` y el revisor) | ver «Estado» | — |

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

## Estado

**Rama lista para revisión, NO cerrada.** PARADA 2: la entrega para mirar. La clasificación de
las diferencias es del consultor; nada de esta rama entra en la hoja de la sesión 7 por su
cuenta. El revisor (apéndice B): 0 bloquea, 5 importa, 4 menor; todo arreglado o declarado en
«Lo hecho con cada hallazgo del revisor».
