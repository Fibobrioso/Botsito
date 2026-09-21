# F14a · La ingesta del detalle por operación

Rama `feature/F14a-ingesta-del-detalle`, desde `a791f92`. Sin tocar main, sin merge, sin tag, sin
push. **`PREREGISTRO.md` intacto** (blob `52649183dcdc55f136d88675feaa7c43459b5277`, con su marca
`SIN RELLENAR`); **cero ficheros `AUTORIZACION-*.md` en el árbol**; **ninguna partición reservada
abierta**. Sin tocar `evidence/`, `feedback/`, ni los repartos y anclas ya commiteados. De
`knowledge/spec/` se toca **una sola cosa, y en el segundo commit**: la nota medida de A-18 en
`ambiguedades.yaml` (§4), que no cambia su `estado`, ni su `decision`, ni su lista de `evidencia`,
y cuyo commit lleva trailer `Fuente:`. `kit check` sigue dando salida **idéntica** a la línea base
después de escribirla.

Lo que el brief llamaba «abrir cuatro días» resultó ser **escribir F14a entera**: no había ingesta
—cero `xlsx`, `openpyxl` o `pandas` en `src/`— ni forma de caso —`find knowledge -name 'caso-*'`
vacío—. Y antes de nada había que corregir una regla que prohibía el paso.

## 1. La línea base

`kit check --sesion 2026-09-09-sesion-01` guardado antes de tocar nada, y vuelto a ejecutar al
final: **idéntico**. `make check` a fichero (nunca a `/dev/null`) al abrir la rama: verde.

## 2. Lo primero no era código: `CLAUDE.md` §3 prohibía el paso

`CLAUDE.md` §3 prohibía «el detalle por operación de los xlsx del corpus» **en bloque, sin
distinguir días**. Los dos documentos que mandan ya eran granulares:

- ADR-0021 §1: «el detalle por operación del backtest del trader **en esos días**» (2026-09-12);
- ADR-0025 §4: «se puede abrir para esos 6 días `dev`, y sólo para ellos».

Tomado al pie de la letra, `CLAUDE.md` prohibía F14a entera. **Tercera vez** que este fichero
resulta ser más estricto que ADR-0021 sin que ningún ADR lo diga, y las tres veces bloqueó un paso
que el propio proceso exige. La caja de «por qué cambió esta regla» queda escrita en §3, y la regla
de la regla —una prohibición escrita ahí que no salga de un ADR se revisa antes de aplicarla— ya
estaba y se reafirma.

Pero **relajar el saco entero habría cambiado un problema por una fuga**: se abriría el resumen del
mes con los 10 días de `fidelidad-1` dentro. De ahí ADR-0037: **el criterio es la granularidad del
dato, no el tipo de fichero**, que da resultados **opuestos dentro del mismo libro** —las filas de un
día `dev` se leen; una pestaña de totales no, aunque esté al lado—.

**Orden ejecutado, y no al revés**: corregir `CLAUDE.md` §3 → escribir ADR-0037 → y sólo entonces
abrir agosto. Declarado el mismo día en `docs/validation/HOLDOUT-EXPOSICIONES.md`, fila 2026-09-21,
con la comprobación de que agosto no tiene **ni un día** en ninguna partición, hecha **antes** de
abrir con `casos_reservados(repo)` y no supuesta.

## 3. Lo que se construyó

### `src/botsito/corpus/libro.py` — el lector único

Stdlib pura (`zipfile` + `xml.etree`): `pandas` está prohibido por dos contratos y `openpyxl` no
está instalado. Lo define por lo que **no** hace:

1. **No enumera.** Selecciona la pestaña por la lista pre-declarada; no recorre las demás. Si falta,
   el error nombra **la esperada**, nunca las que sí hay.
2. **No publica el conjunto de fechas.** Recibe los días que quiere y devuelve sus filas. Una fila
   de otro día se descarta sin contarse y sin acumularse. Un `«14 días en el libro»` publicaría qué
   días reservados **no** operó el trader, y un día laborable sin operaciones **es su etiqueta**
   —está medido: por eso `2026-05-14` quedó quemado el 2026-09-12—.
3. **No decide qué días puede leer.** Eso es de quien llama, contra `casos_reservados`. La puerta
   está antes; esto es el lector.

Y un **contrato por grep** lo ata: `test_solo_un_modulo_puede_nombrar_el_libro_del_trader`, patrón
`\.xlsx|backtesting-analytics|openpyxl`, mismo patrón que
`test_solo_la_puerta_nombra_la_carpeta_del_holdout`. Sustituye al refuerzo que
`SEPTIEMBRE-ENTRA.md` apoyaba en que las dependencias fueran sólo `pyyaml` y `tzdata` —«ninguna ruta
de código puede leer el libro»—: **ese párrafo murió con F14a**, porque un lector de stdlib también
lee, y su sustituto entra en el mismo commit.

### `src/botsito/cases/ingesta.py` — los días se DERIVAN, no se eligen

No hay `--dias`, ni `--mes`, ni `--desde`. El conjunto es

    días pedidos  =  (casos en un reparto COMMITEADO)  −  casos_reservados(repo)

y un humano no puede ampliarlo. Tres negativas duras: un día que no esté en ningún reparto **aborta
el comando entero** (así no se puede ingerir un mes antes de su sorteo); un día reservado se
descarta **sin escribirse y sin nombrarse en la salida**; y si un reparto no se puede leer,
`casos_reservados` lanza y el comando falla —un mapa a medias es indistinguible de uno completo—.

El reparto tiene que estar **commiteado**, mismo criterio que `problemas_de_anterioridad`: si no,
un `particiones.yaml` sin commitear podría marcar un día como `dev` y hacerlo ingerible.

### `src/botsito/cases/biblioteca.py` — la forma del caso, y la guardia de los precios

Un caso es **un día**, y su id ya existía (`ventanas.id_caso` da `caso-<símbolo>-<día>`): esto no
inventa identidad, le pone cuerpo a un esqueleto que ya estaba en el reparto.

**Es la primera vez que hay PRECIOS bajo `knowledge/cases/`.** Por eso la guardia de ADR-0037 §9:
`problemas_de_biblioteca` afirma que ningún fichero de `knowledge/cases/dev/` corresponde a un caso
reservado, corre dentro de `knowledge validate` **siempre y sin `data/`**, y hay un test de contrato
que la ve fallar. El disparador que ADR-0033 dejó escrito —«el día que exista bajo
`knowledge/cases/<camino>/` un fichero con una etiqueta, un PRECIO o el detalle por operación de un
día asignado a una partición reservada, ese camino necesita lector guardado»— **no se cumple hoy**
porque sólo hay días `dev`; lo que faltaba era el mecanismo que garantice que siga sin cumplirse
mañana, y es éste.

### `botsito casos ingerir | check`

`ingerir --material --fecha` escribe los casos y **cuenta por RECUENTO, nunca por fechas**, como las
líneas `LECTURA:` de ADR-0033: `«N casos escritos de M días ingeribles; K filas leídas; 0 pestañas de
agregado abiertas»`. Esa salida puede acabar delante de cualquiera.

## 4. Lo que se midió en vez de suponerse, y es lo que más vale de la rama

Se abrió **agosto** —material de desarrollo, cero días reservados— para aprender el formato. Y salió
que **ninguna columna del libro es el objetivo planeado.**

### El invariante geométrico, que estaba puesto como higiene

Se escribió como guardia permanente contra un intercambio de columnas: para `buy`, el stop por
debajo de la entrada; para `sell`, por encima. Aplicado a las tres columnas candidatas:

```
idealTP:   del lado correcto 43, del lado MALO 4, sin valor  0
maxTP:     del lado correcto 20, del lado MALO 0, sin valor 27
initialSL: del lado correcto 42, del lado MALO 0, sin valor  5
```

- **`maxTP` se cae**: está relleno **si y sólo si la operación ganó** —20 filas con `maxTP`, las 20
  con `rPnL > 0`; 27 sin `maxTP`, ninguna con `rPnL > 0` (22 en pérdida, 5 a cero)—. Un objetivo
  *planeado* no puede faltar precisamente cuando se pierde: `maxTP` es «lo más lejos que llegó a
  favor», un resultado.
- **`idealTP` se cae** porque en **4 de 47 filas está del lado de la pérdida** —entre la entrada y el
  stop, las cuatro `sell` perdedoras— y su RR implícito no tiene estructura
  (0,2 · 0,1 · −0,2 · 2,1 · 1,1 · 56,6).

**La lección, y va literal.** El invariante geométrico se puso como test permanente de higiene, **no
como discriminador**, y acabó siendo el que contestó la pregunta que tres cruces diseñados a
propósito no vieron. Los tres cruces —presencia contra resultado, RR calculado contra RR declarado,
recuento de valores distintos— miraban **correlaciones**; el invariante miraba **si el número podía
ser lo que se decía que era**. Una comprobación de sentido puesta por higiene vale más que un cruce
diseñado, porque no sabe qué está buscando.

### Los cuatro cruces sobre el RR

| Cruce | Qué se midió | Resultado | Qué decide |
|---|---|---|---|
| RR declarado vs. `maxTP` | ¿Las columnas de RR se calculan desde `maxTP`? | **18/18 cuadran** a dos decimales | Las columnas de RR son métricas de **resultado**, misma familia que `maxTP` |
| RR declarado vs. `idealTP` | Lo mismo desde `idealTP` | **3 de 42** | `idealTP` no alimenta el RR del fichero |
| `avgRiskReward` repetido | ¿Es un promedio agregado clonado por fila? | **16 valores distintos en 42 filas**; `maxRiskReward`, 15 en 47 | **Es por operación.** El motivo mecánico que se había supuesto para descartar la reconstrucción era FALSO; el de fondo basta |
| Suelo del RR implícito de `maxTP` | ¿Hay suelo en 3,0? | **17 de 18 en 3,00 o por encima**, tres clavadas en 3,00, un único 2,50 | Huella mecánica de la regla, independiente de la cita |

Y que **15 de 18 se pasen** de 3,00 es evidencia de que el TP **no** es una orden límite colocada en
3R exacto: una orden límite habría cerrado ahí y el recorrido máximo no podría superarlo.

### El suelo en 3,00 mide algo que nadie había medido: es la primera medida de A-18

La medida del suelo **no es del objetivo planeado**: es del **RR REALIZADO**, calculado sobre la
distancia entrada-stop. Y esa distinción, que parecía contabilidad, es exactamente lo que A-18
lleva abierta desde F11. Los tres parámetros, en la spec de HEAD:

| Parámetro | Valor | Estado | Fuente |
|---|---|---|---|
| `objetivo_rr` | `3` | CONFIRMED | `fb-2026-09-09-sesion-01-7fbbb2e7` |
| `base_calculo_objetivo` | `caja_completa` | CONFIRMED | `ev-v2-003256-0197f4e1` |
| `stop_fraccion_caja` | `0.8` | CONFIRMED | `fb-2026-09-09-sesion-01-d34a0222` |

Y `knowledge/spec/strategy_spec.yaml:1063` ya lo avisaba, sin que nadie lo hubiera contrastado con
material: *«El RR REALIZADO sigue siendo `objetivo_rr / stop_fraccion_caja`, no `objetivo_rr`
[…] Quien mida fidelidad en F26 no debe leer esa diferencia como un fallo del bot: es la
mecánica.»* A-18 —*base sobre la que se mide el objetivo 1:3*, ABIERTA, `resuelve_en: [F11, F26]`—
es justo esa pregunta, y **las dos lecturas predicen cosas distintas y medibles**:

```
base = caja_completa  ->  RR sobre entrada-stop = objetivo_rr / stop_fraccion_caja = 3 / 0,8 = 3,75
base = riesgo_real    ->  RR sobre entrada-stop = objetivo_rr                      =         3,00
```

**Lo medido en agosto**, sobre las 18 filas que tienen `maxTP` e `initialSL` a la vez (de las 20
con `maxTP`: dos de ellas no tienen stop):

```
2,50 · 3,00 · 3,00 · 3,00 · 3,05 · 3,06 · 3,12 · 3,22 · 3,25
3,25 · 3,29 · 3,29 · 3,33 · 3,43 · 3,46 · 3,54 · 3,75 · 5,33

mínimo 2,50   ·   máximo 5,33   ·   tres clavadas en 3,00
>= 3,00:  17 de 18          >= 3,75:  2 de 18  (una exactamente 3,75, y un 5,33)
```

**Corrección de un número del brief.** El brief decía «todos por debajo de 3,75»; no lo son. **Son
16 de 18**, porque hay un 3,75 exacto y un 5,33. No cambia la conclusión —cambia su fuerza, y hacia
arriba: un suelo **en** 3,00 con tres filas clavadas ahí es la firma de un objetivo en 3R
sobrepasado por el recorrido, no la de un objetivo en 3,75R al que 16 de 18 ganadoras no llegaron.

**Lo que esto dice, y es un hallazgo sobre parámetros CONFIRMED.** La combinación de hoy
—`caja_completa` **con** el stop a `0,8`— **no cuadra con el material**. O la base es `riesgo_real`,
o el stop del trader en su backtest no está a 0,8 de la caja. Las dos posibilidades tocan un
parámetro CONFIRMED.

**Y A-18 NO se decide hoy, con el motivo escrito.** Es **un** mes y son **18 filas**. Y sobre todo:
**la caja no está en el fichero**. El RR que se mide es riesgo real *por construcción*, así que si
el stop del trader viviera en el borde de la caja (`stop_fraccion_caja` = 1) las dos lecturas
coincidirían y la medida **no discriminaría**. Lo que sí hay es **la primera medida que A-18 ha
tenido nunca**, y apunta al mismo lado al que `ev-v4-011951-5fb49e03` ya empujaba —el trader dice
que un ganador cubre «2 o 3» perdidas, que cuadra mejor con medir sobre el riesgo real—. A-18 gana
la nota en `knowledge/spec/ambiguedades.yaml`; su estado, su `decision` y su lista de `evidencia`
**no se tocan**.

**Se repite sobre mayo**, en `trabajo/mayo-dev-ingerido`. Dos meses que coincidan mueven esto de
«una medida» a «un hecho», y entonces sí toca decidir.

**Una trampa medida al escribir esa nota**, que se lleva a `CLAUDE.md`: tocar el **texto** de una
ambigüedad —no su `estado`, no su `decision`— deja `make check` en rojo con
`test_lo_commiteado_es_lo_que_sale_de_la_fuente`, porque `docs/spec/ambiguedades.md` es GENERADO y
va commiteado. Hay que pasar `botsito spec docs --escribir` en el **mismo** commit. La regla de la
casa decía qué sitios toca *abrir* y *cerrar* una ambigüedad, y no contemplaba **editarla**.

### Lo que sí es el objetivo, y lo contestó el corpus

Una **REGLA**, no una columna: `objetivo_rr` con su `base_calculo_objetivo`, que la spec ya tenía.
Cita literal del trader, `ev-v2-001658-d02fb71a` (v2 0:16:58), «el ratio de riesgo-beneficio de 1 a
3» como mínimo, y «como objetivo fijo» en v1 0:04:14. **El xlsx simplemente no registra el objetivo
planeado.**

**Por eso el caso NO lleva campo `objetivo`**, y no es que lo lleve vacío: un campo opcional vacío es
una invitación a que dentro de seis meses alguien lo rellene con `maxTP`. **Quitar el campo es el
mecanismo**; un comentario no lo es. Y `problemas_de_biblioteca` rechaza un documento que nombre
`maxTP` o `idealTP`.

### El instante viene en UTC, y eso sostiene la sesión H4

`dateStart` es texto sin huso (`2026/08/03 06:03:05`). Interpretado como **UTC** y llevado a
`huso_operativa`, **las 47 operaciones de agosto caen dentro de las dos sesiones declaradas** (25 en
`07-11`, 22 en `11-15`, cero fuera); leído como hora local de Madrid, **16 de 47 quedarían fuera de
toda sesión**. La ingesta convierte desde UTC y lo declara.

### Dos propiedades del material que no se corrigen ni se descartan

- **4 de 47 filas tienen `idealTP` entre la entrada y el stop.** No es un error del fichero: es cómo
  viene.
- **5 de 47 filas no tienen `initialSL`.** Una fila sin stop **no produce caso**, y no se cae en
  silencio: se cuenta y se dice con su motivo en la salida. Un caso que desaparece sin constancia es
  el defecto que a la sesión 1 le costó dos días —`2026-05-25` y `2026-06-29`— y que sólo delata un
  contador.

## 5. La pasada por el corpus, que no era opcional, y lo que cambió

Se hizo antes de redactar nada como ambigüedad, y **el corpus contestó DOS veces lo que estaba a
punto de irse al trader**:

- **El objetivo**: `ev-v2-001658-d02fb71a`. No hacía falta preguntar.
- **Los parciales**: `ev-v1-002313-6342a154` y `ev-v2-001819-60a1b0f1`, y sobre todo la sesión 1 en
  cámara, **v6 0:17:07**: *«espero a que llegue al 1.3, no digo, oh, está en 2 y cierro parciales,
  no, o sea, objetivamente ahora trabajamos, o sea, sin toma de parciales y que tiene que llegar al
  ratio 1.3 sí o sí»* (el ASR escribe `1.3` donde el trader dice 1:3). Es el propio trader, en la
  sesión de elicitación, diciendo que hoy **no** toma parciales.

Se descartó v2 0:46:26 como cita: habla del **bot**, no de lo que el trader hace.

**La regla que sale de aquí, y va a deuda con condición fechada**: buscar en el corpus **antes** de
redactar cualquier ambigüedad, y **escribir qué términos se buscaron**. Una pregunta al trader cuesta
un hueco de sesión; una búsqueda en el corpus no cuesta nada. La forma mecánica sería un campo en
`ambiguedades.yaml` que obligue a declarar los términos buscados, y **no entra en esta rama** porque
es cambio de esquema: condición fechada, la siguiente ambigüedad que se abra.

**A-33 no se abre.** La pasada acotada la contestó, y no cambió la forma del caso.

## 6. Una corrección que me toca a mí

ADR-0037 se commiteó (`a791f92`) **afirmando en su decisión 7 que el objetivo es `idealTP`**. Es
falso, y se midió media hora después al probar el lector. La corrección va **dentro del propio ADR**,
en caja, con fecha y con los números, y no se reescribe el cuerpo: el error queda visible.

Peor que el error: **antes de la corrección se escribieron DOS consecuencias para F26 sin medir la
cadena, y las dos eran falsas en direcciones opuestas** —«el objetivo falta en la mayoría de
unidades» y «no se puede puntuar en absoluto»—. La regla que sale: **una consecuencia para F26 es una
afirmación como cualquier otra y no se escribe sin medir la cadena entera hasta ella.**

**La consecuencia real, TERCERA versión — y la segunda también se quedaba corta.** F26 podrá
puntuar el objetivo contra la REGLA —`entrada ± objetivo_rr × base_calculo_objetivo`— **cuando A-18
esté cerrada, y no antes**: hoy esa regla tiene **dos lecturas que difieren en un 25 % del
recorrido** (3,75 frente a 3,00 sobre la distancia entrada-stop, §4). Puntuar «contra la regla» sin
decir cuál de las dos es puntuar contra un número que todavía no existe. Lo que en ningún caso podrá
F26 es verificar que en una operación concreta el trader colocara ese TP, porque el fichero no lo
guarda.

Las dos primeras redacciones eran error mío —falsas en direcciones opuestas, sin medir la cadena—.
**Ésta no lo es**: la cadena era más larga de lo que nadie había escrito, y sólo apareció al cruzar
el RR realizado con los tres parámetros. La regla se amplía: una consecuencia para F26 no se escribe
sin medir la cadena entera hasta ella, **y la cadena incluye las ambigüedades abiertas que cuelgan
de los parámetros que nombra**.

## 7. Los agregados: hoy el riesgo es FUTURO, no presente

Medido: el libro de agosto tiene **una sola pestaña**, `backtesting-analytics`, y **ningún agregado
dentro**. O sea que hoy la regla del fichero mixto no protege de nada real —no hay nada que evitar en
este libro—. Se escribe igual, y el test la prueba contra un libro sintético cuya pestaña de
agregado es **XML inválido a propósito**: si algún día alguien la toca, revienta.

El riesgo es real y es futuro: el libro de **mayo** y el de **septiembre** contienen días reservados,
y un agregado suyo no se puede trocear. Ninguna autorización lo abre.

## 8. Los tests

Seis de contrato nuevos en `tests/contract/test_ingesta.py`, sobre un xlsx **sintético** construido
con stdlib —el material real no entra en los tests—:

| Test | Qué ve fallar |
|---|---|
| `test_la_ingesta_abre_de_verdad_y_produce_casos` | que el camino entero funciona, no sólo que no explota |
| `test_un_dia_reservado_no_se_ingiere_ni_se_nombra` | el día reservado no aparece ni en el resultado ni en la salida |
| `test_el_agregado_no_se_lee_aunque_viva_en_el_mismo_fichero` | pestaña de agregado con XML inválido: tocarla revienta |
| `test_el_invariante_geometrico_aborta_nombrando_la_fila` | stop del lado equivocado ⇒ aborta, nombrando la fila |
| `test_una_fila_sin_stop_no_produce_caso_y_se_cuenta` | el contador, que es lo único que delata la desaparición |
| `test_el_lector_no_publica_el_conjunto_de_fechas_ni_de_columnas` | ni el retorno ni el error mencionan lo encontrado |

Más `test_solo_un_modulo_puede_nombrar_el_libro_del_trader` en
`tests/contract/test_import_contracts.py`, y `RAIZ_MATERIAL` en `tests/conftest.py`: **hasta hoy nada
impedía que un test abriera el xlsx de mayo** —la guarda sólo miraba la carpeta del holdout—. ADR-0033
lo dejó escrito («el día que F14 escriba la ingesta, pasa por la puerta») y ese día era hoy.

## 9. Lo que NO se ha hecho

- **No se ha ingerido nada de verdad.** No hay ni un `caso-*.yaml` commiteado. El comando existe y
  los tests lo ejercitan contra material sintético; la ingesta real de mayo y de los 4 `dev` de
  septiembre es la decisión del §11.
- **No se toma la decisión por sesión.** Convertir «no hay operación en la sesión 11-15» en
  `no_trade` es una **inferencia nuestra**, no un dato del trader, y ADR-0016 exige que una
  inferencia declare el ADR que la decide. Esa decisión es F14 D1 y **no está tomada**: el caso
  guarda lo que el material dice —las operaciones— y la derivación es de F14b. Escribir hoy un
  `no_trade` derivado sería exactamente «llamar lo que hizo el trader a algo que dedujimos nosotros».
- **`idealTP` no se guarda** y no se le gasta al trader una pregunta por ella. Queda como deuda:
  *columna del material que no sabemos qué es y no usamos*.
- **No cierra** el alcance de `excluir` en `kappa_entre_sesiones` (bloqueante para firmar, ADR-0033
  enmendado), ni `EXPOSICIONES` sin mecanismo.

## 10. Deuda que esta rama DESCUBRE, y hay que leerla

**JUNIO sigue siendo `dev` en el reparto de la sesión 1, y ADR-0025 lo descartó.** Medido:

```
dias_ingeribles(repo) → 20 días:  2026-05: 6 · 2026-06: 10 · 2026-09: 4
```

Hoy es inocuo —no hay xlsx de junio en el corpus, así que no se ingiere nada— pero **el día que
llegue uno, la ingesta escribiría 10 casos de un mes que el consultor descartó, sin que nada chille**.
El `config.yaml` del kit no tiene `cobertura_material`; el del camino de fidelidad sí. No se arregla
aquí porque tocar el reparto commiteado de la sesión 1 no es cosa de esta rama.

## 11. Qué debe decidir el usuario

> **Los cuatro puntos de abajo quedaron DECIDIDOS por el consultor el 2026-09-21**, al validar esta
> rama y antes del ritual. Se dejan escritos con su decisión al lado, porque el informe tiene que
> poder leerse dentro de seis meses sin el hilo de la conversación. La decisión 0 —el commit de
> A-18— es la que produjo la §4 de arriba, y no estaba en ninguna de las dos listas.

1. **DECIDIDO: F14a se valida**, con el commit de A-18 dentro, y va al ritual con tag `stable/F14a-ingesta`.
2. **DECIDIDO: la ingesta real de mayo va en la SIGUIENTE rama**, `trabajo/mayo-dev-ingerido`, y
   **con más alcance del que yo proponía**: no sólo ingiere los 6 días `dev` —6 `caso-*.yaml` con
   precios, cuyo commit arrastra por primera vez el régimen del trailer `Fuente:` a esta línea de
   trabajo— sino que **repite sobre ellos la medida del RR de la §4**. Eso es lo que convierte un
   mes en dos y lo que puede mover A-18 de «una medida» a «un hecho»: si mayo también da suelo en
   3,00, la lectura `caja_completa` queda en serios apuros y entonces sí toca decidirla.

   Mi motivo era que esta rama se valide como mecanismo sin mezclarlo con el material. El del
   consultor es más fuerte y lo dejo con sus palabras: **el informe dice CERO `caso-*.yaml`, y eso
   es lo que permite validarla como MECANISMO**; en cuanto escriba 6 casos con precios deja de ser
   «la ingesta funciona» para ser «la ingesta funciona y además aquí está el primer material», y
   las dos cosas no se validan por separado.

3. **DECIDIDO: junio (§10) se arregla con `cobertura_material` en el `config.yaml` del kit, y NO se toca el reparto de la sesión 1** —artefacto commiteado y anclado por blob, línea base de comparación de toda la semana, y soporte de la prueba de anterioridad por caso: reparticionar es legítimo con cero `LABEL_CASE`, pero el radio de explosión no se justifica para un defecto hoy inocuo—. La guardia va **donde se lee**, no reescribiendo la historia. Y lo que añadió el consultor: **la exclusión tiene que GRITAR** —un día que esté en un reparto y fuera de `cobertura_material` se cuenta, se nombra el mes y se dice el motivo en la salida—, porque un mapa incompleto indistinguible de uno completo es justo lo que se acaba de arreglar en `casos_reservados`.
4. **DECIDIDO: el campo `buscado_en_corpus` es condición fechada.** Es cambio de esquema en `knowledge/spec/`, con su trailer `Fuente:` y con el test que congela cuáles están RESUELTAS, y no se atornilla a una rama que cierra. La condición, escrita para que no sea «alguna vez»: **la próxima ambigüedad que se abra lleva el campo, y el commit que la abra trae el cambio de esquema**. Hoy no se abre ninguna, así que esperar no cuesta nada.

## 12. Cómo comprobarlo

```bash
git log --oneline -3
git status --short

# La puerta sigue cerrada
git hash-object docs/validation/PREREGISTRO.md   # 52649183dcdc55f136d88675feaa7c43459b5277
grep -c "SIN RELLENAR" docs/validation/PREREGISTRO.md
find . -name "AUTORIZACION-*.md" -not -path "./.git/*" | wc -l   # 0

# Los días se derivan, no se eligen
uv run python -c "from pathlib import Path; from botsito.cases.ingesta import dias_ingeribles; \
import collections; d=dias_ingeribles(Path('.')); \
print(len(d), dict(sorted(collections.Counter(k[:7] for k in d).items())))"

# El contrato del lector único
uv run pytest tests/contract/test_import_contracts.py -k libro_del_trader -q
uv run pytest tests/contract/test_ingesta.py -q

# La nota de A-18: está, y no ha cambiado nada de lo que decide
grep -c "PRIMERA MEDIDA" knowledge/spec/ambiguedades.yaml
uv run python -c "from pathlib import Path; from botsito.cases.ambiguedades import cargar_ambiguedades as c; a=[x for x in c(Path('knowledge/spec/ambiguedades.yaml')) if x.id=='A-18'][0]; print(a.estado, a.decision, len(a.evidencia))"   # ABIERTA None 3
uv run botsito spec check

# Todo
make check > make-check.log 2>&1; echo $?     # a FICHERO, nunca a /dev/null
uv run botsito kit check --sesion 2026-09-09-sesion-01
```

## Estado
WAITING_FOR_USER_VALIDATION
