# F14a · La ingesta del detalle por operación

Rama `feature/F14a-ingesta-del-detalle`, desde `a791f92`. Sin tocar main, sin merge, sin tag, sin
push. **`PREREGISTRO.md` intacto** (blob `52649183dcdc55f136d88675feaa7c43459b5277`, con su marca
`SIN RELLENAR`); **cero ficheros `AUTORIZACION-*.md` en el árbol**; **ninguna partición reservada
abierta**. Sin tocar `knowledge/spec/`, `evidence/`, `feedback/`, ni los repartos y anclas ya
commiteados.

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

**La consecuencia real, medida**: F26 **sí** puede puntuar el objetivo, comparando el del bot contra
la REGLA —`entrada ± objetivo_rr × base_calculo_objetivo`—. Lo que **no** puede es verificar que en
una operación concreta el trader colocara ese TP, porque el fichero no lo guarda.

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

1. **Validar F14a** y, si procede, el ritual de merge con tag `stable/F14a-ingesta`.
2. **Si la ingesta REAL de mayo entra en esta rama o en la siguiente.** Escribiría 6 `caso-*.yaml`
   bajo `knowledge/cases/dev/` —con precios— y su commit necesita trailer `Fuente:`, porque
   `knowledge/cases/` está en `DIRECTORIOS_CON_FUENTE`. Mi recomendación: **en la siguiente**, para
   que esta rama se valide como mecanismo y el primer material escrito no se mezcle con la discusión
   del mecanismo que lo escribe.
3. **Junio (§10)**: si se corrige el reparto de la sesión 1 o se le pone `cobertura_material` al
   `config.yaml` del kit.
4. **La regla del corpus antes de la ambigüedad (§5)**: si el campo de términos buscados entra en
   `ambiguedades.yaml` en la siguiente ambigüedad que se abra, como está anotado, o antes.

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

# Todo
make check > make-check.log 2>&1; echo $?     # a FICHERO, nunca a /dev/null
uv run botsito kit check --sesion 2026-09-09-sesion-01
```

## Estado
WAITING_FOR_USER_VALIDATION
