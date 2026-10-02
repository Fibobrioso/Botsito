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

## 2. Fase 1 · El freno, implementado

**Los umbrales**, en `knowledge/spec/parametros.yaml`. Los cuatro son de categoría `ejecucion`,
DEFAULT_AMBIGUOUS bajo **A-54**, `consumido_por: [ADR-0067]` y fuente ADR-0067:

| Parámetro | Valor | Por qué |
|---|---|---|
| `freno_peticiones_aviso` | 1000 | La mitad del límite, y unas 75 veces el día más cargado medido (13 peticiones). Avisa con mucho margen, sin frenar |
| `freno_peticiones_corte` | 1500 | El 75 % del límite. Deja 500 peticiones para lo que protege la cuenta, acotado por `firma_ordenes_simultaneas_max` y las posiciones abiertas |
| `freno_bucle_repeticiones` | 5 | Un día normal no repite una petición: reubicar cambia el precio. Cinco iguales es un bucle |
| `freno_bucle_minutos` | 1 | Cinco iguales en un minuto no las pide ninguna regla, que deciden una vez por cierre de M1 |

Son un margen del proyecto, no una cifra de FTMO, y se revisan con A-54.

**A-54**, ABIERTA, clase `medicion`, no bloqueante, `resuelve_en: [F33]`: qué cuenta FTMO como
petición al servidor, con qué reloj corta el día y qué pasa al pasarse (§0.4). Cita
`ev-v4-012524-0ef85a89` como A-27: el trader sobre operar una cuenta de fondeo con sus límites. No
hay ítem del corpus sobre el límite de peticiones, y su comentario lo dice. Va con su fila en la
tabla «Known Ambiguities» de `PROJECT_STATE.md`. Los cuatro parámetros PROVISIONAL cuelgan de una
ABIERTA, como pide `tests/contract/test_provisional_cuelga_de_abierta.py`.

**El código**:
- `engine/freno.py`, nuevo:
  - `LimitesFreno`, con la validación de los umbrales;
  - `FrenoPeticiones.admitir`, que cuenta y niega;
  - `Corte`, cada entrada del registro;
  - el log a nivel WARNING en el aviso y en cada corte.
- `engine/broker.py`:
  - `ReglasBroker.freno`;
  - el freno armado en `Broker.__init__`. Sin umbrales, en `mensajes_dia_max`, y se niega si el
    corte pasa del límite de la firma;
  - `_admitir`, que llaman los cinco métodos;
  - `Traza.cortes`;
  - `_mover` devuelve si movió.
- `engine/simulacion.py`: `limites_freno_de(registro)` y `reglas_broker_de(perfil, registro=None)`.
  Los scripts que lo llaman sin registro siguen igual, y frenan en el límite de la firma.
- `engine/cableado.py`: pasa el registro, guarda `TrazaBroker.cortes`, y el informe del arnés gana
  la sección «El freno de peticiones» con los umbrales y cada aviso o petición negada por día.
- `docs/adr/0067-…` y su fila en el índice. Spec 15.6.1 → 15.7.0, con `spec docs --escribir`.

**La decisión de §1, aplicada**:
- **lo que protege sale siempre y cuenta**: cancelar, cerrar a mercado y el stop de una posición
  hacia el break even;
- **lo negado no se cuenta**: colocar y modificar una pendiente devuelven `Rechazo` con
  `freno_corte` o `freno_bucle`, y un stop hacia fuera negado deja la posición igual.

**Lo que cambia en un test que ya había.** `test_peticiones.py` fijaba que «nada frena aunque se
pase del límite». Ahora fija lo contrario: sin umbrales del registro, el broker frena en
`mensajes_dia_max`. `test_cableado.py` y `test_preparar_a21.py` arman el motor con
`reglas_broker_de(perfil, registro)`, como el cableado real.

**Plataforma.** Nada de la rama toca hooks, rutas ni el sistema de archivos: no hace falta la CI de
Linux por `fix/`.

## 3. Fase 2 · Los tests, rompiendo la guardia a propósito

`tests/unit/test_freno_peticiones.py`, con los umbrales del registro salvo donde se fija otro corte
para ver el borde:

| Lo que pide el encargo | Test | Lo que mide |
|---|---|---|
| un bucle de 5.000 peticiones no pasa del corte | `test_un_bucle_de_5000_peticiones_distintas_no_pasa_del_corte` | 5.000 compras distintas, una por segundo: salen 1.500 (el corte) y se niegan 3.500, ninguna llega al servidor; un aviso |
| (y el bucle de iguales) | `test_un_bucle_de_5000_peticiones_iguales_lo_para_el_freno_de_bucles` | 5.000 veces la misma compra: salen 4 y el resto se niega por `freno_bucle` |
| | `test_el_bucle_cuenta_las_iguales_aunque_haya_otras_en_medio_y_solo_en_su_ventana` | colocar y cancelar la misma orden alternando es un bucle; las mismas, espaciadas más que la ventana, no |
| al corte, cerrar o cancelar sale | `test_al_llegar_al_corte_cancelar_cerrar_y_el_break_even_salen_y_cuentan` | con el día cortado salen la cancelación, el break even y el cierre, y cuentan |
| el contador vuelve a cero con el día de FTMO | `test_el_contador_vuelve_a_cero_con_el_dia_de_la_firma_no_con_la_sesion` | cruzar las 11:00 de Madrid (09:00Z) no lo vuelve a cero; cruzar la medianoche de Praga (22:00Z en verano), sí |
| | `test_el_dia_lo_da_el_broker_y_el_freno_no_lo_supone` | el freno cambia de día con la fecha que le da el broker |
| ninguna posición sin stop | `test_ninguna_posicion_queda_sin_stop_por_el_freno` | con el día cortado, el stop hacia fuera se niega y la posición conserva el suyo; el break even sale; la orden negada no existe |
| el día normal no toca ningún umbral | `test_el_dia_de_cinco_escenarios_no_toca_ningun_umbral` y `test_un_dia_de_10_a_13_peticiones_no_toca_ningun_umbral` | el día sintético de cinco escenarios (10 peticiones) por el cableado real, y días de 10 y 13: ni aviso ni nada negado |
| | `test_los_umbrales_del_registro_van_por_debajo_de_las_2000_con_margen` y `test_unos_umbrales_sin_sentido_no_arman_el_freno` | los umbrales del registro, y que el broker se niega con un corte por encima del límite de la firma |

**Roto a propósito.** Un script de la carpeta de trabajo hace que el broker deje de preguntar al
freno: cambia `Broker._admitir` en memoria, sin tocar ningún fichero. Con eso corre el fichero de
tests. **Fallan seis**:
- los dos bucles de 5.000;
- el bucle con otras en medio;
- lo que sale al corte;
- el día de la firma;
- ninguna posición sin stop.

Los otros cinco no miden el freno: el día normal (que no corte nada), los umbrales y el freno solo.

**Los días de desarrollo medidos.** Los de agosto (10, 10 y 13 peticiones,
`ESCENARIOS-POR-SESION.md` §6.4) no se volvieron a correr: el umbral más bajo, el aviso, está en
1000. Los representa el test de 10 a 13.

## Estado

EN CURSO: Fases 0, 1 y 2 hechas; falta el revisor.
