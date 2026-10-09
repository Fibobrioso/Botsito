# Adelgazar PROJECT_STATE, punto Y y la prueba de octubre de la demo de FTMO

Rama `trabajo/adelgazar-estado`, abierta el 2026-10-08 desde `main` en 8cfd479 (merge 8d1578d,
tag `stable/F37g-guion-mismo-comando`; comprobados con `git rev-parse` antes de abrir). Encargo:
docs/encargos/trabajo-adelgazar-estado.md. Riesgo bajo: solo documentos. No cambia motor, spec,
knowledge, parametros, guardias, hooks ni tests; nadie ejecuta `motor arnes`.

## 0. Lo primero

- `PROJECT_STATE.md`: 24.362 bytes en `main`; **19.976 bytes** al final de la rama (objetivo
  20.000 o menos; tope del test 25.000, sin tocar).
- Salen **12 lineas**: 7 de «Pendientes heredados» (la cabecera de A3 y su d) cuentan como dos),
  3 de «Technical Debt» y 2 de «Reglas vivas». Todas con su texto literal, su condicion y su
  evidencia al final de `docs/state/HISTORIA.md`, en cuatro bloques (§2).
- **Para el consultor, tres cosas:**
  1. **A4 se queda**, aunque HISTORIA la da HECHA: su linea lleva dentro una PROPUESTA PENDIENTE
     (adelantar la negativa por A-27, ADR-0057 §5) que no vive en ningun otro sitio vivo, y
     `docs/validation/MEMORIA-SUITE.md:97-99` dice que «queda anotada como PENDIENTE en
     `PROJECT_STATE.md` (A4)». Si el consultor la da por decidida o caducada, sale.
  2. **La salida que hace bajar de 20.000 es la decision del 2026-09-30 sobre marzo** (Reglas
     vivas, condicion d). Sin ella la prevision era 20.510 bytes. Si el consultor prefiere que se
     quede, faltan unos 520 bytes, y lo siguiente que podria salir esta en §1.4.
  3. **CLAUDE.md:154-158 ha envejecido**: dice que marzo «no se sortea ni se ingiere hasta que A-42
     este RESUELTA con el trader en la sesion 4», y A-42 ya esta RESUELTA (ADR-0069). No se toca
     aqui (el encargo solo abre CLAUDE.md para el punto Y); se apunta.
- Fase 4: **el script SI registra el modo de la cuenta**: `modo_margen`, con
  `ACCOUNT_MARGIN_MODE`, en `tools/mql5/MedirDemoFTMO.mq5:370` (fila `contexto`). No se cambia.
  La medida de husos coincide con lo esperado (§5).

## 1. Fase 0: el inventario

Bytes por seccion, medidos con un guion sobre el fichero (`## ` y `### ` como cortes), antes y
despues:

| Seccion | Antes | Prevision (fase 0) = despues |
|---|---:|---:|
| cabecera `# PROJECT STATE` | 802 | 134 |
| Current Branch | 44 | 44 |
| Current Feature | 252 | 252 |
| Stable Main State | 537 | 537 |
| Last Stable Commit | 177 | 177 |
| Tests Currently Passing | 226 | 226 |
| Next Action (sin los pendientes) | 4.143 | 4.242 (la frase de la entrada A) |
| Pendientes heredados | 2.880 | 1.852 |
| Known Ambiguities | 3.421 | 3.062 |
| Technical Debt | 6.866 | 5.767 |
| Reglas vivas (intro) | 174 | 67 |
| Change Regimes | 922 | 922 |
| Things That Must Not Be Changed | 836 | 836 |
| Decisions and Rationale | 2.055 | 1.180 |
| Known Issues | 370 | 370 |
| Completed Features | 370 | 157 |
| Change Log | 258 | 151 |
| **Total** | **24.333** | **19.976** |

«Antes» es el fichero de la rama recien abierta (623b43b), que ya lleva la rama nueva en Current
Branch y Current Feature: 29 bytes menos que los 24.362 de `main`. La prevision se calculo en la
fase 0 aplicando las salidas y las introducciones a una copia en la carpeta de trabajo, con el
mismo guion que despues se aplico al fichero; dio 19.976 y el fichero final mide lo mismo.

Condiciones del encargo: (a) HECHA o PAGADA, (b) REPETIDA, (c) SUSTITUIDA, (d) NO ES DE SU SECCION;
«se queda» si ninguna se demuestra (niega por defecto). Cada linea, por su arranque.

### 1.1 Pendientes heredados

| Linea | Condicion | Evidencia |
|---|---|---|
| A2 (MedirDemoFTMO, tres ejecuciones) | **(b) sale** | Entrada A de la Next Action (tres ejecuciones, la primera antes del 25-10, «Con el primer CSV, rama para fijar los valores de ADR-0057 y A-27») y docs/runbooks/DEMO-FTMO.md:74-80 (las tres fechas) |
| A3 (ramas de codigo, en este orden) | **(a) sale** | Sus ramas a, b, c y 0, HECHAS en `stable/F36-nocturno-01oct` (HISTORIA, «LO QUE DECIA NEXT ACTION HASTA EL 2026-09-30»); la d), abajo |
| d) vida de la orden stop y RN-007 | **(a)+(b) sale** | RN-006: merge cf6b1bf, tag `stable/F36d-orden-stop-pivote`, ADR-0064, docs/validation/F35-ORDEN-STOP-PIVOTE.md. RN-007: entrada H de la Next Action |
| A4 (memoria de la suite) | **se queda** | La memoria SI esta hecha (`stable/F31c-memoria-suite`, `stable/F31d-ci-linux-memoria`; HISTORIA:656), pero la linea lleva la propuesta PENDIENTE de ADR-0057 §5 y MEMORIA-SUITE.md:97-99 la remite a esta linea; ADR-0057 §5 sigue igual. Niega por defecto |
| A5 (para la sesion 4) | **(a) sale** | Se pregunto todo en la sesion 4 (`stable/F36v-sesion-04`): A-42, A-51, A-21, G-2, E-1 y A-50 estan en la hoja, «Las que hay que hacer» (docs/sesion-4/PREGUNTAS.md, seccion 1), y en SESION-04-EXTRACCION.md §3.1, §3.9, §3.11, §3.13, §3.17 y §3.18; A-39 y A-13 no estaban en esa seccion (PREGUNTAS.md:337 esta en «Las que ya estan respondidas», y lo de los cortes de audio en la seccion 3), pero se preguntaron en la sesion como S-5 y S-24 (SESION-04-EXTRACCION.md §3.6 y §3.23). Corregido tras el revisor (a1); la nota, al final de HISTORIA |
| 2 (marzo interrumpe; entrega) | se queda | docs/runbooks/ENTRADA-MARZO.md:32 remite a «Next Action 2 y 12» para la entrega (`vistos.yaml`, confirmacion escrita del trader); no vive en otro sitio |
| 6 (febrero no se toca ni se descarga) | se queda | CLAUDE.md no lo dice (solo «febrero o marzo vienen detras», CLAUDE.md:147); ningun runbook |
| 7 (junio, la guardia y los once dias) | se queda | Sin evidencia de arreglo |
| 8 (brief de los 4 dev de septiembre) | se queda | Sin evidencia |
| 9 (re-descargar un mes rompe kit build) | se queda | Sin evidencia |
| 10 (el dueno: no comprar; Swing; prueba gratuita) | se queda | Parcialmente sustituida: el tipo Swing 100k existe (prueba creada el 2026-10-08, entrada A), el apalancamiento esta en FTMO-REGLAS R9 (1:30) y A-27/A-28 los miden los pasos 1-2 de DEMO-FTMO. Pero «no comprar todavia» y «grabar spread y ticks de esa demo desde el primer dia» no viven en otro sitio. Niega por defecto |
| 12 (marzo entra por su propia rama; libros.yaml) | se queda | ENTRADA-MARZO.md:32 remite a ella; ENTRADA-MARZO.md:194 cubre la entrada en `libros.yaml`, pero no «Aleks no abre el fichero antes» ni la complementariedad con 2 |
| 15 (A-18, pregunta de reserva) | se queda | A-18 sigue ABIERTA; ninguna respuesta registrada a esa pregunta |
| 22 (la sesion 02) | **(a) sale** | Merge 408b609, tag `stable/F19-sesion-02-videos`, SESION-02-VIDEO.md y SESION-02-EXTRACCION.md; despues, sesiones 3 y 4 |
| 23 (marzo recibido sin abrir) | **(b) sale** | CLAUDE.md:154-158 y ENTRADA-MARZO.md (paso a y PARADA B0) |
| 25 (RN-004 bloqueada solo por A-35) | se queda | A-35 sigue ABIERTA |
| 27 (pendiente para Aleks, con FTMO) | se queda | La respuesta de FTMO (FTMO-REGLAS.md) contesta el gap trading, pero no si la comision es por lado (R12 NO ENCONTRADA) ni todo lo demas |
| 30 (RN-004 tras A-35, con arnes y visor) | se queda | A-35 ABIERTA |
| 34 (pendientes de ticks-llenado) | se queda | Solo su (a) se acerca a la X; (b) deslizamiento y (c) swap, sin otro sitio |
| 35 (RN-020 tras A-44) | se queda | A-44 y A-51 ABIERTAS |
| 36 (medir en la demo las cuatro decisiones de ADR-0057) | **(b) sale** | Entrada A; DEMO-FTMO.md:86-96 (pasos 1-7 frente a ADR-0057 d1-d4 y §5, A-27); ADR-0057 §5:58-61 (los dos stops level con el mismo valor) |
| 37 (rechazos por volumen maximo) | se queda | Sin evidencia |

### 1.2 Technical Debt

| Linea | Condicion | Evidencia |
|---|---|---|
| Sin git callan... (HISTORIAL-SIN-GIT §3) | se queda | Abierta |
| RN-029 a RN-032 citan de relleno... | se queda | Abierta |
| EL BROKER SIMULADO LLENA AL INSTANTE UNA LIMITE... | se queda | Su texto entero (HISTORIA, Archivo 1) dice RESUELTA en el simulador pero «Sigue PENDIENTE medir en la demo lo que hace MT5» |
| LA GRAMATICA DEL KIT PASA A LA UNIDAD OPERACION | se queda | «hay que adaptar la gramatica y `kappa.py` antes del primer etiquetado por operacion»; sin evidencia |
| **LA LECTURA PREVIA DE LA TRANSCRIPCION DE v6...** | **(a) sale, PAGADA** | Pedia decidir si ese dia se retira del holdout: retirado en merge 286c113, tag `stable/F14-v6-fuera-del-holdout`, ADR-0041, V6-FUERA-DEL-HOLDOUT.md (HISTORIA:777) |
| `cherry-pick` Y `rebase` NO PASAN POR LA PUERTA... | se queda | CLAUDE.md da la regla y la guardia los bloquea, pero la deuda (no pasan por `pre-commit`) sigue |
| `scripts/v5_criterio.py` SOLO RECONOCE CAJAS DE VENTA | se queda | Sin evidencia |
| NADA COMPRUEBA MECANICAMENTE QUE EL CUERPO DE UN INFORME CERRADO... | se queda | CLAUDE.md la remite aqui («Technical Debt») |
| LA SERIE DEL TRADER ES OANDA... | se queda | Su propia linea dice que la parte de la serie sigue viva (A-16 ABIERTA) |
| EL FRACTAL 5/120... | se queda | Sin evidencia |
| `maxTP` ES EL PRECIO DE CIERRE... | se queda | No vive en otro sitio vivo |
| LA GUARDIA DE `cobertura_material`... | se queda | Sin evidencia |
| EL `no_trade` POR AUSENCIA NO ESTA DECIDIDO... | se queda | Sin evidencia |
| `fecha_grabacion` ... EJE DE PRIMERA CLASE | se queda | Sin evidencia |
| CUARTA APARICION DEL PUNTO CIEGO DEL DETECTOR... | se queda | Sin evidencia |
| **LOS CINCO PATRONES DE DEFECTO...** | **(b)+(d) sale, RECLASIFICADA** | Entera en docs/runbooks/ERRORES-RECURRENTES.md:35-41, como dice su propia linea; es regla, no deuda |
| LA PRIMERA MEDIDA DE A-18 SALE DEL MATERIAL... | se queda | A-18 ABIERTA |
| F26 NO PUEDE PUNTUAR EL OBJETIVO HASTA QUE A-18... | se queda | A-18 ABIERTA |
| `idealTP`... | se queda | Sin evidencia |
| BUSCAR EN EL CORPUS ANTES DE REDACTAR CUALQUIER AMBIGUEDAD... | se queda | docs/runbooks/AMBIGUEDADES.md no lo dice (buscado «corpus», «busc»); tampoco CLAUDE.md, `.claude/agents/` ni `.claude/skills/` |
| EL DIA QUE UN CAMINO GUARDE MATERIAL EN `knowledge/cases/<camino>/`... | se queda | Sin evidencia |
| `lectura_de_velas` SIGUE LEYENDO EL `config.yaml`... | se queda | Sin evidencia |
| DOS DIAS DEL UNIVERSO DE LA SESION 1... | se queda | Sin evidencia |
| UNA PREGUNTA ABRE N PARTICIONES... | se queda | Sin evidencia |
| EL FALLBACK DE `leer_fichero`... | se queda | Sin evidencia |
| UN TOKEN NO PUEDE DECLARAR QUIEN LO PRODUCE... | se queda | Sin evidencia |
| UNA `pregunta` DE AMBIGUEDAD PUEDE NOMBRAR UN INSTANTE... | se queda | Sin evidencia |
| EL PUNTO CIEGO DEL DETECTOR..., TERCERA APARICION | se queda | Sin evidencia |
| EL DETECTOR DE CONTRADICCIONES NO VE LOS TEMAS HERMANOS | se queda | Sin evidencia |
| LA VIA DE PROPUESTA NO ADMITE `supersede` | se queda | CLAUDE.md la llama deuda («deuda anotada el 2026-09-17»): sigue abierta |
| UN CONFIRM SOBRE UN ITEM SUPERSEDIDO QUEDA INVISIBLE... | se queda | Sin evidencia |
| Transcripciones heredadas (Whisper tiny, `_procesado/`)... | se queda | MIRAR-EL-MATERIAL.md:81-83 dice que sirven para localizar y no para citar, pero no literal (falta que F07 cita solo sobre `tr-*` y la decision del 2026-09-05). Niega por defecto |
| Copia de seguridad de las crudas activas y los WAV... | se queda | INCOMPLETA |
| **v5 (...) en Drive desde el 2026-09-06...** | **(d) sale, RECLASIFICADA** | Es un hecho y esta en knowledge/corpus/fuentes.yaml:35 (`drive_id` y subcarpeta) y manifest.yaml:2273. Nota: `fuentes.yaml` dice 2026-09-07 |
| `data/fotogramas/` ... no se copia a Drive | se queda | No vive en otro sitio |
| F07, limitacion declarada... | se queda | No vive en otro sitio vivo |
| Hook local: tras cambiar `scripts/git-hooks/`... | se queda | Sin otro sitio comprobado |
| `data aggregate` con una ventana fuera del dataset... | se queda | Sin evidencia de que F14 lo trate como error |
| Proteccion de rama en GitHub... | se queda | Sin evidencia |
| F11: las reglas de `strategy_spec.yaml` son PROSA... | se queda | Que F12 lo cerrara no esta comprobado aqui |

### 1.3 Reglas vivas

| Linea | Condicion | Evidencia |
|---|---|---|
| Change Regimes: holdout/{1,2,3} | se queda | CLAUDE.md da el punto 3, pero no esta linea (que es abrir, la guarda de `tests/conftest.py`...) |
| Change Regimes: data/manifests/... | se queda | CLAUDE.md dice la inmutabilidad, no «Correccion = manifiesto nuevo con `reemplaza_a`; exactamente una extraccion activa por video» |
| Things That Must Not Be Changed (5 lineas) | se queda | No viven literales en otro sitio |
| Decisions 2026-09-04 (tres) | se queda | Sin comprobar literal en otro sitio; niega por defecto |
| Decisions 2026-09-25, SIMULADOR-CUENTA §5 | se queda | Vigente |
| **Decisions 2026-09-25, `firma_comision_por_lado`** | **(c) sale, SUSTITUIDA** | Implementada en ba28a82 (2026-09-26; en `main` con `stable/F24-ticks-llenado`): hoy knowledge/cuentas/ftmo-2step-swing-100k.yaml:386-398, `estado: CONFIRMED`, `valor: true`, `fuente: {tipo: decision, id: ADR-0050}`, y la condicion «hasta que FTMO lo confirme» en la descripcion. Lo que falta de FTMO sigue en el punto 27 |
| **Decisions 2026-09-30, marzo por el camino de fidelidad** | **(d)+(c) sale, SUSTITUIDA** | Vive literal en docs/validation/REGISTRO-MARZO.md, «Estado» (160-167) y §4 (119-128), y en CLAUDE.md:154-158; su parte de A-42 se cumplio (A-42 RESUELTA, ADR-0069, `stable/F37d-activacion-a42`) |
| Known Issues (dos) | se queda | No viven en otro sitio |

### 1.4 Si el consultor quiere margen

Ninguna otra linea cumple hoy una condicion con evidencia. Las mas cercanas, que piden una decision
y no una medida: A4 (si la propuesta de A-27 se da por decidida o caduca, unos 125 bytes), el punto
10 (si «no comprar todavia» deja de valer, unos 120), y la linea «Candidatas a ambiguedad sin abrir»
de Known Ambiguities (C2 y C3 ya son A-48 y A-49; fuera del alcance de esta fase).

## 2. Fase 1: lo que salio y adonde

Al final de `docs/state/HISTORIA.md`, tras el Archivo 24, cuatro bloques con el texto literal de
cada linea, su condicion y su evidencia:

- `# Pendiente heredado SALE · ...`: A2, A3, d), A5, 22, 23 y 36.
- `# Technical Debt PAGADA · ...`: la lectura previa de v6.
- `# Technical Debt RECLASIFICADA · ...`: los cinco patrones y v5 en Drive.
- `# Regla viva SUSTITUIDA · ...`: `firma_comision_por_lado` y marzo del 2026-09-30.

En `PROJECT_STATE.md` no queda resumen de ninguna. Lo que se queda no cambia de texto: comprobado
con un diff linea a linea frente a `main` (§6).

## 3. Fase 2: las introducciones

La cabecera del fichero y las de «Pendientes heredados», «Known Ambiguities», «Technical Debt»,
«Reglas vivas», «Completed Features» y «Change Log» pasan a una o dos lineas que apuntan a
`docs/state/README.md`. Lo que decian y README no decia (la lista de lo que vive en HISTORIA, «una
sesion nueva lee este fichero y CLAUDE.md», la fuente de la tabla de ambiguedades, como entra y
sale una deuda, que `state check` regla 4 mira las dos Completed Features...) se copio antes, TAL
CUAL, a README, en «Lo que decian las introducciones de PROJECT_STATE.md hasta el 2026-10-08». Y
README gana «Que sale de PROJECT_STATE, y con que criterio»: las cuatro clases de bloque, el
criterio (a)-(d), la negacion por defecto, con fecha y rama, y el punto Y. Las secciones, su orden y
la tabla de `test_kit.py` no cambian.

## 4. Fase 3: el punto Y

Buscado con grep «Next Action», «commit de estado», «HECHAS» y «punto 3» en `.claude/skills/`
(cerrar-rama y abrir-rama), `docs/state/README.md`, `CLAUDE.md` y `docs/runbooks/`. Sitios y su
antes y despues:

| Sitio | Antes | Despues |
|---|---|---|
| docs/runbooks/RITUAL.md, punto 3 del commit del contrato | «Las entradas de Next Action que la rama deja HECHAS salen de `PROJECT_STATE.md`» ... «Si la rama no cierra ninguna, este punto no toca nada.» | «TODO cambio de la Next Action que mande la orden de cierre se hace aquí, en este commit» (punto Y): salen las HECHAS (con el mismo bloque en HISTORIA), entran las nuevas y cambian las que diga la orden; `wc -c PROJECT_STATE.md` por debajo de 25.000 o se para ANTES del commit; «Si la orden no cambia la Next Action, este punto no toca nada.» |
| RITUAL.md, comentario del `git add` | `# solo si el punto 3 sacó alguna entrada de Next Action` | `# solo si el punto 3 cambió la Next Action` |
| RITUAL.md, la puerta | «más `M  PROJECT_STATE.md` si el punto 3 sacó algo» | «más `M  PROJECT_STATE.md` si el punto 3 cambió la Next Action» |
| RITUAL.md, paso del commit de estado (antes linea 216) | «SOLO las líneas de cabecera: Current Branch (`main`), Current Feature, Stable Main State, Next Action y Last Stable Commit.» | «... Current Branch (`main`), Current Feature, Stable Main State y Last Stable Commit. La Next Action ya cambió en la rama, en el commit del contrato (punto 3 de arriba): aquí solo cambia si la orden de cierre lo pide expresamente, y solo en lo que pida» (con la fecha y lo que decia antes) |
| .claude/skills/cerrar-rama/SKILL.md, paso 3 | Listaba en ese commit solo el registro de HISTORIA y la fila de ERRORES-RECURRENTES | Tercer punto: todo cambio de la Next Action que mande la orden, con `PROJECT_STATE.md` por debajo de 25.000 bytes |
| cerrar-rama, paso 5 | «SOLO las lineas de cabecera de la lista del runbook» (la lista nombraba la Next Action) | Anade: «La Next Action no: ya cambio en el paso 3, y aqui solo si la orden lo pide expresamente.» |
| docs/state/README.md, «Lo HECHO del Next Action sale...» | Solo hablaba de las HECHAS | Anade que desde el 2026-10-08 ese commit lleva TODO cambio de la Next Action que mande la orden |

Sin cambio, revisados: `abrir-rama` (no habla de la Next Action), `CLAUDE.md` (tampoco),
ERRORES-RECURRENTES.md:51, :54 y :66 (filas historicas de la tabla: no se reescriben),
ENTRADA-MARZO.md:32 (remite a los puntos 2 y 12, que se quedan) y RENOVAR-CIERRES.md:22 (remite a
la entrada N, que sigue).

## 5. Fase 4: la prueba de octubre de 2026

Seccion nueva al final de docs/runbooks/DEMO-FTMO.md, con lo que declara Aleks y sin el numero de
cuenta. La entrada A de `PROJECT_STATE.md` gana una frase que apunta a ella.

La medida de husos, con `zoneinfo` (guion en la carpeta de trabajo, no en el repositorio):

```
2026-10-12 03:00 Lima -> 2026-10-12 10:00 CEST (UTC+0200)
2026-10-12 07:30 Lima -> 2026-10-12 14:30 CEST (UTC+0200)
2026-10-12 08:00 Lima -> 2026-10-12 15:00 CEST (UTC+0200)
2026-10-21 03:00 Lima -> 2026-10-21 10:00 CEST (UTC+0200)
2026-10-21 07:30 Lima -> 2026-10-21 14:30 CEST (UTC+0200)
2026-10-21 08:00 Lima -> 2026-10-21 15:00 CEST (UTC+0200)
2026-10-23 03:00 Lima -> 2026-10-23 10:00 CEST (UTC+0200)
2026-10-23 07:30 Lima -> 2026-10-23 14:30 CEST (UTC+0200)
2026-10-23 08:00 Lima -> 2026-10-23 15:00 CEST (UTC+0200)
2026-10-26 03:00 Lima -> 2026-10-26 09:00 CET (UTC+0100)
2026-10-26 07:30 Lima -> 2026-10-26 13:30 CET (UTC+0100)
2026-10-26 08:00 Lima -> 2026-10-26 14:00 CET (UTC+0100)
```

Coincide con lo esperado: 10:00-15:00 y 14:30. Dentro de la franja 9-18 del runbook
(DEMO-FTMO.md:41) y de la ventana del bot, 07:00-15:00 Europe/Madrid (`ventana_inicio` y
`ventana_fin`, parametros.yaml:351 y :367); las 08:00 de Lima caen justo en las 15:00, el borde. El
26-10 se da solo como control del cambio de hora: no se escribe en el runbook.

**El modo de la cuenta:** `tools/mql5/MedirDemoFTMO.mq5:370` escribe
`Dato(m, "contexto", "modo_margen", EnumToString((ENUM_ACCOUNT_MARGIN_MODE)AccountInfoInteger(ACCOUNT_MARGIN_MODE)))`.
Lo registra. No se cambia el script.

## 6. Comprobaciones

- `wc -c PROJECT_STATE.md`: **19976**.
- Lo que se queda no cambia: un guion compara linea a linea el `PROJECT_STATE.md` de la rama con el
  de `main`. Las unicas lineas nuevas son las introducciones (cabecera y seis secciones), Current
  Branch, Current Feature, la entrada A (una frase al final) y las dos «— ninguna desde el
  Archivo 24»; las unicas que desaparecen son las introducciones viejas, las 12 que salen y lo que
  cambio al abrir la rama.
- Cada linea que sale esta, byte a byte, en su bloque de `docs/state/HISTORIA.md`: comprobado con
  `grep -cF` de cada una sobre lo anadido.
- `uv run pytest tests/unit/test_project_state.py tests/unit/test_historia.py -q`, con `tests/unit/test_kit.py` (la tabla de ambiguedades): **47 passed**; `uv run botsito
  state check`: OK.
- `make check > make-check.log 2>&1`:
  - sobre el arbol de 623b43b (apertura): exit 0, 0 `failed`, 2454 passed, `SELLO: make check en
    verde sobre el arbol ebdeb4b2bb2f4727533528df52e710c3c8483f56`, pico 293 MiB;
  - sobre el arbol de 01b8405 (fases 1 a 4): exit 0, 0 `failed`, 2454 passed, `SELLO: make check en
    verde sobre el arbol 0cf6956c2d4ffb3eb560b0a7ba89d31ab69a10a6`, pico 293 MiB;
  - sobre el arbol final (este informe con el del revisor pegado y la nota de A5 en HISTORIA): se
    lee en su log antes del ultimo commit, que no existiria sin el sello (el hook `pre-commit` lo
    exige).
- No hay CI de Linux: la rama no toca hooks, rutas ni plataforma (encargo).

## 7. Informe del revisor

Subagente `revisor`, sobre 623b43b y 01b8405, con el alcance del encargo. No ejecuto `make check`
(ya estaba en verde y tarda 20 minutos); si el resto de comprobaciones del contrato. Pegado con sus
tablas y hallazgos tal cual; sus listas «Comprobado sin hallazgos», «Evidencia de las salidas» y
«Comandos ejecutados» van condensadas en parrafo (la ultima, omitida salvo su linea final), sin
quitar ninguna comprobacion ni cambiar lo que dicen:

> ## Informe del revisor · trabajo/adelgazar-estado · 2026-10-08
>
> Alcance: commits 623b43b y 01b8405 sobre main 8cfd479. No ejecuté `make check`, como pediste. Sí ejecuté `scripts/contrato_rama.py`, el pytest de `test_project_state.py` y `test_historia.py`, `state check` y `wc -c`.
>
> ### Eje (a) · Reglas de la casa
> Resumen: 0 bloquea, 1 importa, 3 menor.
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | a1 | importa | En la salida de A5 se dice que lo que listaba «entró en la hoja de la sesión 4», y para A-13 y A-39 eso es inexacto. En `PREGUNTAS.md`, A-13 y A-39 figuran fuera de la hoja («Lo que tapan los cortes de audio de v9»). La fila de la línea 337, citada como evidencia de A-13, está en la sección «Las que ya están respondidas: no se vuelven a preguntar». Las dos sí se preguntaron después en la sesión: S-5 (A-30/A-39) y S-24 (A-13), en `SESION-04-EXTRACCION.md` §3.6 y §3.23. La condición (a) se sostiene. Lo que falla es la cita `A-13:337` y la frase «todo entró en la hoja». | `docs/sesion-4/PREGUNTAS.md:337` y las líneas 352-366 (sección 3). `SESION-04-EXTRACCION.md:466, 860, 937, 954`. Texto de HISTORIA en la línea 7060 y de ADELGAZAR-ESTADO.md línea 72. |
> | a2 | menor | Dos reglas de operación de las introducciones viejas quedaron solo dentro de la cita «Lo que decían las introducciones… hasta el 2026-10-08». Son «una deuda nueva entra con una línea que apunte a su informe; una pagada se borra de aquí» y «abrir una ambigüedad añade su fila; cerrarla la quita». El encargo lo permite, porque pide pasar la cita literal a README. Aun así, la regla vigente queda como cita histórica y no como texto operativo. | `docs/state/README.md:76-116`. La intro nueva de «Technical Debt» en `PROJECT_STATE.md` solo dice «texto entero y criterio de salida: README». |
> | a3 | menor | REGISTRO-MARZO §4 sigue titulado «Propuesta, SIN APLICAR». Que fue aceptada consta solo en «Estado» (líneas 160-167). La salida de la decisión del 2026-09-30 cita ambos sitios, así que es correcta. Basta con saber que el §4 solo no basta. | `REGISTRO-MARZO.md:115` frente a `:160-167`. |
> | a4 | menor | La salida de la línea 22 («sesión 02 con A-35 y A-44 como PRIORIDAD») es legítima por (a), porque la sesión se hizo. A-35 y A-44 siguen ABIERTAS y sus consecuencias quedan en 25, 30 y 35, que se quedan. No hay pérdida de información. Lo anoto por si el consultor prefiere que la prioridad siga visible. | `PROJECT_STATE.md:63, 65, 67`. |
>
> Comprobado sin hallazgos: el contrato (`contrato_rama.py`: 9 ficheros dentro; 7 tests de `test_project_state.py` y `test_historia.py` pasan; `state check` OK; `wc -c` 19976 frente a 24362 en main; ningún fichero de `rutas_protegidas` en el diff); los 12 textos que salen, literales en los cuatro bloques nuevos de HISTORIA (igualdad exacta de línea, script de solo lectura), tras el «# Archivo 24»; HISTORIA solo suma (`numstat 293 0`); lo que se queda no cambia (solo son nuevas las introducciones, Current Branch y Current Feature, la frase de la entrada A y las dos «— ninguna desde el Archivo 24»); las introducciones viejas, literales en `docs/state/README.md:76-116`; sin `Fuente:` que comprobar, sin ADR, evidencia, feedback, ambigüedades ni informes cerrados cambiados. RITUAL tras el punto Y: el punto 3 (137-145), el comentario del `git add` (153), la puerta (161) y el paso del commit de estado (219-223) dicen lo mismo; la 232 sigue coherente; `cerrar-rama/SKILL.md:74-76` y `:83`, y `README.md:23-33` y `:68-71`, alineados; `abrir-rama` y `CLAUDE.md` no hablan de la Next Action; `ERRORES-RECURRENTES.md:51, 54, 66` son filas históricas; `ENTRADA-MARZO.md:32` y `RENOVAR-CIERRES.md:22` remiten a entradas que se quedan; ningún otro sitio dice lo contrario. Fase 4 (`DEMO-FTMO.md:101-119`): sin número de cuenta (grep de 6 o más dígitos); `zoneinfo` da 03:00→10:00 CEST, 07:30→14:30 y 08:00→15:00 el 12-oct, y el 25-oct 03:00 ya da 09:00 CET; la franja 9-18 en `DEMO-FTMO.md:41`; `ventana_inicio` "07:00" (`parametros.yaml:351`) y `ventana_fin` "15:00" (`:367`); las 08:00 de Lima en el borde, y el texto lo dice.
>
> Evidencia de las salidas, comprobada contra el repositorio: **marzo del 2026-09-30** se sostiene por (d) y (c): `REGISTRO-MARZO.md` «Estado» (160-167) trae literal el camino de fidelidad con `eurusd-2026-03`, A-42 RESUELTA por el trader y no por ADR, «la PARADA B0 no cambia» y las 7 imágenes sin abrir y preguntadas (la 19); §4 (119-128) los cupos y la semilla; `ENTRADA-MARZO.md:98-107` la PARADA B0 y la semilla; `CLAUDE.md:154-158` el camino y las imágenes; A-42 RESUELTA (`ambiguedades.yaml:1118`, ADR-0069). Matiz: la decisión sigue «Estado: ACTIVE» y sus consecuencias (semilla antes del sorteo, cupos) viven ahora solo en un informe y un runbook, no en CLAUDE.md; es (d) válido, pero es la salida con más peso, y la decisión es del consultor. **23**: (b), `ENTRADA-MARZO.md:46, 98-107`. **`firma_comision_por_lado`**: (c), `ftmo-2step-swing-100k.yaml:386-398` (`CONFIRMED`, `true`, ADR-0050), ba28a82 ancestro de `stable/F24-ticks-llenado`, lo de FTMO en el 27. **v6**: (a), `stable/F14-v6-fuera-del-holdout` → 286c113, ADR-0041, `V6-FUERA-DEL-HOLDOUT.md`, `retirados.yaml`. **RN-006 y d)**: `stable/F36d-orden-stop-pivote` → cf6b1bf, `F35-ORDEN-STOP-PIVOTE.md`, RN-007 en la H. **22**: `stable/F19-sesion-02-videos` → 408b609, `SESION-02-VIDEO.md`, `SESION-02-EXTRACCION.md`, tags de las sesiones 3 y 4. **36 y A2**: (b), `DEMO-FTMO.md:90-96` (d1-d4 y §5), `--diagnostico-a27` en `ADR-0057:67`, fechas en `DEMO-FTMO.md:75-79`. **Cinco patrones**: `ERRORES-RECURRENTES.md:35-41`. **v5**: `fuentes.yaml:35`, `manifest.yaml:2273`; la nota 09-07 frente a 09-06 es correcta. **A4 se queda**: `MEMORIA-SUITE.md:97-99` la remite a A4 y la propuesta de A-27 no vive en otro sitio.
>
> ### Eje (b) · Encargo
> Resumen: 0 bloquea, 1 importa, 1 menor. Requisitos: 12 hechos, 0 parciales, 0 no hechos.
>
> | # | Requisito | Estado | Evidencia |
> |---|---|---|---|
> | 1 | Verificar con git la base (main en 8cfd479, tag en 8d1578d) y abrir con la skill | Hecho | ADELGAZAR-ESTADO.md línea 3. `git log` muestra 623b43b sobre 8cfd479. |
> | 2 | PROJECT_STATE a 20.000 bytes o menos | Hecho | `wc -c` da 19976. |
> | 3 | Fase 0: tabla por línea con condición y evidencia, más bytes antes y después | Hecho | ADELGAZAR-ESTADO.md §1.1-1.4. A4, 6 y 10 comprobadas: A4 y 10 se quedan, y 6 se queda porque CLAUDE.md no lo dice. |
> | 4 | Comprobar `firma_comision_por_lado` | Hecho | §1.3 y el yaml de la cuenta. |
> | 5 | Fase 1: un bloque por clase al final de HISTORIA, con texto literal, condición y evidencia | Hecho | HISTORIA desde la línea 7041: cuatro bloques con los nombres exactos del encargo. |
> | 6 | Fase 2: introducciones a 1-2 líneas que apunten a README; lo que decían pasa a README | Hecho | Diff de `PROJECT_STATE.md` y `README.md:76-116`. |
> | 7 | README: párrafo con las clases y el criterio (a)-(d), con fecha y rama | Hecho | `README.md:46-71`. |
> | 8 | Fase 3: paso del commit de estado, punto 3, comentario del `git add` y puerta | Hecho | `RITUAL.md:137-145, 153, 161, 219-223`. |
> | 9 | Fase 3: grep en skills, README, CLAUDE.md y runbooks, y lista de sitios con antes y después | Hecho | ADELGAZAR-ESTADO.md §4 (tabla y «Sin cambio, revisados»). Coincide con mi grep. |
> | 10 | Fase 4: sección en DEMO-FTMO.md sin número de cuenta, husos medidos | Hecho | Verificado en el eje (a). |
> | 11 | Informe: ¿registra `MedirDemoFTMO.mq5` el modo de cuenta? | Hecho | `tools/mql5/MedirDemoFTMO.mq5:370` escribe `modo_margen` con `ACCOUNT_MARGIN_MODE`. El informe lo dice bien, en §0 y en §5. El script no se cambió. |
> | 12 | Una frase en la entrada A; Y sin marcar HECHA; nadie ejecuta `motor arnes` | Hecho | `PROJECT_STATE.md:39` tiene la frase y la entrada Y sigue en la línea 36. El informe lo declara. |
>
> Lo que NO se toca, comprobado con el diff: hooks, tests, spec, knowledge, `src/`, `tools/`, `scripts/` y CLAUDE.md quedan intactos. Los ficheros tocados están dentro de `rutas_permitidas`.
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | b1 | importa | Falta la comprobación que el encargo pide para el cierre. El informe dice (§6) que `make check` queda «sobre el árbol de este commit», pero la línea del resultado final (exit 0, ningún failed, SELLO) se remite a «Informe del revisor», que aún no existe. Cuando se pegue este informe, hay que añadir también el resultado del `make check` y mover el «Estado» para que siga al final. Eso lo hace quien pega. | ADELGAZAR-ESTADO.md líneas 245-247 y 250-253. |
> | b2 | menor | El informe cita bien que `CLAUDE.md:154-158` ha envejecido. Esa línea sigue siendo coherente como condicional («hasta que A-42 esté RESUELTA»), y la condición ya se cumple. No se corrige aquí, pues el encargo no abre CLAUDE.md para eso. Conviene que el consultor lo decida. | ADELGAZAR-ESTADO.md §0, punto 3, y `CLAUDE.md:154-158`. |
>
> ### Lo que no pude comprobar
> - `make check` y su `SELLO` sobre 01b8405 (fuera por instrucción).
> - Que el trader respondiera de hecho en la sesión 4 a las preguntas de A5: solo vi que `SESION-04-EXTRACCION.md` las trata; no abrí material de la sesión.
> - `stable/F31c-memoria-suite` y `stable/F31d-ci-linux-memoria` apuntan a 1cca80e y 99ea2f5; no comprobé su contenido, porque A4 se queda.
>
> ### Lo que quizá debería salir o quedarse (sin cambiar nada)
> - A4 se queda, y es correcto (~125 bytes si el consultor da la propuesta de ADR-0057 §5 por decidida).
> - Punto 10 («no comprar todavía», unos 120 bytes): lo decide el consultor.
> - «Candidatas a ambigüedad sin abrir»: C2 y C3 ya son A-48 y A-49; fuera de alcance, ya apuntado.
> - Technical Debt «Hook local…»: candidata a (b) parcial (`RITUAL.md:348`: «Hay que ejecutarlo cada vez que cambia un hook»), pero le falta la nota del 2026-09-07; niega por defecto es lo correcto.
> - Transcripciones heredadas: medio en `MIRAR-EL-MATERIAL.md:81`; se queda bien (falta «F07 cita solo sobre `tr-*`»).
> - Ninguna otra línea que se quedó debería salir con la evidencia que hay, y ninguna de las que salen debería haberse quedado.
>
> La guardia me bloqueó tres veces (redirección a fichero, `git tag -l`, `for` y comandos encadenados), y reescribí en llamadas separadas.

**Que se hizo con cada hallazgo:**

- **a1 (importa), arreglado:** la fila de A5 en §1.1 dice ahora donde estaba cada pregunta; en
  HISTORIA, que solo se amplia, una nota al final («# Nota a la salida de A5») corrige la cita sin
  tocar el bloque.
- **b1 (importa), arreglado:** §6 lleva el resultado de los dos `make check` y como se sella el
  ultimo; el «Estado» va al final.
- **a2, a3, a4 y b2 (menores), declarados para el consultor:** a2, las dos reglas de operacion
  («una deuda nueva entra con una linea que apunte a su informe; una pagada se borra de aqui» y
  «abrir una ambiguedad anade su fila; cerrarla la quita») quedan en README solo dentro de la cita;
  si el consultor las quiere como texto operativo, es una linea en README. a3 y a4, sin cambio. b2
  es el punto 3 de §0 (CLAUDE.md:154-158).

## Estado

**LISTA PARA REVISION, NO CERRADA.** El punto Y sigue en la Next Action: sale en el commit del
contrato, con la orden de cierre de Aleks (encargo). Nadie ejecuto `motor arnes`.
