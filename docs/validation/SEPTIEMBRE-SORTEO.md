# El reparto de septiembre, fijado antes de ninguna etiqueta

Rama `trabajo/septiembre-sorteo`, desde `87c87cd` (tag `stable/F13-camino-de-fidelidad`). Sin tocar
main, sin merge, sin tag, sin push. **Nadie ha abierto nada** —ni el xlsx, ni una fila, ni las
capturas—; `PREREGISTRO.md` sigue vacío. `knowledge/spec/` sin tocar (12.1.1), `evidence/` y
`feedback/` tampoco.

## 1. La línea base

`kit check --sesion 2026-09-09-sesion-01` a un fichero antes de nada. **Resultado: salida IDÉNTICA**,
medida tras corregir la fecha y otra vez tras el sorteo.

## 2. La fecha del backtest: el 19, no el 20

`vistos.yaml` decía `visto_el: 2026-09-20`, que era la fecha de la **entrega** —la única con fuente
cuando se escribió, y así quedaba anotado en el propio fichero—. El trader ha dicho que lo
backtesteó el **2026-09-19**, así que hay dato real y la fecha de entrega deja de hacer de sustituta.

**La fuente se escribe tal cual**: es la declaración del consultor del 2026-09-21. Se buscó captura
en `corpus/.../Mensajes del trader/` y **no la hay** —esa carpeta sólo tiene
`mensaje-whatsapp-0208-zonas-de-control.png`, del 11 de septiembre y de otro tema—. Es más débil que
un fichero y por eso se dice, en vez de disfrazarla de algo más sólido.

**Y el 19 es sábado, y cuadra.** El material cubre hasta el viernes 18: es un backtest de fin de
semana sobre la semana recién cerrada. Queda dicho aquí y en `vistos.yaml` porque una fecha de
backtest en sábado es justo el dato que dentro de seis meses alguien lee como errata y «corrige».

**No mueve nada, medido antes de darlo por bueno**: el filtro compara `visto_el` con la fecha de la
**sesión**, y la sesión 1 es del 2026-09-09, anterior a las dos fechas. `kit check` idéntico, y
septiembre no lo ha sorteado ningún paquete del kit, así que no hay reproducción que romper. Va en su
propio commit (`96594b5`).

## 3. Lo que el reparto estrenaba, comprobado antes de sortear

| qué | resultado |
|---|---|
| `asignar` con cupo **0** en un nombre reservado | funciona; las particiones vacías **no aparecen** en la asignación |
| dos particiones vacías representables | sí — la decisión de dejarlas vacías no depende de una limitación del código |
| el test de la puerta (unión exacta) con cubos vacíos | sigue cierto, **y ahora por el motivo correcto** (§5) |

Y el universo real, medido antes de fijar nada: **14 días**. Los cupos suman 14 exactos, así que
**no sobra ninguno** — nadie se cae en silencio como les pasó a `2026-05-25` y `2026-06-29` en la
sesión 1.

## 4. El reparto

```
artefacto eurusd-2026-09 · seed 20260921 · universo 14 · 109 días excluidos
fidelidad-dev 4   ·  fidelidad-1 10  ·  fidelidad-2 0  ·  fidelidad-3 0
dev: 2026-09-01, 2026-09-04, 2026-09-17, 2026-09-18
```

Los 109 excluidos son los días laborables de enero, mayo, junio, julio y agosto, todos con el mismo
motivo: `sin material etiquetado del trader (<mes> no esta en cobertura_material)`. Es ruidoso y es
verdad: este camino existe para repartir material etiquetado.

**El argumento, que es lo que hay que poder reproducir; el número sólo es su consecuencia:**

**(a) Concentrar, y el motivo no es la potencia sino la tentación.** Ningún reparto llega a las 36
unidades efectivas, así que ninguna cifra será defendible se reparta como se reparta. Tres cubos de
~3 días no dan tres medidas: dan **tres cifras que se contradirán entre sí**, y eso invita a escoger
la que convenga. Un cubo da una cifra honesta, con su intervalo ancho y a la vista.

**(b) `fidelidad-2` y `fidelidad-3` vacías a propósito**, reservadas para material que pueda cargar
una cifra de verdad —febrero o marzo, el mes limpio que sigue pendiente—. Llenarlas hoy sería quemar
dos aperturas para no medir nada.

**(c) Sólo 4 `dev` porque mayo ya tiene seis sin abrir.** Los `dev` de septiembre no son el recurso
escaso: están para comprobar la ingesta y el formato contra un mes **distinto**, y para que el motor
no acabe afinado sólo sobre mayo. Cada `dev` de más sale de la reserva.

El seed es `20260921`, la fecha en que el reparto se fija, que es a lo que el seed tiene que estar
atado para que la anterioridad signifique algo.

## 5. El test de la puerta, reforzado otra vez

Afirmaba la **unión exacta** de los repartos de ambos caminos. Cierto — pero hasta hoy el camino de
fidelidad **no tenía ni un reservado**, así que la igualdad se cumplía por vacuidad por ese lado:
borrar su glob no la habría roto. Con el sorteo dentro ya se ejercita de verdad, y se añade la
afirmación que lo fija: **ninguno de los dos caminos puede aportar cero**. Si mañana alguien quita un
camino del glob de la puerta, el test lo dice.

## 6. Anclado en el mismo commit

`botsito fidelidad anclar --artefacto eurusd-2026-09` va en el commit que crea el artefacto
(`394a18e`): `particiones.yaml 03529e10…`, `ventanas.yaml cd92b2bd…`. Sin ancla, el artefacto
nacería con el agujero que se tapó el 2026-09-21.

La **anterioridad** queda ahora probada por dos piezas distintas: el ancla (inmutabilidad, desde ya)
y `cases/anterioridad.py` (anterioridad por caso, el día que exista la primera etiqueta). Hoy no
existe ninguna.

## 7. Lo que NO se ha hecho

- **Nadie ha abierto nada**, ni antes ni después del sorteo. Los `dev` se abren con su propio brief.
- Sigue en pie el freno de ADR-0036 §6: **antes de la primera autorización** hay que cerrar el
  agujero de `excluir` en `kappa_entre_sesiones`. No bloquea este sorteo; bloquea abrir.
- Sigue en pie la cita con el problema de re-descargar un mes: la descarga nos ata al rango
  2026-09-01..20.

## 8. Qué debe decidir el usuario

Validar la rama. Y después, lo que queda pendiente de verdad: **pedirle al trader un mes que no haya
tocado** (febrero o marzo), que es lo único que puede llenar `fidelidad-2` con una cifra defendible.

## 9. Cómo comprobarlo

```
uv run botsito kit check --sesion 2026-09-09-sesion-01        # identico a la linea base
uv run botsito fidelidad check --artefacto eurusd-2026-09     # se recompone igual
uv run botsito knowledge validate                              # exit 0, "1 artefactos de fidelidad"
uv run pytest tests/unit/test_puerta_holdout.py tests/contract/test_anterioridad.py -q
make check > make-check.log 2>&1; echo "exit=$?"
```

## Estado
WAITING_FOR_USER_VALIDATION
