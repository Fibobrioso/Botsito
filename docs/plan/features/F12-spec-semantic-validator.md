# F12 · spec-semantic-validator

**Rama:** `feature/F12-spec-semantic-validator` · **Fase:** 2 · **Depende de:** F11 (`stable/F11`, spec 3.0.1)

## Objetivo

Que la spec deje de poder decir cosas incoherentes **entre si**, y que las reglas dejen de ser prosa
que nadie puede comprobar. F11 dejo cada pieza bien citada por separado; F12 valida el conjunto y
convierte los campos ejecutables en algo que el motor de F18-F23 pueda implementar sin interpretar.

Criterio del plan (MASTER_PLAN §A, F12): **"falla nombrando el id"**. Ningun error de esta capa
puede ser un aviso generico: dice `RN-014`, `objetivo_rr` o `A-18`.

## Punto de partida: lo que la auditoria de F11 ya construyo

**Este brief NO empieza en cero.** La auditoria del 2026-09-10 (P1..P14) absorbio buena parte de lo
que el plan asignaba a F12. Lo que YA existe en `main` y no hay que rehacer:

| Comprobacion | Donde |
|---|---|
| cada regla nombra parametros que existen y cita algo que existe | `comprobar_contra` |
| el `literal` de una regla o un termino aparece de verdad en su cita | `comprobar_literales` |
| una regla sobre parametros de entorno declara el ADR que la decide | `comprobar_decisiones` (ADR-0016) |
| una regla VIGENTE no puede nombrar un parametro `UNKNOWN` | `validation/knowledge.py` |
| una magnitud y su base de calculo se nombran juntas | `test_una_base_de_calculo_no_puede_vivir_en_la_prosa` (ADR-0014) |
| un parametro no cita un registro de feedback revocado | `validation/knowledge.py` (P13) |
| los campos ejecutables no llevan cifras, ni en digitos ni en letras | `spec/modelo.py` |
| el hash cubre valor, estado, fuente, huso, titulo, literal, notas y decision | `spec/manifiesto.py` (ADR-0016) |

F12 empieza donde eso termina.

## Alcance cerrado (que SI)

**1. Las reglas dejan de ser prosa.** Es la deuda que el §8 del informe de F11 asigna explicitamente
aqui: *"`cuando` y `entonces` son texto en español: nada garantiza que el motor de F18-F23 implemente
lo que la regla dice"*. MASTER_PLAN §A manda las **tablas de decision** a F12/F22. F12 escribe la
forma; F22 la ejecuta.

**2. Cobertura del registro.** Hoy hay **10 parametros con valor que ninguna regla vigente nombra**:

```
broker_dst · broker_offset_base · cuenta_objetivo · cuenta_pruebas · huso_grafico
instrumento · instrumento_digitos · latencia_ms · modelo_llenado · saldo_inicial_cuenta
```

**Nueve de los diez ya tienen dueno en el plan**: MASTER_PLAN H.2:211 asigna la ficha del
instrumento, el reloj del broker, la cuenta y el modelo de llenado a **F24, F28, F31 y F33**. El
decimo, `huso_grafico`, es documental por ADR-0017. Asi que el punto no es inventarles reglas -eso
seria justo lo que ADR-0016 acaba de impedir leer como palabra del trader- sino que **cada parametro
con valor declare quien lo consume**: una regla vigente, o una funcionalidad posterior con su fila
de H.2. Cinco faltan de verdad, segun la revision: `broker_dst` y `broker_offset_base` en RN-020,
`instrumento_digitos` en RN-026, `modelo_llenado` en RN-011 y una regla de alcance para
`instrumento`. Y el caso simetrico sale gratis: los 6 UNKNOWN explican su motivo en prosa
(`stop_colchon_spread.descripcion` dice "se queda UNKNOWN a proposito"), sin campo que lo declare.

**3. Coherencia entre reglas.** Cuatro reglas vigentes (`RN-005`, `RN-008`, `RN-009`, `RN-018`) no
nombran ningun parametro: son prohibiciones puras. Hay que decidir si eso es legitimo y comprobar lo
que hoy no comprueba nadie: reglas que se contradicen entre si, reglas inalcanzables, y el orden de
precedencia cuando dos aplican al mismo instante.

**4. La fragilidad de los `R-01..R-14`.** La tabla en si **ya estaba escrita** -anexo de
`docs/validation/SESION-01-2026-09-09.md`-, asi que la deuda del §8 de F11 estaba obsoleta y este
punto se reduce: el identificador es **posicional** (`scripts/hoja_sesion_docx.py` numera por indice
sobre `contexto_preguntas.yaml`), vive fuera de `src/` y no tiene test. Insertar o reordenar una
entrada renumera las catorce en silencio y deja el anexo mintiendo. Se arregla con un `id: R-NN`
explicito y un test que lo ate al anexo.

**5. Un comando que lo diga.** `botsito spec check` (o la capa spec de `knowledge validate`) que
enumere los fallos **nombrando el id**, y salga con 1.

## Fuera de alcance (que NO)

- **Ejecutar** las tablas de decision: eso es F18-F23. F12 define y valida la forma.
- Reabrir valores del registro. Un valor solo cambia por feedback o por ADR (ADR-0002).
- Cerrar ambiguedades. A-13, A-14, A-15..A-20 se cierran con el trader o con una medicion (A-11
  figura RESUELTA, aunque el barrido de fidelidad dejo anotado que su valor es una inferencia).
- Los statecharts de jornada y ciclo: son F22.
- `feedback pending` filtrando lo aplicado: deuda de F11, va a F13.
- `mapa_parametros.yaml` y donde vive lo que queda de el: F13.

## Entradas

`knowledge/spec/{strategy_spec,parametros,glossary,ambiguedades,spec_manifest}.yaml` (spec 3.0.1) ·
`knowledge/feedback/**` · `knowledge/evidence/**` · `docs/adr/**` · el informe de la sesion 1 para la
tabla R-NN.

## Salidas (ficheros)

- `src/botsito/spec/` — las comprobaciones nuevas y el esquema de la forma ejecutable.
- `knowledge/spec/strategy_spec.yaml` — las 24 reglas vigentes con su campo ejecutable nuevo.
- `docs/adr/00NN-*.md` — la decision sobre la forma ejecutable de una regla.
- `tests/unit/test_spec.py`, `tests/contract/` — una guardia por comprobacion.
- `docs/validation/F12-spec-semantic-validator.md`.

## Tests

Por **comprobacion**, no por funcion: cada regla semantica nueva trae un caso que la dispara y otro
que no, y el mensaje de error tiene que contener el id. Mas los goldens de la spec real: las 24
reglas vigentes y todos los parametros del registro pasan enteros.

## Criterio de aceptacion

1. `make check` verde, `knowledge validate` incluido.
2. Toda regla vigente tiene forma ejecutable comprobable; ninguna se queda en prosa sin declararlo.
3. Los 10 parametros huerfanos estan resueltos: nombrados por una regla o declarados sueltos con
   motivo.
4. Cada fallo de esta capa nombra el id que lo causa.
5. `spec_version` sube y el hash cubre la forma nueva.

## Riesgos

- **Sobre-formalizar.** Una tabla de decision que no sepa expresar "el precio rompe el extremo
  anterior con mecha" obligara a meter prosa dentro de la tabla, y habremos cambiado el sitio del
  problema. Hay que probar la forma contra las cuatro reglas mas dificiles ANTES de convertir las 24.
- **Duplicar F22.** El limite entre "forma comprobable" y "motor" es fino y el plan lo cruza en
  F12/F22. Si se difumina, F22 se encuentra el trabajo hecho a medias y con otra forma.
- **Congelar una spec que aun se mueve.** A-11, A-13, A-14, A-18 y A-19 siguen abiertas; dos de ellas
  y tres parametros corren con un default nuestro (`reloj_dia_riesgo`,
  `zonas_control_max_por_esquema` y, en cuanto lo cree el piloto, `break_even_criterio_ruptura`).
  Formalizar sobre eso es legitimo, pero la forma tiene que admitir que una regla cambie sin
  reescribirla entera.

## Revision de diseno (agente, antes de programar)

PENDIENTE. Seccion obligatoria desde F05: no se programa hasta que este cerrada, con los hallazgos
aceptados o descartados con su motivo.

### Decisiones del consultor

**D1 · PREDICADOS NOMBRADOS, CON ARGUMENTOS** (cerrada el 2026-09-10; la forma concreta la fija
ADR-0019 tras probarla contra las ocho reglas mas dificiles, donde la version sin argumentos aguanto
UNA). `cuando` y `entonces` se componen de
predicados con nombre, definidos UNA vez en su propio fichero y reutilizados por las reglas:

```yaml
# strategy_spec.yaml — TODO en el mismo fichero: un cuarto romperia el contrato del hash
RN-004:
  cuando:
    todos_de:
      - alcanza: {que: liquidez_m15}
      - cruza:
          que: liquidez_m15
          criterio: liquidez_m15_criterio_toma   # el NOMBRE, nunca el valor
  entonces:
    hace: [{marcar: liquidez_tomada}]

predicados:
  cruza:
    argumentos: [que, criterio]
    cita: fb-2026-09-09-sesion-01-6e15504f
    literal: >-
      ¿Vale con que la vela cierre con el cuerpo por encima del máximo [...] Con cuerpo
```

El ejemplo anterior de este brief era `cierra_con_cuerpo_al_otro_lado`, y **estaba roto**:
`liquidez_m15_criterio_toma` tiene `opciones: [cuerpo, mecha]`, asi que el VALOR quedaba horneado
en el NOMBRE. Si el trader dice "mecha", o el predicado ignora el parametro que declara, o el nombre
miente: dos puertas para el mismo hecho (ADR-0002). Lo encontro la revision de diseno.

Se descarta la **tabla de decision** -que es lo que MASTER_PLAN nombra literalmente- por el riesgo
que este brief ya anotaba: la geometria de velas no cabe en columnas booleanas sin meter prosa dentro
de las celdas, y entonces el problema solo cambia de sitio. Se descarta la **prosa con vocabulario
cerrado** porque deja el peso real en F22 y no cierra la deuda del §8.

**Lo que NO hereda, corregido el 2026-09-10.** El brief afirmaba que un predicado "hereda gratis
las ocho guardias". **Es falso**: no existe ningun tipo `Predicado`, y `comprobar_literales`,
`comprobar_contra` y `comprobar_decisiones` iteran `list[Regla]` y `list[Termino]` y nada mas.
**Cada una de las ocho hay que extenderla**, y eso es trabajo de F12 que el brief daba por hecho. Un
predicado ademas necesita `literal` propio, o la guardia de cita no tendria nada que comparar.

**F22 implementa cada predicado**; ese es el limite. Y tiene una pieza sin dueno que hay que
asignar: F22 es capa `domain`, que no puede importar `botsito.spec` ni `yaml`, asi que **no puede
leer los predicados**. La tabla nombre -> funcion va en `spec/` o en `engine`, y la guardia "todo
predicado declarado tiene implementacion" no puede ser de F12 (la implementacion no existe aun): se
decide si es de F23.

**D2 · PILOTO DE CUATRO, luego el resto** (cerrada el 2026-09-10). Se convierten primero las cuatro
mas dificiles, y solo si la forma las aguanta se hacen las veinte restantes:

| Regla | Por que es dificil |
|---|---|
| RN-003 | sesgo por ruptura del extremo con **mecha**, y un equal no cuenta: geometria pura |
| RN-006 | la orden se reubica **al completarse cada zona de control**: no es por vela ni por tiempo |
| RN-014 | el break even lo dispara la ruptura de una zona que **se forma despues** de la entrada |
| RN-020 | acumulacion con **dos bases distintas** y un corte de dia que es un default nuestro |

Si la forma falla, se cambia habiendo gastado cuatro reglas y no veinticuatro.

### Pendientes, a cerrar CON la evidencia del piloto

- **D3 · ¿Una regla vigente sin parametros es legitima?** Son cuatro (RN-005, RN-008, RN-009,
  RN-018) y todas son prohibiciones puras. Con predicados nombrados es probable que dejen de estar
  vacias -pasan a nombrar predicados en vez de parametros-, asi que la pregunta puede disolverse
  sola. Se decide al terminar el piloto, no antes.
- **D4 · Precedencia** entre reglas que aplican al mismo instante: orden del fichero, campo
  explicito, o error. El piloto incluye RN-020, que es la que mas probablemente choque con otra
  (el freno del dia corta lo que las demas permiten), asi que dara el caso real sobre el que decidir.

**Revision de diseno por agente: PENDIENTE.** El ritual la exige antes de programar.

## Que habilita

**F18-F23** (el motor: por primera vez tendra una spec que puede implementar sin interpretar),
**F26** (medir fidelidad contra reglas comprobables y no contra parrafos) y **F13/F14**, que comparten
el esquema de `knowledge/`.
