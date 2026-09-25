# A-35 en las transcripciones: la clasificación de los 10 pasajes

Rama `trabajo/a35-pivote-formado`, 2026-09-24. Sin merge, sin tag y sin push.

**Qué se clasifica:** los pasajes de la salida congelada (`A35-PIVOTE-FORMADO-SALIDA.txt`), los 10 y
ninguno fuera. La norma es la de `A35-PIVOTE-FORMADO-CRITERIO.md` §2:
- **RESPONDE:** enuncia de forma general cuándo un pivote está formado, o cuándo un alto o un bajo
  cuenta como marcado;
- **DUDA:** apunta a una regla, pero no la enuncia en general. Para la regla global, no responde;
- **NO RESPONDE:** habla de otra cosa.

**De dónde sale cada frase:** está copiada de la salida, que es la cruda. Una frase que ocupa varios
segmentos se da con sus números y los segmentos separados por « / ». Todas se han comprobado por
script contra su pasaje.

**Fotogramas:** es el más cercano según `botsito corpus frames show`, y se indica si ya estaba medido
o citado en el repositorio. **No se ha abierto ninguno.**

**Qué no se hace aquí:** no se aplica la regla global. La aplica el consultor.

| pasaje | tr | intervalo | clase | frase literal | por qué | fotograma |
|---|---|---|---|---|---|---|
| 1 | v1 | 0:14:09-0:15:42 | NO RESPONDE | #192 «Desde el punto más abajo te genera la vela contraria» | Dónde se pone el stop («aquí sería mi stop loss», #194) | — |
| 2 | v3 | 1:02:31-1:04:48 | **DUDA** | #830-#831 «¿cuántas velas a cada lado / valían un máximo o mínimo estructural? ¿a qué te»; #835 «pues tú en cuenta, o sea, las mechas» | Le preguntan por la definición del pivote y contesta con las mechas y un ejemplo con deícticos (#838-#845, «aquí y aquí»). Dice con qué se mapea, no cuándo está formado. El «cierra la vela de H4» de #809 es del cierre agresivo del trade | `fr-v3-982da728/3865000` (1:04:25), no medido |
| 3 | v3 | 1:07:40-1:09:17 | NO RESPONDE | #875 «ver la contra si hay un flujo bajista hay una vela contraria marcarlo acá y eso es ahora» | Order blocks en M5 y M1 («el flujo de órdenes está desarrollando en m5 no en m1», #870), no la liquidez de M15 | — |
| 4 | v3 | 1:14:26-1:16:44 | **DUDA** | #975 «porque yo puedo poner cuántas velas a cada lado y invalidar un máximo y decir, pues, yo lo que hago es mapear de tal manera la estructura»; #976 «si hay un flujo alcista, una vela contraria, pues marca un mínimo si es roja y eso, y al revés, si el flujo es bajista, una vela verde, pues una vela alcista marca un retroceso y eso.» | Es general sobre **qué vela** marca el extremo, la contraria al flujo, y rehúsa expresamente contar velas a cada lado. Pero **no dice cuándo**: al iniciarse la vela contraria o a su cierre. Su ítem, `ev-v3-011540-5425b533`, tiene el tema `mapeo.m1.vela_contraria_marca_extremo`: lo registra como mapeo de M1, no de M15 | `fr-v3-982da728/4540000` (1:15:40), **citado** en el cuestionario de la sesión 1 del kit con ese ítem; no consta medición en pantalla |
| 5 | v4 | 0:27:16-0:29:24 | **DUDA** | #461-#462 «está bajista trata entonces ya sabes que aquí la vela contraria pues ya te está diciendo que / ese es ese nivel de allí este nivel aquí pues es muy posible» | La vela contraria señala el nivel, pero en un ejemplo y con deícticos. El «ya tiene la vela cerrada» de #466 es del tiempo para calcular el lote de la orden límite | `fr-v4-9ad0ebb8/1681000` (0:28:01), no medido |
| 6 | v4 | 0:34:22-0:36:01 | **DUDA** | #597-#601 «cual y ya apenas una manera de identificarlos es la vela contraria o sea estas son un flujo / bajista, se desarrolla una vela / alcista, entonces ya / claramente tienes que, ya marcas / la zona de M15» | Casi general («una manera de identificarlos»): cuando se desarrolla la vela contraria, se marca la zona de M15. Pero «se desarrolla» no separa el inicio del cierre, y está dicho sobre un ejemplo | `fr-v4-9ad0ebb8/2116000` (0:35:16), no medido |
| 7 | v4 | 0:44:15-0:45:51 | NO RESPONDE | #773 «ya vas a poner el break even allí o sea apenas rompe esto o cierra la vela pues ya proteges y» | Break even | — |
| 8 | v4 | 0:49:15-0:51:41 | **DUDA** | #836 «A ver, siguiente es, cuando marcas la zona de liquidez en M15, ¿tomas el último pico que ya se formó del todo o simplemente el punto más alto de las últimas velas aunque sigan en curso?»; #844-#846 «Ah, o sea, por ejemplo, en este caso / Tenemos aquí en M15 / Uno ya formado»; #849 «Por encima de este ya formado» | Es la acotación de ADR-0045: formado, no en curso. Pero contesta **con el ejemplo** («en este caso», «aquí») y no dice cuándo está formado. Después el interlocutor pide que sea «un poco más claro en esa pregunta» (#852), y la respuesta pasa a la toma con cuerpo (#853-#857). Ítem `ev-v4-005053-885e2773` | `fr-v4-9ad0ebb8/3048000` (0:50:48), no medido |
| 9 | v4 | 0:57:21-0:59:14 | **RESPONDE → al iniciarse la vela contraria** | #942 «Entonces, la vela contraria para mí, apenas se inicia una vela contraria en un flujo de órdenes, yo ya lo tomo como un punto en el cual yo ya voy marcando, por ejemplo, en ese caso, si sé que la vela MX se me ha desarrollado, yo ya, o sea, no tenemos nada aquí, sé que aquí, entonces yo ya marco y sé que esperaría un breaker en M1 para seguir operando.» | Lo enuncia en general («para mí, apenas se inicia una vela contraria en un flujo de órdenes») y dice cuándo un punto cuenta como marcado: **en cuanto empieza la vela contraria**, sin esperar a su cierre. Por el contexto es M15: después espera el breaker en M1, aunque la cruda dice «la vela MX». Ítem `ev-v4-005749-1e9325cb`. **Notas para el consultor** en la sección de las dudas, punto 2 | `fr-v4-9ad0ebb8/3486000` (0:58:06), no medido. Su vecino inmediato, `fr-v4-9ad0ebb8/3426000` (0:57:06), **sí está medido**: la línea horizontal «15 lq» del token `liquidez_m15` |
| 10 | v4 | 1:07:40-1:09:15 | NO RESPONDE | #1157 «la operación lo más rápido posible se cierra la vela y si no termina por debajo con un rompimiento» | Gestión de una entrada activada sin ruptura (cerrar la operación) | — |

## Recuento

| pasajes | RESPONDE | DUDA | NO RESPONDE |
|---|---|---|---|
| 10 | 1 (P9) | 5 (P2, P4, P5, P6, P8) | 4 (P1, P3, P7, P10) |

## Las dudas, para el consultor

1. **Las cinco DUDAS y el que responde van en la misma dirección.** El extremo lo marca **la vela
   contraria al flujo** (P4, P5, P6 y P9), y no un recuento de velas a cada lado, que el trader
   rehúsa expresamente (P4, #975; P2 contesta «las mechas»). Lo que las separa es el **cuándo**:
   solo P9 lo dice, «apenas se inicia».
2. **P9 frente a P8, posible tensión.** A la pregunta «¿el último pico que ya se formó del todo, o
   el punto más alto de las últimas velas aunque sigan en curso?», P8 contesta «Uno ya formado».
   P9 marca el punto «apenas se inicia una vela contraria», con esa vela todavía en curso.
   - **Pueden ser compatibles:** la vela que hace el extremo ya cerró, y la que está en curso es
     la contraria.
   - **Pueden no serlo:** mientras la vela contraria está en curso, su mecha todavía puede superar
     el extremo.

   **El texto no lo decide.** Si se leen como opuestos, la regla global manda preguntar.
3. **P9 dice «voy marcando»**, que puede ser una marca provisional que se ajusta, y no la marca
   definitiva.
4. **El ítem de P4 está registrado como mapeo de M1** (`mapeo.m1.vela_contraria_marca_extremo`), y
   su fotograma ya se llevó al cuestionario de la sesión 1. Si la regla de la vela contraria vale
   igual en M15 es lectura, no cita. P6 la dice de M15 («ya marcas la zona de M15»), y P9 por el contexto.
5. **Ningún fotograma de los que deciden está medido.** Los de P6, P8 y P9 están localizados por la
   transcripción, así que abrirlos es posible por ADR-0038. Esta rama no los abre.

## Estado

CLASIFICADO. La regla global no se ha aplicado: la aplica el consultor.
