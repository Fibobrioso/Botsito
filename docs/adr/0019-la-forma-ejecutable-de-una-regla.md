---
status: ACTIVE
date: 2026-09-10
phase: F12
---

# 0019 · La forma ejecutable de una regla: predicados con argumentos, ligadura, y cuatro cosas con nombre

## Decision

1. **Predicados CON ARGUMENTOS**, y todo argumento de valor es un **nombre del registro**, nunca un
   valor. `rompe: {que: ..., contra: ..., criterio: sesgo_h4_criterio_ruptura}`.
2. **Ligadura de variables** entre `cuando` y `entonces` (`liga:`, `distinta_de:`, `posterior_a:`).
3. **Cuatro cosas con nombre, no una**: `predicados` (geometría), `hechos` (estado del bot, con quién
   los produce y quién los consume), `acumuladores` (suma/cuenta + base + reinicio) y, en `entonces`,
   `permite:` / `prohibe:` / `hace:`.
4. **Todo vive DENTRO de `strategy_spec.yaml`**, como claves de nivel superior nuevas. No hay cuarto
   fichero.
5. **Estado `PENDIENTE_DEFINICION`** para la regla cuya condición el corpus no define, con su
   ambigüedad. Hoy: RN-008.
6. **`cuando` es un árbol booleano**: `todos_de` / `cualquiera_de` / `ninguno_de`.

## Problema que resuelve

D1 decidió "predicados nombrados" con la forma más simple posible: nombre + booleano. La revisión de
diseño (tres agentes, 2026-09-10) la probó contra las ocho reglas más difíciles y **aguantó una**.

**El ejemplo canónico del brief ya contenía el fallo.** Proponía
`cierra_con_cuerpo_al_otro_lado: {parametros: [liquidez_m15_criterio_toma]}`. Ese parámetro tiene
`opciones: [cuerpo, mecha]`: **el valor está horneado en el nombre del predicado**. Si el trader dice
"mecha", o el predicado ignora el parámetro que declara, o el nombre miente. Dos puertas para el
mismo hecho, que es lo que ADR-0002 prohíbe.

**Sin argumentos, la geometría explota en nombres.** La misma primitiva —romper un extremo— aparece
con sujeto, referencia y criterio distintos en RN-003, RN-004, RN-014 y en el glosario. Sin
argumentos hacen falta `rompe_extremo_h4_previa_con_mecha`,
`rompe_punto_extremo_anterior_con_mecha`, `rompe_zona_posterior_a_la_entrada`… cada uno con su
definición en prosa.

**Sin ligadura, un cuantificador se convierte en una cadena de texto.** RN-014 dice *"otra zona de
control posterior a la entrada"*: eso es un existencial, una desigualdad y una comparación temporal.
Sin `liga:` acaban dentro del nombre `otra_zona_de_control_posterior_a_la_entrada`. Y **no es
teórico**: por no tener esa distinción, RN-006 se disparaba sobre el mismo evento que RN-014 y hacía
lo contrario (ADR-0018).

**Y sin acumuladores, el hallazgo más caro de la fase seguiría sin ser mecanizable.** Que agotar los
cartuchos NO acota el día se encontró **a mano**, comparando el reinicio de un acumulador con el
alcance de otro, y vive en las `notas` de RN-020. Con `alcanza_tope_diario: true` como predicado
opaco, una máquina sigue sin poder encontrarlo: `reloj_dia_riesgo`, `base_calculo_perdida_diaria` y
la noción de "acumulada" quedan escondidas dentro del nombre. El problema cambiaría de sitio, que es
exactamente lo que este ejercicio existe para impedir.

## Alternativas consideradas

- **A. Predicado = nombre + booleano** (la D1 original).
- **B. Tabla de decisión**, que es lo que MASTER_PLAN §A nombra literalmente.
- **C. Un cuarto fichero `predicados.yaml`.**
- **D. Escribir un predicado para RN-008** con un nombre convincente.

## Por que elegimos esta opcion

Porque es **la forma mínima que aguanta las ocho reglas duras**, probada contra ellas antes de
escribir código. Y porque mantiene el límite con F22 nítido: F12 valida que el predicado exista, no
se duplique y no se contradiga; **F22 lo implementa**.

Que todo viva dentro de `strategy_spec.yaml` no es cosmética: un cuarto fichero **rompía el contrato
del hash por las dos vías** —`cargar_manifiesto` exige `len(cubre) == 3`, ADR-0013 §5 dice "los TRES
ficheros" y MASTER_PLAN H.2:215 lo repite— y habría obligado a enmendar los dos documentos para
ganar, a cambio, la posibilidad de que alguien hashee solo tres de cuatro. Dentro del fichero, los
predicados entran en el hash **por construcción** y ADR-0013 sigue siendo cierto palabra por palabra.

## Por que descartamos las demas

- **A**: aguanta 1 de 8. Su propio ejemplo canónico viola ADR-0002.
- **B**: la geometría de velas no cabe en columnas booleanas sin meter prosa en las celdas. El plan
  la nombra, y este ADR lo enmienda con su motivo, que es lo que exige MASTER_PLAN §F.
- **C**: ver arriba. Coste alto, beneficio negativo.
- **D**: ~~RN-008 no se puede formalizar: el corpus nunca define qué es un breaker.~~
  **CORREGIDO el mismo día, ver abajo.** Se mantiene el estado `PENDIENTE_DEFINICION` en el
  esquema, porque el caso que describe es real; lo que era falso es que RN-008 fuera ese caso. El glosario dice *"uno de los dos esquemas de entrada; sin él no hay entrada"* —circular—
  y la cita del propio predicado sería `ev-v4-001844-93dcb658`, cuyo literal dice *"el esquema de
  entrada **que ya sabemos cuál es**"*. Un predicado con nombre convincente y definición vacía
  **pasaría las ocho guardias heredadas y `make check` en verde**, porque comprueban PROCEDENCIA, no
  DEFINICIÓN. Por eso existe `PENDIENTE_DEFINICION`: mejor una regla que dice que le falta la
  definición, que un nombre bonito que la tapa.

## Corrección: la definición SÍ estaba en el corpus

Este ADR afirmó que *"el corpus nunca define qué es un breaker"* y marcó RN-008 como
`pendiente_definicion`. **Era un error de búsqueda, señalado por el consultor el mismo día.**

Lo que se comprobó fue el **glosario** —cuya definición era circular— y **una** cita
(`ev-v4-001844`, *"el esquema de entrada que ya sabemos cuál es"*). Lo que no se comprobó fue el
corpus. Y ahí está, repartida en una docena de ítems:

| Ítem | Lo que define |
|---|---|
| `ev-v4-000243-5f8875ce` | los **dos** esquemas: *"o bien directamente rompe el precio […] sólo con velas rojas […] o […] con un pequeño retroceso pequeña zona de control y luego rompe"* |
| `ev-v3-004201-bfeb3734` | el primero no espera retroceso: *"Con el breaker ya me basta […] marco mi orden limit y ya está"* |
| `ev-v3-004230-ed95f336` | el segundo: *"genera como que este da zona de control aquí y luego rompe"* |
| `ev-v3-011653-38c712f3` | el breaker marca el bloque de origen y **no se usa el CHoCH** |
| `ev-v4-005910-d24c0345` | criterio: en M1 vale mecha o cuerpo; **la de M15 tiene que ser cuerpo** |
| `ev-v1-001435-f0586d02` | la zona tiene que ser *"limpia"*, sin ruido |

**La lección, que vale más que la corrección**: toda esta sesión ha ido de que nada afirme más de
lo que su cita sostiene. Afirmar una **ausencia** es una afirmación como cualquier otra, y exige
buscar en la **fuente** —las transcripciones, con `kb find`— y no en el índice. El glosario es un
índice.

Lo que sí queda abierto, y por eso A-21 se reformula en vez de borrarse: **qué es una zona de
control "limpia, sin ruido"**. Es lo único de la geometría de entrada que sigue siendo cualitativo.

## Impacto

- `version_esquema` de `strategy_spec.yaml` sube a **3**.
- **Parámetros que la forma obliga a crear**, porque un criterio escrito a pelo (`criterio: mecha`)
  sería un valor de negocio en un campo ejecutable: `sesgo_h4_criterio_ruptura` (cita
  `fb-…-8eccf5c0`), `zona_control_criterio_completada` (cita `fb-…-a456bc3f`) y
  `break_even_criterio_ruptura`, **que es A-13 y está ABIERTA**: entra `DEFAULT_AMBIGUOUS`.
- `sesgo_h4_regla` (`vela_anterior_cierre_mecha`) mezcla sujeto y criterio en un enum; al escribir el
  predicado se queda sin trabajo o duplica los argumentos. Se resuelve en el piloto.
- **El orden del piloto no cambia** (ADR-0018, D2): RN-003, RN-006, RN-014 y RN-020 primero. Si la
  forma no las aguanta, se cambia habiendo gastado cuatro reglas.

## Fecha / fase

2026-09-10, F12 (revisión de diseño, antes de programar).

## Estado

ACTIVE
