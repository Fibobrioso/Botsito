# El umbral de construcción que habilita medir mayo

Rama `trabajo/umbral-mayo`, abierta el 2026-10-07 como tarea nocturna desde `main` en 9e4c89a
(commit de estado sobre el merge 92312e3, tag `stable/F37e-respaldo-a11`; `git rev-parse main
origin/main` dio `9e4c89a4a64f2c717fa7feaf31ea1e3b79d2c6b7` las dos). Encargo:
`docs/encargos/trabajo-umbral-mayo.md`. Es el punto J de la Next Action.

**No se ejecutó `botsito motor arnes` en esta rama**, con ningún mes. Todos los tests nuevos son
sintéticos: corridas escritas a mano, y desde la enmienda (§9) argumentos que solo se PARSEAN
con el parser real (`build_parser()`), sin ejecutar el comando. **Una salvedad, declarada:** durante la fase 0 ejecuté una vez `uv run botsito motor
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
  implementa aquí: **queda para el consultor** (§5). *(Nota posterior: resuelta; da «no», como cualquier opción fuera de la lista cerrada, §9 y §11.)*


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

> **Superado en parte por §9** (respuesta del consultor del 2026-10-07): la condición D2 ya no es
> «sin `--diagnostico-*`» sino la lista cerrada de opciones, y `informe` recibe `opciones` en vez de
> `con_diagnostico`. Lo de abajo describe el commit `d16a06e`, tal como se hizo.

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
| `uv run python docs/validation/anexos/UMBRAL-MAYO/sin_d2.py` | en `d16a06e`, `VEREDICTO: el test falla si se quita D2` (§3); desde la enmienda, `VEREDICTO: los tres tests fallan si se quita D2` (§9) |
| `make check > make-check.log 2>&1`, por commit | apertura `2102 passed` (sello `c84ee21f…`); fase 1 `2102 passed` (`d2c6477a…`); fase 2 `2111 passed` (`a827ef59…`); fase 3 `2119 passed` (`f5858a9a…`); primer revisor `2120 passed` (`23d950fc…`); enmienda `2124 passed` (`dc7c9b9a…`); el último, en el mensaje al consultor |

**No se ejecutó `botsito motor arnes`** sobre ningún mes; la única invocación fue `--help`
(cabecera). Ningún fichero de salida de una corrida entró en la rama.

## 6. Desviaciones

1. **La corrida tiene que cubrir todo `construccion`** (§0.e): D1 dice «sobre el conjunto de
   construcción vigente»; el comando admite `--meses` con una parte. Decidido en el ADR, con test.
2. **La línea dice `habilita medir el conjunto de medida (2026-05) (ADR-0070)`**, no «habilita medir
   mayo» (§3): los meses salen del criterio y no hay un nombre de mes en `src/`.
3. **`informe` exige `con_diagnostico`** (argumento obligatorio, con test): no lo pedía el encargo;
   impide que un llamador nuevo se quede en «sin diagnóstico» por omisión. *Aceptada; desde la
   enmienda el argumento obligatorio es `opciones` (§9).*
4. **`--depuracion` queda para el consultor** (§0.e y el «Impacto» del ADR). *Resuelta por la
   respuesta del consultor: da «no», como cualquier opción fuera de la lista (§9); la lista final, con `--simular`, `--perfil` y `--fase`, en §11.*
5. **La invocación `motor arnes --help`** (cabecera): contra la letra del encargo, sin efecto.

## 7. Lo que se hizo con los hallazgos del revisor

> Primera pasada, sobre `d16a06e`. El test de a2 se reescribió con la enmienda (§9): ahora comprueba
> que el comando pasa `opciones`, no `diag.activo`.

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
del subcomando; desde la segunda pasada del revisor, `--repo` también cuenta como opción fuera de
la lista (§10).

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

*(Nota posterior: el consultor resolvió esta PARADA el mismo día; la corrida que habilita lleva `--simular`, con la cuenta real y su primera fase. Lo hecho, en §11.)*

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
- **Las opciones de la corrida se leen de los propios parsers**, `cli.opciones_de_la_corrida(parsers,
  args)`: las acciones del parser raíz y del subcomando cuyo valor difiere del que su parser pone
  por defecto, con su nombre largo. Una opción que se añada mañana, al subcomando o a la raíz, sale
  ahí sin tocar nada. Los dos parsers se guardan en `args` con `set_defaults(parser_raiz=…)` y
  `set_defaults(parser_de_la_corrida=…)`, y el comando hace
  `opciones = opciones_de_la_corrida((args.parser_raiz, args.parser_de_la_corrida), args)`. El
  parser raíz entró en la segunda pasada del revisor (a1, §10): sin él, `--repo` no contaba.
- **El veredicto** (`habilita_medir`, en `cases/`) recibe `opciones_fuera`, y cada una da el motivo
  «opción fuera de la lista: <nombre>». `informe` exige ahora `opciones` (antes `con_diagnostico`).
- **ADR-0070**: un recuadro de ENMIENDA al principio y el cuerpo editado (decisiones 3 y 5, la
  alternativa descartada 3 y el impacto). El ADR no está cerrado en `main`, así que se edita en la
  rama; la versión anterior queda en `3320177`.

*(Nota posterior: la segunda enmienda, §11, añade `--simular`, `--perfil` y `--fase` a la lista; las filas de `--depuracion` y de la lista de esta tabla quedan como dice §11.)*

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
| `test_el_comando_pasa_al_informe_las_opciones_leidas_del_parser` | — | lee `cli.py` con `ast`: la única llamada a `arnes.informe` pasa `opciones`, y `opciones` es `opciones_de_la_corrida((args.parser_raiz, args.parser_de_la_corrida), args)` |

**Que los tests de D2 fallan si se quita la condición**, medido en memoria
(`anexos/UMBRAL-MAYO/sin_d2.py`, salida en `sin_d2-SALIDA.txt`): con el veredicto sustituido por uno
que ignora las opciones fuera de la lista, los tres -el del diagnóstico, el de `--depuracion` y el
de la opción inventada- FALLAN; con el código tal cual, antes y después, pasan.

`Tests Currently Passing`: 1371 → 1375.

**Hallazgo para la fila de la rama** (respuesta, punto 3; menor, sesión): se ejecutó `uv run botsito
motor arnes --help` con el encargo prohibiéndolo «con cualquier opción»; sin efecto, declarado.
Lección: la ayuda de un comando prohibido se lee en el código, no ejecutándolo. Esta vez la tabla del
§8 se leyó del código.

## 10. Lo que se hizo con la segunda pasada del revisor

| # | Gravedad | Qué se hizo |
|---|---|---|
| a1 | importa | `opciones_de_la_corrida` lee también el parser raíz: `--repo` (la única opción de la raíz que cambia la corrida; `--version` sale antes de correr) da ahora «no». Test nuevo, `test_una_opcion_del_parser_raiz_tambien_cuenta`. Es lo que pide la respuesta («cualquier otra opción presente, conocida o futura»), así que no contradice el encargo. `Tests Currently Passing`: 1376. |
| a2 | importa | El informe deja de contradecirse: §3 y §7 llevan una nota de que la enmienda los supera en parte; §5 da la salida de `sin_d2.py` de cada versión y los `make check` de la primera pasada y de la enmienda; §6.3 y §6.4 dicen cómo quedaron (aceptada; resuelta). |
| a3 | menor | El título de ADR-0070 y su fila del índice dicen ahora «solo con las opciones de una lista cerrada», en vez de «sin diagnóstico». |
| a4 | menor | La cabecera dice que, desde la enmienda, los tests también PARSEAN argumentos con el parser real. |

Las cuatro comprobaciones aparte dan SÍ, con la excepción de `--repo`, que es a1 y queda arreglada.
`sin_d2.py`, repetido tras el arreglo: `VEREDICTO: los tres tests fallan si se quita D2`.

## Informe del revisor, segunda pasada (subagente `revisor`, 2026-10-07), tal cual

## Informe del revisor · trabajo/umbral-mayo · segunda pasada (commit 51a92ca) · 2026-10-07

### Eje (a) · Reglas de la casa
Resumen: 0 bloquea, 2 importa, 2 menor.

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| a1 | importa | `opciones_de_la_corrida` no ve las opciones del parser raíz, y la más relevante es `--repo`, que cambia el repositorio entero (spec, criterio, datos). Una corrida con `--repo OTRO` y solo `--salida` habilitaría «sí» si llegara a las cifras. El encargo dice «cualquier otra opción presente, conocida o futura». Hoy `--repo` es la única opción de ese tipo (la otra es `--version`, que sale antes de correr). El §8 lo dice («`--repo` y `--version` son del parser raíz») pero no lo decide ni lo trata como opción fuera de la lista. | `cli.py:2217-2223` recorre solo `parser._actions` del subparser. `cli.py:2907` define `--repo` en la raíz. Sonda con `parse_args` y sin ejecutar el comando: `['--repo','X:/otro','motor','arnes'] -> ('--salida',)`. Arreglo mínimo, para que lo decida el consultor: pasar también el parser raíz, o dar «no» si `args.repo` difiere del valor por defecto. |
| a2 | importa | El informe quedó contradictorio tras la enmienda. §9 describe el código nuevo, pero §3, §5, §6 y §7 siguen describiendo el viejo (`con_diagnostico`, `diag.activo`) sin una nota de que quedan superadas. En §5 el comando `sin_d2.py` sigue con la salida vieja `VEREDICTO: el test falla si se quita D2`; la real hoy es `los tres tests fallan si se quita D2`. §6.3 dice «`informe` exige `con_diagnostico`» y §6.4 dice «`--depuracion` queda para el consultor», cuando ya da «no». §5 tampoco lista los comandos de esta pasada, y la fila de `make check` dice «el del commit del revisor, en su mensaje», pero el mensaje de 51a92ca no trae cifras. | `docs/validation/UMBRAL-MAYO.md:63,67,137-141,156,165,194,206-209,216`. La salida real de `sin_d2.py` está en la comprobación 2. |
| a3 | menor | El título del ADR-0070 y su fila del índice siguen diciendo «sin diagnóstico». La regla ahora es la lista cerrada, y `--depuracion` mostró que «sin diagnóstico» no basta. | `docs/adr/0070-umbral-de-construccion-para-medir-mayo.md:6` y `docs/adr/README.md:76`. |
| a4 | menor | La cabecera del informe sigue diciendo «Todos los tests nuevos son sintéticos». Es cierto, pero los tests nuevos de la enmienda parsean con `build_parser()`, y esto no se declara ahí (sí en §9). | `UMBRAL-MAYO.md:7-14` frente a `:372-373`. |

Comprobado sin hallazgos:
- **Contrato:** `uv run python scripts/contrato_rama.py` da `CONTRATO: 18 ficheros dentro del contrato de trabajo/umbral-mayo (riesgo medio …, 6 comprobaciones para el revisor)`.
- **`make check`:** `make-check.log` tiene `SELLO: … dc7c9b9a1f512556ebe285d6af33e9c419bd963c` y `PICO DE MEMORIA … 290 MiB`. `git rev-parse 51a92ca^{tree}` da ese mismo árbol, así que el sello es del commit revisado. `git status --short` sale limpio.
- **Otras comprobaciones:**
  - `state check` da OK.
  - `knowledge validate` da OK, con 152 registros de feedback y 503 items de evidencia, historial intacto y commits con Fuente.
  - El commit lleva `Fuente: ADR-0070` en el cuerpo (no toca `knowledge/spec` ni `knowledge/cases`).
  - El `## Estado` del ADR sigue siendo `ACTIVE`.
  - `Tests Currently Passing` pasa de 1371 a 1375: son los 4 tests nuevos de `test_umbral_mayo.py`.
- **Ficheros no tocados por la enmienda:** ningún cambio en `.claude/`, `Makefile`, `src/botsito/domain` ni en `knowledge/`.

### Eje (b) · Encargo (respuesta del consultor del 2026-10-07)
Resumen: 0 bloquea, 0 importa, 0 menor. Requisitos: 11 hechos, 0 parciales, 0 no hechos.

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 1 | Lista CERRADA `--salida`, `--tracemalloc`, `--meses`; cualquier otra da «no» | Hecho | `engine/arnes.py:64`; `arnes.informe` calcula `set(opciones) - OPCIONES_QUE_NO_CAMBIAN_LA_CORRIDA` (`:250`) |
| 2 | `--meses` solo vale si cubre todo el conjunto | Hecho | `habilita_medir` mantiene la condición de `faltan` (`criterio_fidelidad.py`); `test_una_corrida_sobre_parte_de_construccion_no_habilita` |
| 3 | Motivo «opción fuera de la lista: <nombre>» | Hecho | `criterio_fidelidad.py`: `f"opción fuera de la lista: {o}"`; los tests lo comprueban literal |
| 4 | La lista vive en un solo sitio, con comentario que cita ADR-0070 | Hecho | `arnes.py:60-64` (comentario con «ADR-0070 (enmienda del 2026-10-07)»); un solo `grep` de la constante en `src` |
| 5 | Test: `--depuracion` da «no» | Hecho | `test_depuracion_da_no` |
| 6 | Test: opción inventada añadida al parser da «no» | Hecho | `test_una_opcion_nueva_del_parser_da_no_sin_tocar_la_lista` |
| 7 | Test: solo las de la lista da «sí» si llega a las cifras | Hecho | `test_solo_las_de_la_lista_y_que_llega_da_si` |
| 8 | El test de diagnóstico sigue fallando si se quita la condición | Hecho | comprobación 2 |
| 9 | ADR: recuadro de enmienda, cuerpo editado y dicho en el informe | Hecho | ADR líneas 12-20; §9 «ADR-0070: un recuadro de ENMIENDA … la versión anterior queda en `3320177`» |
| 10 | Tabla de TODAS las opciones leída del código, sin ejecutar el comando | Hecho | §8; comprobación 3 |
| 11 | PARA solo en `--simular`; el resto del punto 1 hecho; no se ejecuta el arnés | Hecho | §8 «PARA en el punto de `--simular`, y solo en él»; Estado del informe; `--simular` queda fuera de la lista |

Lo que no hay que olvidar: la copia de la respuesta en encargo e informe es literal (diff de encargo vs §«Respuesta del consultor»). Los hallazgos a1 y a2 son del eje (a) y no mezclan.

### Comprobaciones aparte
1. **Una opción nueva del parser da «no» sin tocar la lista: SÍ en lo pedido, con una excepción (a1).**
   - `uv run python -m pytest -p no:cacheprovider tests/unit/test_umbral_mayo.py -q` da 22 passed.
   - **Cómo funciona:** el test añade `--opcion-inventada` a `probe.parser_de_la_corrida` (el mismo subparser, vía `set_defaults`) y parsea con ese parser. `opciones_de_la_corrida` lee `parser._actions` en vivo (`cli.py:2217`), la opción sale, `arnes.informe` la resta de la lista y `habilita_medir` la convierte en motivo. La lista queda como el mismo objeto (`is lista_antes`).
   - **Valor igual al por defecto:** no hay caso hoy. Las 13 opciones del subparser tienen default `None` o `False`, y las `store_true` tienen default `False`, así que dar la opción siempre difiere. Sondeado: `--meses ""` sale como `--meses`, `--diagnostico-a27 0` sale (0 ≠ None), y los prefijos abreviados `--sim --dep` salen como `--simular` y `--depuracion`. Una opción futura con `default=X` pasada explícitamente como X no se detectaría, pero entonces coincide con la corrida por defecto y no cambia nada.
   - **`store_true` con default distinto de `False`:** no existe hoy, y el mismo razonamiento cubre un default `True`.
   - **`--repo` (parser raíz):** NO se detecta, y es el hallazgo a1. Las acciones del subparser no incluyen las de la raíz.
2. **Los tests de D2 fallan sin la condición: SÍ.** `uv run python docs/validation/anexos/UMBRAL-MAYO/sin_d2.py` dio, con exit 0:
   ```
   test_una_corrida_con_diagnostico_que_llega_a_las_dos_sale_no: con D2 pasa; sin D2 FALLA (AssertionError); restaurado pasa
   test_depuracion_da_no: con D2 pasa; sin D2 FALLA (AssertionError); restaurado pasa
   test_una_opcion_nueva_del_parser_da_no_sin_tocar_la_lista: con D2 pasa; sin D2 FALLA (AssertionError); restaurado pasa
   VEREDICTO: los tres tests fallan si se quita D2
   ```
   El script no ejecuta `motor arnes`: parchea `arnes.habilita_medir` en memoria y llama a las funciones de test. Coincide con `sin_d2-SALIDA.txt`.
3. **La tabla del §8 corresponde al código: SÍ.**
   - **Opciones:** el subparser (`cli.py:3066-3082`) tiene `--salida`, `--meses`, `--tracemalloc`; `_opciones_simulacion` (`:2324-2347`) añade `--simular`, `--depuracion`, `--perfil`, `--fase`; `_opciones_diagnostico` (`:2270-2321`) añade `--diagnostico-a35`, `-a21`, `-a44`, `-a47`, `-a27` y `-cuenta-diaria`. Son 13, la tabla tiene 13 y la salida del sondeo da las mismas. `--repo` y `--version` son de la raíz, como dice el §8. Los números de línea citados son correctos.
   - **`--simular`:** `engine/motor.py:233` es `return ResultadoDia(dia.dia.isoformat(), (), trazas)`, y es el único `ResultadoDia(` de `motor.py`. Sin `--simular`, `motor_arnes` usa `MotorSpec` (`cli.py` ~2425-2431) y no produce operaciones. `engine/cableado.py:250` devuelve `self._operaciones_del_bot(...)`, y esa función (`:329-351`) toma las posiciones del broker con `abierta_ms` y sesión. Lo afirmado es cierto.
   - **Matices menores del §8:**
     - «`validar_meses` niega medida y lo ajeno» es correcto (`arnes.py:89-102`).
     - La afirmación «hoy ninguna corrida puede dar sí» se sostiene: sin `--simular` no hay operaciones del bot, y con ella la opción está fuera de la lista.
4. **Nadie ejecutó `motor arnes`: SÍ, para este commit.**
   - `grep` de `motor_arnes`, `main(`, `subprocess`, `os.system` y `--help` en `tests/unit/test_umbral_mayo.py` y en los `.py` de `anexos/UMBRAL-MAYO` solo da `def main` de `sin_d2.py`.
   - `git log -p -S"motor arnes"` sobre `tests`, `scripts` y anexos solo muestra docstrings que mencionan el comando.
   - Los tests solo llaman a `build_parser().parse_args(...)` y a `opciones_de_la_corrida`, nunca a `motor_arnes`.
   - `motor_arnes` solo se llama desde el despacho de `cli.py:3333`.
   - Lo único de esta pasada que toca el comando real es lo que ejecuté yo: `parse_args` en una sonda. No se ha ejecutado el arnés.
   - Nota: en el commit 51a92ca no puedo ver qué hizo la sesión de Claude Code, solo su resultado. El `--help` anterior sigue declarado (cabecera) y el consultor ya lo trató.

### Lo que no pude comprobar
- **Orden de trabajo:** si la tabla del §8 se escribió «antes» del punto 1, como pide el consultor, no se puede saber (todo entra en un solo commit).
- **Control de la fila de ERRORES-RECURRENTES:** el «hallazgo para la fila de la rama» (punto 3 de la respuesta) está en §9 del informe, pero la fila en `docs/runbooks/ERRORES-RECURRENTES.md` no aparece en este diff. Es del cierre, no de esta pasada.
- **`make check`:** no lo ejecuté, por encargo. Me apoyé en `make-check.log` (sello `dc7c9b9a…`, igual al árbol de 51a92ca).

### Comandos ejecutados
1. `git log --format='%h %s' main..HEAD`, `git show --stat 51a92ca`, `git status --short`
2. `git show 51a92ca -- src tests scripts docs/validation/anexos`
3. `uv run python docs/validation/anexos/UMBRAL-MAYO/sin_d2.py`
4. `grep` de `_opciones_simulacion`, `_opciones_diagnostico`, `def build_parser` y `mt_arnes` en `cli.py`; lecturas de `cli.py` 2268-2397, 2397-2445, 2900-2920 y 3060-3090
5. `uv run python -m pytest -p no:cacheprovider tests/unit/test_umbral_mayo.py -q` (22 passed)
6. `grep` de `motor_arnes`, `parser_de_la_corrida`, `OPCIONES_QUE_NO`, `opciones_de_la_corrida` en `src`, `tests`, `scripts` y anexos
7. Lecturas de `engine/motor.py` 225-240, `engine/cableado.py` 240-262 y 326-352 y `engine/arnes.py` 89-103
8. `git diff 1cfc14a 51a92ca -- docs/encargos/trabajo-umbral-mayo.md PROJECT_STATE.md` y `git diff 1cfc14a 51a92ca -- docs/adr/0070-...md`
9. `grep` de `motor_arnes|main(|subprocess|os.system|--help` en el test y los anexos; `git log -p -S"motor arnes" main..HEAD -- tests scripts docs/validation/anexos Makefile`
10. `uv run python scripts/contrato_rama.py`; `uv run botsito state check`; `tail`/`grep SELLO|PICO` de `make-check.log`; `git rev-parse 51a92ca^{tree}`; `git diff main...HEAD --stat -- .claude Makefile src/botsito/domain`
11. `grep` de `con_diagnostico|diag.activo|…` sobre `docs/validation/UMBRAL-MAYO.md`; `uv run botsito knowledge validate`
12. Sonda con `uv run python -c` (solo `build_parser().parse_args` y `opciones_de_la_corrida`, sin ejecutar el comando); un primer intento con `Write` falló porque la herramienta está deshabilitada, y no escribió nada.

## Respuesta del consultor a la PARADA de `--simular` (2026-10-07), tal cual

> Modelo: Opus · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA de --simular en trabajo/umbral-mayo (2026-10-07). Cópiala tal cual al encargo y al informe.
>
> 1. La corrida que habilita medir el conjunto de medida LLEVA --simular, obligatoriamente. Por qué: sin ella el motor no produce operaciones (engine/motor.py:233), y ADR-0043 compara instantes de LLENADO, que solo da el bróker simulado (cableado.py:250); además es como operará el bot. Una corrida sin --simular da «no» con el motivo «sin simulación».
> 2. --perfil y --fase: solo se admiten con el perfil de la cuenta real (FTMO 2-Step Swing 100k, ADR-0026) y su PRIMERA fase. Antes de escribir, lee en el código los valores por defecto de las dos y el nombre de ese perfil y esa fase en knowledge/cuentas/, y déjalo en el informe. La regla se escribe como condición: el perfil y la fase EFECTIVOS de la corrida (dados o por defecto) tienen que ser esos dos; cualquier otro valor da «no» con su motivo. Si el perfil por defecto no es el de FTMO 2-Step Swing 100k, o no hay una fase que sea claramente la primera, PARA y dímelo.
> 3. La lista cerrada queda: --salida, --tracemalloc, --meses (cubriendo todo construcción), --simular (obligatoria), --perfil y --fase (solo con los valores del punto 2). Todo lo demás, incluido --repo, --depuracion y cualquier opción futura, da «no». Lo de los ticks queda cubierto: un día sin ticks exige --depuracion, que da «no».
> 4. Tests que lo rompan a propósito: sin --simular da «no»; --simular con otro perfil o con otra fase da «no»; --simular con perfil y fase por defecto y con las cifras da «sí»; los anteriores siguen. ADR-0070: su recuadro de enmienda recoge 1 a 3, con fecha.
>
> Sigue sin ejecutarse el arnés. knowledge validate, make check y state check en verde, y el revisor sobre lo cambiado, comprobando aparte que sin --simular nunca sale «sí».
>
> Rama lista para revisión, NO cerrada.

## 11. La corrida que habilita, simulada con la cuenta real y su primera fase (respuesta a la PARADA)

### 11.1 Los valores por defecto de `--perfil` y `--fase`, leídos del código (punto 2)

Leídos sin ejecutar nada, antes de escribir la regla:

| Qué | Dónde | Valor |
|---|---|---|
| `--perfil` por defecto | `cli.py:2346-2349`, `default=None` («por defecto, el unico») | `None` |
| Qué hace `None` | `engine/cableado.py:421-435`, `perfil_del_repo`: si `knowledge/cuentas/` tiene un solo `*.yaml`, ese; con varios, error que pide `--perfil` | el único perfil |
| Perfiles en `knowledge/cuentas/` | `ls knowledge/cuentas/`: `README.md`, `cierres/`, `ftmo-2step-swing-100k.yaml` | uno: `ftmo-2step-swing-100k` |
| Su nombre en el código | `engine/perfil_cuenta.py:69-70`, `PerfilCuenta.nombre = ruta.stem`; `cableado.py:486`, `perfil=perfil.nombre` | `ftmo-2step-swing-100k` |
| Que es FTMO 2-Step Swing 100k | ADR-0026 («La prop firm es FTMO, reto 2-Step, tipo de cuenta Swing», tamaño 100.000 USD); el yaml, `firma_programa: "2-step"` (R1) | sí |
| `--fase` por defecto | `cli.py:2351-2354`, `default=None` («por defecto, la primera que declara») | `None` |
| Qué hace `None` | `cableado.py:470`, `fase_real = fase if fase is not None else perfil.fases()[0]` | la primera del perfil |
| Las fases del perfil | `perfil_cuenta.py:81-82`, `fases()` = `firma_fases` partido por espacios; el yaml, `firma_fases: "reto verificacion fondeada"`, «las fases del programa, en el orden en que se pasan. R1: reto («FTMO Challenge»), verificacion («Verification») y fondeada» | primera: `reto` |

**El perfil por defecto ES el de FTMO 2-Step Swing 100k, y hay una fase que es claramente la
primera** (`reto`: el programa declara sus fases en el orden en que se pasan, y R1 lo dice). No se
dan las condiciones de PARA del punto 2.

### 11.2 Lo que se hizo

- **La regla, como condición sobre los valores EFECTIVOS.** `cases/criterio_fidelidad.py` gana
  `Simulacion(perfil, fase, primera_fase)`, y `habilita_medir` recibe `simulacion` (obligatorio, sin
  valor por defecto): `None` da «sin simulación»; un perfil distinto de `perfil_para_medir` da
  «perfil <nombre>: solo cuenta <perfil_para_medir>»; una fase distinta de la primera del perfil da
  «fase <nombre>: solo cuenta la primera del perfil, <primera>». Los motivos se suman a los de
  siempre.
- **El perfil que cuenta vive en el criterio, no en el código** (ADR-0002; ADR-0050: ningún nombre
  de firma en el código): campo nuevo `perfil_para_medir: ftmo-2step-swing-100k` en
  `knowledge/cases/criterio_fidelidad.yaml`, cargado y validado (texto no vacío). La primera fase no
  es un campo: sale del propio perfil, así que no puede desalinearse de él.
- **El comando pasa lo efectivo.** `cli.py`, rama `--simular`: `simulacion =
  Simulacion(motor.perfil, motor.fase, perfil_cuenta.fases()[0])`, con el perfil y la fase que el
  motor cableado usó de verdad (`cableado.py:486-487`, ya resueltos los `None`); sin `--simular`,
  `simulacion = None`. Una `--fase` que el perfil no tenga no llega al veredicto: el cableado la
  rechaza antes (`reglas_de_fase`).
- **La lista cerrada** (`engine/arnes.py`, `OPCIONES_QUE_NO_CAMBIAN_LA_CORRIDA`) queda `--salida`,
  `--tracemalloc`, `--meses`, `--simular`, `--perfil` y `--fase`, con el comentario que dice cuáles
  se comprueban aparte. `--repo`, `--depuracion`, los `--diagnostico-*` y cualquier opción futura
  siguen dando «no». `--perfil` y `--fase` sin `--simular` están en la lista, pero la corrida da «sin
  simulación».
- **ADR-0070**: un segundo recuadro de ENMIENDA, fechado, con los puntos 1 a 3, y el cuerpo editado
  (decisiones 3 y 5, una razón más en «Por que elegimos», el impacto; se quita «queda para el
  consultor»). El ADR sigue sin estar en `main`; la versión anterior queda en `5e46075`. Al
  reescribir el impacto, la frase «el motor necesita además los diagnósticos de A-21, A-35 y A-44»
  pasa a atribuirse al encargo: no se midió en la rama (medirlo exigía correr el arnés).

### 11.3 Tests (`tests/unit/test_umbral_mayo.py`), sintéticos y sin ejecutar el comando

La corrida «buena» de los tests anteriores lleva ahora `--simular` y una `Simulacion` válida (el
perfil del criterio de prueba y `fase == primera_fase`); los anteriores siguen y siguen pasando.

| Test | Qué rompe | Línea o comprobación |
|---|---|---|
| `test_sin_simular_da_no` | la corrida que llega a las cifras, sin `--simular` | `…: no (sin simulación)` |
| `test_sin_simulacion_nunca_sale_si` | sin simulación, tres medidas (una perfecta, 10/10 y 10/10) por dos juegos de opciones de la lista | nunca «sí»; siempre con «sin simulación» |
| `test_simular_con_otro_perfil_da_no` | `--simular --perfil otra-cuenta` | `…: no (perfil otra-cuenta: solo cuenta perfil-de-prueba)` |
| `test_simular_con_otra_fase_da_no` | `--simular --fase verificacion` | `…: no (fase verificacion: solo cuenta la primera del perfil, reto)` |
| `test_simular_con_perfil_y_fase_por_defecto_y_las_cifras_da_si` | `--simular` solo, con las cifras | `…: sí` |
| `test_perfil_y_fase_dados_con_los_valores_que_cuentan_da_si` | `--simular --perfil <el que cuenta> --fase reto` | `…: sí` |
| `test_el_perfil_que_cuenta_es_el_unico_perfil_del_repositorio_y_su_primera_fase_es_reto` | — | sobre el repositorio real: `perfil_para_medir` es el único yaml de `knowledge/cuentas/` y su primera fase es `reto` (lo de §11.1, fijado) |
| `test_depuracion_da_no` (reescrito) | `--simular --depuracion` | `…: no (opción fuera de la lista: --depuracion)`: `--simular` ya no es motivo |
| `test_la_lista_es_exactamente_la_de_la_enmienda` (reescrito) | — | las seis opciones |
| `test_el_informe_exige_decir_que_opciones_uso_la_corrida_y_si_simulo` (renombrado) | llamar a `informe` sin `opciones` o sin `simulacion` | `TypeError` |
| `test_el_comando_pasa_al_informe_las_opciones_y_la_simulacion` (renombrado) | — | lee `cli.py` con `ast`: la única llamada a `arnes.informe` pasa `opciones=opciones, simulacion=simulacion`, y `simulacion` se asigna `Simulacion(motor.perfil, motor.fase, perfil_cuenta.fases()[0])` o `None` |

`test_llega_a_las_dos_sin_diagnostico_y_sobre_todo_el_conjunto_habilita` pasa a llamarse
`test_llega_a_las_dos_simulada_y_sobre_todo_el_conjunto_habilita`. `Tests Currently Passing`:
1376 → 1383 (siete funciones nuevas).

**Que los tests fallan si se quita cada condición**, medido en memoria
(`anexos/UMBRAL-MAYO/sin_d2.py`, ampliado; salida en `sin_d2-SALIDA.txt`): dos mutaciones del
veredicto que usa el arnés, «sin la lista» (ignora las opciones fuera) y «sin la simulación»
(recibe siempre una simulación válida). Con cada una fallan sus cuatro tests (los de la lista: el
diagnóstico, `--depuracion`, la opción inventada y `--repo`; los de la simulación: sin `--simular`,
nunca «sí» sin simulación, otro perfil y otra fase), y restaurado pasan:
`VEREDICTO: los ocho tests fallan si se quita su condicion`.

### 11.4 Comandos de esta parte

| Comando | Salida |
|---|---|
| `uv run ruff check src tests`, `uv run ruff format --check src tests` | limpio |
| `uv run mypy` | `Success: no issues found in 242 source files` |
| `uv run pytest tests/unit/test_umbral_mayo.py -q` | 30 pasan |
| `uv run python docs/validation/anexos/UMBRAL-MAYO/sin_d2.py` | `VEREDICTO: los ocho tests fallan si se quita su condicion` |
| `uv run botsito state check` | `OK` |
| `make check > make-check.log 2>&1` (commit `071c30f`) | `2132 passed`; `SELLO: make check en verde sobre el arbol adbb6932933506e11eb047444ee91c99e2b39956` (el de `071c30f`); `PICO DE MEMORIA` 291 MiB; `exit=0` |

No se ejecutó `botsito motor arnes` en esta parte, de ninguna forma.

## 12. Lo que se hizo con la tercera pasada del revisor

| # | Gravedad | Qué se hizo |
|---|---|---|
| a1 | menor | Notas posteriores junto a §0.e (`--depuracion`, resuelta) y a §6.4 (la lista final, en §11); las de §8 y la tabla de §9 ya estaban. La fila 11 que señala (`--simular` «queda fuera de la lista») está DENTRO del informe pegado de la segunda pasada, que se deja tal cual: describe el estado de `51a92ca`/`5e46075`, y el estado final es el de §11 y `## Estado`. |
| a2 | menor | §11.4 recoge el `make check` de `071c30f`: `2132 passed`, el sello del árbol `adbb6932…` (el de `071c30f`), 291 MiB, `exit=0`. |
| b1 | menor | Sin cambio: es la limitación declarada (el enlace entre el comando y el veredicto se prueba leyendo el código con `ast`, porque probarlo con el comportamiento exigiría ejecutar el arnés, prohibido). Queda para el consultor por si la rama de medida quiere un test que lo ejecute. |

Las tres comprobaciones aparte dan SÍ: sin `--simular` nunca sale «sí» (sin camino en el código y
con las mutaciones de `sin_d2.py`: `VEREDICTO: los ocho tests fallan si se quita su condicion`), el
perfil y la fase del veredicto son los efectivos, y ningún commit ejecutó el arnés.

## Informe del revisor, tercera pasada (subagente `revisor`, 2026-10-07), tal cual

## Informe del revisor · trabajo/umbral-mayo · tercera pasada (commit 071c30f) · 2026-10-07

Rama `trabajo/umbral-mayo`, HEAD `071c30f`. `git status --short` limpio. Diff revisado: `git diff 5e46075 071c30f` (15 ficheros). Todos están dentro de `rutas_permitidas` (`contrato_rama.py`: «18 ficheros dentro del contrato»). Ninguna ruta protegida cambia: no hay cambios en `knowledge/spec/`, `engine/motor.py`, `cableado.py`, `broker.py` ni `.claude/`.

### Eje (a) · Reglas de la casa
Resumen: 0 bloquea, 0 importa, 2 menor.

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| a1 | menor | El informe conserva afirmaciones anteriores que la segunda enmienda deja falsas, sin nota junto a ellas. La tabla de tests de §9 sigue diciendo que `test_depuracion_da_no` da `…--depuracion; …--simular` y que la lista es `{--salida, --tracemalloc, --meses}`. §0.e, línea 91 («`--depuracion` … queda para el consultor») y §6.4 solo se corrigen en parte. Hay una nota de §11 en §8 (línea 359) y en la tabla de §9 (línea 387). Faltan en §0.e y en la tabla encargo-frente-a-hecho (fila 11, línea 466: «`--simular` queda fuera de la lista»). Es historia de la rama y no engaña a quien lea hasta §11, pero la fila 11 contradice el estado final. | `docs/validation/UMBRAL-MAYO.md:91`, `:395`, `:396-ss` (tabla §9), `:466`. Notas posteriores solo en `:359` y `:387`. |
| a2 | menor | §11.4 no recoge el `make check` de este commit. El informe de la rama dice que «el último, en el mensaje al consultor». Lo he comprobado yo: `make-check.log` termina en `2132 passed`, `SELLO … adbb6932933506e11eb047444ee91c99e2b39956`, `PICO DE MEMORIA … 291 MiB`, `exit=0`. Ese árbol es el de `HEAD^{tree}`. Conviene dejar el sello y el recuento en §11.4. | `make-check.log:67`, `git rev-parse HEAD^{tree}` = `adbb6932…`. `docs/validation/UMBRAL-MAYO.md` §11.4 (solo ruff, mypy, pytest, anexo y `state check`). |

Comprobado sin hallazgos:
- **Contrato.** `uv run python scripts/contrato_rama.py` da `CONTRATO: 18 ficheros dentro del contrato de trabajo/umbral-mayo (riesgo medio, …, 6 comprobaciones para el revisor)`.
- **Comprobaciones del contrato que no escriben:**
  - `pytest tests/unit/test_umbral_mayo.py -q`: 30 puntos, sin fallos.
  - `sin_d2.py`: `VEREDICTO: los ocho tests fallan si se quita su condicion`.
  - `botsito state check`: `OK: rama 'trabajo/umbral-mayo'…`.
  - `knowledge validate` forma parte de `make check`, y `make-check.log` trae `OK: 503 items de evidencia, 0 contradicciones abiertas, historial intacto`. No hay `knowledge-validate.log` suelto.
- **Calidad.** `ruff check src tests` limpio, `ruff format --check` con 242 ficheros ya formateados, `mypy` sin problemas en 242 ficheros.
- **Trailer `Fuente:`.** `071c30f` lleva `Fuente: ADR-0070` en el cuerpo. El ADR existe y la rama no toca `knowledge/spec/` ni `knowledge/cases/` de valor: solo añade `perfil_para_medir` a `criterio_fidelidad.yaml` (el trailer lo cubre).
- **ADR-0002 / ADR-0050.** `git diff 5e46075 071c30f -- src | grep -i ftmo` no devuelve nada, así que no hay nombre de firma en `src/`. El nombre `ftmo-2step-swing-100k` vive solo en `knowledge/cases/criterio_fidelidad.yaml`, y el código lo lee de `Criterio.perfil_para_medir`. Los umbrales siguen en el yaml.
- **Texto no vacío.** `_texto()` valida el campo, y los cinco constructores de `Criterio` en los tests pasan el campo nuevo.
- **ADR-0070.** `status: ACTIVE`. La segunda enmienda es un recuadro fechado (2026-10-07) con los puntos 1 a 3 del consultor. La decisión 3 y la 5, «Por qué elegimos» e «Impacto» están coherentes con ella. La fila del índice (`docs/adr/README.md:76`) ya refleja la lista cerrada y sigue en `ACTIVE`.
- **`Tests Currently Passing`.** El campo pasa de 1376 a 1383, y `state check` da OK. `test_umbral_mayo.py` pasa de 17 a 24 `def test_` (+7), como dice §11.3.
- **Líneas citadas en §11.1.** Existen y dicen lo que el informe afirma:
  - `cli.py:2346-2354`: `--perfil` y `--fase` con `default=None`.
  - `cableado.py:421-435`: `perfil_del_repo`, con el único perfil si no se da nombre.
  - `cableado.py:470`: `fase_real = fase if fase is not None else perfil.fases()[0]`.
  - `cableado.py:486-487`: `perfil=perfil.nombre`, `fase=fase_real`.
  - `perfil_cuenta.py:69-70` y `81-82`.
  - `knowledge/cuentas/ftmo-2step-swing-100k.yaml:37` (`firma_programa "2-step"`) y `:86` (`firma_fases "reto verificacion fondeada"`).
  - `ls knowledge/cuentas`: un solo perfil.
  - ADR-0026 (título «FTMO, reto 2-Step, tipo Swing»).
  - `engine/motor.py:233` y `cableado.py:250`, citados por el consultor, existen y son lo que se dice.
- **Afirmación del ADR sobre los diagnósticos.** El ADR y el informe atribuyen al encargo (D2, línea 17) que el motor necesita hoy A-21, A-35 y A-44. Dicen explícitamente que no se midió, y no afirman más de lo que la cita sostiene.
- **Informe y Estado.** `## Estado` es la última sección, el informe existe y la copia de la respuesta del consultor está en encargo e informe (misma frase, línea a línea).
- **Rutas del contrato y regímenes.** No se toca `knowledge/evidence/`, `feedback/`, manifests, corpus, holdout ni informes cerrados de `main`. El único `-` en el informe de la rama es el `## Estado` anterior, que es de la rama.
- No aplican: puntos 5 (ambigüedades), 8 (guardias de citas) ni 10 (evidencia nueva), porque no hay cambios en esos sitios.

### Eje (b) · Encargo
Resumen: 0 bloquea, 0 importa, 1 menor. Requisitos: 9 hechos, 0 parciales, 0 no hechos (las respuestas anteriores ya estaban cubiertas en pasadas previas).

| # | Requisito (respuesta a la PARADA de `--simular`) | Estado | Evidencia |
|---|---|---|---|
| 1 | Sin `--simular`, «no» con motivo «sin simulación» | Hecho | `criterio_fidelidad.py:197-198` (`motivos.append("sin simulación")`); `test_sin_simular_da_no` y `test_sin_simulacion_nunca_sale_si` pasan |
| 2a | Leer en el código los valores por defecto de `--perfil` y `--fase`, y el nombre del perfil y de la fase en `knowledge/cuentas/`, y dejarlo en el informe | Hecho | §11.1, con las líneas citadas verificadas arriba |
| 2b | Condición sobre los valores EFECTIVOS (dados o por defecto) | Hecho | `cli.py:2441`, `Simulacion(motor.perfil, motor.fase, perfil_cuenta.fases()[0])`; `criterio_fidelidad.py:200-206`; ver comprobación aparte 2 |
| 2c | PARAR si el perfil por defecto no es el de FTMO 2-Step Swing 100k o no hay primera fase clara | Hecho (no se dan las condiciones de parada) | El perfil por defecto es el único de `knowledge/cuentas/`, y `firma_fases` empieza por `reto` (yaml línea 86) |
| 3 | Lista cerrada: `--salida`, `--tracemalloc`, `--meses`, `--simular`, `--perfil`, `--fase`; todo lo demás, incluidos `--repo` y `--depuracion`, da «no» | Hecho | `arnes.py` (`OPCIONES_QUE_NO_CAMBIAN_LA_CORRIDA`, seis opciones, con comentario que cita ADR-0070); `test_la_lista_es_exactamente_la_de_la_enmienda`, `test_depuracion_da_no`, `test_una_opcion_del_parser_raiz_tambien_cuenta` |
| 4a | Test: sin `--simular`, «no» | Hecho | `test_sin_simular_da_no` |
| 4b | Test: otro perfil o otra fase, «no» | Hecho | `test_simular_con_otro_perfil_da_no`, `test_simular_con_otra_fase_da_no` |
| 4c | Test: perfil y fase por defecto con las cifras, «sí» | Hecho | `test_simular_con_perfil_y_fase_por_defecto_y_las_cifras_da_si`, `test_perfil_y_fase_dados_con_los_valores_que_cuentan_da_si` |
| 4d | Los tests anteriores siguen | Hecho | Los reescritos solo pierden el motivo `--simular`. 30 pasan |
| 4e | ADR-0070 con recuadro de enmienda fechado con 1 a 3 | Hecho | `docs/adr/0070-*.md` líneas 22-40 (`ENMIENDA (2026-10-07 …)`, con los tres puntos) |
| 5 | Informe `UMBRAL-MAYO.md` §11 y Estado | Hecho | §11 y `## Estado` actualizados |
| 6 | El arnés sigue sin ejecutarse; `make check`, `state check` y `knowledge validate` en verde | Hecho | Ver comprobación aparte 3 y el sello de a2 |

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| b1 | menor | Lo que pide el encargo, «comprobando aparte que sin --simular nunca sale sí», se cumple en el veredicto. La conexión entre el comando y el veredicto, en cambio, solo la prueba un test sobre el texto del código (`ast` + cadena `Simulacion(motor.perfil, motor.fase, perfil_cuenta.fases()[0])`). No hay un test de comportamiento que pase por `motor_arnes`, y no puede haberlo sin ejecutar el arnés. Es una limitación asumida y declarada («se lee el código, sin ejecutar el comando»), no un fallo. | `tests/unit/test_umbral_mayo.py` (`test_el_comando_pasa_al_informe_las_opciones_y_la_simulacion`, últimas líneas) |

Lo que la rama hace y el encargo no pide: nada relevante. El campo `perfil_para_medir` y la clase `Simulacion` son la forma de escribir la condición sin nombre de firma en `src/` (ADR-0050), y el informe lo dice (§11.2). El cambio de `Criterio` obligó a tocar los cinco constructores de test (`test_arnes_motor`, `test_cableado`, `test_huecos_motor`, `test_visor`, `test_umbral_mayo`), y es mecánico. No se tocó nada que el encargo diga que no se toque.

### Comprobaciones aparte

**1. Sin `--simular` nunca sale «sí»: confirmado.**
- `habilita_medir` (`criterio_fidelidad.py:182-218`) tiene `simulacion` como argumento keyword obligatorio, sin valor por defecto. Con `simulacion is None` añade el motivo «sin simulación». Devuelve `Veredicto(not motivos, …)`, así que con un motivo no puede habilitar, vengan las cifras que vengan.
- `arnes.informe` (`arnes.py:~250-265`) también exige `simulacion` keyword sin valor por defecto, y se lo pasa tal cual. No hay otro llamador de `informe` ni de `habilita_medir` en `src/` ni en `scripts/` (`grep`).
- En `motor_arnes` (`cli.py:~2420-2452`): la rama `else` (sin `--simular`) asigna `simulacion = None`. La rama `if args.simular` es la única que construye `Simulacion`. No hay camino con `simulacion` distinto de `None` sin `--simular`, ni un valor por defecto que lo eluda.
- `--perfil` y `--fase` sin `--simular` están en la lista, pero el veredicto da «no (sin simulación)».
- `uv run python docs/validation/anexos/UMBRAL-MAYO/sin_d2.py` (en memoria, sin escribir) dio: `VEREDICTO: los ocho tests fallan si se quita su condicion`. Con la condición quitada fallan los cuatro de la lista y los cuatro de la simulación (`test_sin_simular_da_no`, `test_sin_simulacion_nunca_sale_si`, `test_simular_con_otro_perfil_da_no`, `test_simular_con_otra_fase_da_no`). Restaurados, pasan. La mutación «sin la simulación» sustituye perfil y fase a la vez, y no separa cada una. Se cubre porque cada test rompe una sola.

**2. El perfil y la fase del veredicto son los EFECTIVOS: confirmado.**
- `cli.py:2441`: `Simulacion(motor.perfil, motor.fase, perfil_cuenta.fases()[0])`.
- `motor` es el `MotorCableado` que devolvió `construir_motor_cableado`. Sus campos son `perfil=perfil.nombre` y `fase=fase_real` (`cableado.py:486-487`), ya con el `None` resuelto (`fase_real = fase if fase is not None else perfil.fases()[0]`, línea 470).
- `perfil_cuenta` es el mismo objeto que se le pasó al motor. `args.perfil` y `args.fase` crudos no llegan al veredicto.
- Una `--fase` inexistente la rechaza `reglas_de_fase` antes de llegar al veredicto.

**3. Ningún commit de la rama ejecutó `botsito motor arnes`: no hay evidencia de lo contrario, con una salvedad ya declarada.**
- Los tests solo hacen `build_parser().parse_args([...])` y `opciones_de_la_corrida`. `grep` de `motor_arnes|subprocess|os.system` en `test_umbral_mayo.py` y en los anexos: sin llamadas. El único `main()` es el de `sin_d2.py`, que parchea `arnes.habilita_medir` y llama a funciones de test.
- `git log -p -S"motor arnes" main..HEAD -- tests scripts Makefile docs/validation/anexos` solo muestra docstrings y comentarios.
- Los mensajes de commit dicen «No se ejecuto el arnes». §11.4 lo repite («de ninguna forma»). No hay ficheros de salida de una corrida en la rama.
- La salvedad es la invocación `motor arnes --help` de la fase 0, declarada en el informe y ya señalada por el consultor. No es de esta pasada. No es comprobable por git que el agente no lo ejecutó fuera de los commits.

### Lo que no pude comprobar
- Que la copia de la respuesta del consultor en el encargo sea «tal cual» respecto al mensaje original: no tengo el original. Solo comprobé que encargo e informe coinciden entre sí.
- Que ninguna sesión ejecutara `botsito motor arnes` sin dejar rastro en git: git solo ve commits. Me baso en tests, scripts, mensajes y ausencia de salidas.
- El comportamiento real del comando `motor arnes` con `--simular`: no puedo ejecutarlo. Eso incluye si el motor necesita los diagnósticos A-21, A-35 y A-44 para correr, que es lo que decide si hoy alguna corrida puede dar «sí». El ADR lo atribuye al encargo y dice que no se midió.
- La CI de `main` o de Linux: la rama no toca `.claude/` ni la plataforma.

### Comandos ejecutados
1. `git branch --show-current && git status --short && git log --format='%h %s' main..HEAD && git diff --stat 5e46075 071c30f`
2. `git diff 5e46075 071c30f -- src knowledge tests PROJECT_STATE.md`
3. `tail -40 docs/encargos/trabajo-umbral-mayo.md; cat contrato.yaml`
4. `git log -3 --format='%h%n%B---' 071c30f` y `sed` de `cli.py` 2300-2520
5. `git diff 5e46075 071c30f -- docs/adr docs/validation/UMBRAL-MAYO.md docs/encargos`
6. `sed`/`grep` de `cableado.py`, `motor.py`, `perfil_cuenta.py` y `knowledge/cuentas/ftmo-2step-swing-100k.yaml` (solo lectura)
7. `grep` de `opciones_de_la_corrida` y de los `set_defaults` en `cli.py`
8. `grep` de `habilita_medir|arnes.informe|Simulacion(` en `src` y `scripts`
9. Lectura de `docs/validation/anexos/UMBRAL-MAYO/sin_d2.py` y de su `-SALIDA.txt`
10. `uv run pytest tests/unit/test_umbral_mayo.py -q`
11. `uv run python docs/validation/anexos/UMBRAL-MAYO/sin_d2.py`
12. `uv run ruff check src tests`
13. `uv run ruff format --check src tests`
14. `uv run mypy`
15. `uv run python scripts/contrato_rama.py`
16. `tail make-check.log`, `git rev-parse HEAD^{tree}`, `git diff --name-status 5e46075 071c30f`
17. `uv run botsito state check`
18. `grep` de `motor arnes` en `UMBRAL-MAYO.md`; `grep` de `motor_arnes|main(|subprocess` en tests y anexos; `git log -p -S"motor arnes" main..HEAD -- tests scripts Makefile docs/validation/anexos`
19. Lecturas finales de `criterio_fidelidad.py`, `arnes.py` y `UMBRAL-MAYO.md` (líneas 1-20, 86-96, 388-402, 455-470, 196-222)

No ejecuté `botsito motor arnes` (ni `--help`) ni leí material protegido.

## Estado

**LISTA PARA REVISIÓN, NO cerrada (2026-10-07).** Ni merge, ni tag, ni push. La PARADA de
`--simular` (§8) está resuelta por el consultor (§11). Tercera pasada del revisor: 0 bloquea,
0 importa, 3 menores (dos arreglados, uno declarado; §12).

- ADR-0070, con sus dos enmiendas: mayo solo se mide cuando una corrida del arnés sobre todo
  `construccion`, SIMULADA con el perfil de la cuenta real (`ftmo-2step-swing-100k`) y su primera
  fase (`reto`), y solo con `--salida`, `--tracemalloc`, `--meses`, `--simular`, `--perfil` y
  `--fase`, llega a 0,70 de cobertura y 0,60 de precisión en esa misma corrida. Sin `--simular`,
  «no» («sin simulación»); otro perfil u otra fase, «no»; cualquier otra opción, conocida o futura,
  del subcomando o del parser raíz (como `--repo`), «no».
- Si el motor necesita hoy los diagnósticos de A-21, A-35 y A-44 para correr (lo dice el encargo;
  no se midió), hoy ninguna corrida puede dar «sí».
- **No se ejecutó el arnés** en esta rama (una invocación de `--help` en la fase 0, declarada; la
  tabla de opciones y los valores por defecto se leyeron del código).
