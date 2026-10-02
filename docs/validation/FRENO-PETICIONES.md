# FUNCTIONALITY VALIDATION REPORT · Freno de peticiones al servidor

Rama `feature/freno-peticiones`, abierta el 2026-10-02 desde `main` `695041d` (tag
`stable/F36o-cerrar-a29-a36`). Encargo, copiado tal cual: `docs/encargos/feature-freno-peticiones.md`.
Es la K de Next Action. Tarea autónoma: NO se cierra.

Objetivo: que el bot no pueda superar el límite de mensajes al servidor de FTMO, pase lo que pase en
el código que lo llama. Sin cobertura agregada: nada de esta rama cuenta parejas ni compara con las
operaciones del trader.

## 0. Fase 0 · Inventario, antes de escribir código

### 0.1 Quién envía peticiones hoy

**Las siete reglas** (medido en `feature/escenarios-por-sesion`, `ESCENARIOS-POR-SESION.md` §6.4): las
vigentes cuya forma ejecutable llama a una acción que acaba en el broker.

| Regla | Acción (`engine/primitivas_broker.py`) | Petición |
|---|---|---|
| RN-002 | `cerrar_a_mercado` | cerrar |
| RN-030 | `cerrar_a_mercado` | cerrar |
| RN-004 | `abrir_escenario` (con `orden_pendiente_al_abrir_escenario` = `se_retira`) | cancelar |
| RN-006 | `reubicar_orden_limite` | cancelar (o modificar, si la orden no nace en el punto) |
| RN-014 | `mover_stop` | modificar (el stop de una posición) |
| RN-015 | `colocar_orden_limite` | colocar (límite o stop) |
| RN-035 | `retirar_orden_limite` | cancelar |

**Y dos que no son reglas:**
- **el propio broker**, que mueve el stop al break even al tick (ADR-0065, `_mover`) y lo apunta como
  `modificar`;
- **el cableado**, que al cerrar la ventana del día cierra a mercado lo que quede abierto y cancela
  lo pendiente (`engine/cableado.py`, fin del día).

**Todas pasan por cinco métodos del broker**: `_colocar` (colocar límite o stop), `modificar`,
`cancelar`, `cerrar_a_mercado` y `_mover` (`engine/broker.py`). Es el único sitio por el que una
petición llega al servidor, y ahí vive el contador.

### 0.2 Qué cuenta hoy el contador

`Broker._peticiones` (rama `feature/contador-peticiones`; cabecera de `engine/broker.py`): una
`Peticion(instante_ms, tipo, id, aceptada)` por cada colocar, modificar (una pendiente o el stop de
una posición), cancelar y cerrar a mercado, **aceptada o rechazada**: la lectura más estricta de
«server requests». No cuenta lo que el servidor hace solo -llenar, expirar, saltar el stop o el
objetivo-, ni `abrir_conocida`, que repite una operación del trader y no la emite el bot. Una
petición que el broker no admite (`BrokerError`) no se apunta: es un error de quien llama.

**Solo mide.** `ReglasBroker.mensajes_dia_max` (2.000, de `firma_mensajes_dia_max`) se imprime al lado
del recuento en el informe del arnés (`_informe_peticiones`) y **nada frena**.

### 0.3 En qué reloj cambia el día

En el de la firma, no en el de las sesiones. `peticiones_por_dia` agrupa por
`_dia_local(instante, huso_corte)`, y `huso_corte` es `perfil.huso_corte()`, o sea
`firma_huso_corte` del perfil de cuenta (`engine/perfil_cuenta.py`): el reloj con que la firma corta
el día, el mismo del día de riesgo (ADR-0027). ADR-0063 separó de él el reloj de las sesiones
(`reloj_sesiones`), que dice cuándo abre y cierra la ventana y no toca el corte del día.

### 0.4 Qué cuenta FTMO como mensaje: lo que consta y lo que no

**Lo que consta** (`docs/validation/FTMO-REGLAS.md`, R13):
- «an excessive number of more than 2,000 server requests per day» (Forbidden Trading Practices),
  que es `firma_mensajes_dia_max` = 2.000;
- y otra FAQ: «200 orders at a time and 2000 max positions per day limitation, just as the limited
  acceptance of the server messages».

**Lo que NO consta, y queda PENDIENTE DE LA DEMO** (o del soporte de FTMO), sin suponerlo:
- **qué es una «server request»**: si cuenta una petición rechazada, una modificación del stop, una
  cancelación o un cierre;
- **con qué reloj corta FTMO ese día** para este límite: se supone el de `firma_huso_corte`, el
  mismo del día de riesgo, pero R13 no lo dice;
- **qué pasa al pasarse**: R13 lo llama práctica prohibida, sin decir si el servidor rechaza
  (MetaTrader tiene su propio código, `10024 TOO_MANY_REQUESTS`).

La demo (ADR-0057, `tools/mql5/MedirDemoFTMO.mq5`) **no lo mide**: solo traduce el código 10024 si
sale, con una pausa de 1,5 s entre peticiones, y no cuenta peticiones ni toca el límite. Hasta que
se mida, el freno cuenta como el contador: **todas, aceptadas o rechazadas, y también las que
protegen la cuenta**. Es la lectura que más pronto corta.

## 1. El diseño (escrito antes de implementar)

**Dónde vive.** En el puerto: dentro de los cinco métodos del broker de §0.1, antes de apuntar la
petición. Una regla de la estrategia no llama al servidor: llama a una acción, que llama al broker,
y el broker pregunta al freno. Ninguna regla puede saltárselo. El freno es una clase aparte, sin IO
ni reloj propio (`engine/freno.py`), para que el adaptador real de MetaTrader use la misma.

**Los umbrales, en el registro (ADR-0002)**, de categoría `ejecucion` (una decisión de margen del
proyecto, no un hecho de la firma). Todos DEFAULT_AMBIGUOUS bajo una ambigüedad nueva y ABIERTA,
**A-54** (qué cuenta FTMO como mensaje y con qué margen se frena; clase `medicion`):
- `freno_peticiones_aviso`: el día que llega aquí, se apunta un aviso en el log. No frena;
- `freno_peticiones_corte`: desde aquí, ese día no sale nada que no proteja la cuenta;
- `freno_bucle_repeticiones` y `freno_bucle_minutos`: N peticiones IGUALES dentro de esa ventana
  cortan el envío el resto del día.

Los valores, en §2, con su motivo.

**Qué protege la cuenta, y pasa siempre**:
- **cancelar** una pendiente: quita exposición;
- **cerrar** a mercado una posición;
- **mover el stop de una posición viva hacia el lado que reduce el riesgo**: el break even. Lo
  incluyo aunque la orden diga «cerrar o cancelar», porque negarlo deja la posición con más riesgo
  del que la regla del trader quiere (RN-014), y no puede repetirse: el stop solo sube una vez.

Un stop que se alejara del precio no protege y se frena.

**Las que protegen CUENTAN para el límite.** FTMO no dice que no sean «server requests» (§0.4), así
que se cuentan, y el corte deja hueco para ellas. Lo que no hacen es frenarse: un freno que
impidiera cerrar o cancelar dejaría la cuenta peor que pasarse del límite.

**Nunca queda una posición sin stop por el freno.** El stop viaja en la orden (A-11): colocar ya
lleva el stop, y el broker no admite una orden sin él (`_colocar`). Lo que el freno niega no crea
nada: una orden negada no llega a existir y no se llena. El freno nunca quita ni aleja un stop. Lo
único que puede negar sobre una posición es alejar su stop, y eso no la deja sin él.

**Qué hace al negar.**
- Colocar y modificar una pendiente devuelven un `Rechazo` con motivo `freno_corte` o
  `freno_bucle`, como el broker devuelve un rechazo del servidor. Quien llama ya sabe tratarlo: el
  cableado marca la zona como rechazada.
- Mover el stop hacia fuera devuelve la posición sin tocar.
- **No es una petición**: no llega al servidor y no se cuenta.

Todo corte, cada aviso y cada petición negada quedan en la traza del broker
(`Traza.cortes`, con instante, tipo, id y motivo) y en el log (`logging`, nivel WARNING). El informe
del arnés los imprime por día junto al recuento.

**Peticiones iguales** (el freno contra bucles):
- colocar con el mismo lado, precio, stop, objetivo y lote;
- o modificar la misma orden a los mismos precios.

No importa el id: un bucle que cancela y vuelve a colocar la misma orden con id nuevo cada vez es
el caso que busca. «Seguidas en poco tiempo» se lee como N dentro de la ventana, aunque haya otras
en medio: la reubicación alterna cancelar y colocar, y con «consecutivas» no se vería nunca. Las
que protegen no entran: no pueden repetirse sobre el mismo objeto.

**El día del freno** es el de §0.3: cambia a medianoche en `huso_corte`, y entonces todo vuelve a
cero, incluido un corte por bucle.

**Construcción.** `ReglasBroker` gana `freno: LimitesFreno | None`.
- `reglas_broker_de(perfil, registro)` lo lee del registro cuando se le pasa el registro, y el
  cableado se lo pasa siempre.
- Si quien construye el broker no trae umbrales (un script o un test que arma `ReglasBroker` a
  mano), el broker frena igual en `mensajes_dia_max`, el límite de la firma, sin margen ni aviso:
  **ningún camino deja el broker sin freno si el perfil dice el límite.**
- Sin `mensajes_dia_max` (los tests del broker puro, que no tienen firma) no hay límite que
  defender.

## Estado

EN CURSO: Fase 0 escrita (inventario y diseño). Fase 1 y 2, pendientes.
