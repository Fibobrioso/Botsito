# runbooks/
Operacion en demo y real (F33): arranque, pre-vuelo, incidentes, kill-switch. Vacio hasta F33.

- `RITUAL.md` · el ritual de cierre de una rama, con sus puertas. Lo ejecuta el usuario; la
  sesion no hace merge, ni tag, ni push.
- `ENTRADA-MARZO.md` · como entra el backtest de marzo por el camino de fidelidad (ADR-0046 §6):
  comandos, salida esperada y las paradas de la sesion. Ensayado en
  `tests/contract/test_ensayo_marzo.py`.
- `SESION-DE-PREGUNTAS.md` · una sesion solo de preguntas con el trader, sin kit ni casos: antes,
  durante y despues, con sus cuatro reglas y como entran las respuestas. Escrito para la sesion 02.
