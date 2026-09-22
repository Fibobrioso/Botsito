# Que el cero signifique una sola cosa

Rama `trabajo/cobertura-material-del-kit`, desde `da52c1b` (tag `stable/F14a-ingesta`). Sin tocar
main, sin merge, sin tag, sin push. **`PREREGISTRO.md` intacto** (blob
`52649183dcdc55f136d88675feaa7c43459b5277`); **cero `AUTORIZACION-*.md`**; **cero `caso-*.yaml`**;
`data/` sin tocar. Sin descargar ningún mes.

La rama empezó llamándose «la guardia que falta: un mes descartado sigue siendo ingerible», y **no
va de junio**. Va de que hasta hoy un día sin filas podía ser **dos cosas incompatibles** —«el
trader miró y no operó», que es un dato suyo, y «este mes no tiene material», que es ausencia de
conocimiento— y las dos daban **exactamente el mismo silencio**.

## 1. La línea base

`kit check --sesion 2026-09-09-sesion-01` guardado antes de tocar nada y vuelto a ejecutar al
final: **idéntico** (`diff` vacío). `make check` a fichero, nunca a `/dev/null`.

Resultado final de `make check`, pegado y no descrito:

```
uv run ruff check src tests scripts      -> All checks passed!
uv run mypy                              -> Success: no issues found in 131 source files
uv run lint-imports                      -> Contracts: 4 kept, 0 broken.
uv run pytest                            -> 775 passed in 288.59s
exit code                                -> 0
```

**La pasada anterior salió en rojo y va dicho**: `1 failed, 774 passed`, porque el contador de
`PROJECT_STATE` decía 548 funciones de test y hay 555. Es la guardia `documentos_vivos` haciendo su
trabajo sobre un documento que describe el presente.

## 2. La revisión de diseño refutó el brief TRES veces, y por eso está aquí

Se hizo antes de escribir una línea de código, midiendo. No con dos agentes: a mano, por coste, y
cumplió su función.

| Lo que el brief daba por cierto | Lo medido |
|---|---|
| Los dos caminos tienen esquemas distintos y hay que unificarlos | **Es el mismo**: `config_desde_doc` vive en `paquete.py` y `CLAVES_OPCIONALES` (`paquete.py:71`) ya admitía el campo. Nada que unificar |
| `cobertura_material` en el config del kit cierra el defecto | **No lo toca**: `dias_ingeribles` no lee el config. `inspect.getsource` → `universo` False, `cobertura` False, `cargar_config` False |
| Declarar junio con cero tramos funciona hoy | **El esquema lo rechazaba** (`paquete.py:139-140`, `lista de tramos no vacia`) |
| Abril entraría en el universo de la sesión 2 y lo vuelve bloqueante | **Falso, y el error era mío**: `2026-04` está en `vistos.yaml` desde el 2026-09-12 y `universo()` lo excluye por `meses_vistos` |
| Bastaba con el campo en el config | **La llamada del kit no lo pasaba**: `universo(...)` con nueve argumentos, `cobertura` en su valor por defecto |

**Las dos últimas son correcciones de una medida que había dado yo**, y sobre ella se montó el §0
del brief y el orden de tres ramas. Leí `manifiestos_del_prefijo` y afirmé sobre la cadena sin
seguir hasta el filtro de vistos ni comprobar la llamada. Es el patrón 3 de la lista, y ese mismo
día ya me había pasado con `ev-v4-011951`.

## 3. Los TRES agujeros

1. **Junio es ingerible HOY.** `dias_ingeribles` no lee el config, y los diez días de junio ya
   están dentro del `particiones.yaml` commiteado, que está anclado por blob y no se toca.
2. **Junio entraría en el universo de un `kit build` NUEVO.** No lo tapa `vistos.yaml` —y es
   correcto que no lo tape: el trader no vio junio, así que **es ciego**— y la llamada del kit no
   pasaba la cobertura. Se sortearía a una partición y no se etiquetaría nunca.
3. **El cero significa dos cosas**, y además `--material` puede ser el libro equivocado sin que
   nada lo diga. Es el que más vale y no lo tocó ninguna corrección.

**Las dos preguntas son ortogonales, y hacen falta las dos:**

|  | `vistos.yaml` — ¿es ciego? | `cobertura_material` — ¿hay material? |
|---|---|---|
| abril | **NO** | **SÍ** |
| junio | **SÍ** | **NO** |

Junio es el único mes con dataset que es ciego y está vacío, y ésa es la combinación que hasta hoy
no se podía expresar.

## 4. Lo que se construyó

**CERO TRAMOS es un valor con significado** (`paquete.py`): dice *«hay decisión sobre este mes y no
hay material»*. Hasta hoy se rechazaba como error, y por eso la única forma de excluir un mes era
invertir el default para todos (`solo_con_cobertura`), que es el riesgo de negar un mes legítimo
porque nadie lo declaró. **`solo_con_cobertura` sigue en `False`**: un mes no declarado queda **sin
acotar**, no excluido.

**El motivo dejó de mentir** (`ventanas.motivo_de_cobertura`, público a propósito). Con la lista
vacía decía literalmente `«(2026-06 cubre )»`. Ahora: `«2026-06: sin material del trader (declarado
con cero tramos en cobertura_material)»`. La función vive fuera del bucle para que el test compruebe
**la frase** y no una copia suya.

**La llamada del kit pasa la cobertura** (`paquete.py`). Hasta hoy el campo era inerte en este
camino.

**LA PUERTA en `dias_ingeribles`.** Un día cuyo mes no esté declarado —o lo esté con cero tramos—
no es ingerible. **No lanza**: los niega y los devuelve contados **por mes**, porque lanzar dejaría
el comando inservible mientras junio siga repartido, y negarlos en silencio es justo lo que la rama
viene a cerrar. Dos motivos distintos, porque son dos cosas distintas: *no está declarado* frente a
*declarado con cero tramos*.

**LA REGLA POR MES en `ingerir`.** Si un mes pedido no tiene **ni una fila** en el libro que se ha
pasado, es error y se nombra el mes. Habla del **fichero** —«el material que me has dado»— y no de
los días del trader, así que no publica calendario.

**EL CERO QUE QUEDA, contado y dicho.** Después de la puerta y de la regla, un día ingerible sin
filas significa una sola cosa, y el comando lo dice con ese motivo. Antes imprimía «1 casos escritos
de 4 días ingeribles» y callaba los tres.

## 5. Lo medido, antes y después

```
ANTES   dias_ingeribles(repo)                  -> 20 : 2026-05 6 · 2026-06 10 · 2026-09 4
DESPUES dias_ingeribles(repo, config.cobertura) -> 10 : 2026-05 6 · 2026-09 4
        negados -> {'2026-06': (10, '2026-06 esta declarado con CERO tramos: no hay material...')}
```

`kit check --sesion 2026-09-09-sesion-01`: **IDÉNTICO** a la línea base.

Y un aviso **esperado**, que es la enmienda de ADR-0035 funcionando:

```
AVISO: 2026-09-09-sesion-01/ventanas.yaml: su config congelado difiere del config.yaml de hoy
en cobertura_material. Es lo esperado cuando el config global evoluciona: el paquete se
reproduce con el suyo (ADR-0035, enmienda del 2026-09-21).
```

## 5b. Las líneas que imprime el comando, que son el entregable

«Que el cero signifique una sola cosa» vive en el **mensaje**, no en el código. Ejecutado de
verdad sobre un repo temporal con el config y el registro reales, un reparto sintético y un xlsx
sintético:

**(a) Un día ingerible sin operaciones** — `exit = 0`, y no es un error:

```
INGESTA: 1 casos escritos de 2 dias ingeribles; 1 filas leidas; 0 pestanas de agregado abiertas
INGESTA: 1 dias ingeribles sin ninguna operacion: el material cubre esos dias y el trader no
         opero. NO producen caso hoy, y que produzcan un `no_trade` es una decision que no esta
         tomada (ADR-0016)
```

**(b) Un mes sin material** —junio, declarado con cero tramos— `exit = 0`, y se niega **por mes**:

```
INGESTA: 1 casos escritos de 1 dias ingeribles; 1 filas leidas; 0 pestanas de agregado abiertas
INGESTA: 2 dias de 2026-06 NO son ingeribles: 2026-06 esta declarado con CERO tramos: no hay
         material del trader. No se han leido ni escrito, y no se nombran uno a uno: un dia
         laborable que no aparece es su etiqueta
```

**(c) El libro equivocado** —el de mayo, pidiéndole días de septiembre— `exit = 1`, y **no escribe
nada**:

```
ERROR: el material que se ha pasado no tiene ni una fila de 2026-09: o es el libro de otro mes, o
       falta. No se escribe nada, porque un cero de aqui no se puede distinguir de un dia sin
       operaciones
```

Los tres mensajes dicen **el motivo**, y ninguno nombra un día.

## 5c. El agujero 2, ejecutado

Un `kit build` NUEVO sobre el repo sintético de `tests/unit/test_kit.py`:

```
(1) SIN cobertura  ->  universo = 9 casos, mes 2026-05 · excluidos = 2     <- el estado de `main`
(2) CON "2026-05": []  ->  KitError: se piden 5 casos y el universo tiene 0
    y el motivo de cada dia excluido:
    2026-05: sin material del trader (declarado con cero tramos en cobertura_material)
(3) CON tramos de verdad  ->  universo = 9 casos (antes 9) · mismos dias: True
```

El (3) es el que impide cerrar de más: acotar a todo el mes **no quita ningún día**.

## 6. Lo que se declaró en el config, y lo que NO

Se declara **sólo lo que ya estaba declarado en otro sitio**: mayo `01..31` (del `vistos.yaml`: *«el
trader backtesteó mayo entero y lo entregó el 2026-09-11»*, commit `8fb2323`), septiembre `01..18`
(ya en `fidelidad/config.yaml` y en `vistos.yaml`), y junio con **cero tramos** (ADR-0025 §1).

**No se declaran enero, abril, julio ni agosto**, y el motivo es de proceso y no de olvido: sus
tramos saldrían de **leer la columna de fechas** de sus backtests, y eso lo hace el consultor una
sola vez antes del sorteo y lo declara el mismo día (ADR-0021 §1, `CLAUDE.md`). Los cuatro están en
`vistos.yaml`, así que ningún paquete ciego los sortea.

## 7. Los tests

| Test | Qué ve |
|---|---|
| `test_sin_cobertura_un_mes_descartado_sigue_siendo_ingerible` | **EL DEFECTO EN ROJO**: es el estado de `main` |
| `test_la_puerta_niega_el_mes_sin_material_y_lo_dice_por_mes` | se cuenta, se nombra el mes y el motivo, y **ni un día** aparece |
| `test_un_mes_no_declarado_se_niega_con_otro_motivo` | no declarado ≠ declarado vacío |
| `test_los_dos_ceros_se_distinguen` | **el criterio que prueba la rama**: día sin operaciones se cuenta; mes sin filas es error con el mes |
| `test_el_esquema_admite_cero_tramos_y_sigue_rechazando_lo_demas` | la lista de días sigue prohibida |
| `test_el_motivo_de_cero_tramos_no_miente` | la frase real, no una copia |
| `test_la_cobertura_saca_un_mes_del_universo_y_el_kit_la_pasa` | **el agujero 2**, y además **CONSTRUYE de verdad** con tramos reales |

El último cubre el criterio §5.3: una guardia que sólo sabe decir que no no ha demostrado nada.

## 8. Los tres patrones, comprobados

- **Input global y mutable del que depende la reproducción**: no. El paquete de la sesión 1 se
  recompone con su `datasets:` y su `config:` congelados (ADR-0035); el cambio del config global
  produce un aviso de deriva y nada más, y `kit check` sale idéntico.
- **Prohibición más estricta que el ADR**: no. La puerta sale de ADR-0025 §1 y de ADR-0036, y el
  default permisivo se conserva a propósito.
- **Regla que enumera los casos en vez de nombrar la condición**: **es el patrón que esta rama
  arregla**, y hubo que resistirse a repetirlo. `solo_con_cobertura=True` habría sido enumerar —hay
  que declarar todos los meses o no entra ninguno—; cero tramos nombra la condición y deja el
  default abierto.

## 9. Lo que NO se ha hecho

- **No se decide si un día ingerible sin filas produce un `no_trade`.** Hoy no produce nada y así
  se queda: toca la forma del caso y roza «un día sin ninguna operación ES su etiqueta». Lo que esta
  rama aporta es que, cuando se tome, se tomará sobre un conjunto donde el cero **ya no es ambiguo**.
- No se descargó abril, febrero ni marzo. No se ingirió mayo. No se tocó A-18 ni la predicción
  congelada. No se tocó el reparto ni las anclas.

## 10. Una limitación que crea esta rama, y va dicha

La regla por mes usa los **días pedidos**: si el trader no hubiera operado en **ninguno** de los
días ingeribles de un mes, el libro correcto daría cero filas de ese mes y el comando lo llamaría
error. Con seis días `dev` de mayo es improbable, pero **no es imposible**, y el error diría algo
falso. La alternativa —preguntarle al lector si el fichero tiene alguna fila de ese mes, sin
filtrar por día— distinguiría los dos casos, pero rompe la regla de que el lector no acumula nada
del libro (ADR-0037 §6). **Se deja como está**, y el motivo que lo sostiene es que **falla hacia
el lado seguro**: un falso error **para** el comando, no fabrica un dato. En una rama que existe
para que nadie fabrique ausencias, equivocarse parando es el error barato.

**Pero el arreglo existe y se nombra para que no se redescubra:** *declarar el mes del material y
compararlo con lo pedido*, en vez de deducirlo de las filas. El fichero ya viene con el mes en el
nombre y el inventario ya lo hashea. Con la declaración, pasar el libro de mayo y pedir días de
septiembre **se niega antes de leer una fila**, sin tocar ADR-0037 §6 —el lector sigue sin acumular
nada del libro— y la limitación desaparece: un cero dentro del mes declarado vuelve a ser un dato.

**No se hace aquí.** Va a Technical Debt con su condición —el día que un mes llegue con cero
operaciones en todos sus días ingeribles, o el día que el mes del material sea metadato declarado,
lo que pase antes— y necesita una medida propia que no es de esta rama: si el inventario del corpus
ya registra el mes o hay que añadirlo.

## 11. Qué debe decidir el usuario

1. **Validar la rama** y, si procede, el ritual con tag `stable/F14-cobertura` (comprobado con
   `git tag -l`: no colisiona).
2. **DECIDIDO el 2026-09-21: la limitación del §10 se queda**, porque falla hacia el lado
   seguro, y **su arreglo queda nombrado** en Technical Debt con su condición.
3. **DECIDIDO: el `no_trade` por ausencia NO entra en la rama de mayo.** Espera a la rama de la
   forma del caso, con su ADR, y por tres motivos: es una decisión sobre **qué es un caso** y no
   sobre cómo se ingiere; la rama de mayo ya tiene su trabajo —ingerir los 6 días `dev` y repetir
   la medida del RR contra la predicción congelada— y su valor es ser el **primer material real**,
   así que meterle dentro una decisión semántica la hace no validable por separado; y **esperar
   sale barato justamente por lo que esta rama compra**: la salida de mayo ya va a decir qué días
   no produjeron caso y por qué, así que la decisión se podrá tomar después sobre un conjunto
   limpio y **sin volver a ingerir**.

   Mayo ingiere lo que tiene operaciones, dice cuáles no y por qué, y escribe **cero** casos
   `no_trade`. En su rama es donde toca mirar «un día sin ninguna operación ES su etiqueta», que es
   lo que quemó algo el 2026-09-12.

## 12. Cómo comprobarlo

```bash
uv run python -c "from pathlib import Path; from botsito.cases.paquete import cargar_config; \
from botsito.cases.ingesta import dias_ingeribles; import collections; \
c=cargar_config(Path('knowledge/cases/kit/config.yaml')); i=dias_ingeribles(Path('.'), c.cobertura); \
print(len(i.dias), dict(sorted(collections.Counter(k[:7] for k in i.dias).items()))); print(i.negados)"
# -> 10 {'2026-05': 6, '2026-09': 4}   y junio negado por MES

uv run pytest tests/contract/test_cobertura.py -q
uv run pytest tests/unit/test_kit.py -q -k cobertura
uv run botsito kit check --sesion 2026-09-09-sesion-01     # IDENTICO a la linea base
make check > make-check.log 2>&1; echo $?                   # a FICHERO, nunca a /dev/null
```

## Estado
WAITING_FOR_USER_VALIDATION
