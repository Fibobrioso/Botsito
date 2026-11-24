# AUDITORIA-CAZADOR-2026-11-23 · La auditoría «cazador» del 23 de noviembre de 2026, copiada tal cual

Hecha por Claude Code como orquestador, sin rama, el 2026-11-23, sobre `main` en 8a10590b, y dirigida
a Aleks (su §2 y su §3 le contestan); copiada tal cual (rama `trabajo/puente-techo`, fase A). Debajo
de la raya, el texto de `INFORME-CAZADOR-2026-11-23.md` sin tocar una línea: 29039 bytes, sha256
`3a228954dcc81ed886add70f0aeb0702908e6593549c7b6f653043c459e1164a` del fichero del Escritorio de
Aleks. Su material de apoyo (las entregas, la síntesis, las vías, la tabla y el resultado crudo, que
su cabecera llama «esta carpeta») se queda fuera del repo, en el Escritorio de Aleks
(`auditoria-cazador-trabajo\`).

---

# AUDITORÍA CAZADOR · 2026-11-23 · Vías no exploradas hacia la rentabilidad

- **Base:** main en 8a10590b (`stable/F39l-recorrida-construccion-3` = main^1). No se escribió nada en el repo; `git status` vacío al empezar y al terminar.
- **Cómo:** un Workflow (`wf_bbc4408d-768`) con 87 agentes y 0 errores:
  - 15 líneas de exploración: 7 sobre el repo, de solo lectura (`auditor-encargo`), y 8 en la web (GitHub con `gh`, artículos, documentación oficial, foros y YouTube);
  - 1 juez y arquitecto, que fundió los hallazgos en 27 vías;
  - 54 verificadores adversarios, dos lentes por vía: repo y reglas, y economía y estadística con la web;
  - 1 crítico de completitud, que añadió 8 vías nuevas, y 16 verificadores para esas 8.
  - Después, yo corroboré con fichero:línea las cifras que deciden (§2) y añadí lo que el enjambre no cerró (§4.2, vía V00).
- **Lo que no se hizo:** no se abrió el holdout, ni data/, ni el corpus, ni fotogramas, ni libros. No se ejecutó pytest, ni el arnés, ni ningún guion que cargue velas o ticks.
- **Dónde está todo:** en esta carpeta.
  - `entregas/` tiene las 15 entregas de exploración, tal cual.
  - `sintesis.md` tiene el juez.
  - `vias.md` tiene las 35 vías con sus dos veredictos y correcciones.
  - `tabla.md` es el índice.
  - `resultado-completo.json` es el resultado crudo.

## §1 · La respuesta, en seis líneas

1. **Tienes razón en la forma del problema, no en su nombre.**
   - Lo que separa el registro del trader del bot **no son los costes**. El registro bruto da +0,98 R. El techo, antes de pagar comisión, da entre +0,10 y +0,43 R. La diferencia, de 0,55 a 0,88 R, está en el **R bruto**: el bot no gestiona las mismas operaciones como las gestiona el trader.
   - Eso sí es «estructuración incompleta».
2. **Pero los costes no son ligeros, y hay que decirlo con su cifra.**
   - La comisión es 5/D en R (D, la distancia al stop en puntos). Con stops de 1,5 a 1,8 pips de mediana, cuesta entre 0,28 y 0,33 R a la mediana y 0,43 R de media en el registro.
   - Ninguna pieza de arquitectura toca ese 5/D: el R no depende del lote.
   - Para que el bot gane hay que **recuperar el bruto del trader** y, aparte, **elegir dónde y cómo se paga el coste**.
3. **La pista más fuerte ya estaba publicada y nadie la había puesto en el centro.**
   - V2 es una regla fija, sin break even, sobre las mismas operaciones de abril y agosto. Da +0,88 R bruto, frente a +0,98 del registro: reproduce el 90 % de su bruto.
   - El techo, con el break even de la zona posterior (RN-014, cuya geometría leímos nosotros según ADR-0061 §4), mueve el stop en 79 de 191 operaciones (41 %). En el registro solo 5 de 77 cierran a cero (6,5 %).
   - **El primer sospechoso del bruto perdido es nuestro break even, no la comisión.**
4. **Corroborado por mí: FX Replay ya cobra el spread en las compras.**
   - 15 de 111 compras del trader quedan por encima del rango de la M1 BID de Dukascopy, y 0 de 87 ventas. Es la firma de llenar las compras por el ask.
   - El neto del registro (+0,56 R con 5 USD) no baja a +0,36 como temía la síntesis: la premisa aguanta mejor.
5. **La medida más barata y más grande que falta son los ticks reales de FTMO.**
   - El servidor de la demo de FTMO ya sirve ticks reales al Strategy Tester: está medido en el repo, un día. Nadie ha medido hasta dónde llegan hacia atrás ni los ha exportado.
   - Si cubren los meses de construcción, se puede repetir el techo con el spread y el feed del bróker que ejecuta, **sin esperar a grabar F17 en vivo**.
6. **Estadística: no hay potencia para detectar mejoras pequeñas.**
   - Con N = 191, ninguna mejora por debajo de ~0,3 R se distingue del ruido de elegir entre variantes.
   - Todo cambio tiene que salir de una **causa medida** (una cita del trader, un hecho de la plataforma, una identidad aritmética), nunca de un R mejor.

## §2 · Lo que corroboré yo (lo pediste: «si no te cuadran cifras, corrobora»)

| Cifra | Fuente | Resultado |
|---|---|---|
| Compras y ventas fuera del rango de la M1 BID de Dukascopy | `docs/validation/anexos/METODO-FIDELIDAD-RENTABILIDAD/medir-a16.txt`, recuento con grep | **15 de 111 compras, 0 de 87 ventas.** Distancia de 1 a 4 puntos; en 11 de las 15, el tick del lado (el ask) da 0. Cuadra con llenar las compras al ask. |
| ¿«El trader dispara por el precio medio» (síntesis, apoyándose en ORDEN-STOP-O-LIMITE §2.3)? | `ORDEN-STOP-O-LIMITE.md:118-156` | **FALSO como prueba.** Con tolerancia 0 y ventana de 60 s, «al revés» da 75/0, mejor que el medio (74/1). La tabla separa STOP de LÍMITE, no el lado, porque «el lado de la última aproximación es siempre el de la ruptura» (:155-156). Retirado. |
| Ticks reales de FTMO en el tester | `EA-CONEXION.md:141-145` | **CIERTO.** «generating based on real ticks»; se contaron 83.305 ticks de un día. Nadie midió la profundidad; las velas M1 empiezan a principios de 2025. |
| D del techo: mediana 1,80 pips; 17 % por debajo de 1,0 pip; 60 % por debajo de 2,0 | `MARGEN-LOTE.md:599-608` (lectura B) | **CIERTO.** El margen a 1:30 recorta el lote en el 58-73 % de las operaciones (:610-611). |
| Registro: bruto +0,98 [+0,50; +1,48]; con 5 USD, neto +0,56 [+0,05; +1,08]; V2 bruto +0,88 y neto +0,47 | `VIABILIDAD-COMISION.md`, tablas de las fases 2 y 3 | **CIERTO.** El informe también dice que el spread de la anotada «ya va dentro de los llenados de OANDA» (:99-101). Ahora hay un indicio medido de que es así, por lo menos en las compras. |
| A-16 «no medida» | `medir-a16.txt:1-11` | **MATIZ.** La entrada del trader frente a Dukascopy SÍ está medida: mediana 0 y 92,4 % dentro del rango de la M1. Lo que falta es comparar vela contra vela; el «+2 puntos» era una muestra anterior de 36 valores de agosto. |

Otras correcciones de cifras que hicieron los verificadores y el crítico, y que hay que arrastrar a cualquier ADR:
- **La dispersión que se usa para el techo.** Para la potencia, el SPRT y el efecto mínimo detectable hay que usar la del techo por días, con un error típico de ~0,129 sacado de meta.txt:14. No la sd de 2,2 R de la serie anotada.
- **La comisión que cambia el signo del techo** es de unos **1,5 a 3,2 USD de ida y vuelta**, no de «0 a 2,5». Lo da la pendiente de 0,068 a 0,134 R por USD.
- **El corte del lote por margen.** Hoy está hacia D < 20,5 puntos (500 / 24,4 lotes), no en 16,7.
- **La página de soporte de FX Replay no dice** que el gráfico sea BID por defecto. Lo que sí dice es que ofrece **OANDA, Dukascopy y Pepperstone** como proveedores de forex, cada uno con su propio feed (support.fxreplay.com, «what broker data sources…»). El repo da por hecho OANDA sin haberlo comprobado.
- **El techo sobre las mismas 77 operaciones del registro no está publicado.** Todas las comparaciones mezclan +0,98, que son dos meses, con −0,239, que son cuatro.
- **La tesis se apoya en parte en un libro que el trader no avala.**
  - El trader dio por bueno el backtest de agosto grabado en vídeo, «porque incluye los break even» (ADR-0073:49-54). El xlsx que se usa como registro de agosto es el otro.
  - Sin agosto queda abril solo: 35 operaciones, +1,05 bruto [+0,31; +1,83].

## §3 · La tesis de Aleks, punto por punto

| Afirmación | Veredicto | Cifra |
|---|---|---|
| «El backtest gana con solidez» | **En bruto, sí**: +0,98 R con un intervalo que no toca el 0, y bastarían ~13 operaciones para rechazar E = 0 si la cifra no tuviera sesgo. **En neto, por los pelos**: +0,56 con el extremo bajo en +0,05, en dos meses. Encima pesan S-14 (131 de 198 operaciones vienen de libros sin vídeo), el libro de agosto que el trader no avala y que no hay ninguna fuente de que gane en real. | VIABILIDAD-COMISION; criterio_fidelidad.yaml:55-65; ADR-0073:49-54 |
| «Unos costes ligeros no deberían matar la rentabilidad» | **Al registro no lo matan**: 0,98 − 5/D solo es negativo con D por debajo de ~5 puntos. **Al bot, sí**, porque su bruto es de +0,10 a +0,43 (lo más probable, +0,12 a +0,19) y la comisión cuesta de 0,34 a 0,67 R, entre 1,9 y 3,4 veces su bruto. Con stops de 1,5 pips, el coste no es ligero: es una de cada tres partes de la R. | meta.txt:13, :18; criterio_fidelidad.py:869-882 |
| «Es la estructuración del bot» | **Sí en el bruto, no en el coste.** El bruto que se pierde (0,55-0,88 R) no lo explica ningún coste: es gestión (break even, objetivo), selección (S-14, el libro) y mecánica de entrada. El coste, en cambio, no tiene arreglo de arquitectura: 5/D es una identidad. | §4 |
| «Pasar el discrecional al 100 % a código» | **Hoy, lejos.** La fidelidad está en 15,2 % / 14,4 % con una trayectoria plana. El bot no sabe abstenerse: operó en 13 de las 14 sesiones de los 7 días en que el trader no operó. Y llega antes que él: de las 114 operaciones del trader sin pareja, en 83 la orden más cercana del bot es anterior. Un bot fiel heredaría el techo. **El camino no es «más sesiones con el mismo método»; es medir de dónde sale el bruto (§4) y fijar después qué regla se codifica.** | RECORRIDA-CONSTRUCCION-3; recuentos de R5 sobre cuenta-por-mes.txt |

## §4 · Dónde está de verdad el dinero que se pierde

### 4.1 · El reparto (aritmética sobre cifras publicadas)

```
registro bruto (FX Replay, ya con el spread en las compras)   +0,98 R   (77 operaciones, abril+agosto)
V2 bruto (regla fija sin BE, Dukascopy, -2 puntos)            +0,88 R   (67, abril+agosto)
techo antes de comisión (regla dictada, con BE)               +0,10 a +0,43 R   (191, cuatro meses)
techo neto                                                    -0,239 R
```
- **Del registro a V2:** −0,10 R. Una regla fija, sin break even, casi lo reproduce.
- **De V2 al techo antes de comisión:** −0,45 a −0,78 R. Ahí cambian a la vez:
  - el break even RN-014 (79 movidos);
  - entrar con una orden stop por ticks (7 no colocables, el hueco);
  - quitar el desfase de −2 puntos;
  - meter las operaciones de stop cortísimo;
  - sumar enero y julio;
  - el cierre RN-002.
- **Del techo bruto al neto:** −0,34 a −0,67 R de comisión.

**Una hipótesis que hay que medir.** Supón que de esas 79 operaciones con el break even movido, solo 10 son en el registro operaciones que el trader llevó al objetivo. Cada una vale ~3,75 R + 0,33 R ≈ 4 R de diferencia. 10 × 4 / 191 ≈ **+0,21 R** de bruto perdido, solo por ahí. Es aritmética, no una medida: nadie ha publicado cuántas cierran en break even ni qué hizo el trader con esas mismas operaciones.

### 4.2 · V00 (nueva, la que el enjambre dejó abierta): la matriz de desenlaces, operación a operación

**Qué es.** Sobre las mismas operaciones de los días dev (primero las 77 de abril y agosto, luego las 198), una tabla 3×3 que cruza dos desenlaces:
- el del **trader**, según su libro: objetivo, stop, cero o salida manual;
- el del **techo**: objetivo, stop, break even o cierre RN-002.

Se publican solo los **recuentos de cada celda**, sin ningún R. Más tres columnas sin R: si el break even se movió, el minuto en que se movió y el múltiplo del objetivo que marcó el trader.

**Por qué es la medida que decide.**
- Dice, sin elegir nada por el R, en cuántas operaciones el bot gestiona distinto lo que el trader gestionó: **es fidelidad de la gestión**, la pieza que el método de ADR-0043 no mide (ese método solo empareja entradas).
- Si la celda «trader objetivo / techo break even» es grande, la culpa es de la geometría de la zona posterior, y la pregunta para el trader sale con ejemplos de sus propias operaciones.
- Si es pequeña, el break even queda descartado y el sospechoso pasa a ser la entrada o la serie.

**Puertas.**
- El detalle por operación de los días dev se lee sin puerta (ADR-0021 §1; CLAUDE.md, punto 3).
- ADR-0098 §4 c) prohíbe el R por clase: por eso aquí hay solo recuentos.
- Hace falta una NOTA de Aleks que la autorice como diagnóstico de fidelidad y fije por escrito que no se usará para elegir ninguna regla.
- Se declara en HOLDOUT-EXPOSICIONES el día en que se corre.

**Coste.** Una rama corta: el guion lee las salidas de techo_parejas y la columna de salida de los libros de los días dev.

**Riesgo de ajuste.** Bajo si la regla de lectura se escribe antes. Por ejemplo: «si más del X % de las 79 son objetivo en el registro, se pregunta al trader por RN-014 con esos ejemplos». Nunca «se quita RN-014».

## §5 · Las vías, priorizadas, con su veredicto y la cifra corregida

Las 35 vías salieron con MATIZ en las dos lentes; ninguna sobrevivió tal cual ni ninguna quedó refutada. Aquí van con las correcciones ya aplicadas. Clave de efecto: **R** = puede mover la esperanza del techo; **M** = es una medida que decide adónde ir; **P** = protege contra un error.

### A · Medir lo que decide (las primeras dos semanas)

| # | Vía | Efecto | Coste | Puerta |
|---|---|---|---|---|
| V00 | Matriz de desenlaces trader frente a techo, por operación (§4.2) | M: atribuye el bruto perdido | 1 rama corta | NOTA de Aleks; ADR-0098 §4 c), solo recuentos |
| V02 | **Ticks reales de FTMO desde el Strategy Tester.** Medir su profundidad con un EA que cuenta ticks sin leer precios. Si cubren los cuatro meses dev: exportarlos con `CopyTicksRange` (guion en `tools/mql5/`), hashearlos y congelarlos. En la misma prueba, sacar las aperturas H4 del servidor. Criterio de calidad escrito antes: hueco máximo dentro de 07-15 Madrid, minutos sin ticks y coherencia con su propio M1. El recuento por día no basta: MT5 rellena con ticks sintéticos donde faltan. | M y R: si el spread de FTMO en los llenados es ~2 puntos menor, de +0,13 a +0,27 R; si es igual o mayor, 0 o peor | 30 min de Aleks más un guion MQL5 de 150-250 líneas | Una prueba gratuita viva (A.5); para usarlo como fuente, un ADR que enmiende ADR-0005 y ADR-0024 §4 |
| V01 | **El lado y el proveedor de FX Replay.** (a) Aleks pone 10-20 órdenes sintéticas, en las dos direcciones y con el proveedor Dukascopy dentro de FX Replay, con spread y comisión a 0 y después con valores; cruzar con los ticks bid y ask. (b) Preguntar qué proveedor tiene seleccionado el trader. (c) Separar la asimetría de las compras (15/111) en entrada y salida. | M: fija si el neto del registro es +0,56 o menos | ~1 h de Aleks y 1-2 días de guion | ADR-0029 §1 lo deja abierto; solo días dev |
| Puente | El puente V2→techo de la auditoría anterior, **reordenado: el break even primero**. Después la entrada por stop, el desfase, las operaciones de stop corto y los meses. | M: dice cuánto pesa cada pieza | 1-2 ramas | Lo que ya estaba escrito en §8.1 de la auditoría anterior |
| V04 | Preguntas cerradas al trader, sin ninguna cifra nuestra: qué proveedor usa en FX Replay y si tiene el spread y la comisión activados (una captura de la configuración); si en real se salta sesiones; cómo coloca el TP en la herramienta (A-56); tamaño mínimo de caja que toma en real. **Y la nueva VN6:** acceso de solo lectura a su cuenta real (contraseña de inversor o un extracto de la firma), filtrado por Aleks antes de que lo vea nadie (ADR-0072). | M: es la premisa | 0 | ADR-0072; para leer su real, un ADR que diga quién, qué y cuándo |

### B · El coste: dónde y cómo se paga

| # | Vía | Efecto corregido | Comentario |
|---|---|---|---|
| V03 | Publicar el coste por tramo de D (comisión/D y spread/D, sin ningún R) y un registro de costes por operación, con un test sintético (en un paseo aleatorio, −s/D) que descarta un doble cobro | P/M | Lo más barato. Pide una NOTA para la tabla por tramos |
| V13 | **Carril de ejecución con un filtro de coste fijado antes**: no entrar si (5+s)/D > k, con k fijado por una regla de presupuesto, no por la distribución observada | R: de +0,04 a +0,23, y el techo se queda entre −0,20 y −0,01. **Recorta pérdidas, no cura.** Pierde fidelidad (el trader opera esos stops) y choca con ADR-0081:241-243 | Necesita un ADR que supersede la lectura de ADR-0081, y que el trader diga si en real toma cajas de menos de 1 pip |
| V21 | Matriz de fricción por firma y cuenta, con un what-if lineal sobre las posiciones ya corridas | R: cada USD de ida y vuelta vale de 0,068 a 0,134 R; el signo solo cambia con una comisión de ~1,5-3,2 USD o una fricción total por debajo de unos 6,5 puntos | FTMO cobra 5 USD por lote de ida y vuelta en forex simulado (su blog oficial). El cambio de firma tira lo medido en ADR-0071 y ADR-0090 |
| V25 | **Subir D en vez de bajar el coste**: el mismo método con la caja en M5, u otro instrumento (índices sin comisión según el blog de FTMO, sin verificar), elegidos ANTES por fricción/D | R: ahorra ~0,30 R de coste **si el bruto se conserva**, y eso es una hipótesis fuerte. Rompe la fidelidad: es otro método, con otro holdout | La que más mueve el coste, y la más especulativa. Hoy, solo una medida de D/ATR en dev |
| V26 | Microestructura: stop-limit, entrada a límite, latencia, horas de spread mínimo, spread máximo | R: todas juntas, de ~0,1 a 0,15 R como mucho | Menores; el filtro de spread máximo entraría dentro de V13 |

### C · Ejecución y traducción del gráfico a la orden

| # | Vía | Efecto | Comentario |
|---|---|---|---|
| V17 | Un traductor de niveles con `lado_del_grafico` como parámetro y, si V01 lo pide, un disparo virtual por la serie del gráfico | Fidelidad; en R, ±0,07 como mucho | Lo decide V01. Si FX Replay llena como un bróker (W1), la traducción literal de hoy ya es la correcta |
| VN4 | Markout de los llenados: el precio medio a 1, 5, 30, 60 y 300 s del llenado, frente a un placebo de instantes | M: dice si las entradas stop compran justo el pico (selección adversa) | Barata, sin R |
| V22 | Prueba de truncado para todos los detectores (también el cierre al tick del break even, que hoy no tiene ese test) | P: solo puede empeorar el techo o dejarlo igual | Antes de cualquier prueba en real |

### D · Fidelidad, con otro foco

| # | Vía | Qué aporta |
|---|---|---|
| V07 | Abstención y momento: la matriz 2×2 de operar o no por sesión, el adelanto del bot frente a un nulo por permutación, y un placebo para la cascada | Es lo que hoy falla (13 de las 14 sesiones en que el trader no operó; 83 de 114 operaciones donde el bot va antes). Es lo que hay que preguntarle al trader: «¿qué te hace NO entrar?» |
| V09 | Placebo de señal: entradas y zonas al azar, con la misma geometría, el mismo horario y la misma D | Dice si la señal del bot añade algo al stop y al objetivo. Con N = 191 solo detecta diferencias de 0,33-0,40 R o más; si sale en ±2 errores típicos, no es concluyente (no prueba ausencia) |
| V15 | ¿Cuánto se repite el trader a sí mismo? Sus entradas en vivo de las sesiones frente a su libro | Calibra la vara del 0,70. Hay que sacar las entradas de fotogramas localizados de un vídeo en cuarentena: coste alto |
| V24 | Un clasificador interpretable de qué candidatos toma el trader, **solo para generar preguntas** | Con ~85 unidades efectivas, lo esperable es que no bata a las líneas base; antes, tablas de contingencia por variable |
| VN1 | Índice de fragilidad por proveedor: las H4 del sesgo y las M1 que disparan el break even con un cuerpo menor que la diferencia entre feeds | Acota cuánto de la infidelidad no es del código |
| VN3 | Un anotador humano ciego aplica la spec escrita: los ingenieros, antes de ver el material | Mide si la spec escrita es suficiente: si un humano tampoco llega al 0,70, falta especificación, no código |

### E · Validación estadística (protege lo de arriba)

| # | Vía | Qué aporta |
|---|---|---|
| V06 | Un libro de ensayos y la deflación: contar cada variante medida en los meses dev | Mejor de 20 variantes sin ventaja ≈ +0,30 R de suerte (cota para variantes independientes) |
| V05 | R por dólar arriesgado (entre −0,37 y −0,26 en el bot, frente a −0,429 con el mismo peso por operación), riesgo efectivo (0,28-0,39 % frente al 0,5 % nominal), P(pasar el reto) por bloques de días y el efecto mínimo detectable | La puerta mide lo que no paga; los «pasa» de VIABILIDAD se calcularon sin margen |
| V16 | Paridad del simulador con el Strategy Tester sobre los ticks de FTMO y con nautilus_trader sobre los mismos ticks de Dukascopy | Descarta un error del simulador ≥ 1,8 puntos a favor (lo que haría falta para cruzar +0,10) |
| VN5 | Un presupuesto único de la brecha: cada vía se carga contra un fondo con tope, para no contar dos veces el mismo coste | Evita sumar mejoras que se solapan |

### F · Probar la premisa con costes reales

| # | Vía | Comentario |
|---|---|---|
| V20 | **El trader decide y el bot ejecuta en la demo de FTMO**: el trader marca la caja y el bot pone las órdenes y registra todos los costes | No es el «100 % código»: es la única prueba rápida de si **su** estrategia gana con los costes reales y sin S-14. SPRT honesto: ~320 operaciones con 0,05/0,05, de 8 a 9 meses. Necesita un ADR (ADR-0098:147-148), y las firmas prohíben mezclar bot y operación manual en el mismo reto (ADR-0026:90-91): en demo no aplica |
| VN8 | S-14 por la frecuencia: julio, con vídeo, da 5,2 operaciones por día; los libros sin vídeo, 2,1 | Solo recuentos. Es la medida más directa del sesgo de los libros |
| VN7 | La volatilidad como covariable del coste: pronosticar el coste en R de 2025 antes de medirlo | Evita la sorpresa en la puerta de rentabilidad |

### G · Riesgo de cuenta y cumplimiento

| # | Vía | Comentario |
|---|---|---|
| V14 | Duraciones y modificaciones del bot frente a R16 y R13 de FTMO | Riesgo binario de perder la cuenta; un histograma de duraciones en los días dev |
| V19 | Riesgo por operación: d) y e) fallan por la escala | Con 0,3 % se cumplirían, pero b) y c) no cambian, y con E < 0 la probabilidad de pasar baja |
| V18 | Break even neto de costes (entrada + c) | **Pregunta al trader, no una palanca.** El ahorro real, ~0,07-0,11 R con la q implícita del techo |

### H · Descartadas, con su motivo

- **V27, meta-etiquetado con ML entrenado con el R:** ADR-0092 §6 lo prohíbe y no tiene potencia con N ≈ 191.
  - Sí cabe un meta-etiquetado con etiqueta de **fidelidad** (V24).
  - Y un filtro de coste fijado antes no depende del R (V13).
- **Copiar en vivo al trader (copy trading):** fuera del objetivo del bot. FTMO solo admite copiar entre cuentas propias.
- **Librerías ICT/SMC (smart-money-concepts y similares) como oráculo:** su definición es centrada, así que mira el futuro (look-ahead), y no hay evidencia pública de que ICT/SMC tenga ventaja **neta de costes** (W4-H9). Sirven solo como contraejemplo de definiciones.

## §6 · La arquitectura que propongo (reenfoque)

**Principio: separar lo que dicta el trader de lo que el bot decide para pagar los costes, y medir cada plano en su sitio.**

1. **Datos con varios proveedores.** Un manifiesto inmutable por proveedor:
   - Dukascopy, como referencia;
   - FTMO, exportado del tester (V02);
   - la serie del trader, el proveedor que tenga seleccionado en FX Replay (V01).

   Cada MercadoDia usa un solo proveedor, el spread va por proveedor y el huso se convierte al ingerir. Un ADR fija de antemano con qué feed se juzga 2025: con el del bróker que ejecuta.
2. **Decisión.** Es el dominio puro: la regla del trader en las coordenadas de **su** gráfico. Solo cambia con una cita suya (`fb-` o `ev-`).
   - **Novedad:** hay dos especificaciones de gestión, cada una con su sello:
     - **la dictada**, la de hoy;
     - **la practicada**, que describe lo que hace su registro (el múltiplo del objetivo que marca la herramienta, la frecuencia de break even), sacada del material y no del R.

     Ninguna se elige por el R. Se le preguntan al trader las dos con ejemplos de V00, y la respuesta decide (ADR-0092 §6).
3. **Traductor de niveles** (V17): del nivel del gráfico a la orden del bróker según `lado_del_grafico`.
4. **Ejecución y coste**, una capa aparte de categoría `ejecucion`. Lleva los vetos de margen, de la firma y, solo con un ADR, el de coste por D (V13). Nada de esta capa mira el R.
5. **Bróker simulado con un registro de costes por operación** (V03): comisión, spread de entrada y de salida, hueco y deslizamiento. Se valida contra el Strategy Tester y contra nautilus (V16).
6. **Métricas en tres planos que no se mezclan:**
   - **fidelidad de entrada:** la de hoy, más la abstención (V07);
   - **fidelidad de gestión:** V00, nueva;
   - **coste**, por tramo de D;
   - **rentabilidad:** R con el mismo peso, R por dólar, P(pasar), deflactada (V05, V06). Se mide una vez.
7. **Vivo:** el EA ejecuta y veta. Antes, la conciliación diaria por cuatro causas (decisión, datos, llenado y coste; V23), y un ADR de Aleks sobre si una demo que decide cuenta como «en vivo».

## §7 · Plan de ataque, con lo que decide Aleks en cada punto

**Semana 1 (desde el 2026-11-23), sin el trader y sin prueba de FTMO**
- Aleks:
  - la prueba sintética de V01 (a) en FX Replay, ~1 h;
  - mandar al trader las preguntas de V04, sin cifras: el proveedor y la captura de la configuración de spread y comisión;
  - pedir el acceso de solo lectura de VN6.
- Rama de diagnóstico sin R:
  - V00: los recuentos de la matriz de desenlaces;
  - V03: el coste por tramo de D y su test sintético;
  - V05 y V06: las métricas y el libro de ensayos;
  - VN8: la frecuencia por libro;
  - V14: las duraciones.
- **Aleks decide:** una NOTA o un ADR con la lista cerrada de diagnósticos y sus reglas de lectura, ANTES de que corran.

**Semana 2 (los ingenieros llegan hacia el 2026-12-03)**
- Aleks abre una prueba gratuita de FTMO. En la misma prueba: la profundidad de los ticks, exportarlos y congelarlos (V02), las aperturas H4 y el arranque de F17.
- Los ingenieros: la capa de proveedores (V11), la paridad con nautilus (V16) y la prueba de truncado (V22).
- **Aleks decide:** con V01, en qué «mundo» está FX Replay; con V00, si el sospechoso es el break even.

**Semanas 3-4**
- El techo sobre el feed de FTMO (V12) y la paridad con el tester.
- El puente con el break even primero.
- El placebo de señal (V09), pre-registrado.

**Punto de decisión (hacia el 2026-12-20): el ADR de Aleks que cierra R4.7**

| Si… | Entonces |
|---|---|
| V00 y el puente dicen que el bruto perdido es nuestro break even o nuestra entrada | La regla practicada se le enseña al trader con sus ejemplos; con su cita se corrige la spec y se vuelve a medir el techo (ADR nuevo que declare lo visto). **Es el camino que da la razón a Aleks.** |
| El techo sobre FTMO sube cerca de 0 | Se abre el carril V13 con k pre-registrado y una sola medida en 2025 |
| El placebo da señal ≈ 0 y el bruto no aparece con ningún arreglo | O V20 (el trader decide, el bot ejecuta) para probar la premisa con costes reales, o V25 (subir D) como otra estrategia con su propio holdout |

En todos los casos se decide qué es «en vivo» en una demo (ADR-0082 D4).

## §8 · Lo que sigue sin saberse

- Si el trader gana en real; VN6 lo contestaría.
- Cuántas de las 79 operaciones con el break even movido cierran a cero, y qué hizo el trader con ellas (V00).
- El spread de FTMO en los instantes de llenado (V02).
- Si el tester sirve ticks reales de todos los meses de construcción. Solo está medido un día.
- Si la demo de FTMO ejecuta como la cuenta Swing de pago (P-D1).
- El techo sobre las 77 del registro, igual por igual.

## §9 · Fuentes externas que aguantaron la verificación

- FX Replay ofrece OANDA, Dukascopy y Pepperstone para forex: https://support.fxreplay.com/articles/what-broker-data-sources-does-fx-replay-use-for-its-charts
- FX Replay y la línea del ask, los spreads y las comisiones (no dice si el gráfico es bid, ask o medio): https://support.fxreplay.com/articles/understanding-the-ask-line-spreads-and-commissions-on-fx-replay
- MT5, «Every tick based on real ticks»: rellena huecos con ticks generados y usa el M1 para corregir: https://www.metatrader5.com/en/terminal/help/algotrading/tick_generation
- `copy_ticks_range` de Python: https://www.mql5.com/en/docs/python_metatrader5/mt5copyticksrange_py
- Modelos de llenado de nautilus_trader: https://nautilustrader.io/docs/latest/concepts/backtesting/fill-models/
- La librería de referencia de SMC: https://github.com/joshyattridge/smart-money-concepts
- Placebo de FVG en TradingView: https://de.tradingview.com/script/Kbq3WncE-Fair-Value-Gap-FVG-Statistics-with-Placebo-Control/
- Bailey y López de Prado, probabilidad de sobreajuste del backtest: https://papers.ssrn.com/abstract=2460551
- Comisión de FTMO, 5 USD por lote de ida y vuelta en forex simulado (el blog oficial; hay que confirmarlo para la cuenta 2-Step): https://ftmo.oanda.com/blog/a-refined-trading-setup-for-the-us-market/
- Prácticas prohibidas en otras firmas, como ejemplo de reglas sobre scalping: https://the5ers.com/faqs/prohibited-trading-practices/

Auditoría entregada. No hay rama que cerrar; nada se ha commiteado.
