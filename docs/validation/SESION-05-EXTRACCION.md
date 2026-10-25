# Sesión 5 con el trader (v15 y v16): la extracción por pregunta

> **PLANTILLA mientras la rama está EN CURSO**: la tabla final (§5) entra con la extracción.

> **Borrador para el consultor. Esta rama NO resuelve nada**: no hay `feedback apply`, ni
> ambigüedades cerradas, ni cambios en la spec, en el motor, en los casos ni en las cifras. Cada
> «resuelve» de abajo es una propuesta sobre lo que dijo el trader; el destino de cada respuesta lo
> decide el consultor en otra rama (V, R4.1; encargo del 2026-10-25,
> `docs/encargos/trabajo-sesion-05.md`).

Rama `trabajo/sesion-05`, abierta el 2026-10-25 desde `main` en `7eef8cf` (commit de estado sobre
el merge `68eaa83`, tag `stable/F38c-guardia-alias`). Tramo R4 de la hoja de ruta (R4.1, NA:V).
Skill `ingerir-sesion`, de principio a fin, para los dos vídeos de la sesión (v15, 2026-10-23, y
v16, 2026-10-25). Plantilla: `SESION-04-EXTRACCION.md`. Tag de cierre previsto:
`stable/F38d-sesion-05`.

## Base comprobada al abrir

- `git fetch --prune origin`; en `main`, `git status --short` vacío.
- `git rev-parse --short main` = `7eef8cf`; `git rev-parse main origin/main` da dos veces
  `7eef8cff93b7d5665a21345c10971ba52de775bd`.
- El último `- Tag: ` de `docs/state/HISTORIA.md` es `stable/F38c-guardia-alias`;
  `git rev-parse "stable/F38c-guardia-alias^{commit}"` = `git rev-parse main^1` =
  `68eaa836b9825cb666420accd5abb3e37438af87`; `git ls-remote --tags origin stable/F38c-guardia-alias`
  da `2de0a82… refs/tags/stable/F38c-guardia-alias` (el objeto del tag anotado). Es también el
  primero de `git tag --list 'stable/*' --sort=-creatordate`.
- CI de `main` sobre su HEAD, una consulta suelta a la API de check-runs con el sha literal:
  `python  completed  success  …/actions/runs/40161007232/…`.
- `git branch --list` solo da `main`; `git ls-remote --heads origin` solo da `refs/heads/main`
  (ningún `fix/*`).
- `scripts/transcribir_sesion.py` de `main`: `"05": {` en la línea 176, `"05": ORDEN_SESION_05` en
  `HOJAS` (línea 212) y `SESION_EN_CURSO = "05"` (línea 214).
- `docs/runbooks/DECISIONES-DE-PROCESO.md`: la entrada `- 2026-10-21 · Para los encargos, dos
  reglas del consultor…` (línea 28).

## 0. Lo primero

### 0.1 Las respuestas de Aleks a las preguntas a) a d) del encargo (2026-10-25), copiadas tal cual

Preguntadas en el terminal antes del registro de v15 y v16 (encargo, «ENTRADAS»). Las cuatro
decisiones numeradas de a) son del consultor y mandan en esta rama:

> a) v15 (23-oct): SÍ. A lo largo del vídeo el trader compartió su FX Replay y enseñó ejemplos de su operativa con JULIO como mes. NO sé qué días de julio enseñó (puede haber días del 18 al 31, que no son de construcción) ni en qué minutos; tampoco recuerdo si en pantalla se veían cifras de resultados. No habló de septiembre, marzo ni diciembre, que yo recuerde.
>    v16 (25-oct): trátalo igual que v15 (puede que también enseñara el replay de julio; no lo recuerdo con seguridad).
>    Decisión del consultor para esto: (1) en esta rama NO se abre NINGÚN fotograma de v15 ni de v16; frames extract y frames check sí se hacen, pero nadie los mira, y las citas salen solo de la filtrada. (2) Las frases que nombren julio con un día, u otro mes fuera de lo libre, las bloquea la cuarentena por condición del guion; verifica en el registro de cada filtrada cuántos bloques cayeron por eso y decláralo. (3) Declara en HOLDOUT-EXPOSICIONES.md, con fecha de hoy, que Aleks vio en directo el replay de julio del trader en las dos grabaciones, días sin precisar. (4) Si en la filtrada aparece un día de julio del 18 en adelante fuera de un bloque en cuarentena, PARADA sin copiarlo.
> b) v15: de S-1 a S-18 en el orden del PDF; S-18 quedó incompleta al final de v15. v16: S-18 se repitió desde el principio y se siguió hasta S-25, y después «Para cerrar». Se hicieron TODAS: no quedó ninguna para WhatsApp ni para la sesión 6. S-17 está entera en v15. S-18 está en los dos vídeos: la respuesta que vale es la de v16; la de v15 se informa como incompleta.
> c) No lo leí, y ya no hace falta: S-24 se le preguntó directamente al trader en esta sesión. Lo que diga en S-24 sustituye al dato de 1:44:49; en el informe, di qué pasa con H con esa respuesta.
> d) No tengo hoja con notas; solo los vídeos.
>
> Además: el trader confirmó por WhatsApp lo de marzo el 2026-10-25 a las 13:58 (Lima). La captura está en corpus/Estrategia del trader/Material adicional de su operativa/Mensajes del trader/mensaje-whatsapp-2026-10-25-1358.png. No la abras ni la registres todavía: el consultor te pasará el texto transcrito en un añadido al encargo.

El añadido llegó el mismo día y está copiado en el encargo como «Ampliación declarada del
2026-10-25: la confirmación escrita de marzo».

Lo que se sigue de ellas:
- **a)** Ningún fotograma de v15 ni de v16 se abre (§2). La cuarentena por condición se mide en el
  registro de cada filtrada, y la exposición del replay de julio se declara en
  `HOLDOUT-EXPOSICIONES.md`. Un día de julio del 18 en adelante fuera de la cuarentena es PARADA.
- **b)** v15 lleva S-1 a S-17 enteras y el arranque de S-18. v16 lleva S-18 entera, S-19 a S-25 y
  «Para cerrar». Nada quedó para WhatsApp ni para la sesión 6, aunque `PREGUNTAS.md:83` lo preveía
  para S-23 y S-18. El código de S-17 se busca igual en las dos filtradas, como pide el encargo.
- **c)** El minuto 1:44:49 de v10 no se leyó: no entra ningún dato de Aleks. S-24 de esta sesión
  sustituye a ese dato.
- **d)** No hay hoja con notas: no entra nada en `Sesiones/`.

## Estado

EN CURSO.
