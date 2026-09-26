# Verificación de `trabajo/preparar-a35-a44` antes del cierre

Rama `trabajo/preparar-a35-a44`, 2026-09-26, segunda sesión autónoma sobre la misma rama. Sin
merge, sin tag y sin push. Solo construcción (abril y agosto); mayo, marzo, febrero y septiembre ni
se tocaron ni se ejecutaron; `PREREGISTRO.md` sigue vacío con el blob `52649183…`; cero
autorizaciones. Cada commit con su sello; `PROJECT_STATE.md` solo la rama y el recuento de tests
que `state check` exige. El material para la reunión está FUERA del repositorio (§5).

## 1. ¿El selector de A-35 llega al motor? Había un bug de cableado, y está corregido

**Medido antes de tocar nada.** Una sesión sintética completa por `arnes.correr` con el motor real
(la spec vigente) en la que la vela contraria vuelve al nivel del pivote con su mecha antes de
cerrar: las dos lecturas daban **trazas idénticas** (mismas disparadas, mismo instante de
`liquidez_tomada`, mismas anotaciones), aunque el pivote estaba disponible catorce minutos antes
con `inicio_vela_contraria` (medido sobre los mismos datos).

**La causa, en el cableado.** `alcanza_nivel` y `cruza` exigían que la vela que puede tomar el
nivel fuera POSTERIOR a la vela contraria (`ultima.inicio >= pivote.contraria_fin`). Esa
convención mía anulaba el selector: daba igual cuándo naciera el pivote, porque la primera vela
que podía tocarlo era siempre la siguiente a la contraria. Además la traza no dejaba huella de
cuándo el pivote estaba a la vista.

**La corrección (`29cf798`), sin cambiar la granularidad de la toma (§2):**
- la vela que puede tomar el nivel sigue siendo la última M15 cerrada, pero **solo si el pivote ya
  existía antes de que cerrara** (`formado_en < fin`). Con `inicio_vela_contraria` la propia vela
  contraria cuenta, porque el pivote nace en su primera M1; con `cierre_vela_contraria` no, porque
  nace en su cierre. Es el selector el que decide, que es lo que tenía que pasar;
- la traza lleva la huella del selector: las anotaciones `liquidez_m15` (qué pivote es la
  liquidez y desde qué minuto) y `liquidez_m15_alcanzada` (el primer cierre de M15 que llegó al
  nivel), en `TrazaSesion.anotaciones`, como `sesgo_h4`.

**El test** (`tests/unit/test_preparar_a35.py`,
`test_por_el_arnes_real_las_lecturas_dejan_trazas_distintas_si_el_precio_vuelve`): la misma
sesión por `arnes.correr`; con `inicio` la liquidez nace en el minuto 1 de la contraria y se
alcanza en su cierre; con `cierre` nace en el cierre de la contraria y se alcanza dos velas
después; las trazas difieren. **RN-004 dispara en el mismo cierre con las dos** y el test lo exige,
porque es lo que la granularidad de §2 impone: la vela que marca el pivote no puede cerrar con
cuerpo al otro lado del extremo que acaba de hacer, así que con la toma medida al cierre de M15 y
con cuerpo la diferencia está en el toque, no en la toma. Sin que el precio vuelva en la contraria,
las huellas coinciden (también en el test).

**El embudo de la fase 4, repetido tras la corrección** (diagnóstico, las dos lecturas, `sin_tope`):
RN-004 61 de 84 sesiones, `liquidez_tomada` 38 de 49, las cinco paradas de siempre sin cuenta,
filas por sesión idénticas entre lecturas. No se mueve, y no tenía por qué: la corrección cambia el
toque dentro de la contraria y la toma no.

## 2. ¿De dónde sale que RN-004 evalúe sobre la última M15 cerrada? No hay fuente que lo diga

Lo que dice la spec (RN-004, `strategy_spec.yaml`): «el precio alcanza el alto o el bajo de M15
marcado» y «se da por tomada solo si **una vela** cierra con cuerpo al otro lado». La forma
(`alcanza_nivel {que: liquidez_m15}`, `cruza {que, criterio}`) no nombra la temporalidad de la
vela. La nota de RN-004 y su cita (`fb-2026-09-09-sesion-01-6e15504f`) dicen «solo en M15; en M1
el rompimiento es indiferente», que habla de QUÉ liquidez se toma con cuerpo, no de qué vela cierra.
ADR-0028 §2 dice que la estrategia se evalúa al cierre de M1 sobre velas cerradas, sin decir de qué
tamaño. Lo más cercano en el corpus son tres ítems de v4 —`ev-v4-001533-73539d90` («lo rompa con
cuerpo y cierre con cuerpo por encima de la zona de liquidez»), `ev-v4-003849-3fe5161b` («en M1 la
mitigación de liquidez vale con mecha; en M15 tiene que cerrar con cuerpo») y
`ev-v4-003942-cfffa382` («en M15 la mitigación de liquidez es con cuerpo; en M1 se trata de otra
manera»)— que se pueden leer como «la vela de M15 es la que cierra», pero también como «la liquidez
de M15 se mitiga con cuerpo», sin decir de qué vela.

**Textualmente: no hay fuente que fije la vela, y evaluar sobre la última M15 cerrada fue una
elección de implementación** mía en `f6ca15f`, tomada por coherencia con «la liquidez es de M15»
y no por una cita. **No se cambia** en esta rama. Queda como **ambigüedad candidata** (no se abre
en `ambiguedades.yaml`): «qué vela tiene que cerrar con cuerpo al otro lado de la liquidez de M15»,
con tres lecturas posibles: **al cierre de M15** (la de hoy), **al cierre de M1** (la vela del
evento del motor, ADR-0028 §2) y **al tick** (el precio pasa el nivel, que la cita del trader
excluye: «con cuerpo»). La fase 3b mide cuánto separa hoy a las dos primeras.

## 3. Medición descriptiva en construcción (nada se decide)

`scripts/verificacion_a35_a44.py`, salida completa en `VERIFICACION-A35-A44-SALIDA.txt` (días de
construcción, sesiones, minutos y recuentos; ninguna entrada, ningún stop, ningún resultado). Base:
77 operaciones del trader en 42 días; el pivote de referencia es el más reciente ya formado del lado
del sesgo (RN-005) con la lectura `cierre_vela_contraria`, y `inicio_vela_contraria` dice desde qué
minuto la contraria iba contraria.

**(a) Toque de la liquidez dentro de la vela contraria.** De las 77 operaciones, 7 caen en
sesiones con sesgo `ambiguo` (sin lado, sin liquidez marcada) y ninguna carece de pivote del lado
antes de la entrada. **En 30 de las 70 restantes, el pivote fue tocado dentro de su propia vela
contraria, después de que esa vela empezara a ir contraria**: son las operaciones en las que las
dos lecturas divergirían si la toma se evaluara dentro de la vela. En 19 de las 30 la contraria va
contraria desde su primer minuto; el toque llega entre su minuto 1 y su minuto 11. La lista, con
la hora UTC de la contraria y del toque, está en la salida.

**(b) Toma con cuerpo en una M1 dentro de una M15 todavía abierta.** En 53 operaciones una M1
cierra con cuerpo al otro lado del pivote antes de la entrada. Esa M1 cierra entre 0 y 14 minutos
antes del cierre de su M15 (mediana 8) y entre 1 y 93 minutos antes de la entrada (mediana 12).
**En 13 operaciones el trader entró ANTES de que cerrara la M15 en la que la M1 ya había tomado el
nivel**: con la toma medida al cierre de M15 (§2), en esas 13 el motor sabría de la toma después
de que el trader ya hubiera entrado. Es el dato que separa las lecturas «al cierre de M15» y «al
cierre de M1» de §2; no dice cuál es la del trader.

**(c) Las 11 sesiones del trader en las que RN-004 no toma liquidez, por causa:**

| causa | sesiones |
|---|---|
| sesgo `ambiguo`: sin lado, no hay liquidez marcada (RN-033 ya prohíbe) | 6 |
| hay pivote del lado del sesgo y se tocó con la mecha, pero ninguna M15 cerró con cuerpo al otro lado | 4 |
| hay pivote del lado del sesgo, pero el precio no volvió a su nivel en la sesión | 1 |

Ninguna es «no hay pivote». Las 4 tocadas sin cuerpo son exactamente el caso que la lectura «al
cierre de M1» o «al tick» de §2 podría cambiar; no se ajusta nada.

**(d) A-44 de punta a punta, con un marcador que sí se alcanza.** `--diagnostico-a44
marcador_cero` (`fde95bb`): un tope de cero sobre la equity, que se alcanza sin perder nada.
Medido en construcción, etiquetado DIAGNOSTICO-A44-marcador_cero: **RN-020 dispara en 84 de 84
sesiones y fija `detenido_por_tope` en las 49 del trader**; en el motor cableado, además,
`colocar_orden_limite` queda bloqueada (test). El bloqueo funciona de punta a punta. Ese valor no
es plausible de nadie y no se registra en ningún sitio; solo existe como modo de diagnóstico.

## 4. Lo que estos números NO dicen

No dicen qué lectura de A-35 es la del trader, ni qué vela cierra con cuerpo, ni si tiene tope.
Todo lo de arriba es descriptivo y sale de convenciones fijas y visibles (`PREPARACION-A35-A44.md`
§2 y §5); el mecanismo se activa con lo que el trader responda, y solo con eso
(`docs/runbooks/ACTIVAR-A35-A44.md`).

## 5. El material para la reunión, fuera del repositorio

En `C:\Users\USER\Desktop\reunion-a35-a44\` (no versionado): cinco páginas del visor
(`ejemplo-1.html` … `ejemplo-5.html`) de días de construcción cortadas en el instante del toque
dentro de la vela contraria, sin entrada ni resultado (la vista termina antes de la primera
operación del trader del día), con M1 y M15 conmutables; `correspondencia.tsv` con el caso, la
sesión y la hora de corte de cada una; y `hoja-aleks.md`, con lo que dice cada lectura en cada
ejemplo y diez repreguntas cerradas de confirmación para A-35 y A-44 (la mecha que supera el nivel,
el doji, la vela que vuelve a su color, qué vela cierra con cuerpo, el toque dentro de la propia
contraria, el tope en dinero o en porcentaje, la base semanal, lo abierto, `sin_tope` frente a la
sesión 1 y el reloj del reinicio). No se tocó `ambiguedades.yaml` ni la hoja oficial.

## 6. Qué pregunta desbloquea más en construcción

Con la cuenta cableada y las dos hipótesis puestas, el embudo se para en UNA sola primitiva:
`toca_colocar_orden_limite`, la geometría de la zona de entrada, que es **A-21** (y detrás, la
demás geometría de la entrada). **A-35 y A-44 son las llaves para que el motor corra a secas**
—sin ellas se niega—, pero en construcción su valor no cambia el embudo: RN-004 ya dispara en 61
de 84 sesiones con cualquiera de las dos lecturas, y RN-020 no bloquea mientras el bot no opere.
**Lo que más desbloquea es A-21.** A-35 importa para la fidelidad del instante (13 entradas del
trader anteriores al cierre de la M15 de la toma, §3b) y A-44 para la cuenta cuando el bot opere.

## Estado

WAITING_FOR_USER_VALIDATION. Rama lista para revisión, NO cerrada.
