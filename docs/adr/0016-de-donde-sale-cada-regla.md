---
status: ACTIVE
date: 2026-09-10
phase: F11
---

# 0016 · De donde sale cada regla: el campo `decision`, y un hash que cubre lo que un humano lee

## Decision

1. **Campo `decision` (opcional, `ADR-NNNN`) en las reglas** de `strategy_spec.yaml`.
2. **Es OBLIGATORIO cuando la regla opera sobre un parametro de entorno**, es decir uno cuya
   `fuente` es `decision` y no `feedback`/`evidence`. `knowledge validate` lo comprueba.
3. **RN-026** (abstenerse si el broker no admite el stop) y **RN-027** (redondear el lotaje a la
   baja) declaran `decision: ADR-0016`: las dos son decisiones nuestras y este ADR las sostiene.
   **RN-020** declara `ADR-0015`, por `reloj_dia_riesgo`.
4. **El hash de la spec cubre tambien `titulo`, `literal`, `notas` y `decision`** de cada regla, y
   el `literal` de cada termino del glosario.

## Problema que resuelve

La verificacion de literales comprueba que el `literal` de una regla **este de verdad en su cita**.
Lo que no comprueba -ni puede, en general- es que la regla no diga **mas** de lo que su literal
sostiene. Dos reglas reales lo demostraban:

| Regla | Lo que decide | Lo que dice su literal |
|---|---|---|
| RN-026 | si el stop cae dentro de `instrumento_stops_level`, no se abre la operacion | *"Que sea fiel a la operativa y no busque nada adicional."* |
| RN-027 | el lote se redondea al escalon del broker, **siempre a la baja** | *"El lotaje se pone sobre la caja completa de SL, pero automaticamente se mueve al 0.8..."* |

Las dos pasaban la comprobacion, porque sus literales existen en sus citas. Las dos son decisiones
de ingenieria correctas y ninguna la dijo el trader. Presentadas asi, un lector futuro las lee como
palabra del trader y no las revisa.

Y el **hash** cubria de cada regla solo `id`, `cuando`, `entonces`, `parametros`, `cita` y `estado`.
O sea: la correccion de riesgo mas importante de toda la fase -que el tope porcentual del 4,5 % es
el unico freno del dia que existe, y no una red que nunca se toca- vivia **solo en las `notas` de
RN-020** y se podia borrar sin que `spec_version` se moviera. En la misma regla, el `titulo` decia
literalmente lo contrario que esas notas, y nada lo veia.

## Alternativas consideradas

- **A. Exigir a mano una revision de cada regla** contra su literal, sin mecanizar nada.
- **B. Prohibir que una regla nombre parametros de entorno**, moviendolos a otra capa.
- **C. Dejar el hash como estaba**, argumentando que `titulo` y `notas` no los ejecuta el motor.
- **D. Hashear los BYTES** de los tres ficheros, y acabar con la discusion.

## Por que elegimos esta opcion

Porque **el caso que importa si es mecanizable**. No se puede decidir por programa si una frase en
español dice mas que otra, pero si se puede detectar la señal que acompaña a ese fallo: una regla
construida sobre parametros que **no dijo el trader** esta decidiendo por su cuenta. La guardia
encontro las dos reglas conocidas en su primera ejecucion, y ademas RN-020, que acababa de heredar
el mismo problema al ganar `reloj_dia_riesgo`.

Y sobre el hash: `titulo` y `notas` no los ejecuta el motor, pero **son lo que lee la persona que
valida**. Si el proposito del hash es que un backtest pueda decir contra que spec corrio, y la spec
es tambien lo que un humano aprueba, entonces el texto que ese humano lee es parte del contrato.

## Por que descartamos las demas

- **A**: es lo que habia. Falló: la auditoria de cierre reviso el glosario, encontro ocho
  definiciones que decian mas que su cita, las corrigio, **y no miro las reglas con el mismo
  criterio**. Una revision que depende de acordarse no es una guardia.
- **B**: el motor tiene que saber el escalon del lote y el stops level. Sacarlos de las reglas los
  esconderia en el codigo, que es peor.
- **C**: el argumento se cae con el ejemplo: la frase mas cara de la fase estaba en unas `notas`.
- **D**: ya se descarto en ADR-0013 y sigue en pie: reordenar un comentario cambiaria la version de
  la spec sin cambiar la spec.

## Que sustituye de otros ADR

**Amplia ADR-0013** en dos puntos -el esquema de la regla gana un campo, y el alcance del hash
crece- sin tocar sus decisiones. El hash sigue siendo sobre la estructura re-serializada y sobre
los tres ficheros.

## Impacto

- Cualquier regla nueva que use la ficha del instrumento, el reloj del broker o la cuenta tendra
  que decir en que ADR se decide. El coste es una linea; el beneficio es que nadie vuelva a leer
  una decision nuestra como palabra del trader.
- El hash cambia para toda la spec. `spec_version` sube a 2.0.0: RN-020 cambia de **titulo y de
  sentido declarado** -de "son una red, no el freno" a "es el unico freno del dia"-, y la politica
  de ADR-0013 dice mayor cuando una regla cambia de sentido.
- **Deuda anotada**: `instrumento_stops_level` vale 0, medido contra la demo, asi que RN-026 hoy no
  llega a activarse nunca. Hay que volver a medirlo en la cuenta fondeada antes de F33.

## Fecha / fase

2026-09-10, F11 (auditoria previa a la validacion).

## Estado

ACTIVE
