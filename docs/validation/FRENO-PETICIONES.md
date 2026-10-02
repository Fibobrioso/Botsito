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
  acceptance of the server messages». Son OTROS dos límites, de órdenes a la vez y de posiciones
  al día, que no son el de peticiones; FTMO-REGLAS.md dice que el repo no los recoge
  (`firma_mensajes_dia_max` solo es el de peticiones), y este freno tampoco (revisor, a4).

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
  del que la regla del trader quiere (RN-014). **Solo el PRIMER movimiento** (corregido tras el
  revisor, b1: en `652c75b` valía cualquiera, y un bucle de subidas no se frenaba). Así cada cosa
  que protege se da una vez por orden o posición, y su número está acotado.

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
(`Traza.cortes`, con instante, tipo, id y motivo) y en el log: el aviso y el corte a nivel WARNING,
cada negada a nivel INFO (corregido tras el revisor, a3). El informe
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
| (tras el revisor, §4) | `test_un_bucle_que_sube_el_stop_no_se_cuela_por_lo_que_protege` | 5.000 subidas del stop con el día cortado: sale la primera, se niegan 4.999 |
| | `test_modificar_una_pendiente_negada_la_deja_como_estaba`, `test_el_break_even_al_tick_sale_con_el_dia_cortado`, `test_el_log_dice_el_corte_con_su_motivo_y_cada_negada` y `test_el_dia_y_los_umbrales_salen_del_perfil_y_del_registro` | la pendiente negada no cambia; el break even al tick sale con el día cortado; el log; el reloj sale del perfil |

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

## 4. Informe del revisor

Subagente `revisor`, sobre `91b3291`, `ab1367f` y `652c75b`. Los hallazgos, tal cual; lo
comprobado sin hallazgos, resumido.

> ## Informe del revisor · feature/freno-peticiones · 2026-10-02
>
> ### Eje (a) · Reglas de la casa
> Resumen: 0 bloquea, 3 importa, 1 menor.
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | a1 | importa | La evidencia que cita A-54 no sostiene la ambigüedad. `ev-v4-012524-0ef85a89` trata de que el trader elige FundedNext con un 5 % diario y un 8 % total. No dice nada de FTMO, de peticiones ni de mensajes al servidor. El comentario de A-54 lo admite a medias («ningún ítem del corpus habla del límite») y la cita va «como en A-27». Es una cita de relleno para cumplir el esquema. | `knowledge/evidence/v4/ev-v4-012524-0ef85a89.yaml`; `knowledge/spec/ambiguedades.yaml:1508-1509`. |
> | a2 | importa | Dos afirmaciones son falsas para `mover_stop`, y dos documentos las repiten. (1) Informe §1: lo que protege «no puede repetirse: el stop solo sube una vez». (2) `parametros.yaml`, descripción de `freno_peticiones_corte`: el hueco para lo que protege «está acotado por firma_ordenes_simultaneas_max y las posiciones abiertas». `Broker.mover_stop` es público y cada subida de un punto del stop pasa como «protege», sin límite. Ver b1. | `docs/validation/FRENO-PETICIONES.md` §1; `knowledge/spec/parametros.yaml`; `src/botsito/engine/broker.py:543-551` (`protege = stop > p.stop`). |
> | a3 | importa | El ADR y el informe dicen que «cada petición negada» queda en el log (WARNING). El código solo registra en el log el primer corte del día (`_cortar`) y el aviso (`_contar`). Cada negada posterior solo va a `Traza.cortes`, sin `LOG`. No hay ningún test con `caplog`, así que el log no está probado. | `src/botsito/engine/freno.py`; `docs/adr/0067-…md` §6. |
> | a4 | menor | Dos erratas de forma. (1) El informe §0.4 cita «otra FAQ» de R13 con «2000 max positions per day», que es un límite distinto del de peticiones, y no lo distingue. (2) La fila 0067 del índice ADR queda colocada antes de la 0037. Se heredó ya antes con la 0066, así que no es de esta rama. | `docs/adr/README.md` (diff); `docs/validation/FTMO-REGLAS.md:60`. |
>
> Comprobado sin hallazgos: el contrato (22 ficheros, ninguno protegido); `state check`, `spec check` y `knowledge validate`; el `Fuente:` de `652c75b` (los ids existen); A-54 ABIERTA, `medicion`, no bloqueante, con sus cuatro parámetros, su doc generado y su fila en `PROJECT_STATE.md`; los cuatro DEFAULT_AMBIGUOUS bajo A-54 y `test_provisional_cuelga_de_abierta.py`; `test_no_business_literals`; spec 15.7.0 y los docs generados; ADR-0067 y `test_adr.py`; `PROJECT_STATE.md` 22.904 bytes y la K sin mover a HISTORIA; los regímenes de cambio; la Fase 0 contra el repo (las siete reglas, los días 10/10/13, R13, `MedirDemoFTMO.mq5` solo traduce 10024, lo que no consta queda pendiente); la Fase 0 commiteada antes que el código; nada de plataforma.
>
> ### Eje (b) · Encargo
> Resumen: 0 bloquea, 2 importa, 2 menor. Requisitos: 15 hechos, 1 parcial (el log de cada corte, a3), 0 no hechos.
>
> Rompiendo el freno en memoria (`Broker._admitir` parcheado), fallan las seis que dice el informe. Negada no cuenta y la que protege sí.
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | b1 | importa | **«Protege la cuenta» deja colar un bucle ilimitado de `mover_stop`.** `_mover` pone `protege=True` a cualquier stop que mejore el actual (`stop > p.stop` en una larga). Las protegidas no pasan ni por el corte ni por el bucle. Un bucle que suba el stop un punto cada vez (stops distintos, así que `bucle` tampoco lo ve) no se frena nunca, y lo medí. Esto contradice el objetivo del encargo («no pueda superar… pase lo que pase en el código que lo llama»). El encargo solo exceptúa «cerrar o cancelar»; el broche del stop lo añade la rama, lo declara y lo justifica con una premisa falsa (a2). Arreglo posible: un tope duro para las protegidas, o dejar pasar el stop solo si es el primer movimiento (`stop_original is None`). | En memoria: `_broker(LimitesFreno(corte=3))`, tres colocar, y 5.000 llamadas a `b.mover_stop(pos.id, BID-5000+1+k, …)` dan «cortado None, total tras 5000 trailing 5003, peticiones 5003, cortes 0». |
> | b2 | importa | **Los scripts con `reglas_broker_de(perfil)` sin registro caen al límite de la firma en crudo, y las protegidas pueden pasarlo.** Sin umbrales, `Broker.__init__` arma `LimitesFreno(corte=mensajes_dia_max)`, o sea corte = 2.000, sin aviso ni bucle. Las protegidas siguen pasando por encima. «Más de 2.000» es la práctica prohibida, así que ese camino no deja margen. Afecta a `scripts/repeticion_trader.py:80`, `scripts/viabilidad_trader.py:242` y `tests/regression/test_cuenta_7_de_agosto.py:61`. Por su volumen hoy no llegan a 2.000, así que es teórico. | `src/botsito/engine/simulacion.py:99-117`; `broker.py:__init__`. |
> | b3 | menor | Una colocación negada no se guarda en `broker.ordenes` ni en `_rechazos`, y el cableado asigna id con `f"o{len(ctx.broker.ordenes)+1}"`. Varias negadas seguidas repiten id en `Traza.cortes` y en los eventos «rechazo». No rompe nada, pero hace menos legible el rastro. Además `tb.rechazos` no incluye las negadas por el freno, mientras el cableado emite el evento «rechazo» y marca la zona como rechazada. | `src/botsito/engine/primitivas_broker.py:511,521-524`; `broker.py:_colocar`. |
> | b4 | menor | Huecos de test. No hay test de `modificar` negado de una pendiente, ni de `_aplicar`/el break even al tick bajo corte, ni de fin de día del cableado bajo corte, ni de log (`caplog`). El «día de la firma» se prueba con Praga puesto a mano en `ReglasBroker`, no leyéndolo del perfil. | `tests/unit/test_freno_peticiones.py`. |
>
> ### Lo que no pude comprobar
> `make check` y su `SELLO` (escribe; no hay `make-check.log`); la CI de Linux (no hace falta); `spec docs --check` (no existe el flag); el recuento 1177 (su `grep` da 1178; `state check` lo acepta); la cobertura, no calculada.

**Respuesta de la sesión, hallazgo a hallazgo:**
- **b1 y a2, arreglados: el agujero era real.**
  - **Qué cambia:** protege solo el PRIMER movimiento del stop hacia dentro (`p.stop_original is
    None`), que es el break even de RN-014. Los siguientes se frenan como lo demás (`_mover`). Así
    cada cosa que protege se da una vez por orden o posición, y lo de §1 y de la descripción de
    `freno_peticiones_corte` pasa a ser verdad.
  - **Test nuevo:** `test_un_bucle_que_sube_el_stop_no_se_cuela_por_lo_que_protege`, el mismo bucle
    del revisor. Con el día cortado, de 5.000 subidas sale la primera y se niegan 4.999. En
    `652c75b` salían las 5.000.
- **a3, arreglado:** cada petición negada va también al log, a nivel INFO, con su motivo. El aviso
  y el corte siguen en WARNING. Corregidos el ADR §6 y el informe §1, y hay test con `caplog`:
  `test_el_log_dice_el_corte_con_su_motivo_y_cada_negada`.
- **b4, arreglado en lo que importa.** Tests nuevos:
  - `test_modificar_una_pendiente_negada_la_deja_como_estaba`;
  - `test_el_break_even_al_tick_sale_con_el_dia_cortado` (`_aplicar`);
  - `test_el_dia_y_los_umbrales_salen_del_perfil_y_del_registro`: Praga sale de `firma_huso_corte`
    del perfil de FTMO, y los umbrales del registro.

  El fin de día del cableado bajo corte no lleva test propio: llama a `cerrar_a_mercado` y
  `cancelar`, que ya prueba `test_al_llegar_al_corte_…`.
- **a4, arreglado en lo de esta rama:** §0.4 dice que «200 orders at a time» y «2000 max positions
  per day» son otros dos límites, que el freno no recoge. El orden del índice de ADR viene de antes
  y no se toca.
- **a1, declarado; lo decide el consultor.** Es verdad: ningún ítem del corpus habla del límite de
  peticiones, y el esquema exige al menos uno (`cases/ambiguedades.py`: «una ambiguedad cita al
  menos un item de evidencia»). Se siguió el precedente de A-27, y el comentario de A-54 lo dice.
  Hay dos salidas, y las dos son de otra rama: que el esquema admita una ambigüedad de la firma sin
  evidencia del corpus, citando su fuente (FTMO-REGLAS R13), o dejarlo así.
- **b2, declarado.** Sin umbrales del registro el broker frena en el límite de la firma, sin margen.
  Lo que protege puede pasar de 2.000 por pocas: ahora, con b1, son a lo sumo una cancelación, un
  cierre y un break even por orden o posición. Solo lo usan dos scripts de análisis que no operan
  y un test de regresión. Operar en una cuenta real pasa por el cableado, que siempre trae los
  umbrales. Cerrarlo del todo es exigir el registro en `reglas_broker_de`, y eso toca `scripts/`,
  que no está en el contrato.
- **b3, declarado.** Una colocación negada no existe en `broker.ordenes`, y por eso el id se puede
  repetir en la traza. Es a propósito, porque nunca llegó al servidor. `tb.rechazos` cuenta los
  rechazos del servidor; los del freno están en `tb.cortes` y en su sección del informe.
- **El recuento 1177 frente a 1178 del `grep`:** `state check` cuenta a su manera y da OK. Con los
  cinco tests nuevos son 1182.

## 5. Orden de cierre del consultor: lo que entra antes de cerrar (2026-10-02)

**a) Lo que protege, tras el corte por BUCLE: faltaba el test.** El código ya lo hacía: en
`FrenoPeticiones.admitir` lo que protege sale antes de mirar el corte, sea diario o por bucle. Pero
ningún test lo probaba. Los dos tests de bucle solo miraban lo negado, y lo que protege solo se
probaba tras el corte diario. Test nuevo,
`test_tras_el_corte_por_bucle_cancelar_cerrar_y_el_break_even_salen_y_cuentan`:
- cinco compras iguales cortan el día por bucle;
- después salen y cuentan la cancelación de la pendiente, el primer stop a break even y el cierre;
- una compra nueva sigue negada por `freno_bucle`.

**Roto a propósito**, en memoria, con un freno que niega también lo que protege cuando el corte es
por bucle: el test nuevo FALLA, y el del corte diario (`test_al_llegar_al_corte_…`) sigue pasando.
Es decir, el test que había no lo habría visto.

**b) A-54 dice de dónde sale.** Su `pregunta` dice que la cita de evidencia es de relleno porque el
esquema exige una, que ningún ítem del corpus habla del límite y que la fuente real es
`docs/validation/FTMO-REGLAS.md` R13. `spec docs --escribir` en el mismo commit. Technical Debt
suma la línea de la orden: el esquema exige una cita de evidencia aunque la fuente sea una regla de
FTMO (A-27, A-54).

**c) Lo que cuenta FTMO como mensaje** -las rechazadas, las modificaciones, las cancelaciones- está
pendiente de la **respuesta del soporte de FTMO, que pide Aleks**. Si cuenta más de lo que cuenta
el freno, los umbrales se revisan. Lo dice A-54 en su `pregunta`, y completa lo de §0.4.

**PROJECT_STATE.md** (`wc -c`): la línea nueva de Technical Debt habría llevado el fichero por
encima de 23.000 bytes. Para dejarle sitio, la línea de `Current Feature` de esta rama se acorta.
Esa línea se sustituye al cerrar.

## Estado

**Rama lista para revisión, NO cerrada.** Tarea autónoma: no se cierra.
- Fase 0 (inventario y diseño, commiteada antes del código), Fase 1 (el freno en el puerto) y
  Fase 2 (los tests, rotos a propósito) hechas.
- El revisor está pasado, y el agujero que encontró (b1) está cerrado y probado.
- Para el consultor:
  - la evidencia de A-54 (a1);
  - el freno sin umbrales en los scripts (b2);
  - los umbrales PROVISIONAL, con A-54, en la demo de FTMO.
- La K de Next Action sigue en `PROJECT_STATE.md` hasta el cierre.
