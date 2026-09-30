# Plan de la noche del 30 de septiembre al 1 de octubre de 2026

Rama `trabajo/nocturno-01oct`, **desde `14e01bc`** (el `docs(state)` de `stable/F31b-ci-a27`), que
es el último `main` con la CI en verde confirmada. No sale de `main`: el cierre de
`trabajo/memoria-suite` (`stable/F31c-memoria-suite`, `main` en `67ab298`) terminó con la CI en
rojo, y la instrucción de Aleks para ese caso era no arreglarlo, no tocar `main` y partir de aquí.
Va anotado al principio del informe de la noche.

Sesión autónoma: Aleks duerme. **Nada sobre `main`, ningún push, ninguna rama cerrada ni borrada,
ninguna credencial, ninguna conexión a bróker ni a MetaTrader, ninguna descarga de datos ni
dependencia nueva.** Cada commit entra con `make check` en verde y sellado.

## 1. Qué funcionalidades son «F32 en adelante»

La numeración sigue la de los tags (`stable/F31c-memoria-suite` es el último), no la de la tabla A
de `docs/plan/MASTER_PLAN.md`, donde F32 es la paridad con el Strategy Tester y exige MetaTrader,
que esta noche no se toca. Las funcionalidades pendientes y su orden son los de `PROJECT_STATE.md`,
Next Action A3 (orden del consultor del 2026-09-29), que a su vez es la lista de
`docs/validation/ACTIVAR-SESION-03.md` §3: lo que la spec dice desde la sesión 3 y el motor todavía
no hace.

| n.º | Funcionalidad | De dónde sale | Estado al empezar |
|---|---|---|---|
| F32 | El sesgo: la doble ruptura la decide el color (RN-003, RN-033) y el cierre antes del fin de la vela H4 (RN-002) | A3.a; desalineaciones 1 y 2 | desbloqueada |
| F33 | Sesiones independientes: `liquidez_tomada` caduca al abrir la sesión; la caja por operación | A3.b; desalineación 3; ADR-0056 §4 | la primera parte, desbloqueada; la caja por operación depende de candidatas sin decidir (C1) |
| F34 | Gestión: el stop se redondea alejándose de la entrada; la toma de RN-004 en la vela de M1; el break even al tocar | A3.c; desalineaciones 4 y 5 | las dos primeras, desbloqueadas; el break even necesita una lectura de «zona de control posterior» |
| F35 | La vida de la orden stop (RN-006, rama 3 de ADR-0056) y la vela casi plana (RN-007) | A3.d; desalineaciones 6 y 7 | la orden stop, con selectores y diagnóstico; RN-007 **bloqueada**: el trader no dio el umbral |
| F36 | Separar el reloj de las sesiones del reloj del día de riesgo | A3.0; desalineación 9; ADR-0059 | desbloqueada como mecanismo; el valor (UTC+2 fijo) lo decide el consultor con A-42 |
| F37 | Calendario de cierres de mercado para la regla de gap trading de FTMO | A3.e; Technical Debt del 2026-09-29 | **bloqueada a priori**: no existe el calendario de cierres del bróker |

Se intentan en ese orden. Si una no se puede hacer sin una decisión de Aleks o sin un dato que no
existe, se anota como bloqueada y se pasa a la siguiente. Si `make check` no queda verde en unos
tres intentos serios, se vuelve al último commit verde, se anota por qué y se pasa a la siguiente.

## 2. Criterios de aceptación, funcionalidad a funcionalidad

Comunes a todas: tests primero, a partir de la spec; ninguna cifra en el código ni en una `forma`
(ADR-0002, ADR-0019); todo cambio de `knowledge/spec/` viaja con `botsito spec docs --escribir`, con
`spec_manifest.yaml` subido de versión y con su trailer `Fuente:`; un ADR nuevo va **PROPUESTO**;
la corrida del arnés sobre construcción (abril y agosto, solo días `dev`, por la compuerta) se mide
antes y después con los mismos diagnósticos y la diferencia se escribe en el informe. Ninguna
corrida toca mayo, marzo, febrero ni septiembre.

### F32 · El sesgo

Fuentes: `fb-2026-09-29-sesion-03-31fb311f` y `fb-2026-09-29-sesion-03-617f496a` (el color),
`fb-2026-09-29-sesion-03-1168f036` (siempre hay sesgo), `fb-2026-09-29-sesion-03-c38c4aef` (el
cierre un minuto antes del fin de la vela H4); ADR-0044 y ADR-0049.

1. Con la vela H4 rompiendo los dos extremos de su anterior, `sesgo_h4` da el lado del color con
   que cierra: verde, alcista; roja, bajista. Con un solo extremo roto el color sigue sin decidir.
2. `insuficiente` se conserva (ninguna ruptura dentro de `sesgo_h4_tope_velas`, que es un tope del
   proyecto y no del trader), y RN-033 sigue prohibiendo con él.
3. En construcción, las sesiones que eran `ambiguo` pasan a tener lado y RN-033 deja de dispararse
   en ellas. Se mide.
4. RN-002: con una posición viva, se cierra a mercado cuando a la vela H4 en curso le queda lo que
   diga un parámetro nuevo del registro (el «un minuto» del trader), **sobre la rejilla de
   `anclaje_h4`**. `ventana_fin` no se toca. Prueba de punta a punta por el cableado sobre el día
   sintético de 2030.

### F33 · Sesiones independientes

Fuente: `fb-2026-09-29-sesion-03-5021677e` (A-46 RESUELTA: «cada uno es un mundo diferente»).

1. El hecho `liquidez_tomada` declara `caduca: al_abrir_sesion`, como `sesgo`: una toma de la
   primera sesión no vale en la segunda.
2. El productor de la zona de entrada (`engine/zonas.py`) deja de guardar una sola toma y un solo
   esquema por día: los de una sesión no sobreviven a la apertura de la siguiente.
3. La caja por operación (ADR-0056 §4): solo si se puede escribir sin decidir la candidata C1 (qué
   pasa con la orden pendiente cuando aparece una caja nueva). Si no, queda anotada.

### F34 · Gestión

Fuentes: `fb-2026-09-29-sesion-03-11910e0a` (el redondeo), `fb-2026-09-29-sesion-03-b2e074e3` (la
toma con una vela de M1), `fb-2026-09-29-sesion-03-9f506366` (el break even al tocar).

1. `escribir_stop_en_la_orden` lee `stop_fraccion_redondeo`, nombrado en la forma de RN-011: con
   `alejandose_de_la_entrada` el stop queda a la distancia redondeada hacia arriba, y el lote sale de
   esa distancia.
2. RN-004: la vela que toma el nivel de M15 es la última M1 cerrada, con cuerpo; deja de ser la
   última M15 cerrada (PROVISIONAL de ADR-0054 §4).
3. Break even: `se_completa_zona_de_control` para RN-014, mirado en M1, con el stop exactamente en
   la entrada. Solo con una lectura de la zona posterior que salga del corpus.

### F35 · La vida de la orden stop

ADR-0056 §7, rama 3: la orden nace en el posible punto de breaker y se mueve con él, con la
tercera lectura de A-29 en diagnóstico. RN-007 no se implementa: falta el umbral de «casi plana».

### F36 · Dos relojes

ADR-0059: un parámetro propio para el reloj de las sesiones, distinto de `huso_operativa`, que se
queda como reloj del día de riesgo. Con los dos relojes iguales la salida no cambia; con el de las
sesiones en UTC+2 fijo, el cableado deja de negarse en invierno. El valor no se cambia esta noche.

### F37 · Calendario de cierres

Solo si existe en el repositorio una fuente de los cierres del bróker. Si no, bloqueada.

## 3. Si se acaban las funcionalidades desbloqueadas

`docs/nocturno/BRECHA-EN-VIVO.md`: inventario de lo que falta entre el código y ejecutar en vivo en
FTMO. Solo documento.

## 4. Cierre de la noche

La rama queda en su último commit verde, con `docs/nocturno/INFORME-01oct.md` commiteado.
