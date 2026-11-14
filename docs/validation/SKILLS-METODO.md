# SKILLS-METODO · tres skills al día con ADR-0093 y las lecciones registradas

PLANTILLA: este informe no trae tabla final de preguntas al trader; es una rama de documentos.

Rama `trabajo/skills-metodo` (tramo «Carril: guardias y deuda» de `docs/plan/HOJA-DE-RUTA.md`).
Encargo del consultor del 2026-11-14: `docs/encargos/trabajo-skills-metodo.md`.

Estado: EN CURSO, fase 1 (respuesta del consultor a la PARADA del 2026-11-14).

## Apertura (2026-11-14)

Base comprobada con git y gh antes de abrir, tras `git fetch --prune origin`:

| Comprobación | Salida |
|---|---|
| `git rev-parse --short main` | `73b4e7a9` |
| `git rev-parse main origin/main` | `73b4e7a98cefd62dd820e28f0627ae7499ad5976` las dos veces |
| `git rev-parse "stable/F39b-dieta-estado^{commit}"` = `git rev-parse main^1` | `6054c4cee7fc6e2c735956f3a70944e765e591af` las dos |
| `git ls-remote --tags origin stable/F39b-dieta-estado` | `7d3bd785… refs/tags/stable/F39b-dieta-estado` (tag anotado; su commit, `6054c4ce…`) |
| Último `- Tag: ` de HISTORIA | `stable/F39b-dieta-estado` |
| CI de `main` en `73b4e7a9…` (check-runs, sha literal) | `python completed success`, run 43560175823 |
| `git branch --list` / `git ls-remote --heads origin` | solo `main` en local y en origin |
| `stable/F39c-skills-metodo` | no existe ni en local (`git tag -l`) ni en origin (`git ls-remote --tags`) |
| Tramo | `## Carril: guardias y deuda` en `docs/plan/HOJA-DE-RUTA.md:700`, literal |
| `wc -c PROJECT_STATE.md` en main | 23879 |
| Modelo | Opus 5.5, esfuerzo medio (fijado con `/effort` por Aleks antes del encargo) |

Desviaciones de la apertura, declaradas:

1. La fila de `docs/validation/HOLDOUT-EXPOSICIONES.md` del 2026-11-14 entra en el commit de
   apertura (encargo, punto 0), y `rutas_permitidas` la incluye: la verificación de `abrir-rama`
   («`git diff main --stat` = encargo, contrato, `PROJECT_STATE.md`, `docs/state/HISTORIA.md` y el
   artefacto, nada más») no se cumple al pie de la letra hasta que D3 b) la ajuste.
2. El encargo se escribió con Write en la carpeta de trabajo de la sesión, tal cual, y un guion de
   Python le antepuso `> ` a cada línea al copiarlo a `docs/encargos/trabajo-skills-metodo.md`; no
   pasó por ningún heredoc.

## Decisión del consultor: por qué esta rama va ahora (encargo, punto 1)

Copiada del encargo como decisión del consultor (2026-11-14): RUMBO-2026-11.md §6; esta rama no es
de fidelidad. Desde RUMBO van 4 de fidelidad (F38v a F38y) y, con esta, 5 que no lo son (F38u,
F38z, F39a, F39b y esta). El consultor la acepta porque hasta la grabación de la 7a no hay rama de
fidelidad posible y porque sirve directamente a las dos siguientes (la ingesta de la 7a y su
activación). Tiene que estar cerrada antes de la ingesta; si el domingo 15, con la grabación
hecha, no está para cerrar, PARADA y decide el consultor.

## Fase 0 (2026-11-14): inventario, sin tocar las skills

Leído todo en el árbol de la rama, que en esos ficheros es el de `main` (`73b4e7a9`). El
contraste del encargo con el repo lo hizo además el agente `auditor-encargo` (sección siguiente).

### a. Dónde entra cada cambio, y el texto que propongo

| Decisión | Skill y sitio de hoy | Qué entra |
|---|---|---|
| D1 d | `activar-sesion/SKILL.md:12-14` (precedentes) | una frase nueva tras :14: ACTIVAR-SESION-06-MOTOR.md, la última activación cerrada, anterior a ADR-0093 |
| D1 b | `activar-sesion/SKILL.md:44-48` (viñeta «El arnes») | se sustituye (la única sustitución que el encargo admite en activar-sesion) |
| D1 a | `activar-sesion/SKILL.md:49`, entre «Limites» y «El recorrido» | sección nueva «El metodo de ADR-0093 §4», con las palabras del ADR entre comillas |
| D1 c | `activar-sesion/SKILL.md:80-81`, tras el punto de `spec_version` del paso 3 | un punto nuevo: regenerar `Generado.mqh` en el mismo commit |
| D2 a | `ingerir-sesion/SKILL.md:39-40`, tras el último punto de «Limites» | un punto nuevo: el trailer `Fuente:` de `tramos_no_citables.yaml` |
| D2 b | `ingerir-sesion/SKILL.md:29`, tras el punto de ADR-0038 | un punto nuevo: ningún fotograma antes de situar el tramo; lecciones 3, 5, 6 y 7 de la fila de `trabajo/video-julio` |
| D2 c | `ingerir-sesion/SKILL.md:46`, tras el párrafo de «Herramientas», sin tocarlo | un párrafo nuevo: `frames show` primero, Read solo de la ruta que imprime. **PARADA: ver abajo y la decisión 0** |
| D2 d | `ingerir-sesion/SKILL.md:123`, sin tocarla | una línea de continuación debajo: el log, fuera del repo |
| D3 a | `abrir-rama/SKILL.md:78-79`, tras «la fase 0 la escribe fase-cero en su commit» | una frase: la línea de PLANTILLA en los primeros 600 caracteres |
| D3 b | `abrir-rama/SKILL.md:91-95` (paso 7) y `:111-112` (verificación) | una frase en el paso 7; la viñeta de la verificación se ajusta |

Los textos, tal como entren, irán en el diff de cada skill (sección «Fase 1», tras la respuesta a la
PARADA). La forma de D2 d:
**el log a la carpeta de trabajo de la sesión, fuera del repo**. Ninguna skill ni runbook lo escribe
hoy fuera: `docs/runbooks/CONTRATO-DE-RAMA.md:100`, `docs/runbooks/ENTRADA-MARZO.md:103`, `:205` y
`:290` lo escriben en la raíz y `ENTRADA-MARZO.md:106` y `:292` lo borran después. La forma sale de
la lección 11 de la fila de `trabajo/preparacion-sesion-7` («la salida de una herramienta va a la
carpeta de trabajo, nunca a la raíz del repo», ERRORES-RECURRENTES.md:118). Como D4 solo deja
añadir, la línea de :123 se queda y la nueva, debajo, dice dónde va el fichero. Los dos runbooks no
se tocan (D5): van a la lista para el consultor.

### b. Las fuentes, leídas

| Fuente | Dónde | Lo que dice (lo que se usa) |
|---|---|---|
| ADR-0093 §4 | `docs/adr/0093-el-metodo-de-las-sesiones-y-de-las-activaciones.md:90-107` | test que rompe en `main`; declarar ANTES las filas; julio en la rama con su delta frente a la línea base; si no casa, PARADA; el delta, diagnóstico, nunca ajusta un parámetro ni elige entre dos lecturas; la única lectura que decide es la del pivote |
| ADR-0093 §6, línea base | mismo fichero, `:124-130` | RECORRIDA-CONSTRUCCION-2.md §1.1 y §4; parejas de julio 14, operaciones de más de julio 39; no es la columna del Marcador |
| ADR-0093 §6, qué se mide | `:121-123` | «la primera corrida de ADR-0070 §3 [...] después de activar la 7b» |
| `docs/plan/PIVOTES-SESION-7.yaml` | `:14-27` (`linea_base`) | las mismas cifras, fijadas por sha256 en `tests/unit/test_pivotes_sesion_7.py` |
| ADR-0093 §2, punto 5 | `:53-57` | «en la ingesta, ningún fotograma se abre antes de que la voz o un fotograma ya abierto sitúen el tramo en el día de construcción» (lo dice para el caso de otro backtest en pantalla) |
| ADR-0092 §6 | citado por ADR-0093 §4 (`:99`, `:103`) y §6 (`:158`) | el delta, diagnóstico |
| ADR-0070, «Decision», punto 3 | `docs/adr/0070-umbral-de-construccion-para-medir-mayo.md:54-60` | la lista cerrada de opciones de la corrida que cuenta |
| La corrida que cuenta, hoy | PROJECT_STATE.md:28 (Next Action F, «(3) la corrida de ADR-0070 §3 y la lectura del pivote (ADR-0093 §6)»); `docs/plan/HOJA-DE-RUTA.md:384-390` (R4.3: «el pivote leído en la re-corrida siguiente»); `:486` (R5.7: «NA:F, paso 3») | ver «Lo que no cuadra al pie de la letra», 1 |
| R3.1 | `docs/plan/HOJA-DE-RUTA.md:159` | HECHA: ya no es la corrida que cuenta (después vino R3.9, HECHA, `:299-315`) |
| Regenerar la capa | `docs/runbooks/RENOVAR-CIERRES.md:56-65` («Cómo se comprueba»); `docs/validation/CAPA-GENERADA.md:511-512` («regenera en el mismo commit (D3)»); `src/botsito/mql5bridge/generar_capa.py:54` (`GENERADO`) y `:59` (`ENTRAN`) | la orden, `uv run python src/botsito/mql5bridge/generar_capa.py --repo . --perfil ftmo-2step-swing-100k`; `tests/unit/test_capa_generada.py` falla si el fichero no es lo que da el generador |
| ACTIVAR-SESION-06-MOTOR.md | `docs/validation/ACTIVAR-SESION-06-MOTOR.md:1-4` | abierta el 2026-11-05; cerrada el 2026-11-06 (`stable/F38o-activar-sesion-06-motor`); ADR-0093 es del 2026-11-11 (`0093-...md:232`) |
| Trailer `Fuente:` de los tramos | `tests/contract/test_tramos_fuente.py:72-85` (`test_repositorio_real`, con `ids_de_fuente`: los ids tienen que existir); `src/botsito/comun/historial.py:288-304` | |
| SESION-06-EXTRACCION.md §7 | `docs/validation/SESION-06-EXTRACCION.md:834-861` | **punto 3**: el commit sin `Fuente:`, verde en su propio `make check` y cazado por el siguiente; **punto 1**: el primer `make check` en rojo por la línea de PLANTILLA |
| Fila de `trabajo/video-julio` | `docs/runbooks/ERRORES-RECURRENTES.md:115` | del consultor (6): «un fotograma de un backtest solo se abre después de que la voz o un fotograma ya abierto sitúen ese tramo en el mes permitido, y nunca en el arranque de una grabación»; (7): «la voz que lee cifras del mes marca el tramo, y desde ahí no se abre ningún fotograma hasta que la voz vuelva a un día concreto»; de la sesión (3): antes de abrir un fotograma localizado por un segmento, se lee si el segmento o sus vecinos leen cifras; (5): «el primer fotograma de cada vídeo, al empezar, es el de más riesgo» |
| VIDEO-JULIO.md §11.1 | `docs/validation/VIDEO-JULIO.md:986-1001` (punto c) | la guardia niega `frames show` en el tramo; no niega el Read del PNG por su ruta |
| `frames show` | `src/botsito/cli.py:3193-3200` (opciones `--video`, `--t`, `--n`) y `:560-566` (imprime el id, la ruta y el segmento filtrado) | la regla de D2 c se cumple con la CLI tal como es |
| Fila de `trabajo/preparacion-sesion-7` | `docs/runbooks/ERRORES-RECURRENTES.md:118` | de la sesión: «el log de `knowledge validate` en la raíz dejó el primer `make check` en verde y sin sello»; lección 11 |
| Fila de `trabajo/guardia-falsos-positivos` | `docs/runbooks/ERRORES-RECURRENTES.md:121` | lección 3: «la fila de HOLDOUT-EXPOSICIONES del día se escribe antes del primer `make check` del día, no después» |
| PLANTILLA | `tests/unit/test_hoja_de_ruta.py:96-103` (`[:600]`) y `:245` (solo `SESION-*-EXTRACCION.md`) | |
| `tests/unit/test_skills.py` | `:21` (`PREFIJOS`), `:22` (`PLANTILLA`: `<`, `>`, `{`, `*`, `0N`, `NN`), `:57-65` | el primer término de cada código entre comillas invertidas que empiece por un prefijo, sin `:línea` ni puntuación final |

### c. Herencias

Buscado «skill», «ingerir-sesion», «activar-sesion», «abrir-rama», «fotograma», «Generado.mqh» y
«knowledge-validate» en PROJECT_STATE (Technical Debt y Next Action), en HISTORIA desde el registro
de F38u (`docs/state/HISTORIA.md:16300` en adelante) y en las filas de F38u a F39b de
ERRORES-RECURRENTES (`:115-122`):

- PROJECT_STATE.md:83 (activar-sesion y `Generado.mqh`) y :142 (ingerir-sesion y abrir-rama): las
  dos que paga esta rama.
- PROJECT_STATE.md:112 (un fotograma dentro de un tramo no citable se puede abrir): se queda; D2 c
  la nombra y no la paga (encargo).
- PROJECT_STATE.md:150 (dos textos que ADR-0093 deja viejos: `scripts/graficos_sesion.py:66-71` y
  `engine/decisiones.py:7-8`): código; no entra (D5).
- HISTORIA:17233-17234 (cierre de `trabajo/preparacion-sesion-7`: la línea de `ingerir-sesion`
  ampliada con ADR-0093 §2): es la de :142, ya contada.
- Las filas de F38u a F39b no piden nada más de estas tres skills. Lo que piden de otros ficheros,
  a la lista para el consultor.

### Lo que no cuadra al pie de la letra (y por qué no es PARADA)

1. **«la de R4.3, paso (3)»** (D1 b): R4.3 (`HOJA-DE-RUTA.md:384-390`) no tiene pasos numerados; el
   paso (3) es el de la Next Action F (PROJECT_STATE.md:28), que R4.3 lleva en sus Refs (`NA:F`) y
   R5.7 cita como «NA:F, paso 3» (`HOJA-DE-RUTA.md:486`). Es la misma corrida que ADR-0093 §6 («Qué
   se mide», `:121-123`). La decisión no cambia: la skill la nombra por R4.3 y por ADR-0093 §6, que
   no caducan con la letra de la Next Action, y dice que es su paso (3).
2. **«SESION-06-EXTRACCION.md §7, punto 1»** para el trailer (D2 a): el del trailer es el punto 3
   (`:846-856`); el punto 1 es el de la PLANTILLA (`:837-841`), que es el que cita D3 a por su
   lado. La skill cita el punto 3.
3. **ADR-0093 §2, punto 5** dice la regla de los fotogramas para el caso de otro backtest o material
   reservado en pantalla; la generaliza a toda ingesta la lección 6 del consultor de la fila de
   `trabajo/video-julio` (para cualquier fotograma de un backtest), como dice D2 b. La skill cita las
   dos.
4. **La sección de CAPA-GENERADA.md que dice «D3»** para regenerar es la fase 2
   (`CAPA-GENERADA.md:511-512`); la regla escrita entera está en `RENOVAR-CIERRES.md:56-65`, que la
   extiende al perfil y nombra su guardia, `tests/unit/test_capa_generada.py`. La skill cita las
   dos y la guardia.
5. **«nunca elige entre dos lecturas»** (D1 a) lo dice ADR-0093 §4 (`:102`), no ADR-0092 §6
   (`docs/adr/0092-...md:160-178`, que dice que las métricas sobre construcción son diagnóstico y
   ningún parámetro se ajusta por ellas). La skill atribuye cada frase a su ADR.

### Lo que sí no cuadra: D2 c, imposible en la ingesta de la 7a → PARADA

D2 c manda abrir un fotograma con `corpus frames show` primero y después Read solo de la ruta que
imprime. **Para un vídeo de sesión en cuarentena la guardia niega `frames show` siempre**:
`_analizar_cli` (`.claude/hooks/guardia.py:2526-2537`) bloquea `corpus frames show --video <v>`
si `<v>` está en `sesiones_en_cuarentena` (`:425-438`: los vídeos de `fuentes.yaml` con
`drive_id: null`, menos v6), con el mensaje «imprime la transcripcion cruda. [...] Como
reescribirlo: localiza el instante en la version filtrada y abre el PNG por su ruta
(`data/fotogramas/<v>/png-1fps/<ms>.png`)». La 7a entra así: el paso 1 de `ingerir-sesion` la
registra con `drive_id: null` y la añade a la cuarentena. Y la negación «dentro de un tramo no
citable» (`_tramos_en_la_cli`, `:2613-2622`) solo vale para los vídeos con tramos VIGILADOS, los
que no están en cuarentena (`tramos_vigilados`, `:462-465`; hoy v6 y v13,
`tests/unit/test_guardia_claude.py:684-697`), y solo mira el instante de `--t`.

Escrita como dice D2 c, la skill dejaría la ingesta de la 7a sin ninguna forma permitida de abrir
un fotograma. Es un hecho que contradice una decisión: PARADA (encargo, punto 2). Lo hallaron el
`auditor-encargo` y la sesión lo midió en el código de la guardia (sin ejecutarla sobre ningún
vídeo).

### Herencias que salen de lecciones registradas y el encargo no nombra

- **Lección 8 de la fila de `trabajo/video-julio`** (ERRORES-RECURRENTES.md:115): «un tramo no
  citable nuevo de un vídeo que no está en cuarentena cambia lo que espera
  `test_guardia_claude.py::test_los_tramos_del_repo_real`: se amplía el contrato a ese test en el
  mismo commit, o `make check` sale en rojo». Toca los pasos 2 y 4 de `ingerir-sesion`; a la 7a no
  le afecta (en cuarentena). Por la regla del punto 3 c entraría: decisión 2.
- **Lección de la fila de `trabajo/dieta-estado`** (ERRORES-RECURRENTES.md:122, 4.ª columna):
  «Antes de un make check, uv run botsito knowledge validate sobre el informe» (los ids
  inexistentes). Entraría en el paso 6 de `abrir-rama`: decisión 2.

### Para el consultor (no entra: otros ficheros, D5)

- `docs/runbooks/CONTRATO-DE-RAMA.md:100` y `docs/runbooks/ENTRADA-MARZO.md:103`, `:205` y `:290`
  escriben el log de `knowledge validate` en la raíz (la trampa de la fila de
  `trabajo/preparacion-sesion-7`).
- Cómo se corre julio en una activación (comando, opciones y cálculo del delta de ADR-0093 §4) no
  está escrito en ningún sitio (grep de «corre julio» y «delta de julio»: solo ADR-0093, RUMBO,
  `PREPARACION-SESION-7.md:277` y `:443` y los encargos, sin comando): lo tiene que fijar el
  encargo de la activación de la 7a.
- PROJECT_STATE.md:150 (`scripts/graficos_sesion.py:66-71` y `engine/decisiones.py:7-8`): código.
- La activación de la 7a genera las láminas de la 7b, revisa PREGUNTAS-7B.md y pasa
  `SESION_EN_CURSO` a "08" (PROJECT_STATE.md:28): es de su encargo, no de la skill.
- PROJECT_STATE.md:28 dice «C y R6a en los huecos»: esta rama ocupa ese hueco sin entrada `###` en
  su tramo (el encargo da el motivo, punto 1).

## El encargo frente al repo (auditor-encargo, 2026-11-14)

44 afirmaciones: 33 cuadran, 8 con matiz y 3 no cuadran. Las tres: «R4.3, paso (3)» (D1 b; arriba,
1), «SESION-06-EXTRACCION.md §7, punto 1» (D2 a; arriba, 2) y D2 c para un vídeo en cuarentena
(arriba, PARADA). Matices que cambian lo que se escribe: ADR-0093 §2, punto 5, se escribe para un
caso y lo generaliza la lección 6 (arriba, 3); «nunca elige entre dos lecturas» es de ADR-0093, no
de ADR-0092 (arriba, 5); la regla de regenerar cubre también el perfil y tiene guardia (arriba, 4);
la línea base de §6 es la del pivote, y usarla para el delta de una activación es la lectura que el
encargo pide; la PLANTILLA fuera de las extracciones no sale de un ADR ni de una lección (decisión
1); ninguna skill ni runbook escribe el log de `knowledge validate` fuera del repo (arriba, D2 d);
la verificación de `abrir-rama` no es el único sitio que enumera los ficheros (también el paso 4,
el paso 7 y «Artefacto»). No comprobó la red (el tag F39c en origin y la CI): los comprobó la
sesión en la apertura.

## Lo que necesito que decidas

0. **D2 c, cómo se abre un fotograma.** Opciones: (a) la regla por casos: en un vídeo con tramos
   vigilados (fuera de cuarentena), primero `uv run botsito corpus frames show --video <v> --t <h:mm:ss>`,
   que la guardia niega dentro de un tramo no citable, y después Read solo de la ruta que imprime;
   en un vídeo de sesión en cuarentena (la 7a), donde la guardia niega `frames show` siempre, Read
   del PNG por su ruta `data/fotogramas/<v>/png-1fps/<ms>.png`, solo para un instante localizado en
   la filtrada (ADR-0038; mensaje de la guardia, `guardia.py:2531-2537`); en los dos, después de la
   regla de D2 b; (b) D2 c fuera, y queda solo D2 b. Recomiendo (a): es lo que la guardia deja hacer
   y lo único con lo que se abre un fotograma de la 7a, y cita la línea de Technical Debt de :112,
   que no se paga. Coste de (b): la skill no dice cómo se abre un fotograma, que es lo que pedía.
1. **D3 a, la palabra «convención».** Opciones: (a) «`test_hoja_de_ruta.py` lo comprueba solo en los
   `SESION-*-EXTRACCION.md`; en los demás informes es la convención que piden sus encargos
   (DIETA-ESTADO.md, ACTIVAR-SESION-06.md y SKILLS-METODO.md)»; (b) «en los demás informes es la
   convención», tal cual. Recomiendo (a): dice de dónde sale, y D4 no admite una regla sin ADR ni
   lección. Coste de (b): ninguno práctico; solo que la frase no tiene fuente.
2. **Las dos herencias de lecciones** (lección 8 de `trabajo/video-julio` en `ingerir-sesion`, pasos
   2 y 4; la de `trabajo/dieta-estado` en `abrir-rama`, paso 6). Opciones: (a) entran, como manda el
   punto 3 c; (b) a la lista para el consultor. Recomiendo (a): salen de lecciones registradas y las
   dos han costado un `make check` en rojo. Coste de (b): la siguiente ingesta o apertura depende de
   que su encargo lo recuerde.

Lo demás de D1-D6 cuadra con lo medido (las citas, corregidas como arriba). Si la respuesta es
(a), (a) y (a), la fase 1 entra en tres commits como pide el punto 4.

`make check` del commit de apertura (`c227edc9`): exit 0, 3513 passed, 6 xfailed, ningún `failed`,
SELLO sobre el árbol `ab82b181`. `PICO DE MEMORIA de make check: 317 MiB en test`.

## Respuesta del consultor a la PARADA (2026-11-14)

Copiada tal cual (también al final del encargo):

> Respuesta del consultor a la PARADA de la fase 0 de trabajo/skills-metodo (2026-11-14). Cópiala tal cual en el informe, en su sección, y aplícala.
>
> 0. D2 c: opción (a), por casos. En un vídeo fuera de cuarentena, primero uv run botsito corpus frames show (la guardia lo niega dentro de un tramo no citable) y después Read solo de la ruta que imprime. En un vídeo de sesión en cuarentena, la guardia niega frames show siempre (.claude/hooks/guardia.py, _analizar_cli, hacia :2526-2537) y su mensaje manda abrir el PNG por su ruta: Read de data/fotogramas/<v>/png-1fps/<ms>.png, solo para un instante localizado antes en la filtrada y nunca dentro de un tramo de tramos_no_citables.yaml (la guardia aún no niega ese Read: VIDEO-JULIO.md §11.1 y su línea de Technical Debt, que esta rama no paga). En los dos casos, después de la regla de D2 b. La versión del encargo era un error del consultor: no se podía cumplir para ningún vídeo en cuarentena.
> 1. D3 a: opción (a). «Es la convención que piden sus encargos», con DIETA-ESTADO, ACTIVAR-SESION-06 y esta rama como fuente.
> 2. Las dos herencias: opción (a), entran las dos, cada una con su cita. La lección 8 de la fila de trabajo/video-julio (un tramo nuevo de un vídeo fuera de cuarentena amplía test_los_tramos_del_repo_real en el mismo commit) va en ingerir-sesion. La de trabajo/dieta-estado (knowledge validate antes de cada make check) va en el paso 6 de abrir-rama, escrita con la forma de log que D2 d deje fuera de la raíz.
> 3. Las correcciones de cita de la fase 0 se aceptan: R4.3 sin «paso (3)», que es de la Next Action F, citando R4.3 y ADR-0093 §6 «Qué se mide»; el trailer Fuente: en SESION-06-EXTRACCION §7, punto 3; «nunca elige entre dos lecturas», de ADR-0093 §4; y la regla de regenerar la capa, citando también RENOVAR-CIERRES.md, con su perfil y su test, sin ampliar la skill más allá de lo que esa fuente dice.
> 4. Mi lista queda anotada, sin tocar nada de ella en esta rama: el log de knowledge validate en la raíz que escriben CONTRATO-DE-RAMA.md y ENTRADA-MARZO.md, y que el comando de la corrida de julio lo fija el encargo de la activación de la 7a.
> 5. Sigue con la fase 1 (un commit por skill, sellados), el revisor con su alcance y «Rama lista para revisión, NO cerrada». En la fila de ERRORES-RECURRENTES deja la 3.ª columna para mí.

## Fase 1 (2026-11-14): las tres skills, un commit por skill

### 1. `activar-sesion` (D1 a-d; respuesta a la PARADA, punto 3)

- D1 d: los precedentes ganan una frase con `ACTIVAR-SESION-06-MOTOR.md`, anterior a ADR-0093.
- D1 b: la viñeta «El arnes» se sustituye (la única sustitución de la skill). La corrida que
  cuenta, por R4.3 («Hecho cuando») y ADR-0093 §6, «Qué se mide», sin el «paso (3)» de la Next
  Action F (punto 3 de la respuesta).
- D1 a: la sección «El metodo de ADR-0093 §4», con las palabras del ADR entre comillas; «nunca
  elige entre dos lecturas» atribuido a ADR-0093 §4; la línea base, la de §6 y
  `PIVOTES-SESION-7.yaml`, sin copiar sus cifras; el comando de julio, del encargo de cada
  activación.
- D1 c: un punto en el paso 3, con la orden y el alcance de RENOVAR-CIERRES.md («`parametros.yaml`,
  el perfil») y su test, sin más (punto 3 de la respuesta).
- Paga la línea de Technical Debt de PROJECT_STATE.md:83 entera: sale, literal, al final de
  HISTORIA en «# Technical Debt PAGADA · sale de PROJECT_STATE.md en trabajo/skills-metodo
  (2026-11-14)», con su evidencia (`activar-sesion/SKILL.md:106-111`).

El diff (antes y después):

```diff
diff --git a/.claude/skills/activar-sesion/SKILL.md b/.claude/skills/activar-sesion/SKILL.md
index 99b69d67..4e752780 100644
--- a/.claude/skills/activar-sesion/SKILL.md
+++ b/.claude/skills/activar-sesion/SKILL.md
@@ -14,2 +14,4 @@ precedentes: `docs/validation/ACTIVAR-SESION-03.md`, `docs/validation/ACTIVACION
 `docs/runbooks/ACTIVAR-A35-A44.md`. Si esta skill y ellos discrepan, ganan ellos y se dice.
+La ultima activacion cerrada es `docs/validation/ACTIVAR-SESION-06-MOTOR.md`
+(`stable/F38o-activar-sesion-06-motor`, 2026-11-06), anterior a ADR-0093 (2026-11-11).
 
@@ -43,7 +45,29 @@ precedentes: `docs/validation/ACTIVAR-SESION-03.md`, `docs/validation/ACTIVACION
   test con el codigo de main») y pase despues.
-- **El arnes** (`uv run botsito motor arnes`) solo si el encargo o la respuesta a la PARADA lo
-  autorizan expresamente (`ACTIVAR-A35-A44.md` lo pedia tras activar; los encargos recientes lo
-  prohiben salvo autorizacion). La corrida que cuenta es la de la entrada R3.1 de
-  `docs/plan/HOJA-DE-RUTA.md`, con las opciones de ADR-0070 («Decision», punto 3). En la duda,
-  PARADA.
+- **El arnes** (`uv run botsito motor arnes`). La corrida de julio de 2026 de ADR-0093 §4 forma
+  parte de toda activacion y es diagnostico (seccion siguiente). Cualquier otra corrida del arnes,
+  solo si el encargo o la respuesta a la PARADA la autorizan expresamente (`ACTIVAR-A35-A44.md` lo
+  pedia tras activar; los encargos recientes lo prohiben salvo autorizacion). La corrida que cuenta
+  ya no es la de R3.1: es la de R4.3 de `docs/plan/HOJA-DE-RUTA.md` («el pivote leído en la
+  re-corrida siguiente»), «la primera corrida de ADR-0070 §3 [...] después de activar la 7b»
+  (ADR-0093 §6, «Qué se mide»), con las opciones de ADR-0070 («Decision», punto 3) y la lectura del
+  pivote de ADR-0093 §6. En la duda, PARADA.
+
+## El metodo de ADR-0093 §4
+
+Desde ADR-0093 (2026-11-11), con sus palabras:
+
+- «Cada respuesta se escribe primero como test sobre casos de construcción que rompe en `main`».
+- «Cada activación declara ANTES qué filas de la clasificación vigente debería convertir en
+  pareja», y corre julio de 2026 en la rama, «con su delta de parejas y de operaciones de más frente
+  a la línea base».
+- La linea base: §4 no la define. Es la de ADR-0093 §6 («Línea base»), con sus cifras en
+  `docs/plan/PIVOTES-SESION-7.yaml` (`linea_base`): esa lectura, y no otra.
+- «Si el delta de julio de una activación no casa con lo que declaró, la regla no se retoca hasta
+  que la cifra salga: PARADA» (ADR-0093 §4).
+- El delta es diagnostico: «La cifra dice si la respuesta se entendió, nunca ajusta un parámetro»
+  (ADR-0093 §4, que cita ADR-0092 §6) y «El delta nunca elige entre dos lecturas de un parámetro»
+  (ADR-0093 §4).
+- Como se corre julio en una activacion (el comando, sus opciones y como se calcula el delta) no
+  esta escrito en ningun sitio (`docs/validation/SKILLS-METODO.md`, fase 0): lo fija y lo cita el
+  encargo de cada activacion.
 
@@ -81,2 +105,8 @@ precedentes: `docs/validation/ACTIVAR-SESION-03.md`, `docs/validation/ACTIVACION
      `uv run botsito spec docs --escribir`, en el mismo commit;
+   - si toca un parametro que entra en la capa de MT5 (`ENTRAN` de
+     `src/botsito/mql5bridge/generar_capa.py`; `parametros.yaml` o el perfil), se regenera
+     `mql5/Include/Botsito/Capa/Generado.mqh` en el mismo commit:
+     `uv run python src/botsito/mql5bridge/generar_capa.py --repo . --perfil ftmo-2step-swing-100k`
+     (`docs/runbooks/RENOVAR-CIERRES.md`, «Cómo se comprueba»; `docs/validation/CAPA-GENERADA.md`,
+     fase 2, D3); `tests/unit/test_capa_generada.py` falla si el fichero no es lo que da el generador;
    - si la regla gana un sitio con `cita`: las tres guardias de `src/botsito/spec/modelo.py`;
```

`make check` del commit 1 (`a8acd219`): exit 0, 3513 passed, 6 xfailed, ningún `failed`, SELLO
sobre el árbol `0433f5fa`. `PICO DE MEMORIA de make check: 318 MiB en test`.

### 2. `ingerir-sesion` (D2 a-d; respuesta a la PARADA, puntos 0, 2 y 3)

- D2 b (`:30-38`): la regla de los fotogramas, por ADR-0093 §2, punto 5, y las lecciones 3, 5, 6 y
  7 de la fila de `trabajo/video-julio`; la 6 es la que la lleva a toda ingesta (fase 0, «Lo que no
  cuadra al pie de la letra», 3).
- D2 a (`:50-53`): el trailer `Fuente:` de `tramos_no_citables.yaml`, con
  `tests/contract/test_tramos_fuente.py` y SESION-06-EXTRACCION.md §7, punto 3 (punto 3 de la
  respuesta).
- Herencia (`:54-57`; respuesta, punto 2): la lección 8 de la fila de `trabajo/video-julio`, con su
  frase entre comillas.
- D2 c (`:65-74`), por casos (respuesta, punto 0): fuera de cuarentena, `frames show` y Read de la
  ruta que imprime; en cuarentena, Read del PNG por su ruta, solo para un instante localizado antes
  en la filtrada y nunca dentro de un tramo no citable. La línea de «Herramientas» (`:61-63`, antes `:44-46`) no se
  toca, y la línea de Technical Debt de PROJECT_STATE.md:111 (antes :112) se queda.
- D2 d (`:152-155`): el log de `knowledge validate`, fuera del repo; la línea de `:151` (antes `:123`) se queda,
  porque D4 solo deja añadir.

Paga dos de las tres partes de la línea de Technical Debt de PROJECT_STATE.md:141 (antes :142), el
trailer `Fuente:` y los fotogramas; la tercera, la PLANTILLA, es de `abrir-rama`, así que la línea
se queda hasta el commit siguiente (D6).

El diff (antes y después):

```diff
diff --git a/.claude/skills/ingerir-sesion/SKILL.md b/.claude/skills/ingerir-sesion/SKILL.md
index 3dd354b5..c57ebe19 100644
--- a/.claude/skills/ingerir-sesion/SKILL.md
+++ b/.claude/skills/ingerir-sesion/SKILL.md
@@ -29,2 +29,11 @@ reglas viven en `CLAUDE.md`, `docs/runbooks/SESION-DE-PREGUNTAS.md` («Después
   Analytics ni el tramo sin audio; de 25 en 25 como mucho, anotando cada lote antes del siguiente.
+- **Ningun fotograma se abre antes de que la voz o un fotograma ya abierto situen el tramo en un
+  dia de construccion**, en toda ingesta. ADR-0093 §2, punto 5, lo escribe para la sesion en que
+  aparece en pantalla otro backtest, Analytics o material de un mes reservado; la leccion 6 de la
+  fila de `trabajo/video-julio` en `docs/runbooks/ERRORES-RECURRENTES.md` lo dice de cualquier
+  fotograma de un backtest, «y nunca en el arranque de una grabación»: el primer fotograma de cada
+  video, al empezar, es el de mas riesgo (misma fila, leccion 5). La voz que lee cifras del mes
+  marca el tramo, y desde ahi no se abre ningun fotograma hasta que la voz vuelva a un dia concreto
+  (leccion 7); antes de abrir un fotograma localizado por un segmento, se lee si el segmento o sus
+  vecinos leen cifras (leccion 3).
 - `kb find`, `kb at`, `corpus transcript show`, `corpus frames show` y `evidence propose` ensenan
@@ -40,2 +49,10 @@ reglas viven en `CLAUDE.md`, `docs/runbooks/SESION-DE-PREGUNTAS.md` («Después
   fotogramas tampoco (rompen la huella del sello).
+- **Todo commit que toque `knowledge/corpus/tramos_no_citables.yaml` lleva en el cuerpo su trailer
+  `Fuente:`**, con ids que existan: lo exige `tests/contract/test_tramos_fuente.py`, que mira los
+  commits, asi que el `make check` de ese mismo commit sale verde y lo caza el siguiente
+  (`docs/validation/SESION-06-EXTRACCION.md` §7, punto 3: el commit se tuvo que rehacer).
+- **Un tramo no citable nuevo de un video que no esta en cuarentena** cambia lo que espera
+  `tests/unit/test_guardia_claude.py` (`test_los_tramos_del_repo_real`): «se amplía el contrato a
+  ese test en el mismo commit, o `make check` sale en rojo» (leccion 8 de la fila de
+  `trabajo/video-julio` en `docs/runbooks/ERRORES-RECURRENTES.md`).
 
@@ -47,2 +64,13 @@ Read de la filtrada y de fotogramas localizados, Write/Edit para `fuentes.yaml`,
 
+Un fotograma se abre segun el video, y siempre despues de la regla de los fotogramas de «Limites»
+(respuesta del consultor a la PARADA de `trabajo/skills-metodo`, punto 0, en
+`docs/validation/SKILLS-METODO.md`):
+- **video fuera de cuarentena**: primero `uv run botsito corpus frames show --video <vN> --t <h:mm:ss>`,
+  que la guardia niega dentro de un tramo no citable, y despues Read solo de la ruta que imprime;
+- **video de sesion en cuarentena**: la guardia niega `frames show` siempre (`_analizar_cli`,
+  `.claude/hooks/guardia.py`) y su mensaje manda abrir el PNG por su ruta: Read de
+  `data/fotogramas/<v>/png-1fps/<ms>.png`, solo para un instante localizado antes en la filtrada y
+  nunca dentro de un tramo de `tramos_no_citables.yaml`. La guardia aun no niega ese Read
+  (`docs/validation/VIDEO-JULIO.md` §11.1; su linea de Technical Debt sigue abierta).
+
 ## El recorrido
@@ -123,2 +151,6 @@ items de evidencia nuevos.
 - `uv run botsito knowledge validate > knowledge-validate.log 2>&1` en verde (ids, tramos, citas).
+  El log, en la carpeta de trabajo de la sesion, fuera del repo, nunca en la raiz: alli es un
+  fichero sin seguir y `make check` sale en verde y sin sello (`CLAUDE.md`, «main no se toca»; fila
+  de `trabajo/preparacion-sesion-7` en `docs/runbooks/ERRORES-RECURRENTES.md`, «De la sesion» y
+  leccion 11).
 - `git diff --name-status main...HEAD -- knowledge/evidence knowledge/corpus/transcripciones
```
