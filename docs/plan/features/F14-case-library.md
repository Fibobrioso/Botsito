# F14 · case-library

**Rama:** `feature/F14-case-library` · **Depende de:** F09, F11, F15 (fila del plan: *"Casos
ejecutables con tres particiones reservadas (holdout-1/2/3) · guarda de holdout por audit hook ·
runner independiente"*)
**Revisión de diseño:** PENDIENTE.

> **F14a se separó de aquí el 2026-09-21** (rama `feature/F14a-ingesta-del-detalle`, ADR-0037,
> informe `docs/validation/F14A-INGESTA.md`). F14a construye **sólo la ingesta del detalle por
> operación**: el lector único del libro (`corpus/libro.py`), los días que se DERIVAN del reparto en
> vez de elegirse, la forma del caso en `knowledge/cases/dev/` y la guardia de que ningún caso
> reservado viva ahí. **No toma D1**: el caso guarda las operaciones que el material dice, y el
> `no_trade` por ausencia sigue siendo una inferencia nuestra sin ADR que la decida (ADR-0016). Y
> resolvió por medida algo que esta página daba por hecho: **el xlsx no registra el objetivo
> planeado** —ninguna columna lo es— porque el objetivo es la regla `objetivo_rr`
> (`ev-v2-001658-d02fb71a`, ADR-0037 §7 y su corrección).

---

## 1. Qué problema resuelve, y cuál NO

El proyecto entero descansa en una promesa: *"verificable caso a caso contra sus decisiones"*
(PROJECT_STATE, Project Goal). Hoy esa promesa no tiene dónde apoyarse. Existe la spec ejecutable
(F12), existe el dataset congelado (F15) y existe el material del trader, pero **no existe un solo
caso**: ni un formato, ni un fichero, ni nada que pueda decir "este día el trader hizo esto".

Lo que F14 **no** resuelve: comparar el bot con el trader. Eso es F26, y necesita un motor que
todavía no existe (F18-F24). F14 construye **la biblioteca y el banco de pruebas**, no el veredicto.

Esta distinción es la que decide casi todo lo demás y hay que tenerla delante: **el runner de F14
no ejecuta la estrategia, porque no hay estrategia que ejecutar**. Ejecuta *algo* que recibe un
caso y devuelve decisiones, y hoy ese algo solo puede ser un doble de prueba.

## 2. Punto de partida: lo que ya hay, medido

| Qué | Dónde | Estado |
|---|---|---|
| Universo decidido | ADR-0025 | **6 días `dev` de mayo**: 2026-05-08, 05-12, 05-15, 05-18, 05-20, 05-28. 13 de holdout (6/4/3). Junio fuera |
| Reparto sellado | `knowledge/cases/kit/2026-09-09-sesion-01/particiones.yaml` | se reproduce byte a byte y **no se toca** |
| OHLC congelado de mayo | `data/manifests/eurusd-m1-2026-05-03d048ed.yaml` | mes entero, con hash |
| Decisiones del trader en mayo | `corpus/.../Backtest mayo 2026/backtesting-analytics MAYO 2026.xlsx` | 68 operaciones **de los 19 días**, dev y holdout mezclados en el mismo fichero |
| Carpetas previstas | `knowledge/cases/{dev,holdout/1,holdout/2,holdout/3,fixtures}` | declaradas en el README y en MASTER_PLAN §59; **vacías** |
| Guarda de holdout | `tests/conftest.py:18` | **STUB**: devuelve `None`. PROJECT_STATE la daba por viva y no lo está (ADR-0021) |
| Etiquetas de sesión | `LABEL_CASE` | **CERO registros**. El kit se diseñó para producirlas y la sesión 1 no las produjo |

## 3. Las preguntas que la revisión de diseño tiene que cerrar

### D1 · ¿De dónde sale la verdad de un caso: del xlsx o de `LABEL_CASE`?

Son dos fuentes con naturalezas distintas y el kit está construido para la segunda:

- **el xlsx de mayo** trae lo que el trader hizo *de verdad* backtesteando: 68 operaciones con sus
  precios. Es material rico, pero no dice nada de los días en los que **no** operó, y "no operar"
  es una decisión de la estrategia (RN-022, `comportamiento_sin_regla`);
- **`LABEL_CASE`** es la gramática que F10 diseñó (`07-11: venta@08:37 e=...; 11-15: no_trade`),
  cubre las dos sesiones de cada día incluido el `no_trade`, y tiene `kappa` para medir su
  consistencia. No existe ni uno.

**Hay que elegir una como fuente primaria y decir qué se hace con la otra.** Si es el xlsx, hay que
derivar los `no_trade` por ausencia, y eso es una inferencia nuestra sobre la operativa del trader:
exactamente la clase de cosa que ADR-0016 obliga a declarar.

### D2 · ¿Qué es un caso: un día o una operación?

La partición asigna **días** (`particiones.yaml`), la ventana tiene **dos sesiones** (07-11 y
11-15) y el xlsx tiene **operaciones**. Un día con dos operaciones, ¿es un caso o dos? De esto
depende el formato, el runner y lo que F26 pueda medir después.

### D3 · El xlsx contiene los 13 días de holdout. ¿Cómo se impide leerlos?

Es el riesgo más concreto de toda la funcionalidad: **la verdad de los días reservados vive en el
mismo fichero que la de los días `dev`**, y `HOLDOUT-EXPOSICIONES.md` §3 dice que ese detalle por
operación no se abre sin autorización y sin `PREREGISTRO.md` commiteado.

Hace falta decidir si la ingesta filtra por día y descarta el resto sin escribirlo en ningún sitio,
o si se materializa todo y la guarda vigila la lectura. **Lo primero es más difícil de estropear.**

### D4 · La guarda del holdout: ¿qué vigila exactamente y cómo?

> **HECHO fuera de F14 (2026-09-17, rama `trabajo/guarda-de-holdout`, ADR-0033).** Hook de auditoría `autouse` para cualquier llamante, visto saltar por cada vía de lectura; una puerta en `botsito.cases.holdout` para todo lo que abra, con autorización commiteada y `PREREGISTRO.md` relleno; y `kit build` / `kit check` que declaran las velas que leen. F14 NO rehace esto: lo usa. Lo que le queda a F14 es que su ingesta del xlsx pase por la puerta (D3).

El stub promete *"fallará si cualquier módulo bajo `botsito.spec` o `botsito.domain` abre un fichero
de `knowledge/cases/holdout/`"*. Hay que decidir el mecanismo (¿`sys.audit` hook? ¿un `open`
envuelto? ¿`autouse` en toda la suite?) y, sobre todo, **probar que salta**: una guarda de holdout
que no se ha visto fallar nunca no es una guarda. Es la lección que F13 aprendió con las tres
guardias de `DECIDIDA`, que corrían sobre el repositorio real sin que nadie comprobara que saltaban.

### D5 · ¿Qué ejecuta el runner, si el motor es F18-F24?

Opciones que la revisión debe pesar: un `Protocol` con un doble de prueba; un runner que solo
valide el formato y los fixtures; o posponer el runner entero a F18. **La fila del plan lo pide
como entregable de F14** (*"runner independiente"*), así que posponerlo hay que justificarlo.

### D6 · ¿Los fixtures OHLC se copian o se referencian?

`knowledge/cases/fixtures/` promete *"instantáneas OHLC/ticks con hash"*, y el dataset de mayo ya
está congelado con su manifiesto en `data/`, que **no está en git**. Copiar seis días de M1 a
`knowledge/` los mete en el repositorio y los hace reproducibles sin `data/`; referenciarlos deja
la biblioteca inútil en una máquina limpia. Hay que medir cuánto ocupan seis días antes de decidir.

## 4. Fuera de alcance

- **Medir fidelidad**: F26, y exige `PREREGISTRO.md` commiteado antes (ADR-0021).
- **Abrir cualquier partición de holdout**, incluido el detalle por operación de esos 13 días.
- **El motor**: F18-F24.
- **Reparticionar mayo** (ADR-0025) o tocar el paquete de la sesión 1.
- **El mes limpio** que se le pidió al trader: cuando llegue, entra como paquete nuevo.

## 5. Criterio de aceptación (borrador, la revisión lo afina)

1. `make check` verde.
2. Existen los 6 casos `dev` de mayo, con su formato declarado y validado por un cargador estricto.
3. **La guarda del holdout salta**, y hay un test que la ve saltar. Deja de ser un stub. **HECHO en la rama de la guarda (ADR-0033):** `tests/unit/test_guarda_holdout.py` y `tests/unit/test_puerta_holdout.py`.
4. Ningún fichero de `knowledge/cases/holdout/` se lee en toda la suite, y se comprueba.
5. El `no_trade` está representado explícitamente, no por ausencia de fila.
6. Cada caso dice de dónde sale su verdad, con el mismo régimen de cita que el resto del proyecto.

## 6. Riesgos

| Riesgo | Por qué duele |
|---|---|
| Abrir holdout sin darse cuenta al ingerir el xlsx | irreversible: quema una de las tres particiones, y solo hay tres |
| Inferir `no_trade` por ausencia y llamarlo "lo que hizo el trader" | mete una inferencia nuestra en el sitio donde va su decisión (ADR-0016) |
| Seis casos | con seis días no se sostiene ninguna afirmación estadística. El brief de F14 debe decirlo donde se vea |
| Un runner sin motor que acabe siendo andamiaje muerto | se escribe una vez y se tira en F18 |

## 7. Qué habilita

**F18-F20** (los casos de sesgo verdes son su puerta), **F26** (fidelidad) y **F28** (fixtures
generados para MQL5).
