---
status: ACTIVE
date: 2026-09-25
phase: post-F14 (rama `trabajo/simulador-cuenta`)
---

# 0050 · El simulador: la capa de cuenta

## Decision

El simulador tiene dos mitades: el **bróker simulado**, que convierte las órdenes del motor en
operaciones con instantes, precios, lotes y costes (otra rama, junto con los ticks y el modelo de
llenado), y la **capa de cuenta**, que recibe esas operaciones y dice si la cuenta de la firma
**pasa o se suspende**. Este ADR fija la capa de cuenta. No depende del trader: todo lo que decide
sale del reglamento de la firma (`docs/validation/FTMO-REGLAS.md`, leído de fuente oficial el
2026-09-25) y de las decisiones del consultor de ese mismo día.

### 1. Las cuatro decisiones del consultor, escritas

Del 2026-09-25, recogidas en `PROJECT_STATE.md` (Next Action 26) sobre las preguntas de
`FTMO-REGLAS.md` §4 «para el consultor»:

- **(a) Se modelan los objetivos de beneficio y los días mínimos de cada fase** (R1, R4), de modo
  que una serie de operaciones diga si una fase se SUPERA, y no solo si se pierde la cuenta.
- **(b) La comisión y los swaps van DENTRO de la equity que vigila la firma** (R2: «Balance + Open
  Positions P/L ± Swaps – Commissions»). La capa de cuenta recibe los costes como CARGOS con
  instante y los descuenta del saldo en ese instante; el importe lo calcula el bróker simulado.
- **(c) El volumen máximo y los límites de órdenes y posiciones entran como `firma_*`** dentro de un
  perfil de cuenta (R11, R13): `firma_volumen_max_lotes`, `firma_ordenes_simultaneas_max`,
  `firma_posiciones_dia_max`, junto a `firma_mensajes_dia_max`. Los consume el bróker simulado.
- **(d) Hay una guardia de AVISO por incoherencia del tamaño de posición** (R17). Solo avisa: nunca
  cambia el estado de la cuenta.

### 2. Lo que ADR-0049 dejó escrito y aquí se cumple

- **H6: la capa de cuenta PERSISTE entre días dentro del simulador**, mientras la estrategia empieza
  cada día de cero. Una ejecución de la capa de cuenta cubre TODA la fase: el saldo del corte de
  cada medianoche es el saldo con el que terminó el día anterior, el límite total no se reinicia
  nunca y los días de trading se acumulan. La capa de cuenta no toca ningún estado de estrategia.
- **H4: el gate DESCONOCIDO sigue estricto.** Esta capa no enchufa nada al motor de estrategia: los
  diez gates que hoy prohíben `abrir_operacion` siguen prohibiendo hasta que el bróker y el cableado
  los hagan evaluables. Sin ticks, el camino intravela será pesimista por OHLC de M1; con ticks, el
  orden real: el bróker producirá las MARCAS de precio de cada operación y la capa de cuenta las
  evalúa sin saber de dónde salen.

### 3. Tres capas, y una firma nueva es un fichero nuevo

**Estrategia, instrumento y perfil de cuenta son capas separadas.** La estrategia vive en la spec y
en `parametros.yaml`; el instrumento en su ficha (`instrumento_*`, A-27); y **el perfil de cuenta es
UN fichero en `knowledge/cuentas/`** —UNA firma, UN programa, UN tipo de cuenta y UN capital— con el
FORMATO DEL REGISTRO (ADR-0002, ADR-0012) y leído por `config.registro.cargar_registro`: la misma
puerta, los mismos tipos y los mismos tres estados. Una firma nueva es un perfil nuevo en
configuración, **nunca código nuevo**: el motor de cuenta no contiene ninguna cifra ni ningún nombre
de firma (`test_no_business_literals`), y un perfil INVENTADO en `tests/fixtures/cuentas/` lo
demuestra corriendo la misma secuencia con otro capital, otro reloj, otra magnitud vigilada y otro
límite total.

Lo que un fichero tiene que declarar para ser un perfil (`engine/perfil_cuenta.py`): solo
parámetros `prop_firm`; `firma_huso_corte`, el reloj con el que la firma corta el día;
`firma_fases`, en orden; y por cada fase `firma_<fase>_objetivo_aplica`, `firma_<fase>_objetivo`,
`firma_<fase>_dias_minimos_aplica` y `firma_<fase>_dias_minimos`. Un booleano dice si la regla
aplica y, cuando no aplica, el umbral se queda `UNKNOWN` (ADR-0012 §2).

**Cada cifra cita su regla de `FTMO-REGLAS.md` (R1..R20)** en su descripción, y un test comprueba
que la regla citada existe. **Lo que la fuente oficial no dice va en `UNKNOWN`**: leerlo falla
nombrando el parámetro y el perfil, y **el simulador se niega a correr si lo necesita para
DECIDIR**. En el perfil de FTMO quedan sin valor `firma_comision_por_lado` (R12: si los 5 USD por
lote son por lado o por operación completa, NO ENCONTRADA), `firma_tamano_posicion_ratio_aviso`
(R17: «substantially larger» no tiene cifra; Next Action 27), y el objetivo y los días mínimos de
la fondeada, que por R1 y R4 no existen.

**Un nombre que coincide con `parametros.yaml` lleva el mismo valor, y un test lo cruza**
(precedente: ADR-0012 §1, que cruzó el kit con el registro). Es una duplicación DECLARADA y
vigilada: la spec sigue leyendo `parametros.yaml` y el perfil lo lee solo el simulador. Fundirlos
—que RN-029 a RN-032 lean del perfil— toca la spec y queda para el consultor.

**El reloj de corte.** `firma_huso_corte` vale `Europe/Prague` (R2, R4: «00:00 CE(S)T»). ADR-0027
descartó un `firma_huso_corte` para la SPEC porque sería «dos puertas para el mismo instante» que
`huso_operativa`; aquí el reloj es una propiedad de la FIRMA y vive en su perfil, porque otra firma
puede cortar en Nueva York, y **un test afirma que hoy da los mismos instantes que `huso_operativa`
en las 365 medianoches de un año, con sus dos cambios de hora**. Si algún día divergen, ese test es
el aviso que ADR-0027 §alt. 3 pedía.

### 4. La capa de cuenta: funciones puras

`engine/cuenta.py`. `reglas_de_fase(perfil, fase)` lee del perfil todo lo que UNA fase necesita
—y ahí es donde se niega si falta un valor— y `evaluar_fase(operaciones, reglas, contrato)` corre
la fase desde el capital inicial. Sin IO, sin reloj de pared, sin bróker. Lo que lleva:

1. **Saldo y equity.** El saldo cambia al cerrar (P/L realizado) y con cada cargo; la equity es el
   saldo más el P/L flotante de lo abierto a su último precio observado (apertura, marcas, cierre).
   El P/L se calcula sobre precios y lotes con el tamaño del contrato como ARGUMENTO, en la moneda
   de cotización, que se trata como moneda de la cuenta: la conversión cruzada es del bróker.
2. **El día de la firma**, en `firma_huso_corte`: un corte a cada medianoche local, ANTES de
   cualquier evento de ese instante, que fija el saldo del corte. El primer día usa el capital
   inicial (R2). Un día de trading es un día local en el que se ABRE una posición (R4), y los días
   no tienen que ser consecutivos.
3. **La pérdida diaria**: la magnitud vigilada no puede caer POR DEBAJO de
   `saldo_corte − firma_perdida_diaria_max % del capital inicial` (o del capital, si
   `firma_base_perdida_diaria` lo dice). **Estrictamente por debajo**: R18 dice «drops below», así
   que quedarse EN el límite no infringe.
4. **La pérdida total**: estática sobre el capital inicial (R3) o, si `firma_perdida_total_arrastra`
   lo declara, sobre el saldo máximo alcanzado.
5. **El objetivo y los días mínimos**: la fase se SUPERA en el primer cierre que deja el saldo en
   el objetivo o por encima (R1: «exceeds [...] by the required Profit Target»; el ejemplo oficial
   es 110.000, y llegar a 110.000 cuenta), **sin posiciones vivas** («with all positions closed») y
   con los días de trading cumplidos. Una fase sin objetivo (la fondeada) nunca se supera: sigue
   EN_CURSO.
6. **El estado final**: `EN_CURSO`, `SUPERADA` o `SUSPENDIDA`, con el motivo y el instante EXACTOS
   del evento que lo decide. La primera suspensión o superación es TERMINAL: cada fase de FTMO es
   una cuenta nueva, así que lo que venga después no se evalúa y se cuenta aparte.
7. **La guardia de tamaño de posición** (R17): aviso por una operación cuyo lote supera
   `firma_tamano_posicion_ratio_aviso` veces la mediana de los lotes de LAS DEMÁS. **Sin cifra en
   el perfil no se evalúa, y el resultado lo dice nombrando el parámetro**; no bloquea la ejecución
   porque no decide nada sobre la cuenta, y FTMO no la cuantifica. Si el consultor prefiere que la
   ausencia de cifra impida correr, es cambiar una línea; se deja escrito aquí para que no pase por
   silencio.

Convenios menores, declarados para que no parezcan accidentes: a igual instante, un cierre se
procesa antes que un cargo, una marca o una apertura; el orden de entrada de las operaciones no
importa (la línea de tiempo se ordena por instante e id); las magnitudes son `Decimal`.

**El margen de ADR-0031 NO está aquí.** `firma_margen_seguridad` es un freno de la ESTRATEGIA
(RN-029 a RN-032: frenar antes del límite); la capa de cuenta modela LA FIRMA, que suspende en el
límite. Es lo que permite medir, más adelante, cuántas veces el freno habría evitado la suspensión.

### 5. Cómo se conecta con la spec, y qué queda pendiente

La spec declara dos acumuladores de la firma (`strategy_spec.yaml`): `perdida_dia_firma` —«caída
de la magnitud vigilada (equity) por debajo del saldo al corte diario», base
`firma_base_perdida_diaria`, reinicia con `reloj_dia_riesgo`— y `perdida_total_firma` —«por debajo
del capital inicial», base `saldo_inicial_cuenta`, reinicia `nunca`, `arrastra:
firma_perdida_total_arrastra`—. Los leen `se_acerca_al_limite {acumulador, tope, margen}` (RN-029,
RN-030, RN-031) y `no_cabe_la_operacion {acumulador, tope, margen, riesgo, sobre}` (RN-032), las
cuatro primitivas de acumulador que ADR-0031 dejó para el motor.

**Esta capa es quien puede alimentarlos**, porque lleva en cada instante exactamente sus dos bases
y su magnitud: `perdida_dia_firma = saldo_corte − vigilada` y `perdida_total_firma = base_total −
vigilada` (capital inicial, o saldo máximo si arrastra). **En esta rama NO se enchufa al motor**: el
cableado va con el bróker, porque sin operaciones no hay nada que acumular. Lo que el cableado
tendrá que decidir, y aquí se describe sin inventarlo:

- **La forma incremental.** Hoy `evaluar_fase` recorre una secuencia completa; el motor necesita el
  estado de la cuenta ANTES de cada decisión (los gates se evalúan antes de abrir). El estado
  interno ya avanza evento a evento; hay que exponerlo como `avanzar(estado, evento)` y que el
  bróker emita los eventos (apertura, marca, cargo, cierre).
- **El signo y el recorte del acumulador.** La spec dice «caída»: no dice si un acumulador con la
  equity POR ENCIMA de su base vale cero o negativo. Con `se_acerca_al_limite` da igual —un valor
  negativo nunca alcanza `tope − margen`—, pero con `no_cabe_la_operacion` no: sumar el riesgo a un
  acumulador negativo (holgura ganada en el día) es más permisivo que sumarlo a cero. **Pendiente
  de la spec o de ADR-0031**; aquí no se elige.
- **La comparación.** `alcanza_tope` y `se_acerca_al_limite` dicen «llega a»; la firma infringe
  «por debajo». Son lecturas distintas a propósito (la estrategia frena ANTES), y el cableado tiene
  que conservar las dos: mayor o igual para el freno, estrictamente por debajo para la firma.
- **El reloj.** El acumulador diario de la spec reinicia con `reloj_dia_riesgo` (`civil_operativa`,
  ADR-0027); la capa de cuenta corta con `firma_huso_corte`. Hoy coinciden y un test lo afirma; el
  cableado debe leer UNO de los dos y declararlo.
- **La fase de riesgo por tick** (ADR-0028): con OHLC de M1, las marcas serán pesimistas (ADR-0049
  H4); con ticks, reales. La capa de cuenta no cambia.

## Problema que resuelve

Sin bróker simulado el motor no puede producir ninguna operación (ADR-0048 H4), y sin capa de
cuenta, aunque las produjera, nadie diría si la cuenta de FTMO sobrevive a ellas ni si una fase se
pasa. Las cuatro decisiones del consultor del 2026-09-25 estaban en `PROJECT_STATE.md` y en ningún
ADR, en ningún registro y en ninguna spec (Next Action 26 lo dice así). Y las cifras de FTMO que
`FTMO-REGLAS.md` trajo con fuente —objetivos, días mínimos, costes, volumen, límites del servidor—
no tenían dónde vivir: `parametros.yaml` es de la spec y tocarlo arrastra documentos generados,
trailers y guardias que no tienen nada que ver con una firma.

## Alternativas consideradas

1. **Un perfil en `knowledge/cuentas/` con el formato del registro, leído por la misma puerta;
   capa de cuenta como funciones puras sobre una línea de tiempo; sin cablear** (elegida).
2. **Meter las cifras nuevas en `parametros.yaml`** y que la capa de cuenta lea el registro de la
   spec.
3. **Un formato propio de perfil** (otro esquema YAML, otro cargador) con las citas a R1..R20 como
   campo estructurado.
4. **Capa de cuenta incremental desde el principio**, expuesta como máquina de estados para el
   motor, y cablear RN-029 a RN-032 en esta misma rama.
5. **Que la guardia de tamaño sin cifra impida correr**, como cualquier otro parámetro sin valor.

## Por que elegimos esta opcion

- **La misma puerta, sin tocar la spec.** El cargador del registro ya sabe de tipos, estados,
  rangos, enums y fuentes; un perfil reutiliza todo eso y añade solo lo que un perfil exige. Los
  tres estados de ADR-0012 bastan: `UNKNOWN` ya significa «leerlo falla», que es lo que el brief
  pide para un NO ENCONTRADA.
- **La firma es configuración.** Con el motor sin cifras y sin nombres, el perfil sintético
  demuestra que cambiar de firma es cambiar un fichero, que es lo que ADR-0048 §6 ya decía del
  instrumento y del perfil de cuenta.
- **Funciones puras sobre una secuencia cerrada** son lo que se puede medir hoy con tests exactos:
  el instante de la suspensión, los cortes de los cambios de hora, la equity flotante. La forma
  incremental se construye encima cuando exista el bróker, no antes.

## Por que descartamos las demas

- **(2)** Cada parámetro nuevo en `parametros.yaml` obliga a `spec docs --escribir`, al trailer
  `Fuente:` y a `comprobar_consumo`, y el brief de esta rama prohíbe tocar la spec. Y mezcla capas:
  una cifra de FTMO no es un parámetro de la estrategia.
- **(3)** Un segundo esquema es una segunda puerta (ADR-0002, «dos puertas para el mismo valor»),
  con sus propios errores y sin las guardias que el registro ya tiene. La cita a R1..R20 va en la
  descripción y un test la comprueba: cumple lo mismo sin otro formato.
- **(4)** Cablear sin bróker es cablear contra nada: no hay operaciones, así que el estado
  incremental no se puede medir, y los huecos de §5 (signo del acumulador, reloj) habría que
  inventarlos. ADR-0049 H4 los deja para el ADR del simulador CON el bróker.
- **(5)** La guardia no decide nada sobre la cuenta y FTMO no da cifra: negarse a correr por ella
  dejaría el perfil real de FTMO inutilizable hasta que Aleks pregunte (Next Action 27), y a cambio
  no protegería de nada. Se deja NO EVALUABLE y dicho.

## Impacto

- **`knowledge/cuentas/`** (carpeta nueva, con README): `ftmo-2step-swing-100k.yaml`, el perfil
  de FTMO, cada cifra con su regla R1..R20 y cuatro parámetros sin valor.
- **`src/botsito/engine/perfil_cuenta.py`**: `cargar_perfil`, `PerfilCuenta`, los accesores que
  convierten un `UNKNOWN` en `ParametroSinValorError` con nombre, y las guardias de lo que un perfil
  tiene que declarar.
- **`src/botsito/engine/cuenta.py`**: `Operacion`, `Marca`, `Cargo`, `ReglasFase`,
  `reglas_de_fase`, `evaluar_fase`, `guardia_tamano_posicion` y `ResultadoFase`.
- **`tests/fixtures/cuentas/sintetica-una-fase-50k.yaml`**: el perfil inventado.
- **Tests**: `tests/unit/test_perfil_cuenta.py` y `tests/unit/test_cuenta.py`, con los nueve casos
  que pidió el brief y el contrato de accesores del perfil.
- **Sin tocar**: `knowledge/spec/`, `ambiguedades.yaml`, el motor de estrategia, el arnés y su
  línea base.
- **Lo que queda con dueño**: el bróker simulado, los ticks y el modelo de llenado (Next Action
  32); el cableado de §5, con el bróker; la medición de `firma_comision_por_lado` en la plataforma
  y la pregunta a FTMO por R17 (Next Action 27); fundir el perfil con `parametros.yaml`, si el
  consultor lo quiere; y un tipo `lista` del registro para `firma_fases`, hoy texto.

## Fecha / fase

2026-09-25 · post-F14, rama `trabajo/simulador-cuenta`. Decisiones del consultor del 2026-09-25
(Next Action 26); Next Action 31.

## Estado

ACTIVE
