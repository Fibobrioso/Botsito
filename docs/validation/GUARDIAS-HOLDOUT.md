# GUARDIAS-HOLDOUT · La fila del día en el sello (G2), dos huecos de test_hoja_de_ruta (H) y el estudio de G1

> PLANTILLA hasta la fase 0 (la línea con que nació): ya no lo es; la rama está lista para revisión.

Rama `trabajo/guardias-holdout`, abierta el 2026-11-19 (21:07, reloj de la laptop en Lima, UTC-5)
desde `main` en fa592071 (commit de estado sobre el merge 2fc884ac del tag
`stable/F39g-preregistro`). Encargo: `docs/encargos/trabajo-guardias-holdout.md`. Tramo: «Carril:
guardias y deuda». Tag previsto: `stable/F39h-guardias-holdout` (no existe en origin:
`git ls-remote --tags origin "stable/F39h*"` vacío). Riesgo: **alto**, como manda el encargo.

Los nombres «G1» y «G2» de este informe son los del encargo. No son la G.1 ni la G.2 de la hoja de
ruta (`HOJA-DE-RUTA.md:734` y `:745`), ni `trabajo/guardia-g1`, ni los de `GUARDIAS-CITAS.md`
(herencia 5 del auditor). Por eso las líneas que se preparan para PROJECT_STATE los describen por
lo que hacen.

La PARADA es condicional (encargo): las decisiones vinieron por adelantado. Seguí con todo lo que
cuadraba con lo medido. Lo que no cuadra, o lo que el encargo no decide, está en la PARADA final
(§9).

## 0. Apertura: la base comprobada

- `git rev-parse --short main` = `fa592071`; `git rev-parse main origin/main` da dos veces
  `fa592071fe071e12893709f28076062802312c76`.
- Último tag de HISTORIA: `stable/F39g-preregistro`; `git rev-parse "stable/F39g-preregistro^{commit}"`
  = `2fc884ac7b337d9d4ce8ced311f6acdb8cfd7125` = `git rev-parse main^1`; está en origin
  (`git ls-remote --tags origin stable/F39g-preregistro` no sale vacío).
- CI de `main` sobre fa592071: `gh run view 44653987599` →
  `{"conclusion":"success","headBranch":"main","headSha":"fa592071fe071e12893709f28076062802312c76","status":"completed","workflowName":"ci"}`.
  Es el run que nombraba el encargo, y está verde.
- `git branch --list` solo daba `main`; `git ls-remote --heads origin "fix/*"` vacío.
- Commit de apertura `e115f208`, sellado (`SELLO: make check en verde sobre el arbol 0ee5f4b1…`;
  3536 passed, 6 xfailed). Antes del primer `make check` del día se escribió y estadió la fila
  de HOLDOUT-EXPOSICIONES del 2026-11-19.

## 1. Fase 0

### 1.1 (0.1) Herencias

| Qué pide | Fichero:línea | Pieza |
|---|---|---|
| «make check, en una rama trabajo/*, no sella si HOLDOUT-EXPOSICIONES.md no tiene una fila con la fecha del día … guardia pendiente, propuesta en trabajo/cuenta-por-mes» | `PROJECT_STATE.md:102` | G2 |
| La propuesta de diseño: fila cuya primera celda sea la fecha local, leída del árbol ESTADIADO, en la fase del contrato; «En `main` y en el ritual de cierre no se exige» | `CUENTA-POR-MES.md:722-731` (escrita tras el hallazgo b1 del revisor, `:812`, que decía que solo estaba la cita del consultor, `:628`) | G2 |
| La lección «la fila de HOLDOUT-EXPOSICIONES del día se escribe antes del primer `make check` del día» (3 de la sesión) y A1 (la fila del 2026-11-13 faltaba) | `ERRORES-RECURRENTES.md:121` (`trabajo/guardia-falsos-positivos`) | G2 |
| El trabajo del 2026-11-07 empezó sin su fila; «una lección que se rompe en la rama siguiente pide una guardia» | `ERRORES-RECURRENTES.md:113` (`trabajo/cuenta-por-mes`) | G2 |
| a1: lo leído el 18 sin fila, escrita tarde | `ERRORES-RECURRENTES.md:126` (`trabajo/laminas-sesion-7b`) | G2 |
| Cada `make check` lee el M1 de marzo y de junio para calentar, sin declararlo; «hoy lo cubre HOLDOUT-EXPOSICIONES» | `PROJECT_STATE.md:107`; `HOJA-DE-RUTA.md:765` (G.2) | G2 (por qué) |
| Los guiones de la plataforma (`contrato_rama.py` entre ellos), cambiados en una rama, no se ejecutan sueltos desde la sesión | `PROJECT_STATE.md:93` (entera en HISTORIA); `GUARDIA-G1.md` §6.4 | G2 (0.3) |
| «test_hoja_de_ruta no distingue un registro «HECHA · T» de una letra reutilizada del de la T vigente: letras_hechas es un conjunto» | `PROJECT_STATE.md:111`; `VIDEO-JULIO.md:775-777` (§10.1) | H (b) |
| La regla de la letra reutilizada | `docs/runbooks/DECISIONES-DE-PROCESO.md`, entrada del 2026-10-27 | H (b) |
| (c) «Depende de» y «después,» sin «de» | ninguna fuente escrita en el repo: el «buzón del consultor del 2026-11-08» no está en el repo (auditor, 24); lo sostiene el código, `test_hoja_de_ruta.py:29-31` | H (c) |
| B1 de `trabajo/guardia-g1`: el id de un caso reservado en tres commits de la rama; «ningún id de un caso reservado en un comando» | `ERRORES-RECURRENTES.md:106` | G1 |
| a2 de una rama de septiembre: una fecha de septiembre que coincide con un día reservado (la subida de v5 a Drive), quitada del informe y viva en la historia | `ERRORES-RECURRENTES.md:83` | G1 |
| (5) «el alcance "ninguna fecha reservada en nada commiteado" se comprueba sobre cada commit de la rama (`git log -p` …)» | `ERRORES-RECURRENTES.md:118` (`trabajo/preparacion-sesion-7`) | G1 |
| La fecha de un día reservado retirada del informe del revisor | `HISTORIA.md:19410` (auditor, 31) | G1 |

En el carril «Carril: guardias y deuda» de la hoja de ruta (`HOJA-DE-RUTA.md:722`) ninguna `###`
recoge G2, H ni G1: vienen de Technical Debt. No hay `NA:` ni «Depende de» que comprobar
(auditor).

### 1.2 (0.2) Dónde vive G2

- `make check` corre `contrato` justo detrás de `desellar` (`Makefile:82`, «Va el primero tras
  desellar», `:62-64`), y en la CI (`ci.yml`: `push` a `main`, `feature/**` y `fix/**`;
  `make check`). La CI nunca corre en `trabajo/**`.
- **Decisión aplicada: G2 se llama desde `main()`, no desde `comprobar()`.** Es lo que menos toca:
  las 16 funciones de `tests/unit/test_contrato_rama.py` (25 casos con los parametrizados; auditor,
  11) llaman a `comprobar()` en repos sin HOLDOUT-EXPOSICIONES, y siguen intactas, sin darles
  fila.
- **En el propio `contrato_rama.py`, no en un módulo nuevo:** la línea de `mypy --strict` vive en
  el Makefile (`Makefile:41`), y `pyproject.toml` solo cubre `botsito` y `tests`. Un módulo nuevo
  en `scripts/` exigiría siempre tocar el Makefile (auditor, 12), y eso descarta la otra vía del
  encargo.
- La regla de actuación es un `startswith("trabajo/")` explícito sobre la rama local
  (`rama_actual`, `git symbolic-ref`). Con eso, `main`, `fix/`, `feature/` y HEAD separado quedan
  fuera; `_sin_prefijo` no se usa.

### 1.3 (0.3) La guardia de Claude Code

Medido con la guardia por stdin (`python .claude/hooks/guardia.py < <json>`), con el código nuevo:

- **Editar `contrato_rama.py`: pasa.** Las ediciones se hicieron con Edit sin ninguna negativa.
- **`make check > make-check.log 2>&1`: pasa** (exit 0). `_analizar_make` solo mira que el
  `Makefile` sea el de `main` (`guardia.py:2419-2445`, `:4085-4090`), y el Makefile no cambia.
- **`uv run python scripts/contrato_rama.py`: NEGADO**, pero no por recorrer directorios. El
  motivo literal: «el codigo lanza `… 'git' '-c' 'core.quotepath=false' …` (`subprocess.run`), y la
  guardia lo niega como comando: … clave fuera de la lista cerrada». Es el `_git` que el guion YA
  tenía (`contrato_rama.py:179-186` en `main`), y lo que el repo ya registra para cualquier rama que
  cambie un guion de la plataforma (`PROJECT_STATE.md:93`; `GUARDIA-G1.md` §6.4). La premisa del
  encargo («no debe recorrer directorios y nombrar algo sensible a la vez») no aplica. El auditor
  la marcó INCORRECTA (14) por lo mismo: el ajuste que el encargo preveía no lo resuelve.
  Comprobado de todos modos: G2 lee un solo fichero del índice (`git show :ruta`) y no casa con
  `CODIGO_QUE_RECORRE` (`guardia.py:1096`).
- Qué cambia: nada del diseño. En `main`, tras el merge, el guion vuelve a ser idéntico al de
  `main` (código revisado) y el paso 6 de abrir-rama lo lanza. En esta rama lo ejecuta `make check`,
  y las comprobaciones del contrato lo dicen así (§7, desviación 4). Queda el orden del paso 6
  frente a la fila: §9, punto 2.

### 1.4 (0.4) Las filas y el reloj

- La tabla de `HOLDOUT-EXPOSICIONES.md` es la ÚNICA del fichero cuya cabecera empieza por
  `| Fecha |` (`:15`, `grep -n "^| *Fecha *|"`); va de la `:15` a la `:167` y la sigue
  «## Lo que esto obliga»: no está al final. Sus filas empiezan por `| AAAA-MM-DD |`
  (151 al abrir la rama). Las 81 de noviembre nombran la rama con `trabajo/…`. Una nombra dos
  ramas, y hay nombres que son prefijo de otros (`trabajo/laminas` frente a
  `trabajo/laminas-motivos`; auditor, 18). Por eso G2 exige la rama ENTERA, con frontera (§2).
- El reloj: `date` de la laptop da `-0500` (Lima). G2 usa `datetime.date.today()`, el día LOCAL de
  la máquina (§8, límite 1).

## 2. G2 · No se sella sin la fila del día (hecho)

En `scripts/contrato_rama.py`, después de `comprobar`:

- `problemas_fila_del_dia(rama, hoy, texto)`: la función pura, con la rama, el día y el texto por
  parámetro. Fuera de `trabajo/*` devuelve `[]`. Si no, pasa cuando alguna fila de la tabla de
  exposiciones (`filas_de_exposiciones`: la primera tabla con cabecera `| Fecha |`, hasta su
  primera línea que no es de tabla) cumple dos cosas. La primera, que su primera columna sea
  `hoy` en AAAA-MM-DD. La segunda, que nombre la rama entera con
  `(?<![\w/.-])<rama>(?![\w/-])`. Al fallar da el mensaje del encargo, literal: «G2: falta la fila
  de HOLDOUT-EXPOSICIONES del <hoy> para trabajo/<rama>; escríbela y estadíala antes de este make
  check (ADR-0021 §4)».
- `texto_estadiado(raiz, ruta)`: `git show :ruta` (el índice, lo que se sella), o None.
- `fila_del_dia(raiz, hoy)`: la rama local, y solo si empieza por `trabajo/`, el texto estadiado.
- `main()`: imprime el contrato como antes, y después G2. Si falla, el mensaje va a stderr y sale
  con 1. Si pasa en `trabajo/*`, imprime
  `G2: fila de HOLDOUT-EXPOSICIONES del <hoy> para <rama>, estadiada`. El día sale de `_hoy()`
  (reloj local) una sola vez.
- `mypy --strict scripts/contrato_rama.py`, `ruff check` y `ruff format --check`: limpios.

Tests en `tests/unit/test_fila_del_dia.py` (nuevo), con el texto y el día inyectados. Cada uno de
la lista del encargo:

| Caso del encargo | Test |
|---|---|
| sin fila | `test_falla_sin_ninguna_fila_del_dia`, `test_falla_sin_el_fichero` |
| fila de ayer | `test_falla_con_la_fila_de_ayer` |
| fila de hoy de otra rama | `test_falla_con_la_fila_de_hoy_de_otra_rama` (5 casos: otra rama, una que empieza igual, una que es prefijo, el mismo nombre con `fix/`, `feature/trabajo/prueba`) |
| fila de hoy solo sin estadiar | `test_cuenta_la_fila_estadiada_y_no_la_del_arbol` (repo temporal: sin estadiar falla; estadiada pasa; estadiada y borrada del árbol, pasa) |
| fila buena | `test_pasa_con_la_fila_de_hoy_que_nombra_la_rama`, `test_la_tabla_no_tiene_que_estar_al_final` |
| rama fix/x y main (no actúa) | `test_fuera_de_trabajo_no_actua` (main, `fix/`, `feature/`, vacía, «trabajo» sin barra) y `test_en_un_repo_fuera_de_trabajo_no_actua` (main, `fix/prueba` y HEAD separado) |

Y además: `test_solo_cuenta_la_tabla_de_exposiciones_y_su_primera_columna` (otra tabla, el día
fuera de la primera columna, prosa); `test_main_del_guion_niega_sin_la_fila_en_trabajo` (`main()`
entero, con `_hoy` sustituido); `test_hoy_es_el_dia_del_reloj_local`.

**Que rompen, medido con mutantes** (editados en el fichero, pytest, y vuelta atrás comprobada por
`git hash-object`: `b9bfa80e…` antes y después). Primero intenté cargarlos en memoria desde la
carpeta de la sesión, y la guardia lo negó dos veces: un subproceso calculado, y la carga del
guion cambiado con su `git -c` (§7, desviación 3). Resultados:

| Mutante | Tests que fallan |
|---|---|
| lee el árbol de trabajo y no el índice | `test_cuenta_la_fila_estadiada_y_no_la_del_arbol` |
| actúa fuera de `trabajo/` (sin el `startswith`) | `test_fuera_de_trabajo_no_actua` ×3 y `test_en_un_repo_fuera_de_trabajo_no_actua` |
| la rama como subcadena, sin frontera | `test_falla_con_la_fila_de_hoy_de_otra_rama` ×2 |
| no mira la rama | 5 |
| `main()` no llama a G2 | `test_main_del_guion_niega_sin_la_fila_en_trabajo` |

**CLAUDE.md**: una línea «Guardia:» bajo «Toda exposicion se declara … el mismo dia», en el mismo
commit que G2.

## 3. H · Dos huecos de test_hoja_de_ruta (hecho)

- **(c)** `DEPENDENCIA` reconoce también `depende de` y `despu[eé]s,` (sin «de»).
- **(b)** Función nueva `letras_registradas_tras_su_ultima_vida(historia)`: las letras cuyo ÚLTIMO
  registro «# Next Action HECHA · X ·» va después del último `# Archivo` de HISTORIA en que X
  estaba viva en la Next Action. HISTORIA solo se amplía, y el Archivo de una rama va antes que el
  registro que esa rama escribe al cerrar. `problemas_b` añade el problema «esta HECHA y HISTORIA
  no la registra despues de su ultima vida en la Next Action (una letra reutilizada lleva su
  registro nuevo)» cuando la letra tiene un registro, pero ninguno posterior a su última vida.
- **La decisión del encargo se cumple: con la detección nueva, la hoja de ruta y PROJECT_STATE.md
  de `main` siguen pasando.** Medido antes de tocar el test, con un guion de solo lectura en la
  carpeta de la sesión: (c) sobre la Next Action de `main` → `[]`, sin ningún disparador nuevo. (b):
  las 9 letras HECHAS en la hoja (E, O, P, S, T, U, W, X, Y) tienen su último registro detrás de
  su última vida; ninguna letra muerta tiene el registro antes. Después, los cuatro tests del repo
  real (a-d) en verde con el código nuevo. Nada va a la PARADA por H.
- Tests sintéticos nuevos: `test_c_se_rompe_con_depende_de_y_con_despues_coma` (3 casos);
  `test_b_se_rompe_si_falta_el_registro_de_una_letra_reutilizada`, que enseña además que
  `letras_hechas` ya daba la W (el hueco); y
  `test_b_la_vida_de_una_letra_solo_cuenta_en_la_next_action_de_un_archivo`. Con el código viejo
  (la `DEPENDENCIA` de antes y la rama `al_dia` quitada), fallan los 4 nuevos que tienen que
  fallar; el fichero, restaurado por hash (`dcf641a2…`).
- H paga la línea de Technical Debt `PROJECT_STATE.md:111` (auditor, herencia 1): su salida va en
  lo preparado para el cierre (§10).

## 4. G1 · Estudio, sin implementar: fechas de días ocultos en lo que añade una rama

### 4.1 El guion y su fase 0 con la guardia

`anexos/GUARDIAS-HOLDOUT/medir_g1.py`. Los días ocultos salen de `casos_ocultos` (la puerta;
`holdout.py:456`) y viven en memoria; no imprime fechas, ids, líneas ni nombres de fichero. Su
salida, entera, en `anexos/GUARDIAS-HOLDOUT/medir_g1.txt`: `grep -cE "[0-9]{4}-[0-9]{2}-[0-9]{2}"`
da 0. La lectura se declaró en HOLDOUT-EXPOSICIONES antes de la primera corrida, y se amplió antes
de la segunda.

La fase 0 del guion chocó dos veces con la guardia. La primera, por `git -c core.quotepath=false`.
La segunda, por `git log` con un argumento que se construye al ejecutarse. Seguí la forma que la
propia guardia propone en su mensaje («rutas LITERALES»): cada llamada a git va literal entera
(subcomando, rango `stable/F39a-guardia-falsos-positivos^1..main` y pathspec
`:(exclude)knowledge/cases/holdout/`), y el reparto por rama se reconstruye en Python desde el
grafo. Con eso la guardia lo deja pasar (exit 0 por stdin). Es lo que permite
`DECISIONES-DE-PROCESO.md`, entrada del 2026-10-21, punto (1), declarado aquí (§7, desviación 2).

Rango: las ramas cerradas de F39a a F39g (**incluida** F39a, porque el encargo dice «desde») y
los commits de estado de `main`: 76 commits, 69 con diff fuera del holdout, 16.885 líneas
añadidas o de mensaje.

### 4.2 Lo medido

Días ocultos: 34; desde el inicio del proyecto (2026-09-04, `DECISIONES-DE-PROCESO.md`), 8. Solo
esos 8 pueden coincidir con una fecha de trabajo.

| Clase | Líneas con un día oculto | De ellas, con uno anterior al proyecto |
|---|---|---|
| trailer `Fuente:` | 0 | 0 |
| mensaje de commit, fuera del trailer | 1 | 0 |
| `uv.lock` | 0 | 0 |
| fichero de asignación (`particiones.yaml`) | 0 | 0 |
| id de trabajo (`ev-`/`fb-`/`…-sesion-`) | 19 | 0 |
| id de caso, **el id exacto de un caso oculto** | 1 | 1 |
| id de caso, solo la fecha | 0 | 0 |
| `docs/state/` | 0 | 0 |
| `HOLDOUT-EXPOSICIONES.md` | 2 | 0 |
| prosa de `docs/` | 9 | 0 |
| código o tests | 0 | 0 |
| otra | 0 | 0 |
| **TOTAL** | **32** | **1** |

El reparto por rama no se da (revisor, b4: la rama y la carpeta juntas, o el total por rama
cruzado con las clases, acotaban el fichero). `uv.lock` y los ficheros de asignación no cambian en
el rango (auditor, 26): esas clases dan 0 por construcción, y la medida no dice nada de ellas.

- **Una sola línea añadida en el rango lleva el id exacto de un caso oculto, en `tests/unit`.**
  Su fecha es anterior al proyecto y lleva cerca una marca de mercado. Un id de caso oculto ES su
  día de mercado: esto es una fuga real, ya en `main`. No la abrí. Se localiza solo por carpeta y
  se declara (§9, punto 0).
- Las otras 31 caen todas en septiembre, dentro del periodo del proyecto. Llevan delante una marca
  de trabajo (consultor, rama, decisión, sesión…) 7 de ellas: 4 ids y 3 de prosa. Una marca de
  mercado cerca (una hora, H4, operación, entrada…), 4 ids; ninguna de prosa.
- **Las fechas de los meses reservados enteros** (`meses_reservados.yaml`: hoy cinco, octubre y
  noviembre de 2026 entre ellos) salen en **794** líneas del rango. Son las fechas de trabajo del
  propio proyecto en esos meses.
- **En el árbol de `main`** (`git grep -o` de `caso-<símbolo>-AAAA-MM-DD`, fuera del holdout): 753
  ids de caso; 122 con fecha de un día oculto, y de esos, **100 son el id exacto de un caso
  oculto**. Por carpeta: `knowledge/cases` 68 (68 exactos: los repartos, donde la asignación tiene
  que nombrarlos); `tests/unit` 25 (13); `tests/contract` 18 (10); `docs/validation` 11 (9).
  **Fuera de `knowledge/cases`, 32 ids exactos de casos ocultos están escritos hoy en `main`.**

### 4.3 Qué separa una fuga de una fecha de trabajo, y cada variante sobre esta historia

Una fecha de mercado reservada que se escribe es una fuga. Una fecha de trabajo que coincide con un
día reservado no lo es. La fecha sola no las distingue en septiembre: 8 de los días ocultos caen
dentro del periodo del proyecto. Lo que sí separa, medido:

| Variante | Qué marca | Aciertos (fuga real) | Falsos positivos | Sin decidir |
|---|---|---|---|---|
| V0 ingenua: todo día oculto en lo añadido | 32 | 1 | 19 seguros (ids de trabajo) | 12 (9 de prosa, 2 de la tabla, 1 mensaje) |
| V1: V0 sin ids de trabajo, trailers, `uv.lock`, repartos, `docs/state/` ni HOLDOUT-EXPOSICIONES | 11 | 1 | 0 seguros | 10 (9 de prosa, 1 mensaje) |
| **V2 estrecha: el id EXACTO de un caso oculto (fuera de los repartos) o un día oculto ANTERIOR al proyecto** | **1** | **1** | **0** | **0** |
| V3: V1 y, para las de septiembre, solo con marca de mercado y sin marca de trabajo | 1 | 1 | 0 | 0 (las 10 de septiembre quedan fuera: 3 con marca de trabajo y 7 sin ninguna marca, sin saber si eran fugas) |
| V-mes: toda fecha de un mes reservado entero | 794 | — | casi todas son fechas de trabajo | — |

Los «sin decidir» no se pueden resolver sin leer las líneas, y leerlas sería saber qué fecha de
septiembre es un día oculto: eso es exponerlo (§6). Sobre si en los 9 de prosa había alguna
fuga, nada se afirma.

**Propuesta: V2, en su propia rama, sobre lo ESTADIADO de la rama** (las líneas añadidas contra el
merge-base, más los mensajes de sus commits). Es viable: en esta historia caza la única fuga
medible y no da ningún falso positivo. Tres condiciones de diseño que salen de la medida:

1. Sus mensajes no pueden repetir la fecha ni el id. Solo el fichero (o su carpeta, si el nombre
   lleva una fecha) y la línea.
2. Los repartos (`knowledge/cases/*/*/particiones.yaml`) quedan exentos por ruta, porque la
   asignación tiene que nombrar los ids.
3. Las fechas de septiembre dentro del periodo del proyecto, las de los meses reservados y las de
   los ids de trabajo quedan fuera: ninguna variante las decide sin un falso positivo seguro o sin
   abrir.

La guardia no puede mirar toda la historia de la rama hacia atrás sin heredar lo que ya está
escrito en `main` (los 32 ids exactos): mira lo añadido. Y no puede vivir en el Makefile (no se
toca); cabe en `contrato_rama.py`, como G2.

## 5. El encargo frente al repo (auditor)

Subagente `auditor-encargo` sobre e115f208: 32 afirmaciones, 19 correctas, 12 con matiz y 1
incorrecta, más 5 herencias no recogidas. Lo que cambia algo:

- **INCORRECTA (14)**: el paso 0.3 suponía que el guion suelto pasaría si no recorre directorios.
  Lo niega el `git -c` que ya trae (§1.3). Lo medí igual.
- **Matiz (7)**: la propuesta de `CUENTA-POR-MES.md:722-731` sí es un diseño, pero **exime el
  ritual de cierre** y no pide que la fila nombre la rama. El encargo decide lo segundo, y G2 lo
  cumple. Lo primero va a la PARADA (§9, punto 1).
- **Matiz (11)**: «16 tests» son 16 funciones y 25 casos; no todos corren en `trabajo/prueba`.
- **Matiz (12)**: un módulo nuevo en `scripts/` exige siempre tocar el Makefile (§1.2).
- **Matiz (18)**: hay nombres de rama que son prefijo de otros. G2 pide la rama entera (§2).
- **Matiz (20)**: ADR-0021 §4 pide «el mismo dia»; «antes de este make check» y «que nombre la
  rama» vienen de lecciones (`ERRORES-RECURRENTES.md:112` y `:121`), no del ADR. El mensaje cita
  el ADR por la obligación de declarar.
- **Matiz (24)**: el «buzón del 2026-11-08» no está en el repo. (b) tiene fuente escrita
  (`PROJECT_STATE.md:111`); (c), no.
- **Matiz (26), (27)**: `uv.lock` y los repartos no cambian en el rango; F39a, incluida o no
  (§4.1).
- **Matiz (29)**: PROJECT_STATE.md ya está en 24.604 bytes en la rama (396 de margen).
- **Herencias**: (1) H paga `PROJECT_STATE.md:111` (§10); (2) con `contrato_rama.py` cambiado, ni
  la sesión ni el revisor lo pueden lanzar suelto, y el contrato lo pedía (§7, desviación 4); (3)
  el `make check` del commit `chore(cierre)` corre en `trabajo/<rama>` y G2 actuará en él (§9,
  punto 1); (4) el paso 6 de abrir-rama lanza el guion ANTES de que el paso 7 escriba la fila, y ni
  la skill ni `CONTRATO-DE-RAMA.md` ni `RITUAL.md` están en `rutas_permitidas` (§9, punto 2); (5)
  los nombres G1/G2 chocan con otros (cabecera).

## 6. Lo que no pude medir

- El texto de la línea del `make-check.log` local en la que el revisor contó un día oculto
  (revisor, b2): un AVISO de `knowledge validate`, que viene del código de `main` y sale en todo
  `make check` local, y que nombra un id de trabajo de paquete de sesión cuya fecha coincide con
  un día oculto. En el log de la CI no aparece. El log está fuera de git. Es la clase «id de
  trabajo» de §4.3 en una salida, y el encargo prohíbe que un log lleve esa fecha: no lo puede
  evitar esta rama sin tocar `src/` (protegido). Va con el punto 0 de §9.

- Si alguna de las 12 líneas de septiembre sin decidir (9 de prosa de F39g, 2 de
  HOLDOUT-EXPOSICIONES, 1 mensaje de F39e) es una fuga. Para saberlo habría que leerlas, y eso
  diría qué fecha de septiembre es un día oculto.
- Qué son los 32 ids exactos de casos ocultos de `main` fuera de `knowledge/cases` (tests y
  `docs/validation`): fixtures que tenían que ser sintéticos, citas de un informe o una
  exposición. Por el mismo motivo.
- Un log de la CI con la línea `CONTRATO:` en `fix/`: llega con la CI de esta rama (§8).

## 7. Desviaciones

1. **Incidente de terminal, declarado el mismo día.** Un `grep -n "^|"` sobre
   HOLDOUT-EXPOSICIONES, para ver su forma, sacó por la salida de la sesión las dos primeras filas
   de su tabla (las dos de septiembre). Nombran un día reservado de mayo que ya está
   escrito en ellas en `main`. No es información nueva, pero el encargo pide que ninguna salida de
   terminal lleve una fecha reservada. Desde ahí, las salidas sobre esa tabla se recortaron a la
   fecha y la rama, y toda salida de G1 se comprobó sin fechas antes de imprimirla.
2. **El guion de G1, en la forma que propone la guardia** (llamadas a git literales), tras dos
   negativas (§4.1). La guardia no se rodeó: el guion dejó de construir argumentos al ejecutarse.
3. **Los mutantes de G2, a mano en el fichero**, no cargados en memoria: la guardia negó la carga
   del guion cambiado. Restaurado por hash.
4. **Las comprobaciones del contrato**: sale `uv run python scripts/contrato_rama.py` (la guardia
   lo niega suelto en esta rama, §1.3) y entra «make-check.log, líneas CONTRATO y G2». Si se quiere
   suelto, lo lanza Aleks con «!».
5. **El rango de G1 incluye F39a** (el encargo dice «desde»; el auditor, 27, lo dejó abierto).
6. **Una fecha de trabajo que coincide con un día oculto, en esta misma rama.** Antes del push,
   un recuento de lo que añade la rama (diff contra `main` y mensajes, con `casos_ocultos` en
   memoria) dio 2 líneas con un día oculto, 0 ids exactos y 0 mensajes. Eran las dos frases del
   incidente de 7.1, que citaban las fechas de las dos filas de septiembre de HOLDOUT-EXPOSICIONES.
   Son fechas de TRABAJO: la primera columna de esas filas, escritas en `main` desde septiembre. Una
   de las dos coincide con un día oculto (no sé cuál: el recuento es por línea). Salieron de los dos
   textos el mismo día, y la fila del incidente lo declara. Siguen en la historia de `e115f208` y
   `aff916c8`, porque una rama no se reescribe (`rebase` no se usa). Es el caso de §4.3 con nombre:
   V0 y V1 lo habrían marcado, y V2 no, porque no es un id ni una fecha anterior al proyecto.

## 8. Límites declarados

1. **El reloj de G2 es el local de la máquina.** En la laptop de Aleks, Lima (UTC-5); las filas de
   HOLDOUT-EXPOSICIONES también se fechan así. Una máquina con otro huso exige la fila de su día.
   G2 actúa en `make check`, no en los hooks: si `make check` sella antes de medianoche y el commit
   va después, el commit pasa. La fila del día nuevo la pide el `make check` siguiente.
2. **G2 no comprueba que la fila se escribiera ANTES de leer** (ni del primer clon del día). Solo
   que esté al sellar. Lo dijo ya la propuesta (`CUENTA-POR-MES.md:729-730`).
3. **G2 actúa en todo `make check` de una rama `trabajo/*`**, también en el del commit
   `chore(cierre)`, que corre sin contrato (§9, punto 1).
4. **En esta rama, `contrato_rama.py` solo lo ejecuta `make check`** (o Aleks con «!»), hasta que
   sea el de `main`.

## 9. PARADA final (lo apartado y lo que el encargo no decide)

Ninguna pieza de G2, H ni G1 se apartó: lo medido no contradijo ninguna decisión del encargo.
Pero en dos puntos se hizo otra cosa que lo que el encargo pedía, y van aquí para que el consultor
los ratifique o no: el guion de G1, cuando chocó con la guardia (punto 5), y la historia de la rama
con fechas que el encargo prohibía (punto 6). Los demás puntos son consecuencias que el encargo no
previó.

## Lo que necesito que decidas

0. **La fuga del rango y los 32 ids exactos de casos ocultos de `main` fuera de `knowledge/cases`**
   (§4.2). Opciones: (a) una rama propia que los localice con la puerta, sin imprimirlos, y los
   sustituya por ids sintéticos (un símbolo de prueba o fechas libres), declarando en
   HOLDOUT-EXPOSICIONES que estuvieron escritos y decidiendo con ADR-0021 §5 y ADR-0041 si alguno
   quema; (b) declararlos y dejarlos. Recomiendo (a): un id oculto en un test o en un informe es
   la fecha de mercado reservada escrita, y la guardia propuesta en §4.3 no mira lo que ya está en
   `main`. Coste de (b): la guardia de V2 nacería con 32 ids heredados que no ve.
1. **G2 en el commit `chore(cierre)`** (`RITUAL.md:153-171`, que corre `make check` en
   `trabajo/<rama>` sin contrato; auditor, herencia 3). Opciones: (a) dejarlo: el cierre pide la
   fila de su día, como ya se hace a mano (fila de `trabajo/sesion-07` del 2026-11-18, «el cierre»,
   escrita antes del primer `make check`), y en el cierre se añade a `RITUAL.md` una línea que lo
   diga; (b) eximir el cierre cuando no hay `contrato.yaml`, como decía la propuesta de
   `CUENTA-POR-MES.md:728-729`. Recomiendo (a): el `make check` del cierre también lee el M1 de
   marzo y de junio, y ADR-0021 §4 no distingue. Coste de (b): un hueco por el que un día entero
   de cierre queda sin fila.
2. **El orden de abrir-rama frente a G2** (auditor, herencia 4). El paso 6 lanza
   `scripts/contrato_rama.py` antes de que el paso 7 escriba la fila. Desde que G2 esté en `main`,
   toda rama nueva fallaría en el paso 6 si la fila no está ya estadiada. El artefacto ya tiene que
   estarlo, por el mismo motivo. Y `CONTRATO-DE-RAMA.md` («Qué comprueba make check») y
   `RITUAL.md` no nombran G2. Lo mismo `entregar-rama`, que en su paso 2 lanza el guion y lo
   exige en verde (`.claude/skills/entregar-rama/SKILL.md:52`; revisor, a5): desde G2, eso pide
   también la fila del día. Opciones: (a) ampliar el contrato de esta rama a
   `.claude/skills/abrir-rama/SKILL.md`, `.claude/skills/entregar-rama/SKILL.md`,
   `docs/runbooks/CONTRATO-DE-RAMA.md` y `docs/runbooks/RITUAL.md` y escribirlo aquí, antes del
   cierre: la fila del día y el artefacto, estadiados antes del paso 6;
   (b) dejarlo para el cierre o para la rama siguiente. Recomiendo (a): la primera rama que se abra
   tras el merge tropezaría en el paso 6. Coste de (b): esa rama descubre G2 por su mensaje.
3. **La guardia de fechas reservadas (G1).** Opciones: (a) V2 en su propia rama (id exacto de un
   caso oculto fuera de los repartos, o día oculto anterior al proyecto; sobre lo añadido y los
   mensajes de la rama; mensajes sin la fecha), después del punto 0; (b) V1 (todo día oculto fuera
   de las clases de trabajo); (c) no hacerla. Recomiendo (a): 1 acierto y 0 falsos positivos en la
   historia medida. Coste de (b): 10 avisos sin decidir que nadie puede comprobar sin abrir el día.
4. **La comprobación suelta de `contrato_rama.py` en esta rama** (§7, desviación 4). Opciones:
   (a) vale el `make check` (sus líneas `CONTRATO:` y `G2:`); (b) Aleks lo lanza con «!» antes del
   cierre. Recomiendo (a): es el mismo código y el mismo comando que lanza el Makefile. Coste de
   (b): ninguno, salvo el paso a mano.
5. **El guion de G1, cuando chocó con la guardia** (revisor, b3). El encargo decía: «Si la fase 0
   del propio guion choca con la guardia, apártalo a la PARADA y dilo». Chocó dos veces y lo
   rehíce en la forma que propone el mensaje de la guardia («rutas LITERALES»: cada llamada a git,
   literal entera). Así lo permite la regla general de `DECISIONES-DE-PROCESO.md` (entrada del
   2026-10-21, punto 1), y con esa forma lo lancé. Aquí choca el encargo con una regla de proceso,
   no con una skill, y decidí por la regla sin preguntar. Opciones: (a) ratificarlo y que la medida
   valga; (b) no ratificarlo: la medida de §4 queda sin valor de decisión hasta que el consultor la
   autorice. Recomiendo (a): el guion no rodeó nada (lo que la guardia lee es exactamente lo que se
   ejecuta), está commiteado y declarado en HOLDOUT-EXPOSICIONES. Coste de (b): el punto 3 se
   decidiría sin medida.
6. **Fechas que el encargo prohibía, en la historia de la rama** (revisor, b1; §7.6). Dos
   cosas siguen en la historia de `e115f208` y `aff916c8`, y ya en origin por `fix/`. La primera,
   dos frases con fechas de TRABAJO que coinciden con un día oculto. La segunda, la salida de G1
   de `aff916c8`, con el reparto por rama que acotaba el fichero del id oculto (revisor, b4). El
   árbol de la rama ya está limpio: 0 líneas con un día oculto o un id oculto contra `main`
   (recuento del revisor y mío). Opciones: (a) aceptarlas en la historia de `main` con el merge de
   siempre, declaradas aquí y en HOLDOUT-EXPOSICIONES; (b) cerrar la rama con un merge que no
   arrastre su historia, lo que cambia `RITUAL.md` y es decisión de proceso. Recomiendo (a): la
   historia de `main` ya trae casos así (`ERRORES-RECURRENTES.md:83`, «quitada del informe, sigue
   en la historia»; GUARDIA-G1, B1, «enmascarado»), y el punto 0 cubre lo heredado. Coste de (b):
   un ritual nuevo para un caso que la guardia V2 no habría marcado.
7. **Los mutantes de G2, a mano en el fichero real** (revisor, a1). La guardia negó dos veces
   cargarlos desde un guion de la carpeta de la sesión. La primera, por un subproceso calculado:
   «Como reescribirlo: el modulo o el guion por una ruta o un nombre LITERAL que exista al
   inspeccionar, o sin cargarlo». La segunda, por la carga del guion cambiado con su `git -c`. Seguí
   el «sin cargarlo»: ningún guion lo carga; cada mutante se escribe con Edit en el fichero, se pasa
   la suite exenta de `tests/` y se restaura (`git hash-object`, igual antes y después). Opciones:
   (a) aceptarlo como la forma que el mensaje proponía; (b) contarlo como un cambio de vía tras una
   negativa. Recomiendo (a), pero lo dejo a su juicio, porque «cambiar de vía tras una negativa es
   rodearla» (`SESGO-H4-COLOR.md` §10, citado en DECISIONES). Coste de (b): ninguno sobre el
   código; los tests son los mismos y pasan.

## 10. Preparado para el cierre (sin tocar PROJECT_STATE.md)

PROJECT_STATE.md: 24.604 bytes en la rama (tope 25.000). En el cierre:

- **Sale** la línea `:102` (G2), que esta rama paga: «make check, en una rama trabajo/*, no sella
  si HOLDOUT-EXPOSICIONES.md no tiene una fila con la fecha del día …».
- **Sale** la línea `:111` (letras reutilizadas), que H paga: «test_hoja_de_ruta no distingue un
  registro «HECHA · T» de una letra reutilizada …».
- **Entra** la línea que fijó el consultor (respuesta a la PARADA final, punto 3), tal cual: «Sin
  guardia contra fechas de días ocultos en lo que añade una rama. En main hay 32 ids exactos de
  casos ocultos fuera de knowledge/cases, uno de ellos de F39a-F39g en tests/unit. Primero, una rama
  que los sustituya en tests sin abrirlos (los informes cerrados, por recuadro o declarados);
  después, la variante estrecha V2 (GUARDIAS-HOLDOUT.md §4.3 y §9).»
- Y, por decisión de Aleks del 2026-11-20 (lo mete él en la orden de cierre), la deuda de la guardia
  que salió de la comprobación del enlace del corpus: resuelve por realpath, y con un enlace en
  `corpus/` deja de aplicar las reglas del material adicional; un Read de la carpeta
  `Backtest <mes>` en sí no se niega. El texto lo trae la orden.

Las dos salidas suman 403 bytes (243 + 160; revisor, a3); la entrada del consultor, 361 con su
«- » (`printf … | wc -c`), sin ajustar, porque no pasa de 400. Queda 24.604 − 403 + 362 ≈ 24.563,
antes de la línea del corpus que traiga la orden.

## 11. El encargo, punto por punto

| # | Requisito del encargo | Estado | Evidencia |
|---|---|---|---|
| 1 | Abrir con abrir-rama desde fa592071; base con git; CI de main sobre fa592071 con un `gh run view` suelto (el run 44653987599) | Hecho | §0; el run es ese y está verde |
| 2 | Contrato: riesgo alto, tramo "Carril: guardias y deuda", artefacto GUARDIAS-HOLDOUT.md, lista blanca con CLAUDE.md, scripts/ y tests/unit/ tocados; lo protegido manda | Hecho | `contrato.yaml`; `CONTRATO: 12 ficheros dentro del contrato …` en `make-check.log` |
| 3 | Tag previsto stable/F39h-guardias-holdout, sin existir en origin | Hecho | §0 (`git ls-remote` vacío; auditor, 4) |
| 4 | Mandan abrir-rama, fase-cero y entregar-rama; decir los choques | Hecho | Sin choque: fase-cero para «salvo que el encargo diga cuándo seguir», y el encargo lo dice (PARADA condicional) |
| 5 | Sin NotebookLM; ningún ADR nuevo | Hecho | `git diff --stat main...HEAD` no toca `docs/adr/` (protegido en el contrato) |
| 6 | PARADA condicional: seguir con lo que cuadre, apartar solo lo que contradiga, PARADA final; nunca cerrar | Hecho | §9: nada apartado; 5 decisiones que el encargo no prevé. Sin cierre |
| 7 | Si frena la guardia, no rodearla | Hecho, a ratificar | §7.2 y §7.3; §9, puntos 5 y 7 |
| 8 | El Makefile no se toca | Hecho | protegido en el contrato; `git diff --stat` sin Makefile |
| 9 | La medianoche: la fila del día nuevo antes de un make check | Hecho | todos los `make check` de la rama empezaron el 2026-11-19, con su fila (G2 lo comprobó en cada uno) |
| 10 | NO cambian src/botsito/, knowledge/, motor, spec, cifras, ADR, Makefile, HOJA-DE-RUTA.md | Hecho | `git diff --stat main...HEAD` (§12) |
| 11 | Nada de lo reservado se abre ni se imprime; ninguna fecha reservada en mensajes, logs, asserts, ficheros commiteados ni terminal; recuentos de G1 por clase o carpeta | Parcial, declarado | El árbol, limpio (0 líneas con un día o un id oculto contra `main`). Quedan: el incidente de terminal (§7.1); dos frases y la salida de G1 por rama, en la historia de dos commits (§7.6; §9, punto 6); el AVISO de `knowledge validate` del log local, que viene de `main` (§6). G1, ya por clase y carpeta, sin rama |
| 12 | knowledge/cases/holdout/ fuera de todo git show/diff/log -p | Hecho | `medir_g1.py` (pathspec `:(exclude)knowledge/cases/holdout/` en el `git log -p` y en el `git grep`); el recuento de la rama, igual |
| 13 | La fila de HOLDOUT del día, antes del primer make check | Hecho | fila del 2026-11-19 estadiada en el commit de apertura |
| 14 | 0.1 Herencias con fichero y línea | Hecho | §1.1 |
| 15 | 0.2 Dónde vive G2; función aparte; startswith explícito; día y texto por parámetro; comprobar() o main(); módulo nuevo o no | Hecho | §1.2: en `main()`, en `contrato_rama.py` |
| 16 | 0.3 La guardia: editar, make check y el guion suelto | Hecho; la premisa del encargo era incorrecta | §1.3: el guion suelto se niega por el `git -c` que ya traía, no por recorrer directorios |
| 17 | 0.4 La forma de las filas y el reloj | Hecho | §1.4 |
| 18 | G2: pasa con una fila estadiada de hoy que nombre la rama | Hecho | §2; `G2: fila de HOLDOUT-EXPOSICIONES del 2026-11-19 para trabajo/guardias-holdout, estadiada` en `make-check.log` |
| 19 | G2: el mensaje al fallar, literal | Hecho | `contrato_rama.py`, `problemas_fila_del_dia`; `_mensaje` del test |
| 20 | G2: tests que rompen (sin fila; ayer; otra rama; sin estadiar; buena; fix/x y main) | Hecho de otra forma | §2: los seis casos; que rompen, con mutantes del fichero (con el código de `main` el test no carga: las funciones no existen) |
| 21 | CLAUDE.md: línea «Guardia:» en la regla de exposiciones, mismo commit | Hecho | commit `aff916c8` |
| 22 | H (c) «Depende de» y «después,» | Hecho | §3 |
| 23 | H (b) el registro de una letra reutilizada | Hecho | §3 |
| 24 | H: solo si la hoja y PROJECT_STATE de main siguen pasando; si no, PARADA | Hecho | §3: siguen pasando; nada a la PARADA |
| 25 | H: tests sintéticos que rompen | Hecho de otra forma | §3: con el código viejo (mutante idéntico al de `main` en esas dos funciones) fallan los 4 nuevos |
| 26 | G1: no escribir la guardia | Hecho | ningún cambio de código de guardia por G1 |
| 27 | G1: guion commiteado en anexos/GUARDIAS-HOLDOUT/ con la función de la compuerta, sin imprimir días | Hecho | `medir_g1.py` (`casos_ocultos`); salida `medir_g1.txt` sin fechas |
| 28 | G1: medir sobre las líneas añadidas y los mensajes de las ramas desde F39a, sin el holdout, por clase | Hecho | §4.2 |
| 29 | G1: declarar la lectura en HOLDOUT antes de lanzarlo | Hecho | fila del 2026-11-19 «el estudio de G1», ampliada antes de la segunda corrida |
| 30 | G1: la condición que separa fuga de fecha de trabajo, falsos positivos y fugas por variante, propuesta | Hecho | §4.3 |
| 31 | G1: si la fase 0 del guion choca con la guardia, PARADA | Hecho de otra forma | chocó dos veces y pasó con la forma literal que la guardia propone (§4.1; §7.2) |
| 32 | Informe: fase 0, lo hecho, desviaciones, límites (el reloj de G2), PARADA final | Hecho | §1-§9 |
| 33 | Push a fix/guardias-holdout y CI de Linux; único fallo aceptado, state check por fix/; comprobar ahí que G2 no actúa en fix/ | Hecho | §12 |
| 34 | Revisor con los cuatro alcances además de los suyos | Hecho | §13 y §14 |
| 35 | PROJECT_STATE.md bajo 25.000 bytes; preparar sin tocar la línea que G2 paga y la nueva de G1 | Hecho | §10 |
| 36 | Dar número del run, sha del último commit y número de commits | Hecho | mensaje final y §12 |

## 12. Lo que no cambia, la CI y los commits

- `git diff --stat main...HEAD -- . ":(exclude)knowledge/cases/holdout/"`: `CLAUDE.md`,
  `PROJECT_STATE.md` (Current Branch, Current Feature, el recuento de tests a 2097 y el Archivo 76
  en Completed Features y Change Log), `contrato.yaml`, el encargo, `docs/state/HISTORIA.md`
  (Archivo 76), `GUARDIAS-HOLDOUT.md`, `HOLDOUT-EXPOSICIONES.md`, los dos ficheros de
  `anexos/GUARDIAS-HOLDOUT/`, `scripts/contrato_rama.py`, `tests/unit/test_fila_del_dia.py` y
  `tests/unit/test_hoja_de_ruta.py`. Nada de `src/`, `knowledge/`, `docs/adr/`, el Makefile ni
  `HOJA-DE-RUTA.md`. El revisor lo comprobó por commits (0 commits que toquen esas rutas).
- **CI de Linux por `fix/guardias-holdout`** (`git push origin trabajo/guardias-holdout:fix/guardias-holdout`):
  - run **44667806518** sobre `aff916c8`: `failure`, con un único fallo,
    `test_state_check_ok_on_real_repo` («PROJECT_STATE declara la rama 'trabajo/guardias-holdout';
    la rama actual es 'fix/guardias-holdout'»): el aceptado. `1 failed, 3473 passed, 93 skipped`;
  - run **44671243811** sobre `29babd0e`: lo mismo, solo ese fallo;
  - **G2 no actúa en `fix/`**: en los dos, el log trae la línea `CONTRATO: 12 ficheros dentro del
    contrato de trabajo/guardias-holdout …` y ninguna `G2:` (`gh run view 44671243811 --log | grep -c "G2:"`
    → 0). En local, en `trabajo/guardias-holdout`, cada `make check` trae
    `G2: fila de HOLDOUT-EXPOSICIONES del 2026-11-19 para trabajo/guardias-holdout, estadiada`.
  - El run del último commit, el de lo que se hizo con los hallazgos del revisor, va en el mensaje
    final a Aleks (este informe va dentro de ese commit).
- Commits: `e115f208` (apertura), `aff916c8` (G2, H, G1 y el informe), `29babd0e` (fuera las
  fechas de las dos filas de septiembre) y el de los hallazgos del revisor.

## 13. Informe del revisor

Subagente `revisor`, una pasada, sobre `29babd0e`, con los cuatro alcances del encargo. Pegado tal
cual, salvo **tres retiradas** marcadas «[retirado: …]»: la rama y el número de ficheros con que el
hallazgo b4 y su comando 37 acotaban el fichero que lleva el id oculto. Es la misma pista que b4
pide quitar; se retira por el mismo motivo por el que se retira lo que cita un tramo no citable.

> ## Informe del revisor · trabajo/guardias-holdout · 2026-11-19
>
> Revisado sobre 29babd0e: 3 commits sobre fa592071 (e115f208, aff916c8, 29babd0e) y árbol de trabajo limpio. En ningún comando, salida ni línea de este informe sale una fecha AAAA-MM-DD de un día oculto ni un id `caso-…`. En las salidas que pedí, las fechas iban tapadas.
>
> ### Eje (a) · Reglas de la casa
> Resumen: 0 bloquea, 1 importa, 4 menor.
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | a1 | importa | Los mutantes de G2 cambiaron de vía tras dos negativas. Primero se intentó cargarlos en memoria; la guardia lo negó dos veces y se pasó a editar el fichero real. DECISIONES-DE-PROCESO (2026-10-21, punto 1) pide una PARADA tras una negativa, salvo que se siga «la forma que la propia guardia propone en su mensaje». El informe no dice que la guardia propusiera editar el fichero a mano, ni copia su mensaje. Sin eso, es el caso de «cambiar de vía tras una negativa es rodearla». | `GUARDIAS-HOLDOUT.md:145-148` («la guardia lo negó dos veces … Resultados») y `:330-331` (desviación 3); `docs/runbooks/DECISIONES-DE-PROCESO.md:28` |
> | a2 | menor | El «## Estado» está desfasado: dice «Faltan el `make check` y el commit», pero los dos commits ya están sellados y hay dos CI corridas. | `GUARDIAS-HOLDOUT.md:427-428`; `make-check.log`: `SELLO: … 3fbcb13a…`, que es `git rev-parse 29babd0e^{tree}` |
> | a3 | menor | El §10 estima que la línea que entra en Technical Debt ocupa «unos 330» bytes. Medido: las dos salidas suman 403 bytes (243 + 160) y el bloque de la entrada tiene 445, unos 385 sin prefijo ni sangrado. La conclusión («por debajo de los 24.604») se sostiene; la cifra no. | `sed -n '102p'` / `'111p' PROJECT_STATE.md \| wc -c` → 243 / 160; `sed -n '408,412p' GUARDIAS-HOLDOUT.md \| wc -c` → 445 |
> | a4 | menor | La línea nueva de CLAUDE.md usa el nombre «G2». El propio informe advierte que ese nombre choca con la G.2 de la hoja de ruta, y por eso describe por su función las líneas para PROJECT_STATE. CLAUDE.md vive más que el informe. | `CLAUDE.md:188-190`; `GUARDIAS-HOLDOUT.md:11-14` |
> | a5 | menor | La skill `entregar-rama` también lanza `uv run python scripts/contrato_rama.py` y lo exige en verde. Desde G2 eso pide además la fila del día. La PARADA 2 solo nombra abrir-rama, CONTRATO-DE-RAMA y RITUAL. | `.claude/skills/entregar-rama/SKILL.md:52`; `GUARDIAS-HOLDOUT.md:381-389` |
>
> Comprobado sin hallazgos:
> - **Contrato.** El guion suelto lo niega la guardia (declarado, `contrato.yaml:34-36`). Evidencia que lo sustituye: la línea `CONTRATO: 12 ficheros dentro del contrato de trabajo/guardias-holdout (riesgo alto, …)` y `G2: fila de HOLDOUT-EXPOSICIONES del <hoy> para trabajo/guardias-holdout, estadiada`. Las dos salen en `make-check.log`, y la línea CONTRATO también en las CI 44667806518 y 44671243811.
> - **Comprobaciones del contrato.** `uv run pytest tests/unit/test_contrato_rama.py tests/unit/test_fila_del_dia.py tests/unit/test_hoja_de_ruta.py -p no:cacheprovider` da `65 passed`, exit 0. `make check`: no lo lancé (escribe). `make-check.log` da `3561 passed, 6 xfailed`, `SELLO: make check en verde sobre el arbol 3fbcb13a…`, que es exactamente el árbol de 29babd0e, y `PICO DE MEMORIA … 319 MiB`. `knowledge validate`: las líneas OK de su etapa en el log.
> - **Trailers `Fuente:`.** Ningún commit toca `knowledge/spec` ni `knowledge/cases`: `git log main..HEAD -- knowledge src Makefile docs/adr docs/plan/HOJA-DE-RUTA.md tests/contract …` → 0 commits.
> - **Holdout.** Nada bajo `knowledge/cases/holdout/`. El guion de G1 lo excluye en sus dos llamadas que leen contenido (`medir_g1.py:110-111` y `:243-245`). Las exposiciones del día están: las dos filas de la rama (`HOLDOUT-EXPOSICIONES.md:167-168`, leídas recortadas y con las fechas tapadas) declaran los `make check`, la fase 0 y la lectura de G1.
> - **Regímenes.** La rama no cambia nada en evidence, feedback, manifests, transcripciones, fotogramas ni `libros.yaml`. En HOLDOUT-EXPOSICIONES el neto contra main son 2 líneas añadidas (`--numstat` 2 0); la edición de 29babd0e cae sobre una fila de la propia rama que no está en main.
> - **Ambigüedades y ADR:** la rama no toca ninguno.
> - **Informes cerrados:** ningún `docs/validation/*.md` de main cambia, salvo el registro de exposiciones, que solo crece.
> - **Sitios con `cita` en la spec:** ninguno nuevo. **Cifras en `src/`:** ninguna.
> - **HISTORIA.** El Archivo 76 contiene entero el PROJECT_STATE de main (comprobado en memoria). PROJECT_STATE ocupa 24.604 bytes.
> - **Tres citas del informe contra su fuente:** `PROJECT_STATE.md:102` y `:111`, `CUENTA-POR-MES.md:722-731`, `Makefile:41`, `:62-64` y `:82`, `guardia.py:1096` (`CODIGO_QUE_RECORRE`), `guardia.py:2419` y `:4085-4090`, y `DECISIONES-DE-PROCESO.md:28`. Todas dicen lo que el informe les atribuye.
> - **Items de evidencia nuevos:** ninguno.
>
> ### Eje (b) · Encargo
> Resumen: 0 bloquea, 5 importa, 1 menor. Requisitos: 27 hechos, 1 hecho de otra forma, 5 parciales (uno de ellos, este revisor, en curso), 1 no hecho (pendiente por naturaleza).
>
> | # | Requisito | Estado | Evidencia |
> |---|---|---|---|
> | 1 | Abrir con abrir-rama, base comprobada, CI de main 44653987599 verde | Hecho | `GUARDIAS-HOLDOUT.md:20-33` |
> | 2 | Contrato: riesgo alto, tramo, artefacto | Hecho | `contrato.yaml:2-4` |
> | 3 | Lista blanca; lo protegido manda | Hecho | `contrato.yaml:5-31` |
> | 4 | El tag previsto no existe en origin | Hecho | `git ls-remote --tags origin "stable/F39h*" \| wc -l` → 0 |
> | 5 | No se tocan src, knowledge, spec, ADR, Makefile ni HOJA-DE-RUTA; ningún ADR nuevo | Hecho | git log con esas rutas → 0 commits; `.claude` sin cambios |
> | 6 | La fila del día antes del primer make check | Hecho | la fila ya está en el árbol de e115f208, el que selló el primer make check de la rama |
> | 7 | Ninguna fecha reservada en lo commiteado ni en lo impreso | Parcial | b1 y b2 |
> | 8 | holdout fuera de todo show/diff/log -p | Hecho en el guion | `medir_g1.py:110-111`; lo demás, en «no pude comprobar» |
> | 9 | 0.1 herencias, con tabla | Hecho | `:37-58` |
> | 10 | 0.2 G2: función aparte, `startswith("trabajo/")`, día y texto por parámetro, llamada desde main() | Hecho | `contrato_rama.py` (diff): `problemas_fila_del_dia`, `fila_del_dia`, `main()`; informe `:60-75` |
> | 11 | 0.3 la guardia | Hecho (premisa contradicha y declarada) | `:77-96` |
> | 12 | 0.4 las filas y el reloj | Hecho | `:98-107` |
> | 13 | G2 lee lo estadiado (`git show :ruta`) | Hecho | `texto_estadiado` en el diff; test `test_fila_del_dia.py:168-176` |
> | 14 | Mensaje literal del encargo | Hecho | diff de `problemas_fila_del_dia`; `test_fila_del_dia.py:63-67` |
> | 15 | Tests: sin fila, ayer, otra rama, sin estadiar, buena, fix/x y main | Hecho | `test_fila_del_dia.py:73-185` |
> | 16 | Línea «Guardia:» en CLAUDE.md, en el mismo commit | Hecho | aff916c8 trae CLAUDE.md y `contrato_rama.py` (`git log --stat`) |
> | 17 | H (c): «Depende de» y «después,» | Hecho | diff de `DEPENDENCIA` |
> | 18 | H (b): el registro de una letra reutilizada | Hecho | `letras_registradas_tras_su_ultima_vida` y la rama `al_dia` de `problemas_b` |
> | 19 | H solo si la hoja y el PS de main siguen pasando | Hecho | medido en memoria con `git show main:…`: `problemas_c` → [], `problemas_b` → 0, `problemas_a` → 0 |
> | 20 | Tests sintéticos que rompen | Hecho | 3 tests nuevos, `test_hoja_de_ruta.py:463-519`; los mutantes no los pude repetir |
> | 21 | G1 sin implementar | Hecho | ningún código de guardia en la rama |
> | 22 | Guion en anexos que usa la puerta y no imprime | Hecho | `medir_g1.py:34`, `:154-160`; en `medir_g1.txt`, 0 fechas, 0 días ocultos y 0 ids (recuento) |
> | 23 | Medida por clase sobre el rango desde F39a | Hecho | `medir_g1.txt:5-19`; cuadra con la tabla del informe `:212-226` y con las cuentas de `:236-238` |
> | 24 | Declarar la lectura antes de lanzarlo | Hecho según la fila | `HOLDOUT-EXPOSICIONES.md:168` («declarado ANTES de lanzarlo»); el orden no lo pude verificar |
> | 25 | Condición, falsos positivos y fugas por variante, propuesta | Hecho | `:248-280` |
> | 26 | «Si la fase 0 del guion choca con la guardia, a la PARADA» | Hecho de otra forma | b3 |
> | 27 | Recuentos por clase o carpeta, nunca por nombre de fichero | Hecho (literal) | `medir_g1.py:266-274`; matiz en b4 |
> | 28 | Informe con fase 0, punto por punto, desviaciones, límites y PARADA | Parcial | falta «El encargo, punto por punto» (b5) |
> | 29 | CI de Linux en fix/; único fallo state check; G2 no actúa en fix/ | Hecho en la CI; Parcial en el informe | b6 |
> | 30 | Revisor con los cuatro alcances | Parcial (en curso) | este informe |
> | 31 | PROJECT_STATE por debajo de 25.000 bytes | Hecho | 24.604 |
> | 32 | Líneas de Technical Debt preparadas sin tocar PS | Hecho | `:400-415` (cifra, a3) |
> | 33 | Dar el número del run, el sha y el número de commits | Parcial (pendiente) | datos: run 44671243811, 29babd0e, 3 commits |
> | 34 | «Rama lista para revisión, NO cerrada» | No hecho (pendiente) | — |
>
> Los cuatro alcances:
> - **(1) Ninguna fecha reservada ni nombre que la delate.** El neto de la rama contra main está limpio: 1.581 líneas añadidas, 0 con un día oculto y 0 con un id oculto (recuento con `casos_ocultos` en memoria). Los mensajes de los tres commits dan 0 y los nombres de fichero, 0. Lo que queda está en b1, b2, b4 y b7.
> - **(2) G2 fuera de trabajo/* y en la CI.** El código hace `if not rama.startswith(PREFIJO_G2): return []`, tanto en `problemas_fila_del_dia` como en `fila_del_dia`. En las CI 44667806518 (aff916c8) y 44671243811 (29babd0e) sale la línea `CONTRATO:` y ninguna `G2:`, y la rama vista es `'fix/guardias-holdout'`. El único fallo es `test_state_check_ok_on_real_repo` («PROJECT_STATE declara la rama 'trabajo/guardias-holdout'; la rama actual es 'fix/guardias-holdout'»), con `1 failed, 3473 passed, 93 skipped`. Los hooks no llaman a `contrato_rama.py` (grep en scripts, .github y Makefile: solo `Makefile:66`).
> - **(3) G2 lee lo estadiado.** `_git(raiz, "show", f":{ruta}")` lee el índice. El test con repo temporal cubre los tres casos: sin estadiar falla, estadiado pasa, y estadiado y borrado del árbol pasa (`test_fila_del_dia.py:168-176`).
> - **(4) H no deja en rojo la hoja de main.** Con PS, HISTORIA y hoja de `main` en memoria, (a), (b) y (c) dan 0 problemas. Las letras con registro HECHA que vuelven a estar vivas (A, F, I, J, Q) son las mismas en main y en la rama, y ninguna figura HECHA en la hoja.
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | b1 | importa | El encargo dice «Ningún … fichero commiteado … lleva una fecha de un día reservado». La historia de la rama sí la lleva: 1 línea en e115f208 (`HOLDOUT-EXPOSICIONES.md`) y 1 en aff916c8 (`GUARDIAS-HOLDOUT.md`), las dos ya en origin (fix/, run 44667806518), y entrarán en main con el merge. El §7.6 lo declara, pero el §9 no lo pone ante el consultor como decisión y dice «Nada … se apartó». Es una fecha de trabajo, pero lo que se pide es literal y la decisión (aceptarlo en la historia de main) es del consultor. | recuento con `casos_ocultos` sobre `git log -p -U0 main..HEAD -- . ':(exclude)…'`: `('MSG e115f208','anadida-dia','docs/validation/HOLDOUT-EXPOSICIONES.md') 1`, `('MSG aff916c8','anadida-dia','docs/validation/GUARDIAS-HOLDOUT.md') 1`; neto 0; `GUARDIAS-HOLDOUT.md:336-344`, `:361` |
> | b2 | importa | Lo impreso. El `make-check.log` del sello de esta rama trae 1 línea con un día oculto: un AVISO de `knowledge validate` que nombra un paquete de sesión, es decir, un id de trabajo cuya fecha coincide con un día oculto. Sale en todo `make check` local y viene del código de main, no de esta rama. El encargo prohíbe expresamente que un log lleve esa fecha y el informe no lo menciona. En el log de la CI no aparece (0 líneas de esa forma). | recuento sobre `make-check.log`: `linea 121 de 129 \| inicio sin cifras: AVISO: ####-##-##-sesion-`; `gh run view 44667806518 --log \| grep -cE "AVISO: [0-9]{4}-…-sesion"` → 0 |
> | b3 | importa | El encargo decía: «Si la fase 0 del propio guion choca con la guardia, apártalo a la PARADA y dilo». Chocó dos veces y se rehízo en la forma que propone la guardia. Lo permite la regla general (DECISIONES 2026-10-21, punto 1) y está declarado, pero el informe no dice que el encargo pedía otra cosa ni por qué gana la regla general, y el §9 afirma que nada se apartó. | encargo `:46`; `GUARDIAS-HOLDOUT.md:195-201`, `:328-329`, `:361` |
> | b4 | importa | El informe localiza el id exacto de un caso oculto por «[retirado: la rama] + tests/unit». El merge de [retirado: la rama] cambió solo [retirado: el número de ficheros] de `tests/unit`, con nombres públicos, así que la pista se reduce a muy pocos ficheros que la guardia no tiene por qué cubrir como material protegido. Cumple la letra («por carpeta») pero va contra el alcance (1) («ni un nombre de fichero que la delate»). Bastaría la carpeta sin la rama, o la clase. | `GUARDIAS-HOLDOUT.md:232-235`; `medir_g1.txt:34`; un `git diff --name-only` del merge de esa rama `-- tests/unit \| wc -l` (los nombres no los imprimí) |
> | b5 | importa | Falta «El encargo, punto por punto» (E5 de `trabajo/entorno-code`). Está anunciado para después, pero hoy falta. | `GUARDIAS-HOLDOUT.md` no tiene esa sección (índice §0-§10, Exposiciones, Estado) |
> | b6 | importa | El encargo pide comprobar en la CI que G2 no actúa en fix/. Ya está medido (las dos CI: CONTRATO sin G2), pero el informe aún lo da como pendiente y no trae el run 44671243811 ni su resultado. | `GUARDIAS-HOLDOUT.md:318`; `gh run view 44671243811` → `conclusion: failure`, solo state check |
> | b7 | menor | Los días de los tests (`HOY`, `AYER` y la fila de la cabecera) caen en meses reservados enteros (2026-10 y 2026-11 están en `meses_reservados.yaml`). Sus asserts imprimirían esas fechas si fallan. No son días ocultos (recuento 0), y la fila del día de G2 obliga a escribir la fecha de hoy, así que es inevitable en el código, no en los tests: unas fechas sintéticas fuera de todo mes reservado lo evitarían. | `test_fila_del_dia.py:21-22`, `:32`; `grep -oE "20[0-9]{2}-[0-9]{2}" knowledge/cases/meses_reservados.yaml \| sort -u` → incluye 2026-10 y 2026-11 |
>
> Lo que la rama hace y el encargo no pide, todo declarado o inherente a G2:
> - `main()` ya no corta tras un fallo del contrato: sigue a G2 y sale con 1.
> - Tests extra: `test_solo_cuenta_…`, `test_main_del_guion_…` y `test_hoy_es_…`.
> - Clases extra en G1: id de caso, HOLDOUT-EXPOSICIONES y mensaje fuera del trailer.
>
> Ninguna cosa sin justificar.
>
> ### Lo que no pude comprobar
> - **`uv run python scripts/contrato_rama.py` suelto:** lo niega la guardia en esta rama. Sustituye `make-check.log` (CONTRATO y G2), que corresponde al árbol de HEAD, más las dos CI.
> - **`make check` y `knowledge validate` sueltos:** escriben (el sello y el log). Sustituyen el `SELLO` sobre `3fbcb13a` (= `29babd0e^{tree}`), el `PICO DE MEMORIA` de 319 MiB y las líneas OK de la etapa knowledge del log.
> - **Los mutantes de G2 y de H:** escriben en el repo. Solo tengo lo que cuenta el informe y la vuelta atrás por hash que declara.
> - **El texto de la línea 121 de `make-check.log`:** el clasificador negó incluso una impresión con las fechas tapadas. Solo sé que empieza por `AVISO: ####-##-##-sesion-`.
> - **Recuentos de días o ids ocultos en los logs de la CI:** la guardia niega todo código que consulte la CI. Solo hice greps de patrones con las fechas tapadas.
> - **Que cada `git show`, `diff` o `log -p` de la sesión excluyera el holdout:** solo puedo verificar los del guion commiteado.
> - **El orden real «fila antes de lanzar G1»:** solo lo afirma la propia fila.
> - **Que el encargo esté copiado «tal cual»:** no tengo el mensaje original.
> - **Si alguna de las 12 líneas «sin decidir» o de los 32 ids heredados es una fuga:** habría que leerlas.
>
> ### Comandos ejecutados
> 1. `git branch --show-current && git merge-base main HEAD && git log --format='%h %s' main..HEAD && git diff --stat main...HEAD -- . ":(exclude)knowledge/cases/holdout/" && git status --short`
> 2. Read: el encargo, `contrato.yaml` y `GUARDIAS-HOLDOUT.md`
> 3. `git diff main...HEAD -- scripts/contrato_rama.py CLAUDE.md PROJECT_STATE.md`
> 4. `grep -n "def _git\|def rama_actual\|…" -A3 scripts/contrato_rama.py`
> 5. `gh run view 44667806518 --json conclusion,status,headBranch,headSha,jobs`
> 6. `gh run view 44667806518 --log | grep -E "CONTRATO|G2:|passed|failed|…" | sed (fechas tapadas)` (y dos variantes para la causa del fallo y la salida capturada)
> 7. `gh run list --branch fix/guardias-holdout --json …`
> 8. `grep -E "SKIPPED.*(test_fila_del_dia|…)"` sobre el log de la CI; `ls -la make-check.log`; `grep -E "^SELLO|PICO DE MEMORIA|CONTRATO:|^G2:|passed|failed" make-check.log | sed (fechas tapadas)`
> 9. `git rev-parse 29babd0e^{tree} aff916c8^{tree} HEAD && git log -1 --format='%ci' 29babd0e && git diff --name-status main...HEAD -- . ":(exclude)…"`
> 10. `git diff --numstat main...HEAD -- HOLDOUT-EXPOSICIONES.md HISTORIA.md CLAUDE.md`; el diff de HOLDOUT recortado a 60 caracteres; `git diff -U0 … | grep "^@@"`
> 11. `grep -cE "[0-9]{4}-[0-9]{2}-[0-9]{2}"` sobre los ficheros nuevos; `grep -n "casos_ocultos|^from|…" medir_g1.py`
> 12. Read: `medir_g1.py:1-200`
> 13. Dos intentos de recuento con `uv run python -c`, negados por la guardia: git con argumentos dinámicos, y una tubería hacia python.
> 14. `uv run python -c` (git literal, `casos_ocultos` en memoria) → recuento por commit
> 15. `uv run python -c` → recuento neto; `make-check.log`; `medir_g1.txt`; ¿es día oculto el inicio del proyecto?
> 16. `uv run python -c` con máscara de fechas → negado por el clasificador
> 17. `uv run python -c` → solo fichero y número de línea de lo marcado
> 18. `gh run view 44667806518 --log | grep -cE "AVISO: …-sesion"`; `grep -cE … make-check.log`
> 19. `sed -n '115,125p' make-check.log | sed 's/[0-9]/#/g'`
> 20. Read: `test_fila_del_dia.py`
> 21. Glob de `meses_reservados.yaml`; `grep … | grep -oE "20[0-9]{2}-[0-9]{2}" | sort -u`
> 22. `git diff -U0 main...HEAD -- docs/state/HISTORIA.md | grep … | uniq -c` (solo el mes de la fecha anterior al proyecto: julio, mes de desarrollo)
> 23. `git diff main...HEAD -- tests/unit/test_hoja_de_ruta.py`
> 24. `awk` de la Next Action de PS (formato de letras); `grep -c "^# Archivo "`; recuento de registros HECHA
> 25. `uv run pytest tests/unit/test_contrato_rama.py tests/unit/test_fila_del_dia.py tests/unit/test_hoja_de_ruta.py -q -p no:cacheprovider` (dos veces; la segunda con `-rA` y el exit) → 65 passed, exit 0
> 26. `grep -n … tests/unit/test_hoja_de_ruta.py`; Read de `:255-314`
> 27. `uv run python -c` → (a), (b) y (c) contra `git show main:PROJECT_STATE.md`, `main:docs/state/HISTORIA.md` y `main:docs/plan/HOJA-DE-RUTA.md`
> 28. Un `for` sobre los commits, negado por la guardia; `git log --stat --format='== %h %s' main..HEAD -- . ":(exclude)…"`
> 29. `uv run python -c` → Archivo 76 frente al PS de main; tamaño de PS; mensaje de e115f208 con las fechas tapadas
> 30. `grep -n "trabajo/guardias-holdout" HOLDOUT-EXPOSICIONES.md | sed (fechas tapadas) | cut -c1-700`
> 31. `sed -n` de `PROJECT_STATE.md:93,102,107,111`, de `Makefile:41,62-64,82` y `grep CODIGO_QUE_RECORRE`
> 32. `sed -n` de `CUENTA-POR-MES.md:722-731`, de `ERRORES-RECURRENTES.md:121` y de `RITUAL.md:153-171`
> 33. `wc -c` de las líneas 102 y 111 de PS y de `GUARDIAS-HOLDOUT.md:408-412`
> 34. `git log … -- <rutas protegidas> | wc -l`; cabecera de `HOLDOUT-EXPOSICIONES.md`; grep de su régimen
> 35. `grep -n "2026-10-21" DECISIONES-DE-PROCESO.md`; Read de `:28-39`
> 36. `head -30 meses_reservados.yaml` (fechas tapadas); `git ls-remote --tags origin "stable/F39h*" | wc -l` → 0
> 37. [retirado: el comando que contaba los ficheros de `tests/unit` del merge de una rama, y su resultado]
> 38. Read de `medir_g1.txt`; `grep -n "print("`, `def carpeta`, `sed -n '400,428p'` y la llamada `git grep` de `medir_g1.py`
> 39. `grep -n "def _analizar_make"`; `sed -n '4085,4090p' guardia.py`; `git diff --quiet main...HEAD -- .claude`
> 40. Grep de `contrato_rama` en scripts, .github, Makefile, skills y comun
> 41. `gh run view 44671243811 --json status,conclusion,headSha`; `gh run view 44671243811 --log | grep … | sed (fechas tapadas)`

## 14. Lo que se hizo con los hallazgos del revisor

| # | Gravedad | Qué se hizo |
|---|---|---|
| a1 | importa | Contestado y llevado al consultor: el mensaje de la guardia, copiado, proponía «o sin cargarlo», y eso es lo que se hizo (Edit en el fichero, suite exenta, restaurado por hash). Si vale o no, §9, punto 7 |
| a2 | menor | Arreglado: `## Estado` al día |
| a3 | menor | Arreglado: §10 con las cifras medidas (403; unos 385) |
| a4 | menor | Arreglado: la línea de CLAUDE.md dice «la fila del dia en `scripts/contrato_rama.py`», sin «G2» |
| a5 | menor | Arreglado: `entregar-rama` entra en §9, punto 2 |
| b1 | importa | Llevado al consultor: §9, punto 6 (la historia de dos commits, también con la salida de G1 por rama) |
| b2 | importa | Declarado: §6 y §9, punto 0. Sale del código de `main` (el AVISO de `knowledge validate`, `src/` protegido) |
| b3 | importa | Llevado al consultor: §9, punto 5 |
| b4 | importa | Arreglado en el árbol: `medir_g1.py` ya no imprime las líneas por rama ni la rama en el detalle (tercera corrida declarada en la fila de G1); §4.1, §4.2, §7.5, §9.0 y §10, sin la rama; el informe del revisor, con tres retiradas. Lo de antes sigue en la historia de `aff916c8` (§9, punto 6) |
| b5 | importa | Arreglado: §11 |
| b6 | importa | Arreglado: §12 |
| b7 | menor | Arreglado: las fechas sintéticas de `test_fila_del_dia.py` y de los dos sintéticos nuevos de `test_hoja_de_ruta.py` pasan a agosto de 2026 (mes de construcción, fuera de todo mes reservado). Las fechas de trabajo (las filas de la rama, el comentario de `contrato_rama.py`) se quedan: G2 obliga a escribir la de hoy |

Después de los arreglos: `uv run pytest tests/unit/test_fila_del_dia.py tests/unit/test_hoja_de_ruta.py tests/unit/test_contrato_rama.py -q` en verde. El recuento de lo que añade la rama contra `main` (con `casos_ocultos` en memoria), sobre el árbol final, da 0 líneas con un día oculto y 0 ids ocultos.

## Respuesta del consultor a la PARADA final

Dada por Aleks (consultor) el 2026-11-20, en un solo mensaje; copiada también al final de `docs/encargos/trabajo-guardias-holdout.md`. Tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA final de trabajo/guardias-holdout (§9 de GUARDIAS-HOLDOUT.md), 2026-11-20. Cópiala tal cual al informe, en una sección «Respuesta del consultor a la PARADA final».
>
> Antes de nada: hoy es 2026-11-20 en el reloj de la laptop. La fila de HOLDOUT-EXPOSICIONES de hoy, que nombre trabajo/guardias-holdout, se escribe y se estadía antes del primer make check. G2 ya la exige en esta rama.
>
> 0. La fuga del rango y los 32 ids heredados: (a), pero NO en esta rama. Va a una rama propia del carril «guardias y deuda», después de la ingesta y la activación de la 7b; no adelanta el camino crítico. Sus condiciones, para el cierre y para su encargo:
>    - Se localizan con la puerta y en memoria, sin imprimir ids, fechas ni líneas.
>    - En tests/unit y tests/contract se sustituyen por ids sintéticos, o por ids calculados desde la puerta al ejecutarse, sin escribirlos.
>    - Los informes CERRADOS de docs/validation no se reescriben, porque el régimen es el recuadro con el cuerpo intacto. Su fase 0 dice cuántos de los 9 están en informes cerrados, y el consultor decide si un recuadro sin el id sirve o se declaran sin más.
>    - Si alguno «quema», su fase 0 lo propone con ADR-0021 §5 y ADR-0041, y lo decide el consultor en su PARADA.
>    - El AVISO de knowledge validate de §6 entra en esa rama como pregunta, porque toca src/.
>    - Por qué no aquí: ya está en main, no hay exposición nueva y esta rama no puede tocar tests/contract ni src/.
>
> 1. G2 en el cierre: (a). G2 actúa en todo make check de trabajo/*, también en el del chore(cierre).
>    - Como el commit chore(cierre) solo admite contrato, HISTORIA, ERRORES-RECURRENTES, PROJECT_STATE y HOJA-DE-RUTA (la puerta de RITUAL.md enumera esos ficheros), la fila del día del cierre va ANTES, en un commit propio de la rama, sellado: «docs(<rama>): la fila de HOLDOUT del <día>, antes de los make check del cierre». Es lo que hizo trabajo/sesion-07 en f663aa2. Si la fila del día ya está, ese commit no hace falta.
>    - Por qué: el make check del cierre lee lo mismo que los demás, y ADR-0021 §4 no distingue.
>
> 2. abrir-rama, entregar-rama y los runbooks: (a), en esta rama.
>    - Se amplía contrato.yaml con rutas_permitidas: .claude/skills/abrir-rama/SKILL.md, .claude/skills/entregar-rama/SKILL.md, docs/runbooks/CONTRATO-DE-RAMA.md y docs/runbooks/RITUAL.md. También .claude/skills/cerrar-rama/SKILL.md, SOLO si su recorrido necesita nombrar el commit de la fila del punto 1; si con RITUAL.md basta, no se toca y se dice. Verifica que ninguna esté en rutas_protegidas; si alguna está, sale de ahí.
>    - Qué se escribe:
>      - abrir-rama: la fila del día, que nombre la rama, y el artefacto, estadiados ANTES del paso 6, porque desde G2 el guion del paso 6 falla sin ella. Se reordena el texto del paso 7, que hoy la pone después.
>      - entregar-rama, paso 2: el guion en verde exige también la fila del día.
>      - CONTRATO-DE-RAMA.md, «Que comprueba make check, y que no»: G2, con su mensaje y dónde no actúa.
>      - RITUAL.md: lo del punto 1, en su sitio, antes del bloque del chore(cierre), con su puerta.
>    - Solo documentación: nada de código ni de tests nuevos. Pero comprueba con un make check que test_hoja_de_ruta y los tests de skills (si hay alguno que lea esas skills) siguen en verde.
>
> 3. La guardia de fechas: (a). V2 en su propia rama, después de la del punto 0 y con sus tres condiciones de §4.3. Para el cierre, la línea de Technical Debt que entra es esta (ajústala solo si pasa de 400 bytes o el tope de PROJECT_STATE lo pide):
>    «Sin guardia contra fechas de días ocultos en lo que añade una rama. En main hay 32 ids exactos de casos ocultos fuera de knowledge/cases, uno de ellos de F39a-F39g en tests/unit. Primero, una rama que los sustituya en tests sin abrirlos (los informes cerrados, por recuadro o declarados); después, la variante estrecha V2 (GUARDIAS-HOLDOUT.md §4.3 y §9).»
>    Salen las dos líneas de §10.
>
> 4. La comprobación del contrato: (a). Vale el make check: es el mismo guion y el mismo comando.
>
> 5. El guion de G1: (a), ratificado. Seguiste la forma literal que propone el propio mensaje de la guardia, y la permite DECISIONES-DE-PROCESO (2026-10-21, punto 1): lo que la guardia leyó es lo que se ejecutó, y eso no es rodearla. La cláusula «apártalo a la PARADA» del encargo era más estricta que esa regla, y es un error del consultor, que irá a la fila del cierre.
>
> 6. Las fechas en la historia de la rama: (a). Se aceptan en la historia de main con el merge de siempre, declaradas aquí y en HOLDOUT-EXPOSICIONES. No se reescribe nada.
>
> 7. Los mutantes a mano: (a). Editar el fichero real, pasar la suite normal y restaurar por hash no rodea la guardia: la guardia negaba cargar código sin revisar por otra vía, y el mutante pasa por la vía normal. Una condición: comprueba y escribe en el informe que ningún commit de la rama contiene un mutante, es decir, que contrato_rama.py solo tiene la versión final en aff916c8 y 72ebedfa (git log -p sobre ese fichero, sin imprimir nada fuera de él).
>
> Lo que sigue: commit con la fila de hoy, los cambios del punto 2 y esta respuesta en el informe (make check sellado antes, como siempre); push a fix/guardias-holdout y CI de Linux con su número de run; revisor con alcance en lo nuevo (las skills y los runbooks frente a G2 y al RITUAL, caso a caso); su informe pegado al final. PROJECT_STATE no se toca más allá de lo que ya lleva la rama; las líneas de §10 entran en el cierre.
>
> Rama lista para revisión, NO cerrada.

## 15. Aplicación de la respuesta del consultor (2026-11-20)

| Punto | Qué se hizo | Evidencia |
|---|---|---|
| Antes de nada | La fila de HOLDOUT-EXPOSICIONES del 2026-11-20, que nombra `trabajo/guardias-holdout`, escrita y estadiada antes del primer `make check` del día (las 00:25 en la laptop) | `HOLDOUT-EXPOSICIONES.md`, fila del 2026-11-20; la línea `G2:` de `make-check.log` |
| 0 | Nada en esta rama, como manda. Sus condiciones quedan en la respuesta, copiada arriba y al final del encargo, para la rama propia | — |
| 1 | Escrito en `RITUAL.md` (punto 2): el commit de la fila del día del cierre, antes del `chore(cierre)`. Medido lo que el consultor afirma: `f663aa29` de `trabajo/sesion-07` es «docs(sesion-07): la fila de HOLDOUT del 2026-11-18, antes de los make check del cierre» y solo toca `HOLDOUT-EXPOSICIONES.md` (`git show --stat`, con el holdout excluido) | `RITUAL.md`, «Antes del merge: la fila de HOLDOUT del día» |
| 2 | `contrato.yaml` ampliado con las cinco rutas, `cerrar-rama` incluida (abajo); ninguna estaba en `rutas_protegidas`, que no nombra `.claude/` ni `docs/runbooks/`. Escrito: **abrir-rama**, paso 6 nuevo (la fila del día y el artefacto, estadiados ANTES de comprobar), paso 7 (las comprobaciones, con la línea `G2:` esperada) y paso 8 (sello y commit), más la fila en `rutas_permitidas` del paso 4 y en la verificación; **entregar-rama**, paso 2 (el guion en verde exige la fila, y si la rama cambió el guion vale la línea del log); **CONTRATO-DE-RAMA.md**, en «Que comprueba `make check`, y que no», G2 con su mensaje literal, la línea de éxito y dónde no actúa; **RITUAL.md**, el apartado nuevo «Antes del merge: la fila de HOLDOUT del día» antes del del contrato, con su bloque y su puerta, el recuento de commits de la puerta de `git log main..` y la puerta del `chore(cierre)`, que ahora espera también la línea `G2:` | `git diff main...HEAD -- .claude/skills docs/runbooks` |
| 2 (cerrar-rama) | **Sí se toca**, en dos líneas: su recorrido cuenta los commits esperados («mas el del contrato») y con la fila del día sería uno más, y su paso 3 empieza por el apartado del contrato del RITUAL. Con solo RITUAL.md, la puerta del recuento de commits de la skill quedaba mal | `.claude/skills/cerrar-rama/SKILL.md`, «Entradas» y paso 3 |
| 2 (tests) | Solo documentación. `uv run pytest tests/unit/test_skills.py tests/unit/test_push_atomico.py tests/unit/test_hooks_utf8.py tests/unit/test_contrato_rama.py tests/unit/test_hoja_de_ruta.py tests/unit/test_fila_del_dia.py -q` en verde (`test_skills` lee las skills: sus rutas citadas existen; `test_push_atomico`, que los bloques del RITUAL no añaden pushes). Y el `make check` del commit | `make-check.log` del commit |
| 3 | La línea del consultor, en §10, tal cual: 361 bytes con «- », sin ajustar | §10 |
| 4 | Nada que hacer: vale la línea `CONTRATO:` / `G2:` de `make check` | — |
| 5 | Ratificado; nada que hacer en la rama. «Error del consultor» para la fila del cierre | — |
| 6 | Aceptado; nada se reescribe | — |
| 7 | **Ningún commit de la rama tiene un mutante.** `git log --format=%h main..HEAD -- scripts/contrato_rama.py` → solo `aff916c8`; `git rev-parse aff916c8:scripts/contrato_rama.py 72ebedfa:scripts/contrato_rama.py` y `git hash-object scripts/contrato_rama.py` dan los tres `fde14594…` (la versión final; `b9bfa80e…` era el blob durante los mutantes, antes de acortar una línea del docstring que pidió `ruff`); `git log -p main..HEAD -- scripts/contrato_rama.py \| grep -c MUTANTE` → 0, y las cinco formas de mutante (`p = raiz / ruta`, `rama in fila`, `g2: list[str] = []`, `not rama or rama == "main"`, la comparación solo por el día) → 0 líneas añadidas. Lo mismo para `tests/unit/test_hoja_de_ruta.py`: `MUTANTE` → 0 | los comandos, en la sesión, sin imprimir nada fuera del fichero |

## 16. CI y revisor de la segunda vuelta

Pendiente en este commit: el push a `fix/guardias-holdout`, su run y el revisor sobre lo nuevo.

## Exposiciones

Declaradas en `HOLDOUT-EXPOSICIONES.md`:

- **El 2026-11-19**: la apertura y la fase 0 (los `make check` del día, que leen el M1 de marzo y
  de junio para calentar; los documentos y el código de la fase 0; el incidente de terminal de
  §7.1), y el estudio de G1 (la asignación por `casos_ocultos`, solo en memoria; los textos de los
  commits del rango; el `git grep` de ids del árbol de `main`; solo recuentos; su tercera corrida,
  sin el reparto por rama). Y lo que no se pudo evitar, con su sitio: el incidente de terminal
  (§7.1) y las fechas de trabajo que coinciden con un día oculto, quitadas el mismo día (§7.6).
- **El 2026-11-20**: la respuesta del consultor (los `make check` del día; las skills y los
  runbooks; el `git log -p` de `contrato_rama.py` del punto 7, contado; el revisor), y, antes, sin
  rama ni commit, la comprobación del enlace del corpus que pidió Aleks (`corpus check --hashes` y
  Read simulados a la guardia, que no leen nada).

## Estado

Rama lista para revisión, NO cerrada. La fase 0, G2, H y el estudio de G1, hechos; la respuesta del
consultor a la PARADA final, aplicada punto por punto (§15): las skills `abrir-rama`,
`entregar-rama` y `cerrar-rama`, `CONTRATO-DE-RAMA.md` y `RITUAL.md` saben de G2 y de la fila del
día del cierre. La CI de Linux y el revisor de esta segunda vuelta, en §16.
