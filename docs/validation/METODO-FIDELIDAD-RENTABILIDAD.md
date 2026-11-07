# METODO-FIDELIDAD-RENTABILIDAD · el método con el que se juzga al bot (ADR-0092)

```ids-inexistentes
ADR-0092 — lo crea la fase 1 de esta rama; el bloque sale en el mismo commit que lo crea
```

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

## Estado

FASE 0 ENTREGADA. PARADA: espera la respuesta del consultor (umbrales y decisiones 0 a 13). Nada de
la fase 1 empieza antes.
