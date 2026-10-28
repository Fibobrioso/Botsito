# RECORRIDA-CONSTRUCCION · La corrida que cuenta por ADR-0070 §3 sobre toda la construcción (R4.1, entradas V y F)

Rama `trabajo/recorrida-construccion`, abierta el 2026-10-27 desde `main` en 88f97f7 (commit de
estado sobre el merge d843dbc, tag `stable/F38f-activar-sesion-05-motor`). Encargo:
`docs/encargos/trabajo-recorrida-construccion.md`. Tramo: R4 (R4.1 de `docs/plan/HOJA-DE-RUTA.md`,
lo que queda; V y F de la Next Action).

Antes de abrir se comprobó con git (skill `abrir-rama`, paso 1):

- `git rev-parse --short main` = 88f97f7; `git rev-parse main origin/main` da dos veces
  88f97f7222882e61ba2fb61e553c7727638c659b; `git status --short` vacío.
- El último tag de `docs/state/HISTORIA.md` es `stable/F38f-activar-sesion-05-motor`;
  `git rev-parse "stable/F38f-activar-sesion-05-motor^{commit}"` = `git rev-parse main^1` =
  d843dbc58cc9c23d8fb81f21309e1efe461b3417; `git ls-remote --tags origin stable/F38f-activar-sesion-05-motor`
  devuelve el tag (90679585…).
- La CI de `main` sobre 88f97f7222882e61ba2fb61e553c7727638c659b, por la API de check-runs con el
  sha literal (`gh api repos/{owner}/{repo}/commits/<sha>/check-runs`): un check `python`,
  `completed` / `success`, run 40537113754 (el que cita el cierre).
- `git branch --list` solo da `main`; `git ls-remote --heads origin "fix/*"` sale vacío, y
  `git ls-remote --heads origin` solo da `main`.
- `wc -c PROJECT_STATE.md` = 22924 bytes, como dice el encargo.
- `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1` está en el entorno de la sesión (`echo`, da `1`).

## 0. Lo que se decide antes de correr, y la fase 0 (2026-10-27)

### 0.0 Lo que se decide antes de correr (DECISIÓN DEL CONSULTOR, 2026-10-27, salvo lo que cita su ADR)

Copiado del encargo, con lo medido en esta fase 0 al lado:

1. **La corrida 1 (cuenta arrastrada) es la que cuenta por ADR-0070 §3** (NOTA del 2026-10-26,
   `docs/adr/0070-…md:81-88`). Su línea `habilita medir el conjunto de medida (2026-05) (ADR-0070): …`
   (`engine/arnes.py:379-380`; `medida: ["2026-05"]`, `criterio_fidelidad.yaml:41`) se copia literal
   a este informe.
2. **Si dice «no»**: se sigue construyendo, mayo no se toca y el umbral no cambia (ADR-0070 §4,
   `:90-91`).
3. **Si dice «sí»**: PARADA, y nada de mayo. Por ADR-0070 §6 (`:102-104`) un «sí» habilita la rama de
   medida, con su propio ADR, y no la sustituye; qué hace esa rama con A-35 y A-44 ABIERTAS y con los
   parámetros DEFAULT_AMBIGUOUS (§0.i) lo decide el consultor en ese ADR.
4. **La clasificación por patrones se hace sobre la corrida 2** (cuenta diaria), como en R3.1
   (`CORRIDA-CONSTRUCCION.md:945`); la corrida 1 da el veredicto y el camino de la cuenta y se
   clasifica solo como contexto.
5. **La lista «Entradas antes de la alternancia»**: cada orden LLENADA del bot cuyo llenado ocurrió
   con menos de dos zonas de control formadas desde la toma de su escenario (RN-009,
   `strategy_spec.yaml:1517-1525`; ADR-0076 §2 y su NOTA `:74-80`; ADR-0085 §4 `:93-99`), con dos
   columnas: cuántas zonas había al llenar (0 o 1) y dónde estaba la orden. **Cómo se asignan las dos
   columnas sin dar dos respuestas lo decide la PARADA (punto 0 de «Lo que necesito que decidas»)**:
   el auditor midió que las tres categorías del encargo no se excluyen (§0.f).

### 0.a La corrida 1 usa solo opciones de la lista cerrada; los diagnósticos se rechazan; el nombre de la corrida 2

- **La lista cerrada** vive en `src/botsito/engine/arnes.py:80-82`:
  `OPCIONES_QUE_NO_CAMBIAN_LA_CORRIDA = {"--salida", "--tracemalloc", "--meses", "--simular",
  "--perfil", "--fase"}`; `informe` resta esa lista a las opciones que la corrida usó (`:281-284`)
  y las opciones salen de los propios parsers, las que tienen un valor distinto del de por defecto
  (`cli.py:2218-2232`, `opciones_de_la_corrida`; la llamada en `:2449`). Medido con
  `build_parser().parse_args` sobre los dos comandos de la fase 2 (guion de la carpeta de trabajo,
  `medir_fase0.py`, apartado 4):
  - corrida 1 (`--simular --salida x.txt`): opciones `('--salida', '--simular')`, fuera de la lista
    `[]`; `perfil None`, `fase None`, `meses None`;
  - corrida 2 (`--simular --diagnostico-cuenta-diaria --salida x.txt`): opciones
    `('--diagnostico-cuenta-diaria', '--salida', '--simular')`, fuera de la lista
    `['--diagnostico-cuenta-diaria']`: su veredicto dirá «no (opción fuera de la lista:
    --diagnostico-cuenta-diaria; …)» aunque llegue a los umbrales, como ADR-0070 §3 manda. Sin
    `--simular` la opción sale con código 2 (`cli.py:2250-2251`).
- **Perfil y fase efectivos.** `--perfil` por defecto `None` → `cableado.perfil_del_repo(repo, None)`
  (`cli.py:2397`; `cableado.py:546-560`): el único yaml de `knowledge/cuentas/`,
  `ftmo-2step-swing-100k`, que es `perfil_para_medir` (`criterio_fidelidad.yaml:30`). `--fase` por
  defecto `None` → `perfil.fases()[0]` (`cableado.py:595`); medido: `fases ('reto', 'verificacion',
  'fondeada')`, primera `reto` (`ftmo-2step-swing-100k.yaml:76-86`, `firma_fases: "reto verificacion
  fondeada"`). La `Simulacion` que recibe el veredicto se construye con el perfil y la fase del motor
  cableado y la primera del perfil (`cli.py:2440`), que `test_umbral_mayo.py:334-337` congela por
  `ast`. Huso de corte del perfil: `Europe/Prague`.
- **Sin `--meses`**, `meses = list(criterio.construccion)` (`cli.py:2385`): los cuatro meses, en el
  orden del yaml (`["2026-04", "2026-07", "2026-08", "2026-01"]`, `criterio_fidelidad.yaml:40`);
  `habilita_medir` no echa en falta ninguno (`cases/criterio_fidelidad.py:207-211`).
- **`--diagnostico-a35` y `--diagnostico-a44` se rechazan hoy**, medido contra el registro de la rama
  (`medir_fase0.py`, apartado 5):
  - `lectura_pivote(registro, Diagnostico(a35="cierre_vela_contraria"))` →
    `DiagnosticoRechazadoError: liquidez_m15_pivote_formado ya esta fijado en 'cierre_vela_contraria'
    (A-35 respondida): la corrida cuenta y no admite --diagnostico-a35`
    (`engine/diagnostico.py:111-116`; el valor, `parametros.yaml:526-527`, CONFIRMED);
  - `tope_del_registro(registro, huso, Diagnostico(a44="sin_tope"))` → `TopeRechazadoError:
    perdida_trader_alcance ya esta fijado en 'dia' (A-44 respondida): la corrida cuenta y no admite
    --diagnostico-a44` (`engine/tope_trader.py:140-144`; el valor, `parametros.yaml:1451-1452`).
  - Las dos son `ValueError`, así que el comando saldría con código 2 (`cli.py:2459-2462`).
- **El motor no necesita ningún `--diagnostico-*`**: `lectura_pivote(registro)` da
  `cierre_vela_contraria` y `tope_del_registro(registro, huso)` da `tope del trader: dia, sobre
  saldo, en porcentaje; dia 4.5 sobre saldo_inicial_dia; reinicio en Europe/Prague; SUPUESTO:
  reinicio con el huso de corte del perfil (el trader no dijo otro)` (`tope_trader.py:171-205`;
  `perdida_trader_reinicio_huso` UNKNOWN, `parametros.yaml:1530`, de ahí el SUPUESTO, `:191-194`).
  A-21 (`zonas.lectura_limpia`, `solo_una_zona_de_control`, `parametros.yaml:997-998`) y A-47
  (`entrada_tipo_orden = stop_en_ruptura`, `:903-904`) también están fijadas. `Diagnostico()` sin
  nada: `etiquetas ()`, `activo False`: la corrida 1 sale SIN rótulo y con el nombre pedido.
- **El nombre real de la corrida 2**: `Diagnostico(cuenta_diaria=True).etiquetas` =
  `('DIAGNOSTICO-CUENTA-diaria',)` (`diagnostico.py:38`, `:92-93`) y
  `nombre_etiquetado(Path("diaria.txt"), …)` = **`diaria.DIAGNOSTICO.cuenta=diaria.txt`**
  (`:168-184`; `MARCA_FICHERO`, `:161`); cada línea de esa salida empezará por
  `[DIAGNOSTICO-CUENTA-diaria] ` (`etiquetar`, `:129-140`). El fichero final de la corrida 2 es, pues,
  `docs/validation/anexos/RECORRIDA-CONSTRUCCION/diaria.DIAGNOSTICO.cuenta=diaria.txt`.

### 0.b Ticks: cada día dev tiene ticks; las 18 horas perdidas

Los cuatro manifiestos de `data/manifests/ticks/` (`eurusd-ticks-2026-01-1ce59681`,
`-04-1d189bdd`, `-07-6e7dc7cd`, `-08-75bd3a08`; son los únicos, `ls data/manifests/ticks/`), leídos
por el guion de la carpeta de trabajo con sus rutas por argumento, frente a los días `dev` que da la
compuerta del arnés (`arnes.dias_de_construccion`, mes a mes):

| Mes | ficheros del manifiesto | días `dev` | coinciden uno a uno | horas pedidas (UTC) | presentes | perdidas | ausentes_404 |
|---|---|---|---|---|---|---|---|
| 2026-01 | 21 | 21 | sí | 06-14 | 184 | 5 | 0 |
| 2026-04 | 21 | 21 | sí | 05-13 | 182 | 7 | 0 |
| 2026-07 | 13 | 13 | sí | 05-13 | 114 | 3 | 0 |
| 2026-08 | 21 | 21 | sí | 05-13 | 186 | 3 | 0 |

**Ningún día dev sin ticks: no hay PARADA por ticks y no hace falta `--depuracion`** (que además da
«no», ADR-0070 §3). **Total 18 horas perdidas**, las mismas 18 que `anexos/CORRIDA-CONSTRUCCION/horas_perdidas.py:18-24`
escribe tal cual (comparadas una a una: iguales); **17 caen dentro de las sesiones** y
`2026-04-22T13Z` fuera (la ventana de verano acaba a las 13:00Z, `FUERA_DE_SESION`, `:25`;
`horas_utc` de abril es 05-13 y la hora 13Z es la de después del cierre). Lo que hace el cableado con
una hora perdida no cambia desde R3.1: minuto a minuto cae al respaldo M1 (`CORRIDA-CONSTRUCCION.md`
§1.b); un día sin ningún tick lo rechaza `MotorCableado.correr_dia` salvo con `--depuracion`
(`cableado.py:240-244`). Los manifiestos no han cambiado desde el 2026-10-13 (auditor, `git log`).

### 0.c Calentamiento: qué mes anterior carga cada mes, y la fila de HOLDOUT-EXPOSICIONES

`arnes.dias_de_mercado` (`engine/arnes.py:179-220`) carga, por cada mes de los días,
`(_mes_anterior(mes), mes)` si `buscar_manifiesto` encuentra el dataset (`:201-206`; sin el
anterior, «el calentamiento empieza en el mes»); `_mes_anterior` (`:174-176`) da `2025-12` para
enero. Datasets M1 en `data/manifests/` (nombres, `ls`): 2026-01, 03, 04, 05, 06, 07, 08 y 09;
ninguno de 2025-12. Así que hoy: **enero** calienta desde su propio mes; **abril** carga el M1
**entero de marzo** (mes reservado entero y sin sortear, `meses_reservados.yaml`;
`casos_reservados` da 0 para 2026-03 porque no tiene casos); **julio** carga el M1 **entero de
junio** (11 casos reservados por recuento hoy, §0.g de exposiciones); **agosto** carga julio entero
(días 18 a 31 de julio: no están en ninguna partición -`casos_reservados` da 0 en 2026-07- pero
tampoco son construcción, ADR-0078; solo velas). El visor, que esta rama no abre, calienta igual
(`engine/visor.py`, `Preparador._m1`).

**Fila propuesta para `docs/validation/HOLDOUT-EXPOSICIONES.md` (se escribe en la fase 1, en su
propio commit, ANTES de correr nada; la fase 0 no ha leído ninguna vela):**

> | 2026-10-27 | **Rama `trabajo/recorrida-construccion` (`RECORRIDA-CONSTRUCCION.md`), declarado ANTES de correr nada.** (1) **La fase 0 (el mismo día):** ningún libro, ninguna imagen, ningún fotograma, ninguna transcripción; nada de marzo, mayo, junio, septiembre, diciembre ni febrero. Los repartos solo por RECUENTO con un guion de la carpeta de trabajo que recibe la raíz por argumento y no imprime claves (`casos_reservados` 34 y `casos_ocultos` 34; 13 en 2026-05, 11 en 2026-06, 10 en 2026-09; 0 en 2025-12 y en los cuatro meses de construcción 2026-01, 04, 07 y 08). Los 76 casos dev de construcción por la compuerta del arnés (`arnes.dias_de_construccion`: recuento de días y de operaciones por mes); los cuatro manifiestos de ticks de construcción enteros; las salidas commiteadas de `anexos/PUNTO-USADO/` (días dev). El auditor del encargo leyó solo el repo: contó `direccion:` en `knowledge/cases/dev/caso-eurusd-<mes>-*.yaml` de los cuatro meses y los manifiestos M1 con `ls data/manifests \| grep -c` (la forma que ERRORES-RECURRENTES.md desaconseja: solo salieron recuentos). (2) **Lo que leerán las tres corridas de `motor arnes --simular` de la fase 2** (las dos commiteadas y la repetición de la 1 fuera del repo para el `diff` de determinismo) **y el guion de la fase 1 f)** (`anexos/RECORRIDA-CONSTRUCCION/entradas_antes_alternancia.py`, que carga las velas como el arnés, `arnes.dias_de_mercado`, y reproduce la corrida 2), **para CALENTAR el sesgo H4** (`engine/arnes.py:179-220`): el dataset M1 **entero de marzo de 2026** (mes reservado entero y sin sortear, `meses_reservados.yaml`) para abril y el **entero de junio de 2026** (11 días reservados por recuento: medidos hoy) para julio, además del M1 de julio para agosto y de los cuatro meses de construcción; enero no tiene M1 anterior. Leer velas para calentar no es abrir (ADR-0021 §1; ADR-0033 §4). Las salidas (`anexos/RECORRIDA-CONSTRUCCION/`) dan el sesgo H4, las M15 y las órdenes del BOT de los días dev: ninguna etiqueta, ningún precio de un día reservado; ningún guion, tabla ni informe imprime una H4, un pivote, un precio ni un instante anteriores al día dev al que pertenecen (regla «(antes del dia)» de `anexos/VISOR-CONSTRUCCION/comun_visor.py`; lección a1 de R3.1). La copia de `patrones.py` solo lee la salida del arnés. (3) **Cada `make check` de la rama** lee el M1 entero de marzo por `test_preparar_a35.py` y `test_visor.py` (las filas del 2026-10-18, 2026-10-26 punto (5) y 2026-10-27). | por el recuento: marzo de 2026 entero (sin partición: mes reservado entero); holdout-1, holdout-2 y holdout-3 (los 11 días de junio) | la sesión, con el encargo del consultor del 2026-10-27 y su respuesta a la PARADA | No: solo velas, ninguna etiqueta ni cifra del bot sobre un día reservado (ADR-0021 §1) |

Remite, como pide el encargo, a las filas de lo que cada `make check` ya lee: la del 2026-10-14
(el calentamiento del arnés, `arnes.dias_de_mercado`) y la del 2026-10-27 (los dos tests con el
motor nuevo); la deuda de `PROJECT_STATE.md:111` cita las del 2026-10-18 y 2026-10-26, y la del
10-27 remite a ellas (auditor, #31 y H4).

### 0.d Recuentos de partida: días dev y operaciones del trader por mes, y qué viene de vídeo

Contados hoy por la compuerta del arnés (`arnes.dias_de_construccion(repo, criterio, [mes])`, que
veta cualquier caso oculto; `casos_reservados` 0 en los cuatro meses, comprobado antes):

| Mes | días dev | primer y último día | operaciones del trader | sesiones con operaciones |
|---|---|---|---|---|
| 2026-01 | 21 | 2026-01-02 .. 2026-01-30 | 54 | 30 |
| 2026-04 | 21 | 2026-04-01 .. 2026-04-29 | 35 | 23 |
| 2026-07 | 13 | 2026-07-01 .. 2026-07-17 | 67 | 25 |
| 2026-08 | 21 | 2026-08-03 .. 2026-08-31 | 42 | 26 |
| total | 76 | | 198 | 104 |

Los mismos 76 y 198 que R3.1 (`CORRIDA-CONSTRUCCION.md:273-279`) y que la NOTA de ADR-0070 (`:75`);
las 104 sesiones son las que PUNTO-USADO clasifica («104 sesiones con rn003»). Los `cupos.dev` de
los repartos (`knowledge/cases/visto/<mes>/particiones.yaml`): 21, 21, 13 y 21.

**Qué viene de vídeo**, verificado contra `ACTIVAR-SESION-05.md` §0.b.7 (`:288-312`) y
`knowledge/corpus/fuentes.yaml` (`naturaleza`, solo metadatos): **enero** no (v4 es una entrevista
sobre el backtest, `fuentes.yaml:32`); **abril** un solo día grabado, el 29 (v5, `:38`); **julio**
«sí, según el trader» (v11-v13, `:124-145`, «no comprobado: lo comprueba la rama que lo transcriba»;
T de la Next Action); **agosto** no el libro que hay: v7 y v8 graban la segunda mitad de agosto pero
su exportación no ha llegado (NA:Q, `PROJECT_STATE.md:50`), así que sus casos dev siguen saliendo del
xlsx. Para la lista «Para S-14» la columna «viene de vídeo» va por día en abril (solo el 29) y
«según el trader» en todo julio; enero y agosto, no.

### 0.e `patrones.py` sobre una salida sin rótulo: medido

`anexos/CORRIDA-CONSTRUCCION/patrones.py:57-58` corta cada línea por el primer `"] "`
(`_cuerpo = ln.split("] ", 1)[-1]`) y busca `POR_SESION` en lo que queda. Las líneas «Por sesion»
llevan `"] "` en su propio cuerpo (`arnes.py:319`: `{hecho}:no[{productoras}]` seguido de espacio),
así que sin rótulo el corte se come el principio de la línea. Medido con `medir_patrones_rotulo.py`
(carpeta de trabajo) sobre la diaria commiteada de PUNTO-USADO (con rótulo) y una copia sin rótulo
escrita fuera del repo:

- con rótulo: `_cuerpo` empieza por `2026-01-02 07-11 | trader 2 | bot ` y `POR_SESION` casa (sesgo
  `insuficiente`); sin rótulo: `_cuerpo` empieza por `detenido_por_tope:no[productoras s` y
  `POR_SESION` NO casa; la línea sin rótulo lleva `"] "` en su cuerpo: `True`;
- con rótulo: 364 filas, **104 sesiones con rn003**; P1 44, P2 33, P3 60, P4 40, P5 115, P6 51,
  P7 3, T0 18 (lo mismo que `anexos/PUNTO-USADO/patrones.txt`);
- sin rótulo: 364 filas, **0 sesiones con rn003**; **P1 180**, P5 115, P6 51, T0 18; P2, P3, P4 y P7
  desaparecen.

Así que el efecto es el que dice el encargo con un matiz del auditor (#36): caen en P1 solo las
filas del trader sin pareja (`patrones.py:108-112`; T0, P5 y P6 no miran el sesgo), y la señal que
lo delata es la cabecera, «0 sesiones con rn003» (`:169`). **Sobre la corrida 1 de esta rama, que
sale sin rótulo, el guion de `main` habría dado un P1 falso**: por eso la copia de
`anexos/RECORRIDA-CONSTRUCCION/` corta el rótulo solo si la línea empieza por `[DIAGNOSTICO`, como
manda el encargo (`comun_visor.py:153` corta si empieza por `[`; el efecto es el mismo sobre estas
salidas y se sigue la regla del encargo), con las reglas de clasificación literales, y con un test de
humo sobre una línea «Por sesion» real con rótulo y otra sin él. **Herencia del auditor (H2)**:
`patrones.py:45-46` importa `horas_perdidas` de su propio directorio; copiado solo, falla al
importar: la copia va con `horas_perdidas.py` (idéntico: las 18 horas no han cambiado, §0.b), o
importa el de R3.1 por ruta. PARADA, punto 3.

### 0.f La lista de la decisión 5: cómo se obtienen las zonas y dónde estaba la orden

**Lo que da la salida y lo que no.** «Diferencias por operacion» da, por fila, quién, día, sesión,
lado, instante, entrada y resultado (`patrones.py:66-67`); «### Ordenes» da por orden día, sesión,
id, colocada, precio, resultado, motivo, instante del resultado, lote, distancia, margen, riesgo,
lote del riesgo, límite, **punto (`nivel@inicio`) y caja 1** (`cableado.py:798-802`, `:869-926`);
«Rechazos por motivo» da recuentos por mes (`:966-989`). **Ninguna da las zonas de control
formadas desde la toma, ni el instante de la toma del escenario** (`traza.fijados` con
`liquidez_tomada` no se imprime: `arnes.informe` solo cuenta hechos producidos por sesión,
`:312-319`). Así que la lista no sale de las salidas solas: hace falta el motor.

**Cómo las calcula el motor.** RN-009 lee `zonas_desarrolladas_superan` (`engine/zonas.py:466-481`):
toma `toma["instante"]` de la memoria de la sesión, `m1 = datos.m1_entre(toma - LOOKBACK_M1,
instante)`, el índice de la vela de la toma, y `zonas_de_control(m1, idx_toma, len(m1) - 1,
lado) > tope` (`domain/estructura_m1.py:153-170`: los pivotes de M1 en el sentido de la entrada
formados después de la primera vela del impulso, con `_pivotes_m1`, que desde ADR-0085 salta las
velas sin cuerpo). La orden nace en `zona_del_punto` (`zonas.py:363-412`): `ultimo_punto_de_ruptura(m1,
lado, hasta)` con `hasta = idx_toma + 1` si `orden_stop_punto = referencia_de_la_toma`, o `None` (el
último pivote con TODAS las M1 cerradas) con `ultimo_pivote_m1`, que es el valor vigente
(`parametros.yaml:687-689`, DEFAULT_AMBIGUOUS bajo A-48); cada punto es la clave
`nivel@contraria_inicio` (`:388`) y cada caja distinta de ese punto, con `caja_se_fija =
en_cada_cierre_m1`, una zona nueva (`:394-398`); `punto_de_zona[id]` guarda la clave (`:407`) y la
zona se liga al escenario vigente (`:408`, `escenario["zonas"]`). El escenario guarda su toma
(`_abrir`, `:217-227`: `instante`, `nivel`, `lado`, `pivote`). **RN-006 reubica cancelando** la
orden pendiente y dejando que RN-011 y RN-015 coloquen otra en la zona nueva, con otro id
(`primitivas_broker.py:755-761`; `strategy_spec.yaml:1390-1395`): la llenada es siempre la ÚLTIMA
orden de su escenario, y las anteriores salen en «Ordenes» como `cancelada` con motivo «reglas
disparadas en ese cierre: RN-006, …» (`cableado.py:174-191`). El cableado guarda por orden su zona
(`ctx.zona_de_orden[id] = z.id`, `primitivas_broker.py:652`), que `TrazaBroker.zona_de_orden` comparte
(`cableado.py:291`), y la posición abierta de cada orden llenada (`broker.posiciones`, `orden_id`,
`abierta_ms`). El punto de la referencia se distingue del primero tras la toma por su
`contraria_inicio`: el de la referencia se forma con `m1[:idx_toma + 1]`, así que su vela contraria
empieza ANTES del cierre de la toma; los puntos posteriores tienen `contraria_inicio >=
toma["instante"]`.

**La forma por defecto del consultor, medida como viable sin tocar `src/`**: un guion
`anexos/RECORRIDA-CONSTRUCCION/entradas_antes_alternancia.py` que construye el motor EXACTAMENTE como
`cli.motor_arnes` (`cli.py:2384-2447`: criterio, registro, config, vocabulario,
`arnes.dias_de_construccion`, `diagnostico.lectura_pivote(registro)`, `perfil_del_repo`,
`tope_del_registro`, `lectura_limpia`, `lectura_tipo_orden`, `arnes.dias_de_mercado`,
`construir_motor_cableado`), con `motor.cuenta_diaria = True` y sin ningún `Diagnostico` fijo (el de
`comun_visor.py:37-39` hoy se rechaza, §0.a), corre `arnes.correr` sobre los cuatro meses y después
LEE, por día: `motor.brokers[dia]` (órdenes y posiciones), `motor.trazas_broker[dia]`
(`zona_de_orden`, `cancelaciones`), `motor.estados[dia]` (la memoria del productor:
`zonas._de_la_sesion(estado, sesion)["escenarios"]`, `punto_de_zona`, `zonas.zonas_del_dia`) y las
M1 por `mercado[dia].datos.m1_entre` (`engine/motor.py:143-147`). Para cada orden LLENADA: el
escenario de su zona (`zonas.escenario_de_zona`), la toma de ese escenario, el índice de la vela de
la toma en las M1, y `zonas_de_control(m1, idx_toma, idx_ultimo_cierre_antes_del_llenado, lado)`
(las M1 cerradas hasta el último cierre anterior al `abierta_ms` de la posición: lo que RN-009 vería
en ese cierre); y, para «dónde estaba», la clave del punto de su zona frente a la toma (referencia /
primer punto tras la toma / posterior) y cuántas órdenes anteriores del mismo escenario se cancelaron
por RN-006 antes de ella. Nada de esto decide: solo lee la memoria del motor después de correr, como
`traza_por_cierre.py` (`:329-357`) y `cableado._punto_y_caja` (`:853-866`).

**Esto reproduce la corrida 2 (cuenta diaria) y no la 1**: con `cuenta_diaria` el cableado reinicia
cuenta, seguidor del tope y racha cada día (`cableado.py:248-249`), que es lo que la corrida 2 hace;
el guion lo dice en su cabecera y **comprueba que sus órdenes llenadas coinciden una a una (día,
sesión, id, colocada, precio, instante del llenado, punto, caja 1) con las filas `llenada` de
«### Ordenes» de `diaria.DIAGNOSTICO.cuenta=diaria.txt`**, y sale con 3 (PARADA) si difieren, como
`traza_por_cierre.py:176-182`. Coste: otra corrida entera (~6-9 min, §0.j), que no es ninguno de
los tres comandos del arnés: es el comando del guion que la PARADA fija (punto 2). Si el consultor
prefiere que el guion corra ADEMÁS con la cuenta arrastrada para marcar qué llenadas existen también
en la corrida 1, es otra corrida más; la lista «Para S-14» no lo necesita (lo lee del fichero de la
corrida 1: curva de equity, veredicto y «Ordenes»).

**Lo que imprime y lo que no.** Por fila: día, sesión, id de la orden, instante del llenado, lado,
zonas al llenar (y al colocar), dónde estaba (con la clave del punto, `nivel@inicio`, que ya
imprime «Ordenes»), reubicaciones, resultado en R (de «Diferencias por operacion») y si la empareja
el trader. El instante de la toma y la clave del punto son del día dev: la toma ocurre dentro de una
sesión (desde las 05:00Z/06:00Z) y la referencia se busca en las 240 M1 anteriores (`LOOKBACK_M1`,
`zonas.py:115-117`), así que ninguno es anterior a las 00:00Z del día; aun así el guion aplica
`antes_del_dia` (como `comun_visor.py:76-78`) y escribe «(antes del dia)» si alguno lo fuera. No
imprime ninguna H4, ningún pivote de M15 ni ninguna vela. El guion carga las M1 por los cargadores
del motor, sin nombrar `data/` (la raíz sale de su propia ruta, como `comun_visor.py:21`): si la
guardia lo niega, PARADA con la alternativa, sin rodearla.

**La regla de asignación de las dos columnas, para la PARADA (auditor, #22).** En S-10 la orden se
coloca en el punto de la referencia y RN-006 la reubica AL primer punto tras la toma, donde se llena
(`ACTIVAR-SESION-05-MOTOR.md:178`): es a la vez «primer punto tras la toma» y «reubicada»; S-10b se
reubica dos veces y se llena en un punto posterior (`:179`). Las tres categorías del encargo no se
excluyen. Propuesta: la columna «dónde» dice la POSICIÓN del punto de la orden llenada (referencia /
1.er punto tras la toma / posterior, por `contraria_inicio` frente a la toma) y una columna aparte
«reubicaciones» cuenta las órdenes anteriores del escenario canceladas por RN-006 (S-10: 1.er punto, 1
reubicación, 0 zonas; S-10b: posterior, 2 reubicaciones, 1 zona). Así «una reubicada sale como
reubicada» (fase 1) sin perder dónde se llenó.

### 0.g La línea base: qué cubre, cuándo entró y quién la nombra

- `docs/validation/CABLEADO-SIMULADOR-LINEA-BASE.txt` entró en git en **a0d0599, 2026-09-26**
  (`git log --format='%h %ad' -- <fichero>`: un solo commit), escrito con `motor arnes --simular
  --salida …` (320,5 s, 247,5 MiB; `CABLEADO-SIMULADOR.md:174-175`). Anterior a ADR-0069 (la rejilla,
  2026-10-06), ADR-0070 (2026-10-07), ADR-0075 y ADR-0080 (el sesgo por color, 2026-10-17).
- **Qué cubre** (leído entero, 162 líneas): `CONJUNTO: construccion (2026-04, 2026-08); dias 42;
  sesiones con operaciones del trader 49` (`:4`); operaciones del trader 77, del bot 0, cobertura
  0/77, precisión sin definir (`:7-11`); embudo con `sesgo 49 de 49` y cinco paradas NO_IMPLEMENTADA
  (`:16-29`); reglas disparadas (`:31-35`); seis avisos de orden (`:37-43`); «RN-003 al abrir la
  sesion: por sesion alcista 21; ambiguo 6; bajista 22; por operacion a favor 58; ambiguo 7; en contra
  12» (`:45-47`); 49 líneas «Por sesion» SIN rótulo y con el formato viejo (`:49-98`); la simulación
  (EN_CURSO, saldo 100000, 42 días de curva, `eventos: 0`, `rechazos del broker: 0`, `huecos con
  nombre: acumulador:perdida_dia, acumulador:perdida_semana`, `:100-162`). **No tiene** «Diferencias
  por operacion», «Ordenes», «Rechazos por motivo», «Peticiones», el freno, los cierres ni la línea
  de veredicto de ADR-0070 (todas posteriores).
- **Qué es comparable en el `diff`, y qué cambia por qué** (medido sobre el formato de hoy,
  `arnes.informe` y `cableado.informe_simulacion`): (1) la línea CONJUNTO difiere entera (cuatro
  meses, 76 días, 104 sesiones frente a dos, 42 y 49): cambia por construcción; (2) las operaciones
  del trader de abril y agosto son las mismas 77 (35 + 42, §0.d), pero el total dirá 198: cambia
  por construcción; (3) «RN-003 al abrir» es un agregado de TODAS las sesiones (`arnes.py:347-376`),
  no por mes, así que no se parte en el `diff`: abril y agosto solo se aíslan por sus líneas «Por
  sesion» (auditor, #45), y **el sesgo cambió por el MOTOR**, no solo por construcción: las sesiones
  van por la rejilla H4 (ADR-0069), la H4 neutra con doble ruptura no decide (ADR-0075) y el sesgo
  cambia solo si rompe y cierra del color (ADR-0080: ocho sesiones cambiaron, `SESGO-H4-COLOR.md`); el
  informe comparará el rn003 de las 49 sesiones de abril y agosto línea a línea, con un guion que lea
  las dos salidas; (4) el embudo y las paradas: la línea base paraba en `perdida_dia`, `perdida_semana`,
  `alcanza_nivel`, `cruza` y `toca_colocar_orden_limite` (A-44, A-35 y A-21 sin valor); hoy ninguna
  es hueco: cambia por el motor; (5) la simulación: `eventos: 0` frente a las órdenes de hoy; cambia
  por el motor; (6) los seis «Avisos de orden dentro de una clase» (`:37-43`): comparables en las
  sesiones de abril y agosto si siguen. Lo que la línea base NO tiene no se compara: se describe.
- **Quién la nombra como vigente** (grep de `LINEA-BASE` sobre rutas literales): `ACTIVAR-A35-A44.md:208`
  (el `diff` de §5) y `:241` («contra la línea base vigente»); `CORRIDA-CONSTRUCCION.md:457` y `:483`
  (respuesta a la PARADA de la fase 0 de R3.1, punto 5: «HER:30 y HER:35 siguen apuntando a
  CABLEADO-SIMULADOR-LINEA-BASE.txt hasta que A-35 y A-44 tengan valor», que ya lo tienen);
  `PLATAFORMA-ADELANTADA.md:211` (la cita); `PREPARACION-A35-A44.md:107` y `:184`;
  `CABLEADO-SIMULADOR.md:25` y `:174`; `PROJECT_STATE.md:52` (la V); `ACTIVAR-SESION-05.md:446`,
  `:1101`; `ACTIVAR-SESION-05-MOTOR.md:779`. **Nada en `tests/`, `src/`, `scripts/` ni
  `docs/plan/HOJA-DE-RUTA.md`** (grep vacío en los cuatro). Así que nada ejecutable la lee: cambiar la
  vigente es cambiar documentos.
- **La opción por defecto del consultor** (la salida de la corrida 1 pasa a ser la línea base
  vigente tal como queda en anexos, sin copia, y `ACTIVAR-A35-A44.md` gana una NOTA al principio de
  §5 que lo diga y declare la desviación del visor) toca un fichero fuera del contrato
  (`docs/runbooks/` está en `rutas_protegidas`): se amplía el contrato solo a ese runbook, en el
  commit de la NOTA, después de la fase 2 (la NOTA nombra un fichero que aún no existe). Matiz del
  auditor (#8): ningún régimen de CLAUDE.md declara inmutable la línea base vieja; lo que hay es la
  práctica de «no se tocan» (`CABLEADO-SIMULADOR.md:174-176`) y `rutas_protegidas` del contrato
  (`contrato.yaml`), que es lo que esta rama aplica. PARADA, punto 4.

### 0.h Herencias

Con `grep -n "re-corrida"` sobre `docs/plan/HOJA-DE-RUTA.md`, `docs/runbooks/`, `docs/adr/`,
`docs/validation/*.md` y `PROJECT_STATE.md`:

| Dónde | Qué hereda esta rama | Cómo se recoge |
|---|---|---|
| HOJA-DE-RUTA R4.1, Estado (`:223-227`) | «Queda la re-corrida de ADR-0070 §3 con su `diff` (ACTIVAR-A35-A44.md §5.1), que mire las entradas que nacen en el primer punto tras la toma y se llenan antes de la alternancia» | las dos corridas, el `diff` y la lista de la decisión 5; R4.1 pasa a HECHA en el cierre |
| HOJA-DE-RUTA R4.2 (`:229-250`) | «S-14 con los días de construcción que dé la re-corrida» (`:234`); «Depende de: la re-corrida del arnés (R4.1, lo que queda)» (`:248`); `NA:V` en Refs (`:230`) | la lista «Para S-14»; en el cierre, «Depende de» sin la re-corrida, los recuentos de las dos listas en «Qué es», NA:V fuera |
| HOJA-DE-RUTA R5.2 (`:266-272`, auditor H1) | «Depende de: R3.1, con una corrida que cuente» (`:270`); `ACTIVAR-SESION-05.md:1149-1151` ya dice que esa corrida es esta re-corrida | línea del cierre nueva: R5.2 depende del veredicto de la corrida 1 de esta rama (R4.1), no de R3.1. PARADA, punto 6 |
| `ACTIVAR-A35-A44.md` §5 (`:204-217`) y §5.1 (`:219-255`) | el `diff` contra la línea base vigente; «mirada con el visor» (`:209`, `:238`); cifras de referencia de R3.1: `liquidez_tomada` 98 y 97 de 104 (`:236`), RN-020 «con `sin_tope`, 0 de 104» (`:254`); la NOTA del 10-26 (`:221-226`): «lo demás de esta sección … sigue pendiente y es lo que queda de R4.1» | el `diff`; el visor NO se abre (desviación declarada, encargo); el informe da `liquidez_tomada` y `detenido_por_tope` sobre las 104 sesiones frente a esas cifras (auditor H5); la NOTA de §5 (PARADA, punto 4) |
| `ACTIVAR-SESION-05.md` §3, punto 12 (`:1059-1064`) y §5 (`:1100-1102`, `:1131`, `:1143-1151`) | S-14: «los días de construcción en que el bot opera y él no … cuando la re-corrida tras la rama de motor los dé»; las líneas del cierre que nombran la re-corrida | la lista «Para S-14», por día y sesión (P6 de la corrida 2) |
| `ACTIVAR-SESION-05-MOTOR.md` §0.b.8 (`:170-190`), §2 punto 5 (`:750-760`), §3 (`:779-781`, `:793-795`) | la serie S-10 entra por el camino real antes de la alternancia; el dibujo 3 de S-15; «QUEDA la re-corrida … después la sesión 6» | la lista de la decisión 5; V sale en el cierre |
| ADR-0076 §2, NOTA (`:74-80`) y ADR-0085 §4 (`:93-99`) | «la re-corrida de ADR-0070 §3 lo mira» / «la re-corrida lo mira» | la lista de la decisión 5; sin NOTA nueva en los ADR (nada se decide) |
| ADR-0070 §3, NOTA del 10-26 (`:81-88`) | «la corrida … es la re-corrida que sigue a la rama de motor» | la corrida 1; su veredicto literal en una NOTA fechada al ADR, si la PARADA 2 lo aprueba |
| `PROJECT_STATE.md` V (`:52`) y F (`:32`) | «QUEDA la re-corrida … después la sesión 6 (R4.2)»; «F. La re-corrida del arnés (ADR-0070 §3); después la sesión 6; R6a en los huecos» | las líneas del cierre (§0.k) |
| ADR-0080 `:87`, `:239` y ADR-0081 `:192` | «la re-corrida» de W y de E | HECHAS en sus ramas (SESGO-H4-COLOR.md §4, MARGEN-LOTE.md §4): no son de esta |

### 0.i Lo que el arnés hace ahora y antes no; qué reinicia la cuenta diaria

- **RN-020 evaluado** (`strategy_spec.yaml:2008-2047`): `perdida_trader_alcance = dia` (CONFIRMED,
  S-4), `perdida_trader_unidad = porcentaje` (CONFIRMED), `perdida_trader_magnitud = saldo`
  (DEFAULT_AMBIGUOUS bajo A-44, `parametros.yaml:1475-1477`), `perdida_maxima_diaria = 4.5` sobre
  `saldo_inicial_dia`; el huso de reinicio es el del perfil, `Europe/Prague`, marcado SUPUESTO
  (`tope_trader.py:191-194`, `:76`; descripción medida en §0.a). El seguidor corta a medianoche de
  ese huso (`SeguidorTope.avanzar`, `:230-240`) y da `perdida_dia` sobre el SALDO (`:255`, `:270-274`).
  En la salida: `TOPE DEL TRADER (RN-020, A-44): …` (`cableado.py:733-734`), `detenido_por_tope: N de
  104` en el embudo, `detenido_por_tope:si` y `disparadas … RN-020` en «Por sesion», y
  `PRIMERO EN TOCAR UN LIMITE` (`:737`). Antes (R3.1 y PUNTO-USADO) corría con `sin_tope`: 0 de 104.
- **ADR-0086**: la forma de RN-020 gana `retirar_ordenes_pendientes` (`strategy_spec.yaml:2015`);
  cada retirada sale en «Ordenes» como `cancelada` con motivo «reglas disparadas en ese cierre:
  RN-020, …» (`cableado.py:174-191`, `:892-897`): se cuentan por ese motivo.
- **RN-036** con `racha_perdidas_reinicio = tras_la_detencion` (CONFIRMED, `parametros.yaml:1359-1360`;
  `racha_perdidas_max = 9`): `RACHA DE PERDIDAS (RN-036, A-51): …` (`cableado.py:735-736`),
  `detenido_por_racha` en el embudo y «Por sesion» (la línea real medida en §0.e lo trae), y las
  cancelaciones con RN-036 en el motivo.
- **RN-037** (`strategy_spec.yaml:1042-1050`, `cierre_h4_antelacion = 1`): «en el ultimo tramo de la
  vela H4» en el motivo de las cancelaciones (`cableado.py:188-189`) y `RN-037` en `disparadas`.
  Auditor (#50, #58): también **RN-035 retira un minuto antes del fin de la H4** desde esa rama
  (recuadros en ADR-0060 §5-§6 y ADR-0066 §4): va a la lista de cambios que separan estas corridas
  de las de PUNTO-USADO.
- **El embudo** trae hoy cuatro frenos (`detenido_por_tope`, `detenido_por_tope_total`,
  `detenido_por_cartuchos`, `detenido_por_racha`); las líneas ya estaban en PUNTO-USADO (tope 0 de
  104, cartuchos 1 de 104): lo nuevo es que `detenido_por_tope` pueda encenderse (auditor, #50).
- **Los parámetros DEFAULT_AMBIGUOUS con los que corre la corrida que cuenta** (leídos del registro,
  `parametros.yaml`, 12):

  | Parámetro | Valor | Ambigüedad | Categoría |
  |---|---|---|---|
  | `liquidez_m15_mecha_que_vuelve` | `cualquier_mecha` | A-35 | estrategia |
  | `perdida_trader_magnitud` | `saldo` | A-44 | estrategia |
  | `orden_stop_punto` | `ultimo_pivote_m1` | A-48 | estrategia |
  | `caja_bloque` | `r6` | A-48 | estrategia |
  | `caja_se_fija` | `en_cada_cierre_m1` | A-49 | ejecucion |
  | `caja_lado_de_ruido` | `caja_entera` | A-50 | estrategia |
  | `orden_pendiente_al_abrir_escenario` | `se_mueve` | A-53 | estrategia |
  | `freno_peticiones_aviso` | 1000 | A-54 | ejecucion |
  | `freno_peticiones_corte` | 1500 | A-54 | ejecucion |
  | `freno_bucle_repeticiones` | 5 | A-54 | ejecucion |
  | `freno_bucle_minutos` | 1 | A-54 | ejecucion |
  | `cierre_pendientes` | `cancelar` | A-55 | ejecucion |

  Y tres UNKNOWN que el motor suple: `perdida_trader_reinicio_huso` (el huso del perfil, SUPUESTO),
  `perdida_trader_dia_usd` y `perdida_trader_semana_usd` (no se leen con `porcentaje`).
- **Qué reinicia la cuenta diaria cada día** (`cableado.py:248-249`): `self.cuenta, self.seguidor,
  self.racha = None, None, None`: la cuenta viva (saldo, equity, estado, días de trading), el
  seguidor del tope (sus cortes y el saldo de corte) y la racha de pérdidas (RN-036); y la curva, el
  veredicto y `PRIMERO EN TOCAR` son solo del último día (`:739-743`). Lo que NO reinicia: la memoria
  del productor es de cada día de todos modos (`EstadoDia`, nace y muere con el día).

### 0.j Tiempo y memoria esperados

- PUNTO-USADO §4 (`:463-467`): 504,3 s / 467,0 s / 363,9 s y 631,8-634,2 MiB por corrida, con el
  motor de ADR-0083 (tres corridas y la repetición: unos 30 min de arnés).
- ACTIVAR-SESION-05 §0.b.2 (`:163-166`): solo abril con `--simular`, 171,5 s y 235,2 MiB, pero con
  el motor de la rama de SPEC (sin ADR-0084 a 0086, RN-037, la racha ni la caja entera: auditor,
  #53), no con el de hoy.
- Para esta rama: tres corridas del arnés (1, 2 y la repetición de la 1) a unos 6-9 min y ~630 MiB
  cada una, el guion de f) (otra corrida entera, ~6-9 min) y dos `make check` más (17,5 min cada uno
  hoy: 1047,6 s, `PICO DE MEMORIA` 298 MiB): **unas dos horas de máquina, que caben en una sesión**,
  una cosa a la vez y nunca a la par de un `make check`. En segundo plano con
  `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1` (comprobado: `1`); si una muere por memoria, no se
  relanza sin decirlo.

### 0.k El encargo frente al repo (informe del auditor, 2026-10-27)

El auditor del encargo (`.claude/agents/auditor-encargo.md`) contrastó 60 afirmaciones: **45
correctas, 0 incorrectas, 15 con matiz**, y 7 herencias no recogidas. Lo que cambia algo de lo que se
pide, con lo que se hace:

| # | Afirmación | Veredicto | Qué se hace |
|---|---|---|---|
| 7 | «ADR-0083 sigue PROVISIONAL» | MATIZ: solo en D1 (`0083-…md:209`) | se escribe así |
| 8 | «CABLEADO-SIMULADOR-LINEA-BASE.txt es evidencia inmutable» | MATIZ: ningún régimen lo declara; práctica + contrato | §0.g; se protege por contrato |
| 22 | las tres categorías de la decisión 5 | MATIZ: no se excluyen; la reubicada es otra orden | §0.f; PARADA, punto 0 |
| 31 | las filas del make check son las del 10-14 y 10-27 | MATIZ: la deuda cita 10-18 y 10-26; y los make check de ESTA rama leen marzo | la fila propuesta remite a las tres y declara los make check de la rama |
| 36 | «todo cae en P1 sin aviso» | MATIZ: solo las del trader sin pareja; la cabecera avisa con «0 sesiones con rn003» | §0.e, medido |
| 37 | «como comun_visor.py» | MATIZ: comun_visor corta si empieza por `[` | se sigue la regla del encargo (`[DIAGNOSTICO`) |
| 38 | «ninguna da las zonas» | MATIZ: «Ordenes» da punto y caja 1 | §0.f los usa para la columna «dónde» |
| 43 | la línea base «no tiene» secciones | MATIZ: trae `rechazos del broker: 0` y los huecos | §0.g |
| 45 | lo comparable del diff | MATIZ: «RN-003 al abrir» es un agregado; el sesgo cambió por el motor | §0.g; el informe compara rn003 por sesión |
| 50, 58 | cambios del motor que separan de PUNTO-USADO | MATIZ: falta RN-035 un minuto antes | §0.i; se añade |
| 53 | «midió solo abril con el de ahora» | MATIZ: motor de la rama de spec | §0.j |
| 56 | «T0 y P1 a P7» | MATIZ: existe «P? solo otro lado» | se tabula también |
| 60 | la F nueva | MATIZ: pasa el test; la rama de la cuarentena no tiene entrada en la hoja | PARADA, punto 6 |
| H1 | R5.2 «Depende de: R3.1, con una corrida que cuente» | herencia | PARADA, punto 6 |
| H2 | la copia de patrones.py importa horas_perdidas.py | herencia | PARADA, punto 3 |
| H5 | las cifras de referencia de §5.1 (98/97 de 104; 0 de 104) | herencia | el informe las compara |
| H6, H7 | la zona reutilizada en un escenario nuevo; la orden del primer cierre cotizada con el respaldo M1 | opcionales, sin dueño | el guion de f) deja la traza; «posible M» marca lo del respaldo |

Lo que el auditor no pudo comprobar y esta fase 0 sí midió: los 11 casos reservados de junio hoy
(§0.c); que la corrida entera salga con código 0 con el motor de hoy sigue sin medir (es la fase 2).

### 0.l Lo que no pude medir

- Si la guardia deja correr el guion de f) (carga velas por los cargadores del motor) y la
  redirección del `diff` a fichero: se sabe al ejecutarlos; si niega, PARADA con el comando.
- Si la corrida entera sale con código 0 con el motor de hoy (solo hay evidencia de abril con el
  motor de la rama de spec y de `test_preparar_a35.py` sobre abril en cada make check).
- Cuánto tardará cada corrida con RN-020 evaluado: se copian las líneas TIEMPO y MEMORIA.

### 0.m Exposiciones

**Ninguna de holdout en la fase 0**: ningún libro, imagen, fotograma ni transcripción; nada de marzo,
mayo, junio, septiembre, diciembre ni febrero; ninguna vela leída (el arnés no se ha corrido). Lo
leído, material de desarrollo y recuentos, va en el punto (1) de la fila propuesta en §0.c, que se
escribe en la fase 1 en su propio commit, ANTES de correr nada, como manda el encargo.

## Lo que necesito que decidas

0. **Las dos columnas de la decisión 5** (§0.f). Opciones: (a) «dónde» = posición del punto de la
   orden llenada frente a la toma (referencia / 1.er punto tras la toma / posterior, por
   `contraria_inicio`), y una columna aparte «reubicaciones» con las órdenes del escenario
   canceladas por RN-006 antes de ella (S-10: 1.er punto, 1 reubicación, 0 zonas; S-10b: posterior,
   2, 1 zona); (b) las tres categorías del encargo tal cual, con «reubicada» absorbiendo a las
   otras dos cuando hubo RN-006. Recomiendo (a): no da dos respuestas y conserva lo que el dibujo 3
   pregunta (dónde se llenó). Coste de (b): S-10 y S-10b saldrían las dos como «reubicada» y se
   perdería en qué punto se llenaron.
1. **«Zonas al llenar»**: con las M1 cerradas hasta el último cierre anterior al instante del
   llenado (lo que RN-009 vería en ese cierre), y además una columna «zonas al colocar» (en el
   cierre que colocó la orden llenada). Opciones: (a) las dos columnas, la lista filtra por «al
   llenar» < 2; (b) solo «al llenar». Recomiendo (a): cuesta una columna y enseña si RN-009 pudo
   morder al colocar. Coste de (b): ninguno de medida; menos contexto.
2. **El comando literal del guion de f)**, que reproduce la corrida 2 y compara sus llenadas con
   «Ordenes» de la diaria commiteada:
   `uv run python docs/validation/anexos/RECORRIDA-CONSTRUCCION/entradas_antes_alternancia.py --diaria "docs/validation/anexos/RECORRIDA-CONSTRUCCION/diaria.DIAGNOSTICO.cuenta=diaria.txt" --salida docs/validation/anexos/RECORRIDA-CONSTRUCCION/entradas-antes-alternancia.txt`
   Opciones: (a) ese comando, una corrida (cuenta diaria); (b) además `--arrastrada` con una segunda
   corrida para marcar qué llenadas existen en la corrida 1. Recomiendo (a): la lista «Para S-14» lee
   lo de la cuenta arrastrada del fichero de la corrida 1. Coste de (b): otros 6-9 min y un guion
   que corre dos motores.
3. **La copia de `patrones.py`** (§0.e, H2). Opciones: (a) copiar a `anexos/RECORRIDA-CONSTRUCCION/`
   `patrones.py` (con el corte del rótulo solo si la línea empieza por `[DIAGNOSTICO`, y ninguna
   regla más) y `horas_perdidas.py` idéntico (las 18 horas no cambian, §0.b); (b) la copia de
   `patrones.py` importa `horas_perdidas` de `anexos/CORRIDA-CONSTRUCCION/` por ruta. Recomiendo (a):
   la carpeta queda completa y el guion corre solo. Coste de (b): un anexo que depende de la
   carpeta de otra rama.
4. **La línea base** (§0.g). Opciones: (a) la del encargo: `cuenta-arrastrada.txt` en anexos pasa a
   ser la vigente, sin copia, y `ACTIVAR-A35-A44.md` gana una NOTA al principio de §5 (contrato
   ampliado a ese runbook solo para la NOTA, en un commit propio tras la fase 2, porque nombra un
   fichero que aún no existe) que diga la nueva vigente, que el `diff` de esta rama compara lo
   comparable de §0.g, y la desviación del visor; (b) además copiar la salida a
   `docs/validation/RECORRIDA-LINEA-BASE.txt`. Recomiendo (a). Coste de (b): dos copias del mismo
   fichero.
5. **La fila de HOLDOUT-EXPOSICIONES** (§0.c), tal como está propuesta, en el primer commit de la
   fase 1 con el README de la carpeta. Opciones: (a) así; (b) con cambios que digas. Recomiendo (a).
6. **Las líneas del cierre que el auditor echa en falta** (H1, H3): (a) la F del encargo tal cual y,
   en el cierre, una entrada nueva en «Carril: guardias y deuda» de la hoja de ruta para la rama corta
   de la cuarentena por condición (la deuda PRIORITARIA de PROJECT_STATE), y R5.2 pasa a «Depende de:
   la corrida que cuenta de R4.1 (esta rama) y su veredicto»; (b) la F sin la rama de la cuarentena
   (que ya está en Technical Debt) y R5.2 igual. Recomiendo (a): la hoja manda el orden
   (`HOJA-DE-RUTA.md:3-19`) y F la nombra primero. Coste de (b): F y la hoja dicen cosas distintas.
7. **El orden de la fase 2** si una corrida muere por memoria o sale con código distinto de 0: PARADA
   con el error literal, sin relanzar, como manda el encargo. Opciones: (a) así; (b) relanzar una vez
   en primer plano antes de parar. Recomiendo (a): es lo que dice el encargo.

## Respuesta del consultor a la PARADA (2026-10-27)

Copiada tal cual:

> Modelo: Fable 5.1 · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA de la fase 0 de trabajo/recorrida-construccion (2026-10-27). Cópiala tal cual al final del encargo y del informe, en «Respuesta del consultor a la PARADA», con su fecha, y aplícala punto por punto (skill fase-cero). Si al aplicar algo lo medido lo contradice, PARADA 2 antes de seguir.
>
> 0. (a). La columna «dónde» da la posición del punto de la orden llenada frente a la toma (referencia / primer punto tras la toma / posterior, por contraria_inicio), y una columna aparte, «reubicaciones», cuenta las órdenes anteriores del mismo escenario canceladas por RN-006. Motivo: las tres categorías del encargo se solapan (S-10 es a la vez primer punto y reubicada), y así no se pierde ninguna de las dos cosas. Añado una marca más: si la zona de la orden llenada pertenece a un escenario distinto del de la toma vigente al llenar (la zona reutilizada en un escenario nuevo, H6 del auditor), la fila lo dice en una columna «escenario», sin cambiar nada más.
> 1. (a). «Zonas al llenar» = zonas_de_control con las M1 cerradas hasta el último cierre anterior al llenado (lo que RN-009 ve en ese cierre), y además «zonas al colocar». Motivo: es exactamente la condición en la que RN-009 muerde.
> 2. (a). Queda autorizado, una sola vez y después de las tres corridas del arnés, este comando literal:
>    uv run python docs/validation/anexos/RECORRIDA-CONSTRUCCION/entradas_antes_alternancia.py --diaria "docs/validation/anexos/RECORRIDA-CONSTRUCCION/diaria.DIAGNOSTICO.cuenta=diaria.txt" --salida docs/validation/anexos/RECORRIDA-CONSTRUCCION/entradas-antes-alternancia.txt
>    Si sus llenadas no coinciden una a una con las «llenada» de «Ordenes» de la corrida 2, sale con 3 y es PARADA: no se ajusta el guion para que coincidan. Nunca a la vez que make check ni que otra corrida.
> 3. (a). La copia de horas_perdidas.py va idéntica, al lado de la de patrones.py. Motivo: la copia la importa, y un fichero idéntico no cambia ninguna regla.
> 4. (a). La línea base vigente pasa a ser la salida de la corrida 1 tal como queda en anexos, sin copia. La NOTA al principio de ACTIVAR-A35-A44.md §5 va en un commit propio después de la fase 2, con el contrato ampliado solo a ese runbook, y declara también la desviación del visor (motor visor --caso no se abre en esta rama). CABLEADO-SIMULADOR-LINEA-BASE.txt no se toca.
> 5. (a). La fila de HOLDOUT-EXPOSICIONES tal como está propuesta en §0.c, en su propio commit, ANTES de correr nada.
> 6. (a), con esta forma para las líneas del cierre:
>    - F tal cual la propone el encargo.
>    - Entrada nueva en la hoja de ruta, en el carril G: «G.5 · La cuarentena por condición», Refs: —; Qué es: la línea PRIORITARIA de Technical Debt (diciembre en meses_libres con NA:I sin decidir, y la fecha numérica seguida de coma que no se tapa; SESION-05-EXTRACCION.md §2.7 y §11, a4); Depende de: nada; Quién: la sesión, con el encargo del consultor; Hecho cuando: los dos casos tienen su test que rompe en main y pasa en la rama, antes de ingerir la sesión 6. Comprueba que test_hoja_de_ruta pasa con ella.
>    - R5.2, «Depende de» pasa a: «la corrida que cuenta (R4.1; ADR-0070 §3) con un "sí", y el ADR propio de la rama de medida (ADR-0070 §6)».
> 7. (a). Si una corrida o el guion mueren o salen con un código distinto de 0 (salvo el 1 del diff), PARADA con el error literal, sin relanzar.
>
> Sigue con la fase 1 (la fila, el README, los dos guiones con sus tests de humo en los dos sentidos y su salida pegada), make check en verde antes de cada commit con ruff format, ruff check y mypy antes, y después la fase 2 y la PARADA 2 con todo commiteado. Si la guardia o el clasificador niegan algo, PARADA con el comando exacto y lo lanzo yo con «!».
>
> Rama lista para revisión, NO cerrada.

## 1. Fase 1 · La fila de exposiciones, el README y los guiones (la respuesta aplicada)

### 1.1 Puntos 5 y 0.c · La fila de HOLDOUT-EXPOSICIONES y el README, en su propio commit

La fila del 2026-10-27 de `docs/validation/HOLDOUT-EXPOSICIONES.md` es la propuesta en §0.c, tal
cual, con una precisión: el guion de f) se nombra por su fichero final
(`entradas_antes_alternancia.py`). Y `docs/validation/anexos/RECORRIDA-CONSTRUCCION/README.md` nace
en el mismo commit con los comandos literales y qué es cada fichero: la carpeta tiene que existir
antes de correr, porque el arnés no la crea (`cli.py`, `salida.write_text`).

### 1.2 Puntos 0, 1, 2 y 3 · Los guiones y su test de humo

Cuatro ficheros en `docs/validation/anexos/RECORRIDA-CONSTRUCCION/`:

- **`patrones.py`**: copia de `anexos/CORRIDA-CONSTRUCCION/patrones.py` con UNA diferencia, medida
  con `diff`: la cabecera que lo declara, la ruta de «Uso» y `_cuerpo`, que corta el rótulo solo si la
  línea empieza por `[DIAGNOSTICO` y lleva `"] "` (`ROTULO`); ninguna regla de clasificación cambia
  (el `diff` no toca ninguna otra línea). Sobre la diaria rotulada de PUNTO-USADO da lo mismo que
  `anexos/PUNTO-USADO/patrones.txt` («364 filas, 104 sesiones con rn003»; P1 44, P2 33, P3 60, P4 40,
  P5 115, P6 51, P7 3, T0 18), y sobre la MISMA salida sin rótulo (la copia de la carpeta de trabajo
  de §0.e) da exactamente la misma tabla, donde el guion de R3.1 daba 0 sesiones y 180 P1.
- **`horas_perdidas.py`**: copia IDÉNTICA (`diff` vacío) de la de R3.1, porque `patrones.py` lo
  importa de su directorio (punto 3).
- **`entradas_antes_alternancia.py`**: el guion de f) (§0.f), con las reglas puras separadas para
  el test: `donde_esta` (referencia / primer punto tras la toma / posterior, por `contraria_inicio`
  frente al cierre de la toma; punto 0), `reubicaciones_antes` (las órdenes anteriores del mismo
  escenario canceladas con RN-006 en su motivo), `en_la_lista` (zonas al llenar < 2),
  `llenadas_de_ordenes` (las filas `llenada` de «### Ordenes», con y sin rótulo). Construye el motor
  como `cli.motor_arnes`, con `motor.cuenta_diaria = True` (reproduce la corrida 2), compara sus
  llenadas línea a línea con las de `--diaria` y sale con 3 si difieren; después lee la memoria del
  motor: `_zonas_hasta` llama a `zonas_de_control` con las M1 cerradas hasta el último cierre anterior
  al llenado (`abierta_ms // MS_POR_MINUTO`) y al colocar (`(colocada_ms + 1) // MS_POR_MINUTO`;
  punto 1), la columna «escenario» marca si la zona es de otro escenario que el vigente al llenar
  (punto 0, H6), R sale del stop con el que nació la posición, y la pareja o el patrón, de la medida
  del criterio y de la copia de `patrones.py` sobre la diaria. Enmascara con «(antes del dia)» todo
  instante anterior a las 00:00Z del día dev. **Ampliado en el commit siguiente** (antes de correr
  nada) con dos columnas más, solo lectura, para la lista «Para S-14»: el sesgo de la sesión (la
  anotación de RN-003 de la traza) y el camino del bot en ella (`camino_de`: el primer instante en
  que la sesión fijó cada hecho, con su regla, enmascarado si es anterior al día), porque las
  sesiones de P6 no tienen línea «Por sesion» en la salida del arnés (`arnes.informe` solo lista las
  sesiones con operaciones del trader, `:293`).
- **`test_humo.py`** (*declarado tras el revisor, b3*: la fase 0 e) pedía una línea «Por sesion»
  «real», y la fase 1, «salidas sintéticas»; el test usa una línea sintética con el formato exacto
  de la real -la de §0.e, recortada a su cabecera y a un `{hecho}:no[...]`- para no depender de un
  fichero de otra rama; la línea real, con rótulo y sin él, se midió en §0.e):
  10 tests sobre salidas sintéticas, en los dos sentidos:
  `uv run pytest docs/validation/anexos/RECORRIDA-CONSTRUCCION/test_humo.py -q` → `..........  [100%]`
  (10 passed; 9 antes de la ampliación). Una llenada con 0 zonas y otra con 1 entran en la lista y su columna lo dice; con 2 o
  con 3, no; una reubicada sale con `1` en la columna de reubicaciones y una no reubicada con `0`;
  `donde_esta` da las tres posiciones (y el cierre de la toma cuenta ya como «tras la toma»);
  `reubicaciones_antes` no cuenta la cancelada por RN-035 ni la posterior; `llenadas_de_ordenes`
  lee solo las `llenada`, con y sin rótulo; la copia de `patrones.py` lee el sesgo de una línea
  «Por sesion» sintética con rótulo y sin él (P4 en las dos) **y el guion viejo de R3.1, cargado por
  ruta, rompe sin rótulo** (0 sesiones y P1 sesgo); `_cuerpo` solo corta `[DIAGNOSTICO`; y
  `camino_de` da el primer instante de cada hecho, salta los apagados y enmascara lo anterior al día.

`ruff format --check`: «4 files already formatted»; `ruff check`: «All checks passed!»; `mypy`
sobre `entradas_antes_alternancia.py` y `test_humo.py`: los únicos dos errores son
`Item "TextIO" of "TextIO | Any" has no attribute "reconfigure"` en `horas_perdidas.py:34` y
`patrones.py:180`, que son las líneas de R3.1 (los originales dan los mismos dos errores,
`CORRIDA-CONSTRUCCION/patrones.py:166` y `horas_perdidas.py:34`): no se tocan, porque la copia de
`horas_perdidas.py` es idéntica por decisión (punto 3) y la de `patrones.py` cambia solo `_cuerpo`.
Los guiones nuevos no tienen ningún error propio de mypy.

## 2. Fase 2 · Las corridas (2026-10-27)

Sobre el código commiteado (74ab3cb, nada de `src/` cambia respecto a `main`), sin `--meses`, una
corrida cada vez y ninguna a la par de un `make check`, en segundo plano con
`CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1`. Los tres comandos literales del encargo y lo que
salió por pantalla, tal cual:

1. `uv run botsito motor arnes --simular --salida docs/validation/anexos/RECORRIDA-CONSTRUCCION/cuenta-arrastrada.txt`
   → `OK: informe del arnes en docs\validation\anexos\RECORRIDA-CONSTRUCCION\cuenta-arrastrada.txt`;
   `TIEMPO: 336.5 s; MEMORIA: pico del proceso de 629.1 MiB`; `exit=0`. Fichero final:
   **`cuenta-arrastrada.txt`** (1.224 líneas; `grep -c DIAGNOSTICO` = 0: sin rótulo).
2. `uv run botsito motor arnes --simular --diagnostico-cuenta-diaria --salida docs/validation/anexos/RECORRIDA-CONSTRUCCION/diaria.txt`
   → `TIEMPO: 299.0 s; MEMORIA: pico del proceso de 638.3 MiB`; `exit=0`. Fichero final:
   **`diaria.DIAGNOSTICO.cuenta=diaria.txt`** (3.507 líneas, todas con el rótulo
   `[DIAGNOSTICO-CUENTA-diaria] `), el nombre que §0.a predijo.
3. La 1 repetida con `--salida` en la carpeta de trabajo de la sesión (fuera del repo) y comparada
   con `diff` contra la commiteada: §2.4.

Ninguna salió con un código distinto de 0, ninguna pidió `--depuracion` ni un día fuera de la
construcción (§0.b: todos los días dev tienen ticks).

### 2.1 La corrida 1, la que cuenta por ADR-0070 §3: el veredicto literal

Línea 13 de `cuenta-arrastrada.txt`, copiada tal cual:

```
habilita medir el conjunto de medida (2026-05) (ADR-0070): no (cobertura 3.5 % por debajo de 70.0 %; precision 13.2 % por debajo de 60.0 %)
```

Dice **«no»**, y por las dos condiciones de umbral, sin ningún motivo de opción (la lista cerrada se
cumplió: ningún «opción fuera de la lista», «sin simulación», perfil ni fase). **Decisión 2 del
consultor (§0.0): se sigue construyendo, mayo no se toca y el umbral no cambia (ADR-0070 §4).** Lo
que la corrida 2 dice en la misma línea: `no (opción fuera de la lista: --diagnostico-cuenta-diaria;
cobertura 20.7 % por debajo de 70.0 %; precision 15.6 % por debajo de 60.0 %)`, como §0.a predijo.

### 2.2 Por corrida y por mes: operaciones del trader, puntuables del bot, parejas, cobertura y precisión

De «### Resumen por mes» de cada salida (el orden es el de `construccion`):

| Corrida | Mes | días | trader | bot puntuables | bot en días sin trader | parejas | cobertura | precisión |
|---|---|---|---|---|---|---|---|---|
| 1 arrastrada | 2026-04 | 21 | 35 | 0 | 0 | 0 | 0/35 (0.0 %) | sin definir (cero operaciones del bot puntuables) |
| 1 arrastrada | 2026-07 | 13 | 67 | 0 | 0 | 0 | 0/67 (0.0 %) | sin definir |
| 1 arrastrada | 2026-08 | 21 | 42 | 0 | 0 | 0 | 0/42 (0.0 %) | sin definir |
| 1 arrastrada | 2026-01 | 21 | 54 | 53 | 0 | 7 | 7/54 (13.0 %) | 7/53 (13.2 %) |
| 1 arrastrada | **total** | 76 | 198 | 53 | 0 | 7 | 7/198 (3.5 %) | 7/53 (13.2 %); parejas en el mismo minuto 5 |
| 2 diaria | 2026-04 | 21 | 35 | 53 | 19 | 7 | 7/35 (20.0 %) | 7/53 (13.2 %) |
| 2 diaria | 2026-07 | 13 | 67 | 56 | 0 | 15 | 15/67 (22.4 %) | 15/56 (26.8 %) |
| 2 diaria | 2026-08 | 21 | 42 | 73 | 9 | 12 | 12/42 (28.6 %) | 12/73 (16.4 %) |
| 2 diaria | 2026-01 | 21 | 54 | 81 | 0 | 7 | 7/54 (13.0 %) | 7/81 (8.6 %) |
| 2 diaria | **total** | 76 | 198 | 263 | 28 | 41 | 41/198 (20.7 %) | 41/263 (15.6 %); parejas en el mismo minuto 26 |

**Por qué la corrida 1 solo opera en enero.** El arnés corre los meses en orden de fecha
(`validar_meses` devuelve `sorted`, `arnes.py:121`): enero primero. Con la cuenta arrastrada, el
saldo baja de 100.000 a 90.741,16 el 2026-01-20 (curva: `2026-01-20 | 92415.29 | 90741.16`;
mínimo del tramo; máximo 102.686,13 el 2026-01-06). En la sesión 11-15 de ese día la corrida 1 aún
llena o6, o7 y o13; después de la última, **RN-032** («no se abre una operación cuyo riesgo no cabe
antes del límite de la firma», `strategy_spec.yaml:2491-2499`: la pérdida total más el riesgo de la
operación llega al límite menos `firma_margen_seguridad`) prohíbe `abrir_operacion` en todos los
cierres: desde `2026-01-21 07-11` hasta `2026-08-31` ninguna sesión llena nada, y cada línea «Por
sesion» de esas fechas con `orden_dimensionada:si` acaba en `bloqueadas
RN-015:accion:colocar_orden_limite:prohibida:abrir_operacion`, con RN-032 entre las disparadas (128 de
152 sesiones). *Corregido tras el revisor, a4: la primera redacción decía que RN-032 prohibía desde
la sesión 11-15 del 2026-01-20 entera, y daba los 96 bloqueos de las 104 sesiones como medida de
RN-032; ese bloqueo aparece también en 16 sesiones de enero anteriores al 2026-01-20 (el
`prohibida:abrir_operacion` lo dan también otras reglas, p. ej. con una posición viva), así que no
mide solo RN-032.* El límite total de la firma no arrastra
(`firma_perdida_total_arrastra = false`), así que una vez gastado el 10 % menos el margen no vuelve a
caber ninguna operación. **La cuenta no corta el tramo** («Veredicto de la cuenta: estado EN_CURSO;
motivo: sin objetivo alcanzado ni limite infringido; instante: -»; `PRIMERO EN TOCAR UN LIMITE:
ninguno`; `dias de trading: 13`), pero el bot deja de operar el 2026-01-20 y abril, julio y agosto
corren con todos los hechos del camino producidos (`todos los hechos del camino producidos`: 22 de
23 sesiones en abril, 23 de 25 en julio, 24 de 26 en agosto) y ninguna orden colocada. Es el camino
de la cuenta que la decisión 4 aparta de la clasificación: por eso los patrones se cuentan sobre la
corrida 2. Y el tramo no es continuo (enero, y de abril a agosto con huecos): la curva es indicativa,
como dijo R3.1.

**La cuenta de la corrida 1**: saldo final 90.741,16; equity final 90.741,16; 13 días de trading; 76
días en la curva (enero del 2 al 30 se mueve; del 2026-04-01 al 2026-08-31 la curva repite
90.741,16). Peor día: 2026-01-20 (de 92.415,29 a 90.741,16, −1,81 % del saldo de corte; el límite
diario de la firma es 5 %).

**Peticiones al servidor (informativo, como en R3.1):** corrida 1, 395 en total, máximo diario 66
(2026-01-19) frente a `firma_mensajes_dia_max` 2000; 63 de los 76 días con 0. Corrida 2, 2.454 en
total (enero 679, abril 630, julio 459, agosto 686), máximo diario 73 (2026-07-17); 3 días con 0. El
freno de ADR-0067 (umbrales `aviso 1000, corte 1500, bucle 5 iguales en 1 min`, PROVISIONALES bajo
A-54): «ningun aviso ni ninguna peticion negada» en las dos. Los cierres de mercado (ADR-0068):
«ninguna peticion negada ni ninguna pendiente cancelada» en las dos.

### 2.3 Lo que el arnés hace ahora y antes no (§0.i), medido en las dos salidas

| Qué | Corrida 1 (arrastrada) | Corrida 2 (diaria) |
|---|---|---|
| `TOPE DEL TRADER (RN-020, A-44)` | `tope del trader: dia, sobre saldo, en porcentaje; dia 4.5 sobre saldo_inicial_dia; reinicio en Europe/Prague; SUPUESTO: reinicio con el huso de corte del perfil (el trader no dijo otro)` | la misma línea |
| Sesiones que detiene RN-020 (`detenido_por_tope: N de 104`; `RN-020` en disparadas) | 0 de 104; RN-020 no aparece en «Reglas disparadas» | 0 de 104; ídem |
| Órdenes que retira ADR-0086 (canceladas con RN-020 en el motivo) | 0 | 0 |
| `detenido_por_tope_total` | 0 de 104 | 0 de 104 |
| RN-036 (racha): sesiones en que dispara / `detenido_por_racha` / `RACHA DE PERDIDAS` al final | 2 de 152 (1 de 104) / 1 de 104 / `5 seguidas; la ultima el 2026-01-20` | 0 de 152 / 0 de 104 / `2 seguidas; la ultima el 2026-08-31` (la cuenta diaria reinicia la racha cada día) |
| RN-037 (el último minuto antes de las 11 o las 3): sesiones en que dispara | 152 de 152 | 152 de 152 |
| Cancelaciones «en el ultimo tramo de la vela H4» (RN-035 y RN-037 en el motivo) | 0 | 4 (1 en enero, 3 en agosto); RN-035 dispara en 4 de 152 sesiones |
| `detenido_por_cartuchos` | 2 de 104 (RN-016 en 2 sesiones) | 4 de 104 (RN-016 en 4) |
| `liquidez_tomada` (la referencia de ACTIVAR-A35-A44.md §5.1: R3.1 dio 98 y 97 de 104) | 96 de 104 | 96 de 104 |
| `orden_dimensionada` / `operacion del bot` | 96 / 16 de 104 | 96 / 92 de 104 |
| Qué reinicia la cuenta diaria (`cableado.py:248-249`) | — | la cuenta, el seguidor del tope y la racha, cada día; la curva, el veredicto y `PRIMERO EN TOCAR` son solo del último día (`CUENTA: REINICIADA CADA DIA`) |

RN-020 no detuvo ninguna sesión: en la corrida 1 la cuenta nunca pierde el 4,5 % del saldo de
corte en un día (el peor día pierde 1,81 %), y en la corrida 2 cada día empieza en 100.000. Los 12
parámetros DEFAULT_AMBIGUOUS con los que corrió la corrida que cuenta son los de la tabla de §0.i
(el registro no cambió en la rama: `git diff main -- knowledge/` vacío).

### 2.4 La repetición de la corrida 1 fuera del repo (determinismo)

Después de la corrida 2, nunca a la vez: `uv run botsito motor arnes --simular --salida
<carpeta de trabajo de la sesión>/cuenta-arrastrada.txt` → `TIEMPO: 342.6 s; MEMORIA: pico del
proceso de 630.4 MiB`; `exit=0`. `diff docs/validation/anexos/RECORRIDA-CONSTRUCCION/cuenta-arrastrada.txt
<la copia>` → sin salida, `diff exit=0`: **idéntica byte a byte**. La copia se borró (`rm`; `ls`
de la carpeta ya no la lista) y no se commitea. Tres corridas: 336,5 + 299,0 + 342,6 s de arnés
(16,3 min) y de 629 a 638 MiB de pico, lo que §0.j esperaba.

### 2.5 El diff contra la línea base (`diff-linea-base.txt`)

`diff docs/validation/CABLEADO-SIMULADOR-LINEA-BASE.txt docs/validation/anexos/RECORRIDA-CONSTRUCCION/cuenta-arrastrada.txt > docs/validation/anexos/RECORRIDA-CONSTRUCCION/diff-linea-base.txt`
→ `exit=1` (hay diferencias; no es un fallo). 1.348 líneas: 129 de la línea base salen (`<`), 1.191
de la corrida 1 entran (`>`), en 14 bloques; de las 162 líneas de la línea base, 33 siguen iguales
(títulos de sección, `MOTOR`, `PERFIL`, `FASE`, las etiquetas fijas). Por sección:

| Bloque (líneas de la base → de la corrida 1) | Sección | Qué cambia | Comparable | Por qué cambia |
|---|---|---|---|---|
| 4 → 4 | CONJUNTO | `(2026-04, 2026-08); dias 42; sesiones 49` → `(2026-01, 2026-04, 2026-07, 2026-08); dias 76; sesiones 104` | no | construcción más amplia (ADR-0078, ADR-0079) |
| 7-8, 10-12 → 7-13 | Criterio de fidelidad | trader 77 → 198; bot 0 → 53; cobertura 0/77 → 7/198; precisión sin definir → 7/53; mismo minuto 0 → 5; **línea de veredicto nueva** (no existía: ADR-0070 es del 2026-10-07) | las 77 operaciones de abril y agosto siguen dentro de las 198 (35 + 42, §0.d) | construcción (el total) y motor (el bot opera) |
| 16-22 → 17-24 | Embudo de hechos | `sesgo 49 de 49` → `104 de 104`; `orden_dimensionada 0` → 96; `liquidez_tomada 0` → 96; `operacion del bot 0` → 16; `detenido_por_racha` nuevo | el sesgo se produce en todas las sesiones en las dos | construcción (104) y motor (A-35, A-44 y A-21 con valor; RN-036) |
| 25-29 → 27 | Paradas NO_IMPLEMENTADA | cinco paradas (`perdida_dia`, `perdida_semana`, `alcanza_nivel`, `cruza`, `toca_colocar_orden_limite`, 49 de 49 cada una) → `ninguna` | sí: era el hueco de A-44, A-35 y A-21 | motor |
| 32-35 → 30-50 | Reglas disparadas | 3 reglas (RN-001, RN-003, RN-033) → 20 | RN-003 sigue en todas; RN-001 42/84 → 78/152 | motor y construcción |
| 38-43 → 53-301 | Avisos de orden | 6 avisos (RN-001, RN-033, en 6 sesiones de abril y agosto) → 249 | los 6 de la base no se repiten tal cual: hoy los avisos son de RN-004/RN-006/RN-011/RN-012 | motor |
| 46-47 → 304-309 | RN-003 al abrir | `alcista 21; ambiguo 6; bajista 22` → `alcista 51; bajista 52; insuficiente 1` (y cuatro líneas nuevas de ADR-0060/0075/0080); por operación `a favor 58; ambiguo 7; en contra 12` → `154; 42; insuficiente 2` | **no por mes: es un agregado de todas las sesiones**; se compara por sesión abajo | construcción (104 sesiones) y motor (ADR-0069, 0075, 0080) |
| 50-98 → 312-683 | Por sesion | 49 líneas → 104, y el formato gana `detenido_por_racha`, `bloqueadas` | sí, sesión a sesión en abril y agosto (abajo) | motor y construcción |
| 103 → 688-691 | Simulación | `DIAS CORRIDOS 42` → 76; `TOPE DEL TRADER`, `RACHA DE PERDIDAS`, `PRIMERO EN TOCAR` nuevas | — | construcción y motor |
| 109-111 → 697-699 | Veredicto de la cuenta | saldo 100000 → 90741.16; días de trading 0 → 13 | — | motor (el bot opera) |
| 114-155 → 702-777 | Curva de equity | 42 días planos → 76 días, enero se mueve | los 42 días de abril y agosto siguen en la curva, planos en las dos (en la base por no operar; aquí por RN-032) | motor |
| 158 → 780-1220 | Eventos del broker | `ninguno` → 127 (todos de enero) | — | motor |
| 160-162 → 1222-1224 y lo que sigue | Totales, huecos y secciones nuevas | `eventos: 0` → 127; `rechazos 0` → 4; huecos `perdida_dia, perdida_semana` → `ninguno`; después, las secciones que la base no tiene (Diferencias por operacion, Ordenes, Rechazos, Peticiones, freno, cierres) | los huecos: sí (A-44 cerró el hueco de RN-020) | motor |

**El rn003 de las 49 sesiones de abril y agosto, sesión a sesión** (guion `comparar_rn003.py` de la
carpeta de trabajo, que lee las líneas «Por sesion» de las dos salidas): las 49 sesiones de la base
están en la corrida 1 (más las 55 de enero y julio); **8 cambian de sesgo**: `2026-04-03 11-15`
ambiguo → alcista, `2026-04-13 11-15` ambiguo → bajista, `2026-04-24 07-11` ambiguo → bajista,
`2026-08-04 11-15` alcista → bajista, `2026-08-07 11-15` bajista → alcista, `2026-08-11 07-11`
ambiguo → alcista, `2026-08-20 07-11` ambiguo → bajista, `2026-08-26 11-15` ambiguo → alcista. Las
seis «ambiguo» desaparecen (ADR-0075: la H4 neutra con doble ruptura no decide; ADR-0080: el sesgo
cambia por el color) y dos sesiones de agosto se dan la vuelta (ADR-0080: «las mismas ocho sesiones
cambian», SESGO-H4-COLOR.md, con la rejilla de ADR-0069). Por mes: abril `alcista 10, ambiguo 3,
bajista 10` → `alcista 11, bajista 12`; agosto `alcista 11, ambiguo 3, bajista 12` → `alcista 13,
bajista 13`. Ninguna de las 41 restantes cambia. Es lo que §0.g anunció: el sesgo de abril y agosto
cambió por el MOTOR, no por la construcción.

### 2.6 Los patrones T0 y P1 a P7 de las dos corridas, por mes

Con la copia de `patrones.py` (§1.2), `--filas` a `patrones-diaria.txt` y `patrones-arrastrada.txt`
(sus cabeceras, tal cual: `448 filas, 104 sesiones con rn003` y `244 filas, 104 sesiones con
rn003`). **La clasificación que cuenta es la de la corrida 2 (decisión 4)**; la corrida 1 va como
contexto del camino de la cuenta. «P? solo otro lado»: 0 filas en las dos.

| Corrida | Mes | P1 sesgo | P2 entrada | P3 otra zona | P4 sin orden | P5 de más | P6 trader no operó | P7 repetidas | T0 pareja |
|---|---|---|---|---|---|---|---|---|---|
| 2 diaria | 2026-01 | 7 | 16 | 20 | 3 | 60 | 14 | 1 | 7 |
| 2 diaria | 2026-04 | 9 | 5 | 13 | 1 | 31 | 34 | 0 | 7 |
| 2 diaria | 2026-07 | 20 | 12 | 15 | 1 | 39 | 2 | 4 | 15 |
| 2 diaria | 2026-08 | 8 | 7 | 12 | 3 | 43 | 27 | 0 | 12 |
| 2 diaria | **total** | **44** | **40** | **60** | **8** | **173** | **77** | **5** | **41** |
| 1 arrastrada | 2026-01 | 7 | 11 | 11 | 17 | 37 | 9 | 1 | 7 |
| 1 arrastrada | 2026-04 | 9 | 0 | 0 | 26 | 0 | 0 | 0 | 0 |
| 1 arrastrada | 2026-07 | 20 | 0 | 0 | 47 | 0 | 0 | 0 | 0 |
| 1 arrastrada | 2026-08 | 8 | 0 | 0 | 34 | 0 | 0 | 0 | 0 |
| 1 arrastrada | **total** | **44** | **11** | **11** | **124** | **37** | **9** | **1** | **7** |

Detalles de la corrida 2 (de la cabecera de `patrones-diaria.txt`): P1 por sesgo del bot: alcista
14, bajista 28, insuficiente 2 (44 filas en 21 sesiones: las mismas 44 y 21 que la corrida 1 y que
PUNTO-USADO, porque el sesgo no cambió desde ADR-0080); P3: misma entrada otra hora 3, otra entrada
57; P5: mismo lado 137, otro lado 36; P6: en día 28, en sesión 49; P7: Δentrada 0 puntos 1, 1 punto
2, 3 puntos 2. **Filas que tocan una hora perdida, marcadas «posible M» sin cambiar de patrón: 25
en la corrida 2 y 12 en la corrida 1** (las filas, con su marca, en los dos ficheros `--filas`).

**Como contexto, nunca como referencia, PUNTO-USADO** (`anexos/PUNTO-USADO/patrones.txt`, la
diaria de entonces, 364 filas; `patrones-arrastrada.txt`, 240 filas):

| Corrida de PUNTO-USADO | Mes | P1 | P2 | P3 | P4 | P5 | P6 | P7 | T0 |
|---|---|---|---|---|---|---|---|---|---|
| diaria | 2026-01 | 7 | 13 | 26 | 6 | 43 | 8 | 0 | 2 |
| diaria | 2026-04 | 9 | 4 | 11 | 6 | 22 | 21 | 0 | 5 |
| diaria | 2026-07 | 20 | 9 | 14 | 14 | 25 | 2 | 3 | 7 |
| diaria | 2026-08 | 8 | 7 | 9 | 14 | 25 | 20 | 0 | 4 |
| diaria | total | 44 | 33 | 60 | 40 | 115 | 51 | 3 | 18 |
| arrastrada | total | 44 | 12 | 22 | 118 | 37 | 5 | — | 2 |

Lo que separa estas corridas de aquellas, sin ajustar nada para acercarlas: ADR-0084 (la mecha que
pasa el nivel de M15 y vuelve lo mueve, `cualquier_mecha`), ADR-0085 (la vela sin cuerpo en M1 no
corta la racha ni cuenta como alternancia; RN-007 con umbral cero), ADR-0086 (RN-020 retira la
pendiente al tope), RN-037 (ningún orden en el último minuto de la H4) y la retirada de RN-035 un
minuto antes del fin de la H4, A-35 y A-44 con valor (el motor corre sin diagnóstico; RN-020 evaluado
con el tope del trader en vez de `sin_tope`), la racha de RN-036 a cero tras la detención
(`tras_la_detencion`: en PUNTO-USADO la racha de enero -`12 seguidas`- seguía viva y bloqueaba; aquí
la arrastrada la deja en 5 y lo que bloquea de febrero en adelante es RN-032) y la caja entera frente
al nivel tomado (RN-005, `caja_lado_de_ruido = caja_entera`). En la diaria, las parejas pasan de 18
a 41, P4 (el trader opera a favor y el bot no tiene ninguna orden en la sesión) de 40 a 8, P5 de 115
a 173 y P6 de 51 a 77: el bot coloca en más sesiones. En la arrastrada, el bot de PUNTO-USADO dejó
de operar por la racha; el de hoy, por RN-032 desde el 2026-01-20: los dos acaban con ≈90.7 k
(90.711,97 entonces, 90.741,16 ahora) y P4 en abril, julio y agosto es toda la columna.

### 2.7 El embudo por mes y los rechazos por motivo de las dos corridas

«### Embudo por mes: primer hecho del camino que falta en las sesiones con operaciones del trader
y sin operación del bot»:

| Corrida | Mes | sesiones con trader | sin operación del bot | de ellas: todos los hechos producidos | `orden_dimensionada[productoras sin cumplirse]` |
|---|---|---|---|---|---|
| 1 arrastrada | 2026-04 | 23 | 23 | 22 | 1 |
| 1 arrastrada | 2026-07 | 25 | 25 | 23 | 2 |
| 1 arrastrada | 2026-08 | 26 | 26 | 24 | 2 |
| 1 arrastrada | 2026-01 | 30 | 14 | 11 | 3 |
| 2 diaria | 2026-04 | 23 | 2 | 1 | 1 |
| 2 diaria | 2026-07 | 25 | 3 | 1 | 2 |
| 2 diaria | 2026-08 | 26 | 3 | 1 | 2 |
| 2 diaria | 2026-01 | 30 | 4 | 1 | 3 |

En la corrida 2 quedan 12 sesiones con operaciones del trader y sin operación del bot: 8 en las que
`orden_dimensionada` no se produjo (RN-011 no dimensionó: sin punto con caja, o la zona del lado de
ruido), y 4 con todos los hechos producidos (el bot colocó y la orden no se llenó, se canceló o se
rechazó). Ningún freno `detenido_por_*` aparece en el embudo por mes de ninguna de las dos.

«### Rechazos por motivo (mes | motivo | peticion | rechazos)»: corrida 1, `2026-01 |
precio_invalido | colocar | 4`; corrida 2, `precio_invalido | colocar` 8 (enero), 10 (abril), 8
(julio), 10 (agosto) = 36. Ningún otro motivo, ningún rechazo al modificar ni al llenar. «Ordenes no
enviadas por el bot»: `ninguna` en las dos. Órdenes: corrida 1 `cancelada 158, llenada 53, rechazada
4`; corrida 2 `cancelada 1002, llenada 291, rechazada 36`. Casi todas las cancelaciones llevan RN-006
en el motivo (la reubicación cancela y recoloca: 158 de 158 en la 1; 998 de 1.002 en la 2, y las 4
restantes «en el ultimo tramo de la vela H4» con RN-035 y RN-037). El límite que mordió el lote al
colocar (`limite`): corrida 2, `margen` 445, `volumen+margen` 144, `ninguno` 740.

### 2.8 Las diferencias más grandes de la corrida 2: costes, sesiones cargadas y el respaldo M1 (respuesta a la PARADA 2, punto 1)

Medido con `anexos/RECORRIDA-CONSTRUCCION/costes_y_sesiones.py`, que solo LEE las salidas
commiteadas de la carpeta (`diaria…txt`, `cuenta-arrastrada.txt`, `entradas-antes-alternancia.txt`)
y los TICKS de los días dev de construcción en ventanas de un minuto alrededor de cada evento, por
`data.ticks.cargar_ticks`; no corre el motor, no lee el calentamiento ni ninguna vela, y no imprime
nada anterior a las 00:00Z de su día (todos los instantes son de 05:00Z en adelante):
`uv run python docs/validation/anexos/RECORRIDA-CONSTRUCCION/costes_y_sesiones.py > docs/validation/anexos/RECORRIDA-CONSTRUCCION/costes-y-sesiones.txt`
→ `exit=0`. El R de las salidas es **por precio**, desde el llenado y sobre el riesgo con el que
nació la posición (su stop original): no lleva la comisión, que va en su propia columna, en R (10 USD
por lote ida y vuelta, `firma_comision_usd_por_lote` 5 por lado, sobre la distancia del stop: 1 USD
por punto y lote). **Comprobación**: en los 25 casos de a) el R recalculado desde el precio de salida
(el tick que la dispara, o el objetivo, que se llena a su precio) es el de la salida («cuadra» 25 de
25).

**a) Llenadas de la corrida 2 con |R − R esperado| > 0,25** (esperado sin costes, el del consultor:
stop −1; stop tras moverlo a break even 0; objetivo +3,75). **25 de las 286 con R esperado** (las 5
cerradas a mercado al fin de la ventana no tienen R esperado: 2026-01-02 11-15 o9 +0,57;
2026-01-21 11-15 o26 −0,09; 2026-04-02 11-15 o9 +1,43; 2026-04-06 07-11 o6 −0,28; 2026-08-13 07-11
o9 +1,86). «R teórico» = el R con el llenado exactamente en el 0 y la salida en su nivel; para el
objetivo, `floor(3·caja) / ceil(0,8·caja)` (el stop se redondea alejándose, `stop_fraccion_redondeo`,
y el objetivo hacia abajo, `fijar_objetivo`): con cajas pequeñas ya no es 3,75. El deslizamiento es
cuántos puntos pasado el 0 llegó el tick que llenó la orden stop; el salto, cuántos puntos pasado su
nivel llegó el tick que saltó el stop.

| día | sesión | orden | lado | motivo | R | esperado | caja / stop (pt) | R teórico | llenado: fuente, desliz. (pt), spread | salida: fuente, salto (pt) | límite del lote | comisión en R | causa | regla como está escrita |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-01-05 | 07-11 | o3 | venta | objetivo | +2.86 | +3.75 | 7 / 6 | +3.50 | ticks 06:04:22, +1, 3 | ticks, +0 | volumen+margen (riesgo 0.146%) | 1.67 | redondeo de una caja de 7 pt; el tick que llena la orden stop llega 1 pt pasado el 0 | sí |
| 2026-01-12 | 11-15 | o5 | compra | objetivo | +3.38 | +3.75 | 15 / 12 | +3.75 | ticks 10:27:27, +1, 5 | ticks, +0 | margen (riesgo 0.293%) | 0.83 | el tick que llena la orden stop llega 1 pt pasado el 0 | sí |
| 2026-01-13 | 07-11 | o15 | venta | stop | -1.40 | -1.00 | 6 / 5 | -1.00 | ticks 09:35:09, +0, 6 | ticks, +2 | volumen+margen (riesgo 0.122%) | 2.00 | el tick que salta el stop llega 2 pt pasado su nivel | sí |
| 2026-01-15 | 07-11 | o2 | venta | objetivo | +3.38 | +3.75 | 15 / 12 | +3.75 | ticks 06:12:00, +1, 3 | ticks, +0 | margen (riesgo 0.294%) | 0.83 | el tick que llena la orden stop llega 1 pt pasado el 0 | sí |
| **2026-01-16** | **11-15** | **o16** | compra | objetivo | **+2.18** | +3.75 | 9 / 8 | +3.38 | ticks 12:35:15, +3, 4 | ticks, +0 | volumen+margen (riesgo 0.196%) | 1.25 | redondeo de una caja de 9 pt; el tick que llena la orden stop llega 3 pt pasado el 0 | sí |
| 2026-01-19 | 07-11 | o3 | compra | objetivo | +3.43 | +3.75 | 8 / 7 | +3.43 | ticks 06:48:30, +0, 3 | ticks, +0 | volumen+margen (riesgo 0.172%) | 1.43 | redondeo de una caja de 8 pt | sí |
| 2026-01-27 | 07-11 | o9 | venta | objetivo | +3.48 | +3.75 | 34 / 28 | +3.64 | ticks 06:48:52, +1, 1 | ticks, +0 | ninguno (riesgo 0.500%) | 0.36 | redondeo de una caja de 34 pt; desliz. 1 pt | sí |
| 2026-01-29 | 11-15 | o28 | venta | stop | -1.86 | -1.00 | 17 / 14 | -1.00 | ticks 12:54:12, +0, 2 | ticks, +12 | margen (riesgo 0.334%) | 0.71 | el tick que salta el stop llega 12 pt pasado su nivel | sí |
| 2026-04-01 | 11-15 | o7 | compra | objetivo | +2.10 | +3.75 | 17 / 14 | +3.64 | ticks 12:30:23, +7, 4 | ticks, +0 | margen (riesgo 0.344%) | 0.71 | redondeo de una caja de 17 pt; el tick que llena la orden stop llega 7 pt pasado el 0 | sí |
| **2026-04-07** | **07-11** | **o1** | venta | stop | **-2.00** | -1.00 | 5 / 4 | -1.00 | **respaldo_m1 05:00:00**, +0, - | ticks, +4 | volumen+margen (riesgo 0.099%) | 2.50 | llenado con el respaldo M1 fuera de la cobertura de ticks (el minuto antes de la ventana) y **con la M1 cuyo cierre colocó la orden**; el tick que salta el stop llega 4 pt pasado su nivel | **NO** |
| 2026-04-07 | 07-11 | o4 | venta | stop tras break even | -0.33 | +0.00 | 15 / 12 | +0.00 | ticks 05:09:27, +0, 4 | ticks, +4 | margen (riesgo 0.296%) | 0.83 | salto del stop 4 pt | sí |
| 2026-04-08 | 07-11 | o4 | compra | objetivo | +3.48 | +3.75 | 34 / 28 | +3.64 | ticks 07:15:28, +1, 2 | ticks, +0 | ninguno (riesgo 0.500%) | 0.36 | redondeo de una caja de 34 pt; desliz. 1 pt | sí |
| 2026-04-16 | 07-11 | o9 | compra | stop | -1.33 | -1.00 | 14 / 12 | -1.00 | ticks 07:56:02, +0, 2 | ticks, +4 | margen (riesgo 0.290%) | 0.83 | salto del stop 4 pt | sí |
| 2026-04-22 | 07-11 | o3 | venta | stop | -1.29 | -1.00 | 15 / 12 | -1.00 | ticks 05:15:02, +2, 5 | ticks, +4 | margen (riesgo 0.291%) | 0.83 | desliz. 2 pt; salto del stop 4 pt | sí |
| **2026-04-23** | **07-11** | **o3** | venta | stop | **-2.00** | -1.00 | 5 / 4 | -1.00 | **respaldo_m1 05:05:00**, +0, - | respaldo_m1, +4 | volumen+margen (riesgo 0.097%) | 2.50 | llenado con el respaldo M1 en una hora perdida y **con la M1 cuyo cierre colocó la orden**; la salida, también con el respaldo (la M1 abre 4 pt pasado el stop: hueco de ADR-0051 §4) | **NO** |
| 2026-04-24 | 07-11 | o6 | venta | stop | -1.50 | -1.00 | 5 / 4 | -1.00 | ticks 05:43:18, +0, 5 | ticks, +2 | volumen+margen (riesgo 0.098%) | 2.50 | salto del stop 2 pt sobre un stop de 4 | sí |
| 2026-04-24 | 07-11 | o23 | venta | objetivo | +3.29 | +3.75 | 19 / 16 | +3.56 | ticks 08:22:57, +1, 4 | ticks, +0 | margen (riesgo 0.390%) | 0.62 | redondeo de una caja de 19 pt; desliz. 1 pt | sí |
| 2026-07-02 | 11-15 | o9 | compra | stop | -1.29 | -1.00 | 8 / 7 | -1.00 | ticks 10:18:40, +0, 5 | ticks, +2 | volumen+margen (riesgo 0.175%) | 1.43 | salto del stop 2 pt | sí |
| 2026-07-03 | 07-11 | o5 | compra | objetivo | +2.57 | +3.75 | 13 / 11 | +3.55 | ticks 06:03:31, +3, 4 | ticks, +0 | margen (riesgo 0.274%) | 0.91 | redondeo de una caja de 13 pt; desliz. 3 pt | sí |
| 2026-07-07 | 11-15 | o22 | venta | objetivo | +3.20 | +3.75 | 11 / 9 | +3.67 | ticks 12:35:03, +1, 2 | ticks, +0 | volumen+margen (riesgo 0.224%) | 1.11 | redondeo de una caja de 11 pt; desliz. 1 pt | sí |
| 2026-07-08 | 07-11 | o6 | compra | stop tras break even | -0.41 | +0.00 | 67 / 54 | +0.00 | ticks 08:25:52, +0, 4 | ticks, +22 | ninguno (riesgo 0.500%) | 0.19 | salto del stop 22 pt | sí |
| 2026-08-18 | 11-15 | o15 | venta | stop tras break even | -0.33 | +0.00 | 25 / 20 | +0.00 | ticks 09:40:20, +1, 3 | ticks, +7 | margen (riesgo 0.492%) | 0.50 | desliz. 1 pt; salto del stop 7 pt | sí |
| 2026-08-25 | 07-11 | o10 | venta | objetivo | +3.20 | +3.75 | 11 / 9 | +3.67 | ticks 07:23:47, +1, 5 | ticks, +0 | volumen+margen (riesgo 0.220%) | 1.11 | redondeo de una caja de 11 pt; desliz. 1 pt | sí |
| 2026-08-28 | 11-15 | o17 | venta | stop tras break even | -0.46 | +0.00 | 14 / 12 | +0.00 | ticks 10:46:30, +1, 2 | ticks, +6 | margen (riesgo 0.294%) | 0.83 | desliz. 1 pt; salto del stop 6 pt | sí |
| 2026-08-31 | 11-15 | o14 | compra | stop tras break even | -0.33 | +0.00 | 32 / 26 | +0.00 | ticks 12:41:16, +1, 4 | ticks, +9 | ninguno (riesgo 0.500%) | 0.38 | desliz. 1 pt; salto del stop 9 pt | sí |

Por tipo de causa (un caso puede tener varias): deslizamiento de la entrada 15, salto del stop 13,
redondeo de una caja pequeña 10, respaldo M1 con la vela que decidió la orden 2, respaldo M1 en la
salida 1. Ninguno lo causa el lote limitado: el límite (volumen o margen) baja el lote y con él el
dinero, no el R por precio; sí lo deja en la columna de riesgo (del 0,097 % al 0,5 % del saldo). La
**comisión**, que el R de la salida no lleva, pesa 10 USD por lote sobre la distancia del stop:
**2,50 R en los stops de 4 puntos** y 2,00 en el de 5, más que el R de su propio stop. *Declarado
tras el revisor (a5):* el guion escribe a mano la fracción del stop (0,8), el múltiplo del objetivo
(3), la comisión (5 por lado) y el valor del punto (1 USD por lote), con los valores del registro y
del perfil de esta rama (`parametros.yaml`, `ftmo-2step-swing-100k.yaml`), solo para explicar el
redondeo y la comisión; no decide nada, pero si el registro cambia, sus columnas «R teórico» y
«comisión en R» dejan de valer.

Los dos casos que nombra el consultor:
- **2026-04-07 07-11 o1, −2,00 R, llenada a las 05:00:00.** Venta stop en 1.15378, colocada en el
  primer cierre de la ventana (04:59:59.999Z), caja de 5 puntos y stop de 4 (lote limitado por volumen
  y margen, riesgo 0,099 %). El minuto 04:59 no tiene ticks (el manifiesto de abril baja las horas
  05-13 UTC), así que el bróker la evalúa con el **respaldo M1 sobre la M1 de 04:59, la misma cuyo
  cierre colocó la orden** (`llenado.primer_llenado_stop` toma toda vela cuyo fin, 05:00:00.000, es
  posterior al instante de colocar, 04:59:59.999; con ticks, en cambio, salta todo tick anterior o
  igual a ese instante). Se llena a su nivel con el sello del cierre, 05:00:00.000, y el primer tick de
  la ventana (05:00:00.061) trae el ASK en 1.15386, 4 puntos pasado el stop (1.15382): −8 puntos sobre
  un riesgo de 4.
- **2026-01-16 11-15 o16, +2,18 R por objetivo.** Compra stop en 1.16161 con una caja de 9 puntos:
  stop a 8 (7,2 redondeado alejándose) y objetivo a 27 (1.16188), así que con el llenado en el 0 ya
  da 27/8 = 3,38, no 3,75. El tick que la llena (12:35:15.720, ticks, spread 4) trae el ASK 3 puntos
  pasado el 0 (1.16164): el riesgo pasa a 11 y el recorrido al objetivo a 24, 24/11 = 2,18. Antes
  había movido el stop a break even (12:38:15.595) y el objetivo se alcanzó a las 12:46:39.863.

**b) Sesiones de la corrida 2 con más de 4 llenadas: 9** (de la salida de §2.8, parte b):

| sesión | llenadas | escenarios con llenadas (n: llenadas) | puntos distintos | cartuchos gastados antes de cada llenada, por escenario | racha máxima del día (tope 9) | resultado del día en % del saldo (tope 4,5 de pérdida) | «Por sesion» de la salida |
|---|---|---|---|---|---|---|---|
| 2026-01-13 07-11 | 7 | 4 (n1: 3, n2: 1, n3: 1, n4: 2) | 5 | n1: 0, 1, 2; n2: 0; n3: 0; n4: 0, 1 | 6 | −4,01 | RN-016 disparada |
| 2026-01-14 07-11 | 5 | 2 (3, 2) | 3 | n1: 0, 1, 2; n2: 0, 1 | 4 | −0,92 | RN-016, RN-034 |
| 2026-04-15 11-15 | 5 | 3 (1, 3, 1) | 4 | n2: 0, 1, 2 | 2 | −1,78 | no hay (P6) |
| 2026-04-24 07-11 | 5 | 4 (1, 1, 2, 1) | 5 | todos 0 | 2 | −0,87 | RN-034 |
| 2026-07-02 11-15 | 6 | 3 (1, 2, 3) | 4 | n3: 0, 1, 2 | 6 | −3,63 | RN-016 disparada |
| 2026-07-03 07-11 | 5 | 3 (2, 2, 1) | 4 | n1: 0, 1; n2: 0, 1 | 2 | −0,05 | RN-034 |
| 2026-07-07 11-15 | 5 | 3 (2, 2, 1) | 5 | n1: 0, 1; n2: 0, 1 | 4 | −2,13 | RN-034 |
| 2026-07-10 07-11 | 5 | 3 (2, 2, 1) | 5 | n1: 0, 1; n2: 0, 1 | 6 | −3,37 | — |
| **2026-08-24 07-11** | **8** | **5 (2, 2, 1, 1, 2)** | **8** | n1: 0, 1; n2: 0, 1; n3: 0; n4: 0; n5: 0, 1 | **7** | **−4,15** | no hay (P6) |

Ninguna llenada ocurrió con tres cartuchos ya gastados en su escenario (cartuchos_max 3): RN-016 se
aplica como está escrita, y cada escenario nuevo vuelve a tener sus tres intentos porque lo abre una
toma de otra liquidez de M15 (`cartuchos_reinicio = siguiente_liquidez_m15`, `intentos_tras_toma_nueva
= vuelven_a_cartuchos_max`). **2026-08-24 07-11**: 8 llenadas en 5 escenarios y 8 puntos distintos,
ninguno con más de dos llenadas; la racha del día llega a 7 (las dos llenadas a break even no la
cortan; tope 9) y el resultado del día, a −4,15 % del saldo (R por el riesgo de cada orden, menos la
comisión; tope de RN-020 4,5): ni RN-036 ni RN-020 podían detener, según las cifras de la salida. Lo
mismo en las otras ocho. **Las nueve: «regla aplicada como está escrita»** (RN-016, RN-036 y RN-020).
**Lo que la salida no da**: de qué toma sale cada escenario. Ninguna salida commiteada imprime el
instante ni el nivel de las tomas (la memoria del productor no se escribe), y sacarlo exige correr el
motor o leer el calentamiento, que este punto excluye: va a «Lo que no pude medir».

**c) El respaldo M1, en las dos corridas** (parte c de la salida): la causa de los dos «NO» no es de
esos dos casos. El bróker evalúa una orden contra **la M1 cuyo cierre la colocó** siempre que el
minuto de esa M1 no tiene ticks: en el borde de la ventana (el minuto antes de la primera hora con
ticks) y en las horas perdidas. Recuento por corrida:

| Corrida | eventos del respaldo | llenadas con la M1 que colocó la orden: en el borde de la ventana | ídem, en una hora perdida | otras llenadas del respaldo (hora perdida) | stops y stops movidos del respaldo |
|---|---|---|---|---|---|
| 1 (la que cuenta) | 8 | 1 (2026-01-06 07-11 o1) | 1 (2026-01-05 11-15 o20) | 2 | 4 |
| 2 (diaria) | 34 | 2 (2026-01-06 07-11 o1; 2026-04-07 07-11 o1) | 8 | 6 | 18 |

Las 10 de la corrida 2: 2026-01-05 o20 (P5), 2026-01-06 o1 (P5, +3,64), 2026-04-06 o11 y o12 (P6),
2026-04-07 o1 y o28 (P6), 2026-04-23 o3 (P5), 2026-07-10 o3 (P5) y **o4 (T0, una de las 41 parejas)**,
2026-08-20 o14 (P5). **En la corrida 1 ninguna de las dos es una de las 7 parejas** (las 7 son de
2026-01-02, 07, 09, 12, 13, 14 y 19): sin ellas la precisión sería 7/51 (13,7 %) y el veredicto
seguiría siendo «no»; lo que no se puede medir sin correr es si el camino de la cuenta (RN-032 desde el
2026-01-20) cambiaría.

**c) Regla aplicada como está escrita**: «sí» en 23 de los 25 casos de a) y en las 9 sesiones de b).
**«NO» en dos casos de a)** (2026-04-07 07-11 o1 y 2026-04-23 07-11 o3), con esta evidencia: la orden
se evalúa contra precios **anteriores a su colocación** (la M1 cuyo cierre la colocó), y ADR-0051 §2
dice que una orden «no se evalúa contra ese mismo tick: contra el siguiente (sin mirar al futuro: el
motor decide con lo que ya cerró)», y el módulo `engine/llenado.py:10-12` lo dice de los ticks («Un
evento nunca se evalua contra el tick en el que se decidio: solo contra los posteriores»; el
respaldo, `:13-15`, no lo dice: *corregido tras el revisor, a3*); el respaldo de §5 no lo excluye
por escrito, y en 2026-04-07 además no
es una hora perdida sino el borde de la cobertura de ticks, y §8 deja el respaldo «solo para depurar»
y para las horas perdidas. **Por el punto 1 c) de la respuesta: PARADA 3 antes del revisor** (abajo).

## 3. La lista «Entradas antes de la alternancia» (decisión 5; respuesta a la PARADA, puntos 0, 1 y 2)

Comando autorizado, una sola vez y después de las tres corridas, nunca a la vez que nada:
`uv run python docs/validation/anexos/RECORRIDA-CONSTRUCCION/entradas_antes_alternancia.py --diaria "docs/validation/anexos/RECORRIDA-CONSTRUCCION/diaria.DIAGNOSTICO.cuenta=diaria.txt" --salida docs/validation/anexos/RECORRIDA-CONSTRUCCION/entradas-antes-alternancia.txt`
→ `OK: … entradas-antes-alternancia.txt (291 llenadas, 259 en la lista)`; `exit=0`. La cabecera
del fichero: `ORDENES llenadas frente a «### Ordenes» de la corrida 2: iguales (291)`: las 291
órdenes llenadas que reproduce el guion (cuenta reiniciada cada día) coinciden línea a línea con las
291 filas `llenada` de «### Ordenes» de `diaria.DIAGNOSTICO.cuenta=diaria.txt` (si no, habría
salido con 3). Ninguna fila lleva «(antes del dia)» (`grep -c`: 0): ningún instante ni punto es
anterior a las 00:00Z de su día dev. Las columnas, en el orden de la respuesta a la PARADA: zonas al
llenar y al colocar (punto 1), dónde (referencia / primer punto tras la toma / posterior) y
reubicaciones (punto 0), escenario (la marca de H6: 12 llenadas cuya zona es de un escenario
anterior al vigente al llenar, con «vig. n X»), R sobre el riesgo con el que nació la posición, y
pareja (T0, por la medida del criterio) o patrón (P5, P6, de `patrones.py` sobre la corrida 2). **Sin
conclusiones: es para el dibujo 3 de S-15, y RN-009 no cambia.**

### 3.1 El resumen (del fichero, «## Resumen»)

- Llenadas: 291; **en la lista (zonas al llenar < 2): 259**; fuera (2 o más zonas): 32.
- Por mes: enero 77, abril 61, julio 48, agosto 73 (de 81, 72, 56 y 82 llenadas).
- Por zonas al llenar: **0 zonas 149; 1 zona 110**.
- Por dónde estaba la orden: **primer punto tras la toma 161; referencia 43; posterior 55**. Cruce
  con las zonas: 0 zonas → primer punto 106, referencia 43; 1 zona → primer punto 55, posterior 55
  (ninguna «referencia» con 1 zona, ninguna «posterior» con 0, como es de esperar: un punto
  posterior ya deja una zona detrás).
- Por reubicaciones (órdenes anteriores del mismo escenario canceladas por RN-006): 0 → 46; 1 → 55;
  2 → 47; 3 → 44; 4 → 25; 5 → 20; 6 → 4; 7 → 5; 8 → 3; 9 → 5; 10 → 2; 11 → 3. **213 de las 259
  llenadas venían de al menos una reubicación** (S-10: primer punto, reubicada, 0 zonas: aquí son
  las 106 − las de reubicaciones 0 de ese grupo); 46 se llenaron en la primera orden del escenario.
- Por pareja o patrón: **P5 (de más, en sesión con trader) 160; P6 (el trader no operó) 65; T0 pareja
  34** (de las 41 parejas de la corrida 2, 7 se llenaron con 2 o más zonas). Cruce: 0 zonas → P5 88,
  P6 41, T0 20; 1 zona → P5 72, P6 24, T0 14. Dónde × patrón: primer punto → P5 99, P6 41, T0 21;
  referencia → P5 22, P6 13, T0 8; posterior → P5 39, P6 11, T0 5.
- Resultado en R (sobre el riesgo inicial; la salida de `motivo_cierre`): **positivos 36, negativos
  176, cero 47** (stops a break even); por motivo: stop 222, objetivo 34, manual 3 (cierre forzoso
  al fin de la ventana). Con 0 zonas: objetivo 22, stop 124, manual 3; con 1 zona: objetivo 12, stop 98.
- Las 32 que quedan fuera (2 o más zonas al llenar), en «## Todas las llenadas» del fichero.
- **Marca E (respuesta a la PARADA 3, punto 1 a): 10 de las 259 filas** llevan «E: llenada con la
  vela que la colocó (ADR-0051 §2)»: el bróker las llenó con el respaldo M1 en la vela cuyo cierre
  colocó la orden (§2.8 c). Las 10 llenadas así de la corrida 2 están todas en esta lista (ninguna
  tiene 2 o más zonas). Es un error nuestro, no una regla del trader: no se eligen para la sesión 6.
  La marca va en la tabla de §3.2; `entradas-antes-alternancia.txt` no la lleva, porque solo lo
  regenera el guion de f), que corre el motor y estaba autorizado una sola vez.

### 3.2 La lista, por día y sesión (las 259; el fichero trae además entrada, punto, sesgo y camino)

Hora = el llenado, UTC; «al colocar» = zonas en el cierre que colocó la orden; reubic. =
reubicaciones; escenario = el de la zona («vig.» = el vigente al llenar, si es otro).

| día | sesión | orden | lado | llenada (UTC) | zonas al llenar | al colocar | dónde | reubic. | escenario | R | pareja o patrón |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-01-02 | 11-15 | o7 | venta | 12:12:26 | 0 | 0 | primer punto tras la toma | 6 | n 1 | -1.00 (stop) | P5 |
| 2026-01-02 | 11-15 | o9 | venta | 13:28:06 | 0 | 0 | referencia | 0 | n 2 | +0.57 (manual) | T0 |
| 2026-01-05 | 07-11 | o3 | venta | 06:04:22 | 1 | 1 | posterior | 2 | n 1 | +2.86 (objetivo) | P5 |
| 2026-01-05 | 07-11 | o16 | venta | 08:33:08 | 0 | 0 | primer punto tras la toma | 4 | n 3 | +3.60 (objetivo) | P5 |
| 2026-01-05 | 07-11 | o18 | venta | 09:28:17 | 0 | 0 | primer punto tras la toma | 0 | n 4 | +3.75 (objetivo) | P5 |
| 2026-01-05 | 11-15 | o19 | venta | 10:22:00 | 0 | 0 | referencia | 0 | n 1 | -1.00 (stop) | P5 |
| 2026-01-05 | 11-15 | o20 | venta | 10:24:00 | 1 | 1 | primer punto tras la toma | 0 | n 1 | +0.00 (stop) | P5 · **E: llenada con la vela que la colocó (ADR-0051 §2)** |
| 2026-01-05 | 11-15 | o21 | venta | 10:56:00 | 0 | 0 | referencia | 0 | n 2 | -1.00 (stop) | P5 |
| 2026-01-06 | 07-11 | o1 | compra | 06:00:00 | 0 | 0 | referencia | 0 | n 1 | +3.64 (objetivo) | P5 · **E: llenada con la vela que la colocó (ADR-0051 §2)** |
| 2026-01-06 | 07-11 | o9 | compra | 08:02:05 | 1 | 1 | posterior | 5 | n 3 | +3.65 (objetivo) | P5 |
| 2026-01-06 | 11-15 | o20 | venta | 13:43:00 | 0 | 0 | primer punto tras la toma | 3 | n 1 | -1.12 (stop) | P6 |
| 2026-01-06 | 11-15 | o21 | venta | 13:44:30 | 0 | 0 | primer punto tras la toma | 3 | n 1 | +3.50 (objetivo) | P6 |
| 2026-01-07 | 07-11 | o2 | venta | 06:34:16 | 0 | 0 | referencia | 1 | n 1 | -1.00 (stop) | T0 |
| 2026-01-07 | 07-11 | o4 | venta | 06:39:03 | 1 | 1 | primer punto tras la toma | 2 | n 1 | -1.00 (stop) | P5 |
| 2026-01-07 | 07-11 | o9 | venta | 06:55:07 | 0 | 0 | primer punto tras la toma | 2 | n 2 | -1.00 (stop) | P5 |
| 2026-01-07 | 07-11 | o10 | venta | 06:57:57 | 1 | 1 | primer punto tras la toma | 2 | n 2 | +0.00 (stop) | P5 |
| 2026-01-07 | 11-15 | o11 | venta | 10:03:27 | 0 | 0 | referencia | 0 | n 1 | -1.00 (stop) | P6 |
| 2026-01-07 | 11-15 | o18 | venta | 13:00:00 | 0 | 0 | primer punto tras la toma | 0 | n 2 | -1.00 (stop) | P6 |
| 2026-01-08 | 07-11 | o2 | compra | 06:30:49 | 0 | 0 | referencia | 1 | n 1 | +0.00 (stop) | P5 |
| 2026-01-08 | 07-11 | o8 | compra | 08:08:57 | 1 | 1 | posterior | 4 | n 2 | -1.11 (stop) | P5 |
| 2026-01-09 | 07-11 | o3 | venta | 08:04:03 | 0 | 0 | primer punto tras la toma | 2 | n 1 | +0.00 (stop) | P5 |
| 2026-01-09 | 11-15 | o13 | venta | 13:38:25 | 1 | 1 | posterior | 2 | n 2 | -1.00 (stop) | P6 |
| 2026-01-12 | 11-15 | o5 | compra | 10:27:27 | 0 | 0 | primer punto tras la toma | 4 | n 1 | +3.38 (objetivo) | P5 |
| 2026-01-12 | 11-15 | o8 | compra | 13:03:46 | 1 | 0 | primer punto tras la toma | 2 | n 2 | +3.69 (objetivo) | T0 |
| 2026-01-13 | 07-11 | o3 | venta | 07:35:42 | 0 | 0 | primer punto tras la toma | 2 | n 1 | -1.00 (stop) | P5 |
| 2026-01-13 | 07-11 | o4 | venta | 07:36:00 | 1 | 1 | primer punto tras la toma | 2 | n 1 | -1.20 (stop) | P5 |
| 2026-01-13 | 07-11 | o7 | venta | 08:02:25 | 0 | 0 | primer punto tras la toma | 1 | n 2 | -1.00 (stop) | P5 |
| 2026-01-13 | 07-11 | o12 | venta | 09:06:56 | 1 | 1 | posterior | 1 | n 3 | +0.00 (stop) | P5 |
| 2026-01-13 | 07-11 | o15 | venta | 09:35:09 | 0 | 0 | primer punto tras la toma | 2 | n 4 | -1.40 (stop) | P5 |
| 2026-01-13 | 07-11 | o17 | venta | 09:37:02 | 1 | 1 | primer punto tras la toma | 3 | n 4 | -0.14 (stop) | P5 |
| 2026-01-13 | 11-15 | o18 | compra | 11:21:51 | 0 | 0 | referencia | 0 | n 1 | -0.13 (stop) | T0 |
| 2026-01-13 | 11-15 | o22 | compra | 12:44:54 | 0 | 0 | primer punto tras la toma | 3 | n 2 | -1.09 (stop) | P5 |
| 2026-01-14 | 07-11 | o2 | compra | 06:01:10 | 0 | 0 | primer punto tras la toma | 1 | n 1 | -1.25 (stop) | P5 |
| 2026-01-14 | 07-11 | o3 | compra | 06:02:00 | 0 | 0 | primer punto tras la toma | 1 | n 1 | -1.25 (stop) | T0 |
| 2026-01-14 | 07-11 | o5 | compra | 06:05:00 | 1 | 1 | posterior | 1 | n 1 | -1.00 (stop) | P5 |
| 2026-01-14 | 07-11 | o9 | compra | 08:01:30 | 0 | 0 | primer punto tras la toma | 3 | n 2 | -1.12 (stop) | P5 |
| 2026-01-14 | 07-11 | o10 | compra | 08:03:50 | 0 | 0 | primer punto tras la toma | 3 | n 2 | +3.60 (objetivo) | P5 |
| 2026-01-15 | 07-11 | o2 | venta | 06:12:00 | 0 | 0 | referencia | 1 | n 1 | +3.38 (objetivo) | P5 |
| 2026-01-15 | 07-11 | o4 | venta | 07:07:43 | 1 | 0 | primer punto tras la toma | 0 | n 2 | -0.10 (stop) | P5 |
| 2026-01-15 | 07-11 | o7 | venta | 08:30:20 | 1 | 1 | primer punto tras la toma | 2 | n 3 | -1.04 (stop) | P5 |
| 2026-01-15 | 11-15 | o14 | venta | 10:36:44 | 0 | 0 | referencia | 1 | n 1 | -0.19 (stop) | P6 |
| 2026-01-16 | 07-11 | o7 | venta | 09:27:42 | 0 | 0 | primer punto tras la toma | 1 | n 2 | +0.00 (stop) | P5 |
| 2026-01-16 | 11-15 | o15 | compra | 12:34:38 | 1 | 1 | posterior | 7 | n 1 | -1.00 (stop) | P6 |
| 2026-01-16 | 11-15 | o16 | compra | 12:35:15 | 1 | 1 | posterior | 7 | n 1 | +2.18 (objetivo) | P6 |
| 2026-01-16 | 11-15 | o17 | compra | 12:55:48 | 0 | 0 | referencia | 0 | n 2 | +0.00 (stop) | P6 |
| 2026-01-19 | 07-11 | o3 | compra | 06:48:30 | 0 | 0 | primer punto tras la toma | 2 | n 1 | +3.43 (objetivo) | P5 |
| 2026-01-19 | 07-11 | o5 | compra | 07:49:14 | 1 | 0 | primer punto tras la toma | 0 | n 2 | -0.05 (stop) | P5 |
| 2026-01-19 | 07-11 | o9 | compra | 08:16:01 | 1 | 0 | primer punto tras la toma | 3 | n 3 | -0.21 (stop) | P5 |
| 2026-01-19 | 07-11 | o15 | compra | 09:23:08 | 1 | 1 | posterior | 5 | n 4 | -1.14 (stop) | P5 |
| 2026-01-19 | 11-15 | o32 | venta | 13:25:19 | 1 | 0 | primer punto tras la toma | 1 | n 3 | -1.00 (stop) | T0 |
| 2026-01-20 | 11-15 | o6 | compra | 12:59:00 | 1 | 1 | posterior | 5 | n 1 | -1.00 (stop) | P5 |
| 2026-01-20 | 11-15 | o7 | compra | 13:00:11 | 1 | 1 | posterior | 5 | n 1 | -1.08 (stop) | P5 |
| 2026-01-20 | 11-15 | o13 | compra | 13:31:00 | 1 | 1 | posterior | 5 | n 2 | -1.00 (stop) | P5 |
| 2026-01-21 | 07-11 | o4 | venta | 06:46:24 | 0 | 0 | primer punto tras la toma | 3 | n 1 | -1.11 (stop) | P5 |
| 2026-01-21 | 11-15 | o15 | venta | 11:31:16 | 1 | 1 | posterior | 7 | n 1 | +0.00 (stop) | P5 |
| 2026-01-21 | 11-15 | o17 | venta | 12:25:09 | 0 | 0 | primer punto tras la toma | 1 | n 2 | -1.00 (stop) | P5 |
| 2026-01-22 | 07-11 | o2 | venta | 06:35:32 | 0 | 0 | primer punto tras la toma | 1 | n 1 | +3.75 (objetivo) | P6 |
| 2026-01-22 | 07-11 | o4 | venta | 07:28:14 | 0 | 0 | primer punto tras la toma | 0 | n 2 | -1.00 (stop) | P6 |
| 2026-01-23 | 07-11 | o6 | compra | 06:17:57 | 0 | 0 | primer punto tras la toma | 5 | n 1 | -1.00 (stop) | P5 |
| 2026-01-23 | 07-11 | o9 | compra | 06:53:22 | 0 | 0 | referencia | 0 | n 2 | -1.00 (stop) | P5 |
| 2026-01-23 | 07-11 | o10 | compra | 06:55:52 | 0 | 0 | primer punto tras la toma | 0 | n 2 | -1.00 (stop) | P5 |
| 2026-01-26 | 07-11 | o12 | compra | 07:49:56 | 1 | 1 | posterior | 5 | n 2 | -1.05 (stop) | P5 |
| 2026-01-27 | 07-11 | o3 | venta | 06:08:10 | 0 | 0 | primer punto tras la toma | 2 | n 1 | -1.10 (stop) | P5 |
| 2026-01-27 | 07-11 | o4 | venta | 06:10:02 | 1 | 1 | primer punto tras la toma | 2 | n 1 | +3.67 (objetivo) | P5 |
| 2026-01-27 | 07-11 | o9 | venta | 06:48:52 | 1 | 0 | primer punto tras la toma | 4 | n 2 | +3.48 (objetivo) | P5 |
| 2026-01-27 | 07-11 | o11 | venta | 09:55:21 | 0 | 0 | primer punto tras la toma | 1 | n 3 | -1.00 (stop) | P5 |
| 2026-01-27 | 11-15 | o14 | venta | 11:08:09 | 0 | 0 | primer punto tras la toma | 1 | n 1 | +0.00 (stop) | P6 |
| 2026-01-27 | 11-15 | o20 | venta | 12:01:00 | 0 | 0 | primer punto tras la toma | 5 | n 2 | -1.00 (stop) | P6 |
| 2026-01-27 | 11-15 | o21 | venta | 12:05:46 | 1 | 1 | posterior | 5 | n 2 | -1.00 (stop) | P6 |
| 2026-01-28 | 07-11 | o5 | compra | 07:54:45 | 0 | 0 | primer punto tras la toma | 4 | n 1 | +0.00 (stop) | P5 |
| 2026-01-28 | 07-11 | o9 | compra | 08:55:32 | 1 | 0 | primer punto tras la toma | 3 | n 2 | +0.00 (stop) | P5 |
| 2026-01-29 | 07-11 | o5 | compra | 06:14:55 | 1 | 1 | posterior | 4 | n 1 | +3.50 (objetivo) | P5 |
| 2026-01-29 | 07-11 | o16 | compra | 08:44:44 | 1 | 1 | posterior | 1 | n 3 | +0.00 (stop) | P5 |
| 2026-01-29 | 11-15 | o28 | venta | 12:54:12 | 0 | 0 | primer punto tras la toma | 3 | n 1 | -1.86 (stop) | P5 |
| 2026-01-29 | 11-15 | o29 | venta | 12:55:00 | 0 | 0 | primer punto tras la toma | 3 | n 1 | -1.00 (stop) | P5 |
| 2026-01-30 | 07-11 | o3 | venta | 07:35:25 | 0 | 0 | primer punto tras la toma | 2 | n 1 | +0.00 (stop) | P5 |
| 2026-01-30 | 11-15 | o8 | venta | 10:54:26 | 1 | 1 | primer punto tras la toma | 4 | n 1 | +0.00 (stop) | P5 |
| 2026-04-01 | 07-11 | o2 | compra | 07:56:07 | 1 | 0 | primer punto tras la toma | 1 | n 1 | -1.00 (stop) | P6 |
| 2026-04-01 | 11-15 | o7 | compra | 12:30:23 | 0 | 0 | primer punto tras la toma | 1 | n 1 | +2.10 (objetivo) | P5 |
| 2026-04-02 | 11-15 | o8 | venta | 12:11:26 | 0 | 0 | primer punto tras la toma | 7 | n 1 | -0.03 (stop) | P6 |
| 2026-04-03 | 07-11 | o10 | venta | 06:15:00 | 1 | 1 | posterior | 9 | n 1 | -1.00 (stop) | P5 |
| 2026-04-03 | 07-11 | o14 | venta | 06:54:47 | 1 | 0 | primer punto tras la toma | 2 | n 2 | -0.07 (stop) | P5 |
| 2026-04-03 | 11-15 | o20 | compra | 11:43:37 | 1 | 0 | primer punto tras la toma | 2 | n 2 | -0.23 (stop) | P5 |
| 2026-04-03 | 11-15 | o24 | compra | 12:41:05 | 1 | 0 | primer punto tras la toma | 2 | n 3 | -0.08 (stop) | P5 |
| 2026-04-06 | 07-11 | o5 | compra | 06:32:00 | 1 | 1 | primer punto tras la toma | 4 | n 1 | -1.06 (stop) | T0 |
| 2026-04-06 | 07-11 | o6 | compra | 08:57:01 | 0 | 0 | referencia | 0 | n 2 | -0.28 (manual) | P5 |
| 2026-04-06 | 11-15 | o11 | compra | 10:01:00 | 0 | 0 | primer punto tras la toma | 4 | n 1 | -1.00 (stop) | P6 · **E: llenada con la vela que la colocó (ADR-0051 §2)** |
| 2026-04-06 | 11-15 | o12 | compra | 10:03:00 | 1 | 1 | primer punto tras la toma | 4 | n 1 | +0.00 (stop) | P6 · **E: llenada con la vela que la colocó (ADR-0051 §2)** |
| 2026-04-07 | 07-11 | o1 | venta | 05:00:00 | 0 | 0 | referencia | 0 | n 1 | -2.00 (stop) | P6 · **E: llenada con la vela que la colocó (ADR-0051 §2)** |
| 2026-04-07 | 07-11 | o6 | venta | 06:31:14 | 0 | 0 | primer punto tras la toma | 1 | n 2 | -1.00 (stop) | P6 |
| 2026-04-07 | 11-15 | o28 | compra | 10:26:00 | 0 | 0 | referencia | 0 | n 1 | -1.10 (stop) | P6 · **E: llenada con la vela que la colocó (ADR-0051 §2)** |
| 2026-04-07 | 11-15 | o29 | compra | 10:29:00 | 0 | 0 | referencia | 0 | n 1 | -0.01 (stop) | P6 |
| 2026-04-08 | 07-11 | o4 | compra | 07:15:28 | 0 | 0 | primer punto tras la toma | 3 | n 1 | +3.48 (objetivo) | P6 |
| 2026-04-08 | 07-11 | o6 | compra | 08:16:20 | 0 | 0 | primer punto tras la toma | 1 | n 2 | -1.00 (stop) | P6 |
| 2026-04-09 | 07-11 | o2 | compra | 05:03:28 | 1 | 0 | primer punto tras la toma | 0 | n 1 | -1.00 (stop) | P5 |
| 2026-04-09 | 07-11 | o6 | compra | 05:41:30 | 0 | 0 | primer punto tras la toma | 0 | n 2 | -1.12 (stop) | P5 |
| 2026-04-09 | 11-15 | o8 | compra | 11:04:24 | 0 | 0 | referencia | 1 | n 1 | +3.73 (objetivo) | P5 |
| 2026-04-10 | 11-15 | o3 | venta | 09:25:48 | 1 | 0 | primer punto tras la toma | 2 | n 1 | +0.00 (stop) | P6 |
| 2026-04-10 | 11-15 | o8 | venta | 11:12:19 | 1 | 0 | primer punto tras la toma | 3 | n 3 | -1.00 (stop) | P6 |
| 2026-04-10 | 11-15 | o16 | venta | 12:39:11 | 1 | 1 | posterior | 4 | n 4 | +0.00 (stop) | P6 |
| 2026-04-13 | 07-11 | o5 | compra | 05:05:00 | 0 | 0 | primer punto tras la toma | 4 | n 1 | -1.00 (stop) | P5 |
| 2026-04-14 | 07-11 | o7 | compra | 06:23:31 | 0 | 0 | primer punto tras la toma | 1 | n 2 | +3.75 (objetivo) | T0 |
| 2026-04-14 | 11-15 | o16 | compra | 12:05:49 | 0 | 0 | primer punto tras la toma | 2 | n 1 | -1.00 (stop) | T0 |
| 2026-04-14 | 11-15 | o17 | compra | 12:10:38 | 1 | 1 | posterior | 2 | n 1 | +0.00 (stop) | P5 |
| 2026-04-15 | 07-11 | o8 | venta | 06:14:16 | 0 | 0 | referencia | 0 | n 2 | +0.00 (stop) | P6 |
| 2026-04-15 | 11-15 | o23 | compra | 10:32:09 | 0 | 0 | primer punto tras la toma | 4 | n 2 | -1.07 (stop) | P6 |
| 2026-04-15 | 11-15 | o26 | compra | 10:36:04 | 1 | 1 | posterior | 6 | n 2 | -1.10 (stop) | P6 |
| 2026-04-15 | 11-15 | o28 | compra | 11:49:12 | 0 | 0 | referencia | 0 | n 3 | +0.00 (stop) | P6 |
| 2026-04-16 | 07-11 | o4 | compra | 06:08:17 | 0 | 0 | primer punto tras la toma | 3 | n 1 | -1.00 (stop) | P5 |
| 2026-04-16 | 07-11 | o7 | compra | 06:11:29 | 1 | 1 | primer punto tras la toma | 5 | n 1 | -0.04 (stop) | P5 |
| 2026-04-16 | 07-11 | o9 | compra | 07:56:02 | 0 | 0 | primer punto tras la toma | 0 | n 2 | -1.33 (stop) | P5 |
| 2026-04-16 | 11-15 | o18 | venta | 11:10:27 | 1 | 1 | posterior | 8 | n 1 | +0.00 (stop) | P5 |
| 2026-04-17 | 07-11 | o10 | venta | 08:55:41 | 1 | 1 | posterior | 9 | n 1 | -1.00 (stop) | P5 |
| 2026-04-20 | 07-11 | o2 | compra | 05:30:00 | 0 | 0 | primer punto tras la toma | 1 | n 1 | -1.00 (stop) | P6 |
| 2026-04-20 | 07-11 | o5 | compra | 05:33:17 | 1 | 1 | posterior | 3 | n 1 | -1.00 (stop) | P6 |
| 2026-04-20 | 11-15 | o8 | compra | 09:33:46 | 0 | 0 | referencia | 2 | n 1 | +0.00 (stop) | P6 |
| 2026-04-22 | 07-11 | o3 | venta | 05:15:02 | 1 | 0 | primer punto tras la toma | 2 | n 1 | -1.29 (stop) | P5 |
| 2026-04-22 | 07-11 | o8 | venta | 07:46:00 | 0 | 0 | referencia | 0 | n 2 | -1.00 (stop) | P5 |
| 2026-04-22 | 11-15 | o21 | compra | 11:46:12 | 1 | 1 | primer punto tras la toma | 6 | n 2 | -1.05 (stop) | P6 |
| 2026-04-23 | 07-11 | o1 | venta | 05:01:00 | 0 | 0 | referencia | 0 | n 1 | -1.14 (stop) | P5 |
| 2026-04-23 | 07-11 | o3 | venta | 05:05:00 | 0 | 0 | primer punto tras la toma | 1 | n 1 | -2.00 (stop) | P5 · **E: llenada con la vela que la colocó (ADR-0051 §2)** |
| 2026-04-23 | 07-11 | o12 | venta | 06:55:12 | 1 | 1 | posterior | 2 | n 2 | +3.56 (objetivo) | P5 |
| 2026-04-24 | 07-11 | o6 | venta | 05:43:18 | 1 | 1 | posterior | 5 | n 1 | -1.50 (stop) | P5 |
| 2026-04-24 | 07-11 | o8 | venta | 06:44:30 | 0 | 0 | primer punto tras la toma | 0 | n 2 | +3.75 (objetivo) | T0 |
| 2026-04-24 | 07-11 | o19 | venta | 08:01:31 | 1 | 0 | primer punto tras la toma | 10 | n 3 | +0.00 (stop) | P5 |
| 2026-04-24 | 07-11 | o20 | venta | 08:06:38 | 1 | 1 | posterior | 10 | n 3 | -1.00 (stop) | P5 |
| 2026-04-24 | 07-11 | o23 | venta | 08:22:57 | 0 | 0 | primer punto tras la toma | 1 | n 4 | +3.29 (objetivo) | P5 |
| 2026-04-24 | 11-15 | o26 | compra | 12:37:44 | 0 | 0 | primer punto tras la toma | 2 | n 1 | -1.09 (stop) | P5 |
| 2026-04-24 | 11-15 | o27 | compra | 12:39:32 | 1 | 0 | primer punto tras la toma | 2 | n 1 | -1.00 (stop) | P5 |
| 2026-04-27 | 07-11 | o2 | compra | 05:01:07 | 0 | 0 | primer punto tras la toma | 0 | n 1 | -1.00 (stop) | P6 |
| 2026-04-27 | 07-11 | o3 | compra | 05:02:02 | 0 | 0 | primer punto tras la toma | 0 | n 1 | -1.11 (stop) | P6 |
| 2026-04-27 | 07-11 | o4 | compra | 05:03:44 | 0 | 0 | primer punto tras la toma | 0 | n 1 | +0.00 (stop) | P6 |
| 2026-04-27 | 07-11 | o11 | compra | 06:04:52 | 0 | 0 | primer punto tras la toma | 4 | n 2 | -1.00 (stop) | P6 |
| 2026-04-28 | 07-11 | o4 | venta | 08:11:54 | 0 | 0 | primer punto tras la toma | 3 | n 1 | -1.07 (stop) | T0 |
| 2026-04-28 | 11-15 | o9 | venta | 11:14:06 | 1 | 1 | primer punto tras la toma | 4 | n 1 | +0.00 (stop) | P6 |
| 2026-04-28 | 11-15 | o10 | venta | 12:54:41 | 0 | 0 | referencia | 0 | n 2 | -1.00 (stop) | P6 |
| 2026-04-29 | 07-11 | o6 | venta | 07:14:06 | 1 | 1 | posterior | 5 | n 1 | -0.10 (stop) | P5 |
| 2026-04-29 | 11-15 | o11 | venta | 09:36:33 | 0 | 0 | primer punto tras la toma | 3 | n 1 | +3.64 (objetivo) | T0 |
| 2026-07-01 | 07-11 | o4 | venta | 05:11:13 | 0 | 0 | primer punto tras la toma | 3 | n 1 | -1.00 (stop) | P5 |
| 2026-07-01 | 07-11 | o5 | venta | 05:12:11 | 1 | 1 | primer punto tras la toma | 3 | n 1 | -1.00 (stop) | P5 |
| 2026-07-01 | 11-15 | o10 | venta | 10:58:16 | 1 | 1 | posterior | 3 | n 1 | +3.60 (objetivo) | P5 |
| 2026-07-02 | 07-11 | o3 | compra | 05:37:32 | 0 | 0 | primer punto tras la toma | 2 | n 1 | -1.00 (stop) | P6 |
| 2026-07-02 | 07-11 | o4 | compra | 05:40:20 | 1 | 1 | posterior | 2 | n 1 | +0.00 (stop) | P6 |
| 2026-07-02 | 11-15 | o7 | compra | 09:13:30 | 0 | 0 | primer punto tras la toma | 2 | n 1 | +0.00 (stop) | P5 |
| 2026-07-02 | 11-15 | o9 | compra | 10:18:40 | 0 | 0 | primer punto tras la toma | 0 | n 2 | -1.29 (stop) | P5 |
| 2026-07-02 | 11-15 | o12 | compra | 10:21:52 | 1 | 1 | posterior | 2 | n 2 | -1.00 (stop) | T0 |
| 2026-07-02 | 11-15 | o24 | compra | 12:01:00 | 1 | 1 | posterior | 11 | n 3 | -1.00 (stop) | T0 |
| 2026-07-02 | 11-15 | o25 | compra | 12:02:09 | 1 | 1 | posterior | 11 | n 3 | -1.00 (stop) | P5 |
| 2026-07-03 | 07-11 | o4 | compra | 06:02:06 | 0 | 0 | primer punto tras la toma | 3 | n 1 | -1.00 (stop) | P5 |
| 2026-07-03 | 07-11 | o5 | compra | 06:03:31 | 0 | 0 | primer punto tras la toma | 3 | n 1 | +2.57 (objetivo) | P5 |
| 2026-07-03 | 07-11 | o6 | compra | 07:24:42 | 0 | 0 | referencia | 0 | n 2 | -1.00 (stop) | P5 |
| 2026-07-03 | 07-11 | o8 | compra | 07:35:41 | 1 | 1 | posterior | 1 | n 2 (vig. n 3) | -1.00 (stop) | P5 |
| 2026-07-03 | 11-15 | o15 | compra | 09:13:34 | 0 | 0 | primer punto tras la toma | 3 | n 1 | +0.00 (stop) | P5 |
| 2026-07-07 | 07-11 | o6 | venta | 08:26:50 | 1 | 1 | posterior | 5 | n 1 | -1.00 (stop) | P5 |
| 2026-07-07 | 11-15 | o7 | venta | 10:35:15 | 0 | 0 | referencia | 0 | n 1 | -1.07 (stop) | P5 |
| 2026-07-07 | 11-15 | o11 | venta | 10:43:03 | 1 | 1 | posterior | 3 | n 1 | -0.14 (stop) | P5 |
| 2026-07-07 | 11-15 | o15 | venta | 11:26:01 | 0 | 0 | primer punto tras la toma | 3 | n 2 | -1.00 (stop) | P5 |
| 2026-07-07 | 11-15 | o22 | venta | 12:35:03 | 1 | 1 | posterior | 4 | n 3 | +3.20 (objetivo) | P5 |
| 2026-07-08 | 07-11 | o2 | compra | 07:19:11 | 0 | 0 | referencia | 1 | n 1 | +3.67 (objetivo) | T0 |
| 2026-07-08 | 07-11 | o6 | compra | 08:25:52 | 0 | 0 | primer punto tras la toma | 3 | n 2 | -0.41 (stop) | P5 |
| 2026-07-09 | 07-11 | o4 | compra | 07:52:19 | 0 | 0 | primer punto tras la toma | 3 | n 1 | -1.00 (stop) | P5 |
| 2026-07-09 | 07-11 | o8 | compra | 08:45:25 | 1 | 0 | primer punto tras la toma | 2 | n 2 | -1.00 (stop) | P5 |
| 2026-07-09 | 11-15 | o16 | compra | 10:59:01 | 1 | 1 | posterior | 4 | n 1 | -0.09 (stop) | P5 |
| 2026-07-10 | 07-11 | o3 | compra | 05:28:00 | 1 | 1 | primer punto tras la toma | 1 | n 1 | -1.00 (stop) | P5 · **E: llenada con la vela que la colocó (ADR-0051 §2)** |
| 2026-07-10 | 07-11 | o4 | compra | 05:32:00 | 1 | 1 | posterior | 1 | n 1 | -1.00 (stop) | T0 · **E: llenada con la vela que la colocó (ADR-0051 §2)** |
| 2026-07-10 | 07-11 | o12 | compra | 07:59:02 | 1 | 1 | posterior | 3 | n 3 | -1.11 (stop) | P5 |
| 2026-07-10 | 11-15 | o16 | venta | 10:58:43 | 0 | 0 | primer punto tras la toma | 2 | n 1 | -1.00 (stop) | T0 |
| 2026-07-13 | 07-11 | o12 | venta | 07:13:34 | 0 | 0 | primer punto tras la toma | 1 | n 2 | +0.00 (stop) | P5 |
| 2026-07-13 | 11-15 | o13 | compra | 09:02:14 | 0 | 0 | referencia | 0 | n 1 | -0.05 (stop) | P5 |
| 2026-07-13 | 11-15 | o22 | compra | 09:55:33 | 1 | 0 | primer punto tras la toma | 1 | n 2 | +0.00 (stop) | P5 |
| 2026-07-14 | 07-11 | o2 | compra | 06:20:07 | 0 | 0 | referencia | 1 | n 1 | -1.00 (stop) | T0 |
| 2026-07-14 | 07-11 | o7 | compra | 06:55:30 | 1 | 1 | primer punto tras la toma | 2 | n 2 | -1.00 (stop) | T0 |
| 2026-07-14 | 11-15 | o11 | compra | 09:35:04 | 0 | 0 | primer punto tras la toma | 3 | n 1 | +0.00 (stop) | T0 |
| 2026-07-15 | 07-11 | o3 | compra | 05:04:01 | 0 | 0 | primer punto tras la toma | 2 | n 1 | -1.00 (stop) | P5 |
| 2026-07-15 | 07-11 | o4 | compra | 05:06:16 | 0 | 0 | primer punto tras la toma | 2 | n 1 | -1.08 (stop) | T0 |
| 2026-07-15 | 07-11 | o7 | compra | 06:45:00 | 0 | 0 | primer punto tras la toma | 0 | n 2 | -1.00 (stop) | P5 |
| 2026-07-15 | 11-15 | o23 | venta | 12:37:22 | 0 | 0 | primer punto tras la toma | 1 | n 1 | -1.04 (stop) | P5 |
| 2026-07-15 | 11-15 | o24 | venta | 12:39:37 | 0 | 0 | primer punto tras la toma | 1 | n 1 | -1.00 (stop) | P5 |
| 2026-07-16 | 07-11 | o6 | compra | 05:55:58 | 1 | 1 | posterior | 5 | n 1 | -1.00 (stop) | T0 |
| 2026-07-16 | 11-15 | o12 | compra | 09:35:57 | 0 | 0 | primer punto tras la toma | 2 | n 1 | +3.67 (objetivo) | P5 |
| 2026-07-16 | 11-15 | o18 | compra | 12:40:41 | 0 | 0 | primer punto tras la toma | 0 | n 3 | -1.03 (stop) | P5 |
| 2026-07-17 | 07-11 | o10 | venta | 05:46:05 | 1 | 0 | primer punto tras la toma | 9 | n 1 | -1.00 (stop) | T0 |
| 2026-07-17 | 07-11 | o22 | venta | 06:32:32 | 1 | 1 | posterior | 11 | n 2 | -1.00 (stop) | P5 |
| 2026-07-17 | 11-15 | o24 | compra | 09:40:58 | 0 | 0 | referencia | 1 | n 1 | -0.05 (stop) | P5 |
| 2026-07-17 | 11-15 | o26 | compra | 10:54:43 | 0 | 0 | referencia | 0 | n 3 | -1.00 (stop) | P5 |
| 2026-07-17 | 11-15 | o38 | compra | 12:46:33 | 1 | 1 | posterior | 4 | n 4 | +0.00 (stop) | P5 |
| 2026-08-03 | 07-11 | o1 | venta | 05:48:46 | 0 | 0 | referencia | 0 | n 1 | +0.00 (stop) | P5 |
| 2026-08-03 | 07-11 | o2 | venta | 05:51:09 | 0 | 0 | primer punto tras la toma | 0 | n 1 | -1.00 (stop) | P5 |
| 2026-08-03 | 07-11 | o6 | venta | 07:36:53 | 0 | 0 | referencia | 3 | n 2 | -0.03 (stop) | P5 |
| 2026-08-03 | 11-15 | o14 | venta | 09:51:57 | 1 | 1 | posterior | 7 | n 1 | +0.00 (stop) | T0 |
| 2026-08-03 | 11-15 | o18 | venta | 11:06:13 | 1 | 1 | posterior | 3 | n 2 | -1.08 (stop) | P5 |
| 2026-08-03 | 11-15 | o28 | venta | 12:03:38 | 1 | 1 | posterior | 9 | n 3 | -1.05 (stop) | P5 |
| 2026-08-04 | 11-15 | o15 | venta | 10:54:04 | 1 | 1 | primer punto tras la toma | 5 | n 1 | +0.00 (stop) | P5 |
| 2026-08-05 | 07-11 | o9 | compra | 06:24:06 | 1 | 1 | posterior | 3 | n 2 | -1.00 (stop) | P6 |
| 2026-08-05 | 11-15 | o17 | compra | 12:47:25 | 0 | 0 | primer punto tras la toma | 3 | n 1 | -1.00 (stop) | P6 |
| 2026-08-06 | 07-11 | o4 | venta | 05:59:27 | 0 | 0 | primer punto tras la toma | 3 | n 1 | -1.00 (stop) | P5 |
| 2026-08-06 | 07-11 | o5 | venta | 06:00:00 | 1 | 1 | primer punto tras la toma | 3 | n 1 | -1.00 (stop) | T0 |
| 2026-08-06 | 11-15 | o11 | venta | 10:34:53 | 0 | 0 | primer punto tras la toma | 4 | n 1 | +0.00 (stop) | P6 |
| 2026-08-07 | 07-11 | o4 | compra | 05:27:15 | 0 | 0 | primer punto tras la toma | 3 | n 1 | -1.00 (stop) | P5 |
| 2026-08-07 | 07-11 | o13 | compra | 07:07:54 | 1 | 1 | primer punto tras la toma | 2 | n 2 | -0.11 (stop) | P5 |
| 2026-08-07 | 07-11 | o14 | compra | 07:10:00 | 1 | 1 | posterior | 2 | n 2 | +0.00 (stop) | P5 |
| 2026-08-07 | 07-11 | o16 | compra | 08:15:10 | 0 | 0 | primer punto tras la toma | 1 | n 3 | +0.00 (stop) | P5 |
| 2026-08-07 | 11-15 | o17 | compra | 10:49:23 | 0 | 0 | referencia | 0 | n 1 | -0.25 (stop) | P5 |
| 2026-08-10 | 07-11 | o2 | venta | 05:08:18 | 0 | 0 | referencia | 1 | n 1 | +0.00 (stop) | P6 |
| 2026-08-10 | 11-15 | o16 | compra | 09:39:10 | 0 | 0 | primer punto tras la toma | 3 | n 1 | -1.00 (stop) | P5 |
| 2026-08-10 | 11-15 | o18 | compra | 09:42:02 | 1 | 1 | posterior | 4 | n 1 | +3.75 (objetivo) | P5 |
| 2026-08-10 | 11-15 | o24 | compra | 11:16:11 | 0 | 0 | primer punto tras la toma | 5 | n 2 | -0.08 (stop) | P5 |
| 2026-08-10 | 11-15 | o25 | compra | 11:21:38 | 1 | 1 | posterior | 5 | n 2 | -1.00 (stop) | P5 |
| 2026-08-11 | 07-11 | o2 | compra | 05:57:13 | 0 | 0 | referencia | 1 | n 1 | +0.00 (stop) | P5 |
| 2026-08-11 | 07-11 | o7 | compra | 08:08:39 | 1 | 0 | primer punto tras la toma | 4 | n 2 | +0.00 (stop) | T0 |
| 2026-08-11 | 11-15 | o12 | venta | 11:06:43 | 0 | 0 | primer punto tras la toma | 4 | n 1 | -1.00 (stop) | P6 |
| 2026-08-11 | 11-15 | o13 | venta | 11:08:02 | 1 | 1 | primer punto tras la toma | 4 | n 1 | -0.05 (stop) | P6 |
| 2026-08-12 | 07-11 | o8 | venta | 08:26:03 | 0 | 0 | primer punto tras la toma | 2 | n 2 | -1.00 (stop) | P5 |
| 2026-08-12 | 11-15 | o14 | venta | 11:37:49 | 1 | 0 | primer punto tras la toma | 1 | n 2 | -1.21 (stop) | P6 |
| 2026-08-13 | 07-11 | o2 | venta | 05:04:24 | 1 | 0 | primer punto tras la toma | 1 | n 1 | -1.17 (stop) | P5 |
| 2026-08-13 | 07-11 | o9 | venta | 08:51:21 | 0 | 0 | referencia | 0 | n 3 | +1.86 (manual) | P5 |
| 2026-08-17 | 07-11 | o1 | compra | 05:00:01 | 0 | 0 | referencia | 0 | n 1 | -1.00 (stop) | P5 |
| 2026-08-17 | 11-15 | o15 | compra | 10:12:19 | 1 | 0 | primer punto tras la toma | 4 | n 1 | +0.00 (stop) | P6 |
| 2026-08-17 | 11-15 | o17 | compra | 10:42:34 | 0 | 0 | primer punto tras la toma | 0 | n 2 | -0.20 (stop) | P6 |
| 2026-08-18 | 07-11 | o4 | venta | 05:51:15 | 1 | 1 | primer punto tras la toma | 3 | n 1 | -1.00 (stop) | P6 |
| 2026-08-18 | 07-11 | o6 | venta | 07:08:15 | 0 | 0 | primer punto tras la toma | 1 | n 2 | -1.22 (stop) | P6 |
| 2026-08-18 | 07-11 | o10 | venta | 07:32:00 | 1 | 0 | primer punto tras la toma | 2 | n 3 | -1.00 (stop) | P6 |
| 2026-08-18 | 11-15 | o14 | venta | 09:36:18 | 0 | 0 | referencia | 3 | n 1 | -1.00 (stop) | P6 |
| 2026-08-18 | 11-15 | o15 | venta | 09:40:20 | 1 | 0 | primer punto tras la toma | 3 | n 1 | -0.33 (stop) | P6 |
| 2026-08-18 | 11-15 | o18 | venta | 12:10:07 | 0 | 0 | primer punto tras la toma | 0 | n 3 | -1.00 (stop) | P6 |
| 2026-08-20 | 07-11 | o3 | venta | 06:02:00 | 1 | 0 | primer punto tras la toma | 2 | n 1 | -1.00 (stop) | P5 |
| 2026-08-20 | 07-11 | o14 | venta | 07:45:00 | 0 | 0 | primer punto tras la toma | 1 | n 3 | -1.00 (stop) | P5 · **E: llenada con la vela que la colocó (ADR-0051 §2)** |
| 2026-08-20 | 07-11 | o17 | venta | 08:47:50 | 1 | 0 | primer punto tras la toma | 1 | n 4 | -1.00 (stop) | P5 |
| 2026-08-20 | 11-15 | o19 | compra | 10:50:01 | 0 | 0 | referencia | 1 | n 1 | -1.00 (stop) | P5 |
| 2026-08-20 | 11-15 | o30 | compra | 11:49:09 | 1 | 1 | primer punto tras la toma | 3 | n 2 | -1.00 (stop) | T0 |
| 2026-08-21 | 07-11 | o2 | compra | 05:32:51 | 0 | 0 | referencia | 1 | n 1 | +3.60 (objetivo) | T0 |
| 2026-08-21 | 07-11 | o5 | compra | 07:49:14 | 0 | 0 | primer punto tras la toma | 2 | n 2 | -1.00 (stop) | P5 |
| 2026-08-21 | 07-11 | o7 | compra | 07:51:12 | 1 | 1 | posterior | 2 | n 2 | -1.00 (stop) | P5 |
| 2026-08-21 | 11-15 | o10 | compra | 11:37:05 | 0 | 0 | primer punto tras la toma | 2 | n 1 | -1.05 (stop) | P5 |
| 2026-08-21 | 11-15 | o14 | compra | 12:21:03 | 0 | 0 | primer punto tras la toma | 1 | n 2 | +0.00 (stop) | P5 |
| 2026-08-24 | 07-11 | o3 | compra | 05:25:00 | 0 | 0 | primer punto tras la toma | 2 | n 1 | -1.00 (stop) | P6 |
| 2026-08-24 | 07-11 | o4 | compra | 05:27:04 | 1 | 1 | posterior | 2 | n 1 | -1.00 (stop) | P6 |
| 2026-08-24 | 07-11 | o6 | compra | 06:26:02 | 1 | 0 | primer punto tras la toma | 1 | n 2 | -1.08 (stop) | P6 |
| 2026-08-24 | 07-11 | o12 | compra | 07:19:42 | 0 | 0 | primer punto tras la toma | 3 | n 3 | +0.00 (stop) | P6 |
| 2026-08-24 | 07-11 | o21 | compra | 08:15:54 | 0 | 0 | primer punto tras la toma | 1 | n 5 | -1.10 (stop) | P6 |
| 2026-08-24 | 11-15 | o25 | venta | 11:29:53 | 0 | 0 | primer punto tras la toma | 1 | n 1 | -1.00 (stop) | T0 |
| 2026-08-24 | 11-15 | o30 | venta | 12:31:22 | 1 | 0 | primer punto tras la toma | 4 | n 2 | -0.07 (stop) | P5 |
| 2026-08-25 | 07-11 | o2 | venta | 06:21:07 | 1 | 0 | primer punto tras la toma | 1 | n 1 | -1.09 (stop) | P5 |
| 2026-08-25 | 07-11 | o10 | venta | 07:23:47 | 1 | 1 | posterior | 5 | n 2 | +3.20 (objetivo) | P5 |
| 2026-08-25 | 07-11 | o12 | venta | 08:31:03 | 0 | 0 | primer punto tras la toma | 1 | n 3 | -1.00 (stop) | P5 |
| 2026-08-25 | 07-11 | o13 | venta | 08:32:02 | 0 | 0 | primer punto tras la toma | 1 | n 3 | +0.00 (stop) | P5 |
| 2026-08-25 | 11-15 | o19 | venta | 11:54:00 | 0 | 0 | primer punto tras la toma | 1 | n 1 | +3.75 (objetivo) | P5 |
| 2026-08-26 | 07-11 | o7 | venta | 05:39:19 | 0 | 0 | primer punto tras la toma | 6 | n 1 | -1.00 (stop) | T0 |
| 2026-08-26 | 07-11 | o10 | venta | 05:42:54 | 0 | 0 | primer punto tras la toma | 8 | n 1 | -1.00 (stop) | P5 |
| 2026-08-26 | 07-11 | o11 | venta | 05:44:11 | 1 | 1 | posterior | 8 | n 1 | -1.00 (stop) | P5 |
| 2026-08-26 | 07-11 | o17 | venta | 07:07:02 | 0 | 0 | primer punto tras la toma | 5 | n 2 | -1.12 (stop) | P5 |
| 2026-08-26 | 11-15 | o24 | compra | 10:31:00 | 0 | 0 | primer punto tras la toma | 3 | n 1 | +0.00 (stop) | P5 |
| 2026-08-26 | 11-15 | o27 | compra | 11:26:30 | 0 | 0 | referencia | 0 | n 3 | +3.60 (objetivo) | T0 |
| 2026-08-27 | 11-15 | o9 | venta | 12:13:40 | 1 | 1 | primer punto tras la toma | 2 | n 1 | +0.00 (stop) | T0 |
| 2026-08-28 | 07-11 | o6 | venta | 06:05:52 | 1 | 1 | posterior | 5 | n 1 | -1.00 (stop) | P6 |
| 2026-08-28 | 11-15 | o16 | venta | 10:42:17 | 0 | 0 | primer punto tras la toma | 9 | n 1 | -1.08 (stop) | T0 |
| 2026-08-31 | 07-11 | o4 | compra | 05:40:41 | 1 | 0 | primer punto tras la toma | 3 | n 1 | -1.00 (stop) | P5 |
| 2026-08-31 | 07-11 | o7 | compra | 06:58:11 | 0 | 0 | referencia | 1 | n 2 | -1.00 (stop) | T0 |
| 2026-08-31 | 11-15 | o14 | compra | 12:41:16 | 0 | 0 | referencia | 1 | n 1 | -0.33 (stop) | P6 |

## 4. La lista «Para S-14»: las sesiones de P6 de la corrida 2 (el bot opera y el trader no)

De `patrones-diaria.txt` (P6: 77 filas en **34 sesiones**; 49 «en sesión», en días en que el trader
operó la otra sesión, y 28 «en día», en días sin ninguna operación del trader), cruzadas por el
guion `lista_s14.py` (solo lee los anexos) con `entradas-antes-alternancia.txt` (el sesgo y el
camino del bot, el R de cada llenada) y con `cuenta-arrastrada.txt` (si la cuenta de la corrida 1
llega). Fichero: `lista-s14.txt`. **Los días los elige el consultor al preparar la hoja de la sesión
6**; ninguna fila lleva nada anterior a su día dev. «Viene de vídeo» por §0.d: abril solo el 29 (no
hay P6 ese día), julio «según el trader», enero y agosto no. **La cuenta arrastrada de la corrida 1
no corta el tramo (EN_CURSO)** pero su última sesión con un llenado es `2026-01-20 11-15` (§2.2,
RN-032): las 5 sesiones de P6 anteriores a ella tuvieron también llenadas en la corrida 1 (las
mismas), y las 29 posteriores no tienen ninguna orden en la corrida 1.

| día | sesión | vídeo | operaciones del bot (lado, llenada UTC) | sesgo | camino del bot (primer instante de cada hecho) | R de cada llenada | corrida 1 |
|---|---|---|---|---|---|---|---|
| 2026-01-06 | 11-15 | no | 2 ventas (13:43:00, 13:44:30) | bajista | sesgo 10:00Z → liquidez_tomada 13:36Z → orden_dimensionada 13:36Z | -1.12 (stop); +3.50 (objetivo) | llega: llenó 2 |
| 2026-01-07 | 11-15 | no | 2 ventas (10:03:27, 13:00:00) | bajista | 10:00Z → 10:03Z → 10:03Z | -1.00 (stop); -1.00 (stop) | llega: llenó 2 |
| 2026-01-09 | 11-15 | no | 1 venta (13:38:25) | bajista | 10:00Z → 10:39Z → 10:39Z | -1.00 (stop) | llega: llenó 1 |
| 2026-01-15 | 11-15 | no | 1 venta (10:36:44) | bajista | 10:00Z → 10:35Z → 10:35Z | -0.19 (stop) | llega: llenó 1 |
| 2026-01-16 | 11-15 | no | 3 compras (12:34:38, 12:35:15, 12:55:48) | alcista | 10:00Z → 12:25Z → 12:25Z | -1.00 (stop); +2.18 (objetivo); +0.00 (stop) | llega: llenó 3 |
| 2026-01-22 | 07-11 | no | 2 ventas (06:35:32, 07:28:14) | bajista | 06:00Z → 06:32Z → 06:32Z | +3.75 (objetivo); -1.00 (stop) | posterior al 2026-01-20 11-15: sin orden |
| 2026-01-27 | 11-15 | no | 3 ventas (11:08:09, 12:01:00, 12:05:46) | bajista | 10:00Z → 11:06Z → 11:06Z | +0.00 (stop); -1.00 (stop); -1.00 (stop) | sin orden |
| 2026-04-01 | 07-11 | no | 2 compras (07:56:07, 08:03:21) | alcista | 05:00Z → 07:50Z → 07:50Z | -1.00 (stop); +0.00 (stop) | sin orden |
| 2026-04-02 | 11-15 | no | 2 ventas (12:11:26, 12:54:03) | bajista | 09:00Z → 12:03Z → 12:03Z | -0.03 (stop); +1.43 (manual) | sin orden |
| 2026-04-06 | 11-15 | no | 2 compras (10:01:00, 10:03:00) · posible M (hora perdida 2026-04-06T10Z) · **las dos, E: llenada con la vela que la colocó (ADR-0051 §2)** | alcista | 09:00Z → 09:55Z → 09:55Z | -1.00 (stop); +0.00 (stop) | sin orden |
| 2026-04-07 | 07-11 | no | 3 ventas (05:00:00, 05:09:27, 06:31:14) · **la de 05:00:00, E: llenada con la vela que la colocó (ADR-0051 §2)** | bajista | 05:00Z → 05:00Z → 05:00Z | -2.00 (stop); -0.33 (stop); -1.00 (stop) | sin orden |
| 2026-04-07 | 11-15 | no | 2 compras (10:26:00, 10:29:00) · posible M (2026-04-07T10Z) · **la de 10:26:00, E: llenada con la vela que la colocó (ADR-0051 §2)** | alcista | 09:00Z → 10:26Z → 10:26Z | -1.10 (stop); -0.01 (stop) | sin orden |
| 2026-04-08 | 07-11 | no | 2 compras (07:15:28, 08:16:20) | alcista | 05:00Z → 07:11Z → 07:11Z | +3.48 (objetivo); -1.00 (stop) | sin orden |
| 2026-04-10 | 11-15 | no | 4 ventas (09:25:48, 11:12:19, 11:15:07, 12:39:11) | bajista | 09:00Z → 09:19Z → 09:19Z | +0.00; -1.00; +0.00; +0.00 (stops) | sin orden |
| 2026-04-15 | 07-11 | no | 1 venta (06:14:16) | bajista | 05:00Z → 05:02Z → 05:02Z | +0.00 (stop) | sin orden |
| 2026-04-15 | 11-15 | no | 5 compras (09:14:00, 10:32:09, 10:36:04, 10:40:53, 11:49:12) | alcista | 09:00Z → 09:04Z → 09:04Z | +0.00; -1.07; -1.10; -0.17; +0.00 (stops) | sin orden |
| 2026-04-20 | 07-11 | no | 2 compras (05:30:00, 05:33:17) | alcista | 05:00Z → 05:27Z → 05:27Z | -1.00 (stop); -1.00 (stop) | sin orden |
| 2026-04-20 | 11-15 | no | 2 compras (09:33:46, 12:17:20) | alcista | 09:00Z → 09:28Z → 09:28Z | +0.00 (stop); -0.04 (stop) | sin orden |
| 2026-04-22 | 11-15 | no | 1 compra (11:46:12) | alcista | 09:00Z → 09:55Z → 09:55Z | -1.05 (stop) | sin orden |
| 2026-04-27 | 07-11 | no | 4 compras (05:01:07, 05:02:02, 05:03:44, 06:04:52) | alcista | 05:00Z → 05:00Z → 05:00Z | -1.00; -1.11; +0.00; -1.00 (stops) | sin orden |
| 2026-04-28 | 11-15 | no | 2 ventas (11:14:06, 12:54:41) | bajista | 09:00Z → 11:06Z → 11:06Z | +0.00 (stop); -1.00 (stop) | sin orden |
| 2026-07-02 | 07-11 | según el trader (v11-v13; lo comprueba T) | 2 compras (05:37:32, 05:40:20) | alcista | 05:00Z → 05:33Z → 05:33Z | -1.00 (stop); +0.00 (stop) | sin orden |
| 2026-08-05 | 07-11 | no | 1 compra (06:24:06) | alcista | 05:00Z → 05:03Z → 05:03Z | -1.00 (stop) | sin orden |
| 2026-08-05 | 11-15 | no | 1 compra (12:47:25) | alcista | 09:00Z → 12:44Z → 12:44Z | -1.00 (stop) | sin orden |
| 2026-08-06 | 11-15 | no | 1 venta (10:34:53) | bajista | 09:00Z → 10:29Z → 10:29Z | +0.00 (stop) | sin orden |
| 2026-08-10 | 07-11 | no | 2 ventas (05:08:18, 07:32:42) | bajista | 05:00Z → 05:07Z → 05:07Z | +0.00 (stop); -1.08 (stop) | sin orden |
| 2026-08-11 | 11-15 | no | 2 ventas (11:06:43, 11:08:02) | bajista | 09:00Z → 11:02Z → 11:02Z | -1.00 (stop); -0.05 (stop) | sin orden |
| 2026-08-12 | 11-15 | no | 1 venta (11:37:49) | bajista | 09:00Z → 09:13Z → 09:13Z | -1.21 (stop) | sin orden |
| 2026-08-17 | 11-15 | no | 2 compras (10:12:19, 10:42:34) | alcista | 09:00Z → 10:06Z → 10:06Z | +0.00 (stop); -0.20 (stop) | sin orden |
| 2026-08-18 | 07-11 | no | 4 ventas (05:51:15, 07:08:15, 07:11:38, 07:32:00) | bajista | 05:00Z → 05:47Z → 05:47Z | -1.00; -1.22; -0.06; -1.00 (stops) | sin orden |
| 2026-08-18 | 11-15 | no | 3 ventas (09:36:18, 09:40:20, 12:10:07) | bajista | 09:00Z → 09:31Z → 09:31Z | -1.00; -0.33; -1.00 (stops) | sin orden |
| 2026-08-24 | 07-11 | no | 8 compras (05:25:00 a 08:19:05) | alcista | 05:00Z → 05:22Z → 05:22Z | -1.00; -1.00; -1.08; -1.17; +0.00; +0.00; -1.10; -1.00 (stops) | sin orden |
| 2026-08-28 | 07-11 | no | 1 venta (06:05:52) | bajista | 05:00Z → 05:58Z → 05:58Z | -1.00 (stop) | sin orden |
| 2026-08-31 | 11-15 | no | 1 compra (12:41:16) | alcista | 09:00Z → 12:39Z → 12:39Z | -0.33 (stop) | sin orden |

En las 34 sesiones el camino es el mismo: `sesgo` al abrir (RN-003), `liquidez_tomada` (RN-004) y
`orden_dimensionada` (RN-011) en el mismo cierre, y la orden stop en el punto. Dos sesiones de abril
(06 y 07, 11-15) tienen todas sus llenadas en una hora de ticks perdida (posible M). La R de las 77
llenadas de P6: 4 objetivos y 1 cierre manual positivo, 19 a cero exacto (break even) y 53 negativas
(contadas en «## Todas las llenadas» de `entradas-antes-alternancia.txt`, filas P6; *corregido tras
el revisor, a1: la primera redacción decía 5, 24 y 47*).

**Marca E (respuesta a la PARADA 3, punto 1 a): 3 de las 34 filas** (sesiones) llevan «E: llenada
con la vela que la colocó (ADR-0051 §2)», en 4 de sus 77 llenadas: 2026-04-06 11-15 (las dos),
2026-04-07 07-11 (la de 05:00:00) y 2026-04-07 11-15 (la de 10:26:00). No se eligen para la sesión
6. `lista-s14.txt` la lleva: `lista_s14.py` la calcula de la salida de la corrida 2 (la llenada con
`respaldo_m1` cuya orden se colocó 1 ms antes, el cierre de la misma vela) y su cabecera da «10; de
ellas en P6: 4, en 3 sesiones». **Fuera también, por la respuesta a la PARADA 2 (punto 2)**: las
sesiones «posible M» y las del 1 de abril y el 1 de julio (2026-04-01 07-11 está en esta lista).

## 5. El encargo frente a lo hecho

### 5.1 Punto por punto

| # | El encargo pide | Estado | Evidencia |
|---|---|---|---|
| 1 | Rama desde main 88f97f7 con la base entera comprobada, abrir-rama, contrato R4, artefacto, encargo copiado tal cual | Hecho | cabecera; f043554 |
| 2 | Fable 5.1 / esfuerzo alto; `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1` | Hecho | `/model` al empezar; `echo` = 1 (cabecera) |
| 3 | Nada de src/, tests/, knowledge/, Makefile ni .claude/; criterio_fidelidad.yaml, ambigüedades, ADR-0083, informes cerrados y líneas base sin tocar | Hecho | §8: `git diff main --stat -- src/ tests/ knowledge/ Makefile .claude/` vacío; `rutas_protegidas` del contrato |
| 4 | Next Action y hoja de ruta sin tocar en la rama; PROJECT_STATE solo lo de abrir-rama (22.924 bytes verificados) | Hecho | §0 cabecera (`wc -c` 22924 en main); las líneas, en §6 |
| 5 | Antes de leer casos dev, `casos_reservados` por recuento, declarado el mismo día | Hecho | §0.c, §0.m; fila del 2026-10-27 de HOLDOUT-EXPOSICIONES |
| 6 | Nada de mayo ni de meses reservados; el calentamiento declarado; nada anterior al día dev en ningún texto | Hecho | la fila; `grep -c "antes del dia"` 0; ninguna H4 ni pivote impreso; las fechas de los textos son todas de días dev (enero 2-30, abril, julio 1-17, agosto) |
| 7 | Ninguna cifra fija ni cambia un valor, ni los DEFAULT_AMBIGUOUS, ni el umbral | Hecho | `git diff main -- knowledge/` vacío; ADR-0070 §4 |
| 8 | Las 5 decisiones de §0.0 aplicadas | Hecho | §2.1 (1 y 2: «no»), §2.6 (4), §3 (5 con la regla de la PARADA) |
| 9 | Solo los tres comandos del arnés y el guion aprobado; ningún visor | Hecho | §2 y §3: los comandos literales; `motor visor` no se ejecutó (desviación del runbook, §5.2) |
| 10 | Fase 0 a) a j) con fichero:línea y PARADA | Hecho | §0.a-§0.m; respuesta del consultor copiada |
| 11 | Fase 1: fila y README en su commit; guiones con tests de humo en los dos sentidos y su salida pegada; ruff/mypy antes de cada make check | Hecho | a713e23; fec05fc y 74ab3cb; §1.2 (10 passed; mypy: solo los dos errores heredados) |
| 12 | Fase 2: las tres corridas sin `--meses`, TIEMPO y MEMORIA copiados, nombres finales, repetición con diff y borrado, el diff de la línea base a fichero | Hecho | §2, §2.4, §2.5 |
| 13 | Informe: por corrida y mes; veredicto literal; la cuenta (tramo, día y regla); peticiones y freno; tramo no continuo | Hecho | §2.1, §2.2 |
| 14 | Lo de i): RN-020, ADR-0086, RN-036, RN-037, la lista DEFAULT_AMBIGUOUS | Hecho | §2.3, §0.i |
| 15 | El diff resumido por sección con el fichero en anexos | Hecho | §2.5; `diff-linea-base.txt` |
| 16 | Patrones de las dos corridas por mes con la copia arreglada; PUNTO-USADO como contexto con los cambios del motor; posible M | Hecho | §2.6; `patrones-diaria.txt`, `patrones-arrastrada.txt` |
| 17 | Embudo por mes y rechazos por motivo | Hecho | §2.7 |
| 18 | Lista «Entradas antes de la alternancia», por día y sesión, con las dos columnas, patrón, R y pareja; sin conclusiones | Hecho | §3; `entradas-antes-alternancia.txt` |
| 19 | Lista «Para S-14» con primer hecho, R, si la cuenta arrastrada llega, y vídeo | Hecho | §4; `lista-s14.txt` |
| 20 | Encargo frente a lo hecho, desviaciones, comandos, exposiciones | Hecho | §5 |
| 21 | PARADA 2 con todo commiteado | Hecho | el último commit de la rama antes de esta PARADA |
| 22 | Las líneas del cierre, medidas; PROJECT_STATE < 23.000 con ellas | Hecho | §6 (22.872 bytes sobre una copia, con las de la PARADA 3) |
| 23 | Hallazgos para ERRORES-RECURRENTES | Hecho | §7 (siete; el 1 y el 7, del consultor) |
| 24 | Revisor (opus) con los cuatro alcances y el quinto de las PARADAS 2 y 3, informe pegado | Hecho | §10 |
| 25 | Respuesta a la PARADA 2 (§2.8, listas, NOTA de ADR-0070, líneas, revisor) | Hecho | su tabla «La respuesta aplicada, punto por punto» |
| 26 | Respuesta a la PARADA 3 (la marca E, la frase de ADR-0070, las líneas del cierre, el hallazgo) | Hecho salvo la letra (PARADA 4) | su tabla «La respuesta aplicada, punto por punto» |

*Fila 22 corregida tras el revisor (b2): con las líneas de la respuesta a la PARADA 3 PROJECT_STATE
mide 22.872 bytes (simulación de §6), no 22.640, que era la medida de la PARADA 2.*

### 5.2 Desviaciones declaradas

1. **El visor no se abre.** `docs/runbooks/ACTIVAR-A35-A44.md` §5 manda `uv run botsito motor visor
   --caso <caso dev>` después del `diff`; en esta rama no se ejecuta ningún `motor visor` (encargo,
   «Autorización expresa»; respuesta a la PARADA, punto 4; y la respuesta a la PARADA 2, punto 1: «el
   visor NO se abre en esta rama», que sustituye con una medida sobre las salidas y los ticks, §2.8).
   La NOTA de §5 del runbook lo declara (commit propio, contrato ampliado solo a él; *su última frase
   corregida tras el revisor, b1*).
2. **La línea base vigente pasa a ser `anexos/RECORRIDA-CONSTRUCCION/cuenta-arrastrada.txt`**, sin
   copia; `CABLEADO-SIMULADOR-LINEA-BASE.txt` no se toca (punto 4). Los documentos que la nombran
   como vigente (§0.g) siguen diciéndolo: solo el runbook gana la NOTA; lo demás son informes cerrados
   (no se editan) y `PROJECT_STATE.md` (la V sale en el cierre).
3. **Dos guiones auxiliares más que los dos del encargo**: `comparar_rn003.py` (el rn003 por sesión
   frente a la línea base, porque «RN-003 al abrir» no se parte por mes, auditor #45) y
   `lista_s14.py` (la lista de §4 cruzando los anexos). Solo leen los ficheros commiteados de
   `docs/validation/` y no corren nada; con `ruff format`, `ruff check` y `mypy` (sin errores propios).
   Sin test de humo propio: no deciden nada, y sus salidas (`rn003-abril-agosto.txt`, `lista-s14.txt`)
   se comprueban contra las salidas del arnés a mano (tres filas, el revisor).
4. **La copia de `patrones.py` corta el rótulo solo si la línea empieza por `[DIAGNOSTICO`**, como
   dice el encargo; `comun_visor.py` corta si empieza por `[` (auditor, #37). Sobre estas salidas da
   lo mismo.
5. **El guion de f) reproduce la corrida 2** (cuenta diaria), no la 1, como el encargo previó; la
   comprobación una a una salió `iguales (291)`.
6. **Herencia H5 del auditor**: las cifras de referencia de `ACTIVAR-A35-A44.md` §5.1
   (`liquidez_tomada` 98 y 97 de 104 en R3.1; RN-020 0 de 104 con `sin_tope`) se comparan en §2.3:
   hoy 96 de 104 y 0 de 104 (con el tope del trader evaluado).

### 5.3 Comandos ejecutados (literales, en orden)

Apertura y fase 0: los de la cabecera (git, `gh api`), `uv run botsito state check`,
`uv run python scripts/contrato_rama.py`, `make check > make-check.log 2>&1` (×5 hasta la PARADA 2:
apertura, fase 0, fila+README, guiones, ampliación del guion), los dos guiones de medida de la
carpeta de trabajo (`medir_fase0.py`, `medir_patrones_rotulo.py`, solo lectura). Fase 1:
`uv run ruff format`, `uv run ruff check`, `uv run mypy` sobre los ficheros de anexos,
`uv run pytest docs/validation/anexos/RECORRIDA-CONSTRUCCION/test_humo.py -q`,
`uv run python docs/validation/anexos/RECORRIDA-CONSTRUCCION/patrones.py <la diaria de PUNTO-USADO y su copia sin rótulo>`.
Fase 2, cada uno solo y en segundo plano:
1. `uv run botsito motor arnes --simular --salida docs/validation/anexos/RECORRIDA-CONSTRUCCION/cuenta-arrastrada.txt`
2. `uv run botsito motor arnes --simular --diagnostico-cuenta-diaria --salida docs/validation/anexos/RECORRIDA-CONSTRUCCION/diaria.txt`
3. `uv run botsito motor arnes --simular --salida <carpeta de trabajo>/cuenta-arrastrada.txt`; `diff <commiteada> <copia>`; `rm <copia>`
4. `diff docs/validation/CABLEADO-SIMULADOR-LINEA-BASE.txt docs/validation/anexos/RECORRIDA-CONSTRUCCION/cuenta-arrastrada.txt > docs/validation/anexos/RECORRIDA-CONSTRUCCION/diff-linea-base.txt` (exit 1; la guardia no negó la redirección)
5. `uv run python docs/validation/anexos/RECORRIDA-CONSTRUCCION/patrones.py "<diaria>" --filas > …/patrones-diaria.txt` y lo mismo con `cuenta-arrastrada.txt` → `patrones-arrastrada.txt`
6. `uv run python docs/validation/anexos/RECORRIDA-CONSTRUCCION/entradas_antes_alternancia.py --diaria "docs/validation/anexos/RECORRIDA-CONSTRUCCION/diaria.DIAGNOSTICO.cuenta=diaria.txt" --salida docs/validation/anexos/RECORRIDA-CONSTRUCCION/entradas-antes-alternancia.txt` (una vez, después de las tres corridas)
7. `uv run python docs/validation/anexos/RECORRIDA-CONSTRUCCION/comparar_rn003.py docs/validation/CABLEADO-SIMULADOR-LINEA-BASE.txt docs/validation/anexos/RECORRIDA-CONSTRUCCION/cuenta-arrastrada.txt > …/rn003-abril-agosto.txt`
8. `uv run python docs/validation/anexos/RECORRIDA-CONSTRUCCION/lista_s14.py docs/validation/anexos/RECORRIDA-CONSTRUCCION > …/lista-s14.txt`

Tras la PARADA 2 (*añadido tras el revisor, b2*):
9. `uv run python docs/validation/anexos/RECORRIDA-CONSTRUCCION/costes_y_sesiones.py > docs/validation/anexos/RECORRIDA-CONSTRUCCION/costes-y-sesiones.txt` (dos veces: la primera con la salida en la carpeta de trabajo, para revisarla; la commiteada es la segunda), con `ruff format`, `ruff check` y `mypy` antes.
10. Tras la PARADA 3: `lista_s14.py` otra vez (con la marca E), y `uv run python docs/validation/anexos/RECORRIDA-CONSTRUCCION/simular_cierre.py . <letra>` con H, E, R y Z (solo lee el repo; la copia de PROJECT_STATE, en una carpeta temporal).
11. Los guiones de solo lectura de la carpeta de trabajo de la sesión (`resumen_salida.py`, `tabla_entradas.py`, `tabla_costes.py`, `medir_ps.py`, `r_p6.py` y `a_lf.py`, que pasa a LF las salidas escritas por redirección), sobre los anexos.
12. `make check > make-check.log 2>&1` antes de cada commit: 11 en la rama hasta el informe del revisor, todos con `exit=0`, `2970 passed` y `SELLO`.

Lo que la guardia negó en la rama, sin rodearla (todo reescrito en llamadas sueltas, como ella pide):
`$'\r'` en un `grep` (se usó `file`), `date` detrás de un `tail`, `uv run --project` desde la carpeta
de trabajo (se corrió ruff desde la raíz), `cmp` detrás de un `cp` y `cmp` sobre un `.py` (se usó
`diff`). Ninguna negativa tocó material protegido ni un comando del arnés. Después de la PARADA 2,
una más: un comando compuesto con un `grep -r` (§2.8, «Una negativa de la guardia»), rehecho con la
herramienta Grep sobre la ruta literal; y la guardia negó `git status --short` seguido de
`python scripts/contrato_rama.py` en el mismo comando (dos llamadas).

### 5.4 Exposiciones

Las de las dos filas del 2026-10-27 de `docs/validation/HOLDOUT-EXPOSICIONES.md` de esta rama. La
primera, declarada antes de correr: las tres corridas y el guion de f) leyeron para calentar el M1
entero de marzo (mes reservado entero) y de junio (11 días reservados); cada `make check` de la
rama (once hasta el revisor, y los que sigan) lee el M1 de marzo por `test_preparar_a35.py` y
`test_visor.py`. La segunda (*añadida tras el revisor, a2*): `costes_y_sesiones.py` (§2.8) leyó los
TICKS de días dev de construcción, en ventanas de un minuto, después de la PARADA 2; material de
desarrollo, sin ningún día reservado (los manifiestos de ticks solo tienen días dev, §0.b), y sin
calentamiento.

La regla de «nada anterior al día dev» no alcanza la línea «calendario: cubre … UTC, N cierres» de
la salida del arnés: es la cobertura del calendario de cierres del perfil (ADR-0068), no una vela,
un precio, un instante de mercado ni material del trader (respuesta del consultor a la PARADA 4,
punto 2). Ninguna
etiqueta, ninguna operación del trader ni cifra del bot de un día reservado se leyó ni se imprimió;
ningún texto de la rama lleva una fecha, una vela, una H4, un pivote ni un precio anteriores al día
dev al que pertenece. Nada de mayo, marzo (salvo las velas del calentamiento), febrero, septiembre
ni diciembre; ningún libro, imagen, fotograma ni transcripción.

## 6. Las líneas del cierre (preparadas, medidas; no aplicadas en la rama)

- **Next Action, V sale** (R4.1 HECHA) y entra al final de `docs/state/HISTORIA.md` con su texto
  literal bajo `# Next Action HECHA · V · sale de PROJECT_STATE.md en trabajo/recorrida-construccion (<fecha del cierre>)`
  (RITUAL.md, punto 3). El texto literal de hoy (`PROJECT_STATE.md:52`):
  `V. Activar la sesión 5 (R4.1). HECHAS spec y motor (\`trabajo/activar-sesion-05\` y \`trabajo/activar-sesion-05-motor\`, este tag: ADR-0084 a 0086, RN-037; A-35 y A-50 con lectura del consultor, ABIERTAS). QUEDA la re-corrida del arnés con \`--simular\` sobre toda la construcción (ADR-0070 §3; diff contra CABLEADO-SIMULADOR-LINEA-BASE.txt, ACTIVAR-A35-A44.md §5.1); después la sesión 6 (R4.2).`
- **F** pasa a: `F. La rama corta de la cuarentena por condición (Technical Debt, PRIORITARIA) antes de ingerir la sesión 6; la preparación de la sesión 6 (R4.2); R6a en los huecos.`
  Contra `tests/unit/test_hoja_de_ruta.py`: `DEPENDENCIA` casa «antes de ingerir la sesión 6» y
  `LETRA_SUELTA` no encuentra ninguna letra suelta en ese tramo (`R4.2` y `R6a` llevan dígito
  detrás; «PRIORITARIA» es palabra), y la hoja gana la entrada G.5 de abajo para que F no nombre
  nada que la hoja no tenga (respuesta, punto 6).
- **`Current Branch`**: `main`. **`Current Feature`**: `Ninguna rama abierta.
  trabajo/recorrida-construccion cerrada en main el <fecha> (stable/F38g-recorrida-construccion):
  la corrida que cuenta por ADR-0070 §3 dio «no» (cobertura 3,5 %, precisión 13,2 %); se sigue
  construyendo (RECORRIDA-CONSTRUCCION.md).`
- **`PROJECT_STATE.md` con esas líneas aplicadas** (guion `medir_ps.py` de la carpeta de trabajo,
  sobre una copia fuera del repo: sale V con su línea en blanco, cambia F, `Current Branch` y
  `Current Feature`): **22.640 bytes** (hoy en la rama 23.098; en main 22.924; el tope del test,
  25.000; la orden del consultor para este cierre, 23.000). *Con las líneas de la respuesta a la
  PARADA 3 (abajo), 22.872.* `Completed Features` y `Change Log` no
  cambian en el cierre (`docs/state/README.md`); el recuento de tests tampoco (ningún test nuevo
  dentro de `tests/`).
- **Hoja de ruta, R4.1**: `**Estado:** HECHA (\`trabajo/activar-sesion-05\`, \`stable/F38e-activar-sesion-05\`; \`trabajo/activar-sesion-05-motor\`, \`stable/F38f-activar-sesion-05-motor\`; \`trabajo/recorrida-construccion\`, el tag de su cierre: la corrida que cuenta por ADR-0070 §3 dio «no» -cobertura 3,5 %, precisión 13,2 %- y las dos listas para la sesión 6 están en RECORRIDA-CONSTRUCCION.md §3 y §4).`
  Y `NA:V` sale de sus Refs (quedan los `ID:`).
- **Hoja de ruta, R4.2**: `NA:V` sale de sus Refs; «Qué es» gana «S-14 con las 34 sesiones de P6 de
  la re-corrida (RECORRIDA-CONSTRUCCION.md §4; 77 llenadas) y el dibujo 3 de S-15 con las 259
  entradas llenadas con menos de dos zonas de control (§3; 149 con cero, 110 con una)» en lugar de
  «S-14 con los días de construcción que dé la re-corrida»; «Depende de» pasa a «nada (la re-corrida
  está hecha, R4.1)».
- **Hoja de ruta, R5.2, «Depende de»** (respuesta, punto 6): `la corrida que cuenta (R4.1; ADR-0070
  §3) con un "sí", y el ADR propio de la rama de medida (ADR-0070 §6)`.
- **Hoja de ruta, entrada nueva en «Carril: guardias y deuda»** (respuesta, punto 6), con la forma
  de G.4:
  ```
  ### G.5 · La cuarentena por condición
  - **Refs:** —
  - **Qué es:** la línea PRIORITARIA de Technical Debt: diciembre cuenta como libre en `meses_libres`
    con NA:I sin decidir, y la fecha numérica seguida de coma no se tapa (SESION-05-EXTRACCION.md
    §2.7 y §11, a4).
  - **Depende de:** nada.
  - **Quién:** la sesión, con el encargo del consultor.
  - **Hecho cuando:** los dos casos tienen su test que rompe en main y pasa en la rama, antes de
    ingerir la sesión 6.
  ```
  `Refs: —` no lleva ninguna `NA:`/`HER:`/`ID:`, así que `test_hoja_de_ruta` (problemas_b) no
  encuentra nada que comprobar en ella; «NA:I» dentro de «Qué es» es una referencia a una letra
  viva (I sigue en la Next Action). Se comprueba en el cierre con el test en memoria, como en
  `trabajo/entrada-enero`.
- **ADR-0070 §3, NOTA fechada** (el cuerpo no se toca; contrato ampliado al ADR solo para eso, en
  un commit propio, si la PARADA 2 lo aprueba):
  `> **NOTA del <fecha> (\`trabajo/recorrida-construccion\`, no reescribe el cuerpo).** La primera corrida que cuenta por este punto (sin ningún \`--diagnostico-*\`, con \`--simular\`, sobre toda la construcción: 76 días dev, 198 operaciones del trader) dio \`habilita medir el conjunto de medida (2026-05) (ADR-0070): no (cobertura 3.5 % por debajo de 70.0 %; precision 13.2 % por debajo de 60.0 %)\` (\`docs/validation/anexos/RECORRIDA-CONSTRUCCION/cuenta-arrastrada.txt\`, la línea base vigente desde esa rama). Por el punto 4, se sigue construyendo y mayo no se toca.`
- **La línea base** (§0.g, punto 4 de la respuesta): la NOTA al principio de `ACTIVAR-A35-A44.md` §5
  (commit propio, en esta rama, después de la fase 2): la línea base vigente es
  `docs/validation/anexos/RECORRIDA-CONSTRUCCION/cuenta-arrastrada.txt`, qué es comparable con la
  anterior (§2.5), y que `motor visor --caso` no se abrió en la rama (desviación). No hay más
  documento ejecutable que la nombre (§0.g).
- **Technical Debt**: ninguna línea nueva; la deuda de `arnes.dias_de_mercado` (lee marzo y junio
  para calentar) sigue como está, con una fila más en HOLDOUT-EXPOSICIONES que la cita. Y **sale**
  (respuesta a la PARADA 3, punto 1 c) la línea «- El bróker simulado cotiza con el respaldo M1 la
  orden del primer cierre de la ventana: los ticks empiezan en ventana_inicio y la orden lleva 1 ms
  antes (VISOR-CONSTRUCCION.md §4.3).», porque pasa a la Next Action.
- **Next Action, entrada nueva** (respuesta a la PARADA 3, punto 1 c), tras la N, con la letra que
  decida el consultor en la PARADA 4 (no queda ninguna libre: abajo):
  `<letra>. El bróker simulado llena con el respaldo M1 una orden en la vela cuyo cierre la colocó, en todo minuto sin ticks (el borde de la ventana y las horas perdidas), contra ADR-0051 §2 (RECORRIDA-CONSTRUCCION.md §2.8; antes, VISOR-CONSTRUCCION.md §4.3). Rama propia con su test que rompe en main, una NOTA en ADR-0051 §5 y las corridas repetidas; antes de la próxima corrida del arnés que cuente (ADR-0070 §3).`
  Contra `test_hoja_de_ruta` (c): `DEPENDENCIA` casa «antes de la próxima corrida del arnés que
  cuente (ADR-0070 §3)» y `LETRA_SUELTA` no encuentra en ese tramo ninguna letra suelta («ADR-0070»
  lleva guion); la simulación lo confirma (`c: []`).
- **Hoja de ruta, entrada nueva en R3** (tras R3.4):
  ```
  ### R3.5 · El respaldo M1 no llena con la vela que colocó la orden
  - **Refs:** NA:<letra> · ID:ADR-0051
  - **Qué es:** en todo minuto sin ticks (el borde de la ventana y las horas perdidas) el bróker
    simulado llena una orden con la vela M1 cuyo cierre la colocó, con precios anteriores a la
    orden, contra ADR-0051 §2 (RECORRIDA-CONSTRUCCION.md §2.8: 2 llenadas en la corrida que
    cuenta, 10 en la diaria); se corrige con su test, una NOTA en ADR-0051 §5 y las corridas
    repetidas.
  - **Depende de:** nada.
  - **Quién:** la sesión, con el encargo del consultor.
  - **Hecho cuando:** un test que llena con la vela que colocó la orden rompe en `main` y pasa en
    la rama, y las dos corridas de `trabajo/recorrida-construccion` están repetidas en la suya.
  ```
- **R5.2, «Depende de»** (sustituye a la línea de arriba): `la corrida que cuenta (R4.1; ADR-0070
  §3) con un "sí", y el ADR propio de la rama de medida (ADR-0070 §6); y NA:<letra>, el respaldo M1
  corregido (R3.5).`
- **R4.2, «Qué es»**: la línea de S-14 de arriba gana «, sin las marcadas E» (las 10 de §3.2 y las 4
  de §4).
- **Todas las líneas, medidas.** `anexos/RECORRIDA-CONSTRUCCION/simular_cierre.py <raíz> <letra>`
  las aplica en memoria (V a HISTORIA, F, la letra nueva, la deuda que sale, `Current Branch` y
  `Current Feature`; R4.1, R4.2, R5.2, R3.5 y G.5 en la hoja), corre las funciones a, b y c de
  `test_hoja_de_ruta.py` y los cuatro tests de `test_project_state.py` sobre una copia fuera del
  repo: con H, R o Z, `a: []`, `b: []`, `c: []` y **PROJECT_STATE en 22.872 bytes** (por debajo de
  23.000; antes de la respuesta a la PARADA 3, 22.640). Con E, que la hoja ya nombra en una entrada
  HECHA (R3.3), (b) rompe: «NA:E esta HECHA y la letra sigue viva».

## 7. Hallazgos para ERRORES-RECURRENTES (la fila de la rama, en el cierre)

1. **(Del consultor)** El encargo pedía clasificar con `patrones.py` una salida sin rótulo, y su
   lectura por «] » daba un P1 falso sin error; lo vio el auditor del consultor. Lección: un guion de
   anexos escrito para salidas rotuladas se prueba sobre una salida sin rótulo antes de reutilizarlo.
   Señal: «0 sesiones con rn003» en la cabecera (§0.e).
2. **Las categorías de una lista se comprueban sobre el caso que la motiva antes de fijarlas.** Las
   tres del encargo para «dónde estaba la orden» se solapaban en S-10, el caso que la lista quería
   capturar (auditor #22); la PARADA las separó en dos columnas. Señal: el ejemplo nombrado cae en
   dos categorías a la vez.
3. **Un guion copiado de otro anexo se copia con lo que importa.** `patrones.py` importa
   `horas_perdidas.py` de su directorio; copiado solo, falla al importar (auditor H2). Señal: un
   `sys.path.insert(0, parent)` seguido de un import local.
4. **«Un agregado de toda la salida» no se compara por mes en un diff.** «RN-003 al abrir» suma
   todas las sesiones; para comparar abril y agosto con la línea base hizo falta leer las líneas
   «Por sesion» una a una (§2.5). Señal: una sección del informe sin desglose por mes citada como
   «comparable por mes».
5. **La cuenta arrastrada puede quedar «viva» y muda a la vez.** El veredicto dice EN_CURSO y el
   bot no coloca nada desde el 2026-01-20 por RN-032 (el límite total de la firma no arrastra):
   «la cuenta llega a la sesión» no es lo mismo que «el bot pudo operar en ella» (§2.2, §4). Señal:
   `estado: EN_CURSO` con la curva de equity plana y ninguna `llenada` en «### Ordenes» desde un día
   dado, con RN-032 entre las disparadas de cada sesión siguiente (*el bloqueo de RN-015 solo no
   basta: aparece también antes, por otras reglas; revisor, a4*).
6. **La guardia niega lo que encadena un lector con otro comando**: `cmp` tras `cp`, `date` tras
   `tail`, `$'\r'`, `uv run --project`. Una llamada por comando, desde la raíz (§5.3).
7. **(Del consultor, respuesta a la PARADA 3, punto 1 d)** La deuda de VISOR-CONSTRUCCION describió el
   caso en el que se vio («la orden del primer cierre de la ventana») y no la condición («toda orden
   evaluada con el respaldo M1 en la vela que la colocó»), y la condición alcanzó también una hora sin
   ticks fuera del borde (8 de las 10 llenadas de la corrida 2, §2.8 c). Lección: una deuda se escribe
   nombrando la condición, no el caso.

## 8. Lo que NO cambia, medido

`git diff main --stat -- src/ tests/ knowledge/ Makefile .claude/ config/ docs/adr/ docs/plan/
docs/runbooks/` (hasta la PARADA 2, antes del commit de la NOTA del runbook): vacío. Lo que la rama
añade o cambia: `contrato.yaml`, `PROJECT_STATE.md` (la apertura), `docs/state/HISTORIA.md` (el
Archivo 49), `docs/encargos/trabajo-recorrida-construccion.md`, este informe,
`docs/validation/HOLDOUT-EXPOSICIONES.md` (una fila) y `docs/validation/anexos/RECORRIDA-CONSTRUCCION/`
(README, 6 guiones, 1 test, 8 salidas). Ningún parámetro, regla, ambigüedad ni ADR cambia; A-35 y
A-44 siguen ABIERTAS y bloqueantes; ADR-0083 sigue PROVISIONAL en D1; `criterio_fidelidad.yaml` y
`CABLEADO-SIMULADOR-LINEA-BASE.txt` intactos. La CI de Linux: la rama no toca `.claude/`, hooks,
rutas de plataforma ni código, así que no hace falta `fix/`.

## 9. La NOTA del runbook (respuesta a la PARADA, punto 4; commit propio tras la fase 2)

`docs/runbooks/ACTIVAR-A35-A44.md` gana una NOTA al principio de §5 (el cuerpo no se toca): la
medida de §5 se hizo, la línea base vigente es `anexos/RECORRIDA-CONSTRUCCION/cuenta-arrastrada.txt`
sin copia, `CABLEADO-SIMULADOR-LINEA-BASE.txt` no se toca, qué es comparable (§2.5), y la desviación
del visor. El contrato se amplía en el mismo commit solo a ese fichero (`rutas_permitidas`, con su
comentario); `docs/runbooks/` sale de `rutas_protegidas` como carpeta y quedan protegidos por nombre
los runbooks que una rama así podría tocar por costumbre (ERRORES-RECURRENTES, RITUAL, VISOR-DIAS,
ARNES-MOTOR); los demás siguen fuera de `rutas_permitidas`, que es lo que el contrato comprueba.

## Respuesta del consultor a la PARADA 2 (2026-10-27)

Copiada tal cual:

> Modelo: Fable 5.1 · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA 2 de trabajo/recorrida-construccion (2026-10-27). Cópiala tal cual al final del encargo y del informe, en «Respuesta del consultor a la PARADA 2», con su fecha, y aplícala punto por punto (skill fase-cero).
>
> 1. Ningún patrón nuevo, y el visor NO se abre en esta rama. En su lugar, una medida sobre las salidas commiteadas y los ticks de los días dev (nada anterior al día dev, nada del calentamiento), en un §2.8 nuevo del informe:
>    a) Toda llenada de la corrida 2 cuyo R se aparte más de 0,25 del que da su motivo sin costes (stop −1; stop en break even 0; objetivo +3,75, que es 3 veces la distancia del 0 al 1 sobre el riesgo del 0 al 0,8): día, sesión, id, R y la causa leída en la salida y en los ticks (comisión sobre un stop pequeño, deslizamiento, hueco o spread a la apertura de la ventana, respaldo M1 en una hora perdida, el lote limitado por volumen o margen, u otra). Entre ellas, la de −2,00 R del 2026-04-07 07-11, llenada a las 05:00:00, y la de +2,18 R por objetivo del 2026-01-16 11-15.
>    b) Toda sesión de la corrida 2 con más de 4 llenadas (entre ellas, 2026-08-24 07-11, con 8): cuántos escenarios hubo y de qué toma sale cada uno, cuántas llenadas por escenario y por punto, y por qué no detuvieron antes RN-016 (cartuchos), RN-036 (racha) ni RN-020, según la salida.
>    c) Cada caso se marca «regla aplicada como está escrita» o «no» con su evidencia. Si alguno es «no» (una regla que el motor no aplica como dice la spec), PARADA 3 antes del revisor. Si todos son «sí», sigue sin parar.
>    Motivo: son las diferencias más grandes que deja la corrida, y antes de llevarlas a la sesión 6 hay que saber si son del trader o nuestras. Leer salidas y ticks de días dev no necesita el visor.
> 2. La hoja de la sesión 6: las dos listas (§3 y §4) se quedan como están, y los días los elijo yo en la rama de preparación. Desde ya quedan fuera las sesiones marcadas «posible M» y las del 1 de abril y el 1 de julio (su contexto de H4 y M15 puede venir del día anterior, que es reservado o fuera de construcción).
> 3. Apruebo la NOTA de ADR-0070 §3 tal como está en §6, en un commit propio, con el contrato ampliado solo a ese ADR, y con una frase más al final: «Con la cuenta arrastrada, el bot deja de colocar desde el 2026-01-20 por RN-032 (la pérdida total más el riesgo de la siguiente operación llega al límite de la firma), con la cuenta EN_CURSO; RECORRIDA-CONSTRUCCION.md §2.2.»
> 4. Las líneas del cierre de §6 y los hallazgos de §7 quedan aprobados tal cual, con la NOTA del punto 3. Y si el punto 1 cambia algún recuento de §6, se vuelve a medir PROJECT_STATE con wc -c sobre la copia.
> 5. Después, el revisor (opus) con los cuatro alcances del encargo y uno más: (5) que §2.8 dice lo que dicen las salidas, comprobado a mano en tres casos de a) y en la sesión 2026-08-24 07-11 de b), y que nada de §2.8 imprime algo anterior al día dev. Su informe, pegado al final; arregla lo que bloquee o importe, o dime por qué no.
>
> make check en verde antes de cada commit, con ruff format, ruff check y mypy antes sobre lo tocado. Si la guardia o el clasificador niegan algo, PARADA con el comando exacto y lo lanzo yo con «!».
>
> Rama lista para revisión, NO cerrada.

### La respuesta aplicada, punto por punto

| # | Punto | Estado | Evidencia |
|---|---|---|---|
| 1 | §2.8 sobre salidas y ticks de días dev, sin visor ni calentamiento | Hecho | §2.8; `costes_y_sesiones.py` y `costes-y-sesiones.txt`; ningún `motor visor` |
| 1 a | Llenadas con \|R − esperado\| > 0,25, con su causa; los dos casos nombrados | Hecho | §2.8 a): 25 casos, R comprobado en los 25 |
| 1 b | Sesiones con más de 4 llenadas | Hecho, salvo la toma de cada escenario | §2.8 b): 9 sesiones; la toma no está en ninguna salida (Lo que no pude medir) |
| 1 c | «Sí» o «no» por caso; PARADA 3 si hay un «no» | **Dos «NO»: PARADA 3** | §2.8 c); abajo |
| 2 | Las listas se quedan; fuera «posible M» y el 1 de abril y el 1 de julio | Hecho (anotado) | §3 y §4 no cambian; la exclusión, para la rama de preparación |
| 3 | NOTA de ADR-0070 §3, commit propio, contrato ampliado solo al ADR, con la frase de RN-032 | Hecho | su commit (tras el de §2.8) |
| 4 | Líneas del cierre y hallazgos aprobados; volver a medir si §2.8 cambia un recuento de §6 | Hecho | §2.8 no cambia ningún recuento de §6 (los de R4.2 son de §3 y §4): PROJECT_STATE sigue en 22.640 bytes con las líneas |
| 5 | El revisor con el alcance (5) | Pendiente de la PARADA 3 | — |

### Lo que no pude medir (§2.8)

- **De qué toma sale cada escenario** de las nueve sesiones de b). Las salidas commiteadas dan el
  número de escenario de cada llenada (la memoria del productor, `escenarios`, leída por el guion de
  f) en su única corrida) pero no su toma: ni el instante, ni el pivote de M15 tomado. Obtenerla pide
  correr el motor sobre esos días (no autorizado: «Ningún otro comando del arnés ni del visor sin
  preguntármelo») o reconstruir la liquidez de M15 con las velas, que puede venir del calentamiento
  (excluido por el punto 1). Si hace falta, un comando concreto en la respuesta a la PARADA 3.
- El efecto de corregir el respaldo sobre el camino de la cuenta de la corrida 1 (si RN-032 llegaría
  el mismo día): exige otra corrida.

### Una negativa de la guardia en esta fase (sin rodearla)

`grep -n "deslizamiento\|spread" knowledge/cases/kit/llenado.yaml 2>/dev/null | head; ls knowledge/cases/kit/ | head; grep -rn "FICHERO_LLENADO =" src/botsito/engine/`
→ «GUARDIA … bloquea: leer el contenido de .» (un comando compuesto mío, con un `grep -r` y un
fichero que no existe). Se rehízo con la herramienta Grep sobre la ruta literal `src/botsito/engine`
y Read de `knowledge/simulador/llenado.yaml`. No tocó material protegido.

## PARADA 3 · El respaldo M1 evalúa la orden contra la vela que la colocó (2026-10-27)

Lo medido en §2.8 c): **en dos de los 25 casos de a) el motor no aplica el modelo de llenado como
dice ADR-0051**, y la causa no es de esos dos casos sino del respaldo M1 del bróker simulado:

- **Qué hace el código.** `engine/llenado.py`, `primer_llenado_stop` (:187-223; y lo mismo
  `primer_llenado_limite` y `primera_salida`): para cada minuto desde el de colocación
  (`_minutos(desde_ms, …)`, `desde_ms` = el cierre de la M1 que decidió menos 1 ms), si el minuto no
  tiene ticks usa su vela M1 cuando `fin > desde_ms`. La vela del minuto de colocación termina 1 ms
  después de `desde_ms`, así que **cuenta, aunque todos sus precios son anteriores a la orden**. Con
  ticks, en cambio, todo tick `<= desde_ms` se salta (:194-195).
- **Qué dice el ADR.** ADR-0051 §2: «Una orden colocada en un tick no se evalúa contra ese mismo
  tick: contra el siguiente (sin mirar al futuro: el motor decide con lo que ya cerró)»; el módulo lo
  dice de los ticks (`llenado.py:10-12`; el respaldo, `:13-15`, no lo dice). §5 dice que un minuto sin ticks se evalúa con su vela M1,
  sin excluir la de la decisión. §8: «el respaldo M1 solo sirve para depurar … una hora perdida sigue
  cayendo al respaldo».
- **Dónde muerde.** En todo minuto sin ticks en que se coloca una orden: el borde de la ventana (el
  minuto antes de la primera hora del manifiesto: la orden del primer cierre de la ventana, la deuda
  ya anotada en Technical Debt, VISOR-CONSTRUCCION.md §4.3, punto 6) y las horas perdidas. Corrida 1:
  2 llenadas así, ninguna pareja; corrida 2: 10, una pareja (2026-07-10 07-11 o4) y los dos −2,00 R.
- **Lo que NO cambia esta rama**: nada de `src/` (encargo, «QUÉ NO CAMBIA»: si hiciera falta tocar
  `src/`, PARADA). El veredicto de la corrida 1 no depende de esas dos llenadas (§2.8 c).

## Lo que necesito que decidas (PARADA 3)

0. **Cómo se califica.** Opciones: (a) «no» como lo dejo: el respaldo evalúa contra precios
   anteriores a la orden, contra el principio escrito de ADR-0051 §2, y en el borde de la ventana
   fuera de lo que §8 le deja; (b) «sí, con deuda»: §5 lo permite por escrito y la deuda ya está en
   Technical Debt. Recomiendo (a): una orden que se llena con precios de antes de existir no es lo que
   el ADR pretende, y uno de los dos casos ni siquiera está en una hora perdida.
1. **Qué hace esta rama.** Opciones: (a) nada en código: la rama se entrega con el hallazgo, la
   deuda de Technical Debt se amplía en el cierre («el respaldo M1 evalúa la orden contra la vela cuyo
   cierre la colocó, en el borde de la ventana y en las horas perdidas; corrida 1: 2 llenadas, corrida
   2: 10; RECORRIDA-CONSTRUCCION.md §2.8 c») y una entrada nueva de la Next Action (o de la hoja, en R6
   o en el carril de deuda) para la rama de bróker que lo corrija con su test y su ADR o NOTA en
   ADR-0051, y repita la corrida que cuenta; (b) ampliar el contrato a `src/botsito/engine/llenado.py`
   y corregirlo aquí, con test y re-corrida (cambia el encargo: la corrida que cuenta corre «sobre el
   código de main tal cual»). Recomiendo (a): el encargo prohíbe tocar `src/`, el efecto sobre el
   veredicto es nulo y la corrección pide su propio ADR o NOTA (qué hace el respaldo con la vela de la
   decisión: saltarla, o bajar los ticks desde una hora antes de la ventana).
2. **El revisor.** Opciones: (a) lanzarlo tras tu respuesta con los cinco alcances, sobre la rama con
   §2.8 y la NOTA de ADR-0070; (b) esperar a la rama de bróker. Recomiendo (a).
3. **La toma de cada escenario** (Lo que no pude medir): (a) se queda sin medir en esta rama; (b) me
   autorizas un comando concreto (un guion que corra el motor sobre 2026-08-24 y lea la memoria del
   productor, como el de f), solo ese día y con la cuenta diaria). Recomiendo (a): la pregunta de
   b) era si las reglas de parada se aplican, y eso lo responden las cifras de la salida.

## Respuesta del consultor a la PARADA 3 (2026-10-27)

Copiada tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA 3 de trabajo/recorrida-construccion (2026-10-27). Cópiala tal cual al final del encargo y del informe, en «Respuesta del consultor a la PARADA 3», con su fecha, y aplícala punto por punto (skill fase-cero).
>
> 0. «No». En un minuto sin ticks el bróker simulado llena la orden con la vela M1 cuyo cierre la colocó, es decir, con precios anteriores a la orden. ADR-0051 §2 dice que una orden se evalúa contra lo posterior («sin mirar al futuro»), y §5 dice con qué se evalúa un minuto sin ticks, no que valga una vela anterior a la orden. Es un error nuestro (E), no una regla del trader.
> 1. Esta rama no toca src/ (el encargo lo prohíbe y el veredicto no cambia: sin las 2 llenadas la precisión sería 13,7 % y sigue «no»). Lo que sí hace:
>    a) Marca en las dos listas (§3 y §4, y en sus ficheros de anexos si los regenera un guion de la rama) las 10 llenadas de la corrida 2 que el bróker llenó con la vela que colocó la orden, con «E: llenada con la vela que la colocó (ADR-0051 §2)», para que no se elijan para la sesión 6. Y §3.1 y §4 dicen cuántas filas de cada lista llevan la marca.
>    b) La NOTA de ADR-0070 §3 de esta rama gana una frase: «2 de las 53 llenadas de esta corrida salen del respaldo M1 con la vela que colocó la orden, contra ADR-0051 §2 (RECORRIDA-CONSTRUCCION.md §2.8); sin ellas la precisión sería 13,7 % y el veredicto sigue "no".» (La NOTA es de esta rama y no está en main: se edita en un commit propio, sin reescribir el anterior.)
>    c) Líneas del cierre, además de las de §6:
>       - Technical Debt: sale la línea «El bróker simulado cotiza con el respaldo M1 la orden del primer cierre de la ventana…», porque pasa a la Next Action.
>       - Next Action, entrada nueva, con una letra que no esté viva ni aparezca como NA: en la hoja de ruta ni en los registros «# Next Action HECHA» de HISTORIA (compruébalo con grep y di cuál): «<letra>. El bróker simulado llena con el respaldo M1 una orden en la vela cuyo cierre la colocó, en todo minuto sin ticks (el borde de la ventana y las horas perdidas), contra ADR-0051 §2 (RECORRIDA-CONSTRUCCION.md §2.8; antes, VISOR-CONSTRUCCION.md §4.3). Rama propia con su test que rompe en main, una NOTA en ADR-0051 §5 y las corridas repetidas; antes de la próxima corrida del arnés que cuente (ADR-0070 §3).» Comprueba la línea contra test_hoja_de_ruta (palabra de dependencia seguida de una letra suelta que no esté viva).
>       - Hoja de ruta, entrada nueva «R3.5 · El respaldo M1 no llena con la vela que colocó la orden», Refs NA:<letra> · ID:ADR-0051, con Qué es, Depende de (nada), Quién (la sesión, con el encargo del consultor) y Hecho cuando (un test que llena con la vela que colocó la orden rompe en main y pasa en la rama, y las dos corridas de esta rama repetidas en la suya). Y R5.2 nombra NA:<letra> en «Depende de»: la medida de mayo no va sin ese arreglo.
>       - Vuelve a medir PROJECT_STATE con wc -c sobre la copia con todas las líneas; tiene que quedar por debajo de 23.000.
>    d) ERRORES-RECURRENTES, un hallazgo más en la fila de la rama: la deuda de VISOR-CONSTRUCCION describió el caso en el que se vio («la orden del primer cierre de la ventana») y no la condición («toda orden evaluada con el respaldo M1 en la vela que la colocó»), y la condición alcanzó también una hora sin ticks fuera del borde. Lección: una deuda se escribe nombrando la condición, no el caso.
> 2. Lanza ya el revisor (opus) con los cinco alcances, y el quinto ampliado: que los dos «no» de §2.8 y los recuentos 2 y 10 salen de lo que dicen el código del bróker y del cableado (el respaldo M1) y las salidas, comprobado a mano en los dos casos y en dos más de los 10. Su informe, pegado al final; arregla lo que bloquee o importe, o dime por qué no.
> 3. La toma de cada escenario queda sin medir, en «Lo que no pude medir». No hay guion nuevo.
>
> make check en verde antes de cada commit, con ruff format, ruff check y mypy antes sobre lo tocado. Si la guardia o el clasificador niegan algo, PARADA con el comando exacto y lo lanzo yo con «!».
>
> Rama lista para revisión, NO cerrada.

### La respuesta aplicada, punto por punto

| # | Punto | Estado | Evidencia |
|---|---|---|---|
| 0 | «No»: error nuestro (E) | Hecho | §2.8 c), §3.1, §4 |
| 1 a | La marca E en las dos listas y sus recuentos | Hecho | §3.2 (10 filas), §3.1 («10 de las 259»), §4 («3 de las 34», 4 llenadas); `lista-s14.txt` regenerado por `lista_s14.py` («10; de ellas en P6: 4, en 3 sesiones»); `entradas-antes-alternancia.txt` no se regenera (el guion que lo escribe corre el motor y estaba autorizado una sola vez) |
| 1 b | Frase nueva en la NOTA de ADR-0070 §3, commit propio | Hecho | su commit, tras el de esta respuesta |
| 1 c | Líneas del cierre: la deuda sale, la letra nueva, R3.5, R5.2, PROJECT_STATE < 23.000 | Hecho salvo la letra: **PARADA 4** | §6; `simular_cierre.py`: 22.872 bytes, a/b/c vacíos con H, R o Z |
| 1 d | Hallazgo para ERRORES-RECURRENTES | Hecho | §7, punto 7 |
| 2 | El revisor, con el quinto alcance ampliado | Lanzado tras los dos commits de esta respuesta | su informe, al final |
| 3 | La toma de cada escenario, sin medir | Hecho | «Lo que no pude medir (§2.8)» |

## PARADA 4 · No queda ninguna letra que cumpla el punto 1 c) (2026-10-27)

Medido con `grep` sobre `PROJECT_STATE.md`, `docs/plan/HOJA-DE-RUTA.md` y `docs/state/HISTORIA.md`:

| Dónde | Letras |
|---|---|
| Vivas en la Next Action (`^[A-Z]\. `) | A B C D F G I J K L M N Q T U V |
| Como `NA:` en la hoja de ruta | A B C D E F G I J K L M N O P Q S T U V W X Y |
| En los registros `# Next Action HECHA · X ·` de HISTORIA | E F H I J K O P Q R S T U V W X Y Z |

Entre las tres cubren las 26 letras: **ninguna cumple «que no esté viva ni aparezca como NA: en la
hoja de ruta ni en los registros "# Next Action HECHA" de HISTORIA»**. Y `test_hoja_de_ruta` solo
lee entradas de UNA letra (`entradas_vivas`, `^([A-Z])\. `; `REF`, `NA:[A-Z]`), así que una
entrada de dos letras no la vería ni la comprobaría. Las letras que solo están en HISTORIA (H, R y
Z) pasan los tres tests con todas las líneas del cierre (simulación de §6); las que la hoja nombra
en una entrada HECHA rompen (b) (medido con E).

## Lo que necesito que decidas (PARADA 4)

0. **La letra de la entrada nueva.** Opciones: (a) **Z**, que solo está en HISTORIA (`# Next Action
   HECHA · Z ·`, `trabajo/cases-rejilla`, 2026-10-10), no aparece en la hoja y no se confunde con
   los ids de tramo (R3.5) ni con la H reciente (RN-007, 2026-10-26); (b) R (HECHA el 2026-10-05,
   la más antigua, pero «NA:R» al lado de «R3.5» se lee mal); (c) H (HECHA el 2026-10-26, la más
   reciente); (d) ninguna reutilizada: una entrada fuera de la Next Action (solo en la hoja, R3.5,
   sin `NA:`), o un esquema de dos letras, que pide cambiar `test_hoja_de_ruta.py` en su propia rama
   (tests/ está protegido en esta). Recomiendo (a): pasa los tres tests (`a: []`, `b: []`, `c: []`;
   22.872 bytes), y el registro HECHA de la Z anterior queda en HISTORIA con su fecha, que la
   distingue. Coste de (d): o la entrada no está en la Next Action, que es lo que pediste, o una rama
   más antes de cerrar.
1. **Regla para la próxima vez.** Opciones: (a) desde ahora, una letra se reutiliza solo si su
   registro HECHA es anterior y no aparece en la hoja, y el registro HECHA nuevo lleva fecha (ya la
   lleva siempre); (b) abrir en el carril de deuda que `test_hoja_de_ruta` admita entradas de dos
   letras. Recomiendo (a), y (b) solo si se vuelven a agotar.
2. **La línea del calendario de cierres** (revisor, a6). Las dos salidas del arnés llevan, como todo
   anexo del arnés desde ADR-0068 (17 ficheros en `docs/validation/anexos`, 14 ya en `main`), la
   línea `calendario: cubre <desde> a <hasta> UTC, 228 cierres`, cuyo primer extremo cae en un
   diciembre: es la cobertura del calendario de cierres del perfil, no una vela, un precio ni un
   instante de mercado. Opciones: (a) la regla de «nada anterior al día dev» no la alcanza, y se dice
   así; (b) la alcanza, y hace falta una rama que la quite de la salida del arnés (`cableado.py`,
   `_informe_cierres`) y regenere los anexos. Recomiendo (a): no es material de ningún día, y lleva
   en `main` desde ADR-0068 sin que ninguna regla la haya tocado.

## 10. El revisor

Lanzado tras la respuesta a la PARADA 3 (punto 2), sobre 5e66bdd, con los cuatro alcances del
encargo y el quinto de las PARADAS 2 y 3 ampliado. Su informe, tal cual (ninguna cita de un tramo no
citable que retirar):

> ## Informe del revisor · trabajo/recorrida-construccion · 2026-10-27
>
> Base: main 88f97f7 (merge-base). HEAD 5e66bdd. 11 commits. `git status` limpio. El informe está en EN CURSO, con la PARADA 4 abierta (la letra), así que la rama todavía no puede declararse lista. Esa PARADA es una decisión pendiente del consultor y está declarada, no es un defecto.
>
> ### Eje (a) · Reglas de la casa
> Resumen: 0 bloquea, 2 importa, 4 menor.
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | a1 | importa | El recuento de los R de las 77 llenadas de P6 en §4 no cuadra con los anexos. El informe dice «5 objetivos y 1 cierre manual positivo, 24 a cero (break even) y 47 negativas». En los ficheros salen **4 objetivos, 1 manual positivo, 19 a cero exacto y 53 negativas** (de esas 53, 42 son stops completos y 11 son stops tras break even entre −0,01 y −0,33). Contado desde los dos ficheros (`lista-s14.txt` y la sección «## Todas las llenadas» de `entradas-antes-alternancia.txt`, filas P6), da lo mismo en ambos. En la tabla de §4 también salen solo 4 «(objetivo)»: 01-06, 01-16, 01-22 y 04-08. | `docs/validation/RECORRIDA-CONSTRUCCION.md:1323-1324`. Con `uv run python -c` sobre `entradas-antes-alternancia.txt`: `[(('manual','pos'),1), (('objetivo','pos'),4), (('stop','0'),19), (('stop','neg'),53)]` sobre 77 filas P6. |
> | a2 | importa | La lectura de ticks de §2.8 no está declarada. `costes_y_sesiones.py` lee los TICKS de los días dev de construcción (`carpeta_datos`, `buscar_manifiesto_ticks`, `cargar_ticks`) y se ejecutó después de la PARADA 2. La única fila del día en HOLDOUT-EXPOSICIONES se escribió antes de correr nada y solo nombra los manifiestos de ticks (fase 0) y el M1 del calentamiento. Tampoco lo nombra §5.4. CLAUDE.md pide que el material de desarrollo «se declara igual el mismo día». Es material dev: no hay ningún día reservado de por medio (los manifiestos de ticks tienen exactamente los días dev, §0.b). | `costes_y_sesiones.py:35-39,175-195`. `git diff main...HEAD -- docs/validation/HOLDOUT-EXPOSICIONES.md`: una sola fila añadida, sin `costes_y_sesiones`. `RECORRIDA-CONSTRUCCION.md:1414-1423`. |
> | a3 | menor | El informe dice que `engine/llenado.py:10-12` «lo repite para todo evento». El texto citado está en el apartado «Con ticks, el orden real: …», y el respaldo M1 (líneas 13-15) no lo dice. El argumento se sostiene con ADR-0051 §2 y la decisión del consultor; esta cita dice algo menos. | `RECORRIDA-CONSTRUCCION.md:955-956`; `src/botsito/engine/llenado.py:10-15`. |
> | a4 | menor | En §2.2, «desde la sesión 11-15 de ese día RN-032 … prohíbe abrir_operacion en todos los cierres» no es exacto: en 2026-01-20 11-15 la corrida 1 llenó o6, o7 y o13 antes de que mordiera RN-032. Además, el «96 de las 104 llevan ese bloqueo» incluye 16 sesiones de enero anteriores a RN-032 (por ejemplo 2026-01-02 11-15), así que no mide RN-032. La señal del hallazgo 5 de §7 hereda esa imprecisión. | `RECORRIDA-CONSTRUCCION.md:655-660,1535-1539`; `cuenta-arrastrada.txt:1120-1127` (las tres llenadas). En «Por sesion» de la corrida 1, el bloqueo aparece desde 2026-01-02 11-15 (grep). |
> | a5 | menor | `costes_y_sesiones.py` escribe a mano cifras del registro (`FRACCION_STOP = 0.8`, `MULTIPLO_OBJ = 3`, `COMISION_REDONDA_POR_LOTE = 10`, `USD_POR_PUNTO_Y_LOTE = 1`) en vez de leerlas. Como es un guion de medida en anexos y no forma ejecutable, no rompe `test_no_business_literals`. Pero si el registro cambia, «R teórico» y «comisión en R» dejan de valer sin avisar. | `docs/validation/anexos/RECORRIDA-CONSTRUCCION/costes_y_sesiones.py:52-55`. |
> | a6 | menor | Para el alcance (4), la única fecha de mercado fuera de los días dev en los textos commiteados es la línea `calendario: cubre <fecha de 2025> … <fecha de octubre de 2026> UTC, 228 cierres`. Es la cobertura del calendario de cierres de ADR-0068: no es una vela, ni un precio, ni un instante de mercado. El arnés la escribe igual en los 14 anexos que ya hay en main. Su primer extremo cae en un diciembre. La anoto para que el consultor decida si su regla alcanza también a esa línea. | `cuenta-arrastrada.txt:1223`, `diaria.DIAGNOSTICO.cuenta=diaria.txt:3506`, `diff-linea-base.txt:1347`. Grep `calendario: cubre` sobre `docs/validation/anexos`: 17 ficheros. |
>
> Comprobado sin hallazgos:
> - **Contrato.**
>   - `uv run python scripts/contrato_rama.py` → `CONTRATO: 26 ficheros dentro del contrato de trabajo/recorrida-construccion (riesgo alto, artefacto docs/validation/RECORRIDA-CONSTRUCCION.md, tramo 'R4', 3 comprobaciones para el revisor)`, exit 0.
>   - `git diff main --stat -- src/ tests/ knowledge/ Makefile .claude/` → vacío. También vacío sobre `config/ scripts/ pyproject.toml docs/plan/ data/manifests/`.
>   - `make check` no lo ejecuté. Su evidencia es `make-check.log`: `2970 passed`, `SELLO: make check en verde sobre el arbol f3167a7f…`, que es igual a `git rev-parse HEAD^{tree}`, y `PICO DE MEMORIA … 300 MiB`.
> - **Alcance (1).**
>   - `OPCIONES_QUE_NO_CAMBIAN_LA_CORRIDA` = {--salida, --tracemalloc, --meses, --simular, --perfil, --fase} (`arnes.py:80-82`). `informe` resta esa lista (`:281`).
>   - `opciones_de_la_corrida` lee las opciones de los parsers (`cli.py:2218-2232`).
>   - `cuenta-arrastrada.txt`: `grep -c DIAGNOSTICO` = 0. Línea 13: `habilita medir … (ADR-0070): no (cobertura 3.5 % por debajo de 70.0 %; precision 13.2 % por debajo de 60.0 %)`, sin «opción fuera de la lista». La diaria, en cambio, sí la lleva (`:16`), lo que demuestra que el mecanismo funciona.
>   - `PERFIL: ftmo-2step-swing-100k; FASE: reto` (`:687`).
>   - El veredicto es literal e idéntico en §2.1 (`RECORRIDA-CONSTRUCCION.md:625`) y en la NOTA de ADR-0070 §3. Las dos frases añadidas a la NOTA son literales de las respuestas a las PARADAS 2 y 3, y cada una va en su propio commit (a468d5d, 5e66bdd). `## Estado` de ADR-0070 = `ACTIVE`.
> - **Alcance (2).** Ningún fichero de src/, tests/, knowledge/ ni .claude/ en `git diff --stat main...HEAD`.
> - **Alcance (3).**
>   - §2.2: las 10 filas cuadran con «### Resumen por mes» de las dos salidas, y los totales con la cabecera.
>   - §2.6: las 10 filas cuadran con las cabeceras de `patrones-diaria.txt` y `patrones-arrastrada.txt`. La «posible M» da 25 y 12.
>   - §3.2 contra «### Ordenes» de la corrida 2: 2026-01-02 11-15 o7 (llenada 12:12:26, 6 reubicaciones = o1-o6 canceladas con RN-006), 2026-04-07 07-11 o6 (06:31:14), 2026-07-10 07-11 o12 (07:59:02) y las 8 llenadas de 2026-08-24 07-11. Todo cuadra.
>   - §3.1, recalculado desde `entradas-antes-alternancia.txt`: 259 filas, 0 zonas 149 y 1 zona 110, dónde 161/43/55, cruces zonas×patrón y dónde×patrón, R 36/176/47, motivos 222/34/3. Todo igual.
>   - Sesgo en «Por sesion» de la corrida 1: 2026-04-03 07-11 bajista, 2026-04-03 11-15 alcista, 2026-04-09 07-11 alcista, 2026-08-04 11-15 bajista, 2026-08-07 11-15 alcista. Coincide con `patrones-arrastrada.txt` y con `rn003-abril-agosto.txt`.
>   - §2.5: 129 líneas `<`, 1.191 `>`, 14 bloques. La línea base entró en a0d0599.
> - **Alcance (4).** Rastreo mecánico de todos los `.txt` de anexos y del informe:
>   - 0 fechas de mercado fuera de los días dev, salvo la línea del calendario (a6).
>   - Cada clave de punto `nivel@minuto` (215 + 1.329 + 550 + 94) cae en el día dev de su fila.
>   - `grep -c "antes del dia"` = 0 en las tres listas.
>   - Ninguna hora anterior a 05:00Z en las columnas de camino.
>   - Los mensajes de commit de la rama no llevan ninguna fecha ni ningún precio.
> - **Alcance (5), mecanismo.**
>   - `primer_llenado_stop` toma la vela M1 de un minuto sin ticks si `_fin_ms(vela) > desde_ms` (`llenado.py:208-222`). El bróker pasa `desde = max(ahora_ms - 1, ultimo_cambio_ms)` (`broker.py:746-753`). El cableado coloca en `hasta_ms = instante*60000 - 1` (`cableado.py:297,313`).
>   - Así que la vela cuyo cierre colocó la orden (fin = colocada + 1 ms) es elegible: es exactamente lo que dice §2.8 c).
> - **Alcance (5), los casos a mano.**
>   - 2026-04-07 07-11 o1: colocada 04:59:59.999, `llenada | o1 | respaldo_m1` a las 05:00:00, `stop | pos-o1 | ticks` a las 05:00:00.061 (diaria `:1601-1602,:2499`). Caja 5 y distancia 4. El minuto 04:59 está fuera de las horas 05-13 de abril.
>   - 2026-04-23 07-11 o3: colocada 05:04:59.999, llenada 05:05:00 con respaldo y stop a las 05:06:00 con respaldo (`:1695-1696,:2705`). Esa hora está en `HORAS_PERDIDAS`.
>   - De los 10, revisé además 2026-01-05 11-15 o20, 2026-04-06 11-15 o11 y o12, 2026-07-10 07-11 o3 y o4, 2026-08-20 07-11 o14 y 2026-04-07 11-15 o28: en todos, la llenada con respaldo cae 1 ms después de la colocada.
>   - Censo completo. Corrida 2: 16 llenadas con respaldo; 10 son la vela que colocó la orden (2 en el borde y 8 en hora perdida) y 6 son otras (o19, o21 del 01-05; o29 del 04-07; o8 del 04-22; o1 del 04-23; o12 del 08-20). Corrida 1: 4 llenadas con respaldo; 2 son la vela que colocó (01-05 o20 y 01-06 o1) y 2 son otras. Ninguna de esas 2 es una de las 7 parejas (T0 de 01-02, 07, 09, 12, 13, 14 y 19), así que 7/51 = 13,7 %. 2026-07-10 o4 sí es T0 (trader 05:36:35).
>   - Casos de a): 2026-01-16 11-15 o16 (colocada 12:34:59.999, llenada 12:35:15.720, desplazamiento +3, caja 9 y distancia 8, objetivo 12:46:39.863) y 2026-01-29 11-15 o28 (caja 17 y distancia 14, salida 12 puntos pasado el nivel, R −26/14 = −1,86). Las dos cuadran con las salidas.
>   - 2026-08-24 07-11 de b): 8 llenadas (o3, o4, o6, o8, o12, o19, o21, o23), 8 claves de punto distintas, 5 escenarios (2,2,1,1,2) y ninguna línea «Por sesion».
>   - La racha de 7 sigue `racha.py` (`clasificar_cierre`: un stop movido es break even y no corta la racha; 6 en 07-11 más o25 en 11-15).
>   - RN-020 no aparece en ninguna «Reglas disparadas» de las dos salidas (grep: 1 aparición en cada una, la línea TOPE DEL TRADER).
>   - En §2.8 nada es anterior a las 05:00Z de su día.
> - **Citas.** ADR-0051 §2 (`:46-47`), §5 (`:73-78`) y §8 (`:119-122`) son literales. RN-032 está en `strategy_spec.yaml:2491-2499`. `cableado.py:248-249` (la cuenta diaria pone a None la cuenta, el seguidor y la racha). Las tres son correctas.
> - **Regímenes de cambio.** No toca nada de evidence, feedback, manifests, transcripciones, fotogramas ni libros.yaml. HISTORIA solo crece (+168 líneas, y contiene el PROJECT_STATE de main entero). HOLDOUT-EXPOSICIONES: +1 fila. No hay ambigüedades, ni sitios con `cita`, ni informes cerrados editados. CABLEADO-SIMULADOR-LINEA-BASE.txt está intacto. `PROJECT_STATE.md` solo cambia en lo de abrir-rama (23.098 bytes).
> - **Copias de R3.1.** `horas_perdidas.py` es idéntico a la de R3.1 (diff vacío). `patrones.py` difiere solo en la cabecera y en `_cuerpo` (`ROTULO`). `simular_cierre.py` toma la raíz por argumento y escribe solo en `tempfile`.
>
> ### Eje (b) · Encargo
> Resumen: 0 bloquea, 2 importa, 1 menor. Requisitos: 24 hechos, 3 parciales, 0 no hechos.
>
> | # | Requisito | Estado | Evidencia |
> |---|---|---|---|
> | 1 | Rama desde 88f97f7 con abrir-rama, contrato R4 y artefacto; encargo copiado | Hecho | merge-base 88f97f7; `contrato.yaml:1-4`; f043554 |
> | 2 | Archivo 49 en HISTORIA y PS solo lo de abrir-rama | Hecho | diff de PS (Current Branch/Feature, Archivo 49); HISTORIA contiene el PS de main |
> | 3 | Nada de src/tests/knowledge/Makefile/.claude/; criterio_fidelidad, ambigüedades, ADR-0083 y línea base intactos | Hecho | diff vacío (eje a) |
> | 4 | Next Action y hoja de ruta sin tocar | Hecho | `git diff main --stat -- docs/plan/` vacío; en PS solo cambian las líneas de apertura |
> | 5 | Fase 0 a)-j) con fichero:línea y PARADA | Hecho | §0.a-§0.m, «Lo que necesito que decidas» |
> | 6 | Respuestas del consultor copiadas tal cual en encargo e informe (PARADA, 2 y 3) | Hecho | comparadas por guion: las tres iguales (21/17/20 líneas `>`) |
> | 7 | Fila de exposiciones y README en su propio commit, antes de correr | Hecho | a713e23 |
> | 8 | Copia de patrones.py que corta solo `[DIAGNOSTICO`, con horas_perdidas idéntico | Hecho | diffs (eje a) |
> | 9 | Guion f) con test de humo en los dos sentidos | Hecho | `test_humo.py`; §1.2 (no lo ejecuté: escribe caché) |
> | 10 | Test de patrones sobre una línea «Por sesion» **real** con y sin rótulo (fase 0 e) | Hecho de otra forma | `test_humo.py:24-27` usa una línea sintética (b2) |
> | 11 | Las tres corridas con los comandos literales; TIEMPO y MEMORIA; nombres finales | Hecho | §2:606-613; ficheros en anexos |
> | 12 | Repetición de la 1 con diff e idéntica | Hecho (no verificable) | §2.4; la copia se borró |
> | 13 | Diff de la línea base a fichero | Hecho | `diff-linea-base.txt` (129/1191/14) |
> | 14 | Guion f) una vez, coincidencia 291 | Hecho | cabecera de `entradas-antes-alternancia.txt:3` |
> | 15 | Por corrida y por mes: trader, puntuables, parejas, cobertura, precisión; veredicto literal | Hecho | §2.1, §2.2 (comprobados) |
> | 16 | Veredicto de la cuenta, peticiones, freno, tramo no continuo | Hecho | §2.2:662-681 |
> | 17 | Lo de i): RN-020, ADR-0086, RN-036, RN-037; DEFAULT_AMBIGUOUS | Hecho | §2.3, §0.i |
> | 18 | Diff resumido por sección | Hecho | §2.5 |
> | 19 | Patrones de las dos corridas, PUNTO-USADO como contexto, «posible M» | Hecho | §2.6 |
> | 20 | Embudo por mes y rechazos | Hecho | §2.7 |
> | 21 | Lista de la decisión 5 con sus columnas (y las de la respuesta: al colocar, reubicaciones, escenario) | Hecho | §3; cruces recalculados |
> | 22 | Lista «Para S-14» | Hecho, con un recuento erróneo | §4; ver a1 |
> | 23 | §2.8 a) b) c) (PARADA 2, punto 1) | Hecho; la toma por escenario, sin medir con permiso (PARADA 3, punto 3) | §2.8; costes-y-sesiones.txt |
> | 24 | NOTA de ADR-0070 §3 en commit propio (+ las frases de las PARADAS 2 y 3) | Hecho | a468d5d, 5e66bdd |
> | 25 | NOTA de ACTIVAR-A35-A44 §5 en commit propio, contrato ampliado | Hecho, con texto ya superado | 3923789; b1 |
> | 26 | Marca E en las dos listas y sus recuentos (PARADA 3, 1 a) | Hecho | §3.2: 10 filas; §4: 3 de 34; `lista-s14.txt:3` |
> | 27 | Líneas del cierre medidas (incl. la letra nueva) | Parcial | §6; la letra espera la PARADA 4 |
> | 28 | «El encargo, punto por punto», desviaciones, comandos y exposiciones | Parcial | §5, no actualizado tras las PARADAS 2 y 3 (b2) |
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | b1 | importa | La NOTA que la rama añade a `ACTIVAR-A35-A44.md` §5 dice «los días que se abren en el visor los elige el consultor en su PARADA 2». La respuesta a la PARADA 2 dijo después «el visor NO se abre en esta rama». §5.2, punto 1, repite la frase vieja. Como la NOTA es de esta rama y no está en main, se puede corregir antes del cierre. | `git diff main...HEAD -- docs/runbooks/ACTIVAR-A35-A44.md` (última frase de la NOTA); `RECORRIDA-CONSTRUCCION.md:1369-1370`; encargo `:139` («el visor NO se abre en esta rama»). |
> | b2 | importa | §5 se quedó como estaba en la PARADA 2. La fila 22 de §5.1 dice «22.640 bytes» y §6 ya dice 22.872. La fila 24 sigue «Pendiente de la PARADA 2». §5.3 («Comandos ejecutados, literales, en orden») no recoge `costes_y_sesiones.py`, la nueva pasada de `lista_s14.py`, `simular_cierre.py` con su letra, `medir_ps.py` ni los `make check` posteriores (dice «×5 hasta la PARADA 2»). §5.4 no recoge la lectura de ticks de §2.8 (a2). El encargo pide en el informe los «comandos literales ejecutados y las exposiciones del día». | `RECORRIDA-CONSTRUCCION.md:1361,1363,1392-1394,1414-1423,1514-1515`. |
> | b3 | menor | La fase 0 e) pedía un test «sobre una línea «Por sesion» real con rótulo y otra sin él»; el test usa una línea sintética con el formato real. La fase 1 pide «salidas sintéticas», así que el propio encargo se contradice. §1.2 dice «sintética», pero no dice por qué se apartó de «real». | `test_humo.py:24-27`; `RECORRIDA-CONSTRUCCION.md:587`; encargo `:47` y `:57`. |
>
> Lo que la rama hace y el encargo no pedía:
> - `comparar_rn003.py` y `lista_s14.py`, declarados como desviación 3 en §5.2.
> - `simular_cierre.py`, que sale de la PARADA 3, punto 1 c, y se describe en §6.
> - `costes_y_sesiones.py`, que sale de la PARADA 2, punto 1.
>
> Todos están justificados en el informe.
>
> Lo que el encargo dice que no se toca: comprobado con el diff (eje a, alcance 2). Fuera del contrato no hay nada (`contrato_rama.py` en verde).
>
> ### Lo que no pude comprobar
> - El determinismo de la corrida 1 (§2.4): la copia se borró, y el arnés no lo corro (solo lectura).
> - `pytest` de `test_humo.py`: escribe `.pytest_cache` y `__pycache__`. Su evidencia es lo que pega §1.2 (10 passed).
> - La CI de main sobre 88f97f7 y el `/model` al empezar: hacen falta `gh api` y el estado de la sesión. Me quedo con lo que dice la cabecera del informe.
> - Los `make check` de los commits anteriores al último: solo el log del último sigue ahí (sello = árbol de HEAD). El hook `pre-commit` exige el sello en cada commit.
> - La toma de cada escenario (la «zona» de b), §2.8): no está en ninguna salida; la PARADA 3, punto 3 la dejó sin medir.
> - Que el sesgo «alcista/bajista» impreso para 2026-04-01 07-11 y 2026-07-01 no derive de velas del día de calendario anterior: con la rejilla de Madrid, la primera H4 del día puede empezar el día antes. El arnés de main imprime esa etiqueta, que no es ni vela, ni H4, ni precio, ni instante. La respuesta a la PARADA 2, punto 2 ya aparta esas sesiones de la hoja de la sesión 6.
> - Las 18 horas perdidas frente a los manifiestos y los recuentos por manifiesto de §0.b: no leí `data/`.
> - `git write-tree` (escribe): no ejecutado.
>
> ### Comandos ejecutados
> 1. `git branch --show-current && git merge-base main HEAD && git log --format='%h %s' main..HEAD && git diff --stat main...HEAD && git status --short`
> 2. `uv run python scripts/contrato_rama.py`; `git diff main --stat -- src/ tests/ knowledge/ Makefile .claude/`
> 3. `git diff main --stat -- config/ scripts/ pyproject.toml docs/plan/ data/` (lo negó la guardia por `data/`), y después `… data/manifests/`
> 4. `ls -la make-check.log && grep -n "SELLO\|PICO DE MEMORIA\|passed\|failed" make-check.log | tail -8`
> 5. `git rev-parse HEAD^{tree} && git log -1 --format='%h %cd' HEAD`
> 6. Read: encargo, contrato.yaml, informe (por tramos), `llenado.py:1-250`, `cableado.py:225-360`, `broker.py:730-760`, `racha.py:1-165`, `horas_perdidas.py`, `costes-y-sesiones.txt`, `costes_y_sesiones.py:170-220`, `lista-s14.txt`, `test_humo.py:1-40`, ADR-0051 `:40-124`, `strategy_spec.yaml:2488-2501`
> 7. Grep sobre rutas literales: `llenado.py`, `cableado.py`, `src/botsito/engine` (primer_llenado_*), `broker.py`, `arnes.py`, `cli.py`, la diaria y la arrastrada (secciones, órdenes, eventos, respaldo_m1, Por operación), `RECORRIDA-CONSTRUCCION.md` (encabezados, filas), `docs/validation/anexos` (`calendario: cubre`, recuento), `costes_y_sesiones.py`, `simular_cierre.py`, `test_humo.py`, ADR-0051, `knowledge` (*.yaml, nombres de parámetro)
> 8. `diff` de `horas_perdidas.py` y `patrones.py` entre CORRIDA-CONSTRUCCION y RECORRIDA-CONSTRUCCION
> 9. `uv run python -c …` (solo lectura) de cuatro tipos: claves de punto frente al día de su fila (en dos pasadas); fechas de mercado fuera de los días dev en todos los ficheros de la rama y en los anexos; el Archivo 49 frente al PS de main; las respuestas del consultor en encargo e informe; los cruces de §3.1 y los R de P6 (desde `lista-s14.txt` y desde `entradas-antes-alternancia.txt`)
> 10. `grep`/`sed`/`cut`/`head` de solo lectura sobre los anexos: la fecha del calendario, las fechas de la fila de exposiciones, los mensajes de commit (`git log --format`), los resúmenes por mes, la cabecera y el embudo, las cabeceras de patrones y `rn003-abril-agosto.txt`, el sesgo de «Por sesion», las filas de órdenes de muestra, «Reglas disparadas», el bloqueo RN-015, los recuentos de `diff-linea-base.txt`, `git log` de la línea base, `wc -c PROJECT_STATE.md`, `## Estado` de ADR-0070 y las marcas E de §3.2 y §4
> 11. `git diff main...HEAD -- docs/adr/0070-… docs/runbooks/ACTIVAR-A35-A44.md docs/validation/HOLDOUT-EXPOSICIONES.md PROJECT_STATE.md`
>
> Ficheros relevantes: `C:\Users\USER\Desktop\Bot v3\docs\validation\RECORRIDA-CONSTRUCCION.md`, `C:\Users\USER\Desktop\Bot v3\docs\validation\anexos\RECORRIDA-CONSTRUCCION\`, `C:\Users\USER\Desktop\Bot v3\docs\runbooks\ACTIVAR-A35-A44.md`, `C:\Users\USER\Desktop\Bot v3\docs\adr\0070-umbral-de-construccion-para-medir-mayo.md`, `C:\Users\USER\Desktop\Bot v3\docs\validation\HOLDOUT-EXPOSICIONES.md`, `C:\Users\USER\Desktop\Bot v3\src\botsito\engine\llenado.py`.

### 10.1 Lo que se hizo con los hallazgos del revisor

| # | Gravedad | Qué se hizo |
|---|---|---|
| a1 | importa | **Arreglado y medido**: el recuento propio da lo mismo que el suyo (`r_p6.py`, carpeta de trabajo: «77 [('manual pos', 1), ('objetivo pos', 4), ('stop cero', 19), ('stop neg', 53)]»); §4 dice ahora 4, 1, 19 y 53, con el recuadro de la corrección |
| a2 | importa | **Arreglado**: segunda fila del 2026-10-27 en `HOLDOUT-EXPOSICIONES.md` con la lectura de ticks de §2.8 (material de desarrollo, ningún día reservado, sin calentamiento), y §5.4 la nombra |
| a3 | menor | **Arreglado**: §2.8 c) y la PARADA 3 dicen que `llenado.py:10-12` lo dice de los ticks, y que el respaldo (`:13-15`) no lo dice |
| a4 | menor | **Arreglado**: §2.2 dice que el 2026-01-20 11-15 aún llena o6, o7 y o13 y que el bloqueo de RN-015 también lo dan otras reglas antes; la señal del hallazgo 5 de §7 pasa a la curva plana sin llenadas con RN-032 entre las disparadas |
| a5 | menor | **Declarado** en §2.8 (los cuatro valores, de dónde salen y qué columnas dejan de valer si cambian); el guion no se cambia: sus salidas ya están commiteadas y cuadran (alcance 5) |
| a6 | menor | **A la PARADA 4, punto 2**, con recomendación: la línea es la cobertura del calendario de cierres, no material de un día, y lleva en `main` desde ADR-0068 |
| b1 | importa | **Arreglado**: la última frase de la NOTA de `ACTIVAR-A35-A44.md` §5 (de esta rama, no está en `main`) dice ahora que el visor no se abre en la rama y que §2.8 midió sobre las salidas y los ticks; §5.2, punto 1, igual |
| b2 | importa | **Arreglado**: §5.1 (filas 22, 24, 25 y 26 y el recuadro), §5.3 (los comandos tras la PARADA 2, del 9 al 12, y las negativas de la guardia) y §5.4 (la segunda fila) |
| b3 | menor | **Declarado** en §1.2: por qué el test usa una línea sintética con el formato de la real, y que la real se midió en §0.e |

«Lo que no pude comprobar» del revisor: lo cubren la cabecera (la CI de `main` por la API de
check-runs, con su salida, y la variable del entorno), §2.4 (la repetición, con su `diff` vacío),
§1.2 (el `pytest` de los tests de humo: 10 passed) y el hook `pre-commit`, que exige el sello en cada
commit. El sesgo del 1 de abril y del 1 de julio queda fuera de la hoja de la sesión 6 por la
respuesta a la PARADA 2, punto 2.

## Respuesta del consultor a la PARADA 4 y orden de cierre (2026-10-27)

Copiada tal cual:

> Modelo: Opus · Esfuerzo: medio
>
> Respuesta del consultor a la PARADA 4 y orden de cierre de trabajo/recorrida-construccion (2026-10-27). Copia la respuesta tal cual al final del encargo y del informe, en «Respuesta del consultor a la PARADA 4», con su fecha, en un commit propio antes del commit del contrato.
>
> RESPUESTA A LA PARADA 4
> 0. (a) Z. Pasa los tres tests de test_hoja_de_ruta y PROJECT_STATE queda en 22.872 bytes; el registro HECHA de la Z anterior queda en HISTORIA con su fecha, que la distingue.
> 1. (a). Desde hoy, DECISIÓN DEL CONSULTOR: una letra de la Next Action se reutiliza solo si su registro «# Next Action HECHA» es anterior y la hoja de ruta no la nombra; el registro HECHA nuevo lleva su fecha. Esta rama no la escribe en ningún runbook (docs/runbooks/ está fuera de su contrato salvo ACTIVAR-A35-A44.md): la lleva el encargo de la rama de la cuarentena (G.5) a docs/runbooks/DECISIONES-DE-PROCESO.md. Las dos letras solo si se vuelven a agotar.
> 2. (a). La regla de «nada anterior al día dev» no alcanza la línea «calendario: cubre … UTC, N cierres» de la salida del arnés: es la cobertura del calendario de cierres del perfil (ADR-0068), no una vela, un precio, un instante de mercado ni material del trader. Dilo así en §5.4.
>
> ORDEN DE CIERRE
> Ciérrala con la skill cerrar-rama, siguiendo docs/runbooks/RITUAL.md con todas sus puertas. Tag: stable/F38g-recorrida-construccion.
>
> En el commit del contrato (chore(cierre): sale el contrato y entra el registro en HISTORIA):
> - Sale contrato.yaml; entra el registro del cierre en HISTORIA con stable/F38g-recorrida-construccion^{commit} en lugar del sha.
> - Next Action: V sale a HISTORIA con su texto literal bajo «# Next Action HECHA · V · …» (RITUAL.md, punto 3); F, la de §6; entra Z con el texto de §6, tras la N.
> - Technical Debt: sale la línea «El bróker simulado cotiza con el respaldo M1 la orden del primer cierre de la ventana…».
> - Hoja de ruta, todo lo de §6 con Z en lugar de <letra>: R4.1 HECHA (NA:V fuera de sus Refs); R4.2 (NA:V fuera, «Qué es» con las dos listas y «sin las marcadas E», «Depende de» nada); R5.2 con su «Depende de» nuevo y NA:Z; R3.5 nueva con Refs NA:Z · ID:ADR-0051; G.5 nueva.
> - ERRORES-RECURRENTES, la fila de la rama: los hallazgos 1 a 7 de §7 tal cual, y uno más, menor, del consultor: el primer borrador de este encargo llevaba una restricción para un «sí» que contradecía ADR-0070 §6 y una definición de la lista de §0.b.8 que dejaba fuera el caso que la motivaba (S-10, reubicada, y S-10b, con una zona); las vio el auditor del consultor antes de entregar. Lección para el consultor: no es una regla nueva, sino dos que ya existen y no se aplicaron (una restricción se contrasta con el ADR del que sale, y una categoría se prueba sobre el caso que la motiva antes de fijarla). Para el revisor: sin hallazgos que se le escaparan.
> - Antes de commitear, mide PROJECT_STATE con wc -c (tiene que dar unos 22.872, por debajo de 23.000) y pasa test_hoja_de_ruta y test_project_state en el make check sellado.
>
> Después, lo de siempre: merge --no-ff a main, el tag, el commit de estado que solo reemplaza Current Branch, Current Feature (la frase de §6), Stable Main State y Last Stable Commit (la Next Action ya cambió en el contrato y aquí no se toca), make check sellado, push atómico de main y el tag en un solo comando (confirmo la regla ask con «1. Yes»), la CI de main en verde mirada sin guion ni bucle, y borrar la rama local. No hay fix/ que borrar.
>
> Nunca --no-verify, push --force, borrar tags, cherry-pick ni rebase. Si algo no cuadra, PARADA antes del merge.
>
> Informe final: sha de main, tag, número del run de la CI de main con su resultado, ramas que quedan (local y remota) y tamaño de PROJECT_STATE en bytes.

## Estado

LISTA PARA REVISIÓN, NO cerrada. Todo lo del encargo y de las respuestas a las PARADAS 1, 2 y 3 está
hecho y commiteado, con el revisor pegado y sus hallazgos arreglados o declarados. La PARADA 4 está
respondida (la letra es Z; la línea del calendario queda fuera de la regla, §5.4) y llegó la orden
de cierre (2026-10-27, tag `stable/F38g-recorrida-construccion`).
