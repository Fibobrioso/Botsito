# GUARDIAS-HOLDOUT · La fila del día en el sello (G2), dos huecos de test_hoja_de_ruta (H) y el estudio de G1

> PLANTILLA hasta la fase 0 (la línea con que nació): la fase 0, G2, H y el estudio de G1 ya están, abajo.

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

Rango: las ramas cerradas de F39a a F39g (**incluida** F39a, porque el encargo dice «desde»; sin
ella cambia lo que se dice en §4.2) y los commits de estado de `main`: 76 commits, 69 con diff
fuera del holdout, 16.885 líneas añadidas o de mensaje.

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

Por rama: F39a 1, F39e 16, F39g 15; las demás y los commits de estado, 0. `uv.lock` y los ficheros
de asignación no cambian en el rango (auditor, 26): esas clases dan 0 por construcción, y la
medida no dice nada de ellas.

- **La única línea con el id exacto de un caso oculto la añadió `trabajo/guardia-falsos-positivos`
  (F39a) en `tests/unit`.** Su fecha es anterior al proyecto y lleva cerca una marca de mercado.
  Un id de caso oculto ES su día de mercado: esto es una fuga real, ya en `main`. No la abrí. Se
  localiza solo por carpeta y rama, y se declara (§9, punto 0).
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
5. **El rango de G1 incluye F39a.** Sin ella, 31 líneas y ninguna fuga medible.
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

Nada de G2, H ni G1 se apartó: lo medido no contradijo ninguna decisión del encargo. Lo que sigue
son consecuencias que el encargo no previó.

## Lo que necesito que decidas

0. **La fuga de F39a y los 32 ids exactos de casos ocultos de `main` fuera de `knowledge/cases`**
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
   `RITUAL.md` no nombran G2. Opciones: (a) ampliar el contrato de esta rama a
   `.claude/skills/abrir-rama/SKILL.md`, `docs/runbooks/CONTRATO-DE-RAMA.md` y `docs/runbooks/RITUAL.md`
   y escribirlo aquí, antes del cierre: la fila del día y el artefacto, estadiados antes del paso 6;
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

## 10. Preparado para el cierre (sin tocar PROJECT_STATE.md)

PROJECT_STATE.md: 24.604 bytes en la rama (tope 25.000). En el cierre:

- **Sale** la línea `:102` (G2), que esta rama paga: «make check, en una rama trabajo/*, no sella
  si HOLDOUT-EXPOSICIONES.md no tiene una fila con la fecha del día …».
- **Sale** la línea `:111` (letras reutilizadas), que H paga: «test_hoja_de_ruta no distingue un
  registro «HECHA · T» de una letra reutilizada …».
- **Entra**, si el consultor la quiere así: «Las fechas de días ocultos en lo que añade una rama no
  tienen guardia: de F39a a F39g, 32 líneas añadidas con un día oculto; una, el id exacto de un caso
  oculto (F39a, tests/unit); y en main hay 32 ids exactos fuera de knowledge/cases. Propuesta: la
  variante estrecha (id exacto o día anterior al proyecto), en su rama, tras sustituir los
  heredados (GUARDIAS-HOLDOUT.md §4 y §9).»

Las dos salidas suman unos 400 bytes y la entrada unos 330: el fichero queda por debajo de los
24.604.

## Exposiciones

Declaradas en `HOLDOUT-EXPOSICIONES.md`, el 2026-11-19: la apertura y la fase 0 (los `make check`
del día, que leen el M1 de marzo y de junio para calentar; los documentos y el código de la fase
0; el incidente de terminal de §7.1), y el estudio de G1 (la asignación por `casos_ocultos`, solo
en memoria; los textos de los commits del rango; el `git grep` de ids del árbol de `main`; solo
recuentos).

## Estado

EN CURSO: la fase 0, G2, H y el estudio de G1 están hechos. Faltan el `make check` y el commit, la
CI de Linux por `fix/guardias-holdout` y el revisor.
