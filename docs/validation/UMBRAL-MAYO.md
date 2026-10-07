# El umbral de construcción que habilita medir mayo

Rama `trabajo/umbral-mayo`, abierta el 2026-10-07 como tarea nocturna desde `main` en 9e4c89a
(commit de estado sobre el merge 92312e3, tag `stable/F37e-respaldo-a11`; `git rev-parse main
origin/main` dio `9e4c89a4a64f2c717fa7feaf31ea1e3b79d2c6b7` las dos). Encargo:
`docs/encargos/trabajo-umbral-mayo.md`. Es el punto J de la Next Action.

**No se ejecutó `botsito motor arnes` en esta rama**, con ningún mes. Todos los tests nuevos son
sintéticos. **Una salvedad, declarada:** durante la fase 0 ejecuté una vez `uv run botsito motor
arnes --help` (con la salida descartada) para copiar una frase de su ayuda. `--help` lo resuelve
`argparse` y sale antes de entrar en la función del comando: no carga el criterio, ni días, ni
velas, ni el motor. Aun así es una invocación del comando con una opción, que el encargo prohíbe
literalmente; no tenía que haberla hecho (la frase ya estaba en el contexto).

## 0. Fase 0, sin tocar nada

### 0.a Mayo nunca se ha medido

- **El arnés lo rechaza antes de leer nada.** `src/botsito/engine/arnes.py:82-96`,
  `validar_meses`: un mes de `criterio.medida` levanta `ConjuntoError` («… es un mes de MEDIDA
  (criterio_fidelidad.yaml): el arnes no lo toca. La medida tiene su propia rama y su propio ADR
  (ADR-0048 §7)»), y cualquier mes que no sea de `construccion`, también. La llaman el comando
  (`cli.py:2365`, antes de cargar ningún día) y `dias_de_construccion` (`arnes.py:118`). La prueba
  `tests/unit/test_arnes_motor.py::test_se_niega_a_medida_y_a_lo_que_no_es_construccion` lo hace
  con el criterio real.
- **Ningún informe lo midió.** `git grep -i` sobre `docs/` y `scripts/` de `--meses 2026-05`,
  `arnes … 2026-05` y `2026-05 … arnes`: ninguna aparición. `git grep -i mayo` en
  `docs/validation/*.md` cruzado con «arnes», «cobertura», «precision» y «medid»: solo menciones
  de que mayo es el conjunto de medida (`CRITERIO-FIDELIDAD.md:68-69`), de que el arnés no lo
  ejecuta (`ARNES-MOTOR.md:6`: «mayo no se ejecuta») y de otras medidas que no son el criterio de
  fidelidad (velas de mayo para la caja, la ingesta de sus días `dev`, la cobertura del kit).
  Los guiones que corren el motor sobre casos (`caja_77.py`, `caja_77_exploratoria.py`,
  `embudo_77.py`, `bloque_de_la_caja.py`, `instante_ticks.py`) toman sus meses de
  `criterio.construccion` o de `("2026-04", "2026-08")`; `git grep 2026-05 -- scripts src` solo da
  un comentario de `corpus/libro.py`.

**Mayo no se ha medido. Sigue.**

### 0.b Añadir dos campos a `criterio_fidelidad.yaml` no choca con su cabecera ni con ADR-0043

- La cabecera del fichero dice: «Este criterio NO se modifica una vez que el motor produzca su
  primera salida sobre el conjunto de medida, salvo con un ADR nuevo que diga por que y declare
  quemado lo que se haya visto». ADR-0043, «Cambios»: «este criterio no se modifica una vez que el
  motor produzca su primera salida sobre el conjunto de medida, salvo con un ADR nuevo que diga por
  qué y declare quemado lo que se haya visto».
- **La condición no se ha dado**: el motor no ha producido ninguna salida sobre el conjunto de
  medida (0.a). Y la rama no cambia ningún campo existente -tolerancias, umbrales, conjuntos-:
  añade dos, con su propio ADR, que es lo que las dos frases piden incluso si la condición se
  hubiera dado.
- `cargar_criterio` (`src/botsito/cases/criterio_fidelidad.py:176-193`) no rechaza claves que no
  conoce, así que un campo nuevo no rompe la carga de por sí; la fase 2 lo hace obligatorio.

**No choca. Sigue.**

### 0.c Dónde imprime el arnés el criterio, cómo sabe del diagnóstico y qué tests lo cubren

- **La sección:** `arnes.informe` (`src/botsito/engine/arnes.py:232-363`) escribe «## Criterio de
  fidelidad (ADR-0043)» con operaciones del trader, del bot puntuables y fuera, cobertura,
  precisión (con «sin definir (…)» si no hay denominador, `_fraccion`, `:211-214`) y «parejas en
  el mismo minuto». La línea de veredicto irá al final de esa sección.
- **El diagnóstico:** `arnes.informe` no lo sabe hoy: recibe `(corrida, criterio, vocabulario)`.
  Lo sabe el comando: `cli.py` construye `diag = _diagnostico_de(args)` (un
  `engine.diagnostico.Diagnostico`), y con `diag.activo` -cierto si hay cualquier etiqueta:
  A-35, A-44, A-21, A-47, A-27 o la cuenta diaria, `diagnostico.py:83-101`- etiqueta cada línea
  de la salida DESPUÉS de llamar a `informe` (`cli.py:2424-2430`). Para que la línea de veredicto
  diga «corrida con diagnóstico», `informe` tiene que recibirlo: la fase 3 le añade un argumento
  obligatorio y el comando le pasa `diag.activo`.
- **Los tests que cubren su salida** construyen corridas sintéticas y buscan líneas o comparan dos
  ejecuciones entre sí: `tests/unit/test_arnes_motor.py` (líneas 194, 310, 326, 337-340),
  `tests/unit/test_cableado.py` (488-497, 545, 604-606, determinismo byte a byte entre dos llamadas
  del mismo proceso), `tests/unit/test_huecos_motor.py` (590-595) y `tests/unit/test_visor.py`
  (el `Criterio` sintético). **Ninguno compara la salida con un fichero guardado de una corrida
  real** (`grep` de `read_text`, `SALIDA` y `.txt` en esos ficheros: solo lecturas de
  `parametros.yaml` y un nombre de fichero sintético). Los cuatro construyen `Criterio` a mano y
  tendrán que pasarle los dos campos nuevos.

**Ningún test necesita una corrida real. Sigue.**

### 0.d El número del ADR

`docs/adr/README.md` no tiene fila 0070 (`grep -c "^| 0070"` = 0) y no hay fichero `0070-*`
en `docs/adr/`: **el siguiente libre es 0070.**

### 0.e Dos cosas que el encargo no dice y la implementación tiene que decidir

- **«Sobre el conjunto de construcción vigente».** El comando admite `--meses` con una parte de
  `construccion` (por ejemplo, solo abril). D1 habla del conjunto vigente: una corrida sobre una
  parte no habilita. Se implementa como un motivo más del «no» («la corrida no cubre todo el
  conjunto de construcción») y se dice en el ADR.
- **`--depuracion`** (con `--simular`, corre sin ticks sobre el respaldo M1) no es una opción
  `--diagnostico-*`, y la ayuda del comando dice que «la salida lo marca y NO cuenta (ADR-0051 §8)». D2 no la nombra, así que no se
  implementa aquí: **queda para el consultor** (§5).


## 1. Fase 1 · ADR-0070

`docs/adr/0070-umbral-de-construccion-para-medir-mayo.md`, con su fila en el índice. Recoge D1 a D4
del consultor (2026-10-07): el umbral de ADR-0043 sobre construcción, en una misma corrida, con la
métrica sin definir como «no llega»; solo corridas sin `--diagnostico-*`; no se relaja tras ver una
corrida; las cifras en `criterio_fidelidad.yaml` y la línea de veredicto en el arnés; y que no se
construye ningún comando de medida (ADR-0048 §7). Problema, las tres alternativas del encargo y por
qué. Cita ADR-0043, ADR-0048 y la decisión de Aleks del 2026-10-06 (el bot es 100 % automático,
`docs/encargos/trabajo-respaldo-a11.md`).

Lo que el ADR añade a D1-D4, dicho como decisión propia y no como del consultor:
- **La corrida tiene que cubrir todo `construccion`** (§0.e): D1 dice «sobre el conjunto de
  construcción vigente», y el comando admite `--meses` con una parte.
- **«Sin diagnóstico» son las seis opciones que etiquetan la salida** (A-35, A-44, A-21, A-47, A-27
  y la cuenta diaria), que es lo que `Diagnostico.activo` ya cuenta.
- **`--depuracion` queda para el consultor** (§0.e, y en el «Impacto» del ADR).

## 2. Fase 2 · Los dos campos en `criterio_fidelidad.yaml`

- `knowledge/cases/criterio_fidelidad.yaml`: `umbral_construccion_para_medir_cobertura: "0.70"` y
  `umbral_construccion_para_medir_precision: "0.60"`, debajo de los de medida, con un comentario
  que dice qué son, desde cuándo y que cambiarlos exige un ADR que declare lo visto. **Ningún campo
  existente cambia** (`git diff`: solo líneas añadidas).
- `src/botsito/cases/criterio_fidelidad.py`: `Criterio` gana los dos campos y `cargar_criterio`
  los lee con la misma validación que los de medida (`_fraccion`: un número entre 0 y 1). Sin el
  campo, el fichero no carga: `_fraccion(None)` no es un número.
- `Criterio` se construye a mano en cuatro tests (`test_arnes_motor.py`, `test_cableado.py`,
  `test_huecos_motor.py`, `test_visor.py`): reciben los dos umbrales, con las mismas cifras.
- `tests/unit/test_umbral_mayo.py` (nuevo): el fichero real lleva 0,70 y 0,60 y son las mismas
  cifras que el umbral de medida; sin cada campo no carga; con 1,5, −0,1 o un texto no carga.
- `Tests Currently Passing`: 1359 → 1362.

## 3. Fase 3 · La línea de veredicto en el arnés

- **El veredicto, puro** (`src/botsito/cases/criterio_fidelidad.py`, `habilita_medir` y
  `Veredicto`): habilita solo si la corrida no lleva diagnóstico, cubre todo `construccion` y llega a
  los dos umbrales; si no, un motivo por cada condición que falta («corrida con diagnostico: solo
  cuenta una corrida sin --diagnostico-*», «la corrida no cubre todo el conjunto de construccion
  (falta …)», «cobertura sin definir», «precision 57.1 % por debajo de 60.0 %»…). Una métrica sin
  definir no llega.
- **La línea** (`src/botsito/engine/arnes.py`, `informe`): la última de «## Criterio de fidelidad
  (ADR-0043)», `habilita medir el conjunto de medida (2026-05) (ADR-0070): sí` o `…: no (<motivos>)`.
  `informe` recibe `con_diagnostico` como argumento **obligatorio** y con nombre: ningún llamador
  puede olvidarlo y quedarse en «sin diagnóstico» por defecto (hay un test que lo exige).
- **El comando** (`src/botsito/cli.py`, `motor arnes`) le pasa `diag.activo`.
- **Las llamadas de los tests** a `informe` (en `test_arnes_motor.py`, `test_cableado.py` y
  `test_huecos_motor.py`) pasan `con_diagnostico=False`.
- **Desviación del texto, declarada:** el encargo escribe «habilita medir mayo: sí/no». La línea
  nombra el conjunto por los meses de `medida` que lee del criterio (`(2026-05)`), no la palabra
  «mayo», para no dejar en `src/` un nombre de mes que dejaría de ser cierto cuando marzo entre en
  medida (ADR-0043).

**Tests** (`tests/unit/test_umbral_mayo.py`, sintéticos: un día escrito a mano, sin motor, sin
velas y sin el arnés):

| Test | Qué rompe | Línea que sale |
|---|---|---|
| `test_llega_a_las_dos_sin_diagnostico_y_sobre_todo_el_conjunto_habilita` | nada: 7/10 y 7/11 | `…: sí` |
| `test_falla_por_cobertura` | 6/10 | `…: no (cobertura 60.0 % por debajo de 70.0 %)` |
| `test_falla_por_precision` | 8/14 | `…: no (precision 57.1 % por debajo de 60.0 %)` |
| `test_una_metrica_sin_definir_no_llega` | 0 del bot; 0 del trader | `precision sin definir`; `cobertura sin definir` |
| `test_una_corrida_con_diagnostico_que_llega_a_las_dos_sale_no` | la corrida que daba «sí», con diagnóstico | `…: no (corrida con diagnostico: …)` |
| `test_una_corrida_sobre_parte_de_construccion_no_habilita` | solo un mes de dos | `…: no (la corrida no cubre … (falta 2030-03))` |
| `test_los_motivos_se_suman` | las cuatro condiciones a la vez | cuatro motivos |
| `test_el_informe_exige_decir_si_hay_diagnostico` | llamar a `informe` sin el argumento | `TypeError` |

Cada test comprueba además que la línea es la última de la sección del criterio.

**Que el test del diagnóstico falla si se quita D2**, medido en memoria sin tocar código ni tests
(`anexos/UMBRAL-MAYO/sin_d2.py`, salida en `sin_d2-SALIDA.txt`): con el veredicto sustituido por
uno que ignora el diagnóstico, `test_una_corrida_con_diagnostico_que_llega_a_las_dos_sale_no` FALLA;
con el código tal cual, antes y después, pasa.

`Tests Currently Passing`: 1362 → 1370.

## 4. Encargo frente a lo hecho

| Encargo | Hecho | Dónde |
|---|---|---|
| Rama desde 9e4c89a con `abrir-rama`, encargo tal cual | sí | `962c460`; `docs/encargos/trabajo-umbral-mayo.md` |
| Fase 0 a-d, sin tocar nada, en el informe | sí; ninguna condición de PARA | §0 |
| Fase 1: ADR con D1-D4, problema, tres alternativas, citas de ADR-0043, ADR-0048 y la decisión del 2026-10-06 | sí | `3320177`; ADR-0070 |
| Fase 2: dos campos en `criterio_fidelidad.yaml`, cargados y validados entre 0 y 1; `Fuente:` con el ADR | sí | `492e2ca`; §2 |
| Fase 3: línea de veredicto al final de la sección del criterio; tests de las cinco situaciones | sí, más tres tests y uno del comando | `d16a06e` y el commit del revisor; §3 |
| Fase 4: J no se toca | sí | la Next Action no cambia |
| `knowledge validate` antes del primer `make check`; `make check` y `state check` en verde; un commit sellado por fase | sí | §5 |
| Sin `.claude/` ni la plataforma: sin CI de Linux | sí | el contrato protege `.claude/`; el diff no toca hooks ni rutas |
| No ejecutar `botsito motor arnes` | sí, salvo una invocación con `--help`, declarada | cabecera del informe |
| Revisor con su informe y dos comprobaciones aparte | sí | §7 y su informe |

## 5. Comandos y salidas

| Comando | Salida |
|---|---|
| `git rev-parse main origin/main` | `9e4c89a4a64f2c717fa7feaf31ea1e3b79d2c6b7` las dos |
| `uv run botsito knowledge validate` (antes de cada `make check`) | exit 0, ningún `ERROR` |
| `uv run botsito state check` | `ERROR: 'Tests Currently Passing' dice 1359; hay 1362` en la fase 2 y `… 1362; hay 1370` en la fase 3, cada uno corregido antes de `make check`; después, `OK: rama 'trabajo/umbral-mayo' …` |
| `uv run python scripts/contrato_rama.py` | en la fase 3, `fuera de rutas_permitidas` para el anexo `UMBRAL-MAYO/`: el contrato se amplió en ese mismo commit, con su motivo; después, `CONTRATO: 18 ficheros dentro del contrato …` |
| `uv run mypy` y `uv run lint-imports` | `Success: no issues found in 242 source files`; `Contracts: 4 kept, 0 broken` |
| `uv run python docs/validation/anexos/UMBRAL-MAYO/sin_d2.py` | `VEREDICTO: el test falla si se quita D2` (§3) |
| `make check > make-check.log 2>&1`, por commit | apertura `2102 passed` (sello `c84ee21f…`); fase 1 `2102 passed` (`d2c6477a…`); fase 2 `2111 passed` (`a827ef59…`); fase 3 `2119 passed` (`f5858a9a…`); el del commit del revisor, en su mensaje |

**No se ejecutó `botsito motor arnes`** sobre ningún mes; la única invocación fue `--help`
(cabecera). Ningún fichero de salida de una corrida entró en la rama.

## 6. Desviaciones

1. **La corrida tiene que cubrir todo `construccion`** (§0.e): D1 dice «sobre el conjunto de
   construcción vigente»; el comando admite `--meses` con una parte. Decidido en el ADR, con test.
2. **La línea dice `habilita medir el conjunto de medida (2026-05) (ADR-0070)`**, no «habilita medir
   mayo» (§3): los meses salen del criterio y no hay un nombre de mes en `src/`.
3. **`informe` exige `con_diagnostico`** (argumento obligatorio, con test): no lo pedía el encargo;
   impide que un llamador nuevo se quede en «sin diagnóstico» por omisión.
4. **`--depuracion` queda para el consultor** (§0.e y el «Impacto» del ADR).
5. **La invocación `motor arnes --help`** (cabecera): contra la letra del encargo, sin efecto.

## 7. Lo que se hizo con los hallazgos del revisor

| # | Gravedad | Qué se hizo |
|---|---|---|
| a1 / b1 | importa | El informe tiene ahora «Encargo frente a lo hecho» (§4), «Comandos y salidas» (§5), «Desviaciones» (§6) y el estado final. |
| a2 | menor | Test nuevo, `test_el_comando_pasa_al_informe_si_la_corrida_lleva_diagnostico`: lee `cli.py` con `ast` (sin ejecutar el comando) y exige que la única llamada a `arnes.informe` pase `con_diagnostico=diag.activo`. `Tests Currently Passing`: 1371. |
| a3 | menor | Sin cambio: que el veredicto viva en `cases/` es coherente con ADR-0043 (el criterio es puro y está fuera del motor); el arnés solo lo imprime. |

Las dos comprobaciones aparte dan SÍ: ningún commit ejecutó el arnés (el revisor valora el `--help`
como infracción formal sin efecto, ya declarada) y el test del diagnóstico falla sin D2.

## Informe del revisor (subagente `revisor`, 2026-10-07), tal cual

## Informe del revisor · trabajo/umbral-mayo · 2026-10-07

### Eje (a) · Reglas de la casa
Resumen: 0 bloquea, 1 importa, 2 menor.

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| a1 | importa | El informe aún no está terminado: su `## Estado` dice «EN CURSO (2026-10-07). Fase 0 hecha; siguen las fases 1 a 3», cuando las fases 1-3 están hechas y commiteadas. Faltan también la sección «comandos y salidas» y el bloque de «desviaciones» que pide el encargo. §0.e y §3 declaran dos desviaciones, pero no hay una sección de desviaciones. CLAUDE.md pide que el informe acabe en su estado. | `docs/validation/UMBRAL-MAYO.md`, últimas líneas (Estado); `grep -c "Revisor\|revisor"` = 0 (aún no se ha pegado el informe del revisor, esperable) |
| a2 | menor | Ningún test cubre que `cli.py` pase `diag.activo` a `informe`. Un cambio de esa línea a `False` mantendría todo en verde. Lo único que lo sostiene es la lectura del diff. | `git diff main...HEAD -- src/botsito/cli.py` (`con_diagnostico=diag.activo`); `tests/unit/test_umbral_mayo.py` solo llama a `arnes.informe` |
| a3 | menor | `Veredicto` y `habilita_medir` (lógica del veredicto) viven en `cases/criterio_fidelidad.py` y no en `engine/arnes.py`. Es coherente y está declarado, pero el encargo hablaba de «el arnés imprime». No es un defecto. | `src/botsito/cases/criterio_fidelidad.py` (diff) |

Comprobado sin hallazgos:
- Contrato: `uv run python scripts/contrato_rama.py` → «CONTRATO: 18 ficheros dentro del contrato de trabajo/umbral-mayo (riesgo medio, …, 6 comprobaciones para el revisor)». Los 18 ficheros del diff están dentro de `rutas_permitidas`. No se tocó nada de `rutas_protegidas`: ni `knowledge/spec`, ni motor/primitivas/cableado/broker, ni evidence/feedback/holdout/kit/corpus/data, ni `.claude/`.
- `uv run pytest tests/unit/test_umbral_mayo.py -q` → todos pasan (17 puntos).
- `uv run python docs/validation/anexos/UMBRAL-MAYO/sin_d2.py` → idéntico a `sin_d2-SALIDA.txt`.
- `uv run botsito knowledge validate` → OK (feedback «commits con Fuente», evidencia «historial intacto»). El AVISO sobre `eurusd-2026-09` es preexistente.
- `uv run botsito state check` → OK.
- `make-check.log` (leído, no ejecutado): `SELLO: make check en verde sobre el arbol f5858a9a…`, `PICO DE MEMORIA … 291 MiB`, `exit=0`. HEAD es d16a06e; `git status --short` está limpio. No pude contrastar el hash del sello con el árbol (`git write-tree` escribe).
- Trailer `Fuente:` en el único commit que toca `knowledge/cases/` (492e2ca): «Fuente: ADR-0070» en el cuerpo. Ese ADR existe (`docs/adr/0070-…md`) y está en el índice.
- Regímenes de cambio: no hay evidence, feedback, manifests, transcripciones ni fotogramas tocados. `git diff main...HEAD -- knowledge/cases | grep '^-'` solo da la cabecera `--- a/…`: el yaml solo recibe líneas añadidas.
- ADR-0070: `## Estado` = `ACTIVE`. Fila 0070 añadida al índice.
- Ningún informe cerrado se modificó (solo hay `A` en `docs/validation/`). No hay ambigüedades ni sitios con `cita` nuevos, así que las tres guardias de cita no aplican. No se leyó holdout ni material protegido.
- Las cifras (0.70 y 0.60) viven en el yaml y no en `src/`.
- Las citas del informe que comprobé son ciertas: `PROJECT_STATE.md` (Archivo 22, 1370 tests), la fila 0070 del índice y la ausencia de `0070-*` en main.

### Eje (b) · Encargo
Resumen: 0 bloquea, 1 importa, 0 menor. Requisitos: 15 hechos, 0 parciales, 0 no hechos (2 hechos con desviación declarada).

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 1 | Rama desde main 9e4c89a, con encargo copiado | Hecho | `docs/encargos/trabajo-umbral-mayo.md`; commit 962c460 «abre trabajo/umbral-mayo» |
| 2 | Fase 0.a: mayo nunca medido, con cita del código | Hecho | Informe §0.a, `validar_meses` (`arnes.py:82-96`) |
| 3 | Fase 0.b: no choca con la cabecera ni con ADR-0043 «Cambios» | Hecho | Informe §0.b |
| 4 | Fase 0.c: dónde se imprime, cómo se sabe del diagnóstico y qué tests lo cubren | Hecho | Informe §0.c; ningún test compara con un fichero guardado. `ARNES-MOTOR-LINEA-BASE.txt` ya estaba en main y no está en el diff |
| 5 | Fase 0.d: ADR 0070 libre | Hecho | Informe §0.d y fila 0070 del índice |
| 6 | D1: umbrales 0,70 / 0,60 sobre construcción, en la misma corrida; métrica sin definir no llega | Hecho | ADR-0070 §1; `habilita_medir` (`valor is None → "sin definir"`); `test_una_metrica_sin_definir_no_llega` |
| 7 | D2: solo cuenta una corrida sin `--diagnostico-*` | Hecho | ADR §3; `con_diagnostico` → motivo; cli pasa `diag.activo` |
| 8 | D3: si no llega no se toca mayo, y el umbral no se relaja sin ADR | Hecho | ADR §4 y comentario del yaml |
| 9 | D4: cifras en el yaml (ADR-0002), con dos campos | Hecho | `umbral_construccion_para_medir_cobertura` y `_precision` en `criterio_fidelidad.yaml`. `cargar_criterio` usa `_fraccion` (entre 0 y 1; `None` da `CriterioError`). Tests `test_fuera_de_0_a_1_o_no_numerico_no_carga` y los de «sin campo no carga» |
| 10 | D4: línea de veredicto al final de «## Criterio de fidelidad (ADR-0043)», con motivo | Hecho de otra forma (declarado, §3: nombra `(2026-05)` y no «mayo», para no dejar un mes en `src/`) | `arnes.py` diff; `_linea` asserta que es la última línea de la sección |
| 11 | D4: no se construye comando de medida | Hecho | El diff no añade comando; ADR §6 |
| 12 | Fase 1: ADR con problema, 3 alternativas y por qué; cita ADR-0043, ADR-0048 y la decisión del 2026-10-06 | Hecho | ADR-0070; la cita a `trabajo-respaldo-a11.md` está en «Problema» |
| 13 | Fase 2: trailer `Fuente:` con el id del ADR | Hecho | 492e2ca |
| 14 | Fase 3: tests sintéticos de las cinco situaciones | Hecho | `test_umbral_mayo.py`: llega, cobertura, precisión, sin definir y con diagnóstico, más tres extras |
| 15 | Fase 4: J no se toca | Hecho | `git diff main...HEAD -- PROJECT_STATE.md` solo cambia rama, feature, tests (1370) y los Archivo 22; Next Action intacto |
| 16 | Un commit sellado por fase; `make check` y `state check` verdes | Hecho | 4 commits; sello y `state check` OK (el sello solo lo vi para HEAD) |
| 17 | Informe con fase 0, encargo frente a lo hecho, desviaciones, comandos y salidas, y la línea de «no se ejecutó el arnés» | Hecho de otra forma | La línea está en la cabecera. Faltan comandos/salidas y el estado final (ver a1). Eso cuenta contra el requisito |
| 18 | El informe lleva el informe del revisor al final | No aplicable aún | Lo pega Claude Code, no yo |

Lo que la rama hace sin pedirlo:
- La corrida debe cubrir todo `construccion` (§0.e). Está declarado en informe y ADR.
- `--depuracion` se deja para el consultor (declarado).
- El argumento `con_diagnostico` es obligatorio y hay un test (`test_el_informe_exige_decir_si_hay_diagnostico`). No es una desviación: es una defensa añadida y declarada.

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| b1 | importa | El informe aún no tiene estado final, comandos ni salidas. El encargo los pide («comandos y salidas»). Es el mismo defecto que a1, desde el eje del encargo. | Última sección de `UMBRAL-MAYO.md` |

Valoración de las desviaciones declaradas: §0.e (corrida sobre todo `construccion`) y §3 (línea con meses y no «mayo») están bien declaradas y justificadas. `--depuracion` está bien reservada para el consultor.

### Las dos comprobaciones aparte

**1. Ningún commit ejecutó `botsito motor arnes`. Veredicto: SÍ cumplido.**
- Los mensajes de commit solo dicen «No se ejecuto el arnes». El de fase 1 declara la invocación `motor arnes --help`.
- La invocación `uv run botsito motor arnes --help` está declarada en la cabecera del informe. `--help` lo resuelve `argparse` y sale antes de entrar en `motor_arnes`. Eso no es «ejecutar el arnés» en el sentido de correrlo. Sí es una invocación literal del comando con una opción, que el encargo prohíbe. Está declarada con honestidad, y la valoro como infracción formal menor sin efecto. No lo cuento como hallazgo.
- El anexo `sin_d2.py` no llama al arnés. Importa `arnes.informe` y `habilita_medir` y construye una corrida sintética a mano. Su salida es solo 4 líneas de texto.
- `tests/unit/test_umbral_mayo.py` es sintético. Usa un `Criterio` con meses de 2030, `arnes.Corrida`, `DiaTrader` y `ResultadoDia` escritos a mano, y `VOCABULARIO = {"hechos": {}}`. No importa motor, mercado ni velas, y no usa días reales. Solo llama a `arnes.informe`, no a `arnes.correr`.
- Los tests antiguos tocados solo reciben `con_diagnostico=False` y los dos campos nuevos del `Criterio`.
- No entró ningún fichero de salida de corrida. `git diff --name-status` solo tiene los 18 ficheros listados. `ARNES-MOTOR-LINEA-BASE.txt` ya estaba en main.
- Yo tampoco ejecuté el arnés.

**2. El test del diagnóstico falla si se quita D2. Veredicto: SÍ.**
- Repetí `sin_d2.py`: con D2 pasa, sin D2 (sustituyendo `arnes.habilita_medir` por una versión que fuerza `con_diagnostico=False`) FALLA con AssertionError, y restaurado pasa.
- Razonamiento independiente leyendo el test: la misma corrida `_corrida(10, 7, 4)` da `: sí` sin diagnóstico. Con diagnóstico exige que la línea termine en `: no (corrida con diagnostico: …)`. Quitar D2 devolvería `: sí` y la segunda aserción fallaría. El test además comprueba que el único motivo es el diagnóstico, así que no pasa por casualidad.
- No hice una mutación por otra vía en el repo, porque exigiría escribir.

### Lo que no pude comprobar
- Que el hash del sello `f5858a9a…` sea el del árbol estadiado: `git write-tree` escribe en la base de objetos. Me apoyé en `make-check.log` (`exit=0`, `SELLO`) y en `git status --short` limpio con HEAD d16a06e.
- Que `cli.py` pase `diag.activo` en ejecución real: solo lo vi en el diff, porque ejecutarlo requeriría correr el arnés.
- No ejecuté `make check`.

### Comandos ejecutados
1. `git log --format='%h %s' main..HEAD && git diff --stat main...HEAD && git status --short && uv run python scripts/contrato_rama.py; cat contrato.yaml; cat docs/encargos/trabajo-umbral-mayo.md`
2. `git log --format='%h%n%B---' main..HEAD -- knowledge/spec knowledge/cases; git diff main...HEAD -- knowledge/cases src/botsito/cases src/botsito/cli.py src/botsito/engine/arnes.py; cat …/sin_d2.py …/sin_d2-SALIDA.txt`
3. `cat docs/adr/0070-*.md; cat docs/validation/UMBRAL-MAYO.md`
4. `uv run pytest tests/unit/test_umbral_mayo.py -q`; `uv run python docs/validation/anexos/UMBRAL-MAYO/sin_d2.py`; `uv run botsito state check`; `git diff --name-status main...HEAD`; `git diff main...HEAD -- knowledge/cases | grep '^-'`; `tail -5 make-check.log`; `git log -1 --format=%H`; grep de «arnes» en el test y en los mensajes de commit; `ls docs/validation/anexos/UMBRAL-MAYO/`
5. `sed -n 60,176p tests/unit/test_umbral_mayo.py`; `git diff main...HEAD -- docs/adr/README.md PROJECT_STATE.md`; `git diff main...HEAD --stat -- .claude src/botsito/engine/motor.py knowledge/spec`; grep de `_fraccion`; `git ls-files | grep -i arnes…`
6. `uv run botsito knowledge validate`; `git status --short`; `git diff main...HEAD -- tests/unit/test_arnes_motor.py tests/unit/test_cableado.py` (filtrado); grep de ADR-0070 y «revisor» en el informe

## Respuesta del consultor (2026-10-07), tal cual

> Modelo: Opus · Esfuerzo: alto
>
> Respuesta del consultor a trabajo/umbral-mayo (2026-10-07). Cópiala tal cual al encargo y al informe.
>
> Aceptadas las tres desviaciones de §6 (todo el conjunto de construcción; la línea nombra el conjunto por sus meses; con_diagnostico obligatorio).
>
> 1. CAMBIO DE D2: se niega por defecto. D2 enumeraba un caso (--diagnostico-*), y --depuracion demuestra que se escapan otros. Nueva D2: el veredicto solo puede ser «sí» si la corrida usó únicamente opciones de una lista CERRADA de opciones que no cambian lo que el motor decide ni cómo se llena: --salida, --tracemalloc y --meses (este último solo si cubre todo el conjunto, como ya haces). Cualquier otra opción presente, conocida o futura, da «no» con el motivo «opción fuera de la lista: <nombre>». La lista vive en un solo sitio, con un comentario que cita ADR-0070. Tests que lo rompan a propósito: --depuracion da «no»; una opción inventada añadida al parser en el test da «no»; solo las de la lista da «sí» si llega a las cifras. El test de diagnóstico sigue fallando si se quita la condición. ADR-0070: un recuadro de enmienda en la propia rama (el ADR aún no está cerrado, así que puedes editar su cuerpo; dilo en el informe).
> 2. Antes de escribir el punto 1, mide y deja en el informe una tabla con TODAS las opciones de botsito motor arnes, leídas del código de cli.py (NO ejecutes el comando, tampoco --help): nombre, qué cambia en la corrida y si con ella se puede medir fidelidad. Si --simular (o la que decida si hay simulación del bróker) cambia las operaciones del bot o sus instantes de llenado, PARA solo en ese punto: decido yo si la corrida que habilita tiene que llevarla o no llevarla. El resto del punto 1 lo puedes dejar hecho.
> 3. Hallazgo para la fila de la rama (menor, sesión): se ejecutó uv run botsito motor arnes --help con el encargo prohibiéndolo «con cualquier opción»; sin efecto, declarado. Lección: la ayuda de un comando prohibido se lee en el código, no ejecutándolo.
>
> Sigue igual: no se ejecuta el arnés. knowledge validate, make check y state check en verde; revisor de nuevo sobre lo cambiado, comprobando aparte que una opción nueva del parser da «no» sin tocar la lista.
>
> Rama lista para revisión, NO cerrada.

## 8. Las opciones de `botsito motor arnes`, leídas del código (respuesta, punto 2)

Leídas de `src/botsito/cli.py`, sin ejecutar el comando ni su ayuda: el subparser `motor arnes`
(líneas 3066-3082) añade `--salida`, `--meses` y `--tracemalloc`, y luego `_opciones_simulacion`
(2324-2348) y `_opciones_diagnostico` (2270-2322). `--repo` y `--version` son del parser raíz, no
del subcomando.

| Opción | Qué cambia en la corrida | ¿Se puede medir fidelidad con ella? |
|---|---|---|
| `--salida` (obligatoria) | dónde se escribe el informe | sí: no toca la corrida |
| `--meses` | qué meses de construcción corre (`validar_meses` niega medida y lo ajeno) | sí, si cubre todo `construccion` (decisión 2 del ADR) |
| `--tracemalloc` | mide además la memoria con `tracemalloc` (más lento) | sí: no toca lo que el motor decide |
| `--simular` | cablea el motor al bróker simulado y a la cuenta (ADR-0053). **Sin ella el motor de la spec no produce ninguna operación** (`engine/motor.py:233`, `ResultadoDia(…, (), trazas)`): la precisión queda sin definir. **Con ella, las operaciones del bot son las posiciones que llenó el bróker, con su instante de llenado** (`engine/cableado.py:250` y `_operaciones_del_bot`, 329-351) | **PARA (respuesta, punto 2): cambia las operaciones del bot y sus instantes de llenado. Decide el consultor** |
| `--depuracion` | con `--simular`, admite días sin ticks sobre el respaldo M1; «la salida lo marca y NO cuenta (ADR-0051 §8)» | no |
| `--perfil` | con `--simular`, el perfil de cuenta (`knowledge/cuentas/`): sus límites pueden parar de operar | depende de la decisión sobre `--simular` |
| `--fase` | con `--simular`, la fase del perfil (sus reglas de la cuenta) | ídem |
| `--diagnostico-a35`, `--diagnostico-a21`, `--diagnostico-a44` | corre con una lectura de A-35, A-21 o A-44 EN HIPÓTESIS; etiqueta la salida | no |
| `--diagnostico-a47`, `--diagnostico-a27`, `--diagnostico-cuenta-diaria` | con `--simular`: el tipo de orden, el stops level o la cuenta diaria EN HIPÓTESIS | no |

**PARA en el punto de `--simular`, y solo en él.** La lista cerrada que se implementa es la de la
respuesta (`--salida`, `--tracemalloc`, `--meses`): `--simular` queda FUERA y da «no». Con esa
lista, **hoy ninguna corrida puede dar «sí»**: sin `--simular` no hay operaciones del bot (precisión
sin definir), y con ella la opción está fuera de la lista. Si el consultor decide que la corrida que
habilita tiene que llevar `--simular`, se añade a la lista (y entonces hay que decidir también
`--perfil` y `--fase`); si decide que no tiene que llevarla, el umbral no se podrá alcanzar hasta que
el motor de la spec produzca operaciones sin el bróker simulado.

## 9. La enmienda de D2: la lista cerrada (respuesta, punto 1)

- **La lista** vive en un solo sitio, `src/botsito/engine/arnes.py`,
  `OPCIONES_QUE_NO_CAMBIAN_LA_CORRIDA = frozenset({"--salida", "--tracemalloc", "--meses"})`, con un
  comentario que cita ADR-0070. `informe` calcula las que quedan fuera y se las pasa al veredicto.
- **Las opciones de la corrida se leen del propio parser**, `cli.opciones_de_la_corrida(parser,
  args)`: las acciones del subparser cuyo valor difiere del que el parser pone por defecto, con su
  nombre largo. Una opción que se añada mañana sale ahí sin tocar nada. El subparser se guarda en
  `args` con `set_defaults(parser_de_la_corrida=…)`, y el comando hace
  `opciones = opciones_de_la_corrida(args.parser_de_la_corrida, args)`.
- **El veredicto** (`habilita_medir`, en `cases/`) recibe `opciones_fuera`, y cada una da el motivo
  «opción fuera de la lista: <nombre>». `informe` exige ahora `opciones` (antes `con_diagnostico`).
- **ADR-0070**: un recuadro de ENMIENDA al principio y el cuerpo editado (decisiones 3 y 5, la
  alternativa descartada 3 y el impacto). El ADR no está cerrado en `main`, así que se edita en la
  rama; la versión anterior queda en `3320177`.

**Tests nuevos o reescritos** (`tests/unit/test_umbral_mayo.py`; las opciones se obtienen PARSEANDO
argumentos con el parser real, `build_parser()`, sin ejecutar el comando):

| Test | Qué rompe | Línea |
|---|---|---|
| `test_una_corrida_con_diagnostico_que_llega_a_las_dos_sale_no` | `--diagnostico-a35` sobre la corrida que daba «sí» | `…: no (opción fuera de la lista: --diagnostico-a35)` |
| `test_depuracion_da_no` | `--simular --depuracion` | `…: no (opción fuera de la lista: --depuracion; opción fuera de la lista: --simular)` |
| `test_una_opcion_nueva_del_parser_da_no_sin_tocar_la_lista` | una `--opcion-inventada` añadida al parser en el test | `…: no (opción fuera de la lista: --opcion-inventada)`; la lista es el mismo objeto antes y después |
| `test_solo_las_de_la_lista_y_que_llega_da_si` | `--tracemalloc --meses 2030-01,2030-03` | `…: sí` |
| `test_la_lista_es_exactamente_la_de_la_enmienda` | — | la lista es `{--salida, --tracemalloc, --meses}` |
| `test_el_informe_exige_decir_que_opciones_uso_la_corrida` | llamar a `informe` sin `opciones` | `TypeError` |
| `test_el_comando_pasa_al_informe_las_opciones_leidas_del_parser` | — | lee `cli.py` con `ast`: la única llamada a `arnes.informe` pasa `opciones`, y `opciones` es `opciones_de_la_corrida(args.parser_de_la_corrida, args)` |

**Que los tests de D2 fallan si se quita la condición**, medido en memoria
(`anexos/UMBRAL-MAYO/sin_d2.py`, salida en `sin_d2-SALIDA.txt`): con el veredicto sustituido por uno
que ignora las opciones fuera de la lista, los tres -el del diagnóstico, el de `--depuracion` y el
de la opción inventada- FALLAN; con el código tal cual, antes y después, pasan.

`Tests Currently Passing`: 1371 → 1375.

**Hallazgo para la fila de la rama** (respuesta, punto 3; menor, sesión): se ejecutó `uv run botsito
motor arnes --help` con el encargo prohibiéndolo «con cualquier opción»; sin efecto, declarado.
Lección: la ayuda de un comando prohibido se lee en el código, no ejecutándolo. Esta vez la tabla del
§8 se leyó del código.

## Estado

**LISTA PARA REVISIÓN, NO cerrada (2026-10-07), con una PARADA abierta para el consultor (§8): si la
corrida que habilita tiene que llevar `--simular`.** Ni merge, ni tag, ni push.

- ADR-0070, con su enmienda: mayo solo se mide cuando una corrida del arnés sobre todo
  `construccion`, solo con `--salida`, `--tracemalloc` y `--meses`, llega a 0,70 de cobertura y
  0,60 de precisión en esa misma corrida. Cualquier otra opción, conocida o futura, da «no».
- Con la lista de hoy ninguna corrida puede dar «sí» (§8): sin `--simular` no hay operaciones del
  bot, y `--simular` está fuera de la lista.
- **No se ejecutó el arnés** en esta rama (una invocación de `--help` en la fase 0, declarada; la
  tabla de opciones se leyó del código).
