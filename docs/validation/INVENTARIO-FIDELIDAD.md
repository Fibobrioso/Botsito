# Inventario para la fidelidad: cuánto del bot existe y qué falta para medirla

Rama `trabajo/inventario-fidelidad`, 2026-09-23. Sin merge, sin tag y sin push.

**Qué se ha hecho: solo LEER** código, spec y tests. No se ha ejecutado el bot, ni ningún pipeline
contra ningún caso ni contra ningún día de ningún libro. No hay código nuevo.

«Medir fidelidad» es comparar, caso `dev` por caso `dev`, lo que haría el bot con lo que hizo el
trader.

## 0. Resumen

**EL BOT NO EXISTE TODAVÍA como algo que se pueda ejecutar.**

- **Lo que no hay.** En `src/botsito/` no hay motor de estrategia: ningún módulo evalúa un
  predicado ni ejecuta una acción. Lo confirma el `MASTER_PLAN`: F18 a F24 (dominio, statecharts,
  bucle y simulación) y F26 (validador de fidelidad) no se han empezado.
- **La spec sí existe, como forma ejecutable DECLARADA.** De las 32 reglas, 27 están vigentes y
  todas tienen `forma`. Esa forma usa un vocabulario de 23 predicados y 15 acciones. Está validada
  ESTÁTICAMENTE: `spec/modelo.py:comprobar_forma` y `comprobar_vocabulario`, llamadas desde
  `validation/knowledge.py`, con 45 tests en `tests/unit/test_spec.py`. Pero nada la interpreta.
- **La infraestructura sí existe:**
  - velas M1 y su agregación con anclaje y cambio de hora (F15: `data/agregacion.py`);
  - los tipos de valor (`domain/valores.py`);
  - la ventana y el universo de casos (`cases/ventanas.py`);
  - el reparto y la puerta del holdout;
  - 6 casos `dev` de mayo en `knowledge/cases/dev/`.

## 1. De cada regla de la spec al código

**Leyenda de estados:**
- **no existe**: no hay código que la aplique;
- **parcial**: existe un insumo que la regla necesita, pero no la regla.

La columna «forma» dice si la regla tiene forma ejecutable validada estáticamente. Sirve de
contrato para quien la implemente, pero no es implementación.

**Ambigüedades.** Van por la vía que las ata:
- `param`: la regla lee un parámetro que la ambigüedad nombra;
- `cita`: el texto de la regla la nombra;
- `tema`: es inferencia mía por el título, y está sin comprobar.

`bloq` quiere decir `bloqueante: true`.

| regla | qué dice (título) | código hoy | tests | estado | forma | ambigüedades |
|---|---|---|---|---|---|---|
| RN-001 | la ventana operativa es el horario del trader | `cases/ventanas.py:construir_caso` recorta el DÍA de datos (`ventana_local` 00:00-15:00) y `kit/config.yaml` declara las sesiones 07-11 y 11-15; la regla (operar solo dentro) no | `test_agregacion*` indirectos | parcial | sí | — |
| RN-002 | al fin de la ventana se cierra lo abierto | — | — | no existe | sí | A-30 (tema) |
| RN-003 | el sesgo lo fija la H4 previa y cambia si rompe su extremo | `data/agregacion.py:agregar`, `limites_del_dia` y `agregar_serie` construyen las H4 con anclaje (`anclaje_h4`); el sesgo no | `test_agregacion.py` (12), `test_agregacion_dst.py` (9) | parcial | sí | A-26 (tema) |
| RN-004 | la liquidez de M15 se toma con cuerpo | M15 agregables con `agregar(…, 15, …)`; la regla no | los mismos | parcial | sí | **A-24 bloq** (cita) |
| RN-005 | lo del lado de ruido de la liquidez M15 no es entrada | — | — | no existe | sí | A-24 bloq, A-26 (tema) |
| RN-006 | la orden límite se reubica al completarse cada zona de control | — | — | no existe | sí | **A-21 bloq** (tema), A-30 (tema) |
| RN-007 | varias M1 que forman un OB mayor se mapean como una | — | — | no existe | sí | — |
| RN-008 | sin esquema de entrada no hay entrada | — | — | no existe | sí | A-32 (param) |
| RN-009 | más zonas de control de las admitidas invalidan | — | — | no existe | sí | A-21 bloq (tema) |
| RN-010 | entrada activada sin ruptura se gestiona como otra | — | — | no existe | sí | A-29 (cita), A-31 (tema) |
| RN-011 | el lote se dimensiona hasta el stop | tipos `domain/valores.py:Fraccion` y `Porcentaje`; el cálculo no | `test_valores.py` (tipos) | no existe | sí | A-29 (param) |
| RN-012 | el stop cuesta el riesgo entero | — | — | no existe | sí | — (pero ver A-18: stop en dos tiempos) |
| RN-014 | break even al romperse la zona de control posterior | — | — | no existe | sí | A-13 (param, cita) |
| RN-015 | objetivo fijo, trazado con la orden | — | — | no existe | sí | **A-18** (param, cita), A-33 (param) |
| RN-016 | el día se limita por cartuchos | — | — | no existe | sí | A-25 (param), A-31 (cita) |
| RN-017 | un ganador no apaga el día | — | — | no existe | sí | — |
| RN-018 | no hay operaciones en paralelo | — | — | no existe | sí | — |
| RN-019 | reentrada tras un equal sin gastar cartucho | — | — | no existe | sí | A-29, A-31 (cita) |
| RN-020 | el tope porcentual del trader | — | — | no existe | sí | — |
| RN-021 | el spread no se filtra | — | — | no existe | sí | — |
| RN-022 | si no encaja, el bot se abstiene | — | — | no existe | sí | — |
| RN-026 | si el broker no admite el stop, se abstiene | — | — | no existe | sí | A-27 (param) |
| RN-027 | lote redondeado a la baja al escalón | — | — | no existe | sí | A-27 (param) |
| RN-029 | freno diario de la firma | — | — | no existe | sí | A-28 (tema: reloj del día) |
| RN-030 | cierre al acercarse a un límite de la firma | — | — | no existe | sí | A-28 (tema) |
| RN-031 | freno total de la firma | — | — | no existe | sí | — |
| RN-032 | no se abre lo que no cabe antes del límite | — | — | no existe | sí | A-28 (tema) |

**Cuenta:** 3 parciales (RN-001, RN-003 y RN-004), 24 que no existen y ninguna implementada.
Descartadas y fuera del mapa: RN-013, RN-023, RN-024, RN-025 y RN-028.

**Ambigüedades abiertas que no son de una regla:**
- **A-16**, cuánto se separan las velas del trader de las de Dukascopy. Es de los datos (§4).
- **A-28**, el reloj del servidor. Afecta a toda comparación horaria en real, no en backtest.

## 2. El caso y su contraparte en el bot

**Lo que un `caso-*.yaml` lleva hoy.** Es una lista cerrada, definida en
`cases/biblioteca.py:CLAVES_CASO`, `CLAVES_OPERACION` y `CLAVES_FUENTE`:

- caso: `id`, `dia`, `simbolo`, `operaciones` y `fuente`;
- operación: `instante_utc`, `sesion`, `direccion`, `entrada` y `stop`;
- fuente: `tipo`, `fichero`, `sha256` e `ingerido_el`.

La ventana de datos del mismo caso vive en el reparto (`ventanas.yaml`, `cases/ventanas.py:Caso`):
`dataset_id`, `desde_utc`, `hasta_utc`, `n_velas`, `sha256` y `limites_h4` por anclaje candidato.

**Lo que el bot, cuando exista, tendría que producir para poder comparar:**

| campo del caso | contraparte en el bot (según la spec) | nota |
|---|---|---|
| `direccion` | el sesgo H4 (RN-003) y el esquema (RN-008) | comparable |
| `instante_utc` | el instante en que `se_activa_entrada` | Hay que fijar QUÉ instante compara: el de colocar la orden límite (RN-006/011) o el del llenado. El xlsx da el de apertura |
| `entrada` | el precio de la orden límite al activarse | Depende de la reubicación (RN-006) y de la serie de precios (A-16) |
| `stop` | `escribir_stop_en_la_orden` (RN-011/012) | Depende de `stop_fraccion_caja` y de la caja; ver A-18 y el stop en dos tiempos |
| `sesion` | derivable del instante con `huso_operativa` | El caso la fija al ingerir |
| `id`, `dia`, `simbolo`, `fuente` | metadatos | sin contraparte, y no hace falta |

**Lo que el bot produciría y el caso NO tiene:**
- el **objetivo**, excluido a propósito (ADR-0037 §7), así que la regla más discutida (A-18) no se
  puede medir contra el caso;
- el **lote**;
- la **gestión**: break even, reubicaciones y cierre forzoso;
- los **cartuchos**;
- la **caja** (niveles 0 y 1);
- el **resultado**, ni cierre ni PnL, también a propósito.

**Y lo que el caso no tiene pero una medida de fidelidad necesita:** el **`no_trade` de las
sesiones sin operación**. Derivarlo por ausencia es una inferencia sin ADR: es la decisión **D1**
de `docs/plan/features/F14-case-library.md`, y sigue sin tomar. Sin D1, el bot solo se puede
comparar en las sesiones en que el trader operó, que es media medida.

**Los casos `dev` que existen HOY son solo los 6 de mayo** (`knowledge/cases/dev/`), medido
listando la carpeta.
- **Agosto y abril** son material de desarrollo, pero **no tienen ni un `caso-*.yaml`**. Sus
  lecturas (`F14A-INGESTA.md`, `ABRIL-Y-LA-CAJA.md`) midieron el xlsx, no lo ingirieron.
  `ingesta.dias_ingeribles` solo toma días de un reparto del kit, y esos meses no están repartidos.
- **Los 4 `fidelidad-dev` de septiembre** tampoco están ingeridos: la ingesta solo lee el kit.

## 3. Lo mínimo para una primera medida de fidelidad sobre los casos `dev`

La lista está en orden de dependencia. Tamaño: **S**, días; **M**, una rama normal; **L**, varias
ramas.

| # | qué | tamaño | depende de |
|---|---|---|---|
| 1 | **Decidir D1** (la verdad del caso: xlsx o `LABEL_CASE`; el `no_trade` por ausencia), con su ADR | S | consultor |
| 2 | **Fijar qué se compara y con qué tolerancia**: decisión por sesión; dirección; instante, cuál y con qué margen; entrada y stop, con qué margen en puntos dada A-16. Para `dev` no hace falta PREREGISTRO, pero conviene escribirlo antes de mirar | S | 1 |
| 3 | **Decidir de dónde salen más casos `dev`**: ingerir agosto y abril, y los 4 `fidelidad-dev`, que hoy no tienen ruta de ingesta | S (decisión) + M (ingesta) | consultor |
| 4 | **F18: tipos del dominio y sesgo H4** (RN-003), sobre las H4 que ya agrega F15 | M | — |
| 5 | **F19: zonas M15** (liquidez con cuerpo, lado de ruido: RN-004/005) | L | **A-24 bloqueante** |
| 6 | **F20: M1** (mapeo, breaker, zonas de control, esquemas, orden límite y su reubicación: RN-006 a RN-010) | L | **A-21 bloqueante**, A-32, A-29 |
| 7 | **F21: geometría de riesgo** (caja, stop y lote: RN-011/012; objetivo RN-015; BE RN-014) | M | A-18 (solo para el objetivo), A-13 |
| 8 | **F22/F23: estado del día y bucle con reloj causal** (ventana, cierre, cartuchos, no paralelo, reentrada y abstención: RN-001/002/016 a 019/022) | L | 4 a 7 |
| 9 | **Llenado sobre M1** (un F24 mínimo, sin ticks), suficiente para comparar entrada y stop | M | 8 |
| 10 | **Arnés de fidelidad sobre `dev`**: correr 8 y 9 por caso, comparar con 2 y dar un informe descriptivo con intervalo | M | 1, 2, 9 |

**Lo que NO hace falta para esta primera medida:**
- las reglas de la firma y del broker: RN-020, RN-021, RN-026, RN-027 y RN-029 a RN-032;
- ticks (F16/F17);
- MQL5 (F28 en adelante).

Condicionan dinero, no la decisión de entrada.

**Y el orden real lo marcan las dos bloqueantes:** sin A-24 y A-21 no se pueden escribir F19 ni
F20, y sin ellas no hay entrada que comparar.

## 4. Riesgos

**Mirar el futuro (look-ahead).**
- **La agregación no sabe qué hora es.** `data/agregacion.py:agregar` marca `completa` respecto a
  la LISTA de M1 que recibe, no respecto al instante de la decisión. El reparto recorta el caso de
  00:00 a 15:00 (`ventana_local`). Un motor que agregue ese día entero y lea una H4 o M15 antes de
  su cierre vería el futuro.
- **El requisito:** agregar solo con las M1 anteriores al instante, o usar solo velas cerradas en
  ese instante. El MASTER_PLAN ya pide para F19 el test «truncado = completo». RN-003 («la H4
  PREVIA») lo hace explícito para el sesgo.
- **`limites_h4` del caso** está calculado sobre el día completo, pero son límites de reloj, no
  precios. No es look-ahead, y no se debe usar como si lo fuera.
- **El xlsx trae columnas de resultado** (`maxTP` y otras). La ingesta las excluye
  (ADR-0037 §7), pero usarlas para ajustar reglas sería entrenar con la respuesta.

**Huso y velas.**
- **Dos husos distintos.** Los casos guardan `instante_utc` desde libros declarados en UTC
  (`knowledge/corpus/libros.yaml`), las sesiones son de `huso_operativa` (Europe/Madrid, con
  cambio de hora) y el gráfico de FX Replay que ve el trader es **UTC+2 fijo** (`CLAUDE.md`). En
  invierno, Madrid es UTC+1: lo que el trader ve a las 09:00 de su gráfico no es 09:00 de Madrid.
  Afecta a enero; abril y mayo ya están en horario de verano.
- **El anclaje H4.** El parámetro es 17:00 (el candidato `servidor-ny-17` de `kit/config.yaml`).
  **No está medido** que las H4 del gráfico del trader en FX Replay tengan esos mismos límites. Si
  no los tienen, «la H4 previa» del bot y la del trader son velas distintas.
- **Las series de precios (A-16).** El feed del trader y Dukascopy difieren de 1 a 2 puntos, medido
  en abril. Una ruptura «con cuerpo» o «con mecha» a 1 punto del nivel puede salir distinta, y la
  entrada y el stop comparados llevan ese ruido.

**Datos que aún no tenemos:**
- ticks y spread (F16/F17);
- las especificaciones y el reloj de FTMO (A-27, A-28);
- **la caja por operación**: el xlsx no la trae, así que ni `stop_fraccion_caja` ni A-18 se
  pueden contrastar con los casos;
- `LABEL_CASE`: no hay ni una etiqueta del kit ciego;
- **muestra**: 6 casos `dev`, sin potencia. Cualquier cifra será descriptiva (lo dice el
  docstring de `cases/fidelidad.py`).

## 5. Preguntas para el consultor

1. **D1:** ¿la verdad de un caso es el xlsx, con el `no_trade` derivado por ausencia, o
   `LABEL_CASE`? Es el punto 1 de §3, y sin él la medida es parcial.
2. **Agosto, abril y los 4 `fidelidad-dev`:** ¿se les da ruta de ingesta para tener más de 6
   casos `dev`?
3. **El instante que se compara:** ¿colocación de la orden límite o llenado?

## Estado

WAITING_FOR_USER_VALIDATION
