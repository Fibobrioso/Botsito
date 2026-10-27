# ACTIVAR-SESION-05-MOTOR · Lo que la sesión 5 pide al motor (R4.1, entrada V)

Rama `trabajo/activar-sesion-05-motor`, abierta el 2026-10-26 desde `main` en 32904ee (commit de
estado sobre el merge 2c26fb2, tag `stable/F38e-activar-sesion-05`). Encargo:
`docs/encargos/trabajo-activar-sesion-05-motor.md`. Tramo: R4 (R4.1 de `docs/plan/HOJA-DE-RUTA.md`,
lo que queda; V de la Next Action).

Antes de abrir se comprobó con git (skill `abrir-rama`, paso 1):

- `git rev-parse --short main` = 32904ee; `git rev-parse main origin/main` da dos veces
  32904ee0f0d2ebba44abef1c5183655b633fb5e7; `git status --short` vacío.
- El último tag de `docs/state/HISTORIA.md` es `stable/F38e-activar-sesion-05`;
  `git rev-parse "stable/F38e-activar-sesion-05^{commit}"` = `git rev-parse main^1` =
  2c26fb215305ff6d50e0ad7d7d437025056d40b1; `git ls-remote --tags origin stable/F38e-activar-sesion-05`
  devuelve el tag.
- La CI de `main` sobre 32904ee0f0d2ebba44abef1c5183655b633fb5e7: `gh run view 40421174533`
  suelto, `completed` / `success`, `headBranch` main, `headSha` el mismo.
- `git branch --list` solo da `main`; `git ls-remote --heads origin "fix/*"` sale vacío.

Con la apertura entra la fila del 2026-10-26 de `docs/validation/HOLDOUT-EXPOSICIONES.md` con la
exposición del auditor del consultor (el `grep -rln` sobre la raíz de un clon de solo lectura), que
el encargo manda declarar en el primer commit.

Los ADR que el encargo manda escribir se citan aquí antes de existir; cada uno sale del bloque en
el commit que lo crea:

```ids-inexistentes
ADR-0086 — RN-020 retira la orden pendiente al llegar al tope (punto 8); aún no existe
ADR-0087 — el ADR que S-15 tendría si existiera la frontera (punto 9); aún no existe
```

## 0. Fase 0 · Inventario medido, sin tocar spec, knowledge ni código

Medido el 2026-10-26 sobre la apertura de la rama (e8cde8b, encima de 32904ee). Lo leído, por
Read: el encargo y las dos skills que lo mandan, `ACTIVAR-SESION-05.md` §2 y §3, los 17 ítems de
evidencia que el encargo nombra (v15, v16 y v10, en `knowledge/evidence/`), `SESION-05-EXTRACCION.md`
§3.1, §3.3 y §3.4, el motor (`domain/pivotes_m15.py`, `domain/estructura_m1.py`, `engine/zonas.py`,
`engine/racha.py`, `engine/motor.py`, `engine/primitivas.py`, `engine/primitivas_broker.py`,
`engine/cableado.py`, `engine/interprete.py`, `engine/diagnostico.py`, `engine/tope_trader.py`), la
spec (RN-002, RN-004, RN-005, RN-006, RN-007, RN-008, RN-009, RN-011, RN-020, RN-033, RN-035, RN-036
y el vocabulario de predicados y acciones; `parametros.yaml` en los 16 parámetros que la tabla cita;
`ambiguedades.yaml` en A-21, A-35, A-48, A-50 y A-51), los ADR 0045, 0054, 0060, 0061, 0062, 0064,
0066, 0076, 0077 y 0083 con su índice, `feedback/modelo.py`, `feedback/aplicar.py`, `situacion_de`
de `cli.py`, `spec/modelo.py` (las guardias, `comprobar_consumo`, `literal_coincide`) y los tests
que congelan lo que cambia. Tres `pytest` sintéticos en el repositorio, cuatro guiones de la carpeta
de trabajo sobre velas sintéticas y un clon desechable (`C:/cm/motor`, `git worktree add --detach`
sobre e8cde8b; skill `comparar-con-main`) para lo que había que escribir. **Nada de material**:
ninguna filtrada ni cruda, ningún fotograma, ningún libro, ningún caso; nada de julio, diciembre,
marzo ni febrero. Ningún `motor arnes` ni `motor visor`.

### 0.a La tabla de activación

Una fila por punto de las decisiones del consultor (1 a 11). «Hoy» es el código de `main` (igual
que el de la rama, que no lo ha tocado). «Cuadra» dice si la decisión cuadra con lo medido; lo que
no cuadra va a «Lo que necesito que decidas».

| Punto | Ítems y su `afirmacion` | Lo que hace hoy el código y el test que lo congela | ADR que lo fija hoy | Decisión del consultor | Cuadra |
|---|---|---|---|---|---|
| 1 · A-35, la mecha | `ev-v15-000553-9d95178a`: si el precio pasa el alto de M15 solo con la mecha y vuelve, el alto pasa a ser el de esa mecha. Contraste: `ev-v10-012456-9dc1d221` (pasa por poco con la mecha y vuelve: no cuenta, lo tiene que pasar con cuerpo), `ev-v10-020142-30fd2569` (un nivel de M15 roto con mecha anula la entrada; en M1 vale mecha y cuerpo) | (i) `_pivote_de` da el extremo de la racha y la mecha de la contraria no lo mueve (`pivotes_m15.py:86-101`; medido: racha 134, contraria con mecha 140 → 134; en un bajo, racha 96, mecha 90 → 96). (ii) `pivote_mas_reciente` no mira ni las M15 posteriores ni la en curso ni las M1 para el nivel (medido: M15 posterior con mecha 138 y cierre 125 → 134, `toca` sí y `cruza(cuerpo)` no). Test: `test_pivotes_m15.py::test_lo_fijo_y_visible_doji_y_mecha_de_la_contraria` (:145). El nivel lo leen `motor.py:138` (`liquidez_m15`), `primitivas.py:218` (`alcanza_nivel`, `cruza`, `la_toma_es_de_la_sesion`) y `zonas.py:200` (`_toma_del_momento`, que usa `(lado, nivel, formado_en)` como IDENTIDAD de la toma) | ADR-0045 (el pivote más reciente ya formado; «A-35 no se sustituye por un parámetro provisional»), ADR-0054 (descarta «un valor provisional por defecto» porque ADR-0045 lo prohibió), ADR-0062 §1 (la toma la hace una M1 con cuerpo) | parámetro `liquidez_m15_mecha_que_vuelve` = `cualquier_mecha`, DEFAULT_AMBIGUOUS bajo A-35, sin registro; ADR-0084; en espejo en el bajo; solo M15 | En parte: el mecanismo sí; el parámetro provisional bajo A-35 lo prohíben ADR-0045 y ADR-0054 por escrito (decisión 0); el caso (ii) está en tensión con el «no cuenta» de `ev-v10-012456` (decisión 1) |
| 2 · las velas sin cuerpo en M1 | `ev-v15-003959-5898c61e`: las velas sin cuerpo dentro del tramo que marca el punto de breaker no cuentan, sean una o tres, y en venta igual al revés. `ev-v15-004037-a2ab3980`: si entre la verde y la roja hay velas sin cuerpo, el máximo de la verde es punto de breaker siempre que el precio venga de un flujo bajista y después rompa cerrando por debajo. `ev-v16-000851-f5ae3b6f`: en el retroceso, una vela sin cuerpo, una de uno o dos puntos o dos sin cuerpo seguidas no cuentan como alternancia | El doji corta la racha y no forma pivote (`pivotes_m15.py:79`, `:127-128`); medido en M1: V, doji, R → `pivotes_formados` = [] y `ultimo_punto_de_ruptura` = None (sin doji, ALTO en el máximo de la verde); R, doji, V, R + breaker → 1 zona y segundo esquema (la serie S-10 sin doji: 2 zonas, None); V, V(1 punto), R → la de 1 punto es verde y entra en la racha; la zona posterior V, V, doji, R, V → (None, None) y sin doji (3, 1021). Tests: `test_a21_series.py` (fila del doji y `test_las_diferencias_son_solo_el_doji_y_el_breaker_por_mecha`), `test_pivotes_m15.py:145` | ADR-0076 §2 (la fila DISTINTO) y cabecera (la regla de la vela sin cuerpo retirada el 2026-10-11), ADR-0061 §4 (la zona posterior con la misma geometría), ADR-0064 (la caja), A-32 RESUELTA (en M1 la mecha siempre vale) | ADR-0085 (enmienda ADR-0076; NOTA en ADR-0061); solo M1 y solo cuerpo cero; CONFIRM sobre RN-007 | Sí, con dos cosas medidas: la condición de `ev-v15-004037` no la exige el motor y aplicarla pediría cerrar con cuerpo en M1 (decisión 3); y el cambio solo en M1 rompe `test_son_las_funciones_de_r5_y_r6_de_caja_77` (decisión 2) |
| 3 · RN-007 con umbral cero | `ev-v16-002841-8cfe382a`: una vela casi plana tiene que ser de cero puntos de cuerpo, plana totalmente, porque las otras pueden servir para trazar el punto de breaker. Corrige `ev-v10-014310-2296423b` (casi plana podría considerarse con 1 o 2 puntos, «entre comillas») | RN-007 (`strategy_spec.yaml:1346-1375`) dice «casi plana» sin umbral y sus notas «DESALINEADO CON EL MOTOR»; `color()` ya es cuerpo cero (`pivotes_m15.py:66-72`) | — (RN-007 cita `fb-2026-09-29-sesion-03-ffab23dc`, un CORRECT vivo) | CORRECT sobre la evidencia, notas de RN-007; con el 2 si el código es el mismo | Sí (medido en el clon: el CORRECT sobre evidencia sale en `feedback pending` como «(?) sin forma mecánica», no como pendiente). Los puntos 2 y 3 van en UN commit: el código es el de ADR-0085 y las notas de RN-007 se escriben una vez |
| 4 · A-50, la caja entera | `ev-v15-010451-5b123278`: si el 0 de la caja queda justo en la línea del nivel tomado, o por encima en una compra, es indiferente: lo importante es validar bien el posible punto de breaker | `se_desarrolla_en_el_lado_de_ruido` mira solo el 0 (`zonas.py:539`, `e.entrada > toma["nivel"]`, estricto: el 0 EN la línea ya no es ruido); con `orden_nace_en_el_punto` la zona es la de `zona_del_punto` (`:529`), la MISMA llamada que hace `toca_colocar_orden_limite` (`:489`) en ese instante, así que su `extremo` es el 1 que llevará la orden (con `en_cada_cierre_m1` el id lleva el extremo, `:390-394`; `test_orden_stop_pivote.py::test_con_la_caja_recalculada_un_1_nuevo_liga_otra_zona_del_mismo_punto`) | ADR-0064 §4, decisión 4 (RN-005 se aplica a la zona del punto) | parámetro `caja_lado_de_ruido` = `caja_entera`, DEFAULT_AMBIGUOUS bajo A-50, fuente evidence, sin registro; lo lee `se_desarrolla_en_el_lado_de_ruido` | En parte: el valor con fuente evidence pasa `test_registro` y `test_provisional_cuelga_de_abierta` (medido en el clon); pero la lista `parametros` de RN-005 NO es lector para `comprobar_consumo`: tiene que entrar como argumento de la forma (medido en el clon: con `caja: caja_lado_de_ruido` en la forma y en el vocabulario, `spec check` y `knowledge validate` lo aceptan); y no hay ADR donde escribir la lectura del consultor (decisión 4) |
| 5 · S-21, la racha | `ev-v16-002126-d2376f71`: al día siguiente de parar por 9 pérdidas seguidas, la racha empieza en cero. `ev-v10-010804-5b6ad1a3`: la racha sigue de un día a otro | `racha_perdidas_reinicio` = `nunca` CONFIRMED por `fb-2026-10-04-sesion-04-d1792021` (`parametros.yaml:1282-1296`); `SeguidorRacha.__post_init__` solo admite `nunca` (`racha.py:96-97`); `detenido` deja la racha en 9 al día siguiente y la décima vuelve a detener (`:122-132`). Tests que lo congelan: `test_racha_perdidas.py:79` (asserta `REINICIO_NUNCA`), `:117-139` (`test_nueve_perdidas…`), `:293-346` (el décimo día «con la racha en 9») | ADR-0077 §1 y §5 (lectura PROVISIONAL de la sesión) | opción nueva `tras_la_detencion`, CORRECT sobre el parámetro con `--supersede` d1792021; recuadro en ADR-0077 §5 | Sí (medido en el clon: el registro se escribe, `apply --check` propone SOLO ese cambio, `apply` deja `tras_la_detencion` CONFIRMED citándolo y `feedback pending` no lo lista). `test_las_opciones_sin_contrato_se_niegan` NO cambia de sentido: comprueba que `fin_de_dia` se rechaza, y sigue |
| 6 · S-22, el último minuto | `ev-v16-002248-08e9600f`: al llegar la hora de cerrar, la orden sin llenar se quita un minuto antes, igual que se cierra la operación abierta. `ev-v16-002323-515b9da4`: si la orden se llena en el último minuto la cierra enseguida, y en el último minuto antes de las 11 o de las 3 no pone ninguna orden | RN-035 retira al abrir la sesión y a `ventana_fin` (`strategy_spec.yaml:996-1006`); `vence_vela_h4` da SÍ en fin−1 y en fin, NO en fin−2 y fin+1 (medido con el registro real, `cierre_h4_antelacion` = 1); el evento del límite es de la sesión siguiente (`cableado._sesion`, `:502-509`; `test_rn035_ventana_fin.py:90`). Quien COLOCA es RN-015 (`colocar_orden_limite`, `efecto: abrir_operacion`); RN-011 solo dimensiona; RN-006 reubica cancelando (`reubicar_orden_limite`, SIN `efecto`) y RN-011 y RN-015 recolocan en el mismo cierre. Las gates se evalúan antes que los disparadores (`interprete.py:311-345`, `CLASES_EN_ORDEN`). Test: `test_hueco_la_orden_que_se_llena_en_el_ultimo_minuto_se_cierra_en_el_limite` (:72) | ADR-0060 §4-§5 (RN-002 y el límite), §6 (RN-002 no retira órdenes), ADR-0066 §4 (RN-035) | RN-035 retira en [fin−antelación, fin); RN-037 gate; CORRECT sobre RN-035 | Sí, con la forma medida en el clon: un predicado nuevo `en_el_ultimo_tramo_h4` (SÍ en [fin−antelación, fin), NO en fin), tercera rama de RN-035 y gate RN-037 que prohíbe `abrir_operacion`; `spec check` y `knowledge validate` los aceptan (precedencia incluida) y `feedback pending` deja de listar el CORRECT cuando RN-035 lo cita. Un `prohibe` en RN-035 (disparador) no sirve: las prohibiciones se acumulan al disparar y un disparador anterior en el orden ya habría colocado (decisión 5) |
| 7 · S-20 | `ev-v16-001834-732a76b6`: no importa el color de la vela que rompe el punto de breaker; si lo pasa con la mecha, se valida | `_pasa` con MECHA no mira el color (`estructura_m1.py:103-111`; medido: verde que baja la mecha en una venta, roja con mecha en una compra → True). `test_a21_series.py` YA tiene las dos filas del breaker contrario que rompe con mecha (:86-89, :97-99), parametrizadas en compra y venta (:139, :151) | ADR-0076 §4, pregunta 2 | sin registro ni código; fila nueva si falta | Sí: no falta nada; el informe lo dice y no se añade ninguna fila |
| 8 · RN-020 retira la pendiente | — (DECISIÓN DEL CONSULTOR con el motivo de RN-036, ADR-0077 §3) | RN-020 prohíbe `abrir_operacion` y fija `detenido_por_tope`, sin retirar (`strategy_spec.yaml:1959-1968`); RN-036 retira con `retirar_ordenes_pendientes` (`primitivas_broker.py:692-700`, idempotente). Dentro de la spec una pendiente no convive con una posición (RN-011, `ninguno_de`; ADR-0083 D4): la pendiente viva al tocar el tope solo existe sin llenar | ADR-0077 §3 («RN-020 no cambia») | ADR-0086: la forma de RN-020 gana `retirar_ordenes_pendientes`; recuadro en ADR-0077 §3 | Sí. Test sintético: una orden colocada que no se llena y un acumulador `perdida_dia` sintético que da SÍ en un cierre posterior (como `test_cableado._sinteticas` da NO): RN-020 dispara y la pendiente queda CANCELADA; en `main` sigue viva |
| 9 · S-15 | `ev-v15-012616-d534455a`: después de la toma entra en la zona en la que el precio llega a activar la orden, sin número de zonas: la orden se actualiza a la más reciente. `ev-v16-001445-7ca4f033`: el punto de breaker se va actualizando, siempre el más reciente que cumple las condiciones (ítem de S-20 según sus notas y la extracción: usarlo para S-15 es lectura del consultor) | `zonas_de_control` cuenta desde la toma (`estructura_m1.py:141-158`) y `zonas_desarrolladas_superan` también (`zonas.py:462-477`); RN-009 es una gate sobre `abrir_operacion`. Lo medido en 0.b.8: ninguna frontera de retroceso deja S-10 sin esquema, y por el camino real S-10 YA ENTRA | ADR-0076 §2-§3 (A-21 RESUELTA: «limpia» = lo que filtra RN-009) | solo medir; si no hay frontera, a la sesión 6 con dos esquemas | Sí: no existe la frontera (0.b.8); va a la sesión 6 (decisión 6, con lo que el camino real añade a la pregunta) |
| 10 · lo viejo | — | `broker.py:177` («DEFAULT_AMBIGUOUS bajo A-57»); `embudo_77.py:435` y `caja_77_exploratoria.py:132` construyen `Diagnostico(a35=CIERRE_VELA_CONTRARIA, a44=A44_SIN_TOPE, …)` y `bloque_de_la_caja.py:266` `Diagnostico(a44=A44_SIN_TOPE)`: con los parámetros fijados, `lectura_pivote` levanta `DiagnosticoRechazadoError` (`diagnostico.py:111-116`) y `tope_del_registro` `TopeRechazadoError` (`tope_trader.py:140-143`). `test_embudo_77.py` y `test_orden_stop_pivote.py:132` solo IMPORTAN los guiones (`_cargar`), no ejecutan `main` | ADR-0076 §3 (los guiones con argumentos con nombre), ADR-0081 (A-57) | sin ellos; contrato ampliado | Sí |
| 11 · dos recuadros | — | `ACTIVAR-SESION-05.md:935-940` atribuye «la caja entera» al ítem; `:948-953` nombra `fb-2026-10-04-sesion-04-8e2d728a` (el RESOLVE_UNKNOWN sobre A-51) como objetivo del CORRECT | — | recuadros con fecha y rama, cuerpo intacto | Sí |

### 0.b Lo medido, punto por punto

**0.b.1 Los registros se escriben y se aplican.** En el clon `C:/cm/motor` (sin `data/`, sin
`corpus/`), con `uv run botsito feedback new` y todas las opciones obligatorias (`--medio video`,
`--procedencia trader_grabado`, la grabación y el t0 y t1 del ítem, `--recibido-el` 10-23 para v15
y 10-25 para v16, la `cita_literal` como `--respuesta`):

| Registro | Objetivo (admitido por `OBJETIVOS_POR_ACCION`) | Id en el clon | `feedback pending` |
|---|---|---|---|
| CONFIRM sobre RN-007, sin `--valor` (v15, `ev-v15-003959-5898c61e`, 0:39:59-0:40:29) | regla ✓ | `fb-…-72c9a9e8` | «confirma la regla vigente RN-007, que cita fb-2026-09-29-sesion-03-ffab23dc» (sección `(=)`; con `--valor` sería pendiente: `cli.py:2068-2074`) |
| CORRECT sobre `ev-v10-014310-2296423b` (v16, `ev-v16-002841-8cfe382a`, 0:28:41-0:29:02), valor = su afirmación | evidence ✓ | `fb-…-a9e4f879` | sección `(?)`: «un CORRECT sobre evidencia no supersede el item … sin forma mecanica de cruzarlo», como `fb-…-a42c72dd` de la rama anterior; nunca es «reflejado» |
| CORRECT sobre `racha_perdidas_reinicio` = `tras_la_detencion`, `--supersede fb-2026-10-04-sesion-04-d1792021` (v16, `ev-v16-002126-d2376f71`, 0:21:26-0:21:35) | parametro ✓ | `fb-…-978be13f` | antes de `apply`: pendiente («no lo cita todavia»); `apply --check` propone SOLO este cambio («4 parametros; 1 cambian, 3 ya estaban»; la opción `tras_la_detencion` tiene que estar en el enum ANTES, o el registro se rechaza); tras `apply`: CONFIRMED, `valor: tras_la_detencion`, `fuente` el registro, y deja de estar pendiente |
| CORRECT sobre RN-035, valor = la afirmación del ítem (v16, `ev-v16-002248-08e9600f`, 0:22:48-0:23:17) | regla ✓ | `fb-…-1526aa39` | pendiente («RN-035 no lo cita todavia») hasta que RN-035 lo cita con su literal; entonces desaparece |

`feedback pending` del clon al final: «2 pendientes de 139 activos», los dos CORRECT sobre RN-003
que `main` ya lista (deuda G.2 de la hoja de ruta). **«Limpio» significa sin pendientes nuevos.**
Los ids de los registros los calcula la CLI del contenido: en la rama saldrán iguales si el texto
es el mismo.

**0.b.2 Ningún ítem cae en un tramo no citable.** Guion `medir_b2_tramos.py` (lee
`tramos_no_citables.yaml` y los 17 ítems; solape > 0 ms = CAE, el criterio de `verificacion.py`):
los 17 dan solape 0 ms. Los dos más cerca de un tramo: `ev-v16-002126-d2376f71` (0:21:26-0:21:35),
a 10.000 ms del fin del tramo de v16 0:20:02-0:21:16, y `ev-v10-014310-2296423b`, a 11.000 ms del
suyo. A nivel de segmento (`ventana_no_citable`) no se midió: necesita la cruda de v16, que no se
abre; la citación de un registro la comprueba `knowledge validate` al commitearlo.

**0.b.3 Lo que comparten M1 y M15.** `domain/estructura_m1.py:47-53` importa `pivotes_formados` y
`color` de `pivotes_m15.py`, y los llama con velas de M1 en TRES sitios: `referencia_del_breaker`
(:122), `zonas_de_control` (:155) y `ultimo_punto_de_ruptura` (:200). Fuera de `domain/`,
`pivotes_formados` solo lo usa `scripts/bloque_de_la_caja.py:196-215` (`pivote_de_ruptura`), y
`pivote_mas_reciente` solo `engine/motor.py:138`. Medido: la contraria de M1 con mecha 1130 sobre
una racha con máximo 1120 da referencia y punto 1120 hoy, y cambiaría si el cambio del punto 1
fuera común. Por tanto los dos cambios van como ARGUMENTOS de `pivotes_formados` /
`pivote_mas_reciente` con el valor de hoy por defecto: el punto 1 (la mecha) solo lo pide
`motor.py` (M15); el punto 2 (la vela sin cuerpo no corta la racha) solo lo piden los tres
llamadores de `estructura_m1.py` (M1). Un test por marco dice que el otro no se mueve.

**0.b.4 Dónde se juzga la toma y dónde se lee el nivel.** La toma: `alcanza_nivel` (`toca`) y
`cruza` sobre la ÚLTIMA M1 cerrada (`primitivas.py:242-264`, `_liquidez` :204-240, que exige que
el pivote exista antes de que esa M1 cierre), y `la_toma_es_de_la_sesion` con `cruza` sobre las M1
entre `formado_en` y la apertura (:266-296). El nivel: `DatosMercado.liquidez_m15` (`motor.py:131-145`)
llama a `pivote_mas_reciente` con las M15 cerradas y la en curso; lo consumen `primitivas.py:218` y
`zonas.py:200` (`_toma_del_momento`), que guarda `(lado, nivel, formado_en)` como IDENTIDAD del
pivote para distinguir una toma nueva de la misma vista otra vez (`:289`). Consecuencia para el
caso (ii): el nivel solo puede moverse MIENTRAS no esté tomado; en cuanto una M1 lo cruza con el
criterio de la toma, el nivel queda fijo (si siguiera moviéndose, cada M1 posterior con mecha
cambiaría la identidad y `abrir_escenario` vería tomas nuevas). Es lo que propongo implementar: una
función pura de `pivotes_m15.py` que, con las M1 cerradas desde `formado_en` hasta el instante,
lleva el nivel a la mecha más lejana de las que lo pasan SIN cruzarlo con el criterio, y se para en
la primera que lo cruza; la aplica `motor.liquidez_m15`, que tiene las M1. Las M1 de dentro de la
propia contraria ya las cubre (i) (su máxima es la de la contraria).

**0.b.5 Los consumidores de `color() == 0` en M1**, con lo que cambia en cada uno:

| Consumidor | Hoy | Con la decisión del punto 2 |
|---|---|---|
| `pivotes_formados` con velas de M1 (vía `_racha_anterior` :75-83 y `_pivote_en` :127-128): `referencia_del_breaker`, `ultimo_punto_de_ruptura`, `zonas_de_control` | el doji corta la racha, no es contraria y no forma pivote | el doji NO corta la racha, sigue sin ser contraria y sin formar pivote, y NO entra en el extremo (V, doji, R → ALTO en el máximo de la verde) |
| `bloque_de_origen` (:134) | el doji no es contraria: el impulso lo salta | igual (no cambia) |
| `zonas_de_control`, `primer_impulso` (:150) | busca la primera vela del color de la entrada: salta dojis | igual; cambia solo por `pivotes_formados` |
| `extremo_de_la_caja` (:230-235) | R4/R1: la última contraria y el tramo de contrarias; el doji corta el tramo | no cambia (A-48 ABIERTA; con `r6`, el valor vigente, el 1 sale de `punto.marca`, que se mueve con el punto) |
| `_recorrer_zona_posterior` (:280-290) | el doji corta la racha a favor: la R siguiente no deja extremo | el doji se salta (no corta la racha, no entra en el extremo): NOTA en ADR-0061 §4, que ata esta zona «a la misma geometría de M1 que ya usa el breaker» |
| `_pasa` (:103-111) | no mira el color | no cambia |
| `sin_alternancia_literal` (`test_a21_series.py:131`, solo medida) | salta los dojis | igual |

Encaja consumidor por consumidor; ninguno obliga a PARADA. Lo que sí rompe: **herencia 3 del
auditor**, `test_orden_stop_pivote.py::test_son_las_funciones_de_r5_y_r6_de_caja_77`, que ata
`ultimo_punto_de_ruptura` a `pivote_de_ruptura` de `scripts/bloque_de_la_caja.py` sobre 60 series al
azar por lado (`Random(7)`, pasos de −6 a 6). Medido (`medir_r5_dojis.py`): las 120 series llevan
alguna vela sin cuerpo y el último punto cambiaría en 9 de ellas (1 en compra, 8 en venta): el
test fallará si el guion no cambia (decisión 2).

**0.b.6 La zona del punto trae el 1.** `zona_del_punto` (`zonas.py:359-408`) calcula `extremo` con
`extremo_de_la_caja` según `caja_bloque` y, con `caja_se_fija = en_cada_cierre_m1`, lo recalcula en
cada cierre y lo mete en la clave de la zona (:390-394): `se_desarrolla_en_el_lado_de_ruido` (:529)
y `toca_colocar_orden_limite` (:489) llaman a la MISMA función en el mismo instante y reciben la
misma `Zona`, así que el 1 que mira RN-005 es el 1 que llevará la orden. Sí, es ese.

**0.b.7 El último minuto sin el evento del límite.** `vence_vela_h4` da SÍ cuando
`fin − instante <= antelacion` (`primitivas.py:141-150`): medido con el registro real, SÍ en fin−1 y
en fin (el límite), NO en fin−2 y en fin+1. El evento del límite pertenece a la sesión siguiente
(`cableado._sesion`: `instante == hasta` cae en la sesión que acaba solo si ninguna empieza ahí;
con las dos velas H4 de la ventana, las 11 son `desde` de la segunda sesión y ahí
`abre_sesion_operativa` ya retira). Para expresar «[fin − antelación, fin)» sin cifra en la forma hay
dos caminos: un argumento nuevo en `vence_vela_h4` (un token, como `cual` en `se_da_esquema`) o un
predicado nuevo. Ensayado en el clon el predicado `en_el_ultimo_tramo_h4` (argumentos `[anclaje,
antelacion]`, fuente `reloj`, cita `ev-v16-002248-08e9600f`): la tercera rama del `cualquiera_de` de
RN-035 y el único predicado del `cuando` de RN-037 (gate, `prohibe: [abrir_operacion]`, cita
`ev-v16-002323-515b9da4`, parámetros `[anclaje_h4, cierre_h4_antelacion]`); `spec check` lo acepta
sin problema de precedencia ni de literal, y las tres guardias lo recorren sin ampliarse (son
bucles sobre todos los predicados, acciones, hechos y acumuladores: `spec/modelo.py:367-390`,
`:406-411`, `:859-877`). Medido también: un literal de tres palabras («Un minuto antes») NO pasa
`literal_coincide`; el de nueve sí. Quién coloca o reubica: la acción con `efecto: abrir_operacion`
es `colocar_orden_limite` (RN-015, `strategy_spec.yaml:421-435`); RN-011 solo dimensiona;
`reubicar_orden_limite` (RN-006) NO lleva `efecto` -cancela y RN-011 y RN-015 recolocan en el mismo
cierre-, así que la gate frena la recolocación y no la cancelación; con la tercera rama de RN-035
retirando en ese mismo minuto, no queda ninguna orden viva en [fin − antelación, fin). Las gates se
evalúan antes que los disparadores en cada vuelta del evento (`interprete.py:311-345`): por eso un
`prohibe` dentro de RN-035 (disparador) no vale sin cambiarla de clase, porque otro disparador
anterior en el desempate ya habría colocado antes de que RN-035 prohibiera.

**0.b.8 Las series S-10 y S-15 por los dos caminos** (`medir_b8_series.py`, compra, sobre `PREVIO`
y `TOMA` de `test_estructura_m1.py`; la liquidez de M15 del clon de datos puesta por ENCIMA de
todos los precios para que RN-005 no entre en la medida: en las series de A-21, con el BAJO tomado
en 1000, todos los puntos quedan por encima del nivel y RN-005 prohibiría; son series de geometría,
no de lado):

| Serie (tras la toma) | `detectar_esquema` desde la toma, tope 1 | frontera «desde el último punto formado antes del breaker» | frontera «desde el último alto más alto» | camino real (registro vigente: orden en el punto, `en_cada_cierre_m1`, RN-009 en cada cierre) |
|---|---|---|---|---|
| S-10 (a21): V, R, V, R, breaker V | None (2 zonas) | 0 zonas → esquema | 0 zonas → esquema | M1 0: coloca en el punto de la referencia (1120, caja 989); M1 2 (la R): punto nuevo 1041, 0 zonas, RN-009 NO → reubica; M1 3 (la V): la orden en 1041 SE LLENA. Entra ANTES de la alternancia |
| S-10b: V, R, V que no supera el alto anterior, R, breaker V | None (2 zonas) | 0 zonas → esquema | 1 zona → esquema | coloca en 1120; M1 2: reubica a 1041; M1 4 (la segunda R): punto 1036, 1 zona, RN-009 NO → reubica; M1 5 (el breaker): SE LLENA en 1036 |
| S-15: V, R, V, R sucio; V, V impulso; R punto nuevo (1061); R, R retroceso limpio; breaker V | None (3 zonas) | 0 zonas → esquema | 0 zonas → esquema | igual que S-10b: la orden del punto 1036 se llena en la V del impulso nuevo (M1 5), antes de que exista el punto nuevo |

Lo que esto dice: (1) **no existe una frontera de retroceso que deje S-10 sin esquema y dé esquema a
S-15**: toda frontera anclada en el último punto formado antes del breaker da esquema a S-10, porque
su cola (una R y el breaker) es un retroceso limpio de una vela, idéntico a la cola de S-15; lo
único que distingue a S-15 es lo que pasa ANTES de su último punto, y una frontera lo descarta por
definición. (2) **Por el camino real, S-10 ya entra**: la orden stop nace en el primer punto tras la
toma y se llena en la primera verde que lo pasa, antes de que la alternancia exista; RN-009 solo
muerde en el cierre en que hay que colocar o recolocar con dos o más zonas YA formadas desde la
toma (en estas series, nunca). `detectar_esquema` y el camino real no coinciden sobre S-10 misma.
Eso va con la pregunta de la sesión 6 (decisión 6).

**Otras medidas.** `test_kit.py` pasa en el repo real sobre el código de `main` (41 tests);
`test_pivotes_m15.py`, `test_a21_series.py`, `test_racha_perdidas.py`, `test_rn035_ventana_fin.py`,
`test_orden_stop_pivote.py`, `test_provisional_cuelga_de_abierta.py`, `test_registro.py` y
`test_embudo_77.py` pasan (106 tests). En el clon, con los parámetros nuevos escritos a mano
(`caja_lado_de_ruido` con fuente evidence bajo A-50; `liquidez_m15_mecha_que_vuelve` con
`consumido_por: [ADR-0084]` y un ADR-0084 vacío de ensayo), `test_registro.py` y
`test_provisional_cuelga_de_abierta.py` pasan (52 tests), `spec check` solo pide subir
`spec_version` y `knowledge validate` solo denuncia el ADR-0084 de ensayo contra el bloque
`ids-inexistentes` del encargo (lo esperado con un ADR que existe en el clon).

### 0.c El encargo frente al repo

El auditor del encargo (`auditor-encargo`, solo lectura) contrastó 79 afirmaciones: 65 correctas,
1 incorrecta y 13 con matiz, y 7 herencias que el encargo no recoge. Lo que cambia lo que se pide,
con lo medido encima:

| # | Hallazgo | Evidencia | Qué se hace |
|---|---|---|---|
| 1 | INCORRECTA, b.7: «qué acción coloca o reubica una orden (RN-011, RN-006)». Quien coloca es RN-015 (`colocar_orden_limite`, `efecto: abrir_operacion`); RN-011 dimensiona; RN-006 cancela y RN-011+RN-015 recolocan | `strategy_spec.yaml:421-435`, `:1327-1331`, RN-015 | la gate RN-037 prohíbe `abrir_operacion` (0.b.7) |
| 2 | Herencia 1: el parámetro provisional bajo A-35 lo prohíben ADR-0045 («no se sustituye por un parámetro provisional, porque es un mecanismo y no una cifra») y ADR-0054 («(2) es un mecanismo inventado … ADR-0045 lo prohibió para A-35»); lo repiten `ambiguedades.yaml:979-981` y RN-004 (`:1194-1195`). El precedente `perdida_trader_magnitud` llevó NOTA en ADR-0054 §1 | ADR-0045:21; ADR-0054:93, :103-104 | decisión 0 |
| 3 | Herencia 2: `caja_lado_de_ruido` sin lector para `comprobar_consumo` (lector = argumento de una forma, no la lista `parametros`; `modelo.py:761-791`, `:817-822`) y sin ADR para la lectura del consultor; el comentario de A-50 dice que «el motor no cambia hasta la respuesta» | `modelo.py`; `ambiguedades.yaml:1549-1551` | decisión 4 (ensayado: el argumento en la forma de RN-005 lo arregla) |
| 4 | Herencia 3: `test_son_las_funciones_de_r5_y_r6_de_caja_77` y `scripts/bloque_de_la_caja.py` (0.b.5) | `test_orden_stop_pivote.py:128-151` | decisión 2 |
| 5 | Herencia 4: el heredado 35 («RN-020 tampoco retira la orden pendiente … el modelo es RN-036») vive en `docs/runbooks/ACTIVAR-A35-A44.md` §5.1 (:245-247), fuera del contrato, y en la nota de RN-020 (`:1956-1957`) | runbook; RN-020 | decisión 7: ampliar el contrato al runbook para una NOTA, como hizo la rama anterior |
| 6 | Herencia 5: ADR-0060 §6, primera viñeta («RN-002 … no retira órdenes; A-39 sigue ABIERTA … `retirar_orden_limite` sin regla que la use») también queda enmendada por el punto 6; el encargo solo pide recuadro en §5 | ADR-0060:90-92 | recuadro también en §6 (lo digo aquí; no cambia la decisión) |
| 7 | Herencia 6: más tests dependen de `nunca` (`test_racha_perdidas.py:79`, `:293-300`); y `test_las_opciones_sin_contrato_se_niegan` NO congela `nunca`: comprueba que `fin_de_dia` se rechaza | `test_racha_perdidas.py` | se cambian los que dependen del valor y se dice cuáles (0.a, punto 5) |
| 8 | Herencia 7: el nivel también lo consume `zonas.py:200` (`_anotar_toma`), con la identidad del pivote | `zonas.py:186-210`, `:289` | 0.b.4: el nivel se congela al tomarse |
| 9 | Matiz 25: la lista de la sesión 6 (§3, 2) solo pregunta el caso (i) y el bajo, no el (ii) | `ACTIVAR-SESION-05.md:1001-1005` | la línea R4.2 del cierre lo añade |
| 10 | Matiz 39 y 43: el CONFIRM cuenta como confirmación solo sin `--valor`; un CORRECT sobre evidencia sale siempre como «(?) sin mecanismo»; `main` ya lista dos CORRECT sobre RN-003 | `cli.py:2049-2075` | 0.b.1: «limpio» = sin pendientes nuevos |
| 11 | Matiz 66: `test_a21_series.py` ya tiene las filas de S-20 | `:86-89`, `:97-99` | no se añade ninguna |
| 12 | Matiz 69: `ev-v16-001445-7ca4f033` es un ítem de S-20 (sus notas y la extracción); usarlo para S-15 es lectura del consultor | el ítem; `SESION-05-EXTRACCION.md:936-939` | se dice así en el informe y en la lista de la sesión 6 |
| 13 | Matiz 72: `test_orden_stop_pivote.py:132` también carga `scripts/bloque_de_la_caja.py` | — | el punto 10 lo tiene en cuenta (solo importa; no ejecuta `main`) |
| 14 | Matiz 78: en la rama, `PROJECT_STATE.md` ya mide 23.013 bytes (la línea de Current Feature); los 23.000 son orden del consultor, el tope del test 25.000 | `test_project_state.py:21` | el cierre lo deja por debajo, medido con `wc -c` |
| 15 | Matiz 56: ver 7. Matiz 18: `orden_nace_en_el_punto` es una función que lee `orden_limite_nace` | `zonas.py:354` | nada |

El informe del auditor entero queda en la carpeta de trabajo de la sesión y no se copia: lo que
cambia algo está en esta tabla.

### 0.d Lo que no pude medir

- La frontera de S-15 con el cableado ENTERO (ticks y broker): se midió con los predicados reales
  de `engine/zonas.py` sobre M1 sintéticas y el llenado juzgado por la máxima de la M1, no por ticks.
  El resultado no depende de eso: la orden está colocada antes de que la alternancia exista.
- `ventana_no_citable` a nivel de segmento (0.b.2): necesita la cruda.
- `pytest` sobre `tests/unit/test_kit.py` DESDE EL CLON: la guardia de Claude Code lo negó dos veces
  («el codigo nombra la carpeta /, que contiene material protegido»), con ruta relativa y con ruta
  absoluta del clon; en el repo real el mismo comando corre. No se rodeó: se midió en el repo real
  (0.b, «Otras medidas»). Queda dicho para la rama de la guardia.
- Un `pytest` del clon que encadenaba `spec manifest --escribir` y `spec check` en una llamada lo
  negó la guardia (dos ejecuciones en el mismo comando): se partió en dos llamadas.

### 0.e Exposiciones

Ninguna. Nada de esta fase 0 leyó `data/`, `corpus/`, un libro, un caso, una filtrada, una cruda
ni un fotograma: velas sintéticas, la spec, el motor y los tests; el clon se creó sin `data/` ni
`corpus/` y su `knowledge validate` solo avisó de que no están. No se añade fila a
`HOLDOUT-EXPOSICIONES.md`. Estado del repo antes y después del clon: `git status --short` vacío,
`git branch --list` = `main` y la rama, 139 tags; `git worktree list` sin `C:/cm/motor` al terminar
(queda un worktree ajeno a esta sesión, `…/scratchpad/wt-ci`, en `detached HEAD` e7df30b, que ya
estaba antes y no se toca).

## Lo que necesito que decidas

0. **El parámetro provisional bajo A-35 contra ADR-0045 y ADR-0054.** Opciones: (a) ADR-0084
   enmienda ADR-0045 en esa frase (recuadro en su Decisión y fila del índice) y lleva NOTA en
   ADR-0054 («Por qué descartamos las demás», (2)), como hizo `perdida_trader_magnitud` en ADR-0054
   §1; y las dos notas que repiten la prohibición (A-35 en `ambiguedades.yaml`, RN-004) dicen que
   desde ADR-0084 el parámetro existe por decisión del consultor; (b) sin parámetro: `cualquier_mecha`
   fijo en el código y declarado en ADR-0084, y la sesión 6 decide; (c) parar hasta la sesión 6.
   Recomiendo (a): es el precedente de A-44 y lo que pide tu punto 1; (b) deja un mecanismo sin
   puerta en el registro (ADR-0002) y (c) deja el motor sin lo que sí dijo el trader.
1. **El caso (ii) frente a `ev-v10-012456` («no cuenta, lo tiene que pasar con cuerpo»).** Medido:
   hoy una mecha sobre un pivote formado no hace NADA (ni toma ni mueve); con (ii) MUEVE el nivel.
   El ítem de v10 responde a «¿qué haces?» con «no tiene … lo tiene que pasar con cuerpo» (no es
   toma) y el de v15 con «se actualiza el de la mecha». Opciones: (a) mantener `cualquier_mecha`
   y que ADR-0084 escriba la tensión: v10 dice cuándo queda TOMADO y v15 qué alto se usa después,
   con la sesión 6 preguntando (i) o (ii); (b) valor `solo_la_contraria`: (i) seguro y (ii) a la
   sesión 6, sin mover nada que v10 diga que no cuenta. Recomiendo (a): es tu lectura, el ítem de
   v15 contesta literalmente a la pregunta «si después el precio lo supera un poco» (la de A-35),
   y el nivel se congela al tomarse (0.b.4), que es lo que hace compatibles los dos ítems. Coste
   de (b): el motor hace menos de lo que el trader dijo. En los dos casos, la implementación es la
   de 0.b.4 (el nivel se mueve solo mientras no está tomado y se para en la primera M1 que lo cruza
   con el criterio): dilo si no es lo que quieres.
2. **`test_son_las_funciones_de_r5_y_r6_de_caja_77` (9 de 120 series cambian).** Opciones: (a) el
   test compara el productor con el guion de CAJA-77 solo sobre las series SIN velas sin cuerpo y
   añade que en las que las llevan la única diferencia es el punto de ADR-0085 (el guion sigue
   reproduciendo `CAJA-77.md`); (b) el guion gana la misma regla (deja de reproducir lo que
   `CAJA-77.md` midió); (c) retirar el test. Recomiendo (a): mide lo mismo y deja escrita la
   diferencia. Coste de (b): un guion de medida que ya no da sus propias cifras.
3. **La condición de `ev-v15-004037` («venga de un flujo bajista y después rompa cerrando por
   debajo»).** Medido: el motor forma el punto (el ALTO de M1) con cualquier roja que cierra tras
   una racha verde, sin exigir un flujo previo ni que cierre por debajo del mínimo de la verde;
   exigir «cerrar por debajo» es pedir cuerpo en M1 (A-32 RESUELTA: en M1 la mecha siempre vale).
   Opciones: (a) no se aplica, ADR-0085 lo dice y va a la lista de la sesión 6; (b) aplicarla como
   «la roja cierra por debajo del mínimo de la verde». Recomiendo (a), que es lo que tu punto 2
   prevé. Coste de (b): un criterio de cuerpo en M1 contra A-32.
4. **El lector y el sitio de la lectura de `caja_lado_de_ruido`.** Opciones: (a) la forma de RN-005
   gana el argumento `caja: caja_lado_de_ruido` (y el vocabulario de
   `se_desarrolla_en_el_lado_de_ruido`, `argumentos: [que, sentido, caja]`), sin ADR: la LECTURA DEL
   CONSULTOR va en la descripción del parámetro, en las notas de RN-005, en la nota de A-50 (su
   comentario «el motor no cambia hasta la respuesta» se corrige) y en el informe; (b) lo mismo, y
   además ADR-0087 (libre si S-15 va a la sesión 6) con la lectura y el mecanismo. Recomiendo (a):
   es lo ensayado y `spec check` lo acepta; un ADR para un enum de dos valores bajo una ambigüedad
   abierta es más de lo que pide el precedente (`caja_bloque`, sin ADR propio). Coste de (b): un
   ADR más que enmendar cuando el trader conteste.
5. **La forma del último minuto.** Opciones: (a) predicado nuevo `en_el_ultimo_tramo_h4` (SÍ en
   [fin − `antelacion`, fin), NO en el límite), tercera rama de RN-035 y gate nueva RN-037 que
   prohíbe `abrir_operacion`, con `ev-v16-002248` como cita del predicado y de RN-035 (vía su
   CORRECT) y `ev-v16-002323` como cita de RN-037; (b) un argumento nuevo en `vence_vela_h4`
   (`limite: excluido`, un token) y las mismas reglas. Recomiendo (a): un predicado que vale en el
   límite y otro que no son dos cosas distintas con nombre, y ADR-0060 §5 sigue entero para RN-002.
   Coste de (b): un token de valor dentro de una forma. En los dos, RN-037 es gate y RN-035 no
   lleva `prohibe` (0.b.7); los recuadros van en ADR-0060 §5 y §6 y en ADR-0066 §4. El nombre del
   predicado lo decides tú si no te vale ese.
6. **S-15 va a la sesión 6, con lo que el camino real añade.** Opciones: (a) tu decisión tal cual
   (dos esquemas en M1: la alternancia dentro de un retroceso y un retroceso sucio seguido de un
   punto nuevo con su retroceso limpio; «¿en cuál entras?»), más un tercer dibujo con lo medido en
   0.b.8: la orden ya puesta en el primer punto y llenada por la verde del retroceso, antes de la
   alternancia, «¿esa entrada vale?»; (b) tu decisión sin el tercer dibujo. Recomiendo (a): es el
   caso en que `detectar_esquema` y el motor real ya no dicen lo mismo, y sin preguntarlo la
   sesión 6 no lo cierra. Sin registro y sin ADR-0087 en esta rama.
7. **Ampliar el contrato a `docs/runbooks/ACTIVAR-A35-A44.md`** para una NOTA al principio de §5.1
   (el heredado 35 queda hecho por ADR-0086), como hizo la rama anterior con su §1. Opciones:
   (a) sí; (b) no, y la línea R4.1 del cierre lo dice. Recomiendo (a): es donde R4.1 apunta.
8. **El orden de los commits.** Opciones: (a) 1; 2+3 juntos; 4; 5; 6; 8; 10+11 juntos (lo viejo y
   los recuadros, sin código ni spec); (b) cada punto en el suyo. Recomiendo (a): el 2 y el 3
   tocan las mismas notas de RN-007 y el mismo ADR-0085, y el 10 y el 11 no llevan código. El
   punto 7 no lleva commit (nada que añadir) y el 9 no lleva nada hasta la sesión 6.

Espero tu respuesta a la PARADA.

## Respuesta del consultor a la PARADA (2026-10-26)

Copiada tal cual:

> Modelo: Fable 5.1 · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA de trabajo/activar-sesion-05-motor (2026-10-26). Cópiala tal cual al final del encargo y del informe, en «Respuesta del consultor a la PARADA», con su fecha, y aplícala punto por punto (skill fase-cero). Si al aplicar algo lo medido lo contradice, PARADA 2.
>
> 0. (a). ADR-0084 enmienda ADR-0045 en la frase «no se sustituye por un parámetro provisional, porque es un mecanismo y no una cifra» (recuadro en su Decisión y fila del índice) y lleva NOTA en ADR-0054, «Por qué descartamos las demás», (2); las notas de A-35 en ambiguedades.yaml y de RN-004 lo dicen. El motivo va escrito en el ADR: la prohibición era contra un mecanismo inventado que se hiciera pasar por método del trader (ADR-0054, (2)), y este mecanismo lo dijo el trader (ev-v15-000553-9d95178a); el valor provisional solo elige su alcance, y es LECTURA DEL CONSULTOR. Corrige mi error, con su nombre: el encargo pidió un DEFAULT_AMBIGUOUS bajo A-35 sin leer ADR-0045 ni ADR-0054. Para la fila de ERRORES-RECURRENTES del cierre: antes de proponer un valor provisional bajo una ambigüedad, se lee el ADR que la abrió.
> 1. (a). cualquier_mecha, con la tensión escrita en ADR-0084: los dos ítems contestan a la misma pregunta («si después el precio lo supera un poco»); v10 dice que eso no es tomarlo y v15, qué nivel queda; el nivel se congela al tomarse, que es lo que los hace compatibles. La implementación de 0.b.4 es la que quiero: la función pura de pivotes_m15.py que lleva el nivel a la mecha más lejana de las M1 que lo pasan sin cruzarlo con el criterio y se para en la primera que lo cruza, aplicada por motor.liquidez_m15, y con la identidad de _toma_del_momento intacta. La línea R4.2 del cierre añade (ii) a la pregunta de la sesión 6 (tu matiz 9): «¿la mecha que mueve el alto es la de la vela contraria que lo forma, o también la de una vela posterior que lo pasa y vuelve?».
> 2. (a). El test compara solo sobre las series sin velas sin cuerpo y añade otro que exige que, en las que las llevan, la única diferencia sea el punto de ADR-0085. El guion de CAJA-77 no se toca.
> 3. (a). No se aplica; ADR-0085 lo dice (pedirlo sería romper con cuerpo en M1, contra A-32 RESUELTA) y va a la lista de la sesión 6.
> 4. (a). Argumento caja: caja_lado_de_ruido en la forma de RN-005 y en el vocabulario de se_desarrolla_en_el_lado_de_ruido, sin ADR; la lectura del consultor va en la descripción del parámetro, en las notas de RN-005, en la nota de A-50 (se corrige «el motor no cambia hasta la respuesta») y en el informe.
> 5. (a). El predicado en_el_ultimo_tramo_h4 me vale. Tercera rama de RN-035, gate RN-037 sobre abrir_operacion y RN-035 sin prohibe. Recuadros en ADR-0060 §5 y §6 y en ADR-0066 §4, con sus filas del índice. Los literales, de nueve palabras o más, como mediste. Tests de que la orden se retira en el último minuto y de que en el primer cierre de la sesión de las 11 se puede colocar.
> 6. (a), con el tercer dibujo. Además, como lo medido en 0.b.8 dice que la serie S-10 ya entra por el camino real y ADR-0076 §2 la midió con detectar_esquema, va una NOTA en ADR-0076 §2 (en el commit de ADR-0085, que ya lo enmienda) con lo medido, y una línea para el cierre: que la re-corrida mire las entradas que nacen en el primer punto tras la toma y se llenan antes de la alternancia. Sin registro y sin ADR-0087.
> 7. (a). Contrato ampliado a docs/runbooks/ACTIVAR-A35-A44.md, con una NOTA al principio de §5.1 (el heredado 35, hecho por ADR-0086); el cuerpo no se toca.
> 8. (a). Orden de los commits: 1; 2+3; 4; 5; 6; 8; 10+11.
>
> Además:
> 9. ADR-0087 no se crea en esta rama y se queda en los bloques ids-inexistentes del encargo y del informe. Línea para Technical Debt en el cierre: la rama que cree ADR-0087 lo saca de esos dos bloques, o knowledge validate falla.
> 10. Para la fila de ERRORES-RECURRENTES del cierre, también estos errores del consultor: el encargo daba RN-011 como la regla que coloca (es RN-015), y el auditor del consultor buscó sobre la raíz de un clon (ya declarado en la apertura).
> 11. Las dos negativas de la guardia de §0.d (pytest de test_kit.py desde el clon de C:/cm/ y las dos ejecuciones encadenadas) van a las líneas del cierre, en K, junto a la de los tests del clon que ya tiene G.1.
>
> Sigue lo que manda el encargo: un commit por grupo, con el paso 3 de activar-sesion, knowledge validate antes de make check y Fuente: en el cuerpo con ids que existen; CI de Linux por fix/activar-sesion-05-motor con su número de run (gh run view suelto); revisor (opus) con los cinco alcances del encargo y su informe pegado al final; y las líneas del cierre con PROJECT_STATE medido con wc -c, por debajo de 23.000 en neto. Si el clasificador niega un push o la guardia un make, dame el comando exacto y lo lanzo yo con «!».
>
> Rama lista para revisión, NO cerrada.

## 1. La respuesta aplicada, commit a commit

### 1.1 Punto 1 · A-35, la mecha que vuelve (`liquidez_m15_mecha_que_vuelve`, ADR-0084; decisiones 0 y 1)

- **ADR-0084** (`docs/adr/0084-la-mecha-que-pasa-el-nivel-de-m15-y-vuelve-lo-mueve.md`): el
  mecanismo (los casos (i) y (ii), el nivel congelado al tomarse, el espejo en el bajo como
  DECISIÓN DEL CONSULTOR, solo M15), el selector como LECTURA DEL CONSULTOR bajo A-35 y sin
  registro, por qué enmienda ADR-0045 (recuadro en su Decisión y fila del índice) con NOTA en
  ADR-0054 «Por qué descartamos las demás» (2) y su fila, el contraste con `ev-v10-012456`
  (compatible: cuándo queda TOMADO frente a qué nivel se usa) y con `ev-v10-020142` y ADR-0062
  (la ruptura que habilita sigue pidiendo cuerpo), y el error del consultor con su nombre. Sale
  de los dos bloques `ids-inexistentes`.
- **Registro:** `liquidez_m15_mecha_que_vuelve`, `estrategia`, enum `[no_mueve, solo_la_contraria,
  cualquier_mecha]`, DEFAULT_AMBIGUOUS en `cualquier_mecha`, `ambiguedad_id: A-35`, fuente
  evidence `ev-v15-000553-9d95178a`, `consumido_por: [ADR-0084]`; su descripción dice que es
  lectura del consultor y por qué no lleva registro. A-35 en `ambiguedades.yaml`: la pregunta y el
  comentario lo dicen, `parametros` gana el nuevo. RN-004: sus notas. `spec_version` 18.1.9 →
  18.2.0 (un parámetro nuevo); `spec manifest --escribir` y `spec docs --escribir`
  (`docs/spec/ambiguedades.md`, `parametros.md`, `reglas.md`, `glosario.md`). Sin registro de
  feedback: `feedback apply --check` no tiene nada que proponer aquí y no se ejecutó.
- **Código:** `domain/pivotes_m15.py` (`_pivote_de` con la mecha de la contraria, el argumento
  `mecha_que_vuelve` de `pivotes_formados` y `pivote_mas_reciente` con `no_mueve` por defecto,
  `nivel_con_mecha_que_vuelve`, la docstring que ya no deja la mecha «fija y visible»);
  `engine/motor.py` (`DatosMercado` recibe `mecha_que_vuelve` y `criterio_toma`, con lo de siempre
  por defecto, y `liquidez_m15` aplica (i) por el selector y (ii) con las M1 desde `formado_en`
  hasta el instante); `engine/arnes.py` y `engine/visor.py` los leen del registro por su nombre.
  `domain/estructura_m1.py` no cambia: sus tres llamadores no piden ninguna mecha.
- **Tests:** `tests/unit/test_pivotes_m15.py`:
  `test_lo_fijo_y_visible_doji_y_mecha_de_la_contraria` se parte en
  `test_lo_fijo_y_visible_el_doji_corta_la_racha` (no cambia) y
  `test_la_mecha_de_la_contraria_mueve_el_nivel_segun_el_selector`, que CAMBIA DE SENTIDO A
  PROPÓSITO (la mecha 140 de la contraria daba 134; con `solo_la_contraria` y `cualquier_mecha` da
  140, y 90 en el bajo; con `no_mueve` y sin pedir nada, 134); `test_las_mechas_posteriores_mueven_el_nivel_y_la_toma_lo_congela`
  (dos mechas seguidas mueven dos veces: 137, 138; la M1 que cierra sobre el nivel viejo y no sobre
  el movido no es toma; la que cruza congela; con `mecha` como criterio la primera ya es toma),
  `test_el_caso_ii_en_un_bajo_en_espejo` y `test_una_mecha_fuera_del_selector_se_niega`.
  `tests/unit/test_mecha_que_vuelve.py` (nuevo), por el camino real: `DatosMercado.liquidez_m15`
  con el registro vigente y `alcanza_nivel`/`cruza` de `primitivas_escritas` (niveles 137, 138,
  138 en tres cierres; `cruza` NO en la M1 que cierra en 136 y SÍ en la que cierra en 141; la
  anotación `liquidez_m15` de la traza lleva el nivel movido; tras la toma una mecha a 150 no mueve
  nada); cada opción del selector por ese camino (134 / 140 / 141); un valor fuera del enum falla al
  leer el registro y `DatosMercado` lo rechaza; y las series de M1 no se mueven (la contraria de M1
  con mecha 1130 deja la referencia y el punto en 1120). **Con el código de `main`** (clon
  `C:/cm/main`, `git worktree add --detach … main`, los dos ficheros copiados dentro): los dos
  módulos no se recogen, `ImportError: cannot import name 'CUALQUIER_MECHA' from
  'botsito.domain.pivotes_m15'`; y lo que `main` hace con esas velas está medido en §0.a (punto 1)
  y §0.b.4: la contraria con mecha 140 deja el nivel en 134 y una M15 o M1 posterior con mecha
  tampoco lo mueve. **Con el de la rama:** 71 tests en verde entre `test_pivotes_m15.py`,
  `test_mecha_que_vuelve.py`, `test_estructura_m1.py`, `test_a21_series.py`, `test_preparar_a35.py`
  y `test_orden_stop_pivote.py`.
- **`test_kit.py` no cambia**: los conjuntos de RESUELTAS y de bloqueantes ABIERTAS (A-35 y A-44)
  son los mismos; A-35 sigue ABIERTA.
- **Trailer:** `Fuente: ev-v15-000553-9d95178a, ADR-0084`. Commit 35211a0.
- **Tres pasadas de `make check`**: la primera cayó en lint (nueve líneas largas), la segunda en
  mypy (`Pivote | None` sin comprobar en el test); desde entonces, antes de cada `make check`,
  `ruff format`, `ruff check` y `mypy` sobre los ficheros tocados (segundos frente a los 18
  minutos de la suite). Para ERRORES-RECURRENTES en el cierre.

### 1.2 Puntos 2 y 3 · Las velas sin cuerpo en M1 y RN-007 con umbral cero (ADR-0085; decisiones 2, 3 y 6)

En un commit, como se dijo en §0.a: el código es el de ADR-0085 y las notas de RN-007 se escriben
una vez.

- **ADR-0085** (`docs/adr/0085-la-vela-sin-cuerpo-en-m1-no-corta-la-racha-ni-cuenta-como-alternancia.md`):
  los cuatro ítems, el cambio solo en M1 y solo con cuerpo cero (dónde y qué no cambia), las tres
  DECISIONES DEL CONSULTOR (las mechas de la vela sin cuerpo siguen contando donde cuentan; la
  vela de 1 o 2 puntos sigue siendo de su color; la condición de `ev-v15-004037` no se aplica
  porque pediría cuerpo en M1 contra A-32 RESUELTA), que enmienda ADR-0076 en su cabecera y en
  la fila del doji de §2 (recuadros y fila del índice) con la NOTA de lo medido en §0.b.8 sobre
  S-10 por el camino real (decisión 6), y la NOTA en ADR-0061 §4 (fila del índice). Sale de los
  dos bloques `ids-inexistentes`.
- **Registros** (los mismos que en el clon de la fase 0, con los mismos ids):
  `fb-2026-10-23-sesion-05-72c9a9e8`, CONFIRM sobre RN-007 sin valor (v15,
  `ev-v15-003959-5898c61e`, 0:39:59-0:40:29, recibido el 10-23);
  `fb-2026-10-23-sesion-05-a9e4f879`, CORRECT sobre `ev-v10-014310-2296423b` con valor «una vela
  casi plana tiene que ser de cero puntos de cuerpo, plana totalmente» (v16,
  `ev-v16-002841-8cfe382a`, 0:28:41-0:29:02, recibido el 10-25). `feedback apply --check`: «3
  parametros; 0 cambian, 3 ya estaban» (ninguno fija un parámetro; no se aplicó nada).
  `feedback pending`: el CONFIRM en `(=)` («confirma la regla vigente RN-007»), el CORRECT en `(?)`
  («sin forma mecanica de cruzarlo», como `a42c72dd`), y los pendientes siguen siendo los dos
  CORRECT sobre RN-003 de `main`. S-19 sin registro (su ítem mete en el mismo saco las velas de
  uno o dos puntos).
- **RN-007**: sus notas dejan de decir «DESALINEADO CON EL MOTOR» y dicen que casi plana es cuerpo
  cero desde `a9e4f879`, que el motor lo hace en M1 por ADR-0085 y que las mechas de una vela sin
  cuerpo y las velas de 1 o 2 puntos van a la sesión 6; su literal y su cita no cambian, y su
  forma no necesita predicado nuevo (`color() == 0` ya es la definición). `spec_version` 18.2.0 →
  18.2.1 (redacción); `spec manifest --escribir`, `spec docs --escribir`.
- **Código:** `domain/pivotes_m15.py` (`sin_cuerpo` en `_racha_anterior`, `_pivote_en`,
  `_pivote_en_curso`, `pivotes_formados` y `pivote_mas_reciente`, con `corta_la_racha` por
  defecto: M15 no se mueve); `domain/estructura_m1.py` (`_pivotes_m1`, que piden `no_cuenta`, en
  `referencia_del_breaker`, `zonas_de_control` y `ultimo_punto_de_ruptura`;
  `_recorrer_zona_posterior` salta la vela de cuerpo cero). `bloque_de_origen`,
  `extremo_de_la_caja` y `_pasa` no cambian (§0.b.5).
- **Tests.** `tests/unit/test_velas_sin_cuerpo_m1.py` (nuevo): V, sin cuerpo, R da el punto en el
  máximo de la verde, en compra y en venta, con una y con tres velas sin cuerpo (y la vela que
  marca el nivel es la verde, no la sin cuerpo con mecha más alta); R, sin cuerpo, V, R da lo
  mismo que R, V, R (dos zonas, ningún esquema); una vela de 1 punto sigue contando como color
  (forma el punto y alterna en el retroceso); la zona posterior salta la vela sin cuerpo (mismo
  extremo que sin ella); por el camino real, `toca_colocar_orden_limite` con el registro vigente
  liga la zona del BAJO que la vela sin cuerpo cortaba (R, R, sin cuerpo, V en una venta); las
  series de M15 no se mueven (solo `no_cuenta` daría el pivote, y un valor fuera de las dos
  lecturas se niega). CAMBIAN DE SENTIDO A PROPÓSITO: la fila del doji de
  `tests/unit/test_a21_series.py` (de segundo esquema con 1 zona y DISTINTO a ninguno con 2 e
  igual que la lectura literal) y `test_las_diferencias_son_solo_el_doji_y_el_breaker_por_mecha`
  (queda solo el breaker por mecha; el nombre se conserva) con su docstring;
  `tests/unit/test_orden_stop_pivote.py::test_son_las_funciones_de_r5_y_r6_de_caja_77` compara con
  el guion de CAJA-77 sobre las series al azar con cada vela sin cuerpo convertida en una verde de
  un punto (el guion no se toca), y el test nuevo
  `test_en_las_series_con_velas_sin_cuerpo_la_unica_diferencia_es_el_punto_de_adr_0085` exige
  que, con ellas, el punto del productor sea el que el guion da sobre la misma serie sin esas
  velas (decisión 2). **Con el código de `main`** (clon `C:/cm/main`): `test_velas_sin_cuerpo_m1.py`
  no se recoge (`ImportError: cannot import name 'SIN_CUERPO_CORTA'`), y los dos ficheros
  cambiados, corridos aparte, fallan en lo que cambia a propósito: `FAILED
  test_la_tabla_de_series_de_a21[compra-alternancia con cuerpo cero en medio …]`, el mismo en
  venta, y `FAILED test_en_las_series_con_velas_sin_cuerpo_la_unica_diferencia_es_el_punto_de_adr_0085`
  en venta y en compra (`test_las_diferencias…` lee la columna `igual` de la tabla y pasa en los
  dos lados: es la fila la que falla en `main`). **Con el de la rama:** 108 tests en verde entre `test_velas_sin_cuerpo_m1.py`, `test_a21_series.py`,
  `test_orden_stop_pivote.py`, `test_pivotes_m15.py`, `test_estructura_m1.py`,
  `test_mecha_que_vuelve.py`, `test_be_al_tick.py`, `test_preparar_a21.py`,
  `test_caja_hasta_el_llenado.py`, `test_punto_usado.py` y `test_embudo_77.py`.
- **`test_kit.py` no cambia**; A-21 sigue RESUELTA como la deja ADR-0076; ninguna ambigüedad se
  cierra.
- **Trailer:** `Fuente: fb-2026-10-23-sesion-05-72c9a9e8, fb-2026-10-23-sesion-05-a9e4f879,
  ev-v15-003959-5898c61e, ev-v15-004037-a2ab3980, ev-v16-000851-f5ae3b6f, ev-v16-002841-8cfe382a,
  ADR-0085`.

## Estado

EN CURSO. Fase 0 medida (commit 53b879a) y respuesta del consultor del 2026-10-26 recibida:
se aplica punto por punto, un commit por grupo (1; 2+3; 4; 5; 6; 8; 10+11). Hechos: el 1 y el 2+3.
