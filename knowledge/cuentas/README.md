# knowledge/cuentas/

Los perfiles de cuenta del simulador (ADR-0050). Un perfil es UNA firma, UN programa, UN tipo de
cuenta y UN capital, en un fichero con el formato del registro (`knowledge/spec/parametros.yaml`,
ADR-0002 y ADR-0012) que lee `config.registro.cargar_registro` por la misma puerta, con los mismos
tipos y los mismos tres estados. Lo carga `src/botsito/engine/perfil_cuenta.py` y lo ejecuta la
capa de cuenta, `src/botsito/engine/cuenta.py`.

- **Una firma nueva es un fichero nuevo aqui, nunca codigo nuevo.** El motor no contiene ninguna
  cifra ni ningun nombre de firma; `tests/fixtures/cuentas/sintetica-una-fase-50k.yaml` es un
  perfil INVENTADO que lo demuestra en los tests.
- **Cada cifra cita su regla** de `docs/validation/FTMO-REGLAS.md` (R1..R20) en su descripcion, y
  la fuente formal es el ADR que la adopta. Lo que la fuente oficial no dice va en `UNKNOWN`: no
  tiene valor, leerlo falla nombrando el parametro, y el simulador se niega a correr si lo
  necesita para decidir. Ningun valor se inventa.
- **Un nombre que coincide con `parametros.yaml` lleva el mismo valor**, y un test lo cruza
  (precedente: ADR-0012 §1). La spec sigue leyendo `parametros.yaml`; los perfiles los lee solo el
  simulador.

| Fichero | Perfil |
|---|---|
| `ftmo-2step-swing-100k.yaml` | FTMO, programa 2-Step, tipo Swing, 100.000 USD (ADR-0026, FTMO-REGLAS) |

Regimen de cambio: versionado; cada commit que toque un perfil cita en su mensaje la regla o el
ADR de donde sale el valor.
