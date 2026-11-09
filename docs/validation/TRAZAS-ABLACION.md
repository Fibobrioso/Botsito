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

## Estado

EN CURSO (2026-11-09): respuesta del consultor a la PARADA de la fase 0 recibida y copiada arriba;
F1 en curso; F2 a F5 sin esperar, con la PARADA condicional del punto 10.
