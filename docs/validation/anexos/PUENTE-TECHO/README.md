# anexos/PUENTE-TECHO · El puente del techo de ADR-0099

Rama `trabajo/puente-techo` (`docs/validation/PUENTE-TECHO.md`). Pre-registrado en `613aa40c`
(ADR-0099 y `docs/plan/PUENTE-TECHO.yaml`, fijado por `tests/unit/test_puente_techo.py`) antes de que
existiera ningún fichero de esta carpeta. Este README entra en su propio commit antes de la primera
corrida (encargo, fase 1).

## Qué es cada fichero

- `puente.py`: el guion del puente. Carga de `main`, por su ruta y sin copiarlo,
  `anexos/RECORRIDA-CONSTRUCCION-3/techo_parejas.py` (el entorno, las piezas puras, el dimensionado,
  la medida y los formatos) y reescribe con un interruptor por pieza el bucle del día, los pedidos,
  el predicado de RN-002 y las filas de las posiciones abiertas con `abrir_conocida`. Lee
  `PUENTE-TECHO.yaml`, `META-TECHO-PAREJAS.yaml` y `knowledge/cases/criterio_fidelidad.yaml`; no
  lleva ninguna cifra de ellos dentro. Cuatro modos: `control` (D2 a: el control de ADR-0098 §1 con
  el bucle nuevo), `conocida` (D2 c sobre los días dev), `variante <nombre>` y `todo` (las dieciséis
  en el orden del yaml, con la lectura del puente al final). Todos corren antes el control y salen
  con 4 si no pasa.
- `test_puente.py`: su test de humo, sobre datos sintéticos (fechas de 2030), en los dos sentidos.
  `make check` no lo recoge (`testpaths = ["tests"]`).
- `control.txt`: la salida de `puente.py control` (D2 a).
- `conocida.txt`: la salida de `puente.py conocida` (D2 c).
- `base.txt` y `base-repetida.txt`: la variante `base` dos veces (D2 b y D9).
- `<nombre>.txt`: la salida de cada variante, con el nombre que le da el guion.
- `lectura.txt`: la lectura del puente (D6) y el cierre (D7).

## Comandos (desde la raíz; una corrida a la vez, nunca a la par de un `make check`)

```
uv run pytest docs/validation/anexos/PUENTE-TECHO/test_puente.py -p no:cacheprovider
uv run python -B docs/validation/anexos/PUENTE-TECHO/puente.py control docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/cuenta-por-mes.txt > docs/validation/anexos/PUENTE-TECHO/control.txt
uv run python -B docs/validation/anexos/PUENTE-TECHO/puente.py conocida docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/cuenta-por-mes.txt > docs/validation/anexos/PUENTE-TECHO/conocida.txt
uv run python -B docs/validation/anexos/PUENTE-TECHO/puente.py variante base docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/cuenta-por-mes.txt > docs/validation/anexos/PUENTE-TECHO/base.txt
uv run python -B docs/validation/anexos/PUENTE-TECHO/puente.py variante <nombre> docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/cuenta-por-mes.txt > docs/validation/anexos/PUENTE-TECHO/<nombre>.txt
uv run python -B docs/validation/anexos/PUENTE-TECHO/puente.py todo docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/cuenta-por-mes.txt
```

D2 b compara el bloque M1 de `base.txt` con el de `anexos/RECORRIDA-CONSTRUCCION-3/meta.txt` (desde
«## M1 · El techo» hasta la línea anterior a «## M2 · Las parejas») con `diff`; D9, `base.txt` con
`base-repetida.txt`, byte a byte. Los comandos ejecutados, con su hora y su salida, en el informe.

## Lo que no imprime

Ninguna operación con su R, ningún R por clase de setup, por sesión ni por dirección (ADR-0098 §4 c;
ADR-0099 §2), ningún precio, ninguna vela, ningún nivel y nada anterior al día dev al que pertenece.
Por mes, solo d), e) y f) por cuenta y el subtotal de abril y agosto; el bloque de julio, solo en
`base` (es el bloque M1 de `meta.txt`). Las cifras son diagnóstico de construcción (ADR-0092 §6,
recuadro de ADR-0099): ninguna fija ni cambia un valor.
