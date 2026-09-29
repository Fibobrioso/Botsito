# El script de la demo de FTMO y su lector

Rama `trabajo/demo-ftmo-script`, 2026-09-28, desde `main` en `stable/F25-registrar-embudo`. Prepara
la medida en la cuenta de prueba gratuita de FTMO de lo que ADR-0057, A-27 y A-28 dejaron pendiente.
**Nada se ejecuta en FTMO desde aquí, ningún valor entra en los parámetros y ninguna decisión se
cierra**: lo ejecuta Aleks siguiendo `docs/runbooks/DEMO-FTMO.md`, y los valores entran en otra rama,
con los CSV reales delante.

## 1. Fase 1 · El script, `tools/mql5/MedirDemoFTMO.mq5`

**Compilado en esta máquina** con MetaEditor 64 bits del MetaTrader 5 instalado, fuera del
repositorio: **0 errores y 0 avisos**. No se ha ejecutado en ninguna cuenta.

**Seguridad.**
- Se niega a correr si `ACCOUNT_TRADE_MODE` no es `ACCOUNT_TRADE_MODE_DEMO`, si EURUSD no existe o
  no admite operar, si el trading algorítmico está apagado o si la última cotización tiene más de
  dos minutos (mercado cerrado).
- Solo EURUSD, solo `SYMBOL_VOLUME_MIN`, número mágico propio (57057000).
- Toda pendiente lleva caducidad a 15 minutos si el símbolo la admite, y toda posición que abre a
  propósito lleva stop de protección: si el script se cortara a mitad, nada queda indefinido.
- `Limpiar()` borra toda pendiente y cierra toda posición con ese número mágico en EURUSD, con
  hasta cinco intentos, y cuenta lo que queda. Se llama **al empezar** (lo que quedara de una
  ejecución cortada), **después de los pasos 3, 4, 5 y 6**, **al terminar**, y también cuando un
  paso falla, porque el fallo corta la cadena y cae en la limpieza final. Cada limpieza deja una
  fila en el CSV con lo que queda; si queda algo, un aviso en pantalla dice que se cierre a mano.
- Cada orden de prueba se borra en cuanto se mide, y si una pendiente se llena al instante, su
  posición se cierra en el acto.
- Lo que no puede cubrir: un corte del propio MetaTrader en mitad de un paso. Para eso están la
  caducidad, el stop de protección y la limpieza al empezar la ejecución siguiente (runbook, paso 7).

**Lo que mide.** Una fila por medición en `MQL5/Files/MedirDemoFTMO_<fecha y hora del servidor>.csv`,
con la hora del servidor y la GMT en cada fila, y en la columna `responde` la decisión o la
ambigüedad a la que sirve:

| paso | mide | responde |
|---|---|---|
| 1 | stops level, freeze level, digits, point, contrato, volumen mínimo, máximo, paso y límite, modos de llenado, modo de ejecución, caducidades, swap largo y corto, modo de swap, día del triple swap; y de contexto: servidor, empresa, moneda, apalancamiento, modo de margen y build | A-27; ADR-0057 §5; FTMO-REGLAS R11 y R12 |
| 2 | `TimeCurrent`, `TimeTradeServer`, `TimeGMT`, `TimeLocal` y el desfase servidor-GMT en minutos | A-28 |
| 3 | sell stop por encima del bid, buy stop por debajo del ask, sell limit por debajo del bid y buy limit por encima del ask: retcode, si quedó colocada o se llenó, y a qué precio | ADR-0057 d2, d3 y d4 |
| 4 | las cuatro pendientes, del lado bueno, en el nivel exacto, a la distancia del stops level y 1 punto dentro (con stops level 0, las dos últimas son el nivel y 1 punto del lado equivocado) | ADR-0057 d2 y §5; A-27 |
| 5 | una sell stop y una buy limit válidas, modificadas a un precio del lado equivocado: retcode y si la original sigue viva y con su precio | ADR-0057 d3 |
| 6 | una compra y su cierre a mercado: `DEAL_COMMISSION` de cada lado, spread y deslizamiento de cada deal | FTMO-REGLAS R12; ADR-0057 d1 y DN-3 |
| 7 | una buy stop colocada tan cerca como deja el servidor: a qué precio se llena frente a su nivel (espera 120 s; si no salta, se borra) | ADR-0057 d1 |

**El paso 7 no estaba en el brief.** Lo añado porque la tabla del lector pide «cada decisión de
ADR-0057» y, sin él, la d1 -a qué precio se llena una stop- quedaría sin ninguna medida directa: el
paso 6 solo da el deslizamiento a mercado. Se apaga con la entrada `InpMedirLlenadoStop`.

**d4, la cotización con la que se juzga, solo se mide de forma indirecta:** cada fila guarda el bid
y el ask leídos justo antes de enviar, y el retcode dice qué hizo el servidor con ellos. Cuando el
nivel exacto y el punto de dentro den resultados distintos, la comparación sale de ahí.

**Dónde vive.** El brief pide `tools/mql5/`, y así va. El repositorio ya tiene `mql5/`, que
ADR-0001 y el árbol del MASTER_PLAN reservan para el bot en MetaTrader (`Params.mqh` generado,
`RunCases.mq5`, el tester): este script no es el bot ni lee la spec, es un instrumento de medida,
así que la separación tiene sentido. `tools/` y `tools/mql5/` llevan su README y entran en
`tests/unit/test_tree.py`, como toda carpeta del árbol.

## 2. Fase 2 · El lector, `scripts/leer_demo_ftmo.py`

Lee uno o varios CSV (o carpetas) y escribe una tabla con cada decisión de ADR-0057, A-27 y las
reglas de FTMO, una columna por fichero, y el desfase servidor-GMT por fecha para A-28. Un retcode
fuera de lo que cada medición puede devolver -colocada, hecha, precio inválido o stops inválidos-
**se marca INESPERADO en su celda y se lista aparte**: esa fila no mide lo que dice (por ejemplo, el
trading algorítmico apagado). También avisa si una limpieza dejó algo abierto o si falta la fila
del final (ejecución cortada). No escribe nada en el repositorio salvo la salida que se le pida.

**Tests** (`tests/unit/test_leer_demo_ftmo.py`, cinco, sobre CSV sintéticos con cifras inventadas
y años que no son de ningún material): la tabla de un fichero completo; **un retcode inesperado
(10027, trading algorítmico apagado) marcado en la celda y en la lista, sin ocultarse**; dos
ficheros con el desfase por fecha; lo que queda abierto y un corte avisados; y un CSV ajeno
rechazado.

**Ensayo de la CLI** en un `git worktree` desechable, sobre un CSV sintético con el formato de
fecha de MetaTrader (`2030.10.15 10:00:00`) y la salida fuera del repositorio: sale la tabla, la
limit del lado equivocado que se llena aparece con su precio, y un `MARKET_CLOSED` en el paso 3
sale marcado INESPERADO en su celda y en la lista.

## 3. Fase 3 · El runbook

`docs/runbooks/DEMO-FTMO.md`: la cuenta de prueba y MetaTrader, copiar, compilar y lanzar el
script, comprobar que no queda nada abierto, dónde queda el CSV y a dónde va, y las tres fechas:
antes del domingo 25 de octubre, entre el 26 y el 30, y después del domingo 1 de noviembre (Europa
cambia de hora el 25 y Nueva York el 1: la segunda ejecución dice qué calendario sigue el servidor).

**El CSV va a `data/demo_ftmo/`, ignorada por git.** Es el régimen de los datos medidos en bruto
-velas y ticks viven en `data/` fuera de git, y entra su manifiesto con el hash, inmutable, en
`data/manifests/`-. `knowledge/evidence/` es para items de evidencia del corpus con su esquema, no
para ficheros de una plataforma. La rama que use los CSV reales congelará su hash en un manifiesto
y citará desde ahí. El script no escribe el login de la cuenta.

## 4. Estado

Script, lector, tests, runbook e informe en un solo commit sellado. **Rama lista para revisión, NO
cerrada.**
