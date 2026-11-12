# FUNCTIONALITY VALIDATION REPORT

**Funcionalidad:** F (2) · la preparación de la sesión 7, partida en 7a (sesion-07) y 7b (sesion-08) (R4.3)
**Rama:** trabajo/preparacion-sesion-7
**Objetivo:** dejar la sesión 7 lista para grabar en dos días, 7a y 7b, con el método escrito en un ADR, el pivote pre-registrado antes de activar nada, las preguntas de los dos días con las filas que mueve cada una, los días del bloque elegidos por una regla y las láminas de la 7a generadas fuera del repo (encargo en `docs/encargos/trabajo-preparacion-sesion-7.md`).

## Base (comprobada con git al abrir, 2026-11-11)

- `git rev-parse main origin/main`: `e6b073f1a21f230af0b5b9e081952552ca5c6c07` las dos veces.
- Último `- Tag:` de HISTORIA (línea 16971): `stable/F38w-laminas`; `git rev-parse "stable/F38w-laminas^{commit}"` = `git rev-parse main^1` = `b9904c541c3bdec7bb5163d5c6fd2c12393a1e23`; en origin (`git ls-remote --tags`: `ac9da7b…` refs/tags/stable/F38w-laminas).
- CI de main sobre `e6b073f1a21f230af0b5b9e081952552ca5c6c07`: `gh run view 43084251895` da `ci`, `completed`, `success`, `headBranch` main, `headSha` el de arriba.
- `git branch --list`: solo `main`; `git ls-remote --heads origin`: solo `refs/heads/main`.
- `wc -c PROJECT_STATE.md` en main: 23770 bytes.
- Sesión arrancada con `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1` (medido: `echo` da `1`); modelo Opus 5.5 (`claude-opus-5-5`), esfuerzo alto.

## 0. Fase 0 (2026-11-11)

Solo lectura en el repo, salvo la apertura y la fila de exposiciones. Los guiones de medida viven en
la carpeta de trabajo de la sesión (fuera del repo); los que el encargo manda llevar a los anexos
(el de las sustituciones de D3 d, y con él los de 0.4 y 0.7) entran en
`docs/validation/anexos/PREPARACION-SESION-7/` con el primer commit tras la respuesta.

(El bloque `ids-inexistentes` de ADR-0093 salió en el commit que crea el ADR, F1.)

### 0.1 La base, y lo que se mira

- La base, arriba («Base»): cuadra entera.
- **Lo que se ha mirado en la fase 0**, todo de construcción o commiteado: los anexos de
  RECORRIDA-CONSTRUCCION-2 (`patrones-cuenta-por-mes.txt`, `caja-stop.txt`, `para-clasificar.txt`),
  la constante `HORAS_PERDIDAS` de `anexos/RESPALDO-M1/horas_perdidas.py` (importada, sin leer
  ningún manifiesto), los informes cerrados que nombra el encargo, `knowledge/evidence/` y
  `knowledge/feedback/` (Read de ítems nombrados), la spec y los parámetros, y la transcripción
  **filtrada** por la CLI (`corpus transcript show`, por defecto filtrada; `evidence propose` con
  `--salida` en la carpeta de trabajo). Ninguna cruda, ningún fotograma, ningún libro, ningún caso.
- **La compuerta, contada** (guion `dias_d3.py`): los 76 días dev de construcción (enero 21, del 2
  al 30; abril 21, del 1 al 29; julio 13, del 1 al 17; agosto 21, del 3 al 31) frente a
  `casos_ocultos(repo)` (34 casos) y `casos_reservados(repo)` (34): **0 días dev en ninguno de los
  dos**. Ningún id de los ocultos se imprimió.
- Ninguna corrida del arnés ni de `motor laminas` hoy. Declarado en HOLDOUT-EXPOSICIONES, fila de
  este día de la rama.

### 0.2 Herencias

Búsqueda de «sesión 7», «7a», «7b», «R4.3», «preparación», «kit hoja», «pivote», «regla 2»,
«graficos_sesion», «no se enseñan» y «ADR del método» en PROJECT_STATE, el final de HISTORIA,
docs/validation/, docs/adr/, docs/plan/, docs/runbooks/, src/botsito/cli.py y CLAUDE.md. Lo que
deja algo a esta rama:

| # | Dónde | Qué deja | Qué se hace |
|---|---|---|---|
| H1 | `ACTIVAR-SESION-06.md:557-617` («Para la sesión 7», 1 a 11) | las preguntas de A-13, A-35, A-53, A-43, A-48, ADR-0083 D1, la alternancia, A-46, S-22, los gráficos 2 a 6 y lo que pidió para los esquemas | entra entero en 0.3 (cada punto, su sitio); el 10 ya está decidido: los sustituyen las láminas (LAMINAS.md, «La decisión de los gráficos 2 a 6») |
| H2 | ídem, punto 10, **S-7** (gráfico 1) | «va como contexto de los gráficos 2 a 6» | **no entra** (decisión 5): los gráficos 2 a 6 ya no existen; su contenido está dicho y citado (`ev-v17-004338-c8befc62`, `ev-v17-004407-42808be7`: no entraría porque no hubo toma de M15) y el contexto que pidió (`ev-v17-004910-11d48393`: los criterios del bot y los trazos de M15) lo llevan las láminas |
| H3 | ídem, punto 1: el break even «la primera de la hoja» | choca con RUMBO §1 a (primero las que más filas mueven y las del dinero) | orden propuesto en 0.3 con las dos cosas a la vista; **no se cumple el punto 1**: el break even va segundo, detrás del rango de H4 (decisión 1) |
| H4 | `ACTIVAR-SESION-06.md:614-617` (punto 11): su juicio sobre los esquemas de la sesión 6, el contexto de antes y la trendline | para hacer los esquemas | se aplica en F4 (esquemas con lo de antes dibujado; la liquidez con trendline hasta la ruptura, sin extenderla) |
| H5 | `docs/runbooks/ACTIVAR-A35-A44.md:71` y `:126-127` | dicen que el reinicio es `perdida_trader_reinicio_huso`; desde ADR-0089 lo decide `perdida_trader_reinicio` (`primera_sesion_dia_siguiente`, CONFIRMED, `parametros.yaml:1593-1614`) y el `_huso` sigue UNKNOWN y SIN EFECTO con ese valor (`:1616-1627`): **verificado, conviven los dos**. Herencia de `ACTIVAR-SESION-06-MOTOR.md:37` (H9) y `:798` (hallazgo del consultor) | NOTA en la cabecera del runbook (decisión 6), sin tocar el cuerpo ni renombrar nada |
| H6 | `docs/runbooks/ACTIVAR-A35-A44.md:48` (**no la nombra el encargo**) | «no mostrar más gráficos que los que permite su regla 2 (días de construcción, cortados antes de la orden, sin fecha; cambiada el 2026-09-28)» | deja de ser verdad con el recuadro de la regla 2: va en la misma NOTA (decisión 6) |
| H7 | `docs/adr/0092-…md:172-178` (NOTA de §6) | «Cómo se convierte una respuesta del trader en regla lo fijará el ADR del método» | lo fija ADR-0093 §4 (0.8). ADR-0092 no se toca (no está en lo que entra): ADR-0093 dice que cierra esa NOTA |
| H8 | `scripts/graficos_sesion.py:66-71` y `tests/unit/test_graficos_sesion.py:310-318` | «La regla 2 de SESION-DE-PREGUNTAS.md»: abril del 1 al 30, agosto del 1 al 31 (verificado) | no se tocan (D1); línea de Technical Debt para el cierre (decisión 7) |
| H9 | `src/botsito/cli.py:2709-2711` (docstring de `motor_laminas`) y `:3363` (ayuda de `motor laminas`) | «no se enseñan al trader» (verificado; **ningún test mira esas cadenas**: grep en tests/) | se cambian en F1, con el ADR (decisión 8) |
| H10 | `docs/runbooks/LAMINAS.md:5-10` («Lo primero») | «todavía no se enseñan al trader» | recuadro en F1 |
| H11 | `docs/runbooks/SESION-DE-PREGUNTAS.md:12-14`, regla 2 (`:21-28`) y paso 6 de «Antes» (`:92-100`) | la cabecera, la regla y `graficos_sesion.py` | recuadros en F1 |
| H12 | `docs/adr/0083-que-gasta-un-punto.md:87-88` | «Lo que pasa a la sesión 7: qué es un igual, y si la caja de la reentrada es la del primer intento o una nueva» | pregunta de la 7b (0.3, R-4) |
| H13 | `docs/adr/0084-…md:78-79` y `:125-128` | A-35: si la mecha de la propia vela contraria es el alto, y la frase que lo cierra | pregunta de la 7a (0.3, A-6) |
| H14 | `VIDEO-JULIO.md` (respuesta a la PARADA final, puntos 1, 2 y 4) | la tarde del 10 de julio; F7 #10 como pregunta técnica; los ítems F7 #1, #2, #3 y #10 | 0.3 y 0.5 |
| H15 | `TRAZAS-ABLACION.md:1390-1393` (decisiones 0, a y c) | F7 #6 lo crea esta rama; la pregunta 1 de 5.5 (colocación) y la 2 (zonas de control) a la 7a | 0.3 y 0.5 |
| H16 | `ERRORES-RECURRENTES.md`, fila de `trabajo/video-julio` (lección del consultor): un fotograma de un backtest solo se abre después de que la voz o un fotograma ya abierto sitúen el tramo | vive solo en esa fila; la skill `ingerir-sesion` (`.claude/`, protegida) no lo dice | ADR-0093 §2 lo escribe como regla de la ingesta; que la skill lo diga, propuesta para el cierre (carril de skills) |
| H17 | PROJECT_STATE, entrada J; `HOJA-DE-RUTA.md:387` | «J, si la hoja sale de kit hoja» | D1: la hoja no sale de `kit hoja`; se quita en el cierre (propuestas) |
| H18 | `SESION-DE-PREGUNTAS.md:89-91`, paso 5 de «Antes» (auditor, H1) | «ningún gráfico que no sea de los preparados según la regla 2» | choca con que el trader cargue su replay: recuadro en F1 (decisión 11) |
| H19 | `src/botsito/engine/decisiones.py:7-8` (auditor, H3) | «lo fijara el ADR del metodo (RUMBO §1); esto no lo adelanta» | `engine/` protegido: Technical Debt (decisión 12) |
| H20 | `RECORRIDA-CONSTRUCCION-2.md:1323` y `:1333` (auditor, H4) | los ejemplos de la caja, «dos al visor en la rama de la preparación» | van al bloque de días de la 7b; desviación (decisión 13) |

Nada más: «pivote» solo aparece en RUMBO §4 y R4.3 (lo recoge D5); «7a»/«7b», en R4.3, en
PROJECT_STATE (F) y en LAMINAS.md.

### 0.3 Las preguntas candidatas, con sus filas

**Las cuentas del pivote (D5), medidas** (guion `pivote_julio.py` sobre
`anexos/RECORRIDA-CONSTRUCCION-2/patrones-cuenta-por-mes.txt`, julio de 2026):
`T0 (parejas): 14`; `P5: 37 ({'otro lado': 10, 'mismo lado': 27}); P6 en sesion: 2; P6 en dia: 0`;
`operaciones de mas (P5 + P6 en sesion): 39`; `T0 + P2 + P3 + P7 = 14 + 14 + 15 + 3 = 46`;
`tasa de pareja: 14 / 46 = 0.304`; `OK: 14 y 39`. **Salen 14, 39 y 46, las del encargo.**

**Las 29 filas del trader de julio que pueden mover las preguntas**, contadas contra sus fuentes:
- el rango de H4: 30 filas en VIDEO-JULIO.md §4.1 y §4.2 (`:657`: «el rango de H4 30: 1, 6, 7, 15 y
  17 de julio»), de ellas 10 P5 del bot (07-01 07-11 ×3, 07-07 ×6, 07-15 11-15 ×1; las 10 son las 10
  P5 «otro lado» de julio de arriba) y **20 del trader** (P1: 07-01 ×2, 07-06 07-11 ×4, 07-06 11-15
  ×1, 07-07 ×8, 07-15 11-15 ×4, 07-17 11-15 ×1). Las 2 del 1 de julio cuentan: la pregunta es
  abstracta y el día no va al bloque;
- las zonas de control: **8** con el gate RN-009 (TRAZAS-ABLACION.md 5.2, `:878-881`: 07-02 11-15
  ×3, 07-03 11-15 ×1 y 07-14 11-15 ×4; las 4 de 07-14 cuentan aunque la sesión no va al bloque,
  D3 e);
- la colocación: **1**, la P2 de 2026-07-03 07-11 (`filas_por_sesion.py`: «P2/Δentrada minima 11
  puntos (trader): 1»).

20 + 8 + 1 = **29**; las tres listas no se solapan (otros días y otras filas). A la tasa de 14/46
(30,4 %), 29 filas dan 8,8 parejas, «unas 9»; el mínimo 1 pide 19 − 14 = 5 (el 57 % de 8,8:
«algo más de la mitad»). El mínimo 2: (39 − 33) / 39 = 15,4 %, «un 15 %». **La cuenta del porqué de
D5 cuadra con lo medido.**

**Las preguntas**, con lo dicho, lo decidido, las filas y dónde cae cada opción. Código provisional:
A-n para la 7a, B-n para la 7b; en F4 pasan a S-1… dentro de cada id (D2).

| Cód. | Pregunta | De dónde sale | Lo que ya dijo / lo decidido (solo citable) | Filas que puede mover (julio / total) | Dónde cae cada opción |
|---|---|---|---|---|---|
| A-1 | **El rango de H4**: qué vela es el rango, cuándo lo da por actualizado y qué es un rango mayor | R4.3; VIDEO-JULIO.md:621-624 (pregunta 1), §7 #1-#3; strategy_spec.yaml:1127-1128 | **Decidido, no se pregunta**: que la ruptura vale con mecha o con cuerpo, dicho de la vela de rango («con mecha o con cuerpo por debajo de esta vela que es nuestro rango», `ev-v9-000902-25db5bf5`, `valor: mecha`; F7 #2 lo repite) y del extremo de la H4 anterior (`sesgo_h4_criterio_ruptura` = `mecha`, CONFIRMED, `fb-2026-10-04-sesion-04-d2e84172`) y que además tiene que cerrar del color de la ruptura (ADR-0080 §1, `fb-2026-10-04-sesion-04-6e7da456`); que siempre hay sesgo (`ev-v9-001529-ac28bb40` y `fb-2026-09-29-sesion-03-1168f036`, la cita de strategy_spec.yaml:1203-1204; «para el el sesgo es el del ultimo rango, dure lo que dure», `:1206-1207`, es glosa de la spec, no del trader); que el rango se rompe en H4 y no en M15 (`ev-v17-015741-8f9fd638`), y que la toma de la mañana vale por la tarde si el rango no se rompe (`ev-v17-015726-ce2e42e4`, A-46 RESUELTA). **Dicho y no decidido**: «la vela de rango puede durar varias H4» (afirmación de `ev-v9-000902-25db5bf5`), y «como no ha sido mitigado ni por debajo por una vela bajista ni por arriba por una vela alcista para actualizar el rango» (F7 #1). **Abierto**: el bot compara cada H4 con la anterior (RN-003, `sesgo_h4_al_abrir`); el trader, con «el rango», que dura días (07-07: «tres días, dos días», VIDEO-JULIO.md:613). La reserva «suponiendo que no haya otro rango mayor» (strategy_spec.yaml:1127-1128). | **julio 30** (20 del trader, 10 P5 del bot) / total: las 24 P1 del resto (enero 7, abril 9, agosto 8; RECORRIDA-CONSTRUCCION-2.md:1367) sin clase, no medidas contra el rango | regla nueva de sesgo (RN-003 con ADR propio); ninguna opción cae en un parámetro existente |
| A-2 | **Qué zonas cuenta como zonas de control de un esquema** | TRAZAS-ABLACION.md:951-957 (5.5 punto 2), decisión c (`:1393`) | **Decidido, no se pregunta cuántas**: A-20 RESUELTA, «solo 1 zona control bro. si hay 2 se descarta» (`fb-2026-09-09-sesion-01-1b2203b0`; `zonas_control_max_por_esquema` = 1). Hoy el bot cuenta como zonas de control los pivotes de M1 del sentido de la entrada (bajos en una compra) que se forman después de la primera vela del impulso, entre la toma y el breaker (`domain/estructura_m1.py:153-176`, que lee `engine/zonas.py:471-490`) | **julio 8** (gate RN-009) / total: la ablación de RN-009 gana 18 filas del trader y pierde 13 T0 (TRAZAS-ABLACION.md:916-923; diagnóstico, ADR-0092 §6) | la definición de `zonas_desarrolladas_superan` (`pivotes_de_control`); el número no cambia |
| A-3 | **¿En el backtest dejas entradas válidas sin tomar? ¿cuándo y por qué?** (F7 #10) | VIDEO-JULIO.md:939 (respuesta a la PARADA final, punto 2); D6 | «aquí hay una entrada que no le voy a tomar para no afectar al mostreo» (v14, F7 #10; el ítem lo crea F3). Hasta que lo explique, una operación de más no se da por error | ninguna fila del trader; decide cómo se leen **las 39 de más de julio** (192 en total: P5 153 + P6 en sesión 39, `patrones-cuenta-por-mes.txt`) y el mínimo 2 del pivote | ninguna regla del bot: cambia la lectura de P5 (y la salida del pivote, D5) |
| A-4 | **En qué momento coloca la orden respecto de la ruptura del punto** | TRAZAS-ABLACION.md:945-950 (5.5 punto 1), decisión a (`:1391`); ADR-0064 | «aquí no había entrada porque es con mecha, sabemos que tiene que ser con cuerpo [...] aquí sí que tenemos una entrada vale porque nos genera un breaker con cuerpo» (v12, F7 #6; el ítem lo crea F3) frente a «en M1 la mecha siempre vale» (`ev-v16-000234-9a4fa375`, A-32 RESUELTA por S-18): «contradicción con lo fijado» (decisión 0, `:1390`). Hoy la stop nace al aparecer el punto (`orden_limite_nace` = `al_aparecer_punto_de_breaker`, `orden_stop_punto` = `ultimo_pivote_m1`; ADR-0064) y se llena al tick | **julio 5** (07-03 07-11: la P2 y 4 P5) / total: el mecanismo de **toda** orden stop del bot (247 llenadas y cerradas, RECORRIDA-CONSTRUCCION-2 §1.3) | `orden_limite_nace` (nueva opción, con ADR) |
| A-5 | **El break even (A-13)** | ACTIVAR-SESION-06.md:562-573 (punto 1) | `break_even_condicion` = `tocar` (`fb-2026-09-09-sesion-01-0ccafcba`) y `break_even_criterio_ruptura` = `mecha` (`fb-2026-09-29-sesion-03-2cff5008`), CONFIRMED; en la sesión 6, al cierre con cuerpo (`ev-v17-005111-8933dab2`, `ev-v17-005200-4f93afa0`, `ev-v17-005554-172ecbb2`), con la excepción del imbalance (`ev-v17-005352-cda6245d`) y «un poco de margen» (`ev-v17-005454-90ce4feb`) | ninguna pareja (no cambia la entrada); **el dinero**: 100 líneas `stop_movido` frente a 247 llenadas y cerradas en la línea base (`grep -c` sobre `anexos/RECORRIDA-CONSTRUCCION-2/cuenta-por-mes.txt`; 118 de 286 en la diaria del respaldo, ACTIVAR-SESION-06.md:563) | `break_even_condicion` (`tocar` / `cierre`) y `break_even_criterio_ruptura` (`mecha` / `cuerpo`), dos CORRECT con supersede |
| A-6 | **A-35, la mecha** | ACTIVAR-SESION-06.md:574-580 (punto 2); ADR-0084 (recuadro del 2026-11-05) | `liquidez_m15_mecha_que_vuelve` = `solo_la_contraria`, lectura del consultor; A-35 ABIERTA y bloqueante; la vela sin cuerpo en M15 (S-4) no se repregunta; en tensión, «se actualiza el de la mecha» (`ev-v15-000553-9d95178a`, ADR-0084:76-79) y, del recuadro del 2026-11-05 (ADR-0084:125-128), si la mecha de la propia vela contraria es el alto | no medido por fila: decide qué alto o bajo de M15 se toma (RN-004), es decir, cada toma de M15 de la construcción | `liquidez_m15_mecha_que_vuelve` y `liquidez_m15_pivote_formado` |
| B-1 | **El 0 y el stop: «¿de qué sale tu stop?»** (A-48) | RECORRIDA-CONSTRUCCION-2.md:1335-1339; ACTIVAR-SESION-06.md:591-592 (punto 5) | DISPERSA en los dos sentidos: el cociente va de 0,21 a 9,25, mediana 0,83 (`caja-stop.txt`); por eso no se pregunta «¿más lejos o más cerca?» | **julio 16 con el stop fuera y 7 P2 a 4-10 puntos** / total 44 y 24 (`caja-stop.txt`; `grep -c`) | `caja_bloque` y el 0 de A-48 |
| B-2 | **S-22**: el punto de breaker | ACTIVAR-SESION-06-MOTOR.md:791 (decisión 2); ACTIVAR-SESION-06.md:606-608 (punto 9) | «m15» dudoso en la frase de la mecha (`ev-v17-015404-06ac0e9d`); dos lecturas sin regla: si el último pivote no cumple, ¿vale el anterior o no hay punto?; ¿la última vela verde o toda la racha? | no medido por fila: quita el 52 % de los puntos de breaker (ACTIVAR-SESION-06-MOTOR.md:791) | la regla de la fase 3 de ACTIVAR-SESION-06-MOTOR (rama propia, con ADR) |
| B-3 | **S-19**: el precio ya está más allá del 0 al formarse la caja | ACTIVAR-SESION-06-MOTOR.md:792 (decisión 3); RECORRIDA-CONSTRUCCION-2.md:699 | «se pone igual, ya me habilita» (`ev-v17-014103-8cf3e7fb`): ¿entra, espera a que el 0 quede del lado bueno o descarta? Si dice «espero», 3.a y 4.a (lectura del consultor) | no medido por fila: 32 rechazos al colocar en la línea base (TRAZAS-ABLACION.md 5.4, «rechazos 32»), cada uno gasta su punto (ADR-0083) | `precio_invalido` y el gasto del punto (ADR-0083) |
| B-4 | **El «igual» y la caja de la reentrada**, en una sola pregunta | ADR-0083:87-88 (D1); ACTIVAR-SESION-06.md:593-594 (punto 6); VIDEO-JULIO §7 #7 | «un igual» (`ev-v17-013009-5e47afdb`) y la caja del segundo intento (`ev-v17-013815-9cf6f076`); F7 #7 «si es unicuel, podemos reentrar» | **julio 3** (P7) / total 4 P7, «la rama de RN-019» (RECORRIDA-CONSTRUCCION-2.md:1319) | RN-019 (Technical Debt: no dispara) y ADR-0083 D1 |
| B-5 | **A-53**: la orden sin llenar cuando el precio toma otra liquidez de M15 | ACTIVAR-SESION-06.md:581-585 (punto 3) | dijo la (a), la quita (`ev-v17-005730-76948af1`), explicó la (b) (`ev-v17-005846-0891a9c9`, `ev-v17-005914-55580dc0`); `orden_pendiente_al_abrir_escenario` = `se_mueve`, DEFAULT_AMBIGUOUS | no medido | `orden_pendiente_al_abrir_escenario` |
| B-6 | **A-43**: la liquidez tomada antes de las 7, con las horas escritas | ACTIVAR-SESION-06.md:586-590 (punto 4) | antes de las 7 solo para el trazo de liquidez (`ev-v17-010321-352430e3`, `ev-v17-010424-6d7f2d3f`); `toma_antes_de_la_ventana` = `cuenta`, CONFIRMED | no medido | `toma_antes_de_la_ventana` |
| B-7 | *si cabe*: **los dos esquemas** (qué tiene que tener la zona; sin punto breaker de ruptura, ¿nunca hay entrada?) | VIDEO-JULIO.md:625-627 (pregunta 2); D6 | F7 #5 (no se crea ítem: no lo pide el encargo) | **julio 3** (07-02 07-11 P6 ×2, 07-08 P5) | sin regla del bot hoy (los dos esquemas no se distinguen: Technical Debt de `motor laminas`) |
| B-8 | *si cabe*: **seguir tras tres pérdidas** | VIDEO-JULIO.md:628-630 (pregunta 3) | — | **julio 2** (07-02 14:10 y 14:23) | `cartuchos_max` = 3 (RN-016), que «no se toca» (ADR-0083:86) |
| B-9 | *si cabe*: **la alternancia** (RN-009, S-21) | ACTIVAR-SESION-06.md:595-601 (punto 7) | no comparte la premisa (`ev-v17-002954-613d9421`); la liquidez de la izquierda (`ev-v17-003222-85f12e6b`); «puede ser muy ruidoso» (`ev-v17-002803-4c5ea744`); S-21 (`ev-v17-014945-9e7de278`, `ev-v17-015029-bc697500`) | se solapa con A-2: el mismo predicado (`zonas_desarrolladas_superan`) | lo que responda en A-2 |
| B-10 | *si cabe*: **A-46 por la toma** | ACTIVAR-SESION-06.md:602-605 (punto 8) | A-46 RESUELTA; contestó sobre el sesgo y el rango, no sobre la toma (`ev-v17-015726-ce2e42e4`, `ev-v17-015741-8f9fd638`). Si entra, la pregunta lo dice: no reabre A-46, pregunta solo por la toma, que no contestó | no medido | — |
| — | **la tarde del 10 de julio** (fuera de las seis, al final de la 7b) | VIDEO-JULIO.md:935 (punto 1); D6 | el libro tiene tres ventas y el vídeo no la enseña: «¿se grabó en otra parte?» | material, no técnica | — |

**Lo que se descarta, y por qué:** «con mecha o con cuerpo» (F7 #2) **no se pregunta**: está
contestado y decidido (arriba, A-1); su ítem se crea igual como cita (0.5). «¿Cuántas zonas de
control?» tampoco (A-20). La vela sin cuerpo de M15 (S-4 de la sesión 6), resuelta. «¿Cuántos días
puede durar un rango?» (VIDEO-JULIO.md:624) no se pregunta así: ya dijo que la vela de rango «puede
durar varias H4» y que lo ha visto mantenido «tres días, dos días»; se pregunta cuándo lo da por
actualizado.

**Las preguntas de TRAZAS-ABLACION.md 5.5 nombran días y horas** («El 3 de julio, entre las 08:02 y
las 09:35», «El 13 de abril a las 08:47…»): en F4 se reescriben sin ellos, en abstracto y con un
esquema inventado; los días van al bloque y los dice Aleks en la sesión.

### 0.4 Los días

`dias_d3.py`, D3 a) a c) sesión a sesión por la compuerta (a: dev de un mes de construcción y fuera
de ocultos y reservados; b: el laborable anterior también; c: ninguna de las 18 horas perdidas
dentro de la sesión, en Europe/Madrid, y ninguna fila «posible M» de la sesión):

- **La condición b) sobre los 76 días dev excluye exactamente 2026-01-02, 2026-04-01, 2026-07-01 y
  2026-08-03**, la lista del encargo, calculada por la condición.
- **Las diez de LAMINAS pasan las diez** (rango de H4 6 de 6, zonas de control 3 de 3, colocación
  1 de 1).
- **La lista de la 7b de F3.5: pasan 4 de 6.** No pasan 2026-01-02 11-15 (b: el día anterior,
  2026-01-01, no es de construcción) ni 2026-07-10 07-11 (c: la hora perdida 2026-07-10T05Z dentro, y
  2 filas «posible M»).
- Controles: 2026-07-14 11-15 no pasa (c: 2026-07-14T12Z dentro); 2026-07-01 07-11 y 2026-04-01
  11-15 no pasan (b); 2026-07-17 07-11 **sí pasa a) a c)** (D3 f la saca del rango de H4: decisión 3).

**Las sustitutas de D3 d** (`sustitutas.py` sobre `caja-stop.txt` y `para-clasificar.txt`, con la
marca «posible M» de las dos fuentes):

| Grupo | Sale | La siguiente que cumple a) a c) | Las que salta |
|---|---|---|---|
| stop fuera, de mayor a menor | 2026-01-02 11-15 (9,25) | **2026-01-07 07-11 (3,14)**, venta | — |
| P2 a 4-10 puntos, de mayor a menor | 2026-01-02 11-15 (2,25) | **2026-01-13 07-11 (2,07)**, que ya está en la lista (P5): decisión 2; la siguiente distinta, **2026-01-19 11-15 (1,78)** | — |
| P2 a 4-10 puntos, de menor a mayor | 2026-07-10 07-11 (0,38) | **2026-07-17 07-11 (0,48)**, que D3 f saca del bloque: decisión 3; la siguiente, **2026-01-21 07-11 (0,50)** | — |
| stop fuera, de menor a mayor (si 2026-07-02 11-15 va a la 7a) | 2026-07-02 11-15 (0,21) | **2026-07-16 07-11 (0,34)** | 2026-07-10 07-11 (0,32; c) |

**Las filas de cada sesión** (`filas_por_sesion.py` sobre `patrones-cuenta-por-mes.txt`):

| Sesión | Filas (del trader / del bot) | Por patrón | Pregunta a la que sirve |
|---|---|---|---|
| 2026-07-07 11-15 | 9 (4 / 5) | P1 ×4, P5 otro lado ×5 | A-1 |
| 2026-07-07 07-11 | 5 (4 / 1) | P1 ×4, P5 otro lado ×1 | A-1 |
| 2026-07-15 11-15 | 5 (4 / 1) | P1 ×4, P5 otro lado ×1 | A-1 |
| 2026-07-06 07-11 | 4 (4 / 0) | P1 ×4 | A-1 |
| 2026-07-06 11-15 | 1 (1 / 0) | P1 | A-1 |
| 2026-07-17 11-15 | 1 (1 / 0) | P1 (sesgo alcista) | A-1 |
| 2026-07-02 11-15 | 10 (6 / 4) | P3 ×4 (3 con gate RN-009), P2 Δ43, T0, P5 ×4 | A-2 (y B-1, B-8) |
| 2026-04-13 07-11 | 4 (3 / 1) | P3 ×3 (gate RN-009), P5 | A-2 |
| 2026-07-03 11-15 | 2 (1 / 1) | P3 (gate RN-009), P5 | A-2 |
| 2026-07-03 07-11 | 6 (2 / 4) | T0, P2, P5 ×4 | A-4 |
| 2026-01-13 07-11 | 8 (1 / 7) | P2, P5 ×7 | B-1 (cociente 2,33 y 2,07), B-8 (RN-016) |
| 2026-04-15 11-15 | 5 (0 / 5) | P6 en día ×5 | A-3 (el trader no opera), B-1 |
| 2026-01-07 07-11 | 4 (1 / 3) | T0, P5 ×3 | B-1 (3,14) |
| 2026-01-19 11-15 | 3 (3 / 0) | T0, P2, P3 | B-1 (1,78) |
| 2026-01-21 07-11 | 3 (2 / 1) | P2, P3, P5 | B-1 (0,50) |
| 2026-01-22 11-15 | 3 (3 / 0) | P1 (sesgo alcista por 2 puntos; toca A-16) | A-1 (material) |
| 2026-07-16 07-11 | 1 (1 / 0) | T0 (cociente 0,34) | B-1 |

### 0.5 La evidencia de F7 #1, #2, #3, #6 y #10

Medido SIN ESCRIBIR con `ensayo_evidencia.py`: hace lo mismo que `evidence new` antes de escribir
(`limpiar_campos`, `_validar_campos`, `calcular_id` y `_EntornoEvidencia.comprobar`, que localiza
la cita con las funciones de verificación; `cli.py:997-1048`) y no llama a `escribir_item`. Las
citas, de la filtrada por la CLI (`corpus transcript show`):

| # | Vídeo, ventana | Transcripción | Resultado |
|---|---|---|---|
| 1 | v11 0:00:38-0:00:53 | la activa, `tr-v11-…-d5da10be` | ACEPTADA |
| 2 | v11 0:05:50-0:06:00 | la activa | ACEPTADA |
| 3 | v12 0:06:50-0:07:07 | la activa, `tr-v12-…-cb502503` | ACEPTADA |
| 6 | v12 0:00:15-0:00:58 | la activa | ACEPTADA (con `[...]`: dos trozos) |
| 10 | v14 0:42:02-0:42:40 | la vieja, `tr-v14-…-2253ec10` | **RECHAZADA dos veces**: «transcripcion … no es la activa de v14» y «la cita esta en 0:44:05.628-0:44:09.308: ajusta t0/t1» |
| 10 | v14 0:44:04-0:44:11 | la vieja | **RECHAZADA**: «no es la activa de v14» |
| 10 | v14 0:44:04-0:44:11 | la activa, `tr-v14-…-1d289df6` | ACEPTADA |

- **`evidence new` no admite citar una transcripción que no es la activa**, aunque `--transcripcion`
  lo acepte como opción: `_EntornoEvidencia.comprobar` lo pone como problema
  (`cli.py:658-663`) y `escribir_item` no escribe con un problema (`evidence/modelo.py:433-435`).
  `evidence accept` pasa por el mismo `comprobar` (`cli.py:1238`). Solo `evidence propose --check`
  lo deja en aviso (`evidence/propuestas.py:361-362`), pero el esqueleto sale siempre de la activa
  (`cli.py:1116`) y `accept` lo rechazaría después. Lo que dicen VIDEO-JULIO.md §7 («citables
  por su id con `--transcripcion`», `:690-691`) y el encargo («#10 es de la versión vieja de v14:
  `--transcripcion`») **no se cumple**: la medida gana (decisión 0).
- **La transcripción activa de v14 trae el mismo segmento** (`corpus transcript show --video v14
  --t0 0:41:50 --t1 0:44:30`, sin `--transcripcion`: `[0:42:02.058] aquí hay una entrada que
  claramente lleva por debajo […] aquí hay una entrada que no le voy a tomar para no afectar al
  mostreo, o sea importante, el bias es el sistema en este caso,`). La cita se localiza por palabras
  en **0:44:05.628-0:44:09.308**: el 0:42:02 de VIDEO-JULIO.md §7 es el inicio de un segmento largo,
  no el instante de la frase.
- **`evidence propose --check`**, medido con #1 (esqueleto con `--salida` en la carpeta de trabajo,
  rellenado y comprobado ahí): `item 1: localizado en 0:00:38.240-0:00:53.170 (segmentos [10, 11,
  12, 13, 14, 15, 16])`, `OK: 1 items, 0 no_consta; salida sellada`. Usa la misma localización
  (`verificar_citas`). La vía que propongo para F3 es `evidence new` (un ítem por cita, la ventana
  medida aquí), como las ramas de extracción.
- **Ninguna es de v13** (F7 #1 y #2 son de v11; #3 y #6, de v12; #10, de v14): el tramo de precaución
  de v13 (0:00:00-0:00:35) no las toca. Y ninguna ventana pisa un tramo no citable (lo comprueba el
  mismo `comprobar`, `ventana_no_citable`, `cli.py:637-639`).
- **F7 #2 ya está cubierta por lo decidido** (0.3, A-1): se crea igual como cita, con `valor:
  mecha`, el mismo tema y el mismo valor que `ev-v9-000902-25db5bf5` (`sesgo.h4.rango`), así que no
  abre ninguna contradicción.
- **F7 #6 frente a S-18**: con un tema propio (`entrada.breaker_m1_con_cuerpo`, `valor: cuerpo`) el
  detector de contradicciones no la cruza con `ev-v16-000234-9a4fa375` (tema
  `liquidez.m1_mecha_m15_cuerpo`, **sin valor**): la contradicción es la que ya declaró
  TRAZAS-ABLACION (decisión 0) y queda escrita en las notas del ítem, no en `_contradicciones.yaml`
  *(corregido tras el revisor, b11: por la respuesta a la PARADA, punto 15, no va en las notas del
  ítem sino en este informe, F3, y en «Para Aleks» de S-5 de la 7a)*
  (el punto ciego de los temas hermanos, Technical Debt).
- **El trailer `Fuente:`**: `knowledge/evidence/` no está en `DIRECTORIOS_CON_FUENTE`
  (CLAUDE.md, «El trailer Fuente:»: solo `knowledge/spec/` y `knowledge/cases/`); el commit de F3 lo
  lleva igual, con los ids nuevos (`ev-*`) en el cuerpo, como las ramas de extracción.

### 0.6 Las hojas del guion de transcripción

- `scripts/transcribir_sesion.py:136-140` `ORDEN_SESION_06` (S-1 a S-23); `:216-243`
  `CODIGOS_DE_SESION_TEXTO["06"]` (los títulos de `docs/sesion-6/PREGUNTAS.md`, sin recuadros);
  `:245-251` `HOJAS`; `:252` `SESION_EN_CURSO = "06"`; `:715-725` `codigos_validos` suma los de la hoja;
  `:739-741` el `--sesion` por defecto.
- Tests (`tests/unit/test_transcribir_sesion.py`): `_RE_TITULO` (`:582`, la negrita
  «**S-n. …**»), `_titulos_06` (`:649-654`), `test_la_hoja_06_tiene_los_23_codigos_con_su_texto`
  (`:657-663`), `test_la_sesion_en_curso_es_la_06` (`:666-669`),
  `test_s24_y_s25_valen_en_la_05_y_no_en_la_06` y `test_la_filtrada_de_la_06_agrupa_con_su_hoja`
  (`:672-690`).
- Para "07" y "08": `ORDEN_SESION_07` y `ORDEN_SESION_08` (S-1 a S-n de cada documento),
  `CODIGOS_DE_SESION_TEXTO["07"]` y `["08"]` con los títulos de `docs/sesion-7/PREGUNTAS-7A.md` y
  `PREGUNTAS-7B.md`, `HOJAS["07"]` y `["08"]`, `SESION_EN_CURSO = "07"`; en los tests,
  `test_la_sesion_en_curso_es_la_06` pasa a `…_es_la_07` (a propósito, con su motivo), dos tests de
  hoja que leen los títulos de cada documento (como `_titulos_06`), y el que rompe a propósito: un
  código de la hoja que no está en el documento (una copia de la hoja con un S-n de más hace fallar
  la comparación). La 06 no cambia.
- **Nada más da por hecha una sola sesión 7 ni choca con el 08**: `grep` de `sesion-07`,
  `sesion-08`, `"07"` y `"08"` en `src/botsito`, `scripts` y `tests/unit` solo da horas
  (`test_ticks_spread.py:83-118`); el formato del id admite `sesion-08` (`comun/ids.py:29`).

### 0.7 El pivote

`pivote_julio.py` da **14 y 39** (arriba, 0.3): no hay PARADA. Propuesta: el yaml en
`docs/plan/PIVOTES-SESION-7.yaml` (la del encargo; `docs/plan/` no la lee ningún test de la hoja de
ruta) y su test en `tests/unit/test_pivotes_sesion_7.py`, con tres pruebas: (1) el sha256 del
fichero, escrito en el test (cambiar el yaml exige cambiar el test a la vista en el mismo commit);
(2) el contenido leído con el lector estricto (`comun/yaml_estricto.leer_yaml`): los dos mínimos
(19 y 33), la línea base (14 y 39, P5 37 y P6 2), las tres salidas y la contingencia; (3) el que
rompe a propósito: una copia del yaml en `tmp_path` con el mínimo 1 a 18 no da el sha256 escrito (y
la comprobación de contenido la rechaza).

### 0.8 El índice del ADR-0093

«El método de las sesiones y de las activaciones», frente a RUMBO §1 a) a e) y F1:

| § | Decide | RUMBO §1 | F1 |
|---|---|---|---|
| 1 | Las preguntas salen de diferencias medidas, cada una con las filas que puede mover; como mucho seis técnicas por día de sesión (cada día, 7a y 7b, es una sesión con su id); primero las que más filas mueven y las del dinero (A-35, A-13); cerradas, con opciones y «otra, ¿cuál?» en todas; sin días ni fechas; esquemas inventados rotulados; ninguna repregunta lo decidido | a) | 1 |
| 2 | El bloque de días: primero el bloque técnico, en abstracto; después, por sesión, los cinco pasos de F1.2 (Aleks comprueba el día y se lo dice; el trader abre él el replay, en una sesión nueva, sin marcas, backtests ni Analytics, antes de compartir pantalla, y eso **sustituye** la salvaguarda «el gráfico lo prepara Aleks» del recuadro del 2026-09-28; opera con voz; ve las láminas, recortadas al instante de decidir, con caja, orden, stop y objetivo, sin fecha ni nada posterior, y la tipo a solo si se llenó, aceptado por ser construcción ya operada por él, sin enseñar ningún resultado; corrige y se le pregunta «¿siempre, solo en este caso, o de qué depende?»; si aparece otro backtest, Analytics o material reservado, se reconduce, el tramo es no citable el mismo día y en la ingesta ningún fotograma se abre antes de que la voz o uno ya abierto sitúe el tramo en el día de construcción) | b) | 2 |
| 3 | Los días: D3 a) a c), escritos por su condición (RUMBO §1 b los escribía por sus casos: «nunca el 1 de abril ni el 1 de julio»; la condición los incluye, y también el 2 de enero y el 3 de agosto), comprobados por la compuerta y declarados en HOLDOUT-EXPOSICIONES | b) | 3 |
| 4 | De la respuesta a la regla: primero un test sobre casos de construcción que rompe en main; cada activación declara ANTES qué filas de la clasificación vigente debería convertir en pareja, corre un mes de construcción en la rama y da su delta de parejas y de operaciones de más frente a la línea base; la cifra dice si la respuesta se entendió y nunca ajusta un parámetro (ADR-0092 §6). Cierra la NOTA de ADR-0092 §6 | c), d) | 4 |
| 5 | Las clases: error nuestro, regla desconocida, efecto de la cuenta, material incompleto, sin clase; la precisión se lee de verdad solo sobre meses con vídeo | e) | 5 |
| 6 | El pivote de D5, literal, con el yaml y su test, el porqué con la cuenta de 0.3 y lo visto | (§4, enmienda del 2026-11-10) | 6 |
| 7 | Lo que cambia en SESION-DE-PREGUNTAS.md (regla 2, cabecera, paso 6 de «Antes») y en LAMINAS.md («Lo primero»), con recuadros «Por qué cambió» que copian el texto anterior | (cambia SESION-DE-PREGUNTAS, §1) | 7 |
| — | Problema que resuelve; Alternativas consideradas; Por qué elegimos; Por qué descartamos; Impacto (los recuadros, las dos cadenas de cli.py, la NOTA de ACTIVAR-A35-A44, el Technical Debt de graficos_sesion.py); Fecha / fase; Estado ACTIVE | — | — |

**Lo que choca con él** (y se corrige en el mismo commit o se propone para el cierre):
SESION-DE-PREGUNTAS.md:12-14 (la cabecera), `:21-28` (la regla 2: «abril» entero, «cortados ANTES
de la colocación», «sin la fecha visible», «nunca la orden, el stop, el objetivo»), `:41` (en el
recuadro del 2026-09-28, la salvaguarda «el gráfico lo prepara Aleks, no el trader»: el recuadro no
se toca, lo sustituye el nuevo) y `:92-100` (el paso 6); LAMINAS.md:5-10; cli.py:2709-2711 y :3363;
ACTIVAR-A35-A44.md:48 (H6); `graficos_sesion.py:66-71` y su test (H8, Technical Debt); RUMBO §1 b
(el 1 de abril y el 1 de julio por sus casos: RUMBO no se toca, el ADR escribe la condición y lo
dice). **CLAUDE.md no choca**: ninguna línea suya habla de qué se enseña al trader; las capturas de
Analytics siguen prohibidas, y el paso 2 del ADR las aparta de la pantalla. **ADR-0021 no choca**:
enseñar un día de construcción no es abrir ni exponer un reservado (§1), como ya dicen los dos
recuadros de la regla 2.

### 0.9 El tiempo y la memoria

- `motor laminas`: 520-659 s por invocación, pico de unos 645 MiB (docs/runbooks/LAMINAS.md:22-25).
  F6 son dos invocaciones (el ensayo en el clon y la buena), unos 20 minutos, una a la vez y nunca
  junto a un `make check`.
- `make check` de la apertura (este día): 3420 passed, exit 0, 1408 s (test 1288 s); PICO DE MEMORIA 312 MiB en `test` (el mayor proceso, 301 MiB). No selló: quedó sin seguir `knowledge-validate.log`, salida mía de `knowledge validate` en la raíz; se borró y se repitió (fila «Los make check de la rama»).

### 0.10 Lo que no pude medir

- Las filas que mueven A-6 (A-35), B-2 (S-22), B-3 (S-19), B-5 (A-53), B-6 (A-43) y B-10 (A-46): no
  hay recuento por fila commiteado; doy el mecanismo o la cifra de órdenes que sí hay.
- Las filas del rango de H4 fuera de julio: las 24 P1 de los otros meses no están clasificadas
  contra el rango (sin vídeo).
- Cuántas láminas de tipo a y b saldrá en cada sesión del bloque de la 7a: lo da F6.

### 0.11 El encargo frente al repo (auditor-encargo)

78 afirmaciones: 64 correctas, 0 incorrectas, 14 con matiz; 10 herencias o requisitos que el encargo
no recoge. Lo que cambia el trabajo, y dónde queda:

| Del auditor | Qué se hace |
|---|---|
| 6 (PROJECT_STATE en la rama, 23.916 bytes tras abrir) | la cifra de partida del cierre es la de `main`, 23.770; el tamaño final se mide en la PARADA final |
| 15 (la sesión 5 se grabó en dos días con un solo id) | decisión 13 (iii) |
| 21 (ADR-0021 §1 lo dice por exclusión; lo explícito, CLAUDE.md punto 2) | el ADR cita los dos |
| 28 y H5 (D4 frente a R4.5 y F) | decisión 13 (i) |
| 31 (julio, `provisionales_con_video`) | decisión 13 (v) |
| 37 y H6 (2 de las 20 filas del trader son del 1 de julio) | decisión 13 (iv); 0.3 |
| 51 (:2710-2711 es un docstring, :3363 la ayuda) | 0.2, H9; decisión 8 |
| 60 (la cita de la regla del último rango en strategy_spec.yaml:1204 es `fb-…-1168f036` y `ev-v9-001529`; «el del último rango, dure lo que dure» es glosa de la spec; `ev-v9-000902` no está en la spec) | A-1 de 0.3 lo cita así: la regla de «siempre hay sesgo» y la glosa por separado |
| 63 (d2e84172 habla del extremo de la H4 anterior; la que cubre el rango es `ev-v9-000902`) | A-1 de 0.3: F7 #2 lo cubren `ev-v9-000902` (el rango) y d2e84172 (la H4 anterior) |
| 64 (52 % con la lectura (a), 69 % con la (b)) | decisión 1 y B-2 |
| 65 (RC2:699 solo nombra «S-22 y S-19 con sus esquemas y el 52 %») | B-3 cita ACTIVAR-SESION-06-MOTOR.md:792 y :803 |
| 67 (A-46 RESUELTA) | B-10: la pregunta dice que no la reabre |
| 73 (el repo no pide `Fuente:` para `knowledge/evidence/`) | 0.5: va igual, por costumbre (`b3680161`) |
| 76 y H7 (R0.3 HECHA y `NA:F`) | decisión 14 |
| H1 (paso 5 de «Antes») | decisión 11 |
| H2 (A-44 RESUELTA; la regla 2 vieja en ACTIVAR-A35-A44.md:46-51) | decisión 6 |
| H3 (`engine/decisiones.py:7-8`) | decisión 12 |
| H4 (los ejemplos de la caja iban al visor) | decisión 13 (ii) |
| H8 (`ev-v15-000553-9d95178a`, en tensión) | A-6 de 0.3 |
| H9 (el 118 de 286 es de la diaria del respaldo) | medido sobre la línea base: 100 `stop_movido` frente a 247 (0.3, A-5) |
| H10 (F dice que las láminas no se enseñan) | decisión 14 |
| «Lo que no pude comprobar»: la compuerta, `evidence new --transcripcion`, `propose --check` | medido en esta sesión: 0.1, 0.4 y 0.5 |

El informe del auditor, tal cual, en el Apéndice A.

## Lo que necesito que decidas (PARADA de la fase 0)

0. **F7 #10, la transcripción que se cita.** `evidence new` rechaza citar la transcripción vieja de v14 (`cli.py:658-663`, medido en 0.5), y `evidence accept` igual; y la frase está a 0:44:05-0:44:09, no a 0:42:02. Opciones: (a) citar #10 de la transcripción **activa** de v14 (`tr-v14-…-1d289df6`), que trae el mismo segmento, con la ventana 0:44:04-0:44:11 (medida: ACEPTADA); (b) cambiar la CLI para que acepte una transcripción no activa. Recomiendo (a): el texto citado es el mismo y no toca código ni validación. Coste de (b): fuera del contrato (cli.py solo en sus dos cadenas) y toca la verificación de citas.

1. **El reparto de las preguntas**, con las filas de 0.3 (como mucho seis técnicas por día):
   - **7a (sesion-07)**: S-1 el rango de H4 (A-1; julio 30); S-2 el break even (A-5; el dinero: 100 de 247 posiciones movieron el stop); S-3 qué zonas cuentan como zonas de control (A-2; julio 8); S-4 A-35 (A-6; el dinero y bloqueante); S-5 cuándo se coloca la orden respecto de la ruptura del punto (A-4; julio 5 y toda orden stop); S-6 las entradas válidas que deja sin tomar (A-3; la lectura de las 39 de más). Después, el bloque de días.
   - **7b (sesion-08)**: S-1 «¿de qué sale tu stop?» (B-1; julio 23, total 68); S-2 S-22 (B-2; quita el 52 % de los puntos con la lectura «la última verde» y el 69 % con «toda la racha», ACTIVAR-SESION-06-MOTOR.md:148-154); S-3 S-19 (B-3; 32 rechazos); S-4 el «igual» y la caja de la reentrada (B-4; 4 P7); S-5 A-53 (B-5); S-6 A-43 con las horas escritas (B-6). Después, el bloque de días, y al final, fuera de las seis, la tarde del 10 de julio.
   - **No caben en las seis** y quedan escritos al final de PREGUNTAS-7B.md, con sus filas, para que la activación de la 7a (que revisa ese documento antes de grabar, D4) cambie una por otra si la cifra lo pide: los dos esquemas (B-7; julio 3), seguir tras tres pérdidas (B-8; julio 2), la alternancia (B-9; se solapa con S-3 de la 7a) y A-46 por la toma (B-10).
   Opciones del orden de la 7a: (a) el rango primero y el break even segundo; (b) el break even primero, como decía ACTIVAR-SESION-06.md:562. Recomiendo (a): el rango es la que más filas mueve (30 de las 81 de julio) y el break even no mueve ninguna pareja; el dinero entra igual en el segundo y el cuarto puesto. **Lo que no se cumple con (a): el punto 1 de ACTIVAR-SESION-06 («la primera de la hoja»)**. Coste de (b): la pregunta de más filas pasa al segundo puesto. Y para la 7b, (a) las seis del encargo (A-53 y A-43 sin filas medidas) o (b) por la cifra, los dos esquemas y las tres pérdidas en lugar de A-53 y A-43. Recomiendo (a): A-53 y A-43 son ambigüedades abiertas que la sesión 6 contestó en parte, los dos esquemas dependen de lo que responda en las zonas de control (7a) y D4 deja a la activación de la 7a cambiarlas con la cifra nueva. Coste de (b): A-53 y A-43 siguen abiertas otra sesión.

2. **La sustituta de P2 a 4-10 puntos, de mayor cociente**: la siguiente que cumple a) a c) es 2026-01-13 07-11 (2,07), que ya está en la lista (P5). Opciones: (a) la siguiente distinta, 2026-01-19 11-15 (1,78); (b) dejar 2026-01-13 07-11 en los dos sitios y la lista una más corta. Recomiendo (a): la lista quiere un ejemplo más de la caja, y 01-13 ya sirve a B-1 con su cociente de stop (2,33). Coste de (b): un ejemplo menos.

3. **La sustituta de 2026-07-10 07-11**: la siguiente de menor cociente que cumple a) a c) es 2026-07-17 07-11 (0,48), y D3 f dice «del 17 solo va 11-15». Opciones: (a) leer D3 f para todo el bloque y tomar la siguiente, 2026-01-21 07-11 (0,50); (b) leer D3 f solo para el rango de H4 y tomar 2026-07-17 07-11, que cumple a) a c) (D3 d solo pide eso). Recomiendo (a): D3 f se escribió como condición del bloque, y 2026-07-17 11-15 va en la lista de la 7a (reserva o no), así que con (b) el trader vería el mismo día en los dos días de sesión. Coste de (a): un ejemplo de julio, con vídeo, menos.

4. **Los días.**
   - **7a**, en orden de filas: 2026-07-07 11-15 (rango; 9 filas), 2026-07-02 11-15 (zonas de control; 10 filas, 3 con el gate RN-009), 2026-07-03 07-11 (colocación; 6), 2026-07-15 11-15 (rango; 5). Reservas: 2026-04-13 07-11 (zonas de control; 4) y 2026-07-06 07-11 (rango; 4). Cumple lo pedido: dos del rango, una de las zonas de control y 07-03 07-11. 2026-07-07 07-11 (5) no entra para no repetir día con su tarde.
   - **7b**, en orden de filas: 2026-01-13 07-11 (8; B-1 y B-8), 2026-04-15 11-15 (5; el trader no opera: A-3 y B-1), 2026-01-07 07-11 (4; B-1, cociente 3,14), 2026-01-19 11-15 (3; B-1, si decisión 2 a). Reservas: 2026-01-21 07-11 (3; B-1, si decisión 3 a) y 2026-01-22 11-15 (3; P1 por una ruptura de 2 puntos, toca A-16: material). 2026-07-02 11-15 va a la 7a y entra por ella en la 7b 2026-07-16 07-11 (0,34; 1 fila), que propongo como tercera reserva y no en el bloque: es una pareja (T0) con el stop distinto, y la caja ya está en las otras.
   Opciones: (a) estas; (b) cambia las que quieras, con D3 ya comprobada para todas las de arriba. Recomiendo (a).

5. **S-7 (el gráfico 1 de la sesión 6).** Opciones: (a) no entra: los gráficos 2 a 6 ya no existen, lo que dijo está citado (`ev-v17-004338-c8befc62`, `ev-v17-004407-42808be7`) y las láminas llevan el contexto que pidió (las líneas de M15); (b) que su día entre al bloque como lámina: el día está en la clave de la sesión 6, que guarda Aleks fuera del repo, y la sesión no lo sabe. Recomiendo (a). Coste de (b): leer una clave que no está en el repo y repreguntar lo dicho.

6. **La NOTA de ACTIVAR-A35-A44.md** (cabecera, el cuerpo no se toca), con H5 y H6: «**NOTA (2026-11-11, rama `trabajo/preparacion-sesion-7`; el cuerpo no se toca).** Desde ADR-0089 (rama `trabajo/activar-sesion-06-motor`), cuándo vuelve a contar el trader lo decide `perdida_trader_reinicio` (`primera_sesion_dia_siguiente`, CONFIRMED, `fb-2026-11-04-sesion-06-6886938e`); `perdida_trader_reinicio_huso` sigue en el registro, UNKNOWN y SIN EFECTO con ese valor, y solo contaría con `medianoche_huso`; A-44 está RESUELTA desde esa rama (`ambiguedades.yaml:1442`), así que lo que la NOTA del 2026-11-05 dice de A-44 («siguen ABIERTAS») ya no vale para ella. Las filas de §0 y §1 que dan el reinicio a `perdida_trader_reinicio_huso` (`:71`, `:126-127`) describen lo de antes de ADR-0089 (`ACTIVAR-SESION-06-MOTOR.md`, H9 y hallazgo del consultor). Y la regla 2 de `SESION-DE-PREGUNTAS.md` cambió el 2026-11-11 (ADR-0093): el bloque de días enseña las láminas del bot, con la orden, el stop y el objetivo; lo de «cortados antes de la orden, sin fecha» de arriba (`:46-51`) es la regla anterior.» Opciones: (a) esta; (b) solo lo del reinicio, sin A-44 ni la regla 2. Recomiendo (a): H6 queda falsa con el recuadro en el mismo commit, y A-44 RESUELTA es un hecho (auditor, H2).

7. **Technical Debt de `graficos_sesion.py`** (H8), para el cierre: «`scripts/graficos_sesion.py:66-71` y `tests/unit/test_graficos_sesion.py:310-318` dicen que su constante es la regla 2 de SESION-DE-PREGUNTAS.md, con abril del 1 al 30 y agosto del 1 al 31; desde ADR-0093 la regla 2 toma los días de `cobertura_material` y D3 (abril hasta el 29, agosto desde el 3), y el guion queda como el precedente de la sesión 6 (PREPARACION-SESION-7.md §0.2).» Opciones: (a) esta; (b) arreglar la constante aquí. Recomiendo (a): D1 dice que el guion no se toca.

8. **Las dos cadenas de `cli.py`.** Docstring (`:2709-2711`): «… Desde ADR-0093 las laminas se ensenan al trader en el bloque de dias de la sesion (regla 2 de SESION-DE-PREGUNTAS.md; docs/runbooks/LAMINAS.md).» Ayuda (`:3363`): «…, fuera del repositorio; para el bloque de dias de la sesion (ADR-0093)». Opciones: (a) esas; (b) quitar solo «todavia» y la frase del ADR. Recomiendo (a).

9. **El índice del ADR-0093** (0.8), con tres precisiones: (i) el mes de construcción de §4 que corre cada activación es **julio**, el único con vídeo y el del pivote (RUMBO §1 d dice «un mes de construcción»); (ii) ADR-0093 dice que cierra la NOTA de ADR-0092 §6, y ADR-0092 no se toca (no está en lo que entra); (iii) la regla de la ingesta (ningún fotograma antes de que la voz o uno ya abierto sitúe el tramo) va al ADR, y que la skill `ingerir-sesion` lo diga se propone para el cierre (`.claude/` está protegida). Opciones: (a) el índice con las tres; (b) dejar a cada activación elegir el mes. Recomiendo (a): un mes fijo hace comparables los deltas. Coste de (b): deltas de meses distintos no se suman.

10. **El pivote** (0.7): `docs/plan/PIVOTES-SESION-7.yaml` y `tests/unit/test_pivotes_sesion_7.py`, con el sha256, la lectura estricta y el que rompe. Opciones: (a) eso; (b) otra ruta. Recomiendo (a).

11. **El paso 5 de «Antes» de SESION-DE-PREGUNTAS.md** (`:89-91`: «en la pantalla que se graba, ningún gráfico que no sea de los preparados según la regla 2»), que el encargo no nombra en F1.7 (auditor, H1): con el ADR, el trader carga él su replay. Opciones: (a) un recuadro más en el mismo commit, que copia el texto anterior y dice que en el bloque de días la pantalla es el replay que abre el trader (y nada más: ni otro backtest ni Analytics); (b) dejarlo. Recomiendo (a): sin él, el runbook se contradice. Amplía lo que entra (el mismo fichero, otro paso): lo digo como desviación.

12. **Otras dos líneas de Technical Debt para el cierre** (auditor, H3): `src/botsito/engine/decisiones.py:7-8` dice «Como se convierte una respuesta del trader en regla lo fijara el ADR del metodo (RUMBO §1); esto no lo adelanta»: queda viejo con ADR-0093 §4 y `engine/` está protegido. Opciones: (a) línea de Technical Debt; (b) tocar el docstring aquí. Recomiendo (a).

13. **Desviaciones que declaro, para que las des por buenas:** (i) D4 se aparta de R4.5 «Hecho cuando» (`HOJA-DE-RUTA.md:413`) y de F («la preparación genera … las de los días que elija»): las láminas de la 7b no salen aquí (auditor, H5); (ii) los ejemplos de la caja iban «dos al visor en la rama de la preparación» (`RECORRIDA-CONSTRUCCION-2.md:1323`, `:1333`): van al bloque de días de la 7b con sus láminas, y el visor no se usa (auditor, H4); (iii) D2 da dos ids a una sesión partida en dos días, y la sesión 5 se grabó en dos días con un solo id (`2026-10-23-sesion-05`; auditor, matiz 15): aquí no casa porque la 7a se activa antes de grabar la 7b; (iv) de las 29 filas del porqué de D5, 2 (las P1 de 2026-07-01 07-11) son del 1 de julio, que no va a la sesión 7 como día (VIDEO-JULIO.md:598): la pregunta es abstracta y las mueve igual; el ADR lo dice con la cifra (auditor, H6); (v) julio es `provisionales_con_video` y no `dias_con_video` en `criterio_fidelidad.yaml:63-64` (auditor, matiz 31): el ADR dice «el único mes con vídeo (provisional)».

14. **El cierre: R0.3 HECHA** exige quitar `NA:F` de todo su bloque (`HOJA-DE-RUTA.md:43`; `problemas_b`, `test_hoja_de_ruta.py:139-149`), como se hizo con R4.5 (auditor, H7). Y el texto nuevo de F quita también «Las láminas no se enseñan al trader hasta que el ADR del método cambie la regla 2» (auditor, H10). Lo compruebo sobre copias en la PARADA final.

Espero tu respuesta a la PARADA.

## Exposiciones del día

2026-11-11, declaradas en HOLDOUT-EXPOSICIONES (fila de esta rama) antes del primer `make check`:
cada `make check` lee el M1 de marzo y calienta con el de junio (Technical Debt); la compuerta
(`casos_reservados`, `casos_ocultos`), solo contada; anexos commiteados de construcción; la
transcripción filtrada por la CLI (`corpus transcript show` de v11, v12 y v14, y `evidence propose`
de v11 con `--salida` fuera del repo). Ninguna cruda, ningún fotograma, ninguna corrida del arnés ni
de `motor laminas`.

## Desviaciones

1. **La apertura y la fase 0 van en un solo commit.** El primer `make check` de la apertura salió en
   verde y no selló (`knowledge-validate.log` sin seguir); en lugar de repetirlo para la apertura y
   otra vez para la fase 0 (unos 23 minutos cada uno), el segundo sella las dos. El commit trae solo
   lo que abrir-rama y fase-cero escriben.
2. **La respuesta a la PARADA, los anexos de la fase 0 y la fila de exposiciones de F6 van en el
   commit de F1.** `make check` no sella con cambios sin estadiar, y cada uno tarda unos 20
   minutos: el ADR no se mezcla con nada de F2 a F6, solo con lo que lo precede.
3. **F6 se hizo antes que F2** (encargo: «F2 … commit propio, antes de F3 a F6»; revisor, b6). Las
   láminas no dependen del pivote ni de F1 (el motor es el de `3de24780`), y se lanzaron mientras se
   escribía F1, para no tener la máquina parada; F2 se commiteó después (`a2d830e5`). No cambia lo
   que pre-registra F2: ninguna cifra del pivote sale de las láminas.
4. **La NOTA de ACTIVAR-A35-A44, un ajuste más** que los dos declarados en «Cómo se aplica la
   respuesta» (revisor, b9): en la primera versión, la cita de A-44 iba sin la línea
   (`knowledge/spec/ambiguedades.yaml`); se repuso la línea del texto aprobado (`:1442`).
5. **Las fechas del día anterior en dos anexos** (revisor, b7): `dias-d3.txt` y `sustitutas.txt`,
   commiteados en `3e1995df`, escribían como «día de mercado anterior» los de antes del 1 de abril,
   del 1 de julio y del 3 de agosto, calculados por calendario (sin consultar su partición). Los dos
   guiones ya no imprimen la fecha cuando el día anterior no es de construcción, y sus salidas se
   regeneraron; la historia de git conserva la versión vieja (a la PARADA final y a
   HOLDOUT-EXPOSICIONES).

## Los make check de la rama

| Commit | exit | passed / failed | Sello | Pico |
|---|---|---|---|---|
| apertura, primer intento | 0 | 3420 / 0 | **no** (`knowledge-validate.log` sin seguir) | 312 MiB |
| `3de24780` apertura y fase 0 | 0 | 3420 / 0 | `db5af9d5…` | 313 MiB |
| `3e1995df` F1 (y la respuesta, los anexos y la fila de F6) | 0 | 3420 / 0 | `cfdd9d39…` | 311 MiB |
| `a2d830e5` F2 | 0 | 3424 / 0 | `80c3aa75…` | 314 MiB |
| `958a7b9a` F3 a F5 | 0 | 3430 / 0 | `cb29ec17…` | 312 MiB |
| el commit de las correcciones del revisor y el cierre del informe | ver su mensaje | | | |

## Respuesta del consultor a la PARADA de la fase 0 (2026-11-11)

Copiada tal cual:

> Modelo: Opus 5.5 · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA de la fase 0 de trabajo/preparacion-sesion-7 (2026-11-11). Cópiala tal cual al final del encargo y del informe, en «Respuesta del consultor a la PARADA de la fase 0», con su fecha, y aplícala punto por punto (skill fase-cero). Buena fase 0: todo medido, y la cuenta del pivote cuadra.
>
> 0. (a). F7 #10 se cita de la transcripción activa de v14, con la ventana 0:44:04-0:44:11. VIDEO-JULIO.md no se toca: lo medido queda en tu §0.5.
> 1. (a) en los dos días. 7a: S-1 el rango de H4, S-2 el break even, S-3 las zonas de control, S-4 A-35, S-5 la colocación y S-6 F7 #10. 7b: las seis que propones, y al final, fuera de las seis, la tarde del 10 de julio. Al final de PREGUNTAS-7B.md, con sus filas, los cuatro que no caben (B-7 a B-10). El incumplimiento del punto 1 de ACTIVAR-SESION-06 queda declarado como lo escribes.
> 2. (a): 2026-01-19 11-15.
> 3. (a): 2026-01-21 07-11. D3 f es una condición del bloque entero. La escribí ambigua (errores, abajo).
> 4. (a), tal cual. En la 7a: 2026-07-07 11-15, 2026-07-02 11-15, 2026-07-03 07-11 y 2026-07-15 11-15; reservas, 2026-04-13 07-11 y 2026-07-06 07-11. En la 7b: 2026-01-13 07-11, 2026-04-15 11-15, 2026-01-07 07-11 y 2026-01-19 11-15; reservas, 2026-01-21 07-11, 2026-01-22 11-15 y, como tercera, 2026-07-16 07-11.
> 5. (a): S-7 no entra.
> 6. (a), con tu texto.
> 7 y 12. (a), en UNA sola línea de Technical Debt, para no engordar PROJECT_STATE: «Dos textos que ADR-0093 deja viejos y que trabajo/preparacion-sesion-7 no podía tocar: scripts/graficos_sesion.py:66-71, con su test (su constante ya no es la regla 2), y engine/decisiones.py:7-8 (el ADR del método ya existe) (PREPARACION-SESION-7.md §0.2, H8 y H19).» Y H16 no hace línea nueva: se añade al final de la que ya existe sobre la skill ingerir-sesion («… y no dice que ningún fotograma se abre antes de que la voz o uno ya abierto sitúen el tramo, ADR-0093 §2»). Las dos van a las propuestas de la orden de cierre, medidas con wc -c.
> 8. (a).
> 9. (a), con las tres precisiones y una más en §4. Si el delta de julio de una activación no casa con lo que declaró, la regla no se retoca hasta que la cifra salga: PARADA, el consultor vuelve a la voz del trader y decide si la respuesta se entendió mal. El delta nunca elige entre dos lecturas de un parámetro. Y el ADR dice que el delta de cada activación es diagnóstico (ADR-0092 §6): la única lectura de julio que decide algo es la del pivote (D5).
> 10. (a).
> 11. (a): el recuadro del paso 5 de «Antes». La desviación queda aceptada.
> 13. Las cinco desviaciones, aceptadas tal como las declaras.
> 14. De acuerdo. Lo compruebas sobre copias en la PARADA final, con el texto nuevo de F entero.
>
> Además:
> 15. Las notas de la evidencia nueva solo llevan lo de su propia cita: es el patrón «Las notas de un registro… traen contenido de otros items» de ERRORES-RECURRENTES.md (:37), aplicado a la evidencia. La contradicción de F7 #6 con ev-v16-000234-9a4fa375 se escribe en el informe y en las líneas «Para Aleks» de S-5 de la 7a, no en las notas del ítem. Y las notas de F7 #2 no nombran ev-v9-000902-25db5bf5.
> 16. Tu desviación del primer make check, aceptada. La salida de una herramienta va siempre a la carpeta de trabajo, nunca a la raíz del repo.
> 17. Para la fila de ERRORES-RECURRENTES del cierre, los errores del consultor que llegaron a esta rama: 5, todos menores (consultor en Opus 5.5).
>    · La regla del 27-oct y la lista de RECORRIDA-CONSTRUCCION-2 F3.5 escribían casos en lugar de la condición, y dejaron pasar 2026-01-02 11-15. Es la lección que ya trae el encargo.
>    · El encargo daba F7 #10 como citable de la versión vieja de v14 con --transcripcion, y a 0:42:02; lo repetía de VIDEO-JULIO §7. evidence new lo rechaza y la frase está en 0:44:05. Lección: lo que una herramienta acepta como opción no prueba que haga lo que se dice; se ejecuta.
>    · F1.7 no nombraba el paso 5 de «Antes».
>    · La NOTA de ACTIVAR-A35-A44 se quedaba corta: faltaban A-44, que está RESUELTA, y la regla 2 vieja de :46-51.
>    · D3 f se podía leer solo para el rango de H4, y dejaba en el aire 2026-07-17 07-11 para la 7b. Lección: una exclusión dice a qué conjunto se aplica.
>    El segundo punto de la lista del encargo (la primera versión, parada por el auditor del consultor) no llegó a la rama: entra como lección, sin contarlo.
>
> Sigue sin parar con F1 a F6 y la PARADA condicional del encargo. Después: push como fix/preparacion-sesion-7 con su CI (el número de run), el revisor con los ocho alcances del encargo, su informe pegado al final del tuyo, y la PARADA final con lo que pide el encargo y la ruta de C:\Users\USER\Desktop\laminas-sesion-7a.
>
> Rama lista para revisión, NO cerrada.

### Cómo se aplica la respuesta, punto por punto

| Punto | Hecho | Dónde |
|---|---|---|
| 0 | F7 #10 de la transcripción activa de v14, 0:44:04-0:44:11; VIDEO-JULIO.md no se toca | F3 |
| 1 | el reparto: 7a S-1 rango, S-2 break even, S-3 zonas de control, S-4 A-35, S-5 colocación, S-6 F7 #10; 7b las seis de B-1 a B-6 y, fuera, la tarde del 10 de julio; B-7 a B-10 al final de PREGUNTAS-7B.md; el incumplimiento del punto 1 de ACTIVAR-SESION-06, declarado (§0.2, H3) | F4 |
| 2 y 3 | 2026-01-19 11-15 y 2026-01-21 07-11 | F4 |
| 4 | los días, tal cual | F4 y F6 |
| 5 | S-7 no entra | — |
| 6 | la NOTA de ACTIVAR-A35-A44.md, con el texto de la decisión 6. Dos ajustes de forma, declarados: los números de línea que cita son los de después de insertarla (`:84`, `:139-140` y `:59-64`, antes `:71`, `:126-127` y `:46-51`), y el pasaje de la regla 2 vieja va «de abajo», no «de arriba», porque la NOTA queda delante | F1 |
| 7 y 12 | una línea de Technical Debt y la ampliación de la de `ingerir-sesion`, a las propuestas de cierre, medidas con `wc -c` | PARADA final |
| 8 | las dos cadenas de `cli.py` (la ayuda, partida en dos líneas por ruff, E501) | F1 |
| 9 | ADR-0093 con el índice de §0.8, las tres precisiones y la de §4 (PARADA ante un delta que no casa; el delta no elige entre dos lecturas; el delta es diagnóstico y solo decide el pivote) | F1 |
| 10 | `docs/plan/PIVOTES-SESION-7.yaml` y `tests/unit/test_pivotes_sesion_7.py` | F2 |
| 11 | el recuadro del paso 5 de «Antes» | F1 |
| 13 | las cinco desviaciones, aceptadas | «Desviaciones» |
| 14 | sobre copias, en la PARADA final | PARADA final |
| 15 | las notas de la evidencia, solo de su cita; la contradicción de F7 #6 con `ev-v16-000234-9a4fa375`, en este informe (§0.5 y F3) y en «Para Aleks» de S-5 de la 7a | F3 y F4 |
| 16 | la salida de las herramientas, a la carpeta de trabajo | toda la rama |
| 17 | los cinco errores del consultor, a la fila de ERRORES-RECURRENTES del cierre | PARADA final |

## F1 · ADR-0093 (2026-11-11)

- `docs/adr/0093-el-metodo-de-las-sesiones-y-de-las-activaciones.md` y su fila en
  `docs/adr/README.md`. §1 a §7 son los puntos 1 a 7 de F1, con RUMBO §1 a) a e) citado en cada uno
  y las precisiones de la respuesta, puntos 9 y 11.
- `docs/runbooks/SESION-DE-PREGUNTAS.md`: la cabecera, la regla 2, el paso 5 y el paso 6 de
  «Antes», cada uno con su recuadro «Por qué cambió», que copia dentro el texto anterior. Los dos
  recuadros que ya llevaba la regla 2 no se tocan; el del 2026-09-28 queda sustituido en su
  salvaguarda por el nuevo, que lo dice. Aplicado con un guion de la carpeta de trabajo que busca
  cada texto viejo tal cual y sale sin escribir si no está una vez.
- `docs/runbooks/LAMINAS.md`, «Lo primero», con su recuadro.
- `src/botsito/cli.py`: el docstring de `motor_laminas` y la ayuda de `motor laminas`. Ningún test
  las mira.
- `docs/runbooks/ACTIVAR-A35-A44.md`: la NOTA de cabecera.
- El bloque `ids-inexistentes` de ADR-0093 sale del encargo y de este informe.
- En el mismo commit, delante: la respuesta a la PARADA copiada en el encargo y aquí, los guiones y
  las salidas de la fase 0 en `docs/validation/anexos/PREPARACION-SESION-7/` y la fila de
  HOLDOUT-EXPOSICIONES de F6 (desviación 2).

## F6 · Las láminas de la 7a (2026-11-11)

Fila de HOLDOUT-EXPOSICIONES antes de la primera invocación. Las seis sesiones aprobadas (cuatro y
dos reservas; respuesta a la PARADA, punto 4), en un orden barajado que no se escribe en el repo.

1. **El ensayo**, en un clon desechable: `git worktree add --detach C:/wt-p7 HEAD` (sobre
   `3de24780`; ruta corta, por el límite de rutas de Windows), con su `config/settings.local.toml`
   (`[rutas].data` absoluto al `data/` real) y la salida en la carpeta de trabajo de la sesión:
   `uv run botsito motor laminas --sesiones <las sesiones de la 7a, en el orden de clave.txt> --salida <carpeta de trabajo>/ensayo-7a`.
   exit 0; 45 ficheros; 633,8 s; pico del proceso 644,2 MiB. Las dos corridas dan lo mismo,
   `(31, 192, 24, 1150, 0, 32, 0)`: las 31 parejas, las 192 de más y las 1150 órdenes de la línea
   base.
2. **La buena**, desde el repo, con el mismo orden:
   `uv run botsito motor laminas --sesiones <las sesiones de la 7a, en el orden de clave.txt> --salida C:\Users\USER\Desktop\laminas-sesion-7a`
   (la lista sustituida por su marcador: desviación declarada, la misma de LAMINAS). exit 0; 45
   ficheros; 528,7 s; pico 643,0 MiB; las dos corridas, `(31, 192, 24, 1150, 0, 32, 0)`. El árbol de
   trabajo llevaba entonces sin commitear lo de F1 (las dos cadenas de `cli.py` y documentos); el
   motor, el mismo de `3de24780`.
3. **La buena frente al ensayo**: los 45 ficheros, por sha256 (guion de la carpeta de trabajo que
   solo hashea), **0 distintos**. `clave.txt` no se abrió. El clon se retiró (`git worktree remove`).

**Por sesión**, de la consola de `motor laminas`, **sin decir qué carpeta es cuál** (corregido tras
el revisor, b2: con la carpeta al lado, la tabla de §0.4, que da las filas del trader y del bot de
cada sesión, permitía deducir la clave, porque las seis parejas de tipo a y tipo b son distintas).
En el orden de las láminas por sesión, de menos a más: 4 (0 de tipo a y 4 de tipo b), 4 (1 y 3),
5 (1 y 4), 6 (5 y 1), 9 (5 y 4) y 10 (5 y 5); **en total 38 láminas, 17 de tipo a y 21 de tipo b**;
en las 38, la H4 que fija el sesgo cae dentro de la ventana. La versión de `3e1995df` daba la tabla
por carpeta: sigue en la historia de git (a la PARADA final).

**Dónde están:** `C:\Users\USER\Desktop\laminas-sesion-7a\`, con `sesion-01` a `sesion-06`, cada una
con su `indice.html`, y `clave.txt` en la raíz. Ninguna sesión salió con error: no hay PARADA.

## F2 · El pivote (2026-11-11)

- `docs/plan/PIVOTES-SESION-7.yaml`: D5 del encargo, literal (con sus tildes), en sus claves: `que_se_mide`,
  `linea_base` (14 parejas, 39 operaciones de más, P5 37 y P6 2, la fuente, la definición de cada
  cifra y que no son las 425 del Marcador), `minimos` (≥ 19 y ≤ 33), las tres `salidas`,
  `contingencia`, `por_que`, `lo_visto` y `adr_0092_6`. Lo que añadió la fase 0 (las 2 filas del 1
  de julio y las 4 de 2026-07-14 dentro de las 29; 8,8 y 15,4 %; julio en `provisionales_con_video`)
  va aparte, en `matices_medidos`, para que el texto de D5 quede como está. sha256
  `cef25e632b8edb529968a2036b5b43c91e0138e57650bcf3d97f3e5776797eef`, 4552 bytes, LF.
- `tests/unit/test_pivotes_sesion_7.py`: (1) el sha256, escrito en el test; (2) las cifras, el mes,
  `decision: ADR-0093`, las tres salidas en su orden y que no falte ningún texto, leído con
  `comun/yaml_estricto.leer_yaml`; (3) y (4) **rompen a propósito**: una copia con el mínimo 1 a 18
  (o el 2 a 34) cambia el sha256 y la comprobación devuelve exactamente ese problema. `uv run pytest
  tests/unit/test_pivotes_sesion_7.py -q`: 4 passed.
- `PROJECT_STATE.md`, «Tests Currently Passing»: 1998 → 2002 (`state check`).

## F3 · La evidencia (2026-11-11)

Con `evidence new`, la vía medida en §0.5 (respuesta a la PARADA, punto 0), una llamada por ítem;
cada cita, copiada de la transcripción filtrada (`corpus transcript show`) y localizada por la
verificación de citas antes de escribir. Las notas solo llevan lo de su propia cita (punto 15): de
dónde sale (F7 #n de VIDEO-JULIO.md §7), el ASR de una palabra de la cita si hace falta, y este
informe.

| F7 | Ítem | Vídeo, ventana | Transcripción | Tema · valor |
|---|---|---|---|---|
| #1 | `ev-v11-000038-fef9789d` (supersede a `ev-v11-000038-a322e483`) | v11 0:00:38-0:00:53 | activa (`tr-v11-…-d5da10be`) | `sesgo.h4.rango` |
| #2 | `ev-v11-000550-8a2230d4` (supersede a `ev-v11-000550-b140027d`) | v11 0:05:50-0:06:00 | activa | `sesgo.h4.rango` · `mecha` |
| #3 | `ev-v12-000650-370c4bd8` | v12 0:06:50-0:07:07 | activa (`tr-v12-…-cb502503`) | `sesgo.h4.importancia` |
| #6 | `ev-v12-000015-7fc04520` | v12 0:00:15-0:00:58 | activa | `entrada.breaker_m1_con_cuerpo` · `cuerpo` |
| #10 | `ev-v14-004404-ab0281c6` | v14 0:44:04-0:44:11 | **activa** (`tr-v14-…-1d289df6`), punto 0 | `backtest.entradas_sin_tomar` |

- **Corregido tras el revisor (a1):** las afirmaciones de los dos primeros ítems de v11 decían más
  que su cita («de H4» en #1; «la vela del rango» en #2: la cita dice «esta vela»). Como un ítem es
  inmutable, cada uno tiene un ítem nuevo que lo supersede con `evidence new --supersede`, el mismo
  tema y la misma cita, y la afirmación ajustada a la cita; PREGUNTAS-7A.md cita el nuevo de #1.
- `uv run botsito evidence contradictions`: `0 contradicciones abiertas`. #2 comparte tema y valor
  con el ítem de v9 del rango, así que no abre ninguna; #6 tiene tema propio.
- **La contradicción de F7 #6** (punto 15): la voz de v12 pide la ruptura del breaker en M1 con
  cuerpo (`ev-v12-000015-7fc04520`) y la sesión 5 fijó que en M1 la mecha vale
  (`ev-v16-000234-9a4fa375`, S-18, A-32 RESUELTA). TRAZAS-ABLACION la clasificó «contradicción con
  lo fijado» (decisiones de su PARADA final, punto 0). Va aquí y en «Para Aleks» de S-5 de la 7a,
  que la pregunta; no en las notas del ítem, y `_contradicciones.yaml` no la ve (temas distintos:
  el punto ciego de los temas hermanos, Technical Debt).
- **El trailer `Fuente:`**: el repo no lo pide para `knowledge/evidence/`
  (`DIRECTORIOS_CON_FUENTE`, `comun/historial.py:33`: solo `knowledge/spec/` y `knowledge/cases/`);
  el commit lo lleva igual, con los cinco ids, como las ramas de extracción.

## F4 · Las preguntas (2026-11-11)

`docs/sesion-7/PREGUNTAS-7A.md` y `docs/sesion-7/PREGUNTAS-7B.md`, en la forma de
`docs/sesion-6/PREGUNTAS.md`, con el reparto, los días y las reservas de la respuesta a la PARADA
(puntos 1 a 4):

- **7a (sesion-07)**: S-1 el rango de H4, S-2 el break even (A-13), S-3 las zonas de control
  (RN-009), S-4 A-35, S-5 la colocación (ADR-0064) y S-6 las entradas que deja sin tomar (F7 #10).
  El bloque de días (§1, «Para Aleks»): 2026-07-07 11-15, 2026-07-02 11-15, 2026-07-03 07-11 y
  2026-07-15 11-15, con 2026-04-13 07-11 y 2026-07-06 07-11 de reserva, qué pregunta sirve cada una
  y los pasos de ADR-0093 §2. Sin la clave de las láminas.
- **7b (sesion-08)**: S-1 dónde pone el 0 de la caja (A-48; hasta la revisión, «de qué sale tu stop», que preguntaba por el 1, ya decidido: revisor, b1), S-2 S-22, S-3 S-19, S-4 el «igual» y la caja
  de la reentrada (ADR-0083 D1), S-5 A-53 y S-6 A-43; S-7, la tarde que no está en el vídeo, al
  final y fuera de las seis. El bloque de días: 2026-01-13 07-11, 2026-04-15 11-15, 2026-01-07 07-11 y
  2026-01-19 11-15, con 2026-01-21 07-11, 2026-01-22 11-15 y 2026-07-16 07-11 de reserva. El recuadro
  de D4 arriba, y al final (§3) B-7 a B-10 con sus filas.
- **Ninguna pregunta lleva días ni fechas.** Las de TRAZAS-ABLACION.md 5.5 nombraban días y horas
  («El 3 de julio, entre las 08:02 y las 09:35…», «El 13 de abril a las 08:47…»): se reescribieron en
  abstracto, con esquemas inventados (S-3 y S-5 de la 7a); los días van al bloque, y los dice Aleks.
  La de material (S-7 de la 7b) no nombra el día: «Aleks te dice cuál»; el día va en su «Para
  Aleks». Tampoco se nombra el mes en lo que va al PDF («tu backtest grabado en vídeo»).
- **Lo que nos has dicho**, solo con ítems citables y su id, y cada cita copiada de su ítem; dos
  citas largas llevan `[...]` (la de `ev-v16-000234-9a4fa375` en S-5 de la 7a y la de
  `ev-v4-001909-54ac2edd` en S-3, que ya lo trae).
- Lo ya decidido no se repregunta: en S-1 de la 7a, «con mecha o con cuerpo» (decidido; su ítem,
  `ev-v11-000550-8a2230d4`, se creó igual como cita y no va a la hoja); en S-3, cuántas zonas
  (A-20); en S-4, la vela sin cuerpo de M15 (S-4 de la sesión 6). B-10 dice que A-46 no se reabre.
- Al escribir «Para Aleks» se midieron dos cosas que §0.3 daba de otra forma: `caja_bloque` = `r6`
  está CONFIRMED, no DEFAULT_AMBIGUOUS (`parametros.yaml:748-749`); y en A-35 cada opción cae en una
  de las tres de `liquidez_m15_mecha_que_vuelve` (`no_mueve`, `solo_la_contraria`, `cualquier_mecha`;
  `:555`).

## F5 · Las hojas 07 y 08 (2026-11-11)

- `scripts/transcribir_sesion.py`: `ORDEN_SESION_07` (S-1 a S-6) y `ORDEN_SESION_08` (S-1 a S-7),
  `CODIGOS_DE_SESION_TEXTO["07"]` y `["08"]` con los títulos de PREGUNTAS-7A.md y PREGUNTAS-7B.md
  (primera letra en minúscula, como la 06), `HOJAS["07"]` y `["08"]`, y `SESION_EN_CURSO = "07"`.
  La 06 no cambia.
- `tests/unit/test_transcribir_sesion.py`: `test_la_sesion_en_curso_es_la_06` se sustituye A
  PROPÓSITO por `test_la_hoja_06_sigue_en_hojas` y `test_la_sesion_en_curso_es_la_07` (con su
  motivo en el docstring: D2); nuevos `test_la_hoja_07_es_la_de_preguntas_7a` y
  `test_la_hoja_08_es_la_de_preguntas_7b` (leen los títulos de cada documento con el mismo
  `_RE_TITULO` de la 05 y la 06), `test_la_06_no_cambia_con_la_07_y_la_08`,
  `test_la_filtrada_de_la_07_agrupa_con_su_hoja`, y **el que rompe a propósito**,
  `test_un_codigo_de_la_hoja_que_no_esta_en_el_documento_rompe` (la hoja 07 con un S-7 de más da
  `S-7: no esta en PREGUNTAS-7A.md`). `uv run pytest tests/unit/test_transcribir_sesion.py -q`:
  todo en verde; ruff, limpio tras `ruff format`.
- «Tests Currently Passing»: 2002 → 2008 (`state check`).

## Las seis decisiones del encargo (D1 a D6), y dónde quedaron

| | Decisión (encargo, 2026-11-11) | Dónde |
|---|---|---|
| D1 | La hoja de la sesión 7 es el PDF del consultor, hecho desde docs/sesion-7/; no sale de `kit hoja`; J se queda en G.2 | cabecera de PREGUNTAS-7A.md y PREGUNTAS-7B.md; `kit hoja`, `hoja_preguntas.py` y `graficos_sesion.py` sin tocar; F y R4.3 sin J en las propuestas de cierre |
| D2 | 7a es `<AAAA-MM-DD>-sesion-07` y 7b `<AAAA-MM-DD>-sesion-08`; `SESION_EN_CURSO` = "07" aquí y "08" en la activación de la 7a | F5; ADR-0093 §1; recuadro de PREGUNTAS-7B.md. §0.6: nada más da por hecha una sola sesión 7 ni choca con el 08 |
| D3 | Los días por su condición a) a c); d) a f) | ADR-0093 §3; §0.4; `anexos/PREPARACION-SESION-7/dias-d3.txt` y `sustitutas.txt`; respuesta a la PARADA, puntos 2 a 4 |
| D4 | Las láminas de la 7b no se generan aquí | recuadro de PREGUNTAS-7B.md; desviación (i) aceptada (punto 13) |
| D5 | El pivote, pre-registrado | F2 (`docs/plan/PIVOTES-SESION-7.yaml` y su test) y ADR-0093 §6; la cuenta, medida en §0.3 y §0.7 |
| D6 | F7 #10 entre las seis técnicas de la 7a; los dos esquemas a la 7b; la tarde del 10 de julio al final de la 7b, fuera de las seis | S-6 de la 7a; B-7 en §3 de PREGUNTAS-7B.md (no cabe en las seis: punto 1); S-7 de la 7b |

## El encargo frente a lo hecho

| Del encargo | Hecho | Dónde |
|---|---|---|
| Abrir con abrir-rama, riesgo alto, tramo R4, encargo tal cual con un bloque `ids-inexistentes` delante | sí | `3de24780` |
| Base comprobada; PARADA si no cuadra | cuadra | «Base» |
| El vídeo de mapeo: PARADA si llega antes de aprobar los días | no llegó (Aleks no lo dijo) | — |
| FASE 0 con fase-cero y el auditor; PARADA | sí | §0, Apéndice A; respuesta del consultor |
| 0.7: 14 y 39 | 14 y 39 | §0.3, `pivote-julio.txt` |
| F1: ADR-0093, commit propio; recuadros; bloque fuera; referencias verificadas | sí (con la respuesta y los anexos delante: desviación 2) | `3e1995df`; F1 |
| F2: el yaml con D5 literal y su test con sha256, uno que rompe | sí | `a2d830e5`; F2 |
| F3: los ítems de F7 #1, #2, #3, #6 y #10 | sí; #10 de la transcripción activa (punto 0) | F3 |
| F4: PREGUNTAS-7A.md y PREGUNTAS-7B.md | sí | F4 |
| F5: hojas 07 y 08, `SESION_EN_CURSO` = "07", tests y uno que rompe | sí | F5 |
| F6: fila antes, ensayo en clon, una invocación buena, recuentos sin la clave | sí | F6 |
| Ninguna fecha reservada ni resultado en nada commiteado | en el último commit, sí: las fechas que van son de construcción; ninguna cifra de resultado. **Dos anexos de `3e1995df` escribían tres fechas de «día anterior» calculadas por calendario** (revisor, b7): corregido y declarado | desviación 5; PARADA final |
| Una fila de HOLDOUT-EXPOSICIONES por día de trabajo, antes | sí: tres filas del 2026-11-11 (el día, F6 y la de a2 y b7) | HOLDOUT-EXPOSICIONES |
| CI de Linux por `fix/preparacion-sesion-7` | ver «La CI» | «La CI» |
| Revisor con los ocho alcances, su informe al final | ver Apéndice B | Apéndice B |
| PARADA final con las propuestas comprobadas sobre copias | sí | «PARADA final» |

## Lo que no pude medir

- Las filas que mueven A-35, S-22, S-19, A-53, A-43 y A-46 por la toma: no hay recuento por fila
  commiteado (§0.3); se dan el mecanismo o las órdenes.
- Las filas del rango de H4 fuera de julio: las 24 P1 de los otros meses no están clasificadas
  contra el rango, porque no tienen vídeo.
- Si las láminas de la 7a se entienden en la sesión: lo revisan Aleks y el consultor antes (ADR-0093
  §2), con la carpeta del Escritorio.
- La aprobación de Aleks de los mínimos 19 y 33 (2026-11-11) está en el chat; aquí entra por D5 del
  encargo, que la declara.

## La CI de Linux (`fix/preparacion-sesion-7`)

Empujada `958a7b9a` (F1 a F6 y todo el código de la rama) como `fix/preparacion-sesion-7`: **run
43118024345**, `completed` / `failure`, con **1 failed, 3381 passed, 48 skipped**; el único fallo,
el aceptado de `RITUAL.md`: `tests/unit/test_cli.py::test_state_check_ok_on_real_repo` (PROJECT_STATE
declara `trabajo/preparacion-sesion-7` y la rama es `fix/…`). Medido con `gh run view 43118024345
--log-failed`. Lo que se commitea después (las correcciones del revisor) es documentación, evidencia,
dos anexos y un texto de la hoja 08.

Empujada después `e8a8c43b` (las correcciones del revisor): **run 43123877117**, `completed` /
`failure`, con **1 failed, 3381 passed, 48 skipped**, y el mismo único fallo aceptado (`gh run view
43123877117 --log-failed`). El commit de la respuesta a la PARADA final se empuja igual; su run va
en el mensaje final a Aleks y en el registro del cierre.

## Lo hecho con cada hallazgo del revisor

| # | Gravedad | Hecho |
|---|---|---|
| a1 | importa | **Corregido**: dos ítems nuevos supersedan a los de v11 con la afirmación ajustada a la cita (`ev-v11-000038-fef9789d` y `ev-v11-000550-8a2230d4`); PREGUNTAS-7A.md cita el nuevo; F3 lo dice |
| a2 | menor | **Corregido**: fila nueva de HOLDOUT-EXPOSICIONES del 2026-11-11 con F3 por su nombre |
| b1 | bloquea | **Corregido**: S-1 de la 7b pregunta ahora por el 0 (A-48 sigue ABIERTA por el 0; `orden_stop_punto`, opciones `ultimo_pivote_m1` y `referencia_de_la_toma`), con el 1 decidido en «Lo que nos has dicho» y en «Para confirmar»; su título en la hoja 08, «dónde pones el 0 de tu caja» |
| b2 | importa | **Corregido en el informe** (F6 sin la carpeta) y **a la PARADA final**: la versión de `3e1995df` sigue en la historia |
| b3 | importa | **Corregido**: la pregunta 1 de S-4 de la 7a ya no enuncia lo de hoy; su «Para Aleks» lo dice |
| b4 | importa | **Corregido**: fuera las tres repreguntas; «Para Aleks» de S-5 de la 7b cita entera `ev-v17-005914-55580dc0` y dice por qué no se repregunta |
| b5 | importa | **Corregido**: el valor de cada opción en S-1, S-3, S-4 y S-6 de la 7b |
| b6 | importa | **Declarado**: desviación 3 |
| b7 | importa | **Corregido** en los dos guiones y sus salidas; declarado (desviación 5) y en HOLDOUT-EXPOSICIONES; la versión vieja sigue en la historia (PARADA final) |
| b8 | menor | **Corregido**: el recuadro de LAMINAS.md copia también el título anterior |
| b9 | menor | **Corregido** (la línea `:1442` repuesta) y declarado (desviación 4) |
| b10 | menor | **Corregido**: la frase sale de ADR-0093 §3 (la lección va a ERRORES-RECURRENTES) |
| b11 | menor | **Corregido** en §0.5, con su marca |
| «no pudo comprobar»: el tema de F7 #6 | — | a la PARADA final, «lo que no me convence» |
| «no pudo comprobar»: el vídeo de mapeo | — | Aleks no avisó de que hubiera llegado; no hubo PARADA por él |

## Negativas de la guardia

Ninguna sobre algo legítimo que no tuviera la forma que ella misma propone. Las que hubo, todas por
encadenar en una llamada lo que pide ir en llamadas separadas (`git add` y `knowledge validate`;
`sed` y `state check`; `mkdir` y `python`; `python -` y otro `python`; `git status` y
`contrato_rama.py`): se partieron en llamadas como dice su mensaje. Dos más: un `for` en bash (se
leyeron los ficheros con Read) y un `awk` (se partió en `grep`). Y la conocida de `$'\r'` en un `grep -c`
(Technical Debt, carril de guardias): se contó con un guion de la carpeta de trabajo.

## PARADA final

**Las láminas de la 7a**, para que las revises (Aleks las sube en un ZIP a tu chat):
`C:\Users\USER\Desktop\laminas-sesion-7a\` (seis carpetas, 38 láminas; `clave.txt` en la raíz, que
guarda Aleks).

**Lo que no me convence:**
1. **Dos cosas que la historia de git conserva** y que el último commit ya no lleva: la tabla de F6
   por carpeta (revisor, b2: con §0.4 deja deducir la clave) y tres fechas de «día anterior» en dos
   anexos (b7). Las dos están en `3e1995df`. Reescribir la historia no se hace (`rebase` está
   bloqueado y el merge las traería igual). Decide si basta con lo declarado o si la clave de la 7a
   se cambia, volviendo a generar las láminas con otro orden barajado.
2. **El tema de `ev-v12-000015-7fc04520`** (F7 #6) es `entrada.breaker_m1_con_cuerpo`, y la cita no
   dice «M1». El contexto inmediato (0:00:58) habla de la liquidez de M15 (revisor, «lo que no pudo
   comprobar»). Es la contradicción que S-5 de la 7a le pregunta al trader. Si el «con cuerpo» fuera
   de M15, no habría contradicción con S-18. La pregunta no da por hecho ninguno de los dos.
3. **El orden de la 7b.** Las filas de cada sesión del bloque son las de la clasificación vigente.
   Tras activar la 7a cambian, y la activación tiene que revisar el orden (lo dice su recuadro).
4. **S-4 de la 7a, pregunta 1.** Se reescribió para no sugerir el «sí» (revisor, b3). Se aparta de
   la forma que fijó ACTIVAR-SESION-06 (punto 2), y lo dice su «Para Aleks».

**Las propuestas para la orden de cierre**, comprobadas sobre copias en memoria con `problemas_a` a
`problemas_d` de `tests/unit/test_hoja_de_ruta.py` (`anexos/PREPARACION-SESION-7/simular_cierre.py`;
no escribe nada): **[] en los cuatro** con todas a la vez; y un mutante (R0.3 HECHA dejando `NA:F` en
su bloque) da en `problemas_b` «NA:F esta HECHA y la letra sigue viva», que es lo que tiene que
pasar.

1. **F, entera** (sale «(1) J…» por D1 y «Las láminas no se enseñan…»; lo siguiente es la 7a y su
   activación):
   > F. Sesión 6 ACTIVADA en spec (F38n) y motor (F38o); S-22 y S-19 a la sesión 7. La re-corrida que cuenta está hecha (RECORRIDA-CONSTRUCCION-2.md: «no», cobertura 15.7 % y precisión 13.9 %; línea base anexos/RECORRIDA-CONSTRUCCION-2/cuenta-por-mes.txt). Las trazas del motor y la ablación por regla (TRAZAS-ABLACION.md; `motor decisiones`) y las láminas del bot (LAMINAS.md; `motor laminas`; R4.5) están hechas. La sesión 7 está preparada en dos días, 7a (sesion-07) y 7b (sesion-08) (PREPARACION-SESION-7.md; R4.3): el método en ADR-0093, que cambia la regla 2 de SESION-DE-PREGUNTAS.md (el bloque de días enseña las láminas); el pivote pre-registrado en docs/plan/PIVOTES-SESION-7.yaml; las preguntas en docs/sesion-7/; las láminas de la 7a fuera del repo. Siguiente, en este orden: (1) grabar, ingerir y activar la 7a; su activación genera las láminas de la 7b con su motor, revisa PREGUNTAS-7B.md y pasa SESION_EN_CURSO a "08"; (2) grabar, ingerir y activar la 7b, con la rama de S-22 y S-19; (3) la corrida de ADR-0070 §3 y la lectura del pivote (ADR-0093 §6). El vídeo de mapeo, si llega, SIN ABRIR y fuera del repo, por su propia rama. C, R5.7 y R6a en los huecos.
2. **R4.3**: «Qué es» con el reparto definitivo y «Depende de» sin J:
   > - **Qué es:** con el método de ADR-0093 (RUMBO §1): como mucho seis preguntas técnicas por día y un bloque de días con las láminas de R4.5. Preparada en `trabajo/preparacion-sesion-7` (PREPARACION-SESION-7.md), con el reparto que aprobó el consultor el 2026-11-11: 7a (sesion-07), el rango de H4, el break even (A-13), las zonas de control del esquema (RN-009), A-35, cuándo se coloca la orden (ADR-0064) y las entradas válidas que deja sin tomar (F7 #10), más el bloque de días (docs/sesion-7/PREGUNTAS-7A.md); 7b (sesion-08), dónde pone el 0 de la caja (A-48), S-22, S-19, el «igual» y la caja de la reentrada (ADR-0083 D1), A-53 y A-43, más el bloque de días y, al final, la tarde del 10 de julio (docs/sesion-7/PREGUNTAS-7B.md, con los cuatro que no caben). Las láminas de la 7b las genera la activación de la 7a. El pivote, pre-registrado en docs/plan/PIVOTES-SESION-7.yaml (ADR-0093 §6).
   > - **Depende de:** R4.4 y R4.5; el vídeo de mapeo del trader, si llega antes.
   Su «Estado» sigue ABIERTA: «Hecho cuando» es la 7a y la 7b activadas y el pivote leído.
3. **R0.3 HECHA**: «Refs» pasa a `ID:ADR-0092 · ID:ADR-0070 · ID:ADR-0093` (sin `NA:F`), y «Estado» a
   «HECHA (trabajo/preparacion-sesion-7, ADR-0093).».
4. **Technical Debt** (respuesta, puntos 7 y 12), medidas con `wc -c`:
   - línea nueva, **273 bytes** con su salto: «- Dos textos que ADR-0093 deja viejos y que trabajo/preparacion-sesion-7 no podía tocar: scripts/graficos_sesion.py:66-71, con su test (su constante ya no es la regla 2), y engine/decisiones.py:7-8 (el ADR del método ya existe) (PREPARACION-SESION-7.md §0.2, H8 y H19).»
   - la de la skill `ingerir-sesion`, ampliada al final: «…; segunda vez): rama corta de skills; y no dice que ningún fotograma se abre antes de que la voz o uno ya abierto sitúen el tramo, ADR-0093 §2.» (**+109 bytes**; con la F nueva, 297 bytes menos, el total sale 23.916 + 273 + 109 − 297 = 24.001).
5. **El tamaño de PROJECT_STATE**: 23.916 bytes en la rama hoy (`wc -c`), **24.001** con las cuatro
   propuestas aplicadas a la copia; por debajo del tope de 25.000 de `test_project_state.py`, sin
   recorte. El cierre cambia además Current Branch, Current Feature, Stable Main State y Last Stable
   Commit; volver a medir entonces.
6. **Para la fila de ERRORES-RECURRENTES**: en la columna del consultor, los cinco errores menores de
   la respuesta (punto 17), y la lección de la primera versión del encargo sin contarla. De la sesión:
   (a) el log de `knowledge validate` en la raíz dejó el primer `make check` en verde y sin sello
   (punto 16); (b) dos «Para Aleks» de §0.3 decían de un parámetro otra cosa que el registro
   (`caja_bloque` CONFIRMED, no DEFAULT_AMBIGUOUS; las tres opciones de A-35), y se corrigieron al
   escribir F4 (lección: el estado y las opciones de un parámetro se leen del registro al escribir,
   no se copian de un informe); y lo del revisor (Apéndice B): eje (a) 0 bloquea, 1 importa, 1
   menor; eje (b) 1 bloquea, 6 importa, 4 menor; todo corregido en el último commit o declarado. El
   bloquea, b1: la pregunta de A-48 preguntaba por el 1, que la sesión 6 ya decidió, en lugar del 0
   (lección: antes de redactar una pregunta «en parte», leer en `ambiguedades.yaml` qué parte quedó
   decidida, y no fiarse del resumen de un informe anterior). Y dos de holdout que solo vio el
   revisor: la clave de las láminas se podía deducir cruzando dos tablas del informe (b2), y un guion
   de medida escribía fechas de calendario de días que pueden ser reservados (b7). Lección: lo que se
   commitea se mira también por lo que deja deducir y por lo que el guion imprime de sobra, no solo
   por lo que dice.

## Estado

LISTA PARA REVISIÓN (2026-11-11): fase 0 respondida; F1 a F6 hechos, sin ninguna PARADA
condicional; la CI de Linux por `fix/preparacion-sesion-7`, runs 43118024345 y 43123877117, con el
único fallo aceptado (`test_state_check_ok_on_real_repo`); el revisor pasó (Apéndice B) y sus
hallazgos están corregidos o declarados; la PARADA final, arriba; la respuesta del consultor a la
PARADA final, al final del informe, con su primera parte aplicada (el cierre espera a
`/cerrar-rama`).

Rama lista para revisión, NO cerrada.

## Apéndice A · El informe del auditor del encargo (fase 0, 2026-11-11), tal cual

> ## Auditoría del encargo · trabajo/preparacion-sesion-7 · 2026-11-11
>
> Resumen: 78 afirmaciones. 64 son correctas, 0 incorrectas y 14 tienen matiz. Hay 10 herencias o requisitos que el encargo no recoge.
>
> Las cifras del pivote se cumplen contra el anexo: 14 parejas y 39 operaciones de más en julio, y 46 operaciones del trader con bot del mismo lado (14+14+15+3). La base también cuadra. Lo que hay que corregir son referencias incompletas y un cierre que, tal como está, rompe `test_hoja_de_ruta`.
>
> ### Afirmaciones
> | # | Afirmación (del encargo) | Veredicto | Evidencia |
> |---|---|---|---|
> | 1 | main y origin/main en e6b073f | CORRECTA | `git rev-parse --short main origin/main`: e6b073f1 las dos |
> | 2 | commit de estado sobre el merge b9904c5 | CORRECTA | `git log -1 --format=%P e6b073f`: b9904c54… |
> | 3 | tag stable/F38w-laminas, último «- Tag:» de HISTORIA | CORRECTA | HISTORIA.md:16971; el tag apunta a b9904c54 |
> | 4 | CI de main sobre e6b073f, run 43084251895, en verde | CORRECTA | `gh run view 43084251895`: `{"conclusion":"success","headBranch":"main","headSha":"e6b073f1…"}` |
> | 5 | ninguna otra rama local ni remota | CORRECTA | `git branch -a`: main, la rama en curso y origin/main |
> | 6 | PROJECT_STATE en 23.770 bytes | MATIZ | En main son 23.770 (`git show main:PROJECT_STATE.md \| wc -c`). En la rama, tras abrir-rama, son 23.916 (`wc -c`). La cifra final del encargo («que está en 23.770») ya no es la de la rama |
> | 7 | punto (2) de F, R4.3, tramo R4 | CORRECTA | PS:28. HOJA:384-390 (Refs con NA:F). contrato.yaml:4 = título de HOJA:316 |
> | 8 | RUMBO §1 define el método hasta que un ADR lo recoja | CORRECTA | HOJA:42-50 (R0.3 ABIERTA; «Hecho cuando: el ADR de RUMBO §1 existe») |
> | 9 | bloque ids-inexistentes con la forma de activar-sesion-05-motor.md:3-9; ids_citados cuenta los bloques citados; sale en el commit del ADR | CORRECTA | trabajo-activar-sesion-05-motor.md:3-9. ids_citados.py:46 (`_VALLA` admite `>`). Si el id ya existe, falla: :144-145 (DECLARADO_Y_EXISTE). Hay un solo bloque, en la línea 7 |
> | 10 | D1: sesion-6/PREGUNTAS.md:17-18, «La hoja es el PDF del consultor […] No sale de scripts/hoja_preguntas.py» | CORRECTA | PREGUNTAS.md:17-18 |
> | 11 | D1: J se queda en G.2, «antes de la próxima sesión que etiquete días» | CORRECTA | HOJA:713, :740 |
> | 12 | F lleva «(1) J, si la hoja sale de kit hoja» y R4.3 lleva «J, si la hoja sale de `kit hoja`» | CORRECTA | PS:28; HOJA:387 |
> | 13 | D2: regex `^\d{4}-\d{2}-\d{2}-sesion-\d{2}$` en ids.py:29 y paquete.py:77 | CORRECTA | Las dos líneas, literales |
> | 14 | D2: `SESION_EN_CURSO` = "06" y test_la_sesion_en_curso_es_la_06 | CORRECTA | transcribir_sesion.py:252; test_transcribir_sesion.py:666-669 |
> | 15 | D2: 7a y 7b llevan dos ids porque se activan por separado | MATIZ | Precedente medido: la sesión 5 se grabó en dos días con un solo id, `2026-10-23-sesion-05` (HOJA:672-673, A.3). No choca con el 08, pero la fase 0 debería citarlo |
> | 16 | D3: la regla del 2026-10-27 en RECORRIDA-CONSTRUCCION.md:1628 | CORRECTA | :1628, punto 2, con la condición literal |
> | 17 | la lista de F3.5 dejó pasar 2026-01-02 11-15 | CORRECTA | RECORRIDA-CONSTRUCCION-2.md:1340-1352 (solo saca el 1 de abril, el 1 de julio y «posible M») |
> | 18 | D3 a: `cobertura_material` da enero 2-30, abril 1-29, julio 1-17 y agosto 3-31 | CORRECTA | config.yaml:64-67, :74-77, :103-106, :113-116 |
> | 19 | la regla 2 dice «abril»; el 30 lo casa el ADR | CORRECTA | SESION-DE-PREGUNTAS.md:21 y :95. LAMINAS.md:262 (respuesta, punto 3) |
> | 20 | D3 b: hoy son 01-02, 04-01, 07-01 y 08-03 | CORRECTA | Son los primeros días de cada tramo (18). Dentro de cada tramo, el día de mercado anterior es del mismo tramo |
> | 21 | lo de más atrás no excluye: punto 6 de LAMINAS y ADR-0021 §1 (las velas no son holdout) | MATIZ | LAMINAS.md:237 y :268 son correctos. ADR-0021 §1 (:15-19) lo dice solo por exclusión (abrir = etiquetas o cifras del bot); lo explícito está en CLAUDE.md, punto 2 |
> | 22 | D3 c: anexos/RESPALDO-M1/horas_perdidas.py | CORRECTA | Existe; HORAS_PERDIDAS en :18-24 |
> | 23 | D3 d: 01-02 11-15 ocupaba dos sitios y es la misma operación | CORRECTA | RECORRIDA-CONSTRUCCION-2.md:1346-1348 |
> | 24 | 07-10 07-11 tiene horas perdidas a las 05Z; es la de menor cociente de P2 a 4-10 | CORRECTA | horas_perdidas.py:22 ("2026-07-10T05Z", dentro de 07-11, que en verano es 05Z-09Z). RC2:1347 |
> | 25 | caja-stop.txt y para-clasificar.txt | CORRECTA | Los dos están en anexos/RECORRIDA-CONSTRUCCION-2/ |
> | 26 | D3 e: 07-14 11-15, cuatro filas con gate RN-009, hora 12Z dentro, VIDEO-JULIO.md:590 | CORRECTA | TRAZAS:881; VJ:590; horas_perdidas.py:22 |
> | 27 | D3 f: VIDEO-JULIO clasifica 07-17 07-11 «sin clase» | CORRECTA | VJ:654 |
> | 28 | D4: las láminas de la 7b las genera la activación de la 7a | MATIZ | Se aparta de R4.5, «Hecho cuando» (HOJA:413: «las de los días que elija la preparación se generan allí»), y de PS:28 («la preparación genera con `motor laminas` las de los días que elija»). El motivo está dado; el informe tiene que declararlo como desviación |
> | 29 | D5: RUMBO §4, enmienda del 2026-11-10; esquema aceptado el 2026-11-09 | CORRECTA | RUMBO-2026-11.md:37; HOJA:386 |
> | 30 | ADR-0070 §3 y ADR-0092 §8 | CORRECTA | ADR-0070:54 (punto 3); ADR-0092:203-213 |
> | 31 | «Solo julio, el único mes con vídeo» | MATIZ | Julio está en `provisionales_con_video`, no en `dias_con_video` (criterio_fidelidad.yaml:61-65) |
> | 32 | línea base: RC2 §1.1 y §4; T0 de julio = 14 | CORRECTA | RC2:435 y :630. Anexo:5. `grep -c "^T0 pareja.*\| 2026-07-"` = 14 |
> | 33 | definición de las de más en TRAZAS-ABLACION.md:730-731 | CORRECTA | :730-732 |
> | 34 | P5 37 + P6 2 = 39 | CORRECTA | grep -c: P5 37; P6 «en sesion» 2, «en dia» 0 |
> | 35 | el Marcador cuenta otra cosa (425) | CORRECTA | HOJA:826. ADR-0092:59-60 (el recuento aparte de órdenes sin operación del trader) |
> | 36 | mínimos 19 y 33; «algo más de la mitad, 5»; «un 15 %» | CORRECTA | Aritmética: 19−14=5; 39−33=6, que es el 15,4 % de 39. La aprobación de Aleks no consta en el repo |
> | 37 | las 30 del rango de H4 de VIDEO-JULIO §4.2 con sus 10 P5 | MATIZ | El recuento es correcto: 5+4+1+14+5+1 = 30, con 3+6+1 = 10 P5 (VJ:603, 611-613, 651, 655, 657). Pero el «30» sale del recuento conjunto de §4.1 y §4.2 (VJ:657), y 2 de las 20 filas del trader son de 07-01 07-11, que VJ:598 y :885 marcan «[1-jul] no van a la sesión 7 (RUMBO §1 b)» |
> | 38 | 8 filas con gate RN-009 en TRAZAS 5.2 | CORRECTA | TRAZAS:878, 880 y 881 (3+1+4). No se solapan con las del rango |
> | 39 | la P2 de 07-03 07-11 | CORRECTA | VJ:609; TRAZAS:1390 |
> | 40 | 29 = 20 + 8 + 1 | CORRECTA | Las tres partes, arriba |
> | 41 | 46 = T0+P2+P3+P7 = 14+14+15+3 | CORRECTA | Anexo:5 y grep -c sobre las filas (14, 14, 15, 3) |
> | 42 | 14/46 es un 30 %; 29 filas darían unas 9 parejas | CORRECTA | 30,4 % × 29 = 8,8 |
> | 43 | las 10 P5 del rango son del otro lado | CORRECTA | VJ:603, :613, :651 («P5 otro lado») |
> | 44 | o4, o5, o6 y o8 de 07-03 07-11 | CORRECTA | TRAZAS:819-822 |
> | 45 | F7 #10 y su pregunta literal | CORRECTA | VJ:704 y :939 |
> | 46 | «lo visto, al estilo de ADR-0092 §12» | CORRECTA | ADR-0092:270-313 |
> | 47 | 47 láminas en C:\Users\USER\Desktop\laminas-sesion-7-v5 | CORRECTA | LAMINAS.md:1118-1123; HISTORIA:16941-16943 |
> | 48 | TRAZAS y LAMINAS repiten la línea base a 0 bytes | CORRECTA | HOJA:831; LAMINAS.md:729 |
> | 49 | ADR-0092 §6: el pivote nunca ajusta un parámetro | CORRECTA | ADR-0092:160-170 |
> | 50 | D6: R4.3 ponía los dos esquemas en la 7a; VIDEO-JULIO, punto 1, pone la tarde del 10 en el bloque técnico | CORRECTA | HOJA:386; VJ:935 |
> | 51 | dos textos de ayuda de cli.py hacia :2710-2711 y :3363 | MATIZ | :2710-2711 es el docstring de `motor_laminas`, no un texto de ayuda; :3363 sí lo es (`help=`). Ningún test mira esas cadenas (grep en tests/: 0) |
> | 52 | ACTIVAR-SESION-06 §«Para la sesión 7», puntos 1-11; el punto 1, «la primera de la hoja»; el 10 y S-7; el punto 11 de la respuesta de LAMINAS | CORRECTA | ACTIVAR-SESION-06.md:557-617, :562, :609-613; LAMINAS.md:270 |
> | 53 | RUMBO §1 a) pide primero lo que más filas mueve y lo del dinero (A-35, A-13) | CORRECTA | RUMBO:17 |
> | 54 | conviven `perdida_trader_reinicio` (enum, primera_sesion_dia_siguiente) y `perdida_trader_reinicio_huso` (UNKNOWN, sin efecto) | CORRECTA | parametros.yaml:1593-1612 y :1616-1629 |
> | 55 | ACTIVAR-A35-A44.md:71 y :126-127; las NOTAS de cabecera dicen «el cuerpo no se toca» | CORRECTA | :71, :126-127; :3 y :25 |
> | 56 | la herencia está en ACTIVAR-SESION-06-MOTOR.md hacia :37 y :798 | CORRECTA | :37 (H9) y :798 |
> | 57 | la NOTA de ADR-0092 §6 deja la conversión en regla al ADR del método | CORRECTA | ADR-0092:172-178 |
> | 58 | graficos_sesion.py:66-71 y su test hacia :310-318 | CORRECTA | :66-71 (abril 1-30, agosto 1-31); test :310-318 |
> | 59 | fb-…-6e7da456 y fb-…-d2e84172 son lo respondido por WhatsApp | CORRECTA | Los dos son `medio: escrito`, del 2026-10-14. d2e84172 es el CONFIRM de `sesgo_h4_criterio_ruptura` = mecha; 6e7da456, el CORRECT de RN-003 |
> | 60 | ev-v9-000902-25db5bf5 y ev-v9-001529-ac28bb40, «la cita de la regla del último rango, strategy_spec.yaml hacia :1204-1206» | MATIZ | En :1204 se citan fb-…-1168f036 y ev-v9-001529, cuyo literal es «Siempre va a haber un sesgo». «El del último rango, dure lo que dure» es glosa de la spec. ev-v9-000902 no aparece en strategy_spec.yaml (grep: 0) |
> | 61 | «suponiendo que no haya otro rango mayor», hacia :1127-1128 | CORRECTA | strategy_spec.yaml:1127-1128 |
> | 62 | S-23 de la sesión 6 son ev-v17-015726-ce2e42e4 y ev-v17-015741-8f9fd638 | CORRECTA | Las dos notas dicen «S-23 (A-46, RESUELTA…)» |
> | 63 | si «mecha o cuerpo» (F7 #2) ya está contestado, no se pregunta | MATIZ | Está contestado dos veces: ev-v9-000902 («con mecha o con cuerpo por debajo de esta vela que es nuestro rango», valor mecha) y d2e84172. Pero d2e84172 habla del extremo de la H4 anterior (RN-003), no de la vela de rango. La que cubre el rango es ev-v9-000902 |
> | 64 | S-22 quita el 52 % de los puntos de breaker | MATIZ | El 52 % es con la lectura (a), «la última verde». Con (b), «toda la racha», es el 69 % (ACTIVAR-SESION-06-MOTOR.md:148-154) |
> | 65 | S-19: verifica hacia :803 y en RECORRIDA-CONSTRUCCION-2.md hacia :699 | MATIZ | :803 da las dos lecturas. RC2:699 solo dice «S-22 y S-19 con sus esquemas y el 52 %» |
> | 66 | 7a: TRAZAS 5.5, puntos 1 y 2; A-20 ya fija el número | CORRECTA | TRAZAS:945-957; A-20 no está en Known Ambiguities (PS:64-74) |
> | 67 | 7b: ADR-0083 D1 con F7 #7 y las 4 filas de RN-019; A-53; A-43; A-48 «¿de qué sale tu stop?»; A-46 por la toma | MATIZ | Las fuentes casan: ADR-0083:84-87; RC2:1319 (P7, 4) y :1338-1339; ACTIVAR-SESION-06.md:581-605. Pero A-46 está RESUELTA (ACTIVAR-SESION-06.md:602), así que su pregunta tiene que decir por qué no repregunta lo decidido |
> | 68 | las diez sesiones de trabajo-laminas.md | CORRECTA | :61-64 (6+3+1) |
> | 69 | 0.5: F7 #1, #2, #3, #6 y #10; ninguna es de v13; el tramo de v13 es 0:00:00-0:00:35; #10 es de la v14 vieja | CORRECTA | VJ:695-704; VJ:943 (#1, #2, #3, #10); TRAZAS:1390 (#6); tramos_no_citables.yaml:524-526; tr-v14-…-2253ec10.yaml registrada |
> | 70 | 0.6: ORDEN_SESION_06, CODIGOS_DE_SESION_TEXTO["06"], HOJAS | CORRECTA | transcribir_sesion.py:136-140, :216-242, :245-251 |
> | 71 | F1.2: «Antes», paso 1; la salvaguarda del recuadro del 2026-09-28; «Qué sale»; «Después», paso 4; la lección de video-julio | CORRECTA | SDP:66-74, :41-42, :151-153; VJ:930. «Qué sale» es del runbook docs/runbooks/LAMINAS.md:31-44, no del informe |
> | 72 | F1.7: cabecera :12-14; paso 6 de «Antes»; «Lo primero» de LAMINAS | CORRECTA | SDP:12-14, :92-100; runbook LAMINAS.md:5-10 |
> | 73 | F3: «el trailer Fuente: que pida el repo» | MATIZ | El repo no lo pide para knowledge/evidence/: `DIRECTORIOS_CON_FUENTE = ("knowledge/spec/", "knowledge/cases/")` (historial.py:33). Precedente de costumbre: b3680161 lleva «Fuente: ADR-0021» |
> | 74 | CI: transcribir_sesion.py lleva rutas de Windows; se empuja como fix/ | CORRECTA | transcribir_sesion.py:83; RITUAL.md:92-111 |
> | 75 | problemas_a a problemas_d de test_hoja_de_ruta | CORRECTA | test_hoja_de_ruta.py:121-205 |
> | 76 | en el cierre, R0.3 HECHA con ADR-0093 | MATIZ | El bloque de R0.3 lleva NA:F (HOJA:43). Con F viva, problemas_b falla («esta HECHA y la letra sigue viva», test:144-145, que mira el bloque entero) si NA:F no sale de todo el bloque |
> | 77 | F6: ensayo en clon con settings.local.toml; nunca junto a un make check; unos 9-11 min | CORRECTA | runbook LAMINAS.md:22-29 |
> | 78 | D3 a) a c) sobre las sesiones (contadas con mis propios grep, sin la compuerta) | CORRECTA | Diez candidatas: 10 de 10 pasan a) a c). Las 18 «posible M» caen en 7 sesiones; de las candidatas solo 07-10 07-11. En la lista de la 7b solo salen 01-02 11-15, por b), y 07-10 07-11, por c), como dice D3 d |
>
> ### Lo que el repo pide y el encargo no recoge
> | # | Qué | Dónde lo pide | Evidencia |
> |---|---|---|---|
> | H1 | «Antes», paso 5: «ningún gráfico que no sea de los preparados según la regla 2». Choca con que el trader cargue él su replay, y F1.7 no lo lista | SESION-DE-PREGUNTAS.md:89-91 | F1.7 nombra la regla 2, la cabecera y el paso 6, no el 5 |
> | H2 | ACTIVAR-A35-A44.md repite la regla 2 vieja («cortados antes de la orden, sin fecha»), y su NOTA del 2026-11-05 dice «A-35 y A-44 … siguen ABIERTAS». A-44 está RESUELTA desde F38o | ACTIVAR-A35-A44.md:46-51 y :38-39; HOJA:380-382; PS:64-74 (sin A-44) | La NOTA que pide el encargo solo trata el reinicio |
> | H3 | Un docstring del motor quedará viejo tras el ADR-0093. src/botsito/engine/ está protegido y la búsqueda de 0.2 no lo incluye: necesita una línea de deuda o decir por qué no | src/botsito/engine/decisiones.py:7-8: «lo fijara el ADR del metodo (RUMBO §1); esto no lo adelanta» | — |
> | H4 | El destino de los ejemplos de la caja era el visor; el encargo los lleva a días de la 7b sin decir que el paso del visor se sustituye | RC2:1238, :1323, :1333 («dos al visor en la rama de la preparación») | — |
> | H5 | Según R4.5 y F, la preparación genera las láminas de sus días; D4 lo cambia para la 7b. Va como desviación declarada | HOJA:413; PS:28 | — |
> | H6 | Las filas del 1 de julio «no van a la sesión 7». El porqué del ADR (29 filas) incluye 2 P1 de 07-01 07-11, y las 10 P5, 3 de 07-01 | VJ:598, :885 | El ADR tiene que decirlo con la cifra |
> | H7 | R0.3 HECHA exige quitar NA:F de todo su bloque. Precedente: R4.5 «sin NA:F en su bloque» | test_hoja_de_ruta.py:139-149; ERRORES-RECURRENTES, fila de video-julio (b1); HISTORIA:16961 | — |
> | H8 | El recuadro de ADR-0084 manda a la sesión 7 ev-v15-000553-9d95178a, «en tensión», y la mecha de la propia contraria. Queda dentro de A-35 (ACTIVAR-SESION-06 punto 2), pero el encargo no lo nombra | ADR-0084:76-79, :126-128 | — |
> | H9 | El orden de ACTIVAR-SESION-06 punto 1 se apoya en «118 de 286 llenadas», cifra de la diaria de RESPALDO-M1. La línea base vigente es RC2 (247 llenadas en la corrida 1), y ningún informe posterior da otra cifra de break even | ACTIVAR-SESION-06.md:562-563, :378; RC2:437 | Para «las dos cosas a la vista», mejor volver a medir sobre la línea base |
> | H10 | F dice todavía «Las láminas no se enseñan al trader hasta que el ADR del método cambie la regla 2»; tiene que salir en el texto nuevo de F | PS:28 | El encargo pide el texto nuevo de F, pero solo nombra lo de J |
>
> ### Comandos del encargo
> | # | Comando | Existe y se ejecuta así | Evidencia |
> |---|---|---|---|
> | C1 | `uv run botsito motor laminas --sesiones <…> --salida C:\Users\USER\Desktop\laminas-sesion-7a` | Sí. `--sesiones` (dia:sesion, obligatoria) y `--salida` (fuera del repo, vacía, obligatoria) | cli.py:3295-3296, :3360-3374 |
> | C2 | `evidence new … --transcripcion` | Sí. Pide también --video, --t0, --t1, --modalidad, --tipo, --cita, --afirmacion, --tema, --confianza, --extractor y --revisado-por | cli.py:3204-3234 |
> | C3 | `evidence propose --check` | Sí. `propose` no tiene `--transcripcion` | cli.py:3429-3437 |
> | C4 | `kb find`, `kb at` | Sí | cli.py:3395-3418 |
> | C5 | `kit hoja` (no se usa) | Existe | cli.py:3274 |
> | C6 | `uv run botsito state check`; `uv run python scripts/contrato_rama.py`; `uv run botsito knowledge validate > knowledge-validate.log 2>&1`; `make check > make-check.log 2>&1` | Sí | cli.py:3142, :3143-3146; scripts/contrato_rama.py existe |
> | C7 | `casos_reservados(repo)`, `casos_ocultos(repo)` | Sí | cases/holdout.py:351, :456 |
> | C8 | `git worktree add` (ensayo) | Sí | CLAUDE.md, «Ensayos aislados» |
> | C9 | `/model` | Es de Claude Code, no del repo | — |
>
> ### Lo que no pude comprobar
> - La compuerta sobre las sesiones (casos_reservados y casos_ocultos): mi Bash no ejecuta Python del repo. Lo de la fila 78 es grep sobre anexos commiteados.
> - Cómo se comporta `evidence new --transcripcion` con la v14 vieja, y si `propose --check` la acepta: solo se mide ejecutándolo, y el encargo lo deja a la fase 0.
> - Si la guardia deja usar `kb at` (una memoria de punto-usado lo da por negado).
> - Lo que solo está en el chat: la aprobación de Aleks de los mínimos 19 y 33 (2026-11-11), la «primera versión» del encargo y `/model`.
> - El PICO DE MEMORIA: make-check.log estaba a medias (56-58 %) cuando lo miré.
>
> ### Lo más grave
> Ninguna afirmación es falsa, y las cifras del pivote cuadran contra el anexo. Lo que cambiaría el trabajo son cuatro cosas:
>
> 1. **F1.7 se queda corto.** Deja sin tocar el paso 5 de «Antes» (SESION-DE-PREGUNTAS.md:89-91, «ningún gráfico que no sea de los preparados según la regla 2») y la regla 2 vieja que repite ACTIVAR-A35-A44.md:46-51. Con el ADR-0093, dos runbooks contradirían el procedimiento nuevo, en que el trader abre él mismo su replay. Además, la NOTA nueva de ACTIVAR-A35-A44 heredaría «A-44 ABIERTA», que ya no es verdad.
> 2. **La propuesta de cierre «R0.3 HECHA» rompe `test_hoja_de_ruta`.** problemas_b falla mientras NA:F siga en el bloque de R0.3.
> 3. **El porqué del ADR mezcla datos.** Las 29 filas incluyen filas del 1 de julio que VIDEO-JULIO excluye de la sesión 7. Y el «52 %» de S-22 es solo la lectura (a): con (b) es el 69 %. El ADR tiene que escribirlo con su condición.
> 4. **D4 se aparta de R4.5 y de F.** El motivo está dado; el informe tiene que declararlo como desviación.

## Apéndice B · El informe del revisor (opus, 2026-11-11, sobre 958a7b9a), tal cual salvo su lista de 33 comandos, resumida al final

> ## Informe del revisor · trabajo/preparacion-sesion-7 · 2026-11-11
>
> Base `e6b073f1` (`git merge-base main HEAD`), HEAD `958a7b9a`, árbol limpio. 4 commits y 34 ficheros. Encargo: `docs/encargos/trabajo-preparacion-sesion-7.md`. Contrato: `contrato.yaml`. Informe: `docs/validation/PREPARACION-SESION-7.md`. Lo he juzgado tal como está: todavía no tiene las secciones finales.
>
> **Las comprobaciones del contrato:**
> - `uv run python scripts/contrato_rama.py`, exit 0: `CONTRATO: 34 ficheros dentro del contrato de trabajo/preparacion-sesion-7 (riesgo alto, artefacto docs/validation/PREPARACION-SESION-7.md, tramo 'R4 · La sesión 5 con el trader y su activación', 4 comprobaciones para el revisor)`.
> - `uv run botsito state check`, exit 0: `OK: rama 'trabajo/preparacion-sesion-7' - funcionalidad actual: EN CURSO: …`.
> - `uv run botsito knowledge validate`. Lo lancé sin `> knowledge-validate.log`, porque esa redirección escribe en la raíz. Salió con exit 0, todo OK, entre otras: `OK: 1041 documentos: todo id citado existe o esta declarado con motivo` y `OK: 645 items de evidencia, 0 contradicciones abiertas, historial intacto`. Dio 4 avisos, los de siempre: 5 citas con tiempos de segmento, 288 ítems llm sin propuesta y los configs congelados de dos paquetes.
> - `make check` no lo ejecuté. La evidencia está en `make-check.log`:
>   - `:85`: `3430 passed in 1189.59s`.
>   - `:109`: `SELLO: make check en verde sobre el arbol cb29ec17fac927064f89f36ad877c987606e3032`. Coincide con `git rev-parse 958a7b9a^{tree}` = `cb29ec17…`.
>   - `:111`: `PICO DE MEMORIA … 312 MiB`.
> - Además, `uv run pytest -p no:cacheprovider -q tests/unit/test_pivotes_sesion_7.py tests/unit/test_transcribir_sesion.py`: 140 tests, exit 0.
>
> ### Eje (a) · Reglas de la casa
> Resumen: 0 bloquea, 1 importa, 1 menor.
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | a1 | importa | **Dos afirmaciones de evidencia nueva dicen algo que su cita no trae (punto 10 del eje a).** (1) `ev-v11-000038-a322e483`: la cita dice «A ver, este es nuestro rango … Entonces nosotros nos enfocamos en buscar Traits alcistas», y la afirmación dice «el trader busca compras porque su rango **de H4** no ha sido mitigado…». La cita no nombra la H4: la filtrada dice «H4, vale» en 0:00:31.9, fuera de la ventana 0:00:38-0:00:53. (2) `ev-v11-000550-b140027d`: la cita dice «hubiera roto con mecha o con cuerpo por debajo de **esta vela**», y la afirmación dice «por debajo de **la vela del rango**». El contexto lo apoya («Como todavía no se ha roto nuestro rango», 0:05:44), pero queda fuera de la cita. El ítem es inmutable: se corrige superseding si el consultor lo pide. | `knowledge/evidence/v11/ev-v11-000038-a322e483.yaml:7-11`; `knowledge/evidence/v11/ev-v11-000550-b140027d.yaml:7-10`; `uv run botsito corpus transcript show --video v11 --t0 0:00:30 --t1 0:01:00` y `--t0 0:05:45 --t1 0:06:05` |
> | a2 | menor | La fila de HOLDOUT-EXPOSICIONES del día solo declara la lectura de la filtrada «(2) La fase 0». F3 (`corpus transcript show` y `evidence new` sobre v11, v12 y v14) no aparece por su nombre. Es la misma herramienta y el mismo día. | `git diff main...HEAD -- docs/validation/HOLDOUT-EXPOSICIONES.md`, la primera fila nueva |
>
> Comprobado sin hallazgos:
> - **Contrato:** las tres comprobaciones que no escriben, en verde, y el sello de `make check` es el del árbol de HEAD.
> - **Trailer `Fuente:`:** ningún commit toca `knowledge/spec/` ni `knowledge/cases/`. `958a7b9a` lleva igualmente `Fuente:` en el cuerpo, con 5 `ev-*` y ADR-0093, y todos existen.
> - **Holdout:** no se toca `knowledge/cases/` y no se abrió ningún fotograma. Los anexos dan solo recuentos de la compuerta (`dias_d3.py:76-78`, `sustitutas.py:64`) y ningún id de los ocultos.
> - **Regímenes de cambio:** `knowledge/evidence/` tiene solo `A` (5 ficheros). No se tocan feedback, manifests, transcripciones, fotogramas ni `libros.yaml`. HISTORIA solo crece (0 líneas quitadas). HOLDOUT-EXPOSICIONES solo crece (+2 filas).
> - **Ambigüedades:** sin cambios.
> - **ADR-0093:** `## Estado` = `ACTIVE`.
> - **Informes cerrados:** no se toca ninguno.
> - **Tres guardias de una `cita`:** no aplica, no se añade ningún sitio con `cita`.
> - **Cifras:** no cambia código ejecutable, solo dos cadenas de `cli.py`.
> - **Ensayo de F6:** en worktree, según el informe (F6, punto 1).
> - **Cuatro citas del informe, contrastadas con su fuente y ciertas:** `VIDEO-JULIO.md:657` (el rango de H4 30), `TRAZAS-ABLACION.md:878-881` (3+1+4 filas con RN-009), `comun/historial.py:33` (`DIRECTORIOS_CON_FUENTE`) y `cli.py:658-663` (la transcripción que no es la activa).
> - **Notas de la evidencia (punto 15):** solo hablan de su propia cita. #6 no nombra `ev-v16-000234-9a4fa375` y #2 no nombra `ev-v9-000902-25db5bf5`.
>
> ### Eje (b) · Encargo
> Resumen: 1 bloquea, 6 importa, 4 menor. Requisitos: 31 hechos (uno de ellos hecho de otra forma), 6 parciales y 1 no hecho, sobre 38.
>
> | # | Requisito | Estado | Evidencia |
> |---|---|---|---|
> | 1 | Abrir con abrir-rama: el encargo con un bloque ids-inexistentes | Hecho | `git show 3de24780:docs/encargos/…` tiene 1 bloque |
> | 2 | La base, comprobada | Hecho | Informe:7-14 |
> | 3 | Fase 0, de 0.1 a 0.9, con auditor y PARADA | Hecho | Informe:16-379 |
> | 4 | La respuesta copiada tal cual en el encargo y en el informe | Hecho | `diff <(sed -n '120,152p' encargo) <(sed -n '411,443p' informe)`: IDENTICAS |
> | 5 | ADR-0093 §1-§7 = F1.1-7 + RUMBO §1 a-e + puntos 9 y 11 | Hecho (ver b10) | ADR:19-170; precisión (i) en :86-90, (ii) en :99-100, (iii) en :55-57; punto 9 en :92-97; punto 11 en :165-167 |
> | 6 | Recuadros de SESION-DE-PREGUNTAS (cabecera, regla 2, pasos 5 y 6) que copian el texto anterior | Hecho | Los cuatro, comparados con `git diff main...HEAD`: copian el texto de `main` palabra por palabra. El paso 5 copia solo la frase que cambia |
> | 7 | «Lo primero» de LAMINAS.md, con su recuadro | Hecho (ver b8) | `docs/runbooks/LAMINAS.md:5-18` |
> | 8 | La NOTA de ACTIVAR-A35-A44 con el texto de la decisión 6 | Hecho de otra forma | Dos ajustes declarados (informe:454) y uno sin declarar (ver b9). Las líneas `:84`, `:139-140` y `:59-64` son las correctas |
> | 9 | Las dos cadenas de `cli.py` | Hecho | `git diff main...HEAD -- src/botsito/cli.py` |
> | 10 | La fila de ADR-0093 en el índice | Hecho | `docs/adr/README.md`, nueva fila 0093 |
> | 11 | El bloque ids-inexistentes sale en el commit del ADR (alcance 8) | Hecho | 1 bloque en 3de24780 (encargo e informe), 0 en 3e1995df y HEAD; ningún bloque en los demás documentos de la rama |
> | 12 | Las referencias del ADR, verificadas | Hecho | `knowledge validate`: «todo id citado existe» |
> | 13 | El yaml de F2 con D5 literal | Hecho | `docs/plan/PIVOTES-SESION-7.yaml`: cada texto, comparado con D5, es igual. Los matices medidos van aparte en `matices_medidos`, declarado |
> | 14 | El test fija el sha256 y rompe con un mínimo cambiado | Hecho | sha256 `cef25e63…` = `tests/unit/test_pivotes_sesion_7.py:19`; los dos tests que rompen, en :73-95, en verde |
> | 15 | F2 en commit propio, antes de F3 a F6 | Parcial | Ver b6 |
> | 16 | F3: cinco ítems de la filtrada, con `evidence new` | Hecho | Las cinco citas están en `corpus transcript show` (v11 0:00:38 y 0:05:50, v12 0:00:15 y 0:06:50, v14 0:42:02), y `[...]` solo elide |
> | 17 | Las notas solo de su cita, y la contradicción de #6 en el informe y en S-5 | Hecho | Ítems :18; `PREGUNTAS-7A.md:249-252`; informe:556-561 |
> | 18 | El trailer `Fuente:` | Hecho | `git log --format=%B 958a7b9a` |
> | 19 | Los dos documentos, en la forma de la sesión 6 | Hecho | `docs/sesion-7/PREGUNTAS-7A.md` y `PREGUNTAS-7B.md` |
> | 20 | El reparto aprobado (punto 1) | Hecho | 7A S-1 a S-6 y 7B S-1 a S-6, más S-7, en el orden de la respuesta |
> | 21 | Como mucho seis técnicas por día | Hecho | 6 y 6 (+1 de material) |
> | 22 | Sin días ni fechas en lo que va al PDF | Hecho | Fuera de «Para Aleks» y del §1 solo hay horas en el esquema de A-43, que el encargo pide |
> | 23 | Ninguna pregunta repregunta lo decidido | No hecho | Ver b1 |
> | 24 | «Para Aleks» con el valor en que cae cada opción | Parcial | Ver b5 |
> | 25 | El bloque de días con reservas, los pasos, y sin la clave | Hecho | 7A:44-72; 7B:38-63 |
> | 26 | El recuadro de D4 en la 7B | Hecho | 7B:8-14 |
> | 27 | B-7 a B-10 al final, con sus filas | Hecho | 7B:234-244 |
> | 28 | Cada cita de «Lo que nos has dicho», literal | Hecho | 35 citas contrastadas: 13 de 7B y 22 de 7A, con sus 4 `fb-*`. Todas casan con su `cita_literal` o su `respuesta_literal`, y ninguna cae en un tramo no citable de `tramos_no_citables.yaml` |
> | 29 | F5: hojas 07 y 08, `SESION_EN_CURSO`="07", la 06 sin cambios | Hecho | `scripts/transcribir_sesion.py`: los 13 títulos coinciden letra por letra con los documentos |
> | 30 | Los tests de F5 y uno que rompe a propósito | Hecho | `test_un_codigo_de_la_hoja_que_no_esta_en_el_documento_rompe`, en verde |
> | 31 | F6: la fila antes, el ensayo en un worktree y una invocación buena | Hecho (según el informe) | HOLDOUT, segunda fila nueva; informe:487-504 |
> | 32 | F6: tipo a y tipo b por sesión, sin la clave | Parcial | Ver b2 |
> | 33 | Los días según D3 a-f y los puntos 2 a 4 | Hecho | `dias-d3.txt`: 7A, 6 de 6 PASA. `sustitutas.txt`: 01-07 07-11, 01-19 11-15, 01-21 07-11 y 07-16 07-11 «cumple». No van 07-14 11-15 ni 07-17 07-11. La compuerta da «dias dev en ocultos: 0; en reservados: 0» |
> | 34 | Ninguna fecha reservada ni ningún resultado en lo commiteado | Parcial | Ver b7 |
> | 35 | Las filas de HOLDOUT-EXPOSICIONES | Hecho | 2 filas del 2026-11-11 |
> | 36 | Lo que no cambia | Hecho | `git diff --name-status main...HEAD` sobre las rutas protegidas: vacío, salvo `knowledge/evidence/` (5 `A`) |
> | 37 | La CI de `fix/`, con el número de run | Parcial | `origin/fix/preparacion-sesion-7` = `958a7b9a`; el run no consta en el informe |
> | 38 | Las secciones finales del informe y la PARADA final | Parcial (pendiente) | Informe:615-618 (Estado: «por hacer») |
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | b1 | **bloquea** | **S-1 de la 7B pregunta por el 1 de la caja, que ya está decidido, con las opciones que son del 0, que es lo abierto.** ADR-0093 §1 dice «Ninguna vuelve a preguntar lo que ya está decidido», y el encargo pide «el 0 de A-48». La pregunta es «¿hasta dónde llega el 1 de tu caja? (a) el 1 en el último pivote de M1; (b) el 1 en el pivote de la vela de la toma». Pero el 1 ya lo contestó y está CONFIRMED: `caja_bloque` = `r6`, según `ev-v17-010541-05a69879` («al punto más alto de todas las velas desde el punto»), que la propia S-1 cita. Lo abierto es el 0, entre `ultimo_pivote_m1` y `referencia_de_la_toma` (`orden_stop_punto`), y la fuente pedía exactamente eso: «¿dónde pones el 0? (a) aquí; (b) aquí». En la hoja, el 0 solo aparece en «Para precisar», y «Para Aleks» no nombra `orden_stop_punto`. | `docs/sesion-7/PREGUNTAS-7B.md:75-94`; `knowledge/spec/ambiguedades.yaml:1557-1565` («El 1: … caja_bloque = r6 pasa a CONFIRMED … El 0 no queda claro: no eligio entre ultimo_pivote_m1 y referencia_de_la_toma … SIGUE ABIERTA por el 0»); `docs/validation/ACTIVAR-SESION-06.md:591-592`; `knowledge/spec/parametros.yaml:702-706` |
> | b2 | importa | **La clave de las láminas se deduce de lo commiteado (alcance 7).** La tabla de F6 da tipo a y tipo b por carpeta. La tabla de §0.4 (y `filas-por-sesion.txt`) da las filas del trader y del bot de cada sesión. Con la definición de LAMINAS.md «Qué sale» (a = cada orden del bot llenada, b = cada operación del trader sin pareja), las seis parejas (a, b) son distintas y casan una a una con las seis sesiones de la 7A. No escribo aquí cuál es cuál, porque este informe se pega en el repo. Hay precedente parecido en `LAMINAS.md:499-507`. | `docs/validation/PREPARACION-SESION-7.md:509-517` (commit 3e1995df) y `:162-180`; `docs/runbooks/LAMINAS.md:43-46` |
> | b3 | importa | **Una pregunta que sugiere la respuesta (alcance 2).** S-4 de la 7A, Pregunta 1, enuncia una proposición y pide confirmarla: «Una mecha … no mueve el alto; lo toma la vela de M1 que cierra con cuerpo por encima. ¿Es así? (a) sí; (b) no». La proposición es lo que hace hoy el bot, como dice su propio «Para Aleks»: «(a) → … (lo de hoy)». | `docs/sesion-7/PREGUNTAS-7A.md:205-209`, `:222-223` |
> | b4 | importa | **«Para precisar» vuelve a preguntar lo que ya dijo** (ADR-0093 §1: «una pregunta "en parte" … pregunta solo lo que falta»). (1) S-2 de la 7A pregunta «¿por encima de qué tiene que cerrar: del nivel o de la zona de entrada?», y la cita que la misma hoja trae, `ev-v17-005454-90ce4feb`, ya dice «no necesariamente por encima de aquí. Pero sí por encima de la zona de entrada». (2) S-5 de la 7B pregunta «¿Y si antes del punto nuevo el precio toma todavía otra liquidez?», y `ev-v17-005914-55580dc0` ya dice «si antes de que aparezca el nuevo punto el precio toma todavía otra liquidez pues se va actualizando»; «Para Aleks» lo cita cortado con «…» justo antes de esa parte. (3) S-1 de la 7A pregunta «¿Cuánto tiempo puede seguir siendo la misma vela tu rango?», y el informe la da por descartada: «"¿Cuántos días puede durar un rango?" … no se pregunta así». | 7A:136, :147; 7B:189, :194; `knowledge/evidence/v17/ev-v17-005914-55580dc0.yaml:7-8`; 7A:108; informe:126-128 |
> | b5 | importa | **«Para Aleks» no dice en qué valor cae cada opción** (F4 lo pide). Falta en S-1 de la 7B (ninguna opción tiene valor), en S-4 de la 7B (ninguna) y en S-6 de la 7B, Pregunta 2 (sin valor). En S-3 de la 7B, solo «espero» lleva su valor. | 7B:89-94, :168-172, :219-221, :142-146 |
> | b6 | importa | **F6 se hizo antes que F2, y no está declarado.** El encargo pide «F2 · EL PIVOTE (commit propio, antes de F3 a F6)». Las láminas se generaron con F1 sin commitear: «El árbol de trabajo llevaba entonces sin commitear lo de F1», y el Estado decía «F1 y F6 hechos; F2 a F5 … por hacer». F2 es `a2d830e5`, posterior. «Desviaciones» solo trae dos, y esta no está. | Informe:499-502, :617-618, :390-398; `git log` (3e1995df → a2d830e5) |
> | b7 | importa | **Fechas de meses reservados en anexos commiteados** (el encargo dice «En lo que se commitea, ninguna fecha reservada»). `dias-d3.txt` y `sustitutas.txt` escriben, como «anterior», el día de mercado anterior al 1 de abril y el anterior al 1 de julio, que son fechas de marzo y de junio. Se calculan por calendario y la salida no dice si están en una partición. No comprobé su pertenencia para no consultar la compuerta sobre un día reservado. Basta con imprimir «fuera de construcción» sin la fecha. | `docs/validation/anexos/PREPARACION-SESION-7/dias-d3.txt:42-43`; `sustitutas.txt:22`, `:45-46` |
> | b8 | menor | El recuadro de LAMINAS.md copia el párrafo anterior pero no el título que también cambió («## Lo primero: todavía no se enseñan al trader»). | `git diff main...HEAD -- docs/runbooks/LAMINAS.md` |
> | b9 | menor | La NOTA de ACTIVAR-A35-A44 cambia «(`ambiguedades.yaml:1442`)» de la decisión 6 por «(`knowledge/spec/ambiguedades.yaml`)». Es un tercer ajuste que el informe no declara: dice «Dos ajustes de forma». | Informe:361 frente a `docs/runbooks/ACTIVAR-A35-A44.md:46`; informe:454 |
> | b10 | menor | ADR-0093 §3 añade «Una exclusión dice a qué conjunto se aplica (respuesta a la PARADA, punto 17)». No está en F1 ni en RUMBO §1, y el punto 17 es una lección para ERRORES-RECURRENTES, no una decisión (alcance 1: «sin añadir»). | `docs/adr/0093-…md:81` |
> | b11 | menor | §0.5 del informe sigue diciendo que la contradicción de F7 #6 «queda escrita en las notas del ítem». F3 y el punto 15 dicen lo contrario, y el ítem no la lleva. | Informe:224-228 frente a :556-561; `ev-v12-000015-7fc04520.yaml:18` |
>
> ### Lo que no pude comprobar
> - **Las láminas y `clave.txt`:** no los abrí (`C:\Users\USER\Desktop\laminas-sesion-7a`, prohibido por el encargo). Lo de F6 (exit 0, 45 ficheros, 0 distintos por sha256, 38 láminas) sale solo del informe.
> - **La CI de `fix/preparacion-sesion-7`:** el push está (`origin/fix/…` = `958a7b9a`), pero no consulté el run. `gh run list` lo niega el clasificador y el informe no da el número.
> - **`make check`:** no lo ejecuté, porque escribe. La evidencia es `make-check.log`: sello `cb29ec17…` = árbol de HEAD, 3430 passed, pico 312 MiB. Tampoco ejecuté `git write-tree`.
> - **El orden de los pasos:** no puedo saber si F6 coincidió con algún `make check`, ni si `knowledge validate` se pasó antes del `make check` de F3.
> - **El vídeo de mapeo:** no puedo saber si Aleks avisó de que había llegado antes de aprobar los días (condición de PARADA del encargo). No hay rastro en el repo.
> - **Las dos fechas de b7:** no comprobé si están en una partición, por no preguntar a la compuerta por un día reservado.
> - **El tema de `ev-v12-000015-7fc04520`** (`entrada.breaker_m1_con_cuerpo`) da por hecho que el «con cuerpo» es del breaker de M1. La cita no dice M1, y el contexto (0:00:58) habla de la liquidez de M15. No es la afirmación y no cuenta como hallazgo del punto 10, pero toca la contradicción que se le pregunta al trader en S-5 de la 7A.
>
> ### Comandos ejecutados
> (33 entradas; la lista entera la dio el revisor con su informe, y aquí se resume: git de lectura sobre la rama y `main`; las tres comprobaciones del contrato que no escriben; `corpus transcript show` de v11, v12 y v14; `pytest` de los dos ficheros de tests; `sha256sum` y `wc -c` del yaml; Read y Grep de los documentos, los ítems y los parámetros. Dos órdenes que la guardia le negó, un `for f in …; do cat` y un `uv run python -` con `glob`, las rehízo con Read y Grep sin rodearla.)

## Respuesta del consultor a la PARADA final (2026-11-11)

Copiada tal cual:

> Modelo: Opus 5.5 · Esfuerzo: medio
>
> Respuesta del consultor a la PARADA final de trabajo/preparacion-sesion-7 y orden de cierre (2026-11-11). Cópiala tal cual al final del informe, en «Respuesta del consultor a la PARADA final», con su fecha.
>
> PRIMERO, un commit más en la rama («docs(sesion-7): dos arreglos del consultor a las preguntas y la exposición de las tres fechas»), con su make check sellado:
> 1. PREGUNTAS-7A.md, S-5, «Para precisar»: sale «¿Qué orden usas: una orden stop, una limitada o a mercado?», porque A-47 está RESUELTA (ambiguedades.yaml, «el tipo de orden de entrada, stop o límite»; verifícalo) y no se repregunta. Entra en su lugar: «Ese cierre con cuerpo que dices en el vídeo, ¿lo miras en la vela de un minuto o en la de 15 minutos?». En su «Para Aleks», una frase: el tema de ev-v12-000015-7fc04520 dice «breaker de M1» y su cita no dice M1; si el trader responde M15, no hay contradicción con S-18, y la activación de la 7a lo escribe así. El ítem no se toca: es inmutable, y supersede exige el mismo tema.
> 2. PREGUNTAS-7B.md, S-3: una opción más, antes de «otra, ¿cuál?», con lo que dijo en sus propias citas: «muevo el 0 a los nuevos altos y pongo la orden ahí». En su «Para Aleks», a qué lleva esa opción (el 0 se actualiza: la lectura que sostienen ev-v17-014235-f3375358 y ev-v17-014350-ec133d13, con su rama y su ADR). Los títulos de S-5 y S-3 no cambian; si alguno cambia, cámbialo también en CODIGOS_DE_SESION_TEXTO.
> 3. Tu duda 1, resuelta así: basta con declararlo, y nada se regenera. Con ADR-0093 §2 el trader carga él mismo el día en FX Replay, así que la clave ya no protege ninguna fecha que él no vea. La historia de git no se reescribe. Las tres fechas de «día anterior» se cuentan ahora con casos_reservados(repo) y casos_ocultos(repo), solo el número, sin imprimir ninguna. El recuento va a una fila nueva de HOLDOUT-EXPOSICIONES de esta rama, que dice qué commit las lleva (3e1995df) y que la tabla de F6 por carpeta deja deducir la clave.
> 4. Tu duda 2: declarada en el informe, como en el punto 1. Tu duda 3: de acuerdo; el recuadro de PREGUNTAS-7B.md basta.
> Después, push a fix/preparacion-sesion-7, y la CI de Linux sobre ese commit. Mira también la de e8a8c43b. Dame los dos números de run: el único fallo aceptado es test_state_check_ok_on_real_repo.
>
> DESPUÉS, EL CIERRE (cuando yo escriba /cerrar-rama trabajo/preparacion-sesion-7; antes no):
> - Tag: stable/F38x-preparacion-sesion-7.
> - En el commit chore(cierre), en la rama:
>   · sale contrato.yaml;
>   · entra el registro en HISTORIA, con stable/F38x-preparacion-sesion-7^{commit}, el número de commits de la rama y su fila de HOLDOUT-EXPOSICIONES;
>   · entra la fila de ERRORES-RECURRENTES (abajo);
>   · en PROJECT_STATE, la F nueva, tal como la propusiste (sin la J y sin «las láminas no se enseñan»), y lo que sale de F, literal, en HISTORIA bajo un encabezado `# Next Action HECHA · F · trabajo/preparacion-sesion-7 · 2026-11-11`, como se hizo con F en el cierre de trabajo/laminas (verifícalo);
>   · la línea nueva de Technical Debt (273 bytes) y la de ingerir-sesion ampliada;
>   · en HOJA-DE-RUTA, R4.3 con el reparto definitivo y sin J en «Depende de», y R0.3 HECHA con ADR-0093, sin NA:F en su bloque.
>   Todo con el texto de anexos/PREPARACION-SESION-7/simular_cierre.py, comprobado otra vez con problemas_a a problemas_d sobre el árbol real antes del make check. PROJECT_STATE, medido con wc -c (tu cifra: 24.001).
> - El resto, como manda RITUAL.md con la skill cerrar-rama: merge, tag, commit de estado (solo Current Branch, Current Feature, Stable Main State y Last Stable Commit), make check sellado, push atómico de main y el tag (lo confirmo con «1. Yes»), CI de main en verde, y después borrar la rama local y fix/preparacion-sesion-7.
> - Fila de ERRORES-RECURRENTES. El revisor: 1 bloquea y 7 importa, todo arreglado o declarado. Errores del consultor que llegaron a la rama: 6, 1 importa y 5 menores (consultor en Opus 5.5):
>   · importa: la decisión 0 de TRAZAS-ABLACION (consultor, F38v) clasificó o4, o6 y o8 de 2026-07-03 07-11 como «contradicción con lo fijado» dando por hecho que el cuerpo de v12 era de M1, y la cita no dice M1; de ahí salió el tema de ev-v12-000015-7fc04520. Lección: una clase que enfrenta una cita con lo fijado comprueba antes que las dos hablan del mismo marco.
>   · los cinco menores de mi respuesta a la PARADA de la fase 0, punto 17, tal cual.
>   Hallazgos del consultor que el revisor no vio: menor · S-5 de la 7a volvía a preguntar, en «Para precisar», el tipo de orden (A-47 RESUELTA). Lección para el revisor: «ninguna repregunta lo decidido» vale también para «Para precisar», y se contrasta con las RESUELTA de ambiguedades.yaml. Menor · S-3 de la 7b no ofrecía como opción lo que el trader ya había dicho (actualizar el 0). Lección: las opciones de una pregunta «en parte» incluyen la lectura que sostienen sus propias citas. Y tu lección de b1 («antes de redactar una pregunta "en parte", leer en ambiguedades.yaml qué parte quedó decidida»), tal como la propones.
> - Informe final: sha de main, tag, run de la CI de main, ramas que quedan, tamaño de PROJECT_STATE y número de commits de la rama.

### Cómo se aplicó la primera parte (el cierre espera a `/cerrar-rama`)

1. **S-5 de la 7a.** A-47 está RESUELTA (`knowledge/spec/ambiguedades.yaml:1512-1519`, «el tipo de
   orden de entrada, stop o límite»: «se entra siempre por stop», `entrada_tipo_orden` =
   `stop_en_ruptura`, `fb-2026-09-29-sesion-03-92a38105`). Sale la repregunta del tipo de orden y
   entra la del marco del cierre con cuerpo. El «Para Aleks» lleva la frase del tema de
   `ev-v12-000015-7fc04520`, y que el ítem no se toca. El título de S-5 no cambia.
2. **S-3 de la 7b.** Entra la opción (d), «muevo el 0 a los nuevos altos y pongo la orden ahí», y
   «otra, ¿cuál?» pasa a ser (e). En su «Para Aleks», la opción (d) lleva a lo siguiente:
   - es la lectura de las citas y la del consultor en `ACTIVAR-SESION-06.md:546-548`: el rechazo con el 0 vivo no gasta el punto, y la orden se recoloca con el 0 actualizado (RN-006);
   - va en la rama de S-19, con 3.a y 4.a de `ACTIVAR-SESION-06-MOTOR.md:293-301` y un ADR que enmiende ADR-0083 D1;
   - rompería `tests/unit/test_punto_usado.py:343`.

   El título de S-3 no cambia, así que `CODIGOS_DE_SESION_TEXTO` tampoco.
3. **Las tres fechas, contadas por la compuerta** (`anexos/PREPARACION-SESION-7/tres_fechas.py` y
   `tres-fechas.txt`). El guion comprueba antes que son las tres que lleva `3e1995df` (3 de 3) y que
   las salidas de ahora no llevan ninguna (0). Resultado:
   - **una de las tres está en `casos_reservados` y en `casos_ocultos`**;
   - las otras dos no están en ninguno, ni son días dev de construcción.

   Va en una fila nueva de HOLDOUT-EXPOSICIONES, que dice qué commit las lleva y que la tabla de F6
   por carpeta deja deducir la clave. **Para el consultor:** tu decisión de declararlo y no reescribir
   la historia se tomó sin saber que una de las tres es de un día reservado. Lo que guarda la historia
   es esa fecha sola, escrita por calendario: ni una etiqueta, ni una vela, ni una operación. El merge
   la llevaría a `main` dentro de `3e1995df`. Si eso cambia tu decisión, dilo antes de
   `/cerrar-rama`.
4. **Tu duda 2**, declarada: en S-5 de la 7a (punto 1) y en «Lo que no me convence», 2. **Tu duda
   3**: el recuadro de PREGUNTAS-7B.md, sin cambios.

La CI de los dos commits empujados a `fix/preparacion-sesion-7`, en «La CI de Linux».

### Adenda del consultor a la orden de cierre (2026-11-11)

Copiada tal cual:

> Modelo: Opus 5.5 · Esfuerzo: medio
>
> Adenda del consultor a la orden de cierre de trabajo/preparacion-sesion-7 (2026-11-11). Cópiala tal cual al final del informe, debajo de «Respuesta del consultor a la PARADA final».
>
> 1. La decisión del punto 3 no cambia: se mergea con 3e1995df. Esa fecha se saca por calendario de cobertura_material, que es público, y no lleva ninguna etiqueta, vela, operación ni resultado. La historia no se reescribe: rebase, cherry-pick y push --force están prohibidos, y fix/preparacion-sesion-7 ya es público, así que reescribirla tampoco lo quitaría. La fila de HOLDOUT-EXPOSICIONES de 1de78e8b basta (ADR-0021 §4). El registro de HISTORIA del cierre lo dice en una línea, sin la fecha.
> 2. Para la fila de ERRORES-RECURRENTES del cierre, además de lo de la orden:
>    · importa (hallazgo de Claude Code, no del revisor): los guiones de la fase 0 escribieron en anexos commiteados tres fechas de fuera de construcción, calculadas por calendario sin pasar por la compuerta, y una es de un día reservado. Lección: un guion que escribe fechas en un fichero que se commitea solo escribe días que la compuerta da como construcción; las demás se cuentan, no se escriben.
>    · Lección para el revisor: no lo vio. El alcance «ninguna fecha reservada en nada commiteado» se comprueba sobre cada commit de la rama (git log -p de main..rama), no solo sobre el árbol final.
> 3. Los runs 43123877117 (e8a8c43b) y 43137995275 (1de78e8b), con el fallo aceptado, van al registro de HISTORIA.
>
> Con esto la orden de cierre queda completa. Responde que la has recibido y espera a /cerrar-rama.
