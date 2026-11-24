# PUENTE-TECHO · El puente del techo pieza a pieza, pre-registrado antes de correr (R4.7, entrada F)

> PLANTILLA hasta la fase 0: el inventario lo escribe la fase 0 (skill fase-cero) en su commit.

Rama `trabajo/puente-techo`, abierta el 2026-11-23 desde `main` en 8a10590b (commit de estado sobre
el merge 88f678f7 del tag `stable/F39l-recorrida-construccion-3`). Encargo:
`docs/encargos/trabajo-puente-techo.md`. Tramo: R4 (R4.7 de `docs/plan/HOJA-DE-RUTA.md`, lo que la
salida C de ADR-0098 pide antes de seguir; la F de la Next Action). El ADR del puente lo escribe la
fase P, a partir del borrador del ADR que trae Aleks. Tag previsto: `stable/F39m-puente-techo` (no
existe ni en local ni en origin: `git tag -l "stable/F39m*"` y `git ls-remote --tags origin
"stable/F39m*"` vacíos).

## Base comprobada (abrir-rama, paso 1)

- `git rev-parse main origin/main`: `8a10590b485ee3867426bf6dce6d08601e22d13b` dos veces; `git status --short` vacío.
- `git rev-parse "stable/F39l-recorrida-construccion-3^{commit}"` = `88f678f717554cc01c79209802d40b5252015c28` = `git rev-parse main^1`; en origin: `git ls-remote --tags origin stable/F39l-recorrida-construccion-3` da `ccb1f1d1…` (el objeto del tag anotado).
- CI de `main`: `gh run view 45107787390` (suelto, sin guion) → `✓ main ci`, job `python` en 9m7s; con `--json`: `status: completed`, `conclusion: success`, `event: push`, `headBranch: main`, `headSha: 8a10590b485ee3867426bf6dce6d08601e22d13b`. Es el run que dio el informe de cierre.
- `git branch -a` solo daba `main` (y `origin/main`); `git ls-remote --heads origin` solo da `refs/heads/main`.
- Sesión en Opus 5.5 (el esfuerzo no se ve desde la sesión; lo confirma Aleks); `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1` puesta (medido con `echo`): las corridas pueden ir en segundo plano.

## Los cuatro ficheros del Escritorio (sha256 medidos con `sha256sum`)

| Fichero | Bytes | sha256 medido | ¿Coincide con el del consultor? |
|---|---|---|---|
| `AUDITORIA-PROFUNDA-2026-11.md` | 271.910 | `542ee81011e9d82402d6c274bea3ffdfdaa886685fce24811ff146eaead01263` | sí |
| `auditoria-cazador-trabajo/INFORME-CAZADOR-2026-11-23.md` | 29.039 | `3a228954dcc81ed886add70f0aeb0702908e6593549c7b6f653043c459e1164a` | sí |
| el borrador del ADR | 19.965 | `aa4e95ff87144f4b748951fe6de16c68a1cb5950673b9815053eebd8bf58200b` | sí, en la segunda medida (abajo) |
| `PUENTE-TECHO.yaml` | 5.154 | `31e70e0a89db3f5b7c1500d7698f450f6d7d3f3659972ef5443ad383b524cfbf` | sí |

## Desviaciones de la apertura

- **PARADA antes de abrir por el borrador del ADR.** La primera medida dio 18.215 bytes y
  `26c81a4ecb12e9da5f84936e65c25a3cedc8c6d9b98c2d743951fa92c3caadb0` (LF, sin BOM; tampoco
  coincidía con CRLF, sin el salto final ni con uno de más). Se paró sin tocar nada ni leer su texto.
  Respuesta del consultor (2026-11-23): era una versión anterior; Aleks dejó la buena (19.965 bytes),
  cuyo sha coincide. Solo entonces se abrió la rama.
- **La fila de HOLDOUT-EXPOSICIONES del día** se escribió y estadió tras crear la rama y antes de
  cualquier otra escritura, lectura de material o `make check`. Su punto (8) se corrigió, aún
  estadiada y antes del primer `make check`, tras leer la auditoría profunda: el encargo dice que las
  dos auditorías leyeron «solo ficheros commiteados», y su eje P5 corrió `kb find`, que también recorre
  las transcripciones por la vía filtrada de la CLI (`src/botsito/retrieval/consultas.py:90-97`). Gana
  lo medido; la fila lo dice con su nombre. No es material reservado (CLAUDE.md, punto 1).
- **Los cuatro ficheros se leyeron enteros antes de usarlos.** Fechas, con un guion de la carpeta de
  trabajo que no imprime ninguna: 115 fechas en la auditoría profunda, 18 de ellas coinciden con un
  día de un caso reservado; todas son fechas de sucesos del repo dentro de nombres de fichero o ids ya
  commiteados en `main` (`SESION-01-<fecha>.md`, `fb-<fecha>-sesion-01-*`,
  `A-16-proveedor-de-datos-<fecha>.md`, `AUDITORIA-<fecha>-ultracode.md`) o la del primer commit del
  proyecto, y la propia auditoría las clasifica como legítimas en su §14, Parte 3. En el «cazador»,
  el borrador del ADR y el yaml, 0 coincidencias. Ningún resultado sin publicar: la aritmética va
  marcada como tal y la media de un subconjunto que se había colado se retiró allí (§14 y §15 de la
  auditoría profunda).

- **El primer `make check` de la apertura salió en rojo por algo mío** (1 failed, 3611 passed, 28:37):
  `tests/contract/test_repository_integrity.py::test_no_unexpected_ignored_paths` encontró
  `.claude/scheduled_tasks.lock`, el bloqueo del planificador de la sesión de Claude Code, creado a
  las 21:16 al programar con `ScheduleWakeup` un respaldo por si no llegaba el aviso del `make check`.
  Se cancelaron los respaldos pendientes, se borró ese fichero (sin seguir por git; no es del repo) y
  se repitió el `make check`. En esta rama no se vuelve a usar `ScheduleWakeup`: el aviso de las
  tareas de fondo basta. Fila preparada para ERRORES-RECURRENTES (§6).

## §0 · Las decisiones del consultor, la fase A, la fase P y la fase 0

### §0.1 Las decisiones del consultor (D1 a D12, 2026-11-23)

Las doce, tal cual, en el encargo (`docs/encargos/trabajo-puente-techo.md`, «DECISIONES DEL
CONSULTOR»). Cómo quedan frente a lo medido en la fase 0 (§0.4):

| D | En una línea | Frente a lo medido |
|---|---|---|
| D1 | el guion en anexos/PUENTE-TECHO, reutilizando `techo_parejas.py` de `main` cargado por su ruta; bucle, pedidos y la medida de `abrir_conocida` reescritos con interruptores | cuadra; el aviso del auditor del encargo es cierto (b.3): sin cálculo propio, `abrir_conocida` daría cero filas |
| D2 | dos controles (el del bot, 235 de 235; la base contra `meta.txt`) más el de `abrir_conocida` | cuadra: los tres caben (a, b.3) |
| D3 | las diez piezas | cuadran las diez sin tocar `src/` (b) |
| D4 | dieciséis variantes, las del yaml | cuadra (el yaml, leído con el lector estricto: 1 + 8 + 1 + 4 + 2) |
| D5 | lo que imprime cada variante | cuadra (c, d) |
| D6 | las lecturas, del guion, leyendo los tres yaml | cuadra |
| D7 | el cierre del puente contra las publicadas | cuadra: las cifras del yaml son las de §3 (f) |
| D8 | eventos por fuente y no colocables en horas sin ticks, sobre la base | cuadra (b.6) |
| D9 | la base repetida, byte a byte | cuadra |
| D10 | tiempo y memoria | se mide en la base (j) |
| D11 | PARADA si algo pide tocar `src/`, `tests/` o `knowledge/` | nada lo pide |
| D12 | arreglar errores de programación del guion, sí; cambiar una pieza o una variante, no | se aplica en la fase 2 |

### §0.2 La fase A (las dos auditorías, copiadas tal cual)

Commit `5974d36d` (2026-11-23 22:53:16 -0500): `docs/validation/AUDITORIA-PROFUNDA-2026-11.md` y
`docs/validation/AUDITORIA-CAZADOR-2026-11-23.md`, cada una con una cabecera corta (la forma de
`AUDITORIA-2026-11-21.md`) y, debajo de la raya, el fichero del Escritorio byte a byte, comprobado al
montarlas con un guion de la carpeta de trabajo que compara lo que queda debajo de la raya con el
original («cuerpo igual al original: True» en las dos; 0 CR). Los sha256 son los del consultor (ver
la tabla de la apertura): ninguna de las dos difiere. `knowledge validate` no se quejó de ningún id
ni enlace (g): no hizo falta bloque `ids-inexistentes` en ninguna cabecera.

### §0.3 La fase P (el pre-registro, antes de ninguna corrida)

Commit **`613aa40c10358bacfebff4c80efb1524aef019bd`, 2026-11-23 23:32:13 -0500**, el tercero de la
rama, antes de que existiera ningún guion del puente (la hora de la primera corrida, en §1). Lleva:

1. `docs/adr/0099-la-salida-c-se-resuelve-midiendo-primero.md`, el borrador de Aleks salvo las dos
   marcas. `diff` contra el del Escritorio:

   ```
   3c3
   < date: <FECHA-DEL-COMMIT>
   ---
   > date: 2026-11-23
   294c294
   < <FECHA-DEL-COMMIT>; post-F14, rama del puente (R4.7, NA:F).
   ---
   > 2026-11-23; post-F14, rama del puente (R4.7, NA:F).
   ```
2. `docs/plan/PUENTE-TECHO.yaml`, byte a byte: `sha256sum` da
   `31e70e0a89db3f5b7c1500d7698f450f6d7d3f3659972ef5443ad383b524cfbf`; sin CR; `git ls-files -s` y
   `git hash-object` dan el mismo blob (`1b0b248f…`): git no convierte los saltos
   (`.gitattributes`: `* text=auto eol=lf`).
3. `tests/unit/test_puente_techo.py`, con la forma de `test_meta_techo_parejas.py`: el sha256; el
   lector estricto; la decisión; los propios (100, 2, [1, 2], 3 y "0.10"); las diez piezas, que
   ninguna variante nombra una pieza que no exista y que ninguna sobra; las ocho sueltas, todo_junto
   (las cuatro primeras), las cuatro de vuelta y las dos del cierre, en su orden; los meses y las
   publicadas del cierre; los dos órdenes de lectura; las claves de `criterio_fidelidad.yaml`
   (`n_minimo` 100, `esperanza_minima_r` "0.10") y de `META-TECHO-PAREJAS.yaml` (`percentil_alto` 95 y
   su umbral "0.10"); y dos que rompen a propósito (el desfase a 3; una suelta con una pieza que no
   existe). Seis tests: `uv run pytest -q tests/unit/test_puente_techo.py` → 6 passed; ruff format,
   ruff check y mypy en verde.
4. La fila del índice de `docs/adr/README.md` y los dos recuadros, tal cual con la fecha: al final de
   ADR-0092 §6 (detrás del de ADR-0098) y al final de ADR-0098 §3 (justo antes de «### 4. Tres
   ajustes»). Los cuerpos no se tocan.
5. ADR-0099 salió del bloque `ids-inexistentes` del encargo, y el bloque con él. Tests Currently
   Passing, de 2137 a 2143. `state check`, `knowledge validate` (1201 documentos, todo id existe) y
   `make check` en verde (3618 passed, sello del árbol `9dd01d11…`).

### §0.4 La fase 0 (inventario, sin correr el guion)

**a) Lo que se reutiliza de `techo_parejas.py` y lo que se reescribe.** `git diff --stat 88f678f7
HEAD -- docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/` sale vacío: el guion no ha cambiado desde
el cierre de F39l. Se carga por su ruta (`importlib`, con la ruta literal) y se usa sin copiar:
`entorno` (:403-434, el motor de los días dev sin calentamiento, una sola vez), `a_puntos` (:99),
`caja_derivada` (:107), `objetivo_de` (:114), `lote_del_riesgo` (:120), `Medida` y `lectura_techo`
(:135-180), `ordenes_llenadas` y `comparar_control` (:260-333, para el control), `_lote_final`
(:600-624), `filas_de` (:627), `medida_de` (:638-683), `_lineas_medida` (:871-885), `_saldo_de`,
`_r`, `_pct`, `_cargar_meta` (:1010) y `Pedido`, `Traza` y `Recuentos` (:339-373), ampliados por
herencia con lo que falta. Se reescriben, con un interruptor por pieza: el bucle `repetir` (:437-592),
la construcción de los pedidos de `techo` (:783-815, que solo guarda el minuto: el instante y el
precio del caso hacen falta para `entrada_al_precio_del_caso`), el predicado de RN-002 (`_rn002`,
:752-768, que junta los dos predicados) y las filas de las posiciones abiertas con `abrir_conocida`
(b.3). Con todos los interruptores apagados, el bucle nuevo tiene que hacer lo mismo que `repetir`:
se comprueba con D2 a y D2 b, no se supone.

**b) Pieza a pieza, dónde entra el interruptor (todas sin tocar `src/`):**
1. `objetivo_sobre_el_stop`: la base del objetivo en `techo_parejas.py:554` (`base = p.caja if
   base_objetivo == "caja_completa" else distancia_stop`); con la pieza, la distancia de la entrada
   al stop del caso, que con `stop_en_el_08` sigue siendo la del stop del caso («el objetivo no
   cambia»), y `objetivo_de` (:114-117), hacia abajo al punto.
2. `sin_break_even`: el bloque de RN-014 (:523-530) no corre.
3. `entrada_al_precio_del_caso`: `Broker.abrir_conocida` (`src/botsito/engine/broker.py:658-689`)
   **no crea orden** (`self.posiciones[id] = p`, :687; ninguna entrada en `broker.ordenes`), y
   `posiciones_del_bot` salta toda posición sin orden (`cableado.py:1341-1343`: `o =
   broker.ordenes.get(p.orden_id)`; `if o is None: continue`). El auditor del encargo tenía razón:
   `filas_de` daría cero filas. Por eso el guion calcula las filas de esas posiciones con las mismas
   fórmulas de `posiciones_del_bot` (`cableado.py:1323-1377`: `pnl`, la comisión del perfil por lado,
   los swaps hasta el cierre y el riesgo = lotes × distancia de la entrada al stop de apertura /
   escala × contrato) y lo comprueba con D2 c. El instante del caso, por la ingesta
   (`arnes.dias_de_construccion`), es **al segundo**: de las 198 operaciones, 176 traen segundos
   distintos de cero y ninguna fracción de segundo; todas en UTC (guion de recuentos de la carpeta
   de trabajo). En la iteración del minuto del caso, el guion avanza el bróker hasta el milisegundo
   anterior al instante del caso y abre allí, al precio del caso, con el lote del riesgo calculado con
   la cuenta de ese momento y limitado por `_lote_final` (volumen 50 y margen libre al precio de
   conversión del instante: `broker.py:1025` y `:1065`), como hacía `viabilidad_comision.py:157-181`.
   `abrir_conocida` levanta `BrokerError` si el perfil no admite la posición
   (`_limite_infringido`, :1114, y `_margen_infringido`): se cuenta como rechazada con su motivo.
4. `sin_las_de_mas_de_100_lotes`: el lote por riesgo es `lote_del_riesgo` (:546-548), antes de
   `_lote_final` (:549); si pasa de 100 (del yaml), fuera y contada.
5. `desfase_menos_2`: entrada y stop del caso menos 2 puntos (del yaml) en los dos lados, como
   `scripts/viabilidad_trader.py:380-381` (`pts(...) - DESFASE_PUNTOS`, `DESFASE_PUNTOS = 2` en :50);
   la caja y el objetivo salen de ellos.
6. Spread: el bróker recibe el mercado del día como `Mercado(ticks, m1)` (`simulacion.py:78-79`;
   `llenado.py:76-97`), y `techo_parejas.py:486-488` lo pasa a `Broker` en su constructor. El guion
   construye otro `Mercado` con cada tick cambiado (`ask` a `max(bid, ask − k)` o a `bid`; `Tick` es
   un dataclass congelado, `domain/ticks.py:25-31`) y la misma M1: los minutos sin ticks, que van por
   el cierre de la M1 más el spread supuesto por hora (`Mercado.cotizacion`, `llenado.py:99-104`), no
   se tocan. Los eventos por fuente salen de `Traza.por_fuente`, que `_a_la_cuenta` rellena
   (`cableado.py:522`). Las 7 no colocables en una hora sin ticks: si la hora UTC del minuto en que
   se coloca no tiene ningún tick en `md.ticks`.
7. `sin_cierre_h4`: `_rn002` (:752-768) dispara con `vence_vela_h4` O `alcanza_hora`; el guion lleva
   los dos predicados por separado y, con la pieza, solo `alcanza_hora`. El cierre de fin de día
   (:571-575) sigue.
8. `stop_en_el_08`: el stop a `stop_fraccion_caja` (0,8, del registro) por la distancia de la
   entrada al stop del caso, al punto más cercano (`niveles()`, `scripts/viabilidad_comision.py:72-74`:
   `int((Decimal(d) * Decimal("0.8")).to_integral_value())`), y el lote sobre esa distancia (también
   el de la pieza 4); el objetivo no cambia.

**c) El break even y la esperanza antes de comisión.** El bróker guarda el stop original al
moverlo, y `clasificar_cierre` (`primitivas_broker.py:197-201`) da `break_even` a un cierre por stop
con el stop movido: una posición «cierra en el break even» si su motivo es `stop` y su
`stop_original` no es None (el único movimiento es el de RN-014, a la entrada). La esperanza antes de
comisión es la media de `bruto / riesgo` de las filas (`FilaPosicion.bruto`, el PnL bruto de
`cuenta.pnl`, `cableado.py:1345-1348`); la neta, `esperanza_r` sobre `neto / riesgo`, la del techo.

**d) El subtotal de abril y agosto.** `medida_de` (:638-683) ya admite unos días y unos meses de
cuenta: las posiciones de abril y agosto, los días dev de esos dos meses (42, con sus días sin
operaciones) y sus dos cuentas, con `remuestreo_por_dias` y las réplicas y la semilla del bloque
`rentabilidad`, como hace el bloque de julio (:820-824).

**e) Recuentos de partida**, contados en esta sesión por `arnes.dias_de_construccion` con un guion de
la carpeta de trabajo que no imprime claves:

| mes | días dev | sin operaciones | operaciones del trader |
|---|---|---|---|
| 2026-01 | 21 | 0 | 54 |
| 2026-04 | 21 | 5 | 35 |
| 2026-07 | 13 | 0 | 67 |
| 2026-08 | 21 | 2 | 42 |
| total | **76** | 7 | **198** (abril y agosto: **77**) |

Ninguna sin stop. Coinciden con la última cuenta (`RECORRIDA-CONSTRUCCION-3.md:129-136`).
`casos_reservados(repo)`: 34 en total, 0 en los cuatro meses de construcción.

**f) Las publicadas y qué era V1 y V2.** `VIABILIDAD-COMISION.md` §3, filas de 5 USD (:112-113): V1,
70 operaciones, +0,70 bruta y +0,34 neta [−0,15; +0,85]; V2, 67, +0,88 y +0,47 [−0,13; +1,08]. Son
las del yaml. En `scripts/viabilidad_comision.py`: `niveles()` (:66-83) lee el stop del libro como
**el 1** (V1: stop en el 1, objetivo a 3·d, lote sobre d; V2: stop y lote en 0,8·d al punto más
cercano, objetivo a 3·d); cada operación se abre con `abrir_conocida` al precio del caso menos el
desfase y en su segundo (:157-181; `ms_de`, :135-136), con el perfil de entonces sin saldo (sin
margen) y un tope de 100 lotes que, pasado, levanta `BrokerError` y la deja fuera
(«volumen_max_lotes», :176-181 y :300); en V1, el movimiento documentado de una operación
(`vt.MOVIMIENTOS`, :188-196); y todo se cierra al final de la ventana del kit (`md.hasta_ms`,
:197-200), sin RN-002 ni RN-014. **Frente a D3 todo casa**: el techo lee el stop del caso como su 0,8
y deriva la caja (3,75·d de objetivo); con `objetivo_sobre_el_stop` el objetivo queda a 3·d, el de
V1 y V2; con `stop_en_el_08`, el stop y el lote de V2; el tope de 100, sobre el lote por riesgo antes
de limitar, como el `lote_por_riesgo` de entonces (`viabilidad_trader.py:169-176`, hacia abajo a
0,01). Lo que no se reproduce es lo que D7 lista (la cuenta arrastrada, el movimiento de V1, el
bróker en los minutos sin ticks, el 50 con margen que limita, el R nominal), y además que el cierre
de entonces era el del final de la ventana del kit y el de hoy, el de RN-002 por `alcanza_hora` más
el fin de día: se dirá en §3 si el puente no cierra, sin medirlo.

**g) `knowledge validate` sobre las dos auditorías:** «OK: 1199 documentos: todo id citado existe o
esta declarado con motivo», sin ningún ERROR (log en la carpeta de trabajo). Los dos ids de P2-09
escritos sin sufijo (`ev-v3-003220`, `ev-v3-003318`) no los lee como ids: no hizo falta declararlos.

**h) Herencias** (grep sobre rutas literales):
- `docs/plan/HOJA-DE-RUTA.md`: R4.7 (:437-443; su «Hecho cuando», el ADR de Aleks; cita la auditoría
  del 2026-11-21 como punto de partida), A.5 (:750-758, «que también mide el deslizamiento»), R6.0 y
  la línea de Metas: van a las líneas del cierre (§5). **Llaman «grabador» a todo F17**: A.1 (:692,
  «el grabador de spread y ticks (F17, PARCIAL)»), A.5 (:754 y su «Hecho cuando», :758, «el grabador
  hecho») y la fila F:F17 (:892, «PARCIAL: el script de medición …, no el grabador»). Se dicen, no se
  cambian (encargo).
- `PROJECT_STATE.md`: la F de la Next Action (:28), que se amplía en el cierre; el heredado 10 (:57,
  «De la demo de FTMO queda el grabador de spread y ticks, F17»), que también llama grabador a todo
  F17; A-56 en la tabla de abiertas (:72), que no se toca; la deuda de `curva_con_deslizamiento` y
  `veredicto_con_f17` (:100), de F17 y no de esta rama.
- `docs/plan/RUMBO-2026-11.md` (:43), la enmienda que la fase 5 corrige con otra.
- ADR-0098 §3 C y §5, y ADR-0092 §6: los recuadros de la fase P.
- `RECORRIDA-CONSTRUCCION-3.md`, `VIABILIDAD-COMISION.md` y `VIABILIDAD-TRADER.md`: las cifras que el
  puente usa (control, base, publicadas); cerrados, no se tocan.

**i) La fila de HOLDOUT del día, antes del primer `make check`.** Se estadió tras crear la rama y antes
de cualquier otra lectura o escritura; el log del primer `make check` de la apertura (el que cayó por
el bloqueo del planificador) ya traía «G2: fila de HOLDOUT-EXPOSICIONES del 2026-11-23 para
trabajo/puente-techo, estadiada», y el segundo también; la fila entra en el commit de apertura
(`0f021d68`, 22:16:56).

**j) Tiempo y memoria.** Cada `make check` de la rama dura unos 29 minutos (1725 s, 1745 s y 1719 s de
tests; pico de 320 a 322 MiB). El guion no tiene medida previa: se mide en la base (D10) y con eso
se dice cuánto tardarán las dieciséis. Cabe en esta sesión si cada variante tarda lo que una
corrida del arnés (de 318 a 373 s en F39l): unas hora y media.

### §0.5 El encargo frente al repo (auditor y lo medido)

El subagente `auditor-encargo` (2026-11-23, solo lectura) comprobó 38 afirmaciones: 29 correctas, 7
con matiz y 2 que no cuadran, más 4 herencias. Lo que cambia algo, con lo que se hace:

1. **D2 c dice «las nueve variantes que llevan esa pieza»; son siete** (INCORRECTA): la suelta,
   `todo_junto`, tres de las cuatro de vuelta (la que repone `entrada_al_precio_del_caso` no la
   lleva) y las dos del cierre (`PUENTE-TECHO.yaml`, `variantes`). Si D2 c no pasa, la PARADA es en
   esas siete.
2. **«La esperanza antes de comisión» es antes de comisión y de swaps** (MATIZ): `neto = bruto −
   comision − swaps` (`cableado.py:1346-1352`), y la `PosicionCerrada` de la fila solo lleva el neto.
   El guion calcula la media de `bruto / riesgo` de las filas y la rotula «antes de comisión y swaps»
   (los swaps del techo son 0: ninguna posición cruza la noche).
3. **`stop_en_el_08` pone el stop a 0,64 de la caja derivada** (MATIZ): reproduce V2, que leía el
   stop del caso como su 1 (`niveles()`), frente al techo, que lo lee como su 0,8; y redondea al punto
   más cercano, como `niveles()`, no con el redondeo del registro. Es lo que dicen D3 y el yaml; se
   declara.
4. **El tope de 100 lotes no está en `viabilidad_comision.py`** (MATIZ): era el
   `firma_volumen_max_lotes` del perfil de entonces, que salía como `BrokerError`; hoy el perfil dice
   50 y `lote_si_no_cabe: limitar`. En el puente el 100 sale del yaml, como dice D3.
5. **Las posiciones con riesgo no positivo** (hallazgo a5 del revisor de F39l: el techo las filtra
   sin decirlo, `techo_parejas.py:816`): el guion nuevo las cuenta en cada variante («cerradas con
   riesgo no positivo») en lugar de filtrarlas en silencio. En la base no se imprimen dentro del
   bloque M1, que tiene que ser el de `meta.txt`.
6. **D5 es más estricto que ADR-0099 §2** (MATIZ): el ADR dice que cada variante imprime los cuatro
   meses y abril y agosto; D5 deja `v1_de_hoy` y `v2_de_hoy` solo con abril y agosto. Se sigue D5:
   imprimir menos no contradice el ADR, y el yaml dice que esas dos no llevan lectura sobre los
   cuatro. Para ganar tiempo, esas dos corren solo sobre los días de abril y agosto: con una cuenta
   por mes (ADR-0092 §8), lo de un mes no depende de los demás.
7. **`abrir_conocida` no devuelve un `Rechazo`: levanta `BrokerError`** (también por
   `ordenes_simultaneas_max`, `broker.py:1118-1121`): el guion la captura y la cuenta como «al
   abrir: <motivo>».
8. **Las enmiendas de RUMBO §4 van en la cabeza de la sección** (`RUMBO-2026-11.md:37`, antes del
   cuerpo, :39): «al final de las que ya tiene» es justo detrás de la del 2026-11-10 (fase 5).
9. **«Siete observaciones de deslizamiento» (la NOTA de MASTER_PLAN)**: ADR-0090:236 dice «Siete
   muestras» y enumera nueve valores en :234-235. La NOTA copia la cifra del ADR, que es su fuente.
10. **PROJECT_STATE, «hoy 24.680 bytes»**: es el de `main`; en la rama, 24.728 (Current Branch,
    Current Feature y el recuento de tests). Las líneas del cierre se miden sobre el de `main` más
    ellas (§5).
11. **El run 45107787390** no está en ningún texto commiteado del cierre de F39l (HISTORIA da el de
    la apertura); lo que vale es lo que se vio con `gh run view` (apertura).
12. **R4.7 depende de «una prueba gratuita de FTMO viva para F17»**, que no hay: el puente no la
    necesita (ADR-0099 §1-2: se mide sobre construcción); F17 rediseñado sigue esperándola.
13. **«Grabador» por todo F17**: además de lo de (h), MASTER_PLAN.md:127 («Grabar ticks y spread»).
    A.5 está bajo «Carril: guardias y deuda», no bajo el carril de Aleks. Se dice; no se cambia.
14. **El pendiente de la rama que vuelva a tocar el respaldo M1** (HISTORIA, heredados): esta rama no
    toca el respaldo en `src/` (D8 solo lo cuenta): no le aplica.

**Exposición del auditor:** un `grep` suyo imprimió una línea de `knowledge/cases/kit/config.yaml`
(la 9, `ventana_local:`): la configuración del kit, sin fechas, casos ni resultados; no es holdout (el
guion del techo la lee para construir el entorno). Se declara (§0.8).

### §0.6 Lo que necesito que decidas (PARADA condicional: CUADRA)

Las dieciséis variantes se pueden hacer como dice D3 sin tocar `src/` (b): según el encargo, **sigo
a la fase 1 sin esperar**. Lo que va arriba lo aplico así, y lo dejo escrito por si quieres otra cosa:

0. D2 c. Opciones: (a) la PARADA, si falla, en las siete variantes que llevan la pieza; (b) en
   nueve. Recomiendo (a): son siete en el yaml. Coste de (b): ninguna variante que contar de más.
1. La esperanza antes de comisión. Opciones: (a) la media de `bruto / riesgo`, rotulada «antes de
   comisión y swaps»; (b) reconstruir una serie sin comisión pero con swaps. Recomiendo (a): los swaps
   son 0 en el techo y es la cifra que su cita sostiene. Coste de (b): un cálculo que no está en
   ninguna función del repo.
2. Las dos del cierre. Opciones: (a) solo sobre los días de abril y agosto, como D5; (b) los cuatro
   meses y leer solo abril y agosto. Recomiendo (a): mismo resultado con una cuenta por mes y la
   mitad de tiempo. Coste de (b): unos minutos más por variante.

### §0.7 Lo que no pude medir

- La duración del guion antes de correrlo (j): se mide en la base.
- Que `alcanza_hora` (`ventana_fin`) coincida con el `hasta` de la ventana del kit que usaba V1 (el
  auditor no leyó más de `config.yaml`): no se mide; si el cierre del puente no cierra, va a la lista
  de D7 como diferencia de método.
- «Los cambios del bróker en los minutos sin ticks» de D7: no se miden (D7 lo dice).

### §0.8 Exposiciones declaradas (2026-11-23)

Las de la fila del día de `HOLDOUT-EXPOSICIONES.md` (la de la apertura): los cuatro ficheros del
Escritorio, `casos_reservados` y `casos_ocultos` por recuento (34, 0 en construcción), los casos dev
de construcción por la ingesta (los recuentos de e y la precisión del instante, sin claves) y el
código y los documentos de la fase 0. Más, por el auditor, la línea 9 de
`knowledge/cases/kit/config.yaml` (configuración del kit, sin datos; no es holdout).

## Estado

EN CURSO: fase 0 hecha (CUADRA); sigue la fase 1.
