# tools/mql5/
Scripts de MetaTrader 5 para medir en una cuenta DEMO; se copian a `MQL5/Scripts` del terminal y se
compilan alli (el `.ex5` no se versiona).

- `MedirDemoFTMO.mq5` · mide en la prueba gratuita de FTMO lo que ADR-0057, A-27 y A-28 dejaron
  pendiente y, desde la 1.2 (paso 8), cuándo comprueba MT5 el margen de una pendiente stop
  (ADR-0081 §4); escribe un CSV en `MQL5/Files`. Se niega fuera de una cuenta DEMO y no deja nada
  abierto. Como se ejecuta: `docs/runbooks/DEMO-FTMO.md`; como se lee: `scripts/leer_demo_ftmo.py`.
- `ExportarTicksFTMO.mq5` · F17, primera parte (ADR-0099 §5; rama `trabajo/f17-historial`): exporta
  el historial de ticks de EURUSD que el servidor de la demo de FTMO ya guarda, un CSV por dia con
  la M1 del servidor y uno de control con los relojes, en `MQL5/Files` con el prefijo `F17_`. SOLO
  LEE: no llama a ninguna funcion de trading (`tests/contract/test_exportar_ticks_ftmo.py`), se
  niega fuera de una cuenta DEMO y a cualquier dia que no sea de un mes de construccion. Se compila
  con `compilar.py herramienta` (un camino aparte del de la capa) y se instala en
  `MQL5/Scripts/Botsito`. Como se ejecuta: `docs/runbooks/F17-HISTORIAL.md`; como se lee:
  `scripts/leer_historial_f17.py`.
