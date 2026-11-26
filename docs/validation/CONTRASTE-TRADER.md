# CONTRASTE-TRADER · El contraste con el trader de ADR-0099 §6 y la petición escrita de los meses del backtest con costes (R4.7, entrada F)

> Informe de la rama. La fase 0 (skill fase-cero) está en §0 y §5; la respuesta del consultor y lo
> que entra tras ella, en §6 a §8; el revisor, al final.

Rama `trabajo/contraste-trader`, abierta el 2026-11-25 desde `main` en 6c113d16 (commit de estado
sobre el merge 42fdb0b5 del tag `stable/F39n-diagnostico-premisa`). Encargo y su añadido (A1-A5):
`docs/encargos/trabajo-contraste-trader.md`. Tramo: R4 (R4.7 de `docs/plan/HOJA-DE-RUTA.md`; la F
de la Next Action). Tag previsto: `stable/F39o-contraste-trader` (no existe ni en local ni en
origin: `git tag -l "stable/F39o*"` y `git ls-remote --tags origin "stable/F39o*"` vacíos).

## Base comprobada (abrir-rama, paso 1)

- `git rev-parse main origin/main` (tras `git fetch origin`):
  `6c113d161eb7e83bb185306b57a3bb6fa078eeaf` dos veces; `git status --short` vacío.
- `git rev-parse "stable/F39n-diagnostico-premisa^{commit}"` =
  `42fdb0b59c9fa2ea29c35c2551c43c8c1494452b` = `git rev-parse main^1` (el merge); en origin,
  `git ls-remote --tags origin "stable/F39n*"` da `518bbbe6…` (el objeto del tag anotado) y
  `42fdb0b5…` (`^{}`). Es el último `- Tag: ` de HISTORIA (línea 21209) y el último `stable/*` de
  origin.
- CI de `main` sobre su HEAD: `gh run list --branch main --limit 2` → 45670800735, `6c113d16`,
  `completed`, `success`; la API de check-runs con el sha literal da el check `python`
  (139405198029) en `completed` / `success`.
- `git branch --list` solo daba `main`; `git ls-remote --heads origin` solo da `refs/heads/main`, y
  `git ls-remote --heads origin "fix/*"` sale vacío.
- Sesión en Opus 5.5, esfuerzo alto (`/model` al empezar);
  `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1` puesta (medido con `echo`).

## 0. Fase 0

Medido el 2026-11-25 (reloj local, UTC-5). Ninguna imagen abierta, ningún audio escuchado por la
sesión. Lo que se ha leído, en la fila de HOLDOUT del día (§0.1).

### 0.1 La fila de HOLDOUT del día

Escrita y estadiada antes del primer `make check` del día, y commiteada con la apertura
(`459b4514`). Lleva, como su punto (1) y nombrada como **desviación de ADR-0021 §4**, la
declaración **escrita tarde del 2026-11-23**: la transcripción con ASR de los audios, hecha ese día
fuera de cualquier rama y sin cuarentena, y lo que vieron Aleks y el consultor (ADR-0099 §8,
«Las respuestas del trader del 2026-11-23»). Comprobado antes que ninguna fila lo recogía: las del
2026-11-23 (`trabajo/puente-techo`, `HOLDOUT-EXPOSICIONES.md`:189) y del 2026-11-24
(`trabajo/puente-techo` :190 y `trabajo/diagnostico-premisa` :191) dicen «ningún mensaje ni audio
del trader», o «ni sus mensajes o audios del 2026-11-23»; la del 2026-11-25 de esa rama (:192),
lo mismo. Precedente de fila tardía: :172 (`trabajo/sesion-08`, «Escrita tarde para el 2026-11-20
(v20)»).

Lo que esa fila no puede afirmar y pregunta a Aleks (§5, pregunta 4): si el 2026-11-23 Aleks o el
consultor leyeron algo más que las respuestas escritas y el resumen de los audios.

### 0.2 El material

**Las cuatro capturas** (en `corpus/Estrategia del trader/Material adicional de su operativa/Mensajes del trader/`;
`sha256sum` y `ls -l`, SIN ABRIRLAS):

| Nombre en disco hoy | Bytes | sha256 medido | ¿= A1? | Nombre de A5 |
|---|---|---|---|---|
| `Captura de pantalla 2026-11-25 160650.png` | 391.604 | `65a2d71e9e223dd87d4c4edf68d754cb59881e220923b68ff7faca799306f4ca` | sí | `mensaje-whatsapp-2026-11-23-0126-cinco-preguntas.png` |
| `Captura de pantalla 2026-11-25 160703.png` | 76.224 | `a635f76f3be4c89959822767268a6d8dfc3f115e801e68febe82fad7d9f7ef28` | sí | `mensaje-whatsapp-2026-11-23-0956-operativa-real.png` |
| `Captura de pantalla 2026-11-25 160945.png` | 168.123 | `33fa10d2728bb956951e5e283a9153ad37c4e74ac85fce8a6172fa6a7b139ed7` | sí | `mensaje-whatsapp-2026-11-24-1718-propuesta-backtest-costes.png` |
| `Captura de pantalla 2026-11-25 161009.png` | 318.435 | `f47da4e8ffb5b787e8a6c4ed81e56a1186577f5fae6f3a0de5ff98502e5d57dc` | sí | `mensaje-whatsapp-2026-11-24-1719-meses-enero-julio-2024.png` |

Los cuatro coinciden con A1 byte a byte. **El cambio de nombre lo negó la guardia** (`mv` de la
primera: «origen de `mv`: Captura de pantalla 2026-11-25 160650.png», regla de las imágenes del
material adicional, ADR-0038); no se rodeó, y no se intentó con las otras tres. Lo hace Aleks
(§5, decisión 0), como el 2026-10-25 (`fuentes.yaml`, «Aleks la guardo con doble extension (`.png.png`)
y la renombro»).

**Los audios del 2026-11-23** (`C:\Users\USER\Desktop\audios-trader-2026-11-23\`, ocho `.ogg` de
WhatsApp, `WhatsApp Ptt 2026-11-23 at <h.mm.ss> AM.ogg`). Copiados con `cp -n` a la misma subcarpeta
del corpus (la guardia no lo negó) y vueltos a hashear: cada copia da el sha256 del original.

| Original (hora de WhatsApp) | Entra como | Bytes | sha256 | Duración (ASR) |
|---|---|---|---|---|
| `9.59.25 AM` | `audio-whatsapp-2026-11-23-0959-caja-en-una-vela.ogg` | 421.749 | `151a23bbad3baefc6cca793ad951ec0a0ff33afafdf2906ec96f7e6f1cd92011` | 170,6 s |
| `9.59.43 AM` | `audio-whatsapp-2026-11-23-0959-protegido-en-0-80.ogg` | 38.026 | `b74803c54ee28f58236493294b88b9b7daf566c28f37991f42de2570f0ebaaea` | 15,5 s |
| `10.01.41 AM` | `audio-whatsapp-2026-11-23-1001-break-even-y-comision.ogg` | 120.403 | `d1986b2275db4fe2878d9831b990fb5e1b8b2063f7092de1c2b06cb62d7656f6` | 47,2 s |
| `10.02.00 AM` | `audio-whatsapp-2026-11-23-1002-calculo-del-break-even.ogg` | 38.510 | `2e6d6bba7fed1e00493b8d0355d5a2c49b94d759192d37fa2d7dc600afcb551c` | 15,2 s |
| `10.07.46 AM` | `audio-whatsapp-2026-11-23-1007-recalculo-y-reunion.ogg` | 351.319 | `22704d844fc9ca730e71b27109d0145ef04cc3e9bb39643e1752f9edb39ebade` | 140,7 s |
| `10.10.48 AM` | `audio-whatsapp-2026-11-23-1010-objetivo-y-191-operaciones.ogg` | 387.646 | `bb7121e34315d27b076dbe49ed6e0d775ffdeaef5e4ae7fc0113bf68f8198199` | 157,8 s |
| `10.13.09 AM` | `audio-whatsapp-2026-11-23-1013-fundednext-y-esquemas.ogg` | 273.451 | `2d93a892bb6bfa82c487b575ff282c665a563589f0a895ca64311422a9217056` | 109,4 s |

- **El duplicado, que no entra:** `WhatsApp Ptt 2026-11-23 at 9.59.43 AM (1).ogg`, 38.026 bytes,
  sha256 `b74803c54ee28f58236493294b88b9b7daf566c28f37991f42de2570f0ebaaea`, el mismo que el de
  `9.59.43 AM` byte a byte.
- **Dos audios con la misma hora (09:59):** el `<tema>` los distingue; la hora es la del nombre de
  WhatsApp, recortada a HHMM.
- **Formato:** `.ogg` de WhatsApp por la extensión. **`ffprobe` lo negó la guardia** («no es un
  contenedor de video reconocido (extension .mp4, .mov, .mkv, .webm y sus bytes magicos)»;
  `GUARDIA-FFMPEG.md`); no se rodeó. **La duración** es la que escribió el ASR el 2026-11-23 en la
  cabecera de cada transcripción (`duracion: … s`, leída con `grep '^duracion:'`), no una medida de
  hoy; `corpus inventory` no mide la duración de lo que no es un vídeo de `fuentes.yaml`
  (`inventario.py`:248-291).
- **El audio de A2** (`audio-whatsapp-2026-11-24-1801-valida-meses.<ext>`): **no está** en la
  subcarpeta (`ls -la`, 16:20); lo exporta Aleks (§5, decisión 0).
- **Las transcripciones del 2026-11-23**, que no entran (D2): ocho `.txt` al lado de cada audio,
  escritos por `transcribir.py` (fuera del repo, sha256
  `43ef4a627d1c460464e024574c70850a7c14b5e462b05b87aa6454b40c5d1a73`), que llama tal cual a la
  función `transcribir` de `scripts/transcribir_sesion.py` (faster-whisper `large-v3`, `int8_float16`,
  cuda, `beam_size` 5, `temperature` 0, `vad_filter`, `initial_prompt_sha256`
  `327e1ef9…`, modelo sha256 `69f74147…`, igual en las ocho). Formato `mm:ss · texto`. sha256:

  | Transcripción de | sha256 |
  |---|---|
  | `9.59.25 AM` | `a9eef6eb66b687c68c10b155e6bbfd673bdff01f447908bb5a606735af72f8c4` |
  | `9.59.43 AM` | `3d954351da0fa714677e25aad52bf29d723c6c896d1e3d48c61c3c99ee351578` |
  | `9.59.43 AM (1)` (el duplicado) | `1c029cbc4640da658623d43292fb71a09b9c2e84624b6e417c0299d0679e00a0` |
  | `10.01.41 AM` | `a0957fb11baa3fd1805c0187ac241209eb2ffc93e3a800dc39eec0062e372f40` |
  | `10.02.00 AM` | `b72d160feac8c9bd75b23040660aebb920a891cb736775eac5d442d7a9c91225` |
  | `10.07.46 AM` | `b1ca3c6ef66524c0db3cf1f1c7141c2c14b8bf4efcd526683b16a5872dba162e` |
  | `10.10.48 AM` | `975416ce9b45de735981cab71465d278c7f954ea1512bc3d1eb389efa774e05f` |
  | `10.13.09 AM` | `7674e794213629d922a1f61325b69e1f5f15bbe0a181db06cb501f1a0e4a1bef` |

  Las dos del audio duplicado difieren en bytes (1.015 y 1.019) por la línea `audio:` de su
  cabecera; el texto es el mismo.
- **El vídeo de mapeo y el backtest de diciembre de 2025 siguen fuera de `corpus/`:** ningún nombre
  de `corpus/` casa con `*mapeo*`, `*diciembre*`, `*2025-12*` ni `*dic*2025*` (`find corpus -iname …`;
  `*dic*` solo casa con «Material adicional»), y las únicas carpetas `Backtest*` hasta la
  profundidad 3 son las de julio, marzo, mayo y septiembre de 2026. **Desviación de la skill
  fase-cero**, que pide no recorrer una carpeta madre de meses reservados con un filtro: el `find`
  recorrió `corpus/` entero por NOMBRE; no imprimió ningún fichero de dentro de una carpeta
  `Backtest` (ninguno casó). Declarado en la fila del día, punto (2).

### 0.3 El inventario, en un clon desechable

`git worktree add --detach` en la carpeta de trabajo de la sesión, en `459b4514`. Un worktree no
tiene `corpus/` (fuera de git) y la raíz del corpus sale de `fuentes.yaml` (`raiz: "corpus/Estrategia
del trader"`, relativa a `--repo`; `inventario.py`:242-245), así que el `fuentes.yaml` DEL CLON se
cambió, con Edit, a la raíz absoluta del corpus real (la vía de `comparar-con-main` con
`settings.local.toml`); sin unión ni enlace (la unión de `corpus/` rompió la guardia el 2026-11-20).
Orden: `uv run botsito --repo <clon> corpus inventory`, con su log fuera del repo.

**Lo acepta**: exit 0, «OK: manifiesto escrito · heredado_v2: 477 ficheros, 117,626,282 bytes ·
material_adicional: 84 ficheros, 9,436,152 bytes · video_original: 21 ficheros, 98,507,386,788
bytes», sin ningún `AVISO`. `diff` del manifiesto de la rama contra el del clon:

- **11 entradas nuevas**, todas `papel: material_adicional` bajo `Mensajes del trader/`: las cuatro
  capturas (con su nombre de Windows de hoy, porque el cambio de nombre está pendiente) y los siete
  audios, cada una con los bytes y el sha256 de §0.2;
- **`resumen.material_adicional`**: `ficheros` 73 → 84 y `bytes` 6.850.662 → 9.436.152; la
  diferencia, 2.585.490, es la suma de las 11 (954.386 de las capturas y 1.631.104 de los audios);
- **`raiz:`**, que es la del `fuentes.yaml` del clon (la ruta absoluta del ensayo) y en la rama no
  cambia.

**Ninguna otra entrada cambia**: ni un vídeo, ni un fichero ya inventariado, ni la línea
`ffprobe:`. Así que no hay PARADA por 0.3. El inventario de verdad se repite en la rama tras el
cambio de nombre y con el audio de A2 (§5, decisión 1), y la forma esperada de su diff es esta con
los nombres de A5 y una entrada más. El clon se quitó tras el `diff` (`git worktree remove`).

### 0.4 Lo que nombra cada audio

`scripts/barrido_dias.py` **no admite el formato** de las transcripciones: pide líneas
`[mm:ss] texto` (`barrido_dias.py`:34) y las ocho son `mm:ss · texto` (`grep -cE '^\[[0-9]+:[0-9][0-9]\] '`
da 0 en las ocho). Además solo vería enteros de 18 a 31, no meses ni resultados (auditor, 25). Un
guion de recuento ciego de la carpeta de trabajo (meses, años, enteros y términos de resultado, solo
cifras) **lo negó la guardia** («el codigo recorre directorios que construye al ejecutarse y nombra
material sensible»); no se rodeó. Así que **el recuento es a mano**, como prevé el encargo, leyendo
las ocho transcripciones enteras (Read, por su ruta literal):

| Audio | Líneas de texto | Meses nombrados | Años | Días del calendario | Resultados de operaciones | Otras cifras |
|---|---|---|---|---|---|---|
| 0959-caja-en-una-vela | 21 | 0 | 0 | 0 | 0 | niveles de la caja, una relación de objetivo, un porcentaje de retroceso |
| 0959-protegido-en-0-80 | 1 | 0 | 0 | 0 | 0 | niveles de la caja, la relación de objetivo |
| 1001-break-even-y-comision | 5 | 0 | 0 | 0 | 0 | ninguna |
| 1002-calculo-del-break-even | 1 | 0 | 0 | 0 | 0 | ninguna |
| 1007-recalculo-y-reunion | 15 | 0 | 0 | 0 | 0 | la hora de una reunión; «los tres» trades comparados |
| 1010-objetivo-y-191-operaciones | 22 | 0 | 0 | 0 | 0 | niveles de la caja, relaciones de objetivo; **un recuento de operaciones de una medida nuestra** (§0.5, f) |
| 1013-fundednext-y-esquemas | 15 | 0 | 0 | 0 | 0 | ninguna (dice que tuvo ganadoras y perdedoras, sin cifra) |
| (duplicado, 9.59.43 AM (1)) | 1 | 0 | 0 | 0 | 0 | igual que su original |

**Total: 81 líneas de texto, 0 meses, 0 años, 0 días, 0 resultados.** Ningún gráfico ni día
operado: no hay material de un mes que no sea de construcción, así que no hay PARADA por 0.5 ni nada
para `meses_reservados.yaml`. El audio de A2 no está transcrito ni en disco: su recuento, cuando
Aleks lo escuche (§5).

### 0.5 El mapa de lo dicho

Las letras (a)-(f) son las expectativas del consultor del encargo, 0.5; «F#», las frases de §0.7.
Objetivos de `fb-` posibles: los de `TIPOS_OBJETIVO` (`feedback/modelo.py`:53-61; `evidence`,
`regla`, `parametro`, `ambiguedad`, `caso`, `contradiccion`). D1: ninguno se registra.

| Fuente | Tema | Expectativa | ¿Objetivo de `fb-`? | ¿Responde a algo pendiente? |
|---|---|---|---|---|
| 0959-caja-en-una-vela | que el bot traza la caja en una sola vela y no desde el esquema 1 o 2 (F1); que el objetivo se ha calculado desde el 0,8, cuando la referencia es la distancia 1-0 (F2) | (a) sí; (b) sí | (a) `ambiguedad` A-48; (b) `parametro` `base_calculo_objetivo` / `objetivo_rr` | (a): material para A-48 y S-3 (`ACTIVAR-SESION-08.md`:55) y la sesión siguiente (R4.6); no la cierra. (b): ver §0.6 |
| 0959-protegido-en-0-80 | la referencia del objetivo es la distancia 0-1 con el 1:3, y se protege en el 0,80 (F3) | (b) sí: la voz, según el ASR, dice la distancia 0-1, no «el stop» (por comprobar, §5 pregunta 3) | `parametro` `base_calculo_objetivo`, `objetivo_rr`, `stop_fraccion_caja` | nada pendiente: los tres CONFIRMED (`parametros.yaml`:671, 1116 y 1782, sus `valor`) |
| 1001-break-even-y-comision | un trade neutral no afecta; lo que conlleva es la comisión, que según él pesa poco (F4) | (c) sí, opinión | `regla` RN-014 (break even) | V18 de la auditoría «cazador» («Break even neto de costes… Pregunta al trader»; auditor, H5) y A-13 (break even, ABIERTA): lo toca, no responde a la pregunta de A-13 |
| 1002-calculo-del-break-even | el coste del break even se calcula con el número de break even y la comisión (F5) | (c) sí, opinión | `regla` RN-014 | como la fila anterior |
| 1007-recalculo-y-reunion | que va a recalcular sus trades con comisión y lotaje (F6); que el bot marca mal las cajas y que comparó tres operaciones suyas con las del bot (F7); una reunión esa noche (F8) | (a) sí; (e) sí; F6, premisa | ninguno (premisa y logística); (a) A-48 | (a) como arriba; F6, nada del repo |
| 1010-objetivo-y-191-operaciones | el objetivo, calculado sobre la distancia 0-1 (F9); una gestión que podría venir después (proteger o bajar al 0,50; F14); el recuento de operaciones de un análisis que acababa de leer (F10) y unos Excel recalculados (F11) | (b) sí; (f) sí | (b) `parametro`; F14, ninguno (gestión futura, no regla); (f), ninguno | (f): lo que se le enseñó, §5 preguntas 1 y 2 |
| 1013-fundednext-y-esquemas | que ha operado algunas operaciones en FundedNext, ganadoras y perdedoras, y las compartió en el grupo (F12); qué es el esquema 1 y el 2 (F13); que se manden los audios a un asistente para analizarlos | (d) sí; (a) sí | (d) ninguno (premisa; `firma` es la del bot, ADR-0026, auditor 33); (a) A-48 | (d): lo que ya trae el corpus de FundedNext, `ev-v4-012524-0ef85a89` (v4 1:25:24; auditor, H7), sin leerlo contra nada (D5); F13: tema de A-20 (una sola zona de control, cerrada) y de A-48 |
| captura 1 (01:26, Aleks) | las cinco preguntas; «las de M15 y las del PDF pueden esperar» | — | ninguno (es de Aleks) | A-35, A-43 y S-3 (WhatsApp del 2026-11-21, `ACTIVAR-SESION-08.md`:368) **siguen pendientes**: la captura lo dice (A4); la línea de A-35 de Technical Debt sigue |
| captura 2 (09:56, trader) | «1-c» (solo backtest), «2-foundnext», «3-si, todo igual», «4-no se trabajo con spreads o comisión», 5: las sesiones de FX Replay ya no están abiertas, «están en el grupo los excels» | premisa | ninguno (premisa y coste de FX Replay: sin objetivo) | 4: lo que ADR-0100 §1 cita; 5: toca la Q de la Next Action (la exportación de agosto; `PROJECT_STATE.md`:42; auditor, H4), no la cierra |
| captura 3 (2026-11-24 17:18, Aleks) | propone junio y noviembre de 2024, con costes y las condiciones | petición (D4) | ninguno | ADR-0100 §2 (los meses «por escrito»): el informe no lo juzga (D4) |
| captura 4 (2026-11-24 17:19-18:02) | el trader acepta junio y noviembre; Aleks pide enero y julio de 2024 «si todavía no arrancaste»; nota de voz de 0:14 (A2); «esos si son definitivos» | petición (D4) | ninguno | como la anterior. **Hecho (A3):** la petición de enero y julio no repite la pregunta de si ya los había hecho, que solo estaba en la captura 3, para junio y noviembre |
| audio de A2 (18:01, 0:14) | según Aleks, valida los meses | petición | ninguno | pendiente de que Aleks lo escuche (§5) |

Sin leer nada contra la premisa ni contra ninguna cifra (D5): la captura 2 dice «1-c» (ahora mismo
solo en backtest) y el audio 1013, según el ASR, que ha operado algunas operaciones en FundedNext;
las dos cosas se recogen tal cual, sin conciliarlas.

Los temas de los audios son paráfrasis del ASR del 2026-11-23, sin comprobar todavía: ninguna frase
de audio entra como literal hasta que Aleks la compruebe (D2, §5 pregunta 3).

### 0.6 El encargo frente al repo (subagente `auditor-encargo`)

Lanzado al empezar la fase 0, con el `make check` de la apertura corriendo (solo leyó). Resumen: 46
afirmaciones, 28 correctas, 3 incorrectas y 15 con matiz; 7 herencias. Lo que cambia algo:

- **Incorrecta, D3:** «Mensajes del trader» no tiene entrada propia en `fuentes.yaml`: es un párrafo
  de la descripción de `Material adicional de su operativa` (`fuentes.yaml`:348-388), y ya habla de
  dos gráficos H4 del trader, dos esquemas del consultor y una nota de voz de 0:21 que Aleks escuchó
  y no se registró (:353-354, :366-368, :373-375). D3 se aplica ampliando ESE párrafo (§5,
  decisión 2).
- **Incorrecta, (d):** «apalancamiento 1:30» y «deslizamiento apagado»; ya la corrige A3.
- **Incorrecta (en efecto), D2 matiz:** `transcribir_sesion.py` toma `--audio`, pero exige el
  `--video` de una sesión y si no, no escribe nada (:37-41, :49-51): la conclusión de D2 se sostiene.
- **Matiz, 0.3:** el diff del manifiesto no puede ser solo entradas nuevas: cambia siempre
  `resumen.material_adicional` (ficheros y bytes; `inventario.py`:306-314), y `ffprobe:` si cambió
  la versión (:318). Y el clon no tiene `corpus/` (H1). §0.3 y §5, decisión 1.
- **Matiz, D1 (ii):** `feedback/modelo.py`:37-51 son las ACCIONES; los objetivos están en :53-61 y
  :63-76. Y `knowledge/feedback/README.md`:79-82 manda «Si trae una respuesta, registro de
  feedback»: D1 se aparta de ese procedimiento escrito, con sus cuatro motivos, y el informe lo dice
  así (§5, decisión 3).
- **Matiz, (c) y 191:** 191 se publica también en `PUENTE-TECHO.md`:464, `DIAGNOSTICO-PREMISA.md`:223
  y :417, y `AUDITORIA-CAZADOR-2026-11-23.md`:41, :50, :90 y :103: la foto pudo salir de cualquiera
  (cuenta para D7).
- **Matiz, (b):** ADR-0100 §1 (:25) describe con «objetivo a 3 veces el stop» la variante
  `todo_junto`, la del registro, frente a la regla dicha, «objetivo a 3 veces la caja»
  (ADR-0099:28): esa diferencia es A-56. Lo que dice la voz: §0.5, F3 y F9 (la distancia 0-1).
- **Matiz, A5:** la guardia mira el origen de `mv` como lectura y niega las imágenes del material
  adicional: medido, §0.2.
- **Matiz, §7:** PROJECT_STATE en la rama ya está en 24.922 bytes; la línea de Technical Debt de D2
  y la F «sin que crezca» se miden en las líneas del cierre.
- **Herencias:** H1 (el clon sin `corpus/`), H2 (`corpus check --hashes` tras el inventario, la
  pareja de las ramas de sesión), H3 (la captura de configuración de FX Replay del 2026-11-24 trae,
  detrás, el panel de cuenta «Backtesting, Lifetime», agregados que no pueden entrar; ADR-0100:200),
  H4 (la Q), H5 (V18 y A-13), H6 (el contraste no tiene entrada propia en la hoja de ruta: R4.7 lo
  lleva en su «Qué es»), H7 (FundedNext en `ev-v4-012524-0ef85a89`). Y una lección:
  `ERRORES-RECURRENTES.md`:86 («la nota de voz situada en la captura equivocada»): que Aleks confirme
  que la nota de 0:14 es la de la captura 4.

El informe entero del auditor, al final de este informe (§«Informe del auditor»).

### 0.7 Las frases que el informe citaría, para que Aleks las compruebe escuchándolas (D2)

El texto del ASR del 2026-11-23 de cada una NO entra en este commit: va en el mensaje de la
PARADA, y solo las que Aleks compruebe entrarán como literales, marcadas como ASR, tras su
respuesta (D2). El minuto es el del inicio del segmento del ASR.

| F | Audio | Minuto | Tema |
|---|---|---|---|
| F1 | 0959-caja-en-una-vela | 00:00-00:36 | la caja trazada en una sola vela frente al esquema 1 o 2 |
| F2 | 0959-caja-en-una-vela | 02:03-02:42 | desde dónde se ha calculado el objetivo (el 0,8) y la referencia 1-0 |
| F3 | 0959-protegido-en-0-80 | 00:01 | la referencia del objetivo (0-1 con el 1:3) y la protección en el 0,80 |
| F4 | 1001-break-even-y-comision | 00:23-00:36 | el break even y la comisión |
| F5 | 1002-calculo-del-break-even | 00:00 | cómo se calcula el coste del break even |
| F6 | 1007-recalculo-y-reunion | 00:00-00:07 | recalcular sus trades con comisión y lotaje |
| F7 | 1007-recalculo-y-reunion | 01:27-01:36 | objetivo y stop en una sola vela, y el margen para el spread |
| F8 | 1007-recalculo-y-reunion | 01:54-02:09 | la reunión de esa noche |
| F9 | 1010-objetivo-y-191-operaciones | 00:28-00:34 | el objetivo sobre la distancia 0-1 |
| F10 | 1010-objetivo-y-191-operaciones | 01:52-01:59 | el recuento de operaciones de lo que acababa de leer |
| F11 | 1010-objetivo-y-191-operaciones | 02:07 | el sesgo y los Excel recalculados |
| F12 | 1013-fundednext-y-esquemas | 00:17-00:32 | las operaciones en FundedNext, compartidas en el grupo |
| F13 | 1013-fundednext-y-esquemas | 01:15-01:40 | qué es el esquema 1 y el 2 |
| F14 | 1010-objetivo-y-191-operaciones | 00:55-01:10 | una gestión posible (proteger o bajar al 0,50) |
| A2 | audio-whatsapp-2026-11-24-1801-valida-meses | — | sin transcribir: la frase que lo resume, la de Aleks al escucharlo |

### 0.8 Lo que no pude medir

- La duración y el códec de los audios hoy: `ffprobe` negado sobre `.ogg` (§0.2); va la del ASR.
- El recuento ciego de las transcripciones: negado el guion (§0.4); va el recuento a mano.
- El audio de A2: no está en disco.
- Qué era la foto de «las 191 operaciones», ni las capturas de las operaciones del bot que el
  trader dice haber recibido con los últimos vídeos (0959, 00:43), ni los Excel recalculados (F11): no
  los tengo y no los busco (encargo, (c)).
- Que la nota de voz de 0:14 esté en la captura 4 y que la captura 3 sea del 2026-11-24 a las 17:18:
  las capturas no se abren (A1; Aleks lo confirma).

### 0.9 Exposiciones declaradas

La fila del 2026-11-25 de `trabajo/contraste-trader` (§0.1), con la tardía del 2026-11-23. Lo que
se le enseñó al trader (c), en otra fila, con la respuesta de Aleks (D7).

### 0.10 Un error de la sesión, sin consecuencia

Con el `make check` de la apertura corriendo, la sesión puso un `ScheduleWakeup` de respaldo, que
crea `.claude/scheduled_tasks.lock` (ignorado por git) y tumba `test_no_unexpected_ignored_paths`
(lo recoge la memoria de la sesión desde el 2026-11-23). Se canceló y el lock se borró a mano a los
pocos segundos; ese `make check` salió en verde y sellado (3624 passed, `SELLO` sobre
`af5b2398…`). Va a la fila de ERRORES-RECURRENTES del cierre.

## 5. PARADA

### Preguntas a Aleks

1. Copiada tal cual del encargo: «¿Qué era la foto a la que el trader respondió con "las 191
   operaciones"? Qué documento, qué se veía (cifras de R, número de operaciones, porcentajes, meses)
   y cuándo se la mandaste.»
2. El trader habla además, según el ASR, de capturas de las operaciones del bot que se le mandaron
   con los últimos vídeos (0959-caja-en-una-vela, 00:43) y de unos Excel recalculados (F11). ¿Qué eran, y
   llevaban alguna cifra de una medida nuestra?
3. Escuchando los audios: ¿cada frase F1 a F14 de §0.7 dice lo que transcribe el ASR? Corrige lo que
   no (en F5, si dice «sin multiplicarlo» o «y multiplicarlo»). Del audio de A2, la frase que lo
   resume, y si nombra algo más que los meses (un día, otro mes o un resultado).
4. El 2026-11-23, ¿leísteis tú o el consultor algo más que las respuestas escritas y el resumen de
   los audios (las transcripciones, los audios enteros)?
5. ¿La captura 3 es del 2026-11-24 a las 17:18, y la nota de voz de 0:14 es la que se ve en la
   captura 4? ¿Tienes una captura de la configuración de FX Replay SIN ningún resultado? (La del
   2026-11-24 trae detrás el panel «Backtesting, Lifetime» de toda la cuenta: un agregado con meses
   reservados, que por (d) no entra; auditor, H3.)

## Lo que necesito que decidas

0. **El cambio de nombre y el audio de A2.** La guardia niega el `mv` (§0.2). Opciones: (a) Aleks
   renombra las cuatro capturas y deja el audio de A2 en la subcarpeta, y la sesión hashea de nuevo
   antes del inventario; (b) entran con el nombre de Windows. Recomiendo (a): es lo que piden A2 y
   A5, y el patrón de la carpeta. Coste de (b): cuatro nombres que no dicen qué son en el manifiesto,
   para siempre (es solo añadir). Las órdenes, para teclear con `!` desde la raíz del repo:

   ```
   ! cd "corpus/Estrategia del trader/Material adicional de su operativa/Mensajes del trader" && mv -n "Captura de pantalla 2026-11-25 160650.png" mensaje-whatsapp-2026-11-23-0126-cinco-preguntas.png && mv -n "Captura de pantalla 2026-11-25 160703.png" mensaje-whatsapp-2026-11-23-0956-operativa-real.png && mv -n "Captura de pantalla 2026-11-25 160945.png" mensaje-whatsapp-2026-11-24-1718-propuesta-backtest-costes.png && mv -n "Captura de pantalla 2026-11-25 161009.png" mensaje-whatsapp-2026-11-24-1719-meses-enero-julio-2024.png
   ```

1. **El inventario de verdad.** El ensayo en el clon dio lo esperado (§0.3). Opciones: (a) tras la
   decisión 0, `corpus inventory` en la rama (su `manifest.yaml` está en `rutas_permitidas`), con el
   `diff` comprobado contra la forma del ensayo (12 entradas nuevas y el `resumen`, sin la línea
   `raiz:`) y, después, `corpus check --hashes` (auditor, H2); (b) repetir antes el ensayo en otro
   clon con los nombres nuevos. Recomiendo (a): el ensayo ya midió qué cambia y que nada más se
   mueve, y si el `diff` real trae otra cosa, PARA como dice 0.3. Coste de (b): otra hora de hash
   del corpus entero sin saber nada nuevo.
2. **D3, dónde se amplía `fuentes.yaml`.** «Mensajes del trader» no tiene entrada propia: es un
   párrafo de `Material adicional de su operativa` (§0.6). Opciones: (a) se amplía ese párrafo, con
   la forma de la entrada del 2026-10-14 (lo que entra, su fecha y rama, que trae audios por primera
   vez, y las cautelas de D3); (b) una entrada propia en `carpetas`. Recomiendo (a): `clasificar`
   toma la carpeta más larga que case (`inventario.py`:199-201), así que (b) no cambia ningún papel
   pero parte en dos la historia de la subcarpeta. Coste de (b): ninguno técnico; partir lo escrito.
3. **D1 frente a `knowledge/feedback/README.md`:79-82** («Si trae una respuesta, registro de
   feedback»). Opciones: (a) se mantiene D1 y el informe lo dice como apartamiento del procedimiento
   escrito, con sus cuatro motivos; (b) un `fb-` donde haya objetivo (A-48 o los tres parámetros).
   Recomiendo (a): (b) choca con D1 (iii), porque un CONFIRM de los parámetros taparía A-56, y con
   D1 (iv), porque el literal saldría de un ASR hecho fuera de rama sin `t1` comprobable. Coste de
   (a): la respuesta del trader sobre el objetivo y el stop queda solo en este informe hasta el ADR
   de ADR-0099 §7.
4. **Lo que la tabla de §0.5 nombra y no cambia** (auditor H4, H5, H7): la respuesta 5 de la
   captura 2 frente a la Q; F4 y F5 frente a V18 y A-13; F12 frente a `ev-v4-012524-0ef85a89`; y,
   sin conciliarlas, la captura 2 («1-c») frente a F12. Opciones: (a) quedan nombradas en el informe
   y en «Para el ADR de C», sin tocar la Q, A-13 ni ninguna evidencia, ni preguntar nada al trader
   desde esta rama; (b) alguna sube a la Next Action. Recomiendo (a): D5 deja la lectura al ADR de
   ADR-0099 §7. Coste de (b): una línea de PROJECT_STATE, que está a 78 bytes del tope.
5. **La hoja de ruta (auditor H6).** Opciones: (a) el cierre apunta el contraste en el «Qué es» de
   R4.7 como hecho, sin entrada nueva; (b) una entrada R4.11 HECHA, como R4.8 y R4.9. Recomiendo (a):
   el encargo pone R4.7 y la entrada sigue ABIERTA hasta el ADR de C. Coste de (b): una entrada para
   una rama sin medida.
6. **Las dos guardias que negaron medidas legítimas** (el recuento ciego de §0.4 y `ffprobe` sobre
   `.ogg`). La skill fase-cero las da como hallazgo **importa**. Opciones: (a) a la fila de
   ERRORES-RECURRENTES del cierre y a «Carril: guardias y deuda» de la hoja de ruta en el cierre, sin
   tocar `.claude/` aquí (lo prohíbe §2); (b) a Technical Debt de PROJECT_STATE. Recomiendo (a): el
   recuento a mano y la duración del ASR bastaron, y PROJECT_STATE no tiene sitio. Coste de (b): que
   no cabe sin quitar otra línea.

**Espero tu respuesta a la PARADA** (Aleks: las preguntas 1 a 5 y la decisión 0; el consultor: las
decisiones 1 a 6 y lo que la medida haya dejado abierto).

## Respuesta del consultor a la PARADA (2026-11-25, 18:40, hora de Lima), tal cual

Con las respuestas de Aleks al final, como llegaron (la 2, la 3, la 4 y la segunda parte de la 5,
vacías). Copiada también al final del encargo.

> Modelo: Opus 5.5 · Esfuerzo: alto
>
> RESPUESTA DEL CONSULTOR A LA PARADA de `trabajo/contraste-trader` (2026-11-25, 18:40, hora de Lima). Cópiala tal cual al informe, en su sección de la PARADA, junto con las respuestas de Aleks que van al final de este mensaje.
>
> Veredicto: la fase 0 cumple el encargo y el añadido. Acepto las decisiones 0 a 6 con los matices de abajo.
>
> 0. Nombres y audio. Aleks renombra las capturas con tu orden «!». Después vuelve a calcular el sha256 de los cuatro nombres nuevos: tienen que ser los de A1, y si alguno no coincide, PARA. El audio de A2 NO entra: según Aleks (respuesta 5) es solo una risa. Corrección del añadido, error del consultor: A2 y A3 decían que el trader «valida» los meses en ese audio, y no es así. El informe pone la secuencia de las capturas 3 y 4 tal cual: el trader acepta por escrito junio y noviembre de 2024; Aleks pide por escrito enero y julio de 2024 si aún no había arrancado; el trader no contesta por escrito a eso (solo una nota de voz que, según Aleks, es una risa); y Aleks escribe «esos si son definitivos». Sin juzgar ADR-0100 §2 (D4). Sí dice, como hecho, que ninguna captura recoge que el trader no haya operado nunca enero ni julio de 2024.
>
> 1. Inventario: de acuerdo. Lo corres en la rama, compruebas que el diff es el del ensayo (11 entradas nuevas y el bloque resumen) con la raíz SIN cambiar, y después `uv run botsito corpus check --hashes`. Si cambia cualquier otra línea, PARA.
>
> 2. fuentes.yaml: de acuerdo. Amplías el párrafo de «Mensajes del trader» dentro de «Material adicional de su operativa», con la forma de la entrada del 2026-10-14 y las cautelas de D3. No creas una entrada propia.
>
> 3. D1 se mantiene: ningún `fb-`. El informe declara que esto se aparta del paso 4 de knowledge/feedback/README.md:79-82 («si trae una respuesta, registro de feedback»), y por qué: las respuestas no tienen objetivo en el esquema, nada se cierra y un CONFIRM escondería A-56. El README no se toca en esta rama. Precisarlo («si trae una respuesta a un objetivo del esquema») es una línea para «Carril: guardias y deuda» de la hoja de ruta en el cierre.
>
> 4. De acuerdo: el informe nombra Q, V18, A-13 y `ev-v4-012524-0ef85a89` (lo que ya hay de FundedNext) solo por su id, sin tocar ninguno.
>
> 5. De acuerdo: ninguna entrada nueva en la hoja de ruta. El cierre lo apunta en el «Qué es» de R4.7.
>
> 6. De acuerdo. Además, nada de esta rama crece PROJECT_STATE (está a 78 bytes del tope). Van todas a «Carril: guardias y deuda» en el cierre: las dos guardias que negaron medidas legítimas (ffprobe sobre .ogg, el guion de recuento y el cambio de nombre), la transcripción de audios sueltos que falta en `main` (D2) y la precisión del README (punto 3). Al informe solo van las líneas propuestas.
>
> 7. Los literales de los audios. Cuentan las frases que Aleks confirma en la respuesta 3. Donde Aleks corrige, la versión de Aleks es el literal, marcada «[corrige Aleks]». Donde confirma, va el texto del ASR tal cual. Tus cinco lecturas («13» → 1:3; «08»/«080» → 0,8/0,80; «pib» → pip; «funda de nex» → FundedNext; «esquema 12» → esquema 1 y 2) van como nota tuya al pie de la tabla, «lectura de la sesión», salvo las que Aleks diga que oye así. Ninguna frase que Aleks no haya escuchado entra al informe. Si la respuesta 3 está vacía, no entra ningún literal de audio: por cada audio, el fichero, su sha256, el minuto y el tema en una línea neutra, y la falta se dice.
>
> 8. Lo enseñado (D7). F10 y F11 dicen que el trader leyó «las 191 operaciones» y que comenta la fidelidad del bot y unos «Excel recalculados». Según Aleks (respuesta 1), la foto es parte del chat del trader con Gemini, y Aleks no leyó nada de esa parte para no tocar meses reservados. El informe y HOLDOUT lo declaran así: qué se le enseñó al trader queda SIN DETERMINAR; 191 coincide con el número de operaciones llenadas de la corrida (3) (ADR-0099 §8), y ADR-0098 §3 C pedía no enseñarle ninguna cifra de la medida; es una posible desviación que no se puede confirmar ni descartar. Lo mismo con las capturas del bot y los «Excel recalculados» si la respuesta 2 está vacía. No repites ninguna cifra que no sea el 191 que ya dijo él. La consecuencia la decide el ADR de ADR-0099 §7, no esta rama. Ningún ADR se toca por esto (D6 sigue siendo solo el recuadro de ADR-0100 §1).
>
> 9. Pregunta 4, la parte del consultor. Según el registro del consultor, el 2026-11-23 el consultor recibió de Aleks las respuestas escritas y un resumen de los audios en seis puntos hecho por esta sesión de Claude Code, no el texto del ASR. Y una exposición nueva, de hoy: el 2026-11-25 el consultor leyó, en las capturas de esta PARADA, las frases F1 a F14 del ASR. Va a la fila de HOLDOUT de hoy, antes del siguiente `make check`.
>
> 10. Después: aplicas D2 a D7, el recuadro de ADR-0100 §1 en su propio commit, el informe con las líneas propuestas para el cierre y la fila de ERRORES-RECURRENTES (con tu error del ScheduleWakeup y su lección: con un `make check` corriendo no se programa nada que escriba en `.claude/`; y el error del consultor del punto 0, que dio por buena una «validación» sin preguntar qué decía el audio). Luego el revisor con los alcances del encargo. Termina con «Rama lista para revisión, NO cerrada.»
>
> RESPUESTAS DE ALEKS:
> 1. La foto del «191»: «Eso es parte del chat de Gemini donde él metió varias cosas, y para no tocar meses reservados o algo, simplemente no leí NADA.»
> 2. Las capturas del bot y los «Excel recalculados»:
> 3. F1 a F14 escuchadas (cuáles confirmo y qué corrijo; la F5, «sin multiplicarlo» o «multiplicarlo»; cuáles de las cinco lecturas oigo así):
> 4. Lo que leí el día 23:
> 5. El audio de 0:14 «es solo un audio riéndose, no es necesario». Captura 3 y captura de la configuración de FX Replay:

### Cómo se aplica, punto por punto

| Punto | Hecho | Dónde |
|---|---|---|
| 0 | Aleks renombró las cuatro capturas con la orden `!`; sus sha256, vueltos a calcular con los nombres nuevos, son los de A1 (sin PARADA). El audio del 2026-11-24 no entra. La secuencia de las capturas 3 y 4, tal cual, con los dos hechos que pide | §6.1, §6.4 |
| 1 | `corpus inventory` en la rama: el diff es el del ensayo (11 entradas nuevas y el `resumen`), con la raíz sin cambiar; después `corpus check --hashes` | §6.9 |
| 2 | Amplía el párrafo de «Mensajes del trader» de `Material adicional de su operativa`, con la forma de la entrada del 2026-10-14 y las cautelas de D3; sin entrada propia | §6.7; `fuentes.yaml` |
| 3 | Ningún `fb-`; el apartamiento del paso 4 de `knowledge/feedback/README.md`:79-82, declarado; la precisión del README, a las líneas del cierre | §6.8, §8 |
| 4 | Q, V18, A-13 y `ev-v4-012524-0ef85a89`, solo por su id | §7 |
| 5 | Ninguna entrada nueva en la hoja de ruta; el «Qué es» de R4.7 | §8 |
| 6 | PROJECT_STATE no crece (la F propuesta lo baja 13 bytes); las guardias, la transcripción de audios sueltos y el README, a «Carril: guardias y deuda» | §8 |
| 7 | La respuesta 3 llegó vacía: **no entra ningún literal de audio**; por cada audio, el fichero, su sha256, los minutos y el tema en una línea neutra, y la falta se dice | §6.5 |
| 8 | Lo enseñado, SIN DETERMINAR, en el informe y en HOLDOUT; la respuesta 2, vacía, igual; ninguna cifra salvo el 191 | §6.6; HOLDOUT, fila 2 del 2026-11-25 |
| 9 | La parte del consultor del 2026-11-23 y su exposición de hoy (F1-F14), en la fila de HOLDOUT de hoy, escrita antes del siguiente `make check` | HOLDOUT, fila 2 del 2026-11-25 |
| 10 | D2 a D7; el recuadro de ADR-0100 §1 en su propio commit; las líneas del cierre y la fila de ERRORES-RECURRENTES; el revisor | §6 a §8; commit del recuadro; «Informe del revisor» |

## 6. Lo que entra

### 6.1 Por fichero

En `corpus/Estrategia del trader/Material adicional de su operativa/Mensajes del trader/` (fuera de
git) y en `knowledge/corpus/manifest.yaml`, con el papel `material_adicional`:

| Fichero | Bytes | sha256 |
|---|---|---|
| `mensaje-whatsapp-2026-11-23-0126-cinco-preguntas.png` | 391.604 | `65a2d71e9e223dd87d4c4edf68d754cb59881e220923b68ff7faca799306f4ca` |
| `mensaje-whatsapp-2026-11-23-0956-operativa-real.png` | 76.224 | `a635f76f3be4c89959822767268a6d8dfc3f115e801e68febe82fad7d9f7ef28` |
| `mensaje-whatsapp-2026-11-24-1718-propuesta-backtest-costes.png` | 168.123 | `33fa10d2728bb956951e5e283a9153ad37c4e74ac85fce8a6172fa6a7b139ed7` |
| `mensaje-whatsapp-2026-11-24-1719-meses-enero-julio-2024.png` | 318.435 | `f47da4e8ffb5b787e8a6c4ed81e56a1186577f5fae6f3a0de5ff98502e5d57dc` |
| `audio-whatsapp-2026-11-23-0959-caja-en-una-vela.ogg` | 421.749 | `151a23bbad3baefc6cca793ad951ec0a0ff33afafdf2906ec96f7e6f1cd92011` |
| `audio-whatsapp-2026-11-23-0959-protegido-en-0-80.ogg` | 38.026 | `b74803c54ee28f58236493294b88b9b7daf566c28f37991f42de2570f0ebaaea` |
| `audio-whatsapp-2026-11-23-1001-break-even-y-comision.ogg` | 120.403 | `d1986b2275db4fe2878d9831b990fb5e1b8b2063f7092de1c2b06cb62d7656f6` |
| `audio-whatsapp-2026-11-23-1002-calculo-del-break-even.ogg` | 38.510 | `2e6d6bba7fed1e00493b8d0355d5a2c49b94d759192d37fa2d7dc600afcb551c` |
| `audio-whatsapp-2026-11-23-1007-recalculo-y-reunion.ogg` | 351.319 | `22704d844fc9ca730e71b27109d0145ef04cc3e9bb39643e1752f9edb39ebade` |
| `audio-whatsapp-2026-11-23-1010-objetivo-y-191-operaciones.ogg` | 387.646 | `bb7121e34315d27b076dbe49ed6e0d775ffdeaef5e4ae7fc0113bf68f8198199` |
| `audio-whatsapp-2026-11-23-1013-fundednext-y-esquemas.ogg` | 273.451 | `2d93a892bb6bfa82c487b575ff282c665a563589f0a895ca64311422a9217056` |

**No entra:**
- el duplicado `WhatsApp Ptt 2026-11-23 at 9.59.43 AM (1).ogg`, sha256
  `b74803c54ee28f58236493294b88b9b7daf566c28f37991f42de2570f0ebaaea` (el mismo que el de la nota de
  las 09:59:43);
- la nota de voz de 0:14 del trader del 2026-11-24 a las 18:01: según Aleks, «es solo un audio
  riéndose, no es necesario» (respuesta 5); no se exporta ni se escucha;
- las ocho transcripciones del 2026-11-23, fuera del repo con los sha256 de §0.2 (D2): en `main`
  no hay nada que transcriba un audio suelto (auditor, 37);
- ninguna captura de la configuración de FX Replay: la respuesta 5 no trae ninguna, y la del
  2026-11-24 que se conoce trae un agregado de toda la cuenta con meses reservados (auditor, H3).

### 6.2 Las cinco preguntas (captura 1)

Literal del consultor (A1), de `mensaje-whatsapp-2026-11-23-0126-cinco-preguntas.png`, sha256
`65a2d71e9e223dd87d4c4edf68d754cb59881e220923b68ff7faca799306f4ca`. Mensaje de Aleks al trader, el
lunes 2026-11-23 a la 01:26 (hora de Lima). Una etiqueta de fecha tapa la palabra «Estamos», que se
lee en la cita de la captura 2.

> «Hola, ¿qué tal? Estamos ajustando el bot a las condiciones de una cuenta real (spread, comisión, ejecución) y para eso necesito saber cómo es tu operativa fuera del backtest. Son cinco preguntas cortas, puedes contestar con el número y la letra:
> 1. Esta misma estrategia de EURUSD, ¿la estás operando hoy en una cuenta real o de fondeo? a) Sí, y ya he cobrado retiros b) Sí, todavía sin retiros c) Ahora mismo solo en backtest. Si es a) o b), ¿desde cuándo más o menos? No necesito cifras.
> 2. ¿En qué firma o bróker es, y qué tipo de cuenta?
> 3. En esa cuenta, ¿haces exactamente lo mismo que en tus backtests de FX Replay (mismas sesiones, misma caja, mismo stop y mismo objetivo)? a) Igual b) Cambio algo: ¿qué?
> 4. Los resultados de tus backtests en FX Replay, ¿llevan ya descontados el spread y la comisión? a) Los dos b) Solo el spread c) Ninguno d) No lo sé
> 5. Más adelante, ¿podrías pasarme el historial exportado de esa cuenta (el archivo que da la plataforma, no capturas) de unas semanas? No lo mandes todavía: yo te digo de qué fechas.
> Estas van primero. Las otras que te mandé (las de M15 y las del PDF) pueden esperar a que tengas un rato. ¡Gracias!»

### 6.3 Las respuestas escritas del trader (captura 2)

Literal del consultor (A1), de `mensaje-whatsapp-2026-11-23-0956-operativa-real.png`, sha256
`a635f76f3be4c89959822767268a6d8dfc3f115e801e68febe82fad7d9f7ef28`. Respuesta del trader del
2026-11-23 a las 09:56, citando la captura 1.

> «1-c
> 2-foundnext
> 3-si, todo igual
> 4-no se trabajo con spreads o comisión
> 5-las de fx replays que las envíe, ya no lo puedo enviar porque ya no tengo abiertas esas sesiones de backtest, pero están en el grupo los excels»

### 6.4 La petición escrita de los meses del backtest con costes (D4)

La secuencia de las capturas 3 y 4, con sus horas (hora de Lima) y los literales del consultor
(A1). El día de la captura 3 sale del «Ayer» de la captura 4, tomada el 2026-11-25; Aleks no lo ha
confirmado (la segunda parte de su respuesta 5 llegó vacía).

1. **2026-11-24, 17:18, Aleks** (`mensaje-whatsapp-2026-11-24-1718-propuesta-backtest-costes.png`,
   sha256 `33fa10d2728bb956951e5e283a9153ad37c4e74ac85fce8a6172fa6a7b139ed7`):

   > «Te propongo algo que nos va a sacar de dudas a los dos: un backtest de dos meses que no hayas hecho nunca, con los costes reales puestos. Serían junio y noviembre de 2024 (si ya hiciste alguno, dime y elegimos otro de la misma época del año).
   > Cómo:
   > 1. Operas exactamente igual que siempre: mismas cajas, mismo 0,8, mismo objetivo y mismo break even. No cambies nada por saber que hay costes.
   > 2. En FX Replay: datos de OANDA como siempre, spread de 0,2 pips, comisión de 5 USD por lote ida y vuelta (2,5 por lado si te lo pide así) y el lote calculado para arriesgar el 0,5 % en cada operación.
   > 3. Grábalo en vídeo con tu voz, como hiciste con julio, todas las sesiones enteras.
   > 4. Al terminar cada mes me mandas el CSV completo y los vídeos. No hace falta que calcules nada, los números los saco yo.
   > Antes de empezar, confírmame que FX Replay te deja poner el spread y la comisión así, y qué dos meses vas a hacer.»

2. Lo que sigue, de `mensaje-whatsapp-2026-11-24-1719-meses-enero-julio-2024.png`, sha256
   `f47da4e8ffb5b787e8a6c4ed81e56a1186577f5fae6f3a0de5ff98502e5d57dc`:
   - **17:19, el trader**, citando la captura 3, **acepta por escrito junio y noviembre de 2024**:
     «Entonces queda junio y noviembre 2024».
   - **17:20, Aleks:** «si bro».
   - **18:00, Aleks**, **pide por escrito enero y julio de 2024 si aún no había arrancado**: «Una
     cosa: si todavía no arrancaste el backtest, mejor hazlo de enero y julio de 2024 en vez de junio
     y noviembre. Si ya empezaste, sigue con esos, no pasa nada. Lo demás igual: spread 0,2, comisión
     5 USD por lote, lote al 0,5 %, grabando con tu voz y exportando el libro completo. ¡Gracias!»
   - **18:01, el trader:** **no contesta por escrito a eso**; solo manda una nota de voz de 0:14
     que, según Aleks, es una risa (respuesta 5), y que no entra.
   - **18:02, Aleks:** «esos si son definitivos xd».

   La captura trae además mensajes que no se registran ni se interpretan (dos de Aleks a las 18:00,
   una risa del trader a las 18:01 y un «dale bro» de Aleks a las 18:02), como en el precedente del
   2026-10-14.

**Dos hechos, sin juzgar ADR-0100 §2** (D4, A3 y punto 0 de la respuesta):
- la petición de enero y julio no repite la pregunta de si ya los había hecho, que solo estaba en
  la captura 3, para junio y noviembre;
- ninguna captura recoge que el trader no haya operado nunca enero ni julio de 2024.

**La configuración**, como la pedida (A3): datos de OANDA (solo en la captura 3), spread de 0,2
pips, comisión de 5 USD por lote de ida y vuelta, lote para arriesgar el 0,5 % en cada operación,
las sesiones grabadas en vídeo con su voz y el libro completo exportado (el CSV en la captura 3, «el
libro completo» en la de las 18:00). El apalancamiento 1:30 y el deslizamiento apagado no salen en
ninguna captura y no se escriben como parte de la petición. Si cumple ADR-0100 §2 («uno de cada
mitad», «que no haya operado nunca», «por escrito») lo decide la rama de entrada del backtest.

Corrección del consultor (punto 0): A2 y A3 decían que el trader «valida» los meses en la nota de
voz; según Aleks, es una risa.

### 6.5 Los audios (D2; punto 7 de la respuesta)

**La respuesta 3 de Aleks llegó vacía: nadie ha comprobado escuchándola ninguna frase de los
audios, y no entra ningún literal de audio.** Ni el texto del ASR ni las lecturas de la sesión
sobre él. Por cada audio, una línea neutra:

| Fichero | sha256 | Minutos (inicio del segmento del ASR) | Tema |
|---|---|---|---|
| `audio-whatsapp-2026-11-23-0959-caja-en-una-vela.ogg` | `151a23bbad3baefc6cca793ad951ec0a0ff33afafdf2906ec96f7e6f1cd92011` | 00:00-00:36; 02:03-02:42 | cómo traza el bot la caja frente a los esquemas de entrada; desde dónde se calcula el objetivo |
| `audio-whatsapp-2026-11-23-0959-protegido-en-0-80.ogg` | `b74803c54ee28f58236493294b88b9b7daf566c28f37991f42de2570f0ebaaea` | 00:01 | la referencia del objetivo y la protección en el 0,8 |
| `audio-whatsapp-2026-11-23-1001-break-even-y-comision.ogg` | `d1986b2275db4fe2878d9831b990fb5e1b8b2063f7092de1c2b06cb62d7656f6` | 00:23-00:36 | el break even y la comisión |
| `audio-whatsapp-2026-11-23-1002-calculo-del-break-even.ogg` | `2e6d6bba7fed1e00493b8d0355d5a2c49b94d759192d37fa2d7dc600afcb551c` | 00:00 | cómo se calcula el coste del break even |
| `audio-whatsapp-2026-11-23-1007-recalculo-y-reunion.ogg` | `22704d844fc9ca730e71b27109d0145ef04cc3e9bb39643e1752f9edb39ebade` | 00:00-00:07; 01:27-01:36; 01:54-02:09 | recalcular sus operaciones con costes; el trazado de la caja; una reunión |
| `audio-whatsapp-2026-11-23-1010-objetivo-y-191-operaciones.ogg` | `bb7121e34315d27b076dbe49ed6e0d775ffdeaef5e4ae7fc0113bf68f8198199` | 00:28-00:34; 00:55-01:10; 01:52-01:59; 02:07 | el objetivo; una gestión posible; lo que leyó (§6.6) |
| `audio-whatsapp-2026-11-23-1013-fundednext-y-esquemas.ogg` | `2d93a892bb6bfa82c487b575ff282c665a563589f0a895ca64311422a9217056` | 00:17-00:32; 01:15-01:40 | operaciones en FundedNext; qué es cada esquema de entrada |

Lo que la expectativa (b) del encargo pedía —decir literal si la voz
dice la distancia 0-1 o «el stop»— **queda sin literal**: solo el ASR, sin comprobar, la nombraría,
y eso no entra (punto 7).

### 6.6 Lo que se le enseñó al trader (D7; punto 8 de la respuesta)

**SIN DETERMINAR.** En el audio de las 10:10, según el ASR, el trader dice haber leído «las 191
operaciones» y habla de la fidelidad del bot y de unos «Excel recalculados». Según Aleks (respuesta
1), la foto «es parte del chat de Gemini donde él metió varias cosas», y Aleks no leyó nada de esa
parte para no tocar meses reservados. 191 coincide con el número de operaciones llenadas de la
corrida (3) (ADR-0099 §8), y ADR-0098 §3 C pedía el contraste sin enseñarle ninguna cifra de esa
medida: **es una posible desviación de ADR-0098 §3 C que no se puede confirmar ni descartar.** Lo
mismo con las capturas de operaciones del bot y los «Excel recalculados» (la respuesta 2 de Aleks
llegó vacía). Ninguna otra cifra se repite aquí. La consecuencia la decide el ADR de ADR-0099 §7, no
esta rama, y ningún ADR se toca por esto. Declarado en la fila 2 del 2026-11-25 de
`HOLDOUT-EXPOSICIONES.md`.

### 6.7 Las cautelas (D3), en `fuentes.yaml`

El párrafo de «Mensajes del trader» de `Material adicional de su operativa` se amplía (sin entrada
propia, punto 2) con lo que entra y su fecha, que es el contraste de ADR-0099 §6, que por primera
vez trae audios, lo que no entra, y las cautelas: ningún nombre ni número del trader, ni el del
grupo ni de sus miembros, entra al repo; las capturas no las abre la sesión (ADR-0038); el trader
dice que ha operado algunas operaciones en FundedNext y que las compartió en el grupo: no se piden
ni se abren, y si llega un historial, entra SIN ABRIR y un ADR fija antes quién lo lee (ADR-0099 §6,
con ADR-0072 como precedente); y lo que se le mostró al trader, sin determinar.

### 6.8 Ningún registro de feedback (D1; punto 3 de la respuesta)

Ningún `fb-` en esta rama. **Se aparta del paso 4 de `knowledge/feedback/README.md`:79-82** («Si
trae una respuesta, registro de feedback»), por tres motivos: las respuestas no tienen objetivo en
el esquema (la premisa y el coste de FX Replay no son un `evidence`, una `regla`, un `parametro`,
una `ambiguedad`, un `caso` ni una `contradiccion`, `feedback/modelo.py`:53-61; y no hay acción de
nota, :37-51); nada se cierra (ninguna ambigüedad cambia de estado); y un CONFIRM sobre el objetivo
o el stop escondería A-56, la diferencia entre la regla dicha y su registro, que es una medición
(ADR-0073 §3). Además, sin literal de audio comprobado, un registro citaría un ASR hecho fuera de
rama. El README no se toca aquí; su precisión va a las líneas del cierre (§8).

### 6.9 El inventario en la rama (punto 1 de la respuesta)

`uv run botsito corpus inventory`, con el log fuera del repo: exit 0, «OK: manifiesto escrito ·
heredado_v2: 477 ficheros, 117,626,282 bytes · material_adicional: 84 ficheros, 9,436,152 bytes ·
video_original: 21 ficheros, 98,507,386,788 bytes», 0 `AVISO`. `git diff --stat` de
`knowledge/corpus/manifest.yaml`: 46 inserciones y 2 borrados, que son **11 entradas nuevas** (4
líneas cada una, con las rutas y los sha256 de §6.1) y **el `resumen.material_adicional`**
(`ficheros` 73 → 84, `bytes` 6.850.662 → 9.436.152). La línea `raiz:` no cambia, y ninguna otra
tampoco: es el diff del ensayo de §0.3 con los nombres de A5. Después,
`uv run botsito corpus check --hashes`: «OK: el corpus coincide con el manifiesto (hashes)», exit 0, con el log fuera del repo.

### 6.10 El recuadro de ADR-0100 §1 (D6)

En su propio commit, con el cuerpo intacto, junto a la frase que corrige (ADR-0100:31-32, «su
respuesta entra con su `fb-` por su propia rama, ADR-0099 §6»): esa respuesta no tiene objetivo de
`fb-` en el esquema y entra por `CONTRASTE-TRADER.md`. Ningún otro ADR se toca.

## 7. Lo que va a la preparación de la sesión siguiente (R4.6) y al ADR de C

Sin leerlo contra la premisa ni contra ninguna cifra (D5); los temas de audio, sin literal (§6.5).

**Para preparar la sesión siguiente (R4.6):**
- El tema de la caja trazada sobre una sola vela frente al esquema 1 o 2, y qué es cada esquema
  (audios de las 09:59, 10:07 y 10:13): material para A-48 y para S-3 (`ACTIVAR-SESION-08.md`:55),
  que no se cierran. Si se le pregunta, con su forma de pregunta y sin ninguna medida (ADR-0073 §3).
- Siguen pendientes, como dice la captura 1, «las de M15 y las del PDF»: A-35, A-43 y S-3 (WhatsApp
  del 2026-11-21, `ACTIVAR-SESION-08.md`:368). Nada de este material responde a A-35, y su línea de
  Technical Debt sigue; tampoco a A-43 ni a A-58.

**Para el ADR de Aleks de ADR-0099 §7 (la salida C):**
- Las respuestas escritas de la captura 2 (§6.3), tal cual.
- Que, según el ASR sin comprobar, el trader dice haber operado algunas operaciones en FundedNext
  (audio de las 10:13); lo que ya trae el corpus sobre FundedNext es `ev-v4-012524-0ef85a89`. La
  captura 2 dice «1-c» (ahora mismo solo en backtest); las dos cosas, sin conciliar.
- La respuesta 4 de la captura 2, que cita ADR-0100 §1.
- La respuesta 5 de la captura 2 toca la Q de la Next Action; no la cierra.
- Lo que dice del break even y la comisión (audios de las 10:01 y 10:02): V18 de
  `AUDITORIA-CAZADOR-2026-11-23.md` y A-13, sin tocar ninguna.
- Lo que dice del objetivo y la protección en el 0,8 (audios de las 09:59 y 10:10), sin literal:
  A-56, que es una medición.
- Que dice que recalculará sus operaciones con comisión y lotaje (audio de las 10:07).
- Lo que se le enseñó, SIN DETERMINAR (§6.6), y su posible desviación de ADR-0098 §3 C.
- La secuencia de la petición de los meses (§6.4), para la rama de entrada del backtest.

## 8. Las líneas propuestas para el cierre

Ninguna hace crecer `PROJECT_STATE.md` (punto 6). Las cifras de tamaño, medidas con un guion de la
carpeta de trabajo sobre `git show main:PROJECT_STATE.md`.

- **La F** (`PROJECT_STATE.md`:28): «F17 (ADR-0099 §5), el contraste con el trader (ADR-0099 §6) y
  el backtest del trader con costes (ADR-0100, R4.10), pendientes; el diagnóstico de la premisa,
  hecho.» pasa a «F17 (ADR-0099 §5) y el backtest del trader con costes (ADR-0100, R4.10),
  pendientes; el diagnóstico de la premisa y el contraste con el trader, hechos.» Con eso, y
  `Current Branch` y `Current Feature` de vuelta a `main`, PROJECT_STATE queda en **24.837 bytes**
  (24.850 en `main`, −13; el tope, 25.000).
- **La hoja de ruta, R4.7**, sin entrada nueva (punto 5): en su «Qué es», tras «el contraste de la
  premisa con el trader (ADR-0099 §6)», añadir «(hecho, CONTRASTE-TRADER.md: lo dicho y lo pedido
  entran sin `fb-`; lo que se le enseñó, sin determinar)». La entrada sigue ABIERTA.
- **La hoja de ruta, «Carril: guardias y deuda»**, una entrada nueva, G.9:

  ```
  ### G.9 · Lo que esta rama no pudo hacer con las herramientas de main
  - **Refs:** —
  - **Qué es:** cuatro cosas de trabajo/contraste-trader (CONTRASTE-TRADER.md §0.2, §0.4 y §6.8). La guardia negó tres medidas legítimas: `ffprobe` sobre un `.ogg` (solo admite contenedores de vídeo), un guion de recuento ciego de la carpeta de trabajo sobre unas transcripciones de fuera del repo, y el `mv` que renombra una captura de «Mensajes del trader» sin abrirla (lo hizo Aleks). En `main` no hay nada que transcriba un audio suelto (`transcribir_sesion.py` exige el vídeo de una sesión): la transcripción de los audios del 2026-11-23 queda fuera del repo, nombrada por su sha256. Y el paso 4 de `knowledge/feedback/README.md` dice «Si trae una respuesta, registro de feedback», cuando debería decir «si trae una respuesta a un objetivo del esquema».
  - **Depende de:** nada; no adelanta el camino crítico.
  - **Quién:** la sesión, con el encargo del consultor.
  - **Hecho cuando:** las tres formas admitidas por la guardia con su test que las rompe a propósito (o descartadas por escrito), un camino de `main` que transcribe un audio suelto con cuarentena, y el README precisado.
  ```

- **Technical Debt de PROJECT_STATE:** nada (punto 6: va a G.9).
- **La fila de ERRORES-RECURRENTES**, con sus cuatro columnas, en §9 tras el revisor.

## Informe del auditor (subagente `auditor-encargo`, 2026-11-25), tal cual

Copiado tal cual, con sus títulos bajados dos niveles para que no partan este informe. Sus números
de línea de HOLDOUT, PROJECT_STATE y HISTORIA son los del árbol de la apertura.

#### Auditoría del encargo · trabajo/contraste-trader · 2026-11-25

**Resumen:** 46 afirmaciones: 28 correctas, 3 incorrectas, 15 con matiz. Hay 7 herencias que el encargo no recoge.

He trabajado solo leyendo. No he ejecutado `make`, tests, `gh` ni ningún comando que escriba. No he leído la carpeta de audios del Escritorio ni nada protegido. La guardia negó dos comandos míos de solo lectura (un `grep` sin ruta y una asignación de variable). No los rodeé: los rehíce con Grep y Glob.

##### Afirmaciones

| # | Afirmación (literal del encargo) | Veredicto | Evidencia |
|---|---|---|---|
| 1 | «Base: `main` en `6c113d16` … el merge `42fdb0b5` lleva el tag `stable/F39n-diagnostico-premisa` … sin ninguna otra rama» | CORRECTA | `git rev-parse` da `main` = `origin/main` = 6c113d16, y el tag^{commit} = 42fdb0b5. `git branch -a` solo muestra main, la rama de trabajo y origin/main. |
| 2 | «CI de main 45670800735 en verde según ese cierre» | MATIZ | Ese id no aparece en el registro de cierre de F39n. HISTORIA (main):21258-21261 cita los runs 45536934319 y 45543215639 de `fix/` y el 45490418025 de main al abrir. El 45670800735 lo midió la propia sesión: CONTRASTE-TRADER.md:20. Yo no lo puedo comprobar (no uso `gh`). |
| 3 | «tag al cerrar: `stable/F39o-contraste-trader` … el último tag es F39n» | CORRECTA | `git tag --list "stable/F39*"` termina en F39n y no hay ningún F39o. |
| 4 | «Contrato: tramo R4 (R4.7)» | CORRECTA | contrato.yaml:4. El `## R4` está en HOJA-DE-RUTA.md:330 y el `### R4.7`, con `Refs: NA:F`, en :437-438. `scripts/contrato_rama.py:129-152` acepta el tramo por su id. |
| 5 | La lista blanca (encargo, contrato, informe, HOLDOUT, `fuentes.yaml`, `manifest.yaml`, ADR-0100) y «ningún ADR nuevo» | CORRECTA | contrato.yaml:5-13 añade HISTORIA y PROJECT_STATE para la apertura. contrato.yaml:40-43 protege `00*`, README, `0101-*` y `0102-*`. CONTRATO-DE-RAMA.md:28 dice que el contrato se permite siempre a sí mismo. |
| 6 | §2: «`PROJECT_STATE.md` (salvo el Archivo de la apertura)» | MATIZ (menor) | El Archivo 83 vive en HISTORIA (staged, :21274). En PROJECT_STATE la apertura cambia Current Branch, Current Feature y las dos líneas «ninguna desde el Archivo 83» (`git diff --cached PROJECT_STATE.md`). |
| 7 | «la fila de HOLDOUT-EXPOSICIONES del día va ANTES del primer `make check`» | CORRECTA | CLAUDE.md, la guardia G2. Hay fila staged en HOLDOUT:193. |
| 8 | «el recuadro del ADR va en un commit propio … nunca en el `chore(cierre)`» | CORRECTA | Precedente en HISTORIA (main):21228-21231: el commit `47d2540d`. |
| 9 | «el contraste con el trader que ADR-0099 §6 manda hacer en su propia rama» | CORRECTA | 0099:186-188, «entran por su propia rama, con su `fb-` donde toque». |
| 10 | «el ADR de Aleks de ADR-0099 §7 (como tarde … hacia el 2026-12-03)» | CORRECTA | 0099:194-195 |
| 11 | ADR-0100 §2: «los que Aleks le pidió por escrito, o los que él declare por escrito antes de empezar» | CORRECTA | 0100:55-56 |
| 12 | «Las capturas no las abres (ADR-0038; la guardia lo impide)» | MATIZ | ADR-0038 §3 prohíbe en bloque las capturas de Analytics y da el motivo (0038:26-28). Que no se abra ninguna imagen del material adicional lo extiende la guardia (guardia.py:19) y la práctica de fuentes.yaml:357-358. Es coherente con ese motivo y no lo contradice. |
| 13 | (a) «las cinco preguntas … no están en el repo» | CORRECTA | `git grep "ajustando el bot a las condiciones" main` da 0 resultados. |
| 14 | (c) «191 es el número de operaciones llenadas de la corrida (3), las del techo de −0,239 R (ADR-0099 §8; RECORRIDA-CONSTRUCCION-3.md §4)» | CORRECTA, con un matiz | 0099:207-208 y RECORRIDA-CONSTRUCCION-3.md:685-686 y :720. Ningún informe posterior cambia la cifra. Pero 191 se publica también en PUENTE-TECHO.md:464 (`base`), DIAGNOSTICO-PREMISA.md:223 y :417, y AUDITORIA-CAZADOR-2026-11-23.md:41, :50, :90 y :103 («79 de 191»). La foto pudo salir de cualquiera de ellos, y eso cuenta para D7. |
| 15 | ADR-0098 §3 C pedía el contraste «sin enseñarle ninguna cifra de esta medida» | CORRECTA | 0098:148-149 |
| 16 | (d) la configuración incluía «apalancamiento 1:30 y deslizamiento apagado» | INCORRECTA (A3 ya lo corrige) | ADR-0100 §2 (0100:69-74) no los nombra. |
| 17 | 0.1: las filas del 2026-11-23 y del 2026-11-24 «dicen que no leyeron esos mensajes ni audios» | CORRECTA | HOLDOUT:189 y :190 («ningún mensaje ni audio del trader»), :191 («ni sus mensajes o audios del 2026-11-23») y :192. |
| 18 | «ADR-0099 §8 dice que las vieron y ninguna fila lo declara» | CORRECTA | 0099:203 y :221-222. En el HOLDOUT de main, el recuento de «cinco preguntas», «audios del trader» y «respuestas … del 2026-11-23» es 0. |
| 19 | «Precedente … la de `trabajo/sesion-08` del 2026-11-21 que cubre el 2026-11-20» | CORRECTA | HOLDOUT:172: «(1) **Escrita tarde para el 2026-11-20 (v20)**». |
| 20 | 0.2: el vídeo de mapeo y el backtest de diciembre de 2025 «siguen fuera de `corpus/`» | CORRECTA (como estado declarado) | PROJECT_STATE:28 y :36 dicen «fuera del repo». Lo tiene que medir la sesión. |
| 21 | 0.2: los audios, «también formato y duración, si se pueden medir sin que la guardia lo niegue» | MATIZ | La guardia solo deja pasar `ffprobe` sobre contenedores de vídeo (.mp4, .mov, .mkv o .webm) con sus bytes mágicos (guardia.py:3876, :4013-4022 y :4087-4092). Un audio de WhatsApp (.opus, .ogg o .m4a) se negará. `corpus inventory` tampoco mide la duración de un fichero que no es vídeo (inventario.py:274-291). |
| 22 | 0.3: si `corpus inventory` «acepta los audios y las capturas nuevas en esa subcarpeta» | CORRECTA (por el código) | Clasifica por el prefijo de la carpeta (inventario.py:195-202), recorre todo el disco (:279), solo pasa `ffprobe` a los vídeos de fuentes.yaml (:248-273) y `material_adicional` es un papel válido (:24, :389-392). |
| 23 | 0.3: «el diff de `knowledge/corpus/manifest.yaml` son solo las entradas nuevas» | MATIZ | Cambia por fuerza también `resumen.material_adicional` (ficheros y bytes; inventario.py:306-314). Y cambia `ffprobe:` (:318) si la versión instalada es otra. Si no se dice, el PARA de 0.3 y el alcance del revisor saltarían en falso. |
| 24 | 0.3: el inventario «medido en un clon desechable» | MATIZ (el encargo no dice cómo) | Ver la herencia H1: un `git worktree` no tiene `corpus/` y el comando falla antes de medir nada. |
| 25 | 0.4: `scripts/barrido_dias.py` «pide una filtrada con líneas `[mm:ss] texto`» | CORRECTA, con un matiz | barrido_dias.py:4 y :34. Solo detecta enteros sueltos de 18 a 31 (:5-9, :42-55). No ve nombres de mes ni resultados, y deja el resto de la línea a la vista. Para «meses fuera de construcción» y «resultados» hace falta el recuento a mano igualmente. |
| 26 | 0.5: A-35 en Technical Debt, «va al trader por WhatsApp con el esquema del PDF y entra por «Mensajes del trader»» | CORRECTA | PROJECT_STATE:136 |
| 27 | «ACTIVAR-SESION-08.md:368» (A-35, A-43, S-3) | CORRECTA | Es la línea exacta. S-3 es A-48 en la 7b: ACTIVAR-SESION-08.md:55. |
| 28 | A-43, A-48 y A-58, pendientes | CORRECTA | Las tres están ABIERTAS: PROJECT_STATE:67, :68 y :73. |
| 29 | «los parámetros de hoy: `objetivo_rr`, `base_calculo_objetivo` y `stop_fraccion_caja`» | CORRECTA, con un matiz | parametros.yaml:1105 (valor 3), :1759 y :1782 (`caja_completa`, la distancia del 0 al 1) y :662-671 (0,8). Nada lo describe como «stop protegido»: el stop «se escribe EN la orden limite y no se mueve despues». |
| 30 | «ADR-0100 §1 describe su forma de operar como «objetivo a 3 veces el stop»» | CORRECTA, con un matiz | El literal está en 0100:25. Pero describe la variante `todo_junto`, la del registro, frente a la regla dictada, que es «objetivo a 3 veces la caja» (0099:29). Esa diferencia es A-56. |
| 31 | 0.5: si un audio o una captura es material de un mes que no es de construcción, «entraría en `meses_reservados.yaml` el mismo día (MIRAR-EL-MATERIAL.md)» | CORRECTA | MIRAR-EL-MATERIAL.md:118-128, que ya excluye los meses de 2024 de ADR-0100. |
| 32 | D1 (i): «como en `trabajo/activar-sesion-08`, que no creó ninguno» | CORRECTA | `git diff --name-status stable/F39k…^1 stable/F39k… -- knowledge/feedback` da 0 líneas (también para F39j). |
| 33 | D1 (ii): «la premisa y el coste de FX Replay no tienen objetivo en el esquema, y el feedback no tiene acción de nota (feedback/modelo.py:37-51)» | CORRECTA, con un matiz | Las líneas :37-51 son `ACCIONES`: es cierto que no hay acción de nota. Lo que dice qué objetivos existen está en `TIPOS_OBJETIVO`, :53-61, y en `OBJETIVOS_POR_ACCION`, :63-76. Ojo: `firma`, con opciones `[ftmo, fundednext]` (parametros.yaml:1857-1866), es la firma del bot (ADR-0026), de categoría `prop_firm`; no sirve de objetivo para el «2-foundnext». Además, knowledge/feedback/README.md:79-82 manda «Si trae una respuesta, registro de feedback»: D1 se aparta de ese procedimiento escrito y el informe debería decirlo así. |
| 34 | D1 (iii): A-56 es «una medición (A-56, ADR-0073 §3)» | CORRECTA | 0073:47-50: «una medición nunca va al trader». |
| 35 | D1 (iv): «con un audio suelto el validador no comprueba `t1` contra la duración (solo los vídeos del manifiesto la tienen)» | CORRECTA | validation/knowledge.py:77-88 (las duraciones solo salen de `videos`) y feedback/modelo.py:435-444. Un audio tampoco se puede registrar como vídeo en fuentes.yaml: `ffprobe_info` exige pista de vídeo (inventario.py:178-180). |
| 36 | D2: literales del consultor con sha256 «como en `fb-2026-10-04-sesion-04-d2e84172`» | CORRECTA | Ese registro lleva el sha256 de la captura en `registrado_por` (:11-12). |
| 37 | D2: «no hay en `main` nada que transcriba un audio suelto» | MATIZ (en efecto, correcta) | `scripts/transcribir_sesion.py` sí toma `--audio`, pero exige el `--video` de una sesión y, si no, no escribe nada (:37-41, :49-51). `corpus transcribe --video` solo admite vídeos de fuentes.yaml (cli.py:3158-3159). |
| 38 | D3: «`fuentes.yaml` amplía la subcarpeta «Mensajes del trader», cuya descripción hoy solo habla de capturas escritas» | INCORRECTA | (1) No tiene entrada propia: en `carpetas` solo hay `_procesado`, `Material adicional de su operativa` y `Sesiones` (fuentes.yaml:324-395). «Mensajes del trader» es un párrafo de la descripción de la segunda (:348-388). (2) Ese párrafo no habla solo de capturas escritas: ya recoge dos gráficos H4 del trader (:353-354), dos esquemas del consultor (:366-368) y una nota de voz de 0:21 que Aleks escuchó y que no se registró (:373-375). |
| 39 | D3: «por primera vez trae audios» | CORRECTA (como ficheros) | En manifest.yaml, 0 audios bajo `Mensajes del trader/`. Los únicos audios del corpus son 5 mp3 de `_procesado`. |
| 40 | D3: si llega un historial, entra «SIN ABRIR y un ADR fija antes quién lo lee (ADR-0099 §6, con ADR-0072 como precedente)» | CORRECTA | 0099:188-190 |
| 41 | D6: la frase de ADR-0100 §1 «su respuesta entra con su `fb-` por su propia rama» | CORRECTA, con un matiz | Está en 0100:31-32. ADR-0099 §6 dice «donde toque» (0099:187-188), que es compatible con D1: solo ADR-0100 necesita el recuadro, como dice D6. |
| 42 | §7: PROJECT_STATE «está en 24.850 bytes de 25.000» | CORRECTA, con un matiz | `git show main:PROJECT_STATE.md \| wc -c` da 24850; el tope está en test_project_state.py:21. En la rama ya son 24.922. HISTORIA (main):21240 publica 24.946, pero es del `chore(cierre)`, anterior al `docs(state)`. Y «sin que crezca» choca con añadir la línea de Technical Debt de D2: la F pierde unos 45 bytes y la línea nueva suma más, con 150 bytes de margen. Hay que medirlo; el precedente para lo que no cabe es «Pendiente que no cabe en PROJECT_STATE» (HISTORIA:21268-21270). |
| 43 | §7: la F, donde sale «el contraste con el trader (ADR-0099 §6)» | CORRECTA | El literal está en PROJECT_STATE:28. |
| 44 | §7: «la fila de ERRORES-RECURRENTES preparada con sus cuatro columnas» | CORRECTA | ERRORES-RECURRENTES.md:50-51 |
| 45 | A1 frente a A5: «el consultor se las devolvió con estos nombres para que las guarde tal cual» frente a «Aleks las guardó con el nombre de Windows» | MATIZ | Se contradicen dentro del propio añadido; manda A5, que es posterior. El lunes 2026-11-23 es correcto (`date -d` da Monday). |
| 46 | A5: «renombrar no abre la imagen» | MATIZ | Es cierto, pero la guardia mira el origen de `mv` como una lectura (guardia.py:2039-2046) y niega toda imagen del material adicional (:19), así que el renombrado se negará. El precedente es que renombra Aleks (fuentes.yaml:387-388). El encargo ya prevé que lo haga él. |

##### Lo que el repo pide y el encargo no recoge

| # | Qué | Dónde lo pide | Evidencia |
|---|---|---|---|
| H1 | **Cómo encuentra `corpus/` el ensayo en el clon.** `corpus/` está ignorado y un worktree no lo tiene, así que el comando falla con «no existe la raiz del corpus». La raíz sale de fuentes.yaml (`corpus/Estrategia del trader`, relativa) y `--repo` solo cambia la raíz del repo. La unión de `corpus/` es lo que rompió la guardia el 2026-11-20, y la guardia ya negó un `mklink`. Si se pone una raíz absoluta en el fuentes.yaml del clon, el diff trae también la línea `raiz:`. Los precedentes (ACTIVACION-A42, SESGO-H4-COLOR, ENTRADA-JULIO) corrieron el inventario sobre el repo real y comprobaron el diff. **Propongo** que el consultor elija entre (a) el repo real, con el diff de `manifest.yaml` (está en `rutas_permitidas`) y el PARA de 0.3, o (b) el clon con `raiz` absoluta y esa línea declarada. El comando escribe el manifiesto aunque dé AVISO (cli.py:205-216): hay que mirar el código de salida. | CLAUDE.md, «Ensayos aislados» 1; encargo 0.3 | inventario.py:242-245; fuentes.yaml:6; cli.py:3136; HISTORIA:19808 (GUARDIAS-HOLDOUT.md §17); CIERRES-DE-MERCADO.md:374; ENTRADA-JULIO.md:268-272 y :480-485 |
| H2 | **`corpus check --hashes` después del inventario.** Es la pareja habitual de `corpus inventory` y `make check` no la ejecuta. | encargos de sesion-05:50 y :91, sesion-06:36, sesion-07:40 y sesion-08:51 | Makefile:68-70 y :82 (`check` no incluye `corpus`) |
| H3 | **La captura de configuración de FX Replay que ya existe trae agregados de meses reservados.** Es la del 2026-11-24: detrás se ve el panel de cuenta, «Backtesting, Lifetime». Por (d) no puede entrar, y A3 abre la puerta a «una captura de la configuración … sin ningún resultado» sin nombrarla. El encargo debería decir que esa no entra. | ADR-0100 §7 (recuadro); encargo (d) | 0100:200; HOLDOUT:191, punto (9) |
| H4 | **La Q de la Next Action (la exportación de agosto).** La respuesta 5 de la captura 2 («ya no lo puedo enviar porque ya no tengo abiertas esas sesiones de backtest, pero están en el grupo los excels») toca la Q. La auditoría profunda dice que el contraste era la ocasión de volver a pedirla. La tabla de 0.5 no la nombra. | PROJECT_STATE:42 (Q); AUDITORIA-PROFUNDA-2026-11.md:1271 (R-14) | — |
| H5 | **La expectativa (c), «el break even solo cuesta la comisión».** El encargo la trata como opinión, pero la auditoría «cazador» tiene V18 («Break even neto de costes … Pregunta al trader, no una palanca») y A-13 (break even) está ABIERTA. 0.5 debería decir si responde a V18 o a A-13, sin cambiar ninguna. | AUDITORIA-CAZADOR-2026-11-23.md:194; PROJECT_STATE:64 | — |
| H6 | **El tramo.** R4.7 es una entrada paraguas. Su «Depende de» («una prueba gratuita de FTMO viva para F17», HOJA:440) no está HECHO, pero es de F17, no del contraste. El contraste no tiene entrada propia (R-12 de la auditoría profunda), mientras que el puente y la premisa la tuvieron (R4.8 a R4.10). El contraste no se adelanta: la F lo da como pendiente y el orden lo fija el consultor (PROJECT_STATE:23 y :28). Las líneas del cierre deberían decir si sale una entrada nueva o si R4.7 lo apunta en su «Qué es». | HOJA:437-467; AUDITORIA-PROFUNDA:1345 | — |
| H7 | **Lo que el corpus ya trae de FundedNext.** `ev-v4-012524-0ef85a89` («La idea creo que sería Funded Next…», v4 1:25:24) y la deuda de RN-029 a RN-032, que lo citan de relleno. La «D» de 0.5 debería nombrarlo, sin leerlo contra nada (D5). | Technical Debt «buscar en el corpus antes» (PROJECT_STATE:124 y :114) | knowledge/evidence/v4/ev-v4-012524-0ef85a89.yaml |

Además, como lección y no como herencia: ERRORES-RECURRENTES.md:86 recoge un fallo de `trabajo/sesgo-h4-color`, «la nota de voz situada en la captura equivocada». A1 sitúa la nota de 0:14 en la captura 4: conviene que Aleks lo confirme en la PARADA.

##### Comandos del encargo

| # | Comando | Existe y se ejecuta así | Evidencia |
|---|---|---|---|
| C1 | `uv run botsito corpus inventory` | Sí, sin opciones. Su única opción es `--sin-hash`, que no debe usarse: ese manifiesto no pasa `knowledge validate`. Para apuntar a otra raíz, `--repo` va antes del subcomando: `uv run botsito --repo <ruta> corpus inventory`. | cli.py:3136 y :3150-3155; cli.py:189-216 |
| C2 | `scripts/barrido_dias.py` | Sí: `uv run python scripts/barrido_dias.py <filtrada.md> [--desde 18] [--hasta 31]`. | barrido_dias.py:19-21 y :58-62 |
| C3 | Las comprobaciones del contrato (`state check`, `knowledge validate`, `contrato_rama.py`, `make check > make-check.log 2>&1`) | Existen. | cli.py:3140-3147; contrato.yaml:44-48 |

##### Lo que no pude comprobar

- Los sha256 de A1 y A5, y si las cuatro capturas están ya en la subcarpeta: no abro el corpus y no hasheo material del trader.
- Los audios: cuántos son, el duplicado, las horas (09:59 a 10:13), el formato y la extensión. Tampoco dónde está ni cómo se llama la transcripción del 2026-11-23 (no debo leer esa carpeta). Si su fichero se llamara `*cruda-NO-LEER*`, la guardia negaría leerlo y pasarle `barrido_dias.py`.
- Que el trader «operó algunas operaciones en FundedNext», que el audio de A2 «solo valida los meses» y la foto de «las 191».
- El run 45670800735: no consulto la CI.
- Si la guardia deja copiar los audios con `cp` (mira el origen como lectura; sospecho que pasa, porque el Escritorio no está protegido).
- Sospecha sin medir: en Git Bash, `ln -s` copia en vez de enlazar si no está activado `winsymlinks`. Si alguien lo usara para dar `corpus/` al clon, copiaría el corpus entero.
- Cuánto tarda el inventario: rehashea los 21 vídeos.

##### Lo más grave

Hay dos cosas que harían trabajar a la sesión sobre algo falso o imposible.

- **La 0.3 pide medir el inventario «en un clon desechable», pero un worktree no tiene `corpus/`.** El comando falla antes de medir nada. La salida evidente, una unión, es la que rompió la guardia el 2026-11-20. Además, el diff del manifiesto no puede ser «solo las entradas nuevas»: el bloque `resumen` cambia siempre. Sin decidir esto antes, el PARA de 0.3 y el alcance del revisor saltarían en falso.
- **D3 parte de un fuentes.yaml que no existe.** «Mensajes del trader» no es una subcarpeta con entrada propia, sino un párrafo de «Material adicional de su operativa», y ya habla de gráficos, de esquemas y de una nota de voz que no se registró. El texto nuevo tiene que ampliar ese párrafo, siguiendo la forma de la entrada del 2026-10-14 y su nota de voz de 0:21.

A esto se suma H3: el encargo deja entrar «una captura de la configuración sin ningún resultado» sin decir que la única conocida trae agregados de meses reservados y que, por su propio punto (d), no entra.

## Estado

EN CURSO: aplicada la respuesta a la PARADA; faltan el recuadro de ADR-0100 §1 y el revisor.
