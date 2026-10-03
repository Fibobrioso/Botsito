# runbooks/
Operacion en demo y real (F33): arranque, pre-vuelo, incidentes, kill-switch. Vacio hasta F33.

- `RITUAL.md` · el ritual de cierre de una rama, con sus puertas. Desde el 2026-09-26 lo ejecuta
  Claude Code solo ante una orden de cierre explicita de Aleks; desde el 2026-10-01, con la skill
  `cerrar-rama`.
- `MIRAR-EL-MATERIAL.md` · como se abre un fotograma (por instante localizado), donde esta el texto
  de cada transcripcion, el reloj de FX Replay (UTC+2 fijo) y por que cambio tres veces la regla de
  lo que se puede mirar. Mudado de `CLAUDE.md` el 2026-10-01.
- `AMBIGUEDADES.md` · que toca abrir, editar y cerrar una ambiguedad. Mudado de `CLAUDE.md` el
  2026-10-01.
- `ENTRADA-MARZO.md` · como entra el backtest de marzo por el camino de fidelidad (ADR-0046 §6):
  comandos, salida esperada y las paradas de la sesion. Ensayado en
  `tests/contract/test_ensayo_marzo.py`.
- `SESION-DE-PREGUNTAS.md` · una sesion solo de preguntas con el trader, sin kit ni casos: antes,
  durante y despues, con sus cuatro reglas y como entran las respuestas. Escrito para la sesion 02.
- `ARNES-MOTOR.md` · corre el motor sobre construccion y lee su informe: criterio de fidelidad,
  embudo sobre el grafo de hechos y negativas (ADR-0048).
- `DEMO-FTMO.md` · para Aleks: ejecutar `tools/mql5/MedirDemoFTMO.mq5` en la prueba gratuita de
  FTMO, sin jerga, y a donde va su CSV (`data/demo_ftmo/`); tres veces, alrededor del cambio de hora
  de octubre. Se lee con `scripts/leer_demo_ftmo.py`.
- `CONTRATO-DE-RAMA.md` · el `contrato.yaml` de una rama de trabajo: rutas permitidas y
  protegidas, comprobaciones, riesgo y el informe esperado; lo comprueba `make check`. Con la
  plantilla y tres ejemplos.
- `ERRORES-RECURRENTES.md` · los errores que ya se conocen (patron, senal y que hacer), los cinco
  patrones de defecto, y por rama cuantos hallazgos encontro el subagente revisor y cuantos encontro
  despues el consultor; el segundo numero debe tender a cero.
- `VISOR-DIAS.md` · el visor de dias de construccion: una pagina por dia con las velas, lo que
  hizo el trader, lo que hizo el bot y por que, para depurar una regla nueva. La salida no se
  comitea.
- `RENOVAR-CIERRES.md` · cuando y como se renueva el calendario de cierres de FTMO
  (`knowledge/cuentas/cierres/`): por condicion, no cada semana; quien, de donde sale el dato y que
  bloquea la rama que conecte el bot en tiempo real.
