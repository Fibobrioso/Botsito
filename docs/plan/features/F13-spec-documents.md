# F13 · spec-documents

**Rama:** `feature/F13-spec-documents` · **Depende de:** F11 (y de F12, ya en main)
**Fila del plan:** *"Docs y hoja del trader generados | F11 | anti-deriva | docs = generado"*
**Estado del brief:** revisión de diseño por agente **PENDIENTE**. No se programa hasta cerrarla.

---

## 1. Objetivo

Que **la documentación legible de la estrategia se genere y no se escriba**. Hoy la spec vive en
tres YAML que una máquina valida bien y una persona lee mal; y cada vez que alguien ha copiado a
mano una cifra de ahí a un documento, esa copia se ha quedado vieja. Ha pasado **cinco veces en
nueve días**, documentadas:

| Cuándo | Qué se quedó viejo | Cómo se descubrió |
|---|---|---|
| 2026-09-10 (P8, P11) | el recuento de la spec en el HANDOFF y en el §6 del informe de F11 | un script, no la lectura |
| 2026-09-10 | una tercera copia nació desfasada porque `spec_version` subió dos veces antes del merge | ídem |
| 2026-09-12 | `knowledge/spec/README.md` decía "A-1..A-17" cuando ya iban por A-21 | auditoría de consistencia |
| 2026-09-12 | `knowledge/README.md` decía "24 de estrategia en UNKNOWN desde F10" | auditoría de consistencia |
| 2026-09-12 | `PROJECT_STATE` decía `huso_operativa = Etc/GMT-2`, revertido dos días antes | auditoría de consistencia |

La lección ya está escrita en el repositorio —*"el recuento vivo lo da `botsito spec status` y NO se
copia aquí"*— pero es una regla de disciplina, no un mecanismo. F13 pone el mecanismo.

## 2. Punto de partida: lo que ya existe

**No se empieza en cero.** Conviene saber qué hay antes de diseñar:

| Ya existe | Dónde | Qué aporta a F13 |
|---|---|---|
| `botsito spec status` | `cli.py` | la vista viva de "con qué corre el bot y qué sigue en revisión" |
| `botsito spec check` | `cli.py`, F12 | la capa semántica, con sus siete guardias |
| `spec manifest` + hash sobre los tres ficheros | `spec/manifiesto.py` | cómo se detecta que la spec cambió |
| `kit build` / `kit check` | `cases/paquete.py`, F10 | **el patrón exacto de "generado y comprobable"**: `check` recompone el paquete desde su fuente y lo compara |
| `scripts/hoja_sesion_docx.py` | fuera de `src/` | genera la hoja del trader en Word; F12 le dio ids `R-NN` explícitos y un test de contrato |
| `docs/spec/README.md` | escrito en F01 | ya declara *"Versión legible de `strategy_spec.yaml`, GENERADA por F13. No editar a mano"* |

**El patrón a copiar es `kit check`**, no inventar otro: genera, compara con lo commiteado, y falla
nombrando el fichero que no cuadra.

## 3. Alcance cerrado (qué SÍ)

### 3.1 · Generar `docs/spec/` desde `knowledge/spec/`

Un documento legible por una persona, con la spec entera: las 24 reglas vigentes con su condición,
su acción, sus parámetros y su cita; los parámetros con su valor, estado y de dónde sale; el
glosario; y las ambigüedades abiertas. Con `spec_version` y hash en la cabecera.

**Guardia anti-deriva:** `make check` regenera y compara. Si el fichero commiteado no coincide con
lo que sale de `knowledge/spec/`, falla y dice qué fichero. Es la fila del plan: **docs = generado**.

### 3.2 · La hoja del trader

`scripts/hoja_sesion_docx.py` vive fuera de `src/`, que es lo que el propio brief de F12 señaló y
lo que hizo que sus ids fueran posicionales hasta que se arregló. F13 decide su hogar (ver D3).

### 3.3 · Las tres deudas heredadas

| # | Deuda | De dónde viene | Qué hay que hacer |
|---|---|---|---|
| a | `mapa_parametros.yaml` duplica las `opciones` del registro | F10; la unificación se aplazó aquí | unificar, sin romper la reproducibilidad del paquete histórico de la sesión 1 |
| b | `feedback pending` lista también lo ya aplicado | F11 | que filtre |
| c | las cadenas de `supersede` se comprueban una a una, no como cadena completa | F11 | comprobar la cadena entera |

### 3.4 · Las dos decisiones de método que quedaron abiertas

Vienen de la auditoría de proceso del 2026-09-12 y **no son cosméticas**: las dos afectan a lo que
`spec status` enseña y a lo que F26 podrá demostrar.

**(a) Una ambigüedad que decide el consultor no tiene forma de cerrarse.**
Cuatro documentos dicen que sólo cierra el trader, el modelo sólo conoce `ABIERTA` y `RESUELTA`, y
**A-15, A-16 y A-17 llevan decididas y abiertas desde el 2026-09-09**. Consecuencia hoy: `spec
status` presenta como dudoso lo que está decidido. Propuesta del auditor: estados `DECIDIDA` (con
su ADR y su fecha) y `OBSOLETA` (la pregunta dejó de tener sentido), cada uno con su guardia.

**(b) El feedback no sabe CUÁNDO llegó cada respuesta.**
Los 116 registros se fechan el 2026-09-09 porque el esquema exige que `fecha` sea la de la sesión —
y eso está bien—, pero tres son del 10 y del 11, y el canal sólo vive en prosa libre dentro de
`registrado_por`. Propuesta: `recibido_el` (obligatorio, `>= fecha`) y `procedencia` (enum cerrado:
`trader_grabado` · `trader_hoja` · `trader_escrito` · `referido_por_consultor` ·
`reexpresion_consultor`).
**Cuidado, y es lo que hay que resolver en el diseño:** el id de un registro es el hash de su
contenido y los 116 son inmutables. Un campo obligatorio nuevo cambiaría los ids de todos.

## 4. Fuera de alcance (qué NO)

- **Generar la spec en MQL5** (`Params.mqh`): es F28.
- **Reabrir valores del registro.** Un valor sólo cambia por feedback o por ADR (ADR-0002).
- **Cerrar A-15, A-16 o A-17.** F13 construye el mecanismo; usarlo es una decisión del consultor.
- **La biblioteca de casos y el reparto de mayo**: es F14.
- **Implementar la guarda real del holdout** (hoy stub en `tests/conftest.py`): ADR-0021 la asigna
  a F14.
- Un visor, un HTML, o cualquier cosa que no sea texto versionable y difundible en un `git diff`.

## 5. Entradas y salidas

**Entradas:** `knowledge/spec/{strategy_spec,parametros,glossary,ambiguedades,spec_manifest}.yaml` ·
`knowledge/feedback/**` · `knowledge/cases/kit/mapa_parametros.yaml` · `docs/adr/**`.

**Salidas previstas:** `docs/spec/*.md` (generado) · `src/botsito/spec/documentos.py` ·
cambios en `cli.py` · `knowledge/feedback/README.md` y el esquema · `docs/adr/00NN-*.md` con las dos
decisiones de método · tests · `docs/validation/F13-spec-documents.md`.

## 6. Decisiones a cerrar ANTES de programar

Esto es lo que la revisión de diseño tiene que responder, con evidencia y no con preferencia:

| # | Decisión | Por qué no es obvia |
|---|---|---|
| **D1** | ¿Un solo documento generado o varios? | Uno grande se lee peor pero se compara mejor; varios obligan a decidir qué va en cada uno |
| **D2** | ¿Cómo se comprueba la anti-deriva: regenerar y comparar byte a byte, o comparar el hash? | `kit check` ya resolvió esto una vez y aprendió que "byte a byte" obliga a fijar el orden y el formato |
| **D3** | ¿Dónde vive el generador de la hoja del trader? | Moverlo a `src/` lo mete en `mypy` y en los contratos de importación, pero `test_no_business_literals` prohíbe cifras de negocio en `src/` y la hoja las lleva |
| **D4** | ¿`DECIDIDA` y `OBSOLETA` son estados de la ambigüedad, o un campo aparte (`decision: ADR-NNNN`)? | Un estado cambia la máquina y las guardias; un campo puede convivir con `ABIERTA` y ser más honesto |
| **D5** | ¿`recibido_el` y `procedencia` obligatorios u opcionales? | Obligatorios cambian el id de los 116 registros inmutables. Opcionales dejan el hueco abierto para siempre |
| **D6** | La unificación de `mapa_parametros.yaml`, ¿rompe la reproducción del paquete de la sesión 1? | Ese paquete es la prueba de lo que se le preguntó al trader y `kit check` lo compara |

## 7. Tests

Por **comportamiento**, no por función:

- el documento generado coincide con lo commiteado (anti-deriva), y el mensaje dice qué fichero;
- cambiar un valor en `parametros.yaml` **cambia** el documento generado (si no, la guardia es
  decorativa);
- `feedback pending` no lista lo ya aplicado, y sí lista lo pendiente;
- una cadena de `supersede` con un eslabón roto se denuncia entera;
- los goldens: la spec real entra completa, sin perder ninguna regla ni ningún parámetro.

## 8. Criterio de aceptación

1. `make check` verde, `knowledge validate` y `spec check` incluidos.
2. `docs/spec/` está **generado** y su guardia falla si alguien lo edita a mano o si la spec cambia
   sin regenerarlo.
3. Ninguna cifra viva de la spec se copia a mano en ningún documento nuevo.
4. Las tres deudas heredadas (§3.3) están cerradas o explícitamente reasignadas con su motivo.
5. Las dos decisiones de método (§3.4) tienen su ADR y su guardia, o quedan declaradas como
   decisión pendiente del consultor con lo que eso impide.
6. El paquete histórico de la sesión 1 sigue reproduciéndose igual que hoy.

## 9. Riesgos

| Riesgo | Mitigación |
|---|---|
| Un documento generado que nadie lee: coste sin beneficio | que sustituya a algo que hoy se mantiene a mano, no que se sume |
| La guardia anti-deriva se vuelve ruidosa (falla por formato) y alguien la desactiva | D2; y la lección del repositorio: *"una guardia con falsos positivos se desactiva sola"* |
| Tocar el esquema de feedback rompe los 116 registros inmutables | D5, y decidirlo **antes** de escribir código |
| F13 se convierte en "arreglar todo lo que quedó suelto" | §4 y el criterio 4: lo que no entre, se reasigna con su motivo |

## 10. Qué habilita

**F14** (comparte el esquema de `knowledge/` y necesita `feedback pending` fiable), **F26** (medirá
fidelidad contra una spec que una persona puede leer y auditar) y **F28** (exportará a MQL5 desde la
misma fuente: si el documento legible y el `Params.mqh` salen del mismo sitio, no pueden decir cosas
distintas).

## 11. Revisión de diseño (agente, antes de programar)

**PENDIENTE.** Sección obligatoria desde F05: no se programa hasta que esté cerrada, con los
hallazgos aceptados o descartados con su motivo.
