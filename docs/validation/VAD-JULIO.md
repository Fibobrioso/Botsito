# VAD-JULIO · La voz que el VAD del ASR se salta en v12 a v14 (R2.5, letra C)

> PLANTILLA: informe de la rama `trabajo/vad-julio`. Estado: lista para revisión, NO cerrada (ninguna
> candidata cumplió D3; el consultor cierra R2.5 sin retranscribir y F5 no cambia, respuesta a la
> PARADA (b)). La fase 0, el código, el criterio de D3
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
   `PROJECT_STATE.md` en la rama era de unos 840 bytes, no 887 (la apertura añade 47); lo que
   queda al final, en las líneas del cierre.
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
- **`tests/unit/test_transcripcion_vad.py`** (15 funciones, 25 casos; la 15.ª, tras el revisor, b4): (i) las huellas de los 28
  manifiestos de `main`, calculadas con el código de `main` en un clon desechable
  (`git worktree add --detach C:/cm/main main`, guion `huellas_main.py` en la carpeta de trabajo
  de la sesión, retirado el clon después: `git worktree list` sin él) y fijadas en el test; la
  descripción por defecto puesta en lugar de la registrada da la misma huella; el `falso` describe
  lo de siempre; los nombres de los parámetros contra los campos de `VadOptions` del paquete (donde está); (ii) otra
  configuración cambia la huella, abre otra carpeta y queda anotada; (iii) la CLI rechaza 9 casos
  fuera de rango con `ERROR:` y el nombre del parámetro, sin escribir nada; y D2, el ensayo no
  registra nada. Con el motor `falso`. `PROJECT_STATE.md`: 2249 funciones de test (2248 en el commit del código).

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
| M6 (tras el revisor, b4; otro clon de bb5a0bf9 con el test nuevo) | `MotorWhisper.describir()` y `transcribir()` vuelven al `vad_filter=True` fijo de `main` | `test_motor_whisper_describe_y_transcribe_con_su_vad` con `--sin-vad` y con parámetros (el caso por defecto pasa, como debe) |
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
   lista. **Corrección tras el revisor (a1):** el test tiene una exención oficial, el comentario
   `# no-negocio: <motivo>` (`tests/contract/test_no_business_literals.py:112`), que el propio
   paquete `corpus` usa para 0.5 y 2000 (`audio.py:30`, `fotogramas.py:64`); la primera versión de
   este punto decía que escribirlos de otra forma «sería rodearla», y no nombraba la exención, que
   no vi. Se cambió el diseño:
   el código guarda solo los NOMBRES (`VAD_PARAMETROS`); un parámetro que no se da no se anota y lo
   pone el paquete (`vad_parameters=None` → `VadOptions()`), así que la huella por defecto sigue
   siendo la de siempre; uno que se da se anota siempre, aunque coincida con el de defecto (cambia la
   huella, no el resultado). El test compara los nombres con los campos de `VadOptions`. Los valores,
   en 0.3 de este informe y en la enmienda de ADR-0007. Coste: un `make check` más. **Lo que se
   compara (para el consultor):** con la exención, el código copiaría los valores por defecto de
   faster-whisper 1.2.1 y un valor dado igual al de defecto no cambiaría la huella; sin ella (lo
   hecho), el código no depende de los valores de una versión del paquete, y dar a mano un valor de
   defecto (p. ej. `--vad-speech-pad-ms 400`) cambia la huella y abre otra carpeta con el mismo
   resultado. Se queda lo hecho salvo que el consultor prefiera la exención.

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
  largos (900,7-1064,8 s, 1563,3-1710,3 s, 2516,7-2636,5 s) cuyas palabras útiles suman pocos
  segundos dentro de los huecos (el anexo da tramos y segundos, no el número de palabras).
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
   la decide el consultor, antes de correr nada. Un dato más para esa decisión (revisor, «lo que no pudo comprobar»):
   K1 y K2 tienen en el minuto de control palabras útiles que no son «bias» ni «bajista», y Aleks
   dijo que ahí no hay más voz; el minuto del reproductor y el eje de la cruda salen del mismo
   fichero, pero que coincidan al segundo no está medido.
2. **El glosario y «bias».** Si el consultor ve en el anexo (las palabras útiles del minuto de
   control, salida del ASR) una palabra que corresponda a la «bias» que oyó Aleks, y quiere que (i)
   la acepte, hace falta una sustitución del glosario con su ejemplo verificado (ADR-0007 §5), y
   `knowledge/corpus/glosario_asr.yaml` está protegido en esta rama. Sería otra rama, o ampliar el
   contrato. No lo propongo como hecho: lo que el ASR escribe ahí es salida del ASR.
3. **Lo que espera a esta decisión:** D4, D5, la PARADA final (F5) y las líneas del cierre de R2.5.
   Lo que no espera, y sigue en esta rama: la CI de Linux (toca `src/`) y el revisor.

## Respuesta del consultor a la PARADA (b) (2026-11-27)

Copiada tal cual (vale también como respuesta a la PARADA final):

> Modelo: Opus 5.5 · Esfuerzo: alto
>
> RESPUESTA DEL CONSULTOR A LA PARADA (b) de `trabajo/vad-julio` (2026-11-27). Vale también como respuesta a la PARADA final. Cópiala tal cual al informe, en una sección «Respuesta del consultor a la PARADA (b)», y aplícala punto por punto. Leída sobre `f84f4fc` en `fix/vad-julio`.
>
> 1. **R2.5: salida (c). Se cierra sin retranscribir, y el criterio de D3 no se toca.**
>    - D3 se escribió antes de medir y no se relaja después para que pase una candidata. No va ni (b) ni otra tanda (a).
>    - Es una decisión de coste y beneficio, no algo medido. En v14:
>      - K1 (sin VAD) gana 607 s en los huecos, pero escribe 10 palabras en un minuto en el que Aleks no oyó más voz. Queda la salvedad que el revisor dejó abierta: no está medido que el minuto del reproductor y el eje de la cruda coincidan al segundo.
>      - K2 gana solo 31 s.
>    - La pregunta que importaba para F3 era si un VAD distinto recupera las operaciones pendientes de v12 y v13, y eso no se midió: D3 corrió solo sobre v14, que no tiene ninguna operación de F3. Además, 16 de las 24 pendientes son «sin ver» por motivos que no son del ASR (capturas sin eje o sin marcas).
>    - Seguir midiendo cuesta ramas y GPU para un resultado que, como mucho, toca un diagnóstico que ningún umbral lee. Por eso se para aquí.
>    - Queda hecho el VAD configurable y el ensayo (D1 y D2), útil para vídeos y sesiones nuevas. v12 a v14 siguen con sus activas. Las crudas de ensayo se quedan en `data/transcripciones/v14/` (fuera de git), sin borrar.
>
> 2. **F5: NO cambia. Julio sigue provisional** (la tercera salida de la respuesta a la PARADA 4 de VIDEO-JULIO).
>    - Siguen en pie dos respuestas anteriores del consultor:
>      - la de la PARADA 4, punto 3: «si alguna no está comprobada, el bloque no cambia»;
>      - la de la PARADA final, punto 1: no marcar «sin vídeo» ocho días que F2 midió como grabados, salvo la tarde del 10.
>    - El §6 del encargo las sustituía «tras D5», y D5 no se hizo.
>    - Comprobar las 24 operaciones pendientes ya no es trabajo del ASR: pasa al ADR de la salida C como parte del sesgo del material sin vídeo (S-14, R4.7).
>    - No se toca `criterio_fidelidad.yaml`, `cableado.py`, `criterio_fidelidad.py`, los goldens, `fuentes.yaml` ni ningún test de F5. No hay commit de F5.
>    - Lo que sigue diciendo «hasta que T lo compruebe» (T ya no es una letra viva) queda como una línea de Technical Debt propuesta para el cierre: «el texto de julio provisional cita a T, que ya no existe; se reescribe cuando el ADR de C decida S-14».
>
> 3. **Lecciones del consultor.** El cierre las apunta en ERRORES-RECURRENTES como «Error del consultor, apuntado también», como en las filas de renovar-cierres y de reabrir-y-fuente-documental, y no en la columna que mide al revisor.
>    - (a) Fijé el umbral de (iv) en 0,10 sin medir antes el ruido de la propia medida: dos transcripciones con el mismo VAD y otro corte ya dan 0,142. Lección: antes de fijar un umbral sobre una diferencia entre dos salidas, medir con un control cuánto da sin cambio real.
>    - (b) El control positivo (i) exigía un token exacto sin saber cómo escribe ese término el ASR.
>    - (c) D3 midió en v14, donde estaba el minuto de control, pero las operaciones que había que recuperar estaban en v12 y v13. Lección: la candidata se mide donde vive lo que se quiere mejorar, y el control se busca allí.
>    - (d) En el primer borrador de esta respuesta, el consultor dio por medido que «el VAD no las recupera» y cambiaba F5. Lo cazó su auditor antes de entregarla.
>
> 4. **Desviación 2: ACEPTADA.** Los valores por defecto del VAD se quedan fuera del código y solo se guardan los nombres. Así el código no copia valores de una versión del paquete, y esa versión ya está en la huella. Que un valor dado a mano igual al de defecto abra otra carpeta con el mismo resultado es un coste aceptable, y la enmienda de ADR-0007 lo dice. No se usa la exención `# no-negocio:`.
>
> 5. **Desviación 1: ACEPTADA.** Los huecos se toman del manifiesto y no de §1.5. En la práctica ya no aplica, porque D5 no se hace.
>
> 6. **La enmienda de ADR-0007** gana, en un commit propio, un párrafo final: el resultado de D3 (ninguna candidata cumplió; v12 a v14 siguen con sus activas), que solo se midió en v14, y la remisión a `VAD-JULIO.md`.
>
> 7. **Después:**
>    - `make check` sellado en cada commit.
>    - Push a `fix/vad-julio` y el número de run (solo con el fallo aceptado de `state check`).
>    - Una pasada corta del revisor sobre los commits nuevos, con su informe pegado y sus hallazgos resueltos.
>    - En el informe, las líneas propuestas para el cierre, comprobadas contra `test_hoja_de_ruta`:
>      - Hoja de ruta: R2.5 HECHA, con una nota de que se cierra sin cumplir su «Hecho cuando» original, por la decisión del punto 1 y con este informe. R2.4 (:142, «julio sigue provisional») no cambia. En R4.7 (:439, S-14), que la parte de julio no la resuelve el ASR y la decide el ADR de C.
>      - `PROJECT_STATE.md`: la letra C sale, con su texto literal a HISTORIA bajo «# Next Action HECHA · C ·» (no hay ningún registro previo de C), más la línea de Technical Debt del punto 2. Mide el margen: hoy, en la rama, quedan unos 783 bytes.
>      - ERRORES-RECURRENTES: la fila de la rama, con el revisor y las cuatro lecciones del punto 3.
>    - Termina con «Rama lista para revisión, NO cerrada.»

### Cómo se aplica

- **Punto 1:** R2.5 se cierra sin retranscribir y sin tocar el criterio de D3. No va otra tanda. D1 y
  D2 quedan hechos; v12, v13 y v14 siguen con sus activas (`corpus transcript check`: 28
  transcripciones, ninguna nueva). Las tres carpetas de ensayo de v14 siguen en
  `data/transcripciones/v14/`, sin borrar.
- **Punto 2:** F5 no cambia. No hay commit de F5 y no se toca ninguno de sus ficheros de la lista
  blanca (`git diff main --stat -- knowledge/cases/ src/botsito/engine/ src/botsito/cases/ tests/golden/ knowledge/corpus/fuentes.yaml`:
  vacío). La línea de Technical Debt, en las líneas del cierre; dice «el ADR de la salida C de
  ADR-0098» en vez de «el ADR de C», para que no se lea como la letra C que sale.
- **Puntos 3 a 5:** las cuatro lecciones van a la fila de ERRORES-RECURRENTES propuesta (abajo), en la
  columna del consultor. Las desviaciones 1 y 2, aceptadas; la 2 deja el diseño como está.
- **Punto 6:** el párrafo final de la enmienda de ADR-0007 («Resultado (D3 de `trabajo/vad-julio`)»),
  en su commit propio, con su `make check` sellado.
- **Punto 7:** las líneas del cierre, simuladas en memoria contra `test_hoja_de_ruta`, abajo; la
  pasada corta del revisor y la CI, al final.

## Para la orden de cierre (cada línea, comprobada contra `test_hoja_de_ruta`)

Simulado en memoria, sin escribir nada, con
`uv run python docs/validation/anexos/VAD-JULIO/simular_cierre.py .` (salida en
`anexos/VAD-JULIO/simular-cierre.txt`): `a: []`, `b: []`, `c: []`; letras vivas tras el cierre
**ADFGIJMNQ**; R2.5 HECHA; `PROJECT_STATE.md` pasa de 24.233 (con el `Current Feature` de
la entrega) a **24.190 bytes** (tope 25.000: margen de 810). Control: sin el registro de HISTORIA, `b` da «NA:C esta HECHA y HISTORIA no la registra».

1. **`PROJECT_STATE.md`, Next Action:** sale la línea entera de C (y su línea en blanco). En F,
   «La letra C y R6a, en los huecos.» pasa a «R6a, en los huecos.».
2. **`PROJECT_STATE.md`, Technical Debt** (primera línea de la sección):
   «- El texto de julio provisional cita a T, que ya no existe («hasta que T lo compruebe»:
   `criterio_fidelidad.yaml`, `cableado.py:1467`, `criterio_fidelidad.py:341`, ADR-0092 §11); se
   reescribe cuando el ADR de la salida C de ADR-0098 decida S-14 (VAD-JULIO.md, respuesta del
   consultor a la PARADA (b), punto 2).»
3. **`docs/state/HISTORIA.md`**, al final: `# Next Action HECHA · C · sale de PROJECT_STATE.md en
   trabajo/vad-julio (<fecha del cierre>)`, con «Su texto literal en la Next Action (respuesta del
   consultor a la PARADA (b) de trabajo/vad-julio, punto 7; VAD-JULIO.md):» y la línea de C tal
   cual. No hay ningún registro previo de C en HISTORIA (`grep "Next Action HECHA · C"`: vacío).
4. **`docs/plan/HOJA-DE-RUTA.md`, R2.5:** `- **Refs:** NA:C · ID:ADR-0078 · ID:ADR-0007` y un
   `**Estado:**` nuevo al final de la entrada: «HECHA sin cumplir su «Hecho cuando» original
   (`trabajo/vad-julio`, VAD-JULIO.md): el VAD es configurable por transcripción y hay `--ensayo`
   (ADR-0007, enmienda 2026-11-27), pero ninguna candidata cumplió el criterio escrito antes de medir
   (solo se midió en v14). El consultor la cierra sin retranscribir y sin tocar el criterio (respuesta
   a la PARADA (b), punto 1): v12 a v14 siguen con sus activas y F5 no cambia (julio sigue
   provisional); las 24 operaciones sin comprobar pasan al ADR de la salida C (S-14, R4.7).» El resto
   de la entrada, igual. (La línea «Prioridad baja, en los huecos» sale: una entrada HECHA ya no
   tiene prioridad.)
5. **`docs/plan/HOJA-DE-RUTA.md`, R4.7, «Qué es»:** «revisar el sesgo del material sin vídeo (S-14)»
   pasa a «revisar el sesgo del material sin vídeo (S-14; la parte de julio no la resuelve el ASR,
   VAD-JULIO.md, y la decide este ADR)». **R2.4 no cambia.**
6. **`docs/runbooks/ERRORES-RECURRENTES.md`**, la fila de la rama (cuatro columnas):
   | `trabajo/vad-julio` | Dos pasadas, opus (VAD-JULIO.md, «Informe del revisor» y «Segunda pasada del revisor»). Primera: eje (a) 0 bloquea, 2 importa, 2 menor; eje (b) 0 bloquea, 1 importa, 3 menor. a1 (la desviación 2 no nombraba la exención `# no-negocio:` y decía que usarla «sería rodearla»), a2 (la enmienda de ADR-0007 decía «solo los que cambian» y el código anota todos los dados), b1 (faltaba el encargo punto por punto), b4 (ningún test cubría que `MotorWhisper` use la configuración; test y mutación M6 añadidos); arreglados todos, a3 dejado como errata en el informe. Segunda: <la de la pasada corta> | Error del consultor, apuntado también: (a) el umbral de (iv), 0,10, se fijó sin medir el ruido de la propia medida (dos transcripciones con el mismo VAD y otro corte ya dan 0,142); lección: antes de fijar un umbral sobre una diferencia entre dos salidas, medir con un control cuánto da sin cambio real. (b) El control positivo (i) exigía un token exacto sin saber cómo escribe el ASR ese término. (c) D3 midió en v14, donde estaba el minuto de control, y lo que había que recuperar estaba en v12 y v13; lección: la candidata se mide donde vive lo que se quiere mejorar, y el control se busca allí. (d) El primer borrador de la respuesta a la PARADA (b) daba por medido que «el VAD no las recupera» y cambiaba F5; lo cazó el auditor del consultor antes de entregarla | Nada que el consultor viera y el revisor no. Hallazgo de la sesión: `test_no_business_literals` marca valores técnicos de `src/` que coinciden con cifras de negocio (0,5 y 2000); la exención `# no-negocio:` existe y se mira ANTES de cambiar un diseño |
7. **Tag:** `stable/F39s-vad-julio` (el encargo).

## El encargo, punto por punto (tras el revisor, b1)

| Punto del encargo | Estado | Dónde |
|---|---|---|
| §0 Base comprobada con `abrir-rama` (main, origin, tag F39r, CI 46066643655, sin ramas) | Hecho | «La base, comprobada al abrir» |
| §0 Encargo copiado, `contrato.yaml`, Archivo 87 en HISTORIA, tramo R2, riesgo alto, ningún ADR nuevo | Hecho | 668c7be6 |
| §0 Fila de HOLDOUT antes del primer `make check` | Hecho | 668c7be6; la segunda fila del día, en bb5a0bf9 |
| 0.1 `casos_reservados`: ningún día de julio | Hecho | 0.1 |
| 0.2 Lecturas con fichero:línea | Hecho | 0.2 |
| 0.3 Parámetros del VAD leídos en el `.venv` | Hecho | 0.3 |
| 0.4 Activas, cortes y huecos | Hecho | 0.4 |
| 0.5 ¿Ensayo sin registrar? (no: D2) | Hecho | 0.5 |
| 0.6 Citas por id; aviso, no error | Hecho en parte | 0.6: leído en el código y `knowledge validate` sin `ERROR`; «tras cada registro» no llegó (PARADA (b)) |
| 0.7 La tarde del 10 | Hecho | 0.7 (es la sesión 7b) |
| 0.8 `auditor-encargo` | Hecho | 0.8 |
| D1 Opciones de VAD con los nombres de 0.3; función pura; por defecto, lo de hoy | Hecho | «D1 y D2 · El código» |
| D1 Con otros valores, anotados y en la huella | Hecho de otra forma | desviación 2 (los valores por defecto, fuera del código) |
| D1 Tests (i), (ii), (iii) con el `falso`, que rompen a propósito | Hecho | tabla M1-M6 |
| D1 (i) Huellas calculadas en `main` con `comparar-con-main` | Hecho | clon `C:/cm/main` |
| D1 Enmienda de ADR-0007 y `## Fecha / fase` | Hecho | 65659f26; corregida tras el revisor (a2) |
| D1 La configuración ganadora en la enmienda | No hecho | no hay ganadora (PARADA (b)) |
| D2 `--ensayo` con su test, cruda bajo `data/transcripciones/<video>/`, sin manifiesto | Hecho | `test_d2_*` |
| D2 `medir_vad.py`, raíz y salida por argumento, `cargar_cruda` filtrada, cuenta ocultos | Hecho | anexo |
| D3 Criterio copiado antes de la primera corrida | Hecho | entra en 65659f26 (19:19), antes de K1 |
| D3 K0, K1, K2 sobre v14, corte de la activa; tabla (i)-(v) con GPU | Hecho | «D3 · Las corridas» |
| §4 (b) Parar sin retranscribir v12 ni v13 | Hecho | PARADA (b) |
| D4 v12, v13 y v14 con la ganadora | No hecho | PARADA (b); el consultor cierra sin retranscribir (respuesta, punto 1) |
| D5 F2, F3, F4 y F6 de nuevo | No hecho | PARADA (b); no se hace (respuesta, puntos 1 y 5) |
| D6 Ni casos, ni evidencia, ni F5 | Hecho | `git diff main -- knowledge/` vacío |
| §2 Lo que no cambia | Hecho | solo ficheros de la lista blanca (contrato en verde) |
| §6 PARADA final (F5) | Respondida con la PARADA (b) | F5 no cambia; no hay commit de F5 (respuesta, punto 2) |
| §7 Commits sellados (código; informe) | Hecho | 65659f26, bb5a0bf9 y el de los hallazgos del revisor |
| §7 CI de Linux por `fix/vad-julio` | Hecho | «Los `make check` y la CI» |
| §7 Revisor antes de la PARADA final, con su informe pegado | Hecho (antes de la PARADA (b)) | «Informe del revisor» |
| §7 Líneas del cierre (R2.5, PROJECT_STATE, HISTORIA, ERRORES-RECURRENTES) | Hecho | «Para la orden de cierre», simuladas contra `test_hoja_de_ruta` |
| §7 «Rama lista para revisión, NO cerrada» | Hecho | «Estado», tras la segunda pasada del revisor |

## Informe del revisor (2026-11-27, sobre 668c7be6 y 65659f26 más lo estadiado de bb5a0bf9)

### Lo que se hizo con cada hallazgo

| # | Gravedad | Qué se hizo |
|---|---|---|
| a1 | importa | Corregido: la desviación 2 nombra la exención `# no-negocio:` (`test_no_business_literals.py:112`; `audio.py:30`, `fotogramas.py:64`), dice que no la vi, retira «sería rodearla» y compara las dos opciones para el consultor; el diseño se queda salvo que él prefiera la exención. |
| a2 | importa | Corregido en la enmienda de ADR-0007: «un parametro que se da se anota siempre (aunque valga lo mismo que el de defecto)»; `--sin-vad` anota `vad_filter: false`; con parámetros dados, `vad_parameters` con TODOS los dados. |
| a3 | menor | Errata, no se corrige en el guion: el docstring de `medir_vad.py:3` dice «VAD-JULIO.md §2»; el criterio está en «## D3 · El criterio, copiado del encargo ANTES de correr ninguna candidata». El guion se deja como corrió (es lo medido). |
| a4 | menor | Corregido: el margen de `PROJECT_STATE.md`, en las líneas del cierre con la cifra del final; en la fase 0 queda como lo que era al escribirla. |
| b1 | importa | Hecho: «El encargo, punto por punto», arriba. |
| b2 | menor | Corregido: «pocas palabras» → los segmentos largos «cuyas palabras útiles suman pocos segundos dentro de los huecos». |
| b3 | menor | Corregido: el punto 2 de la PARADA (b) dice «si el consultor ve en el anexo […] una palabra que corresponda a la «bias» que oyó Aleks». |
| b4 | menor | Hecho: `test_motor_whisper_describe_y_transcribe_con_su_vad` (tres casos, sin GPU, con `_cargar` parcheado) y su mutación M6, que lo rompe. 2249 funciones de test. |

Lo que el revisor no pudo comprobar y la sesión sí: la CI de `main` 46066643655 (`gh`, al abrir);
los `segundos_motor` de los `ensayo.json` de K1 y K2 (484,1 y 101,5, leídos con `grep` de esa
clave; el corte, el de las órdenes lanzadas, `--objetivo-s 300 --min-s 180 --max-s 420`); que las corridas fueran después de 65659f26 (K1 se lanzó a las 19:19:45, tras el
commit); y `knowledge validate` antes de cada `make check`, sin `ERROR`. Sus lecturas fuera de la
fila 2 de HOLDOUT (el código de faster-whisper, los manifiestos, `make-check.log` y nombres de
ficheros de `knowledge/evidence/`) son documentos y código: no exponen material.

### El informe, tal cual

## Informe del revisor · trabajo/vad-julio · 2026-11-27

Revisado: los commits 668c7be6 y 65659f26 de main..HEAD, y lo que está estadiado (VAD-JULIO.md, sus dos anexos .txt, la fila nueva de HOLDOUT y PROJECT_STATE). No ejecuté make check ni nada que escriba. Tampoco abrí crudas, fotogramas, `data/` ni nada del punto 3.

### Eje (a) · Reglas de la casa
Resumen: 0 bloquea, 2 importa, 2 menor.

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| a1 | importa | **La razón de la desviación 2 no se sostiene.** El informe dice que escribir los valores por defecto de otra forma «sería rodearla» (a la guardia). Pero `test_no_business_literals` tiene una exención oficial con motivo, y el propio paquete `corpus` la usa justo para 0.5 y 2000. Ese cambio de diseño tiene un coste que el consultor querría ver comparado con la exención: dar a mano un valor de defecto (p. ej. `--vad-speech-pad-ms 400`) cambia la huella y abre otra carpeta aunque el resultado sea el mismo. El informe tiene que nombrar la exención y decir por qué no la usó (puede haber razón, p. ej. no copiar al código unos valores por defecto que dependen de la versión del paquete). | `docs/validation/VAD-JULIO.md:253-254` («una guardia no se rodea (escribirlos de otra forma sería rodearla)»). `tests/contract/test_no_business_literals.py:112` `_EXENCION = re.compile(r"#\s*no-negocio:\s*\S.{4,}")` y `:190-196` (`test_exencion_no_negocio_exige_motivo`). `src/botsito/corpus/audio.py:30` `SILENCIO_MINIMO_S = 0.5  # no-negocio: ...`. `src/botsito/corpus/fotogramas.py:64` `HUECO_FOTOGRAMAS_MS = 2000  # no-negocio: ...` |
| a2 | importa | **La enmienda de ADR-0007 contradice el código y a sí misma.** Dice que el manifiesto anota `vad_parameters` con «solo los que cambian». El código anota todos los que se dan, aunque valgan lo mismo que el de defecto, y la misma enmienda dice dos líneas antes que «un parametro que se da se anota siempre». Además «Con parametros dados, el manifiesto anota `vad_filter: false`» mete `--sin-vad`, que no es un parámetro dado. | `docs/adr/0007-transcripcion-en-dos-capas.md`, enmienda 2026-11-27: «un parametro que se da se anota siempre» y «Con parametros dados, el manifiesto anota `vad_filter: false` o `vad_parameters` (solo los que cambian)». `src/botsito/corpus/motor_whisper.py`, `ConfiguracionVad.desde` (`dados = {k: v ... if v is not None}`, todos a `parametros`). `tests/unit/test_transcripcion_vad.py:105-106` (`speech_pad_ms=400`, el de defecto, sale anotado) |
| a3 | menor | El guion cita una sección que no existe: «VAD-JULIO.md §2». El criterio está en «## D3 · El criterio, copiado del encargo…». | `docs/validation/anexos/VAD-JULIO/medir_vad.py:3`. `grep "^## \|^### "` del informe: no hay §2 |
| a4 | menor | El margen de PROJECT_STATE ya no es «unos 840 bytes»: con lo estadiado son 783. Importa para las líneas del cierre. | `VAD-JULIO.md:150`. `git show :PROJECT_STATE.md \| wc -c` → 24217 (tope 25.000). HEAD 24159, main 24112 |

Comprobado sin hallazgos:
- **Contrato.** `scripts/contrato_rama.py`: «CONTRATO: 15 ficheros dentro del contrato de trabajo/vad-julio (riesgo alto, artefacto docs/validation/VAD-JULIO.md, tramo 'R2', 6 comprobaciones para el revisor)» y «G2: fila de HOLDOUT-EXPOSICIONES del 2026-11-27 para trabajo/vad-julio, estadiada», exit 0.
- **Comprobaciones del contrato.**
  - `pytest tests/unit/test_transcripcion_vad.py`: «22 passed», ninguno saltado (aquí está faster_whisper).
  - `corpus transcript check`: «OK: 28 transcripciones coherentes con el disco y el glosario».
  - `state check`: «OK: rama 'trabajo/vad-julio' …».
  - make check: hay uno en marcha. `make-check.log` está a mitad de pytest («Contracts: 4 kept, 0 broken»), sin SELLO todavía. La evidencia de los dos commits es la del informe (`:343-346`).
- **Trailers `Fuente:`.** Ningún commit toca `knowledge/spec` ni `knowledge/cases` (salida vacía).
- **Holdout.**
  - Nada toca `knowledge/cases/holdout/`.
  - Hay dos filas del 2026-11-27. La primera la añade 668c7be6, el commit de apertura, antes del primer make check. La segunda está estadiada y declara los cuatro ficheros leídos por el guion, ningún fotograma y los clones.
  - Ningún agregado.
- **Regímenes.** `git diff --name-status main...HEAD -- knowledge/ data/manifests/` y la versión `--cached`: vacíos. Siguen 28 manifiestos.
- **Ambigüedades.** No se tocan.
- **ADR-0007.** `## Estado` = `ACTIVE`, y `## Fecha / fase` está al día.
- **Informes cerrados.** HOLDOUT-EXPOSICIONES solo gana filas. VIDEO-JULIO.md no se toca.
- **Guardias de `cita`.** No aplica.
- **Informe.** Existe y acaba en su estado (EN CURSO, PARADA (b)).
- **Ensayos y mutaciones.** Según el informe, en worktrees de `C:/cm/`.
- **Citas comprobadas contra su fuente, todas bien:**
  - main `motor_whisper.py:139,159,174`;
  - main `pipeline_transcripcion.py:225-238,255,258-263,266-282,326-332`;
  - `trabajo.py:51-52`;
  - `scripts/transcribir_sesion.py:563-565` (por posición, cuatro campos);
  - `.venv/.../faster_whisper/vad.py:37-42` (0.5 / None / 0 / inf / 2000 / 400) y `:94-95`;
  - `transcribe.py:885-889` (`None` → `VadOptions()`, dict → `VadOptions(**dict)`) y METADATA 1.2.1;
  - `SESION-08-EXTRACCION.md:1` («Sesión 7b»);
  - los encabezados de VIDEO-JULIO (§0.4 :106, §3.5 :535, §5 :569, §4 :583, §6 :663, §1.5 :1203, §1.6 :1220, §3.2 :1354, PARADA 4 :1379, el minuto de escucha :1412/:1416);
  - los tres ítems que citan cb502503 y 1d289df6 (grep -l, nada cita 7f5333a0);
  - los huecos de v12 y v14 contra sus manifiestos (v12 447,9 s; v14 2384,2 s).
- **Sin ítems de evidencia nuevos.**

### Eje (b) · Encargo
Resumen: 0 bloquea, 1 importa, 3 menor. Requisitos: 27 hechos (1 de ellos de otra forma, declarado), 4 parciales, 5 no hechos (todos por la PARADA (b) o pendientes de su turno).

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 1 | §0 Base comprobada con `abrir-rama` (main, origin, tag, CI, sin ramas) | Hecho | VAD-JULIO.md:13-23 (CI 46066643655 no la comprobé: no ejecuté gh) |
| 2 | Encargo copiado, contrato, Archivo en HISTORIA | Hecho | `docs/encargos/trabajo-vad-julio.md`; `contrato.yaml`; `HISTORIA.md:22271` «# Archivo 87 …», solo líneas añadidas |
| 3 | Lista blanca, rutas protegidas y bloque ids-inexistentes vacío | Hecho | contrato.yaml:5-75; contrato_rama OK |
| 4 | Fila de HOLDOUT antes del primer make check | Hecho | la añade 668c7be6, el commit de apertura |
| 5 | 0.1 `casos_reservados`: ninguno de julio | Hecho | VAD-JULIO.md:22-23, :29-31 (no lo ejecuté) |
| 6 | 0.2 Lecturas con fichero:línea | Hecho | :33-72; citas comprobadas en el eje (a) |
| 7 | 0.3 Parámetros del VAD leídos en el `.venv` | Hecho | :76-89 = `vad.py:37-42` |
| 8 | 0.4 Activas, corte y huecos | Hecho | :96-102 contra los manifiestos |
| 9 | 0.5 ¿Ensayo sin registrar? | Hecho | :104-110 |
| 10 | 0.6 Citas por id, «confírmalo con knowledge validate» | Parcial | :112-120. El aviso se confirma leyendo `evidence/modelo.py` y se deja para «tras cada registro», que no ha llegado (justificado). knowledge validate, solo el de apertura. |
| 11 | 0.7 Tarde del 10 | Hecho | :122-127, con la corrección «sesión 7b» |
| 12 | 0.8 `auditor-encargo` | Hecho | :129-152 |
| 13 | D1 Opciones de CLI (apagar y los 6 parámetros, con sus nombres) | Hecho | `cli.py:3197-3203` |
| 14 | D1 Parte del VAD en una función pura sin cargar el modelo | Hecho | `motor_whisper.py`, `describir_vad`/`argumentos_vad` |
| 15 | D1 Por defecto, descripción y huella idénticas, sin claves nuevas | Hecho | `huella_de` y `CLAVES_FUERA_DE_HUELLA` no cambian (diff); `test_i_*` pasan |
| 16 | D1 Con otros valores se anotan y entran en la huella | Hecho de otra forma | declarado: desviación 2, :248-259 (ver a1) |
| 17 | D1 Tests (i), (ii), (iii) con el motor `falso`, que rompen a propósito | Hecho | test_transcripcion_vad.py; tabla M1-M5, :194-201 |
| 18 | D1 (i) Huellas calculadas en main con `comparar-con-main` | Hecho | :178-182; equivalente por el diff (ni `huella_de` ni los manifiestos cambian) |
| 19 | D1 Enmienda de ADR-0007 y `Fecha / fase` | Hecho | diff del ADR (ver a2) |
| 20 | D1 La configuración ganadora en la enmienda | No hecho | por PARADA (b), justificado |
| 21 | D2 `--ensayo` con su test, cruda bajo `data/transcripciones/<video>/`, sin manifiesto | Hecho | `pipeline_transcripcion.py` (ensayo), `test_d2_*` |
| 22 | D2 `medir_vad.py`: raíz y salida por argumento, `cargar_cruda(filtro_de)`, sin `crudo`, cuenta ocultos | Hecho | medir_vad.py:95-97, :136-141 |
| 23 | D3 Criterio copiado tal cual antes de la primera corrida | Hecho | :207-218 idéntico a encargo :105-116; entra en 65659f26 (19:19) con el guion, que no ha cambiado desde entonces |
| 24 | D3 K0/K1/K2 sobre v14 entero con el corte de la activa | Hecho | :223-224, :263 (lo de `ensayo.json` no lo pude verificar) |
| 25 | D3 Medida (i)-(v) | Hecho | medida-v14.txt:6-8; el guion mide lo que dice el criterio (detalle abajo) |
| 26 | D3 No dar palabras del ASR como hecho | Hecho | :285-290 (matiz en b3) |
| 27 | §4 (b): parar sin retranscribir v12 ni v13 | Hecho | :304-308; 28 manifiestos |
| 28 | D4 v12, v13 y v14 | No hecho | por PARADA (b), justificado |
| 29 | D5 F2, F3, F4 y F6 | No hecho | por PARADA (b), justificado |
| 30 | D6 Ni casos, ni evidencia, ni F5 | Hecho | diff de `knowledge/` vacío |
| 31 | §2 Motor, spec, casos, evidencia, feedback y manifests sin tocar | Hecho | diff --stat: solo los 13 ficheros de la lista blanca |
| 32 | §7 Commit del código y los tests | Hecho | 65659f26 |
| 33 | §7 Commit del informe | Parcial | estadiado, make check en marcha |
| 34 | §7 CI de Linux en `fix/vad-julio` | No hecho | pendiente; no depende de la PARADA (:339) |
| 35 | §7 Contenido del informe (fase 0, criterio, tabla con GPU, desviaciones, make check) | Parcial | hecho lo que no depende de la PARADA; falta la CI y la PARADA final |
| 36 | §7 Revisor pegado al final del informe | Parcial | este informe: lo pega la sesión |

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| b1 | importa | **Falta «El encargo, punto por punto»** (la tabla de `entregar-rama`). El encargo tiene fase 0 y la regla E5 lo pide. Se entiende que llega con la entrega, pero hoy falta. | `grep -n "punto por punto" docs/validation/VAD-JULIO.md`: sin salida |
| b2 | menor | **«pocas palabras» no sale del anexo.** De K2 se dice «segmentos útiles muy largos y pocas palabras», pero el anexo da los tramos y los segundos, no el número de palabras. | VAD-JULIO.md:292-293; medida-v14.txt:16-17 (no hay recuento de palabras) |
| b3 | menor | **La PARADA, punto 2, da por hecha una correspondencia.** «lo que el ASR escribe donde Aleks oyó «bias»» supone que el ASR puso una palabra en el sitio de «bias». Eso es inferirlo de la salida del ASR (el anexo trae `'vaya', 'bajista'`), no medirlo. Va con reserva («No lo propongo como hecho») y no nombra la palabra, pero conviene decir «si el consultor ve en el anexo una palabra del ASR que corresponda a «bias»…». | VAD-JULIO.md:334-337; medida-v14.txt:12, :15 |
| b4 | menor | **La conexión real de MotorWhisper no tiene test.** Nada comprueba que `MotorWhisper.describir()` y `transcribir()` usen la configuración: si se volviera a `"vad_filter": True` fijo o se dejara de pasar `argumentos_vad`, ningún test fallaría (no hay mutación sobre `MotorWhisper`). Se puede probar sin GPU parcheando `_cargar`. Hoy la evidencia de que K1 corrió sin VAD son sus 415 segmentos frente a 47. | `motor_whisper.py` (`**describir_vad(...)`, `**argumentos_vad(...)`); test_transcripcion_vad.py:231-271 (solo `MotorFalso`); tabla M1-M5, :194-200 |

**¿Mide `medir_vad.py` lo que dice el criterio?** Sí, con las concreciones declaradas en :220-239.
- Palabra útil: señal `repeticion`/`compresion`/`no_habla` y repetición en 3 o más segmentos visibles (:98-107).
- (i) y (ii): palabras con t0 en [600000, 660000), con el glosario y normalizadas (:112-121, :187-190).
- (iii): unión de palabras útiles ∩ huecos del manifiesto de K0 (`hueco_transcripcion_s: 30.0`).
- (iv): |K0 − cand| / |K0| (:184).
- (v): solo por repetición / visibles (:106-107, :185).
- Los ocultos fuera, por `cargar_cruda` filtrada.
- Ni la regla de desempate ni la elección de ganadora están programadas. Con ninguna candidata que cumpla, no cambia nada.
- La repetición compara el texto normalizado sin glosario, declarado en :225-227.

**La PARADA (b) está bien fundada:**
- K1 falla (i), (ii) con 10, (iv) con 0,250 y (v) con 0,053.
- K2 falla (i) y (iv) con 0,130 (medida-v14.txt:7-8).
- El control Kvieja: comprobé que su `motor` es idéntico al de K0 y que solo cambia el corte (diff de los dos manifiestos de v14: corte, fragmentos, huecos, segmentos y señales). Así que «solo por cambiar el corte» (:299-300) se sostiene.
- «bias» no está en el glosario (`grep -i bias glosario_asr.yaml`: vacío) y el glosario no cambia desde el 2026-09-06, así que el prompt de K1 y K2 es el de K0.
- La PARADA no retranscribe nada y deja abiertas las opciones.

### Lo que no pude comprobar
- Qué hay en `data/`: los `ensayo.json` de K1 y K2 (corte 300/180/420, que solo cambie el VAD en `motor`, `segundos_motor` 484,1 y 101,5) y sus crudas. No leo `data/`.
- Que las corridas fueran después de 65659f26 (19:19:39). Cuadra con el orden del informe, pero la hora de las corridas vive en `data/`.
- Los make check sellados de 668c7be6 y 65659f26: el log se ha sobrescrito y hay uno en marcha sin SELLO ni PICO DE MEMORIA todavía. Solo tengo el informe, :343-346.
- `knowledge validate`: no está en lo que me autorizaron ejecutar, y el contrato lo pide con log fuera del repo.
- La CI de main 46066643655 y los 34 reservados de `casos_reservados`: no ejecuté gh ni el recuento.
- La tabla de mutaciones M1-M5 y el «21 pasan, 1 se salta» del clon: se hicieron en worktrees ya retirados.
- Que el reloj del minuto de Aleks (0:10:00-0:11:00 del reproductor) y el eje de tiempos de la cruda sean el mismo. K1 y K2 sacan «continuamos» en ese minuto, y Aleks dijo que no hay más voz.
- Mis lecturas fuera de la lista de la fila 2 de HOLDOUT (para que la sesión confirme que la fila las cubre): el código de faster_whisper en el `.venv`, los manifiestos de v12 y v14, `make-check.log`, y nombres de ficheros de `knowledge/evidence/` (con `grep -l`, sin abrir ítems).

### Comandos ejecutados
1. `git branch --show-current && git merge-base main HEAD && git log --format='%h %s' main..HEAD && git diff --stat main...HEAD && git status --short`
2. `uv run python scripts/contrato_rama.py`
3. `uv run pytest tests/unit/test_transcripcion_vad.py -q` (y `-v`: «22 passed in 1.72s»)
4. `uv run botsito corpus transcript check`
5. `uv run botsito state check`
6. `git diff main...HEAD -- src/botsito/corpus/motor_whisper.py src/botsito/corpus/transcripcion.py`
7. `git diff main...HEAD -- src/botsito/corpus/pipeline_transcripcion.py src/botsito/cli.py`
8. `git diff main...HEAD -- docs/adr/0007-... docs/validation/HOLDOUT-EXPOSICIONES.md PROJECT_STATE.md; git diff --cached -- PROJECT_STATE.md docs/validation/HOLDOUT-EXPOSICIONES.md`
9. `ls knowledge/corpus/transcripciones/ | grep -E "tr-v1[234]-"`; `diff` de los dos manifiestos de v14
10. `git show main:src/botsito/corpus/motor_whisper.py` (líneas 136-176); `git show main:.../pipeline_transcripcion.py` (225-238, 253-282, 326-332); `trabajo.py` 48-53 y 81-84; `scripts/transcribir_sesion.py` 559-575
11. Lecturas de `.venv/Lib/site-packages/faster_whisper/vad.py` (14-45, 90-97), de `transcribe.py` (880-895, grep de clases) y de METADATA
12. `grep` en `ficheros_con_ocultos.txt` y en VIDEO-JULIO.md («minuto de escucha», encabezados)
13. `head -1 SESION-08-EXTRACCION.md`; `ls knowledge/evidence/v20 | grep -c ev-v20-011213-947092b6`; `grep -rln` de los tres ids en `knowledge/evidence/`
14. `grep` en `tests/contract/test_no_business_literals.py` y de `# no-negocio:` en `src/botsito/`
15. `grep` de `bias`/`vaya` en `glosario_asr.yaml`; `git log` del glosario y del manifiesto 1d289df6
16. `git show :PROJECT_STATE.md | wc -c` (y de HEAD y main)
17. `ls -la make-check.log; tail -c 1500 make-check.log`
18. `git show --stat 65659f26` y los encabezados del informe en ese commit; `git diff --cached --stat` y las líneas quitadas del informe
19. `git log --format='%h%n%B' main..HEAD -- knowledge/spec knowledge/cases`; `git diff --name-status main...HEAD -- knowledge/ data/manifests/` (y `--cached`); `## Estado` de ADR-0007
20. `git log main..HEAD -- HOLDOUT-EXPOSICIONES.md`; `grep "^# Archivo 87"` en HISTORIA; `grep "punto por punto"` en el informe
21. Read de: el encargo, contrato.yaml, VAD-JULIO.md, medir_vad.py, medida-v14.txt, control-v14-vieja.txt, test_transcripcion_vad.py, cli.py:3192-3209, y Grep del manifiesto de v12
(Dos comandos los negó la guardia y no los reescribí para rodearla: un `for` sobre los manifiestos y un `awk` con varias condiciones. Lo mismo lo saqué con Grep y Read.)

## Los `make check` y la CI

- Apertura (668c7be6): exit 0, `3816 passed, 6 xfailed`, `CONTRATO:` y `G2:` en verde, `SELLO`.
- Código, primer intento: exit 2, `1 failed` (`test_no_business_literals`, desviación 2); no se
  commiteó.
- Código (65659f26): exit 0, `3838 passed, 6 xfailed`, `CONTRATO:` (13 ficheros) y `G2:`, `SELLO`.
- Informe y anexos de D3 (bb5a0bf9): exit 0, `3838 passed, 6 xfailed`, `CONTRATO:` (15 ficheros)
  y `G2:`, `SELLO`.
- Los hallazgos del revisor (este commit): su `make check` y su CI, en el mensaje final de la
  sesión y en la orden de cierre (el informe no puede citar el run de su propio commit).
- **CI de Linux sobre bb5a0bf9** (`git push origin trabajo/vad-julio:refs/heads/fix/vad-julio`):
  run **46091156994**, `failure` solo por lo aceptado (`RITUAL.md`:105-107):
  `FAILED tests/unit/test_cli.py::test_state_check_ok_on_real_repo` («ERROR: PROJECT_STATE declara
  la rama 'trabajo/vad-julio'; la rama actual es 'fix/vad-julio'»); `1 failed, 3740 passed, 103
  skipped`, lint, tipos y contratos en verde («All checks passed!»).

## Estado

PENDIENTE de la segunda pasada del revisor (abajo).
