# PLATAFORMA-ADELANTADA · La capa de MT5 que no decide operaciones, adelantada antes de F26 (ADR-0082), y PROJECT_STATE adelgazado

Rama `trabajo/plataforma-adelantada`, abierta el 2026-10-18 desde `main` en 8642b8c (commit de
estado sobre el merge 7d3783d, tag `stable/F37t-visor-construccion`). Encargo:
`docs/encargos/trabajo-plataforma-adelantada.md`. Tramo: R0 («Lo que ordena el trabajo»; la rama
reordena la hoja de ruta y el tramo R6a aun no existe al abrirla). Modelo de la sesion: Opus,
esfuerzo medio, fijados por Aleks en su terminal antes del encargo.

```ids-inexistentes
ADR-0082 — el ADR que esta rama escribe en su fase 1; aún no existe
```

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

## Estado

EN CURSO: fase 0 entregada; PARADA en b), a la espera de la respuesta del consultor.
