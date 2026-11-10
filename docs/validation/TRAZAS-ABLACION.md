# FUNCTIONALITY VALIDATION REPORT

**Funcionalidad:** F (1) · la bitácora de decisiones del motor y el diagnóstico de ablación (R4.4)
**Rama:** trabajo/trazas-ablacion
**Objetivo:** ver por qué decide el motor: una bitácora de decisiones por día y sesión, una ablación que apaga una regla VIGENTE a la vez, los días 2026-04-13, 2026-07-02, 2026-07-03 y 2026-07-14 medidos con su clase propuesta, y el recorte de `PROJECT_STATE.md` (encargo en `docs/encargos/trabajo-trazas-ablacion.md`).

## Base (comprobada con git al abrir, 2026-11-09)

- `git rev-parse main origin/main`: `144e42c24d5afb190bbfedea45f2eeaae32354b1` las dos veces.
- Último `- Tag:` de HISTORIA: `stable/F38u-video-julio`; `git rev-parse "stable/F38u-video-julio^{commit}"` = `git rev-parse main^1` = `129ea336fb67076e87d8d0cde8b610d8e7a6cacf`; en origin (`git ls-remote --tags`: `d134ffc…` refs/tags/stable/F38u-video-julio).
- CI de main sobre `144e42c24d5afb190bbfedea45f2eeaae32354b1` (check-runs): `python completed success`, run 42681006516.
- `git branch --list`: solo `main`; `git ls-remote --heads origin`: solo `refs/heads/main`.
- Modelo: Opus 5.5 (`claude-opus-5-5`, del entorno de la sesión). El esfuerzo no lo puede leer la sesión: `/model` es un comando de Aleks.

## 0. Fase 0 (2026-11-09)

No se ha escrito código, spec ni knowledge. Lo único escrito en el repo es la apertura (encargo,
contrato, Archivo 64 de HISTORIA, `PROJECT_STATE.md` apuntando a la rama, este informe) y la fila del
día en `HOLDOUT-EXPOSICIONES.md`, escrita antes del primer `make check`. Ninguna corrida del arnés.

### 0.1 La base y lo de mirar

- La base, arriba («Base»): las cuatro comprobaciones, en verde.
- Los cuatro días, contra la compuerta (un guion de la carpeta de trabajo de la sesión, `cuatro_dias.py`, que solo imprime recuentos):
  `casos_reservados(repo)` 34 claves y `casos_ocultos(repo)` 34 claves; **0** que nombren 2026-04-13,
  2026-07-02, 2026-07-03 o 2026-07-14. Los cuatro están entre los **76 días** de
  `dias_de_construccion(repo, criterio, construccion)`; `construccion` = 2026-04, 2026-07, 2026-08,
  2026-01 (`criterio_fidelidad.yaml`).
- No se ha abierto ninguna transcripción ni ningún fotograma: la voz se cita de VIDEO-JULIO.md §4 y §7.

### 0.2 Qué da cada pieza (medido en el código; las salidas, sobre `cuenta-por-mes.txt`)

**`Evento` del intérprete** (`engine/interprete.py:117-131`; el otro `Evento` es el de `llenado.py`,
del broker): `disparadas` (lista ORDENADA, en el orden en que dispararon dentro del evento),
`caducados`, `empates`, `fijados` (regla, hecho, valor), `no_implementadas` (regla, primitiva),
`bloqueadas` (regla que INTENTA, `accion:<nombre>`, `prohibida:<efecto>` o `gate desconocido:<efecto>`),
`prohibidos` y `permitidos` (conjuntos de EFECTOS, sin la regla que los fija). Cierto lo del encargo,
con un matiz de línea: `prohibidos.update(...)` en `:260`; `prohibidos: set` está en `:130` (la `:129`
es `bloqueadas`).
- **Solo hay UN efecto con consecuencias mecánicas**: `abrir_operacion`, que lleva la acción
  `colocar_orden_limite` (`strategy_spec.yaml:448`, la única `efecto:` de las acciones). `buscar_entradas`
  se prohíbe (RN-001, RN-033, RN-029, RN-031) y se permite (RN-017, RN-021), pero ninguna acción lo
  lleva: prohibirlo no bloquea nada. Así que «el gate que fija cada prohibición» es, en la práctica,
  qué gates prohibían `abrir_operacion` cuando RN-015 intentó colocar.
- **El gate se puede saber sin tocar el intérprete**: un evento recorre las reglas a punto fijo; en
  cada pasada los gates van primero (`CLASES_EN_ORDEN`, `:33`) y la que dispara se apunta en
  `disparadas` en orden (`:343`). Los gates que prohibían el efecto cuando RN-015 lo intentó son los
  que están en `disparadas` ANTES que RN-015 y lo llevan en su `prohibe` (de la spec). Con
  `gate desconocido`, los gates de clase `gate` con una entrada en `no_implementadas` que lo prohíben.

**`TrazaSesion`** (`engine/motor.py:205-218`): `fijados` (instante, regla, hecho, valor),
`no_implementadas`, `bloqueadas`, `anotaciones`, `disparadas` (CONJUNTO por sesión: se pierde el orden
y el instante), `empates`. Cierto lo del encargo. Lo que pierde frente al `Evento`: el instante de las
bloqueadas y el orden de las disparadas; por eso la bitácora se engancha al evento, no a la traza.

**`ResultadoDia`** (`motor.py:221-225`): `dia`, `operaciones` (formato del criterio), `sesiones`
(nombre → `TrazaSesion`). Nada de tomas, escenarios ni zonas.

**Dónde vive lo que el visor no enseña** (`engine/zonas.py`), todo en `EstadoDia.memoria["zona_de_entrada"]`:
- por sesión (`por_sesion[<sesion>]`): `toma` (instante, nivel, lado, `pivote` = (lado, nivel,
  formado_en)), `escenarios` (lista de `{n, toma, zonas, terminado}`), `puntos` (clave del punto → id
  de zona), `punto_de_zona`, `usadas`, `rechazados`, `esquema`, `zona_id`;
- del día: `zonas` (id → `Zona`: lado, entrada, extremo, por, desde, formada).
- **Se abre un escenario** en `zonas.acciones_escenario.abrir_escenario` (`zonas.py:269-315`, la acción
  de RN-004; envuelta por `primitivas_broker.abrir_escenario`, `:706-724`, que retira la pendiente si
  `orden_pendiente = se_retira`), y el primero también en `_anotar_toma` (`:244-256`).
- **Se liga una zona** en `zona_del_punto` (`:363-412`, con la vida de la orden stop) o en
  `toca_colocar_orden_limite` con el esquema (`:512-522`); las dos, por `_ligar_al_escenario` (`:259`).
- **Se coloca una orden** en `primitivas_broker.colocar_orden_limite` (`:611-663`): el camino «no se
  envía» por el lote (`:632-643`, `ctx.no_enviadas`), el envío al broker (`:652`) y el rechazo al
  colocar (`:657-661`). En `cableado.MotorCableado.correr_dia` el evento se crea en `:391` y es local
  al bucle: de ahí no sale nada más que lo que se copia a la `TrazaSesion` (`:399-405`).

**Las secciones de `motor arnes --simular`** (`cuenta-por-mes.txt`, 588.978 bytes, 3.527 líneas):
`# Arnes del motor`; `## Criterio de fidelidad`; `## Embudo sobre el grafo de hechos`; `## Reglas
disparadas por sesion`; `## Avisos de orden dentro de una clase`; `## RN-003 al abrir la sesion`;
`## Por sesion`; `## Diferencias por operacion` (resumen, embudo y por operación); `## Simulacion`
(cuentas por mes, eventos del broker, órdenes, no enviadas, rechazos, peticiones, freno, cierres);
`## El metodo de ADR-0092` (posiciones, fidelidad por criterios, material sin vídeo, rentabilidad).
La comparación de la ablación no las escribe: usa en proceso las operaciones del bot, las del trader y
el emparejamiento del criterio (ADR-0043: 3 puntos, 15 min), y el recuento de órdenes del broker.

### 0.2b La tensión de 07-03, medida en el código antes de correr nada

**El bot no coloca sus órdenes en «la ruptura de un breaker de M1».** Con los parámetros vigentes
(`cargar_registro`, hoy): `orden_limite_nace = al_aparecer_punto_de_breaker`,
`orden_stop_punto = ultimo_pivote_m1`, `caja_se_fija = en_cada_cierre_m1`, `caja_bloque = r6`,
`liquidez_m15_criterio_toma = cuerpo`, `liquidez_m15_mecha_que_vuelve = solo_la_contraria` y
`breaker_m1_criterio_ruptura = mecha`. Con `al_aparecer_punto_de_breaker`, la zona de cada orden la da
`zona_del_punto` (`zonas.py:363-412`): el ÚLTIMO pivote de M1 contrario a la entrada
(`domain/estructura_m1.ultimo_punto_de_ruptura`, `:201-224`) y la caja R6 desde su vela; la orden es
una STOP en ese punto, que se llena en el tick que lo toca. Ese camino **no lee
`breaker_m1_criterio_ruptura`**. Lo leen solo `_esquema` / `se_da_esquema` (`zonas.py:455-464`,
`:503`, `:535`), que en la vida de la orden stop solo usa RN-008 (`strategy_spec.yaml:1536-1537`), y
RN-008 no prohíbe nunca porque su `ninguno_de` lleva `la_orden_nace_antes_del_esquema`, que da SÍ con
`al_aparecer_punto_de_breaker` (`zonas.py:561-566`); RN-008 es una de las 11 que no disparan. La
nota de RN-008 lo dice así: «con orden_limite_nace = al_aparecer_punto_de_breaker esta regla NO FRENA
LA COLOCACION de la orden stop. Prohibe abrir sin esquema, y la orden stop solo abre cuando el precio
rompe el punto, que es el esquema 1» (`strategy_spec.yaml:1528-1531`). Es decir, para la spec, la
ruptura del punto por el precio, que llena la stop en el tick que lo toca, ES el esquema 1.

Consecuencia para (i)-(iii) de «La tensión de 07-03»:
- **(i) la toma de M15** se mide tal cual: RN-004 la exige con cuerpo (`cruza` con
  `liquidez_m15_criterio_toma = cuerpo`); la bitácora da su nivel, su instante y la M1 que la toma;
- **(ii) «qué breaker de M1 formó su esquema y si rompió con mecha o con cuerpo»** no tiene un
  objeto en el motor de hoy: no hay esquema ni breaker que valide la orden. Lo que sí hay, y la
  bitácora puede dar: el PUNTO (nivel y la vela contraria que lo forma), la caja, la orden stop y su
  llenado; y, al cierre de la M1 del llenado, si esa M1 cerró pasado el punto (con cuerpo) o solo lo
  tocó con la mecha. Esa línea va con el instante del cierre de esa M1, nunca antes;
- **(iii) si la línea rota venía de M15**: la bitácora compara, en el instante en que se liga la
  zona, el nivel del punto con el de la toma y con la liquidez de M15 de cada lado que el motor ve en
  ese instante (`DatosMercado.liquidez_m15`), igualdad en puntos.
Las clases de la tensión hay que releerlas con esto (decisión 2).

### 0.3 Lo que decide el motor y no es una regla RN (la ablación no lo ve)

| Decisión | Dónde | Qué hace |
|---|---|---|
| La toma es la misma liquidez | `zonas.py:293` | RN-004 vuelve a fijar la toma en cada M1 pasada la línea; si el pivote es el mismo, no abre escenario |
| `intentos = siguen_los_que_quedan` | `zonas.py:300-308` | una toma nueva con el escenario vivo lo sigue, con sus intentos |
| `max_escenarios_por_sesion` (A-52) | `zonas.py:310-311` | la toma no abre otro escenario |
| Escenario terminado | `zonas.py:490` | sin colocación hasta otra liquidez de M15 |
| Zona usada / punto rechazado | `zonas.py:496-497`, `primitivas_broker.py:253-254` | la caja o el punto no se vuelven a colocar |
| El punto gastado o liberado tras un cierre | `cableado._el_punto_tras_el_evento` (`:164-191`) | el rechazo al llenar gasta el punto; una pérdida lo libera |
| El lote no llega o no cabe (ADR-0081) | `primitivas_broker.py:632-643` | la orden no se envía; zona usada y punto gastado |
| El broker rechaza al colocar o al llenar | `broker.py` (`_colocar`, `_aplicar`) | rechazo; punto gastado |
| Los cartuchos | `primitivas_broker.cartuchos` (`:385-401`) | el acumulador que lee RN-016 (el freno SÍ es regla) |
| La racha de RN-036 | `engine/racha.py` | el acumulador que lee RN-036 |
| La cuenta y FTMO (ADR-0050) | `engine/cuenta.py` | suspensión de la cuenta: no es un gate RN |
| El freno de peticiones (ADR-0067) | `engine/freno.py` | corta peticiones al servidor |
| Los cierres de mercado (ADR-0068) | `broker._prohibido_por_cierre` | cancela o prohíbe por calendario |
| La red de seguridad del fin del día | `cableado.py:421-430` | cierra y cancela lo vivo |
| El escenario en el que cae una zona, el desempate dentro de una clase | `zonas.py:259`, `interprete.py:161` | por id |

La bitácora sí ve estas (las lee de la memoria del día y del contexto); la ablación solo puede quitar
reglas.

### 0.4 El diseño que propongo

**La bitácora (un observador pasivo).** Un campo nuevo y opcional en `MotorCableado`,
`observador: Callable[..., None] | None = None`. Con `None` (siempre, salvo el subcomando nuevo) el
motor es el de hoy, byte a byte. Con él, `correr_dia` lo llama una vez por cierre de M1, justo después
de copiar el evento a la traza (`cableado.py:405`), con el día, el instante, la sesión, el `Evento`, el
`EstadoDia`, el broker y el contexto. No devuelve nada y el motor no lee nada suyo. Escribe, por día y
sesión, solo lo que CAMBIA en ese cierre (texto determinista, cada línea con el instante del cierre de
M1 en que el motor lo supo):
- la toma de M15 (nivel, lado, pivote y su `formado_en`, la M1 que la toma: apertura, máxima, mínima,
  cierre y si cerró pasada la línea, es decir, con cuerpo) y el escenario que abre, sigue o no abre
  (con la decisión de 0.3 que lo explica);
- cada zona nueva (id, escenario, punto, caja: 0 y 1, su `formada`);
- cada intento de RN-015: colocada (id de orden, precio, stop, objetivo, lote), no enviada (motivo de
  ADR-0081), rechazada (motivo), o BLOQUEADA con los gates que prohibían `abrir_operacion` en ese
  evento (0.2), todos;
- las zonas que tocaba colocar y no se colocaron, con su porqué (usada, punto rechazado, escenario
  terminado);
- los frenos que se encienden o se apagan, los cierres de las órdenes y sus llenados (los eventos del
  broker de ese tramo, ya en `TrazaBroker.eventos`).
Sin mirar al futuro: solo lee lo que el motor ya tiene en ese cierre. La M1 del llenado de una orden
stop se describe en la línea del cierre de esa M1, no en la del llenado. Se escribe en
`data/diagnostico-decisiones/` (ignorada: `/data/*` en `.gitignore`) y los cuatro días se copian al
anexo `docs/validation/anexos/TRAZAS-ABLACION/`.

**La ablación (genérica).** El subcomando carga las reglas como `motor arnes`
(`reglas_ejecutables(cargar_reglas(spec))`, `cli.py:2417`) y, para cada id pedido, pasa a
`MotorCableado` la lista SIN esa regla (filtrada por id, sin ningún caso especial). La spec y su sha no
se tocan. Un id que no sea VIGENTE (DESCARTADA o inexistente) da `ERROR` con su nombre antes de leer
una vela. Sin `--ablacion`, la lista es la de `motor arnes` (un test lo compara).
Comparación, en proceso, contra la corrida base del MISMO proceso (sin ablación, con la cuenta por
mes): por día y sesión, las parejas trader-bot del criterio (ADR-0043) que se ganan y se pierden, las
operaciones del bot sin pareja que aparecen y desaparecen, el delta de órdenes colocadas, y si la
corrida falló (con el error) o se detuvo. Nada de R, PnL ni porcentajes. Las filas de §8 de
RECORRIDA-CONSTRUCCION-2 se cruzan después, en el informe, por día, sesión y operación.

**El subcomando: `motor decisiones`** (otro nombre si prefieres). Opciones propias, sin
`_opciones_diagnostico` ni `_opciones_simulacion`: `--meses` (por defecto, `construccion`),
`--bitacora AAAA-MM-DD[,...]`, `--ablacion RN-NNN[,...]` o `--ablacion-vigentes` (las 32), y
`--carpeta` (por defecto `data/diagnostico-decisiones/`; debe estar dentro de `data/` y se niega
cualquier otra). Siempre simula, con el perfil y la fase por defecto, sin `--depuracion`. **No puede
habilitar medir** porque no llama a `arnes.informe` ni a `habilita_medir`: no produce veredicto ni
las secciones del método; y no escribe donde escribe una corrida que cuenta porque solo escribe en su
carpeta de `data/` y sus ficheros llevan `DIAGNOSTICO` en el nombre. `motor arnes` y `motor visor` no
cambian: ni su parser, ni `OPCIONES_QUE_NO_CAMBIAN_LA_CORRIDA` (`arnes.py:80-82`), ni el test de
`test_diferencias_por_operacion.py:341-361`.

**El nombrado y la etiqueta.** Cada línea empieza por `DIAGNOSTICO-DECISIONES | ` y cada fichero se
llama `bitacora.DIAGNOSTICO.<dia>.txt` o `ablacion.DIAGNOSTICO.<id o vigentes>.txt`, con una función
propia del módulo nuevo; un test lo exige. Además (punto 1 de las decisiones) propongo endurecer
`nombre_etiquetado` (`diagnostico.py:169-185`): hoy acepta cualquier etiqueta que empiece por
`DIAGNOSTICO-A`, así que «DIAGNOSTICO-ABLACION» saldría `aBLACION` en silencio.

**Dónde vive el código.** `src/botsito/engine/decisiones.py` (la bitácora, el filtro de la ablación y
la comparación) y el subcomando en `cli.py`; `cableado.py` solo gana el campo y la llamada.

**El tiempo y la memoria.** La línea base: 339,5 s y 635,6 MiB de pico (RECORRIDA-CONSTRUCCION-2.md:354).
Corridas: (1) `motor arnes --simular` para el diff de 0 bytes, ~340 s; (2) `motor decisiones` con la
base, la bitácora de los cuatro días y las 32 ablaciones en un proceso. Si cada corrida vuelve a
cargar velas y ticks, 33 × ~340 s ≈ 3 h 7 min, o unas 4 h al ritmo del precedente en proceso
(452,1 y 428,5 s, ACTIVAR-SESION-06-MOTOR.md:128-129); cargando el mercado una vez y reutilizándolo
(las corridas no lo modifican), menos: cuánto, no lo he medido (no he corrido el arnés hoy). El pico
del último `make check` (el de la apertura, 29561ef): **310 MiB** en `test` (3343 passed, 22 min 16 s).
Las corridas van una a una y nunca junto a un `make check`.

**Frente al guion que ya existe** (`docs/validation/anexos/VISOR-CONSTRUCCION/traza_por_cierre.py`,
404 líneas, y `resumen_gates.py`; herencia H1 del auditor): ese guion ya mira lo mismo sin tocar
`src/`, sustituyendo en el proceso `Interprete.evento`, `Interprete.evaluar` (los tres predicados de
RN-004 y el pivote de M15) y `cableado.primitivas_cableadas`; cada envoltura llama al original y
devuelve lo mismo, y al final compara sus órdenes con las de main (sale con 3 si difieren). Su
límite es el que el encargo señala: corre UN día suelto, como el visor, desde el capital. Lo que
cambia aquí: (1) un campo con nombre en `MotorCableado` en lugar de sustituir métodos de clase (una
sustitución de `Interprete.evento` vale para todo el proceso, también para las corridas de la
ablación, que no deben llevarla); (2) la corrida entera con la cuenta por mes; (3) gates, tomas,
escenarios, zonas y órdenes en una sola salida; y (4) el subcomando, con tests. De él reutilizo la
idea de comparar las órdenes con y sin observador, que pasa a test.

### 0.5 Herencias

Búsqueda de «rama de trazas», «trazas del motor», «ablación», «R4.4» y «pendiente con dueño» en
PROJECT_STATE, el final de HISTORIA, `docs/validation/`, `docs/adr/` y `docs/plan/` (auditor):

| Herencia | Dónde | Entra |
|---|---|---|
| La pendiente con dueño: 07-14 11-15 (o10, o12 y o14, ¿mismo barrido?) y lo no comprobable de 04-13 y 07-02 | RECORRIDA-CONSTRUCCION-2.md:1355-1358 (allí «F, punto 2; R4.x»; hoy F (1) y R4.4, HISTORIA) | sí, F5 |
| 04-13 07-11 a las 08:47 (zona:59, RN-015 «no», sin posición viva) y 07-02 11-15 a las 12:25 y 12:45 | RECORRIDA-CONSTRUCCION-2.md:1282-1283 | sí, F5 |
| Las 5 de 07-03 07-11 y las 13 «a la rama de trazas»; 07-02 14:10 y 14:23 | VIDEO-JULIO.md:606-610, :649, :657-661 | sí, F5 |
| La nota para P5 (el punto 4 de §10; no hay un encabezado «10.4») | VIDEO-JULIO.md:808-810 | sí, como límite de la salida |
| R4.4 y RUMBO §2 | HOJA-DE-RUTA.md:400-411; RUMBO-2026-11.md:25-27 | sí |
| **H1** `traza_por_cierre.py` y `resumen_gates.py`, ya revisados | VISOR-CONSTRUCCION.md:235, :314-319, :369, :498 | sí, como precedente (arriba) |
| **H2** la deuda de la zona reutilizada en un escenario nuevo, cuyos cierres cuentan en los cartuchos del escenario en que nació: «hace falta la traza por cierre» | PROJECT_STATE.md:97 (entera en HISTORIA); ADR-0083:230; PUNTO-USADO.md:590 y :610 | sí: la bitácora dice el escenario de cada zona y de cada cierre; es la primera hipótesis para 07-14. La deuda no se paga aquí (cambiaría lo que el motor decide) |
| **H3** la carpeta de salida sale de un argumento, nunca de `__file__` ni de una ruta fija | CLAUDE.md, «Ensayos aislados», regla 2; ERRORES-RECURRENTES.md:115 | sí: `--carpeta` |
| **H4** un test «sobre un mes de construcción» corre en cada `make check`: abril calienta con marzo y julio con junio (días reservados); agosto, con julio (construcción) | PROJECT_STATE.md:101 y :103; ADR-0021 §4 | decisión 4 |

### 0.6 El recorte (candidatos de F1)

`PROJECT_STATE.md` en `main`: 23.805 bytes (en la rama, con la apertura: 23.876). Por sección (bytes con salto):
Next Action 6.451, Known Ambiguities 1.702, **Technical Debt 12.755**, Reglas vivas 1.599, el resto
menos de 220 cada una.
- **(e):** las líneas de Technical Debt de más de 200 bytes aún sin acortar son **22** (bytes con el
  salto; recuento abajo). Las que ahorran 60 bytes o más (unas 271 o más): **9** —L83 (322), L84 (301), L89
  (325), L90 (285), L91 (447), L92 (282), L93 (498, ADR-0088), L139 (456, copia de las crudas) y L143
  (707, panel de FTMO)—. Suman 3.623 bytes; acortadas a 160 bytes como mucho más la marca (unos
  51), quedarían en unos 1.900-2.000: un ahorro del orden de **1,6-1,7 KB**. La cifra exacta sale de
  F1, porque cada corte va al final de una frase o de un inciso y algunas conservan la cita.
  Mi primer recuento dio 25, y estaba mal: buscaba la marca con su paréntesis
  «(entera en HISTORIA, …)», y tres ya acortadas (L81, L115, L124) la llevan detrás de su cita
  («…; entera en HISTORIA, Technical Debt ACORTADA)»). Sin ellas son **22**, como dicen el encargo y
  el auditor.
- **(a)-(d):** ninguna sale a primera vista. Las dos que miré: el ADR 0087 de S-15 sigue sin existir (`docs/adr/`
  salta de 0086 a 0088), así que la línea de los `ids-inexistentes` se queda; y la nota de RN-019
  sigue diciendo que A-31 lo pregunta (`strategy_spec.yaml:2024`), así que esa también se queda. F1
  las mira todas, negando por defecto.

### 0.7 El encargo frente al repo (auditor-encargo, informe tal cual en el Apéndice A)

54 afirmaciones: 46 correctas, 0 incorrectas, 8 con matiz. Los que tocan el trabajo:
- **(28) El control de las 11.** «No dispara» es que nunca da SÍ; un gate en DESCONOCIDO mete su
  efecto en `quizas_prohibidos` y bloquea sin disparar (`interprete.py:273-275`, `:330-335`). Lo que
  respalda el cero en la línea base («cuantas se paran en cada primitiva NO_IMPLEMENTADA: ninguna»,
  `cuenta-por-mes.txt:26-27`) se midió en las 104 sesiones con trader, no en las 152. La corrida base
  de la ablación lo medirá en todas (recuento de `no_implementadas` por regla) antes de las 32.
  Y otra razón por la que el control no es trivial, medida en el código: una regla que no dispara se
  EVALÚA en cada cierre, y su evaluación puede tocar la memoria del día. RN-008 evalúa `se_da_esquema`
  (`strategy_spec.yaml:1535-1537`), que pasa por `_esquema` → `_anotar_toma`, que puede abrir el
  primer escenario y guarda `esquema` (`zonas.py:244-256`, `:331-355`). Si quitar RN-008 da delta, sale
  de ahí, y la PARADA lo dirá.
- **(48) R4.4 HECHA:** `problemas_b` lee las referencias del BLOQUE entero (`test_hoja_de_ruta.py:139-141`),
  no solo de «Refs:»: NA:F no puede aparecer en ningún sitio de la entrada.
- **(51) El Marcador:** HOJA-DE-RUTA.md:817 pide una fila a cada rama que corra el arnés sobre toda la
  construcción. El encargo la quita; queda escrito como excepción (decisión 5).
- **(42) El tiempo:** el precedente en proceso tardó 452,1 y 428,5 s (ACTIVAR-SESION-06-MOTOR.md:128-129);
  34 corridas a ese ritmo, unas 4 h.
- **(50) La rama de la CI:** `RITUAL.md:103` da `fix/trazas-ablacion` (`trabajo/<rama>:refs/heads/fix/<rama>`);
  el encargo escribe `fix/trabajo-trazas-ablacion`. Uso el de RITUAL salvo que digas otra cosa.
- Matices de cita sin efecto: arnes.py:74-82 (el `frozenset` en :80-82, el comentario desde :74);
  el test de :341-361 acaba en :357; `prohibidos` está en :130 (la :129 es `bloqueadas`).
- PROJECT_STATE: 23.805 bytes en `main`; 23.876 en la rama tras la apertura. «Antes» de F1 es el de la
  rama, y se dicen los dos.

### 0.8 Lo que no pude medir

- Si alguna de las 11 da DESCONOCIDO en las 48 sesiones sin trader: exige correr el motor (lo hace la
  corrida base de F4).
- Cuánto de los ~340 s es cargar velas y ticks y cuánto correr: no he corrido el arnés hoy.
- Que la repetición de la base dé 0 bytes depende también de `data/`, fuera de git.

### 0.9 Exposiciones del día

La fila de HOLDOUT-EXPOSICIONES del 2026-11-09, escrita antes del primer `make check`: el M1 de marzo
y de junio de cada `make check`; ninguna corrida del arnés; sin transcripciones ni fotogramas.

## Lo que necesito que decidas (fase 0)

0. **El diseño de la bitácora.** Opciones: (a) un campo `observador` opcional en `MotorCableado`,
   llamado tras cada evento; los gates se sacan del orden de `Evento.disparadas` y del `prohibe` de la
   spec, sin tocar el intérprete; (b) un campo nuevo en el `Evento` del intérprete con la regla de
   cada prohibición; (c) sustituir métodos en el proceso, como `traza_por_cierre.py`. Recomiendo (a):
   es exacto para los gates que dan SÍ, no cambia el intérprete y no afecta a las corridas de la
   ablación del mismo proceso. Coste de (b): tocar el intérprete, que comparten todas las corridas.
   Coste de (c): la sustitución vale para todo el proceso.
1. **La etiqueta y el nombre del fichero.** Opciones: (a) etiqueta propia `DIAGNOSTICO-DECISIONES` y
   un nombrado propio, Y además endurecer `nombre_etiquetado` para que «DIAGNOSTICO-A» tenga que ir
   seguido de un número (un test con «DIAGNOSTICO-ABLACION» que falle); (b) solo la etiqueta y el
   nombrado propios, sin tocar `diagnostico.py`. Recomiendo (a): el defecto que señalas existe hoy
   y cuesta un test. Coste de (b): el defecto sigue latente.
2. **(ii) de «La tensión de 07-03»** (0.2b): en el motor de hoy no hay breaker que valide la orden;
   la orden es una stop en el último pivote de M1. Opciones: (a) la bitácora da, por cada orden de
   07-03 07-11, la toma (i), el punto con su vela y la M1 del llenado con o sin cuerpo (en lugar de
   «el breaker»), y si la línea es de M15 (iii); y releo las clases así: «error nuestro» si el punto
   o la toma tratan como de M1 una línea de M15; «contradicción con lo fijado» si el punto es un pivote
   de M1 y la orden se llenó con una mecha; (b) mantener las clases como están escritas y declarar (ii)
   «sin objeto». Recomiendo (a): mide lo que el motor hace de verdad. Coste de (b): ninguna fila
   saldría en «contradicción» por definición.
3. **El nombre y las opciones del subcomando.** Propongo `motor decisiones` con `--meses`,
   `--bitacora`, `--ablacion` / `--ablacion-vigentes` y `--carpeta` (dentro de `data/`), siempre con
   simulación, perfil y fase por defecto y sin `--depuracion`. Opciones: (a) así; (b) otro nombre.
   Recomiendo (a).
4. **El mes de los tests de F2 y F3** (H4). Opciones: (a) los tests de `make check` sobre el
   fixture sintético de `test_cableado.py` (sin velas reales: ni marzo ni junio), y la prueba sobre
   la construcción entera es la corrida de F4 (diff de 0 bytes y bitácora con y sin observador); (b)
   un test sobre agosto real (calienta con julio, construcción), que en la CI de Linux se salta por
   falta de `data/`; (c) sobre abril o julio. Recomiendo (a): no añade lecturas de días reservados a
   cada `make check`. Coste de (b): unos minutos más en cada `make check` y un test que la CI no
   ejecuta. (c) añade una lectura de marzo o de junio a cada `make check`, para siempre.
5. **La fila del Marcador** (auditor, 51). Opciones: (a) sin fila, declarado en el informe como
   excepción a HOJA-DE-RUTA.md:817 (la base repite la línea base y lo demás es diagnóstico), para que
   lo diga la orden de cierre; (b) una fila. Recomiendo (a), como pide el encargo, dicho como excepción.
6. **Las corridas en un proceso.** Opciones: (a) la base, la bitácora de los cuatro días y las 32
   ablaciones en un solo proceso que carga velas y ticks una vez; (b) un proceso por ablación.
   Recomiendo (a) si la memoria lo permite: mido la carga y el pico en la corrida base y, si pasa de
   ~1,5 GiB, paso a (b) y lo digo. Coste de (b): unas 3-4 h.

## Apéndice A · El informe del auditor del encargo (fase 0, 2026-11-09), tal cual

> ## Auditoría del encargo · trabajo/trazas-ablacion · 2026-11-09
> Resumen: 54 afirmaciones: 46 correctas, 0 incorrectas y 8 con matiz. Hay 4 herencias que el encargo no recoge.
>
> Encargo: `C:\Users\USER\Desktop\Bot v3\docs\encargos\trabajo-trazas-ablacion.md`. Contrato: `C:\Users\USER\Desktop\Bot v3\contrato.yaml`. No escribí nada. No lancé make, pytest ni el arnés. No abrí holdout, transcripciones ni fotogramas.
>
> ### Afirmaciones
> | # | Afirmación (literal del encargo) | Veredicto | Evidencia |
> |---|---|---|---|
> | 1 | «main y origin/main en 144e42c … merge 129ea33, tag stable/F38u-video-julio (el último «- Tag:» de HISTORIA)» | CORRECTA | `git rev-parse main origin/main` da 144e42c24d… las dos veces. `for-each-ref --points-at 129ea33` da `refs/tags/stable/F38u-video-julio`. El último «- Tag:» está en HISTORIA.md, en el registro de video-julio (~16480). |
> | 2 | «CI de main sobre 144e42c: run 42681006516 en verde» | CORRECTA | `gh run view 42681006516`: conclusion success, headBranch main, headSha 144e42c24d… |
> | 3 | «ninguna otra rama local ni remota» | CORRECTA | `git branch -a`: main, trabajo/trazas-ablacion, origin/main y origin/HEAD. |
> | 4 | «PROJECT_STATE.md, que está en 23.805 bytes con tope 25.000» | CORRECTA | `git show main:PROJECT_STATE.md \| wc -c` da 23805. TOPE_BYTES = 25_000 en tests/unit/test_project_state.py:21. Nota: tras la apertura, el de la rama mide 23.876 (`wc -c`). La cifra «antes» de F1 tiene que decir de cuál de los dos habla. |
> | 5 | «07-03 … el día de las 5 filas de «error nuestro (sospecha)» de VIDEO-JULIO.md §4.1 y de 2 de las 13» | CORRECTA | VIDEO-JULIO.md:609 (P2 + P5×4 = 5). Las 13 están en :660-661 («07-03 11-15 ×2»). |
> | 6 | «Registro es el de parámetros (ADR-0002), y TrazaSesion y trazas_broker son del motor» | CORRECTA | docs/adr/0002-registro-de-parametros-una-sola-puerta.md. motor.py:206. cableado.py:280. |
> | 7 | «breaker_m1_criterio_ruptura sigue en mecha» | CORRECTA | parametros.yaml:517-518 (CONFIRMED, "mecha"). |
> | 8 | «OPCIONES_QUE_NO_CAMBIAN_LA_CORRIDA (src/botsito/engine/arnes.py:74-82)» | CORRECTA | Comentario en :74 y frozenset en :80-82. |
> | 9 | «test_la_seccion_no_anade_ninguna_opcion_al_comando (tests/unit/test_diferencias_por_operacion.py:341-361)» | MATIZ | El test va de :341 a :357 (`]  # fmt: skip`). Lo que dice es correcto: la lista cerrada y las 13 opciones de `motor arnes`. |
> | 10 | «no comparte _opciones_diagnostico» | CORRECTA | cli.py:2282. Lo usan `motor arnes` (:3094) y `motor visor` (:3120). |
> | 11 | «RECORRIDA-CONSTRUCCION-2.md y VIDEO-JULIO.md son informes cerrados» | CORRECTA | Están en main. El contrato los protege (contrato.yaml:30-33). |
> | 12 | «una NOTA en ADR-0092 §6 … como la NOTA de §8» | CORRECTA | La NOTA de §8 existe (ADR-0092:207). §6 no tiene NOTA todavía (:160-170). |
> | 13 | «El contrato cubre exactamente eso» | CORRECTA | contrato.yaml:5-15: engine/, cli.py, tests/, el informe y su anexo, HOLDOUT, ADR-0092, encargos, HISTORIA y PS. |
> | 14 | «por la compuerta del arnés (dias_de_construccion y casos_ocultos) … casos_reservados(repo)» | CORRECTA | arnes.py:139. cases/holdout.py:351 y :456. |
> | 15 | «Cada corrida del arnés y cada make check calientan con el M1 de marzo y el de junio (Technical Debt)» | CORRECTA | La línea de TD «`arnes.dias_de_mercado` lee para calentar el M1 entero de marzo y de junio…» de PROJECT_STATE. |
> | 16 | «nombre_etiquetado (:169-185) solo admite etiquetas que empiecen por «DIAGNOSTICO-A» o por la de la cuenta, y una «DIAGNOSTICO-ABLACION…» pasaría en silencio» | CORRECTA | diagnostico.py:161 (`PREFIJO_ETIQUETA = "DIAGNOSTICO-A"`) y :169-185. «DIAGNOSTICO-ABLACION-RN-007» saldría como `aBLACION=RN-007`, sin error. |
> | 17 | «La nota para P5 (VIDEO-JULIO.md §10.4)» | MATIZ | No existe ningún «10.4» como encabezado. Es el punto 4 de §10 (VIDEO-JULIO.md:808-810). El repo ya lo cita así (HISTORIA, registro de video-julio; VIDEO-JULIO.md:1655). El contenido es correcto. |
> | 18 | «TrazaSesion (src/botsito/engine/motor.py:206-214) lleva hechos fijados, primitivas no implementadas, acciones bloqueadas, reglas disparadas, anotaciones y empates» | CORRECTA | motor.py:206-214. |
> | 19 | «acumula los prohibidos como un conjunto de efectos, sin la regla (interprete.py:129 y :260); `bloqueadas` lleva la regla que intenta la acción» | MATIZ | `prohibidos: set[str]` está en :130. La :129 es `bloqueadas`. La :260 es correcta. Que `bloqueadas` lleve la regla que intenta la acción es correcto: `evento.bloqueadas.add((regla.id, …, f"prohibida:{efecto}"))` en :271. |
> | 20 | «El visor no nombra las tomas de M15 ni los escenarios, y de los gates solo enseña los frenos» | CORRECTA | RECORRIDA-CONSTRUCCION-2.md:1246-1252. |
> | 21 | «El visor empieza cada día desde el capital (F3.4 (a)) … En 07-15 dieron órdenes distintas» | CORRECTA | RECORRIDA-CONSTRUCCION-2.md:1254-1258 (o25 a o29). |
> | 22 | «el arnés lleva una cuenta por mes (ADR-0092 §8)» | CORRECTA | ADR-0092:195-224. |
> | 23 | «cuenta-por-mes.txt, de `uv run botsito motor arnes --simular --salida <fichero>` (RECORRIDA-CONSTRUCCION-2.md:354: 339,5 s y pico de 635,6 MiB)» | CORRECTA | RECORRIDA-CONSTRUCCION-2.md:354. |
> | 24 | «El fichero no lleva sha, tiempo ni memoria … diff de 0 bytes» | CORRECTA | `grep -c "TIEMPO\|MEMORIA\|sha256\|MiB"` da 0. Ya se repitió una vez con diff=0 (RECORRIDA-CONSTRUCCION-2.md:356 y :361). |
> | 25 | «F38t y F38u no tocaron src/» | CORRECTA | `git diff --stat stable/F38s-cuenta-por-mes main -- src knowledge/spec knowledge/cases knowledge/cuentas config pyproject.toml uv.lock` sale vacío. `material_sin_video` sale de criterio_fidelidad.yaml, que tampoco cambió. Lo que está fuera de git (velas y ticks) no se puede comprobar. |
> | 26 | «11 de las 32 reglas VIGENTE no disparan nunca … RN-007, -008, -010, -019, -020, -021, -022, -026, -029, -030 y -031» | CORRECTA | cuenta-por-mes.txt:29-51 lista 21 disparadas, y las 11 restantes son esas. RN-020 aparece una sola vez (:1271), y es el rótulo «TOPE DEL TRADER» de la Simulación, no un disparo. |
> | 27 | «RN-019, además, en Technical Debt y PUNTO-USADO.md §1.h» | CORRECTA | PROJECT_STATE.md:95-96. PUNTO-USADO.md:239-248. |
> | 28 | «Su ablación es el control: tiene que dar delta cero» | MATIZ | «No dispara» quiere decir que nunca da SI. Un gate que da DESCONOCIDO mete sus efectos en `quizas_prohibidos` y bloquea acciones sin disparar nunca (interprete.py:330-334 y :273-275). Lo que respalda el cero es «cuantas se paran en cada primitiva NO_IMPLEMENTADA: ninguna» (cuenta-por-mes.txt:26-27), y eso se midió solo sobre las 104 sesiones con operaciones del trader, no sobre las 152. La fase 0 debería medir que esas 11 tampoco dan DESCONOCIDO. |
> | 29 | «32 reglas VIGENTE (15 gate, 14 disparador, 2 terminal y 1 fallback) y 5 DESCARTADA» | CORRECTA | strategy_spec.yaml, recuento por (estado, clase): exactamente esas cifras. |
> | 30 | «las 32 llegan al intérprete por reglas_ejecutables (interprete.py:363)» | CORRECTA | :363. Ninguna VIGENTE va sin `forma`. Se llama en cli.py:2417 (arnés) y :2509 (visor). |
> | 31 | «Precedente de guion en proceso: medir_f2_f3.py (ACTIVAR-SESION-06-MOTOR.md:118-130), que corría con la cuenta diaria y vivía fuera del repo» | CORRECTA | ACTIVAR-SESION-06-MOTOR.md:118-130. Pero no es el único precedente, ni el más cercano: herencia H1. |
> | 32 | «VIDEO-JULIO.md §4.1 propuso «error nuestro (sospecha)» … por v12 0:00:15-0:00:58» | CORRECTA | VIDEO-JULIO.md:609 y :632-633. |
> | 33 | «la sesión 5 ya respondió A-32 (S-18; ambiguedades.yaml:864-898): «en M1 la mecha siempre vale» …» | CORRECTA | ambiguedades.yaml:864 (id), :869-874 (la respuesta) y :896 (RESUELTA). |
> | 34 | «breaker_m1_criterio_ruptura = mecha, CONFIRMED (parametros.yaml:501-518)» | CORRECTA | :501 nombre; :517-518. |
> | 35 | «T no cruzó su clase con eso» | CORRECTA | En VIDEO-JULIO.md, `grep -c "A-32\|S-18\|breaker_m1_criterio_ruptura"` da 0. |
> | 36 | «el Evento del intérprete (ojo: hay otro Evento en llenado.py)», ResultadoDia, cableado.py | CORRECTA | interprete.py:118. llenado.py:68. motor.py:222. cableado.py:240 y :293. |
> | 37 | «RECORRIDA-CONSTRUCCION-2.md:1355-1358, la pendiente con dueño …» | CORRECTA | :1355-1358. Allí el dueño se nombra como «F, punto 2; R4.x». Hoy es F (1) y R4.4 (HISTORIA.md:16254: «R4.x de la orden es R4.4»). |
> | 38 | «:1283; a las 08:47, RN-011 da zona:59 y RN-015 «no», sin posición viva» | CORRECTA | RECORRIDA-CONSTRUCCION-2.md:1283. |
> | 39 | «:1282: las de 14:10 y 14:23 ya salieron «sí» …; las no comprobables son las de 12:25 y 12:45» | CORRECTA | RECORRIDA-CONSTRUCCION-2.md:1282. |
> | 40 | «las 13 «a la rama de trazas» (07-02 11-15 ×5, 07-03 11-15 ×2 y 07-14 11-15 ×6); y 07-02 14:10 y 14:23, regla desconocida» | CORRECTA | VIDEO-JULIO.md:606, :610, :649, :660-661 y :607. |
> | 41 | «RUMBO §2 y HOJA-DE-RUTA R4.4» | CORRECTA | RUMBO-2026-11.md:25-27. HOJA-DE-RUTA.md:400-411 (Refs NA:F · ID:ADR-0092; ABIERTA). |
> | 42 | «32 ablaciones; a unos 340 s cada una, unas 3 h» | MATIZ | Son 34 corridas × 340 s ≈ 3,2 h. Pero el único precedente en proceso tardó 452,1 y 428,5 s (ACTIVAR-SESION-06-MOTOR.md:128-129). Con ese ritmo, ≈ 4 h. |
> | 43 | «docs/state/README.md, «Que sale de PROJECT_STATE…», condiciones (a) a (e)» | CORRECTA | README.md:58-92. |
> | 44 | «(hay 22) … 60 bytes o más en las de unos 271 o más (unas 9; las más largas, panel de FTMO, riesgo residual de ADR-0088, copia de seguridad)» | CORRECTA | Medido sobre PS: 62 líneas de TD. 25 pasan de 200 bytes, y 22 no llevan «entera en HISTORIA». 9 llegan a 271 o más. Las tres mayores miden 706, 497 y 455. Con la lectura «con el salto de línea» (README:89-90) siguen siendo 22: ninguna mide 199-200. |
> | 45 | «Lo que sale o se acorta va al final de HISTORIA, en su bloque por clase, con su texto literal» | CORRECTA | README.md:72-75 y :85-86. |
> | 46 | «La Next Action no se toca aquí: la cambia la orden de cierre» | CORRECTA | README.md:99-102. |
> | 47 | La NOTA de §6: «recuentos … diagnóstico de construcción … las ramas de spec citan al trader (ev-, fb-) … ADR del método (RUMBO §1, rama de la preparación de la sesión 7)» | CORRECTA | ADR-0092:166-170. RUMBO-2026-11.md:13. |
> | 48 | «R4.4 HECHA y sin NA:F en sus Refs, como R3.8 (si no, problemas_b … la da por mala)» | MATIZ | `problemas_b` lee las referencias del BLOQUE ENTERO, no solo de «Refs:» (test_hoja_de_ruta.py:139-141, `referencias(bloque)`). NA:F no puede salir en ningún sitio de la entrada, tampoco en «Estado:». Es el mismo b1 que bloqueó en video-julio (ERRORES-RECURRENTES.md:115). R3.8 sí cumple: no nombra ninguna letra (HOJA-DE-RUTA.md:283-296). |
> | 49 | «el texto nuevo de F (sale el (1); F sigue viva …)» | CORRECTA | PROJECT_STATE.md:28: (1) trazas, (2) láminas, (3) sesión 7. |
> | 50 | «por RITUAL.md se empuja como fix/trabajo-trazas-ablacion … El único fallo aceptado es el de state check» | MATIZ | RITUAL.md:103 escribe `git push origin trabajo/<rama>:refs/heads/fix/<rama>`, que da `fix/trazas-ablacion`. En HISTORIA lo habitual es fix/<nombre>, con solo 2 casos de fix/trabajo-…. Lo del fallo aceptado es correcto (RITUAL.md:105-107). |
> | 51 | «Sin fila en el Marcador … las ablaciones son diagnóstico» | MATIZ | HOJA-DE-RUTA.md:817: «Cada rama que corra el arnés sobre toda la construcción añade su fila en su orden de cierre». La corrida base de esta rama es justo eso. El encargo se aparta de la regla de la hoja sin decir que es una excepción (video-julio no tuvo fila porque no corrió nada: VIDEO-JULIO.md, §10 punto 5). |
> | 52 | Tramo R4 / entrada R4.4 / depende de R3.9 / es la siguiente | CORRECTA | contrato.yaml:4 es igual a HOJA-DE-RUTA.md:315. R4.4 lleva NA:F y depende de R3.9, que está HECHA (:298-313). F pone (1) primero, y R0.3 dice que RUMBO manda en el orden de F (:42-49). |
> | 53 | «F7 #6 y #9 … (antes, «la rama de trazas, si los necesita»)» | CORRECTA | VIDEO-JULIO.md:812 y :943. #6 = v12 0:00:15 (la tabla de §7). #9 = la condición del break even. |
> | 54 | «HOLDOUT-EXPOSICIONES.md lleva una fila por cada día … escrita ANTES …» | CORRECTA | Ya está la del 2026-11-09 (HOLDOUT-EXPOSICIONES.md:128): «Corridas del arnés hoy: ninguna». |
>
> ### Lo que el repo pide y el encargo no recoge
> | # | Qué | Dónde lo pide | Evidencia |
> |---|---|---|---|
> | H1 | Ya hay en el repo un guion revisado que hace casi la bitácora. `traza_por_cierre.py` envuelve `Interprete.evento`, `Interprete.evaluar` (los predicados de RN-004 y el pivote de M15 de la liquidez) y `cableado.primitivas_cableadas` (la zona de cada orden). Saca, por cierre, las disparadas, los efectos prohibidos y las bloqueadas, y compara sus órdenes con las de main (sale con 3 si difieren). Hay también `resumen_gates.py`. Corren como el visor, un día suelto desde el capital: la limitación que el encargo señala en el punto de 07-15. El encargo solo cita medir_f2_f3.py. 0.2 y 0.4 deberían medirse contra este guion. | VISOR-CONSTRUCCION.md:235, :314-319, :369 y :498; CORRIDA-CONSTRUCCION.md:1091 | `docs/validation/anexos/VISOR-CONSTRUCCION/traza_por_cierre.py:1-20` y `resumen_gates.py:1-10` |
> | H2 | Deuda que pide justo esta traza: «Una zona del productor reutilizada en un escenario nuevo … sigue ligada al escenario en que nació y sus cierres cuentan en los cartuchos de aquel … hace falta la traza por cierre». Toca de lleno la pregunta de 07-14: por qué RN-016 no frenó y de qué escenario son o10, o12 y o14. | PROJECT_STATE.md:97 (texto entero en HISTORIA.md:10807); ADR-0083:230; PUNTO-USADO.md:590 y :610 | El encargo pide en 0.5 que todo lo dejado a esta rama entre o se diga por qué no, y no la nombra. |
> | H3 | La salida del subcomando tiene que venir de un argumento, nunca de `__file__` ni de una ruta fija. El encargo solo dice «una carpeta ignorada de data/». | CLAUDE.md, «Ensayos aislados», regla 2; ERRORES-RECURRENTES.md:115 (video-julio a1, que bloqueó) | — |
> | H4 | Los tests «sobre un mes de construcción» de F2 y F3 corren en cada make check. Abril calienta con el M1 de marzo y julio con el de junio, los dos con días reservados. Un test así añade una lectura más de reservados en todos los make check, para siempre, y se declara. Agosto calienta con julio, que es construcción. El encargo no fija el mes. | PROJECT_STATE.md:103 (test_visor y test_preparar_a35 ya leen marzo); PS:101 (calienta con el mes anterior); ADR-0021 §4 | — |
>
> ### Comandos del encargo
> | # | Comando | Existe y se ejecuta así | Evidencia |
> |---|---|---|---|
> | 1 | `uv run botsito motor arnes --simular --salida <fichero>` | Sí | cli.py:3080-3094 (`--salida` obligatoria). `--simular` en `_opciones_simulacion`, cli.py:2334. |
> | 2 | `motor visor` (nombrado, no se ejecuta) | Sí | cli.py:3097-3120 (`--caso` o `--todos`, obligatorio uno de los dos). |
> | 3 | El subcomando nuevo de `motor` | No existe todavía | Su nombre se propone en la fase 0. |
> | 4 | `/model` | No es del repo: es de Claude Code | — |
> | 5 | Comprobaciones del contrato: `uv run botsito state check`, `uv run python scripts/contrato_rama.py`, `make check > make-check.log 2>&1` | Sí | cli.py:2923-2925; scripts/contrato_rama.py existe. |
>
> ### Lo que no pude comprobar
> - Que la repetición de la base dé 0 bytes también depende de data/ (velas y ticks fuera de git). No se puede ver desde git.
> - Si alguna de las 11 reglas «que no disparan» da DESCONOCIDO en las 48 sesiones sin operaciones del trader (punto 28). Medirlo exige correr el motor.
> - Qué frenos o decisiones viven fuera de las reglas RN (el seguidor del tope de RN-020 en cableado.py:447; el sesgo de RN-003 lo anota domain/sesgo.py, cuenta-por-mes.txt:715). Es el 0.3 de la sesión; solo vi que existen.
> - Los cuatro días con `casos_reservados` y `casos_ocultos`: no los ejecuté. Son de abril y julio, meses de construcción, y ACTIVAR-SESION-06-MOTOR.md:115-116 dio 0 en construcción.
> - El PICO DE MEMORIA del último make check: el de la apertura sigue corriendo.
>
> ### Lo más grave
> No hay afirmaciones falsas. Lo que más cambia el trabajo es lo que falta. El repo ya tiene `traza_por_cierre.py`, que observa de forma pasiva `Interprete.evento` y `evaluar` y da el gate por cierre y la toma de RN-004 (H1). El diseño de 0.4 tiene que partir de él y explicar en qué se diferencia: corre en proceso con la cuenta por mes, no día a día. Si no, se rehace a ciegas. Además, la deuda de la zona reutilizada que cuenta en los cartuchos de otro escenario (H2, PS:97) puede ser la respuesta a 07-14, y el encargo no la nombra. Tres matices pueden romper la entrega o la decisión:
> - **El control de las 11 reglas (28).** Que nunca den SI no prueba que no bloqueen: un gate en DESCONOCIDO bloquea vía `quizas_prohibidos`.
> - **R4.4 HECHA (48).** NA:F no puede aparecer en ningún sitio de la entrada, no solo en «Refs:».
> - **El Marcador (51).** La hoja exige una fila por cada corrida sobre toda la construcción. Quitarla tiene que quedar dicho como excepción a HOJA-DE-RUTA.md:817.

## Respuesta del consultor a la PARADA de la fase 0 (2026-11-09)

Copiada tal cual:

> Modelo: Opus 5.5 · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA de la fase 0 de trabajo/trazas-ablacion (2026-11-09). Cópiala tal cual al informe con la skill fase-cero y aplícala punto por punto.
>
> 0. El enganche. Campo observador opcional en MotorCableado para lo que no es del intérprete (tomas, escenarios, zonas, puntos, órdenes): de acuerdo. Pero el gate que prohíbe NO se deduce del orden de las disparadas: se apunta en el intérprete, en el sitio donde se prohíbe. Por qué: deducirlo del orden es la clase de error del revisor a1 de RECORRIDA-CONSTRUCCION-2 (atribuir a RN-032 el bloqueo de RN-015), y no cubre el caso que tú mismo mediste, un gate DESCONOCIDO que bloquea sin disparar: en interprete.py, quizas_prohibidos (:323-335) se rehace en cada pasada y no_implementadas acumula sin la pasada, así que no se puede reconstruir después. Cómo:
>    - el Evento gana un registro de quién prohíbe cada efecto (los gates que dispararon y lo prohibieron, en _ejecutar hacia :260) y, en cada acción bloqueada, qué gates lo hicieron, también los desconocidos de esa pasada (hacia :270-274). quizas_prohibidos puede pasar a llevar los ids, sin cambiar qué se bloquea;
>    - es solo registro: nada lo lee para decidir. Un test lo fija sobre el fixture, con un gate que dispara y uno desconocido prohibiendo lo mismo: salen los dos;
>    - la prueba de que no cambia ninguna decisión es la de F4.1: motor arnes con el código de la rama da un diff de 0 bytes contra cuenta-por-mes.txt.
>    Cambia lo que dije en el encargo (sin tocar el intérprete): lo dejo escrito como desviación decidida por mí.
>
> 1. Etiqueta y nombre: DIAGNOSTICO-DECISIONES con nombrado propio, y nombre_etiquetado arreglado para que «DIAGNOSTICO-A» solo acepte una ambigüedad (A seguida de cifras) y rechace todo lo demás, con su test que rompe en main. De acuerdo.
>
> 2. La relectura de 07-03: de acuerdo con medir el punto, su vela, la vela de M1 del llenado (con o sin cuerpo) y si la línea viene de M15. Añade dos datos por orden:
>    (a) si el llenado ocurrió ANTES o DESPUÉS de la primera vela de M1 que cierra más allá del punto;
>    (b) qué toma de M15 abrió el escenario y si su vela cerró con cuerpo.
>    Las clases propuestas quedan así:
>    - error nuestro: el punto o la toma tratan como de M1 una línea de M15, o la toma de M15 se dio con mecha;
>    - contradicción con lo fijado: el punto es un pivote de M1 y el llenado fue con mecha, contra la voz de v12 y con S-18 a favor del bot;
>    - y, si (a) dice que el bot entra antes de que ninguna M1 cierre más allá, propones además «regla desconocida: cuándo se coloca la orden respecto de la ruptura» (toca ADR-0064 y orden_limite_nace). No se cambia nada: decido yo en la PARADA final.
>
> 3. El subcomando: motor decisiones, de acuerdo. --carpeta es obligatorio y la raíz sale de ese argumento (CLAUDE.md, «Ensayos aislados», punto 2), con un test que niega una carpeta fuera de data/. Perfil y fase, los mismos por defecto que la línea base; sin --depuracion.
>
> 4. Los tests de F2 y F3 sobre el fixture sintético de test_cableado.py: de acuerdo. Ningún test lee meses reales. La prueba sobre la construcción entera es F4.
>
> 5. El Marcador: sin fila, declarado en el informe como excepción a HOJA-DE-RUTA.md:817, con el motivo (la corrida base repite la línea base con diff de 0 bytes y no es una corrida nueva; las ablaciones son diagnóstico). La orden de cierre lo dirá.
>
> 6. Un solo proceso, de acuerdo, con dos condiciones:
>    - cada ablación con un motor y un estado nuevos; las velas y los ticks pueden compartirse solo si son de lectura. Antes de las 32, la base corrida dos veces en el mismo proceso tiene que dar recuentos idénticos entre sí y a los de F4.1;
>    - el umbral de 1,5 GiB: si lo pasa, un proceso por ablación, dicho.
>
> 7. El control. El conjunto de control NO es mi lista de 11: lo calcula la bitácora de la base, como las VIGENTE que en toda la construcción ni disparan ni quedan desconocidas en ningún evento. Ese conjunto tiene que dar delta cero; si alguna no lo da, PARADA. RN-008 (que toca la memoria del día al evaluarse) y cualquiera que quede fuera del control se miden como las demás y se explican.
>
> 8. Herencias de tu auditor:
>    - traza_por_cierre.py se queda como está. El informe dice qué cubre la bitácora de lo que hacía y en qué se diferencia (cuenta por mes frente a día suelto);
>    - la deuda de la zona reutilizada (PUNTO-USADO.md §1.c y §4.f) entra en el análisis de 07-14: di, con la bitácora, si sus cierres contaron en los cartuchos de otro escenario y si eso explica que RN-016 no frenara;
>    - la carpeta desde un argumento, en el punto 3; los tests sin meses reales, en el punto 4.
>
> 9. Correcciones mías al encargo, que apuntas como desviaciones: la rama de CI es fix/trazas-ablacion (RITUAL.md:102), no fix/trabajo-trazas-ablacion; NA:F no aparece en ningún sitio del bloque de R4.4 al proponerla HECHA; las corridas pueden llevar unas 4 h.
>
> 10. Sigue. Haz F1 ya, en su commit. Después F2, F3 y F4 sin esperarme, con la PARADA condicional: paras solo si el diff de F4.1 no da 0 bytes, si la base repetida en proceso no cuadra, si alguna regla del control no da delta cero o si el diseño del punto 0 no puede ser solo registro. Si todo cuadra, sigue con F5 hasta la PARADA final, el revisor (agente revisor) y «Rama lista para revisión, NO cerrada». Antes de la primera corrida de cada día, su fila en HOLDOUT-EXPOSICIONES.md.

### Cómo se aplica la respuesta, punto por punto

| Punto | Dónde |
|---|---|
| 0. El gate en el intérprete, solo registro | F2 (con su test del gate que dispara y el desconocido); la prueba, F4.1. **Desviación decidida por el consultor**: el encargo decía «sin tocar el intérprete» |
| 1. `DIAGNOSTICO-DECISIONES` y `nombre_etiquetado` | F3, con el test que rompe en main |
| 2. 07-03: el punto, su vela, la M1 del llenado, (a) antes o después de la primera M1 que cierra pasado el punto, (b) la toma y su cuerpo; las tres clases | F2 (la bitácora lo da) y F5 |
| 3. `motor decisiones`, `--carpeta` obligatorio dentro de `data/` | F3, con su test |
| 4. Tests solo sobre el fixture sintético | F2 y F3 |
| 5. Sin fila en el Marcador, como excepción a HOJA-DE-RUTA.md:817 | «Desviaciones», al final |
| 6. Un proceso; motor y estado nuevos por corrida; la base dos veces idéntica; 1,5 GiB | F3 y F4 |
| 7. El control lo calcula la bitácora de la base | F4 |
| 8. Herencias | `traza_por_cierre.py` sin tocar (F2 dice qué cubre); la zona reutilizada en 07-14 (F5) |
| 9. `fix/trazas-ablacion`; NA:F fuera de todo el bloque de R4.4; ~4 h | «Desviaciones» y F5 |
| 10. F1 ya; F2-F4 sin esperar con la PARADA condicional; F5, revisor y entrega | este orden |

## F1 · El recorte de PROJECT_STATE (2026-11-09)

Con `docs/state/README.md`, «Que sale de PROJECT_STATE, y con que criterio», negando por defecto.

**(a) a (d): ninguna sale.** Las que tenían alguna posibilidad, comprobadas: los docstrings de
`scripts/viabilidad_trader.py:11` y `scripts/viabilidad_comision.py:46` siguen diciendo la comisión
vieja; el visor sigue sin `--diagnostico-cuenta-diaria` (`cli.py:2250-2261` frente a `:2438`); el
ADR 0087 de S-15 sigue sin existir; la nota de RN-019 sigue diciendo que A-31 lo pregunta
(`strategy_spec.yaml:2024`); `letras_hechas` sigue siendo un conjunto (`test_hoja_de_ruta.py:60`);
ningún guion ni el Makefile miran `HOLDOUT-EXPOSICIONES.md` (la guardia de la fila del día sigue
pendiente); el panel de FTMO sigue pendiente en los cuatro sitios que nombra. Los Pendientes
heredados y las Reglas vivas, sin evidencia de estar hechos: se quedan.

**(e): las 9 líneas de 271 bytes o más.** El corte es el válido más largo de 160 bytes como mucho
(antes de «. », «; » o «: », o tras el «)» que cierra un inciso; nunca con una comilla invertida, un
paréntesis o unas comillas sin cerrar), calculado por `acortar.py` (carpeta de trabajo de la sesión):

| Línea (arranque) | Antes | Después | Ahorra |
|---|---|---|---|
| El bróker simulado reserva margen… (con la cita DEMO-EJECUCIONES-2-3.md §0.f) | 322 | 197 | 125 |
| Los docstrings de `scripts/viabilidad_trader.py:11`… (DEMO-EJECUCIONES-2-3.md §3.1) | 301 | 225 | 76 |
| Riesgo residual de C (§5)… | 325 | 205 | 120 |
| Riesgo residual de B (§5)… | 285 | 185 | 100 |
| Los guiones de la plataforma… (GUARDIA-G1.md §6.4) | 447 | 207 | 240 |
| Riesgo residual de la excepción de la carga por ruta… | 282 | 141 | 141 |
| Riesgo residual de ADR-0088 (revisor, B7)… | 498 | 94 | 404 |
| Copia de seguridad de las crudas y los WAV… | 456 | 95 | 361 |
| El panel de FTMO quedó declarado el 2026-11-07… | 707 | 158 | 549 |

Las otras 13 de más de 200 bytes sin acortar ahorrarían menos de 60: se quedan enteras. Tres cortes
dejan poco texto (la de ADR-0088, la de la copia de seguridad y la de los docstrings, que acaba en el
inciso «(«10 (perfil)»)» sin su verbo), porque el primer «: » o «; » que sigue pasa de 160 bytes: es
la lectura estricta de (e), y el texto entero está en HISTORIA.

**Cifra:** `PROJECT_STATE.md` 23.876 bytes antes (23.805 en `main`; +71 de la apertura) y **21.760**
después: −2.116. Al final de HISTORIA, el bloque «# Technical Debt ACORTADA · sale de PROJECT_STATE.md
en trabajo/trazas-ablacion (2026-11-09)», con cada línea entera y lo que queda. La Next Action no se
ha tocado.

**Corrección tras el revisor (b4, 2026-11-09).** «Las otras 13 ahorrarían menos de 60» no era cierto
para una: la de guardia-g1 («- Riesgo residual de `trabajo/guardia-g1` (§4.3): …», 252 bytes), que
tiene un corte válido tras «(§4.3)», como la de ADR-0088. Acortada en el commit de las correcciones:
252 → 100 bytes (ahorra 152), con su texto entero al final de HISTORIA en un bloque nuevo del mismo
título (HISTORIA solo se amplía). Mi error: elegí a mano los candidatos entre las 22 y a esta la di
por de menos de 60. Recontadas ahora TODAS las líneas de Technical Debt de más de 200 bytes sin la
marca, con el mismo criterio de corte de `acortar.py` (`recontar_e.py`, en el anexo):

| Línea (arranque) | Bytes | Ahorro sin la cita | Con la cita que hay que conservar | Queda |
|---|---|---|---|---|
| El validador del journal v1… (EA-CONEXION.md, respuesta a la PARADA, punto 4) | 263 | 106 | 58 | entera |
| Riesgo residual de `trabajo/guardia-g1` (§4.3)… | 252 | 152 | la cita va en el corte | **acortada** |
| RN-019 no dispara nunca en el motor… | 229 | 40 | — | entera |
| El visor no conecta `--diagnostico-cuenta-diaria`… (VISOR-CONSTRUCCION.md §4.3) | 216 | 78 | 49 | entera |
| make check, en una rama trabajo/*, no sella si HOLDOUT-EXPOSICIONES… | 243 | sin corte válido | — | entera |
| `arnes.dias_de_mercado` lee para calentar… (CORRIDA-CONSTRUCCION.md §1.c) | 267 | 60 | 29 | entera |
| La forma de medida de ffmpeg de la guardia… | 204 | 53 | — | entera |
| La ingesta asigna la sesión con el reloj del registro… | 216 | 55 | — | entera |
| Sin git callan, sin aviso… (docs/validation/HISTORIAL-SIN-GIT.md §3 y §6.1) | 234 | 77 | 27 | entera |
| RN-029 a RN-032 citan de relleno… (docs/validation/REABRIR-Y-FUENTE-DOCUMENTAL.md §4.4) | 220 | 100 | 46 | entera |
| EL DIA QUE UN CAMINO GUARDE MATERIAL… | 214 | sin corte válido | — | entera |
| DOS DIAS DEL UNIVERSO DE LA SESION 1… | 215 | sin corte válido | — | entera |
| La skill ingerir-sesion no nombra el trailer Fuente: … (SESION-06-EXTRACCION.md §7) | 220 | 116 | 73, pero el único corte cae dentro del nombre del trailer `Fuente:` (CLAUDE.md, «El trailer `Fuente:`»), que leo como un id: no vale (criterio mío, decisión 8 de la PARADA) | entera |

Las cifras «con la cita», con `citas_e.py` (en el anexo). `PROJECT_STATE.md`: 21.760 → 21.608 bytes.

## F2 y F3 · La bitácora y la ablación (2026-11-09)

**Los tests primero.** `tests/unit/test_decisiones.py` se escribió antes que el código y se ejecutó
sin él: `ERROR tests/unit/test_decisiones.py` (colección: no existía `engine/decisiones.py`). Con el
código de la bitácora y de la ablación escrito y `diagnostico.py` todavía como en `main`, falló uno
solo, el de `nombre_etiquetado` («DID NOT RAISE ValueError» con «DIAGNOSTICO-ABLACION-RN-007»): es
el test que rompe en `main` del punto 1. Ningún test lee velas ni ticks reales: todos van sobre el
día sintético de 2030 de `test_cableado.py` (punto 4).

**Lo que cambia en `src/`:**
- `engine/interprete.py` (punto 0, **desviación decidida por el consultor**: el encargo decía «sin
  tocar el intérprete»). El `Evento` gana tres campos de SOLO REGISTRO: `prohibido_por` (efecto →
  gates que dispararon y lo prohibieron, en orden, apuntado en `_ejecutar` junto a
  `prohibidos.update`), `quizas_por` (efecto → gates que quedaron DESCONOCIDOS y lo prohibirían, en
  alguna pasada) y `bloqueada_por` (por cada acción bloqueada, los gates de ESA pasada: los que
  dispararon y los desconocidos, con su clase). `quizas_prohibidos` pasa de conjunto de efectos a
  diccionario efecto → ids: se sigue mirando con `in`, así que bloquea exactamente lo mismo. La
  línea `evento.prohibidos.update(...)` y la `bloqueadas` no cambian. Nada lee los tres campos para
  decidir (los lee solo `engine/decisiones.py`).
- `engine/cableado.py`: el tipo `Cierre` y el campo `MotorCableado.observador` (None por defecto),
  llamado al final de cada cierre de M1, después de la traza y de las cancelaciones, con lo que el
  motor ya decidió. Con None, el bucle es el de antes.
- `engine/decisiones.py` (nuevo): la `Bitacora` (el observador), la ablación (`sin_regla`,
  `motor_nuevo`), el `Resumen` de una corrida, `comparar` y `correr_diagnostico`, que encadena la
  base con la bitácora, la base repetida sin ella, el control y las ablaciones. Su docstring lleva lo
  de ADR-0092 §6 para la ablación (F3).
- `engine/diagnostico.py`: `nombre_etiquetado` solo acepta «DIAGNOSTICO-A<cifras>-<valor>» y la de
  la cuenta; cualquier otra, `ValueError` (punto 1).
- `cli.py`: `motor decisiones` (punto 3): `--carpeta` (obligatoria, dentro de `data/`, fuera de
  `data/manifests/`), `--meses`, `--bitacora`, `--ablacion` / `--ablacion-vigentes`. Sin
  `_opciones_diagnostico` ni `_opciones_simulacion`: corre lo mismo que `motor arnes --simular` sin
  opciones (perfil y fase por defecto, sin depuración). No llama a `arnes.informe` ni a
  `habilita_medir`: no da veredicto, no escribe el informe del arnés y no puede habilitar medir.
  `motor arnes` y `motor visor` no cambian (`test_la_seccion_no_anade_ninguna_opcion_al_comando`
  sigue igual y en verde).
- `docs/adr/0092-…md`: la NOTA en §6 (F3), sin tocar el cuerpo.

**Lo que dice la bitácora**, por día y sesión, solo lo que CAMBIA en cada cierre de M1, con la hora
de pared y la UTC de ese cierre: la toma de M15 (el pivote, su nivel y su hora de formación, la M1
de la toma con o/h/l/c y si cierra pasada la línea, es decir, con cuerpo); los escenarios que se
abren y terminan; cada zona (lado, 0 y 1, el punto y la vela contraria que lo forma, y si su nivel
es el de la toma de M15 o el de una liquidez de M15 de ese instante); por qué una zona no tuvo orden
(zona usada, punto gastado, escenario terminado, orden pendiente o posición abierta, colocación
bloqueada, qué disparó); los hechos que cambian y la regla que los fija; cada prohibición con TODOS
sus gates; cada acción bloqueada con los gates de esa pasada; cada orden (tipo, lado, zona, precio,
stop, objetivo, lote) y cada cambio de estado; los llenados con (a) del punto 2: si ocurren ANTES o
DESPUÉS de la primera M1 que cierra más allá del precio desde que se colocó la orden, y si la M1 del
llenado cierra más allá (cuerpo) o no (mecha); y los cierres de posiciones con su motivo.

**Frente a `traza_por_cierre.py`** (punto 8, que se queda como está): cubre lo que aquel daba (las
disparadas, los efectos prohibidos, las bloqueadas con su regla, la toma de RN-004 y su pivote, la
zona de cada orden) y añade el gate de cada prohibición (que aquel deducía), los escenarios, los
puntos, la línea de M15 y la vida de cada orden. La diferencia de fondo: aquel corre UN día suelto,
como el visor, desde el capital, sustituyendo métodos de clase en el proceso; la bitácora va dentro
de la corrida entera con la cuenta por mes, por un campo del motor y solo en la corrida que la pide.

**Los tests** (14 funciones; 16 casos):
- F2: con la bitácora el motor decide lo mismo en tres rutas (stop, hueco que suspende la cuenta y
  posición viva): mismas operaciones, trazas, eventos del bróker, órdenes y cuenta; **la mutación**:
  un observador que enciende `detenido_por_cartuchos` un minuto antes de la zona cambia lo decidido y
  la comparación lo ve; un gate que dispara (RN-009) y uno DESCONOCIDO (RN-005) prohibiendo lo mismo
  salen los dos en `bloqueada_por` y en la línea de la bitácora; determinismo byte a byte; sin mirar
  al futuro (con el mercado cortado un minuto después del llenado, las líneas hasta ese cierre son
  las mismas); etiqueta en cada línea y nada de R, dinero ni porcentajes.
- F3: `nombre_etiquetado`; la carpeta fuera de `data/` (y `data/manifests/`, y `data/../x`) se niega;
  los nombres llevan DIAGNOSTICO; el parser de `motor decisiones` tiene exactamente sus seis opciones
  y `--carpeta` es obligatoria; un id DESCARTADA y uno inexistente dan un error que los nombra; sin
  ablación, la lista es la de `motor arnes` (32), y con ella falta solo esa regla; `motor_nuevo` no
  arrastra nada de una corrida anterior y comparte los mercados; y, de punta a punta, la base, la
  base repetida (igual), el control calculado por la bitácora con una regla suya que da «sin delta»,
  y RN-015 que pierde la pareja.
- Un hallazgo del fixture, no del motor: el `toca_colocar_orden_limite` sintético de
  `test_cableado.py` guarda en una clausura que ya dio SÍ, así que solo coloca en la PRIMERA corrida
  del proceso. Los tests que corren el mismo día dos veces usan uno sin estado (`_sin_estado`). Las
  primitivas reales se crean de nuevo cada día (`primitivas_cableadas`, `cableado.py:370`); F4 lo
  comprueba con la base repetida.

**La prueba de que no cambia ninguna decisión sobre la construcción entera es F4.1** (punto 0):
`motor arnes --simular` con el código de la rama, diff contra `cuenta-por-mes.txt`.

## F4 · Las corridas (2026-11-09)

Una a la vez, ninguna junto a un `make check`, todas sobre construcción (2026-01, 2026-04, 2026-07
y 2026-08) por la compuerta del arnés, declaradas antes de la primera en `HOLDOUT-EXPOSICIONES.md`
(su fila del 2026-11-09). Las tres terminaron antes de medianoche en el reloj de la máquina, que
va en UTC−5 (la última, a las 19:51; las 01:51 del 10 en Madrid): la fecha de la fila es la de ese
reloj. Las salidas viven en
`data/trazas-ablacion/` (fuera de git); las que entran al repo, en
`docs/validation/anexos/TRAZAS-ABLACION/` (sin CR, comprobado con `grep -U -c -P "\r"`: 0 en las
seis).

| Corrida | Comando, tal como se ejecutó (Bash en segundo plano) | Tiempo | Pico |
|---|---|---|---|
| F4.1 | `cd "/c/Users/USER/Desktop/Bot v3" && uv run botsito motor arnes --simular --salida data/trazas-ablacion/cuenta-por-mes.txt > data/trazas-ablacion/f41-pantalla.txt 2>&1; echo "exit=$?" >> data/trazas-ablacion/f41-pantalla.txt` | 364,9 s | 636,2 MiB |
| F4.2 | `cd "/c/Users/USER/Desktop/Bot v3" && uv run botsito motor decisiones --carpeta data/trazas-ablacion/bitacora --bitacora 2026-04-13,2026-07-02,2026-07-03,2026-07-14 > data/trazas-ablacion/f42-pantalla.txt 2>&1; echo "exit=$?" >> data/trazas-ablacion/f42-pantalla.txt` | 565,6 s | 633,3 MiB |
| F4.3 | `cd "/c/Users/USER/Desktop/Bot v3" && uv run botsito motor decisiones --carpeta data/trazas-ablacion/ablacion --ablacion-vigentes > data/trazas-ablacion/f43-pantalla.txt 2>&1; echo "exit=$?" >> data/trazas-ablacion/f43-pantalla.txt` | 8297,6 s | 632,9 MiB |

Las tres salieron con `exit=0`. Muy por debajo de 1,5 GiB: no hizo falta un proceso por ablación
(punto 6).

### F4.1 · La base frente a la línea base

`diff` de `data/trazas-ablacion/cuenta-por-mes.txt` contra
`docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/cuenta-por-mes.txt`: **0 bytes**; el mismo
sha256 en los dos, `e6ca305ba31c6307f405d963a8eb043a66d85fafd8262a1806abd53075798054`. Es la prueba
del punto 0: con el registro nuevo del intérprete y el campo `observador` (en `None`), `motor arnes`
decide lo mismo sobre la construcción entera. No hay PARADA.

### F4.2 · La bitácora de los cuatro días, y la base repetida

En un proceso: la base con la bitácora y, después, la base repetida sin ella, cada una con su motor y
su estado nuevos (`motor_nuevo`). Recuentos (parejas, de más, fuera, órdenes, no enviadas, rechazos,
cuentas suspendidas): **(31, 192, 24, 1150, 0, 32, 0)** en las dos, «igual: si». Cuadran con F4.1
(871 canceladas + 247 llenadas + 32 rechazadas = 1150 órdenes; los rechazos, 8 + 11 + 9 + 4 por
mes) y con §8 de RECORRIDA-CONSTRUCCION-2 (T0: 31; P6 en día: 24; P5 153 + P6 en sesión 39 = 192).
No hay PARADA.

Las sesiones enteras de 2026-04-13, 07-02, 07-03 y 07-14 van al anexo
(`bitacora.DIAGNOSTICO.<día>.txt`), con `ablacion.DIAGNOSTICO.base.txt` (los recuentos y lo que
hace cada regla en la base).

**El control, calculado por la bitácora de la base** (punto 7): las VIGENTE que en los 36.556
eventos de la construcción ni disparan ni quedan desconocidas son **RN-008, RN-010, RN-019, RN-020,
RN-026, RN-029, RN-030 y RN-031** (8). De la lista de 11 del encargo salen RN-007, RN-021 y RN-022,
que quedan DESCONOCIDAS en los 36.556 eventos: no disparan, pero se evalúan sin respuesta, así que
no son control por la definición del punto 7; se miden como las demás (y dan delta cero, abajo).

Lo que hace cada regla en la base (`ablacion.DIAGNOSTICO.base.txt`; «bloquea» = acciones que
quedan bloqueadas con esa regla entre los gates de su pasada):

| Regla | Clase | Dispara | Desconocida | Bloquea |
|---|---|---|---|---|
| RN-001 | gate | 591 | 0 | 464 |
| RN-002 | terminal | 5 | 0 | 0 |
| RN-035 | disparador | 2 | 0 | 0 |
| RN-037 | gate | 152 | 0 | 117 |
| RN-003 | disparador | 152 | 0 | 0 |
| RN-033 | gate | 240 | 0 | 0 |
| RN-004 | disparador | 6681 | 0 | 0 |
| RN-005 | gate | 10212 | 0 | 8149 |
| RN-006 | disparador | 869 | 0 | 0 |
| RN-007 | disparador | 0 | 36556 | 0 |
| RN-008 | gate | 0 | 0 | 0 |
| RN-009 | gate | 20513 | 0 | 17772 |
| RN-010 | disparador | 0 | 0 | 0 |
| RN-011 | disparador | 19598 | 0 | 0 |
| RN-012 | disparador | 210 | 210 | 0 |
| RN-014 | disparador | 66 | 0 | 0 |
| RN-015 | disparador | 19598 | 0 | 0 |
| RN-016 | gate | 516 | 0 | 404 |
| RN-017 | disparador | 35 | 0 | 0 |
| RN-034 | disparador | 35 | 0 | 0 |
| RN-018 | gate | 1698 | 0 | 0 |
| RN-019 | disparador | 0 | 0 | 0 |
| RN-020 | gate | 0 | 0 | 0 |
| RN-036 | gate | 814 | 0 | 723 |
| RN-021 | disparador | 0 | 36556 | 0 |
| RN-022 | fallback | 0 | 36556 | 0 |
| RN-026 | gate | 0 | 0 | 0 |
| RN-027 | gate | 19597 | 0 | 0 |
| RN-029 | gate | 0 | 0 | 0 |
| RN-030 | terminal | 0 | 0 | 0 |
| RN-031 | gate | 0 | 0 | 0 |
| RN-032 | gate | 5246 | 0 | 3202 |

### F4.3 · La ablación de las 32 VIGENTE

Un proceso: la base, la base repetida (las dos, (31, 192, 24, 1150, 0, 32, 0), «igual: si») y las
32, una a una, cada una con su motor y su estado nuevos. **Las 8 del control dan «sin delta»**
(`[control]` en el fichero), y también RN-007, RN-021 y RN-022: **las 11 del encargo dan delta
cero**. Ninguna corrida falló ni se detuvo; ninguna cuenta quedó suspendida. No hay PARADA.

Salida entera: `anexos/TRAZAS-ABLACION/ablacion.DIAGNOSTICO.vigentes.txt` (cada línea de delta con
su operación: día, sesión, lado, instante en UTC y entrada). Las filas de §8 se cruzaron con
`patrones-cuenta-por-mes.txt` por (quién, día, sesión, lado, instante, entrada): **todas las
operaciones que cambian tienen su fila** (0 sin fila); las que APARECEN no están en §8 porque no
eran de la base.

Las columnas: parejas que se ganan (la clase de la fila del trader en §8) y que se pierden (todas
son T0 en §8); «de más» = operaciones del bot sin pareja en un día con operaciones del trader (P5 y
P6 en sesión de §8); «día sin trader» = P6 en día; Δ órdenes = órdenes del bot (llenadas,
canceladas y rechazadas al colocar, como las 871 + 247 + 32 de la base) frente a 1150.
«Re-emparejada»: la misma fila del trader sale como perdida con un bot y ganada con otro.

| Regla | Parejas que se ganan | Parejas que se pierden | De más: aparecen / desaparecen | Día sin trader: aparecen / desaparecen | Δ órdenes | Otros recuentos |
|---|---|---|---|---|---|---|
| RN-001 | 0 | 0 | 0 / 0 | 0 / 0 | +1 | — |
| RN-002 | 0 | 0 | 0 / 3 (P5 mismo lado 1, P6 en sesión 2) | 0 / 1 | −27 | rechazos 32 → 30 |
| RN-035 | 0 | 0 | 1 / 2 (P6 en sesión 2) | 1 / 0 | −9 | rechazos 32 → 30 |
| RN-037 | 0 | 0 | 0 / 0 | 0 / 0 | +3 | — |
| RN-003 | 0 | 31 (todas) | 0 / 192 (todas) | 0 / 24 (todas) | −1150 | el bot no opera |
| RN-033 | sin delta | | | | | |
| RN-004 | 0 | 31 (todas) | 0 / 192 (todas) | 0 / 24 (todas) | −1150 | el bot no opera |
| RN-005 | 0 | 0 | 23 / 2 (P5 mismo lado 1, P6 en sesión 1) | 1 / 2 | +42 | rechazos 32 → 35 |
| RN-006 | 3 filas nuevas (P3 ×2, P7 ×1) y 2 re-emparejadas | 24 (22 sin las 2 re-emparejadas) | 137 / 156 (P5 mismo lado 99, P5 otro lado 26, P6 en sesión 31) | 9 / 21 | −898 | parejas 31 → 12; rechazos 32 → 8 |
| RN-007 | sin delta | | | | | |
| RN-008 | sin delta (control) | | | | | |
| RN-009 | 18 filas nuevas (P2 ×7, P3 ×10, P7 ×1) y 2 re-emparejadas | 15 (13 sin las 2 re-emparejadas) | 144 / 88 (P5 mismo lado 55, P5 otro lado 14, P6 en sesión 19) | 29 / 9 | +229 | parejas 31 → 36; rechazos 32 → 75 |
| RN-010 | sin delta (control) | | | | | |
| RN-011 | 0 | 31 (todas) | 0 / 192 (todas) | 0 / 24 (todas) | −1150 | el bot no opera |
| RN-012 | sin delta | | | | | |
| RN-014 | 0 | 3 | 4 / 20 (P5 mismo lado 13, P5 otro lado 4, P6 en sesión 3) | 1 / 2 | −105 | rechazos 32 → 27 |
| RN-015 | 0 | 31 (todas) | 0 / 192 (todas) | 0 / 24 (todas) | −1150 | el bot no opera |
| RN-016 | sin delta | | | | | |
| RN-017 | sin delta | | | | | |
| RN-034 | 0 | 0 | 0 / 0 | 0 / 0 | +2 | — |
| RN-018 | sin delta | | | | | |
| RN-019 | sin delta (control) | | | | | |
| RN-020 | sin delta (control) | | | | | |
| RN-036 | 0 | 1 | 6 / 3 (P5 mismo lado 3) | 0 / 1 | +4 | — |
| RN-021 | sin delta | | | | | |
| RN-022 | sin delta | | | | | |
| RN-026 | sin delta (control) | | | | | |
| RN-027 | sin delta | | | | | |
| RN-029 | sin delta (control) | | | | | |
| RN-030 | sin delta (control) | | | | | |
| RN-031 | sin delta (control) | | | | | |
| RN-032 | 0 | 0 | 1 / 0 | 2 / 0 | +9 | — |

**Las que quedan fuera del control y dan delta cero, explicadas** (punto 7; lo medido es solo que
quitarlas no cambia los recuentos ni ninguna operación):
- RN-007 y RN-021 (disparadores) y RN-022 (fallback): DESCONOCIDAS en todos los eventos. Un
  disparador desconocido no ejecuta su acción, y RN-022 no es un gate, así que no entra en los
  `quizas_prohibidos` de la pasada de gates; quitarlas no cambia nada.
- RN-017: solo `permite` (`buscar_entradas`); un permiso no bloquea ni coloca.
- RN-018 y RN-033: gates que disparan (1698 y 240) y bloquean 0 acciones en la base: en los
  eventos en que disparan, su prohibición no alcanza a ninguna acción.
- RN-016: bloquea 404 acciones, y quitarla no cambia ninguna operación ni ninguna orden. En
  los dos instantes que mira F5 (07-02 14:10 y 14:23) prohíben también RN-001 y RN-009. Que ocurra
  lo mismo en las 404 es lo que dice la ablación, no algo medido acción por acción.
- RN-012 (`realizar_perdida`) y RN-027 (`redondear_lote`): actúan sobre el lote. La comparación
  mira cada operación por (día, sesión, lado, instante y entrada), no su lote, su stop ni su
  objetivo; un lote distinto solo se vería si mueve las no enviadas, los rechazos o las cuentas
  suspendidas (por el margen, el lote mínimo o el saldo), que también se comparan. Lo medido es que
  quitarlas dio delta cero; que el lote no cambie no está medido (Technical Debt propuesta, en F5;
  corregido tras el revisor, a1: decía «no pueden dar delta por construcción»).
- RN-008 (control): ni dispara ni queda desconocida en ningún evento (toca la memoria del día al
  evaluarse, punto 7): su ablación da «sin delta».

Las que dan delta solo en órdenes (RN-001 +1, RN-034 +2, RN-037 +3) colocan órdenes de más que no
llegan a operación ni a rechazo: ninguna operación cambia.

## F5 · Las clases propuestas (2026-11-09)

Todo sale de la bitácora de F4.2 (anexo `anexos/TRAZAS-ABLACION/bitacora.DIAGNOSTICO.<día>.txt`),
que es la corrida con la cuenta por mes (la misma que F4.1). Horas de pared (Europe/Madrid, verano:
UTC+2), como en VIDEO-JULIO.md §4; entre paréntesis, la UTC. Las clases son PROPUESTAS: las decide el
consultor en la PARADA final. Ninguna operación de más del bot se llama error (VIDEO-JULIO.md §10,
punto 4).

### 5.1 La tensión de 07-03, sesión 07-11 (las 5 filas de «error nuestro (sospecha)»)

Lo fijado, de donde se mide: A-32 RESUELTA por la sesión 5 (S-18; `ambiguedades.yaml:864-898`): «en
M1 la mecha siempre vale»; la única ruptura que pide cuerpo es la que habilita la zona lineal de
liquidez de M15, y una línea que viene de M15 cuenta como de M15 aunque se mire en M1.
`breaker_m1_criterio_ruptura = mecha`, CONFIRMED (`parametros.yaml:501-518`); la toma de M15 se pide
con cuerpo (`liquidez_m15_criterio_toma = cuerpo`). Y lo que hace el motor (fase 0, 0.2b): la orden
es una STOP en el último pivote de M1 contrario a la entrada (`orden_limite_nace =
al_aparecer_punto_de_breaker`, `orden_stop_punto = ultimo_pivote_m1`; ADR-0064), que se llena en el
tick que lo toca; para la spec, «la orden stop solo abre cuando el precio rompe el punto, que es el
esquema 1» (`strategy_spec.yaml:1528-1531`).

Las cuatro órdenes del bot que tocan esas cinco filas (las cuatro P5, y la P2 del trader de las 09:24,
cuyo bot más cercano es o6):

| Orden (fila) | (b) Toma de M15 que abrió su escenario | (i) Vela de la toma | Punto (ii) y su vela | (iii) ¿Línea de M15? | (a) Llenado frente a la primera M1 que cierra más allá | M1 del llenado |
|---|---|---|---|---|---|---|
| o4 (P5 08:02) | escenario 1: el bajo de M15 en 1.14500 (formado 07:45), toma a las 07:57 | cierra 1.14497: **con cuerpo** | 1.14496, la vela contraria que abre a las 08:01 | no | llenada 08:02:06: **ANTES** de que ninguna M1 cierre más allá | **mecha** (no cierra más allá) |
| o5 (P5 08:03) | escenario 1, la misma toma | con cuerpo | 1.14496, la misma vela | no | llenada 08:03:31: **ANTES** | **cuerpo** (cierra más allá) |
| o6 (P5 09:24 y P2 del trader 09:24, Δ17) | escenario 2: el bajo de M15 en 1.14512 (formado 08:45), toma a las 09:23 | cierra 1.14510: con cuerpo | 1.14545, la vela contraria que abre a las 09:14 | no | llenada 09:24:42: **ANTES** | **mecha** |
| o8 (P5 09:35) | **escenario 2** (la toma de las 09:23), aunque a las 09:35 se abre el 3 con el bajo de M15 en 1.14507 | con cuerpo (las dos tomas) | 1.14517, la vela contraria que abre a las 09:34 | no | llenada 09:35:41: **ANTES** | **mecha** |

**Dos límites de la medida** (revisor, b5 y b6; dichos aquí porque las clases se apoyan en ellos):
- **(a) no distingue unas órdenes de otras.** La bitácora mira las M1 que cierran entre la colocación
  y el minuto del llenado (`decisiones.py:543-561`); la ventana empieza al colocar, no al formarse el
  punto. Con una orden stop en el punto, el llenado llega en el tick que toca el nivel, antes de que
  ninguna M1 pueda cerrar más allá: «ANTES» sale siempre, salvo un hueco. En las cuatro de la tabla
  colocación y llenado caen en el mismo minuto (o4 08:02 y 08:02:06; o5 08:03 y 08:03:31; o6 09:24
  y 09:24:42; o8 09:35 y 09:35:41): la ventana está vacía. En los cuatro días, 20 «ANTES» y 0
  «DESPUÉS». Lo que (a) mide de verdad es el mecanismo de ADR-0064 (`orden_limite_nace =
  al_aparecer_punto_de_breaker` con una stop), que es el mismo en todas las órdenes del bot.
- **(iii) solo compara con los niveles de M15 de su instante**: la toma del escenario vigente y la
  liquidez de M15 de cada lado en ese cierre, por igualdad exacta. Un nivel de M15 tomado antes en la
  sesión sale «no» (en 07-14, la zona 115 de o13 a las 12:28 tiene el punto 1.13990, que es el bajo
  de M15 de la toma de las 11:19, y sale «no»). En 07-03, los tres niveles de las tomas (1.14500,
  1.14512, 1.14507) no coinciden con los puntos (1.14496, 1.14545, 1.14517); otros niveles de M15
  anteriores de la sesión, y la distancia de 4 puntos entre 1.14496 y 1.14500, no están medidos.

Un hecho de más, de la bitácora: zona:46 (09:23) y zona:51 (09:35, la de o8) se ligan al escenario
ANTERIOR en el mismo cierre de M1 en que RN-004 abre uno nuevo: los gates se evalúan antes que los
disparadores (`CLASES_EN_ORDEN`), RN-005 llama a `zona_del_punto`, que liga la zona al escenario
vigente, y RN-004 abre el escenario nuevo después en ese mismo evento. Así, el stop de o8 (09:37:06)
cuenta en los cartuchos del escenario 2, no del 3. Es la deuda de la zona reutilizada de PUNTO-USADO.md
§1.c y §4.f, vista aquí en su forma más directa (no se toca: cambiaría lo que el motor decide).

**Las clases, con el criterio del punto 2 de la respuesta a la fase 0:**
- «error nuestro» (el punto o la toma tratan como de M1 una línea de M15, o la toma de M15 se dio con
  mecha): **no aplica a ninguna**, con el límite de (iii). Las tres tomas cierran pasada la línea
  (con cuerpo) y ningún punto coincide con un nivel de M15 de su instante (ni con la toma, ni con la
  liquidez de M15 de cada lado); con niveles de M15 anteriores no se ha comparado.
- «contradicción con lo fijado» (el punto es un pivote de M1 y el llenado fue con mecha, contra la voz
  de v12 y con S-18 a favor del bot): **o4, o6 y o8** (y, con o6, la fila P2 del trader de las 09:24).
  La voz de v12 0:00:15-0:00:58 («aquí no había entrada porque es con mecha, sabemos que tiene que ser
  con cuerpo [...] aquí sí que tenemos una entrada vale porque nos genera un breaker con cuerpo»,
  VIDEO-JULIO.md §4.1 y §7 #6) pide cuerpo; S-18 dice que en M1 la mecha vale.
- **o5**: el llenado es al tick, ANTES de que cierre ninguna M1 más allá, pero su propia M1 cierra más
  allá (cuerpo). No es «contradicción» por la vela; sí entra en la tercera.
- «regla desconocida: cuándo se coloca la orden respecto de la ruptura» (toca ADR-0064 y
  `orden_limite_nace`): **las cuatro**, pero no por algo propio de ellas: el bot entra en el tick que
  toca el punto, antes de que ninguna M1 haya cerrado más allá, y eso le pasa a TODA orden stop del
  bot (límite de (a)). La voz de v12 habla de que el breaker «se genera con cuerpo» antes de haber
  entrada; S-18 dice que en M1 la mecha vale. La condición del punto 2 se cumple, pero es del
  mecanismo, no de estas cuatro.

Para la sesión 7, como hecho medido y sin sugerir la respuesta: «El 3 de julio, entre las 08:02 y las
09:35, el bot compró cuatro veces con una orden stop en el último pivote de M1, que se llenó en el
tick que tocaba ese nivel; en tres de las cuatro, la vela de un minuto en que se llenó no cerró por
encima del nivel. En el vídeo dices que ahí no había entrada porque era con mecha y que tiene que ser
con cuerpo; en la sesión 5 dijiste que en M1 la mecha siempre vale. ¿En qué momento colocas la orden
respecto de la ruptura de ese nivel?» (corregida tras el revisor, b7: terminaba en «y qué vela tiene
que cerrar?», que da por hecho que alguna tiene que cerrar).

### 5.2 Las 13 «a la rama de trazas» (VIDEO-JULIO.md §4.1 y §4.2)

| Sesión | Filas | Lo que dice la bitácora | Clase propuesta |
|---|---|---|---|
| 07-02 11-15 | P3 ×3 (trader 11:34, 12:25, 12:45) | en los tres instantes RN-011 dimensiona una zona del escenario vigente y RN-015 queda **bloqueado por RN-009** (las zonas de control desarrolladas superan `zonas_control_max_por_esquema`), sin ningún otro gate; el escenario 1 (toma 11:08) en la de 11:34 y el 2 (toma 12:02) en las de 12:25 y 12:45 | **sin clase** con un hecho nuevo: el gate que deja al bot fuera es RN-009. El número ya lo fijó el trader: A-20 RESUELTA («solo 1 zona control bro. si hay 2 se descarta», fb-2026-09-09-sesion-01-1b2203b0; `zonas_control_max_por_esquema = 1`, CONFIRMED). Lo que no está fijado es qué zonas cuenta él como de control en ese esquema: pregunta 2 de 5.5 (corregido tras el revisor, a2) |
| 07-02 11-15 | P5 ×2 (bot 11:13 = o7, 12:07 = o10) | o7: escenario 1 (toma de 11:08, el bajo de M15 en 1.14126, con cuerpo), llenada 11:13:30, ANTES de que cierre ninguna M1 más allá, y su M1 cierra más allá (cuerpo); o10: escenario 2 (toma de 12:02, bajo 1.14089, con cuerpo), llenada 12:07:11, ANTES, su M1 con cuerpo | **sin clase** (operaciones de más; la nota de P5) |
| 07-03 11-15 | P5 (bot 11:13 = o15) y P3 (trader 12:02) | o15: escenario 1 (toma de 11:08, bajo 1.14503, con cuerpo), llenada 11:13:34, ANTES, su M1 con mecha; a las 12:02, RN-015 bloqueado por **RN-009** | o15: **sin clase** (de más); la P3 de 12:02: **sin clase**, gate RN-009 (A-20 RESUELTA; la misma pregunta 2 de 5.5) |
| 07-14 11-15 | P2 Δ21 (11:35), P2 Δ19 (12:44), P3 ×2 (11:48, 13:06) | en los cuatro instantes RN-015 bloqueado por **RN-009**; escenario 1 (toma 11:19) en las de 11:35 y 11:48; escenario 2 (toma 12:27) en las de 12:44 y 13:06 | **sin clase**, gate RN-009 |
| 07-14 11-15 | P5 ×2 (bot 11:21 = o10, 11:26 = o12) | escenario 1, toma de 11:19 (bajo 1.13990, con cuerpo); llenadas 11:21:03 y 11:26:44, ANTES de que cierre ninguna M1 más allá, las dos con mecha; las dos, stop | **sin clase** (de más) |

### 5.3 La pendiente con dueño (RECORRIDA-CONSTRUCCION-2.md:1355-1358)

- **07-14 11-15 (o10, o12 y o14): no son del mismo barrido.** o10 y o12 son del escenario 1 (la toma
  de las 11:19 del bajo de M15 en 1.13990, formado a las 11:15; zonas 79 y 80, escenario 1); o14 es
  del escenario 2 (la toma de las 12:27 del bajo de M15 en 1.13948, formado a las 12:00; zona 116,
  escenario 2). Dos pérdidas en el escenario 1 y una en el 2, menos de `cartuchos_max = 3` en
  cada uno: RN-016 no tenía que saltar, y no salta (aplicado como está escrito: **sí**). La deuda de
  la zona reutilizada no actúa aquí: las tres zonas son de su propio escenario (o11 reusa zona:79
  dentro del escenario 1, que es lo de ADR-0083). A las 12:36, tras el stop de o14, el siguiente
  intento lo bloquea RN-009.
- **04-13 07-11, 08:47: el gate es RN-009.** RN-011 dimensiona zona:59 (escenario 2) y RN-015 no coloca
  porque lo prohíbe RN-009, solo él (también a las 08:46, 08:48, 08:49 y 08:50). Sin posición viva.
- **07-02 11-15, 12:25 y 12:45: el gate es RN-009**, solo él, sobre zona:140 y zona:149 (escenario 2).
- **07-02 14:10 y 14:23** (ya «sí» en la recorrida): los prohíben **tres** gates, RN-001, RN-009 y
  RN-016. RN-016 por los cartuchos (`detenido_por_cartuchos` desde las 14:08, tras o22, o23 y o25 del
  escenario 3, la toma de las 13:47); RN-001 porque su forma incluye `detenido_por_cartuchos`; y RN-009
  por su cuenta. El visor solo dejaba ver el freno.

**Lo que añade la ablación a 5.2 y 5.3** (F4.3, instantes en UTC como en el fichero): sin RN-009,
de las filas con gate RN-009 ganan pareja **la P3 del trader de 07-02 a las 12:25** (10:25:50Z, con
un bot a las 10:21:52Z) y **las dos P3 de 04-13 a las 08:47 y a las 08:50** (06:47:45Z y 06:50:00Z,
con bots a las 06:47:46Z y 06:50:00Z). Las de 07-02 a las 11:34 y 12:45, la de 07-03 a las 12:02 y
las cuatro de 07-14 no ganan pareja ni sin RN-009: ahí no basta con quitar ese gate. Es un hecho de
la corrida, no una clase: no dice que RN-009 esté mal (sin RN-009 también se pierden 13 parejas de
la base).

### 5.4 De la ablación: las filas que mueve cada regla con delta (sin conclusiones)

Ninguna línea dice «quitar la regla»: la ablación dice qué pasa al apagarla, no si está bien. Las
operaciones de más que aparecen no se llaman error (VIDEO-JULIO.md §10, punto 4; F7 #10).
- **RN-003, RN-004, RN-011, RN-015**: sin ellas el bot no opera (la toma, el escenario, el
  dimensionado y la colocación): se pierden las 31 T0, las 192 de más y las 24 de día sin trader.
- **RN-009** (zonas de control por esquema): gana 18 filas del trader, P2 de 01-02 12:20:20Z,
  01-15 08:42:10Z, 01-19 13:36:00Z, 07-09 07:59:00Z y 11:02:05Z, 08-03 06:03:05Z y 09:46:15Z; P3
  de 01-05 06:25:05Z y 06:48:25Z, 01-06 09:22:00Z, 01-16 07:20:15Z, 01-19 08:32:40Z y 10:15:50Z,
  04-13 06:47:45Z y 06:50:00Z, 07-02 10:25:50Z y 08-04 11:34:50Z; P7 de 07-10 07:17:40Z. Pierde
  13 T0: 04-17 08:36:10Z, 04-23 06:49:35Z, 04-24 06:44:30Z, 04-28 08:12:05Z, 04-29 09:36:25Z,
  07-10 07:50:15Z y 10:58:40Z, 07-14 06:30:30Z, 06:55:30Z y 10:33:40Z, 07-15 05:06:55Z, 07-16
  06:00:10Z y 07-17 05:46:05Z (y re-empareja 01-14 06:03:15Z y 07-10 05:36:35Z). 144 de más
  aparecen y 88 desaparecen; 29 y 9 en días sin trader; +229 órdenes; rechazos 32 → 75.
- **RN-006** (reubicar la orden): gana 3 filas (P3 de 01-21 09:32:10Z y 07-13 11:25:05Z; P7 de
  07-10 07:17:40Z) y pierde 22 T0 (re-empareja 01-14 06:03:15Z y 07-10 07:10:50Z); 137 de más
  aparecen y 156 desaparecen; 9 y 21 en días sin trader; −898 órdenes; rechazos 32 → 8.
- **RN-014** (mover el stop): pierde 3 T0 (01-09 09:07:50Z, 07-16 06:00:10Z, 07-17 05:46:05Z); 4 de
  más aparecen y 20 desaparecen; 1 y 2 en días sin trader; −105 órdenes; rechazos 32 → 27.
- **RN-036**: pierde 1 T0 (07-17 05:46:05Z); 6 de más aparecen y 3 desaparecen (P5 mismo lado); 1
  de día sin trader desaparece; +4 órdenes.
- **RN-005** (el punto en el lado del 0): 23 de más aparecen y 2 desaparecen (P5 mismo lado 1, P6 en
  sesión 1); 1 y 2 en días sin trader; +42 órdenes; rechazos 32 → 35; ninguna pareja cambia.
- **RN-002** (cierre a mercado): 3 de más desaparecen (P5 mismo lado 1, P6 en sesión 2: 01-30
  10:54:26Z, 08-17 10:12:19Z y 10:42:34Z) y 1 de día sin trader (08-18 07:11:38Z); −27 órdenes;
  rechazos 32 → 30.
- **RN-035** (retirar la orden): 1 de más aparece (01-27 10:02:32Z) y 2 desaparecen (P6 en sesión,
  08-17 10:12:19Z y 10:42:34Z); 1 de día sin trader aparece (08-18 07:32:00Z); −9 órdenes;
  rechazos 32 → 30.
- **RN-032**: 1 de más aparece y 2 de día sin trader aparecen (08-18 07:32:00Z y 09:36:18Z); +9
  órdenes.
- **RN-001** (+1), **RN-034** (+2) y **RN-037** (+3): solo órdenes; ninguna operación cambia.

### 5.5 Lo que va a la sesión 7, como hecho medido y sin sugerir la respuesta

1. **Cuándo se coloca la orden respecto de la ruptura del punto** (de 5.1): «El 3 de julio, entre
   las 08:02 y las 09:35, el bot compró cuatro veces con una orden stop en el último pivote de M1,
   que se llenó en el tick que tocaba ese nivel; en tres de las cuatro, la vela de un minuto en que
   se llenó no cerró por encima del nivel. En el vídeo dices que ahí no había entrada porque era con
   mecha y que tiene que ser con cuerpo; en la sesión 5 dijiste que en M1 la mecha siempre vale. ¿En
   qué momento colocas la orden respecto de la ruptura de ese nivel?»
2. **Qué zonas cuentan como zonas de control del esquema** (de 5.2 y 5.3). El número no se pregunta:
   A-20 está RESUELTA («solo 1 zona control bro. si hay 2 se descarta»,
   fb-2026-09-09-sesion-01-1b2203b0; `zonas_control_max_por_esquema = 1`). «El 13 de abril a las
   08:47, el 2 de julio a las 11:34, 12:25 y 12:45, el 3 de julio a las 12:02 y el 14 de julio a las
   11:35, 11:48, 12:44 y 13:06, tú entraste y el bot no, porque contaba en ese esquema más de una zona
   de control. ¿Qué zonas cuentas como zonas de control de un esquema?» (corregida tras el revisor,
   a2: preguntaba cuántas, que ya está respondido).

### 5.6 Propuestas para la orden de cierre, comprobadas sobre una copia

Comprobadas en memoria (sin escribir nada en el repo) con las funciones de
`tests/unit/test_hoja_de_ruta.py`, cargado por su ruta: `problemas_a`, `problemas_b`, `problemas_c` y
`problemas_d` dan **[]** con las tres propuestas aplicadas a la vez; y un mutante (R4.4 HECHA
conservando `NA:F`) da en `problemas_b` «R4 «R4.4 · Trazas del motor y ablación por regla»: NA:F
esta HECHA y la letra sigue viva». F sigue viva (y sigue en los Refs de R0.3, R4.2, R4.3 y G.4);
`PROJECT_STATE.md` pasaría de 21.608 a 22.638 bytes (tope 25.000; repetido tras las
correcciones del revisor). Las letras vivas no cambian
(A, C, D, F, G, I, J, L, M, N, Q).

**(a) El texto nuevo de F** (sale el (1); F sigue viva, ningún encabezado de HECHA):

> F. Sesión 6 ACTIVADA en spec (F38n) y motor (F38o); S-22 y S-19 a la sesión 7. La re-corrida que
> cuenta está hecha (RECORRIDA-CONSTRUCCION-2.md: «no», cobertura 15.7 % y precisión 13.9 %; línea
> base anexos/RECORRIDA-CONSTRUCCION-2/cuenta-por-mes.txt; clasificación en §8: 31 pareja, 19 efecto
> de la cuenta, 4 RN-019, 81 hasta T, 279 sin clase). Las trazas del motor y la ablación por regla
> están hechas (TRAZAS-ABLACION.md; `motor decisiones`), con las clases que decidió el consultor en
> su PARADA final. El rumbo y el método desde aquí: docs/plan/RUMBO-2026-11.md (R0.3 de la hoja de
> ruta). Siguiente, en este orden: (1) láminas del bot a la estética de FX Replay (RUMBO §3); (2) la
> preparación de la sesión 7 con el método nuevo y su ADR (RUMBO §1), con los días de §8, la
> clasificación de las 81 filas del vídeo de julio (VIDEO-JULIO.md §4), sus dos preguntas técnicas
> (la tarde del 10 de julio; las entradas válidas que el trader deja sin tomar en el backtest), las
> dos de TRAZAS-ABLACION.md (cuándo se coloca la orden respecto de la ruptura del punto; qué zonas
> cuentan como zonas de control del esquema) y los ítems de evidencia de F7 #1, #2, #3 y #10. J antes si la
> hoja sale de kit hoja. El vídeo de mapeo, si llega, SIN ABRIR y fuera del repo, y entra antes de
> elegir los días. R6a y RUMBO §5 en los huecos.

(Las cifras «15.7 %» y «13.9 %» son las que ya trae la F de `main`; esta rama no publica ninguna.)

**(b) R4.4 HECHA**, sin `NA:F` en ningún sitio de su bloque (como R3.8), con estas dos líneas
cambiadas y el resto igual:

> - **Refs:** ID:ADR-0092 · ID:ADR-0064 · ID:ADR-0066
> - **Estado:** HECHA (`trabajo/trazas-ablacion`; TRAZAS-ABLACION.md): `motor decisiones` da la
>   bitácora por día y sesión (con el gate de cada prohibición apuntado en el intérprete, solo como
>   registro) y la ablación de las 32 VIGENTE; la base repite la línea base con un diff de 0 bytes y
>   el control da delta cero. Las clases de 04-13, 07-02, 07-03 y 07-14, las de la PARADA final.

**(c) Las líneas de Technical Debt nuevas:**

> - La zona que RN-005 liga al escenario vigente en el mismo cierre de M1 en que RN-004 abre uno
>   nuevo se queda en el escenario anterior, y su stop cuenta en los cartuchos de ese (2026-07-03
>   09:23 y 09:35, zona:46 y zona:51; TRAZAS-ABLACION.md F5): la deuda de la zona reutilizada de
>   PUNTO-USADO.md §1.c y §4.f en su forma directa; no se toca sin la regla del trader.
> - La comparación de `motor decisiones` mira cada operación por (día, sesión, lado, instante, entrada)
>   y no su lote, su stop ni su objetivo: un cambio de lote solo se ve si mueve las no enviadas, los
>   rechazos o las cuentas suspendidas (TRAZAS-ABLACION.md F4.3).
> - El `toca_colocar_orden_limite` sintético de tests/unit/test_cableado.py guarda en una clausura
>   que ya dio SÍ y solo coloca en la primera corrida del proceso; los tests que corren el día dos
>   veces usan uno sin estado (TRAZAS-ABLACION.md F2).

## El encargo, punto por punto

Cada requisito del encargo y de la respuesta del consultor a la fase 0, con su estado: Hecho,
Parcial, No hecho o Hecho de otra forma (sustituye a la tabla gruesa de la primera versión; revisor,
b2).

| # | Requisito | Estado | Dónde |
|---|---|---|---|
| 1 | Abrir con abrir-rama, riesgo alto, tramo R4; encargo tal cual; Archivo de PROJECT_STATE | Hecho | commit 29561efd; `HISTORIA.md`, Archivo 64 |
| 2 | Fila de HOLDOUT-EXPOSICIONES.md antes del primer make check y antes de la primera corrida de cada día | Hecho | dos filas del 2026-11-09 (apertura y corridas) |
| 3 | FASE 0 con inventario medido, auditor y PARADA | Hecho | §0 y «Lo que necesito que decidas»; Apéndice A |
| 4 | La respuesta del consultor copiada tal cual (encargo e informe) y aplicada punto por punto | Hecho | «Respuesta del consultor…» y «Cómo se aplica la respuesta» |
| 5 | (a) La bitácora por día y sesión: tomas, escenarios, zonas, puntos, la orden de cada uno o por qué no, y el gate de cada prohibición | Hecho | F2; anexo `bitacora.DIAGNOSTICO.<día>.txt` |
| 6 | Punto 0: el gate que prohíbe, apuntado en el intérprete, solo como registro, con test de un gate que dispara y uno desconocido | Hecho de otra forma (desviación decidida por el consultor: el encargo decía no tocar el intérprete) | F2; `test_decisiones.py`; F4.1 |
| 7 | La bitácora no cambia lo que el motor decide: tres rutas, mutación, determinismo, sin mirar al futuro | Hecho | F2 (tests sintéticos); F4.2 (base con y sin bitácora, mismos recuentos y operaciones) |
| 8 | Punto 1: etiqueta DIAGNOSTICO-DECISIONES con nombrado propio; `nombre_etiquetado` solo A+cifras, con un test que rompe en main | Hecho | F3; el test se ejecutó con el `diagnostico.py` de main (ver «Los guiones y comandos») |
| 9 | (b) La ablación de las 32 VIGENTE, una a una, por id | Hecho | F3, F4.3 |
| 10 | Punto 3: `motor decisiones` con `--carpeta` obligatoria dentro de `data/`, con test; perfil y fase por defecto; sin `--depuracion` | Hecho | F3 |
| 11 | `motor arnes` y `motor visor` sin cambios | Hecho | F3 (el diff de `cli.py` solo añade); F4.1 |
| 12 | Salida sin R, PnL ni porcentajes; DIAGNOSTICO en el nombre y en cada línea, con test | Hecho (con b11: la bitácora lleva el lote y el desenlace de cada orden; decisión 7 de la PARADA) | F3; anexo |
| 13 | Punto 4: tests solo sobre el fixture sintético | Hecho | `test_decisiones.py` |
| 14 | Sin ablación, la lista de reglas es la de `motor arnes` | Parcial: el test solo comprueba que sin ablación no se quita nada y que son 32 (revisor, b8); la igualdad con `motor arnes` la sostienen que los dos caminos construyen el motor con `construir_motor_cableado` y que la base de F4.2 cuadra con F4.1 | F3, F4.2 |
| 15 | NOTA en ADR-0092 §6 y en el docstring de la ablación | Hecho | ADR-0092; `decisiones.py` |
| 16 | Punto 5: sin fila en el Marcador, declarado como excepción a HOJA-DE-RUTA.md:817 | Hecho | «Desviaciones», 2 |
| 17 | Punto 6: un proceso; motor y estado nuevos por corrida; la base dos veces idéntica entre sí y a F4.1; por debajo de 1,5 GiB | Hecho | F4.2, F4.3 |
| 18 | Punto 7: el control lo calcula la bitácora; delta cero o PARADA; RN-008 y las de fuera, medidas y explicadas | Hecho | F4.2, F4.3 |
| 19 | Punto 8: `traza_por_cierre.py` sin tocar, y en qué difiere la bitácora; la zona reutilizada en el análisis | Hecho | F2; F5 (5.1 y 5.3) |
| 20 | Punto 9: `fix/trazas-ablacion`; NA:F fuera de todo el bloque de R4.4; ~4 h | Hecho (la CI, ver 33) | «Desviaciones»; 5.6 |
| 21 | Punto 10: F1 en su commit; F2-F4 sin esperar con la PARADA condicional; F5, revisor y entrega | Hecho | este orden; ninguna PARADA condicional |
| 22 | (d) F1: el recorte por (a)-(e) | Parcial, corregido: la línea de guardia-g1 se quedó sin acortar (revisor, b4); acortada en el commit de las correcciones | F1 y su corrección |
| 23 | F4.1: diff de 0 bytes contra la línea base | Hecho | F4.1 |
| 24 | F4.2: la bitácora de los cuatro días, sesiones enteras, al anexo | Hecho | anexo |
| 25 | F4.3: la tabla de las 32 con las filas de §8, las de más, el Δ de órdenes y los fallos | Hecho | F4.3 |
| 26 | (c) F5: las 5 de 07-03 con (i)-(iii), (a), (b) y las clases | Hecho, con dos límites declarados tras el revisor (b5 y b6) | 5.1 |
| 27 | F5: las 13 «a la rama de trazas» | Hecho (corregido tras el revisor, a2: A-20 RESUELTA) | 5.2 |
| 28 | F5: la pendiente con dueño (07-14, 04-13 08:47, 07-02 12:25 y 12:45) | Hecho | 5.3 |
| 29 | F5: una línea por regla con delta, sin «quitar la regla» | Hecho | 5.4 |
| 30 | F5: preguntas a la sesión 7 como hecho medido y sin sugerir la respuesta | Hecho, corregidas tras el revisor (b7 y a2) | 5.5 |
| 31 | F5: propuestas de cierre comprobadas con `test_hoja_de_ruta.py` sobre una copia | Hecho | 5.6; guion en el anexo |
| 32 | Informe con el encargo frente a lo hecho, las desviaciones y los comandos tal como se ejecutaron | Hecho (comandos completados tras el revisor, b3 y b9) | esta tabla; «Desviaciones»; «Los guiones y comandos» |
| 33 | CI de Linux por `fix/trazas-ablacion` | Hecho: run 42740007047 sobre 9469bbf (empujado por Aleks a `fix/trazas-ablacion`): `make check` con 1 failed, 3310 passed, 48 skipped; el único fallo, el esperado de `RITUAL.md`: `test_state_check_ok_on_real_repo` («PROJECT_STATE declara la rama 'trabajo/trazas-ablacion'; la rama actual es 'fix/trazas-ablacion'») | «Estado» |
| 34 | Revisor con los 6 alcances, pegado al final | Hecho | Apéndice B |
| 35 | PARADA final con las clases y «Rama lista para revisión, NO cerrada.» | Hecho | «PARADA final»; «Estado» |

## Los guiones y comandos de la sesión (revisor, b3)

Los guiones de análisis vivieron en la carpeta de trabajo de la sesión, fuera del repo. Para que se
puedan leer, su texto va al anexo, en `anexos/TRAZAS-ABLACION/guiones/`, como `<nombre>.py.txt`
(no se ejecutan desde ahí; ninguno escribe en el repo salvo `aplicar_acortadas.py` y `aplicar_b4.py`,
sobre `PROJECT_STATE.md` y `HISTORIA.md`, con la ruta por argumento). `<sp>` es la carpeta de trabajo de la sesión.

| Para qué | Guion | Comando, tal como se ejecutó |
|---|---|---|
| Los tests primero (F2 y F3), y el test de `nombre_etiquetado` con el `diagnostico.py` de main (el fichero aún no se había tocado: «DID NOT RAISE ValueError») | — | `uv run pytest -q tests/unit/test_decisiones.py` |
| F1: los candidatos de (e), por bytes con el salto | `td.py` | `uv run python <sp>/td.py PROJECT_STATE.md` |
| F1: el corte válido más largo de las 9 líneas | `acortar.py` | `uv run python <sp>/acortar.py PROJECT_STATE.md <sp>/acortadas.json` |
| F1: aplicar los cortes y escribir el bloque de HISTORIA | `aplicar_acortadas.py` | `uv run python <sp>/aplicar_acortadas.py PROJECT_STATE.md docs/state/HISTORIA.md <sp>/acortadas.json` |
| F1, corrección: (e) sobre TODAS las líneas de Technical Debt de más de 200 bytes | `recontar_e.py` | `PYTHONUTF8=1 uv run python <sp>/recontar_e.py PROJECT_STATE.md` |
| F1, corrección: el ahorro conservando la cita de cada línea | `citas_e.py` | `PYTHONUTF8=1 uv run python <sp>/citas_e.py PROJECT_STATE.md` |
| F1, corrección: acortar la de guardia-g1 y ampliar HISTORIA | `aplicar_b4.py` | `PYTHONUTF8=1 uv run python <sp>/aplicar_b4.py PROJECT_STATE.md docs/state/HISTORIA.md` |
| F5: la bitácora en torno a unas horas | `en_hora.py` | `uv run python <sp>/en_hora.py anexos/TRAZAS-ABLACION/bitacora.DIAGNOSTICO.<día>.txt <sesión> <HH:MM,...>` |
| Fase 0: los cuatro días frente a `casos_reservados` y `casos_ocultos` (solo recuentos, sin ids) | `cuatro_dias.py` | `uv run python <sp>/cuatro_dias.py` (desde la raíz del repo) |
| F4.3: el resumen por regla | `resumen_ablacion.py` | `uv run python <sp>/resumen_ablacion.py data/trazas-ablacion/ablacion/ablacion.DIAGNOSTICO.vigentes.txt` |
| F4.3: el cruce con §8 («0 sin fila») | `cruce_s8.py` | `PYTHONUTF8=1 uv run python <sp>/cruce_s8.py data/trazas-ablacion/ablacion/ablacion.DIAGNOSTICO.vigentes.txt docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/patrones-cuenta-por-mes.txt` |
| 5.6: las propuestas de cierre con `test_hoja_de_ruta.py`, en memoria | `simular_cierre.py` y `propuesta_cierre.txt` | `PYTHONUTF8=1 uv run python <sp>/simular_cierre.py <repo> <sp>/propuesta_cierre.txt` |

## Desviaciones

1. **El intérprete se tocó** (`engine/interprete.py`), aunque el encargo decía «sin tocar el
   intérprete»: lo decidió el consultor (respuesta a la fase 0, punto 0), solo como registro, y la
   prueba de que no cambia ninguna decisión es F4.1 (diff de 0 bytes).
2. **Sin fila en el Marcador**, como excepción a `docs/plan/HOJA-DE-RUTA.md:817` (punto 5): la
   corrida base repite la línea base con un diff de 0 bytes y no es una corrida nueva; las
   ablaciones son diagnóstico. La orden de cierre lo dirá.
3. **La rama de CI es `fix/trazas-ablacion`** (`RITUAL.md:102`), no `fix/trabajo-trazas-ablacion`
   (punto 9).
4. **`NA:F` fuera de todo el bloque de R4.4** al proponerla HECHA, no solo de sus Refs (punto 9;
   5.6 b).
5. **Las corridas llevaron unas 3 h** (F4.1 6 min, F4.2 9,5 min, F4.3 2 h 18 min), dentro de las ~4 h
   del punto 9.
6. **El control son 8 reglas, no las 11 del encargo** (punto 7): lo calculó la bitácora; RN-007,
   RN-021 y RN-022 quedan desconocidas en todos los eventos y salen del control, y dan delta cero
   igual.
7. **Error mío, corregido**: en la fase 0 conté 25 líneas de Technical Debt candidatas por (e) donde
   eran 22 (tres ya acortadas llevan la marca tras una cita); corregido en F1.
8. **Error mío, corregido tras el revisor (b4)**: F1 dejó sin acortar la línea de guardia-g1, que
   ahorraba 152 bytes; acortada en el commit de las correcciones, y recontadas todas (F1).
9. **La medida (a) de 07-03 no distingue unas órdenes de otras** con una orden stop (revisor, b5):
   declarado en 5.1, y la clase «regla desconocida» pasa a ser del mecanismo (PARADA, decisión 1).
10. **El test de «sin ablación, la lista de `motor arnes`» es débil** (revisor, b8): no se cambia en
   esta rama; lo que sostiene la igualdad es F4.2 frente a F4.1 («El encargo, punto por punto», 14).

## Los `make check` de la rama

| Commit | Resultado |
|---|---|
| apertura (29561efd) | 3343 passed, SELLO sobre 35974bc4, pico 310 MiB |
| fase 0 (50c26648) | el primero, rojo (5 failed: `knowledge validate` por citar un ADR inexistente, el 0087); el segundo, 3343 passed, SELLO sobre 17767f27, pico 310 MiB |
| F1 (5d281ed7) | 3343 passed, SELLO sobre 39d13681, pico 309 MiB |
| F2 y F3 (1f95cafe) | 3359 passed, SELLO sobre f237a9ed, pico 310 MiB |
| F4 y F5 (4ac3810) | 3359 passed, SELLO sobre 3c66a635, pico 309 MiB |
| correcciones del revisor (9469bbf) | 3359 passed, SELLO sobre 2cade966, pico 309 MiB |
| la CI y el estado final (este) | en el mensaje del commit |

## PARADA final · Las clases, para que decidas

Todas son PROPUESTAS; ninguna operación de más se llama error. Reescrita tras el revisor (a2, b5, b6
y b11; su informe, en el Apéndice B).

0. **07-03 07-11, o4, o6 y o8 (y la P2 del trader de las 09:24, con o6): «contradicción con lo
   fijado»** (punto de M1, llenado con mecha; v12 pide cuerpo, S-18 y A-32 dan la mecha por buena
   en M1). Opciones: (a) contradicción con lo fijado; (b) sin clase hasta la sesión 7. Recomiendo
   (a): es lo que mide la bitácora con el criterio del punto 2 (la vela del llenado, no la medida
   (a)). Coste de (b): la tensión entre v12 y S-18 se queda sin nombre en la lista de la sesión 7.
1. **07-03 07-11, o4, o5, o6 y o8: «regla desconocida: cuándo se coloca la orden respecto de la
   ruptura»**. La condición del punto 2 se cumple, pero por el mecanismo y no por estas cuatro:
   toda orden stop del bot se llena antes de que ninguna M1 cierre más allá (límite de (a), 5.1: 20
   «ANTES» y 0 «DESPUÉS» en los cuatro días). Opciones: (a) la clase para las cuatro, dicha como del
   mecanismo de ADR-0064, y la pregunta 1 de 5.5 a la sesión 7; (b) ninguna clase de fila, y la
   pregunta igual, como pregunta sobre ADR-0064. Recomiendo (b): una clase que sale igual en todas
   las órdenes no distingue estas cuatro, y la pregunta es la misma. Coste de (b): las cuatro filas
   se quedan con una sola clase (las tres de «contradicción») o ninguna (o5).
2. **07-03 07-11, «error nuestro»: ninguna**, con el límite de (iii): las tres tomas cierran con
   cuerpo y ningún punto es un nivel de M15 de su instante; con niveles de M15 anteriores de la
   sesión no se ha comparado (y 1.14496 queda a 4 puntos del bajo de M15 en 1.14500). Opciones:
   (a) ninguna fila es «error nuestro»; (b) mantener la sospecha hasta medir esos niveles
   anteriores (cambio de la bitácora, en otra rama). Recomiendo (a): nada medido la sostiene; el
   límite queda escrito. Coste de (b): una rama más antes de la sesión 7.
3. **Las 13 «a la rama de trazas»: sin clase**, con el hecho del gate (RN-009 en las de las horas
   del trader de 07-02, 07-03 y 07-14) y las P5 como operaciones de más. El número de zonas de
   control ya está fijado (A-20 RESUELTA: una; con dos se descarta). Opciones: (a) sin clase, y la
   pregunta 2 de 5.5 (qué zonas cuenta el trader como de control) a la sesión 7; (b) «aplicado como
   está escrito», porque RN-009 cumple A-20. Recomiendo (a): el trader entró en todas esas horas, así
   que o él cuenta las zonas de otra manera o se saltó su regla, y eso no lo dice nada medido. Coste
   de (b): se da por bueno cómo cuenta el motor sin la voz del trader.
4. **La pendiente con dueño**: 07-14 (o10, o12 y o14 no son del mismo barrido; RN-016 aplicado como
   está escrito: sí); 04-13 08:47 y 07-02 12:25 y 12:45, gate RN-009; 07-02 14:10 y 14:23, tres
   gates (RN-001, RN-009 y RN-016). Opciones: (a) cerrada con estos hechos; (b) seguir abierta.
   Recomiendo (a): cada pregunta de RECORRIDA-CONSTRUCCION-2.md:1355-1358 tiene su respuesta medida.
5. **La zona ligada al escenario anterior (07-03 09:23 y 09:35)**: Technical Debt (5.6 c), sin tocar
   el motor. Opciones: (a) Technical Debt; (b) rama de motor ya. Recomiendo (a): cambiaría lo que
   el motor decide sin una regla del trader.
6. **Las propuestas de cierre (5.6)**: F nueva, R4.4 HECHA y tres líneas de Technical Debt, todas
   comprobadas con `test_hoja_de_ruta.py` (repetido tras las correcciones). Las aplica la orden de
   cierre, si las das por buenas.
7. **El lote y el desenlace en la bitácora** (revisor, b11): cada orden lleva su lote y cada
   escenario o posición su desenlace («ganancia», «cerrada por stop/objetivo»); no son R, PnL ni
   porcentajes. Opciones: (a) se quedan; (b) fuera, en otra rama. Recomiendo (a): sin el lote no se
   ve RN-027 ni el margen, y el desenlace es el hecho que explica RN-016. Coste de (a): un dato de
   resultado por operación en un fichero de diagnóstico.
8. **La línea de Technical Debt de los skills (`Fuente:`)** (corrección de F1): su único corte cae
   dentro del nombre del trailer `Fuente:`. Opciones: (a) entera (lo leo como un id); (b) acortada
   en el cierre (ahorra 73 con su cita). Recomiendo (a): (e) prohíbe cortar dentro de un id, y el
   nombre del trailer se usa como tal en CLAUDE.md. Coste de (a): 73 bytes.

## Apéndice B · El informe del revisor (2026-11-09), tal cual

## Informe del revisor · trabajo/trazas-ablacion · 2026-11-09

Revisión de solo lectura: no he escrito, ejecutado tests, `make check`, `uv run` ni el arnés (hay un `make check` en marcha). He revisado lo commiteado (29561efd..1f95cafe) y lo estadiado (F4/F5, la fila de HOLDOUT y el anexo).

**Lo más importante, antes del detalle:**
- **Dos cosas impiden declarar la rama lista**, y las dos están pendientes: la CI de `fix/trazas-ablacion` con su número de run, y el commit de F4/F5. Faltan también la frase final y pegar este informe.
- **El golden se cumple.** Lo he comprobado yo: la salida de F4.1 y la línea base tienen el mismo sha256.
- **La pregunta 2 para la sesión 7 vuelve a preguntar algo que el trader ya respondió** (A-20 RESUELTA, zonas_control_max_por_esquema = 1 CONFIRMED). La recomendación 3 de la PARADA se apoya en «no hay voz del trader», y eso es falso.
- **La medida (a) de 07-03 no puede dar «DESPUÉS» con una orden stop.** En las cuatro órdenes, colocación y llenado caen en el mismo minuto, así que la ventana medida está vacía. La recomendación 1 de la PARADA se apoya en ella.

### Eje (a) · Reglas de la casa
Resumen: 0 bloquea, 2 importa, 1 menor.

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| a1 | importa | **Afirmación que el código no sostiene.** El informe dice que RN-012 y RN-027 «no pueden dar delta por construcción», y la propuesta de Technical Debt 5.6 (c) lo repite. Pero la comparación no mira solo la operación: compara también órdenes no enviadas, rechazos y cuentas suspendidas. Un lote distinto (RN-027 redondea el lote) puede mover esos recuentos por el margen, por el lote mínimo de ADR-0081 o por el saldo. Lo medido es solo que quitarlas dio delta cero; lo de «por construcción» no se sostiene. | `C:\Users\USER\Desktop\Bot v3\docs\validation\TRAZAS-ABLACION.md:753-756` y `:948-950`. `C:\Users\USER\Desktop\Bot v3\src\botsito\engine\decisiones.py:170-174` y `:207-210` (`Resumen` compara `no_enviadas`, `rechazos` y `suspendidas`). `src/botsito/engine/primitivas_broker.py:519-523` (`redondear_lote` cambia `o.lote`, y el comentario remite al «no se coloca» de `colocar_orden_limite`). |
| a2 | importa | **«No hay voz del trader sobre cuántas zonas de control admite el esquema» es falso.** A-20 está RESUELTA desde el 2026-09-11 («solo 1 zona control bro. si hay 2 se descarta», fb-2026-09-09-sesion-01-1b2203b0), y `zonas_control_max_por_esquema = 1` está CONFIRMED con esa fuente. En cambio: la clase «sin clase» de 5.2 y 5.3, la pregunta 2 de 5.5 («¿Cuántas zonas de control dejas que se desarrollen…?») y la recomendación 3 de la PARADA no lo citan. La pregunta 2 re-pregunta una RESUELTA sin decirlo (se busca en el repo antes de preguntar al trader; una RESUELTA se reabre con REOPEN). Lo que el trader no ha fijado es, como mucho, **cómo** cuenta el motor las zonas. | `TRAZAS-ABLACION.md:825`, `:898-902`, `:1019-1022`. `C:\Users\USER\Desktop\Bot v3\knowledge\spec\ambiguedades.yaml:422-436` (A-20, RESUELTA). `C:\Users\USER\Desktop\Bot v3\knowledge\spec\parametros.yaml:1071-1087`. |
| a3 | menor | La tabla F4.3 dice «Δ órdenes = órdenes colocadas frente a 1150». Pero 1150 incluye las 32 rechazadas al colocar (871 + 247 + 32), así que «colocadas» no es exacto. | `TRAZAS-ABLACION.md:704` y `:637`. `docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/cuenta-por-mes.txt:3147`. |

Comprobado sin hallazgos:
- **Contrato** (emulado, porque `contrato_rama.py` no lo ejecuté): los 19 ficheros de `git diff --name-status main` están dentro de `rutas_permitidas`, y ninguno toca `rutas_protegidas` (knowledge/, scripts/, Makefile, .claude/, docs/plan/, RECORRIDA-CONSTRUCCION-2, VIDEO-JULIO).
- **Trailer `Fuente:`**: no hace falta; ningún commit toca `knowledge/spec` ni `knowledge/cases`.
- **Holdout**: nada toca `knowledge/cases/holdout/`. No hay ítems de evidencia ni registros de feedback nuevos, ni cambios en manifests ni en corpus.
- **Ambigüedades**: no se tocan. No hay `cita` nueva, así que las tres guardias no aplican.
- **ADR-0092**: solo se añade la NOTA de §6 y su `## Estado` sigue en `ACTIVE`.
- **Informes y registros solo crecen**: HOLDOUT-EXPOSICIONES.md solo añade filas, y HISTORIA.md solo añade (la única línea `-` del diff es la cabecera). El Archivo 64 está en `HISTORIA.md:16494`.
- **Cinco citas comprobadas contra su fuente**: `ambiguedades.yaml:864-898` (A-32 y la frase «en M1 la mecha siempre vale»); `strategy_spec.yaml:1528-1531`; `parametros.yaml:501-518` (mecha, CONFIRMED); `HOJA-DE-RUTA.md:817`; `RECORRIDA-CONSTRUCCION-2.md:1355-1358`. También la cita de v12 en VIDEO-JULIO.md:700 (§7 #6).
- **Respuesta del consultor**: la copia del encargo (`:115-154`) y la del informe (`:430-469`) son idénticas (mismo md5).

### Eje (b) · Encargo
Resumen: 1 bloquea, 7 importa, 3 menor. Requisitos: 35 hechos, 5 parciales, 4 no hechos.

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 1 | Apertura con abrir-rama (encargo, contrato, Archivo 64) | Hecho | commit 29561efd; `HISTORIA.md:16494` |
| 2 | Base comprobada con git | Hecho | `TRAZAS-ABLACION.md:7-13` |
| 3 | Fase 0, puntos 0.1-0.6, con auditor | Hecho | `:15-288`; Apéndice A en `:331-424` |
| 4 | PARADA «Lo que necesito que decidas» | Hecho | `:290-329` |
| 5 | Respuesta del consultor copiada tal cual (informe y encargo) | Hecho | mismo md5 en los dos bloques |
| 6 | F1: recorte por (a)-(e), texto literal en HISTORIA, cifra antes y después | Parcial | b4. Las 9 líneas pasan literal: el md5 de las líneas `-`/`+` del diff de PS coincide con el bloque `HISTORIA.md:16659-16691`. 23.876 → 21.760 bytes, medido con `wc -c` |
| 7 | F1: la Next Action no se toca | Hecho | el diff de PS no toca esa sección |
| 8 | Punto 0: el gate se apunta en el intérprete, solo como registro, con test de un gate que dispara y otro desconocido | Hecho | diff de `interprete.py`. `quizas_prohibidos` pasa a dict y se sigue mirando con `in` sobre claves, así que bloquea lo mismo. `tests/unit/test_decisiones.py:163-198` |
| 9 | F4.1: diff de 0 bytes contra cuenta-por-mes.txt | Hecho | `sha256sum`: `e6ca305b…798054` en los dos ficheros |
| 10 | F2: con la bitácora el motor decide lo mismo | Hecho | `test_decisiones.py:111-120`. En F4.2 la base con bitácora y la base sin ella dan los mismos recuentos y los mismos conjuntos de operaciones (`ablacion.DIAGNOSTICO.base.txt:1-2`) |
| 11 | F2: mutación comprobada | Hecho | `test_decisiones.py:123-136` |
| 12 | F2: cada prohibición con todos sus gates | Hecho | `decisiones.py:477-496`; `test_decisiones.py:184-198` |
| 13 | F2: sin mirar al futuro | Hecho | `test_decisiones.py:221-237`. `_llenado` solo pinta la vela si `minuto + 1 <= c.instante` (`decisiones.py:546`) |
| 14 | F2: determinista | Hecho | `test_decisiones.py:201-212` |
| 15 | Punto 1: DIAGNOSTICO-DECISIONES, nombrado propio, `nombre_etiquetado` y su test que rompe en main | Hecho | `diagnostico.py:166`, `:184-186`; `test_decisiones.py:243-251`. La demostración en main va sin comando: ver b3 |
| 16 | Punto 3: `motor decisiones`, `--carpeta` obligatoria dentro de data/, con test | Hecho | `cli.py` (parser `decisiones`, `required=True`); `decisiones.py:62-76`; `test_decisiones.py:254-267`, `:287-296` |
| 17 | F3: `motor arnes` y `motor visor` sin cambios | Hecho | el diff de `cli.py` solo añade. `arnes.py` y `test_diferencias_por_operacion.py` no están en el diff |
| 18 | F3: salida etiquetada, sin R, PnL ni %, con test | Hecho | `test_decisiones.py:49`, `:213-215`, `:362-364`. 0 líneas sin etiqueta en el anexo |
| 19 | F3: un id que no sea VIGENTE da un error que lo nombra | Hecho | `test_decisiones.py:299-306` |
| 20 | F3: sin ablación, la lista de reglas es idéntica a la de main | Parcial | b8 |
| 21 | F3: el control da delta cero | Hecho | `test_decisiones.py:335-370`. `ablacion.DIAGNOSTICO.vigentes.txt`: las 8 marcadas `[control]` dan «sin delta» |
| 22 | F3: NOTA en ADR-0092 §6 y en el docstring | Hecho | diff del ADR (solo añade); `decisiones.py:4-9` |
| 23 | Punto 4: los tests solo sobre el fixture sintético | Hecho | `test_decisiones.py` importa de `test_cableado` y solo lee el spec |
| 24 | Punto 6: un proceso, motor nuevo por corrida, la base dos veces igual, por debajo de 1,5 GiB | Hecho | `base.txt:1-2`. Picos en las salidas de pantalla: 636,2, 633,3 y 632,9 MiB |
| 25 | Punto 7: el control lo calcula la bitácora; RN-008 y las de fuera del control, explicadas | Hecho (ver a1) | `base.txt:3`; `TRAZAS-ABLACION.md:742-758` |
| 26 | F4.2: la bitácora de los cuatro días, al anexo | Hecho | las copias del anexo y las de `data/trazas-ablacion/` tienen el mismo sha256 |
| 27 | F4.3: la tabla de las 32, con las filas de §8 | Hecho | muestreo abajo |
| 28 | F5: 07-03 con (i)-(iii), (a), (b) y las clases | Parcial | b5, b6 |
| 29 | F5: las 13 «a la rama de trazas» | Hecho (ver a2) | 5.2. RN-009 comprobado en las horas del trader en las bitácoras de 07-02, 07-03 y 07-14 |
| 30 | F5: la pendiente con dueño y la zona reutilizada (punto 8) | Hecho | 5.3, que coincide con la bitácora de 07-14 (zonas 79 y 80 en el escenario 1, zona 116 en el 2) y con la de 04-13 a las 08:47 (solo RN-009) |
| 31 | F5: la ablación por regla, sin conclusiones | Hecho | 5.4 |
| 32 | F5: preguntas a la sesión 7, como hecho medido y sin sugerir la respuesta | Parcial | a2, b7 |
| 33 | F5: propuestas de cierre comprobadas con test_hoja_de_ruta | Hecho (sin comando) | 5.6; ver b3 |
| 34 | Punto 8: frente a traza_por_cierre.py | Hecho | `TRAZAS-ABLACION.md:575-580` |
| 35 | Punto 5: el Marcador, como excepción declarada | Hecho | `:977-979` |
| 36 | Punto 9: las desviaciones | Hecho | `:972-990` |
| 37 | HOLDOUT: fila del día antes de la primera corrida | Hecho | ver alcance (3) |
| 38 | Nada de lo que no se toca | Hecho | `git diff --name-status main` |
| 39 | Informe con los comandos tal como se ejecutaron | Parcial | b3 |
| 40 | CI por `fix/trazas-ablacion`, con el número de run | No hecho | `TRAZAS-ABLACION.md:1035-1037` («Falta la CI») |
| 41 | El informe del revisor, pegado al final | No hecho (es este) | la tabla remite a un «Apéndice B» que no existe (`:970`) |
| 42 | PARADA final con las clases | Hecho | `:1002-1031` |
| 43 | La frase «Rama lista para revisión, NO cerrada.» | No hecho (pendiente) | `## Estado` dice EN CURSO |
| 44 | «El encargo, punto por punto» (E5, skill entregar-rama) | No hecho | b2 |

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| b1 | bloquea | **La rama no está lista.** El encargo pide la CI de Linux por `fix/trazas-ablacion`, con su run, ANTES de declararla lista, y no se ha hecho. F4/F5, la fila de HOLDOUT y el anexo están estadiados sin commitear. Faltan la frase final y este informe pegado. Mientras sea pendiente es correcto; como entrega, bloquea. | `git status --short` (8 ficheros estadiados); `TRAZAS-ABLACION.md:1035-1037`; encargo `:107` |
| b2 | importa | **Falta la tabla «El encargo, punto por punto»** de entregar-rama: requisitos numerados, cada uno con Hecho / Parcial / No hecho / Hecho de otra forma, incluidas las respuestas del consultor. Lo que hay son dos tablas gruesas: «El encargo frente a lo hecho», con 12 filas y todas «sí», y «Cómo se aplica la respuesta», que dice dónde se aplica cada punto pero no su estado. | `TRAZAS-ABLACION.md:955-970`, `:471-485`; `.claude/skills/entregar-rama/SKILL.md:46-50`, `:97` |
| b3 | importa | **Faltan comandos que el encargo pide** («los comandos tal como se ejecutaron») y la skill exige para el test que rompe en main (comparar-con-main, con comando y salida). No hay comando para: los tests escritos primero y el «DID NOT RAISE» de `nombre_etiquetado` con el `diagnostico.py` de main; `cuatro_dias.py` y `acortar.py` (guiones fuera del repo, sin texto ni comando); el cruce con §8 («0 sin fila»); y la comprobación en memoria de 5.6. | `TRAZAS-ABLACION.md:24`, `:502`, `:528-532`, `:697-700`, `:906-912` |
| b4 | importa | **Alcance (4), F1: una línea se quedó sin acortar.** La lectura escrita es «160 bytes como mucho, contando el «- »». Con ella, el corte largo de la línea «Riesgo residual de `trabajo/guardia-g1` (§4.3)…» mide 161 bytes, así que no vale. El corte válido es tras «(§4.3)», a unos 49 bytes, igual que hizo F1 con la de ADR-0088 (43 bytes). Así ahorra unos 150 bytes, no menos de 60. El informe la cuenta entre «las otras 13 [que] ahorrarían menos de 60». Probable causa: `acortar.py` contó caracteres y no bytes. Ese corte mide 159 caracteres («árbol» y «§» ocupan 2 bytes cada uno), pero no lo puedo ver porque el guion no está en el repo. | `grep -o '^- Riesgo residual de \`trabajo/guardia-g1\`.*cuenta como test del repo' PROJECT_STATE.md \| wc -c` → 162, es decir 161 + salto de línea. `docs/validation/MARGEN-PENDIENTE.md:312-314`; `docs/state/README.md:81-92`; `TRAZAS-ABLACION.md:516` |
| b5 | importa | **Alcance (5): la medida (a) no puede distinguir nada con una orden stop.** El código mira la ventana entre la colocación y el llenado (`m1_entre(colocada, minuto del llenado)`). En las cuatro órdenes de 07-03, colocación y llenado caen en el mismo minuto (o4 colocada al cierre de las 08:02 y llenada a las 08:02:06; o5 08:03 / 08:03:31; o6 09:24 / 09:24:42; o8 09:35 / 09:35:41): la ventana está vacía. Además, una compra stop se llena en el tick que toca el nivel, antes de que ninguna M1 pueda cerrar por encima, así que «DESPUÉS» es imposible salvo un hueco. En los cuatro días salen 20 «ANTES» y 0 «DESPUÉS». La recomendación 1 de la PARADA («se cumple en las cuatro») se apoya en esto sin decirlo. Tampoco se dice que la ventana empieza en la colocación y no al formarse el punto. | `decisiones.py:543-561`. `grep -c ANTES` en las 4 bitácoras: 2, 7, 6, 5; `grep -c DESPUES`: 0 en las 4. `bitacora.DIAGNOSTICO.2026-07-03.txt` (líneas de o4, o5, o6, o8). `TRAZAS-ABLACION.md:808-813`, `:1011-1015` |
| b6 | importa | **Alcance (5): el «no» de (iii) no quiere decir «no viene de M15», y no está declarado.** (iii) solo compara el punto con la toma del escenario vigente y con la liquidez de M15 de ese instante, por igualdad exacta en puntos. Un nivel de M15 ya tomado antes en la sesión sale «no». Ejemplo en 07-14: la zona 115 (o13) a las 12:28 tiene el punto 1.13990, que es el bajo de M15 de la toma de las 11:19, y sale «no». Las zonas 113 y 114, con el mismo nivel, a las 12:25-12:26, salían «SI». En 07-03 sí comprobé que los tres niveles de las tomas (1.14500, 1.14512, 1.14507) no coinciden con los puntos (1.14496, 1.14545, 1.14517). Lo que no queda medido son otros niveles de M15 anteriores, ni la distancia de 4 puntos entre 1.14496 y 1.14500. 5.1 dice «de su instante», que es exacto, pero no dice ese límite al descartar «error nuestro». | `decisiones.py:401-411`; `bitacora.DIAGNOSTICO.2026-07-14.txt` (12:25-12:28); `TRAZAS-ABLACION.md:800-802`, `:1016-1018` |
| b7 | importa | **La pregunta 1 de 5.5 sugiere la respuesta.** «¿…y qué vela tiene que cerrar?» da por hecho que tiene que cerrar alguna vela, que es justo lo que está en tensión con S-18 («en M1 la mecha siempre vale»). El encargo pide las preguntas «sin sugerir la respuesta». | `TRAZAS-ABLACION.md:819`, `:896-897`; encargo `:103` |
| b8 | importa | **El test de «sin ablación, la lista es la de main» es una tautología.** Compara `sin_regla(reglas, None, vigentes)` con la misma `reglas` de la que sale: `list(reglas) == reglas`. No pasa por el camino de `motor_decisiones` ni compara con main. Lo único que lo respalda de verdad es que la base de F4.2 cuadra con F4.1. | `test_decisiones.py:309-316`; `decisiones.py:105-106` |
| b9 | menor | Los comandos de F4 no están tal como se ejecutaron: las salidas de pantalla acaban en una línea `exit=0` que no sale del comando escrito, así que hubo algo más (probablemente un `echo exit=$?`). | `data/trazas-ablacion/f41-pantalla.txt` (cola: `exit=0`); `TRAZAS-ABLACION.md:617-619` |
| b10 | menor | La tabla del encargo remite a un «Apéndice B» que todavía no existe. | `TRAZAS-ABLACION.md:970` |
| b11 | menor | La bitácora no lleva R, PnL ni %, pero sí el lote de cada orden y el desenlace («escenario terminado: ganancia», «cerrada por stop/objetivo»). No incumple la letra del encargo; lo señalo por si el consultor lo quiere fuera. | `grep -oiE … bitacora.DIAGNOSTICO.2026-07-03.txt`: 74 «ganancia»; `decisiones.py:511-512` (`lote {o.lotes}`) |

**Lo que la rama hace y el encargo no pide:** nada que no esté justificado. `--meses`, el veto a `data/manifests/` y el código de salida 4 de la PARADA vienen del diseño aprobado en la fase 0 o los declara el informe (`:555`).

**Los seis alcances, uno a uno**

(1) **Nada cambia lo que el motor decide: se cumple.**
- El intérprete solo añade registro. `prohibidos.update` y `bloqueadas.add` no cambian, y `quizas_prohibidos` pasa a dict pero se sigue mirando con `in` sobre claves, así que bloquea lo mismo (diff de `interprete.py`, `:264-291`, `:339-355`).
- `cableado.py` solo llama al observador si no es None, después de la traza y de las cancelaciones (diff, `:442-449`).
- Golden comprobado por mí: `sha256sum` de `data/trazas-ablacion/cuenta-por-mes.txt` y del de RECORRIDA-CONSTRUCCION-2 dan `e6ca305ba31c6307…98054` los dos.
- La mutación está en `test_decisiones.py:123-136`.
- Matiz: sobre la construcción real, la equivalencia «con bitácora = sin ella» se ve por el `Resumen` (recuentos y conjuntos de operaciones), no byte a byte. Byte a byte solo se probó F4.1, que corre sin observador.
- Hallazgo del alcance: b8.

(2) **`motor arnes` / `motor visor`, etiqueta y nombrado: sin hallazgos.**
- El diff de `cli.py` solo añade (`motor_decisiones` y su parser). `_opciones_diagnostico`, `_opciones_simulacion`, `arnes.py` y `test_diferencias_por_operacion.py` no cambian.
- `nombre_etiquetado` (`diagnostico.py:166`, `:184-190`) acepta exactamente las etiquetas que produce `Diagnostico.etiquetas` (`:84-96`: A35, A44, A47 y A27 con su valor, y CUENTA-diaria), así que los nombres de arnés y visor (`visor.py:1131`, `:1135`; `cli.py:2406`, `:2531`, `:2579`) no cambian.
- Los ficheros nuevos se llaman `bitacora.DIAGNOSTICO.<día>.txt` y `ablacion.DIAGNOSTICO.<…>.txt` (`decisiones.py:79-83`).

(3) **Holdout y HOLDOUT-EXPOSICIONES: sin hallazgos.**
- Hay dos filas del 2026-11-09: la de la apertura, antes del primer `make check`, y la de F4, estadiada, que anuncia 37 corridas. Fueron 1 + 2 + 34, que cuadra.
- La de F4 está escrita antes de la primera corrida. Con `stat`: HOLDOUT-EXPOSICIONES.md modificado a las 17:17:00 (-0500); F4.1 acabó a las 17:23:11 tras 364,9 s, así que empezó hacia las 17:17:06. El commit 1f95cafe es de las 17:16:52, así que ninguna corrida fue junto a un `make check`.
- Solo construcción: `motor_decisiones` pasa por `arnes.validar_meses` y `dias_de_construccion`, que niegan medida, meses fuera de construcción y casos ocultos (`arnes.py:107-121`, `:139-162`).
- Los tests no leen velas reales.
- Las tres corridas acabaron a las 19:51 (-0500): antes de medianoche en ese reloj, a las 01:51 del 10 en Madrid. La fila no fija el reloj del «día».

(4) **El recorte: 8 de las 9 líneas cumplen (e); una línea se quedó fuera (b4).**
- Las 9 líneas acortadas son de Technical Debt y pasan literal a HISTORIA (md5 idénticos).
- Prefijos que quedan en PS, en bytes: 115, 143, 154, 134, 135, 90, 43, 44 y 107; todos ≤ 160.
- Los «antes» coinciden con el informe: 322, 301, 325, 285, 447, 282, 498, 456 y 707.
- Todos los cortes van tras «)» o antes de «: », «; » o «. »; ninguno dentro de una ruta ni de un id; la cita del informe se conserva donde la había.
- (a)-(d): ninguna sale. Lo comprobé en una muestra: el ADR 0087 sigue sin existir y la nota de RN-019 sigue igual.
- De las otras 13, medí la del journal: ahorra 58 bytes con su cita, así que se queda bien. La de guardia-g1 no (b4).

(5) **07-03: cita S-18 y A-32, y la bitácora sostiene los hechos de la tabla; fallan la medida (a) y el límite de (iii).**
- 5.1 cita A-32 y S-18 con `ambiguedades.yaml:864-898` y `breaker_m1_criterio_ruptura` con `parametros.yaml:501-518`.
- Comprobado contra `bitacora.DIAGNOSTICO.2026-07-03.txt`:
  - tomas a las 07:57 (cierra 1.14497), 09:23 (1.14510) y 09:35 (1.14493), las tres con cuerpo;
  - puntos 1.14496 (vela de las 08:01), 1.14545 (09:14) y 1.14517 (09:34);
  - M1 del llenado: o4, o6 y o8 con mecha; o5 con cuerpo;
  - zonas 46 y 51 ligadas al escenario anterior en el mismo cierre en que se abre el nuevo.
- La mecánica de los cartuchos está respaldada por `primitivas_broker.py:395-400`.
- Hallazgos del alcance: b5, b6 y b7.

(6) **Ninguna salida nueva lleva R, PnL ni porcentajes: sin hallazgos** (salvo el menor b11).
- `grep -ciE "%|pnl|\bR\b|rentab|usd|saldo|equity|margen|riesgo|beneficio|perdida"` da 0 en los seis ficheros del anexo, salvo «ganancia» en 07-03.
- 0 líneas sin `DIAGNOSTICO-DECISIONES | ` y 0 CR (`grep -cU -P "\r"`).
- `decisiones.py` no calcula dinero (`Resumen`, `:162-180`). El tiempo y la memoria solo salen por pantalla (`cli.py`, `avisar`).

**Muestreo de las cifras de F4 y F5 (más de cinco):**
- **Base**: `base.txt:1` da (31, 192, 24, 1150, 0, 32, 0). Cuadra con `cuenta-por-mes.txt:3147` (871 + 247 + 32), con `:3154-3157` (rechazos 8, 11, 9 y 4) y con `patrones-cuenta-por-mes.txt` (T0 31; P6 en día 24; P5 153 + P6 en sesión 39 = 192).
- **Tabla de reglas de la base**: RN-001, 005, 009, 012, 016, 032 y 036 idénticas a `base.txt`.
- **Recuentos netos por regla**: los de RN-002, 005, 006, 009, 014, 032, 035 y 036 en `vigentes.txt` cuadran con «aparecen / desaparecen». Por ejemplo, RN-009: 31 − 15 + 20 = 36, y 192 + 144 − 88 = 248.
- **Filas de §8 de RN-009**: las 18 nuevas (P2 ×7, P3 ×10, P7 ×1) y las 2 re-emparejadas salen literalmente en `vigentes.txt`. En §8 comprobé la clase de 12 de ellas: 01-02 12:20:20 P2; 01-19 13:36:00 P2; 04-13 06:47:45 y 06:50:00 P3; 07-02 10:25:50 P3; 07-10 07:17:40 P7; 08-04 11:34:50 P3; 01-21 09:32:10 P3; 07-13 11:25:05 P3; y 01-14 06:03:15, 07-17 05:46:05 y 01-09 09:07:50 T0.
- **Filas de las cuatro días en §8**: 07-03 P2 Δ17 con el bot de las 07:24:42; P5 de 07-03 a las 06:02:06, 06:03:31, 07:24:42 y 07:35:41; P2 y P3 de 07-14 a las 09:35, 09:48, 10:44 y 11:06 (UTC).

### Lo que no pude comprobar
- `uv run python scripts/contrato_rama.py` y `uv run botsito state check`: me pediste no ejecutar `uv`. El contrato lo emulé a mano contra el diff.
- `make check` del commit F4/F5: está corriendo. `make-check.log` iba por el 40 %, sin `SELLO` ni `PICO DE MEMORIA`. Los sellos de los cuatro commits anteriores los da por buenos el hook `pre-commit`, que exige el sello; no los leí.
- `pytest tests/unit/test_decisiones.py` y que el test de `nombre_etiquetado` rompa con el `diagnostico.py` de main: no ejecuté tests, y el informe no trae el comando.
- La CI de `fix/trazas-ablacion`: no existe todavía.
- Si `acortar.py` mide en caracteres: el guion vive fuera del repo. Lo infiero de que 161 bytes son 159 caracteres.
- Las comprobaciones en memoria de 5.6 con `test_hoja_de_ruta.py`, y el cruce con §8 entero («0 sin fila»): no tienen guion ni comando; solo muestreé.
- Que la sesión no abriera transcripciones ni fotogramas: nada en el diff ni en HOLDOUT lo indica, pero no hay forma de verlo desde git.
- Si otros niveles de M15, que no sean las tomas, coinciden con los puntos de 07-03 (b6): exigiría correr el motor.

### Comandos ejecutados
1. `git branch --show-current && git merge-base main HEAD && git log --format='%h %s' main..HEAD && git diff --stat main && git status --short`
2. Read: encargo, `contrato.yaml`, `TRAZAS-ABLACION.md` (entero), `decisiones.py`, `test_decisiones.py`, `ablacion.DIAGNOSTICO.base.txt`
3. `git diff main -- src/botsito/engine/interprete.py src/botsito/engine/cableado.py src/botsito/engine/diagnostico.py`
4. Grep `asdict(|fields(|quizas_prohibidos` en `src/botsito`
5. `git diff main -- src/botsito/cli.py`; Read `cli.py:2357-2506`; Grep `validar_meses|dias_de_construccion` en `arnes.py`
6. Grep `PREFIJO_ETIQUETA|DIAGNOSTICO-A` en `src`; `grep -n …; sed -n 160,200p diagnostico.py`; Read `diagnostico.py:60-99`; Grep `nombre_etiquetado` en `src`
7. `grep -nE "\] sin RN-[0-9]+ \| " ablacion.DIAGNOSTICO.vigentes.txt | grep -vE …` (la primera versión, más ancha, se guardó en un fichero de resultados de la herramienta)
8. `grep -E "sin RN-009 \| pareja" …`; `grep -E "sin RN-(006|014|036) \| pareja" …`; `grep -c` de los aparecen y desaparecen de RN-005, 006 y 009; `grep -E "sin RN-(032|036|014) \| (de mas|en dia)" …`
9. `ls` y `grep` en `anexos/RECORRIDA-CONSTRUCCION-2/` (`cuenta-por-mes.txt`, `patrones-cuenta-por-mes.txt`); Read `cuenta-por-mes.txt:3147-3166`; `head -40 patrones-cuenta-por-mes.txt`; `grep` de las filas muestreadas y de los cuatro días
10. `grep -nE …` en las bitácoras de 07-03, 07-14, 04-13 y 07-02 (tomas, escenarios, zonas, órdenes, llenados, bloqueos)
11. Read `ambiguedades.yaml:862-901`, `strategy_spec.yaml:1520-1544`; Grep/sed de `zonas_control_max_por_esquema`, `parametros.yaml:1071-1100`, `ambiguedades.yaml:400-460`; Grep `cartuchos_max`
12. Grep `zona_del_punto(` y otros en `engine`; Read `primitivas_broker.py:380-409` y `:505-534`; grep de RN-012 y RN-027 y `sed -n 485,515p strategy_spec.yaml`
13. Read `docs/state/README.md:50-109`; `git diff main -- PROJECT_STATE.md`; `grep -n` del bloque en HISTORIA; Read `HISTORIA.md:16655-16692`
14. Intento de bucle `while read` sobre el diff: lo negó la guardia (nombre de entorno `IFS`)
15. `git diff main -- PROJECT_STATE.md | grep '^-- ' | cut -c2- | grep -cxFf - docs/state/HISTORIA.md`
16. `wc -c` de PROJECT_STATE en main, en la rama, en 29561efd y en 5d281ed7
17. Comparación por md5sum de las líneas `-`/`+` del diff de PS con `sed -n '16666~3p'` y `'16667~3p'` de HISTORIA
18. `awk -b` para medir prefijos y largos (el segundo `awk`, con programa construido, lo negó la guardia); `grep -o … | wc -c` sobre las líneas de journal, guardia-g1, visor, RN-029, make check, `dias_de_mercado` e ingesta
19. Grep y Read de `MARGEN-PENDIENTE.md:308-319`
20. `git diff main -- docs/validation/HOLDOUT-EXPOSICIONES.md`; `git diff --cached -- …`; `git log --format='%h %ad %s' --date=iso main..HEAD`
21. `stat -c '%y %n'` de las salidas de `data/trazas-ablacion/`, de HOLDOUT-EXPOSICIONES.md y del anexo (el primer intento, encadenado con `date`, lo negó la guardia)
22. `git diff --name-status main -- <rutas protegidas>` y `git diff --name-status main`
23. `git diff main -- docs/adr/0092-….md`; `grep -n -A2 "^## Estado"`
24. `grep -ciE "%|pnl|…"` en los seis ficheros del anexo (el intento con `$'\r'` lo negó la guardia); `grep -vc "^DIAGNOSTICO-DECISIONES | "`; `grep -cU -P "\r"`; `grep -oiE … | sort | uniq -c`
25. `tail -5 make-check.log` (y `ls -la`)
26. md5sum de la respuesta del consultor en el encargo (`:115-154`) y en el informe (`:430-469`)
27. `tail` de `f41`, `f42` y `f43-pantalla.txt`; `sha256sum` de `data/trazas-ablacion/cuenta-por-mes.txt` y de la línea base
28. `sha256sum` de tres ficheros del anexo frente a sus originales en `data/trazas-ablacion/`
29. `sed -n` de `parametros.yaml:501,515-518`, `HOJA-DE-RUTA.md:817`, `RECORRIDA-CONSTRUCCION-2.md:1355-1358` y `RITUAL.md:100-105`; Grep «breaker con cuerpo» en VIDEO-JULIO.md
30. `grep -n "^# Archivo 64"`; `git diff main -- docs/state/HISTORIA.md | grep -c "^-"`; `git show --stat 29561efd`
31. Grep «punto por punto» en `.claude/skills/entregar-rama/SKILL.md`

Ficheros clave:
- `C:\Users\USER\Desktop\Bot v3\docs\validation\TRAZAS-ABLACION.md`
- `C:\Users\USER\Desktop\Bot v3\src\botsito\engine\decisiones.py`
- `C:\Users\USER\Desktop\Bot v3\tests\unit\test_decisiones.py`
- `C:\Users\USER\Desktop\Bot v3\docs\validation\anexos\TRAZAS-ABLACION\`
- `C:\Users\USER\Desktop\Bot v3\knowledge\spec\ambiguedades.yaml` (A-20, `:422-436`)
- `C:\Users\USER\Desktop\Bot v3\PROJECT_STATE.md`

### Qué se hizo con cada hallazgo (2026-11-09)

| # | Gravedad | Qué se hizo |
|---|---|---|
| a1 | importa | Corregido en F4.3 y en la Technical Debt propuesta (5.6 c): un lote distinto solo se ve si mueve las no enviadas, los rechazos o las cuentas suspendidas; lo medido es el delta cero |
| a2 | importa | Corregido: A-20 RESUELTA (una zona de control; con dos se descarta) citada en 5.2, 5.5, la F propuesta y la PARADA; la pregunta 2 pasa a qué zonas cuenta el trader como de control |
| a3 | menor | Corregido: Δ órdenes incluye las rechazadas al colocar |
| b1 | bloquea | Commits de F4/F5 (4ac3810) y de las correcciones (9469bbf); CI, run 42740007047, con solo el fallo esperado; la frase final, en «Estado» |
| b2 | importa | Hecho: «El encargo, punto por punto», 35 requisitos con su estado |
| b3 | importa | Hecho: «Los guiones y comandos de la sesión», con el texto de cada guion en el anexo |
| b4 | importa | Corregido: la línea de guardia-g1 acortada (252 → 100 bytes, al final de HISTORIA en su bloque); y recontadas por (e), con el mismo guion, TODAS las líneas de más de 200 bytes (corrección de F1). Mi error: la elegí a mano entre las 22 y la di por de menos de 60 |
| b5 | importa | Declarado en 5.1 (límite de (a)) y en la clase «regla desconocida», que pasa a decir que es del mecanismo de ADR-0064 y no de estas cuatro; la recomendación 1 de la PARADA, reescrita |
| b6 | importa | Declarado en 5.1 (límite de (iii)) y en la clase «error nuestro» y la recomendación 2 |
| b7 | importa | Corregida la pregunta 1 (5.1 y 5.5): sin «qué vela tiene que cerrar», y con la voz de v12 y la de S-18 |
| b8 | importa | Declarado en «El encargo, punto por punto», 14; el test no se cambia en esta rama |
| b9 | menor | Corregidos los comandos de F4, con el `cd` y el `echo "exit=$?"` |
| b10 | menor | El Apéndice B existe (es este) |
| b11 | menor | A la PARADA final como decisión 7 |

## Estado

LISTA PARA REVISIÓN (2026-11-09): F1 a F5 hechos, sin ninguna PARADA condicional del punto 10; el
revisor pasó y sus hallazgos están corregidos o declarados (Apéndice B); CI de Linux, run 42740007047 sobre 9469bbf (empujado por Aleks a `fix/trazas-ablacion`): `make check` con 1 failed, 3310 passed, 48 skipped; el único fallo, el esperado de `RITUAL.md`: `test_state_check_ok_on_real_repo` («PROJECT_STATE declara la rama 'trabajo/trazas-ablacion'; la rama actual es 'fix/trazas-ablacion'»). Espera
la decisión del consultor sobre la PARADA final (decisiones 0 a 8) y la orden de cierre.

Rama lista para revisión, NO cerrada.
