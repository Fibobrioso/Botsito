# FUNCTIONALITY VALIDATION REPORT · Renovar el calendario de cierres

Rama `trabajo/renovar-cierres`, abierta el 2026-10-03 desde `main` `60d540c` (último `stable/*`:
`stable/F36r-fuentes-ftmo`, que apunta al merge `36a9801`; comprobado antes de abrir). Encargo,
copiado tal cual: `docs/encargos/trabajo-renovar-cierres.md`.

Objetivo: que el calendario de cierres (`knowledge/cuentas/cierres/ftmo-2step-swing-100k.yaml`, hoy
con `hasta: "2026-10-07"`) no caduque sin que nadie lo vea, y dejar escrito quién lo renueva y
cuándo.

## 0. Fase 0 · Inventario, sin tocar nada

Todo se midió **fuera del repositorio**, en un clon local desechable
(`git clone --no-hardlinks` en la carpeta de trabajo). El clon no tiene los hooks del repositorio,
así que admite commits y tags de ensayo en su `main`. `data/` se le apunta por
`config/settings.local.toml`, sin copiarlo. En el repositorio no se escribió nada. Las salidas del
arnés no se leyeron: solo el código de salida, los `ERROR` y lo que dice el cable trampa del reloj
(abajo).

### 0.1 Qué hace el código cuando el calendario ha caducado

**Lo que se niega depende del INSTANTE SIMULADO, no de la fecha de hoy.**

**1. Ningún camino de los cierres lee el reloj de pared.** En `src/botsito/` solo lo leen:
- `cli.py:904` y `cli.py:1046`, para la marca `generado_el` y las marcas de tiempo;
- `cli.py:2333`, `cli.py:2420`, `cli.py:2446` y `cli.py:2541`, para cronometrar el arnés;
- `cli.py:2590` y `cli.py:2712`, para el `hoy` de una descarga de datos;
- `corpus/fotogramas.py:577` y `corpus/pipeline_transcripcion.py:221`, para la marca de un
  manifiesto.

Ninguno está en `domain/cierres.py`, `engine/calendario_cierres.py`, `engine/broker.py`,
`engine/cableado.py` ni `engine/simulacion.py`. `date.today` no aparece en `src/`.

**2. El cable trampa.** Para no fiarse solo de la lectura, un `sitecustomize` en la carpeta de
trabajo anota cada llamada a `datetime.now`, `datetime.utcnow`, `datetime.today`, `time.time` y
`time.gmtime()` que salga de código de `botsito`: el módulo que llama de inmediato y la línea de
`botsito` en la pila. No cubre `date.today`, porque cambiar esa clase rompe `isinstance`; en `src/`
no se usa. Con `RELOJ_DESFASE_DIAS`, además, adelanta ese reloj N días para todo el proceso: es la
fecha inyectada, sin tocar el reloj del sistema.

**3. El predicado, con instantes inyectados**, contra el calendario real del repositorio:

```
$ uv run python <carpeta de trabajo>/medir_predicado.py
cubre: 2025-12-04 05:00:00.000 UTC -> 2026-10-08 04:00:00.000 UTC (exclusivo)
dia de construccion (14-4-2026 08:00 UTC)    2026-04-14 08:00:00.000 UTC -> se puede
viernes 25-9, ventana de R15                 2026-09-25 19:00:00.000 UTC -> cierre_mercado
miercoles 7-10, 12:00 UTC (futuro, dentro)   2026-10-07 12:00:00.000 UTC -> se puede
ultimo ms cubierto                           2026-10-08 03:59:59.999 UTC -> se puede
primer ms sin cubrir (jueves 8-10)           2026-10-08 04:00:00.000 UTC -> cierre_sin_calendario
jueves 8-10, 07:00 Madrid = 05:00 UTC        2026-10-08 05:00:00.000 UTC -> cierre_sin_calendario
antes de lo cubierto (1-12-2025)             2025-12-01 12:00:00.000 UTC -> cierre_sin_calendario
exit=0
```

Medido el 2026-10-03: el 7-10, un día que todavía no ha llegado, «se puede», y el 1-12-2025, que ya
pasó, se niega. Lo que cuenta es el instante que recibe el predicado.

**4. El arnés sobre los días de construcción, con tres calendarios**, en el clon. Las lecturas en
DIAGNÓSTICO son las de `CONTADOR-PETICIONES.md` §4, porque sin A-35 el motor se niega. Cada línea, tal
como se ejecutó:

```
$ uv run --frozen botsito motor arnes --simular --diagnostico-a35 cierre_vela_contraria --diagnostico-a44 sin_tope --diagnostico-a21 solo_una_zona_de_control --diagnostico-a27 0 --salida <carpeta de trabajo>/arnes-<X>.txt
```

| Calendario | `hasta` | Respecto a hoy (3-10) | exit | Lo que dice |
|---|---|---|---|---|
| A | 2026-09-01 | **ya caducado** | **0** | `OK: informe del arnes en …` |
| B | 2026-08-15 | caducado, y antes del último día de construcción | **2** | `ERROR: dias fuera del calendario de cierres de ftmo-2step-swing-100k (ADR-0068): ['2026-08-17', '2026-08-18', '2026-08-19', '2026-08-20', '2026-08-21', '2026-08-24', '2026-08-25', '2026-08-26', '2026-08-27', '2026-08-28', '2026-08-31']; se alarga `cubre` revisando las Trading Updates de esas semanas` |
| C (el real) | 2026-10-07 | vigente | **0** | `OK: informe del arnes en …` |

El cable trampa, en las tres, anota una sola llamada: `time.time pedido por logging, desde
botsito.engine.broker:55`. La línea 55 del `broker.py` del clon es `import logging`: al cargarse,
`logging` apunta su hora de arranque. No decide nada. En los tests de cierres sale otra igual: la
hora que `logging` pone al registro del `LOG.info` de `broker.py:333`.

**Respuestas a las tres preguntas del encargo:**

| Pregunta | Respuesta medida |
|---|---|
| ¿Lo que se niega depende de la fecha simulada o de la de hoy? | **De la simulada.** El predicado decide con el instante que le pasa el broker, y el cableado compara los días pedidos con `cubre`. El calendario A, caducado respecto a hoy, deja correr toda la construcción |
| ¿Se rompe una simulación sobre días históricos de construcción a partir del 8 de octubre? | **No.** Los días de construcción (1-4 a 31-8-2026) están dentro de `cubre` sea cual sea la fecha de hoy. Solo se negaría a correr un día posterior a `hasta` (como B con agosto) |
| ¿Se rompe algún test o la CI? | **No por la fecha.** La suite entera, en el clon y con el reloj adelantado 10 días (al 13-10, `RELOJ_DESFASE_DIAS=10`), da 1855 pasados, 2 fallos y 3 saltados, que suman los 1860 del repositorio. Los 2 fallos son del clon: `test_no_unexpected_ignored_paths` ve el `config/settings.local.toml` que se le puso, y `test_rutas_windows` ve la ruta larga de la carpeta de trabajo. Los dos fallan igual SIN adelantar el reloj (abajo). Los 3 saltados también son del clon: el contrato (en `main` no hay), `test_fidelidad_marzo` sin `data/` propio y `tokenizers`, que no está en su entorno |

Los comandos de la suite, tal como se ejecutaron en el clon:

```
$ PYTHONPATH=<carpeta de trabajo>/tripwire RELOJ_DESFASE_DIAS=10 RELOJ_LOG=<carpeta de trabajo>/reloj-suite.log uv run --frozen pytest -q -p no:cacheprovider
exit=1
FAILED tests/contract/test_repository_integrity.py::test_no_unexpected_ignored_paths
FAILED tests/unit/test_rutas_windows.py::test_las_rutas_por_defecto_con_el_rotulo_mas_largo_caben_en_este_repo
$ uv run --frozen pytest tests/contract/test_repository_integrity.py::test_no_unexpected_ignored_paths tests/unit/test_rutas_windows.py::test_las_rutas_por_defecto_con_el_rotulo_mas_largo_caben_en_este_repo -q -p no:cacheprovider   # SIN desfase
E       AssertionError: rutas ignoradas no previstas: ['config/settings.local.toml']
E           assert 270 <= 259
```

En esa suite, el cable trampa anota quién pidió el reloj. Desde los cierres, nadie. Desde otros
sitios:
- `logging`, para la hora de cada registro (`engine/freno.py` y `engine/broker.py:333`);
- `zipfile`, al escribir la hoja `.docx`;
- las marcas `generado_el` de `corpus/` y `cli.py`, y el `hoy` de una descarga.

**Lo que sí deja de funcionar al caducar: el bot EN VIVO, cuando exista.** Su instante será el de
ahora. Desde el 2026-10-08 a las 04:00 UTC (las 06:00 de Madrid del jueves):
- negaría toda colocación y toda modificación (`cierre_sin_calendario`);
- cancelaría las pendientes al cruzar ese instante (`proxima_prohibicion` incluye el fin de `cubre`);
- dejaría seguir las posiciones (R7).

Hoy no hay adaptador en vivo (ADR-0068 §4), así que el impacto hoy es cero. Lo mismo valdría para
simular un día de octubre en adelante, cuando haya velas: el cableado se negaría hasta renovar.

### 0.2 Qué fuente cubre la semana del 4 al 10 de octubre y la siguiente

**Lo que dice la fuente**, consultada el 2026-10-03 entre las 16:16 y las 16:18 UTC:

- **Trading Updates** (`https://ftmo.com/en/blog/trading-updates/`). La última publicada es la del
  1-10-2026 (`trading-update-1-oct-2026`, leída el 2026-10-03 hacia las 01:00 UTC en
  `trabajo/fuentes-ftmo`). Trae el festivo de Hong Kong del 1-10 (HK50.cash) y el cambio de hora de
  Australia del 4-10 (AUS200.cash), y **nada del Forex**. A las 16:17 UTC, las de los días 2, 7 y
  8-10-2026 dan **HTTP 404**: todavía no existen. El listado `https://ftmo.com/en/trading-updates/`
  enlaza hasta la del 24-9.
- **API de símbolos** (`https://ftmo.com/wp-json/ftmo/symbols`, leída a las 16:16 UTC, sha256
  `3ea78a30d145daa3…`). `tradingHours` de EUR/USD sigue trayendo la semana del 27-9 al 2-10: hoy es
  sábado y aún no se ha pasado a la nueva. `platformTimeOffset: {"UTC": 3, "Europe/Prague": 1}`.
- **La pauta ya declarada** en el calendario: viernes 16:55 a domingo 17:05 y corte diario
  16:55-17:05, de Nueva York (`trabajo/fuentes-ftmo` y `feature/cierres-de-mercado` §0.2).

**Lo que se supone y NO se escribe en el calendario sin fuente:**
- el lunes 12-10-2026 es Columbus Day en EE. UU. El Forex suele cotizar ese día, pero FTMO no ha
  publicado nada para esa semana;
- no hay cambio de hora en Europa ni en EE. UU. esas dos semanas (Europa el 25-10, EE. UU. el 1-11).

**Conclusión: la fuente cubre hasta el 7-10, que es el `hasta` actual, y nada más.** La semana del
8 al 14 necesita la Trading Update del 8-10, que todavía no existe. Hoy no se puede renovar ni un
día. La Fase 1 renueva cuando esa actualización salga.

**Cuándo publica FTMO**, medido en las 43 Trading Updates ya descargadas (`article:published_time`
de cada página): 26 un jueves (entre las 07:25 y las 13:14 UTC), 13 un miércoles, 2 un martes, 1 un
lunes y 1 un domingo. **Esto deja un hueco casi cada semana.** `cubre` acaba el miércoles (a las
04:00 UTC del jueves), y en la mayoría de semanas la actualización llega el jueves por la mañana: en
vivo, la operativa del jueves (desde las 07:00 de Madrid) quedaría negada hasta renovar.

### 0.3 El procedimiento más ligero que cumple el ritual

**Medido en el clon que tocar el YAML en `main` exige un tag nuevo** (regla 5 de `state check`,
`cli.py:149-157`: en `main`, `git diff --name-only <último tag>..HEAD` solo puede traer
`PROJECT_STATE.md`):

```
$ uv run --frozen botsito state check                      # main recién clonado
OK: rama 'main' - funcionalidad actual: NINGUNA ABIERTA tras `stable/F36r-fuentes-ftmo` (2026-10-03).
# hasta: "2026-10-07" -> "2026-10-14", commit en main SIN tag
$ uv run --frozen botsito state check
ERROR: main tiene cambios sin tag estable desde stable/F36r-fuentes-ftmo: knowledge/cuentas/cierres/ftmo-2step-swing-100k.yaml (en main, tras el tag, solo puede cambiar PROJECT_STATE.md; el HANDOFF y cualquier otro fichero entran por una rama con su tag: MASTER_PLAN §F)
exit=1
# tag stable/F99-ensayo en ese commit, Last Stable Commit apuntando a él, commit de PROJECT_STATE
$ uv run --frozen botsito state check
OK: rama 'main' - funcionalidad actual: NINGUNA ABIERTA tras `stable/F36r-fuentes-ftmo` (2026-10-03).
exit=0
```

**Lo que exige `state check` es el TAG, no la rama.** La rama la exige otra cosa: el hook
`pre-commit` rechaza un commit directo en `main` sin `BOTSITO_ALLOW_MAIN=1`
(`scripts/git-hooks/pre-commit:17`), y esa variable solo la usa el ritual (`CLAUDE.md`, «main no se
toca»). Con las reglas de hoy, **cada renovación es un cierre completo**:
- una rama con encargo, contrato y Archivo;
- el commit del YAML y un informe;
- el revisor;
- la orden de cierre;
- el merge, el tag y el commit de estado;
- tres o cuatro `make check`, de unos 11 minutos cada uno.

**Propuesta, para que decida el consultor:**

| | Opción A: rama propia cada semana | Opción B (recomendada): a lomos de la rama de esa semana |
|---|---|---|
| Qué | `trabajo/renovar-cierres-AAAA-MM-DD`, con un informe corto y el ritual entero | la renovación entra como un commit más en la rama que esté abierta esa semana (su contrato admite el YAML), con su fuente en el informe de esa rama; solo si no hay ninguna, la opción A |
| Coste | dos órdenes de Aleks (abrir y cerrar) y unos 45 minutos de `make check` cada semana | un commit y unas líneas de informe; el cierre ya lo paga la otra rama |
| Riesgo | ninguno nuevo | la renovación espera al cierre de esa rama: si se alarga más allá del miércoles, hace falta la A |

**Quién:** Claude Code, con orden de Aleks (la de abrir, o la de la rama a la que se sube).

**Qué día:** el jueves, en cuanto salga la Trading Update (el miércoles si sale antes): se lee, se
apuntan los cierres del Forex que traiga y `hasta` pasa al miércoles siguiente, nunca más allá.

**El hueco del jueves por la mañana** (§0.2) no se cierra renovando antes, porque no hay fuente. Hay
dos salidas, y las dos son del consultor:
- aceptarlo: hoy no hay bot en vivo, y en el simulador no cuenta;
- o, antes de operar en real, que el adaptador en vivo use las sesiones de MT5 como segunda fuente
  (ADR-0068 §4), que es lo que la línea N ya pide automatizar.

**El aviso previo**, en `state check`, que corre al empezar cada sesión y dentro de cada
`make check`:
- **AVISO** cuando falten 3 días o menos para `hasta`, con la fecha y el puntero al runbook. No
  bloquea;
- **calendario caducado** (hoy > `hasta`): el encargo pide que falle. Hay dos maneras, y el
  consultor elige:
  - **ERROR en `state check`.** `make check` sale en rojo y no sella en ninguna rama hasta renovar,
    y la CI de `main` sale roja en el primer push después de caducar. Obliga a renovar, pero mete la
    fecha de hoy en `make check`: el mismo árbol pasa hoy y falla mañana. Y con el hueco del jueves,
    fallaría casi cada jueves por la mañana;
  - **ERROR solo en un comando propio** (`uv run botsito cierres check`, exit 1 si ha caducado),
    que el runbook manda correr al empezar cada sesión. `state check` y la CI quedan como están, y
    `state check` solo avisa (AVISO también cuando ha caducado).

  Recomiendo la segunda. La fecha de hoy fuera de `make check` mantiene el sello reproducible, y el
  aviso de 3 días ya hace visible la caducidad a cada sesión. En las dos, los tests inyectan `hoy`.

**Tests de la Fase 1** (los que pide el encargo), con `hoy` inyectado:
- un calendario caducado falla, y pasa sin el defecto;
- uno a 3 días avisa, y a 4 no;
- con la guardia rota a propósito, los tests fallan.

## Estado

FASE 0 ENTREGADA: falta el visto bueno del consultor para la Fase 1, que depende de dos cosas:
- la opción A o B de §0.3, y cómo falla el calendario caducado;
- que salga la Trading Update del 8-10, para poder renovar.
