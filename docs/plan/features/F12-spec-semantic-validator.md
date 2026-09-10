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

Algunos es correcto que esten sueltos (`huso_grafico` es documental por ADR-0017; `latencia_ms` solo
lo usa `modelo_llenado`), pero **nadie lo declara**, asi que no se distingue "suelto a proposito" de
"nos hemos olvidado de una regla". F12 exige que cada parametro con valor este nombrado por una regla
vigente **o** declare por que no.

**3. Coherencia entre reglas.** Cuatro reglas vigentes (`RN-005`, `RN-008`, `RN-009`, `RN-018`) no
nombran ningun parametro: son prohibiciones puras. Hay que decidir si eso es legitimo y comprobar lo
que hoy no comprueba nadie: reglas que se contradicen entre si, reglas inalcanzables, y el orden de
precedencia cuando dos aplican al mismo instante.

**4. La tabla `R-01..R-14` -> `fb-…`.** Deuda declarada en el §8 de F11: el informe de la sesion cita
`R-03` y ninguna regla lo hace, asi que la correspondencia no esta escrita en ningun sitio legible.

**5. Un comando que lo diga.** `botsito spec check` (o la capa spec de `knowledge validate`) que
enumere los fallos **nombrando el id**, y salga con 1.

## Fuera de alcance (que NO)

- **Ejecutar** las tablas de decision: eso es F18-F23. F12 define y valida la forma.
- Reabrir valores del registro. Un valor solo cambia por feedback o por ADR (ADR-0002).
- Cerrar ambiguedades. A-11, A-13, A-14, A-15..A-19 se cierran con el trader o con una medicion.
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
reglas vigentes y los 54 parametros pasan enteros.

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
  (`base_calculo_objetivo`, `reloj_dia_riesgo`) corren con un default nuestro. Formalizar sobre eso es
  legitimo, pero la forma tiene que admitir que una regla cambie sin reescribirla entera.

## Revision de diseno (agente, antes de programar)

PENDIENTE. Seccion obligatoria desde F05: no se programa hasta que este cerrada, con los hallazgos
aceptados o descartados con su motivo.

**Decisiones que hay que cerrar antes**, y que son del consultor:

- **D1 · ¿Que forma ejecutable?** Tabla de decision (condicion -> accion, filas exhaustivas) frente a
  predicados nombrados y compuestos, frente a dejarlo en prosa con una guardia de vocabulario cerrado.
- **D2 · ¿F12 convierte las 24 reglas o solo define la forma y convierte un subconjunto piloto?**
- **D3 · ¿Una regla vigente sin parametros (RN-005, RN-008, RN-009, RN-018) es legitima** o toda regla
  tiene que nombrar al menos uno?
- **D4 · Precedencia.** Si dos reglas aplican al mismo instante, ¿manda el orden del fichero, un campo
  explicito, o es un error que dos apliquen a la vez?

## Que habilita

**F18-F23** (el motor: por primera vez tendra una spec que puede implementar sin interpretar),
**F26** (medir fidelidad contra reglas comprobables y no contra parrafos) y **F13/F14**, que comparten
el esquema de `knowledge/`.
