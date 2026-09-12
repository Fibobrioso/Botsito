# F12 · spec-semantic-validator — INFORME DE VALIDACIÓN

**Funcionalidad:** F12 spec-semantic-validator
**Rama:** `feature/F12-spec-semantic-validator`
**Objetivo:** que la spec no pueda decir cosas incoherentes entre sí, y que las reglas dejen de ser
prosa en español y pasen a tener una forma que un motor pueda ejecutar sin interpretar.
**Brief:** `docs/plan/features/F12-spec-semantic-validator.md`
**Estado:** WAITING_FOR_USER_VALIDATION

---

## 0. Lo que hay que mirar primero

F12 empezó como "añadir comprobaciones semánticas" y acabó siendo otra cosa: **las guardias que se
escribieron encontraron defectos vivos en una spec que ya estaba validada y en `main`**. No son
hipótesis; cada uno se disparó solo, con su id, la primera vez que la guardia corrió.

| # | Lo que encontró | Dónde estaba | Coste si nadie lo mira |
|---|---|---|---|
| 1 | Siete defectos en la spec validada de F11, dos capaces de costar dinero | `36e4c65`, corregidos en `925d3f6` | RN-006 ganaba a RN-014 y no ponía el break even; se reentraba tras tocar el tope diario |
| 2 | El freno de riesgo no frenaba y el break even era **inalcanzable** | `fe9ee21` | El tope del 4,5 % prohibía abrir en el tick del evento y nada impedía abrir en el siguiente |
| 3 | A-21 nació mal: la definición de los esquemas **sí** estaba en el corpus | `36bee94` | Se habría llevado a la sesión 2 una pregunta ya respondida |
| 4 | Cuatro reglas ejecutaban un parámetro que **no declaraban** | esta entrega | RN-014 ejecuta `break_even_criterio_ruptura`, DEFAULT_AMBIGUOUS bajo A-13, y la guardia de "regla vigente con valor en revisión" no lo veía |
| 5 | La guardia de citas revocadas nació corta por **tercera** vez | esta entrega | Al cerrar el acuerdo del lotaje, un predicado se quedó citando el registro que ese acuerdo acababa de revocar |
| 6 | `feedback apply` era ciego al caso más común de preguntar | esta entrega | El trader ratifica un default nuestro y el registro se queda diciendo que es un default, con la ambigüedad abierta |

Los dos últimos aparecieron **el mismo día y por el mismo cambio** (ADR-0020), lo que dice algo del
método: un cambio de valor de negocio no es un cambio de valor, es una onda que atraviesa reglas,
citas, descripciones y ambigüedades.

## 0 bis. La auditoría de cierre (dos agentes, 2026-09-11/12)

Dos agentes en paralelo, uno de código y tests y otro de documentación y proceso, con el encargo
de no modificar nada. Entre los dos: **57 hallazgos**. No fue un trámite: el de código encontró
**cuatro defectos de severidad 1 en el trabajo de esta misma funcionalidad**, y uno de ellos puede
costar dinero.

### Lo que encontró el auditor de código

| # | Hallazgo | Estado |
|---|---|---|
| 1 | **`liquidez_tomada` y `estructura_m1` se fijaban sin estar declarados**, así que la guardia de hechos —que solo itera los declarados— no los veía. El primero es la precondición de los dos esquemas de entrada, y vivía únicamente en la prosa de `se_da_esquema`: **un motor que leyera `forma` habría entrado sin esperar a que se tomara la liquidez de M15** | CORREGIDO: `liquidez_tomada` se declara y `se_da_esquema` la exige con `depende_de`; RN-007 pasa a la acción `agrupar_estructura`; la guardia denuncia los hechos usados y no declarados |
| 2 | **El `literal` de un predicado no se comparaba con nada.** Se podía poner cualquier frase en boca del trader dentro del vocabulario. El comentario que había en `comprobar_literales` predijo este caso con esas palabras | CORREGIDO: `comprobar_literales` recibe el vocabulario; test que lo dispara |
| 3 | **La `cita` de un predicado o un acumulador podía no existir**: un `fb-…-deadbeef` pasaba entero | CORREGIDO en `comprobar_contra`, con test |
| 4 | **La `descripcion` de un parámetro estaba fuera del hash**, y es el único sitio donde se define qué significan las dos opciones de `lotaje_base`: reescribir esa frase cambiaba el lote un 25 % sin mover `spec_version` | CORREGIDO: entra en el hash, junto con `alias` y `visto_en` del glosario |
| 5 | **`permite` / `prohibe` no se validaban contra nada** (11 de las 24 reglas vigentes): su valor es una lista y el recorrido los saltaba | CORREGIDO: sección `efectos` y comprobación, con test |
| 6 | Una invocación con argumento que no fuera un mapa se colaba entera | CORREGIDO |
| 7 | `comprobar_citas_revocadas` dejaba fuera los acumuladores: **la cuarta vez que esa guardia nace corta** | CORREGIDO |
| 8 | **El cruce hecho-declarado casaba por SUBCADENA**, y bendecía una declaración falsa: `hechos.sesgo` decía que RN-003 lo consume —lo produce— y colaba porque su `cuando` contiene `sesgo_h4_criterio_ruptura`. Peor: corregir la declaración hacía *fallar* la guardia | CORREGIDO: token exacto, y la declaración falsa arreglada |
| 9 | La comprobación `forma` ⊆ `parametros` que F12 estrenó tenía falsos positivos (una clave que se llama como un parámetro) y un falso negativo que la propia spec ya usa (`OP.stop_fraccion_caja`) | CORREGIDO: recorre el árbol |
| 10 | `comprobar_precedencia` no miraba `forma`, y **RN-013 y RN-015 tenían el disparador ejecutable idéntico byte a byte**, misma clase, sin `complementa` | CORREGIDO: compara disparadores; RN-015 declara que complementa a RN-013 |
| 12 | `pendiente_definicion` se validaba solo de formato: `A-999` pasaba y además eximía a la regla de tener forma | CORREGIDO: se cruza con las ambigüedades ABIERTAS |
| 13 | `comprobar_consumo` no validaba los ids si una regla ya nombraba el parámetro, ni los de los parámetros sin valor, y admitía una regla DESCARTADA como lectora | CORREGIDO |
| 14-18 | Tests que pasaban por la razón equivocada: el de los `R-NN` no ejercitaba el generador, el del vocabulario no cubría acumuladores, `spec check` solo se probaba en verde, el del hash omitía `acciones` | CORREGIDOS |
| 19-23 | Menores: `re.match` aceptaba un salto de línea final, `except ValueError` se tragaba bugs, el vocabulario se parseaba tres veces, `scripts/` estaba fuera de `ruff` | CORREGIDOS (salvo `_ARGS_DE_VALOR`, ver §8) |

### Lo que encontró el auditor de documentación

Verificó una por una las cuatro cuentas de ADR-0020 (21, 27,6, 28,2 y 34,5) y las tres derivadas,
y dio por buena la separación entre lo que decidió el consultor y lo que dijo el trader. Sus
hallazgos fueron de **texto que se quedó afirmando el mundo anterior**, y el más grave estaba
dentro del hash:

- **El glosario decía que "el lote se calcula sobre la caja entera" y que "después el stop se mueve
  a uno de sus niveles"**: las dos cosas falsas desde ADR-0020 y A-11. Corregido.
- `stop_fraccion_caja` y `stop_proteccion_capital` describían un stop que se mueve tras la entrada.
  Corregido.
- La cabecera de `strategy_spec.yaml` y el README afirmaban que el `literal` es siempre **del
  trader**; desde el 2026-09-11 hay tres que son del consultor y lo declaran. Corregido.
- **A-13 apuntaba al parámetro equivocado** (`break_even_condicion`, que es CONFIRMED y lo cerró
  A-4), así que `spec status` enseñaba como "en revisión" un valor cerrado y **escondía
  `break_even_criterio_ruptura`, uno de los dos únicos defaults vivos**. Corregido.
- ADR-0014, ADR-0015, ADR-0016 y ADR-0018 seguían afirmando la aritmética o el estado viejos.
  Enmendados en cabecera, sin reescribir lo que decidieron.
- El brief de F12 decía **dos veces que la revisión de diseño estaba PENDIENTE** cuando se celebró
  el 2026-09-10 y produjo ADR-0018 y ADR-0019. Corregido.
- `PROJECT_STATE` y el HANDOFF describían a `main` y a la rama actual con tres días de retraso, el
  índice de ADR se había quedado en el 0013, y el recuento del vocabulario estaba mal. Corregidos.

## 1. Qué se construyó

**La forma ejecutable de una regla (ADR-0019).** Las 24 reglas vigentes tienen `forma`: un árbol
booleano `cuando` sobre **predicados con argumentos** y un `entonces` con `permite` / `prohibe` /
`hace` sobre **acciones**. El vocabulario vive en `strategy_spec.yaml` —no en un cuarto fichero,
que habría roto el contrato del hash— y son cinco cosas con nombre: **22 predicados, 13 acciones,
2 efectos** (lo que una regla permite o prohíbe, sección nacida en la auditoría de cierre),
**6 hechos** (cada uno con quién lo produce y quién lo consume) y **3 acumuladores** (con su base y
su reinicio). Cada predicado lleva su cita, y desde la auditoría de cierre esas citas y sus
literales se comprueban.

**La precedencia por clase (ADR-0018).** `gate > terminal > disparador > fallback` (una prohibicion gana siempre, y a las 15:00 cerrar la jornada gana a activar una entrada), y no el orden
del fichero, que es editorial: RN-026 y RN-027 son VIGENTES y viven bajo la cabecera "reglas
descartadas". Dos reglas de la misma clase con los mismos parámetros son un error que nombra los
dos ids.

**Las comprobaciones semánticas**, todas en `src/botsito/spec/modelo.py`, todas nombrando el id:

| Guardia | Qué impide |
|---|---|
| `comprobar_contra` | una regla que nombra un parámetro que no existe, o cita algo que no existe |
| `comprobar_literales` | una regla que pone palabras en boca del trader: su `literal` tiene que estar en lo que cita |
| `comprobar_decisiones` | una regla construida sobre parámetros de entorno sin declarar el ADR que la decide (ADR-0016) |
| `comprobar_precedencia` | que el orden del fichero decida quién gana |
| `comprobar_forma` | vocabulario inexistente, argumentos no declarados, un valor de negocio donde va el NOMBRE de un parámetro, hechos que nadie produce o nadie consume, y **`parametros` que no declara lo que `forma` usa** |
| `comprobar_consumo` | un parámetro **con valor** que ninguna regla vigente nombra y que nadie declara leer |
| `comprobar_citas_revocadas` | que una regla, un término del glosario **o el vocabulario** cite un registro que otro ya corrigió |

**`botsito spec check`**: la capa semántica sola, sin las otras nueve delante. `knowledge validate`
la corre también, pero después de corpus, evidencia y feedback, y devuelve en cuanto una de esas
falla: quien está escribiendo reglas no llegaba a ver sus fallos. Comparten `problemas_de_spec`,
así que no pueden divergir.

## 2. Los parámetros sin lector

El brief pedía resolver **diez** parámetros con valor que ninguna regla nombraba. Al encender la
guardia saltaron **catorce**: los diez del brief y **cuatro más** que fueron el hallazgo —
`sesgo_h4_criterio_ruptura`, `zona_control_criterio_completada`, `break_even_criterio_ruptura` y
`stop_en_orden_pendiente` sí se ejecutan, dentro de `forma`, pero sus reglas no los declaraban en
`parametros`, que es justo la lista que leen las otras guardias. De los diez del brief, tres se
cerraron nombrándolos en una regla y siete declaran `consumido_por`.

De los que sí estaban huérfanos:

| Parámetro | Quién lo lee | Por qué |
|---|---|---|
| `broker_dst`, `broker_offset_base` | **RN-020** | el corte del día de riesgo cae en el reloj del servidor (`reloj_dia_riesgo`), y ese reloj no se sabe sin su calendario y su desfase |
| `instrumento_digitos` | **RN-026** | `instrumento_stops_level` viene en puntos: compararlo con una distancia exige la escala del símbolo |
| `modelo_llenado`, `latencia_ms` | F24, F27 | MASTER_PLAN H.2:219 |
| `instrumento` | F24, F28, F31, F33 | MASTER_PLAN H.2:211 |
| `saldo_inicial_cuenta` | F24, F33 | no es base de ningún cálculo: F24 arranca el backtest con él y F33 lo compara con la cuenta real |
| `cuenta_objetivo` | F33 | la cuenta a la que se despliega |
| `cuenta_pruebas` | F17, F33 | F17 mide el reloj del servidor contra ese terminal |
| `huso_grafico` | ADR-0017 | documental: traduce lo que el trader DICE a un instante; no lo ejecuta nadie |

**Una discrepancia deliberada con el brief.** Proponía meter `modelo_llenado` en RN-011. No se
hizo: el modelo de llenado es del simulador, no de la estrategia. Meterlo en una regla habría hecho
pasar por operativa del trader una decisión del motor, que es exactamente lo que ADR-0016 existe
para impedir. Su hogar es F24/F27, y así queda declarado.

## 3. Los `R-NN` dejan de ser posicionales

`scripts/hoja_sesion_docx.py` numeraba las catorce confirmaciones con `enumerate`. Insertar o
reordenar una entrada renumeraba las catorce en silencio y dejaba mintiendo el anexo de
`docs/validation/SESION-01-2026-09-09.md`, que las cita una a una. Ahora el `id` es explícito en
`contexto_preguntas.yaml`, el generador lo valida (formato y unicidad) y un test de contrato ata
las catorce del kit a las catorce del informe.

## 4. `spec status` deja de afirmar lo que no comprueba

Un parámetro sin valor lo está por dos motivos que no valen lo mismo: **el trader lo rechazó** —y
hay un registro `REJECT` que lo sostiene— o **nadie se lo ha preguntado todavía**, que es como
nacieron los 24 que F10 dejó en UNKNOWN. `spec status` llamaba "a propósito" a los dos. Ahora los
separa y lo comprueba contra el feedback. Hoy los siete tienen su `REJECT`.

## 5. Cómo ejecutarlo

```
uv run botsito spec check      # la capa semantica sola; sale con 1 y nombra el id
uv run botsito spec status     # con que corre el bot y que sigue en revision
uv run botsito knowledge validate
make check
```

## 6. Qué está corriendo hoy

El recuento vivo lo da `botsito spec status` y **no se copia aquí**: esa copia se quedó vieja tres
veces en dos días durante F11. Al cierre de esta entrega: `spec 8.2.0`, 24 reglas vigentes con
forma ejecutable y ninguna en prosa, 50 parámetros confirmados, 2 con un default nuestro y 7 sin
valor a propósito, 8 ambigüedades abiertas.

## 7. Impacto sobre lo anterior

- **ADR-0014 queda enmendado en una frase** (ADR-0020): la caja completa ya no es "la misma
  distancia que dimensiona el lote". Lo que decide ADR-0014 —que el objetivo se mide sobre la caja
  completa— sigue en pie.
- **RN-012 dice lo contrario de lo que decía.** Era "la pérdida real es menor que el riesgo
  nominal, y es a propósito"; ahora el stop cuesta el riesgo entero.
- **El registro tiene un campo nuevo** (`consumido_por`) y entra en el hash.
- `feedback apply` cambia de criterio: compara la fuente anterior sea cual sea su tipo.

## 8. Deuda que F12 deja anotada

1. **La guardia de consumo comprueba que la funcionalidad EXISTE, no que su fila de H.2 prometa
   consumir ese parámetro.** Eso lo sostiene la revisión humana; el texto de la guardia prometía lo
   segundo y se ha ajustado a lo que hace. Tres `consumido_por` (`cuenta_objetivo`,
   `cuenta_pruebas`, `saldo_inicial_cuenta`) se apoyaban en la *categoría* de H.2:211 y ahora están
   nombrados en esa fila, pero la relación sigue siendo editorial.
2. **`_ARGS_DE_VALOR` sigue siendo una lista blanca escrita a mano.** Un argumento declarado que no
   esté en ella admite un valor de negocio crudo (`sentido: alcista` pasa hoy). Invertir la lista
   —todo argumento es de valor salvo los que el predicado marque como estructurales— es la forma
   correcta y no entra en esta entrega.
3. **La `descripcion` de un parámetro estaba fuera del hash y ya no lo está**, pero el mismo repaso
   dejó ver que nadie había auditado *qué más* queda fuera. Hoy el hash cubre todos los campos del
   registro, las reglas enteras y las cinco secciones del vocabulario.

## 9. Qué debe decidir el usuario

1. **Validar o no F12.** Si valida: `BOTSITO_ALLOW_MAIN=1 git merge --no-ff`, tag `stable/F12`,
   commit `docs(state)` y push.
2. **La tensión anotada en ADR-0020**: las cifras que el trader mandó sobre mayo (21 %, 27,6 %,
   28,2 %) están contadas en cajas completas, que es la convención vieja del lotaje. Hay que
   ratificarle el acuerdo antes de que esto llegue a una cuenta real, y **no se puede ratificar
   midiendo mayo**: 13 de sus 19 días son holdout.
3. **La deuda de `_ARGS_DE_VALOR`** (lista blanca a mano): arreglarla en F13 o dejarla anotada.

## 10. Qué puede comprobar sin recursos especiales

```
uv run botsito spec check                 # tiene que decir OK
uv run botsito spec status                # los recuentos de la seccion 6
uv run botsito knowledge validate         # todas las capas
make check                                # la suite entera
```

Y para ver que las guardias no son decorativas, romper algo a propósito y ver el id en el mensaje:
cambiar el título de una regla sin tocar `spec_version` (salta el hash), quitar un parámetro de la
lista `parametros` de RN-014 dejándolo en su `forma` (salta la guardia nueva), o borrar el
`consumido_por` de `modelo_llenado` (salta `comprobar_consumo`).

## Estado
WAITING_FOR_USER_VALIDATION
