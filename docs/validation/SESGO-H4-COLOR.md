# SESGO-H4-COLOR · La regla del sesgo de H4 que el trader respondió por WhatsApp (R1.2)

Rama `trabajo/sesgo-h4-color`, abierta el 2026-10-17 desde `main` en 59c8ae7 (commit de estado
sobre el merge fa15a84, tag `stable/F37q-corrida-construccion`). Encargo:
`docs/encargos/trabajo-sesgo-h4-color.md`. Tramo: R1 (R1.2 de `docs/plan/HOJA-DE-RUTA.md`; W de la
Next Action). Modelo de la sesión: Fable 5.1, esfuerzo alto (`/model`, comprobado al abrir).

## 0 · La base, comprobada al abrir

Las cuatro comprobaciones del paso 1 de la skill `abrir-rama`, con su salida:

- `git fetch origin` y `git status --short` vacío; `git rev-parse HEAD main origin/main` → tres
  veces `59c8ae72fc959d81753d22e6fc140ea75ea42bda`.
- El último tag de los registros de cierre de `docs/state/HISTORIA.md` es
  `stable/F37q-corrida-construccion`; `git rev-parse "stable/F37q-corrida-construccion^{commit}"` y
  `git rev-parse main^1` dan los dos `fa15a84405c5d371d2906833616278ad2e25c926`, y
  `git ls-remote --tags origin stable/F37q-corrida-construccion` lo trae
  (`579bff95968cb0060cd3c02a02c1d838173a0a0c refs/tags/stable/F37q-corrida-construccion`).
- La CI de `main` sobre su HEAD, consultada con `gh run view 38656985715` (como pide el encargo:
  ni curl ni guion): `status completed`, `conclusion success`, `headSha 59c8ae72…42bda`,
  `headBranch main`, `event push`, `workflowName ci`, creada el 2026-10-14T23:55:19Z.
- Ninguna otra rama: `git branch --list` da solo `main`; `git ls-remote --heads origin "fix/*"`
  vacío; `git ls-remote --heads origin` solo `refs/heads/main`.

Hecho al abrir (commit c24c50b, sellado: 2643 passed, `SELLO` sobre dc99c115): el encargo tal
cual, `contrato.yaml` (riesgo alto, tramo R1) y el Archivo 34 de `PROJECT_STATE.md` al final de
`docs/state/HISTORIA.md`.

## 1 · Fase 0 · Inventario sin tocar nada (2026-10-17)

Todo leído en el repo y medido en esta sesión. No se escribió código, spec ni knowledge. Lo único
que corrió con código distinto de `main` fue un clon desechable (`git worktree add --detach … main`
en el scratchpad, borrado después) con un parche de MEDIDA sobre `domain/sesgo.py` para contar qué
tests cambian (§1.b); el parche no entra en la rama. El auditor del encargo corrió en paralelo
(§1.h).

Este informe nombra dos ids sintéticos de una medida en memoria (§2.1), y la guardia de ids
citados de `knowledge validate` los exige declarados (hasta la fase 3 declaraba también ADR-0080,
que ya existe):

```ids-inexistentes
ev-v3-011045-00000001 — id sintético de la medida en memoria de §2.1 (un ítem que supersedería a ev-v3-011045-a185d2ba); nunca se escribió
ev-v6-010430-00000002 — id sintético de la misma medida (un ítem de v6 1:04:30-1:05:35); nunca se escribió
```

### 1.a Todo lo que lee, nombra o contradice la regla, y qué cambia

**El motor.**

| Sitio | Qué dice hoy | Qué cambia |
|---|---|---|
| `src/botsito/domain/sesgo.py:3-4` (docstring) | «cambia solo si esa vela rompio el extremo de la anterior, y basta con la mecha; un equal no lo cambia» | gana «y cierra del color de esa ruptura» |
| `domain/sesgo.py:14-15` | «Con un solo extremo roto el color sigue sin decidir nada» | lo contrario: se reescribe citando el ADR nuevo |
| `domain/sesgo.py:50-62` (`ResultadoSesgo`) | `sesgo`, `ruptura_puntos`, `velas_miradas`, `doble_ruptura` | dos campos nuevos para el arnés (§1.f) |
| `domain/sesgo.py:89-99` (doble ruptura) | decide el color; la neutra sigue hacia atrás (ADR-0060 §1, ADR-0075) | no cambia (D2): ya es un caso de la regla nueva |
| `domain/sesgo.py:100-103` (ruptura simple) | `if arriba > 0: ALCISTA`, `if abajo > 0: BAJISTA`, sin mirar el cierre | ALCISTA solo si `cierre > abierta`; BAJISTA solo si `cierre < abierta`; con color contrario (D1) o sin cuerpo (D3) la vela no decide y la búsqueda sigue, como hoy la neutra de doble ruptura |
| `src/botsito/engine/primitivas.py:59-64` | `ANOTACION_SESGO`, `ANOTACION_DOBLE_RUPTURA = "sesgo_h4_doble_ruptura"` | dos anotaciones nuevas (§1.f) |
| `engine/primitivas.py:169-189` (`sesgo_h4_al_abrir`) | llama a `sesgo_h4` con tope y criterio del registro; anota el sesgo y, si `r.doble_ruptura`, `"si"` (:184-185) | anota también las H4 saltadas por color contrario y por neutra simple (§1.f); la firma y el `Resultado` no cambian |
| `engine/primitivas.py:9` (docstring) | nombra `sesgo_h4_al_abrir` | sin cambio |
| `src/botsito/engine/arnes.py:59, 288-289, 306-308, 392-394` | importa las dos anotaciones; cuenta `dobles` por sesión y lo imprime en «## RN-003 al abrir la sesion» | cuenta las dos anotaciones nuevas y las imprime en la misma sección (§1.f); es «la anotación de 4.f», lo único del arnés que se toca |
| `src/botsito/engine/visor.py:47, 157, 328-329, 385-395, 775` | usa `sesgo_h4` para el sesgo de cada sesión; deduce la H4 que decide por `velas_miradas` (:392-395); imprime «doble ruptura: decide el color» (:775) | **nada obligatorio**: `velas_miradas` sigue apuntando a la vela que fijó el sesgo, las saltadas cuentan igual que las neutras de hoy, y los campos nuevos de `ResultadoSesgo` llevan valor por defecto. El visor queda en `rutas_protegidas` y no se abre (encargo §3, y PARADA 4 de R3.1). Enseñar las saltadas en el visor es una mejora para la rama O |

**Los guiones de `scripts/` y de anexos que llaman a `sesgo_h4`** (todos con la misma firma
`sesgo_h4(velas, apertura, tope, criterio)`, que no cambia; ninguno se toca, encargo §3; si alguno
diera otra cosa con el motor nuevo, el informe lo dirá y su salida cerrada no se reescribe):
`scripts/bloque_de_la_caja.py:47, 270-271, 295`; `scripts/orden_stop_o_limite.py:55, 513-514,
555`; `scripts/sesgo_h4_diagnostico.py:53-58, 84, 99-100`; `scripts/verificacion_a21.py:35,
80-81, 128`; `scripts/verificacion_a21_entradas.py:48, 179-180, 255`;
`scripts/verificacion_a35_a44.py:41, 96-97, 124, 231`;
`docs/validation/anexos/CORRIDA-CONSTRUCCION/sesgo_2x2.py:9, 37, 53, 58, 90-91` (su :9 cita
`fb-…-8eccf5c0` como fuente de `mecha`: texto cerrado, se queda) y `sesgo_p1.py:29, 36-37, 51,
98-99` (los dos importan además `_extremos`, que no cambia);
`docs/validation/anexos/ENTRADA-ENERO/sesgo_enero.py:34, 38-39, 68`. `patrones.py` (fase 4) no
llama a `sesgo_h4`: lee la ruta por argumento (`patrones.py:203`, `sys.argv[1]`).

**La spec (`knowledge/spec/`).**

| Sitio | Qué dice hoy | Qué cambia |
|---|---|---|
| `strategy_spec.yaml:48-61`, predicado `rompe` | «el sujeto supera el extremo de la referencia, con el criterio declarado»; cita `fb-2026-09-09-sesion-01-8eccf5c0`; notas: «DESDE ADR-0049 NINGUNA REGLA LO INVOCA» (:57) | **se queda como está**: ninguna regla lo invoca (medido: `rompe:` solo aparece en su declaración) y sigue siendo la primitiva de la geometría |
| `strategy_spec.yaml:62-77`, predicado `sesgo_h4_al_abrir` | «la ultima H4 cerrada … que supero un extremo de su anterior segun `criterio`, buscada hacia atras»; doble ruptura por el color; neutra no decide; cita `8eccf5c0` | la descripción gana «y cerró del color de esa ruptura; si cerró del color contrario, o sin cuerpo, no decide y la búsqueda sigue»; la cita pasa al CORRECT nuevo (§1.d) |
| `strategy_spec.yaml:985-1050`, RN-003: `entonces` :988-995 | «segun sesgo_h4_regla; cambia solo si esa vela rompio el extremo de la anterior, y basta con la mecha; un equal no lo cambia … romper es superar el extremo, por poco que sea» | gana «y cierra del color de esa ruptura (rompe el bajo y cierra roja: bajista; rompe el máximo y cierra verde: alcista); si rompe un extremo y cierra del color contrario no cambia: sigue el sesgo que había» |
| RN-003 `cita` :997 y `literal` :998-999 | `fb-2026-10-04-sesion-04-ca0afae6`, «si esta es una vela neutra…» | el CORRECT nuevo y el literal del WhatsApp (§1.d) |
| RN-003 `notas` :1000-1035 | :1013-1016 «Con un solo extremo roto, el color de la vela NO decide: una vela que cierra roja pero cuya mecha rompio por encima deja el sesgo alcista»; :1030 «que el color no decide vale solo para la ruptura de un extremo» | párrafo nuevo «DESDE EL 2026-10-17 (ADR-0080)…» delante, con la regla, la fecha del WhatsApp y la contradicción de §1.c; lo anterior se conserva como historia (como hizo ADR-0075 con ADR-0060 §6) |
| RN-003 `forma` :1036-1047 | `sesgo_h4_al_abrir {que, contra, criterio, tope}` → `fijar sesgo` | **sin cambio**: la regla vive en el predicado; D5 (ningún parámetro ni interruptor nuevo) |
| `strategy_spec.yaml:1052-1090`, RN-033 | `cuando`/`entonces`/`forma` sobre `ambiguo` e `insuficiente`; notas: `insuficiente` = «ninguna ruptura dentro de sesgo_h4_tope_velas» (:1064, :1079) | `cuando`, `entonces`, `forma` y `cita` no cambian. Lo que sí cambia de hecho: `insuficiente` sale también cuando TODAS las rupturas del tope cerraron del color contrario o sin cuerpo (medido en §1.b, test 1). Propongo una línea en sus notas que lo diga (decisión 3) |
| `strategy_spec.yaml:518-535` (tokens `ambiguo`, `insuficiente`) y `:649-661` (hecho `sesgo`) | `insuficiente`: «ninguna de las ultimas sesgo_h4_tope_velas H4 rompio un extremo» (:530-531) | la descripción de `insuficiente` gana «con lado» (o «ninguna fijó el sesgo») por el mismo motivo |
| `glossary.yaml:74-85`, término `equal` | «No cambia el sesgo: para cambiarlo hace falta romper el extremo anterior, aunque sea por una milesima»; cita `8eccf5c0`; `visto_en: v6 1:03:01` | la definición gana «y cerrar del color de esa ruptura (ADR-0080)»; la cita, decisión 2 |
| `parametros.yaml:397-412`, `sesgo_h4_regla` | enum CONFIRMED `vela_anterior_cierre_mecha`, fuente `8eccf5c0`, «Desde F12 ninguna forma lo lee» | solo la descripción: «la regla vigente es la de ADR-0080 (ruptura del extremo con mecha o cuerpo Y cierre del color de la ruptura)»; valor, estado y fuente no se tocan (D7) |
| `parametros.yaml:413-427`, `sesgo_h4_criterio_ruptura` | enum CONFIRMED `mecha`, fuente `8eccf5c0` | la fuente pasa al CONFIRM nuevo con `feedback apply` (D4, D7); valor y estado iguales |
| `parametros.yaml:428-440`, `sesgo_h4_tope_velas` | entero CONFIRMED 60, fuente ADR-0044 | nada (encargo §3) |
| `spec_manifest.yaml:11` | `spec_version: "17.0.2"` | sube con `spec manifest --escribir` en el commit de la fase 3 |
| `docs/spec/` (`README.md`, `ambiguedades.md`, `glosario.md`, `parametros.md`, `reglas.md`; hoy `reglas.md:114, 118, 1402, 1460` copian lo de arriba) | generados | se regeneran con `spec docs --escribir` en el mismo commit (`tests/contract/test_spec_docs_generados.py`) |

**Los ADR y su índice.** ADR-0044 §2 (:17-22, «la última H4 que rompió un extremo») y su
alternativa descartada «el sentido del cierre … «el color de la vela NO decide»» (:71-72);
ADR-0060 §1 (:26-27, «Con un solo extremo roto, el color sigue sin decidir nada»); ADR-0075 §3
(:58, «con un solo extremo roto el color no decide»). Cada uno gana un recuadro `> **ENMIENDA
(2026-10-17, rama trabajo/sesgo-h4-color, ADR-0080).**` como el que ADR-0075 puso en ADR-0060
(:9-16), y en `docs/adr/README.md` sus filas (0044 en :50, 0060 en :66, 0075 en :81) dicen la
enmienda, como la de 0060 dice hoy la de ADR-0075; entra la fila de 0080
(`tests/unit/test_adr.py:38-42` exige que cada ADR esté en el índice). **El siguiente ADR libre
es 0080**: `ls docs/adr` termina en `0079-enero-entra-en-construccion.md` y
`git log --all -- 'docs/adr/0080-*'` está vacío. Ningún otro ADR contradice la regla: `grep -rn`
de «color … no decide» en `docs/adr`, `docs/runbooks`, `CLAUDE.md`, `docs/plan` y `knowledge/spec`
solo da los tres de arriba, RN-003 (:1016, :1030), `domain/sesgo.py:14` y
`tests/unit/test_sesgo_h4.py:44`.

**Los tests que nombran la regla** (además de §1.b): `tests/unit/test_huecos_motor.py:4` (docstring:
«H4 NEUTRA con doble ruptura no decide»), :169-180 y :244-247 (la neutra de ADR-0075 y
`ANOTACION_DOBLE_RUPTURA`), :457 (compara las anotaciones de dos corridas). Con el parche de §1.b
pasan los 121 de `test_huecos_motor.py`, `test_cableado.py`, `test_arnes_motor.py`,
`test_visor.py`, `test_cierre_vela_h4.py` y `test_sesiones_rejilla_h4.py` en el clon, con dos
`skipped` porque el clon no tiene `data/` (`test_huecos_motor.py:316`, la corrida sobre
construcción, y `test_visor.py:393`): esos dos solo se miden en la rama (§1.i).

### 1.b Los siete tests que la regla cambia de resultado, verificados

Clon desechable de `main` (59c8ae7) en el scratchpad; `tests/unit/test_sesgo_h4.py` con el
código de `main`: `21 passed`. Con el parche de medida (la regla de D1 y D3 sobre
`domain/sesgo.py:100-103`, sin tocar nada más): **7 failed, 14 passed**, y son exactamente los
siete del encargo:

```
FAILED tests/unit/test_sesgo_h4.py::test_rompe_arriba_es_alcista_y_el_color_no_decide
FAILED tests/unit/test_sesgo_h4.py::test_rompe_abajo_es_bajista
FAILED tests/unit/test_sesgo_h4.py::test_un_equal_no_rompe
FAILED tests/unit/test_sesgo_h4.py::test_una_neutra_mantiene_el_sesgo_anterior_alcista_y_bajista
FAILED tests/unit/test_sesgo_h4.py::test_semana_de_desfase_la_h4_de_mitad_de_sesion_cuenta_en_la_siguiente[2026-03-10]
FAILED tests/unit/test_sesgo_h4.py::test_semana_de_desfase_la_h4_de_mitad_de_sesion_cuenta_en_la_siguiente[2026-10-27]
FAILED tests/unit/test_sesgo_h4.py::test_semana_normal_las_h4_cierran_a_la_hora_de_las_sesiones
```

El motivo es el que dice el encargo: el ayudante `h4()` (:26-30) cierra en `alto` por defecto, o
sea VERDE, y `_m1_del_dia` (:192-207) abre cada bloque en su bajo y cierra en medio, también
verde; así que toda ruptura por abajo de esos tests cierra verde y con la regla nueva no decide.
Cómo se rehace cada uno conservando lo que comprobaba (el color siempre explícito; ninguno se
rebaja):

1. `test_rompe_arriba_es_alcista_y_el_color_no_decide` (:40-44): `h4(2, 111, 103, abierta=109,
   cierre=104)` rompe arriba por 3 y cierra ROJA; hoy ALCISTA, con la regla no decide y, como
   `h4(1)` está dentro de `h4(0)`, INSUFICIENTE. Se parte en dos: (i) rompe arriba y cierra VERDE
   (`abierta=104, cierre=109`): ALCISTA, `ruptura_puntos == 3`, `velas_miradas == 1`, `not
   doble_ruptura` (lo que comprobaba, con el color que ahora hace falta); (ii) rompe arriba y
   cierra roja con una H4 detrás que rompió abajo cerrando roja: sigue BAJISTA, `velas_miradas ==
   2` (caso 3 del gráfico), y una variante sin nada detrás dentro del tope: INSUFICIENTE (es el
   test «color contrario sin nada detrás» de la fase 2).
2. `test_rompe_abajo_es_bajista` (:47-49): `h4(2, 107, 101)` rompe abajo con cierre verde por
   defecto. Se escribe el color: `h4(2, 107, 101, abierta=106, cierre=102)` → BAJISTA (caso 1).
3. `test_un_equal_no_rompe` (:58-61): la última iguala los dos extremos (no rompe: sigue igual) y
   manda `h4(1, 107, 99)`, que rompe abajo pero cierra verde por defecto. Se escribe el color en
   `h4(1)`: `abierta=106, cierre=100` → BAJISTA, `velas_miradas == 2`. Conserva lo que comprobaba:
   el equal no rompe y manda la anterior.
4. `test_una_neutra_mantiene_el_sesgo_anterior_alcista_y_bajista` (:90-100): la rama alcista pasa
   (`h4(1, 112, 101)` rompe arriba y cierra verde); la bajista, `h4(1, 108, 98)`, rompe abajo
   cerrando verde. Se escribe `abierta=107, cierre=99`. Conserva: la neutra de doble ruptura
   salta y manda la anterior, en los dos sentidos (ADR-0075).
5. y 6. `test_semana_de_desfase…[2026-03-10]` y `[2026-10-27]` (:221-229): `BLOQUES["05"] =
   (90, 115)` rompe abajo a `(105, 120)` y el bloque abre en 90 y cierra en 102 (verde): con la
   regla no decide y manda la de las 01 (alcista), así que a las 11 sale ALCISTA en vez de
   BAJISTA. Se rehace `_m1_del_dia` para que cada bloque diga el sentido de su cuerpo (p. ej. un
   tercer campo en `BLOQUES`: el de las 05 abre en su alto y cierra en medio, roja); los asserts
   :227-229 (la H4 que cierra a mitad de la sesión de las 07 cuenta en la de las 11) quedan
   iguales.
7. `test_semana_normal_las_h4_cierran_a_la_hora_de_las_sesiones` (:232-240): mismo `BLOQUES`,
   mismo motivo, misma solución; sus asserts (`fin_05 == apertura de las 11`, BAJISTA a las 11,
   ALCISTA a las 07) no cambian.

Los otros 14 pasan con el parche tal como están (entre ellos los de la doble ruptura con color,
`test_romper_por_un_punto_basta` -cierra verde por defecto y rompe arriba- y
`test_anti_look_ahead…`).

### 1.c Lo que el trader dijo antes, y si choca con la regla del WhatsApp

Leído como evidencia (ficheros de `knowledge/evidence/`, con Read). **Matiz al encargo:** v3 y v4
no están en cuarentena, pero v9 SÍ (`SESIONES_EN_CUARENTENA = {"v7", "v8", "v9", "v10"}`,
`corpus/cuarentena.py:51`); leer el ÍTEM de evidencia está permitido igual (CLAUDE.md: la
evidencia tiene su propio criterio, y `kb` solo oculta el ítem cuya cita cae en un tramo no citable
o trae un día oculto), y 0:13:12-0:13:20 no cae en ningún tramo de v9 de
`tramos_no_citables.yaml`. No se abrió ninguna transcripción de v9. A-1 tiene siete ítems
(`ambiguedades.yaml:21-28`), no los tres que nombra el encargo: se leyeron los siete, más los
tres de `sesgo.h4` que el auditor señaló.

| Ítem | Literal (recortado a lo que decide) | Frente a la regla del WhatsApp |
|---|---|---|
| `ev-v3-010948-331c69aa` (v3 1:09:48-1:10:27, tema `sesgo.h4.cambio_exige_cierre_bajo_mecha`) | «tendría que terminar por debajo al menos su mecha por debajo para poder considerar nosotros pues ese cambio de escenario si no operaríamos alcistas independientemente si aquí es rojo rojo rojo verde» | **compatible**: condición necesaria (romper por abajo, basta la mecha) y el color de las velas que NO rompen no cuenta; no dice de qué color cierra la que rompe |
| `ev-v3-011045-a185d2ba` (v3 1:10:45-1:11:21, tema `sesgo.h4.cambio_exige_cierre_encima`) | «para yo poder considerar alcista esta vela de h4 … haber terminado por encima de esta y el color verde … la siguiente sería alcista también … como termina por debajo sería bajista» | **sostiene la regla**: terminar por encima Y verde |
| `ev-v4-004603-d0ffd4f2` (v4 0:46:03-0:46:18) | «como finalizó por debajo llegó terminó mitigar esto entonces … bajista» | compatible (finalizar por debajo → bajista) |
| `ev-v9-001312-19e45e4a` (v9 0:13:12-0:13:20, `valor: mecha`) | «se ha llegado a romper con mecha, con una mecha base inclusive con un pip» | sostiene `mecha` (D4); no habla del color |
| `ev-v3-000824-c81f03eb` (v3 0:08:24, A-1) | «para que yo tome alcista esta vela verde debió de haber pues finalizado al menos con una mecha por encima de esto» | **sostiene la regla**: verde Y mecha por encima |
| `ev-v2-000836-6dbfcd6b`, `ev-v3-000531-4d6375b6`, `ev-v3-011614-a5a05b0a` (los otros de A-1) | la vela anterior fija el enfoque; «alcistas sólo compras bajistas sólo ventas»; la simplificación «solo el color de la vela anterior», dejada abierta | no hablan del cierre de la vela que rompe: compatibles |
| `ev-v3-001001-b5a5aa23` (v3 0:10:01) | «nos lo va a dar la vela anterior [...] independientemente si la vela luego termina verde» | compatible: «la vela luego» es la vela en curso, no la que rompe |
| `ev-v9-000902-25db5bf5` (v9 0:09:02) | «el sesgo es alcista mientras que no se mitigue, pues, con mecha o con cuerpo por debajo de esta vela que es nuestro rango» | sostiene «con mecha o con cuerpo» (D4; es lo mismo que el WhatsApp de las 14:45); el ADR puede citarlo junto a `ev-v9-001312` |
| `ev-v4-003431-3968a5ca` (v4 0:34:31, confianza media) | «la vela anterior no terminó por debajo entonces todavía buscamos operativa alcista» | compatible (terminar por debajo) |
| `fb-2026-09-09-sesion-01-41f46b21` (RESOLVE_UNKNOWN de A-1, activo según `feedback trace A-1`; v6 1:03:01-1:04:30) | literal: «si no genera un rompimiento por encima … seguiríamos operando bajista [...] si es un equal [...] bajista [...] o bien, con una mecha [...] la siguiente operativa [...] sería alcista». Notas de Aleks: «en 1:04:30 una vela que termina bajista pero cuya mecha rompio por encima deja el sesgo alcista. El criterio es la ruptura del extremo, no el color ni el cierre» | el literal sostiene `mecha` (D4); **las notas describen justo el caso 3 del gráfico con el resultado contrario** |

Las notas de `41f46b21` obligaban a mirar. Se leyó la transcripción de v6 (capa corregida,
filtrada; v6 está fuera de la cuarentena con sus dos tramos bloqueados, 0:41:00-0:50:11 y
1:53:30-1:57:31, no tocados) con `corpus transcript show --video v6 --t0 1:03:01 --t1 1:05:50`:

- 1:03:48-1:04:06, el contexto: «seguimos buscando bajistas … tenemos un enfoque bajista, hasta
  que … el precio debería de generar un breaker por encima de esta zona». El sesgo previo es
  BAJISTA.
- 1:04:06: «o bien, con una mecha, … supongamos que esto termina con una mecha por encima **y la
  vela termina verde**, la siguiente operativa … sería, pues, alcista … no un equal, porque si
  fuera un equal, seguiríamos operando bajista». **Compatible** (caso 2, verde).
- 1:04:30-1:04:47: «ahora en este caso no lo hace pero a esta vela de aquí mira **terminó
  bajista** vale pero todo su movimiento como tal **su mecha fue alcista** entonces buscaríamos
  nosotros lo que sería pues **operativa alcista** alcistas por eso es que aquí nos enfocamos en
  buscar operativa alcista».
- 1:04:54-1:05:25: «qué ocurriría si el precio llega y hace con cuerpo … el precio llega aquí y te
  genera un rompimiento aquí y aquí te deja una mecha entonces tú **seguirías buscando operaciones
  bajistas** porque al final y al cabo el precio se arrojó por debajo». **Compatible** con el
  WhatsApp (rompe y cierra de vuelta: no cambia), si describe eso.
- 1:05:26-1:05:35: «pues en este caso fue puesta mecha **aunque fue roja la vela, pues es
  indiferente**, eso, entonces **la siguiente operativa es alcista**».

**Conclusión de 4.c: SÍ hay una contradicción.** Con sesgo previo bajista, una H4 que rompe por
encima con la mecha y cierra ROJA: en la sesión 1 (v6 1:04:30-1:05:35, el 2026-09-09) el trader
dijo «la siguiente operativa es alcista … aunque fue roja la vela, es indiferente»; por WhatsApp
el 2026-10-14 (caso 3 del gráfico de cuatro casos, confirmado «Si, esta bien bro») dijo que no
cambia y sigue el sesgo que había. Es lo que RN-003 recogió en sus notas (:1013-1016) y lo que
ADR-0044 usó para descartar «el sentido del cierre» (:71-72). No hay ítem de evidencia para
1:04:30-1:05:35 (ningún `ev-v6-*` con `t0` entre 1:03 y 1:06): el detector
(`evidence/contradicciones.py:46-65`) solo abre una contradicción entre ítems VIVOS del mismo
`tema` con `valor` distinto, así que hoy no la puede ver. **PARADA, como manda el encargo: no se
decide aquí** (decisión 0).

Para localizar qué señalaba, se abrieron tres fotogramas de v6 por instante localizado en la
transcripción (ADR-0038; `corpus frames show --video v6 --t 1:04:41 | 1:05:10 | 1:05:31 --n 1`,
`fr-v6-22982c02/3881000`, `/3910000`, `/3931000`). Los tres enseñan el gráfico H4 de EURUSD de
TradingView EN DIRECTO (reloj 20:53-20:54 UTC+2 del 09/09/2026, velas del 3 al 9 de septiembre de
2026), con una línea discontinua horizontal y un trazo a mano del trader (ningún precio se copia
aquí: cuatro de esos cinco días tienen caso reservado, §1.j). No resuelven qué vela señala ni
dónde cerró: la pregunta queda para la sesión 5 con esos instantes.
Lo visto son velas de un gráfico en directo, ninguna operación, ninguna etiqueta (declarado en
§1.j).

### 1.d El registro (D7): carpeta, registros y qué cita cada sitio después

**La carpeta de sesión.** El campo `sesion` tiene que casar con `^\d{4}-\d{2}-\d{2}-sesion-\d{2}$`
(`feedback/modelo.py:85` → `comun/ids.py:29`; `modelo.py:243-244`) y `fecha` tiene que ser la de
esa sesión (`modelo.py:247`); `recibido_el` es el día en que llegó la respuesta. El precedente de
A-42 (`ACTIVACION-A42.md` §1.1 y §6.1, D1) puso sus dos `trader_escrito` en
`knowledge/feedback/2026-10-04-sesion-04/` (`fb-…-af490a3a`, `fb-…-fb7831cc`: `fecha
'2026-10-04'`, `recibido_el '2026-10-06'`, `medio escrito`, `registrado_por` «literal transcrito
por el consultor de la captura <ruta> (sha256 <hash>); la sesion no la abrio porque la guardia lo
impide (ADR-0038). El trader, desde sus dos numeros, confirmado por Aleks el 2026-10-06»).
Propuesta en la decisión 1: la misma carpeta, `2026-10-04-sesion-04`, con `fecha 2026-10-04` y
`recibido_el 2026-10-14`.

**Los dos registros** (`botsito feedback new`, `--medio escrito --procedencia trader_escrito
--recibido-el 2026-10-14`, sin `--grabacion`; los literales son los de la entrada W de
`PROJECT_STATE.md`, transcritos y releídos por el consultor; la sesión no abre las capturas):

| | R1 · CORRECT sobre RN-003 | R2 · CONFIRM sobre `sesgo_h4_criterio_ruptura` |
|---|---|---|
| `--objetivo-tipo` / `--objetivo-id` | `regla` / `RN-003` (precedente `fb-…-ca0afae6`, la cita de hoy) | `parametro` / `sesgo_h4_criterio_ruptura` |
| `--accion` | `CORRECT` | `CONFIRM` |
| `--respuesta` (literal) | las dos burbujas de las 14:55, en una (como A-42 unió «1-B)» y «2-c)»): «Para el cambio de sesgo, por ejemplo en el caso 1 la vela roja debe de haber roto con cuerpo o con mecha el bajo de la vela alcista» + «Y terminar al cierre bajista» | el mensaje de las 14:45: «Dependerá de si cierra alcista o bajista si lo hace con mecha o con cuerpo es válido para un cambio de sesgo» |
| `--valor` | «una H4 cambia el sesgo solo si rompe el extremo de la anterior (con mecha o con cuerpo) y cierra del color de esa ruptura: rompe el bajo y cierra roja, bajista; rompe el máximo y cierra verde, alcista; si rompe un extremo y cierra del color contrario no cambia, sigue el sesgo que había» | `mecha` |
| `--registrado-por` | la fórmula de A-42, con la ruta y el sha256 de las cuatro capturas de mensajes (§1.e) y la nota de que el trader escribe desde su número | la fórmula de A-42 con la captura de las 14:45 (`3ebe6904…`) |
| `--notas` | las 14:45 (literal), las 14:48 (pide el gráfico), el gráfico de cuatro casos del consultor (no son días reales) y las 15:18 «Si, esta bien bro»; la nota de voz de 0:21 de las 14:56 visible en la captura de las 14:55, no transcrita: no se registra ni se interpreta; la contradicción de §1.c y que su confirmación va a la sesión 5 | que resuelve lo que `CORRIDA-CONSTRUCCION.md:1316` (4.a-b) dejó a esta rama; que el criterio lo dijo el trader (`41f46b21`, `ev-v9-001312`), no solo la re-expresión de F11 |

`feedback apply --sesion 2026-10-04-sesion-04 --check` hoy: `9 parametros; 0 cambian, 9 ya
estaban` (medido). Con R2 listará `~ sesgo_h4_criterio_ruptura 'mecha' <- <R2>`: el valor es el
mismo pero la fuente anterior (`8eccf5c0`) no es el registro, y eso no es no-op
(`feedback/aplicar.py:62-80`, el comentario de :77-79); `apply` sin `--check` reescribe solo la
`fuente` del parámetro y da el trailer `Fuente:`. R1 no toca el registro (es sobre una regla):
RN-003 pasa a citarlo a mano, con su `literal` dentro de `respuesta_literal`
(`spec/modelo.py:348 comprobar_literales`).

**Qué cita cada sitio después.** RN-003 → R1 (cita y literal). `sesgo_h4_al_abrir` → R1 (es el
predicado que ejecuta la regla; su literal hoy es el de `8eccf5c0`). `sesgo_h4_criterio_ruptura` →
R2, por `apply`. El término `equal` → decisión 2. `rompe` → **se queda con `8eccf5c0`**: ninguna
regla lo invoca y su literal («al menos por un pip o una milésima de pip») es lo que define
romper. `sesgo_h4_regla` → se queda con `8eccf5c0` y solo cambia su descripción (D7). Ninguno
supersede a `8eccf5c0`: tiene exactamente cinco citas en `knowledge/spec/` (`rompe`,
`sesgo_h4_al_abrir`, `equal`, `sesgo_h4_regla`, `sesgo_h4_criterio_ruptura`; medido con `grep -c`:
3+1+2, descontando la mención en prosa de RN-003 :1013), y G1 de `knowledge validate` niega un
registro supersedido citado sin su sustituto al lado.

### 1.e La evidencia: los seis ficheros, listados sin abrir

`ls -la corpus/whatsapp-sesgo-h4-2026-10-14/` y `sha256sum` de los `.png` (ninguno abierto: la
guardia no deja abrir imágenes, ADR-0038; el `LEEME.md`, 1.449 bytes, y la subcarpeta `ws/` no
entran y no se han leído):

| Fichero hoy | Bytes | sha256 | Nombre al entrar |
|---|---|---|---|
| `2-whatsapp-1445-primera-respuesta.png` | 111.552 | `3ebe6904bd3f756101c4f4a1c697f3eecb4f9ee7b4225d95958fff0c1a729ef7` | `mensaje-whatsapp-2026-10-14-1445-primera-respuesta.png` |
| `3-whatsapp-1448-pide-grafico.png` | 18.092 | `1f398563bfd646dcfaf5c603ea521156e7bbe2a2c90df0f7243ecbae020eccb1` | `mensaje-whatsapp-2026-10-14-1448-pide-grafico.png` |
| `4-whatsapp-1455-regla.png` | 95.456 | `dffb4be4da7072b1e2b0e9368e9a757928b88876542a5a7b8dc28cb276111870` | `mensaje-whatsapp-2026-10-14-1455-regla.png` |
| `6-whatsapp-1518-confirma.png` | 198.285 | `f9c4f0aa3f5382ae519a1d0f6a080ebc3e6c24c6e08a237fb9eb71883178775c` | `mensaje-whatsapp-2026-10-14-1518-confirma.png` |
| `1-grafico-pregunta-dos-casos.png` | 80.269 | `74272a09ae6ffb773a1fb7902c370b976bed8c768b7ff596a04354f86a862ef7` | `grafico-consultor-2026-10-14-pregunta-dos-casos.png` |
| `5-grafico-regla-entendida-cuatro-casos.png` | 122.285 | `390bbdacd322eede7a6ce04010c03930acdb3d724f8b5ca7e17361708597acb0` | `grafico-consultor-2026-10-14-regla-cuatro-casos.png` |

El destino, `corpus/Estrategia del trader/Material adicional de su operativa/Mensajes del trader/`
(la raíz del corpus es `fuentes.yaml:6`; la subcarpeta la describe `fuentes.yaml:181-194`), tiene
hoy 9 ficheros (`mensaje-whatsapp-0208-…` y los ocho `mensaje-whatsapp-2026-10-06-…`), todos en
`manifest.yaml:142-178`; ninguno de los seis nombres nuevos colisiona. Los `mv`, preparados para
que los lance Aleks con «!» (uno por línea; `ws/` y el `LEEME.md` se quedan donde están):

```
mv "corpus/whatsapp-sesgo-h4-2026-10-14/2-whatsapp-1445-primera-respuesta.png" "corpus/Estrategia del trader/Material adicional de su operativa/Mensajes del trader/mensaje-whatsapp-2026-10-14-1445-primera-respuesta.png"
mv "corpus/whatsapp-sesgo-h4-2026-10-14/3-whatsapp-1448-pide-grafico.png" "corpus/Estrategia del trader/Material adicional de su operativa/Mensajes del trader/mensaje-whatsapp-2026-10-14-1448-pide-grafico.png"
mv "corpus/whatsapp-sesgo-h4-2026-10-14/4-whatsapp-1455-regla.png" "corpus/Estrategia del trader/Material adicional de su operativa/Mensajes del trader/mensaje-whatsapp-2026-10-14-1455-regla.png"
mv "corpus/whatsapp-sesgo-h4-2026-10-14/6-whatsapp-1518-confirma.png" "corpus/Estrategia del trader/Material adicional de su operativa/Mensajes del trader/mensaje-whatsapp-2026-10-14-1518-confirma.png"
mv "corpus/whatsapp-sesgo-h4-2026-10-14/1-grafico-pregunta-dos-casos.png" "corpus/Estrategia del trader/Material adicional de su operativa/Mensajes del trader/grafico-consultor-2026-10-14-pregunta-dos-casos.png"
mv "corpus/whatsapp-sesgo-h4-2026-10-14/5-grafico-regla-entendida-cuatro-casos.png" "corpus/Estrategia del trader/Material adicional de su operativa/Mensajes del trader/grafico-consultor-2026-10-14-regla-cuatro-casos.png"
```

Después (fase 1): un párrafo nuevo al final de la descripción de la subcarpeta en `fuentes.yaml`
(solo se añade: los seis ficheros, que los dos gráficos son esquemas dibujados por el consultor y
no días reales, que los literales los transcribió el consultor y los releyó contra las capturas el
2026-10-17, que ningún nombre ni número del trader entra, y la nota de voz de las 14:56 no
transcrita), `botsito corpus inventory` (`cli.py:189`; seis entradas nuevas en `manifest.yaml` con
estos mismos sha256) y los dos registros.

### 1.f El arnés: contar por sesión las H4 saltadas (4.f)

Hoy `ResultadoSesgo.doble_ruptura` (`domain/sesgo.py:62`) → `ANOTACION_DOBLE_RUPTURA = "si"`
(`primitivas.py:64, 184-185`) → `dobles` y la línea «de ellas con doble ruptura…» del arnés
(`arnes.py:289, 308, 394`). Lo mismo, por dos:

- `ResultadoSesgo` gana `saltadas_color_contrario: int = 0` (H4 que rompieron UN extremo y cerraron
  del color contrario, D1) y `saltadas_neutras: int = 0` (H4 que rompieron un extremo y cerraron
  sin cuerpo, D3), contadas por `sesgo_h4` en la búsqueda hacia atrás ANTES de la vela que fija el
  sesgo (o hasta el tope). Valor por defecto 0: el visor, los guiones y `test_huecos_motor.py:457`
  no cambian.
- `primitivas.py`: `ANOTACION_SALTADAS_COLOR = "sesgo_h4_saltadas_color_contrario"` y
  `ANOTACION_SALTADAS_NEUTRA = "sesgo_h4_saltadas_neutra"`, anotadas con el número (como texto)
  solo cuando es mayor que 0, al lado de `sesgo_h4_doble_ruptura`.
- `arnes.py`: dos contadores (sesiones con alguna saltada, y total de saltadas) y dos líneas más en
  «## RN-003 al abrir la sesion»: «sesiones con alguna H4 saltada por color contrario (ADR-0080
  D1): N (M velas)» y lo mismo para la neutra simple (D3). Con eso la fase 4 cuenta «en cuántas
  sesiones cambió el sesgo y por qué regla» sin imprimir ninguna fecha ni precio de H4.
- Tests: `test_sesgo_h4.py` (los campos), y en `test_arnes_motor.py` o `test_huecos_motor.py` una
  corrida sintética que anote y cuente (como hoy `ANOTACION_DOBLE_RUPTURA` en
  `test_huecos_motor.py:244-247`; si va ahí, el contrato se amplía con ese fichero).

La neutra de DOBLE ruptura (ADR-0075) también se salta hoy sin contarse; decisión 4.

### 1.g Lectura de material de la re-corrida (4.g)

La misma que declaró R3.1 (`HOLDOUT-EXPOSICIONES.md:52`, fila del 2026-10-14, punto 2): las tres
corridas de `motor arnes --simular` leen, para calentar el sesgo (`arnes.py:182-199`), el M1
ENTERO de marzo de 2026 (mes reservado entero, `meses_reservados.yaml`) y el de junio de 2026 (11
días reservados medidos hoy por recuento: 2 de holdout-1, 4 de holdout-2, 5 de holdout-3; es el
mismo recuento que la fila del 2026-10-14, anterior a la retirada de un día de holdout-3 por
ADR-0041 en 7f8322a: `casos_reservados` lo sigue contando, y no se investigó por qué), además de
los M1 de construcción. Leer velas para calentar no es abrir (ADR-0021 §1, ADR-0033 §4); las salidas no
llevan ninguna etiqueta ni ningún precio de un día reservado, y el informe no imprimirá la fecha
ni el precio de la H4 que fija ningún sesgo (lección a1, `ERRORES-RECURRENTES.md:84`). Se
declarará con su fila el día de la corrida y ANTES de correrla (fase 4). Recuento de hoy, sin
imprimir ninguna clave: 34 reservados y 34 ocultos (13 en 2026-05, 11 en 2026-06, 10 en
2026-09; 0 en los cuatro meses de construcción).

### 1.h El encargo frente al repo (auditor, 2026-10-17)

El informe del agente `auditor-encargo`, tal cual (corrió en paralelo con la fase 0; solo leyó):

> ## Auditoría del encargo · trabajo/sesgo-h4-color · 2026-10-17
> Resumen: 47 afirmaciones; 37 correctas, 3 incorrectas, 7 con matiz. 12 herencias no recogidas.
>
> Encargo: C:\Users\USER\Desktop\Bot v3\docs\encargos\trabajo-sesgo-h4-color.md. Solo he leído. No he ejecutado pytest, make ni ningún `botsito`, y no he abierto ninguna imagen ni nada de holdout ni de xlsx. Lo único que hice en `corpus/` fue listar nombres y tamaños y calcular el sha256 de los seis ficheros de `corpus/whatsapp-sesgo-h4-2026-10-14/`. Esa carpeta no es la carpeta madre del material adicional.
>
> ### Lo más grave (empiezo por aquí)
> 1. **D4 apoya el criterio de mecha en `fb-2026-09-09-sesion-01-41f46b21`, y las notas de ese registro dicen lo contrario de D1.** `knowledge/feedback/2026-09-09-sesion-01/fb-2026-09-09-sesion-01-41f46b21.yaml:18-20`: «Descarta la simplificacion 'color de la vela anterior': en 1:04:30 una vela que termina bajista pero cuya mecha rompio por encima deja el sesgo alcista. El criterio es la ruptura del extremo, no el color ni el cierre.» Las notas de RN-003 (`strategy_spec.yaml:1015-1016`) salen de ahí. Son notas de Aleks sobre lo que se ve en pantalla en v6 1:04:30, no el literal del trader. Aun así, el encargo dice en 4.c que si algo contradice la regla del WhatsApp hay PARADA, y en D4 cita este registro solo como apoyo. La fase 0 tiene que tratarlo como posible contradicción (al detector y a la sesión 5) y comprobarlo en v6 1:03:01-1:04:30, que no cae en ningún tramo no citable.
> 2. **La línea F que el encargo propone para el cierre rompe `test_hoja_de_ruta.py` (c).** El texto «La re-corrida de R3.1 tras el sesgo la hizo W (SESGO-H4-COLOR.md)…» hace que `DEPENDENCIA` encuentre «tras» y `LETRA_SUELTA` encuentre la «W» (`tests/unit/test_hoja_de_ruta.py:28-31`, `:170-180`). Como W ya no estará viva, da «F depende de W, que no esta viva». Es el mismo fallo que el consultor anotó en `trabajo/hoja-de-ruta` (ERRORES-RECURRENTES.md:78, (2)).
> 3. **La fase 1 cambia la spec y el encargo no pide en ella ni manifiesto ni versión.** `feedback apply` escribe la nueva `fuente` de `sesgo_h4_criterio_ruptura` en `parametros.yaml`. El hash de la spec incluye estado y fuente (`knowledge/spec/spec_manifest.yaml:5-7`) y `spec/manifiesto.py:222-244` rechaza un cambio sin subir `spec_version`. Además `docs/spec/{parametros,reglas,glosario}.md` citan hoy 8eccf5c0. El encargo deja `spec_version`, `spec manifest --escribir` y `spec docs --escribir` para la fase 3; ya hacen falta en el commit de la fase 1, con su `Fuente:`.
>
> ### Afirmaciones
> | # | Afirmación (literal o resumida) | Veredicto | Evidencia |
> |---|---|---|---|
> | 1 | Base: main 59c8ae7, commit de estado sobre el merge fa15a84 (stable/F37q) | CORRECTA | `git log 59c8ae7^` = fa15a84; `rev-parse` del tag = fa15a84 |
> | 2 | main = origin/main = tag, y no hay otra rama | CORRECTA | las dos refs en 59c8ae7; `git branch -a`: solo main, trabajo/sesgo-h4-color y origin/main |
> | 3 | El run 38656985715 «no está escrito en el repo» | CORRECTA | grep en docs/PS/skills: solo sale en el encargo y en SESGO-H4-COLOR.md, los dos nuevos |
> | 4 | Informe y anexos en `docs/validation/SESGO-H4-COLOR.md` y `anexos/SESGO-H4-COLOR/` | CORRECTA | la carpeta de anexos todavía no existe (ver H12) |
> | 5 | activar-sesion «cubre las llegadas por escrito fuera de sesión» | CORRECTA | `.claude/skills/activar-sesion/SKILL.md:3,21` |
> | 6 | Los literales están en la entrada W de PROJECT_STATE | CORRECTA | `PROJECT_STATE.md:34` |
> | 7 | NA:W, R1.2, tramo R1 | CORRECTA | `HOJA-DE-RUTA.md:40,63-64`; contrato `tramo: R1` (`contrato_rama.py:123-146` acepta el id) |
> | 8 | D1: «igual que hoy con la neutra de doble ruptura (ADR-0075)» | CORRECTA | `domain/sesgo.py:96-99`; ADR-0075:17-21 |
> | 9 | D2: ADR-0060 §1, decide el color | CORRECTA | ADR-0060:20-27 |
> | 10 | D3: la reserva de S-13, «solo con un sesgo previo alcista» | CORRECTA | ADR-0075:36-40; fb-…-ca0afae6 notas |
> | 11 | CORRIDA-CONSTRUCCION.md:1316 dejó la decisión del estado a esta rama | CORRECTA | :1316, 4.b «lo decido en la rama que active la respuesta del trader» |
> | 12 | 41f46b21 cierra A-1 y apoya la mecha | MATIZ (grave) | Cierra A-1: es el único registro sobre A-1 (`ambiguedades.yaml:17-31`). Literal «o bien, con una mecha […] sería alcista». Pero sus notas (:18-20) dicen que el color no decide (punto 1) |
> | 13 | ev-v9-001312-19e45e4a apoya la mecha | MATIZ | «se ha llegado a romper con mecha, con una mecha base inclusive con un pip», `valor: mecha`; `revisado_por`: «sin revision humana; la cruda no separa voces y el hablante se atribuye por contexto». Más cerca del WhatsApp está ev-v9-000902-25db5bf5 («con mecha o con cuerpo por debajo»), que el encargo no cita |
> | 14 | Que «mecha» fuera solo una re-expresión del consultor «es inexacta» | MATIZ | El propio 8eccf5c0 dice `registrado_por: … re-expresion canonica del consultor (F11)` (:12) y su literal no dice mecha. Lo inexacto es que el trader no lo hubiera dicho nunca (41f46b21, ev-v9-001312, ev-v9-000902). Contradice a PS:34, ERRORES-RECURRENTES.md:84 (2) y CORRIDA §4.7 (:1315) |
> | 15 | ERRORES-RECURRENTES.md:84: una re-expresión que añade criterio va como DEFAULT_AMBIGUOUS | CORRECTA | fila de `trabajo/corrida-construccion`, lección (2); en la misma fila está el incidente a1 |
> | 16 | El siguiente ADR libre es 0080 | CORRECTA | `docs/adr` llega a 0079; ningún «ADR-0080» en docs |
> | 17 | ADR-0060 §1: «Con un solo extremo roto, el color sigue sin decidir nada» | CORRECTA | ADR-0060:27 |
> | 18 | ADR-0044 §2: «la última H4 que rompió un extremo» | CORRECTA | ADR-0044:19 |
> | 19 | ADR-0044, «su alternativa descartada "el color de la vela NO decide"» | MATIZ | La alternativa es «Ante una ruptura doble, tomar el sentido del cierre» (:57). La frase es el motivo del descarte (:71-72) y esa alternativa ya la revirtió ADR-0060 §1 sin poner recuadro en 0044 (G.2, H2) |
> | 20 | ADR-0075 §3: «con un solo extremo roto el color no decide» | CORRECTA | ADR-0075:58 |
> | 21 | Ningún otro ADR lo contradice | CORRECTA | buscando «color no decide», «solo extremo» y «cierra roja» en docs/adr y runbooks solo salen 0044, 0060 y 0075 |
> | 22 | 8eccf5c0 está citado exactamente cinco veces como `cita`/`fuente` en knowledge/spec | CORRECTA | glossary.yaml:81; parametros.yaml:412 (sesgo_h4_regla) y :427 (criterio_ruptura); strategy_spec.yaml:52 (rompe) y :74 (sesgo_h4_al_abrir). Hay una sexta mención en las notas de RN-003 (:1013), que no es cita |
> | 23 | Supersederlo rompería knowledge validate en esas cinco | CORRECTA | parámetros: `validation/knowledge.py:1023-1029`; spec: `spec/modelo.py:877-886`. Además un supersede tiene que tener el mismo objetivo (`parametro:sesgo_h4_regla`), así que ningún registro de D7 podría supersederlo (`feedback/modelo.py:449-454`) |
> | 24 | RN-003 cita hoy fb-…-ca0afae6 | CORRECTA | strategy_spec.yaml:997 |
> | 25 | El CONFIRM «aplicado con feedback apply --check» | INCORRECTA | `--check` no escribe (`cli.py:974-976`). Primero `feedback apply --sesion <s> --check`, que tiene que proponer solo ese parámetro, y luego sin `--check` (SKILL.md:74-75) |
> | 26 | trader_escrito, medio escrito, recibido_el 2026-10-14 | CORRECTA | `feedback/modelo.py:314-318` (trader_escrito exige escrito) y :300-307 (recibido_el ≥ fecha) |
> | 27 | «A-42 usó la de su pregunta» | CORRECTA | fb-…-fb7831cc y fb-…-af490a3a, en `2026-10-04-sesion-04/` (la pregunta S-7 se hizo en la sesión 4) |
> | 28 | sesgo_h4_regla «que ninguna forma lee desde F12» | CORRECTA | descripción en parametros.yaml (~:401-404) |
> | 29 | sesgo_h4_tope_velas = 60 | CORRECTA | parametros.yaml, `valor: 60`, fuente ADR-0044 |
> | 30 | PS en 24.359 bytes en main, tope 25.000 | CORRECTA | `git show main:PROJECT_STATE.md \| wc -c` = 24359; `test_project_state.py:21` `TOPE_BYTES = 25_000`. En la rama ya está en 24.568 tras la apertura |
> | 31 | primitivas.py escribe `sesgo_h4_doble_ruptura`, arnes.py lo cuenta, también visor.py | CORRECTA | primitivas.py:64,184-185; arnes.py:308; visor.py:775 |
> | 32 | RN-003 «según sesgo_h4_regla», notas contrarias, RN-033; «equal» cita 8eccf5c0 | CORRECTA | strategy_spec.yaml:985-989,1052; glossary.yaml:75-81 |
> | 33 | Fallan siete de test_sesgo_h4.py | CORRECTA (por lectura, sin ejecutar) | Con sus nombres: `test_rompe_arriba_es_alcista_y_el_color_no_decide` (:40), `test_rompe_abajo_es_bajista` (:47), `test_un_equal_no_rompe` (:58), `test_una_neutra_mantiene_el_sesgo_anterior_alcista_y_bajista` (:90; falla solo la mitad bajista), `test_semana_de_desfase_la_h4_de_mitad_de_sesion_cuenta_en_la_siguiente[2026-03-10]` y `[2026-10-27]` (:222) y `test_semana_normal_las_h4_cierran_a_la_hora_de_las_sesiones` (:232). Matiz: el primero no falla por el verde por defecto, sino por la vela roja explícita que rompe arriba (:41) |
> | 34 | «las evidencias de A-1» son ev-v3-010948, ev-v3-011045 y ev-v4-004603 | MATIZ (incompleta) | A-1 tiene siete (`ambiguedades.yaml:21-28`). Faltan ev-v2-000836-6dbfcd6b, ev-v3-000531-4d6375b6, ev-v3-000824-c81f03eb (apoya color + ruptura: «vela verde… finalizado al menos con una mecha por encima») y ev-v3-011614-a5a05b0a. Otras de sesgo.h4 que pueden chocar: ev-v3-001001-b5a5aa23 («independientemente si la vela luego termina verde»), ev-v9-000902 y ev-v4-003431-3968a5ca. ev-v3-010948 dice «independientemente si aquí es rojo rojo rojo verde»; ev-v3-011045 exige «terminado por encima… y el color verde»; ev-v4-004603, «finalizó por debajo» |
> | 35 | «no hay cuarentena en v3, v4 ni v9» | INCORRECTA (v9) | `corpus/cuarentena.py:51`: `SESIONES_EN_CUARENTENA = {"v7","v8","v9","v10"}`. Leer el ítem de evidencia sí está permitido (CLAUDE.md) y 0:13:12 no cae en ningún tramo de v9 de `tramos_no_citables.yaml` |
> | 36 | ACTIVACION-A42.md §1.1, :476 y :494 | CORRECTA | :29 «1.1 Están las 8»; :476 fila D1 de la PARADA; :494 respuesta D1 |
> | 37 | rompe no lo invoca ninguna regla | CORRECTA | ninguna forma lo usa; notas en strategy_spec.yaml:57-58 |
> | 38 | Seis ficheros más LEEME.md y ws/ | CORRECTA | Nombres, bytes y sha256: 1-grafico-pregunta-dos-casos.png 80269 74272a09ae6ffb773a1fb7902c370b976bed8c768b7ff596a04354f86a862ef7; 2-whatsapp-1445-primera-respuesta.png 111552 3ebe6904bd3f756101c4f4a1c697f3eecb4f9ee7b4225d95958fff0c1a729ef7; 3-whatsapp-1448-pide-grafico.png 18092 1f398563bfd646dcfaf5c603ea521156e7bbe2a2c90df0f7243ecbae020eccb1; 4-whatsapp-1455-regla.png 95456 dffb4be4da7072b1e2b0e9368e9a757928b88876542a5a7b8dc28cb276111870; 5-grafico-regla-entendida-cuatro-casos.png 122285 390bbdacd322eede7a6ce04010c03930acdb3d724f8b5ca7e17361708597acb0; 6-whatsapp-1518-confirma.png 198285 f9c4f0aa3f5382ae519a1d0f6a080ebc3e6c24c6e08a237fb9eb71883178775c. Ninguno está ya en manifest.yaml |
> | 39 | Destino: la subcarpeta «Mensajes del trader» que describe fuentes.yaml | CORRECTA | fuentes.yaml:6 (raíz), :162, :181 |
> | 40 | HOLDOUT-EXPOSICIONES.md:52-53: el calentamiento lee el M1 de marzo y junio | CORRECTA | :52 punto (2) y :53 punto (1) |
> | 41 | Comandos de :571-577; el arnés añade el sufijo DIAGNOSTICO; patrones.py lee la ruta por argumento | CORRECTA | :571, :574 y :577; `engine/diagnostico.py:169`; `patrones.py:165,203`. Las salidas de referencia son las de §4.9 (7cf8901), no las de §3.1 |
> | 42 | Diagnóstico, ADR-0070 §3 | CORRECTA | ADR-0070:54 y enmiendas |
> | 43 | HISTORIA:7638 es la «# Next Action HECHA · W» del 2026-10-10; qué acepta el test | CORRECTA | :7638. El test solo pide `^# Next Action HECHA · ([A-Z]) ·` (`test_hoja_de_ruta.py:61`); el formato completo con rama y fecha es el de RITUAL.md:141. Precedente de letra repetida: E en :5881 y :8656 |
> | 44 | Línea preparada para F | INCORRECTA | punto 2 de arriba |
> | 45 | R4.1 (HOJA:167, :176 y :178) «deja de esperar a NA:W y a R1.2» | MATIZ | :167 (Refs NA:W) y :178 (Depende R1.2) sí esperan. :176 no espera nada: dice «sin su pregunta 1 (el sesgo, respondida: R1.2)», y es ahí donde entra la pregunta de D3. Quitar NA:W de :167 es obligatorio (test b, :147-148) |
> | 46 | trabajo/* no dispara la CI; rama fix/sesgo-h4-color; RITUAL:92-104 | CORRECTA | `.github/workflows/ci.yml:3-4`; RITUAL.md:101-103 (`trabajo/<rama>:refs/heads/fix/<rama>`). La puerta y el único fallo esperado de state check están en :105-106 |
> | 47 | Fase 1: «feedback new, feedback apply --check y knowledge validate en verde» | MATIZ | falta spec_version, manifest y docs en ese commit (punto 3 de arriba) |
>
> ### Lo que el repo pide y el encargo no recoge
> | # | Qué | Dónde lo pide | Evidencia |
> |---|---|---|---|
> | H1 | Un tercer CORRECT vivo sobre RN-003. `feedback pending` ya no admite dos (hoy 31fb311f y ca0afae6), y la verificación de la skill («feedback pending no lista nada de lo activado») fallará | G.2 de la hoja; SKILL.md:105 | HOJA-DE-RUTA.md:325-327; dos CORRECT vivos en sesion-03 y sesion-04 |
> | H2 | A ADR-0044 le falta el recuadro de §1 y su fila del índice. Esta rama le pone recuadros a 0044 y no dice nada de §1 | G.2 | HOJA-DE-RUTA.md:327-328 |
> | H3 | El índice de ADR: `test_adr.py:42` exige «\| 0080 \|» en docs/adr/README.md, y ADR-0075 puso allí su columna de enmienda. `docs/adr/README.md` no está en las `rutas_permitidas` del contrato, así que `contrato_rama.py` lo rechazará | test_adr; README:81 (precedente) | contrato.yaml, rutas_permitidas |
> | H4 | A-1 está RESUELTA por 41f46b21, que dice que el criterio no es el color. El encargo no dice si A-1 se reabre (REOPEN) y se vuelve a resolver, ni por qué no | AMBIGUEDADES.md; skill: «Lo fijado no se pisa… una respuesta anterior del trader: PARADA» | ambiguedades.yaml:17-31; SKILL.md:30-34 |
> | H5 | F pone la re-corrida después de E y de O; el encargo la hace dentro de W. La hoja la exige en R1.2 («Hecho cuando»), pero el encargo no explica el cambio de orden | PS F | PROJECT_STATE.md:32; HOJA-DE-RUTA.md:73-74 |
> | H6 | Volver a correr guiones cerrados (`scripts/sesgo_h4_diagnostico.py`, que lee marzo para calentar abril; `sesgo_p1.py` y `sesgo_2x2.py`, que leen marzo y junio) es otra lectura que hay que declarar. 4.g solo cubre las tres corridas, y sesgo_p1 ya provocó el incidente a1 | HOLDOUT-EXPOSICIONES:53; ERRORES-RECURRENTES:84 | `sesgo_h4_diagnostico.py:12-13` |
> | H7 | Fila de la fase 0 en HOLDOUT-EXPOSICIONES el mismo día. Precedente: A-42 declaró el listado de capturas por nombre y tamaño. Yo listé y calculé el hash de los seis ficheros (sin abrir ninguno) | ADR-0021 §4 | HOLDOUT-EXPOSICIONES.md:45 |
> | H8 | CORRECT exige `valor_resultante`. El README de feedback pide además la ruta de la captura en `notas`; el precedente la pone en `registrado_por` y en `notas` | modelo.py:77,268; feedback/README.md:79 | fb-…-af490a3a y fb-…-fb7831cc |
> | H9 | Añadir ID:ADR-0080 a las Refs de R1.2 en el cierre, como R1.1 y R3.1 con sus ADR | precedente de la hoja | HOJA-DE-RUTA.md:43-45,127 |
> | H10 | Si ADR-0080 dice que la «re-expresión» es inexacta, CORRIDA §4.7, ERRORES-RECURRENTES:84 y R1.2 dicen otra cosa. El régimen de informes cerrados (recuadro) choca con el encargo (§3) y con el contrato, que protegen CORRIDA-CONSTRUCCION. ERRORES-RECURRENTES sí se puede tocar: hay que decidir si se anota | CLAUDE.md, régimen de docs/validation | CORRIDA-CONSTRUCCION.md:1315; HOJA:68 |
> | H11 | El arnés no crea la carpeta de salida: `salida.write_text` sin mkdir (cli.py:2472), y falla al final, después de unos 5 min leyendo M1 reservado. La carpeta anexos/SESGO-H4-COLOR/ no existe | — | `ls`: no existe |
> | H12 | No citar ADR-0080 en docs/** ni en un `Fuente:` antes de que exista (la guardia de ids citados) | knowledge.py:893-897 | memoria «ids futuros» |
>
> ### Comandos del encargo
> | # | Comando | Existe y se ejecuta así | Evidencia |
> |---|---|---|---|
> | 1-3 | `uv run botsito motor arnes --simular --diagnostico-a35 {cierre,inicio}_vela_contraria --diagnostico-a44 sin_tope [--diagnostico-cuenta-diaria] --salida …` | Sí | cli.py:3079-3094, 2288-2333; `LECTURAS` en pivotes_m15.py:44; `MODOS_A44` en diagnostico.py:48 (ver H11) |
> | 4 | `feedback new` | Sí | cli.py:3213-3246. `--recibido-el` y `--procedencia` son obligatorios por guardia; `--valor` es obligatorio para CORRECT |
> | 5 | `feedback apply --check` | Existe, pero no escribe | falta `--sesion` (cli.py:3249-3251) y la segunda pasada sin `--check` |
> | 6 | `knowledge validate`, `corpus inventory`, `spec manifest --escribir`, `spec docs --escribir` | Sí | cli.py:2932, 3207-3210; precedente de inventory en ACTIVACION-A42.md:581 |
> | 7 | `patrones.py <ruta>` | Sí, ruta por argv | patrones.py:203 |
> | 8 | `git push origin trabajo/sesgo-h4-color:refs/heads/fix/sesgo-h4-color` | Forma correcta | RITUAL.md:103; según la memoria del proyecto, el push lo lanza Aleks porque el clasificador lo niega |
>
> ### Lo que no pude comprobar
> - El contenido de las capturas (literales, la hora 15:18 de Lima, la nota de voz de 0:21 a las 14:56): son imágenes y la guardia no deja abrirlas.
> - Lo que hay en pantalla en v6 1:04:30, que es lo que decide el punto 1: no abrí ni fotograma ni transcripción.
> - Que fallen exactamente esos siete tests y ningún otro: lo razoné sobre el código sin ejecutar nada. Por lectura, test_huecos_motor.py, test_cableado.py y test_visor.py parecen seguir pasando, pero no lo he medido.
> - Si la retirada del día de holdout-3 (ADR-0041) cambia el recuento de días reservados de junio que declarará la fila de 4.g.
> - La CI 38656985715: no consulté gh. La sesión la dio por buena con `gh run view` (SESGO-H4-COLOR.md:19-21).
>
> ### Lo más grave
> Hay tres cosas que cambian lo que se pide. Primera: D4 usa 41f46b21 como apoyo cuando sus notas, y las de RN-003 que salen de ellas, dicen justo lo contrario de D1. Por la propia regla de 4.c eso pide PARADA y mirar v6 1:04:30. Segunda: la línea F preparada para el cierre rompe `test_hoja_de_ruta.py` (c). Tercera: la fase 1 cambia la fuente de un parámetro y por tanto el hash de la spec; sin `spec_version`, `spec manifest` y `spec docs` en ese mismo commit, `make check` no sella. A eso se suman el error sobre la cuarentena de v9, que `--check` no aplica nada, y el índice de ADR que el contrato no deja tocar.

**Lo que se hizo con cada hallazgo:** punto 1 → medido en §1.c (la transcripción y tres
fotogramas de v6: la contradicción existe) y es la decisión 0; punto 2 → §1.k, con un texto
alternativo para F; punto 3 → §1.k (la fase 1 lleva `spec_version`, manifest y docs); #13 y #34 →
las filas nuevas de §1.c (`ev-v9-000902`, `ev-v3-000824`, `ev-v3-001001`, `ev-v4-003431` y los
otros tres de A-1: ninguno contradice, dos sostienen); #14 → en «Lo que NO pregunto» (la lección de
ERRORES-RECURRENTES sigue en pie); #19 → el recuadro de 0044 nombra la alternativa y su motivo;
#25 → §1.k (`--check` y después `apply`); #33 (matiz) → §1.b, test 1: la roja explícita de :41, en
efecto; #35 → §1.c (v9 sí está en cuarentena; el ítem se lee); #45 → §1.k; H1 → §1.k (G.2, se dice
con la salida); H2 → decisión 7; H3 → el contrato, ampliado en este commit; H4 → decisión 6; H5 y
H10 → «Lo que NO pregunto»; H6 → §1.k (ningún guion cerrado se vuelve a correr); H7 → hecho (fila
del 2026-10-17); H8 → §1.d (ruta y sha en `registrado_por` y en `notas`); H9 → §1.k; H11 → §1.k
(README de anexos en la fase 1); H12 → el bloque `ids-inexistentes` de §1 y las notas sin número.
El recuento de junio tras ADR-0041 (lo que el auditor no pudo comprobar) está en §1.g: 11 días
reservados de junio hoy, medido, los mismos que antes de la retirada.

### 1.i Lo que no pude medir

- Qué dan con el parche `test_huecos_motor.py:316` (la corrida sobre construcción con `data/`) y
  `test_visor.py:393`: el clon no tiene `data/` y se saltaron. Se miden en la rama, en el `make
  check` de la fase 3.
- Qué vela señala el trader en v6 1:04:30-1:05:35 y dónde cerró: los tres fotogramas no lo
  resuelven (§1.c).
- Las seis capturas del WhatsApp: la guardia no las abre; los literales son los del consultor.

### 1.j Exposiciones de hoy

Declaradas en `HOLDOUT-EXPOSICIONES.md` (fila del 2026-10-17). Lo que leyó la sesión: ningún
libro, ninguna captura, ninguna hoja; las transcripciones corregidas y FILTRADAS de v3
(1:09:46-1:11:21) y v6 (1:02:53-1:05:50), fuera de cuarentena y fuera de los tramos no citables;
tres fotogramas de v6 (1:04:41, 1:05:10, 1:05:31) con el gráfico H4 de EURUSD en directo del 3 al
9 de septiembre de 2026 (velas y líneas del trader; ninguna operación, ninguna etiqueta;
septiembre de 2026 tiene 10 días reservados por recuento, y de los cinco días laborables que
enseña el gráfico, el recuento de pertenencia está en la fila); la carpeta
`corpus/whatsapp-sesgo-h4-2026-10-14/` por nombre, tamaño y hash; los repartos solo por recuento
(§1.g). Ninguna cifra del bot ni ninguna etiqueta sobre ningún día reservado: no quema.

### 1.k Hallazgos para las fases, el contrato y el cierre

- El contrato se amplía en el commit de esta fase 0 con `docs/adr/README.md` (el índice exige la
  fila de 0080 y las enmiendas de 0044, 0060 y 0075: `test_adr.py:38-42`; H3 del auditor); lo
  demás del contrato ya cubre la fase 3.
- **La fase 1 ya cambia la spec** (auditor, punto 3): `feedback apply` escribe la `fuente` nueva de
  `sesgo_h4_criterio_ruptura`, y el hash de la spec cubre estado y fuente
  (`spec_manifest.yaml:5-7`; `spec/manifiesto.py:222-244` rechaza el cambio sin subir
  `spec_version`). El commit de la fase 1 lleva por tanto `spec_version` (parche), `spec manifest
  --escribir`, `spec docs --escribir` y su `Fuente:`; la fase 3 vuelve a subirla con la regla.
- `feedback apply --check` no escribe (`cli.py:974-976`): la fase 1 hace `--check` (que debe
  proponer solo `sesgo_h4_criterio_ruptura`) y después `apply` sin `--check` (auditor, #25).
- El arnés no crea la carpeta de `--salida` (`cli.py:2472`, auditor H11): la fase 1 commitea
  `docs/validation/anexos/SESGO-H4-COLOR/README.md` (qué es cada fichero y los tres comandos),
  como hizo R3.1 (decisión 3 de su PARADA).
- ADR-0080 no se cita en `docs/**` ni en un `Fuente:` antes de existir (auditor H12): este
  informe lo declara en su bloque `ids-inexistentes` hasta la fase 3, y las notas de R1 y R2 (fase
  1) dicen «el ADR de esta rama» sin número.
- **La línea F que propone el encargo rompe `test_hoja_de_ruta.py` (c)** (auditor, punto 2):
  «La re-corrida de R3.1 **tras** el sesgo la hizo **W**» casa con `DEPENDENCIA` (`\btras\b`,
  :28-31) y `LETRA_SUELTA` saca la W, que ya no estará viva (:170-180): «F depende de W, que no
  esta viva». Texto alternativo, mismo contenido y sin palabra de dependencia ni letra: «E → O →
  V. La re-corrida de R3.1 con el sesgo nuevo ya está hecha (SESGO-H4-COLOR.md §4); si E cambia lo
  que simula, su encargo decide si hace falta otra.» Se mide en memoria antes del cierre, como hizo
  `trabajo/entrada-enero`.
- R4.1 en la hoja: :167 (`NA:W` en Refs) y :178 (`R1.2 (NA:W)` en Depende) sí esperan y tienen que
  cambiar (test b); :176 solo dice «sin su pregunta 1 (el sesgo, respondida: R1.2)», y ahí entra
  la pregunta de D3 (auditor, #45). R1.2 gana `ID:ADR-0080` en sus Refs (H9).
- `feedback pending` ya lista como pendiente el CORRECT de la sesión 3 sobre RN-003
  (`fb-2026-09-29-sesion-03-31fb311f`, «RN-003 no lo cita todavia»); con R1 citado por RN-003,
  saldrá también `ca0afae6`. Es la deuda G.2 de la hoja (:325-327, «no admite dos CORRECT vivos»),
  no un fallo de esta rama; el informe lo dirá con la salida (auditor H1).
- La hoja de ruta (`docs/plan/`) y `docs/validation/CORRIDA-CONSTRUCCION.md` quedan protegidas: sus
  cambios son del commit del contrato de la orden de cierre, como en R3.1 (c87efd9).
- Ningún guion cerrado (`scripts/sesgo_h4_diagnostico.py`, `sesgo_p1.py`, `sesgo_2x2.py`) se vuelve
  a correr en esta rama: cada uno lee el M1 de marzo o de junio para calentar (auditor H6) y el
  encargo no lo pide. Si el consultor quiere una de esas salidas con el motor nuevo, se declara
  antes en HOLDOUT-EXPOSICIONES y la salida nueva va a los anexos de esta rama, nunca sobre la
  cerrada.

## Lo que necesito que decidas

0. **La contradicción de §1.c (v6 1:04:30-1:05:35 frente al WhatsApp del 2026-10-14).**
   Opciones: (a) la rama ACTIVA la regla del WhatsApp -la respuesta más reciente, escrita, con el
   gráfico de cuatro casos confirmado cinco semanas después de la sesión 1- y deja la
   contradicción ABIERTA y a la vista: un ítem de evidencia nuevo para v6 1:04:30-1:05:35 (tema
   `sesgo.h4.ruptura_simple_color`, `valor: indiferente`) y otro que supersede a
   `ev-v3-011045-a185d2ba` con el mismo tema y `valor: cierra_del_color` (su cita ya lo dice),
   para que `evidence contradictions` la abra; el ADR la cuenta; la pregunta va a la sesión 5 con
   los dos instantes y los fotogramas; y las notas de R1 lo dicen. (b) Lo mismo sin ítems: la
   contradicción solo en el ADR, en RN-003 y en la lista de la sesión 5. (c) PARADA larga: no se
   activa nada hasta que el trader la resuelva en la sesión 5; la rama queda en fase 0.
   Recomiendo (a): el WhatsApp es la respuesta explícita a la pregunta exacta (P1) y la más
   reciente, y el detector solo ve ítems. Coste de (b): el detector no la ve y no hay nada que la
   cierre mecánicamente. Coste de (c): W, F, V y R1.2 esperan a la sesión 5, y el motor sigue con
   una regla que el trader acaba de corregir por escrito.
1. **La carpeta de sesión de R1 y R2.** Opciones: (a) `2026-10-04-sesion-04` (`fecha 2026-10-04`,
   `recibido_el 2026-10-14`), como A-42; (b) una carpeta nueva con el formato obligatorio, p. ej.
   `2026-10-14-sesion-05`, que nombra una sesión que no ha existido y choca con V; (c) ampliar el
   formato de `sesion` (código, `comun/ids.py:29`, fuera del encargo). Recomiendo (a): es el
   precedente, cumple el formato y `feedback apply` ya trabaja con esa sesión (9 no-op hoy).
   Coste de (b): una «sesión 5» falsa en el feedback. Coste de (c): una rama de código aparte.
2. **La cita del término `equal`.** Opciones: (a) conserva `8eccf5c0` (lo que sostiene -un equal
   no rompe, «al menos por un pip»- no cambia) y su definición gana «y cerrar del color de esa
   ruptura (ADR-0080)» nombrando el ADR; (b) pasa a citar R1, cuyo literal habla del cambio de
   sesgo pero no del equal. Recomiendo (a): nada afirma más de lo que su cita sostiene. Coste de
   (b): una cita que no habla del término.
3. **RN-033 y el token `insuficiente`.** Opciones: (a) una línea en las notas de RN-033 y en la
   descripción de `insuficiente` (:530-531): desde ADR-0080 también sale cuando todas las rupturas
   del tope cerraron del color contrario o sin cuerpo; forma, cita y `cuando` iguales; (b) no se
   toca RN-033. Recomiendo (a): es verdad medida (§1.b, test 1) y RN-033 es la guardia que la
   aplica. Coste de (b): la spec dice que `insuficiente` es «ninguna ruptura», y ya no es solo eso.
4. **Qué cuenta el arnés.** Opciones: (a) solo lo del encargo: color contrario (D1) y neutra simple
   (D3); (b) además la neutra de doble ruptura de ADR-0075, en un tercer campo y anotación, porque
   hoy se salta sin contarse. Recomiendo (b): cuesta una línea más y la fase 4 lo informa entero.
   Coste de (a): la neutra doble sigue invisible en el arnés.
5. **El literal de R1.** Opciones: (a) las dos burbujas de las 14:55 unidas, como propongo en §1.d;
   (b) solo la primera («Para el cambio de sesgo … el bajo de la vela alcista»), y «Y terminar al
   cierre bajista» en notas; (c) el literal de las 14:45. Recomiendo (a): las dos burbujas son la
   regla entera (ruptura y cierre) y A-42 unió burbujas así. Pido además que confirmes que los
   cuatro literales de la entrada W son los exactos (son los que entran tal cual).
6. **A-1** (RESUELTA por `41f46b21`, cuyas notas dicen que el color no decide; auditor H4).
   Opciones: (a) no se reabre: su pregunta («qué vela H4 fija el sesgo y cuándo cambia») sigue
   contestada -la H4 previa, y cambia cuando rompe el extremo-, y lo que cambia es la condición del
   cierre, que entra por el CORRECT sobre RN-003, igual que ADR-0060 (el color con doble ruptura)
   y ADR-0075 (la neutra) cambiaron la regla sin reabrir A-1 ni A-34; el ADR lo dice. (b) `REOPEN`
   de A-1 con `supersede` a `41f46b21` y un `RESOLVE_UNKNOWN` nuevo con la regla (cinco sitios,
   `AMBIGUEDADES.md`). Recomiendo (a): es el precedente de los dos ADR anteriores. Coste de (b):
   la cadena de A-1 pierde al registro que sostiene `mecha` (D4) y RN-003 pasaría a citar un
   registro de ambigüedad en vez del CORRECT.
7. **El recuadro de ADR-0044.** Opciones: (a) un solo recuadro de esta rama que enmienda §2 y la
   alternativa descartada, y dice de paso que §1 («doble ruptura = AMBIGUO») ya lo enmendaron
   ADR-0060 §1 y ADR-0075 (la deuda G.2 de la hoja, :327-328, que pide ese recuadro y su fila del
   índice; auditor H2); (b) solo §2, y G.2 sigue debiendo el de §1. Recomiendo (a): es el mismo
   recuadro y la misma fila del índice, y deja el ADR entero al día. Coste de (b): un segundo
   recuadro en otra rama para el mismo fichero.

Lo que NO pregunto porque el encargo ya lo fija y el repo lo sostiene: D1-D6 (la fase 0 no mide
nada que las contradiga, salvo lo que la contradicción de §1.c hace con D4 -el literal de
`41f46b21` sigue sosteniendo `mecha`, y `ev-v9-000902` dice «con mecha o con cuerpo»-), los
nombres de los seis ficheros, las tres corridas de la fase 4 tal cual, que `rompe` y
`sesgo_h4_regla` se quedan, y que la re-corrida va dentro de W aunque F la pusiera después de E y
de O (la hoja la exige en «Hecho cuando» de R1.2; auditor H5). Tampoco pregunto por
`ERRORES-RECURRENTES.md:84` y `CORRIDA-CONSTRUCCION.md:1315` (auditor H10): la lección sigue
siendo verdad -el literal de `8eccf5c0` no dice mecha y entró CONFIRMED sin pregunta-; lo que el
ADR añade es que el trader sí lo había dicho en otros sitios (`41f46b21`, `ev-v9-001312`,
`ev-v9-000902`), y eso no corrige ninguna de las dos líneas.

### 1.l Respuesta del consultor a la PARADA (2026-10-17), tal cual

> Modelo: Fable 5.1 · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA de la fase 0 de trabajo/sesgo-h4-color (2026-10-17). Cópiala tal cual en el informe, como manda fase-cero, y aplícala punto por punto.
>
> 0. La contradicción con v6 1:04:30-1:05:35: (a), con dos cambios.
>    - Se activa la regla del WhatsApp. Porqué: es la respuesta escrita a la pregunta exacta, cinco semanas posterior a la sesión 1, y el trader confirmó el caso 3 a propósito («sobre todo el 3 y el 4»). La contradicción queda ABIERTA y a la vista; el ADR, las notas de RN-003 y las de R1 lo cuentan.
>    - Los ítems de evidencia, con el tema de ev-v3-011045-a185d2ba en los dos, porque la guardia exige que el que supersede conserve el tema y el detector solo compara ítems del mismo tema con valor: uno que supersede a ev-v3-011045 con la misma cita y la misma afirmación, que solo añade valor (exige_color_de_la_ruptura), y uno nuevo de v6 1:04:30-1:05:35 con valor color_indiferente. Ninguno nombra el día ni el gráfico del que habla el trader. ev-v3-011045 está citado en la lista de A-1 de ambiguedades.yaml: mide antes si supersederlo rompe knowledge validate o pide tocar A-1. Si lo rompe, si evidence contradictions no abre la contradicción con eso, o si hace falta forzar algo más, se queda en (b) y se dice.
>    - La pregunta para la sesión 5 se hace con un esquema dibujado (como el caso 3), NUNCA con los fotogramas de v6 ni con los instantes de ese gráfico. Porqué: lo que el trader enseña ahí es su sesgo sobre velas en directo de días de fidelidad-1; enseñárselo y que lo explique sería pedirle una etiqueta de esos días.
>
> 0bis. La exposición de §1.j (decisión del consultor, para la fila de hoy de HOLDOUT-EXPOSICIONES). No quema: lo visto son velas y unas líneas del trader, no una operación ni una cifra del bot, y no se sabe qué vela señala. Pero ese pasaje de v6 trae el sesgo que el trader dio en directo sobre un gráfico con cuatro días de fidelidad-1, y eso se acerca a una etiqueta. Por eso:
>    - No se abren más fotogramas de ese tramo ni se cruzan las velas para averiguar qué vela señalaba. Si alguna guardia, guion o test lo hiciera, PARADA.
>    - Amplía la fila del 2026-10-17 con una línea que lo diga, y añade al informe una sección «Para F26»: el pasaje v6 1:03:48-1:05:35 (ya citado por 41f46b21 desde la sesión 1) da el sesgo del trader sobre velas en directo de cuatro días de fidelidad-1; la vela no está identificada y esta rama prohíbe identificarla. Lo decide F26 al rellenar el PREREGISTRO.
>    - Hallazgo para el cierre, no para la rama: antes de abrir un fotograma de un gráfico en directo, se mira qué días enseña por la fecha de grabación del vídeo y se comprueba con casos_reservados si alguno es reservado.
>
> 1. Carpeta de sesión de R1 y R2: (a), 2026-10-04-sesion-04, fecha 2026-10-04, recibido_el 2026-10-14. Porqué: es el precedente de A-42 y no inventa una sesión 5.
>
> 2. La cita del término equal: (a). Conserva 8eccf5c0, y la definición gana «y cerrar del color de esa ruptura (el ADR de esta rama)». Porqué: nada cita más de lo que su literal sostiene.
>
> 3. RN-033 e insuficiente: (a). Una línea en las notas de RN-033 y en la descripción del token; la forma, la cita y el cuándo no cambian. Porqué: es lo medido en §1.b, y la spec no puede decir algo que ya no es verdad.
>
> 4. El arnés: (b). También la neutra de doble ruptura de ADR-0075, en su propio campo y su propia anotación. Porqué: cuesta una línea y la fase 4 cuenta todos los saltos.
>
> 5. El literal de R1: (a), las dos burbujas de las 14:55 unidas. Los cuatro literales de la entrada W son exactos: el consultor los releyó hoy contra las capturas. Tres correcciones a mi encargo:
>    - La nota de voz de 0:21 de las 14:56 no está en la captura de las 14:55: se ve arriba de la de las 15:18 (6-whatsapp-1518-confirma.png). Corrígelo donde lo copiaste.
>    - La captura de las 14:55 trae dos mensajes más del trader que no se registran ni se interpretan: una risa a las 14:55 y, a las 14:56, una petición de que le manden el planteamiento con un gráfico. Se mencionan en las notas de R1 como contexto, sin copiarlos.
>    - Nota de voz: Aleks la escuchó el 2026-10-17 y no añade nada a la regla. No se registra.
>
> 6. A-1: (a), no se reabre. Porqué: es el precedente de ADR-0060 y ADR-0075, y reabrirla quitaría a 41f46b21, que sostiene mecha. El ADR dice que las notas de 41f46b21 («el criterio es la ruptura del extremo, no el color ni el cierre») quedan contradichas por el WhatsApp y que eso es la contradicción abierta del punto 0.
>
> 7. El recuadro de ADR-0044: (a), uno solo que cubre §2, su alternativa descartada y la nota de §1 (deuda G.2). Porqué: es el mismo fichero y la misma fila del índice.
>
> Además:
> - Se aceptan los hallazgos de §1.k: el contrato con docs/adr/README.md; la fase 1 con spec_version, spec manifest --escribir, spec docs --escribir y Fuente:; --check y después apply; el README de los anexos; ADR-0080 sin citar hasta que exista; el texto alternativo de F; R4.1 en :167, :176 y :178; feedback pending con G.2; y no volver a correr guiones cerrados.
> - D4: el ADR cita también ev-v9-000902-25db5bf5 («con mecha o con cuerpo»). ERRORES-RECURRENTES.md:84 y CORRIDA-CONSTRUCCION.md:1315 no se tocan, como dices.
> - Sigue con la fase 1. Los mv de §1.e los lanzo yo con «!» cuando me los pidas, cada uno en su línea.
>
> Rama lista para revisión, NO cerrada, al terminar la fase 4 y el revisor.

### 1.m Corrección al §1.d (punto 5 de la respuesta)

La nota de voz de 0:21 de las 14:56 NO está en la captura de las 14:55: se ve arriba de la de las
15:18 (`6-whatsapp-1518-confirma.png`). Aleks la escuchó el 2026-10-17 y no añade nada a la regla;
no se registra. La captura de las 14:55 trae además dos mensajes del trader que no se registran ni
se interpretan (una risa a las 14:55 y, a las 14:56, una petición de que le manden el
planteamiento con un gráfico): las notas de R1 los mencionan como contexto, sin copiarlos. Donde
§1.d dice «la nota de voz de 0:21 de las 14:56 visible en la captura de las 14:55» vale esto.

### Para F26

El pasaje v6 1:03:48-1:05:35 (sesión 1, 2026-09-09; ya citado por
`fb-2026-09-09-sesion-01-41f46b21` desde la sesión 1) da el sesgo del trader, en directo, sobre
un gráfico H4 que enseña velas de cuatro días de `fidelidad-1` (§1.j, fila del 2026-10-17 de
HOLDOUT-EXPOSICIONES). La vela que señala no está identificada y esta rama prohíbe identificarla:
no se abren más fotogramas de ese tramo ni se cruzan las velas (decisión 0bis del consultor; si
alguna guardia, guion o test lo hiciera, PARADA). Lo que eso vale para la fidelidad lo decide F26
al rellenar el PREREGISTRO. Hallazgo para el cierre (no para esta rama): antes de abrir un
fotograma de un gráfico en directo, se mira qué días enseña por la fecha de grabación del vídeo y
se comprueba con `casos_reservados` si alguno es reservado.

## 2 · Fase 1 · Evidencia y feedback (2026-10-17)

### 2.1 El punto 0 de la respuesta, medido: los ítems de evidencia se quedan en (b)

Antes de crear nada, un guion del scratchpad cargó la evidencia en memoria y añadió dos ítems
sintéticos: uno que supersede a `ev-v3-011045-a185d2ba` (mismo tema, `sesgo.h4.cambio_exige_cierre_encima`,
`valor: exige_color_de_la_ruptura`) y uno de v6 1:04:30-1:05:35 con `valor: color_indiferente`.
Salida:

```
tema del viejo: sesgo.h4.cambio_exige_cierre_encima ; valor: None
G1 con el supersede, fallos: 1
  - knowledge/spec/ambiguedades.yaml:26: nombra ev-v3-011045-a185d2ba, supersedido por ev-v3-011045-00000001; un supersedido solo aparece en el mismo valor o la misma linea de comentario que su sustituto
detector con los dos items nuevos, contradicciones abiertas: 1
  - sesgo.h4.cambio_exige_cierre_encima ['color_indiferente', 'exige_color_de_la_ruptura'] ['ev-v3-011045-00000001', 'ev-v6-010430-00000002']
detector solo con el item de v6, contradicciones abiertas: 0
```

El detector sí abriría la contradicción con los dos ítems, pero supersedir `ev-v3-011045` rompe
`knowledge validate` (G1) en la lista de evidencia de A-1 (`ambiguedades.yaml:26`): habría que
tocar A-1 para sustituir el id, que es justo lo que el punto 0 no quiere. Y el ítem de v6 solo no
abre nada, porque el viejo no tiene `valor`. **Como manda la respuesta, se queda en (b):** ningún
ítem nuevo; la contradicción queda escrita en el ADR, en las notas de RN-003 y en las de R1, y en
la lista «Para el cuestionario de la sesión 5» (con un esquema dibujado, nunca con los fotogramas
de v6: punto 0 y 0bis).

### 2.2 Los dos registros, `feedback apply` y la spec

- **R1** `fb-2026-10-04-sesion-04-6e7da456`: CORRECT sobre RN-003, `medio escrito`,
  `procedencia trader_escrito`, `fecha 2026-10-04`, `recibido_el 2026-10-14`; literal, las dos
  burbujas de las 14:55 unidas (punto 5 de la respuesta); `registrado_por` con la fórmula de A-42
  (ruta y sha256 entero de la captura de las 14:55); notas con la conversación entera (14:45,
  14:48, el esquema de dos casos, 14:55 con los dos mensajes que no se registran, 15:18 y el
  esquema de cuatro casos, la nota de voz de las 14:56 arriba de la captura de las 15:18 que Aleks
  escuchó y no se registra), la contradicción abierta con v6 1:04:30-1:05:35 y la decisión D3.
- **R2** `fb-2026-10-04-sesion-04-d2e84172`: CONFIRM sobre `sesgo_h4_criterio_ruptura`, valor
  `mecha`, literal el mensaje de las 14:45; notas con por qué pasa a ser la fuente y lo que el
  trader ya había dicho de la mecha (`41f46b21`, `ev-v9-001312`, `ev-v9-000902`).
- `feedback apply --sesion 2026-10-04-sesion-04 --check` → `~ sesgo_h4_criterio_ruptura 'mecha'
  <- fb-2026-10-04-sesion-04-d2e84172`, `10 parametros; 1 cambian, 9 ya estaban`. Después, sin
  `--check`: `parametros.yaml` escrito; el diff es la `fuente` del parámetro (de `8eccf5c0` a R2)
  y el serializador deja `valor: mecha` sin comillas. Valor y estado iguales.
- `spec_version` 17.0.2 → 17.0.3 (parche: solo cambia una fuente), `spec manifest --escribir`
  (hash `66c57331…`) y `spec docs --escribir` (`glosario.md`, `parametros.md`, `reglas.md`;
  `ambiguedades.md` también cambia porque lleva la versión).
- `knowledge validate` en verde tras los dos registros (salida en el commit).
- `docs/validation/anexos/SESGO-H4-COLOR/README.md` escrito antes de correr nada (§1.k).
- `fuentes.yaml`: un párrafo nuevo al final de la descripción de «Mensajes del trader» (solo se
  añade) con los seis ficheros, que los dos gráficos son esquemas del consultor, los literales
  releídos el 2026-10-17, la nota de voz y los dos mensajes que no se registran.

Lo que espera a los `mv` de Aleks (§1.e): `botsito corpus inventory` (seis entradas nuevas en
`manifest.yaml`, con los sha256 de §1.e) y su commit.

## 3 · Fases 2 y 3 · Tests primero, el motor, la spec y el ADR (2026-10-17)

### 3.1 Fase 2 · Los tests, en rojo sobre el código de `main`

Los tests se escribieron antes que el motor y se midieron contra el código de `main` (59c8ae7)
en un clon desechable (`git worktree add --detach … main` en el scratchpad, con los tres ficheros
de tests de la rama copiados encima; borrado después). `uv run python -m pytest
tests/unit/test_sesgo_h4.py tests/unit/test_huecos_motor.py tests/unit/test_arnes_motor.py -q`:
**16 FAILED** de los 64 que recogen los tres ficheros (ningún ERROR; los otros 48 pasan en `main`
porque no tocan la regla):

```
FAILED tests/unit/test_sesgo_h4.py::test_caso_1_rompe_el_bajo_y_cierra_roja_es_bajista
FAILED tests/unit/test_sesgo_h4.py::test_caso_3_rompe_el_maximo_y_cierra_roja_sigue_el_sesgo_que_habia
FAILED tests/unit/test_sesgo_h4.py::test_caso_4_rompe_el_bajo_y_cierra_verde_sigue_el_sesgo_que_habia
FAILED tests/unit/test_sesgo_h4.py::test_los_cuatro_casos_al_reves_para_el_alcista
FAILED tests/unit/test_sesgo_h4.py::test_ruptura_simple_sin_cuerpo_no_decide_y_la_busqueda_sigue
FAILED tests/unit/test_sesgo_h4.py::test_color_contrario_sin_nada_detras_dentro_del_tope_es_insuficiente
FAILED tests/unit/test_sesgo_h4.py::test_varias_seguidas_de_color_contrario_se_saltan_todas
FAILED tests/unit/test_sesgo_h4.py::test_la_doble_ruptura_no_cambia_con_la_regla_nueva
FAILED tests/unit/test_sesgo_h4.py::test_con_criterio_de_cuerpo_la_regla_del_color_tambien_vale
FAILED tests/unit/test_sesgo_h4.py::test_las_saltadas_llevan_valor_por_defecto_cero
FAILED tests/unit/test_sesgo_h4.py::test_doble_ruptura_sin_cuerpo_no_decide_y_sin_nada_detras_es_insuficiente
FAILED tests/unit/test_sesgo_h4.py::test_dos_neutras_seguidas_mantienen_el_sesgo
FAILED tests/unit/test_sesgo_h4.py::test_anti_look_ahead_velas_posteriores_y_la_vela_en_curso
FAILED tests/unit/test_huecos_motor.py::test_las_anotaciones_de_las_saltadas_existen
FAILED tests/unit/test_huecos_motor.py::test_una_h4_que_rompe_y_cierra_del_color_contrario_no_cambia_el_sesgo
FAILED tests/unit/test_arnes_motor.py::test_el_informe_cuenta_por_sesion_las_h4_saltadas
```

Lo que cubren, por el encargo: los cuatro casos del esquema (1 y 2 deciden; 3 y 4 «sigue el
sesgo que había», con una H4 detrás que fija el contrario para que se vea que sigue y no da
INSUFICIENTE), los mismos al revés para el alcista, la ruptura simple neutra de D3, el color
contrario sin nada detrás dentro del tope (INSUFICIENTE), varias seguidas de color contrario, la
doble ruptura sin cambios (D2), con criterio `cuerpo`, y sin mirar el futuro (la vela en curso que
rompe arriba y cierra roja, la que la regla nueva saltaría). Los siete de §1.b, rehechos como se
dijo allí, con el color explícito: `test_rompe_arriba_es_alcista_y_el_color_no_decide` pasa a
`test_rompe_arriba_y_cierra_verde_es_alcista` (lo que comprobaba, con el color que hace falta) y
su vela roja es ahora el caso 3; `test_rompe_abajo_es_bajista` → `…_y_cierra_roja_es_bajista`;
`test_un_equal_no_rompe`, `test_una_neutra_mantiene…` (la rama bajista), los dos
`test_semana_de_desfase…` y `test_semana_normal…` cierran roja la vela que rompe abajo
(`_m1_del_dia` gana el sentido del cuerpo por bloque: `BLOQUES["05"]` abre en su alto). Tres
nuevos campos de `ResultadoSesgo` (§1.f, con la neutra doble por el punto 4 de la respuesta)
tienen su test; `test_huecos_motor.py` gana los escenarios `arriba_roja`, `abajo_verde`,
`arriba_sin_cuerpo` y `abajo_sin_cuerpo` (y `abajo` cierra ahora roja, del color de su ruptura),
un test del motor que anota y uno que fija los nombres de las tres anotaciones;
`test_arnes_motor.py`, un motor sintético que anota y el informe que cuenta. El contrato se amplió
con `tests/unit/test_huecos_motor.py` (dicho en §1.f).

### 3.2 Fase 3 · El motor, la spec y el ADR

- **Motor**: `domain/sesgo.py` (docstring; `ResultadoSesgo` con `saltadas_color_contrario`,
  `saltadas_neutras_simples` y `saltadas_neutras_dobles`, 0 por defecto; la ruptura simple decide
  solo con el color de su ruptura, y con color contrario o sin cuerpo la búsqueda sigue),
  `engine/primitivas.py` (`ANOTACION_SALTADAS_COLOR`, `…_NEUTRA_SIMPLE`, `…_NEUTRA_DOBLE`,
  anotadas con el número solo si es mayor que cero) y `engine/arnes.py` (tres líneas más en
  «## RN-003 al abrir la sesion», sesiones y velas por motivo). Los 64 tests de los tres ficheros
  pasan; también `test_cableado.py`, `test_visor.py` y `test_cierre_vela_h4.py` (116 en total en
  esa pasada). `ruff check` y `ruff format` limpios.
- **Spec** (`knowledge/spec/`, trailer `Fuente:` con R1, R2 y ADR-0080): RN-003 (`entonces` con la
  regla; `cita` y `literal` → R1; notas con el párrafo «DESDE EL 2026-10-17 (ADR-0080)» delante,
  con la contradicción abierta y «Con un solo extremo roto, el color de la vela NO decide»
  declarado SUSTITUIDO; lo anterior se conserva como historia); el predicado `sesgo_h4_al_abrir`
  (descripción con el color; `cita` y `literal` → R1; dice que hasta hoy citaba `8eccf5c0`);
  RN-033 (una línea en notas; forma, cita y `cuando` iguales) y el token `insuficiente` (punto 3
  de la respuesta); `equal` (definición con «y cerrar del color de esa ruptura (ADR-0080)», cita
  `8eccf5c0`; punto 2); `sesgo_h4_regla` (solo la descripción; D7). `rompe` no se toca. Ningún
  sitio nuevo con `cita`: las tres guardias de `spec/modelo.py` no cambian. Una trampa medida: el
  `entonces` de una regla no admite cifras (`modelo.py:270`, «contiene la cifra '0'»), así que no
  puede nombrar «ADR-0080»; dice «el ADR del color» y las notas llevan el id.
- `spec_version` 17.0.3 → **18.0.0** (una regla cambia de sentido: mayor, como ADR-0075 subió
  15.9.9 → 16.0.0); `spec manifest --escribir` (hash `e34f5de4…` y después el definitivo del
  commit) y `spec docs --escribir` en el mismo commit.
- **ADR-0080** (`docs/adr/0080-el-sesgo-h4-cambia-solo-si-rompe-y-cierra-del-color-de-la-ruptura.md`):
  D1-D7 con la fecha, la contradicción abierta y A-1 sin reabrir (puntos 0 y 6 de la respuesta),
  el motor y el arnés. Recuadros de enmienda en ADR-0044 (§2, su alternativa descartada y la nota
  de §1 que debía G.2: punto 7), ADR-0060 (§1) y ADR-0075 (§3), y sus filas del índice más la de
  0080.
- `feedback pending` tras el cambio de cita: dos CORRECT sobre RN-003 pendientes
  (`fb-2026-09-29-sesion-03-31fb311f` y ahora `fb-2026-10-04-sesion-04-ca0afae6`, «RN-003 no lo
  cita todavia»): es la deuda G.2 de la hoja (`feedback pending` no admite dos CORRECT vivos sobre
  una regla), no un fallo de esta rama; R1 sale reflejado.
- `knowledge validate` en verde (36 reglas, hash al día); `test_adr`, `test_spec_docs_generados`,
  `test_kit`, `test_hoja_preguntas`, `test_no_business_literals` y `test_cuarentena` en verde.

## 4 · Fase 4 · La re-corrida del arnés con los tres comandos de R3.1 (2026-10-17)

Declarada ANTES de correr en `HOLDOUT-EXPOSICIONES.md` (segunda fila del 2026-10-17: el M1
entero de marzo y de junio para calentar, como R3.1). Los tres comandos de `CORRIDA-CONSTRUCCION.md`
§3.1 tal cual, con la carpeta de `--salida` de esta rama (README de los anexos), uno detrás de
otro, sobre fd5d40d (el commit del motor):

| # | Comando (`uv run botsito motor arnes --simular --diagnostico-a44 sin_tope …`) | Fichero escrito (`docs/validation/anexos/SESGO-H4-COLOR/`) | Tiempo, memoria, exit |
|---|---|---|---|
| 1 | `--diagnostico-a35 cierre_vela_contraria --salida …/arrastrada.txt` | `arrastrada.DIAGNOSTICO.a35=cierre_vela_contraria.a44=sin_tope.txt` | 315,8 s; 630,9 MiB; 0 |
| 2 | `--diagnostico-a35 cierre_vela_contraria --diagnostico-cuenta-diaria --salida …/diaria.txt` | `diaria.DIAGNOSTICO.a35=cierre_vela_contraria.a44=sin_tope.cuenta=diaria.txt` | 278,6 s; 632,7 MiB; 0 |
| 3 | `--diagnostico-a35 inicio_vela_contraria --diagnostico-cuenta-diaria --salida …/a35-inicio.txt` | `a35-inicio.DIAGNOSTICO.a35=inicio_vela_contraria.a44=sin_tope.cuenta=diaria.txt` | 253,4 s; 632,2 MiB; 0 |

Es diagnóstico (ADR-0070 §3), como R3.1: no decide ningún parámetro, no habilita mayo y no se
mide cobertura contra ningún umbral. Ninguna salida ni este informe imprime la fecha ni el precio
de una H4 que fije un sesgo (la única fecha fuera de los meses de construcción en las tres salidas
es la cobertura del calendario de cierres, la misma línea que en R3.1). El clasificador y la
guardia no negaron ningún comando.

### 4.1 En cuántas sesiones cambió el sesgo, y por qué regla

Sección «## RN-003 al abrir la sesion» de las salidas (igual en las tres corridas; el sesgo no
depende de la cuenta ni de A-35), frente a la de R3.1 (sus salidas commiteadas de §4.9; D5):

| | R3.1 (7cf8901) | Esta rama (fd5d40d) |
|---|---|---|
| por sesión (las 104 con operaciones del trader) | alcista 53; bajista 51 | alcista 51; bajista 52; **insuficiente 1** |
| de ellas con doble ruptura, que decide el color (ADR-0060) | 17 | 22 |
| sesiones con alguna H4 saltada por color contrario (D1) | — | **21 (29 velas)** |
| sesiones con alguna H4 saltada por neutra simple (D3) | — | 0 (0 velas) |
| sesiones con alguna H4 saltada por neutra con doble ruptura (ADR-0075) | — | 0 (0 velas) |
| por operación del trader | a favor 150; en contra 48 | a favor 154; en contra 42; insuficiente 2 |
| RN-033 disparada | 0 | 1 de 152 sesiones corridas; 1 de 104 |

**En 8 de las 104 sesiones cambió el sesgo**, todas por D1 (la H4 que antes lo fijaba rompía un
extremo y cerraba del color contrario; ninguna por D3 ni por una neutra doble, que no aparecen en
construcción): 4 de alcista a bajista, 3 de bajista a alcista y 1 de alcista a INSUFICIENTE
(`comparar_rn003.py` del scratchpad, que solo lee las filas `rn003` de las dos salidas; misma salida
sobre las corridas 1 y 2). Por día dev de construcción y sesión (son días de desarrollo; ninguna
H4):

```
2026-01-02 07-11: alcista -> insuficiente (trader 2, bot antes 2, ahora 0)
2026-01-07 07-11: alcista -> bajista     (trader 1, bot antes 0, ahora 1)
2026-01-16 07-11: alcista -> bajista     (trader 1, bot antes 0, ahora 0)
2026-01-23 07-11: bajista -> alcista     (trader 3, bot antes 0, ahora 2)
2026-01-28 07-11: bajista -> alcista     (trader 1, bot antes 1, ahora 2)
2026-01-30 11-15: alcista -> bajista     (trader 2, bot antes 1, ahora 1)
2026-08-04 11-15: alcista -> bajista     (trader 1, bot antes 0, ahora 0)
2026-08-07 11-15: bajista -> alcista     (trader 3, bot antes 0, ahora 0)
```

Seis de las ocho (2026-01-07 07-11, 01-16 07-11, 01-23 07-11, 01-28 07-11, 01-30 11-15 y 08-04
11-15) están entre las 13 sesiones de P1 «con ruptura solo de mecha» que R3.1 dejó para la
pregunta 1 de la sesión 5 (`CORRIDA-CONSTRUCCION.md` §4.4); las otras dos no eran P1. Las 21
sesiones con alguna saltada son más que las 8 que cambian porque en 13 la búsqueda, tras saltar,
vuelve a dar el mismo lado (otra H4 anterior, a veces una doble ruptura: por eso suben de 17 a 22).
**Pasan a INSUFICIENTE: 1** (2026-01-02 07-11; RN-033 prohíbe, y el bot deja de hacer sus 2
operaciones de esa sesión).

### 4.2 Las cifras de cabecera y la tabla por operación

| | R3.1 · corrida 1 | rama · corrida 1 | R3.1 · corrida 2 | rama · corrida 2 | R3.1 · corrida 3 | rama · corrida 3 |
|---|---|---|---|---|---|---|
| cobertura | 1/198 (0,5 %) | 1/198 (0,5 %) | 12/198 (6,1 %) | 12/198 (6,1 %) | 12/198 (6,1 %) | 12/198 (6,1 %) |
| precisión | 1/38 (2,6 %) | 1/32 (3,1 %) | 12/94 (12,8 %) | 12/94 (12,8 %) | 12/94 (12,8 %) | 12/94 (12,8 %) |
| sesiones con operación del bot (de 104) | 19 | 19 | 51 | 53 | 51 | 53 |

Resumen por mes de la corrida 2 (`### Resumen por mes`): solo cambian agosto (bot puntuables 21 →
22, precisión 2/21 → 2/22) y enero (37 → 36, 1/37 → 1/36); abril y julio, iguales. La corrida 3
frente a la 2 de esta rama, con `comparar_corridas.py` de R3.1: **0 sesiones con alguna
diferencia** (operaciones del bot 106 y 106, parejas 12 y 12), lo mismo que R3.1 midió entre sus
corridas 2 y 3.

La corrida 2 de R3.1 frente a la de esta rama, con el mismo guion
(`anexos/SESGO-H4-COLOR/comparar_corridas.txt`; en su pie A es la de R3.1 y B la de esta rama,
los dos ficheros se llaman igual): **7 sesiones con alguna diferencia** en las operaciones del bot
(2026-01-02 07-11, 01-07 07-11, 01-22 07-11, 01-23 07-11, 01-28 07-11, 01-30 11-15 y 08-04
11-15), 106 operaciones del bot en las dos, 12 parejas en las dos. Siete de las ocho sesiones de
§4.1 menos 01-16 07-11 y 08-07 11-15 (donde el bot no operaba ni opera), más 2026-01-22 07-11, una
sesión sin operaciones del trader cuyo sesgo cambió y donde el bot deja de hacer tres compras.

### 4.3 La tabla T0 y P1-P7, con `patrones.py` de R3.1

`uv run python docs/validation/anexos/CORRIDA-CONSTRUCCION/patrones.py <corrida 2 de esta rama>
--filas` (el guion no se copia ni se toca; lee la ruta por argumento), salida completa en
`anexos/SESGO-H4-COLOR/patrones.txt` (292 filas, 104 sesiones con rn003, como R3.1):

| mes | P1 sesgo | P2 entrada | P3 otra zona | P4 sin orden | P5 de más | P6 trader no operó | P7 repetidas | T0 pareja |
|---|---|---|---|---|---|---|---|---|
| 2026-01 | 7 (13) | 9 (9) | 22 (17) | 15 (14) | 30 (28) | 5 (8) | 0 (0) | 1 (1) |
| 2026-04 | 9 (9) | 2 (2) | 8 (8) | 12 (12) | 11 (11) | 16 (16) | 0 (0) | 4 (4) |
| 2026-07 | 20 (20) | 3 (3) | 13 (13) | 23 (23) | 9 (9) | 2 (2) | 3 (3) | 5 (5) |
| 2026-08 | 8 (6) | 4 (4) | 5 (4) | 23 (26) | 14 (13) | 7 (7) | 0 (0) | 2 (2) |
| **total** | **44 (48)** | 18 (18) | **48 (42)** | **73 (75)** | **64 (61)** | **30 (33)** | 3 (3) | 12 (12) |

(entre paréntesis, R3.1, `anexos/CORRIDA-CONSTRUCCION/patrones.txt`). P1 pasa de 48 filas en 25
sesiones a **44 filas en 21 sesiones** (alcista 14, bajista 28, insuficiente 2; antes 16 y 32);
P5 «de más, mismo lado» 52 (47) y «otro lado» 12 (14); P6 en día 12 (12) y en sesión 18 (21). Las
parejas (T0) no cambian: la regla del sesgo no acerca ninguna entrada al trader, mueve filas de P1
a P3/P5 (el bot opera en el lado del trader pero en otra zona) y de P4/P6 a P5. Filas marcadas
«posible M», 16 (16).

### 4.4 Para el cuestionario de la sesión 5

En el orden del consultor, para V (R4.1); sustituyen a la pregunta 1 de
`CORRIDA-CONSTRUCCION.md` §4.5, que el WhatsApp respondió. Sin fechas de días reservados ni
resultados de holdout; las dos se preguntan con un esquema dibujado, nunca con los fotogramas de
v6 ni con los instantes de ese gráfico (respuesta del consultor, puntos 0 y 0bis):

1. **La ruptura simple sin cuerpo (D3, decisión del consultor en ADR-0080 §4):** una H4 rompe el
   extremo de la anterior (con la mecha) y cierra exactamente donde abrió. ¿Cambia el sesgo por el
   lado de la ruptura, o no decide y sigue el sesgo que había (como la neutra de doble ruptura de
   S-13)? Hoy el motor hace lo segundo. En construcción no aparece ninguna (§4.1).
2. **La contradicción con la sesión 1 (ADR-0080 §9):** con el sesgo bajista, una H4 rompe por
   encima con la mecha y cierra ROJA. En la sesión 1 dijo «la siguiente operativa es alcista …
   aunque fue roja la vela, pues es indiferente»; en el WhatsApp del 2026-10-14 confirmó el caso 3
   del esquema (no cambia, sigue bajista). ¿Cuál vale? Si es la del WhatsApp, ¿qué era distinto en
   el caso que explicó en la sesión 1? (sobre un esquema de dos velas dibujado; hoy el motor hace
   lo del WhatsApp).

## 5 · Líneas preparadas para el commit del contrato de la orden de cierre

Medidas en memoria con `anexos/SESGO-H4-COLOR/simular_cierre.py` (como `trabajo/entrada-enero`;
lee `PROJECT_STATE.md`, la hoja y HISTORIA, aplica las sustituciones y corre a, b y c de
`test_hoja_de_ruta.py`); salida en `simular_cierre.txt`: `a: []`, `b: []`, `c: []`,
`PROJECT_STATE hoy: 24568 bytes`, `PROJECT_STATE simulado: 23250 bytes`. En la rama no se tocan
(solo `Tests Currently Passing`, 1556 → 1570, por `state check`).

### 5.1 `PROJECT_STATE.md`

- **W sale entera** de la Next Action a `docs/state/HISTORIA.md` con su texto literal, bajo el
  título `# Next Action HECHA · W · el sesgo de H4 por el color · sale de PROJECT_STATE.md en
  trabajo/sesgo-h4-color (2026-10-17)` (distinto del `… · W · sale de PROJECT_STATE.md en
  trabajo/cases-rejilla (2026-10-10)` de HISTORIA:7638; el test solo exige el prefijo
  `# Next Action HECHA · W ·`, `test_hoja_de_ruta.py:61`, y acepta letras repetidas: E está en
  :5881 y :8656), seguido de «La hace `trabajo/sesgo-h4-color` (docs/validation/SESGO-H4-COLOR.md,
  ADR-0080).»
- **F queda:** «F. E → O → V. La re-corrida de R3.1 con el sesgo nuevo ya está hecha
  (SESGO-H4-COLOR.md §4); si E cambia lo que simula, su encargo decide si hace falta otra.» (el
  texto del encargo, con «tras el sesgo la hizo W» reescrito: «tras» + «W» rompía el test c,
  §1.k).
- **V deja de nombrar W:** «… de CORRIDA-CONSTRUCCION.md §4.5 con su pregunta 1 sustituida por las
  dos de SESGO-H4-COLOR.md §4.4 (la ruptura simple sin cuerpo, D3 de ADR-0080, y la contradicción
  con la sesión 1, con un esquema dibujado), en su orden. Depende de R1.1, de R3.1, de E y O, de J
  (kit hoja) y de la copia de seguridad (A.4).»
- Tamaño que resulta: **23.250 bytes** (hoy 24.568; en `main`, 24.359): baja del de hoy, como pide
  el encargo. El commit de estado del cierre añade lo suyo sobre esa base.

### 5.2 `docs/plan/HOJA-DE-RUTA.md`

- **R1.2** gana `ID:ADR-0080` en sus Refs y la línea «**Estado:** HECHA (`trabajo/sesgo-h4-color`,
  `stable/F37r-sesgo-h4-color`; SESGO-H4-COLOR.md, ADR-0080): la regla del color en la spec y en
  el motor, dos registros de feedback, el arnés vuelto a correr con los tres comandos de R3.1
  (§4). La contradicción con la sesión 1 y la ruptura simple sin cuerpo van a la sesión 5 (R4.1).»
  (el tag es el siguiente libre tras `F37q`; si el cierre le da otro nombre, se cambia ahí).
- **R4.1**: en :167, `NA:W` sale de las Refs; en :176, «sin su pregunta 1 (el sesgo, respondida:
  R1.2)» pasa a «con su pregunta 1 sustituida por las dos de SESGO-H4-COLOR.md §4.4 (la ruptura
  simple sin cuerpo y la contradicción con la sesión 1; R1.2)»; en :178, «R1.2 (NA:W)» pasa a
  «R1.2 (HECHA)».

### 5.3 Para `ERRORES-RECURRENTES.md` (la escribe `cerrar-rama`) y para el cierre

- Hallazgo para el cierre, no para la rama (respuesta del consultor, 0bis): antes de abrir un
  fotograma de un gráfico EN DIRECTO, se mira qué días enseña por la fecha de grabación del vídeo
  y se comprueba con `casos_reservados` si alguno es reservado (§1.j: los tres fotogramas de v6
  enseñaban cuatro días de `fidelidad-1`).
- Lo que el auditor del encargo vio antes de empezar (§1.h): la línea F propuesta rompía el test c
  de la hoja; la fase 1 ya cambiaba el hash de la spec; `--check` no aplica; v9 sí está en
  cuarentena; el índice de ADR no estaba en el contrato.

## 6 · Desviaciones declaradas

1. **El contrato se amplió dos veces** en la rama: `docs/adr/README.md` (fase 0, §1.k) y
   `tests/unit/test_huecos_motor.py` (fase 2, §3.1). Las dos están dichas en el commit que las
   trae.
2. **La fase 1 subió `spec_version` (17.0.3) y regeneró manifest y docs**, que el encargo dejaba
   para la fase 3: `feedback apply` cambia la fuente de un parámetro y el hash de la spec la cubre
   (auditor, punto 3; aceptado por el consultor). La fase 3 la subió otra vez (18.0.0).
3. **`feedback apply` se ejecutó sin `--check` después del `--check`**: el encargo decía «aplicado
   con feedback apply --check», que no escribe (auditor, #25; aceptado).
4. **La fase 1 quedó en dos commits**: 0365d5c (registros, apply, spec, `fuentes.yaml`, README de
   anexos) y el del inventario, que espera a los `mv` de Aleks; las fases 2 y 3 (fd5d40d) y la 4
   no esperaron a él porque no dependen del inventario.
5. **El punto 0 de la respuesta se quedó en su opción (b)** -sin ítems de evidencia- porque
   supersedir `ev-v3-011045` rompe G1 en A-1 (medido, §2.1), como la propia respuesta preveía.
6. **Los siete tests de 4.b**: el primero no se «rehízo» con el mismo nombre: pasó a
   `test_rompe_arriba_y_cierra_verde_es_alcista` y su vela roja es ahora el caso 3 (§3.1); los
   otros seis conservan nombre y asserts, con el color explícito.
7. **El escenario `abajo` de `test_huecos_motor.py` cierra ahora roja** (del color de su ruptura),
   para que siga significando «rompe abajo y decide»; sus tests anteriores no cambiaron de
   resultado.
8. **`entonces` de RN-003 no puede nombrar «ADR-0080»** (la guardia de cifras, `spec/modelo.py:270`):
   dice «el ADR del color» y las notas llevan el id.
9. **El informe nombra dos ids sintéticos** de una medida en memoria (§2.1), declarados en su bloque
   `ids-inexistentes`; ADR-0080 estuvo declarado en el informe y en el encargo hasta que existió.
10. **`sesgo_h4_diagnostico.py`, `sesgo_p1.py` y `sesgo_2x2.py` no se corrieron** con el motor nuevo
    (§1.k): el encargo no lo pedía y cada uno lee el M1 de marzo o de junio para calentar. Sus
    salidas cerradas no dicen lo que daría el motor de hoy (p. ej. `sesgo_p1.txt` «ninguna
    neutra saltada» y «6 de doble ruptura» son del motor de R3.1).

## 7 · El encargo, punto por punto

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 0.1 | Base 59c8ae7 verificada con git, origin, tag; ninguna otra rama | Hecho | §0 |
| 0.2 | CI de main con `gh`, nunca curl ni guion | Hecho | §0, `gh run view 38656985715` |
| 0.3 | Apertura con `abrir-rama`: encargo, contrato, Archivo 34, tramo R1 | Hecho | c24c50b |
| 0.4 | Informe y anexos en sus rutas | Hecho | este fichero; `anexos/SESGO-H4-COLOR/` |
| 0.5 | Skills: fase-cero con auditor-encargo; activar-sesion; entregar-rama | Hecho | §1 (auditor en §1.h), §2-§3, §8-§9 |
| 1 | La regla del WhatsApp en la spec y en el motor, con ADR, feedback y evidencia, y re-corrida | Hecho | fd5d40d, 0365d5c, §4; la evidencia entra como capturas en el corpus (inventario pendiente de los `mv`) |
| D1 | Color contrario: no decide, la búsqueda sigue | Hecho | `domain/sesgo.py`; ADR-0080 §2; tests caso 3 y 4 |
| D2 | Doble ruptura sin cambios | Hecho | `test_la_doble_ruptura_no_cambia_con_la_regla_nueva`; ADR-0080 §3 |
| D3 | Neutra simple: no decide; decisión del consultor; pregunta a la sesión 5 | Hecho | ADR-0080 §4; §4.4 |
| D4 | `sesgo_h4_criterio_ruptura` = mecha, CONFIRMED, con 41f46b21, ev-v9-001312 (y ev-v9-000902) verificados; la lección de ERRORES-RECURRENTES:84 | Hecho | §1.c; ADR-0080 §5; fuente R2 |
| D5 | Ni parámetro ni interruptor; comparación contra las salidas de R3.1 | Hecho | §4; ADR-0080 §6 |
| D6 | ADR-0080 (siguiente libre, verificado); recuadros en 0044 §2 (y nota de §1), 0060 §1, 0075 §3; ningún otro ADR contradice | Hecho | §1.a; `docs/adr/0080-*.md`, README |
| D7 | Dos registros, ninguno supersede 8eccf5c0; CORRECT RN-003 y CONFIRM mecha aplicado; procedencia, medio, recibido_el; carpeta propuesta en la PARADA; `sesgo_h4_regla` solo descripción | Hecho | §2.2; decisión 1 de la PARADA → (a) |
| 3.1 | Ningún otro parámetro ni cifra; tope 60 | Hecho | `git diff main -- knowledge/spec/parametros.yaml`: solo la fuente de `sesgo_h4_criterio_ruptura` y la descripción de `sesgo_h4_regla` |
| 3.2 | Simulador, cuenta, bróker y arnés intactos salvo 4.f | Hecho | `git diff main --name-only`: de `src/` solo `domain/sesgo.py`, `engine/primitivas.py`, `engine/arnes.py` |
| 3.3 | Anexos e informes cerrados no se editan | Hecho | ninguno en el diff; guiones cerrados no corridos (§6.10) |
| 3.4 | Guardias, `.claude/` y Makefile intactos | Hecho | no están en el diff |
| 3.5 | PROJECT_STATE: solo lo del ritual, no engorda | Hecho de otra forma | 24.359 → 24.568 bytes por `Tests Currently Passing` (1556 → 1570, lo exige `state check`); el cierre lo deja en 23.250 (§5) |
| 4.a-g | Fase 0 completa y PARADA | Hecho | §1 |
| 4.b | Los siete tests verificados y rehechos sin rebajar | Hecho | §1.b, §3.1, §6.6 |
| 4.c | Evidencias leídas; contradicción → PARADA, detector y sesión 5 | Hecho | §1.c; punto 0 de la respuesta; §2.1 (detector: (b), medido) |
| 4.e | Seis ficheros listados con sha256; `mv` preparados; nota de voz dicha | Hecho | §1.e; corregido en §1.m (está arriba de la captura de las 15:18) |
| 4.f | Campo nuevo en `ResultadoSesgo` y anotación; el arnés cuenta | Hecho | tres campos y tres anotaciones (punto 4 de la respuesta, (b)) |
| 4.g | Lectura declarada el mismo día y antes de correr | Hecho | HOLDOUT-EXPOSICIONES, segunda fila del 2026-10-17 |
| F1 | Tras los `mv`: inventory, `fuentes.yaml`, manifest; registros con `feedback new`, `apply --check`, `knowledge validate` | Parcial | todo hecho (0365d5c) salvo `corpus inventory` y `manifest.yaml`, que esperan a los `mv` de Aleks |
| F2 | Tests primero, en rojo sobre `main`, con el recuento de FAILED; la lista del encargo; los siete rehechos | Hecho | §3.1: 16 FAILED |
| F3 | Motor, spec, ADR, `spec_version`, manifest y docs en el mismo commit, guardias si hay sitio nuevo, `Fuente:` | Hecho | fd5d40d; sin sitio nuevo con cita |
| F4 | Fila de HOLDOUT antes; los tres comandos tal cual; comparación con R3.1 (sesiones, regla, INSUFICIENTE, T0 y P1-P7 con `patrones.py`); sin fecha ni precio de la H4; diagnóstico | Hecho | §4 |
| 6.1 | Informe con encargo punto por punto, desviaciones, salidas de la fase 4 y la lista de la sesión 5 con D3 | Hecho | §4.4, §6, §7 |
| 6.2 | Líneas del cierre medidas en bytes (W, F, V, hoja, tamaño) | Hecho | §5 |
| 6.3 | CI de Linux si toca la plataforma; si no, el diff de nombres | Hecho | §8 |
| 6.4 | Revisor (opus) con dos alcances; que ninguna consulta de CI fuera con curl o guion | Hecho | §9 |
| R0 | Respuesta del consultor copiada tal cual y aplicada punto por punto | Hecho | §1.l; puntos 0-7 y «Además» en §2-§5 |

## 8 · CI de Linux

No se empuja `fix/sesgo-h4-color`: la rama no toca hooks, rutas, el sistema de archivos ni guiones
que dependan de la plataforma (`RITUAL.md`, «Antes del merge: la CI de Linux»). El diff de nombres
contra `main` (`git diff main --name-only`, más los ficheros de la fase 4): `PROJECT_STATE.md`,
`contrato.yaml`, `docs/adr/{0044,0060,0075,0080}-*.md`, `docs/adr/README.md`,
`docs/encargos/trabajo-sesgo-h4-color.md`, `docs/spec/*.md`, `docs/state/HISTORIA.md`,
`docs/validation/HOLDOUT-EXPOSICIONES.md`, `docs/validation/SESGO-H4-COLOR.md`,
`docs/validation/anexos/SESGO-H4-COLOR/*`, `knowledge/corpus/fuentes.yaml`,
`knowledge/feedback/2026-10-04-sesion-04/fb-…-{6e7da456,d2e84172}.yaml`,
`knowledge/spec/{glossary,parametros,spec_manifest,strategy_spec}.yaml`,
`src/botsito/domain/sesgo.py`, `src/botsito/engine/{primitivas,arnes}.py`,
`tests/unit/test_{sesgo_h4,huecos_motor,arnes_motor}.py`. Nada de `scripts/git-hooks/`,
`.claude/hooks/`, rutas del sistema de archivos ni zoneinfo; `simular_cierre.py` lee tres ficheros
por `Path` relativo a la raíz que recibe.

## Estado

EN CURSO. Fases 0 a 4 hechas; falta el commit del inventario (tras los `mv`), el revisor y su
respuesta.
