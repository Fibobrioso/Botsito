# VAD-JULIO · La voz que el VAD del ASR se salta en v12 a v14 (R2.5, letra C)

> PLANTILLA: informe de la rama `trabajo/vad-julio`. Estado: EN CURSO, en la PARADA (b) (ninguna
> candidata cumple D3; D4, D5 y la PARADA final esperan). La fase 0, el código, el criterio de D3
> (copiado antes de las corridas), la tabla de candidatas, las desviaciones, las comprobaciones y el
> informe del revisor se escriben aquí según avanza la rama.

Rama `trabajo/vad-julio`, abierta el 2026-11-27 desde `main` en 139800f5 (commit de estado sobre
el merge d44f3e58 del tag `stable/F39r-renovar-cierres-2026-11-26`). Encargo:
`docs/encargos/trabajo-vad-julio.md`. Tramo: R2 (R2.5 de `docs/plan/HOJA-DE-RUTA.md`; la letra C
de la Next Action).

## La base, comprobada al abrir (skill `abrir-rama`, paso 1)

- `git rev-parse main origin/main`: `139800f5c860e0ae32d6dff9c3f836b7359848ca` dos veces.
- `git rev-parse "stable/F39r-renovar-cierres-2026-11-26^{commit}"` = `git rev-parse main^1` =
  `d44f3e58712f58bdbc2207f93f4cc4fb3acea857`; el tag está en origin (`git ls-remote --tags`).
  Es el último tag (`git tag --sort=-creatordate`: F39r, F39q, F39p).
- CI de `main` sobre `139800f5…`: check-run `python`, `completed` / `success`, run 46066643655
  (el que citaba el encargo).
- `git branch --list`: solo `main`; `git ls-remote --heads origin "fix/*"`: vacío.
- 0.1, antes de la fila del día: `casos_reservados(repo)` da 34 casos reservados, ninguno de
  2026-07 (los ids son `caso-eurusd-AAAA-MM-DD`).

## 0. Fase 0 (2026-11-27, inventario, antes de tocar código)

### 0.1 La fila del día

Escrita y estadiada antes del primer `make check` de la rama (HOLDOUT-EXPOSICIONES, 2026-11-27,
«`trabajo/vad-julio`: el trabajo del día»). Antes, `casos_reservados(repo)`: 34 casos reservados,
**ninguno de 2026-07** (contados por el prefijo de fecha del id, sin imprimir ids).

### 0.2 Lo leído, con fichero:línea

- **ADR-0007 §3** (`docs/adr/0007-transcripcion-en-dos-capas.md:20-24`): faster-whisper large-v3,
  `vad_filter=True`, sin parámetros del VAD; el manifiesto anota modelo, versiones y corte.
  **Enmienda 2026-09-06** (`:78-100`): `hotwords` descartado, el tope de 223 tokens del prompt,
  `gpu` fuera de la huella y la retranscripción por `reemplaza_a` sin tocar manifiestos.
- **`motor_whisper.py`** (en `main`): `vad_filter=True` fijo en la descripción (`:159`) y en la
  llamada a `transcribe` (`:174`), sin `vad_parameters`; `describir()` **carga el modelo**
  (`:139`, `self._cargar()`, que descarga y carga los pesos en la GPU) antes de describir.
- **`pipeline_transcripcion.py`** (en `main`): `huella_de(corte, motor)` (`:258-263`) es
  `hash_corto` del JSON ordenado de corte y descripción del motor sin
  `CLAVES_FUERA_DE_HUELLA = ("gpu", "initial_prompt_tokens")` (`:255`). Los manifiestos **no
  guardan la huella**: se recalcula desde su `corte` y su `motor` (`:259-261`).
  `_carpeta_base_registrada_ajena` (`:266-282`) dice si la carpeta base `<nombre>` es de otra
  huella; si lo es, `carpeta_para` abre `<nombre>-<hash_corto(huella+sha256_video)>`
  (`trabajo.py:51-52`): solo la carpeta AJENA lleva sufijo (v12 vive en
  `transcripciones/v12/large-v3-int8-float16`; v13 y v14, con sufijo, porque se retranscribieron
  con otro corte).
- **`scripts/transcribir_sesion.py:559-575`**: importa `huella_de` y construye
  `ConfiguracionWhisper` **por posición** con cuatro campos (`:563-565`). `scripts/` está protegido:
  el campo nuevo va al final y con valor por defecto, y el guion sigue igual.
- **El motor `falso`** (`transcripcion.py:100-128`): un segmento por cada 5 s; `describir()` da
  `{"motor": "falso", "modelo": "falso"}`, sin VAD; la CLI lo crea sin configuración
  (`cli.py:281-282`).
- **`cli.py`**: `corpus transcribe` (`:266-325`, opciones en `:3158-3167`): sin opción de VAD;
  `corpus transcript show` (`:414-457`, `:3175-3186`) filtra con `filtro_de(repo, video,
  _meses_libres(repo))` y lee cualquier versión con `--transcripcion <id>`.
- **`cargar_cruda`** (`pipeline_transcripcion.py:326-332`) devuelve la cruda FILTRADA y solo la
  lista; lo oculto queda en `filtro.ocultos`. **`filtro_de`** (`cuarentena.py:475-476`) construye el
  filtro de un vídeo con sus tramos no citables y los meses libres.
- **VIDEO-JULIO.md**: §0.4 (`:106-123`, quién lee `material_sin_video` y qué rompe cada salida);
  §1.5 (`:1203-1218`, la regla de los huecos de 5 min o más, con `volumedetect`); §1.6 y §1.7
  (`:1220-1292`, las retranscripciones con otro corte, que no cubrieron los huecos); §3.0
  (`:346`) y §3.2 (`:1354-1377`, el criterio de F3 que manda); §3.5 (`:535-567`, 67 operaciones:
  5 COINCIDE, 35 APARECE, 3 NO APARECE, 0 CONTRADICE, 8 NO LOCALIZABLE, 16 sin ver); §4 (`:583-661`);
  §5 (`:569-581`); §6 (`:663-686`, los días 23, 24 y 27 «sin datos»); §10.9 (`:858`); la respuesta a
  la PARADA 4 (`:1379-1410`, la opción (a) y las tres salidas de F5) y a la PARADA final
  (`:923-962`, F5 pasa a esta entrada).
- **AUDITORIA-PROFUNDA-2026-11.md:1223** (P3-09, señalado por el auditor): «la rama del VAD
  convierte las no comprobadas y F5 pasa»; coincide con el encargo.

### 0.3 Los parámetros del VAD de la faster-whisper instalada

Leídos en `.venv/Lib/site-packages/faster_whisper/` (versión 1.2.1, `METADATA`):

| Parámetro (`VadOptions`, `vad.py:37-42`) | Por defecto |
|---|---|
| `threshold` | 0.5 |
| `neg_threshold` | `None` (el paquete lo deriva: `max(threshold - 0.15, 0.01)`, `vad.py:94-95`) |
| `min_speech_duration_ms` | 0 |
| `max_speech_duration_s` | `inf` |
| `min_silence_duration_ms` | 2000 |
| `speech_pad_ms` | 400 |

`WhisperModel.transcribe` con `vad_filter=True` y `vad_parameters=None` usa `VadOptions()`
(`transcribe.py:885-890`); con un dict, `VadOptions(**dict)`. Es lo que llama el adaptador. Con
K2 (`threshold` 0,25), el `neg_threshold` derivado baja también, a 0,10.

### 0.4 Las activas de v12 a v14

Leídas en sus manifiestos (`knowledge/corpus/transcripciones/`); los huecos, en su campo `huecos`
(`corpus transcript gaps` no existe):

| Vídeo | Activa | Corte (objetivo/min/max s) | Segmentos | Huecos > 30 s (desde-hasta s, duración) |
|---|---|---|---|---|
| v12 | `tr-v12-large-v3-int8-float16-cb502503` | 600/420/780 | 111 | 4: 481,3-610,5 (129,2); 1661,2-1746,1 (85,0); 1748,9-1849,0 (100,2); 1998,2-2131,7 (133,5) = 447,9 s |
| v13 | `tr-v13-large-v3-int8-float16-7f5333a0` (reemplaza a `…1aeb45d5`) | 300/180/420 | 24 | 6: 29,5-296,4; 398,9-644,2; 702,9-895,7; 1182,0-1291,4; 1305,3-1508,2; 1842,7-2115,4 = 1290,1 s |
| v14 | `tr-v14-large-v3-int8-float16-1d289df6` (reemplaza a `…2253ec10`) | 300/180/420 | 47 | 7: 24,1-333,7; 334,8-901,6; 1226,1-1270,6; 1403,7-1977,0; 1985,3-2522,1; 2670,0-2987,2; 3362,5-3398,5 = 2384,2 s |

El minuto de control (v14 600-660 s) cae dentro del hueco 334,8-901,6 s de la activa de v14.

### 0.5 ¿Se puede correr una candidata sin registrarla? No

`transcribir_video` (en `main`) siempre escribe el manifiesto en `knowledge/corpus/transcripciones/`
(`pipeline_transcripcion.py:225-238`). Y antes, `comprobar_activa` (`trabajo.py:81-110`): con
otra huella la carpeta es otra, así que sin `--reemplaza-a` sale con error («ya tiene la
transcripcion activa…»), y con `--reemplaza-a` registra la candidata como la activa nueva. Por eso
D2 añade `--ensayo` (abajo).

### 0.6 Qué citan las activas por su id

`ev-v12-000015-7fc04520` y `ev-v12-000650-370c4bd8` citan `cb502503`, y `ev-v14-004404-ab0281c6`
cita `1d289df6` (Grep en `knowledge/`; ningún ítem cita `7f5333a0`). `verificar_citas`
(`evidence/modelo.py:368-416`): un ítem que cita una transcripción reemplazada da un AVISO agregado
(«N items citan X, reemplazada por Y; M se localizan tambien en la nueva»), no un error, y una
cruda ausente también es un aviso (`:385-387`, `:398-399`). Por esta vía la PARADA (c) no puede
saltar; se comprueba con `knowledge validate` tras cada registro (D4). `knowledge validate` de la
apertura: sin `ERROR`.

### 0.7 La tarde del 10 de julio

Firme: las 3 NO APARECE se quedan (VIDEO-JULIO.md, recuadro; `ev-v20-011213-947092b6` existe en
`knowledge/evidence/v20/`). **Corrección de nombre** (auditor): el encargo dice «la sesión 8»; en el
repo es la **sesión 7b** (`SESION-08-EXTRACCION.md:1`, «Sesión 7b con el trader»; VIDEO-JULIO.md:809),
y el ítem lo creó `ACTIVAR-SESION-08.md`.

### 0.8 El auditor (`auditor-encargo`)

44 afirmaciones: 30 correctas, 1 incorrecta (la «sesión 8», arriba) y 13 con matiz. Lo que cambia
lo que se hace:

1. **D5, «§1.5 para los huecos»**: §1.5 define el hueco como 5 minutos o más y decide CON
   `volumedetect` (`-ss`/`-t`, que la guardia niega) si un hueco es silencio, para decidir si se
   retranscribe. **Cómo se aplica aquí** (desviación declarada, §Desviaciones, 1): esa decisión ya
   la tomó este encargo (retranscribir con otro VAD), así que en D5 los huecos son los del campo
   `huecos` del manifiesto (> 30 s), los mismos de D3, y no se mide volumen. Los de 5 minutos o más
   de §1.5 se dicen aparte en F2.
2. **§6 sustituye la PARADA 4, punto 3** («si alguna operación queda sin comprobar, el bloque NO
   cambia», VIDEO-JULIO.md:1395): el encargo pone la segunda vía con `dias_con_video`. Se aplica
   como **decisión nueva del consultor**, y la PARADA final lo dice. ADR-0092 §11 (`:283`, `:291-292`)
   y `criterio_fidelidad.yaml:58-65` atan el cambio a «si T comprueba julio», con su `fuente`;
   ADR-0092 no está en la lista blanca: la PARADA final dice qué texto quedaría desfasado.
3. **§3.0 frente a §3.2**: manda §3.2 (el stop, «no legible» en todas).
4. **La voz que lee cifras del mes en v13** (PARADA (d)): además de 0:35:43, VIDEO-JULIO.md:296-297
   nombra **v13 0:19:11** (y v11 0:03:06 y 0:09:31). Se respeta igual.
5. Números de línea que se movieron desde VIDEO-JULIO: la frase «hasta que T lo compruebe» está hoy
   en `cableado.py:1467` (no `:1408`); `test_metodo_adr0092.py:445` es hoy `:516`. Y el margen de
   `PROJECT_STATE.md` en la rama es de unos 840 bytes, no 887 (la apertura añade 47).
6. El push a `fix/` y la ejecución de `medir_vad.py` sobre las crudas pueden negarse (clasificador,
   guardia): medido abajo cuando toca.

## D1 y D2 · El código (2026-11-27)

- **`motor_whisper.py`**: `VAD_PARAMETROS` (`:102-109`, los nombres de 0.3; los valores por
  defecto NO se copian al código, abajo, desviación 2); `ConfiguracionVad` (`:113-165`), que valida
  y guarda SOLO los parámetros que se dan, ordenados (uno dado se anota aunque valga lo mismo que el
  de defecto); `describir_vad` (`:168-176`), PURA, sin cargar el
  modelo: por defecto `{"vad_filter": True}`, lo de siempre; sin VAD, `{"vad_filter": False}`; con
  otros valores, además `vad_parameters`; `argumentos_vad` (`:179-186`), los de `transcribe`
  (`vad_parameters=None` por defecto, como antes). `ConfiguracionWhisper.vad` va al final con
  valor por defecto (`:196`). `describir()` y `transcribir()` usan las dos (`:256`, `:271`).
- **`transcripcion.py`**: `MotorFalso(generar, vad=None)` (`:107-119`): sin `vad`, la descripción de
  siempre; con él, la anota (para probar sin GPU).
- **`pipeline_transcripcion.py`**: `transcribir_video(..., ensayo=False)`. En un ensayo, la carpeta es
  `data/transcripciones/<video>/ensayo-<nombre>-<hash_corto(huella+sha256_video)>/` (`:160-162`),
  fuera de la activa y de ninguna registrada; no se mira la regla de actividad; se escriben la cruda,
  la corregida y un `ensayo.json` LOCAL (huella, motor, corte, huecos, segundos del motor) y **ningún
  manifiesto**; `Resultado.registrado` es `False` (`:95`). `--ensayo` con `--reemplaza-a` es un
  error (`:122-126`). Fuera de un ensayo, nada cambia.
- **`cli.py`**: `--sin-vad`, `--vad-threshold`, `--vad-neg-threshold`,
  `--vad-min-speech-duration-ms`, `--vad-max-speech-duration-s`, `--vad-min-silence-duration-ms`,
  `--vad-speech-pad-ms` (los nombres de 0.3) y `--ensayo` (`:3195-3208`); se validan antes de gastar
  GPU (`:280-302`), con `ERROR:` y exit 1.
- **ADR-0007**: la enmienda «2026-11-27 (VAD configurable, R2.5)», antes de `## Fecha / fase`, y
  `## Fecha / fase` al día.
- **`tests/unit/test_transcripcion_vad.py`** (14 funciones, 22 casos): (i) las huellas de los 28
  manifiestos de `main`, calculadas con el código de `main` en un clon desechable
  (`git worktree add --detach C:/cm/main main`, guion `huellas_main.py` en la carpeta de trabajo
  de la sesión, retirado el clon después: `git worktree list` sin él) y fijadas en el test; la
  descripción por defecto puesta en lugar de la registrada da la misma huella; el `falso` describe
  lo de siempre; los nombres de los parámetros contra los campos de `VadOptions` del paquete (donde está); (ii) otra
  configuración cambia la huella, abre otra carpeta y queda anotada; (iii) la CLI rechaza 9 casos
  fuera de rango con `ERROR:` y el nombre del parámetro, sin escribir nada; y D2, el ensayo no
  registra nada. Con el motor `falso`. `PROJECT_STATE.md`: 2248 funciones de test.

### D1 · Los tests rompen a propósito (clon desechable, 2026-11-27)

En `git worktree add --detach C:/cm/rama HEAD` (65659f26), una mutación cada vez con un guion de la
carpeta de trabajo de la sesión (`mutar.py`), `uv run pytest tests/unit/test_transcripcion_vad.py`
y `git checkout -- src` entre una y otra; el clon, retirado después (`git worktree list` sin él):

| Mutación | Qué cambia | Tests que fallan |
|---|---|---|
| M1 | la descripción por defecto gana `vad_parameters: None` | `test_por_defecto_la_descripcion_es_la_de_hoy`, `test_i_la_descripcion_por_defecto_reproduce_la_de_cada_manifiesto_de_main` |
| M2 | `CLAVES_FUERA_DE_HUELLA` deja fuera `vad_filter` y `vad_parameters` | `test_i_las_huellas_de_main_no_cambian`, `test_i_la_descripcion_por_defecto_reproduce…`, `test_ii_otra_configuracion_cambia_la_huella_y_queda_anotada` |
| M3 | los parámetros dados no se anotan | `test_un_parametro_no_dado_no_se_anota_y_uno_dado_si`, `test_otros_valores_quedan_anotados_y_ordenados`, `test_ii_…`, `test_iii_la_cli_anota_la_configuracion_en_un_ensayo` |
| M4 | sin la comprobación de rango de `threshold` y `neg_threshold` | `test_fuera_de_rango_es_un_error_de_dominio` ×3, `test_iii_la_cli_rechaza_lo_fuera_de_rango` |
| M5 | el ensayo sigue y escribe el manifiesto | `test_d2_el_ensayo_no_registra_nada`, `test_iii_la_cli_anota_la_configuracion_en_un_ensayo` |
| control | sin mutación | 21 pasan, 1 se salta (el clon no tiene el grupo `asr`: `faster_whisper` no está, como en la CI) |

## D3 · El criterio, copiado del encargo ANTES de correr ninguna candidata

Copiado tal cual (encargo, §5, D3):

> - D3. **El criterio para elegir la configuración**, escrito ANTES de correr ninguna candidata. Cópialo tal cual al informe antes de la primera corrida.
>   - Se mide sobre v14 entero, con los parámetros de corte de su activa: solo cambia el VAD.
>   - Candidatas: K0, la activa (la referencia); K1, sin VAD; K2, con VAD pero con el umbral de habla a la mitad del de defecto, el relleno de habla (speech pad) al doble y lo demás por defecto.
>   - **Palabra útil:** una palabra con tiempo, de un segmento que cumple dos condiciones: no lleva ninguna de las señales `repeticion`, `compresion` ni `no_habla` (`transcripcion.py`, `SENALES`; `baja_prob` no excluye), y su texto normalizado no se repite idéntico en 3 o más segmentos de la misma cruda. La segunda condición está porque lo que un VAD apagado inventa en música o ruido suele ser una frase que vuelve. Los segundos se miden con los tiempos de las palabras, no con la duración del segmento. Los segmentos ocultos no cuentan para ninguna candidata.
>   - Para cada candidata:
>     - (i) **control positivo:** en v14 0:10:00-0:11:00 hay palabras útiles que, normalizadas (minúsculas, sin acentos, con el glosario aplicado), incluyen «bias» y «bajista», que es lo que Aleks oyó, no lo que dice un ASR;
>     - (ii) **control de lo inventado:** en ese mismo minuto, en el que según Aleks no hay más voz, las palabras útiles que no son «bias» ni «bajista» son como mucho 4;
>     - (iii) **lo que gana:** los segundos de palabras útiles dentro de los huecos de más de 30 s de K0;
>     - (iv) **lo que pierde:** los segundos de palabras útiles de K0 que la candidata no cubre con palabras útiles, como fracción de los de K0;
>     - (v) **sospecha de invención:** la fracción de segmentos de la candidata que quedan fuera de «útil» solo por la regla de las 3 repeticiones.
>   - **Gana** la que cumple (i), (ii), (iv) ≤ 0,10 y (v) ≤ 0,05 con más (iii). Si las dos cumplen y la que gana menos se queda a menos del 10 % de la otra en (iii), gana la de menor (iv). Si ninguna cumple, PARADA (b).
>   - El informe dice si hay palabra útil y si casa con lo que oyó Aleks, nunca otras palabras del ASR como hecho.

**Cómo lo concreta el guion** (`anexos/VAD-JULIO/medir_vad.py`, escrito antes de la primera
corrida; las concreciones, declaradas):

- K1 = `--sin-vad`; K2 = `--vad-threshold 0.25 --vad-speech-pad-ms 800` (la mitad de 0,5 y el
  doble de 400, 0.3), con `--objetivo-s 300 --min-s 180 --max-s 420`, el corte de la activa.
- **Normalizar** = minúsculas (`casefold`), sin acentos (NFD sin marcas), los signos de puntuación
  como espacio, espacios colapsados. La regla de las 3 repeticiones compara el texto así
  normalizado de los segmentos VISIBLES (los ocultos no cuentan).
- **(i) y (ii)**: las palabras útiles cuyo inicio cae en [600 000, 660 000) ms, juntadas por
  segmento, con el glosario (`knowledge/corpus/glosario_asr.yaml`) aplicado con `glosario.aplicar`
  y luego normalizadas; (i) pide los dos tokens «bias» y «bajista»; (ii) cuenta los tokens que no
  son ninguno de los dos.
- **Segundos**: la UNIÓN de los intervalos [t0, t1] de las palabras útiles (dos palabras que se
  pisan no cuentan dos veces). (iii) = la unión de la candidata ∩ los huecos de K0 (campo `huecos`
  del manifiesto activo); (iv) = |útiles de K0 − útiles de la candidata| / |útiles de K0|;
  (v) = segmentos visibles sin señal que excluya pero con texto repetido 3 o más veces / segmentos
  visibles.
- El guion dice, por candidata, segmentos visibles, ocultos, útiles, (i)-(v), lo de (iii) por
  hueco de K0 y los tiempos (sin texto) de los segmentos útiles que caen en esos huecos; del ASR
  solo imprime los tokens del minuto de control.

## Desviaciones

1. **Los huecos de D5 son los del manifiesto (> 30 s), no los de §1.5** (fase 0.8, punto 1). §1.5
   decidía con `volumedetect` sobre un tramo (`-ss`/`-t`, que la guardia niega) si un hueco de 5
   minutos o más era silencio, para decidir si se retranscribía; esa decisión la toma ya este
   encargo. En D5 los huecos son los del campo `huecos` de cada manifiesto, los mismos que D3, y no
   se mide volumen.
2. **Los valores por defecto del VAD no están en el código.** La primera versión de D1 los fijaba en
   `VAD_POR_DEFECTO` (para no anotar un parámetro dado con su valor por defecto) y el primer
   `make check` del commit del código salió con exit 2 y un `failed`:
   `tests/contract/test_no_business_literals.py::test_no_business_literals_outside_registry`,
   «`motor_whisper.py:102 literal 0.5 (stop reducido / riesgo en fondeo)`» y «`:106 literal 2000
   (limite de mensajes de la prop firm)`». No son cifras de negocio, pero coinciden con dos de la
   lista, y una guardia no se rodea (escribirlos de otra forma sería rodearla). Se cambió el diseño:
   el código guarda solo los NOMBRES (`VAD_PARAMETROS`); un parámetro que no se da no se anota y lo
   pone el paquete (`vad_parameters=None` → `VadOptions()`), así que la huella por defecto sigue
   siendo la de siempre; uno que se da se anota siempre, aunque coincida con el de defecto (cambia la
   huella, no el resultado). El test compara los nombres con los campos de `VadOptions`. Los valores,
   en 0.3 de este informe y en la enmienda de ADR-0007. Coste: un `make check` más.

## D3 · Las corridas sobre v14 (2026-11-27, después del commit del código y de copiar el criterio)

`uv run botsito corpus transcribe --video v14 --ensayo <VAD> --objetivo-s 300 --min-s 180 --max-s 420`,
una tras otra, sin `make check` a la vez; ninguna registra nada (`corpus transcript check`: «OK: 28
transcripciones coherentes con el disco y el glosario»; `knowledge/corpus/transcripciones/` sigue
con 28 manifiestos):

| Candidata | VAD | Ensayo (`data/transcripciones/v14/…`) | `transcripcion_id` del ensayo | Segmentos | GPU (s, `segundos_motor` de `ensayo.json`) |
|---|---|---|---|---|---|
| K0 | el de defecto (la activa) | `large-v3-int8-float16-d3b9ac2d` (registrada) | `tr-v14-large-v3-int8-float16-1d289df6` | 47 | — (no se volvió a correr) |
| K1 | `--sin-vad` | `ensayo-large-v3-int8-float16-3e8940a1` | `tr-v14-large-v3-int8-float16-3d963731` | 415 | 484,1 |
| K2 | `--vad-threshold 0.25 --vad-speech-pad-ms 800` | `ensayo-large-v3-int8-float16-cf5be424` | `tr-v14-large-v3-int8-float16-67e2da0d` | 50 | 101,5 |

La medida, con el guion escrito antes de correr (`uv run python docs/validation/anexos/VAD-JULIO/medir_vad.py
--repo . --datos data --video v14 --salida docs/validation/anexos/VAD-JULIO/medida-v14.txt
--candidata K1=… --candidata K2=…`; salida entera en `anexos/VAD-JULIO/medida-v14.txt`). Ningún
segmento oculto en ninguna de las tres (v14 no tiene tramos no citables y julio es libre):

| Candidata | Segmentos visibles / ocultos | Útiles | Palabras útiles (s) | (i) «bias» y «bajista» | (ii) otras palabras (≤ 4) | (iii) gana en los huecos de K0 (s) | (iv) pierde (≤ 0,10) | (v) sospecha (≤ 0,05) | Cumple |
|---|---|---|---|---|---|---|---|---|---|
| K0 | 47 / 0 | 36 | 152,6 | no | 0 | 0,0 | 0,000 | 0,000 | referencia |
| K1 | 415 / 0 | 361 | 1109,0 | **no** | **10** | 607,2 | **0,250** | **0,053** | **no** |
| K2 | 50 / 0 | 46 | 279,0 | **no** | 3 | 31,3 | **0,130** | 0,000 | **no** |

- **El minuto de control (v14 0:10:00-0:11:00).** K0 no tiene ninguna palabra útil en él (es el
  hueco). **K1 y K2 tienen palabras útiles en ese minuto, y entre ellas está «bajista», que casa con
  lo que oyó Aleks; «bias» no está en ninguna de las dos**, ni tras el glosario. Así que (i) no se
  cumple en ninguna. Lo que el ASR escribe en ese minuto, en el anexo, como salida del ASR y no como
  hecho. K1 tiene además 10 palabras útiles que no son «bias» ni «bajista» en un minuto en el que,
  según Aleks, el trader no dice nada más: (ii) tampoco se cumple; K2 tiene 3.
- **(iii) por hueco de K0** (anexo): K1 gana en los siete (100,5, 103,0, 10,6, 172,0, 119,0, 91,6 y
  10,5 s); K2, poco en cada uno (0,7, 9,2, 4,7, 4,1, 6,8, 3,5 y 2,5 s), con segmentos útiles muy
  largos y pocas palabras (900,7-1064,8 s, 1563,3-1710,3 s, 2516,7-2636,5 s).
- **(iv)**: K1 deja sin cubrir con palabras útiles el 25,0 % de lo que K0 cubre; K2, el 13,0 %.
- **(v)**: K1, 22 de 415 segmentos visibles fuera de «útil» solo por repetirse 3 o más veces
  (0,053); K2, ninguno.
- **Un control, que no es candidata ni cambia el criterio** (`anexos/VAD-JULIO/control-v14-vieja.txt`):
  la versión reemplazada de v14 (`tr-v14-…-2253ec10`, el MISMO VAD por defecto, con el corte de
  600/420/780) frente a K0 da (iv) = **0,142**. Dos transcripciones del mismo vídeo con el VAD de
  siempre ya se quedan por encima de 0,10 solo por cambiar el corte. No es un suelo de ruido de las
  candidatas (ellas tienen el corte de K0), pero dice que el umbral de (iv) es estrecho para esta
  medida, que compara palabras por sus tiempos.

**Resultado: ninguna candidata cumple el criterio de D3. Es la PARADA (b)**: no se retranscribe v12
ni v13 (encargo, §4 b), y tampoco v14, porque D4 la registra «con la ganadora» y no la hay. Por eso
D4 y D5 no se hacen: no hay transcripción nueva con la que volver a medir F2, F3, F4 ni F6, ni
propuesta de F5 (PARADA final) con datos nuevos. Las tres crudas de ensayo se quedan en `data/` (no
viajan en git) para lo que se decida.

## PARADA (b) · Lo que necesito que decidas (2026-11-27)

Ninguna candidata cumple D3: K1 falla (i), (ii), (iv) y (v); K2 falla (i) y (iv). Hecho y
commiteado lo que no depende de esto: D1 y D2 (el VAD configurable y el ensayo, con sus tests y la
enmienda de ADR-0007), la medida y este informe. Ningún manifiesto nuevo, ninguna activa cambiada, y
F5 sigue como está (`material_sin_video` sin tocar; julio provisional).

1. **Qué hacer con R2.5.** Opciones:
   - (a) **Otra tanda de candidatas con el MISMO criterio**, escrita por el consultor antes de
     correrla (por ejemplo, entre K0 y K2: `threshold` 0,35 con `speech_pad_ms` 800; o solo
     `speech_pad_ms` 800; o `min_silence_duration_ms` menor). Cada corrida de v14 cuesta de 2 a 8
     minutos de GPU (K2 101,5 s, K1 484,1 s) y la medida es el mismo guion. Con (i) tal como está,
     ninguna pasa si el ASR no escribe «bias» (punto 2).
   - (b) **Revisar el criterio** antes de otra tanda: (i) exige el token «bias», y en las dos
     candidatas sale «bajista» pero no «bias»; y (iv) ≤ 0,10 queda por debajo de lo que separa dos
     transcripciones con el VAD de siempre y otro corte (0,142, control de D3). Cambiar un umbral
     después de medir es decisión del consultor, no de la sesión, y lo dejo aquí sin proponer cifra.
   - (c) **Cerrar R2.5 sin retranscribir**: el VAD queda configurable para quien lo necesite (la
     sesión 9 o un vídeo nuevo), v12 a v14 siguen con sus activas, F5 sigue como lo dejó VIDEO-JULIO
     (julio provisional, la tercera salida de la PARADA 4) y el informe lo dice.
   Recomiendo **(b) y luego (a)**: el criterio pide a la vez que la candidata recupere la voz corta y
   que no pierda casi nada de K0, y la medida no separa bien «perder voz» de «alinear distinto».
   Una salida sería medir (iv) por segmentos que se pisan y no por milisegundos de palabra. Pero
   la decide el consultor, antes de correr nada.
2. **El glosario y «bias».** Si el consultor quiere que (i) acepte lo que el ASR escribe donde Aleks
   oyó «bias», hace falta una sustitución del glosario con su ejemplo verificado (ADR-0007 §5), y
   `knowledge/corpus/glosario_asr.yaml` está protegido en esta rama. Sería otra rama, o ampliar el
   contrato. No lo propongo como hecho: lo que el ASR escribe ahí es salida del ASR.
3. **Lo que espera a esta decisión:** D4, D5, la PARADA final (F5) y las líneas del cierre de R2.5.
   Lo que no espera, y sigue en esta rama: la CI de Linux (toca `src/`) y el revisor.

## Los `make check` y la CI

- Apertura (668c7be6): exit 0, `3816 passed, 6 xfailed`, `CONTRATO:` y `G2:` en verde, `SELLO`.
- Código, primer intento: exit 2, `1 failed` (`test_no_business_literals`, desviación 2); no se
  commiteó.
- Código (65659f26): exit 0, `3838 passed, 6 xfailed`, `CONTRATO:` (13 ficheros) y `G2:`, `SELLO`.
- Este informe y los anexos: abajo, con su commit.
- CI de Linux (`fix/vad-julio`): abajo.

## Estado

EN CURSO, en la **PARADA (b)**: ninguna candidata cumple D3. D4, D5 y la PARADA final esperan la
decisión del consultor; la rama NO está lista para revisión.
