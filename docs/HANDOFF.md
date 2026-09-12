# HANDOFF · continuar Bot v3 desde otra terminal

Contexto humano que no cabe en `PROJECT_STATE.md`. Lee primero `PROJECT_STATE.md`: si este fichero
lo contradice, manda `PROJECT_STATE.md`. Regla (MASTER_PLAN §F): el HANDOFF se actualiza DENTRO de la
rama de cada funcionalidad, antes del merge; en `main`, tras el tag `stable/*`, solo puede cambiar
`PROJECT_STATE.md` (un `docs(handoff)` en main puso la CI en rojo dos veces, F04 y F05).

## Estado (2026-09-12, fase 1 cerrada en main; F11 validada y cerrada; F12 CERRADA, esperando validacion)
- `main`: merge de F11 `b62f4aa` con tag `stable/F11`; `docs(state)` `3597b3d`. La fase 1 (F03-F08)
  se cerro antes, en `5d8cf3c` con tag `stable/F08`. Protegida en GitHub.
- Cerradas y en main: F01-F09 (salvo las no iniciadas), F15, la auditoria global y los previos
  de F07. Ramas fusionadas borradas.
- F10 elicitation-kit CERRADA el 2026-09-08 (tag `stable/F10`). Lo que dejo: ADR-0011;
  `knowledge/spec/ambiguedades.yaml` (A-1..A-12 legibles por maquina); registro con 24
  parametros de estrategia en UNKNOWN; `knowledge/cases/kit/{config,mapa_parametros,vistos}.yaml`
  (cifras de negocio como datos; enero, julio y agosto VISTOS por el trader); paquete `cases`
  (cuestionario de 21 preguntas con casos `ev-*`, ventanas de dias no vistos de mayo y junio de
  2026 con hash y limites H4 por anclaje, particiones por hash con seed, kappa desde los
  `LABEL_CASE`); CLI `kit build|check|kappa`; `knowledge validate` capa kit con guardia de
  ancestro (particiones commiteadas antes del primer `LABEL_CASE`); paquete real
  `knowledge/cases/kit/2026-09-09-sesion-01/` (nacio con la fecha provisional 2026-09-15 y se movio al celebrarse).
- SESION 1 CELEBRADA el 2026-09-09 y procesada entera (video v6, 2 h 27 min; 107 registros de
  feedback; A-1..A-12 RESUELTAS). Informe: `docs/validation/SESION-01-2026-09-09.md`, que es el
  esquema completo de la estrategia con la cita de cada decision. Cerrada en main con el tag
  `stable/F10-sesion-01`.
- CUIDADO al citar v6: dos tramos NO son especificacion y la guardia los rechaza
  (`knowledge/corpus/tramos_no_citables.yaml`): 0:41:00-0:50:11, donde ambos acuerdan en voz que lo
  que se explica "no va para la operativa", y 1:53:30-1:57:31, donde suena un video ajeno mientras
  el trader se ausenta.
- F11 strategy-spec-schema VALIDADA y cerrada en main el 2026-09-10 (tag `stable/F11`). Lo que dejo:
  - `botsito feedback apply --sesion <s> [--check]`: lleva los valores del feedback al registro.
    NO interpreta: si un valor no encaja en el tipo, falla y dice cual. La re-expresion se hace
    fuera, con un registro que supersede y lleva `valor_canonico` (campo opcional nuevo).
  - `botsito spec status`: con que corre el bot y que sigue en revision (cruza el registro con las
    ambiguedades ABIERTAS).
  - `botsito spec manifest [--escribir]`: hash de la spec sobre los TRES ficheros. Si el hash
    cambia y `spec_version` no, `knowledge validate` falla.
  - `knowledge/spec/`: el recuento vivo lo da `botsito spec status` y NO se copia aqui: esa copia
    se quedo vieja tres veces en dos dias (P8 y P11 de la auditoria). Un test lo vigila.
  - ADR-0012 a ADR-0017. La enmienda a ADR-0005 del 2026-09-09 queda REVOCADA por ADR-0017:
    `huso_operativa` vuelve a `Europe/Madrid`, que es lo que ADR-0005 decia. El trader opera
    siempre a SU hora, sea cual sea la fecha, asi que su reloj es civil y no un offset fijo.
    La rejilla H4 se ancla aparte, en `17:00 America/New_York` = 00:00 de servidor.
- F12 spec-semantic-validator CERRADA y esperando validacion (rama `feature/F12-spec-semantic-validator`). Lo
  que ya existe: ADR-0018 (la precedencia va por CLASE), ADR-0019 (la forma ejecutable: predicados
  con argumentos, ligadura, y `predicados`/`acciones`/`hechos`/`acumuladores` DENTRO de
  strategy_spec.yaml) y ADR-0020 (la base del lotaje). Las 24 reglas vigentes tienen forma
  ejecutable; `spec status` dice cuantas siguen en prosa (hoy, ninguna). CERRADA y a la espera de
  validacion desde el 2026-09-12: los parametros sin lector declaran `consumido_por`, existe
  `botsito spec check`, los `R-NN` son explicitos, la auditoria de cierre (dos agentes) esta
  aplicada y el informe es `docs/validation/F12-spec-semantic-validator.md`.
- EL LOTAJE CAMBIO DE BASE el 2026-09-11 (ADR-0020) y es lo mas caro de este tramo: el 0,5 % de
  riesgo se mide EN el nivel 0,8 y no sobre la caja completa, asi que `lotaje_base` vale
  `hasta_stop_fraccion`, el lote es un 25 % mayor y el stop cuesta el riesgo entero. RN-012 dice
  ahora lo contrario de lo que decia. Si alguien lee material anterior al 2026-09-11 -incluidos
  los mensajes del trader sobre la rentabilidad de mayo- lo encontrara contado en CAJAS
  COMPLETAS, que es la convencion vieja: esta anotado en ADR-0020, con la pregunta pendiente de
  ratificar con el trader.
- BACKTEST DE MAYO 2026 recibido el 2026-09-11 (junio NO). Esta en el corpus, fuera de git, en
  `Material adicional de su operativa/Backtest mayo 2026/`. OJO: 13 de los 19 dias de mayo son
  holdout-1/2/3 segun `knowledge/cases/kit/2026-09-09-sesion-01/particiones.yaml`, asi que no
  puede usarse para elegir parametros; es entrada de F14 y F26.
- Lecciones tecnicas (F12), y la mas cara es la primera:
  - UNA GUARDIA NUEVA NO HEREDA NADA. El vocabulario de ADR-0019 (predicados, acciones, efectos,
    hechos, acumuladores) lleva `cita` y `literal` propios desde el dia uno, y durante toda la
    funcionalidad NADIE los comprobaba: se podia poner cualquier frase en boca del trader dentro
    de un predicado, o citar un `fb-...-deadbeef`. El comentario que habia en `comprobar_literales`
    lo predijo con esas palabras y aun asi paso. Al anadir un sitio con cita, amplia TODAS las
    guardias en el mismo commit: `comprobar_contra`, `comprobar_literales` y
    `comprobar_citas_revocadas`.
  - Casar por SUBCADENA en un JSON serializado es una trampa que bendice mentiras: `hechos.sesgo`
    declaraba que RN-003 lo consume -lo produce- y colaba porque su `cuando` contiene
    `sesgo_h4_criterio_ruptura`. Peor: corregir la declaracion hacia FALLAR la guardia. Se casa el
    token exacto, o se recorre el arbol.
  - Un hecho que se fija y nadie declara es invisible: `liquidez_tomada` (RN-004) y `estructura_m1`
    (RN-007) se fijaban sin estar en `hechos:`, asi que la guardia -que iteraba los declarados- no
    los veia. El primero es la precondicion de los dos esquemas de entrada: un motor que leyera
    `forma` habria entrado sin esperar a que se tomara la liquidez de M15.
  - `permite`/`prohibe` llevan LISTA, no mapa, asi que el recorrido de invocaciones los saltaba y
    sus objetivos no se comprobaban contra nada en once de las veinticuatro reglas vigentes.
  - Las cifras de un informe se verifican con la calculadora antes de escribirlas: 21, 27,6 y 28,2
    salen de 18x3-33x1, 18x3-33x0,8 y 18x3,4-33x1, y eso es lo que dice en que convencion cuenta
    el trader.
  - Cambiar un valor de negocio no es cambiar un valor: al superseder el registro del lotaje,
    dos citas quedaron apuntando a un registro revocado (RN-027 y el predicado
    `no_es_multiplo_de`) y dos textos quedaron afirmando algo falso (la nota de RN-015 y la
    descripcion de `base_calculo_objetivo` decian que el objetivo y el lote comparten distancia).
    Lo destaparon las guardias, no la lectura.
  - La guardia de citas revocadas ha nacido corta CUATRO veces: parametros (P13), luego reglas y
    glosario (RN-013), luego los predicados y acciones de F12, y en la auditoria de cierre se vio
    que seguian fuera los ACUMULADORES, que tambien llevan cita. Al anadir un sitio con `cita`
    propia, amplia `comprobar_citas_revocadas` en el mismo commit.
  - Las reglas no admiten cifras NI en un "nivel 0": `comprobar_contra` salta con el digito
    suelto. Se escribe "la entrada" y "el extremo de la caja".
  - `feedback apply` daba por NO-OP que el trader ratificara un default nuestro: comparaba la
    fuente anterior solo si era de tipo `feedback`, y un DEFAULT_AMBIGUOUS cita evidencia por
    definicion. Arreglado el 2026-09-11 con A-20. Si alguien anade un tipo de fuente, que mire
    esto.
  - Al cerrar una ambiguedad hay que tocar CINCO sitios y solo dos los vigila una guardia:
    el registro (via `apply`), `ambiguedades.yaml` (estado RESUELTA), la regla que la citaba
    -que probablemente citaba la evidencia DEBIL que abrio la duda-, la tabla de PROJECT_STATE
    y el recuento de `knowledge/spec/README.md`. Mas el test de `test_kit` que congela que
    ambiguedades estan RESUELTAS.
  - Una respuesta del trader POR ESCRITO fuera de sesion se registra con su captura en
    `Material adicional de su operativa/Mensajes del trader/`: asi el `respuesta_literal` son
    sus palabras y no una sintesis del consultor, que es la diferencia que A-11 y el lotaje
    tuvieron que declarar en `registrado_por`.
- Lecciones tecnicas (F11):
  - Los heredocs de bash convierten `` en el CARACTER backspace (0x08) dentro de un regex, y el
    patron deja de casar sin dar ningun error. Le paso a `test_no_business_literals`, que estuvo
    con dos patrones muertos sin que nadie lo viera. Escribir regex con Write o con `chr(92)`.
  - `make check` incluye `ruff format --check`: filtrar su salida con grep por "All checks passed"
    engana, porque esa linea la imprime `ruff check` y el format falla despues.
  - `grep -c` sin coincidencias devuelve exit 1 y corta un `&&`.
  - El paquete de una sesion ya celebrada NO se reproduce con `kit build`, y es correcto: el
    cuestionario se genera desde los parametros UNKNOWN y ya no lo estan. `kit check` lo trata
    como aviso si hay feedback de esa sesion.
- Lecciones tecnicas (F10): Dukascopy devuelve 503 y resets a mitad de mes: `data download`
  cachea por dia y se relanza hasta que el manifiesto existe; los literales de negocio no pueden
  ir en `src/` (`config.yaml` del kit); `random.shuffle` no es estable entre versiones (orden por
  hash); la guardia de fecha de commit se falsifica, la de ancestro no; el trader decide por
  sesion H4, no por dia.
- Lecciones tecnicas (F08): el token de CITA (F07, fiel a la cruda) y el token de BUSQUEDA (F08,
  acentos plegados y `0,75` = `0.75`) son distintos a proposito; `localizar_cita` no sirve para
  buscar frases (minimos de 4/3 tokens, una ventana, una localizacion): `buscar_secuencia` es la
  base comun; los segmentos de Whisper son de 5-15 s, asi que el AND va por segmento y la frase
  puede cruzar segmentos; `frames show` (mas cercano por pts) y `kb` (regular anterior
  existente, `referencia_en`) responden preguntas distintas.
- Lecciones tecnicas (F07): el ASR repite palabras en los bordes de segmento ("tiene tiene",
  "no no"): la cita literal las incluye; los segmentos con `boss/voz/blog/split` fuera de las 6
  sustituciones quedan como `dudas` y obligan `confianza: media`; la ventana `t0/t1` debe cubrir
  las palabras localizadas (+-2 s), el `--check` dice donde estan; una cita de <4 tokens o con
  `0,75` donde la cruda dice `0.75` no se localiza a proposito.
- Lecciones tecnicas (previos de F07): con `condition_on_previous_text=False` el
  `initial_prompt` solo condiciona la primera ventana de 30 s de cada fragmento; `hotwords`
  entra en todas pero alarga los segmentos mas alla de la ventana (hasta 40 s) y Whisper salta
  audio (~10 s perdidos en v5, "sell" -> "SL"); faster-whisper trunca el prompt a 223 tokens
  sin avisar (guardia `comprobar_prompt`, contar con `add_special_tokens=False`); medir SIEMPRE
  con la pasada oficial (`corpus transcribe`), no solo con un script suelto (el paso 1 no
  mostro la perdida, el paso 2 si); el YAML estricto rechaza un valor que empieza por comillas
  y sigue texto (`motivo: "x" ...`): sin comillas o todo entrecomillado; `write_text` sin
  `newline="\n"` mete CRLF en Windows y rompe `test_repository_integrity`; las herramientas de
  la sesion no suben binarios grandes a Drive (API: texto/base64 en el mensaje; navegador:
  dialogo nativo; `file_upload`: 10 MB).

## F05 (validada el 2026-09-05)
- Fotogramas de TODO el corpus a 1 fps en PNG sin perdida (ADR-0008), decision del usuario
  ("maxima fidelidad, sin restriccion de recursos") tras medir que una regla de "tramos con
  decision" marca el 46-99 % de cada video. 5 videos: 16 548 fotogramas (8,9 GiB los cuatro de
  F05 + v5) en `data/fotogramas/` (solo en esta maquina; se regeneran en ~11 min con `corpus
  frames extract`). Manifiestos inmutables `fr-v1-5a2a42c3`, `fr-v2-c5a09508`, `fr-v3-982da728`,
  `fr-v4-9ad0ebb8`, `fr-v5-718ecabb` (uno activo por video).
- Informe `docs/validation/F05-frame-extraction.md`: obligatorios leidos, candidatos A-9, ficha
  de reglas en Word (`fr-v3-982da728/101000`), material del 2026-09-05 (v5, xlsx abril, capturas),
  dos auditorias de cierre aplicadas.
- Material del 2026-09-05 ("Info extra de backtesting"): v5 `2026-09-05 21-03-59.mkv` (6 min,
  FXReplay abril; `tr-v5-large-v3-int8-float16-01a1ae03`, 99 segmentos, reemplazada el 2026-09-06
  por `tr-v5-...-3c6fbb57`, 80; en Drive desde el 2026-09-06), xlsx
  abril 2026 (38 operaciones) y 6 capturas de Analytics en `Material adicional de su operativa`.
  Hechos en PROJECT_STATE (seccion "Lineamientos recibidos del usuario y hechos del corpus", ya con ids de evidencia desde F07).
- Lecciones tecnicas: `fps=1` de ffmpeg NO da el fotograma del segundo exacto ni conserva el
  `pts` (regla `select` + `-fps_mode passthrough`); `-ss` necesita `-copyts`; `showinfo` despues
  de `select`; `start_time` debe ser 0. Otra build de ffmpeg = otra carpeta y otro manifiesto con
  `--reemplaza-a`.

## Metodo de trabajo acordado con el usuario
1. Brief en `docs/plan/features/F##-*.md` -> revision de diseno por un agente ANTES de programar.
2. Construir en la rama; commits pequenos; `make check` (o `uv run --no-sync ...` si la GPU tiene
   abierto `botsito.exe`).
3. Auditoria de cierre con dos agentes en paralelo (codigo/tests y docs/proceso) -> aplicar
   correcciones -> informe WAITING_FOR_USER_VALIDATION -> decirle al usuario explicitamente que
   pasos seguir y que debe decidir.
4. El usuario valida -> ritual, con `BOTSITO_ALLOW_MAIN=1` EXPORTADA durante toda la secuencia
   (la exige el hook `pre-commit` en el commit `docs(state)`, NO el merge: `git merge --no-ff`
   no dispara `pre-commit` y no hay `pre-merge-commit`): `git merge --no-ff` -> `git tag -a stable/F##`
   sobre el merge -> commit `docs(state)` que solo toca PROJECT_STATE.md -> `make check` -> push
   main + tag. (`state check` falla a proposito entre el merge y el docs(state).) El HANDOFF ya
   vino actualizado en la rama.
5. Commits que toquen `knowledge/spec` o `knowledge/cases` necesitan trailer `Fuente: ADR-NNNN` o
   ids `ev-`/`fb-` existentes. `knowledge/evidence`, `knowledge/feedback`, `data/manifests`,
   `knowledge/corpus/transcripciones` y `knowledge/corpus/fotogramas` son inmutables (hook +
   historial de git).
6. El usuario exige evidencia (hechos / hipotesis / inferencias separados), no quiere
   recomendaciones prematuras y quiere saber siempre "que debo hacer ahora".

## Comandos utiles
```
make check
uv run botsito knowledge validate
uv run botsito corpus transcript check
uv run botsito corpus transcript show --video v1 --t0 0:06:19 --t1 0:06:19 --margen-s 30
uv run botsito corpus transcribe --video v1        # reanudable; no llama al modelo si ya esta
uv run botsito corpus frames check
uv run botsito corpus frames show --video v3 --t 0:28:56 --n 3
uv run botsito corpus frames extract --video v5    # idempotente
uv run botsito kb find "break even" --top 10       # busqueda con fuente (F08)
uv run botsito kb at --video v4 --t 0:44:56 --contexto
uv run botsito spec check                              # la capa semantica sola (F12); sale con 1
uv run botsito kit build --sesion 2026-09-20-sesion-02 --seed 20260920   # paquete de sesion (F10)
uv run botsito kit check --sesion 2026-09-09-sesion-01   # el paquete real de la sesion 1
uv run botsito kit kappa --sesion-a 2026-09-09-sesion-01 --sesion-b 2026-09-20-sesion-02
uv run --no-sync python scripts/hoja_sesion_docx.py   # hoja de respuestas en Word (raiz)
```

## Lecciones operativas
- `make check` mira la rama ACTUAL contra `Current Branch` de PROJECT_STATE: si creas la rama
  despues de pasar `make check`, la CI falla aunque en local estuviera verde. Crea la rama, ajusta
  PROJECT_STATE y luego valida.
- `knowledge validate` (guardia del trailer `Fuente:`) solo ve commits existentes: correrlo
  DESPUES de commitear cuando el commit toque `knowledge/spec` o `knowledge/cases` (README incluido).
- El clasificador del modo automatico de Claude Code bloquea `rebase`, `cherry-pick`, `branch -f`
  y a veces el merge a `main` con `BOTSITO_ALLOW_MAIN=1`: el usuario ejecuta esos comandos con `!`.
- La CI se consulta sin `gh`: `curl -s https://api.github.com/repos/Fibobrioso/Botsito/commits/<sha>/check-runs`
  (los logs del job requieren el token de `git credential fill`). El merge no tiene run propio: el
  que cuenta es el del `docs(state)`. Mirar SIEMPRE la CI de main tras el ritual.
- Heredocs bash con comillas simples anidadas o barras invertidas fallan en Git Bash: escribir el
  script a un fichero del scratchpad y ejecutarlo.
- Escribir ficheros con `newline="\n"`; git en UTF-8 con `core.quotepath=false`.
- Agentes: pueden caer por limite de sesion; si pasa, hacer la auditoria a mano y decirlo.
- Dukascopy da 503/cortes: la descarga tiene cache por dia y reintentos.
- Datos pesados (`data/transcripciones/`, `data/fotogramas/`) no estan en git: si se cambia de
  maquina, copiarlos o regenerarlos (transcribir ~1 h de GPU; fotogramas ~11 min).
