# El arnés del motor

Rama `trabajo/arnes-motor`, 2026-09-25. Sin merge, sin tag y sin push. ADR-0048. Next Action 28.

Guardas verificadas al empezar: `docs/validation/PREREGISTRO.md` con blob `52649183…`, el declarado;
cero autorizaciones. Nada del material de septiembre; mayo no se ejecuta; febrero no se toca. No se
ha tocado la spec ni `ambiguedades.yaml`.

## 1. Lo que se leyó antes de escribir

- **El criterio** (`cases/criterio_fidelidad.py`, ADR-0043):
  - consume `Operacion(dia, sesion, direccion, instante, entrada)`, con el instante del LLENADO;
  - empareja «uno a uno y determinista»: menor Δinstante, luego menor Δentrada, luego la más
    temprana. Solo casan operaciones del mismo día, sesión y dirección, dentro de las tolerancias
    de `criterio_fidelidad.yaml`;
  - `medir` devuelve `cobertura` y `precision` como `Fraction` o `None` («sin definir»).
- **Los casos `dev`**: uno por día, con `operaciones` en lista cerrada (`instante_utc`, `sesion`,
  `direccion`, `entrada`, `stop`). Construcción tiene 42 días `dev` (21 por mes, del reparto
  dev-visto de ADR-0042), 35 con caso y ninguno oculto.
- **Las velas**: `cargar_serie` por dataset mensual, y `data/agregacion.agregar` con la rejilla por
  reloj de pared: «un límite sin M1 no produce vela».
- **`domain/sesgo.sesgo_h4(velas_h4, apertura, tope, criterio) → ResultadoSesgo`**: solo cuentan las
  H4 con `fin <= apertura`.
- **La compuerta**: las velas no pasan por ella («leer velas para recalcular una ventana no es
  abrir», ADR-0021 §1). Un caso se lee solo si no está en `casos_ocultos`, y `abrir_caso` rechaza
  siempre un retirado.
- **La sesión**: `kit/config.yaml` declara dos, «07-11» y «11-15». Un día tiene dos, y una sesión
  puede tener varias operaciones.

## 2. La parada, y la decisión

**El brief original pedía una cadena lineal de reglas**: «cada regla es una función pura [...] con
el estado que dejaron las reglas anteriores». Contradecía:
- **ADR-0030 §1-2**: el motor «recorre el árbol genérico de `forma` [...] y despacha por nombre a
  primitivas», y descarta el «código a mano por regla»;
- **ADR-0018 §2**: «El orden del fichero deja de tener semántica»;
- **ADR-0028 §4**: punto fijo con refracción.

Además, las sesiones «independientes» contradecían los hechos que la spec hace cruzar de una a otra
(`detenido_por_tope`, `detenido_por_cartuchos`). La sesión paró antes de escribir.

**El consultor eligió la opción (a)**: mantener ADR-0030, ADR-0018 y ADR-0028 tal cual, con un ADR
que los complementa. Es ADR-0048.

## 3. El contrato

**Entrada:**
- los días `dev` de los meses de construcción (`arnes.dias_de_construccion`), por la compuerta;
- sus H4, con el mes anterior como calentamiento (`arnes.dias_de_mercado`);
- la spec vigente (`spec.modelo.cargar_reglas` y `cargar_vocabulario`) y el registro.

**El motor** (`engine/motor.MotorSpec`) corre UN DÍA:
- un evento por cada cierre de M1, desde la apertura de la primera sesión hasta el cierre de la
  última;
- un `EstadoDia` que cruza las dos sesiones;
- en cada evento, el intérprete (`engine/interprete`) recorre las reglas a punto fijo con
  refracción y precedencia por clase.

**Salida:**
- las operaciones del bot, como `criterio_fidelidad.Operacion` (hoy ninguna);
- una traza por sesión: hechos fijados con su instante, primitivas `NO_IMPLEMENTADA` por regla,
  acciones bloqueadas y la anotación de RN-003.

El arnés (`engine/arnes`) mide con `medir` sin tocarlo y escribe el informe.

## 4. Las reglas y sus primitivas

Una regla se ejecuta entera solo si todas sus primitivas están escritas. Las escritas son las de
reloj (`abre_sesion_operativa`, `en_ventana`, `alcanza_hora`), `rompe` sobre la H4 previa (RN-003,
con `domain/sesgo.py`) y la acción `fijar`.

| regla | clase | estado en el arnés |
|---|---|---|
| RN-001 | gate | escrita entera |
| RN-002 | terminal | `accion:cerrar_a_mercado` |
| RN-003 | disparador | escrita entera (`rompe` solo con `vela_h4_previa`) |
| RN-004 | disparador | `predicado:alcanza_nivel`, `predicado:cruza` |
| RN-005 | gate | `predicado:se_desarrolla_en_el_lado_de_ruido` |
| RN-006 | disparador | `accion:reubicar_orden_limite`, `predicado:se_completa_zona_de_control` |
| RN-007 | disparador | `accion:agrupar_estructura`, `predicado:se_mapea_estructura` |
| RN-008 | gate | `predicado:se_da_esquema` |
| RN-009 | gate | `predicado:zonas_desarrolladas_superan` |
| RN-010 | disparador | `accion:gestionar_salida`, `predicado:se_activa_entrada` |
| RN-011 | disparador | `accion:dimensionar_lote`, `accion:escribir_stop_en_la_orden`, `predicado:toca_colocar_orden_limite` |
| RN-012 | disparador | `accion:realizar_perdida`, `predicado:salta_stop` |
| RN-014 | disparador | `accion:mover_stop`, `predicado:se_completa_zona_de_control` |
| RN-015 | disparador | `accion:colocar_orden_limite`, `accion:fijar_objetivo` |
| RN-016 | gate | `acumulador:cartuchos`, `predicado:se_cierra_operacion` |
| RN-017 | disparador | `predicado:se_cierra_operacion` |
| RN-018 | gate | `predicado:operaciones_abiertas_alcanzan` |
| RN-019 | disparador | `accion:reentrar`, `predicado:se_cierra_operacion` |
| RN-020 | gate | `acumulador:perdida_dia`, `acumulador:perdida_semana` |
| RN-021 | disparador | `predicado:contexto_filtrable` |
| RN-022 | fallback | `accion:abstenerse`, `predicado:ninguna_regla_de_entrada_aplica` |
| RN-026 | gate | `accion:abstenerse`, `predicado:distancia_menor_que` |
| RN-027 | gate | `accion:redondear_lote`, `predicado:no_es_multiplo_de` |
| RN-029 | gate | `acumulador:perdida_dia_firma` |
| RN-030 | terminal | `accion:cerrar_a_mercado`, `acumulador:perdida_dia_firma`, `acumulador:perdida_total_firma` |
| RN-031 | gate | `acumulador:perdida_total_firma` |
| RN-032 | gate | `acumulador:perdida_dia_firma`, `acumulador:perdida_total_firma` |

RN-013, RN-023, RN-024, RN-025 y RN-028 están DESCARTADAS y el arnés no las recorre. La tabla sale
de la spec y del registro de primitivas, calculada por script, no escrita a mano.

## 5. Los tests nuevos

`tests/unit/test_arnes_motor.py`, sobre velas y días sintéticos fechados en 2030:
- **Kleene**: una primitiva que falta vale DESCONOCIDO y no decide en `todos_de`, `cualquiera_de` ni
  `ninguno_de`.
- **Una regla desconocida no fija**, y **un `gate` desconocido bloquea la acción con efecto** que
  podría prohibir.
- **Sin mirar al futuro**: añadir velas posteriores al instante T no cambia nada de lo decidido hasta
  T, y el motor nunca entrega una H4 con fin posterior al evento.
- **NO_IMPLEMENTADA detiene la sesión** y queda en el embudo: RN-004 en `predicado:alcanza_nivel`, y
  ninguna operación.
- **Negativa**: medida y lo que no es construcción se rechazan antes de leer. También por la CLI,
  que sale con código 2 sin escribir nada.
- **Centinela**: un día oculto con un fichero roto y una marca dentro no se lee: da
  `HoldoutCerradoError`, sin la marca ni la fecha en el mensaje. Sin la compuerta, ese mismo fichero
  sí se leería y fallaría, así que el centinela está vivo.
- **Un motor que copia al trader** da cobertura y precisión del 100 %, todos los hechos y ninguna
  parada.
- **Un motor que no opera** da cobertura 0 y precisión «sin definir», no 0 ni 100.
- **Determinismo**: el mismo informe byte a byte en dos ejecuciones.

## 6. La línea base

`docs/validation/ARNES-MOTOR-LINEA-BASE.txt`, tal cual, escrito con
`uv run botsito motor arnes --salida docs/validation/ARNES-MOTOR-LINEA-BASE.txt`. Una segunda
ejecución da el mismo fichero byte a byte (`cmp`).

- **Criterio**: 77 operaciones del trader, 0 del bot; cobertura **0/77**; precisión **sin definir**.
- **Embudo**, sobre las 49 sesiones con operaciones del trader:
  - `sesgo` en **43 de 49**;
  - `liquidez_tomada`, `orden_dimensionada`, los tres `detenido_*` y la operación del bot en
    **0 de 49**.
- **Dónde se paran**, las 49:
  - `liquidez_tomada` en `predicado:alcanza_nivel` y `predicado:cruza` (RN-004; el token
    `liquidez_m15` no tiene productor mientras A-35 siga abierta);
  - `orden_dimensionada` en `predicado:toca_colocar_orden_limite` (RN-011);
  - los frenos en sus acumuladores.

  Es lo esperado: RN-003 se supera y el camino hacia la operación se detiene en la primera
  primitiva `NO_IMPLEMENTADA` de cada hecho.

**El contraste con el diagnóstico de RN-003** (`MOTOR-SESGO-H4.md`: 58 a favor, 12 en contra, 7
ambiguas, 0 insuficientes, sobre 77 operaciones). El diagnóstico cuenta **operaciones**; el embudo,
**sesiones**:

| | por operación | por sesión |
|---|---|---|
| total | 77 | 49 |
| sesgo alcista o bajista | 70 (58 a favor + 12 en contra) | 43 (21 alcistas + 22 bajistas) |
| ambiguo | 7 | 6 |
| insuficiente | 0 | 0 |

**Por operación, el arnés reproduce el diagnóstico exactamente**: a favor 58, en contra 12,
ambiguo 7. Por sesión son 6 ambiguas, porque una sesión ambigua tiene dos operaciones. Las 43
sesiones con `sesgo` son las 21 + 22 que no son ambiguas. Cuadra, y no hay diferencia que explicar.

## 7. Tiempo y memoria

**38,6 s y 37,8 s**, en dos ejecuciones sobre los 42 días, con un pico de **32,4 MiB** medido con
`tracemalloc`, que cuenta lo que asigna Python y no el proceso entero. El comando lo imprime por
pantalla y fuera del informe, para que el informe siga siendo determinista.

## 8. Huecos de interpretación

Están en ADR-0048, H1-H6, y ninguno se ha inventado en el código:
- **H1**, RN-003: la forma no expresa AMBIGUO ni INSUFICIENTE;
- **H2**, las sesiones salen de `kit/config.yaml`;
- **H3**, el orden por id dentro de una clase;
- **H4**, sin ticks ni bróker simulado;
- **H5**, `permite` no cambia nada;
- **H6**, cada día empieza de cero.

Lo que A-39 deja abierto es PROVISIONAL.

## Estado

WAITING_FOR_USER_VALIDATION.
