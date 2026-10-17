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

Este informe nombra el ADR nuevo antes de que exista (entra en la fase 3), y la guardia de ids
citados de `knowledge validate` lo exige declarado:

```ids-inexistentes
ADR-0080 — el ADR de esta rama (D6 del encargo), que se escribe en la fase 3; hasta entonces se cita aquí como el siguiente libre
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

## Estado

EN CURSO. Fase 0 entregada; PARADA a la espera de la respuesta del consultor.
