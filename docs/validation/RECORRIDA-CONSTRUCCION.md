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

## Estado

EN CURSO. Fase 0 commiteada; PARADA: espero la respuesta del consultor a «Lo que necesito que
decidas».
