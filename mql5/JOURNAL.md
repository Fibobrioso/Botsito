# El journal de la capa de MT5 · formato v1

El registro que escribe el EA de la capa que nunca decide una operación (ADR-0082; R6a.1, rama
`trabajo/ea-conexion`). **Un solo formato, versionado** (ADR-0082 D7), definido aquí una vez. Lo
escribe `mql5/Include/Botsito/Capa/Journal.mqh` y lo valida
`src/botsito/mql5bridge/journal.py`, que recalcula la cadena sobre los mismos bytes; el golden de
`tests/golden/journal/` lo escriben los dos. Decidido en la respuesta del consultor a la PARADA de
la fase 0 (`docs/validation/EA-CONEXION.md`, puntos 3 y 6). Cambiar cualquier cosa de este
documento es una **versión nueva** (`v` 2), con su lector.

## Los bytes

- Un objeto JSON por línea, **UTF-8 sin BOM**, fin de línea **LF** (nunca CR), y la última línea
  con su LF: una última línea sin LF es una línea **truncada**.
- Cada línea es la **forma canónica** de su objeto: las claves de la tabla, en ese orden, sin
  espacios fuera de los textos, y sin escapar lo que no es ASCII. En los textos se escapan `"` y
  `\` (`\"`, `\\`), `\b`, `\f`, `\n`, `\r` y `\t` con su forma corta, y el resto de los caracteres
  por debajo de U+0020 como `\u00xx` en minúsculas. Es lo que da, en Python,
  `json.dumps(objeto, ensure_ascii=False, separators=(",", ":"))`.
- El EA lo escribe en modo binario (`FILE_BIN`), con los bytes UTF-8 de `StringToCharArray(…,
  CP_UTF8)` sin el 0 final, y `FileFlush` tras cada línea. No en modo texto: en modo texto MT5 pone
  CRLF (medido, `EA-CONEXION.md` §0.c).

## La cadena

`h(n) = SHA-256(b(n))`, donde `b(n)` son los bytes de la línea `n` **sin el LF**; la línea `n+1`
lleva `"prev": h(n)` en hexadecimal en minúsculas (64 caracteres). La primera línea de una cadena
lleva 64 ceros. `seq` empieza en 1 en cada cadena y sube de uno en uno, entre ficheros y entre
reinicios. Cambiar un byte de una línea cambia su hash y rompe el `prev` de la siguiente. Límite:
borrar las últimas líneas no se detecta (ninguna cadena sin sello lo detecta).

## Las claves (siempre todas, en este orden)

| clave | qué es | v1 |
|---|---|---|
| `v` | versión del formato | `1` |
| `seq` | número de secuencia | entero desde 1 |
| `srv` | hora del servidor, `TimeTradeServer()` | `"AAAA-MM-DDTHH:MM:SS"`, sin huso |
| `gmt` | hora GMT, `TimeGMT()`: **sale del reloj del ordenador**, que tiene que estar en hora | ídem |
| `desfase_s` | `srv − gmt`, en segundos (el «offset servidor» de MASTER_PLAN §H.2) | entero |
| `ev` | el evento | ver abajo |
| `datos` | los datos del evento, exactamente las claves de su fila | objeto |
| `regla` | la regla que actuó (§H.2) | `null`: reservada (F23; R6a.4 en adelante) |
| `condicion` | la condición que falló (§H.2) | `null`: reservada |
| `capa_hash` | el hash de lo que la capa recibe generado (ADR-0082 D5) | `null`: reservada para R6a.2 |
| `spec_hash` | el hash de la spec (§H.2, F28) | `null`: reservada (desde F29) |
| `risk_hash` | el hash del riesgo (§H.2, F28) | `null`: reservada (desde F29) |
| `ambiguas` | las lecturas ambiguas (§H.2) | `null`: reservada |
| `prev` | el hash de la línea anterior | 64 hexadecimales |

## Los eventos de v1 y sus datos

| `ev` | cuándo | `datos` |
|---|---|---|
| `arranque` | al arrancar, tras la negativa de `OnInit` | `version_ea`, `build`, `simbolo` (el del gráfico), `conectado`, `cadena_anterior` (`ninguna`, `sigue` o `rota`) |
| `cuenta` | al estar conectado (`TERMINAL_CONNECTED`), la primera vez tras cada arranque | `trade_mode`, `margin_mode` (los nombres de sus enum), `servidor`, `conectado` |
| `negativa` | al conectar, si el modo leído no es DEMO; después, `ExpertRemove()` | `trade_mode`, `motivo` |
| `reloj` | junto a `cuenta` | `time_current`, `time_trade_server`, `time_gmt`, `time_local` (horas), `desfase_servidor_gmt_min`, `desfase_local_gmt_min` (`-TimeGMTOffset()/60`), `time_gmt_offset_seg`, `horario_verano_local_seg` (`TimeDaylightSavings()`) |
| `sesiones` | junto a `cuenta` y en cada cambio de día | `trade` y `quote`: los siete días, de `SUNDAY` a `SATURDAY`, cada uno con la lista de sus sesiones `[desde_s, hasta_s]` (segundos desde las 00:00 del día del servidor) de `SymbolInfoSessionTrade` y `SymbolInfoSessionQuote`; `tope_alcanzado` |
| `latido` | cada `LATIDO_SEG` segundos | `conectado`, `time_current` |
| `cambio_de_dia` | la primera vez que el día del servidor (`srv`) cambia | `dia_anterior`, `dia_nuevo` (`AAAA-MM-DD`) |
| `fin` | en `OnDeinit` | `motivo` (el `reason`) y `motivo_texto` (el nombre de su constante, `REASON_…`) |

Ni login, ni datos personales, ni saldo, ni ninguna cifra de dinero (D2f): el validador rechaza
cualquier clave de `datos` que no sea de esta tabla. `quote` se registra sin usarlo; R6a.5 decide si
sirve (respuesta a la PARADA, punto 7).

## Las dos cifras del formato

Son parte de v1 (respuesta a la PARADA, punto 6): cambiarlas es una versión nueva. No son de la
firma, del bróker, del instrumento ni de la ejecución (D2g); R6a.2 puede generarlas si se decide.

- `LATIDO_SEG = 60`: el periodo del latido, en segundos (`EventSetTimer`).
- `TOPE_SESIONES = 32`: cuántos índices de sesión se piden como mucho por día. El bucle sube el
  índice hasta que la función devuelve `false` (error 4307, `ERR_MARKET_SESSION_INDEX`); el tope
  solo evita un bucle sin fin, y si se alcanza, `tope_alcanzado` es `true`.

## Los ficheros

`MQL5\Files\Botsito\journal_AAAAMMDD.jsonl`, uno por **día del servidor** (`srv`). Se abren con
`FILE_READ|FILE_WRITE|FILE_BIN|FILE_SHARE_READ` y se escribe al final (`FileSeek`): nunca se
truncan. `FILE_SHARE_READ` deja leerlos a otros mientras el EA los tiene abiertos, pero copiarlos con
el EA puesto **no está medido**: las copias de la demo se hicieron con el EA quitado.

- **La cadena sigue entre días y entre reinicios.** Al arrancar, el EA busca el journal más
  reciente de la carpeta y lee su última línea: si valida (acaba en LF, empieza por `{"v":1,"seq":`
  y acaba en `"prev":"<64 hex>"}`), sigue con su `seq + 1` y su hash (`cadena_anterior: sigue`); si
  no hay ninguno, empieza de cero (`ninguna`); si la última línea no valida, empieza una cadena
  nueva desde ceros (`rota`).
- El cambio de día abre el fichero del día nuevo; su primera línea (`cambio_de_dia`) lleva el `prev`
  de la última del día anterior.
- El validador lee uno o varios ficheros, en orden, como una sola cadena; una cadena nueva en medio
  solo es válida si la abre un `arranque` con `cadena_anterior: rota`:

      uv run python src/botsito/mql5bridge/journal.py <fichero> [<fichero>...]

## Cómo lo leerán F23 y F34

F23 (el journal del simulador en Python) escribe esta misma v1 —los campos de §H.2 son las claves de
la tabla— con el mismo validador; hoy el validador vive en `botsito.mql5bridge`, que `engine` no
puede importar (import-linter): cuando F23 lo necesite, el esquema baja a una capa que `engine` vea,
en su rama (Technical Debt). F34 compara la demo con el backtest línea a línea por `(día, ev, regla,
condicion)`, sin mirar `seq` ni `prev`, que solo prueban la integridad de cada lado.
