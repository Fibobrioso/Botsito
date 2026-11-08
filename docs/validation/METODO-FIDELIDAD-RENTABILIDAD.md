# METODO-FIDELIDAD-RENTABILIDAD · el método con el que se juzga al bot (ADR-0092)

Rama `trabajo/metodo-fidelidad-rentabilidad`, abierta el 2026-11-07 desde `main` e01e28c
(tag `stable/F38q-sello-respaldo-m1`, merge 18f548e). Encargo:
`docs/encargos/trabajo-metodo-fidelidad-rentabilidad.md`. Tramo «R3 · Una corrida del arnés sobre
toda la construcción» (R3.7 de la hoja de ruta; R de la Next Action).

## 0. La base, comprobada con git al abrir

- `git rev-parse HEAD` en main = `e01e28cb72bf3a9c16c5cb975fa4cda27895e627`; `origin/main` el mismo
  (`git fetch origin --prune`; `git ls-remote --heads origin` solo da `refs/heads/main`).
- `git rev-parse "stable/F38q-sello-respaldo-m1^{commit}"` = `18f548e11447455f0bed34bea4e9d022752416e1`
  = `git rev-parse main^1`; el tag esta en origin (`git ls-remote --tags origin`, objeto 12703cc).
- `gh run view 42400168427 --json headSha,status,conclusion,headBranch,name`:
  `{"conclusion":"success","headBranch":"main","headSha":"e01e28cb72bf3a9c16c5cb975fa4cda27895e627","name":"ci","status":"completed"}`.
- `git branch -a`: solo `main` y `origin/main`; `git ls-remote --heads origin "fix/*"` vacio.
- `grep 0092` en `docs/` y en `PROJECT_STATE.md`: ningun ADR-0092 (solo trozos de shas y de offsets).
- Modelo: Opus 5.5, el que pide el encargo.
- El primer `make check` de la apertura salió en rojo: 5 tests de `knowledge validate` (3252
  pasaron), porque este informe citaba ADR-0092 en su título sin su propio bloque `ids-inexistentes`
  (el bloque exime el id solo en el documento que lo lleva, `validation/ids_citados.py:23-26`; lo
  cazó también el auditor, H1). Añadido el bloque, `knowledge validate` exit 0. Es la trampa de la
  memoria «make check: ids futuros»: se comprueba ANTES de los 20 minutos.
- El segundo `make check` salió en verde (3257 passed) pero **no selló**: «ficheros sin seguir
  fuera de .gitignore (1): knowledge-validate.log», el log de la comprobación del contrato, que
  escribí en la raíz del repo y nunca se ha commiteado (`git ls-files knowledge-validate.log`: 0).
  Borrado, el tercero selló el commit de apertura. Desde ahí, ese log va a la carpeta de trabajo
  de la sesión, fuera del repo.

## Fase 0 · inventario sin tocar código ni knowledge/ (2026-11-07)

Todo lo de esta fase es lectura del código y de documentos, más recuentos sobre las DOS salidas ya
commiteadas de `docs/validation/anexos/RESPALDO-M1/`: `cuenta-arrastrada.txt` (la línea base
vigente, ADR-0070 punto 3, NOTA del 2026-10-29) y `diaria.DIAGNOSTICO.cuenta=diaria.txt` (un
diagnóstico que por ADR-0070 punto 3 no cuenta; cada cifra que sale de ella lo dice). **Ninguna
corrida del arnés y ninguna cifra agregada nueva del bot.** Los guiones de recuento están en la
carpeta de trabajo de la sesión y pasan al anexo `anexos/METODO-FIDELIDAD-RENTABILIDAD/` en la fase
1, punto 3 (el encargo lo pone ahí): `recuentos_vistos.py` (c y e), `huecos_material.py` (c),
`recuento_compuerta.py` (la compuerta) y `simular_cierre.py` (h).

**Aviso del auditor que vale para todo c) y e) (afirmaciones 14 y 16).** La línea base es de un
motor anterior: anterior a la activación de la sesión 6 en el motor (F38o), a la comisión medida de
ADR-0090 (2,50 por lote y lado; aquella corrió con 5) y al sello de ADR-0091. La lección 2 de F38q
sigue: «una lista que va a decidir algo se saca del código vigente, no de una salida vieja»
(`ERRORES-RECURRENTES.md:111`). Por eso lo que sale de esas salidas aquí es DESCRIPTIVO, y ninguna
decisión de la PARADA se apoya solo en ello: el camino de la cuenta se decide sobre el código y los
huecos del material (medidos con los manifiestos), y las tolerancias, sobre una regla.

### 0.a Lo que ya mide el simulador y escribe el arnés, para la rentabilidad

Dónde se escribe cada sección de la salida: el arnés (`engine/arnes.py:358-433`, `informe`) y,
con `--simular`, la cola del cableado (`engine/cableado.py:727-794`, `informe_simulacion`, más
`_informe_ordenes` y `_informe_peticiones`).

| Pieza | Qué hace hoy el simulador | Dónde se escribe | Desde la salida |
|---|---|---|---|
| Resultado de cada operación, en USD | la cuenta abre la posición al llenarse y la cierra al precio de cierre (`cableado.py:421-439`); el bróker guarda `precio_cierre` (`cableado.py:433`) | **no se escribe**: «Eventos del broker» lleva solo `dia | instante | tipo | id | fuente` (`cableado.py:774-783`) y «### Ordenes» el precio de la ORDEN, no el de cierre (`cableado.py:804-808`) | **columna nueva** |
| Comisión | se carga al llenar (`comision_por_lote × lotes`, `cableado.py:428-429`) y, si `comision_por_lado`, otra vez al cerrar (`:434-435`) | solo dentro del saldo de la curva | columna nueva (por operación) |
| Swaps | se cargan al cerrar, con su instante (`cableado.py:436-438`) | solo dentro del saldo de la curva | columna nueva (por operación) |
| Resultado en R | no existe; el riesgo al colocar sí: «riesgo (% del saldo)», «lote», «distancia (puntos)» de «### Ordenes» (`cableado.py:804-808`, `:813-820`) | el riesgo sí; el resultado no | **columna nueva** (el PnL neto entre el riesgo en USD al colocar) |
| Desenlace (ganancia, pérdida, break even) | el motor lo clasifica en cada cierre con `clasificar_cierre` (`primitivas_broker.py:184-188`; `cableado.py:440-446`) y lo usa para los cartuchos y la racha, pero **no lo escribe** | se reconstruye a medias cruzando «Eventos» con «Ordenes» (0.d) | guion que cruza secciones, o columna nueva |
| Saldo al corte, saldo final y equity mínima de cada día | `curva_de_equity` (`cableado.py:534-545`): un `DiaDeCuenta` por día corrido | «### Curva de equity» (`cableado.py:767-769`) | **tal cual** |
| Drawdown diario máximo, en la magnitud que vigila la firma | la cuenta vigila `firma_magnitud_vigilada` = `equity` (`ftmo-2step-swing-100k.yaml:256-266`; `cuenta.py:312`) contra `saldo_corte − 5 % del capital` (`firma_perdida_diaria_max` "5", `:208-221`; `firma_base_perdida_diaria` = `saldo_corte_diario`, `:222-233`; `cuenta.py:316-317`) | la curva trae `saldo al corte` y `equity minima` de cada día | **guion de una sola sección** (la curva): (saldo al corte − equity mínima) / capital, por día; con «-» en la equity mínima, el día no tuvo posición |
| Drawdown total máximo | límite estático (`firma_perdida_total_max` "10", `firma_perdida_total_arrastra` false, `:234-255`; `cuenta.py:321-322`) | la curva | **guion de una sola sección**: capital − la menor equity mínima (o saldo) de la curva |
| Frenos y suspensión de la firma | RN-030 cierra a mercado al acercarse a un límite (`strategy_spec.yaml:2424`); RN-032 no abre una operación cuyo riesgo no cabe (`:2529`; la suma prospectiva, `primitivas_broker.py:336-341`); la suspensión es el estado SUSPENDIDA de la cuenta (`cuenta.py:482`) | «PRIMERO EN TOCAR UN LIMITE» (`cableado.py:743`) y «### Veredicto de la cuenta sobre el tramo» (`:755-766`); lo que RN-032 bloquea sale en la columna `bloqueadas` de «Por sesion» (`arnes.py:330-335`) | tal cual |
| Objetivo de la fase reto | `firma_reto_objetivo` "10" y 4 días mínimos (`ftmo-…yaml:101-133`); la cuenta da SUPERADA en el primer cierre que deja el saldo en la meta sin posiciones vivas (`cuenta.py:373-385`) | «estado», «motivo», «dias de trading» del veredicto (`cableado.py:757-766`) | tal cual |

Lo que el encargo pide verificar, verificado: la columna «resultado» de «### Por operacion» es el
EMPAREJAMIENTO (`cuenta-arrastrada.txt:439`; todas sus filas dicen PAREJA o SIN PAREJA, la escribe
`arnes._fila` desde `diferencias_por_operacion`, `arnes.py:525-532` y `:614-662`), y no hay columna
de PnL en USD por operación ni en esa tabla ni en «### Ordenes» ni en «Eventos». En «Eventos»
aparecen exactamente los cinco tipos `llenada`, `stop`, `stop_movido`, `objetivo` y `manual`
(`cuenta-arrastrada.txt:779-911`).

En resumen: **el drawdown diario y el total ya se calculan desde la salida, con un guion sobre la
curva; la esperanza en R después de costes pide una columna nueva por operación** (PnL neto en USD
con comisión y swaps, y R neto), porque ni el precio de cierre ni el coste de cada operación salen.
Ninguna cifra calculada aquí.

### 0.b La fidelidad por criterios: qué se puede comparar pieza a pieza

**Lo que trae el caso del trader.** `cases/ingesta.Operacion` (`ingesta.py:116-121`): `instante_utc`
(el llenado, `INSTANTE-LLENADO-SALIDA.txt`), `sesion`, `direccion`, `entrada` y `stop`. Nada más.
Y el arnés **descarta el stop** al leer el caso: `arnes._operacion` construye la `Operacion` del
criterio (`criterio_fidelidad.py:45-50`), que no lo tiene (`arnes.py:124-131`; auditor, 40).

**Lo que se deriva** (con su condición):
- **el 0 de la caja** = la entrada: el 0 es `Zona.entrada` (`engine/zonas.py:134-142`; ADR-0058),
  y el trader entra con la orden en el 0 (ADR-0056);
- **el 1 de la caja**, del stop en el 0,8 (`stop_fraccion_caja` "0.8", `parametros.yaml:602-616`;
  ADR-0073): distancia completa = |entrada − stop| / 0,8. **Matiz del auditor (41, H7):** esa
  derivación es la que A-56 discute; en 26 de 38 ganadoras el material da un RR dentro de
  [3,00, 3,75), que con el stop exactamente en el 0,8 tendría que caer fuera
  (`ambiguedades.yaml:1886-1901`). La caja derivada del caso es, por tanto, una lectura sujeta a
  A-56, no una medida;
- **el punto**: es la clave `nivel@inicio` de la vela contraria (ADR-0083; la columna «punto» de
  «### Ordenes», p. ej. `117206@29455921` con precio 1.17206, `cuenta-arrastrada.txt:913`). Su
  NIVEL es el del 0, así que se compara como la entrada; su INICIO (qué vela) no sale de la entrada
  ni del stop.

**Lo que no trae:** la liquidez de M15 que se tomó (ni su nivel ni su instante), la vela del
breaker ni el bloque. Solo existen en el vídeo de los libros grabados (0.d).

**Lo que trae el bot.** La operación del criterio (día, sesión, dirección, instante del llenado,
entrada; `cableado.py:460-483`); por orden, en «### Ordenes», el precio, el resultado (colocada,
llenada, cancelada, rechazada), el lote, la distancia al stop en puntos, el riesgo, el punto y el 1
de la caja (`cableado.py:804-808`, `:813-820`); en el embudo, qué hechos de origen `regla` produjo
cada sesión con operaciones del trader (`sesgo`, `orden_dimensionada`, `liquidez_tomada` y los
frenos `detenido_por_*`, ADR-0048 punto 5, `arnes.py:382-388`); el sesgo de RN-003 de cada sesión
(`arnes.py:323-335`); y en memoria, no en la salida, las zonas con su 0, su 1, su `por` y su
instante (`cableado.py:695-706`, solo para el visor). El nivel de la liquidez de M15 que tomó el bot
no se escribe: el embudo solo dice `liquidez_tomada:si`.

**Los patrones** (cabecera de `anexos/RESPALDO-M1/patrones.py:16-41`, la clasificación del
consultor en `CORRIDA-CONSTRUCCION.md:1206-1228`): T0 pareja; P1 contra el sesgo; P7 entrada
repetida ya emparejada; P2 mismo lado a ≤ 15 min y > 3 puntos (la caja); P3 mismo lado a > 15 min
(otra zona o liquidez); P4 sin orden; P5 bot de más; P6 donde el trader no operó (más «P? solo otro
lado» y la marca «posible M»).

| Criterio | Del trader | Del bot | Comparable hoy |
|---|---|---|---|
| Sesión y dirección | en el caso | operación y orden | **pieza a pieza** (ya lo hace el criterio por operación) |
| Sesgo de H4 | no en el caso; se infiere de la dirección | rn003 de cada sesión | **derivada**: P1 la mide (dirección contra sesgo) |
| La entrada (el 0) | `entrada` | precio de la orden y del llenado | **pieza a pieza** |
| El instante | `instante_utc` (llenado) | llenado; colocación de la orden | **pieza a pieza** (llenado contra llenado) |
| El stop (el 0,8) | `stop`, pero el arnés lo tira | precio ± distancia al stop de «### Ordenes» | **pieza a pieza**, si el arnés lleva el stop del caso (hoy no: tocaría `arnes._operacion` o un lector propio en `cases/`) |
| La caja (el 1) | derivada de entrada y stop, sujeta a A-56 | «caja 1» de «### Ordenes» | **derivada** |
| El punto | su nivel = la entrada; su vela, no | «punto» (`nivel@inicio`) | **derivada** por el nivel; la vela, **no** |
| La liquidez de M15 | no está | solo `liquidez_tomada:si/no`; su nivel no se escribe | **no comparable** con el material de los casos; solo con el vídeo, en los libros grabados, y a mano |
| Stop, TP, gestión | — | — | ADR-0043 los dejó fuera por A-18 y A-31 (hoy RESUELTAS), ADR-0037 §7 y A-13 (ABIERTA) (auditor, H6): el stop puede entrar; TP y gestión siguen fuera |

### 0.c El camino de la cuenta (sesgo 2)

- **Cómo itera.** `cli.py:2391` toma los días con `arnes.dias_de_construccion`, que pasa por
  `validar_meses` y ORDENA los meses (`arnes.py:107-121`): aunque el yaml los lista
  `["2026-04", "2026-07", "2026-08", "2026-01"]` (`criterio_fidelidad.yaml:40`), la corrida va
  2026-01 → 04 → 07 → 08 (`cli.py:2447`, `tuple(sorted(set(meses)))`; la curva de la línea base
  sale en ese orden, `cuenta-arrastrada.txt:702-777`). `arnes.correr` llama a
  `motor.correr_dia` día a día (`arnes.py:226-234`).
- **Qué arrastra.** `MotorCableado` guarda entre días la cuenta (`CuentaViva`: saldo, saldo al
  corte, días de trading, estado), el seguidor del tope del trader y la racha de pérdidas de
  RN-036, y el primer límite tocado (`cableado.py:219-228`); solo se crean si son `None`
  (`:251-254`, `:267-270`), y `cuenta_diaria` (el diagnóstico) los pone a `None` cada día
  (`:249-250`). El bróker y el estado de estrategia son nuevos cada día (`:256`, `:289`), y lo que
  queda vivo al final del día se cierra o se cancela (`:355-366`): **ninguna posición pasa de un
  día a otro**. Lo fija ADR-0053 §6 («La cuenta PERSISTE en todo el tramo», ADR-0050, ADR-0049 H6;
  auditor, H2).
- **Entre meses no contiguos la cuenta sigue como si fueran días seguidos**: la cuenta corta todos
  los días de calendario que cruza entre dos días corridos (`curva_de_equity`, `cableado.py:535-538`),
  así que febrero, marzo, mayo, junio y julio del 18 al 31 pasan sin operar con el saldo y el límite
  total (estático, desde el capital) intactos.
- **RN-032** (`strategy_spec.yaml:2529-2548`; la lectura prospectiva en `primitivas_broker.py:336-341`):
  no se abre una operación si la pérdida de la firma más su riesgo llega al límite menos
  `firma_margen_seguridad` ("0.5", `parametros.yaml:1886`). No detiene nada: prohíbe operación a
  operación. En la línea base el saldo queda en 90.652,93 el 2026-01-20 (`cuenta-arrastrada.txt:714`)
  y no vuelve a cambiar (`:715-777`): con la pérdida total en 9.347,07 sobre 100.000 y el límite en
  10.000 − 500, ninguna operación cabe y la cuenta no puede recuperar holgura, porque no opera. Está
  EN_CURSO, no SUSPENDIDA (`:694`, `:691`).
- **Recuento sobre una salida ya vista** (`recuentos_vistos.py` sobre `cuenta-arrastrada.txt`; la
  «congelada» es: posterior al último día con alguna orden del bot):

  | | |
  |---|---|
  | último día con alguna orden del bot | 2026-01-20 (13 días con órdenes) |
  | días de la curva posteriores | 63, todos con saldo 90652.9300000 y sin equity mínima |
  | operaciones del trader en la salida | 198 |
  | **operaciones del trader en días con la cuenta congelada** | **165**: enero 21, abril 35, julio 67, agosto 42 |
  | operaciones del trader el mismo 2026-01-20 | 1 |

  Contraste descriptivo (la diaria, que no cuenta): ahí la cuenta empieza de cero cada día y no
  congela (`RESPALDO-M1.md:777-778`).
- **Dónde tiene huecos el material** (`huecos_material.py`: las fechas de los 76 días dev por la
  compuerta y las fechas sin datos de los manifiestos M1 de los CUATRO meses de construcción; los
  meses de fuera no se leen):

  | Hueco | Días de mercado sin correr en meses de construcción | Meses de fuera por medio |
  |---|---|---|
  | 2026-01-30 → 2026-04-01 | 0 | 2026-02, 2026-03 |
  | 2026-04-29 → 2026-07-01 | 1 (el 30 de abril) | 2026-05, 2026-06 |
  | 2026-07-17 → 2026-08-03 | 10 (julio del 20 al 31) | — |

  Tres huecos y cuatro tramos de días seguidos; **dentro de ningún mes de construcción hay un hueco**.
- **Las dos formas.**
  - *«La cuenta se reinicia donde el material tiene un hueco de días de mercado»*: una CONDICIÓN
    del recorrido (entre dos días corridos hay al menos un día de mercado sin correr), no una
    opción. Toca `arnes.correr` o `MotorCableado.correr_dia` (poner cuenta, seguidor y racha a
    `None` en el hueco, como hace hoy `cuenta_diaria`, `cableado.py:249-250`), necesita saber qué
    es un día de mercado (los manifiestos o el calendario de cierres del perfil, ADR-0068) y
    enmienda ADR-0053 §6. Sobre la construcción de hoy da 4 cuentas.
  - *«Una cuenta por mes»*: la misma maquinaria, con la condición «cambia el mes». Sobre la
    construcción de hoy da **las mismas 4 cuentas**. Se separan en el material futuro: un mes con
    un hueco dentro, o un mes de MEDIDA, donde los días dev y los reservados se intercalan (con «por
    hueco», cada día reservado reiniciaría la cuenta; con «por mes», no).
  - Ninguna de las dos es una opción de línea de comandos, así que **ninguna entra en
    `OPCIONES_QUE_NO_CAMBIAN_LA_CORRIDA`** (`arnes.py:80-82`): la lista no cambia. Si se hiciera
    opción, habría que decidir si entra; como condición escrita en un ADR, la corrida que cuenta la
    lleva siempre.
  - Las dos **cambian lo que el motor decide** (el saldo dimensiona el lote y RN-032 lee la pérdida
    acumulada), así que no caben en esta rama, cuyo encargo dice que ninguna decisión del motor
    cambia: ADR-0092 puede fijarlo y la rama de motor que lo implemente va antes de la re-corrida
    que cuenta, o la re-corrida lo implementa. Lo decide la PARADA (punto 6).
- **Lo que no se puede saber sin correr** (auditor, «Lo que no pude comprobar»): si con la comisión
  de 2,50, el sello de ADR-0091 y el motor de F38o RN-032 seguiría congelando la cuenta el
  2026-01-20. No hace falta para decidir el camino: el arrastre entre meses no contiguos es un
  hecho del código, no de la cifra.

### 0.d El material sin vídeo (sesgo 3)

**La clase de cada libro de construcción** (`ACTIVAR-SESION-05.md:288-312`, contrastado hoy con
`knowledge/corpus/libros.yaml:18, :30, :54, :69`):

| Libro | Grabado en vídeo | Clase para S-14 |
|---|---|---|
| Enero 2026 (`libros.yaml:54`) | No (v4 es una entrevista sobre el backtest, `fuentes.yaml:32`) | faltan sesiones de break even |
| Abril 2026 (`libros.yaml:30`) | Solo el 29 (v5, `fuentes.yaml:38-46`) | faltan sesiones de break even, salvo el 29 |
| Julio 2026, 1-17 (`libros.yaml:69`) | Sí, según el trader (v11-v13); sin comprobar hasta T (R2.4) | grabado en vídeo, provisional |
| Agosto 2026 (`libros.yaml:18`) | No el libro que hay (v7 y v8 graban otro backtest; su exportación no ha llegado, NA:Q) | faltan sesiones de break even; cambia si llega Q (auditor, H16) |

S-14: «Solo me he saltado a lo mejor para cuando en una sesión había break events, me lo he saltado.
… pero en los últimos partes que se ha enviado con vídeo y todo pues no» (`ev-v15-011912-0ae32588`),
y el final de v16 lo confirma (`ev-v16-003421-b824b770`).

**Cómo se obtendría el desenlace de cada operación del bot desde la salida** (por lo de 0.a):
- se cruza «Eventos del broker» por (día, id): `llenada oN` abre; el siguiente `stop`,
  `objetivo` o `manual` de `pos-oN` cierra; un `stop_movido` de `pos-oN` antes del `stop` lo
  convierte en break even (es la regla de `clasificar_cierre`: STOP con el stop movido es
  `break_even`, STOP sin moverlo es `salto_el_stop`, y lo demás, ganancia o pérdida por el signo
  del bruto, `primitivas_broker.py:184-188`);
- **`manual`** (un cierre a mercado: el fin de ventana de RN-002 o RN-030) se clasifica por el signo
  del bruto, que pide el precio de cierre, y la salida no lo trae: con un guion, el desenlace de un
  `manual` queda sin definir;
- el lado y el día salen de «### Ordenes»; el libro, del mes del día.
- **Matiz del auditor (37):** el `break_even` del motor es un MECANISMO (saltó el stop ya movido),
  no un PnL cero: con la comisión, un break even del bot pierde dinero, y lo que el trader llama
  break even puede no ser lo mismo (y M, el break even de una venta que salta por el ASK, lo toca).

Por tanto la métrica «sin las operaciones del bot que acabaron en break even en libros sin vídeo» se
puede calcular **con un guion que cruce Eventos y Ordenes**, salvo los cierres `manual`; **con la
columna de desenlace** que pediría 0.a (escrita desde `clasificar_cierre`, que el motor ya ejecuta)
sale entera y sin reconstruir nada. Sin calcularla. Y se toca con la deuda «el `no_trade` por
ausencia no está decidido» y su coletilla de S-14 (`PROJECT_STATE.md:122`; auditor, H8): un día en
que el bot opera y el trader no puede ser una sesión que el trader se saltó.

### 0.e Las tolerancias (sesgo 4): distribución sobre las dos salidas ya vistas

Recuento con `recuentos_vistos.py` sobre `anexos/RESPALDO-M1/`. Tramos: |Δentrada| en puntos de
0,00001; |Δinstante| con los segundos, «0-15» = hasta 15:00 incluido, «16-30» = de 15:01 a 30:00,
«>30» = más. «Bot más cercano» es el que la tabla imprime: el más cercano EN INSTANTE de la sesión,
**sin exigir el lado** (`arnes.py:489-503`; auditor, H15), así que se parte por lado.

**`cuenta-arrastrada.txt` (la línea base vigente):**

| Filas del trader | N | 0-3 | 4-5 | 6-10 | >10 | 0-15 min | 16-30 | >30 |
|---|---|---|---|---|---|---|---|---|
| PAREJA | 7 | 7 | 0 | 0 | 0 | 7 | 0 | 0 |
| SIN PAREJA, bot más cercano (todas) | 23 | 1 | 2 | 5 | 15 | 12 | 4 | 7 |
| … del mismo lado | 23 | 1 | 2 | 5 | 15 | 12 | 4 | 7 |
| … del otro lado | 0 | | | | | | | |

(Las otras 168 filas del trader dicen «ninguna operacion del bot en la sesion».)

**`diaria.DIAGNOSTICO.cuenta=diaria.txt` (diagnóstico; no cuenta por ADR-0070 punto 3):**

| Filas del trader | N | 0-3 | 4-5 | 6-10 | >10 | 0-15 min | 16-30 | >30 |
|---|---|---|---|---|---|---|---|---|
| PAREJA | 40 | 40 | 0 | 0 | 0 | 40 | 0 | 0 |
| SIN PAREJA, bot más cercano (todas) | 136 | 6 | 13 | 21 | 96 | 46 | 26 | 64 |
| … del mismo lado | 106 | 6 | 12 | 20 | 68 | 44 | 22 | 40 |
| … del otro lado | 30 | 0 | 1 | 1 | 28 | 2 | 4 | 24 |

Cuadra con las cabeceras ya commiteadas: 7 parejas = «cobertura: 7/198» (`cuenta-arrastrada.txt:10`)
y 40 = «cobertura: 40/198» (la diaria, línea 13). Las PAREJA están dentro de 3 puntos y 15 minutos
por construcción. No propongo tolerancias. **Y una advertencia para la PARADA:** esta tabla ya la ha
visto quien va a decidir las tolerancias; cualquier cambio de los 3 puntos y 15 minutos se decidiría
con ella a la vista (es lo que ADR-0070 punto 4 llama «declarar lo visto»).

### 0.f A-16 (sesgo 1): diseño de la medida, sin ejecutarla

**Lo que ya hay** (auditor, H4, que el encargo no recoge): A-16 cita solo el anexo del 2026-09-09
(MT5/FundedNext frente a Dukascopy, 2 puntos de mediana, `A-16-proveedor-de-datos-2026-09-09.md:32`,
«esta medición no la cubre», `:52-53`), pero el repo tiene medidas posteriores de la serie del
trader: `BLOQUE-DE-LA-CAJA.md:192-210` (las leyendas OHLC de 9 velas, 36 valores: OANDA − Dukascopy
mediana +2 puntos, máximo 4, OANDA por encima), `ABRIL-Y-LA-CAJA.md:250, :439` y
`LA-CAJA-DEL-29-DE-ABRIL.md:275` (con 2 y 3 velas), y `VIABILIDAD-TRADER.md:185` (4 casos en que una
serie toca un nivel y la otra se queda a 5-11 puntos). ADR-0043 apoya su tolerancia de 3 puntos en
«las series difieren 1-2 puntos (A-16)» (`0043:80-83`; auditor, H5). La medida nueva no compara
velas con velas: compara la ENTRADA del trader con el mercado de Dukascopy del minuto del llenado,
sobre las 198 operaciones de construcción.

**La medida.** Para cada operación del trader de los días dev de construcción (por la compuerta:
`arnes.dias_de_construccion(repo, criterio, criterio.construccion)`, la misma que usa el arnés, que
cruza cada caso con `casos_ocultos` antes de leerlo, `arnes.py:134-168`; recontado hoy: 76 días y
198 operaciones, `recuento_compuerta.py`):
1. el minuto del llenado: `instante_utc` truncado al minuto;
2. **M1**: la vela de Dukascopy de ese minuto (BID; `data/manifests/README.md:14`), y la distancia
   en puntos de la entrada al rango [low, high], 0 si cae dentro;
3. **ticks**, cuando el minuto los tenga (los ficheros diarios van de las 05:00 a las 14:00 UTC,
   p. ej. `data/manifests/ticks/eurusd-ticks-2026-04-1d189bdd.yaml:9-14`; columnas
   `ts_utc,ask,bid,…`, `data/manifests/README.md:48`): la distancia al tick más cercano del minuto,
   con el lado en que se llenaría la orden (una venta, el BID; una compra, el ASK) y, aparte, con
   los dos lados;
4. estadísticos, en total y por mes: N, mediana, p90 y proporción dentro del rango (distancia 0); y
   cuántas sin ticks en su minuto (las horas perdidas, `anexos/RESPALDO-M1/horas_perdidas.py`).

**Qué hay que leer, y si abre algo.**
- los casos dev de los cuatro meses (instante, dirección y entrada de 198 operaciones): material de
  desarrollo, se lee sin puerta (`CLAUDE.md`; ADR-0021 §1) y se declara el mismo día;
- los manifiestos M1 de los cuatro meses (`data/manifests/eurusd-m1-2026-01-e37291d4.yaml`, `-04-990211bd`,
  `-07-aa162170`, `-08-0d42230e`) y sus CSV, solo el minuto de cada operación; los cuatro de ticks
  (`data/manifests/ticks/`) y el CSV de cada uno de los 76 días;
- **no** se lee el mes anterior (no hay sesgo que calentar): ni marzo ni junio, que tienen días
  reservados;
- `casos_reservados(repo)`: 34 casos, todos en 2026-05 (13), 2026-06 (11) y 2026-09 (10); 0 en los
  cuatro meses de construcción; `casos_ocultos`, el mismo reparto (`recuento_compuerta.py`, hoy).
  Leer velas no es abrir casos (ADR-0021 §1): no abre nada; se declara en
  `HOLDOUT-EXPOSICIONES.md` el día que se corra.

**El guion propuesto:** `docs/validation/anexos/METODO-FIDELIDAD-RENTABILIDAD/medir_a16.py`, con la
raíz por argumento (CLAUDE.md, «Ensayos aislados», regla 2), que solo lee e imprime; la salida,
`medir-a16.txt`, con una fila por operación (día, sesión, lado, distancia M1, distancia al tick) y
los estadísticos. Sin precios del bot: no es una corrida del bot. No se corre hasta la fase 1.

**Lo que la medida no resuelve:** si el `entryPrice` del xlsx es el 0 de la caja o el llenado con su
spread (haría falta leer el libro; auditor, «Lo que no pude comprobar»). La medida mide la distancia,
sea cual sea la causa.

### 0.g Los textos que ADR-0092 tendría que enmendar o anotar

| Texto | Línea | Qué le hace ADR-0092 |
|---|---|---|
| ADR-0043, Decision: Unidad, Emparejamiento, Métricas | `0043:14-26` | NOTA: la fidelidad se mide también por criterios (0.b), con las métricas de la PARADA |
| ADR-0043, «Fuera del criterio» | `0043:27-28` | NOTA: el stop entra si la PARADA lo pone (A-18 y A-31 RESUELTAS); TP y gestión siguen fuera |
| ADR-0043, «Umbral de desarrollo» | `0043:43-44` | NOTA, según el punto 5 de la PARADA |
| ADR-0043, «Cambios» | `0043:47-49` | NOTA: la cláusula se dispara con la primera salida del motor sobre MEDIDA, que no se ha producido (ninguna salida con 2026-05 en su CONJUNTO: `grep -rlE 'CONJUNTO: .*2026-05' docs/` vacío; ningún `--meses` con 2026-05; el arnés lo niega, `arnes.py:110-115`; auditor, 12). Mayo no se toca ni se quema |
| ADR-0043, «Por qué», la tolerancia | `0043:80-83` | NOTA: A-16 medida (0.f) |
| ADR-0070 punto 1 (el umbral) | `0070:44-50` | según el punto 5 de la PARADA |
| ADR-0070 punto 3 (la lista cerrada; NOTAs) | `0070:54-113` | NOTA: declara lo visto (las corridas de RECORRIDA-CONSTRUCCION y de RESPALDO-M1) y, si entra un camino de la cuenta, que es una condición y la lista no cambia |
| ADR-0070 punto 4 (declarar lo visto) | `0070:115-116` | es la cláusula que obliga a declarar; ADR-0092 la cumple |
| ADR-0070 punto 5: la línea «habilita medir…» y los campos del yaml | `0070:117-126`; impresa en `arnes.py:379-380`, calculada en `criterio_fidelidad.py:182-220` | **el encargo la sitúa en el punto 3; es el 5** (auditor, 45). Qué pasa con ella, punto 5 de la PARADA |
| ADR-0070 punto 6 (la medida tiene su rama y su ADR) | `0070:127-129` | la rentabilidad sobre meses no vistos necesita un comando que hoy no existe (auditor, H3) |
| ADR-0053 §6 (la cuenta persiste en todo el tramo) | `0053:179-185` | enmienda, si la PARADA cambia el camino de la cuenta (auditor, H2) |
| MASTER_PLAN, NOTA de cabecera de ADR-0082 | `MASTER_PLAN.md:10-17` | NOTA nueva si la puerta de salida a vivo pasa a ser la rentabilidad |
| MASTER_PLAN §0, el principio | `MASTER_PLAN.md:37` | ya enmendado por la NOTA de ADR-0082; el cuerpo no se toca |
| F26 / F27 / F35 | `MASTER_PLAN.md:119`, `:120`, `:130` | F35 dice «Memorando de decision» y su criterio es «decision humana» (auditor, 8): la puerta de rentabilidad es condición necesaria del memorando, no lo sustituye |
| §H, la fila del pre-registro | `MASTER_PLAN.md:221` | la amplía G, no esta rama |
| Las dos Reglas vivas | `PROJECT_STATE.md:150-151` | la segunda, en el cierre (propuesta en el punto 5); la primera sale de `MASTER_PLAN.md:36` y no de un ADR (auditor, 28): ADR-0092 le da el mecanismo |
| `criterio_fidelidad.yaml` | `:1-7` (la cabecera repite «declare quemado»), `:10-30` | campos nuevos (abajo) |
| `PREREGISTRO.md`, «Que tiene que llevar» | `:15-24` | la amplía G; una NOTA de esta rama tiene que dejar intacta la marca «SIN RELLENAR», o la puerta lo daría por relleno (`holdout.py:76`, `MARCA_SIN_RELLENAR`; auditor, H13) |
| `CLAUDE.md` | — | no nombra el criterio (`grep ADR-0043|ADR-0070|criterio_fidelidad|rentabilidad CLAUDE.md`: 0) |

**Campos nuevos de `criterio_fidelidad.yaml`** (ADR-0002: las cifras solo ahí; `test_no_business_literals`
lo guarda): las tolerancias por pieza del criterio (las que la PARADA ponga), el umbral de cada
pieza si lo hay, y los de la rentabilidad: esperanza mínima en R neta, margen bajo el límite diario
y bajo el total (en porcentaje del capital, como el perfil), N mínimo de operaciones, y el
tratamiento del deslizamiento (un enum, si es «pendiente de F17»). Todos cargados y validados por
`cargar_criterio` (`criterio_fidelidad.py:254-283`), y un yaml sin ellos no carga.

**Las guardias que fijan hoy esos textos:** `tests/unit/test_criterio_fidelidad.py:104` (el fichero
dice lo que dice ADR-0043), `tests/unit/test_umbral_mayo.py:50-307` (las cifras de construcción, la
lista cerrada exacta, la línea de veredicto y sus motivos), `tests/unit/test_diferencias_por_operacion.py`,
`tests/unit/test_kit.py:418` (A-16 ABIERTA en la tabla), `tests/unit/test_hoja_de_ruta.py`,
`tests/unit/test_project_state.py` (secciones y tope de 25.000; el 23.000 es la alerta del
consultor) y `tests/contract/test_no_business_literals.py` (auditor, H14).

**Borrador de ADR-0092** (la fase 1 lo escribe con lo que diga la respuesta; aquí, la forma):

> # 0092 · El bot se juzga por criterios para construir y por rentabilidad para operar en vivo
>
> Enmienda ADR-0043 y ADR-0070 [y ADR-0053 §6, si el punto 6 lo pide]. Decisión de Aleks del
> 2026-10-29 (Next Action R, hoja de ruta R3.7); umbrales del consultor en su respuesta a la PARADA
> de `trabajo/metodo-fidelidad-rentabilidad` (fecha), escritos antes de ninguna corrida nueva.
>
> ## Decision
> 1. **La fidelidad es la herramienta de construcción y se mide de dos formas.** Por operación
>    entera (ADR-0043, sin cambios) y por criterios, pieza a pieza: [las piezas del punto 0], cada
>    una con su tolerancia [UMBRAL: lo fija el consultor en la PARADA], contra [las órdenes / las
>    operaciones del bot, punto 1]. Una pieza que el material no trae (la liquidez de M15) se dice
>    no comparable y no puntúa.
> 2. **La rentabilidad es la puerta para operar en vivo.** Se mide UNA sola vez, con la spec sellada
>    (un hash de `strategy_spec.yaml` y `parametros.yaml` en el pre-registro), sobre [los meses no
>    vistos del punto 4], con el perfil de la cuenta real y su primera fase, y pasa si: esperanza en
>    R neta por operación (después de comisión, swaps y deslizamiento) ≥ [UMBRAL]; drawdown diario
>    máximo, en la equity que vigila la firma, ≤ 5 % del capital menos [UMBRAL]; drawdown total
>    máximo ≤ 10 % menos [UMBRAL]; y al menos [UMBRAL] operaciones. Ninguna suspensión de la firma.
> 3. **El deslizamiento** [punto 3: pendiente de F17 con la regla de cómo entra / la forma sin
>    cifra].
> 4. **Contra optimizar sobre resultados.** Ningún parámetro de la spec se elige ni se ajusta por la
>    cifra de rentabilidad: se mide una vez, sobre meses que el bot no ha visto, con la spec
>    sellada; si no pasa, se vuelve a construir y la cifra vista no vuelve a medir (los meses
>    pasan a construcción y quedan escritos, como mayo en ADR-0043). Las condiciones previas de F26
>    que tocan a cualquier métrica sobre reservados (F26 lee la diferencia 3,00/3,75 como conocida y
>    la mide en A-56; los dos días del universo de la sesión 1 sin partición) son condiciones de esa
>    medida.
> 5. **El camino de la cuenta** [punto 6].
> 6. **Lo visto, declarado** (ADR-0070 punto 4): las corridas de construcción ya vistas son las de
>    `anexos/CORRIDA-CONSTRUCCION/`, `anexos/RECORRIDA-CONSTRUCCION/` y `anexos/RESPALDO-M1/` (la
>    línea base vigente), y las tablas de 0.c y 0.e de METODO-FIDELIDAD-RENTABILIDAD.md, que se
>    vieron antes de fijar los umbrales. Mayo no se ha visto: ninguna salida del motor sobre la
>    medida; este ADR enmienda el criterio sin quemarlo.
> 7. **Dónde viven las cifras:** `knowledge/cases/criterio_fidelidad.yaml` (ADR-0002); las
>    funciones, puras, en `cases/criterio_fidelidad.py`; el arnés solo las escribe.
> 8. **Qué tiene que llevar PREREGISTRO.md para la rentabilidad** (lo amplía G): la métrica y su
>    cálculo, los umbrales, los meses y por qué esos, el hash de la spec sellada, el tratamiento del
>    deslizamiento y qué se hace si no pasa.

### 0.h Las líneas del cierre (preparadas sobre una copia; no aplicadas en la rama)

Simuladas con `simular_cierre.py` (en memoria, la forma de `anexos/SELLO-RESPALDO-M1/simular_cierre.py`;
ADR-0092 se añade al conjunto de ids existentes porque lo crea la fase 1). Las frases que dependen de
la respuesta llevan [PARADA].
- **PROJECT_STATE**: sale **R** (`PROJECT_STATE.md:52`) con su registro «# Next Action HECHA · R ·
  el método de juicio del bot · sale de PROJECT_STATE.md en trabajo/metodo-fidelidad-rentabilidad
  (fecha)» en HISTORIA; la letra ya tenía uno, del 2026-10-05 (`HISTORIA.md:4689`), y el nuevo
  lleva su fecha (`DECISIONES-DE-PROCESO.md:29`). **F**: «Siguiente: R y después la re-corrida que
  cuenta (ADR-0070 §3), la primera con la comisión medida (ADR-0090 §3) y con el sello del respaldo
  de ADR-0091;» pasa a «Siguiente: la re-corrida que cuenta (ADR-0070 §3), la primera con la comisión
  medida (ADR-0090 §3), el sello del respaldo de ADR-0091 y el método de ADR-0092;» (lo demás de F,
  incluida la preparación de la sesión 7, queda). **G**: «…ADR-0073) y A-16.» pasa a «…ADR-0073);
  A-16, medida en R3.7. Y la ampliación de PREREGISTRO §«Que tiene que llevar» y de la fila de
  MASTER_PLAN §H con el criterio de rentabilidad de ADR-0092.». **Technical Debt**: la que nazca en
  la fase 1. La segunda Regla viva, como diga el punto 5.
- **Hoja de ruta**: R3.7 cambia `NA:R` por `ID:ADR-0092` en sus Refs y gana «Estado: HECHA
  (`trabajo/metodo-fidelidad-rentabilidad`; METODO-FIDELIDAD-RENTABILIDAD.md): ADR-0092 [PARADA];
  A-16 medida.»; R5.1 dice «A-16 (Oanda frente a Dukascopy), medida en R3.7
  (METODO-FIDELIDAD-RENTABILIDAD.md); el criterio de rentabilidad de ADR-0092 en PREREGISTRO»;
  R5.2 deja de nombrar `NA:R` («El sello del respaldo M1 (R3.6) y el método (R3.7, ADR-0092) están
  HECHOS.»). Las dos corridas de R3.6 siguen en la re-corrida que cuenta (R3.7, «Qué es»).
- **Salida de la simulación:** `R viva en la copia? False; R HECHA en HISTORIA? True; NA:R en la
  hoja simulada? False`; `a: []`, `b: []`, `c: []`; PROJECT_STATE con las líneas del cierre
  **22.140 bytes**, y con el Current Feature del cierre **22.187**; los cuatro tests de
  `test_project_state` pasan. Por debajo de 23.000.

### 0.i El encargo frente al repo (auditor)

El subagente `auditor-encargo` (2026-11-07): 46 afirmaciones, 30 correctas, 1 incorrecta, 15 con
matiz; 17 herencias no recogidas. Solo leyó; dos órdenes suyas las negó la guardia (un `..` y un
`for $(...)`) y las relanzó con una ruta más estrecha, sin rodear nada. Lo que cambia algo:

| # | Afirmación del encargo | Veredicto | Lo que dice el repo |
|---|---|---|---|
| 45 | la línea «habilita medir…» es de ADR-0070 §3 | **INCORRECTA** | es el punto 5 (`0070:117-126`); gana el repo y así se usa en 0.g |
| 8 | F35, «puerta de salida a vivo» | MATIZ | `MASTER_PLAN.md:130`: «Memorando de decision», criterio «decision humana»; «go-live-gate» es solo el nombre de la rama. La puerta automática choca con la decisión humana: punto 5 |
| 14, 16 | la línea base vigente; la lección 2 de F38q | MATIZ | la línea base es de un motor anterior a F38o, a la comisión de 2,50 y al sello; lo que decide no sale de ella (aviso al principio de esta fase) |
| 21 | A-16 no cubre la fuente del trader | MATIZ | hay medidas posteriores de la serie del trader que A-16 no cita (0.f) |
| 22, 33 | si A-16 se cierra, los cinco sitios | MATIZ | los cinco sitios (`AMBIGUEDADES.md:26-35`) incluyen el feedback, la regla que cita A-16 (`strategy_spec.yaml:1138`) y `scripts/hoja_preguntas.py`; A-16 dice «no la puede cerrar ninguna decision» (`ambiguedades.yaml:293`); el contrato protege `knowledge/spec/`; y tocar `knowledge/spec/` convierte esta rama en «la próxima que toque knowledge/spec», que paga los cuatro textos del panel de FTMO, uno de ellos en `parametros.yaml`, que el encargo protege: punto 8 |
| 32 | el docstring de `viabilidad_comision.py:46` | MATIZ | es un comentario de código, no un docstring; esta rama no corre el guion y no lo toca |
| 34 | las dos condiciones previas de F26 | CORRECTA, incompleta | G nombra además «una pregunta abre N particiones» (`PROJECT_STATE.md:129`) y los días retirados de holdout-3 y fidelidad-1 (H12) |
| 35 | las corridas de R3.6, después de esta rama | MATIZ | R3.6 dice «pasan a R3.7 y a la re-corrida»; R3.7 y HISTORIA las ponen después de R3.7: coherente con el encargo |
| 37 | el desenlace solo sale cruzando secciones | CORRECTA, con MATIZ | el motor ya lo clasifica (`clasificar_cierre`) y no lo escribe; su break even es un mecanismo, no un PnL cero (0.d) |
| 40, 41 | las piezas del caso y la caja derivada | MATIZ | el arnés descarta el stop; la derivación de la caja es la que A-56 discute; el inicio del punto no se deriva (0.b) |
| 46 | `wc -c` por debajo de 23.000 | MATIZ | la guardia está en 25.000; 23.000 es la alerta del consultor |

Herencias que el encargo no recoge, y dónde entran: H1 (el bloque `ids-inexistentes` del informe:
**arreglado** en el commit de apertura); H2 (ADR-0053 §6, en 0.c y en el punto 6); H3 (no hay
comando de medida de rentabilidad, punto 4); H4 y H5 (medidas previas de A-16 y la tolerancia de
ADR-0043, en 0.f y el punto 7); H6 (A-18 y A-31 RESUELTAS: el stop puede entrar, 0.b y punto 0);
H7 (A-56 frente a la caja, 0.b); H8 (la deuda del `no_trade` y S-14, 0.d); H9 (los meses candidatos
a «no vistos»: febrero, que «no se toca y no se descarga», HER:6, `PROJECT_STATE.md:59`; diciembre
sin vídeo, NA:I; marzo, R5.3; y pedir al trader un mes no tocado, `PREREGISTRO.md:32-33`: punto 4);
H10 (el N del Deflated Sharpe de F27 es de EJECUCIONES de backtest, no el «N mínimo de operaciones»
de la PARADA; los dos modelos de llenado de F27, `MASTER_PLAN.md:227-228`; holdout-2 es la «cifra
final de fidelidad», `:220`: punto 4); H11 (el deslizamiento pendiente de F17 es HER:10; la comisión,
HER:27: punto 3); H12 (lo que queda de G); H13 (la marca «SIN RELLENAR» de PREREGISTRO: 0.g y punto
12); H14 (los tests que fijan la línea de veredicto: 0.g); H15 (el «más cercano» sin el lado: 0.e,
partido por lado); H16 (Q y M en el sesgo 3: 0.d); H17 (R4.2 no lleva «HECHA» pero su Estado dice
activada en spec y motor: la dependencia de R3.7 se cumple). En SELLO-RESPALDO-M1.md,
RESPALDO-M1.md, ACTIVAR-SESION-06*.md y las últimas 300 líneas de HISTORIA.md el auditor no
encontró nada más, y mi `grep` de «R3.7|NA:R|a R|para R|rentabilidad» en los tres primeros da lo
mismo (R3.7, su dependencia de R4.2, las corridas de R3.6, la entrada R y el §4.5).

Contrastadas por mí, además: la regla de las dos corridas de R3.6 (`HOJA-DE-RUTA.md:222-224`,
`:246-247`); los docstrings de Technical Debt (`PROJECT_STATE.md:88`): esta rama no corre esos
guiones; la deuda del panel de FTMO (`:141`): no se paga aquí salvo lo que diga el punto 8.

### 0.j Exposiciones

Fila del 2026-11-07 en `HOLDOUT-EXPOSICIONES.md`, en el commit de esta fase. Leído: las salidas ya
commiteadas `anexos/RESPALDO-M1/cuenta-arrastrada.txt` y `diaria.DIAGNOSTICO.cuenta=diaria.txt`
(días dev: filas por operación con instantes y entradas, la curva, los eventos y las órdenes), por
Read, Grep y `recuentos_vistos.py`; `CORRIDA-CONSTRUCCION.md` §4.5 (días dev); las fechas de los 76
días dev por `arnes.dias_de_construccion` y sus operaciones EN MEMORIA, sin imprimirlas
(`recuento_compuerta.py`, solo recuentos por mes; `huecos_material.py`, solo fechas de días dev);
`casos_reservados` y `casos_ocultos`, solo recuentos por mes; los manifiestos M1 de los cuatro meses
de construcción (fechas sin datos) y la cabecera del de ticks de abril; **dos líneas del CSV de
ticks del 2026-04-01** (día dev de construcción), para ver sus columnas; y los dos `make check` de
la apertura (el M1 de marzo de siempre, `test_visor.py` y `test_preparar_a35.py`). El auditor:
documentos, ADR, código y tests; de las salidas commiteadas, tipos de línea y formatos. Ningún
libro, imagen, fotograma, transcripción, nada de un mes reservado. La propuesta para la fase 1, en
el punto 13.

### 0.k Lo que no pude medir

- Si RN-032 seguiría congelando la cuenta con el motor de hoy: lo diría una corrida, prohibida. No
  hace falta para ninguna decisión (0.c).
- Si la entrada del caso es el 0 de la caja o el llenado con su spread: haría falta leer el libro.
- El desenlace y el PnL de cada operación del bot de la línea base: el encargo no los pide y serían
  cifras nuevas del bot; además, los `manual` no se pueden clasificar desde la salida (0.d).
- Que ningún informe `.md` haya corrido el motor sobre mayo por otra vía: comprobado sobre las
  salidas `.txt`, el código del arnés y `grep` de los comandos (0.g), no leyendo cada informe.

## Lo que necesito que decidas

0. **Las piezas de la fidelidad por criterios.** Opciones: (a) las comparables hoy pieza a pieza o
   de forma derivada (0.b): sesión y dirección; sesgo (dirección contra rn003); entrada (el 0);
   instante; stop (el 0,8, que el arnés hoy descarta: haría falta que el criterio lo lleve); la caja
   (el 1, derivada y sujeta a A-56); el nivel del punto. La liquidez de M15 se declara no comparable
   con el material de los casos. (b) Solo las que el caso trae literalmente (sesión, dirección,
   entrada, instante, stop), sin derivadas. (c) (a) más la liquidez de M15 leída a mano del vídeo en
   los libros grabados. Recomiendo (a): cubre las cuatro piezas de la decisión de Aleks que el
   material permite y dice cuál no. Coste de (b): pierde la caja y el punto, que son lo que P2 y P3
   separan. Coste de (c): una lectura humana de vídeo en un criterio que se calcula, y solo julio y
   el 29 de abril. Cada pieza con su tolerancia: [UMBRAL: lo fija el consultor en la PARADA].
1. **Contra qué del bot se compara cada pieza, y la unidad.** Opciones: (a) contra las ÓRDENES que el
   bot colocó en la misma (día, sesión, dirección), llenadas o no («### Ordenes» trae precio, punto,
   caja 1 y distancia al stop): para cada operación del trader, la orden más cercana en instante, y
   el recuento en cascada sesión-dirección → caja → punto → entrada, como el embudo; (b) contra las
   operaciones LLENADAS, como el criterio por operación; (c) cada pieza por separado, sin cascada.
   Recomiendo (a): la caja y el punto existen aunque la orden no se llene, y la cascada dice dónde
   se separa el bot. Coste de (b): un bot congelado por RN-032 (0.c) no tiene ninguna pieza que
   comparar. Coste de (c): no dice qué pieza falla primero.
2. **El criterio de rentabilidad.** Opciones para la unidad: (a) R neto por operación = PnL neto en
   USD (con comisión y swaps, y el deslizamiento del punto 3) entre el riesgo en USD al colocar
   (lote × distancia al stop); esperanza = media de R neto; drawdown diario = (saldo al corte −
   equity mínima) / capital, y total = capital − la menor equity, los dos en la magnitud que vigila
   la firma (0.a); (b) lo mismo en USD, sin R. Recomiendo (a): el R es la unidad del trader (1:3) y
   no depende del saldo. Coste de (b): la cifra cambia con el capital y el lote. Los umbrales:
   esperanza mínima en R neta, margen bajo el 5 % diario, margen bajo el 10 % total y N mínimo de
   operaciones: [UMBRAL: lo fija el consultor en la PARADA]. Y si una suspensión de la firma, o un
   SUPERADA del reto, cuenta aparte.
3. **El deslizamiento sin modelo** (`deslizamiento_fijo_puntos` 0, `llenado.yaml:9-12`; ADR-0090 §7,
   ADR-0051 §4). Opciones: (a) pre-registrado como pendiente de F17 (HER:10), con la regla escrita de
   cómo entra: cuando F17 lo mida, la esperanza se recalcula restando a cada llenado y a cada cierre
   por stop [la medida de F17 que fije el consultor: su mediana, su p90…], y la puerta no puede dar
   «sí» antes; (b) una forma sin cifra: el informe da, además de la esperanza con deslizamiento 0, el
   deslizamiento por llenado (en puntos) que la lleva al umbral (el punto de equilibrio), y la puerta
   exige que ese punto de equilibrio supere [UMBRAL]. Recomiendo (a), con el punto de equilibrio de
   (b) informado sin decidir nada: ADR-0002 y ADR-0051 §4 prohíben inventar la cifra, y (b) solo
   traslada la cifra inventada al umbral del punto de equilibrio. Coste de (a): la puerta espera a
   F17 (la demo de FTMO con el grabador de spread y ticks).
4. **Sobre qué meses no vistos, una sola vez.** Opciones: (a) meses SIN material del trader que el
   bot no ha corrido (febrero de 2026, hoy «no se toca y no se descarga», HER:6, y meses de 2025):
   la rentabilidad no necesita etiquetas, así que no abre ningún holdout; (b) los reservados, por la
   puerta de ADR-0033, en la misma apertura que F26 (medir una cifra del bot sobre un día reservado
   ES abrirlo, ADR-0021); (c) mayo, el conjunto de medida. Recomiendo (a): es lo único que el bot
   no ha visto y que no gasta material del trader; y como la rentabilidad no compara con él, no
   necesita que el trader lo haya operado. Coste de (a): bajar las velas y los ticks, renovar el
   calendario de cierres hacia atrás (N, condición 1) y levantar HER:6, que es decisión tuya; y
   sigue faltando el comando de medida, que el arnés hoy no tiene (niega todo lo que no sea
   construcción, ADR-0048 §7; auditor, H3): rama propia con su ADR, como la de mayo (ADR-0070 punto
   6). Coste de (b): gasta una partición y ata la rentabilidad a las condiciones previas de F26.
   Coste de (c): mayo se quema para fidelidad.
5. **El papel de la fidelidad tras el cambio, la línea «habilita medir…» y la segunda Regla viva.**
   Opciones: (a) la fidelidad (por operación y por criterios) se queda como herramienta de
   construcción y como diagnóstico de F26; ADR-0070 sigue gobernando cuándo se mide MAYO y la línea
   de veredicto no cambia; la rentabilidad del punto 2 es la condición necesaria para operar en vivo,
   y F35 sigue siendo un memorando y una decisión humana; (b) la fidelidad por criterios pasa a ser
   también el umbral para medir mayo (cambia ADR-0070 punto 1 y la línea); (c) mayo deja de
   medirse por fidelidad y ADR-0070 queda sin objeto. Recomiendo (a): es lo que dijo Aleks («la
   fidelidad sigue siendo la herramienta de construcción»), no cambia ningún umbral pre-registrado
   y no toca la línea ni sus once tests. Coste de (b): un umbral nuevo de construcción fijado con
   las corridas de construcción ya vistas. Coste de (c): mayo pierde su papel sin que nadie lo haya
   decidido. **Propuesta para la segunda Regla viva** (`PROJECT_STATE.md:151`), en el cierre: «La
   rentabilidad pre-registrada de ADR-0092, medida una vez sobre meses que el bot no ha visto,
   precede a todo lo que decida operaciones en vivo (F29, F30 y lo de F31-F32 que dependa de
   ellos), y la fidelidad sigue siendo la herramienta de construcción; la capa de plataforma de
   ADR-0082, que nunca decide una operación, puede ir antes.» Y la primera Regla viva («Parametros
   no se optimizan contra resultados») gana su mecanismo en ADR-0092 punto 4.
6. **El camino de la cuenta.** Opciones: (a) la cuenta se reinicia donde el material tiene un hueco
   de días de mercado (una condición, 0.c); (b) una cuenta por mes; (c) como hoy, arrastrada en todo
   el tramo. Las dos primeras dan hoy las mismas 4 cuentas. Recomiendo (b) para la construcción:
   misma partición hoy, y en un mes de medida no reinicia en cada día reservado; y que en los meses
   no vistos (punto 4), que son seguidos, la cuenta se arrastre como operará. Coste de (a): en un mes
   con días reservados intercalados, una cuenta por tramo de días seguidos. Coste de (c): 165 de las
   198 operaciones del trader caen en días con la cuenta ya congelada en la línea base (0.c), y la
   precisión solo mide enero. Cualquiera de (a) y (b) cambia lo que el motor decide y enmienda
   ADR-0053 §6: ADR-0092 la fija, y la implementa la rama de motor que vaya antes de la re-corrida
   que cuenta (o la propia re-corrida), no esta, porque el encargo dice que ninguna decisión del
   motor cambia aquí. No entra en `OPCIONES_QUE_NO_CAMBIAN_LA_CORRIDA`: es una condición, no una
   opción.
7. **Las tolerancias del criterio por operación (3 puntos, 15 min).** Opciones: (a) quedan como
   están, y A-16 se informa como un sesgo declarado de la cifra; (b) se atan a la medida de A-16 por
   una regla escrita ANTES de medirla (p. ej. «la tolerancia de entrada es la mayor de 3 y [el
   estadístico de A-16 que fije el consultor]»). Recomiendo (a): las tolerancias están
   pre-registradas (ADR-0043, ADR-0070) y la tabla de 0.e ya está vista; (b) es limpia respecto a
   A-16 pero no respecto a esa tabla. Coste de (a): si A-16 sale por encima de 3 puntos, la
   cobertura tiene un techo que no es del bot, y hay que decirlo en cada cifra.
8. **A-16, después de medirla.** Opciones: (a) se mide en la fase 1 (punto 3 del encargo) y queda
   ABIERTA con `resuelve_en: [F26]`, sin tocar `knowledge/spec/`; su cierre va a la rama de G/F26;
   (b) se cierra aquí como RESUELTA con la medida como fuente documental, por los cinco sitios de
   `AMBIGUEDADES.md` (feedback, la regla que la cita en `strategy_spec.yaml:1138`,
   `scripts/hoja_preguntas.py` y su test, `test_kit.py:418`, la tabla y `spec docs --escribir`);
   (c) se cambia solo su `resuelve_en`. Recomiendo (a): (b) y (c) tocan `knowledge/spec/`, que el
   contrato protege, y convierten esta rama en «la próxima que toque knowledge/spec», que tendría
   que pagar los cuatro textos del panel de FTMO, uno en `parametros.yaml`, que el encargo protege.
   Coste de (a): A-16 sigue en la tabla de Known Ambiguities con la medida hecha.
9. **El diseño de la medida de A-16** (0.f). Opciones: (a) M1 BID para los dos lados, más el tick del
   lado de llenado (BID en la venta, ASK en la compra) y, aparte, el de los dos lados; (b) solo M1
   BID. Recomiendo (a): con ticks se ve si la entrada del trader existió en Dukascopy por el lado
   en que se llenaría; la M1 es solo BID. Coste de (b): una compra queda medida contra el BID, con
   el spread dentro.
10. **Lo que la fase 1 puede tocar en `engine/`.** Opciones: (a) solo salida, en `arnes.py` y
    `cableado.py`: la línea de las métricas por criterios y de rentabilidad, y en «### Ordenes» o
    en una tabla nueva por posición las columnas desenlace (de `clasificar_cierre`), PnL neto en USD
    (con comisión y swaps), riesgo en USD al colocar y R neto; más, para el stop del trader, que el
    criterio lo lleve (`arnes._operacion`); con un test que fije que la salida de decisiones no
    cambia byte a byte salvo las líneas nuevas; (b) nada en `engine/`: un guion que cruce secciones.
    Recomiendo (a): sin el PnL por operación no hay esperanza en R (0.a), y el desenlace de los
    `manual` no sale (0.d). Coste de (b): la esperanza no se puede calcular y la métrica del sesgo 3
    queda incompleta. Con (a), el contrato se amplía a `src/botsito/engine/arnes.py` y `cableado.py`
    en un commit, y el riesgo de la rama sigue medio.
11. **El sesgo 3 en la cifra.** Opciones: (a) la re-corrida da, además de la cifra entera, la misma
    sin las operaciones del bot que acabaron en break even en los libros sin vídeo (enero, agosto,
    abril salvo el 29), y la clase de julio sigue provisional hasta T; (b) solo la cifra entera, con
    el sesgo declarado. Recomiendo (a): es lo que S-14 permite medir y no cambia el criterio. Coste
    de (b): la precisión se lee contra un trader que se saltó sesiones.
12. **Las NOTAS de MASTER_PLAN y PREREGISTRO.** Opciones: (a) una NOTA en la cabecera de
    MASTER_PLAN (como la de ADR-0082) que diga que la puerta de salida a vivo es la rentabilidad de
    ADR-0092 y que F35 sigue siendo la decisión humana; en PREREGISTRO, una NOTA que nombre ADR-0092
    y deje intacta la marca «SIN RELLENAR»; (b) ninguna: G lo hace todo. Recomiendo (a): el plan no
    quedaría diciendo otra cosa que el ADR, y G sigue haciendo la ampliación de los dos ficheros.
    Coste de (b): hasta G, MASTER_PLAN y PREREGISTRO no nombran la puerta.
13. **Exposiciones de la fase 1**, una fila antes de correr nada: (1) cada `make check`, con el M1 de
    marzo de siempre; (2) los clones de `comparar-con-main`, con tests sintéticos (y los de `main`
    que lean `data/` de construcción, como en las ramas anteriores); (3) `medir_a16.py`: los casos
    dev de los cuatro meses (instante, dirección, entrada) y sus M1 y ticks del minuto de cada
    operación, sin el mes anterior; (4) los guiones de recuento sobre las salidas ya vistas.
    Opciones: (a) así; (b) con lo que añadas. Recomiendo (a).

Espero tu respuesta a la PARADA.

## Respuesta del consultor a la PARADA (2026-11-07)

Copiada tal cual:

> Modelo: Opus 5.5 · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA de trabajo/metodo-fidelidad-rentabilidad (2026-11-07). Cópiala tal cual al informe con la skill fase-cero, bajo «Respuesta del consultor», antes de empezar la fase 1. Los umbrales de aquí se escriben antes de ninguna corrida nueva; lo que ya vi lo declaro en L. Cuando digo «punto n» hablo de esta respuesta; la numeración interna de ADR-0092 la fijas tú al escribirlo y la citas como «ADR-0092 §n».
>
> L. Lo visto por el consultor antes de decidir (va a la sección «Lo visto, declarado» de ADR-0092, por ADR-0070 punto 4): el informe de la fase 0 entero, con las tablas de 0.c (165 de 198 operaciones del trader en días con la cuenta congelada, sobre cuenta-arrastrada.txt) y de 0.e (las distribuciones de Δ de las dos salidas de anexos/RESPALDO-M1/); de la línea base vigente, su curva de equity, su saldo y equity finales y el bloqueo de RN-032 por el límite total desde el 2026-01-20 (ADR-0070 punto 3, NOTA del 2026-10-29) con su ritmo de llenadas; y la esperanza del TRADER en R, con comisión y remuestreo, de VIABILIDAD-TRADER.md §2 y VIABILIDAD-COMISION.md. No existe ninguna esperanza en R del BOT ni ninguna cifra suya sobre mes alguno fuera de construcción. Lo que de abajo se apoya en algo de eso, lo dice: el camino de la cuenta (punto 6) sale de un hecho del código, no de la cifra, pero la cifra se vio; el criterio e) y la forma del remuestreo se parecen a lo que VIABILIDAD-TRADER hace con el trader, y por eso el umbral de esperanza del bot es más alto que el borde estrecho que ahí se mide; las tolerancias no cambian.
>
> 0. Piezas de la fidelidad por criterios: (a) recortada. Entran sesión y dirección, la entrada (el 0), el stop (el 0,8) y el instante, pieza a pieza; y el sesgo de H4, derivado (rn003 de la sesión frente a la dirección del trader), que se informa aparte porque no necesita una orden del bot. NO entran como piezas propias la caja (el 1) ni el punto: la caja del trader se deriva solo de su entrada y su stop con la misma regla del 0,8 que usa el bot, así que con la entrada y el stop comparados no añade información y sí arrastra la duda de A-56; y el nivel del punto es el 0, ya comparado, y su vela no se deriva. La liquidez de M15 se declara no comparable con el material de los casos y no puntúa. Tolerancias: entrada 3 puntos e instante 15 minutos (las de ADR-0043, sin cambio); stop 3 puntos (campo nuevo tolerancia_stop_puntos, entero como tolerancia_entrada_puntos, mismo valor y misma razón: los dos son un nivel leído en otra serie, A-16). La fidelidad por criterios es herramienta de construcción y diagnóstico: NO lleva umbral de paso.
> Porqué: mide dónde se separa el bot sin piezas redundantes ni derivadas discutidas.
>
> 1. Contra qué y en qué orden: (a), contra las órdenes que el bot colocó, llenadas o no, en cascada. Para cada operación del trader: (1) ¿hay alguna orden del bot en el mismo (día, sesión, dirección)?; de las que haya se toma la más cercana en ENTRADA y, a igualdad, la de colocación más cercana en instante; (2) entrada a ≤ 3 puntos; (3) stop a ≤ 3 puntos; (4) la orden se llenó y su llenado está a ≤ 15 minutos del llenado del trader (si no se llenó, cae en «en el nivel, no llenada»). Cada operación del trader se informa por el último escalón que alcanza. Aparte, en recuento: las órdenes del bot en un (día, sesión, dirección) sin ninguna operación del trader. Las cifras de la cascada se dan por mes y en total, diciendo qué cuentan y sobre qué salida (lección 2 de F38q).
> Porqué: la caja se identifica por el nivel, y una orden congelada o no llenada también dice si el bot vio la misma zona.
>
> 2. Criterio de rentabilidad (la puerta para operar en vivo). Unidad: (a), R neto por operación = PnL neto en USD (comisión del perfil, 2,50 por lote y lado según ADR-0090 §3, y swaps) entre el riesgo en USD al colocar, tal como lo calcula la cuenta al dimensionar (lote, distancia al stop y el valor del punto del contrato; no una fórmula nueva). Se mide sobre las operaciones llenadas del bot, en la fase FONDEADA del perfil (punto 4), con el deslizamiento del punto 3 y sobre los meses del punto 4. PASA solo si se cumplen todas:
>   a) N ≥ 100 operaciones llenadas;
>   b) esperanza (media del R neto) ≥ +0,10 R;
>   c) el percentil 5 de la media del R neto por remuestreo POR DÍAS de mercado (10.000 réplicas, semilla fija 20261107) es > 0;
>   d) en ningún día la pérdida diaria, en la magnitud y con la base que vigila la firma (firma_magnitud_vigilada, firma_base_perdida_diaria), llega al 3 % del capital inicial (el límite es el 5 %: 2 puntos de margen);
>   e) la menor equity del tramo no baja del 94 % del capital inicial (el límite es el 10 %: 4 puntos de margen);
>   f) la cuenta no entra en SUSPENDIDA en ningún momento.
> Los bloqueos de RN-032 no son criterio: si la cuenta llegó a donde RN-032 bloquea, ya incumplió d) o e). Si no se cumple a), el resultado es «insuficiente» y se aplica la extensión del punto 4; cualquier otro incumplimiento es «no pasa».
> Porqué: una sola trayectoria de unos meses es un camino entre muchos; los márgenes cubren la varianza de vivo, y c) exige que el borde no sea ruido de unos pocos días.
>
> 3. Deslizamiento sin modelo: (a), pendiente de F17 (heredado 10; ADR-0090 §7 dice que lo mide F17), con el punto de equilibrio de (b) informado sin decidir nada con él. Regla escrita ahora: la medida se corre una vez con deslizamiento_fijo_puntos en 0 (llenado.yaml, sin tocar). Cuando F17 mida el deslizamiento de las órdenes stop, se recalcula SIN volver a correr el bot: a cada llenado de orden stop y a cada cierre por stop o a mercado se le resta la MEDIANA medida (los cierres por objetivo no se tocan), y con el PnL recalculado se vuelven a evaluar b), c), d) y e) (d y e sobre la curva recompuesta operación a operación, sumando el ajuste al día de cada cierre; los lotes y los bloqueos de RN-032 no se recalculan, y el informe lo dice); además la esperanza recalculada con el PERCENTIL 90 de F17 tiene que ser > 0. La puerta no puede dar «pasa» antes de F17. El informe de la medida da también el deslizamiento por llenado, en puntos, que llevaría la esperanza a +0,10 R.
> Porqué: ADR-0002 y ADR-0051 §4 prohíben la cifra inventada; con esta regla el número que falta solo puede venir de la medida.
>
> 4. Meses no vistos, una sola vez: (a) en su forma limpia, sin febrero de 2026. Los meses son JUNIO A NOVIEMBRE DE 2025, seguidos, con la cuenta arrastrada en todo el tramo (como operará) y en la fase FONDEADA del perfil (firma_fases la tiene; el simulador corre una fase por ejecución y no se encadenan fases: pasar el reto y la verificación es otra pregunta, con su objetivo y sus días mínimos, que se informa aparte si alguna vez se mide, y no es la puerta). Porqué esos meses: no hay material del trader de 2025 salvo diciembre (NA:I; "2025-12" en meses_reservados.yaml), que queda fuera; no hay velas ni ticks de 2025 bajados (data/manifests/ solo tiene 2026); el bloque cubre verano, los dos cambios de hora de 2025 (Europa el 26 de octubre, que mueve el día de riesgo; EE. UU. el 2 de noviembre, que mueve la rejilla H4 anclada a las 17:00 de Nueva York) e invierno, que es como empezará el vivo; y no gasta febrero de 2026, el único mes ciego limpio confirmado por el trader (heredado 6, sin levantar; año en meses_reservados.yaml), ni ninguna partición del holdout. Extensión, fijada ahora: si al acabar noviembre de 2025 N < 100, se añaden con la misma spec mayo, abril, marzo, febrero y enero de 2025, en ese orden y de uno en uno, hasta N ≥ 100; si con enero sigue N < 100, «insuficiente» y no pasa. La decisión de añadir mira solo N, nunca el resultado. Dónde viven esos meses: en el bloque de rentabilidad de criterio_fidelidad.yaml (campos meses y extension) y en ADR-0092, y el arnés los niega como hoy niega todo lo que no es construcción (ADR-0048 §7). NO entran en meses_reservados.yaml: ese fichero es para material del trader, tapa por número de mes en cualquier año (holdout.py) y taparía julio y agosto de construcción contra ADR-0078 y ADR-0079; tampoco en las listas construccion ni medida. Condiciones antes de correr la medida, que fija su propia rama con su ADR (ADR-0070 punto 6; el comando no existe): la spec sellada (hash de strategy_spec.yaml, parametros.yaml, el perfil de knowledge/cuentas/ y knowledge/simulador/llenado.yaml, y el sha de src/, en PREREGISTRO.md, que rellena G); el calendario de cierres renovado hacia atrás hasta enero de 2025 (RENOVAR-CIERRES.md, condición 1, leída como la lee NA:I; hoy empieza el 2025-12-04); las velas M1 y los ticks de Dukascopy de esos meses con su manifiesto, bajados siguiendo los heredados 7 y 9 (verifícalos) y declarados; la deuda del spread supuesto para minutos sin ticks, que se busca por la hora de pared de Madrid (Technical Debt), nombrada como riesgo de noviembre y de la extensión de invierno; y la construcción en el umbral de ADR-0070 (la línea «habilita medir», el pre-registrado que ya existe). Una sola ejecución: si se repite por un fallo técnico, se declara con su causa y la spec no cambia entre las dos. Si no pasa, esos meses quedan escritos en el yaml como vistos_rentabilidad y no vuelven a medir nunca (no son construcción: no tienen casos del trader); la siguiente medida usa otros meses, que fijará su ADR.
> Porqué: la rentabilidad no necesita etiquetas del trader, así que no gasta su material; y fijar hoy los meses, la fase y la extensión deja fuera la tentación de elegirlos después.
>
> 5. Papel de la fidelidad: (a). La fidelidad, por operación y por criterios, es la herramienta de construcción; ADR-0070 sigue gobernando cuándo se mide mayo y su línea «habilita medir…» (punto 5 de ADR-0070, no el 3: gana el repo) y sus tests no cambian. Lo que ADR-0092 SÍ enmienda de ADR-0070 es una condición de la corrida que cuenta: el camino de la cuenta (punto 6), y lo declara con lo visto (L). La rentabilidad del punto 2 es condición NECESARIA para todo lo que decida operaciones en vivo; F26 (el holdout de fidelidad) deja de ser esa condición y queda como diagnóstico que se informa en el memorando; F27 (sensibilidad y ventaja, DSR, N de pruebas) no se sustituye: sigue en el plan y F35 sigue dependiendo de ella; F35 sigue siendo el memorando y la decisión humana de Aleks. La segunda Regla viva queda, en el cierre, con tu redacción: «La rentabilidad pre-registrada de ADR-0092, medida una vez sobre meses que el bot no ha visto, precede a todo lo que decida operaciones en vivo (F29, F30 y lo de F31-F32 que dependa de ellos), y la fidelidad sigue siendo la herramienta de construcción; la capa de plataforma de ADR-0082, que nunca decide una operación, puede ir antes.» El mecanismo de la primera Regla viva va en ADR-0092 como lo tienes en el borrador (tu punto 4), más una frase: las métricas de rentabilidad que el arnés imprima sobre CONSTRUCCIÓN son diagnóstico, y ninguna rama de spec o de motor se justifica con ellas (las ramas de spec citan al trader, ev-/fb-, nunca una cifra de rentabilidad).
> Porqué: es la decisión de Aleks del 2026-10-29 y no mueve ningún umbral ya pre-registrado.
>
> 6. Camino de la cuenta: (b), una cuenta por mes en construcción (y en mayo cuando se mida); en los meses no vistos, arrastrada en todo el tramo (punto 4). ADR-0092 enmienda ADR-0053 §6 y la condición de la corrida que cuenta de ADR-0070, y lo dice. Es una condición del recorrido, no una opción: OPCIONES_QUE_NO_CAMBIAN_LA_CORRIDA no cambia, y --diagnostico-cuenta-diaria sigue siendo diagnóstico. Lo implementa una rama de motor corta, propia, ANTES de la re-corrida que cuenta (trabajo/cuenta-por-mes; Opus · alto; test que rompe en main), no esta rama ni la re-corrida.
> Porqué: en vivo la cuenta nunca salta de enero a abril; el arrastre entre meses no contiguos es un hecho del código (cli.py y cableado.py, 0.c).
>
> 7. Tolerancias por operación (3 puntos, 15 minutos): (a), quedan. Regla escrita ANTES de medir A-16: si su mediana de distancia M1 supera 3 puntos, o la proporción dentro del rango baja del 50 %, cada cifra de fidelidad lo dice («la cobertura tiene un techo que no es del bot») y nace en Technical Debt una línea para que la decisión la tome un ADR propio; en esta rama la tolerancia no cambia, salga lo que salga.
>
> 8. A-16: (a). Se mide en la fase 1 y queda ABIERTA, con resuelve_en F26, sin tocar knowledge/spec/. La medida y las previas que encontró el auditor (BLOQUE-DE-LA-CAJA.md, ABRIL-Y-LA-CAJA.md, LA-CAJA-DEL-29-DE-ABRIL.md, VIABILIDAD-TRADER.md) se nombran en el informe y en ADR-0092; su cierre va a la primera rama que toque knowledge/spec y pague la deuda del panel de FTMO.
>
> 9. Diseño de A-16: (a), M1 BID más el tick del lado en que se llenaría (BID en la venta, ASK en la compra) y, aparte, los dos lados; N, mediana, p90 y proporción dentro del rango, en total y por mes, y cuántas sin ticks en su minuto. Sin mes anterior.
>
> 10. engine/: (a), solo salida, en arnes.py y cableado.py: una tabla nueva «### Posiciones» (o columnas en «### Ordenes», lo que deje la salida más legible; lo dices) con desenlace (de clasificar_cierre), PnL bruto, comisión, swaps, PnL neto en USD, riesgo en USD al colocar y R neto; la línea de la cascada por criterios y la de las métricas de rentabilidad (marcada «diagnóstico» en construcción); y que el criterio lleve el stop del caso (arnes._operacion). El test fija que la salida existente no cambia byte a byte salvo las líneas y la tabla nuevas, y que el emparejamiento por operación da lo mismo con y sin el stop. Ninguna decisión ni ningún llenado cambia. El contrato se amplía a src/botsito/engine/arnes.py y cableado.py en un commit, con este punto como fuente; el riesgo sigue medio. Las funciones de cálculo (cascada, R neto, remuestreo por días, drawdown, N, punto de equilibrio, recálculo del punto 3) van puras en cases/criterio_fidelidad.py, con tests sintéticos, y las cifras en criterio_fidelidad.yaml.
>
> 11. Sesgo 3: (a). La re-corrida da la cifra entera y, además, la misma sin las operaciones del bot que acabaron en break even (desenlace break_even de clasificar_cierre, el mecanismo, no un PnL cero) en los libros sin vídeo (enero, agosto y abril salvo el 29); julio, provisional como grabado hasta T. Es diagnóstico: no entra en ningún umbral.
>
> 12. NOTAS: (a). Una NOTA en la cabecera de MASTER_PLAN, junto a la de ADR-0082: la condición necesaria para operar en vivo es la rentabilidad de ADR-0092, F27 sigue y F35 sigue siendo la decisión humana; la fila de F30 (depende de F26) la toca G con la de §H. En PREREGISTRO.md, una NOTA que nombre ADR-0092 y lo que tiene que llevar para la rentabilidad, dejando intacta la marca «SIN RELLENAR» (holdout.py, MARCA_SIN_RELLENAR): la ampliación de «Que tiene que llevar» es de G.
>
> 13. Exposiciones: (a), las cuatro filas como las propones, cada una el día que se haga y antes de correr nada.
>
> Campos nuevos de criterio_fidelidad.yaml (ADR-0002; cargados y validados por cargar_criterio con los validadores que hagan falta —_fraccion solo admite 0..1 y _entero rechaza textos—, y un yaml sin ellos no carga): tolerancia_stop_puntos 3 (entero, como tolerancia_entrada_puntos); y un bloque rentabilidad con fase "fondeada", n_minimo 100, esperanza_minima_r "0.10", percentil_remuestreo 5, replicas_remuestreo 10000, semilla_remuestreo 20261107, perdida_diaria_max "0.03", perdida_total_max "0.06", deslizamiento "pendiente_F17", percentil_deslizamiento_f17 90, meses ["2025-06","2025-07","2025-08","2025-09","2025-10","2025-11"], extension ["2025-05","2025-04","2025-03","2025-02","2025-01"] y vistos_rentabilidad []. La cabecera del yaml copia «declare quemado» de ADR-0043 «Cambios»: ADR-0092 enmienda esa frase con su NOTA (la cláusula se dispara con la primera salida sobre MEDIDA; declarar lo visto lo exige ADR-0070 punto 4) y la cabecera cita la NOTA.
>
> Lo demás de la fase 1, como dice el encargo (un commit por punto, sin ninguna corrida del arnés). En las líneas del cierre (0.h): F reescrita a «Siguiente: la rama de la cuenta por mes (ADR-0092, trabajo/cuenta-por-mes) y después la re-corrida que cuenta (ADR-0070 §3), la primera con la comisión medida (ADR-0090 §3), el sello del respaldo de ADR-0091 y el método de ADR-0092;», con el resto de F igual; en la hoja de ruta, R3.7 HECHA, una entrada nueva en R3 para la cuenta por mes antes de la re-corrida, y en R5 la medida de rentabilidad sobre junio-noviembre de 2025 con las condiciones del punto 4. Fila de ERRORES-RECURRENTES preparada con este hallazgo del consultor, que su auditor no vio: el encargo situó la línea «habilita medir…» en ADR-0070 §3 y es el punto 5 (menor; lección: un número de sección se cita leído, no del borrador).
>
> Sigue la fase 1. Rama lista para revisión, NO cerrada.

## Fase 1 · La respuesta aplicada (2026-11-07)

Antes de escribir nada, medí lo que la respuesta afirma del repo (CLAUDE.md, «Como se trabaja»):
- `"2025-12"` está en `knowledge/cases/meses_reservados.yaml` (con `2026-02` y `2026-03`), y
  `cases/holdout.py:634` tapa por número de mes en cualquier año (`tapados = {int(mes[5:7]) ...}`):
  meter un mes de 2025 taparía su número también en 2026. Cierto.
- El calendario de cierres empieza el 2025-12-04 (`knowledge/cuentas/cierres/ftmo-2step-swing-100k.yaml:18-22`). Cierto.
- `firma_fases` = `"reto verificacion fondeada"` (`ftmo-2step-swing-100k.yaml:86`). Cierto.
- `data/manifests/` solo tiene 2026 (eurusd-m1 de 2026-01 y de 2026-03 a 2026-09, sin febrero, y
  ticks de los cuatro meses de construcción). Cierto. *(Corregido tras el revisor, a6: decía «de
  2026-01 a 2026-09».)*
- F30 depende de F26 (`MASTER_PLAN.md:124` en `main`; `:132` en la rama, tras la NOTA nueva). Cierto.
  *(Corregido tras el revisor, a3.)*
- VIABILIDAD-TRADER.md §2 es «Esperanza en R, con intervalo del 95 % por bootstrap» (`:85`). Cierto.
- Los heredados 7 y 9 (`HISTORIA.md:698` y `:701`), verificados como pide el punto 4: los dos tocan
  la descarga de 2025. El 7, porque la guardia de `stable/F14-cobertura` saca junio del universo de
  un paquete ciego y junio de 2025 es un junio; el 9, porque `manifiestos_del_prefijo` toma todo lo
  del prefijo del kit, así que un manifiesto de 2025 con ese prefijo entra en `universo()` (no
  solapa con 2026, que es lo que rompe `kit build`, pero cambia el universo). Escrito en ADR-0092 §5
  como condición de la rama de la medida.

### 1.1 Punto 1: ADR-0092, los recuadros, las NOTAS y el índice

- `docs/adr/0092-el-bot-se-construye-por-fidelidad-y-se-juzga-por-rentabilidad.md`, con su
  numeración propia (§1 a §13); cada § dice de qué punto de la respuesta sale. Las cifras, solo con
  el nombre de su campo y entre paréntesis el valor de la respuesta; viven en el yaml (punto 2).
- Recuadros: ADR-0043 en su Decision (la fidelidad por criterios, tras las métricas), en «Fuera del
  criterio» (el stop entra en la de criterios; A-18 y A-31 RESUELTAS) y una NOTA en «Cambios» (la
  cláusula no se ha disparado; mayo no se quema); ADR-0070 punto 3 (la cuenta por mes, condición de
  la corrida que cuenta; la lista cerrada y la línea del punto 5 no cambian) y una NOTA en el punto
  4 (lo visto, en ADR-0092 §12); ADR-0053 §6 (una cuenta por mes en construcción; arrastrada en los
  meses no vistos).
- NOTA en la cabecera de `docs/plan/MASTER_PLAN.md`, tras la de ADR-0082 (punto 12). **La de
  `docs/validation/PREREGISTRO.md` no está: PARADA 2** (abajo). La escribí y, con ella estadiada,
  `tests/unit/test_puerta_holdout.py::test_con_el_preregistro_de_hoy_la_puerta_se_niega_y_nombra_adr_0021`
  falló en sus seis particiones: la puerta compara el fichero con HEAD
  (`cases/holdout.py:124-134`, `_commiteado_y_sin_cambios`) y, con un cambio sin commitear, el
  motivo es «no esta commiteado tal como esta en el arbol» y no «sigue vacio», que es lo que el test
  exige (`test_puerta_holdout.py:39`). Como `make check` sella el árbol estadiado ANTES del commit,
  ningún commit puede cambiar PREREGISTRO.md con ese test en verde, y `--no-verify` está prohibido.
  Quité el cambio (guardado en la carpeta de trabajo) y ADR-0092 y la fila del índice lo dicen.
- La fila 0092 del índice (`docs/adr/README.md`).
- **«Lo visto, declarado» (ADR-0092 §12) contra el repo:** la lista de L, más todas las salidas del
  arnés sobre construcción commiteadas: `grep -rlE '^(\[[^]]*\] )?CONJUNTO: construccion'
  docs/validation/` da 12 ficheros (los 8 de la raíz de `docs/validation/` y los 4 de
  `anexos/RECORRIDA-CONSTRUCCION/` y `anexos/RESPALDO-M1/`), y `grep -l 'CONJUNTO: construccion'
  docs/validation/anexos/*/*.txt` añade los diagnósticos de `CORRIDA-CONSTRUCCION`,
  `SESGO-H4-COLOR`, `MARGEN-LOTE` y `PUNTO-USADO` y el `diff-linea-base.txt` de RECORRIDA. El ADR
  las nombra todas.
- El contrato se amplía en este commit (punto 10 de la respuesta): `src/botsito/engine/arnes.py`,
  `src/botsito/engine/cableado.py` y `docs/adr/0053-el-cableado-del-simulador.md`; de
  `rutas_protegidas` sale la carpeta `src/botsito/engine/` y entran, por nombre, el bróker, el
  llenado, la cuenta, las primitivas y el motor, que no se tocan. Riesgo, medio.
- El bloque `ids-inexistentes` sale del encargo y de este informe en este commit, como decía.
- La respuesta del consultor, copiada tal cual al final del encargo y de este informe, va en este
  mismo commit y no en uno propio: así cada `make check` (unos 21 minutos) sella un punto.

### 1.2 Punto 2: el yaml, las funciones puras y la salida del arnés

**`knowledge/cases/criterio_fidelidad.yaml`** (ADR-0002): `tolerancia_stop_puntos: 3` y el bloque
`rentabilidad` con los trece campos de la respuesta, con los valores de la respuesta y ninguno más
(`fase: fondeada`, `n_minimo: 100`, `esperanza_minima_r: "0.10"`, `percentil_remuestreo: 5`,
`replicas_remuestreo: 10000`, `semilla_remuestreo: 20261107`, `perdida_diaria_max: "0.03"`,
`perdida_total_max: "0.06"`, `deslizamiento: pendiente_F17`, `percentil_deslizamiento_f17: 90`,
`meses` de 2025-06 a 2025-11, `extension` de 2025-05 a 2025-01 y `vistos_rentabilidad: []`); la
cabecera cita la NOTA de ADR-0043 «Cambios». Ningún campo existente cambia.

**`src/botsito/cases/criterio_fidelidad.py`**, todo puro:
- la carga: `cargar_criterio` exige `tolerancia_stop_puntos` (entero positivo, como la de entrada) y
  el bloque entero (`_rentabilidad`). Validadores nuevos, porque `_fraccion` solo admite 0..1 y
  `_entero` rechaza textos: `_decimal` (un número escrito como TEXTO, para que `0.10` no se lea en
  coma flotante), `_percentil` (1 a 99), `_meses_validos` (AAAA-MM, sin repetir); y tres
  comprobaciones de conjunto: `meses` no vacío, ningún mes a la vez en `meses` y `extension`, y
  ninguno de construcción ni de medida;
- `Operacion` gana `stop` opcional (None en el bot); `Criterio` gana `tolerancia_stop_puntos` y
  `rentabilidad`, con None por defecto solo para los criterios sintéticos de los tests de antes
  (ocho construyen `Criterio` por posición; `cargar_criterio` los exige);
- la cascada (ADR-0092 §2): `OrdenCriterio`, `cascada_por_criterios` y `cascada_por_mes`, con los
  escalones `SIN_ORDEN`, `ENTRADA_FUERA`, `STOP_FUERA`, `SIN_STOP` (un caso sin stop; no hay
  ninguno en construcción), `NO_LLENADA` («en el nivel, no llenada»), `LLENADA_FUERA` y `COMPLETA`;
- la rentabilidad (§3): `PosicionCerrada`, `r_neto`, `esperanza_r`, `percentil_por_dias` (con
  reemplazo, tantos días como los corridos, con o sin operaciones; percentil de rango inferior;
  determinista por la semilla), `perdida_diaria_maxima` y `equity_minima_del_tramo` (sobre la curva
  de equity), `medir_rentabilidad` y `veredicto_rentabilidad` («insuficiente» sin N, «no pasa» con
  un motivo por letra, «pendiente de F17» con todo cumplido mientras el deslizamiento lo esté);
- el deslizamiento (§4): `con_deslizamiento`, `curva_con_deslizamiento`, `punto_de_equilibrio` y
  `veredicto_con_f17` (la mediana restada a cada llenado afectado, b) a e) otra vez sobre la curva
  recompuesta, y la esperanza con el percentil 90 > 0).

**`src/botsito/engine/arnes.py` y `cableado.py`, SOLO salida** (punto 10):
- `arnes._operacion` lleva el stop del caso: los 75 ficheros de `knowledge/cases/dev/` lo traen
  (`grep -l 'stop:' knowledge/cases/dev/*.yaml | wc -l` = 75 de 75), y de ellos 69 son los días de
  construcción con operaciones (`medir-a16.txt:2`) y 6 son días dev de mayo, que es MEDIDA. Ese
  `grep` leyó el contenido de esos 6 casos de mayo (solo cuántos llevan la clave; ni nombres ni
  valores): leerlos no necesita puerta (ADR-0025 §4), y se declara en HOLDOUT-EXPOSICIONES el mismo
  día. *(Corregido tras el revisor, a2: decía «los 75 casos dev de construcción con operaciones».)*
- `MotorCableado` gana `operaciones_trader` y `criterio`, que rellena `construir_motor_cableado`
  con lo que ya recibía (los días y el criterio). Así la cascada tiene las operaciones del trader
  y las órdenes del bot sin tocar `cli.py`, que no está en el contrato. Ninguna decisión los lee;
- una sección nueva AL FINAL del informe de la simulación, «## El metodo de ADR-0092 (solo
  salida…)»: «### Posiciones» (una tabla nueva y no siete columnas más en «### Ordenes», que ya
  lleva diecisiete: lo dice el punto 10, «lo dices»), «### Fidelidad por criterios» (la cascada por
  mes y en total, y las órdenes sin trader) y «### Rentabilidad» (a) a f), el veredicto y el punto
  de equilibrio), marcada DIAGNÓSTICO sobre construcción. El PnL bruto usa la misma función que la
  cuenta (`cuenta.pnl`); la comisión, como la carga `_a_la_cuenta`; el riesgo, como la anotación
  de la orden (`primitivas_broker._margen_al_colocar`: lote × distancia / escala × contrato).

**Tests** (sintéticos): `tests/unit/test_criterio_campos_adr0092.py` (26: el yaml real carga; sin
cada campo nuevo no carga; valores mal formados no cargan), que importa SOLO lo que ya existía en
`main` para que allí rompa por lo que mide; y `tests/unit/test_metodo_adr0092.py` (30, y 33 con
el test del golden de `main` que se añadió tras el revisor: cada escalón
de la cascada, el desempate, las órdenes sin trader, el emparejamiento por operación igual con y sin
stop, el stop en `arnes._operacion`, R neto, remuestreo, drawdown, el veredicto por letra, el
deslizamiento y F17, y la salida del motor sobre el día sintético de `test_cableado.py`: la sección
va al final y lo de antes no cambia; la tabla de posiciones cuadra con la cuenta, `neto ==
saldo − capital`; sin criterio lo dice y con él saca cascada y rentabilidad). Los tests de
antes que tocan el criterio, el arnés y el cableado siguen en verde (`test_criterio_fidelidad`,
`test_umbral_mayo`, `test_diferencias_por_operacion`, `test_cableado`, `test_arnes_motor`,
`test_huecos_motor`, `test_visor`, `test_simulacion`, `test_cuenta_7_de_agosto`,
`test_selector_orden_stop`, `test_ensayo_marzo` y `tests/contract/`), y `lint-imports`: 4 kept.
`Tests Currently Passing` de PROJECT_STATE pasa de 1880 a 1903 funciones de test (`state check`), y a 1904 con el test del golden.

**Regresión contra `main`** (skill `comparar-con-main`), sin ninguna corrida del arnés:
- estado del repo antes y después: `git branch --list` = `main` y la rama; 151 tags; `origin` solo
  `refs/heads/main`; `git worktree list` sin clones al acabar. En `C:/cm` hay restos de ramas
  anteriores que no son de esta y no se tocaron;
- clon `C:/cm/mf` (`git worktree add --detach … main`, e01e28c) con los dos ficheros de test de la
  rama copiados dentro: `test_criterio_campos_adr0092.py` da **1 passed y 25 failed, todos «DID NOT
  RAISE CriterioError»** (el yaml de `main`, sin los campos, carga);
  `test_metodo_adr0092.py` **no se colecciona**: `ImportError: cannot import name 'COMPLETA'`.
  Salidas en `anexos/METODO-FIDELIDAD-RENTABILIDAD/tests-campos-con-main.txt` y
  `tests-metodo-con-main.txt`. Ningún test lee `data/`, así que el clon no llevó `settings.local.toml`;
- **la salida existente, byte a byte**: el lado «rama» no puede ser HEAD porque el punto 2 aún no
  está commiteado (la skill pide la rama commiteada; desvío declarado): es un segundo clon
  `C:/cm/rf` (`--detach HEAD`, 56eb235) con los cuatro ficheros cambiados del punto 2 copiados. En
  los dos, el mismo volcado del informe de la simulación sobre el día sintético con tres rutas
  (stop, hueco y viva). El volcado es AUTOCONTENIDO (`montar_volcado.py` copia las líneas 1-225 de
  `test_cableado.py`, sin su import de `tests.unit`), porque la guardia niega ejecutar en un clon un
  test que no está en el repo y carga `tests.unit` («no se pudo resolver el modulo
  `tests.unit.test_cableado`»); es lo que propone su mensaje, no un rodeo. Resultado
  (`comparar_volcados.py`, `volcados-main-rama.txt`):

  | fichero | sha256 main | sha256 rama | sha256 de la rama hasta la sección nueva | igual |
  |---|---|---|---|---|
  | volcado-hueco.txt | 5a3878781676f7a6 | 1c59d0d6308f3e13 | 5a3878781676f7a6 | sí |
  | volcado-stop.txt | 02d0872ac4678050 | 00066d7f443f4c63 | 02d0872ac4678050 | sí |
  | volcado-viva.txt | 89cb70b85dcfafc0 | 752c15450648c7a6 | 89cb70b85dcfafc0 | sí |

  Lo único que cambia es la sección nueva al final; sin criterio en el motor sintético, dice «sin
  el criterio de ADR-0092». La fila de la ruta stop: compra límite de 25,90 lotes, bruto −440,30,
  comisión 129,50 (2,50 por lote y lado), neto −569,80, riesgo 414,40, R neto −1,375. Son cifras
  de un día SINTÉTICO de 2030, no del bot sobre construcción;
- los dos clones, quitados con `git worktree remove --force` (llevaban los tests copiados y los
  volcados, sin seguir) y `git worktree prune`. Las salidas, pasadas a LF (salían con CRLF).
- **Repetida tras el revisor (b4), con la rama ya commiteada**: clones `C:/cm/mf2` (`main`,
  e01e28c) y `C:/cm/rf2` (`--detach HEAD`, 1b10082, que lleva el punto 2 commiteado, sin copiar
  nada). Los mismos seis hashes de la tabla de arriba, en los dos lados: la copia de la primera
  vez era el código que se commiteó. `volcados-main-rama.txt` es ya esta salida. Los tres
  volcados de `main` quedan congelados en `tests/golden/informe_simulacion/main-{hueco,stop,viva}.txt`
  (con su línea en `tests/golden/README.md`), y `test_lo_que_ya_salia_es_byte_a_byte_lo_de_main`
  exige que la salida de la rama empiece EXACTAMENTE por ellos: es el test del punto 10 que compara
  con `main` y no con la propia rama.

**Lo que queda del punto 11** (sesgo 3): la cifra sin las operaciones del bot de break even en los
libros sin vídeo necesita saber qué días son de un libro sin vídeo, y la respuesta no nombra dónde
vive esa lista (ningún campo del yaml la lleva). No la invento en `src/` ni añado un campo que la
respuesta no lista: PARADA 2, punto 1. La re-corrida va después de `trabajo/cuenta-por-mes`, así que
no bloquea nada de esta rama.

### 1.3 Punto 3: A-16 medida, y los recuentos de c), d) y e) con su guion

**La exposición, antes de correr nada** (punto 13): fila del 2026-11-07, «la fase 1», en
`HOLDOUT-EXPOSICIONES.md`, con sus cuatro partes. Los `make check` y los dos clones del punto 2 ya
se habían hecho cuando la escribí: van declarados el mismo día, pero después, y la fila lo dice.
`medir_a16.py` y los recuentos se declararon antes de ejecutarlos (la fila estaba estadiada).

**A-16** (`anexos/METODO-FIDELIDAD-RENTABILIDAD/medir_a16.py . --filas`, exit 0, salida
`medir-a16.txt`; el diseño, el de 0.f con la respuesta, punto 9). Lo que mide es lo que hace el
TRADER contra los datos, no el bot. Por la compuerta del arnés: 76 días dev de construcción, 69 con
operaciones, 198 operaciones; ninguna sin M1 en su minuto. Distancia en puntos de la entrada del
trader (Oanda, FX Replay) al rango de la M1 BID de Dukascopy del minuto del llenado, y al tick más
cercano de ese minuto:

| mes | N | mediana M1 | p90 M1 | dentro del rango M1 | mediana tick del lado | p90 tick del lado | mediana tick dos lados | p90 tick dos lados | sin ticks en su minuto |
|---|---|---|---|---|---|---|---|---|---|
| 2026-01 | 54 | 0 | 0 | 94,4 % | 0 | 1 | 0 | 0 | 2 |
| 2026-04 | 35 | 0 | 1 | 85,7 % | 0 | 1 | 0 | 0 | 2 |
| 2026-07 | 67 | 0 | 0 | 91,0 % | 0 | 1 | 0 | 0 | 4 |
| 2026-08 | 42 | 0 | 0 | 97,6 % | 0 | 1 | 0 | 0 | 0 |
| **total** | **198** | **0** | **0** | **92,4 %** | **0** | **1** | **0** | **0** | **8** |

Fuera del rango M1 quedan 15 de 198: 9 a 1 punto, 4 a 2, 1 a 3 y 1 a 4 (recuento de las filas
por operación de `medir-a16.txt`). **La regla escrita antes de medir** (respuesta, punto 7; ADR-0092
§9): mediana M1 0 frente a 3 puntos y 92,4 % dentro frente al 50 %: **no se dispara**. No nace
ninguna línea de Technical Debt por ella, y la tolerancia no cambia. A-16 queda ABIERTA con
`resuelve_en: [F26]` (punto 8): esta rama no toca `knowledge/spec/`. Lo que la medida dice y lo que
no:
- dice que la entrada del trader EXISTIÓ, en 183 de 198 operaciones, dentro de la vela de Dukascopy
  del minuto de su llenado, y a 1-4 puntos en las otras 15; con ticks, la mediana al tick más
  cercano del lado del llenado es 0 y el p90 es 1 punto;
- no compara velas con velas ni la ruptura de un nivel por una milésima, que es la pregunta de A-16
  (`ambiguedades.yaml:291-292`): para eso siguen las medidas previas (`BLOQUE-DE-LA-CAJA.md` §2.3,
  mediana +2 puntos con OANDA por encima; `VIABILIDAD-TRADER.md` §4, 4 casos a 5-11 puntos), que
  ADR-0092 §10 nombra. Una vela de un minuto tiene rango de varios puntos: estar dentro no quiere
  decir que las dos series marquen el mismo precio en el mismo instante.

**Los recuentos de c), d) y e)**, ahora con su guion en el anexo:
- c) y e): `recuentos_vistos.py anexos/RESPALDO-M1` → `recuentos-vistos.txt`, sobre las dos
  salidas ya vistas: las mismas cifras que 0.c y 0.e (165 de 198 operaciones del trader en días con
  la cuenta congelada en `cuenta-arrastrada.txt`; las tablas de Δ, partidas por lado);
- c): `huecos_material.py .` → `huecos-material.txt`: tres huecos y cuatro tramos, como en 0.c;
- la compuerta: `recuento_compuerta.py .` → `recuento-compuerta.txt`: 34 casos reservados y 34
  ocultos, todos en 2026-05, 2026-06 y 2026-09; 0 en los cuatro meses de construcción; 76 días dev y
  198 operaciones;
- d) no tiene recuento: el encargo pide decir cómo se obtiene el desenlace, sin calcular la métrica
  (0.d), y desde el punto 2 lo da la columna «desenlace» de «### Posiciones». La métrica del
  sesgo 3 espera a la PARADA 2, punto 1.

Los docstrings de `scripts/viabilidad_trader.py` y `viabilidad_comision.py` (Technical Debt) no se
tocan: esta rama no corrió esos guiones.

### 1.4 Punto 4: las líneas del cierre, probadas sobre una copia (no aplicadas en la rama)

Con `anexos/METODO-FIDELIDAD-RENTABILIDAD/simular_cierre.py` (en memoria; salida en
`simular-cierre.txt`), sustituciones exactas sobre PROJECT_STATE, la hoja de ruta y HISTORIA:

- **PROJECT_STATE.md**
  - sale **R** (`PROJECT_STATE.md:52`), con su registro nuevo al final de HISTORIA: «# Next Action
    HECHA · R · el método de juicio del bot · sale de PROJECT_STATE.md en
    trabajo/metodo-fidelidad-rentabilidad (fecha)». La letra ya tenía uno, del 2026-10-05
    (`HISTORIA.md:4689`), y el nuevo lleva su fecha (`DECISIONES-DE-PROCESO.md:29`). El texto del
    registro resume ADR-0092 y la medida de A-16, como está en el guion;
  - **F**, con el texto de la respuesta: «Siguiente: la rama de la cuenta por mes (ADR-0092,
    trabajo/cuenta-por-mes) y después la re-corrida que cuenta (ADR-0070 §3), la primera con la
    comisión medida (ADR-0090 §3), el sello del respaldo de ADR-0091 y el método de ADR-0092;», y
    el resto de F igual;
  - **G**: «… ADR-0073) y A-16.» pasa a «… ADR-0073) y A-16 (medida en R3.7, sigue ABIERTA). Y lo
    de ADR-0092: PREREGISTRO §«Que tiene que llevar» y MASTER_PLAN §H (y la fila de F30) con la
    rentabilidad (ADR-0092 §13).»;
  - **la segunda Regla viva** (`PROJECT_STATE.md:151`), con la redacción del punto 5, tal cual;
  - **Technical Debt**: no nace ninguna línea. La regla del punto 7 no se disparó (§1.3), y lo que
    queda pendiente (la NOTA de PREREGISTRO y la lista del sesgo 3) es la PARADA 2, no una deuda.
- **La hoja de ruta**
  - R3.7: `NA:R` sale de sus Refs (entra `ID:ADR-0092`) y gana «Estado: HECHA»;
  - **R3.8 nueva**, «Una cuenta por mes en la corrida que cuenta» (Refs `NA:F · ID:ADR-0092 ·
    ID:ADR-0053 · ID:ADR-0070`; depende de R3.7): `trabajo/cuenta-por-mes`, antes de la re-corrida;
  - R5.1: «A-16 …, que se mide antes, en R3.7» pasa a «A-16 …, medida en R3.7
    (METODO-FIDELIDAD-RENTABILIDAD.md §1.3) y ABIERTA»;
  - R5.2: sale `NA:R`; depende también de la cuenta por mes (R3.8), y el sello (R3.6) y el método
    (R3.7, ADR-0092) están HECHOS;
  - **R5.6 nueva**, «La rentabilidad, la puerta para operar en vivo» (Refs `NA:G · NA:N · HER:7 ·
    HER:9 · HER:10 · ID:ADR-0092 · F:F27`), con las condiciones del punto 4: junio a noviembre de
    2025 y su extensión, la fase fondeada, la spec sellada en PREREGISTRO (G), el calendario
    renovado hacia atrás (N), los datos según los heredados 7 y 9, el riesgo del spread supuesto
    por la hora de pared, la construcción en el umbral de ADR-0070, y que no da «pasa» antes de F17;
  - las dos corridas de R3.6 siguen en la re-corrida que cuenta (R3.7, «Qué es»: no se tocan).
- **Salida de la simulación:** `R viva en la copia? False; R HECHA en HISTORIA? True; NA:R en la hoja
  simulada? False`; `a: []`, `b: []`, `c: []`; PROJECT_STATE con las líneas del cierre **22.349
  bytes**, y con el Current Feature del cierre **22.411** (los cuatro tests de `test_project_state`
  pasan); por debajo de 23.000. Hoy, en la rama, `wc -c PROJECT_STATE.md` = 22.286.

## El encargo, punto por punto

| # | Requisito (encargo y respuesta) | Estado | Dónde |
|---|---|---|---|
| 1 | Base: main e01e28c, tag a 18f548e, CI 42400168427 verde, ninguna otra rama | Hecho | §0 |
| 2 | Abrir con abrir-rama: contrato con tramo, riesgo medio, artefacto | Hecho | `contrato.yaml`; commit 1380b6c |
| 3 | grep de «0092» antes de usarlo; revisar /model | Hecho | §0 |
| 4 | Ninguna corrida del arnés ni cifra agregada nueva del bot | Hecho | ningún `motor arnes` en la rama; las cifras del bot que salen son recuentos sobre salidas ya vistas (§0.c, §0.e) y las de un día SINTÉTICO de 2030 (§1.2) |
| 5 | NO cambia: decisiones, llenados, bróker, estrategia, spec, parámetros, perfil, tolerancias | Hecho | `git diff --stat main...HEAD`: ninguno de esos ficheros; los volcados del punto 2, idénticos hasta la sección nueva |
| 6 | PREREGISTRO no se rellena | Hecho | no se toca (PARADA 2) |
| 7 | Herencia R3.7 entera (cuatro sesgos, NOTA de MASTER_PLAN, F35, lo visto) | Hecho | §0.c a §0.f, §1.3; ADR-0092 §7 y §12; NOTA de MASTER_PLAN |
| 8 | Herencia RESPALDO-M1 §4.5 y su orden de cierre, punto 2 | Hecho | §0.c (165 de 198) |
| 9 | Herencia R5.1 y A-16: medida, sin cerrarla salvo decisión | Hecho | §1.3; A-16 ABIERTA (punto 8) |
| 10 | Herencia ACTIVAR-SESION-05 §0.b.7 y S-14 | Hecho | §0.d; ADR-0092 §11 |
| 11 | Herencia ADR-0090 §3 y §7, ADR-0051 §4: el deslizamiento | Hecho | ADR-0092 §4; funciones del punto 2 |
| 12 | ADR-0043 «Cambios» y ADR-0070 §4: sin quemar mayo; declarar lo visto; no escribir «quemado por ADR-0043» | Hecho | ADR-0092 §12; NOTA en ADR-0043; `grep "quemado por ADR-0043"` en los ADR, el plan, el yaml y este informe: solo esta fila, que lo cita (y el encargo copiado) |
| 13 | Reglas vivas: el mecanismo contra optimizar y la redacción de la segunda | Hecho | ADR-0092 §6 y §7; la regla, en las líneas del cierre (§1.4) |
| 14 | MASTER_PLAN §0, la NOTA de ADR-0082, F26, F27, F35, §H; condiciones previas de F26 nombradas | Hecho | §0.g; NOTA nueva; ADR-0092 §7 |
| 15 | Las dos corridas de R3.6 siguen en la re-corrida | Hecho | §1.4 |
| 16 | Docstrings de viabilidad y deuda del panel de FTMO: no se pagan | Hecho | §1.3; no se toca `knowledge/spec/` |
| 17 | Búsqueda de «R3.7», «NA:R», «método», «rentabilidad»… | Hecho | §0.i |
| 18 | Fase 0, puntos a) a i), sin tocar código ni knowledge | Hecho | §0.a a §0.k; commit 9b7fa7f |
| 19 | PARADA y espera | Hecho | «Lo que necesito que decidas»; respuesta copiada tal cual |
| 20 | Respuesta copiada tal cual con fase-cero | Hecho | final del encargo y de este informe |
| 21 | Fase 1, punto 1: ADR-0092, recuadros, NOTAS, índice, Fuente, ids-inexistentes fuera | Hecho de otra forma | §1.1, commit 56eb235. La NOTA de PREREGISTRO no entra: PARADA 2, punto 0 |
| 22 | Fase 1, punto 2: yaml, funciones puras, salida del arnés, tests, uno que rompe en main | Hecho | §1.2, commit del punto 2; 25 tests fallan en main y uno no se colecciona |
| 23 | Punto 2: un test que fija que la salida de decisiones no cambia, y que el emparejamiento da lo mismo con y sin stop | Hecho | `test_la_seccion_nueva_va_al_final_y_lo_que_ya_salia_no_cambia`, `test_el_emparejamiento_por_operacion_da_lo_mismo_con_el_stop_que_sin_el`; la regresión de hashes |
| 24 | Fase 1, punto 3: A-16 con su guion, salida y exposición; recuentos de c), d) y e) | Hecho | §1.3 |
| 25 | Fase 1, punto 4: el informe con las líneas del cierre sobre la copia | Hecho | §1.4 |
| 26 | Un commit por punto, con estadiar, state check, make check y su log | Hecho de otra forma | puntos 1, 2 y 3 en sus commits (56eb235, 47a526c, 1b10082); el punto 4 va en el MISMO commit que el informe del revisor y lo que se hizo con sus hallazgos, para sellar una vez (desviación 12) |
| 27 | ruff format, ruff check y mypy sobre lo tocado | Hecho | §1.2 |
| 28 | Respuesta, punto 0: las piezas y la tolerancia del stop | Hecho | ADR-0092 §1; yaml |
| 29 | Respuesta, punto 1: la cascada contra las órdenes, por mes y en total | Hecho | ADR-0092 §2; `cascada_por_criterios`; «### Fidelidad por criterios» |
| 30 | Respuesta, punto 2: el criterio de rentabilidad a) a f) | Hecho | ADR-0092 §3; `veredicto_rentabilidad` |
| 31 | Respuesta, punto 3: la regla del deslizamiento y el punto de equilibrio | Hecho | ADR-0092 §4; `veredicto_con_f17`, `punto_de_equilibrio` |
| 32 | Respuesta, punto 4: los meses, la fase, la extensión, dónde viven, las condiciones | Hecho | ADR-0092 §5; yaml; R5.6 en las líneas del cierre |
| 33 | Respuesta, punto 5: el papel de la fidelidad; la línea «habilita medir» y sus tests no cambian | Hecho | ADR-0092 §7; `habilita_medir` y `test_umbral_mayo.py` sin tocar |
| 34 | Respuesta, punto 6: una cuenta por mes, enmienda de ADR-0053 §6 y de ADR-0070; la implementa otra rama | Hecho | ADR-0092 §8; recuadros; R3.8 |
| 35 | Respuesta, punto 7: las tolerancias quedan y la regla de A-16 | Hecho | ADR-0092 §9; no se dispara (§1.3) |
| 36 | Respuesta, punto 8: A-16 ABIERTA y las medidas previas nombradas | Hecho | ADR-0092 §10; §1.3 |
| 37 | Respuesta, punto 9: el diseño de A-16 | Hecho | `medir_a16.py` |
| 38 | Respuesta, punto 10: engine solo salida; contrato ampliado en un commit | Hecho | §1.1 y §1.2 |
| 39 | Respuesta, punto 11: la cifra sin los break even de los libros sin vídeo | Parcial | ADR-0092 §11 lo fija; dónde vive la lista de libros, PARADA 2, punto 1 |
| 40 | Respuesta, punto 12: NOTAS en MASTER_PLAN y PREREGISTRO | Parcial | MASTER_PLAN, sí; PREREGISTRO, PARADA 2, punto 0 |
| 41 | Respuesta, punto 13: las exposiciones | Hecho de otra forma | la fila de la fase 1; los `make check` y los clones del punto 2 se declararon el mismo día pero después (§1.3) |
| 42 | Respuesta: los campos del yaml, validados; un yaml sin ellos no carga; la cabecera cita la NOTA | Hecho | §1.2 |
| 43 | Respuesta: F, R3.7 HECHA, la entrada de R3 y la de R5 en las líneas del cierre | Hecho | §1.4 |
| 44 | Respuesta: la fila de ERRORES-RECURRENTES con el hallazgo de la sección | Hecho | abajo |
| 45 | CI: sin fix/ (no toca hooks, rutas, .claude/ ni plataforma) | Hecho | ningún fichero de esos en el diff |
| 46 | El revisor (opus) con los seis alcances, y su informe pegado | Hecho | §8 |

## Desviaciones, declaradas

1. **La NOTA de PREREGISTRO.md no está** (punto 12): con el fichero cambiado sin commitear,
   `test_puerta_holdout` falla y `make check` no sella. PARADA 2, punto 0.
2. **La lista de los libros sin vídeo no se escribe** (punto 11): la respuesta no dice dónde vive.
   PARADA 2, punto 1.
3. **La respuesta del consultor y el contrato ampliado van en el commit del punto 1**, y no en
   commits propios: un `make check` por punto.
4. **Las exposiciones (1) y (2) de la fila de la fase 1 se declararon después de hacerlas**, el
   mismo día (§1.3). El punto 13 pedía «antes de correr nada».
5. **El lado «rama» de la regresión byte a byte** es un clon de HEAD con los cuatro ficheros del
   punto 2 copiados, porque el punto aún no estaba commiteado (la skill pide la rama commiteada), y
   el volcado es autocontenido porque la guardia niega un test fuera del repo que importe
   `tests.unit` (§1.2).
6. **Tres `make check` en la apertura** por dos trampas ya conocidas (el id futuro y un log sin
   seguir; §0).
7. **Los campos nuevos de `Criterio` llevan `None` por defecto**, para no tocar los ocho tests que
   lo construyen por posición; `cargar_criterio` los exige, y es la única vía del arnés.
8. **`MotorCableado` gana `operaciones_trader` y `criterio`**, que no nombra el punto 10, para que
   la cascada se escriba sin tocar `cli.py`, que no está en el contrato. Solo salida.
9. **El bloque `rentabilidad` del yaml lleva una clave `adr: ADR-0092`** que la respuesta no lista,
   como la de arriba del fichero (`adr: ADR-0043`). No se carga ni se valida: solo dice de dónde
   sale el bloque (revisor, a7).
10. **La forma del remuestreo por días la elegí yo** donde la respuesta no la detalla (con
    reemplazo, tantos días como los corridos, media agrupada, percentil de rango inferior). Va
    escrita en ADR-0092 §3 c) y la confirma el consultor: PARADA 2, punto 2 (revisor, b6).
11. **El test del golden de `main`** (`tests/golden/informe_simulacion/`), añadido tras el revisor
    (b4): no lo pedía el encargo, pero es el único test del repo que compara con la salida de
    `main` y no con la de la propia rama.
12. **El punto 4 no tiene commit propio**: el `make check` que lo sellaba empezó antes de que la
    guardia negara el `git add` (iba encadenado con `state check`), así que lo paré sin esperar a
    que no sellara (revisor, a1), y el punto 4 va con el informe del revisor y sus arreglos en un
    solo commit sellado.

## Lo que no pude medir (fase 1)

- La cascada, la rentabilidad y la tabla de posiciones sobre la CONSTRUCCIÓN: exigen una corrida
  del arnés, prohibida aquí. Solo están probadas sobre el día sintético y en los tests. La primera
  salida real es la de la re-corrida que cuenta, después de `trabajo/cuenta-por-mes`.
- Si RN-032 seguiría congelando la cuenta con el motor de hoy (0.k).
- El remuestreo con 10.000 réplicas sobre 76 días y decenas de operaciones: cuánto tarda en la
  corrida real. En los tests corre con 200 y 500 réplicas.

## La fila de ERRORES-RECURRENTES (preparada para el cierre; la escribe `cerrar-rama`)

| Rama | Hallazgos del revisor | Hallazgos del consultor despues | Que se le escapo |
|---|---|---|---|
| `trabajo/metodo-fidelidad-rentabilidad` | Una pasada, opus, con los siete alcances del encargo (§8; lo hecho, §8.1): reglas 1 bloquea (a1, el `make check` sobre un árbol sin estadiar, ya parado), 1 importa (a2, los 6 casos dev de mayo en un `grep` sin declarar), 5 menor; encargo 1 bloquea (b1, la NOTA de PREREGISTRO: PARADA 2), 3 importa (b2, lo visto incompleto: el visor y lo derivado; b3, la letra e) del consultor cambiada a c) sin decirlo; b4, el test «byte a byte» comparaba la rama consigo misma: entra un golden de `main`), 2 menor. Todos arreglados o contestados | (1) **(menor, del consultor; su auditor no lo vio)** el encargo situó la línea «habilita medir…» en ADR-0070 §3, y es el punto 5. Lección: un número de sección se cita leído, no del borrador. | (2) **Un test de la puerta del holdout ata PREREGISTRO.md a HEAD**: ningún commit puede cambiar ese fichero con `make check` en verde, ni para una NOTA. Señal: una ruta que la puerta lee con `_commiteado_y_sin_cambios`. (3) **El informe cita su ADR futuro en el título**: el bloque `ids-inexistentes` exime el id solo en el documento que lo lleva, y el encargo lo trae, el informe no. (4) **Un log en la raíz rompe el sello** aunque `make check` salga en verde: los logs de las comprobaciones van fuera del repo. (5) **Una letra del consultor no se «corrige» al pasarla al ADR** sin declararlo (b3): se copia, y si parece un error, se pregunta. (6) **Un test de «la salida no cambia» que compara la rama consigo misma no prueba nada** (b4): la referencia es la salida de `main`, congelada como golden. (7) **Una orden encadenada que la guardia niega no ejecuta NINGUNA de sus partes**: el `git add` no se hizo y el `make check` siguiente corrió sobre un árbol sin estadiar (a1). |

## PARADA 2 · La NOTA de PREREGISTRO.md no se puede commitear con `test_puerta_holdout` en verde

Lo medido: arriba, en 1.1. El texto de la NOTA que pedía el punto 12, tal como lo escribí (no está
en el repo):

> **NOTA de ADR-0092 (2026-11-07, `trabajo/metodo-fidelidad-rentabilidad`; no rellena nada: este
> fichero sigue SIN RELLENAR).** Desde ADR-0092 la condicion necesaria para operar en vivo es la
> RENTABILIDAD pre-registrada (ADR-0092 §3), medida una vez sobre meses que el bot no ha visto
> (junio a noviembre de 2025, con su extension, §5); F26 queda como diagnostico. Para la
> rentabilidad, este fichero tendra que llevar (ADR-0092 §13): la metrica y su calculo (el R neto
> por operacion, §3); los umbrales (`criterio_fidelidad.yaml`, bloque `rentabilidad`); los meses, la
> extension y por que esos, y la fase (§5); el hash de la spec sellada y el sha de `src/` (§5); el
> tratamiento del deslizamiento, pendiente de F17 (§4); y que se hace si no pasa
> (`vistos_rentabilidad`, §5). La ampliacion de «Que tiene que llevar» es de G.

0. Dónde va lo que PREREGISTRO.md tendrá que llevar para la rentabilidad. Opciones: (a) no se toca
   PREREGISTRO.md en esta rama: lo dice ADR-0092 §13 (ya escrito) y la NOTA de MASTER_PLAN, y lo
   lleva G, que de todos modos tiene que cambiar ese test al rellenar el fichero; (b) esta rama
   cambia el test para que, con PREREGISTRO.md cambiado y sin commitear, acepte también el motivo
   «no esta commiteado» (es `tests/`, dentro del contrato); (c) un test nuevo de la rama que
   compruebe en un repo de prueba que la NOTA no quita la marca, y la NOTA en un commit aparte con
   el test viejo marcado como esperado que falle solo en ese commit. Recomiendo (a): el contenido ya
   está en ADR-0092 §13, y (b) y (c) aflojan una guardia del holdout para meter una nota. Coste de
   (a): hasta G, PREREGISTRO.md no nombra ADR-0092. Coste de (b): el test deja de distinguir «vacío»
   de «sin commitear» en el repo real.
1. Dónde vive la lista de los libros sin vídeo del punto 11 (enero, agosto y abril salvo el 29;
   julio, provisional como grabado hasta T). Opciones: (a) un bloque nuevo en
   `criterio_fidelidad.yaml`, `material_sin_video: {meses: ["2026-01", "2026-04", "2026-08"],
   dias_con_video: ["2026-04-29"], provisionales_con_video: ["2026-07"], fuente:
   ACTIVAR-SESION-05.md §0.b.7}`, y la línea en la salida del arnés en esta rama; (b) lo mismo, pero
   la línea y el bloque los hace `trabajo/cuenta-por-mes`, que va antes de la re-corrida; (c) un
   campo por libro en `knowledge/corpus/libros.yaml`, que es solo-añadir y no lo admite para los
   libros ya commiteados. Recomiendo (a): la clasificación ya está medida, y la re-corrida la
   necesita escrita antes; la función pura que filtra no hace falta escribirla aparte: es `medir`
   sobre las operaciones del bot sin las de break even de esos días. Coste de (b): una rama de motor
   corta carga con algo que no es del motor. Coste de (c): no se puede.
2. La forma del remuestreo de ADR-0092 §3 c), que la respuesta no detalla y que escribí yo
   (revisor, b6). Opciones: (a) la de `percentil_por_dias`, ya escrita en ADR-0092 §3 c): cada
   réplica sortea con reemplazo tantos días como los corridos, con o sin operaciones, y toma la
   media AGRUPADA del R neto de todas sus operaciones; percentil de rango inferior; `random.Random`
   con la semilla; (b) la media de las medias diarias, solo sobre días con operaciones; (c) remuestrear
   operaciones y no días. Recomiendo (a): los días sin operaciones existen en vivo (pesan en el
   número de operaciones de cada réplica) y la media agrupada es la misma esperanza de b). Coste de
   (b): un día con una operación pesa como uno con diez. Coste de (c): no es «por días», y deja
   fuera que los resultados de un mismo día se parecen.

Sigo con lo demás de la fase 1 mientras tanto, como dice el encargo.

## 8. El revisor

Subagente `revisor` (opus), lanzado con el informe terminado y el punto 4 estadiado, con los siete
alcances del encargo (reglas de la casa; el encargo y la respuesta; ninguna corrida del arnés ni
cifra agregada nueva del bot; ningún umbral que salga de la rama; el motor no cambia; todo día
leído de construcción y declarado; lo «visto» de ADR-0092 frente a lo commiteado). Su informe, tal
cual (no cita ningún tramo no citable: ninguna retirada):

> ## Informe del revisor · trabajo/metodo-fidelidad-rentabilidad · 2026-11-07
>
> Rama `trabajo/metodo-fidelidad-rentabilidad`, base `e01e28c`. Hay cinco commits (1380b6c, 9b7fa7f, 56eb235, 47a526c, 1b10082). El punto 4 está estadiado en el índice: el informe y los dos ficheros `simular_cierre.py` y `simular-cierre.txt`.
>
> ### Eje (a) · Reglas de la casa
> Resumen: 1 bloquea, 1 importa, 5 menor.
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | a1 | bloquea (para el commit del punto 4) | El `make check` que está corriendo empezó antes de que se estadiaran los dos ficheros del punto 4. CLAUDE.md dice que, mientras corre `make check`, lo que haya que escribir en el repositorio espera, y `git add` escribe el índice. La huella hará fallar el sello, así que ese commit no se puede hacer con esta corrida: hay que relanzar `make check`. | `make-check.log:5` dice «CONTRATO: 32 ficheros dentro del contrato…». Ahora `uv run python scripts/contrato_rama.py` da «CONTRATO: 34 ficheros». El contrato cuenta `git diff --cached` (`scripts/contrato_rama.py:203`). En el gitStatus del arranque los dos ficheros salían como `??`; ahora `git status --porcelain` da `A  …/simular-cierre.txt` y `A  …/simular_cierre.py`. La huella está en `scripts/sello_make_check.py:12-18`. |
> | a2 | importa | Dos problemas en la misma frase del informe. (1) Dice «los 75 casos dev de construcción con operaciones lo traen», y no es así: los 75 ficheros de `knowledge/cases/dev/` incluyen 6 de mayo, que es medida y no construcción. Los de construcción con operaciones son 69. (2) Ese `grep` leyó el contenido de los 6 casos dev de mayo. Leerlos está permitido sin puerta (ADR-0025 §4), pero no está declarado: las dos filas del 2026-11-07 dicen «nada de un mes reservado» y «los días leídos son de construcción». | `METODO-FIDELIDAD-RENTABILIDAD.md:777-778`. Medido con `ls knowledge/cases/dev/` por mes: 21 de 2026-01, 16 de 2026-04, **6 de 2026-05**, 13 de 2026-07 y 19 de 2026-08. `medir-a16.txt:2` da «dias dev con operaciones: 69». Las filas están en `HOLDOUT-EXPOSICIONES.md` (diff, filas +102 y +103). |
> | a3 | menor | `MASTER_PLAN.md:124` es la línea de F30 en `main`. En la rama, con la NOTA añadida, es la `:132`, y la `:124` es F23. | `METODO-FIDELIDAD-RENTABILIDAD.md:699`. En la rama, `sed -n 124p` da «\| F23 …» y `grep -n "\| F30 "` da 132. `git show main:docs/plan/MASTER_PLAN.md`, línea 124, da F30. |
> | a4 | menor | Dos filas de «El encargo, punto por punto» no se sostienen hoy. La fila 26 dice «cuatro commits de fase 1 sellados» y el cuarto no está commiteado. La fila 46 dice «Hecho \| §8» y el informe no tiene §8; el propio Estado dice «Falta el revisor (§8)». | `METODO-FIDELIDAD-RENTABILIDAD.md:964`, `:984` y `:1065`. `grep -n "§8\|## 8"` no encuentra ninguna sección 8. |
> | a5 | menor | La fila de exposiciones de la fase 1 declara la M1 y los ticks «de cada uno de los 76 días dev». El guion salta los días sin operaciones, así que lee 69. Declara de más, no de menos. | `HOLDOUT-EXPOSICIONES.md`, fila +103. `medir_a16.py:105-106` (`if not d.operaciones: continue`). |
> | a6 | menor | El informe dice que hay M1 «de 2026-01 a 2026-09», y no hay manifiesto de 2026-02. | `METODO-FIDELIDAD-RENTABILIDAD.md:697-698`. `ls data/manifests/` da 01, 03, 04, 05, 06, 07, 08 y 09. |
> | a7 | menor | El bloque `rentabilidad` del yaml lleva una clave `adr: ADR-0092` que no está entre los campos que listó el consultor. Es inocua, pero no se declara. | `knowledge/cases/criterio_fidelidad.yaml`, diff, línea `+  adr: ADR-0092`. |
>
> Comprobado sin hallazgos:
> - **Contrato.** `contrato_rama.py` sale con exit 0. `state check` da «OK: rama 'trabajo/metodo-fidelidad-rentabilidad' …».
> - **knowledge validate** (a la consola, sin el log en la raíz): exit 0, con «OK: 924 documentos: todo id citado existe…» y «OK: 57 ambiguedades registradas…».
> - **pytest de 12 ficheros:** `test_adr`, `test_criterio_campos_adr0092`, `test_metodo_adr0092`, `test_puerta_holdout`, `test_umbral_mayo`, `test_criterio_fidelidad`, `test_cableado`, `test_no_business_literals`, `test_hoja_de_ruta`, `test_project_state`, `test_historia` y `test_diferencias_por_operacion`. Salen 211 puntos en la barra y ninguna F ni E (esta configuración no imprime la línea de resumen).
> - **Trailer `Fuente:`.** El único commit que toca `knowledge/cases` (47a526c) lleva «Fuente: ADR-0092, ADR-0043, ADR-0070», en el cuerpo y con ids que existen.
> - **Holdout.** Nada bajo `knowledge/cases/holdout/` en `git diff --name-status`.
> - **Régimen de cambios.** Ni evidence, ni feedback, ni manifests, ni transcripciones, ni fotogramas, ni `libros.yaml` en el diff. `ambiguedades.yaml` no cambia, y A-16 sigue ABIERTA en la línea 302.
> - **ADR.** `## Estado` empieza por ACTIVE en 0092 (:344), 0043, 0053 y 0070. Los recuadros de 0043, 0053 y 0070, la NOTA de MASTER_PLAN, HISTORIA (Archivo 60) y HOLDOUT-EXPOSICIONES solo añaden líneas: 0 líneas `-`.
> - **Ningún informe cerrado tocado.** Ningún sitio nuevo con `cita`.
> - **Citas comprobadas contra su fuente:**
>   - `holdout.py:634` (`tapados = {int(mes[5:7]) …}`);
>   - `ftmo-2step-swing-100k.yaml:86` (`valor: "reto verificacion fondeada"`);
>   - `cierres/ftmo-2step-swing-100k.yaml:18-22` (`desde: "2025-12-04"`);
>   - `test_puerta_holdout.py:39` («sigue vacio»);
>   - `holdout.py:124-134` y `:156-158`;
>   - `HISTORIA.md:4689` (el registro de R del 2026-10-05);
>   - `DECISIONES-DE-PROCESO.md:29`, que existe en `docs/runbooks/`;
>   - A-18 y A-31, RESUELTAS (`ambiguedades.yaml:382` y `:859`), como dice el recuadro de ADR-0043.
> - **Cifras.** Las del yaml son exactamente las de la respuesta: `tolerancia_stop_puntos` 3, `fondeada`, 100, "0.10", 5, 10000, 20261107, "0.03", "0.06", `pendiente_F17`, 90, los meses 2025-06 a 2025-11, la extensión 2025-05 a 2025-01 y `[]`.
>
> ### Eje (b) · Encargo
> Resumen: 1 bloquea, 3 importa, 2 menor. Requisitos: 24 hechos, 2 parciales, 1 no hecho (en PARADA 2), 2 hechos de otra forma.
>
> | # | Requisito | Estado | Evidencia |
> |---|---|---|---|
> | 1 | Abrir la rama: contrato con tramo, riesgo medio y artefacto; encargo copiado; Archivo 60 | Hecho | `contrato.yaml:1-4`; commit 1380b6c; `+# Archivo 60` |
> | 2 | Fase 0, puntos a) a i), sin tocar código ni knowledge, y la PARADA | Hecho | informe §0.a-§0.k y «Lo que necesito que decidas» (:501); 9b7fa7f solo toca el informe y HOLDOUT-EXPOSICIONES |
> | 3 | La respuesta, copiada tal cual en el informe y al final del encargo | Hecho | `diff` del encargo (:64-116) con el informe (:635-687) da IGUALES |
> | 4 | P1: ADR-0092 con recuadros en ADR-0043 y ADR-0070, más ADR-0053 §6 | Hecho | diff de los cuatro ADR |
> | 5 | P1: NOTA en la cabecera de MASTER_PLAN, junto a la de ADR-0082 | Hecho | `MASTER_PLAN.md:19-26`, justo tras la NOTA de ADR-0082 |
> | 6 | P1 / respuesta, punto 12: NOTA en PREREGISTRO.md | **No hecho (PARADA 2)** | ver b1 |
> | 7 | P1: fila del índice, `Fuente:`, bloque ids-inexistentes fuera | Hecho | `docs/adr/README.md` +1; 56eb235 lleva «Fuente: ADR-0043, …»; el bloque solo queda citado en `encargos:4` y `:48` |
> | 8 | P1: contrato ampliado a arnes.py y cableado.py en un commit | Hecho de otra forma (declarado) | `contrato.yaml:2,18-19`, en 56eb235; desviación 3 |
> | 9 | P2: yaml con los campos nuevos; un yaml sin ellos no carga | Hecho | `criterio_fidelidad.py:299-369`; en main, 25 tests fallan con «DID NOT RAISE» (`tests-campos-con-main.txt`) |
> | 10 | P2: funciones puras: cascada, R neto, remuestreo, drawdown, N, punto de equilibrio, F17 | Hecho | `criterio_fidelidad.py:372+`; 30 tests sintéticos |
> | 11 | P2 / punto 10: «### Posiciones» con desenlace, bruto, comisión, swaps, neto, riesgo y R neto; la cascada; la rentabilidad marcada «diagnóstico» | Hecho | `cableado.py:1116-1355` (CABECERA_POSICIONES, `_informe_metodo`) |
> | 12 | Punto 10: el criterio lleva el stop (`arnes._operacion`) | Hecho | `arnes.py:124-136`; test en `test_metodo_adr0092.py:171-174` |
> | 13 | Punto 10: test de que la salida existente no cambia byte a byte, y emparejamiento igual con y sin stop | Parcial | ver b4; `test_metodo_adr0092.py:157-168` (stop) y `:359-369` |
> | 14 | P2: al menos un test que rompe en main, con su salida pegada | Hecho | `tests-campos-con-main.txt`; `tests-metodo-con-main.txt` («ImportError: cannot import name 'COMPLETA'») |
> | 15 | P3: A-16 con su guion, su salida y la exposición previa | Hecho | `medir_a16.py`, `medir-a16.txt`, fila +103 |
> | 16 | Punto 9: M1 BID, tick del lado y de los dos lados, N, mediana, p90, dentro del rango, por mes y en total, sin ticks, sin mes anterior | Hecho | `medir_a16.py:104-152`; `tipo_precio: BID` en el manifiesto; `simulacion.py:194-206` (solo la ventana del día) |
> | 17 | Punto 7: la regla escrita antes de medir | Hecho | ADR-0092 §9; `medir_a16.py:157`; no se dispara (mediana 0, 92,4 %) |
> | 18 | Punto 8: A-16 ABIERTA, knowledge/spec sin tocar, las medidas previas nombradas | Hecho | `ambiguedades.yaml:302`; ADR-0092 §10 |
> | 19 | P3: recuentos de c), d) y e) con su guion | Hecho | `recuentos-vistos.txt` («165» en :5), `huecos-material.txt`, `recuento-compuerta.txt` |
> | 20 | P4: líneas del cierre sobre una copia; test_hoja_de_ruta y test_project_state; menos de 23.000 bytes | Hecho | `simular-cierre.txt:1-5` (a, b y c vacíos; 22.349 y 22.411 bytes) |
> | 21 | Cierre: F con el texto de la respuesta, R3.7 HECHA, R3.8, R5.6, segunda Regla viva | Hecho | `simular_cierre.py:73-148` |
> | 22 | Punto 11: la cifra sin los break even de los libros sin vídeo | Parcial (declarado, PARADA 2 punto 1) | informe §1.2 (:837-841) |
> | 23 | Punto 13: exposiciones antes de correr nada | Hecho de otra forma (declarado) | fila +103: (1) y (2) declarados después, el mismo día; desviación 4 |
> | 24 | Alcance: ninguna corrida del arnés ni cifra agregada nueva del bot | Hecho (en lo que el repo deja ver) | `grep -rln "CONJUNTO\|motor arnes"` en el anexo no da nada; las cifras del bot son recuentos sobre RESPALDO-M1 o del día sintético de 2030 (`volcados-main-rama.txt:10`) |
> | 25 | Alcance: ninguna cifra de umbral sale de la rama | Hecho | eje (a), última viñeta; los números de `medir_a16.py:42-43` son los del punto 7 |
> | 26 | Alcance: el motor no cambia | Hecho | el diff de engine/ solo toca `arnes.py` y `cableado.py`; `grep operaciones_trader\|\.criterio\b` en src/: solo `cableado.py:255,648,1269,1279` (salida); `volcados-main-rama.txt:2-4` da «igual a main» True ×3 hasta la sección nueva |
> | 27 | Alcance: todo día leído es de construcción y está declarado | Parcial | ver a2 (los 6 casos dev de mayo) |
> | 28 | Alcance: lo «visto» del §12 coincide con las salidas commiteadas | Parcial | ver b2 |
> | 29 | Informe con «El encargo, punto por punto», desviaciones, lo no medido y la fila de ERRORES-RECURRENTES | Hecho | :935, :986, :1007, :1016 |
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | b1 | bloquea (está declarado; se resuelve con la respuesta del consultor) | Falta la NOTA de PREREGISTRO.md que piden el punto 12 y la fase 1, punto 1. El motivo está bien medido: `test_puerta_holdout` exige «sigue vacio», y con el fichero cambiado sin commitear la puerta da «no esta commiteado tal como esta en el arbol». Como el sello es del árbol estadiado, ningún commit puede cambiar ese fichero con el test en verde. La rama no está lista hasta que el consultor conteste la PARADA 2. | `holdout.py:124-134` (`_commiteado_y_sin_cambios`) y `:156-158`; `test_puerta_holdout.py:34-39`; las 6 particiones salen de `holdout.py:57` (RESERVADAS); la PARADA 2 está en el informe, :1022-1059 |
> | b2 | importa | ADR-0092 §12 no declara un conjunto de salidas del bot sobre construcción que ya están commiteadas: las 20 páginas y trazas del visor de `anexos/VISOR-CONSTRUCCION/dias/`. Son DIAGNÓSTICO, con órdenes y operaciones del bot y del trader por día. Tampoco nombra los censos derivados (`RECORRIDA-CONSTRUCCION/costes-y-sesiones.txt`, `RESPALDO-M1/censo-respaldo.txt`). El grep de `CONJUNTO: construccion` no los ve porque no llevan esa línea. | `ls …/VISOR-CONSTRUCCION/dias/` da 20 de cada tipo: `pagina.txt`, `traza.txt`, `contexto.txt` y `ticks.txt`. La cabecera de `2026-01-08.pagina.txt:3-5` dice «DIAGNOSTICO-… · operaciones del trader 4, del bot 1». Las páginas entraron en el commit 304da27. La lista del ADR está en `0092-…md:244-258`. |
> | b3 | importa | En «Lo visto, declarado», el ADR cambia sin decirlo la letra que escribió el consultor. La respuesta, en L, dice «el criterio **e)** y la forma del remuestreo se parecen a lo que VIABILIDAD-TRADER hace»; el ADR dice «el criterio **c)** de §3». Puede ser una corrección razonable, pero toca la declaración de lo visto y no está entre las desviaciones. | `encargos/…:68` y `METODO-…md:639` («el criterio e)»), frente a `0092-…md:241` («el criterio c) de §3»); la lista de desviaciones (:986-1005) no lo menciona |
> | b4 | importa | El test que pedía el punto 10 («la salida existente no cambia byte a byte») compara la salida de la rama con la misma salida de la rama, quitando `_informe_metodo` por monkeypatch. Así no puede detectar un cambio de decisión, porque las dos salidas salen del mismo motor. La comparación con main está en un anexo, y su lado «rama» fue un clon de 56eb235 con los ficheros copiados (desviación 5), no el commit 47a526c. Que ninguna decisión lee los campos nuevos sí se ve en el código. | `test_metodo_adr0092.py:359-369`; `volcados-main-rama.txt`; desviación 5 (:996-999) |
> | b5 | menor | El riesgo al colocar se vuelve a escribir en línea, en vez de reutilizar el cálculo que ya existe. La respuesta pedía «no una fórmula nueva». La fórmula es la misma que la de `_margen_al_colocar` y el test la cuadra en el día sintético. | `cableado.py:1179`, frente a `primitivas_broker.py:573-578`; `test_metodo_adr0092.py:383` |
> | b6 | menor | La forma del remuestreo la eligió la rama: réplicas de len(días) días con reemplazo, incluidos los días sin operaciones; media agrupada; percentil `floor(p·(n−1)/100)`. Está en el informe §1.2, pero no en ADR-0092 §3, que es lo que pre-registra la puerta. | `criterio_fidelidad.py` (`percentil_por_dias`, docstring del diff :311-337); `METODO-…md:768-769`; `0092-…md:78-79` |
>
> Lo que el encargo dice que no se toca está intacto: `git diff --name-status main...HEAD` no trae `broker.py`, `llenado.py`, `cuenta.py`, `primitivas_broker.py`, `motor.py`, `knowledge/spec/`, `knowledge/cuentas/`, `knowledge/simulador/`, `knowledge/corpus/`, `strategy_spec.yaml`, `parametros.yaml`, `PREREGISTRO.md`, `cli.py`, `.claude/` ni el Makefile. Las ocho desviaciones declaradas cuadran con el código; la 7 se ve en `criterio_fidelidad.py:367-368` (`cargar_criterio` exige los campos) y la 8 en que `cli.py` no aparece en el diff.
>
> ### Lo que no pude comprobar
> - **El `make check` en curso.** Todavía no tiene la línea `SELLO` ni la de `PICO DE MEMORIA`, y no lo corrí. Por a1, espero que no selle.
> - **Los `make check` de los commits 1 a 3.** Sus logs ya no están. Que sellaron solo se infiere de que el hook dejó commitear.
> - **El fallo de `test_puerta_holdout` con la NOTA estadiada.** Reproducirlo exige escribir PREREGISTRO.md. El mecanismo lo verifiqué leyendo el código (b1).
> - **Que no hubo ninguna corrida del arnés fuera del repo.** Solo puedo ver que no hay ninguna salida commiteada nueva.
> - **La afirmación de que la guardia niega ejecutar en un clon un test que importa `tests.unit`** (desviación 5), y cuánto tardan 10.000 réplicas.
> - **Exposiciones de esta pasada del revisor, para que la sesión las declare el mismo día:**
>   - un `grep -l 'stop:'` y un `ls` contado por mes sobre `knowledge/cases/dev/`, que incluyen los 6 casos dev de mayo (permitido por ADR-0025 §4, sin imprimir fechas);
>   - 12 líneas de la cabecera de `VISOR-CONSTRUCCION/dias/2026-01-08.pagina.txt`, día de construcción;
>   - lectura de `recuentos-vistos.txt`, `recuento-compuerta.txt`, `huecos-material.txt`, `medir_a16.py`, la cabecera de `medir-a16.txt`, `volcados-main-rama.txt` y la cola de los dos `tests-*-con-main.txt`;
>   - `knowledge validate`, `state check`, `contrato_rama.py` y pytest de 12 ficheros sintéticos.
>   - Ninguna filtrada, cruda, fotograma, libro ni caso reservado; ningún listado de `knowledge/cases/holdout`.
>
> ### Comandos ejecutados
> 1. `git branch --show-current`, `git merge-base main HEAD`, `git log --format='%h %s' main..HEAD`, `git diff --stat main...HEAD`, `git status --short`, `git diff --cached --stat`
> 2. Read de `docs/encargos/trabajo-metodo-fidelidad-rentabilidad.md`, `contrato.yaml`, `METODO-FIDELIDAD-RENTABILIDAD.md:620-1066` y `docs/adr/0092-…md`
> 3. `uv run python scripts/contrato_rama.py`
> 4. `uv run botsito state check`
> 5. `uv run botsito knowledge validate 2>&1 | tail -15`
> 6. `git log --format='%h%n%B----' main..HEAD -- knowledge/spec knowledge/cases`; `git diff --name-status main...HEAD`; `git log --name-status main..HEAD`
> 7. Grep de `^## Estado` en los ADR 0092, 0043, 0070 y 0053 (el primer intento, encadenado con pytest, lo negó la guardia y lo partí en dos llamadas)
> 8. `uv run pytest -q -p no:cacheprovider` sobre 7 ficheros y después sobre 12 (lista en el eje a)
> 9. `git diff main...HEAD -- knowledge/cases/criterio_fidelidad.yaml`, `-- src/botsito/cases/criterio_fidelidad.py` (grep de números), `-- src/botsito/engine/arnes.py` y `-- src/botsito/engine/cableado.py`
> 10. Grep y Read en `engine/` (`_margen_al_colocar`, `_a_la_cuenta`, `por operacion del trader`, `por_operacion`), `cableado.py:425-484`, `primitivas_broker.py:540-600`, `arnes.py:395-444` y `cli.py:2410-2459`
> 11. `grep -n "^def test_"` en los dos tests nuevos; Read de `test_metodo_adr0092.py:150-408`
> 12. Read de `medir_a16.py`, `volcados-main-rama.txt`, el `README.md` del anexo, `recuentos-vistos.txt`, `recuento-compuerta.txt`, `huecos-material.txt`, `simular-cierre.txt` y `simular_cierre.py`; Grep de `mercado_de_construccion` en `simulacion.py`
> 13. `git diff main...HEAD -- docs/validation/HOLDOUT-EXPOSICIONES.md`
> 14. `grep -rlE '^(\[[^]]*\] )?CONJUNTO: construccion' docs/validation/`; `grep -rl 'CONJUNTO: construccion' docs/validation/`; `ls anexos/SELLO-RESPALDO-M1/`
> 15. `grep -rlE '^## Por sesion|…' docs/validation/ --include=*.txt`; `head -12` de `VISOR-CONSTRUCCION/dias/2026-01-08.pagina.txt`; `ls` de VISOR-CONSTRUCCION y de su carpeta `dias` contados por tipo; `ls docs/validation/anexos/`
> 16. `diff` de la respuesta en el encargo (:64-116) con la del informe (:635-687)
> 17. `grep` de «ids-inexistentes», «quemado por ADR-0043» y «criterio e)\|criterio c)»
> 18. `git diff main...HEAD` de los ADR 0043, 0053 y 0070, MASTER_PLAN y el README de los ADR; `git diff -U4` de MASTER_PLAN; `git diff` de PROJECT_STATE
> 19. Grep de A-18, A-31 y A-16 en `ambiguedades.yaml` (un `awk` lo negó la guardia; lo sustituí por Grep)
> 20. Read de `test_puerta_holdout.py:1-60`, `holdout.py:90-170` y Grep de RESERVADAS
> 21. `git status --porcelain=v1`, `git diff --cached --name-status` y `cat make-check.log | head -20`; Grep y Read de `sello_make_check.py` y de `contrato_rama.py`
> 22. Comprobación de citas: `sed -n` de `holdout.py:634`, del yaml del perfil, de `MASTER_PLAN.md:124` en la rama y en main, de `HISTORIA.md:4689`, de `cierres/…yaml:18-22` y de `docs/runbooks/DECISIONES-DE-PROCESO.md:29`
> 23. `ls knowledge/cases/dev/` contado por mes; `grep -l 'stop:' knowledge/cases/dev/*.yaml | wc -l`; `head -3 medir-a16.txt`
> 24. `ls data/manifests/`; `grep -i bid` en los manifiestos M1
> 25. `tail` de `tests-campos-con-main.txt` y de `tests-metodo-con-main.txt`
> 26. `git log -1 --format=%B` de 56eb235 y de 1b10082
> 27. `git diff main...HEAD` de los cinco documentos de solo añadir: líneas `-` = 0

### 8.1 Lo que se hizo con los hallazgos del revisor

| # | Gravedad | Qué se hizo |
|---|---|---|
| a1 | bloquea | Ya visto antes de que llegara: la guardia negó el `git add` del punto 4 (iba encadenado con `state check`), el `make check` arrancó sobre un árbol sin estadiar y lo paré. El punto 4 entra en el commit de este §8, con un `make check` nuevo y sellado (desviación 12) |
| a2 | importa | Arreglado: la frase de §1.2 dice ahora 75 ficheros, 69 de construcción con operaciones y 6 de mayo; y la lectura de esos 6 casos de mayo (solo un recuento) está declarada en una fila nueva del 2026-11-07 en HOLDOUT-EXPOSICIONES, con la del revisor |
| a3 | menor | Arreglado: `MASTER_PLAN.md:124` en `main` y `:132` en la rama |
| a4 | menor | Arreglado: la fila 26 dice que el punto 4 va con este §8 («Hecho de otra forma»), y la 46 apunta ya a un §8 que existe |
| a5 | menor | Arreglado en la fila de la fase 1: 69 días dev con operaciones, de los 76 |
| a6 | menor | Arreglado: M1 de 2026-01 y de 2026-03 a 2026-09, sin febrero |
| a7 | menor | Declarado como desviación 9; la clave no se carga |
| b1 | bloquea | Es la PARADA 2, punto 0, y la contesta el consultor: la rama no puede cambiar PREREGISTRO.md sin aflojar `test_puerta_holdout`, y eso no lo decide la sesión. Lo que el fichero tendrá que llevar está escrito en ADR-0092 §13 y en la NOTA de MASTER_PLAN |
| b2 | importa | Arreglado en ADR-0092 §12: entran las páginas, trazas, contextos y ticks del visor de los 20 días de `anexos/VISOR-CONSTRUCCION/dias/` y todo lo derivado de las corridas que está commiteado en sus anexos (patrones, censos, costes, listas de S-14, entradas antes de la alternancia, diffs de la línea base), con la forma en que se buscó |
| b3 | importa | Arreglado: el error era mío. La respuesta dice «el criterio e)», y e) es lo que VIABILIDAD-TRADER §3 comprueba con el trader (las reglas de FTMO, escenario a escenario). ADR-0092 §12 dice ya «el criterio e)», como en L |
| b4 | importa | Arreglado de dos formas. (1) La regresión se repitió con la rama COMMITEADA (`C:/cm/rf2`, 1b10082, sin copiar nada) frente a `main` (`C:/cm/mf2`): los mismos seis hashes, así que la copia de la primera vez era el código commiteado. (2) Los tres volcados de `main` quedan congelados en `tests/golden/informe_simulacion/`, y el test nuevo `test_lo_que_ya_salia_es_byte_a_byte_lo_de_main` exige que la salida de la rama empiece exactamente por ellos: compara con `main` y no consigo misma, y un cambio de decisión o de llenado en el día sintético lo rompería (desviación 11) |
| b5 | menor | Contestado, sin cambio: el riesgo de `_margen_al_colocar` se calcula dentro de un cierre de `primitivas_cableadas` (`primitivas_broker.py:558-582`), así que no se puede llamar desde fuera, y sacarlo a una función tocaría `primitivas_broker.py`, que el contrato protege. La fórmula es la misma y la cuadra `test_la_tabla_de_posiciones_cuadra_con_la_cuenta` |
| b6 | menor | Arreglado y llevado al consultor: la forma exacta del remuestreo está ya en ADR-0092 §3 c), dicha como lectura de la rama, y la PARADA 2, punto 2, le pide que la confirme (desviación 10) |

## Estado

FASE 1 HECHA (puntos 1 a 4) y revisada (§8), con la **PARADA 2 abierta** para el consultor: (0) la
NOTA de PREREGISTRO.md, que la rama no puede commitear sin aflojar `test_puerta_holdout`; (1)
dónde vive la lista de los libros sin vídeo del sesgo 3; (2) la confirmación de la forma del
remuestreo de ADR-0092 §3 c). Ninguna bloquea el método: el ADR, el yaml, las funciones, la salida
del arnés, A-16 y los recuentos están hechos y sellados. Sin CI por `fix/`: la rama no toca hooks,
rutas, `.claude/` ni plataforma.

Rama lista para revisión, NO cerrada.
