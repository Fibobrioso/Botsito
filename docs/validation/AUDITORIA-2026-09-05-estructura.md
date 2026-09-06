# AUDITORIA GLOBAL DE LA ESTRUCTURA · 2026-09-05

**Rama:** `feature/F05-auditoria-estructura` (desde `main` = `stable/F05` + `docs(state)` + revert)
**Pedida por:** el usuario ("una auditoria que busque fixear los errores que hayamos dejado en el
camino de esta estructura; necesitamos todo check antes de proseguir"), antes de abrir F07.
**Metodo:** dos agentes en paralelo (codigo/tests; documentacion/proceso/CI), sin editar; las
correcciones las aplico la sesion en esta rama con tests nuevos; `make check` verde al cierre.

## Veredicto de los auditores (antes de corregir)
- Codigo: la estructura esta sana; guardias de historial, hook, esquemas y contratos hacen lo que
  dicen; `make check` verde; ningun bug invalida lo ya validado. Diez hallazgos (1 media-alta,
  2 medias, 7 bajas) y deuda barata.
- Docs/proceso: el repo esta en verde, pero el ritual escrito no cubria el HANDOFF (dos commits
  en main en rojo sin registro), el HANDOFF de main contradecia PROJECT_STATE y los previos de
  F07 estaban en cinco sitios con una cifra contradictoria (4 frente a 5 videos).

## Correcciones aplicadas

### Codigo (con test cada una)
- **A1 · `corpus transcribe` sin las guardias de F05** (media-alta): en un clon sin `data/`, una
  retranscripcion (glosario v2, otro motor) pisaba la carpeta base y dejaba `knowledge validate`
  en rojo para siempre; ademas se admitian dos transcripciones activas por video. Nuevo modulo
  `corpus/trabajo.py` con las guardias comunes a transcripciones y fotogramas (carpeta de trabajo
  decidida tambien por los manifiestos registrados, exactamente una activa por video,
  inmutabilidad del contenido por carpeta, manifiesto existente idempotente sin `reemplaza_a`);
  `pipeline_transcripcion` y `fotogramas` las usan; `manifiestos_transcripcion.cargar_todos`
  exige una activa por video (los 5 reales cumplen). Es el requisito real de "retranscribir los
  5 videos con `--reemplaza-a`" antes de F07.
- **A3/A4** WAV ilegible y manifiesto de transcripcion con YAML invalido: `AudioError` /
  `TranscripcionError` en vez de traceback (el WAV ilegible se reextrae una vez).
- **A5** `corpus check` con un video sin `fichero` en el manifiesto: `validar_manifiesto` lo
  exige y lo compara con `fuentes.yaml` (antes `KeyError`).
- **A6** `parse_ms` estricto (`h:mm:ss[.mmm]`, sin signo, espacios ni `_`, tres decimales):
  `-0:00:01` ya no se leia como 1 s. F07 copia estos tiempos en la evidencia.
- **A7** El glosario rechaza un `.` sin escapar (`\bm.\b` casaba `m1` y `m5`).
- **A8** `carpeta_datos` unica en `config/ajustes.py`: `knowledge validate` reporta `ERROR:
  ajustes:` con un `settings.local.toml` roto en vez de seguir con `repo/data` en silencio.
- **A9** `transcript show --margen-s` negativo es error.
- **A10** Criterio unico para un manifiesto que ya existe: repetirlo sin `reemplaza_a` es
  idempotente; pedir otro `reemplaza_a` es error (antes divergian transcribe y frames).
- **A2** `state check`: la regla "en main, tras el tag, solo PROJECT_STATE.md" se mantiene (no se
  exenta el HANDOFF: la garantia es que nada entra en main sin tag) y el mensaje de error
  nombra el ritual. Decision de proceso: el HANDOFF se actualiza en la rama.
- Deuda pagada: `TOLERANCIA_DURACION_S` unica en `comun/documentos.py`; `import re` en su sitio
  en `evidence/modelo.py`; `Any` innecesarios sustituidos por `Callable`/tipos reales; docstring
  del pipeline con las marcas de carpeta; helpers duplicados (`_carpeta_para`, `_leer`,
  `_SUFIJO_CARPETA`) en un solo modulo.
- Tests: `pytest.raises(Exception)` -> excepciones concretas; `parse_ms` con negativos, signos y
  separadores; glosario con punto; escenario "otro video / clon sin data/" del pipeline con
  `reemplaza_a`; rutas de Important Files existen (`test_project_state_rutas.py`).

### Documentacion y proceso
- MASTER_PLAN §F: el HANDOFF se actualiza DENTRO de la rama; el run de CI que se anota es el del
  `docs(state)`; una rama de auditoria cierra con tag `stable/F##-auditoria-N` e informe propio.
  §0, B y ADR-0001 con los manifiestos de fotogramas (ADR-0008); H con F04/F05 en la fila de
  tests de historial y "5 videos + v5 en Drive" en la fila de cita; H.2 con F05 hecho y una fila
  nueva "Previos y entradas de F07" que reune lo que estaba en cinco sitios.
- PROJECT_STATE: Important Files corregido (`comun/historial.py`); "4 videos" -> 5; cifras de
  disco unificadas; Change Regimes ya incluia fotogramas; incidente de CI en main registrado
  (runs 33988126976, 34000351246, 34000376588, 34000499649); lineamientos del usuario separados
  de los hechos del corpus pendientes de evidencia; Change Log en orden descendente.
- HANDOFF reescrito (F05 validada, siguiente F07, regla del HANDOFF, comandos de fotogramas).
- READMEs de docs, scripts, hooks, knowledge, evidencia (`v1..v5`), validation (estado del
  informe no se edita tras el merge) y plantilla de brief (revision de diseno desde F05).
- `ci.yml`: `cancel-in-progress` solo fuera de main (c97273f quedo sin veredicto).

## Anotado y no cambiado (con motivo)
- Los 8 informes de validacion conservan `WAITING_FOR_USER_VALIDATION`: la validacion queda en
  PROJECT_STATE y en el tag (convencion escrita ahora en `docs/validation/README.md`).
- `drive_id` de v5 es una nota hasta que el usuario lo suba a Drive (fila H.2 de F07).
- `evidence.validar_contra_manifiesto` sigue aceptando rutas heredadas de `manifest.ficheros`:
  el cambio (parametro `referencias` alimentado por `referencias_conocidas`, en `knowledge
  validate` y en `evidence new`) es alcance de F07 y esta en su fila H.2.
- `data aggregate` con ventana vacia (rc 0 con AVISO): sin decision; Known Issue vigente.
- Parametros de FundedNext en Technical Debt: son datos para F11/F33, no deuda; se mueven al
  abrir F11.
- Hipotesis no verificadas por los auditores: precision de `pts_time` en `showinfo` de ffmpeg 6
  con `t >= 1000 s`; `historial_evaluable` en un worktree; `comprobar_obligatorios` con un
  obligatorio en un segundo ausente.

## Resultado
`make check` verde (ruff, mypy strict, 4 contratos de importacion, tests, `state check`,
`config validate`, `knowledge validate` con 5 videos, 5 transcripciones, 5 extracciones, 3
manifiestos de datos, historial intacto). Cifras en PROJECT_STATE.

## Que debe decidir el usuario
1. RATIFICAR la regla de proceso: el HANDOFF se actualiza en la rama y nunca en main tras el tag
   (alternativa descartada: exentar `docs/HANDOFF.md` en `state check`, que abre main a commits
   sin tag).
2. RATIFICAR el cierre de esta auditoria como rama con tag `stable/F05-auditoria-1` (ritual de
   MASTER_PLAN §F), para que `state check` en main siga en verde.
3. Confirmar que los previos de F07 (fila H.2) son los que hay que ejecutar en este orden:
   glosario v2 -> retranscribir 5 videos -> copia en Drive -> v5 en Drive -> abrir F07.

## Estado
WAITING_FOR_USER_VALIDATION
