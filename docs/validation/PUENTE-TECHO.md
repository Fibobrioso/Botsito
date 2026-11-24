# PUENTE-TECHO · El puente del techo pieza a pieza, pre-registrado antes de correr (R4.7, entrada F)

> Entregado el 2026-11-24: la lectura del puente es «solo_juntas» (ninguna suelta deja de dar
> no_gana; todo_junto, no_concluyente); el cierre cierra con V1 y V2. Rama lista para revisión, NO
> cerrada.

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
  La respuesta del consultor, tal cual (también al final del encargo):

  > Respuesta del consultor a la PARADA antes de abrir (2026-11-23): el ADR-0099-borrador.md del
  > Escritorio era una versión anterior. Aleks ya ha puesto la buena (19.965 bytes). Vuelve a medir
  > su sha256: si da aa4e95ff87144f4b748951fe6de16c68a1cb5950673b9815053eebd8bf58200b, sigue con el
  > encargo tal cual, empezando por la rama y la fila de HOLDOUT-EXPOSICIONES antes del primer make
  > check. Si no coincide, PARADA otra vez con el sha y los bytes, sin tocar nada.

  La segunda medida dio 19.965 bytes y ese sha: solo entonces se abrió la rama.
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
   fórmulas de `posiciones_del_bot` (`cableado.py:1323-1377`: `pnl`, la comisión del perfil por lado
   y los swaps hasta el cierre), salvo el riesgo: `posiciones_del_bot` lo toma del precio y el stop
   de la ORDEN (`cableado.py:1352`) y el guion, sin orden, de la entrada y el stop de apertura de la
   posición (lotes × distancia / escala × contrato); los dos coinciden cuando la stop se llena a su
   precio, que es el caso que compara D2 c (corrección del revisor, a3). El instante del caso, por la
   ingesta (`arnes.dias_de_construccion`), es **al segundo**: de las 198 operaciones, 176 traen
   segundos distintos de cero y ninguna fracción de segundo; todas en UTC (guion de recuentos de la
   carpeta de trabajo). En la iteración del minuto del caso (que decide en el cierre de la M1
   anterior), el guion calcula el lote del riesgo con el saldo de la cuenta y el margen libre del
   bróker de ese cierre, y el precio de conversión del instante del caso (`_lote_final`: volumen 50 y
   margen libre, `broker.py:1025` y `:1065`); después `abrir_conocida` avanza el bróker hasta el
   instante del caso y abre allí, al precio del caso (`broker.py:673`, `:1109-1112`). Si en ese tramo,
   de menos de un minuto, se cerrara otra posición, el lote saldría del saldo de antes: el efecto no
   está medido (corrección del revisor, a1; en ninguna corrida hubo rechazos). `viabilidad_comision.py`
   (:157-181) avanzaba hasta el milisegundo anterior y calculaba el lote con el saldo de entonces.
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

**f) Las publicadas y qué era V1 y V2.** `VIABILIDAD-COMISION.md` §3, filas de 5 USD (:111-112): V1,
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

### §0.9 La fase 1 (el README y el guion, antes de correr)

- `anexos/PUENTE-TECHO/README.md`, en su propio commit, **`f042fa10` (2026-11-24 00:46:14)**,
  antes de la primera corrida; con él, la fila de HOLDOUT-EXPOSICIONES del 2026-11-24, escrita y
  estadiada antes del primer `make check` del día (su log: «G2: fila … del 2026-11-24 …, estadiada»).
- `puente.py` (cuatro modos: `control`, `conocida`, `variante <nombre>`, `todo`) y `test_puente.py`.
  Lee los tres yaml y no lleva ninguna de sus cifras dentro: los nombres de las piezas con cifra
  (`sin_las_de_mas_de_100_lotes`, `desfase_menos_2`, `spread_menos_1` y `_2`) los compone con
  `propios` y comprueba que son los del yaml, en su orden. Dos ajustes de forma que pidió la guardia,
  sin rodearla: (1) `import techo_parejas` tras un `sys.path.insert` a la carpeta vecina lo negó
  («no se pudo resolver el modulo»); se carga con `importlib` por su ruta literal, que es lo que la
  propia guardia indica; (2) `ruff.exe` por su ruta lo negó («no sabe con que se ejecuta»): ruff y
  mypy se corrieron con `uv run` dentro del repo, con el guion ya copiado y sin ningún `make check`
  en marcha.
- ruff format, ruff check y mypy en verde sobre los dos. El test de humo, **15 passed**:

  ```
  $ uv run pytest docs/validation/anexos/PUENTE-TECHO/test_puente.py -p no:cacheprovider -v
  collected 15 items
  docs\validation\anexos\PUENTE-TECHO\test_puente.py ...............       [100%]
  ============================= 15 passed in 1.16s ==============================
  ```

  La primera vez fallaron cuatro, los cuatro por errores del test o del guion y no de una pieza:
  `Piezas()` traía `spread=None` y `piezas_de` daba 0 (el valor por defecto pasó a 0); las reglas
  sintéticas del bróker no traían `stops_level_puntos` (una stop no se coloca sin él, ADR-0057); y el
  break even del test cerraba en un minuto sin mercado.

## §1 · Los controles (D2), D8 y D9

Primera corrida del guion: **2026-11-24 00:49:07** (`date` justo antes), **1 h 17 min después del
pre-registro** (`613aa40c`, 2026-11-23 23:32:13). Todas desde la raíz, una a la vez y sin ningún
`make check` en marcha.

**D2 a, el control de ADR-0098 §1 con el bucle nuevo** (`control.txt`):

```
## El control (ADR-0098 §1), con el bucle de puente.py (D2 a)
posiciones del bot en la salida: 235; entran en el control: 235; fuera (manual de una regla solo del bot): 0
reproducidas al centimo (lote, motivo, instante del cierre, PnL neto): 235 de 235
control: PASA
```

**D2 b, la base contra `meta.txt`.** El bloque M1 de `base.txt` (de «## M1 · El techo» al final del
bloque de julio, 21 líneas) contra el de `anexos/RECORRIDA-CONSTRUCCION-3/meta.txt` (de «## M1 · El
techo» a la línea anterior a «## M2 · Las parejas», 21 líneas), extraídos con `sed` a la carpeta de
trabajo: **`diff` vacío, exit 0**. Con todos los interruptores apagados, el bucle nuevo da el techo.

**D2 c, `abrir_conocida` frente a la orden stop, sobre los días dev** (`conocida.txt`): de las 191
posiciones del techo, las 124 llenadas al precio de su orden, abiertas otra vez con `abrir_conocida`
en el instante y al precio del llenado, con el mismo lote, stop y objetivo: **124 de 124** con el mismo
riesgo, lote, motivo e instante del cierre y el mismo R bruto y neto; ninguna rechazada. Y en el test
de humo, sobre datos sintéticos, una compra por orden stop y por `abrir_conocida` da el mismo riesgo,
bruto, neto y cierre, y con otro stop el riesgo ya no es el mismo. **Un arreglo del control,
declarado (D12):** la primera corrida dio 122 de 124 (`conocida-antes-del-arreglo.txt`): dos
posiciones de un día dev de julio, llenadas por el respaldo M1, cerraban en otro instante. Medido con
un guion de diagnóstico de la carpeta de trabajo (motivos e instantes de ese día, sin precios): el
respaldo sella el llenado en el último milisegundo de la vela y `minuto_de_apertura` solo le suma el
minuto a esa fuente (ADR-0091 §2); reabiertas en ese milisegundo con la fuente «caso», RN-014 miraba
una vela antes. D2 c compara ahora con la misma fuente de apertura que la posición del techo (el
campo `fuente` del pedido). Las fórmulas del riesgo y del R no cambiaron; en la variante
`entrada_al_precio_del_caso` la fuente sigue siendo «caso», en el segundo del caso.

**D8, sobre la base (sin R):** eventos del techo por fuente: `ticks` 368, `respaldo_m1` 16 y
`cierre_m1` 77 (los `stop_movido` con ticks en su minuto); de las 7 no colocables, **0** caen en una
hora UTC sin ticks y 0 en un minuto sin ticks (el de la colocación).

**D9, determinismo:** `base.txt` y `base-repetida.txt`, iguales byte a byte (`cmp` exit 0; sha256
`af0129808e8192dcb39221357c11e640835a2113f419fed793a115909faad986` los dos, tal como salieron, con
CRLF). La primera comparación dio una diferencia: `base.txt` y `control.txt` llevaban al final la
línea «PICO DE MEMORIA» de `scripts/pico_memoria.py`, que escribe en la salida estándar de la orden
que mide; se quitó de los dos ficheros (no la imprime el guion) y su cifra va abajo.

**Los finales de línea (un ajuste declarado, D12).** El primer `make check` de este commit cayó en
`test_no_crlf_in_tracked_text_files`: en Windows, `print` escribe CRLF al redirigir la salida. Las 21
salidas se pasaron a LF con un guion de la carpeta de trabajo que solo cambia `\r\n` por `\n`, y
`puente.py` escribe ya LF (`sys.stdout.reconfigure(..., newline="\n")`). Para ver que no cambia nada
más, la base se corrió otra vez con el guion cambiado: **igual byte a byte a `base.txt` convertida**
(`cmp` exit 0); `base.txt` y `base-repetida.txt` dan ahora los dos
`6bd49ae0b19c3f1f0e69fda45565e7d81b8fd9c55a9ad9d3f6bc8649e46c69ef`.

**D10, tiempo y memoria:** la base, 82 s (00:50:34 a 00:51:56, control incluido) y un pico de **592
MiB** (`pico_memoria.py ejecutar`; el control, 591 MiB). Las dieciséis, una a una: de 75 a 90 s cada
una, unos 21 minutos en total (la hora de escritura de cada salida). Ni 3 horas ni 1,5 GiB.

## §2 · Las variantes (D4, D5, D6)

Una fila por variante, copiada de su salida (`anexos/PUENTE-TECHO/<nombre>.txt`). E bruta: antes de
comisión y swaps (media de `bruto / riesgo`); E neta, p5 y p95: la media del R neto y sus percentiles
5 y 95 por `remuestreo_por_dias` (10000 réplicas, semilla 20261107, del bloque `rentabilidad`). Las de
vuelta llevan el nombre de la pieza del techo que reponen sobre `todo_junto`. Ninguna corrida tuvo
rechazos del bróker ni cerradas con riesgo no positivo; ninguna cerró al fin del día. Los eventos que
salen del respaldo M1 (D3, sin R), en las tres de spread: `spread_menos_1`, `respaldo_m1` 16, `ticks`
378 y `cierre_m1` 83; `spread_menos_2`, 16, 378 y 85; `sin_spread`, 16, 380 y 88 (la base: 16, 368 y
77). El respaldo no lleva el spread cambiado: sus 16 eventos son los mismos en las cuatro.

**Los cuatro meses** (76 días dev):

| variante | N | no coloc. | no llen. | fuera tope | rechazadas | BE movido | cierran en BE | RN-002 | fin de día | E bruta | E neta | p5 | p95 | d) | e) | f) suspendida | lectura por el R | lectura de ADR-0098 §2 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base | 191 | 7 | 0 | 0 | ninguna | 79 | 46 | 7 | 0 | 0.127 | -0.239 | -0.450 | -0.026 | 4.88 % | 92.05 % | no | no_gana | no_gana |
| objetivo_sobre_el_stop | 191 | 7 | 0 | 0 | ninguna | 75 | 37 | 3 | 0 | 0.192 | -0.173 | -0.374 | 0.034 | 3.46 % | 92.77 % | no | no_gana | no_gana |
| sin_break_even | 191 | 7 | 0 | 0 | ninguna | 0 | 0 | 15 | 0 | 0.153 | -0.213 | -0.451 | 0.033 | 4.62 % | 90.65 % | no | no_gana | no_gana |
| entrada_al_precio_del_caso | 198 | 0 | 0 | 0 | ninguna | 82 | 46 | 8 | 0 | 0.174 | -0.190 | -0.385 | 0.012 | 4.91 % | 94.24 % | no | no_gana | no_gana |
| sin_las_de_mas_de_100_lotes | 183 | 7 | 0 | 8 | ninguna | 79 | 46 | 7 | 0 | 0.197 | -0.132 | -0.329 | 0.074 | 4.88 % | 92.05 % | no | no_gana | no_gana |
| desfase_menos_2 | 181 | 17 | 0 | 0 | ninguna | 78 | 46 | 7 | 0 | 0.176 | -0.190 | -0.444 | 0.073 | 4.55 % | 95.49 % | no | no_gana | no_gana |
| spread_menos_1 | 196 | 2 | 0 | 0 | ninguna | 85 | 50 | 7 | 0 | 0.168 | -0.196 | -0.419 | 0.034 | 4.95 % | 93.54 % | no | no_gana | no_gana |
| spread_menos_2 | 196 | 2 | 0 | 0 | ninguna | 87 | 51 | 8 | 0 | 0.188 | -0.176 | -0.398 | 0.059 | 4.59 % | 94.37 % | no | no_gana | no_gana |
| sin_spread | 197 | 1 | 0 | 0 | ninguna | 90 | 52 | 7 | 0 | 0.312 | -0.052 | -0.274 | 0.179 | 4.51 % | 94.32 % | no | no_gana | no_gana |
| todo_junto | 190 | 0 | 0 | 8 | ninguna | 0 | 0 | 9 | 0 | 0.350 | 0.022 | -0.190 | 0.246 | 4.06 % | 95.61 % | no | no_concluyente | no_gana |
| de_vuelta_objetivo_sobre_el_stop | 190 | 0 | 0 | 8 | ninguna | 0 | 0 | 16 | 0 | 0.240 | -0.088 | -0.309 | 0.138 | 4.65 % | 92.59 % | no | no_gana | no_gana |
| de_vuelta_sin_break_even | 189 | 0 | 0 | 9 | ninguna | 78 | 36 | 3 | 0 | 0.323 | -0.001 | -0.190 | 0.200 | 3.51 % | 96.40 % | no | no_gana | no_gana |
| de_vuelta_entrada_al_precio_del_caso | 183 | 7 | 0 | 8 | ninguna | 0 | 0 | 9 | 0 | 0.310 | -0.019 | -0.224 | 0.205 | 3.98 % | 91.95 % | no | no_gana | no_gana |
| de_vuelta_sin_las_de_mas_de_100_lotes | 198 | 0 | 0 | 0 | ninguna | 0 | 0 | 9 | 0 | 0.288 | -0.076 | -0.292 | 0.156 | 4.06 % | 95.61 % | no | no_gana | no_gana |

**Abril y agosto juntos** (42 días dev; sin lectura, D5):

| variante | N | no coloc. | no llen. | fuera tope | rechazadas | BE movido | cierran en BE | RN-002 | fin de día | E bruta | E neta | p5 | p95 | d) | e) | f) suspendida |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base | 74 | 3 | 0 | 0 | ninguna | 30 | 16 | 4 | 0 | 0.113 | -0.318 | -0.679 | 0.031 | 1.26 % | 96.26 % | no |
| objetivo_sobre_el_stop | 74 | 3 | 0 | 0 | ninguna | 28 | 10 | 1 | 0 | 0.381 | -0.051 | -0.443 | 0.325 | 1.32 % | 97.86 % | no |
| sin_break_even | 74 | 3 | 0 | 0 | ninguna | 0 | 0 | 6 | 0 | 0.167 | -0.264 | -0.660 | 0.139 | 2.30 % | 96.39 % | no |
| entrada_al_precio_del_caso | 77 | 0 | 0 | 0 | ninguna | 30 | 15 | 4 | 0 | 0.233 | -0.196 | -0.531 | 0.138 | 1.29 % | 97.80 % | no |
| sin_las_de_mas_de_100_lotes | 68 | 3 | 0 | 6 | ninguna | 30 | 16 | 4 | 0 | 0.267 | -0.097 | -0.401 | 0.202 | 1.26 % | 96.99 % | no |
| desfase_menos_2 | 71 | 6 | 0 | 0 | ninguna | 29 | 16 | 4 | 0 | 0.153 | -0.279 | -0.725 | 0.189 | 1.95 % | 95.49 % | no |
| spread_menos_1 | 77 | 0 | 0 | 0 | ninguna | 31 | 17 | 4 | 0 | 0.088 | -0.340 | -0.704 | 0.010 | 2.29 % | 95.93 % | no |
| spread_menos_2 | 77 | 0 | 0 | 0 | ninguna | 32 | 18 | 4 | 0 | 0.111 | -0.317 | -0.685 | 0.040 | 2.32 % | 96.05 % | no |
| sin_spread | 77 | 0 | 0 | 0 | ninguna | 33 | 17 | 4 | 0 | 0.319 | -0.110 | -0.486 | 0.246 | 1.40 % | 97.10 % | no |
| todo_junto | 71 | 0 | 0 | 6 | ninguna | 0 | 0 | 2 | 0 | 0.649 | 0.285 | -0.095 | 0.660 | 2.20 % | 99.05 % | no |
| de_vuelta_objetivo_sobre_el_stop | 71 | 0 | 0 | 6 | ninguna | 0 | 0 | 6 | 0 | 0.367 | 0.004 | -0.355 | 0.375 | 1.99 % | 96.43 % | no |
| de_vuelta_sin_break_even | 70 | 0 | 0 | 7 | ninguna | 28 | 9 | 1 | 0 | 0.636 | 0.281 | -0.056 | 0.624 | 1.30 % | 99.32 % | no |
| de_vuelta_entrada_al_precio_del_caso | 68 | 3 | 0 | 6 | ninguna | 0 | 0 | 2 | 0 | 0.631 | 0.267 | -0.097 | 0.641 | 2.27 % | 98.44 % | no |
| de_vuelta_sin_las_de_mas_de_100_lotes | 77 | 0 | 0 | 0 | ninguna | 0 | 0 | 2 | 0 | 0.507 | 0.079 | -0.328 | 0.484 | 2.45 % | 98.86 % | no |
| v1_de_hoy | 70 | 0 | 0 | 7 | ninguna | 0 | 0 | 1 | 0 | 0.729 | 0.375 | -0.024 | 0.772 | 2.77 % | 98.70 % | no |
| v2_de_hoy | 67 | 0 | 0 | 10 | ninguna | 0 | 0 | 0 | 0 | 0.920 | 0.503 | 0.052 | 0.955 | 3.00 % | 99.21 % | no |

## §3 · El cierre del puente (D7)

`v1_de_hoy` y `v2_de_hoy`, leídas solo sobre abril y agosto, frente a las publicadas del yaml
(`VIABILIDAD-COMISION.md` §3, 5 USD), con las tolerancias del yaml (3 operaciones; 0,10 R de neta):

```
CIERRE DEL PUENTE (ADR-0099 §2) frente a la publicada: cierra; N 70 frente a 70 (+0); esperanza neta 0.375 frente a 0.34 (+0.035); antes de comision 0.729 frente a 0.70 (+0.029)
CIERRE DEL PUENTE (ADR-0099 §2) frente a la publicada: cierra; N 67 frente a 67 (+0); esperanza neta 0.503 frente a 0.47 (+0.033); antes de comision 0.920 frente a 0.88 (+0.040)
```

**Las dos cierran.** Fuera por el tope de 100 lotes: 7 en `v1_de_hoy` y 10 en `v2_de_hoy`, los mismos
recuentos que publicó `VIABILIDAD-COMISION.md` (§2, fila de 5 USD: 7 y 10). Las diferencias de método
que siguen ahí, sin medirlas (D7): la cuenta arrastrada de entonces frente a una por mes; el
movimiento documentado de una operación en V1, que no se reproduce; los cambios del bróker en los
minutos sin ticks; el tope de volumen, que era 100 y excluía y hoy es 50 con el margen y limita; el R,
nominal menos la comisión entonces y hoy el PnL neto entre el riesgo, con swaps; y el cierre, al final
de la ventana del kit entonces y hoy por `alcanza_hora` y el fin del día.

## §4 · La lectura del puente (D6), literal

```
## La lectura del puente (ADR-0099 §3)
sueltas: objetivo_sobre_el_stop no_gana, sin_break_even no_gana, entrada_al_precio_del_caso no_gana, sin_las_de_mas_de_100_lotes no_gana, desfase_menos_2 no_gana, spread_menos_1 no_gana, spread_menos_2 no_gana, sin_spread no_gana; todo_junto: no_concluyente
LECTURA DEL PUENTE: solo_juntas
```

Las dieciséis salen también en `todo.txt` (una sola corrida de `puente.py todo`, con el entorno
construido una vez): sus 16 bloques son iguales a los de las corridas sueltas y su control al de
`control.txt` (comparados con un guion de la carpeta de trabajo); como `todo` corrió con el guion
final, eso también dice que el arreglo de D2 c no tocó la base. `lectura.txt` copia de él, tal cual, las dos líneas del cierre con sus cabeceras y la lectura del puente, con dos líneas añadidas: la cabecera del fichero y el título «## El cierre del puente (ADR-0099 §2), sobre abril y agosto» (corrección del revisor, a4).
En la línea del cierre, «antes de comision» es la E bruta de las tablas (antes de comisión y swaps;
los swaps son 0: ninguna posición cruza la noche).

## §5 · Las líneas del cierre, preparadas y medidas sobre una copia (no aplicadas)

`anexos/PUENTE-TECHO/simular_cierre.py` (con la forma del de F39l) las aplica en memoria sobre copias
de `PROJECT_STATE.md`, `docs/plan/HOJA-DE-RUTA.md` y `docs/state/HISTORIA.md`, corre
`test_hoja_de_ruta` (a, b y c) y `test_project_state` y no escribe nada en el repo
(`simular-cierre.txt`):

```
letras vivas en la copia: A C D F G I J M N Q; F viva? True
R4.8: HECHA? True; alguna letra (NA:) en el bloque? False
R4.7 cita ADR-0099? True; ABIERTA? True
A.5 cita ADR-0099 §5? True; «que también mide» sigue? False
R6.0 lleva la razón retirada? True
a: []
b: []
c: []
PROJECT_STATE del cierre: 24740 bytes (cabe en 25000); la rama hoy, con la F nueva: 24899 bytes
bytes de la F: antes 992, despues 1163
```

PROJECT_STATE del cierre, en la forma que escribirá el ritual: **24.740 bytes**, por debajo de 24.900.
Las líneas, tal como las aplicaría la orden de cierre (el texto exacto, en `simular_cierre.py`):

- **Next Action, la F**: detrás de «y la siguiente (R4.6) se prepara.», la frase «ADR-0099: se mide
  primero; el puente del techo, hecho (PUENTE-TECHO.md, lectura «solo_juntas»); F17 rediseñado
  (ADR-0099 §5) y el contraste con el trader, pendientes.» No sale nada; ninguna letra sale ni entra.
- **Hoja de ruta:** en la línea de Metas, detrás de «para marzo de 2027», «que no cabe con ninguna vía
  (ADR-0098 §6)»; R4.7 con ADR-0099 en Refs, su «Qué es» con la auditoría profunda
  (AUDITORIA-PROFUNDA-2026-11.md, que partió de la del 2026-11-21) y las tres medidas de ADR-0099, y su
  «Hecho cuando» en «el ADR de Aleks que acota ADR-0099 §7»; **R4.8** nueva tras R4.7, «El puente del
  techo pieza a pieza (ADR-0099)», con Refs ADR-0099 y ADR-0098, HECHA con su lectura y sin ninguna
  letra en su bloque; A.5 con F17 rediseñado (heredado 10; ADR-0099 §5: el historial de ticks del
  servidor de la demo, el grabador y la medida de las órdenes stop) en lugar de «que también mide el
  deslizamiento», y ADR-0099 en Refs; R6.0, «por el tope de peticiones (razón retirada por el recuadro
  del 2026-11-22 de ADR-0082; la decisión sigue)». Sin fila en el Marcador.
- **Lo que llama «grabador» a todo F17** (dicho, no cambiado): el heredado 10 de PROJECT_STATE
  (:57), A.1 (:692), el «Hecho cuando» de A.5 («el grabador hecho», :758), la fila F:F17 (:892) y
  MASTER_PLAN.md:127 («Grabar ticks y spread»).

## §6 · La fila de ERRORES-RECURRENTES, preparada (no aplicada)

| `trabajo/puente-techo` | Una pasada, opus, con los ocho alcances del encargo (PUENTE-TECHO.md, «Informe del revisor»; lo hecho, en «Lo que se hizo con los hallazgos del revisor»): eje (a) 0 bloquea, 1 importa, 4 menor; eje (b) 0 bloquea, 5 importa, 0 menor. a1 (cuándo se calcula el lote de `abrir_conocida`: la frase del informe no era la del código), b1 (D3 pedía contar los eventos del respaldo en las de spread), b3 (comandos sin literal ni hora), b4 (el guion de diagnóstico, declarado después de correrlo), b5 (la respuesta del consultor, parafraseada), arreglados; b2 (el test de humo no pasa el break even ni el tope por el bucle), dicho y no arreglado. | **Del consultor, que llegaron a Claude Code: 5.** (importa) El sha256 del borrador del ADR no casaba: el Escritorio tenía una versión anterior (PARADA antes de abrir). (menor) D2 c decía «las nueve variantes»: son siete. (menor) La fila de HOLDOUT del encargo decía que las dos auditorías leyeron «solo ficheros commiteados»: la profunda corrió `kb find`, que recorre la transcripción filtrada. (menor) «La esperanza antes de comisión» es antes de comisión y de swaps. (menor) «Hoy 24.680 bytes» era el PROJECT_STATE de `main`. **De la sesión, 5:** el `ScheduleWakeup` de respaldo dejó `.claude/scheduled_tasks.lock` en el repo y tumbó un `make check` entero; la línea de `pico_memoria.py ejecutar` fue a la salida medida (D9 la cazó); la primera versión de D2 c reabría con la fuente «caso» las posiciones llenadas por el respaldo M1; las salidas con CRLF tumbaron otro `make check` (`test_no_crlf_in_tracked_text_files`); y el guion de diagnóstico de D2 c se declaró en HOLDOUT después de correrlo (el mismo día). |

## §7 · La fase 5: dos notas en docs/plan (commit propio, `e9be7390`)

- `docs/plan/RUMBO-2026-11.md` §4: la enmienda del 2026-11-24, tal cual con la fecha del commit,
  **justo detrás de la del 2026-11-10** y antes del cuerpo de §4: en ese fichero las enmiendas van en
  la cabeza de la sección (`RUMBO-2026-11.md:37`), así que «al final de las que ya tiene» es ahí (lo
  vio el auditor del encargo, §0.5 punto 8). El cuerpo no se toca.
- `docs/plan/MASTER_PLAN.md`: la NOTA del 2026-11-24, tal cual, dentro del mismo bloque citado y
  detrás de la del 2026-11-19 (ADR-0096), con su forma (`> **NOTA (fecha, rama …, ADR).**`). La fila
  de F17 no se toca. «Siete observaciones» copia la cifra de ADR-0090 §7, que dice «Siete muestras»
  y enumera nueve valores (§0.5 punto 9).

## El encargo, punto por punto

| # | Lo que pide | Hecho | Evidencia |
|---|---|---|---|
| 1 | Base comprobada; tag F39m libre; REAP | Hecho | apertura |
| 2 | Fila de HOLDOUT del día antes de todo, y la del día nuevo | Hecho (23 y 24); el guion de diagnóstico de D2 c, declarado después de correrlo (el mismo día) | §0.4 i; §0.9; «Exposiciones» |
| 3 | Los cuatro ficheros, sha256 y leídos enteros | Hecho; PARADA por el del ADR, resuelta | apertura |
| 4 | abrir-rama con el contrato pedido | Hecho (`0f021d68`) | `contrato.yaml` |
| 5 | Fase A, commit propio, primero | Hecho (`5974d36d`) | §0.2 |
| 6 | Fase P, commit propio, antes de la fase 0 y de toda corrida | Hecho (`613aa40c`, 23:32:13) | §0.3; §1 |
| 7 | Fase 0, a a j, con su auditor y CUADRA | Hecho (`6ba82dee`) | §0.4-§0.8 |
| 8 | README en su commit antes de correr | Hecho (`f042fa10`, 00:46:14) | §0.9 |
| 9 | `puente.py` con sus modos | Hecho | §0.9 |
| 10 | Su test de humo: cada pieza en los dos sentidos | **Parcial** (15 passed): las piezas puras, D2 c, RN-002, las lecturas y el cierre; el break even «que se mueve y que no» y el tope «que entra y que sale» no pasan por el interruptor de `repetir` (revisor, b2) | §0.9; «Lo que se hizo» |
| 11 | D2 a, D2 b, D2 c, D8, D9, D10 | Hecho; D2 c con un arreglo declarado | §1 |
| 12 | D3: las diez piezas, con el recuento del respaldo en las de spread | Hecho (el recuento, desde la revisión: revisor, b1) | §2 |
| 13 | Las ocho sueltas, todo_junto y las cuatro de vuelta, a su fichero | Hecho; exit 0 las dieciséis | §2 |
| 14 | El cierre y la lectura, en `lectura.txt` y literal | Hecho | §3, §4 |
| 15 | Fase 5, las dos notas | Hecho (`e9be7390`) | §7 |
| 16 | Las líneas del cierre, medidas sobre una copia | Hecho | §5 |
| 17 | Revisor (opus) con los ocho alcances | Hecho | «Informe del revisor» |
| 18 | Nada de `src/`, `knowledge/`, `scripts/`, Makefile ni `.claude/` | Hecho | `git diff main --stat` |
| 19 | Ninguna recomendación de spec ni de motor | Hecho | todo el informe |

**Propuestas de otras variantes (D4), sin correrlas:** ninguna.

**Los tests que rompen a propósito (entregar-rama, paso 3), hecho de otra forma.** Los dos de
`tests/unit/test_puente_techo.py` que rompen (el desfase a 3; una suelta con una pieza que no existe)
fallan con el yaml mutado y pasan con el del repo (6 passed). Contra `main` el test no puede pasar por
construcción: allí no existen ni el yaml ni el test (`git cat-file -e main:docs/plan/PUENTE-TECHO.yaml`
y `… main:tests/unit/test_puente_techo.py`, exit 128 los dos), así que no se montó el clon desechable.
Sin CI de Linux: la rama no toca la plataforma (ni `.claude/`, ni hooks, ni rutas, ni código de
sistema; `git diff --stat main...HEAD -- src knowledge scripts Makefile .claude` vacío).
PROJECT_STATE en la rama: 24.728 bytes (tope 25.000).

## Los comandos ejecutados, con su hora (2026-11-24)

Desde la raíz, una a una. Las horas con «~» salen de la hora de escritura de cada salida (`ls -l`);
las demás, de `date`. Los guiones de la carpeta de trabajo de la sesión (fuera del repo) se nombran
por su nombre.

```
~00:47  uv run ruff format docs/validation/anexos/PUENTE-TECHO/puente.py docs/validation/anexos/PUENTE-TECHO/test_puente.py
~00:47  uv run ruff check --output-format concise docs/validation/anexos/PUENTE-TECHO/puente.py docs/validation/anexos/PUENTE-TECHO/test_puente.py
~00:47  uv run mypy docs/validation/anexos/PUENTE-TECHO/puente.py docs/validation/anexos/PUENTE-TECHO/test_puente.py
~00:48  uv run pytest docs/validation/anexos/PUENTE-TECHO/test_puente.py -p no:cacheprovider -q --tb=line   (4 failed; arreglados)
~00:48  uv run pytest docs/validation/anexos/PUENTE-TECHO/test_puente.py -p no:cacheprovider -v             (15 passed)
00:49:07  uv run python scripts/pico_memoria.py ejecutar -- uv run python -B docs/validation/anexos/PUENTE-TECHO/puente.py control docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/cuenta-por-mes.txt > docs/validation/anexos/PUENTE-TECHO/control.txt 2> control.err
00:50:34  uv run python scripts/pico_memoria.py ejecutar -- uv run python -B docs/validation/anexos/PUENTE-TECHO/puente.py variante base docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/cuenta-por-mes.txt > docs/validation/anexos/PUENTE-TECHO/base.txt 2> base.err
~00:52  sed -n '/^## M1 · El techo/,/^## M2 · Las parejas/p' docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/meta.txt | sed '$d' > m1-meta.txt
~00:52  sed -n '/^## M1 · El techo/,/^### D8/p' docs/validation/anexos/PUENTE-TECHO/base.txt | sed '$d' > m1-base.txt
~00:52  diff m1-meta.txt m1-base.txt   (exit 0; repetido sobre las versiones del índice, git show :…, antes del commit: exit 0)
~00:53  uv run python -B docs/validation/anexos/PUENTE-TECHO/puente.py variante base docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/cuenta-por-mes.txt > docs/validation/anexos/PUENTE-TECHO/base-repetida.txt
~00:54  uv run --no-sync python -B quitar_pico.py docs/validation/anexos/PUENTE-TECHO/base.txt docs/validation/anexos/PUENTE-TECHO/control.txt
~00:54  cmp base.txt base-repetida.txt   (exit 0)
~00:56  uv run python -B docs/validation/anexos/PUENTE-TECHO/puente.py conocida docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/cuenta-por-mes.txt > docs/validation/anexos/PUENTE-TECHO/conocida.txt   (exit 5)
~00:57  uv run --no-sync python -B diag_conocida.py <el día dev de julio que difería>   (motivos e instantes, sin precios)
00:57:50  cp conocida.txt conocida-antes-del-arreglo.txt
00:59:11  uv run python -B docs/validation/anexos/PUENTE-TECHO/puente.py conocida docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/cuenta-por-mes.txt > docs/validation/anexos/PUENTE-TECHO/conocida.txt   (exit 0)
01:00:58  … variante objetivo_sobre_el_stop … > objetivo_sobre_el_stop.txt
01:02:23  … variante sin_break_even … > sin_break_even.txt
01:03:43  … variante entrada_al_precio_del_caso … > entrada_al_precio_del_caso.txt
01:04:59  … variante sin_las_de_mas_de_100_lotes … > sin_las_de_mas_de_100_lotes.txt
01:06:15  … variante desfase_menos_2 … > desfase_menos_2.txt
01:07:39  … variante spread_menos_1 … > spread_menos_1.txt
01:09:04  … variante spread_menos_2 … > spread_menos_2.txt
01:10:34  … variante sin_spread … > sin_spread.txt
01:12:04  … variante todo_junto … > todo_junto.txt
01:13:27  … variante de_vuelta_objetivo_sobre_el_stop … > de_vuelta_objetivo_sobre_el_stop.txt
01:14:47  … variante de_vuelta_sin_break_even … > de_vuelta_sin_break_even.txt
01:16:06  … variante de_vuelta_entrada_al_precio_del_caso … > de_vuelta_entrada_al_precio_del_caso.txt
01:17:25  … variante de_vuelta_sin_las_de_mas_de_100_lotes … > de_vuelta_sin_las_de_mas_de_100_lotes.txt
01:18:50  … variante v1_de_hoy … > v1_de_hoy.txt
01:20:05  … variante v2_de_hoy … > v2_de_hoy.txt
01:22:46  uv run python -B docs/validation/anexos/PUENTE-TECHO/puente.py todo docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/cuenta-por-mes.txt > docs/validation/anexos/PUENTE-TECHO/todo.txt
~01:25  uv run --no-sync python -B cruzar_todo.py docs/validation/anexos/PUENTE-TECHO   (16 de 16; control igual)
~01:25  uv run --no-sync python -B hacer_lectura.py docs/validation/anexos/PUENTE-TECHO   (lectura.txt)
~01:30  uv run python -B docs/validation/anexos/PUENTE-TECHO/simular_cierre.py > docs/validation/anexos/PUENTE-TECHO/simular-cierre.txt
~01:58  uv run --no-sync python -B a_lf.py docs/validation/anexos/PUENTE-TECHO/*.txt   (21 de 23 pasados a LF)
~02:00  uv run python -B docs/validation/anexos/PUENTE-TECHO/puente.py variante base docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/cuenta-por-mes.txt > base-lf.txt   (con el guion en LF; cmp contra base.txt convertida: exit 0)
~03:00  … variante spread_menos_1, spread_menos_2 y sin_spread, otra vez, con el recuento por fuente (revisor, b1)
03:03   uv run python -B docs/validation/anexos/PUENTE-TECHO/puente.py todo docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/cuenta-por-mes.txt > docs/validation/anexos/PUENTE-TECHO/todo.txt   (otra vez, con el guion final)
```

En las líneas con «…», el comando es `uv run python -B docs/validation/anexos/PUENTE-TECHO/puente.py
variante <nombre> docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/cuenta-por-mes.txt >
docs/validation/anexos/PUENTE-TECHO/<nombre>.txt`, literal, con el nombre de la línea.

## Exposiciones de cada día

- **2026-11-23:** la fila de la apertura de `HOLDOUT-EXPOSICIONES.md` (con la línea del auditor del
  encargo en la configuración del kit) y §0.8.
- **2026-11-24:** la fila de ese día: los `make check` (marzo y junio para calentar, como todos),
  `puente.py` y su test sobre los días dev de construcción sin calentamiento y los casos dev por la
  ingesta, y el revisor. **Una desviación:** el guion de diagnóstico de D2 c (un día dev de julio,
  dentro del 1 al 17; motivos e instantes, sin precios) se declaró el mismo día pero DESPUÉS de
  correrlo (su punto 3 bis lo dice); el encargo pide «antes de hacerla» (revisor, b4). No es material
  reservado. Nada más: ningún libro, imagen, fotograma, transcripción ni cruda, nada de mayo y ningún
  mensaje del trader.

## Lo que se hizo con los hallazgos del revisor

| # | Gravedad | Lo hecho |
|---|---|---|
| a1 | importa | Arreglado en §0.4 b.3: el lote sale del saldo y el margen del cierre de la M1 anterior y del precio de conversión del instante del caso; `abrir_conocida` avanza después hasta ese instante. El efecto de una posición que se cerrara en ese tramo no está medido, y se dice. |
| a2 | menor | Arreglado: las filas de 5 USD están en `VIABILIDAD-COMISION.md:111-112`. |
| a3 | menor | Arreglado en §0.4 b.3: `posiciones_del_bot` toma el riesgo de la orden; el guion, de la entrada y el stop de apertura; coinciden en lo que compara D2 c. |
| a4 | menor | Arreglado: `lectura.txt` copia tal cual sus líneas de `todo.txt` y añade la cabecera y un título, y el informe lo dice. |
| a5 | menor | Arreglado: fuera la línea «PLANTILLA hasta la fase 0»; el Estado, al día. |
| b1 | importa | Arreglado: `puente.py` imprime los eventos por fuente en las tres variantes de spread (D3 lo pide; D5 dice «nada más», y gana D3 por ser la pieza); se repitieron las tres (cada salida cambia solo en esa línea: `git diff`) y `todo`. |
| b2 | importa | **No arreglado; dicho.** El test de humo prueba las piezas puras (el tope, el objetivo, el desfase, el ASK, el stop al 0,8), D2 c por la orden stop y por `abrir_conocida`, RN-002 con y sin la H4 y la clasificación del break even, pero no pasa por `repetir` el interruptor del break even ni el del tope: haría falta un entorno sintético con una M1 que complete la zona de RN-014. Las salidas reales lo muestran (`sin_break_even`, «break even movido: 0»; `sin_las_de_mas_de_100_lotes`, «fuera por el tope de lotes: 8»), pero no son el test. Queda para tu decisión. |
| b3 | importa | Arreglado: la lista de comandos, con los literales y su hora, de §«Los comandos ejecutados». |
| b4 | importa | Arreglado: la desviación, en «Exposiciones de cada día» y en la fila de §6. |
| b5 | importa | Arreglado: la respuesta del consultor a la PARADA de apertura, tal cual, en la apertura y al final del encargo. |

## Informe del revisor

> ## Informe del revisor · trabajo/puente-techo · 2026-11-24
>
> Base: `git merge-base main HEAD` = 8a10590b. Seis commits (0f021d68, 5974d36d, 613aa40c, 6ba82dee, f042fa10, da15d984), más la fase 5 estadiada (MASTER_PLAN.md +7, RUMBO-2026-11.md +2, PUENTE-TECHO.md +11). No hay ficheros sin seguir. Mientras revisaba corría un `make check` (empezó a las 02:31; el log lleva la línea «G2 … 2026-11-24 … estadiada» y aún no tiene SELLO), así que no ejecuté Python, pytest ni make.
>
> ### Eje (a) · Reglas de la casa
> Resumen: 0 bloquea, 1 importa, 4 menor.
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | a1 | importa | El informe describe la apertura de `entrada_al_precio_del_caso` como algo que el código no hace. El informe dice «el guion avanza el bróker hasta el milisegundo anterior al instante del caso y abre allí … con el lote del riesgo calculado con la cuenta de ese momento». El código calcula el saldo, el margen libre y el lote con el bróker y la cuenta en `hasta_ms`, que es el cierre de la M1 anterior. Después `abrir_conocida` avanza el bróker por su cuenta hasta `instante_ms`. Si en ese tramo de menos de un minuto se cierra otra posición, el lote sale del saldo anterior. Nadie ha medido el efecto (ninguna corrida tiene rechazos). Hay que corregir la frase, o medir y decir que no cambia nada. | PUENTE-TECHO.md:164-167; puente.py:484 (saldo), :494-497 (`_lote_final` en el estado de `hasta_ms`), :510-512; broker.py:673 y :1109-1112 (`_avanza_reloj` → `avanzar(instante_ms)`) |
> | a2 | menor | Cita desplazada una línea: las filas de 5 USD de V1 y V2 están en :111-112, no en :112-113. | PUENTE-TECHO.md:217; `grep -n "^\| 5 \| V[12] " VIABILIDAD-COMISION.md` → 111 y 112 |
> | a3 | menor | El informe dice que el riesgo de `posiciones_del_bot` es «lotes × distancia de la entrada al stop de apertura». En realidad usa el precio y el stop de la ORDEN. D2 c no puede notar la diferencia, porque solo compara las 124 posiciones con entrada igual al precio de la orden (puente.py:986). | PUENTE-TECHO.md:159-161; cableado.py:1352 `riesgo = o.lotes * Decimal(abs(o.precio - o.stop)) …` |
> | a4 | menor | `lectura.txt` se llama «extracto literal» de `todo.txt`, pero lleva dos líneas que `todo.txt` no tiene: la cabecera y «## El cierre del puente (ADR-0099 §2), sobre abril y agosto». | `diff <(sed -n '353,380p' todo.txt) lectura.txt` → `0a1 >` y `1a3 >`; PUENTE-TECHO.md:511 |
> | a5 | menor | El informe arrastra dos frases viejas. Sigue la línea «PLANTILLA hasta la fase 0», y el Estado dice «siguen la fase 5 y el revisor» con la fase 5 ya estadiada. | PUENTE-TECHO.md:3 y :630 |
>
> Comprobado sin hallazgos:
> - **Contrato:** no lo ejecuté. Todas las rutas del diff están en `rutas_permitidas` (contrato.yaml:5-21). Ninguna está en `rutas_protegidas`.
> - **Trailers `Fuente:`:** no aplican; ningún commit toca `knowledge/spec` ni `knowledge/cases` (`git diff --stat main...HEAD`).
> - **Holdout y material:**
>   - Nada toca `knowledge/cases/holdout/`.
>   - Hay fila del 2026-11-23 y del 2026-11-24 en HOLDOUT-EXPOSICIONES.md (:189-190).
>   - No hay fotogramas, transcripciones ni libros.
>   - No hay agregados de meses reservados en las salidas.
> - **Regímenes de cambio:** no hay nada en evidence, feedback, manifests ni corpus. Solo se añaden líneas (numstat «N 0») en HISTORIA.md (181), HOLDOUT (2), 0092 (2), 0098 (2), MASTER_PLAN (7) y RUMBO (2).
> - **Ambigüedades:** no se cambian.
> - **ADR-0099:** su `## Estado` empieza por `ACTIVE` (0099:296-298).
> - **Informes cerrados:** no se edita ninguno. Los `docs/validation/*.md` del diff son nuevos, salvo HOLDOUT, que solo añade filas.
> - **Sitios con `cita`:** la rama no añade ninguno.
> - **Cifras:** puente.py no lleva ninguna cifra de los yaml. Las piezas con número se componen desde `propios` (:116-127) y se cotejan con el yaml (:1045).
> - **Citas comprobadas contra su fuente:**
>   - cableado.py:1341-1343 (`if o is None: continue`): correcta.
>   - primitivas_broker.py:197-201 (`clasificar_cierre`): correcta.
>   - broker.py:1118-1121 (`ordenes_simultaneas_max`): correcta.
>   - viabilidad_trader.py:50 y :380-381 (`DESFASE_PUNTOS`): correcta.
>   - viabilidad_comision.py:66-83 (`niveles()`): correcta.
>   - VIABILIDAD-COMISION.md §2 (7 y 10 fuera con 5 USD, :91-94): correcta.
> - **PROJECT_STATE:** 24.728 bytes en la rama y 24.680 en main, como dice el informe.
>
> ### Eje (b) · Encargo
> Resumen: 0 bloquea, 4 importa, 0 menor. Requisitos: 32 hechos, 4 parciales, 0 no hechos. El revisor pegado al final del informe queda pendiente por diseño.
>
> | # | Requisito | Estado | Evidencia |
> |---|---|---|---|
> | 1 | Base, tag, CI y ramas comprobados; tag F39m libre | Hecho | PUENTE-TECHO.md:13-18 |
> | 2 | Modelo y REAP | Hecho | :19 |
> | 3 | Fila de HOLDOUT antes de todo, y la del día nuevo | Hecho (el punto 8 se corrigió con lo medido, y se declara) | HOLDOUT:189-190; PUENTE-TECHO.md:37-42, :255-259 |
> | 4 | Cuatro ficheros: sha256 y lectura entera | Hecho (hubo una PARADA por el ADR, resuelta) | :21-36 |
> | 5 | Contrato pedido (R4, riesgo medio, artefacto, rutas) | Hecho | contrato.yaml |
> | 6 | Encargo copiado, bloque `ids-inexistentes` y su retirada en el pre-registro | Hecho | `git show 613aa40c -- docs/encargos/…` |
> | 7 | Antes del pre-registro, el id solo en el encargo | Hecho (contrato.yaml lleva el glob `docs/adr/0099-*.md` porque el encargo lo pide) | `git diff main 5974d36d` → solo contrato.yaml:11 |
> | 8 | Fase A: cabecera y cuerpo tal cual | Hecho | `tail -n +12 … \| cmp -` → 0 (profunda); `tail -n +13 … \| cmp -` → 0 (cazador) |
> | 9 | P.1: ADR igual salvo dos marcas, diff en el informe | Hecho | `diff Escritorio/ADR-0099-borrador.md docs/adr/0099-…` → solo 3c3 y 294c294, igual que PUENTE-TECHO.md:101-110 |
> | 10 | P.2: yaml byte a byte | Hecho | `cmp` → 0; sha 31e70e0a… el mismo en el Escritorio, el repo y `git show 613aa40c:` |
> | 11 | P.3: test del yaml | Hecho (no lo ejecuté) | tests/unit/test_puente_techo.py:24, :134-168 |
> | 12 | P.4: índice y dos recuadros tal cual | Hecho | `git diff main -- docs/adr/…`: texto idéntico al encargo |
> | 13 | P.5: sha y hora del pre-registro frente a la primera corrida | Hecho | PUENTE-TECHO.md:95, :379-380 |
> | 14 | Fase 0 a-j en su commit | Hecho | 6ba82dee; PUENTE-TECHO.md:131-264 |
> | 15 | README en su commit antes de correr | Hecho | f042fa10 a las 00:46:14, antes de la corrida de las 00:49:07 |
> | 16 | puente.py con sus modos, lee los tres yaml, sin cifras | Hecho (más el modo `conocida`, justificado por D2 c) | puente.py:1050-1109 |
> | 17 | Test de humo: cada pieza en los dos sentidos | Parcial | hallazgo b2 |
> | 18 | D2 a | Hecho | control.txt:4-6 (235 de 235, igual que meta.txt:3-6) |
> | 19 | D2 b | Hecho | `diff <(sed -n '9,29p' base.txt) <(sed -n '8,28p' meta.txt)` → vacío, exit 0 |
> | 20 | D2 c | Hecho, con el arreglo de D12 declarado | conocida.txt:11-12; conocida-antes-del-arreglo.txt:11-14 |
> | 21 | D3, las diez piezas | Parcial: falta el recuento de eventos del respaldo en las de spread | hallazgo b1 |
> | 22 | D4, dieciséis variantes en orden | Hecho | todo.txt (cabeceras de :8 a :366) |
> | 23 | D5 | Hecho | base.txt:33-53 y las demás salidas |
> | 24 | D6, lectura leída del yaml | Hecho | puente.py:219-253; todo.txt:378-380 |
> | 25 | D7 | Hecho | todo.txt:364, :376; PUENTE-TECHO.md:492-498 |
> | 26 | D8 | Hecho | base.txt:30-31 |
> | 27 | D9 | Hecho | `cmp base.txt base-repetida.txt` → 0; sha 6bd49ae0… en los dos |
> | 28 | D10 | Hecho | PUENTE-TECHO.md:430-432 |
> | 29 | Fase 5: dos notas tal cual | Hecho (estadiado, sin commitear) | `git diff --cached`: texto idéntico al encargo |
> | 30 | Informe: apertura y §0 a §6 | Hecho | PUENTE-TECHO.md |
> | 31 | Comandos literales con su hora | Parcial | hallazgo b3 |
> | 32 | Líneas del cierre medidas sobre una copia | Hecho | simular-cierre.txt; simular_cierre.py:160-162 (escribe solo en un tempdir) |
> | 33 | PROJECT_STATE ≤ 24.900 | Hecho (24.740 en el cierre; 24.899 en la rama) | simular-cierre.txt:9 |
> | 34 | Ninguna recomendación de spec ni de motor | Hecho | grep «ecomiend\|habría que\|debería\|mejor»: solo §0.6 (:324-330), opciones de procedimiento |
> | 35 | Toda exposición, ANTES de hacerla | Parcial | hallazgo b4 |
> | 36 | Nada de src/, knowledge/, scripts/, Makefile ni .claude/ | Hecho | `git diff --stat main...HEAD` y `--cached`: ninguna de esas rutas |
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | b1 | importa | D3 pide, para las tres variantes de spread, que «el guion cuente cuántos eventos salen del respaldo». puente.py calcula `por_fuente` en todas las variantes (:551) pero solo lo imprime en `base` (:941-952). Las salidas de spread no lo traen, y el informe no lo declara como «hecho de otra forma». Choca con D5 («nada más»): hay que decirlo y elegir. | encargo:54; sin_spread.txt:8-29 (sin línea de fuentes); puente.py:941-952 |
> | b2 | importa | La fase 1 pide que el test de humo pruebe en los dos sentidos que cada pieza cambia lo que dice («el break even que se mueve y que no; la operación de más de 100 lotes que entra y que sale»). El test de BE mueve el stop a mano y solo prueba la clasificación; nunca pasa por el interruptor de `repetir`. El del tope prueba la función pura. `entrada_al_precio_del_caso` solo se prueba por D2 c. El informe da el punto por «Hecho; 15 passed». Las salidas reales (BE movido 0 en sin_break_even; fuera 8) lo atenúan, pero no son el test. | test_puente.py:107-113, :208-232 (`b.mover_stop` a mano); puente.py:457, :491; PUENTE-TECHO.md:589 |
> | b3 | importa | El encargo pide «los comandos literales ejecutados con su hora», y la lista no los trae todos. Hay plantillas («conocida ... > conocida.txt», «variante <nombre> ... > <nombre>.txt»). Faltan con su hora: pytest del test de humo, ruff y mypy, el guion de diagnóstico de D2 c, la tercera corrida de la base (LF), el guion que pasó las salidas a LF y el sed/diff de D2 b. | PUENTE-TECHO.md:603-616 |
> | b4 | importa | El guion de diagnóstico de D2 c se declaró en HOLDOUT después de correrlo. La fila lo dice: «3 bis, escrito el mismo día DESPUÉS de correrlo». Cumple el «mismo día» de CLAUDE.md (era un día dev de julio dentro del 1 al 17), pero no el «ANTES de hacerla» del encargo. El informe no lo cuenta entre las desviaciones ni en la fila de ERRORES de §6. | HOLDOUT-EXPOSICIONES.md:190 («(3 bis, escrito el mismo día DESPUÉS de correrlo»); encargo:141; PUENTE-TECHO.md:556-564, :625-626 |
> | b5 | importa | La respuesta del consultor a la PARADA de apertura (el sha del borrador) va parafraseada en el informe («era una versión anterior; Aleks dejó la buena»), no copiada tal cual. Tampoco está al final del encargo, que acaba en «Rama lista para revisión, NO cerrada.». | PUENTE-TECHO.md:35-36; docs/encargos/trabajo-puente-techo.md:144 |
>
> **Los ocho alcances del encargo:**
> 1. **Orden del pre-registro:** se cumple. 613aa40c (2026-11-23 23:32:13) es anterior a f042fa10 (00:46:14), y la primera corrida es de las 00:49:07 según el informe. puente.py entra por primera vez en da15d984. El diff del ADR solo cambia 3c3 y 294c294, las dos marcas. El yaml es idéntico (`cmp` 0, sha 31e70e0a…).
> 2. **Los dos controles de D2:** pasan.
>    - El diff del bloque M1, de base.txt:9-29 contra meta.txt:8-28, sale vacío (exit 0). El control da 235 de 235 en los dos.
>    - `repetir` de puente.py (:363-554) frente al de techo_parejas.py (:437-592), con todo apagado:
>      - Firma: añade `piezas` y `dias`; con `None` recorre `ent.dias`, igual que antes (:401 / :472).
>      - RN-002: `predicado_rn002(reg, False)` evalúa los dos predicados y los une con OR, como `_rn002`. Solo cambia el orden de evaluación, y los predicados son puros (tp:763) (:352-358 / :762-766).
>      - Recuentos: van por mes en un Counter y se suman al imprimir, con las mismas claves («al colocar:», «al llenar:») (:304-325 / :363-373).
>      - Mercado: sin pieza de spread es `md.mercado()`, que es `Mercado(self.ticks, self.m1)` (simulacion.py:78-79) (:415-419 / :487).
>      - Contadores nuevos: `horas_con_ticks`, `por_fuente` y los dos de las no colocables son solo de lectura; `ticks_del_minuto` es un `dict.get` (llenado.py:93-94) (:427, :477-480, :551).
>      - Break even: el bloque queda bajo `if not piezas.sin_break_even`, así que con la pieza apagada corre igual (:457).
>      - Colocación: la condición es `not p.conocida and …`, y `conocida` es False en el techo (:473).
>      - Lote: el tope vale None, `lote_forzado` None e `instante_lote` = `hasta_ms`, así que `_lote_final` recibe los mismos argumentos (:485-497 / :546-550).
>      - Objetivo: `base_del_objetivo` con la pieza apagada da `caja` si `caja_completa` y si no `|entrada - stop|`, igual que tp:554 (:504-507).
>      - El resto del día es idéntico.
>      - `pedidos_del_techo` (:720-763) frente a `techo` (:783-815): con `Piezas()` da la misma entrada, el mismo stop, la misma `caja_derivada` y el mismo minuto `int(timestamp)//60`.
>      - `filas()`, sin conocidas, devuelve `tp.filas_de` (:617-618), y el filtro `riesgo > 0` es el mismo (:770 / :816).
>    - Conclusión: con todo apagado el bucle es equivalente, y el diff vacío de D2 b lo confirma.
> 3. **Las piezas de D3:** cada una cambia solo lo que dice.
>    - objetivo: :189-193.
>    - BE: :457.
>    - entrada: :473, :494, :508-516; sin no colocables ni no llenadas.
>    - tope antes de limitar: :488-493.
>    - desfase en los dos lados, con la distancia intacta: :180.
>    - spread solo en `Tick.ask`, nunca por debajo del bid; la M1 del respaldo intacta: :196-212 y llenado.py:115-118.
>    - sin_cierre_h4: :355-356; el fin de día sigue en :532-536.
>    - stop al 0,8 con el redondeo de `niveles()`, el lote sobre esa distancia y el objetivo sobre la caja original: :183-186.
>    - Salvedades: a1 (cuándo se calcula el lote de `abrir_conocida`) y b1.
> 4. **Lo prohibido:** las salidas no imprimen ninguna operación con su R, ningún R por setup, sesión o dirección, ningún precio, vela ni nivel. Lo único por operación es conocida-antes-del-arreglo.txt:12-13 (día dev de julio dentro del 1 al 17, id y el campo «cerrada»), sin R. El bloque de julio solo sale en base, como permite el encargo.
> 5. **Las tablas de §2:** coinciden con las salidas en las cinco variantes que comprobé (base, sin_spread, todo_junto, de_vuelta_sin_break_even y v2_de_hoy), en las dos tablas y columna a columna. Además, los bloques de `todo.txt` son iguales a base.txt, todo_junto.txt, sin_spread.txt y v2_de_hoy.txt (diff 0).
> 6. **Rutas intocables:** ni src/, ni knowledge/, ni scripts/, ni .claude/, ni el Makefile. En tests/ solo entra tests/unit/test_puente_techo.py.
> 7. **Fechas:** en las líneas añadidas (lo commiteado y lo estadiado, auditorías incluidas) no hay ninguna fecha con día de 2025, febrero, marzo, mayo o junio de 2026, ni de julio del 18 en adelante. De 2025 solo aparecen meses sin día. Las fechas de septiembre, octubre y diciembre de 2026 son todas de sucesos del repo: sesiones, ADR, ramas, commits, nombres de fichero o ids, y la fecha prevista de los ingenieros. La media de un subconjunto retirada de la auditoría no queda en el texto (grep de su valor: 0). Lo que no pude es cruzarlas con `casos_reservados` (ver abajo).
> 8. **Recomendaciones:** el informe no recomienda ningún cambio de spec ni de motor. Las tres «Recomiendo (a)» de §0.6 son de procedimiento.
>
> ### Lo que no pude comprobar
> - `uv run python scripts/contrato_rama.py` y las demás comprobaciones del contrato: son Python y corría un `make check`. El make-check.log está a medias (sin SELLO ni PICO DE MEMORIA), así que no hay sello del árbol estadiado de la fase 5.
> - Los 15 passed del test de humo, los 6 de test_puente_techo.py, ruff y mypy: no los ejecuté.
> - La hora de la primera corrida (00:49:07): solo la da el informe; git no la guarda.
> - La tercera corrida de la base con el guion en LF, y la comparación de los 16 bloques de `todo.txt` con un guion de la carpeta de trabajo: no están en el repo. Comparé cuatro bloques a mano.
> - El cruce de las fechas de septiembre y octubre de 2026 con los días de `casos_reservados(repo)`: es Python y toca la lista reservada. Las juzgué por su contexto.
> - El efecto real del hallazgo a1 sobre las cifras: haría falta correr puente.py.
>
> [Comandos: 22 entradas, todas de lectura (git log, show, diff y diff --cached; diff, cmp y sha256sum contra el Escritorio; sed, grep y cat -A sobre las salidas y el código; Read de los ficheros citados). Un `for` lo negó la guardia; no lo reescribió para esquivarla y usó `git log --stat`. La cuenta de CR con `$'\r'` también la negó; no la repitió.]

## Estado

Entregado el 2026-11-24: la lectura del puente es «solo_juntas» (las ocho sueltas dan no_gana y
todo_junto no_concluyente); el cierre cierra con V1 y V2. Rama lista para revisión, NO cerrada.
