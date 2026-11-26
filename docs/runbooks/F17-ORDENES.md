# La medida de las órdenes stop y el grabador de ticks de la demo de FTMO (F17, segunda parte)

Para Aleks, en las pruebas gratuitas de FTMO que se activen después (otras ramas). Dos scripts de
MetaTrader 5: **`tools/mql5/MedirOrdenesFTMO.mq5`** (versión 1.0) coloca órdenes stop en la DEMO y
registra cada entrada stop, cada cierre por stop y cada cierre a mercado con los ticks del servidor;
**`tools/mql5/GrabarTicksFTMO.mq5`** (versión 1.0) graba los ticks de EURUSD, una hora por fichero.
El repositorio los lee con el criterio escrito antes de cualquier llenado
(`docs/plan/F17-ORDENES.yaml`): el deslizamiento por clase (ADR-0092 §4, ADR-0099 §5) y el spread
de FTMO por hora. **No cambia nada de la estrategia ni de los parámetros**: `deslizamiento` sigue en
`pendiente_F17` hasta que el ADR que resuelva C, o la rama que lea la medida, diga cómo entra.
Rama: `trabajo/f17-ordenes`; el historial, en `docs/runbooks/F17-HISTORIAL.md`.

## Antes de nada: la pregunta a FTMO

**La medida no se lanza hasta que FTMO conteste** al correo de Aleks del 2026-11-26 (si la prueba
gratuita ejecuta como el Challenge y la cuenta real, P4-08; y si medir con un guion propio, con 1 lote
y unos 25, es práctica prohibida, hiperactividad o afecta a un Challenge futuro: R13, R16 y R17;
el correo, en `docs/validation/F17-ORDENES.md`). El historial y el grabador sí, porque solo leen. Si
la respuesta dice que mezclar los dos tamaños incumple R17, se hace un estrato por prueba; si dice
que la medida está prohibida, no se corre. En los dos casos, PARADA al consultor en la rama de la
prueba. La respuesta entra parafraseada, nunca literal.

## Las pruebas

Cada prueba gratuita dura 14 días y solo puede haber una activa. Lo que hace falta (D3): **100
muestras por clase en el estrato «uno»** (1,00 lote) y **30 por clase en el «bot»** (el lote de
ADR-0081 D2, unos 25); si la mediana «bot» pasa a la «uno» en 1 punto o más, el lote importa y hacen
falta 100 «bot» por clase. Cada ciclo da una entrada y una salida (por stop, o a mercado a los 300
s), así que los ciclos son las muestras de la clase más escasa entre las dos salidas.

- **La primera prueba**: el historial primero (`F17-HISTORIAL.md`), luego el grabador en marcha todo
  el tiempo, y la medida: «uno» entero (unos 250 ciclos, unos 3 días de ventana) y lo que quepa de
  «bot».
- **Las siguientes**: «bot» hasta sus 30 por clase. **Cuántas, no está medido**, y el plan se rehace
  con lo que mida la primera (la fracción de ciclos que salen por stop y el coste por ciclo). Las dos
  estimaciones, las dos SUPUESTOS (F17-ORDENES.md, 0.4 y el auditor):
  - con el supuesto de martingala (el coste esperado de un ciclo «bot» es la comisión, el spread y el
    deslizamiento, 150-200 USD): una prueba más para «bot», dos con margen; seis o siete más si el
    lote importa;
  - con la del auditor (unos 20 ciclos «bot» por prueba, contando unos 575 USD por un ciclo que sale
    por stop y unos 175 por uno a mercado): unas tres pruebas para «bot»; unas diez si el lote importa.

## Lo que hacen, y lo que no hacen nunca

**MedirOrdenesFTMO** (`tests/contract/test_medir_ordenes_ftmo.py`):

- **se niega a correr si la cuenta no es DEMO**, antes de cualquier petición, con la condición de
  `MedirDemoFTMO.mq5`; y si el capital del historial no es el de la prueba (100.000);
- **solo EURUSD y su número mágico** (57057100, que no es el de `MedirDemoFTMO`); la limpieza solo
  toca lo suyo;
- **un ciclo cada vez**, alternando compra y venta: una orden stop a 5 puntos del precio, con su stop
  a 18 puntos en la orden (y un objetivo lejano de respaldo, por si el script muere) y caducidad; si
  no se llena en 120 s se borra; si se llena, sale por su stop o, a los 300 s, a mercado;
- tras cada llenado, espera 5 s y guarda los ticks del servidor desde que se puso hasta que se llenó;
- al empezar, tras cada ciclo y al terminar, borra lo suyo y comprueba que no queda nada.

**Los topes**, cada uno leído de la cuenta y de su historial, así que valen igual si se relanza el
mismo día. Son constantes del script; un test exige que sean estos:

| tope | valor | qué hace |
|---|---|---|
| (a) peor caso de todo lo vivo, compras y ventas | 1.000 USD | si con el lote del estrato no cabe, se baja el lote hasta que quepa; si ninguno cabe, para |
| (b) pérdida del día de riesgo | 3.000 USD | para si la equity de la cuenta baja del saldo al empezar el día menos esto |
| (c) pérdida total | 8.000 USD | para si la equity baja del capital inicial menos esto |
| (d) peticiones de trading del día | 500 | las cuenta del historial y de sus propios CSV del día (las rechazadas) |
| pausa entre peticiones | 1.500 ms | fija, no es una entrada |
| (e) margen hasta el cierre de la sesión | 150 min | no coloca nada más cerca del fin de la sesión de hoy |
| ventana muerta | de 22 a 3 h del servidor | ni coloca ni tiene nada: así el saldo a las 00:00 del servidor es el de las 00:00 de España |

**Los topes (b) y (c) son de la cuenta entera**, como los cuenta FTMO: **mientras corre la medida, en
esa cuenta no opera nada más** (el exportador y el grabador solo leen). Las 2 h 30 min de (e) son un
margen nuestro, no de R15 (que habla de dos horas o menos antes de un cierre de al menos dos), y las
sesiones de MetaTrader no traen los festivos (ADR-0068, «Alternativas», 2): **no se lanza la medida
un día con un cierre anunciado por FTMO, ni el día hábil anterior**.

**GrabarTicksFTMO** (`tests/contract/test_grabar_ticks_ftmo.py`):

- **no opera**: no llama a ninguna función de órdenes ni de posiciones; no necesita *Algo Trading*;
- se niega fuera de DEMO; solo EURUSD;
- graba en bucle, una hora del servidor por fichero, escrito primero en `.part` y renombrado al
  cerrar la hora, así que un `.csv` está siempre entero.

Lo que no se sabe de MetaTrader se mide con lo que sale (ADR-0082 D7): en qué huso van las sesiones
(la capa las da por servidor), si una petición rechazada entra en el historial, si a los 5 s el
terminal tiene todos los ticks del llenado y hasta dónde guarda el servidor los ticks hacia atrás.

## Una vez: compilarlos e instalarlos

La guardia de Claude Code no deja a la sesión lanzar MetaEditor con un guion cambiado en la rama:
lo lanzas tú, con el comando exacto que te da el consultor tras revisar el diff, desde la raíz del
repositorio (una línea `!`), sobre los ficheros commiteados (tienen que estar en el índice de git):

    uv run python src/botsito/mql5bridge/compilar.py herramienta --repo . --metaeditor "<ruta de MetaEditor64.exe>" --salida docs/validation/anexos/F17-ORDENES --instalar "<carpeta de datos del terminal>" tools/mql5/MedirOrdenesFTMO.mq5 tools/mql5/GrabarTicksFTMO.mq5

El log tiene que decir **0 errors, 0 warnings** para los dos. El `.ex5` no entra en git.

## Cada vez: el grabador

1. Un gráfico de EURUSD. **Ver → Navegador → Scripts → Botsito**, arrastra **GrabarTicksFTMO**.
   No tiene entradas.
2. **Déjalo corriendo** toda la prueba. Para pararlo, quítalo del gráfico: la hora en curso queda en
   `.part`.
3. **Si el terminal se cierra o se reinicia, el grabador no vuelve solo** (un script no se recarga;
   un servicio sí, pero `compilar.py` solo instala scripts): **relánzalo** igual. Al relanzarlo
   borra el `.part` y rehace del servidor, hora a hora, desde la siguiente al último `.csv` entero;
   lo que el servidor ya no guarde sale en el control como **HUECO** (`rehecha_<hora>_ticks` 0).
4. La primera vez empieza al inicio de la hora en que lo lanzas, nunca antes.

## Cada vez: la medida

1. **Solo cuando FTMO haya contestado** (arriba), en un día hábil sin cierre anunciado ni víspera de
   uno, **en la ventana del bot**: de 07:00 a 15:00 de España. El script no coloca nada de 22:00 a
   03:00 del servidor.
2. Un gráfico de EURUSD y el botón **Algo Trading** activado. Arrastra **MedirOrdenesFTMO**. Las
   entradas: **`InpEstrato`** `uno` o `bot` (nada más: el lote lo calcula el script) e
   **`InpCiclos`**, cuántos como mucho en esa ejecución. Las dos se alternan en la misma cuenta:
   una ejecución «uno», otra «bot».
3. **Esperar** a la ventana **«MedirOrdenesFTMO: terminado»**. Si salta un tope, lo dice su fila y la
   cuenta queda sin nada del script; si dice «ATENCION: quedan», ciérralo a mano (Ctrl+T) y díselo
   a la sesión. Relanzarlo el mismo día es seguro: los topes se leen de la cuenta.

## Cómo se congela y cómo se lee

MetaTrader deja los ficheros en **MQL5 → Files**: de la medida, `F17M_<estrato>_<AAAAMMDD_HHMMSS>.csv`
por ejecución y `F17M_ticks_<deal>.csv` por llenado; del grabador, `F17G_<AAAA-MM-DD>_<HH>.csv` por
hora y `F17G_control_<AAAAMMDD_HHMMSS>.csv` por arranque. **No los abras con Excel ni los renombres**:
cópialos tal cual a `data/f17-ordenes/<AAAA-MM-DD>/` y `data/f17-grabador/<AAAA-MM-DD>/` (fuera de git).

**Antes de leer nada**, la sesión escribe la fila del día en `HOLDOUT-EXPOSICIONES.md` (por recuento
de días, y si su mes está en `meses_reservados.yaml`) y congela cada carpeta con su manifiesto en
`data/manifests/f17-ordenes/` o `data/manifests/f17-grabador/` (esquemas `schema_f17_ordenes: 1` y
`schema_f17_grabador: 1` de `data/manifests/README.md`; nunca en `f17/`). Después:

    uv run python scripts/leer_ordenes_f17.py medida data/f17-ordenes/<dia> --salida <fichero fuera del repo>
    uv run python scripts/leer_ordenes_f17.py grabador data/f17-grabador/<dia> --salida <fichero fuera del repo>

La medida da por clase y estrato n, mediana, percentil 90, máximo, `sin_tick`, `al_colocar`, fuera
de ventana y `bot_reducido`, y el veredicto de D3; el grabador, el spread de FTMO por hora de la
ventana. Imprimen puntos y recuentos; ningún precio. Lo que el número no dice: que la prueba
gratuita ejecute como el Challenge y la cuenta real (P4-08).
