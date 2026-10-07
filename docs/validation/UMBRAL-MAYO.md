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

## Estado

**EN CURSO (2026-10-07).** Fase 0 hecha; siguen las fases 1 a 3.
