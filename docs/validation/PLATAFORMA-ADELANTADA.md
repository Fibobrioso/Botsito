# PLATAFORMA-ADELANTADA · La capa de MT5 que no decide operaciones, adelantada antes de F26 (ADR-0082), y PROJECT_STATE adelgazado

Rama `trabajo/plataforma-adelantada`, abierta el 2026-10-18 desde `main` en 8642b8c (commit de
estado sobre el merge 7d3783d, tag `stable/F37t-visor-construccion`). Encargo:
`docs/encargos/trabajo-plataforma-adelantada.md`. Tramo: R0 («Lo que ordena el trabajo»; la rama
reordena la hoja de ruta y el tramo R6a aun no existe al abrirla). Modelo de la sesion: Opus,
esfuerzo medio, fijados por Aleks en su terminal antes del encargo.

(Hasta que existió, ADR-0082 iba declarado aquí en un bloque `ids-inexistentes`; salió en el commit
que lo creó.)

## Apertura: la base, comprobada con git

- `git rev-parse main origin/main`: `8642b8c2affe157e82ba9d73815fe7f1a62eaf32` las dos veces.
- `git rev-parse main^1` y `git rev-parse "stable/F37t-visor-construccion^{commit}"`:
  `7d3783dbc5e562fc97ad39a84532454fea9132b5` las dos; el tag esta en origin
  (`git ls-remote --tags origin stable/F37t-visor-construccion`: `2fe6cfd...`, el objeto del tag
  anotado). Es el ultimo `- Tag: ` de `docs/state/HISTORIA.md`.
- CI de `main` sobre 8642b8c2affe157e82ba9d73815fe7f1a62eaf32 (API de check-runs, sha literal):
  `python` · `completed` · `success`.
- `git branch --list`: solo `main`; `git ls-remote --heads origin "fix/*"`: vacio.

## Fase 0 · inventario (sin tocar nada)

Medido el 2026-10-18 en la rama, sobre el árbol de `main` 8642b8c. Cada hallazgo con
`fichero:línea`; las búsquedas, con `Grep` sobre las rutas que se nombran.

### a) Dónde se dice que F26 va antes de cualquier MQL5

Búsqueda: `(F26|fidelidad).{0,120}(MQL5|MT5|MetaTrader)` y su inversa, y «antes de cualquier
MQL5» / «precede a cualquier», en `CLAUDE.md`, `docs/runbooks/`, `.claude/`, `docs/plan/`,
`docs/adr/`, `docs/research/` y `PROJECT_STATE.md` (y una segunda pasada de `mql5|F26` en
`CLAUDE.md`, `docs/runbooks/` y `.claude/`).

**Sitios vivos (se alinean en la fase 2/3):**

| Sitio | Texto | Qué se hace |
|---|---|---|
| `PROJECT_STATE.md:167` | «La validacion de fidelidad (F26) precede a cualquier MQL5.» | se sustituye (fase 2) y la vieja va a HISTORIA |
| `docs/plan/MASTER_PLAN.md:27` (§0) | «Validacion de fidelidad (F26) antes de cualquier MQL5.» | el cuerpo no se toca: NOTA nueva arriba (fase 2) |
| `docs/plan/HOJA-DE-RUTA.md:263` (R6.1) | «**Depende de:** R5.5 (fidelidad antes de MQL5, MASTER_PLAN §A).» | se reescribe (fase 3). La atribución a «§A» no es exacta: el principio está en §0 (`MASTER_PLAN.md:27`); §A solo lo refleja en la fila de F30 («F29, F26», `MASTER_PLAN.md:114`) |

**No son la regla, y no se tocan:**
- `docs/plan/MASTER_PLAN.md:114` (fila F30, «Depende de: F29, F26»): coherente con D2 (F30 sigue
  esperando a F26). Y `MASTER_PLAN.md:137` (§D, `F30 (◄ F26)`), lo mismo.
- `docs/adr/0006-capas-revisadas-y-paquete-comun.md:12`: «`validation` (F26, F30, F32) conduce el
  motor y el puente MQL5»: describe capas, no orden.
- `docs/plan/features/F11-strategy-spec-schema.md:170`: enumera funcionalidades; no ordena.

**Instantáneas congeladas, informes cerrados y HISTORIA (solo se listan):**
- `docs/plan/MASTER_PLAN.html:115` («Validación de fidelidad antes del EA… antes de escribir una
  línea de MQL5 (fase 6)»), `:384` (FASE 5, «la medición de fidelidad antes de escribir MQL5»),
  `:609` (grafo, `F30 differential ◄── F26`), `:697` (la secuencia del método) y `:783` («La
  validación de fidelidad (F26) precede a cualquier MQL5.»).
- `docs/research/2026-09-03-del-corpus-al-bot.html:635` («La validación contra el trader era el
  paso 15 de 18. Aquí es la etapa 4 de 9, antes del EA y del backtest de ventaja»).
- `docs/state/HISTORIA.md`: cada Archivo copia la línea de PROJECT_STATE (también el Archivo 37 de
  esta rama).
- Informes cerrados: ninguno la enuncia como regla (la búsqueda solo da
  `docs/validation/F15-market-data-ohlc.md:145`, que habla de capas).

**`CLAUDE.md`, `docs/runbooks/` y `.claude/`: ningún sitio.** Lo único que nombra MQL5 allí es
`docs/runbooks/DEMO-FTMO.md` (cómo copiar `tools/mql5/MedirDemoFTMO.mq5`) y su línea en
`docs/runbooks/README.md:20`. No hay PARADA por a).

### b) Dónde vive la capa (D4): las dos lecturas, con su cita

**Lectura 1 · El EA de MQL5.**

| Sitio | Lo que dice |
|---|---|
| `docs/adr/0001-repository-structure-and-change-regimes.md:10-12` | «`mql5/` (ejecucion, con parametros generados desde `knowledge/spec/`)»; y :21, «exige dos implementaciones (Python y MQL5) que lean la misma fuente» |
| `docs/plan/MASTER_PLAN.md` §A, `:112-118` | F28 «Params.mqh y fixtures generados»; F29 «Dominio en MQL5»; F31 `feature/F31-mql5-expert-advisor` «EA, ordenes idempotentes, veto de riesgo, journal» (dep. F29, F30); F33 «Demo, pre-vuelo, runbooks» (dep. F17, F31) |
| `MASTER_PLAN.md` §B, fila `mql5/` | «EA, includes (Params.mqh generado), RunCases, tester (fase 6)» |
| `MASTER_PLAN.md` §H, fila «MQL5: …» | «verificacion de `ACCOUNT_MARGIN_MODE` al arrancar; journal con flush y hash encadenado; veto de riesgo con parametros propios» → F29, F31 |
| `MASTER_PLAN.md` §H.2, fila de parámetros sin hogar | «F28: `Params.mqh` (estrategia+instrumento+ejecucion) y `Risk.mqh` (prop_firm) con dos hashes en el journal. F33: `[broker]` en settings, entorno `real`, pre-vuelo contra `SymbolInfo*`/`AccountInfo*`» |
| `MASTER_PLAN.md` §H.2, fila «Veto de riesgo solo en MQL5» | RN-029..RN-032 son «regla pura del dominio…; F24 la ejecuta; F28 la exporta; F30 la cubre; el journal registra cada veto como abstencion» |
| `MASTER_PLAN.md` §H.2, fila «Estado de jornada no persistente en el EA» | «F31: al arrancar reconstruye la jornada desde el historial de MT5 (magic + comentario con `spec_hash` y numero de cartucho) y el journal»; F23: journal con `spec_hash`, `risk_hash` |
| `MASTER_PLAN.md` §H.2, fila de los tres relojes | «F28: exportar tabla de transiciones DST del horizonte… F33: pre-vuelo compara offset real con la tabla y aborta» |
| `docs/adr/0030-…:18-20` | «F29 (MQL5) refleja las mismas primitivas con los mismos nombres»; «El contrato Python↔MQL5 sigue cubriendo parámetros y casos (ADR-0001), no reglas» |
| `docs/adr/0071-…:146` (§7, «Hechos para el conector (F33)») | «una orden del EA va con uno de los dos» (FOK/IOC) |
| `mql5/README.md` | «Ejecucion en MetaTrader 5 (fase 6). Include/Botsito/Params.mqh se GENERA desde knowledge/spec/ (F28)…»; el árbol `mql5/{Experts,Include/Botsito,Scripts,tester}` existe con solo README |
| `docs/research/2026-09-03-del-corpus-al-bot.html:483` (instantánea) | «El plan previo eligió un núcleo Python con adaptador al paquete `MetaTrader5`… Esta investigación recomienda que la ejecución final sea un EA MQL5 nativo», con cuatro razones (las 2.000 peticiones y `OnTick`, el Strategy Tester con ticks reales, el VPS sin puente, la equivalencia) |
| `docs/nocturno/BRECHA-EN-VIVO.md:47-49` y `:62-66` (2026-10-01, inventario) | «el plan no prevé un puente Python en vivo sino un Expert Advisor en MQL5 con el dominio reescrito»; su decisión 1: un EA «que solo ejecuta y recibe las decisiones de Python… exige un puente en vivo que el plan no tiene y que choca con el límite de peticiones» |
| `tools/mql5/MedirDemoFTMO.mq5:759` | la guarda de DEMO: `if((ENUM_ACCOUNT_TRADE_MODE)AccountInfoInteger(ACCOUNT_TRADE_MODE) != ACCOUNT_TRADE_MODE_DEMO)` (MQL5 ya escrito y ejecutado en la demo, ADR-0071) |

**Lectura 2 · Un adaptador en vivo en Python que reutiliza las clases.**

| Sitio | Lo que dice |
|---|---|
| `docs/adr/0067-…:17-21` (§1) | el freno vive en el puerto; «El freno no tiene IO ni reloj propio, y el adaptador real de MetaTrader usará la misma clase». Lo repite el docstring de `src/botsito/engine/freno.py:7-8` |
| `docs/adr/0068-…:61-68` (§4) | «En vivo, el adaptador de MetaTrader convierte las sesiones del símbolo (`SymbolInfoSessionTrade`) en cierres con `cierres_desde_sesiones` y las une al calendario con `unir_cierres`» (funciones Python de `src/botsito/domain/cierres.py:121` y `:169`) |
| `docs/adr/0005-…:12-13` (§1) | «El adaptador de MetaTrader 5 (terminal + cuenta) se anade en F17/F33»; y :61, la alternativa «paquete `MetaTrader5` + terminal + cuenta» para descargar datos |
| `docs/adr/0006-…:10-12` y `pyproject.toml:95-117` | la capa `botsito.mql5bridge`, hermana de `viewer`, por encima de `engine` («`validation` (F26, F30, F32) conduce el motor y el puente MQL5») |
| `src/botsito/mql5bridge/__init__.py` | paquete vacío; su docstring: «Exporta spec y casos a MQL5; lanza compilacion y tester; parsea resultados (F28, F30)». No habla de operar en vivo |
| `MASTER_PLAN.md` §H.2, fila de los tres relojes | «F17: desfase servidor-UTC en cada evento (`TimeTradeServer() - TimeGMT()`; el modulo `MetaTrader5` de Python devuelve `time` en hora de servidor)» |
| `pyproject.toml:68-79` y `:89-93` | `MetaTrader5` está prohibido en `botsito.domain` y `botsito.spec`; en ninguna otra capa. No es dependencia del proyecto (`pyproject.toml:7-10`: `pyyaml`, `tzdata`), y ningún fichero de `src/` lo importa (Grep `MetaTrader5` en `src/`: 0) |

**Qué haría falta enmendar en cada caso (la letra que contradice, nada más):**
- Si la capa es el **EA de MQL5**: ADR-0067 §1 («el adaptador real de MetaTrader usará la misma
  clase»: el EA no puede usar una clase Python; sería un puerto de `FrenoPeticiones`) y ADR-0068 §4
  («el adaptador de MetaTrader convierte… con `cierres_desde_sesiones` y… `unir_cierres`»: lo
  haría el EA con su puerto de esas dos funciones). ADR-0005 §1 dice «adaptador» sin lenguaje: no
  contradice. MASTER_PLAN §A (F31 «EA») y §H no contradicen. ADR-0081 no dice dónde vive en vivo
  (solo `:141`, «el pre-vuelo de la demo lo vuelve a leer»).
- Si la capa es un **adaptador Python**: contradicen MASTER_PLAN §A F31
  (`feature/F31-mql5-expert-advisor`, «EA, ordenes idempotentes, veto de riesgo, journal») y §H
  («MQL5: … verificacion de `ACCOUNT_MARGIN_MODE` al arrancar; journal con flush y hash
  encadenado; veto de riesgo con parametros propios»), cuyo cuerpo no se toca (NOTA del
  2026-10-10): se enmendarían en la NOTA nueva. ADR-0001 (`mql5/` es «ejecucion»), ADR-0071 §7
  («una orden del EA») y `mql5/README.md` («Ejecucion en MetaTrader 5») tendrían recuadro o nota.
  La docstring de `mql5bridge` («Exporta spec y casos… (F28, F30)») no cubre operar en vivo: es
  código, fuera de esta rama. El contrato de capas permitiría un adaptador en `mql5bridge`
  (por encima de `engine`, puede importar `engine.freno` y `domain.cierres`), sin tocar
  `pyproject.toml`; añadir el paquete `MetaTrader5` sería una dependencia nueva.
- **En las dos**, ADR-0067 §1 cuenta RN-030 entre «las reglas de la estrategia (RN-002, RN-004,
  RN-006, RN-014, RN-015, RN-030 y RN-035)»; D3 la pone en el veto de la firma, de la capa. No es
  una contradicción de lugar, pero sí de nombre: lo señalo para que lo decidas.

**Qué del código de hoy se reutiliza tal cual o se reescribe:**

| Pieza | Dónde | Qué es | Adaptador Python | EA de MQL5 |
|---|---|---|---|---|
| Freno | `src/botsito/engine/freno.py` (`LimitesFreno` :51, `FrenoPeticiones` :83) | estado puro; importa solo `logging`, `collections`, `dataclasses`, `datetime.date` (:32-36) | tal cual (ADR-0067 §1) | se reescribe |
| Cierres | `src/botsito/domain/cierres.py` (`ventana_prohibida_por_cierre` :86, `cierres_desde_sesiones` :121, `unir_cierres` :169) | dominio puro; importa solo `collections.abc` y `dataclasses` (:18-19) | tal cual (ADR-0068 §4) | se reescribe |
| Calendario | `src/botsito/engine/calendario_cierres.py` (lee `knowledge/cuentas/cierres/<perfil>.yaml`, ADR-0068 §4) | lector Python | tal cual | lo sustituye el calendario generado (D5) |
| Límite del lote | `src/botsito/engine/broker.py` `margen_requerido` :148, `lote_que_cabe` :161, `limitar_lote` :186; lo llama `_lote_final` en `engine/primitivas_broker.py:527` | funciones puras con `Decimal` | `limitar_lote` y `margen_requerido` tal cual; `_lote_final` lee `ctx.broker` simulado, se reescribe contra la cuenta real | se reescribe |
| Veto de la firma | RN-029..RN-032 en `knowledge/spec/strategy_spec.yaml:2138-2380`, ejecutadas por el intérprete del motor (`engine/`, ADR-0030) | reglas de la spec | el intérprete es el del motor | F29 (dominio en MQL5), ADR-0030 §3 |

Fuera de las dos: ningún módulo de `src/` habla hoy con un terminal (Grep `MetaTrader5` en `src/`:
0; `mql5bridge` vacío).

**Para D3, lo que lee cada regla del veto de la firma** (`knowledge/spec/strategy_spec.yaml` y la
categoría de cada parámetro en `knowledge/spec/parametros.yaml`):

| Regla | Parámetros | Hechos | ¿Cumple D3? |
|---|---|---|---|
| RN-029 (`:2138`) | `firma_perdida_diaria_max`, `firma_base_perdida_diaria`, `firma_magnitud_vigilada`, `saldo_inicial_cuenta`, `reloj_dia_riesgo`, `firma_margen_seguridad`: todos `prop_firm` | acumulador `perdida_dia_firma`, `detenido_por_tope` | sí |
| RN-030 (`:2197`) | los de RN-029 más `firma_perdida_total_max`, `firma_perdida_total_arrastra`, `firma_cierre_al_tope`: todos `prop_firm` | los dos acumuladores y `operacion_abierta` (una posición) | sí |
| RN-031 (`:2256`) | `firma_perdida_total_max`, `saldo_inicial_cuenta`, `firma_perdida_total_arrastra`, `firma_magnitud_vigilada`, `firma_margen_seguridad`: `prop_firm` | `perdida_total_firma`, `detenido_por_tope_total` | sí |
| RN-032 (`:2302`) | los de la firma **más `riesgo_por_operacion` y `base_calculo_riesgo`, los dos de categoría `estrategia`** | `no_cabe_la_operacion` con `riesgo: riesgo_por_operacion` | **no**: lee dos parámetros de categoría estrategia. Por D3 se queda fuera de la capa y espera a F26 |

Y el lote del riesgo, RN-011 (`strategy_spec.yaml:1419`): `lotaje_base`, `riesgo_por_operacion`,
`base_calculo_riesgo`, `stop_fraccion_caja`… de categoría estrategia: de la estrategia, como dice
D3. Los dos parámetros de ADR-0081 que la capa usaría, `lote_margen_libre_fraccion` y
`lote_si_no_cabe`, son de `ejecucion`.

### c) MASTER_PLAN §A: las filas que toca la rama, y la NOTA nueva

- F28 (`MASTER_PLAN.md:112`): «Params.mqh y fixtures generados» (dep. F11, F14). Adelanta la parte
  de firma, bróker y ejecución, y el calendario (D5); la de estrategia espera a F26.
- F31 (`:115`): «EA, ordenes idempotentes, veto de riesgo, journal» (dep. F29, F30). Adelanta
  órdenes idempotentes, veto de la firma (sin RN-032), journal y reconciliación; lo que decide
  operaciones espera.
- F33 (`:118`): «Demo, pre-vuelo, runbooks» (dep. F17, F31). Adelanta el pre-vuelo.
- La NOTA del 2026-10-10 está en `MASTER_PLAN.md:3-8`. Lo que lee un test de MASTER_PLAN:
  `tests/unit/test_hoja_de_ruta.py:232-235` (`_funcionalidades`) parte el texto por la PRIMERA
  aparición de la cadena «`## A ·`» (en cualquier sitio, no solo a principio de línea) y toma las
  filas `| Fnn |` hasta el siguiente `\n## `. Una NOTA arriba no rompe nada si no contiene la
  cadena «`## A ·`». Los demás tests que nombran MASTER_PLAN (`tests/unit/test_tree.py:74`, que
  exige que exista; `test_kit.py:328`, `test_spec.py:175` y `tests/contract/test_kit_particiones.py:1`,
  solo en comentarios) no leen su texto. No se crean números F nuevos.

### d) PROJECT_STATE: la condición de salida de cada línea

Criterio de `docs/state/README.md:58-75` («Que sale de PROJECT_STATE, y con que criterio»).
**Niega por defecto.** La hoja de ruta no cuenta para (b); las «Candidatas a ambiguedad sin
abrir» no están en el criterio y se quedan. Las líneas son las de `PROJECT_STATE.md` en esta rama
(las mismas que en `main`); los bytes llevan el salto de línea. El texto entero de los heredados y
de las deudas en mayúsculas está en `docs/state/HISTORIA.md` (Archivo 1, `:536-617` y `:684-727`),
y se comparó entero, no truncado. Medido por tres lecturas en paralelo y comprobado después por la
sesión en cada línea que sale.

**Lo que sale (9 líneas, 1.489 bytes):**

| Línea | Texto (inicio) | Bytes | Condición | Evidencia |
|---|---|---|---|---|
| 79 | «34. Ticks: el deslizamiento y el swap, las ejecuciones 2 y 3 (A).» | 68 | (b) | entero en la entrada A, `PROJECT_STATE.md:48`: «las ejecuciones 2 y 3 de MedirDemoFTMO … Miden A-28, el nivel de ADR-0057 §2, deslizamientos, swaps y la comisión». Lo que tenía de más el texto entero (`HISTORIA.md:726`) ya se recortó con orden del consultor en `trabajo/hoja-de-ruta` (`HISTORIA.md:7941-7951`) y en `trabajo/entrada-enero` (`HISTORIA.md:9174`). Sale `HER:34` de A.1 (`HOJA-DE-RUTA.md:282`) y «heredado 34, partes b y c» de su «Qué es» (`:284`) |
| 126 | «`maxTP` ES EL PRECIO DE CIERRE DE LAS GANADORAS…» | 88 | (d) | literal en `docs/adr/0037-…md:96-99`: «`maxTP` es el PRECIO DE CIERRE de las ganadoras, no la excursión favorable máxima … `maxTP` == `avgClosePrice` en las 17 filas». Y su consecuencia la cerró A-33 (RESUELTA, ADR-0073) y lo que queda vive en A-56 |
| 130 | «CUARTA APARICION DEL PUNTO CIEGO DEL DETECTOR…» | 96 | (a) | texto entero en `HISTORIA.md:560`: «NO mira `ambiguedades.yaml` y NO mira los `supersede` de EVIDENCIA … TIENE RAMA PROPIA». Pagada por la guardia G1, `stable/F37b-guardias-citas` (fe37973): `src/botsito/validation/citas_supersedidas.py:3-6`, «En todo fichero bajo knowledge/spec/, un id ev-* supersedido solo puede aparecer … que nombra su sustituto» (y `ambiguedades.yaml` está bajo `knowledge/spec/`). La recencia como eje sigue viva en la línea 129, que se queda |
| 131 | «LA PRIMERA MEDIDA DE A-18 SALE DEL MATERIAL, NO DE LA SESION, Y SE REPITE SOBRE MAYO…» | 125 | (a) | la repetición sobre mayo está hecha: `docs/adr/0040-…md:26-31`, la tabla agosto/abril/mayo («mayo \| 5 \| 4 \| `MAYO-DEV.md` §2»); y A-18 está RESUELTA (ADR-0073; `ambiguedades.yaml:374`) |
| 151-152 | «`data aggregate` con una ventana fuera del dataset devuelve solo cabeceras … F14 debe tratar la ventana vacia como error del caso.» | 175 | (a) | el AVISO está en `src/botsito/cli.py:2864`; F14 excluye el caso con su motivo: `src/botsito/cases/ventanas.py:137-142` (`Excluido(…, "ventana … fuera del dataset …")`), con test en `tests/unit/test_kit.py:558`. Matiz: «excluido con motivo» y no «error» |
| 156 | «F11: las reglas de `strategy_spec.yaml` son PROSA … lo cierra F12 (validacion semantica).» | 151 | (a) | `stable/F12` (77c7501): `docs/validation/F12-spec-semantic-validator.md:167-168`, «reglas vigentes con forma ejecutable y ninguna en prosa» (ADR-0019) |
| 162 | «knowledge/cases/holdout/{1,2,3}/ → tres particiones reservadas; cada una se abre una sola vez…» | 576 | (d) | literal en `knowledge/cases/holdout/README.md:1` («No se lee desde ningun sitio salvo la puerta `botsito.cases.holdout` (ADR-0033); la guarda de tests lo vigila»), `:3-9` (la tabla de particiones; «Un holdout abierto queda quemado»), `:11-40` (qué es abrirlo, quién lo autoriza, PREREGISTRO, la autorización por partición) y `CLAUDE.md` «Que se puede mirar y que no», puntos 2 y 3 (`kit build`/`kit check` declaran las velas que leen). Lo único que solo está aquí es el nombre `tests/conftest.py` («la guarda de tests», en el README) |
| 169 | «Umbrales pre-registrados no se relajan tras ver resultados. · Un holdout abierto queda quemado (…)» | 210 | (d) | `knowledge/cases/holdout/README.md:29-30` («Un umbral no se relaja despues de ver el resultado: para eso se pre-registra») y `:9` («Un holdout abierto queda quemado»); qué es abrir, `:11` (ADR-0021); la declaración, `CLAUDE.md` «Toda exposicion se declara en `docs/validation/HOLDOUT-EXPOSICIONES.md` el mismo dia, siempre (ADR-0021 §4)» |

**Lo que se queda, con el motivo:**

*Pendientes heredados* (`:69-80`):
- 2 (106 B): la línea corta está en `CLAUDE.md` «Marzo de 2026 esta RECIBIDO» y en
  `docs/runbooks/ENTRADA-MARZO.md:94-95`, pero el texto entero (`HISTORIA.md:684`) lleva más
  (`visto_el` con la fecha del backtest y su commit; la confirmación como CONFIRM de F09 sobre el
  paquete, «sin sus palabras, no vale»; que es para fidelidad-2/3), que no vive en otro sitio. Y
  `ENTRADA-MARZO.md:32` remite a «Next Action 2 y 12».
- 6, 7, 8, 9 (FEBRERO; JUNIO Y LOS ONCE DÍAS; EL BRIEF DE SEPTIEMBRE; RE-DESCARGAR UN MES): no
  viven en otro sitio y no están hechos (para el 9, `src/botsito/cases/ventanas.py:276` sigue
  fallando con «dos datasets cubren el mismo dia»).
- **10** (81 B), frente a A: A-28 sí está en A (`:48`), pero **el grabador de spread y ticks (F17)
  no está ni en A ni en V ni en un runbook**: se queda.
- 12: `ENTRADA-MARZO.md:205` y `:229` cubren `libros.yaml` y el control por velas, pero no
  «Febrero no se toca ni se descarga» ni su relación con el 2; y `:32` remite aquí.
- **25** (229 B), frente a A y V: V (`:56`) solo nombra A-35 entre las «en parte»; el runbook
  `ACTIVAR-A35-A44.md:192` cubre lo que pasa al fijar A-35, pero no la nota de R3.1 (98 y 97 de 104),
  que solo está en un informe (`CORRIDA-CONSTRUCCION.md:1407`). No es (a): R3.1 fue diagnóstico
  («No se mueven: A-35 y A-44 siguen «en parte»», `CORRIDA-CONSTRUCCION.md:289-290`). Se queda.
- 27: la «maximum capital allocation rule» y el asterisco de «USD/LOT*» solo viven aquí
  (`FTMO-REGLAS.md:309-310`, sin respuesta).
- **30** (310 B), frente a V: el runbook `ACTIVAR-A35-A44.md:184-195` cubre la medida, pero no la
  cláusula de A-43 del texto entero ni la nota de R3.1 (`CORRIDA-CONSTRUCCION.md:674`); y
  `CORRIDA-CONSTRUCCION.md:483`: «HER:30 y HER:35 siguen apuntando a
  CABLEADO-SIMULADOR-LINEA-BASE.txt hasta que A-35 y A-44 tengan valor». Se queda.
- **35** (307 B), frente a V: V solo nombra A-44; `ACTIVAR-A35-A44.md:76-95` y `:194` cubren la
  magnitud y la medida, pero no «el siguiente bloqueo del bot después de A-35», la nota de
  RN-036/ADR-0077 ni la de R3.1. Se queda.

*Technical Debt* (`:107-156`): se quedan todas salvo las seis de arriba. Las que más se acercan a
salir y por qué no:
- 107-113 (las del visor y `arnes.dias_de_mercado`): nuevas de VISOR-CONSTRUCCION §4.3 o
  CORRIDA-CONSTRUCCION, sin arreglo.
- 115-119: abiertas (sin rama que las pague; `cases/visto.py:14` sigue comprobando por nombre).
- **Las deudas en mayúsculas del 2026-09-17 al 2026-09-25, una por una:**
  - 120 GRAMÁTICA DEL KIT (09-25, ADR-0047): `src/botsito/cases/kappa.py:3` sigue con «La unidad de
    acuerdo es (caso, sesion)». Abierta.
  - 121 `cherry-pick` Y `rebase` (09-25): `CLAUDE.md` «El trabajo entra por commits y merges» dice
    la regla y que la guardia los bloquea, pero no que la garantía de fondo es la CI ni que Aleks,
    en su terminal, no tiene la guardia. Duda, luego se queda.
  - 122 `v5_criterio.py` SOLO CAJAS DE VENTA (09-23): `scripts/v5_criterio.py:148-155`, sin cambio.
  - 123 NADA COMPRUEBA EL CUERPO DE UN INFORME CERRADO (09-22): `CLAUDE.md` «Regimenes de cambio»
    remite aquí («Nada lo comprueba mecanicamente todavia (Technical Debt)»).
  - 124 OANDA Y DUKASCOPY (09-21): A-16 sigue ABIERTA; ADR-0069 deja viva «la parte de la serie».
  - 125 EL FRACTAL 5/120 (09-21): ningún ADR lo trata.
  - 126 `maxTP`: **sale** (arriba).
  - 127 LA GUARDIA DE `cobertura_material` (09-21): espera la decisión sobre qué es un paquete
    ciego; junio no está en `knowledge/cases/meses_reservados.yaml`.
  - 128 EL `no_trade` POR AUSENCIA (09-21): ningún ADR lo decide; `CORRIDA-CONSTRUCCION.md:1071`
    la cita como deuda viva.
  - 129 `fecha_grabacion` (09-21): nada ordena por ella; ADR-0037 «no se declara ninguna regla de
    recencia».
  - 130 CUARTA APARICIÓN: **sale** (arriba).
  - 131 A-18 SOBRE MAYO: **sale** (arriba).
  - 133 `idealTP` (09-21): casi entero en ADR-0037 (`:61`, `:85-87`, `:166-168`), que dice «Queda
    anotado como deuda».
  - 134 BUSCAR EN EL CORPUS ANTES DE REDACTAR (09-21): pedía un campo en «LA PROXIMA AMBIGUEDAD QUE
    SE ABRA» (`HISTORIA.md:565`); no existe en `cases/ambiguedades.py:32-49`. Abierta.
  - 135 EL DÍA QUE UN CAMINO GUARDE MATERIAL (09-21): el «añadir el camino a `CARPETAS_RESERVADAS`
    … en el MISMO commit» solo vive aquí.
  - 136 `lectura_de_velas` LEE EL `config.yaml` DE HOY (09-21): `cli.py:1481-1482` la llama sin
    `config=`. Abierta.
  - 137 DOS DÍAS SIN PARTICIÓN (09-20) y 138 UNA PREGUNTA ABRE N PARTICIONES (09-21): están en
    ADR-0035 y ADR-0033/0036 (un ADR no cuenta para (b)) y **la entrada G (`:42`) no los contiene:
    remite a «las condiciones previas que hoy viven en Technical Debt»**; si salieran, G quedaría
    apuntando al vacío. Se quedan. Lo mismo la 132 (F26 y la diferencia 3,00/3,75).
  - 139 EL FALLBACK DE `leer_fichero` (09-21): `cases/holdout.py:331` sin cambio.
  - 140 UN TOKEN NO PUEDE DECLARAR QUIÉN LO PRODUCE (09-20): `spec/modelo.py:1002` sin cambio.
  - 141 UNA `pregunta` PUEDE NOMBRAR UN INSTANTE SIN SU ITEM (09-20): ninguna guardia lo cruza.
  - 142 TERCERA APARICIÓN y 143 TEMAS HERMANOS (09-20 y 09-17):
    `evidence/contradicciones.py:47-49` agrupa aún por tema idéntico.
  - 144 LA VÍA DE PROPUESTA NO ADMITE `supersede` (09-17): `CLAUDE.md` lo dice, pero no «Hay que
    elegir…» (`HISTORIA.md:576`).
  - 145 UN CONFIRM SOBRE UN ITEM SUPERSEDIDO (09-17): `cli.py:2050-2051` no mira si el item vive.
- 146, 148, 149, 150, 153-155: solo en parte en otro sitio (ADR-0007, ADR-0008, ADR-0003,
  `RITUAL.md:355-356`), y lo que falta no vive en ninguna parte.
- **147, la copia de seguridad**: abierta (`HOJA-DE-RUTA.md:309-314`, A.4, la cita por su texto).
  Se queda, así que A.4 no cambia.

*Reglas vivas* (`:162-185`; la 167 la sustituye la rama):
- 163 (INMUTABLES): está repartida entre `CLAUDE.md` «Regimenes de cambio», ADR-0005, ADR-0007 y
  ADR-0008, no entera en un sitio. Duda, luego se queda.
- 166, «Regimenes de cambio de knowledge/. · Pureza de domain/. · Parametros no se optimizan
  contra resultados.»: «Pureza de domain/.» está en `CLAUDE.md` («`src/botsito/domain/` → sin IO,
  sin reloj, sin MetaTrader»), pero las otras dos no viven en otro sitio, y sacar solo un trozo
  reescribiría la línea. Se queda entera.
- 168 (la firma y el tipo de cuenta) y 170-171 (LF y UTF-8): no viven enteras en otro sitio.
- 175-177 (las tres decisiones del 2026-09-04): las alternativas y la parte de Bot v2 solo viven
  aquí.
- **178, la decisión del 2026-09-25 frente a ADR-0050**: ADR-0050 lleva el fondo (`:88-93`,
  `firma_huso_corte` en el perfil y el test de las medianoches; `:123-128`, la guardia sin cifra no
  impide correr; `:83-86`, la duplicación declarada), pero deja ABIERTAS al consultor justo las dos
  cosas que la 178 cierra: «Si el consultor prefiere que la ausencia de cifra impida correr, es
  cambiar una línea» (`:126-127`) y «Fundirlos … queda para el consultor» (`:85-86`). La
  ratificación «al validar» no está en ADR-0050 ni en ningún ADR posterior. Se queda.
- 181-185 (Known Issues): «no por línea» y lo de citar las dos fuentes no está en `CLAUDE.md`; la
  aceptación de 32 bits no vive en otro sitio (y su cifra «353 items» está vieja, sin reescribirla).

### e) Texto de la Next Action repetido en la hoja de ruta o en un runbook (propuesta; no se edita)

| Entrada | Texto | Dónde vive | Bytes en PS | Qué falta allí |
|---|---|---|---|---|
| N | el calendario cubre hasta el 7-10-2026, se renueva por condición, (1) hacia atrás si una simulación lo pide, (2) antes del tiempo real con SymbolInfoSessionTrade o el procedimiento del jueves, y sin una de las dos la rama no se cierra | `docs/runbooks/RENOVAR-CIERRES.md:9-27`, entero salvo la fecha | 684 | «cubre hasta el 7-10-2026» (lo dice `cubre` del yaml del perfil) y la cita a `stable/F36s-renovar-cierres`. Esta rama cambia N de todos modos (D6: R6a.1 y R6a.5 cumplen la condición 2) |
| A | ejecuciones 2 y 3 de la demo | `docs/runbooks/DEMO-FTMO.md:83-89` (fechas y el script 1.1) | 760 | `MargenAlcanza` y FTMO-P-D1 §3, la medida de ADR-0081 §4, y el calendario de noticias opcional: NO está entero |
| B, C, D, K | la guardia | `HOJA-DE-RUTA.md` G.1 los resume, no los copia; la hoja no cuenta para (b) | — | no aplica |

Para las demás entradas (F, Y, T, U, G, I, J, H, Q, V, L, M) no he encontrado su texto entero en
un runbook; la hoja de ruta las resume con sus Refs, y no cuenta para (b).

### f) Bytes por sección, antes y después

`PROJECT_STATE.md` medido con un guion de la carpeta de trabajo que trocea por `## `/`### `.

| Sección | `main` (24.391) | Rama hoy | Previsión |
|---|---|---|---|
| Cabecera + Current Branch + Current Feature | 134 + 24 + 231 | 134 + 49 + 359 | igual (el cierre la reescribe) |
| Stable Main State, Last Stable Commit, Tests | 583 + 183 + 226 | igual | igual |
| Next Action | 7.242 | igual | igual (no se toca) |
| Pendientes heredados | 1.987 | igual | 1.919 (−68, el 34) |
| Known Ambiguities (con las candidatas) | 2.380 | igual | igual |
| Technical Debt | 7.718 | igual | 7.083 (−635) |
| Reglas vivas (la cabecera y sus cuatro subsecciones) | 3.375 | igual | 2.746 (−786 de la 162 y la 169; +157 de la regla nueva: 218 bytes frente a 61) |
| Completed Features + Change Log | 308 | igual | igual |
| **Total** | **24.391** | **24.544** | **23.212** |

**La previsión no baja de 21.500**: con lo que el criterio deja salir, PROJECT_STATE queda hacia
23.200, unos 2.700 bytes por encima de 20.500. Lo que más haría falta, de mayor a menor, va en la
decisión 6.

## El encargo frente al repo (auditor-encargo)

El subagente `auditor-encargo` comprobó 34 afirmaciones del encargo: 24 CORRECTAS, 9 con MATIZ y
1 INCORRECTA; y 11 cosas que el repo pide y el encargo no dice. Lo que cambia algo:

| # | Afirmación | Veredicto | Evidencia | Qué hago |
|---|---|---|---|---|
| 21 | «El veto de la firma (RN-029 a RN-032) cumple la condición, porque solo lee cuenta y registro» | **INCORRECTA para RN-032** | `strategy_spec.yaml:2302-2352`: RN-032 lee `riesgo_por_operacion` y `base_calculo_riesgo`, de categoría `estrategia` (`parametros.yaml`). RN-029, RN-030 y RN-031 solo leen `prop_firm` | el encargo lo prevé («esa se queda fuera y se dice»): decisión 1 |
| 22 | D3/D5: la capa lee parámetros «de firma, bróker y ejecución» | MATIZ | el registro tiene cinco categorías (`estrategia`, `prop_firm`, `ejecucion`, `instrumento`, `broker`); sin `instrumento` (`instrumento_lote_paso`, `instrumento_lote_minimo`…) no se limita ni se redondea un lote | decisión 2 |
| 23 | De ADR-0081, «la capa recibe un lote y lo limita; no lo calcula» | MATIZ | ADR-0081 §3: el límite lo gobierna `lote_si_no_cabe` (`ejecucion`, DEFAULT_AMBIGUOUS bajo A-57); con `no_operar` el límite decide no operar | decisión 3 |
| 17 | §H.2 «habla de dos hashes» | CORRECTA, con matiz | «`Params.mqh` (estrategia+instrumento+ejecucion) y `Risk.mqh` (prop_firm) con dos hashes en el journal»: el hash de `Params.mqh` mezcla la estrategia, que espera a F26 | decisión 5 |
| 29 | «journal y reconciliación» (D1, R6a.3) | MATIZ | en el plan «reconciliación» es F34, demo↔backtest (`MASTER_PLAN.md:119`); lo de F31 es reconstruir la jornada al arrancar, con el test «reinicio a media jornada» (§H.2) | decisión 4 |
| 28 | R6a.7: `ACCOUNT_MARGIN_MODE` en el pre-vuelo (§H, §H.2) | MATIZ | §H pone la verificación de `ACCOUNT_MARGIN_MODE` «al arrancar» en F29 y F31, no en F33 | la llevo a R6a.7 como dice D9 y lo digo en el ADR |
| 12, 13 | ADR-0006/mql5bridge y §H.2 como apoyo de la lectura Python | MATIZ | `mql5bridge` es el puente de exportación y tester (F28, F30); §H.2 solo dice cómo devuelve la hora el módulo `MetaTrader5` | recogido en b) tal cual |
| 8 | research html hacia :635 | MATIZ | `:635` dice «antes del EA», no «MQL5»; y `:483` recomienda «que la ejecución final sea un EA MQL5 nativo» frente al adaptador `MetaTrader5` | añadido a b) |
| 6 | R6.1 atribuye la regla a «§A» | CORRECTA, con matiz | la regla está en §0 (`MASTER_PLAN.md:27`); §A solo la refleja en F30 | se corrige al reescribir R6.1 |

Lo que el repo pide y el encargo no dice:
- **`ids-inexistentes`**: ADR-0082 ya se citaba sin existir, y el primer `make check` de la rama
  salió en rojo (5 fallos, todos `id citado que no existe: … ADR-0082`). Arreglado como en
  `trabajo/entrada-enero`: un bloque en el encargo y otro en este informe; el id salió de
  PROJECT_STATE. Los bloques salen en el commit que crea el ADR.
- **`docs/nocturno/BRECHA-EN-VIVO.md` §1** (2026-10-01) ya planteó D4: «el plan no prevé un puente
  Python en vivo sino un Expert Advisor en MQL5» (`:47-49`), y su decisión 1 (`:62-66`). Añadido a b).
- **El perfil de cuenta** (`knowledge/cuentas/ftmo-2step-swing-100k.yaml`, ADR-0050 §3) es donde
  vive el tope de volumen y el apalancamiento (ADR-0081: «la spec NO lee `firma_volumen_max_lotes`»);
  D5 solo nombra parámetros y calendario: decisión 2.
- **A-57** en R6a.6 (por `lote_si_no_cabe`): decisión 3.
- **La deuda de las citas de relleno de RN-029..RN-032** (`PROJECT_STATE.md:117`) toca a R6a.4: la
  nombro en su «Qué es».
- **El test «reinicio a media jornada»** de F31 (§H.2): va en R6a.3.
- **Nada de recuentos** en la hoja de ruta ni en las reglas vivas (`tests/contract/test_documentos_vivos.py`).
- **R0 no tiene entrada para esta rama** (R0.1 y R0.2 están HECHAS; el encargo no pide R0.3): no
  añado ninguna.
- **R7.1 conserva `NA:N`** en sus Refs y la condición 2 en «Depende de»: al reescribir su «Depende
  de» (R6.1 y R6a), la condición 2 pasa a R6a.1 y R6a.5, que llevan `NA:N`; dejo `NA:N` también en
  las Refs de R7.1, que siguen siendo verdad.

## Lo que no pude medir

- Nada de MT5: cómo se compila por línea de órdenes, el Strategy Tester o `SymbolInfoSessionTrade`
  (D7 lo deja a la fase 0 de R6a.1).
- Si el paquete `MetaTrader5` de Python corre fuera de Windows: no está en el repo y no lo afirmo.
- La protección de rama de GitHub (deuda 153-155): no consultada.

## Exposiciones

Ninguna. No se leyó material del trader, ni holdout, ni libros; ni se ejecutó el arnés ni el visor.

## Lo que necesito que decidas

0. **D4, dónde vive la capa.** Opciones: (a) el EA de MQL5 (MASTER_PLAN §A F31 y §H; ADR-0001;
   research `:483`; BRECHA-EN-VIVO §1): se enmiendan con recuadro ADR-0067 §1 y ADR-0068 §4, y
   `engine/freno.py`, `domain/cierres.py` y `limitar_lote` se portan a MQL5. (b) Un adaptador en
   vivo en Python, en `mql5bridge` (ADR-0067 §1, ADR-0068 §4, ADR-0005 §1): reutiliza esas piezas
   tal cual, añade la dependencia `MetaTrader5`, y lo enmendado es MASTER_PLAN §A F31 y §H (en la
   NOTA), ADR-0001, ADR-0071 §7 y `mql5/README.md`. Sin recomendación: el encargo pide hechos y no
   opinión en b).
1. **RN-032 fuera de la capa.** Lee `riesgo_por_operacion` y `base_calculo_riesgo`, de categoría
   estrategia. Opciones: (a) R6a.4 lleva el veto de RN-029, RN-030 y RN-031, y RN-032 espera a F26;
   el ADR lo dice como consecuencia de D3. (b) Se cambia RN-032 para que no lea parámetros de
   estrategia. Recomiendo (a): es lo que D3 manda («esa se queda fuera y se dice»). Coste de (b):
   tocar la spec, que esta rama no puede.
2. **La categoría `instrumento` y el perfil de cuenta.** D3 permite «firma, bróker y ejecución»;
   limitar un lote necesita `instrumento_lote_paso` y `instrumento_lote_minimo`, y el tope de
   volumen y el apalancamiento viven en el perfil de cuenta, no en `parametros.yaml`. Opciones:
   (a) D3 y D5 dicen «firma, bróker, instrumento y ejecución, y el perfil de cuenta». (b) Se deja
   como está. Recomiendo (a): ninguna de esas entradas es un hecho de la estrategia. Coste de (b):
   R6a.6 no se puede hacer sin saltarse D3.
3. **`lote_si_no_cabe = no_operar` (A-57).** Con esa opción, cuando el lote no cabe la capa no
   envía la orden. Opciones: (a) es un veto, como el rechazo por margen del bróker: la capa no
   decide qué operar, solo se niega a enviar lo que no cabe; R6a.6 lleva `ID:A-57`. (b) Esa opción
   es de la estrategia y espera a F26: la capa solo limita (`limitar`). Recomiendo (a): D3 ya dice que
   la capa «veta», y el veto lee solo cuenta, símbolo y un parámetro de ejecución. Coste de (b):
   mientras A-57 siga abierta, la capa tiene una opción del registro que no sabe cumplir.
4. **«Reconciliación» en D1 y R6a.3.** Opciones: (a) en la capa quiere decir reconstruir el estado
   al arrancar (órdenes, posiciones y journal contra la cuenta, con el test «reinicio a media
   jornada» de §H.2), y la reconciliación demo↔backtest sigue en F34. (b) Incluye ya lo de F34.
   Recomiendo (a): F34 compara con el backtest, que es de la estrategia. Coste de (b): R6a.3 dependería
   de F32.
5. **El hash de lo generado (D5).** §H.2 define dos hashes: `Params.mqh` (estrategia + instrumento
   + ejecución) y `Risk.mqh` (prop_firm). Opciones: (a) el ADR lo dice como está y añade que lo que
   la capa recibe antes de F26 (sin estrategia) lleva su propio hash, distinto de los dos del plan,
   que se fija en R6a.2. (b) Se redefine ya el par de hashes del plan. Recomiendo (a): no decide nada
   que R6a.2 vaya a medir. Coste de (b): enmendar §H.2 sin haber diseñado el fichero.
6. **PROJECT_STATE no llega a 20.500 con el criterio de hoy.** Previsión: 23.212 bytes. Lo que más
   ayudaría, de mayor a menor:
   (a) llevar a sus runbooks, literal desde HISTORIA, lo que les falta a los heredados 25, 30 y 35
   (`docs/runbooks/ACTIVAR-A35-A44.md`: las notas de R3.1, la cláusula de A-43, «el siguiente
   bloqueo del bot después de A-35» y RN-036) y a los 2 y 12 (`docs/runbooks/ENTRADA-MARZO.md`:
   `visto_el`, el CONFIRM de F09, «Febrero no se toca» y su `:32`, que remite a la Next Action), y
   que salgan por (b): −1.066 bytes, ampliando el contrato a esos dos runbooks;
   (b) un recuadro en ADR-0050 que registre la ratificación del 2026-09-25 (las dos cosas que
   dejaba al consultor), y la línea 178 sale por (d): −492, dentro del contrato;
   (c) en la orden de cierre, N reducida a lo que no está en `RENOVAR-CIERRES.md` (la fecha de
   `cubre` y el puntero): unos −500; N cambia de todos modos (D6);
   (d) llevar a `CLAUDE.md` la regla 163 (INMUTABLES, con `reemplaza_a` y «una extracción activa por
   vídeo») y los Known Issues del trailer: unos −400, pero toca `CLAUDE.md`.
   Con (a)+(b)+(c) quedaría hacia 21.150; con (d), hacia 20.750; y el cierre reescribe Current
   Feature y Stable Main State, que pueden bajar unos 300 más. Recomiendo (a) y (b) en esta rama y
   (c) en la orden de cierre, y que el objetivo pase a 21.500. Coste de mantener 20.500: (d), que
   cambia `CLAUDE.md`, y aun así queda justo.

Espero tu respuesta a la PARADA.

## Respuesta del consultor a la PARADA (2026-10-18)

Dada por Aleks (consultor) el 2026-10-18. Copiada tal cual:

> Respuesta del consultor a la PARADA de la fase 0 de trabajo/plataforma-adelantada (2026-10-18). Cópiala tal cual al informe y aplícala punto por punto (skill fase-cero). Las letras (a)-(d) de tu decisión 6 las llamo «opción 6a», «opción 6b»…, y (a)-(d) a secas son las condiciones de docs/state/README.md.
>
> 0. D4: (a), el EA de MQL5.
>    Porqué:
>    - El bot final es un EA (F29-F31; ADR-0001:20-21, «exige dos implementaciones (Python y MQL5) que lean la misma fuente»), así que una capa en Python habría que tirarla al llegar F29.
>    - research :483 da cuatro razones, escritas para FundedNext, y cada una se cita como es:
>      · El tope de 2.000 peticiones vale igual en FTMO (FTMO-REGLAS.md:60, R13; firma_mensajes_dia_max = 2000 en el perfil). Un bucle de Python que sondea gasta presupuesto; el EA reacciona a OnTick.
>      · El Strategy Tester con ticks reales y el VPS sin puente no tienen cita de FTMO en el repo: el ADR los da como razones de research, sin afirmarlos para FTMO, y los mide R6a.1 (D7).
>      · La cuarta, la equivalencia entre dos implementaciones (E6), es la de F30, y sigue valiendo.
>    - ADR-0082 responde por su nombre a la pregunta 1 de BRECHA-EN-VIVO.md §1 (:62-66):
>      · se descarta el EA que recibe las decisiones de Python, porque exige un puente en vivo que choca con el tope de peticiones;
>      · el dominio se porta a MQL5 en F29, después de F26;
>      · antes de F26 solo va la capa de ADR-0082.
>    Lo que se hace:
>    - ADR-0082 lo decide como D4, con estas razones y sus citas.
>    - Recuadro en ADR-0067 §1: «el adaptador real de MetaTrader usará la misma clase» queda enmendado por ADR-0082. El EA porta FrenoPeticiones a MQL5, y engine/freno.py sigue siendo la referencia y el freno del simulador. En el mismo recuadro: RN-030 es del veto de la firma (ADR-0082 D3); la frase de §1 sigue siendo cierta en lo que dice (llama a acciones del bróker), pero no la hace regla de la estrategia.
>    - Recuadro en ADR-0068 §4: en vivo, el EA porta cierres_desde_sesiones y unir_cierres; las funciones de domain/cierres.py siguen siendo la referencia.
>    - Los dos recuadros van en el mismo commit que crea ADR-0082, después del frontmatter y antes de «## Estado» (test_adr.py). La fila de cada uno en docs/adr/README.md pasa a «ACTIVE (… ; enmendado por ADR-0082)».
>    - El docstring de engine/freno.py:7-8 dice lo mismo que ADR-0067 §1. Es código y esta rama no lo toca: va como deuda de una línea en Technical Debt, que apunta a PLATAFORMA-ADELANTADA.md, y la paga R6a.4.
>    - Cada pieza portada se prueba contra los mismos casos que sus tests de Python (D4 del encargo). Eso no sustituye a F30.
> 1. RN-032: (a). R6a.4 lleva RN-029, RN-030 y RN-031, y RN-032 espera a F26. El ADR lo escribe como consecuencia de D3, con la cita strategy_spec.yaml:2302-2356. Porqué: es lo que D3 manda, y la opción (b) tocaría la spec.
> 2. Categoría instrumento y perfil de cuenta: (a). D3 y D5 dicen «parámetros de firma, bróker, instrumento y ejecución, y el perfil de cuenta (knowledge/cuentas/)». Porqué: ninguno es un hecho de la estrategia, y sin ellos R6a.6 no se puede hacer.
> 3. lote_si_no_cabe: (a). Hoy su valor es limitar (ADR-0081, DEFAULT_AMBIGUOUS bajo A-57). Su opción no_operar es un veto: la capa no elige qué operar, se niega a enviar lo que no cabe, leyendo solo cuenta, símbolo y un parámetro de ejecución. R6a.6 cumple las dos opciones, con el valor que deje A-57 en la sesión 5, y lleva ID:A-57.
> 4. Reconciliación: (a). En la capa quiere decir reconstruir el estado al arrancar (órdenes, posiciones y journal contra la cuenta), con el test «reinicio a media jornada» de §H.2 en R6a.3. La reconciliación demo-backtest sigue en F34. Porqué: el backtest es de la estrategia.
> 5. El hash: (a). El ADR describe los dos hashes de §H.2 tal como están, y lo que la capa recibe antes de F26 lleva su propio hash, que se fija en R6a.2. Porqué: no se decide ahora lo que R6a.2 va a medir.
> 6. PROJECT_STATE: las opciones 6a y 6b en esta rama, la 6c en la orden de cierre, y la 6d no, porque CLAUDE.md queda fuera de esta rama. El objetivo pasa a 21.500 bytes al final de la rama.
>    - Opción 6a. El contrato se amplía a docs/runbooks/ACTIVAR-A35-A44.md y docs/runbooks/ENTRADA-MARZO.md.
>      · Para cada heredado (2, 12, 25, 30 y 35), lo que se lleva al runbook es el texto de la línea VIVA de PROJECT_STATE, con sus añadidos (los «· R3.1: …» incluidos), más lo que esa línea remite a HISTORIA. Se toma del último Archivo que la trae, se cita de dónde sale, y se lleva como instrucción operativa de ese runbook, no como pegote de archivo.
>      · La línea sale por la condición (b) solo si después el runbook la contiene entera.
>      · Si algo de esa versión no puede ir al runbook, la línea se queda: por ejemplo, un hecho de marzo que ENTRADA-MARZO.md no decía, una fecha de días reservados o lo que el trader backtesteó. Niega por defecto.
>      · El diff de ENTRADA-MARZO.md lo revisa el revisor, en su alcance, antes del commit: ni fechas de días reservados ni hechos de marzo nuevos.
>      · Por cada heredado que salga, su HER:n sale de la hoja de ruta en el mismo commit (R4.1 para 25, 30 y 35; R5.3 para 2 y 12; A.3 para 2) y se sustituye por el puntero al runbook.
>    - Opción 6b. Recuadro en ADR-0050 que registra la ratificación del 2026-09-25 tal como está en PROJECT_STATE.md:177, citando esa línea y su fecha; después la línea sale por la condición (d).
>    - Si con 6a y 6b la rama no baja de 21.500, no pares: dilo en el informe con la cifra exacta.
>
> Lo demás de la fase 0 queda aceptado tal cual:
> - ACCOUNT_MARGIN_MODE va en R6a.7 y en el arranque de R6a.1, y el ADR cita §H.
> - La deuda de las citas de relleno de RN-029 a RN-032 se nombra en R6a.4.
> - El bloque ids-inexistentes sale en el commit que crea ADR-0082.
> - No hay entrada R0.3.
> - NA:N se queda en las Refs de R7.1.
>
> Sigue con las fases 1 a 4 y el cierre del encargo. Rama lista para revisión, NO cerrada.

## La respuesta, aplicada punto por punto

| Punto | Qué se hizo | Dónde |
|---|---|---|
| 0 · D4: el EA de MQL5 | ADR-0082 §4 lo decide con las razones y las citas de la respuesta (ADR-0001:20-21; research `:483`, cada razón como es; `FTMO-REGLAS.md:60`, R13, y `firma_mensajes_dia_max` en el perfil, `knowledge/cuentas/ftmo-2step-swing-100k.yaml:327`, valor 2000; BRECHA-EN-VIVO §1, `:62-66`). Recuadro en ADR-0067 §1 (el EA porta `FrenoPeticiones`; RN-030 es del veto de la firma) y en ADR-0068 §4 (el EA porta `cierres_desde_sesiones` y `unir_cierres`), los dos después del frontmatter y antes de «## Estado»; sus filas del índice, «…; enmendado por ADR-0082 en §1/§4». La deuda del docstring de `engine/freno.py:7-8`, en Technical Debt, la paga R6a.4. «Cada pieza portada se prueba contra los mismos casos que sus tests de Python», en ADR-0082 §4 y en las entradas de R6a | ADR-0082; ADR-0067; ADR-0068; `docs/adr/README.md`; PROJECT_STATE; HOJA-DE-RUTA R6a |
| 1 · RN-032 fuera | ADR-0082 §3, con la cita `strategy_spec.yaml:2302-2356`; R6a.4 lleva RN-029, RN-030 y RN-031 en sus Refs | ADR-0082; R6a.4 |
| 2 · `instrumento` y el perfil | D3 y D5 dicen «los parámetros de firma, bróker, instrumento y ejecución, y el perfil de cuenta (`knowledge/cuentas/`)» | ADR-0082 §3 y §6; R6a.2 |
| 3 · `lote_si_no_cabe` | ADR-0082 §3: `no_operar` es un veto; la capa cumple las dos opciones con el valor que deje A-57; R6a.6 lleva `ID:A-57` | ADR-0082; R6a.6 |
| 4 · Reconciliación | ADR-0082 §5: reconstruir el estado al arrancar, con el test «reinicio a media jornada» en R6a.3; demo↔backtest sigue en F34 | ADR-0082; R6a.3 |
| 5 · El hash | ADR-0082 §6: los dos hashes de §H.2 como están; lo que la capa recibe antes de F26 lleva su propio hash, que fija R6a.2 | ADR-0082; R6a.2 |
| 6 · PROJECT_STATE | 6a: contrato ampliado (commit de esta fase) a `ACTIVAR-A35-A44.md` y `ENTRADA-MARZO.md`; los heredados 12, 25, 30 y 35 salen por (b); **el 2 se queda** (revisor, b1: el runbook no puede llevar entera la versión que remitía a HISTORIA). 6b: recuadro en ADR-0050 §4 y la 178 sale por (d). 6c queda para la orden de cierre. 6d no. **No baja de 21.500: queda en 22.517 bytes** (abajo, «Tamaño final») | contrato.yaml; los dos runbooks; ADR-0050; HISTORIA |
| Aceptado tal cual | `ACCOUNT_MARGIN_MODE` en R6a.7 y en el arranque de R6a.1, con §H citado (ADR-0082 §10); la deuda de las citas de relleno, nombrada en R6a.4; el bloque `ids-inexistentes` sale en el commit que crea ADR-0082; sin R0.3; `NA:N` sigue en las Refs de R7.1 | ADR-0082; HOJA-DE-RUTA |

**Una cita de la respuesta que no casa, dicha con su nombre:** la opción 6b cita la decisión del
2026-09-25 como `PROJECT_STATE.md:177`; en el árbol de la rama era la línea **178** (la 177 era la
decisión del 2026-09-04 sobre las inferencias en `evidence/`). Se aplicó a la del 2026-09-25, que es
la que la respuesta describe, y el recuadro de ADR-0050 y el bloque de HISTORIA lo dicen.

## Fase 1 · ADR-0082

`docs/adr/0082-la-capa-de-mt5-que-nunca-decide-una-operacion-va-antes-de-f26.md` (0082 era el
siguiente libre: `docs/adr/` acababa en 0081), con el formato de `0000-template.md`, el título que
nombra la condición de D3 y su fila en `docs/adr/README.md` con las enmiendas entre paréntesis.
Lleva D1 a D9 con su autor y su fecha (§1 D1, §2 D2, §3 D3, §4 D4 de la respuesta, §6 D5, §7 D6, §8
D7, §9 D8, §10 D9), y lo que la respuesta añade (§3: la categoría `instrumento`, el perfil, RN-032 y
`lote_si_no_cabe`; §5: la reconciliación; §6: el hash). Enmienda MASTER_PLAN §0 y la regla de
PROJECT_STATE (D2, con la frase nueva literal), ADR-0067 §1 y ADR-0068 §4.

## Fase 2 · Los sitios de la regla y del plan, antes y después

| Sitio | Antes | Después |
|---|---|---|
| `PROJECT_STATE.md`, «Things That Must Not Be Changed» | «- La validacion de fidelidad (F26) precede a cualquier MQL5.» | «- La validación de fidelidad (F26) precede a todo lo que decida operaciones en vivo (F29, F30 y lo de F31-F32 que dependa de ellos); la capa de plataforma de ADR-0082, que nunca decide una operación, puede ir antes.» La vieja, literal, en HISTORIA («# Regla viva SUSTITUIDA · sale de PROJECT_STATE.md en trabajo/plataforma-adelantada (2026-10-18)»), con ADR-0082 como evidencia |
| `docs/plan/MASTER_PLAN.md` | la NOTA del 2026-10-10 y nada más arriba; §0 dice «Validacion de fidelidad (F26) antes de cualquier MQL5.» | una NOTA nueva (2026-10-18, esta rama, ADR-0082) debajo de la del 2026-10-10: el principio de §0 queda enmendado con la frase de arriba; lo que adelanta de F28, F31 y F33; y que su orden vive en el tramo R6a. El cuerpo no se toca. La NOTA no contiene «`## A ·`» ni empieza ninguna línea por `\| F` |
| `docs/plan/HOJA-DE-RUTA.md`, R6.1 «Depende de» | «R5.5 (fidelidad antes de MQL5, MASTER_PLAN §A).» | «F29, F30 y lo de F31-F32 que decide operaciones dependen de R5.5 (ADR-0082, que enmienda MASTER_PLAN §0); lo demás de F31 vive en R6a.» |

Ningún otro sitio vivo lo decía (fase 0, a). Las instantáneas congeladas (`MASTER_PLAN.html`, el
informe de investigación), los informes cerrados y HISTORIA no se tocan.

## Fase 3 · La hoja de ruta

**Desviación pedida del paso 4 de `entregar-rama`** (las entradas de la hoja no se tocan en la
rama): esta rama las toca porque el encargo lo pide (fase 3 y opción 6a de la respuesta).

- **Tramo nuevo** «## R6a · La capa de MT5 que no decide operaciones (ADR-0082)», entre R5 y R6,
  con su cabecera (en paralelo a R2-R5, en los huecos de espera, sin quitarle turno a F) y siete
  entradas, R6a.1 a R6a.7, una por rama de D9, con los cuatro campos y sus Refs. Ninguna HECHA.
  Refs: `ID:ADR-0082` en todas; `F:F17`, `F:F28`, `F:F31`, `F:F33`; `ID:ADR-0057`, `ID:ADR-0067`,
  `ID:ADR-0068`, `ID:ADR-0081`; `ID:A-28`, `ID:A-54`, `ID:A-55`, `ID:A-57`; `ID:RN-029`,
  `ID:RN-030`, `ID:RN-031` (no RN-032); `NA:N` en R6a.1 y R6a.5.
- **R6.1**: su «Depende de», como arriba.
- **R7.1**: su «Qué es» deja de decir que el pre-vuelo va aquí («el pre-vuelo va en R6a.7»), y su
  «Depende de» pasa a «R6.1 y R6a (la lectura de SymbolInfoSessionTrade de la condición 2 de NA:N
  llega en R6a.1 y R6a.5)». `NA:N` sigue en sus Refs.
- **Por los heredados que salen**: A.1 sin `HER:34` y sin «heredado 34, partes b y c»; R4.1 sin
  `HER:25`, `HER:30` ni `HER:35`, con `ID:RN-004`, `ID:RN-020` y el puntero a
  `docs/runbooks/ACTIVAR-A35-A44.md` §5.1; R5.3 sin `HER:12`, con el puntero al paso 0 y al paso d
  de `ENTRADA-MARZO.md`. `HER:2` sigue en R5.3 y en A.3, porque el heredado 2 se queda.
- **Un contrato futuro puede nombrar «R6a» como tramo**: `scripts/contrato_rama.py`,
  `tramos_de_la_hoja` (`:123-131`) toma de cada `## ` el título entero y lo que va antes de « · »;
  medido sobre la hoja de la rama, `R6a` está en el conjunto y `problemas_de_tramo('R6a', …)` da
  `[]`.
- `tests/unit/test_hoja_de_ruta.py` pasa con el tramo nuevo («Comprobaciones», abajo).

## Fase 4 · Lo que salió de PROJECT_STATE, y adónde

Todo al final de `docs/state/HISTORIA.md` (solo se amplía), literal, con su condición y su
evidencia, en bloques con el formato de `docs/state/README.md`:

| Línea (fase 0) | Qué | Condición | Bloque de HISTORIA |
|---|---|---|---|
| 75 | heredado 12 | (b), `ENTRADA-MARZO.md` paso 0 (opción 6a) | «# Pendiente heredado SALE · 12 · …» |
| 76 | heredado 25 | (b), `ACTIVAR-A35-A44.md` §5.1 (opción 6a) | «# Pendiente heredado SALE · 25 · …» |
| 78 | heredado 30 | (b), `ACTIVAR-A35-A44.md` §5.1 (opción 6a) | «# Pendiente heredado SALE · 30 · …» |
| 79 | heredado 34 | (b), entrada A | «# Pendiente heredado SALE · 34 · …» |
| 80 | heredado 35 | (b), `ACTIVAR-A35-A44.md` §5.1 (opción 6a) | «# Pendiente heredado SALE · 35 · …» |
| 130, 131, 151-152, 156 | CUARTA APARICIÓN; A-18 SOBRE MAYO; `data aggregate`; F11 PROSA | (a) | «# Technical Debt PAGADA · …» |
| 126 | `maxTP` | (d) | «# Technical Debt RECLASIFICADA · …» |
| 167 | la regla de F26 | (c), ADR-0082 | «# Regla viva SUSTITUIDA · …» |
| 169 | umbrales y holdout quemado | (d) | el mismo bloque |
| 178 | la decisión del 2026-09-25 | (d), recuadro de ADR-0050 §4 (opción 6b) | el mismo bloque |

**Opción 6a, cómo se llevó cada heredado a su runbook.** El texto es el de la línea viva (con sus
«· R3.1: …» y sus otras notas), más lo que recortaba con «…»: para el 12, el 25, el 30 y el 35, el
texto entero del Archivo 1 (el último que no lo recorta), y para el 25 sin la frase de A-21 (la
línea viva ya no la trae: A-21 está RESUELTA, ADR-0076). Cada runbook dice de dónde sale.
- **El heredado 2 se queda en PROJECT_STATE** (revisor, b1, aplicado negando por defecto). La versión
  que su línea remite a HISTORIA (el texto entero del Archivo 1, `HISTORIA.md:684`, y el bloque «#
  Pendiente heredado SALE · 2 (en parte)» del 2026-10-10) empieza por «MARZO INTERRUMPE LO QUE HAYA
  EN VUELO CUANDO LLEGUE. El trader confirmo el 2026-09-21 que no habia visto febrero NI marzo, y
  backtestea MARZO…»: eso es lo que el trader backtesteó, que la respuesta dice que no va al
  runbook, y entonces la línea se queda. Su bloque de salida se quitó de la cola de HISTORIA antes
  del commit (no había entrado en ninguno), y `HER:2` sigue en R5.3 y A.3.
- `docs/runbooks/ENTRADA-MARZO.md`, paso 0: deja de remitir a «Next Action 2 y 12»; dice que lo que
  falta sigue en el heredado 2 y, como instrucción, lo que falta de la entrega (`vistos.yaml` con
  `visto_el` y `cobertura_material`, material del camino de fidelidad para `fidelidad-2` y
  `fidelidad-3`; el CONFIRM de F09, «sin sus palabras, no vale»; el paso a) y el heredado 12 entero
  (`libros.yaml` por el método de velas con control; Aleks no abre el fichero antes, **salvo la
  columna de fechas del paso a**, ADR-0046 §6a, que el runbook ya decía; febrero no se toca ni se
  descarga; complementa la entrega). **No entra ningún hecho de marzo nuevo ni ninguna fecha de
  días reservados** (el revisor lo comprobó sobre el diff: solo trae las fechas 2026-10-18,
  2026-10-12 y 2026-10-10).
- `docs/runbooks/ACTIVAR-A35-A44.md`, §5.1 nuevo («RN-004 tras A-35 y RN-020 tras A-44: lo que
  queda, y cómo se mide»): los tres, como puntos operativos de §5. Al 25 se le añade entre
  paréntesis que el productor ya está construido desde `trabajo/preparar-a35-a44` («escribirlo es
  fijar su valor, §1»), porque el runbook lo dice en su cabecera y la línea viva decía «se escribe
  el productor»; y la nota de R3.1 del 30 nombra su informe (`CORRIDA-CONSTRUCCION.md` §3.4), que en
  PROJECT_STATE iba implícito.

Lo que entra en PROJECT_STATE en esta rama: la regla nueva (218 bytes frente a 61), la deuda del
docstring de `engine/freno.py` y Current Branch y Current Feature de la rama.

## Tamaño final de PROJECT_STATE

**22.517 bytes** (`main`: 24.391; tope del test: 25.000; objetivo de la respuesta: 21.500). **No
baja de 21.500: le sobran 1.017 bytes.** Con 6a y 6b llegaba a 21.834; el revisor devolvió dos
líneas que salían sin poder (el heredado 2, b1, 107 bytes; la regla 162, a1, 576 bytes: el nombre
`tests/conftest.py` solo vivía en PROJECT_STATE, y `knowledge/cases/holdout/README.md` está fuera
del contrato). La respuesta dice no parar y decirlo. Lo que queda para el cierre: la opción 6c (N,
unos −500) y la reescritura de Current Feature y Stable Main State; y, si el consultor quiere que
la 162 salga, que una rama con `knowledge/` en su contrato escriba `tests/conftest.py` en el README
del holdout.

| Sección | Rama al abrir | Final |
|---|---|---|
| Cabecera, Current Branch, Current Feature | 134 + 49 + 359 | igual |
| Stable Main State, Last Stable Commit, Tests | 583 + 183 + 226 | igual |
| Next Action | 7.242 | igual (no se toca) |
| Pendientes heredados | 1.987 | 955 |
| Known Ambiguities | 2.380 | igual |
| Technical Debt | 7.718 | 7.268 (−635 de lo que sale; +185 de la deuda del docstring) |
| Reglas vivas | 3.375 | 2.830 |
| Completed Features + Change Log | 308 | igual |
| **Total** | **24.544** | **22.517** |

## Propuestas sobre la Next Action (para la orden de cierre)

No se ha tocado la Next Action. Lo que cambie (F, N y las ramas de R6a en los huecos) va en el
commit del contrato con la orden de cierre. La tabla de la fase 0 e) sigue valiendo: N, casi entera
en `RENOVAR-CIERRES.md` (684 bytes; falta la fecha de `cubre`), es la opción 6c; y la condición 2
de N queda cumplida por diseño en R6a.1 y R6a.5 (ADR-0082 D6).

## Lo que queda para el consultor (del revisor)

- **ADR-0050 §5 y ADR-0053 llaman «de la ESTRATEGIA» a los frenos de RN-029 a RN-032** (revisor,
  b2): `docs/adr/0050-…md`, «`firma_margen_seguridad` es un freno de la ESTRATEGIA (RN-029 a
  RN-032…)», y `docs/adr/0053-…md`, «los frenos de la estrategia disparan ANTES del límite». Choca
  con D3 (RN-029, RN-030 y RN-031 son del veto de la firma), no con D4. Es la misma contradicción de
  nombre que la respuesta resolvió con recuadro en ADR-0067; aquí no se pusieron recuadros, porque
  la respuesta solo los pide en ADR-0067 y ADR-0068. Decídelo en la orden de cierre.

## El encargo, punto por punto

| Punto del encargo | Hecho | Dónde |
|---|---|---|
| Verificar la base antes de abrir | sí | «Apertura» |
| Abrir con `abrir-rama`: encargo, contrato (tramo R0, rutas) y Archivo 37 | sí | ea60aaf |
| Fase 0 a)-f), PARADA en b) | sí | 9192552; «Fase 0» |
| Fase 1: ADR-0082 con D1-D9, D4 de la respuesta, título con la condición, fila del índice, recuadros | sí | «Fase 1» |
| Fase 2: la regla de PROJECT_STATE, la NOTA de MASTER_PLAN, otros sitios vivos (ninguno) | sí | «Fase 2» |
| Fase 3: el tramo R6a, R6.1, R7.1, «R6a» como tramo, la desviación declarada | sí | «Fase 3» |
| Fase 4: lo que sale, literal en HISTORIA; lo que se queda, sin tocar | sí | «Fase 4» |
| PROJECT_STATE en 20.500 (21.500 tras la respuesta) | **no**: 22.517, dicho como manda la respuesta | «Tamaño final» |
| No cambia motor, spec, knowledge, parámetros, guardias, hooks, Makefile, src, tests, mql5, tools | sí | `git diff main --name-only`: solo documentos de `rutas_permitidas` |
| La Next Action no se edita | sí | el diff de PROJECT_STATE no toca la sección |
| `make check` con SELLO y los cinco tests | sí | «Comprobaciones» |
| CI de Linux | no hace falta: la rama no toca hooks, rutas, código ni plataforma | — |
| Revisor, con su alcance, pegado al final | sí | «Informe del revisor» |

## Comprobaciones

- `uv run pytest tests/unit/test_project_state.py tests/unit/test_historia.py
  tests/unit/test_hoja_de_ruta.py tests/unit/test_adr.py tests/unit/test_kit.py
  tests/contract/test_documentos_vivos.py -q`: todo en verde, sobre el árbol final.
- `make check > make-check.log 2>&1` sobre el árbol estadiado del commit de las fases 1-4: el
  resultado, en el mensaje de ese commit y en el resumen a Aleks (el log no se commitea).
- Tamaño final exacto de `PROJECT_STATE.md`: **22.517 bytes**.

## Estado

Rama lista para revisión, NO cerrada.

## Informe del revisor

Subagente `revisor`, sobre el árbol estadiado de las fases 1-4 (antes de los arreglos), 2026-10-18.
Tal cual, salvo su lista de comandos ejecutados, que va resumida en una línea; sus números de línea
son los de ese árbol, antes de los arreglos.

### Lo que se hizo con cada hallazgo

| # | Gravedad | Qué se hizo |
|---|---|---|
| b1 | bloquea | El heredado 2 vuelve a PROJECT_STATE (negar por defecto); su bloque de salida sale de la cola de HISTORIA, que no había entrado en ningún commit; `HER:2` vuelve a R5.3 y A.3; el paso 0 de ENTRADA-MARZO dice que lo que falta sigue en el heredado 2 |
| a1 | importa | La regla 162 vuelve a PROJECT_STATE: `tests/conftest.py` solo vivía allí, y el README del holdout está en `knowledge/`, fuera del contrato. Su punto sale del bloque «Regla viva SUSTITUIDA» de la cola de HISTORIA |
| a2 | importa | ADR-0082, «Por que elegimos» y «Por que descartamos» (2): RN-032 la metía el veto de la firma enumerado «RN-029 a RN-032» de la tercera consecuencia de D3, no la lista de D1 |
| a3, b4 | importa | «Comprobaciones», con los tests y `make check`; «(abajo)» apunta ahí |
| b2 | importa | En «Lo que queda para el consultor»: no se ponen recuadros que la respuesta no pide |
| b3 | importa | «El encargo, punto por punto» |
| b5 | menor | ADR-0082 §6: «con sus hashes en el journal», como D5; el hash propio de antes de F26 es el punto 5 de la respuesta |

### El informe, tal cual

## Informe del revisor · trabajo/plataforma-adelantada · 2026-10-18
La rama aún no está lista: hay 1 hallazgo que bloquea (el heredado 2) y 6 que importan. Los siete puntos del alcance, en corto:

1. **ADR-0082 y D1 a D9:** cumple. Lleva D1 a D9 con autor y fecha, D4 y los puntos 1-5 de la respuesta, y D3 está escrita como condición (`0082…md:37-45`). Pero dos frases del ADR atribuyen RN-032 a la lista de D1, y la lista no la nombra (a3, importa). Hay además una errata de número en D5 (b5, menor).
2. **«antes de cualquier MQL5»:** cumple. Solo queda en la cita de la NOTA (`MASTER_PLAN.md:11`), en el cuerpo de MASTER_PLAN, que no se toca (`:37`), en ADR-0082, en las instantáneas HTML, en el encargo y en el informe.
3. **Recuadros por D4:** cumple. ADR-0067 §1 y ADR-0068 §4 llevan su recuadro, y ADR-0005 §1 no contradice D4. Lo que sí queda es otra cosa: ADR-0050 y ADR-0053 llaman «de la estrategia» a los frenos de RN-029 a RN-032. Choca con D3, no con D4, y no está dicho (b2, importa).
4. **Lo que sale de PROJECT_STATE:** cada línea quitada está byte a byte en HISTORIA, y lo que se queda no cambia de texto. La línea 162 sale por la condición (d) aunque el propio informe admite que una parte solo vivía allí (a1, importa).
5. **R6a en test_hoja_de_ruta:** cumple. El test pasa y ninguna entrada de R6a está HECHA.
6. **ENTRADA-MARZO.md y ACTIVAR-A35-A44.md:** el diff no trae fechas de días reservados ni hechos de marzo nuevos. Los heredados 12, 25, 30 y 35 están enteros. El heredado 2 no lo está, y aun así sale de PROJECT_STATE (b1, bloquea).
7. **La cita «PROJECT_STATE.md:177»:** bien tratada. Se aplicó a la línea 178, y lo dicen el informe y HISTORIA.

### Eje (a) · Reglas de la casa
Resumen: 0 bloquea, 3 importa, 0 menor.

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| a1 | importa | La línea 162 de PROJECT_STATE (las particiones del holdout) sale por (d), «vive literal en otro sitio». No vive literal: el informe reconoce que el nombre `tests/conftest.py` («la guarda de `tests/conftest.py` vigila a cualquier llamante durante los tests») solo estaba en PROJECT_STATE. El README del holdout dice solo «la guarda de tests lo vigila». El bloque de HISTORIA dice «vive literal» y calla esa salvedad. El criterio dice: «Si no vive en ningun otro sitio, se queda» y «Niega por defecto». | `docs/validation/PLATAFORMA-ADELANTADA.md:184`: «Lo único que solo está aquí es el nombre `tests/conftest.py`»; `docs/state/HISTORIA.md:10444`: «Condicion (d): vive literal en `knowledge/cases/holdout/README.md:1`…»; `knowledge/cases/holdout/README.md:1`; `docs/state/README.md:68-71` |
| a2 | importa | Hay dos sitios donde ADR-0082 dice algo que su fuente no sostiene. Primero: «una lista… metió RN-032» y «la condición… ya decidió una de la lista: RN-032». La lista de D1 no nombra el veto de la firma. RN-032 entró por la tercera consecuencia de D3 («El veto de la firma (RN-029 a RN-032)… Entra en la capa aunque D1 no lo nombre»). | `docs/adr/0082-…md:178-179` y `:185-186`; encargo `docs/encargos/trabajo-plataforma-adelantada.md:15` (D1, sin veto de la firma) y `:20` |
| a3 | importa | El informe se presenta como terminado salvo el revisor, pero no recoge el resultado de `make check` ni los cinco tests que pide el cierre. Además, `:531` remite a una comprobación «(abajo)» que no existe. Sí hay un `make-check.log` con SELLO, pero no se puede atar al árbol estadiado de ahora (ver «Lo que no pude comprobar»). | `PLATAFORMA-ADELANTADA.md:531` «pasa con el tramo nuevo (abajo)», `:602-604`; un Grep de «make check\|SELLO\|test_kit» solo da `:161`, `:182` y `:334` |

Comprobado sin hallazgos:
- **Contrato:** `contrato_rama.py` da «CONTRATO: 14 ficheros dentro del contrato… 3 comprobaciones», con exit 0. `git diff main --name-only` da 14 ficheros, todos en `rutas_permitidas`, y nada en `src/`, `tests/`, `mql5/`, `tools/`, `knowledge/`, `scripts/`, `.claude/` ni `Makefile`.
- **make-check.log:** «2677 passed», «SELLO: make check en verde sobre el arbol c91f8f3da5039b43195fde63f49dcdfef9f6036e», «PICO DE MEMORIA de make check: 296 MiB».
- **Trailers `Fuente:`:** ningún commit ni cambio estadiado toca `knowledge/`.
- **Holdout:** el informe declara «Exposiciones: Ninguna». Yo no abrí material del trader. Sí leí `knowledge/cases/holdout/README.md`, que es documentación y no una partición.
- **Regímenes:** sin cambios en evidence, feedback, manifests, transcripciones, fotogramas ni `libros.yaml`. HISTORIA solo crece (0 líneas quitadas frente a `main`).
- **Ambigüedades:** no se tocan.
- **ADR:** el `## Estado` de 0082 empieza por `ACTIVE`, y los de 0050, 0067 y 0068 no cambian. Pasan `test_adr.py`, `test_project_state.py`, `test_historia.py` y `test_hoja_de_ruta.py`.
- **Informes cerrados:** la rama solo cambia `PLATAFORMA-ADELANTADA.md`.
- **Citas:** ninguna `cita` nueva en la spec.
- **Lo que sale de PROJECT_STATE, byte a byte:** las 17 líneas quitadas están literales al final de HISTORIA (`:10368-10448`). Lo que se queda solo cambia en Current Branch, Current Feature, la regla sustituida, el «Archivo 36→37» y la deuda nueva del docstring.
- **Evidencias de las salidas:** comprobadas `cli.py:2864`, `ventanas.py:137-142`, `test_kit.py:558`, `F12…md:167-168`, `citas_supersedidas.py:3-6`, `ADR-0040:26-31`, `ADR-0037:96-99`, A-18 RESUELTA y la entrada A `:48` del heredado 34.
- **Citas de ADR-0082 contra su fuente:** `ADR-0001:20-21`, `FTMO-REGLAS.md:60`, `ftmo…yaml:327` (2.000), `research.html:483`, `BRECHA-EN-VIVO.md:62-66`, `MedirDemoFTMO.mq5:759`, `strategy_spec.yaml:1419` y `:2302` (RN-032 lee `riesgo_por_operacion` y `base_calculo_riesgo`, de categoría estrategia), `freno.py:7-8`, `broker.py:148/161/186`, §H.2 «dos hashes», `RENOVAR-CIERRES.md:19`.

### Eje (b) · Encargo
Resumen: 1 bloquea, 3 importa, 1 menor. Requisitos: 22 hechos, 4 parciales, 1 no hecho.

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 1 | Verificar la base (8642b8c, padre 7d3783d, tag) | Hecho | informe `:12-21` |
| 2 | abrir-rama: encargo, contrato, Archivo 37 | Hecho | ea60aaf; HISTORIA Archivo 37 |
| 3 | Contrato: tramo R0, rutas permitidas y protegidas (+6a) | Hecho | `contrato.yaml:4-24` |
| 4 | No cambia código, spec ni guardias | Hecho | `git diff main --name-only` |
| 5 | Fase 0 a)-f) y PARADA en b) | Hecho | informe `:23-419` |
| 6 | ADR 0082 (siguiente libre), plantilla, fila del índice con enmiendas | Hecho | `docs/adr/README.md:88`; cabeceras como `0000-template.md` |
| 7 | D1 a D9 con autor y fecha, D4 de la respuesta, título con la condición de D3 | Hecho (ver a2, b5) | `0082…md:7`, `:20-154` |
| 8 | Recuadros en ADR-0067 §1 y ADR-0068 §4, y sus filas | Hecho | diff de 0067 `:23-29`, 0068 `:70-74`; README `:73-74` |
| 9 | Regla de PROJECT_STATE sustituida literal; la vieja a HISTORIA con su bloque | Hecho | diff de PS; `HISTORIA.md:10437-10442` |
| 10 | NOTA nueva en MASTER_PLAN, con el cuerpo intacto | Hecho | `MASTER_PLAN.md:9-18` |
| 11 | Otros sitios vivos alineados | Hecho (no hay ninguno) | Grep: solo `MASTER_PLAN.md:11` (cita) y `:37` (cuerpo) |
| 12 | Tramo R6a entre R5 y R6, con cabecera, R6a.1-7, Refs y ninguna HECHA | Hecho | `HOJA-DE-RUTA.md:258-333`; sin «Estado:» entre 258 y 335; test en verde |
| 13 | R6.1 «Depende de» | Hecho | `HOJA-DE-RUTA.md` R6.1 |
| 14 | R7.1 «Qué es» y «Depende de» | Hecho | diff de R7.1 |
| 15 | Que un contrato futuro pueda nombrar «R6a» | Hecho | informe `:527-530`; `contrato_rama.py:123-131` |
| 16 | Declarar la desviación del paso 4 de entregar-rama | Hecho | informe `:510-511` |
| 17 | PROJECT_STATE ≤ 20.500 (21.500 tras la respuesta) | Parcial, declarado | `wc -c` = 21834; informe `:578-581` (la respuesta permite no parar) |
| 18 | Lo que sale, a HISTORIA literal, con condición y evidencia | Hecho | comparación byte a byte: las 17 líneas, OK |
| 19 | HER:n fuera de la hoja de ruta | Hecho | diff de R4.1, R5.3, A.1 y A.3; test en verde |
| 20 | La Next Action no se edita | Hecho | el diff de PS no toca la sección |
| 21 | Respuesta 0 (deuda del docstring, piezas portadas probadas con los mismos casos) | Hecho | PS (Technical Debt, línea nueva); `0082…md:88-93` |
| 22 | Respuestas 1-5 y lo aceptado (ACCOUNT_MARGIN_MODE, citas de relleno, ids-inexistentes, sin R0.3, NA:N) | Hecho | `0082…md:47-63`, `:95-111`, `:140-151`; R6a.4, R6a.6; R7.1 Refs |
| 23 | Opción 6a: heredados 2, 12, 25, 30 y 35 enteros en los runbooks | Parcial | 12, 25, 30 y 35 enteros; el 2, no (b1) |
| 24 | Opción 6b: recuadro en ADR-0050 y salida de la línea 178 | Hecho | `0050…md:130-139`; `HISTORIA.md:10447-10448` |
| 25 | Contenido del informe pedido en el cierre | Parcial | faltan los tests, `make check` y «El encargo, punto por punto» (a3, b3) |
| 26 | `make check` con exit 0 y SELLO | Parcial / no comprobable | log con SELLO c91f8f3…; sin poder atarlo al árbol estadiado |
| 27 | Revisor pegado al final del informe | No hecho (pendiente: es este informe) | — |

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| b1 | bloquea | **Heredado 2:** sale de PROJECT_STATE sin que ENTRADA-MARZO.md contenga la versión que la línea remitía a HISTORIA. La respuesta del consultor dice: «La línea sale por la condición (b) solo si después el runbook la contiene entera» y «Si algo de esa versión no puede ir al runbook, la línea se queda: por ejemplo… lo que el trader backtesteó». El informe toma como esa versión el bloque «SALE · 2 (en parte)», que trae el texto entero. Ese texto lleva «MARZO INTERRUMPE LO QUE HAYA EN VUELO CUANDO LLEGUE. El trader confirmo el 2026-09-21 que no habia visto febrero NI marzo…», y el runbook no lo lleva. El informe deja fuera la confirmación de forma declarada, pero aun así saca la línea. «MARZO INTERRUMPE…» no aparece ni declarado. Se resuelve de una de dos formas: el heredado 2 vuelve a PROJECT_STATE (106 B) o el consultor lo acepta por escrito. | `HISTORIA.md:7897` y `:684`; `ENTRADA-MARZO.md:32-51` (el diff); informe `:563-565`: «lo que el trader confirmó el 2026-09-21 y qué backtesteó (Archivo 1) se queda en HISTORIA»; `HISTORIA.md:10374` dice «vive entero» |
| b2 | importa | **Punto 3 del alcance:** ADR-0050 §4 y ADR-0053 llaman a los frenos de RN-029 a RN-032 «de la ESTRATEGIA», y ADR-0082 D3 pone RN-029, RN-030 y RN-031 en la capa, como veto de la firma. Es la misma contradicción de nombre que el informe señaló para ADR-0067 (`:116-118`) y que el consultor resolvió con recuadro solo allí. No contradice D4, pero la rama no lo nombra. | `docs/adr/0050-…md:145-146` «`firma_margen_seguridad` es un freno de la ESTRATEGIA (RN-029 a RN-032…)»; `docs/adr/0053-…md:116` «los frenos de la estrategia disparan ANTES del límite» |
| b3 | importa | Falta en el informe la tabla «El encargo, punto por punto» de entregar-rama. «La respuesta, aplicada punto por punto» (`:469-480`) cubre solo la respuesta, no el encargo. | Grep de «punto por punto» en el informe: solo `:425` y `:469` |
| b4 | importa | El cierre del encargo pide que el informe recoja que pasan `test_project_state.py`, `test_historia.py`, `test_hoja_de_ruta.py`, `test_adr.py` y `test_kit.py`, y `make check` con SELLO. No está (lo mismo que a3, visto desde el encargo). | encargo `:61`; informe `:576-604` |
| b5 | menor | D5 dice en el encargo «con sus hashes en el journal», y en el ADR «con su hash en el journal». El cambio de número viene de mezclarlo con el punto 5 de la respuesta y no se dice. | encargo `:22`; `0082…md:105` |

Lo que la rama hace sin que el encargo lo pida, y que el informe sí justifica:
- `ID:RN-004` e `ID:RN-020` en R4.1 (informe `:524`).
- El paréntesis del productor ya construido en ACTIVAR §5.1 (informe `:567-571`).

Lo que el encargo dice que no se toca: comprobado con el diff, nada fuera del contrato.

Respuesta del consultor: las 43 líneas son idénticas en el encargo (`:79-121`) y en el informe (`:425-467`), comparadas por programa.

Punto 6a (fechas y hechos de marzo):
- Las líneas añadidas a los dos runbooks solo traen las fechas 2026-10-18, 2026-10-12 y 2026-10-10. Ninguna fecha de marzo.
- «El xlsx ya esta en el corpus (REGISTRO-MARZO.md §2, punto 1)» no es un hecho nuevo: ya lo dicen CLAUDE.md («Marzo de 2026 esta RECIBIDO») y la línea 94-95 del propio runbook.
- «Aleks no abre el fichero antes, salvo la columna de fechas del paso a (ADR-0046 §6a)» ya lo decía el runbook en `:20` y en el paso a.

Punto 7: informe `:482-485` y `HISTORIA.md:10448` dicen que era la 178 (en `main`, 177 es la decisión del 2026-09-04 y 178 la del 2026-09-25, comprobado con `git show main:PROJECT_STATE.md`). El recuadro de ADR-0050 la cita entera, con su fecha, sin número de línea.

### Lo que no pude comprobar
- **Que el SELLO de `make-check.log` (árbol c91f8f3…) sea el del árbol estadiado de ahora.** Para eso haría falta `git write-tree`, que escribe en la base de objetos. Lo que hay: el log es de las 16:59:14 y `.git/index` de las 17:24:22. Eso no prueba nada, porque `git status` también refresca el índice.
- **`test_kit.py`:** no lo ejecuté (es largo). La única evidencia es «2677 passed» en el log.
- **Si «MARZO INTERRUMPE LO QUE HAYA EN VUELO» sigue vigente** o ya lo dejó sin objeto la hoja de ruta. Es juicio del consultor, y por eso b1 se puede resolver con su aceptación por escrito.

### Comandos ejecutados
(31 comandos de lectura: git, Read, grep, sed, `uv run pytest` de los tests del alcance y dos comparaciones por programa, todos de solo lectura; la lista entera está en el informe que devolvió el subagente.)
