# ACTIVAR-SESION-06 · Las respuestas de la sesión 6 entran en la spec (R4.2, entrada F)

> PLANTILLA hasta la fase 0: este informe nace EN CURSO y todavía no tiene tabla (SESION-06-EXTRACCION.md §7, punto 1).

Rama `trabajo/activar-sesion-06`, abierta el 2026-11-05 desde `main` en 0f57738 (commit de estado
sobre el merge 78d560d, tag `stable/F38m-sesion-06`). Encargo:
`docs/encargos/trabajo-activar-sesion-06.md`. Tramo: R4 (R4.2 de `docs/plan/HOJA-DE-RUTA.md`;
F de la Next Action).

Antes de abrir se comprobó con git (skill `abrir-rama`, paso 1):

- `git rev-parse --short main` = 0f57738; `git rev-parse main origin/main` da dos veces
  0f577380b278389ceb186449c41af1e59f78e00a; `git status --short` vacío.
- El último tag de `docs/state/HISTORIA.md` es `stable/F38m-sesion-06`;
  `git rev-parse "stable/F38m-sesion-06^{commit}"` = `git rev-parse main^1` =
  78d560d86eac1ac46517455c2763db0ad666ab3a; `git ls-remote --tags origin stable/F38m-sesion-06`
  devuelve el tag.
- CI de `main`: `gh run view 42076588321` suelto: `headSha` 0f577380b278389ceb186449c41af1e59f78e00a,
  `completed` / `success`.
- `git branch --list` solo daba `main`; `git ls-remote --heads origin "fix/*"` salió vacío.

Primer commit sellado: `8cb07d6` (`make check`: `3210 passed`, `SELLO` sobre el árbol 88d74804…).

# FASE 0 (2026-11-05)

Todo lo de esta fase se midió sin escribir nada en el repositorio, salvo este informe y su fila de
`HOLDOUT-EXPOSICIONES.md`. Lo que hacía falta escribir para medirlo (los registros, el registro de
parámetros, las ambigüedades y la batería de tests) se escribió en un clon desechable,
`git worktree add --detach C:/cm/s6 HEAD` sobre `8cb07d6`, con su `config/settings.local.toml`
apuntando al `data/` real; el clon se quitó al terminar (`git worktree remove --force C:/cm/s6`;
`git worktree list` vuelve a dar solo el repo). Ninguna filtrada ni ninguna cruda se leyó: las citas
de abajo salen del texto de los ítems de `SESION-06-EXTRACCION.md` §8, leído en `knowledge/evidence/v17/`.

## 0. El encargo frente al repo (auditor)

El subagente `auditor-encargo` contrastó 101 afirmaciones: 75 correctas, 6 incorrectas y 20 con
matiz, más 12 herencias que el encargo no recoge. Lo que cambia algo de lo que se pide:

| # | Afirmación del encargo | Lo medido | Efecto |
|---|---|---|---|
| I1 | Las filas de A-49 y A-50 en Known Ambiguities «pasan a RESUELTA» / «cambian» | SALEN: `AMBIGUEDADES.md:6-11` («CERRARLA la toca QUITANDO la fila») y `test_kit.py:466-480` (la tabla son exactamente las ABIERTAS) | se quitan; la cuenta de bytes de (c) va con eso |
| I2 | Sacar A-49 y A-50 de `EN_PARTE_SESION_4` es «sin precedente» | El precedente es A-32 (`test_kit.py:316-320`, `trabajo/activar-sesion-05`) | ninguno |
| I3 | A-48 «a la sesión 7, C.6»; el «igual», «(C.7)» | A-48 es C.5; ADR-0083 es C.6; C.7 es la alternancia | se lee por el contenido |
| I4 | «A-35 y A-44 quedan con todos sus parámetros con valor» | `perdida_trader_reinicio_huso`, `perdida_trader_dia_usd` y `perdida_trader_semana_usd` siguen UNKNOWN (`parametros.yaml:1501-1531`); los dos de dinero no tienen efecto con `unidad = porcentaje`, el del reinicio usa el corte del perfil marcado SUPUESTO (`engine/tope_trader.py:189-194`) | la palabra es «con valor en los parámetros que el motor lee», como en ACTIVAR-SESION-05.md |
| I5 | Otros ítems «en sus notas» o «en las notas» de los registros de A.1, A.5 y A.7, y el «es indiferente» sin ítem | `ERRORES-RECURRENTES.md:37`: las notas de un `fb-*` solo con lo que trae su ítem; fue **bloquea** en `trabajo/activar-sesion-05` (b1, `ERRORES-RECURRENTES.md:99`). Un registro es inmutable | decisión 0 |
| M1 | Cerrar A-49 toca `test_kit.py:283` y `:321` | Y `test_una_en_parte_no_entra_en_resueltas` (`test_kit.py:441-463`) exige `sobre_a49 == []`: NINGÚN registro sobre A-49. Medido en el clon: falla | decisión 1 |
| M2 | A.2 resuelve la PARADA de §4 con su paso 2 | `ACTIVAR-A35-A44.md:190-192` pide también el paso 1, un RESOLVE_UNKNOWN sobre la ambigüedad, y la skill dice que el runbook gana | decisión 2 |
| M3 | La candidata va «en PREPARACION-A35-A44.md §5» | Es un informe cerrado en `main`: recuadro fechado junto a §5, cuerpo intacto (`CLAUDE.md`, «Regímenes de cambio») | decisión 3 |
| M4 | A.3: «la única lectura del selector en la que esa M1 toma» es que ninguna mecha POSTERIOR mueva | `no_mueve` también lo cumple (`test_mecha_que_vuelve.py:132-143`); lo que elige `solo_la_contraria` frente a `no_mueve` es el ejemplo de la sesión 5 (ADR-0084 §1, fuera de ítem) y `ev-v17-002250-d6ca3ef8`, que habla de la vela SIN CUERPO y no de la contraria. «El alto es el punto más alto, mechas incluidas» y «la vela sin cuerpo no corta la racha» son la conclusión de la extracción (`SESION-06-EXTRACCION.md:365-366`; notas de `ev-v17-002155-f2c95111`), no frases del trader | decisión 4 |
| M5 | A.3: «no hace falta ADR nuevo» | La hoja de la sesión 6 decía «con (a) … hace falta ADR» (`SESION-06-EXTRACCION.md:334-335`). Con `solo_la_contraria` el selector ya existe y ADR-0084 §2 lo describe: basta el recuadro, pero hay que decir que se aparta de la hoja | decisión 4 |
| M6 | A.3: CONFIRM sobre RN-004 con `ev-v17-001036-e7bdd027` | Dicho sobre su gráfico, con «suponiendo» (confianza media en el ítem): un ejemplo, no una regla general. Y lo que dice -otra vela verde actualiza la zona- es «el más reciente» de ADR-0045, que RN-004 no enuncia: RN-004 es «la liquidez de M15 se toma con cuerpo» (`strategy_spec.yaml:1236-1248`). En el clon, `feedback pending` lo da como «confirma la regla vigente RN-004, que cita fb-2026-09-09-sesion-01-6e15504f»: confirmaría una frase que el ítem no dice | decisión 5 |
| M7 | A-50 «y la hoja» | A-50 no está en `ORDEN_SESION_02` (`scripts/hoja_preguntas.py:56-60`): su quinto sitio no toca nada | ninguno |
| M8 | A.7: «de cuánto se pasa el 0 dijo “es indiferente”» | La extracción los separa: «es indiferente la verdad» (85:49) y «no entiende la pregunta de cuánto se pasa el 0» (86:37-86:41) (`SESION-06-EXTRACCION.md:573-574`); y de la caja a caballo solo dice que puede ir «entre», sin ítem (:575-577) | se remite a §3.4 con esas dos frases |
| M9 | C.1: «en las sesiones 1, 4 y 5 dijo las dos cosas» | La extracción: la 1 «apenas toca», la 4 «apenas cierra», la 5 las dos (`SESION-06-EXTRACCION.md:503-506`) | se escribe así |
| M10 | C.1: «las notas de break_even_condicion» | El parámetro no tiene notas, solo `descripcion` (`parametros.yaml:925-933`); la ambigüedad, `pregunta` y comentarios | va en la `descripcion` y en el texto de A-13 |
| M11 | A.1: `ev-v17-000134-725523bf`, «cierra al tocar el stop» | El ítem dice «por lo general» | se escribe con esas palabras |
| M12 | C.7: «la liquidez de la izquierda» con dos ítems | Solo la dice `ev-v17-003222-85f12e6b`; `ev-v17-002803-4c5ea744` habla de lo que hace después y de «ruidoso» | se cita cada uno por lo suyo |
| M13 | A.3: «solo si el test de docstrings lo exige» | Ningún test mira el docstring de `domain/pivotes_m15.py` (los que dicen «docstring» en `tests/` no lo tocan); y el contrato no permite `src/` | `src/` no se toca |

Herencias que el encargo no recoge y entran en esta rama sin decisión (son «la regla de la spec
que la citaba» o un texto que queda falso): las notas de RN-020 (`strategy_spec.yaml:803`,
`:2051-2055`), RN-004 (`:1298-1303`, dice `cualquier_mecha`), RN-007 (`:1467-1468`, «A la sesion
6…»), el texto de A-35 (`ambiguedades.yaml:973`, `:1012`) y de A-44 (`:1331`); y
`PROJECT_STATE.md:87` («C2 y C3 abiertas como A-48 y A-49»), que se ajusta en el commit de A-49. Las
que piden decisión van a §«Lo que necesito que decidas» (6 a 9).

**Comandos.** `feedback apply --check` va con `--sesion 2026-11-04-sesion-06` (`cli.py:3250`);
`feedback new` necesita además `--grabacion "Grabación de pantalla 2026-11-04 142903.mp4"`
(`knowledge/corpus/fuentes.yaml:198-199`), `--respuesta`, `--registrado-por`, `--objetivo-*` y
`--accion` (`cli.py:3213-3244`); `evidence contradictions` ESCRIBE `_contradicciones.yaml`, así que en
la fase 0 solo se corrió en el clon.

**Negativa de la guardia al auditor**, declarada: un `grep` de solo lectura sobre `GUARDIA-G1.md`
con el literal de una URL de fichero en el patrón (falso positivo: lo leyó como ruta). No lo
reescribió; buscó otros términos.

## a. Tabla de activación

Una fila por fila de `SESION-06-EXTRACCION.md` §5. «Cuadra» dice si la decisión del encargo casa con
lo medido; «no del todo» remite a §«Lo que necesito que decidas».

| Fila | Destino | Ítems | Qué hace hoy el código | Test que lo prueba | Cuadra |
|---|---|---|---|---|---|
| S-1 (A-44, magnitud) | A.1 | `000218-001b08fb`, `000134-725523bf` | `perdida_trader_magnitud` = `saldo` DEFAULT_AMBIGUOUS (`parametros.yaml:1456-1478`); lo lee `engine/tope_trader.py:176`; con `saldo` la abierta no cuenta (`:255`) | `test_preparar_a44.py:145-162` (registro real) y el de saldo/equity (`:165-`) | sí, con las notas de la decisión 0 |
| S-2 (A-44, reinicio) | A.2 / B.1 | `000250-a468bcec`, `000351-331daa6d`, `000321-37cebf44` | `SeguidorTope.avanzar` corta en la medianoche de `huso_reinicio` (`engine/tope_trader.py:230-240`); sin valor, el huso del perfil y SUPUESTO (`:189-194`) | `test_preparar_a44.py:151-158` (SUPUESTO con el registro real) | sí, con la decisión 2 |
| S-3 (A-35, la mecha) | A.3 | `001319-419307f6`, `001610-c43239a9`, `001712-dc155b5d`, `001728-b7b9a32c`, `001847-4e7b7c0b`; y `001036-e7bdd027`, `001543-c92f549c` | `cualquier_mecha`: las M1 posteriores mueven el nivel hasta la toma (`engine/motor.py:165-174`); con `solo_la_contraria` solo la contraria (`domain/pivotes_m15.py`, `_pivote_de`) | `test_mecha_que_vuelve.py:96-155`, `test_pivotes_m15.py:170-250` | no del todo: decisiones 4 y 5 |
| S-3, el nivel se congela | A.3 | `001728-b7b9a32c` («no sé si» detrás) | `nivel_con_mecha_que_vuelve` congela en la toma (`pivotes_m15.py:264-`); con `solo_la_contraria` no se llama (`motor.py:165`) | `test_mecha_que_vuelve.py:105-129` | sí: con `solo_la_contraria` deja de aplicarse, y el recuadro lo dice |
| S-4 (A-35, sin cuerpo en M15) | A.4 / B.2 | `002155-f2c95111`, `002250-d6ca3ef8`, `002217-af442f84` | M15 con `corta_la_racha`, M1 con `no_cuenta` (`pivotes_m15.py:67-72`, `:101-112`) | `test_pivotes_m15.py` (por marco) | sí, como lectura (M4) |
| S-18 (ADR-0083 D1) | A.9 / C.6 | `013939-860b33e0`, `013806-e8869c2a`, `013009-5e47afdb`, `013815-9cf6f076`, `012917-46a2c561` | el rechazo gasta el punto; el cierre sin ganancia lo libera (`engine/cableado.py:150-166`; `zonas.py:415`) | `test_punto_usado.py` | sí |
| S-7 (gráfico 1) | sin destino en el encargo | `004338-c8befc62`, `004407-42808be7` | — | — | decisión 8 |
| S-8 (gráfico 2) | C.10 | `004841-7f53bbb0`, `004910-11d48393` | — | — | sí |
| S-9 a S-12 | C.10 | — | — | — | sí |
| S-5 | C.7 | `002516-426ce5b2`, `002803-4c5ea744`, `002954-613d9421` | RN-009 (`strategy_spec.yaml:1517`) | `test_a21_series.py` | sí (M12) |
| S-6 | C.7 | `003356-f27b96e3`, `003222-85f12e6b` | igual | igual | sí |
| S-13 (A-13) | C.1 | `005111-8933dab2`, `005200-4f93afa0`, `005352-cda6245d`, `005454-90ce4feb`, `005554-172ecbb2` | `tocar`: vigilancia al tick (`cableado.py:322-326`) | `test_be_al_tick.py` | sí (b.5) |
| S-14 (A-53) | C.3 | `005730-76948af1`, `005846-0891a9c9`, `005914-55580dc0` | `se_mueve` (`parametros.yaml:836-856`) | `test_escenarios_por_sesion.py` | sí |
| S-15 (A-43) | C.4 | `010321-352430e3`, `010424-6d7f2d3f` | `cuenta`, CONFIRMED (`parametros.yaml:768-790`) | `test_escenarios_por_sesion.py:180-210` | sí |
| S-16 (A-48, el 1) | A.5 | `010541-05a69879`, `011328-a701a547` | `caja_bloque` = `r6` DEFAULT_AMBIGUOUS (`parametros.yaml:693-713`); `zonas.py:89`, `estructura_m1.py:68` | `test_orden_stop_pivote.py` (sintético), `test_selector_orden_stop.py` | sí, con la decisión 0 |
| S-16 (A-49) | A.6 | `011254-542726f6` (confianza media), `011419-0862662c`, `013815-9cf6f076` | `caja_se_fija` = `en_cada_cierre_m1` DEFAULT_AMBIGUOUS, `ejecucion` (`parametros.yaml:714-739`); `zonas.py:92` | `test_caja_hasta_el_llenado.py:28-32` | sí, con la decisión 1 |
| S-17 (A-50) | A.7 | `012500-39e18f12`, `012441-2ade00be`, `012715-8aaaa59f` | `caja_lado_de_ruido` = `caja_entera` DEFAULT_AMBIGUOUS; la forma de RN-005 (`zonas.py:111`, `:543`) | `test_caja_lado_de_ruido.py:124-135` | sí, con la decisión 0 y M8 |
| S-19 | B.4 | `014103-8cf3e7fb`, `014235-f3375358`, `014350-ec133d13` | la stop del lado equivocado es `precio_invalido` (`engine/broker.py:543-555`) y el rechazo al colocar gasta el punto (`cableado.py:151-165`; ADR-0083 D1) | `test_punto_usado.py` | sí (b.6) |
| S-20 | A.8 | `014603-63d190df`, `014644-674966b7`, `014736-30d2947b` | ADR-0085 §3: 1 o 2 puntos siguen siendo de su color; la mecha de la sin cuerpo cuenta | `test_pivotes_m15.py`, `test_estructura_m1.py` | sí (b.2) |
| S-21 | C.7 | `014945-9e7de278`, `015029-bc697500` | RN-009 | — | sí |
| S-22 | B.3 / C.9 | `015307-0870a8ca`, `015318-1256caf7`, `015404-06ac0e9d` | el punto se forma con cualquier roja que cierra tras una racha verde (ADR-0085 §3, tercera viñeta; `estructura_m1.py:201`, `ultimo_punto_de_ruptura`) | `test_estructura_m1.py` | sí |
| S-23 (A-46) | C.8 | `015726-ce2e42e4`, `015741-8f9fd638` | A-46 RESUELTA | — | sí |
| Para cerrar | D | `015829-7ba798f5`, `015854-de425918`, `000559-5a0a1597` | — | — | sí |

**Respuestas con «creo» o con un ejemplo sin regla general que el encargo activa:** (1) el CONFIRM de
RN-004, `ev-v17-001036-e7bdd027`, dicho sobre su gráfico con «suponiendo» (decisión 5); (2) S-3, el
nivel se congela, con el «no sé si» de `ev-v17-001728-b7b9a32c`: va al recuadro de ADR-0084 como
dicho «con ese no sé si», sin fijar nada; (3) `ev-v17-012917-46a2c561` (S-18), con «a lo mejor» y
«qué raro»: solo al recuadro de ADR-0083. El resto de lo que se activa (S-1, S-16 ×2, S-17, S-20) es
regla general sin «creo» según la tabla de la extracción.

## b. Lo medido

### b.1 Los registros de A.1, A.5, A.6 y A.7, escritos en el clon

Los seis `feedback new` del ensayo (A.1, A.5, A-49, A-50 y su parámetro, más el CORRECT de A.8 y el
CONFIRM de RN-004) salieron `OK`. `feedback apply --sesion 2026-11-04-sesion-06 --check`:

```
  ~ caja_bloque                  'r6'  <- fb-…-5ad747e7
  ~ caja_lado_de_ruido           'caja_entera'  <- fb-…-6f849f8c
  ~ perdida_trader_magnitud      'saldo'  <- fb-…-ce093488
3 parametros; 3 cambian, 0 ya estaban
```

(«cambian» porque pasan de DEFAULT_AMBIGUOUS a CONFIRMED: el valor es el mismo.) Sin `--check`
escribe los tres CONFIRMED con fuente `feedback` y les quita `ambiguedad_id`
(`feedback/aplicar.py:275-306`). `caja_se_fija` no aparece: es `ejecucion` y apply la rechazaría
(`aplicar.py:187-192`); pasa a mano. Los ids del ensayo no son los de la rama (el hash cambia con el
texto definitivo). Con todo eso y A-49 y A-50 en RESUELTA, `knowledge validate` en el clon:
`OK: 198 registros de feedback …`, `OK: 640 items de evidencia, 0 contradicciones abiertas` (con
`spec_version` subida a 18.5.3 y el manifiesto regenerado; sin subirla, `ERROR: spec: … el hash no
coincide`). `feedback pending`: ninguno de la sesión 6 pendiente; el CORRECT de A.8 sale como
«(?) … sin forma mecanica de cruzarlo», igual que sus dos precedentes, y el CONFIRM de RN-004 como
«(=) confirma la regla vigente» (M6). `test_registro.py` y `test_provisional_cuelga_de_abierta.py`,
en verde en el clon.

### b.2 El CORRECT sobre `ev-v16-000851-f5ae3b6f`

En el clon pasa `knowledge validate` (arriba) y `evidence contradictions`:
`OK: knowledge/evidence/_contradicciones.yaml con 0 contradicciones abiertas`. La respuesta literal
del ensayo es la de `ev-v17-014736-30d2947b` («una vela de uno o dos puntos con cuerpo en el retroceso …
es válido … como cambio de color para trazar el punto»).

### b.3 Los cambios a mano

`liquidez_m15_mecha_que_vuelve` a `solo_la_contraria` con fuente `ev-v17-001319-419307f6` (sigue
DEFAULT_AMBIGUOUS, A-35) y `caja_se_fija` a CONFIRMED sin `ambiguedad_id` con fuente `decision`
ADR-0074: `test_registro.py` (`:163-180`: estrategia con feedback o evidence; ejecución con
decisión) y `test_provisional_cuelga_de_abierta.py` en verde en el clon.

### b.4 Los tests que cambian de sentido

En el clon, con todo lo de b.1 a b.3, 70 ficheros de test (los que leen `parametros.yaml`,
`ambiguedades.yaml`, el feedback o la spec, más `test_pivotes_m15.py` y `test_transcribir_sesion.py`),
nombrados uno a uno: **10 fallan**, y todos son los que congelan el estado de hoy. En `main` (mismo
código, el `make check` de `8cb07d6`: `3210 passed`) los diez pasan.

| Test | Por qué falla | Cambio a propósito |
|---|---|---|
| `test_mecha_que_vuelve.py::test_el_registro_real_trae_el_selector_como_lectura_del_consultor` | espera `cualquier_mecha` y la fuente de la sesión 5 | `solo_la_contraria`, fuente `ev-v17-001319-419307f6` |
| `test_mecha_que_vuelve.py::test_por_el_camino_real_las_mechas_mueven_el_nivel_y_la_toma_lo_congela` | con el registro real el nivel queda `[134, 134, 134]`, no `[137, 138, 138]` | por el camino real, la M1 posterior NO mueve el nivel y la que cierra sobre 134 toma; el caso (ii) pasa a pedirse con `cualquier_mecha` explícito |
| `test_mecha_que_vuelve.py::test_un_valor_fuera_del_enum_falla_al_leer_el_registro` | busca la línea `valor: cualquier_mecha` | la de `solo_la_contraria` (una sola en el fichero: se comprueba) |
| `test_caja_hasta_el_llenado.py::test_el_registro_dice_en_cada_cierre_m1_bajo_a49` | espera DEFAULT_AMBIGUOUS bajo A-49 | CONFIRMED, sin `ambiguedad_id`, fuente decisión ADR-0074 |
| `test_caja_lado_de_ruido.py::test_el_registro_real_y_un_valor_fuera_del_enum` | espera DEFAULT_AMBIGUOUS bajo A-50 y la fuente de la sesión 5 | CONFIRMED, fuente `feedback` (el `fb-*` de A.7) |
| `test_kit.py::test_ambiguedades_reales_y_esquema` | RESUELTAS | gana A-49 y A-50 |
| `test_kit.py::test_una_en_parte_no_entra_en_resueltas` | A-49 y A-50 en `EN_PARTE_SESION_4` y `sobre_a49 == []` | salen de `EN_PARTE_SESION_4`; el bloque de A-49 (decisión 1) |
| `test_kit.py::test_project_state_refleja_las_ambiguedades_abiertas` | las filas de A-49 y A-50 | se quitan de la tabla |
| `test_hoja_preguntas.py::test_cada_pregunta_sale_tal_cual_y_en_su_orden` y `::test_escribe_un_docx_que_se_abre` | la hoja se niega a llevar A-49 RESUELTA | A-49 sale de `ORDEN_SESION_02` y de `ORDEN` del test |

No cambia: `test_preparar_a44.py` (la magnitud sigue siendo `saldo`; solo su docstring dice
«DEFAULT_AMBIGUOUS bajo A-44» y se ajusta), `test_escenarios_por_sesion.py`,
`test_selector_orden_stop.py`, `test_orden_stop_pivote.py` (sustituyen líneas que no cambian),
`test_pivotes_m15.py` (pasa la opción explícita), `test_hoja_de_ruta.py` (sus Refs solo exigen que el
id exista, `test_hoja_de_ruta.py:156-157`) y `test_transcribir_sesion.py` (el orden de las hojas 02 y
03 es historia fija). El test de A.10 es nuevo (control de la sesión 6).

### b.5 La opción `cierre` de `break_even_condicion`, de punta a punta

Está implementada. RN-014 nombra el instante en su forma (`mover_stop: {… cuando:
break_even_condicion}`, `strategy_spec.yaml:1764`), que `mover_stop` lee (`primitivas_broker.py:765-773`).
El predicado deja el nivel en el contexto en cada cierre (`zona_posterior_completada` con
`break_even_criterio_ruptura`, `primitivas_broker.py:282-288`), y el cableado lo arma al tick SOLO con
`tocar` (`cableado.py:322-326`); con `cierre` el stop pasa en el cierre de la M1, fuente `cierre_m1`
(ADR-0065 §5). Lo prueba por el motor `test_be_al_tick.py:236-271`, parametrizado
`[("tocar", -3, True), ("cierre", -16, False)]`; la fuente `cierre_m1`, `:286-294`. **No hay test por
el motor con el criterio `cuerpo`**: si la sesión 7 dice «cierre con cuerpo», son dos CORRECT con
`supersede` (`fb-2026-09-09-sesion-01-0ccafcba` y `fb-2026-09-29-sesion-03-2cff5008`) y un test por
el motor con `cierre` + `cuerpo` antes de dar el cambio por hecho.

### b.6 Recuentos en las salidas de `docs/validation/anexos/RESPALDO-M1/`

Con un guion de la carpeta de trabajo que cuenta por sección y no imprime filas (solo recuentos;
los meses son de construcción):

| Salida | Órdenes | Rechazadas al colocar | Motivo | `stop_movido` (break even) |
|---|---|---|---|---|
| `diaria.DIAGNOSTICO.cuenta=diaria.txt` | 1.329 (1.006 canceladas, 286 llenadas, 37 rechazadas) | 37 (enero 8, abril 10, julio 9, agosto 10) | todas `precio_invalido`; 0 `stops_level` | 118 (114 al tick, 4 por el respaldo M1) |
| `cuenta-arrastrada.txt` | 215 (158, 53, 4) | 4 (enero) | todas `precio_invalido` | 21 (20 al tick, 1 respaldo) |

`precio_invalido` es exactamente la pendiente del lado equivocado (`broker.py:553-555`): las 37
rechazadas de la diaria son la situación de S-19, y con D1 cada una gasta su punto. 118 de 286
llenadas pasaron por break even: es lo que movería un cambio de `break_even_condicion` (C.1).

### b.7 Quién espera lo que se cierra o se fija

- **A-49:** `PROJECT_STATE.md:79` (fila) y `:87` (candidatas: «C2 y C3 abiertas como A-48 y A-49»);
  `HOJA-DE-RUTA.md:46` (R1.1), `:62`, `:250` (R4.1), `:280-283` (R4.2); `scripts/hoja_preguntas.py:58`.
- **A-50:** `PROJECT_STATE.md:80`; `HOJA-DE-RUTA.md:46`, `:62`, `:250`, `:281`, `:299`, `:558`.
- **Parámetros:** `caja_bloque` (`engine/zonas.py:89`, `domain/estructura_m1.py:68`), `caja_se_fija`
  (`zonas.py:92`), `caja_lado_de_ruido` (`zonas.py:111`, `:543`), `perdida_trader_magnitud`
  (`tope_trader.py:47`; `ACTIVAR-A35-A44.md:19`, `:52`, `:106-107`), `liquidez_m15_mecha_que_vuelve`
  (`motor.py:165`, `arnes.py:214`, `visor.py:320`). `CLAUDE.md` no nombra ninguno.
- La hoja de ruta no se toca en la rama; sus Refs a A-49 y A-50 no rompen ningún test (b.4).

### b.8 La línea de Technical Debt de D

PAGADA por la C de `trabajo/guardia-g1`: en Bash `resolver` expande las llaves (`_llaves`,
`.claude/hooks/guardia.py:1918`) y una URL `file:` se mira como su ruta (`:1694`, `:2141-2148`;
`GUARDIA-G1.md:911-912`), con `test_h_las_llaves_y_las_url_en_bash_se_niegan` y la medida en Windows
(`GUARDIA-G1.md:1598-1601`). Lo que queda es el «Riesgo residual de C» (`PROJECT_STATE.md:98`), que
no se toca. La línea `PROJECT_STATE.md:145` sale en el commit del contrato con esa cita.

### b.9 Lo que el encargo hereda

- Next Action F: es este encargo; su texto nuevo, en las líneas del cierre.
- `HOJA-DE-RUTA.md:242`: R3.7 depende de «la activación de la sesión 6 (R4.2)»; el encargo solo pide
  la precisión para R3.6. Propuesta: R3.7 gana la misma coletilla (decisión 9).
- `HOJA-DE-RUTA.md:599`: una entrada HECHA («antes de ingerir la sesión 6»): nada.
- `HOJA-DE-RUTA.md:638`: la fecha fija «el martes 3 de noviembre» (sale en el cierre); y
  `docs/runbooks/DEMO-FTMO.md:138` dice lo mismo: línea del cierre (decisión 9).
- J (`PROJECT_STATE.md:40`): «antes de la próxima sesión con el trader que use la hoja»: R4.3 depende
  también de J si la hoja de la 7 sale de `kit hoja` (decisión 9).
- El final de `docs/state/HISTORIA.md` (registro de cierre de `trabajo/sesion-06`): nada pendiente
  para esta rama que no esté en el encargo.
- Technical Debt, ADR 0087 (`PROJECT_STATE.md:103`): sin relación con lo que se activa aquí; sigue.

### b.10 La hoja de preguntas

Cerrar A-49 solo toca `ORDEN_SESION_02` (`scripts/hoja_preguntas.py:56-60`) y `ORDEN` de
`tests/unit/test_hoja_preguntas.py:28-32`; los dos tests que fallan en el clon (b.4) lo piden y nada
llama a `kit hoja`. A-50 no está en la hoja. Sin PARADA.

## c. El tamaño de PROJECT_STATE

En memoria, sobre el de `main` (23.247 bytes), con un guion que no escribe: salen las filas de A-49
(105 bytes) y A-50 (134) y la línea de Technical Debt de D (208); la F pasa de 788 a 448 bytes; L gana
«caja_bloque ya no cuelga de ese ítem (sesión 6).»: **22.511 bytes**; con lo que el cierre siempre
sustituye (Current Feature, Stable Main State, Last Stable Commit, los «Archivo N»), **unos 22.389**.
Cabe en los 23.000 que pide el encargo (el tope del test es 25.000, `tests/unit/test_project_state.py`)
sin mover nada.

## d. El plan de commits

1. A-44, la magnitud (A.1): registro sobre el parámetro, apply, `descripcion`, nota de A-44 y de
   RN-020, `test_preparar_a44.py` (docstring), spec_version.
2. A-35 (A.3, A.4): `liquidez_m15_mecha_que_vuelve` a mano, nota de A-35 y de RN-004 (y RN-007),
   recuadro de ADR-0084 y su fila, los tres tests de `test_mecha_que_vuelve.py` (y, si se decide, el
   CONFIRM de RN-004: decisión 5).
3. A-48, `caja_bloque` (A.5): registro, apply, nota de A-48 con «desviación», recuadro de ADR-0064
   (decisión 7), spec_version.
4. A-49 (A.6): registro sobre la ambigüedad, `caja_se_fija` a mano, los cinco sitios, recuadro de
   ADR-0074 y su fila, `test_kit.py`, `test_caja_hasta_el_llenado.py`, la hoja y su test,
   `PROJECT_STATE.md:87`.
5. A-50 (A.7): dos registros, apply, los cinco sitios (la hoja no lo lleva), nota de RN-005,
   `test_kit.py`, `test_caja_lado_de_ruido.py`.
6. S-20 (A.8): CORRECT sobre `ev-v16-000851-f5ae3b6f`, recuadro de ADR-0085 §3 y su fila, nota de RN-004
   (el matiz de M15).
7. S-18 (A.9): recuadro de ADR-0083 y su fila.
8. S-2 (A.2): NOTA de `ACTIVAR-A35-A44.md`, recuadro junto a §5 de `PREPARACION-A35-A44.md`, nota de A-44.
9. A.10: el test de control de la sesión 6.
10. El informe: §«Para la rama de motor», §«Para la sesión 7», las líneas del cierre.

Cada uno: `knowledge validate` antes, `make check`, y `Fuente:` en el cuerpo con los `fb-*` ya
escritos.

## Lo que no pude medir

- Los ids definitivos de los registros: el hash depende del texto final (notas incluidas), que espera
  a la decisión 0.
- El número total de tests de la batería del clon: el `tail` cortó la línea de resumen; los diez
  fallos son la lista entera de `-rf`.
- El arnés: prohibido en la rama. Que `solo_la_contraria` cambie operaciones del bot no se mide aquí:
  lo mide la re-corrida que cuenta (ADR-0070 §3), después de la rama de motor.

## Exposiciones

Una fila nueva en `HOLDOUT-EXPOSICIONES.md` (2026-11-05): (1) los recuentos de b.6 sobre las dos
salidas del respaldo (construcción; solo recuentos, y los de la tabla de rechazos por mes de
construcción); (2) la batería del clon, que como cada `make check` lee el M1 de marzo para calentar
(Technical Debt, `test_visor.py` y `test_preparar_a35.py`) y data/ real; (3) el auditor abrió ADR-0083
§4 y §6, que nombran un día de julio y dos ventas de abril (desarrollo), y algunas salidas de grep
traían fechas de enero (desarrollo). Ningún día reservado, ninguna filtrada, ninguna cruda, ningún
listado de `knowledge/cases`.

## Lo que necesito que decidas

0. **Las notas de los registros.** El encargo pone otros ítems (y una frase sin ítem) en las notas de
   los registros de A.1, A.5 y A.7; `ERRORES-RECURRENTES.md:37` lo prohíbe y fue **bloquea** en la
   sesión 5. Opciones: (a) las notas de cada `fb-*` solo con lo de su ítem, más la palabra
   «desviación» en el de A.5; los otros ítems a la `descripcion` del parámetro, a la nota de la
   ambigüedad o de la regla y al informe; (b) como dice el encargo. Recomiendo (a): un registro es
   inmutable y (b) repite un error ya medido. Coste de (b): un hallazgo bloquea del revisor que no se
   puede arreglar.
1. **El test que prohíbe registros sobre A-49** (`test_kit.py:441-463`, `sobre_a49 == []`). Opciones:
   (a) reescribirlo a propósito: sobre A-49 hay exactamente un registro, el RESOLVE_UNKNOWN de la sesión
   6, y el CONFIRM de la sesión 4 sigue sobre su ítem (`fb-2026-10-04-sesion-04-35a080e2`); el
   docstring y el comentario de `:313-316` lo cuentan; (b) cerrar A-49 sin registro sobre ella, como
   DECIDIDA por ADR-0074. Recomiendo (a): el trader lo dijo con regla general y A-49 es `pregunta`.
   Coste de (b): un ADR nuevo y A-49 cerrada por el consultor cuando la cerró el trader.
2. **El paso 1 de §4 del runbook (S-2).** `ACTIVAR-A35-A44.md:190-192` pide un RESOLVE_UNKNOWN sobre
   A-44 con la cita, dejándola ABIERTA. Opciones: (a) sin registro, como en las sesiones 3 y 5 (sobre
   A-44 no hay ninguno, medido), con la palabra «desviación» del paso 1 en la NOTA y en el informe; el
   registro sobre el parámetro nuevo va en la rama de motor; (b) el registro del paso 1 ahora. Recomiendo
   (a): un RESOLVE_UNKNOWN activo sobre una ABIERTA es lo que `test_kit` vigila en A-49, y cerrar A-44
   lo decides en la PARADA de la rama de motor. Coste de (b): un registro sobre una «en parte», contra
   tu regla de «Qué no cambia».
3. **La candidata en `PREPARACION-A35-A44.md` §5.** Es un informe cerrado. Opciones: (a) un recuadro
   fechado junto a §5, con la lectura nueva y sus dos ítems, el cuerpo intacto; (b) una línea dentro
   de §5. Recomiendo (a): es la regla de `docs/validation/`. Coste de (b): un cuerpo cerrado editado.
4. **A.3, en qué boca va cada cosa.** Lo que el trader dijo descarta `cualquier_mecha` (la (a),
   `ev-v17-001712-dc155b5d`) y no elige entre `no_mueve` y `solo_la_contraria`; «mechas incluidas» y
   «no corta la racha» son de la extracción. Opciones: (a) `solo_la_contraria`, LECTURA DEL CONSULTOR,
   con este motivo escrito: entre las dos que la (a) deja, la que conserva el ejemplo de la sesión 5
   (ADR-0084 §1); el recuadro de ADR-0084 dice que se aparta de la hoja («hace falta ADR») porque el
   selector y su opción ya existen, y que `ev-v15-000553-9d95178a` (que contestaba al caso (ii)) queda
   sin CORRECT, en tensión, a la sesión 7 (C.2); (b) `no_mueve`, con la frase de 13:19; (c) como el
   encargo. Recomiendo (a). Coste de (c): el recuadro pondría en boca del trader dos conclusiones del
   informe (lo que el revisor de la sesión 5 marcó como b2).
5. **El CONFIRM sobre RN-004 con `ev-v17-001036-e7bdd027`.** Opciones: (a) sin registro: el ítem va a
   las notas de RN-004 como lo que ya hace «el más reciente» de ADR-0045, dicho sobre su gráfico;
   (b) CONFIRM sobre RN-004; (c) CONFIRM sobre el ítem de ADR-0045 (`ev-v1-001334-96e8ca40`).
   Recomiendo (a): es un ejemplo con «suponiendo», y RN-004 no dice lo que el ítem confirma. Coste de
   (b): `feedback pending` lo cuenta como confirmación de la cita de la sesión 1 sobre el cuerpo.
6. **Las notas de reglas que quedan falsas** (RN-020, RN-004, RN-007, A-35, A-44; arriba). Opciones:
   (a) en el commit de cada respuesta; (b) en un commit propio al final. Recomiendo (a).
7. **ADR que dicen lo contrario sin recuadro**: ADR-0053 (`:130-133`, `:226-228`: la magnitud no la
   dijo el trader), ADR-0054 (`:46`, `:121`), ADR-0064 (`:165`, `caja_bloque` provisional) y ADR-0074
   (`:64`). Opciones: (a) recuadro fechado de una o dos líneas en cada uno, con su fila del índice, en
   el commit de su respuesta; (b) solo ADR-0074, y ADR-0053 en la rama de motor. Recomiendo (a): tu
   alcance 1 del revisor («nada contradice un ADR sin recuadro»). Coste de (b): ADR-0053 y ADR-0064
   dicen hasta la rama de motor que un valor del trader es nuestro.
8. **S-7 (gráfico 1)** no tiene destino. Opciones: (a) C, sin pregunta nueva: dijo (a), no hubo toma,
   sobre un M15 que no ve claro; va como contexto de los gráficos 2 a 6; (b) D. Recomiendo (a). Y a
   §«Para la sesión 7» se añaden, de la extracción, su juicio sobre los esquemas (§4.1, 16) y el
   consejo de la trendline (§3.6), remitidos sin citar.
9. **Las líneas del cierre que el encargo no nombra.** (a) R3.7 gana también «y la activación de la
   sesión 6 (R4.2), rama de motor incluida»; R4.3 depende de la rama de motor y de J si la hoja sale de
   `kit hoja`; `DEMO-FTMO.md:138` («el martes 3») se corrige en el commit del contrato; (b) solo lo del
   encargo. Recomiendo (a).

Espero tu respuesta a la PARADA.

## Respuesta del consultor a la PARADA (2026-11-05)

Dada por Aleks (consultor) el 2026-11-05. Copiada tal cual:

> Respuesta del consultor a la PARADA de trabajo/activar-sesion-06 (2026-11-05). Cópiala tal cual al final del encargo y del informe, en «Respuesta del consultor a la PARADA», con su fecha, y aplícala punto por punto (skill fase-cero). Si al aplicar algo medido lo contradice, PARADA 2.
>
> 0. (a). Las notas de cada fb-* solo con lo que trae su ítem, más la palabra «desviación» en el de caja_bloque; los demás ítems y la frase sin ítem van a la descripción del parámetro, a la nota de la ambigüedad o de la regla y al informe. Corrige mi error, y es repetido: el revisor de la sesión 5 lo marcó como bloquea (ERRORES-RECURRENTES.md:37 y :99). Lección para la fila del consultor en el cierre: un registro lleva un ítem y nada más; lo que acompaña va a la descripción.
> 1. (a). test_una_en_parte_no_entra_en_resueltas se reescribe a propósito: sobre A-49 hay exactamente un registro, el RESOLVE_UNKNOWN de la sesión 6, y el CONFIRM de la sesión 4 sigue sobre su ítem (fb-2026-10-04-sesion-04-35a080e2); el docstring y el comentario de :313-316 lo cuentan, y el commit y el informe dicen que cambia de sentido. Motivo: el trader lo dijo con regla general y A-49 es pregunta, no decisión.
> 2. (a). Ningún registro sobre A-44, como en las sesiones 3 y 5, con la palabra «desviación» del paso 1 de §4 en la NOTA de ACTIVAR-A35-A44.md y en el informe; el registro sobre el parámetro nuevo va en la rama de motor. Motivo: un RESOLVE_UNKNOWN activo sobre una ABIERTA es justo lo que test_kit vigila, y el cierre de A-44 se decide en la PARADA de la rama de motor.
> 3. (a). Recuadro fechado junto a §5 de PREPARACION-A35-A44.md con la lectura nueva y sus dos ítems; el cuerpo intacto. Corrige mi error: es un informe cerrado.
> 4. (a). solo_la_contraria, LECTURA DEL CONSULTOR, con este motivo escrito en la descripción y en el recuadro de ADR-0084: la (a) de ev-v17-001712-dc155b5d descarta cualquier_mecha; entre las dos lecturas que quedan, la que conserva el ejemplo de la sesión 5 (ADR-0084 §1) es solo_la_contraria. El recuadro dice que se aparta de la hoja de la sesión 6 («hace falta ADR») porque el selector y su opción ya existen, y que ev-v15-000553-9d95178a, que contestaba al caso (ii), queda sin CORRECT y en tensión hasta la sesión 7 (C.2). Corrige mi error: «mechas incluidas» y «no corta la racha» son conclusiones de la extracción, no frases del trader; nada de eso va en boca suya. La confirmación de C.2 para la sesión 7 se reescribe con lo que sí dijo: que la mecha de una vela posterior que pasa y vuelve no mueve el alto, y que lo toma la vela de M1 que cierra con cuerpo por encima; y se le pregunta aparte, con el esquema de la sesión 5, si la mecha de la propia vela roja que forma el alto es el alto.
> 5. (a). Sin CONFIRM: ev-v17-001036-e7bdd027 va a las notas de RN-004 como lo que ya hace «el más reciente» de ADR-0045, dicho sobre su gráfico y con «suponiendo». Corrige mi error: RN-004 no enuncia lo que ese ítem confirma.
> 6. (a). Las notas de RN-020, RN-004, RN-007, A-35 y A-44, y PROJECT_STATE.md:87, se corrigen en el commit de la respuesta que las deja falsas.
> 7. (a). Recuadro fechado de una o dos líneas en ADR-0053, ADR-0054, ADR-0064 y ADR-0074, cada uno con su fila del índice, en el commit de su respuesta. Motivo: es el alcance 1 del revisor.
> 8. (a). S-7 va a C sin pregunta nueva, como contexto de los gráficos 2 a 6; y a §«Para la sesión 7» entran, remitidos sin citar, su juicio sobre los esquemas (SESION-06-EXTRACCION.md §4.1, 16) y el consejo de la trendline (§3.6).
> 9. (a). En las líneas del cierre: R3.7 gana «y la activación de la sesión 6 (R4.2), rama de motor incluida»; R4.3 depende de la rama de motor y de J si la hoja sale de kit hoja; DEMO-FTMO.md:138 («el martes 3») se corrige en el commit del contrato.
>
> Además, de §0:
> 10. I4: la frase es «A-35 y A-44 quedan con valor en los parámetros que el motor lee, y siguen ABIERTAS», como en ACTIVAR-SESION-05.md; perdida_trader_reinicio_huso, perdida_trader_dia_usd y perdida_trader_semana_usd siguen UNKNOWN y sin efecto, y la nota de A-44 lo dice.
> 11. I1 e I2: las filas de A-49 y A-50 salen de Known Ambiguities, y el precedente para sacarlas de EN_PARTE_SESION_4 es A-32: el commit lo cita. Corrige mis dos errores de redacción del encargo.
> 12. M8, M9, M10, M11 y M12: se escriben como lo medido (las dos frases de §3.4 por separado; la 1 «apenas toca», la 4 «apenas cierra», la 5 las dos; la contradicción de A-13 en la descripcion de break_even_condicion y en el texto de A-13; «por lo general» en lo de ev-v17-000134-725523bf; cada ítem de C.7 por lo suyo).
> 13. Para §«Para la sesión 7», con los recuentos de b.6: la pregunta del break even (C.1) va la primera y el informe dice por qué, 118 de 286 llenadas pasaron por break even; y la de S-19 lleva el recuento de las 37 rechazadas por precio_invalido, para la PARADA de la rama de motor.
> 14. La negativa de la guardia al auditor (el grep con una URL de fichero en el patrón) queda declarada en el informe como está; no se reescribe el comando.
>
> Sigue lo que manda el encargo: un commit por respuesta en el orden de d, knowledge validate antes de make check, Fuente: en el cuerpo con ids que existen, spec_version subida, CI de Linux por fix/activar-sesion-06 con su número de run (gh run view suelto), revisor (opus) con los cinco alcances del encargo y su informe pegado al final. Si el clasificador niega un push o la guardia un make, dame el comando exacto y lo lanzo yo con «!».
>
> Rama lista para revisión, NO cerrada.

## Estado

EN CURSO: respuesta del consultor recibida; se aplica punto por punto.
