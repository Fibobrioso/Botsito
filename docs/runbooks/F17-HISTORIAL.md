# El historial de ticks de la demo de FTMO (F17, primera parte)

Para Aleks, en la prueba gratuita de FTMO que se active después (otra rama). Un script de
MetaTrader 5 exporta los ticks de EURUSD que el servidor de la demo **ya guarda**, día a día, con la
M1 del propio servidor, solo de los meses de construcción; el repositorio dice, con el criterio
escrito antes de ver un tick (`docs/plan/F17-HISTORIAL.yaml`), si cada mes **cubre** (ADR-0099 §5).
Si cubre, el spread de FTMO sale de ahí sin esperar al grabador. **No cambia nada de la estrategia
ni de los parámetros**, y que un mes cubra no autoriza a usar esos ticks como fuente de una medida:
eso pide un ADR que enmiende ADR-0005 y ADR-0024 §4.

El script es `tools/mql5/ExportarTicksFTMO.mq5` (versión 1.0, rama `trabajo/f17-historial`).
Cuánto tarda no está medido: depende de cuántos ticks tenga que bajar el terminal del servidor.

## Lo que hace, y lo que no hace nunca

- **No opera.** No llama a ninguna función de órdenes ni de posiciones
  (`tests/contract/test_exportar_ticks_ftmo.py`); no necesita el botón *Algo Trading*.
- **Se niega a correr si la cuenta no es de prueba (DEMO)**, con la misma condición que
  `MedirDemoFTMO.mq5`.
- **Solo EURUSD y solo días de enero, abril, julio y agosto de 2026**, los meses de construcción
  (`criterio_fidelidad.yaml`). Si el rango que le pides tiene UN día de otro mes, sale sin pedir nada
  al servidor (febrero no se toca ni se descarga: heredado 6 de PROJECT_STATE).
- Por cada día escribe dos ficheros y, al final, uno de control con los relojes y lo pedido. No
  escribe el login de la cuenta.
- Lo que no se sabe de MetaTrader se mide con lo que sale (ADR-0082 D7): en qué reloj van los
  instantes de los ticks y de las velas, si la M1 es la de BID y si los ticks son los guardados. El
  lector lo contrasta con el control y con los puntos (c), (d1) y (d2) del criterio.

## Una vez: compilarlo e instalarlo

La guardia de Claude Code no deja a la sesión lanzar MetaEditor con un guion cambiado en la rama:
lo lanzas tú, con el comando exacto que te da la sesión, desde la raíz del repositorio (una línea
`!`), que compila una copia del fichero tal como está en el índice de git, deja el log en los anexos
de la rama e instala el `.ex5` en `MQL5\Scripts\Botsito\` de tu terminal:

    uv run python src/botsito/mql5bridge/compilar.py herramienta --repo . --metaeditor "<ruta de MetaEditor64.exe>" --salida docs/validation/anexos/F17-HISTORIAL --instalar "<carpeta de datos del terminal>" tools/mql5/ExportarTicksFTMO.mq5

La carpeta de datos del terminal es la que abre **Archivo → Abrir carpeta de datos**. El log tiene
que decir **0 errors, 0 warnings**. El `.ex5` no entra en git (`.gitignore`).

## Cada vez: ejecutarlo

1. **Cualquier día y hora**: no hace falta el mercado abierto, porque no opera. Mejor sin otros
   scripts corriendo.
2. **Un gráfico de EURUSD**, como en `DEMO-FTMO.md` («Cada vez», paso 3).
3. **Lanzarlo** desde **Ver → Navegador → Scripts → Botsito**, arrastrando **ExportarTicksFTMO**
   encima del gráfico. En la ventana de entradas pon **un mes entero cada vez**: `InpDesde`
   `2026.01.01` e `InpHasta` `2026.01.31`; después abril (`2026.04.01` a `2026.04.30`), julio
   (`2026.07.01` a `2026.07.31`) y agosto (`2026.08.01` a `2026.08.31`). Un mes a medias no cubre:
   el criterio cuenta todos sus laborables.
4. **Esperar** a la ventana **«ExportarTicksFTMO: terminado»**. Si sale otra cosa (no es DEMO, un día
   de otro mes), no se ha pedido nada: díselo a la sesión.

## Dónde quedan los ficheros y a dónde van

MetaTrader los deja en **Archivo → Abrir carpeta de datos → MQL5 → Files**:
`F17_<AAAA-MM-DD>_ticks.csv` y `F17_<AAAA-MM-DD>_m1.csv` por día, y un
`F17_control_<AAAAMMDD_HHMMSS>.csv` por ejecución. **No los abras con Excel ni los renombres**:
cópialos tal cual, cada mes con su control, a **`data/f17/<AAAA-MM>/`** del repositorio (fuera de
git), y nada más en esa carpeta.

**Antes de leer nada**, la sesión escribe la fila del día en `HOLDOUT-EXPOSICIONES.md` y congela cada
mes con su manifiesto en `data/manifests/f17/` (esquema `schema_f17_historial: 1` de
`data/manifests/README.md`, escrito a mano con `sha256sum`, como el de la demo). Después lo lee:

    uv run python scripts/leer_historial_f17.py data/f17/2026-04 --salida <fichero fuera del repo>

El lector se niega a cualquier fichero que no sea de un día de construcción, pasa cada instante del
reloj del servidor a UTC con `broker_offset_base` y `broker_dst` del registro, dice si el control
cuadra con ellos, da por mes los puntos (a), (b), (c), (d1) y (d2) y su veredicto, CUBRE o NO
CUBRE, y, solo si cubre, el spread de FTMO por hora y la diferencia mediana con el de Dukascopy, como
diagnóstico. Imprime recuentos, fracciones y puntos de spread; ningún precio.
