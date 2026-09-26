# Preparación de A-35 y A-44: RN-004 y RN-020 listas para activarse con la respuesta del trader

Rama `trabajo/preparar-a35-a44`, 2026-09-26, sesión autónoma sobre `main` en
`stable/F24-cableado-simulador`. Sin merge, sin tag y sin push: el cierre lo decide Aleks tras la
revisión del consultor. Ningún ADR nuevo: el mecanismo no decide nada; deja escrito, con opciones
cerradas y sin valor, lo que el trader tiene que responder mañana.

Guardas, verificadas al empezar (§0 del brief) y al terminar: `PREREGISTRO.md` con blob
`52649183…` y sin rellenar; cero autorizaciones en `knowledge/cases/holdout/`; nada de septiembre;
mayo, marzo y febrero ni se descargaron ni se ejecutaron (la compuerta de construcción se niega
antes de leer, también con `--diagnostico-*`, con test); ninguna fecha de día reservado o retirado
en ningún fichero commiteado (comprobado por patrón sobre cada fichero generado antes de
commitearlo); ningún `--no-verify`; un commit sellado por paso.

**Una contradicción entre el brief y el código, medida y resuelta al mínimo.** El brief dice «No
toques PROJECT_STATE (lo actualiza el cierre)». `make check` —la puerta del sello— ejecuta
`state check`, que exige que `PROJECT_STATE.md` declare la RAMA ACTUAL y el RECUENTO de funciones
de test; medido: con la rama nueva y un test más, falla con dos errores y no sella, así que ningún
commit de esta rama podía entrar. Se tocaron esas dos cosas y nada más (la línea de la rama y el
número), como hizo la rama anterior con el mismo mandato del consultor; todo lo narrativo queda
para el cierre. Está dicho en cada commit.

## 1. Las lecturas de «formado» que están documentadas, y de dónde salen

A-35 pregunta cuándo un alto o un bajo de M15 cuenta como formado. Lo que el corpus documenta,
según `docs/validation/A35-PIVOTE-FORMADO-CLASIFICACION.md` (los 10 pasajes de A-35, clasificados
con el criterio congelado de A-24) y los ítems de evidencia que cita:

| lectura (opción del selector) | fuente | cita |
|---|---|---|
| `inicio_vela_contraria` | v4 0:57:49-0:58:29, segmento #942, `ev-v4-005749-1e9325cb` (P9, el único que RESPONDE) | «la vela contraria para mí, apenas se inicia una vela contraria en un flujo de órdenes, yo ya lo tomo como un punto en el cual yo ya voy marcando» |
| `cierre_vela_contraria` | v4 0:50:53-0:50:58, segmentos #846 y #849, `ev-v4-005053-885e2773` (P8, DUDA; la acotación de ADR-0045) | «Uno ya formado» y «Por encima de este ya formado», frente a «el punto más alto de las últimas velas aunque sigan en curso» |

Y lo que las dos comparten, que no es lectura sino mecanismo: **el extremo lo marca la vela
contraria al flujo de M15**, no un recuento de velas a cada lado, que el trader rehúsa (v3 #975,
`ev-v3-011540-5425b533`, P4; también P5, P6 y P9). **No hay una tercera lectura documentada**: las
dudas 1 y 2 de la clasificación dicen que lo que separa a los pasajes es solo el «cuándo», y que
P8 y P9 pueden ser compatibles o no según se lea. No se inventa ninguna otra. Si el trader responde
otra cosa, el runbook para (`docs/runbooks/ACTIVAR-A35-A44.md` §4).

## 2. Qué se construyó, y dónde

| paso | commit | qué |
|---|---|---|
| dominio | `8486068` | `domain/pivotes_m15.py`: la vela contraria al flujo marca el extremo de la racha anterior; «formado» es un SELECTOR con las dos lecturas y ninguna más; el más reciente manda (ADR-0045); `toca` y `cruza` con cuerpo o mecha. Puro. 9 tests sobre M15 sintéticas |
| RN-004 | `f6ca15f` | `liquidez_m15_pivote_formado` en el registro (estrategia, enum, **UNKNOWN**); `DatosMercado` con M15 y M1 y la lectura; `alcanza_nivel` y `cruza` sobre la última M15 cerrada posterior a la vela contraria, del lado que fija el sesgo; `engine/diagnostico.py`; `--diagnostico-a35`. spec 13.0.0 → 13.1.0. 10 tests |
| RN-020 | `2cf7425` | seis `perdida_trader_*` en el registro (**UNKNOWN**); `engine/tope_trader.py` con los tres estados y el seguidor de cortes con su huso; RN-020 en el cableado con la peor equity del minuto y el primer límite tocado en la traza; `--diagnostico-a44`. spec 13.1.0 → 13.2.0. 14 casos de test |
| este informe | — | §3 y §5 |
| el runbook | — | `docs/runbooks/ACTIVAR-A35-A44.md` |

**El contrato, igual en las dos:** SIN FIJAR no es un valor válido. Con el parámetro UNKNOWN el
arnés y el visor se niegan tras la compuerta de construcción, nombrando A-35 o A-44 y sin leer una
sola vela. La única excepción es pedir el diagnóstico a propósito, y entonces **cada línea, cada
fichero y cada página** llevan `DIAGNOSTICO-A35-<lectura>` y/o `DIAGNOSTICO-A44-<modo>`: un fichero
así nunca puede llamarse como una línea base, y el informe empieza diciendo que no vale para
ninguna medida de fidelidad ni conjunto de medición. Con el valor ya fijado, pedir el diagnóstico
se rechaza (test con un registro sintético CONFIRMED). El modo diagnóstico NO es «un modo que no
bloquee» (la alternativa que ADR-0048 y ADR-0049 H4 rechazaron): los gates se evalúan con un valor
hipotético etiquetado, no se saltan, y lo que sale no puede contar.

**Lo que el mecanismo deja FIJO Y VISIBLE sin decidirlo por el trader** (cada cosa es un candidato
del §5): el nivel es el extremo de la racha de velas del mismo color anterior a la contraria y la
mecha de la propia contraria no lo mueve; un doji no es de ningún color y corta la racha; con
`inicio_vela_contraria` el pivote es el estado de cada instante (si la vela en curso vuelve a su
color, desaparece); los toques cuentan desde el fin de la vela contraria; la vela que toca y cruza
es la última M15 cerrada, con el criterio `liquidez_m15_criterio_toma` que la forma nombra; y el
lado del pivote lo fija el sesgo (RN-005: alcista → el BAJO más reciente; bajista → el ALTO), con
`ambiguo` e `insuficiente` sin liquidez marcada.

Del tope del trader: RN-020 se evalúa con la peor equity del minuto, como los frenos de la firma
(ADR-0053 §5); el instante del toque del trader es el de esa peor marca, el de la firma es el
exacto de su suspensión, y a igual instante la traza nombra al trader; la base `saldo_actual` de la
semana se evalúa con el saldo del momento de la lectura; el marcador del diagnóstico es un dólar
sobre la equity, que no es un valor plausible del trader.

## 3. El embudo descriptivo, en DIAGNÓSTICO, solo sobre construcción (abril y agosto)

Cinco corridas de `botsito motor arnes` sobre los 42 días de construcción (84 sesiones, 49 con
operaciones del trader, 77 operaciones): una por lectura de A-35 con `sin_tope` y con el marcador
de A-44, y una más con `--simular` (la cuenta cableada). **Todas rotuladas DIAGNÓSTICO, ninguna
vale para nada.**

| variante (DIAGNÓSTICO) | RN-004 dispara | `liquidez_tomada` | paradas NO_IMPLEMENTADA (sesiones del trader) | siguiente bloqueador tras RN-004 |
|---|---|---|---|---|
| A35 `inicio_vela_contraria` · A44 `sin_tope` | 61 de 84; 38 de 49 | 38 de 49 | 5: `cartuchos`, `perdida_dia_firma`, `perdida_total_firma`, `se_cierra_operacion`, `toca_colocar_orden_limite` (49 de 49 cada una) | RN-011 (`toca_colocar_orden_limite`) |
| A35 `inicio_vela_contraria` · A44 `marcador` | idéntico | idéntico | idéntico | idéntico |
| A35 `cierre_vela_contraria` · A44 `sin_tope` | idéntico | idéntico | idéntico | idéntico |
| A35 `cierre_vela_contraria` · A44 `marcador` | idéntico | idéntico | idéntico | idéntico |
| A35 `cierre_vela_contraria` · A44 `marcador` · `--simular` | idéntico | idéntico | **1**: `toca_colocar_orden_limite` (49 de 49) | RN-011 (`toca_colocar_orden_limite`) |

Frente a la línea base vigente (`CABLEADO-SIMULADOR-LINEA-BASE.txt`, con `--simular`): las
paradas pasan de 5 (`perdida_dia`, `perdida_semana`, `alcanza_nivel`, `cruza`,
`toca_colocar_orden_limite`) a **1**. En las corridas sin `--simular` las cuatro primitivas de los
acumuladores de la firma y `se_cierra_operacion` siguen paradas porque el motor de la spec no
tiene cuenta ni bróker: son las mismas de siempre en ese modo. Las reglas disparadas, RN-001 (42
de 84), RN-003 (84 de 84) y RN-033 (15 de 84), no se mueven; RN-004 aparece con **61 de 84**. Los 6
avisos de H3 (`gate RN-001, RN-033`) siguen ahí (§6). Cobertura 0/77 en todas, como toca: nadie
coloca una orden sin la geometría.

**Las cuatro variantes sin `--simular` son idénticas byte a byte una vez quitada la etiqueta**, fila
por fila. Medido, y tiene explicación, no es un fallo: (a) las dos lecturas difieren en CUÁNDO el
pivote está disponible (catorce minutos, con test), pero RN-004 toma la liquidez sobre la última
M15 cerrada posterior a la vela contraria, así que dispara en el mismo cierre con las dos; la
diferencia solo se vería en un consumidor que leyera el nivel durante la vela contraria (RN-005,
sin escribir); (b) `sin_tope` y el marcador dan lo mismo porque el bot no opera y su pérdida es
cero. **Conclusión que el brief manda decir textualmente: el embudo no separa las lecturas, y
aunque las separara no serviría para elegir una: la lectura la elige el trader, no el ajuste.**

Las 11 sesiones del trader sin `liquidez_tomada`: 6 con sesgo `ambiguo` (sin lado no hay liquidez
marcada, y RN-033 ya prohíbe), 4 alcistas y 1 bajista en las que ninguna M15 posterior a la
contraria cerró con cuerpo al otro lado del pivote más reciente dentro de la ventana.

**Dónde se detiene ahora cada sesión.** Con `--simular` (la cuenta y el bróker cableados) todas las
sesiones del trader llegan al mismo sitio: `orden_dimensionada:no[predicado:toca_colocar_orden_limite]`,
con `detenido_por_tope`, `detenido_por_tope_total` y `detenido_por_cartuchos` en «productoras sin
cumplirse» (los gates evaluados, y NO). Es decir: **tras RN-004, el siguiente bloqueador es la
geometría de la entrada** —`toca_colocar_orden_limite` (RN-011), que depende de la zona de control
(A-21), del esquema (`se_da_esquema`, RN-008) y de las demás ambigüedades de la entrada—, y detrás
de ella `cartuchos` (RN-016), que solo se pide cuando hay un cierre.

## 4. Lo que este informe NO hace, por regla

No recomienda una lectura por cobertura ni por cercanía a las operaciones del trader; no fija
ningún parámetro; no marca A-35 ni A-44 como resueltas. **La lectura la elige el trader, no el
ajuste.** Las cinco corridas van rotuladas DIAGNÓSTICO en el nombre y en cada línea, y no se
commitean: viven en la carpeta de trabajo de la sesión y se regeneran con los comandos de la tabla.

## 5. Candidatos a ambigüedad, SIN tocar `ambiguedades.yaml`

Cosas que el mecanismo deja fijas porque nadie las decidió, y que dependen del trader o del
consultor. Ninguna se ha abierto: se llevan a la revisión.

1. **La mecha de la vela contraria supera el nivel.** Es la segunda mitad de A-35 («¿qué haces si
   después el precio lo supera un poco?»). Hoy el nivel es el extremo de la racha anterior y la
   contraria no lo mueve (`pivotes_m15.py`, con test). Del trader.
2. **Una vela sin cuerpo (doji) en la racha o como contraria.** Hoy no es de ningún color y corta
   la racha. Del trader (o decisión del consultor si es indiferente).
3. **Con `inicio_vela_contraria`, la vela en curso que vuelve a su color.** Hoy el pivote
   desaparece (P9 dice «voy marcando», duda 3 de la clasificación). Del trader.
4. **Qué vela cierra «con cuerpo al otro lado»: la M1 del evento o la M15.** RN-004 no lo dice; hoy
   es la última M15 cerrada. Del trader.
5. **El lado del pivote lo fija el sesgo de H4.** Leído de RN-005; la vela que marca el extremo es
   contraria al flujo de M15 y no al sesgo (nota del token `liquidez_m15`), y qué pasa cuando el
   flujo va contra el sesgo es A-26, ABIERTA. Del trader (A-26) y del consultor (que la lectura de
   RN-005 sea esa).
6. **Los toques cuentan desde el fin de la vela contraria**, también con `inicio_vela_contraria`.
   Ligado al 1: si la propia contraria puede tomar el nivel, cambia. Del trader.
7. **Un tope del trader en dinero no lo nombra la forma de RN-020**, que pasa `perdida_maxima_diaria`
   (un porcentaje). El mecanismo lo admite leyendo `perdida_trader_*_usd` del registro; si el trader
   responde en dinero, la forma debería nombrarlo (ADR-0019 §1): decisión del consultor con su ADR.
8. **La base `saldo_actual` de la semana** (CONFIRMED en la sesión 1): hoy se evalúa con el saldo del
   instante de la lectura. Si el trader quiso decir «el saldo con el que empecé la semana», es
   `saldo_inicial_semana`, que la opción ya admite. Del trader.
9. **A igual instante, quién tocó primero** (trader o firma): hoy la traza nombra al trader y el más
   restrictivo manda igual. Del consultor.
10. **`sin_tope` contradice la sesión 1** (4,5 % y 9 % CONFIRMED). El runbook lo registra como
    RESOLVE_CONTRADICTION y lo deja al consultor.

## 6. Lo que quedó sin terminar, y la fase 6

- **Fase 6 (los 6 avisos de H3):** véase §7 al final de este informe, que se completa en su propio
  commit.
- **Lo que no se hizo a propósito:** no se tocó la spec ejecutable (`strategy_spec.yaml` solo cambió
  de versión por los parámetros nuevos del registro; ninguna regla, ningún token); no se abrió
  ninguna ambigüedad; no se escribió ningún productor de zonas (`toca_colocar_orden_limite`), que es
  el siguiente bloqueo y depende de A-21 y las demás.

## Estado

WAITING_FOR_USER_VALIDATION. Rama lista para revisión, NO cerrada.
