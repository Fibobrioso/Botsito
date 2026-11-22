# RECORRIDA-CONSTRUCCION-3 · La corrida (3): la 7b activada, sobre toda la construcción, el pivote de ADR-0093 §6 y la meta de ADR-0098: el techo del trader y el R de las parejas (R4.3, entrada F)

> PLANTILLA hasta la entrega: la fase 0 está escrita; las corridas, el pivote y la meta van en §1 a §8.

Rama `trabajo/recorrida-construccion-3`, abierta el 2026-11-22 desde `main` en 19c171d7 (commit de
estado sobre el merge f04868cc del tag `stable/F39k-activar-sesion-08`). Encargo:
`docs/encargos/trabajo-recorrida-construccion-3.md`. Tramo: R4 (R4.3 de `docs/plan/HOJA-DE-RUTA.md`;
el paso (3) de la F de la Next Action), más la medida de la meta de ADR-0098, que sustituye a R5.7.
Tag previsto: `stable/F39l-recorrida-construccion-3` (no existe ni en local ni en origin: `git tag
--list "stable/F39l*"` y `git ls-remote --tags origin "stable/F39l*"` vacíos).

## Base comprobada (abrir-rama, paso 1)

- `git rev-parse main origin/main`: `19c171d7af422bdcf5e75f1fc1cd3caa2ced0c70` dos veces; `git status --short` vacío.
- `git rev-parse "stable/F39k-activar-sesion-08^{commit}"` = `f04868ccb5fe23b80b21312d4519fa8742ecc3e8` = `git rev-parse main^1`; en origin: `git ls-remote --tags origin stable/F39k-activar-sesion-08` da `1d2fc835…` (el objeto del tag anotado).
- CI de `main`: `gh run view 45051429307` (suelto, sin guion, como pide el encargo; la skill `abrir-rama` nombra la API de check-runs) → `workflowName: ci`, `status: completed`, `conclusion: success`, `headSha: 19c171d7af422bdcf5e75f1fc1cd3caa2ced0c70` (2026-11-22T17:47:43Z). Es el número que da el encargo; el informe de cierre de F39k que lo dio no está en el repo.
- `git branch --list` solo daba `main`; `git ls-remote --heads origin` solo da `refs/heads/main`.
- Sesión en Opus 5.5, esfuerzo alto; `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1` puesta (medido con `echo`): las corridas pueden ir en segundo plano.

## Desviaciones de la apertura

- **`META-TECHO-PAREJAS.yaml` no estaba en el Escritorio al empezar.** `ls` encontró solo
  el borrador del ADR de la meta; se le pidió a Aleks antes de abrir, sin reconstruirlo, y lo dejó. Los dos
  ficheros se leyeron enteros antes de abrir: ninguna fecha de día reservado ni ningún resultado.
- **La fila de HOLDOUT-EXPOSICIONES del día** se escribió y estadió (14:32, hora local) tras crear la
  rama y antes de cualquier otra escritura, lectura de material o `make check`. Declara lo que leen los
  `make check` como la skill `abrir-rama` y las filas de hoy: el M1 de marzo y el calentamiento con el
  de junio (el encargo nombraba solo marzo; gana la skill).
- **ADR-0098 no se pudo citar fuera del encargo antes de existir**: el primer `knowledge validate` dio
  cuatro «id citado que no existe» (PROJECT_STATE, la fila de HOLDOUT y la cabecera de este informe),
  porque el bloque `ids-inexistentes` solo exime al documento que lo lleva. Se quitó el id de esos tres
  ficheros hasta el commit del pre-registro.

## §0 · Las decisiones del consultor, la fase P y la fase 0

### §0.1 Las decisiones del consultor (D1 a D14)

Están en el encargo («DECISIONES DEL CONSULTOR (2026-11-22)»), escritas antes de correr. Cada sección
del informe dice cuál aplica; la fase 0 (§0.3) dice cuáles cuadran con lo medido y §0.5 la única que
no.

### §0.2 La fase P (el pre-registro, antes de ninguna corrida)

- **Commit `539f7983dc96384272359de970841509cbc3abd8`, 2026-11-22 15:49:25 -0500**,
  «docs(adr): ADR-0098, la meta pre-registrada antes de la corrida (3)», justo después del de apertura
  (`3457fb31`, 15:12:55). La hora de la primera corrida va en §1, para que se vea el orden.
- `docs/adr/0098-la-meta-se-mide-en-la-corrida-3.md` frente a `C:\Users\USER\Desktop\ADR-0098-borrador.md`
  (`diff`), solo las dos marcas:

  ```
  3c3
  < date: <FECHA-DEL-COMMIT>
  ---
  > date: 2026-11-22
  292c292
  < <FECHA-DEL-COMMIT>; post-F14, rama de la corrida (3) (R4.3, NA:F).
  ---
  > 2026-11-22; post-F14, rama de la corrida (3) (R4.3, NA:F).
  ```

- `docs/plan/META-TECHO-PAREJAS.yaml`: `cmp` con el del Escritorio, idéntico. 2.839 bytes, 50 LF, 0 CR,
  sin BOM, sha256 `bb8291df8da8cbc53334f6128348a38e2cf516aef286da4fbeca456ec5b21bcc`, el mismo en el
  blob del índice (`git show :docs/plan/META-TECHO-PAREJAS.yaml`): git no convirtió los saltos
  (`.gitattributes`: `* text=auto eol=lf`).
- `tests/unit/test_meta_techo_parejas.py`, con la forma de `test_pivotes_sesion_7.py`: el sha256 del yaml;
  lectura con `leer_yaml`; `decision` = ADR-0098; los seis valores de `propios` (95, "0.10", "0.10", "0",
  "0", 2); las salidas A, B, C y D en su orden; las cuatro claves de la precedencia (C, B, A, D, en el
  orden del yaml); el orden de lectura del techo (gana, no_gana, no_concluyente) y las claves de las dos
  lecturas; que `parejas_minimo_desde` nombra `minimos.minimo_1_parejas_de_julio_al_menos` de
  `PIVOTES-SESION-7.yaml` con el valor 19; que `criterio_fidelidad.yaml` trae `rentabilidad` con
  `n_minimo` 100 y `esperanza_minima_r` "0.10"; y dos que rompen a propósito (la banda de las parejas que
  ganan a "0.05"; el mínimo que remite a otra clave del pivote). 5 tests en verde; `ruff format`,
  `ruff check` y `mypy` limpios. Tests Currently Passing: 2132 → 2137.
- La fila 0098 del índice (`docs/adr/README.md`) y el recuadro, tal cual con la fecha del commit, al
  final de ADR-0092 §6, tras su NOTA del 2026-11-09; el cuerpo no se toca.
- ADR-0098 salió del bloque `ids-inexistentes` del encargo, y el bloque con él. `state check` y
  `knowledge validate` limpios; `make check` en verde: 3612 passed, 6 xfailed, sello sobre el árbol
  `8c0f0dd4…`.
- **Desviación declarada (auditor, choque 9):** la skill `fase-cero` manda auditar el encargo antes de
  usarlo y no escribir código antes de la respuesta, y el encargo pone la fase P (con su test) antes de
  la fase 0. Se siguió el orden del encargo, que es la prueba del pre-registro. El auditor no encontró
  nada en el ADR ni en el yaml que no case con el repo.

### §0.3 La fase 0 (inventario, sin correr el arnés)

**a) La corrida 1 cuenta, y el nombre de la 2.**
- Los comandos de la fase 2 usan `--simular` y `--salida`; las dos están en
  `OPCIONES_QUE_NO_CAMBIAN_LA_CORRIDA` (`src/botsito/engine/arnes.py:80-82`, junto a `--tracemalloc`,
  `--meses`, `--perfil` y `--fase`). Las opciones se leen de los parsers, no de una lista
  (`src/botsito/cli.py:2218-2232`), y cualquiera fuera de la lista da «no» (`arnes.py:286-289`).
- Sin `--meses`, los meses son los de `construccion` (`cli.py:2386`): 2026-04, 2026-07, 2026-08 y
  2026-01; el orden de las cuentas lo da `arnes.validar_meses` (ordenados, `arnes.py:121`).
- Perfil efectivo: sin `--perfil`, el único de `knowledge/cuentas/` (`src/botsito/engine/cableado.py:694-699`):
  `ftmo-2step-swing-100k`, que es `perfil_para_medir` (`knowledge/cases/criterio_fidelidad.yaml:37`).
  Fase efectiva: sin `--fase`, la primera del perfil (`cableado.py:734`): `reto` (`firma_fases` = «reto
  verificacion fondeada», `knowledge/cuentas/ftmo-2step-swing-100k.yaml:85-86`). `habilita_medir` lo
  comprueba con `Simulacion(motor.perfil, motor.fase, perfil.fases()[0])` (`cli.py:2441`;
  `src/botsito/cases/criterio_fidelidad.py:194-213`).
- La cuenta por mes es una condición del recorrido, no una opción: `MotorCableado.correr_dia` cierra la
  cuenta al cambiar de mes y abre otra (`cableado.py:334-345`), salvo con `cuenta_diaria`, que solo pone
  `--diagnostico-cuenta-diaria` (`cli.py:2261`, `:2438`).
- **La corrida 2 escribe `docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/diaria.DIAGNOSTICO.cuenta=diaria.txt`**:
  `nombre_etiquetado` (`src/botsito/engine/diagnostico.py:174-191`; la etiqueta, `:95`), aplicado antes de
  leer velas (`cli.py:2405-2407`). Es el nombre que dio la corrida 2 de RECORRIDA-CONSTRUCCION-2.

**b) Ticks.** Con el mismo mercado que construye el arnés (`simulacion.mercado_de_construccion`,
`src/botsito/engine/simulacion.py:183-218`, por su compuerta), sobre los 76 días dev: **ningún día dev
sin ticks**. Cada manifiesto cubre los días de su mes (`eurusd-ticks-2026-01-1ce59681`: 21;
`eurusd-ticks-2026-04-1d189bdd`: 21; `eurusd-ticks-2026-07-6e7dc7cd`: 13; `eurusd-ticks-2026-08-75bd3a08`:
21). Las horas perdidas, las que cubre el respaldo M1, las da cada manifiesto por mes:
- 2026-01: 5 (01-05 10Z, 01-14 07Z, 01-20 11Z, 01-23 11Z, 01-29 11Z);
- 2026-04: 7 (04-03 09Z, 04-06 10Z, 04-07 10Z, 04-22 07Z, 04-22 10Z, 04-22 13Z, 04-23 05Z);
- 2026-07: 3 (07-10 05Z, 07-14 12Z, 07-16 11Z);
- 2026-08: 3 (08-14 07Z, 08-17 11Z, 08-20 07Z).

Son 18, como las 18 «filas marcadas posible M (hora perdida)» de `patrones.py` sobre la línea base
anterior. No hace falta `--depuracion`. Guion de la carpeta de trabajo de la sesión, con la raíz por
argumento; la primera versión repetía las horas del mes en cada día (las da el manifiesto, no el día), y
lo de arriba es el recuento por mes.

**c) La comisión del perfil.** `firma_comision_usd_por_lote` = `"2.50"`, CONFIRMED
(`knowledge/cuentas/ftmo-2step-swing-100k.yaml:382-384`), y `firma_comision_por_lado` = `true`, CONFIRMED
(`:401`, `:412-413`): ADR-0090 §3. El bróker las lee por su nombre (`simulacion.py:140-141`) y la cuenta
carga la comisión al llenar y, por lado, al cerrar (`cableado.py:530-537`).

**d) Recuentos de partida**, por la compuerta del arnés (`arnes.dias_de_construccion`,
`arnes.py:139-173`), con un guion de la carpeta de trabajo que no imprime ninguna clave reservada:

| mes | días dev | días sin operaciones | operaciones del trader | sin stop |
|---|---|---|---|---|
| 2026-04 | 21 | 5 | 35 | 0 |
| 2026-07 | 13 | 0 | 67 | 0 |
| 2026-08 | 21 | 2 | 42 | 0 |
| 2026-01 | 21 | 0 | 54 | 0 |
| total | **76** | 7 | **198** | **0** |

76 días y 198 operaciones, los de la última cuenta (RECORRIDA-CONSTRUCCION-2.md §1.1; NOTA del
2026-11-08 de ADR-0070 §3); `git log stable/F38t-recorrida-construccion-2..main -- knowledge/cases/dev
knowledge/cases/criterio_fidelidad.yaml` sale vacío (auditor). `casos_reservados(repo)`: 34 en total, 0
en cada uno de los cuatro meses de construcción; `casos_ocultos(repo)`: 34, 0 en los cuatro; ninguno de
los 76 días dev leídos está en ninguno de los dos.

**e) Los guiones de `main`, sobre la salida de hoy** (`data/activar-sesion-08/julio-f2.txt`, que sigue en
la laptop), desde su sitio y sin copiarlos, con su salida a la carpeta de trabajo:
- `anexos/RECORRIDA-CONSTRUCCION-2/patrones.py <julio-f2.txt> --filas` (con el `sed` del CRLF): exit 0;
  **idéntico byte a byte** (`cmp`) a `data/activar-sesion-08/patrones-julio-f2.txt`. 87 filas, 25
  sesiones con rn003; julio T0 10, P5 18, P6 2.
- `anexos/PREPARACION-SESION-7/pivote_julio.py <patrones-julio-f2.txt>`: exit 1 («NO CUADRA: no son 14 y
  39», que no es un fallo) y la misma salida que `anexos/ACTIVAR-SESION-08/pivote-julio-f2.txt` (T0 10,
  operaciones de más 20). Filtra 2026-07 (`pivote_julio.py:16-25`): lee igual una salida de los cuatro
  meses.
- `anexos/ACTIVAR-SESION-07/delta_julio.py` (f2 contra sí misma, cuatro argumentos): exit 0; 87 filas en
  una y otra, ningún cambio. Filtra 2026-07 (`delta_julio.py:26`).
- `anexos/RECORRIDA-CONSTRUCCION-2/resumen_corrida.py <julio-f2.txt>`: exit 0.
- `anexos/RECORRIDA-CONSTRUCCION-2/para_clasificar.py <julio-f2.txt> <julio-f2.txt>`: exit 0, y su
  comprobación contra la cascada de cada salida «coincide». Pide DOS salidas, la corrida 1 y la 2
  (`para_clasificar.py:8-10`, `:415`): en la fase 2 serán `cuenta-por-mes.txt` y la diaria.
- `anexos/RECORRIDA-CONSTRUCCION-2/diff_por_seccion.py <julio-base.txt> <julio-f2.txt> <diff>` (el `diff`
  de las dos, a la carpeta de trabajo): exit 0; 619 líneas en una y otra, 166 quitadas y 166 puestas,
  repartidas por sección.
- Su test de humo, desde su sitio:

  ```
  $ uv run pytest docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/test_humo.py -p no:cacheprovider
  21 passed in 0.44s
  ```

Todos leen la salida de hoy. **Pero `para_clasificar.py` choca con D14**: su último bloque, «Resumen de
la lista anterior, por mes», imprime por mes la **suma del R neto** de las órdenes del bot sin trader
(`para_clasificar.py:389-404`), y su lista, el R neto de cada una (`:374`). Es un R de una clase de
órdenes (las de un día, sesión y dirección sin operación del trader), por mes, que no es ninguna línea
por cuenta del arnés, y ADR-0098 §4 c) dice que en la corrida (3) no se calcula ni se imprime. Es la
decisión 0 (§0.5): hasta tu respuesta no lo corro sobre las corridas de esta rama. `resumen_corrida.py`
imprime por mes el PnL neto en USD de las posiciones («Posiciones, por mes»), que no es un R y es lo
que ya dicen los saldos de cada cuenta: lo corro y lo digo.

**f) La factibilidad de ADR-0098 §1, pieza a pieza. CUADRA: todo se puede hacer sin tocar `src/`.**

*Lo que se llama suelto, sin reescribirlo:*
- El bróker simulado y su orden stop: `Broker` (`src/botsito/engine/broker.py:364`), `colocar_stop`
  (`:477-492`), `avanzar` (`:764`), `mover_stop` (`:691`), `cerrar_a_mercado` (`:644`), `cancelar`
  (`:633`), `precio_de_conversion` (`:1025`) y `margen_libre` (`:1065`). La comprobación de lado:
  `lado_equivocado_al_colocar` (`:558-571`), la misma con la que el bróker rechaza (`_precio_infringido`,
  `:573-591`). La espera de ADR-0097 vive en el cableado, antes de enviar
  (`primitivas_broker.py:665-682`), y **no se aplica al trader**: §1 dice que con el precio ya del otro
  lado la orden es «no colocable» (auditor, #43).
- Lo que el bróker y la cuenta necesitan, con los mismos valores que la corrida:
  `construir_motor_cableado` (`cableado.py:702-758`) da los mercados de los días dev (M1 y ticks, por la
  compuerta), las reglas del bróker con el calendario de cierres, las de la fase, la configuración del
  llenado y el contrato, sin correr nada y **sin calentamiento**: el calentamiento del sesgo lo hace
  `arnes.dias_de_mercado`, que el guion no llama. Los límites de cada sesión salen de
  `reloj_de_las_sesiones(registro).limites_de_sesiones` (`src/botsito/engine/motor.py:189-192`), sin velas.
- `CuentaViva` (`src/botsito/engine/cuenta.py:391`) y su curva por día, `cerrar_dia_en_curso` (`:543`), la
  que usa la corrida (`cableado.py:654-659`); `reglas_de_fase` (`cuenta.py:118-152`). La fase solo cambia
  el objetivo y los días mínimos (`cuenta.py:124-133`); los límites son del perfil (`:143-147`). La
  cuenta sigue tras SUSPENDIDA, que es una marca y no corta (`cuenta.py:479-484`): el trader sigue
  operando y f) lo dice, como pide §1.
- El paso de los eventos del bróker a la cuenta (apertura, comisión al llenar y al cerrar, swaps,
  cierre): `MotorCableado._a_la_cuenta` (`cableado.py:506-560`), llamado con un objeto que lleva solo lo
  que lee (`cuenta`, `reglas_broker` y `racha` en `None`: la racha es de RN-036, regla solo del bot). El
  PnL bruto, la comisión, los swaps, el neto y el riesgo de cada posición: `posiciones_del_bot`
  (`cableado.py:1323-1372`), el mismo cálculo que imprime «### Posiciones».
- El tope del lote: `limitar_lote` (`broker.py:188-221`), con `lote_si_no_cabe` = `limitar`,
  `lote_margen_libre_fraccion` = 0,95 y paso y mínimo de 0,01 (CONFIRMED).
- La zona del break even: `zona_posterior_completada` (`src/botsito/domain/estructura_m1.py:263`) con
  `break_even_criterio_ruptura` = `cuerpo` y `break_even_condicion` = `cierre` (CONFIRMED): con `cierre`
  el stop se mueve en el cierre de la M1, sin vigilancia al tick (`cableado.py:422-426` solo vigila con
  `tocar`).
- El cierre forzoso: los predicados de RN-002, `vence_vela_h4` y `alcanza_hora`
  (`src/botsito/engine/primitivas.py:154-163`, `:195-200`), de `primitivas_escritas(registro)`; solo leen
  el instante y el registro (`anclaje_h4` 17:00, `cierre_h4_antelacion` 1, `ventana_fin` 15:00,
  `reloj_sesiones` = `rejilla_h4`).
- El redondeo «alejándose de la entrada»: `REDONDEO_DEL_STOP` (`primitivas_broker.py:93`), con
  `stop_fraccion_redondeo` = `alejandose_de_la_entrada` (ROUND_UP) y `stop_fraccion_caja` = 0,8.
- Las cifras: `r_neto`, `esperanza_r`, `remuestreo_por_dias`, `perdida_diaria_maxima`,
  `equity_minima_del_tramo`, `medir_por_cuentas` y `punto_de_equilibrio` (`criterio_fidelidad.py:582`,
  `:588`, `:611`, `:657`, `:670`, `:696`, `:869`), con las réplicas (10.000), la semilla (20261107) y el
  percentil (5) del bloque `rentabilidad` (`criterio_fidelidad.yaml:66-80`).

*Lo que vive dentro del intérprete y se reproduce en el guion* (vale solo si pasa el control):
- El dimensionado: `_lote_resuelto` (`primitivas_broker.py:612-628`: saldo × riesgo / distancia hasta el
  stop, con `lotaje_base` = `hasta_stop_fraccion`, `base_calculo_riesgo` = `saldo_actual`,
  `riesgo_por_operacion` = 0,5), `redondear_lote` (`:523-537`, hacia abajo al paso), `_lote_final`
  (`:551-575`, `limitar_lote` con el margen libre por 0,95 al precio de conversión del instante) y el «no
  se coloca» por debajo del mínimo (`:651-662`).
- El objetivo: `fijar_objetivo` (`:499-521`): `objetivo_rr` = 3 sobre `base_calculo_objetivo` =
  `caja_completa`, hacia abajo al punto.
- La gestión del break even de la posición viva: `se_completa_zona_de_control` con `posterior_a`
  (`:286-308`: las M1 cerradas desde `minuto_de_apertura`, y SI en el cierre de la M1 que pasa el punto)
  y `mover_stop` a la entrada (`:811-822`).
- El cierre forzoso (`cerrar_a_mercado`, `:709-719`) y el bucle del día con su cierre de fin de día
  (`cableado.py:396-468`; el fin de día, `:457-468`).

*El trader, por la vía de la ingesta:* `arnes.dias_de_construccion` (`arnes.py:139-173`) da por cada
operación dev su día, sesión, dirección, instante, entrada y stop (`_operacion`, `arnes.py:124-136`);
ninguna columna de resultado, ningún xlsx. Ninguna de las 198 viene sin stop (punto d).

*T0 y «### Posiciones»:* la fila T0 de `patrones.py --filas` trae el día y, del bot, el instante del
llenado y la entrada («PAREJA bot <instante> <entrada>»), que son las columnas «llenada UTC» y «entrada»
de «### Posiciones». Medido sobre la línea base anterior: las 31 filas T0 casan cada una con **una sola**
posición cerrada, y ninguna posición repite (día, llenado, entrada).

*Los motivos de cierre de «### Posiciones»:* `stop`, `objetivo` y `manual` (`cableado.py:1312`). En la
línea base anterior: 210 `stop`, 32 `objetivo` y 5 `manual`, y los 5 `manual` en un cierre de M1 en que
`vence_vela_h4` o `alcanza_hora` dan SI (RN-002): **entran en el control**. Un `manual` fuera de ese
instante solo puede venir de una regla solo del bot (RN-030 cierra a mercado; ADR-0098 §1) y queda
fuera, contado con su instante.

*La diferencia emparejada:* `remuestreo_por_dias` (`criterio_fidelidad.py:611-646`) solo lee de cada
posición su `dia` y su `r_neto` = `pnl_neto / riesgo` (`:582-585`): una `PosicionCerrada` con `pnl_neto`
igual a la diferencia y `riesgo` 1 da esa diferencia (los otros campos de `PosicionCerrada` no los lee).
El percentil 95 sale de la misma función con `percentil=95` (índice `floor(95 (n − 1) / 100)` sobre las
medias ordenadas); el 5 y el 95 son dos llamadas con la misma semilla.

*Los rechazos al colocar y cómo caen en §1:*
- `precio_invalido` (el lado): **no colocable**; el guion lo mira antes con `lado_equivocado_al_colocar`,
  la misma comprobación, y no envía nada;
- `stops_level`: el perfil lo fija en 0 (A-27, ADR-0071): no rechaza nunca;
- `cierre_mercado` y `cierre_sin_calendario` (ADR-0068, `broker.py:441-456`), `freno_*` (R13,
  `src/botsito/engine/freno.py:40-42`), `volumen_max_lotes`, `ordenes_simultaneas_max` y
  `posiciones_dia_max` (`broker.py:1114-1130`) y `margen_libre` (`:536-540`): **rechazada por el bróker**,
  con su motivo;
- al llenar, `margen_libre` (`broker.py:880-899`): rechazada por el bróker, con su motivo.

*La caja 1 de cada orden del bot:* «### Ordenes» la trae en su última columna («caja 1»), con la entrada
(«precio»), la distancia al stop en puntos y el lote (cabecera de la línea base anterior, su línea 1996).

*Lecturas que hago donde §1 no lo dice con todas las letras* (no cambian ninguna pieza; si no las quieres
así, dímelo en la respuesta):
- **El control coloca cada orden del bot en su instante real** («colocada UTC» de «### Ordenes»), no en el
  cierre de la M1 anterior al llenado, que §1 fija para el trader: el lote del bot, cuando muerde el
  margen, depende del precio de conversión de ese instante (`primitivas_broker.py:562-564`), y
  reproducirlo al céntimo lo exige. La regla de colocación del trader se ejerce en el techo, no en el
  control.
- **Con dos posiciones del trader vivas a la vez, el break even se mira en cada una**, con su propia zona
  posterior. El predicado del bot pide una sola posición viva (`primitivas_broker.py:287-289`) porque el
  bot no puede tener dos (RN-011 y RN-018); el guion dirá cuántas veces pasa.
- **«No llenada en la sesión»**: la orden se cancela al terminar la sesión de la operación (sus límites,
  por la puerta del reloj). No se aplica ninguna otra regla de retirada (RN-035), como dice §1.

**g) Herencias** (grep sobre las rutas literales del encargo y el auditor). Entran:
- la F de la Next Action (`PROJECT_STATE.md:28`): «(3) la corrida de ADR-0070 §3 y la lectura del
  pivote…, los frenos de la cuenta como están (su efecto por sesión de julio, como dato); A-43…: si no
  contesta antes, (3) corre con el valor de hoy… R5.7 después de (3)». §7 la reescribe;
- R4.3 (`docs/plan/HOJA-DE-RUTA.md:383-389`): su «Hecho cuando» («7a y 7b ingeridas y activadas, y el
  pivote leído en la re-corrida siguiente») se cumple al leer el pivote; **pasa a HECHA y entonces no
  puede llevar `NA:F` en sus Refs** (`test_hoja_de_ruta.py:177`; la F sigue viva en R4.2 y R4.6;
  auditor, herencia 6). El encargo pide «R4.3 con el pivote leído»; §7 lo prepara así;
- R4.6 (`:417-420`): «Hecho cuando» añade «o la lectura de ADR-0098 cambia el objetivo» (§7);
- R5.7 (`:489-497`): la sustituye ADR-0098 (§7);
- R5.2 (`:440-444`): «Depende de» pasa de R3.9 a R3.10 (§7);
- R5.6 (`:485`), «la re-corrida que cuenta, con su línea «habilita medir» en sí»: no cambia; ADR-0098 §3
  A la nombra solo si sale A;
- el Marcador de la hoja de ruta: una fila nueva (§7);
- `docs/validation/ACTIVAR-SESION-08.md:701-716`, «Para la corrida de (3)»: lo único que cambió en el
  motor (F2), las tensiones (D8) y, con sus palabras, las filas de julio que cambian entre la corrida por
  mes y la diaria y qué freno lo explica (D6);
- la línea de Technical Debt de D7 (`PROJECT_STATE.md:159`).

No entran: E21 (`ACTIVAR-SESION-08.md:717-718`), que va a la rama del margen del break even; y la NOTA
de ADR-0070 no es de la fase 0 (D3, tras la fase 2).

**h) La fila del día, antes del primer `make check`.** La fila de HOLDOUT-EXPOSICIONES del 2026-11-22
para esta rama se escribió y estadió a las 14:32:37 (hora local, `date` justo después de `git add`),
tras crear la rama y antes de cualquier lectura de material, clon o `make check`. El primer `make check`
(el de la apertura) imprimió `G2: fila de HOLDOUT-EXPOSICIONES del 2026-11-22 para
trabajo/recorrida-construccion-3, estadiada` y selló el árbol `deb20421…`; el commit de apertura,
`3457fb31`, es de las 15:12:55.

**i) Tiempo y memoria.** La corrida que cuenta de RECORRIDA-CONSTRUCCION-2 dio 339,5 s y 635,6 MiB (la de
LAMINAS, 321,7 s y 640,0 MiB, sin contar); cada `make check` de esta rama dura unos 27 minutos (1625,67 s
y 1612,29 s de tests en los dos primeros; 318 y 319 MiB de pico). Tres corridas, el guion de la meta (del
orden de una corrida: los mismos días, ticks y bróker, sin intérprete) y unos siete `make check`: cabe en
una sesión, con los `make check` como cuello.

**j) La premisa de D5.** `7592c73e` es «feat(orden): la stop cuyo 0 queda del lado malo espera (F2,
ADR-0097, A-59)», y ACTIVAR-SESION-08.md:509 dice que julio-f2 corrió sobre él. `git diff --stat 7592c73e
main -- src/ knowledge/spec/ knowledge/cuentas/`: **nada en `src/` ni en `knowledge/cuentas/`**; en
`knowledge/spec/`, `ambiguedades.yaml` (29 líneas), `parametros.yaml` (72) y `spec_manifest.yaml` (19.1.0
→ 19.1.5). En `parametros.yaml` ninguna línea `valor:`, `estado:`, `opciones:`, `nombre:` ni `tipo:`
cambia: son descripciones, de los commits de la propia rama `cb02d3a9`, `46028e24`, `a34d7ecc` y
`62a4152f` (no del cierre). El motor que decide es el de julio-f2. Y julio-f2 se corrió con `--meses
2026-07`, la corrida 1 sin `--meses`: que con una cuenta por mes julio empiece igual lo midió el recuadro
de ADR-0093 §4 (`0093:126-128`: «con `--meses 2026-07` reproduce, 106 filas idénticas»).

### §0.4 El encargo frente al repo (auditor y lo medido)

El subagente `auditor-encargo` contrastó 54 afirmaciones: 41 correctas, 1 incorrecta y 12 con matiz,
más 10 herencias o choques. Lo que cambia algo:

1. **INCORRECTA, D10: «un rechazo de ADR-0097».** ADR-0097 no rechaza: la stop del lado malo no se envía
   y espera (`docs/adr/0097-la-orden-cuyo-0-queda-del-lado-malo-espera.md:24-30`). Su rastro en la salida
   es la sección «### Esperas» (`cableado.py:997`) y que desaparecen los rechazos por `precio_invalido`
   (en julio, de 5 a 0: ACTIVAR-SESION-08.md:525). **Gana la medida:** en D10 atribuyo a la 7b una espera
   de «### Esperas» o un `precio_invalido` que desaparece, y lo digo con su nombre. No paro por esto: es
   la evidencia que D10 pide, con su forma real.
2. **D3 y D6 («bloqueada por RN-032», «qué freno lo explica»).** La lección que más se ha repetido en
   estas corridas (ERRORES-RECURRENTES.md, fila de `trabajo/recorrida-construccion-2`, lección 5): el
   `prohibida:abrir_operacion` de RN-015 no nombra el gate. Atribuyo a RN-032 o a RN-036 solo lo que dice
   la columna `bloqueadas regla:accion:motivo` de «## Por sesion» (`arnes.py:260-265`, `:339-340`) o el
   primer toque de la cuenta; lo demás, «sin atribuir».
3. **D7, «cuántos caen en un día o en una hora sin ticks»**: la salida no lista las horas perdidas;
   salen del punto b (las 18 horas, por manifiesto) y se cruzan con las filas «rechazada» de
   «### Ordenes». `horas_perdidas.py` (anexos de RECORRIDA-CONSTRUCCION-2) es la copia de `main` que lo
   hace igual.
4. **D9: `para_clasificar.py` pide la corrida 1 y la 2**, no solo la 1 (arriba, e).
5. **D8: «lo único que cambió desde la corrida anterior de julio es `orden_stop_lado_malo`».** Es cierto
   frente a la `base` de ACTIVAR-SESION-08; frente a julio-f2 no cambió nada que decida (punto j).
6. **D3: lo que entró en el motor desde la línea base anterior.** Además de la 7a (F39e) y la 7b (F39k),
   tocaron `src/` o la spec tres merges que repitieron la línea base a 0 bytes: `trazas-ablacion`
   (76bbe099), `laminas` (b9904c54) y `laminas-motivos` (7d3002c8) (PIVOTES-SESION-7.yaml, `lo_visto`).
   La NOTA lo dirá. Y el break even de la 7a es «al cierre y con cuerpo».
7. **D4: la contingencia.** Su texto es del 2026-11-11 (ADR-0093 §6 y el yaml); del 2026-11-19 es la
   decisión de aplicarla sin retocarla. «Contra los mismos mínimos» y «sin mezclar» solo están en R4.3.
8. **PROJECT_STATE: 24.669 bytes es `main`; la rama lleva 24.801** (la línea de Current Feature). El tope
   es estricto (`test_project_state.py:21`, `:52`). §7 mide en la forma que escribirá el ritual (cabeceras
   del cierre, sin la Current Branch de la rama) y da las dos cifras.
9. **Fase P antes del auditor** (choque con `fase-cero`): §0.2.
10. **`entregar-rama` paso 3**: un test que rompe a propósito se demuestra fallando con el código de
    `main`. `test_meta_techo_parejas.py` no existe en `main` y su yaml tampoco; lo demuestra la entrega.
11. **Fixtures sintéticas** del test de humo nuevo con fechas de días dev o de 2030, nunca de meses con
    reservados, y `antes_del_dia.py` también sobre los `.py` y el informe (lección 6 de la misma fila);
    **la cadena de carga del test de humo, en tres niveles como mucho** (lecciones 1 y 7).

Lo demás del auditor, correcto o con un matiz que no cambia nada (la CI con `gh run view` frente a la API
de check-runs; que «evidencia inmutable» de la línea base anterior lo sostienen el contrato y ADR-0070, no
un régimen de CLAUDE.md), queda en su informe; las cifras que verificó con fuente están en a) a j).

### §0.5 Lo que necesito que decidas (PARADA condicional)

Todo lo demás de D1 a D14 cuadra con lo medido, y la rama sigue a la fase 1 sin esperarte (el encargo:
«si algo no cuadra, paras SOLO en eso, sigues con lo demás»).

0. **`para_clasificar.py` sobre las corridas de (3) (D9 frente a D14).** Su resumen final imprime por mes
   la suma del R neto de las órdenes del bot sin trader, y su lista el R neto de cada una: un R de una
   clase de órdenes por mes, que ADR-0098 §4 c) no deja calcular ni imprimir en la corrida (3).
   Opciones: (a) no correrlo sobre las corridas de esta rama, y D9 lleva solo los patrones de las dos
   corridas; (b) correrlo tal cual y commitear su salida entera, porque el encargo lo pide y el R por
   orden ya lo imprime el arnés en «### Posiciones»; (c) un guion nuevo en esta carpeta que dé la lista
   sin el R (la lista es la materia de R4.6; el R no hace falta para clasificar). Recomiendo (c): da a
   la sesión siguiente lo que pide D9 sin el R que prohíbe §4 c), y `para_clasificar.py` de `main` no se
   toca. Coste de (b): una salida con R por clase en la rama que pre-registra no hacerlo. Hasta tu
   respuesta, no lo corro.

### §0.6 Lo que no pude medir

- Que la guardia deje lanzar los tres comandos de la fase 2 desde la sesión: solo se sabe al lanzarlos;
  si niega alguno, PARADA con el comando y lo lanza Aleks con «!».
- Cuántas veces el trader tiene dos posiciones vivas, cuántas órdenes no son colocables o no se llenan:
  lo dice el guion de la fase 4, sin R.

### §0.7 Exposiciones declaradas

La fila del 2026-11-22 de `docs/validation/HOLDOUT-EXPOSICIONES.md`, escrita y estadiada antes del
primer `make check`. La fase 0 leyó lo que esa fila declara (puntos 1 a 5): el M1 de marzo y el de junio
en cada `make check`; los dos ficheros del Escritorio; `casos_reservados` y `casos_ocultos` por
recuento; los casos dev de los cuatro meses por la compuerta del arnés (día, sesión, dirección, instante,
entrada y stop); los manifiestos y los ticks de los 76 días dev (sin calentamiento); las salidas de días
dev de `data/activar-sesion-08/`; y el auditor, que leyó solo el repo.

### §0.8 La fase 1 (el README y el guion de la meta, antes de correr)

- `docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/README.md`, en su propio commit (`c5bdad44`,
  17:02:54), antes de correr: qué es cada fichero y los comandos literales.
- `anexos/RECORRIDA-CONSTRUCCION-3/techo_parejas.py`, con los tres modos (`control`, `techo` y `parejas`;
  los tres corren antes el control y salen con 4 si no pasa). Lee `META-TECHO-PAREJAS.yaml`,
  `PIVOTES-SESION-7.yaml` y `criterio_fidelidad.yaml` y escribe él mismo la lectura del techo, la de las
  parejas, la salida A a D y la precedencia con el pivote (que lee de `pivote-julio.txt` y de los mínimos
  del yaml del pivote). Su docstring dice pieza a pieza el modelo de ADR-0098 §1, lo que llama suelto del
  motor (§0.3 f) y lo que reproduce. No imprime ninguna operación del trader con su R ni ningún R por
  clase, sesión o dirección; por mes, solo d), e) y f) por cuenta, y julio entero como diagnóstico.
- Lo que el guion hace donde §1 no lo dice con todas las letras, las tres lecturas de §0.3 f), y dos
  más: el R del bot de cada pareja sale de la repetición del control (exacta y verificada al céntimo con
  «### Posiciones»), no de la columna redondeada; y un `manual` fuera del control se cierra a mercado en
  su instante, para que la cuenta del mes siga igual.
- `test_techo_parejas.py`, su test de humo sobre datos sintéticos (fechas de 2030): una salida A, una B,
  una C y una D construidas a mano; las fronteras en el otro sentido; el control que falla con un
  céntimo y con una posición de más o de menos; el remuestreo de la diferencia frente a su cuenta a mano
  (un día; tres días con 50 réplicas, repitiendo el sorteo); la caja derivada, el objetivo, el lote y la
  salida del pivote. `make check` no lo recoge:

  ```
  $ uv run pytest docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/test_techo_parejas.py -p no:cacheprovider -v
  14 passed in 0.61s
  ```

  `ruff format` (2 sin cambios), `ruff check` («All checks passed!») y `mypy` («no issues found in 2
  source files») sobre los dos.
- **El ensayo del control sobre `data/activar-sesion-08/julio-f2.txt`** (el motor de hoy, julio; declarado
  en la fila complementaria del día), solo el modo `control`: 30 posiciones del bot, 30 en el control,
  ninguna fuera, **30 de 30 reproducidas al céntimo**, «control: PASA». El primer intento se paró al
  leer «### Ordenes», que acaba en una línea de resumen; se arregló la lectura (un error de programación
  del guion, no una pieza del modelo) y el segundo dio lo de arriba.

## §1 · La corrida 1, la que cuenta (D1, D2, D6, D7 y D8)

**Comando** (desde la raíz, sobre `bca9ba20`, en segundo plano, sola): `uv run botsito motor arnes
--simular --salida docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/cuenta-por-mes.txt`. Empezó a las
**17:39:11** (`date` justo antes), una hora y cincuenta minutos después del pre-registro (`539f7983`,
15:49:25). Exit 0:

```
OK: informe del arnes en docs\validation\anexos\RECORRIDA-CONSTRUCCION-3\cuenta-por-mes.txt
TIEMPO: 345.7 s; MEMORIA: pico del proceso de 638.5 MiB
```

Sin `--meses`; ningún rótulo DIAGNOSTICO en la corrida (las dos apariciones de la palabra son los
títulos de «### Material sin video» y «### Rentabilidad» de la sección del método, como en la línea base
anterior). `## Simulacion`: «PERFIL: ftmo-2step-swing-100k; FASE: reto», «DIAS CORRIDOS: 76», «CUENTA:
UNA POR MES (ADR-0092 §8): 4 cuentas». D12: ni 20 minutos ni 1,5 GiB.

**D1, el veredicto, literal:**

`habilita medir el conjunto de medida (2026-05) (ADR-0070): no (cobertura 15.2 % por debajo de 70.0 %; precision 14.4 % por debajo de 60.0 %)`

Por ADR-0070 §4, se sigue construyendo y mayo no se toca. **D2:** `cuenta-por-mes.txt` es la línea base
vigente tal como queda en anexos, sin copia; la de `anexos/RECORRIDA-CONSTRUCCION-2/` no se toca. **D11:**
la corrida repetida fuera del repo (la 3) sale **idéntica byte a byte** (§2).

**En total y por mes** (líneas literales de «## Criterio de fidelidad» y «### Resumen por mes»):
operaciones del trader 198; del bot puntuables 208; del bot en días sin operaciones del trader 27;
cobertura 30/198 (15.2 %); precisión 30/208 (14.4 %); parejas en el mismo minuto 18.

| mes | días | trader | bot puntuables | bot en días sin trader | parejas | cobertura | precisión |
|---|---|---|---|---|---|---|---|
| 2026-04 | 21 | 35 | 55 | 17 | 10 | 10/35 (28.6 %) | 10/55 (18.2 %) |
| 2026-07 | 13 | 67 | 30 | 0 | 10 | 10/67 (14.9 %) | 10/30 (33.3 %) |
| 2026-08 | 21 | 42 | 46 | 10 | 5 | 5/42 (11.9 %) | 5/46 (10.9 %) |
| 2026-01 | 21 | 54 | 77 | 0 | 5 | 5/54 (9.3 %) | 5/77 (6.5 %) |

**La cascada por criterios** (ADR-0092 §2; «diagnostico de construccion, sin umbral»), literal:

| mes | sin orden del bot en su (día, sesión, dirección) | orden, entrada fuera de tolerancia | entrada, stop fuera de tolerancia | entrada; el caso no trae stop | en el nivel, no llenada | en el nivel, llenada fuera de tolerancia de instante | las cuatro piezas | total |
|---|---|---|---|---|---|---|---|---|
| 2026-01 | 14 | 23 | 15 | 0 | 1 | 0 | 1 | 54 |
| 2026-04 | 5 | 15 | 9 | 0 | 1 | 0 | 5 | 35 |
| 2026-07 | 32 | 20 | 9 | 0 | 0 | 1 | 5 | 67 |
| 2026-08 | 19 | 15 | 4 | 0 | 1 | 0 | 3 | 42 |
| total | 70 | 73 | 37 | 0 | 3 | 1 | 14 | 198 |

«ordenes del bot en un (dia, sesion, direccion) sin ninguna operacion del trader: 321».

**Los bloques por cuenta** (literal; lo «DERIVADO» es de `resumen_corrida.py`, anexo
`resumen-cuenta-por-mes.txt`): las cuatro **EN_CURSO**, «PRIMERO EN TOCAR UN LIMITE: ninguno»; ninguna
SUSPENDIDA.

| cuenta | saldo final | días de trading | racha de RN-036 al cerrar | equity mínima (derivada) | peor pérdida diaria (derivada) |
|---|---|---|---|---|---|
| 2026-01 | 90951.46 | 20 | 3 seguidas; la última el 2026-01-29 | 90,95 % (2026-01-29) | 4,35 % (2026-01-13) |
| 2026-04 | 103245.00 | 21 | 0 seguidas; la última el 2026-04-28 | 99,05 % (2026-04-01) | 2,29 % (2026-04-10) |
| 2026-07 | 90633.16 | 8 | 6 seguidas; la última el 2026-07-10 | 90,63 % (2026-07-10) | 2,50 % (2026-07-06) |
| 2026-08 | 90922.26 | 16 | 2 seguidas; la última el 2026-08-26 | 90,92 % (2026-08-26) | 2,71 % (2026-08-18) |

**Las peticiones** (R13; `resumen-cuenta-por-mes.txt`): 611, 561, 220 y 479 en enero, abril, julio y
agosto (1.871 en total), con un máximo diario de 68; «El freno de peticiones (ADR-0067)»: «ningun aviso
ni ninguna peticion negada»; «Los cierres de mercado (ADR-0068)»: «ninguna peticion negada ni ninguna
pendiente cancelada»; «Ordenes no enviadas por el bot»: ninguna.

**La sección «## El metodo de ADR-0092»** (líneas literales, con su marca DIAGNOSTICO):

```
### Material sin video (ADR-0092 §11; DIAGNOSTICO, ningun umbral lo lee)
operaciones del bot quitadas (break_even en un dia sin video): 42
esperanza sin ellas (media del R neto, 193 operaciones): -0.443
### Rentabilidad (ADR-0092 §3; DIAGNOSTICO sobre construccion, ADR-0092 §6: la puerta solo se mide sobre 2025-06, 2025-07, 2025-08, 2025-09, 2025-10, 2025-11, fase fondeada)
FASE de esta corrida: reto
a) N (operaciones llenadas y cerradas): 235
b) esperanza (media del R neto): -0.429
c) percentil 5 de la media del R neto, por remuestreo por dias (10000 replicas, semilla 20261107, 76 dias): -0.651; replicas descartadas por no tener ninguna operacion: 0 de 10000
d) perdida diaria maxima (equity, base saldo_corte_diario), por cuenta: 4.35 % del capital inicial; la peor, la cuenta de 2026-01
e) equity minima, por cuenta: 90.63 % del capital inicial; la peor, la cuenta de 2026-07
f) alguna cuenta entro en SUSPENDIDA: no
criterios a) a f): no pasa (b) esperanza -0.429 por debajo de 0.10 R; c) percentil 5 del remuestreo -0.651, no mayor que 0; d) perdida diaria maxima 4.3 %, en o por encima de 3.0 %; e) equity minima 90.6 %, por debajo de 94.0 %)
deslizamiento por llenado afectado que lleva la esperanza a 0.10 R (ADR-0092 §4, sin decidir nada): -3.65 puntos
```

Diagnóstico de construcción (ADR-0092 §6): nada de aquí justifica una rama.

### §1.1 D6, los frenos de la cuenta, como dato y sin umbral

Con `anexos/RECORRIDA-CONSTRUCCION-3/frenos_julio.py` (nuevo; solo lee la corrida 1 y el delta de julio
entre ella y la diaria, `delta-julio-cuenta-por-mes-diaria.txt`) → `frenos-julio.txt`. El freno se nombra
solo si **dispara en esa sesión** de la corrida 1 (la columna «disparadas» de «## Por sesion»): la línea
`RN-015:accion:colocar_orden_limite:prohibida:abrir_operacion` de «bloqueadas» no nombra el gate (lección
5 de la fila de `trabajo/recorrida-construccion-2` en ERRORES-RECURRENTES) y sale en las 25 sesiones de
julio, con freno o sin él.

| sesión de julio | trader | bot (corrida 1) | filas que cambian a la diaria | freno que dispara en la corrida 1 |
|---|---|---|---|---|
| 2026-07-01 07-11 | 2 | 1 | 0 | ninguno |
| 2026-07-01 11-15 | 1 | 2 | 0 | ninguno |
| 2026-07-02 11-15 | 6 | 5 | 0 | ninguno |
| 2026-07-03 07-11 | 2 | 1 | 5 | RN-036 |
| 2026-07-03 11-15 | 1 | 0 | 2 | RN-036 |
| 2026-07-06 07-11 | 4 | 4 | 0 | ninguno |
| 2026-07-06 11-15 | 1 | 1 | 0 | ninguno |
| 2026-07-07 07-11 | 4 | 3 | 0 | ninguno |
| 2026-07-07 11-15 | 4 | 2 | 0 | ninguno |
| 2026-07-08 07-11 | 1 | 2 | 0 | ninguno |
| 2026-07-08 11-15 | 1 | 0 | 0 | ninguno |
| 2026-07-09 07-11 | 1 | 2 | 0 | ninguno |
| 2026-07-09 11-15 | 1 | 1 | 0 | ninguno |
| 2026-07-10 07-11 | 8 | 4 | 2 | RN-032 |
| 2026-07-10 11-15 | 3 | 0 | 3 | RN-032 |
| 2026-07-13 07-11 | 1 | 0 | 2 | RN-032 |
| 2026-07-13 11-15 | 3 | 0 | 6 | RN-032 |
| 2026-07-14 07-11 | 2 | 0 | 2 | RN-032 |
| 2026-07-14 11-15 | 6 | 0 | 8 | RN-032 |
| 2026-07-15 07-11 | 2 | 0 | 5 | RN-032 |
| 2026-07-15 11-15 | 4 | 0 | 5 | RN-032 |
| 2026-07-16 07-11 | 1 | 0 | 1 | RN-032 |
| 2026-07-16 11-15 | 3 | 0 | 6 | RN-032 |
| 2026-07-17 07-11 | 4 | 0 | 5 | RN-032 |
| 2026-07-17 11-15 | 1 | 0 | 2 | RN-032 |

54 filas cambian (34 de patrón y 20 que aparecen; ninguna desaparece), **todas** en las 14 sesiones en que
dispara un freno de la cuenta en la corrida 1, y ninguna en las 11 sin freno. En la cuenta diaria la
racha y la pérdida total empiezan de cero cada día.

**La primera sesión con freno de cada cuenta mensual de la corrida 1**, y el saldo al corte de ese día
(curva por día del bloque de la cuenta):
- 2026-01: 2026-01-13 11-15 (RN-032); saldo al corte 105043.10;
- 2026-04: ningún freno de la cuenta dispara en una sesión con operaciones del trader;
- 2026-07: 2026-07-03 07-11 (RN-036); saldo al corte 96308.41; RN-032, desde 2026-07-10 07-11 hasta el 17
  (saldo al corte del 10: 92374.52), y el bot no llena ninguna orden desde 2026-07-10 11-15;
- 2026-08: 2026-08-20 07-11 (RN-036); saldo al corte 93007.08; RN-032, del 2026-08-26 al 31.

RN-032 dispara en 25 de las 152 sesiones (23 de las 104 con operaciones del trader) y RN-036 en 10 (7);
RN-020 en ninguna (`resumen-cuenta-por-mes.txt`).

### §1.2 D7, los rechazos por motivo y por día

**Ninguno.** «### Rechazos por motivo (mes | motivo | peticion | rechazos)»: «ninguno»; ninguna fila
«rechazada» en «### Ordenes» (resultados: cancelada 253, 229, 91 y 202; llenada 77, 72, 30 y 56). Así que
ninguno cae en un día o en una hora sin ticks (las 18 horas perdidas de §0.3 b). La línea base anterior
tenía 32, todos `precio_invalido` al colocar (8, 11, 9 y 4 por mes); con ADR-0097 esas órdenes no se
envían y esperan: «### Esperas» trae 25 (enero 3, abril 10, julio 6, agosto 6). Si la deuda de
Technical Debt sale o se queda lo decides tú en la PARADA final (§7 da los bytes con y sin ella).

### §1.3 D8, las lecturas DEFAULT_AMBIGUOUS con que corrió y las tensiones

Los diez parámetros DEFAULT_AMBIGUOUS de `knowledge/spec/parametros.yaml`, con su ambigüedad de
`knowledge/spec/ambiguedades.yaml`:

| parámetro | valor | ambigüedad |
|---|---|---|
| `sesgo_h4_rango_nuevo` | `vela_que_rompe_con_su_color` | A-58 |
| `liquidez_m15_mecha_que_vuelve` | `solo_la_contraria` | A-35 |
| `orden_stop_punto` | `ultimo_pivote_m1` | A-48 |
| `orden_stop_lado_malo` | `espera` | A-59 |
| `orden_pendiente_al_abrir_escenario` | `se_mueve` | A-53 |
| `freno_peticiones_aviso`, `freno_peticiones_corte`, `freno_bucle_repeticiones`, `freno_bucle_minutos` | 1000, 1500, 5, 1 | A-54 |
| `cierre_pendientes` | `cancelar` | A-55 |

Las tensiones, tal como las dejó ACTIVAR-SESION-08.md («Para la corrida de (3)»):
`toma_antes_de_la_ventana` = `cuenta`, CONFIRMED, frente al «no es válido» de la 7a (A-43); A-53
(`se_mueve`); A-35 sin respuesta; RN-019, que no dispara (no sale en «Reglas disparadas por sesion» de la
corrida 1); `orden_stop_punto` y `sesgo_h4_rango_nuevo` (A-48 y A-58); y los frenos de la cuenta (RN-032,
RN-036), que mide §1.1. Frente a julio-f2 no cambió nada que decida (§0.3 j); frente a la `base` de
ACTIVAR-SESION-08, solo `orden_stop_lado_malo` = `espera`. Aleks no trajo ninguna respuesta del trader a
A-43 ni a A-35 antes de la corrida 1.

## §2 · La corrida 2, de contexto (diagnóstico: no cuenta)

`uv run botsito motor arnes --simular --diagnostico-cuenta-diaria --salida
docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/diaria.txt`, exit 0, escribió **`diaria.DIAGNOSTICO.cuenta=diaria.txt`**:

```
OK: informe del arnes en docs\validation\anexos\RECORRIDA-CONSTRUCCION-3\diaria.DIAGNOSTICO.cuenta=diaria.txt
TIEMPO: 317.7 s; MEMORIA: pico del proceso de 644.2 MiB
```

Cada línea lleva el rótulo `[DIAGNOSTICO-CUENTA-diaria]`, y su veredicto dice «no (opción fuera de la
lista: --diagnostico-cuenta-diaria; cobertura 22.7 % …)». Cobertura 45/198 (22.7 %), precisión 45/276
(16.3 %); por mes: abril 10/35 y 10/55, julio 19/67 y 19/59, agosto 11/42 y 11/72, enero 5/54 y 5/90.
Rentabilidad (diagnóstico): N 303, esperanza −0.473, percentil 5 −0.659.

**La corrida 3** (la 1 repetida, D11): `uv run botsito motor arnes --simular --salida
<carpeta de trabajo de la sesión>/cuenta-por-mes-repetida.txt`, exit 0, «TIEMPO: 372.6 s; MEMORIA: pico del
proceso de 639.3 MiB»; `diff` contra la commiteada: exit 0, **idénticas byte a byte**. La copia se borró.

## §3 · El pivote de ADR-0093 §6 (D4 y D5)

**D5, el control de julio**, antes de leer el pivote:
`delta_julio.py data/activar-sesion-08/patrones-julio-f2.txt anexos/.../patrones-cuenta-por-mes.txt
data/activar-sesion-08/julio-f2.txt anexos/.../cuenta-por-mes.txt` → `delta-julio-f2-cuenta-por-mes.txt`:
«filas de 2026-07: base 87, nuevo 87»; «sesiones de 2026-07: 25; cambian de rn003: 0»; «filas que
cambian de patron: 0»; «filas que aparecen: 0»; «filas que desaparecen: 0». Las filas de julio de la
corrida 1 repiten las de julio-f2: 10 parejas y 20 de más.

**La contingencia aplica.** Sobre la corrida 1 (`pivote-julio.txt`): T0 10; operaciones de más (P5 + P6
en sesión) 20. Pero la cuenta por mes de julio **deja de llenar por un freno de la cuenta antes del 17**:
RN-032 dispara en las 12 sesiones de julio desde 2026-07-10 07-11 hasta 2026-07-17 11-15, ninguna otra
regla que prohíba abrir está entre las disparadas, y el bot no llena ninguna orden desde 2026-07-10 11-15
(la curva de la cuenta no tiene equity mínima del 13 al 17; §1.1). La cuenta acaba EN_CURSO, no SUSPENDIDA.
Por la contingencia de ADR-0093 §6 y `PIVOTES-SESION-7.yaml` («si en esa corrida la cuenta de julio acaba
SUSPENDIDA o deja de llenar por un freno de la cuenta antes del 17, el pivote se lee sobre la corrida
diaria de contexto, y el informe lo dice»), sin retocarla (decisión de Aleks del 2026-11-19; R4.3), el
pivote **se lee sobre la corrida 2**, contra los mismos mínimos y sin mezclar parejas de las dos.

`pivote_julio.py patrones-diaria.txt` → `pivote-julio-diaria.txt` (exit 1, «NO CUADRA: no son 14 y 39»,
que no es un fallo):

```
patrones-diaria.txt, mes 2026-07
T0 (parejas): 19
P5: 38 ({'mismo lado': 36, 'otro lado': 2}); P6 en sesion: 2; P6 en dia: 0
operaciones de mas (P5 + P6 en sesion): 40
```

Con los mínimos del yaml (`minimo_1_parejas_de_julio_al_menos: 19`,
`minimo_2_operaciones_de_mas_de_julio_como_mucho: 33`): parejas 19 ≥ 19, sí; operaciones de más 40 ≤
33, no. **Se cumple uno**, y su salida literal (`salidas.se_cumple_uno`): «una sesión más con el trader
con el mismo método, y tras su activación se vuelve a leer con estos mismos números». La misma clave la
calcula `techo_parejas.py` (§4). No la interpreto.

El yaml dice «incluida la rama de S-22 y S-19»: S-22 no se activó (decisión del consultor en
`trabajo/activar-sesion-08`, F3).

## §4 · La meta de ADR-0098 (fase 4)

`anexos/RECORRIDA-CONSTRUCCION-3/control.txt` y `meta.txt`, de los comandos del README (exit 0 los dos):

```
## El control (ADR-0098 §1)
posiciones del bot en la salida: 235; entran en el control: 235; fuera (manual de una regla solo del bot): 0
reproducidas al centimo (lote, motivo, instante del cierre, PnL neto): 235 de 235
control: PASA

## M1 · El techo (ADR-0098 §1)
operaciones del trader en los dias dev: 198; sin stop: 0; no colocables: 7; no llenadas: 0; fuera por el lote minimo: 0; fuera de la ventana: 0
rechazadas por el broker, por motivo: ninguna
llenadas y cerradas: 191; cierres de M1 con mas de una posicion viva: 0; cierres por RN-002: 7; al fin del dia: 0; break even movido: 79
a) N (llenadas y cerradas): 191
b) esperanza (media del R neto): -0.239
c) percentil 5 y percentil 95 de la media del R neto, por remuestreo por dias (10000 replicas, semilla 20261107, todos los dias dev corridos): -0.450 y -0.026; replicas descartadas: 0
d) perdida diaria maxima, por cuenta: 4.88 % del capital inicial; la peor, la cuenta de 2026-07
e) equity minima, por cuenta: 92.05 % del capital inicial; la peor, la cuenta de 2026-07
f) alguna cuenta entro en SUSPENDIDA: no
deslizamiento por llenado afectado que lleva la esperanza a 0.10 R (ADR-0092 §4, sin decidir nada): -2.52 puntos
LECTURA DEL TECHO: no_gana

### Julio de 2026, como diagnostico (sin umbral; el unico mes con video, provisional)
a) N (llenadas y cerradas): 64
b) esperanza (media del R neto): -0.245
c) percentil 5 y percentil 95 de la media del R neto, por remuestreo por dias (10000 replicas, semilla 20261107, los dias dev de julio): -0.546 y 0.085; replicas descartadas: 0
d) perdida diaria maxima, por cuenta: 4.88 % del capital inicial; la peor, la cuenta de 2026-07
e) equity minima, por cuenta: 92.05 % del capital inicial; la peor, la cuenta de 2026-07
f) alguna cuenta entro en SUSPENDIDA: no

## M2 · Las parejas (ADR-0098 §1)
filas T0 de la corrida 1, por mes: 2026-01 5, 2026-04 10, 2026-07 10, 2026-08 5
parejas con las dos patas: 29; sin pata del trader: 1; sin pata del trader (no colocable, no llenada, rechazada o lote minimo): 1; sin la posicion del bot: 0
media del R neto del bot en sus parejas: -0.140; del trader en las mismas operaciones: -0.338; diferencia emparejada media (bot - trader): 0.198
percentiles 5 y 95 por remuestreo por dias (10000 replicas, semilla 20261107, 76 dias): del bot -0.745 y 0.540; de la diferencia -0.132 y 0.592
minimo de parejas (PIVOTES-SESION-7.yaml, minimos.minimo_1_parejas_de_julio_al_menos): 19
LECTURA DE LAS PAREJAS: ni_una_cosa_ni_otra

## La salida (ADR-0098 §3)
techo: no_gana; parejas: ni_una_cosa_ni_otra
SALIDA: C (el techo no gana)
pivote de ADR-0093 §6 (de pivote-julio-diaria.txt): parejas de julio 19, operaciones de mas 40, minimos 19 y 33: se_cumple_uno (una sesión más con el trader con el mismo método, y tras su activación se vuelve a leer con estos mismos números)
PRECEDENCIA CON EL PIVOTE (C): manda sobre cualquier salida del pivote
```

**La salida la da el guion: C.** Por qué, en las palabras de §2 de ADR-0098 que el guion aplica: «no gana:
incumple d), e) o f); o la esperanza es < 0; o el percentil 95 es < +0,10 R»: aquí la esperanza es
−0,239 y el percentil 95, −0,026 (d), 4,88 %, también incumple). No la reinterpreto ni la matizo.

Notas de método, sin interpretación: el control pasó con todas las posiciones del bot, ninguna fuera; la
precedencia lee el pivote de la diaria porque la contingencia aplica (§3), y con el de la corrida 1 la
clave sería la misma (`se_cumple_uno`: 10 < 19 y 20 ≤ 33); el R del bot de cada pareja sale de la
repetición del control, verificada al céntimo. La línea «sin pata del trader» repite la cifra dos veces
(el total y su única categoría): es la forma del guion, no una cifra distinta.

## §5 · Los patrones y la lista para clasificar (D9)

`patrones.py --filas` (con el `sed` del CRLF) → `patrones-cuenta-por-mes.txt` (403 filas, 104 sesiones
con rn003) y `patrones-diaria.txt` (456 filas). Por mes:

| corrida | mes | P1 sesgo | P2 entrada | P3 otra zona | P4 sin orden | P5 de más | P6 donde el trader no operó | P7 entradas repetidas | T0 pareja |
|---|---|---|---|---|---|---|---|---|---|
| 1 (por mes) | 2026-01 | 9 | 16 | 18 | 5 | 61 | 11 | 1 | 5 |
| 1 (por mes) | 2026-04 | 5 | 6 | 11 | 3 | 31 | 31 | 0 | 10 |
| 1 (por mes) | 2026-07 | 1 | 8 | 14 | 32 | 18 | 2 | 2 | 10 |
| 1 (por mes) | 2026-08 | 8 | 4 | 14 | 11 | 33 | 18 | 0 | 5 |
| 1 (por mes) | total | 23 | 34 | 57 | 51 | 143 | 62 | 3 | 30 |
| 2 (diaria) | 2026-01 | 9 | 17 | 21 | 1 | 70 | 15 | 1 | 5 |
| 2 (diaria) | 2026-04 | 5 | 6 | 11 | 3 | 31 | 31 | 0 | 10 |
| 2 (diaria) | 2026-07 | 1 | 18 | 24 | 1 | 38 | 2 | 4 | 19 |
| 2 (diaria) | 2026-08 | 8 | 7 | 12 | 3 | 46 | 25 | 1 | 11 |
| 2 (diaria) | total | 23 | 48 | 68 | 8 | 185 | 73 | 6 | 45 |

Como contexto, RECORRIDA-CONSTRUCCION-2 §4, verificado en su anexo
`anexos/RECORRIDA-CONSTRUCCION-2/patrones-cuenta-por-mes.txt` (414 filas): enero 7, 17, 21, 1, 66, 15, 1,
7; abril 9, 5, 12, 1, 29, 33, 0, 8; julio 20, 14, 15, 1, 37, 2, 3, 14; agosto 8, 4, 6, 22, 21, 13, 0, 2;
total 44, 40, 54, 25, 153, 63, 4, 31.

**La lista para clasificar (`para_clasificar.py`): pendiente de la decisión 0 (§0.5)**, porque su resumen
imprime un R por clase de órdenes que ADR-0098 §4 c) no deja en esta corrida. Sin conclusiones: es la
materia de la sesión siguiente (R4.6, paso 1).

## §6 · Los diffs contra la línea base anterior (D10)

- `diff-linea-base.txt` (`anexos/RECORRIDA-CONSTRUCCION-2/cuenta-por-mes.txt` frente a la corrida 1; exit
  1): 3527 → 3393 líneas, 2360 quitadas y 2226 puestas. Por sección (`diff-linea-base-por-seccion.txt`),
  las mayores: «### Ordenes» 1109/969, «### Eventos del broker» 380/336, «### Posiciones» 238/226,
  «### Por operacion» 204/193, «## Avisos de orden dentro de una clase» 152/200; «### Esperas», 0/28
  (sección nueva); «### Rechazos por motivo», 4/1.
- `diff-diaria.txt` (las dos diarias; exit 1): 3957 → 3921 líneas, 1747 quitadas y 1711 puestas
  (`diff-diaria-por-seccion.txt`); «### Esperas», 0/37.

**Lo que la evidencia deja atribuir** (gana la medida sobre la forma del encargo: ADR-0097 no rechaza,
espera; §0.4, 1):
- **A la 7b (F39k, ADR-0097):** las esperas de «### Esperas» (25 en la corrida 1: enero 3, abril 10, julio
  6, agosto 6) y la desaparición de los 32 rechazos `precio_invalido` al colocar de la línea base anterior
  («### Rechazos por motivo»: de cuatro filas a «ninguno»).
- **A la 7a (F39e):** el break even al cierre y con cuerpo (`break_even_condicion` = `cierre`,
  `break_even_criterio_ruptura` = `cuerpo`): los eventos `stop_movido` pasan de `ticks` (32, 32, 18 y 16
  por mes en la línea base anterior, más 2 `respaldo_m1`) a `cierre_m1` (25, 26, 8 y 16, más 5
  `respaldo_m1`) (`resumen-cuenta-por-mes.txt` de las dos ramas, «Eventos del broker, por mes»). Y
  ADR-0094 (el sesgo del rango vigente): «## RN-003 al abrir la sesion» pasa de «alcista 51; bajista 52;
  insuficiente 1» con 22 dobles rupturas a «alcista 57; bajista 46; insuficiente 1» con 8, y «por operacion
  del trader: a favor 154; en contra 42» a «a favor 175; en contra 21».
- **Sin atribuir:** todo lo demás (las filas de «### Ordenes», de «### Posiciones» y de «### Por
  operacion», las cuentas y la cascada), porque cada una arrastra las anteriores del mes y ninguna fila
  dice qué regla nueva la movió. Los merges de `trazas-ablacion`, `laminas` y `laminas-motivos`, que también
  tocaron `src/` o la spec, repitieron la línea base a 0 bytes (§0.4, 6).

## §7 · Las líneas del cierre, preparadas y medidas sobre una copia (no aplicadas)

`anexos/RECORRIDA-CONSTRUCCION-3/simular_cierre.py` las aplica en memoria sobre copias de
`PROJECT_STATE.md`, `docs/plan/HOJA-DE-RUTA.md` y `docs/state/HISTORIA.md` y corre `test_hoja_de_ruta`
(a, b y c) y `test_project_state`; en el repo no escribe nada (`simular-cierre.txt`):

```
letras vivas en la copia: A C D F G I J M N Q; F viva? True
R3.10: HECHA? True; NA:F en el bloque? False
R4.3: HECHA? True; NA:F en el bloque? False
R5.7: HECHA? True; NA:F en el bloque? False
R4.6 cita ADR-0098? True
R5.2 cita R3.10? True
«R5.7 después de (3)» en la F? False
a: []
b: []
c: []
PROJECT_STATE del cierre, con la linea de D7: 24505 bytes (cabe en 25000); la rama hoy: 24598 bytes con la F nueva
PROJECT_STATE del cierre, sin la linea de D7: 24337 bytes (cabe en 25000); la rama hoy: 24598 bytes con la F nueva
bytes de la F: antes 1030, despues 827
bytes de la linea de D7: 168
```

PROJECT_STATE del cierre, en la forma que escribirá el ritual (cabeceras del cierre, sin la Current Branch
de la rama): **24.505 bytes con la línea de D7 y 24.337 sin ella**, por debajo de 24.900 (y de main, que
tiene 24.669). Las líneas, tal como las aplicaría la orden de cierre:

- **Next Action, la F**, una frase por cosa, sin quitar lo vivo («R5.7 después de (3)» sale; ninguna letra
  sale ni entra): «F. La sesión 7, en dos días con el método de ADR-0093 (R4.3), ingerida y ACTIVADA: la 7a
  (F39e: ADR-0094, A-58 abierta; break even al cierre, A-13 abierta por el margen) y la 7b (F39k: la stop
  cuyo 0 queda del lado malo espera, ADR-0097, A-59 abierta); A-48 y A-58, a la sesión siguiente. La corrida
  (3) de ADR-0070 §3 dio «no» (cobertura 15.2 %, precisión 14.4 %; RECORRIDA-CONSTRUCCION-3.md). La línea
  base vigente es anexos/RECORRIDA-CONSTRUCCION-3/cuenta-por-mes.txt. El pivote de ADR-0093 §6, por su
  contingencia sobre la diaria (19 parejas de julio y 40 de más): «una sesión más». La meta de ADR-0098:
  salida C, el techo no gana, y manda sobre el pivote. El vídeo de mapeo (recibido el 2026-11-18): SIN
  ABRIR y fuera del repo, no se ingiere; octubre y noviembre de 2026, reservados. C y R6a en los huecos.»
  Lo que sigue a C (ADR-0098 §3: F17, S-14, A-16, Aleks con el trader; la sesión siguiente se prepara y no
  se graba hasta un ADR de Aleks) lo fija tu respuesta, no esta frase.
- **Hoja de ruta:** R3.10 nueva tras R3.9, con la forma de R3.9, HECHA con el veredicto (Refs ADR-0070,
  ADR-0092, ADR-0097 y ADR-0098; ninguna letra en todo su bloque); R4.3 HECHA, sin `NA:F` en Refs (la F
  sigue viva en R4.2 y R4.6), con ADR-0098 en Refs y en su Estado el pivote leído por la contingencia y su
  salida y la de ADR-0098; R4.6 con ADR-0098 en Refs y «Hecho cuando» con «o la lectura de ADR-0098 cambia
  el objetivo»; R5.7 sustituida por la medida de ADR-0098 y HECHA (sin `NA:F`), con la salida C en su
  Estado; R5.2 «Depende de» cita R3.10; y el Marcador: `| 2026-11-22 | RECORRIDA-CONSTRUCCION-3.md |
  15.2 / 14.4 | 22.7 / 16.3 | -0.429 | 321 |` (cobertura y precisión de la corrida 1 y de la diaria; la
  esperanza del bot, de la corrida 1; las operaciones de más como las define el Marcador: las órdenes del
  bot en un (día, sesión, dirección) sin operación del trader, 321, no las del pivote). El texto exacto de
  cada sustitución, en `simular_cierre.py`.
- **Technical Debt:** la línea de D7 se queda o sale según decidas (168 bytes).

## §8 · La fila de ERRORES-RECURRENTES, preparada (no aplicada)

| Rama | Qué se encontró | Señal | Qué hacer |
|---|---|---|---|
| `trabajo/recorrida-construccion-3` | (1) El bloque `ids-inexistentes` solo exime al documento que lo lleva: citar el ADR del encargo en PROJECT_STATE, en la fila de HOLDOUT o en la cabecera del informe antes de que exista tumba `knowledge validate` (cuatro errores en la apertura). (2) Una decisión del encargo choca con el ADR que el mismo encargo pre-registra: D9 pedía `para_clasificar.py`, que imprime un R por clase, y ADR-0098 §4 c) lo prohíbe. (3) D10 pedía atribuir «un rechazo de ADR-0097», y ADR-0097 no rechaza: espera (auditor). (4) La contingencia del pivote se activó sin SUSPENDIDA, por un freno que deja de llenar (RN-032 desde el 10 de julio). (5) Un guion que lee una sección de la salida tiene que parar en su línea de resumen («ordenes: …»): el ensayo del control sobre una salida ya expuesta lo cazó antes de la corrida. | (1) «id citado que no existe» en el primer `knowledge validate`. (2) un guion de `main` que imprime R sobre una clase. (3) la palabra «rechazo» junto a ADR-0097. (4) días al final del mes sin equity mínima en la curva de la cuenta. (5) `IndexError` al partir una línea sin columnas. | (1) El id solo en el encargo hasta el commit que lo crea. (2) Antes de correr, cruzar cada guion pedido con lo que el pre-registro prohíbe imprimir. (3) El rastro de ADR-0097 es «### Esperas» y los `precio_invalido` que desaparecen. (4) Leer la contingencia con la curva y «disparadas», antes del pivote. (5) Ensayar el guion de la meta sobre una salida ya expuesta del motor de hoy antes de la corrida que cuenta. |

## El encargo frente a lo hecho

| # | Punto del encargo | Hecho | Evidencia |
|---|---|---|---|
| 1 | Base comprobada (main, tag, CI, ramas, tag previsto) | Hecho | «Base comprobada»; run 45051429307 |
| 2 | Variable del reaper y /model | Hecho | `echo`: `REAP=1`; Opus 5.5, alto |
| 3 | La fila de HOLDOUT, lo primero, por recuento | Hecho | 14:32:37, antes del primer `make check` (§0.3 h); filas complementarias del día |
| 4 | Los dos ficheros de Aleks, leídos; sin fechas reservadas | Hecho (el yaml llegó a mitad) | «Desviaciones de la apertura» |
| 5 | abrir-rama, contrato, encargo, `ids-inexistentes` con ADR-0098 | Hecho | `3457fb31`; contrato.yaml |
| 6 | Fase P: ADR, yaml, test, índice, recuadro, sale del bloque | Hecho | `539f7983`, 15:49:25; §0.2 |
| 7 | Fase 0, a a j, con el auditor y la PARADA condicional | Hecho; PARADA en un punto | `acae32e8`; §0.3 a §0.5 |
| 8 | Fase 1: README en su commit, guion, test, ruff/mypy | Hecho | `c5bdad44`, `bca9ba20`; §0.8 |
| 9 | Fase 2: las tres corridas, una a una | Hecho | §1, §2 |
| 10 | D1, veredicto literal; D2, línea base | Hecho | §1 |
| 11 | D3, NOTA en ADR-0070 §3, en un commit propio | Hecho tras las salidas | su commit |
| 12 | D4, el pivote, con la contingencia | Hecho; la contingencia aplica | §3 |
| 13 | D5, el control de julio | Hecho: repite | §3 |
| 14 | D6, D7, D8 | Hecho | §1.1, §1.2, §1.3 |
| 15 | D9, patrones y lista para clasificar | Patrones hechos; la lista, a la decisión 0 | §5 |
| 16 | D10, los dos diffs, atribución | Hecho (con «### Esperas» en lugar de «rechazo») | §6 |
| 17 | D11, determinismo | Hecho: idéntica | §2 |
| 18 | D12, tiempo y memoria | Dentro: 345,7 s, 317,7 s y 372,6 s; 638,5 a 644,2 MiB | §1, §2 |
| 19 | D13, nada de `src/`, `tests/` (salvo el test nuevo) ni `knowledge/` | Hecho | `git diff main --stat` |
| 20 | D14, ADR-0098 §1, §2 y §4 c) al pie de la letra | Hecho, con las lecturas declaradas | §0.3 f, §0.8, §4 |
| 21 | Fase 4: control y, si pasa, techo, parejas y salida | Hecho: pasa; salida C | §4 |
| 22 | §7, líneas del cierre medidas sobre una copia | Hecho | §7 |
| 23 | §8, fila de ERRORES preparada | Hecho | §8 |
| 24 | Revisor (opus) con los siete alcances | Al final del informe | su informe |

**Desviaciones:** el yaml llegó a mitad de la apertura; la fila de HOLDOUT declara junio para los `make
check`, como la skill (el encargo nombraba solo marzo); la fase P va antes del auditor, contra el orden de
`fase-cero`; las citas de ADR-0098 fuera del encargo se quitaron hasta que existió; D10 atribuye con
«### Esperas» y no con «un rechazo de ADR-0097», que no existe; `para_clasificar.py` no se corrió (decisión
0); el pivote se lee sobre la diaria porque la contingencia aplica; el guion de la meta pasó por un
segundo ensayo tras arreglar la lectura de «### Ordenes».

**Comandos ejecutados** (desde la raíz; los de las corridas, del encargo, literales):
- `uv run botsito motor arnes --simular --salida docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/cuenta-por-mes.txt`
- `uv run botsito motor arnes --simular --diagnostico-cuenta-diaria --salida docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/diaria.txt`
- `uv run botsito motor arnes --simular --salida <carpeta de trabajo>/cuenta-por-mes-repetida.txt` y `diff` contra la commiteada
- `uv run python -B docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/patrones.py <salida> --filas > <destino>` y `sed -i 's/\r$//' <destino>`, para las dos salidas
- `uv run python -B docs/validation/anexos/PREPARACION-SESION-7/pivote_julio.py <patrones>`, para las dos
- `uv run python -B docs/validation/anexos/ACTIVAR-SESION-07/delta_julio.py <4 argumentos>`: f2 → corrida 1 (D5) y corrida 1 → diaria (D6)
- los dos `diff` de D10 y `diff_por_seccion.py` sobre cada uno; `resumen_corrida.py` sobre las dos salidas
- `techo_parejas.py control` y `parejas` (README); `frenos_julio.py`; `simular_cierre.py`; `antes_del_dia.py` (el de `main`) sobre los ficheros nuevos de la carpeta: ninguna fecha de material fuera de la construcción ni anterior a su día (las que marca son de calendario, de 2026-11-08 a 2026-11-22, sintéticas de 2030 o de un día dev)

**Exposiciones de cada día:** todo el trabajo es del 2026-11-22; sus cuatro filas en HOLDOUT-EXPOSICIONES
(la de la apertura, la del ensayo del control y lo de la fase 0, la de los guiones nuevos, y la del
revisor).

## Estado

EN CURSO: fases P, 0, 1, 2, 3 y 4 hechas; la NOTA de ADR-0070 y el revisor, a continuación.
