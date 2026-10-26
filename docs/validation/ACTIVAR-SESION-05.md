# ACTIVAR-SESION-05 · Las respuestas de la sesión 5 entran en la spec (R4.1, entrada V)

Rama `trabajo/activar-sesion-05`, abierta el 2026-10-25 desde `main` en b61c8f8 (commit de estado
sobre el merge baaf74b, tag `stable/F38d-sesion-05`). Encargo:
`docs/encargos/trabajo-activar-sesion-05.md`. Tramo: R4 (R4.1 de `docs/plan/HOJA-DE-RUTA.md`;
V de la Next Action).

Antes de abrir se comprobó con git (skill `abrir-rama`, paso 1):

- `git rev-parse --short main` = b61c8f8; `git rev-parse main origin/main` da dos veces
  b61c8f8626603cea57d3fd27c4bcc0b6d9dd93e8; `git status --short` vacío.
- El último tag de `docs/state/HISTORIA.md` es `stable/F38d-sesion-05`;
  `git rev-parse "stable/F38d-sesion-05^{commit}"` = `git rev-parse main^1` =
  baaf74b6009363a53a8f104c651657d7fc2745b8; `git ls-remote --tags origin stable/F38d-sesion-05`
  devuelve el tag.
- La CI de `main` sobre b61c8f8626603cea57d3fd27c4bcc0b6d9dd93e8: `gh run view 40266284524`
  suelto, `completed` / `success`, `headBranch` main, `headSha` el mismo.
- `git branch --list` solo da `main`; `git ls-remote --heads origin "fix/*"` sale vacío.

## 0. Fase 0 · Inventario medido, sin tocar spec, knowledge ni código

Medido el 2026-10-25 sobre la apertura de la rama (encima de b61c8f8). Lo leído: la extracción
(`SESION-05-EXTRACCION.md` §3 a §8, su §7.1 y su revisor), los 21 ítems de evidencia que el encargo
nombra (todos en `knowledge/evidence/v15/` y `v16/`, por Read), `ambiguedades.yaml` (A-1, A-13,
A-24, A-32, A-35, A-43, A-44, A-46, A-48, A-49, A-50, A-53, A-57), `parametros.yaml` (los 18
parámetros que la tabla cita), `strategy_spec.yaml` (RN-003, RN-004, RN-005, RN-007, RN-009, RN-020,
RN-035, RN-036), los ADR 0045, 0053, 0066, 0075, 0076, 0077, 0080, 0081 y 0083 y su índice, el motor
(`domain/pivotes_m15.py`, `domain/estructura_m1.py`, `engine/tope_trader.py`, `engine/diagnostico.py`,
`engine/zonas.py`, `engine/primitivas.py`, `engine/primitivas_broker.py`, `engine/cableado.py`,
`engine/interprete.py`, `cli.py`), `feedback/modelo.py` y `feedback/aplicar.py`, los tests que la
FASE 0 b.5 nombra y los que `grep` encontró además, `scripts/hoja_preguntas.py`,
`tests/unit/test_hoja_preguntas.py`, `tests/unit/test_en_parte_no_se_cierra.py`,
`tests/unit/test_hoja_de_ruta.py`, `docs/runbooks/ACTIVAR-A35-A44.md`, `AMBIGUEDADES.md`,
`docs/state/README.md`, `knowledge/corpus/libros.yaml` y `fuentes.yaml` (solo metadatos: ficheros,
fechas de grabación y `naturaleza`; ninguna fila de ningún libro), y los registros de feedback que el
encargo cita como precedente (`fb-2026-09-09-sesion-01-2ba4c3e7`, `-bff260ea`,
`fb-2026-10-04-sesion-04-8e2d728a`, `-ca0afae6`, `-c3d0c855`) y `ev-v9-004919-c6bfb3ee`. Los
`feedback trace` de A-32, A-35, A-44, A-57 y `perdida_maxima_semanal`. **Ninguna filtrada, ninguna
cruda, ningún fotograma, ningún libro, ningún caso; nada de julio, diciembre, marzo ni febrero.**
Las citas de este informe salen SOLO de los ítems de §8 de la extracción, con el texto de cada ítem.

### 0.a La tabla de activación

Una fila por código de `SESION-05-EXTRACCION.md` §5. «Destino» es la letra del encargo (A activar,
B rama de motor, C sesión 6, D líneas del cierre); «hoy» es lo que hace el código, con
`fichero:línea` de la rama (igual que `main`); «cuadra» dice si lo medido sostiene la decisión del
consultor y, si no, qué cambia (detalle en §0.b y en «Lo que necesito que decidas»).

| Código | Qué cierra o toca | Destino | Ítems que la citan | Qué hace hoy el código | Test que lo prueba | ¿Cuadra? |
|---|---|---|---|---|---|---|
| S-1 | RN-003 / ADR-0080 §9 (la contradicción con la sesión 1) | A.5 CONFIRM | `ev-v15-000049-3b294480`, `ev-v15-000138-ef123dfc` | `domain/sesgo.py`: con un extremo roto decide solo el color de esa ruptura; con el color contrario la búsqueda sigue (ADR-0080 §2 y §10); RN-003 `strategy_spec.yaml:996-1071` | `tests/unit/test_sesgo_h4.py::test_caso_3_rompe_el_maximo_y_cierra_roja_sigue_el_sesgo_que_habia` (:67) | Sí: (b) es lo que hace el motor. El objetivo del CONFIRM tiene que ser la regla RN-003: un ADR no es objetivo de feedback (`feedback/modelo.py:53-61`). Recuadro en ADR-0080 §9 |
| S-2 | ADR-0080 §4 (D3, la ruptura simple sin cuerpo) | A.5 CONFIRM | `ev-v15-000256-f3c52278` | `domain/sesgo.py`: la neutra simple no decide y la búsqueda sigue (ADR-0080 §4 y §10); RN-003 `entonces` (:1007-1009) | `test_sesgo_h4.py::test_ruptura_simple_sin_cuerpo_no_decide_y_la_busqueda_sigue` (:107) | Sí. CONFIRM sobre RN-003; el recuadro de §4 dice que el caso bajista no lo dijo con sus palabras |
| S-3 | A-35, primera mitad (bloqueante) | A.1 (parámetro) · B.1 (segunda mitad) · C | `ev-v15-000447-6699c708`, `ev-v15-000530-234d4a81`, `ev-v15-000553-9d95178a` | `domain/pivotes_m15.py`: la contraria CERRADA marca el extremo de la racha anterior y con `cierre_vela_contraria` está formado en su `fin` (:117-132); la vela sin cuerpo no es contraria y corta la racha (:127-128, :27-28); la mecha de la contraria NO mueve el nivel (:23-26, `_pivote_de` :86-101 toma el extremo de la racha). `liquidez_m15_pivote_formado` UNKNOWN (`parametros.yaml:495-512`); sin fijar el arnés y el visor se niegan (`engine/diagnostico.py:104-126`; `cli.py:2395`, `:2519`) | `tests/unit/test_pivotes_m15.py::test_lectura_cierre_ni_un_minuto_antes_del_cierre_de_la_contraria` (:76), `::test_lo_fijo_y_visible_doji_y_mecha_de_la_contraria` (:145); `test_preparar_a35.py` | Sí para la primera mitad: `cierre_vela_contraria` y «la sin cuerpo no cuenta» ya están en el motor. La segunda mitad («se actualiza el de la mecha») contradice :23-26: rama de motor (B.1). `feedback apply` admite el RESOLVE_UNKNOWN sobre el parámetro con la ambigüedad ABIERTA (`aplicar.py:160-169`, el valor en `opciones` :202-208; precedente A-43). Los tests que cambian: §0.b.5 |
| S-4 | A-44 (bloqueante) | A.2 · C | `ev-v15-000856-ee8f7ba3`, `ev-v15-000913-bdb12f92`, `ev-v15-001546-0dadd11e` | `engine/tope_trader.py:134-205` (`tope_del_registro`: el alcance decide `aplica_dia`/`aplica_semana`; la magnitud elige `vigilada = equity` o `saldo`, :255); el cableado evalúa con la PEOR equity del minuto (`cableado.py:299-306`); `primitivas_broker.py:343-370` (un alcance que no incluye el acumulador: NO); sin cuenta, `primitivas.py:314-325`. Los seis `perdida_trader_*` UNKNOWN (`parametros.yaml:1338-1402`) | `test_preparar_a44.py::test_cada_alcance_y_cada_unidad_se_leen_del_registro` (:155), `::test_alcances_unidades_y_magnitud_en_el_seguidor` (:226; saldo frente a equity :239-246) | Sí, con la magnitud declarada como lectura del consultor. Medido en §0.b.3: con `dia` y `saldo` no lanza, no lee `perdida_maxima_semanal`, y una caída en abierto que se recupera da `perdida_dia` 0 (con `equity`, 5,00). La procedencia del registro de la magnitud va a la PARADA |
| S-5 | A-57 (ADR-0081 D1) | A.3 | `ev-v15-001758-c27d9c4c` | `lote_si_no_cabe` = `limitar`, DEFAULT_AMBIGUOUS bajo A-57, categoría `ejecucion` (`parametros.yaml:1810-1829`); lo lee `primitivas_broker.py:524-527` y `:634`; `broker.py:177` lo comenta | `tests/unit/test_margen_lote.py::test_el_lote_se_limita_por_margen_por_volumen_y_por_los_dos` (:250), `::test_en_el_dia_sintetico_el_lote_se_limita_por_margen_y_se_coloca` (:270), `::test_con_no_operar_la_orden_que_no_cabe_no_se_envia_y_queda_anotada` (:324) | Sí: (a) = `limitar`. `feedback apply` no escribe un parámetro de `ejecucion` (`aplicar.py:187-192`): pasa a mano a CONFIRMED con fuente `decision` ADR-0081, que es lo que `test_registro.py:176-180` exige; `test_provisional_cuelga_de_abierta.py` exige que deje de ser DEFAULT_AMBIGUOUS. `test_margen_lote.py:315-321` busca `    valor: limitar` una vez: la línea no cambia. La respuesta lleva «creo», «por ahora» y vino tras la disyuntiva de Aleks: va a la PARADA como reserva, no como objeción |
| S-6 | ADR-0083 (pregunta 3 de PUNTO-USADO.md) | A.6 (recuadro) · C | `ev-v15-002029-1ac081ae`, `ev-v15-002441-2e609b87`, `ev-v15-002729-30480ec5` | `engine/zonas.py:434` `liberar_usada` (ADR-0083 D1: tras una pérdida o un break even el punto se vuelve a colocar, con la misma caja o con otra, sin número de reentradas) | `tests/unit/test_punto_usado.py::test_tras_una_perdida_el_mismo_punto_se_vuelve_a_colocar_con_la_misma_caja` (:191), `::test_tras_una_perdida_un_1_nuevo_coloca_otra_zona_del_mismo_punto` (:218), `::test_tras_un_break_even_el_mismo_punto_se_vuelve_a_colocar_igual_que_tras_la_perdida` (:244) | Sí: en parte; nada se registra; ADR-0083 sigue PROVISIONAL con su recuadro |
| S-7 | A-48 y A-49 | C | `ev-v15-003244-dcd8a834`, `ev-v15-003619-9fbc7f08` | `caja_bloque` = `r6` y `orden_stop_punto` = `ultimo_pivote_m1`, DEFAULT_AMBIGUOUS (`parametros.yaml:646-662`, `:624-640`); el 1 se recalcula en cada cierre de M1 (ADR-0074); `engine/zonas.py` `zona_del_punto` | `tests/unit/test_orden_stop_pivote.py` | Sí: en parte, nada se fija. `test_kit.py:446-449` exige que no haya ningún registro sobre A-49 |
| S-8 | VISOR-CONSTRUCCION.md §3.2, A | B.2 | `ev-v15-003959-5898c61e`, `ev-v15-004037-a2ab3980` | el doji corta la racha y no forma pivote (`pivotes_m15.py:127-128`); el impulso salta las de cuerpo cero pero una racha cortada no da el bloque que el trader ve (`estructura_m1.py:128-138`, `:268-291`) | `tests/unit/test_a21_series.py`, fila «alternancia con cuerpo cero en medio» | Sí: motor |
| S-9 | A-24 (DECIDIDA, ADR-0045) | A.5 CONFIRM | `ev-v15-004448-aac87b77` | `domain/pivotes_m15.py:176-198` `pivote_mas_reciente` (el más reciente del lado pedido) | `test_pivotes_m15.py::test_el_mas_reciente_del_lado_pedido_manda` (:123) | Sí en lo que hace el motor. **No cuadra la forma:** CONFIRM no admite objetivo `ambiguedad` (`modelo.py:66`), y A-24 es DECIDIDA: ADR-0045 dice que pasa a RESUELTA «solo con un registro del trader que apunte a ella». La cita lleva «por lo general». PARADA, punto 3 |
| S-10 | A-43, segunda parte | C | `ev-v15-005126-5baccf2a` | RN-004 `la_toma_es_de_la_sesion` con `toma_antes_de_la_ventana` = `cuenta` (`parametros.yaml:694`; `strategy_spec.yaml:1200-1203`) | `tests/unit/test_escenarios_por_sesion.py::test_la_toma_antes_de_la_ventana_la_decide_el_parametro` (:179) | Sí: en parte |
| S-11 | A-46 / ADR-0066 §1 | A.5 CONFIRM | `ev-v15-005839-f2e43c27` | RN-004 `la_toma_es_de_la_sesion` (`strategy_spec.yaml:1200-1203`): una toma de una sesión anterior del día no cuenta | `tests/unit/test_sesiones_independientes.py::test_liquidez_tomada_caduca_al_abrir_cada_sesion` (:114) | Sí: el motor hace (b). El objetivo del CONFIRM: la regla RN-004 (un ADR no es objetivo). A-46 no se reabre |
| S-12a | RN-005 | A.5 CONFIRM sobre RN-005 y CORRECT sobre `ev-v9-004919-c6bfb3ee` | `ev-v15-010104-23adba23` | `engine/zonas.py:522-540` `se_desarrolla_en_el_lado_de_ruido`: en una compra es ruido lo que queda POR ENCIMA del nivel tomado (:539) | `tests/unit/test_spec_fidelidad.py::test_rn005_prohibe_el_lado_de_ruido_y_no_el_de_la_operativa` (:58) | Sí. CORRECT sobre evidencia lo admite el modelo (`modelo.py:67`; precedente `fb-2026-09-09-sesion-01-2ba4c3e7`) |
| S-12b | A-50 | B.4 · C | `ev-v15-010451-5b123278` | `zonas.py:522-540` mira solo `e.entrada`, el 0 (:539) | — | Sí: motor, con A-50 ABIERTA |
| S-13 | A-53 | C | `ev-v15-010818-cc8e1e08`, `ev-v15-010850-f0728663` | `orden_pendiente_al_abrir_escenario` = `se_mueve`, DEFAULT_AMBIGUOUS bajo A-53 (`parametros.yaml:762-780`) | `tests/unit/test_escenarios_por_sesion.py` | Sí: en parte |
| S-14 | CORRIDA-CONSTRUCCION.md §4.5, p. 7 | D · C | `ev-v15-011023-5f0f2dd1`, `ev-v15-011728-b5bd4d05`, `ev-v15-011912-0ae32588`, `ev-v15-011956-dce80292`; el final de v16, `ev-v16-003421-b824b770` | nada en el código; la deuda «el no_trade por ausencia no está decidido» (`PROJECT_STATE.md:132`) | — | Sí; el recuento de libros, §0.b.7 |
| S-15 | CORRIDA §4.5, p. 8 / RN-009 | B.5 | `ev-v15-012616-d534455a` | `estructura_m1.py:141-158` `zonas_de_control` cuenta desde la toma; `:324-326` más zonas que `zonas_control_max_por_esquema` = 1 (`parametros.yaml:926-943`) → sin esquema | `test_a21_series.py` fila S-10 (2 zonas → None) | Sí: motor, con ADR que diga el alcance del recuento |
| S-16 | CORRIDA §4.5, p. 9 | C | — (no resuelve) | — | — | Sí |
| S-17 | A-13 | C | `ev-v15-013510-6364e7e0`, `ev-v15-013605-c041b814` | `break_even_condicion` = `tocar`, CONFIRMED (`parametros.yaml:851-861`; ADR-0065) | tests de `feature/be-al-tick` | Sí: no se toca |
| S-18 | A-32 | A.4 | `ev-v16-000234-9a4fa375`, `ev-v16-000603-6955d127` | `breaker_m1_criterio_ruptura` = `mecha` (`parametros.yaml:478-494`) → `_pasa` con MECHA (`estructura_m1.py:103-111`); `liquidez_m15_criterio_toma` = `cuerpo` (:513-523) → `cruza` (`pivotes_m15.py:208-218`). La única lectura que descarta una entrada por una mecha de M1 es `sin_mecha_mas_alla_del_extremo` (`estructura_m1.py:334`), INACTIVA: `zona_control_limpia` = `solo_una_zona_de_control` (`parametros.yaml:897-925`) | `test_pivotes_m15.py::test_toca_y_cruza_con_cuerpo_o_con_mecha` (:157); `test_a21_series.py` fila «breaker contrario (R) que rompe con mecha, retroceso limpio» → primer esquema; `::test_a21_queda_cerrada_con_la_opcion_que_ya_existia` | Sí: ningún código descarta por una línea de M1 rota con mecha. Quien la cita: `parametros.yaml:910` («que nivel era es A-32», descripción de `zona_control_limpia`), `scripts/hoja_preguntas.py:56` y su test (:29), `test_kit.py:313` (EN_PARTE_SESION_4) |
| S-19 | ADR-0076 §4, pregunta 1 | A.5 si el motor hace (b) → **medido (§0.b.4): no lo hace → B.9** | `ev-v16-000851-f5ae3b6f` | el doji corta la racha (`pivotes_m15.py:127-131`): la verde que sigue al doji no forma pivote, `zonas_de_control` cuenta 1 y el motor ENTRA (`estructura_m1.py:141-158`) | `test_a21_series.py`, fila «alternancia con cuerpo cero en medio (R, doji, V, R) y breaker V»: `segundo_esquema`, 1 zona, lectura literal «NO limpia», DISTINTO | **No cuadra con CONFIRM**: la (b) del trader («sigo como si no estuviera») deja R, V, R, que es la serie S-10 (2 zonas, sin esquema); el motor entra. Sin registro aquí; rama de motor (como prevé el encargo) |
| S-20 | ADR-0076 §4, pregunta 2 | B.8 · C | `ev-v16-001445-7ca4f033`, `ev-v16-001834-732a76b6` | `_pasa` con MECHA no mira el color de la vela que rompe (`estructura_m1.py:103-111`, `:321-323`) | `test_a21_series.py` fila «breaker contrario (R) que rompe con mecha, retroceso limpio (R, R)» → primer esquema | Sí: en parte; el motor ya rompe con la mecha de cualquier color (la rama de motor solo lo apunta) |
| S-21 | ADR-0077 §5 | B.6 | `ev-v16-001952-9fe00b36`, `ev-v16-002126-d2376f71` | `racha_perdidas_reinicio` = `nunca`, CONFIRMED (`parametros.yaml:1259-1273`); `engine/racha.py:79` `SeguidorRacha` (ADR-0077 §5: al día siguiente sigue en 9) | `tests/unit/test_racha_perdidas.py` | Sí: motor (opción nueva, CORRECT, recuadro ADR-0077 §5) |
| S-22 | RN-035 | B.7 | `ev-v16-002248-08e9600f`, `ev-v16-002323-515b9da4` | RN-035 retira la pendiente en `ventana_fin` (`strategy_spec.yaml:936-994`); el hueco del último minuto está congelado | `tests/unit/test_rn035_ventana_fin.py::test_hueco_la_orden_que_se_llena_en_el_ultimo_minuto_se_cierra_en_el_limite` (:72) | Sí: motor |
| S-23 | ADR-0075 | A.5 CONFIRM | `ev-v16-002521-02c1be20`, `ev-v16-002641-e8e6eafc` | `domain/sesgo.py`: la neutra de doble ruptura no decide y se cuenta (`saltadas_neutras_dobles`, ADR-0080 §10); RN-003 `entonces` | `test_sesgo_h4.py::test_una_neutra_mantiene_el_sesgo_anterior_alcista_y_bajista` (:249), `::test_dos_neutras_seguidas_mantienen_el_sesgo` (:267) | Sí. Objetivo: la regla RN-003; la reserva de `fb-2026-10-04-sesion-04-ca0afae6` (solo con sesgo alcista) queda contestada en las notas |
| S-24 | RN-007 (H) | B.3 | `ev-v16-002746-31cbc565`, `ev-v16-002841-8cfe382a` | RN-007 (`strategy_spec.yaml:1300-1329`): «casi plana» sin umbral, DESALINEADO CON EL MOTOR | — | Sí: motor; H sale en el cierre |
| S-25 | ENTRADA-JULIO.md §8 | D (lo mide T) | `ev-v16-003010-e455f173`, `ev-v16-003149-b3b79c79` | — | — | Sí |
| Para cerrar | NA:I, NA:Q, marzo | D | `ev-v16-003228-b515b93e`, `ev-v16-003249-49af3f8b`, `ev-v16-003421-b824b770` | — | — | Sí: NA:I y NA:Q no cambian; la medida de §3.5 se queda |

Lo que queda registrado SIN decidir aquí: `feedback trace` de A-32, A-35, A-44 y A-57 da «sin
registros de feedback» (la de A-44 de la sesión 3 no se registró: PARÓ, `ambiguedades.yaml:1282-1289`).

### 0.b Lo medido, punto por punto

**b.1 · Los registros de A.1, A.2 y A.3 se pueden escribir y aplicar así.** Medido en un clon
desechable, `C:/cm/rama` (`git worktree add --detach C:/cm/rama HEAD` sobre la apertura, con su
`config/settings.local.toml` apuntando al `corpus/` y al `data/` reales; skill `comparar-con-main`),
el 2026-10-26. Se crearon con `feedback new` seis registros de prueba, con las fechas del encargo
(v15: `--fecha 2026-10-23 --recibido-el 2026-10-23`; v16: `--recibido-el 2026-10-25`), la cita de su
ítem como `--respuesta` y `--procedencia trader_grabado`: RESOLVE_UNKNOWN sobre
`liquidez_m15_pivote_formado` = `cierre_vela_contraria` (A.1), sobre `perdida_trader_alcance` = `dia`,
`perdida_trader_unidad` = `porcentaje` y `perdida_trader_magnitud` = `saldo` (A.2, la magnitud en la
forma (a) para medirla), sobre A-57 (A.3, con `--valor`, que RESOLVE_UNKNOWN exige: `modelo.py:77`) y
sobre A-32 (A.4). Los seis se escribieron a la primera (`OK: knowledge/feedback/2026-10-23-sesion-05/
fb-…yaml`); sus ids no valen para la rama, porque el hash lleva el texto y se volverán a crear.

- `uv run botsito feedback apply --sesion 2026-10-23-sesion-05 --check`, tal cual:

  ```
  + liquidez_m15_pivote_formado  'cierre_vela_contraria'  <- fb-…-22770b9d
  + perdida_trader_alcance       'dia'  <- fb-…-15870e65
  + perdida_trader_magnitud      'saldo'  <- fb-…-b646f325
  + perdida_trader_unidad        'porcentaje'  <- fb-…-aa3ceca9
  4 parametros; 4 cambian, 0 ya estaban
  --check: no se ha escrito nada
  ```

  (Los ids van recortados a propósito: son los de los registros DE PRUEBA del clon, que no existen
  en el repositorio, y `knowledge validate` niega un id citado que no existe; el primer `make check`
  de esta fase 0 salió en rojo por eso, con cinco tests -`test_cli.py`, `test_citas_supersedidas.py`
  y `test_historial_sin_git.py`-, la misma lección que `SESION-05-EXTRACCION.md` §7.1.)

  Propone solo los cuatro parámetros; los dos registros sobre ambigüedades no entran (apply solo
  lee objetivos `parametro`, `aplicar.py:160-169`). Sin `--check` escribe los cuatro bloques
  (`estado: CONFIRMED`, `valor`, `fuente: {tipo: feedback, id: fb-…}`; diff de 20 líneas) y
  devuelve el trailer `Fuente:` con los cuatro ids. **El estado que queda:** los cuatro CONFIRMED por
  `feedback`, también la magnitud, que es lo que §0.e, 4, discute.
- `feedback pending` antes de aplicar lista los seis como pendientes («no lo cita todavia» los
  cuatro parámetros; «A-57 esta ABIERTA», «A-32 esta ABIERTA»); después de aplicar quedan los dos de
  las ambigüedades hasta que el YAML las dé RESUELTAS. **No se queja de un parámetro fijado con su
  ambigüedad ABIERTA** (A-35, A-44): cuenta los cuatro como reflejados (111 de 131 activos).
- `knowledge validate` con los seis registros y antes de aplicar: en verde (`OK: 182 registros de
  feedback, historial intacto, commits con Fuente`, exit 0). Después de aplicar y de dar RESUELTAS a
  A-32 y A-57 a mano: un solo `ERROR: spec: spec_manifest.yaml: el hash no coincide con los ficheros
  … si la spec cambio a proposito, sube spec_version y regenera` (exit 1). Es lo esperado y lo que
  cada commit hace (`spec manifest --escribir`); ningún otro error (`OK: registro con 109 parametros
  (13 sin confirmar)`; las ambigüedades y la evidencia en verde).
- **A-57 a mano:** `lote_si_no_cabe` ya lleva `fuente: {tipo: decision, id: ADR-0081}` en su estado
  DEFAULT_AMBIGUOUS (`parametros.yaml`, debajo de `consumido_por`); el cambio es `estado: CONFIRMED` y
  quitar `ambiguedad_id: A-57` (`config/registro.py` lo rechaza fuera de DEFAULT_AMBIGUOUS). Con eso y
  A-57 RESUELTA: `tests/contract/test_provisional_cuelga_de_abierta.py`, `test_registro.py` y
  `test_margen_lote.py` pasan en el clon (0 fallos; `test_registro.py` 51 tests); `test_hoja_preguntas.py`
  falla por A-32 (`HojaError: ya no se preguntan (estan RESUELTA): A-32`, dos tests), como manda
  AMBIGUEDADES.md.
- **Los tests de §0.b.5, medidos en el clon** (`uv run pytest <fichero> -q -rf`; «rama» = el clon con
  los valores; «main» = la rama real, donde el `make check` de la apertura dio 2918 passed):

  | Fichero | main | rama (clon) |
  |---|---|---|
  | `test_preparar_a35.py` | passed | 3 FAILED: `test_sin_fijar_el_motor_se_niega_nombrando_a35` («DID NOT RAISE SinFijarError»), `test_la_cli_se_niega_sin_lectura_y_no_escribe_nada` (`assert (0 == 2)`: a secas corre), `test_por_la_cli_en_diagnostico_todo_sale_etiquetado_si_hay_datos` (`assert 2 == 0`: el diagnóstico se rechaza) |
  | `test_preparar_a44.py` | passed | 7 FAILED: `test_sin_fijar_se_niega_nombrando_a44_y_el_diagnostico_corre`, `test_sin_tope_rn020_no_bloquea_ni_es_hueco`, `test_con_un_valor_concreto_rn020_prohibe_al_cierre_de_m1_siguiente_a_la_perdida`, `test_independiente_de_la_firma_se_aplica_el_que_se_toque_primero_y_la_traza_lo_dice`, `test_el_motor_de_la_spec_sin_cuenta_evalua_rn020_con_tope_y_sin_el_es_hueco`, `test_el_marcador_cero_se_alcanza_sin_perder_nada_y_rn020_bloquea_de_punta_a_punta`, `test_la_cli_se_niega_sin_a44_aunque_a35_vaya_en_diagnostico`. Pasa `test_sin_tope_fijado_ni_diagnostico_sigue_siendo_hueco_con_nombre` (construye el motor con `None`) |
  | `test_preparar_a21.py` | passed | 5 FAILED: los cuatro que pasan por `_motor` (`test_el_primer_esquema_forma_la_zona_y_rn011_la_liga_en_el_cierre_del_breaker`, `test_el_segundo_esquema_y_las_dos_zonas`, `test_las_dos_lecturas_de_a21_dejan_trazas_distintas_por_el_arnes_real`, `test_sin_mirar_al_futuro_la_zona_existe_desde_el_cierre_del_breaker_con_cada_lectura`) y `test_por_el_cableado_la_zona_llega_al_broker_como_una_orden_limite` |
  | `test_sesiones_independientes.py` | passed | 4 FAILED: los cuatro del fichero (todos pasan por `_motor`) |
  | `test_rutas_windows.py` | passed | 1 FAILED: `test_la_cli_se_niega_ante_una_ruta_larga_antes_de_leer_nada` |
  | `test_visor.py` | passed | 1 FAILED: `test_por_la_cli_sobre_un_dia_dev_de_construccion_si_hay_datos` |
  | `test_hoja_preguntas.py` | passed | 2 FAILED (A-32 RESUELTA, arriba) |
  | `test_cableado.py`, `test_racha_perdidas.py`, `test_umbral_mayo.py`, `test_diferencias_por_operacion.py`, `test_en_parte_no_se_cierra.py`, `test_margen_lote.py`, `test_registro.py`, `test_provisional_cuelga_de_abierta.py` | passed | passed (0 fallos) |
  | `test_kit.py`, `test_selector_orden_stop.py`, `test_renovar_cierres.py` | passed | **no medidos en el clon: la guardia los negó** («el codigo nombra la carpeta /» para `test_kit.py`; «recorre directorios que construye al ejecutarse y nombra material sensible» para los otros dos). Es la deuda K de la Next Action (la guardia no reconoce como tests los de un clon de `C:/cm/`), no se rodeó. Lo que cambia en ellos está razonado en §0.b.5 por el código (`EN_PARTE_SESION_4` y RESUELTAS; las dos opciones de diagnóstico en la CLI) |

  Veintitrés tests cambian de sentido (3 + 7 + 5 + 4 + 1 + 1 + 2), más los tres no medidos. Todos
  por lo previsto en §0.b.5; dos cifras cambian respecto a la previsión: en `test_preparar_a44.py`
  son 7 y no 8 (el del hueco con `None` no toca el registro), y en `test_preparar_a21.py` son 5 y
  no 2 (`_motor` lo usan cuatro tests).

**b.2 · El arnés a secas y con `--simular`.** En el mismo clon, con los cuatro valores aplicados,
sobre UN mes de construcción (`--meses 2026-04`; una corrida parcial no habilita nada, ADR-0070 §2;
§0.e, 14) y la salida fuera del repositorio, en `C:/cm/salida/`, que no se commitea ni se lee:

```
uv run botsito motor arnes --meses 2026-04 --salida C:/cm/salida/arnes-secas.txt
  OK: informe del arnes en C:\cm\salida\arnes-secas.txt
  TIEMPO: 72.4 s; MEMORIA: pico del proceso de 68.7 MiB
  exit=0
uv run botsito motor arnes --simular --meses 2026-04 --salida C:/cm/salida/arnes-simular.txt
  OK: informe del arnes en C:\cm\salida\arnes-simular.txt
  TIEMPO: 171.5 s; MEMORIA: pico del proceso de 235.2 MiB
  exit=0
```

Los dos corren a secas (código 0), el fichero se llama como se pidió (sin `.DIAGNOSTICO.` en el
nombre) y `grep -c DIAGNOSTICO` da 0 en los dos. De su contenido solo se leyó eso y el número de
líneas (159 y 542): ninguna cifra de cobertura, de operaciones ni de veredicto. La lectura del M1 de
marzo para calentar abril está declarada en `HOLDOUT-EXPOSICIONES.md` (fila del 2026-10-26), escrita
antes de correr.

**b.3 · `tope_del_registro` con alcance `dia` y magnitud `saldo`.** Sobre un registro SINTÉTICO (el
helper `_registro_sintetico` de `tests/unit/test_preparar_a44.py`, en una carpeta temporal del
sistema), con un guion de la carpeta de trabajo (`medir_b3.py`) que envuelve los accesores de
`Registro` para anotar qué lee. Salida, tal cual:

```
descripcion: tope del trader: dia, sobre saldo, en porcentaje; dia 4.5 sobre saldo_inicial_dia; reinicio en Europe/Prague; SUPUESTO: reinicio con el huso de corte del perfil (el trader no dijo otro)
tope_dia: 4.5 | tope_semana: None
aplica_dia: True | aplica_semana: False
leidos del registro, en orden: ['opcion:perdida_trader_alcance', 'opcion:perdida_trader_magnitud', 'opcion:perdida_trader_unidad', 'porcentaje:perdida_maxima_diaria', 'texto:perdida_trader_reinicio_huso', 'opcion:base_calculo_perdida_diaria', 'opcion:base_calculo_perdida_semanal']
lee perdida_maxima_semanal: False
acumuladores (saldo intacto, equity -5000): {'perdida_dia': Decimal('0'), 'perdida_dia:tope': Decimal('4.5')}
acumuladores (saldo -5000, equity -5000): {'perdida_dia': Decimal('5.00'), 'perdida_dia:tope': Decimal('4.5')}
acumuladores (saldo -4500 = 4,5 %): {'perdida_dia': Decimal('4.500'), 'perdida_dia:tope': Decimal('4.5')}
EQUITY acumuladores (saldo intacto, equity -5000): {'perdida_dia': Decimal('5.00'), 'perdida_dia:tope': Decimal('4.5')}
```

- No lanza: `tope_del_registro` lee alcance, magnitud y unidad; con `dia` lee `perdida_maxima_diaria`
  y NO `perdida_maxima_semanal` (`tope_trader.py:179-190`: la rama `SEMANA, AMBOS` no se entra);
  `perdida_trader_reinicio_huso` UNKNOWN cae en `ParametroDesconocidoError` y el huso pasa a ser el
  del perfil, marcado SUPUESTO (:191-194). Lee siempre `base_calculo_perdida_semanal` (:202),
  aunque no la use.
- Con `alcance = dia`, `perdida_maxima_semanal` = 9 no se lee en ninguna parte: el acumulador
  `perdida_semana` da NO en el motor de la spec (`primitivas.py:316-318`) y en el cableado
  (`primitivas_broker.py:358-360`), y la segunda rama del `cualquiera_de` de RN-020 es NO, no
  DESCONOCIDO: ningún hueco con nombre.
- La magnitud: con `saldo`, una caída en abierto de 5.000 que se recupera deja `perdida_dia` en 0;
  con `equity` da 5,00 % y RN-020 pararía el día. Es exactamente lo que el encargo dice que no es
  inocuo, y es el test sintético que pide («TESTS QUE ROMPEN A PROPÓSITO», tercero).
- Una forma de CORRECT que deje `perdida_maxima_semanal` «sin efecto limpiamente»: no la hay. Es
  `porcentaje` con `minimo: "0"`; un `0` sería un tope que se alcanza con cualquier pérdida (y con
  ninguna: `perdida >= umbral` con 0, `primitivas.py:325`), no «no hay». Cuadra con la decisión de
  dejarlo CONFIRMED en 9 y sin efecto por el alcance, declarado como desviación del runbook §1.

**b.4 · S-19 con `test_a21_series.py`.** `uv run pytest tests/unit/test_a21_series.py -q -rA`:
28 passed. Las filas que importan, tal cual las nombra el test (compra y venta):

```
PASSED ...[compra-S-10: V, R, V, R y breaker V-pasos0-None-2-False-RVR-True]
PASSED ...[compra-alternancia con cuerpo cero en medio (R, doji, V, R) y breaker V-pasos5-segundo_esquema-1-False-RVR-False]
```

Lo que dicen: con R, doji, V, R y breaker V el motor da `segundo_esquema` con **1 zona de control**
(entra), y la lectura literal «sin alternancia, saltando las de cuerpo cero» da NO limpia (RVR):
DISTINTO. La (b) del trader («no cuenta, sigo como si no estuviera», `ev-v16-000851-f5ae3b6f`) es
esa lectura literal: quitado el doji queda R, V, R, que es la serie S-10 (`None`, 2 zonas, no
entra). El motor hace lo contrario porque el doji corta la racha (`pivotes_m15.py:127-131`) y la
verde que le sigue no forma el pivote que `zonas_de_control` contaría (`estructura_m1.py:155-157`).
**El motor NO hace (b): S-19 no se registra aquí y va a la rama de motor (B.9)**, como el encargo
prevé en A.5.

**b.5 · Todos los tests que cambian al fijar A-35 y A-44.** Uno a uno, con lo que cambia. El orden
de las compuertas en la CLI (`cli.py:2391-2405` arnés, `:2509-2530` visor): construcción →
`lectura_pivote` (A-35) → `tope_del_registro` (A-44) → `lectura_limpia` → tipo de orden (A-47, solo
`--simular`) → ruta de salida → velas. Con A-35 fijada, `lectura_pivote` RECHAZA `--diagnostico-a35`
(`diagnostico.py:111-116`) antes de todo lo que va detrás; con A-44 fijada, `tope_del_registro`
rechaza `--diagnostico-a44` (`tope_trader.py:140-144`).

| Test | Qué comprueba hoy | Qué cambia |
|---|---|---|
| `test_preparar_a35.py::test_sin_fijar_el_motor_se_niega_nombrando_a35` (:335) | con el registro REAL, `lectura_pivote` lanza `SinFijarError` y con `Diagnostico(a35=…)` corre | FALLA al fijar A-35: pasa a comprobar que el registro real da `cierre_vela_contraria` y que el diagnóstico se RECHAZA (lo que el test sintético de :342 ya comprueba) |
| `test_preparar_a35.py::test_la_cli_se_niega_sin_lectura_y_no_escribe_nada` (:388) | mes de medida con `--diagnostico-a35`: MEDIDA (sin cambio); mes de construcción a secas: exit 2 nombrando A-35; el visor a secas: exit 2 o 3 | el mes de construcción a secas ya no se niega por A-35 (ni por A-44 tras A.2): corre, y necesita `data/` (se salta sin ella, como los demás); el visor a secas sobre `--todos` o un caso, igual. Se reescribe: a secas corre, y «la compuerta de construcción manda primero» sigue |
| `test_preparar_a35.py::test_por_la_cli_en_diagnostico_todo_sale_etiquetado_si_hay_datos` (:419) | con `data/`: `--diagnostico-a35 … --diagnostico-a44 sin_tope` corre etiquetado y no existe el fichero a secas | con los dos fijados el diagnóstico se rechaza (exit 2, «ya esta fijado»): se reescribe al revés, a secas corre (código 0), el fichero se llama como se pidió, ninguna línea lleva `[DIAGNOSTICO`, y el diagnóstico se rechaza sin escribir nada |
| `test_preparar_a44.py::test_sin_fijar_se_niega_nombrando_a44_y_el_diagnostico_corre` (:122) | con el registro REAL, `TopeSinFijarError` y los dos modos de diagnóstico | FALLA al fijar A-44: pasa a comprobar `dia`/`saldo`/`porcentaje`, `tope_dia` 4,5, `tope_semana` None, el huso SUPUESTO y el rechazo del diagnóstico |
| `test_preparar_a44.py` :277, :296, :317, :345 (motor cableado) y :358, :380 (motor de la spec) | construyen el tope con `tope_del_registro(registro REAL, …, Diagnostico(a44=…))` | con `perdida_trader_alcance` fijado, `tope_del_registro` lanza `TopeRechazadoError` (:140-144): los seis FALLAN. Cambio a propósito: el tope hipotético se construye sobre un registro SIN A-44 (copia del real con los tres `perdida_trader_*` a UNKNOWN, el patrón de `_registro_con_a47_unknown` de `test_selector_orden_stop.py`), o directamente con `TopeTrader(...)` como ya hace `_tope()` (:187). El sentido de cada test no cambia; lo que prueban son los tres estados del tope sobre el cableado |
| `test_preparar_a44.py::test_la_cli_se_niega_sin_a44_aunque_a35_vaya_en_diagnostico` (:407) | `--diagnostico-a35` solo: exit 2 nombrando A-44 | con A-35 fijada el diagnóstico de A-35 se rechaza ANTES de llegar a A-44 (exit 2, «ya esta fijado … no admite --diagnostico-a35»): cambia de sentido en el commit de A-35 (a secas se niega nombrando A-44) y otra vez en el de A-44 (a secas corre; el diagnóstico se rechaza). Dos toques, si los commits van separados |
| `test_preparar_a21.py::_motor` (:154-162, lo usan cuatro tests) y `::test_por_el_cableado_la_zona_llega_al_broker_como_una_orden_limite` (:294) | tope con `Diagnostico(a44=SIN_TOPE)` sobre la copia del registro real | `TopeRechazadoError` al fijar A-44 (la copia solo cambia `orden_limite_nace`): los cinco FALLAN (medido, §0.b.1) y pasan a `tope_del_registro(registro, huso)` a secas; sobre un día sintético sin pérdidas el tope del día no dispara, así que lo que prueban no cambia |
| `test_preparar_a21.py::test_la_cli_no_conoce_diagnostico_a21_y_la_compuerta_de_medida_manda` (:411) | argparse rechaza `--diagnostico-a21`; un mes de medida con `--diagnostico-a35/-a44` se niega por MEDIDA | NO cambia: la compuerta de construcción va antes que `lectura_pivote` (`cli.py:2391` frente a `:2395`), y argparse antes que todo |
| `test_sesiones_independientes.py::_motor` (:104-111, lo usan los cuatro tests del fichero) | tope con `Diagnostico(a44=SIN_TOPE)` sobre la copia del registro real (:39-48) | `TopeRechazadoError` al fijar A-44: los cuatro FALLAN (medido); a secas, como en `test_preparar_a21.py` |
| `test_selector_orden_stop.py::test_la_cli_se_niega_sin_a47…` (:141-146) | CLI con `--diagnostico-a35 … --diagnostico-a44` sobre una copia del registro con A-47 UNKNOWN; espera «A-47» | al fijar A-35, `lectura_pivote` rechaza el diagnóstico antes de llegar a A-47 (exit 2, pero sin «A-47» en el error): quitar las dos opciones; la negativa de A-47 sigue igual |
| `test_selector_orden_stop.py::test_la_cli_con_a47_fijada_pasa_a_pedir_a27` (:180-185) | lo mismo, con el perfil sin stops level; necesita `data/` | igual: quitar las dos opciones |
| `test_renovar_cierres.py::test_simular_un_dia_posterior_a_hasta_sale_con_2_y_lo_nombra` (:185-190) | CLI con los dos diagnósticos; espera «dias fuera del calendario de cierres» | el rechazo del diagnóstico llega antes que el calendario: quitar las dos opciones |
| `test_rutas_windows.py::test_la_cli_se_niega_ante_una_ruta_larga_antes_de_leer_nada` (:69-93) | arnés y visor con `--diagnostico-a35/-a44` y una carpeta larga; espera el LIMITE en el error | el rechazo del diagnóstico llega antes que `comprobar_ruta` (`cli.py:2395` frente a `:2404`): quitar las opciones; la carpeta sigue pasando del límite sin rótulo (el test la construye con 40 de margen). `_mas_largas()` y los dos tests de `nombre_etiquetado` no cambian (funciones puras) |
| `test_visor.py::test_por_la_cli_sobre_un_dia_dev_de_construccion_si_hay_datos` (:368) | a secas exit 2; con los dos diagnósticos corre y la página lleva el rótulo | a secas corre (código 0) y la página vuelve a llamarse `<caso>.html`, sin `DIAGNOSTICO` en el cuerpo; el diagnóstico se rechaza. Es lo que el runbook §2 anuncia |
| `test_kit.py::test_ambiguedades_reales_y_esquema` (:360) | bloqueantes ABIERTAS == {A-35, A-44} | NO cambia: las dos siguen ABIERTAS. Las RESUELTAS (:281-307) ganan A-32 y A-57 |
| `test_kit.py::test_una_en_parte_no_entra_en_resueltas` (:434-455) con `EN_PARTE_SESION_4` (:313) | ninguna de las ocho «en parte» de la sesión 4 está en RESUELTAS ni RESUELTA en el YAML; ningún registro sobre A-49 | A-32 está en ese conjunto y la sesión 5 la RESUELVE (S-18): el conjunto pierde A-32, con su comentario (la 4 la dejó en parte, la 5 la cierra); el resto no cambia. Es un test de A.4, no de A-35/A-44 |
| `tests/contract/test_provisional_cuelga_de_abierta.py` | todo DEFAULT_AMBIGUOUS cuelga de una ABIERTA | con A-57 RESUELTA, `lote_si_no_cabe` no puede seguir DEFAULT_AMBIGUOUS: pasa a CONFIRMED con `decision` ADR-0081 (A.3) y el test sigue en verde |
| `test_registro.py::test_fichero_real_cada_valor_de_estrategia_cita_al_trader` (:157-180) | estrategia con valor → fuente feedback/evidence; no estrategia con valor → fuente decision | en verde con lo previsto: `liquidez_m15_pivote_formado` y los tres `perdida_trader_*` CONFIRMED por `feedback` (apply los escribe así, `aplicar.py:300-305`); `lote_si_no_cabe` (`ejecucion`) con `decision` |
| `test_cableado.py::test_la_etiqueta_de_la_cuenta_diaria` (:781), `test_diferencias_por_operacion.py` (:341-357), `test_umbral_mayo.py` (:168-175) | etiquetas y nombres de `Diagnostico`; la lista de opciones del parser; una corrida con `--diagnostico-a35` sale «no» | NO cambian: no leen el registro, y las opciones siguen en el parser (ADR-0070 D2 las sigue negando) |
| `test_racha_perdidas.py` | `seguidor_del_registro` (la racha), no el tope | NO cambia |
| `test_hoja_preguntas.py` (:27-32) y `scripts/hoja_preguntas.py` (:54-59) | la hoja lleva A-32 | A-32 RESUELTA hace fallar la hoja («ya no se preguntan»): sale de `ORDEN_SESION_02` y de `ORDEN` (A.4). A-57 no está en la hoja |
| `test_en_parte_no_se_cierra.py` | ninguna «solo en parte» está RESUELTA; la sesión 4 deja A-32 en parte | NO cambia: la 5 da S-18 como «resuelve», y el test de la 4 lee solo su informe |

Fuera de `tests/`, tres guiones construyen `Diagnostico(a35=…, a44=…)` contra el registro real y
dejarán de correr con los valores fijados: `scripts/embudo_77.py:435` (su comentario :424 ya lo
prevé: «el diagnostico se rechaza, y este script dejo de correr»), `scripts/caja_77_exploratoria.py:132`
y `scripts/bloque_de_la_caja.py:266`. No son tests ni están en el contrato; se declaran aquí para la
rama de motor. Y el comentario de `src/botsito/engine/broker.py:177` («DEFAULT_AMBIGUOUS bajo
A-57») queda viejo con A.3; `src/` está protegido: a la rama de motor.

**b.6 · Quién espera cada ambigüedad que se cierra y cada parámetro que se fija** (`grep -rn` de
A-32, A-57, `liquidez_m15_pivote_formado`, `perdida_trader_`, `lote_si_no_cabe` en `CLAUDE.md`,
`docs/runbooks/`, `PROJECT_STATE.md` y `docs/plan/HOJA-DE-RUTA.md`):

- `CLAUDE.md`: nada.
- `PROJECT_STATE.md`: la V de la Next Action (:54, nombra A-32 entre las «en parte» y A-57); las
  filas de A-32 (:82) y A-57 (:93) de Known Ambiguities, que salen en sus commits.
- `docs/plan/HOJA-DE-RUTA.md` (no se toca en la rama): R1.1 Refs `ID:A-32` (:45) y su Estado HECHA
  que cuenta A-32 entre las «en parte» (:61, historia); R3.3 Estado «A-57 abierta para la sesión 5»
  (:178, historia); R4.1 Refs `ID:A-32 · ID:A-57` (:200-201) y su «Qué es» (:212); R6a.6 Refs
  `ID:A-57` y «con el valor que deje A-57» (:335-337: el valor que deja es `limitar`, y la línea
  sigue siendo verdad); el carril de guardias (:474, historia de la hoja de preguntas). Los `ID:`
  siguen existiendo tras cerrar, así que `test_hoja_de_ruta.py` (problemas_b, :156-157) no obliga a
  quitarlos; el encargo deja quitarlos del R4.1 «si el test lo pide»: no lo pide.
- `docs/runbooks/ACTIVAR-A35-A44.md`: el runbook entero (§0 «tiene que salir A-35 sin fijar», §1 y
  §2). Queda VIEJO al activar; no está en `rutas_permitidas`. PARADA, punto 6.
- `docs/runbooks/ERRORES-RECURRENTES.md:90`: la fila de `trabajo/barrido-sesion-5` (historia).
- En la spec (`knowledge/spec/`, permitida): `parametros.yaml:910` (A-32 en la descripción de
  `zona_control_limpia`), `:1825-1828` (A-57 en `lote_si_no_cabe`), `strategy_spec.yaml:1488`
  («DEFAULT bajo A-57» en la descripción del lote de RN-011), las notas de RN-004 y el token
  `liquidez_m15` (A-35), RN-020 y los acumuladores (A-44), y el comentario de cabecera de los seis
  `perdida_trader_*` (`parametros.yaml:1334-1337`).

**b.7 · El recuento de S-14, por `libros.yaml` y sin abrir filas.** `knowledge/corpus/libros.yaml`
tiene cinco libros; de construcción (`HOLDOUT-EXPOSICIONES.md`: enero, abril, julio y agosto), cuatro.
Qué backtest viene de una grabación en vídeo, por `fuentes.yaml` (`naturaleza`) y `libros.yaml`:

| Libro (construcción) | Grabado en vídeo | De dónde sale |
|---|---|---|
| Enero 2026 (`ENERO 2026.xlsx`) | No | ningún vídeo del backtest; v4 es «entrevista … sobre el backtest de enero en FXReplay» (`fuentes.yaml:32`), no la grabación de hacerlo |
| Abril 2026 (`ABRIL 2026.xlsx`) | No | ningún vídeo lo nombra |
| Julio 2026 (`JULIO_2026.xlsx`) | Sí, según el trader | v11, v12 y v13 (`fuentes.yaml:119-145`): «parte del backtest del 1 al 17 de julio que exporta el xlsx del mes (no comprobado: lo comprueba la rama que lo transcriba)», y v14 el tramo final sin xlsx. Lo comprueba T (R2.4) |
| Agosto 2026 (`AGOSTO 2026.xlsx`) | No el libro que hay | v7 y v8 (`fuentes.yaml:52-79`) graban en la sesión 2 un backtesting de la segunda mitad de agosto, y S-16 de la sesión 4 lo da por bueno; pero su exportación no ha llegado (NA:Q) y el libro de agosto que mide hoy es anterior |
| Mayo 2026 | No | reservado (ADR-0043); no es de construcción |

Lo que S-14 añade: en los backtests NO grabados en vídeo el trader se saltaba las sesiones que iban a
acabar en break even («me he saltado … en lugar de poner break even no he operado … no se ve
reflejado en el backtest», `ev-v15-011023-5f0f2dd1`; `ev-v15-011912-0ae32588`), y en los grabados
en vídeo no («en los últimos partes que se ha enviado con vídeo y todo pues no se está tal cual»,
`ev-v15-011956-dce80292`; el final de v16, `ev-v16-003421-b824b770`). Para F26: de los cuatro libros
de construcción, uno (julio) es de la clase «grabado en vídeo», y solo según el trader hasta que T lo
compruebe; enero, abril y el agosto que hay son de la clase en que faltan sesiones de break even.

### 0.c `PROJECT_STATE.md` y los 23.000 bytes

`main` lo tiene en 24.412 bytes; en la rama, con el `Current Feature` de la apertura, 24.537 (el
cierre lo vuelve a sustituir, hacia unos 300). Medido con `wc -c` línea a línea (bytes UTF-8):

| Movimiento del cierre | Bytes |
|---|---|
| Sale la V larga (:54) | −1.537 |
| Sale H (:50) | −482 |
| Salen las filas de A-32 (:82) y A-57 (:93) | −93, −139 |
| Entra la V corta (borrador en §«Las líneas para el commit del contrato») | +≈400 |
| Entra la línea de S-14 en G (:40, hoy 681) | +≈250 |
| Entra la línea de S-14 en la deuda del `no_trade` (:132, hoy 91) | +≈230 |
| F cambia de texto (:32, hoy 90) | ≈0 |
| `Current Feature` del cierre en lugar del de la apertura (:10, 449) | −≈150 |
| **Resultado** | **≈23.030** |

Queda unos 30 bytes por encima de 23.000 (y la cifra exacta depende de las líneas finales). Lo que
propongo mover por su régimen, sin quitar nada vivo (`docs/state/README.md`: lo que deja de ser
verdad se sustituye; la historia vive en `HISTORIA.md`):

1. La segunda frase de la introducción de Technical Debt (:99, 271 bytes): «Lo que no era deuda,
   desde trabajo/previa-sesion-5: … tabla en PREVIA-SESION-5.md §6» (≈200 bytes). Es historia de
   una limpieza ya hecha, y PREVIA-SESION-5.md §6 la conserva.
2. La deuda «LA SERIE DEL TRADER ES OANDA … Y EL RELOJ DE SU GRAFICO ES UTC+2 FIJO» (:129, 228
   bytes): la parte del reloj está pagada (ADR-0069) y la propia línea lo dice; se deja solo la
   parte viva de la serie (≈110 bytes).

Con las dos, ≈22.700. Si se prefiere no tocarlas, cabe la alternativa de llevar a HISTORIA el
párrafo «Candidatas a ambiguedad sin abrir» (:96, 554 bytes) dejando un puntero de una línea; son
candidatas vivas, así que lo recomiendo menos. PARADA, punto 7.

### 0.d El plan de commits

| # | Commit | Qué lleva | `Fuente:` |
|---|---|---|---|
| 1 | apertura (hecho) | encargo, contrato, Archivo 47, artefacto | — |
| 2 | fase 0 (este) | §0 del informe y la fila de HOLDOUT-EXPOSICIONES | — |
| 3 | A-35 | el registro sobre `liquidez_m15_pivote_formado`; `feedback apply`; notas de A-35, RN-004, el token `liquidez_m15` y la descripción del parámetro (con «desviación»); `spec_version` 18.1.3 → 18.1.4, manifiesto y docs; los tests de §0.b.5 que cambian con A-35 (`test_preparar_a35.py`, `test_selector_orden_stop.py`, `test_renovar_cierres.py`, `test_rutas_windows.py`, `test_visor.py`, y la primera reescritura de `test_preparar_a44.py::test_la_cli_se_niega_sin_a44…`) | el `fb-*` nuevo, ev-v15-000447-6699c708, ev-v15-000530-234d4a81 |
| 4 | A-44 | los tres registros (`perdida_trader_alcance`, `_unidad`, `_magnitud`); `feedback apply`; notas de A-44, RN-020, los acumuladores, la descripción de `perdida_maxima_semanal` (desviación del runbook §1) y el comentario de cabecera de los `perdida_trader_*`; `spec_version`; `test_preparar_a44.py` (los siete tests medidos), `test_preparar_a21.py` (cinco), `test_sesiones_independientes.py` (cuatro); el test sintético saldo/equity | los tres `fb-*`, ev-v15-000856-ee8f7ba3, ev-v15-000913-bdb12f92, fb-2026-09-09-sesion-01-bff260ea, fb-2026-10-04-sesion-04-8e2d728a |
| 5 | A-57 | el registro sobre A-57; `lote_si_no_cabe` a CONFIRMED con `decision` ADR-0081 a mano; `ambiguedades.yaml` RESUELTA; fila fuera de Known Ambiguities; descripción del lote en RN-011 (`strategy_spec.yaml:1488`); `test_kit.py` RESUELTAS; recuadro en ADR-0081 (D1 deja de ser PROVISIONAL) y su fila del índice; `spec_version` | el `fb-*`, ev-v15-001758-c27d9c4c, ADR-0081 |
| 6 | A-32 | el registro sobre A-32; `ambiguedades.yaml` RESUELTA; fila fuera; `parametros.yaml:910`; `scripts/hoja_preguntas.py` y `test_hoja_preguntas.py`; `test_kit.py` (RESUELTAS gana A-32, EN_PARTE_SESION_4 la pierde); `spec_version` | el `fb-*`, ev-v16-000234-9a4fa375, ev-v16-000603-6955d127 |
| 7 | las confirmaciones | los CONFIRM de S-1, S-2, S-9, S-11, S-12a, S-23 y el CORRECT sobre `ev-v9-004919-c6bfb3ee`; notas de RN-003, RN-004 y RN-005; recuadros en ADR-0080 §4 y §9 y su fila del índice; `spec_version` | los `fb-*` nuevos y sus ítems |
| 8 | ADR-0083 | el recuadro de S-6 y la fila del índice | — |
| 9 | el test de control de A.7 | `tests/unit/test_en_parte_no_se_cierra.py` | — |
| 10 | el informe | lo que falta del informe, la amplitud del contrato si la PARADA la aprueba, el revisor | — |

Cada uno con `knowledge validate` antes de `make check`, sellado, y el trailer `Fuente:` en el
cuerpo cuando toque `knowledge/spec/`.

### 0.e El encargo frente al repo

El subagente `auditor-encargo` (solo lectura, 2026-10-25) contrastó 66 afirmaciones: 39 correctas,
3 incorrectas y 24 con matiz, y 12 cosas que el repo pide y el encargo no recoge. Lo que cambia el
trabajo, con la evidencia que dio y la que añadió la sesión:

**Incorrectas**
1. «La tabla Known Ambiguities sí, porque test_project_state lo exige»: quien lo exige es
   `tests/unit/test_kit.py::test_project_state_refleja_las_ambiguedades_abiertas` (:458;
   `AMBIGUEDADES.md:6-11`); `test_project_state.py` solo mira que la sección exista y el tope de
   25.000 bytes. El efecto es el mismo: la fila sale en el commit que cierra cada una.
2. «`test_en_parte_no_se_cierra.py` ya lee las dos extracciones por su glob»: lee cuatro
   (`SESION-0*-EXTRACCION.md`, :15: de la 02 a la 05). Lo que falta sigue siendo el test de control
   de la 5 (A.7).
3. «Mide … por libros.yaml … qué libros vienen de un backtest grabado en vídeo»: `libros.yaml` no
   registra eso (campos `fichero`, `lecturas`, `medida`, `declarado_el`, `fuente`); hace falta
   cruzarlo con `fuentes.yaml`. Hecho así en §0.b.7.

**Con matiz, lo que pesa**
4. **La magnitud `saldo` (A.2).** La cita (`ev-v15-000913-bdb12f92`) no dice ni saldo ni equity; un
   RESOLVE_UNKNOWN sobre el parámetro lo deja CONFIRMED con fuente `feedback` (`aplicar.py:300-305`),
   es decir, como si lo hubiera dicho el trader. El repo pide otra cosa por tres vías: la lección de
   `ERRORES-RECURRENTES.md:84` (una re-expresión que añade un criterio que el literal no trae va como
   DEFAULT_AMBIGUOUS; ADR-0080 §5 dice que «sigue en pie»), la decisión del consultor del 2026-10-19
   sobre b10 (`docs/sesion-5/PREGUNTAS.md:204-209`: `bff260ea` «no basta como fuente»), y las
   procedencias de `feedback/modelo.py:118-125` (`reexpresion_consultor` es «lo mismo, en el tipo que
   espera el registro»; ninguna es «lectura del consultor»). Alternativa medible: `perdida_trader_magnitud`
   a DEFAULT_AMBIGUOUS con `ambiguedad_id: A-44` y `valor: saldo`, a mano, con fuente `feedback`
   `fb-2026-09-09-sesion-01-bff260ea` (el único literal del trader con «saldo»; un DEFAULT_AMBIGUOUS
   de estrategia cita feedback o evidencia, `test_registro.py:171-175`), y la descripción con la lectura
   del consultor; el motor lo lee igual (`registro.opcion`, anotado) y `test_provisional_cuelga_de_abierta`
   sigue en verde porque A-44 sigue ABIERTA (precedente: `orden_stop_punto`, `parametros.yaml:624-645`).
   PARADA, punto 1.
5. **Los CONFIRM de A.5** nombran ADR o ambigüedades como objetivo (ADR-0080 §4, A-24, ADR-0066,
   ADR-0075), y CONFIRM solo admite `evidence`, `regla`, `parametro` o `paquete` (`modelo.py:66`).
   Mapa propuesto en la tabla de §0.a y en la PARADA, punto 3.
6. **El precedente de A-43** fue un CORRECT sobre un DEFAULT_AMBIGUOUS que decía lo contrario de lo
   firme (`ACTIVAR-SESION-04.md:536`, `:675-689`); aquí son RESOLVE_UNKNOWN sobre UNKNOWN para que el
   arnés corra. El motivo es otro, y la desviación se declara con el suyo.
7. **La segunda mitad de A-35 y el runbook:** `ACTIVAR-A35-A44.md:56-58` dice que si el trader
   contradice lo fijo y visible de `pivotes_m15.py` «se abren como ambigüedades nuevas». El encargo
   decide que no (ya es la pregunta de A-35): es otra desviación declarada del runbook. Y la
   restricción «la mecha de LA VELA CONTRARIA» de B.1 sale de 06:49-06:58, que no está en ningún
   ítem; `ev-v15-000553-9d95178a` dice solo «se actualiza el de la mecha». La rama de motor lo
   escribirá con lo que el ítem sostiene y remitirá a §3.1 de la extracción para lo demás.
8. **«creo» en A.2:** `ev-v15-000913-bdb12f92` empieza «bueno, creo que aquí hay un error»; la unidad
   descansa en él. Sin «creo» está `ev-v10-010913-c4949417` («un 4,5% de pérdida en el día»,
   `PREGUNTAS.md:204`). Va en la lista de «creo» de la PARADA.
9. **ADR con textos viejos y sin recuadro** al fijar A-35 y A-44: ADR-0053 §3.3 (:123-125, «no
   declaran magnitud … y no se supone») y el final de §9 (:204-213), ADR-0054 §1 e Impacto (:14-24,
   :99, «todos UNKNOWN») y ADR-0070 §3 (:62, «hoy A-21, A-35 y A-44»). El alcance (1) del revisor
   exige que nada contradiga un ADR sin recuadro: una NOTA en cada uno (el precedente es la NOTA de
   ADR-0070 del 2026-10-14). `docs/adr/` está permitido. PARADA, punto 5.
10. **ADR-0080 §4 no usa la palabra PROVISIONAL** (ni su fila del índice): dice «decisión del
    consultor … va como pregunta de confirmación a la sesión 5». El recuadro dirá que la confirmación
    llegó (S-2), con la reserva del caso bajista.
11. **A.6 cita cosas que no están en los ítems:** «son decisiones diferentes» (27:11-27:16) y la duda
    sobre los «equals» (25:05-25:21). `ev-v15-002029-1ac081ae` habla de quitar la condicional cuando
    hay break even; `ev-v15-002729-30480ec5`, de que el punto tiene que haber roto; `ev-v15-002441-2e609b87`,
    de que el 1 sigue y el 0 se actualiza. El recuadro de ADR-0083 cita solo eso y remite a §3.2 de
    la extracción para lo demás, sin citarlo.
12. **A-13 (C):** «apenas toque» está en `ev-v15-013605-c041b814`; la confirmación de 97:48 no está
    en ningún ítem y su ASR es dudoso (extracción :848-850). La lista de la sesión 6 lo dice así.
13. **S-14 en C frente a «nada se pregunta con días reales»:** los días en que el bot opera y él no
    SON días reales de construcción. Se contradicen; la lista de la sesión 6 lo deja como lo pidió
    él (69:57) y marca la excepción para que el consultor la decida al preparar la hoja.
14. **El arnés con `--simular` (b.2):** por ADR-0070 §3 una corrida con `--simular` sobre toda la
    construcción y solo opciones de la lista es la que cuenta, y su veredicto, si da «sí», habilita
    la rama de mayo (§6). El encargo no puede declararla diagnóstico. Y lee para calentar el M1 de
    marzo y de junio (`PROJECT_STATE.md:117`), que se declara el mismo día. PARADA, punto 4 (correr
    con `--meses` de un solo mes, que por §2 no habilita, y declararlo).
15. **`test_provisional_cuelga_de_abierta.py` está en `tests/contract/`**, fuera de
    `rutas_permitidas`; no hay que tocarlo: pasa al dejar `lote_si_no_cabe` CONFIRMED.
    `test_registro.py:176-180` sí exige `decision` para un no-estrategia con valor.
16. **23.000 bytes** es el umbral de aviso del revisor (`ERRORES-RECURRENTES.md:55`), no un tope de
    test (`TOPE_BYTES = 25_000`, `test_project_state.py:21`). Se cumple igual: §0.c.

**Lo que el repo pide y el encargo no recoge**
17. Al activar A-44, RN-020 no retira la orden pendiente al llegar a su tope; el modelo es RN-036
    (`retirar_ordenes_pendientes`, ADR-0077; `ACTIVAR-A35-A44.md:223-225`). Va a «Para la rama de
    motor» como punto 10.
18. La medida de R4.1 «con su medida» (el `diff` con `--simular` contra
    `CABLEADO-SIMULADOR-LINEA-BASE.txt`, runbook §5.1): es la re-corrida tras la rama de motor, no
    esta rama. Se dice en las líneas del cierre.
19. El tercer sitio del runbook §3.3 para A-35: la nota del token `liquidez_m15`
    (`strategy_spec.yaml:588-592`, «hasta que se responda la regla no se escribe»). En el commit de
    A-35.
20. Los cinco sitios de A-57: además de `ambiguedades.yaml` y la tabla, la nota de RN-011
    (`strategy_spec.yaml:1488`, «DEFAULT bajo A-57»), la descripción y el `ambiguedad_id` de
    `lote_si_no_cabe` (`parametros.yaml:1824-1828`; `config/registro.py:446-447` rechaza el
    `ambiguedad_id` fuera de DEFAULT_AMBIGUOUS). En el commit de A-57.
21. Los de A-32: la hoja de preguntas y su test, `parametros.yaml:910` y `EN_PARTE_SESION_4`. En el
    commit de A-32.
22. Las dos deudas que la extracción dejó a V (§11 a4, diciembre en `meses_libres`; a7, el barrido)
    ya están en Technical Debt (`PROJECT_STATE.md:100-101`, carril de guardias): no son de esta rama.
23. `feedback pending` y un RESOLVE_UNKNOWN sobre un parámetro cuya ambigüedad sigue ABIERTA: se
    mide en §0.b.1.
24. El comentario de `src/botsito/engine/broker.py:177` y los tres guiones de §0.b.5: a la rama de
    motor.

### 0.f Lo que no pude medir

- Si una cita de un ítem cae en un tramo no citable: no se recorrió `tramos_no_citables.yaml` ítem
  a ítem porque los ítems de §8 ya pasaron esa puerta al crearse (`evidence new` la rechaza,
  SESION-05-EXTRACCION.md §3.5) y el revisor de aquella rama los cruzó (a3). Se cita solo lo que los
  ítems traen.
- La re-corrida y el `diff` contra la línea base: no se corren aquí (ADR-0070 §3; punto 14).
- `test_kit.py`, `test_selector_orden_stop.py` y `test_renovar_cierres.py` en el clon: la guardia
  de Claude Code los negó (§0.b.1), porque un test de un clon de `C:/cm/` no es para ella un test
  del repositorio (deuda K de la Next Action). No se rodeó; lo que cambia en ellos se razonó por el
  código. Hallazgo **importa** para la Next Action: K ya lo recoge, y esta rama lo confirma con tres
  ficheros más.

### 0.g Exposiciones

Una, declarada antes de ocurrir: la corrida del arnés de §0.b.2 lee para calentar el sesgo H4 de
abril el M1 entero de marzo de 2026 (`HOLDOUT-EXPOSICIONES.md`, fila del 2026-10-26, escrita antes
de correr). Lo demás que se leyó está en §0 (spec, código, tests, ADR, runbooks, ítems de evidencia y
registros de feedback por Read; `libros.yaml` y `fuentes.yaml` solo metadatos); los `pytest` del
clon y el guion de §0.b.3 son sintéticos o leen el `data/` solo por las puertas del propio código
(`test_visor.py` y `test_preparar_a35.py`, que ya declaran lo suyo en filas anteriores); ningún
listado de `knowledge/cases/` ni de carpetas con meses reservados. Al terminar, el clon se retiró
(`git worktree remove --force C:/cm/rama`, `git worktree prune`); `C:/cm/salida/` queda fuera del
repositorio y sin leer.

## Lo que necesito que decidas

0. **El choque entre el encargo y la skill `activar-sesion`** («En parte no se cierra … sin fijar
   nada», SKILL.md:35-36; el encargo dice que si chocan ganan las skills). Opciones: (a) la desviación
   declarada de A.1 y A.2 manda, con esa palabra en registros, notas e informe, como pide el encargo;
   (b) la skill manda y A-35 y A-44 no se fijan (el arnés sigue sin correr a secas). Recomiendo (a):
   es lo que el encargo decide a propósito y con precedente; coste de (b): la rama no cumple su
   objetivo.
1. **La magnitud `saldo`** (§0.e, 4). Opciones: (a) RESOLVE_UNKNOWN sobre `perdida_trader_magnitud`
   con la cita de `ev-v15-000913` y procedencia `trader_grabado`, que queda CONFIRMED por `feedback`;
   (b) `perdida_trader_magnitud` a DEFAULT_AMBIGUOUS, `valor: saldo`, `ambiguedad_id: A-44`, fuente
   `fb-2026-09-09-sesion-01-bff260ea`, escrito a mano, sin registro de feedback, con la lectura del
   consultor en la descripción y en las notas de RN-020; el arnés corre igual y la magnitud es la
   primera pregunta de la sesión 6. Recomiendo (b): dice lo que es -un default nuestro bajo una
   ambigüedad ABIERTA, como `orden_stop_punto`- y no hace pasar por voz del trader lo que no dijo;
   cuadra con `ERRORES-RECURRENTES.md:84` y con tu decisión del 2026-10-19 sobre b10. Coste de (a):
   un CONFIRMED con fuente feedback cuya cita no dice saldo, y el revisor (alcance 1 y 2) lo verá.
2. **La unidad `porcentaje` descansa en una cita con «creo»** (`ev-v15-000913`). Opciones: (a) se
   activa igual, con la reserva en las notas y la sesión 1 detrás (`bff260ea`: «menos un 4,5»);
   (b) se cita además `ev-v10-010913-c4949417` (sesión 4, «un 4,5% de pérdida en el día», sin
   «creo») en las notas. Recomiendo (b): cuesta una línea.
3. **El objetivo de cada CONFIRM de A.5**, porque CONFIRM no admite ADR ni ambigüedad
   (`modelo.py:66`). Propuesta: S-1 y S-2 y S-23 sobre la regla RN-003 (tres registros, tres
   literales distintos); S-9 y S-11 sobre la regla RN-004 (sus notas llevan A-24 DECIDIDA y
   `la_toma_es_de_la_sesion`); S-12a sobre RN-005 (como dice el encargo). Para S-9 hay otra forma:
   (b) RESOLVE_UNKNOWN sobre A-24, que ADR-0045 prevé («pasa a RESUELTA solo con un registro del
   trader que apunte a ella»), con sus cinco sitios (la hoja de preguntas la lleva por DECIDIDA,
   `test_kit.py:387-395`). Recomiendo (a) CONFIRM sobre RN-004 y A-24 sigue DECIDIDA: la cita lleva
   «por lo general» y el encargo no pide cerrarla. Coste de (b): cinco sitios más y una RESUELTA
   sostenida por un «por lo general».
4. **El arnés de b.2** (§0.e, 14). Opciones: (a) a secas y con `--simular` sobre UN mes de
   construcción (`--meses 2026-04`): prueba que corre sin `--diagnostico-*`, y por ADR-0070 §2 una
   corrida parcial no habilita nada; su fichero fuera del repo y sin resumir; (b) sobre toda la
   construcción, como dice el encargo, aceptando que por ADR-0070 §3 es una corrida que cuenta y que
   su veredicto quedaría escrito sin leerse. Recomiendo (a). En los dos casos la lectura del M1 de
   marzo (para abril) se declara antes de correr.
5. **Las NOTAS en ADR-0053 §3.3 y §9, ADR-0054 §1 e Impacto y ADR-0070 §3** (§0.e, 9), para que
   ningún ADR diga «UNKNOWN» o «hoy A-35 y A-44» con los valores puestos. Opciones: (a) una NOTA
   fechada en cada uno, en los commits de A-35 y A-44, y sus filas del índice; (b) nada, y el
   revisor lo marca. Recomiendo (a).
6. **`docs/runbooks/ACTIVAR-A35-A44.md`** queda viejo (§0 exige que el arnés se niegue; §1 y §2
   describen lo que esta rama hace) y no está en `rutas_permitidas`. Opciones: (a) ampliar el
   contrato a ese fichero en un commit propio y poner una NOTA al principio (activado el
   2026-10-25, qué se desvió: la segunda mitad de A-35 no abre ambigüedad nueva, `perdida_maxima_semanal`
   sin CORRECT, la magnitud); (b) dejarlo y que lo recoja la rama de motor. Recomiendo (a).
7. **`PROJECT_STATE.md` y los 23.000** (§0.c): con las líneas del cierre queda en ≈23.030. Opciones:
   (a) acortar la introducción de Technical Debt (:99) y la deuda de Oanda (:129) como dice §0.c
   (≈22.700); (b) llevar a HISTORIA el párrafo de candidatas sin abrir (:96) con un puntero;
   (c) dejarlo en ≈23.030, por debajo del tope de 25.000 del test. Recomiendo (a); lo haría en el
   commit del contrato, que es donde entran las líneas del cierre.
8. **Los dos commits de A-35 y A-44 y los cinco tests de CLI que llevan las dos opciones** (§0.b.5):
   (a) dos commits, como pide el plan d, con esos cinco tests tocados dos veces (en el de A-35
   pasan a esperar la negativa de A-44; en el de A-44, a correr a secas); (b) un solo commit para
   las dos, con cada test tocado una vez. Recomiendo (a): cada commit deja el repo verde y dice la
   verdad de su momento; coste, un `make check` más y diez minutos.
9. **Las reservas de lo que se activa**, para que las veas juntas: A-57 con «creo» y «por ahora» y
   tras la disyuntiva de Aleks (S-5); la unidad de A-44 con «creo» (S-4, punto 2); S-9 «por lo
   general»; S-2 con el caso bajista no dicho; S-12a con la línea que mezcla pregunta y respuesta
   (`ev-v15-010104`, confianza media). Ninguna tiene un ejemplo sin regla general salvo S-6, que no
   se activa. Opciones: (a) se activan todas con la reserva escrita en las notas del registro;
   (b) alguna se deja para la sesión 6 (dime cuál). Recomiendo (a).

Espero tu respuesta a la PARADA.

## Respuesta del consultor a la PARADA (2026-10-26)

Copiada tal cual.

> Respuesta del consultor a la PARADA de trabajo/activar-sesion-05 (2026-10-26). Cópiala tal cual al final del encargo y del informe, en «Respuesta del consultor a la PARADA», con su fecha, y aplícala punto por punto (skill fase-cero). Si al aplicar algo medido lo contradice, PARADA 2.
>
> 0. (a). La desviación declarada de A.1 y A.2 manda sobre activar-sesion, con la palabra «desviación» en los registros, las notas y el informe. Motivo: sin ella el arnés no corre a secas hasta la sesión 6, y lo que se fija está dicho por el trader (A-35) o es un valor provisional a la vista (A-44, punto 1).
> 1. (b). perdida_trader_magnitud a DEFAULT_AMBIGUOUS, valor saldo, ambiguedad_id A-44, fuente fb-2026-09-09-sesion-01-bff260ea, a mano y sin registro de feedback; la lectura del consultor va en su descripción y en las notas de RN-020, y la magnitud es la primera pregunta de la sesión 6. Motivo: es un default nuestro bajo una ambigüedad ABIERTA (precedente orden_stop_punto), y un CONFIRMED pondría en boca del trader lo que no dijo. Corrige mi error: el encargo decía «registro RESOLVE_UNKNOWN sobre el parámetro» y eso contradecía ERRORES-RECURRENTES.md:84 y mi propia decisión del 2026-10-19 sobre b10. El test sintético saldo/equity se queda.
> 2. (b). La unidad lleva además ev-v10-010913-c4949417 en las notas, con la reserva del «creo» de ev-v15-000913-bdb12f92.
> 3. (a). S-1, S-2 y S-23, CONFIRM sobre RN-003; S-9 y S-11, sobre RN-004; S-12a, sobre RN-005, más el CORRECT sobre ev-v9-004919-c6bfb3ee. A-24 sigue DECIDIDA. Los recuadros de ADR-0080 §4 y §9, ADR-0066 y ADR-0075 citan esos registros. Corrige mi error: los objetivos del encargo (ADR y ambigüedades) no los admite CONFIRM (modelo.py:66).
> 4. (a). Arnés a secas y con --simular solo con --meses 2026-04, fichero fuera del repo y sin resumir, con la lectura del M1 de marzo declarada antes de correr (ya está). Corrige mi error: por ADR-0070 §3 la corrida sobre toda la construcción con --simular cuenta, y esa es la re-corrida que va después de la rama de motor.
> 5. (a). Una NOTA fechada en ADR-0053 §3.3 y §9, ADR-0054 §1 e Impacto y ADR-0070 §3, en los commits de A-35 y A-44, con sus filas del índice. Lo que añadí de más en el encargo, el recuadro de ADR-0066 y ADR-0075 por S-11 y S-23, va también como NOTA de una línea en el commit de las confirmaciones.
> 6. (a). Amplía el contrato a docs/runbooks/ACTIVAR-A35-A44.md, en un commit propio, con una NOTA al principio: activado el 2026-10-26, lo que se fijó y las tres desviaciones (la segunda mitad de A-35 no abre ambigüedad nueva; perdida_maxima_semanal sin CORRECT; la magnitud como DEFAULT_AMBIGUOUS). El cuerpo no se toca.
> 7. (a). Acortar la introducción de Technical Debt y dejar de la deuda de Oanda solo la parte viva de la serie, en el commit del contrato. Las candidatas sin abrir se quedan.
> 8. (a). Dos commits, con los cinco tests de CLI tocados dos veces, y cada commit en verde.
> 9. (a). Todas se activan, con su reserva escrita en las notas del registro.
>
> Además, lo que sale de §0.e:
> 10. B.1 (la segunda mitad de A-35): la rama de motor escribe lo que sostiene ev-v15-000553-9d95178a («se actualiza el de la mecha») y remite a SESION-05-EXTRACCION.md §3.1 para el ejemplo del replay, sin citarlo. Que sea la mecha de la vela contraria es lo que se pregunta en la sesión 6 para confirmarlo. Corrige mi error: el encargo restringía a la vela contraria con un tramo que no está en ningún ítem.
> 11. Lista de la sesión 6, S-14 (§0.e.13): los días en que el bot opera y él no se enseñan como permite la regla 2 de SESION-DE-PREGUNTAS.md (solo días de construcción, cortados antes de la orden y sin fecha), y la elección de los días la hago yo al preparar la hoja. Corrige la frase «nada de esto se pregunta con días reales», que era demasiado ancha: quédala como «ningún día reservado ni ninguna fecha».
> 12. §0.e.17 (RN-020 no retira la orden pendiente al llegar al tope): de acuerdo, entra en «Para la rama de motor» como punto 10, con RN-036 de modelo.
> 13. §0.e.18 (la medida de R4.1 con su diff): va en las líneas del cierre como la re-corrida que sigue a la rama de motor, no en esta rama.
> 14. §0.f (la guardia niega los tests de un clon en C:/cm/): hallazgo importa, de acuerdo. Ponlo en las líneas del cierre como ampliación de K, con los tres ficheros nuevos.
>
> Sigue lo que manda el encargo: un commit por respuesta, knowledge validate antes de make check, Fuente: en el cuerpo con ids que existen, CI de Linux por fix/activar-sesion-05 con su número de run (gh run view suelto), revisor (opus) con los cuatro alcances del encargo más un quinto (cada DEFAULT_AMBIGUOUS nuevo dice en su descripción que es lectura del consultor y bajo qué ambigüedad) y su informe pegado al final. Si el clasificador niega un push o la guardia un make, dame el comando exacto y lo lanzo yo con «!».
>
> Rama lista para revisión, NO cerrada.

## 1. La respuesta aplicada, commit a commit

Cada punto de la respuesta del consultor, en el orden del plan de §0.d; lo que al aplicarlo
contradijo algo medido va como PARADA nueva. Todos los registros llevan la cita de su ítem de
SESION-05-EXTRACCION.md §8 como `respuesta_literal`, `--medio video`, la grabación de v15 o v16,
el tramo del ítem, `--procedencia trader_grabado` y las fechas del encargo (v15: `--fecha 2026-10-23
--recibido-el 2026-10-23`; v16: `--recibido-el 2026-10-25`).

### 1.1 A-35 · `liquidez_m15_pivote_formado` = `cierre_vela_contraria` (puntos 0 y 10)

**El registro:** `fb-2026-10-23-sesion-05-03449065`, RESOLVE_UNKNOWN sobre el PARÁMETRO (no sobre
la ambigüedad), cita `ev-v15-000447-6699c708` (0:04:47-0:05:09), notas con `ev-v15-000530-234d4a81`
(la sin cuerpo no cuenta) y `ev-v15-000553-9d95178a` (la segunda mitad, a la rama de motor). El
`registrado_por` y las notas llevan la palabra DESVIACION dos veces, como pidió el punto 0: de la
skill `activar-sesion` («en parte no se cierra … sin fijar nada») y del runbook
`ACTIVAR-A35-A44.md` §1 (la segunda mitad no abre una ambigüedad nueva: ya es la pregunta de
A-35). Ningún registro sobre A-35, que SIGUE ABIERTA y bloqueante.

**`feedback apply --sesion 2026-10-23-sesion-05 --check`** propuso exactamente este registro
(`1 parametros; 1 cambian, 0 ya estaban`) y sin `--check` escribió `estado: CONFIRMED`,
`valor: cierre_vela_contraria` y `fuente: {tipo: feedback, id: fb-…-03449065}` en
`parametros.yaml` (la descripción, a mano, con la fecha, los tres ítems y la desviación).

**Los sitios tocados** (los del runbook §3.3 que aplican a un parámetro fijado con la ambigüedad
abierta; la tabla de `PROJECT_STATE.md` y la hoja de preguntas no cambian porque A-35 sigue
ABIERTA):
- `knowledge/spec/ambiguedades.yaml`, A-35: «RESPONDIDA EN PARTE en la sesion 5 … SIGUE ABIERTA» al
  final de `pregunta` (el precedente de A-44 tras la sesión 3) y un comentario fechado con la
  desviación y lo que falta para la sesión 6.
- `knowledge/spec/strategy_spec.yaml`: las notas de RN-004 («DESDE EL 2026-10-26 … A-35 TIENE
  VALOR … DESVIACION declarada») y la descripción del token `liquidez_m15` («ESTA RESPONDIDO EN SU
  PRIMERA MITAD»), que era el tercer sitio del runbook (§0.e, 19).
- `spec_version` 18.1.3 → 18.1.4, `spec manifest --escribir` (hash `3167d9bbbb88…`) y
  `spec docs --escribir` (los cuatro de `docs/spec/`).
- ADR-0054: NOTA fechada bajo §1 y en Impacto; ADR-0070: NOTA bajo la de §3 del 2026-10-14 (el
  diagnóstico queda solo para A-44, y la corrida que cuenta es la re-corrida tras la rama de
  motor). Las dos filas del índice de `docs/adr/README.md` lo dicen (punto 5).

**Tests que cambian de sentido a propósito** (§0.b.5; medidos en el clon de §0.b.1, donde los de
`main` fallaban con el valor puesto):
- `test_preparar_a35.py`: `test_sin_fijar_el_motor_se_niega_nombrando_a35` pasa a
  `test_con_el_registro_real_la_lectura_es_el_cierre_y_el_diagnostico_se_rechaza` (el registro
  real da `cierre_vela_contraria`; `Diagnostico(a35=…)` se rechaza con «ya esta fijado») y la
  negativa sin fijar se conserva sobre un registro sintético UNKNOWN en
  `test_sin_fijar_se_niega_nombrando_a35` (test nuevo: 1693 → 1694 funciones);
  `test_la_cli_se_niega_sin_lectura_y_no_escribe_nada` pasa a
  `test_la_cli_rechaza_el_diagnostico_de_a35_y_no_escribe_nada` (medida sigue negándose con
  MEDIDA; `--diagnostico-a35` sobre construcción se rechaza sin escribir; a secas, la siguiente
  compuerta es A-44, que en este commit sigue sin fijar: **se toca otra vez en el commit de
  A-44**); `test_por_la_cli_en_diagnostico_todo_sale_etiquetado_si_hay_datos` corre solo con
  `--diagnostico-a44 sin_tope`, el fichero es `informe.DIAGNOSTICO.a44=sin_tope.txt` y ninguna
  línea lleva `DIAGNOSTICO-A35` (se toca otra vez en el commit de A-44: a secas).
- Los cinco tests de CLI que pedían los dos diagnósticos pierden `--diagnostico-a35` en este
  commit y `--diagnostico-a44` en el siguiente (punto 8): `test_preparar_a44.py::
  test_la_cli_se_niega_sin_a44_aunque_a35_vaya_en_diagnostico` (ahora
  `…_con_a35_ya_fijada`: a secas se niega nombrando A-44), `test_selector_orden_stop.py` (dos
  tests), `test_renovar_cierres.py`, `test_rutas_windows.py` (`diag` solo con A-44) y
  `test_visor.py` (a secas sigue en 2, ahora por A-44; la página se llama
  `<caso>.DIAGNOSTICO.a44=sin_tope.html` y no lleva `DIAGNOSTICO-A35`).
- Sin cambio, como preveía §0.b.5: `test_preparar_a21.py::test_la_cli_no_conoce_diagnostico_a21…`
  (la compuerta de medida va antes), `test_cableado.py`, `test_umbral_mayo.py`,
  `test_diferencias_por_operacion.py`, `test_kit.py` (bloqueantes ABIERTAS siguen siendo
  {A-35, A-44}).

`uv run pytest` sobre los once ficheros tocados o vecinos (`test_preparar_a35`, `test_preparar_a44`,
`test_selector_orden_stop`, `test_renovar_cierres`, `test_rutas_windows`, `test_visor`, `test_kit`,
`test_registro`, `test_hoja_preguntas`, `test_spec_docs_generados`, `test_adr`): 161 en verde, 0
fallos. `knowledge validate`: exit 0 (`OK: registro con 109 parametros (16 sin confirmar)`,
`OK: 177 registros de feedback, historial intacto, commits con Fuente`).

### 1.2 A-44 · `perdida_trader_alcance` = `dia`, `perdida_trader_unidad` = `porcentaje`, `perdida_trader_magnitud` = `saldo` como DEFAULT_AMBIGUOUS (puntos 0, 1, 2, 5, 8 y 12)

**Los registros**, los dos sobre PARÁMETROS, ninguno sobre A-44 (que SIGUE ABIERTA y bloqueante):
- `fb-2026-10-23-sesion-05-e9559876`, RESOLVE_UNKNOWN sobre `perdida_trader_alcance` = `dia`, cita
  `ev-v15-000856-ee8f7ba3` (0:08:56-0:09:04). Las notas dicen que con `dia` el motor no lee
  `perdida_maxima_semanal`, que queda CONFIRMED en 9 y SIN EFECTO, sin CORRECT: la segunda
  desviación declarada del runbook `ACTIVAR-A35-A44.md` §1 (punto 6 de la respuesta).
- `fb-2026-10-23-sesion-05-1772d9ef`, RESOLVE_UNKNOWN sobre `perdida_trader_unidad` =
  `porcentaje`, cita `ev-v15-000913-bdb12f92` (0:09:13-0:09:20); las notas llevan la RESERVA del
  «creo» y, como pidió el punto 2 (b), la cita de la sesión 4 sin «creo», `ev-v10-010913-c4949417`.
- Los dos `registrado_por` y las notas llevan DESVIACION (de la skill `activar-sesion`, punto 0).

**`feedback apply --check`** propuso exactamente los dos (`3 parametros; 2 cambian, 1 ya estaban`:
el tercero es el de A-35, ya escrito) y sin `--check` los dejó CONFIRMED con `fuente: feedback`.

**La magnitud, a mano (punto 1 (b)):** `perdida_trader_magnitud` pasa de UNKNOWN a
`DEFAULT_AMBIGUOUS`, `valor: saldo`, `ambiguedad_id: A-44`, `fuente: {tipo: feedback, id:
fb-2026-09-09-sesion-01-bff260ea}`, y su descripción dice que es LECTURA DEL CONSULTOR bajo A-44,
qué dice y qué no dice esa cita («De la cuenta basado en el saldo»: la base del porcentaje, no si lo
abierto cuenta), por qué no entra CONFIRMED (precedente `orden_stop_punto`; la lección 2 de
`trabajo/corrida-construccion` en ERRORES-RECURRENTES.md) y que es la primera pregunta de la
sesión 6. Sin registro de feedback. `tests/contract/test_provisional_cuelga_de_abierta.py` y
`test_registro.py` en verde (un DEFAULT_AMBIGUOUS de estrategia con fuente `feedback`, bajo una
ABIERTA).

**Los sitios tocados** (la tabla de `PROJECT_STATE.md` y la hoja no cambian: A-44 sigue ABIERTA):
- `parametros.yaml`: el comentario de cabecera de los seis `perdida_trader_*`, las descripciones
  de `alcance` y `unidad` (fecha, ítem, registro, desviación), la de `magnitud` (arriba) y la de
  `perdida_maxima_semanal` («SIN EFECTO … sin CORRECT, como DESVIACION declarada del runbook §1»).
- `ambiguedades.yaml`, A-44: «RESPONDIDA EN PARTE en la sesion 5 … SIGUE ABIERTA» en `pregunta` y
  un comentario fechado con lo fijado, la lectura del consultor y el orden de la sesión 6
  (magnitud primero, reloj después).
- `strategy_spec.yaml`: las notas de RN-020 (valor, magnitud como lectura del consultor con la
  medida de §0.b.3, reloj SUPUESTO, desviación, y «LO QUE ESTA REGLA SIGUE SIN HACER: no retira la
  orden pendiente al llegar al tope», punto 12) y las descripciones de los acumuladores
  `perdida_dia` y `perdida_semana` (sin tocar su `magnitud`, que la spec no declara: la lleva el
  parámetro, ADR-0002).
- `spec_version` 18.1.4 → 18.1.5, manifiesto (`bfae30bb0afb…`) y los cuatro docs de `docs/spec/`.
- ADR-0053: NOTA fechada bajo §3.3 y al final de §9; ADR-0054: la NOTA de §1 y la de Impacto
  ganan A-44; ADR-0070: la NOTA de §3 dice que el motor ya no necesita ningún diagnóstico. Las tres
  filas del índice actualizadas (punto 5).

**Tests que cambian de sentido a propósito** (§0.b.5; en el clon de §0.b.1 los de `main` fallaban
con los valores puestos: 7 + 5 + 4):
- `test_preparar_a44.py`: los siete que pedían el tope hipotético sobre el registro REAL pasan a
  pedirlo sobre un registro SINTÉTICO sin A-44 (`_diagnostico`, sobre `_registro_sintetico`): lo
  que prueban -los tres estados del tope sobre el cableado y sobre el motor de la spec- no cambia.
  Dos tests nuevos (1694 → 1696 funciones):
  `test_con_el_registro_real_el_tope_es_el_del_dia_en_porcentaje_sobre_el_saldo` (dia, saldo,
  porcentaje, 4,5, semana `None`, huso SUPUESTO, diagnóstico rechazado) y el **test sintético que
  pidió el encargo**, `test_con_el_registro_real_una_caida_en_abierto_que_se_recupera_no_cuenta`:
  con el tope leído del registro, una equity 5.000 por debajo con el saldo intacto da `perdida_dia`
  0; el mismo tope leído como `equity` daría 5 (%). Si alguien cambia la magnitud sin pasar por
  A-44, falla. Y `test_la_cli_se_niega_sin_a44…` (tocado por segunda vez, punto 8) pasa a
  `test_la_cli_rechaza_el_diagnostico_de_a44_con_el_tope_fijado`.
- `test_preparar_a21.py` (`_motor` y el test del cableado) y `test_sesiones_independientes.py`
  (`_motor`): `tope_del_registro(registro, huso)` a secas; sus días sintéticos no pierden y el tope
  del día no dispara. Importes de `Diagnostico` que sobraban, fuera.
- Los cinco tests de CLI, por segunda vez: pierden `--diagnostico-a44`. `test_visor.py` corre a
  secas, la página vuelve a ser `<caso>.html` sin `DIAGNOSTICO` y el diagnóstico se rechaza sin
  escribir; `test_rutas_windows.py` ya no construye el `Diagnostico`.
- `test_preparar_a35.py`, segunda vez: `test_la_cli_rechaza_el_diagnostico_de_a35_y_no_escribe_nada`
  comprueba también el rechazo de `--diagnostico-a44`, y
  `test_por_la_cli_en_diagnostico_todo_sale_etiquetado_si_hay_datos` pasa a
  `test_por_la_cli_a_secas_el_informe_cuenta_y_no_lleva_etiqueta_si_hay_datos` (con `data/`: a
  secas corre con código 0, el fichero se llama como se pidió, ninguna línea lleva `[DIAGNOSTICO`,
  y con los dos diagnósticos se rechaza sin escribir nada más).

**Una trampa medida, corregida en el mismo commit:** `test_rutas_windows.py::
test_la_cli_se_niega_ante_una_ruta_larga_antes_de_leer_nada` construía la carpeta 40 caracteres
por debajo del límite y era el rótulo del diagnóstico el que la pasaba; sin rótulo la carpeta cabía,
el arnés corrió entero sobre el primer mes de construcción y falló al escribir
(`FileNotFoundError`). §0.b.5 lo preveía al revés («la carpeta sigue pasando del límite sin
rótulo»): error de la fase 0, corregido aquí. Ahora la carpeta sola pasa del límite y la CLI se
niega antes de leer nada. Esa corrida única, y que `test_preparar_a35.py` y `test_visor.py` corran
desde ahora a secas en cada `make check` con la misma lectura de antes, están declaradas en
`HOLDOUT-EXPOSICIONES.md` (fila del 2026-10-26, punto 5).

`uv run pytest` sobre los diecinueve ficheros tocados o vecinos (los ocho de arriba más `test_kit`,
`test_registro`, `test_provisional_cuelga_de_abierta`, `test_spec_docs_generados`, `test_adr`,
`test_cableado`, `test_racha_perdidas`, `test_umbral_mayo`, `test_diferencias_por_operacion`,
`test_en_parte_no_se_cierra`, `test_spec_fidelidad`): un fallo, el de la trampa, y en verde tras
corregirlo. `knowledge validate`: exit 0 (`OK: registro con 109 parametros (14 sin confirmar)`,
`OK: 179 registros de feedback`).

### 1.3 A-57 RESUELTA · `lote_si_no_cabe` = `limitar`, confirmado por el trader (A.3; punto 9)

**El registro:** `fb-2026-10-23-sesion-05-146c4789`, RESOLVE_UNKNOWN sobre LA AMBIGÜEDAD A-57
(ADR-0022), cita `ev-v15-001758-c27d9c4c` (0:17:58-0:18:15), `valor_resultante` «baja el lote a lo
que cabe y entra igual (lote_si_no_cabe = limitar, la opcion a; por ahora)». Las notas llevan las
tres reservas (punto 9 (a)): «por ahora» y «creo» (17:58), y que contestó después de que Aleks,
preguntado por él, planteara la disyuntiva (remitiendo a SESION-05-EXTRACCION.md §3.2, S-5, sin
citarla); y que no ha vivido el caso en su cuenta. `feedback apply --check` no propone nada nuevo
(`3 parametros; 0 cambian, 3 ya estaban`): el registro va sobre la ambigüedad, no sobre el
parámetro, y `lote_si_no_cabe` es de `ejecucion`.

**Los cinco sitios** (`AMBIGUEDADES.md`):
1. `parametros.yaml`, `lote_si_no_cabe`: a mano, `estado: CONFIRMED`, sin `ambiguedad_id`, la fuente
   sigue siendo `decision` ADR-0081 (lo que exige `test_registro.py:176-180` para un parámetro que
   no es de estrategia); la descripción dice quién lo confirmó, cuándo y con qué reservas.
2. `ambiguedades.yaml`, A-57: `estado: RESUELTA`, «RESUELTA el 2026-10-23 en la sesion 5 …» al final
   de `pregunta` con las reservas, y un comentario fechado.
3. La regla que lo citaba: las notas de RN-011 («DEFAULT bajo A-57 hasta el 2026-10-26 … A-57 ESTA
   RESUELTA»).
4. La tabla «Known Ambiguities» de `PROJECT_STATE.md`: sale la fila de A-57.
5. La hoja de preguntas: A-57 no estaba en ella (no cambia).

Más `tests/unit/test_kit.py` (RESUELTAS gana A-57, con su comentario), `spec_version` 18.1.5 →
18.1.6 con manifiesto (`5532492a9236…`) y docs, y ADR-0081: recuadro bajo D1 («CONFIRMADO POR EL
TRADER … D1 deja de ser PROVISIONAL», con las reservas), su `## Estado` y la fila del índice. El
comentario de `src/botsito/engine/broker.py:177` («DEFAULT_AMBIGUOUS bajo A-57») queda viejo y
`src/` está protegido: a la rama de motor (§0.e, 24).

**Lo medido:** `tests/contract/test_provisional_cuelga_de_abierta.py`, `test_registro.py`,
`test_margen_lote.py`, `test_kit.py`, `test_hoja_preguntas.py`, `test_en_parte_no_se_cierra.py`,
`test_spec_docs_generados.py`, `test_adr.py`, `test_project_state.py` y
`test_reabrir_y_fuente_documental.py`: 176 en verde, 0 fallos. `knowledge validate`: exit 0.
`feedback pending`: el registro de A-57 queda reflejado (A-57 RESUELTA); los dos pendientes que
lista son anteriores a la rama (`fb-2026-09-29-sesion-03-31fb311f` y
`fb-2026-10-04-sesion-04-ca0afae6`, los CORRECT sobre RN-003 que §0.e ya contaba y que las notas de
RN-003 explican).

### 1.4 A-32 RESUELTA · en M1 la mecha siempre vale (A.4; ningún valor cambia)

**El registro:** `fb-2026-10-23-sesion-05-b8271811`, RESOLVE_UNKNOWN sobre LA AMBIGÜEDAD A-32, cita
`ev-v16-000234-9a4fa375` (v16, 0:02:34-0:03:12; `--fecha 2026-10-23 --recibido-el 2026-10-25`, la
grabación del 2026-10-25), `valor_resultante` «en M1 la mecha siempre vale; la unica ruptura que
pide cuerpo es la que habilita la zona lineal de liquidez de M15, y una linea que viene de M15
cuenta como de M15 aunque se mire en M1 (… ya fijados; ningun valor cambia)». Las notas llevan
`ev-v16-000603-6955d127` («la cuento como de M15 aunque la mire de M1»), la sesión 4
(`ev-v10-020142-30fd2569`, la que la dejó en parte), que lo dijo en compra y en venta, y la
verificación que pedía el encargo. Ningún registro sobre parámetros: `feedback apply --check` sigue
proponiendo `0 cambian, 3 ya estaban`.

**La verificación de A.4** (medida en la fase 0, §0.a, fila S-18, y no contradicha al aplicar):
`breaker_m1_criterio_ruptura` = `mecha` (`_pasa` con MECHA, `domain/estructura_m1.py:103-111`) y
`liquidez_m15_criterio_toma` = `cuerpo` (`cruza`, `domain/pivotes_m15.py:208-218`) ya lo hacen; la
única lectura del motor que descarta una entrada por una mecha de M1,
`sin_mecha_mas_alla_del_extremo` (`estructura_m1.py:334`), está INACTIVA porque
`zona_control_limpia` = `solo_una_zona_de_control` (`grep -n sin_mecha_mas_alla_del_extremo
src/botsito`: la constante, su lista y esa única rama). Sin PARADA.

**Los cinco sitios:**
1. El registro de parámetros: ningún valor cambia; las descripciones de `breaker_m1_criterio_ruptura`
   («CONFIRMADO EN LA SESION 5 … A-32 RESUELTA») y de `zona_control_limpia` («que nivel era es
   A-32, RESUELTA … era la liquidez de M15») lo dicen.
2. `ambiguedades.yaml`, A-32: `estado: RESUELTA`, «RESUELTA el 2026-10-25 en la sesion 5 …» en
   `pregunta`, y un comentario fechado (la 4 la dejó en parte, la 5 la resuelve).
3. La regla que la citaba: ninguna regla de `strategy_spec.yaml` nombra A-32 (`grep -n A-32`: 0
   líneas); el sitio es la descripción de `zona_control_limpia` (punto 1).
4. La tabla «Known Ambiguities» de `PROJECT_STATE.md`: sale la fila de A-32.
5. La hoja de preguntas: `scripts/hoja_preguntas.py` pierde el bloque «La liquidez de M15», que
   solo llevaba A-32, y `tests/unit/test_hoja_preguntas.py` pierde «A-32» de `ORDEN`, los dos con
   su comentario.

Más `tests/unit/test_kit.py`: RESUELTAS gana A-32 y `EN_PARTE_SESION_4` la pierde, con el
comentario (una sesión posterior puede cerrar lo que la 4 dejó en parte; lo que la 5 deja en
parte lo vigilará el test de control de A.7). `spec_version` 18.1.6 → 18.1.7, manifiesto
(`19930de08bdb…`) y docs.

**Lo medido:** `test_kit`, `test_hoja_preguntas` (con la hoja escrita en un `.docx` temporal),
`test_en_parte_no_se_cierra`, `test_registro`, `test_spec_docs_generados`, `test_project_state`,
`test_hoja_de_ruta`, `test_reabrir_y_fuente_documental`, `test_pivotes_m15` y `test_a21_series`:
192 en verde, 0 fallos. `knowledge validate`: exit 0. `feedback pending`: el registro de A-32
reflejado; siguen los dos CORRECT antiguos sobre RN-003 de §1.3. Una trampa propia, corregida
antes de validar: tres notas de la spec citaron un id `fb-…` escrito antes de crear el registro
(el hash sale del contenido): sustituido por el real, `b8271811`, en los tres sitios (`grep` del
provisional: 0 líneas).

### 1.5 Las confirmaciones (A.5; puntos 3, 5 y 9): S-1, S-2, S-23, S-9 y S-12a, y el CORRECT sobre `ev-v9-004919-c6bfb3ee`. S-11, a la PARADA 2

**Los registros**, todos CONFIRM sin valor sobre una REGLA (el punto 3 corrige el encargo: CONFIRM no
admite ADR ni ambigüedad, `modelo.py:66`), con la cita de su ítem y la reserva en las notas (punto 9):

| Código | Registro | Objetivo | Cita | Lo que confirma | Reserva en las notas |
|---|---|---|---|---|---|
| S-1 | `fb-2026-10-23-sesion-05-af24c935` | RN-003 | `ev-v15-000049-3b294480` (0:00:49-0:01:16) | el caso 3 de la regla del color: rompe el máximo solo con la mecha y cierra roja → sigue bajista; cierra la contradicción de ADR-0080 §9 con la sesión 1 a favor del color; se decide al cierre de la vela (`ev-v15-000138-ef123dfc`); A-1 no se reabre | solo el caso bajista |
| S-2 | `fb-2026-10-23-sesion-05-85ce7ba5` | RN-003 | `ev-v15-000256-f3c52278` (0:02:56-0:03:17) | D3 de ADR-0080 §4: la ruptura simple sin cuerpo no decide y sigue el sesgo que había | el caso bajista no lo dijo con sus palabras |
| S-23 | `fb-2026-10-23-sesion-05-b09c3fed` | RN-003 | `ev-v16-002641-e8e6eafc` (v16, 0:26:41-0:26:46; `--recibido-el 2026-10-25`) | con el sesgo bajista la neutra de doble ruptura mantiene el sesgo, también dos seguidas (`ev-v16-002521-02c1be20`); la reserva de `fb-2026-10-04-sesion-04-ca0afae6` queda contestada | «creo» solo en un ejemplo |
| S-9 | `fb-2026-10-23-sesion-05-bd88993f` | RN-004 | `ev-v15-004448-aac87b77` (0:44:48-0:44:54) | la liquidez que RN-004 toma es la más reciente (A-24, DECIDIDA por ADR-0045, sigue DECIDIDA: el registro apunta a la regla) | «por lo general»; solo la compra |
| S-12a | `fb-2026-10-23-sesion-05-ffb3011e` | RN-005 | `ev-v15-010104-23adba23` (1:01:04-1:01:25) | en una compra la caja queda por debajo del nivel tomado, y en venta al revés: RN-005 sigue; A-50 (S-12b) ABIERTA | la línea mezcla pregunta y respuesta (confianza media) |
| S-12a | `fb-2026-10-23-sesion-05-a42c72dd` | CORRECT sobre `ev-v9-004919-c6bfb3ee`, `valor_resultante` «por debajo del nivel tomado en una compra» | la misma cita | el ítem de la sesión 3 («tiene que ser todo por encima») queda corregido por la sesión 5 sin editarlo ni supersederlo (precedente `fb-2026-09-09-sesion-01-2ba4c3e7`) | — |

`feedback apply --check` no propone nada (ningún registro sobre parámetros). `feedback pending
--todos` da los seis como reflejados: los cinco CONFIRM, «confirma la regla vigente»; el CORRECT
sobre evidencia, «sin forma mecanica de cruzarlo», como los de la sesión 1.

**Las notas de las reglas** (una línea por lo que confirma, como pedía el encargo): RN-003
(«CONFIRMADA EN LA SESION 5 … tres CONFIRM»: S-1 cierra la contradicción, S-2 deja de ser
provisional, S-23 contesta la reserva del caso bajista), RN-004 (S-9: la más reciente; A-24 sigue
DECIDIDA) y RN-005 (S-12a y el CORRECT). `spec_version` 18.1.7 → 18.1.8, manifiesto
(`20076c8d14a4…`) y docs.

**Los ADR** (punto 5): ADR-0080, recuadro bajo §4 («CONFIRMADO POR EL TRADER … D3 deja de ser una
decisión provisional», con la reserva) y recuadro al final de §9 («CONTRADICCIÓN CERRADA …»);
ADR-0075, NOTA de una línea bajo las reservas de §1 (S-23); las dos filas del índice. **La NOTA de
ADR-0066 por S-11 NO se escribe en este commit**: S-11 va a la PARADA 2 (abajo).

**Lo medido:** `test_sesgo_h4`, `test_spec_fidelidad`, `test_adr`, `test_registro`,
`test_spec_docs_generados`, `test_citas_supersedidas`, `test_cli` y `test_kit`: 211 en verde, 0
fallos. `knowledge validate`: exit 0.

**S-11, lo que al aplicarlo contradice algo medido (PARADA 2, abajo):** la cita de S-11
(`ev-v15-005839-f2e43c27`: «Si hay una continuidad de sesgo, sí. Pero si no, no») contesta el caso
preguntado -el sesgo cambia a las 11, la toma de la mañana no vale- como hace el motor, pero su
primera mitad dice que CON continuidad de sesgo la toma de la mañana SÍ vale para la tarde, y eso
es lo contrario de A-46 RESUELTA («cada uno es un mundo diferente», `fb-2026-09-29-sesion-03-5021677e`:
la pregunta de A-46 era exactamente si la toma de la mañana sigue valiendo en la tarde, sin
distinguir el sesgo) y de lo que RN-004 hace con `la_toma_es_de_la_sesion` (ADR-0066 §1), medido
en `test_sesiones_independientes.py::test_la_toma_de_la_primera_sesion_no_vale_en_la_segunda`
(el sesgo sigue alcista y la toma no vale). Un CONFIRM sobre RN-004 con esa cita afirmaría más de
lo que la regla hace; la skill `activar-sesion` manda PARADA cuando una respuesta contradice una
respuesta anterior del trader. La hoja ya lo preveía al revés (`PREGUNTAS.md:414-419`: si contesta
(a), A-46 se REABRE con un `REOPEN`); el trader contestó (b) para el caso preguntado y (a) para el
caso que A-46 ya tenía respondido. Ningún registro de S-11 en este commit.

### 1.6 ADR-0083 sigue PROVISIONAL: el recuadro de S-6 (A.6)

Recuadro bajo D1 de ADR-0083 con lo que dijo el trader en S-6 y solo con lo que los tres ítems
sostienen (§0.e, 11): la duda sobre las reentradas en el mismo nivel tras un break even
(`ev-v15-002029-1ac081ae`, «una duda, no una regla»), el ejemplo en que el 1 sigue y el 0 se
actualiza (`ev-v15-002441-2e609b87`) y que el punto tiene que haber roto para volver a validarse
(`ev-v15-002729-30480ec5`); lo demás del tramo (que son decisiones distintas, los «equals») se
remite a SESION-05-EXTRACCION.md §3.2 sin citarlo. Ningún registro de feedback (en parte). El
`## Estado` del ADR y su fila del índice dicen que D1 sigue PROVISIONAL y que la pregunta pasa a la
sesión 6 (§3, 8). `test_adr.py` en verde (el Estado empieza por `ACTIVE`).

## Estado

EN CURSO (2026-10-26): la respuesta del consultor a la PARADA está copiada y se aplica punto por
punto, un commit por respuesta (§1). Lo hecho hasta aquí lo dice §1; lo que falta, el plan de §0.d.
