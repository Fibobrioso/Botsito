# F13 · spec-documents

**Rama:** `feature/F13-spec-documents` · **Depende de:** F11 (y de F12, ya en main)
**Fila del plan:** *"Docs y hoja del trader generados | F11 | anti-deriva | docs = generado"*
**Revisión de diseño:** **CERRADA el 2026-09-12** (dos agentes). D1..D6 decididas abajo.

---

## 1. Objetivo, corregido por la revisión

La primera versión de este brief decía que F13 existe porque copiar cifras a mano falla, y ponía
cinco ejemplos. La revisión comprobó los cinco —**son ciertos**— y encontró el fallo del
razonamiento:

> **Ninguna de esas copias viejas era una copia de `knowledge/spec/` a `docs/spec/`. Todas eran
> prosa narrativa: el HANDOFF, `PROJECT_STATE`, los README, el acta de la sesión 1. Generar
> `docs/spec/` no habría evitado ni una sola.**

Y de paso: eran **seis** copias en **tres** días, no cinco en nueve, y el total documentado pasa de
diez. Además había **cuatro vivas** en el momento de la revisión —incluida una de negocio, el ancla
H4 en un offset fijo que ADR-0017 había revocado— corregidas en `3324e5e`.

Así que el objetivo no es "generar un documento". Es **doble**, y el orden importa:

| | Qué | Por qué |
|---|---|---|
| **A** | que el documento generado **sustituya** a lo que hoy se mantiene a mano | si solo se suma, F13 es coste; solo vale si mata al menos dos copias vivas |
| **B** | extender la guardia anti-copia a los documentos que **sí** llevan cifras vivas | es lo que habría cazado las seis, y el mecanismo ya existe: `test_registro_accessors.py` lo hace con dos documentos desde el 2026-09-10 |

## 2. Punto de partida

| Ya existe | Dónde | Qué aporta |
|---|---|---|
| `spec status` · `spec check` (7 guardias) | `cli.py`, `spec/modelo.py` | la vista viva y la capa semántica |
| hash de la spec | `spec/manifiesto.py` | **cubre tres ficheros: NO cubre `ambiguedades.yaml`** |
| `kit check` | `cases/paquete.py:549` | compara **byte a byte** tras normalizar CRLF, con exenciones nombradas (`DEPENDEN_DE_LAS_RESPUESTAS`, `:50`) |
| **dos guardias anti-copia** | `test_registro_accessors.py:110` y `:170` | vigilan `knowledge/spec/README.md` y el HANDOFF. **El mecanismo existe; es estrecho, no inexistente** |
| generador de la hoja | `scripts/hoja_sesion_docx.py` | ya genera; F12 le puso ids `R-NN` y un test |

**Conflicto de alcance a resolver**: `docs/spec/README.md` promete *"versión legible de
**`strategy_spec.yaml`**"*; `docs/README.md:7` y `MASTER_PLAN:52` prometen *"generada desde
**`knowledge/spec/`**"*. Son dos contratos incompatibles y hay que elegir uno y corregir el otro.

## 3. Alcance cerrado

### 3.1 · Generar `docs/spec/`, y que sustituya

Cuatro documentos, uno por fichero fuente (D1). Y **lo que muere**:

| Muere / se reduce a un puntero | Por qué puede |
|---|---|
| `docs/validation/SESION-01-2026-09-09.md` §2 "La estrategia tal como queda especificada" | es lo que el HANDOFF llama *"el esquema completo de la estrategia"*, se mantiene a mano y **ya ha estado viejo dos veces en dos días** |
| el recuento de `knowledge/spec/README.md:4-7` | hoy lo vigila una regex escrita a mano que ya falló una vez |
| `docs/spec/README.md` | lo reemplaza el índice generado |

**No se tocan**: los ADR y los informes de validación (artefactos fechados), el HANDOFF (narración
con fechas, fuera de la guardia **a propósito**), `PROJECT_STATE` (lo único que puede cambiar en
`main` tras el tag) y `hoja_trader.md` de cada sesión (ya generado e histórico).

### 3.2 · La hoja del trader

**Ya se genera.** Lo que falta es meterla bajo red: se mueve a `src/botsito/cases/hoja_docx.py`
(D3), con lo que entra en `mypy --strict` y en los contratos de importación.

### 3.3 · Las cuatro deudas heredadas

| # | Deuda | Enunciado correcto | De dónde |
|---|---|---|---|
| a | `mapa_parametros.yaml` | unificar `opciones` **y decidir dónde viven `temas` y `ambiguedad`**, que es la mitad grande | F10 · F11 §390 |
| b | `feedback pending` | lista los 70 activos sin mirar si el valor ya llegó al registro | F11 |
| c | cadenas de `supersede` | ~~compara el objetivo solo con el predecesor inmediato~~ **ENUNCIADO FALSO, corregido al hacerlo**: comparar con el predecesor inmediato YA es transitivo, así que la cadena entera habla del mismo objetivo por construcción. El hueco real era el **TIEMPO**: nada impedía que un registro corrigiera a otro POSTERIOR | F11 §388 |
| d | `_ARGS_DE_VALOR` | lista blanca a mano: un argumento fuera de ella admite un valor de negocio crudo (`sentido: alcista` pasa hoy). **Y no era la única puerta**: la auditoría de cierre encontró otras cinco, entre ellas un número crudo (`tope: 9.5`) y una clave estructural (`que: cuerpo`) | F12 §204 |

### 3.4 · Las dos decisiones de método → **ADR + lo mínimo, no reescribir la máquina**

La revisión las acota: son **baratas de decidir y caras de implementar**. F13 construye el
mecanismo; **usarlo sobre A-15/A-16/A-17 es una decisión del consultor y queda fuera** (§4).

## 4. Fuera de alcance

- Generar MQL5 (`Params.mqh`): **F28**.
- Reabrir valores del registro (ADR-0002). **EXCEPCIÓN, decidida el 2026-09-12 y declarada
  aquí**: `filtro_noticias` pasa de `no` a `regla`, cambia de categoría a `prop_firm` y su fuente
  pasa del trader a ADR-0022. No es reabrir un valor del trader —lo que él dijo se conserva
  intacto, y sigue siendo verdad sobre su operativa—: es una restricción de la cuenta a la que va
  el bot, de la misma familia que RN-026 (stops level) y RN-027 (redondeo).
- **Cerrar A-15, A-16 o A-17**: F13 hace el mecanismo; el ADR que las cierra lo escribe el consultor.
- La biblioteca de casos y el reparto de mayo: **F14**.
- La guarda real del holdout (hoy stub): **F14**, por ADR-0021.

## 5. Entradas y salidas

**Entradas:** `knowledge/spec/*.yaml` · `knowledge/feedback/**` · `mapa_parametros.yaml` · `docs/adr/**`.

**Salidas:** `docs/spec/*.md` (generado) · `src/botsito/cases/spec_docs.py` **(no `spec/generador.py`: importa
`cases` y las capas lo prohíben, D3; tampoco `documentos.py`, que ya existe en `comun/`)** · `src/botsito/cases/hoja_docx.py` · `cli.py` ·
`knowledge/spec/ambiguedades.yaml` y su cargador · `knowledge/feedback/` esquema y README ·
`docs/adr/0022-*.md` y `0023-*.md` · tests · `docs/validation/F13-spec-documents.md`.

## 6. Las seis decisiones, CERRADAS

| # | Decisión | Evidencia que la cierra |
|---|---|---|
| **D1** | **Cuatro documentos**, uno por fichero fuente | los tamaños no se parecen (830 / 1.021 / 315 / 119 líneas) y, sobre todo, **el hash cubre tres ficheros y no `ambiguedades.yaml`**: una cabecera con hash mentiría sobre una cuarta parte |
| **D2** | **Regenerar y comparar byte a byte**, con exenciones nombradas | es lo que `kit check` ya sostuvo en producción (`paquete.py:549`). El hash **no sirve**: no cubre las ambigüedades, se calcula sobre la estructura re-serializada y no sobre los bytes, y no dice nada del feedback |
| **D3** | **`src/botsito/cases/hoja_docx.py`** | medido: **una** ofensa de literales (`EURUSD`, que debe leerse del registro), **cero** errores de `mypy --strict`, ruff ya la cubre. Pero importa `cases`, y las capas prohíben que un módulo de `spec/` lo haga |
| **D4** | **Estado `DECIDIDA`** (no un campo), con `decision: ADR-NNNN` y `decidida_el`. **`OBSOLETA` no** | las dos revisiones discreparon y decide el código: `cuestionario.py:123` mete en el cuestionario de la sesión siguiente toda `ABIERTA`, así que un campo dejaría que **se le vuelva a preguntar al trader lo que el consultor ya decidió**. `OBSOLETA` no tendría ningún ocupante hoy |
| **D5** | **Opcionales en el esquema, obligatorios por guardia desde `2026-09-13`** | medido sobre los 116 reales: **0 ids cambian** si son opcionales (`contenido_canonico` salta el campo ausente, igual que con `valor_canonico` en F11); **116 de 116 dejan de cargar** si son obligatorios, porque `_validar` revienta antes del hash |
| **D6** | **Unificar es seguro. La premisa era falsa** | `cuestionario.yaml` y `hoja_trader.md` ya están exentos por "sesión celebrada"; `kit check` da exit 0 con dos AVISOS **hoy**, antes de tocar nada. El docstring que decía lo contrario está caduco. **Pero** al borrar `opciones` desaparece el test que las cruza: hay que reponerlo contra el paquete commiteado |

## 7. Tests

- el documento generado coincide con lo commiteado, y el mensaje dice **qué fichero**;
- cambiar un valor en `parametros.yaml` **cambia** el generado (si no, la guardia es decorativa);
- `feedback pending` no lista lo ya aplicado;
- una corrección que llega **antes que lo que corrige** se denuncia (ver (c): el enunciado original de este punto era falso);
- `DECIDIDA` exige un ADR **que exista y que nombre el id**, y no vale sobre una `bloqueante`;
- `recibido_el`/`procedencia` se exigen desde el corte y no antes; los 116 conservan su id;
- goldens: la spec real entra entera.

## 8. Criterio de aceptación

1. `make check` verde, `knowledge validate` y `spec check` incluidos.
2. `docs/spec/` generado, con guardia que falla si se edita a mano o si la spec cambia sin regenerar.
3. **Al menos dos copias vivas mueren** (§3.1): el §2 del acta y el recuento del README.
4. Las **cuatro** deudas de §3.3 cerradas o reasignadas con su motivo.
5. `DECIDIDA` y los dos campos del feedback existen **con su guardia**, no solo en el esquema.
6. El paquete histórico de la sesión 1 sigue dando exit 0 en `kit check`.
7. Los 116 registros de feedback conservan su id. Se comprueba.

## 9. Riesgos

| Riesgo | Mitigación |
|---|---|
| **Generar dentro de `docs/` choca con el ritual**: tras el tag, en `main` solo puede cambiar `PROJECT_STATE.md`, y un `docs(...)` en `main` ya puso la CI en rojo dos veces | regenerar **solo** dentro de la rama; la guardia comprueba, no escribe |
| `make check` no tiene dónde colgar la guardia (no hay target `docs`) | test de contrato, que ya es un marcador declarado |
| Un documento que nadie lee | criterio 3: si no mata dos copias vivas, F13 no está hecha |
| La guardia se vuelve ruidosa y alguien la desactiva | exenciones **nombradas y razonadas**, como `paquete.py:574-588` |
| Unificar `opciones` borra la única guardia cruzada | reponerla contra el paquete commiteado (D6) |
| F13 se convierte en "arreglar todo lo suelto" | §4 y el criterio 4 |

## 10. Qué habilita

**F14** (comparte esquema y necesita `feedback pending` fiable), **F26** (medirá contra una spec
auditable, y `recibido_el` le da la única frase que puede sostener mecánicamente: qué valores se
fijaron **antes** de la exposición del holdout del 2026-09-11 y cuáles después) y **F28**.

## 11. Fuera de F13, pero se hace antes: A-14

No necesita ninguna de las dos decisiones. Está **respondida de hecho** desde el 2026-09-10 —lo dice
su propio texto: *"Sigue ABIERTA solo por forma: falta su frase, no la respuesta"*— y se cierra hoy
con un `RESOLVE_UNKNOWN` referido, exactamente como se cerró A-11. Hacerlo primero deja el problema
en su tamaño real (**tres** ambigüedades del consultor, no cuatro) y estrena la guardia de RESUELTA
que se añadió el 2026-09-12.
