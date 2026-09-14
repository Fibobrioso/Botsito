---
status: ACTIVE
date: 2026-09-14
phase: post-F13 (antes de F18 y F21)
---

# 0029 · Lado del precio y redondeo de niveles

## Decision

1. **Toda la geometría se mide sobre BID**: la liquidez de M15, la caja, el nivel de entrada, el
   stop y el objetivo. Es el lado de los datos de referencia (ADR-0005 fija
   `BID_candles_min_1.bi5`). **Lo que NO está verificado**: que sea también el lado sobre el que
   decide el trader. FX Replay no dice en ninguna fuente oficial qué lado dibuja (buscado el
   2026-09-14 en su centro de ayuda, sin respuesta). Si dibujara ASK o el precio medio, se abre
   ambigüedad y este punto se revisa.
2. **El llenado usa el lado que corresponde a la dirección**: una compra se llena a ASK
   (= BID + spread del momento) y una venta a BID. El spread sale del perfil medido en la demo (F17),
   nunca del proveedor histórico.
3. **Redondeo a puntos enteros: al más cercano, y en caso de empate, en contra del bot.** En un
   empate, el stop se aleja de la entrada y el objetivo se acerca. Ejemplos: 0,8 × 137 = 109,6 → 110
   puntos de stop (al más cercano, sin empate); 0,75 × 138 = 103,5 → 104 (empate, se aleja).
4. **El lote se redondea siempre a la baja** al escalón del bróker. Ya lo dice RN-027 (ADR-0016);
   aquí solo se declara que es la misma familia de decisión.

## Problema que resuelve

La auditoría del 2026-09-13 lo lista entre las decisiones de arquitectura sin ADR (§9.3): la spec
nombra niveles como fracciones de una caja, los precios del proyecto son enteros en puntos
(ADR-0005), y nada decía en qué lado del libro se mide la caja ni hacia dónde se redondea la
fracción. MASTER_PLAN H.2 lo dejaba como riesgo abierto: *«Redondeo fraccion → puntos (0,75 × 137 =
102,75) [...] stop al lado conservador»*, sin decir qué es conservador ni en qué empate. Sin esto,
F18 y F21 lo elegirían al escribir el tipo `Puntos`, y F29 en MQL5 podría elegir otra cosa.

## Alternativas consideradas

1. **BID para la geometría, lado por dirección para el llenado, al más cercano con empate en contra
   del bot** (elegida).
2. **Precio medio (BID + ASK) / 2** para la geometría.
3. **Redondeo siempre en contra del bot** (el stop siempre hacia fuera, el objetivo siempre hacia
   dentro), también sin empate.
4. **Redondeo bancario** (al par en el empate).

## Por que elegimos esta opcion

Porque la cifra que este proyecto va a producir es una medida de fidelidad que luego autoriza poner
dinero. Un redondeo que favorezca al bot la infla por construcción, y no hay forma de detectarlo
después. Resolver el empate en contra cuesta unas décimas de R y compra que el número signifique
algo. Y BID es el único lado del que hay datos de referencia para todo 2026 (ADR-0005, ADR-0024).

## Por que descartamos las demas

- **(2) Precio medio**: no hay medio en los datos de referencia —Dukascopy se descarga en BID— y
  habría que reconstruirlo con un spread histórico que ADR-0024 no reconoce como referencia.
- **(3) Siempre en contra**: sesga todos los niveles hasta un punto entero y no solo los empates;
  sobre cajas pequeñas es una parte apreciable del stop, y deja de medir la estrategia del trader
  para medir una más conservadora.
- **(4) Bancario**: en el empate a veces favorece al bot. Es simétrico en promedio, y el promedio
  no es lo que importa en una medida que decide si se pone dinero.

## Impacto

- **Con los valores de hoy casi no hay empates**: 0,8 por una caja entera de puntos deja décimas en
  múltiplos de 0,2 y nunca 0,5, y el objetivo (3 × caja completa) es entero. La regla de empate
  cubre valores futuros del registro, no es decorativa: con `stop_fraccion_caja` en 0,75 aparece en
  una de cada cuatro cajas (las de un número de puntos par no múltiplo de 4).
- **Consecuencia en las salidas, que F24 tiene que simular y F32 contrastar con Strategy Tester**:
  en MT5 una posición comprada se cierra a BID y una vendida a ASK, así que el stop y el objetivo de
  una VENTA, dibujados en BID, los alcanza el ASK: el stop (por encima) salta un spread antes de que
  el BID llegue, y el objetivo (por debajo) se alcanza un spread después. No es una decisión
  nueva: es el punto 2 aplicado a la salida, y se declara para que nadie lo lea como un fallo de
  fidelidad.
- F18 escribe la regla de redondeo en el tipo `Puntos`; F21 la usa y la prueba con un golden con
  residuo 0,5; F28-F29 la exportan con aritmética entera. MASTER_PLAN H.2 cita este ADR.
- El punto 1 queda pendiente de verificación con el trader o con FX Replay (informe de la rama).

## Fecha / fase

2026-09-14, después de F13 (decisión del consultor, sobre la auditoría del 2026-09-13).

## Estado

ACTIVE
