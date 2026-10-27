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
  con mecha 1130 deja la referencia y el punto en 1120). **Tras el revisor (b3), dos tests del
  cargador** en el mismo fichero: `arnes.dias_de_mercado` y `visor.Preparador.preparar`, con
  `buscar_manifiesto`, `cargar_manifiesto` y `cargar_serie` sustituidos por una serie sintética de
  2030 (nada toca `data/`) y, en el visor, un motor falso que se queda con el `DiaDeMercado` y
  corta antes de los stops del trader, comprueban que el `DatosMercado` que llega al motor lleva
  `mecha_que_vuelve` y `criterio_toma` iguales a `liquidez_m15_mecha_que_vuelve` y
  `liquidez_m15_criterio_toma` del registro (y la lectura de A-35 como hasta hoy); si `arnes.py` o
  `visor.py` no pasaran el selector, fallarían. **Con el código de `main`** (clon
  `C:/cm/main`, `git worktree add --detach … main`, los ficheros de hoy copiados dentro tras el
  revisor): los dos módulos no se recogen, `ImportError: cannot import name 'CUALQUIER_MECHA' from
  'botsito.domain.pivotes_m15'` (es un fallo de importación, no de comportamiento: lo que `main`
  hace con esas velas está medido en §0.a, punto 1, y §0.b.4: la contraria con mecha 140 deja el
  nivel en 134 y una M15 o M1 posterior con mecha tampoco lo mueve; y los dos del cargador, de
  importarse, fallarían en `main` con `AttributeError` porque su `DatosMercado` no tiene
  `mecha_que_vuelve`). **Con el de la rama:** 75 tests en verde entre `test_pivotes_m15.py`,
  `test_mecha_que_vuelve.py`, `test_estructura_m1.py`, `test_a21_series.py`, `test_preparar_a35.py`
  y `test_orden_stop_pivote.py` (`75 passed in 51.99s`).
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
  un punto (el cálculo del guion, R5 y R6, no se toca; cómo construye `Diagnostico` sí cambia en
  el punto 10, §1.7 y desviación (g) de §4), y el test nuevo
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
  ADR-0085`. Commit 225ac79 (puntos 2 y 3).

### 1.3 Punto 4 · A-50, la caja entera (`caja_lado_de_ruido`; decisión 4)

Sin ADR: la LECTURA DEL CONSULTOR va en la descripción del parámetro, en las notas de RN-005, en
la nota de A-50 y aquí. Commit 5b44cd6 (punto 4; hasta el revisor, a1, cada sección de §1 llevaba
el sha del commit anterior: corregidos los cinco).

- **Registro:** `caja_lado_de_ruido`, `estrategia`, enum `[solo_el_0, caja_entera]`,
  DEFAULT_AMBIGUOUS en `caja_entera`, `ambiguedad_id: A-50`, fuente evidence
  `ev-v15-010451-5b123278`, sin registro de feedback (precedente `caja_bloque`); su descripción
  dice qué dijo el trader (el 0 en la línea o por encima «es indiferente»; lo importante es validar
  el punto), que eso descarta mirar solo el 0, y que la caja ENTERA es lectura del consultor
  deducida de su ejemplo (§3.3 de la extracción, fuera del ítem). Lector: el argumento
  `caja: caja_lado_de_ruido` en la forma de RN-005 y en el vocabulario de
  `se_desarrolla_en_el_lado_de_ruido` (`argumentos: [que, sentido, caja]`, con su descripción),
  como se ensayó en §0.b (`comprobar_consumo` lo acepta). RN-005: `parametros` y sus notas. A-50
  en `ambiguedades.yaml`: la pregunta («RESPONDIDA EN PARTE … SIGUE ABIERTA»), el comentario
  (corregido «el motor no cambia hasta la respuesta»), `evidencia` gana el ítem y `parametros` el
  selector; `docs/runbooks/AMBIGUEDADES.md` leído antes. `spec_version` 18.2.1 → 18.3.0 (un
  parámetro nuevo); `spec manifest --escribir`, `spec docs --escribir`. `feedback apply --check`
  no tiene nada que proponer (sin registro).
- **Código:** `engine/zonas.py`, `se_desarrolla_en_el_lado_de_ruido` lee `caja` por su nombre: con
  `solo_el_0`, lo de siempre (la entrada); con `caja_entera`, ruido solo si el 0 Y el 1 (el
  `extremo` de la zona del punto, el mismo que llevará la orden, §0.b.6) quedan del lado de
  ruido; una lectura fuera de las dos se niega con nombre. El 0 justo en la línea sigue sin ser
  ruido con ninguna (estricto, como antes).
- **Tests.** `tests/unit/test_caja_lado_de_ruido.py` (nuevo), por el camino real
  (`primitivas_zona` con el registro y `zona_del_punto`), en compra y en venta: la caja a caballo
  (el 0 del lado de ruido, el 1 no) NO es ruido con `caja_entera` y SÍ con `solo_el_0`; la caja
  entera del lado de ruido es ruido con las dos; el 0 justo en la línea no lo es con ninguna; el
  registro real trae el valor como DEFAULT_AMBIGUOUS bajo A-50 con su fuente, y un valor fuera
  del enum falla al leer el registro. `test_spec_fidelidad.py::test_rn005_prohibe_el_lado_de_ruido_y_no_el_de_la_operativa`
  CAMBIA DE SENTIDO A PROPÓSITO en la invocación exacta (gana `caja`; los dos argumentos de
  siempre, iguales). `test_orden_stop_pivote._registro` conoce el parámetro nuevo (para pedir
  `solo_el_0` sobre el registro real). `test_registro.py` y
  `test_provisional_cuelga_de_abierta.py` pasan con el valor de fuente evidence (lo que el encargo
  pedía verificar). **Con el código de `main`** (clon `C:/cm/main`): los siete tests del fichero
  nuevo (cuatro funciones, dos de ellas en compra y en venta) fallan, `ParametroDesconocidoError:
  parametro no registrado: caja_lado_de_ruido` y `AssertionError: caja_lado_de_ruido` (la línea
  del valor no existe en su registro): fallan por el registro, no por el comportamiento, porque
  `main` no tiene el parámetro con el que se le pide la lectura; lo que `main` hace con la caja a
  caballo (solo el 0) está medido en §0.a, punto 4 (revisor, b3). **Con el de
  la rama:** 197 tests en verde entre `test_caja_lado_de_ruido.py`, `test_spec_fidelidad.py`,
  `test_spec.py`, `test_orden_stop_pivote.py`, `test_preparar_a21.py`, `test_huecos_motor.py`,
  `test_cableado.py`, `test_registro.py` y `test_provisional_cuelga_de_abierta.py`.
- **`test_kit.py` no cambia**; A-50 sigue ABIERTA (no bloqueante, como estaba).
- **Trailer:** `Fuente: ev-v15-010451-5b123278`.

### 1.4 Punto 5 · S-21, la racha tras la detención (`racha_perdidas_reinicio` = `tras_la_detencion`; decisión 5)

Commit dd2042f (punto 5); el arreglo del revisor (b4), en el commit del cierre de este informe.

- **Registro:** `fb-2026-10-23-sesion-05-978be13f`, CORRECT sobre el parámetro
  `racha_perdidas_reinicio` con valor `tras_la_detencion` y `--supersede
  fb-2026-10-04-sesion-04-d1792021` (el RESOLVE_UNKNOWN de la sesión 4, valor `nunca`; sin el
  supersede seguiría vivo sin que el parámetro lo cite); v16, `ev-v16-002126-d2376f71`,
  0:21:26-0:21:35, recibido el 10-25; mismo id que en el clon de la fase 0. La opción
  `tras_la_detencion` entra en el enum ANTES del `apply` (si no, el registro se rechaza).
  `feedback apply --check`: «4 parametros; 1 cambian, 3 ya estaban», SOLO este; `feedback apply`
  deja el parámetro CONFIRMED en `tras_la_detencion` citando el registro; `feedback pending`
  sigue con los dos CORRECT sobre RN-003 de `main` y nada nuevo. A-51 sigue RESUELTA y sin
  REOPEN: lo que cambia es la lectura que ADR-0077 §5 declaraba provisional (recuadro allí y fila
  del índice). La descripción del parámetro dice las dos cosas (la sesión 4 con su reserva: la
  línea mezcla la lectura del consultor y la respuesta). RN-036: su `entonces` («con la racha en
  cero») y sus notas; lo que cuenta y cuándo detiene no cambia. `spec_version` 18.3.0 → 18.3.1
  (un valor y una redacción); `spec manifest --escribir`, `spec docs --escribir`.
- **Código:** `engine/racha.py`: `SeguidorRacha` admite `tras_la_detencion` junto a `nunca` (las
  otras dos siguen sin contrato); `detenido` anota el día operativo en que ve la detención
  (`detenido_en`) y, con `tras_la_detencion`, al llegar un día posterior -al consultar o al
  registrar un cierre- pone la racha a cero (`_reiniciar_si_toca`). Con `nunca`, lo de antes. La
  docstring del módulo lo cuenta. **Tras el revisor (b4):** la primera versión solo reiniciaba si
  `detenido` había visto la detención ese día; si la novena pérdida se registraba sin consulta
  posterior en su día (el cierre a mercado de fin de día del cableado, que se registra tras la
  última evaluación), al día siguiente la racha seguía en nueve y la décima volvía a detener,
  como con `nunca`. Ahora el seguidor recuerda el último tope con que se le consultó
  (`tope_visto`, que sigue nombrando la forma de RN-036: ninguna cifra) y `_detenida_antes_de`
  reinicia también cuando la racha está en ese tope o por encima y la pérdida que la dejó ahí cayó
  en un día anterior. Sin ninguna consulta nunca, el seguidor no conoce el tope y no reinicia (el
  cableado consulta en cada cierre de M1, así que ese caso no se da en él).
- **Tests** (`tests/unit/test_racha_perdidas.py`). CAMBIAN DE SENTIDO A PROPÓSITO:
  `test_los_cuatro_parametros_son_del_trader_y_estan_confirmados` (el reinicio es
  `tras_la_detencion` y cita el CORRECT), `test_nueve_perdidas_con_un_break_even_en_medio_detienen_hasta_el_dia_siguiente`
  (al día siguiente la racha es 0 y una pérdida más no detiene) y
  `test_el_cableado_detiene_el_noveno_dia_y_vuelve_a_operar_el_decimo` (el décimo día opera con la
  racha en cero, su pérdida es la primera de otra racha, RN-036 no dispara y el informe dice «1
  seguidas»). Nuevos: `test_el_reinicio_llega_aunque_nadie_consulte_despues_de_la_novena` (antes
  `…_entre_medias`, que consultaba `detenido` tras la novena y prometía más de lo que probaba,
  b4: ahora la novena se registra sin consulta posterior y el primer cierre del día siguiente
  cuenta desde cero, igual si lo primero del día siguiente es la consulta; y sin ninguna consulta
  nunca la racha sigue), `test_ocho_perdidas_cruzan_de_un_dia_a_otro_y_la_novena_detiene`
  (cinco y tres son ocho; la novena detiene su día; al siguiente, cero) y
  `test_con_nunca_la_racha_sigue_en_nueve_y_la_decima_vuelve_a_detener` (la lectura provisional
  de ADR-0077 §5 sigue teniendo contrato con `nunca`, probada con un seguidor hecho a mano).
  `test_las_opciones_sin_contrato_se_niegan` NO cambia: `fin_de_dia` se sigue negando. Un valor
  fuera del enum falla al leer el registro (`test_registro.py::test_enum_exige_opciones_y_el_valor_debe_estar_en_ellas`,
  que ya existía, lo cubre para todo enum). **Con el código de `main`** (clon `C:/cm/main`): cinco
  fallos, `AttributeError: module 'botsito.engine.racha' has no attribute
  'REINICIO_TRAS_LA_DETENCION'`, `'SeguidorRacha' object has no attribute 'detenido_en'`,
  `assert (10 == 1)` y `AssertionError: (10, datetime.date(2030, 1, 28))` en el cableado (el
  décimo día volvía a detener); con los tests de hoy, copiados de nuevo al clon tras el revisor
  (b3): `5 failed, 9 passed`, los mismos cinco. **Con el de la rama:** 88 tests en verde entre
  `test_racha_perdidas.py`, `test_cableado.py` y `test_registro.py`.
- **`test_kit.py` no cambia**: A-51 sigue en RESUELTAS.
- **Trailer:** `Fuente: fb-2026-10-23-sesion-05-978be13f, ev-v16-002126-d2376f71`.

### 1.5 Punto 6 · S-22, el último minuto (RN-035 y RN-037, `en_el_ultimo_tramo_h4`; decisión 5)

Commit 4855860 (punto 6; su primer `make check` salió en rojo por los dos tests de
`test_vida_de_la_orden.py`, corregidos en el mismo commit, abajo).

- **Registro:** `fb-2026-10-23-sesion-05-1526aa39`, CORRECT sobre RN-035 con valor «al llegar la
  hora de cerrar, la orden sin llenar se quita un minuto antes, igual que se cierra la operacion
  abierta» (v16, `ev-v16-002248-08e9600f`, 0:22:48-0:23:17, recibido el 10-25; mismo id que en
  el clon). `feedback apply --check` no tiene nada que proponer (ningún parámetro); `feedback
  pending` deja de listarlo en cuanto RN-035 lo cita, y quedan los dos CORRECT sobre RN-003 de
  `main`.
- **Spec.** Predicado nuevo `en_el_ultimo_tramo_h4` (`[anclaje, antelacion]`, fuente `reloj`,
  cita `ev-v16-002248-08e9600f`, literal de nueve palabras: «Si está abierta o todavía no se ha
  llenado la orden Un minuto antes»; tres de tres palabras no pasaban `literal_coincide`,
  §0.b.7): SÍ en [fin − `antelacion`, fin) de la vela H4 de la rejilla de `anclaje_h4`, NO en el
  límite, que ya es de la sesión siguiente. **RN-035**: título y `cuando` con la tercera rama,
  `cita` y `literal` del CORRECT, `parametros` gana `anclaje_h4` y `cierre_h4_antelacion`, la
  forma gana `en_el_ultimo_tramo_h4` como primera opción del `cualquiera_de` (las dos de antes se
  quedan como red), y las notas quitan que «un minuto antes» es frase del consultor y el HUECO,
  dicen que valer también a las 11 es LECTURA DEL CONSULTOR y remiten a RN-037 (la frase estaba
  dos veces en las notas; la segunda, en la RESERVA de la sesión 4, la vio el revisor, b1, y dice
  ahora que «un minuto antes» era entonces frase del consultor y en la sesión 5 lo dijo el
  trader). **RN-037**, gate
  nueva (la 32.ª vigente): `cuando` el mismo predicado, `prohibe: [abrir_operacion]` -el efecto de
  `colocar_orden_limite`, RN-015, que es quien coloca (el encargo decía RN-011; matiz del
  auditor)-, cita `ev-v16-002323-515b9da4` y literal de catorce palabras; sus notas dicen por qué
  es una gate aparte y no un `prohibe` en RN-035 (§0.b.7: las gates se evalúan antes que los
  disparadores), y ya no ponen entre «» la `afirmacion` del ítem como si fueran palabras del trader
  (revisor, a2: sus palabras son las del `literal`). Las tres guardias de `spec/modelo.py` no se amplían: ya recorren todos los
  predicados y reglas con cita (medido en el clon y aquí, `knowledge validate` en verde).
  `spec_version` 18.3.1 → 18.4.0 (una regla y un predicado nuevos); `spec manifest --escribir`,
  `spec docs --escribir`. Recuadros en ADR-0060 §5 y §6 y en ADR-0066 §4, con sus filas del
  índice.
- **Código:** `engine/primitivas.py`, `en_el_ultimo_tramo_h4` junto a `vence_vela_h4`, con la
  misma rejilla (`_fin_de_la_h4`) y `0 < fin − instante <= antelacion`. Nada más: la retirada es
  `retirar_orden_limite` (ya existía) y la prohibición la aplica el intérprete.
- **Tests.** `tests/unit/test_ultimo_minuto.py` (nuevo), por el cableado real con la spec y el
  registro vigentes, a las 11 y a las 3: la orden sin llenar se retira en el evento fin − 1 y no se
  llena aunque el BID baje en ese minuto (en `main` se llenaba: `assert 'llenada' ==
  'cancelada'`); una zona que aparece en fin − 1 no se coloca, con RN-037 en `disparadas` y
  `("RN-015", "accion:colocar_orden_limite", "prohibida:abrir_operacion")` en `bloqueadas` (en
  `main`, `'RN-037' in {...}` falla y la orden se colocaba); en el primer cierre de la sesión de
  las 11 sí se coloca (pasa también en `main`: es la guardia de que el límite no se toca; para
  ese test hizo falta un `toca_colocar_orden_limite` sintético SIN estado, porque el de
  `test_cableado` se consume al evaluarse y en una apertura el intérprete evalúa el `cuando` de
  RN-011 una vez más para avisar del empate con RN-003, ADR-0049 H3: se dice en su docstring);
  lo que se llena en el minuto anterior al último lo cierra RN-002 en el evento siguiente, fin − 1,
  en el que RN-035 ya no encuentra nada (ADR-0060 §5 entero para la posición; el encargo pedía
  ese test con lo que se llene «en ese minuto», el último, y en el último ya no puede llenarse
  nada porque RN-035 retira en su primer evento: hecho de otra forma, desviación (f) de §4); y la forma y el
  vocabulario (el predicado de reloj con sus dos argumentos, RN-037 gate, las citas). CAMBIAN DE
  SENTIDO A PROPÓSITO: `test_rn035_ventana_fin.py::test_hueco_la_orden_que_se_llena_en_el_ultimo_minuto_se_cierra_en_el_limite`
  (a las 11 y a las 3: la orden se retira en el último minuto y no se llena; el nombre se
  conserva) y `::test_rn035_retira_la_pendiente_a_ventana_fin_y_el_cableado_no_encuentra_nada` (la
  retirada es a 14:59, no a `ventana_fin`), y en `test_escenarios_por_sesion.py`
  `test_la_orden_viva_al_cambiar_de_sesion_segun_el_parametro[se_retira]` y
  `test_la_orden_viva_cuando_otra_toma_abre_un_escenario` (la orden de la mañana se retira a las
  10:59, no en la apertura de la tarde; RN-035 dispara en la sesión 07-11); y en
  `test_vida_de_la_orden.py` los dos de la pendiente cancelada (a ventana_fin y al abrir otra
  sesión), que el primer `make check` de este commit sacó en rojo: la cancelación cae un minuto
  antes y la fila del informe de órdenes la rotula «en el ultimo tramo de la vela H4»
  (`cableado._motivo_de_cancelacion` gana ese rótulo con `cierre_h4_antelacion` del registro, sin
  cifra). **Con el código de `main`** (clon `C:/cm/main`, con los tests de hoy copiados de nuevo
  tras el revisor, b3): esos cinco fallan como se ha dicho (`test_escenarios_por_sesion.py`: `4
  failed, 15 passed`, los dos de `…segun_el_parametro` y los dos de `…otra_toma_abre_un_escenario`,
  `assert 1894701599999 == (((31578360 - 1) * 60000) - 1)`) y en `test_ultimo_minuto.py` fallan
  cinco de siete (`5 failed, 2 passed`: los dos de la retirada, `assert 'llenada' ==
  'cancelada'`; los dos de RN-037, `assert 'RN-037' in {'RN-003', 'RN-011', 'RN-015'}`; y
  `KeyError: 'RN-037'` en el de la forma; pasan el del primer cierre de las 11 y el de RN-002).
  **Con el de la rama:** 279 tests en verde entre `test_ultimo_minuto.py`,
  `test_rn035_ventana_fin.py`, `test_escenarios_por_sesion.py`, `test_cableado.py`,
  `test_cierre_vela_h4.py`, `test_racha_perdidas.py`, `test_spec.py`, `test_spec_fidelidad.py`,
  `test_huecos_motor.py`, `test_sesiones_independientes.py`, `test_punto_usado.py`,
  `test_margen_lote.py`, `test_caja_hasta_el_llenado.py`, `test_orden_stop_pivote.py`,
  `test_be_al_tick.py`, `test_dos_relojes.py`, `test_preparar_a44.py` y `test_preparar_a21.py`.
- **`test_kit.py` no cambia**; ninguna ambigüedad se toca (A-30 y A-39 siguen RESUELTAS).
- **Trailer:** `Fuente: fb-2026-10-23-sesion-05-1526aa39, ev-v16-002248-08e9600f,
  ev-v16-002323-515b9da4`.

### 1.6 Puntos 8 y 7 · RN-020 retira la orden pendiente al llegar al tope (ADR-0086; decisiones 7 y 8)

Commit 7208db2 (punto 8 y el runbook del 7).

- **ADR-0086** (`docs/adr/0086-rn020-retira-la-orden-pendiente-al-llegar-al-tope.md`): DECISIÓN
  DEL CONSULTOR, sin ítem de evidencia, con el modelo y el motivo de RN-036 (ADR-0077 §3: el
  bróker la llenaría por ticks mientras el trader ya ha dejado de operar); enmienda ADR-0077 §3
  en «RN-020 no cambia» (recuadro allí y fila del índice); cierra el heredado 35. Sale de los dos
  bloques `ids-inexistentes`; queda solo ADR-0087 (decisión 9: no se crea en esta rama). Su §2
  cita «solo el del día y las 9 seguidas» con su id, `ev-v15-000856-ee8f7ba3` (el ítem que ya
  citaba RN-020 desde `trabajo/activar-sesion-05`, no de los que nombra el encargo; revisor, a2).
- **Spec.** RN-020: su `entonces` («y se retira la orden pendiente que quede»), la forma (`hace`
  gana `retirar_ordenes_pendientes: {}`, la acción de RN-036, sin argumentos e idempotente) y sus
  notas (en vez de «LO QUE ESTA REGLA SIGUE SIN HACER», que lo hace desde ADR-0086, por decisión
  del consultor y no por el trader). No lee nada más ni cambia lo que cuenta; `decision` sigue en
  ADR-0027 (el corte del día). `spec_version` 18.4.0 → 18.5.0 (una regla hace algo nuevo);
  `spec manifest --escribir`, `spec docs --escribir`. Sin registro: nada que aplicar.
- **Punto 7:** el contrato gana `docs/runbooks/ACTIVAR-A35-A44.md` (comentado en `contrato.yaml`;
  `contrato_rama.py` en verde con 49 ficheros) para la NOTA al principio de §5.1 (el heredado 35,
  hecho por ADR-0086; la re-corrida sigue pendiente); el cuerpo no se toca.
- **Código:** ninguno: la acción existe desde ADR-0077 (`primitivas_broker.py`).
- **Tests.** `tests/unit/test_rn020_retira_pendiente.py` (nuevo), por el cableado real y la spec
  real: una orden colocada en MINUTO_ZONA que no se llena y un acumulador `perdida_dia` SINTÉTICO
  (como los de `test_cableado`) que da SÍ desde un cierre posterior; RN-020 dispara en ese cierre,
  fija `detenido_por_tope`, la orden queda CANCELADA en ese mismo instante, las peticiones son
  colocar y cancelar, el cableado no encuentra nada al fin del día y RN-035 ya no tiene nada que
  retirar a las 10:59; y la forma de RN-020 lleva la acción de RN-036. **Con el código de `main`**
  (clon `C:/cm/main`): los dos fallan, `cancelada and 1894701599999 == ((31578245 * 60000) - 1)`
  (la orden seguía viva hasta que RN-035 la retiraba a las 11) y `{'retirar_ordenes_pendientes':
  {}} in [{'fijar': …}]` (la forma no la llevaba). **Con el de la rama:** 164 tests en verde entre
  `test_rn020_retira_pendiente.py`, `test_preparar_a44.py`, `test_cableado.py`, `test_spec.py`,
  `test_spec_fidelidad.py`, `test_huecos_motor.py`, `test_racha_perdidas.py` y
  `test_diferencias_por_operacion.py`.
- **`test_kit.py` no cambia**; A-44 sigue ABIERTA con sus parámetros como estaban.
- **Trailer:** `Fuente: ADR-0086`.

### 1.7 Puntos 10 y 11 · Lo viejo del final de §2 y los dos recuadros de corrección

Commit b18fe31 (puntos 10 y 11). Sin código del motor ni spec.

- **Punto 10.** `src/botsito/engine/broker.py:177`: el comentario de las opciones de
  `lote_si_no_cabe` deja de decir «DEFAULT_AMBIGUOUS bajo A-57» (A-57 está RESUELTA desde la
  sesión 5; CONFIRMED en `limitar`). Los tres guiones que construían `Diagnostico` con valores que
  hoy se rechazan: `scripts/embudo_77.py` y `scripts/caja_77_exploratoria.py` quitan `a35` y `a44`
  (quedan A-27 y A-47 en hipótesis, y el registro da la lectura y el tope) y
  `scripts/bloque_de_la_caja.py` pasa `Diagnostico()` a `tope_del_registro` (lo rechazaba
  `TopeRechazadoError`); sus importaciones sobrantes salen. No se ejecutan sobre material; los
  tests que los importan pasan: `test_embudo_77.py`, `test_orden_stop_pivote.py` (carga
  `bloque_de_la_caja.py`) y `test_margen_lote.py` (el bróker): 35 en verde. `mypy` sobre los tres
  guiones da cuatro avisos que ya están en `main` (medido en el clon `C:/cm/main`: los mismos
  cuatro); `make check` los admite como hasta ahora.
- **Punto 11.** Dos recuadros de corrección en `docs/validation/ACTIVAR-SESION-05.md` (informe
  cerrado: recuadro con fecha y rama, cuerpo intacto; el contrato lo permitía desde la apertura):
  junto a §2, 4, que «la caja entera» es lectura del consultor deducida de su ejemplo y no lo que
  dice `ev-v15-010451-5b123278`; y junto a §2, 6, que el registro de la sesión 4 es
  `fb-2026-10-04-sesion-04-d1792021` (no `8e2d728a`, el de A-51) y que un CORRECT va sobre el
  parámetro, no sobre un registro.
- **Trailer:** ninguno (ni `knowledge/spec` ni `knowledge/cases`); `knowledge validate` en verde.

## 2. La lista para la sesión 6 (lo que esta rama le deja; R4.2)

Para la hoja de la sesión 6, además de la lista de `ACTIVAR-SESION-05.md` §3 (cada pregunta con
opciones y «otra, ¿cuál?», con esquemas de velas y el marco escrito):

1. **A-35, la mecha (§3, 2, ampliada; decisión 1):** «Marcas un alto en M15 cuando cierra la vela
   contraria. ¿La mecha que mueve el alto es la de la vela contraria que lo forma, o también la de
   una vela posterior que lo pasa y vuelve? (a) solo la de la contraria; (b) también la de una
   posterior; (c) otra, ¿cuál? ¿Y lo mismo en un bajo?». Hoy `liquidez_m15_mecha_que_vuelve` =
   `cualquier_mecha` (lectura del consultor, ADR-0084). Esquema en M15: la contraria roja con la
   mecha por encima del alto, y una vela posterior con la mecha por encima y el cierre por debajo.
2. **Las mechas de una vela sin cuerpo en M1 (§3, 10, segunda pregunta):** hoy cuentan donde
   cuentan (romper un nivel, el 1 de la caja), por decisión del consultor (ADR-0085 §3).
3. **En M15, si una vela sin cuerpo entre la racha y la contraria corta la racha** (ADR-0085 §2):
   «En M15, una racha de velas verdes, una vela sin cuerpo y después la roja que cierra: ¿la roja
   marca el alto de las verdes, o la vela sin cuerpo corta la racha y no hay alto? (a) marca el
   alto; (b) lo corta; (c) otra, ¿cuál?». Hoy, en M15, lo corta (`pivotes_m15`, sin cambio).
4. **La condición de `ev-v15-004037-a2ab3980`** («venga de un flujo bajista y después rompa
   cerrando por debajo»; ADR-0085 §3, no aplicada): «Para que el máximo de la verde sea punto de
   breaker, ¿la roja de después tiene que cerrar por debajo del mínimo de la verde, o basta con que
   sea roja? ¿Y hace falta que el precio venga de un flujo bajista? (a) basta con que sea roja;
   (b) tiene que cerrar por debajo; (c) otra, ¿cuál?». Hoy basta con que sea roja (en M1 la mecha
   siempre vale, A-32).
5. **S-15, la zona más reciente (decisión 6), dos preguntas separadas, cada una con su dibujo en
   M1 y el marco escrito en el dibujo** (rehechas por la orden de cierre del consultor del
   2026-10-27, punto 5: el dibujo de la alternancia dentro de un retroceso sale, porque el trader
   ya lo contestó en la sesión 4, S-10, ADR-0076 §1; la versión anterior, con tres dibujos y una
   pregunta que contradecía S-10, la vio el auditor del consultor). **Dibujo 2:** «Después de la
   toma, el primer retroceso tiene alternancia; aparece un punto nuevo y su retroceso está limpio.
   ¿Entras en este segundo? (a) sí; (b) no; (c) otra, ¿cuál?». **Dibujo 3** (el que mide §0.b.8):
   «La orden ya está puesta en el primer punto tras la toma y se llena con la primera vela verde
   del retroceso, antes de que haya alternancia. ¿Esa entrada vale? (a) sí; (b) no, había que
   esperar al punto siguiente; (c) otra, ¿cuál?». Sin registro y sin ADR en esta rama; RN-009 no
   cambia.
6. **S-19 frente a S-24 (§3, 10, primera pregunta):** la vela de 1 o 2 puntos sigue siendo de su
   color (ADR-0085 §3) hasta que el trader diga lo contrario.
7. **A-50 (§3, 7):** los dos dibujos, con el valor de hoy `caja_entera` (lectura del consultor).

## 3. Las líneas preparadas para el commit del contrato del cierre

Medidas con `wc -c` (bytes UTF-8) sobre el texto ya escrito, en una copia de `PROJECT_STATE.md`
de la rama con estas líneas aplicadas, hecha por el guion `medir_ps.py` de la carpeta de trabajo
de la sesión (no está en el repo; sustituye V y F, amplía K, añade la deuda, pone `Current Branch`
en `main` y `Current Feature` con la frase de abajo): **22.974 bytes** (hoy en la rama, 23.013; en
`main`, 22.989; el tope del test, 25.000). La V nueva mide 396 bytes, la de hoy 562; la F, 85.
Tras el revisor (b7, m2): la V lleva las tres cosas que dicta el encargo («este tag», «sobre toda
la construcción» y el `diff` contra CABLEADO-SIMULADOR-LINEA-BASE.txt) y, para que quepa, K y la
deuda se acortan; la frase de `Current Feature` ya no es un supuesto de 232 bytes sino la de abajo
(213 bytes), y el margen hasta 23.000 es de 26 bytes: el cierre no añade nada más a
`PROJECT_STATE.md`, y si el consultor cambia alguna frase se vuelve a medir.

- **V** (sustituye a la de hoy):
  `V. Activar la sesión 5 (R4.1). HECHAS spec y motor (\`trabajo/activar-sesion-05\` y \`trabajo/activar-sesion-05-motor\`, este tag: ADR-0084 a 0086, RN-037; A-35 y A-50 con lectura del consultor, ABIERTAS). QUEDA la re-corrida del arnés con \`--simular\` sobre toda la construcción (ADR-0070 §3; diff contra CABLEADO-SIMULADOR-LINEA-BASE.txt, ACTIVAR-A35-A44.md §5.1); después la sesión 6 (R4.2).`
- **F** (sustituye a la de hoy):
  `F. La re-corrida del arnés (ADR-0070 §3); después la sesión 6; R6a en los huecos.`
- **K** (se amplía al final):
  `Y las dos negativas de ACTIVAR-SESION-05-MOTOR.md §0.d (pytest desde C:/cm/, encadenadas).`
- **Technical Debt** (línea nueva, tras la del alias de la raíz):
  `- ADR-0087 sigue en los \`ids-inexistentes\` del encargo y del informe de trabajo/activar-sesion-05-motor; lo saca la rama que lo cree.`
- **Current Branch:** `main`. **Current Feature** (sustituye a la de hoy):
  `Ninguna rama abierta. trabajo/activar-sesion-05-motor cerrada en main el <fecha> (stable/F38f-activar-sesion-05-motor): la parte de motor de la sesión 5; lo siguiente, la re-corrida del arnés (F; docs/plan/HOJA-DE-RUTA.md).`
  (medida con `2026-10-27` en `<fecha>`; otra fecha del mismo formato pesa lo mismo).
- **Known Ambiguities:** no cambia: ninguna ambigüedad se abre ni se cierra (A-35 y A-50 siguen
  ABIERTAS con el mismo título, clase y bloqueante).
- **`docs/plan/HOJA-DE-RUTA.md`, R4.1, Estado:** «spec y motor HECHOS (`trabajo/activar-sesion-05`,
  `stable/F38e-activar-sesion-05`; `trabajo/activar-sesion-05-motor`, el tag de su cierre;
  ACTIVAR-SESION-05-MOTOR.md: ADR-0084 a ADR-0086, RN-037). Queda la re-corrida de ADR-0070 §3 con
  su `diff` (ACTIVAR-A35-A44.md §5.1), que mire las entradas que nacen en el primer punto tras la
  toma y se llenan antes de la alternancia (§0.b.8).» Sin «HECHA» a secas mientras NA:V siga viva
  (`test_hoja_de_ruta`, `problemas_b`).
- **`docs/plan/HOJA-DE-RUTA.md`, R4.2, «Qué es»:** gana lo de §2 de este informe: A-35 (la contraria
  o cualquier mecha, y el bajo); las mechas de una vela sin cuerpo en M1; en M15, si una vela sin
  cuerpo corta la racha; la condición de `ev-v15-004037-a2ab3980`; S-15 con los dos dibujos del
  punto 5 de la orden de cierre (§2, punto 5).
- **`docs/runbooks/ERRORES-RECURRENTES.md`, fila de la rama** (la escribe `cerrar-rama`), con lo
  que el consultor pidió (respuesta a la PARADA, puntos 0 y 10, y el encargo, «PRIMER COMMIT»):
  (1) antes de proponer un valor provisional bajo una ambigüedad se lee el ADR que la abrió
  (ADR-0045 y ADR-0054 prohibían el de A-35; lo vio el auditor); (2) el encargo daba RN-011 como
  la regla que coloca, y es RN-015 (`colocar_orden_limite` lleva el `efecto`); (3) el auditor del
  consultor buscó sobre la raíz de un clon de solo lectura (la fila del 2026-10-26 de
  HOLDOUT-EXPOSICIONES): tampoco se busca sobre la raíz, solo sobre rutas literales; y, de la
  sesión, (4) antes de cada `make check`, `ruff format`, `ruff check` y `mypy` sobre los ficheros
  tocados (tres pasadas perdidas en esta rama por lint, mypy y dos tests que congelaban el
  instante de una cancelación y no salieron en un `grep` previo: `git grep` de los instantes y
  las reglas que cambian, antes del `make check`).

## 4. El encargo, punto por punto

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 1 | Rama desde 32904ee, base comprobada con git, CI 40421174533 con `gh run view` suelto | Hecho | cabecera; commit e8cde8b |
| 2 | Contrato: tramo R4, riesgo alto, artefacto; ampliado a los tres guiones (encargo, 10), a ACTIVAR-SESION-05.md (11) y al runbook (respuesta, 7) | Hecho | `contrato.yaml`; §1.6 y §1.7 |
| 3 | Encargo copiado tal cual, con el bloque `ids-inexistentes` (ADR-0084 a 0087); cada uno sale al crearse | Hecho; queda ADR-0087 (respuesta, 9) | `docs/encargos/…`; §1.1, §1.2, §1.6 |
| 4 | PRIMER COMMIT: la fila del 2026-10-26 en HOLDOUT-EXPOSICIONES con la exposición del auditor del consultor | Hecho | commit e8cde8b |
| 5 | FASE 0 a (tabla), b.1-b.8, c (PARADA) | Hecho | §0 |
| 6 | Ninguna ambigüedad se cierra; `test_kit.py` no cambia; A-51 y A-21 RESUELTAS | Hecho | `test_kit.py` sin tocar (diff); §1.1-§1.6 |
| 7 | Nada fijado se pisa sin su régimen (CORRECT con su objetivo; la regla cita su CORRECT; ADR enmendado con recuadro y fila) | Hecho | §1.2, §1.4, §1.5; ADR-0045, 0054, 0060, 0061, 0066, 0076, 0077 |
| 8 | Todo comportamiento nuevo sale de un ítem o va como LECTURA/DECISIÓN DEL CONSULTOR | Hecho | ADR-0084 §2-§3, ADR-0085 §3, ADR-0086, RN-035/RN-037, parámetros |
| 9 | Ninguna cifra en una forma; el minuto es `cierre_h4_antelacion`; casi plana es cuerpo cero | Hecho | §1.2, §1.5 |
| 10 | No cambian A-13, ADR-0083, A-44 y sus parámetros, lo que RN-036 cuenta, RN-009; M15 solo por el punto 1, M1 no por el 1 | Hecho | diff; `test_las_series_de_m1_no_se_mueven`, `test_las_series_de_m15_no_se_mueven` |
| 11 | Sin arnés, sin visor a mano, sin material; `test_preparar_a35.py` y `test_visor.py` declarados como hasta ahora | Hecho | §5 |
| 12 | Next Action y hoja de ruta sin tocar; sus líneas en el informe | Hecho | §3 |
| 13 | Makefile, `.claude/` y la guardia sin tocar; informes cerrados solo con los dos recuadros | Hecho | diff; §1.7 |
| 14 | Fechas de los registros (v15 10-23 / v16 10-25, `video`, `trader_grabado`, t0/t1, cita literal) | Hecho | los cuatro registros |
| 15 | Punto 1: parámetro, ADR-0084 (enmienda ADR-0045, NOTA ADR-0054: decisión 0), espejo en el bajo, contraste con v10 y ADR-0062, docstring, A-35, RN-004, tests | Hecho | §1.1 |
| 16 | Punto 2: ADR-0085 (enmienda ADR-0076, NOTA ADR-0061), solo M1 y cuerpo cero, decisiones del consultor, condición de 004037 no aplicada (decisión 3), CONFIRM RN-007, tests | Hecho | §1.2 |
| 17 | Punto 3: CORRECT sobre `ev-v10-014310`, notas de RN-007 | Hecho (en el commit del 2) | §1.2 |
| 18 | Punto 4: `caja_lado_de_ruido`, lector por argumento de RN-005 (decisión 4), A-50, tests | Hecho | §1.3 |
| 19 | Punto 5: `tras_la_detencion`, CORRECT con supersede, ADR-0077 §5, `SeguidorRacha`, RN-036, tests | Hecho | §1.4 |
| 20 | Punto 6: RN-035 en el último minuto, RN-037 gate, `en_el_ultimo_tramo_h4` (decisión 5), recuadros 0060 §5/§6 y 0066 §4, tests | Hecho | §1.5 |
| 21 | Punto 7: S-20 sin registro ni código; la fila de `test_a21_series.py` ya existía | Hecho (nada que añadir) | §0.a, 7 |
| 22 | Punto 8: ADR-0086, RN-020 retira, recuadro ADR-0077 §3, test | Hecho | §1.6 |
| 23 | Punto 9: S-15 medido y PARADA; sin frontera: a la sesión 6 con los dibujos; NOTA en ADR-0076 §2 (decisión 6) | Hecho | §0.b.8, §2, ADR-0085 §4 |
| 24 | Punto 10: `broker.py:177` y los tres guiones | Hecho | §1.7 |
| 25 | Punto 11: los dos recuadros en ACTIVAR-SESION-05.md | Hecho | §1.7 |
| 26 | Por cada commit, el paso 3 de activar-sesion: registros, `apply --check` solo con los de esa respuesta, AMBIGUEDADES.md, `test_kit.py`, `spec_version`, manifest y docs, lector de cada parámetro, tests de sentido cambiado dichos, `knowledge validate`, `Fuente:` | Hecho | §1.1-§1.7; `git log --format=%B main..HEAD` |
| 27 | Tests que rompen: por cambio de motor (1, 2, 4, 5, 6, 8) el que falla con `main`; por marco; por enum; `test_kit.py` | Hecho | §6 |
| 28 | HOLDOUT: nunca listar ni buscar sobre la raíz; exposiciones el mismo día; ningún día real en los tests | Hecho | §5; series de 2030 |
| 29 | ENTREGA: CI por `fix/`, revisor opus con cinco alcances, líneas del cierre, PROJECT_STATE medido | Hecho | §3, §7, §8 |
| 30 | Respuesta a la PARADA copiada tal cual y aplicada punto por punto; PARADA 2 si algo la contradecía | Hecho; sin PARADA 2 | «Respuesta del consultor…», §1 |

**Desviaciones declaradas:** (a) el commit 2+3 y el 10+11 agrupan puntos, como pidió la respuesta
(punto 8); (b) `test_rn035_ventana_fin.py::test_hueco…` conserva su nombre aunque ya no congela un
hueco (§1.5); (c) el test de la colocación a las 11 usa un `toca_colocar_orden_limite` sintético
sin estado (§1.5), porque el de `test_cableado` se consume al evaluarse; (d) el primer `make check`
del commit 4855860 salió en rojo por dos tests de `test_vida_de_la_orden.py` que no se habían
buscado antes, corregidos en el mismo commit con el rótulo nuevo de la traza (§1.5); (e) los
recuadros de ACTIVAR-SESION-05.md llevan la fecha del 2026-10-27, el día en que se escribieron (el
reloj cambió de día durante la rama); (f) el encargo pedía un test de que «lo que se llene en ese
minuto lo cierra RN-002 en el evento siguiente», y el test escrito llena la orden en el minuto
ANTERIOR al último: en el último ya no puede llenarse nada, porque RN-035 la retira en el primer
evento de ese minuto (el de fin − 1), así que el caso del encargo no existe en el cableado y el
test prueba el más cercano que sí existe (revisor, b6); (g) la respuesta (punto 2) dice «el guion
de CAJA-77 no se toca» y el commit b18fe31 cambia `scripts/bloque_de_la_caja.py`: no su cálculo
(R5 y R6, que son lo que el test compara), sino cómo construye `Diagnostico`, que el punto 10 de la
misma respuesta manda cambiar en los tres guiones; las dos frases hablan de partes distintas del
fichero (revisor, m4); (h) las notas de tres registros de feedback traen contenido de otros ítems o
de la spec (72c9a9e8: RN-007 y ADR-0085; 978be13f: `ev-v10-010804` y ADR-0077; 1526aa39: lo que
dice `ev-v16-002323`; y a9e4f879, que vio el auditor del consultor: la justificación del régimen
con `fb-2026-09-29-sesion-03-ffab23dc`), contra «las notas de cada registro, solo con lo que trae
su ítem»; además, el `respuesta_literal` de 72c9a9e8 empieza con la pregunta leída («cambia algo
si son 3 velas sin cuerpo en vez de una») y su ítem, `ev-v15-003959-5898c61e`, no lleva la reserva
de «mezcla». Son inmutables tras el commit y se quedan como están, sin superseder (decisión del
consultor en la orden de cierre del 2026-10-27, punto 6: son notas de contexto y no cambian
objetivo, acción, valor ni cita; revisor, b2; §8). La guardia que compare las notas con el ítem va
a G.2 de la hoja de ruta en el cierre.

## 5. Exposiciones

Una, declarada el 2026-10-27 en HOLDOUT-EXPOSICIONES tras el revisor (m5; el encargo la nombra):
lo que lee `data/` en cada `make check` de la rama es lo de siempre, ya declarado en las filas del
2026-10-18 y del 2026-10-26 (`test_preparar_a35.py` y `test_visor.py` corren el arnés y el visor a
secas sobre abril con el M1 de marzo para calentar), pero ahora con el motor nuevo: la fila del 27
lo dice con los `make check` de cada commit de la rama y lo que el motor nuevo hace distinto con
las mismas velas; ninguna salida se copia al informe. Todo lo demás de la rama es sintético (series de 2030 y de `test_estructura_m1`),
spec, docs y tests; los clones `C:/cm/motor` (retirado, §0.e) y `C:/cm/main` (los tests que
fallan con `main`; sin `data/`, sin `corpus/`) no leyeron material. Ningún día reservado, ningún
resultado de operación, ninguna cifra de material en nada de lo escrito.

## 6. Lo que NO cambia, y los tests que rompen a propósito

`git diff --stat main...HEAD`: `57 files changed` (y `contrato_rama.py` en verde: «57 ficheros
dentro del contrato»; el informe decía 52, revisor a3). Fuera de lo que el encargo pide no hay
nada: ni `Makefile`, ni `.claude/`, ni `knowledge/evidence/`, `knowledge/cases/`,
`knowledge/corpus/`, ni los registros de las sesiones anteriores, ni `docs/plan/`, ni
`tests/unit/test_kit.py` (sus conjuntos de RESUELTAS y de bloqueantes ABIERTAS, A-35 y A-44, son
los de `main`: 41 tests en verde sobre el código de `main` en la fase 0 y en cada `make check` de
la rama; la salida de hoy en la rama, `uv run pytest -p no:cacheprovider tests/unit/test_kit.py`:
`41 passed in 70.52s (0:01:10)`, revisor m3). `src/botsito/cli.py` y `src/botsito/feedback/`
(protegidos por el contrato) no se tocan.

| Cambio de motor | Test que falla con `main` (clon `C:/cm/main`) y pasa con la rama | Marco que no se mueve | Enum |
|---|---|---|---|
| 1 · la mecha que vuelve (M15) | `test_mecha_que_vuelve.py`, `test_pivotes_m15.py` (ImportError en `main`; lo que `main` hace, medido en §0.a); y, tras el revisor (b3), los dos tests del cargador de `test_mecha_que_vuelve.py` por `arnes.dias_de_mercado` y `visor.Preparador.preparar` con cargadores sintéticos, que en `main` fallan porque `DatosMercado` no tiene `mecha_que_vuelve` | `test_las_series_de_m1_no_se_mueven` | `test_un_valor_fuera_del_enum_falla_al_leer_el_registro` |
| 2 · la vela sin cuerpo (M1) | `test_velas_sin_cuerpo_m1.py` (ImportError), la fila del doji de `test_a21_series.py` y el test nuevo de CAJA-77 en `test_orden_stop_pivote.py` | `test_las_series_de_m15_no_se_mueven` | — |
| 4 · la caja entera | `test_caja_lado_de_ruido.py` (siete fallos en `main`, por el registro: `main` no tiene el parámetro; lo que hace con la caja, en §0.a) | — | `test_el_registro_real_y_un_valor_fuera_del_enum` |
| 5 · la racha | `test_racha_perdidas.py` (cinco fallos en `main`) | — | `test_registro.py::test_enum_exige_opciones…` (todo enum) y `test_las_opciones_sin_contrato_se_niegan` |
| 6 · el último minuto | `test_ultimo_minuto.py` (cinco de siete), `test_rn035_ventana_fin.py`, `test_escenarios_por_sesion.py`, `test_vida_de_la_orden.py` | — | — |
| 8 · RN-020 retira | `test_rn020_retira_pendiente.py` (dos de dos) | — | — |

Las salidas de cada corrida en el clon están en §1.1 a §1.6.

## 7. La CI de Linux

`git push origin trabajo/activar-sesion-05-motor:refs/heads/fix/activar-sesion-05-motor` (el
clasificador lo dejó pasar). Run **40460127761** sobre b18fe31881a26ee70b0528a4589aae03d83ac58b
(`gh run view 40460127761` suelto y la API de check-runs con el sha literal): `completed`,
`failure` con el único fallo aceptado, `test_cli.py::test_state_check_ok_on_real_repo`
(`PROJECT_STATE declara la rama 'trabajo/activar-sesion-05-motor'; la rama actual es
'fix/activar-sesion-05-motor'`): `1 failed, 2921 passed, 46 skipped in 334.75s`. Los 46 saltados
son los de siempre en Linux (sin `data/`). El run del último commit (el de este informe con los
arreglos del revisor, §8) se consulta igual (`gh run view <run>` suelto, o la API de check-runs
con su sha literal) y va en el mensaje final a Aleks y en el registro del cierre
(`docs/state/HISTORIA.md`): anotarlo aquí exigiría otro commit, con otro run sin anotar.

## 8. El revisor

Subagente `revisor` (`.claude/agents/revisor.md`, modelo opus), lanzado con el informe terminado hasta §7 y los cinco alcances del encargo (ENTREGA), y con la regla del holdout del encargo (rutas literales, nunca la raíz ni `knowledge/cases` con un filtro detrás). Su informe, tal cual (ninguna retirada: no cita ningún tramo no citable):

## Informe del revisor · trabajo/activar-sesion-05-motor · 2026-10-27

Base: `git merge-base main HEAD` = 32904ee. Commits e8cde8b..b18fe31 (9). Sin commitear: solo `docs/validation/ACTIVAR-SESION-05-MOTOR.md` (lo esperado: le faltan §7 y §8). La rama **no está lista**: hay un hallazgo que bloquea en el eje (b), y una corrección de una línea lo resuelve.

### Eje (a) · Reglas de la casa
Resumen: 0 bloquea, 2 importa, 2 menor.

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| a1 | importa | En §1 del informe, cada sección lleva el sha del commit del punto anterior. §1.2 no lleva ninguno y b18fe31 no aparece en §1. El «Estado» dice «siete commits sellados» y lista nueve más «el de este informe». | `ACTIVAR-SESION-05-MOTOR.md:478` (§1.3, punto 4) dice «Commit 2+3: 225ac79», y el punto 4 es 5b44cd6. `:520` (§1.4, punto 5) dice «Commit 4: 5b44cd6», y es dd2042f. `:565` (§1.5, punto 6) dice «Commit 5: dd2042f», y es 4855860. `:632` (§1.6, punto 8) dice «Commit 6: 4855860», y es 7208db2. `:667` (§1.7) dice «Commit 8: 7208db2», y es b18fe31. Lo comprobé con `git log --format='%h %s' main..HEAD`, donde 5b44cd6=feat(a50), dd2042f=feat(rn036), 4855860=feat(rn035), 7208db2=feat(rn020) y b18fe31=chore puntos 10 y 11. El «Estado» está en `:841`. |
| a2 | importa | Hay texto entre comillas que no reproduce la cita del ítem: (1) en la descripción de `racha_perdidas_reinicio`, «al día siguiente de parar por nueve pérdidas … Pues al día siguiente Nuevamente en cero», cuando la cita de ev-v16-002126-d2376f71 es solo «Pues al día siguiente Nuevamente en cero, o sea, se sigue continuando» y lo primero es una paráfrasis de la afirmación; (2) ADR-0086 §2 cita «solo el del día y las 9 seguidas» sin id: sale de ev-v15-000856-ee8f7ba3 («no solo el del día…»), que no está entre los ítems que nombra el encargo; (3) las notas de RN-037 ponen entre «» la `afirmacion` de ev-v16-002323 como si fueran palabras del trader. | `knowledge/spec/parametros.yaml:1348-1349`; `knowledge/evidence/v16/ev-v16-002126-d2376f71.yaml:7`; `docs/adr/0086-…md:31`; `knowledge/evidence/v15/ev-v15-000856-ee8f7ba3.yaml:7`; `knowledge/spec/strategy_spec.yaml:1048-1050` frente a `ev-v16-002323-515b9da4.yaml:10-11`. |
| a3 | menor | Cifras del informe que no cuadran: §6 dice «52 ficheros» y `git diff --stat` da 57; §1.3 dice que fallan «los seis tests del fichero nuevo» con `main` y fallan 7; la V nueva «mide 378 bytes» y, tal como está escrita en §3, mide 384. | `ACTIVAR-SESION-05-MOTOR.md:816`, `:509`, `:726`. Lo medí con `git diff --stat main...HEAD` (57 files); con pytest en C:/cm/main, 7 FAILED en `test_caja_lado_de_ruido.py`; y con Python sobre la línea 729, 384 bytes. |
| a4 | menor | El recuadro de ADR-0060 §5 afirma sin condición que «ninguna orden está pendiente cuando empiezan los ticks del último minuto». Eso solo vale con `orden_pendiente_al_abrir_sesion = se_retira`: con `sigue_hasta_ventana_fin`, RN-035 dispara a las 10:59 sin retirar. | `docs/adr/0060-…md` (recuadro de §5); `strategy_spec.yaml:1034` (`retirar_orden_limite … segun: orden_pendiente_al_abrir_sesion`); `tests/unit/test_escenarios_por_sesion.py:460` («con `sigue_hasta_ventana_fin` sin retirar»). |

Comprobado sin hallazgos:
- **Contrato.** `contrato_rama.py` da «CONTRATO: 57 ficheros dentro del contrato … 5 comprobaciones».
- **`feedback apply --check`.** «4 parametros; 0 cambian, 4 ya estaban; --check: no se ha escrito nada».
- **`knowledge validate`** (sin redirigir, exit=0). Da «OK: 191 registros de feedback, historial intacto, commits con Fuente» y «37 reglas … hash del manifiesto al dia».
- **`make-check.log`.** «2968 passed», «SELLO: … arbol 6df24870…», que es `b18fe31^{tree}`, y «PICO DE MEMORIA … 299 MiB».
- **`spec docs --escribir`.** No lo ejecuté porque escribe. Lo sustituye `tests/contract/test_spec_docs_generados.py`, que pasa.
- **Trailers `Fuente:`.** Están en el cuerpo de los 6 commits que tocan `knowledge/spec`, y todos sus ids existen.
- **Holdout.** Nada toca `knowledge/cases/`. El clon C:/cm/main no tiene `config/settings.local.toml` ni `data/` (solo `manifests`).
- **Regímenes.** El feedback es solo `A` (4 registros). No cambia nada en `evidence`, `corpus`, `manifests` ni `libros.yaml`. El CORRECT sobre un parámetro fijado por el trader lleva `supersede` (978be13f→d1792021), y no hay ningún RESOLVE ni REOPEN.
- **Ambigüedades.** A-35 y A-50 cambian en el mismo commit que `docs/spec/ambiguedades.md` (35211a0, 5b44cd6), sin abrir ni cerrar ninguna. A-50 gana un ítem que sí habla de su pregunta.
- **ADR.** 0084, 0085 y 0086 llevan `ACTIVE` y `test_adr.py` pasa.
- **Informe cerrado.** `ACTIVAR-SESION-05.md` solo gana dos recuadros `>`, con fecha y rama.
- **Tres guardias de cita.** No hay ningún sitio nuevo de otra clase: predicados y reglas ya se recorren (`spec/modelo.py:382, 415, 879`).
- **Cifras.** Ninguna en las formas.
- **Ítems de evidencia.** La rama no añade ninguno.
- **Citas del informe contrastadas.** «un doji no es de ningún color…» (ADR-0076:61-62), «llenaría por ticks…» (ADR-0077:56) y la frase de ADR-0045:21 cuadran con su fuente.

### Eje (b) · Encargo
Resumen: 1 bloquea, 6 importa, 5 menor. Requisitos: 31 hechos, 9 parciales, 2 no hechos (pendientes de entrega), 1 hecho de otra forma (declarado).

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 1 | Rama desde 32904ee, base y CI de main comprobadas | Hecho | merge-base 32904ee; informe:8-18 |
| 2 | Contrato: R4, riesgo alto, artefacto; ampliado a los guiones, a ACTIVAR-SESION-05.md y al runbook | Hecho | `contrato.yaml:2-4,8,17-21` |
| 3 | Encargo tal cual con `ids-inexistentes`; cada id sale al crearse | Hecho | `git diff e8cde8b HEAD -- docs/encargos/…`: solo el bloque y la respuesta |
| 4 | PRIMER COMMIT: fila de HOLDOUT del 2026-10-26 | Hecho | e8cde8b; `HOLDOUT-EXPOSICIONES.md:73` |
| 5 | FASE 0 a, b.1-b.8 y c, «Lo que necesito que decidas» | Hecho | informe §0 y :252-320 |
| 6 | Respuesta copiada tal cual en el encargo y en el informe | Hecho | `diff` de encargo:136-157 frente a informe:326-347: IGUALES |
| 7 | Orden de commits 1; 2+3; 4; 5; 6; 8; 10+11 | Hecho | `git log` |
| 8 | Ninguna ambigüedad se cierra; `test_kit.py` sin tocar; A-51 y A-21 RESUELTAS | Hecho | diff de `ambiguedades.yaml` (solo A-35 y A-50, ABIERTAS); `test_kit.py` fuera del diff y en verde |
| 9 | Régimen: objetivo admitido por la acción; la regla cita su CORRECT | Hecho | `feedback/modelo.py:66-69`; RN-035 cita 1526aa39 (`strategy_spec.yaml:982-983`) |
| 10 | Notas de cada registro solo con lo de su ítem | Parcial | b2 |
| 11 | Todo comportamiento sale de un ítem o va rotulado como LECTURA o DECISIÓN | Parcial | b5 |
| 12 | Ninguna cifra en una forma | Hecho | spec diff |
| 13 | No cambian A-13, ADR-0083, A-44/`perdida_trader_*`, lo que cuenta RN-036 ni RN-009; M15 solo por el punto 1 | Hecho | diff de `parametros.yaml` y de la spec |
| 14 | Sin arnés, sin visor a mano, sin material | Hecho | informe §5; el clon no tiene `data/` |
| 15 | Next Action y hoja de ruta sin tocar | Hecho | diff de PS (solo CB, CF, Tests y archivo); `docs/plan/` fuera del diff |
| 16 | Makefile y `.claude/` sin tocar; informes cerrados solo con recuadros | Hecho | diff |
| 17 | Fechas, medio, procedencia, t0/t1 y cita de los registros | Hecho | los 4 yaml |
| 18 | P1: parámetro, ADR-0084, recuadro en 0045, NOTA en 0054, docstring, A-35, RN-004 | Hecho | diff |
| 19 | P1: tests (alto/bajo, i/ii, cada opción, el cuerpo toma, dos mechas, M1 iguales, test partido) | Hecho | `test_pivotes_m15.py:149-271`, `test_mecha_que_vuelve.py` (el bajo (ii) solo por dominio) |
| 20 | P2: ADR-0085, solo M1 y cuerpo cero, decisiones, CONFIRM, la fila de a21 y CAJA-77 | Hecho | 225ac79 |
| 21 | P3: CORRECT sobre ev-v10-014310; RN-007 sin «DESALINEADO» | Hecho | `a9e4f879.yaml`; grep de DESALINEADO: 0 |
| 22 | P4: `caja_lado_de_ruido`, lector, A-50, RN-005, tests | Hecho | 5b44cd6 |
| 23 | P5: CORRECT con supersede, SeguidorRacha, RN-036, recuadro en 0077 §5, tests | Hecho (con b4) | dd2042f |
| 24 | P6: RN-035 retira en [fin−antelación, fin), cita su CORRECT, parámetros | Hecho | `strategy_spec.yaml:967-1036` |
| 25 | P6: las notas de RN-035 quitan «un minuto antes es frase del consultor» y el HUECO | Parcial | b1 |
| 26 | P6: RN-037 gate; recuadros en 0060 §5/§6 y 0066 §4 con su fila | Hecho | diff de ADR y README |
| 27 | P6: tests (el hueco cambia, no se coloca, primer cierre de las 11, red, RN-002 cierra lo llenado «en ese minuto») | Parcial | b6 |
| 28 | P7: S-20 sin registro ni código | Hecho | informe §0.a fila 7 |
| 29 | P8: ADR-0086, RN-020, recuadro 0077 §3, test, `Fuente: ADR-0086` | Hecho | 7208db2 |
| 30 | P9: S-15 medido, PARADA, sesión 6, NOTA en ADR-0076 §2 | Hecho | informe §0.b.8; ADR-0076:74-80 |
| 31 | P10: `broker.py` y los tres guiones | Hecho | b18fe31; `test_embudo_77.py` en verde |
| 32 | P11: dos recuadros en ACTIVAR-SESION-05.md | Hecho | b18fe31 |
| 33 | Paso 3 por commit: `spec_version` (18.1.9 → 18.5.0), manifest y docs, validate, `Fuente:` | Hecho | `spec_manifest.yaml`; trailers |
| 34 | Cada cambio de motor con un test que falla con `main` por el camino real | Parcial | b3 |
| 35 | Un test por marco | Parcial | b3 |
| 36 | Un test por enum | Hecho (racha, por el test genérico; declarado en §1.4) | informe:552-554 |
| 37 | `test_kit.py` «con la salida» | Parcial | m3 |
| 38 | HOLDOUT: toda exposición el mismo día, también lo que leen en `make check` con el motor nuevo | Hecho de otra forma (declarado en §5) | m5 |
| 39 | Líneas del cierre (V, F, R4.1, R4.2, KA, TD, K, ERRORES) | Parcial | b7 |
| 40 | PS medido con `wc -c`, por debajo de 23.000 | Parcial | m2 |
| 41 | CI de Linux por `fix/`, con su run | No hecho (pendiente) | informe:837 «PENDIENTE» |
| 42 | El informe del revisor pegado al final | No hecho (pendiente: es este) | — |
| 43 | «El encargo, punto por punto» | Hecho | informe §4 |

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| b1 | bloquea | El encargo (punto 6) pide «Sus notas quitan que «un minuto antes» es frase del consultor y el HUECO». Se quitó una aparición, pero queda otra, que ahora contradice la regla (la cita de RN-035 es ese minuto, y sí se fija). El informe da el punto por hecho. | `knowledge/spec/strategy_spec.yaml:1022`: «(SESION-04-EXTRACCION.md §3.6); «un minuto antes» es frase del consultor y no se fija.» Lo afirma como hecho `ACTIVAR-SESION-05-MOTOR.md:580-581`. |
| b2 | importa | «Las notas de cada registro, solo con lo que trae su ítem» (encargo, QUÉ NO CAMBIA) no se cumple en tres registros: 1526aa39 trae lo que dice OTRO ítem («Para precisar, ev-v16-002323-515b9da4: si se llena…»); 978be13f trae ev-v10-010804 y ADR-0077; 72c9a9e8 trae el contenido de RN-007 y de ADR-0085. Son inmutables: solo cabe aceptarlo o superseder. | `fb-2026-10-23-sesion-05-1526aa39.yaml:19-24`; `…-978be13f.yaml:18-22`; `…-72c9a9e8.yaml:16-19` |
| b3 | importa | Alcance (4). Para los puntos 1 y 4, el fallo con `main` es de importación o de registro, no de comportamiento: `ImportError … CUALQUIER_MECHA` y, en `test_caja_lado_de_ruido.py`, 7 fallos `ParametroDesconocidoError` o `AssertionError: caja_lado_de_ruido`. Ningún test sintético pasa por `arnes.dias_de_mercado` ni por `visor.Preparador`, que son los que leen el selector del registro: `_datos` monta `DatosMercado` a mano, así que si `arnes.py:212-215` no pasara el selector, nada fallaría en CI. `test_las_series_de_m15_no_se_mueven` solo llama a `pivotes_formados`, no a `DatosMercado.liquidez_m15`. Además, 4 de los tests copiados en C:/cm/main son versiones ANTERIORES a las de la rama, así que las salidas «con main» del informe para `test_ultimo_minuto.py` (y para `test_mecha_que_vuelve`, `test_pivotes_m15` y `test_escenarios_por_sesion`) no son de los tests actuales. | Con pytest en C:/cm/main (salida arriba). `tests/unit/test_mecha_que_vuelve.py:57-67`; `test_velas_sin_cuerpo_m1.py:145-162`. `diff -q` rama/clon: «differ» en esos 4, y en `test_ultimo_minuto.py` cambian las aserciones de RN-037 (líneas 112-119). Sí fallan por comportamiento con `main`: la fila del doji de a21, el test nuevo de CAJA-77, `test_rn035_ventana_fin` (3), `test_vida_de_la_orden` (3), `test_racha_perdidas` (5) y `test_rn020` (2). |
| b4 | importa | Con `tras_la_detencion`, la racha vuelve a cero solo si `detenido()` se consultó el mismo día, después de la novena pérdida (que es lo que fija `detenido_en`). Si la novena se registra sin consulta posterior ese día, al día siguiente sigue en 9 y la décima vuelve a detener, que es el comportamiento de `nunca`. El nombre `test_el_reinicio_llega_aunque_nadie_consulte_entre_medias` promete más de lo que prueba: consulta el día 0 (línea 153). En el cableado, el camino posible es el cierre a mercado de fin de día (`cableado.py:351-353`, registrado en :360 tras la última evaluación). | Sonda sin escribir (`uv run python -B -c …`): «racha tras 9 sin consultar ese dia 9 / dia siguiente, detenido: False racha 9 / una perdida mas: racha 10 detenido True». `src/botsito/engine/racha.py` (`_reiniciar_si_toca` exige `detenido_en`). |
| b5 | importa | Alcance (1). «El nivel se congela al tomarse» es una restricción que no sale de ningún ítem y no va rotulada como DECISIÓN DEL CONSULTOR, aunque la ordenó la respuesta (punto 1). Aparece como mecanismo sin rótulo en ADR-0084 §2, en la descripción de `liquidez_m15_mecha_que_vuelve` y en las notas de RN-004. Tiene efecto visible: una M1 que cierra con cuerpo sobre el nivel ORIGINAL deja de ser toma si una mecha anterior lo movió. | `docs/adr/0084-…md:41-46`; `parametros.yaml` (desc. del selector, «en cuanto una M1 lo cruza … el nivel se congela»); `test_pivotes_m15.py:222` («cierra sobre 134 pero no sobre 137: no es toma») |
| b6 | importa | El encargo pide un test de que «Lo que se llene en ese minuto lo cierra RN-002 en el evento siguiente». El test escrito usa el minuto ANTERIOR al último. Es «hecho de otra forma» (ya nada puede llenarse en el último minuto), pero no está en las «Desviaciones declaradas» ni se dice por qué. | encargo:87; `ACTIVAR-SESION-05-MOTOR.md:604-605` y :794-801 (no lo lista) |
| b7 | importa | La V preparada omite tres cosas que el encargo dicta, sin declararlo: «(este tag)», «sobre toda la construcción» y «diff contra CABLEADO-SIMULADOR-LINEA-BASE.txt». | encargo:123 frente a `ACTIVAR-SESION-05-MOTOR.md:729` |
| m1 | menor | En la lista de la sesión 6, S-15 lleva las opciones sin escribir: «(a) … (b) … (c) otra, ¿cuál?». | `ACTIVAR-SESION-05-MOTOR.md:714-715` |
| m2 | menor | Los 22.991 bytes de PS dependen de una frase de Current Feature SUPUESTA de 232 bytes y de una V de 378, que escrita mide 384: el margen real es de 3 a 9 bytes. El guion `medir_ps.py` no está en el repo. | informe:722-726 |
| m3 | menor | El encargo pide que `test_kit.py` vaya «con la salida»; el informe da solo «41 tests en verde». | encargo:110; informe:192, :820 |
| m4 | menor | La respuesta (punto 2) dice «El guion de CAJA-77 no se toca», y b18fe31 cambia `scripts/bloque_de_la_caja.py` (el Diagnostico, punto 10). El informe dice a la vez «el guion no se toca» (§1.2) y lo cambia (§1.7), sin conciliarlo. | `test_orden_stop_pivote.py:172,190` (`_cargar("bloque_de_la_caja")`); diff de `scripts/bloque_de_la_caja.py:265-267` |
| m5 | menor | No hay fila nueva en HOLDOUT-EXPOSICIONES por lo que leen `test_preparar_a35`/`test_visor` en los `make check` del 26 y 27 «con el motor nuevo», que el encargo nombra. El informe §5 lo remite a las filas fijas del 18 y del 26: es una desviación declarada, y el consultor decide si le basta. | encargo:115; informe:803-812 |

### Lo que no pude comprobar
- **La CI de Linux.** Pendiente: el informe dice «PENDIENTE» en §7.
- **Las versiones actuales de 4 tests contra el código de `main`** (`test_ultimo_minuto.py`, `test_mecha_que_vuelve.py`, `test_pivotes_m15.py`, `test_escenarios_por_sesion.py`). Habría que copiarlas al clon, y eso escribe; las copias de C:/cm/main son anteriores.
- **El commit desde el que se creó C:/cm/main.** `git -C C:/cm/main rev-parse` y `git worktree list` los bloqueó `solo_lectura.py`. Lo sustituye `git show main:src/botsito/domain/pivotes_m15.py | diff -q - C:/cm/main/…`, que sale IGUAL.
- **El sello de cada commit intermedio.** Solo existe el `make-check.log` del último, que sella `b18fe31^{tree}`. No ejecuté `make check` porque escribe.
- **Si el caso de b4 se da en el cableado real**, es decir, si un cierre a mercado de fin de día puede dar la novena pérdida.
- **`ventana_no_citable` por segmento.** Necesita la cruda de v15 y v16, que no se abre. Por tramos sí lo comprobé: los 9 ítems dan solape 0. El más cercano es ev-v16-002126 (0:21:26), a 10 s del fin del tramo 0:20:02-0:21:16; ev-v15-004037 acaba en 0:40:55 y el tramo siguiente de v15 empieza en 0:41:22.
- **`medir_ps.py`.** Está en la carpeta de trabajo de la sesión, no en el repo.

### Comandos ejecutados
1. `git branch --show-current && git merge-base main HEAD && git log --format='%h %s' main..HEAD && git status --short`
2. `git diff --stat main...HEAD`
3. Read de `docs/encargos/trabajo-activar-sesion-05-motor.md`, `contrato.yaml` y `docs/validation/ACTIVAR-SESION-05-MOTOR.md` (entero)
4. `uv run python scripts/contrato_rama.py`
5. `git log --format='%h %s%n%b%n-----' main..HEAD`
6. `git log --format='%h' --name-status main..HEAD -- knowledge/spec knowledge/cases knowledge/feedback knowledge/evidence knowledge/corpus data/manifests`
7. Glob `knowledge/evidence/**/ev-v1[56]-*`; Read de los 4 registros de feedback y de los 9 ítems citados; Read de `knowledge/corpus/tramos_no_citables.yaml`
8. Grep de `OBJETIVOS_POR_ACCION` y `PROCEDENCIAS` en `src/botsito/feedback/modelo.py`
9. `git diff main...HEAD -- knowledge/spec/strategy_spec.yaml`
10. Grep y Read de `src/botsito/spec/modelo.py` (las guardias y `CLAVES_VOCABULARIO`)
11. `git diff main...HEAD -- docs/adr/README.md docs/adr/0045* 0054* 0060* 0061* 0066* 0076* 0077*`
12. Read de ADR-0084, 0045, 0085, 0086, 0076 (1-66) y 0062 (1-60)
13. Grep «las 9 seguidas» en `knowledge/evidence/v15` y `v16`
14. `git diff main...HEAD -- docs/validation/ACTIVAR-SESION-05.md docs/runbooks/ACTIVAR-A35-A44.md docs/validation/HOLDOUT-EXPOSICIONES.md`
15. `grep -n -o` de los títulos de fila de `docs/validation/HOLDOUT-EXPOSICIONES.md`
16. `ls -la C:/cm/main`, `ls -la C:/cm/main/config C:/cm/main/data` (bloqueados por `solo_lectura.py`: `git worktree list` y `git -C C:/cm/main rev-parse HEAD`)
17. `git show main:src/botsito/domain/pivotes_m15.py | diff -q - C:/cm/main/src/botsito/domain/pivotes_m15.py`
18. `ls -la` de 6 tests en C:/cm/main; `diff -q` de 12 tests rama/clon; `diff` de los 3 que difieren
19. `cd C:/cm/main && uv run pytest -q -p no:cacheprovider C:/cm/main/tests/unit/test_velas_sin_cuerpo_m1.py …` (ImportError)
20. `cd C:/cm/main && uv run pytest -q -p no:cacheprovider` sobre `test_caja_lado_de_ruido.py`, `test_rn020_retira_pendiente.py` y `test_racha_perdidas.py` (14 FAILED)
21. `cd C:/cm/main && uv run pytest … test_caja_lado_de_ruido.py | grep "^E"`
22. `uv run pytest -p no:cacheprovider` en el repo sobre 11 ficheros (128 passed)
23. `cd C:/cm/main && uv run pytest` sobre `test_a21_series`, `test_orden_stop_pivote`, `test_rn035_ventana_fin` y `test_vida_de_la_orden` (10 FAILED)
24. Grep de `def test_las_series_de_m1_no_se_mueven` y `…m15…`
25. `git diff main...HEAD -- src/botsito/engine/{motor,arnes,visor,cableado,broker}.py`
26. Grep de `DatosMercado(` en `src` y `scripts`
27. `git diff main...HEAD -- src/botsito/domain/pivotes_m15.py src/botsito/domain/estructura_m1.py`
28. `git diff main...HEAD -- knowledge/spec/ambiguedades.yaml PROJECT_STATE.md`
29. `git show --stat` de 35211a0 y 5b44cd6
30. `diff <(sed -n '136,157p' encargo) <(sed -n '326,347p' informe)`
31. `git diff e8cde8b HEAD -- docs/encargos/trabajo-activar-sesion-05-motor.md`
32. `wc -c PROJECT_STATE.md`, `git show main:PROJECT_STATE.md | wc -c` y medidas de las líneas V/F/K; `uv run python -c` (longitud de la V propuesta: 384)
33. `git diff main...HEAD -- src/botsito/engine/{zonas,primitivas,racha}.py`
34. Grep y Read de `test_racha_perdidas.py`; sonda `uv run python -B -c` con `seguidor_del_registro` (sin escribir)
35. Read de `cableado.py:270-465` y Grep de `.registrar(` y `.detenido(`
36. Read de RN-036 y RN-035 en `strategy_spec.yaml`; Grep de «DESALINEADO|un minuto antes» es frase|HUECO»; `git show main:knowledge/spec/strategy_spec.yaml | grep -n "un minuto antes» es frase"`
37. `git diff main...HEAD -- knowledge/spec/parametros.yaml knowledge/spec/spec_manifest.yaml`
38. `uv run botsito feedback apply --sesion 2026-10-23-sesion-05 --check`
39. `uv run botsito feedback pending`
40. `uv run botsito knowledge validate` (stdout; exit=0)
41. `uv run pytest` sobre `tests/contract/test_spec_docs_generados.py`, `test_no_business_literals.py`, `test_provisional_cuelga_de_abierta.py`, `tests/unit/test_registro.py`, `test_hoja_preguntas.py`, `test_reabrir_y_fuente_documental.py`, `test_spec.py`, `test_spec_fidelidad.py`, `test_project_state.py` y `test_historia.py` (todo en verde)
42. `grep` de `SELLO`, `PICO`, `passed` y `CONTRATO` en `make-check.log`; `git rev-parse "b18fe31^{tree}" "7208db2^{tree}"`
43. `git diff main...HEAD -- scripts/`; Grep de `_cargar` en `test_orden_stop_pivote.py`
44. `uv run pytest` sobre `test_embudo_77`, `test_orden_stop_pivote`, `test_escenarios_por_sesion`, `test_vida_de_la_orden` y `test_estructura_m1` (54 passed)
45. `git show --stat` de e8cde8b, b18fe31, 7208db2, 4855860, dd2042f y 225ac79
46. Grep de líneas en `parametros.yaml:1348` y `strategy_spec.yaml:1048`

Ficheros clave: `C:\Users\USER\Desktop\Bot v3\knowledge\spec\strategy_spec.yaml` (línea 1022, b1), `C:\Users\USER\Desktop\Bot v3\docs\validation\ACTIVAR-SESION-05-MOTOR.md`, `C:\Users\USER\Desktop\Bot v3\src\botsito\engine\racha.py`, `C:\Users\USER\Desktop\Bot v3\knowledge\feedback\2026-10-23-sesion-05\`.

### Lo que se hizo con los hallazgos del revisor (2026-10-27)

Todo lo de abajo va en el commit que cierra este informe (el décimo de la rama), con su propio
`make check` y su run de la CI (§7). Los hallazgos que tocan la spec llevan `spec_version` 18.5.0
→ 18.5.1 (solo redacción: descripciones y notas), `spec manifest --escribir` y `spec docs
--escribir`.

- **b1 (bloquea) · Arreglado.** `strategy_spec.yaml`, notas de RN-035: la segunda aparición, en
  la RESERVA de la sesión 4, dice ahora «"un minuto antes" era entonces frase del consultor, y en
  la sesión 5 lo dijo el trader (arriba)»; ya no contradice la cita de la regla. §1.5 lo dice.
- **b2 (importa) · Contestado, no arreglado.** Los tres registros (72c9a9e8, 978be13f, 1526aa39)
  son inmutables tras su commit (CLAUDE.md, `knowledge/feedback/`: solo añadir). Lo que traen de
  más son notas de contexto, no cambian el objetivo, la acción, el valor ni la cita de ninguno.
  Cabe dejarlo así o superseder cada uno con un registro igual cuyas notas solo traigan lo de su
  ítem; lo decide el consultor. Desviación (h) de §4.
- **b3 (importa) · Arreglado.** (1) Dos tests nuevos del cargador en `test_mecha_que_vuelve.py`,
  por `arnes.dias_de_mercado` y `visor.Preparador.preparar`, con los tres cargadores de velas
  sustituidos por una serie sintética (nada toca `data/`): comprueban que el `DatosMercado` que
  llega al motor lleva el selector y el criterio de la toma del registro; en `main` fallan con
  `AttributeError` (§1.1 y §6). (2) Los tests de hoy copiados de nuevo a `C:/cm/main` y
  corridos uno a uno: `test_mecha_que_vuelve.py` y `test_pivotes_m15.py`, el mismo `ImportError`;
  `test_ultimo_minuto.py`, `5 failed, 2 passed`; `test_escenarios_por_sesion.py`, `4 failed, 15
  passed`; `test_racha_perdidas.py`, `5 failed, 9 passed`; las salidas, en §1.1, §1.4 y §1.5.
  (3) §1.3 y §6 dicen que los fallos del punto 4 con `main` son por el registro (el parámetro no
  existe), y remiten a §0.a para lo que `main` hace.
- **b4 (importa) · Arreglado.** `engine/racha.py`: `SeguidorRacha` recuerda el último tope con que
  se le consultó (`tope_visto`; la cifra sigue viniendo de la forma de RN-036) y
  `_detenida_antes_de` reinicia también cuando la racha está en ese tope o por encima y la última
  pérdida cayó en un día anterior, aunque nadie consultara `detenido` tras la novena. Test
  renombrado y reescrito: `test_el_reinicio_llega_aunque_nadie_consulte_despues_de_la_novena`
  (la novena sin consulta posterior; el día siguiente, tanto si lo primero es un cierre como una
  consulta, cuenta desde cero; y sin ninguna consulta nunca, la racha sigue). §1.4 lo cuenta.
- **b5 (importa) · Arreglado.** «El nivel se congela al tomarse» lleva el rótulo DECISIÓN DEL
  CONSULTOR (respuesta a la PARADA, punto 1; no sale de ningún ítem) en los tres sitios:
  ADR-0084 §2 (con su efecto visible), la descripción de `liquidez_m15_mecha_que_vuelve` y las
  notas de RN-004.
- **b6 (importa) · Declarado.** Desviación (f) de §4 y la frase en §1.5: en el último minuto no
  puede llenarse nada porque RN-035 retira en su primer evento; el test prueba el minuto anterior,
  que es el caso más cercano que existe.
- **b7 (importa) · Arreglado.** La V de §3 lleva «este tag», «sobre toda la construcción» y «diff
  contra CABLEADO-SIMULADOR-LINEA-BASE.txt»; K y la deuda se acortan para que quepa; medida de
  nuevo: 22.974 bytes (§3).
- **a1 (importa) · Arreglado.** Los shas de §1.2 a §1.7 son ahora los de cada punto (225ac79,
  5b44cd6, dd2042f, 4855860, 7208db2, b18fe31), y el «Estado» cuenta los commits.
- **a2 (importa) · Arreglado.** (1) La descripción de `racha_perdidas_reinicio` pone entre «» solo
  la cita del ítem; (2) ADR-0086 §2 cita «solo el del día y las 9 seguidas» con su id,
  `ev-v15-000856-ee8f7ba3` (el ítem que RN-020 ya citaba); (3) las notas de RN-037 ya no ponen
  entre «» la `afirmacion` del ítem.
- **a3 (menor) · Arreglado.** §6: 57 ficheros; §1.3 y §6: siete fallos en `test_caja_lado_de_ruido.py`
  con `main`; §3: la V medida tal como está escrita (396 bytes).
- **a4 (menor) · Arreglado.** El recuadro de ADR-0060 §5 dice la condición: con
  `orden_pendiente_al_abrir_sesion` = `se_retira` (el valor vigente; con `sigue_hasta_ventana_fin`
  RN-035 dispara sin retirar).
- **m1 (menor) · Arreglado.** §2, punto 5: las opciones (a), (b) y (c) de la pregunta de S-15,
  escritas.
- **m2 (menor) · Arreglado.** §3 trae la frase de `Current Feature` con la que se midió (213
  bytes) y el margen real (26 bytes); el guion `medir_ps.py` sigue en la carpeta de trabajo de la
  sesión y el informe lo dice.
- **m3 (menor) · Arreglado.** §6 trae la salida de `test_kit.py` en la rama: `41 passed in
  70.52s (0:01:10)`.
- **m4 (menor) · Declarado.** Desviación (g) de §4 y la frase en §1.2: «el guion no se toca» es
  su cálculo (R5 y R6); lo que cambia es cómo construye `Diagnostico` (punto 10).
- **m5 (menor) · Arreglado.** Fila del 2026-10-27 en HOLDOUT-EXPOSICIONES: lo que
  `test_preparar_a35.py` y `test_visor.py` leen en cada `make check` de la rama con el motor nuevo
  (las mismas velas: abril y el M1 de marzo para calentar). §5 remite a ella.

Lo que el revisor no pudo comprobar y sigue así: el sello de cada commit intermedio (cada uno se
commiteó tras su `make check` en verde, y el hook `pre-commit` no deja otro; solo queda en el
repo el `make-check.log` del último); `ventana_no_citable` por segmento (necesita la cruda, que
no se abre; por tramos, 0 solapes); y `medir_ps.py` (fuera del repo, a propósito: solo sirve a
este informe).

## Orden de cierre (consultor, 2026-10-27)

Copiada tal cual del mensaje de Aleks del 2026-10-27:

> Modelo: Fable 5.1 · Esfuerzo: alto (la misma sesión)
>
> Orden de cierre de trabajo/activar-sesion-05-motor (consultor, 2026-10-27). Tag: stable/F38f-activar-sesion-05-motor (comprueba que está libre en local y en origin). Cópiala al informe, en una sección «Orden de cierre», y sigue la skill cerrar-rama cuando lance /cerrar-rama.
>
> ANTES DEL CIERRE, en la rama, un commit propio con make check sellado (decisiones del consultor sobre lo que su auditor vio y el revisor no):
> 1. A-30 en knowledge/spec/ambiguedades.yaml (RESUELTA; antes, docs/runbooks/AMBIGUEDADES.md): la frase «"Un minuto antes" es frase del consultor y no se fija» pasa a decir que entonces lo era y que en la sesión 5 lo dijo el trader (RN-035, fb-2026-10-23-sesion-05-1526aa39), y «va a trabajo/activar-sesion-04-motor» pasa a «hecho en trabajo/activar-sesion-04-motor». Su estado no cambia. spec docs --escribir en el mismo commit.
> 2. Notas de RN-035: que la retirada un minuto antes se hace según orden_pendiente_al_abrir_sesion (con se_retira, el valor vigente), como ya dice el recuadro de ADR-0060 §5.
> 3. La descripción de cierre_h4_antelacion nombra también RN-035, RN-037 y en_el_ultimo_tramo_h4.
> 4. ADR-0077: recuadro en §6 («RN-020 no cambia»), que remite a ADR-0086, y una NOTA junto a la alternativa 4 de «Por qué descartamos» que diga que tras_la_detencion la adopta tras la respuesta del trader (fb-2026-10-23-sesion-05-978be13f). Fila del índice.
> 5. La pregunta de S-15 del informe (§2, punto 5) se rehace: el dibujo 1 (la alternancia dentro de un retroceso) sale, porque ya lo contestó en la sesión 4 (S-10, ADR-0076 §1); quedan dos preguntas separadas. Dibujo 2: «Después de la toma, el primer retroceso tiene alternancia; aparece un punto nuevo y su retroceso está limpio. ¿Entras en este segundo? (a) sí; (b) no; (c) otra, ¿cuál?». Dibujo 3: «La orden ya está puesta en el primer punto tras la toma y se llena con la primera vela verde del retroceso, antes de que haya alternancia. ¿Esa entrada vale? (a) sí; (b) no, había que esperar al punto siguiente; (c) otra, ¿cuál?». Los dos en M1, con el marco escrito en el dibujo.
> 6. b2: los registros 72c9a9e8, 978be13f y 1526aa39 se quedan como están, y también a9e4f879, que su auditor vio con lo mismo (la justificación del régimen con fb-…-ffab23dc); además, el literal de 72c9a9e8 empieza con la pregunta leída y su ítem no lleva la reserva de «mezcla». La desviación (h) de §4 se amplía con eso. Sin superseder: son notas de contexto y no cambian objetivo, acción, valor ni cita.
> spec_version según la regla del manifiesto (redacción), spec manifest --escribir, spec docs --escribir, knowledge validate antes de make check, trailer Fuente: fb-2026-10-23-sesion-05-1526aa39, fb-2026-10-23-sesion-05-978be13f, ADR-0086. Push a fix/activar-sesion-05-motor y su run con un gh run view suelto: verde salvo el fallo aceptado de state check, antes del merge.
>
> COMMIT DEL CONTRATO (punto Y de RITUAL), además de lo de siempre:
> - Las líneas de §3 tal cual: V, F, K (las dos negativas de §0.d), la línea de Technical Debt de ADR-0087, Current Feature con la fecha del cierre; Known Ambiguities sin cambio. PROJECT_STATE por debajo de 23.000 bytes, medido con wc -c: el margen es de 26 bytes, así que nada más entra en PROJECT_STATE; si no cabe, PARADA antes de recortar nada vivo.
> - Hoja de ruta: R4.1 con el Estado de §3 (sin «HECHA» a secas); R4.2 «Qué es» con lo de §2 y S-15 con los dos dibujos del punto 5; y en G.2 una viñeta nueva: «Una comprobación que compare las notas de cada registro de feedback con el ítem que cita (segunda rama seguida con notas que traen contenido de otros ítems: trabajo/activar-sesion-05 y trabajo/activar-sesion-05-motor)».
> - La NOTA del runbook ya entró en la rama: nada más.
>
> Hallazgos para ERRORES-RECURRENTES (fila de trabajo/activar-sesion-05-motor):
> - (importa, del consultor) El encargo puso un valor provisional bajo A-35 sin leer ADR-0045 ni ADR-0054, que lo prohibían. Lección: antes de proponer un valor provisional bajo una ambigüedad, se lee el ADR que la abrió.
> - (importa, del consultor) El auditor del consultor hizo un grep sobre la raíz de un clon y leyó el holdout sin imprimirlo (fila del 2026-10-26 de HOLDOUT-EXPOSICIONES). Lección: también el auditor del consultor busca solo sobre rutas literales.
> - (importa, del consultor) La respuesta a la PARADA ordenó «el nivel se congela al tomarse» sin rotularlo como decisión del consultor (lo cazó el revisor, b5). Lección: toda restricción que no sale de un ítem lleva su rótulo también en una respuesta a una PARADA.
> - (menor, del consultor) El encargo daba RN-011 como la regla que coloca (es RN-015) y pedía un test para algo que no puede pasar (lo llenado en el último minuto, b6). Lección: el mecanismo que nombra un encargo se lee en la spec antes de escribirlo.
> - (importa, de la sesión, lo cazó el auditor del consultor y no el revisor) La frase que el encargo mandaba quitar seguía en A-30 y en docs/spec/ambiguedades.md, y la pregunta de S-15 contradecía S-10. Lección para el revisor: una frase que el encargo manda quitar se busca en toda la spec y sus docs generados, no solo en la regla; y toda pregunta para el trader se cruza con lo que ya contestó.
> - (importa, de la sesión, lo cazó el revisor) Las notas de cuatro registros con contenido de otros ítems, segunda rama seguida (b2): pasa a «Patrones que ya se conocen», con su señal, y la guardia queda en G.2.
> - (importa, de la sesión, lo cazó el revisor) La racha solo se reiniciaba si se consultaba tras la novena, y el nombre del test prometía más (b4); los fallos con main de los puntos 1 y 4 eran de importación o de registro, no de comportamiento, y las copias del clon eran viejas (b3). Lección: el test que falla con main tiene que fallar por comportamiento y con la versión de hoy del test.
> - (menor, de la sesión) Tres make check perdidos por lint, mypy y tests no buscados antes. Lección: ruff format, ruff check y mypy sobre lo tocado, y git grep de los instantes y reglas que cambian, antes de make check.
> - Lo bueno: la fase 0 midió que S-15 no tenía frontera y que S-10 ya entra por el camino real; el predicado en_el_ultimo_tramo_h4 separa el límite sin cifra; y la PARADA corrigió dos errores del consultor antes de escribir código.
>
> Después del cierre: CI de main sobre el HEAD nuevo con un gh run view suelto; retira el clon C:/cm/main con git worktree remove; y el informe final con sha de main, tag, run de la CI de main, ramas que quedan (locales y fix/ en origin) y bytes de PROJECT_STATE.

## Estado

Rama lista para revisión, NO cerrada. Los once puntos del encargo aplicados según la respuesta del consultor del 2026-10-26, en diez commits sellados: e8cde8b (apertura), 53b879a (fase 0 y PARADA), 35211a0 (punto 1), 225ac79 (puntos 2 y 3), 5b44cd6 (punto 4), dd2042f (punto 5), 4855860 (punto 6), 7208db2 (puntos 8 y 7), b18fe31 (puntos 10 y 11), ce42294 (los arreglos del revisor, §8; CI run 40466482458, solo el fallo aceptado) y el commit de la orden de cierre (sus seis puntos: A-30, las notas de RN-035, `cierre_h4_antelacion`, ADR-0077 §6 y su NOTA, la pregunta de S-15 en §2 y la desviación (h); `spec_version` 18.5.2). CI de Linux por `fix/activar-sesion-05-motor`: §7 y el mensaje final. b2 decidido por el consultor (los registros se quedan). A la espera de `/cerrar-rama`.
