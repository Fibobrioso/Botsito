# Verificación de A-21: la medida «entrada dentro de la zona», operación por operación

Rama `trabajo/preparar-a21`, segunda tarea, 2026-09-26. Verifica el 6 de 77 de
`PREPARACION-A21.md` §3, clasifica las operaciones que caen fuera, mide el uso de una toma de
liquidez de una sesión anterior del mismo día, y acorta las rutas del diagnóstico. Sin merge, sin
tag, sin push. Solo construcción (abril y agosto); nada de mayo, marzo, febrero ni septiembre;
`PREREGISTRO.md` sin rellenar (blob `52649183…`); en `PROJECT_STATE.md` solo la rama y el recuento
de tests, que `state check` exige. Todo en DIAGNÓSTICO (A-35 `cierre_vela_contraria`, A-44
`sin_tope`, A-21 cada lectura): **nada de esto elige lectura ni ajusta la geometría.**

Lo produce `scripts/verificacion_a21_entradas.py`; su salida completa, con las 77 operaciones, está
en `VERIFICACION-A21-SALIDA.txt` (días de construcción, distancias en puntos; ningún precio ni
resultado del trader).

## 1. Fase 1 · ¿El 6 de 77 es real o un error de medición?

**Veredicto: no hay error de medición en lo que se compara; el 6 de 77 es real con la definición
que usaba, y con la tolerancia del criterio de fidelidad pasa a 7 de 77.** Dos cosas quedan
escritas que antes eran supuestos:

| supuesto | qué se compara | fuente |
|---|---|---|
| **la zona** | la que el productor del motor tiene VIVA en el instante del llenado del trader: el esquema detectado desde la PRIMERA toma del día (`liquidez_tomada` no caduca al abrir la sesión), con las M1 anteriores al llenado y la lectura de A-21 dada. El lado lo fija el sesgo de la sesión en que se hizo la toma, como lo anota el productor, no la dirección del trader | `engine/zonas.py`, `_anotar_toma` / `_esquema` |
| **el precio** | `entrada` del caso = `entryPrice` del backtest (F14a). En un backtest de órdenes límite es el precio límite y el de llenado a la vez: no hay otro precio de ejecución en el material. El instante del caso es el llenado (`INSTANTE-LLENADO-SALIDA.txt`) | `cases/ingesta.py`, `F14A-INGESTA.md` |
| **la tolerancia** | «dentro» es d ≤ 0 sin tolerancia; «en el borde» es 0 < d ≤ 3, con `tolerancia_entrada_puntos` de `criterio_fidelidad.yaml` (ADR-0043), leída del fichero | `cases/criterio_fidelidad.py` |
| **la distancia firmada d** | entrada del trader menos el borde CERCANO de la zona (compra), o al revés (venta): d > 0 fuera por el lado del precio; −caja ≤ d ≤ 0 dentro; d < −caja más allá del extremo | este script |

**Una corrección de medida, sí, aunque no cambia el 6.** El primer script (`verificacion_a21.py`)
tomaba el LADO de la zona del sesgo de la sesión de la operación; el productor lo toma del sesgo de
la sesión de la TOMA. Con el lado del productor, las operaciones con zona viva pasan de 37 a 39
(lectura a) y de 32 a 34 (b), y las «en dirección contraria a la zona» de 7 a 13 y de 4 a 9; el
«dentro» sigue en 6 y 6. El script nuevo lleva la corrección y el viejo queda como está, con su
salida, porque su cifra principal no se mueve y su texto ya dice qué medía.

**La distribución de d, sobre las operaciones con zona viva en el llenado:**

| lectura | con zona viva | dentro (−caja ≤ d ≤ 0) | en el borde (0 < d ≤ 3) | fuera, lado del precio (d > 3) | más allá del extremo (d < −caja) | min · p25 · mediana · p75 · max |
|---|---|---|---|---|---|---|
| (a) `solo_una_zona_de_control` | 39 de 77 | **6** | **1** | 21 | 11 | −151 · −24 · 20 · 83 · 312 |
| (b) `sin_mecha_mas_alla_del_extremo` | 34 de 77 | **6** | **1** | 17 | 10 | −151 · −24 · 2,5 · 71 · 168 |

Con la tolerancia de ADR-0043 (3 puntos): **7 de 77 en las dos lecturas**. Las 6 «dentro» y la del
borde son las mismas operaciones en las dos.

**Las operaciones SIN zona viva y su motivo** (a: 38; b: 43): 18 llegan antes de que RN-004 haya
tomado ninguna liquidez ese día; 20 (a) o 25 (b) llegan con la toma hecha pero sin un esquema
válido antes del llenado (el breaker no ha cerrado todavía, o la lectura lo rechaza). Con el lado de
la toma desaparece la categoría «sin lado» que tenía el primer script (7 operaciones en sesiones de
sesgo ambiguo): el productor toma el lado de la sesión de la toma, y esas operaciones pasan a tener
zona o a una de las otras dos categorías (§3).

**Geometría, operación por operación** (`VERIFICACION-A21-SALIDA.txt`, línea «geometria»): la caja
del motor va de 5 a 29 puntos (mediana 10) y la distancia entrada-stop del trader de 3 a 49
(mediana 15). **En 29 de las 39 operaciones con zona (a) el stop del trader está MÁS LEJOS que la
caja ENTERA del motor**, y el motor pondría el suyo a `stop_fraccion_caja` (0,8) de esa caja, más
cerca todavía. En 10 el stop del trader cabe dentro de la caja. Dicho como medida y nada más: la
caja de una vela de M1 es, en tres de cada cuatro operaciones, más estrecha que lo que el trader
arriesga.

## 2. Fase 2 · Clasificación descriptiva de las que caen fuera

Cada operación con zona viva se prueba, en este orden, contra: dentro; borde; más allá del extremo;
**el cuerpo y no la mecha** (la entrada a ≤3 puntos del borde del cuerpo del bloque); **el borde
lejano o el medio** de la caja; **un grupo de velas contrarias** (las contrarias consecutivas que
acaban en el bloque, si su rango la contiene); **otra vela contraria entre la toma y el breaker**;
**desfase de temporalidad** (la entrada cae en el rango de la M15 que contiene el bloque); **otra
zona anterior a la toma** (una contraria anterior o igual a la vela de la toma cuyo rango la
contiene); y **no se sabe**. La primera que casa es «la causa más probable»; se listan todas las
que casan. **Es descriptivo: ninguna categoría cambió la geometría, y una operación que casa con
varias no dice cuál es la buena.**

| categoría | (a) primera causa | (a) casa | (b) primera causa | (b) casa |
|---|---|---|---|---|
| dentro | 6 | 6 | 6 | 6 |
| en el borde (≤ 3) | 1 | 1 | 1 | 1 |
| más allá del extremo | 11 | 11 | 10 | 10 |
| el cuerpo y no la mecha | 0 | **0** | 0 | **0** |
| el borde lejano o el medio | 0 | 1 | 0 | 0 |
| un grupo de velas contrarias (bloque mayor) | 0 | **0** | 0 | **0** |
| otra vela contraria entre la toma y el breaker | 0 | **0** | 0 | **0** |
| desfase de temporalidad (la M15 del bloque) | 3 | 7 | 3 | 6 |
| otra zona anterior a la toma | 10 | **19** | 8 | 16 |
| no se sabe | 8 | 8 | 6 | 6 |
| total con zona viva | 39 | | 34 | |

Lo que se ve, sin interpretarlo: **ninguna entrada del trader casa con el cuerpo del bloque, con un
bloque de varias velas ni con otra contraria del impulso**; las que no están dentro casan sobre
todo con **una contraria ANTERIOR a la toma** (19 de 39) y con **la M15 del bloque** (7), y 11 de
ellas están **más allá del extremo** de la caja del motor (entran más profundo que todo el bloque).
Tres causas posibles para «anterior a la toma», que este informe no separa: el trader usa otra toma
(la suya, no la primera del día del motor), usa un bloque formado antes de la toma, o su toma es la
misma y su bloque es otro. Las 8 «no se sabe» están a más de 70 puntos de la zona, todas en la
sesión de la tarde, y 6 de las 8 con la toma hecha en la sesión de la mañana (§3). Y 13 de las 39 (a) van en dirección CONTRARIA
al lado de la zona: ahí el sesgo del motor y el del trader no coinciden (RN-003/RN-005, no A-21).

## 3. Fase 3 · `liquidez_tomada` entre sesiones

Medido sobre construcción con la traza del motor: **en 31 sesiones el motor abre con una toma de
liquidez hecha en una sesión ANTERIOR del mismo día** (el hecho no caduca al abrir; solo `sesgo` lo
hace). En esas 31, RN-011 no dispara NUNCA con la toma ajena (0 de 31): el esquema de la toma
está en memoria y `toca_colocar_orden_limite` solo es SI en el minuto del breaker, que ya pasó; pero
**RN-008 y RN-009 sí se evalúan y disparan con esa toma en las 31** (RN-008 prohíbe si no hubo
esquema; RN-009 cuenta las zonas del retroceso desde esa toma). **25 operaciones del trader caen en
esas sesiones**, y **18 (a) / 16 (b) de las 39/34 con zona viva tienen la zona formada en otra
sesión** (las 8 y 6 «no se sabe» del §2 son en su mayoría de estas). Nada se cambia: queda como
ambigüedad CANDIDATA, sin tocar `ambiguedades.yaml`, con la pregunta cerrada para el trader:

> **«Si la liquidez se tomó en Londres, ¿sigue valiendo para operar en Nueva York, o en Nueva York
> esperas una toma nueva?»** → sigue valiendo = lo que hace hoy el motor · toma nueva = la spec
> escribe `caduca: al_abrir_sesion` en `liquidez_tomada` (su nota ya dice que F14b lo anticipó) y el
> productor la sigue sin tocar nada, porque la toma sigue al hecho.

## 4. Fase 4 · Material de dibujo, fuera del repo

`C:\Users\USER\Desktop\reunion-a35-a44\a21-dibujo\`: seis días de construcción con operación del
trader, elegidos para cubrir las categorías del §2 que tienen algún día (dentro; borde; M15 del
bloque; más allá del extremo; no se sabe con la toma de otra sesión); para «cuerpo», «grupo de
velas» y «otra vela del impulso» no hay día porque no casan con ninguna operación, y se preguntan
igual. Por día: `dibujo-N.html` (el gráfico M1/M15 cortado antes de la primera entrada del trader
de la sesión, sin zona, sin operaciones de nadie, sin fecha, sin hechos del motor) y
`motor-N.html` (el mismo corte con la zona del motor y su tabla). `clave-SOLO-ALEKS.md` da la
entrada real, la zona y la categoría de cada día; `preguntas-a21.md` trae cinco preguntas cerradas
(qué velas forman el bloque, mecha o cuerpo, dónde va la orden, M1 o M15, y la de la fase 3) más
una sobre la invalidación. La hoja oficial no se toca.

## 5. Fase 5 · Rutas que caben en Windows

El NOMBRE del fichero de diagnóstico lleva ahora la forma compacta
`.DIAGNOSTICO.a35=<lectura>.a44=<modo>.a21=<lectura>` (antes, las tres etiquetas completas: 105
caracteres), y **toda ruta que el arnés o el visor vayan a escribir se comprueba ANTES de leer una
vela** (`engine/diagnostico.py`, `comprobar_ruta`, límite 259): si no cabe, código 2 y el mensaje
dice cuántos caracteres tiene y que se use una carpeta más corta con `--salida`. Las líneas y las
páginas siguen llevando las etiquetas completas. `tests/unit/test_rutas_windows.py`: la forma del
nombre, la guarda con una ruta corta y una larga, las rutas por defecto de este repo con las tres
etiquetas más largas caben, y la CLI del arnés y del visor se niegan ante una ruta larga sin
escribir nada. `PREPARACION-A35-A44.md` (cerrado en `main`) lleva su recuadro de corrección;
ADR-0054, una nota.

## 6. Lo que este informe NO hace

No cambia la geometría para acercar la cifra al trader; no elige lectura; no fija ningún parámetro;
no abre ninguna ambigüedad (la de la fase 3 es candidata). Las categorías del §2 son etiquetas de
coincidencia, no causas probadas: la causa la dice el trader dibujando (§4).

## 7. Estado

Rama lista para revisión, NO cerrada.
