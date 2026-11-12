# CAPA-GENERADA · lo que la capa de MT5 recibe del repo, generado y con su hash

Rama `trabajo/capa-generada` (hoja de ruta R6a.2, tramo R6a; ADR-0082 D5). Encargo del consultor
del 2026-11-12: `docs/encargos/trabajo-capa-generada.md`.

## Apertura (2026-11-12)

Base comprobada con git y gh antes de abrir:

- `git rev-parse main origin/main`: `893ce6f57bc40f644415785063d6b27eb9ef8977` las dos veces
  (`git rev-parse --short main` = `893ce6f5`, el sha del encargo).
- `git rev-parse "stable/F38y-laminas-motivos^{commit}"` = `git rev-parse main^1` =
  `7d3002c87026573e5c24aada940e490be5907da1`; el tag esta en origin (`git ls-remote --tags`:
  `bd7686fc… refs/tags/stable/F38y-laminas-motivos`).
- CI de `main` sobre `893ce6f5…` (check-runs): `python completed success`, run 43217308040.
- `git branch --list`: solo `main`; `git ls-remote --heads origin "fix/*"`: vacio.
- `PROJECT_STATE.md` en main: 23.899 bytes.

Exposición: cada `make check` lee el M1 entero de marzo y calienta con el de junio (Technical Debt).
El primer `make check` de la apertura se lanzó sin la fila del día y se paró a medias para
escribirla; `docs/validation/HOLDOUT-EXPOSICIONES.md` entra en `rutas_permitidas` (lo señaló el
auditor del encargo, herencia 1) y la fila del 2026-11-12 de esta rama declara las dos lecturas.

`make check` de la apertura (commit `cee851c8`): exit 0, 3443 passed, ningún `failed`, SELLO sobre el árbol `e9812162`.
`PICO DE MEMORIA de make check: 316 MiB en `test` (suma de sus procesos, memoria comprometida, Windows; el mayor proceso, 305 MiB)`

## Fase 0 (2026-11-12): inventario y medida, sin código de la capa

Todo medido en esta sesión, solo leyendo. Los guiones de medida están en la carpeta de trabajo de la
sesión, fuera del repo (leen los yaml con `yaml.safe_load` y el calendario con
`engine/calendario_cierres.py`; no escriben nada). Ningún fichero de la capa, del generador ni de
los tests se ha escrito.

### a. Qué entra en lo generado (D1)

Criterio, el de D1: entra lo que no es de categoría `estrategia` ni es un hecho de la estrategia
**y** lo lee una pieza de R6a.3 a R6a.8 según su «Qué es» (`docs/plan/HOJA-DE-RUTA.md`: R6a.3 :529,
R6a.4 :541, R6a.5 :550, R6a.6 :559, R6a.7 :569-575, R6a.8 :582). Lo que no lee ninguna pieza se
queda fuera (niega por defecto, ADR-0082:43): entra cuando la pieza que lo necesite lo lea, y se
regenera. «Reglas» es la lista `parametros:` de cada regla de `strategy_spec.yaml`. P =
`knowledge/spec/parametros.yaml:línea`; C = `knowledge/cuentas/ftmo-2step-swing-100k.yaml:línea`.

**Entran 32 nombres** (13 están en los dos ficheros y salen una vez; de la pareja de stops level
sale uno, decisión 3; `firma_huso_corte`, según la decisión 0):

| nombre | dónde | cat. | estado | valor | consumido_por | reglas | pieza (hoja) |
|---|---|---|---|---|---|---|---|
| instrumento_digitos | P:62 | instrumento | CONFIRMED | 5 | — | RN-026 | R6a.3 (:529, precios de las órdenes), R6a.7 (:571) |
| instrumento_contrato | P:78 | instrumento | CONFIRMED | "100000" | — | RN-027 | R6a.6 (:559; `limitar_lote`, engine/broker.py:188-219), R6a.7 |
| instrumento_lote_minimo | P:93 | instrumento | CONFIRMED | "0.01" | — | RN-011, RN-027 | R6a.6, R6a.7 |
| instrumento_lote_paso | P:108 | instrumento | CONFIRMED | "0.01" | — | RN-027 | R6a.6, R6a.7 |
| instrumento_stops_level | P:123 | instrumento | CONFIRMED | 0 | — | RN-026 | R6a.3, R6a.7 · sinónimo, b |
| broker_offset_base | P:140 | broker | CONFIRMED | 120 | F17, F24, F33 | RN-020 | R6a.7 (:574, «120 y `us`») |
| broker_dst | P:160 | broker | CONFIRMED | us | F17, F24, F33 | RN-020 | R6a.7 (:574) |
| reloj_dia_riesgo | P:1630 | prop_firm | CONFIRMED | civil_operativa | — | RN-020, 029, 030, 032 | R6a.4 (:541) |
| saldo_inicial_cuenta | P:1731 / C:52 | prop_firm | CONFIRMED | "100000" | F24, F33 / — | RN-029 a 032 | R6a.4, R6a.7 |
| firma | P:1755 / C:17 | prop_firm | CONFIRMED | ftmo | F33 | RN-001, 020, 028-032 | R6a.7 (perfil) |
| firma_programa | P:1770 / C:29 | prop_firm | CONFIRMED | "2-step" | F33 | — | R6a.7 (perfil) |
| firma_tipo_cuenta | P:1783 / C:40 | prop_firm | CONFIRMED | swing | F33 | — | R6a.7 (perfil) |
| firma_perdida_diaria_max | P:1799 / C:208 | prop_firm | CONFIRMED | "5" | — | RN-029, 030, 032 | R6a.4 |
| firma_perdida_total_max | P:1816 / C:234 | prop_firm | CONFIRMED | "10" | — | RN-030, 031, 032 | R6a.4 |
| firma_base_perdida_diaria | P:1831 / C:222 | prop_firm | CONFIRMED | saldo_corte_diario | — | RN-029, 030, 032 | R6a.4 |
| firma_perdida_total_arrastra | P:1845 / C:247 | prop_firm | CONFIRMED | false | — | RN-030, 031, 032 | R6a.4 |
| firma_magnitud_vigilada | P:1857 / C:256 | prop_firm | CONFIRMED | equity | — | RN-029 a 032 | R6a.4 |
| firma_cierre_al_tope | P:1870 | prop_firm | CONFIRMED | si | — | RN-030 | R6a.4 |
| firma_margen_seguridad | P:1886 | prop_firm | CONFIRMED | "0.5" | — | RN-029 a 032 | R6a.4 |
| firma_mensajes_dia_max | P:1906 / C:327 | prop_firm | CONFIRMED | 2000 | F23, F24, F31 / F24 | — | R6a.4 (freno, ADR-0067) |
| freno_peticiones_aviso | P:1923 | ejecucion | DEFAULT_AMBIGUOUS (A-54) | 1000 | ADR-0067 | — | R6a.4 |
| freno_peticiones_corte | P:1941 | ejecucion | DEFAULT_AMBIGUOUS (A-54) | 1500 | ADR-0067 | — | R6a.4 |
| freno_bucle_repeticiones | P:1959 | ejecucion | DEFAULT_AMBIGUOUS (A-54) | 5 | ADR-0067 | — | R6a.4 |
| freno_bucle_minutos | P:1976 | ejecucion | DEFAULT_AMBIGUOUS (A-54) | 1 | ADR-0067 | — | R6a.4 |
| firma_gap_margen_minutos | P:1991 / C:352 | prop_firm | CONFIRMED | 120 | ADR-0068 | — | R6a.5 (:550) |
| firma_gap_cierre_minimo_minutos | P:2008 / C:365 | prop_firm | CONFIRMED | 120 | ADR-0068 | — | R6a.5 |
| lote_si_no_cabe | P:2040 | ejecucion | CONFIRMED | limitar | ADR-0081 | RN-011 | R6a.6 (:560, nombrado) |
| lote_margen_libre_fraccion | P:2066 | ejecucion | CONFIRMED | "0.95" | ADR-0081 | RN-011 | R6a.6 |
| firma_apalancamiento | P:2100 / C:270 | prop_firm | CONFIRMED | 30 | ADR-0081, F33 / ADR-0081 | RN-011 | R6a.6, R6a.7 |
| firma_volumen_max_lotes | C:286 | prop_firm | CONFIRMED | "50" | F24 | RN-011 | R6a.6 («por volumen») |
| firma_stops_level_puntos | C:444 | prop_firm | CONFIRMED | 0 | F24 | — | sinónimo de instrumento_stops_level (b) |
| firma_huso_corte | C:63 | prop_firm | CONFIRMED | "Europe/Prague" | — | — | R6a.4 (el corte del día de la firma) · decisión 0 |

Que RN-011 (estrategia) lea `instrumento_lote_minimo`, `lote_si_no_cabe`, `lote_margen_libre_fraccion`,
`firma_apalancamiento` y `firma_volumen_max_lotes` no los saca (D1): la capa recibe un lote y lo
limita, no lo calcula (ADR-0082:50-56). `lote_si_no_cabe` es CONFIRMED hoy (P:2040), no
DEFAULT_AMBIGUOUS como decía ADR-0082:53 (A-57 se resolvió en `trabajo/activar-sesion-05`).

**Fuera, y por qué:**

| nombre | dónde | cat. | estado | consumido_por | motivo |
|---|---|---|---|---|---|
| modelo_llenado | P:184 | ejecucion | CONFIRMED | F24, F27 | del simulador (D1) |
| latencia_ms | P:200 | ejecucion | CONFIRMED | F24, F27 | del simulador (D1) |
| reloj_sesiones | P:233 | ejecucion | CONFIRMED | — | de la estrategia (D1): RN-001, 002, 035, 036 lo leen como reloj de las sesiones del trader. Sin `consumido_por`: se sostiene por su descripción, no por él (auditor, 15) |
| sesiones_primera_vela_h4 | P:262 | ejecucion | CONFIRMED | ADR-0069 | de la estrategia (D1) |
| huso_grafico | P:281 | ejecucion | CONFIRMED | ADR-0017, 0063, 0069 | de la estrategia (D1) |
| sesgo_h4_tope_velas | P:454 | ejecucion | CONFIRMED | F18 | de la estrategia (D1; F18 es el sesgo H4) |
| caja_se_fija | P:753 | ejecucion | CONFIRMED | ADR-0064, 0074 | de la estrategia (D1) |
| huso_operativa | P:212 | ejecucion | CONFIRMED | ADR-0027, 0053, 0063 | **dudoso, para ti** (D1): decisión 0 |
| cierre_pendientes | P:2022 | ejecucion | DEFAULT_AMBIGUOUS (A-55) | ADR-0068 | **dudoso, para ti** (D1): decisión 1 |
| filtro_noticias | P:1229 | prop_firm | CONFIRMED | F33 | ninguna pieza lo lee; RN-028 está DESCARTADA |
| firma_noticias_restringe | P:2086 / C:339 | prop_firm | CONFIRMED | F33 | ninguna pieza lo lee (Swing no restringe) |
| cuenta_objetivo, cuenta_pruebas | P:1699, P:1715 | prop_firm | CONFIRMED | F33; F17, F33 | ninguna pieza de R6a.3-R6a.8 los lee. La negativa fuera de DEMO de R6a.1 compara con la constante `ACCOUNT_TRADE_MODE_DEMO` de MQL5, no con el parámetro |
| firma_fases y los ocho de objetivos y días mínimos de reto, verificación y fondeada | C:76-198 | prop_firm | CONFIRMED (dos UNKNOWN) | — | ninguna pieza los lee (son del simulador de fases) |
| firma_fondeada_objetivo, firma_fondeada_dias_minimos | C:181, C:198 | prop_firm | **UNKNOWN** | — | sin valor: no se generan, y ninguna pieza los necesita |
| firma_ordenes_simultaneas_max, firma_posiciones_dia_max | C:303, C:315 | prop_firm | CONFIRMED | F24 | ninguna pieza los nombra (el freno de R6a.4 es el de peticiones) · decisión 2 |
| firma_comision_usd_por_lote, firma_comision_por_lado, firma_swap_largo_puntos, firma_swap_corto_puntos | C:382-429 | prop_firm | CONFIRMED | F24 | del simulador (costes); ninguna pieza los lee |
| firma_tamano_posicion_aviso_aplica | C:461 | prop_firm | CONFIRMED | — | ninguna pieza lo lee |
| firma_tamano_posicion_ratio_aviso | C:471 | prop_firm | **UNKNOWN** | — | sin valor: no se genera |

Ningún parámetro UNKNOWN lo necesita una pieza: no hay PARADA por D1.

### b. Una fuente por nombre (D2)

- **Nombres en los dos ficheros: 14** (firma, firma_programa, firma_tipo_cuenta, saldo_inicial_cuenta,
  firma_perdida_diaria_max, firma_perdida_total_max, firma_base_perdida_diaria,
  firma_perdida_total_arrastra, firma_magnitud_vigilada, firma_apalancamiento,
  firma_mensajes_dia_max, firma_noticias_restringe, firma_gap_margen_minutos,
  firma_gap_cierre_minimo_minutos). **Hoy no difieren en tipo, valor, opciones ni estado** (los 14
  CONFIRMED en los dos). Difieren en `unidad` tres de ellos (`firma`, `firma_perdida_diaria_max`,
  `firma_perdida_total_max`: «prop firm de destino» / «prop firm»; «capital simulado inicial» /
  «capital inicial») y en `consumido_por` varios (p. ej. saldo_inicial_cuenta: [F24, F33] / []).
  Ni `unidad` ni `consumido_por` se generan (d), así que no tienen por qué hacer fallar.
- **El test que los cruza** es `tests/unit/test_perfil_cuenta.py:106-120`
  (`test_un_nombre_que_coincide_con_parametros_yaml_lleva_el_mismo_valor`) y compara
  `(tipo, valor, opciones)`, **no el estado**: confirmado. Se amplía al estado en la fase 1.
- **Sinónimos con nombre distinto: dos parejas**, ninguna más (busqué los `instrumento_*` y los
  `firma_*` que nombran la misma magnitud):
  - `instrumento_stops_level` (P:123, instrumento, puntos, CONFIRMED, 0) y `firma_stops_level_puntos`
    (C:444, prop_firm, puntos, CONFIRMED, 0). El perfil dice «es la misma magnitud y lleva el mismo
    valor, 0» (C:453-454). **Ningún test los cruza hoy.** Decisión 3: qué nombre sale.
  - `huso_operativa` (P:212, «Europe/Madrid») y `firma_huso_corte` (C:63, «Europe/Prague»). Los
    cruza `test_el_reloj_de_corte_de_ftmo_coincide_hoy_con_el_del_trader`
    (test_perfil_cuenta.py:123-134), **por instantes** a medianoche de cada día de 2030, no por
    texto. **Aquí D2 no se puede aplicar tal cual**: sus valores son textos distintos y el generador
    fallaría siempre. Y ADR-0053 §4 (:150-156) ya decide esta pareja: «el reloj del simulador es el
    del perfil de cuenta (`firma_huso_corte`), y el cableado COMPRUEBA al arrancar que coincide con
    `huso_operativa` (…) en las medianoches de cada día del tramo». No es una pareja de sinónimos que
    se une: son dos relojes que hoy coinciden (lo señaló el auditor como INCORRECTA, 22). Decisión 0.

### c. El calendario de cierres (D3)

- `cubre` (knowledge/cuentas/cierres/ftmo-2step-swing-100k.yaml:18-23): desde el 2025-12-04 hasta el
  **2026-10-07**, en America/New_York; en instantes, [2025-12-04T05:00Z, 2026-10-08T04:00Z).
  Confirmado.
- Pautas: `semanal` del viernes 16:55 al domingo 17:05 y `diario` de 16:55 a 17:05, las dos en
  America/New_York. Extraordinarios: 3 (el 25-dic-2025, el 1-ene-2026 y el cambio de hora del
  8-mar-2026, este en Etc/GMT-2 → Etc/GMT-3), cada uno con su fuente.
- Lo que da `engine/calendario_cierres.py` sin decidir nada: `cargar_calendario(ruta)` (:184) valida
  el yaml y `DefinicionCalendario.calendario()` (:89) expande las pautas día a día en su huso (una
  semana más a cada lado de `cubre`), añade los extraordinarios y los junta con `juntar_cierres`
  (domain/cierres.py:135; no es `unir_cierres`, :169, que mezcla fuentes y busca discrepancias).
  Devuelve un `CalendarioCierres` (domain/cierres.py:48): los cierres ya juntos y en orden, y
  `cubre_desde_ms`/`cubre_hasta_ms`. Es exactamente lo que recibe hoy el predicado de Python.
- Medido sobre el calendario real: **228 cierres juntos** (180 «diario», 45 «diario + semanal», 2
  «diario + extraordinario» y 1 «diario + semanal + extraordinario» el fin de semana del 8-mar);
  218 tocan `cubre`; 48 duran 120 minutos o más; **todos sus bordes caen en segundos enteros**.
- **Lo que propongo: los instantes, no la pauta** (decisión 4). Lo generado lleva, en segundos UTC,
  `cubre` y los 228 cierres que da `calendario()`, con su fuente, tal cual. Por qué: la pauta está en
  America/New_York con su cambio de hora, y pasarla a instantes en el EA sería portar la conversión
  de husos (lógica); con los instantes, R6a.5 recibe lo mismo que el predicado de Python y solo porta
  `ventana_prohibida_por_cierre`, `cierres_desde_sesiones` y `unir_cierres`. Lo generado no filtra por
  duración (eso es del predicado). Coste: regenerar al renovar el calendario, que ya es la regla de D3.
- La corrida de la fase 3 cae fuera de `cubre` (acaba el 7-oct): no importa, porque la rama no opera.
  Lo dirá también el procedimiento.

### d. El fichero, la orden y el hash (D4 y D5)

- **Nombre:** `mql5/Include/Botsito/Capa/Generado.mqh`. Dice lo que es (no se edita a mano) y no
  choca con `Params.mqh` ni `Risk.mqh` (MASTER_PLAN.md:238 y :270, para F28).
- **La orden**, con la raíz por argumento (CLAUDE.md, «Ensayos aislados», 2):

      uv run python src/botsito/mql5bridge/generar_capa.py --repo . --perfil ftmo-2step-swing-100k

  escribe el fichero; con `--comprobar` no escribe nada y sale con 1 si el fichero del repo difiere
  de lo que generaría (y dice la primera línea distinta). El generador falla, sin escribir, si D2 no
  se cumple (un nombre de los dos ficheros con tipo, valor, opciones o estado distintos; la pareja de
  stops level con valores distintos; la de husos según la decisión 0), si un parámetro que entra es
  UNKNOWN o si la lista de los que entran nombra uno que no existe.
- **Lo que lleva**, como constantes `const` (D8) y un `enum` de MQL5 por cada parámetro de tipo
  `enum` y otro para los tres estados (decisión 5). Por parámetro: `P_<NOMBRE>` con su valor y
  `P_<NOMBRE>_ESTADO`. El valor se escribe como lo trae el yaml (texto, sin pasar por `float`), para
  que regenerar sea estable byte a byte. Tipos: fraccion, porcentaje, decimal y lotes → `double`;
  entero, minutos y puntos → `int`; booleano → `bool`; texto y hora → `string`. Ni `unidad` ni
  `descripcion` ni `consumido_por`: un cambio de redacción no debe cambiar el hash. Del calendario,
  `CIERRES_CUBRE_DESDE`/`HASTA` y tres arrays `const` (inicio, fin y fuente). La cabecera dice que se
  genera, desde qué ficheros y con qué orden, sin fecha ni sha (si no, regenerar daría diff).
- **El hash (D5)**: `capa_hash = SHA-256` en hexadecimal minúscula de **los bytes del fichero
  generado sin la única línea que lo lleva**, quitada entera con su LF. Esa línea es exactamente
  `const string CAPA_HASH = "<64 hex>";`. El generador escribe primero el resto, calcula el hash y lo
  pone. El test lo recalcula por su cuenta, sin importar el generador: lee los bytes, comprueba que
  hay una línea y solo una con esa forma, la quita, hace `hashlib.sha256` y compara. En un tag
  stable es la misma cuenta sobre `git show <tag>:mql5/Include/Botsito/Capa/Generado.mqh` (lo que
  hará R6a.7).
- **Desde knowledge/cuentas/ también.** `mql5/README.md:2` y ADR-0001:12 dicen que lo de MQL5 se
  genera desde `knowledge/spec/`; lo de la capa se genera también desde el perfil y el calendario de
  `knowledge/cuentas/`. No se corrigen aquí; línea para el cierre.
- **import-linter**: `pyproject.toml:105-117` pone `botsito.mql5bridge` en la capa 3, por encima de
  `engine`, `spec` y `config`: el generador puede leerlos. Confirmado.

### e. El journal v2 (D6)

- **Hoy:** `journal.py:37` fija `VERSION = 1`, y `_comprobar_objeto` rechaza cualquier otra
  (`:172-173`, «este lector es de la v1») y exige `null` en las seis reservadas (`:181-183`).
  `UltimaLinea` (Journal.mqh:152-181) exige la cabecera `{"v":<JOURNAL_VERSION>,"seq":`, así que un
  EA v2 sobre un journal v1 da `rota` (confirmado).
- **Lo que cambia (decisión 6):** el lector valida cada objeto con el esquema de la versión que
  declara su `v` (1 o 2); en v2, `capa_hash` es 64 hexadecimales en minúsculas **en todas las
  líneas** y las otras cinco reservadas siguen `null`; las claves, su orden y los eventos no cambian.
  Una llamada que mezcle versiones se rechaza (no hay cadena mixta). JOURNAL.md define la v2 una vez
  y dice en qué se diferencia de la v1.
- **El golden queda atado al hash si no se hace nada** (lo vi al leer `compilar.py`): el script de
  pruebas escribe el golden con el mismo escritor que el EA; si ese escritor lee `CAPA_HASH` de
  `Generado.mqh`, cada regeneración cambia el golden y obliga a volver a pasar las pruebas en MT5.
  Propongo que `JournalLinea` reciba el `capa_hash` como argumento: el EA le pasa `CAPA_HASH` y el
  script un valor fijo de prueba. Así el golden no depende de lo generado.
- **Goldens:** el v1 de `tests/golden/journal/` se queda congelado (lo seguirá leyendo el lector v1);
  el v2 va a una carpeta nueva, `tests/golden/journal_v2/`, porque `compilar.py pruebas` compara con
  **todos** los `.jsonl` bajo `--golden` (compilar.py:193). `test_journal_mql5.py:29-35` fija el
  hash de la última línea de cada cadena: los del v2, nuevos (auditor, herencia 7). El caso «rota»
  del script escribe hoy una línea v1 a mano (BotsitoPruebasCapa.mq5:140): pasa a v2.
- **Los journals congelados de R6a.1** (`anexos/EA-CONEXION/demo-*`) los lee
  `tests/unit/test_journal_demo_cierre.py`: siguen validando como v1, sin tocar los anexos
  (`docs/validation/anexos/EA-CONEXION/` está en `rutas_protegidas`).
- `VERSION_EA` sube a `"1.1"`, y con él `#property version` (`"1.00"`, Botsito.mq5:15), la
  `#property description` («(R6a.1)», :16) y la cabecera (:2-12, «journal v1», «llegan generadas en
  R6a.2») (auditor, 40 y herencia 6). Las dos deudas (PROJECT_STATE:85 y :86): esta rama no toca la
  comprobación del LF de `UltimaLinea` ni el reinicio de globales, así que no se pagan.

### f. Los tests de la capa (D8)

- **`LA_CAPA`** (`tests/contract/test_capa_mt5.py:506-513`): los seis ficheros de R6a.1. `_capa()`
  (:516-523) recorre `mql5/Experts`, `mql5/Include/Botsito` y `mql5/Scripts`, y
  `test_la_capa_son_los_ficheros_de_r6a1` (:526-529) exige que sean exactamente esos. Entra
  `Generado.mqh`, y el test pasa a llamarse `test_la_capa_son_los_ficheros_de_la_lista`.
- **`DEFINES_PERMITIDOS`** (:73): `VERSION_EA`, `JOURNAL_VERSION`, `LATIDO_SEG`, `TOPE_SESIONES`. No
  cambia: lo generado no lleva `#define`.
- **`globales()`** (:201-207) busca `^(?:static\s+)?<tipo>`, y `const` no es un tipo de la lista: una
  línea que empieza por `const` no cuenta como global. Confirmado.
- **El detector, `cifras_y_nombres`** (:266-272): decimales fuera de los textos, los cinco nombres de
  `TEXTOS_PROHIBIDOS` (:74, `EURUSD|XAUUSD|NASDAQ|FTMO|FundedNext`, distinguiendo mayúsculas y
  **también dentro de los textos**) y los `#define` fuera de la lista. **No prohíbe enteros** (su caso
  bueno `"int n = 32;"`, :410): esta rama no lo amplía a enteros, y lo declara. Leí la capa buscando
  enteros de firma, bróker o instrumento escritos a mano: **no hay ninguno**. En el EA y los includes
  solo hay `LATIDO_SEG` 60, `TOPE_SESIONES` 32, el `/60` de los minutos y las longitudes del hash; en
  el script de pruebas, los datos de los casos del golden (`6230`, `[300,86100]`, `18000`, fechas) y
  esperas en ms. No hay PARADA por enteros.
- **El cambio:** el detector exime `Generado.mqh` solo si sus bytes son idénticos a lo que da el
  generador, regenerado en memoria por el propio test; si difiere, lo trata como cualquier otro
  fichero (y además falla). Se rompe a propósito en los dos sentidos: (1) un `Generado.mqh` de
  ejemplo idéntico a lo generado con un decimal y `EURUSD` pasa, y el mismo con un byte cambiado no
  pasa; (2) un decimal o `FTMO` en cualquier otro fichero de la capa no pasa aunque `Generado.mqh` sea
  correcto. Y como pide a6 (EA-CONEXION.md:1142 y :1278; auditor, herencia 2), el test pasa a
  llamarse por lo que comprueba: `test_la_capa_no_lleva_decimales_ni_nombres_fuera_de_lo_generado`.
- `LECTURA_PERMITIDA` sigue vacía (:72).

### g. El Strategy Tester sin una prueba viva (D9)

**No lo medí**, y no se puede medir sin MT5 ni sin cuenta: lo de R6a.1 se midió con la prueba de
octubre conectada (EA-CONEXION.md:127-145; `ACCOUNT_TRADE_MODE` era DEMO «con la cuenta de prueba
conectada»), y con otra cuenta no está medido (:135-136). Para medirlo habría que arrancar el
terminal con la cuenta de la prueba ya vencida, y eso no lo hago sin tu orden (D9: el terminal se
toca solo en la fase 3). Decisión 7.

### h. Herencias

Buscado R6a.2, capa_hash, LATIDO_SEG y Params.mqh en PROJECT_STATE, HISTORIA, la hoja de ruta,
EA-CONEXION.md, PLATAFORMA-ADELANTADA.md y ADR-0082 (yo y el auditor):

- **Entran en esta rama:** JOURNAL.md:45 (`capa_hash` reservada) y :71 («R6a.2 puede generarlas si
  se decide»: con D7, no se generan); EA-CONEXION.md §7 (:729-749: compilar, `LA_CAPA`,
  `DEFINES_PERMITIDOS`, el tester, VERSION_EA que sube, «R6a.2: llenarlo es la versión 2»); a6
  (:1142, :1278: renombrar el detector); la cabecera y las `#property` del EA (Botsito.mq5:2-16) y el
  párrafo de R6a.1 de `mql5/README.md`, que dicen v1 (auditor, herencia 6); JOURNAL.md:99 («F23
  escribe esta misma v1»).
- **Líneas para el cierre (no se tocan aquí):** hoja, R6a.2 :521-522 (D7: no se generan, y por qué);
  PROJECT_STATE:82 («El validador del journal v1…»: pasa a decir v1 y v2; auditor, herencia 4);
  `mql5/README.md:2` y ADR-0001:12 («se genera desde `knowledge/spec/`», d: el encargo dice que no
  se corrigen aquí); la línea de activar-sesion de D3.
- **Para que lo decidas (decisión 8):** ADR-0082 §6 (:104-111) habla de «sus hashes» y MASTER_PLAN
  §H.2 (:270) de dos (`spec_hash` de Params.mqh y `risk_hash` de Risk.mqh, F28). El journal ya
  reserva `spec_hash` y `risk_hash`. Con un solo `capa_hash`, lo de prop_firm viaja hoy en
  `capa_hash` y en F28 viajaría también en `risk_hash` (auditor, 35 y herencia 5).
- **Fuera de alcance, para que lo sepas:** la prueba gratuita que crees para la fase 3 es la misma
  que piden A.5 y F17 (HOJA-DE-RUTA.md:689-697, «una sola activa a la vez»; RUMBO-2026-11.md:43;
  auditor, herencia 3).
- PLATAFORMA-ADELANTADA.md no nombra nada de esto que no esté arriba.

## El encargo frente al repo (auditor-encargo, 2026-11-12)

El auditor contrastó 62 afirmaciones: 51 correctas, 1 incorrecta y 10 con matiz, y halló 7
herencias. Lo que cambia el trabajo:

- **INCORRECTA (22): la pareja huso_operativa / firma_huso_corte de D2.** Ver b y la decisión 0.
- **Herencia 1: cada `make check` lee el M1 de marzo** y hay que declararlo el mismo día, y
  `HOLDOUT-EXPOSICIONES.md` no estaba en `rutas_permitidas`. Hecho en la apertura (fila del
  2026-11-12 y contrato ampliado). Lo mismo matiza «la rama no lee velas» (§3 del encargo, auditor
  61): la rama no las pide, pero cada `make check` las lee.
- **MATIZ (35) y herencia 5: un solo hash frente a «sus hashes».** Decisión 8.
- **MATIZ (40) y herencia 6:** con VERSION_EA suben las `#property` y la cabecera del EA (e).
- **MATIZ (48) y herencia 2:** a6 pide renombrar el detector (f).
- **Herencia 7:** los hashes de la última línea de los goldens van escritos en el test (e).
- **Herencia 3:** la prueba de la fase 3 es la misma que necesitan A.5 y F17 (h).
- Matices menores, sin efecto: 4 de las 5 últimas ramas son de fidelidad, no 5 (F38u es R2.4; la
  proporción de RUMBO §6 se cumple igual); también depende de esta rama R6a.7; «el predicado
  (cierre_sin_calendario)» es el motivo `MOTIVO_SIN_CALENDARIO` (domain/cierres.py:22); la hoja dice
  «`SymbolInfo`/`AccountInfo` con el perfil», y «el instrumento» sale de MASTER_PLAN.md:270; de los
  cinco parámetros de la estrategia solo `sesgo_h4_tope_velas` apunta a una pieza en `consumido_por`
  (F18): los otros se sostienen por su descripción.

## Lo que no pude medir

- El Strategy Tester sin una prueba viva (g).
- Que MQL5 compile arrays `const` de nivel global con inicializador y un `enum` por parámetro: lo
  dirá la compilación de la fase 2. Si no compila, PARADA.
- La CI la consulté con gh (check-runs del commit de estado): verde. El auditor no la pudo ver.

## Exposiciones

La fila del 2026-11-12 de `trabajo/capa-generada` en HOLDOUT-EXPOSICIONES.md: los `make check` de la
rama (cada uno lee el M1 de marzo y calienta con el de junio). Nada más.

## Lo que necesito que decidas

0. La pareja de husos (D2). Opciones: (a) entra `firma_huso_corte` (el corte del día de la firma, el
   que necesita el veto de R6a.4), `huso_operativa` queda fuera, y el generador comprueba, como
   ADR-0053 §4, que los dos dan los mismos instantes en las medianoches de cada día de `cubre`, y
   falla si no; (b) entran los dos, comprobados igual; (c) ninguno hasta R6a.4. Recomiendo (a): es lo
   que ya decide ADR-0053 §4 para el simulador, `huso_operativa` es el reloj del trader, y la
   comparación por texto fallaría siempre. Coste de (b): un nombre de la operativa del trader en la
   capa sin pieza que lo lea. Nota para R6a.4: MQL5 recibirá un nombre IANA; cómo lo pasa a instantes
   lo decide esa rama.
1. `cierre_pendientes` (DEFAULT_AMBIGUOUS, A-55). Opciones: (a) fuera; (b) dentro, con su estado.
   Recomiendo (a): es la política del bróker simulado, no una regla de la firma, y qué hace la capa
   con una pendiente al abrir la ventana lo decide R6a.5 con A-55; entrar después es regenerar.
   Coste de (b): ninguno técnico, pero lleva a la capa algo que aún no es de la firma.
2. Los que no lee ninguna pieza (filtro_noticias, firma_noticias_restringe, cuenta_objetivo,
   cuenta_pruebas, las fases y sus objetivos, comisiones, swaps, firma_ordenes_simultaneas_max,
   firma_posiciones_dia_max, firma_tamano_posicion_aviso_aplica). Opciones: (a) fuera, por la regla
   de D1; (b) todo el perfil dentro. Recomiendo (a): D1 exige que una pieza lo lea, y entran cuando
   una lo lea. Coste de (b): constantes que nadie usa, que cambian el hash cuando cambian.
3. La pareja de stops level. Opciones: (a) sale `instrumento_stops_level`; (b) sale
   `firma_stops_level_puntos`. En las dos, el generador falla si sus valores difieren. Recomiendo
   (a): es la ficha del instrumento, como los otros cuatro `instrumento_*` que compara el pre-vuelo
   con `SymbolInfo`. Coste de (b): ninguno grave; el nombre del perfil dice «firma».
4. La forma del calendario. Opciones: (a) los 228 instantes juntos de `calendario()`, en segundos
   UTC, con `cubre` y su fuente; (b) la pauta y los extraordinarios con sus husos. Recomiendo (a):
   es lo que recibe hoy el predicado de Python y no hay que portar la conversión de husos. Coste de
   (b): portar a MQL5 el cambio de hora de America/New_York.
5. La forma de las constantes. Opciones: (a) `const` por parámetro con su valor y su estado, y un
   `enum` de MQL5 por parámetro enum y otro para los estados; (b) los enum como texto. Recomiendo
   (a): un valor mal escrito en una pieza no compila. Coste de (b): ninguno hoy; una pieza compara
   textos.
6. El journal v2. Opciones: (a) `capa_hash` en todas las líneas, el lector por la versión que
   declara cada línea, sin mezclar versiones en una llamada, `JournalLinea` con el hash como
   argumento (el script de pruebas, uno fijo), el golden v1 congelado y el v2 en
   `tests/golden/journal_v2/`; (b) `capa_hash` solo en el `arranque`. Recomiendo (a): la tabla de
   JOURNAL.md dice qué lleva cada clave en todas las líneas, y cada línea dice con qué capa se
   escribió; el hash como argumento evita que el golden dependa de lo generado. Coste de (b): un
   caso especial por evento.
7. El tester (D9). Opciones: (a) la corrida de cierre en la demo, con la prueba nueva, como R6a.1;
   (b) antes, intentar el tester con la cuenta vencida. Recomiendo (a): la corrida en la demo es la
   que escribe `cuenta` con la cuenta real conectada, y (b) no está medido y puede no dar nada. Coste
   de (b): arrancar el terminal con una cuenta vencida para quizá no medir nada.
8. Uno o dos hashes. Opciones: (a) un solo `capa_hash` (D5), y `risk_hash` sigue reservado para F28;
   (b) dos ya. Recomiendo (a), como D5 y ADR-0082 §6 («lo que la capa recibe antes de F26 lleva su
   propio hash»). Línea para el cierre: en F28, lo de prop_firm viajará también en `risk_hash`, y esa
   rama dice si `capa_hash` sigue. Coste de (b): fijar ahora lo que es de F28.

Espero tu respuesta a la PARADA.

## Respuesta a la PARADA (consultor, 2026-11-12)

Copiada tal cual (también al final del encargo, «Cambio del consultor»):

> Modelo: Opus · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA de la fase 0 de trabajo/capa-generada (2026-11-12). Cópiala tal cual al informe (CAPA-GENERADA.md, «Respuesta a la PARADA») y al final de docs/encargos/trabajo-capa-generada.md, bajo «Cambio del consultor» (los puntos A a E). Donde choque con el encargo, manda esto. Aplícala punto por punto.
>
> A. Cambio de calendario y de alcance (Aleks fija la sesión 7a para el domingo 15 de noviembre; su ingesta no puede abrirse con esta rama abierta).
> A1. Sin demo ni prueba nueva de FTMO: la fase 3 sale del encargo y no me pides crear ninguna prueba. «El hash está en el journal» se comprueba con el script de pruebas, que corre sin conexión (EA-CONEXION.md, hacia :100). Es una lectura mía del «Hecho cuando» de R6a.2: decláralo como desviación decidida por el consultor.
> A2. La corrida en la demo pasa a R6a.8, que ya necesita la demo una semana. Para el commit del contrato prepara: (i) la línea de R6a.8 en la hoja, que dice que su journal en la demo es v2 y comprueba que capa_hash coincide con el del repo en el tag vigente; (ii) la línea de Estado de R6a.2, que dice que el hash se comprobó con el script de pruebas y que la demo queda para R6a.8.
> A3. El procedimiento de docs/runbooks/DEMO-FTMO.md se escribe igual, para R6a.8, incluido mover el journal v1 fuera de MQL5/Files antes del primer arranque v2.
> A4. Calendario: fases 1 y 2 hoy y mañana viernes; revisor y «Rama lista para revisión, NO cerrada» el sábado 14. Si no cabe, PARADA con lo que recortarías.
> A5. Si el domingo, con la grabación hecha, la rama no está para cerrar, PARADA y decido yo; no abras nada más.
>
> B. Las nueve decisiones.
> 0. (a). Entra firma_huso_corte; huso_operativa queda fuera. El generador comprueba, como ADR-0053 §4, que los dos dan los mismos instantes en la medianoche de cada día de `cubre`, y falla si no. Por qué: es el reloj que ya usa el simulador, y reloj_dia_riesgo: civil_operativa es la medianoche en huso_operativa (ADR-0027, citado en ADR-0053 §4), así que la capa la resuelve con firma_huso_corte bajo esa misma comprobación. Línea para la hoja, en R6a.4: «reloj_dia_riesgo se resuelve con firma_huso_corte, comprobado contra huso_operativa al generar (ADR-0053 §4); cómo pasa MQL5 un nombre IANA a instantes lo decide esta rama». D2 queda corregida así: un error del consultor, para la fila de ERRORES-RECURRENTES.
> 1. (a). cierre_pendientes, fuera: qué hace la capa con una pendiente al abrir la ventana lo decide R6a.5 con A-55, y entrar entonces es regenerar.
> 2. (a). Fuera lo que no lee ninguna pieza, por la regla de D1.
> 3. (a). Sale instrumento_stops_level, y el generador falla si difiere de firma_stops_level_puntos.
> 4. (a). Los 228 instantes juntos de calendario(), en segundos UTC, con `cubre` y su fuente.
> 5. (a). Si el enum o los arrays const globales no compilan en MQL5, PARADA.
> 6. (a), con un añadido por A1. El golden v2 va con el hash fijo de prueba, como propones. Además, el script de pruebas escribe un fichero aparte, fuera de --golden (comparar_con_golden solo recorre los del golden, compilar.py:192-201), con una línea v2 escrita por JournalLinea con el CAPA_HASH real de Generado.mqh. compilar.py pruebas lo valida como v2 y comprueba que su capa_hash es igual al recalculado desde el Generado.mqh del repo; si no lo es, falla. Ese paso lleva su test en Python, roto a propósito en los dos sentidos (hash distinto y fichero ausente). La salida de la corrida va a los anexos, con su sha256.
> 7. No aplica: la demo sale de la rama (A1 y A2). No arranques el terminal con la cuenta vencida.
> 8. (a). Un solo capa_hash. Línea para el cierre: en F28, lo de prop_firm viajará también en risk_hash, y esa rama dice si capa_hash sigue.
>
> C. Lo demás de la fase 0.
> - La fila de HOLDOUT-EXPOSICIONES de la apertura y la ampliación del contrato, bien.
> - lote_si_no_cabe CONFIRMED frente a ADR-0082:53, que lo da por DEFAULT_AMBIGUOUS: déjalo en el informe como línea para el cierre; aquí no se toca el ADR.
> - El matiz de «4 de las 5 últimas ramas son de fidelidad», aceptado: la proporción de RUMBO §6 se cumple igual.
> - PROJECT_STATE:82, mql5/README.md:2 y ADR-0001:12, como líneas para el cierre, como dices.
>
> Sigue con la fase 1 (tests primero, cada uno roto a propósito en los dos sentidos, make check sellado) y la fase 2. PARADA solo si algo no cuadra con esto. Rama lista para revisión, NO cerrada.

`make check` del commit de la fase 0 (`4518e631`): exit 0, 3443 passed, ningún `failed`, SELLO
sobre el árbol `43793082`. `PICO DE MEMORIA de make check: 311 MiB`.

## Fase 1 (2026-11-12): los tests, y lo que hace falta para que pasen

Aplicada la respuesta punto por punto (B0 a B8). **Desviación declarada:** la fase 1 trae, además de
los tests, lo de Python que esos tests ejercen: el generador, su salida commiteada, el lector v1/v2
con su golden v2 y la comprobación del `capa_hash` del script en `compilar.py`. R6a.1 hizo lo mismo:
un test de un fichero generado no pasa sin el fichero. Lo de MQL5 (Journal.mqh, el EA y el script de
pruebas) es la fase 2. Los tests se escribieron antes que el fichero: con el generador escrito y sin
`Generado.mqh`, ocho tests de `test_capa_generada.py` y `test_capa_mt5.py` fallaban, y fallaban solo
por eso.

Lo que entra:

- `src/botsito/mql5bridge/generar_capa.py`. Lee los 31 parámetros de `ENTRAN` por la puerta del
  registro: los de `parametros.yaml` y los del perfil, con D2 sobre los nombres comunes (tipo, valor,
  opciones y estado). Comprueba la pareja de stops level (B3) y los dos relojes en las medianoches de
  cada día de `cubre` (B0). `reloj_dia_riesgo` tiene que ser `civil_operativa`, y un parámetro
  `UNKNOWN` hace fallar. Escribe constantes `const` y un `enum` de MQL5 por parámetro enum y otro
  para los estados (B5); el calendario va como los 228 instantes juntos en segundos UTC, con
  `cubre` y su fuente (B4). Ni `#define` ni variables. `--comprobar` no escribe y sale con 1 si el
  fichero difiere.
- `mql5/Include/Botsito/Capa/Generado.mqh`, escrito por Aleks con «!» (abajo):
  `capa_hash 8d1f61bcd24837826dd89a76133323abc92998b211f67398374028622c0e7601`.
- `journal.py`, v1 y v2: en v2, `capa_hash` es un hash de 64 hexadecimales en todas las líneas; cada
  fichero se lee por la versión que declara y una llamada que mezcla versiones se rechaza. El golden
  v1 queda congelado y el v2 está en `tests/golden/journal_v2/`, generado desde el v1 con el hash
  fijo de prueba por `anexos/CAPA-GENERADA/fase1/generar_golden_v2.py` (B6). Hashes finales:
  continua `828b6d6f…54aee`, rota `54f31263…4a31f`.
- `compilar.py pruebas --repo`: valida `capa/capa_hash.jsonl` como v2 y comprueba que su
  `capa_hash` es el recalculado desde el `Generado.mqh` del índice. Falla si no lo es o si falta el
  fichero, y da el sha256 de cada fichero de la salida (B6, el añadido).
- `mql5/JOURNAL.md`, formatos v1 y v2; `tests/golden/README.md`.
- `test_perfil_cuenta.py`: el cruce entre el perfil y el registro compara también el estado (un
  `DEFAULT_AMBIGUOUS` no es un `CONFIRMED`).
- `test_capa_mt5.py`: `Generado.mqh` entra en la lista de la capa y se exime de la prohibición de
  cifras y nombres solo si es byte a byte lo que da el generador.
- `Tests Currently Passing`: de 2017 a 2039 funciones de test.

### Cada comprobación, rota a propósito

En los dos sentidos: cada test tiene su caso que pasa y su caso que falla (sobre una copia de los
yaml en `tmp_path`, nunca sobre el repo). Y además se rompió el código o el fichero real, uno a uno;
después se restauró cada fichero desde su copia en la carpeta de trabajo de la sesión, `diff -q` dio
igual y los 69 tests de los cinco ficheros pasaron.

| Rotura | Lo que falló |
|---|---|
| 1. Un valor de `Generado.mqh` editado a mano (5.0 → 5.5) | `test_regenerar_no_da_diff`, `test_la_copia_de_los_yaml_da_lo_mismo_y_un_valor_cambiado_no`, `test_la_orden_comprobar_no_escribe_y_dice_si_difiere`, `test_el_hash_se_recalcula_por_su_cuenta`, `test_la_capa_no_lleva_decimales_ni_nombres_fuera_de_lo_generado` |
| 2. El `CAPA_HASH` de `Generado.mqh` cambiado (un dígito) | los mismos cinco |
| 3. La comprobación de los relojes, desactivada | `test_los_dos_relojes_tienen_que_dar_la_misma_medianoche` |
| 4. La de la pareja de stops level, desactivada | `test_la_pareja_de_stops_level_tiene_que_coincidir` |
| 5. La del `capa_hash` hexadecimal en v2, desactivada | `test_en_v2_capa_hash_es_un_hash_y_las_demas_reservadas_null` |
| 6. La comparación con el hash del repo en `compilar.py`, desactivada | `test_el_capa_hash_del_script_en_los_dos_sentidos` |
| 7. El rechazo de la cadena mixta, desactivado | `test_cada_fichero_se_lee_por_su_version_y_no_hay_cadena_mixta` |
| 8. El fichero ausente en `compilar.py` da `[]` | `test_el_capa_hash_del_script_en_los_dos_sentidos` |

### La guardia

- **PARADA, y Aleks con «!».** La guardia negó `uv run python src/botsito/mql5bridge/generar_capa.py
  …`, porque la ruta `// CAPA_HASH = SHA-256 de este fichero sin su linea (…)` no se puede canonizar.
  Un guion nuevo se lee como código sin revisar, y la guardia tomó por ruta de red un texto suyo que
  empieza por `//`: los comentarios de MQL5 que escribe en la cabecera. Es un falso positivo. No lo
  rodeé: lo lanzó Aleks con «!» desde la raíz y escribió solo `Generado.mqh`. Va a la deuda de la
  guardia (letra K): un literal de texto que empieza por `//` no es una ruta.
- **`cmp`, negado.** «La guardia no sabe con qué se ejecuta» el primer fichero. Lee `cmp a b` como si
  ejecutara `a`, y es un falso positivo de la misma deuda. Comprobé la restauración con `diff -q`,
  que la guardia deja, sin tocar el comando negado.
- **Una asignación `O=…` mía**, negada por la lista cerrada de nombres de entorno. No es un fallo de
  la guardia: rescribí el comando sin la variable, que es la forma que ella propone.

## Estado

EN CURSO: fase 1 hecha (falta su commit sellado); después, la fase 2.
