# SKILLS-METODO · tres skills al día con ADR-0093 y las lecciones registradas

PLANTILLA: este informe no trae tabla final de preguntas al trader; es una rama de documentos.

Rama `trabajo/skills-metodo` (tramo «Carril: guardias y deuda» de `docs/plan/HOJA-DE-RUTA.md`).
Encargo del consultor del 2026-11-14: `docs/encargos/trabajo-skills-metodo.md`.

Estado: Rama lista para revisión, NO cerrada (al final).

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
- PROJECT_STATE.md:150 (dos textos que ADR-0093 deja viejos; la línea está ACORTADA, y los dos,
  `scripts/graficos_sesion.py:66-71` y `engine/decisiones.py:7-8`, los nombra su texto entero en
  `docs/state/HISTORIA.md:17417`): código; no entra (D5).
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
- PROJECT_STATE.md:150 (línea ACORTADA; los dos ficheros, en su texto entero de HISTORIA:17417):
  código.
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

`make check` del commit de la fase 0 (`86b28167`): exit 0, 3513 passed, 6 xfailed, ningún
`failed`, SELLO sobre el árbol `9c0b9adb`. `PICO DE MEMORIA de make check: 318 MiB en test`
(añadido tras el revisor, B1).

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

`make check` del commit 2 (`c7920376`): exit 0, 3513 passed, 6 xfailed, ningún `failed`, SELLO
sobre el árbol `8a8dffb4`. `PICO DE MEMORIA de make check: 319 MiB en test`.

### 3. `abrir-rama` (D3 a-b; respuesta a la PARADA, puntos 1 y 2)

- D3 a (`:74-79`): la línea de PLANTILLA en los primeros 600 caracteres; `test_hoja_de_ruta.py` lo
  comprueba solo en los `SESION-*-EXTRACCION.md`; en los demás informes, «la convención que piden
  sus encargos», con DIETA-ESTADO, ACTIVAR-SESION-06 y esta rama como fuente (respuesta, punto 1).
- Herencia (`:89-92`; respuesta, punto 2): la lección de la fila de `trabajo/dieta-estado`,
  `knowledge validate` antes de cada `make check`, con el log fuera del repo, la forma de D2 d.
- D3 b (`:97-101`): la fila de HOLDOUT-EXPOSICIONES del día antes del primer `make check`; si la
  rama lo corre el día de la apertura, entra en el commit de apertura y `rutas_permitidas` la
  incluye. La verificación (`:113-115`) se ajusta: es la única viñeta cambiada de la skill. El paso
  4 (`rutas_permitidas`), la lista del `git add` del paso 7 y «Artefacto» no se tocan (D4: solo se
  añade); la frase nueva del paso 7 los completa.
- Paga la parte de PLANTILLA de la línea de Technical Debt de PROJECT_STATE.md:141, y con ella la
  línea entera (las otras dos partes, en `c7920376`): sale, literal, al mismo bloque de HISTORIA,
  con su evidencia.

El diff (antes y después):

```diff
diff --git a/.claude/skills/abrir-rama/SKILL.md b/.claude/skills/abrir-rama/SKILL.md
index 8ab7127a..894f3326 100644
--- a/.claude/skills/abrir-rama/SKILL.md
+++ b/.claude/skills/abrir-rama/SKILL.md
@@ -73,2 +73,8 @@ para `PROJECT_STATE.md`.
    fase 0 la escribe fase-cero en su commit.
+   Nace tambien con su linea de PLANTILLA en sus primeros 600 caracteres:
+   `tests/unit/test_hoja_de_ruta.py` lo comprueba solo en los `docs/validation/SESION-*-EXTRACCION.md`
+   (sin ella, el primer `make check` de la rama sale en rojo, por segunda vez en
+   `docs/validation/SESION-06-EXTRACCION.md` §7, punto 1); en los demas informes es la convencion
+   que piden sus encargos (`docs/validation/DIETA-ESTADO.md`, `docs/validation/ACTIVAR-SESION-06.md`
+   y `docs/validation/SKILLS-METODO.md`).
 5. **Archivo de PROJECT_STATE** (`docs/state/README.md`, «Como se archiva»):
@@ -82,2 +88,6 @@ para `PROJECT_STATE.md`.
    FINAL de `make check`: mejor verlo antes) y `uv run python scripts/contrato_rama.py`.
+   Y, antes de cada `make check`, `uv run botsito knowledge validate` sin `ERROR`, con su log en la
+   carpeta de trabajo de la sesion, fuera del repo (fila de `trabajo/preparacion-sesion-7` en
+   `docs/runbooks/ERRORES-RECURRENTES.md`, leccion 11): un id inexistente citado en el informe tumba
+   `make check` (fila de `trabajo/dieta-estado`, misma tabla).
 7. **Sello y commit.** `git add` de los ficheros nombrados (encargo, contrato, `PROJECT_STATE.md`,
@@ -86,2 +96,7 @@ para `PROJECT_STATE.md`.
    `chore(rama): abre <rama> (encargo, contrato y Archivo N de PROJECT_STATE)`.
+   La fila de `docs/validation/HOLDOUT-EXPOSICIONES.md` del dia va antes del primer `make check`
+   (leccion 3 de la fila de `trabajo/guardia-falsos-positivos` en
+   `docs/runbooks/ERRORES-RECURRENTES.md`): si la rama corre `make check` el dia de la apertura,
+   entra en este commit, estadiada con los demas, y `rutas_permitidas` la incluye
+   (`trabajo/dieta-estado` y `trabajo/skills-metodo` lo declararon como desviacion).
 
@@ -97,4 +112,5 @@ nuevo al final de `docs/state/HISTORIA.md` y `PROJECT_STATE.md` apuntando a la r
 - `tests/unit/test_historia.py` en verde dentro de `make check` (HISTORIA solo se amplio).
-- `git diff main --stat` = encargo, contrato, `PROJECT_STATE.md`, `docs/state/HISTORIA.md` y el
-  artefacto, nada mas.
+- `git diff main --stat` = encargo, contrato, `PROJECT_STATE.md`, `docs/state/HISTORIA.md`, el
+  artefacto y, si entro en el commit de apertura (paso 7), `docs/validation/HOLDOUT-EXPOSICIONES.md`;
+  nada mas.
 - Las cuatro comprobaciones de la base (paso 1), con su salida, en el informe de la rama.
```

`make check` del commit 3 (`d3d00f9f`): exit 0, 3513 passed, 6 xfailed, ningún `failed`, SELLO
sobre el árbol `1b20d3e2`. `PICO DE MEMORIA de make check: 318 MiB en test` (añadido tras el
revisor, B1).

### PROJECT_STATE.md

`wc -c PROJECT_STATE.md`: **23435** bytes (23879 en `main`): salen las dos líneas de Technical Debt
y cambian `Current Branch`, `Current Feature`, `Completed Features` y `Change Log` (abrir-rama).
Nada más cambia. `tests/unit/test_skills.py`, `test_historia.py`, `test_project_state.py` y
`test_hoja_de_ruta.py` pasan dentro de cada `make check`.

## El encargo, punto por punto

| Punto | Qué pedía | Estado | Dónde |
|---|---|---|---|
| 0 | Base comprobada, `git fetch --prune`, una sola rama, F39c libre | Hecho | «Apertura» |
| 0 | Abrir con `abrir-rama`: encargo con Write, contrato, Archivo en HISTORIA | Hecho (el encargo, Write más un guion que antepone `> `: desviación 2) | `c227edc9`; Archivo 71 |
| 0 | Contrato: tramo literal, riesgo bajo, las tres skills y HOLDOUT en `rutas_permitidas` | Hecho | `contrato.yaml` |
| 0 | Informe con PLANTILLA en sus primeros 600 caracteres | Hecho | línea 3 |
| 0 | Fila de HOLDOUT antes del primer `make check`, en el commit de apertura, declarada como desviación | Hecho | HOLDOUT-EXPOSICIONES.md:148; desviación 1 |
| 0 | `/model`: Opus, esfuerzo medio | Hecho | «Apertura» |
| 1 | La decisión del consultor, en el informe | Hecho | «Decisión del consultor» |
| 2 D1 a | Sección del método de ADR-0093 §4, con sus palabras; la línea base de §6 y PIVOTES; el comando de julio, del encargo | Hecho | `activar-sesion/SKILL.md:55-73` |
| 2 D1 b | La viñeta «El arnés», sustituida | Hecho, con la cita corregida (respuesta, punto 3) | `activar-sesion/SKILL.md:46-53` |
| 2 D1 c | Regenerar `Generado.mqh` en el mismo commit | Hecho, con RENOVAR-CIERRES.md, su perfil y su test | `activar-sesion/SKILL.md:106-111` |
| 2 D1 d | ACTIVAR-SESION-06-MOTOR.md en los precedentes, anterior a ADR-0093 | Hecho | `activar-sesion/SKILL.md:15-16` |
| 2 D2 a | El trailer `Fuente:` de los tramos | Hecho, citando §7, punto 3 | `ingerir-sesion/SKILL.md:50-53` |
| 2 D2 b | Ningún fotograma antes de situar el tramo; las lecciones de video-julio | Hecho (lecciones 3, 5, 6 y 7) | `ingerir-sesion/SKILL.md:30-38` |
| 2 D2 c | Cómo se abre un fotograma | PARADA y hecho por casos (respuesta, punto 0) | `ingerir-sesion/SKILL.md:65-74` |
| 2 D2 d | El log de `knowledge validate` fuera de la raíz | Hecho: carpeta de trabajo, fuera del repo | `ingerir-sesion/SKILL.md:152-155` |
| 2 D3 a | PLANTILLA: test solo en las extracciones; convención en los demás | Hecho (respuesta, punto 1) | `abrir-rama/SKILL.md:74-79` |
| 2 D3 b | HOLDOUT antes del primer `make check`; la verificación ajustada | Hecho | `abrir-rama/SKILL.md:97-101` y `:113-115` |
| 2 D4 | Cada línea con su fuente; rutas que no rompan `test_skills.py`; solo se añade salvo D1 b y la verificación | Hecho; `test_skills.py` en verde | diffs de «Fase 1» |
| 2 D5 | Nada fuera de las tres skills, PS, HISTORIA, el encargo, el informe y HOLDOUT; sin material ni arnés | Hecho | `git diff main --stat` |
| 2 D6 | Las dos líneas de Technical Debt, por (a) PAGADA, literales en HISTORIA, en el commit que paga cada una | Hecho: :83 en `a8acd219`; :142 (entera) en el commit de `abrir-rama` | final de HISTORIA |
| 3 | Fase 0 y PARADA condicional | PARADA por D2 c; respondida | «Fase 0», «Respuesta del consultor a la PARADA» |
| 4 | Un commit por skill, sellado; PICO DE MEMORIA; los cuatro tests; `wc -c` | Hecho | «Fase 1»; «PROJECT_STATE.md» |
| 5 | El informe | Este | — |
| 6 | El revisor con su alcance, su informe pegado; sin CI de Linux | Ver «Informe del revisor» | — |

## Lo que no entró, y por qué

- Los runbooks que escriben el log de `knowledge validate` en la raíz
  (`docs/runbooks/CONTRATO-DE-RAMA.md:100`, `docs/runbooks/ENTRADA-MARZO.md:103`, `:205` y `:290`):
  D5; en la lista del consultor (respuesta, punto 4).
- El comando, las opciones y el cálculo del delta de la corrida de julio de una activación: no
  están escritos en ningún sitio; los fija el encargo de la activación de la 7a (respuesta,
  punto 4).
- La línea de Technical Debt del fotograma dentro de un tramo no citable (PROJECT_STATE.md:111):
  la rama no la paga (encargo, D2 c).
- PROJECT_STATE.md:148 (en `main`, :150), los dos textos que ADR-0093 deja viejos: código (D5).
- Lo que la activación de la 7a tiene que hacer además (las láminas de la 7b, PREGUNTAS-7B.md,
  `SESION_EN_CURSO`): es de su encargo, no de la skill.

## Desviaciones

1. La fila de HOLDOUT-EXPOSICIONES en el commit de apertura, antes de que D3 b ajustara la
   verificación de `abrir-rama` (punto 0 del encargo).
2. El encargo, escrito con Write en la carpeta de trabajo y copiado con un guion que antepone `> `.
3. Las negativas de la guardia, ninguna sobre material: dos comandos compuestos (`uv run python -`
   o un guion detrás de `git add`/`tail`) y dos listados (`find .` y `git ls-files` sin ruta, que
   listarían nombres del holdout). Se partieron en llamadas sueltas o se cambió por rutas literales,
   la forma que propone su mensaje; ninguna era un paso de la skill ni pedía rodear nada.
4. Las citas del encargo corregidas en la fase 0 (R4.3 «paso (3)», SESION-06 §7 punto 3), aceptadas
   por la respuesta, punto 3.

## Para la orden de cierre: la fila de ERRORES-RECURRENTES.md

| Rama | Hallazgos del revisor | Lo que vio el consultor después | Lecciones |
|---|---|---|---|
| `trabajo/skills-metodo` | Una pasada, opus, sobre `d3d00f9f` («Informe del revisor», abajo): eje (a) 0 bloquea, 1 importa, 2 menor; eje (b) 1 bloquea, 0 importa, 3 menor. **B1 (bloquea):** faltaban en el informe los `make check` de la fase 0 y del commit 3, con su PICO, y el punto 4 decía «Hecho». A1 (importa: el informe sin estado al final), A3 (la atribución de los dos ficheros a una línea ACORTADA), B2 («y no otra» en la línea base, más de lo que dice la fuente), B3 (`frames show --n` mayor que 1 fuera de la mirada de la guardia), corregidos; A2 y B4, declarados («Lo que se hizo con los hallazgos del revisor») | (la deja el consultor) | **De la sesión:** (1) una regla de cómo se abre un fotograma se mide contra la guardia para los dos casos, vídeo en cuarentena y fuera de ella, antes de escribirla: `_analizar_cli` niega `frames show` siempre en un vídeo en cuarentena (D2 c, PARADA de la fase 0); (2) una cita de la hoja de ruta por «paso» se busca en la entrada: los pasos numerados son de la Next Action, que caduca; se cita la entrada y su ADR. |

## Lo que se hizo con los hallazgos del revisor

En un commit propio, sellado (el último de la rama):

- **B1 (bloquea):** añadidos los `make check` de la fase 0 (`86b28167`, árbol `9c0b9adb`, 318 MiB)
  y del commit 3 (`d3d00f9f`, árbol `1b20d3e2`, 318 MiB), sacados de sus mensajes de commit y del
  `make-check.log` de cada uno, que se leyó antes de commitear. El punto 4 de la tabla queda bien.
- **A1 (importa):** el informe acaba en su estado, y la línea 8 lo remite al final.
- **A3 (menor):** los dos ficheros de PROJECT_STATE.md:150 se atribuyen ahora a su texto entero de
  HISTORIA:17417; la línea de PROJECT_STATE está ACORTADA.
- **B2 (menor):** la línea base de `activar-sesion` (`:63-64`) ya no dice «esa lectura, y no
  otra»: dice que se lee como la de ADR-0093 §6 y que es lectura del encargo, D1 a, como pedía D1
  a. Mismo número de líneas.
- **B3 (menor):** en `ingerir-sesion` (`:69`), fuera de cuarentena, «solo mira el instante de
  `--t`: sin `--n`» (`_tramos_en_la_cli`, `guardia.py:2619-2620`): con `--n` mayor que 1, la CLI
  imprime rutas que la guardia no miró. Es la condición de la respuesta, punto 0 («nunca dentro de
  un tramo»), aplicada a lo que hace la guardia; no es una regla nueva. Mismo número de líneas, así
  que las evidencias fichero:línea del bloque PAGADA de HISTORIA (que solo se amplía) siguen
  valiendo.
- **A2 (menor), declarado y después pagado** (orden de cierre, punto 1; sección «Orden de cierre», abajo): la orden de la verificación de `ingerir-sesion` (`:151`) sigue con
  `> knowledge-validate.log`; D4 solo deja añadir, y la línea de debajo dice dónde va el log. Si se
  quiere cambiar la orden, es para una rama que pueda sustituir texto de la skill.
- **B4 (menor), declarado:** «si la rama corre `make check` el dia de la apertura» es la redacción
  de D3 b; el paso 7 siempre lo corre, así que en la práctica la fila entra siempre.

## Informe del revisor

Pegado tal cual (agente `revisor`, opus, sobre `d3d00f9f`, 2026-11-14):

## Informe del revisor · trabajo/skills-metodo · 2026-11-14

HEAD d3d00f9f, base main 73b4e7a9 (`git merge-base main HEAD` = 73b4e7a98cef…). `git status --short` sale vacío. Cinco commits, nueve ficheros.

Resumen: la rama no rompe ninguna regla de la casa. Hay un bloquea del eje (b), que se arregla con una línea: falta en el informe el `make check` del tercer commit de la fase 1. Las citas de las skills son literales y la regla de los fotogramas se puede cumplir en los dos casos. Las dos líneas de Technical Debt salen pagadas enteras.

### Eje (a) · Reglas de la casa
Resumen: 0 bloquea, 1 importa, 2 menor.

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| A1 | importa | El informe no acaba en su estado. El único «Estado:» está en la línea 8 y está desfasado: dice «EN CURSO, fase 1» cuando la fase 1 ya está hecha. El fichero termina con la fila de ERRORES-RECURRENTES. CLAUDE.md, «Como se trabaja»: «Un informe por rama en `docs/validation/`, con su estado al final». Lo normal es que lo ponga `entregar-rama`, pero hoy falta. | `docs/validation/SKILLS-METODO.md:8` («Estado: EN CURSO, fase 1 …»); `:517-521`, la última sección, sin estado |
| A2 | menor | En `ingerir-sesion`, la orden de la verificación sigue escribiendo el log con una ruta relativa (`> knowledge-validate.log`, que cae en la raíz). Justo debajo, la línea nueva dice «nunca en la raiz». Se lee como una contradicción. Se dejó a propósito (D4: solo se añade) y está declarado, pero quien copie la orden repite la trampa. | `.claude/skills/ingerir-sesion/SKILL.md:151` frente a `:152-155`; `SKILLS-METODO.md:335-336` |
| A3 | menor | El informe atribuye a `PROJECT_STATE.md:150` los nombres `scripts/graficos_sesion.py:66-71` y `engine/decisiones.py:7-8`. Esa línea está acortada y no los trae: los traen ADR-0093, «Impacto», y el texto entero en HISTORIA. | `SKILLS-METODO.md:113-114`; `git show main:PROJECT_STATE.md \| sed -n 150p` → «Dos textos que ADR-0093 deja viejos y que trabajo/preparacion-sesion-7 no podía tocar … (…; entera en HISTORIA, Technical Debt ACORTADA)»; `docs/adr/0093-…md:223-226` |

Comprobado sin hallazgos:
1. **Contrato.**
   - `uv run python scripts/contrato_rama.py` → «CONTRATO: 9 ficheros dentro del contrato de trabajo/skills-metodo (riesgo bajo, artefacto docs/validation/SKILLS-METODO.md, tramo 'Carril: guardias y deuda', 4 comprobaciones para el revisor)», exit 0.
   - `uv run botsito state check` → «OK: rama 'trabajo/skills-metodo' …», exit 0.
   - `wc -c PROJECT_STATE.md` → 23435, igual que el informe.
   - `make check` no lo ejecuté. Su evidencia es `make-check.log`: «3513 passed, 6 xfailed», ningún `failed` (la única coincidencia es «xfailed»), «SELLO: make check en verde sobre el arbol 1b20d3e2…», que es `git rev-parse HEAD^{tree}`, y «PICO DE MEMORIA de make check: 318 MiB en `test`».
   - Los árboles sellados que cita el informe coinciden con los de sus commits: ab82b181 (c227edc9), 0433f5fa (a8acd219) y 8a8dffb4 (c7920376).
2. **Trailers `Fuente:`.** Ningún commit toca `knowledge/spec` ni `knowledge/cases`: `git log … -- knowledge/spec knowledge/cases` sale vacío.
3. **Holdout y material.** No se toca nada del holdout. La fila de HOLDOUT-EXPOSICIONES del 2026-11-14 entró en el commit de apertura, con la forma de la de dieta-estado. Todos los commits son del 14.
4. **Regímenes de cambio.** `git diff --name-status main...HEAD` no toca evidence, feedback, manifests, transcripciones, fotogramas ni `libros.yaml`. HISTORIA solo se amplía: la única línea «-» del diff es la cabecera `---`.
5. **Ambigüedades.** No cambian.
6. **ADR.** Ninguno nuevo ni cambiado. `test_adr.py` en verde.
7. **Informes cerrados.** Solo cambia HOLDOUT-EXPOSICIONES, que es un registro vivo, con una línea añadida.
8. **Tres guardias de `cita`.** No aplica: la rama no toca la spec.
9. **Lo demás de CLAUDE.md.**
   - No hay cifras en la forma ejecutable.
   - Comprobé contra su fuente siete citas del informe, todas exactas:
     - `:94`, lecciones 6 y 7 de video-julio (ERRORES-RECURRENTES.md:115);
     - `:97`, «el log de `knowledge validate` en la raíz dejó el primer `make check` en verde y sin sello» (`:118`);
     - `:98`, la lección 3 de guardia-falsos-positivos (`:121`);
     - `:83`, ADR-0093 §6 en `:121-123`;
     - `:88`, PROJECT_STATE.md:28, «(3) la corrida de ADR-0070 §3 y la lectura del pivote (ADR-0093 §6)»;
     - `:88`, HOJA-DE-RUTA.md:486, «NA:F, paso 3»;
     - `:91`, la fecha de ADR-0093 en `:232`.
10. **Items de evidencia nuevos.** Ninguno.
- **Rutas de `test_skills.py`.** Las 19 rutas nuevas con prefijo existen con esas mayúsculas y minúsculas (`git ls-files --error-unmatch …`), así que Linux no las rompe. Ninguna va pegada a otro carácter. `uv run pytest tests/unit/test_skills.py tests/unit/test_historia.py tests/unit/test_project_state.py tests/unit/test_hoja_de_ruta.py -p no:cacheprovider -rA`: 38 PASSED, ningún FAILED ni ERROR.
- **CI de Linux.** No hace falta: la rama no toca `scripts/git-hooks/`, `.claude/hooks/`, rutas, el sistema de archivos ni scripts (RITUAL.md:91-95). Lo que tiene de `.claude/` son tres SKILL.md.

### Eje (b) · Encargo
Resumen: 1 bloquea, 0 importa, 3 menor. Requisitos: 21 hechos, 1 parcial, 0 no hechos.

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 1 | Base: main, tag, una sola rama, F39c libre | Hecho | `git rev-parse main` = 73b4e7a9; `stable/F39b-dieta-estado^{commit}` = `main^1` = 6054c4ce; `git branch --list` da solo main y la rama; `git tag -l "stable/F39c*"` vacío. Lo de origin y la CI, solo por el informe (`:12-26`) |
| 2 | Abrir con abrir-rama: encargo, contrato y Archivo | Hecho | c227edc9; la desviación del guion que antepone `> ` está declarada (`:34-36`) |
| 3 | Contrato: tramo literal, riesgo bajo, las tres skills y HOLDOUT | Hecho | `contrato.yaml:2-13`; contrato_rama en verde |
| 4 | Informe con la PLANTILLA en sus primeros 600 caracteres | Hecho | `SKILLS-METODO.md:3` |
| 5 | Fila de HOLDOUT antes del primer `make check`, en la apertura, declarada como desviación | Hecho | `HOLDOUT-EXPOSICIONES.md:148`; `SKILLS-METODO.md:30-33` |
| 6 | La decisión del consultor (RUMBO §6), escrita en el informe | Hecho | `:38-45` |
| 7 | D1 a: el método de ADR-0093 §4 con sus palabras, la línea base de §6 y PIVOTES, el comando de julio del encargo | Hecho. Las cinco citas son literales con ADR-0093:92-102 | `activar-sesion/SKILL.md:55-72` |
| 8 | D1 b: viñeta «El arnes» sustituida (julio como diagnóstico, otras corridas autorizadas, R4.3 y ADR-0093 §6, opciones de ADR-0070 punto 3) | Hecho, con la cita corregida (respuesta, punto 3). No contradice ADR-0070 (la corrida que cuenta sigue con la lista cerrada de `:54-60`), ni ADR-0092 §6 (diagnóstico, `:168-170`), ni ADR-0093 §4 y §6 | `activar-sesion/SKILL.md:46-53`; R4.3 «Hecho cuando» en `HOJA-DE-RUTA.md:389`, literal |
| 9 | D1 c: regenerar `Generado.mqh` en el mismo commit | Hecho, sin pasar de RENOVAR-CIERRES | `activar-sesion/SKILL.md:106-111`. La orden y «`parametros.yaml`, el perfil» son las de `RENOVAR-CIERRES.md:56-65`. Fase 2, D3, en `CAPA-GENERADA.md:511-512` (la Fase 2 empieza en `:484`). `ENTRAN` en `generar_capa.py:59` |
| 10 | D1 d: ACTIVAR-SESION-06-MOTOR, anterior a ADR-0093 | Hecho | `activar-sesion/SKILL.md:15-16` |
| 11 | D2 a: trailer `Fuente:` de `tramos_no_citables.yaml` | Hecho, citando el punto 3 de §7 | `ingerir-sesion/SKILL.md:50-53`; `SESION-06-EXTRACCION.md` §7, punto 3; `test_tramos_fuente.py:72-85` |
| 12 | D2 b: ningún fotograma antes de situar el tramo, con las lecciones de video-julio | Hecho. «y nunca en el arranque de una grabación» es literal de la lección 6 | `ingerir-sesion/SKILL.md:30-38`; ERRORES-RECURRENTES.md:115, lecciones 3, 5, 6 y 7; ADR-0093:53-57 |
| 13 | D2 c (respuesta, punto 0): cómo se abre un fotograma, por casos | Hecho. Se puede cumplir en los dos casos (detalle debajo de la tabla) | `ingerir-sesion/SKILL.md:65-74`. La línea de «Herramientas» `:61-63` no se tocó |
| 14 | D2 d: el log de `knowledge validate` fuera de la raíz | Hecho, sin tocar `.gitignore` | `ingerir-sesion/SKILL.md:152-155`; lección 11 en ERRORES-RECURRENTES.md:118, «(11) la salida de una herramienta va a la carpeta de trabajo, nunca a la raíz del repo» |
| 15 | D3 a: PLANTILLA; el test solo en las extracciones y «la convención que piden sus encargos» en los demás | Hecho | `abrir-rama/SKILL.md:74-79`. `test_hoja_de_ruta.py:98-100` (`[:600]`) y `:242-244`. DIETA-ESTADO.md y ACTIVAR-SESION-06.md llevan PLANTILLA en sus primeros 600 bytes |
| 16 | D3 b: HOLDOUT antes del primer `make check`, y la verificación ajustada | Hecho | `abrir-rama/SKILL.md:97-101` y `:113-115`; lección 3 en ERRORES-RECURRENTES.md:121; DIETA-ESTADO.md:26 lo declaró como desviación |
| 17 | Herencias (respuesta, punto 2): la lección 8 en ingerir-sesion y la de dieta-estado en el paso 6 de abrir-rama | Hecho. La cita de la lección 8 es literal | `ingerir-sesion/SKILL.md:54-57`; `abrir-rama/SKILL.md:89-92`; ERRORES-RECURRENTES.md:122 |
| 18 | D4: solo se añade, salvo D1 b y la verificación de D3 b | Hecho | En el diff solo se quitan las 5 líneas de la viñeta «El arnes» y las 2 de la verificación de abrir-rama |
| 19 | D5: nada fuera del contrato; sin material ni arnés | Hecho | `git diff --name-status`: las tres skills, PS, `contrato.yaml`, el encargo, HISTORIA, HOLDOUT y el informe |
| 20 | D6: las dos líneas de TD, literales al final de HISTORIA, en el commit que paga cada una | Hecho (detalle debajo de la tabla) | a8acd219 quita la línea de :83; d3d00f9f quita la de :142 |
| 21 | Punto 4: un commit por skill, sellado, con el PICO DE MEMORIA de cada `make check` y `wc -c` | **Parcial** | Ver B1 |
| 22 | Punto 5: las secciones del informe y las respuestas del consultor iguales en el informe y el encargo | Hecho | `sed -n 61,68p` del encargo con `grep -c -F -x -f -` sobre el informe → 8 de 8 líneas; «El encargo, punto por punto» en `:462-489` |

Detalle del requisito 13 (D2 c), medido en el código sin ejecutar nada sobre vídeos:
- **Vídeo en cuarentena.** `_analizar_cli` niega `corpus frames show` cuando `--video` está en `sesiones_en_cuarentena` (`guardia.py:1098-1102`, `:2531-2537`). Su mensaje manda leer `data/fotogramas/<v>/png-1fps/<ms>.png`.
- **Vídeo fuera de cuarentena.** `_tramos_en_la_cli` niega el instante `--t` que cae dentro de un tramo vigilado (`:2617-2637`).
- **El Read del PNG.** `motivo_fichero` no niega ningún Read de `data/fotogramas/` (`:563-598`).
- **Lo que imprime la CLI.** `frames show` imprime la ruta del PNG (`cli.py:560-565`) y admite `--video`, `--t` y `--n` (`:3193-3196`).

Detalle del requisito 20 (D6):
- Las dos líneas de `main` aparecen byte a byte en el bloque «# Technical Debt PAGADA · sale de PROJECT_STATE.md en trabajo/skills-metodo (2026-11-14)». La de :142 está en `HISTORIA.md:18385`.
- Las líneas que dan de evidencia son correctas: `activar-sesion:106-111`, `ingerir-sesion:50-53`, `:30-38`, `:65-74` y `abrir-rama:74-79`.
- La de :142 está pagada entera, en sus tres partes: el trailer, la PLANTILLA y los fotogramas.

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| B1 | bloquea | Falta en el informe el `make check` del tercer commit de la fase 1 (d3d00f9f), con su línea PICO DE MEMORIA. El encargo lo pide expresamente: «En cada make check, la línea PICO DE MEMORIA al informe» (punto 4). Aun así, la tabla «punto por punto» marca el punto 4 como «Hecho». La evidencia existe y es una línea de arreglo: `make-check.log` trae «SELLO … 1b20d3e2…» (= `HEAD^{tree}`) y «PICO DE MEMORIA de make check: 318 MiB en `test`». Tampoco está el `make check` del commit de la fase 0, 86b28167: el de `:226-227` es el de la apertura (árbol ab82b181 = `c227edc9^{tree}`). | `SKILLS-METODO.md:398-453`: la sección de abrir-rama no tiene línea de `make check`, cuando `:318-319` y `:395-396` sí la tienen para los commits 1 y 2. `:487`: «4 · … PICO DE MEMORIA … · Hecho» |
| B2 | menor | La línea base: D1 a pedía decir que es «esa lectura», es decir, una lectura del encargo. La skill la da como un hecho y le añade exclusividad: «Es la de ADR-0093 §6 … esa lectura, y no otra». ADR-0093 §6 la define para el pivote, no para el delta de cada activación, y ninguna fuente dice «y no otra». | `activar-sesion/SKILL.md:63-64`; ADR-0093:124-129; el encargo, D1 a |
| B3 | menor | Fuera de cuarentena, la guardia solo mira el instante de `--t`. Con `--n` mayor que 1, `frames show` imprime los N fotogramas más cercanos, y alguno puede caer dentro de un tramo. «Read solo de la ruta que imprime» no lo excluye. El informe lo sabía en la fase 0 («solo mira el instante de `--t`»), pero la skill no lo dice. | `guardia.py:2619-2620` y `:2629`; `cli.py:556` y `:561-565`; `SKILLS-METODO.md:154`; `ingerir-sesion/SKILL.md:68-69` |
| B4 | menor | La condición «si la rama corre `make check` el dia de la apertura» se cumple siempre, porque el paso 7 sella la apertura con `make check`. La verificación, en cambio, la trata como optativa («si entro»). Es la redacción del propio encargo (D3 b). | `abrir-rama/SKILL.md:94-100` y `:113-115` |

Lo que la rama hace y el encargo no pide: nada que no esté respaldado. Lo añadido sale de las respuestas del consultor a la PARADA:
- la lección 3 junto a la 5, la 6 y la 7;
- la orden de `generar_capa.py` (punto 3);
- las dos herencias (punto 2).

Lo que no se toca (D5): comprobado con `git diff --name-status`.

### Lo que no pude comprobar
- **`make check`**: escribe, así que no lo ejecuté. Lo sustituye `make-check.log`: su SELLO es el árbol de HEAD, su PICO es 318 MiB y la suite sale en verde.
- **Origin, el tag F39c en origin y la CI de `main` (run 43560175823)**: necesitan red. Solo lo afirma el informe (`:17-23`); en local cuadra.
- **El comportamiento real de la guardia sobre un vídeo**: no ejecuté ni `frames show` ni Read de ningún PNG, por orden del encargo. Lo de D2 c sale de leer el código.
- No leí material del trader, velas, holdout ni fotogramas.

### Comandos ejecutados
1. `git branch --show-current && git merge-base main HEAD && git log --format='%h %s' main..HEAD && git diff --stat main...HEAD && git status --short`
2. `git diff main...HEAD -- .claude/skills PROJECT_STATE.md docs/validation/HOLDOUT-EXPOSICIONES.md`
3. `uv run python scripts/contrato_rama.py; uv run botsito state check` encadenados: **negado por la guardia** (exige comandos separados). Se partió en los dos siguientes.
4. `uv run python scripts/contrato_rama.py`
5. `uv run botsito state check`
6. `wc -c PROJECT_STATE.md; ls -la make-check.log; grep -E "SELLO|PICO DE MEMORIA|passed|failed" make-check.log | tail -5`
7. `git diff main...HEAD -- docs/state/HISTORIA.md | grep …` (el bloque PAGADA y las líneas «-»)
8. `git rev-parse HEAD^{tree} a8acd219^{tree} c7920376^{tree} c227edc9^{tree}`
9. Read de las tres SKILL.md, del encargo, de `contrato.yaml`, de `SKILLS-METODO.md` y de ADR-0093; Read de ADR-0070:40-74 y ADR-0092:150-184
10. `grep`/`sed` sobre HOJA-DE-RUTA.md (R4.3, `:486`), PIVOTES-SESION-7.yaml, RENOVAR-CIERRES.md:50-70, CAPA-GENERADA.md y generar_capa.py
11. `sed -n 830,862p docs/validation/SESION-06-EXTRACCION.md`; Read de `tests/contract/test_tramos_fuente.py`
12. `sed -n 90,106p` y `238,252p` de `tests/unit/test_hoja_de_ruta.py`
13. Un `grep` con bucle `for`: **negado por la guardia**. Rehecho con Grep sobre los encargos y con `head -c 600 … | grep` sobre DIETA-ESTADO.md y ACTIVAR-SESION-06.md
14. Read de ERRORES-RECURRENTES.md:115; `sed -n 118p/121p/122p … | grep -o …`
15. `grep -n` y Read de `.claude/hooks/guardia.py` (`:420-479`, `:560-629`, `:1095-1102`, `:2520-2637`)
16. `grep`/`sed` y Read de `src/botsito/cli.py` (`:537-571`, `:3190-3202`, `:3648-3656`); Grep de `png-1fps` en `src/botsito/corpus`
17. `sed -n 980,1003p docs/validation/VIDEO-JULIO.md`; `grep -n fotograma PROJECT_STATE.md`
18. `git show main:PROJECT_STATE.md | sed -n 83p | grep -c -F -x -f - docs/state/HISTORIA.md`, y lo mismo con la línea 142 (`grep -n`)
19. `git log --format='== %h %s' --stat main..HEAD`; `git show <commit> -- PROJECT_STATE.md`
20. `sed -n 61,68p docs/encargos/trabajo-skills-metodo.md | grep -c -F -x -f - docs/validation/SKILLS-METODO.md`; `git diff main...HEAD --name-status`; `git log --format='%h%n%B' main..HEAD -- knowledge/spec knowledge/cases`
21. `uv run pytest tests/unit/test_skills.py tests/unit/test_historia.py tests/unit/test_project_state.py tests/unit/test_hoja_de_ruta.py tests/unit/test_adr.py -q -p no:cacheprovider`, y la misma corrida con `-rA` (38 PASSED, ningún FAILED)
22. `sed -n 88,98p docs/runbooks/RITUAL.md`
23. `git ls-files --error-unmatch <las 19 rutas nuevas>`
24. `grep -n "def test_los_tramos_del_repo_real" …`; `grep` sobre ACTIVAR-SESION-06-MOTOR.md y HISTORIA (F38o)
25. `git log --format='%h %ad' --date=iso main..HEAD`
26. `grep -c -i failed make-check.log`; `grep -n CONTRATO make-check.log`
27. `grep` de ERROR en `src/botsito/validation/knowledge.py` y en `cli.py`
28. `sed -n 148p PROJECT_STATE.md`; `git show main:PROJECT_STATE.md | sed -n 150p`
29. Grep de PAGADA en `docs/state/README.md`
30. `git branch --list; git rev-parse main "stable/F39b-dieta-estado^{commit}" main^1; git tag -l "stable/F39c*"`

## Orden de cierre (2026-11-14)

Copiada tal cual (también al final del encargo):

> Orden de cierre de trabajo/skills-metodo (consultor, 2026-11-14). Revisada la rama contra main: el diff de las tres skills es el que dice el informe; cada lección citada (video-julio 3, 5, 6, 7 y 8; preparacion-sesion-7 11; la de dieta-estado; guardia-falsos-positivos 3) dice en ERRORES-RECURRENTES.md lo que la skill le atribuye; la orden de generar_capa.py es la de RENOVAR-CIERRES.md; las dos líneas de Technical Debt salen enteras y están literales en HISTORIA, que solo crece; y PROJECT_STATE, fuera de esas dos, solo cambia en Current Branch, Current Feature y las dos líneas del Archivo 71. Se cierra con la skill cerrar-rama y docs/runbooks/RITUAL.md, con todas sus puertas.
>
> 1. Antes del chore(cierre), un commit propio en la rama, sellado: en .claude/skills/ingerir-sesion/SKILL.md, la orden de verificación que aún escribe «> knowledge-validate.log» en la raíz (:151) se sustituye en su misma línea por la forma que escribe el log en la carpeta de trabajo de la sesión, fuera del repo, y las líneas nuevas de debajo (:152-155) no se tocan, para que ninguna línea se mueva y las evidencias fichero:línea de HISTORIA sigan valiendo (compruébalo con wc -l antes y después; si cambia el número de líneas, PARADA). Es el menor que el revisor dejó declarado porque el encargo solo dejaba añadir: lo autorizo ahora, porque la ingesta de la 7a usa esta skill y una skill no puede mandar una cosa y la contraria. El informe lo recoge en su sección y en el estado. Es una excepción declarada a RITUAL.md (hacia :116-118: el del contrato es el único commit que el cierre añade a la rama), con el precedente del punto 1a de la orden de cierre de trabajo/guardia-falsos-positivos; dilo en el registro.
> 2. Tag: stable/F39c-skills-metodo (comprueba antes que no existe ni en local ni en origin). Mensaje del merge: «merge trabajo/skills-metodo: activar-sesion, ingerir-sesion y abrir-rama al día con ADR-0093 y las lecciones registradas». Mensaje del tag anotado: «trabajo/skills-metodo: las tres skills de la ingesta y la activación de la 7a al día; pagadas dos líneas de Technical Debt». Si cerrar-rama propone otros, usa estos.
> 3. La fila de HOLDOUT-EXPOSICIONES del 2026-11-14 ya está en la rama (commit de apertura). Si el cierre cruzara a otro día en Lima, antes del primer make check de ese día va su fila en un commit propio de la rama; hoy no debería hacer falta.
> 4. Commit chore(cierre) en la rama (punto 3 de RITUAL), uno solo:
>    - sale contrato.yaml;
>    - entra en HISTORIA el «# Registro de cierre · `trabajo/skills-metodo` (<fecha>)», con la forma del de trabajo/dieta-estado: stable/F39c-skills-metodo^{commit} en lugar del sha del merge; los commits de la rama (c227edc9, 86b28167, a8acd219, c7920376, d3d00f9f, 10af3962, el del punto 1 y este); la fila de HOLDOUT-EXPOSICIONES dentro de la rama; que no hubo CI de Linux porque la rama no toca hooks, permisos, rutas, el sistema de archivos ni código (RITUAL.md, hacia :93-96), con la confirmación del revisor; las dos líneas de Technical Debt pagadas; y el tamaño de PROJECT_STATE con wc -c;
>    - entra la fila de ERRORES-RECURRENTES.md que prepara el informe, con sus cuatro columnas y la rama entre acentos graves como las demás filas; en la 3.ª (hallazgos del consultor después), este texto: «1 importa, 4 menores, todos del consultor y cazados antes de la revisión. Importa: D2 c del encargo (abrir un fotograma solo por frames show y Read de la ruta que imprime) no se podía cumplir para ningún vídeo en cuarentena, porque la guardia niega frames show en ellos; lo cazó la fase 0, y el mismo error estaba en el prompt de la ingesta de la 7a, ya corregido antes de pegarlo. Menores: «paso (3)» atribuido a R4.3, que es de la Next Action F; el trailer Fuente: en §7 punto 1 y no en el 3; «nunca elige entre dos lecturas» atribuido a ADR-0092 §6 y no a ADR-0093 §4; y la restricción «solo añadir» del encargo, que dejó en ingerir-sesion una orden que contradecía la línea nueva (pagado en el punto 1 de la orden de cierre). Nada en la rama que el revisor no viera.»; en la 4.ª, la lección preparada, y detrás: «Una regla sobre cómo se usa una herramienta se escribe después de leer lo que la guardia deja hacer con ella para cada caso (vídeo en cuarentena o no), no desde la documentación de la herramienta.»;
>    - Next Action: no sale, no entra y no cambia nada. Hoja de ruta: no cambia.
>    - Comprueba que PROJECT_STATE queda por debajo de 25.000 bytes antes del commit; si no, PARADA.
> 5. Merge a main, tag, y commit de estado que solo reemplaza Current Branch (main), Current Feature, Stable Main State y Last Stable Commit: la Next Action no se toca y no se añade nada a Completed Features ni al Change Log. make check sellado y push atómico de main y el tag en un solo comando (yo confirmo la regla ask con «1. Yes»). CI de main en verde antes de borrar nada.
> 6. Borra la rama local trabajo/skills-metodo. No hay fix/skills-metodo en origin: compruébalo con git ls-remote y dilo.
> 7. Informe final: sha de main, sha del merge, tag, run de la CI de main con su resultado, ramas que quedan en local y en origin, tamaño exacto de PROJECT_STATE.md en main con wc -c, y la hora de cada make check del cierre.
>
> Cuando respondas a esto, escribiré /cerrar-rama trabajo/skills-metodo en una línea aparte.

**Punto 1, hecho en un commit propio de la rama, sellado, antes del `chore(cierre)`:** la orden de
verificación de `ingerir-sesion` (`:151`) escribe ahora el log en
`<carpeta de trabajo fuera del repo>/knowledge-validate.log`, sustituida en su misma línea; las
líneas `:152-155` no se tocan. `wc -l .claude/skills/ingerir-sesion/SKILL.md`: 159 antes y 159
después, así que las evidencias fichero:línea de HISTORIA siguen valiendo. Es una excepción
declarada a RITUAL.md (hacia :116-118), con el precedente del punto 1a de la orden de cierre de
`trabajo/guardia-falsos-positivos`.

## Estado

**Rama lista para revisión, NO cerrada; con la orden de cierre del 2026-11-14, en cierre.** Las tres skills al día (`a8acd219`, `c7920376`,
`d3d00f9f`), las dos líneas de Technical Debt fuera, pagadas enteras; los arreglos del revisor en el
último commit, sellado. Sin CI de Linux (RITUAL.md, hacia :93-96; el revisor lo confirma). La
orden de cierre es de Aleks; tag de cierre previsto: `stable/F39c-skills-metodo`.
