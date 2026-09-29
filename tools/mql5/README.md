# tools/mql5/
Scripts de MetaTrader 5 para medir en una cuenta DEMO; se copian a `MQL5/Scripts` del terminal y se
compilan alli (el `.ex5` no se versiona).

- `MedirDemoFTMO.mq5` · mide en la prueba gratuita de FTMO lo que ADR-0057, A-27 y A-28 dejaron
  pendiente y escribe un CSV en `MQL5/Files`. Se niega fuera de una cuenta DEMO y no deja nada
  abierto. Como se ejecuta: `docs/runbooks/DEMO-FTMO.md`; como se lee: `scripts/leer_demo_ftmo.py`.
