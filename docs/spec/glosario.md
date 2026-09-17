<!-- GENERADO por `botsito spec docs`. No editar a mano: `make check` lo comprueba. -->

# Glosario: que es cada cosa

`spec_version 12.0.0` · hash `683748bc94ea…`

11 terminos. Aqui se dice QUE es cada cosa, no que se hace con ella -eso son las reglas- ni con que numero -eso es el registro-.

### breaker

*Tambien: BOS, bos.*

la ruptura que marca el bloque de origen en M1. Es lo que el trader usa para fijar la orden limite, y no usa el CHoCH

Cita `ev-v3-011653-38c712f3`: *«breaker que define cómo se marca el bloque de origen es eso. No uso lo que sería el shot como giro como tal»* · visto en v3 1:16:53

### caja

*Tambien: cuadro de Gann, caja de niveles.*

la distancia entre la entrada y el extremo del stop inicial, dividida en niveles. Es la unidad en la que se miden el objetivo y la proteccion. Dos cosas que esta definicion afirmo hasta el 2026-09-11 y que hoy son falsas: el lote NO se dimensiona sobre la caja entera sino sobre la distancia hasta stop_fraccion_caja (ADR-0020), y el stop NO se mueve despues, sino que se escribe en la orden limite antes de que la entrada se active (A-11, RN-011)

Cita `ev-v2-003336-fc210a05`: *«yo calculo mi lotaje desde aquí, o sea, como si fuera lo básico un bot normal, pero luego automáticamente, se de inicio la entrada»* · visto en v2 0:33:36

### cartucho

*Tambien: intento.*

cada operacion que gasta el cupo. Ni el break even, ni una entrada invalidada, ni la reentrada tras un equal cuentan como uno

Cita `fb-2026-09-09-sesion-01-aa2abe65`: *«un intento no es considerado un break even, ¿vale? una entrada invalidada pues tampoco es considerado un intento [...] reentrada después de equal, tampoco es considerado un intento»* · visto en v6 0:52:19

### cerrar un equal

*Tambien: activacion sin ruptura, equal (la salida).*

el precio activa la orden y la posicion se cierra con lo que el trader llama un equal; se vuelve a entrar y no se gasta intento. En la spec es el cierre de una operacion que se activo sin ruptura (RN-010, RN-019). Esa correspondencia es lectura nuestra de v6 1:22:25-1:23:19, donde el trader describe una entrada activada sin validar que un equal saca con perdida

Cita `fb-2026-09-09-sesion-01-060cd801`: *«Cuando el precio activa tu orden y cierras lo que llamas un equal, vuelves a entrar [...] ¿y gastas tus intentos? Sí, esto no gasta intentos, me dijiste, ¿no? No»* · visto en v6 1:52:26

### equal

*Tambien: equal high, equal low, igual.*

dos extremos al mismo precio. No cambia el sesgo: para cambiarlo hace falta romper el extremo anterior, aunque sea por una milesima. Es GEOMETRIA: la salida que un equal provoca tiene su propio termino, "cerrar un equal", y la spec ya no usa esta palabra como resultado de cierre ni como forma de activarse

Cita `fb-2026-09-09-sesion-01-8eccf5c0`: *«si no genera un rompimiento por encima, o sea, al menos por un pip o una milésima de pip, entonces seguiríamos operando bajista»* · visto en v6 1:03:01

### estructura

*Tambien: dos velas como una.*

como el trader llama a lo que antes describia como "dos velas como una"; el termino lo corrigio el mismo en la sesion 1

Cita `fb-2026-09-09-sesion-01-7ee9cabc`: *«sería considerado una estructura [...] en el lenguaje del bot sería considerado una estructura»* · visto en v6 1:38:48

### flujo de ordenes

*Tambien: order flow, mapeo.*

una de las tres piezas del modelo, junto al breaker y al marco de liquidez; el trader lo usa como sinonimo de mapear el mercado

Cita `ev-v3-000030-94d71563`: *«Un flujo de órdenes, o sea, mapeo del mercado, breaker y marco de liquidez»* · visto en v3 0:00:30

### liquidez de M15

*Tambien: LQ M15.*

el alto o el bajo de M15 que el precio busca. Se da por tomada solo si una vela cierra con CUERPO al otro lado; una mecha que lo perfore no cuenta

Cita `fb-2026-09-09-sesion-01-6e15504f`: *«¿Vale con que la vela cierre con el cuerpo por encima del máximo, por debajo del mínimo, o vale con que la mecha lo perfore? Con cuerpo»* · visto en v6 1:49:21

### primer esquema de entrada

*Tambien: esquema 1.*

el precio rompe directamente, sin retroceso: con el breaker basta para marcar la orden limite

Cita `ev-v3-004201-bfeb3734`: *«Yo no espero ningún retroceso, si se han dado cuenta. Con el breaker ya me basta [...] apenas el breaker, o sea, marco mi orden limit y ya está»* · visto en v3 0:42:01

### segundo esquema de entrada

*Tambien: esquema 2.*

el precio hace un pequeno retroceso que deja una zona de control, y despues rompe

Cita `ev-v4-000243-5f8875ce`: *«si hace el otro esquema pues con un pequeño retroceso pequeña zona de control y luego rompe»* · visto en v4 0:02:43

### zona de control

el tramo que el precio deja antes de romper. Se da por COMPLETADA cuando rompe el punto extremo anterior, y basta con que lo rompa con mecha

Cita `fb-2026-09-09-sesion-01-a456bc3f`: *«como sé que una zona de control se ha completado, cuando apenas me generó un rompimiento [...] rompe el punto alto anterior con mecha, con mecha no importa»* · visto en v6 1:25:36
