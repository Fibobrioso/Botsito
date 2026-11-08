# CUENTA-POR-MES · la cuenta del motor, una por mes (ADR-0092 §8)

Rama `trabajo/cuenta-por-mes`, abierta el 2026-11-07 desde `main` 8aeed0b
(tag `stable/F38r-metodo-fidelidad-rentabilidad`, merge a1907fa). Encargo:
`docs/encargos/trabajo-cuenta-por-mes.md`. Tramo «R3 · Una corrida del arnés sobre toda la
construcción» (R3.8 de la hoja de ruta; F de la Next Action).

## 0. La base, comprobada con git al abrir

- `git rev-parse HEAD` en main = `8aeed0b336c0e80ab1d7124096f04880e569ede7`; `origin/main` el mismo
  (`git fetch origin --prune`; `git ls-remote --heads origin` solo da `refs/heads/main`).
- `git rev-parse "stable/F38r-metodo-fidelidad-rentabilidad^{commit}"` =
  `a1907fa3d0dead56bc109cea6f680841c8e629cc` = `git rev-parse main^1`; el tag esta en origin
  (`git ls-remote --tags origin`, objeto 4323f6b).
- `gh run view 42440794180 --json headSha,conclusion,status,workflowName,headBranch`:
  `{"conclusion":"success","headBranch":"main","headSha":"8aeed0b336c0e80ab1d7124096f04880e569ede7","status":"completed","workflowName":"ci"}`.
- `git branch -a`: solo `main` y `origin/main`; `git ls-remote --heads origin "fix/*"` vacio.
- Modelo: Opus 5.5, el que pide el encargo.

## Fase 0 · inventario sin tocar código (2026-11-07)

Medido leyendo el código de la rama recién abierta (idéntico a `main` en `src/`, `scripts/` y
`tests/`) y contrastado por el subagente `auditor-encargo` (53 afirmaciones: 36 cuadran, 14 con
matiz, 3 no cuadran; sus hallazgos, en e) y en la PARADA condicional). Ninguna corrida del arnés.

### a) El estado que `MotorCableado` guarda entre días, y el orden de los días

| Estado | Dónde vive | Dónde se reinicia hoy |
|---|---|---|
| `cuenta` (`CuentaViva`) | `cableado.py:243` | nace en `correr_dia` si es `None` (`:278-279`); con `cuenta_diaria`, a `None` cada día (`:276-277`) |
| `seguidor` (`SeguidorTope`, A-44) | `:244` | nace si hay `tope` y es `None` (`:294-297`); con `cuenta_diaria`, cada día (`:277`) |
| `racha` (`SeguidorRacha`, RN-036) | `:247` | nace si es `None` (`:280-281`); con `cuenta_diaria`, cada día (`:277`) |
| `primero_en_tocar` | `:249` | nunca: `_anotar_toque` vuelve en cuanto tiene valor (`:413-414`), también con `cuenta_diaria` |
| `trazas_broker`, `brokers`, `estados` | `:250-252` | por clave de día; solo salida (los leen el informe y el visor) |

El bróker (`Broker(...)`, `:283`), el `ContextoDia` (`:303`) y el estado de estrategia
(`EstadoDia()`, `:316`) nacen cada día: D1 cuadra en que no hay nada más que reiniciar. El freno de
peticiones vive en el bróker (`reglas_broker.freno` es configuración).

El orden: `arnes.validar_meses` ordena y deduplica los meses (`arnes.py:121`);
`arnes.dias_de_construccion` recorre `for mes in meses` y dentro del mes los casos por id
(`arnes.py:151-172`, `sorted(c ...)` en `:158`); `arnes.correr` es una comprensión plana sobre esos
días (`arnes.py:238`), que no agrupa por sí misma: el agrupado viene de `dias_de_construccion`. Así
un mes nunca queda partido. El visor con `--todos` usa la misma función (`Preparador.dias`,
`visor.py:281-282`) y llama a `correr_dia` día a día (`visor.py:325`). `cli.py` solo ordena la
etiqueta `Corrida.meses`.

### b) Los consumidores y los textos de D7, uno por uno

| Consumidor | Qué lee hoy | Con varias cuentas |
|---|---|---|
| `curva_de_equity` (`cableado.py:561-572`) | `motor.cuenta.cerrar_dia_en_curso()`, filtrada por `trazas_broker` | daría solo la curva del último mes: cada cuenta cerrada guarda la suya (D3) |
| `MotorCableado.veredicto` (`:512-515`) | `motor.cuenta` | el veredicto del último mes; los de los cerrados, en D3 |
| `_primero_en_tocar` (`:749-753`) | `motor.primero_en_tocar` | el del último mes; los demás, en D3 |
| `informe_simulacion` (`:756-828`) | todo lo anterior y `motor.racha` | D4: con un mes igual; con varios, bloques por mes |
| `_informe_metodo` (`:1310-1407`) | `curva_de_equity` y `motor.cuenta.estado` (`:1365-1366`) | D5 |
| el visor (`detalle_para_visor`, `:743-744`; `visor.py:145-146`, `:949-950`) | `TrazaBroker.saldo_fin` y `equity_fin`, por día | no cambia; el primer día de un mes nuevo trae el saldo de la cuenta nueva |
| `scripts/embudo_77.py:905` | rótulo literal «cuenta arrastrada entre dias (ADR-0053 §6)» | deja de ser cierto: se cambia (D7) |
| `scripts/f35_resultado_r.py:81` | rótulo «arrastrada entre dias», sin «cuenta» ni ADR; NO construye el motor: lee el JSON de `embudo_77` (`:70-74`) | se cambia igual, para que describa el JSON que escribe `embudo_77` desde esta rama |
| `scripts/orden_stop_o_limite.py:431`, `scripts/caja_77_exploratoria.py:146` | construyen el motor y corren `arnes.correr` sobre varios meses (`:435`, `:150`); NO llevan ningún rótulo de la cuenta | nada que cambiar en el texto; si se vuelven a correr, sus decisiones entre meses cambian (dentro de un mes, no) |
| `cli.py:2324-2326` | ayuda de `--diagnostico-cuenta-diaria`: «en vez de arrastrarse (ADR-0053 §6)» | se reescribe |
| `diagnostico.py:35-37` | «la corrida normal arrastra la cuenta entre dias (ADR-0053 §6)» | se reescribe |
| comentarios de `MotorCableado` (`cableado.py:240-241`, `:245-246`, `:248`) | «por defecto se arrastra, ADR-0053 §6», «persiste entre dias», «en toda la corrida» | se reescriben. `:139`, `:192` (`MOTIVO_FIN_DIA`, que se imprime) y `:382` citan ADR-0053 §6 por la red de seguridad del fin del día, que sigue cierta: no se tocan |
| `racha.py:1-3` | «PERSISTE entre dias como la cuenta (ADR-0053 §6)» | fuera de las rutas del encargo: PARADA condicional, punto 1 |

### c) Los tests que corren días con el motor cableado

Medido con un espía de `MotorCableado.correr_dia` que anota los meses de cada motor y lanza
`pytest tests/unit` (guion y salida en `anexos/CUENTA-POR-MES/medir_meses.py` y
`meses-fase0.txt`; la primera forma, un plugin por `PYTHONPATH`, la negó la guardia por la
variable de entorno, y se rehízo sin ella): **89 tests corren el motor cableado, 0 motores corren
más de un mes**, y los meses vistos son `2030-01` (los sintéticos) y `2026-04` (un motor de un
solo mes; ningún test de esta rama ni ninguna corrida del arnés). Los que corren VARIOS días en
el mismo motor son todos de enero de 2030: `test_cableado.py:713-723` y `:766-774` (días 15 y 21),
`test_racha_perdidas.py:375-390` (15 a 28) y `test_reinicio_tope_trader.py:190-198` (15 y 16).
Ninguno corre más de un mes: ninguno de los seis de D7 se cambia.

Los que asertan la cabecera: PRIMERO EN TOCAR, `test_preparar_a44.py:371` y `:398`; TOPE, `:349`;
RACHA, `test_racha_perdidas.py:411`; «CUENTA: REINICIADA CADA DIA», `test_cableado.py:778`; la
cabecera y la curva enteras, por el prefijo del golden de e01e28c, `test_metodo_adr0092.py:370-383`
(compara hasta `CABECERA_METODO`: la sección de ADR-0092 no tiene golden).

### d) D1-D8 frente a lo medido

- D1: cuadra para la cuenta, el seguidor del tope y el primero en tocar. **No cuadra para la
  racha** (PARADA condicional, punto 1).
- D2, D3, D4: cuadran. D4: el golden existente cubre la cabecera, la curva y los eventos, no la
  sección de ADR-0092 (la cubre la guardia nueva de D5).
- D5: cuadra, con tres medidas. (i) `perdida_diaria_maxima` y `equity_minima_del_tramo` son un
  máximo y un mínimo POR DÍA (`criterio_fidelidad.py:657-675`), así que por cuenta salen la misma
  cifra que sobre la curva de todos los días seguidos: lo nuevo es decir de qué mes, y no cambia
  ninguna cifra. (ii) La guardia nueva no protege nada con el `_motor` de los tests, que no lleva
  `criterio`: la sección solo dice «sin el criterio de ADR-0092» (`cableado.py:1320-1327`). El
  golden se genera con el criterio REAL (`cargar_criterio`) puesto en el motor, para que salgan a)
  a f), en una carpeta nueva `tests/golden/metodo_adr0092/` (la de `informe_simulacion/` está
  protegida por el contrato). Y (iii) reescribir el motivo de f) sin condición choca con «con un
  solo mes, igual que hoy»: PARADA condicional, punto 2.
- D6: cuadra. D7: cuadra con los matices de b) (los guiones). D8: cuadra; el recuadro de ADR-0070
  punto 3 queda en futuro (PARADA condicional, punto 3).

### e) El encargo frente al repo (auditor-encargo)

Lo que no cuadra o cuadra con matiz, y gana el repo:
1. «los guiones que construyen el motor cableado (embudo_77, f35_resultado_r, orden_stop_o_limite,
   caja_77_exploratoria)»: `f35_resultado_r.py` no lo construye; el rótulo literal solo está en
   `embudo_77.py:905`; los otros dos no llevan rótulo (b).
2. «el bucle de arnes.correr agrupa por mes»: agrupa `dias_de_construccion`; `correr` es plano (a).
3. METODO-FIDELIDAD-RENTABILIDAD.md §0.c cita líneas anteriores a los commits de F38r
   (`cableado.py:219-228` hoy es `:240-249`, `arnes.py:226-234` hoy es `:231-239`).
4. ADR-0049 dice que la cuenta persiste en DOS sitios (`:132`, H6, y `:178`, H6 (c)): la NOTA va
   tras el primero, que es la decisión.
5. «22.764 bytes» cuadra en `main`; en la rama ya son 22.675. El tope del repo es 25.000
   (`tests/unit/test_project_state.py:21`); los 23.000 son el margen de los encargos.
6. La «lección 8 de F38r» está en `docs/runbooks/ERRORES-RECURRENTES.md:112`, trampa (8), no en el
   informe de F38r.
7. Al marcar R3.8 HECHA, su `Refs` pierde `NA:F` (F sigue viva): si no, `test_hoja_de_ruta.py:144-145`
   falla con «esta HECHA y la letra sigue viva». Va en las líneas del cierre.
8. `curva_con_deslizamiento` y `veredicto_con_f17` toman una sola curva y su `previo` se arrastraría
   entre cuentas. Hoy no tienen llamadores (solo los tests); cuando F17 los use, irán por cuenta.
   Anotado como deuda, sin tocarlos.
9. D5 no nombra la tabla de posiciones, el material sin vídeo ni el punto de equilibrio de la
   sección: quedan como hoy, sobre todas las operaciones.

**Lo que se aplica sin esperar**, porque cuadra con lo medido: D1 para la cuenta, el seguidor del
tope y el primero en tocar; D2, D3, D4, D5 (con el golden en carpeta nueva y con el criterio real),
D6, D7 (con los guiones como dice b) y D8. Sigo con la fase 1 sin esperar respuesta, como pide el
encargo.

### PARADA condicional (solo en esto; lo demás se aplica)

1. **La racha de RN-036 al cambiar de mes.** D1 la reinicia, pero la descripción del acumulador en
   la spec dice «contando en TODOS los dias de la corrida … el calendario no la reinicia»
   (`knowledge/spec/strategy_spec.yaml:847-853`, protegido por el encargo), el trader dijo «la
   racha sigue de un día a otro y una semana otra» (`parametros.yaml:1416-1426`) y ADR-0077 §3 la
   ata a la cuenta «PERSISTE entre días como la cuenta» (`:46-49`), igual que `racha.py:1-3`
   (fuera de las rutas). ADR-0092 §8 solo habla de «la cuenta». **Aplicado mientras tanto: la racha
   NO se reinicia al cambiar de mes** (lo de hoy); la cuenta, el seguidor y el primero en tocar,
   sí. **Propuesta:** aplicar D1 entero, porque ADR-0077 §3 la hace vivir «como la cuenta» y en
   vivo la cuenta nunca salta de enero a abril; eso pide, en el mismo commit, una NOTA en ADR-0077
   §3, el texto de `racha_perdidas` en la spec con `botsito spec docs --escribir` y su trailer
   `Fuente: ADR-0092`, y el docstring de `racha.py`, con las tres rutas en el contrato. Es una
   línea en `correr_dia` y un test que ya está escrito (D6 (2), la parte de la racha, marcado
   `xfail` estricto hasta la respuesta).
2. **El motivo de f).** D5 lo reescribe a «alguna cuenta entro en SUSPENDIDA», y D4/D5 piden que
   con un mes todo sea igual que hoy. Con un mes y la cuenta SUSPENDIDA, si N llega al mínimo, la
   línea «criterios a) a f)» cambiaría (el golden sintético no lo ve: N=1 da «insuficiente»).
   **Aplicado:** el motivo dice «la cuenta entro en SUSPENDIDA» con una cuenta y «alguna cuenta
   entro en SUSPENDIDA (AAAA-MM, ...)» con varias. **Propuesta:** dejarlo así; o, si se quiere el
   texto nuevo siempre, es un cambio de una línea y se dice que con un mes cambia.
3. **ADR-0070 punto 3.** Su recuadro y su fila del índice dicen «La implementa
   `trabajo/cuenta-por-mes`», en futuro; D8 solo marca «Implementado» en ADR-0053 y ADR-0070 no está
   en las rutas. **No tocado. Propuesta:** la misma coletilla «Implementado en
   trabajo/cuenta-por-mes (2026-11-07)» al final de su recuadro, en esta rama o en el cierre.

## Fase 1

### Punto 1 · Los textos de D8

- ADR-0092 §8: una NOTA (2026-11-07) con la lista de lo que empieza de nuevo al cambiar de mes, la
  condición, el porqué, la diaria intacta y la medida de §5 sin existir todavía. La racha va en la
  NOTA como PENDIENTE de la PARADA condicional, punto 1: la NOTA dice lo que hace el código.
- `docs/adr/README.md`: la fila de 0092 nombra la NOTA.
- ADR-0053 §6: el recuadro gana al final «Implementado en `trabajo/cuenta-por-mes` (2026-11-07; …)».
- ADR-0050 H6 (§2) y ADR-0049 H6: una NOTA de una línea cada uno, que remite a ADR-0092 §8. En
  ADR-0049 va tras el párrafo de la decisión de H6 (`:132-136`); el resumen de alternativas
  (`:178`) no se toca.
- Ningún cuerpo reescrito. ADR-0070 punto 3, sin tocar (PARADA condicional, punto 3).

### Punto 2 · El motor: la condición, el reinicio y la conservación (D1, D2, D3; D6 (1)-(4) y (6))

- `MotorCableado` gana dos atributos de estado interno (D2): `mes_en_curso`, el AAAA-MM de la
  clave del último día corrido, y `cuentas_cerradas`, la lista ordenada de `CuentaDelMes` (D3: mes,
  estado, motivo, instante, saldo, equity, días de trading, primer toque, la racha al cierre y la
  curva). En `correr_dia`, justo donde ya se reiniciaba la diaria: con `cuenta_diaria`, lo de hoy y
  nada más; si no, cuando el mes del día es distinto de `mes_en_curso`, la cuenta en curso se
  fotografía en `cuentas_cerradas` y `cuenta`, `seguidor` y `primero_en_tocar` vuelven a `None`
  (nacen de nuevo unas líneas más abajo, por el mismo código de siempre: la cuenta desde el capital
  del perfil). **La racha no se toca** (PARADA condicional, punto 1). Ninguna opción ni campo de
  configuración nuevo; `OPCIONES_QUE_NO_CAMBIAN_LA_CORRIDA`, intacta.
- `curva_de_equity` sigue dando la curva de la cuenta en curso (un mes: la de siempre); la parte
  común sale a `_curva_de`, que usa también la foto. `cuentas_del_tramo(motor)` da las cerradas más
  la en curso, para la salida del punto 3. Ninguna decisión lee las cerradas.
- Tests nuevos, sintéticos (`tests/unit/test_cuenta_por_mes.py`, con los escenarios en
  `tests/unit/escenarios_cuenta_por_mes.py`, el día de 2030 de `test_cableado.py` desplazado a
  enero y febrero de 2030 con el `_mercado_del_dia` de `test_racha_perdidas.py`): (1) enero se
  suspende por el salto de 2.000 puntos y febrero vuelve a operar con el lote del capital, igual que
  febrero corrido solo, y la cuenta de enero queda conservada; (2) con el tope del registro, el
  seguidor de febrero nace con el capital y sin cortes y el primer toque de febrero es de febrero;
  la racha, un `xfail` estricto con D1 tal cual y un test con lo de hoy (sigue: 2); (3) dos días
  del mismo mes y (4) la diaria con dos meses: el informe ENTERO es el de `main`, por golden; y la
  diaria no conserva cuentas y su primer toque sigue siendo el de enero; (6) el visor:
  `detalle_para_visor` del primer día de febrero da el saldo y la equity de febrero corrido solo;
  y uno más, el mes por la clave (15 y 16 de enero, 12 y 13 de febrero: una sola cuenta cerrada,
  con dos días).
- **Los goldens de `main`**, en `tests/golden/cuenta_por_mes/` (los dos de D6 (3) y (4)) y
  `tests/golden/metodo_adr0092/` (los de la sección de ADR-0092 del punto 3, con el criterio real),
  y la salida de `main` del escenario que cambia, en `anexos/CUENTA-POR-MES/main/`: generados en un
  clon desacoplado de `main` (`git worktree add --detach C:/cm/cpm main`, 8aeed0b) con los dos
  ficheros de test de la rama copiados dentro, por `PYTHONUTF8=1 uv run pytest -q -s
  tests/unit/test_cuenta_por_mes.py::test_el_volcado_de_los_escenarios > C:/cm/volcado-main.txt`
  (exit 0) y `anexos/CUENTA-POR-MES/partir_volcado.py` (7 ficheros). Primero lo intenté con un
  guion que importaba `tests.unit`, y la guardia lo negó (no resuelve `from tests.unit import ...`
  desde un guion; no se rodea: se rehízo por pytest). El primer volcado salió en cp1252 (el «§»):
  se repitió con `PYTHONUTF8=1`.
- En `main`, el escenario de dos meses deja febrero congelado: «estado: SUSPENDIDA», la curva de
  febrero sin equity mínima y ningún evento de febrero (`anexos/CUENTA-POR-MES/main/dos-meses.txt`).
- `ruff format`, `ruff check` y `mypy` en verde sobre lo tocado; los tests de cableado, racha,
  a44, tope, margen, método y arnés, en verde con el código de la rama. La comparación de los
  tests nuevos con el código de `main`, sobre la rama commiteada, va en el punto 3.

#### Los tests del punto 2 con el código de `main`, sobre la rama commiteada (8d7b359)

En el clon `C:/cm/cpm` (`main` 8aeed0b), con `tests/unit/escenarios_cuenta_por_mes.py`,
`tests/unit/test_cuenta_por_mes.py` y los goldens de la rama copiados dentro:
`PYTHONUTF8=1 uv run pytest -q -p no:cacheprovider -rA tests/unit/test_cuenta_por_mes.py`, exit
1 (salida entera en `anexos/CUENTA-POR-MES/main/rompe-en-main-punto-2.txt`). Rompen POR LO QUE
MIDEN:
- `test_el_segundo_mes_vuelve_a_operar_desde_el_capital`: `assert 0 == 1`, las operaciones de
  febrero; en `main` RN-031 y RN-032 prohíben y febrero no coloca.
- `test_el_seguidor_del_tope_y_el_primer_toque_...`: `assert [(2030-02-12 06:00, 'dia'), ...] ==
  []`; en `main` el seguidor corta el día y la semana al abrir febrero con el saldo de enero.
- `test_el_visor_ve_el_saldo_del_mes_nuevo_desde_el_capital`: `48070.5000000 == 99430.2000000`;
  en `main` el visor ve el saldo suspendido de enero.

Pasan en `main`, como deben: los dos goldens (`dentro-de-un-mes`, `diaria-dos-meses`) y el volcado;
el `xfail` estricto de la racha es `XFAIL` también en `main` (allí tampoco se reinicia). Los otros
cuatro fallan en `main` por `AttributeError: 'MotorCableado' object has no attribute
'cuentas_cerradas'`: prueban la conservación de D3 (y que la diaria y un mes no conserven nada),
que en `main` no existe; no son los que prueban el reinicio.

### Punto 3 · La salida (D4, D5) y los textos de D7

- `informe_simulacion`: con un solo mes, o con la diaria, el código de siempre, sin tocar (el `if`
  nuevo solo envuelve el bloque del veredicto y la curva). Con varios meses (hay cuentas
  cerradas): en la cabecera «RACHA DE PERDIDAS (RN-036, A-51): por cuenta: ver cada mes», «PRIMERO
  EN TOCAR UN LIMITE: por cuenta: ver cada mes» y «CUENTA: UNA POR MES (ADR-0092 §8): N cuentas»
  (tras el primer toque, donde va la línea de la diaria); y en vez de «### Veredicto de la cuenta
  sobre el tramo» y «### Curva de equity», un bloque «### Cuenta de AAAA-MM» por cuenta, en orden,
  con su primer toque, su racha al cerrar el mes, estado, motivo, instante, saldo, equity, días de
  trading y su curva, con las mismas líneas que el tramo entero (la curva va con su rótulo en
  minúsculas dentro del bloque, sin `###` propio).
- `_informe_metodo` (D5): la cascada, la esperanza, la tabla de posiciones, el material sin vídeo,
  el remuestreo y el punto de equilibrio, como hoy, sobre todo. Con varios meses, d) y e) por
  cuenta con `medir_por_cuentas` (nueva y pura en `criterio_fidelidad.py`, con su test) y la línea
  dice la peor y de qué mes; f) dice «alguna cuenta entro en SUSPENDIDA: si (AAAA-MM)» o «no». La
  función confirma la medida de la fase 0, d) (i): las cifras de la peor cuenta son las de la curva
  de todos los días seguida (`test_medir_por_cuentas_...`). El motivo del veredicto, como dice la
  PARADA condicional 2: con una cuenta, el de `main`; con varias, «f) alguna cuenta entro en
  SUSPENDIDA (meses)». Para eso `MedidaRentabilidad` gana dos campos con valor por defecto
  (`cuentas = 1`, `meses_suspendidos = ()`): es más que «el motivo y una función pura», y se dice
  aquí (desviación 3).
- La guardia nueva de D5: `tests/golden/metodo_adr0092/main-{hueco,stop,viva}.txt`, la sección
  generada en `main` con el criterio real en el motor y una operación del trader por posición, y
  `test_con_un_mes_la_seccion_de_adr0092_es_la_de_main`. El golden de
  `tests/golden/informe_simulacion/` no se ha tocado (ruta protegida del contrato) y
  `test_lo_que_ya_salia_es_byte_a_byte_lo_de_main` sigue en verde.
- D6 (5): `test_con_varios_meses_la_salida_lleva_un_bloque_por_cuenta` y
  `test_con_varios_meses_d_y_e_son_por_cuenta_y_f_dice_cual`.
- Los textos de D7: la ayuda de `--diagnostico-cuenta-diaria` (`cli.py`), el comentario de
  `diagnostico.py`, los comentarios de `MotorCableado` (punto 2) y los rótulos de
  `scripts/embudo_77.py:905` y `scripts/f35_resultado_r.py:81`, a «arrastrada dentro de cada mes,
  una cuenta por mes (ADR-0092 §8)»; nada más de los guiones. `orden_stop_o_limite.py` y
  `caja_77_exploratoria.py` no llevan rótulo: no se tocan (fase 0, b).
- **Regresión contra `main` por hash** (los siete ficheros del volcado de los escenarios, `main`
  en el clon y la rama en el repo, con `partir_volcado.py`):

| Fichero | sha256 main (16) | sha256 rama (16) | ¿Igual? |
|---|---|---|---|
| `cuenta_por_mes/main-dentro-de-un-mes.txt` | 7b825a9a07853c64 | 7b825a9a07853c64 | sí |
| `cuenta_por_mes/main-diaria-dos-meses.txt` | 649818441641fc1a | 649818441641fc1a | sí |
| `metodo_adr0092/main-hueco.txt` | 00b8204b5254e080 | 00b8204b5254e080 | sí |
| `metodo_adr0092/main-stop.txt` | 87f47c046f8b083c | 87f47c046f8b083c | sí |
| `metodo_adr0092/main-viva.txt` | b7c6390eee622012 | b7c6390eee622012 | sí |
| `anexo/dos-meses.txt` | 0a03f0f898a2b302 | 8df71537ec0a750e | no, a propósito |
| `anexo/dos-meses-con-criterio.txt` | 1ad9b4a03db51634 | ff56a15e68dfa0aa | no, a propósito |

  Los dos que difieren, en `anexos/CUENTA-POR-MES/main/` y `rama/`, con su `diff` en
  `diff-dos-meses.txt` y `diff-dos-meses-con-criterio.txt`: la cabecera, los dos bloques, febrero
  que opera desde 100.000 (su orden, sus dos eventos, su petición y su posición) y d), e) y f) por
  cuenta; a) pasa de 1 a 2 y las réplicas descartadas de 2454 a 0 porque febrero ahora tiene una
  operación. Nada más. Son cifras de un día SINTÉTICO de 2030, no del bot sobre material.
- `ruff format`, `ruff check` y `mypy` en verde sobre lo tocado de `src/` y `tests/`. `mypy` sobre
  `scripts/embudo_77.py` y `scripts/f35_resultado_r.py` da 7 errores, los mismos en `main` (medido
  en el clon): anteriores a la rama, en líneas que no se tocan.

### Punto 4 · Las líneas del cierre, probadas sobre una copia

`uv run python -B docs/validation/anexos/CUENTA-POR-MES/simular_cierre.py` (en memoria; la copia de
PROJECT_STATE, en una carpeta temporal que se borra), salida:

```
F viva en la copia? True; NA:F en R3.8? False; R3.8 HECHA? True
a: []
b: []
c: []
«la rama de la cuenta por mes» en la copia? False; R3.8 como dependencia pendiente de R5.2? False; R3.8 en el «Depende de» de R5.6? False
PROJECT_STATE con las lineas del cierre: 22682 bytes (wc -c de la copia); con las cuatro lineas de cabecera del cierre: 22616; los tests de test_project_state: ok
```

**Por debajo de 23.000: no hace falta recorte.** Las líneas, literales en el guion:
- **F**: «Siguiente: la rama de la cuenta por mes (ADR-0092, trabajo/cuenta-por-mes) y después la
  re-corrida que cuenta …» pasa a «Siguiente: la re-corrida que cuenta (ADR-0070 §3), la primera
  con la comisión medida (ADR-0090 §3), el sello del respaldo de ADR-0091, el método de ADR-0092 y
  la cuenta por mes;», con el resto de F igual. F sigue viva: no sale a HISTORIA y no lleva
  registro HECHA.
- **Technical Debt**, la línea del visor: «… (cli.py:2558; el arnés sí, :2438): con `--todos
  --simular` corre una cuenta por mes como el arnés (ADR-0092 §8), nunca la diaria
  (VISOR-CONSTRUCCION.md §4.3).» Las líneas de `cli.py` se movieron una por la ayuda nueva
  (medido en la rama).
- **La hoja de ruta**: R3.8 pierde `NA:F` de sus Refs (si no, `test_hoja_de_ruta.py:144-145` da «esta
  HECHA y la letra sigue viva»: fase 0, e) 7) y gana «Estado: HECHA (`trabajo/cuenta-por-mes`;
  CUENTA-POR-MES.md) …»; R5.2 deja de depender de R3.8 («El sello del respaldo M1 (R3.6), el método
  (R3.7, ADR-0092) y la cuenta por mes (R3.8) están HECHOS.»); R5.6, «… y la re-corrida que cuenta,
  con su línea «habilita medir» en sí …», sin «después de R3.8».
- Las cuatro cabeceras del ritual, simuladas con el tag siguiente libre, `stable/F38s-cuenta-por-mes`,
  y un sha de relleno.
- Si el consultor responde la PARADA condicional 1 con «la racha también», la línea de Estado de
  R3.8 añade «y la racha de RN-036» en el mismo commit que la aplique.

### Desviaciones

1. **La fila de HOLDOUT-EXPOSICIONES llegó tarde.** La lección 8 de F38r pide escribirla ANTES del
   primer clon, `make check` o lectura del día. Los tres `make check` del 2026-11-07 (apertura,
   fase 0 y punto 1), el espía de meses y el auditor se hicieron sin ella; se declararon el
   2026-11-08, al día siguiente, en una fila con fecha del 7. La del 8 se escribió y estadió antes
   de su primer clon y su primer `make check`.
2. **Un fichero escrito en el repo con `make check` corriendo.** Durante el `make check` del punto 3
   escribí `anexos/CUENTA-POR-MES/simular_cierre.py` en el repo (CLAUDE.md, «nada escribe mientras
   corre make check», punto 3). Me di cuenta en el acto y lo moví a la carpeta de trabajo antes de
   que acabara; la huella del final cuadró con la del principio y selló (árbol a275b5c). Se volvió
   a copiar tras el commit del punto 3.
3. **`criterio_fidelidad.py` cambia algo más que «el motivo y una función pura»**:
   `MedidaRentabilidad` gana dos campos con valor por defecto (`cuentas`, `meses_suspendidos`) para
   que el motivo de f) sepa si hay una cuenta o varias (PARADA condicional 2). Con los valores por
   defecto todo lo que ya la usaba da lo de antes.
4. **La guardia negó dos formas, y no se rodeó**: el plugin de pytest por `PYTHONPATH` (variable de
   entorno fuera de la lista) y un guion que importaba `tests.unit` desde fuera de `tests/` (no
   resuelve el import). Se rehicieron con `pytest.main` desde un guion que no importa `tests.unit` y
   con un test de volcado por `pytest -s`. Las dos negativas son legítimas para la guardia; no
   piden cambiarla.
5. **D4, el formato del bloque**: dentro de «### Cuenta de AAAA-MM» las líneas son las mismas que
   las del tramo entero, pero el rótulo de la curva va como línea («curva de equity (…):») y no
   como `###` propio, para que el bloque sea uno solo; y la racha lleva «al cerrar el mes».
6. **D7, los guiones**: dos de los cuatro que nombra el encargo no llevan el rótulo y uno no
   construye el motor (fase 0, e) 1): se cambiaron los dos rótulos que existen.

### Lo que no se pudo medir

- Ninguna corrida del arnés, por la regla de la rama: cómo cambia la corrida que cuenta con una
  cuenta por mes se verá en la rama siguiente. Tampoco se ha medido sobre días reales que el visor
  con `--todos --simular` dé una cuenta por mes: está probado a nivel de `correr_dia` y
  `detalle_para_visor` con días sintéticos (D6 (6)), y `Preparador.preparar` llama a `correr_dia`
  día a día (`visor.py:325`).
- Qué motor de un solo mes de abril de 2026 vio el espía de la fase 0: el espía solo anotó meses,
  no nombres de test.

### Las líneas del cierre

Las del punto 4, literales en `anexos/CUENTA-POR-MES/simular_cierre.py`. Y la fila de
ERRORES-RECURRENTES, preparada (se completa con lo que encuentren el revisor y el consultor):

| `trabajo/cuenta-por-mes` | (el revisor, abajo) | (1) **(menor)** El encargo puso la racha de RN-036 en la lista de lo que empieza de nuevo cada mes sin medir el texto de la spec, que la describe «contando en TODOS los dias de la corrida» (PARADA condicional 1). Lección: una decisión que reinicia un acumulador de la spec se mide contra la `descripcion` de ese acumulador antes de escribirla. (2) **(menor)** D7 nombró cuatro guiones con un rótulo que solo tiene uno. Lección: un literal se busca con grep antes de citarlo en una lista. (3) **(menor, de la sesión)** La fila de exposición, tarde otra vez (desviación 1), y un fichero escrito en el repo con `make check` corriendo (desviación 2). Lección: la fila va en el mismo turno en que se abre la rama, antes del primer `make check`; y mientras corre `make check`, los borradores van a la carpeta de trabajo. |

## El encargo, punto por punto

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 1 | Base: main 8aeed0b, tag → a1907fa, CI 42440794180 en verde, ninguna otra rama | Hecho | §0 |
| 2 | Abrir con `abrir-rama`: contrato (tramo entre comillas, riesgo alto, artefacto, rutas) | Hecho | 15b1374; `contrato.yaml` |
| 3 | Revisar /model | Hecho | §0: Opus 5.5 |
| 4 | Objetivo: una cuenta por mes, como condición; `OPCIONES_QUE_NO_CAMBIAN_LA_CORRIDA` y la diaria sin cambiar | Hecho | punto 2; la lista, sin tocar (`arnes.py` protegido y sin diff) |
| 5 | NO cambia: estrategia, firma, bróker, llenado, `cuenta.py`, primitivas, spec, registro, perfiles, simulador, criterio, tolerancias, umbrales, la lista, la diaria | Hecho | `git diff --stat main...HEAD`: ninguno de esos ficheros; los goldens de la diaria y de un mes, iguales |
| 6 | Dentro de un mes, ninguna decisión ni llenado cambia | Hecho | golden `dentro-de-un-mes` (informe entero), hash igual a `main` |
| 7 | Ninguna corrida del arnés ni cifra agregada nueva del bot | Hecho | solo días sintéticos de 2030; ningún `motor arnes` |
| 8 | Herencias: NOTAs en ADR-0050 H6 y ADR-0049 | Hecho | punto 1 (12c4861) |
| 9 | Herencias: buscar «cuenta por mes», «R3.8», … y añadir lo que falte | Hecho | fase 0, b) y e): `racha.py`, ADR-0077, la spec y ADR-0070 (PARADA condicional 1 y 3) |
| 10 | D1: lo que empieza de nuevo | **Parcial** | la cuenta, el seguidor y el primer toque, sí; la racha, en PARADA condicional 1 |
| 11 | D2: en `correr_dia`, como condición; el estado, atributo del motor | Hecho | `cableado.py`, `correr_dia` |
| 12 | D3: las cuentas cerradas, en orden, con todo; la diaria no conserva | Hecho | `CuentaDelMes`; `test_con_la_diaria_no_se_conserva_ninguna_cuenta` |
| 13 | D4: con un mes, byte a byte; con varios, cabecera y bloques; la diaria, igual | Hecho (formato del bloque, desviación 5) | goldens; `test_con_varios_meses_la_salida_lleva_un_bloque_por_cuenta` |
| 14 | D5: cascada, esperanza y remuestreo como hoy; d) y e) por cuenta con el mes; f) «alguna cuenta»; función pura con su test; golden de la sección desde `main` y su test | Hecho (motivo de f), PARADA condicional 2; desviación 3) | `medir_por_cuentas`; `tests/golden/metodo_adr0092/`; hashes iguales |
| 15 | D6 (1)-(6), sintéticos, que rompan en `main` por lo que miden, con la salida contra `main` en el anexo | Hecho | punto 2; `anexos/CUENTA-POR-MES/main/rompe-en-main-punto-2.txt` |
| 16 | D7: consumidores, rótulos de los guiones, ayuda de `cli.py`, `diagnostico.py`, comentarios del motor; los seis tests, sin cambiar | Hecho (los guiones, desviación 6) | punto 3; ninguno de los seis tests se ha cambiado |
| 17 | D8: NOTA en ADR-0092 §8 y su fila del índice; NOTAs en 0050 y 0049; «Implementado» en el recuadro de 0053 | Hecho | 12c4861 |
| 18 | Fase 0 a)-e), commiteada sola | Hecho | f66ce24 |
| 19 | Fase 1, un commit por punto, con state check, `make check`, ruff y mypy | Hecho | 12c4861, 8d7b359, 1912f77 y el del punto 4 |
| 20 | La fila de HOLDOUT-EXPOSICIONES antes del primer clon / `make check` de cada día | **Hecho de otra forma** | la del 7, tarde (desviación 1); la del 8, antes |
| 21 | Punto 4: las líneas del cierre sobre una copia; tests de la hoja y de PS en verde; `wc -c` con las cuatro cabeceras; PARADA si pasa de 23.000 | Hecho | 22.682 y 22.616 bytes: sin PARADA |
| 22 | Sin `fix/`: no toca hooks, rutas, `.claude/` ni plataforma | Hecho | `git diff --stat`: nada de eso |
| 23 | Informe con todo, y el revisor (opus) con los siete alcances, pegado al final | Hecho | abajo |
| 24 | Rama lista para revisión, NO cerrada | Hecho | `## Estado` |

## Estado

EN CURSO.
