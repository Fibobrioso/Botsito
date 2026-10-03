---
status: ACTIVE
date: 2026-10-02
phase: post-F14 (rama `feature/cierres-de-mercado`, A3 e) de «Pendientes heredados»)
---

# 0068 · La ventana prohibida antes de un cierre de mercado largo vive en el puerto del broker, con un calendario versionado por perfil

> **PROVISIONAL en dos cosas.** (1) `cierre_pendientes`, DEFAULT_AMBIGUOUS bajo A-55: la regla
> escrita de FTMO no dice qué pasa con una pendiente. (2) El huso del calendario, `America/New_York`,
> que supone que el servidor cambia de hora con EE. UU. Lo dice una Trading Update, no una medida, y
> A-28 (`broker_dst`) sigue abierta (revisor, a1). Con cualquier lectura de A-28 (`us`, `eu` o
> `ninguno`), el cierre del viernes cae entre las 21:55 y las 23:55 de Madrid, y su ventana nunca
> toca la operativa. Las dos horas de margen y el mínimo de dos horas son de R15 y están CONFIRMED.
> Es una tarea autónoma: el consultor no lo ha revisado todavía.

## Decision

### 1. Un predicado único, en el dominio, al que pregunta el broker

`ventana_prohibida_por_cierre(instante, calendario, margen, minimo)`, en `domain/cierres.py`, sin
IO ni reloj. Devuelve `None` o la prohibición con su motivo:
- `cierre_mercado`: desde `margen` antes de un cierre de `minimo` o más hasta que el cierre acaba.
  Los dos bordes de R15 van dentro: «two hours or less before», «closed for at least two hours». Con
  el mercado cerrado tampoco se coloca;
- `cierre_sin_calendario`: fuera del tramo que cubre el calendario. Ahí no se sabe, así que el bot
  se abstiene (MASTER_PLAN H.2).

Lo consulta el broker en `_colocar` y en `modificar` (una pendiente), ANTES que el freno de
peticiones. Las siete reglas que envían peticiones pasan por esos métodos (ADR-0067 §1), así que
ninguna se lo salta. Lo negado devuelve un `Rechazo` con su motivo, no llega al servidor y no se
cuenta.

### 2. Lo que se hace dentro de la ventana

- **Colocar** (límite o stop): se niega.
- **Modificar una pendiente** (RN-006): se niega, y la orden sigue como estaba. Se toma como
  colocarla en otro precio. R15 no lo dice, así que va como pregunta en A-55. Con `cancelar`, el
  valor de partida, no llega a pasar: la pendiente ya se canceló al empezar la ventana (revisor, b2).
- **Una pendiente ya puesta**: lo dice `cierre_pendientes` (`cancelar` | `mantener`), DEFAULT
  `cancelar` bajo A-55. Con `cancelar`, el broker la cancela al empezar la ventana, antes que
  cualquier llenado de ese instante. Es lo que protege la cuenta: sale siempre y cuenta como
  petición (ADR-0067 §3).
- **Una posición abierta**: nada. R7 permite en Swing mantenerla de noche y el fin de semana.
- `abrir_conocida` (repetir una operación del trader) no pasa por el predicado, porque no la emite
  el bot.
- **Más allá de la letra de R15**, y declarado: se niega también con el mercado cerrado (el servidor
  rechazaría la orden) y fuera de lo que cubre el calendario (abstenerse).

### 3. Instantes absolutos; el huso, en cada hora declarada

La ventana es una duración antes de un instante, en milisegundos UTC, y nunca depende de un reloj de
pared. El reloj solo entra al convertir la hora declarada de un cierre en un instante, cada una con
su huso (como los libros, ADR-0039). El servidor de FTMO cierra EURUSD a las 23:55 de su reloj. Según
la Trading Update del 5-mar-2026, ese reloj cambia de hora con EE. UU., así que se declara como 16:55
`America/New_York`. Es PROVISIONAL: lo que A-28 mide observando una transición, y sigue abierta.
Cuando A-28 se cierre, el huso del calendario se revisa con ella. No se leen `broker_offset_base` ni
`broker_dst`.

### 4. El calendario: versionado por perfil, unido a la plataforma por la más restrictiva

`knowledge/cuentas/cierres/<perfil>.yaml`, leído por `engine/calendario_cierres.py`. Lleva `cubre`,
la pauta `semanal` y la `diario` y los `extraordinarios`, cada uno con su fuente (Trading Updates de
FTMO y API de símbolos). En vivo, el adaptador de MetaTrader convierte las sesiones del símbolo
(`SymbolInfoSessionTrade`) en cierres con `cierres_desde_sesiones` y las une al calendario con
`unir_cierres`: gana la unión, y cada cierre largo que una fuente trae y la otra no va al log como
discrepancia.

### 5. Los parámetros

- `firma_gap_margen_minutos` = 120 y `firma_gap_cierre_minimo_minutos` = 120: `prop_firm`,
  CONFIRMED, de R15. Van en el perfil de FTMO y en `parametros.yaml`, con el mismo valor.
- `cierre_pendientes` = `cancelar`: `ejecucion`, DEFAULT_AMBIGUOUS bajo A-55.

### 6. Todo queda escrito

Cada negada y cada pendiente cancelada al empezar la ventana van al log (INFO) y a `Traza.cierres`
con su motivo. El informe del arnés lleva la sección «Los cierres de mercado (ADR-0068)».

### 7. El simulador no corre fuera del calendario

`construir_motor_cableado` carga el calendario del perfil y se niega a correr un día fuera de
`cubre`, como con un parámetro UNKNOWN: así un calendario vencido no cambia una medida en silencio.

## Problema que resuelve

R15 de `docs/validation/FTMO-REGLAS.md` prohíbe abrir «two hours or less before a relevant financial
market is closed for at least two hours», y el ticket VDW-DPMWR-965 lo confirma (traslado de Aleks
del 29-09-2026). El bot no tenía calendario de cierres (A3 e) de «Pendientes heredados»).

## Alternativas consideradas

1. **Una condición en las reglas de la spec** (RN-001): una regla nueva o una acción olvidada se la
   saltaría. El encargo la pide donde ninguna regla pueda saltársela.
2. **Solo las sesiones de MT5**: por su firma (`día de la semana`, `índice`) no expresan una fecha,
   así que un festivo no sale. Además, en el simulador no hay MT5.
3. **Solo el calendario versionado**: no ve un cierre que FTMO publique el jueves para el lunes si
   nadie lo apunta.
4. **La ventana en el reloj del servidor**: el registro lo tiene UNKNOWN (A-28), y una duración no
   necesita reloj.
5. **Seguir abriendo fuera del calendario**: aproximaría.

## Por que elegimos esta opcion

Es la única que cumple «ninguna regla puede saltárselo» y que dice de dónde sale cada cierre. Y no
cambia ningún día medido: ningún cierre largo de EURUSD en FTMO empieza antes de las 17:00 de
Madrid entre el 4-12-2025 y el 7-10-2026 (`docs/validation/CIERRES-DE-MERCADO.md` §0.2).

## Por que descartamos las demas

Ver «Alternativas consideradas».

## Impacto

- **Código**:
  - `domain/cierres.py` (nuevo);
  - `engine/calendario_cierres.py` (nuevo);
  - `engine/broker.py` (`ReglasBroker.cierres`, el predicado en `_colocar` y `modificar`, la
    cancelación al empezar la ventana, `Traza.cierres`);
  - `engine/simulacion.py` (`reglas_broker_de(perfil, registro, calendario)`);
  - `engine/cableado.py` (carga el calendario, se niega fuera de `cubre`, y lo informa).
- **Knowledge**:
  - `knowledge/cuentas/cierres/ftmo-2step-swing-100k.yaml` (nuevo);
  - dos parámetros en el perfil y en `parametros.yaml`, y `cierre_pendientes`;
  - A-55, nueva.
- **Tests**: `tests/unit/test_cierres_de_mercado.py`.
- Medido en `docs/validation/CIERRES-DE-MERCADO.md`.

## Fecha / fase

2026-10-02 · rama `feature/cierres-de-mercado`. `PROJECT_STATE.md`, «Pendientes heredados», A3 e).

## Estado

ACTIVE (PROVISIONAL en `cierre_pendientes`: se revisa con A-55, con la respuesta de soporte de FTMO)
