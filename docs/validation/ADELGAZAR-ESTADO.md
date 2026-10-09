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
| A5 (para la sesion 4) | **(a) sale** | Todo lo que lista entro en docs/sesion-4/PREGUNTAS.md (A-42:37, A-39:120, A-51:177, A-21:199, G-2:222, E-1:269, A-50:277, A-13:337) y se pregunto (`stable/F36v-sesion-04`, SESION-04-EXTRACCION.md §3) |
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
- `make check > make-check.log 2>&1` sobre el arbol de este commit: exit 0, ningun `failed`, linea
  `SELLO` (el resultado de la corrida final, con el informe del revisor pegado, va en «Informe del
  revisor»).
- No hay CI de Linux: la rama no toca hooks, rutas ni plataforma (encargo).

## Estado

**LISTA PARA REVISION, NO CERRADA.** El punto Y sigue en la Next Action: sale en el commit del
contrato, con la orden de cierre de Aleks (encargo). Nadie ejecuto `motor arnes`.
